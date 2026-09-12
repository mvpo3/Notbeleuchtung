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
    aussen_tuer_rz,
    pfeil_durch_hauseingang,
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


def test_tuer_rz_ist_vom_aufheller_ausgenommen():
    """Owner-Entscheid 2026-09-09: das Tür-RZ der Pflichträume (norm_quelle =
    QUELLE_TUERLEUCHTE) bekommt KEINEN Aufheller — es sitzt an der Tür, das
    Rauminnere trägt die mittige Zusatzleuchte. Ein gewöhnliches Fluchtweg-RZ
    (andere Quelle) bekommt ihn weiterhin."""
    tuer_rz = _rz().model_copy(update={"norm_quelle": QUELLE_TUERLEUCHTE})
    assert aufheller_je_rz([tuer_rz], _raum()) == []
    assert len(aufheller_je_rz([_rz()], _raum())) == 1


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
    # Owner-Korrektur 2026-09-08 + R-B (Fachdoku v2): an der Tür ein RETTUNGSZEICHEN
    # (Pfeil-unten, Piktogramm blickt INS Rauminnere) — NICHT mehr eine Antipanik-SL.
    out = tuerleuchte_pflichtraeume(_raum_mit_tuer(typ), FakeNormProvider())
    assert len(out) == 1
    p = out[0]
    assert p.kind == "rz"                    # Rettungszeichen, nicht Sicherheitsleuchte
    assert p.richtung == "unten"
    # Owner-Korrektur 2026-09-10 (AutoCAD-Diff L-Demo): das Tür-RZ sitzt nicht mehr exakt
    # auf der Schwelle, sondern ~150 mm IM bedienten Raum (Richtung Raum-Inneres).
    assert math.hypot(p.xy_mm[0] - 5000.0, p.xy_mm[1] - 0.0) <= 160.0   # nahe der Tür
    assert point_in_polygon(p.xy_mm, _RAUM_POLY)                        # leicht im Raum
    # Tür (5000,0) liegt unter dem Raum-Zentrum (5000,4000) → Piktogramm blickt ins
    # Rauminnere (nach oben) = unten-Block rot 180 (R-B, kalibriert am Elektroplan-DE-EG).
    assert p.rotation_deg == 180.0
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
    # RZ an der Tür zum GANG (nach Owner-Korrektur ~150 mm ins Raum-Innere versetzt).
    assert math.hypot(out[0].xy_mm[0] - 9000.0, out[0].xy_mm[1] - 0.0) <= 160.0
    assert point_in_polygon(out[0].xy_mm, _RAUM_POLY)


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


# ── R3: communal ABSTELLRAUM (Fahrradraum) — Owner-Korrektur 2026-09-11 ─────────
def test_tuerleuchte_communal_abstellraum():
    """AutoCAD-Diff Elektroplan DE („Hier hast du es Vergessen" am Fahrradraum):
    der GEMEINSAME Abstellraum (ist_communal=True) bekommt das Tür-RZ wie
    TECHNIK/MUELLRAUM; der private Wohnungs-Abstellraum bleibt draußen."""
    m = _raum_mit_tuer("ABSTELLRAUM")
    communal = m.model_copy(update={"raeume": [
        m.raeume[0].model_copy(update={"ist_communal": True}), m.raeume[1]]})
    out = tuerleuchte_pflichtraeume(communal, FakeNormProvider())
    assert len(out) == 1
    assert out[0].kind == "rz"
    assert out[0].norm_quelle == QUELLE_TUERLEUCHTE
    # privater Abstellraum unveraendert ohne Tuer-RZ (Owner-Entscheid 2026-09-07):
    assert tuerleuchte_pflichtraeume(m, FakeNormProvider()) == []


# ── R2: communal Raum + AUSSEN-Tür = Notausgang-RZ — Owner-Korrektur 2026-09-11 ─
def _raum_mit_aussentuer(communal=True, ausgaenge=(), detail=None):
    tuer = Tuer(id="d1", xy_mm=(5000.0, 0.0), von_raum="m1", nach_raum="AUSSEN",
                tuer_detail=detail)
    return RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(10000.0, 8000.0)),
        raeume=[Raum(id="m1", raum_typ="MUELLRAUM", polygon_mm=_RAUM_POLY,
                     ist_communal=communal)],
        tueren=[tuer], ausgaenge=list(ausgaenge),
    )


