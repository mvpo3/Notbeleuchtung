"""Clearance-Relocation-Pass (Slice 18.27.0).

Anker-agnostischer Post-Anker-Schritt: validiert, dass ein wand-montiertes
Symbol auf einem freien Wandsegment von >= CLEARANCE_MIN_MM sitzt. Reicht die
Clearance nicht, wird im RELOCATE_RADIUS_MM-Umkreis der naechste qualifizierende
Punkt gesucht (Option C: erst dieselbe Wand, dann Nachbarwand) und das Symbol
mit minimaler Bewegung dorthin relociert. Findet sich kein Spot, bleibt der
Anker stehen (Warn + Counter).

Greift NICHT in die Resolver ein — arbeitet auf der fertigen Placement-Payload.
Free-Interval-Substrat kommt aus opening_bridge.opening_free_intervals (Ecken +
Oeffnungen); Nachbar-Symbole werden hier zusaetzlich als Intervall-Grenzen
eingezogen (opening_free_intervals kennt sie nicht).
"""
from __future__ import annotations

import logging
import math
from typing import Optional, Sequence

from engine.walls.door_opening_index import point_in_polygon
from engine.walls.opening_bridge import opening_free_intervals
from engine.walls.position_resolver import (
    CORNER_INSET_MM,
    OPENING_CLEARANCE_MM,
    PERP_INSET_MM,
    _point_to_segment_dist,
    _polygon_centroid,
    _polygon_min_dist,
    filter_walls_by_room_polygon,
)
from engine.walls.wall import Wall

logger = logging.getLogger(__name__)

# pending Fachpraxis-Formalisierung → clearance_rules.yaml (handoff B)
CLEARANCE_MIN_MM: float = 130.0
# pending Fachpraxis-Formalisierung → clearance_rules.yaml (handoff B)
RELOCATE_RADIUS_MM: float = 1500.0

# Owning-Wall-Guard: das Symbol muss perpendikular <= PERP_INSET_MM + diese
# Toleranz an der Wand liegen, damit die Wand als "tragend" gilt. Verhindert,
# dass ein frei-driftendes Anker-Symbol auf eine geratene Wand gezwungen wird.
OWNING_WALL_PERP_TOL_MM: float = 60.0
# Halbe Slot-Breite, mit der ein Nachbar-Symbol die freien Intervalle splittet.
# Symbol-Breite ist auf dieser Ebene unbekannt → konservativ halbe Min-Clearance.
NEIGHBOR_HALF_WIDTH_MM: float = CLEARANCE_MIN_MM / 2.0

# R3: symbol_catalog.yaml traegt KEINEN mount/placement-type (Stand 18.27.0).
# Konservative Allowlist der Schalter/Steckdose-Kinds — alles andere bleibt
# unangetastet. Erweitern, sobald ein mount-type im Katalog liegt (handoff B).
WALL_MOUNTED_KINDS: frozenset[str] = frozenset({
    "schuko_einfach",
    "schuko_zweifach",
    "wechselschalter",
    "ausschalter_einpolig",
    "taster",
})

# Decision-Source-Tiers, die eine forced_wall NIE per Relocation verlassen darf.
_PROTECTED_TIERS: tuple[str, ...] = ("rule:ove", "rule:lb")
_EXACT_FACHPRAXIS_REASONS: tuple[str, ...] = (
    "control_group_doorframe_150mm",
    "thermostat_doorframe_150mm",
    "bedroom_door_switch_doorframe_150mm",
    "bed_switch_at_nightstand_midpoint",
    "kitchen_loggia_switch_doorframe_150mm",
    "kitchen_loggia_switch_wall_midpoint",
    "kitchen_loggia_switch_window_anchor",
    "single_room_switch_doorframe_150mm",
    "wc_control_switch_doorframe_150mm",
    "bath_control_group_rt_switches_doorframe_150mm",
    "wz_normal_door",
    "wz_rt_sliding_door_150mm_group",
    "vr_switch_at_gsp_wall_line",
    "vr_sliding_door_switch_wall_line",
    "vr_intercom_door_opening_side",
    "bath_wm_wt_marker_safe_wall_pdf_s31",
    "bath_washbasin_socket_safe_wall_600mm_pdf_s31",
    "bath_heater_socket_",
    "corridor_socket_at_switch_group_bab",
    "corridor_switch_between_door_trim_and_wall",
    "corridor_switch_doortrim_wall_slot_185mm_mid",
    "storage_switch_outside_door_side_150mm",
    "storage_socket_inside_door_side_bab",
)


