"""Tests stempel_anker — Raumstempel finden, gruppieren, Polygonen zuordnen.

Echte Pläne (Projekte/_eingang) per skip-Gate; die ±10 %-Flag-Logik läuft
deterministisch gegen eine synthetische In-Memory-DXF.
"""
from __future__ import annotations

from pathlib import Path

import ezdxf
import pytest

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.raumlayer import raeume_aus_layer
from notbeleuchtung.raumerkennung.stempel_anker import (
    Stempel,
    belag_hinweis,
    finde_stempel,
    flaeche_aus_text,
    ordne_zu,
    restflaechen,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
EINGANG = REPO_ROOT / "Projekte" / "_eingang"


def _plan(name: str):
    p = EINGANG / f"{name}.dxf"
    if not p.exists():
        pytest.skip(f"Eingangs-DXF fehlt: {p}")
    return lade_dxf(p)


# ---------------------------------------------------------------- Parsing-Einheiten

@pytest.mark.parametrize("text,erwartet", [
    ("38,35 m2", 38.35),
    ("25,67^  m2^ ", 25.67),          # ArchiCAD-Stacking-Reste
    ("1.84m2", 1.84),                 # Punkt-Dezimal, ohne Leerzeichen
    ("100.95 m²", 100.95),            # Unicode-Hochzahl
    ("12 qm", 12.0),
    ("KABINE 140/110", None),         # Müll-Wert
    ("Gußasphalt Bfl", None),
])
def test_flaeche_aus_text(text, erwartet):
    assert flaeche_aus_text(text) == erwartet


@pytest.mark.parametrize("belag,hinweis", [
    ("Fliesen", "NASSRAUM/VORRAUM"),
    ("Parkett", "WOHNRAUM"),
    ("Estr. vers.", "KELLER/TECHNIK"),
    ("Gußasphalt Bfl", "KELLER/TECHNIK"),
    (None, None),
    ("Marmor", None),
])
def test_belag_hinweis(belag, hinweis):
    assert belag_hinweis(belag) == hinweis


# ---------------------------------------------------------------- Rennweg (INSERT-Stempel)

def test_rennweg_zehn_stempel_mit_flaeche_und_belag():
    plan = _plan("Rennweg_OG3")
    stempel = finde_stempel(plan)
    assert len(stempel) == 10
    assert all(s.flaeche_m2 is not None for s in stempel)
    assert all(s.belag in ("Parkett", "Fliesen") for s in stempel)
    namen = " ".join(s.name for s in stempel)
    for muss in ("Bad", "WC", "Gang", "Wohnküche"):
        assert muss in namen
    # ROOM_NAME-ATTRIB ist die Quelle — sauberer Name statt Blockname-Suffix.
    assert "Hobbyraum/Fitness" in namen
    assert all(s.quelle == "Attribut" for s in stempel)


def test_rennweg_bad_601_trotz_grenz_einfuegepunkt_richtig_zugeordnet():
    plan = _plan("Rennweg_OG3")
    stempel = finde_stempel(plan)
    raeume = raeume_aus_layer(plan)
    assert len(raeume) == 10
    zu = ordne_zu(stempel, raeume)
    bad6 = next(z for z in zu if z.stempel.flaeche_m2 == pytest.approx(6.01))
    bad5 = next(z for z in zu if z.stempel.flaeche_m2 == pytest.approx(5.63))
    assert bad6.flag == "ok"
    assert bad6.raum.flaeche_m2 == pytest.approx(6.01, rel=0.02)
    assert bad5.raum.flaeche_m2 == pytest.approx(5.63, rel=0.02)
    assert bad6.polygon_index != bad5.polygon_index
    assert not restflaechen(raeume, zu)  # alle 10 Polygone gestempelt


# ---------------------------------------------------------------- Barawitzka (lose MTEXT)

def test_barawitzka_gruppierung_loser_mtexte():
    plan = _plan("Barawitzka_EG")
    stempel = finde_stempel(plan)
    # Belegt (scripts-Analyse, Layer '0._EG PP_2_810 Raum'): 41 Flächen-MTEXT,
    # davon 38 mit Raumnamen aus dem Wörterbuch. Die 5 Rest-Flächen sind keine
    # Räume bzw. nicht auflösbar: 'Rampe', 'Eigengarten' (2×), 'Kleinkinder-
    # spielplatz' (Außenflächen) und 'SR' (unbelegte Abkürzung — nicht geraten).
    # 2 der 38 tragen einen m²-Anker außerhalb dieses Layers.
    assert len(stempel) == 38
    assert {"Treppenhaus 1", "Treppenhaus 2", "Gard."} <= {s.name for s in stempel}
    assert next(s for s in stempel if s.name == "Treppenhaus 1").typ == "STIEGENHAUS"
    asr = next(s for s in stempel if s.name == "ASR")
    assert asr.flaeche_m2 == pytest.approx(25.67)
    assert asr.belag == "Gußasphalt Bfl"
    assert asr.typ == "ABSTELLRAUM"
    assert asr.quelle == "MTEXT"
    wk = next(s for s in stempel if s.name == "Waschküche")
    assert wk.flaeche_m2 == pytest.approx(4.46)
    assert wk.typ == "WASCHKÜCHE"


# ---------------------------------------------------------------- Mollgasse (ATTRIB-Stempel)

def test_mollgasse_sqm_attribs_und_vertauschte_paare(mollgasse_blank_eg):
    plan = lade_dxf(mollgasse_blank_eg)
    stempel = finde_stempel(plan)  # darf nie werfen
    sqm = [s for s in stempel if s.quelle == "Attribut"]
    assert len(sqm) >= 80  # 83 '01-SQM'-INSERTs
    wc = next(s for s in sqm if s.name == "WC" and s.flaeche_m2 == pytest.approx(1.84))
    assert wc.typ == "WC"
    assert wc.belag == "Fliesen"
    # Müll-AREA ('KABINE 140/110') → flaeche None, kein Ziffern-Belag.
    lift = next(s for s in sqm if s.name.startswith("AUFZUG"))
    assert lift.flaeche_m2 is None
    assert lift.belag is None
    # Geheilte AREA/FLOOR-Vertauschung: Fläche gefunden, obwohl sie im FLOOR steht.
    getauscht = [s for s in sqm if s.belag and "belag" in s.belag.lower()]
    assert all(s.flaeche_m2 is None or s.flaeche_m2 > 0 for s in getauscht)


def test_leerer_plan_null_stempel(tmp_path):
    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    p = tmp_path / "leer.dxf"
    doc.saveas(str(p))
    assert finde_stempel(lade_dxf(p)) == []


# ---------------------------------------------------------------- ±10 %-Flags (synthetisch)

def _quadrat(x0: float, y0: float, seite_mm: float):
    return [(x0, y0), (x0 + seite_mm, y0), (x0 + seite_mm, y0 + seite_mm), (x0, y0 + seite_mm)]


def _st(m2, pos):
    return Stempel(name="Zimmer", typ="ZIMMER", flaeche_m2=m2, belag=None,
                   position_mm=pos, quelle="MTEXT", layer="T")


@pytest.mark.parametrize("stempel_m2,flag", [
    (16.0, "ok"),          # Polygon 4×4 m = 16 m² → ±0 %
    (12.0, "zu_gross"),    # Polygon +33 % größer als Stempel
    (20.0, "zu_klein"),    # Polygon −20 % kleiner als Stempel
])
def test_flags_zehn_prozent(stempel_m2, flag):
    poly = _quadrat(0, 0, 4000)  # 16 m²
    zu = ordne_zu([_st(stempel_m2, (2000, 2000))], [poly])
    assert zu[0].flag == flag
    assert zu[0].polygon_index == 0
    assert zu[0].abweichung_prozent == pytest.approx((16 - stempel_m2) / stempel_m2 * 100)


def test_flag_kein_polygon():
    zu = ordne_zu([_st(10.0, (0, 0))], [])
    assert zu[0].flag == "kein_polygon"
    assert zu[0].polygon_index is None
    assert zu[0].abweichung_prozent is None


def test_flaechen_match_schlaegt_punkt_in_polygon():
    """Stempel-Punkt liegt IM falschen (großen) Polygon — ±10 %-Match zieht ihn ins richtige."""
    gross = _quadrat(0, 0, 10000)          # 100 m²
    klein = _quadrat(11000, 0, 3000)       # 9 m²
    st = _st(9.0, (5000, 5000))            # Punkt mitten im großen Polygon
    zu = ordne_zu([st], [gross, klein])
    assert zu[0].polygon_index == 1
    assert zu[0].flag == "ok"
    rest = restflaechen([gross, klein], zu)
    assert rest == [gross]


def test_ohne_flaeche_punkt_in_polygon():
    poly = _quadrat(0, 0, 4000)
    zu = ordne_zu([_st(None, (2000, 2000))], [poly])
    assert zu[0].polygon_index == 0
    assert zu[0].flag == "ok"
    assert zu[0].abweichung_prozent is None
