"""geometry.py — geometrische Primitive für die Platzierung (Fachpraxis-Methode).

Portiert aus elektro-planer `backend/engine/placement_geometry.py` (siehe
docs/PORT_LOG.md). Reine Geometrie — Punkte/Polygone rein, Punkte raus. KEINE
Contract-/Render-/Pipeline-Kopplung: Möbel-Polygone, Sperrflächen etc. werden als
Argumente übergeben. So sind alle Primitive hermetisch mit synthetischen Eingaben
testbar und der Platzierer bleibt vom Rendern entkoppelt (Import-Grenze Slice 2).
"""
from __future__ import annotations

import math

Point = tuple[float, float]
Polygon = list[Point]


def _bbox(points: list[Point]) -> tuple[float, float, float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)


def _bbox_area(bbox: tuple[float, float, float, float]) -> float:
    return max(0.0, bbox[2] - bbox[0]) * max(0.0, bbox[3] - bbox[1])


def _clamp(value: float, lo: float, hi: float) -> float:
    if lo > hi:
        return (lo + hi) / 2.0
    return max(lo, min(hi, value))


def _on_segment(p: Point, a: Point, b: Point, eps: float = 1e-6) -> bool:
    cross = (p[1] - a[1]) * (b[0] - a[0]) - (p[0] - a[0]) * (b[1] - a[1])
    if abs(cross) > eps:
        return False
    dot = (p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])
    if dot < -eps:
        return False
    sq_len = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    return dot <= sq_len + eps


