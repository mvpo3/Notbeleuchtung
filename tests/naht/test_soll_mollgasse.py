"""Soll-Tests Mollgasse EG — teilweise schon erreicht, dann scharf.

Ist-Prüfung 2026-09-06 (``ArchitekturRaumProvider().parse('Projekte/_eingang/
Mollgasse_EG.dxf', 'EG')``): **2 STIEGENHAUS-Räume** (Soll ≥2 erfüllt →
scharfer Test, kein xfail), **0 LIFT-Räume** (LIFT-Block mit Achsenkreuz
statt X wird nicht erkannt → xfail strict).
"""
from pathlib import Path

import pytest

PLAN = Path("Projekte/_eingang/Mollgasse_EG.dxf")


@pytest.fixture(scope="module")
def rm():
    if not PLAN.exists():                        # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {PLAN}")
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ArchitekturRaumProvider().parse(str(PLAN), "EG")


def test_zwei_stiegenhaus_raeume(rm):
    """Scharf: Ist 2026-09-06 = 2 STIEGENHAUS (Stempel-Typisierung greift)."""
    stgh = [r for r in rm.raeume if r.raum_typ == "STIEGENHAUS"]
    assert len(stgh) >= 2, f"nur {len(stgh)} STIEGENHAUS-Räume"


@pytest.mark.xfail(
    strict=True,
    reason="LIFT-Block (1.65×1.90 m, Achsenkreuz statt X, Blockname LIFT) wird nicht erkannt",
)
def test_soll_zwei_lift_raeume(rm):
    lifte = [r for r in rm.raeume if r.raum_typ == "LIFT"]
    assert len(lifte) >= 2, f"nur {len(lifte)} LIFT-Räume"
