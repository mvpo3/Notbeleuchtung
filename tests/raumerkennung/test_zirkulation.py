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


def _weg_plan(tmp_path, name: str, punkte, layer: str = "A_Fluchtweg"):
    """20x12-m-Hülle + eine Polylinie auf ``layer``."""
    import ezdxf

    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4  # mm
    msp = doc.modelspace()
    doc.layers.add("02-TWA-G00-LEG-M0")
    doc.layers.add(layer)
    ecken = [(0, 0), (20000, 0), (20000, 12000), (0, 12000)]
    for i in range(4):
        msp.add_line(ecken[i], ecken[(i + 1) % 4],
                     dxfattribs={"layer": "02-TWA-G00-LEG-M0"})
    msp.add_lwpolyline(punkte, dxfattribs={"layer": layer})
    p = tmp_path / name
    doc.saveas(str(p))
    return p


def test_fluchtweg_layer_archicad_familie(tmp_path):
    # Fischamender/ArchiCAD nennt den Layer 'A_Fluchtweg' statt '09-WEG'.
    p = _weg_plan(tmp_path, "a_fluchtweg.dxf", [(2000, 6000), (18000, 6000)])
    graph = zirkulation_aus_dxf(lade_dxf(p))
    assert len(graph.segmente) >= 1
    assert all(s.laenge_mm > 0 for s in graph.segmente)


def test_stummel_polylinie_erzeugt_kein_segment(tmp_path):
    # 50 mm < Snap-Raster (100 mm) → degeneriert, würde nur einen Knoten ohne Kante liefern.
    p = _weg_plan(tmp_path, "stummel.dxf", [(2000, 6000), (2050, 6000)])
    graph = zirkulation_aus_dxf(lade_dxf(p))
    assert graph.segmente == []
    assert graph.edges == []
