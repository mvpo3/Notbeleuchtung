"""S2 — waende: Wände → Raum-Polygone + Fläche."""
from __future__ import annotations

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.waende import raeume_aus_waenden


def test_synth_zwei_raeume(synth_dxf):
    raeume = raeume_aus_waenden(lade_dxf(synth_dxf))
    assert len(raeume) == 2
    flaechen = sorted(r.flaeche_m2 for r in raeume)
    assert flaechen == [96.0, 144.0]  # rechter 8×12, linker 12×12 m
    for r in raeume:
        assert len(r.polygon_mm) >= 4
        assert r.raum_typ == ""  # Typ kommt in S3


def test_mollgasse_raeume_nonempty(mollgasse_eg):
    raeume = raeume_aus_waenden(lade_dxf(mollgasse_eg))
    assert len(raeume) > 0
    assert all(r.flaeche_m2 > 0 for r in raeume)