def is_wall_mounted(placement: dict) -> bool:
    """Allowlist-Gate (R3): nur die konservative Schalter/Steckdose-Familie."""
    return str(placement.get("catalog_entry_id", "")).strip().lower() in WALL_MOUNTED_KINDS


def _along(wall: Wall, point: tuple[float, float]) -> float:
    ux, uy = wall.unit_vector
    return (point[0] - wall.start_xy[0]) * ux + (point[1] - wall.start_xy[1]) * uy


def owning_wall(
    point: tuple[float, float],
    room_walls: Sequence[Wall],
    *,
    perp_tol_mm: float = OWNING_WALL_PERP_TOL_MM,
) -> Optional[Wall]:
    """Nearest-Room-Wall mit Guard (R1): das Symbol muss perpendikular
    <= PERP_INSET_MM + perp_tol_mm an der Wand liegen. Kein Treffer → None
    (Caller behandelt das wie no_spot, statt auf eine geratene Wand zu zwingen).
    """
    if not room_walls:
        return None
    best: Optional[tuple[float, Wall]] = None
    for w in room_walls:
        d = _point_to_segment_dist(point, w.start_xy, w.end_xy)
        if best is None or d < best[0]:
            best = (d, w)
    if best is None or best[0] > PERP_INSET_MM + perp_tol_mm:
        return None
    return best[1]


def split_at_neighbors(
    intervals: list[tuple[float, float]],
    neighbor_alongs: Sequence[float],
    *,
    half_width_mm: float = NEIGHBOR_HALF_WIDTH_MM,
) -> list[tuple[float, float]]:
    """Schneide ein [along - half, along + half]-Fenster pro Nachbar-Symbol aus
    den freien Intervallen. Deterministisch (sortierte Nachbarn)."""
    result = list(intervals)
    for c in sorted(neighbor_alongs):
        lo, hi = c - half_width_mm, c + half_width_mm
        nxt: list[tuple[float, float]] = []
        for a, b in result:
            if hi <= a or b <= lo:
                nxt.append((a, b))
                continue
            if a < lo:
                nxt.append((a, lo))
            if hi < b:
                nxt.append((hi, b))
        result = nxt
    return [(a, b) for a, b in result if b - a > 1e-6]


def free_intervals_for(
    wall: Wall,
    neighbor_alongs: Sequence[float] = (),
) -> list[tuple[float, float]]:
    """Free-Interval-Substrat: opening_free_intervals (Ecken + Oeffnungen),
    danach an den Nachbar-Symbolen gesplittet."""
    base = opening_free_intervals(
        wall,
        corner_inset_mm=CORNER_INSET_MM,
        clearance_mm=OPENING_CLEARANCE_MM,
    )
    return split_at_neighbors(base, neighbor_alongs)


def _interval_containing(
    intervals: Sequence[tuple[float, float]], d: float
) -> Optional[tuple[float, float]]:
    for a, b in intervals:
        if a <= d <= b:
            return (a, b)
    return None


def clearance_at(
    wall: Wall, d: float, neighbor_alongs: Sequence[float] = ()
) -> float:
    """Breite des freien Intervalls, in dem das Symbol bei along-Distanz d sitzt
    (0.0 wenn in keinem freien Intervall)."""
    iv = _interval_containing(free_intervals_for(wall, neighbor_alongs), d)
    return (iv[1] - iv[0]) if iv is not None else 0.0


def _nearest_qualifying_along(
    intervals: Sequence[tuple[float, float]], d: float, min_w: float
) -> Optional[float]:
    """Naechste along-Distanz zu d in einem Intervall >= min_w. Das Symbol wird
    mit min_w/2-Rand von den Intervall-Enden gehalten (minimale Bewegung)."""
    best: Optional[tuple[float, float]] = None
    margin = min_w / 2.0
    for a, b in intervals:
        if b - a < min_w:
            continue
        lo, hi = a + margin, b - margin
        cand = max(lo, min(hi, d))
        dist = abs(cand - d)
        if best is None or dist < best[0]:
            best = (dist, cand)
    return best[1] if best is not None else None


