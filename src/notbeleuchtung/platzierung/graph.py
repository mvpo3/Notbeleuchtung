"""graph — Fluchtweg-Graph über NetworkX (Anker + Deckung/Distanz).

Baut aus `RaumModell.zirkulation` (Selman) einen ungerichteten, gewichteten Graphen
und liefert graph-basierte Platzierungs-Primitive:

* **Kreuzungs-Anker** — Knoten, an denen sich ≥ 3 Fluchtweg-Kanten treffen
  (Verzweigung/Kreuzung); EN 1838 §4.1.2 f) Pflicht-Betonungspunkt (RZ/SL ≤ 2 m).
* **Distanz-zum-Ausgang** — kürzeste Weglänge je Knoten zum nächsten Ausgang
  (Dijkstra über `len_mm`); Basis für Deckungs-/Reichweiten-Checks (RZ-Sichtlinie,
  Leuchten-Verdichtung entlang der Linie).

Reine Analyse, render-frei, **kein Contract berührt**. Ergänzt die generative
Segment-Strategie (`communal_stgh_strategy`) um die Graph-Schichten des Ausbau-
Fahrplans (Anker → Linie → Fläche → Deckung, s. PLATZIERUNGS_KONZEPTE.md).
"""
from __future__ import annotations

import networkx as nx

from notbeleuchtung.hauptengine.contracts import RaumModell


def build_circulation_graph(raum: RaumModell) -> nx.Graph:
    """`RaumModell.zirkulation` → ungerichteter Graph (Kanten gewichtet mit len_mm).

    Ausgangs-/Tür-Knoten, die nur in Kanten vorkommen (nicht in `nodes`), werden von
    NetworkX implizit angelegt — so hängen die Ausgänge am Graphen, auch wenn der
    Provider sie nicht als Node führt.
    """
    G = nx.Graph()
    z = raum.zirkulation
    for n in z.nodes:
        G.add_node(n.id, xy=n.xy_mm, typ=n.typ, room_type=n.room_type)
    for e in z.edges:
        G.add_edge(e.from_, e.to, len_mm=float(e.len_mm))
    return G


def kreuzungs_anker(G: nx.Graph, min_degree: int = 3) -> list[str]:
    """Knoten-IDs, an denen ≥ `min_degree` Fluchtweg-Kanten zusammenlaufen.

    Das sind Kreuzungen/Verzweigungen — EN 1838 §4.1.2 f) verlangt dort ein
    Rettungszeichen/eine Sicherheitsleuchte (≤ 2 m), das beide Wege erkennbar macht.
    """
    return sorted(n for n, d in G.degree() if d >= min_degree)


def distanz_zu_ausgang(raum: RaumModell, G: nx.Graph | None = None) -> dict[str, float]:
    """Kürzeste Weglänge (mm) jedes Knotens zum nächstgelegenen Ausgang (Dijkstra).

    Multi-Source über alle `raum.ausgaenge`, die im Graphen hängen. Leerer Dict, wenn
    kein Ausgang erreichbar. Basis für Reichweiten-/Deckungs-Checks entlang der Linie.
    """
    if G is None:
        G = build_circulation_graph(raum)
    exits = {a.id for a in raum.ausgaenge if a.id in G}
    if not exits:
        return {}
    return nx.multi_source_dijkstra_path_length(G, exits, weight="len_mm")
