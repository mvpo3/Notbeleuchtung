"""Contract 5 — OibBefund/OibErgebnis (Output des OIB-Pfads, OIB-RL 2 Tabelle 6).

Was der (spätere) OibProvider.bewerte_oib aus einem ProjektKontext produziert:
je Gebäudeteil eine Erforderlichkeits-Stufe + Audit-Trail (Quelle, Fundstelle,
angewandter Schwellenwert, Eingangswerte, fehlende Fakten). Reine Datenmodelle —
KEINE Bewertungs-Logik hier.

Pydantic ist die Quelle der Wahrheit; das JSON-Schema wird daraus generiert
(scripts/gen_schema.py) und eingecheckt (Drift-Gate in CI).
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from .projekt_kontext import RaumReferenz

CONTRACT_VERSION = "1.0.0"

OibStufe = Literal[
    "nicht_erforderlich",
    "eingeschraenkt",
    "uneingeschraenkt",
    "review_required",
]


class OibErgebnis(BaseModel):
    """Erforderlichkeits-Befund für genau einen Gebäudeteil (mit Audit-Trail)."""

    contract: Literal["OibErgebnis"] = "OibErgebnis"
    contract_version: str = CONTRACT_VERSION
    gebaeudeteil_id: str
    stufe: OibStufe
    zeile: str | None = None
    quelle: str
    norm_ausgabe: str
    fundstelle_seite: str | None = None
    angewandter_schwellenwert: str | None = None
    eingangswerte: dict[str, str] = Field(default_factory=dict)
    fehlende_fakten: list[str] = Field(default_factory=list)
    hinweise: list[str] = Field(default_factory=list)
    ausfuehrungs_verweise: list[str] = Field(default_factory=list)


class OibBefund(BaseModel):
    """Gesamt-Output über alle Gebäudeteile eines ProjektKontext."""

    contract: Literal["OibBefund"] = "OibBefund"
    contract_version: str = CONTRACT_VERSION
    ergebnisse: list[OibErgebnis] = Field(default_factory=list)
    nicht_zugeordnete_raum_referenzen: list[RaumReferenz] = Field(default_factory=list)
