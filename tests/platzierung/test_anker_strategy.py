"""anker_strategy — RZ an Kreuzungs-Ankern (degree>=3) + Ausgängen, Richtung z. Ausgang."""
import json
from pathlib import Path

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import (
    Ausgang,
    BBox,
    Edge,
    Node,
    RaumModell,
    ZirkulationsGraph,
)
from notbeleuchtung.platzierung.anker_strategy import plan_rettungszeichen_anker

FIXTURES = Path(__file__).parents[1] / "fixtures"


def _plus_korridor() -> RaumModell:
    # Kreuzung J (degree 4) + 3 Raum-Enden + 1 Ausgang unterhalb von J.
    nodes = [
        Node(id="J", typ="junction", xy_mm=(0.0, 0.0)),
        Node(id="N", typ="room", xy_mm=(0.0, 8000.0)),
        Node(id="E", typ="room", xy_mm=(9000.0, 0.0)),
        Node(id="W", typ="room", xy_mm=(-9000.0, 0.0)),
    ]
    edges = [
        Edge(**{"from": "J", "to": "N", "len_mm": 8000.0}),
        Edge(**{"from": "J", "to": "E", "len_mm": 9000.0}),
        Edge(**{"from": "J", "to": "W", "len_mm": 9000.0}),
        Edge(**{"from": "J", "to": "EXIT", "len_mm": 6000.0}),
    ]
    return RaumModell(
        floor="DEMO",
        bounds_mm=BBox(min_xy=(-9000.0, -6000.0), max_xy=(9000.0, 8000.0)),
        ausgaenge=[Ausgang(id="EXIT", xy_mm=(0.0, -6000.0), typ="final_exit")],
        zirkulation=ZirkulationsGraph(nodes=nodes, edges=edges),
    )


def test_rz_an_kreuzung_und_ausgang():
    out = plan_rettungszeichen_anker(_plus_korridor(), FakeNormProvider())
    # Genau 2 Anker: die Kreuzung J + der Ausgang EXIT (die Raum-Enden N/E/W nicht).
    assert len(out) == 2
    assert all(p.kind == "rz" for p in out)
    xy = {p.xy_mm for p in out}
    assert (0.0, 0.0) in xy          # Kreuzung J
    assert (0.0, -6000.0) in xy      # Ausgang EXIT


def test_richtung_zeigt_zum_ausgang():
    out = plan_rettungszeichen_anker(_plus_korridor(), FakeNormProvider())
    bei_j = next(p for p in out if p.xy_mm == (0.0, 0.0))
    # J liegt über EXIT → Fluchtrichtung nach unten.
    assert bei_j.richtung == "unten"
    bei_exit = next(p for p in out if p.xy_mm == (0.0, -6000.0))
    assert bei_exit.richtung == "unten"  # Ausgang erreicht


def _kreuz_mit_isoliertem_ausgang() -> RaumModell:
    # Kreuzung J (degree 3) + Ausgang, der in KEINER Kante vorkommt (nicht im Graph).
    nodes = [
        Node(id="J", typ="junction", xy_mm=(0.0, 0.0)),
        Node(id="N", typ="room", xy_mm=(0.0, 8000.0)),
        Node(id="E", typ="room", xy_mm=(9000.0, 0.0)),
        Node(id="W", typ="room", xy_mm=(-9000.0, 0.0)),
    ]
    edges = [
        Edge(**{"from": "J", "to": "N", "len_mm": 8000.0}),
        Edge(**{"from": "J", "to": "E", "len_mm": 9000.0}),
        Edge(**{"from": "J", "to": "W", "len_mm": 9000.0}),
    ]
    return RaumModell(
        floor="DEMO",
        bounds_mm=BBox(min_xy=(-9000.0, -6000.0), max_xy=(9000.0, 8000.0)),
        ausgaenge=[Ausgang(id="EXIT_ISO", xy_mm=(0.0, -6000.0), typ="final_exit")],
        zirkulation=ZirkulationsGraph(nodes=nodes, edges=edges),
    )


