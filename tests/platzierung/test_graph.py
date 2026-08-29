"""graph — NetworkX-Fluchtweg-Graph: Aufbau, Kreuzungs-Anker, Distanz-zum-Ausgang."""
import json
from pathlib import Path

import networkx as nx

from notbeleuchtung.hauptengine.contracts import RaumModell
from notbeleuchtung.platzierung.graph import (
    build_circulation_graph,
    distanz_zu_ausgang,
    kreuzungs_anker,
)

FIXTURES = Path(__file__).parents[1] / "fixtures"


def _raum() -> RaumModell:
    data = json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    return RaumModell.model_validate(data)


def test_build_graph_haengt_ausgaenge_ein():
    raum = _raum()
    G = build_circulation_graph(raum)
    # 2 Stiegenhaus-Knoten + 2 Ausgänge (nur in Kanten) = 4 Knoten, 2 Kanten
    assert G.number_of_nodes() == 4
    assert G.number_of_edges() == 2
    assert "exit_b" in G and "exit_a" in G


def test_distanz_zu_ausgang_ueber_len_mm():
    raum = _raum()
    dist = distanz_zu_ausgang(raum)
    # Ausgänge selbst = 0; Stiegenhaus-Knoten = Kantenlänge zum Ausgang.
    assert dist["exit_a"] == 0.0 and dist["exit_b"] == 0.0
    assert dist["stgh_b"] == 3300.0
    assert dist["stgh_a"] == 2400.0


def test_thin_graph_hat_keine_kreuzung():
    # Das dünne 4OG-Fixture hat nur Stich-Kanten (degree 1) → kein Kreuzungs-Anker.
    # Echte Kreuzungen kommen mit Selmans vollem Graph (Slice 4).
    assert kreuzungs_anker(build_circulation_graph(_raum())) == []


def test_kreuzungs_anker_findet_verzweigung():
    # Sternknoten 'K' mit 4 Armen → degree 4 ≥ 3 → Anker.
    G = nx.Graph()
    for arm in ("n", "s", "e", "w"):
        G.add_edge("K", arm, len_mm=1000.0)
    assert kreuzungs_anker(G) == ["K"]
    assert kreuzungs_anker(G, min_degree=5) == []
