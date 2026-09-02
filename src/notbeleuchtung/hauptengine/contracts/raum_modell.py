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

CONTRACT_VERSION = "1.1.0"

# v1.1.0 (Sonderstellen, Option A nach docs/SPEC_SONDERSTELLEN_CONTRACT.md) —
# hervorzuhebende Stellen nach EN 1838 §4.1.2. Typ-Vokabular deckt sich mit der
# ISO-7010-Symbolik des Profi-Plans (din_Feuerloescher_F001, din_Hydrant_F002, …).
SonderstellenTyp = Literal[
    "feuerloescher", "hydrant", "erste_hilfe", "brandmelder", "niveauaenderung",
]


class BBox(BaseModel):
    min_xy: XY
    max_xy: XY


class Sonderstelle(BaseModel):
    """Hervorzuhebende Stelle nach EN 1838 §4.1.2 — punktförmig.

    Die Norm-Anforderung ist ein Abstand zum Gerät (Leuchte „nahe", ANMERKUNG:
    ≤ 2 m horizontal) — deshalb ein Punkt-Modell, kein Raum-Flag. Heute ist kein
    Typ automatisch aus dem Architekturplan erkennbar (Spec §4) — die Quelle ist
    i.d.R. eine manuelle Angabe; `quelle` trägt die Herkunft als Audit-Trail.
    """

    id: str
    typ: SonderstellenTyp
    xy_mm: XY
    raum_id: str | None = None
    quelle: str = ""              # Audit-Trail: woher die Angabe stammt


class Raum(BaseModel):
    id: str
    raum_typ: str                       # z.B. "STIEGENHAUS", "GANG", "WC", "ZIMMER"
    polygon_mm: list[XY] = Field(default_factory=list)
    flaeche_m2: float = 0.0
    ist_fluchtweg: bool = False
    ist_communal: bool = False
    # v1.1.0 — Raum-Eigenschaften mit Norm-Folge (Anforderung gilt dem Raum bzw.
    # der Aufgabenfläche, nicht einem Punkt → Flags statt Sonderstelle):
    ist_barrierefrei: bool = False        # EN 1838 §4.3.8 (Antipanik-Pflicht barrierefreies WC)
    besondere_gefaehrdung: bool = False   # EN 1838 §4.4.1 (Arbeitsplätze, erhöhter Lux-Anspruch)


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
    # v1.1.0 — punktförmige Pflichtstellen (EN 1838 §4.1.2); leer = keine bekannt.
    sonderstellen: list[Sonderstelle] = Field(default_factory=list)
