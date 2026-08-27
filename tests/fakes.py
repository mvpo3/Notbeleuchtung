"""Fake-Provider für Slice 0 — liefern die Golden-Fixtures.

Jeder Owner testet gegen diese Doubles der Nachbarn, nie gegen deren echten Code.
Werden Slice 1/2/4 einzeln durch echte Provider (registry.build_default_bundle)
ersetzt.
"""
from __future__ import annotations

import json
from pathlib import Path

from notbeleuchtung.hauptengine.contracts import (
    PlatzierungsErgebnis,
    ProviderBundle,
    RaumModell,
)
from notbeleuchtung.normwissen import En1838NormProvider

FIXTURES = Path(__file__).parent / "fixtures"


def _load(name: str) -> dict:
    with open(FIXTURES / name, encoding="utf-8") as fh:
        return json.load(fh)


class FakeRaumProvider:
    """Selman-Double — RaumModell aus Fixture."""

    def parse(self, dxf_path: str, floor: str) -> RaumModell:
        return RaumModell.model_validate(_load("raum_modell_4og.json"))


# Enis' Norm-Provider ist ab Slice 1 echt (En1838NormProvider aus data/*.yaml) —
# kein Fake mehr. Erster sanktionierter Fake→echt-Swap; Raum + Platzierer bleiben
# Fake, bis ihre Slices (4/2) landen.


class FakePlatzierer:
    """Leonis-Double — PlatzierungsErgebnis aus Fixture (ignoriert Input)."""

    def place(self, raum: RaumModell, norm) -> PlatzierungsErgebnis:
        return PlatzierungsErgebnis.model_validate(_load("platzierung_4og.json"))


def build_fake_bundle() -> ProviderBundle:
    return ProviderBundle(
        raum=FakeRaumProvider(),
        norm=En1838NormProvider(),
        platzierer=FakePlatzierer(),
    )
