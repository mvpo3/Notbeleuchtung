"""Tests für stempel_flutung (Raster-Flutung vom Stempelpunkt).

Synthetische Mini-Pläne direkt aus Wandkoerper-Objekten (kein DXF nötig);
die echte Rennweg-Probe skippt, wenn der Plan fehlt (Gate-Muster wie conftest).
"""
from __future__ import annotations

from pathlib import Path

import pytest
from shapely.geometry import Polygon

from notbeleuchtung.raumerkennung.stempel_anker import Stempel
from notbeleuchtung.raumerkennung.stempel_flutung import FlutRaum, flute_stempel
from notbeleuchtung.raumerkennung.tueren import TuerOeffnung
from notbeleuchtung.raumerkennung.wandkoerper import Wandkoerper

REPO_ROOT = Path(__file__).resolve().parents[2]
EINGANG = REPO_ROOT / "Projekte" / "_eingang"


def _wand(x0: float, y0: float, x1: float, y1: float) -> Wandkoerper:
    return Wandkoerper(
        polygon_mm=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
        material="STAHLBETON", layer="Test", quelle="msp",
        breite_mm=min(x1 - x0, y1 - y0),
    )


def _stempel(x: float, y: float, m2: float | None, name: str = "Zimmer") -> Stempel:
    return Stempel(name=name, typ=None, flaeche_m2=m2, belag=None,
                   position_mm=(x, y), quelle="MTEXT", layer="Test")


def _raum_mit_tuer(gap_von: float, gap_bis: float) -> list[Wandkoerper]:
    """Rechteckraum innen (0,0)–(5000,4000), Wand 200 mm, Türlücke rechts."""
    return [
        _wand(-200, -200, 5200, 0),
        _wand(-200, 4000, 5200, 4200),
        _wand(-200, 0, 0, 4000),
        _wand(5000, 0, 5200, gap_von),
        _wand(5000, gap_bis, 5200, 4000),
    ]


# ── (a) Rechteckraum mit Tür-Lücke → Flutung ±10 % ok ───────────────────────
def test_rechteckraum_mit_tuer_ok():
    wk = _raum_mit_tuer(1500, 2500)  # Lücke 1000 mm
    tuer = TuerOeffnung(xy_mm=(5100, 2000), breite_mm=1000, winkel_grad=None,
                        quelle="arc")
    (fr,) = flute_stempel(None, [_stempel(2500, 2000, 20.0)], wk, [tuer])
    assert isinstance(fr, FlutRaum)
    assert fr.quelle == "FLUTUNG"
    assert fr.flag == "ok"
    assert abs(fr.abweichung_prozent) <= 10.0
    assert Polygon(fr.polygon_mm).area / 1e6 == pytest.approx(20.0, rel=0.1)


# ── (b) Öffnung 1.4 m zum Nachbarraum → erst Stufe 1.5 versiegelt, ok ───────
def test_grosse_oeffnung_hoechste_stufe():
    wk = [
        _wand(-200, -200, 9400, 0),        # unten (beide Räume)
        _wand(-200, 4000, 9400, 4200),     # oben
        _wand(-200, 0, 0, 4000),           # links
        _wand(9200, 0, 9400, 4000),        # rechts
        _wand(5000, 0, 5200, 1300),        # Mittelwand unter der Öffnung
        _wand(5000, 2700, 5200, 4000),     # Mittelwand über der Öffnung (Lücke 1400)
    ]
    # Tür sitzt am Anschlag (Drehpunkt) — Radius 1.2 m reicht nicht, 1.5 m schon.
    tuer = TuerOeffnung(xy_mm=(5100, 1300), breite_mm=1400, winkel_grad=None,
                        quelle="arc")
    (fr,) = flute_stempel(None, [_stempel(2500, 2000, 20.0)], wk, [tuer])
    assert fr.flag == "ok"
    assert abs(fr.abweichung_prozent) <= 10.0
    # Nicht in den Nachbarraum geleakt:
    assert max(x for x, _ in fr.polygon_mm) <= 5200 + 100