def test_exit_jenseits_der_tuer_fluchtachse_zeigt_raus():
    """v8-Befund Hauseingang (Elektroplan DE): der Tür-Block-Insert (WET) liegt
    ~250 mm INNEN, der Exit-Punkt auf der Schwelle — „tuer − exit" zeigte damit
    ZURÜCK in den Gang, das Exit-RZ rutschte nach draußen und blickte nach außen
    (rot 180 statt 0). Die Vorzeichen-Härtung spiegelt die Fluchtachse am Anlauf:
    RZ sitzt raumseitig (südlich), Piktogramm blickt ins Rauminnere (rot 0)."""
    from notbeleuchtung.hauptengine.contracts import (
        Ausgang,
        BBox,
        FluchtwegSegment,
        RaumModell,
        Tuer,
    )
    from notbeleuchtung.hauptengine.contracts import Raum as _Raum
    from notbeleuchtung.platzierung.communal_stgh_strategy import plan_rettungszeichen

    rm = RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(10000.0, 8000.0)),
        raeume=[_Raum(id="gang", raum_typ="GANG", ist_fluchtweg=True, ist_communal=True,
                      polygon_mm=[(0.0, 0.0), (10000.0, 0.0), (10000.0, 5000.0), (0.0, 5000.0)])],
        # Tür-Insert 250 mm INNEN (südlich) des Exits auf der Nordwand:
        tueren=[Tuer(id="he", xy_mm=(5000.0, 4750.0), von_raum="gang", nach_raum="AUSSEN",
                     ist_notausgang=True, tuer_detail="hauseingang")],
        ausgaenge=[Ausgang(id="E", xy_mm=(5000.0, 5000.0), typ="final_exit")],
        zirkulation={"nodes": [], "edges": [], "segmente": [
            FluchtwegSegment(segment_id="s1", reason="exit", ziel_ausgang="E",
                             polyline_mm=[(5000.0, 1000.0), (5000.0, 5000.0)])]},
    )
    rz = [p for p in plan_rettungszeichen(rm, FakeNormProvider())
          if math.hypot(p.xy_mm[0] - 5000.0, p.xy_mm[1] - 5000.0) < 1000.0]
    assert len(rz) == 1
    assert rz[0].xy_mm[1] < 5000.0          # raumseitig (südlich), NICHT draußen
    assert rz[0].rotation_deg == 0.0        # Blick ins Rauminnere (−y)


def test_phantom_durchgang_ist_keine_tuer():
    """Owner-Befund 2026-09-12 („dort gibt es aber keine Tür, dort ist eine Wand"):
    die Erkennung lieferte die Wand Müllraum↔Gang als 6064-mm-GEOMETRIE_OEFFNUNG-
    „Durchgang" — das Tür-RZ hing an der Wand. Öffnungen jenseits jedes Türmaßes
    (> 1300 mm, Selmans Nennmaßbereich 60–130 cm) sind keine Türen: das RZ gehört
    an die echte 900er-Tür."""
    from notbeleuchtung.hauptengine.contracts import Tuer

    raum = _raum_mit_tuer("MUELLRAUM")
    echte = raum.tueren[0]                               # 900er an (5000, 0)
    raum.tueren.insert(0, Tuer(id="phantom", xy_mm=(9900.0, 4000.0),
                               von_raum="r1", nach_raum="gang",
                               breite_mm=6064.0, ohne_tuerblatt=True))
    raum.raeume.append(Raum(id="gang", raum_typ="GANG",
                            polygon_mm=[(10000.0, 0.0), (12000.0, 0.0),
                                        (12000.0, 8000.0), (10000.0, 8000.0)],
                            ist_fluchtweg=True, ist_communal=True))
    out = tuerleuchte_pflichtraeume(raum, FakeNormProvider())
    rz = [p for p in out if p.kind == "rz"]
    assert len(rz) == 1
    d = math.hypot(rz[0].xy_mm[0] - echte.xy_mm[0], rz[0].xy_mm[1] - echte.xy_mm[1])
    assert d <= 200.0, f"RZ hängt {d:.0f} mm von der echten Tür (an der Phantom-Wand?)"


def test_aussen_tuer_rz_am_muellraum_ausgang():
    """„Hier ist der Ausgang vom Müllraum": AUSSEN-Tür eines communal Raums traegt
    ein RZ (EN 1838 §4.1.2 g) — Piktogramm blickt ins Rauminnere (R-B), ~150 mm im Raum."""
    out = aussen_tuer_rz(_raum_mit_aussentuer(), FakeNormProvider())
    assert len(out) == 1
    p = out[0]
    assert p.kind == "rz"
    assert p.richtung == "unten"
    # Zentrum (5000,4000) → Tür (5000,0): Piktogramm blickt zurück ins Rauminnere
    # (nach oben) = rot 180 (R-B; Ground truth Müllraum-Südtür ~180°).
    assert p.rotation_deg == 180.0
    assert p.xy_mm[0] == pytest.approx(5000.0, abs=1.0)
    assert p.xy_mm[1] == pytest.approx(150.0, abs=1.0)   # 150 mm im Raum-Inneren
    assert p.norm_quelle != QUELLE_TUERLEUCHTE           # echte Norm-Quelle (§4.1.2 g)


