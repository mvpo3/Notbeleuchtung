"""rest_komponenten — stempellose Restflächen als Räume labeln (Quelle 'REST').

Nach der Kaskade raumlayer → raum-hatch → stempel_flutung bleiben Flächen ohne
Stempel übrig (Stiegenhaus-Kerne, Gänge, Schächte). Die werden hier aus der
Wandmaske rekonstruiert:

    Fläche = Außenkontur − wand_union − bereits belegte Räume; Türöffnungen
    werden als Trennlinien (Kreisstempel) in die Wandmaske eingezeichnet
    (50-mm-Raster wie stempel_flutung), freie Zellen gelabelt, je Komponente
    ≥1 m² ein ``Raum``. Typ-Regeln:

    - enthält STIEGE-/Treppen-/LIFT-Block-Insert          → STIEGENHAUS
    - schmal (Breite <2.5 m) mit ≥3 Türöffnungen am Rand  → GANG
    - klein (<3 m²) ohne Tür oder mit STO-Kästchen drin   → SCHACHT
    - sonst                                               → UNBEKANNT

Grenze: rein 2D, Rasterauflösung ``raster_mm``; nur das größte zusammenhängende
Bauteil (Außenkontur = größte Union-Komponente).
"""
from __future__ import annotations

import re

import numpy as np
from shapely.geometry import Point, Polygon
from skimage.measure import label
from skimage.morphology import disk

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from .dxf_load import XY, DxfPlan
from .stempel_flutung import _fuelle, _Raster, _vektorisiere
from .tueren import TuerOeffnung
from .wandkoerper import (
    Wandkoerper,
    _kurzseite,
    aussenkontur,
    bounds_aus_wandkoerpern,
    wand_union,
)

_MIN_M2 = 1.0
_SCHACHT_MAX_M2 = 3.0
_GANG_BREITE_MAX_MM = 2500.0
_GANG_MIN_TUEREN = 3
_TUER_RAND_MM = 600.0          # Tür zählt „am Rand“, wenn ≤ 0.6 m vom Polygon
_BELEGT_PUFFER_MM = 100.0      # frisst 50-mm-Raster-Slivers zwischen Raum und Wand

# Treppen-/Lift-Blöcke (Mollgasse: 'STIEGE', 'LIFT') → Komponente = Stiegenhaus.
_STIEGE_RX = re.compile(r"STIEGE|TREPPE|STAIR|LIFT|AUFZUG", re.IGNORECASE)
# Rote Schlitz-/Durchbruch-Kästchen (Mollgasse '04-STO…'/'05-STO…', ~0.08 m).
_STO_LAYER_RX = re.compile(r"0\d-STO", re.IGNORECASE)
_STO_MAX_M2 = 0.5
_MARKER_NAEHE_MM = 1000.0      # Insert-Basispunkte liegen oft AUF der Wand


def _marker_punkte(plan: DxfPlan | None) -> tuple[list[XY], list[XY]]:
    """(Stiegen-/Lift-Insert-Punkte, STO-Kästchen-Zentren) in mm."""
    stiegen: list[XY] = []
    sto: list[XY] = []
    if plan is None:
        return stiegen, sto
    for e in plan.space:
        t = e.dxftype()
        if t == "INSERT" and _STIEGE_RX.search(str(e.dxf.name)):
            # bbox-Zentrum der Block-Geometrie statt Insert-Punkt: ArchiCAD-
            # Weltkoordinaten-Blöcke (Rennweg Stair_N) tragen den Insert-Punkt
            # weit weg von der Geometrie.
            try:
                import ezdxf.bbox
                ext = ezdxf.bbox.extents(e.virtual_entities(), fast=True)
                if ext.has_data:
                    c = ext.center
                    stiegen.append(plan._scale((c.x, c.y)))
                    continue
            except Exception:  # noqa: BLE001, S110 — kaputter Block: Insert-Punkt reicht
                pass
            stiegen.append(plan._scale(e.dxf.insert))
        elif (t in ("LWPOLYLINE", "POLYLINE") and getattr(e, "closed", False)
              and _STO_LAYER_RX.search(str(e.dxf.layer))):
            pts = plan.entity_points(e)
            if len(pts) >= 3:
                shp = Polygon(pts)
                if 0 < shp.area <= _STO_MAX_M2 * 1e6:
                    sto.append((shp.centroid.x, shp.centroid.y))
    return stiegen, sto


