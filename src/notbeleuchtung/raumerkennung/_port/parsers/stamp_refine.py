"""stamp_refine — Stempel-geführte Loop-Suche (Slice N1).

Interpretiert die Zeichner-Methodik (docs/MARKER_METHODIK_KG.md) als ZIEL
statt als Geometrie: der Zeichner zieht Marker-Loops, DAMIT jeder Raum-
Stempel ein Face bekommt, dessen Fläche zum Stempel passt. Genau dieses
Ziel wird hier direkt gesucht — projekt-agnostisch, weil Raumstempel +
Wandgeometrie in jedem KG-Plan vorhanden sind (keine Marker-Blöcke nötig).

Pro coarse-Raum zwei Suchrichtungen:

  Face zu GROSS (Ratio > Band) — der Raum ist mit Nachbarn verschmolzen,
      weil Trennkanten fehlen. Kandidaten sind NUR vorhandene Plan-Kanten
      im Face (R1: nachziehen, nicht erfinden) — erst Wand-/HID-Layer,
      dann alle Nicht-Annotations-Layer — plus kurze End-Verbinder für
      offene Stichwände (R2/R3: Türen/Lücken überzeichnen). Akzeptiert
      wird NUR die Zerteilung, deren Anker-Subface das Ratio-Band trifft
      → Sliver-sicher by construction, der Stempel selbst validiert.

  Face zu KLEIN (Ratio < Band) — eine Fehlkante zerschneidet den Raum.
      Anker-lose Nachbar-Faces (Artefakte ohne Stempel) werden gierig
      vereinigt, bis das Band getroffen ist; Faces mit fremdem Stempel-
      Anker sind tabu.

Kein Treffer → Raum bleibt unverändert coarse (fail-safe, kein Raten).
"""
from __future__ import annotations

import math
from typing import Any

from shapely.geometry import LineString, Point, Polygon
from shapely.ops import nearest_points, polygonize, unary_union
from shapely.strtree import STRtree

from parsers.keller_geometry import (
    _RATIO_HIGH,
    _arc_to_segments,
    _polyline_segments,
    inner_offset,
    is_wall_layer,
    snap_segments,
)

Seg = tuple[tuple[float, float], tuple[float, float]]

# End-Verbinder: freies Stichwand-Ende → nächste Kante. 1500 mm deckt
# Türbreiten (R3) und Aufzugs-/Schachtöffnungen; das Ratio-Band verhindert
# Fehlschlüsse durch zu lange Verbinder.
CONNECT_MAX_MM = 1500.0
NODE_TOL_MM = 50.0          # Endpunkt-Raster für Degree-Bestimmung (wie Slice B/H)
MIN_PIECE_MM = 30.0         # kürzere Clip-Reste sind Rauschen
MIN_STAMP_M2 = 1.0          # kleinere/fehlende Stempel sind nicht suchbar
MAX_LOCAL_EDGES = 1000      # Kandidaten-Deckel pro Tier (Garage-Riesenfaces)
MAX_MERGE_STEPS = 8

# Layer, deren zweites Namensfeld Annotation statt Bau-Geometrie trägt —
# nie als Raumgrenze anbieten (Bemaßung/Beschriftung/Schraffur/Raster).
_ANNOTATION_TOKENS = ("BEM", "TEXT", "TXT", "DIM", "MASS", "SCHRAFF",
                      "RAST", "PLOT")


def _is_hid_layer(layer: str) -> bool:
    parts = str(layer or "").split("-")
    return len(parts) > 1 and parts[1].upper() == "HID"


def _is_annotation_layer(layer: str) -> bool:
    up = str(layer or "").upper()
    return any(tok in up for tok in _ANNOTATION_TOKENS)


