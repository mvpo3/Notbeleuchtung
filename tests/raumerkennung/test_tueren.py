"""S4 — tueren: TÜR-Blöcke → Tuer."""
from __future__ import annotations

import math

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
    # Innentüren tragen plausible Nennbreiten aus dem Blocknamen; ohne Zahl im
    # Namen (WET/…) ist die Breite None mit Grund (v1.4.0, nie 0.0/Default).
    innen = [t for t in tueren if not t.ist_notausgang]
    assert all(600.0 <= t.breite_mm <= 1300.0 for t in innen
               if t.breite_mm is not None)
    assert all(t.breite_quelle == "BLOCKNAME" for t in innen
               if t.breite_mm is not None)
    assert all(t.breite_quelle == "UNBEKANNT" and t.breite_grund
               for t in innen if t.breite_mm is None)


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


# ── v1.4.0: keine Messung ist None mit Quelle/Grund, nie 0.0 ────────────────

def test_keine_messung_ist_none_mit_quelle_und_grund(tmp_path):
    """Ein Öffnungs-Marker trägt eine ID, keine Breite → None + UNBEKANNT.

    Gegenprobe im selben Plan: eine benannte Tür trägt ihr Nennmaß mit
    breite_quelle="BLOCKNAME". Der Code darf nirgends ein Maß erfinden —
    kein Default, kein Normwert, kein Mittelwert.
    """
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    for name in ("TÜR-90", "Öffnung_81"):
        blk = doc.blocks.new(name=name)
        blk.add_line((0, 0), (900, 0))
    msp.add_blockref("TÜR-90", (4000, 4000))
    msp.add_blockref("Öffnung_81", (8000, 4000))
    p = tmp_path / "none.dxf"
    doc.saveas(str(p))

    tueren = tueren_aus_dxf(lade_dxf(p))
    assert len(tueren) == 2
    gemessen = [t for t in tueren if t.breite_mm is not None]
    ohne = [t for t in tueren if t.breite_mm is None]
    assert len(gemessen) == len(ohne) == 1
    assert gemessen[0].breite_mm == 900.0
    assert gemessen[0].breite_quelle == "BLOCKNAME"
    assert gemessen[0].breite_grund is None
    assert ohne[0].breite_quelle == "UNBEKANNT"
    assert ohne[0].breite_grund                      # Grund ist Pflicht
    assert ohne[0].lichte_mm is None                 # nie abgeleitet


# ── S4a: ArchiCAD-Weltkoordinaten-Türblöcke (Diagnose U12) ──────────────────

def _archicad_weltkoordinaten_dxf(pfad):
    """Rennweg-Muster: Türblock VERSCHACHTELT im Wand-Block, Blockinhalte in
    WELT-Koordinaten, ``base_point`` ≈ INSERT-Punkt (Translation 0) — der
    INSERT-Punkt liegt dadurch weit außerhalb des Planbereichs, die Tür-
    Geometrie aber mittendrin.

    Am echten Plan gemessen (OG1, 7 Zargentüren): der Schwenkbogen sitzt am
    Scharnier; die ÖFFNUNG ist als geschlossenes Türblatt-Rechteck LÄNGS der
    Wand gezeichnet (zwei blattlange Linien), die offene Blattstellung als
    EINE Linie quer dazu. Die Wandseite ist also der ARC-Endpunkt mit den
    MEISTEN blattlangen Segmenten am Scharnier.
    """
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4  # mm
    msp = doc.modelspace()
    W = "02-TWA-G00-LEG-M0"
    if W not in doc.layers:
        doc.layers.add(W)
    # 12 Wandlinien im Modelspace: ≥ 10 → kein Wrapper-Mode; 20 m Spanne → Faktor 1.0
    ecken = [(0, 0), (20000, 0), (20000, 12000), (0, 12000)]
    for i in range(4):
        a, b = ecken[i], ecken[(i + 1) % 4]
        for j in range(3):
            p0 = (a[0] + (b[0] - a[0]) * j / 3, a[1] + (b[1] - a[1]) * j / 3)
            p1 = (a[0] + (b[0] - a[0]) * (j + 1) / 3, a[1] + (b[1] - a[1]) * (j + 1) / 3)
            msp.add_line(p0, p1, dxfattribs={"layer": W})
    anker = (900000.0, 900000.0)
    tuer = doc.blocks.new("Zargentür_1_Fl 10[1]", base_point=anker)
    tuer.add_arc((5000, 3000), 840, 0, 90)          # Schwenkbogen, Sweep 90°
    tuer.add_line((5000, 3000), (5840, 3000))       # Blatt geschlossen → Wandseite
    tuer.add_line((5000, 2960), (5840, 2960))       # Blattrücken (40 mm Blattdicke)
    tuer.add_line((5000, 3000), (5000, 3840))       # Blatt offen → Blattspitze
    wand = doc.blocks.new("Wall_1", base_point=anker)
    wand.add_line((0, 2900), (10000, 2900), dxfattribs={"layer": W})
    wand.add_line((0, 3100), (10000, 3100), dxfattribs={"layer": W})
    wand.add_blockref("Zargentür_1_Fl 10[1]", anker)
    msp.add_blockref("Wall_1", anker)
    doc.saveas(str(pfad))
    return pfad


def test_weltkoordinaten_tuerblock_liegt_an_der_geometrie(tmp_path):
    """Der Türblock wird an seiner GEOMETRIE verortet, nicht am INSERT-Punkt.

    Ohne ``planbereich`` bleibt alles wie bisher (Familien mit INSERT an der
    Tür dürfen sich nicht ändern) — die Geometrie-Lage greift nur, wenn der
    INSERT-Punkt außerhalb des Planbereichs liegt.
    """
    from notbeleuchtung.hauptengine.contracts.raum_modell import BBox
    from notbeleuchtung.raumerkennung.tueren import im_planbereich, tuer_oeffnungen

    plan = lade_dxf(_archicad_weltkoordinaten_dxf(tmp_path / "welt.dxf"))
    assert plan.factor == 1.0
    bereich = BBox(min_xy=(0.0, 0.0), max_xy=(10000.0, 8000.0))

    oeff = [o for o in tuer_oeffnungen(plan, bereich) if o.quelle == "block"]
    assert len(oeff) == 1, oeff
    o = oeff[0]
    assert math.dist(o.xy_mm, (5420.0, 3000.0)) <= 5.0, o.xy_mm
    rest = o.winkel_grad % 180.0
    assert min(rest, 180.0 - rest) <= 2.0, o.winkel_grad
    assert o.breite_mm == 840.0
    assert o.breite_quelle == "GEOMETRIE_SCHWENKRADIUS"
    assert o.wand_block == "Wall_1"
    assert im_planbereich([o], bereich) == [o]

    # Gegenprobe: ohne planbereich unverändert der INSERT-Punkt
    ohne = [x for x in tuer_oeffnungen(plan) if x.quelle == "block"]
    assert [x.xy_mm for x in ohne] == [(900000.0, 900000.0)]
