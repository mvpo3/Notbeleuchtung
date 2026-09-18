"""Raum-Kaskade im Provider — dieselben Räume wie die Prüfstrecke.

Gemessen wird auf den versionierten Plänen unter ``Projekte/`` (siehe
``tests/plaene.py``). Referenz sind die Prüfstrecken-Kennzahlen
(scripts/plan_pruefen.py): Rennweg 14, Barawitzka 47, Mollgasse 62 Räume.
"""
from __future__ import annotations

from pathlib import Path

from notbeleuchtung.raumerkennung import ArchitekturRaumProvider
from plaene import BARAWITZKA_EG, MOLLGASSE_EG, RENNWEG_OG3, plan


def _parse(dxf: Path):
    return ArchitekturRaumProvider().parse(str(plan(dxf)), "EG")


def _typisiert(rm) -> int:
    return sum(1 for r in rm.raeume if r.raum_typ and r.raum_typ != "UNBEKANNT")


def test_rennweg_raeume_und_tueren():
    rm = _parse(RENNWEG_OG3)
    assert len(rm.raeume) >= 10
    assert _typisiert(rm) >= 10
    # Rennweg hat keine benannten Tür-Blöcke im Modelspace — die Türöffnungen
    # der Kaskade füllen den Contract (früher: 0 Türen).
    assert len(rm.tueren) >= 5


def test_barawitzka_raeume():
    rm = _parse(BARAWITZKA_EG)
    # Obergrenze 47 → 53 (Fachteil 2): lift_erkennung ergänzt ADDITIV echte
    # LIFT-Räume (Plan-Texte »Aufzug 1/2«, »Lifttüre 90/200«), die die
    # Prüfstrecken-Referenz (47) nicht kannte. Ist 2026-09-07: 50 (davon 3 LIFT).
    assert 41 <= len(rm.raeume) <= 53
    assert _typisiert(rm) >= 30


def test_mollgasse_raeume_kuratiert():
    rm = _parse(MOLLGASSE_EG)
    # Kuratierte Kaskade statt Rohflächen (früher 192 untypisierte Polygone).
    assert 55 <= len(rm.raeume) <= 70
    assert _typisiert(rm) >= 40
