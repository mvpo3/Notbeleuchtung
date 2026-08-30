"""Contract 4 — ProjektKontext (OIB-Richtlinie 2, Tabelle 6: Erforderlichkeit).

Gebäudeweiter, NICHT geschossweiser Kontext: Nutzungsart/Gebäudeklasse/Flächen/
Bettenzahl je Gebäudeteil. Anderer Input als der geschossweise EN-1838-Pfad
(RaumModell/NormRegelwerk) → bewusst getrennter Contract + eigenes Protocol
(OibProvider). Reine Datengrundlage; KEIN Resolver, KEINE Tabelle-6-Grenzwerte hier.

Pydantic ist die Quelle der Wahrheit; das JSON-Schema wird daraus generiert
(scripts/gen_schema.py) und eingecheckt (Drift-Gate in CI).

`None` bei einem Fachwert bedeutet ausdrücklich „nicht erhoben / unbekannt" —
keine Defaultwerte erfinden.
"""
from __future__ import annotations

import math
from datetime import date
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, Field, field_validator, model_validator

CONTRACT_VERSION = "1.0.0"

# --- Fachliche Enums (exakt aus OIB-RL 2 Tabelle 6 / Erläuterungen abgeleitet) -----

Nutzungsart = Literal[
    "WOHNGEBAEUDE",
    "SONSTIGES_GEBAEUDE",
    "SCHULE_KINDERGARTEN",
    "BEHERBERGUNG_STUDENTENHEIM",
    "SCHUTZHUETTE_EXTREMLAGE",
    "VERKAUFSSTAETTE_AUSSTELLUNGSSTAETTE",
    "SCHANK_SPEISEWIRTSCHAFT",
    "DISKOTHEK_TANZCAFE",
    "ALTEN_SENIORENHEIM",
    "PFLEGEHEIM",
    "KRANKENHAUS",
    "VERSAMMLUNG_INNERHALB_GEBAEUDE",
    "VERSAMMLUNG_AUSSERHALB_GEBAEUDE",
    "BETRIEBSBAU",
    "GARAGE",
    "PARKDECK",
    "UEBERDACHTER_STELLPLATZ",
    "VERKEHRSEINRICHTUNG",
    "NICHT_IN_TABELLE_6",
]

Gebaeudeklasse = Literal["GK1", "GK2", "GK3", "GK4", "GK5"]

LageZurWohnung = Literal["INNERHALB_WOHNUNG", "AUSSERHALB_WOHNUNG"]

Bundesland = Literal["W", "NOE", "OOE", "SBG", "STMK", "KTN", "TIR", "VBG", "BGLD"]


# --- Validierte Feldtypen ----------------------------------------------------------

def _finite_nonneg(v: float | None) -> float | None:
    """None = nicht erhoben; sonst endlich (kein NaN/Inf) und >= 0."""
    if v is None:
        return v
    if not math.isfinite(v):
        raise ValueError("darf nicht NaN oder Infinity sein")
    if v < 0:
        raise ValueError("darf nicht negativ sein")
    return v


def _int_nonneg(v: int | None) -> int | None:
    """None = nicht erhoben; sonst >= 0 (Zählwert)."""
    if v is None:
        return v
    if v < 0:
        raise ValueError("Zählwert darf nicht negativ sein")
    return v


# Fläche/Höhe in physikalischen Einheiten — None erlaubt, sonst finite & >= 0.
MengeFloat = Annotated[float | None, AfterValidator(_finite_nonneg)]
# Zählwert (strenge int-Bindung via pydantic) — None erlaubt, sonst >= 0.
ZaehlInt = Annotated[int | None, AfterValidator(_int_nonneg)]


# --- Modelle -----------------------------------------------------------------------

class RaumReferenz(BaseModel):
    """Verweis auf einen konkreten Raum im geschossweisen RaumModell.

    floor + raum_id gemeinsam, damit die Zuordnung Raum↔Geschoss über mehrere
    Geschosse eindeutig bleibt (keine getrennten floors[]/raum_ids[]-Listen).
    """

    floor: str
    raum_id: str

    @field_validator("floor", "raum_id")
    @classmethod
    def _nicht_leer(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("darf nicht leer sein")
        return v


class Gebaeudeteil(BaseModel):
    """Ein OIB-Tabelle-6-Beurteilungseinheit (z.B. Wohnteil, Garage) eines Projekts."""

    id: str
    bezeichnung: str = ""
    nutzungsart: Nutzungsart
    gebaeudeklasse: Gebaeudeklasse | None = None
    fluchtniveau_m: MengeFloat = None
    lage_zur_wohnung: LageZurWohnung | None = None
    netto_grundflaeche_m2: MengeFloat = None
    verkaufsflaeche_m2: MengeFloat = None
    nutzflaeche_garage_m2: MengeFloat = None
    betten_anzahl: ZaehlInt = None
    schlafplaetze_anzahl: ZaehlInt = None
    verabreichungsplaetze_anzahl: ZaehlInt = None
    personen_anzahl_bestimmt: ZaehlInt = None
    # Arbeitsstätte nach ASchG bleibt bewusst PRO Gebäudeteil (nicht global).
    arbeitsstaette_nach_aschg: bool | None = None
    raum_referenzen: list[RaumReferenz] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def _id_nicht_leer(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Gebaeudeteil.id darf nicht leer sein")
        return v


class ProjektKontext(BaseModel):
    """Gebäudeweiter Kontext neben dem geschossweisen RaumModell.

    Input des OIB-Pfads (OibProvider.bewerte_oib). Enthält je Gebäudeteil die
    fachlichen Fakten, aus denen der (spätere) Resolver die Tabelle-6-Erforderlichkeit
    ableitet.
    """

    contract: Literal["ProjektKontext"] = "ProjektKontext"
    contract_version: str = CONTRACT_VERSION
    jurisdiction: Literal["AT"] | None = None
    bundesland: Bundesland | None = None
    projekt_stichtag: date | None = None
    gebaeudeteile: list[Gebaeudeteil] = Field(default_factory=list)

    @model_validator(mode="after")
    def _ids_eindeutig(self) -> ProjektKontext:
        ids = [g.id for g in self.gebaeudeteile]
        if len(ids) != len(set(ids)):
            raise ValueError("Gebaeudeteil.id muss innerhalb eines ProjektKontext eindeutig sein")
        return self
