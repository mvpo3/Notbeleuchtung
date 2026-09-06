"""raumlayer.raeume_aus_hatch — HATCH-Raumpolygone + Varianten-Versatz.

Barawitzka: 41 Raum-HATCHes liegen in den Icon-Varianten, die Stempel in der
PP_2-Variante — der Versatz wird über die '170 Schachtwände'-Layer-Familie
bestimmt und die Polygone auf die Stempel-Variante geschoben.
"""
from __future__ import annotations

from pathlib import Path

import ezdxf
import pytest

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.raumlayer import (
    raeume_aus_hatch,
    raeume_aus_layer,
    varianten_versatz,
)
from notbeleuchtung.raumerkennung.stempel_anker import Stempel, finde_stempel, ordne_zu

REPO_ROOT = Path(__file__).resolve().parents[2]
BARAWITZKA = REPO_ROOT / "Projekte" / "_eingang" / "Barawitzka_EG.dxf"
RENNWEG = REPO_ROOT / "Projekte" / "_eingang" / "Rennweg_OG3.dxf"

_SUFFIX = "810 Raum"


@pytest.fixture(scope="module")
def barawitzka():
    if not BARAWITZKA.exists():
        pytest.skip(f"Barawitzka-DXF fehlt: {BARAWITZKA}")
    plan = lade_dxf(BARAWITZKA)
    return plan, finde_stempel(plan)


def test_barawitzka_41_raumpolygone(barawitzka):
    plan, stempel = barawitzka
    raeume = raeume_aus_hatch(plan, stempel)
    assert len(raeume) == 41
    assert all(1.0 <= r.flaeche_m2 <= 200.0 for r in raeume)


def test_barawitzka_varianten_versatz(barawitzka):
    plan, stempel = barawitzka
    # Prefixe aus den echten Layern ableiten (Umlaute können cp-dekodiert sein).
    hatch_layer = next(e.dxf.layer for e in plan.space
                       if e.dxftype() == "HATCH" and _SUFFIX in e.dxf.layer)
    quell = hatch_layer[: hatch_layer.index(_SUFFIX) - 1]
    ziel = stempel[0].layer[: stempel[0].layer.index(_SUFFIX) - 1]
    versatz = varianten_versatz(plan, quell, ziel)
    assert versatz is not None
    # Verifizierter Versatz Icon_1→PP_2 (Quell-Einheit m, hier mm/1000).
    assert round(versatz[0] / 1000, 6) == pytest.approx(-31.818365, abs=1e-6)
    assert round(versatz[1] / 1000, 6) == pytest.approx(2.550370, abs=1e-6)


def test_barawitzka_stempel_zuordnung(barawitzka):
    plan, stempel = barawitzka
    raeume = raeume_aus_hatch(plan, stempel)
    zu = ordne_zu(stempel, raeume)
    ok = [z for z in zu
          if z.abweichung_prozent is not None and abs(z.abweichung_prozent) <= 10.0]
    assert len(ok) >= 38


def _synth_hatch_dxf(path: Path) -> Path:
    """Mini-DXF (mm): 2 HATCHes ohne Raum-Layer — 20 m² mit Stempel, 250 m² ohne."""
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    W = "02-TWA-G00-LEG-M0"
    for lyr in (W, "Fuellung"):
        if lyr not in doc.layers:
            doc.layers.add(lyr)
    corners = [(0, 0), (30000, 0), (30000, 16000), (0, 16000)]
    for i in range(4):
        msp.add_line(corners[i], corners[(i + 1) % 4], dxfattribs={"layer": W})
    h1 = msp.add_hatch(dxfattribs={"layer": "Fuellung"})       # 5×4 m = 20 m²
    h1.paths.add_polyline_path(
        [(1000, 1000), (6000, 1000), (6000, 5000), (1000, 5000)], is_closed=True)
    h2 = msp.add_hatch(dxfattribs={"layer": "Fuellung"})       # 25×10 m = 250 m²
    h2.paths.add_polyline_path(
        [(7000, 1000), (32000, 1000), (32000, 11000), (7000, 11000)], is_closed=True)
    doc.saveas(str(path))
    return path


def test_hatch_ohne_raumlayer_mit_stempel(tmp_path):
    plan = lade_dxf(_synth_hatch_dxf(tmp_path / "hatch.dxf"))
    st = [Stempel(name="Büro", typ="BUERO", flaeche_m2=20.0, belag=None,
                  position_mm=(3000.0, 3000.0), quelle="MTEXT", layer="Fuellung")]
    raeume = raeume_aus_hatch(plan, st)
    # 20-m²-HATCH mit Stempel drin → Raum; 250 m² ohne Stempel → kein Raum.
    assert len(raeume) == 1
    assert raeume[0].flaeche_m2 == pytest.approx(20.0, abs=0.1)


def test_hatch_ohne_stempel_kein_raum(tmp_path):
    plan = lade_dxf(_synth_hatch_dxf(tmp_path / "hatch2.dxf"))
    assert raeume_aus_hatch(plan, stempel=None) == []


def test_rennweg_raeume_aus_layer_regression():
    if not RENNWEG.exists():
        pytest.skip(f"Rennweg-DXF fehlt: {RENNWEG}")
    assert len(raeume_aus_layer(lade_dxf(RENNWEG))) == 10
