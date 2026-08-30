"""Contract 6 — LBVorgabe (2. Input: Leistungsbeschreibung → explizite Vorgaben).

Der **2. Engine-Input** neben dem Architekturplan: die projektspezifischen, EXPLIZITEN
Auftraggeber-Vorgaben aus der Leistungsbeschreibung (LB), die Norm-Defaults
**übersteuern** (CLAUDE.md-Hierarchie: LB-explizit → Referenz-Praxis → EN-1838/ÖNorm →
OVE-Verbote). Diese Modelle sind das Ergebnis des LB-Parsings (Enis' Lane, `normwissen/
lb/`); der Contract selbst gehört der Hauptengine (Leonis, 3-Owner).

Kanonischer Fall (aus realen LBs, s. `knowledge/extracted/LB_ANALYSE_beispiele.md`):
eine LB kann für GK4 „KEINE Sicherheitsbeleuchtung in Stiegenhaus/Gängen" verlangen —
das **kippt** den Norm-Default `STIEGENHAUS → sicherheitsleuchte`. `bereiche_exklusion`
trägt genau diesen Hard-Override; `bereiche_inklusion` den umgekehrten Fall.

`None`/leere Liste = „in der LB nicht spezifiziert" → dann greift der Norm-Default.
Keine Defaultwerte erfinden. Jede Vorgabe trägt `lb_quelle` (Datei + §/Seite) als
Audit-Trail — spiegelbildlich zu `norm_quelle`.

Pydantic ist die Quelle der Wahrheit; das JSON-Schema wird daraus generiert
(scripts/gen_schema.py) und eingecheckt (Drift-Gate in CI).
"""
from __future__ import annotations

import math
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, Field, field_validator, model_validator

CONTRACT_VERSION = "1.0.0"

# Art der Sicherheitsstromversorgung (EN 1838 / OVE E 8101: getrennter SV-Kreis).
SystemTyp = Literal["einzelbatterie", "gruppenbatterie", "zentralbatterie"]
# Leuchten-Überwachung.
Ueberwachung = Literal["einzelleuchte", "zentral"]
# Prüfeinrichtung.
Pruefung = Literal["automatisch", "web", "manuell"]
# Wo Rettungszeichen gesetzt werden (EN 1838 §4.1 / EN ISO 7010).
RzStelle = Literal[
    "fluchttuer", "kreuzung", "richtungsaenderung", "niveauaenderung", "notausgang_aussen"
]


def _finite_nonneg(v: float | None) -> float | None:
    """None = nicht spezifiziert; sonst endlich (kein NaN/Inf) und >= 0."""
    if v is None:
        return v
    if not math.isfinite(v):
        raise ValueError("darf nicht NaN oder Infinity sein")
    if v < 0:
        raise ValueError("darf nicht negativ sein")
    return v


def _int_nonneg(v: int | None) -> int | None:
    if v is None:
        return v
    if v < 0:
        raise ValueError("darf nicht negativ sein")
    return v


MengeFloat = Annotated[float | None, AfterValidator(_finite_nonneg)]
ZaehlInt = Annotated[int | None, AfterValidator(_int_nonneg)]


class BereichsRegel(BaseModel):
    """Explizite LB-Vorgabe OB ein Raumtyp Sicherheitsbeleuchtung erhält.

    `raum_typ` muss auf Selmans RaumModell-Vokabular mappen (STIEGENHAUS/GANG/GARAGE …),
    sonst greift die Regel im Platzierer nicht. `sicherheitsbeleuchtung=False` in
    `bereiche_exklusion` ist der Hard-Override gegen den Norm-Default.
    """

    raum_typ: str
    sicherheitsbeleuchtung: bool
    begruendung: str | None = None   # z.B. "GK4 — Brandschutzkonzept"

    @field_validator("raum_typ")
    @classmethod
    def _nicht_leer(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("raum_typ darf nicht leer sein")
        return v


class SonderLux(BaseModel):
    """Erhöhte Mindest-Beleuchtungsstärke an einem Ort (z.B. Feuerlöscher ≥ 5 lx)."""

    ort: str
    min_lux: MengeFloat = None

    @field_validator("ort")
    @classmethod
    def _nicht_leer(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("ort darf nicht leer sein")
        return v


class LBVorgabe(BaseModel):
    """Explizite, projektspezifische Vorgaben aus der Leistungsbeschreibung (2. Input)."""

    contract: Literal["LBVorgabe"] = "LBVorgabe"
    contract_version: str = CONTRACT_VERSION
    projekt: str | None = None
    system_typ: SystemTyp | None = None
    batterie_standort: str | None = None
    betriebsdauer_min: ZaehlInt = None          # z.B. „8 Std" → 480; übersteuert EN-1838-Default
    umschaltzeit_max_s: MengeFloat = None
    mindest_lux_fluchtweg: MengeFloat = None
    ueberwachung: Ueberwachung | None = None
    pruefung: Pruefung | None = None
    piktogramm_norm: str | None = None          # z.B. "EN ISO 7010"
    fabrikat_rz: str | None = None
    fabrikat_sl: str | None = None
    bereiche_inklusion: list[BereichsRegel] = Field(default_factory=list)
    bereiche_exklusion: list[BereichsRegel] = Field(default_factory=list)
    rz_stellen: list[RzStelle] = Field(default_factory=list)
    sonder_lux: list[SonderLux] = Field(default_factory=list)
    norm_bezug: list[str] = Field(default_factory=list)
    lb_quelle: str = ""                          # Datei + §/Seite (Audit-Trail)

    @model_validator(mode="after")
    def _kein_bereich_widerspruch(self) -> LBVorgabe:
        inkl = {b.raum_typ for b in self.bereiche_inklusion}
        exkl = {b.raum_typ for b in self.bereiche_exklusion}
        kollision = inkl & exkl
        if kollision:
            raise ValueError(
                f"Raumtyp gleichzeitig in Inklusion und Exklusion: {sorted(kollision)}"
            )
        return self
