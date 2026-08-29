"""Raster-Umriss: Hauptausgänge = Perimeter-Türen an der Außenwand."""
from __future__ import annotations

from notbeleuchtung.raumerkennung.dxf_load import bounds_mm, lade_dxf
from notbeleuchtung.raumerkennung.footprint import (
    ausgaenge_aus_umriss,
    gebaeude_umriss,
)
from notbeleuchtung.raumerkennung.tueren import tueren_aus_dxf


def test_synth_umriss_innen_aussen(synth_dxf):
    plan = lade_dxf(synth_dxf)
    umriss = gebaeude_umriss(plan, bounds_mm(plan))
    assert umriss is not None
    # Es gibt sowohl Außen- als auch Innenbereich.
    assert umriss.aussen.any()
    assert (~umriss.aussen).any()
    # Die einzelne Innentür (Trennwand-Mitte) ist KEIN Perimeter.
    assert umriss.ist_perimeter((5000.0, 2500.0)) is False


def test_mollgasse_leer_hauptausgaenge(mollgasse_blank_eg):
    plan = lade_dxf(mollgasse_blank_eg)
    tueren = tueren_aus_dxf(plan)
    ausg = ausgaenge_aus_umriss(plan, tueren, bounds_mm(plan))
    # Wenige echte Hauptausgänge (Perimeter), nicht 44 Türen und nicht 11 Müll.
    assert 1 <= len(ausg) <= 10
    assert all(a.typ == "final_exit" for a in ausg)
    # Perimeter-Türen sind eine echte Teilmenge aller Türen.
    assert len(ausg) < len(tueren)
