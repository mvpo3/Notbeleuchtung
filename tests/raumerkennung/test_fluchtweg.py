"""fluchtweg — explizite Linien, GRAPH-Wege übers Gang-Skelett, FALLBACK."""
from __future__ import annotations

import ezdxf
import pytest

from notbeleuchtung.hauptengine.contracts.raum_modell import (
    Ausgang,
    Raum,
    Tuer,
)
from notbeleuchtung.raumerkennung.dxf_load import DxfPlan
from notbeleuchtung.raumerkennung.fluchtweg import (
    explizite_linien,
    fluchtwege,
    linien_segmente,
)


def _plan(tmp_path):
    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    for name in ("FLW_EG", "Kataster Grenzen", "irgendwas"):
        doc.layers.add(name)
    doc.layers.get("Kataster Grenzen").color = 96
    doc.layers.get("irgendwas").color = 96
    msp = doc.modelspace()
    msp.add_line((0, 0), (5000, 0), dxfattribs={"layer": "FLW_EG"})
    msp.add_line((0, 0), (5000, 0), dxfattribs={"layer": "Kataster Grenzen"})
    msp.add_line((0, 1000), (5000, 1000), dxfattribs={"layer": "irgendwas"})
    return DxfPlan(doc=doc, space=msp, factor=1.0)


def test_explizite_linien_flw_und_farbe_96(tmp_path):
    linien = explizite_linien(_plan(tmp_path))
    # FLW-Layer + Farbe-96-Linie auf neutralem Layer; Kataster ausgeschlossen.
    assert len(linien) == 2
    segs = linien_segmente(linien, 0)
    assert all(s.quelle == "LINIE" for s in segs)
    assert segs[0].segment_id == "seg_1"


def _gang_szene():
    gang = Raum(id="gang", raum_typ="GANG",
                polygon_mm=[(0, 0), (20000, 0), (20000, 2000), (0, 2000)],
                nutzungsklasse="ALLGEMEIN_ERSCHLIESSUNG")
    zi = Raum(id="zi", raum_typ="ZIMMER",
              polygon_mm=[(0, 2000), (4000, 2000), (4000, 6000), (0, 6000)],
              nutzungsklasse="WOHNUNG_PRIVAT")
    start = Tuer(id="wet", xy_mm=(2000.0, 2000.0), von_raum="zi",
                 nach_raum="gang", tuer_detail="wohnungseingang")
    ziel = Tuer(id="haus", xy_mm=(20000.0, 1000.0), von_raum="gang",
                nach_raum="AUSSEN", tuer_detail="hauseingang")
    ausgang = Ausgang(id="exit_haus", xy_mm=(20000.0, 1000.0), typ="final_exit")
    return [gang, zi], [start, ziel], [ausgang]


def test_graph_segment_vom_wohnungseingang_zum_ausgang():
    raeume, tueren, ausgaenge = _gang_szene()
    segs = fluchtwege(raeume, tueren, ausgaenge, [])
    graph = [s for s in segs if s.quelle == "GRAPH"]
    assert len(graph) == 1
    s = graph[0]
    assert s.start_raum == "zi" and s.ziel_ausgang == "exit_haus"
    assert s.polyline_mm[0] == (2000.0, 2000.0)
    assert s.polyline_mm[-1] == (20000.0, 1000.0)
    assert s.laenge_mm >= 18000.0
    # Der Weg läuft über das Gang-Skelett, nicht durch die Wand: alle
    # Zwischenpunkte liegen im Gangband.
    assert all(0 <= y <= 2000 for _, y in s.polyline_mm[1:-1])


def test_start_nahe_expliziter_linie_wird_uebersprungen():
    raeume, tueren, ausgaenge = _gang_szene()
    linie = linien_segmente([[(1500.0, 1900.0), (19000.0, 1900.0)]], 0)
    segs = fluchtwege(raeume, tueren, ausgaenge, linie)
    assert [s for s in segs if s.quelle == "GRAPH"] == []


def test_fallback_mittelachse_fuer_gang_ohne_weg():
    gang = Raum(id="gang", raum_typ="GANG",
                polygon_mm=[(0, 0), (12000, 0), (12000, 2000), (0, 2000)])
    (s,) = fluchtwege([gang], [], [], [])
    assert s.quelle == "FALLBACK" and s.richtung_unbekannt
    assert s.start_raum == "gang"
    assert s.laenge_mm == pytest.approx(12000.0)
    assert all(y == pytest.approx(1000.0) for _, y in s.polyline_mm)
