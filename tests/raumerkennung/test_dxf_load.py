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
