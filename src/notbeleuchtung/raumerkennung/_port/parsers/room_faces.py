"""room_faces — extract closed room polygons from wall segments via planar
arrangement (Slice 18.3.1).

Walls are line segments; the rooms are the minimal faces of the planar graph they
form. Pipeline:
    snap endpoints → split segments at intersections → build undirected edges →
    half-edge traversal (turn clockwise at each node) → minimal faces → drop the
    outer face. Anchor→face matching is done by the caller via point-in-polygon.

Pure geometry, no ezdxf/DXF dependency. O(n²) intersection — fine for the ~1000
wall segments per floor. Robustness via grid-snapping (SNAP_MM).
"""
from __future__ import annotations

import math
from collections import defaultdict

SNAP_MM = 10.0          # merge endpoints/intersections within this grid
_EPS = 1e-6

Point = tuple[float, float]
Seg = tuple[Point, Point]


def _snap(p: Point) -> Point:
    return (round(p[0] / SNAP_MM) * SNAP_MM, round(p[1] / SNAP_MM) * SNAP_MM)


def _seg_intersection(a: Seg, b: Seg) -> Point | None:
    """Proper intersection point of two segments, or None. Endpoints touching
    count (so a T-junction splits the crossed segment)."""
    (x1, y1), (x2, y2) = a
    (x3, y3), (x4, y4) = b
    rx, ry = x2 - x1, y2 - y1
    sx, sy = x4 - x3, y4 - y3
    denom = rx * sy - ry * sx
    if abs(denom) < _EPS:
        return None  # parallel / collinear — handled by shared snapped endpoints
    t = ((x3 - x1) * sy - (y3 - y1) * sx) / denom
    u = ((x3 - x1) * ry - (y3 - y1) * rx) / denom
    if -_EPS <= t <= 1 + _EPS and -_EPS <= u <= 1 + _EPS:
        return (x1 + t * rx, y1 + t * ry)
    return None


def _split_segments(segs: list[Seg]) -> list[Seg]:
    """Split every segment at all intersection points with other segments.
    Endpoints are snapped to the grid so coincident nodes merge."""
    # collect split params per segment
    extra: list[list[Point]] = [[] for _ in segs]
    n = len(segs)
    for i in range(n):
        a = segs[i]
        for j in range(i + 1, n):
            p = _seg_intersection(a, segs[j])
            if p is not None:
                extra[i].append(p)
                extra[j].append(p)
    out: list[Seg] = []
    for idx, (p0, p1) in enumerate(segs):
        pts = [p0, p1] + extra[idx]
        pts = [_snap(p) for p in pts]
        # order along the segment
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        pts.sort(key=lambda q: (q[0] - p0[0]) * dx + (q[1] - p0[1]) * dy)
        for k in range(len(pts) - 1):
            if pts[k] != pts[k + 1]:
                out.append((pts[k], pts[k + 1]))
    return out


def _build_adjacency(segs: list[Seg]) -> dict[Point, list[Point]]:
    """Undirected node→neighbours (deduped)."""
    adj: dict[Point, set[Point]] = defaultdict(set)
    for p0, p1 in segs:
        if p0 == p1:
            continue
        adj[p0].add(p1)
        adj[p1].add(p0)
    return {k: sorted(v) for k, v in adj.items()}


def _faces(adj: dict[Point, list[Point]]) -> list[list[Point]]:
    """Minimal faces via half-edge traversal: from each directed edge, repeatedly
    take the most-clockwise next edge at the arrival node until the cycle closes."""
    visited: set[tuple[Point, Point]] = set()
    faces: list[list[Point]] = []
    for u in adj:
        for v in adj[u]:
            if (u, v) in visited:
                continue
            face = [u]
            cur_u, cur_v = u, v
            ok = True
            while True:
                visited.add((cur_u, cur_v))
                face.append(cur_v)
                # incoming direction at cur_v points from cur_u→cur_v
                back = math.atan2(cur_u[1] - cur_v[1], cur_u[0] - cur_v[0])
                best = None
                best_ang = None
                for w in adj[cur_v]:
                    if w == cur_u and len(adj[cur_v]) > 1:
                        continue  # avoid immediate U-turn unless dead end
                    ang = math.atan2(w[1] - cur_v[1], w[0] - cur_v[0])
                    # clockwise-most turn relative to the incoming edge
                    d = (back - ang) % (2 * math.pi)
                    if best_ang is None or d < best_ang:
                        best_ang, best = d, w
                if best is None:
                    ok = False
                    break
                cur_u, cur_v = cur_v, best
                if (cur_u, cur_v) == (u, v):
                    break
                if len(face) > len(adj) * 2 + 5:
                    ok = False
                    break
            if ok and len(face) >= 4 and face[0] == face[-1]:
                faces.append(face[:-1])
    return faces


def _poly_area_signed(poly: list[Point]) -> float:
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s / 2.0


def extract_room_faces(segments: list[Seg]) -> list[list[Point]]:
    """Closed room-face polygons from wall segments. The outer (largest, opposite-
    orientation) face is dropped. Returns CCW polygons."""
    if not segments:
        return []
    segs = _split_segments(segments)
    adj = _build_adjacency(segs)
    faces = _faces(adj)
    if not faces:
        return []
    # drop the outer face: the one with the largest |area| and the sign opposite
    # to the majority (interior faces share one orientation in half-edge traversal).
    areas = [_poly_area_signed(f) for f in faces]
    max_abs = max(range(len(faces)), key=lambda i: abs(areas[i]))
    outer_sign = 1 if areas[max_abs] > 0 else -1
    out = []
    for f, a in zip(faces, areas):
        if abs(a) < SNAP_MM * SNAP_MM:  # degenerate sliver
            continue
        sign = 1 if a > 0 else -1
        if sign == outer_sign and abs(a) == abs(areas[max_abs]):
            continue  # the outer face itself
        # normalise to CCW
        out.append(f if a > 0 else f[::-1])
    return out
