"""Soll-Tests Baufeld E2 — Zielbild (xfail strict), skip solange nur als Zip.

Das Projekt liegt im Repo nur als ``Projekte/Baufeld_E2.zip`` (731 MB
unkomprimiert) — entpackt jemand nach ``Projekte/Baufeld E2/``, laufen die
Solls gegen den ersten dort gefundenen DXF.
"""
from pathlib import Path

import pytest

ORDNER = Path("Projekte/Baufeld E2")


@pytest.fixture(scope="module")
def rm():
    if not ORDNER.is_dir():                      # pragma: no cover — Zip nicht entpackt
        pytest.skip(f"Baufeld E2 nicht entpackt: {ORDNER} (Projekte/Baufeld_E2.zip)")
    dxfs = sorted(ORDNER.rglob("*.dxf"))
    if not dxfs:                                 # pragma: no cover
        pytest.skip(f"kein DXF unter {ORDNER}")
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ArchitekturRaumProvider().parse(str(dxfs[0]), "EG")


@pytest.mark.xfail(strict=True, reason="Baufeld nie gegen die Erkennung gelaufen — Soll ungeprüft")
def test_soll_mindestens_ein_ausgang(rm):
    assert len(rm.ausgaenge) >= 1, "kein Ausgang erkannt"


@pytest.mark.xfail(strict=True, reason="Baufeld nie gegen die Erkennung gelaufen — Soll ungeprüft")
def test_soll_mindestens_ein_segment(rm):
    assert len(rm.zirkulation.segmente) >= 1, "kein Fluchtweg-Segment erkannt"
