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
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import (
    LBVorgabe,
    NormProvider,
    PlatzierungsErgebnis,
    RaumModell,
)

from . import lb_override
from .anker_strategy import plan_rettungszeichen_anker
from .communal_stgh_strategy import plan_rettungszeichen
from .deckung import verdichte_fluchtweg
from .flaechen_strategy import plan_antipanik, plan_sicherheitsleuchten
from .gang_strategy import plan_rettungszeichen_gang
from .graph import build_circulation_graph, kreuzungs_anker


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

    def place(
        self, raum: RaumModell, norm: NormProvider, lb: LBVorgabe | None = None
    ) -> PlatzierungsErgebnis:
        platzierungen = [
            *_plan_rettungszeichen(raum, norm),          # Anker
            *plan_sicherheitsleuchten(raum, norm),       # Betonungspunkte (Aufheller)
            *plan_antipanik(raum, norm),                 # Fläche
            *verdichte_fluchtweg(raum, norm),            # Linie + Deckung (Lux)
        ]
        # 2. Input: explizite LB-Vorgaben übersteuern die norm-getriebene Platzierung.
        platzierungen = lb_override.anwenden(platzierungen, raum, lb)
        return PlatzierungsErgebnis(floor=raum.floor, platzierungen=platzierungen)
