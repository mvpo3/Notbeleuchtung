"""aussenbereich — Komponenten-Konturen, offene und geschlossene Außenflächen."""
from __future__ import annotations

import ezdxf
from shapely.geometry import Point

from notbeleuchtung.raumerkennung.aussenbereich import (
    aussen_indizien,
    aussenkontur_komponenten,
    erkenne_aussenbereiche,
)
from notbeleuchtung.raumerkennung.dxf_load import DxfPlan
from notbeleuchtung.raumerkennung.wandkoerper import Wandkoerper


def _wk(x0, y0, x1, y1) -> Wandkoerper:
    return Wandkoerper(
        polygon_mm=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
        material="STAHLBETON", layer="wand", quelle="msp", breite_mm=300.0)


def _ring(x0, y0, x1, y1, d=1500.0) -> list[Wandkoerper]:
    """Geschlossener Wand-Ring (4 Platten der Dicke d) um das Rechteck."""
    return [
        _wk(x0, y0, x1, y0 + d), _wk(x0, y1 - d, x1, y1),
        _wk(x0, y0, x0 + d, y1), _wk(x1 - d, y0, x1, y1),
    ]


def _leerer_plan(baum_xy=None, gruen_linie=None) -> DxfPlan:
    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    if baum_xy is not None:
        doc.blocks.new("BAUM_LAUB")
        doc.layers.add("20-AUS")
        msp.add_blockref("BAUM_LAUB", baum_xy, dxfattribs={"layer": "20-AUS"})
    if gruen_linie is not None:
        doc.layers.add("02-FIL-G00-LEG-GRÜN")
        msp.add_line(*gruen_linie, dxfattribs={"layer": "02-FIL-G00-LEG-GRÜN"})
    return DxfPlan(doc=doc, space=msp, factor=1.0)


def test_zwei_trakte_geben_zwei_komponenten_und_offenen_zwischenraum():
    koerper = _ring(0, 0, 20000, 20000) + _ring(30000, 0, 50000, 20000)
    komponenten = aussenkontur_komponenten(koerper)
    assert len(komponenten) == 2, "je Trakt eine Außenkontur (Barawitzka-Muster)"
    ab = erkenne_aussenbereiche(_leerer_plan(), koerper)
    zwischen = Point(25000, 10000)   # Fläche zwischen den Trakten, offen n. Rand
    assert any(p.covers(zwischen) for p in ab.offen), "Zwischenraum nicht AUSSEN"
    assert not ab.gedeckt().covers(zwischen)
    # Rauminneres bleibt gedeckt (kein AUSSEN):
    assert ab.gedeckt().covers(Point(10000, 10000))


def test_eingeschlossener_hof_mit_baum_ist_aussen_geschlossen():
    koerper = _ring(0, 0, 30000, 30000, d=5000.0)   # Hof 20×20 m, versiegelt
    hof = Point(15000, 15000)
    ab = erkenne_aussenbereiche(_leerer_plan(baum_xy=(15000, 15000)), koerper)
    assert any(p.covers(hof) for p in ab.geschlossen), "Hof nicht als geschlossen erkannt"
    assert not any(p.covers(hof) for p in ab.offen)
    # Geschlossener Hof zählt als gedeckt → Türen dorthin werden NICHT AUSSEN
    # (kein final_exit; offene Frage an Enis).
    assert ab.gedeckt().covers(hof)


def test_hof_ohne_indiz_bleibt_unklassifiziert():
    koerper = _ring(0, 0, 30000, 30000, d=5000.0)
    ab = erkenne_aussenbereiche(_leerer_plan(), koerper)
    assert not ab.geschlossen and not ab.offen or all(
        not p.covers(Point(15000, 15000)) for p in ab.geschlossen + ab.offen)


def test_aussen_indizien_baum_und_gruenlayer():
    plan = _leerer_plan(baum_xy=(1000, 2000),
                        gruen_linie=((0, 0), (5000, 0)))
    pts = aussen_indizien(plan)
    assert (1000.0, 2000.0) in pts
    assert (0.0, 0.0) in pts
