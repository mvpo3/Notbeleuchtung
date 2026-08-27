"""Contract 2 — NormRegelwerk (Enis: Normwissen -> Hauptengine).

NEU gegenüber dem elektro-planer-Scaffold. Nicht nur Daten — Enis liefert eine
Query-API (siehe ports.NormProvider), damit Leonis die Norm FRAGT statt YAML zu
parsen. Diese Modelle sind die Antwort- + Snapshot-Typen.

Werte-Quelle: ÖNORM EN 1838:2013 (Lux, Erkennungsweite l = z*h, Montagehöhe,
Dauer) — maschinenlesbar in normwissen/data/*.yaml, gepflegt allein von Enis.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

CONTRACT_VERSION = "1.0.0"

Klassifikation = Literal["rz", "antipanik", "sicherheitsleuchte"]


class NormAnforderung(BaseModel):
    """Antwort der Norm-Query für einen Raum bzw. Fluchtweg-Abschnitt."""

    min_lux: float                       # 1.0 Rettungsweg / 0.5 Antipanik (EN 1838)
    klassifikation: Klassifikation
    montagehoehe_mm: int = 2000          # >= 2000 (EN 1838 §4.1)
    erkennungsweite_m: float | None = None   # l = z*h; None wenn nicht anwendbar
    symbol_katalog_keys: list[str] = Field(default_factory=list)
    mindest_anzahl: int = 1              # z.B. RZ = 2 immer
    dauer_min: int = 60                  # Notbetriebsdauer
    quelle: str = ""                     # "ÖNORM EN 1838:2013 §4.2.1" — rückverfolgbar


class RaumRegel(BaseModel):
    """Ein Eintrag im Regelwerk-Snapshot (pro Raumtyp/Fluchtweg-Klasse)."""

    raum_typ: str
    ist_fluchtweg: bool
    anforderung: NormAnforderung


class ErkennungsweiteParameter(BaseModel):
    z_hinterleuchtet: float = 200.0      # EN 1838: hinterleuchtet
    z_beleuchtet: float = 100.0          # beleuchtet


class NormRegelwerk(BaseModel):
    """Serialisierbarer Voll-Dump für den Freeze-Snapshot-Test.

    `quellen` = die Menge aller Quellen-Strings, die der Provider je vergibt —
    die Naht-Invariante prüft, dass jede Platzierung.norm_quelle hierin liegt.
    """

    contract: Literal["NormRegelwerk"] = "NormRegelwerk"
    contract_version: str = CONTRACT_VERSION
    norm: str = "ÖNORM EN 1838:2013"
    erkennungsweite: ErkennungsweiteParameter = Field(default_factory=ErkennungsweiteParameter)
    regeln: list[RaumRegel] = Field(default_factory=list)
    quellen: list[str] = Field(default_factory=list)
