"""footprint — Gebäude-Umriss per Raster-Flood-Fill (innen vs. außen).

Naive Vektor-Methoden (Wand-Polygonisierung, Buffer-Union, konvexe Hülle)
scheitern am lückigen, nicht-konvexen Wandwerk. Robust ist Rasterung:

    Wände rastern → morphologisch dilatieren (Türlücken schließen) → freie
    Fläche → von der Ecke (garantiert außen) fluten → alles Nicht-Geflutete ist
    Gebäude-Inneres.

Daraus: **Hauptausgänge = Perimeter-Türen** — Türen, deren Rasterzelle nahe am
Außenbereich liegt (in der Außenwand). Innentüren liegen tief im Inneren.
Nur ``scikit-image`` (kein scipy) — Distanz via Dilatation der Außen-Maske.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from skimage.draw import line as _rasterline
from skimage.measure import label
from skimage.morphology import dilation, disk

from notbeleuchtung.hauptengine.contracts.raum_modell import Ausgang, BBox, Tuer

from .dxf_load import DxfPlan
from .waende import wand_segmente

_RES_MM = 200.0          # Rasterauflösung
_CLOSE_MM = 1000.0       # Dilatation zum Schließen der Türlücken
_PERIMETER_MM = 1600.0   # „nahe Außenwand" → Perimeter-Tür

XY = tuple[float, float]


@dataclass
class Umriss:
    """Rasterisierter Gebäude-Umriss (Außen-Maske + Transform)."""

    aussen: np.ndarray          # True = außerhalb des Gebäudes
    nahe_aussen: np.ndarray     # True = innerhalb _PERIMETER_MM zur Außenkante
    x0: float
    y0: float
    res: float

    def _px(self, xy: XY) -> tuple[int, int]:
        h, w = self.aussen.shape
        r = int((xy[1] - self.y0) / self.res) + 4
        c = int((xy[0] - self.x0) / self.res) + 4
        return min(max(r, 0), h - 1), min(max(c, 0), w - 1)

    def ist_perimeter(self, xy: XY) -> bool:
        """True, wenn die Position an der Gebäude-Außenwand liegt (Perimeter)."""
        r, c = self._px(xy)
        return bool(self.nahe_aussen[r, c] and not self.aussen[r, c])


def gebaeude_umriss(plan: DxfPlan, bounds: BBox) -> Umriss | None:
    """Raster-Umriss aus den Wänden; None wenn keine Wände."""
    segs = wand_segmente(plan)
    if not segs:
        return None
    x0, y0 = bounds.min_xy
    x1, y1 = bounds.max_xy
    res = _RES_MM
    w = int((x1 - x0) / res) + 8
    h = int((y1 - y0) / res) + 8
    wall = np.zeros((h, w), dtype=bool)
    for a, b in segs:
        r0 = int((a[1] - y0) / res) + 4
        c0 = int((a[0] - x0) / res) + 4
        r1 = int((b[1] - y0) / res) + 4
        c1 = int((b[0] - x0) / res) + 4
        rr, cc = _rasterline(r0, c0, r1, c1)
        wall[np.clip(rr, 0, h - 1), np.clip(cc, 0, w - 1)] = True

    closed = dilation(wall, disk(round(_CLOSE_MM / res)))
    labels = label(~closed)
    aussen = labels == labels[0, 0]  # Ecke (0,0) ist garantiert außen
    nahe = dilation(aussen, disk(round(_PERIMETER_MM / res)))
    return Umriss(aussen=aussen, nahe_aussen=nahe, x0=x0, y0=y0, res=res)


def ausgaenge_aus_umriss(
    plan: DxfPlan, tueren: list[Tuer], bounds: BBox
) -> list[Ausgang]:
    """Hauptausgänge = Türen an der Gebäude-Außenwand (``final_exit``)."""
    umriss = gebaeude_umriss(plan, bounds)
    if umriss is None:
        return []
    out: list[Ausgang] = []
    for t in tueren:
        if umriss.ist_perimeter(t.xy_mm):
            out.append(
                Ausgang(id=f"exit_{len(out) + 1}", xy_mm=t.xy_mm, typ="final_exit")
            )
    return out
