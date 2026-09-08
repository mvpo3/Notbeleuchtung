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

from .bausteine import AGV_SV_F as _AGV_SV_F
from .bausteine import KORRIDOR_TYPEN as _KORRIDOR_TYPEN
from .bausteine import building_assigner as _building_assigner
from .geometry import find_center_visual, point_in_polygon

AUFHELLER_KEY = "sicherheitsleuchte_aufheller"
QUELLE_AUFHELLER = "fachpraxis: aufheller-500mm"

#: Regel 2026-09-07: diese Raumtypen bekommen IMMER eine Sicherheitsleuchte an
#: der Tür — fensterlose Innen-/Nebenräume, bei Netzausfall muss die Tür
#: auffindbar bleiben. TECHNIK/MUELLRAUM sind kanonische Vokabular-Typen
#: (docs/VOKABULAR.md); KINDERWAGENRAUM ist der GEMEINSAME Kinderwagenraum im
#: Wohnbau (Owner-Wahl, Referenz-Praxis), NICHT der private Wohnungs-Abstellraum.
#: ⚠️ Naht Selman: raumerkennung/raumtyp.py ebnet `kinderwagen`→ABSTELLRAUM ein
#: (STORAGE), d.h. auf ECHTEN Plänen trägt ein Kinderwagenraum heute
#: `ABSTELLRAUM`, nicht `KINDERWAGENRAUM` — bis die Erkennung den Typ erhält,
#: greift diese Regel nur, wo der Plan den Literal `KINDERWAGENRAUM` führt
#: (docs/COORDINATION.md 2026-09-07).
_TUERLEUCHTE_RAUMTYPEN = {"TECHNIK", "MUELLRAUM", "KINDERWAGENRAUM"}
#: Symbol = din-AP3-Antipanikleuchte, die in der SICHERHEITSLEUCHTEN-Rolle als
#: Universal-Leuchte verwendet wird (Rolle ≠ Produkt) — die knowledge-gestützte
#: Darstellung der Raum-Sicherheitsbeleuchtung. KEIN Aufheller (Zusatz-/Fülllicht).
TUERLEUCHTE_KEY = "antipanik_leuchte"
#: Referenz-Praxis (Owner-Wahl „immer"): dokumentierte Regel SL-13 in
#: normwissen/data/platzierung_regeln.yaml (leuchtenart sicherheitsleuchte) +
#: INOTEC HB2026 (Technikräume 5 lx) + EN 1838:2025 §5.4 + reale Elektro-LB §5.1.23.
QUELLE_TUERLEUCHTE = (
    "Referenz-Praxis: Technik-/Nebenraum-SL an der Tür "
    "(INOTEC HB2026 · EN 1838:2025 §5.4 · Elektro-LB §5.1.23)"
)
#: Montagehöhe der Tür-Sicherheitsleuchte (über der Tür; ≥ EN-1838-Mindesthöhe 2 m).
TUERLEUCHTE_HOEHE_MM = 2400.0
#: Erschließungs-Raumtypen — eine Tür DORTHIN ist die „Ausgangs"-Tür des Raums.
_ERSCHLIESSUNG = _KORRIDOR_TYPEN | {"STIEGENHAUS"}


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


def _tuer_des_raums(raum: RaumModell, r):
    """Die (Haupt-)Tür eines Raums oder None.

    Reihenfolge: bevorzugt eine Tür, die in einen Erschließungsraum (GANG/Flur/
    Stiegenhaus) führt — das ist die „Ausgangs"-Tür; sonst die erste referenzierte
    Tür; sonst geometrisch die dem Raum-Zentrum nächste Tür, die im Raumpolygon
    liegt. Fehlt jede Tür-Information, None (der Aufrufer platziert dann nichts —
    fail-closed, keine Leuchte an geratener Stelle).
    """
    typen = {x.id: (x.raum_typ or "").upper() for x in raum.raeume}
    referenziert = [t for t in raum.tueren if r.id in (t.von_raum, t.nach_raum)]
    if referenziert:
        def _zielraum(t):
            return t.nach_raum if t.von_raum == r.id else t.von_raum
        erschliessung = [
            t for t in referenziert
            if typen.get(_zielraum(t) or "", "") in _ERSCHLIESSUNG
        ]
        return (erschliessung or referenziert)[0]
    if len(r.polygon_mm) >= 3:
        drin = [t for t in raum.tueren if point_in_polygon(t.xy_mm, r.polygon_mm)]
        if drin:
            cx, cy = find_center_visual(r.polygon_mm)
            return min(drin, key=lambda t: (t.xy_mm[0] - cx) ** 2 + (t.xy_mm[1] - cy) ** 2)
    return None


def tuerleuchte_pflichtraeume(raum: RaumModell) -> list[Platzierung]:
    """Referenz-Praxis 2026-09-07: TECHNIK/MUELLRAUM bekommen IMMER eine
    Sicherheitsleuchte an der Tür.

    Eine Leuchte je Pflichtraum, gesetzt an der (Haupt-)Tür des Raums (`bei der
    Tür`). Symbol = Antipanik-AP3 (Universal-Sicherheitsleuchte, Rolle ≠ Produkt),
    `kind="sicherheitsleuchte"` (Rolle: Raum-Sicherheitsbeleuchtung, KEINE
    Antipanik-Zone). Diese Räume sind fensterlose Innen-/Nebenräume und liegen
    meist NICHT auf dem erkannten Fluchtweg — deshalb greift keine norm-getriebene
    Strategie, und die Regel setzt die Leuchte explizit. Trägt der Raum keine
    bestimmbare Tür, wird nichts gesetzt (fail-closed — keine Leuchte an geratener
    Stelle). Quelle: `QUELLE_TUERLEUCHTE` (Referenz-Praxis, s. o.).
    """
    pflicht = [r for r in raum.raeume if (r.raum_typ or "").upper() in _TUERLEUCHTE_RAUMTYPEN]
    if not pflicht:
        return []
    assign_building = _building_assigner(
        [find_center_visual(r.polygon_mm)[0] for r in raum.raeume if len(r.polygon_mm) >= 3]
    )
    out: list[Platzierung] = []
    for r in pflicht:
        tuer = _tuer_des_raums(raum, r)
        if tuer is None:
            continue
        out.append(
            Platzierung(
                xy_mm=(tuer.xy_mm[0], tuer.xy_mm[1]),
                catalog_key=TUERLEUCHTE_KEY,
                rotation_deg=0.0,
                mirror_x=False,
                height_mm=TUERLEUCHTE_HOEHE_MM,
                kind="sicherheitsleuchte",
                richtung="gerade",
                circuit_hint=f"AGV-{assign_building(tuer.xy_mm[0])}-F{_AGV_SV_F}",
                covers_segment=[],
                norm_quelle=QUELLE_TUERLEUCHTE,
            )
        )
    return out
