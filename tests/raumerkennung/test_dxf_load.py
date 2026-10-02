"""S1 — dxf_load: öffnen, Einheiten, bounds_mm."""
from __future__ import annotations

import pytest

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


def _plan_mit_wand_im_block(tmp_path, ausreisser=False):
    """DXF, dessen Wände NUR in einer Blockdefinition liegen (Baufeld-Muster).

    $INSUNITS=6 (Meter) lügt: die Zeichnung steht in mm. Ohne Block-Abstieg
    findet die Kalibrierung 0 Wandpunkte und fällt auf $INSUNITS zurück → ×1000.
    """
    import ezdxf

    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 6                      # behauptet Meter
    blk = doc.blocks.new("GRUNDRISS")
    for i in range(12):                              # 30 m × 20 m Wandrechteck
        blk.add_line((0, i * 1000), (30000, i * 1000),
                     dxfattribs={"layer": "A-WALL"})
    msp = doc.modelspace()
    # Baufeld-Muster: die INSERTs SELBST liegen auf dem Wand-Layer (damit der
    # Modelspace als Architektur-Raum gewählt wird), die Linien stecken aber
    # ausschließlich in der Blockdefinition.
    for k in range(12):
        msp.add_blockref("GRUNDRISS", (0, 0), dxfattribs={"layer": "A-WALL"})
        del k
    if ausreisser:
        # Zwei Phantom-Punkte 400 km daneben (Baufeld-4OG-Muster).
        msp.add_line((0, 0), (4e8, 4e8), dxfattribs={"layer": "A-WALL"})
    p = tmp_path / ("ausreisser.dxf" if ausreisser else "block.dxf")
    doc.saveas(p)
    return p


def test_wand_im_block_kalibriert_nicht_ueber_insunits(tmp_path):
    """Baufeld 1OG/2OG/4OG: Wände nur im Block → früher Faktor 1000 statt 1."""
    plan = lade_dxf(_plan_mit_wand_im_block(tmp_path))
    assert plan.factor == 1.0


def test_ausreisser_kippen_den_faktor_nicht(tmp_path):
    """Ein paar Phantom-Punkte dürfen die Dekaden-Wahl nicht verschieben."""
    plan = lade_dxf(_plan_mit_wand_im_block(tmp_path, ausreisser=True))
    assert plan.factor == 1.0


# ── Entscheid 7 (Owner 2026-10-01, D-04): Maßstab über die Tür ───────────────
# Greift der $INSUNITS-Rückfall oder widerspricht die Türprobe, kalibriert der Plan
# über die gemessenen Türschwenkbögen: Faktor = die Dekade, die den Median der
# Bögen MIT Tür-Beleg (Tür-Layer oder Tür-Block, Schwenk 60–120°) an die Regelbreite
# legt; zu wenige Türen oder zu große Streuung → „Maßstab unsicher" (LUECKEN § 28).
# Die Möbel-Bögen spiegeln die Lage auf Rennweg EG / Am Rain OG4/OG3/EG: 60–130
# Einheiten auf Möbel-Layern, mehr als Türen — die alte Türprobe zählte sie (Faktor 10).
def _tuer_plan(tmp_path, radien, layer="Türen", sweep=90.0, moebel=0, block=False):
    import ezdxf

    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    if block:                       # ein Tür-Block, je Radius ein INSERT (Layer „0")
        doc.blocks.new("TÜR-90").add_arc((0, 0), radien[0], 0, sweep)
    for i, r in enumerate(radien):
        if block:
            msp.add_blockref("TÜR-90", (5000 * i, 0))
        else:
            msp.add_arc((5000 * i, 0), r, 0, sweep, dxfattribs={"layer": layer})
    for i in range(moebel):
        msp.add_arc((700 * i, 9000), 60 + 3 * i, 0, 90, dxfattribs={"layer": "Möblierung"})
    p = tmp_path / "tuer.dxf"
    doc.saveas(p)
    return p


