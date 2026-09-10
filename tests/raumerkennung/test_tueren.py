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


# ── Beschriftungs-Fahnen sind keine Türen (Muthgasse-Regression) ────────────

# echter Blockname aus Muthgasse_E2 (83 INSERTs, Blockdef = 1× LINE)
FAHNE = ("HNP_Beschriftung Türen - AF 50 - Durchgangslichte_ Nummer_ "
         "Brandschutz_ STUK oben Projekt-12188994-1")
# echter Blockname aus Muthgasse_E2 (Türblatt, Blockdef trägt ARC r=900)
ECHT = "HNP_T_BZ_1-DF - HNP_T32_BZ-S_H_EI230_1DF_90x200 WET-16703914-1"


def test_ist_tuer_block_grenze_beschriftungsfahne():
    """Regex-Grenze in beide Richtungen: die Fahne fällt, das Türblatt bleibt."""
    from notbeleuchtung.raumerkennung.tueren import _ist_tuer_block

    assert _ist_tuer_block(FAHNE) is False
    assert _ist_tuer_block(ECHT) is True


def test_beschriftungsfahne_wird_verworfen_und_gezaehlt(tmp_path):
    """Beide Einstiege (``tueren_aus_dxf`` UND ``tuer_oeffnungen``) müssen die
    Fahne verwerfen — sie hat keine Türgeometrie, nur eine Führungslinie."""
    from notbeleuchtung.raumerkennung import tueren as T

    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4  # mm
    msp = doc.modelspace()
    doc.layers.add("02-TWA-G00-LEG-M0")
    W = "02-TWA-G00-LEG-M0"
    corners = [(0, 0), (18000, 0), (18000, 12000), (0, 12000)]
    for i in range(4):
        msp.add_line(corners[i], corners[(i + 1) % 4], dxfattribs={"layer": W})
    # Fahne: Führungslinie, kein Türblatt
    fahne = doc.blocks.new(name=FAHNE)
    fahne.add_line((0, 0), (0, 1200))
    msp.add_blockref(FAHNE, (4000, 6000))
    # echtes Türblatt: Schwenkbogen r=900 in der Blockdefinition
    echt = doc.blocks.new(name=ECHT)
    echt.add_arc((0, 0), 900, 0, 90)
    msp.add_blockref(ECHT, (9000, 6000))
    p = tmp_path / "fahne.dxf"
    doc.saveas(str(p))

    plan = lade_dxf(p)
    T._verworfene_bloecke.clear()
    tueren = tueren_aus_dxf(plan)
    assert [t.xy_mm for t in tueren] == [(9000.0, 6000.0)], (
        f"Fahne nicht verworfen: {[(t.id, t.xy_mm) for t in tueren]}"
    )
    # der Ausschluss ist nachvollziehbar, nicht stillschweigend
    assert T._verworfene_bloecke.get(FAHNE) == 1

    # zweiter Einstieg: keine Phantom-TuerOeffnung an der Fahnen-Position
    oeff = T.tuer_oeffnungen(plan)
    assert [round(o.xy_mm[0]) for o in oeff] == [9000], (
        f"Fahne als TuerOeffnung durchgekommen: {oeff}"
    )