def test_ausgang_ausserhalb_graph_bekommt_rz():
    # Realer Mollgasse-Fall: Ausgänge liegen neben, nicht auf dem Wegenetz (nicht im
    # Graph). §4.1.2 g verlangt trotzdem ein RZ an jedem Ausgang.
    out = plan_rettungszeichen_anker(_kreuz_mit_isoliertem_ausgang(), FakeNormProvider())
    xy = {p.xy_mm for p in out}
    assert (0.0, -6000.0) in xy      # isolierter Ausgang trotzdem mit RZ
    bei_exit = next(p for p in out if p.xy_mm == (0.0, -6000.0))
    assert bei_exit.richtung == "unten"  # graphlos → raus


def _zwei_nahe_kreuzungen() -> RaumModell:
    # J1 und J2 nur 100 mm auseinander, beide degree>=3 → ohne Dedup zwei RZ <250mm.
    nodes = [
        Node(id="J1", typ="junction", xy_mm=(0.0, 0.0)),
        Node(id="J2", typ="junction", xy_mm=(100.0, 0.0)),
        Node(id="A", typ="room", xy_mm=(0.0, 5000.0)),
        Node(id="B", typ="room", xy_mm=(-5000.0, 0.0)),
        Node(id="C", typ="room", xy_mm=(0.0, -5000.0)),
        Node(id="D", typ="room", xy_mm=(100.0, 5000.0)),
        Node(id="E", typ="room", xy_mm=(5100.0, 0.0)),
        Node(id="F", typ="room", xy_mm=(100.0, -5000.0)),
    ]
    edges = ([Edge(**{"from": "J1", "to": n, "len_mm": 5000.0}) for n in ("A", "B", "C")]
             + [Edge(**{"from": "J2", "to": n, "len_mm": 5000.0}) for n in ("D", "E", "F")])
    return RaumModell(
        floor="DEMO", bounds_mm=BBox(min_xy=(-5000.0, -5000.0), max_xy=(5100.0, 5000.0)),
        zirkulation=ZirkulationsGraph(nodes=nodes, edges=edges),
    )


def test_nahe_anker_werden_verschmolzen():
    # Zwei Kreuzungen 100 mm auseinander → genau EIN RZ (keine Doppelplatzierung <250mm).
    out = plan_rettungszeichen_anker(_zwei_nahe_kreuzungen(), FakeNormProvider())
    assert len(out) == 1


def test_kreuzung_ohne_erreichbaren_ausgang_zeigt_luftlinie():
    # Disconnected graph: Kreuzung J hat KEINEN Weg zum Ausgang (Ausgang hängt an
    # keiner Kante) → kein Dijkstra-Gefälle. Der Pfeil darf nicht „unten"
    # (= „Ausgang erreicht") fabrizieren, sondern zeigt per Luftlinie zum
    # geometrisch nächsten Ausgang — hier liegt er im OSTEN → „rechts".
    raum = _kreuz_mit_isoliertem_ausgang()
    raum = raum.model_copy(update={"ausgaenge": [
        Ausgang(id="EXIT_ISO", xy_mm=(12000.0, 0.0), typ="final_exit"),
    ]})
    out = plan_rettungszeichen_anker(raum, FakeNormProvider())
    bei_j = next(p for p in out if p.xy_mm == (0.0, 0.0))
    assert bei_j.richtung == "rechts"


def test_kreuzung_ganz_ohne_ausgaenge_faellt_auf_unten():
    # Gar kein Ausgang im Modell → keinerlei Richtungs-Information; der dokumentierte
    # Letzt-Fallback „unten" bleibt (Regression-Schranke für _zwei_nahe_kreuzungen).
    out = plan_rettungszeichen_anker(_zwei_nahe_kreuzungen(), FakeNormProvider())
    assert len(out) == 1 and out[0].richtung == "unten"


def test_duenner_graph_nur_ausgaenge():
    # 4OG-Fixture: 2 Stich-Kanten, keine Kreuzung → nur die 2 Ausgänge als Anker.
    data = json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    out = plan_rettungszeichen_anker(RaumModell.model_validate(data), FakeNormProvider())
    assert len(out) == 2  # exit_a + exit_b, keine degree>=3-Kreuzung
    assert all(p.kind == "rz" for p in out)
