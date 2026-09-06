"""stempel_flutung — Raumpolygone per Raster-Flutung vom Stempelpunkt aus.

Für Stempel OHNE zugeordnetes Raumpolygon (Pläne ohne Raum-Layer/Raum-Hatches)
wird der Raum aus den Wandkörpern rekonstruiert:

    Wände rastern (50-mm-Zellen) → Türöffnungen morphologisch versiegeln
    (Kreisstempel, Stufen 0.6/0.9/1.2/1.5 m, generisches Closing nur als letzte
    Stufe) → vom Stempelpunkt fluten → Region zur Wand zurückdehnen → Kontur
    vektorisieren + an die Wandkanten snappen → Fläche gegen den m²-Stempel
    prüfen (±10 %). Passt keine Stufe, bleibt das beste Ergebnis mit Flag
    ``flutung_unsicher`` — NIE verwerfen. Mehrere Stempel im selben Flutgebiet
    werden per Watershed (Distanz-Relief) getrennt.

Die Flutung verlässt die Gebäude-Außenkontur nicht: das Raster-Äquivalent von
``aussenkontur(wandkoerper)`` ist ein Ecken-Flood auf der maximal versiegelten
Wandmaske (wie footprint.py) — alles Außen wird zu Wand. Koordinaten werden über
den Raster-Ursprung (Wand-Bounds) lokalisiert, große Plan-Offsets (Rennweg
~12.5e6 mm) sind damit egal.

Grenze: rein 2D, Rasterauflösung ``raster_mm`` (Default 50 mm); Stempel ohne
m²-Angabe bekommen die niedrigste Versiegelungsstufe und Flag ``ok``.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy import ndimage
from shapely.geometry import Polygon
from shapely.ops import snap
from skimage.draw import polygon as _fill_polygon
from skimage.measure import find_contours, label
from skimage.morphology import closing, disk
from skimage.segmentation import watershed

from .dxf_load import XY, DxfPlan
from .stempel_anker import Stempel
from .tueren import TuerOeffnung
from .wandkoerper import Wandkoerper, bounds_aus_wandkoerpern, wand_union

_TOLERANZ_PROZENT = 10.0
# Versiegelungsstufen (Kreisradius in mm); letzte Stufe zusätzlich mit
# generischem Closing 1.2 m (NUR dort — sonst frisst es Gänge).
_STUFEN_MM = (600.0, 900.0, 1200.0, 1500.0)
_CLOSING_MM = 1200.0
_SIMPLIFY_MM = 25.0
_SNAP_MM = 50.0


@dataclass
class FlutRaum:
    """Ein per Flutung rekonstruierter Raum (Polygon in mm)."""

    polygon_mm: list[XY]
    stempel: Stempel
    abweichung_prozent: float          # (Flutfläche − Stempelfläche) / Stempel · 100
    flag: str                          # 'ok' | 'flutung_unsicher'
    quelle: str = "FLUTUNG"


@dataclass
class _Raster:
    """Pixel-Transform: mm ↔ (row, col), Ursprung = Wand-Bounds (lokalisiert)."""

    x0: float
    y0: float
    res: float
    pad: int
    shape: tuple[int, int]

    def px(self, xy: XY) -> tuple[int, int]:
        h, w = self.shape
        r = round((xy[1] - self.y0) / self.res) + self.pad
        c = round((xy[0] - self.x0) / self.res) + self.pad
        return min(max(r, 0), h - 1), min(max(c, 0), w - 1)

    def mm(self, r: float, c: float) -> XY:
        return (self.x0 + (c - self.pad) * self.res, self.y0 + (r - self.pad) * self.res)


def _fuelle(mask: np.ndarray, geom, raster: _Raster) -> None:
    """Polygon(e) in die Maske rastern (Exterior=True, Löcher wieder frei)."""
    polys = geom.geoms if geom.geom_type in ("MultiPolygon", "GeometryCollection") \
        else [geom]
    for p in polys:
        if p.geom_type != "Polygon" or p.is_empty:
            continue
        for ring, wert in [(p.exterior, True)] + [(i, False) for i in p.interiors]:
            rc = [raster.px(xy) for xy in ring.coords]
            rr, cc = _fill_polygon([r for r, _ in rc], [c for _, c in rc],
                                   shape=mask.shape)
            mask[rr, cc] = wert


@dataclass
class _Flutwerk:
    """Gerasterte Wand-/Innen-Masken + stufenweise Segmentierung (Cache)."""

    raster: _Raster
    wand: np.ndarray                   # True = Wand (inkl. außerhalb Außenkontur)
    tueren: list[TuerOeffnung]
    stempel: list[Stempel]
    _cache: dict[int, dict[int, np.ndarray]] = field(default_factory=dict)

    def _blockiert(self, stufe: int) -> np.ndarray:
        b = self.wand.copy()
        r_px = max(1, round(_STUFEN_MM[min(stufe, len(_STUFEN_MM) - 1)] / self.raster.res))
        for t in self.tueren:
            rr, cc = self.raster.px(t.xy_mm)
            d = disk(r_px, dtype=bool)
            r0, c0 = rr - r_px, cc - r_px
            rs = slice(max(r0, 0), min(r0 + d.shape[0], b.shape[0]))
            cs = slice(max(c0, 0), min(c0 + d.shape[1], b.shape[1]))
            b[rs, cs] |= d[rs.start - r0:rs.stop - r0, cs.start - c0:cs.stop - c0]
        if stufe >= len(_STUFEN_MM):       # letzte Stufe: generisches Closing
            b |= closing(b, disk(round(_CLOSING_MM / self.raster.res)))
        return b

    def masken(self, stufe: int) -> dict[int, np.ndarray]:
        """Je Stempel-Index seine Flutregion bei dieser Versiegelungsstufe.

        Stempel auf Wand/Versiegelung starten am nächsten freien Pixel (EDT).
        Teilen sich mehrere Stempel eine Region, trennt Watershed
        (Marker = Stempelpunkte, Distanz-Transform als Relief).
        """
        if stufe in self._cache:
            return self._cache[stufe]
        blockiert = self._blockiert(stufe)
        frei = ~blockiert
        # EDT auf 'blockiert': für jedes Pixel Index des nächsten FREIEN Pixels.
        _, (ir, ic) = ndimage.distance_transform_edt(blockiert, return_indices=True)
        labels = label(frei)
        starts: dict[int, tuple[int, int]] = {}
        gruppen: dict[int, list[int]] = {}
        for i, st in enumerate(self.stempel):
            r, c = self.raster.px(st.position_mm)
            r, c = int(ir[r, c]), int(ic[r, c])
            lbl = int(labels[r, c])
            starts[i] = (r, c)
            if lbl:
                gruppen.setdefault(lbl, []).append(i)
        out: dict[int, np.ndarray] = {i: np.zeros_like(frei) for i in range(len(self.stempel))}
        for lbl, idx in gruppen.items():
            region = labels == lbl
            if len(idx) == 1:
                out[idx[0]] = region
                continue
            relief = ndimage.distance_transform_edt(region)
            marker = np.zeros(region.shape, dtype=np.int32)
            for i in idx:
                marker[starts[i]] = i + 1
            ws = watershed(-relief, markers=marker, mask=region)
            for i in idx:
                out[i] = ws == i + 1
        # Geodätisch zur Wand zurückdehnen: die VERSIEGELTEN Zellen (blockiert ∧
        # ¬wand) den nächstliegenden Regionen zuschlagen (geodätischer Watershed
        # auf konstantem Relief) — Nachbarregionen konkurrieren mit, damit ein
        # großer Siegel-Kreis nicht über die Türlinie in den Nachbarraum leakt.
        siegel = blockiert & ~self.wand
        if siegel.any() and any(m.any() for m in out.values()):
            marker = np.zeros(frei.shape, dtype=np.int32)
            rest = frei.copy()
            for i, m in out.items():
                marker[m] = i + 1
                rest &= ~m
            marker[rest] = len(self.stempel) + 1
            ws = watershed(np.zeros(frei.shape, dtype=np.uint8), markers=marker,
                           mask=frei | siegel)
            for i, m in out.items():
                if m.any():
                    out[i] = ws == i + 1
        for i, m in out.items():
            if m.any():
                out[i] = ndimage.binary_fill_holes(m)
        self._cache[stufe] = out
        return out


def _shoelace(pts: list[tuple[float, float]]) -> float:
    return 0.5 * abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1])))


def _vektorisiere(mask: np.ndarray, raster: _Raster, wand_grenze) -> Polygon:
    """Maske → größte Kontur → simplify(25 mm) → Snap an Wandkanten (50 mm)."""
    konturen = find_contours(mask.astype(np.uint8), 0.5)
    if not konturen:
        return Polygon()
    beste = max(konturen, key=lambda k: _shoelace([(r, c) for r, c in k]))
    pts = [raster.mm(r, c) for r, c in beste]
    poly = Polygon(pts).buffer(0)
    if poly.geom_type != "Polygon":
        if poly.is_empty:
            return Polygon()
        poly = max(poly.geoms, key=lambda g: g.area)
    poly = poly.simplify(_SIMPLIFY_MM)
    if wand_grenze is not None and not wand_grenze.is_empty:
        gesnappt = snap(poly, wand_grenze, _SNAP_MM).buffer(0)
        if gesnappt.geom_type == "Polygon" and not gesnappt.is_empty:
            poly = gesnappt
    return poly


def flute_stempel(
    plan: DxfPlan | None,
    stempel_ohne_polygon: list[Stempel],
    wandkoerper: list[Wandkoerper],
    tueren: list[TuerOeffnung],
    raster_mm: float = 50.0,
) -> list[FlutRaum]:
    """Je Stempel ohne Polygon einen Raum aus den Wandkörpern fluten (s. Modul-Doc).

    ``plan`` wird nicht gelesen (Koordinaten sind bereits mm) — er hält die
    Kaskaden-Signatur (plan_pruefen._raeume) stabil.
    """
    del plan
    if not stempel_ohne_polygon or not wandkoerper:
        return []
    union = wand_union(wandkoerper)
    b = bounds_aus_wandkoerpern(wandkoerper)
    res = raster_mm
    pad = round((max(_STUFEN_MM) + _CLOSING_MM) / res) + 4
    h = math.ceil((b.max_xy[1] - b.min_xy[1]) / res) + 2 * pad + 1
    w = math.ceil((b.max_xy[0] - b.min_xy[0]) / res) + 2 * pad + 1
    raster = _Raster(x0=b.min_xy[0], y0=b.min_xy[1], res=res, pad=pad, shape=(h, w))

    wand = np.zeros((h, w), dtype=bool)
    _fuelle(wand, union, raster)
    werk = _Flutwerk(raster=raster, wand=wand, tueren=tueren,
                     stempel=stempel_ohne_polygon)
    # Außenkontur (Raster-Äquivalent von aussenkontur()): Ecken-Flood auf der
    # maximal versiegelten Maske — die Ecke (0,0) liegt dank pad garantiert außen.
    lbl = label(~werk._blockiert(len(_STUFEN_MM)))
    werk.wand = wand | (lbl == lbl[0, 0])                   # außen = Wand
    grenze = union.boundary if not union.is_empty else None

    out: list[FlutRaum] = []
    for i, st in enumerate(stempel_ohne_polygon):
        best: tuple[float, Polygon] | None = None   # (|abw|, poly)
        best_abw = 0.0
        for stufe in range(len(_STUFEN_MM) + 1):
            m = werk.masken(stufe)[i]
            if not m.any():
                continue
            poly = _vektorisiere(m, raster, grenze)
            if poly.is_empty:
                continue
            if not st.flaeche_m2:
                out.append(FlutRaum(list(poly.exterior.coords), st, 0.0, "ok"))
                break
            abw = (poly.area / 1e6 - st.flaeche_m2) / st.flaeche_m2 * 100.0
            if best is None or abs(abw) < best[0]:
                best, best_abw = (abs(abw), poly), abw
            if abs(abw) <= _TOLERANZ_PROZENT:
                out.append(FlutRaum(list(poly.exterior.coords), st, round(abw, 1), "ok"))
                break
            if abw < 0:      # zu klein — höhere Versiegelung macht es nur kleiner
                break
        if len(out) > i:     # ok-Treffer (oder ohne m²) bereits angehängt
            continue
        if best is not None:
            out.append(FlutRaum(list(best[1].exterior.coords), st,
                                round(best_abw, 1), "flutung_unsicher"))
        else:                # nichts flutbar — trotzdem NIE verwerfen
            out.append(FlutRaum([], st, -100.0, "flutung_unsicher"))
    return out