def test_aussen_tuer_rz_nicht_fuer_private_balkontuer():
    assert aussen_tuer_rz(_raum_mit_aussentuer(communal=False), FakeNormProvider()) == []


def test_aussen_tuer_rz_skip_bei_nahem_ausgang_und_hauseingang():
    # Modellierter Ausgang ≤2 m an der Tür → Anker-Pfad zeichnet, keine Dublette.
    nah = _raum_mit_aussentuer(ausgaenge=[Ausgang(id="E", xy_mm=(5000.0, 0.0), typ="final_exit")])
    assert aussen_tuer_rz(nah, FakeNormProvider()) == []
    # Hauseingang ist R4-Domäne (Anker-Exit-RZ), nicht R2.
    assert aussen_tuer_rz(_raum_mit_aussentuer(detail="hauseingang"), FakeNormProvider()) == []


# ── R4: Hauseingang-Pfeil = Fluchtrichtung — Owner-Korrektur 2026-09-11 ─────────
def test_pfeil_durch_hauseingang_zeigt_zum_ausgang():
    """R4 + R-B (Fachdoku v2): RZ nahe der hauseingang-Tür wird auf die allgemeine
    Türregel rotiert — Piktogramm blickt ins Rauminnere (Gegenrichtung der
    Fluchtachse zum modellierten Ausgang), nie in die Aufschlagrichtung."""
    rm = RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(10000.0, 8000.0)),
        raeume=[Raum(id="g", raum_typ="GANG", polygon_mm=_RAUM_POLY, ist_fluchtweg=True)],
        tueren=[Tuer(id="he", xy_mm=(5000.0, 5000.0), von_raum="g", nach_raum="AUSSEN",
                     tuer_detail="hauseingang", ist_notausgang=True)],
        ausgaenge=[Ausgang(id="E", xy_mm=(5000.0, 6000.0), typ="final_exit")],
    )
    falsch = _rz(xy=(5000.0, 4600.0), key="notlicht_ks_stiege", rot=90.0)
    falsch = falsch.model_copy(update={"richtung": "unten"})
    out = pfeil_durch_hauseingang([falsch], rm)
    # Ausgang liegt noerdlich (Fluchtachse +y) → Piktogramm blickt ins Rauminnere
    # (nach unten) = rot 0 (R-B, allgemeine Türregel gilt auch am Hauseingang).
    assert out[0].rotation_deg == 0.0
    # RZ weit weg von der Tür bleibt unveraendert:
    fern = falsch.model_copy(update={"xy_mm": (500.0, 500.0), "rotation_deg": 90.0})
    assert pfeil_durch_hauseingang([fern], rm)[0].rotation_deg == 90.0


# ── R5: communal Nebenraum generalisiert (Spielraum) — Owner 2026-09-11 Runde 2 ─
def test_tuerleuchte_communal_zimmer_spielraum():
    """„Im Spielraum gehört auch eine Notleuchte": JEDER communal Nebenraum
    (hier ZIMMER/Spielraum) bekommt das Tür-RZ; privates ZIMMER nicht."""
    m = _raum_mit_tuer("ZIMMER")
    communal = m.model_copy(update={"raeume": [
        m.raeume[0].model_copy(update={"ist_communal": True}), m.raeume[1]]})
    out = tuerleuchte_pflichtraeume(communal, FakeNormProvider())
    assert len(out) == 1
    assert out[0].kind == "rz"
    assert tuerleuchte_pflichtraeume(m, FakeNormProvider()) == []


def test_tuerleuchte_nicht_fuer_communal_erschliessung():
    """Erschließungs-/Vorraum-Flächen sind ausgenommen — die Erkennung flaggt
    private Wohnungs-Vorräume real mit communal=True (Elektroplan DE)."""
    for typ in ("VORRAUM", "GANG", "STIEGENHAUS", "BALKON"):
        m = _raum_mit_tuer(typ)
        communal = m.model_copy(update={"raeume": [
            m.raeume[0].model_copy(update={"ist_communal": True}), m.raeume[1]]})
        assert tuerleuchte_pflichtraeume(communal, FakeNormProvider()) == [], typ


