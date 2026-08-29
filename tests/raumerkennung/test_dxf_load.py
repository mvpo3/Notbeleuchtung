"""S1 — dxf_load: öffnen, Einheiten, bounds_mm."""
from __future__ import annotations

from notbeleuchtung.raumerkennung.dxf_load import bounds_mm, lade_dxf


def test_synth_bounds(synth_dxf):
    plan = lade_dxf(synth_dxf)
    assert plan.factor == 1.0  # mm
    bb = bounds_mm(plan)
    assert bb.min_xy == (0.0, 0.0)
    assert bb.max_xy == (20000.0, 12000.0)


def test_mollgasse_fertig_ist_mm(mollgasse_eg):
    plan = lade_dxf(mollgasse_eg)
    assert plan.factor == 1.0  # fertiger Plan ist mm
    bb = bounds_mm(plan)
    assert 5_000 < bb.max_xy[0] - bb.min_xy[0] < 300_000


def test_mollgasse_leer_ist_meter_kalibriert(mollgasse_blank_eg):
    # Echter Input steht in Metern trotz $INSUNITS=4 → muss ×1000 kalibriert werden.
    plan = lade_dxf(mollgasse_blank_eg)
    assert plan.factor == 1000.0
    bb = bounds_mm(plan)
    # Nach Kalibrierung liegt die Ausdehnung im mm-Bereich eines Geschosses.
    assert 8_000 < bb.max_xy[0] - bb.min_xy[0] < 500_000
