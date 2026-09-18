"""Tests für wandkoerper (Erscheinungsbild-Erkennung) + tueren.tuer_oeffnungen.

Die Familien-Pläne sind versioniert (`tests/plaene.py`) — fehlt einer, ist das
ein Fehler. Nur der Fischamender-Plan BT1 EG behält sein Skip-Gate.
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
from plaene import BARAWITZKA_EG, MOLLGASSE_EG, RENNWEG_OG3
from plaene import plan as pruefe_plan

REPO_ROOT = Path(__file__).resolve().parents[2]


def _plan(pfad: Path):
    return lade_dxf(pruefe_plan(pfad))


@pytest.fixture(scope="module")
def rennweg():
    return _plan(RENNWEG_OG3)


@pytest.fixture(scope="module")
def mollgasse():
    return _plan(MOLLGASSE_EG)


@pytest.fixture(scope="module")
def barawitzka():
    return _plan(BARAWITZKA_EG)


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


# ── Fischamender BT1 EG (Wrapper-Block-Plan, ein Layer A_Waende) ─────────────
BT1_EG = (REPO_ROOT / "Projekte" / "BVH Fischamenderstraße"
          / "fertige Elektromontagepläne" / "BT1"
          / "Elektromontageapläne_ERDGESCHOSS BT1.dxf")


def test_fischamender_bt1_eg_wandkoerper():
    """Die Familie liefert Wandkörper — ausdrücklich NICHT 0.

    Bauform: `plan.space` ist der Wrapper-Block '65465465' (nicht der
    Modelspace), die Wände liegen doppelt dargestellt (HATCH + Linienzug) auf
    EINEM Layer `A_Waende`, überwiegend direkt im Wrapper, ein Teil eine
    Block-Ebene tiefer — `finde_wandkoerper` steigt dafür selbst ab.

    Ist-Stand 3d91a2c (selbst gemessen, 12 s): 241 Wandkörper, davon 195 `msp`
    + 46 aus Blöcken, 210 auf `A_Waende`. Die Bänder (≥150 / ≥150) sind
    GESETZT, nicht kalibriert — Abstand zum Ist als Luft für Plan-Varianten.
    Anlass: die Behauptung »BT1-EG hat 0 Wandkörper« (2026-09-12) war ein
    Messfehler (`len(getattr(modell, "wandkoerper", []))` auf einem
    RaumModell, das dieses Feld nicht führt). Fällt diese Familie je wirklich
    auf 0, bricht dieser Test statt still 126 Durchgangs-Türen zu verlieren.
    """
    if not BT1_EG.exists():
        pytest.skip(f"Plan fehlt: {BT1_EG}")
    plan = lade_dxf(BT1_EG)
    # Mindestaussagen statt Gleichheit: die konkrete Block-Nummer und der
    # genaue Layer-Name sind Ist-Werte DIESER einen Datei — ein Variantenexport
    # wuerde sie ohne Sachgrund brechen. Tragend ist die BAUFORM: plan.space
    # ist nicht der Modelspace, und es gibt einen erkannten Wand-Layer.
    assert plan.space is not plan.doc.modelspace()
    assert plan.wall_layers
    wk = finde_wandkoerper(plan)
    assert len(wk) >= 150, f"nur {len(wk)} Wandkörper — Fischamender-Regress"
    assert sum(1 for k in wk if k.layer == "A_Waende") >= 150
    assert any(k.quelle.startswith("block:") for k in wk)
