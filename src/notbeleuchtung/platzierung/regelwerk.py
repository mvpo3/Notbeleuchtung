"""regelwerk — RIVOPLAN-Zeichenregeln als Daten (RW-###) + Umsetzungs-Mapping.

Quelle: ``platzierung/data/notbeleuchtung_regeln.json`` — generiert aus
``knowledge/Pläne zeichnen Wissen/_Analyse_Regelwerk/REGELWERK_Notbeleuchtung.json``
(Auftrag „Wissensaufbau Notbeleuchtungsplanung" 2026-09-29, Mollgasse = Basis).
Eigene Lane: das ist Referenz-Praxis-Wissen (Zeichenregeln des Auftraggebers),
KEIN Enis-Normwissen — Norm-Werte kommen weiter ausschließlich vom NormProvider.

Verwendung:
- ``regel("RW-006")`` → Regel-Datensatz (frozen).
- ``quelle("RW-006")`` → Audit-String ``"Referenz-Praxis: RW-006 — <thema>"``
  für ``Platzierung.norm_quelle`` (Präfix-Kanal, kein Contract-Change).
- ``UMSETZUNG`` → RW-ID → Code-Stelle (modul.funktion) für bereits gebaute
  Regeln, deren norm_quelle norm-begründet bleibt (Fixtures/Naht unangetastet).
  Vollständigkeits-Test: tests/platzierung/test_regelwerk.py.
"""
from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from types import MappingProxyType

_DATEN = Path(__file__).resolve().parent / "data" / "notbeleuchtung_regeln.json"

PRAXIS_PREFIX = "Referenz-Praxis: "


@dataclass(frozen=True)
class Regel:
    id: str
    thema: str
    regel: str
    leuchtentyp: str
    prioritaet: str                      # "basis" | "ergaenzung"
    nb_ref: str | None = None
    geometrische_bedingung: Mapping = field(default_factory=dict)

    @property
    def ist_basis(self) -> bool:
        return self.prioritaet == "basis"


# RW-ID → Code-Stelle der bereits umgesetzten Regel (modul.funktion).
# Bewusst statisch: bestehende norm_quelle-Strings bleiben unangetastet
# (Naht-Invariante + Golden-Fixtures); Doku-Detail in docs/ENGINE_IST.md.
UMSETZUNG: dict[str, str] = {
    "RW-001": "bausteine.rotation_piktogramm_in_raum + fachpraxis.plant_tuer_rz",
    "RW-002": "fachpraxis.plant_tuer_rz (communal-Kandidaten)",
    "RW-003": "fachpraxis.plant_tuer_rz + anker_strategy (final_exit)",
    "RW-004": "stgh_strategy.fluchtvektor",
    "RW-005": "stgh_strategy.plan_stiegenhaus_rz + fachpraxis.stiegenhaus_rz_nachpass",
    "RW-006": "communal_stgh_strategy (gerade Gang-RZ) + gang_strategy._ist_abzweig",
    "RW-007": "bausteine.select_key/key_und_rotation/richtung_und_rotation",
    "RW-008": "sichtkette.kette_ausduennen + platzierer._sichtlinien_garantie",
    "RW-009": "anker_strategy (graph.kreuzungs_anker)",
    "RW-010": "deckung.verdichte_fluchtweg + flaechen_strategy.plan_antipanik + lux_nachweis",
    "RW-012": "dokumentiert (Alternativ-Positionen = Owner-Ermessen, kein Automatismus)",
    "RW-013": "bausteine.ist_untergeschoss + stgh_strategy.fluchtvektor(hinauf=True)",
    "RW-014": "montage_art je Strategie + platzierer (Decke-Default)",
    "RW-016": "anker_strategy._wasserscheide_achse + graph.distanz_je_ausgang",
    "RW-018": "dokumentiert (Gebäudehälften-Prozessregel: nie raten)",
    "RW-019": "fachpraxis.plant_tuer_rz (_TUERLEUCHTEN_RAUMTYPEN)",
    "RW-020": "sichtkette.kette_ausduennen (+_MIN_KORRIDOR_ARM_MM-Guard)",
    "RW-027": "fachpraxis.entferne_schacht_leuchten + _TUERLEUCHTE_KEIN_COMMUNAL",
    # Neue Basis-Regeln aus dem 5-Projekte-Abgleich 2026-09-29:
    "RW-029": "flaechen_strategy.find_center_visual (mittig zum Bereich; Diagonal-Konstruktion dokumentiert)",
    "RW-030": "deckung.verdichte_fluchtweg (lux-getriebene Zusatz-Leuchten = Kann-Fall)",
    "RW-031": "flaechen_strategy + fachpraxis (Antipanik in UG-/Allgemeinräumen, AP3-Referenz-Praxis; Lichtberechnung bestätigt)",
    "RW-032": "dokumentiert (Decke mittig = zulässige Alternative; Regelfall Wand = NB-R14/RW-014 gebaut)",
    "RW-034": "pipeline.run → render/lux_nachweis_bericht.schreibe_bericht (automatisch je Geschoss-Lauf)",
}

