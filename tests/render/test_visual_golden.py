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

from notbeleuchtung.hauptengine.contracts import (
    Platzierung,
    PlatzierungsErgebnis,
    RaumModell,
)
from notbeleuchtung.hauptengine.render import dxf_zu_pdf, render_dxf
from notbeleuchtung.symbols import library

pytestmark = pytest.mark.visual

FIXTURES = Path(__file__).parent.parent / "fixtures"
GOLDEN = FIXTURES / "golden"
FAILURES = Path(__file__).parent.parent / "failures"
PIXEL_SCHWELLE = 30.0  # je-Kanal-Abweichung (0..255), ab der ein Pixel als „verändert" gilt
ANTEIL_MAX = 0.002     # max. Anteil veränderter Pixel (0,2 %) — tolerant ggü. Font-Jitter


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


def _assert_matches_golden(png: Path, golden: Path, name: str) -> None:
    """Pixel-Diff gegen die Baseline (oder schreibt sie bei NOTBEL_UPDATE_GOLDEN neu)."""
    if os.environ.get("NOTBEL_UPDATE_GOLDEN") or not golden.exists():
        golden.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(png, golden)
        pytest.skip(f"Golden-Baseline (neu) geschrieben: {golden}")

    ist, soll = _rgb(png), _rgb(golden)

    def _overlay(diff: np.ndarray) -> Path:
        FAILURES.mkdir(parents=True, exist_ok=True)
        pfad = FAILURES / f"{name}_diff.png"
        mx = float(diff.max()) or 1.0
        mpimg.imsave(str(pfad), (diff / mx).clip(0, 1))
        return pfad

    # Shape-Mismatch: Diff auf der gemeinsamen Region schreiben, statt nur hart zu failen —
    # so sieht man auch bei Größen-Drift, WAS sich geändert hat.
    if ist.shape != soll.shape:
        h, w = min(ist.shape[0], soll.shape[0]), min(ist.shape[1], soll.shape[1])
        pfad = _overlay(np.abs(ist[:h, :w] - soll[:h, :w]))
        pytest.fail(f"Render-Shape {ist.shape} != Golden {soll.shape}. Diff (Region): {pfad}")

    # Lokalitäts-sensitiv: Anteil der Pixel mit spürbarer Abweichung (max je Kanal >
    # Schwelle) — ein reiner Mittelwert über ALLE Pixel maskiert kleine, aber echte
    # lokale Regressionen (verrutschte Legende) im großen weißen Hintergrund.
    per_pixel = np.abs(ist - soll).max(axis=2)
    anteil = float((per_pixel > PIXEL_SCHWELLE).mean())
    if anteil > ANTEIL_MAX:
        pfad = _overlay(np.abs(ist - soll))
        pytest.fail(
            f"Sicht-Abweichung: {anteil * 100:.3f}% Pixel > {PIXEL_SCHWELLE:g} "
            f"(erlaubt {ANTEIL_MAX * 100:g}%). Diff: {pfad}"
        )


def test_visual_golden_4og(tmp_path):
    png = _render_png(tmp_path)
    _assert_matches_golden(png, GOLDEN / "4og_notbeleuchtung.png", "4og_notbeleuchtung")


def _platzierung_mix() -> PlatzierungsErgebnis:
    """Realistische Misch-Szene für die Sicht-Golden — deckt die Render-Pfade ab, die der
    faithful-5-RZ-4og-Golden NICHT trägt und hinter denen C2 (Doppelpfeil) + der
    Belegungs-Overflow versteckt waren: RZ mit `richtung="gerade"` (beidseitiger
    Doppelpfeil), Sicherheitsleuchte + Antipanik als eigene Symbole, und eine
    Belegungsliste mit BL-Schaltungsart über zwei Kreise."""
    q = "ÖNORM EN 1838:2013 §4.2.1"

    def rz(xy, richtung, key, kreis):
        return Platzierung(xy_mm=xy, catalog_key=key, kind="rz", richtung=richtung,
                           rotation_deg=0.0, height_mm=2400.0, circuit_hint=kreis, norm_quelle=q)

    def sl(xy, kreis):
        return Platzierung(xy_mm=xy, catalog_key="sicherheitsleuchte_aufheller",
                           kind="sicherheitsleuchte", richtung="gerade", height_mm=2400.0,
                           circuit_hint=kreis, norm_quelle=q)

    def ap(xy, kreis):
        return Platzierung(xy_mm=xy, catalog_key="antipanik_leuchte", kind="antipanik",
                           richtung="gerade", height_mm=2400.0, circuit_hint=kreis, norm_quelle=q)

    plz = [
        rz((-60000.0, 20000.0), "gerade", "notlicht_ks_stiege", "AGV-A-F13"),  # Doppelpfeil
        rz((-45000.0, 20000.0), "rechts", "notlicht_ks_stiege_rechts", "AGV-A-F13"),
        sl((-70000.0, 33000.0), "AGV-A-F13"),
        sl((-52000.0, 33000.0), "AGV-B-F13"),
        sl((-40000.0, 6000.0), "AGV-B-F13"),
        ap((-73000.0, 34000.0), "AGV-B-F13"),
        ap((-37000.0, 7000.0), "AGV-B-F13"),
    ]
    return PlatzierungsErgebnis(floor="4OG", platzierungen=plz)


def test_visual_golden_mix(tmp_path):
    import ezdxf

    raum = RaumModell.model_validate(
        json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    )
    dxf = tmp_path / "mix.dxf"
    render_dxf(_platzierung_mix(), raum, dxf)

    # Selbst-validierend (kein blindes Golden): die Misch-Szene MUSS die Pfade wirklich
    # ausüben, sonst wacht der Pixel-Golden über nichts. 7 Platzierungen → 7 getaggte
    # INSERTs (XDATA sitzt je Platzierung am Primär-Block; der Doppelpfeil-Zweitblock
    # der „gerade"-RZ ist Deko derselben Platzierung, wie die Blatt-Legende ungetaggt).
    doc = ezdxf.readfile(str(dxf))
    inserts = [e for e in doc.modelspace().query("INSERT")
               if e.has_xdata("NOTBELEUCHTUNG")]   # Plan-Symbole; Blatt-Deko trägt kein XDATA
    assert len(inserts) == 7
    # Owner-Fixierung: Blatt-Modus trägt ALLES — keine Belegungs-Box daneben.
    assert not doc.modelspace().query("MTEXT[layer=='din_SIBEL_11_system']")

    png = tmp_path / "mix.png"
    dxf_zu_pdf(dxf, png, dpi=100)
    _assert_matches_golden(png, GOLDEN / "mix_notbeleuchtung.png", "mix_notbeleuchtung")
