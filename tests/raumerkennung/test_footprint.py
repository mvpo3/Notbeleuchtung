"""Raster-Umriss: Hauptausgänge = Perimeter-Türen an der Außenwand."""
from __future__ import annotations

from notbeleuchtung.raumerkennung.dxf_load import bounds_mm, lade_dxf
from notbeleuchtung.raumerkennung.footprint import (
    gebaeude_umriss,
    hauptausgaenge,
)


def test_synth_umriss_innen_aussen(synth_dxf):
    plan = lade_dxf(synth_dxf)
    umriss = gebaeude_umriss(plan, bounds_mm(plan))
    assert umriss is not None
    # Es gibt sowohl Außen- als auch Innenbereich.
    assert umriss.aussen.any()
    assert (~umriss.aussen).any()
    # Außenwand-Mittelpunkt liegt am Rand, die Innentür (Mitte) nicht.
    assert umriss.ist_am_rand((4000.0, 0.0)) is True      # Unterkante-Mitte
    assert umriss.ist_am_rand((2500.0, 2500.0)) is False  # Raum-Inneres


def test_mollgasse_leer_hauptausgaenge(mollgasse_blank_eg):
    plan = lade_dxf(mollgasse_blank_eg)
    ausg = hauptausgaenge(plan, bounds_mm(plan))
    # Wenige echte Hauptausgänge (Doppeltür am Rand), 1–2 je Gebäude/Stiegenhaus.
    assert 1 <= len(ausg) <= 6
    assert all(a.typ == "final_exit" for a in ausg)
