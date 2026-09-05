"""Contract 3 — PlatzierungsErgebnis (Leonis: Platzierung -> Hauptengine).

Fertige Norm-Entscheidung je Symbol: Position, Katalog-Key, Richtung, Höhe, Art,
Kreis-Hinweis. Die Hauptengine verdrahtet + zeichnet nur noch. Evolviert den
Contract-B-Scaffold (notlicht_placement) aus elektro-planer Slice 2.50.0.

Naht-Invarianten (CI): jede `covers_segment` ist ein `segment_id` aus dem
RaumModell; jeder `catalog_key` existiert im Schrack-Mapping; jede `norm_quelle`
stammt aus dem NormRegelwerk.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

XY = tuple[float, float]

CONTRACT_VERSION = "1.2.0"   # 1.1.0: +lb_quelle · 1.2.0: Symbol-Datenmodell (Digest #6)

Kind = Literal["rz", "sicherheitsleuchte", "antipanik"]
Richtung = Literal["links", "rechts", "gerade", "oben", "unten"]

# Schaltungsart je Leuchte (Profi-Belegungsplan §3b): DL = Dauerlicht (maintained,
# Rettungszeichen müssen immer leuchten), BL = Bereitschaftslicht (non-maintained).
Schaltungsart = Literal["DL", "BL"]


class Platzierung(BaseModel):
    xy_mm: XY
    catalog_key: str                     # Schrack-Key, muss in schrack_symbol_mapping.yaml existieren
    rotation_deg: float = 0.0
    mirror_x: bool = False
    height_mm: float = 2400.0
    kind: Kind
    richtung: Richtung | None = None     # RZ-Pfeilrichtung
    circuit_hint: str = ""               # z.B. "AGV-A-F13" (Sicherheitskreis)
    covers_segment: list[str] = Field(default_factory=list)  # FK -> RaumModell segment_id
    norm_quelle: str = ""                # welche NormAnforderung diese Platzierung begründet
    lb_quelle: str = ""                  # LB-Provenienz (2. Input): welche LBVorgabe sie
    #                                      erzwang/übersteuerte (leer = rein norm-getrieben)
    # v1.2.0 — Symbol-Datenmodell (Profi-Plan Digest #6, Block-Attribute je Leuchte).
    # Alle optional/None: der Platzierer füllt, was er weiß; Render fällt sonst auf
    # seine bisherige Synthese zurück (NODEID) bzw. lässt das Attribut weg.
    schaltungsart: Schaltungsart | None = None  # DL (RZ) / BL (SL/AP) — Belegungsliste + Prüfung
    luminaire_id: str | None = None      # Leuchten-ID/NODEID (Wartung/Adressierung, z.B. "RZ-001")
    typ_letter: str | None = None        # TYPENUMBER: Legenden-Letter (Typ A/B/…) — Stückliste #7
    typ_name: str | None = None          # TYPENAME: Produktbezeichnung (aus LB/Produktdaten)
    montage_art: str | None = None       # MountingMethod: AP/WA/DA/EB …
    technologie: str | None = None       # Technology (z.B. "LED")
    stromaufnahme_ma: float | None = None  # Produkt-Nennstrom (mA) — strombasierter
    #                                        Stromkreis-Deckel (#14) statt Stückzahl-Platzhalter


class PlatzierungsErgebnis(BaseModel):
    """Was Leonis produziert, was die Hauptengine rendert."""

    contract: Literal["PlatzierungsErgebnis"] = "PlatzierungsErgebnis"
    contract_version: str = CONTRACT_VERSION
    floor: str
    coordinate_system: Literal["mm"] = "mm"
    platzierungen: list[Platzierung] = Field(default_factory=list)