# ── R7: kein RZ im Wohnungs-Vorraum an der Stiege — Owner 2026-09-11 Runde 2 ────
from notbeleuchtung.platzierung.fachpraxis import (
    entferne_wohnungs_vorraum_rz,
    stiegenhaus_rz_nachpass,
)


def _raum_wohnungs_vorraum():
    vr_poly = [(0.0, 0.0), (2000.0, 0.0), (2000.0, 1400.0), (0.0, 1400.0)]  # 2,8 m²
    return RaumModell(
        floor="1OG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(10000.0, 8000.0)),
        raeume=[
            Raum(id="vr", raum_typ="GANG", polygon_mm=vr_poly, flaeche_m2=2.8,
                 ist_fluchtweg=True, ist_communal=True),
            Raum(id="wz", raum_typ="WOHNZIMMER",
                 polygon_mm=[(0.0, 1400.0), (2000.0, 1400.0), (2000.0, 5000.0), (0.0, 5000.0)]),
            Raum(id="stgh", raum_typ="STIEGENHAUS", ist_communal=True,
                 polygon_mm=[(2000.0, 0.0), (5000.0, 0.0), (5000.0, 3000.0), (2000.0, 3000.0)]),
        ],
        tueren=[
            Tuer(id="t-wz", xy_mm=(1000.0, 1400.0), von_raum="vr", nach_raum="wz"),
            Tuer(id="t-stgh", xy_mm=(2000.0, 700.0), von_raum="vr", nach_raum="stgh"),
        ],
    )


def test_wohnungs_vorraum_rz_wird_entfernt():
    """„RZ NICHT in der Wohnung": kleiner Stiegen-Vorraum, übrige Türen privat →
    Segment-RZ darin fliegt; Tür-RZ der Pflichträume bliebe."""
    rm = _raum_wohnungs_vorraum()
    drin = _rz(xy=(1000.0, 700.0)).model_copy(update={"richtung": "unten"})
    assert entferne_wohnungs_vorraum_rz([drin], rm) == []
    tuer_rz = drin.model_copy(update={"norm_quelle": QUELLE_TUERLEUCHTE})
    assert entferne_wohnungs_vorraum_rz([tuer_rz], rm) == [tuer_rz]


def test_wohnungs_vorraum_mit_communal_anbindung_bleibt():
    """Grenzt der kleine GANG zusätzlich an eine COMMUNAL Fläche (echter
    Erschließungs-Knoten), bleibt sein RZ."""
    rm = _raum_wohnungs_vorraum()
    raeume = [r.model_copy(update={"ist_communal": True}) if r.id == "wz" else r
              for r in rm.raeume]
    rm2 = rm.model_copy(update={"raeume": raeume})
    drin = _rz(xy=(1000.0, 700.0))
    assert entferne_wohnungs_vorraum_rz([drin], rm2) == [drin]


# ── R8: Stiegenhaus-RZ an die Wand, Richtung Abstieg — Owner 2026-09-11 Runde 2 ─
def test_stiegenhaus_rz_wandert_ins_stiegenhaus():
    """„RZ im Stiegenhaus … zeigt in die Richtung wie man in den Erdgeschoß kommt":
    das unten-RZ am stair_exit wird INS Stiegenhaus versetzt, Pfeil Richtung
    Stiegen-Zentrum (Abstieg)."""
    stgh_poly = [(2000.0, 0.0), (5000.0, 0.0), (5000.0, 3000.0), (2000.0, 3000.0)]
    rm = RaumModell(
        floor="1OG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(10000.0, 8000.0)),
        raeume=[Raum(id="stgh", raum_typ="STIEGENHAUS", polygon_mm=stgh_poly,
                     ist_communal=True)],
        ausgaenge=[Ausgang(id="X", xy_mm=(2000.0, 1500.0), typ="stair_exit")],
    )
    rz = _rz(xy=(1900.0, 1500.0), key="notlicht_ks_stiege", rot=270.0)
    rz = rz.model_copy(update={"richtung": "unten"})
    out = stiegenhaus_rz_nachpass([rz], rm)
    assert point_in_polygon(out[0].xy_mm, stgh_poly)      # IM Stiegenhaus
    # Exit (2000,1500) → Zentrum (3500,1500): Richtung +x → unten-Block rot 90.
    assert out[0].rotation_deg == 90.0
    # RZ fern vom stair_exit bleibt unangetastet:
    fern = rz.model_copy(update={"xy_mm": (9000.0, 7000.0)})
    assert stiegenhaus_rz_nachpass([fern], rm)[0].xy_mm == (9000.0, 7000.0)
