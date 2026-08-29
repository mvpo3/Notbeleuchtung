"""S4 — tueren: TÜR-Blöcke → Tuer."""
from __future__ import annotations

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.tueren import ausgaenge_aus_dxf, tueren_aus_dxf


def test_synth_eine_tuer(synth_dxf):
    tueren = tueren_aus_dxf(lade_dxf(synth_dxf))
    assert len(tueren) == 1
    t = tueren[0]
    assert t.breite_mm == 800.0          # TÜR-80 → 800 mm
    assert t.xy_mm == (5000.0, 2500.0)
    assert t.ist_notausgang is False     # Innentür
    # Synth hat keine Außentür → kein Ausgang.
    assert ausgaenge_aus_dxf(lade_dxf(synth_dxf)) == []


def test_mollgasse_tueren(mollgasse_eg):
    tueren = tueren_aus_dxf(lade_dxf(mollgasse_eg))
    # EG hat mehrere Türen; Achsmarker/Türöffner sind ausgeschlossen.
    assert len(tueren) >= 10
    # Innentüren tragen plausible Nennbreiten; Außentüren (WET/…) ggf. 0.
    innen = [t for t in tueren if not t.ist_notausgang]
    assert all(600.0 <= t.breite_mm <= 1300.0 for t in innen)


def test_mollgasse_leer_ausgaenge_sind_aussentueren(mollgasse_blank_eg):
    # Ausgänge = Außen-/Eingangstüren (WET_AUSSEN, SCHIEBETÜR, Fenstertür).
    ausg = ausgaenge_aus_dxf(lade_dxf(mollgasse_blank_eg))
    assert len(ausg) >= 1
    assert all(a.typ == "final_exit" for a in ausg)
