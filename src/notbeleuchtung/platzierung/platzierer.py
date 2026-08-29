"""platzierer — Leonis' echte Platzierungs-Logik (erfüllt das `Platzierer`-Port).

`NotlichtPlatzierer.place(raum, norm)` konsumiert Selmans `RaumModell` + Enis'
`NormProvider` und produziert das Contract-B `PlatzierungsErgebnis`. Er zeichnet
nichts (Render = Hauptengine, Slice 3) und importiert kein anderes Owner-Package —
nur die Contracts + die render-freie Strategy.

Rettungszeichen entlang der Fluchtweg-Segmente (`communal_stgh_strategy`) +
raum-bezogene Sicherheitsleuchten / Antipanik (`flaechen_strategy`). Alle drei
Strategien sind norm-getrieben und render-frei.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import (
    NormProvider,
    PlatzierungsErgebnis,
    RaumModell,
)

from .communal_stgh_strategy import plan_rettungszeichen
from .flaechen_strategy import plan_antipanik, plan_sicherheitsleuchten


class NotlichtPlatzierer:
    """Erfüllt `hauptengine.contracts.ports.Platzierer`."""

    def place(self, raum: RaumModell, norm: NormProvider) -> PlatzierungsErgebnis:
        platzierungen = [
            *plan_rettungszeichen(raum, norm),
            *plan_sicherheitsleuchten(raum, norm),
            *plan_antipanik(raum, norm),
        ]
        return PlatzierungsErgebnis(floor=raum.floor, platzierungen=platzierungen)
