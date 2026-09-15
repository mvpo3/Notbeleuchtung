"""Tests rest_komponenten — synthetische Wandkörper, keine DXF-Datei nötig.

Die Typ-Marker (Treppen-Insert, Schacht-Text, STO-Kästchen) kommen aus einem
In-Memory-``DxfPlan`` (factor 1.0 → Plan-Koordinaten sind mm).
"""
from __future__ import annotations

import ezdxf
from shapely.geometry import Point, Polygon

from notbeleuchtung.raumerkennung.dxf_load import XY, DxfPlan
from notbeleuchtung.raumerkennung.rest_komponenten import komponenten_ohne_stempel
from notbeleuchtung.raumerkennung.tueren import TuerOeffnung
from notbeleuchtung.raumerkennung.wandkoerper import Wandkoerper


def _wk(x0: float, y0: float, x1: float, y1: float) -> Wandkoerper:
    return Wandkoerper(polygon_mm=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                       material="STAHLBETON", layer="wand", quelle="msp",
                       breite_mm=min(x1 - x0, y1 - y0))


# 8×4-m-Box, Trennwand bei x≈4 m mit 0.9-m-Türöffnung, kleine türlose
# Schacht-Box im rechten Raum. Linker Raum ist „belegt".
_WAENDE = [
    _wk(0, 0, 8000, 200), _wk(0, 3800, 8000, 4000),
    _wk(0, 0, 200, 4000), _wk(7800, 0, 8000, 4000),
    _wk(3900, 200, 4100, 1500), _wk(3900, 2400, 4100, 3800),
    _wk(5500, 1500, 7100, 1600), _wk(5500, 2900, 7100, 3000),
    _wk(5500, 1500, 5600, 3000), _wk(7000, 1500, 7100, 3000),
]
_TUER = TuerOeffnung(xy_mm=(4000.0, 1950.0), breite_mm=900.0,
                     winkel_grad=None, quelle="block")
_LINKS = [(200.0, 200.0), (3900.0, 200.0), (3900.0, 3800.0), (200.0, 3800.0)]

# S3a-Layout: wie oben, aber die Schacht-Box misst innen 1.4 × 0.9 m (≈1.2 m²,
# Muster Rennweg DG2 `rest_2` mit 1,16 m²).
_WAENDE_S3A = _WAENDE[:6] + [
    _wk(5500, 1500, 7100, 1600), _wk(5500, 2500, 7100, 2600),
    _wk(5500, 1500, 5600, 2600), _wk(7000, 1500, 7100, 2600),
]
_SCHACHT_MITTE: XY = (6300.0, 2050.0)      # Mitte der Schacht-Box
_IM_GROSSEN_REST: XY = (4500.0, 3000.0)    # im rechten Raum, außerhalb der Box


def _plan(texte: list[tuple[str, XY]] | None = None,
          stiegen: list[XY] | None = None, sto: list[XY] | None = None) -> DxfPlan:
    """In-Memory-Plan mit den Typ-Markern (Wände kommen als ``Wandkoerper``)."""
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    for txt, xy in texte or []:
        msp.add_text(txt, dxfattribs={"insert": xy})
    if stiegen:
        doc.blocks.new("STIEGE_1")
        for xy in stiegen:
            msp.add_blockref("STIEGE_1", xy)
    if sto:
        doc.layers.add("04-STO")
        for x, y in sto:
            msp.add_lwpolyline([(x - 100, y - 100), (x + 100, y - 100),
                                (x + 100, y + 100), (x - 100, y + 100)],
                               close=True, dxfattribs={"layer": "04-STO"})
    return DxfPlan(doc=doc, space=msp, factor=1.0)


def _klein(raeume):
    return min(raeume, key=lambda r: r.flaeche_m2)


def test_rest_findet_rechten_raum_und_schacht():
    raeume = komponenten_ohne_stempel(None, _WAENDE, [_TUER], [_LINKS])
    typen = sorted(r.raum_typ for r in raeume)
    assert "SCHACHT" in typen                      # türlose Kleinfläche
    gross = max(raeume, key=lambda r: r.flaeche_m2)
    assert gross.raum_typ == ""                    # untypisiert, kein "UNBEKANNT"
    assert 8.0 <= gross.flaeche_m2 <= 14.0         # rechter Raum minus Schacht-Box
    # Belegter linker Raum liefert KEINE Rest-Komponente.
    links = Polygon(_LINKS)
    assert not any(links.covers(Point(*r.polygon_mm[0])) and links.covers(
        Polygon(r.polygon_mm).centroid) for r in raeume)
    assert all(r.id.startswith("rest_") for r in raeume)


def test_ohne_waende_leer():
    assert komponenten_ohne_stempel(None, [], [], []) == []


# --- S3a: Schacht-Evidenz vor der Treppenmarker-Regel (Diagnose Rennweg U2) ---

def test_schacht_text_schlaegt_treppenmarker():
    """DG2 `rest_2`: „DBA SCHACHT" im Polygon, Treppenmarker 700 mm daneben."""
    plan = _plan(texte=[("DBA SCHACHT", _SCHACHT_MITTE)], stiegen=[(7700.0, 2050.0)])
    klein = _klein(komponenten_ohne_stempel(plan, _WAENDE_S3A, [_TUER], [_LINKS]))
    assert klein.flaeche_m2 < 3.0
    assert klein.raum_typ == "SCHACHT"


def test_sto_kaestchen_schlaegt_treppenmarker():
    """Zweiter Evidenz-Zweig: STO-Kästchen im Polygon, Marker mitten drin."""
    plan = _plan(stiegen=[_SCHACHT_MITTE], sto=[_SCHACHT_MITTE])
    klein = _klein(komponenten_ohne_stempel(plan, _WAENDE_S3A, [_TUER], [_LINKS]))
    assert klein.raum_typ == "SCHACHT"


def test_tuerlose_kleinflaeche_am_marker_bleibt_stiegenhaus():
    """Ohne Planzeichen bleibt die Markerregel vorn (Liftringe; S3b/F4 offen)."""
    plan = _plan(stiegen=[_SCHACHT_MITTE])
    klein = _klein(komponenten_ohne_stempel(plan, _WAENDE_S3A, [_TUER], [_LINKS]))
    assert klein.flaeche_m2 < 3.0
    assert klein.raum_typ == "STIEGENHAUS"


def test_grosse_flaeche_mit_text_und_marker_bleibt_stiegenhaus():
    """Deckelung < 3 m²: der Treppenlauf bleibt STIEGENHAUS trotz Schacht-Text."""
    plan = _plan(texte=[("DBA SCHACHT", _IM_GROSSEN_REST)], stiegen=[_IM_GROSSEN_REST])
    raeume = komponenten_ohne_stempel(plan, _WAENDE_S3A, [_TUER], [_LINKS])
    gross = max(raeume, key=lambda r: r.flaeche_m2)
    assert gross.flaeche_m2 >= 3.0
    assert gross.raum_typ == "STIEGENHAUS"


def test_text_ohne_schacht_wortgrenze_ist_keine_evidenz():
    """Negativ: „DBA" allein, „DBA Raum" und „Schachtverzug" sind kein Planzeichen."""
    plan = _plan(texte=[("DBA", _SCHACHT_MITTE), ("DBA Raum", _SCHACHT_MITTE),
                        ("Schachtverzug im Zimmer", _SCHACHT_MITTE)],
                 stiegen=[_SCHACHT_MITTE])
    klein = _klein(komponenten_ohne_stempel(plan, _WAENDE_S3A, [_TUER], [_LINKS]))
    assert klein.raum_typ == "STIEGENHAUS"