# Regeln ohne Engine-Umsetzung mit dokumentiertem Grund (Naht/Input fehlt bzw.
# Prozess-/Prüfregel außerhalb des Platzierers) — Test erzwingt Begründung.
NICHT_UMSETZBAR: dict[str, str] = {
    "RW-011": "Schräg-Rotations-Grenzfall — Kandidat, wartet auf Regelwerk-Beleg-Schnitt",
    "RW-015": "Kabeltrasse 450 mm: Trassenlage fehlt im leeren Architekturplan (Selman/LB-Naht)",
    "RW-017": "Garage-Durchquerbarkeit: Garage-Zirkulation fehlt aus Erkennung (Selman S-KG)",
    "RW-021": "SV-Anlagen-Position = LB-/circuit-Lane, kein Platzierer-Concern",
    "RW-022": "Dokumentklassen-/Quellen-Disziplin = Analyse-Prozessregel",
    "RW-023": "Cluster-/MFU-Fluchtweg: braucht offene-Fläche-Zirkulation (Selman-Naht)",
    "RW-024": "Mehr-Treppenhaus-Zuordnung: Prozessregel, Erkennungs-Naht",
    "RW-025": "Terrasse/Dachausstieg ≠ sicherer Bereich: Erkennungs-Klassifikation (Selman)",
    "RW-026": "INSUNITS-/Textanker-Disziplin = Eingabe-Healthcheck (scripts/dxf_healthcheck)",
    "RW-028": "AP-Längsachsen-Rotation: Antipanik wird derzeit rotationslos gesetzt — Achs-Rotation = Folge-Slice (Golden-Shift, Owner-GO)",
    "RW-033": "OG-I-Gang-Ausnahme: sichtkette dünnt bereits aus; explizite Ausnahme-Regel = Folge-Slice (verändert Mollgasse-Bänder)",
    "RW-035": "Stiegenpfeil-Farb-Heuristik = Erkennungs-Lane (Selman)",
}


@lru_cache(maxsize=1)
def _lade() -> Mapping[str, Regel]:
    daten = json.loads(_DATEN.read_text(encoding="utf-8"))
    regeln: dict[str, Regel] = {}
    for r in daten:
        regeln[r["id"]] = Regel(
            id=r["id"],
            thema=r.get("thema", ""),
            regel=r.get("regel", ""),
            leuchtentyp=r.get("leuchtentyp", "-"),
            prioritaet=r.get("prioritaet", "ergaenzung"),
            nb_ref=r.get("nb_ref"),
            geometrische_bedingung=MappingProxyType(r.get("geometrische_bedingung") or {}),
        )
    return MappingProxyType(regeln)


def alle() -> Mapping[str, Regel]:
    return _lade()


def regel(rw_id: str) -> Regel:
    return _lade()[rw_id]


def basis_regeln() -> list[Regel]:
    return [r for r in _lade().values() if r.ist_basis]


def quelle(rw_id: str) -> str:
    """Audit-String für norm_quelle neuer praxisbegründeter Platzierungen."""
    r = regel(rw_id)
    return f"{PRAXIS_PREFIX}{r.id} — {r.thema}"
