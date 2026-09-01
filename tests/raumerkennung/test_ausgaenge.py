"""S6 — ausgaenge: die Familien-Kaskade Stufe für Stufe.

Jede Stufe bekommt einen eigenen Synth-Plan (Bauweise wie ``conftest.build_synth_dxf``,
mind. 20x12 m wegen der Skala-Kalibrierung), der genau das Zeichen-Muster dieser
Stufe trägt und die spezifischeren Stufen bewusst leer lässt.
"""
from __future__ import annotations

import ezdxf
import pytest

from notbeleuchtung.raumerkennung.ausgaenge import ausgaenge_ermitteln
from notbeleuchtung.raumerkennung.dxf_load import bounds_mm, lade_dxf
from notbeleuchtung.raumerkennung.tueren import tueren_aus_dxf

WAND = "02-TWA-G00-LEG-M0"


def _huelle(tmp_path, name: str):
    """Leeres 20x12-m-Gebäude (nur Außenwände) — Basis für jede Kaskaden-Stufe."""
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4  # mm
    msp = doc.modelspace()
    doc.layers.add(WAND)
    ecken = [(0, 0), (20000, 0), (20000, 12000), (0, 12000)]
    for i in range(4):
        msp.add_line(ecken[i], ecken[(i + 1) % 4], dxfattribs={"layer": WAND})
    return doc, msp, tmp_path / name


def _ausgaenge(pfad):
    plan = lade_dxf(pfad)
    return ausgaenge_ermitteln(plan, tueren_aus_dxf(plan), bounds_mm(plan))


def test_stufe1_doppeltuer_am_rand_ist_final_exit(tmp_path):
    doc, msp, p = _huelle(tmp_path, "stufe1.dxf")
    # Doppeltür in der Außenwand: zwei Schwenkbögen r=900, Drehpunkte 1800 mm auseinander.
    msp.add_arc((9100, 0), 900, 0, 90)
    msp.add_arc((10900, 0), 900, 90, 180)
    doc.saveas(str(p))

    ausgaenge = _ausgaenge(p)
    assert len(ausgaenge) >= 1
    assert any(a.typ == "final_exit" for a in ausgaenge)


def test_stufe3_stiegenhaus_ist_stair_exit(tmp_path):
    doc, msp, p = _huelle(tmp_path, "stufe3.dxf")
    # Treppen-Block (Stufenlinien in der Block-Definition, damit die Extents greifen).
    blk = doc.blocks.new("STIEGE")
    for i in range(6):
        blk.add_line((0, i * 300), (2000, i * 300))
    msp.add_blockref("STIEGE", (3000, 3000))
    # Eine gewöhnliche Tür am Stiegenhaus — keine Doppeltür, keine Außentür.
    msp.add_arc((4000, 4000), 900, 0, 90)
    doc.saveas(str(p))

    ausgaenge = _ausgaenge(p)
    assert len(ausgaenge) >= 1
    assert all(a.typ == "stair_exit" for a in ausgaenge)


def test_stufe4_einzeltuer_am_rand_ist_door(tmp_path):
    doc, msp, p = _huelle(tmp_path, "stufe4.dxf")
    # Nur eine gewöhnliche Tür in der Außenwand: kein Paar, kein Außentür-Block,
    # kein Stiegenhaus → Fallback-Stufe.
    msp.add_arc((10000, 0), 900, 0, 90)
    doc.saveas(str(p))

    ausgaenge = _ausgaenge(p)
    assert len(ausgaenge) == 1
    assert ausgaenge[0].typ == "door"


def test_stufe2_aussentuer_am_rand_ist_final_exit(tmp_path):
    """Stufe 2 wird über ``_aussentueren_am_rand`` direkt geprüft.

    Grund: der Außentür-Block (``WET_…``) liefert im Synth-Plan zwar eine Tür mit
    ``ist_notausgang=True``, aber die Kaskade erreicht Stufe 2 nur, wenn Stufe 1
    leer bleibt — und ein Plan ohne jeden Schwenkbogen hat auch keine belastbare
    Tür-Geometrie mehr. Die Hilfsfunktion mit echtem ``Umriss`` ist die
    aussagekräftigere Prüfung.
    """
    from notbeleuchtung.hauptengine.contracts.raum_modell import Tuer
    from notbeleuchtung.raumerkennung.ausgaenge import _aussentueren_am_rand
    from notbeleuchtung.raumerkennung.footprint import gebaeude_umriss

    doc, _msp, p = _huelle(tmp_path, "stufe2.dxf")
    doc.saveas(str(p))
    plan = lade_dxf(p)
    umriss = gebaeude_umriss(plan, bounds_mm(plan))
    assert umriss is not None

    aussen = Tuer(id="tuer_1", xy_mm=(10000.0, 0.0), breite_mm=1000.0, ist_notausgang=True)
    innen = Tuer(id="tuer_2", xy_mm=(10000.0, 6000.0), breite_mm=800.0, ist_notausgang=True)
    normal = Tuer(id="tuer_3", xy_mm=(10000.0, 0.0), breite_mm=800.0, ist_notausgang=False)

    treffer = _aussentueren_am_rand([aussen, innen, normal], umriss)
    assert treffer == [aussen.xy_mm]


def test_huelle_ohne_tueren_liefert_keine_ausgaenge(tmp_path):
    """Keine Stufe greift → leere Liste (statt eines erfundenen Ausgangs)."""
    doc, _msp, p = _huelle(tmp_path, "ohne_tueren.dxf")
    doc.saveas(str(p))
    plan = lade_dxf(p)
    assert ausgaenge_ermitteln(plan, [], bounds_mm(plan)) == []


@pytest.mark.parametrize("typ", ["final_exit", "stair_exit", "door"])
def test_kaskade_kennt_nur_diese_typen(typ):
    from notbeleuchtung.raumerkennung.ausgaenge import _als_ausgaenge

    (a,) = _als_ausgaenge([(1.0, 2.0)], typ)
    assert a.typ == typ and a.xy_mm == (1.0, 2.0)