def collect_all_segments(doc, factor_to_mm: float) -> list[tuple[Seg, str]]:
    """Alle Linien-Kanten des Modelspace (beliebige Layer) in mm, mit Layer."""
    f = float(factor_to_mm)
    out: list[tuple[Seg, str]] = []
    for e in doc.modelspace():
        lay = str(e.dxf.layer or "")
        t = e.dxftype()
        if t == "LINE":
            a = (e.dxf.start.x * f, e.dxf.start.y * f)
            b = (e.dxf.end.x * f, e.dxf.end.y * f)
            if a != b:
                out.append(((a, b), lay))
        elif t == "LWPOLYLINE":
            pts = [(p[0] * f, p[1] * f) for p in e.get_points()]
            out.extend((s, lay) for s in _polyline_segments(pts, bool(e.closed)))
        elif t == "POLYLINE":
            try:
                pts = [(v.dxf.location.x * f, v.dxf.location.y * f)
                       for v in e.vertices]
            except Exception:
                continue
            out.extend((s, lay) for s in _polyline_segments(
                pts, bool(getattr(e, "is_closed", False))))
        elif t == "ARC":
            out.extend((s, lay) for s in _arc_to_segments(
                e.dxf.center.x, e.dxf.center.y, e.dxf.radius,
                float(e.dxf.start_angle), float(e.dxf.end_angle), f))
    return out


def _clip_into_face(face: Polygon, ls: LineString) -> list[Seg]:
    """Segment auf das Face-Innere clippen → Teilstücke > MIN_PIECE_MM."""
    inter = ls.intersection(face)
    if inter.is_empty:
        return []
    parts = getattr(inter, "geoms", [inter])
    out: list[Seg] = []
    for g in parts:
        if g.geom_type != "LineString" or g.length <= MIN_PIECE_MM:
            continue
        coords = list(g.coords)
        out.extend((coords[i], coords[i + 1]) for i in range(len(coords) - 1)
                   if coords[i] != coords[i + 1])
    return out


def _connectors(pieces: list[Seg], boundary: LineString) -> list[Seg]:
    """Offene Stichwand-Enden auf die nächste Kante verbinden (R2/R3)."""
    if not pieces:
        return []

    def key(p):
        return (round(p[0] / NODE_TOL_MM), round(p[1] / NODE_TOL_MM))

    degree: dict[tuple[int, int], int] = {}
    for a, b in pieces:
        for p in (a, b):
            degree[key(p)] = degree.get(key(p), 0) + 1

    targets = [boundary] + [LineString([a, b]) for a, b in pieces]
    tree = STRtree(targets)
    out: list[Seg] = []
    seen: set[tuple[int, int]] = set()
    for i, (a, b) in enumerate(pieces):
        for p in (a, b):
            k = key(p)
            if degree[k] != 1 or k in seen:
                continue
            seen.add(k)
            pt = Point(p)
            best: tuple[float, tuple[float, float]] | None = None
            for j in tree.query(pt.buffer(CONNECT_MAX_MM)):
                if targets[j].geom_type == "LineString" and j == i + 1:
                    continue  # eigenes Segment
                q = nearest_points(pt, targets[j])[1]
                d = pt.distance(q)
                if d < NODE_TOL_MM or d > CONNECT_MAX_MM:
                    continue
                if best is None or d < best[0]:
                    best = (d, (q.x, q.y))
            if best is not None:
                out.append((p, best[1]))
    return out


def _clear_parts(poly: Polygon, offset_mm: float
                 ) -> tuple[Polygon | None, float]:
    """(größtes Teil-Polygon, GESAMT-Lichtfläche mm²) nach Innen-Offset.

    Anders als ``inner_offset`` geht bei Zerfall (schmale Gänge reißen an
    Tür-Engstellen) die Fläche der kleineren Teile NICHT verloren — der
    Stempel bemisst den ganzen Gang, nicht sein größtes Fragment.
    """
    if offset_mm <= 0:
        return poly, poly.area
    shrunk = poly.buffer(-offset_mm, join_style=2)
    if shrunk.is_empty:
        return None, 0.0
    parts = list(shrunk.geoms) if shrunk.geom_type == "MultiPolygon" else [shrunk]
    return max(parts, key=lambda g: g.area), sum(g.area for g in parts)


def _ratio(poly: Polygon, lab_m2: float, offset_mm: float) -> float | None:
    _, area = _clear_parts(poly, offset_mm)
    if area <= 0:
        return None
    return (area / 1e6) / lab_m2 if lab_m2 > 0 else None


MIN_SHARED_MM = 100.0       # kürzere Zell-Berührung ist keine echte Nachbarschaft
WALL_NEAR_MM = 40.0         # Kante gilt als Wand, wenn so nah an Wand-Layer-Geometrie
MAX_GROW_STEPS = 60         # tier1-Zellen sind fein (Stufen) → viele kleine Schritte


