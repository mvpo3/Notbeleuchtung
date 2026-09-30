"""wohnungsklasse — die zweistufige Klassenregel aus docs/GATE_TUERSTAPEL.md § 6g
in der Fassung der OWNER-ENTSCHEIDE vom 2026-09-21 (sie gehen § 6g vor).

Schritt 1 (Anker, ohne Iteration) entscheidet über Erreichbarkeit vom
STIEGENHAUS und den TÜRTYP — nie über eine Raumklasse — und er entscheidet
**nur PRIVAT endgültig**: „vom Stiegenhaus ohne Wohnungseingang erreichbar"
ist nach F11 nur die erste Hälfte eines UND und damit bloß Voraussetzung.
Schritt 2 (ALLGEMEIN bei zwei Wohnungen ODER einem Ausgang ODER einem
allgemeinen Nebenraum, sonst PRIVAT) läuft auf allem, was Schritt 1 offen
lässt, iterativ bis zum Fixpunkt mit Deckel 10. Schritt 3 führt Oszillatoren
als unbestimmt (``nutzungsklasse = None``) statt zu raten.

Darüber steht der Fail-Safe-Grundsatz des Owners: **im Zweifel Notlicht
behalten.** Notlicht (Flags, Anker, Leuchten) wird nur dort entzogen, wo die
ANKERREGEL privat bestätigt.
"""
from __future__ import annotations

import copy
import inspect
import itertools

import pytest
from shapely.geometry import Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Ausgang, Raum, Tuer
from notbeleuchtung.raumerkennung import wohnungsklasse as wk
from notbeleuchtung.raumerkennung.fluchtweg import fluchtwege
from notbeleuchtung.raumerkennung.wohnungen import bilde_wohnungen


def _tuer(tid, von, nach, detail=None, xy=(0.0, 0.0)):
    return Tuer(id=tid, xy_mm=xy, von_raum=von, nach_raum=nach,
                tuer_detail=detail)


