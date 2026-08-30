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
    NormProvider,
    PlatzierungsErgebnis,
    RaumModell,
)

from .anker_strategy import plan_rettungszeichen_anker
from .communal_stgh_strategy import plan_rettungszeichen
from .deckung import verdichte_fluchtweg
from .flaechen_strategy import plan_antipanik, plan_sicherheitsleuchten
from .graph import build_circulation_graph, kreuzungs_anker


def _plan_rettungszeichen(raum: RaumModell, norm: NormProvider):
    """Anker-Strategie, wenn der Graph Kreuzungen (degree>=3) hat — sonst Segment-
    Fallback. So nutzt ein echter Zirkulationsgraph (Selman) die saubere Anker-
    Platzierung, während das dünne Fixture die faithful 5-RZ-Reproduktion behält."""
    if kreuzungs_anker(build_circulation_graph(raum)):
        return plan_rettungszeichen_anker(raum, norm)
    return plan_rettungszeichen(raum, norm)


class NotlichtPlatzierer:
    """Erfüllt `hauptengine.contracts.ports.Platzierer`."""

    def place(self, raum: RaumModell, norm: NormProvider) -> PlatzierungsErgebnis:
        platzierungen = [
            *_plan_rettungszeichen(raum, norm),          # Anker
            *plan_sicherheitsleuchten(raum, norm),       # Betonungspunkte (Aufheller)
            *plan_antipanik(raum, norm),                 # Fläche
            *verdichte_fluchtweg(raum, norm),            # Linie + Deckung (Lux)
        ]
        return PlatzierungsErgebnis(floor=raum.floor, platzierungen=platzierungen)
