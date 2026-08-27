"""Opening-aware logical wall bridge (Slice 18.24.20).

Production-facing helper: it keeps raw wall fragments available upstream, but
feeds resolvers with logical walls that bridge proven door/window openings and
carry forbidden ``opening_spans`` along the wall.
"""
from __future__ import annotations

import hashlib
import logging
import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Sequence

from engine.walls.door_opening import DoorOpening
from engine.walls.wall import OpeningSpan, Wall
from engine.walls.window_opening import WindowOpening

logger = logging.getLogger(__name__)

ANGLE_TOL_DEG = 2.0
LINE_OFFSET_TOL_MM = 80.0
OPENING_MARGIN_MM = 120.0
DEFAULT_OPENING_CLEARANCE_MM = 150.0
MIN_OPENING_OVERLAP_MM = 50.0
# Slice 18.26.0: an opening may only bridge a gap it actually FILLS. Without
# this the gap_overlap>=50mm test let a 1040mm door bridge a 22m gap between
# collinear fragments of different units' walls (26m monster logical walls →
# 14 symbols snapped onto a wall outside their room). Legit door/window bridges
# have gap<=opening_span; the cross-unit monsters had gap-opening>=13581mm. The
# 300mm headroom absorbs fragment-endpoint noise / wider reveals.
GAP_FILL_TOL_MM = 300.0
# Self-scaling sanity tripwire behind the gap-fill guard (warn-only, no crash):
# a logical bridge longer than its constituents + bridged openings + this margin
# is flagged for review.
BRIDGE_LEN_SANITY_MARGIN_MM = 500.0


@dataclass(frozen=True)
class BridgeStats:
    raw_walls: int
    logical_walls: int
    bridge_count: int
    bridged_source_walls: int
    opening_spans: int
    door_spans: int
    window_spans: int
    max_bridge_len_mm: float
    oversize_bridge_count: int

    def to_dict(self) -> dict:
        return {
            "raw_walls": self.raw_walls,
            "logical_walls": self.logical_walls,
            "bridge_count": self.bridge_count,
            "bridged_source_walls": self.bridged_source_walls,
            "opening_spans": self.opening_spans,
            "door_spans": self.door_spans,
            "window_spans": self.window_spans,
            "max_bridge_len_mm": self.max_bridge_len_mm,
            "oversize_bridge_count": self.oversize_bridge_count,
        }


@dataclass(frozen=True)
class _OpeningCandidate:
    opening_id: str
    kind: str
    center_xy: tuple[float, float]
    unit: tuple[float, float]
    span_min_abs: float
    span_max_abs: float
    clearance_mm: float


def _angle_delta(a: float, b: float) -> float:
    delta = abs((a - b) % 180.0)
    return min(delta, 180.0 - delta)


def _project(point: tuple[float, float], unit: tuple[float, float]) -> float:
    return point[0] * unit[0] + point[1] * unit[1]


def _line_offset(point: tuple[float, float], unit: tuple[float, float]) -> float:
    nx, ny = -unit[1], unit[0]
    return point[0] * nx + point[1] * ny


def _wall_span_abs(wall: Wall, unit: tuple[float, float]) -> tuple[float, float]:
    a = _project(wall.start_xy, unit)
    b = _project(wall.end_xy, unit)
    return (min(a, b), max(a, b))


def _wall_offset(wall: Wall, unit: tuple[float, float]) -> float:
    return (
        _line_offset(wall.start_xy, unit)
        + _line_offset(wall.end_xy, unit)
    ) / 2.0


def _overlap(a: tuple[float, float], b: tuple[float, float]) -> float:
    return max(0.0, min(a[1], b[1]) - max(a[0], b[0]))


def _midpoint(wall: Wall) -> tuple[float, float]:
    return (
        (wall.start_xy[0] + wall.end_xy[0]) / 2.0,
        (wall.start_xy[1] + wall.end_xy[1]) / 2.0,
    )


def _canonical_wall_unit(wall: Wall) -> tuple[float, float]:
    ux, uy = wall.unit_vector
    if ux < 0.0 or (abs(ux) < 1e-9 and uy < 0.0):
        return (-ux, -uy)
    return (ux, uy)


def _unit_from_angle(angle_deg: float) -> tuple[float, float]:
    rad = math.radians(angle_deg)
    ux, uy = math.cos(rad), math.sin(rad)
    if ux < 0.0 or (abs(ux) < 1e-9 and uy < 0.0):
        ux, uy = -ux, -uy
    return (ux, uy)


