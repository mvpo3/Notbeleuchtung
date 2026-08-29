"""S5 — zirkulation: 09-WEG → Segmente + Graph + Ausgänge."""
from __future__ import annotations

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.zirkulation import zirkulation_aus_dxf


def test_synth_fluchtweg(synth_dxf):
    graph = zirkulation_aus_dxf(lade_dxf(synth_dxf))
    assert len(graph.segmente) == 1
    seg = graph.segmente[0]
    assert seg.laenge_mm == 15000.0         # 10000 + 5000
    assert seg.reason == "long_run"         # >= 5 m
    assert len(graph.nodes) == 3
    assert len(graph.edges) == 2


def test_mollgasse_fluchtweg(mollgasse_eg):
    graph = zirkulation_aus_dxf(lade_dxf(mollgasse_eg))
    assert len(graph.segmente) > 0
    assert all(s.laenge_mm > 0 for s in graph.segmente)
    assert len(graph.nodes) > 0
    assert all(e.len_mm > 0 for e in graph.edges)
