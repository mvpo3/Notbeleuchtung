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

CONTRACT_VERSION = "1.2.0"

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
    gleichmaessigkeit_max: float | None = None   # Ud als max:min (EN 1838 §4.2.2/§4.3.2: je 40;
    #   §4.4.2 nennt Uo >= 0,1 für Arbeitsplätze — Uo (kleinste:mittlere, EN 12665) ist ein
    #   anderes Maß als Ud (kleinste:größte) und gehört NICHT in dieses Feld.
    umschaltzeit_max_s: float | None = None      # Umschaltzeit auf SV, Vollwert (100 % in 60 s);
    #   die Norm ist zweistufig (§4.2.6/§4.3.6: 50 % in 5 s) — der 5-s-Halbwert liegt als
    #   `umschaltzeit.halbwert_s` in normwissen/data, nicht in diesem Skalar.
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
    """Flächenbasierte Antipanik-Trigger — welche Fläche welche Pflicht auslöst.

    Quelle ist NICHT EN 1838 (dort kommt keine flächenbezogene Auslöse-Schwelle vor),
    sondern OVE E 8101:2019 718.560.9.001.AT bzw. ÖVE/ÖNORM E 8002-1 — dort
    scope-gebunden an „erhöhte Anforderungen nach der Art der Nutzung" (OVE R 12-2 /
    OIB-RL 2). Der Konsument (`flaechen_strategy`) darf sie deshalb nur anwenden, wenn
    der OIB-Pfad diesen Scope bestätigt (OibBefund-Gate), nie global.

    v1.2.0. Werte + `quelle` kommen aus `normwissen/data` (Enis); None = Norm liefert
    (noch) keine Schwelle. Konsument fragt sie statt sie zu raten.
    """

    antipanik_min_m2: float | None = None     # ab dieser freien Fläche Antipanik-Pflicht (OVE, ≈ 60 m²)
    wc_sanitaer_min_m2: float | None = None   # WC/Sanitär ab dieser Fläche antipanik-relevant (OVE, ≈ 8 m²)
    quelle: str | None = None                 # Quellen-String der Schwellen (z.B. OVE E 8101:2019
    #   718.560.9.001.AT) — Audit-Trail des Flächen-Triggers; muss in NormRegelwerk.quellen liegen
    #   (Naht-Invariante), sonst fällt der Trigger auf die Antipanik-Regel-Quelle zurück.


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
