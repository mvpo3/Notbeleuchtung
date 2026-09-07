"""fachpraxis — Praxis-Regeln des Owners (weder Norm- noch LB-Wissen).

Slice 2.3 (MEGA-Prompt 2026-09-07). Werte sind bewusst KEIN YAML in
`normwissen/` — sie stammen aus der Planungspraxis des Owners, nicht aus
EN 1838/ÖNorm. Stellt sich später heraus, dass ein Wert in einer LB stehen
kann, wandert er in den LB-explizit-Pfad (Entscheidungs-Hierarchie).

Mess-Protokoll (docs/analyse/mollgasse_ug_notbeleuchtung.md, Abschlussreport):
- Regel A („Tür-RZ-unten → Pfeil links") wurde nach Messung VERWORFEN
  (Gate G3, Owner-Entscheid in-Session): Mollgasse-GU 5/41 links, die
  Owner-korrigierte wohnbau_v7-Datei bestätigt #111 (Pfeil rotiert ZUR Tür).
- Regel B (Aufheller 500 mm) in Lesart **B1** gebaut (Gate G4, Owner-Entscheid
  in-Session auf Owner-Wort): die GU-Pläne kennen keinen Aufheller-Typ, die
  Messung konnte B1/B2 nicht entscheiden — Quelle ist die Owner-Ansage
  („Aufheller 500 mm neben dem RZ"), nicht die Empirie.

Audit-Trail: `norm_quelle = "fachpraxis: aufheller-500mm"` (die Naht-Invariante
prüft Quellen nur auf der Golden-Fixture; ein eigenes `decision_source`-Feld
wäre ein 3-Owner-Contract-Slice → handoff(contracts) im Report).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from notbeleuchtung.hauptengine.contracts import Platzierung, RaumModell

from .geometry import point_in_polygon

AUFHELLER_KEY = "sicherheitsleuchte_aufheller"
QUELLE_AUFHELLER = "fachpraxis: aufheller-500mm"


@dataclass(frozen=True)
class FachpraxisRegeln:
    """Konstanten der Owner-Praxis. Quelle: Leonis 07.09.2026 (G3/G4-Entscheide),
    Demo-Projekte + Mollgasse-UG-Referenz (Slice 4.1) als Mess-Kontext."""

    aufheller_abstand_mm: float = 500.0
    #: reserviert — Regel A (tuer_rz_richtung) nach Messung verworfen (G3).
    tuer_naehe_mm: float = 300.0


def _effektive_richtung_deg(p: Platzierung) -> float | None:
    """Weltwinkel des RZ-Pfeils (Basis→Spiegel→Rotation) — None ohne Richtungs-Block."""
    # Lazy-Import: hält den Modul-Import ezdxf-frei und zyklenfrei (bausteine
    # importiert symbols.orientation bereits — gleiche Grenze).
    from notbeleuchtung.symbols import load_symbol_mapping
    from notbeleuchtung.symbols.orientation import basis_deg

    entry = load_symbol_mapping().get(p.catalog_key) or {}
    basis = basis_deg(str(entry.get("block_name", "")))
    if basis is None:
        return None
    eff = (180.0 - basis) % 360.0 if p.mirror_x else basis
    return (eff + p.rotation_deg) % 360.0


def _in_einem_raum(raum: RaumModell, xy: tuple[float, float]) -> bool:
    return any(
        len(r.polygon_mm) >= 3 and point_in_polygon(xy, r.polygon_mm)
        for r in raum.raeume
    )


def aufheller_je_rz(
    platzierungen: list[Platzierung],
    raum: RaumModell,
    regeln: FachpraxisRegeln | None = None,
) -> list[Platzierung]:
    """Regel B1: je RZ EIN Aufheller, `aufheller_abstand_mm` hinter dem RZ.

    „Hinter" = entgegen der effektiven Pfeilrichtung (weg vom Ausgang, Richtung
    Rauminneres — der Flüchtende kommt von dort und braucht das Licht VOR dem
    Zeichen). RZ ohne definierte Richtung (Doppelpfeil `gerade`, rotations-
    neutrale Symbole) bekommen keinen Aufheller. Liegt die Zielposition in
    keinem Raumpolygon, wird der Aufheller NICHT gesetzt (nie still außerhalb) —
    **fail-closed**: fehlen dem RaumModell die Polygone ganz (fragmentierte
    CAD-Familien liefern real leere `raeume`), ist die Kontur unbekannt und es
    wird KEIN Aufheller gesetzt, statt ihn ungeprüft ins Nichts zu platzieren.
    """
    regeln = regeln or FachpraxisRegeln()
    out: list[Platzierung] = []
    for p in platzierungen:
        if p.kind != "rz":
            continue
        eff = _effektive_richtung_deg(p)
        if eff is None:
            continue
        winkel = math.radians(eff + 180.0)
        xy = (
            p.xy_mm[0] + regeln.aufheller_abstand_mm * math.cos(winkel),
            p.xy_mm[1] + regeln.aufheller_abstand_mm * math.sin(winkel),
        )
        # Fail-closed: ohne belegte Kontur (leere raeume ODER Position außerhalb
        # aller Polygone) kein Aufheller — Review-Befund 2026-09-07.
        if not _in_einem_raum(raum, xy):
            continue
        out.append(
            Platzierung(
                xy_mm=xy,
                catalog_key=AUFHELLER_KEY,
                rotation_deg=0.0,
                mirror_x=False,
                height_mm=p.height_mm,
                kind="sicherheitsleuchte",
                richtung="gerade",
                circuit_hint=p.circuit_hint,
                covers_segment=[],
                norm_quelle=QUELLE_AUFHELLER,
            )
        )
    return out
