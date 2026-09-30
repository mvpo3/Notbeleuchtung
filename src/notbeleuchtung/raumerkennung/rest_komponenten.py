"""rest_komponenten — stempellose Restflächen als Räume labeln (Quelle 'REST').

Nach der Kaskade raumlayer → raum-hatch → stempel_flutung bleiben Flächen ohne
Stempel übrig (Stiegenhaus-Kerne, Gänge, Schächte). Die werden hier aus der
Wandmaske rekonstruiert:

    Fläche = Außenkontur − wand_union − bereits belegte Räume; Türöffnungen
    werden als Trennlinien (Kreisstempel) in die Wandmaske eingezeichnet
    (50-mm-Raster wie stempel_flutung), freie Zellen gelabelt, die Labels
    geodätisch in die Türscheiben zurückgedehnt (wie stempel_flutung, Slice
    S3b) und je Komponente ≥1 m² ein ``Raum``. Typ-Regeln:

    - klein (<3 m²) mit Schacht-Text/STO-Kästchen drin    → SCHACHT (Planzeichen)
    - enthält STIEGE-/Treppen-/LIFT-Block-Insert          → STIEGENHAUS
    - schmal (Breite <2.5 m) mit ≥3 Türöffnungen am Rand  → GANG
    - klein (<3 m²) ohne Tür, mit Schacht-Beleg            → SCHACHT
    - klein (<3 m²) ohne Tür, ohne Schacht-Beleg           → NISCHE (Slice K2)
    - sonst                                               → "" (untypisiert)

Grenze: rein 2D, Rasterauflösung ``raster_mm``; nur das größte zusammenhängende
Bauteil (Außenkontur = größte Union-Komponente).
"""
from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass, field

