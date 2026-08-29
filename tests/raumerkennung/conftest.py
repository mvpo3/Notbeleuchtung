"""Gemeinsame Fixtures für die Raumerkennungs-Tests.

Die echten Architektur-DXF (`Projekte/…`) sind groß und ggf. untracked — Tests
die sie brauchen werden per `skipif` gegatet, wenn die Datei fehlt.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
MOLLGASSE_DIR = REPO_ROOT / "Projekte" / "Mollgasse Notbeleuchtung"


def mollgasse_dxf(floor: str) -> Path:
    """Pfad zur Mollgasse-DXF eines Geschosses (z.B. 'EG', '4OG')."""
    return MOLLGASSE_DIR / f"WHA_MOL_{floor}.dxf"


@pytest.fixture
def mollgasse_eg() -> Path:
    p = mollgasse_dxf("EG")
    if not p.exists():
        pytest.skip(f"Mollgasse-DXF fehlt: {p}")
    return p