def _rechteck(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


# ── (a) Schritt 1 entscheidet ohne Klassen ──────────────────────────────────
def _plan_a(detail_stiegenhaustuer: str):
    raeume = [Raum(id="vor", raum_typ="VORRAUM", ist_fluchtweg=True, ist_communal=True),
              Raum(id="zi", raum_typ="ZIMMER"),
              Raum(id="stgh", raum_typ="STIEGENHAUS", ist_fluchtweg=True,
                   ist_communal=True)]
    tueren = [_tuer("t1", "vor", "zi", "zimmertuer"),
              _tuer("t2", "vor", "stgh", detail_stiegenhaustuer)]
    return raeume, tueren


def test_schritt1_nur_ueber_wohnungseingang_ist_privat():
    """Ein VORRAUM, den man vom Stiegenhaus nur durch eine Wohnungseingangs-
    tür erreicht, ist PRIVAT (§ 6g Schritt 1)."""
    raeume, tueren = _plan_a("wohnungseingang")
    bilde_wohnungen(raeume, tueren)
    assert raeume[0].nutzungsklasse == "WOHNUNG_PRIVAT"


# ── (a2) E1: Schritt 1 entscheidet NUR PRIVAT endgültig ─────────────────────
def test_schritt1_entscheidet_nur_privat_endgueltig():
    """F11 ist ein UND: „ALLGEMEIN nur, wenn vom Stiegenhaus ohne Wohnungs-
    eingang erreichbar UND mindestens zwei Wohnungen oder ein Ausgang darüber
    erschlossen werden." Die Erreichbarkeit ist die VORAUSSETZUNG, kein
    Urteil — Schritt 1 gibt den Raum offen an Schritt 2 weiter
    (Owner-Korrektur 2026-09-21)."""
    raeume, tueren = _plan_a("stiegenhaustuer")
    assert wk.schritt1(raeume, tueren, {"vor"}) == {}


def test_schritt1_blattlose_oeffnung_geht_ebenfalls_an_schritt2():
    """Auch der nur durch eine blattlose Öffnung getrennte Raum ist nicht mehr
    sofort unbestimmt — er geht offen an Schritt 2 (Owner 2026-09-21)."""
    raeume, tueren = _plan_a("wohnungseingang")
    tueren[1].ohne_tuerblatt = True
    assert wk.schritt1(raeume, tueren, {"vor"}) == {}


def test_schritt1_wohnungseingang_mit_blatt_bleibt_endgueltig():
    raeume, tueren = _plan_a("wohnungseingang")
    klasse, grund = wk.schritt1(raeume, tueren, {"vor"})["vor"]
    assert klasse == wk.PRIVAT
    assert grund.startswith("Schritt 1")


def _plan_zwei_wohnungen():
    """Derselbe VORRAUM offen am Stiegenhaus, aber er erschließt ZWEI
    getrennte private Gruppen → nach F11 ALLGEMEIN."""
    raeume = [Raum(id="vor", raum_typ="VORRAUM", ist_fluchtweg=True,
                   ist_communal=True),
              Raum(id="zi1", raum_typ="ZIMMER"),
              Raum(id="zi2", raum_typ="ZIMMER"),
              Raum(id="stgh", raum_typ="STIEGENHAUS", ist_fluchtweg=True,
                   ist_communal=True)]
    tueren = [_tuer("t1", "vor", "zi1", "wohnungseingang"),
              _tuer("t2", "vor", "zi2", "wohnungseingang"),
              _tuer("t3", "vor", "stgh", "stiegenhaustuer")]
    return raeume, tueren


def test_schritt2_zwei_wohnungen_machen_allgemein():
    raeume, tueren = _plan_zwei_wohnungen()
    bilde_wohnungen(raeume, tueren)
    assert raeume[0].nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"


def test_schritt2_eine_wohnung_macht_privat():
    """Nur EINE Wohnung, kein Ausgang, kein Nebenraum → die zweite Hälfte von
    F11 ist nicht erfüllt → PRIVAT."""
    raeume, tueren = _plan_a("stiegenhaustuer")
    bilde_wohnungen(raeume, tueren)
    assert raeume[0].nutzungsklasse == "WOHNUNG_PRIVAT"


@pytest.mark.parametrize("detail,erwartet",
                         [("wohnungseingang", "WOHNUNG_PRIVAT"),
                          ("stiegenhaustuer", "WOHNUNG_PRIVAT")])
def test_schritt1_reihenfolge_invariant(detail, erwartet):
    """Gleiches Ergebnis bei umgedrehter Raum- UND Türliste (§ 6g Schritt 4)."""
    raeume, tueren = _plan_a(detail)
    bilde_wohnungen(raeume, tueren)
    vorwaerts = {r.id: r.nutzungsklasse for r in raeume}

    raeume_r, tueren_r = _plan_a(detail)
    raeume_r.reverse()
    tueren_r.reverse()
    bilde_wohnungen(raeume_r, tueren_r)
    rueckwaerts = {r.id: r.nutzungsklasse for r in raeume_r}

    assert vorwaerts == rueckwaerts
    assert vorwaerts["vor"] == erwartet


def test_schritt1_liest_keine_raumklasse_per_konstruktion():
    """Schritt 1 bekommt Raum-IDs und Türen — kein Raum-Objekt, also KANN er
    die Nutzungsklasse nicht lesen (§ 6g: „per Konstruktion")."""
    quelle = inspect.getsource(wk._erreichbar)
    assert "nutzungsklasse" not in quelle
    parameter = set(inspect.signature(wk._erreichbar).parameters)
    assert parameter == {"start", "tueren", "durch_wohnungseingang"}


# ── (b) Schritt 2: Fixpunkt, Deckel 10 ──────────────────────────────────────
def _oszillator():
    """Drei Gänge im Stern um g0, an g0 ein Zimmer z0 (gefunden per
    Zufallssuche, Runde 7). Mit „erschließt" TRANSITIV über allgemeine Räume
    (Owner Board 5, 2026-09-21) pendelt die Iteration aus dem Start
    „alle allgemein" mit Periode 3: alle allgemein → g0 erreicht über g1/g2
    nur z0 → alle privat → g0 zählt z0, g1, g2 → g0 allgemein → g1/g2 zählen
    über g0 z0 und den jeweils anderen → alle allgemein.

    Der alte Zwei-Gänge-Oszillator (g1–p1, g2–p2, g1–g2) pendelt mit der
    transitiven Regel nicht mehr: jeder Gang erreicht über den anderen beide
    Wohnungen, beide sind stabil allgemein."""
    return [_tuer("t0", "z0", "g0"),
            _tuer("t1", "g2", "g0"),
            _tuer("t2", "g0", "g1")]


def test_klassifiziere_erreicht_schritt2_ueberall_wo_schritt1_nicht_privat_sagt():
    """Gegenstück zur Runde-3-Behauptung „Schritt 2 ist unerreichbar": nach
    der Owner-Korrektur vom 2026-09-21 entscheidet Schritt 1 nur noch PRIVAT
    endgültig, also läuft Schritt 2 auf JEDEM Kandidaten, den keine
    Wohnungseingangstür mit Blatt abschließt. Der Test zählt die Aufrufe über
    dieselbe Türtyp-Matrix wie der alte Test."""
    rufe: list[set[str]] = []
    echt = wk.schritt2

    def spion(tueren, basis, offene, *rest, **kw):
        rufe.append(set(offene))
        return echt(tueren, basis, offene, *rest, **kw)

    details = (None, "zimmertuer", "wohnungseingang", "stiegenhaustuer")
    wk.schritt2 = spion
    try:
        for d_stgh in details:
            for d_zi in details:
                for blattlos in (True, False):
                    raeume, tueren = _plan_a(d_stgh)
                    tueren[1].ohne_tuerblatt = blattlos
                    tueren[0].tuer_detail = d_zi
                    wk.klassifiziere(raeume, tueren)
    finally:
        wk.schritt2 = echt
    # Nur die Kombination „wohnungseingang MIT Blatt" entscheidet Schritt 1
    # endgültig; das sind 4 der 32 Fälle (d_zi frei, blattlos=False).
    assert len(rufe) == 28, f"Schritt 2 lief {len(rufe)}x statt 28x"
    assert all(r == {"vor"} for r in rufe)


# ── (b2) E2: Schritt 2 kennt auch den allgemeinen Nebenraum ─────────────────
def test_schritt2_allgemeiner_nebenraum_macht_allgemein():
    """Owner-Erweiterung 2026-09-21: „in UG/KG gibt es keine Wohnungen — ein
    Kellergang würde sonst privat und verlöre sein Notlicht." Ein einziger
    ALLGEMEIN_NEBENRAUM reicht also."""
    tueren = [_tuer("t1", "g1", "kel")]
    klassen, gruende = wk.schritt2(tueren, {"kel": "ALLGEMEIN_NEBENRAUM"},
                                   {"g1"})
    assert klassen["g1"] == wk.ALLGEMEIN
    assert "Nebenraum" in gruende["g1"], gruende["g1"]


def test_schritt2_ausgang_macht_allgemein():
    tueren = [_tuer("t1", "g1", "AUSSEN", "hauseingang")]
    klassen, _ = wk.schritt2(tueren, {}, {"g1"})
    assert klassen["g1"] == wk.ALLGEMEIN


def test_schritt2_nebenraum_menge_kommt_aus_nutzungsklasse_py():
    """Die Menge wird nicht erfunden: jeder Kanon-Typ, den
    ``nutzungsklasse.py`` auf ALLGEMEIN_NEBENRAUM abbildet (Keller, Technik,
    Garage, Lager, Müllraum, Waschküche, Kinderwagenraum), macht den Gang
    allgemein."""
    from notbeleuchtung.raumerkennung.nutzungsklasse import (
        _MAP,
        nutzungsklasse_fuer,
    )

    typen = [t for t, k in _MAP.items() if k == "ALLGEMEIN_NEBENRAUM"]
    assert len(typen) >= 7, typen
    for typ in typen:
        klassen, _ = wk.schritt2([_tuer("t1", "g1", "n")],
                                 {"n": nutzungsklasse_fuer(typ)}, {"g1"})
        assert klassen["g1"] == wk.ALLGEMEIN, typ


def test_schritt2_eine_wohnung_ohne_nebenraum_bleibt_privat():
    klassen, _ = wk.schritt2([_tuer("t1", "g1", "p1", "wohnungseingang")],
                             {"p1": "WOHNUNG_PRIVAT"}, {"g1"})
    assert klassen["g1"] == wk.PRIVAT


def test_schritt2_konvergiert_auf_fixpunkt():
    """Ein Gang mit genau einer privaten Komponente wird privat — in einer
    Runde stabil."""
    tueren = [_tuer("t1", "g1", "p1", "wohnungseingang")]
    basis = {"p1": "WOHNUNG_PRIVAT"}
    klassen, gruende = wk.schritt2(tueren, basis, {"g1"})
    assert klassen["g1"] == "WOHNUNG_PRIVAT"
    assert "Schritt 2" in gruende["g1"]


def test_schritt2_deckel_macht_oszillator_unbestimmt():
    """Der Deckel greift: ein Oszillator wird unbestimmt (None), nicht
    endlos gerechnet."""
    tueren = _oszillator()
    basis = {"z0": "WOHNUNG_PRIVAT"}
    klassen, gruende = wk.schritt2(tueren, basis, {"g0", "g1", "g2"})
    assert klassen == {"g0": None, "g1": None, "g2": None}, klassen
    assert f"{wk.DECKEL}" in gruende["g1"]
    assert "oszill" in gruende["g1"].lower()


def test_schritt2_deckel_behauptet_nicht_dass_die_regel_keinen_fixpunkt_hat():
    """Reviewer-Befund Runde 5 (Linse Regel, latent): der Deckel-Text darf nur
    sagen, dass die ITERATION keinen Fixpunkt erreicht — der Stern-Oszillator
    HAT Fixpunkte, etwa (g0 allgemein, g1 privat, g2 allgemein): g0 zählt z0
    und g1, g1 erreicht über den allgemeinen g0 genau die Wohnung z0, g2 über
    g0 z0 und g1. Belegt mit der transitiven Zählung (Board 5)."""
    tueren = _oszillator()
    basis = {"z0": "WOHNUNG_PRIVAT"}
    fix = dict(basis, g0=wk.ALLGEMEIN, g1=wk.PRIVAT, g2=wk.ALLGEMEIN)
    assert wk._erschliesst("g0", tueren, fix)[0] >= 2          # → allgemein
    assert wk._erschliesst("g1", tueren, fix)[0] == 1          # → privat
    assert wk._erschliesst("g2", tueren, fix)[0] >= 2          # → allgemein
    klassen, gruende = wk.schritt2(tueren, basis, {"g0", "g1", "g2"})
    assert klassen == {"g0": None, "g1": None, "g2": None}
    for rid in ("g0", "g1", "g2"):
        assert "kein Fixpunkt" not in gruende[rid], gruende[rid]
        assert "Fixpunkt" in gruende[rid], gruende[rid]


# ── (c) Schritt 3: unbestimmt wird konservativ behandelt ────────────────────
def test_unbestimmt_erscheint_in_der_warnliste_mit_grund():
    warnungen = wk.warnungen_aus({"g1": None}, {"g1": "oszilliert nach 10 Runden"})
    assert warnungen == ["unbestimmt: g1 — oszilliert nach 10 Runden"]


def test_fluchtweg_klasse_ohne_fallback_auf_den_statischen_default():
    """§ 6g nennt ``fluchtweg._klasse`` wörtlich als Stelle, die zum Slice
    gehört: der stille Rückfall auf ``nutzungsklasse_fuer(raum_typ)`` macht aus
    einem unbestimmten VORRAUM WOHNUNG_PRIVAT und aus einem unbestimmten GANG
    ALLGEMEIN_ERSCHLIESSUNG — genau die willkürliche Festlegung, die § 6g
    ausschließt. Heute übt die Zeile nichts aus (``erschliessung`` fängt die
    unbestimmten über die explizite Menge ab), aber ein vierter Aufrufer macht
    sie wieder scharf."""
    from notbeleuchtung.raumerkennung import fluchtweg

    for typ in ("VORRAUM", "GANG"):
        r = Raum(id="x", raum_typ=typ, nutzungsklasse=None)
        assert fluchtweg._klasse(r) is None, f"{typ}: Fallback steht noch"


def _unbestimmter_gang():
    """Modellzustand mit EINEM unbestimmten Gang (Klasse None, Flags wie
    gestempelt) plus Stiegenhaus und Ausgang."""
    gang = Raum(id="gang", raum_typ="GANG", polygon_mm=_rechteck(5000, 0, 15000, 4000),
                ist_fluchtweg=True, ist_communal=True, nutzungsklasse=None)
    stgh = Raum(id="stgh", raum_typ="STIEGENHAUS", polygon_mm=_rechteck(0, 0, 5000, 4000),
                ist_fluchtweg=True, ist_communal=True,
                nutzungsklasse="ALLGEMEIN_ERSCHLIESSUNG")
    keller = Raum(id="kel", raum_typ="KELLER", polygon_mm=_rechteck(15000, 0, 20000, 4000),
                  nutzungsklasse="ALLGEMEIN_NEBENRAUM")
    tueren = [_tuer("tw", "gang", "stgh", "wohnungseingang", xy=(5000.0, 2000.0)),
              _tuer("tk", "gang", "kel", None, xy=(15000.0, 2000.0)),
              _tuer("tx", "stgh", "AUSSEN", "hauseingang", xy=(0.0, 2000.0))]
    return [gang, stgh, keller], tueren


def test_unbestimmter_raum_behaelt_anker_und_leuchte():
    """Konservativ (§ 6g Schritt 3): unbestimmt heißt nicht privat — R3 nimmt
    die Flags nicht weg, der Klassenfilter der Platzierung (nutzungsklasse ==
    WOHNUNG_PRIVAT) greift nicht, R4 lässt den Gang communal."""
    raeume, tueren = _unbestimmter_gang()
    gang = raeume[0]
    assert gang.id in wk.unbestimmte_raeume(raeume, tueren)
    wk.setze_wohnungsflags(raeume, tueren)
    assert gang.nutzungsklasse is None
    assert gang.ist_fluchtweg is True and gang.ist_communal is True


def test_unbestimmter_raum_bleibt_knoten_im_graph():
    """Und er reißt den Graph nicht auf: der Weg aus dem Keller findet den
    Ausgang weiterhin."""
    raeume, tueren = _unbestimmter_gang()
    ausgaenge = [Ausgang(id="exit_tx", xy_mm=(0.0, 2000.0), typ="final_exit")]
    segmente = fluchtwege(raeume, tueren, ausgaenge, [], "EG")
    graph = [s for s in segmente if s.quelle == "GRAPH"]
    assert graph, "unbestimmter Gang fällt als Knoten aus dem Fluchtweg-Graph"


# ── (e) Durchleitung ────────────────────────────────────────────────────────
def _durchleitung_plan():
    """KELLER → GANG g1 → privater GANG v (Wohnungseingang zum Stiegenhaus)
    → GANG g2 → Hauseingang. Ohne Durchleitung zerfällt der Weg an v. Am
    privaten Gang liegt das Zimmer z: seit G4 (Owner 2026-09-22) wird nur
    entzogen, wenn hinter dem Wohnungseingang ein Aufenthaltsraum liegt."""
    raeume = [
        Raum(id="kel", raum_typ="KELLER", polygon_mm=_rechteck(0, 0, 5000, 4000)),
        Raum(id="g1", raum_typ="GANG", polygon_mm=_rechteck(5000, 0, 10000, 4000),
             ist_fluchtweg=True, ist_communal=True),
        Raum(id="v", raum_typ="GANG", polygon_mm=_rechteck(10000, 0, 15000, 4000),
             ist_fluchtweg=True, ist_communal=True),
        Raum(id="g2", raum_typ="GANG", polygon_mm=_rechteck(15000, 0, 20000, 4000),
             ist_fluchtweg=True, ist_communal=True),
        Raum(id="stgh", raum_typ="STIEGENHAUS", polygon_mm=_rechteck(10000, 4000, 15000, 8000),
             ist_fluchtweg=True, ist_communal=True),
        Raum(id="z", raum_typ="ZIMMER", polygon_mm=_rechteck(10000, -4000, 15000, 0)),
    ]
    tueren = [
        _tuer("tk", "kel", "g1", None, xy=(5000.0, 2000.0)),
        _tuer("ta", "g1", "v", "zimmertuer", xy=(10000.0, 2000.0)),
        _tuer("tb", "v", "g2", "zimmertuer", xy=(15000.0, 2000.0)),
        _tuer("tw", "v", "stgh", "wohnungseingang", xy=(12500.0, 4000.0)),
        _tuer("tx", "g2", "AUSSEN", "hauseingang", xy=(20000.0, 2000.0)),
        _tuer("tz", "v", "z", "zimmertuer", xy=(12500.0, 0.0)),
    ]
    return raeume, tueren


def test_durchleitung_zerreisst_den_weg_nicht():
    raeume, tueren = _durchleitung_plan()
    bilde_wohnungen(raeume, tueren)
    v = next(r for r in raeume if r.id == "v")
    assert v.nutzungsklasse == "WOHNUNG_PRIVAT", "Schritt 1 hat v nicht privat gemacht"
    ausgaenge = [Ausgang(id="exit_tx", xy_mm=(20000.0, 2000.0), typ="final_exit")]
    segmente = fluchtwege(raeume, tueren, ausgaenge, [], "EG")
    durch_v = [s for s in segmente if s.quelle == "GRAPH"
               and s.ziel_ausgang == "exit_tx" and s.start_raum == "kel"]
    assert durch_v, "kein Weg vom Keller zum Ausgang — der private Raum reißt den Graph auf"


def test_durchgeleiteter_raum_bekommt_keine_stuetzpunkte_und_keine_anker():
    raeume, tueren = _durchleitung_plan()
    bilde_wohnungen(raeume, tueren)
    v = next(r for r in raeume if r.id == "v")
    # R3: wohnungsinterner Gang ist kein Fluchtweg und nicht communal →
    # provider ruft anker_fuer_gang nicht mehr auf, R4 nimmt das FALLBACK-Segment.
    assert v.ist_fluchtweg is False and v.ist_communal is False
    ausgaenge = [Ausgang(id="exit_tx", xy_mm=(20000.0, 2000.0), typ="final_exit")]
    segmente = fluchtwege(raeume, tueren, ausgaenge, [], "EG")
    assert not [s for s in segmente if s.segment_id == "seg_fallback_v"]
    innen = Polygon(v.polygon_mm)
    drin = [p for s in segmente for p in s.polyline_mm if innen.contains(Point(p))]
    assert not drin, f"Stützpunkte im durchgeleiteten Raum: {drin}"


def test_durchleitung_wird_als_warnung_ausgewiesen():
    """Board-Antrag statt Contract-Änderung: die Wirkung wird gebaut, die
    Durchleitung als Provider-Warnung ausgewiesen (§ 6g)."""
    raeume, tueren = _durchleitung_plan()
    bilde_wohnungen(raeume, tueren)
    ausgaenge = [Ausgang(id="exit_tx", xy_mm=(20000.0, 2000.0), typ="final_exit")]
    notiz: list[str] = []
    fluchtwege(raeume, tueren, ausgaenge, [], "EG", durchleitung=notiz)
    assert [z for z in notiz if z.startswith("durchleitung:") and "v" in z], notiz


def _durchleitung_plan_direkt():
    """Derselbe Fall OHNE Zwischen-Gang: der Nebenraum hängt DIREKT am
    kippenden Raum (kel → v(privat) → g2 → Hauseingang). Genau diese
    Topologie nennt § 6g als Nebenwirkung (Rennweg UG KINDERWAGENRAUM
    21,49 m²); in ``_durchleitung_plan`` liegt der private Raum dagegen
    MITTEN im Weg und die Starttür hängt am communalen ``g1``."""
    raeume = [
        Raum(id="kel", raum_typ="KINDERWAGENRAUM",
             polygon_mm=_rechteck(0, 0, 5000, 4000)),
        Raum(id="v", raum_typ="GANG", polygon_mm=_rechteck(5000, 0, 10000, 4000),
             ist_fluchtweg=True, ist_communal=True),
        Raum(id="g2", raum_typ="GANG", polygon_mm=_rechteck(10000, 0, 15000, 4000),
             ist_fluchtweg=True, ist_communal=True),
        Raum(id="stgh", raum_typ="STIEGENHAUS",
             polygon_mm=_rechteck(5000, 4000, 10000, 8000),
             ist_fluchtweg=True, ist_communal=True),
    ]
    tueren = [
        _tuer("tk", "kel", "v", None, xy=(5000.0, 2000.0)),
        _tuer("tb", "v", "g2", "zimmertuer", xy=(10000.0, 2000.0)),
        _tuer("tw", "v", "stgh", "wohnungseingang", xy=(7500.0, 4000.0)),
        _tuer("tx", "g2", "AUSSEN", "hauseingang", xy=(15000.0, 2000.0)),
    ]
    return raeume, tueren


def test_nebenraum_direkt_am_privaten_raum_behaelt_seinen_weg():
    """Die Durchleitung darf auch dann kein Loch lassen, wenn die STARTTÜR
    selbst am (bis Runde 9) privaten Raum hängt — sonst fehlt genau der Fall,
    für den sie gebaut wurde. Seit dem Riegel (Owner 2026-09-22, G3: „Tür zu
    einem allgemeinen Nebenraum → in keinem Schritt PRIVAT") kippt v gar
    nicht mehr — er bleibt allgemein, und der Weg aus dem Nebenraum läuft als
    voller Knoten durch ihn."""
    raeume, tueren = _durchleitung_plan_direkt()
    bilde_wohnungen(raeume, tueren)
    v = next(r for r in raeume if r.id == "v")
    assert v.nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG", "G3: nie privat"
    assert (v.ist_fluchtweg, v.ist_communal) == (True, True)
    ausgaenge = [Ausgang(id="exit_tx", xy_mm=(15000.0, 2000.0), typ="final_exit")]
    segmente = fluchtwege(raeume, tueren, ausgaenge, [], "EG")
    aus_kel = [s for s in segmente if s.quelle == "GRAPH" and s.start_raum == "kel"]
    assert aus_kel, "kein Weg aus dem Nebenraum — Loch im Graph"


def _durchleitung_l_form():
    """Durchleitung durch einen L-förmigen privaten Gang: die Direktlinie
    zwischen seinen beiden Türen (10000,2000) → (2000,10000) läuft über
    (6000,6000) — außerhalb des L, also durch eine Wand."""
    l_form = [(0, 0), (10000, 0), (10000, 4000), (4000, 4000), (4000, 10000),
              (0, 10000)]
    raeume = [
        Raum(id="kel", raum_typ="KELLER", polygon_mm=_rechteck(0, 14000, 4000, 18000)),
        Raum(id="g1", raum_typ="GANG", polygon_mm=_rechteck(0, 10000, 4000, 14000),
             ist_fluchtweg=True, ist_communal=True),
        Raum(id="v", raum_typ="GANG", polygon_mm=l_form,
             ist_fluchtweg=True, ist_communal=True),
        Raum(id="g2", raum_typ="GANG", polygon_mm=_rechteck(10000, 0, 15000, 4000),
             ist_fluchtweg=True, ist_communal=True),
        Raum(id="stgh", raum_typ="STIEGENHAUS", polygon_mm=_rechteck(-5000, 0, 0, 4000),
             ist_fluchtweg=True, ist_communal=True),
        # G4 (Owner 2026-09-22): ein Zimmer in der Wohnung des privaten Gangs.
        Raum(id="z", raum_typ="ZIMMER", polygon_mm=_rechteck(4000, 4000, 10000, 10000)),
    ]
    tueren = [
        _tuer("tk", "kel", "g1", None, xy=(2000.0, 14000.0)),
        _tuer("tb", "g1", "v", "zimmertuer", xy=(2000.0, 10000.0)),
        _tuer("ta", "v", "g2", "zimmertuer", xy=(10000.0, 2000.0)),
        _tuer("tw", "v", "stgh", "wohnungseingang", xy=(0.0, 2000.0)),
        _tuer("tx", "g2", "AUSSEN", "hauseingang", xy=(15000.0, 2000.0)),
        _tuer("tz", "v", "z", "zimmertuer", xy=(7000.0, 4000.0)),
    ]
    return raeume, tueren


def test_durchleitung_fuehrt_nicht_durch_die_wand():
    """Reviewer-Hinweis Runde 3: bei einem nicht-konvexen Raum verlässt die
    Direktlinie das Polygon — dann liefe ein GRAPH-Segment durch eine Wand.
    Kleinster Eingriff: nur durchleiten, wenn das Raumpolygon die Strecke
    deckt, sonst Skelettpfad (die übrigen Durchleitungs-Tests nutzen nur
    Rechtecke)."""
    from shapely.geometry import LineString
    from shapely.ops import unary_union

    raeume, tueren = _durchleitung_l_form()
    bilde_wohnungen(raeume, tueren)
    v = next(r for r in raeume if r.id == "v")
    assert v.id in wk.durchleitung_raeume(raeume, tueren), "Vorbedingung"
    ausgaenge = [Ausgang(id="exit_tx", xy_mm=(15000.0, 2000.0), typ="final_exit")]
    notiz: list[str] = []
    segmente = fluchtwege(raeume, tueren, ausgaenge, [], "EG", durchleitung=notiz)
    weg = next(s for s in segmente if s.segment_id == "seg_graph_tk")
    innen = unary_union([Polygon(r.polygon_mm) for r in raeume
                         if r.id in ("kel", "g1", "v", "g2")]).buffer(50.0)
    assert innen.covers(LineString(weg.polyline_mm)), (
        "GRAPH-Segment verlässt die Räume — Direktlinie durch die Wand")
    assert [z for z in notiz if "NICHT direkt" in z and " v " in z + " "], notiz


# ── (g) Türblatt: eine blattlose Öffnung schließt keine Wohnung ab ──────────
def test_blattlose_stiegenhausoeffnung_behaelt_ihr_notlicht():
    """§ 6f verlangt je Kipp-Raum den Nachweis, dass er wirklich wohnungs-
    intern ist. Eine Öffnung OHNE Türblatt (DG2: 4854 mm) schließt keine
    Wohnung ab. Seit der Owner-Korrektur 2026-09-21 entscheidet Schritt 2 die
    KLASSE (hier: eine Wohnung, kein Ausgang, kein Nebenraum → privat) — das
    NOTLICHT bleibt trotzdem, weil die Ankerregel den Raum nicht privat
    bestätigt — Grundsatz „im Zweifel Notlicht behalten"."""
    raeume, tueren = _plan_a("wohnungseingang")
    tueren[1].ohne_tuerblatt = True
    bilde_wohnungen(raeume, tueren)
    vor = next(r for r in raeume if r.id == "vor")
    assert vor.id not in wk.bestaetigt_privat(raeume, tueren)
    assert vor.ist_fluchtweg is True and vor.ist_communal is True


def test_stiegenhaustuer_mit_blatt_entscheidet_weiter():
    """Gegenprobe: MIT Türblatt bleibt es bei der Entscheidung aus Schritt 1."""
    raeume, tueren = _plan_a("wohnungseingang")
    tueren[1].ohne_tuerblatt = False
    bilde_wohnungen(raeume, tueren)
    assert raeume[0].nutzungsklasse == "WOHNUNG_PRIVAT"


# ── (h) ehemals Rückkopplung Klasse → Türrolle → Klasse (seit E7 entfallen) ─
def _rueckkopplung():
    """Der Mechanismus von Barawitzka ``raum_19`` im Kleinen: der VORRAUM ist
    vom STIEGENHAUS über die Kette stgh → ABSTELLRAUM → vor offen erreichbar.
    Bis Runde 6 machte die Rollenkorrektur in ``bilde_wohnungen`` aus den
    Kettentüren ``wohnungseingang``, und die Ankerregel las das in der
    nächsten Runde — die Rückkopplung Klasse → Türrolle → Klasse. Seit E7
    (Owner Board 7) liest die Klassifikation nur die ROHEN Rollen; die
    korrigierten werden danach abgeleitet und nie zurückgelesen."""
    raeume = [Raum(id="vor", raum_typ="VORRAUM", ist_fluchtweg=True,
                   ist_communal=True),
              Raum(id="ar", raum_typ="ABSTELLRAUM"),
              Raum(id="stgh", raum_typ="STIEGENHAUS", ist_fluchtweg=True,
                   ist_communal=True)]
    tueren = [_tuer("t_we", "vor", "stgh", "wohnungseingang"),
              _tuer("t_kette", "stgh", "ar", "zimmertuer"),
              _tuer("t_ar", "ar", "vor", "zimmertuer")]
    return raeume, tueren


def test_rueckkopplung_laeuft_auf_einen_fixpunkt():
    """Befund B1: der ausgelieferte Zustand muss ein Fixpunkt der eigenen
    Regel sein — eine Nachrechnung auf dem ausgelieferten Modell liefert
    dieselbe Klasse. Seit E7 gilt das per Konstruktion: das Modell trägt die
    rohen Rollen, die Nachrechnung liest dieselbe Eingabe."""
    raeume, tueren = _rueckkopplung()
    bilde_wohnungen(raeume, tueren)
    nach, _ = wk.klassifiziere(raeume, tueren)
    for r in raeume:
        if r.id in nach:
            assert r.nutzungsklasse == nach[r.id], (
                f"{r.id}: ausgeliefert {r.nutzungsklasse}, Nachrechnung {nach[r.id]}")


def _zustand(raeume, tueren):
    """Der vollständige ausgelieferte Zustand — alles, was ``bilde_wohnungen``
    anfasst."""
    return ({r.id: (r.nutzungsklasse, r.ist_fluchtweg, r.ist_communal,
                    r.wohnung_id) for r in raeume},
            {t.id: t.tuer_detail for t in tueren})


@pytest.mark.parametrize("bau", [_plan_zwei_wohnungen, _rueckkopplung,
                                 _durchleitung_plan, _durchleitung_plan_direkt,
                                 _unbestimmter_gang],
                         ids=lambda f: f.__name__.lstrip("_"))
def test_bilde_wohnungen_ist_idempotent(bau):
    """Befund B1: derselbe Aufruf ein zweites Mal auf dem ausgelieferten
    Modell muss denselben Zustand liefern — Klassen, Flags, ``wohnung_id`` und
    Türrollen."""
    raeume, tueren = bau()
    bilde_wohnungen(raeume, tueren)
    eins = _zustand(raeume, tueren)
    bilde_wohnungen(raeume, tueren)
    assert _zustand(raeume, tueren) == eins


def test_setze_wohnungsflags_gibt_flags_auch_zurueck():
    """B1, gemessene Ursache: R3 nahm Flags nur WEG. Wird ein Raum wieder
    nicht-privat, muss er sie zurückbekommen, sonst entsteht der Mischzustand
    „Klasse allgemein, Flags [0,0]" (Barawitzka EG ``raum_30``)."""
    raeume, tueren = _unbestimmter_gang()
    gang = raeume[0]
    gang.ist_fluchtweg = gang.ist_communal = False
    assert wk.setze_wohnungsflags(raeume, tueren) == ["gang"]
    assert (gang.ist_fluchtweg, gang.ist_communal) == (True, True)


def test_wohnung_id_wird_geleert_wenn_der_raum_die_private_menge_verlaesst():
    """B1, zweite gemessene Ursache: ``wohnung_id`` wurde nie geleert."""
    raeume, tueren = _plan_zwei_wohnungen()
    raeume[0].wohnung_id = "top_alt"
    bilde_wohnungen(raeume, tueren)
    assert raeume[0].nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"
    assert raeume[0].wohnung_id is None


# ── (i) E3: Fail-Safe-Riegel der Ankerregel ────────────────────────────────
def _nicht_kandidat(stiegenhaus_kette: bool):
    """GANG ohne eigene Stiegenhaustür — über ihn entscheidet nicht das
    zweistufige Verfahren, sondern ``_verfeinere_gang_privat``, und die macht
    ihn privat (nur private Nachbarn, keine Tür in Stiegenhaus oder AUSSEN).

    Mit ``stiegenhaus_kette`` erreicht ihn die Ankerregel vom Stiegenhaus
    trotzdem OHNE Wohnungseingang — über blattlose Durchgänge, die die
    Rollenkorrektur nicht anfasst (``tuer_detail`` ist ``None``). Genau diese
    Topologie haben die fünf widersprochenen Räume: BARA ``raum_31`` über
    ``durchgang_20``, MOLL_EG ``raum_56`` über ``durchgang_31``.
    Ohne die Kette erreicht sie ihn gar nicht — die 13 nicht auswertbaren.
    """
    raeume = [Raum(id="g", raum_typ="GANG", ist_fluchtweg=True,
                   ist_communal=True),
              Raum(id="zi", raum_typ="ZIMMER"),
              Raum(id="neben", raum_typ="ABSTELLRAUM"),
              Raum(id="stgh", raum_typ="STIEGENHAUS", ist_fluchtweg=True,
                   ist_communal=True)]
    tueren = [_tuer("t1", "g", "zi", "zimmertuer"),
              _tuer("t2", "g", "neben", None)]
    if stiegenhaus_kette:
        tueren.append(_tuer("durchgang_1", "neben", "stgh", None))
    return raeume, tueren


def test_widersprochener_raum_wird_allgemein_und_behaelt_notlicht():
    """E3: „Die Ankerregel sagt allgemein, also gilt allgemein." Auf den
    Prüfplänen seit Runde 7 (Ankerregel auf rohen Rollen, E5): Mollgasse EG
    ``raum_22``/``raum_56`` und Barawitzka ``raum_31`` über die Ankerregel,
    Mollgasse EG ``raum_29``/``raum_57`` als Paar mit zwei Fixpunkten (E5)."""
    raeume, tueren = _nicht_kandidat(stiegenhaus_kette=True)
    warnungen: list[str] = []
    bilde_wohnungen(raeume, tueren, warnungen)
    g = raeume[0]
    assert g.nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"
    assert (g.ist_fluchtweg, g.ist_communal) == (True, True)
    assert g.id not in wk.bestaetigt_privat(raeume, tueren)


def test_nicht_auswertbarer_raum_behaelt_notlicht():
    """E3: die 13 vom Stiegenhaus über KEINE Tür erreichbaren Räume — laut
    Owner ein Tür- oder Raumerkennungsloch (Messfall für S4c/S3b), kein
    Klassifikationsproblem. Sie behalten Notlicht; die Iteration führt sie
    mit Grund als unbestimmt. K4 (Owner 2026-09-30) gibt ihm danach die
    Klasse aus dem Wohnungsumriss — g ist über die rohe Zimmertür Mitglied
    der Wohnung des Zimmers → privat; die Ankerregel bestätigt das nicht,
    Notlicht bleibt."""
    raeume, tueren = _nicht_kandidat(stiegenhaus_kette=False)
    warnungen: list[str] = []
    bilde_wohnungen(raeume, tueren, warnungen)
    g = raeume[0]
    assert g.nutzungsklasse == "WOHNUNG_PRIVAT"
    assert (g.ist_fluchtweg, g.ist_communal) == (True, True)
    assert g.id not in wk.bestaetigt_privat(raeume, tueren)
    assert [w for w in warnungen if w.startswith("k4: g — privat")
            and "vorher unbestimmt" in w and "erreichbar" in w], warnungen


def test_v2_kandidat_ohne_ankerbestaetigung_behaelt_notlicht():
    """E3, vierter Punkt: „liegt ein V2-Raum außerhalb der 14 bestätigten,
    behält er Notlicht." Schritt 2 macht diesen Vorraum privat (eine Wohnung),
    die Ankerregel bestätigt das aber nicht — also bleiben Flags stehen."""
    raeume, tueren = _plan_a("stiegenhaustuer")
    bilde_wohnungen(raeume, tueren)
    vor = raeume[0]
    assert vor.nutzungsklasse == "WOHNUNG_PRIVAT"
    assert (vor.ist_fluchtweg, vor.ist_communal) == (True, True)
    assert vor.id not in wk.bestaetigt_privat(raeume, tueren)


def test_ankerbestaetigter_raum_verliert_notlicht():
    """Die Gegenprobe: die 14 bestätigten (91,40 m²) verlieren beide Flags."""
    raeume, tueren = _plan_a("wohnungseingang")
    bilde_wohnungen(raeume, tueren)
    vor = raeume[0]
    assert vor.nutzungsklasse == "WOHNUNG_PRIVAT"
    assert vor.id in wk.bestaetigt_privat(raeume, tueren)
    assert (vor.ist_fluchtweg, vor.ist_communal) == (False, False)


def test_ankerregel_ist_dieselbe_funktion_wie_in_schritt1():
    """E3 wörtlich: „Die Ankerregel ist dieselbe Funktion wie in Schritt 1 —
    wiederverwenden, nicht nachbauen." Schritt 1 ruft ``ankerurteil``."""
    assert "ankerurteil(" in inspect.getsource(wk.schritt1)
    assert "ankerurteil(" in inspect.getsource(wk.bestaetigt_privat)


def test_ankergrund_nennt_die_wohnungseingangstuer_des_pfads():
    """§ 6g Punkt 4 verlangt „über welche Tür". Der Grund nannte bisher die
    LETZTE Tür des Pfads — gemessen OG1 ``raum_4``: „nur über die
    Wohnungseingangstür durchgang_3 (mit Türblatt)", obwohl ``durchgang_3``
    eine blattlose Zimmertür ist. Genannt werden muss die Wohnungseingangstür,
    über die der Pfad läuft (mit Blatt), bzw. die blattlose Öffnung."""
    raeume = [Raum(id="stgh", raum_typ="STIEGENHAUS"),
              Raum(id="vor", raum_typ="VORRAUM"),
              Raum(id="g", raum_typ="GANG")]
    tueren = [_tuer("t_we", "stgh", "vor", "wohnungseingang"),
              _tuer("t_z", "vor", "g", "zimmertuer")]
    tueren[1].ohne_tuerblatt = True
    urteil, grund = wk.ankerurteil(raeume, tueren)["g"]
    assert urteil == wk.A_PRIVAT
    assert "t_we" in grund and "t_z" not in grund, grund
    tueren[0].ohne_tuerblatt = True
    urteil, grund = wk.ankerurteil(raeume, tueren)["g"]
    assert urteil == wk.A_UNKLAR
    assert "t_we" in grund and "t_z" not in grund, grund


@pytest.mark.parametrize("blattlos_aussen,blattlos_innen,urteil_g,tuer",
                         [(False, True, "privat", "t_we"),
                          (True, False, "privat", "t_z"),
                          (True, True, "unklar", "t_z")])
def test_blattlose_innentuer_hebt_den_wohnungsabschluss_nicht_auf(
        blattlos_aussen, blattlos_innen, urteil_g, tuer):
    """E1: PRIVAT, wenn der Raum nur über eine Wohnungseingangstür MIT Blatt
    erreichbar ist; offen, wenn ihn vom Stiegenhaus NUR eine blattlose
    Öffnung trennt. Liegt auf dem Weg eine Wohnungseingangstür MIT Blatt, ist
    der Raum abgeschlossen — gleich, ob dahinter noch eine blattlose
    Wohnungseingangs-Öffnung folgt. Runde 4 sperrte jede blattlose Öffnung in
    der Blatt-Suche und machte so Rennweg OG1 ``raum_4``/``raum_5`` (hinter
    ``tuer_3`` MIT Blatt und ``durchgang_1`` ohne) unauswertbar — bestätigt
    wurden sie erst über die Rollenkorrektur, die ``durchgang_1`` zur
    Zimmertür machte: eine Klasse, die sich über abgeleitete Türrollen selbst
    bestätigt."""
    raeume = [Raum(id="stgh", raum_typ="STIEGENHAUS"),
              Raum(id="vor", raum_typ="VORRAUM"),
              Raum(id="g", raum_typ="GANG")]
    tueren = [_tuer("t_we", "stgh", "vor", "wohnungseingang"),
              _tuer("t_z", "vor", "g", "wohnungseingang")]
    tueren[0].ohne_tuerblatt = blattlos_aussen
    tueren[1].ohne_tuerblatt = blattlos_innen
    urteil, grund = wk.ankerurteil(raeume, tueren)["g"]
    assert urteil == urteil_g, grund
    assert tuer in grund, grund


def _vorraum_am_keller():
    """Kandidat G am Stiegenhaus mit einem Zimmer, dahinter der VORRAUM V
    hinter einem Wohnungseingang MIT Blatt; V hat eine Tür zu einem KELLER.
    Die Ankerregel nennt V privat, die Flur-Verfeinerung hält ihn allgemein
    (Nachbar KELLER). In Runde 8 startete V beim Ankerurteil privat und
    bewegte sich in Runde 1; seit Runde 9 startet er allgemein (Board 4)."""
    return ([_r("S", "STIEGENHAUS"), _r("G", "GANG"), _r("V", "VORRAUM"),
             _r("Z1", "ZIMMER", False), _r("Z2", "ZIMMER", False),
             _r("K", "KELLER", False)],
            [_t("ts", "G", "S", "stiegenhaustuer"),
             _t("w1", "G", "Z1", "wohnungseingang"),
             _t("wv", "G", "V", "wohnungseingang"),
             _t("z", "V", "Z2", "zimmertuer"),
             _t("k", "V", "K")])


def _vorraum_hinter_blatt():
    """Wie ``_vorraum_am_keller``, aber ohne Keller: V liegt nur an einem
    Zimmer und (hinter ``wv`` MIT Blatt) am allgemeinen Gang G — sein einziger
    Fixpunkt ist privat. V startet bei allgemein (Runde 9, L1) und wechselt
    in Runde 1 auf privat; Runde 2 bestätigt."""
    raeume, tueren = _vorraum_am_keller()
    return ([r for r in raeume if r.id != "K"], [t for t in tueren if t.id != "k"])


def test_ohne_fixpunkt_im_deckel_wird_alles_bewegte_unbestimmt(monkeypatch):
    """Die Klassen-Iteration (Schritt 2 und Flur-Verfeinerung, seit Runde 7
    EINE Iteration — E7: die äußere Kette über die Türrollen gibt es nicht
    mehr) hat den Deckel ``DECKEL``. Erreicht sie darin keinen Fixpunkt, wird
    nicht die Phase ausgeliefert, in der man aufgehört hat zu rechnen: jeder
    Raum, dessen Klasse sich unterwegs bewegt hat, wird unbestimmt geführt —
    mit Grund, und er behält sein Notlicht. Hier erzwungen mit ``DECKEL = 1``:
    V wechselt in Runde 1 von allgemein (Start, Board 4) auf privat. (Runde 8
    nahm ``_vorraum_am_keller``, dessen V beim Ankerurteil privat startete;
    seit alle Nicht-Kandidaten allgemein starten, bewegt sich dort nichts.)

    K4 (Owner 2026-09-30) überstimmt das „bleibt unbestimmt" danach: V ist
    Mitglied seiner Wohnung → privat, und weil die Ankerregel V privat
    bestätigt (nur hinter ``wv`` mit Blatt, Zimmer in der Wohnung), entzieht
    ``bestaetigt_privat`` ihm das Notlicht — dasselbe Ergebnis wie ohne
    Deckel. Auf den 23 Prüfgeschossen gibt es keinen solchen Fall
    (docs/SLICES_K1_K4.md, K4)."""
    from notbeleuchtung.raumerkennung import wohnungen as W

    monkeypatch.setattr(W, "DECKEL", 1)
    raeume, tueren = _vorraum_hinter_blatt()
    warnungen: list[str] = []
    bilde_wohnungen(raeume, tueren, warnungen)
    v = next(x for x in raeume if x.id == "V")
    assert v.nutzungsklasse == "WOHNUNG_PRIVAT"
    assert (v.ist_fluchtweg, v.ist_communal) == (False, False)
    assert "V" in wk.bestaetigt_privat(raeume, tueren)
    assert [w for w in warnungen if w.startswith("k4: V — privat")
            and "Schritt 3" in w and "keinen Fixpunkt" in w], warnungen
    monkeypatch.undo()
    raeume, tueren = _vorraum_hinter_blatt()
    bilde_wohnungen(raeume, tueren)
    v = next(x for x in raeume if x.id == "V")
    assert v.nutzungsklasse == "WOHNUNG_PRIVAT", "ohne Deckel: Fixpunkt"


# ── (j) B2: Stiegenhaus-Anker, der in einen privaten Raum fällt ────────────
def test_anker_wird_auf_die_stiegenhaus_seite_gezogen():
    """Befund B2: die Türanker des Stiegenhauses liegen auf der Schwelle. Wird
    der Nachbarraum privat, liegt der Anker geometrisch IN einer Wohnung —
    genau die Verletzung, deren Beseitigung die Abnahmezahl des Slices ist
    (Mollgasse 1OG ``raum_2``/``4``/``69``/``72``, je 0 → 1). Er wird auf die
    Stiegenhaus-Seite gezogen statt gestrichen: ein gestrichener Türanker
    kostet das Rettungszeichen an der Stiegenhaustür."""
    from notbeleuchtung.hauptengine.contracts.raum_modell import Anker

    stgh = Raum(id="stgh", raum_typ="STIEGENHAUS",
                polygon_mm=_rechteck(0, 0, 5000, 4000),
                nutzungsklasse="ALLGEMEIN_ERSCHLIESSUNG")
    vor = Raum(id="vor", raum_typ="VORRAUM",
               polygon_mm=_rechteck(5000, 0, 9000, 4000),
               nutzungsklasse="WOHNUNG_PRIVAT")
    tueren = [_tuer("tw", "vor", "stgh", "wohnungseingang", xy=(5000.0, 2000.0))]
    raeume = [stgh, vor]
    # Der Anker liegt 1 mm INNERHALB des privaten Vorraums.
    a = Anker(id="stgh_tuer_tw", typ="TUER", xy_mm=(5001.0, 2000.0),
              raum_id="stgh")
    neu = wk.anker_aus_privat_ziehen([a], raeume, tueren)
    assert len(neu) == 1
    assert not Polygon(vor.polygon_mm).contains(Point(neu[0].xy_mm))
    assert Polygon(stgh.polygon_mm).buffer(1.0).contains(Point(neu[0].xy_mm))


def test_fremder_anker_wird_auch_aus_unbestaetigt_privatem_raum_gezogen():
    """B2 wörtlich: „Stiegenhaus-Anker, die geometrisch in einen privat
    GEWORDENEN Raum fallen" — privat geworden ist auch ein Raum, den Schritt 2
    privat macht, ohne dass die Ankerregel bestätigt (gemessen Mollgasse EG
    ``raum_7``: vier Anker von STIEGENHAUS ``raum_51`` darin). Der fremde Anker
    wird gezogen; die EIGENEN Anker des Raums bleiben — er behält sein
    Notlicht (Grundsatz).

    Planer-Entscheid P2 (Runde 11) würde diese Zusicherung umdrehen; er ist
    NICHT gebaut, siehe ``anker_aus_privat_ziehen`` und Bericht Runde 11."""
    from notbeleuchtung.hauptengine.contracts.raum_modell import Anker

    stgh = Raum(id="stgh", raum_typ="STIEGENHAUS",
                polygon_mm=_rechteck(0, 0, 5000, 4000),
                nutzungsklasse="ALLGEMEIN_ERSCHLIESSUNG")
    vor = Raum(id="vor", raum_typ="VORRAUM",
               polygon_mm=_rechteck(5000, 0, 9000, 4000),
               nutzungsklasse="WOHNUNG_PRIVAT")
    tueren = [_tuer("ts", "vor", "stgh", "stiegenhaustuer", xy=(5000.0, 2000.0))]
    raeume = [stgh, vor]
    assert "vor" not in wk.bestaetigt_privat(raeume, tueren), "Vorbedingung"
    fremd = Anker(id="stgh_tuer_ts", typ="TUER", xy_mm=(5001.0, 2000.0),
                  raum_id="stgh")
    eigen = Anker(id="vor_tuer_1", typ="TUER", xy_mm=(7000.0, 2000.0),
                  raum_id="vor")
    neu = {a.id: a for a in wk.anker_aus_privat_ziehen([fremd, eigen], raeume,
                                                       tueren)}
    assert set(neu) == {"stgh_tuer_ts", "vor_tuer_1"}
    assert not Polygon(vor.polygon_mm).contains(Point(neu["stgh_tuer_ts"].xy_mm))
    assert neu["vor_tuer_1"].xy_mm == (7000.0, 2000.0)


def test_stiegenhaus_anker_wird_auch_aus_privatem_zimmer_gezogen():
    """Slice S3b, Rennweg OG3 ``rest_3_tuer_tuer_4``: erreicht die Restfläche
    des Stiegenhauses die Blocktür, bekommt es seinen Türanker auf dem
    Türpunkt. Den deckt das gestempelte ZIMMER, das durch die Öffnung ragt —
    die Restfläche endet ``_BELEGT_PUFFER_MM`` + ½ Zelle davor (nominal
    125 mm, an ``tuer_4`` nach simplify/snap gemessen 118,5 mm).
    Gate (6) zählt JEDEN Raum der Klasse ``WOHNUNG_PRIVAT``, nicht nur
    GANG/VORRAUM: der Anker wird auch aus dem Zimmer auf die Stiegenhaus-Seite
    gezogen, nicht gestrichen."""
    from notbeleuchtung.hauptengine.contracts.raum_modell import Anker

    stgh = Raum(id="stgh", raum_typ="STIEGENHAUS",
                polygon_mm=_rechteck(0, 0, 4880, 4000),
                nutzungsklasse="ALLGEMEIN_ERSCHLIESSUNG")
    zi = Raum(id="zi", raum_typ="ZIMMER",
              polygon_mm=_rechteck(4990, 0, 9000, 4000),
              nutzungsklasse="WOHNUNG_PRIVAT")
    tueren = [_tuer("tw", "zi", "stgh", "wohnungseingang", xy=(5000.0, 2000.0))]
    a = Anker(id="stgh_tuer_tw", typ="TUER", xy_mm=(5000.0, 2000.0),
              raum_id="stgh")
    neu = wk.anker_aus_privat_ziehen([a], [stgh, zi], tueren)
    assert len(neu) == 1
    assert not Polygon(zi.polygon_mm).contains(Point(neu[0].xy_mm)), neu[0].xy_mm
    assert Polygon(stgh.polygon_mm).contains(Point(neu[0].xy_mm)), neu[0].xy_mm


def test_anker_ohne_ausweg_wird_gestrichen():
    """Lässt sich der Anker nicht auf die eigene Seite ziehen, wird er
    gestrichen — ein Anker in einer Wohnung ist die Verletzung, die Gate (6)
    zählt."""
    from notbeleuchtung.hauptengine.contracts.raum_modell import Anker

    vor = Raum(id="vor", raum_typ="VORRAUM",
               polygon_mm=_rechteck(0, 0, 9000, 4000),
               nutzungsklasse="WOHNUNG_PRIVAT")
    stgh = Raum(id="stgh", raum_typ="STIEGENHAUS", polygon_mm=[],
                nutzungsklasse="ALLGEMEIN_ERSCHLIESSUNG")
    tueren = [_tuer("tw", "vor", "stgh", "wohnungseingang", xy=(0.0, 2000.0))]
    a = Anker(id="x", typ="TUER", xy_mm=(4000.0, 2000.0), raum_id="stgh")
    assert wk.anker_aus_privat_ziehen([a], [vor, stgh], tueren) == []


# ── (k) Runde 5: Reihenfolge, Zyklus-Grund, unbestätigt private Flure ──────
def _t(tid, von, nach, detail=None, blattlos=False):
    t = _tuer(tid, von, nach, detail)
    t.ohne_tuerblatt = blattlos
    return t


def _r(rid, typ, notlicht=True):
    return Raum(id=rid, raum_typ=typ, ist_fluchtweg=notlicht,
                ist_communal=notlicht)


def _vollzustand(raeume, tueren, wohnungen):
    return (sorted((r.id, r.nutzungsklasse, r.ist_fluchtweg, r.ist_communal,
                    r.wohnung_id) for r in raeume),
            sorted((t.id, t.tuer_detail) for t in tueren),
            sorted(tuple(sorted(w.raum_ids)) for w in wohnungen))


def _alle_reihenfolgen(bau):
    """``{vollzustand: warnungen}`` über ALLE Raumreihenfolgen, je mit
    vorwärts und rückwärts laufender Türliste."""
    ergebnisse: dict = {}
    for perm in itertools.permutations(range(len(bau()[0]))):
        for rueckwaerts in (False, True):
            raeume, tueren = bau()
            raeume = [raeume[i] for i in perm]
            if rueckwaerts:
                tueren.reverse()
            warnungen: list[str] = []
            w = bilde_wohnungen(raeume, tueren, warnungen)
            z = _vollzustand(raeume, tueren, w)
            ergebnisse.setdefault(repr(z), (z, sorted(warnungen)))
    return list(ergebnisse.values())


def _u1():
    """Reviewer-Topologie U1 (Runde 4): stgh −WE− v0 (Kandidat) −zt− v1
    VORRAUM −zt− g1 GANG −zt− z. Die Flur-Verfeinerung hat für v1/g1 ZWEI
    Fixpunkte (beide privat, beide allgemein); welcher herauskam, entschied
    die Listenreihenfolge (Gauß-Seidel) — gemessen 360 von 720
    Reihenfolgen „privat, ankerbestätigt, Flags 00", die anderen 360
    „allgemein, Flags 11"."""
    return ([_r("v0", "VORRAUM"), _r("v1", "VORRAUM"), _r("g1", "GANG"),
             _r("z", "ZIMMER", False), _r("z0", "ZIMMER", False),
             _r("stgh", "STIEGENHAUS")],
            [_t("t_we", "stgh", "v0", "wohnungseingang"),
             _t("t_a", "v0", "v1", "zimmertuer"),
             _t("t_b", "v1", "g1", "zimmertuer"),
             _t("t_c", "g1", "z", "zimmertuer"),
             _t("t_d", "v0", "z0", "zimmertuer")])


def test_flur_verfeinerung_haengt_nicht_an_der_reihenfolge():
    """Befund B6 (Runde 4, Linse Regel): ``_verfeinere_gang_privat`` las
    Nachbarklassen, die sie im selben Durchlauf schon überschrieben hatte —
    damit hing sogar der Notlicht-Entzug an der Listenreihenfolge. Jetzt:
    über ALLE 720 Raumreihenfolgen × zwei Türreihenfolgen genau EIN
    Ergebnis.

    Die Flur-Verfeinerung hat für v1/g1 zwei Fixpunkte (beide privat, beide
    allgemein). Owner-Grundsatz 2026-09-22 (G2): der private Fixpunkt macht
    beide ausnahmslos ankerbestätigt privat (nur über ``t_we`` MIT Blatt
    erreichbar) und lässt keinen offen — der physische Beleg geht dem
    Tiebreak vor: beide privat, und weil Zimmer dahinter liegen (G4), Flags
    00. Runde 9 (L1, Board 4 als allgemeine Regel) lieferte „beide
    allgemein"; die Lesart hat der Owner verworfen."""
    ergebnisse = _alle_reihenfolgen(_u1)
    assert len(ergebnisse) == 1, (
        f"{len(ergebnisse)} verschiedene Ergebnisse je nach Reihenfolge")
    (raeume, _, _), warnungen = ergebnisse[0]
    zustand = {rid: rest for rid, *rest in raeume}
    for rid in ("v1", "g1"):
        klasse, flucht, communal, _ = zustand[rid]
        assert klasse == "WOHNUNG_PRIVAT", f"{rid}: {klasse}"
        assert (flucht, communal) == (False, False), f"{rid}: nicht entzogen"
        assert not [w for w in warnungen if w.startswith(f"unbestimmt: {rid} ")]


def _u2():
    """Reviewer-Topologie U2 (Muster Mollgasse 1OG ``raum_34``): Kandidat G
    am Stiegenhaus (blattlose Stiegenhaustür), dahinter drei Vorräume hinter
    Wohnungseingängen MIT Blatt. Bis Runde 6 ohne Fixpunkt: Schritt 2 zählte
    die Vorräume nur, wenn sie privat waren, und die Flur-Verfeinerung machte
    einen Vorraum neben einem allgemeinen Raum allgemein. Seit Board 6
    (Owner 2026-09-21) begrenzt der Wohnungseingang MIT Blatt die
    Flur-Verfeinerung — und Schritt 2 zählt transitiv (Board 5)."""
    return ([_r("G", "GANG"), _r("V1", "VORRAUM"), _r("V2", "VORRAUM"),
             _r("V3", "VORRAUM"), _r("Z1", "ZIMMER", False),
             _r("Z2", "ZIMMER", False), _r("Z3", "ZIMMER", False),
             _r("stgh", "STIEGENHAUS")],
            [_t("d10", "G", "stgh", "stiegenhaustuer", blattlos=True),
             _t("t14", "G", "V1", "wohnungseingang"),
             _t("t20", "G", "V2", "wohnungseingang"),
             _t("t21", "G", "V3", "wohnungseingang"),
             _t("z1", "V1", "Z1", "zimmertuer"),
             _t("z2", "V2", "Z2", "zimmertuer"),
             _t("z3", "V3", "Z3", "zimmertuer")])


@pytest.mark.parametrize("vorbelegung", [
    {}, dict.fromkeys(("G", "V1", "V2", "V3"), "ALLGEMEIN_ERSCHLIESSUNG"),
    dict.fromkeys(("G", "V1", "V2", "V3"), "WOHNUNG_PRIVAT"),
    {"G": "ALLGEMEIN_ERSCHLIESSUNG", "V1": "WOHNUNG_PRIVAT",
     "V2": "WOHNUNG_PRIVAT", "V3": "WOHNUNG_PRIVAT"}],
    ids=["ohne", "alle_A", "alle_P", "G_A_V_P"])
def test_e8_wohnungseingang_mit_blatt_begrenzt_die_flur_verfeinerung(vorbelegung):
    """E8 (Owner Board 6, 2026-09-21): „Ein Wohnungseingang mit Türblatt ist
    physischer Beleg und begrenzt die Flur-Verfeinerung." Die Vorräume hinter
    ``t14``/``t20``/``t21`` werden nicht mehr vom allgemeinen Gang G davor
    allgemein gemacht — sie sind PRIVAT, und weil die Ankerregel auf den
    ROHEN Rollen sie nur über einen Wohnungseingang MIT Blatt erreicht,
    bestätigt: Flags 00 (R3). G erschließt drei Wohnungen → ALLGEMEIN, behält
    alles. Bis Runde 6 waren alle vier unbestimmt (Zyklus ohne Fixpunkt).
    Gleich aus jeder Vorbelegung, idempotent."""
    raeume, tueren = _u2()
    for r in raeume:
        if r.id in vorbelegung:
            r.nutzungsklasse = vorbelegung[r.id]
    warnungen: list[str] = []
    bilde_wohnungen(raeume, tueren, warnungen)
    by_id = {r.id: r for r in raeume}
    assert by_id["G"].nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"
    assert (by_id["G"].ist_fluchtweg, by_id["G"].ist_communal) == (True, True)
    bestaetigt = wk.bestaetigt_privat(raeume, tueren)
    for rid in ("V1", "V2", "V3"):
        r = by_id[rid]
        assert r.nutzungsklasse == "WOHNUNG_PRIVAT", f"{rid}: {r.nutzungsklasse}"
        assert rid in bestaetigt, rid
        assert (r.ist_fluchtweg, r.ist_communal) == (False, False), rid
    assert not [w for w in warnungen if w.startswith("unbestimmt:")], warnungen
    eins = _vollzustand(raeume, tueren, [])
    bilde_wohnungen(raeume, tueren)
    assert _vollzustand(raeume, tueren, []) == eins, "nicht idempotent"


def test_e8_blattlose_oeffnung_begrenzt_nicht():
    """Gegenprobe zu E8: dieselbe Topologie mit blattlosen Wohnungseingängen.
    Eine blattlose Öffnung schließt keine Wohnung ab (E1) — die Vorräume
    liegen am allgemeinen Gang und werden allgemein, nichts wird entzogen."""
    raeume, tueren = _u2()
    for t in tueren:
        if t.id in ("t14", "t20", "t21"):
            t.ohne_tuerblatt = True
    bilde_wohnungen(raeume, tueren)
    by_id = {r.id: r for r in raeume}
    for rid in ("V1", "V2", "V3"):
        assert by_id[rid].nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG", rid
        assert (by_id[rid].ist_fluchtweg, by_id[rid].ist_communal) == (True, True)
    assert not wk.bestaetigt_privat(raeume, tueren)


def _loch_paar():
    """Rennweg OG2 ``raum_9`` GANG / ``raum_10`` VORRAUM im Kleinen: beide vom
    Stiegenhaus über KEINE Tür erreichbar (Tür- oder Raumerkennungsloch),
    beide nur an Zimmern, einander über eine blattlose Öffnung benachbart.
    Die Flur-Verfeinerung entscheidet jeden über den anderen."""
    return ([_r("g", "GANG"), _r("v", "VORRAUM"), _r("z1", "ZIMMER", False),
             _r("z2", "ZIMMER", False), _r("z3", "ZIMMER", False),
             _r("stgh", "STIEGENHAUS")],
            [_t("d8", "g", "v", "wohnungseingang", blattlos=True),
             _t("d5", "g", "z1", "wohnungseingang", blattlos=True),
             _t("t2", "v", "z2", "zimmertuer"),
             _t("t5", "v", "z3", "zimmertuer")])


def test_e5_loch_paar_folgt_rohen_tueren():
    """Owner-Grundsatz 2026-09-22 (G1.2, „Wohnung folgt rohen Türen"): v ist
    über die rohen Zimmertüren ``t2``/``t5`` an z2/z3 gebunden → gehört zu
    dieser Wohnung, unbestimmt, Flags 11; g ist nur über rohe
    Wohnungseingänge (``d8``/``d5``) angebunden → Erschließung, allgemein.
    Runde 8/9 (E5 Satz 2, aufgehoben) machten beide allgemein und zerlegten
    die Wohnung in drei Einraum-Wohnungen. Über alle Reihenfolgen EIN
    Ergebnis, jede Wohnung hat einen Eingang. K4 (Owner 2026-09-30): v ist
    Mitglied seiner Wohnung → Klasse privat statt offen, Flags bleiben 11
    (Ankerregel „über keine Tür erreichbar" bestätigt nicht)."""
    ergebnisse = _alle_reihenfolgen(_loch_paar)
    assert len(ergebnisse) == 1, (
        f"{len(ergebnisse)} verschiedene Ergebnisse je nach Reihenfolge")
    (raeume, _, gruppen), warnungen = ergebnisse[0]
    zustand = {rid: rest for rid, *rest in raeume}
    assert tuple(zustand["g"]) == ("ALLGEMEIN_ERSCHLIESSUNG", True, True, None)
    klasse, flucht, communal, whg = zustand["v"]
    assert (klasse, flucht, communal) == ("WOHNUNG_PRIVAT", True, True)
    assert whg == zustand["z2"][3] == zustand["z3"][3] is not None
    assert [w for w in warnungen if w.startswith("k4: v — privat")
            and "vorher unbestimmt" in w], warnungen
    assert gruppen == [("v", "z2", "z3"), ("z1",)], gruppen
    raeume, tueren = _loch_paar()
    for w in bilde_wohnungen(raeume, tueren):
        assert w.eingangs_tuer_ids, f"{w.id} {w.raum_ids} ohne Wohnungseingang"


def _muth_paar():
    """Muthgasse E2 ``raum_51`` VORRAUM / ``raum_94`` GANG im Kleinen: beide vom
    Stiegenhaus über keine Tür erreichbar; der Gang hat Wohnungseingänge MIT
    Blatt zu einem Zimmer, einer Küche und dem Vorraum, der Vorraum blattlose
    Öffnungen zur Küche und zum Bad. Bis Runde 6 wurden beide als Loch in die
    Wohnung gezählt: EINE Wohnung aus allen fünf Räumen, OHNE Eingang
    (Muthgasse ``top_11``, 14 Räume)."""
    return ([_r("G", "GANG"), _r("V", "VORRAUM"), _r("z1", "ZIMMER", False),
             _r("k", "KÜCHE", False), _r("b", "BAD", False),
             _r("stgh", "STIEGENHAUS")],
            [_t("t3", "G", "z1", "wohnungseingang"),
             _t("t99", "G", "k", "wohnungseingang"),
             _t("t7", "G", "V", "wohnungseingang"),
             _t("d50", "V", "k", "zimmertuer", blattlos=True),
             _t("d52", "V", "b", "zimmertuer", blattlos=True)])


def test_e5_keine_wohnung_ohne_eingang_durch_offen_gelassene_raeume():
    """Die harte Abnahme im Kleinen (Muthgasse ``top_11`` bleibt weg), jetzt
    nach rohen Türen (Owner 2026-09-22, G1.2): G ist nur über rohe
    Wohnungseingänge angebunden → Erschließung, allgemein; V hängt über die
    rohen Zimmertüren ``d50``/``d52`` an Küche und Bad → gehört zu ihrer
    Wohnung, unbestimmt. Beide behalten Notlicht, jede Wohnung hat ihren
    Eingang (``t7``/``t99`` bzw. ``t3``). Runde 9 machte V allgemein
    (E5 Satz 2, aufgehoben). K4 (Owner 2026-09-30): V ist Mitglied seiner
    Wohnung → privat statt offen, Notlicht bleibt."""
    raeume, tueren = _muth_paar()
    wohnungen = bilde_wohnungen(raeume, tueren)
    by_id = {r.id: r for r in raeume}
    assert by_id["G"].nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"
    assert by_id["V"].nutzungsklasse == "WOHNUNG_PRIVAT"
    for rid in ("G", "V"):
        assert (by_id[rid].ist_fluchtweg, by_id[rid].ist_communal) == (True, True)
    assert sorted((w.raum_ids, sorted(w.eingangs_tuer_ids)) for w in wohnungen) == [
        (["V", "b", "k"], ["t7", "t99"]), (["z1"], ["t3"])]


def _o3():
    """Reviewer-Topologie O3 (Runde 5): Kandidat G an der Stiegenhaustür,
    zwei Vorräume V1/V2 hinter Wohnungseingängen MIT Blatt, ein Zimmer Z0
    direkt am Gang, dazu ein Vorraum Y zwischen V1 und V2. Bis Runde 6 pendelte
    die Kette vom statischen Default aus; seit E8 begrenzen ``w1``/``w2`` die
    Flur-Verfeinerung — V1/Y/V2 entscheiden sich damit nur noch gegenseitig
    und haben zwei Fixpunkte (alle privat, alle allgemein)."""
    return ([_r("G", "GANG"), _r("V1", "VORRAUM"), _r("V2", "VORRAUM"),
             _r("Y", "VORRAUM"), _r("Z0", "ZIMMER", False),
             _r("Z1", "ZIMMER", False), _r("Z2", "ZIMMER", False),
             _r("ZY", "ZIMMER", False), _r("stgh", "STIEGENHAUS")],
            [_t("ts", "G", "stgh", "stiegenhaustuer"),
             _t("w1", "G", "V1", "wohnungseingang"),
             _t("w2", "G", "V2", "wohnungseingang"),
             _t("z0", "G", "Z0", "wohnungseingang"),
             _t("z1", "V1", "Z1", "zimmertuer"),
             _t("z2", "V2", "Z2", "zimmertuer"),
             _t("y1", "V1", "Y", "zimmertuer"),
             _t("y2", "V2", "Y", "zimmertuer"),
             _t("zy", "Y", "ZY", "zimmertuer")])


def test_e8_o3_zwei_fixpunkte_hinter_blatt_der_belegte_gilt():
    """O3 unter E8/E6: ``w1``/``w2`` (MIT Blatt, Gang davor vom Stiegenhaus
    ohne Wohnungseingang erreichbar) begrenzen die Flur-Verfeinerung; V1/Y/V2
    haben dann zwei Fixpunkte — alle privat und alle allgemein. Der private
    macht alle drei ankerbestätigt privat und lässt keinen offen: der
    physische Beleg geht dem Tiebreak vor (Owner 2026-09-22, G2) — privat,
    Flags 00 (Zimmer dahinter, G4). Die Wohnung folgt rohen Türen:
    {V1, V2, Y, Z1, Z2, ZY} und {Z0}. Runde 9 (L1) lieferte „alle allgemein"
    und vier Einraum-Wohnungen. G erschließt mehrere Wohnungen → allgemein.
    Kein Zyklus, über alle Stichproben-Reihenfolgen EIN Ergebnis."""
    ergebnisse = _stichprobe_reihenfolgen(_o3)
    assert len(ergebnisse) == 1, len(ergebnisse)
    (raeume, _, gruppen), warnungen = ergebnisse[0]
    zustand = {rid: rest for rid, *rest in raeume}
    assert zustand["G"][0] == "ALLGEMEIN_ERSCHLIESSUNG"
    for rid in ("V1", "V2", "Y"):
        assert tuple(zustand[rid][:3]) == ("WOHNUNG_PRIVAT", False, False), (
            rid, zustand[rid])
    assert gruppen == [("V1", "V2", "Y", "Z1", "Z2", "ZY"), ("Z0",)], gruppen
    assert not warnungen, warnungen


def _flur_mit_stiegenhaustuer_und_ausgang():
    """Flur ``vor`` mit Stiegenhaustür und EINEM Zimmer, das Stiegenhaus hat
    den Hauseingang. Schritt 2: eine Wohnung → privat; die Ankerregel
    erreicht ``vor`` ohne Wohnungseingang → NICHT bestätigt."""
    raeume = [Raum(id="zi", raum_typ="ZIMMER", polygon_mm=_rechteck(0, 0, 5000, 4000)),
              Raum(id="vor", raum_typ="VORRAUM", polygon_mm=_rechteck(5000, 0, 10000, 4000),
                   ist_fluchtweg=True, ist_communal=True),
              Raum(id="stgh", raum_typ="STIEGENHAUS",
                   polygon_mm=_rechteck(10000, 0, 15000, 4000),
                   ist_fluchtweg=True, ist_communal=True)]
    tueren = [_tuer("t1", "vor", "zi", "wohnungseingang", xy=(5000.0, 2000.0)),
              _tuer("t2", "vor", "stgh", "stiegenhaustuer", xy=(10000.0, 2000.0)),
              _tuer("tx", "stgh", "AUSSEN", "hauseingang", xy=(15000.0, 2000.0))]
    return raeume, tueren


def test_unbestaetigt_privater_flur_behaelt_eingang_und_weg():
    """Reviewer-Befund Runde 4 (Linse Sicherheit, blockierend 1), Option W:
    ein Kandidat, den nur Schritt 2 privat macht, behält sein Notlicht — und
    wer Notlicht behält, behält seine Zirkulation. Auf dem Stand der Vorrunde
    machte die Rollenkorrektur ``t1`` zur Zimmertür, der Fluchtweg-Start des
    Zimmers fiel weg (gemessen Rennweg UG ``seg_graph_tuer_3``, DG1
    ``seg_graph_durchgang_3``). Jetzt zählt der unbestätigt private Flur für
    Rollen und Wohnungsgrenze als Erschließung; seine Klasse bleibt."""
    raeume, tueren = _flur_mit_stiegenhaustuer_und_ausgang()
    bilde_wohnungen(raeume, tueren)
    by_id = {r.id: r for r in raeume}
    vor = by_id["vor"]
    assert vor.nutzungsklasse == "WOHNUNG_PRIVAT"
    assert vor.id not in wk.bestaetigt_privat(raeume, tueren), "Vorbedingung"
    assert (vor.ist_fluchtweg, vor.ist_communal) == (True, True)
    assert next(t for t in tueren if t.id == "t1").tuer_detail == "wohnungseingang"
    # E7: die Rolle, mit der der Fluchtweg rechnet, ist die korrigierte.
    from notbeleuchtung.raumerkennung.wohnungsklasse import korrigierte_rollen
    assert korrigierte_rollen(raeume, tueren)["t1"] == "wohnungseingang"
    assert vor.wohnung_id is None
    assert by_id["zi"].wohnung_id is not None
    ausgaenge = [Ausgang(id="exit_tx", xy_mm=(15000.0, 2000.0), typ="final_exit")]
    segmente = fluchtwege(raeume, tueren, ausgaenge, [], "EG")
    assert [s for s in segmente if s.quelle == "GRAPH" and s.start_raum == "zi"], (
        "kein Fluchtweg-Segment aus dem Zimmer")


# ── (l) Runde 7: Owner-Entscheide 2026-09-21 nachmittags (Board 4-7) ────────
#: Topologien, auf denen die Rollenkorrektur bis Runde 6 wirklich eine Rolle
#: umschrieb (Loch-Paar: ``d8``/``d5`` → zimmertuer; Rückkopplung: ``t_ar`` →
#: wohnungseingang) — und die Muster aus den Owner-Boards.
_R7_BAUTEN = [_rueckkopplung, _plan_zwei_wohnungen, _loch_paar, _u1, _u2, _o3,
              _muth_paar, _flur_mit_stiegenhaustuer_und_ausgang]


def _s7c_wanderung(aussen_typ: str, aussen_detail: str | None, dreh: bool):
    """Slice S7c (Abschnitt (r)), hier definiert, weil die E7-Zusicherungen
    dieses Abschnitts sie mitparametrisieren. Owner-Regel S7c: privater
    VORRAUM ``vor`` mit INNERER Tür ``t_in`` zum ZIMMER ``zi`` und ÄUSSERER
    Tür ``t_out`` in die Erschließung ``aussen`` (STIEGENHAUS oder allgemeiner
    GANG).

    Die Klassen sind hier GESETZT — ``korrigierte_rollen`` leitet nach Contract
    aus der FERTIGEN Klassifikation ab (Einbahn, § 6g.6), der Test prüft also
    genau seine Eingabe. ``vor`` ist bestätigt privat: die Ankerregel erreicht
    ihn vom Stiegenhaus NUR über ``t_we`` (Wohnungseingang MIT Türblatt), das
    ZIMMER belegt die Wohnung (G4), kein Riegel greift.

    ``dreh`` dreht beide Türseiten — die Regel darf nicht an ``von_raum`` vs.
    ``nach_raum`` hängen.
    """
    raeume = [
        Raum(id="zi", raum_typ="ZIMMER", nutzungsklasse=wk.PRIVAT,
             polygon_mm=_rechteck(0, 0, 5000, 4000)),
        Raum(id="vor", raum_typ="VORRAUM", nutzungsklasse=wk.PRIVAT,
             polygon_mm=_rechteck(5000, 0, 9000, 4000)),
        Raum(id="stgh", raum_typ="STIEGENHAUS", nutzungsklasse=wk.ALLGEMEIN,
             polygon_mm=_rechteck(9000, 0, 13000, 4000),
             ist_fluchtweg=True, ist_communal=True),
        Raum(id="aussen", raum_typ=aussen_typ, nutzungsklasse=wk.ALLGEMEIN,
             polygon_mm=_rechteck(5000, 4000, 9000, 8000),
             ist_fluchtweg=True, ist_communal=True),
    ]
    paare = {"t_in": ("vor", "zi"), "t_we": ("stgh", "vor"),
             "t_out": ("vor", "aussen")}
    if dreh:
        paare = {k: (b, a) for k, (a, b) in paare.items()}
    tueren = [_tuer("t_in", *paare["t_in"], "zimmertuer", xy=(5000.0, 2000.0)),
              _tuer("t_we", *paare["t_we"], "wohnungseingang", xy=(9000.0, 2000.0)),
              _tuer("t_out", *paare["t_out"], aussen_detail, xy=(7000.0, 4000.0))]
    return raeume, tueren


def _s7c_flur_und_gang():
    """Dieselbe S7c-Topologie ohne vorgesetzte Klassen und ohne Rolle an
    ``t_out`` — für die E7-Zusicherungen, die ``bilde_wohnungen`` selbst
    fahren. ``bilde_wohnungen`` macht hier den äußeren GANG selbst privat: die
    rollenlose Tür verbindet ihn nach (b) mit ``vor``, die Ankerregel bestätigt
    ihn über ``t_we`` (gemessen S7c Runde 2)."""
    raeume, tueren = _s7c_wanderung("GANG", None, False)
    for r in raeume:
        r.nutzungsklasse = None
    return raeume, tueren


@pytest.mark.parametrize("bau", [*_R7_BAUTEN, _s7c_flur_und_gang],
                         ids=lambda f: f.__name__.lstrip("_"))
def test_e7_bilde_wohnungen_aendert_keine_tuerrolle(bau):
    """E7 (Owner Board 7): „Die Ankerregel liest nur rohe Türrollen, nie
    Raumklassen und nie korrigierte Rollen." Die korrigierten Rollen werden
    NICHT in ``tuer_detail`` geschrieben (Entscheidung (i), Bericht Runde 7):
    das Modell trägt die rohen Rollen, und ein zweiter Lauf liest dieselbe
    Eingabe wie der erste."""
    raeume, tueren = bau()
    roh = {t.id: t.tuer_detail for t in tueren}
    bilde_wohnungen(raeume, tueren)
    assert {t.id: t.tuer_detail for t in tueren} == roh


@pytest.mark.parametrize("bau", _R7_BAUTEN, ids=lambda f: f.__name__.lstrip("_"))
def test_e7_ankerregel_liest_nur_rohe_rollen(bau, monkeypatch):
    """Jeder Aufruf der Ankerregel während ``bilde_wohnungen`` sieht genau die
    Rollen, mit denen die Türen hereinkamen — Schritt 1, Riegel und die
    Bestätigung für R3/R4. Bis Runde 6 las sie ab der zweiten Runde die
    korrigierten Rollen der Vorrunde."""
    from notbeleuchtung.raumerkennung import wohnungen as W

    gesehen: list[dict] = []
    echt = wk.ankerurteil

    def spion(raeume, tueren):
        gesehen.append({t.id: t.tuer_detail for t in tueren})
        return echt(raeume, tueren)

    monkeypatch.setattr(wk, "ankerurteil", spion)
    monkeypatch.setattr(W, "ankerurteil", spion, raising=False)
    raeume, tueren = bau()
    roh = {t.id: t.tuer_detail for t in tueren}
    bilde_wohnungen(raeume, tueren)
    assert gesehen, "die Ankerregel lief nicht"
    abweichend = [g for g in gesehen if g != roh]
    assert not abweichend, f"Ankerregel las korrigierte Rollen: {abweichend[0]}"


@pytest.mark.parametrize("bau", [*_R7_BAUTEN, _s7c_flur_und_gang],
                         ids=lambda f: f.__name__.lstrip("_"))
def test_e7_klassifikation_haengt_nicht_an_korrigierten_rollen(bau, monkeypatch):
    """Einbahn: rohe Rolle → Klasse → korrigierte Rolle → Fluchtweg, nie
    zurück. Werden die korrigierten Rollen verfälscht (hier: jede Tür
    „wohnungseingang"), bleiben Klassen, Flags und ``wohnung_id`` gleich —
    die Klassifikation liest sie nicht."""
    from notbeleuchtung.raumerkennung import wohnungen as W

    def stand(raeume):
        return {r.id: (r.nutzungsklasse, r.ist_fluchtweg, r.ist_communal,
                       r.wohnung_id) for r in raeume}

    raeume, tueren = bau()
    bilde_wohnungen(raeume, tueren)
    soll = stand(raeume)
    falsch = lambda rr, tt: {t.id: "wohnungseingang" for t in tt}
    monkeypatch.setattr(wk, "korrigierte_rollen", falsch)
    # Seit Runde 8 importiert ``wohnungen`` die Funktion gar nicht mehr.
    monkeypatch.setattr(W, "korrigierte_rollen", falsch, raising=False)
    raeume, tueren = bau()
    bilde_wohnungen(raeume, tueren)
    assert stand(raeume) == soll


def _rollen_oszillator(tz_detail, tz_blattlos=False):
    """Reviewer-Topologie Runde 6 (Linse Regel, blockierend): VORRAUM X mit
    ``tx`` Wohnungseingang MIT Blatt zum STIEGENHAUS S, ZIMMER Z mit ``tz`` zu
    S, Tür ``d`` X–Z Zimmertür mit Blatt. Bis Runde 6 pendelten Türrolle von
    ``d`` und Ankerbestätigung von X (Klasse konstant), und unter
    ``DECKEL = 10`` wurde X lautlos das Notlicht entzogen."""
    def bau():
        return ([_r("X", "VORRAUM"), _r("Z", "ZIMMER", False),
                 _r("S", "STIEGENHAUS")],
                [_t("tx", "X", "S", "wohnungseingang"),
                 _t("tz", "Z", "S", tz_detail, tz_blattlos),
                 _t("d", "X", "Z", "zimmertuer")])
    bau.__name__ = f"_rollen_oszillator_{tz_detail}{'_blattlos' if tz_blattlos else ''}"
    return bau


_ROLLEN_OSZ = [_rollen_oszillator(None), _rollen_oszillator("stiegenhaustuer"),
               _rollen_oszillator("wohnungseingang", True)]


@pytest.mark.parametrize("bau", _ROLLEN_OSZ, ids=lambda f: f.__name__.lstrip("_"))
def test_e7_rollen_oszillator_ist_strukturell_weg(bau, monkeypatch):
    """E7.6: deterministisch, zweimal gleich, keine Notlicht-Entnahme ohne
    Ankerbestätigung auf ROHEN Rollen, und dasselbe Ergebnis unter Deckel 9,
    10 und 11. X erreicht die Ankerregel roh über Z (``tz``, ``d``) ohne bzw.
    nur durch eine blattlose Öffnung — also nicht bestätigt, Flags 11."""
    from notbeleuchtung.raumerkennung import wohnungen as W

    ergebnisse = set()
    for deckel in (9, 10, 11):
        monkeypatch.setattr(W, "DECKEL", deckel)
        raeume, tueren = bau()
        warnungen: list[str] = []
        w = bilde_wohnungen(raeume, tueren, warnungen)
        eins = _vollzustand(raeume, tueren, w)
        w2 = bilde_wohnungen(raeume, tueren)
        assert _vollzustand(raeume, tueren, w2) == eins, f"DECKEL {deckel}: nicht idempotent"
        x = next(r for r in raeume if r.id == "X")
        assert "X" not in wk.bestaetigt_privat(raeume, tueren), deckel
        assert (x.ist_fluchtweg, x.ist_communal) == (True, True), deckel
        ergebnisse.add(repr((eins, sorted(warnungen))))
    assert len(ergebnisse) == 1, ergebnisse


def test_e6_null_wohnungen_ist_allgemein():
    """E6 (Owner Board 5): „Ein Raum, der null Wohnungen erschließt (Podest,
    Foyer), kann nicht privat sein." Podest zwischen zwei Stiegenhaus-Teilen
    (Muster Rennweg DG2 ``raum_6``, Mollgasse EG ``raum_7``): bis Runde 6
    „sonst PRIVAT"."""
    raeume = [_r("pod", "VORRAUM"), _r("s1", "STIEGENHAUS"), _r("s2", "STIEGENHAUS")]
    tueren = [_t("d3", "pod", "s1", "wohnungseingang", blattlos=True),
              _t("d4", "pod", "s2", "wohnungseingang", blattlos=True)]
    bilde_wohnungen(raeume, tueren)
    pod = raeume[0]
    assert pod.nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"
    assert (pod.ist_fluchtweg, pod.ist_communal) == (True, True)


def _kellergang(ziel_typ: str):
    """Rennweg UG ``raum_12`` im Kleinen: Kandidat g am Stiegenhaus, EIN WC
    dahinter, und über den allgemeinen Gang g2 ein Kinderwagenraum bzw. eine
    Tür ins Freie."""
    raeume = [_r("g", "GANG"), _r("wc", "WC", False), _r("g2", "GANG"),
              _r("stgh", "STIEGENHAUS")]
    tueren = [_t("t7", "g", "stgh", "stiegenhaustuer"),
              _t("t3", "g", "wc", "wohnungseingang"),
              _t("t5", "g", "g2")]
    if ziel_typ == "AUSSEN":
        tueren.append(_t("tx", "g2", "AUSSEN", "hauseingang"))
    else:
        raeume.append(_r("ziel", ziel_typ, False))
        tueren.append(_t("t2", "g2", "ziel"))
    return raeume, tueren


@pytest.mark.parametrize("ziel_typ", ["KINDERWAGENRAUM", "AUSSEN"])
def test_e6_erschliesst_transitiv_ueber_allgemeinen_zwischenraum(ziel_typ):
    """E6: „Erschließt" zählt transitiv über allgemeine Räume. g erschließt
    direkt nur das WC (eine Wohnung) — über den allgemeinen Gang g2 aber den
    Kinderwagenraum bzw. einen Ausgang → ALLGEMEIN. Bis Runde 6 (direkt)
    PRIVAT; das war der Kellergang, mit dem der Owner E2 begründet hat."""
    raeume, tueren = _kellergang(ziel_typ)
    bilde_wohnungen(raeume, tueren)
    g = raeume[0]
    assert g.nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG", g.nutzungsklasse
    assert (g.ist_fluchtweg, g.ist_communal) == (True, True)


def test_e6_stiegenhaus_ist_ursprung_nicht_durchgang():
    """Planer-Auslegung zu E6: das STIEGENHAUS ist Ursprung, nicht Durchgang.
    Was nur über das Stiegenhaus erreichbar ist (hier ein zweites Zimmer und
    ein Keller), erschließt das Stiegenhaus, nicht ``vor`` — ``vor``
    erschließt genau eine Wohnung und nichts Allgemeines → PRIVAT."""
    raeume = [_r("vor", "VORRAUM"), _r("zi", "ZIMMER", False),
              _r("zi2", "ZIMMER", False), _r("kel", "KELLER", False),
              _r("stgh", "STIEGENHAUS")]
    tueren = [_t("t1", "vor", "zi", "wohnungseingang"),
              _t("t2", "vor", "stgh", "stiegenhaustuer"),
              _t("t3", "stgh", "zi2", "wohnungseingang"),
              _t("t4", "stgh", "kel")]
    bilde_wohnungen(raeume, tueren)
    assert raeume[0].nutzungsklasse == "WOHNUNG_PRIVAT"


def test_e6_erreichte_wohnung_beendet_den_weg():
    """E6: „Eine erreichte Wohnung zählt und beendet den Weg dort (nicht in
    die Wohnung hinein)." Der Keller hinter dem Zimmer zählt nicht."""
    raeume = [_r("g", "GANG"), _r("zi", "ZIMMER", False),
              _r("kel", "KELLER", False), _r("stgh", "STIEGENHAUS")]
    tueren = [_t("t1", "g", "zi", "wohnungseingang"),
              _t("t2", "g", "stgh", "stiegenhaustuer"),
              _t("t3", "zi", "kel")]
    bilde_wohnungen(raeume, tueren)
    assert raeume[0].nutzungsklasse == "WOHNUNG_PRIVAT"


def _nicht_konvergent():
    """Kleinster per Zufallssuche gefundener Fall (Runde 7), in dem die
    Iteration auch nach dem Neustart bei ALLGEMEIN (E5) weiter pendelt:
    Kandidat G hinter einer blattlosen Öffnung am Stiegenhaus, ein Zimmer z
    und ein Vorraum V hinter einem Wohnungseingang MIT Blatt."""
    return ([_r("stgh", "STIEGENHAUS"), _r("V", "VORRAUM"), _r("G", "GANG"),
             _r("z", "ZIMMER", False)],
            [_t("t0", "z", "G", "zimmertuer"),
             _t("t1", "stgh", "G", "wohnungseingang", blattlos=True),
             _t("t2", "V", "G", "wohnungseingang")])


def test_nicht_konvergenz_wird_unbestimmt_mit_grund(monkeypatch):
    """Was die Iteration intern weiter braucht (E7.5): Nicht-Konvergenz →
    unbestimmt mit Grund, Notlicht bleibt — gleich unter Deckel 9/10/11,
    über alle Reihenfolgen, idempotent. Der Grund behauptet nicht, die Regel
    habe keinen Fixpunkt. K4 (Owner 2026-09-30) danach: V ist Mitglied
    seiner (Einraum-)Wohnung, die hat aber keinen Aufenthaltsraum →
    Aufenthaltsraum-Sperre, V bleibt unbestimmt („G4: kein
    Aufenthaltsraum"); G liegt in keiner Wohnung und ist nur blattlos
    getrennt → bleibt unbestimmt mit K4-Grund."""
    from notbeleuchtung.raumerkennung import wohnungen as W

    ergebnisse = set()
    for deckel in (9, 10, 11):
        monkeypatch.setattr(W, "DECKEL", deckel)
        raeume, tueren = _nicht_konvergent()
        warnungen: list[str] = []
        w = bilde_wohnungen(raeume, tueren, warnungen)
        eins = _vollzustand(raeume, tueren, w)
        w = bilde_wohnungen(raeume, tueren)
        assert _vollzustand(raeume, tueren, w) == eins, deckel
        assert [x for x in warnungen
                if x.startswith("k4: V — offen: G4: kein Aufenthaltsraum")], warnungen
        for rid, klasse, zeile in (("G", None, "unbestimmt: G "),
                                   ("V", None, "unbestimmt: V ")):
            r = next(x for x in raeume if x.id == rid)
            assert r.nutzungsklasse == klasse, (deckel, rid, r.nutzungsklasse)
            assert (r.ist_fluchtweg, r.ist_communal) == (True, True), rid
            grund = next(x for x in warnungen if x.startswith(zeile))
            assert "Schritt 3" in grund and "keinen Fixpunkt" in grund, grund
            assert "kein Fixpunkt" not in grund and "ohne Fixpunkt" not in grund
        ergebnisse.add(repr((eins, sorted(warnungen))))
    assert len(ergebnisse) == 1, ergebnisse
    monkeypatch.undo()
    assert len(_stichprobe_reihenfolgen(_nicht_konvergent)) == 1


@pytest.mark.parametrize("bau", _R7_BAUTEN + _ROLLEN_OSZ + [_nicht_konvergent],
                         ids=lambda f: f.__name__.lstrip("_"))
def test_r7_idempotent_und_reihenfolge_invariant(bau):
    """(f) Reihenfolge-Invarianz und Idempotenz bleiben — auf allen
    Runde-7-Mustern: ausgeliefert → zweiter Lauf gleich, und über alle
    Raumreihenfolgen × zwei Türreihenfolgen genau EIN Ergebnis."""
    raeume, tueren = bau()
    w = bilde_wohnungen(raeume, tueren)
    eins = _vollzustand(raeume, tueren, w)
    w = bilde_wohnungen(raeume, tueren)
    assert _vollzustand(raeume, tueren, w) == eins
    assert len(_stichprobe_reihenfolgen(bau)) == 1


def _stichprobe_reihenfolgen(bau, n: int = 24):
    """Wie ``_alle_reihenfolgen``, aber ``n`` gesetzte Zufallsreihenfolgen
    (Räume UND Türen) plus vorwärts/rückwärts — für Bauten mit mehr als sechs
    Räumen, wo alle Permutationen zu viele wären."""
    import random

    ergebnisse: dict = {}
    for seed in range(-2, n):
        raeume, tueren = bau()
        if seed == -1:
            raeume.reverse()
            tueren.reverse()
        elif seed >= 0:
            random.Random(seed).shuffle(raeume)
            random.Random(seed + 1000).shuffle(tueren)
        warnungen: list[str] = []
        w = bilde_wohnungen(raeume, tueren, warnungen)
        z = _vollzustand(raeume, tueren, w)
        ergebnisse.setdefault(repr(z), (z, sorted(warnungen)))
    return list(ergebnisse.values())


# ── (m) Runde 8: Befunde der Vorrunde (E5 beide Sätze, Einbahn, Loch) ───────
def _topologie_l(typ1: str, typ2: str):
    """Reviewer-Topologie L (Runde 7, Linse Regel, blockierend 2): Kandidat G
    am Stiegenhaus mit einem Zimmer Z2; dahinter V1 hinter einem
    Wohnungseingang MIT Blatt, dann V2 und ein Zimmer Z. In Runde 7 gab
    dieselbe Topologie je nach GANG/VORRAUM-Etikett von V1/V2 „privat,
    Notlicht weg" (VORRAUM/VORRAUM) oder „allgemein, Notlicht bleibt"
    (sonst): die Iteration startete beim statischen Default des Etiketts."""
    def bau():
        return ([_r("S", "STIEGENHAUS"), _r("G", "GANG"), _r("V1", typ1),
                 _r("V2", typ2), _r("Z", "ZIMMER", False),
                 _r("Z2", "ZIMMER", False)],
                [_t("ts", "G", "S", "stiegenhaustuer"),
                 _t("w2", "G", "Z2", "wohnungseingang"),
                 _t("w1", "G", "V1", "wohnungseingang"),
                 _t("d", "V1", "V2", "zimmertuer"),
                 _t("z", "V2", "Z", "zimmertuer")])
    bau.__name__ = f"_topologie_l_{typ1[0]}{typ2[0]}"
    return bau


_ETIKETTEN = [("VORRAUM", "VORRAUM"), ("VORRAUM", "GANG"),
              ("GANG", "VORRAUM"), ("GANG", "GANG")]


def _ergebnis(bau):
    raeume, tueren = bau()
    warnungen: list[str] = []
    w = bilde_wohnungen(raeume, tueren, warnungen)
    return repr((_vollzustand(raeume, tueren, w), sorted(warnungen)))


def test_e5_start_haengt_nicht_am_etikett():
    """E5 Satz 1 als REGEL, nicht als Etikett (Runde 7, Linse Regel,
    blockierend 2): ob die Iteration pendelte oder in einem Fixpunkt landete,
    entschied das Etikett. V1/V2 haben zwei Fixpunkte (beide privat und
    ankerbestätigt — nur über ``w1`` MIT Blatt erreichbar —, beide
    allgemein). Der private ist voll ankerbestätigt und lässt keinen offen:
    Beleg vor Tiebreak (Owner 2026-09-22, G2) — alle vier Etikettierungen
    liefern „beide privat", Flags 00 (Zimmer Z in derselben Wohnung, G4).
    Runde 9 (L1) lieferte „beide allgemein" — verworfen. G erschließt in
    jedem Fall zwei Wohnungen → allgemein."""
    ergebnisse = {f"{a}/{b}": _ergebnis(_topologie_l(a, b)) for a, b in _ETIKETTEN}
    assert len(set(ergebnisse.values())) == 1, ergebnisse
    raeume, tueren = _topologie_l("GANG", "GANG")()
    bilde_wohnungen(raeume, tueren)
    by_id = {r.id: r for r in raeume}
    assert by_id["G"].nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"
    assert (by_id["G"].ist_fluchtweg, by_id["G"].ist_communal) == (True, True)
    assert wk.bestaetigt_privat(raeume, tueren) == {"V1", "V2"}
    for rid in ("V1", "V2"):
        assert by_id[rid].nutzungsklasse == "WOHNUNG_PRIVAT", rid
        assert (by_id[rid].ist_fluchtweg, by_id[rid].ist_communal) == (False, False)


def _loch_paar_etikett(typ_g: str, typ_v: str):
    """Das Loch-Paar mit wählbarem Etikett — Rennweg OG2 ``raum_4``/``raum_5``
    sind VORRAUM/VORRAUM, ``raum_9``/``raum_10`` GANG/VORRAUM."""
    def bau():
        raeume, tueren = _loch_paar()
        raeume[0].raum_typ, raeume[1].raum_typ = typ_g, typ_v
        return raeume, tueren
    bau.__name__ = f"_loch_paar_{typ_g[0]}{typ_v[0]}"
    return bau


@pytest.mark.parametrize("typ_g,typ_v", _ETIKETTEN,
                         ids=[f"{a[0]}{b[0]}" for a, b in _ETIKETTEN])
def test_e5_loch_paar_haengt_nicht_am_etikett(typ_g, typ_v):
    """Gemessen an Rennweg OG2 ``raum_4``/``raum_5`` (VORRAUM/VORRAUM) und
    ``raum_9``/``raum_10`` (GANG/VORRAUM): die Wohnung folgt rohen Türen,
    nicht dem Etikett (Owner 2026-09-22, G1.2). Für jedes Etikett: v hängt
    über rohe Zimmertüren an z2/z3 → in deren Wohnung, unbestimmt; g hängt
    nur über rohe Wohnungseingänge → Erschließung, allgemein, keine Wohnung.
    Beide behalten Notlicht, jede Wohnung hat einen Eingang, und der
    Messfall S4c/S3b (vom Stiegenhaus über keine Tür erreichbar) steht
    weiter in den Warnungen. Runde 8/9: beide allgemein (E5 Satz 2,
    aufgehoben). K4 (Owner 2026-09-30): v ist Mitglied seiner Wohnung →
    privat statt offen, Notlicht bleibt; offen bleibt keiner."""
    raeume, tueren = _loch_paar_etikett(typ_g, typ_v)()
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    by_id = {r.id: r for r in raeume}
    assert by_id["g"].nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"
    assert by_id["g"].wohnung_id is None
    assert by_id["v"].nutzungsklasse == "WOHNUNG_PRIVAT"
    for rid in ("g", "v"):
        assert (by_id[rid].ist_fluchtweg, by_id[rid].ist_communal) == (True, True)
        assert [w for w in warnungen if w.startswith(f"loch: {rid} — ")
                and "über keine Tür erreichbar" in w
                and "Messfall S4c/S3b" in w], warnungen
    assert not [w for w in warnungen if w.startswith("unbestimmt:")], warnungen
    assert [w for w in warnungen if w.startswith("k4: v — privat")], warnungen
    assert sorted(w.raum_ids for w in wohnungen) == [["v", "z2", "z3"], ["z1"]]
    assert all(w.eingangs_tuer_ids for w in wohnungen)


def _loch_in_wohnung():
    """Rennweg OG3 ``raum_10`` im Kleinen: GANG L, vom Stiegenhaus über keine
    Tür erreichbar (Tür- oder Raumerkennungsloch), nur an Küche, Zimmer und
    Bad; daneben die erschlossene Wohnung hinter Gang G. Offen gelassen
    bildet L mit k/z/b eine Wohnung OHNE Eingang."""
    return ([_r("S", "STIEGENHAUS"), _r("G", "GANG"), _r("Y", "ZIMMER", False),
             _r("Y2", "ZIMMER", False), _r("L", "GANG"),
             _r("k", "KÜCHE", False), _r("z", "ZIMMER", False),
             _r("b", "BAD", False)],
            [_t("ts", "G", "S", "stiegenhaustuer"),
             _t("ty", "G", "Y", "wohnungseingang"),
             _t("ty2", "G", "Y2", "wohnungseingang"),
             _t("tk", "L", "k", "zimmertuer"),
             _t("tz", "L", "z", "zimmertuer"),
             _t("tb", "L", "b", "wohnungseingang")])


def _loch_in_wohnung_mit_eingang():
    """Dieselbe Wohnung, aber die Küche hat einen Wohnungseingang ins Freie —
    die Wohnung hat also einen Eingang, auch wenn L offen bleibt."""
    raeume, tueren = _loch_in_wohnung()
    tueren.append(_t("te", "k", "AUSSEN", "wohnungseingang"))
    return raeume, tueren


def _loch_rest_ohne_eingang():
    """Dieselbe Wohnung, aber die Badtür hat keine Rolle: als ALLGEMEIN
    gezählt, bliebe das Bad eine Wohnung ohne Eingang — L zu öffnen hilft
    nicht."""
    raeume, tueren = _loch_in_wohnung()
    next(t for t in tueren if t.id == "tb").tuer_detail = None
    return raeume, tueren


def test_e5_loch_raum_ueber_zimmertuer_bleibt_in_seiner_wohnung():
    """Owner-Grundsatz 2026-09-22 (G1.2, G1.4): E5 Satz 2 („ein unbestimmter
    Raum darf keine Wohnung ohne Eingang erzeugen; wenn doch, gilt er als
    allgemein") ist AUFGEHOBEN — er ließ eine Notlicht-Regel (a) die Wohnung
    (b) zerteilen (Rennweg OG3 ``raum_10``: vier Einraum-Wohnungen). L hängt
    über die rohen Zimmertüren ``tk``/``tz`` an Küche und Zimmer → gehört zu
    ihrer Wohnung {L, b, k, z} (``tb`` verbindet innen), unbestimmt, Flags 11,
    der Messfall S4c/S3b mit Grund in den Warnungen. Dass diese Wohnung
    keinen Eingang hat, ist ein Tür- oder Raumerkennungsloch (auf HEAD
    genauso) — eine Mess-Abnahme, keine Regel im Code (G1.4). K4 (Owner
    2026-09-30): L ist Mitglied dieser Wohnung → Klasse privat statt offen,
    Flags bleiben 11."""
    raeume, tueren = _loch_in_wohnung()
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    by_id = {r.id: r for r in raeume}
    assert by_id["L"].nutzungsklasse == "WOHNUNG_PRIVAT"
    assert (by_id["L"].ist_fluchtweg, by_id["L"].ist_communal) == (True, True)
    assert [w for w in warnungen if w.startswith("k4: L — privat")
            and "vorher unbestimmt" in w], warnungen
    loch = [w for w in warnungen if w.startswith("loch: L — ")]
    assert len(loch) == 1, warnungen
    assert "über keine Tür erreichbar" in loch[0] and "Messfall S4c/S3b" in loch[0]
    assert "Zimmertür an seine Wohnung gebunden" in loch[0], loch[0]
    assert sorted((w.raum_ids, w.eingangs_tuer_ids) for w in wohnungen) == [
        (["L", "b", "k", "z"], []), (["Y"], ["ty"]), (["Y2"], ["ty2"])]


@pytest.mark.parametrize("bau", [_loch_in_wohnung_mit_eingang, _loch_rest_ohne_eingang],
                         ids=lambda f: f.__name__.lstrip("_"))
def test_e5_loch_raum_bleibt_offen_wo_allgemein_keinen_eingang_schafft(bau):
    """Die Grenzen von E5 Satz 2: hat die Wohnung schon einen Eingang, entsteht
    durch das Offenlassen keine Wohnung ohne Eingang; hätte der Rest auch mit
    L allgemein keinen, hilft „allgemein" nicht. In beiden Fällen bleibt L
    unbestimmt IN seiner Wohnung (Loch, Messfall S4c/S3b) und behält sein
    Notlicht. K4 (Owner 2026-09-30): danach Klasse privat als Mitglied der
    Wohnung, Notlicht bleibt."""
    raeume, tueren = bau()
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    by_id = {r.id: r for r in raeume}
    assert by_id["L"].nutzungsklasse == "WOHNUNG_PRIVAT"
    assert (by_id["L"].ist_fluchtweg, by_id["L"].ist_communal) == (True, True)
    gruppe = next(w for w in wohnungen if "L" in w.raum_ids)
    assert sorted(gruppe.raum_ids) == ["L", "b", "k", "z"]
    assert [w for w in warnungen if w.startswith("k4: L — privat")
            and "vorher unbestimmt: Ankerregel nicht auswertbar: vom Stiegenhaus "
                "über keine Tür" in w], warnungen
    assert [w for w in warnungen if w.startswith("loch: L — ")], warnungen


def _blattlos_getrennt():
    """Mollgasse EG ``raum_23`` im Kleinen (Reviewer Runde 7, Linse Naht,
    blockierend 4): VORRAUM R hat einen Wohnungseingang MIT Blatt ``tw`` zum
    allgemeinen Gang G (E8-Grenze), Zimmertüren zu WC w und Abstellraum a und
    eine Tür ohne Rolle zum untypisierten Raum U; U hängt über die BLATTLOSE
    Wohnungseingangs-Öffnung ``o`` am Gang. Die Ankerregel: „nur durch die
    Öffnung o OHNE Türblatt getrennt" → unbestimmt. Mit Polygonen, damit der
    Fluchtweg rechnen kann."""
    raeume = [
        Raum(id="S", raum_typ="STIEGENHAUS", polygon_mm=_rechteck(0, 0, 4000, 4000),
             ist_fluchtweg=True, ist_communal=True),
        Raum(id="G", raum_typ="GANG", polygon_mm=_rechteck(4000, 0, 12000, 4000),
             ist_fluchtweg=True, ist_communal=True),
        Raum(id="U", raum_typ="", polygon_mm=_rechteck(12000, 0, 16000, 8000)),
        Raum(id="R", raum_typ="VORRAUM", polygon_mm=_rechteck(4000, 4000, 12000, 8000),
             ist_fluchtweg=True, ist_communal=True),
        Raum(id="w", raum_typ="WC", polygon_mm=_rechteck(4000, 8000, 8000, 12000)),
        Raum(id="a", raum_typ="ABSTELLRAUM",
             polygon_mm=_rechteck(8000, 8000, 12000, 12000)),
    ]
    tueren = [
        _tuer("tx", "S", "AUSSEN", "hauseingang", xy=(0.0, 2000.0)),
        _tuer("ts", "G", "S", "stiegenhaustuer", xy=(4000.0, 2000.0)),
        _tuer("o", "G", "U", "wohnungseingang", xy=(12000.0, 2000.0)),
        _tuer("u", "U", "R", None, xy=(12000.0, 6000.0)),
        _tuer("tw", "R", "G", "wohnungseingang", xy=(8000.0, 4000.0)),
        _tuer("z1", "R", "w", "zimmertuer", xy=(6000.0, 8000.0)),
        _tuer("z2", "R", "a", "zimmertuer", xy=(10000.0, 8000.0)),
    ]
    tueren[2].ohne_tuerblatt = True
    return raeume, tueren


def test_blattlos_getrennter_unbestimmter_raum_zaehlt_als_erschliessung():
    """Befund Runde 7 (Linse Naht, blockierend 4): ``wohnungsraeume`` zählte
    JEDEN unbestimmten Nicht-Kandidaten mit Ankerurteil „unklar" als Loch zur
    Wohnung, auch den nur blattlos getrennten — obwohl E1 sagt „eine
    blattlose Öffnung schließt keine Wohnung ab". Mollgasse EG ``raum_23``
    verlor so 9 von 10 Zirkulationspunkten, die Wege aus WC und Abstellraum
    durch ihn fielen weg. Jetzt: nur ein GAR NICHT erreichbarer Raum ist ein
    Loch; der blattlos getrennte zählt für Wohnungsgrenze und korrigierte
    Rollen als Erschließung. R bleibt unbestimmt und behält Notlicht UND
    seine Wege („wer sein Notlicht behält, behält auch seine Zirkulation")."""
    from notbeleuchtung.raumerkennung.wohnungsklasse import korrigierte_rollen

    raeume, tueren = _blattlos_getrennt()
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    r = next(x for x in raeume if x.id == "R")
    assert r.nutzungsklasse is None
    assert (r.ist_fluchtweg, r.ist_communal) == (True, True)
    assert r.wohnung_id is None, "blattlos getrennt ist kein Loch"
    assert [w for w in warnungen if w.startswith("unbestimmt: R — Ankerregel nicht "
                                                 "auswertbar: vom Stiegenhaus nur durch")]
    assert sorted((w.raum_ids, w.eingangs_tuer_ids) for w in wohnungen) == [
        (["a"], ["z2"]), (["w"], ["z1"])]
    rollen = korrigierte_rollen(raeume, tueren)
    assert (rollen["z1"], rollen["z2"]) == ("wohnungseingang", "wohnungseingang")
    ausgaenge = [Ausgang(id="exit_tx", xy_mm=(0.0, 2000.0), typ="final_exit")]
    segmente = fluchtwege(raeume, tueren, ausgaenge, [], "EG")
    innen = Polygon(r.polygon_mm)
    drin = {s.segment_id for s in segmente for p in s.polyline_mm
            if innen.contains(Point(p))}
    assert {"seg_graph_z1", "seg_graph_z2"} <= drin, drin


_R8_BAUTEN = ([_topologie_l(a, b) for a, b in _ETIKETTEN]
              + [_loch_paar_etikett(a, b) for a, b in _ETIKETTEN]
              + [_loch_in_wohnung, _loch_in_wohnung_mit_eingang,
                 _loch_rest_ohne_eingang, _blattlos_getrennt, _vorraum_am_keller])


# Gegenbeispiele des Reviewers zu S7c Runde 1 (Linse Einbahn, Blockierend 1):
# Topologien, auf denen die (b)-Eingangsliste und die korrigierten
# Wohnungseingänge auseinanderfallen. Klassen NICHT vorgesetzt wirken nur dort,
# wo ``bilde_wohnungen`` sie ohnehin neu setzt (GANG/VORRAUM).
def _s7c_aussen_stiegenhaustuer():
    return _s7c_wanderung("GANG", "stiegenhaustuer", False)


def _s7c_aussen_brandschutz():
    return _s7c_wanderung("GANG", "brandschutztuer", False)


def _s7c_aussen_balkontuer_an_gang():
    return _s7c_wanderung("GANG", "balkontuer", False)


def _s7c_zwei_aussen():
    """Zwei äußere Türen des privaten Vorraums in zwei Gänge."""
    raeume, tueren = _s7c_wanderung("GANG", "stiegenhaustuer", False)
    raeume.append(Raum(id="gang2", raum_typ="GANG", nutzungsklasse=wk.ALLGEMEIN,
                       polygon_mm=_rechteck(5000, -4000, 9000, 0),
                       ist_fluchtweg=True, ist_communal=True))
    tueren.append(_tuer("t_out2", "vor", "gang2", "brandschutztuer",
                        xy=(7000.0, 0.0)))
    return raeume, tueren


def _s7c_privater_gang():
    """Privat gewordener GANG ``flur`` statt VORRAUM, äußere Tür roh
    ``stiegenhaustuer``."""
    return ([Raum(id="zi", raum_typ="ZIMMER", polygon_mm=_rechteck(0, 0, 5000, 4000)),
             Raum(id="flur", raum_typ="GANG",
                  polygon_mm=_rechteck(5000, 0, 9000, 4000)),
             Raum(id="stgh", raum_typ="STIEGENHAUS",
                  polygon_mm=_rechteck(9000, 0, 13000, 4000),
                  ist_fluchtweg=True, ist_communal=True),
             Raum(id="gang", raum_typ="GANG",
                  polygon_mm=_rechteck(5000, 4000, 9000, 8000),
                  ist_fluchtweg=True, ist_communal=True)],
            [_tuer("t_in", "flur", "zi", "zimmertuer", xy=(5000.0, 2000.0)),
             _tuer("t_we", "stgh", "flur", "wohnungseingang", xy=(9000.0, 2000.0)),
             _tuer("t_out", "flur", "gang", "stiegenhaustuer", xy=(7000.0, 4000.0))])


def _s7c_verschachtelt_weich():
    """Verschachtelte Vorräume ``stgh -t_we-> vor1 -t_mid-> vor2 -t_in-> zi``;
    ``vor2`` ist zusätzlich blattlos vom Gang erreichbar (``t_loch``), also nur
    unbestätigt privat (Option W). Vorbestehend schon auf ``bface2b``."""
    loch = _tuer("t_loch", "vor2", "gang", xy=(5500.0, 4000.0))
    loch.ohne_tuerblatt = True
    return ([Raum(id="zi", raum_typ="ZIMMER", polygon_mm=_rechteck(0, 0, 4000, 4000)),
             Raum(id="vor2", raum_typ="VORRAUM",
                  polygon_mm=_rechteck(4000, 0, 7000, 4000)),
             Raum(id="vor1", raum_typ="VORRAUM",
                  polygon_mm=_rechteck(7000, 0, 10000, 4000)),
             Raum(id="stgh", raum_typ="STIEGENHAUS",
                  polygon_mm=_rechteck(10000, 0, 14000, 4000),
                  ist_fluchtweg=True, ist_communal=True),
             Raum(id="gang", raum_typ="GANG",
                  polygon_mm=_rechteck(4000, 4000, 10000, 8000),
                  ist_fluchtweg=True, ist_communal=True)],
            [_tuer("t_in", "vor2", "zi", "zimmertuer", xy=(4000.0, 2000.0)),
             _tuer("t_mid", "vor1", "vor2", "zimmertuer", xy=(7000.0, 2000.0)),
             _tuer("t_we", "stgh", "vor1", "wohnungseingang", xy=(10000.0, 2000.0)),
             _tuer("t_g", "gang", "stgh", xy=(10000.0, 6000.0)),
             loch])


_S7C_GEGENBEISPIELE = [_s7c_aussen_stiegenhaustuer, _s7c_aussen_brandschutz,
                       _s7c_aussen_balkontuer_an_gang, _s7c_zwei_aussen,
                       _s7c_privater_gang, _s7c_verschachtelt_weich]


@pytest.mark.parametrize("bau", _R7_BAUTEN + _ROLLEN_OSZ + [_nicht_konvergent] + _R8_BAUTEN
                         + [_s7c_flur_und_gang] + _S7C_GEGENBEISPIELE,
                         ids=lambda f: f.__name__.lstrip("_"))
def test_e7_bilde_wohnungen_liest_keine_korrigierte_rolle(bau, monkeypatch):
    """E7.2 wörtlich: „Die gesamte Klassifikation (…, Wohnungsbildung/
    ``wohnung_id``, Flags) liest KEINE korrigierte Rolle." Bis Runde 7 rief
    ``bilde_wohnungen`` ``korrigierte_rollen`` für die Eingangsliste der
    Wohnungen. Jetzt ist die Funktion während des Laufs verboten — auch die
    neue Regel E5 Satz 2 („Wohnung ohne Eingang") liest nur Klassen und
    rohe Rollen.

    Die Eingangsliste (b) und die danach abgeleiteten korrigierten
    Wohnungseingänge (a) sind NICHT gleich, und sie dürfen es nicht erzwingen:
    (b) liest einen klassenfreien Erschließungs-Begriff
    (``wohnungszugehoerigkeit``), (a) Klassen und Ankerregel
    (``wohnungsraeume``); Gleichheit ginge nur durch Rückspeisen von (a) nach
    (b), gegen die Einbahn. Gemessen (S7c Runde 2, 66 Topologien: 55 aus
    diesem Modul, 11 des Reviewers) weichen die Listen in BEIDEN Richtungen ab,
    aber nur an zwei Stellen — genau das bindet diese Zusicherung, sonst gilt
    Tür für Tür Gleichheit:

    * NUR in (b): der Raum auf der Wohnungsseite gehört zur (b)-Wohnung, ist
      für (a) aber nicht privat (unbestimmt, allgemein klassifiziert, Option
      W) — schon auf ``bface2b`` 4× (``verschachtelt_weich``,
      ``zwei_gruppen``, ``durchleitung_plan_direkt``);
    * NUR korrigiert: ausschließlich an Türen mit anderer roher Rolle als
      Zimmertür/Wohnungseingang, die S7c an der Grenze privat|Erschließung
      zum Wohnungseingang macht (22×; 20 davon zusätzlich an einem Raum, den
      (a) und (b) verschieden einordnen — der unbestätigt private GANG als
      eigene (b)-Wohnung —, 2 nicht: ``_rollen_oszillator``, ``tz``). Eine
      rohe Zimmertür oder ein roher Wohnungseingang am Rand ist nie NUR
      korrigiert (Reviewer S7c Runde 2, 66 Topologien, 12 Pläne)."""
    from notbeleuchtung.raumerkennung import wohnungen as W

    echt = wk.korrigierte_rollen

    def verboten(*_a, **_k):
        raise AssertionError("korrigierte_rollen während bilde_wohnungen gelesen")

    monkeypatch.setattr(wk, "korrigierte_rollen", verboten)
    monkeypatch.setattr(W, "korrigierte_rollen", verboten, raising=False)
    raeume, tueren = bau()
    wohnungen = bilde_wohnungen(raeume, tueren)
    monkeypatch.undo()
    korr = echt(raeume, tueren)
    privat_a, _ = wk.wohnungsraeume(raeume, tueren)
    in_wohnung = {rid for w in wohnungen for rid in w.raum_ids}
    verschieden = {r.id for r in raeume
                   if (r.id in in_wohnung) != (r.id in privat_a)}
    for w in wohnungen:
        drin = set(w.raum_ids)
        rand = [t for t in tueren if len({t.von_raum, t.nach_raum} & drin) == 1]
        assert set(w.eingangs_tuer_ids) <= {t.id for t in rand}, w
        for t in rand:
            in_b = t.id in w.eingangs_tuer_ids
            in_k = korr[t.id] == "wohnungseingang"
            innen = t.von_raum if t.von_raum in drin else t.nach_raum
            if in_b and not in_k:
                assert innen in verschieden, ("nur (b)", w, t.id, t.tuer_detail)
            elif in_k and not in_b:
                assert t.tuer_detail not in ("zimmertuer", "wohnungseingang"), (
                    "nur korrigiert", w, t.id, t.tuer_detail)


@pytest.mark.parametrize("bau", _R8_BAUTEN, ids=lambda f: f.__name__.lstrip("_"))
def test_r8_idempotent_und_reihenfolge_invariant(bau):
    """(f) Reihenfolge-Invarianz und Idempotenz auch auf den Runde-8-Mustern
    (Etikett, Loch in Wohnung ohne Eingang, blattlos getrennt)."""
    raeume, tueren = bau()
    w = bilde_wohnungen(raeume, tueren)
    eins = _vollzustand(raeume, tueren, w)
    w = bilde_wohnungen(raeume, tueren)
    assert _vollzustand(raeume, tueren, w) == eins
    assert len(_stichprobe_reihenfolgen(bau)) == 1


# ── (n) Runde 9: Board 4 als ALLGEMEINE Regel (L1) ──────────────────────────
def _fest(raeume, tueren) -> dict:
    """Die festen Räume der Regel (Owner 2026-09-22): Loch-Räume nach rohen
    Türen (an die Wohnung gebunden → offen, sonst allgemein), die nach R1
    gebundenen Gänge (offen, R1-Erweiterung 2026-09-27) und der Riegel (G3,
    allgemein) — wie ``bilde_wohnungen``."""
    _, in_wohnung, erschliessung, r1_gaenge = wk.wohnungszugehoerigkeit(raeume, tueren)
    fest = dict.fromkeys(in_wohnung | r1_gaenge)
    fest.update(dict.fromkeys(erschliessung, wk.ALLGEMEIN))
    for rid in wk.riegel_nie_privat(raeume, tueren):
        fest.setdefault(rid, wk.ALLGEMEIN)
    return fest


def _eine_runde(raeume, tueren, fest):
    """Test-Orakel: EINE Runde der Klassenregel, wie ``bilde_wohnungen`` sie
    iteriert — Schritt 2 auf den offenen Kandidaten, Flur-Verfeinerung und
    Riegel, alle aus demselben Schnappschuss (Jacobi)."""
    from notbeleuchtung.raumerkennung import wohnungen as W

    kand = wk.kandidaten(raeume, tueren)
    offen = kand - set(wk.schritt1(raeume, tueren, kand)) - set(fest)
    stgh = {r.id for r in raeume if r.raum_typ == "STIEGENHAUS"}
    alt = {r.id: r.nutzungsklasse for r in raeume}
    zwei = {rid: wk.schritt2_urteil(rid, tueren, alt, stgh, 0)[0] for rid in offen}
    ausser = kand | set(fest)
    W._verfeinere_gang_privat(raeume, tueren, ausser=ausser,
                              grenze=wk.erschliessung_erwiesen(raeume, tueren),
                              unbestimmt={rid for rid in kand if alt[rid] is None})
    wk.riegel(raeume, tueren, ausser)
    for r in raeume:
        if r.id in zwei:
            r.nutzungsklasse = zwei[r.id]
    return {r.id: r.nutzungsklasse for r in raeume}


def _fixpunkte(bau):
    """``(bewegliche Räume, [(Belegung, entzogen)])`` — ALLE Fixpunkte einer
    Runde über die beweglichen GANG/VORRAUM (Belegungen allgemein, privat,
    offen; Schritt 1 privat, feste Räume nach ``_fest``)."""
    from notbeleuchtung.raumerkennung.nutzungsklasse import nutzungsklasse_fuer

    raeume, tueren = bau()
    kand = wk.kandidaten(raeume, tueren)
    eins = wk.schritt1(raeume, tueren, kand)
    fest = _fest(raeume, tueren)
    bew = sorted(r.id for r in raeume if r.raum_typ in wk.SCOPE_TYPEN
                 and r.id not in eins and r.id not in fest)
    out = []
    for belegung in itertools.product((wk.ALLGEMEIN, wk.PRIVAT, None), repeat=len(bew)):
        raeume, tueren = bau()
        soll = dict(zip(bew, belegung))
        for r in raeume:
            if r.raum_typ not in wk.SCOPE_TYPEN:
                r.nutzungsklasse = r.nutzungsklasse or nutzungsklasse_fuer(r.raum_typ)
            elif r.id in eins:
                r.nutzungsklasse = wk.PRIVAT
            elif r.id in fest:
                r.nutzungsklasse = fest[r.id]
            else:
                r.nutzungsklasse = soll[r.id]
        vor = {r.id: r.nutzungsklasse for r in raeume}
        if _eine_runde(raeume, tueren, fest) == vor:
            out.append((soll, frozenset(wk.bestaetigt_privat(raeume, tueren))))
    return bew, out


def _minimalpaar(y_blattlos: bool):
    """Reviewer-Minimalpaar Runde 8 (Linse Regel, blockierend): Kandidat C
    hinter dem Wohnungseingang ``tw`` MIT Blatt (Schritt 1: privat), dahinter
    X und Y. X ist ankerprivat und hat zwei Fixpunkte — allgemein und privat.
    ``y_blattlos=False``: Y wie X nur über ``tw`` erreichbar (Muster Rennweg
    OG1 ``raum_4``/``raum_5``). ``True``: Y zusätzlich über ein Zimmer Q und
    eine BLATTLOSE Öffnung am Stiegenhaus erreichbar, X–Y ein Wohnungseingang
    MIT Blatt (Muster Mollgasse EG ``raum_57``/``raum_29``). Runde 8 (Start
    beim Ankerurteil) lieferte X einmal privat, einmal allgemein."""
    def bau():
        raeume = [_r("S", "STIEGENHAUS"), _r("C", "VORRAUM"), _r("X", "VORRAUM"),
                  _r("Y", "VORRAUM"), _r("Z", "ZIMMER", False)]
        tueren = [_t("tw", "S", "C", "wohnungseingang"),
                  _t("cx", "C", "X", "zimmertuer"),
                  _t("yz", "Y", "Z", "zimmertuer")]
        if y_blattlos:
            raeume.append(_r("Q", "ZIMMER", False))
            tueren += [_t("xy", "X", "Y", "wohnungseingang"),
                       _t("sq", "S", "Q", "wohnungseingang", blattlos=True),
                       _t("qy", "Q", "Y", "zimmertuer")]
        else:
            tueren.append(_t("xy", "X", "Y", "zimmertuer"))
        return raeume, tueren
    bau.__name__ = f"_minimalpaar_{'Y_blattlos' if y_blattlos else 'Y_privat'}"
    return bau


@pytest.mark.parametrize("y_blattlos", [False, True], ids=["Y_privat", "Y_blattlos"])
def test_e5_zwei_fixpunkte_beleg_vor_tiebreak(y_blattlos):
    """Owner-Grundsatz 2026-09-22 (G2): „physischer Beleg (Wohnungseingang
    mit Türblatt, Ankerregel bestätigt alle strittigen Räume ausnahmslos und
    lässt keinen offen) geht vor dem Fixpunkt-Tiebreak." X hat in beiden
    Varianten zwei Fixpunkte (allgemein, privat); welcher gilt, hängt weder
    am Verlauf der Iteration noch am Etikett (Reviewer Runde 8, Linse Regel).
    ``Y_privat`` (Muster Rennweg OG1 ``raum_4``/``raum_5``): der private
    Fixpunkt macht X und Y ankerbestätigt privat → er gilt, entzogen werden
    C, X, Y. ``Y_blattlos`` (Muster Mollgasse EG ``raum_57``/``raum_29``): Y
    ist nicht ankerbestätigt → Tiebreak (Board 4), X und Y allgemein,
    Flags 11, entzogen nur C. Runde 9 (L1) lieferte in beiden allgemein."""
    bau = _minimalpaar(y_blattlos)
    raeume, tueren = bau()
    assert wk.ankerurteil(raeume, tueren)["X"][0] == wk.A_PRIVAT, "Vorbedingung"
    _, fix = _fixpunkte(bau)
    assert {f["X"] for f, _ in fix} >= {wk.ALLGEMEIN, wk.PRIVAT}, fix
    bilde_wohnungen(raeume, tueren)
    by_id = {r.id: r for r in raeume}
    klasse, flags = ((wk.ALLGEMEIN, (True, True)) if y_blattlos
                     else (wk.PRIVAT, (False, False)))
    for rid in ("X", "Y"):
        assert by_id[rid].nutzungsklasse == klasse, rid
        assert (by_id[rid].ist_fluchtweg, by_id[rid].ist_communal) == flags, rid
    assert wk.bestaetigt_privat(raeume, tueren) == ({"C"} if y_blattlos
                                                     else {"C", "X", "Y"})


def _zufall(rnd):
    """Zufallstopologie — derselbe Generator wie in den Reviewer-Suchen
    Runde 7/8 (Stiegenhaus, 2–5 GANG/VORRAUM, 1–4 Zimmer/Bad/WC, manchmal ein
    Keller und eine Tür ins Freie, zufällige Rollen, 20 % blattlos)."""
    raeume = [_r("S", "STIEGENHAUS")]
    n_scope, n_priv = rnd.randint(2, 5), rnd.randint(1, 4)
    raeume += [_r(f"g{i}", rnd.choice(["GANG", "VORRAUM"])) for i in range(n_scope)]
    raeume += [_r(f"z{i}", rnd.choice(["ZIMMER", "BAD", "WC"]), False)
               for i in range(n_priv)]
    if rnd.random() < .3:
        raeume.append(_r("k0", "KELLER", False))
    ids = [r.id for r in raeume]
    tueren, paare = [], set()
    for i in range(rnd.randint(n_scope + 1, n_scope + n_priv + 3)):
        a, b = rnd.sample(ids, 2)
        if (a, b) in paare or (b, a) in paare:
            continue
        paare.add((a, b))
        rolle = rnd.choice([None, "zimmertuer", "zimmertuer", "wohnungseingang",
                            "wohnungseingang", "stiegenhaustuer"])
        tueren.append(_t(f"t{i}", a, b, rolle, rnd.random() < .2))
    if rnd.random() < .2:
        tueren.append(_t("ta", rnd.choice(ids[1:]), "AUSSEN"))
    return raeume, tueren


def test_e5_zwei_fixpunkte_zufallssuche(monkeypatch):
    """Board 4 und G2 (Owner 2026-09-22) als allgemeine Regel, gesetzte
    Zufallssuche (Generator und Seed der Reviewer-Suchen, 200 Topologien,
    alle Fixpunkte über 3^n Belegungen): ausgeliefert wird ein Fixpunkt —
    einer mit den MEISTEN allgemeinen Räumen (Tiebreak), außer ein Fixpunkt
    macht alle abweichenden Räume ankerbestätigt privat und lässt keinen
    offen (Beleg vor Tiebreak); dann dieser, und in dieser Suche wird keiner
    übersehen. Das ist GEMESSEN, nicht bewiesen — Runde 11 zusätzlich 4 475
    Topologien mit Fixpunkt (Seeds 2–4), 0 übersehen; vor der Korrektur P3
    (Probe ab dem erreichten Stand) war es 1, Zeuge
    ``test_r11_beleg_probe_startet_beim_erreichten_stand``. Kein
    Raum des Riegels (G3) ist privat. Erreicht die Iteration keinen Fixpunkt
    (Schritt 3), dann nur, wo es keinen gibt, und jeder unbestimmte Raum
    behält sein Notlicht. Bis Runde 9 prüfte die Suche „kleinster Entzug" —
    der Beleg vor Tiebreak entzieht gewollt mehr (OG1 ``raum_4``/``raum_5``).

    Die Suche prüft die Klassen-Iteration; K4 (Owner 2026-09-30) läuft
    danach, ist hier ausgeschaltet und hat seine eigene Suche über dieselben
    Topologien (``test_k4_zufallssuche``)."""
    import random

    from notbeleuchtung.raumerkennung import wohnungen as W

    monkeypatch.setattr(W, "klasse_aus_umriss", lambda raeume, tueren: {})
    rnd = random.Random(20260921)
    verstoesse = []
    for i in range(200):
        spec = _zufall(rnd)

        def bau(spec=spec):
            return copy.deepcopy(spec)

        raeume, tueren = bau()
        warnungen: list[str] = []
        bilde_wohnungen(raeume, tueren, warnungen)
        bew, fix = _fixpunkte(bau)
        entzug = wk.bestaetigt_privat(raeume, tueren)
        urteil = wk.ankerurteil(raeume, tueren)
        by_id = {r.id: r for r in raeume}
        verstoesse += [(i, "Riegel privat", rid) for rid in wk.riegel_nie_privat(raeume, tueren)
                       if by_id[rid].nutzungsklasse == wk.PRIVAT]
        if any(w.startswith("unbestimmt:") and "Schritt 3" in w for w in warnungen):
            if fix:
                verstoesse.append((i, "Schritt 3 trotz Fixpunkt"))
            verstoesse += [(i, "Schritt 3 ohne Notlicht", rid) for rid in bew
                           if by_id[rid].nutzungsklasse is None
                           and ((by_id[rid].ist_fluchtweg, by_id[rid].ist_communal)
                                != (True, True) or rid in entzug)]
            continue
        geliefert = {rid: by_id[rid].nutzungsklasse for rid in bew}
        fixe = [f for f, _ in fix]
        if geliefert not in fixe:
            verstoesse.append((i, "kein Fixpunkt geliefert"))
            continue

        def belegt(f, basis, bew=bew, urteil=urteil):
            anders = [rid for rid in bew if f[rid] != basis[rid]]
            return anders and all(f[rid] == wk.PRIVAT and urteil[rid][0] == wk.A_PRIVAT
                                  for rid in anders)

        n_a = max(sum(k == wk.ALLGEMEIN for k in f.values()) for f in fixe)
        tiebreak = [f for f in fixe if sum(k == wk.ALLGEMEIN for k in f.values()) == n_a]
        if geliefert in tiebreak:
            if any(belegt(f, geliefert) for f in fixe):
                verstoesse.append((i, "Beleg übersehen"))
        elif not any(belegt(geliefert, f) for f in tiebreak):
            verstoesse.append((i, "weder Tiebreak noch voller Beleg"))
    assert not verstoesse, f"{len(verstoesse)} Verstöße, z. B. {verstoesse[:5]}"


def test_k4_zufallssuche(monkeypatch):
    """K4 (Owner 2026-09-30) über die 200 Topologien der Fixpunkt-Suche, je
    mit und ohne K4: K4 setzt nur die Klasse von GANG/VORRAUM, die ohne K4
    unbestimmt sind; die Wohnungen (b) sind dieselben; kein Raum des Riegels
    wird privat; Notlicht ändert sich nur 11 → 00 und nur für Räume, die
    ``bestaetigt_privat`` trägt; wer offen bleibt, behält Flags 11."""
    import random

    from notbeleuchtung.raumerkennung import wohnungen as W

    def lauf(spec, mit_k4):
        raeume, tueren = copy.deepcopy(spec)
        if not mit_k4:
            monkeypatch.setattr(W, "klasse_aus_umriss", lambda r, t: {})
        bilde_wohnungen(raeume, tueren)
        monkeypatch.undo()
        return raeume, tueren

    rnd = random.Random(20260921)
    verstoesse = []
    for i in range(200):
        spec = _zufall(rnd)
        ohne, _ = lauf(spec, False)
        mit, tueren = lauf(spec, True)
        vor = {r.id: r for r in ohne}
        entzug = wk.bestaetigt_privat(mit, tueren)
        riegel = wk.riegel_nie_privat(mit, tueren)
        for r in mit:
            v = vor[r.id]
            if r.wohnung_id != v.wohnung_id:
                verstoesse.append((i, "Wohnung", r.id))
            if r.nutzungsklasse != v.nutzungsklasse and (
                    r.raum_typ not in wk.SCOPE_TYPEN or v.nutzungsklasse is not None):
                verstoesse.append((i, "Klasse außerhalb K4", r.id))
            if r.id in riegel and r.nutzungsklasse == wk.PRIVAT:
                verstoesse.append((i, "Riegel privat", r.id))
            fl, fl_v = (r.ist_fluchtweg, r.ist_communal), (v.ist_fluchtweg, v.ist_communal)
            if fl != fl_v and not (fl_v == (True, True) and fl == (False, False)
                                   and r.id in entzug):
                verstoesse.append((i, "Flags", r.id, fl_v, fl))
            if (r.raum_typ in wk.SCOPE_TYPEN and r.nutzungsklasse is None
                    and fl != (True, True)):
                verstoesse.append((i, "offen ohne Notlicht", r.id))
    assert not verstoesse, f"{len(verstoesse)} Verstöße, z. B. {verstoesse[:5]}"


_R9_BAUTEN = [_minimalpaar(False), _minimalpaar(True), _vorraum_hinter_blatt]


@pytest.mark.parametrize("bau", _R9_BAUTEN, ids=lambda f: f.__name__.lstrip("_"))
def test_r9_einbahn_idempotent_und_reihenfolge_invariant(bau, monkeypatch):
    """(a) und (f) auf den Runde-9-Mustern: verfälschte korrigierte Rollen
    ändern weder Klasse noch Flags noch ``wohnung_id`` (Einbahn, Board 7); ein
    zweiter Lauf ist gleich; über die Stichproben-Reihenfolgen EIN
    Ergebnis."""
    from notbeleuchtung.raumerkennung import wohnungen as W

    raeume, tueren = bau()
    w = bilde_wohnungen(raeume, tueren)
    eins = _vollzustand(raeume, tueren, w)
    w = bilde_wohnungen(raeume, tueren)
    assert _vollzustand(raeume, tueren, w) == eins, "nicht idempotent"
    assert len(_stichprobe_reihenfolgen(bau)) == 1
    def falsch(_raeume, tueren_):
        return {t.id: "wohnungseingang" for t in tueren_}

    monkeypatch.setattr(wk, "korrigierte_rollen", falsch)
    monkeypatch.setattr(W, "korrigierte_rollen", falsch, raising=False)
    raeume, tueren = bau()
    w = bilde_wohnungen(raeume, tueren)
    assert _vollzustand(raeume, tueren, w) == eins, "hängt an korrigierten Rollen"


# ── (o) Runde 10: Owner-Grundsatz 2026-09-22 — (a) Notlicht, (b) Wohnung ────
# „Es sind zwei getrennte Fragen, die nie vermischt werden: (a) Bekommt der
# Raum Notlicht? Entscheidet fail-safe … (b) Zu welcher Wohnung gehört der
# Raum? Entscheiden ausschließlich rohe Türen: Wohnungseingang ist Grenze,
# Zimmertür ist innen. … Eine Regel zu (a) darf keine Wohnung zerteilen."
def _wohnungsstand(raeume, wohnungen):
    """(b) vollständig: Wohnungen mit ihren Eingängen und ``wohnung_id`` je Raum."""
    return (sorted((tuple(sorted(w.raum_ids)), tuple(sorted(w.eingangs_tuer_ids)))
                   for w in wohnungen),
            sorted((r.id, r.wohnung_id) for r in raeume))


def _riegel_bau(weg: str):
    """G3 je Weg (Reviewer Runde 9, Linse Sicherheit, Hinweis 1): ein VORRAUM V
    hinter einem Wohnungseingang MIT Blatt, der zugleich einen Hauseingang
    bzw. eine Tür zu einem allgemeinen Nebenraum hat.

    * ``schritt1_hauseingang``/``schritt1_ins_freie``/``schritt1_nebenraum``:
      V ist Kandidat (``tw`` zum Stiegenhaus) — Schritt 1 sprach ihn bisher
      endgültig privat (``schritt1_ins_freie``: Tür ins Freie ohne Rolle).
    * ``e8_nebenraum``: V ist kein Kandidat; sein Wohnungseingang MIT Blatt
      führt zum KELLER K, den die Ankerregel vom Stiegenhaus ohne
      Wohnungseingang erreicht — die E8-Grenze nahm K aus der
      Flur-Verfeinerung, V wurde privat.
    * ``e8_hauseingang``: V hinter ``tw`` zum allgemeinen Gang G (E8-Grenze),
      dazu ein Hauseingang zu einem untypisierten Raum U.
    * ``tiebreak_nebenraum``: das OG1-Paar X/Y (``_minimalpaar``), X mit Tür
      zu einem Keller — die Beleg-Probe (G2) darf ihn nicht privat machen."""
    def bau():
        if weg == "tiebreak_nebenraum":
            raeume, tueren = _minimalpaar(False)()
            return (raeume + [_r("K", "KELLER", False)],
                    tueren + [_t("xk", "X", "K")])
        raeume = [_r("S", "STIEGENHAUS"), _r("V", "VORRAUM"), _r("Z", "ZIMMER", False)]
        tueren = [_t("tz", "V", "Z", "zimmertuer")]
        if weg.startswith("schritt1"):
            tueren.append(_t("tw", "S", "V", "wohnungseingang"))
        if weg == "schritt1_hauseingang":
            tueren.append(_t("tx", "V", "AUSSEN", "hauseingang"))
        elif weg == "schritt1_ins_freie":
            tueren.append(_t("tx", "V", "AUSSEN"))
        elif weg == "schritt1_nebenraum":
            raeume.append(_r("K", "KELLER", False))
            tueren.append(_t("tk", "V", "K"))
        elif weg == "e8_nebenraum":
            raeume.append(_r("K", "KELLER", False))
            tueren += [_t("sk", "S", "K"), _t("tw", "K", "V", "wohnungseingang")]
        elif weg == "e8_hauseingang":
            raeume += [_r("G", "GANG"), _r("U", "")]
            tueren += [_t("ts", "S", "G", "stiegenhaustuer"),
                       _t("tw", "G", "V", "wohnungseingang"),
                       _t("tu", "V", "U", "hauseingang")]
        return raeume, tueren
    bau.__name__ = f"_riegel_{weg}"
    return bau


_RIEGEL_WEGE = ["schritt1_hauseingang", "schritt1_ins_freie", "schritt1_nebenraum",
                "e8_nebenraum",
                "e8_hauseingang", "tiebreak_nebenraum"]


def _hinter_blatt(typ: str, fremde_wohnung: bool = False):
    """G4: VORRAUM ``vor`` hinter dem Wohnungseingang ``tw`` MIT Blatt, dahinter
    genau ein Raum ``x`` vom Typ ``typ`` (``""`` = untypisiert). Mit
    ``fremde_wohnung`` liegt ein Zimmer daneben, aber in einer ANDEREN Wohnung
    (eigener Wohnungseingang vom Stiegenhaus)."""
    def bau():
        raeume = [_r("stgh", "STIEGENHAUS"), _r("vor", "VORRAUM"), _r("x", typ, False)]
        tueren = [_t("tw", "stgh", "vor", "wohnungseingang"),
                  _t("t1", "vor", "x", "zimmertuer")]
        if fremde_wohnung:
            raeume.append(_r("zi", "ZIMMER", False))
            tueren.append(_t("tz", "stgh", "zi", "wohnungseingang"))
        return raeume, tueren
    bau.__name__ = f"_hinter_blatt_{typ or 'untypisiert'}{'_fremd' if fremde_wohnung else ''}"
    return bau


def _zwei_gruppen():
    """G2 je Gruppe: das OG1-Paar X/Y (``_minimalpaar``, voll belegt) und
    daneben, am eigenen Stiegenhaus bS, die Gruppe bG0/bG1 ohne vollen Beleg
    (Zufallsfund Runde 10, Paar 1661: ab privat gestartet macht Schritt 2 den
    Kandidaten bG2 privat, ohne Ankerbestätigung)."""
    raeume, tueren = _minimalpaar(False)()
    raeume += [_r("bS", "STIEGENHAUS"), _r("bG0", "VORRAUM"), _r("bG1", "VORRAUM"),
               _r("bG2", "GANG"), _r("bG3", "VORRAUM"), _r("bZ0", "WC", False),
               _r("bZ1", "WC", False), _r("bK", "KELLER", False)]
    tueren += [_t("b0", "bG2", "bS"), _t("b1", "bZ0", "bZ1", "stiegenhaustuer", True),
               _t("b2", "bG0", "bG1"), _t("b3", "bK", "bZ0", "wohnungseingang"),
               _t("b4", "bG2", "bG1", "wohnungseingang"),
               _t("b5", "bS", "bK", "zimmertuer"),
               _t("b6", "bG2", "bG3", "zimmertuer", True)]
    return raeume, tueren


_R10_BAUTEN = ([_loch_paar, _muth_paar, _loch_in_wohnung, _minimalpaar(False),
                _minimalpaar(True), _o3, _u1, _u2, _topologie_l("GANG", "GANG"),
                _blattlos_getrennt, _plan_zwei_wohnungen, _vorraum_hinter_blatt]
               + [_riegel_bau(w) for w in _RIEGEL_WEGE]
               + [_hinter_blatt("BAD"), _hinter_blatt("ZIMMER", True),
                  _zwei_gruppen])


@pytest.mark.parametrize("bau", _R10_BAUTEN, ids=lambda f: f.__name__.lstrip("_"))
def test_r10_wohnung_liest_weder_klasse_noch_tiebreak(bau, monkeypatch):
    """G1.1: die Wohnungszugehörigkeit (``wohnung_id``, Wohnungsgruppen,
    Wohnungseingänge) liest nur rohe Türrollen, Türblatt, Topologie und den
    Raumtyp — nie ``nutzungsklasse``, nie ein Ergebnis von Schritt 1/2/3, nie
    den Fixpunkt-Tiebreak. Klassen, Flags und ``wohnung_id`` ALLER Räume vor
    dem Lauf beliebig verfälscht, und die Klassenregel (a) umgedreht (Start
    und feste Räume PRIVAT statt ALLGEMEIN) → dieselben Wohnungen."""
    import random

    from notbeleuchtung.raumerkennung import wohnungen as W

    raeume, tueren = bau()
    soll = _wohnungsstand(raeume, bilde_wohnungen(raeume, tueren))
    klassen = [wk.PRIVAT, wk.ALLGEMEIN, wk.NEBENRAUM, None]
    for seed in range(6):
        rnd = random.Random(seed)
        raeume, tueren = bau()
        for r in raeume:
            r.nutzungsklasse = rnd.choice(klassen)
            r.ist_fluchtweg = r.ist_communal = rnd.random() < .5
            r.wohnung_id = rnd.choice([None, "top_9"])
        assert _wohnungsstand(raeume, bilde_wohnungen(raeume, tueren)) == soll, seed
    monkeypatch.setattr(W, "ALLGEMEIN", wk.PRIVAT)
    raeume, tueren = bau()
    assert _wohnungsstand(raeume, bilde_wohnungen(raeume, tueren)) == soll, (
        "Tiebreak umgedreht")


@pytest.mark.parametrize("bau,loch,wohnung,erschliessung", [
    (_loch_paar, "v", ["v", "z2", "z3"], "g"),
    (_muth_paar, "V", ["V", "b", "k"], "G"),
], ids=["loch_paar", "muth_paar"])
def test_r10_loch_raum_folgt_rohen_tueren(bau, loch, wohnung, erschliessung):
    """G1.2 (Owner 2026-09-22, Fragebogen „Wohnung folgt rohen Türen"): ein
    Loch-Raum, der über rohe Zimmertüren an eine Wohnung gebunden ist, gehört
    zu dieser Wohnung (b) und bleibt für (a) unbestimmt, Flags 11; einer, der
    nur über rohe Wohnungseingänge angebunden ist, ist Erschließung — keine
    Wohnung, allgemein, Flags 11. Der Messfall S4c/S3b bleibt im Bericht.
    Bis Runde 9 waren beide allgemein (E5 Satz 2, aufgehoben). K4 (Owner
    2026-09-30): der gebundene Loch-Raum ist Mitglied seiner Wohnung → Klasse
    privat statt offen, Flags bleiben 11."""
    raeume, tueren = bau()
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    by_id = {r.id: r for r in raeume}
    r = by_id[loch]
    assert r.nutzungsklasse == wk.PRIVAT, r.nutzungsklasse
    assert (r.ist_fluchtweg, r.ist_communal) == (True, True)
    assert sorted(next(w for w in wohnungen if loch in w.raum_ids).raum_ids) == wohnung
    assert [w for w in warnungen if w.startswith(f"k4: {loch} — privat")
            and "vorher unbestimmt" in w], warnungen
    g = by_id[erschliessung]
    assert g.nutzungsklasse == wk.ALLGEMEIN, g.nutzungsklasse
    assert (g.ist_fluchtweg, g.ist_communal) == (True, True)
    assert g.wohnung_id is None
    for rid in (loch, erschliessung):
        assert [w for w in warnungen if w.startswith(f"loch: {rid} — ")
                and "Messfall S4c/S3b" in w], (rid, warnungen)
    assert all(w.eingangs_tuer_ids for w in wohnungen), wohnungen


def test_r10_eine_notlicht_regel_zerteilt_keine_wohnung(monkeypatch):
    """G1.3: „(a) darf (b) nicht ändern." Rennweg OG1 ``raum_4``/``raum_5`` im
    Kleinen (``_minimalpaar``): C hinter ``tw`` MIT Blatt, X/Y dahinter, Zimmer
    Z. Nach rohen Türen ist {C, X, Y, Z} EINE Wohnung — gleich, ob die
    Klassenregel X/Y privat oder (hier erzwungen) allgemein liefert. In Runde 9
    zerfiel sie unter L1 in {C} und {Z} (Gate (5) auf OG1)."""
    from notbeleuchtung.raumerkennung import wohnungen as W

    bau = _minimalpaar(False)
    raeume, tueren = bau()
    soll = _wohnungsstand(raeume, bilde_wohnungen(raeume, tueren))
    assert soll[0] == [(("C", "X", "Y", "Z"), ("tw",))], soll

    def alles_allgemein(raeume_, tueren_, ausser=frozenset(), **_):
        for r in raeume_:
            if r.raum_typ in wk.SCOPE_TYPEN and r.id not in ausser:
                r.nutzungsklasse = wk.ALLGEMEIN

    monkeypatch.setattr(W, "_verfeinere_gang_privat", alles_allgemein)
    raeume, tueren = bau()
    w = bilde_wohnungen(raeume, tueren)
    assert {r.id: r.nutzungsklasse for r in raeume if r.id in "XY"} == {
        "X": wk.ALLGEMEIN, "Y": wk.ALLGEMEIN}, "Vorbedingung"
    assert _wohnungsstand(raeume, w) == soll


@pytest.mark.parametrize("bau,privat,gruppen", [
    (_minimalpaar(False), {"C", "X", "Y"}, [["C", "X", "Y", "Z"]]),
    (_o3, {"V1", "V2", "Y"}, [["V1", "V2", "Y", "Z1", "Z2", "ZY"], ["Z0"]]),
    (_u1, {"v0", "v1", "g1"}, [["g1", "v0", "v1", "z", "z0"]]),
    (_topologie_l("GANG", "GANG"), {"V1", "V2"}, [["V1", "V2", "Z"], ["Z2"]]),
], ids=["og1_paar", "o3", "u1", "topologie_l"])
def test_r10_beleg_vor_tiebreak(bau, privat, gruppen):
    """G2 (Owner 2026-09-22): „physischer Beleg (Wohnungseingang mit Türblatt,
    Ankerregel bestätigt alle strittigen Räume ausnahmslos und lässt keinen
    offen) geht vor dem Fixpunkt-Tiebreak. … Das deckt OG1 raum_4/5." Die
    strittigen Räume haben zwei Fixpunkte (allgemein / privat); der private
    ist voll ankerbestätigt → er gilt: Klasse privat, bestätigt, und weil
    hinter dem Wohnungseingang ein Zimmer liegt (G4), entzogen. Keine
    tiebreak-Zeile. Runde 9 (L1) lieferte hier überall „allgemein"."""
    raeume, tueren = bau()
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    by_id = {r.id: r for r in raeume}
    for rid in privat:
        assert by_id[rid].nutzungsklasse == wk.PRIVAT, rid
        assert (by_id[rid].ist_fluchtweg, by_id[rid].ist_communal) == (False, False), rid
    assert wk.bestaetigt_privat(raeume, tueren) == privat
    assert sorted(sorted(w.raum_ids) for w in wohnungen) == gruppen
    assert not [w for w in warnungen if w.startswith("tiebreak:")], warnungen


def test_r10_ohne_vollen_beleg_gilt_der_tiebreak():
    """G2, Gegenprobe (Mollgasse EG ``raum_57``/``raum_29``, ``_minimalpaar``
    mit Y über eine blattlose Öffnung erreichbar): X ist ankerprivat, aber ein
    privater Fixpunkt hielte X nur mit Y privat, und Y ist nicht
    ankerbestätigt. Kein voller Beleg → der Tiebreak entscheidet: allgemein,
    Flags 11 — und dafür steht eine Berichtszeile mit Grund (G2)."""
    raeume, tueren = _minimalpaar(True)()
    warnungen: list[str] = []
    bilde_wohnungen(raeume, tueren, warnungen)
    by_id = {r.id: r for r in raeume}
    for rid in ("X", "Y"):
        assert by_id[rid].nutzungsklasse == wk.ALLGEMEIN, rid
        assert (by_id[rid].ist_fluchtweg, by_id[rid].ist_communal) == (True, True)
    assert wk.bestaetigt_privat(raeume, tueren) == {"C"}
    zeile = [w for w in warnungen if w.startswith("tiebreak: X — ")]
    assert len(zeile) == 1, warnungen
    assert "Board 4" in zeile[0] and "Notlicht bleibt" in zeile[0], zeile[0]


def test_r10_beleg_je_gruppe():
    """G2: „Ankerregel bestätigt alle strittigen Räume ausnahmslos" gilt je
    Gruppe benachbarter Räume — ein unbelegter Rest an ANDERER Stelle des
    Plans nimmt dem OG1-Paar den Beleg nicht. X/Y wie allein privat und
    entzogen; bG0/bG1 allgemein mit tiebreak-Zeile, Notlicht bleibt. Bis zur
    Trennung je Gruppe (Runde 10) prüfte die Probe alle strittigen Räume
    gemeinsam und gab X/Y den Tiebreak (allgemein)."""
    raeume, tueren = _zwei_gruppen()
    warnungen: list[str] = []
    bilde_wohnungen(raeume, tueren, warnungen)
    by_id = {r.id: r for r in raeume}
    for rid in ("X", "Y"):
        assert by_id[rid].nutzungsklasse == wk.PRIVAT, rid
        assert (by_id[rid].ist_fluchtweg, by_id[rid].ist_communal) == (False, False)
    assert {"X", "Y"} <= wk.bestaetigt_privat(raeume, tueren)
    for rid in ("bG0", "bG1"):
        assert wk.ankerurteil(raeume, tueren)[rid][0] == wk.A_PRIVAT, "Vorbedingung"
        assert by_id[rid].nutzungsklasse == wk.ALLGEMEIN, rid
        assert (by_id[rid].ist_fluchtweg, by_id[rid].ist_communal) == (True, True)
        assert [w for w in warnungen if w.startswith(f"tiebreak: {rid} — ")], warnungen
    assert not [w for w in warnungen if w.startswith(("tiebreak: X ", "tiebreak: Y "))]


@pytest.mark.parametrize("weg", _RIEGEL_WEGE)
def test_r10_riegel_je_weg(weg):
    """G3 (Owner 2026-09-22): „Ein Raum mit Hauseingang, Tür ins Freie oder
    Tür zu einem allgemeinen Nebenraum ist in keinem Schritt PRIVAT, auch
    nicht in Schritt 1 und nicht an der E8-Grenze." Je Weg: Klasse nicht
    privat, beide Flags, kein Entzug."""
    raeume, tueren = _riegel_bau(weg)()
    bilde_wohnungen(raeume, tueren)
    rid = "X" if weg == "tiebreak_nebenraum" else "V"
    r = next(x for x in raeume if x.id == rid)
    assert r.nutzungsklasse != wk.PRIVAT, (weg, r.nutzungsklasse)
    assert (r.ist_fluchtweg, r.ist_communal) == (True, True), weg
    assert rid not in wk.bestaetigt_privat(raeume, tueren), weg
    assert rid not in wk.schritt1(raeume, tueren, wk.kandidaten(raeume, tueren))


@pytest.mark.parametrize("typ,entzug", [
    ("ZIMMER", True), ("WOHNZIMMER", True), ("SCHLAFZIMMER", True), ("KÜCHE", True),
    ("BAD", False), ("WC", False), ("ABSTELLRAUM", False), ("", False)])
def test_r10_entzug_nur_mit_aufenthaltsraum(typ, entzug):
    """G4 (Owner 2026-09-22, UG ``raum_6``): „Notlicht wird nur entzogen, wenn
    hinter dem Wohnungseingang mindestens ein Aufenthaltsraum liegt (Zimmer,
    Wohnzimmer, Schlafzimmer, Küche, Wohnküche). Bad, WC, Abstellraum oder
    untypisierte Räume allein belegen keine Wohnung, dort bleibt Notlicht."
    ``vor`` ist in jedem Fall Schritt 1 privat und ankerbestätigt."""
    raeume, tueren = _hinter_blatt(typ)()
    bilde_wohnungen(raeume, tueren)
    vor = raeume[1]
    assert vor.nutzungsklasse == wk.PRIVAT
    assert wk.ankerurteil(raeume, tueren)["vor"][0] == wk.A_PRIVAT
    assert ("vor" in wk.bestaetigt_privat(raeume, tueren)) == entzug, typ
    assert (vor.ist_fluchtweg, vor.ist_communal) == (not entzug, not entzug), typ


def test_r10_aufenthaltsraum_in_fremder_wohnung_zaehlt_nicht():
    """G4: „hinter dem Wohnungseingang" = in derselben Wohnung nach (b). Ein
    Zimmer in einer anderen Wohnung desselben Stiegenhauses belegt nichts."""
    raeume, tueren = _hinter_blatt("BAD", fremde_wohnung=True)()
    wohnungen = bilde_wohnungen(raeume, tueren)
    assert sorted(sorted(w.raum_ids) for w in wohnungen) == [["vor", "x"], ["zi"]]
    assert "vor" not in wk.bestaetigt_privat(raeume, tueren)
    assert (raeume[1].ist_fluchtweg, raeume[1].ist_communal) == (True, True)


def test_r10_aufenthaltsraeume_stehen_im_kanon():
    """G4: die Typnamen kommen aus ``raumtyp.py`` und sind nicht erfunden.
    „Wohnküche" nennt der Owner, der Kanon kennt sie nicht (gemeldet);
    KINDERZIMMER steht im Kanon und WIRD Aufenthaltsraum (Owner R4,
    2026-09-22) — aber als eigener Slice nach dem Türstapel; in S7 darum
    nicht dabei."""
    from notbeleuchtung.raumerkennung.raumtyp import _TYP_MAP

    kanon = {label for label, _, _ in _TYP_MAP.values()}
    assert wk.AUFENTHALTSRAUM <= kanon, wk.AUFENTHALTSRAUM - kanon
    assert not {"WOHNKÜCHE", "WOHNKUECHE"} & kanon
    assert "KINDERZIMMER" not in wk.AUFENTHALTSRAUM


@pytest.mark.parametrize("bau", _R10_BAUTEN, ids=lambda f: f.__name__.lstrip("_"))
def test_r10_einbahn_idempotent_und_reihenfolge_invariant(bau, monkeypatch):
    """Einbahn (Board 7), Idempotenz und Reihenfolge-Invarianz bleiben — auf
    allen Runde-10-Mustern."""
    from notbeleuchtung.raumerkennung import wohnungen as W

    raeume, tueren = bau()
    w = bilde_wohnungen(raeume, tueren)
    eins = _vollzustand(raeume, tueren, w)
    w = bilde_wohnungen(raeume, tueren)
    assert _vollzustand(raeume, tueren, w) == eins, "nicht idempotent"
    assert len(_stichprobe_reihenfolgen(bau)) == 1

    def falsch(_raeume, tueren_):
        return {t.id: "wohnungseingang" for t in tueren_}

    monkeypatch.setattr(wk, "korrigierte_rollen", falsch)
    monkeypatch.setattr(W, "korrigierte_rollen", falsch, raising=False)
    raeume, tueren = bau()
    w = bilde_wohnungen(raeume, tueren)
    assert _vollzustand(raeume, tueren, w) == eins, "hängt an korrigierten Rollen"


# ── (p) Runde 11: R1 — Loch-GANG zu Einzelräumen (Owner 2026-09-22) ─────────
# „Ein Loch-GANG, hinter dessen rohen Wohnungseingängen NUR Einzelräume liegen
# (jede dahinterliegende Raumgruppe hat genau einen Raum), bildet mit diesen
# Räumen EINE Wohnung; er selbst bleibt für (a) unbestimmt mit Notlicht."
def _og3_loch_gang():
    """Rennweg OG3 ``raum_10`` im Kleinen: GANG L, vom Stiegenhaus über KEINE
    Tür erreichbar (``t5`` führt nach KEIN_RAUM — die echte Eingangsseite ist
    ein Türerkennungsloch), mit vier rohen Wohnungseingängen zu KÜCHE k
    (blattlos, wie ``durchgang_1``), ZIMMER z, BAD b und ABSTELLRAUM a. Jeder
    dieser vier ist für sich allein eine Raumgruppe. Daneben die erschlossene
    Wohnung Y hinter dem Gang G."""
    return ([_r("S", "STIEGENHAUS"), _r("G", "GANG"), _r("Y", "ZIMMER", False),
             _r("L", "GANG"), _r("k", "KÜCHE", False), _r("z", "ZIMMER", False),
             _r("b", "BAD", False), _r("a", "ABSTELLRAUM", False)],
            [_t("ts", "G", "S", "stiegenhaustuer"),
             _t("ty", "G", "Y", "wohnungseingang"),
             _t("t5", "L", wk.KEIN_RAUM),
             _t("d1", "L", "k", "wohnungseingang", blattlos=True),
             _t("t11", "L", "z", "wohnungseingang"),
             _t("t13", "L", "b", "wohnungseingang"),
             _t("t14", "L", "a", "wohnungseingang")])


def _og3_loch_gang_mehrraeumig():
    """Dasselbe, aber hinter dem Wohnungseingang ``t11`` liegt eine Wohnung aus
    ZWEI Räumen (z + z2 über eine rohe Zimmertür) — das Muster von Muthgasse
    ``raum_94``. Eine einzige mehrräumige Gruppe genügt: L bindet nicht."""
    raeume, tueren = _og3_loch_gang()
    raeume.append(_r("z2", "ZIMMER", False))
    tueren.append(_t("tz2", "z", "z2", "zimmertuer"))
    return raeume, tueren


def test_r11_loch_gang_zu_einzelraeumen_bildet_eine_wohnung():
    """R1: hinter den rohen Wohnungseingängen von L liegen NUR Einzelräume →
    L bildet mit ihnen EINE Wohnung {L, a, b, k, z} (wie HEAD auf Rennweg
    OG3: ``raum_1``/``raum_4``/``raum_6``/``raum_7``/``raum_10``). L selbst
    bleibt für (a) unbestimmt mit Notlicht, Flags 11. Dass diese Wohnung
    keinen Eingang hat, ist das Türerkennungsloch ``t5`` — auf HEAD genauso.
    Bis Runde 10 war L Erschließung und die vier Räume wurden vier
    Einraum-Wohnungen (Gate (3) OG3 0 → 4). K4 (Owner 2026-09-30): L ist
    Mitglied dieser Wohnung → Klasse privat statt offen, Notlicht bleibt."""
    raeume, tueren = _og3_loch_gang()
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    by_id = {r.id: r for r in raeume}
    assert by_id["L"].nutzungsklasse == wk.PRIVAT, by_id["L"].nutzungsklasse
    assert (by_id["L"].ist_fluchtweg, by_id["L"].ist_communal) == (True, True)
    assert "L" not in wk.bestaetigt_privat(raeume, tueren)
    assert sorted((sorted(w.raum_ids), sorted(w.eingangs_tuer_ids))
                  for w in wohnungen) == [(["L", "a", "b", "k", "z"], []),
                                          (["Y"], ["ty"])]
    assert by_id["L"].wohnung_id == by_id["k"].wohnung_id is not None
    assert [w for w in warnungen if w.startswith("k4: L — privat")
            and "vorher unbestimmt" in w], warnungen
    loch = [w for w in warnungen if w.startswith("loch: L — ")]
    assert len(loch) == 1 and "Messfall S4c/S3b" in loch[0], warnungen
    assert "Einzelräume" in loch[0], loch[0]


@pytest.mark.parametrize("bau,loch,wohnungen_soll", [
    (_og3_loch_gang_mehrraeumig, "L",
     [["Y"], ["a"], ["b"], ["k"], ["z", "z2"]]),
    (_muth_paar, "G", [["V", "b", "k"], ["z1"]]),
], ids=["og3_mehrraeumig", "muth_raum_94"])
def test_r11_loch_gang_mit_mehrraeumiger_gruppe_bindet_nicht(bau, loch, wohnungen_soll):
    """R1, Gegenprobe: liegt hinter auch nur EINEM rohen Wohnungseingang eine
    mehrräumige Raumgruppe, bleibt der Loch-GANG Erschließung — allgemein,
    keine Wohnung, Flags 11 (Muthgasse E2 ``raum_94``: hinter seinen rohen
    Wohnungseingängen liegen mehrräumige Wohnungen)."""
    raeume, tueren = bau()
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    r = {x.id: x for x in raeume}[loch]
    assert r.nutzungsklasse == wk.ALLGEMEIN, r.nutzungsklasse
    assert r.wohnung_id is None
    assert (r.ist_fluchtweg, r.ist_communal) == (True, True)
    assert sorted(sorted(w.raum_ids) for w in wohnungen) == wohnungen_soll
    assert [w for w in warnungen if w.startswith(f"loch: {loch} — ")
            and "keine Wohnung" in w], warnungen


_R11_BAUTEN = [_og3_loch_gang, _og3_loch_gang_mehrraeumig]


@pytest.mark.parametrize("bau", _R11_BAUTEN, ids=lambda f: f.__name__.lstrip("_"))
def test_r11_einbahn_idempotent_und_reihenfolge_invariant(bau, monkeypatch):
    """R1 ändert nichts an Einbahn (Board 7), Idempotenz, Reihenfolge-Invarianz
    und der Trennung (a)/(b): verfälschte Klassen und Flags ergeben dieselben
    Wohnungen (R1 liest reine Topologie der rohen Türen)."""
    import random

    raeume, tueren = bau()
    w = bilde_wohnungen(raeume, tueren)
    eins = _vollzustand(raeume, tueren, w)
    soll = _wohnungsstand(raeume, w)
    assert _vollzustand(raeume, tueren, bilde_wohnungen(raeume, tueren)) == eins
    assert len(_stichprobe_reihenfolgen(bau)) == 1
    for seed in range(6):
        rnd = random.Random(seed)
        raeume, tueren = bau()
        for r in raeume:
            r.nutzungsklasse = rnd.choice([wk.PRIVAT, wk.ALLGEMEIN, wk.NEBENRAUM, None])
            r.ist_fluchtweg = r.ist_communal = rnd.random() < .5
            r.wohnung_id = rnd.choice([None, "top_9"])
        assert _wohnungsstand(raeume, bilde_wohnungen(raeume, tueren)) == soll, seed


def _p3_zeuge():
    """Planer-Entscheid P3 (Reviewer Runde 10, Linse Regel, Hinweis 1), der
    Zeuge aus der eigenen Suche (Seed 3, Topologie 705): ``g1``/``g2`` sind
    ankerprivat (``t7``/``t3``, Wohnungseingang MIT Blatt) und haben mit
    ``g0`` zusammen einen voll ankerbestätigten Fixpunkt. Startete die
    Beleg-Probe die übrigen beweglichen Räume wieder bei ALLGEMEIN statt beim
    erreichten Stand, fiel er zusammen."""
    return ([_r("S", "STIEGENHAUS"), _r("g0", "VORRAUM"), _r("g1", "VORRAUM"),
             _r("g2", "GANG"), _r("z0", "WC", False), _r("z1", "ZIMMER", False),
             _r("z2", "WC", False)],
            [_t("t0", "g1", "z2"),
             _t("t1", "S", "g0", "wohnungseingang", blattlos=True),
             _t("t2", "z0", "z1", "stiegenhaustuer"),
             _t("t3", "g1", "g2", "wohnungseingang"),
             _t("t4", "z0", "S", "wohnungseingang"),
             _t("t5", "S", "z1", "zimmertuer"),
             _t("t6", "z2", "g2", "stiegenhaustuer"),
             _t("t7", "g1", "g0", "wohnungseingang")])


def test_r11_beleg_probe_startet_beim_erreichten_stand():
    """P3: die Beleg-Probe (G2) darf die übrigen beweglichen Räume nicht auf
    ALLGEMEIN zurücksetzen — sonst übersieht sie einen Fixpunkt, den es gibt.
    Hier sind ``g1``/``g2`` ankerprivat und privat ein Fixpunkt; vor der
    Korrektur lieferte die Regel für beide den Tiebreak (allgemein, zwei
    ``tiebreak:``-Zeilen). Die Wohnungen (b) sind in beiden Fällen dieselben,
    und weil in ``top_1`` nur ein WC liegt, entzieht G4 kein Notlicht — die
    Richtung ist sicher."""
    raeume, tueren = _p3_zeuge()
    urteil = wk.ankerurteil(raeume, tueren)
    assert [urteil[r][0] for r in ("g1", "g2")] == [wk.A_PRIVAT] * 2, "Vorbedingung"
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    by_id = {r.id: r for r in raeume}
    for rid in ("g1", "g2"):
        assert by_id[rid].nutzungsklasse == wk.PRIVAT, rid
        assert (by_id[rid].ist_fluchtweg, by_id[rid].ist_communal) == (True, True)
    assert not [w for w in warnungen if w.startswith("tiebreak:")], warnungen
    assert not wk.bestaetigt_privat(raeume, tueren)
    assert sorted((sorted(w.raum_ids), sorted(w.eingangs_tuer_ids))
                  for w in wohnungen) == [(["g1", "g2", "z2"], ["t7"]),
                                          (["z0"], ["t4"]), (["z1"], ["t5"])]


# ── (q) Runde 14: Terminierungszweig „Fixpunkte nicht gesucht" ───────────────
def _ohne_fixpunkt_kein_probelauf():
    """Der dritte Terminierungszweig der Klassen-Iteration: die Beleg-Probe
    (G2) läuft nur bei Fixpunkt des GANZEN Plans (``wohnungen.py``,
    ``ponytail:``-Deckel). Pendelt ein fremder Teil, gilt überall der
    Tiebreak, und die Begründung sagt es — „die Iteration erreicht keinen
    Fixpunkt, kein Probelauf".

    Gefunden mit dem Zufallsgenerator des R13-Reviewers (Seed 24124, 4 Treffer
    in 40 000 Plänen, ``review_regel_r13/fix2.log``), danach auf sechs Räume
    minimiert: ``K`` hängt über einen blattlosen Wohnungseingang am
    Stiegenhaus und pendelt mit ``V1``; ``V2``/``V3`` sind ankerprivat
    (erreichbar nur über ``t3`` mit Türblatt) und bleiben allgemein."""
    return ([_r("S", "STIEGENHAUS"), _r("K", "VORRAUM"), _r("V1", "GANG"),
             _r("V2", "GANG"), _r("V3", "GANG"), _r("Z", "ABSTELLRAUM")],
            [_t("tK", "S", "K", "wohnungseingang", True),
             _t("t1", "K", "V1", "wohnungseingang"),
             _t("t3", "K", "V3", "wohnungseingang"),
             _t("t23", "V2", "V3", "zimmertuer"),
             _t("tZ", "V2", "Z", "zimmertuer")])


def test_r14_ohne_fixpunkt_gilt_der_tiebreak_ohne_probelauf():
    """Der Zweig ist erreichbar, fail-safe und NENNT seinen Grund. Bis Runde 13
    war er in keinem Test: ``grep "kein Probelauf" tests/`` gab 0 Treffer,
    während der Deckel-Zweig (``test_ohne_fixpunkt_im_deckel_wird_alles_
    bewegte_unbestimmt``) und der Pendel-Zweig gedeckt waren."""
    raeume, tueren = _ohne_fixpunkt_kein_probelauf()
    urteil = wk.ankerurteil(raeume, tueren)
    assert [urteil[r][0] for r in ("V2", "V3")] == [wk.A_PRIVAT] * 2, "Vorbedingung"
    warnungen: list[str] = []
    bilde_wohnungen(raeume, tueren, warnungen)
    by_id = {r.id: r for r in raeume}
    # Kein Fixpunkt: K und V1 pendeln und werden unbestimmt (Schritt 3). K4
    # (Owner 2026-09-30): V1 ist Mitglied einer Wohnung ohne Aufenthaltsraum →
    # Aufenthaltsraum-Sperre, bleibt offen; K liegt in keiner und bleibt offen.
    assert [by_id[r].nutzungsklasse for r in ("K", "V1")] == [None, None], \
        {r.id: r.nutzungsklasse for r in raeume}
    assert [w for w in warnungen
            if w.startswith("k4: V1 — offen: G4: kein Aufenthaltsraum")], warnungen
    assert [w for w in warnungen if w.startswith("unbestimmt: V1 — ")
            and "Schritt 3" in w], warnungen
    for rid in ("V2", "V3"):
        assert by_id[rid].nutzungsklasse == wk.ALLGEMEIN, rid
        zeile = [w for w in warnungen if w.startswith(f"tiebreak: {rid} — ")]
        assert len(zeile) == 1, warnungen
        assert "kein Probelauf" in zeile[0], zeile[0]
        assert "Notlicht bleibt" in zeile[0], zeile[0]
    # Fail-safe: der Zweig entzieht nichts.
    for rid in ("K", "V1", "V2", "V3"):
        assert (by_id[rid].ist_fluchtweg, by_id[rid].ist_communal) == (True, True), rid
    assert not wk.bestaetigt_privat(raeume, tueren)


# ── (r) Slice S7c: die Rolle wandert an die äußere Tür ───────────────────────
# Die Topologie ``_s7c_wanderung`` und ``_s7c_flur_und_gang`` stehen in
# Abschnitt (l), weil die E7-Zusicherungen dort sie mitparametrisieren.
@pytest.mark.parametrize("dreh", [False, True], ids=["vor_nach", "gedreht"])
@pytest.mark.parametrize("aussen_detail,soll", [
    (None, "wohnungseingang"),
    ("brandschutztuer", "wohnungseingang"),
    ("stiegenhaustuer", "wohnungseingang"),
    ("balkontuer", "balkontuer"),
], ids=["ohne_rolle", "brandschutz", "stiegenhaustuer", "balkontuer"])
def test_s7c_rolle_wandert_an_die_aeussere_tuer(aussen_detail, soll, dreh):
    """Owner-Regel S7c (2026-09-26), wörtlich: „wird ein Vorraum privat,
    wandert die Rolle Wohnungseingang an die äußere Tür (Vorraum zu
    Stiegenhaus oder allgemeinem Gang). Die innere Tür wird zimmertuer."

    Vor diesem Slice hing die Wanderung an der ROHEN Rolle: nur eine Tür, die
    roh ``zimmertuer`` oder ``wohnungseingang`` war, konnte zum Wohnungseingang
    werden. Die äußere Tür eines privat gewordenen GANGES trägt roh aber
    ``stiegenhaustuer`` (Regel 4 der Türtypisierung: GANG ist im Kanon statisch
    allgemein) oder gar keine Rolle (GANG × GANG) — sie blieb liegen, und
    ``fluchtweg.py`` fand im Obergeschoss keinen Start. Der Fall ist auf den 12
    Prüfplänen gemessen NICHT vorhanden (0 Türen); die Zusicherung hält die
    Regel trotzdem fest, weil sie über die rohe Rolle nichts annehmen darf.

    Die Klassen sind GESETZT. Die Variante ``ohne_rolle`` ist nur so
    erreichbar: ohne vorgesetzte Klassen macht ``bilde_wohnungen`` den äußeren
    GANG hier selbst privat (die rollenlose Tür verbindet ihn nach (b) mit
    ``vor``, die Ankerregel bestätigt ihn über ``t_we``) — dann liegen beide
    Seiten von ``t_out`` in der Wohnung, und nichts wandert (gemessen S7c
    Runde 2, Reviewer-Hinweis 5).

    ``balkontuer`` wandert NIE (Reviewer-Hinweis 1): das Modul zählt die
    Balkontür bewusst weder als Wohnungsgrenze (``wohnungsgruppen``) noch als
    Ausgang; sie bleibt, was sie ist. Auf echten Daten ist der Fall nicht
    erreichbar (``tuer_typisierung`` vergibt ``balkontuer`` nur an BALKON/
    TERRASSE oder AUSSEN, nie an Erschließung) — der Riegel hält ihn fest."""
    raeume, tueren = _s7c_wanderung("GANG", aussen_detail, dreh)
    assert "vor" in wk.bestaetigt_privat(raeume, tueren), "Vorbedingung"
    rollen = wk.korrigierte_rollen(raeume, tueren)
    assert rollen["t_out"] == soll, rollen
    assert rollen["t_in"] == "zimmertuer", rollen
    assert rollen["t_we"] == "wohnungseingang", rollen


@pytest.mark.parametrize("dreh", [False, True], ids=["vor_nach", "gedreht"])
def test_s7c_stiegenhaustuer_des_privaten_vorraums_ist_schon_der_eingang(dreh):
    """Gegenprobe zur anderen Hälfte der Owner-Regel („Vorraum zu
    Stiegenhaus"): dort ist die Wanderung STRUKTURELL schon erledigt.
    ``tuer_typisierung.py`` Regel 3 (STIEGENHAUS × WOHNUNG_PRIVAT) gibt jeder
    Tür STIEGENHAUS ↔ VORRAUM roh ``wohnungseingang``; und trüge sie eine
    andere Rolle, wäre der Vorraum vom Stiegenhaus OHNE Wohnungseingang
    erreichbar und damit nie ankerprivat (``ankerurteil`` → ``A_ALLGEMEIN``),
    also nie in der privaten Menge von ``wohnungsraeume``. Gemessen auf
    Mollgasse 1OG: ``tuer_3``/``tuer_4`` (``raum_35`` ↔ ``raum_2``/``raum_4``)
    sind roh UND korrigiert Wohnungseingänge."""
    raeume, tueren = _s7c_wanderung("GANG", None, dreh)
    assert wk.korrigierte_rollen(raeume, tueren)["t_we"] == "wohnungseingang"
    # Trägt dieselbe Tür roh `stiegenhaustuer`, ist `vor` nicht mehr ankerprivat.
    for t in tueren:
        if t.id == "t_we":
            t.tuer_detail = "stiegenhaustuer"
    assert wk.ankerurteil(raeume, tueren)["vor"][0] == wk.A_ALLGEMEIN
    assert "vor" not in wk.bestaetigt_privat(raeume, tueren)


# ── (s) R1-Erweiterung, Fassung A+C (Owner 2026-09-27): der Wohnungsflur ────
# „§ 7e, R1-Erweiterung: Fassung (A+C). Der gebundene Gang bleibt unbestimmt wie
# der Loch-Gang. Begründung: der Gang gehört zur Wohnung, ist aber kein Beleg
# für eine eigene Wohnung; unbestimmt heißt Notlicht bleibt, und das ist die
# sichere Richtung." A: sein Zugang sind nur Stiegenhaustüren MIT Blatt ohne
# rohen Wohnungseingang; C: unter den Einzelräumen ein Aufenthaltsraum UND ein
# Bad/WC/Abstellraum. Der Loch-Fall (Abschnitt (p)) bleibt, wie er ist.
def _og3_flur():
    """(i) Rennweg OG3 ``raum_10`` seit Slice S3b im Kleinen: ``_og3_loch_gang``,
    aber ``t5`` erreicht das Stiegenhaus — roh ``stiegenhaustuer`` MIT Blatt
    (``tuer_5``, 940 mm). L ist kein Loch mehr; ``t5`` ist sein einziger
    Zugang (A), seine vier rohen Wohnungseingänge führen je zu einem
    Einzelraum, darunter Küche/Zimmer UND Bad/Abstellraum (C). G davor ist ein
    Gang vor EINEM Zimmer — ohne Bad/WC/Abstellraum, er bindet nicht (C)."""
    raeume, tueren = _og3_loch_gang()
    return raeume, [_t("t5", "S", "L", "stiegenhaustuer") if t.id == "t5" else t
                    for t in tueren]


def _og3_flur_anders(name: str, typen=None, t5=None, raeume_dazu=(), tueren_dazu=()):
    """``_og3_flur`` mit genau EINER Abweichung — anderen Raumtypen hinter L
    (dann kann nur C ausschließen), einem anderen ``t5`` oder zusätzlichen
    Türen an L (dann nur A), oder einer Zweiergruppe (Einzelräume)."""
    def bau():
        raeume, tueren = _og3_flur()
        for r in raeume:
            r.raum_typ = (typen or {}).get(r.id, r.raum_typ)
        if t5 is not None:
            tueren = [t5() if t.id == "t5" else t for t in tueren]
        return (raeume + [f() for f in raeume_dazu],
                tueren + [f() for f in tueren_dazu])
    bau.__name__ = f"_og3_flur_{name}"
    return bau


_og3_flur_studios = _og3_flur_anders(
    "studios", typen={"k": "ZIMMER", "b": "ZIMMER", "a": "ZIMMER"})
_og3_flur_nur_nassraeume = _og3_flur_anders("nur_nassraeume", typen={"k": "WC", "z": "BAD"})
_og3_flur_hauseingang = _og3_flur_anders(
    "hauseingang", t5=lambda: _t("t5", "L", wk.AUSSEN, "hauseingang"),
    tueren_dazu=[lambda: _t("tzs", "z", "S", "wohnungseingang", blattlos=True)])
_og3_flur_tuer_ins_freie = _og3_flur_anders(
    "tuer_ins_freie", tueren_dazu=[lambda: _t("tx", "L", wk.AUSSEN)])
_og3_flur_rollenlos_zum_gang = _og3_flur_anders(
    "rollenlos_zum_gang", tueren_dazu=[lambda: _t("tx", "L", "G")])
_og3_flur_rollenlos_untypisiert = _og3_flur_anders(
    "rollenlos_untypisiert", raeume_dazu=[lambda: _r("U", "")],
    tueren_dazu=[lambda: _t("tx", "L", "U")])
_og3_flur_blattlos = _og3_flur_anders(
    "blattlos", t5=lambda: _t("t5", "S", "L", "stiegenhaustuer", blattlos=True))
_og3_flur_zweiergruppe = _og3_flur_anders(
    "zweiergruppe", raeume_dazu=[lambda: _r("z2", "ZIMMER", False)],
    tueren_dazu=[lambda: _t("tz2", "z", "z2", "zimmertuer")])


def _og3_loch_gang_nur_zimmer():
    """(vii) Der Loch-Fall ohne C: ``_og3_loch_gang`` (``t5`` nach KEIN_RAUM —
    rollenlos, also auch ohne A), hinter L aber nur Zimmer. R1 vom 2026-09-22
    bindet ihn; A und C dürfen den Loch-Fall nicht enger machen."""
    raeume, tueren = _og3_loch_gang()
    for r in raeume:
        if r.id in ("k", "b", "a"):
            r.raum_typ = "ZIMMER"
    return raeume, tueren


_GETRENNT = [(("Y",), ("ty",)), (("a",), ("t14",)), (("b",), ("t13",)),
             (("k",), ("d1",)), (("z",), ("t11",))]
_EINE_WOHNUNG = [(("L", "a", "b", "k", "z"), ()), (("Y",), ("ty",))]
#: (b) je Bau: Wohnungen mit ihren Eingängen, wie ``_wohnungsstand`` sie führt.
_R1AC_SOLL = {
    "_og3_flur": _EINE_WOHNUNG,
    "_og3_flur_studios": _GETRENNT,
    "_og3_flur_nur_nassraeume": _GETRENNT,
    "_og3_flur_hauseingang": [(("Y",), ("ty",)), (("a",), ("t14",)), (("b",), ("t13",)),
                              (("k",), ("d1",)), (("z",), ("t11", "tzs"))],
    "_og3_flur_tuer_ins_freie": _GETRENNT,
    "_og3_flur_rollenlos_zum_gang": _GETRENNT,
    "_og3_flur_rollenlos_untypisiert": _GETRENNT,
    "_og3_flur_blattlos": _GETRENNT,
    "_og3_flur_zweiergruppe": [(("Y",), ("ty",)), (("a",), ("t14",)), (("b",), ("t13",)),
                               (("k",), ("d1",)), (("z", "z2"), ("t11",))],
    "_og3_loch_gang": _EINE_WOHNUNG,
    "_og3_loch_gang_nur_zimmer": _EINE_WOHNUNG,
}
_R1AC_GEGENFAELLE = [_og3_flur_studios, _og3_flur_nur_nassraeume, _og3_flur_hauseingang,
                     _og3_flur_tuer_ins_freie, _og3_flur_rollenlos_zum_gang,
                     _og3_flur_rollenlos_untypisiert, _og3_flur_blattlos,
                     _og3_flur_zweiergruppe]
_R1AC_BAUTEN = [_og3_flur, *_R1AC_GEGENFAELLE, _og3_loch_gang, _og3_loch_gang_nur_zimmer]


def test_r1ac_wohnungsflur_hinter_stiegenhaustuer_bildet_eine_wohnung():
    """(i) L ist vom Stiegenhaus über ``t5`` ohne Wohnungseingang erreichbar
    (kein Loch), sein Zugang ist nur diese Stiegenhaustür mit Blatt (A), und
    hinter seinen rohen Wohnungseingängen liegen nur Einzelräume mit Küche/
    Zimmer UND Bad/Abstellraum (C) → EINE Wohnung {L, a, b, k, z} wie auf HEAD
    5ac3e0f (Rennweg OG3 ``{raum_1, raum_4, raum_6, raum_7, raum_10}``) statt
    vier Einraum-Wohnungen. Ohne Eingang: ``t5`` bleibt Stiegenhaustür (Owner,
    Board-Frage 1: nicht (b)).

    (a): L bleibt unbestimmt wie der Loch-Gang — Klasse ``None``, Flags 11,
    nicht entzogen —, mit eigenem Grund („Wohnungsflur hinter
    Stiegenhaustür"), nicht „Ankerregel nicht auswertbar"; dazu eine
    ``r1:``-Zeile, die den Zugang nennt, und keine ``loch:``-Zeile.

    K4 (Owner 2026-09-30, R1-Aussetzung): K4 setzt für L keine Klasse, L
    bleibt unbestimmt; die ``k4:``-Zeile nennt „R1-Flur, Owner 2026-09-30"."""
    raeume, tueren = _og3_flur()
    assert wk.ankerurteil(raeume, tueren)["L"][0] == wk.A_ALLGEMEIN, "Vorbedingung"
    assert "L" not in wk.loch_raeume(raeume, tueren), "Vorbedingung: kein Loch"
    _, in_wohnung, _, r1_gaenge = wk.wohnungszugehoerigkeit(raeume, tueren)
    assert (in_wohnung, r1_gaenge) == (set(), {"L"})
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    by_id = {r.id: r for r in raeume}
    assert _wohnungsstand(raeume, wohnungen)[0] == _R1AC_SOLL["_og3_flur"]
    assert by_id["L"].wohnung_id == by_id["z"].wohnung_id is not None
    assert by_id["L"].nutzungsklasse is None, by_id["L"].nutzungsklasse
    assert (by_id["L"].ist_fluchtweg, by_id["L"].ist_communal) == (True, True)
    assert "L" not in wk.bestaetigt_privat(raeume, tueren)
    assert [w for w in warnungen
            if w.startswith("k4: L — offen: R1-Flur, Owner 2026-09-30")], warnungen
    offen = [w for w in warnungen if w.startswith("unbestimmt: L — ")]
    assert len(offen) == 1, warnungen
    assert "Wohnungsflur hinter Stiegenhaustür" in offen[0], offen[0]
    assert "kein Beleg für eine eigene Wohnung" in offen[0], offen[0]
    assert "Notlicht bleibt" in offen[0] and "nicht auswertbar" not in offen[0], offen[0]
    r1 = [w for w in warnungen if w.startswith("r1: L — ")]
    assert len(r1) == 1, warnungen
    assert "t5" in r1[0] and "nur Einzelräume" in r1[0] and "(R1)" in r1[0], r1[0]
    assert not [w for w in warnungen if w.startswith("loch: L")], warnungen


@pytest.mark.parametrize("bau", _R1AC_GEGENFAELLE, ids=lambda f: f.__name__[len("_og3_flur_"):])
def test_r1ac_gang_bindet_nicht(bau):
    """Gegenfälle, jeder weicht von (i) in genau EINEM Punkt ab:
    (ii) C — ``studios`` (hinter L nur Zimmer, ein Gang vor Studios) und
    ``nur_nassraeume`` (WC/Bad/Abstellraum, kein Aufenthaltsraum; Mollgasse EG
    ``raum_39``); (iii) A — ``hauseingang`` (einziger Zugang ein Hauseingang,
    die Zimmer hängen blattlos am Stiegenhaus; Mollgasse EG ``raum_34``) und
    ``tuer_ins_freie``; (iv) A — eine rollenlose Tür zu einem anderen GANG oder
    zu einem untypisierten Raum (Rennweg UG ``raum_12``); (v) A — ``blattlos``
    (der Zugang ist eine Öffnung ohne Türblatt); (vi) ``zweiergruppe`` (hinter
    ``t11`` eine Wohnung aus zwei Räumen, Muthgasse E2 ``raum_94``). L bleibt
    Erschließung: keine Wohnung, allgemein, Flags 11, keine ``r1:``-Zeile."""
    raeume, tueren = bau()
    assert "L" not in wk.loch_raeume(raeume, tueren), "Vorbedingung: kein Loch"
    assert wk.wohnungszugehoerigkeit(raeume, tueren)[3] == set()
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    r = {x.id: x for x in raeume}["L"]
    assert r.wohnung_id is None
    assert r.nutzungsklasse == wk.ALLGEMEIN, r.nutzungsklasse
    assert (r.ist_fluchtweg, r.ist_communal) == (True, True)
    assert _wohnungsstand(raeume, wohnungen)[0] == _R1AC_SOLL[bau.__name__]
    assert not [w for w in warnungen if w.startswith("r1: ")], warnungen


def test_r1ac_loch_gang_bindet_ohne_a_und_c():
    """(vii) Der Loch-Fall wird durch A und C nicht enger: ein Loch-GANG mit
    nur Zimmern dahinter und rollenlosem ``t5`` nach KEIN_RAUM bindet wie bis
    jetzt (R1 vom 2026-09-22) — unbestimmt, Flags 11, ``loch:``-Zeile mit
    R1-Grund, keine ``r1:``-Zeile. ``_og3_loch_gang`` selbst hält Abschnitt (p)
    fest (``test_r11_loch_gang_zu_einzelraeumen_bildet_eine_wohnung``). K4
    (Owner 2026-09-30): danach Klasse privat als Mitglied, Flags 11."""
    raeume, tueren = _og3_loch_gang_nur_zimmer()
    assert "L" in wk.loch_raeume(raeume, tueren), "Vorbedingung: Loch"
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    r = {x.id: x for x in raeume}["L"]
    assert _wohnungsstand(raeume, wohnungen)[0] == _R1AC_SOLL["_og3_loch_gang_nur_zimmer"]
    assert r.nutzungsklasse == wk.PRIVAT, r.nutzungsklasse
    assert (r.ist_fluchtweg, r.ist_communal) == (True, True)
    loch = [w for w in warnungen if w.startswith("loch: L — ")]
    assert len(loch) == 1 and "Einzelräume" in loch[0], warnungen
    assert not [w for w in warnungen if w.startswith("r1: ")], warnungen


@pytest.mark.parametrize("bau", _R1AC_BAUTEN, ids=lambda f: f.__name__.lstrip("_"))
def test_r1ac_einbahn_idempotent_und_reihenfolge_invariant(bau, monkeypatch):
    """(viii) Reihenfolge-Invarianz (Räume UND Türen), Idempotenz und Einbahn
    (Board 7): verfälschte Klassen, Flags und ``wohnung_id`` und der
    umgedrehte Tiebreak ändern die Wohnungen (b) nicht — sie stehen
    AUSDRÜCKLICH fest (``_R1AC_SOLL``) —, verfälschte korrigierte Rollen
    ändern die Klassen (a) nicht."""
    import random

    from notbeleuchtung.raumerkennung import wohnungen as W

    raeume, tueren = bau()
    w = bilde_wohnungen(raeume, tueren)
    soll = _wohnungsstand(raeume, w)
    assert soll[0] == _R1AC_SOLL[bau.__name__]
    eins = _vollzustand(raeume, tueren, w)
    assert _vollzustand(raeume, tueren, bilde_wohnungen(raeume, tueren)) == eins
    assert len(_stichprobe_reihenfolgen(bau)) == 1
    for seed in range(6):
        rnd = random.Random(seed)
        raeume, tueren = bau()
        for r in raeume:
            r.nutzungsklasse = rnd.choice([wk.PRIVAT, wk.ALLGEMEIN, wk.NEBENRAUM, None])
            r.ist_fluchtweg = r.ist_communal = rnd.random() < .5
            r.wohnung_id = rnd.choice([None, "top_9"])
        assert _wohnungsstand(raeume, bilde_wohnungen(raeume, tueren)) == soll, seed

    def falsch(_raeume, tueren_):
        return {t.id: "wohnungseingang" for t in tueren_}

    monkeypatch.setattr(wk, "korrigierte_rollen", falsch)
    monkeypatch.setattr(W, "korrigierte_rollen", falsch, raising=False)
    raeume, tueren = bau()
    assert _vollzustand(raeume, tueren, bilde_wohnungen(raeume, tueren)) == eins
    monkeypatch.setattr(W, "ALLGEMEIN", wk.PRIVAT)
    raeume, tueren = bau()
    assert _wohnungsstand(raeume, bilde_wohnungen(raeume, tueren)) == soll, "Tiebreak umgedreht"


# ── (t) R1-Typfilter (Owner 2026-09-27, § 7e Frage 3 und 4) ─────────────────
# „Vestibül oder Flur hinter einer Wohnungseingangstür zählt nicht als
# Einzelraum. Begründung: derselbe Grundsatz wie beim gebundenen Gang. Ein
# Durchgangsraum ist kein Beleg für eine eigene Wohnung, er erschließt nur."
# „Der Nachbar verliert sein Notlicht nicht. Wenn der gebundene Gang unbestimmt
# bleibt (A+C), bleibt auch sein Nachbar unbestimmt, solange kein eigener Beleg
# vorliegt."
_og3_flur_vorraum = _og3_flur_anders(
    "vorraum", raeume_dazu=[lambda: _r("N", "VORRAUM")],
    tueren_dazu=[lambda: _t("tn", "L", "N", "wohnungseingang")])
_og3_flur_gang = _og3_flur_anders(
    "gang", raeume_dazu=[lambda: _r("N", "GANG")],
    tueren_dazu=[lambda: _t("tn", "L", "N", "wohnungseingang")])


def _og3_loch_gang_vorraum():
    """Der Loch-Fall mit einem VORRAUM N hinter einem rohen Wohnungseingang von
    L: N ist selbst Loch-Raum, hat keine Gruppengröße, L bindet nicht — schon
    ohne Typfilter (§ 6g.5, im Loch-Fall strukturell ohne Wirkung)."""
    raeume, tueren = _og3_loch_gang()
    return (raeume + [_r("N", "VORRAUM")],
            tueren + [_t("tn", "L", "N", "wohnungseingang")])


@pytest.mark.parametrize("bau,loch,soll", [
    (_og3_flur_vorraum, False, sorted([*_GETRENNT, (("N",), ("tn",))])),
    (_og3_flur_gang, False, sorted([*_GETRENNT, (("N",), ("tn",))])),
    (_og3_loch_gang_vorraum, True, _GETRENNT),
], ids=["vorraum_T11", "gang_T27", "loch_vorraum"])
def test_r1_typfilter_vorraum_und_gang_zaehlen_nicht_als_einzelraum(bau, loch, soll,
                                                                    monkeypatch):
    """``_og3_flur`` (A und C erfüllt) mit einem VORRAUM (T11) oder GANG (T27) N
    hinter einem weiteren rohen Wohnungseingang MIT Blatt von L: N ist eine
    Gruppe aus genau einem Raum, zählt aber nicht als Einzelraum — L bindet
    NICHT, keine Wohnung {L, N, …}. Vor dem Filter band L, die gemeinsame
    Wohnung war über Küche/Zimmer G4-belegt, N wurde bestätigt privat und
    verlor sein Notlicht (11 → 00). Jetzt behält N, was er ohne R1 hat: der
    ganze Zustand (Klassen, Flags, Wohnungen, Warnungen) ist der ohne R1, N hat
    Flags 11. Dazu der Loch-Fall mit VORRAUM-Nachbar: bindet nicht."""
    raeume, tueren = bau()
    assert ("L" in wk.loch_raeume(raeume, tueren)) is loch, "Vorbedingung"
    assert wk.wohnungszugehoerigkeit(raeume, tueren)[3] == set()
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    by_id = {r.id: r for r in raeume}
    assert _wohnungsstand(raeume, wohnungen)[0] == soll
    assert by_id["L"].wohnung_id is None
    assert by_id["L"].nutzungsklasse == wk.ALLGEMEIN, by_id["L"].nutzungsklasse
    for rid in ("L", "N"):
        assert (by_id[rid].ist_fluchtweg, by_id[rid].ist_communal) == (True, True), rid
    assert "N" not in wk.bestaetigt_privat(raeume, tueren)
    assert not [w for w in warnungen if w.startswith("r1: ")], warnungen
    assert len(_stichprobe_reihenfolgen(bau)) == 1
    eins = (_vollzustand(raeume, tueren, wohnungen), warnungen)
    monkeypatch.setattr(wk, "_gang_einzelraeume", lambda *_a: set())
    raeume, tueren = bau()
    ohne_r1: list[str] = []
    assert (_vollzustand(raeume, tueren, bilde_wohnungen(raeume, tueren, ohne_r1)),
            ohne_r1) == eins, "wie ohne R1"
