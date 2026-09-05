"""Fake-Provider für Slice 0 — liefern die Golden-Fixtures.

Jeder Owner testet gegen diese Doubles der Nachbarn, nie gegen deren echten Code.
Werden Slice 1/2/4 einzeln durch echte Provider (registry.build_default_bundle)
ersetzt.
"""
from __future__ import annotations

import json
from pathlib import Path

from notbeleuchtung.hauptengine.contracts import (
    BereichsRegel,
    FluchtwegSegment,
    Gebaeudeteil,
    LBVorgabe,
    NormAnforderung,
    NormRegelwerk,
    OibBefund,
    OibErgebnis,
    PlatzierungsErgebnis,
    ProjektKontext,
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


class FakeLBProvider:
    """Enis-Double für den 2. Input — parst „irgendeine LB-Datei" in eine feste
    `LBVorgabe`, die Sicherheitsbeleuchtung im STIEGENHAUS ausschließt (Fischa-GK4-Fall).
    Der Inhalt der Datei ist egal — geprüft wird nur, dass der LB-Pfad durch die
    Pipeline bis in die Override-Schicht fließt."""

    def parse_lb(self, lb_path: str) -> LBVorgabe:
        return LBVorgabe(
            projekt="Fake-GK4",
            bereiche_exklusion=[
                BereichsRegel(raum_typ="STIEGENHAUS", sicherheitsbeleuchtung=False, begruendung="GK4"),
            ],
            lb_quelle=lb_path,
        )


def build_fake_bundle() -> ProviderBundle:
    """Nur Raum noch Fake (Slice 4) — Norm ab Slice 1 und Platzierer ab Slice 2 ECHT."""
    return ProviderBundle(
        raum=FakeRaumProvider(),
        norm=En1838NormProvider(),
        platzierer=NotlichtPlatzierer(),
    )


def build_fake_bundle_mit_lb() -> ProviderBundle:
    """Wie `build_fake_bundle`, aber mit verdrahtetem LB-Provider (2. Input aktiv)."""
    bundle = build_fake_bundle()
    bundle.lb = FakeLBProvider()
    return bundle


class FakeLBReviewProvider:
    """Enis-Double für den FAIL-CLOSED-Fall: der Parser bricht mit `LbFehler` ab.

    So verhält sich `LbTextProvider`, wenn die LB einen blockierenden Befund trägt
    (kein Notbeleuchtungs-Abschnitt, ausgelagerter Verweis, unbekannter Raumtyp …).
    `meldung` ist frei setzbar, damit die Header-Kürzung prüfbar bleibt.
    """

    def __init__(self, meldung: str | None = None) -> None:
        self._meldung = meldung or (
            "LB erfordert manuelle Prüfung (test.pdf) — notbeleuchtungs_abschnitt: "
            "Kein Abschnitt zur Notbeleuchtung gefunden."
        )

    def parse_lb(self, lb_path: str) -> LBVorgabe:
        from notbeleuchtung.normwissen.lb import LbFehler

        raise LbFehler(self._meldung)


def build_fake_bundle_mit_lb_review(meldung: str | None = None) -> ProviderBundle:
    """Wie `build_fake_bundle_mit_lb`, aber der LB-Provider verlangt Review."""
    bundle = build_fake_bundle()
    bundle.lb = FakeLBReviewProvider(meldung)
    return bundle


class FakeOibProvider:
    """OIB-Double — fester Erforderlichkeits-Befund (Stufe je Konstruktor).

    Ignoriert die Projektfakten; je Gebäudeteil des ProjektKontext ein Ergebnis mit
    der gesetzten Stufe. So üben die Tests das Flächen-Trigger-Gate (offen/zu/
    fail-closed), ohne an Enis' echter Tabelle-6-Auswertung zu hängen."""

    def __init__(self, stufe: str = "eingeschraenkt") -> None:
        self._stufe = stufe

    def bewerte_oib(self, projekt: ProjektKontext) -> OibBefund:
        teile = projekt.gebaeudeteile or [
            Gebaeudeteil(id="teil_1", nutzungsart="SONSTIGES_GEBAEUDE")
        ]
        return OibBefund(
            ergebnisse=[
                OibErgebnis(
                    gebaeudeteil_id=t.id,
                    stufe=self._stufe,
                    quelle="OIB-RL 2 Tabelle 6 (Fake)",
                    norm_ausgabe="Mai 2023 (Fake)",
                    # Echo wie der echte OibRl2Provider (raum-genaues Gate v2 testbar).
                    raum_referenzen=list(t.raum_referenzen),
                )
                for t in teile
            ]
        )


def build_fake_bundle_mit_oib(stufe: str = "eingeschraenkt") -> ProviderBundle:
    """Wie `build_fake_bundle`, aber mit verdrahtetem OIB-Provider (3. Input aktiv)."""
    bundle = build_fake_bundle()
    bundle.oib = FakeOibProvider(stufe)
    return bundle