def point_in_polygon(point: Point, polygon: Polygon) -> bool:
    """Ray-casting point-in-polygon test; boundary counts as inside."""
    if len(polygon) < 3:
        return False
    x, y = point
    inside = False
    j = len(polygon) - 1
    for i, pi in enumerate(polygon):
        pj = polygon[j]
        # Null-Kanten überspringen — Arch-Polygone tragen den Schluss-Vertex
        # DOPPELT; für die degenerierte Kante (a == b) ist cross=dot=sq_len=0 und
        # _on_segment meldete JEDEN Punkt als "auf der Kante" → point_in_polygon
        # war für solche Polygone konstant True (Raum-Guards No-Op).
        if pj == pi:
            j = i
            continue
        if _on_segment(point, pj, pi):
            return True
        xi, yi = pi
        xj, yj = pj
        crosses = (yi > y) != (yj > y)
        if crosses:
            x_intersect = (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi
            if x_intersect >= x:
                inside = not inside
        j = i
    return inside


def _dist(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _bbox_contains_point(
    bbox: tuple[float, float, float, float],
    point: Point,
    eps: float = 1e-6,
) -> bool:
    return (
        bbox[0] - eps <= point[0] <= bbox[2] + eps
        and bbox[1] - eps <= point[1] <= bbox[3] + eps
    )


def _bbox_overlaps(
    a: tuple[float, float, float, float],
    b: tuple[float, float, float, float],
    eps: float = 1e-6,
) -> bool:
    return not (
        a[2] <= b[0] + eps
        or b[2] <= a[0] + eps
        or a[3] <= b[1] + eps
        or b[3] <= a[1] + eps
    )


def _normalise_exclusions(
    room_polygon: Polygon,
    exclusion_polygons: list[Polygon],
) -> list[Polygon]:
    if len(room_polygon) < 3:
        return []
    room_bbox = _bbox(room_polygon)
    result: list[Polygon] = []
    for poly in exclusion_polygons:
        if len(poly) < 3:
            continue
        bbox = _bbox(poly)
        if _bbox_area(bbox) <= 0.0:
            continue
        if _bbox_overlaps(room_bbox, bbox):
            result.append(poly)
    return result


def _inside_any_exclusion(point: Point, exclusions: list[Polygon]) -> bool:
    return any(point_in_polygon(point, poly) for poly in exclusions)


def _mountable(
    point: Point,
    room_polygon: Polygon,
    exclusions: list[Polygon],
) -> bool:
    return point_in_polygon(point, room_polygon) and not _inside_any_exclusion(point, exclusions)


def _relocate_outside_exclusions(
    point: Point,
    room_polygon: Polygon,
    exclusions: list[Polygon],
    *,
    existing: list[Point],
    clearance_mm: float = 150.0,
) -> Point:
    """Move a planned point out of no-mount polygons while staying near it."""
    if _mountable(point, room_polygon, exclusions):
        return point

    minx, miny, maxx, maxy = _bbox(room_polygon)
    margin = min(clearance_mm, max((maxx - minx) * 0.05, 0.0), max((maxy - miny) * 0.05, 0.0))
    lo_x, hi_x = minx + margin, maxx - margin
    lo_y, hi_y = miny + margin, maxy - margin

    candidates: list[Point] = []
    for poly in exclusions:
        eb = _bbox(poly)
        if not _bbox_contains_point(eb, point):
            continue
        left = eb[0] - clearance_mm
        right = eb[2] + clearance_mm
        below = eb[1] - clearance_mm
        above = eb[3] + clearance_mm
        candidates.extend([
            (left, point[1]),
            (right, point[1]),
            (point[0], below),
            (point[0], above),
            (left, below),
            (left, above),
            (right, below),
            (right, above),
        ])

    # Robust fallback for unusual shaft shapes: sample a small room grid.
    for xf in (0.20, 0.35, 0.50, 0.65, 0.80):
        for yf in (0.20, 0.35, 0.50, 0.65, 0.80):
            candidates.append((minx + (maxx - minx) * xf, miny + (maxy - miny) * yf))

    valid: list[Point] = []
    for cx, cy in candidates:
        candidate = (_clamp(cx, lo_x, hi_x), _clamp(cy, lo_y, hi_y))
        if _mountable(candidate, room_polygon, exclusions):
            valid.append(candidate)

    if not valid:
        # Last resort: keep the old point. The caller flags the placement so the
        # diagnostic output remains reviewable instead of silently disappearing.
        return point

    def score(candidate: Point) -> tuple[float, float]:
        nearest_existing = min((_dist(candidate, p) for p in existing), default=10_000.0)
        return (_dist(candidate, point), -nearest_existing)

    return min(valid, key=score)


def find_center_diagonal(polygon: Polygon) -> Point:
    """Raum-Mitte = Mittelpunkt der Ecke→Ecke-Diagonale.

    Für rechteckige Räume identisch mit der Bbox-Mitte; das ist die robuste
    Interpretation der „Linie von einer Ecke zur anderen, Mitte nehmen"-Methode.
    """
    if not polygon:
        raise ValueError("empty polygon")
    minx, miny, maxx, maxy = _bbox(polygon)
    return ((minx + maxx) / 2.0, (miny + maxy) / 2.0)


def find_center_visual(polygon: Polygon) -> Point:
    """Raum-Mitte für UNREGELMÄSSIGE Polygone: pole of inaccessibility
    (tiefster Innenpunkt, shapely polylabel).

    Die Bbox-Mitte kippt bei L-förmigen Räumen in die Nische; polylabel bleibt
    innen. Für rechteckige Räume ist polylabel ≈ Bbox-Mitte → abwärtskompatibel.
    Fallback (kein shapely / degeneriert): Bbox-Mitte.
    """
    if not polygon:
        raise ValueError("empty polygon")
    try:
        from shapely.geometry import Polygon as _SPoly
        from shapely.ops import polylabel as _polylabel
    except ImportError:
        return find_center_diagonal(polygon)
    sp = _SPoly(polygon)
    if not (sp.is_valid and sp.area > 0):
        return find_center_diagonal(polygon)
    minx, miny, maxx, maxy = _bbox(polygon)
    bbox_area = (maxx - minx) * (maxy - miny)
    # Nahezu rechteckig → Bbox-Mitte ist die exakte Methode. Nur bei echter
    # L-Form (Flächen-Ratio < 0.9) übernimmt polylabel.
    if bbox_area > 0 and sp.area / bbox_area >= 0.9:
        return find_center_diagonal(polygon)
    p = _polylabel(sp, tolerance=10.0)
    return (float(p.x), float(p.y))


def room_main_axis(polygon: Polygon) -> str:
    """Raum-Hauptachse: 'horizontal' wenn Breite ≥ Höhe, sonst 'vertical'."""
    minx, miny, maxx, maxy = _bbox(polygon)
    return "horizontal" if (maxx - minx) >= (maxy - miny) else "vertical"


def offset_point(center: Point, axis: str, dist_mm: float, positive: bool = True) -> Point:
    """Verschiebe einen Punkt um dist_mm entlang der Hauptachse."""
    s = dist_mm if positive else -dist_mm
    if axis == "horizontal":
        return (center[0] + s, center[1])
    return (center[0], center[1] + s)


def subdivide_halves_along_axis(polygon: Polygon, axis: str | None = None) -> list[Point]:
    """Raum entlang der Hauptachse halbieren, je Hälften-Mitte zurückgeben.
    Liefert die zwei Viertel-Punkte (Mitten der beiden Hälften)."""
    minx, miny, maxx, maxy = _bbox(polygon)
    if axis is None:
        axis = room_main_axis(polygon)
    cx = (minx + maxx) / 2.0
    cy = (miny + maxy) / 2.0
    if axis == "horizontal":
        q1 = minx + (maxx - minx) * 0.25
        q3 = minx + (maxx - minx) * 0.75
        return [(q1, cy), (q3, cy)]
    q1 = miny + (maxy - miny) * 0.25
    q3 = miny + (maxy - miny) * 0.75
    return [(cx, q1), (cx, q3)]
