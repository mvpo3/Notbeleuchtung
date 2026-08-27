"""position_resolver.py - Position-Resolver `wall_ref -> (x_mm, y_mm)`
(Slice 11.5.0).

ERSTER Konsument des Wall-Resolvers (Slice 11.4.0). Berechnet aus einer
``wall_ref`` plus ``room_walls`` plus ``room_polygon`` die konkrete
Symbol-Position auf der gemappten Wand.

MVP-Subdivision (4 aktive Strategien):
- ``_position_longest_wall`` fuer ``wall_bwu_*`` (43 Live-Decisions)
- ``_position_near_window`` fuer ``wall_top_window`` (6, braucht
  ``WindowOpeningIndex``)
- ``_position_not_a_wall`` fuer ``ceiling_*``, ``door_frame`` (43,
  Polygon-Centroid-Approximation)
- Passthrough fuer ``needs_furniture`` (39) und ``needs_door_anchor`` (7)

``near_door_*``-Strategy ist Slice 11.5.1 nach DoorOpening-Modell-
Erweiterung um ``hinge_xy`` + ``handle_side_xy``. Heute referenziert
``DoorOpening`` nur ``polygon_mm`` ohne Lock-/Hinge-Diskriminierung -
deshalb hier explizit als ``STATUS_POS_NEEDS_DOOR_ANCHOR`` gepunted.

Sibling-Aware: Live-Pre-Read zeigt 28/101 Gruppen mit >=2 Decisions auf
gleicher (apt, room, wall_ref) - max 4 Sockets auf wall_bwu_distributed
in Wohnzimmer. ``position_index`` + ``siblings_count`` distribieren
gleichmaessig entlang der Wand.

Konsumenten-Touch in dieser Slice: null. ``coordinate_assigner.py``
blieb parallel-existent bis zur Konsumenten-Migration in 11.8.0 und
wurde in Slice 11.8.2 sunset (M2 Phase 8 finalisiert).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from typing import Optional

from engine.walls.door_opening import DoorOpening
from engine.walls.door_opening_index import DoorOpeningIndex, point_in_polygon
from engine.walls.resolver import (
    STATUS_AMBIGUOUS,
    STATUS_NEEDS_CORNER_ANCHOR,
    STATUS_NEEDS_FURNITURE,
    STATUS_NOT_A_WALL_ANCHOR,
    STATUS_NOT_FOUND,
    STATUS_OK,
    STATUS_UNKNOWN_REF,
    resolve_wall_ref,
)
from engine.walls.wall import Wall
from engine.walls.opening_bridge import (
    DEFAULT_OPENING_CLEARANCE_MM,
    distribute_distance_avoiding_openings,
    nearest_distance_avoiding_openings,
    opening_free_length,
)
from engine.walls.window_opening_index import WindowOpeningIndex

# ---- MVP-Defaults (Fachpraxis, no LB-override yet) -------------------

# Inset vom Wand-Ende zur Vermeidung von Eckpositionen (mm).
CORNER_INSET_MM: float = 200.0
# Perpendiculaerer Inset Wand -> Raum-Inneres (mm).
# Slice 11.9.0: 50 -> 150. Pre-Read zeigte E_Steckdose+Schalter
# median = 50mm = PERP_INSET_MM exakt; bei DEFAULT_WALL_THICKNESS_MM=200
# (Halbwand 100mm) sitzt das Symbol IN der Wand-Geometrie. Neu: 100mm
# Halbwand + 50mm Sicherheits-Inset = 150mm (analog WINDOW_PERP_INSET_MM
# aus Slice 11.7.0).
PERP_INSET_MM: float = 150.0
# Edge-Toleranz fuer Polygon-Containment-Filter (mm).
ROOM_POLYGON_EDGE_TOL_MM: float = 100.0
# Sibling-Jitter-Step fuer ceiling/door_frame (mm).
NOT_A_WALL_JITTER_MM: float = 100.0
# Slice 11.5.1: Distanz vom handle_side-Anker entlang Wand-Richtung (mm).
NEAR_DOOR_OFFSET_MM: float = 250.0
# Slice 18.13.0: Perp-Inset für near_door_outside — über die Türaußenkante
# hinaus klar auf die Flurseite (größer als PERP_INSET_MM, das nur ins
# Rauminnere reicht). Klingel/ATÖ-Taster „vor der Wohnungstür".
OUTSIDE_PERP_INSET_MM: float = 180.0
# Slice 16.6.0: Abstand zwischen Geschwister-Symbolen an DERSELBEN Tür entlang
# der Wand (entstapelt GSP/Klingel/Schalter am selben Eingang). position_index=0
# + siblings_count=1 → kein Offset (bestehendes Verhalten unverändert).
NEAR_DOOR_SIBLING_SPACING_MM: float = 200.0
# Slice vr-room-polygon-fix: synthetische Handle-Offset entlang Wand wenn
# eine Tuer kein handle_side_xy aufgeloest hat (~halbe Standard-800mm-Tuer).
# Konsistent mit replay/position_estimator._position_near_door (400mm).
SYNTH_HANDLE_HALF_WIDTH_DEFAULT_MM: float = 400.0
# Slice C3-near-door-centroid-rescue: wenn KEIN Tuer-Handle im Raum-Polygon
# liegt (handle_side_pos zeigt vom Raum weg / wall_bbox-Polygon ist lose),
# rette ueber die Tuer mit min Polygon-Distanz (= raum-eigene Tuer) + Inset
# Richtung Centroid. MAX_DIST faengt die raum-eigene Tuer (lose bbox: ~700mm)
# und schliesst Nachbar-/ferne Tueren aus (>=1.2m). INSET_MARGIN schiebt
# ueber die Polygon-Grenze hinaus komfortabel ins Rauminnere.
RESCUE_MAX_DOOR_DIST_MM: float = 1200.0
RESCUE_INSET_MARGIN_MM: float = 400.0
# Slice 11.5.2: Inset von Polygon-Ecke Richtung Centroid (Verteiler-Eck-Anker).
# Konsistent zum near_corner-Default der M2-Vorgaenger-Pipeline
# (coordinate_assigner.near_corner, sunset in Slice 11.8.2).
CORNER_ANCHOR_INSET_MM: float = 300.0
# Verteiler-Co-Location: E- + Medienverteiler teilen wall_corner_or_door_adjacent
# und gehoeren NEBENEINANDER an EINE Ecke (Platzierungsregel: nebeneinander wenn
# Platz, sonst uebereinander). Abstand entlang der Wand ~ Verteiler-Breite.
VERTEILER_SIBLING_SPACING_MM: float = 400.0
# Slice 18.7.0: Abstand des ersten Verteilers vom Eingangstuer-Anker entlang der
# Eingangswand (haelt Verteiler aus dem Tuer-Schwung). Video-Regel v2_vorraum #1:
# Verteiler nebeneinander an der Wand beim Wohnungseingang. Geometrie = Track A.
ENTRANCE_VERTEILER_DOOR_CLEARANCE_MM: float = 400.0
# Slice 11.7.0: Perpendiculaerer Inset fuer ``_position_near_window``.
# Window-Centroid liegt typisch AUF der Wand-Mittellinie
# (DEFAULT_WALL_THICKNESS_MM=200, Halbwand=100). PERP_INSET_MM=50 reicht
# nicht ins Raum-Inneres - Symbol landet IM Window-Polygon (Live: 5/97
# wall_top_window-Decisions kollidieren mit Window-Aussparung).
# WINDOW_PERP_INSET_MM = 100mm Halbwand + 50mm Sicherheits-Inset.
WINDOW_PERP_INSET_MM: float = 150.0
# Geometrischer Abstand zu Tuer-/Fensteroeffnungen fuer Placement-Skip.
# Bewusst keine Norm-Zahl: nur ein Kollisions-/Darstellungsabstand.
OPENING_CLEARANCE_MM: float = DEFAULT_OPENING_CLEARANCE_MM
# Slice 2.33.0: Der Opening-Span-Nudge darf nur entlang der Wand schieben AUF
# der das Symbol tatsaechlich sitzt. Auf 1/2OG tragen die (fragmentierten)
# Tuer-Wandstuecke oft keine opening_spans — die "naechste" Span-Wand war dann
# eine FERNE Querwand und der Escape teleportierte das Symbol quer durch den
# Raum (A_2+3-WOHNZIMMER-RT: 4,4 m neben der Referenz). Schranke = Halbwand
# dicker Waende (~150) + PERP_INSET + Reserve.
OPENING_NUDGE_WALL_MAX_DIST_MM: float = 300.0

# ---- Status constants ------------------------------------------------

STATUS_POS_OK = "pos_ok"
STATUS_POS_NEEDS_DOOR_ANCHOR = "pos_needs_door_anchor"
STATUS_POS_NEEDS_FURNITURE = "pos_needs_furniture"
STATUS_POS_NO_WALL_FOUND = "pos_no_wall_found"
STATUS_POS_UNKNOWN_REF = "pos_unknown_ref"


# ---- Result dataclass ------------------------------------------------


@dataclass(frozen=True)
class PositionResult:
    """Ausgang einer Position-Resolution.

    Felder
    ------
    x_mm, y_mm
        Symbol-Mittelpunkt in mm-Welt. None bei NEEDS_*-Status.
    z_mm
        Slice 11.6.0: Symbol-Unterkante (UK) in mm ueber FFB. Pass-
        through aus ``PlacementDecision.height_uk_mm`` (Caller liefert
        via ``resolve_position(height_uk_mm=...)`` aus dem
        HeightResolver-Stack: LB-Override -> Fachpraxis -> Default).
        Fallback auf ``height_ok_mm`` wenn UK None (z.B. Verteiler).
        None bei NEEDS_*-Status oder wenn beide Hoehen fehlen.
    rotation_deg
        Slice 11.6.0: Symbol-Rotation in Grad. atan2(normal_into_room)
        in deg fuer Strategien mit Wand-Kontext (longest_wall,
        near_door, near_window). 0.0 fuer Decken-/Eck-Strategien
        (ceiling, door_frame, corner_anchor). None fuer Passthrough.
    wall
        Gemappte Wand (aus ``ResolveResult.wall``) bei
        ``STATUS_POS_OK`` mit longest_wall- oder near_window-Strategy.
        None bei not_a_wall (Polygon-Centroid) und allen
        Passthrough-Status.
    status
        Eines der ``STATUS_POS_*``.
    reason
        Frei-Text-Detail (z.B. ``longest_wall_distributed``,
        ``ceiling_uses_room_centroid``,
        ``door_frame_uses_room_centroid_approximation``,
        ``needs_door_anchor:near_door_lock_side``,
        ``needs_furniture_geometry:wall_appliance_mid``).
    """

    x_mm: Optional[float]
    y_mm: Optional[float]
    wall: Optional[Wall]
    status: str
    reason: str
    # Slice 11.6.0: z + rotation (backward-compat via Optional + None default)
    z_mm: Optional[int] = None
    rotation_deg: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "x_mm": self.x_mm,
            "y_mm": self.y_mm,
            "z_mm": self.z_mm,
            "rotation_deg": self.rotation_deg,
            "wall_id": self.wall.id if self.wall else None,
            "status": self.status,
            "reason": self.reason,
        }


# ---- Geometry helpers (inline, kein cross-package coupling) ----------


def _polygon_centroid(
    polygon: list[tuple[float, float]],
) -> tuple[float, float]:
    """Signed-area-weighted Centroid; Vertex-Mittel als Fallback."""
    n = len(polygon)
    if n < 3:
        return (0.0, 0.0)
    cx = cy = signed_area_2 = 0.0
    for i in range(n):
        x0, y0 = polygon[i]
        x1, y1 = polygon[(i + 1) % n]
        cross = x0 * y1 - x1 * y0
        signed_area_2 += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    if abs(signed_area_2) < 1e-9:
        return (
            sum(p[0] for p in polygon) / n,
            sum(p[1] for p in polygon) / n,
        )
    factor = 1.0 / (3.0 * signed_area_2)
    return (cx * factor, cy * factor)


def _point_to_segment_dist(
    point: tuple[float, float],
    a: tuple[float, float],
    b: tuple[float, float],
) -> float:
    px, py = point
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    seg_len_sq = dx * dx + dy * dy
    if seg_len_sq < 1e-9:
        return math.hypot(px - ax, py - ay)
    t = max(
        0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / seg_len_sq)
    )
    fx, fy = ax + t * dx, ay + t * dy
    return math.hypot(px - fx, py - fy)


def _polygon_min_dist(
    point: tuple[float, float],
    polygon: list[tuple[float, float]],
) -> float:
    """0 wenn drin, sonst Distanz zur naechsten Kante."""
    if len(polygon) < 3:
        return math.inf
    if point_in_polygon(point, tuple(polygon)):
        return 0.0
    best = math.inf
    n = len(polygon)
    for i in range(n):
        d = _point_to_segment_dist(
            point, polygon[i], polygon[(i + 1) % n]
        )
        if d < best:
            best = d
    return best


_ROTATION_SNAP_TOL_DEG: float = 5.0


def _snap_to_90(deg: float, tol_deg: float = _ROTATION_SNAP_TOL_DEG) -> float:
    """Slice 11.9.0: Snap-to-nearest-90 fuer Symbol-Rotationen.

    Wand-Normal-Berechnung produziert kleinen Float-Drift (0.3-0.7 deg)
    und folgt auch echten leicht-schraegen Waenden exakt (Live: 3.4 deg
    bei E_Schalter 86.3 / 183.4). Beide Klassen werden zu 0/90/180/270
    gesnapped wenn innerhalb tol_deg. Echte Diagonal-Waende > tol_deg
    bleiben unangetastet (Pass-Through, falls 11.9.1 sie unterstuetzen
    will). Output ist im DXF-Range [0, 360)."""
    snapped = round(deg / 90.0) * 90.0
    if abs(deg - snapped) < tol_deg:
        return snapped % 360
    return deg % 360


def _rotation_into_room_deg(
    wall_unit: tuple[float, float],
    anchor_xy: tuple[float, float],
    room_centroid: tuple[float, float],
) -> float:
    """Slice 11.6.0: Symbol-Rotation in Grad. Symbol 'schaut' senkrecht
    von der Wand weg ins Raum-Inneres - Rotation = atan2 des Normal-
    Vektors. Vorzeichen-Flip via Centroid-Test (analoge Konvention zur
    M2-Vorgaenger-Pipeline ``distribute_along_wall`` und der
    longest_wall-Strategie hier).

    Slice 11.9.0: Snap-to-nearest-90 am Ende (tol 5 deg) - eliminiert
    Float-Drift und leicht-schraege-Wand-Artefakte (siehe ``_snap_to_90``)."""
    ux, uy = wall_unit
    nx, ny = -uy, ux
    if (
        nx * (room_centroid[0] - anchor_xy[0])
        + ny * (room_centroid[1] - anchor_xy[1])
    ) < 0.0:
        nx, ny = -nx, -ny
    return _snap_to_90(math.degrees(math.atan2(ny, nx)))


def _point_in_polygon_with_tol(
    point: tuple[float, float],
    polygon: list[tuple[float, float]],
    tol_mm: float,
) -> bool:
    """True wenn Punkt im Polygon liegt ODER innerhalb ``tol_mm`` der
    Boundary. Slice 11.5.1: gemeinsames Pattern fuer near_door und
    near_window - Anker-Punkte (handle_side_xy, window_centroid) liegen
    typisch direkt auf der Wand-Mittellinie und damit auf der
    Polygon-Grenze. Strict ``point_in_polygon`` ist Ray-Casting-flaky
    auf der Boundary."""
    return _polygon_min_dist(point, polygon) <= tol_mm


# ---- Public helpers --------------------------------------------------


def filter_walls_by_room_polygon(
    walls: list[Wall],
    room_polygon: list[tuple[float, float]],
    *,
    edge_tol_mm: float = ROOM_POLYGON_EDGE_TOL_MM,
) -> list[Wall]:
    """Filtere Walls deren Mittelpunkt im Raum-Polygon ODER auf der
    Polygon-Grenze (innerhalb ``edge_tol_mm``) liegt.

    Notwendig weil ``Wall.room_id == None`` fuer alle 772 Live-Walls
    (Loader setzt es nicht). Border-Walls haben Mittelpunkte direkt
    auf der Polygon-Boundary - reines ``point_in_polygon`` gibt dort
    Ray-Casting-Inkonsistenz, deshalb Distanz-basierter Filter.
    """
    if len(room_polygon) < 3:
        return []
    out: list[Wall] = []
    for w in walls:
        probes = [
            (
                (w.start_xy[0] + w.end_xy[0]) / 2.0,
                (w.start_xy[1] + w.end_xy[1]) / 2.0,
            ),
            w.start_xy,
            w.end_xy,
            *w.source_midpoints,
        ]
        if any(_polygon_min_dist(p, room_polygon) <= edge_tol_mm for p in probes):
            out.append(w)
    return out


def _mountable_walls(walls: list[Wall]) -> list[Wall]:
    """Walls eligible as electrical mount targets."""
    return [w for w in walls if not w.no_mount]


def _nearest_mountable_wall(forced_wall: Wall, walls: list[Wall]) -> Wall | None:
    if not walls:
        return None
    anchor = (
        (forced_wall.start_xy[0] + forced_wall.end_xy[0]) / 2.0,
        (forced_wall.start_xy[1] + forced_wall.end_xy[1]) / 2.0,
    )
    return min(
        walls,
        key=lambda w: _point_to_segment_dist(anchor, w.start_xy, w.end_xy),
    )


# ---- Public dispatcher ------------------------------------------------


def resolve_position(
    wall_ref: Optional[str],
    room_walls: list[Wall],
    room_polygon: list[tuple[float, float]],
    *,
    window_index: Optional[WindowOpeningIndex] = None,
    door_index: Optional[DoorOpeningIndex] = None,
    position_index: int = 0,
    siblings_count: int = 1,
    height_uk_mm: Optional[int] = None,
    height_ok_mm: Optional[int] = None,
    target_door: Optional[DoorOpening] = None,
    forced_wall: Optional[Wall] = None,
) -> PositionResult:
    """Resolve eine ``wall_ref`` zu konkreter ``(x_mm, y_mm, z_mm, rotation_deg)``.

    Parameters
    ----------
    wall_ref
        String aus ``PlacementDecision.wall_ref``.
    room_walls
        Subset der globalen ``list[Wall]`` (gefiltert via
        ``filter_walls_by_room_polygon``).
    room_polygon
        Raum-Polygon in mm-Welt fuer Centroid-Fallback und Inset-
        Richtung.
    window_index
        Optional - benoetigt fuer ``wall_top_window``.
    door_index
        Optional - benoetigt fuer ``near_door_*`` / ``wall_*_door``
        (Slice 11.5.1). Wenn None, fallen near_door-Refs auf
        ``STATUS_POS_NEEDS_DOOR_ANCHOR`` (11.5.0-Verhalten).
    position_index
        Index des Symbols innerhalb seiner sibling-Gruppe (0-based).
    siblings_count
        Gesamtzahl der Symbole mit gleicher ``wall_ref`` im selben
        Raum (>=1).
    height_uk_mm, height_ok_mm
        Slice 11.6.0: Pass-through aus
        ``PlacementDecision.height_uk_mm`` / ``height_ok_mm`` (vom
        HeightResolver-Stack). Nicht hier neu resolved - z = UK wenn
        gesetzt, sonst OK, sonst None.

    Strategie
    ---------
    Step 1: ``resolve_wall_ref`` aus 11.4.0 klassifiziert die
    ``wall_ref``. Step 2: Position-Strategy via Status-Dispatch.
    Step 3: z + rotation_deg in Strategy-Result gesetzt (Slice 11.6.0).
    """
    if siblings_count < 1:
        siblings_count = 1
    if position_index < 0:
        position_index = 0

    # Slice 11.6.0: z = UK bevorzugt, OK als Fallback (z.B. Verteiler).
    z_mm = height_uk_mm if height_uk_mm is not None else height_ok_mm
    mountable_room_walls = _mountable_walls(room_walls)

    # Slice 18.18.3 Step 5: Wand-Wahl-Regel hat eine konkrete Wand vorgegeben
    # (Consumer wählt via wall_roles aus function/room → wall_role). Positionierung
    # = bestehende longest_wall-Mathematik auf DIESER Wand (Last-Mile unverändert).
    # Nur für wand-anker-Symbole; near-door/ceiling kommen hier nicht an (Consumer
    # übergibt forced_wall nur für die wand-anker-Familien).
    if forced_wall is not None and not forced_wall.no_mount:
        return replace(
            _position_longest_wall(
                wall=forced_wall, room_polygon=room_polygon,
                position_index=position_index, siblings_count=siblings_count,
                z_mm=z_mm,
            ),
            reason="wall_choice_rule_forced",
        )
    if forced_wall is not None and forced_wall.no_mount:
        fallback_wall = _nearest_mountable_wall(forced_wall, mountable_room_walls)
        if fallback_wall is None:
            return PositionResult(
                x_mm=None, y_mm=None, wall=None,
                status=STATUS_POS_NO_WALL_FOUND,
                reason=f"no_mount_forced_wall_no_fallback:{forced_wall.id}",
            )
        result = _position_longest_wall(
            wall=fallback_wall, room_polygon=room_polygon,
            position_index=position_index, siblings_count=siblings_count,
            z_mm=z_mm,
        )
        return replace(
            result,
            reason=f"no_mount_forced_wall_skipped:{forced_wall.id}:{result.reason}",
        )

    res = resolve_wall_ref(wall_ref, mountable_room_walls)

    if res.status in (STATUS_OK, STATUS_AMBIGUOUS):
        # Wall-Resolver liefert STATUS_OK nur fuer wall_bwu_* heute.
        return _position_longest_wall(
            wall=res.wall,
            room_polygon=room_polygon,
            position_index=position_index,
            siblings_count=siblings_count,
            z_mm=z_mm,
        )

    if res.status == STATUS_NOT_A_WALL_ANCHOR:
        return _position_not_a_wall(
            wall_ref=(wall_ref or "").strip(),
            room_polygon=room_polygon,
            position_index=position_index,
            z_mm=z_mm,
        )

    if res.status == STATUS_NEEDS_FURNITURE:
        # Slice 11.8.x: Routing zu existierenden Strategien
        # (B3-Hybrid-Schuld aus 11.8.0 aufgeloest).
        # Historischer Pre-Read (M2 Vorgaenger-Pipeline, sunset in
        # 11.8.2) hatte fuer NEEDS_FURNITURE-wall_refs HETEROGENE
        # Buckets:
        #   wall_appliance_*, worktop_wall_bwm -> bucket=wall_bwu
        #     -> distribute_along_wall(longest_wall)  [24 Live-Decisions]
        #   wall_high_bwo, wall_mid_inner       -> bucket=wall_high
        #     -> near_corner(polygon)                  [15 Live-Decisions]
        # Routing reuse-t _position_longest_wall + _position_corner_anchor
        # (gleiche Mathematik wie M2-Vorgaenger-Pipeline -> 0 Drift).
        wr_norm = (wall_ref or "").lower().strip()

        # Cluster 1: Geraete/Worktop -> longest_wall
        if (
            wr_norm.startswith("wall_appliance")
            or wr_norm == "worktop_wall_bwm"
        ):
            if not mountable_room_walls:
                reason = (
                    f"furniture_proxy:no_room_walls:{wr_norm}"
                    if not room_walls
                    else f"furniture_proxy:no_mountable_room_walls:{wr_norm}"
                )
                return PositionResult(
                    x_mm=None, y_mm=None, wall=None,
                    status=STATUS_POS_NEEDS_FURNITURE,
                    reason=reason,
                )
            # Fix 2.6.1-Folge: "längste Wand" kann ein geteiltes Segment sein,
            # das den Raum gar nicht berührt (A_26: Streuner 5,7 m über der
            # WOHNKÜCHE). Wahl-Kriterium = größte ÜBERLAPPUNG der Raum-
            # Projektion auf der Wandachse; Länge nur als Tie-Break. Ohne
            # nutzbare Überlappung (kein Polygon) → Alt-Verhalten längste.
            def _room_overlap(w):
                s0, s1 = _room_span_on_wall(w, room_polygon)
                return max(0.0, s1 - s0)

            sorted_walls = sorted(
                mountable_room_walls,
                key=lambda w: (_room_overlap(w), w.length_mm),
                reverse=True,
            )
            result = _position_longest_wall(
                wall=sorted_walls[0],
                room_polygon=room_polygon,
                position_index=position_index,
                siblings_count=siblings_count,
                z_mm=z_mm,
            )
            return replace(
                result,
                reason=f"furniture_proxy:longest_wall:{result.reason}",
            )

        # Cluster 2: wall_high_bwo / wall_mid_inner -> corner_anchor
        if wr_norm in ("wall_high_bwo", "wall_mid_inner"):
            result = _position_corner_anchor(
                wall_ref=wr_norm,
                room_polygon=room_polygon,
                position_index=position_index,
                z_mm=z_mm,
            )
            return replace(
                result,
                reason=f"furniture_proxy:corner_anchor:{result.reason}",
            )

        # Defensive: unbekannter NEEDS_FURNITURE-wall_ref (sollte nicht
        # auftreten - Live-Pre-Read deckt 6/6 wall_refs ab).
        return PositionResult(
            x_mm=None, y_mm=None, wall=None,
            status=STATUS_POS_NEEDS_FURNITURE,
            reason=f"furniture_proxy:unknown_pattern:{wr_norm}",
        )

    if res.status == STATUS_NEEDS_CORNER_ANCHOR:
        return _position_corner_anchor(
            wall_ref=(wall_ref or "").strip(),
            room_polygon=room_polygon,
            position_index=position_index,
            z_mm=z_mm,
        )

    if res.status == STATUS_UNKNOWN_REF:
        return PositionResult(
            x_mm=None, y_mm=None, wall=None,
            status=STATUS_POS_UNKNOWN_REF,
            reason=res.reason,
        )

    # STATUS_NOT_FOUND: differenziere via reason
    if res.status == STATUS_NOT_FOUND:
        if res.reason.startswith("needs_door_context"):
            if door_index is not None:
                near_res = _position_near_door(
                    wall_ref=(wall_ref or "").strip(),
                    room_polygon=room_polygon,
                    door_index=door_index,
                    z_mm=z_mm,
                    target_door=target_door,
                    position_index=position_index,
                    siblings_count=siblings_count,
                )
                return _nudge_result_out_of_opening(
                    near_res, mountable_room_walls, room_polygon
                )
            return PositionResult(
                x_mm=None, y_mm=None, wall=None,
                status=STATUS_POS_NEEDS_DOOR_ANCHOR,
                reason=res.reason,
            )
        if res.reason.startswith("needs_window_context"):
            return _position_near_window(
                room_polygon=room_polygon,
                window_index=window_index,
                position_index=position_index,
                z_mm=z_mm,
            )
        # empty_room_walls (oder andere)
        return PositionResult(
            x_mm=None, y_mm=None, wall=None,
            status=STATUS_POS_NO_WALL_FOUND,
            reason=res.reason,
        )

    # Defensive - sollte nicht erreichbar sein
    return PositionResult(
        x_mm=None, y_mm=None, wall=None,
        status=STATUS_POS_UNKNOWN_REF,
        reason=f"unhandled_status:{res.status}",
    )


# ---- Private strategies -----------------------------------------------


def _room_span_on_wall(wall, room_polygon) -> tuple[float, float]:
    """Projektion des Raum-Polygons auf die Wandachse → (span0, span1) in
    Wand-Distanz-Koordinaten, geclippt auf [0, length]. span0 > span1 =
    Raum liegt komplett außerhalb der Wand (disjunkt). Leeres/degeneriertes
    Polygon → (0, length) = ganze Wand nutzbar (Alt-Verhalten)."""
    if len(room_polygon) < 3:
        return (0.0, wall.length_mm)
    ux, uy = wall.unit_vector
    ts = [
        (p[0] - wall.start_xy[0]) * ux + (p[1] - wall.start_xy[1]) * uy
        for p in room_polygon
    ]
    return (max(0.0, min(ts)), min(wall.length_mm, max(ts)))


def _position_longest_wall(
    wall: Optional[Wall],
    room_polygon: list[tuple[float, float]],
    position_index: int,
    siblings_count: int,
    z_mm: Optional[int] = None,
) -> PositionResult:
    """Distribute entlang der laengsten Wand mit Corner-Inset und
    perpendiculaerem Raum-Inset.

    Position-Formel:
        t = (position_index + 0.5) / siblings_count   if siblings_count > 1
        t = 0.5                                        if siblings_count == 1
        usable = max(length - 2*CORNER_INSET, 0)
        d = CORNER_INSET + t * usable                  (clamped to [0, length])
        along = wall.point_at_distance(d)
        normal = perpendicular(unit_vector), Richtung -> Centroid
        position = along + PERP_INSET_MM * normal
    """
    if wall is None:
        return PositionResult(
            x_mm=None, y_mm=None, wall=None,
            status=STATUS_POS_NO_WALL_FOUND,
            reason="longest_wall_resolver_returned_none",
        )

    length = wall.length_mm
    d_safe = distribute_distance_avoiding_openings(
        wall,
        position_index,
        siblings_count,
        corner_inset_mm=CORNER_INSET_MM,
        clearance_mm=OPENING_CLEARANCE_MM,
    )
    if d_safe is None:
        if not wall.opening_spans:
            d = length / 2.0
        else:
            return PositionResult(
                x_mm=None, y_mm=None, wall=wall,
                status=STATUS_POS_NO_WALL_FOUND,
                reason="longest_wall_no_opening_free_span",
            )
    else:
        d = d_safe

    # Fix 2.6.1-Folge: Wände können weit über den Raum hinauslaufen (geteilte
    # Segmente) — Distributions-Positionen dann außerhalb der Wohnung (A_26:
    # Streuner 5,7 m über der WOHNKÜCHE). Clamp von d auf die Projektion des
    # Raum-Polygons auf die Wandachse (+Corner-Inset), wenn die Spanne nutzbar.
    span0, span1 = _room_span_on_wall(wall, room_polygon)
    if span1 - span0 >= 2 * CORNER_INSET_MM:
        d = min(max(d, span0 + CORNER_INSET_MM), span1 - CORNER_INSET_MM)

    along_x, along_y = wall.point_at_distance(d)
    ux, uy = wall.unit_vector
    nx, ny = -uy, ux

    centroid = _polygon_centroid(room_polygon)
    if (
        nx * (centroid[0] - along_x) + ny * (centroid[1] - along_y)
    ) < 0.0:
        nx, ny = -nx, -ny

    rot = _rotation_into_room_deg(
        wall.unit_vector, (along_x, along_y), centroid
    )

    return PositionResult(
        x_mm=along_x + PERP_INSET_MM * nx,
        y_mm=along_y + PERP_INSET_MM * ny,
        z_mm=z_mm,
        rotation_deg=rot,
        wall=wall,
        status=STATUS_POS_OK,
        reason=(
            "longest_wall_distributed_opening_skip"
            if wall.opening_spans else "longest_wall_distributed"
        ),
    )


def _position_near_window(
    room_polygon: list[tuple[float, float]],
    window_index: Optional[WindowOpeningIndex],
    position_index: int = 0,
    z_mm: Optional[int] = None,
) -> PositionResult:
    """``wall_top_window`` - Symbol ueber dem Fenster im Raum.

    Pickt das erste Window dessen Polygon-Centroid im Raum-Polygon
    liegt. Position = Window-Centroid + PERP_INSET nach Raum-Inneres.
    """
    if window_index is None:
        return PositionResult(
            x_mm=None, y_mm=None, wall=None,
            status=STATUS_POS_NO_WALL_FOUND,
            reason="window_index_required_for_wall_top_window",
        )

    candidates: list[tuple[tuple[float, float], tuple[float, float], float]] = []
    for w in window_index._openings:
        win_centroid = _polygon_centroid(list(w.polygon_mm))
        # Slice 11.5.1: Edge-Tolerance fuer Aussenwand-Fenster -
        # Window-Centroid liegt typisch auf Wand-Mittellinie, also
        # auf der Polygon-Grenze.
        if not _point_in_polygon_with_tol(
            win_centroid, room_polygon, ROOM_POLYGON_EDGE_TOL_MM
        ):
            continue

        # Slice 11.7.0 Layer 1.5: Inset entlang Polygon-kurzer-Achse
        # statt Centroid-Richtung. Window-Polygone sind 200mm ×
        # Fenster-Breite (Live: 207×1401, 200×1200 etc.) -
        # Centroid-Richtung kann entlang der LANGEN Achse zeigen,
        # dann reicht WINDOW_PERP_INSET_MM nicht aus dem Polygon
        # heraus (Live-Befund 2/5 Kollisionen vor 1.5).
        wp = w.polygon_mm
        xs = [p[0] for p in wp]
        ys = [p[1] for p in wp]
        bbox_w = max(xs) - min(xs)
        bbox_h = max(ys) - min(ys)
        if bbox_w <= bbox_h:
            short_unit = (1.0, 0.0)
            short_len = bbox_w
        else:
            short_unit = (0.0, 1.0)
            short_len = bbox_h

        # Sign-Flip: short_unit muss ins Raum-Inneres zeigen.
        # Test-Offset short_len/2 + 10mm = klar ausserhalb Polygon.
        test_offset = short_len / 2.0 + 10.0
        test_pt = (
            win_centroid[0] + short_unit[0] * test_offset,
            win_centroid[1] + short_unit[1] * test_offset,
        )
        if not point_in_polygon(test_pt, tuple(room_polygon)):
            short_unit = (-short_unit[0], -short_unit[1])

        # Inset-Magnitude skaliert mit echter Wand-Stärke pro Window:
        # Halbwand + 50mm Sicherheits-Inset, mind. WINDOW_PERP_INSET_MM.
        # Standard 200mm-Wand: max(150, 100+50) = 150 (kein Drift fuer
        # die 3/5 axis-aligned Faelle die schon resolven).
        # Dicke 300mm-Wand:    max(150, 150+50) = 200 (skaliert).
        inset = max(WINDOW_PERP_INSET_MM, short_len / 2.0 + 50.0)

        # Symbol-Rotation: schaut senkrecht von der Wand weg = entlang
        # short_axis_unit. Konsistent zu longest_wall + near_door wo
        # Rotation aus Wand-Normal kommt (NICHT mehr Centroid-Richtung).
        rot = math.degrees(math.atan2(short_unit[1], short_unit[0]))

        candidates.append((win_centroid, short_unit, inset))

    if candidates:
        # Multiple JAL / Sonnenschutzanschluesse in one room must not collapse
        # onto the first window. Use a deterministic window order and the
        # sibling position index from the placement group.
        candidates.sort(key=lambda row: (row[0][1], row[0][0]))
        idx = min(max(position_index, 0), len(candidates) - 1)
        win_centroid, short_unit, inset = candidates[idx]
        rot = math.degrees(math.atan2(short_unit[1], short_unit[0]))
        return PositionResult(
            x_mm=win_centroid[0] + short_unit[0] * inset,
            y_mm=win_centroid[1] + short_unit[1] * inset,
            z_mm=z_mm,
            rotation_deg=rot,
            wall=None,
            status=STATUS_POS_OK,
            reason=f"near_window_short_axis_inset:window_index={idx}",
        )

    return PositionResult(
        x_mm=None, y_mm=None, wall=None,
        status=STATUS_POS_NO_WALL_FOUND,
        reason="no_window_in_room_polygon",
    )


def _position_not_a_wall(
    wall_ref: str,
    room_polygon: list[tuple[float, float]],
    position_index: int,
    z_mm: Optional[int] = None,
) -> PositionResult:
    """``ceiling_*`` und ``door_frame`` - Polygon-Centroid mit
    Sibling-Jitter. Slice 11.6.0: rotation = 0 (keine Wand-Orientierung)."""
    cx, cy = _polygon_centroid(room_polygon)
    x = cx + position_index * NOT_A_WALL_JITTER_MM
    y = cy

    wr = wall_ref.lower().strip()
    if wr.startswith("ceiling"):
        reason = f"ceiling_uses_room_centroid:{wr}"
    elif wr == "door_frame":
        reason = "door_frame_uses_room_centroid_approximation"
    else:
        reason = f"non_wall_anchor_centroid:{wr}"

    return PositionResult(
        x_mm=x, y_mm=y,
        z_mm=z_mm, rotation_deg=0.0,
        wall=None,
        status=STATUS_POS_OK,
        reason=reason,
    )


def _door_half_width(
    polygon_mm: tuple[tuple[float, float], ...] | list[tuple[float, float]],
    wall_unit: tuple[float, float],
) -> float:
    """Halbe Tuer-Spanne entlang ``wall_unit``, abgeleitet aus ``polygon_mm``
    (Tuer-Aussparung = Breite x Wand-Staerke). Fallback auf
    ``SYNTH_HANDLE_HALF_WIDTH_DEFAULT_MM`` wenn Polygon fehlt oder die
    abgeleitete Spanne unplausibel ist (<300 oder >1500mm)."""
    if not polygon_mm or wall_unit is None:
        return SYNTH_HANDLE_HALF_WIDTH_DEFAULT_MM
    projs = [p[0] * wall_unit[0] + p[1] * wall_unit[1] for p in polygon_mm]
    span = max(projs) - min(projs)
    if 300.0 <= span <= 1500.0:
        return span / 2.0
    return SYNTH_HANDLE_HALF_WIDTH_DEFAULT_MM


def _door_anchor(
    door: DoorOpening,
) -> Optional[tuple[float, float, float, float]]:
    """``(handle_x, handle_y, wall_unit_x, wall_unit_y)`` einer Tür, oder None.

    Nutzt ``handle_side_xy`` wenn gesetzt (Drehtür/WET), sonst synthetisiert
    es aus ``hinge + wall_unit * half_width`` (Schiebetür ohne Lock-Seite).
    Ohne ``wall_unit`` — oder ohne ``hinge`` bei fehlendem handle — None."""
    if door.wall_unit_xy is None:
        return None
    handle = door.handle_side_xy
    if handle is None:
        if door.hinge_xy is None:
            return None
        half_w = _door_half_width(door.polygon_mm, door.wall_unit_xy)
        handle = (door.hinge_xy[0] + door.wall_unit_xy[0] * half_w,
                  door.hinge_xy[1] + door.wall_unit_xy[1] * half_w)
    return (handle[0], handle[1], door.wall_unit_xy[0], door.wall_unit_xy[1])


def _door_anchor_hinge(
    door: DoorOpening,
) -> Optional[tuple[float, float, float, float]]:
    """``(hinge_x, hinge_y, -wall_unit_x, -wall_unit_y)`` einer Tür, oder None.

    Türleiste = Band-/Scharnierseite (gegenüber der Öffnungs-/Griffseite). Der
    Anker liegt am ``hinge_xy``; das negierte ``wall_unit`` schiebt das Symbol
    in ``_near_door_result`` von der Türöffnung WEG (auf die Leistenseite),
    statt zur Klinke hin. Für den Freilauftürschließer."""
    if door.wall_unit_xy is None or door.hinge_xy is None:
        return None
    ux, uy = door.wall_unit_xy
    return (door.hinge_xy[0], door.hinge_xy[1], -ux, -uy)


def _near_door_result(
    anchor: tuple[float, float, float, float],
    wr: str,
    centroid: tuple[float, float],
    position_index: int,
    z_mm: Optional[int],
) -> PositionResult:
    """Symbol-Position aus Tür-Anker: Offset entlang der Wand (inkl. Sibling-
    Spacing — Slice 16.6.0) + ``PERP_INSET_MM`` ins Rauminnere. Reason-Strings
    rückwärtskompatibel zu Slice 11.5.1."""
    hx, hy, ux, uy = anchor
    if wr == "near_door_hinge_side":
        # Türleiste: fix am Scharnier (kein Sibling-Spread — Freilauf ist allein).
        off = NEAR_DOOR_OFFSET_MM
    else:
        # position_index=0 + siblings → kein Sibling-Offset (Alt-Verhalten).
        off = NEAR_DOOR_OFFSET_MM + position_index * NEAR_DOOR_SIBLING_SPACING_MM
    along_x = hx + off * ux
    along_y = hy + off * uy
    nx, ny = -uy, ux
    # Normal ins Rauminnere (Richtung Centroid).
    if nx * (centroid[0] - along_x) + ny * (centroid[1] - along_y) < 0.0:
        nx, ny = -nx, -ny
    # Slice 18.13.0: near_door_outside → auf die FLURSEITE (Normal umkehren, weg
    # vom Centroid, größerer Inset über die Türaußenkante hinaus). Symbol schaut
    # in den Flur (Klingel/ATÖ-Taster vor der Wohnungstür).
    outside = wr == "near_door_outside"
    if outside:
        nx, ny = -nx, -ny
        perp = OUTSIDE_PERP_INSET_MM
        facing_ref = (along_x + nx * 1000.0, along_y + ny * 1000.0)
    else:
        perp = PERP_INSET_MM
        facing_ref = centroid
    if wr == "wall_corner_or_door_adjacent":
        reason = "wall_corner_or_door_adjacent_handle_side_offset"
    elif wr == "wall_mid_near_door":
        reason = "wall_mid_near_door_handle_side_offset"
    elif wr == "near_door_hinge_side":
        reason = "near_door_hinge_side_offset"
    elif outside:
        reason = "near_door_outside_offset"
    else:
        reason = f"near_door_handle_side_offset:{wr}"
    rot = _rotation_into_room_deg((ux, uy), (along_x, along_y), facing_ref)
    return PositionResult(
        x_mm=along_x + perp * nx,
        y_mm=along_y + perp * ny,
        z_mm=z_mm,
        rotation_deg=rot,
        wall=None,
        status=STATUS_POS_OK,
        reason=reason,
    )


def _nudge_result_out_of_opening(
    result: PositionResult,
    room_walls: list[Wall],
    room_polygon: list[tuple[float, float]],
) -> PositionResult:
    """Move a door-adjacent result out of a logical opening span if needed."""
    if (
        result.status != STATUS_POS_OK
        or result.x_mm is None
        or result.y_mm is None
        or not room_walls
    ):
        return result
    point = (result.x_mm, result.y_mm)
    opening_walls = [w for w in room_walls if w.opening_spans]
    if not opening_walls:
        return result
    wall = min(
        opening_walls,
        key=lambda w: _point_to_segment_dist(point, w.start_xy, w.end_xy),
    )
    # Slice 2.33.0: sitzt das Symbol gar nicht auf dieser Wand, ist der
    # Span-Test (nur ALONG-Projektion) bedeutungslos — nicht nudgen.
    if _point_to_segment_dist(
        point, wall.start_xy, wall.end_xy
    ) > OPENING_NUDGE_WALL_MAX_DIST_MM:
        return result
    ux, uy = wall.unit_vector
    d = (point[0] - wall.start_xy[0]) * ux + (point[1] - wall.start_xy[1]) * uy
    hit = None
    for span in wall.opening_spans:
        s = span.normalized()
        if s.start_mm - OPENING_CLEARANCE_MM <= d <= s.end_mm + OPENING_CLEARANCE_MM:
            hit = s
            break
    if hit is None:
        return result
    centroid = _polygon_centroid(room_polygon)
    direction = 1.0 if d <= (hit.start_mm + hit.end_mm) / 2.0 else -1.0
    if result.reason.startswith("near_door_hinge_side_offset"):
        # Hinge-side symbols belong on the door-leaf/hinge side.  When the
        # anchor lies inside the logical opening span, escape away from the
        # opening-side stack so FLTS does not collapse onto KL/ATÖ outside.
        direction = -direction
    safe_d = nearest_distance_avoiding_openings(
        wall,
        d,
        direction=direction,
        corner_inset_mm=CORNER_INSET_MM,
        clearance_mm=OPENING_CLEARANCE_MM,
    )
    if safe_d is None:
        return result
    along_x, along_y = wall.point_at_distance(safe_d)
    nx, ny = -uy, ux
    if nx * (centroid[0] - along_x) + ny * (centroid[1] - along_y) < 0.0:
        nx, ny = -nx, -ny
    return replace(
        result,
        x_mm=along_x + PERP_INSET_MM * nx,
        y_mm=along_y + PERP_INSET_MM * ny,
        wall=wall,
        reason=f"{result.reason}:opening_span_nudged",
    )


def _position_near_door(
    wall_ref: str,
    room_polygon: list[tuple[float, float]],
    door_index: DoorOpeningIndex,
    z_mm: Optional[int] = None,
    *,
    target_door: Optional[DoorOpening] = None,
    position_index: int = 0,
    siblings_count: int = 1,
) -> PositionResult:
    """``near_door_*``, ``wall_mid_near_door`` (Slice 11.5.1 + 16.6.0).

    Slice 16.6.0: ``target_door`` (Zirkulations-Routing aus
    ``near_door_routing``) wird — wenn gesetzt — direkt verankert; sonst die
    erste Tür mit Handle im Raum-Polygon (Alt-Verhalten). ``position_index`` /
    ``siblings_count`` verteilen Geschwister an DERSELBEN Tür entlang der Wand
    (entstapelt GSP/Klingel/Schalter). Schiebetüren (kein handle_side, aber
    hinge+wall_unit) bekommen einen synthetischen Handle.
    """
    if len(room_polygon) < 3:
        return PositionResult(
            x_mm=None, y_mm=None, wall=None,
            status=STATUS_POS_NO_WALL_FOUND,
            reason=f"empty_room_polygon:{wall_ref}",
        )

    wr = wall_ref.lower().strip()
    centroid = _polygon_centroid(room_polygon)
    # Türleiste-Ref (Freilauftürschließer) → Anker am hinge_xy statt handle_side.
    anchor_fn = _door_anchor_hinge if wr == "near_door_hinge_side" else _door_anchor

    # Slice 16.6.0: explizit zugewiesene Ziel-Tür direkt verankern.
    if target_door is not None:
        anchor = anchor_fn(target_door)
        if anchor is not None:
            return _near_door_result(anchor, wr, centroid, position_index, z_mm)
        # unbrauchbares Target → unten auf Heuristik/Rescue fallen

    for door in door_index._openings:
        anchor = anchor_fn(door)
        if anchor is None:
            continue
        # Slice 11.5.1: Edge-Tolerance — handle liegt typisch auf der
        # Wand-Mittellinie und damit auf der Polygon-Grenze des Raums.
        if not _point_in_polygon_with_tol(
            (anchor[0], anchor[1]), room_polygon, ROOM_POLYGON_EDGE_TOL_MM
        ):
            continue
        return _near_door_result(anchor, wr, centroid, position_index, z_mm)

    # Slice C3-near-door-centroid-rescue: kein Handle landete im Raum-Polygon
    # (handle_side_pos zeigt oft vom Raum weg, wall_bbox-Polygon ist lose).
    # Rette ueber die Tuer mit minimaler Polygon-Distanz (= raum-eigene Tuer)
    # und setze das Symbol vom Tuer-Centroid Richtung Raum-Centroid ins Innere
    # (Centroid ist immer innen — unabhaengig vom verdrehten handle_side und
    # der losen bbox). Working near-door-Faelle returnen oben und erreichen
    # diesen Punkt nie. Exakte Wand-Anlage ist NICHT das Ziel (Polygon-Lift
    # B' Backlog) — plausibel im richtigen Raum nahe der Tuer reicht.
    best: tuple[float, tuple[float, float]] | None = None
    for door in door_index._openings:
        poly = door.polygon_mm
        if not poly:
            continue
        ax = sum(p[0] for p in poly) / len(poly)
        ay = sum(p[1] for p in poly) / len(poly)
        dist = _polygon_min_dist((ax, ay), room_polygon)
        if best is None or dist < best[0]:
            best = (dist, (ax, ay))
    if best is not None and best[0] <= RESCUE_MAX_DOOR_DIST_MM:
        dist, (ax, ay) = best
        vx, vy = centroid[0] - ax, centroid[1] - ay
        vnorm = math.hypot(vx, vy)
        if vnorm > 1e-6:
            ux, uy = vx / vnorm, vy / vnorm
            step = dist + RESCUE_INSET_MARGIN_MM
            rx, ry = ax + ux * step, ay + uy * step
            # In Raum-bbox klemmen (garantiert in-room trotz loser Geometrie)
            xs = [p[0] for p in room_polygon]
            ys = [p[1] for p in room_polygon]
            m = 100.0
            rx = max(min(xs) + m, min(max(xs) - m, rx))
            ry = max(min(ys) + m, min(max(ys) - m, ry))
            return PositionResult(
                x_mm=rx, y_mm=ry, z_mm=z_mm, rotation_deg=0.0,
                wall=None, status=STATUS_POS_OK,
                reason=f"door_centroid_rescue:{wr}",
            )

    return PositionResult(
        x_mm=None, y_mm=None, wall=None,
        status=STATUS_POS_NEEDS_DOOR_ANCHOR,
        reason=f"no_door_with_handle_in_room_polygon:{wr}",
    )


def _position_corner_anchor(
    wall_ref: str,
    room_polygon: list[tuple[float, float]],
    position_index: int,
    z_mm: Optional[int] = None,
) -> PositionResult:
    """``wall_corner_or_door_adjacent`` (Slice 11.5.2) - Verteiler-Eck-
    Anker.

    Strategie analog zum near_corner-Pattern der M2-Vorgaenger-Pipeline
    (sunset in 11.8.2): pickt eine Polygon-Ecke und setzt den Symbol-
    Anker mit ``CORNER_ANCHOR_INSET_MM``-Inset Richtung Centroid (Symbol
    sitzt im Raum-Inneren, nicht auf der Polygon-Grenze).

    Sibling-Aware: ``position_index % len(corners)`` verteilt mehrere
    Verteiler im selben Raum auf verschiedene Ecken (Live: A1/VR hat
    e_verteiler + schwachstrom_verteiler nebeneinander - sollten nicht
    auf derselben Position landen).

    Slice 11.6.0: rotation = 0.0 MVP. Wand-Eck-Heuristik (welche der 2
    angrenzenden Waende gibt die Symbol-Orientierung?) ist Backlog
    fuer 11.8.0 wenn DXF-INSERT-Visualisierung das nahelegt.
    """
    if len(room_polygon) < 3:
        return PositionResult(
            x_mm=None, y_mm=None, wall=None,
            status=STATUS_POS_NO_WALL_FOUND,
            reason=f"empty_room_polygon:{wall_ref}",
        )

    n = len(room_polygon)
    cx, cy = _polygon_centroid(room_polygon)
    wr = (wall_ref or "").lower().strip()

    # Verteiler-Co-Location: e_verteiler + schwachstrom_verteiler teilen
    # wall_corner_or_door_adjacent → an EINER Ecke nebeneinander entlang der
    # laengeren angrenzenden Wand, nicht auf verschiedene Ecken gestreut.
    if wr == "wall_corner_or_door_adjacent":
        corner = room_polygon[0]
        dx, dy = cx - corner[0], cy - corner[1]
        d = math.hypot(dx, dy)
        if d < 1e-6:
            ax, ay = corner[0], corner[1]
        else:
            ax = corner[0] + dx / d * CORNER_ANCHOR_INSET_MM
            ay = corner[1] + dy / d * CORNER_ANCHOR_INSET_MM
        prev_pt, next_pt = room_polygon[-1], room_polygon[1 % n]
        e_prev = (prev_pt[0] - corner[0], prev_pt[1] - corner[1])
        e_next = (next_pt[0] - corner[0], next_pt[1] - corner[1])
        edge = e_next if math.hypot(*e_next) >= math.hypot(*e_prev) else e_prev
        elen = math.hypot(*edge)
        ux, uy = (edge[0] / elen, edge[1] / elen) if elen > 1e-6 else (1.0, 0.0)
        off = position_index * VERTEILER_SIBLING_SPACING_MM
        return PositionResult(
            x_mm=ax + ux * off, y_mm=ay + uy * off,
            z_mm=z_mm, rotation_deg=0.0,
            wall=None,
            status=STATUS_POS_OK,
            reason=f"corner_anchor_colocated:{wr}",
        )

    corner_idx = position_index % n
    corner = room_polygon[corner_idx]
    dx = cx - corner[0]
    dy = cy - corner[1]
    d = math.hypot(dx, dy)
    if d < 1e-6:
        x, y = corner[0], corner[1]
    else:
        x = corner[0] + dx / d * CORNER_ANCHOR_INSET_MM
        y = corner[1] + dy / d * CORNER_ANCHOR_INSET_MM

    return PositionResult(
        x_mm=x, y_mm=y,
        z_mm=z_mm, rotation_deg=0.0,
        wall=None,
        status=STATUS_POS_OK,
        reason=f"corner_anchor_first_polygon_corner:{wall_ref}",
    )


def position_verteiler_at_anchor(
    count: int,
    anchor_xy: tuple[float, float],
    room_walls: list[Wall],
    room_polygon: list[tuple[float, float]],
    z_values: Optional[list[Optional[int]]] = None,
) -> list[PositionResult]:
    """Slice 18.15.0 — Verteiler ÜBEREINANDER an einer markierten Position.

    Der Architektplan markiert die Verteiler-Stelle selbst (Text „WV / MV" im
    Abstellraum). Hier werden die Verteiler an ``anchor_xy`` gesetzt, entlang der
    nächsten Raumwand gestapelt (übereinander, je ``VERTEILER_SIBLING_SPACING_MM``),
    ``PERP_INSET_MM`` ins Rauminnere, Rotation mit dem Schrack-Block-Offset (−90°,
    konsistent zu ``position_verteiler_entrance_wall``)."""
    if count <= 0 or not room_walls or len(room_polygon) < 3:
        return []
    wall = min(
        room_walls,
        key=lambda w: _point_to_segment_dist(anchor_xy, w.start_xy, w.end_xy),
    )
    ux, uy = wall.unit_vector
    centroid = _polygon_centroid(room_polygon)
    nx, ny = -uy, ux
    if nx * (centroid[0] - anchor_xy[0]) + ny * (centroid[1] - anchor_xy[1]) < 0.0:
        nx, ny = -nx, -ny
    # Stapel-Richtung entlang der Wand zur Raummitte (sonst stapelt der 2.
    # Verteiler aus dem — oft kleinen — Abstellraum hinaus).
    cw = centroid[0] - anchor_xy[0], centroid[1] - anchor_xy[1]
    direction = 1.0 if (cw[0] * ux + cw[1] * uy) >= 0.0 else -1.0
    base_distance = (
        (anchor_xy[0] - wall.start_xy[0]) * ux
        + (anchor_xy[1] - wall.start_xy[1]) * uy
    )
    base_safe_d = nearest_distance_avoiding_openings(
        wall,
        base_distance,
        direction=direction,
        corner_inset_mm=CORNER_INSET_MM,
        clearance_mm=OPENING_CLEARANCE_MM,
    )
    if base_safe_d is None:
        return []
    ax, ay = wall.point_at_distance(base_safe_d)
    rot = (_rotation_into_room_deg(
        wall.unit_vector, (ax, ay), centroid) - 90.0) % 360.0

    z_values = z_values or []
    results: list[PositionResult] = []
    for i in range(count):
        z_mm = z_values[i] if i < len(z_values) else None
        # Stapelung ENTLANG der Wand Richtung Raummitte (Original 18.15.0);
        # der Initial-Import trug eine WIP-Variante, die entlang der Normale
        # durch die Wand hinaus stapelte (Suite-Red seit Import).
        px, py = wall.point_at_distance(
            base_safe_d + direction * i * VERTEILER_SIBLING_SPACING_MM)
        results.append(PositionResult(
            x_mm=px + PERP_INSET_MM * nx,
            y_mm=py + PERP_INSET_MM * ny,
            z_mm=z_mm, rotation_deg=rot, wall=wall,
            status=STATUS_POS_OK, reason="verteiler_marker_stacked",
        ))
    return results


def position_verteiler_entrance_wall(
    count: int,
    entrance_door: DoorOpening,
    room_walls: list[Wall],
    room_polygon: list[tuple[float, float]],
    z_values: Optional[list[Optional[int]]] = None,
) -> list[PositionResult]:
    """Slice 18.7.0 — Verteiler nebeneinander an der Wohnungseingangswand.

    Fachpraxis-Regel (v2_vorraum #1, O-Ton): Elektro- + Medienverteiler stehen
    NEBENEINANDER an derselben Wand beim Wohnungseingang — nicht an einer
    willkuerlichen Polygon-Ecke (``corner_anchor_colocated``, das ist der Bug).

    Geometrie: Eingangswand = die Raumwand mit minimaler Distanz zum Tuer-Anker
    (hinge_xy, sonst Tuer-Centroid). Verteiler werden ab
    ``ENTRANCE_VERTEILER_DOOR_CLEARANCE_MM`` vom projizierten Tuer-Anker entlang
    der Wand verteilt (Richtung des laengeren freien Wand-Stuecks), je
    ``VERTEILER_SIBLING_SPACING_MM`` versetzt, ``PERP_INSET_MM`` ins Rauminnere,
    Rotation senkrecht von der Wand weg.

    Rueckgabe: ``count`` ``PositionResult``-Eintraege (POS_OK) oder ``[]`` wenn
    keine Raumwand vorhanden → Caller faellt auf bestehende Heuristik zurueck.
    """
    if count <= 0 or not room_walls or len(room_polygon) < 3:
        return []

    anchor = entrance_door.hinge_xy
    if anchor is None:
        poly = entrance_door.polygon_mm
        anchor = (
            sum(p[0] for p in poly) / len(poly),
            sum(p[1] for p in poly) / len(poly),
        )

    # Eingangswand = naechste Raumwand zum Tuer-Anker, die LANG GENUG ist um
    # beide Verteiler nebeneinander zu tragen. Ohne Laengen-Filter greift die
    # naechste Wand oft einen kurzen Tuerlaibungs-Stummel → beide Verteiler
    # clampen auf denselben Punkt (gestapelt statt nebeneinander).
    needed_span = (count - 1) * VERTEILER_SIBLING_SPACING_MM + 2.0 * CORNER_INSET_MM
    long_enough = [
        w for w in room_walls
        if opening_free_length(
            w,
            corner_inset_mm=CORNER_INSET_MM,
            clearance_mm=OPENING_CLEARANCE_MM,
        ) >= needed_span
    ]
    candidates = long_enough or room_walls
    wall = min(
        candidates,
        key=lambda w: _point_to_segment_dist(anchor, w.start_xy, w.end_xy),
    )
    sx, sy = wall.start_xy
    ex, ey = wall.end_xy
    dx, dy = ex - sx, ey - sy
    seg_len_sq = dx * dx + dy * dy
    if seg_len_sq < 1e-9:
        return []
    # Projektion des Tuer-Ankers auf die Wand → Distanz d0 vom start.
    t = max(0.0, min(1.0, ((anchor[0] - sx) * dx + (anchor[1] - sy) * dy) / seg_len_sq))
    length = wall.length_mm
    d0 = t * length
    # Richtung mit mehr freier Wand (vom Tuer-Anker weg, ins laengere Stueck).
    direction = 1.0 if (length - d0) >= d0 else -1.0

    ux, uy = wall.unit_vector
    centroid = _polygon_centroid(room_polygon)
    z_values = z_values or []

    results: list[PositionResult] = []
    for i in range(count):
        d = d0 + direction * (
            ENTRANCE_VERTEILER_DOOR_CLEARANCE_MM + i * VERTEILER_SIBLING_SPACING_MM
        )
        d = max(CORNER_INSET_MM, min(length - CORNER_INSET_MM, d))
        safe_d = nearest_distance_avoiding_openings(
            wall,
            d,
            direction=direction,
            corner_inset_mm=CORNER_INSET_MM,
            clearance_mm=OPENING_CLEARANCE_MM,
        )
        if safe_d is None:
            return []
        d = safe_d
        along_x, along_y = wall.point_at_distance(d)
        nx, ny = -uy, ux
        if nx * (centroid[0] - along_x) + ny * (centroid[1] - along_y) < 0.0:
            nx, ny = -nx, -ny
        # Slice 18.14.0: Schrack-Block-Konvention. Die learned Wand-Symbole auf
        # dieser Wand (z.B. Schuko) stehen auf 270, während die geometrische
        # Normale 0 ergibt → die Schrack-Symbole sind ggü. der Normale um 90°
        # gedreht. Der computed Verteiler braucht denselben −90°-Offset, sonst
        # liegt die Box quer statt flach an der Wand.
        rot = (_rotation_into_room_deg(
            wall.unit_vector, (along_x, along_y), centroid
        ) - 90.0) % 360.0
        z_mm = z_values[i] if i < len(z_values) else None
        results.append(
            PositionResult(
                x_mm=along_x + PERP_INSET_MM * nx,
                y_mm=along_y + PERP_INSET_MM * ny,
                z_mm=z_mm,
                rotation_deg=rot,
                wall=wall,
                status=STATUS_POS_OK,
                reason="verteiler_entrance_wall",
            )
        )
    return results
