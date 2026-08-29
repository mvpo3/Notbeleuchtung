"""S4 — tueren: TÜR-Blöcke → Tuer."""
from __future__ import annotations

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.tueren import tueren_aus_dxf


def test_synth_eine_tuer(synth_dxf):
    tueren = tueren_aus_dxf(lade_dxf(synth_dxf))
    assert len(tueren) == 1
    t = tueren[0]
    assert t.breite_mm == 800.0          # TÜR-80 → 800 mm
    assert t.xy_mm == (5000.0, 2500.0)


def test_mollgasse_tueren(mollgasse_eg):
    tueren = tueren_aus_dxf(lade_dxf(mollgasse_eg))
    # EG hat mehrere Wohnungstüren; Achsmarker/Türöffner sind ausgeschlossen.
    assert len(tueren) >= 10
    assert all(600.0 <= t.breite_mm <= 1300.0 for t in tueren)  # plausible Nennmaße