# ── (c) offener Riesenbereich → flutung_unsicher, NICHT verworfen ───────────
def test_riesenbereich_unsicher():
    wk = [  # Halle innen 30 m × 30 m = 900 m², Stempel behauptet 10 m²
        _wand(-200, -200, 30200, 0),
        _wand(-200, 30000, 30200, 30200),
        _wand(-200, 0, 0, 30000),
        _wand(30000, 0, 30200, 30000),
    ]
    ergebnisse = flute_stempel(None, [_stempel(15000, 15000, 10.0)], wk, [])
    assert len(ergebnisse) == 1
    (fr,) = ergebnisse
    assert fr.flag == "flutung_unsicher"
    assert fr.abweichung_prozent > 10.0
    assert Polygon(fr.polygon_mm).area / 1e6 == pytest.approx(900.0, rel=0.1)


# ── (d) zwei Stempel in einem Flutgebiet → Watershed trennt ─────────────────
def test_watershed_trennt_zwei_stempel():
    wk = [  # 10 m × 4 m, Engstelle bei x=5000 (Öffnung 1500, KEINE Tür)
        _wand(-200, -200, 10200, 0),
        _wand(-200, 4000, 10200, 4200),
        _wand(-200, 0, 0, 4000),
        _wand(10000, 0, 10200, 4000),
        _wand(4900, 0, 5100, 1250),
        _wand(4900, 2750, 5100, 4000),
    ]
    stempel = [_stempel(2500, 2000, 19.5, "Links"), _stempel(7500, 2000, 19.5, "Rechts")]
    ergebnisse = flute_stempel(None, stempel, wk, [])
    assert len(ergebnisse) == 2
    for fr in ergebnisse:
        assert fr.polygon_mm, f"{fr.stempel.name} ohne Polygon"
        a = Polygon(fr.polygon_mm).area / 1e6
        assert 14.0 <= a <= 25.0, f"{fr.stempel.name}: {a:.1f} m² unplausibel"


# ── (e) Stempelpunkt AUF der Wand → nächster freier Punkt ───────────────────
def test_stempel_auf_wand():
    wk = _raum_mit_tuer(1500, 2500)
    tuer = TuerOeffnung(xy_mm=(5100, 2000), breite_mm=1000, winkel_grad=None,
                        quelle="arc")
    # Punkt mitten IN der linken Wand (ArchiCAD-Zonen-Referenz auf der Grenze).
    (fr,) = flute_stempel(None, [_stempel(-100, 2000, 20.0)], wk, [tuer])
    assert fr.flag == "ok"
    assert Polygon(fr.polygon_mm).area / 1e6 == pytest.approx(20.0, rel=0.1)


# ── Leere Inputs ────────────────────────────────────────────────────────────
def test_leere_inputs():
    assert flute_stempel(None, [], [], []) == []
    assert flute_stempel(None, [_stempel(0, 0, 10.0)], [], []) == []


# ── echte Rennweg-Probe (skip-Gate) ─────────────────────────────────────────
def test_rennweg_mindestens_ein_raum_flutbar():
    pfad = EINGANG / "Rennweg_OG3.dxf"
    if not pfad.exists():
        pytest.skip(f"Plan fehlt: {pfad}")
    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
    from notbeleuchtung.raumerkennung.stempel_anker import finde_stempel
    from notbeleuchtung.raumerkennung.tueren import tuer_oeffnungen
    from notbeleuchtung.raumerkennung.wandkoerper import finde_wandkoerper

    plan = lade_dxf(pfad)
    wk = finde_wandkoerper(plan)
    stempel = [s for s in finde_stempel(plan) if s.flaeche_m2]
    assert stempel, "Rennweg ohne m²-Stempel"
    ergebnisse = flute_stempel(plan, stempel, wk, tuer_oeffnungen(plan))
    assert len(ergebnisse) == len(stempel)  # NIE verwerfen
    assert any(fr.flag == "ok" for fr in ergebnisse), \
        [f"{fr.stempel.name}: {fr.abweichung_prozent}%" for fr in ergebnisse]
