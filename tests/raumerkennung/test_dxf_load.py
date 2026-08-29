"""S1 — dxf_load: öffnen, Einheiten, bounds_mm."""
from __future__ import annotations

from notbeleuchtung.raumerkennung.dxf_load import bounds_mm, lade_dxf


def test_synth_bounds(synth_dxf):
    plan = lade_dxf(synth_dxf)
    assert plan.factor == 1.0  # mm
    bb = bounds_mm(plan)
    assert bb.min_xy == (0.0, 0.0)
    assert bb.max_xy == (8000.0, 5000.0)


def test_mollgasse_bounds_plausibel(mollgasse_eg):
    plan = lade_dxf(mollgasse_eg)
    assert plan.factor == 1.0  # Mollgasse ist mm
    bb = bounds_mm(plan)
    w = bb.max_xy[0] - bb.min_xy[0]
    h = bb.max_xy[1] - bb.min_xy[1]
    # Wohnhaus-Geschoss: einige Meter bis ~150 m Ausdehnung, in mm.
    assert 5_000 < w < 300_000
    assert 5_000 < h < 300_000
