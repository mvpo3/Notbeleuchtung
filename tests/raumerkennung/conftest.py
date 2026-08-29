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


# Echter LEERER Architektur-Input (in Metern!) — Gegenstück zum fertigen Plan.
MOLLGASSE_BLANK = REPO_ROOT / "Projekte" / "Mollgasse" / "Erdgeschoß.dxf"


@pytest.fixture
def mollgasse_blank_eg() -> Path:
    if not MOLLGASSE_BLANK.exists():
        pytest.skip(f"Leerer Mollgasse-Input fehlt: {MOLLGASSE_BLANK}")
    return MOLLGASSE_BLANK


def build_synth_dxf(path: Path) -> Path:
    """Deterministische Mini-DXF (mm): zwei Räume, ein Stempel, eine Tür.

    Layout (mm): Außenrechteck 0..8000 × 0..5000, Trennwand bei x=5000 →
    linker Raum (5×5 m) + rechter Raum (3×5 m). MTEXT 'STIEGENHAUS' im linken
    Raum. TÜR-80-INSERT in der Trennwand. Fluchtweg-Polyline auf 09-WEG.
    """
    import ezdxf

    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4  # mm
    msp = doc.modelspace()
    for lyr in ("02-TWA-G00-LEG-M0", "05-SYM-G00-LEG-M0",
                "01-TXT-G00-LEG-M0", "09-WEG-G00-LEG-M0"):
        if lyr not in doc.layers:
            doc.layers.add(lyr)
    W = "02-TWA-G00-LEG-M0"
    # Außenrechteck
    corners = [(0, 0), (8000, 0), (8000, 5000), (0, 5000)]
    for i in range(4):
        a, b = corners[i], corners[(i + 1) % 4]
        msp.add_line(a, b, dxfattribs={"layer": W})
    # Trennwand
    msp.add_line((5000, 0), (5000, 5000), dxfattribs={"layer": W})
    # Raumstempel im linken Raum
    msp.add_mtext("STIEGENHAUS", dxfattribs={"layer": "01-TXT-G00-LEG-M0"}
                  ).set_location((2500, 2500))
    # Tür in der Trennwand
    if "TÜR-80_10er-WAND" not in doc.blocks:
        doc.blocks.new("TÜR-80_10er-WAND")
    msp.add_blockref("TÜR-80_10er-WAND", (5000, 2500),
                     dxfattribs={"layer": "05-SYM-G00-LEG-M0"})
    # Fluchtweg
    msp.add_lwpolyline([(2500, 2500), (6500, 2500), (6500, 500)],
                       dxfattribs={"layer": "09-WEG-G00-LEG-M0"})
    doc.saveas(str(path))
    return path


@pytest.fixture
def synth_dxf(tmp_path) -> Path:
    return build_synth_dxf(tmp_path / "synth.dxf")