import numpy as np
from shapely.geometry import Point, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union
from skimage.measure import label
from skimage.morphology import disk
from skimage.segmentation import watershed

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from .dxf_load import XY, DxfPlan
from .stempel_flutung import _fuelle, _Raster, _vektorisiere
from .tueren import TuerOeffnung
from .wandkoerper import (
    Wandkoerper,
    _hatch_punkte,
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

# Schacht-Beschriftung als Planzeichen (Diagnose Rennweg U2, Slice S3a):
# Wortgrenze, „DBA" allein ist kein Schacht, Raum-/Treppen-/Lifttexte schließen
# aus (Barawitzka „Aufzug 1 BD 1,98/2,02", „Treppenlauf BD 4,745/1,26").
# ponytail: Wortschatz nur auf Rennweg gemessen (DG2 „DBA SCHACHT") — beim
# ersten Plan einer anderen Familie mit Schacht-Beschriftung nachmessen.
_SCHACHT_TEXT_RX = re.compile(
    r"(?<![A-ZÄÖÜ])SCHACHT(?![A-ZÄÖÜ])|(?<![A-Z])(?:F?BDB|DDB)(?![A-Z])")
_SCHACHT_AUSSCHLUSS_RX = re.compile(
    r"(?<![A-ZÄÖÜ])RAUM(?![A-ZÄÖÜ])|TREPP|STIEG|AUFZUG|LIFT")

# Owner-Regel a, Slice K2 (2026-09-29): „rote Kontur allein ist kein Beleg.
# SCHACHT braucht mindestens eines: Text DDB/BDB/DBA/Schacht/Durchbruch in
# 500 mm, U-förmige Schachtmauer, FEUERFESTER_STEIN-Keil, Schacht-Zone oder
# -Layer. Sonst NISCHE." Sie greift an der einzigen SCHACHT-Quelle ohne
# Planzeichen, der türlosen Kleinfläche (Diagnose Rennweg U5, DG2 `rest_5`).
# Stempel-SCHACHT (Zone, `raumtyp`) und Liftschacht-Reste (S5c/F1, Kabine
# > 50 %) sind durch ihre Quelle belegt und laufen hier nie durch.
# ponytail: U-förmige Schachtmauer ist NICHT umgesetzt — im Korpus hängt kein
# SCHACHT allein daran, ohne Positivbeispiel gibt es keinen Schwellwert
# (Randmessung und Owner-Frage: docs/SLICES_K1_K4.md, K2).
_BELEG_TEXT_RX = re.compile(
    r"(?<![A-ZÄÖÜ])(?:F?BDB|DDB|DBA|SCHACHT)(?![A-ZÄÖÜ])|DURCHBRUCH")
_BELEG_TEXT_MM = 500.0
# Keil = HATCH FEUERFESTER_STEIN (Rennweg HKLS). Er belegt den Schacht, den er
# markiert: den Kasten (geschlossene Polylinie ≤ 3 m², die ihn enthält). Die
# Fläche muss zu mindestens der Hälfte in solchen Kästen liegen — gemessen
# Rennweg: DBA-/Installationsschächte 0,65–0,99, Fensternische DG2 `rest_5`
# 0,18 (der Kasten „Schachtverzug über Dach" streift sie nur).
_KEIL_MUSTER = "FEUERFESTER_STEIN"
_KASTEN_TOL_MM = 20.0
_KASTEN_ANTEIL = 0.5
_SCHACHT_LAYER_RX = re.compile(r"SCHACHT", re.IGNORECASE)


@dataclass
class _Belege:
    """Schacht-Belege eines Plans (mm): Textpunkte, Kasten-Union, Layer-Punkte."""

    texte: list[XY] = field(default_factory=list)
    kaesten: BaseGeometry = field(default_factory=Polygon)
    layer_punkte: list[XY] = field(default_factory=list)


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


def _schacht_text_punkte(plan: DxfPlan | None) -> list[XY]:
    """Einfügepunkte der Schacht-Beschriftungen (mm) — Planzeichen-Evidenz."""
    out: list[XY] = []
    if plan is None:
        return out
    for e in plan.space:
        t = e.dxftype()
        if t == "MTEXT":
            txt = e.plain_text()
        elif t == "TEXT":
            txt = e.dxf.text
        else:
            continue
        s = " ".join(str(txt).upper().split())
        if _SCHACHT_TEXT_RX.search(s) and not _SCHACHT_AUSSCHLUSS_RX.search(s):
            out.append(plan._scale(e.dxf.insert))
    return out


def _schacht_belege(plan: DxfPlan | None) -> _Belege:
    """Beleg-Kandidaten der Owner-Regel a (Slice K2) aus dem Plan, in mm."""
    b = _Belege()
    if plan is None:
        return b
    keile: list[Polygon] = []
    polylinien: list[Polygon] = []
    for e in plan.space:
        t = e.dxftype()
        if t in ("TEXT", "MTEXT"):
            s = " ".join(str(e.plain_text() if t == "MTEXT" else e.dxf.text).upper().split())
            if _BELEG_TEXT_RX.search(s) and not _SCHACHT_AUSSCHLUSS_RX.search(s):
                b.texte.append(plan._scale(e.dxf.insert))
            continue
        if t == "HATCH" and str(e.dxf.pattern_name or "").upper() == _KEIL_MUSTER:
            pts = [plan._scale(p) for p in _hatch_punkte(e)]
            if len(pts) >= 3 and not (k := Polygon(pts).buffer(0)).is_empty:
                keile.append(k)
        elif t in ("LWPOLYLINE", "POLYLINE") and getattr(e, "closed", False):
            pts = plan.entity_points(e)
            if len(pts) >= 3:
                p = Polygon(pts).buffer(0)
                if 0 < p.area <= _SCHACHT_MAX_M2 * 1e6:
                    polylinien.append(p)
        if _SCHACHT_LAYER_RX.search(str(e.dxf.layer)) and (pts := plan.entity_points(e)):
            b.layer_punkte.append((sum(x for x, _ in pts) / len(pts),
                                   sum(y for _, y in pts) / len(pts)))
    if keile:
        b.kaesten = unary_union([p for p in polylinien
                                 if any(p.buffer(_KASTEN_TOL_MM).covers(k) for k in keile)])
    return b


def _hat_beleg(shp: Polygon, b: _Belege) -> bool:
    """Owner-Regel a: Text in 500 mm, Keil-Kasten über die halbe Fläche, Schacht-Layer."""
    return (any(shp.distance(Point(p)) <= _BELEG_TEXT_MM for p in b.texte)
            or (not b.kaesten.is_empty
                and shp.intersection(b.kaesten).area >= _KASTEN_ANTEIL * shp.area)
            or any(shp.covers(Point(p)) for p in b.layer_punkte))


def _typisiere(shp: Polygon, tueren: list[TuerOeffnung],
               stiegen: list[XY], sto: list[XY],
               schacht_texte: Sequence[XY] = (),
               belege: _Belege | None = None) -> tuple[str, bool, bool]:
    """Typ-Regeln (s. Modul-Doc) → (raum_typ, ist_fluchtweg, ist_communal)."""
    # Diagnose Rennweg U2, Slice S3a: Planzeichen schlägt den Treppenmarker —
    # das Bbox-Zentrum der U-Treppe um den Lift liegt IM Schacht, damit wurde
    # der beschriftete DBA-Schacht (DG2 `rest_2`) zum STIEGENHAUS.
    if shp.area < _SCHACHT_MAX_M2 * 1e6 and any(
            shp.covers(Point(p)) for p in (*schacht_texte, *sto)):
        return "SCHACHT", False, False
    if any(shp.distance(Point(p)) <= _MARKER_NAEHE_MM for p in stiegen):
        return "STIEGENHAUS", True, True
    tuer_n = sum(1 for t in tueren
                 if shp.distance(Point(t.xy_mm)) <= _TUER_RAND_MM)
    if _kurzseite(shp) < _GANG_BREITE_MAX_MM and tuer_n >= _GANG_MIN_TUEREN:
        return "GANG", True, True
    # STO im Polygon hat schon die erste Regel gefangen — hier bleibt „türlos".
    # Slice K2: ohne Schacht-Beleg ist die türlose Kleinfläche eine NISCHE
    # (Nutzungsklasse None, also fail-safe kein KEIN_RAUM).
    if shp.area < _SCHACHT_MAX_M2 * 1e6 and tuer_n == 0:
        if _hat_beleg(shp, belege or _Belege()):
            return "SCHACHT", False, False
        return "NISCHE", False, False
    # Leerer raum_typ = untypisiert — „UNBEKANNT" ist KEIN Typ (VOKABULAR.md §1).
    return "", False, False


def komponenten_ohne_stempel(
    plan: DxfPlan | None,
    wandkoerper: list[Wandkoerper],
    tueren: list[TuerOeffnung],
    bereits_belegte_polygone: list[list[XY]],
    raster_mm: float = 50.0,
) -> list[Raum]:
    """Restflächen (Außenkontur − Wände − belegte Räume) als Räume, Quelle 'REST'.

    ``plan`` liefert nur die Typ-Marker (Stiegen-/Lift-Blöcke, STO-Kästchen,
    Schacht-Texte) — ``None`` ist erlaubt, dann typt nur die Geometrie-Regel.
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
    siegel = np.zeros((h, w), dtype=bool)
    for t in tueren:
        r_px = max(1, round(max(_TUER_RAND_MM, t.breite_mm or 0.0) / res))
        rr, cc = raster.px(t.xy_mm)
        d = disk(r_px, dtype=bool)
        r0, c0 = rr - r_px, cc - r_px
        rs = slice(max(r0, 0), min(r0 + d.shape[0], h))
        cs = slice(max(c0, 0), min(c0 + d.shape[1], w))
        siegel[rs, cs] |= d[rs.start - r0:rs.stop - r0, cs.start - c0:cs.stop - c0]
    blockiert |= siegel
    belegt = np.zeros((h, w), dtype=bool)
    for poly in bereits_belegte_polygone:
        if len(poly) < 3:
            continue
        shp = Polygon(poly).buffer(_BELEGT_PUFFER_MM)
        if not shp.is_empty:
            _fuelle(blockiert, shp, raster)
            _fuelle(belegt, shp, raster)

    stiegen, sto = _marker_punkte(plan)
    schacht_texte = _schacht_text_punkte(plan)
    belege = _schacht_belege(plan)
    grenze = union.boundary if not union.is_empty else None
    frei = ~blockiert
    labels = label(frei)
    # Slice S3b (docs/GATE_TUERSTAPEL.md § 7): die Türscheiben geodätisch
    # zurückdehnen wie stempel_flutung.masken — nur Zellen, die allein die
    # Scheibe sperrt (nie Wand, Freiland, belegter Raum), Watershed auf
    # konstantem Relief mit ALLEN Labels als Markern, damit sich zwei
    # Restflächen an derselben Tür an der Türlinie treffen. Ohne das endeten
    # die Konturen r mm vor der Tür (Rennweg OG3: `seite_fehlt` an 7 Blocktüren).
    # Keine Lochfüllung: `_vektorisiere` nimmt ohnehin die Außenkontur; die
    # Füllung wirkte nur an Diagonal-Engstellen und zog dort Wandzellen als
    # Brücke ein (Rennweg DG2: Schacht-Lappen 1,85 m² an `rest_1`).
    siegel &= innen & ~wand & ~belegt
    if siegel.any() and labels.max():
        labels = watershed(np.zeros(labels.shape, dtype=np.uint8), markers=labels,
                           mask=frei | siegel)
    out: list[Raum] = []
    for lbl in range(1, int(labels.max()) + 1):
        m = labels == lbl
        # _MIN_M2 erst NACH der Rückdehnung (vorher fielen Kleinräume hinter
        # einer Tür weg, deren erodierter Kern < 1 m² war).
        if m.sum() * res * res < _MIN_M2 * 1e6:
            continue
        shp = _vektorisiere(m, raster, grenze)
        if shp.is_empty or shp.area < _MIN_M2 * 1e6:
            continue
        typ, flucht, communal = _typisiere(shp, tueren, stiegen, sto, schacht_texte, belege)
        out.append(Raum(
            id=f"rest_{len(out) + 1}",
            raum_typ=typ,
            polygon_mm=[(float(x), float(y)) for x, y in shp.exterior.coords[:-1]],
            flaeche_m2=shp.area / 1e6,
            ist_fluchtweg=flucht,
            ist_communal=communal,
        ))
    return out
