"""Fake-Provider für Slice 0 — liefern die Golden-Fixtures.

Jeder Owner testet gegen diese Doubles der Nachbarn, nie gegen deren echten Code.
Werden Slice 1/2/4 einzeln durch echte Provider (registry.build_default_bundle)
ersetzt.
"""
from __future__ import annotations

import json
from pathlib import Path

from notbeleuchtung.hauptengine.contracts import (
    FluchtwegSegment,
    NormAnforderung,
    NormRegelwerk,
    PlatzierungsErgebnis,
    ProviderBundle,
    RaumModell,
)
from notbeleuchtung.normwissen import En1838NormProvider
from notbeleuchtung.platzierung import NotlichtPlatzierer

FIXTURES = Path(__file__).parent / "fixtures"


def _load(name: str) -> dict:
    with open(FIXTURES / name, encoding="utf-8") as fh:
        return json.load(fh)


class FakeRaumProvider:
    """Selman-Double — RaumModell aus Fixture."""

    def parse(self, dxf_path: str, floor: str) -> RaumModell:
        return RaumModell.model_validate(_load("raum_modell_4og.json"))


# Enis' Norm-Provider ist ab Slice 1 echt: der Durchstich (build_fake_bundle) läuft
# über En1838NormProvider aus normwissen/data/*.yaml. FakeNormProvider bleibt als
# Nachbar-Double für Owner-Unit-Tests stehen (tests/platzierung), damit Leonis
# gegen ein stabiles Snapshot-Double testet statt gegen Enis' echten Code.


class FakeNormProvider:
    """Enis-Double — Query-API gegen den Snapshot-Fixture."""

    def __init__(self) -> None:
        self._snapshot = NormRegelwerk.model_validate(_load("norm_regelwerk_snapshot.json"))
        self._by_typ = {(r.raum_typ, r.ist_fluchtweg): r.anforderung for r in self._snapshot.regeln}

    def fuer_raum(self, raum_typ: str, ist_fluchtweg: bool) -> NormAnforderung:
        hit = self._by_typ.get((raum_typ, ist_fluchtweg))
        if hit is not None:
            return hit
        # Default: Rettungsweg-Anforderung
        return NormAnforderung(
            min_lux=1.0, klassifikation="rz", montagehoehe_mm=2400,
            erkennungsweite_m=30.0, symbol_katalog_keys=["notlicht_ks_stiege"],
            mindest_anzahl=1, dauer_min=60, quelle="ÖNORM EN 1838:2013 §4.2.1",
        )

    def fuer_fluchtweg_abschnitt(self, segment: FluchtwegSegment) -> NormAnforderung:
        return self.fuer_raum("GANG", True)

    def erkennungsweite_m(self, piktogramm_hoehe_m: float, hinterleuchtet: bool) -> float:
        z = self._snapshot.erkennungsweite.z_hinterleuchtet if hinterleuchtet \
            else self._snapshot.erkennungsweite.z_beleuchtet
        return z * piktogramm_hoehe_m

    def regelwerk_snapshot(self) -> NormRegelwerk:
        return self._snapshot


class FakePlatzierer:
    """Leonis-Double — PlatzierungsErgebnis aus Fixture (ignoriert Input).

    Slice 0-Referenz. Der E2E-Durchstich nutzt ab Slice 2 den echten
    `NotlichtPlatzierer` (siehe `build_fake_bundle`)."""

    def place(self, raum: RaumModell, norm, lb=None) -> PlatzierungsErgebnis:
        return PlatzierungsErgebnis.model_validate(_load("platzierung_4og.json"))


def build_fake_bundle() -> ProviderBundle:
    """Nur Raum noch Fake (Slice 4) — Norm ab Slice 1 und Platzierer ab Slice 2 ECHT."""
    return ProviderBundle(
        raum=FakeRaumProvider(),
        norm=En1838NormProvider(),
        platzierer=NotlichtPlatzierer(),
    )