def _place_on_wall(
    wall: Wall, d: float, room_polygon: list[tuple[float, float]]
) -> tuple[float, float, float]:
    """(x, y, rotation_deg) — Punkt bei along-Distanz d, PERP_INSET_MM ins
    Rauminnere, Rotation senkrecht von der Wand weg Richtung Centroid."""
    ax, ay = wall.point_at_distance(d)
    ux, uy = wall.unit_vector
    nx, ny = -uy, ux
    cx, cy = _polygon_centroid(room_polygon)
    if nx * (cx - ax) + ny * (cy - ay) < 0.0:
        nx, ny = -nx, -ny
    rot = math.degrees(math.atan2(ny, nx)) % 360.0
    return (ax + PERP_INSET_MM * nx, ay + PERP_INSET_MM * ny, rot)


def _is_protected(placement: dict) -> bool:
    ds = str(placement.get("decision_source", "")).lower()
    return any(t in ds for t in _PROTECTED_TIERS)


def _protected_from_relocation(placement: dict) -> bool:
    """Architektur-Regel: ein heuristic:clearance-Move darf LB/Referenz/OVE nie
    überschreiben. Reference-Tier = learned (über coords_source erkennbar, der
    decision_source erbt nur den generativen Tier-Tag); OVE/LB = decision_source.
    Beide bleiben unangetastet (Anker bleibt + clearance_protected_count)."""
    if str(placement.get("coords_source", "")) == "learned_placement":
        return True
    reason = str(placement.get("coords_reason", "")).lower()
    if any(token in reason for token in _EXACT_FACHPRAXIS_REASONS):
        return True
    return _is_protected(placement)


def _room_for_point(
    point: tuple[float, float], candidate_rooms: list[dict]
) -> Optional[list[tuple[float, float]]]:
    """Polygon des Raums, der den Punkt enthaelt (sonst naechstes)."""
    polys = [
        [tuple(pt) for pt in r.get("polygon_mm", [])]
        for r in candidate_rooms
    ]
    polys = [p for p in polys if len(p) >= 3]
    if not polys:
        return None
    for poly in polys:
        if point_in_polygon(point, tuple(poly)):
            return poly
    return min(polys, key=lambda poly: _polygon_min_dist(point, poly))


