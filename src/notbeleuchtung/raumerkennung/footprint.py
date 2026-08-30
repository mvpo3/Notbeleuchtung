"""footprint — Gebäude-Umriss (Raster-Flood-Fill) + Hauptausgang-Erkennung.

Naive Vektor-Methoden (Wand-Polygonisierung, Buffer-Union, konvexe Hülle)
scheitern am lückigen, nicht-konvexen Wandwerk. Robust ist Rasterung:

    Wände rastern → dilatieren (Türlücken schließen) → freie Fläche → von der
    Ecke (garantiert außen) fluten → alles Nicht-Geflutete ist Gebäude-Inneres.
    Der Ring am Übergang innen/außen ist die Gebäude-Außenkante.

**Hauptausgang = Doppeltür am Gebäude-Rand.** Fachmuster (vom Owner bestätigt):
Gebäude-Haupteingänge sind als **Doppeltür** gezeichnet — zwei Tür-Blätter,
d.h. zwei Schwenkbögen (ARCs) gleicher Größe, deren Drehpunkte eine
Türöffnungsbreite (~1.4–2.6 m) auseinanderliegen. Ein solches ARC-Paar **an der
Außenkante** ist ein Hauptausgang. So werden die (vielen) Innen- und
Fassaden-Einzeltüren ausgeschlossen. Je Gebäude/Stiegenhaus 1–2 Stück.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np
from skimage.draw import line as _rasterline
from skimage.measure import label
from skimage.morphology import dilation, disk, erosion

from notbeleuchtung.hauptengine.contracts.raum_modell import Ausgang, BBox

from .dxf_load import DxfPlan
from .waende import wand_segmente

_RES_MM = 200.0          # Rasterauflösung
_CLOSE_MM = 1000.0       # Dilatation zum Schließen der Türlücken
_RIM_MM = 800.0          # Toleranzband um die Gebäude-Außenkante

_ARC_MIN_MM = 600.0      # Schwenkbogen-Radius (≈ Tür-Blattbreite)
_ARC_MAX_MM = 1300.0
_PAIR_MIN_MM = 1400.0    # Abstand der zwei Drehpunkte einer Doppeltür
_PAIR_MAX_MM = 2600.0
_PAIR_RADIUS_TOL_MM = 250.0

XY = tuple[float, float]


@dataclass
class Umriss:
    """Rasterisierter Gebäude-Umriss (Außen-Maske + Rand-Band + Transform)."""

    aussen: np.ndarray          # True = außerhalb des Gebäudes
    rand: np.ndarray            # True = im Toleranzband um die Außenkante
    x0: float
    y0: float
    res: float
    pad: int

    def _px(self, xy: XY) -> tuple[int, int]:
        h, w = self.aussen.shape
        r = int((xy[1] - self.y0) / self.res) + self.pad
        c = int((xy[0] - self.x0) / self.res) + self.pad
        return min(max(r, 0), h - 1), min(max(c, 0), w - 1)

    def ist_am_rand(self, xy: XY) -> bool:
        """True, wenn die Position an der Gebäude-Außenkante liegt."""
        r, c = self._px(xy)
        return bool(self.rand[r, c])


def gebaeude_umriss(plan: DxfPlan, bounds: BBox) -> Umriss | None:
    """Raster-Umriss aus den Wänden; None wenn keine Wände."""
    segs = wand_segmente(plan)
    if not segs:
        return None
    x0, y0 = bounds.min_xy
    x1, y1 = bounds.max_xy
    res = _RES_MM
    close_px = round(_CLOSE_MM / res)
    pad = close_px + 4  # Rand > Schließ-Dilatation, sonst frisst sie die Ecke
    w = int((x1 - x0) / res) + 2 * pad
    h = int((y1 - y0) / res) + 2 * pad
    wall = np.zeros((h, w), dtype=bool)
    for a, b in segs:
        r0 = int((a[1] - y0) / res) + pad
        c0 = int((a[0] - x0) / res) + pad
        r1 = int((b[1] - y0) / res) + pad
        c1 = int((b[0] - x0) / res) + pad
        rr, cc = _rasterline(r0, c0, r1, c1)
        wall[np.clip(rr, 0, h - 1), np.clip(cc, 0, w - 1)] = True

    closed = dilation(wall, disk(close_px))
    labels = label(~closed)
    aussen = labels == labels[0, 0]  # Ecke (0,0) ist garantiert außen
    solid = ~aussen
    kante = solid & ~erosion(solid, disk(2))     # dünner Ring der Außenkante
    rand = dilation(kante, disk(round(_RIM_MM / res)))
    return Umriss(aussen=aussen, rand=rand, x0=x0, y0=y0, res=res, pad=pad)


def _schwenkboegen(plan: DxfPlan) -> list[tuple[float, float, float]]:
    """Tür-Schwenkbögen als (x, y, radius) in mm (radius ≈ Tür-Blattbreite)."""
    out: list[tuple[float, float, float]] = []
    for e in plan.entities():
        if e.dxftype() != "ARC":
            continue
        r = float(e.dxf.radius) * plan.factor
        if _ARC_MIN_MM < r < _ARC_MAX_MM:
            cx, cy = plan._scale(e.dxf.center)
            out.append((cx, cy, r))
    return out


def _doppeltuer_mittelpunkte(plan: DxfPlan) -> list[XY]:
    """Mittelpunkte von Doppeltüren: Paare gleich großer Schwenkbögen, deren
    Drehpunkte eine Türöffnungsbreite auseinanderliegen."""
    arcs = _schwenkboegen(plan)
    mitten: list[XY] = []
    for (x1, y1, r1), (x2, y2, r2) in combinations(arcs, 2):
        d = np.hypot(x1 - x2, y1 - y2)
        if _PAIR_MIN_MM < d < _PAIR_MAX_MM and abs(r1 - r2) < _PAIR_RADIUS_TOL_MM:
            mitten.append(((x1 + x2) / 2.0, (y1 + y2) / 2.0))
    return mitten


def hauptausgaenge(plan: DxfPlan, bounds: BBox) -> list[Ausgang]:
    """Hauptausgänge = Doppeltüren an der Gebäude-Außenkante (``final_exit``)."""
    umriss = gebaeude_umriss(plan, bounds)
    if umriss is None:
        return []
    out: list[Ausgang] = []
    for xy in _doppeltuer_mittelpunkte(plan):
        if umriss.ist_am_rand(xy):
            out.append(
                Ausgang(id=f"exit_{len(out) + 1}",
                        xy_mm=(float(xy[0]), float(xy[1])), typ="final_exit")
            )
    return out
