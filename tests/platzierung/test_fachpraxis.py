"""fachpraxis — Owner-Praxisregel B1: Aufheller 500 mm hinter jedem RZ.

Regel A (Tür-RZ → links) wurde nach Messung verworfen (Gate G3, Owner-Entscheid
2026-09-07) — siehe fachpraxis.py-Docstring + docs/analyse/. Der frühere
hypothesis-Property-Test ist als deterministischer Winkel-Sweep umgesetzt
(hypothesis ist keine Projekt-Dependency).
"""
import math

import pytest

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import Ausgang, BBox, Platzierung, Raum, RaumModell, Tuer
from notbeleuchtung.platzierung.fachpraxis import (
    AUFHELLER_KEY,
    QUELLE_AUFHELLER,
    QUELLE_TUERLEUCHTE,
    TUERLEUCHTE_KEY,
    FachpraxisRegeln,
    aufheller_je_rz,
    tuerleuchte_pflichtraeume,
)
from notbeleuchtung.platzierung.geometry import point_in_polygon

_GROSS = [(0.0, 0.0), (20000.0, 0.0), (20000.0, 20000.0), (0.0, 20000.0)]


def _raum(poly=None) -> RaumModell:
    poly = poly or _GROSS
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return RaumModell(
        floor="T",
        bounds_mm=BBox(min_xy=(min(xs), min(ys)), max_xy=(max(xs), max(ys))),
        raeume=[Raum(id="r1", raum_typ="GANG", polygon_mm=poly, ist_fluchtweg=True)],
        ausgaenge=[Ausgang(id="E", xy_mm=(max(xs), (min(ys) + max(ys)) / 2), typ="final_exit")],
    )


def _rz(xy=(10000.0, 10000.0), key="notlicht_ks_stiege_rechts", rot=0.0, mirror=False):
    return Platzierung(
        xy_mm=xy, catalog_key=key, rotation_deg=rot, mirror_x=mirror,
        height_mm=2400.0, kind="rz", richtung="rechts",
        circuit_hint="AGV-A-F13", covers_segment=[], norm_quelle="EN 1838",
    )


def test_aufheller_500mm_hinter_dem_rz():
    out = aufheller_je_rz([_rz()], _raum())
    assert len(out) == 1
    a = out[0]
    assert a.kind == "sicherheitsleuchte"
    assert a.catalog_key == AUFHELLER_KEY
    assert a.norm_quelle == QUELLE_AUFHELLER
    d = math.hypot(a.xy_mm[0] - 10000.0, a.xy_mm[1] - 10000.0)
    assert abs(d - 500.0) <= 1.0
    # rechts-RZ: Pfeil → +x, Rauminneres = −x.
    assert a.xy_mm[0] == pytest.approx(9500.0, abs=1.0)


def test_nicht_rz_und_richtungslose_bekommen_keinen_aufheller():
    sl = _rz()
    sl = sl.model_copy(update={"kind": "sicherheitsleuchte"})
    doppel = _rz(key="notlicht_ks_stiege_links", rot=0.0)
    doppel = doppel.model_copy(update={"richtung": "gerade", "catalog_key": "antipanik_leuchte"})
    out = aufheller_je_rz([sl, doppel], _raum())
    assert out == []


def test_position_ausserhalb_wird_nicht_gesetzt():
    # RZ am linken Rand, Pfeil rechts → Aufheller läge bei x=-500 außerhalb.
    out = aufheller_je_rz([_rz(xy=(0.0, 10000.0))], _raum())
    assert out == []


def test_ohne_raumpolygone_fail_closed():
    """Review-Befund 2026-09-07: fehlen dem RaumModell die Polygone ganz
    (fragmentierte CAD-Familien liefern real leere raeume), wird KEIN Aufheller
    gesetzt (fail-closed) — statt ihn ungeprüft ins Nichts zu platzieren."""
    leer = RaumModell(
        floor="T", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(20000.0, 20000.0)),
        raeume=[], ausgaenge=[Ausgang(id="E", xy_mm=(20000.0, 10000.0), typ="final_exit")],
    )
    assert aufheller_je_rz([_rz()], leer) == []
    # Auch ein Raum ohne verwertbares Polygon (< 3 Punkte) zählt nicht als Kontur.
    duenn = RaumModell(
        floor="T", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(20000.0, 20000.0)),
        raeume=[Raum(id="r1", raum_typ="GANG", polygon_mm=[(0.0, 0.0), (1.0, 0.0)])],
    )
    assert aufheller_je_rz([_rz()], duenn) == []


@pytest.mark.parametrize("winkel_deg", range(0, 360, 10))
def test_winkel_sweep_500mm_und_im_polygon(winkel_deg):
    """Deterministischer Sweep statt hypothesis: für jede Pfeilrichtung bleibt
    der Abstand 500 mm und die Position im Polygon (oder wird nicht gesetzt)."""
    rz = _rz(key="notlicht_ks_stiege", rot=float(winkel_deg))  # unten-Basis + Rotation
    raum = _raum()
    out = aufheller_je_rz([rz], raum, FachpraxisRegeln())
    if not out:
        return  # „nicht platzierbar" ist erlaubt, still außerhalb nicht
    a = out[0]
    assert abs(math.hypot(a.xy_mm[0] - 10000.0, a.xy_mm[1] - 10000.0) - 500.0) <= 1.0
    assert point_in_polygon(a.xy_mm, _GROSS)