def _opening_from_door(
    door: DoorOpening,
    idx: int,
    *,
    clearance_mm: float,
) -> _OpeningCandidate | None:
    if not door.polygon_mm:
        return None
    center = (
        sum(p[0] for p in door.polygon_mm) / len(door.polygon_mm),
        sum(p[1] for p in door.polygon_mm) / len(door.polygon_mm),
    )
    if door.wall_unit_xy is not None:
        ux, uy = door.wall_unit_xy
        norm = math.hypot(ux, uy)
        if norm <= 1e-9:
            return None
        unit = (ux / norm, uy / norm)
        if unit[0] < 0.0 or (abs(unit[0]) < 1e-9 and unit[1] < 0.0):
            unit = (-unit[0], -unit[1])
    else:
        unit = _long_axis_unit(door.polygon_mm)
    projs = [_project(p, unit) for p in door.polygon_mm]
    return _OpeningCandidate(
        opening_id=door.door_id or f"door_{idx:04d}",
        kind="door",
        center_xy=center,
        unit=unit,
        span_min_abs=min(projs) - OPENING_MARGIN_MM,
        span_max_abs=max(projs) + OPENING_MARGIN_MM,
        clearance_mm=clearance_mm,
    )


def _opening_from_window(
    window: WindowOpening,
    idx: int,
    *,
    clearance_mm: float,
) -> _OpeningCandidate | None:
    if not window.polygon_mm:
        return None
    unit = _long_axis_unit(window.polygon_mm)
    center = (
        sum(p[0] for p in window.polygon_mm) / len(window.polygon_mm),
        sum(p[1] for p in window.polygon_mm) / len(window.polygon_mm),
    )
    projs = [_project(p, unit) for p in window.polygon_mm]
    return _OpeningCandidate(
        opening_id=window.window_id or f"window_{idx:04d}",
        kind="window",
        center_xy=center,
        unit=unit,
        span_min_abs=min(projs) - OPENING_MARGIN_MM,
        span_max_abs=max(projs) + OPENING_MARGIN_MM,
        clearance_mm=clearance_mm,
    )


def _long_axis_unit(
    polygon: Sequence[tuple[float, float]],
) -> tuple[float, float]:
    best_len = -1.0
    best = (1.0, 0.0)
    n = len(polygon)
    for i in range(n):
        x0, y0 = polygon[i]
        x1, y1 = polygon[(i + 1) % n]
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy)
        if length > best_len:
            best_len = length
            best = (dx / length, dy / length) if length > 1e-9 else best
    if best[0] < 0.0 or (abs(best[0]) < 1e-9 and best[1] < 0.0):
        best = (-best[0], -best[1])
    return best


class _UnionFind:
    def __init__(self, items: Iterable[str]):
        self.parent = {item: item for item in items}

    def find(self, item: str) -> str:
        parent = self.parent[item]
        if parent != item:
            self.parent[item] = self.find(parent)
        return self.parent[item]

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        self.parent[max(ra, rb)] = min(ra, rb)


