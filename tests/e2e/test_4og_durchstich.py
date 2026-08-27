"""E2E-Durchstich Slice 0 — Pipeline mit Fake-Providern.

Beweist, dass die Contract-Naht + Komposition steht, bevor eine Zeile echte Logik
existiert. Pro Slice wird ein Fake gegen einen echten Provider getauscht.
"""
from fakes import build_fake_bundle
from notbeleuchtung.hauptengine.pipeline import Output, run


def test_durchstich_fake_providers():
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG")
    assert isinstance(out, Output)
    # 5 echte 4OG-Rettungszeichen reproduziert
    assert out.render_summary["n_symbols"] == 5
    assert out.render_summary["by_kind"] == {"rz": 5}
    assert out.render_summary["floor"] == "4OG"
    assert out.render_summary["rendered"] is False   # echtes DXF ab Slice 3
    assert len(out.raum.raeume) == 2


def test_naht_pipeline_covers_only_known_segments():
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG")
    known = {s.segment_id for s in out.raum.zirkulation.segmente}
    for p in out.platzierung.platzierungen:
        assert set(p.covers_segment) <= known