def test_aufheller_liegt_gegen_pfeilrichtung_auf_der_achse():
    # unten-Block ohne Rotation: Pfeil → −y, Aufheller bei +y (gleiche x-Achse).
    rz = _rz(key="notlicht_ks_stiege_unten", rot=0.0)
    out = aufheller_je_rz([rz], _raum())
    assert len(out) == 1
    assert out[0].xy_mm[0] == pytest.approx(10000.0, abs=1.0)
    assert out[0].xy_mm[1] == pytest.approx(10500.0, abs=1.0)


# ── Lux-Gate: Aufheller nur wo unterversorgt (Owner 2026-09-08) ──────────────
def _sl(xy):
    return Platzierung(
        xy_mm=xy, catalog_key=AUFHELLER_KEY, rotation_deg=0.0, height_mm=2400.0,
        kind="sicherheitsleuchte", richtung="gerade", circuit_hint="AGV-A-F13",
        covers_segment=[], norm_quelle="EN 1838",
    )


def _strong(gamma, c=0.0):
    return 3000.0


def _weak(gamma, c=0.0):
    return 2.0


def test_aufheller_lux_gate_ueberspringt_bei_deckung():
    # Starke SL direkt am Aufheller-Kandidaten (9500,10000) + echte Photometrie →
    # Punkt weit über 1 lx → kein Aufheller (keine Überproduktion).
    out = aufheller_je_rz([_rz(), _sl((9500.0, 10000.0))], _raum(), FakeNormProvider(), i_cd_fn=_strong)
    assert out == []


def test_aufheller_lux_gate_setzt_bei_defizit_ohne_licht():
    # Keine Sicherheitsleuchte am Punkt → unterversorgt → Aufheller gesetzt.
    out = aufheller_je_rz([_rz()], _raum(), FakeNormProvider(), i_cd_fn=_strong)
    assert len(out) == 1
    assert out[0].catalog_key == AUFHELLER_KEY


def test_aufheller_lux_gate_setzt_bei_schwachem_licht():
    # SL vorhanden, aber schwache Photometrie → Punkt < 1 lx → Aufheller nötig.
    out = aufheller_je_rz([_rz(), _sl((9500.0, 10000.0))], _raum(), FakeNormProvider(), i_cd_fn=_weak)
    assert len(out) == 1


def test_aufheller_ohne_photometrie_bleibt_bedingungslos():
    # Ohne i_cd_fn (keine LDT) kein Gate — auch mit SL am Punkt wird gesetzt.
    out = aufheller_je_rz([_rz(), _sl((9500.0, 10000.0))], _raum(), FakeNormProvider())
    assert len(out) == 1


# ── Tür-Leuchte TECHNIK/MUELLRAUM (Owner-Regel 2026-09-07) ───────────────────
_RAUM_POLY = [(0.0, 0.0), (10000.0, 0.0), (10000.0, 8000.0), (0.0, 8000.0)]


def _raum_mit_tuer(raum_typ: str, tuer_xy=(5000.0, 0.0), nach="gang") -> RaumModell:
    return RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(10000.0, 8000.0)),
        raeume=[
            Raum(id="t1", raum_typ=raum_typ, polygon_mm=_RAUM_POLY),
            Raum(id="gang", raum_typ="GANG",
                 polygon_mm=[(0.0, 8000.0), (10000.0, 8000.0), (10000.0, 9000.0), (0.0, 9000.0)]),
        ],
        tueren=[Tuer(id="d1", xy_mm=tuer_xy, von_raum="t1", nach_raum=nach)],
    )


@pytest.mark.parametrize("typ", ["TECHNIK", "MUELLRAUM", "KINDERWAGENRAUM"])
def test_tuerleuchte_ist_rz_an_der_tuer(typ):
    # Owner-Korrektur 2026-09-08: an der Tür ein RETTUNGSZEICHEN (Pfeil-unten, zur Tür
    # rotiert) — NICHT mehr eine Antipanik-SL. Kleiner konvexer Raum → nur das RZ.
    out = tuerleuchte_pflichtraeume(_raum_mit_tuer(typ), FakeNormProvider())
    assert len(out) == 1
    p = out[0]
    assert p.kind == "rz"                    # Rettungszeichen, nicht Sicherheitsleuchte
    assert p.richtung == "unten"
    assert p.xy_mm == (5000.0, 0.0)          # exakt an der Tür
    # Tür (5000,0) liegt unter dem Raum-Zentrum (5000,4000) → Pfeil zeigt nach unten (rot 0°).
    assert p.rotation_deg == 0.0
    assert p.norm_quelle == QUELLE_TUERLEUCHTE
    assert "F13" in p.circuit_hint           # getrennter Sicherheitskreis
    assert p.height_mm >= 2000.0             # EN-1838-Mindesthöhe


