"""anker_strategy — graph-basierte RZ-Platzierung an Entscheidungspunkten.

Die generative Segment-Strategie (`communal_stgh_strategy`) setzt 1 RZ je
Fluchtweg-Segment — gut für dünne Fixtures, aber sie **überproduziert auf realen
Wegenetzen** (Mollgasse: 77 RZ aus 77 WEG-Segmenten). Diese Strategie setzt RZ
stattdessen an den **Ankern des Zirkulationsgraphen**:

* **Kreuzungen** — Knoten mit `degree >= 3` (EN 1838 §4.1.2 f, Pflicht-Betonungspunkt)
* **Ausgänge** — `raum.ausgaenge` (EN 1838 §4.1.2 g)

Die Fluchtrichtung je Anker zeigt **zum nächsten Ausgang** (Gefälle der Dijkstra-
Distanz, `graph.distanz_zu_ausgang`). Nutzt `platzierung/graph.py` (networkx) + die
Richtungs-Blockwahl aus `communal_stgh_strategy`. Render-frei, kein Contract berührt.

Voraussetzung: ein Zirkulationsgraph mit Knoten/Kanten (Selmans echter Graph, Slice 4).
Auf dem dünnen 4OG-Fixture (2 Kanten, keine Kreuzung) liefert sie nur die Ausgänge —
darum bleibt `plan_rettungszeichen` (Segment-basiert) die Default-Strategie, bis der
echte Graph da ist.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import (
    FluchtwegSegment,
    NormProvider,
    Platzierung,
    RaumModell,
)

from .communal_stgh_strategy import (
    _AGV_SV_F,
    _building_assigner,
    _richtung_und_rotation,
    _select_key,
)
from .graph import build_circulation_graph, distanz_zu_ausgang, kreuzungs_anker


def _node_positions(raum: RaumModell) -> dict[str, tuple[float, float]]:
    pos = {n.id: (n.xy_mm[0], n.xy_mm[1]) for n in raum.zirkulation.nodes}
    pos.update({a.id: (a.xy_mm[0], a.xy_mm[1]) for a in raum.ausgaenge})
    return pos


def plan_rettungszeichen_anker(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """RZ an Kreuzungs-Ankern (degree>=3) + Ausgängen, Richtung zum nächsten Ausgang."""
    G = build_circulation_graph(raum)
    if G.number_of_nodes() == 0:
        return []
    pos = _node_positions(raum)
    dist = distanz_zu_ausgang(raum, G)
    exits = {a.id for a in raum.ausgaenge if a.id in G}
    anker = sorted(set(kreuzungs_anker(G)) | exits)
    assign_building = _building_assigner([pos[n][0] for n in anker if n in pos])

    out: list[Platzierung] = []
    for nid in anker:
        if nid not in pos:
            continue
        nx_, ny = pos[nid]
        # Am Ausgang: Pfeil „unten" (Ausgang erreicht). An Kreuzungen: Richtung zum
        # nächsten Ausgang = Nachbar mit kleinster Dijkstra-Distanz (Gefälle-Richtung).
        nbrs = [m for m in G.neighbors(nid) if m in pos and m in dist]
        if nid not in exits and nbrs and nid in dist:
            tgt = min(nbrs, key=lambda m: dist[m])
            richtung, fallback_rot = _richtung_und_rotation(pos[tgt][0] - nx_, pos[tgt][1] - ny)
        else:
            richtung, fallback_rot = "unten", 270.0
        seg = FluchtwegSegment(segment_id=f"anker_{nid}", polyline_mm=[(nx_, ny)], reason="corner")
        anf = norm.fuer_fluchtweg_abschnitt(seg)
        catalog_key, is_directional = _select_key(anf.symbol_katalog_keys, richtung)
        rotation = 0.0 if is_directional else fallback_rot
        mirror_x = False if is_directional else (richtung == "rechts")
        out.append(
            Platzierung(
                xy_mm=(nx_, ny),
                catalog_key=catalog_key,
                rotation_deg=rotation,
                mirror_x=mirror_x,
                height_mm=float(anf.montagehoehe_mm),
                kind="rz",
                richtung=richtung,
                circuit_hint=f"AGV-{assign_building(nx_)}-F{_AGV_SV_F}",
                covers_segment=[],
                norm_quelle=anf.quelle,
            )
        )
    return out
