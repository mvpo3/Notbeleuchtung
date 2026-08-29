"""S5 — zirkulation: 09-WEG → Segmente + Graph + Ausgänge."""
from __future__ import annotations

from notbeleuchtung.raumerkennung.dxf_load import bounds_mm, lade_dxf
from notbeleuchtung.raumerkennung.zirkulation import zirkulation_aus_dxf


def test_synth_fluchtweg(synth_dxf):
    plan = lade_dxf(synth_dxf)
    graph, ausgaenge = zirkulation_aus_dxf(plan, bounds_mm(plan))
    assert len(graph.segmente) == 1
    seg = graph.segmente[0]
    assert seg.laenge_mm == 6000.0          # 4000 + 2000
    assert seg.reason == "exit"             # Ende (6500,500) nahe Unterkante y=0
    assert len(graph.nodes) == 3
    assert len(graph.edges) == 2
    assert len(ausgaenge) >= 1


def test_mollgasse_fluchtweg(mollgasse_eg):
    plan = lade_dxf(mollgasse_eg)
    graph, _ausgaenge = zirkulation_aus_dxf(plan, bounds_mm(plan))
    assert len(graph.segmente) > 0
    assert all(s.laenge_mm > 0 for s in graph.segmente)
    assert len(graph.nodes) > 0
    assert all(e.len_mm > 0 for e in graph.edges)