def test_andere_raumtypen_bekommen_keine_tuerleuchte():
    fake = FakeNormProvider()
    assert tuerleuchte_pflichtraeume(_raum_mit_tuer("BUERO"), fake) == []
    # ABSTELLRAUM bewusst NICHT: die Regel gilt für den GEMEINSAMEN Kinderwagen-
    # raum, nicht den privaten Wohnungs-Abstellraum (Owner-Entscheid 2026-09-07).
    assert tuerleuchte_pflichtraeume(_raum_mit_tuer("ABSTELLRAUM"), fake) == []
    assert tuerleuchte_pflichtraeume(_raum_mit_tuer("LAGER"), fake) == []


def test_tuerleuchte_fail_closed_ohne_tuer():
    """Kein Tür-Bezug und keine Tür im Polygon → keine Leuchte an geratener Stelle."""
    ohne = RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(10000.0, 8000.0)),
        raeume=[Raum(id="t1", raum_typ="TECHNIK", polygon_mm=_RAUM_POLY)],
    )
    assert tuerleuchte_pflichtraeume(ohne, FakeNormProvider()) == []


def test_tuerleuchte_bevorzugt_erschliessungs_tuer():
    """Bei mehreren Türen gewinnt die zum GANG/Stiegenhaus (die Ausgangstür)."""
    rm = RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(10000.0, 8000.0)),
        raeume=[
            Raum(id="t1", raum_typ="TECHNIK", polygon_mm=_RAUM_POLY),
            Raum(id="gang", raum_typ="GANG", polygon_mm=_RAUM_POLY),
            Raum(id="lager", raum_typ="LAGER", polygon_mm=_RAUM_POLY),
        ],
        tueren=[
            Tuer(id="d_lager", xy_mm=(1000.0, 0.0), von_raum="t1", nach_raum="lager"),
            Tuer(id="d_gang", xy_mm=(9000.0, 0.0), von_raum="t1", nach_raum="gang"),
        ],
    )
    out = tuerleuchte_pflichtraeume(rm, FakeNormProvider())
    assert out[0].xy_mm == (9000.0, 0.0)     # RZ an der Tür zum GANG


def test_grosser_tiefer_raum_bekommt_mittige_antipanik():
    # Tiefer Raum (weitester Punkt > RZ-Erkennungsweite 30 m) + ≥ 60 m² → Tür-RZ PLUS
    # mittige Antipanikleuchte gegen Panik im hinteren Bereich.
    tief = [(0.0, 0.0), (40000.0, 0.0), (40000.0, 40000.0), (0.0, 40000.0)]  # 1600 m²
    rm = RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(40000.0, 41000.0)),
        raeume=[
            Raum(id="t1", raum_typ="TECHNIK", polygon_mm=tief, flaeche_m2=1600.0),
            Raum(id="gang", raum_typ="GANG",
                 polygon_mm=[(0.0, 40000.0), (40000.0, 40000.0), (40000.0, 41000.0), (0.0, 41000.0)]),
        ],
        tueren=[Tuer(id="d1", xy_mm=(0.0, 0.0), von_raum="t1", nach_raum="gang")],
    )
    out = tuerleuchte_pflichtraeume(rm, FakeNormProvider())
    assert len(out) == 2
    assert out[0].kind == "rz"
    zusatz = out[1]
    assert zusatz.kind == "antipanik"
    assert zusatz.catalog_key == TUERLEUCHTE_KEY   # antipanik_leuchte
    assert point_in_polygon(zusatz.xy_mm, tief)     # mittig im Raum


def test_verwinkelter_kleiner_raum_bekommt_mittigen_aufheller():
    # L-Form (verdeckte Ecke) + < 60 m² → Tür-RZ PLUS mittiger Aufheller.
    L = [(0.0, 0.0), (8000.0, 0.0), (8000.0, 8000.0), (4000.0, 8000.0),
         (4000.0, 4000.0), (0.0, 4000.0)]  # 48 m², Fläche/Bbox = 0.75 < 0.85
    rm = RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(8000.0, 9000.0)),
        raeume=[
            Raum(id="t1", raum_typ="MUELLRAUM", polygon_mm=L, flaeche_m2=48.0),
            Raum(id="gang", raum_typ="GANG",
                 polygon_mm=[(0.0, 8000.0), (4000.0, 8000.0), (4000.0, 9000.0), (0.0, 9000.0)]),
        ],
        tueren=[Tuer(id="d1", xy_mm=(2000.0, 8000.0), von_raum="t1", nach_raum="gang")],
    )
    out = tuerleuchte_pflichtraeume(rm, FakeNormProvider())
    assert len(out) == 2
    assert out[0].kind == "rz"
    assert out[1].kind == "sicherheitsleuchte"
    assert out[1].catalog_key == AUFHELLER_KEY
