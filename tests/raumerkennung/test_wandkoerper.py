"""Tests für wandkoerper (Erscheinungsbild-Erkennung) + tueren.tuer_oeffnungen.

Die echten Pläne liegen in `Projekte/_eingang/` und sind ggf. untracked —
Tests skippen, wenn die Datei fehlt (gleiches Gate-Muster wie conftest).
"""
from __future__ import annotations

import statistics
from pathlib import Path

import pytest

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.tueren import tuer_oeffnungen
from notbeleuchtung.raumerkennung.wandkoerper import (
    Wandkoerper,
    aussenkontur,
    bounds_aus_wandkoerpern,
    finde_wandkoerper,
    wand_union,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
EINGANG = REPO_ROOT / "Projekte" / "_eingang"


def _plan(name: str):
    p = EINGANG / name
    if not p.exists():
        pytest.skip(f"Plan fehlt: {p}")
    return lade_dxf(p)


@pytest.fixture(scope="module")
def rennweg():
    return _plan("Rennweg_OG3.dxf")


@pytest.fixture(scope="module")
def mollgasse():
    return _plan("Mollgasse_EG.dxf")


@pytest.fixture(scope="module")
def barawitzka():
    return _plan("Barawitzka_EG.dxf")


# ── Rennweg (ArchiCAD, Wände als HATCHes in Wall_N-Blöcken, mm) ─────────────
def test_rennweg_wandkoerper(rennweg):
    wk = finde_wandkoerper(rennweg)
    assert len(wk) >= 50
    # Blöcke liegen in Weltkoordinaten — kein doppelter Insert-Offset:
    # alle Körper müssen im Plan-Fenster (~12.5e6 / 356e6 mm) liegen.
    b = bounds_aus_wandkoerpern(wk)
    assert 12.0e6 < b.min_xy[0] and b.max_xy[0] < 13.0e6
    assert 356.0e6 < b.min_xy[1] and b.max_xy[1] < 357.0e6
    assert any(k.quelle.startswith("block:Wall_") for k in wk)
    beton = [k.breite_mm for k in wk if k.material == "STAHLBETON"]
    assert beton, "kein Stahlbeton erkannt"
    assert 150.0 <= statistics.median(beton) <= 250.0
    assert len(wand_union(wk).geoms) <= 15


def test_rennweg_tueroeffnungen(rennweg):
    bloecke = [t for t in tuer_oeffnungen(rennweg) if t.quelle == "block"]
    assert len(bloecke) == 11  # Zargentür_1_Fl 10[1..11]
    assert {t.breite_mm for t in bloecke} == {840.0, 940.0}


# ── Mollgasse (msp-HATCHes in Metern, TÜR-80-Blockfamilie) ──────────────────
def test_mollgasse_wandkoerper(mollgasse):
    wk = finde_wandkoerper(mollgasse)
    assert len(wk) >= 100
    assert any("GK" in k.layer for k in wk), "GK-Trennwände fehlen"
    # Belagsflächen (LILA/GRÜN) sind keine Wände.
    assert not any("LILA" in k.layer or "GR" in k.layer.upper()[-4:] for k in wk)


def test_mollgasse_tueroeffnungen(mollgasse):
    oeffnungen = tuer_oeffnungen(mollgasse)
    assert len([t for t in oeffnungen if t.quelle == "block"]) >= 35


# ── Barawitzka (SOLID-Fragmente, Türen nur als Schwenkbogen-ARCs) ───────────
def test_barawitzka_wandkoerper(barawitzka):
    wk = finde_wandkoerper(barawitzka)
    assert len(wk) >= 100
    # Nur die Stempel-Variante (PP_2) — Icon_1/Icon_3-Duplikate gefiltert.
    assert not any("Icon_" in k.layer for k in wk)


def test_barawitzka_tueroeffnungen(barawitzka):
    arcs = [t for t in tuer_oeffnungen(barawitzka) if t.quelle == "arc"]
    assert len(arcs) >= 20


# ── Fallback: Doppellinien-Wände (synthetisch) ──────────────────────────────
@pytest.fixture
def doppellinien_dxf(tmp_path):
    import ezdxf

    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    doc.layers.add("02-TWA-G00-LEG-M0")
    msp = doc.modelspace()
    msp.add_line((0, 0), (20000, 0), dxfattribs={"layer": "02-TWA-G00-LEG-M0"})
    msp.add_line((0, 100), (20000, 100), dxfattribs={"layer": "02-TWA-G00-LEG-M0"})
    p = tmp_path / "doppellinie.dxf"
    doc.saveas(str(p))
    return p


def test_doppellinien_fallback(doppellinien_dxf):
    wk = finde_wandkoerper(lade_dxf(doppellinien_dxf))
    assert len(wk) == 1
    (k,) = wk
    assert isinstance(k, Wandkoerper)
    assert k.breite_mm == pytest.approx(100.0, abs=1.0)
    assert k.quelle == "msp"
    u = wand_union(wk)
    assert u.area == pytest.approx(20000 * 100, rel=0.05)
    assert aussenkontur(wk).area == pytest.approx(u.area, rel=0.01)
    b = bounds_aus_wandkoerpern(wk)
    assert b.max_xy[0] == pytest.approx(20000, abs=1.0)


def test_bounds_aus_wandkoerpern_leer():
    with pytest.raises(ValueError):
        bounds_aus_wandkoerpern([])
