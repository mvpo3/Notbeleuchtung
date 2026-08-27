"""architecture_dxf.py — Parser for blank Austrian architecture DXFs.

Slice 7 — converts a wrapper-block-style architecture DXF into a structured
ArchitectureModel with rooms, walls, doors, windows and TOP-unit boundaries
in millimetres (engine-native units). All operations are read-only.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Optional

import ezdxf
from ezdxf import bbox
from ezdxf.layouts import BlockLayout

from engine.walls.door_opening import DEFAULT_WALL_THICKNESS_MM
from parsers.layer_profiles import LayerProfile, load_profile
from parsers.scale_detector import ScaleInfo, detect_scale

# ── Layer maps ─────────────────────────────────────────────────
WALL_LAYERS: dict[str, str] = {
    "02-TWA-G00-L04-M0": "tragend",
    "02-ZWA-G00-L04-M0": "zwischen",
    "02-WDA-G00-L04-M0": "aussen",
}

# Slice 18.2.0: floor-agnostic wall-type lookup. Wall layers carry a per-floor
# token ("02-TWA-G00-L04-M0" on the 4th floor; "-L01-"/"-LEG-"/"-LKG-"/"-L05-"
# on others), so the exact-name WALL_LAYERS dict only ever matched ONE floor.
# Match by the section-type token (first two "-" segments, e.g. "02-TWA")
# instead — identical across every floor. WALL_LAYERS is kept for backward-
# compat importers (replay/_coord_transform). TWB/TWE (Brüstung / erdberührte
# Kellerwand) are deliberately NOT included — that is a Track-B domain call.
_WALL_TYPE_BY_TOKEN: dict[str, str] = {
    "02-TWA": "tragend",
    "02-ZWA": "zwischen",
    "02-WDA": "aussen",
}


def wall_type_for_layer(layer: str) -> Optional[str]:
    """Wall type for a wall layer of *any* floor, or None. Keys on the
    section-type token (``02-TWA``/``02-ZWA``/``02-WDA``) so it is independent
    of the per-floor suffix (-L04-/-L01-/-LEG-/-LKG-/-L05- …)."""
    parts = layer.split("-", 2)
    if len(parts) >= 2:
        return _WALL_TYPE_BY_TOKEN.get(f"{parts[0]}-{parts[1]}")
    return None

ROOM_LABEL_BLOCK = "01-SQM"
TOP_BOUNDARY_BLOCK = "00-top"
FLOOR_HEIGHT_BLOCK = "01-HK1"

# Geschoss-Titel-Stempel im 01-SQM-Block (Plan-Beschriftung, keine Räume).
# Exakte Namen aus dem 8-Floor-Scan (Slice 1.19.0): "1. STOCK".."4. STOCK",
# "ERDGESCHOSS", "DACHGESCHOSS", "DG". "GEHWEG" u.ä. bleiben Räume.
_FLOOR_TITLE_STAMP_RE = re.compile(
    r"^\s*(?:\d+\.\s*STOCK|ERDGESCHOSS|DACHGESCHOSS|DG)\s*$", re.IGNORECASE)

from parsers.door_patterns import (  # noqa: E402  (logical grouping)
    DOOR_LABEL_PATTERNS,
    DOOR_NAME_PATTERNS,
    SLIDING_DOOR_PATTERNS,
)

WINDOW_NAME_PATTERNS = ("FENSTER",)
SLIDING_DOOR_DEPTH_MM = 200.0

# Slice 9.2.8: switch placement next to door, on the handle side.
# Praxis-convention (E 8101 has no concrete value); 100 mm matches the
# DOOR_BUFFER_MM used for swing-zone avoidance in 9.2.7.
HANDLE_SIDE_OFFSET_MM = 100.0

# Hatch layer carrying per-room colored fills. The actual fill content lives
# on several 02-FIL-* layers; we collect HATCHes from all of them as polygon
# candidates for room boundaries.
ROOM_HATCH_LAYERS = (
    "02-FIL-G00-L04-LILA",
    "02-FIL-G00-L04-ORANGE",
    "02-FIL-G00-L04-PLATTENBELAG",
    "02-FIL-G00-L04-STB",
    "01-FIL-G00-L04-M0",
)

# Slice 18.2.0: floor-agnostic room-hatch match (same per-floor-token issue as
# the wall layers). Match by section + colour-suffix, ignoring the floor token.
_ROOM_HATCH_SUFFIXES = frozenset({"LILA", "ORANGE", "PLATTENBELAG", "STB"})
_ROOM_HATCH_LAYER_RANK = {
    "ORANGE": 0,
    "STB": 1,
    "LILA": 2,
    "PLATTENBELAG": 3,
    "M0": 4,
}
_ROOM_HATCH_PATTERN_RANK = {
    # Real sample plans use ANSI32/ANSI33/HONEY for meaningful architectural
    # fills. Decorative tiles/platten are useful but less precise for rooms.
    "ANSI32": 0,
    "ANSI33": 0,
    "HONEY": 1,
    "CROSS": 2,
    "BRICK": 2,
    "BRASS": 2,
    "SQUARE": 2,
}


def is_room_hatch_layer(layer: str) -> bool:
    """True for the per-room coloured fill layers on any floor (02-FIL-…-LILA/
    ORANGE/PLATTENBELAG/STB, plus 01-FIL-…-M0)."""
    if layer.startswith("02-FIL-") and layer.rsplit("-", 1)[-1] in _ROOM_HATCH_SUFFIXES:
        return True
    return layer.startswith("01-FIL-") and layer.rsplit("-", 1)[-1] == "M0"

# Width parsing from door block names like "TÜR-80_10er-WAND".
_DOOR_WIDTH_RE = re.compile(r"T(?:Ü|UE|U)R[^0-9]*(\d+)", re.IGNORECASE)
_WINDOW_WIDTH_RE = re.compile(r"FENSTER[^0-9]*(\d+)", re.IGNORECASE)

# Slice 9.2.6: tolerance for wall ↔ room assignment (segment-to-polygon
# min-distance). 250 mm catches walls drawn on either polygon-edge surface
# while keeping per-room wall counts manageable. Empirically: 100 % room
# coverage at this threshold (no room ends up with zero walls).
WALL_TO_ROOM_TOL_MM = 250.0

# Mollgasse dialect signal (AA-OQ-01): GLASWAND / GLASGELAENDER are annotated
# as TEXT/MTEXT directly on their wall segment. Parsed-model correlation needs
# headroom because MTEXT insert/align points can sit on the label baseline.
NO_MOUNT_ANNOTATION_MAX_DIST_MM = 250.0
NO_MOUNT_DECISION_SOURCE = "rule:architecture_assumptions:AA-OQ-01:loggia_verglasung_no_mount"

# Slice 18.3.3: second-pass for rooms left with zero walls (failed polygon /
# open outdoor areas). Assign the nearest anchor-visible walls within this radius,
# capped, so balconies/terraces get their building wall for outdoor symbols.
EMPTY_ROOM_RADIUS_MM = 4000.0
EMPTY_ROOM_MAX_WALLS = 12


# ── Data models ────────────────────────────────────────────────
@dataclass
class RoomAnchor:
    name: str
    area_m2: float
    floor: str
    number: str
    anchor_x_mm: float
    anchor_y_mm: float
    top: Optional[str] = None


@dataclass(frozen=True)
class RoomHatch:
    """Room/floor fill boundary with the DXF semantics kept attached."""

    polygon_mm: list[tuple[float, float]]
    layer: str
    pattern: str = ""


@dataclass
class WallSegment:
    start_mm: tuple[float, float]
    end_mm: tuple[float, float]
    layer: str
    wall_type: str
    # Slice 18.36.0 (ADR 0011 Linien-First): additive FIL annotation. thickness_mm
    # = OBB-short of the matched in-band FIL hatch; material_class = its layer suffix
    # token VERBATIM (STB/ORANGE/LILA/…). None when no in-band hatch covers the wall.
    # Meaning/mounting consequence is Track B — not interpreted here.
    thickness_mm: Optional[float] = None
    material_class: Optional[str] = None
    decision_source: str = ""
    no_mount: bool = False
    no_mount_source: str = ""


@dataclass
class Door:
    block_name: str
    position_mm: tuple[float, float]
    rotation_deg: float
    width_mm: Optional[float] = None
    # Slice 9.2.7: pre-computed swing/slide forbidden polygon in world-mm.
    # Empty list when geometry could not be derived (e.g. block has no ARC
    # and no fallback rectangle). is_sliding distinguishes the two
    # geometry sources for downstream reporting.
    xscale: float = 1.0
    yscale: float = 1.0
    swing_polygon_mm: list[tuple[float, float]] = field(default_factory=list)
    is_sliding: bool = False
    # Slice 9.2.8: hinge + handle-side anchor used for switch placement.
    # hinge_world_mm: ARC center transformed to world coords (door pivot).
    # band_end_world_mm: ARC endpoint at start_angle (door blade tip when
    # closed) -- this point sits on the wall, radius away from the hinge.
    # handle_side_pos_mm: band_end + HANDLE_OFFSET_MM along wall_unit_xy
    # (canonical switch position next to the door frame on the handle side).
    # All zero (0, 0) for sliding doors -- no defined handle side.
    hinge_world_mm: tuple[float, float] = (0.0, 0.0)
    band_end_world_mm: tuple[float, float] = (0.0, 0.0)
    handle_side_pos_mm: tuple[float, float] = (0.0, 0.0)
    wall_unit_xy: tuple[float, float] = (0.0, 0.0)


@dataclass
class Window:
    block_name: str
    position_mm: tuple[float, float]
    rotation_deg: float
    width_mm: Optional[float] = None
    height_mm: Optional[float] = None


@dataclass
class Furniture:
    block_name: str
    layer: str
    x_mm: float
    y_mm: float
    rotation_deg: float
    room_idx: Optional[int] = None
    apartment_id: Optional[str] = None
    category_hint: Optional[str] = None
    bbox_mm: list[tuple[float, float]] = field(default_factory=list)
    center_mm: Optional[tuple[float, float]] = None
    size_mm: Optional[tuple[float, float]] = None
    text_labels: list[str] = field(default_factory=list)
    marker_kind: Optional[str] = None
    bbox_confidence: Optional[str] = None


@dataclass
class ArchitectureMarker:
    text: str
    marker_kind: str
    layer: str
    x_mm: float
    y_mm: float
    room_idx: Optional[int] = None
    apartment_id: Optional[str] = None
    bbox_mm: list[tuple[float, float]] = field(default_factory=list)
    center_mm: Optional[tuple[float, float]] = None
    source_entity_type: str = "TEXT"


@dataclass
class TopBoundary:
    top_id: str
    anchor_mm: tuple[float, float]
    finished_floor_label: str = ""


@dataclass
class Room:
    anchor: RoomAnchor
    polygon_mm: list[tuple[float, float]]
    polygon_source: str  # "wall_bbox" | "walls_flood" | "anchor_only"
    doors: list[Door] = field(default_factory=list)
    windows: list[Window] = field(default_factory=list)
    walls: list["WallSegment"] = field(default_factory=list)
    review_flag: bool = False
    review_reason: str = ""


@dataclass
class ArchitectureModel:
    tops: list[TopBoundary]
    rooms: list[Room]
    walls: list[WallSegment]
    bbox_mm: tuple[float, float, float, float]
    scale: ScaleInfo
    source_path: str = ""
    apartments: list = field(default_factory=list)
    # Slice 9.2.7: all extracted doors (deduplicated by position). Some
    # doors are not assigned to any room because they sit outside the
    # 500 mm room-edge tolerance; the avoidance pass needs them anyway.
    all_doors: list = field(default_factory=list)
    all_windows: list = field(default_factory=list)
    furniture: list[Furniture] = field(default_factory=list)
    markers: list[ArchitectureMarker] = field(default_factory=list)
    profile_diagnostics: dict = field(default_factory=dict)


# ── Pure helpers ───────────────────────────────────────────────
def _to_mm(p: tuple[float, float],
           scale_info: ScaleInfo) -> tuple[float, float]:
    f = scale_info.factor_to_mm
    return (p[0] * f, p[1] * f)


def _attrib_dict(insert) -> dict[str, str]:
    """Return ATTRIB tag → text for a given INSERT entity."""
    out: dict[str, str] = {}
    for a in getattr(insert, "attribs", []) or []:
        tag = getattr(a.dxf, "tag", None)
        val = (getattr(a.dxf, "text", "") or "").strip()
        if tag and val:
            out[tag] = val
    return out


def _parse_area_m2(raw: str) -> float:
    """Parse '12.98m2' → 12.98. Returns 0.0 if malformed.

    Anchored at string start: AREA-Attribute wie 'KABINE 140/110' (Aufzug-
    Kabinenmaße in cm) oder 'PFLICHTSTELLPLATZ 09-12' (Stellplatz-Nummern)
    sind KEINE Flächen — erste-Zahl-Greifen machte daraus 140 m² / 9 m².
    Suffixe nach der Zahl bleiben erlaubt ('130.04m2 (NICHT UNTERKELLERT)')."""
    m = re.match(r"\s*(\d+(?:[.,]\d+)?)", raw or "")
    if not m:
        return 0.0
    try:
        return float(m.group(1).replace(",", "."))
    except ValueError:
        return 0.0


def _point_in_polygon(point: tuple[float, float],
                      polygon: list[tuple[float, float]]) -> bool:
    """Ray casting (even-odd rule). Edge cases are pessimistic."""
    if len(polygon) < 3:
        return False
    x, y = point
    inside = False
    n = len(polygon)
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi
        ):
            inside = not inside
        j = i
    return inside


def _polygon_area(polygon: list[tuple[float, float]]) -> float:
    """Shoelace area, mm². Returns absolute value."""
    if len(polygon) < 3:
        return 0.0
    s = 0.0
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) * 0.5


def _polygon_centroid(polygon: list[tuple[float, float]]) -> tuple[float, float]:
    area_twice = 0.0
    cx = 0.0
    cy = 0.0
    for i, (x1, y1) in enumerate(polygon):
        x2, y2 = polygon[(i + 1) % len(polygon)]
        cross = x1 * y2 - x2 * y1
        area_twice += cross
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross
    if abs(area_twice) < 1e-9:
        xs = [p[0] for p in polygon]
        ys = [p[1] for p in polygon]
        return (sum(xs) / len(xs), sum(ys) / len(ys))
    return (cx / (3.0 * area_twice), cy / (3.0 * area_twice))


def _entity_plain_text(entity) -> str:
    if hasattr(entity, "plain_text"):
        try:
            return str(entity.plain_text())
        except Exception:
            pass
    return str(getattr(entity.dxf, "text", "") or "")


def _entity_insert_xy(entity) -> tuple[float, float]:
    point = getattr(entity.dxf, "insert", None)
    if point is None:
        point = getattr(entity.dxf, "align_point", None)
    if point is None:
        return (0.0, 0.0)
    return (float(point.x), float(point.y))


def _entity_anchor_points_mm(entity, scale_info: ScaleInfo) -> list[tuple[float, float]]:
    """Return insert/align anchors in mm-world, de-duplicated."""
    out: list[tuple[float, float]] = []
    for attr in ("insert", "align_point"):
        point = getattr(entity.dxf, attr, None)
        if point is None:
            continue
        xy = _to_mm((float(point.x), float(point.y)), scale_info)
        if not any(math.hypot(xy[0] - p[0], xy[1] - p[1]) < 1e-6 for p in out):
            out.append(xy)
    if out:
        return out
    return [_to_mm(_entity_insert_xy(entity), scale_info)]


def _clean_annotation_text(raw: str) -> str:
    """Strip common MTEXT formatting while keeping semantic words."""
    text = re.sub(r"\\[A-Za-z][^;]*;", " ", raw or "")
    text = re.sub(r"\\[A-Za-z][0-9.+-]*", " ", text)
    text = re.sub(r"[{}\\]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _parse_room_label_text(raw: str) -> tuple[str, Optional[float]]:
    text = re.sub(r"[{}\\^]", " ", raw or "")
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    area = None
    area_unit_re = r"(?:m\s*2|m²|mÂ²|m\^2)"
    for line in lines:
        m = re.search(rf"(\d+(?:[,.]\d+)?)\s*{area_unit_re}", line, re.I)
        if m:
            area = float(m.group(1).replace(",", "."))
            break
    name_candidates = [
        line for line in lines
        if not re.search(rf"(?:{area_unit_re}|\d+[,.]\d+\s*m)", line, re.I)
        and not re.fullmatch(r"\d+[A-Za-z]?", line)
    ]
    name = name_candidates[0] if name_candidates else (lines[0] if lines else "")
    return (name, area)


_FISCH_MATERIAL_WORDS = {
    "asphalt",
    "asphalt bfl",
    "parkett",
    "plattenbelag",
    "betonplatten",
    "feinsteinzeug",
    "rasen",
    "kies",
    "gußasphalt",
    "gussasphalt",
    "asphaltfeinbeton",
    "asphaltfeinbeton bfl",
    "pflasterstein",
    "gärtn. gest.",
    "gärtn. gestaltet",
    "gaertn. gest.",
    "gaertn. gestaltet",
    "mech.entl.",
    "mech. entl.",
    "entlüftung ü. dach",
    "entlueftung ue. dach",
    "lüftungsschlitze tür",
    "lueftungsschlitze tuer",
    "epdm dachfolie",
    "intensivbegruenung",
    "extensivbegruenung",
    "pflaster",
    "rigol",
}


# Slice R2: Wohnungs-Aggregat-Stempel ("Top 2.06" = Wohnungs-Gesamtfläche,
# Fischamender-Konvention) — nie ein Raum-Name (Analogie 01-SQM-TOP-Skip 1.8.0).
_TOP_AGGREGATE_RE = re.compile(r"^\s*Top\s*\d", re.IGNORECASE)


def _is_room_name_candidate(text: str) -> bool:
    clean = text.strip()
    if not clean:
        return False
    if _TOP_AGGREGATE_RE.match(clean):
        return False
    low = clean.lower()
    if low in _FISCH_MATERIAL_WORDS:
        return False
    if re.search(r"(?:m\s*2|m²|m\^2|\d+[,.]\d+\s*m)", clean, re.I):
        return False
    if re.fullmatch(r"[\d\s,.]+", clean):
        return False
    if re.fullmatch(r"m", clean, re.I):
        return False
    return bool(re.search(r"[A-Za-zÄÖÜäöüß]", clean))


def _mtext_markup_is_bold(raw_markup: str) -> bool:
    """True wenn der MTEXT-Inline-Fontcode ein Bold-Flag trägt (\\f...|b1|...;)."""
    return bool(re.search(r"\\[fF][^;]*?\|b1[|;]", raw_markup or ""))


def _hatch_polygon(
    hatch: RoomHatch | list[tuple[float, float]],
) -> list[tuple[float, float]]:
    if isinstance(hatch, RoomHatch):
        return hatch.polygon_mm
    return hatch


def _hatch_layer_suffix(hatch: RoomHatch | list[tuple[float, float]]) -> str:
    if not isinstance(hatch, RoomHatch):
        return ""
    return hatch.layer.rsplit("-", 1)[-1].upper()


def _hatch_semantic_rank(hatch: RoomHatch | list[tuple[float, float]] | None) -> int:
    if hatch is None:
        return 99
    suffix = _hatch_layer_suffix(hatch)
    layer_rank = _ROOM_HATCH_LAYER_RANK.get(suffix, 50)
    pattern = hatch.pattern.upper() if isinstance(hatch, RoomHatch) else ""
    pattern_rank = _ROOM_HATCH_PATTERN_RANK.get(pattern, 20)
    return layer_rank * 10 + pattern_rank


def _segment_distance(point: tuple[float, float],
                      a: tuple[float, float],
                      b: tuple[float, float]) -> float:
    """Distance from point to segment ab."""
    px, py = point
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    seg_len_sq = dx * dx + dy * dy
    if seg_len_sq < 1e-9:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / seg_len_sq))
    fx, fy = ax + t * dx, ay + t * dy
    return math.hypot(px - fx, py - fy)


def _seg_to_polygon_min_dist(seg_start: tuple[float, float],
                             seg_end: tuple[float, float],
                             polygon: list[tuple[float, float]]) -> float:
    """Min distance from segment to polygon boundary.

    Computed as min over all (wall-endpoint → polygon-edge) and
    (polygon-vertex → wall-segment) point-to-segment distances. Captures
    both parallel-but-offset walls and walls that touch a single polygon
    vertex.
    """
    if len(polygon) < 3:
        return math.inf
    best = math.inf
    n = len(polygon)
    for i in range(n):
        p = polygon[i]
        q = polygon[(i + 1) % n]
        # wall endpoints to this poly-edge
        for endpoint in (seg_start, seg_end):
            d = _segment_distance(endpoint, p, q)
            if d < best:
                best = d
        # poly-edge endpoints to this wall-segment
        for vertex in (p, q):
            d = _segment_distance(vertex, seg_start, seg_end)
            if d < best:
                best = d
    return best


def _assign_walls_to_rooms(rooms: list["Room"],
                           walls: list["WallSegment"],
                           tol_mm: float = WALL_TO_ROOM_TOL_MM) -> None:
    """Populate `room.walls` for each room. In-place, idempotent.

    A wall is assigned to a room when its min distance to the room
    polygon is ≤ tol_mm. Walls between two rooms (interior) are assigned
    to both — that's correct: each room sees the wall as its own.
    """
    for r in rooms:
        if len(r.polygon_mm) < 3:
            continue
        for w in walls:
            d = _seg_to_polygon_min_dist(w.start_mm, w.end_mm, r.polygon_mm)
            if d <= tol_mm:
                r.walls.append(w)

    # Slice 18.3.3: rooms whose polygon failed (anchor_only — e.g. open
    # balconies/terraces/loggias) get NO walls from the distance pass, so no
    # outdoor symbol can be placed. Give each still-empty room its nearest walls
    # that the anchor can SEE (line of sight not blocked by another wall). Only
    # touches rooms with zero walls → can never worsen an existing assignment.
    from parsers.room_partition import clear_line_of_sight
    wall_segs = [(w.start_mm, w.end_mm) for w in walls]
    for r in rooms:
        if r.walls:
            continue
        ax = r.anchor.anchor_x_mm
        ay = r.anchor.anchor_y_mm
        near = sorted(
            ((_segment_distance((ax, ay), w.start_mm, w.end_mm), w) for w in walls),
            key=lambda c: c[0],
        )[:EMPTY_ROOM_MAX_WALLS]
        for d, w in near:
            if d > EMPTY_ROOM_RADIUS_MM:
                break
            mid = ((w.start_mm[0] + w.end_mm[0]) / 2.0,
                   (w.start_mm[1] + w.end_mm[1]) / 2.0)
            if clear_line_of_sight((ax, ay), mid, wall_segs):
                r.walls.append(w)


def _is_on_polygon_edge(point: tuple[float, float],
                        polygon: list[tuple[float, float]],
                        tol_mm: float) -> bool:
    if len(polygon) < 2:
        return False
    n = len(polygon)
    for i in range(n):
        a = polygon[i]
        b = polygon[(i + 1) % n]
        if _segment_distance(point, a, b) <= tol_mm:
            return True
    return False


def _ray_segment_intersection(origin: tuple[float, float],
                              direction: tuple[float, float],
                              a: tuple[float, float],
                              b: tuple[float, float]) -> Optional[tuple[float, float, float]]:
    """Ray (origin + t*direction, t>=0) vs. segment ab.

    Returns (px, py, t) of the intersection, or None if no positive-t hit
    inside the segment.
    """
    ox, oy = origin
    dx, dy = direction
    ax, ay = a
    bx, by = b
    sx, sy = bx - ax, by - ay

    denom = dx * sy - dy * sx
    if abs(denom) < 1e-9:
        return None
    t = ((ax - ox) * sy - (ay - oy) * sx) / denom
    u = ((ax - ox) * dy - (ay - oy) * dx) / denom
    if t < 1e-6 or u < 0.0 or u > 1.0:
        return None
    return (ox + t * dx, oy + t * dy, t)


# Slice 16.1.5.2.a/b: opening-geometry helpers + virtual-wall closure.
# Opening = Wand-Aussparung als Linien-Segment (Tür-Pfosten zu Tür-Pfosten).
# Walls im DXF haben physische Gaps an Tür-Positionen (2 Segmente links+rechts
# der Tür). Raycast passt durch den Gap zu fernen Wänden → polygon_area_ratio
# bis 14.43x (16.1.5.1 baseline). 16.1.5.2.b fügt für jede Tür ein virtuelles
# WallSegment in die Raycast-Walls-Liste ein, das den Gap schließt.
# Windows ausgeschlossen (D7: Pre-Read zeigt walls sind durchgehend an
# Fenster-Positionen, perp_to_wall=0).
_OPENING_PROJECTION_BUFFER_MM = 50.0
# D8-Fix: door-endpoint sitzt ~40mm offset von nearest wall-endpoint (Pre-Read
# Q2). Virtual wall ohne Extension lässt 40mm Gap an beiden Enden → Ray-Leak.
# +50mm extension closet den Gap mit 10mm safety margin. Overlap mit
# benachbarten Wall-Endpoints ist harmlos (closest-hit-Raycast ignoriert).
_VIRTUAL_WALL_EXTENSION_MM = 50.0
# D6-Fix: Sliding-Door Fallback braucht nearest-wall-direction. Doors mit
# perp-distance > diesem Wert werden geskippt (kein Wand-Bezug erkennbar).
_SLIDING_DOOR_MAX_WALL_DISTANCE_MM = 800.0


def _door_to_opening_segment(
    door: Door,
) -> Optional[tuple[tuple[float, float], tuple[float, float]]]:
    """Door → (start_mm, end_mm) Wand-Öffnungs-Segment.

    Normal-Door: hinge_world_mm → band_end_world_mm (präzise on-wall-Geometrie
    aus extract_doors). Sliding-Door (oder fehlende hinge/band-Daten): fallback
    auf position_mm ± rotation_deg-Richtung * width/2.
    Returns None falls width_mm fehlt (Door ohne parsbare Breite).
    """
    if door.width_mm is None or door.width_mm <= 0:
        return None
    if door.hinge_world_mm != (0.0, 0.0) and door.band_end_world_mm != (0.0, 0.0):
        return (door.hinge_world_mm, door.band_end_world_mm)
    rad = math.radians(door.rotation_deg)
    ux, uy = math.cos(rad), math.sin(rad)
    hw = door.width_mm / 2.0
    px, py = door.position_mm
    return ((px - ux * hw, py - uy * hw), (px + ux * hw, py + uy * hw))


def _window_to_opening_segment(
    window: Window,
) -> Optional[tuple[tuple[float, float], tuple[float, float]]]:
    """Window → (start_mm, end_mm) Wand-Öffnungs-Segment.

    Windows haben keine hinge/band-Geometrie (anders als Doors) — Endpunkte
    werden aus position_mm + rotation_deg + width_mm berechnet.
    Returns None falls width_mm fehlt.
    """
    if window.width_mm is None or window.width_mm <= 0:
        return None
    rad = math.radians(window.rotation_deg)
    ux, uy = math.cos(rad), math.sin(rad)
    hw = window.width_mm / 2.0
    px, py = window.position_mm
    return ((px - ux * hw, py - uy * hw), (px + ux * hw, py + uy * hw))


def _hit_in_opening(
    hit_pt: tuple[float, float],
    opening: tuple[tuple[float, float], tuple[float, float]],
) -> bool:
    """True wenn hit_pt innerhalb einer Wand-Öffnung liegt.

    "Innerhalb" = perpendicular distance zur Opening-Linie unter
    DEFAULT_WALL_THICKNESS_MM/2 (=100mm, bestätigt dass hit auf derselben
    Wand sitzt) UND projection-Punkt liegt auf dem Opening-Segment mit
    ±_OPENING_PROJECTION_BUFFER_MM tolerance an beiden Enden.
    """
    (sx, sy), (ex, ey) = opening
    vx, vy = ex - sx, ey - sy
    length_sq = vx * vx + vy * vy
    if length_sq < 1e-9:
        return False
    hx, hy = hit_pt
    t = ((hx - sx) * vx + (hy - sy) * vy) / length_sq
    length = math.sqrt(length_sq)
    buf_t = _OPENING_PROJECTION_BUFFER_MM / length
    if t < -buf_t or t > 1.0 + buf_t:
        return False
    perp_x = sx + t * vx
    perp_y = sy + t * vy
    perp_dist = math.hypot(hx - perp_x, hy - perp_y)
    return perp_dist < DEFAULT_WALL_THICKNESS_MM / 2.0


def _detect_effective_mm_scale_factor(doors: list[Door]) -> float:
    """Empirical mm-scale factor: median(door.width_mm / hypot(band-hinge))
    snapped to nearest power of 10.

    D30-Fix: scale_detector kann factor_to_mm falsch zurückgeben (4OG
    confidence=0.3, factor=1.0 obwohl coords in Meter). Door.width_mm ist
    immer mm (geparsed aus Block-Namen "TÜR-80" → 800). Hinge/band-coords
    sind in source-units. Ratio = mm/coord-unit = wahrer Skalenfaktor.

    Returns 1.0 falls keine usable doors (safe default = "data is mm").
    """
    factors: list[float] = []
    for d in doors:
        if d.width_mm is None or d.width_mm <= 0:
            continue
        if d.hinge_world_mm == (0.0, 0.0) or d.band_end_world_mm == (0.0, 0.0):
            continue
        coord_len = math.hypot(
            d.band_end_world_mm[0] - d.hinge_world_mm[0],
            d.band_end_world_mm[1] - d.hinge_world_mm[1],
        )
        if coord_len < 1e-6:
            continue
        factors.append(d.width_mm / coord_len)
    if not factors:
        return 1.0
    factors.sort()
    median = factors[len(factors) // 2]
    if median <= 0:
        return 1.0
    return 10.0 ** round(math.log10(median))


def _sliding_door_opening_via_wall(
    door: Door,
    walls: list[WallSegment],
) -> Optional[tuple[tuple[float, float], tuple[float, float]]]:
    """Sliding-Door (oder Door ohne hinge/band-Geometrie) → Opening via
    nearest-wall direction.

    D6-Fix: rotation_deg von Sliding-Door-Blöcken steht senkrecht zur
    Wand-Richtung (Pre-Read Q3). Stattdessen wird die nächste Wand (perp <
    _SLIDING_DOOR_MAX_WALL_DISTANCE_MM) gesucht und das Opening entlang
    deren Richtung gebaut.
    """
    if door.width_mm is None or door.width_mm <= 0:
        return None
    px, py = door.position_mm
    best_w = None
    best_perp = math.inf
    for w in walls:
        ax, ay = w.start_mm
        bx, by = w.end_mm
        vx, vy = bx - ax, by - ay
        l2 = vx * vx + vy * vy
        if l2 < 1e-9:
            continue
        t = ((px - ax) * vx + (py - ay) * vy) / l2
        if not (0.0 <= t <= 1.0):
            continue
        perp_x = ax + t * vx
        perp_y = ay + t * vy
        perp = math.hypot(px - perp_x, py - perp_y)
        if perp < best_perp:
            best_perp = perp
            best_w = w
    if best_w is None or best_perp > _SLIDING_DOOR_MAX_WALL_DISTANCE_MM:
        return None
    wvx = best_w.end_mm[0] - best_w.start_mm[0]
    wvy = best_w.end_mm[1] - best_w.start_mm[1]
    wlen = math.hypot(wvx, wvy)
    if wlen < 1e-6:
        return None
    ux, uy = wvx / wlen, wvy / wlen
    hw = door.width_mm / 2.0
    return ((px - ux * hw, py - uy * hw), (px + ux * hw, py + uy * hw))


def _build_virtual_walls_from_doors(
    doors: list[Door],
    walls: list[WallSegment],
) -> list[WallSegment]:
    """Door-Liste → list[WallSegment] mit +_VIRTUAL_WALL_EXTENSION_MM
    extension an beiden Enden (D8-Fix für 40mm Endpoint-Offset).

    Normal-Doors nutzen hinge→band direkt. Sliding-Doors (oder Doors ohne
    hinge/band-Geometrie) gehen über _sliding_door_opening_via_wall.
    """
    out: list[WallSegment] = []
    for d in doors:
        if d.width_mm is None or d.width_mm <= 0:
            continue
        if (not d.is_sliding
                and d.hinge_world_mm != (0.0, 0.0)
                and d.band_end_world_mm != (0.0, 0.0)):
            base = (d.hinge_world_mm, d.band_end_world_mm)
        else:
            base = _sliding_door_opening_via_wall(d, walls)
            if base is None:
                continue
        sx, sy = base[0]
        ex, ey = base[1]
        dx, dy = ex - sx, ey - sy
        length = math.hypot(dx, dy)
        if length < 1e-6:
            continue
        ux, uy = dx / length, dy / length
        ext = _VIRTUAL_WALL_EXTENSION_MM
        ext_start = (sx - ux * ext, sy - uy * ext)
        ext_end = (ex + ux * ext, ey + uy * ext)
        out.append(WallSegment(
            start_mm=ext_start,
            end_mm=ext_end,
            layer="<virtual_door_opening>",
            wall_type="virtual",
        ))
    return out


def _opening_span_via_nearest_wall(
    pos_mm: tuple[float, float],
    width_mm: Optional[float],
    walls: list[WallSegment],
) -> Optional[tuple[tuple[float, float], tuple[float, float]]]:
    """Slice 16.1.5.2.e: opening span on the nearest wall, generic over the
    feature carrying it (window or sliding door).

    Mirrors _sliding_door_opening_via_wall but parametrised on (pos, width)
    instead of a Door, so windows can reuse the proven nearest-wall snap.
    rotation_deg is deliberately NOT used (D6: block rotation can sit
    perpendicular to the wall). Returns the (start, end) span centred on the
    feature, aligned to the nearest wall's direction, or None if no wall is
    within _SLIDING_DOOR_MAX_WALL_DISTANCE_MM.
    """
    if width_mm is None or width_mm <= 0:
        return None
    px, py = pos_mm
    best_w = None
    best_perp = math.inf
    for w in walls:
        ax, ay = w.start_mm
        bx, by = w.end_mm
        vx, vy = bx - ax, by - ay
        l2 = vx * vx + vy * vy
        if l2 < 1e-9:
            continue
        t = ((px - ax) * vx + (py - ay) * vy) / l2
        if not (0.0 <= t <= 1.0):
            continue
        perp_x = ax + t * vx
        perp_y = ay + t * vy
        perp = math.hypot(px - perp_x, py - perp_y)
        if perp < best_perp:
            best_perp = perp
            best_w = w
    if best_w is None or best_perp > _SLIDING_DOOR_MAX_WALL_DISTANCE_MM:
        return None
    wvx = best_w.end_mm[0] - best_w.start_mm[0]
    wvy = best_w.end_mm[1] - best_w.start_mm[1]
    wlen = math.hypot(wvx, wvy)
    if wlen < 1e-6:
        return None
    ux, uy = wvx / wlen, wvy / wlen
    hw = width_mm / 2.0
    return ((px - ux * hw, py - uy * hw), (px + ux * hw, py + uy * hw))


def _build_virtual_walls_from_windows(
    windows: list[Window],
    walls: list[WallSegment],
) -> list[WallSegment]:
    """Slice 16.1.5.2.e: close window-frame gaps so raycast polygons stop
    leaking through them (D31). Windows carry no hinge geometry, so each is
    snapped to its nearest wall via _opening_span_via_nearest_wall and a virtual
    segment of window width is laid along that wall, extended by
    _VIRTUAL_WALL_EXTENSION_MM at both ends (same as door openings). Windows
    without a known width are skipped (gap stays open).
    """
    out: list[WallSegment] = []
    for win in windows:
        span = _opening_span_via_nearest_wall(win.position_mm, win.width_mm, walls)
        if span is None:
            continue
        (sx, sy), (ex, ey) = span
        dx, dy = ex - sx, ey - sy
        length = math.hypot(dx, dy)
        if length < 1e-6:
            continue
        ux, uy = dx / length, dy / length
        ext = _VIRTUAL_WALL_EXTENSION_MM
        out.append(WallSegment(
            start_mm=(sx - ux * ext, sy - uy * ext),
            end_mm=(ex + ux * ext, ey + uy * ext),
            layer="<virtual_window_opening>",
            wall_type="virtual",
        ))
    return out


# Slice B'-fragment-gap-closure: bridge collinear axis-aligned wall fragments
# across un-doored openings (passages with NO door block, which the door-VW
# closure cannot reach — e.g. the VR north passage). MAX_GAP ~ doorway width;
# wider open-plan gaps stay open. PERP/AXIS tolerances keep it to genuinely
# collinear stubs on the same wall line.
_FRAGMENT_BRIDGE_MAX_GAP_MM = 1300.0
_FRAGMENT_BRIDGE_PERP_TOL_MM = 60.0
_FRAGMENT_BRIDGE_AXIS_TOL_MM = 60.0


def _build_fragment_bridges(walls: list[WallSegment]) -> list[WallSegment]:
    """Connect collinear wall fragments separated by a gap <= MAX_GAP.

    Only ADDS virtual walls (closes openings) — never removes any, so two
    rooms can never be merged by this step. Doored gaps are already closed by
    _build_virtual_walls_from_doors; this catches un-doored passages/fragment
    gaps that otherwise let raycast polygons leak (D-B').
    """
    horiz: list[tuple[float, float, float]] = []  # (y, xmin, xmax)
    vert: list[tuple[float, float, float]] = []    # (x, ymin, ymax)
    for w in walls:
        (x1, y1), (x2, y2) = w.start_mm, w.end_mm
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        if dy <= _FRAGMENT_BRIDGE_AXIS_TOL_MM and dx > dy:
            horiz.append(((y1 + y2) / 2.0, min(x1, x2), max(x1, x2)))
        elif dx <= _FRAGMENT_BRIDGE_AXIS_TOL_MM and dy > dx:
            vert.append(((x1 + x2) / 2.0, min(y1, y2), max(y1, y2)))

    out: list[WallSegment] = []

    def _bridge(group: list[tuple[float, float, float]], horizontal: bool) -> None:
        n = len(group)
        for i in range(n):
            ci, lo_i, hi_i = group[i]
            for j in range(i + 1, n):
                cj, lo_j, hi_j = group[j]
                if abs(ci - cj) > _FRAGMENT_BRIDGE_PERP_TOL_MM:
                    continue
                if hi_i < lo_j:
                    gap, g0, g1 = lo_j - hi_i, hi_i, lo_j
                elif hi_j < lo_i:
                    gap, g0, g1 = lo_i - hi_j, hi_j, lo_i
                else:
                    continue  # overlap → no gap
                if 0.0 < gap <= _FRAGMENT_BRIDGE_MAX_GAP_MM:
                    c = (ci + cj) / 2.0
                    seg = (((g0, c), (g1, c)) if horizontal
                           else ((c, g0), (c, g1)))
                    out.append(WallSegment(
                        start_mm=seg[0], end_mm=seg[1],
                        layer="<virtual_bridge>", wall_type="virtual"))

    _bridge(horiz, True)
    _bridge(vert, False)
    return out


def _cast_ray_to_walls(origin: tuple[float, float],
                       direction: tuple[float, float],
                       walls: list[WallSegment]) -> Optional[tuple[float, float]]:
    """Closest wall hit along ray. Returns hit point or None."""
    best_t = math.inf
    best_pt: Optional[tuple[float, float]] = None
    for w in walls:
        hit = _ray_segment_intersection(origin, direction, w.start_mm, w.end_mm)
        if hit is None:
            continue
        px, py, t = hit
        if t < best_t:
            best_t = t
            best_pt = (px, py)
    return best_pt


def _compute_bbox(walls: list[WallSegment]) -> tuple[float, float, float, float]:
    if not walls:
        return (0.0, 0.0, 0.0, 0.0)
    xs: list[float] = []
    ys: list[float] = []
    for w in walls:
        xs.extend([w.start_mm[0], w.end_mm[0]])
        ys.extend([w.start_mm[1], w.end_mm[1]])
    return (float(min(xs)), float(min(ys)), float(max(xs)), float(max(ys)))


# ── Loading ────────────────────────────────────────────────────
_WRAPPER_WALL_THRESHOLD = 10  # min wall-layer entities for a layout to count
_SUPPORTED_WALL_ENTITY_TYPES = {"LINE", "LWPOLYLINE", "ARC", "CIRCLE", "ELLIPSE"}


def _wall_entity_count(layout) -> int:
    return sum(
        1 for e in layout
        if e.dxftype() in _SUPPORTED_WALL_ENTITY_TYPES
        and wall_type_for_layer(e.dxf.layer)
    )


def load_architecture(path: Path) -> tuple[ezdxf.document.Drawing, BlockLayout]:
    """Open the DXF, return the layout that carries the architecture.

    Two supported layouts (auto-detected):
    - Wrapper-Mode: modelspace contains an INSERT whose target block holds
      ≥10 wall-layer entities. The wrapper-block is returned.
    - Direct-Mode: architecture entities (walls, anchors, doors, …) live
      directly in the modelspace. The modelspace is returned.

    Raises if neither layout is recognized.
    """
    doc = ezdxf.readfile(str(path))
    msp = doc.modelspace()

    wrapper_blocks: list[BlockLayout] = []
    for e in msp:
        if e.dxftype() != "INSERT":
            continue
        try:
            target = doc.blocks[e.dxf.name]
        except KeyError:
            continue
        if _wall_entity_count(target) >= _WRAPPER_WALL_THRESHOLD:
            wrapper_blocks.append(target)

    if len(wrapper_blocks) == 1:
        return doc, wrapper_blocks[0]
    if len(wrapper_blocks) > 1:
        names = [b.name for b in wrapper_blocks]
        raise ValueError(
            f"Architecture DXF: expected at most 1 wrapper-block, "
            f"found {len(wrapper_blocks)}: {names}"
        )

    msp_walls = _wall_entity_count(msp)
    if msp_walls >= _WRAPPER_WALL_THRESHOLD:
        return doc, msp

    raise ValueError(
        f"Architecture DXF layout not recognized: no wrapper-block with "
        f">={_WRAPPER_WALL_THRESHOLD} wall-layer entities, and modelspace "
        f"has only {msp_walls}. Expected layers: "
        f"{', '.join(t + '-*' for t in _WALL_TYPE_BY_TOKEN)}."
    )


def load_architecture_for_profile(
    path: Path,
    profile: LayerProfile,
) -> tuple[ezdxf.document.Drawing, BlockLayout]:
    strategy = str(profile.layout.get("strategy", ""))
    if strategy == "direct_modelspace":
        doc = ezdxf.readfile(str(path))
        return doc, doc.modelspace()
    if strategy != "wrapper_or_direct":
        raise NotImplementedError(
            f"Layer profile {profile.profile_id!r}: layout strategy "
            f"{strategy!r} not implemented in this slice"
        )
    return load_architecture(path)


def _detect_scale_for_profile(doc, profile: LayerProfile) -> ScaleInfo:
    detected = detect_scale(doc)
    factor = profile.scale.get("factor_to_mm")
    if factor is None:
        return detected
    override_factor = float(factor)
    signals = dict(detected.signals)
    signals["profile_override"] = {
        "profile_id": profile.profile_id,
        "previous_factor_to_mm": detected.factor_to_mm,
        "factor_to_mm": override_factor,
        "source": "profile.scale.factor_to_mm",
    }
    return ScaleInfo(
        factor_to_mm=override_factor,
        confidence=1.0,
        signals=signals,
        source_unit=str(profile.scale.get("source_unit") or detected.source_unit or ""),
    )


# ── Extraction ────────────────────────────────────────────────
def extract_top_boundaries(block: BlockLayout,
                            scale_info: ScaleInfo) -> list[TopBoundary]:
    """Collect 00-top INSERTs as apartment-unit anchors."""
    tops: list[TopBoundary] = []
    hk1: list[tuple[tuple[float, float], str]] = []

    for e in block:
        if e.dxftype() != "INSERT":
            continue
        if e.dxf.name == FLOOR_HEIGHT_BLOCK:
            attrs = _attrib_dict(e)
            label = attrs.get("HEIGHT", "")
            pos_native = (e.dxf.insert.x, e.dxf.insert.y)
            hk1.append((_to_mm(pos_native, scale_info), label))

    for e in block:
        if e.dxftype() != "INSERT" or e.dxf.name != TOP_BOUNDARY_BLOCK:
            continue
        attrs = _attrib_dict(e)
        raw_top = attrs.get("TOP", "").strip()
        if not raw_top:
            continue
        top_id = raw_top.replace("TOP", "").strip()

        anchor_native = (e.dxf.insert.x, e.dxf.insert.y)
        anchor_mm = _to_mm(anchor_native, scale_info)

        # Nearest 01-HK1 within 5 m (5000 mm) for the floor-height label.
        floor_label = ""
        best = math.inf
        for h_pos, h_label in hk1:
            d = math.hypot(h_pos[0] - anchor_mm[0], h_pos[1] - anchor_mm[1])
            if d < best and d < 5000.0:
                best = d
                floor_label = h_label

        tops.append(TopBoundary(top_id=top_id, anchor_mm=anchor_mm,
                                finished_floor_label=floor_label))
    return tops


def extract_room_anchors(block: BlockLayout,
                          scale_info: ScaleInfo,
                          profile: LayerProfile | None = None) -> list[RoomAnchor]:
    if profile is not None:
        cfg = dict(profile.roles.get("rooms") or {})
        if str(cfg.get("anchor_strategy") or "") == "text_groups":
            return extract_room_text_anchors(block, scale_info, profile)

    out: list[RoomAnchor] = []
    seen: set[tuple[str, float, float]] = set()
    for e in block:
        if e.dxftype() != "INSERT" or e.dxf.name != ROOM_LABEL_BLOCK:
            continue
        attrs = _attrib_dict(e)
        name = attrs.get("ROOM", "").strip()
        if not name:
            continue
        # Slice 1.8.0: Wohnflächen-SUMMEN-Stempel ("TOP 24 (SONDERWUNSCH)",
        # "TOP 2 - Sonderwunsch") sind KEINE Räume — sie gehören dem
        # building_units-Pfad (area_stamps_from_msp) und würden hier als
        # Phantom-Räume die Cluster + Flächen-Summen verschmutzen.
        if re.match(r"^\s*TOP\b", name, re.IGNORECASE):
            continue
        # Slice 1.19.0: Geschoss-Titel-Stempel ("1. STOCK", "ERDGESCHOSS",
        # "DACHGESCHOSS", "DG") sind Plan-Beschriftung, keine Räume — sie
        # sitzen mitten in echten Faces und erzeugen Phantom-coarse-Räume.
        # Nur bei leerem AREA-Attribut droppen (ein echter Raum hätte Fläche).
        if (not attrs.get("AREA", "").strip()
                and _FLOOR_TITLE_STAMP_RE.match(name)):
            continue
        pos_mm = _to_mm((e.dxf.insert.x, e.dxf.insert.y), scale_info)
        # Slice 1.8.0: Standard-/Sonderwunsch-Overlays doppeln Raum-Stempel
        # an (nahezu) identischer Position — Duplikat = ein Raum.
        key = (name.upper(), round(pos_mm[0] / 100.0), round(pos_mm[1] / 100.0))
        if key in seen:
            continue
        seen.add(key)
        out.append(RoomAnchor(
            name=name,
            area_m2=_parse_area_m2(attrs.get("AREA", "")),
            floor=attrs.get("FLOOR", ""),
            number=attrs.get("NR", ""),
            anchor_x_mm=pos_mm[0],
            anchor_y_mm=pos_mm[1],
        ))
    return out


def extract_room_text_anchors(
    block: BlockLayout,
    scale_info: ScaleInfo,
    profile: LayerProfile,
) -> list[RoomAnchor]:
    """Collect room anchors from nearby room-name and area text groups."""
    cfg = dict(profile.roles.get("rooms") or {})
    layer_patterns = tuple(
        re.compile(str(pattern), re.IGNORECASE)
        for pattern in (cfg.get("label_layers") or ())
    )
    labels = []
    for entity_index, e in enumerate(block):
        if e.dxftype() not in {"MTEXT", "TEXT"}:
            continue
        layer = str(e.dxf.layer)
        if layer_patterns and not any(p.search(layer) for p in layer_patterns):
            continue
        raw = _entity_plain_text(e)
        if not raw.strip():
            continue
        name, area = _parse_room_label_text(raw)
        if area is None:
            # Slice R1 (Barawitzka-Regelgeschosse): die m²-Zeile des Stempels
            # trägt KEIN Einheiten-Suffix ("25,67" statt "25,67 m²") — auf
            # den Label-Layern ist eine nackte Dezimalzahl die Fläche.
            m = re.fullmatch(r"(\d{1,4}[.,]\d{1,2})", raw.strip())
            if m:
                area = float(m.group(1).replace(",", "."))
        labels.append({
            "entity_index": entity_index,
            "raw_text": raw,
            "name": name,
            "area_m2_label": area,
            "bold": (e.dxftype() == "MTEXT"
                     and _mtext_markup_is_bold(str(e.text))),
            "position_mm": _entity_anchor_points_mm(e, scale_info)[0],
        })

    anchors: list[RoomAnchor] = []
    for area_label in [label for label in labels if label["area_m2_label"] is not None]:
        ax, ay = area_label["position_mm"]
        nearby = []
        for label in labels:
            if label is area_label:
                continue
            lx, ly = label["position_mm"]
            if abs(lx - ax) <= 650.0 and abs(ly - ay) <= 850.0:
                nearby.append((label, lx - ax, ly - ay, math.hypot(lx - ax, ly - ay)))
        # Slice R2: Wohnungs-Aggregat-Stempel ("Top 2.06") auch im
        # Anker-Fallback droppen — sonst Phantom-Anker-Räume.
        # Konvention: Namenszeile steht ÜBER der Flächen-Zeile (dy > 0).
        # Ist die nächste Zeile OBERHALB eine Top-Zeile, gehört diese
        # Fläche zum Wohnungs-Aggregat (Kombi-Stempel: "Top 1.09" +
        # Gesamt-m² direkt über dem Raumstempel) → droppen.
        above = [
            item for item in nearby
            if item[2] > 0.0
            and (_TOP_AGGREGATE_RE.match(str(item[0].get("name") or ""))
                 or _is_room_name_candidate(str(item[0].get("name") or "")))
        ]
        if above:
            nearest_above = min(above, key=lambda item: item[3])
            if _TOP_AGGREGATE_RE.match(
                    str(nearest_above[0].get("name") or "")):
                continue
        name_candidates = [
            item for item in nearby
            if _is_room_name_candidate(str(item[0].get("name") or ""))
        ]
        # Slice R1: Bold-Namenszeile bevorzugen (N5-Lernen — Namenszeile
        # trägt |b1|, Bodenaufbau-Zeilen b0). Opt-in via label_prefer_bold.
        bold_candidates = (
            [item for item in name_candidates if item[0].get("bold")]
            if cfg.get("label_prefer_bold") else []
        )
        preferred = [item for item in name_candidates if 30.0 <= item[2] <= 450.0]
        chosen_name = None
        if bold_candidates:
            chosen_name = sorted(bold_candidates,
                                 key=lambda item: item[3])[0][0]
        elif preferred:
            chosen_name = sorted(
                preferred, key=lambda item: (abs(item[1]), abs(item[2] - 170.0))
            )[0][0]
        elif name_candidates:
            chosen_name = sorted(name_candidates, key=lambda item: item[3])[0][0]
        name = (chosen_name or {}).get("name") or f"Room {len(anchors) + 1}"
        anchors.append(RoomAnchor(
            name=str(name).strip(),
            area_m2=float(area_label["area_m2_label"] or 0.0),
            floor="",
            number=str(area_label["entity_index"]),
            anchor_x_mm=ax,
            anchor_y_mm=ay,
        ))
    # Slice R1: Overlay-/Doppel-Stempel dedupen — gleicher Name + gleiche
    # Fläche in <3 m Abstand ist EIN Raum (Muster wie der 01-SQM-Pfad).
    # Slice R2 zusätzlich: Dachschrägen-Doppelflächen (Fischamender DG —
    # anrechenbare Wohnfläche + Grundfläche als gestapelte Zeilen unter
    # EINEM Namen, <600 mm) → EIN Anker, größere Fläche (= Grundfläche,
    # matcht das Boden-Face) gewinnt.
    deduped: list[RoomAnchor] = []
    for a in anchors:
        merged = False
        for i, b in enumerate(deduped):
            if b.name.upper() != a.name.upper():
                continue
            dx = abs(b.anchor_x_mm - a.anchor_x_mm)
            dy = abs(b.anchor_y_mm - a.anchor_y_mm)
            same_stamp = (dx < 100.0 and dy < 600.0)
            overlay = (abs(b.area_m2 - a.area_m2) < 0.005
                       and math.hypot(dx, dy) < 3000.0)
            if same_stamp or overlay:
                if a.area_m2 > b.area_m2:
                    deduped[i] = a
                merged = True
                break
        if not merged:
            deduped.append(a)
    return deduped


def _polyline_segments(points: list[tuple[float, float]],
                       closed: bool) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    segs: list[tuple[tuple[float, float], tuple[float, float]]] = []
    n = len(points)
    if n < 2:
        return segs
    last = n if closed else n - 1
    for i in range(last):
        a = points[i]
        b = points[(i + 1) % n]
        if a != b:
            segs.append((a, b))
    return segs


ARC_FLATTEN_MAX_ANGLE_DEG = 10.0
MIN_WALL_CURVE_RADIUS_MM = 1200.0
MIN_HATCH_BOUNDARY_AREA_M2 = 0.05
MAX_HATCH_BOUNDARY_AREA_M2 = 40.0
MIN_HATCH_BOUNDARY_SEGMENT_MM = 80.0


def _bulge_arc_segments(
    start: tuple[float, float],
    end: tuple[float, float],
    bulge: float,
    max_angle_deg: float = ARC_FLATTEN_MAX_ANGLE_DEG,
) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """Approximate one LWPOLYLINE bulge arc as short line segments.

    DXF bulge = tan(included_angle / 4). Positive bulge bends left from
    start->end. Returning line segments keeps downstream ray-casting unchanged
    while preserving curved architecture edges with bounded angular error.
    """
    if abs(bulge) < 1e-12:
        return [(start, end)] if start != end else []

    sx, sy = start
    ex, ey = end
    dx = ex - sx
    dy = ey - sy
    chord = math.hypot(dx, dy)
    if chord <= 1e-9:
        return []

    theta = 4.0 * math.atan(bulge)
    sin_half = math.sin(theta / 2.0)
    tan_half = math.tan(theta / 2.0)
    if abs(sin_half) <= 1e-12 or abs(tan_half) <= 1e-12:
        return [(start, end)]

    mx = (sx + ex) / 2.0
    my = (sy + ey) / 2.0
    left_x = -dy / chord
    left_y = dx / chord
    center_offset = chord / (2.0 * tan_half)
    cx = mx + left_x * center_offset
    cy = my + left_y * center_offset
    radius = abs(chord / (2.0 * sin_half))

    a0 = math.atan2(sy - cy, sx - cx)
    a1 = math.atan2(ey - cy, ex - cx)
    if theta > 0:
        while a1 <= a0:
            a1 += 2.0 * math.pi
    else:
        while a1 >= a0:
            a1 -= 2.0 * math.pi

    steps = max(
        2,
        int(math.ceil(abs(math.degrees(a1 - a0)) / max(max_angle_deg, 1.0))),
    )
    points = [start]
    for i in range(1, steps):
        a = a0 + (a1 - a0) * (i / steps)
        points.append((cx + radius * math.cos(a), cy + radius * math.sin(a)))
    points.append(end)
    return _polyline_segments(points, closed=False)


def _polyline_segments_with_bulge(
    points: list[tuple[float, float, float]],
    closed: bool,
) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    segs: list[tuple[tuple[float, float], tuple[float, float]]] = []
    n = len(points)
    if n < 2:
        return segs
    last = n if closed else n - 1
    for i in range(last):
        x1, y1, bulge = points[i]
        x2, y2, _ = points[(i + 1) % n]
        segs.extend(_bulge_arc_segments((x1, y1), (x2, y2), bulge))
    return segs


def _arc_steps(start_angle: float, end_angle: float,
               max_angle_deg: float = ARC_FLATTEN_MAX_ANGLE_DEG) -> int:
    span = end_angle - start_angle
    while span <= 0.0:
        span += 360.0
    return max(2, int(math.ceil(span / max(max_angle_deg, 1.0))))


def _arc_segments(
    center: tuple[float, float],
    radius: float,
    start_angle_deg: float,
    end_angle_deg: float,
    max_angle_deg: float = ARC_FLATTEN_MAX_ANGLE_DEG,
) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    if radius <= 0.0:
        return []
    steps = _arc_steps(start_angle_deg, end_angle_deg, max_angle_deg)
    span = end_angle_deg - start_angle_deg
    while span <= 0.0:
        span += 360.0
    points: list[tuple[float, float]] = []
    cx, cy = center
    for i in range(steps + 1):
        angle = math.radians(start_angle_deg + span * (i / steps))
        points.append((cx + radius * math.cos(angle),
                       cy + radius * math.sin(angle)))
    return _polyline_segments(points, closed=False)


def _circle_segments(
    center: tuple[float, float],
    radius: float,
    max_angle_deg: float = ARC_FLATTEN_MAX_ANGLE_DEG,
) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    if radius <= 0.0:
        return []
    steps = max(8, int(math.ceil(360.0 / max(max_angle_deg, 1.0))))
    cx, cy = center
    points = [
        (
            cx + radius * math.cos(2.0 * math.pi * i / steps),
            cy + radius * math.sin(2.0 * math.pi * i / steps),
        )
        for i in range(steps)
    ]
    return _polyline_segments(points, closed=True)


def _ellipse_segments(
    center: tuple[float, float],
    major_axis: tuple[float, float],
    ratio: float,
    start_param: float,
    end_param: float,
    max_angle_deg: float = ARC_FLATTEN_MAX_ANGLE_DEG,
) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    major_len = math.hypot(major_axis[0], major_axis[1])
    if major_len <= 0.0 or ratio <= 0.0:
        return []
    span = end_param - start_param
    while span <= 0.0:
        span += 2.0 * math.pi
    steps = max(8, int(math.ceil(abs(math.degrees(span)) / max(max_angle_deg, 1.0))))
    ux = major_axis[0] / major_len
    uy = major_axis[1] / major_len
    vx = -uy
    vy = ux
    minor_len = major_len * ratio
    cx, cy = center
    points: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = start_param + span * (i / steps)
        x = cx + major_len * math.cos(t) * ux + minor_len * math.sin(t) * vx
        y = cy + major_len * math.cos(t) * uy + minor_len * math.sin(t) * vy
        points.append((x, y))
    return _polyline_segments(points, closed=False)


def _hatch_boundary_wall_segments(
    hatches: list[RoomHatch],
) -> list[WallSegment]:
    """Convert architectural fill boundaries into conservative wall edges.

    In the MOL plans, many selected "wall" regions are HATCH entities on
    02-FIL-* layers rather than explicit 02-TWA/ZWA/WDA linework. Their
    boundary paths are valuable raycast blockers, but only within a plausible
    size band so outdoor/area fills cannot swallow rooms.
    """
    walls: list[WallSegment] = []
    min_area = MIN_HATCH_BOUNDARY_AREA_M2 * 1_000_000.0
    max_area = MAX_HATCH_BOUNDARY_AREA_M2 * 1_000_000.0
    for hatch in hatches:
        poly = hatch.polygon_mm
        if len(poly) < 3:
            continue
        area = _polygon_area(poly)
        if area < min_area or area > max_area:
            continue
        for s, t in _polyline_segments(poly, closed=True):
            if math.hypot(t[0] - s[0], t[1] - s[1]) < MIN_HATCH_BOUNDARY_SEGMENT_MM:
                continue
            walls.append(WallSegment(s, t, hatch.layer, "hatch_boundary"))
    return walls


def _mark_no_mount(wall: WallSegment) -> None:
    wall.no_mount = True
    wall.no_mount_source = NO_MOUNT_DECISION_SOURCE
    if wall.decision_source:
        if NO_MOUNT_DECISION_SOURCE not in wall.decision_source:
            wall.decision_source = f"{wall.decision_source}|{NO_MOUNT_DECISION_SOURCE}"
    else:
        wall.decision_source = NO_MOUNT_DECISION_SOURCE


def _nearest_mount_annotation_wall(
    points_mm: list[tuple[float, float]],
    walls: list[WallSegment],
) -> tuple[WallSegment | None, float]:
    best_wall: WallSegment | None = None
    best_dist = math.inf
    for wall in walls:
        if wall.wall_type == "hatch_boundary":
            continue
        for point in points_mm:
            dist = _segment_distance(point, wall.start_mm, wall.end_mm)
            if dist < best_dist:
                best_wall = wall
                best_dist = dist
    return best_wall, best_dist


def _annotate_no_mount_walls_from_text(
    block: BlockLayout,
    scale_info: ScaleInfo,
    walls: list[WallSegment],
) -> None:
    """Tag Mollgasse glass/loggia walls as no-mount from nearby GLAS text."""
    if not walls:
        return
    for entity in block:
        if entity.dxftype() not in {"TEXT", "MTEXT"}:
            continue
        clean = _clean_annotation_text(_entity_plain_text(entity))
        if "GLAS" not in clean.upper():
            continue
        wall, dist = _nearest_mount_annotation_wall(
            _entity_anchor_points_mm(entity, scale_info),
            walls,
        )
        if wall is None or dist > NO_MOUNT_ANNOTATION_MAX_DIST_MM:
            continue
        _mark_no_mount(wall)


def extract_walls(block: BlockLayout,
                   scale_info: ScaleInfo) -> list[WallSegment]:
    walls: list[WallSegment] = []
    for e in block:
        layer = e.dxf.layer
        wtype = wall_type_for_layer(layer)
        if wtype is None:
            continue
        if e.dxftype() == "LINE":
            s = _to_mm((e.dxf.start.x, e.dxf.start.y), scale_info)
            t = _to_mm((e.dxf.end.x, e.dxf.end.y), scale_info)
            walls.append(WallSegment(s, t, layer, wtype))
        elif e.dxftype() == "LWPOLYLINE":
            pts_native = [(p[0], p[1], p[2]) for p in e.get_points("xyb")]
            f = scale_info.factor_to_mm
            pts = [(x * f, y * f, bulge) for x, y, bulge in pts_native]
            for s, t in _polyline_segments_with_bulge(pts, bool(e.closed)):
                walls.append(WallSegment(s, t, layer, wtype))
        elif e.dxftype() == "ARC":
            f = scale_info.factor_to_mm
            center = (e.dxf.center.x * f, e.dxf.center.y * f)
            radius = float(e.dxf.radius) * f
            if radius < MIN_WALL_CURVE_RADIUS_MM:
                continue
            for s, t in _arc_segments(
                center,
                radius,
                float(e.dxf.start_angle),
                float(e.dxf.end_angle),
            ):
                walls.append(WallSegment(s, t, layer, wtype))
        elif e.dxftype() == "CIRCLE":
            f = scale_info.factor_to_mm
            center = (e.dxf.center.x * f, e.dxf.center.y * f)
            radius = float(e.dxf.radius) * f
            if radius < MIN_WALL_CURVE_RADIUS_MM:
                continue
            for s, t in _circle_segments(center, radius):
                walls.append(WallSegment(s, t, layer, wtype))
        elif e.dxftype() == "ELLIPSE":
            f = scale_info.factor_to_mm
            center = (e.dxf.center.x * f, e.dxf.center.y * f)
            major = (e.dxf.major_axis.x * f, e.dxf.major_axis.y * f)
            if math.hypot(major[0], major[1]) < MIN_WALL_CURVE_RADIUS_MM:
                continue
            for s, t in _ellipse_segments(
                center,
                major,
                float(e.dxf.ratio),
                float(e.dxf.start_param),
                float(e.dxf.end_param),
            ):
                walls.append(WallSegment(s, t, layer, wtype))
    walls.extend(_hatch_boundary_wall_segments(
        extract_room_hatches(block, scale_info)
    ))
    _annotate_no_mount_walls_from_text(block, scale_info, walls)
    return walls


def extract_walls_line_plus_hatch(block: BlockLayout,
                                  scale_info: ScaleInfo,
                                  profile: LayerProfile,
                                  diagnostics: Optional[dict] = None
                                  ) -> list[WallSegment]:
    cfg = _role_config(profile, "walls")
    layer_patterns = _compile_role_patterns(profile, "walls")
    entity_types = {
        str(entity_type).upper()
        for entity_type in (cfg.get("entity_types") or ["LINE", "HATCH"])
    }
    default_type = str(cfg.get("default_type") or "unknown")
    convert_hatch_boundaries = bool(cfg.get("hatch_boundaries", False))
    source = f"profile:{profile.profile_id}/walls/line_plus_hatch"
    walls: list[WallSegment] = []
    diag = {
        "line_segments": 0,
        "hatches": 0,
        "inserts": 0,
        "ignored": {},
    }
    for e in block:
        if not _layer_matches(e.dxf.layer, layer_patterns):
            continue
        etype = e.dxftype()
        if etype not in entity_types:
            if etype == "INSERT":
                diag["inserts"] += 1
                continue
            ignored = diag["ignored"]
            ignored[etype] = ignored.get(etype, 0) + 1
            continue
        if etype == "LINE":
            s = _to_mm((e.dxf.start.x, e.dxf.start.y), scale_info)
            t = _to_mm((e.dxf.end.x, e.dxf.end.y), scale_info)
            walls.append(WallSegment(
                s, t, e.dxf.layer, default_type,
                decision_source=source,
            ))
            diag["line_segments"] += 1
        elif etype == "HATCH":
            diag["hatches"] += 1
            if not convert_hatch_boundaries:
                continue
            for native in _hatch_boundary_paths_native(e):
                points_mm = [
                    (x * scale_info.factor_to_mm, y * scale_info.factor_to_mm)
                    for x, y in native
                ]
                for s, t in _polyline_segments(points_mm, closed=True):
                    if math.hypot(t[0] - s[0], t[1] - s[1]) < MIN_HATCH_BOUNDARY_SEGMENT_MM:
                        continue
                    walls.append(WallSegment(
                        s, t, e.dxf.layer, default_type,
                        decision_source=f"{source}:hatch_boundary",
                    ))
                    diag["hatch_segments"] = diag.get("hatch_segments", 0) + 1
        elif etype == "INSERT":
            diag["inserts"] += 1
            doc = getattr(block, "doc", None)
            if doc is None or e.dxf.name not in doc.blocks:
                continue
            sx = float(e.dxf.xscale or 1.0)
            sy = float(e.dxf.yscale or 1.0)
            rot_rad = math.radians(float(e.dxf.rotation or 0.0))
            ix = float(e.dxf.insert.x)
            iy = float(e.dxf.insert.y)
            insert_child_segments: list[tuple[tuple[float, float], tuple[float, float]]] = []
            for child in doc.blocks[e.dxf.name]:
                child_type = child.dxftype()
                if child_type == "LINE":
                    insert_child_segments.append((
                        (float(child.dxf.start.x), float(child.dxf.start.y)),
                        (float(child.dxf.end.x), float(child.dxf.end.y)),
                    ))
                elif child_type == "LWPOLYLINE":
                    pts = [
                        (float(p[0]), float(p[1]), float(p[4]) if len(p) > 4 else 0.0)
                        for p in child.get_points("xyseb")
                    ]
                    insert_child_segments.extend(
                        _polyline_segments_with_bulge(pts, bool(child.closed))
                    )
                elif child_type == "ARC":
                    insert_child_segments.extend(_arc_segments(
                        (float(child.dxf.center.x), float(child.dxf.center.y)),
                        float(child.dxf.radius),
                        float(child.dxf.start_angle),
                        float(child.dxf.end_angle),
                    ))
                elif child_type == "CIRCLE":
                    insert_child_segments.extend(_circle_segments(
                        (float(child.dxf.center.x), float(child.dxf.center.y)),
                        float(child.dxf.radius),
                    ))
                elif child_type == "ELLIPSE":
                    insert_child_segments.extend(_ellipse_segments(
                        (float(child.dxf.center.x), float(child.dxf.center.y)),
                        (float(child.dxf.major_axis.x), float(child.dxf.major_axis.y)),
                        float(child.dxf.ratio),
                        float(child.dxf.start_param),
                        float(child.dxf.end_param),
                    ))
            child_coords_are_world = _insert_child_segments_are_world_native(
                insert_child_segments,
                ix,
                iy,
                sx,
                sy,
                rot_rad,
            )
            if child_coords_are_world:
                diag["insert_world_coord_blocks"] = diag.get("insert_world_coord_blocks", 0) + 1
            for s_native, t_native in insert_child_segments:
                if child_coords_are_world:
                    s = _to_mm(s_native, scale_info)
                    t = _to_mm(t_native, scale_info)
                else:
                    s = _block_to_world_mm(
                        s_native[0], s_native[1], sx, sy, rot_rad, ix, iy, scale_info
                    )
                    t = _block_to_world_mm(
                        t_native[0], t_native[1], sx, sy, rot_rad, ix, iy, scale_info
                    )
                if math.hypot(t[0] - s[0], t[1] - s[1]) <= 1.0:
                    continue
                walls.append(WallSegment(
                    s, t, e.dxf.layer, default_type,
                    decision_source=f"{source}:insert_block",
                ))
                diag["insert_segments"] = diag.get("insert_segments", 0) + 1
        else:
            ignored = diag["ignored"]
            ignored[etype] = ignored.get(etype, 0) + 1
    if diagnostics is not None:
        diagnostics["walls"] = diag
    return walls


def _insert_child_segments_are_world_native(
    child_segments: list[tuple[tuple[float, float], tuple[float, float]]],
    ix_native: float,
    iy_native: float,
    sx: float,
    sy: float,
    rot_rad: float,
) -> bool:
    """Detect CAD blocks whose child geometry is already in world coordinates.

    Some ArchiCAD exports place wall geometry in an INSERT, but the block content
    is not local around (0, 0). Its native coordinates already sit at the plan
    location, and the INSERT point is near that same coordinate. Applying the
    normal INSERT translation would double the offset and push walls far away
    from rooms. Only default transforms are treated this way; rotated/scaled
    blocks stay on the normal affine path.
    """
    if not child_segments:
        return False
    if abs(sx - 1.0) > 1e-6 or abs(sy - 1.0) > 1e-6 or abs(rot_rad) > 1e-6:
        return False

    points = [point for segment in child_segments for point in segment]
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    center_x = (min_x + max_x) / 2.0
    center_y = (min_y + max_y) / 2.0
    diag = math.hypot(max_x - min_x, max_y - min_y)
    dist_to_insert = math.hypot(center_x - ix_native, center_y - iy_native)
    dist_to_origin = math.hypot(center_x, center_y)

    # Local block geometry usually has a small absolute center and a separate
    # INSERT translation. World-coordinate child geometry sits close to the
    # INSERT point while being far away from origin.
    close_to_insert = dist_to_insert <= max(diag * 2.0, 100.0)
    far_from_origin = dist_to_origin >= max(diag * 3.0, 1000.0)
    return close_to_insert and far_from_origin


def _name_matches(name: str, patterns: tuple[str, ...]) -> bool:
    upper = name.upper()
    return any(p.upper() in upper for p in patterns)


def _block_to_world_mm(bx: float, by: float,
                       sx: float, sy: float,
                       rot_rad: float,
                       ix_native: float, iy_native: float,
                       scale_info: ScaleInfo) -> tuple[float, float]:
    """Affine: scale -> rotate -> translate, then native-units -> mm."""
    x = bx * sx
    y = by * sy
    c = math.cos(rot_rad)
    s = math.sin(rot_rad)
    xr = c * x - s * y
    yr = s * x + c * y
    f = scale_info.factor_to_mm
    return ((xr + ix_native) * f, (yr + iy_native) * f)


def _door_geometry(insert_e, doc, scale_info: ScaleInfo,
                   arc_steps: int = 18) -> dict:
    """Single-source-of-truth for all door world-mm geometry.

    Returns a dict with keys:
      swing_polygon_mm  list[(x, y)]   forbidden zone (sector or rect)
      is_sliding        bool
      hinge_world_mm    (x, y)         door pivot in world coords
      band_end_world_mm (x, y)         ARC endpoint on the wall (start- ODER
                                       end_angle — Insert-Ausrichtung, 2.6.1)
      handle_side_pos_mm (x, y)        band_end + HANDLE_SIDE_OFFSET_MM
                                       along wall_unit (canonical switch pos)
      wall_unit_xy      (ux, uy)       normalized vector hinge -> band_end

    For sliding doors and degenerate blocks all anchor fields are (0, 0).
    """
    blk = doc.blocks[insert_e.dxf.name]
    sx = float(insert_e.dxf.xscale)
    sy = float(insert_e.dxf.yscale)
    rot_rad = math.radians(float(insert_e.dxf.rotation or 0.0))
    ix = float(insert_e.dxf.insert.x)
    iy = float(insert_e.dxf.insert.y)

    result: dict = {
        "swing_polygon_mm": [],
        "is_sliding": False,
        "hinge_world_mm": (0.0, 0.0),
        "band_end_world_mm": (0.0, 0.0),
        "handle_side_pos_mm": (0.0, 0.0),
        "wall_unit_xy": (0.0, 0.0),
    }

    arcs = [e for e in blk if e.dxftype() == "ARC"]
    if arcs:
        arc = arcs[0]
        cx_b = float(arc.dxf.center.x)
        cy_b = float(arc.dxf.center.y)
        r_b = float(arc.dxf.radius)
        a0 = math.radians(float(arc.dxf.start_angle))
        a1 = math.radians(float(arc.dxf.end_angle))
        if a1 <= a0:
            a1 += 2.0 * math.pi

        # Swing polygon: hinge + arc_steps points along the bow
        block_pts = [(cx_b, cy_b)]
        for k in range(arc_steps + 1):
            t = a0 + (a1 - a0) * k / arc_steps
            block_pts.append((cx_b + r_b * math.cos(t),
                              cy_b + r_b * math.sin(t)))
        result["swing_polygon_mm"] = [
            _block_to_world_mm(bx, by, sx, sy, rot_rad, ix, iy, scale_info)
            for bx, by in block_pts
        ]

        # Anchor points for switch placement (Slice 9.2.8, Fix 2.6.1):
        # hinge = ARC center. band_end = der Bogen-ENDPUNKT der AUF DER WAND
        # liegt (Türblatt geschlossen). Ob das start_angle oder end_angle ist,
        # hängt von Block-Spiegelung/Rotation ab (A_24-WET, 180°: end_angle!)
        # — fix start_angle drehte dort die Wandachse um 90° und schob die
        # ganze near_door-Familie an die falsche Wand. Entscheidung: der
        # Endpunkt, dessen Richtung ab hinge mit hinge→INSERT-Punkt
        # (Blockbasis sitzt in der Wandöffnung) ausgerichtet ist; degeneriert
        # (insert≈hinge) → Alt-Verhalten start_angle.
        hinge_w = _block_to_world_mm(
            cx_b, cy_b, sx, sy, rot_rad, ix, iy, scale_info
        )
        cand_w = [
            _block_to_world_mm(
                cx_b + r_b * math.cos(a),
                cy_b + r_b * math.sin(a),
                sx, sy, rot_rad, ix, iy, scale_info,
            )
            for a in (a0, a1)
        ]
        insert_w = _block_to_world_mm(0.0, 0.0, sx, sy, rot_rad, ix, iy,
                                      scale_info)
        iv = (insert_w[0] - hinge_w[0], insert_w[1] - hinge_w[1])
        ilen = math.hypot(iv[0], iv[1])
        band_w = cand_w[0]
        if ilen > 50.0:
            def _align(p):
                dx, dy = p[0] - hinge_w[0], p[1] - hinge_w[1]
                dlen = math.hypot(dx, dy)
                if dlen < 1e-6:
                    return -2.0
                return (dx * iv[0] + dy * iv[1]) / (dlen * ilen)
            band_w = max(cand_w, key=_align)
        result["hinge_world_mm"] = hinge_w
        result["band_end_world_mm"] = band_w
        wdx = band_w[0] - hinge_w[0]
        wdy = band_w[1] - hinge_w[1]
        wlen = math.hypot(wdx, wdy)
        if wlen > 1e-6:
            ux, uy = wdx / wlen, wdy / wlen
            result["wall_unit_xy"] = (ux, uy)
            result["handle_side_pos_mm"] = (
                band_w[0] + HANDLE_SIDE_OFFSET_MM * ux,
                band_w[1] + HANDLE_SIDE_OFFSET_MM * uy,
            )
        return result

    # No ARC -> sliding door (or unknown). Build a rectangle from the
    # block's LWPOLYLINE bbox, inflated to SLIDING_DOOR_DEPTH_MM thick.
    result["is_sliding"] = True
    xs: list[float] = []
    ys: list[float] = []
    for e in blk:
        if e.dxftype() == "LWPOLYLINE":
            for p in e.get_points("xy"):
                xs.append(float(p[0]))
                ys.append(float(p[1]))
    if not xs or not ys:
        return result
    bx_min, bx_max = min(xs), max(xs)
    by_min, by_max = min(ys), max(ys)
    # Sliding-door fallback rectangle: SLIDING_DOOR_DEPTH_MM is a target
    # in mm-world; convert to native (block) units via factor_to_mm.
    depth_native = SLIDING_DOOR_DEPTH_MM / scale_info.factor_to_mm
    if (by_max - by_min) < depth_native:
        cy = (by_min + by_max) / 2.0
        by_min = cy - depth_native / 2.0
        by_max = cy + depth_native / 2.0
    if (bx_max - bx_min) < depth_native:
        cx = (bx_min + bx_max) / 2.0
        bx_min = cx - depth_native / 2.0
        bx_max = cx + depth_native / 2.0
    corners = [(bx_min, by_min), (bx_max, by_min),
               (bx_max, by_max), (bx_min, by_max)]
    result["swing_polygon_mm"] = [
        _block_to_world_mm(bx, by, sx, sy, rot_rad, ix, iy, scale_info)
        for bx, by in corners
    ]
    return result


def _door_swing_polygon(insert_e, doc, scale_info: ScaleInfo,
                        arc_steps: int = 18
                        ) -> tuple[list[tuple[float, float]], bool]:
    """Backward-compatible adapter -- new code should call _door_geometry."""
    g = _door_geometry(insert_e, doc, scale_info, arc_steps=arc_steps)
    return g["swing_polygon_mm"], g["is_sliding"]


def _plausible_door_width_mm(value: float) -> Optional[float]:
    """Normalize geometry-derived door width into mm when plausible."""
    if 500.0 <= value <= 1800.0:
        return value
    if 0.5 <= value <= 1.8:
        return value * 1000.0
    return None


def extract_doors(block: BlockLayout, doc, scale_info: ScaleInfo) -> list[Door]:
    out: list[Door] = []
    for e in block:
        if e.dxftype() != "INSERT":
            continue
        name = e.dxf.name
        if not _name_matches(name, DOOR_NAME_PATTERNS):
            continue
        # Slice 9.2.7: filter Tuerachse-style label blocks. They match
        # the DOOR_NAME_PATTERNS prefix but are not actual doors -- they
        # are floor-plan labels with an ATTDEF and no ARC/wall geometry.
        if _name_matches(name, DOOR_LABEL_PATTERNS):
            continue
        attrs = _attrib_dict(e)
        width_mm: Optional[float] = None
        for key in ("WIDTH", "BREITE"):
            if key in attrs:
                try:
                    width_mm = float(attrs[key].replace(",", ".")) * 10.0
                    break
                except ValueError:
                    pass
        if width_mm is None:
            m = _DOOR_WIDTH_RE.search(name)
            if m:
                width_mm = float(m.group(1)) * 10.0
        pos_mm = _to_mm((e.dxf.insert.x, e.dxf.insert.y), scale_info)
        xscale = float(e.dxf.xscale)
        yscale = float(e.dxf.yscale)
        swing_poly: list[tuple[float, float]] = []
        is_sliding = _name_matches(name, SLIDING_DOOR_PATTERNS)
        hinge_w = (0.0, 0.0)
        band_w = (0.0, 0.0)
        handle_w = (0.0, 0.0)
        wall_u = (0.0, 0.0)
        if doc is not None:
            geo = _door_geometry(e, doc, scale_info)
            swing_poly = geo["swing_polygon_mm"]
            # Trust geometric detection over name-pattern when they
            # disagree (e.g. a swing door named SCHIEBE-by-mistake).
            is_sliding = geo["is_sliding"]
            hinge_w = geo["hinge_world_mm"]
            band_w = geo["band_end_world_mm"]
            handle_w = geo["handle_side_pos_mm"]
            wall_u = geo["wall_unit_xy"]
            if width_mm is None:
                if hinge_w != (0.0, 0.0) and band_w != (0.0, 0.0):
                    derived_width = math.hypot(
                        band_w[0] - hinge_w[0],
                        band_w[1] - hinge_w[1],
                    )
                    width_mm = _plausible_door_width_mm(derived_width)
                elif swing_poly:
                    xs = [p[0] for p in swing_poly]
                    ys = [p[1] for p in swing_poly]
                    derived_width = max(max(xs) - min(xs), max(ys) - min(ys))
                    width_mm = _plausible_door_width_mm(derived_width)
        out.append(Door(
            block_name=name,
            position_mm=pos_mm,
            rotation_deg=float(e.dxf.rotation or 0.0),
            width_mm=width_mm,
            xscale=xscale,
            yscale=yscale,
            swing_polygon_mm=swing_poly,
            is_sliding=is_sliding,
            hinge_world_mm=hinge_w,
            band_end_world_mm=band_w,
            handle_side_pos_mm=handle_w,
            wall_unit_xy=wall_u,
        ))
    return out


def extract_windows(block: BlockLayout,
                     scale_info: ScaleInfo) -> list[Window]:
    out: list[Window] = []
    for e in block:
        if e.dxftype() != "INSERT":
            continue
        name = e.dxf.name
        if not _name_matches(name, WINDOW_NAME_PATTERNS):
            continue
        attrs = _attrib_dict(e)
        width_mm: Optional[float] = None
        height_mm: Optional[float] = None
        for key in ("WIDTH", "BREITE"):
            if key in attrs:
                try:
                    width_mm = float(attrs[key].replace(",", ".")) * 10.0
                    break
                except ValueError:
                    pass
        for key in ("HEIGHT", "HÖHE", "HOEHE"):
            if key in attrs:
                try:
                    height_mm = float(attrs[key].replace(",", ".")) * 10.0
                    break
                except ValueError:
                    pass
        if width_mm is None:
            m = _WINDOW_WIDTH_RE.search(name)
            if m:
                width_mm = float(m.group(1)) * 10.0
        pos_mm = _to_mm((e.dxf.insert.x, e.dxf.insert.y), scale_info)
        out.append(Window(
            block_name=name,
            position_mm=pos_mm,
            rotation_deg=float(e.dxf.rotation or 0.0),
            width_mm=width_mm,
            height_mm=height_mm,
        ))
    return out


def _insert_entities_by_layer(block: BlockLayout,
                              profile: LayerProfile,
                              role: str) -> list:
    layer_patterns = _compile_role_patterns(profile, role)
    return [
        e for e in block
        if e.dxftype() == "INSERT"
        and _layer_matches(e.dxf.layer, layer_patterns)
    ]


def extract_doors_by_layer_pattern(block: BlockLayout,
                                   doc,
                                   scale_info: ScaleInfo,
                                   profile: LayerProfile) -> list[Door]:
    out: list[Door] = []
    for e in _insert_entities_by_layer(block, profile, "doors"):
        name = e.dxf.name
        attrs = _attrib_dict(e)
        width_mm: Optional[float] = None
        for key in ("WIDTH", "BREITE"):
            if key in attrs:
                try:
                    width_mm = float(attrs[key].replace(",", ".")) * 10.0
                    break
                except ValueError:
                    pass
        if width_mm is None:
            m = _DOOR_WIDTH_RE.search(name)
            if m:
                width_mm = float(m.group(1)) * 10.0
        pos_mm = _to_mm((e.dxf.insert.x, e.dxf.insert.y), scale_info)
        xscale = float(e.dxf.xscale)
        yscale = float(e.dxf.yscale)
        swing_poly: list[tuple[float, float]] = []
        is_sliding = False
        hinge_w = (0.0, 0.0)
        band_w = (0.0, 0.0)
        handle_w = (0.0, 0.0)
        wall_u = (0.0, 0.0)
        if doc is not None:
            geo = _door_geometry(e, doc, scale_info)
            swing_poly = geo["swing_polygon_mm"]
            is_sliding = geo["is_sliding"]
            hinge_w = geo["hinge_world_mm"]
            band_w = geo["band_end_world_mm"]
            handle_w = geo["handle_side_pos_mm"]
            wall_u = geo["wall_unit_xy"]
            if width_mm is None:
                if hinge_w != (0.0, 0.0) and band_w != (0.0, 0.0):
                    width_mm = _plausible_door_width_mm(math.hypot(
                        band_w[0] - hinge_w[0],
                        band_w[1] - hinge_w[1],
                    ))
                elif swing_poly:
                    xs = [p[0] for p in swing_poly]
                    ys = [p[1] for p in swing_poly]
                    width_mm = _plausible_door_width_mm(
                        max(max(xs) - min(xs), max(ys) - min(ys))
                    )
        out.append(Door(
            block_name=name,
            position_mm=pos_mm,
            rotation_deg=float(e.dxf.rotation or 0.0),
            width_mm=width_mm,
            xscale=xscale,
            yscale=yscale,
            swing_polygon_mm=swing_poly,
            is_sliding=is_sliding,
            hinge_world_mm=hinge_w,
            band_end_world_mm=band_w,
            handle_side_pos_mm=handle_w,
            wall_unit_xy=wall_u,
        ))
    return out


def extract_windows_by_layer_pattern(block: BlockLayout,
                                     scale_info: ScaleInfo,
                                     profile: LayerProfile) -> list[Window]:
    out: list[Window] = []
    for e in _insert_entities_by_layer(block, profile, "windows"):
        name = e.dxf.name
        attrs = _attrib_dict(e)
        width_mm: Optional[float] = None
        height_mm: Optional[float] = None
        for key in ("WIDTH", "BREITE"):
            if key in attrs:
                try:
                    width_mm = float(attrs[key].replace(",", ".")) * 10.0
                    break
                except ValueError:
                    pass
        for key in ("HEIGHT", "HÖHE", "HOEHE"):
            if key in attrs:
                try:
                    height_mm = float(attrs[key].replace(",", ".")) * 10.0
                    break
                except ValueError:
                    pass
        if width_mm is None:
            m = _WINDOW_WIDTH_RE.search(name)
            if m:
                width_mm = float(m.group(1)) * 10.0
        pos_mm = _to_mm((e.dxf.insert.x, e.dxf.insert.y), scale_info)
        out.append(Window(
            block_name=name,
            position_mm=pos_mm,
            rotation_deg=float(e.dxf.rotation or 0.0),
            width_mm=width_mm,
            height_mm=height_mm,
        ))
    return out


def extract_room_hatches(block: BlockLayout,
                          scale_info: ScaleInfo
                          ) -> list[RoomHatch]:
    """Collect HATCH boundary polygons as candidate room outlines (mm)."""
    hatches: list[RoomHatch] = []
    for e in block:
        if e.dxftype() != "HATCH":
            continue
        layer = e.dxf.layer
        if not is_room_hatch_layer(layer):
            continue
        pattern = str(getattr(e.dxf, "pattern_name", "") or "")
        for path in e.paths:
            verts: list[tuple[float, float]] = []
            # ezdxf hatch paths can be PolylinePath or EdgePath
            if hasattr(path, "vertices") and path.vertices:
                for v in path.vertices:
                    verts.append(
                        _to_mm((float(v[0]), float(v[1])), scale_info)
                    )
            elif hasattr(path, "edges"):
                for edge in path.edges:
                    et = getattr(edge, "EDGE_TYPE", None)
                    if et == "LineEdge":
                        verts.append(_to_mm(
                            (float(edge.start[0]), float(edge.start[1])),
                            scale_info,
                        ))
                        verts.append(_to_mm(
                            (float(edge.end[0]), float(edge.end[1])),
                            scale_info,
                        ))
                    elif hasattr(edge, "start"):
                        verts.append(_to_mm(
                            (float(edge.start[0]), float(edge.start[1])),
                            scale_info,
                        ))
            if len(verts) >= 3:
                # de-dup consecutive duplicates from edge expansion
                cleaned: list[tuple[float, float]] = []
                for v in verts:
                    if not cleaned or cleaned[-1] != v:
                        cleaned.append(v)
                if len(cleaned) >= 3:
                    hatches.append(RoomHatch(
                        polygon_mm=cleaned,
                        layer=layer,
                        pattern=pattern,
                    ))
    return hatches


# ── Polygon derivation ────────────────────────────────────────
def _flood_fill_polygon(anchor_xy: tuple[float, float],
                        anchor_area_m2: float,
                        walls: list[WallSegment],
                        ray_count: int = 32) -> Optional[list[tuple[float, float]]]:
    """Cast N rays from the anchor and stitch nearest hits into a polygon.

    Missing rays are skipped (the polygon just has fewer corners). The
    polygon is accepted as long as we keep at least 3 ordered hits.
    """
    pts: list[tuple[float, float]] = []
    for k in range(ray_count):
        ang = 2.0 * math.pi * k / ray_count
        direction = (math.cos(ang), math.sin(ang))
        hit = _cast_ray_to_walls(anchor_xy, direction, walls)
        if hit is not None:
            pts.append(hit)
    if len(pts) < 3:
        return None
    return pts


def _bbox_polygon(anchor_xy: tuple[float, float],
                  walls: list[WallSegment]) -> Optional[list[tuple[float, float]]]:
    """Cast 4 axis-aligned rays from anchor; return rectangle of hits.

    Returns None if any of N/S/E/W rays misses (room not enclosed
    on that side, e.g. open balcony).
    """
    directions = [
        (1.0, 0.0),    # E
        (-1.0, 0.0),   # W
        (0.0, 1.0),    # N
        (0.0, -1.0),   # S
    ]
    hits = []
    for d in directions:
        hit = _cast_ray_to_walls(anchor_xy, d, walls)
        if hit is None:
            return None
        hits.append(hit)

    east_x = hits[0][0]
    west_x = hits[1][0]
    north_y = hits[2][1]
    south_y = hits[3][1]

    ax, ay = anchor_xy
    if not (west_x < ax < east_x and south_y < ay < north_y):
        return None

    # Inset 50 mm so polygon doesn't touch walls
    INSET = 50.0
    return [
        (west_x + INSET,  south_y + INSET),
        (east_x - INSET,  south_y + INSET),
        (east_x - INSET,  north_y - INSET),
        (west_x + INSET,  north_y - INSET),
    ]


# Slice 16.1.5.2.d: catastrophe cap for leaked polygons.
# > 2.5 (loop-level review band) , << 1700-3400 (D31 observed).
POLYGON_REJECT_RATIO = 5.0

# Slice 18.24.2: wall-derived polygons are synthetic geometry and directly
# drive room containment. The visual multi-floor QA showed real leaks at
# 2.5-4.95x, below the old catastrophe cap. Keep the legacy cap for generic
# helpers/hatches, but apply this stricter acceptance band to wall_bbox and
# walls_flood candidates so oversized derived geometry can fall through.
WALL_DERIVED_POLYGON_REJECT_RATIO = 2.5
SPECIAL_SURFACE_POLYGON_REJECT_RATIO = 1.5
WALL_DERIVED_MAX_RADIUS_FACTOR = 4.0
WALL_DERIVED_MIN_MAX_RADIUS_MM = 8000.0
SPECIAL_SURFACE_MAX_RADIUS_FACTOR = 2.5
SPECIAL_SURFACE_ROOM_PATTERNS = (
    "BALKON",
    "LOGGIA",
    "TERRASSE",
    "FLACHDACH",
    "PODEST",
    "VORPLATZ",
    "GARAGE",
    "GARAGEN",
    "DOPPELPARKER",
    "GEHWEG",
    "RAMPE",
    "SPIELPLATZ",
    # Slice 1.28.0: EG-Außenflächen (Pre-Read: 8 Räume, alle EG). GRÄSER in
    # beiden Varianten — Downstream-Matcher (apartment_clustering.is_outdoor,
    # unit_faces._fidelity_buckets, building_units._is_outdoor) upper()n ohne
    # Umlaut-Translation, _is_special_surface_room normalisiert Ä→AE.
    "EIGENGARTEN",
    "GRÄSER",
    "GRAESER",
    "STAUDENBEET",
)


def _norm_room_name(value: str) -> str:
    return (value or "").upper().replace("Ä", "AE").replace("Ö", "OE").replace(
        "Ü", "UE").replace("ẞ", "SS")


def _is_special_surface_room(name: str) -> bool:
    norm = _norm_room_name(name)
    return any(pattern in norm for pattern in SPECIAL_SURFACE_ROOM_PATTERNS)


def _polygon_area_ratio(polygon: list[tuple[float, float]],
                        anchor_area_m2: float) -> float:
    """Polygon area / expected area. Returns 1.0 if expected is 0."""
    expected_mm2 = anchor_area_m2 * 1_000_000.0
    if expected_mm2 <= 0:
        return 1.0
    return _polygon_area(polygon) / expected_mm2


def _polygon_sane(polygon: list[tuple[float, float]],
                  anchor_area_m2: float) -> bool:
    """Slice 16.1.5.2.d: reject catastrophically oversized polygons.

    A ray leaking through a window-frame or fragment gap traces a polygon
    enclosing far more than the room (D31: wall_bbox ratios 1700-3400x on
    WHA_MOL_4OG). Such polygons drag placements outside the room. Reject
    anything above POLYGON_REJECT_RATIO so derive_room_polygon falls through
    to the next source.

    Empty polygons are never sane. When no expected area is known
    (anchor_area_m2 <= 0) size is unjudgeable, so we keep the polygon
    (old behaviour) rather than discard usable geometry.
    """
    if not polygon:
        return False
    if anchor_area_m2 <= 0:
        return True
    return _polygon_area_ratio(polygon, anchor_area_m2) <= POLYGON_REJECT_RATIO


def _wall_derived_polygon_sane(polygon: list[tuple[float, float]],
                               anchor_area_m2: float,
                               max_ratio: float = WALL_DERIVED_POLYGON_REJECT_RATIO,
                               anchor_xy: Optional[tuple[float, float]] = None,
                               max_radius_factor: float = WALL_DERIVED_MAX_RADIUS_FACTOR) -> bool:
    """Stricter guard for raycast-derived room polygons.

    ``_polygon_sane`` remains the broad compatibility check. This helper is
    used only when accepting wall_bbox / walls_flood as a room polygon source.
    """
    if not _polygon_sane(polygon, anchor_area_m2):
        return False
    if anchor_area_m2 <= 0:
        return True
    if anchor_xy is not None:
        expected_span = math.sqrt(anchor_area_m2) * 1000.0
        max_radius = max(
            WALL_DERIVED_MIN_MAX_RADIUS_MM,
            expected_span * max_radius_factor,
        )
        if any(math.hypot(x - anchor_xy[0], y - anchor_xy[1]) > max_radius
               for x, y in polygon):
            return False
    return (
        _polygon_area_ratio(polygon, anchor_area_m2)
        <= max_ratio
    )


_POLYGON_SOURCE_RANK = {
    "hatch": 0,
    "wall_bbox": 1,
    "walls_flood": 2,
}
POLYGON_CANDIDATE_NEAR_TOL = 0.15
PolygonCandidate = tuple[
    list[tuple[float, float]],
    str,
    RoomHatch | list[tuple[float, float]] | None,
]


def _polygon_candidate_score(candidate: PolygonCandidate,
                             anchor_area_m2: float) -> tuple[float, int, int, float]:
    """Rank accepted polygon candidates.

    Area agreement is the strongest signal. Source rank breaks near ties, then
    smaller area wins as the conservative containment choice.
    """
    polygon, source, meta = candidate
    ratio = _polygon_area_ratio(polygon, anchor_area_m2)
    if anchor_area_m2 <= 0:
        ratio = 1.0
    area_error = abs(ratio - 1.0)
    source_rank = _POLYGON_SOURCE_RANK.get(source, 99)
    semantic_rank = _hatch_semantic_rank(meta) if source == "hatch" else 99
    return (
        max(0.0, area_error - POLYGON_CANDIDATE_NEAR_TOL),
        source_rank,
        semantic_rank,
        area_error,
    )


# Slice B'-overshrink-guard: a bridge that closes a passage can also clip a
# room far below its anchor area (D-B': VR-top25 0.37x, COMMUNAL leak-rooms).
# When the bridged polygon undershoots this ratio, re-derive WITHOUT bridges
# and keep whichever polygon sits closer to the anchor area (= saner). The
# "closer to 1.0" test protects the bridge-dependent rooms generically: a room
# whose un-bridged derivation leaks oversized (VR-top19/24: 1.5-3.9x) keeps its
# bridged polygon instead of swapping into the leak.
OVERSHRINK_RATIO = 0.6


def derive_room_polygon(
    anchor: RoomAnchor,
    hatches: list[RoomHatch | list[tuple[float, float]]],
    walls: list[WallSegment],
    doors: Optional[list[Door]] = None,
    windows: Optional[list[Window]] = None,
    bridges: Optional[list[WallSegment]] = None,
    diag: Optional[dict] = None,
) -> tuple[list[tuple[float, float]], str]:
    """Slice 16.1.5.2.b: doors enable virtual-wall gap closure.

    Doors-Liste wird in WallSegment-Objekte umgewandelt (siehe
    _build_virtual_walls_from_doors mit +50mm extension) und VOR Raycast
    in die walls-Liste eingefügt. Polygon traced damit die korrekte
    Raum-Boundary inkl. Tür-Linien — kein Ray-Leak durch Wand-Gaps mehr.
    Windows excluded (D7-Pre-Read: walls bereits durchgehend an
    Fenster-Positionen).

    Slice B'-overshrink-guard: nach der gebridgten Ableitung greift ein
    Per-Raum-Guard — schrumpft ein Bridge den Raum unter OVERSHRINK_RATIO
    der Anchor-Fläche, wird ohne Bridges neu abgeleitet und das sanere
    Polygon (näher an Anchor) behalten.

    Slice 18.19.1 (Diagnose-only): ``diag`` ist ein optionales Out-Dict.
    Wenn ein voll umschlossenes (4-Ray-) bbox-Polygon existierte, aber von
    ``_polygon_sane`` als oversize verworfen wurde (Ratio > POLYGON_REJECT_RATIO),
    wird ``diag['reject_ratio']`` gesetzt. Trennt KG-Abteile (umschlossen,
    geleakt) von echten open-boundary-Räumen (bbox=None). Beeinflusst KEINE
    Geometrie/Auswahl — reiner Diagnose-Kanal für review_reason.
    """
    pt = (anchor.anchor_x_mm, anchor.anchor_y_mm)
    wall_derived_max_ratio = (
        SPECIAL_SURFACE_POLYGON_REJECT_RATIO
        if _is_special_surface_room(anchor.name)
        else WALL_DERIVED_POLYGON_REJECT_RATIO
    )
    wall_derived_max_radius_factor = (
        SPECIAL_SURFACE_MAX_RADIUS_FACTOR
        if _is_special_surface_room(anchor.name)
        else WALL_DERIVED_MAX_RADIUS_FACTOR
    )

    def _derive(use_bridges: bool) -> tuple[list[tuple[float, float]], str]:
        eff_walls = walls
        # Slice B'-fragment-gap-closure: collinear-fragment bridges close
        # un-doored passages before raycast (with door/window virtual walls).
        if use_bridges and bridges:
            eff_walls = eff_walls + bridges
        if doors:
            virtual = _build_virtual_walls_from_doors(doors, walls)
            if virtual:
                eff_walls = eff_walls + virtual
        if windows:
            virtual_win = _build_virtual_walls_from_windows(windows, walls)
            if virtual_win:
                eff_walls = eff_walls + virtual_win
        candidates: list[PolygonCandidate] = []

        # 1) Wall-bounding-box (clean axis-aligned rectangles).
        bbox_poly = _bbox_polygon(pt, eff_walls)
        if bbox_poly and _wall_derived_polygon_sane(
            bbox_poly,
            anchor.area_m2,
            max_ratio=wall_derived_max_ratio,
            anchor_xy=pt,
            max_radius_factor=wall_derived_max_radius_factor,
        ):
            candidates.append((bbox_poly, "wall_bbox", None))
        # Diagnose-only (18.19.1 + 18.24.2): bbox lieferte ein voll
        # umschlossenes Polygon (alle 4 Rays trafen), das aber oversize
        # verworfen wurde. area>0 + non-empty bbox + nicht wall-derived-sane
        # => Ratio > WALL_DERIVED_POLYGON_REJECT_RATIO.
        elif bbox_poly and diag is not None and anchor.area_m2 > 0:
            diag["reject_ratio"] = _polygon_area_ratio(bbox_poly, anchor.area_m2)
        # 2) 32-ray flood fill (fallback).
        poly = _flood_fill_polygon(pt, anchor.area_m2, eff_walls)
        if poly and _wall_derived_polygon_sane(
            poly,
            anchor.area_m2,
            max_ratio=wall_derived_max_ratio,
            anchor_xy=pt,
            max_radius_factor=wall_derived_max_radius_factor,
        ):
            candidates.append((poly, "walls_flood", None))
        if candidates:
            best_poly, best_src, _ = min(
                candidates,
                key=lambda cand: _polygon_candidate_score(cand, anchor.area_m2),
            )
            return (best_poly, best_src)
        return ([], "anchor_only")

    poly, src = _derive(use_bridges=True)

    # Slice B'-overshrink-guard: only when bridges actually contributed and we
    # have a measurable polygon + expected area to compare against.
    if bridges and src != "anchor_only" and anchor.area_m2 > 0:
        ratio = _polygon_area_ratio(poly, anchor.area_m2)
        if ratio < OVERSHRINK_RATIO:
            poly_u, src_u = _derive(use_bridges=False)
            if poly_u:
                ratio_u = _polygon_area_ratio(poly_u, anchor.area_m2)
                # Swap only if the un-bridged polygon is the saner one (closer
                # to the anchor area) — keeps bridge-dependent rooms intact.
                if abs(ratio_u - 1.0) < abs(ratio - 1.0):
                    return (poly_u, src_u)
    return (poly, src)


def assign_top_to_rooms(rooms: list[Room], tops: list[TopBoundary]) -> None:
    """Assign each room to nearest TOP anchor (Euclidean)."""
    if not tops:
        for r in rooms:
            r.review_flag = True
            r.review_reason = "no TOPs detected"
        return
    for r in rooms:
        rp = (r.anchor.anchor_x_mm, r.anchor.anchor_y_mm)
        best_t = None
        best_d = math.inf
        for t in tops:
            d = math.hypot(t.anchor_mm[0] - rp[0], t.anchor_mm[1] - rp[1])
            if d < best_d:
                best_d = d
                best_t = t
        if best_t is not None:
            r.anchor.top = best_t.top_id


# ── Furniture extraction (Slice 11.10.0) ──────────────────────
# Layer-Regex deckt 07_MOB-* (Wohnmöbel) und 07-SAN-* (Sanitär,
# Küchengeräte inkl. ...-Küche-Sub-Layer). 07-SYM-* trägt die kurzen
# Fachpraxis-Marker aus der PDF (GS, MIKRO, BR, AR, WM, WV/MV ...).
_FURNITURE_LAYER_RE = re.compile(r"^07[_-](MOB|SAN)", re.IGNORECASE)
_FURNITURE_MARKER_LAYER_RE = re.compile(r"^07-SYM", re.IGNORECASE)
_MARKER_TEXT_MAX_LEN = 32
_LABEL_TO_FURNITURE_MAX_MM = 700.0

# Block-Name -> category_hint Stub-Lookup. Wird in 11.10.1 durch den
# Loader für backend/data/furniture_catalog.yaml ersetzt. Pattern-Quelle:
# .claude/skills/elektroplan-dxf-conventions/SKILL.md Lookup-Tabelle.
_CATEGORY_HINT_RULES: tuple[tuple[re.Pattern, str], ...] = (
    (re.compile(r"^K[üu]hlschrank$", re.IGNORECASE), "kueche_grossgeraet"),
    (re.compile(r"^kochfeld$", re.IGNORECASE),       "kueche_grossgeraet"),
    (re.compile(r"^Sp[üu]le$", re.IGNORECASE),       "kueche_grossgeraet"),
    (re.compile(r"^07-W[MT].*", re.IGNORECASE),      "bad_grossgeraet"),
    (re.compile(r"^07-WC.*", re.IGNORECASE),         "bad_sanitaer"),
    (re.compile(r"^07-(Dusche|Badewanne).*", re.IGNORECASE),
                                                     "bad_sanitaer"),
    (re.compile(r"^WANDL[ÜU]FER$", re.IGNORECASE),   "bad_klima"),
    (re.compile(r"^WET$", re.IGNORECASE),            "bad_grossgeraet"),
    (re.compile(r"^TV-", re.IGNORECASE),             "wohnzimmer_tv"),
    (re.compile(r"^BETT(_90)?$", re.IGNORECASE),     "schlafzimmer"),
    (re.compile(r"^ECKSOFA", re.IGNORECASE),         "wohnzimmer_moebel"),
    (re.compile(r"^m[öo]bel_(schreibtisch|tisch)$", re.IGNORECASE),
                                                     "wohnzimmer_moebel"),
)


def _category_hint(block_name: str) -> Optional[str]:
    for pat, cat in _CATEGORY_HINT_RULES:
        if pat.match(block_name):
            return cat
    return None


_MARKER_KIND_ALIASES: tuple[tuple[re.Pattern, str], ...] = (
    (re.compile(r"^\*$"), "KUEHLSCHRANK_STERN"),
    (re.compile(r"^GS$", re.IGNORECASE), "GS"),
    (re.compile(r"^MIKRO$", re.IGNORECASE), "MIKRO"),
    (re.compile(r"^BR$", re.IGNORECASE), "BR"),
    (re.compile(r"^AR$", re.IGNORECASE), "AR"),
    (re.compile(r"^WM$", re.IGNORECASE), "WM"),
    (re.compile(r"^WT$", re.IGNORECASE), "WT"),
    (re.compile(r"^HT$", re.IGNORECASE), "HT"),
    (re.compile(r"^BTA", re.IGNORECASE), "BTA"),
    (re.compile(r"\bWV\b", re.IGNORECASE), "WV"),
    (re.compile(r"\bMV\b", re.IGNORECASE), "MV"),
    (re.compile(r"KEMPER", re.IGNORECASE), "KEMPER"),
    (re.compile(r"REGEN|FALLROHR|DOWNPIPE", re.IGNORECASE), "DOWNPIPE"),
    (re.compile(r"KLIMA", re.IGNORECASE), "KLIMA"),
)


_SERVICE_MARKER_KIND_ALIASES: tuple[tuple[re.Pattern, str], ...] = (
    (re.compile(
        r"E[-_ ]?SCHACHT|SCHACHTTYP|SCHACHT|INSTALLATION|DDB|BDB|FBDB|HKLS|WDB|"
        r"\b(?:DD|BD|FBD|DDB|BDB|FBDB|WDD|WODD)\b"
        r"\s*(?:[-/]\s*)?(?:HT|ET)?\s*\d",
                re.IGNORECASE), "SCHACHT"),
    (re.compile(r"L[ÜU]FT|LUEFT|WANDL[ÜU]F|ABLUFT|ZULUFT",
                re.IGNORECASE), "LUEFTUNG"),
    (re.compile(r"AUFZUG|LIFT|STGH|STIEGENHAUS|PODEST",
                re.IGNORECASE), "AUFZUG"),
    (re.compile(r"TECHNIK|E[-_ ]?RAUM|ELEKTRO|MSR|HEIZRAUM|HAUSTECHNIK",
                re.IGNORECASE), "TECHNIK"),
)


def _marker_kinds(
    text: str,
    *,
    layer: str = "",
    max_len: int = _MARKER_TEXT_MAX_LEN,
    include_service: bool = False,
) -> list[str]:
    clean = _clean_annotation_text(text).strip()
    if not clean:
        return []
    out: list[str] = []
    if len(clean) <= max_len:
        for pat, kind in _MARKER_KIND_ALIASES:
            if pat.search(clean):
                out.append(kind)
        if include_service:
            service_clean = re.sub(r"\bL[ÜU]FTRAUM\b", "", clean, flags=re.IGNORECASE)
            for pat, kind in _SERVICE_MARKER_KIND_ALIASES:
                if pat.search(service_clean):
                    out.append(kind)
    if include_service:
        for pat, kind in _SERVICE_MARKER_KIND_ALIASES:
            if pat.search(layer):
                out.append(kind)
    deduped: list[str] = []
    for kind in out:
        if kind not in deduped:
            deduped.append(kind)
    return deduped


def _insert_bbox_mm(insert, scale_info: ScaleInfo) -> tuple[
    list[tuple[float, float]], Optional[tuple[float, float]], Optional[tuple[float, float]], Optional[str]
]:
    """Best-effort INSERT extents in mm-world.

    ezdxf can resolve many INSERT bounding boxes through block definitions. When
    it cannot, callers keep the insert point and the bbox fields stay optional.
    """
    try:
        ext = bbox.extents([insert])
    except Exception:
        return [], None, None, None
    try:
        minx, miny = float(ext.extmin.x), float(ext.extmin.y)
        maxx, maxy = float(ext.extmax.x), float(ext.extmax.y)
    except Exception:
        return [], None, None, None
    if not all(math.isfinite(v) for v in (minx, miny, maxx, maxy)):
        return [], None, None, None
    if maxx < minx or maxy < miny:
        return [], None, None, None
    p0 = _to_mm((minx, miny), scale_info)
    p1 = _to_mm((maxx, miny), scale_info)
    p2 = _to_mm((maxx, maxy), scale_info)
    p3 = _to_mm((minx, maxy), scale_info)
    center = ((p0[0] + p2[0]) / 2.0, (p0[1] + p2[1]) / 2.0)
    size = (abs(p2[0] - p0[0]), abs(p2[1] - p0[1]))
    return [p0, p1, p2, p3], center, size, "insert_bbox"


def _entity_bbox_mm(entity, scale_info: ScaleInfo) -> tuple[
    list[tuple[float, float]], Optional[tuple[float, float]], Optional[tuple[float, float]]
]:
    """Best-effort TEXT/MTEXT extents in mm-world for service diagnostics."""
    try:
        ext = bbox.extents([entity])
    except Exception:
        return [], None, None
    try:
        minx, miny = float(ext.extmin.x), float(ext.extmin.y)
        maxx, maxy = float(ext.extmax.x), float(ext.extmax.y)
    except Exception:
        return [], None, None
    if not all(math.isfinite(v) for v in (minx, miny, maxx, maxy)):
        return [], None, None
    if maxx < minx or maxy < miny:
        return [], None, None
    p0 = _to_mm((minx, miny), scale_info)
    p1 = _to_mm((maxx, miny), scale_info)
    p2 = _to_mm((maxx, maxy), scale_info)
    p3 = _to_mm((minx, maxy), scale_info)
    center = ((p0[0] + p2[0]) / 2.0, (p0[1] + p2[1]) / 2.0)
    size = (abs(p2[0] - p0[0]), abs(p2[1] - p0[1]))
    return [p0, p1, p2, p3], center, size


def _nearest_labels(
    point: tuple[float, float],
    markers: list[ArchitectureMarker],
    max_dist_mm: float = _LABEL_TO_FURNITURE_MAX_MM,
) -> list[str]:
    ranked: list[tuple[float, str]] = []
    for marker in markers:
        d = math.hypot(marker.x_mm - point[0], marker.y_mm - point[1])
        if d <= max_dist_mm:
            ranked.append((d, marker.text))
    ranked.sort(key=lambda item: item[0])
    return [text for _, text in ranked]


def _block_marker_kind(block_name: str) -> Optional[str]:
    name = (block_name or "").strip()
    rules = (
        (re.compile(r"^07_Kemper-?ventil$", re.IGNORECASE), "KEMPER"),
        (re.compile(r"^KLIMAGER[ÄA]T$", re.IGNORECASE), "KLIMA"),
        (re.compile(r"^07_Klimasifon$", re.IGNORECASE), "KLIMA_SIPHON"),
        (re.compile(r"^07-WM", re.IGNORECASE), "WM"),
        (re.compile(r"^07-WT", re.IGNORECASE), "WT"),
        (re.compile(r"^07-WC", re.IGNORECASE), "WC"),
        (re.compile(r"^WANDL[ÜU]F", re.IGNORECASE), "LUEFTER"),
        (re.compile(r"^K[üu]hlschrank", re.IGNORECASE), "KUEHLSCHRANK"),
        (re.compile(r"^kochfeld", re.IGNORECASE), "KOCHFELD"),
        (re.compile(r"^Sp[üu]le", re.IGNORECASE), "SPUELE"),
        (re.compile(r"^TV-", re.IGNORECASE), "TV"),
        (re.compile(r"^BETT", re.IGNORECASE), "BETT"),
    )
    for pat, kind in rules:
        if pat.search(name):
            return kind
    return None


def extract_markers(block: BlockLayout,
                    scale_info: ScaleInfo,
                    rooms: list[Room],
                    walls: Optional[list[WallSegment]] = None,
                    profile: Optional[LayerProfile] = None) -> list[ArchitectureMarker]:
    """Extract text markers used by Fachpraxis and service-core detection."""
    from parsers.room_partition import assign_room
    wall_segs = [(w.start_mm, w.end_mm) for w in (walls or [])]
    marker_cfg = _role_config(profile, "markers") if profile is not None else {}
    if marker_cfg:
        layer_patterns = _compile_role_patterns(profile, "markers")
        include_service = bool(marker_cfg.get("classify_service", False))
        max_len = int(marker_cfg.get("max_text_len") or 80)
    else:
        layer_patterns = (_FURNITURE_MARKER_LAYER_RE,)
        include_service = False
        max_len = _MARKER_TEXT_MAX_LEN
    out: list[ArchitectureMarker] = []
    seen: set[tuple[str, str, str, int, int]] = set()
    for e in block:
        entity_type = e.dxftype()
        if entity_type not in {"TEXT", "MTEXT", "INSERT"}:
            continue
        if entity_type == "INSERT" and not include_service:
            continue
        layer = str(e.dxf.layer)
        if not _layer_matches(layer, layer_patterns):
            continue
        if entity_type == "INSERT":
            text = str(e.dxf.name)
            bbox_mm, center_mm, _, _ = _insert_bbox_mm(e, scale_info)
        else:
            text = _clean_annotation_text(_entity_plain_text(e))
            bbox_mm, center_mm, _ = _entity_bbox_mm(e, scale_info)
        kinds = _marker_kinds(
            text,
            layer=layer,
            max_len=max_len,
            include_service=include_service,
        )
        if not kinds:
            continue
        insert_x_mm, insert_y_mm = _to_mm(_entity_insert_xy(e), scale_info)
        if entity_type == "INSERT":
            x_mm, y_mm = center_mm or (insert_x_mm, insert_y_mm)
        else:
            x_mm, y_mm = (insert_x_mm, insert_y_mm)
        room_idx: Optional[int] = assign_room((x_mm, y_mm), rooms, wall_segs)
        apartment_id: Optional[str] = (
            rooms[room_idx].anchor.top if room_idx is not None else None
        )
        for kind in kinds:
            key = (kind, text, layer, round(x_mm), round(y_mm))
            if key in seen:
                continue
            seen.add(key)
            out.append(ArchitectureMarker(
                text=text,
                marker_kind=kind,
                layer=layer,
                x_mm=x_mm,
                y_mm=y_mm,
                room_idx=room_idx,
                apartment_id=apartment_id,
                bbox_mm=bbox_mm,
                center_mm=center_mm,
                source_entity_type=entity_type,
            ))
    return out


def extract_furniture(block: BlockLayout,
                      scale_info: ScaleInfo,
                      rooms: list[Room],
                      walls: Optional[list[WallSegment]] = None,
                      profile: Optional[LayerProfile] = None,
                      markers: Optional[list[ArchitectureMarker]] = None) -> list[Furniture]:
    """Extract möbel/sanitär INSERTs from architecture-DXF.

    Iterates INSERTs on configured furniture layers and
    returns a flat list of Furniture records. Each record carries its
    room_idx and apartment_id (= ``rooms[room_idx].anchor.top``).

    Slice 18.3.2: room_idx via ``room_partition.assign_room`` — point-in-polygon
    first, then nearest label-anchor with a wall-clear line of sight. This fixes
    open floor plans (open kitchen-living has no closed wall loop, so pure
    containment left >40% of furniture unassigned).
    """
    from parsers.room_partition import assign_room
    wall_segs = [(w.start_mm, w.end_mm) for w in (walls or [])]
    layer_patterns = (
        _compile_role_patterns(profile, "furniture")
        if profile is not None else (_FURNITURE_LAYER_RE,)
    )
    markers = markers or []
    out: list[Furniture] = []
    for e in block:
        if e.dxftype() != "INSERT":
            continue
        layer = e.dxf.layer
        if not _layer_matches(layer, layer_patterns):
            continue
        name = e.dxf.name
        x_mm, y_mm = _to_mm((e.dxf.insert.x, e.dxf.insert.y), scale_info)
        rotation_deg = float(e.dxf.rotation or 0.0)
        room_idx: Optional[int] = assign_room((x_mm, y_mm), rooms, wall_segs)
        apartment_id: Optional[str] = (
            rooms[room_idx].anchor.top if room_idx is not None else None
        )
        bbox_mm, center_mm, size_mm, bbox_confidence = _insert_bbox_mm(e, scale_info)
        label_anchor = center_mm or (x_mm, y_mm)
        out.append(Furniture(
            block_name=name,
            layer=layer,
            x_mm=x_mm,
            y_mm=y_mm,
            rotation_deg=rotation_deg,
            room_idx=room_idx,
            apartment_id=apartment_id,
            category_hint=_category_hint(name),
            bbox_mm=bbox_mm,
            center_mm=center_mm,
            size_mm=size_mm,
            text_labels=_nearest_labels(label_anchor, markers),
            marker_kind=_block_marker_kind(name),
            bbox_confidence=bbox_confidence,
        ))
    out.extend(_extract_san_heater_rects(
        block, scale_info, rooms, wall_segs, layer_patterns, markers,
    ))
    return out


# Heizkoerper sind im Architektplan KEINE Bloecke, sondern nackte
# LWPOLYLINE-Rechtecke auf 07-SAN (Slice 2.14.5, Korrektur-DXF TOP 24:
# Handtuchheizkoerper 50x600 mm an der BAD-Wand, User-HT-Dose sitzt auf der
# Heizkoerper-MITTE). Signatur: geschlossenes achsparalleles Rechteck,
# Schmalseite 30-120 mm, Laengsseite 300-1500 mm.
_HEATER_RECT_SHORT_MM = (30.0, 120.0)
_HEATER_RECT_LONG_MM = (300.0, 1500.0)


def _extract_san_heater_rects(block: BlockLayout,
                              scale_info: ScaleInfo,
                              rooms: list[Room],
                              wall_segs: list,
                              layer_patterns,
                              markers: list[ArchitectureMarker]) -> list[Furniture]:
    from parsers.room_partition import assign_room
    out: list[Furniture] = []
    for e in block:
        if e.dxftype() != "LWPOLYLINE":
            continue
        layer = e.dxf.layer
        if "SAN" not in layer.upper():
            continue
        if not _layer_matches(layer, layer_patterns):
            continue
        pts = [(p[0], p[1]) for p in e.get_points()]
        if len(pts) == 5 and abs(pts[0][0] - pts[4][0]) < 1e-9 and abs(pts[0][1] - pts[4][1]) < 1e-9:
            pts = pts[:4]
        if len(pts) != 4:
            continue
        if not all(
            abs(pts[i][0] - pts[(i + 1) % 4][0]) < 1e-6
            or abs(pts[i][1] - pts[(i + 1) % 4][1]) < 1e-6
            for i in range(4)
        ):
            continue
        pts_mm = [_to_mm(p, scale_info) for p in pts]
        xs = [p[0] for p in pts_mm]
        ys = [p[1] for p in pts_mm]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        short, long_ = min(w, h), max(w, h)
        if not (_HEATER_RECT_SHORT_MM[0] <= short <= _HEATER_RECT_SHORT_MM[1]
                and _HEATER_RECT_LONG_MM[0] <= long_ <= _HEATER_RECT_LONG_MM[1]):
            continue
        cx, cy = (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0
        room_idx = assign_room((cx, cy), rooms, wall_segs)
        bbox = [
            (min(xs), min(ys)), (max(xs), min(ys)),
            (max(xs), max(ys)), (min(xs), max(ys)),
        ]
        out.append(Furniture(
            block_name="HEIZKOERPER_SAN_RECT",
            layer=layer,
            x_mm=cx,
            y_mm=cy,
            rotation_deg=0.0,
            room_idx=room_idx,
            apartment_id=(
                rooms[room_idx].anchor.top if room_idx is not None else None
            ),
            category_hint="bad_heizkoerper",
            bbox_mm=bbox,
            center_mm=(cx, cy),
            size_mm=(w, h),
            text_labels=_nearest_labels((cx, cy), markers),
            marker_kind="HT",
            bbox_confidence="polyline_rect",
        ))
    return out


def annotate_walls_with_fil_material(
    walls: list[WallSegment],
    hatches: list[RoomHatch],
) -> None:
    """Slice 18.36.0 — additive FIL→WallSegment material annotation (ADR 0011).

    Reuses the B+A matcher from ``check_fil_match_coverage`` to set
    ``thickness_mm`` + ``material_class`` on the LINE walls covered by an
    in-band FIL hatch. Pure and counts-neutral: it mutates existing
    WallSegments in place, never splits/filters them. A wall matched by
    several hatches keeps the one with the largest on-axis overlap. No
    consumption — meaning/mounting stays Track B.
    """
    # Function-local import: check_fil_match_coverage imports this module, so a
    # top-level import would be circular (mirrors the apartment_clustering
    # import inside parse_architecture below).
    from diagnostics.check_fil_match_coverage import (
        LONG_TOL_MM,
        _in_band,
        _interval_overlap_len,
        _line_set_matches_hatch,
        _obb,
        _offset_fallback_matches_hatch,
        _segment_interval_on_axis,
        _suffix,
    )

    line_walls = [w for w in walls if w.wall_type != "hatch_boundary"]
    if not line_walls:
        return

    def _claim(best: dict, indices, long_, short_, axu, axv, cx, cy, sx,
               skip: set) -> None:
        hatch_span = (-long_ / 2 - LONG_TOL_MM, long_ / 2 + LONG_TOL_MM)
        for si in indices:
            if si in skip:
                continue
            iv = _segment_interval_on_axis(line_walls[si], axu, axv, cx, cy)
            ov = _interval_overlap_len(iv, hatch_span)
            cur = best.get(si)
            if cur is None or ov > cur[0]:
                best[si] = (ov, short_, sx)

    # Pass 1 — PRIMARY (autoritativ). Primary-rejected Hatches für Pass 2 merken.
    primary: dict[int, tuple[float, float, str]] = {}
    rejected: list[tuple] = []
    for h in hatches:
        long_, short_, axu, axv, cx, cy = _obb(h.polygon_mm)
        if not _in_band(short_):
            continue
        sx = _suffix(h.layer)
        matched, indices = _line_set_matches_hatch(
            line_walls, long_, short_, axu, axv, cx, cy
        )
        if matched:
            _claim(primary, indices, long_, short_, axu, axv, cx, cy, sx, set())
        else:
            rejected.append((long_, short_, axu, axv, cx, cy, sx))

    # Pass 2 — Slice 18.38.0 KG-Offset-Fallback. Füllt NUR primary-freie LINEs:
    # ein versetzter Fallback überschreibt NIE einen sauberen Primary-Match
    # (sonst kippte eine ferne Offset-Hatch eine LINE mit näherer on-axis-Hatch).
    fallback: dict[int, tuple[float, float, str]] = {}
    primary_walls = set(primary)
    for (long_, short_, axu, axv, cx, cy, sx) in rejected:
        matched, indices = _offset_fallback_matches_hatch(
            line_walls, long_, short_, axu, axv, cx, cy, sx
        )
        if matched:
            _claim(fallback, indices, long_, short_, axu, axv, cx, cy, sx,
                   primary_walls)

    for si, (_ov, short_, sx) in {**fallback, **primary}.items():
        line_walls[si].thickness_mm = short_
        line_walls[si].material_class = sx


_PROFILE_STRATEGY_REGISTRY = {
    "rooms": {"anchor_raycast", "closed_polygons"},
    "walls": {"lwpolyline_typed", "line_plus_hatch"},
    "wall_material": {"hatch_boundary_plus_thickness_annotation", "disabled"},
    "doors": {"blocks_by_name_pattern", "blocks_by_layer_pattern"},
    "windows": {"blocks_by_name_pattern", "blocks_by_layer_pattern"},
    "furniture": {"blocks_by_layer_pattern"},
    "markers": {"text_by_layer_pattern", "disabled"},
}


def _role_config(profile: LayerProfile, role: str) -> dict:
    return dict(profile.roles.get(role) or {})


def _compile_patterns(patterns: list[str] | tuple[str, ...]) -> tuple[re.Pattern, ...]:
    return tuple(re.compile(str(pattern), re.IGNORECASE) for pattern in patterns)


def _compile_role_patterns(profile: LayerProfile,
                           role: str,
                           key: str = "layer_patterns") -> tuple[re.Pattern, ...]:
    return _compile_patterns(tuple(_role_config(profile, role).get(key) or ()))


def _layer_matches(layer: str, patterns: tuple[re.Pattern, ...]) -> bool:
    return any(pattern.search(layer) for pattern in patterns)


def _hatch_boundary_paths_native(entity) -> list[list[tuple[float, float]]]:
    """Return simple native 2D boundary paths from a HATCH entity."""
    paths: list[list[tuple[float, float]]] = []
    for path in entity.paths:
        verts: list[tuple[float, float]] = []
        if hasattr(path, "vertices") and path.vertices:
            for vertex in path.vertices:
                verts.append((float(vertex[0]), float(vertex[1])))
        elif hasattr(path, "edges"):
            for edge in path.edges:
                if getattr(edge, "EDGE_TYPE", None) == "LineEdge":
                    verts.append((float(edge.start[0]), float(edge.start[1])))
                    verts.append((float(edge.end[0]), float(edge.end[1])))
                elif hasattr(edge, "start"):
                    verts.append((float(edge.start[0]), float(edge.start[1])))
        cleaned: list[tuple[float, float]] = []
        for vertex in verts:
            if not cleaned or cleaned[-1] != vertex:
                cleaned.append(vertex)
        if len(cleaned) >= 2 and cleaned[0] == cleaned[-1]:
            cleaned = cleaned[:-1]
        if len(cleaned) >= 3:
            paths.append(cleaned)
    return paths


def extract_rooms_closed_polygons(
    block: BlockLayout,
    scale_info: ScaleInfo,
    doors: list[Door],
    windows: list[Window],
    profile: LayerProfile,
    diagnostics: Optional[dict] = None,
) -> list[Room]:
    cfg = _role_config(profile, "rooms")
    polygon_layers = _compile_role_patterns(profile, "rooms", "polygon_layers")
    label_layers = _compile_role_patterns(profile, "rooms", "label_layers")
    open_cfg = dict(cfg.get("open_contour") or {})
    micro_gap_max_mm = float(open_cfg.get("micro_gap_max_mm", 100.0))
    micro_area_max_m2 = float(open_cfg.get("micro_gap_max_closing_area_m2", 0.01))
    min_room_area_m2 = float(open_cfg.get("min_room_area_m2", 0.5))
    polygon_source = str(cfg.get("polygon_source") or "closed_polygon_profile")
    prefer_bold = bool(cfg.get("label_prefer_bold", False))
    # Slice N7: Mini-Polygon-Filter (Schacht-/Lüftungs-Kästchen auf dem
    # Raum-Layer klauen sonst Label-Gruppen). Opt-in pro Profil, 0.0 = aus.
    min_polygon_area_m2 = float(cfg.get("min_polygon_area_m2", 0.0))
    entity_types = {
        str(entity_type).upper()
        for entity_type in (cfg.get("entity_types") or ["LWPOLYLINE"])
    }

    candidates = []
    candidate_diag = {
        "a_raeume_lwpolyline_total": 0,
        "closed_flag": 0,
        "closed_by_repeated_endpoint": 0,
        "strict_closed": 0,
        "micro_gap_closed": 0,
        "micro_gap_artifact_rejected": 0,
        "large_open_rejected": 0,
        "accepted": 0,
        "rejected_open": 0,
        "rejected_degenerate": 0,
        "rejected_below_min_area": 0,
        "open_rejections": [],
    }

    for entity_index, e in enumerate(block):
        if e.dxftype() != "LWPOLYLINE":
            continue
        layer = str(e.dxf.layer)
        if not _layer_matches(layer, polygon_layers):
            continue
        candidate_diag["a_raeume_lwpolyline_total"] += 1
        native = [(float(p[0]), float(p[1])) for p in e.get_points("xy")]
        if len(native) < 2:
            candidate_diag["rejected_degenerate"] += 1
            continue

        closed_by_flag = bool(e.closed)
        closed_by_endpoint = len(native) >= 2 and native[0] == native[-1]
        if closed_by_flag:
            candidate_diag["closed_flag"] += 1
        if closed_by_endpoint:
            candidate_diag["closed_by_repeated_endpoint"] += 1

        status = "strict_closed" if (closed_by_flag or closed_by_endpoint) else "open"
        if closed_by_endpoint:
            native = native[:-1]
        poly_mm = [(x * scale_info.factor_to_mm, y * scale_info.factor_to_mm)
                   for x, y in native]
        area_m2 = _polygon_area(poly_mm) / 1_000_000.0
        if len(poly_mm) < 3 or area_m2 <= 0:
            candidate_diag["rejected_degenerate"] += 1
            continue
        if min_polygon_area_m2 > 0.0 and area_m2 < min_polygon_area_m2:
            candidate_diag["rejected_below_min_area"] += 1
            continue

        if status == "open":
            gap_mm = math.hypot(
                poly_mm[0][0] - poly_mm[-1][0],
                poly_mm[0][1] - poly_mm[-1][1],
            )
            rejection = {
                "entity_index": entity_index,
                "layer": layer,
                "vertices": len(native),
                "endpoint_gap_mm": gap_mm,
                "closing_area_m2": area_m2,
            }
            if gap_mm <= micro_gap_max_mm and area_m2 <= micro_area_max_m2:
                if area_m2 < min_room_area_m2:
                    rejection["reason"] = "micro_gap_sliver_below_min_room_area"
                    candidate_diag["micro_gap_artifact_rejected"] += 1
                    candidate_diag["rejected_open"] += 1
                    candidate_diag["open_rejections"].append(rejection)
                    continue
                status = "micro_gap_closed"
                candidate_diag["micro_gap_closed"] += 1
            else:
                rejection["reason"] = "large_or_gray_open_contour"
                candidate_diag["large_open_rejected"] += 1
                candidate_diag["rejected_open"] += 1
                candidate_diag["open_rejections"].append(rejection)
                continue

        if status == "strict_closed":
            candidate_diag["strict_closed"] += 1
        candidate_diag["accepted"] += 1
        candidates.append({
            "entity_index": entity_index,
            "layer": layer,
            "polygon_mm": poly_mm,
            "area_m2_polygon": area_m2,
            "centroid_mm": _polygon_centroid(poly_mm),
            "polygon_source": (
                f"{polygon_source}:micro_gap_closed"
                if status == "micro_gap_closed" else polygon_source
            ),
        })

    if "HATCH" in entity_types:
        candidate_diag["room_hatch_total"] = 0
        candidate_diag["room_hatch_paths"] = 0
        for entity_index, e in enumerate(block):
            if e.dxftype() != "HATCH":
                continue
            layer = str(e.dxf.layer)
            if not _layer_matches(layer, polygon_layers):
                continue
            candidate_diag["room_hatch_total"] += 1
            for native in _hatch_boundary_paths_native(e):
                candidate_diag["room_hatch_paths"] += 1
                poly_mm = [
                    (x * scale_info.factor_to_mm, y * scale_info.factor_to_mm)
                    for x, y in native
                ]
                area_m2 = _polygon_area(poly_mm) / 1_000_000.0
                if len(poly_mm) < 3 or area_m2 <= 0:
                    candidate_diag["rejected_degenerate"] += 1
                    continue
                if area_m2 < min_room_area_m2:
                    candidate_diag["rejected_degenerate"] += 1
                    continue
                candidate_diag["strict_closed"] += 1
                candidate_diag["accepted"] += 1
                candidates.append({
                    "entity_index": entity_index,
                    "layer": layer,
                    "polygon_mm": poly_mm,
                    "area_m2_polygon": area_m2,
                    "centroid_mm": _polygon_centroid(poly_mm),
                    "polygon_source": f"{polygon_source}:hatch_boundary",
                })

    labels = []
    for entity_index, e in enumerate(block):
        if e.dxftype() not in {"MTEXT", "TEXT"}:
            continue
        layer = str(e.dxf.layer)
        if not _layer_matches(layer, label_layers):
            continue
        raw = _entity_plain_text(e)
        name, area = _parse_room_label_text(raw)
        x, y = _entity_insert_xy(e)
        labels.append({
            "entity_index": entity_index,
            "raw_text": raw,
            "name": name,
            "area_m2_label": area,
            "bold": e.dxftype() == "MTEXT" and _mtext_markup_is_bold(str(e.text)),
            "position_mm": (x * scale_info.factor_to_mm,
                            y * scale_info.factor_to_mm),
        })

    # Slice N8: Raum-Namen aus INSERT-Attributen (ArchiCAD-Zonen-Stempel wie
    # Rennweg: pro Raum ein Block mit ROOM_NAME-Attribut auf dem Raum-Layer).
    # Opt-in via label_insert_attrib_tags; area_m2_label bleibt None, damit
    # das Flächen-Ratio-Verhalten (high/coarse) unverändert bleibt.
    insert_attrib_tags = [
        str(tag) for tag in (cfg.get("label_insert_attrib_tags") or [])
    ]
    insert_labels = []
    if insert_attrib_tags:
        for entity_index, e in enumerate(block):
            if e.dxftype() != "INSERT":
                continue
            layer = str(e.dxf.layer)
            if not _layer_matches(layer, label_layers):
                continue
            attribs = {
                str(a.dxf.tag): str(a.dxf.text) for a in e.attribs
            }
            name = next(
                (attribs[tag].strip() for tag in insert_attrib_tags
                 if attribs.get(tag, "").strip()),
                None,
            )
            if not name:
                continue
            insert_labels.append({
                "entity_index": entity_index,
                "name": name,
                "position_mm": (
                    float(e.dxf.insert.x) * scale_info.factor_to_mm,
                    float(e.dxf.insert.y) * scale_info.factor_to_mm,
                ),
            })

    area_label_groups = []
    for area_label in [label for label in labels if label["area_m2_label"] is not None]:
        ax, ay = area_label["position_mm"]
        nearby = []
        for label in labels:
            if label is area_label:
                continue
            lx, ly = label["position_mm"]
            if abs(lx - ax) <= 650.0 and abs(ly - ay) <= 850.0:
                nearby.append((label, lx - ax, ly - ay, math.hypot(lx - ax, ly - ay)))
        # Slice R2: "Top 2.06"-Stempel = Wohnungs-GESAMT-Fläche (Analogie
        # Mollgasse-TOP-Skip, Slice 1.8.0). Ist die nächste Zeile an dieser
        # Flächen-Zeile eine Top-Zeile, IST die Gruppe der Aggregat-Stempel
        # → keine Raum-Label-Gruppe (würde dem Raum-Polygon den echten
        # Namen wegschnappen, ratio 0.3–0.5).
        # Konvention: Namenszeile steht ÜBER der Flächen-Zeile (dy > 0).
        # Ist die nächste Zeile OBERHALB eine Top-Zeile, gehört diese
        # Fläche zum Wohnungs-Aggregat (Kombi-Stempel: "Top 1.09" +
        # Gesamt-m² direkt über dem Raumstempel) → droppen.
        above = [
            item for item in nearby
            if item[2] > 0.0
            and (_TOP_AGGREGATE_RE.match(str(item[0].get("name") or ""))
                 or _is_room_name_candidate(str(item[0].get("name") or "")))
        ]
        if above:
            nearest_above = min(above, key=lambda item: item[3])
            if _TOP_AGGREGATE_RE.match(
                    str(nearest_above[0].get("name") or "")):
                continue
        name_candidates = [
            item for item in nearby
            if _is_room_name_candidate(str(item[0].get("name") or ""))
        ]
        if prefer_bold:
            bold_candidates = [item for item in name_candidates if item[0].get("bold")]
            if bold_candidates:
                name_candidates = bold_candidates
        preferred = [item for item in name_candidates if 30.0 <= item[2] <= 450.0]
        chosen_name = None
        if preferred:
            chosen_name = sorted(
                preferred, key=lambda item: (abs(item[1]), abs(item[2] - 170.0))
            )[0][0]
        elif name_candidates:
            chosen_name = sorted(name_candidates, key=lambda item: item[3])[0][0]
        area_label_groups.append({
            "area_label": area_label,
            "name_label": chosen_name,
            "name": (chosen_name or {}).get("name") or "",
            "area_m2_label": area_label["area_m2_label"],
            "position_mm": area_label["position_mm"],
            "nearby_label_count": len(nearby),
        })

    for insert_label in insert_labels:
        area_label_groups.append({
            "area_label": {"entity_index": insert_label["entity_index"]},
            "name_label": None,
            "name": insert_label["name"],
            "area_m2_label": None,
            "position_mm": insert_label["position_mm"],
            "nearby_label_count": 0,
        })

    used_groups: set[int] = set()
    rooms: list[Room] = []
    area_deltas: list[float] = []
    label_assignments: list[dict] = []
    label_inside_count = 0
    for candidate in candidates:
        poly = candidate["polygon_mm"]
        centroid = candidate["centroid_mm"]
        containing = [
            (i, math.hypot(group["position_mm"][0] - centroid[0],
                           group["position_mm"][1] - centroid[1]))
            for i, group in enumerate(area_label_groups)
            if _point_in_polygon(group["position_mm"], poly)
        ]
        if containing:
            ranked = sorted(containing, key=lambda item: item[1])
        else:
            ranked = sorted(
                [
                    (i, math.hypot(group["position_mm"][0] - centroid[0],
                                   group["position_mm"][1] - centroid[1]))
                    for i, group in enumerate(area_label_groups)
                ],
                key=lambda item: item[1],
            )
        chosen = None
        for group_idx, distance in ranked:
            if group_idx not in used_groups:
                chosen = (group_idx, distance)
                break
        if chosen is None and ranked:
            chosen = ranked[0]

        label_group = None
        label_inside = False
        if chosen is not None:
            group_idx, _distance = chosen
            used_groups.add(group_idx)
            label_group = area_label_groups[group_idx]
            label_inside = _point_in_polygon(label_group["position_mm"], poly)
            if label_inside:
                label_inside_count += 1
        name = (label_group or {}).get("name") or f"Room {len(rooms) + 1}"
        area_label = (label_group or {}).get("area_m2_label")
        area_m2 = float(area_label) if area_label is not None else candidate["area_m2_polygon"]
        if area_label is not None:
            area_deltas.append(abs(candidate["area_m2_polygon"] - float(area_label)))
        label_assignments.append({
            "entity_index": candidate["entity_index"],
            "name": name,
            "area_m2_polygon": candidate["area_m2_polygon"],
            "area_m2_label": area_label,
            "label_inside_polygon": label_inside,
            "label_group_idx": chosen[0] if chosen is not None else None,
            "area_label_entity_index": (
                (label_group or {}).get("area_label") or {}
            ).get("entity_index"),
        })

        anchor_xy = (
            tuple(label_group["position_mm"]) if label_group is not None
            else tuple(centroid)
        )
        room = Room(
            anchor=RoomAnchor(
                name=name,
                area_m2=area_m2,
                floor="",
                number=str(candidate["entity_index"]),
                anchor_x_mm=anchor_xy[0],
                anchor_y_mm=anchor_xy[1],
            ),
            polygon_mm=poly,
            polygon_source=candidate["polygon_source"],
            doors=[d for d in doors if _is_on_polygon_edge(d.position_mm, poly, tol_mm=500.0)],
            windows=[w for w in windows if _is_on_polygon_edge(w.position_mm, poly, tol_mm=500.0)],
        )
        if label_group is None:
            room.review_flag = True
            room.review_reason = "closed polygon without room label"
        elif not label_inside:
            room.review_flag = True
            room.review_reason = "room label outside polygon"
        rooms.append(room)

    if diagnostics is not None:
        diagnostics["rooms"] = {
            "room_polygons": len(rooms),
            "room_labels": len(labels),
            "area_label_groups": len(area_label_groups),
            "polygons_with_label": sum(1 for room in rooms if room.anchor.name),
            "polygons_with_name": sum(1 for room in rooms if room.anchor.name),
            "polygons_with_area": sum(1 for room in rooms if room.anchor.area_m2 > 0),
            "polygons_with_area_delta_le_0_5_m2": sum(
                1 for delta in area_deltas if delta <= 0.5
            ),
            "area_label_groups_unused": max(0, len(area_label_groups) - len(used_groups)),
            "label_inside_polygon": label_inside_count,
            "area_delta_m2_median": (
                sorted(area_deltas)[len(area_deltas) // 2] if area_deltas else None
            ),
            "area_delta_m2_max": max(area_deltas) if area_deltas else None,
            "polygon_candidates": candidate_diag,
            "label_assignments": label_assignments,
        }
    return rooms


def _require_profile_strategy(
    profile: LayerProfile,
    role: str,
    allowed: set[str],
) -> str:
    strategy = profile.role_strategy(role)
    if strategy not in allowed:
        raise NotImplementedError(
            f"Layer profile {profile.profile_id!r}: role {role!r} "
            f"strategy {strategy!r} not implemented in this slice"
        )
    return strategy


def _extract_walls_for_profile(
    block: BlockLayout,
    scale_info: ScaleInfo,
    profile: LayerProfile,
    diagnostics: Optional[dict] = None,
) -> list[WallSegment]:
    strategy = _require_profile_strategy(
        profile, "walls", _PROFILE_STRATEGY_REGISTRY["walls"]
    )
    if strategy == "line_plus_hatch":
        return extract_walls_line_plus_hatch(
            block, scale_info, profile, diagnostics=diagnostics
        )
    return extract_walls(block, scale_info)


def _extract_hatches_for_profile(
    block: BlockLayout,
    scale_info: ScaleInfo,
    profile: LayerProfile,
) -> list[RoomHatch]:
    strategy = _require_profile_strategy(
        profile, "wall_material", _PROFILE_STRATEGY_REGISTRY["wall_material"]
    )
    if strategy == "disabled":
        return []
    return extract_room_hatches(block, scale_info)


def _annotate_walls_for_profile(
    walls: list[WallSegment],
    hatches: list[RoomHatch],
    profile: LayerProfile,
) -> None:
    strategy = _require_profile_strategy(
        profile, "wall_material", _PROFILE_STRATEGY_REGISTRY["wall_material"]
    )
    if strategy == "disabled":
        return
    annotate_walls_with_fil_material(walls, hatches)


def _extract_doors_for_profile(
    block: BlockLayout,
    doc,
    scale_info: ScaleInfo,
    profile: LayerProfile,
) -> list[Door]:
    strategy = _require_profile_strategy(
        profile, "doors", _PROFILE_STRATEGY_REGISTRY["doors"]
    )
    if strategy == "blocks_by_layer_pattern":
        return extract_doors_by_layer_pattern(block, doc, scale_info, profile)
    return extract_doors(block, doc, scale_info)


def _extract_windows_for_profile(
    block: BlockLayout,
    scale_info: ScaleInfo,
    profile: LayerProfile,
) -> list[Window]:
    strategy = _require_profile_strategy(
        profile, "windows", _PROFILE_STRATEGY_REGISTRY["windows"]
    )
    if strategy == "blocks_by_layer_pattern":
        return extract_windows_by_layer_pattern(block, scale_info, profile)
    return extract_windows(block, scale_info)


def _derive_anchor_raycast_rooms(
    anchors: list[RoomAnchor],
    hatches: list[RoomHatch],
    walls: list[WallSegment],
    doors: list[Door],
    windows: list[Window],
    bridges: list[WallSegment],
) -> list[Room]:
    rooms: list[Room] = []
    for a in anchors:
        diag: dict = {}
        poly, src = derive_room_polygon(a, hatches, walls, doors=doors,
                                        windows=windows, bridges=bridges,
                                        diag=diag)
        if poly:
            rd = [d for d in doors if _is_on_polygon_edge(d.position_mm, poly, tol_mm=500.0)]
            rw = [w for w in windows if _is_on_polygon_edge(w.position_mm, poly, tol_mm=500.0)]
        else:
            rd, rw = [], []
        r = Room(anchor=a, polygon_mm=poly, polygon_source=src,
                 doors=rd, windows=rw)
        if src == "anchor_only":
            r.review_flag = True
            if "reject_ratio" in diag:
                r.review_reason = (
                    f"polygon rejected oversize {diag['reject_ratio']:.2f}x")
            else:
                r.review_reason = "polygon detection failed"
        elif a.area_m2 > 0:
            ratio = _polygon_area_ratio(poly, a.area_m2)
            if ratio > 2.5 or ratio < 0.4:
                r.review_flag = True
                r.review_reason = f"polygon area off by {ratio:.2f}x"
        rooms.append(r)
    return rooms


def _extract_rooms_for_profile(
    block: BlockLayout,
    scale_info: ScaleInfo,
    anchors: list[RoomAnchor],
    hatches: list[RoomHatch],
    walls: list[WallSegment],
    doors: list[Door],
    windows: list[Window],
    bridges: list[WallSegment],
    profile: LayerProfile,
    diagnostics: Optional[dict] = None,
) -> list[Room]:
    strategy = _require_profile_strategy(
        profile, "rooms", _PROFILE_STRATEGY_REGISTRY["rooms"]
    )
    if strategy == "closed_polygons":
        rooms = extract_rooms_closed_polygons(
            block,
            scale_info,
            doors,
            windows,
            profile,
            diagnostics=diagnostics,
        )
        # Slice R1 (Hybrid, opt-in `anchor_fallback: text_groups`):
        # Regelgeschosse ohne explizite Raum-Polygone (Barawitzka: Stempel
        # Name+m², aber 815-Konturen offen) — Stempel, die von keinem
        # Polygon-Raum abgedeckt sind, werden Anker-Räume und laufen
        # downstream durch die Wand-Rekonstruktion (N4-Doktrin bleibt:
        # plan-explizites Polygon gewinnt, Fallback nur für den Rest).
        cfg = dict(profile.roles.get("rooms") or {})
        if str(cfg.get("anchor_fallback") or "") == "text_groups":
            text_anchors = extract_room_text_anchors(block, scale_info,
                                                     profile)
            # Gleiche Raum-Definition wie der Polygon-Pfad (N7): Stempel
            # unterhalb min_polygon_area_m2 sind KEINE Räume (Schacht-
            # Kästchen-Labels würden sonst als Anker wieder auftauchen).
            min_area = float(cfg.get("min_polygon_area_m2") or 0.0)
            polys = [r.polygon_mm for r in rooms
                     if r.polygon_mm and len(r.polygon_mm) >= 3]
            remaining = [
                a for a in text_anchors
                if a.area_m2 >= min_area
                and not any(_point_in_polygon(
                    (a.anchor_x_mm, a.anchor_y_mm), poly) for poly in polys)
            ]
            if remaining:
                rooms = rooms + _derive_anchor_raycast_rooms(
                    remaining, hatches, walls, doors, windows, bridges
                )
        return rooms
    return _derive_anchor_raycast_rooms(
        anchors, hatches, walls, doors, windows, bridges
    )


def _extract_furniture_for_profile(
    block: BlockLayout,
    scale_info: ScaleInfo,
    rooms: list[Room],
    walls: list[WallSegment],
    profile: LayerProfile,
    markers: Optional[list[ArchitectureMarker]] = None,
) -> list[Furniture]:
    _require_profile_strategy(
        profile, "furniture", _PROFILE_STRATEGY_REGISTRY["furniture"]
    )
    return extract_furniture(
        block, scale_info, rooms, walls, profile=profile, markers=markers
    )


def _extract_markers_for_profile(
    block: BlockLayout,
    scale_info: ScaleInfo,
    rooms: list[Room],
    walls: list[WallSegment],
    profile: LayerProfile,
) -> list[ArchitectureMarker]:
    if profile.roles.get("markers"):
        strategy = _require_profile_strategy(
            profile, "markers", _PROFILE_STRATEGY_REGISTRY["markers"]
        )
        if strategy == "disabled":
            return []
        return extract_markers(block, scale_info, rooms, walls, profile=profile)
    return extract_markers(block, scale_info, rooms, walls)


# ── Orchestrator ──────────────────────────────────────────────
# Slice 16.1.5.1: lru_cache lets multiple resolvers (door/wall/polygon) in
# the replay-pipeline share a single in-process parse. Three call-sites in
# replay/* now collapse to ONE actual ezdxf.readfile per process. Cache key
# is the Path argument; tests using different paths get separate entries.
@lru_cache(maxsize=4)
def parse_architecture(path: Path, profile_id: str = "mollgasse") -> ArchitectureModel:
    path = Path(path)
    profile = load_profile(profile_id)
    doc, block = load_architecture_for_profile(path, profile)
    # Slice 9.3.0: empirical scale detection. ScaleInfo is threaded
    # through every extractor so that mm-conversion is a single lookup
    # against the detected factor — no hardcoded M_TO_MM anywhere.
    scale_info = _detect_scale_for_profile(doc, profile)
    profile_diagnostics: dict = {"profile_id": profile.profile_id}
    tops = extract_top_boundaries(block, scale_info)
    anchors = extract_room_anchors(block, scale_info, profile)
    walls = _extract_walls_for_profile(
        block, scale_info, profile, diagnostics=profile_diagnostics
    )
    doors = _extract_doors_for_profile(block, doc, scale_info, profile)
    windows = _extract_windows_for_profile(block, scale_info, profile)
    hatches = _extract_hatches_for_profile(block, scale_info, profile)
    # Slice 18.36.0: additive FIL material/thickness annotation on the line
    # walls (ADR 0011 Linien-First). Counts-neutral — no split/filter.
    _annotate_walls_for_profile(walls, hatches, profile)
    # Slice B'-fragment-gap-closure: collinear-fragment bridges built once
    # (O(n^2) over walls) and shared across all room raycasts.
    bridges = _build_fragment_bridges(walls)

    rooms = _extract_rooms_for_profile(
        block, scale_info, anchors, hatches, walls, doors, windows, bridges,
        profile, diagnostics=profile_diagnostics
    )

    # Slice 16.1.6: floor-filtered nearest-anchor clustering replaces the
    # door-graph BFS (slice 9.1.2), which over-merged two physical units that
    # share a Stiegenhaus. Default target storey = modal FOK across tops[];
    # rooms whose nearest anchor is off-floor fall out (None top). Pass
    # target_fok to cluster a different storey for multi-floor batching.
    from parsers.apartment_clustering import cluster_apartments_floor_filtered

    # Slice 1.3.0: Bauteil-Zahl aus dem Profil — Bauteile können auf
    # verschiedenen FOK-Niveaus liegen, der Filter läuft dann pro Bauteil.
    bu_cfg = profile.building_units or {}
    n_bauteile = len(bu_cfg.get("bauteile") or []) or 1

    # Slice 1.4.0: Wohnflächen-Summen-Stempel des Architekten als
    # Ground-Truth für das Grenzraum-Refinement (Koordinaten → mm).
    area_stamps_mm: list = []
    area_blocks = set(bu_cfg.get("area_stamp_blocks") or [])
    if area_blocks:
        from types import SimpleNamespace

        from parsers.building_units import area_stamps_from_msp

        f_mm = scale_info.factor_to_mm or 1.0
        area_stamps_mm = [
            SimpleNamespace(top_ids=a.top_ids, area_m2=a.area_m2,
                            variant=a.variant,
                            x_mm=a.x * f_mm, y_mm=a.y * f_mm)
            for a in area_stamps_from_msp(
                block, "", area_blocks,
                str(bu_cfg.get("area_room_attrib") or "ROOM"),
                str(bu_cfg.get("area_attrib") or "AREA"))
        ]

    # Fallback (fremde Pläne ohne 00-top-Türschilder): manche Architekten/
    # Projekt-Dialekte (Selo/MVP) stempeln die Wohnungsnummer NUR in den
    # 01-SQM-Summenstempel ("Top 1"/"Top 2") statt in ein eigenes Türschild-
    # INSERT. Ohne Türschild bleibt ``tops`` leer → 0 Wohnungen → nichts
    # platziert. Dann die Summenstempel als TOP-Anker verwenden; trägt KEIN
    # Stempel eine "Top N"-Nummer (freistehendes Einzelhaus), ist die ganze
    # Zeichnung EINE Wohnung (Anker = Stempel-Zentroid). Greift NUR bei leerem
    # ``tops`` → Mollgasse (mit Türschildern) unberührt.
    if not tops and area_stamps_mm:
        numbered = [a for a in area_stamps_mm if getattr(a, "top_ids", None)]
        if numbered:
            tops = [
                TopBoundary(
                    top_id="+".join(str(i) for i in a.top_ids),
                    anchor_mm=(float(a.x_mm), float(a.y_mm)),
                )
                for a in numbered
            ]
        else:
            xs = [float(a.x_mm) for a in area_stamps_mm]
            ys = [float(a.y_mm) for a in area_stamps_mm]
            tops = [TopBoundary(top_id="1",
                                anchor_mm=(sum(xs) / len(xs), sum(ys) / len(ys)))]

    apartments = cluster_apartments_floor_filtered(
        rooms, tops, n_bauteile=n_bauteile,
        area_stamps=area_stamps_mm,
        outdoor_patterns=SPECIAL_SURFACE_ROOM_PATTERNS)

    rooms_by_id = {id(r): r for r in rooms}
    for apt in apartments:
        for rid in apt.room_ids:
            r = rooms_by_id.get(rid)
            if r:
                if apt.is_communal:
                    r.anchor.top = "COMMUNAL"
                else:
                    r.anchor.top = apt.estimated_top

    # Slice 9.2.6: link walls to their rooms for wall-snap placement.
    _assign_walls_to_rooms(rooms, walls)

    # Slice 18.72: PDF-Fachpraxis-Marker (07-SYM) before furniture so labels
    # can be attached to nearby inserts without changing the old fields.
    markers = _extract_markers_for_profile(
        block, scale_info, rooms, walls, profile
    )

    # Slice 11.10.0: möbel-extraction runs after apartment/top assignment
    # so that Furniture.apartment_id mirrors the rooms[].anchor.top
    # populated above.
    furniture = _extract_furniture_for_profile(
        block, scale_info, rooms, walls, profile, markers=markers
    )

    bbox_mm = _compute_bbox(walls)
    model = ArchitectureModel(
        tops=tops, rooms=rooms, walls=walls,
        bbox_mm=bbox_mm, scale=scale_info,
        apartments=apartments,
        source_path=str(path),
        all_doors=list(doors),
        all_windows=list(windows),
        furniture=furniture,
        markers=markers,
        profile_diagnostics=profile_diagnostics,
    )

    # Slice 1.16.0: wandgenaue Face-Polygone ersetzen die Raycast-Polygone,
    # wo fidelity=high (Anker in kleinster Face + Stempel-Ratio im Fenster).
    # Läuft NACH Clustering/Wall-Assign — deren Ergebnisse bleiben auf dem
    # bisherigen Stand; Konsumenten sehen die Provenance via polygon_source.
    from parsers.unit_faces import apply_face_polygons

    ff = apply_face_polygons(model, profile_id, block=block)
    profile_diagnostics["unit_faces"] = ff.stats
    return model
