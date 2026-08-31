"""Visual-DoD-Golden — render → Raster (PNG) → Pixel-Diff gegen eingecheckte Baseline.

Sicht-Regression für den gerenderten Plan: schlägt der Diff über die Toleranz, wird ein
Diff-Overlay nach `tests/failures/` geschrieben (gitignored) und der Test failt mit dem
Pfad. So sieht man Layout-Regressionen (verrutschte Legende, fehlende Koten …), die die
Entity-Readback-Tests (`test_render_dxf.py`) nicht fangen.

Marker `visual` → default deselektiert (langsam). Lauf:
    .venv/Scripts/python.exe -m pytest -m visual
Baseline (neu) schreiben (nach bewusster Render-Änderung):
    NOTBEL_UPDATE_GOLDEN=1 .venv/Scripts/python.exe -m pytest -m visual
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest

pytest.importorskip("matplotlib")

import matplotlib.image as mpimg
import numpy as np

from notbeleuchtung.hauptengine.contracts import PlatzierungsErgebnis, RaumModell
from notbeleuchtung.hauptengine.render import dxf_zu_pdf, render_dxf
from notbeleuchtung.symbols import library

pytestmark = pytest.mark.visual

FIXTURES = Path(__file__).parent.parent / "fixtures"
GOLDEN = FIXTURES / "golden"
FAILURES = Path(__file__).parent.parent / "failures"
TOLERANZ = 2.0  # mittlere absolute Abweichung je Kanal (0..255), matplotlib-jitter-tolerant


@pytest.fixture(autouse=True)
def _fresh_cache():
    library.reset_cache()
    yield
    library.reset_cache()


def _render_png(tmp_path: Path) -> Path:
    platzierung = PlatzierungsErgebnis.model_validate(
        json.loads((FIXTURES / "platzierung_4og.json").read_text(encoding="utf-8"))
    )
    raum = RaumModell.model_validate(
        json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    )
    dxf = tmp_path / "plan.dxf"
    render_dxf(platzierung, raum, dxf)
    png = tmp_path / "plan.png"
    dxf_zu_pdf(dxf, png, dpi=100)  # .png-Endung → matplotlib schreibt PNG statt PDF
    return png


def _rgb(pfad: Path) -> np.ndarray:
    """PNG als HxWx3-float-Array (0..255), Alpha verworfen."""
    arr = mpimg.imread(str(pfad)).astype(float)
    if arr.ndim == 3 and arr.shape[2] == 4:
        arr = arr[:, :, :3]
    return arr * 255.0 if arr.max() <= 1.0 else arr


def test_visual_golden_4og(tmp_path):
    png = _render_png(tmp_path)
    golden = GOLDEN / "4og_notbeleuchtung.png"

    if os.environ.get("NOTBEL_UPDATE_GOLDEN") or not golden.exists():
        golden.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(png, golden)
        pytest.skip(f"Golden-Baseline (neu) geschrieben: {golden}")

    ist, soll = _rgb(png), _rgb(golden)
    assert ist.shape == soll.shape, f"Render-Shape {ist.shape} != Golden {soll.shape}"

    diff = np.abs(ist - soll)
    mittel = float(diff.mean())
    if mittel > TOLERANZ:
        FAILURES.mkdir(parents=True, exist_ok=True)
        overlay = FAILURES / "4og_notbeleuchtung_diff.png"
        mpimg.imsave(str(overlay), (diff / diff.max()).clip(0, 1))
        pytest.fail(f"Sicht-Abweichung {mittel:.2f} > {TOLERANZ} (Toleranz). Diff: {overlay}")