def _wall_fraction(shared, wall_tree: STRtree | None,
                   wall_lines: list[LineString]) -> float:
    """Anteil einer geteilten Zell-Kante, der auf Wand-Layer-Geometrie liegt."""
    if wall_tree is None or shared.length <= 0:
        return 0.0
    n = max(2, int(shared.length // 200) + 1)
    hits = 0
    for i in range(n + 1):
        p = shared.interpolate(i / n, normalized=True)
        idx = wall_tree.query(p.buffer(WALL_NEAR_MM))
        if any(wall_lines[j].distance(p) <= WALL_NEAR_MM for j in idx):
            hits += 1
    return hits / (n + 1)


def _cell_search(face: Polygon, anchor: Point, lab_m2: float,
                 local: list[tuple[Seg, str]], offset_mm: float,
                 vocab=None) -> Polygon | None:
    """Zell-Wachstum: Face in atomare Zellen zerlegen, ab der Anker-Zelle
    über NICHT-Wand-Kanten wachsen, bis die Stempel-Fläche passt.

    Das ist die Zeichner-Methodik als Suche: sein Loop umschließt eine
    Vereinigung vorhandener Plan-Zellen; Wände sind Raumgrenzen (nie
    queren), Stufen-/HID-/Symbol-Kanten sind Innenleben (queren erlaubt),
    und der Stempel entscheidet, wann der Loop komplett ist.
    """
    _is_wall = vocab.is_wall if vocab is not None else is_wall_layer
    _is_hid = vocab.is_hid if vocab is not None else _is_hid_layer
    lo, hi = _RATIO_HIGH
    tiers: list[list[Seg]] = [[], []]
    for seg, lay in local:
        if _is_annotation_layer(lay):
            continue
        pieces = _clip_into_face(face, LineString(seg))
        if _is_wall(lay) or _is_hid(lay):
            tiers[0].extend(pieces)
        tiers[1].extend(pieces)
    wall_lines = [LineString(s) for s, lay in local if _is_wall(lay)]
    wall_tree = STRtree(wall_lines) if wall_lines else None

    ext = list(face.exterior.coords)
    ext_segs: list[Seg] = [(ext[i], ext[i + 1]) for i in range(len(ext) - 1)
                           if ext[i] != ext[i + 1]]
    for tier in (tiers[0], tiers[1]):
        if not tier or len(tier) > MAX_LOCAL_EDGES:
            continue
        pieces = tier + _connectors(tier, face.exterior)
        snapped = snap_segments(ext_segs + pieces, NODE_TOL_MM)
        lines = [LineString([a, b]) for a, b in snapped]
        cells = list(polygonize(unary_union(lines)))
        seeds = [c for c in cells if c.contains(anchor)]
        if not seeds:
            continue
        region = min(seeds, key=lambda g: g.area)
        in_region = {id(region)}
        max_area = hi * lab_m2 * 1e6   # harte Obergrenze fürs Roh-Wachstum
        for _ in range(MAX_GROW_STEPS):
            r = _ratio(region, lab_m2, offset_mm)
            if r is not None and lo <= r <= hi:
                return region
            if r is None or r > hi:
                break  # Anker-Zelle/Region schon zu groß → nächster Tier
            best: tuple[float, Polygon] | None = None
            for c in cells:
                if id(c) in in_region:
                    continue
                # Kandidat, der übers Band hinausschösse, wird übersprungen —
                # Greedy darf nicht die größte, sondern nur eine PASSENDE
                # Nachbar-Zelle nehmen (PODEST-Befund: +12 m² auf 4.5er-Stempel).
                if region.area + c.area > max_area:
                    continue
                shared = region.exterior.intersection(c.exterior)
                if shared.is_empty or shared.length < MIN_SHARED_MM:
                    continue
                wf = _wall_fraction(shared, wall_tree, wall_lines)
                if wf > 0.5:
                    continue  # Wand dazwischen → anderer Raum
                score = shared.length * (1.0 - wf)
                if best is None or score > best[0]:
                    best = (score, c)
            if best is None:
                break  # nur noch Wände/zu große Zellen → kein Treffer hier
            merged = unary_union([region, best[1]])
            if merged.geom_type != "Polygon":
                break
            in_region.add(id(best[1]))
            region = merged
    return None


def _merge_search(face: Polygon, anchor: Point, lab_m2: float,
                  all_faces: list[Polygon], blocked: list[Point],
                  offset_mm: float) -> Polygon | None:
    """Anker-lose Nachbar-Faces ketten-vereinigen bis das Ratio-Band passt.

    Erst-Check: passt schon das ROHE Face (Summen-Lichtfläche)? Dann war
    nur der Offset-Zerfall das Problem (schmale Gänge). Sonst wird pro
    Schritt der Nachbar mit der längsten Berührung angefügt — Nachbarn
    mit fremdem Stempel-Anker oder Band-Überschuss sind tabu; die
    Kandidaten werden je Schritt NEU gesucht (Gang-Ketten wachsen weiter).
    """
    lo, hi = _RATIO_HIGH
    cur = face
    r = _ratio(cur, lab_m2, offset_mm)
    if r is not None and lo <= r <= hi:
        return cur
    max_area = hi * lab_m2 * 1e6
    used = {id(face)}
    for _ in range(MAX_MERGE_STEPS):
        best: tuple[float, Polygon] | None = None
        for g in all_faces:
            if id(g) in used or g.distance(cur) > NODE_TOL_MM * 1.5:
                continue
            if cur.area + g.area > max_area:
                continue
            if any(g.contains(p) for p in blocked):
                continue
            shared = g.buffer(NODE_TOL_MM * 1.5).intersection(cur.boundary).length
            if shared < MIN_SHARED_MM:
                continue
            if best is None or shared > best[0]:
                best = (shared, g)
        if best is None:
            return None
        merged = unary_union([cur, best[1]])
        if merged.geom_type != "Polygon":
            used.add(id(best[1]))
            continue
        used.add(id(best[1]))
        cur = merged
        r = _ratio(cur, lab_m2, offset_mm)
        if r is not None and lo <= r <= hi:
            return cur
    return None


def refine_rooms(rooms: list, room_faces: list, all_faces: list[Polygon],
                 doc, factor_to_mm: float, offset_mm: float,
                 vocab=None) -> dict[str, Any]:
    """Stempel-geführte Nachbesserung aller coarse-Räume (mutiert ``rooms``).

    ``room_faces`` = pro Raum das gematchte Roh-Face (vor Innen-Offset) oder
    None. ``vocab`` (Slice N3) = projekt-spezifisches Layer-Vokabular,
    ``None`` = Mollgasse-Default. Rückgabe: Zähler für die Summary.
    """
    lo, hi = _RATIO_HIGH
    stats = {"attempted": 0, "refined": 0, "split": 0, "merged": 0}
    if not any(r.fidelity == "coarse" for r in rooms):
        return stats
    local_all = collect_all_segments(doc, factor_to_mm)
    lines = [LineString(s) for s, _ in local_all]
    tree = STRtree(lines)
    anchors = [Point(r.anchor_xy) for r in rooms if r.fidelity != "zone"]

    for i, room in enumerate(rooms):
        face = room_faces[i]
        if (room.fidelity != "coarse" or face is None
                or room.label_area_m2 < MIN_STAMP_M2
                or room.area_ratio is None):
            continue
        stats["attempted"] += 1
        anchor = Point(room.anchor_xy)
        result: Polygon | None = None
        kind = None
        if room.area_ratio > hi:
            idx = tree.query(face)
            local = [local_all[j] for j in idx if lines[j].intersects(face)]
            result = _cell_search(face, anchor, room.label_area_m2,
                                  local, offset_mm, vocab=vocab)
            kind = "split"
        elif room.area_ratio < lo:
            blocked = [p for p in anchors
                       if (p.x, p.y) != tuple(room.anchor_xy)]
            result = _merge_search(face, anchor, room.label_area_m2,
                                   all_faces, blocked, offset_mm)
            kind = "merged"
        if result is None:
            continue
        largest, total_area = _clear_parts(result, offset_mm)
        if largest is None or total_area <= 0:
            continue
        room.polygon_mm = [(x, y) for x, y in largest.exterior.coords]
        room.polygon_area_m2 = total_area / 1e6
        room.area_ratio = room.polygon_area_m2 / room.label_area_m2
        room.fidelity = "high"
        room.refined = True
        stats["refined"] += 1
        stats[kind] += 1
    return stats