@pytest.mark.parametrize(("radien", "kw", "faktor"), [
    ([900, 900, 840], {"moebel": 20}, 1.0),          # mm, Möbel-Bögen zählen nicht
    ([90, 90, 84], {}, 10.0),                         # cm
    ([0.9, 0.84, 0.9], {}, 1000.0),                   # m (trotz $INSUNITS=4)
    ([800, 900, 940, 800], {"layer": "A-DOOR"}, 1.0),
], ids=["mm_mit_moebeln", "cm", "m", "a_door"])
def test_tuerkalibrierung_setzt_die_dekade(tmp_path, radien, kw, faktor):
    plan = lade_dxf(_tuer_plan(tmp_path, radien, **kw))
    assert plan.factor == faktor
    assert not plan.massstab_unsicher
    assert plan.faktor_quelle.startswith(f"Türkalibrierung ({len(radien)} Türbögen, Median ")
    med = sorted(radien)[len(radien) // 2] if len(radien) % 2 else None
    if med is not None:
        assert f"Median {med * faktor:.0f} mm" in plan.faktor_quelle


def test_tuerkalibrierung_aus_tuerbloecken(tmp_path):
    plan = lade_dxf(_tuer_plan(tmp_path, [900, 900, 900], layer="0", block=True))
    assert (plan.factor, plan.massstab_unsicher) == (1.0, False)
    assert plan.faktor_quelle.startswith("Türkalibrierung (3 Türbögen, Median 900 mm")


@pytest.mark.parametrize(("radien", "kw", "grund"), [
    ([900, 900], {}, "zu wenige Türbögen (2 < 3)"),
    ([], {"moebel": 20}, "zu wenige Türbögen (0 < 3)"),
    ([900, 900, 900], {"sweep": 180.0}, "zu wenige Türbögen (0 < 3)"),
    ([300, 900, 2700, 900, 300], {}, "Streuung MAD 67 % > 25 %"),
    ([300, 300, 300], {}, "Median 300 mm außerhalb 600–1300 mm"),
], ids=["zwei_tueren", "nur_moebel", "halbkreise", "streuung", "median_ausserhalb"])
def test_ohne_plausible_tueren_massstab_unsicher(tmp_path, radien, kw, grund):
    plan = lade_dxf(_tuer_plan(tmp_path, radien, **kw))
    assert plan.massstab_unsicher
    assert plan.factor == 1.0                         # $INSUNITS bleibt, kein Abbruch
    assert plan.faktor_quelle.startswith("$INSUNITS=4 (keine Wand-Spanne 15–500 m messbar)")
    assert grund in plan.faktor_quelle
    assert plan.faktor_quelle.endswith("— Maßstab unsicher")


def test_tuerkalibrierung_widerspricht_spanne(tmp_path):
    """Wand-Spanne 100 m legt Faktor 1 eindeutig fest; drei Türbögen mit Radius 90
    widersprechen → die Türregel entscheidet (Entscheid 7), mit Ausweis."""
    import ezdxf

    doc = ezdxf.new()
    doc.layers.add("A-WALL")
    msp = doc.modelspace()
    for i in range(12):
        msp.add_line((0, i * 1000), (100_000, i * 1000), dxfattribs={"layer": "A-WALL"})
    for i in range(3):
        msp.add_arc((5000 * i, 500), 90, 0, 90, dxfattribs={"layer": "Türen"})
    p = tmp_path / "widerspruch.dxf"
    doc.saveas(p)
    plan = lade_dxf(p)
    assert (plan.factor, plan.massstab_unsicher) == (10.0, False)
    assert plan.faktor_quelle.endswith("— widerspricht Spanne (Faktor 1)")


def test_spanne_und_tueren_einig_bleibt_spanne(tmp_path):
    """Gegenprobe: Spanne und Türen einig → Quelle bleibt `spanne` (kein Ausweis)."""
    import ezdxf

    doc = ezdxf.new()
    doc.layers.add("A-WALL")
    msp = doc.modelspace()
    for i in range(12):
        msp.add_line((0, i * 1000), (100_000, i * 1000), dxfattribs={"layer": "A-WALL"})
    for i in range(3):
        msp.add_arc((5000 * i, 500), 900, 0, 90, dxfattribs={"layer": "Türen"})
    p = tmp_path / "einig.dxf"
    doc.saveas(p)
    plan = lade_dxf(p)
    assert (plan.factor, plan.faktor_quelle, plan.massstab_unsicher) == (1.0, "spanne", False)