def bridge_walls_across_openings(
    walls: Sequence[Wall],
    door_openings: Iterable[DoorOpening] = (),
    window_openings: Iterable[WindowOpening] = (),
    *,
    clearance_mm: float = DEFAULT_OPENING_CLEARANCE_MM,
) -> tuple[list[Wall], BridgeStats]:
    """Return logical walls with door/window openings bridged conservatively.

    A bridge is allowed only when a door/window opening overlaps the gap between
    two collinear fragments of the same wall type. Arbitrary collinear gaps are
    not merged.
    """
    walls = list(walls)
    by_id = {w.id: w for w in walls}
    uf = _UnionFind(by_id.keys())
    opening_by_pair: dict[tuple[str, str], list[_OpeningCandidate]] = defaultdict(list)

    openings: list[_OpeningCandidate] = []
    for idx, door in enumerate(door_openings):
        cand = _opening_from_door(door, idx, clearance_mm=clearance_mm)
        if cand is not None:
            openings.append(cand)
    for idx, window in enumerate(window_openings):
        cand = _opening_from_window(window, idx, clearance_mm=clearance_mm)
        if cand is not None:
            openings.append(cand)

    for opening in openings:
        candidates: list[tuple[float, Wall, tuple[float, float], float]] = []
        opening_angle = math.degrees(math.atan2(opening.unit[1], opening.unit[0]))
        opening_offset = _line_offset(opening.center_xy, opening.unit)
        for wall in walls:
            if _angle_delta(wall.angle_deg, opening_angle) > ANGLE_TOL_DEG:
                continue
            offset = _wall_offset(wall, opening.unit)
            if abs(offset - opening_offset) > LINE_OFFSET_TOL_MM:
                continue
            span = _wall_span_abs(wall, opening.unit)
            candidates.append((offset, wall, span, abs(offset - opening_offset)))

        best: tuple[float, Wall, Wall] | None = None
        for i, (_off_a, a, span_a, dist_a) in enumerate(candidates):
            for _off_b, b, span_b, dist_b in candidates[i + 1:]:
                if a.wall_type != b.wall_type:
                    continue
                if span_a[1] <= span_b[0]:
                    gap = (span_a[1], span_b[0])
                elif span_b[1] <= span_a[0]:
                    gap = (span_b[1], span_a[0])
                else:
                    continue
                opening_span = (opening.span_min_abs, opening.span_max_abs)
                gap_overlap = _overlap(gap, opening_span)
                if gap_overlap < MIN_OPENING_OVERLAP_MM:
                    continue
                # Gap-fill guard (Slice 18.26.0): the opening must actually FILL
                # the gap, not merely touch it. Reject pairs where the fragment
                # gap is wider than the opening it claims to bridge.
                if (gap[1] - gap[0]) - (opening_span[1] - opening_span[0]) > GAP_FILL_TOL_MM:
                    continue
                score = (
                    abs((gap[1] - gap[0]) - (opening_span[1] - opening_span[0]))
                    + dist_a
                    + dist_b
                    - gap_overlap
                )
                if best is None or score < best[0]:
                    best = (score, a, b)
        if best is None:
            continue
        _score, a, b = best
        uf.union(a.id, b.id)
        opening_by_pair[tuple(sorted((a.id, b.id)))].append(opening)

    groups: dict[str, list[Wall]] = defaultdict(list)
    for wall in walls:
        groups[uf.find(wall.id)].append(wall)

    pair_openings_by_root: dict[str, list[_OpeningCandidate]] = defaultdict(list)
    for pair, pair_openings in opening_by_pair.items():
        pair_openings_by_root[uf.find(pair[0])].extend(pair_openings)

    logical: list[Wall] = []
    max_bridge_len_mm = 0.0
    oversize_bridge_count = 0
    for root in sorted(groups):
        group = sorted(groups[root], key=lambda w: w.id)
        if len(group) == 1:
            logical.append(group[0])
            continue

        unit = _canonical_wall_unit(group[0])
        offset = sum(_wall_offset(w, unit) for w in group) / len(group)
        nx, ny = -unit[1], unit[0]
        spans = [_wall_span_abs(w, unit) for w in group]
        start_t = min(s[0] for s in spans)
        end_t = max(s[1] for s in spans)

        bridge_len = end_t - start_t
        root_openings = pair_openings_by_root.get(root, [])
        fragment_len = sum(s[1] - s[0] for s in spans)
        opening_len = sum(o.span_max_abs - o.span_min_abs for o in root_openings)
        sanity_cap = fragment_len + opening_len + BRIDGE_LEN_SANITY_MARGIN_MM
        max_bridge_len_mm = max(max_bridge_len_mm, bridge_len)
        if bridge_len > sanity_cap:
            oversize_bridge_count += 1
            logger.warning(
                "opening_bridge: oversize logical wall %.0fmm > cap %.0fmm "
                "(fragments=%d, openings=%d) source=%s",
                bridge_len,
                sanity_cap,
                len(group),
                len(root_openings),
                tuple(w.id for w in group),
            )
        source_ids = tuple(w.id for w in group)
        source_midpoints = tuple(_midpoint(w) for w in group)
        opening_spans = []
        for opening in pair_openings_by_root.get(root, []):
            start = max(0.0, opening.span_min_abs - start_t)
            end = min(end_t - start_t, opening.span_max_abs - start_t)
            if end - start <= MIN_OPENING_OVERLAP_MM:
                continue
            opening_spans.append(OpeningSpan(
                start_mm=start,
                end_mm=end,
                opening_id=opening.opening_id,
                kind=opening.kind,
                clearance_mm=opening.clearance_mm,
            ).normalized())
        opening_spans.sort(key=lambda s: (s.start_mm, s.end_mm, s.kind, s.opening_id))
        digest = hashlib.sha1("|".join(source_ids).encode("utf-8")).hexdigest()[:12]
        no_mount = all(w.no_mount for w in group)
        no_mount_source = ""
        if no_mount:
            no_mount_source = "|".join(
                sorted({w.no_mount_source for w in group if w.no_mount_source})
            )
        logical.append(Wall(
            id=f"wb_{digest}",
            start_xy=(unit[0] * start_t + nx * offset, unit[1] * start_t + ny * offset),
            end_xy=(unit[0] * end_t + nx * offset, unit[1] * end_t + ny * offset),
            wall_type=group[0].wall_type,
            room_id=group[0].room_id,
            opening_spans=tuple(opening_spans),
            source_wall_ids=source_ids,
            source_midpoints=source_midpoints,
            is_logical_bridge=True,
            no_mount=no_mount,
            no_mount_source=no_mount_source,
        ))

    source_bridged = {
        sid for wall in logical if wall.is_logical_bridge for sid in wall.source_wall_ids
    }
    door_spans = sum(
        1 for wall in logical for span in wall.opening_spans if span.kind == "door"
    )
    window_spans = sum(
        1 for wall in logical for span in wall.opening_spans if span.kind == "window"
    )
    stats = BridgeStats(
        raw_walls=len(walls),
        logical_walls=len(logical),
        bridge_count=sum(1 for wall in logical if wall.is_logical_bridge),
        bridged_source_walls=len(source_bridged),
        opening_spans=door_spans + window_spans,
        door_spans=door_spans,
        window_spans=window_spans,
        max_bridge_len_mm=max_bridge_len_mm,
        oversize_bridge_count=oversize_bridge_count,
    )
    return logical, stats