def _typisiere(shp: Polygon, tueren: list[TuerOeffnung],
               stiegen: list[XY], sto: list[XY]) -> tuple[str, bool, bool]:
    """Typ-Regeln (s. Modul-Doc) → (raum_typ, ist_fluchtweg, ist_communal)."""
    if any(shp.distance(Point(p)) <= _MARKER_NAEHE_MM for p in stiegen):
        return "STIEGENHAUS", True, True
    tuer_n = sum(1 for t in tueren
                 if shp.distance(Point(t.xy_mm)) <= _TUER_RAND_MM)
    if _kurzseite(shp) < _GANG_BREITE_MAX_MM and tuer_n >= _GANG_MIN_TUEREN:
        return "GANG", True, True
    if shp.area < _SCHACHT_MAX_M2 * 1e6 and (
            tuer_n == 0 or any(shp.covers(Point(p)) for p in sto)):
        return "SCHACHT", False, False
    return "UNBEKANNT", False, False


def komponenten_ohne_stempel(
    plan: DxfPlan | None,
    wandkoerper: list[Wandkoerper],
    tueren: list[TuerOeffnung],
    bereits_belegte_polygone: list[list[XY]],
    raster_mm: float = 50.0,
) -> list[Raum]:
    """Restflächen (Außenkontur − Wände − belegte Räume) als Räume, Quelle 'REST'.

    ``plan`` liefert nur die Typ-Marker (Stiegen-/Lift-Blöcke, STO-Kästchen) —
    ``None`` ist erlaubt, dann typt nur die Geometrie-Regel.
    """
    if not wandkoerper:
        return []
    union = wand_union(wandkoerper)
    # d=1000: echte Öffnungen bis ~1.7 m (Rennweg) müssen überbrückt werden,
    # sonst zerfällt die Kontur und „größtes Polygon" ist ein Splitter.
    kontur = aussenkontur(wandkoerper, d_mm=1000.0)
    if kontur.is_empty:
        return []
    b = bounds_aus_wandkoerpern(wandkoerper)
    res = raster_mm
    pad = 4
    h = int(np.ceil((b.max_xy[1] - b.min_xy[1]) / res)) + 2 * pad + 1
    w = int(np.ceil((b.max_xy[0] - b.min_xy[0]) / res)) + 2 * pad + 1
    raster = _Raster(x0=b.min_xy[0], y0=b.min_xy[1], res=res, pad=pad, shape=(h, w))

    innen = np.zeros((h, w), dtype=bool)
    _fuelle(innen, kontur, raster)
    blockiert = ~innen
    wand = np.zeros((h, w), dtype=bool)
    _fuelle(wand, union, raster)
    blockiert |= wand
    # Türöffnungen als Trennlinien versiegeln (wie stempel_flutung, Stufe 0).
    for t in tueren:
        r_px = max(1, round(max(_TUER_RAND_MM, t.breite_mm) / res))
        rr, cc = raster.px(t.xy_mm)
        d = disk(r_px, dtype=bool)
        r0, c0 = rr - r_px, cc - r_px
        rs = slice(max(r0, 0), min(r0 + d.shape[0], h))
        cs = slice(max(c0, 0), min(c0 + d.shape[1], w))
        blockiert[rs, cs] |= d[rs.start - r0:rs.stop - r0, cs.start - c0:cs.stop - c0]
    for poly in bereits_belegte_polygone:
        if len(poly) < 3:
            continue
        shp = Polygon(poly).buffer(_BELEGT_PUFFER_MM)
        if not shp.is_empty:
            _fuelle(blockiert, shp, raster)

    stiegen, sto = _marker_punkte(plan)
    grenze = union.boundary if not union.is_empty else None
    labels = label(~blockiert)
    out: list[Raum] = []
    for lbl in range(1, int(labels.max()) + 1):
        m = labels == lbl
        if m.sum() * res * res < _MIN_M2 * 1e6:
            continue
        shp = _vektorisiere(m, raster, grenze)
        if shp.is_empty or shp.area < _MIN_M2 * 1e6:
            continue
        typ, flucht, communal = _typisiere(shp, tueren, stiegen, sto)
        out.append(Raum(
            id=f"rest_{len(out) + 1}",
            raum_typ=typ,
            polygon_mm=[(float(x), float(y)) for x, y in shp.exterior.coords[:-1]],
            flaeche_m2=shp.area / 1e6,
            ist_fluchtweg=flucht,
            ist_communal=communal,
        ))
    return out
