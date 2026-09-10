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


def _stiegen_szene():
    """Gang → Stiegenhaus → Hauseingang: stair_exit als Zwischenknoten."""
    gang = Raum(id="gang", raum_typ="GANG",
                polygon_mm=[(0, 0), (20000, 0), (20000, 2000), (0, 2000)],
                nutzungsklasse="ALLGEMEIN_ERSCHLIESSUNG")
    stgh = Raum(id="stgh", raum_typ="STIEGENHAUS",
                polygon_mm=[(20000, 0), (26000, 0), (26000, 2000), (20000, 2000)],
                nutzungsklasse="ALLGEMEIN_ERSCHLIESSUNG")
    zi = Raum(id="zi", raum_typ="ZIMMER",
              polygon_mm=[(0, 2000), (4000, 2000), (4000, 6000), (0, 6000)],
              nutzungsklasse="WOHNUNG_PRIVAT")
    wet = Tuer(id="wet", xy_mm=(2000.0, 2000.0), von_raum="zi",
               nach_raum="gang", tuer_detail="wohnungseingang")
    st = Tuer(id="st", xy_mm=(20000.0, 1000.0), von_raum="gang",
              nach_raum="stgh", tuer_detail="stiegenhaustuer")
    haus = Tuer(id="haus", xy_mm=(26000.0, 1000.0), von_raum="stgh",
                nach_raum="AUSSEN", tuer_detail="hauseingang")
    ausgaenge = [Ausgang(id="exit_st", xy_mm=(20000.0, 1000.0), typ="stair_exit"),
                 Ausgang(id="exit_haus", xy_mm=(26000.0, 1000.0), typ="final_exit")]
    return [gang, stgh, zi], [wet, st, haus], ausgaenge


def test_eg_weg_endet_am_final_exit_stair_ist_zwischenknoten():
    raeume, tueren, ausgaenge = _stiegen_szene()
    segs = fluchtwege(raeume, tueren, ausgaenge, [], geschoss="EG")
    graph = {s.segment_id: s for s in segs if s.quelle == "GRAPH"}
    weg = graph["seg_graph_wet"]
    assert weg.ziel_ausgang == "exit_haus", "EG-Weg muss am final_exit enden"
    assert weg.polyline_mm[-1] == (26000.0, 1000.0)
    # Zusätzliches Segment Stiegenhaustür → nächster final_exit:
    assert graph["seg_graph_st"].ziel_ausgang == "exit_haus"


def test_og_weg_endet_am_stair_exit():
    raeume, tueren, ausgaenge = _stiegen_szene()
    segs = fluchtwege(raeume, tueren, ausgaenge, [], geschoss="OG3")
    (weg,) = [s for s in segs if s.quelle == "GRAPH"]
    assert weg.ziel_ausgang == "exit_st"
    assert weg.polyline_mm[-1] == (20000.0, 1000.0)


def test_eg_ohne_final_exit_warnung_mit_grund():
    raeume, tueren, ausgaenge = _stiegen_szene()
    nur_stair = [a for a in ausgaenge if a.typ == "stair_exit"]
    warnungen: list[str] = []
    segs = fluchtwege(raeume, tueren, nur_stair, [], geschoss="EG",
                      warnungen=warnungen)
    assert any("ohne final_exit" in w for w in warnungen)
    assert any("haus" in w for w in warnungen), "Grund nennt die Außen-Tür"
    # Ersatzweise laufen die Wege weiter zum stair_exit (kein Leer-Ergebnis):
    assert [s for s in segs if s.quelle == "GRAPH"]


def test_fallback_mittelachse_fuer_gang_ohne_weg():
    gang = Raum(id="gang", raum_typ="GANG",
                polygon_mm=[(0, 0), (12000, 0), (12000, 2000), (0, 2000)])
    (s,) = fluchtwege([gang], [], [], [])
    assert s.quelle == "FALLBACK" and s.richtung_unbekannt
    assert s.start_raum == "gang"
    assert s.laenge_mm == pytest.approx(12000.0)
    assert all(y == pytest.approx(1000.0) for _, y in s.polyline_mm)


def test_kein_final_exit_warnung_nennt_raum_und_grund():
    """Gar kein final_exit im Plan → Warnung mit Endraum UND Grund."""
    raeume, tueren, _ = _stiegen_szene()
    warnungen: list[str] = []
    fluchtwege(raeume, tueren, [], [], geschoss="EG", warnungen=warnungen)
    pro_start = [w for w in warnungen if "von Tür wet" in w]
    assert pro_start, "Pro-Start-Warnung fehlt im Fall ohne final_exit"
    assert "Endraum zi" in pro_start[0]          # Raumbezug
    # Grundtext selbst, nicht die Tür-ID (die auch „haus" enthält).
    assert "ohne Ausgangs-Rolle" in pro_start[0]


def test_grund_tuer_ohne_nachbarraum_vs_aussenbereich_nicht_erkannt():
    """Spec-Gründe unterscheiden: EINE Seite ohne Raum → „Tür ohne
    Nachbarraum"; BEIDE Seiten ohne Raum → „Außenbereich nicht erkannt"."""
    from notbeleuchtung.raumerkennung.fluchtweg import _final_exit_fehlt_grund
    from notbeleuchtung.raumerkennung.tuer_zuordnung import KEIN_RAUM

    einseitig = Tuer(id="t1", xy_mm=(0.0, 0.0), von_raum="zi",
                     nach_raum=KEIN_RAUM, breite_mm=900.0)
    beidseitig = Tuer(id="t2", xy_mm=(0.0, 0.0), von_raum=KEIN_RAUM,
                      nach_raum=KEIN_RAUM, breite_mm=900.0)
    assert "ohne Nachbarraum" in _final_exit_fehlt_grund([einseitig])
    assert "Außenbereich nicht erkannt" in _final_exit_fehlt_grund([beidseitig])
