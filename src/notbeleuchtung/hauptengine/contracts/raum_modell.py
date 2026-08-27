"""Contract 1 — RaumModell (Selman: Raumerkennung -> Hauptengine).

Reines Geometrie-/Topologie-Ergebnis der Architektur-Erkennung. KEIN Norm-Urteil
(Symboltyp/Richtung/Anzahl entscheidet Leonis via NormRegelwerk). Evolviert den
Contract-A-Scaffold (fluchtweg_graph) aus elektro-planer Slice 2.50.0 um Vollräume.

Pydantic ist die Quelle der Wahrheit; das JSON-Schema wird daraus generiert
(scripts/gen_schema.py) und eingecheckt (Drift-Gate in CI).
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

XY = tuple[float, float]

CONTRACT_VERSION = "1.0.0"


class BBox(BaseModel):
    min_xy: XY
    max_xy: XY


class Raum(BaseModel):
    id: str
    raum_typ: str                       # z.B. "STIEGENHAUS", "GANG", "WC", "ZIMMER"
    polygon_mm: list[XY] = Field(default_factory=list)
    flaeche_m2: float = 0.0
    ist_fluchtweg: bool = False
    ist_communal: bool = False


class Tuer(BaseModel):
    id: str
    xy_mm: XY
    breite_mm: float = 0.0
    von_raum: str | None = None
    nach_raum: str | None = None
    ist_notausgang: bool = False
    schwenk_richtung: Literal["links", "rechts", "unbekannt"] = "unbekannt"


class Ausgang(BaseModel):
    id: str
    xy_mm: XY
    typ: Literal["final_exit", "stair_exit", "door"]


class Node(BaseModel):
    id: str
    typ: Literal["room", "door", "exit", "stair", "junction"]
    xy_mm: XY
    room_type: str | None = None


class Edge(BaseModel):
    from_: str = Field(alias="from")
    to: str
    len_mm: float

    model_config = {"populate_by_name": True}


class FluchtwegSegment(BaseModel):
    segment_id: str
    polyline_mm: list[XY] = Field(default_factory=list)
    laenge_mm: float = 0.0
    reason: Literal["exit", "corner", "long_run", "direction_change"]


class ZirkulationsGraph(BaseModel):
    nodes: list[Node] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)
    segmente: list[FluchtwegSegment] = Field(default_factory=list)


class RaumModell(BaseModel):
    """Was Selman produziert, was Leonis + Render konsumieren."""

    contract: Literal["RaumModell"] = "RaumModell"
    contract_version: str = CONTRACT_VERSION
    floor: str
    coordinate_system: Literal["mm"] = "mm"
    bounds_mm: BBox
    raeume: list[Raum] = Field(default_factory=list)
    tueren: list[Tuer] = Field(default_factory=list)
    ausgaenge: list[Ausgang] = Field(default_factory=list)
    zirkulation: ZirkulationsGraph = Field(default_factory=ZirkulationsGraph)
