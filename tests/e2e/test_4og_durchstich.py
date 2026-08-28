"""E2E-Durchstich Slice 0 — Pipeline mit Fake-Providern.

Beweist, dass die Contract-Naht + Komposition steht, bevor eine Zeile echte Logik
existiert. Pro Slice wird ein Fake gegen einen echten Provider getauscht.
"""
from fakes import build_fake_bundle
from notbeleuchtung.hauptengine.pipeline import Output, run


def test_durchstich_fake_providers(tmp_path):
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG",
              out_path=tmp_path / "4og_notbeleuchtung.dxf")
    assert isinstance(out, Output)
    # 5 echte 4OG-Rettungszeichen reproduziert
    assert out.render_summary["n_symbols"] == 5
    assert out.render_summary["by_kind"] == {"rz": 5}
    assert out.render_summary["floor"] == "4OG"
    assert out.render_summary["rendered"] is True    # echtes DXF seit Slice 3
    assert (tmp_path / "4og_notbeleuchtung.dxf").is_file()
    assert len(out.raum.raeume) == 2


def test_durchstich_ohne_out_path_bleibt_summary_only():
    """Compat-Guard: ohne out_path kein DXF, Summary wie vor Slice 3."""
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG")
    assert out.render_summary["rendered"] is False
    assert "output_path" not in out.render_summary


def test_naht_pipeline_covers_only_known_segments():
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG")
    known = {s.segment_id for s in out.raum.zirkulation.segmente}
    for p in out.platzierung.platzierungen:
        assert set(p.covers_segment) <= known
