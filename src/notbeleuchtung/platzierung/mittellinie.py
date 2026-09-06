"""mittellinie — Rettungsweg-Mittelachse via Skelettierung (scikit-image).

EN 1838 bemisst die Fluchtweg-Beleuchtung auf der **Mittellinie** des Weges (1 lx,
Ud ≥ 1:40) — wir haben aber Polygone. Dieses Modul rastert ein Gang-/Raum-Polygon
und zieht die **mediale Achse** (`skimage.morphology.skeletonize`) heraus: die Linie,
entlang der Sicherheitsleuchten verdichtet werden (Schicht „Linie" im Fahrplan
Anker → Linie → Fläche → Deckung). Reine Geometrie, render-frei.

`leuchten_auf_linie` sampelt die Achse in festem Abstand → Kandidat-Positionen für
Fluchtweg-Sicherheitsleuchten (der Abstand kommt später aus der Hersteller-
Abstandstabelle / dem Lux-Nachweis, hier Parameter).
"""
from __future__ import annotations

import numpy as np
from skimage.draw import polygon as _sk_polygon
from skimage.morphology import skeletonize as _skeletonize

Point = tuple[float, float]
Polygon = list[Point]


def _raster(polygon: Polygon, raster_mm: float):
    xs = [p[0] for p in polygon]
    ys = [p[1] for p in polygon]
    minx, miny = min(xs), min(ys)
    w = int((max(xs) - minx) / raster_mm) + 3
    h = int((max(ys) - miny) / raster_mm) + 3
    cc = np.array([(x - minx) / raster_mm + 1 for x in xs])
    rr = np.array([(y - miny) / raster_mm + 1 for y in ys])
    mask = np.zeros((h, w), dtype=bool)
    fr, fc = _sk_polygon(rr, cc, shape=(h, w))
    mask[fr, fc] = True
    return mask, minx, miny


def mittellinie(polygon: Polygon, raster_mm: float = 200.0) -> list[Point]:
    """Mediale Achse (Skelett) des Polygons als Punktliste in mm.

    `raster_mm` = Rasterauflösung (feiner = genauer + langsamer). Für rechteckige
    Gänge ergibt das die Längsmittellinie; bei L-Formen folgt die Achse dem Knick.
    """
    if len(polygon) < 3:
        return []
    mask, minx, miny = _raster(polygon, raster_mm)
    skel = _skeletonize(mask)
    rows, cols = np.nonzero(skel)
    return [(minx + (c - 1) * raster_mm, miny + (r - 1) * raster_mm) for r, c in zip(rows, cols)]


def leuchten_auf_linie(polygon: Polygon, abstand_mm: float, raster_mm: float = 200.0) -> list[Point]:
    """Kandidat-Positionen entlang der Mittelachse in ~`abstand_mm` Abstand.

    Greedy-räumliches Ausdünnen: Achsen-Punkte der Reihe nach abgehen, einen neuen
    Punkt nur setzen, wenn er von **allen bereits gesetzten** ≥ `abstand_mm` entfernt
    ist. Der Abgleich gegen alle (statt nur den letzten) verhindert Überproduktion bei
    2D-verzweigten Skeletten (breite/offene Räume, deren Mittelachse kein einfacher
    Strich ist). Der exakte Abstand folgt aus dem Lux-Nachweis (`lux.py`).
    """
    pts = mittellinie(polygon, raster_mm)
    if not pts:
        return []
    pts = sorted(pts)  # entlang x (dominante Achse bei Gängen)
    gesetzt = [pts[0]]
    for p in pts[1:]:
        if all(((p[0] - gx) ** 2 + (p[1] - gy) ** 2) ** 0.5 >= abstand_mm
               for gx, gy in gesetzt):
            gesetzt.append(p)
    return gesetzt


def leuchten_auf_linie_mit_richtung(
    polygon: Polygon, abstand_mm: float, raster_mm: float = 200.0
) -> list[tuple[float, float, float]]:
    """Wie `leuchten_auf_linie`, plus **Achsen-Azimut je Kandidat** (Grad, math.
    positiv, 0° = +x).

    Der Azimut ist die lokale Tangente der Mittelachse am Kandidaten — die
    Richtung, in der eine Corridor-Optik (C0-Keule längs des Gangs) montiert
    wird. Er speist den richtungsrichtigen Lux-Nachweis (`lux`-Leuchten-Tripel)
    UND wird als Montage-Rotation an die Platzierung geschrieben; C0/C180-
    Symmetrie der Optik macht die 180°-Ambiguität der Tangente unschädlich.
    """
    pts = mittellinie(polygon, raster_mm)
    if not pts:
        return []
    pts = sorted(pts)
    gesetzt = leuchten_auf_linie(polygon, abstand_mm, raster_mm)

    def tangente(g: Point) -> float:
        i = min(range(len(pts)), key=lambda k: (pts[k][0] - g[0]) ** 2 + (pts[k][1] - g[1]) ** 2)
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        if abs(dx) < 1e-9 and abs(dy) < 1e-9:
            return 0.0
        return float(np.degrees(np.arctan2(dy, dx))) % 360.0

    return [(gx, gy, tangente((gx, gy))) for gx, gy in gesetzt]
