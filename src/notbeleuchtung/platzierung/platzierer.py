"""platzierer — Leonis' echte Platzierungs-Logik (erfüllt das `Platzierer`-Port).

`NotlichtPlatzierer.place(raum, norm)` konsumiert Selmans `RaumModell` + Enis'
`NormProvider` und produziert das Contract-B `PlatzierungsErgebnis`. Er zeichnet
nichts (Render = Hauptengine) und importiert kein anderes Owner-Package.

Orchestriert den Fahrplan **Anker → Linie → Fläche → Deckung**:
* **RZ:** `anker_strategy` (graph-basiert, an Kreuzungen+Ausgängen) wenn der
  Zirkulationsgraph Kreuzungen hat (echter Graph); sonst Fallback auf die
  Segment-Strategie `communal_stgh_strategy` (dünnes 4OG-Fixture).
* **Sicherheitsleuchten + Antipanik:** raum-bezogen (`flaechen_strategy`).
* **Deckung:** Lux-getriebene Verdichtung der Korridore (`deckung`).
Alle Strategien sind norm-getrieben und render-frei.

**Photometrie (F2→F1-Naht):** `NotlichtPlatzierer(i_cd_fn=…)` nimmt optional ein
Lichtstärke-Callable `i_cd_fn(γ_grad) -> cd` — die richtungsabhängige Hersteller-
Photometrie (EULUMDAT/LDT). Die Hauptengine (`registry`) baut es aus
`normwissen.photometrie.Photometrie.intensitaet` und injiziert es beim Konstruieren;
`platzierung` bleibt so frei von `normwissen`-Imports (Owner-Grenze). Fehlt es, rechnet
die Deckung mit der konstanten isotropen Lichtstärke.
"""
from __future__ import annotations

from collections.abc import Callable

from notbeleuchtung.hauptengine.contracts import (
    LBVorgabe,
    NormProvider,
    OibBefund,
    PlatzierungsErgebnis,
    RaumModell,
)

from . import abstand_nachpass, circuit_zuordnung, deckungs_zuordnung, lb_override
from .anker_strategy import plan_rettungszeichen_anker
from .communal_stgh_strategy import plan_rettungszeichen
from .deckung import verdichte_fluchtweg
from .flaechen_strategy import plan_antipanik, plan_sicherheitsleuchten
from .gang_strategy import plan_rettungszeichen_gang
from .graph import build_circulation_graph, kreuzungs_anker
from .sonderstellen_strategy import plan_flag_raeume, plan_sonderstellen


def _plan_rettungszeichen(raum: RaumModell, norm: NormProvider):
    """RZ-Strategie nach Verfügbarkeit des Fluchtweg-Wissens:

    1. **Anker** (Graph-Kreuzungen degree>=3) — echter Zirkulationsgraph (Selman).
    2. **Segment** — 1 RZ je Fluchtweg-Segment (dünnes 4OG-Fixture, faithful 5 RZ).
    3. **GANG-Fallback** — weder Kreuzung noch Segment (fremde CAD-Familie ohne
       erkannten Fluchtweg-Layer): RZ entlang der GANG-Mittelachsen, damit die
       Engine auch ohne Fluchtweg-Layer RZ setzt (fischamender-Bug B2)."""
    if kreuzungs_anker(build_circulation_graph(raum)):
        return plan_rettungszeichen_anker(raum, norm)
    segment_rz = plan_rettungszeichen(raum, norm)
    if segment_rz:
        return segment_rz
    return plan_rettungszeichen_gang(raum, norm)


class NotlichtPlatzierer:
    """Erfüllt `hauptengine.contracts.ports.Platzierer`."""

    def __init__(self, i_cd_fn: Callable[[float], float] | None = None) -> None:
        # Richtungsabhängige Hersteller-Lichtstärke (aus F2-Photometrie); None = konstant.
        self._i_cd_fn = i_cd_fn

    def place(
        self,
        raum: RaumModell,
        norm: NormProvider,
        lb: LBVorgabe | None = None,
        *,
        oib: OibBefund | None = None,
    ) -> PlatzierungsErgebnis:
        platzierungen = [
            *_plan_rettungszeichen(raum, norm),          # Anker
            *plan_sicherheitsleuchten(raum, norm),       # Betonungspunkte (Aufheller)
            *plan_antipanik(raum, norm, oib=oib),        # Fläche (Trigger OIB-gegated)
            *plan_sonderstellen(raum, norm),             # Pflichtstellen §4.1.2 (SL+RZ)
            *plan_flag_raeume(raum, norm),               # barrierefrei/Gefährdung (Flags)
            *verdichte_fluchtweg(raum, norm, i_cd_fn=self._i_cd_fn),  # Linie + Deckung (Lux)
        ]
        # 2. Input: explizite LB-Vorgaben übersteuern die norm-getriebene Platzierung.
        platzierungen = lb_override.anwenden(platzierungen, raum, lb)
        # Kollisionen an der Strategie-Naht auflösen (Dubletten mergen, verschieden-artige
        # entzerren) — nach lb_override (das SL hinzufügt), vor der Deckungs-Zuordnung,
        # damit diese die finalen Positionen sieht.
        platzierungen = abstand_nachpass.entzerre(platzierungen, raum)
        # Fluchtweg-Deckung nachträglich geometrisch zuordnen (füllt covers_segment,
        # das die RZ-Strategien selbst nicht setzen) → Deckungs-Prüfung wird aussagekräftig.
        platzierungen = deckungs_zuordnung.zuordnen(platzierungen, raum, norm)
        # Stromkreise final vergeben: Dauer-/Bereitschaftslicht trennen + je Kreis deckeln
        # (statt alles grob auf AGV-{Gebäude}-F13 zu mischen). Läuft zuletzt, nach lb_override.
        platzierungen = circuit_zuordnung.zuordnen(platzierungen)
        return PlatzierungsErgebnis(floor=raum.floor, platzierungen=platzierungen)
