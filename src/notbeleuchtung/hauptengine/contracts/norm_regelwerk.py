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

CONTRACT_VERSION = "1.1.0"

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
    # v1.1.0 (Track B) — abfragbare Norm-Werte, Zahlen kommen aus normwissen/data (Enis);
    # None = die Norm liefert (noch) keinen Wert, Konsument fällt auf seinen Default zurück.
    gleichmaessigkeit_max: float | None = None   # Ud als max:min (EN 1838: 40 Rettungsweg / 10 Antipanik)
    umschaltzeit_max_s: float | None = None      # Umschaltzeit auf Sicherheitsstromversorgung
    quelle: str = ""                     # "ÖNORM EN 1838:2013 §4.2.1" — rückverfolgbar


class RaumRegel(BaseModel):
    """Ein Eintrag im Regelwerk-Snapshot (pro Raumtyp/Fluchtweg-Klasse)."""

    raum_typ: str
    ist_fluchtweg: bool
    anforderung: NormAnforderung


class ErkennungsweiteParameter(BaseModel):
    z_hinterleuchtet: float = 200.0      # EN 1838: hinterleuchtet
    z_beleuchtet: float = 100.0          # beleuchtet


class FlaechenSchwellen(BaseModel):
    """Flächenbasierte Trigger (EN 1838 §4.3 / OIB) — welche Fläche welche Pflicht auslöst.

    v1.1.0 (Track B). Werte kommen aus `normwissen/data` (Enis); None = Norm liefert
    (noch) keine Schwelle. Konsument (`flaechen_strategy`) fragt sie statt sie zu raten.
    """

    antipanik_min_m2: float | None = None     # ab dieser freien Fläche Antipanik-Pflicht (≈ 60 m²)
    wc_sanitaer_min_m2: float | None = None   # WC/Sanitär ab dieser Fläche antipanik-relevant (≈ 8 m²)


class ArbeitsplatzLux(BaseModel):
    """Arbeitsplätze mit besonderer Gefährdung (EN 1838 §4.4) — erhöhte Lux-Anforderung.

    v1.1.0 (Track B). Werte aus `normwissen/data` (Enis); None = kein Norm-Wert.
    """

    min_lux: float | None = None          # z.B. 15 lx bzw. 10 % der Nennbeleuchtungsstärke
    min_lux_absolut: float | None = None  # absolute Untergrenze (z.B. 5 lx)


class NormRegelwerk(BaseModel):
    """Serialisierbarer Voll-Dump für den Freeze-Snapshot-Test.

    `quellen` = die Menge aller Quellen-Strings, die der Provider je vergibt —
    die Naht-Invariante prüft, dass jede Platzierung.norm_quelle hierin liegt.
    """

    contract: Literal["NormRegelwerk"] = "NormRegelwerk"
    contract_version: str = CONTRACT_VERSION
    norm: str = "ÖNORM EN 1838:2013"
    erkennungsweite: ErkennungsweiteParameter = Field(default_factory=ErkennungsweiteParameter)
    # v1.1.0 (Track B) — zusätzliche abfragbare Norm-Werte (Enis füllt normwissen/data).
    flaechen_schwellen: FlaechenSchwellen = Field(default_factory=FlaechenSchwellen)
    arbeitsplatz_lux: ArbeitsplatzLux = Field(default_factory=ArbeitsplatzLux)
    regeln: list[RaumRegel] = Field(default_factory=list)
    quellen: list[str] = Field(default_factory=list)
