"""gang_anker — Platzierungs-Anker entlang der Gang-Mittelachse.

Die Mittelachse kommt aus dem skimage-Skelett des Raumpolygons
(``fluchtweg._skelett_pfad`` wiederverwendet — dieselbe Achse wie die
GRAPH-Segmente). Anker:

- **TUER** — Lot jeder Gang-Tür auf die Achse; ``winkel_grad`` =
  Türwandwinkel (Rotationsquelle der RZ über der Tür — geliefert als Feld,
  die Regel-Umsetzung bleibt Leonis),
- **RICHTUNGSWECHSEL** — Achsen-Knick > 30°,
- **KREUZUNG** — Schnittpunkt zweier Fluchtweg-Segmente im Raum,
- **ENDE** — Achsen-Endpunkte,
- **STRECKE** — Zwischenpunkte alle ~10 m.

``fluchtrichtung_grad`` je Anker = Richtung zum nächsten stair_exit/
final_exit, abgelesen am nächstliegenden Fluchtweg-Segment mit
``ziel_ausgang`` (Segment-Polylinien laufen Start → Ausgang).

ADR-0006 (bindend, zitiert): „Für Fluchtweg-Sicherheitsleuchten leitet der
Verdichter den Korridor-Achsen-Azimut ab, rechnet die C-Ebene RELATIV dazu
und schreibt DENSELBEN Azimut als rotation_deg — der Plan selbst ist die
Montage-/Ausrichtungs-Zusicherung." Diese Anker liefern die Azimute
(``winkel_grad``/``fluchtrichtung_grad``); Platzierung/Rotation entscheidet
die Platzierung (Leonis) — hier wird NICHTS platziert.
"""
from __future__ import annotations

import math
from itertools import pairwise

from shapely.geometry import LineString, Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import (
    Anker,
    FluchtwegSegment,
    Raum,
    Tuer,
)

from .fluchtweg import _skelett_pfad

XY = tuple[float, float]

_KNICK_GRAD = 30.0
_STRECKE_MM = 10_000.0
_ANKER_MIN_ABSTAND_MM = 2000.0
_TUER_AN_RAUM_MM = 600.0


def _achse(poly: Polygon) -> list[XY]:
    """Skelett-Mittelachse: Skelett-Pfad zwischen den beiden entferntesten
    Kanten-Mittelpunkten des Raumpolygons (Wiederverwendung von
    ``fluchtweg._skelett_pfad`` — folgt bei L-Gängen dem Knick)."""
    coords = list(poly.exterior.coords)
    mitten = [((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
              for p, q in pairwise(coords)]
    if len(mitten) < 2:
        return []
    a, b = max(((p, q) for i, p in enumerate(mitten) for q in mitten[i + 1:]),
               key=lambda pq: math.dist(*pq))
    pfad = _skelett_pfad(poly, a, b)
    # Raster-Jitter des Skeletts glätten, sonst wird jeder Pixel-Zickzack
    # ein falscher RICHTUNGSWECHSEL-Anker.
    glatt = LineString(pfad).simplify(500.0)
    return [(float(x), float(y)) for x, y in glatt.coords]


def _winkel(a: XY, b: XY) -> float:
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


def _wandwinkel(poly: Polygon, xy: XY) -> float:
    pt = Point(xy)
    best, best_d = 0.0, math.inf
    coords = list(poly.exterior.coords)
    for a, b in pairwise(coords):
        d = LineString([a, b]).distance(pt)
        if d < best_d:
            best_d = d
            best = _winkel(a, b) % 180.0
    return best


def _fluchtrichtung(xy: XY, segmente: list[FluchtwegSegment]) -> float | None:
    """Lokale Richtung ZUM Ausgang am nächsten Segment mit ``ziel_ausgang``."""
    best_seg, best_d = None, math.inf
    for s in segmente:
        if not s.ziel_ausgang or len(s.polyline_mm) < 2:
            continue
        d = LineString(s.polyline_mm).distance(Point(xy))
        if d < best_d:
            best_d, best_seg = d, s
    if best_seg is None:
        return None
    pts = best_seg.polyline_mm            # läuft Start → ziel_ausgang
    k = min(range(len(pts)), key=lambda i: math.dist(pts[i], xy))
    if k + 1 < len(pts):
        return _winkel(pts[k], pts[k + 1]) % 360.0
    return _winkel(pts[k - 1], pts[k]) % 360.0


def anker_fuer_gang(raum: Raum, tueren: list[Tuer],
                    fluchtwege: list[FluchtwegSegment]) -> list[Anker]:
    """Anker eines GANG-Raums entlang der Skelett-Mittelachse (s. Modul-Doc)."""
    if len(raum.polygon_mm) < 3:
        return []
    poly = Polygon(raum.polygon_mm).buffer(0)
    if poly.is_empty:
        return []
    achse = _achse(poly)
    if len(achse) < 2:
        return []
    linie = LineString(achse)
    anker: list[Anker] = []

    def _neu(typ: str, xy: XY, winkel: float | None = None) -> None:
        anker.append(Anker(
            id=f"{raum.id}_{typ.lower()}_{len(anker) + 1}", typ=typ, xy_mm=xy,
            winkel_grad=winkel,
            fluchtrichtung_grad=_fluchtrichtung(xy, fluchtwege),
            raum_id=raum.id))

    # TUER — Lot jeder Gang-Tür auf die Achse, Winkel = Türwandwinkel.
    for t in tueren:
        an_raum = (raum.id in (t.von_raum, t.nach_raum)
                   or poly.exterior.distance(Point(t.xy_mm)) < _TUER_AN_RAUM_MM)
        if not an_raum:
            continue
        lot = linie.interpolate(linie.project(Point(t.xy_mm)))
        _neu("TUER", (float(lot.x), float(lot.y)),
             winkel=_wandwinkel(poly, t.xy_mm))

    # ENDE — Achsen-Endpunkte.
    _neu("ENDE", achse[0])
    _neu("ENDE", achse[-1])

    # RICHTUNGSWECHSEL — Knick > 30° in der Achse.
    for i in range(1, len(achse) - 1):
        w1 = _winkel(achse[i - 1], achse[i])
        w2 = _winkel(achse[i], achse[i + 1])
        diff = abs(w2 - w1) % 360.0
        diff = min(diff, 360.0 - diff)
        if diff > _KNICK_GRAD:
            _neu("RICHTUNGSWECHSEL", achse[i])

    # KREUZUNG — Schnittpunkte zweier Fluchtweg-Segmente im Raum.
    segs = [LineString(s.polyline_mm) for s in fluchtwege
            if len(s.polyline_mm) >= 2]
    for i, s1 in enumerate(segs):
        for s2 in segs[i + 1:]:
            x = s1.intersection(s2)
            punkte = ([x] if x.geom_type == "Point"
                      else list(getattr(x, "geoms", [])))
            for p in punkte:
                if p.geom_type != "Point" or not poly.covers(p):
                    continue
                xy = (float(p.x), float(p.y))
                if all(math.dist(xy, a.xy_mm) > _ANKER_MIN_ABSTAND_MM
                       for a in anker):
                    _neu("KREUZUNG", xy)

    # STRECKE — Zwischenpunkte alle ~10 m, weg von bestehenden Ankern.
    d = _STRECKE_MM
    while d < linie.length:
        p = linie.interpolate(d)
        xy = (float(p.x), float(p.y))
        if all(math.dist(xy, a.xy_mm) > _ANKER_MIN_ABSTAND_MM for a in anker):
            _neu("STRECKE", xy)
        d += _STRECKE_MM
    return anker
