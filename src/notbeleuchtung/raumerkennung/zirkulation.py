"""zirkulation — 09-WEG-Geometrie → Fluchtweg-Segmente + Knoten/Kanten-Graph.

Die geplante Fluchtweg-Zirkulation liegt als LINE/LWPOLYLINE auf den ``09-WEG*``-
Layern. Daraus entstehen:
- ``FluchtwegSegment`` je Polylinie (mit Länge + grobem ``reason``),
- ein ``ZirkulationsGraph`` (Knoten = gesnappte Endpunkte, Kanten = Segmentstücke),
- ``Ausgang``-Objekte an Weg-Enden nahe der Außenkante (grad-1-Knoten).

Rein topologisch; Norm-Urteile (Notausgang-Pflicht) folgen später.
"""
from __future__ import annotations

import math
from itertools import pairwise

import networkx as nx

from notbeleuchtung.hauptengine.contracts.raum_modell import (
    Edge,
    FluchtwegSegment,
    Node,
    ZirkulationsGraph,
)

from .dxf_load import DxfPlan

WEG_PREFIX = ("09-WEG",)
_SNAP_MM = 100.0        # Endpunkte in diesem Raster fallen zusammen
_LONG_RUN_MM = 5000.0

XY = tuple[float, float]


def _snap(p: XY) -> XY:
    return (round(p[0] / _SNAP_MM) * _SNAP_MM, round(p[1] / _SNAP_MM) * _SNAP_MM)


def _weg_polylinien(plan: DxfPlan) -> list[list[XY]]:
    """LINE/LWPOLYLINE der 09-WEG-Layer als Punktlisten (mm)."""
    out: list[list[XY]] = []
    for e in plan.entities(WEG_PREFIX):
        if e.dxftype() in ("LINE", "LWPOLYLINE", "POLYLINE"):
            pts = plan.entity_points(e)
            if len(pts) >= 2:
                out.append(pts)
    return out


def _laenge(pts: list[XY]) -> float:
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def _reason(pts: list[XY]) -> str:
    if _laenge(pts) >= _LONG_RUN_MM:
        return "long_run"
    if len(pts) > 2:
        return "corner"
    return "direction_change"


def zirkulation_aus_dxf(plan: DxfPlan) -> ZirkulationsGraph:
    """Fluchtweg-Segmente + Knoten/Kanten-Graph aus den 09-WEG-Layern.

    Ausgänge werden NICHT hier bestimmt (die 09-WEG-Annotation endet am
    Planrahmen, nicht am Ausgang) — sie kommen aus den Außentüren (``tueren``).
    """
    polylinien = _weg_polylinien(plan)

    segmente: list[FluchtwegSegment] = []
    g = nx.Graph()
    for i, pts in enumerate(polylinien, start=1):
        segmente.append(
            FluchtwegSegment(
                segment_id=f"seg_{i}",
                polyline_mm=[(float(x), float(y)) for x, y in pts],
                laenge_mm=_laenge(pts),
                reason=_reason(pts),
            )
        )
        snapped = [_snap(p) for p in pts]
        for a, b in pairwise(snapped):
            if a != b:
                g.add_edge(a, b, len_mm=math.dist(a, b))

    node_id: dict[XY, str] = {p: f"n_{k}" for k, p in enumerate(g.nodes, start=1)}
    nodes = [
        Node(id=node_id[p], typ="junction", xy_mm=(float(p[0]), float(p[1])))
        for p in g.nodes
    ]
    edges = [
        Edge.model_validate(
            {"from": node_id[a], "to": node_id[b], "len_mm": d["len_mm"]}
        )
        for a, b, d in g.edges(data=True)
    ]
    return ZirkulationsGraph(nodes=nodes, edges=edges, segmente=segmente)
