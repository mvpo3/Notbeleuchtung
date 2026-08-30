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
