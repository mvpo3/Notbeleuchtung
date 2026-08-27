"""room_partition — assign a point to its room by nearest label-anchor with a
wall-blocked line of sight (Slice 18.3.2).

Wall-based room polygons fail on open floor plans (an open kitchen-living has no
closed wall loop), so point-in-polygon leaves >40% of furniture unassigned. The
robust model: every point belongs to the nearest *room label* (anchor) it can
"see" without crossing a wall. This is a geodesic/visibility Voronoi of the
anchors and it partitions open spaces correctly (kitchen items → kitchen label,
sofa → living label) while a doorway-separated neighbour is cut off by its wall.

Pure geometry. assign_room tries point-in-polygon first (reliable when the
polygon is good), then nearest-visible-anchor, then plain nearest.
"""
from __future__ import annotations

import math

Point = tuple[float, float]
_EPS = 1e-9


def _point_in_polygon(pt: Point, poly: list[Point]) -> bool:
    x, y = pt
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xin = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < xin:
                inside = not inside
    return inside


def _ccw(a: Point, b: Point, c: Point) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _segments_cross(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
    """True if segment p1p2 properly straddles segment p3p4 (shared endpoints or
    collinear touching do NOT count as crossing — a sight-line grazing a wall end
    still sees past it)."""
    d1 = _ccw(p3, p4, p1)
    d2 = _ccw(p3, p4, p2)
    d3 = _ccw(p1, p2, p3)
    d4 = _ccw(p1, p2, p4)
    return ((d1 > _EPS and d2 < -_EPS) or (d1 < -_EPS and d2 > _EPS)) and \
           ((d3 > _EPS and d4 < -_EPS) or (d3 < -_EPS and d4 > _EPS))


def clear_line_of_sight(p: Point, q: Point, wall_segs: list[tuple[Point, Point]]) -> bool:
    """True if the segment p→q crosses no wall."""
    for a, b in wall_segs:
        if _segments_cross(p, q, a, b):
            return False
    return True


def assign_room(
    point: Point,
    rooms,
    wall_segs: list[tuple[Point, Point]],
    *,
    max_los_anchors: int = 8,
) -> int | None:
    """Index of the room ``point`` belongs to, or None if there are no rooms.

    1) point-in-polygon over rooms with a usable polygon (reliable case),
    2) else the nearest anchor with a wall-clear line of sight,
    3) else the plain nearest anchor (degenerate: every sight-line blocked).
    """
    if not rooms:
        return None
    # 1) containment
    for idx, r in enumerate(rooms):
        poly = getattr(r, "polygon_mm", None)
        if poly and len(poly) >= 3 and _point_in_polygon(point, poly):
            return idx
    # rank anchors by distance
    def _anchor(r) -> Point:
        a = r.anchor
        return (a.anchor_x_mm, a.anchor_y_mm)

    order = sorted(
        range(len(rooms)),
        key=lambda i: math.hypot(point[0] - _anchor(rooms[i])[0],
                                 point[1] - _anchor(rooms[i])[1]),
    )
    # 2) nearest visible
    for i in order[:max_los_anchors]:
        if clear_line_of_sight(point, _anchor(rooms[i]), wall_segs):
            return i
    # 3) plain nearest
    return order[0]
