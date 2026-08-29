"""S4 — tueren: TÜR-Blöcke → Tuer."""
from __future__ import annotations

import ezdxf

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.tueren import tueren_aus_dxf


def test_synth_eine_tuer(synth_dxf):
    tueren = tueren_aus_dxf(lade_dxf(synth_dxf))
    assert len(tueren) == 1
    t = tueren[0]
    assert t.breite_mm == 800.0          # TÜR-80 → 800 mm
    assert t.xy_mm == (12000.0, 6000.0)
    assert t.ist_notausgang is False     # Innentür


def test_arc_fallback_ohne_tuerbloecke(tmp_path):
    # ArchiCAD-Stil: Türen nur als Schwenkbogen (kein Tür-Block) → ARC-Fallback.
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4  # mm
    msp = doc.modelspace()
    doc.layers.add("02-TWA-G00-LEG-M0")
    W = "02-TWA-G00-LEG-M0"
    corners = [(0, 0), (18000, 0), (18000, 12000), (0, 12000)]
    for i in range(4):
        msp.add_line(corners[i], corners[(i + 1) % 4], dxfattribs={"layer": W})
    # zwei Tür-Schwenkbögen (r=900), keine Tür-Blöcke
    msp.add_arc((5000, 6000), 900, 0, 90)
    msp.add_arc((10000, 6000), 900, 0, 90)
    p = tmp_path / "arc.dxf"
    doc.saveas(str(p))
    tueren = tueren_aus_dxf(lade_dxf(p))
    assert len(tueren) == 2
    assert all(t.breite_mm == 900.0 for t in tueren)  # Breite = Schwenkradius


def test_mollgasse_tueren(mollgasse_eg):
    tueren = tueren_aus_dxf(lade_dxf(mollgasse_eg))
    # EG hat mehrere Türen; Achsmarker/Türöffner sind ausgeschlossen.
    assert len(tueren) >= 10
    # Innentüren tragen plausible Nennbreiten; Außentüren (WET/…) ggf. 0.
    innen = [t for t in tueren if not t.ist_notausgang]
    assert all(600.0 <= t.breite_mm <= 1300.0 for t in innen)
