"""Raum-Kaskade im Provider — dieselben Räume wie die Prüfstrecke.

Gegatet: die Prüf-DXF in ``Projekte/_eingang`` sind groß und ggf. untracked.
Referenz sind die Prüfstrecken-Kennzahlen (scripts/plan_pruefen.py):
Rennweg 14, Barawitzka 47, Mollgasse 62 Räume.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

EINGANG = Path(__file__).resolve().parents[2] / "Projekte" / "_eingang"


def _parse(name: str):
    dxf = EINGANG / f"{name}.dxf"
    if not dxf.exists():
        pytest.skip(f"Prüf-DXF fehlt: {dxf}")
    return ArchitekturRaumProvider().parse(str(dxf), "EG")


def _typisiert(rm) -> int:
    return sum(1 for r in rm.raeume if r.raum_typ and r.raum_typ != "UNBEKANNT")


def test_rennweg_raeume_und_tueren():
    rm = _parse("Rennweg_OG3")
    assert len(rm.raeume) >= 10
    assert _typisiert(rm) >= 10
    # Rennweg hat keine benannten Tür-Blöcke im Modelspace — die Türöffnungen
    # der Kaskade füllen den Contract (früher: 0 Türen).
    assert len(rm.tueren) >= 5


def test_barawitzka_raeume():
    rm = _parse("Barawitzka_EG")
    assert 41 <= len(rm.raeume) <= 47
    assert _typisiert(rm) >= 30


def test_mollgasse_raeume_kuratiert():
    rm = _parse("Mollgasse_EG")
    # Kuratierte Kaskade statt Rohflächen (früher 192 untypisierte Polygone).
    assert 55 <= len(rm.raeume) <= 70
    assert _typisiert(rm) >= 40
