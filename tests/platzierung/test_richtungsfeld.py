"""richtungsfeld — Fluchtrichtung (Distanz-Gefälle) + Wasserscheide bei zwei Ausgängen."""
import networkx as nx

from notbeleuchtung.platzierung.richtungsfeld import richtungsfeld, wasserscheiden

# Gerader Gang: n0..n6 auf x=0,2000,...,12000.
POS = {f"n{i}": (2000.0 * i, 0.0) for i in range(7)}


def _gang() -> nx.Graph:
    G = nx.Graph()
    for i in range(6):
        G.add_edge(f"n{i}", f"n{i+1}", len_mm=2000.0)
    return G


def test_ein_ausgang_alle_pfeile_zum_ausgang():
    G = _gang()
    feld = richtungsfeld(G, ["n0"], POS)          # Ausgang links
    for i in range(1, 7):
        assert feld[f"n{i}"]["richtung"] == "links"   # alle zeigen zum Ausgang
    assert wasserscheiden(G, ["n0"]) == []


def test_zwei_stiegenhaeuser_wasserscheide():
    G = _gang()
    exits = ["n0", "n6"]                            # zwei Stiegenhäuser (beide Enden)
    feld = richtungsfeld(G, exits, POS)
    assert feld["n1"]["richtung"] == "links"        # linke Hälfte → linker Ausgang
    assert feld["n5"]["richtung"] == "rechts"       # rechte Hälfte → rechter Ausgang
    assert feld["n1"]["nach_ausgang"] == "n0"
    assert feld["n5"]["nach_ausgang"] == "n6"
    # genau eine Wasserscheide-Kante in der Mitte (n3<->n4)
    ws = wasserscheiden(G, exits)
    assert len(ws) == 1
    assert set(ws[0]) == {"n3", "n4"}


def test_ausgang_selbst_ist_erreicht():
    feld = richtungsfeld(_gang(), ["n0"], POS)
    assert feld["n0"]["dist_mm"] == 0.0
