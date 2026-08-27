"""platzierer — Leonis' echte Platzierungs-Logik (erfüllt das `Platzierer`-Port).

`NotlichtPlatzierer.place(raum, norm)` konsumiert Selmans `RaumModell` + Enis'
`NormProvider` und produziert das Contract-B `PlatzierungsErgebnis`. Er zeichnet
nichts (Render = Hauptengine, Slice 3) und importiert kein anderes Owner-Package —
nur die Contracts + die render-freie Strategy.

Slice 2: Rettungszeichen entlang der Fluchtweg-Segmente (siehe
`communal_stgh_strategy`). Antipanik / Sicherheitsleuchten folgen in späteren Slices.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import (
    NormProvider,
    PlatzierungsErgebnis,
    RaumModell,
)

from .communal_stgh_strategy import plan_rettungszeichen


class NotlichtPlatzierer:
    """Erfüllt `hauptengine.contracts.ports.Platzierer`."""

    def place(self, raum: RaumModell, norm: NormProvider) -> PlatzierungsErgebnis:
        platzierungen = plan_rettungszeichen(raum, norm)
        return PlatzierungsErgebnis(floor=raum.floor, platzierungen=platzierungen)
