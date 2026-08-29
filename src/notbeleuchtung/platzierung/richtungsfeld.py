"""richtungsfeld — Fluchtrichtung als Gefälle des Distanzfeldes zum nächsten Ausgang.

Die Pfeilrichtung eines Rettungszeichens ist kein Rätsel, sondern folgt zwingend aus
dem Graphen: sie zeigt zum Nachbarn, der die Distanz zum **nächsten** Ausgang am
stärksten verringert (Abstieg des Multi-Source-Dijkstra-Feldes).

Bei mehreren Ausgängen (z.B. **zwei Stiegenhäuser**) routet jeder Punkt zu seinem
nächstgelegenen Ausgang. An der **Wasserscheide** — der Kante, deren Enden zu
*verschiedenen* Ausgängen fliehen — teilt sich der Fluchtweg: dort gehört ein
**beidseitiges** Rettungszeichen (EN 1838 §4.1.2 e/f: „du kannst in beide Richtungen
flüchten"). Rein graph-basiert, render-frei, kein Contract berührt.
"""
from __future__ import annotations

import networkx as nx

from .communal_stgh_strategy import _richtung_und_rotation

Point = tuple[float, float]


def naechster_ausgang(G: nx.Graph, exits: list[str]) -> dict[str, tuple[str, float]]:
    """Je Knoten: (nächstgelegener Ausgang, Weglänge dorthin) via Multi-Source-Dijkstra."""
    best: dict[str, tuple[str, float]] = {}
    for e in exits:
        if e not in G:
            continue
        for n, d in nx.single_source_dijkstra_path_length(G, e, weight="len_mm").items():
            if n not in best or d < best[n][1]:
                best[n] = (e, d)
    return best


def richtungsfeld(
    G: nx.Graph, exits: list[str], pos: dict[str, Point]
) -> dict[str, dict]:
    """Je Knoten die Fluchtrichtung: `{richtung, rotation_deg, nach_ausgang, dist_mm}`.

    `richtung` = Abstiegsrichtung des Distanzfeldes (Nachbar mit kleinster Rest-
    Distanz), auf Kardinal gerundet. Ausgangsknoten selbst → 'unten' (erreicht).
    """
    best = naechster_ausgang(G, exits)
    feld: dict[str, dict] = {}
    for n in G.nodes:
        if n not in best or n not in pos:
            continue
        ausgang, dist = best[n]
        if dist == 0.0:
            feld[n] = {"richtung": "unten", "rotation_deg": 270.0, "nach_ausgang": ausgang, "dist_mm": 0.0}
            continue
        kandidaten = [(m, best[m][1]) for m in G.neighbors(n) if m in best and m in pos]
        if not kandidaten:
            continue
        tgt = min(kandidaten, key=lambda mc: mc[1])[0]
        richtung, rotation = _richtung_und_rotation(pos[tgt][0] - pos[n][0], pos[tgt][1] - pos[n][1])
        feld[n] = {"richtung": richtung, "rotation_deg": rotation, "nach_ausgang": ausgang, "dist_mm": dist}
    return feld


def wasserscheiden(G: nx.Graph, exits: list[str]) -> list[tuple[str, str]]:
    """Kanten, deren Enden zu VERSCHIEDENEN Ausgängen fliehen — dort teilt sich der
    Fluchtweg (Kandidaten für beidseitige Rettungszeichen)."""
    best = naechster_ausgang(G, exits)
    return [
        (u, v)
        for u, v in G.edges
        if u in best and v in best and best[u][0] != best[v][0]
    ]