def logical_wall_by_source_id(walls: Sequence[Wall]) -> dict[str, Wall]:
    """Map raw wall ids to their logical replacement when one exists."""
    out: dict[str, Wall] = {}
    for wall in walls:
        if wall.is_logical_bridge:
            for source_id in wall.source_wall_ids:
                out[source_id] = wall
        else:
            out[wall.id] = wall
    return out


def opening_free_intervals(
    wall: Wall,
    *,
    corner_inset_mm: float,
    clearance_mm: float = DEFAULT_OPENING_CLEARANCE_MM,
    symbol_width_mm: float = 0.0,
) -> list[tuple[float, float]]:
    """Allowed distances along a wall after subtracting opening spans."""
    start = min(max(corner_inset_mm, 0.0), wall.length_mm)
    end = max(min(wall.length_mm - corner_inset_mm, wall.length_mm), start)
    allowed = [(start, end)]
    inflate = max(clearance_mm, 0.0) + max(symbol_width_mm, 0.0) / 2.0
    for raw in sorted(wall.opening_spans, key=lambda s: s.start_mm):
        span = raw.normalized()
        forbidden = (
            max(start, span.start_mm - inflate),
            min(end, span.end_mm + inflate),
        )
        if forbidden[1] <= forbidden[0]:
            continue
        next_allowed: list[tuple[float, float]] = []
        for a, b in allowed:
            if forbidden[1] <= a or b <= forbidden[0]:
                next_allowed.append((a, b))
                continue
            if a < forbidden[0]:
                next_allowed.append((a, forbidden[0]))
            if forbidden[1] < b:
                next_allowed.append((forbidden[1], b))
        allowed = next_allowed
    return [(a, b) for a, b in allowed if b - a > 1e-6]


def opening_free_length(
    wall: Wall,
    *,
    corner_inset_mm: float,
    clearance_mm: float = DEFAULT_OPENING_CLEARANCE_MM,
) -> float:
    return sum(
        b - a
        for a, b in opening_free_intervals(
            wall, corner_inset_mm=corner_inset_mm, clearance_mm=clearance_mm
        )
    )


def distribute_distance_avoiding_openings(
    wall: Wall,
    position_index: int,
    siblings_count: int,
    *,
    corner_inset_mm: float,
    clearance_mm: float = DEFAULT_OPENING_CLEARANCE_MM,
) -> float | None:
    """Map sibling index onto the usable, opening-free wall intervals."""
    intervals = opening_free_intervals(
        wall, corner_inset_mm=corner_inset_mm, clearance_mm=clearance_mm
    )
    total = sum(b - a for a, b in intervals)
    if total <= 1e-6:
        return None
    siblings_count = max(1, siblings_count)
    position_index = max(0, min(position_index, siblings_count - 1))
    t = 0.5 if siblings_count == 1 else (position_index + 0.5) / siblings_count
    target = t * total
    acc = 0.0
    for a, b in intervals:
        length = b - a
        if acc + length >= target:
            return a + (target - acc)
        acc += length
    return intervals[-1][1]


def nearest_distance_avoiding_openings(
    wall: Wall,
    desired_d_mm: float,
    *,
    direction: float = 1.0,
    corner_inset_mm: float,
    clearance_mm: float = DEFAULT_OPENING_CLEARANCE_MM,
) -> float | None:
    """Return nearest opening-free distance, preferring ``direction`` side."""
    intervals = opening_free_intervals(
        wall, corner_inset_mm=corner_inset_mm, clearance_mm=clearance_mm
    )
    if not intervals:
        return None
    for a, b in intervals:
        if a <= desired_d_mm <= b:
            return desired_d_mm
    preferred: list[float] = []
    fallback: list[float] = []
    for a, b in intervals:
        candidate = a if desired_d_mm < a else b
        if (candidate - desired_d_mm) * direction >= 0.0:
            preferred.append(candidate)
        else:
            fallback.append(candidate)
    pool = preferred or fallback
    return min(pool, key=lambda d: abs(d - desired_d_mm))
