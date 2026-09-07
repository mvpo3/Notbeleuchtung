"""aussenbereich — Komponenten-Konturen, offene und geschlossene Außenflächen."""
from __future__ import annotations

import ezdxf
from shapely.geometry import Point
from shapely.ops import unary_union

from notbeleuchtung.raumerkennung.aussenbereich import (
    _SCHLIESS_MM,
    _wand_geschlossen,
    aussen_indizien,
    aussenkontur_komponenten,
    erkenne_aussenbereiche,
    grundstuecksgrenze,
    ueberdachungen,
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


def _wand_zu(koerper):
    return _wand_geschlossen(koerper, _SCHLIESS_MM)


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


def _grenz_plan(typ: str, gehsteig=None) -> DxfPlan:
    """Plan mit KATASTER-Layer: als geschlossene Polylinie oder nur als DIMENSION.

    Der DIMENSION-Fall bildet Rennweg_OG3 nach (Layer 'New_GRUNDSTÜCKSGRENZE'
    mit 103 DIMENSION und NULL Liniengeometrie) — dort darf kein Ring entstehen.
    """
    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    doc.layers.add("KATASTER-GRENZE")
    ecken = [(-5000, -5000), (35000, -5000), (35000, 35000), (-5000, 35000)]
    if typ == "polyline":
        msp.add_lwpolyline(ecken, close=True, dxfattribs={"layer": "KATASTER-GRENZE"})
    else:
        msp.add_aligned_dim(p1=ecken[0], p2=ecken[1], distance=1000,
                            dxfattribs={"layer": "KATASTER-GRENZE"})
    if gehsteig is not None:
        doc.layers.add("09-SYM-GEHSTEIG")
        msp.add_line(*gehsteig, dxfattribs={"layer": "09-SYM-GEHSTEIG"})
    return DxfPlan(doc=doc, space=msp, factor=1.0)


def test_grundstuecksgrenze_nur_mit_liniengeometrie():
    koerper = _ring(0, 0, 30000, 30000, d=5000.0)
    ring = grundstuecksgrenze(_grenz_plan("polyline"), _wand_zu(koerper))
    assert ring is not None and abs(ring.area - 40000 * 40000) < 1.0
    # Gleicher Layer, aber nur DIMENSION → Typ-Filter greift, kein Falschpositiv.
    assert grundstuecksgrenze(_grenz_plan("dimension"), _wand_zu(koerper)) is None


def test_hof_ohne_strassenkante_bleibt_geschlossen():
    """Hof am Grundstücksrand: erst die Straßenkante macht ihn zum Weg ins Freie.

    Barawitzka-Muster: nach Süden offener Hof, Grundstück reicht dort weiter;
    im Norden liegt die Straße, aber davor steht das Gebäude.
    """
    koerper = [_wk(0, 25000, 30000, 30000),          # Nordtrakt
               _wk(0, 0, 5000, 30000), _wk(25000, 0, 30000, 30000)]
    hof = Point(15000, 12000)

    def _plan(gehsteig_y=None) -> DxfPlan:
        doc = ezdxf.new()
        doc.header["$INSUNITS"] = 4
        msp = doc.modelspace()
        doc.layers.add("KATASTER-GRENZE")
        # Grundstück: im Norden bündig mit dem Gebäude, nach Süden 10 m Hof.
        msp.add_lwpolyline([(0, -10000), (30000, -10000), (30000, 30000),
                            (0, 30000)], close=True,
                           dxfattribs={"layer": "KATASTER-GRENZE"})
        if gehsteig_y is not None:
            doc.layers.add("09-SYM-GEHSTEIG")
            msp.add_line((0, gehsteig_y), (30000, gehsteig_y),
                         dxfattribs={"layer": "09-SYM-GEHSTEIG"})
        return DxfPlan(doc=doc, space=msp, factor=1.0)

    ab = erkenne_aussenbereiche(_plan(gehsteig_y=32000), koerper)
    assert any(p.covers(hof) for p in ab.geschlossen), "Straße im Norden verbaut"
    assert not any(p.covers(hof) for p in ab.offen)

    ab2 = erkenne_aussenbereiche(_plan(gehsteig_y=-12000), koerper)
    assert any(p.covers(hof) for p in ab2.offen), "Straßenkante im Süden nicht erkannt"


def _decke_plan(rechteck) -> DxfPlan:
    """Plan mit EINER geschlossenen Deckenfläche auf einem Decken-Layer."""
    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    doc.layers.add("0._EG PP_2_210 Decke")
    (x0, y0), (x1, y1) = rechteck
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True,
                       dxfattribs={"layer": "0._EG PP_2_210 Decke"})
    return DxfPlan(doc=doc, space=msp, factor=1.0)


def test_ueberdachung_nur_bei_nicht_flaechendeckendem_deckenlayer():
    """Flächendeckende Decke (Rennweg-Muster) → nichts; ein Deckenstück über
    der offenen Außenfläche zwischen zwei Trakten → eine Überdachung."""
    koerper = _ring(0, 0, 20000, 20000) + _ring(30000, 0, 50000, 20000)
    ab = erkenne_aussenbereiche(_leerer_plan(), koerper)
    gebaeude = unary_union(ab.komponenten)

    voll = _decke_plan(((0, 0), (50000, 20000)))     # deckt 100 % des Gebäudes
    assert ueberdachungen(voll, gebaeude, ab.offen) == []

    vordach = _decke_plan(((22000, 5000), (28000, 15000)))   # 6 × 10 m im Hof
    treffer = ueberdachungen(vordach, gebaeude, ab.offen)
    assert len(treffer) == 1
    assert abs(treffer[0].area / 1e6 - 60.0) < 0.1
