"""dxf_healthcheck — Eingabe-DXF-Gesundheit (Skill plan-verify, Schritt 0)."""
import sys
from pathlib import Path

import ezdxf

sys.path.insert(0, str(Path(__file__).parents[2] / "scripts"))
import dxf_healthcheck as hc


def _plan(tmp_path, name, extra=None) -> str:
    """Mini-DXF: sauberer 10×8-m-Raum; `extra(msp)` fügt optional Störer hinzu."""
    doc = ezdxf.new()
    msp = doc.modelspace()
    for a, b in [((0, 0), (10000, 0)), ((10000, 0), (10000, 8000)),
                 ((10000, 8000), (0, 8000)), ((0, 8000), (0, 0))]:
        msp.add_line(a, b, dxfattribs={"layer": "wand"})
    if extra:
        extra(msp)
    p = tmp_path / name
    doc.saveas(p)
    return str(p)


def test_sauberer_plan_ist_gesund(tmp_path):
    b = hc.pruefe(_plan(tmp_path, "clean.dxf"))
    assert b.gesund is True
    assert b.ausreisser == 0
    assert b.span_x_m <= 11.0 and b.span_y_m <= 9.0


def test_koordinaten_versatz_wird_erkannt(tmp_path):
    # Eine Linie am 4OG-artigen Versatz (y ≈ 347.535 km) → Ausreißer + Riesen-Spanne.
    def stoerer(msp):
        msp.add_line((95904, 347_534_960_853), (96000, 347_534_960_900),
                     dxfattribs={"layer": "130 Wand Innen"})
    b = hc.pruefe(_plan(tmp_path, "versatz.dxf", stoerer))
    assert b.gesund is False
    assert b.ausreisser >= 1
    assert b.span_y_m > hc.SPAN_WARN_M
    assert any("Wand Innen" in lay for lay, _ in b.top_layer_fern)


def test_zwei_cluster_im_report(tmp_path):
    def stoerer(msp):
        msp.add_line((0, 3.4e11), (1, 3.4e11), dxfattribs={"layer": "bemassung"})
    b = hc.pruefe(_plan(tmp_path, "cluster.dxf", stoerer))
    assert len(b.cluster) >= 2                 # ~0 UND +1e11-Bucket
    assert "NO-GO" in hc.report(b)             # Report weist NO-GO aus
    assert b.gesund is False


def test_main_exit_codes(tmp_path, capsys):
    clean = _plan(tmp_path, "ok.dxf")

    def stoerer(msp):
        msp.add_line((0, 5e11), (1, 5e11))
    bad = _plan(tmp_path, "bad.dxf", stoerer)
    assert hc.main([clean]) == 0
    assert hc.main([bad]) == 1
    assert hc.main([clean, bad]) == 1          # ein auffälliger reicht für Exit 1


def test_unlesbare_datei_ist_nogo(tmp_path):
    fehlt = str(tmp_path / "gibtsnicht.dxf")
    b = hc.pruefe(fehlt)
    assert b.gesund is False and b.fehler is not None