def relocate_for_clearance(
    output: list[dict],
    walls: Sequence[Wall],
    arch_apt_top_by_id: dict,
    arch_rooms_by_top_name: dict,
) -> dict[str, int]:
    """Post-Anker-Pass. Mutiert ``output`` in-place (x/y/rotation + Tags) und
    gibt die Counter zurueck. Anker-agnostisch ueber alle pos_ok-Wandsymbole."""
    counters = {
        "clearance_relocated_count": 0,
        "clearance_no_spot_count": 0,
        "clearance_forced_override_count": 0,
        "clearance_protected_count": 0,
    }

    def _key(p: dict):
        return (
            str(p.get("apartment_id")),
            str(p.get("matched_room")),
            str(p.get("catalog_entry_id")),
            float(p.get("x_mm") or 0.0),
            float(p.get("y_mm") or 0.0),
        )

    candidates = [
        p for p in output
        if p.get("coords_status") == "pos_ok"
        and p.get("x_mm") is not None
        and p.get("y_mm") is not None
        and is_wall_mounted(p)
    ]
    candidates.sort(key=_key)

    # Pre-Pass: Owning-Wall + along je Kandidat. Map Wall-id → laufende alongs
    # (wird bei Relocation aktualisiert, damit spaetere Symbole es sehen).
    info: dict[int, dict] = {}
    alongs_by_wall: dict[str, list[float]] = {}
    for p in candidates:
        point = (float(p["x_mm"]), float(p["y_mm"]))
        top = arch_apt_top_by_id.get(p.get("apartment_id"))
        room_name = p.get("matched_room")
        cands = arch_rooms_by_top_name.get((top, room_name), []) if (top and room_name) else []
        room_polygon = _room_for_point(point, cands)
        room_walls = (
            filter_walls_by_room_polygon(list(walls), room_polygon)
            if room_polygon else []
        )
        wall = owning_wall(point, room_walls)
        rec = {
            "point": point,
            "room_polygon": room_polygon,
            "room_walls": room_walls,
            "wall": wall,
            "along": _along(wall, point) if wall is not None else None,
        }
        info[id(p)] = rec
        if wall is not None:
            alongs_by_wall.setdefault(wall.id, []).append(rec["along"])

    for p in candidates:
        # Tier-Schutz vor allem anderen: LB/Referenz/OVE-Platzierungen werden
        # nicht relociert (decision_source unangetastet, nur coords_reason-Tag).
        if _protected_from_relocation(p):
            counters["clearance_protected_count"] += 1
            p["coords_reason"] = f"{p.get('coords_reason') or ''}:clearance_protected"
            continue
        rec = info[id(p)]
        wall = rec["wall"]
        if wall is None:
            counters["clearance_no_spot_count"] += 1
            _tag(p, ":clearance_no_spot")
            continue
        point = rec["point"]
        d = rec["along"]
        room_polygon = rec["room_polygon"]
        room_walls = rec["room_walls"]

        neighbors = [a for a in alongs_by_wall.get(wall.id, []) if a is not d]
        if clearance_at(wall, d, neighbors) >= CLEARANCE_MIN_MM:
            _tag(p, ":clearance_ok")
            continue

        # Option C — Schritt 1: dieselbe Wand.
        intervals = free_intervals_for(wall, neighbors)
        cand_d = _nearest_qualifying_along(intervals, d, CLEARANCE_MIN_MM)
        if cand_d is not None:
            nx, ny, rot = _place_on_wall(wall, cand_d, room_polygon)
            if math.hypot(nx - point[0], ny - point[1]) <= RELOCATE_RADIUS_MM:
                _move(p, nx, ny, rot, f":clearance_relocated_{round(math.hypot(nx - point[0], ny - point[1]))}mm")
                counters["clearance_relocated_count"] += 1
                # laufende along auf der Wand aktualisieren
                lst = alongs_by_wall.get(wall.id, [])
                for i, a in enumerate(lst):
                    if a is d:
                        lst[i] = cand_d
                        break
                rec["along"] = cand_d
                continue

        # Option C — Schritt 2: Nachbarwand im Radius (minimale Bewegung).
        # Tier-Schutz greift bereits im Frontguard oben — hier nur noch der
        # forced-Marker für die override-Zählung.
        forced = p.get("coords_source") == "wall_choice_rule"

        best: Optional[tuple[float, float, float, float, Wall, float]] = None
        for w in room_walls:
            if w.id == wall.id:
                continue
            w_neighbors = [a for a in alongs_by_wall.get(w.id, [])]
            w_intervals = free_intervals_for(w, w_neighbors)
            # Ziel-along = Projektion des Original-Punkts auf die Nachbarwand.
            proj_d = _along(w, point)
            qd = _nearest_qualifying_along(w_intervals, proj_d, CLEARANCE_MIN_MM)
            if qd is None:
                continue
            wx, wy, wrot = _place_on_wall(w, qd, room_polygon)
            dist = math.hypot(wx - point[0], wy - point[1])
            if dist > RELOCATE_RADIUS_MM:
                continue
            if best is None or dist < best[0]:
                best = (dist, wx, wy, wrot, w, qd)

        if best is not None:
            dist, wx, wy, wrot, w, qd = best
            if forced:
                counters["clearance_forced_override_count"] += 1
                _move(p, wx, wy, wrot, ":clearance_forced_override")
            else:
                counters["clearance_relocated_count"] += 1
                _move(p, wx, wy, wrot, f":clearance_relocated_{round(dist)}mm")
            alongs_by_wall.setdefault(w.id, []).append(qd)
            # alte along entfernen
            lst = alongs_by_wall.get(wall.id, [])
            for i, a in enumerate(lst):
                if a is d:
                    lst.pop(i)
                    break
            rec["wall"] = w
            rec["along"] = qd
            continue

        counters["clearance_no_spot_count"] += 1
        _tag(p, ":clearance_no_spot")

    return counters


def _tag(p: dict, suffix: str) -> None:
    p["coords_reason"] = f"{p.get('coords_reason') or ''}{suffix}"
    ds = str(p.get("decision_source", ""))
    if "|heuristic:clearance" not in ds:
        p["decision_source"] = f"{ds}|heuristic:clearance"


def _move(p: dict, x: float, y: float, rot: float, suffix: str) -> None:
    p["x_mm"] = x
    p["y_mm"] = y
    p["rotation_deg"] = rot
    _tag(p, suffix)
