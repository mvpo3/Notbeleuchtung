"""kreuzcheck — Fluchtweglinien-Endpunkte ↔ final_exit, beide Richtungen."""
from __future__ import annotations

from shapely.geometry import box

from notbeleuchtung.hauptengine.contracts.raum_modell import (
    Ausgang,
    BBox,
    FluchtwegSegment,
    RaumModell,
    Tuer,
    ZirkulationsGraph,
)
from notbeleuchtung.raumerkennung.kreuzcheck import kreuzcheck

KONTUR = box(0, 0, 20000, 20000)


def _modell(segmente, ausgaenge, tueren=()):
    return RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0, 0), max_xy=(20000, 20000)),
        tueren=list(tueren), ausgaenge=ausgaenge,
        zirkulation=ZirkulationsGraph(segmente=segmente))


def _linie(sid, pts):
    return FluchtwegSegment(segment_id=sid, polyline_mm=pts,
                            laenge_mm=1.0, reason="exit", quelle="LINIE")


def test_endpunkt_an_kante_ohne_exit_gibt_warnung_und_kandidat():
    tuer = Tuer(id="hof", xy_mm=(20000.0, 10500.0), von_raum="r1",
                nach_raum="AUSSEN", quelle="arc_aussen")
    m = _modell([_linie("s1", [(5000.0, 10000.0), (19500.0, 10000.0)])],
                [], [tuer])
    erg = kreuzcheck(m, KONTUR)
    assert erg.endpunkte_aussenkante == [(19500.0, 10000.0)]
    assert len(erg.warnungen) == 1 and "s1" in erg.warnungen[0]
    (k,) = erg.kandidaten
    assert k.typ == "notausgang_kandidat" and k.tuer_id == "hof"


def test_endpunkt_mit_final_exit_ist_gedeckt():
    m = _modell([_linie("s1", [(5000.0, 10000.0), (19500.0, 10000.0)])],
                [Ausgang(id="e1", xy_mm=(20000.0, 10000.0), typ="final_exit")])
    erg = kreuzcheck(m, KONTUR)
    assert erg.gedeckte_endpunkte == [(19500.0, 10000.0)]
    assert not erg.warnungen and not erg.kandidaten
    assert not erg.unbenutzte_exits


def test_endpunkt_weit_von_der_kante_zaehlt_nicht():
    # Mollgasse-Befund: Außenweg-Kanten 2–47 m vom Gebäude sind KEINE
    # Ausgangs-Kandidaten — nur Endpunkte ≤ 1.5 m an der Außenkante zählen.
    m = _modell([_linie("s1", [(5000.0, 10000.0), (10000.0, 10000.0)])], [])
    erg = kreuzcheck(m, KONTUR)
    assert erg.endpunkte_aussenkante == [] and not erg.warnungen


def test_final_exit_ohne_endende_linie_ist_unbenutzt():
    m = _modell([], [Ausgang(id="e1", xy_mm=(0.0, 10000.0), typ="final_exit")])
    erg = kreuzcheck(m, KONTUR)
    assert erg.unbenutzte_exits == ["e1"]
