"""tuer_zuordnung — von_raum/nach_raum aus Probepunkten beidseits der Sehne."""
from __future__ import annotations

import pytest
from shapely.geometry import Polygon, box

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.tuer_zuordnung import (
    AUSSEN,
    KEIN_RAUM,
    durchgaenge_ohne_tuerblatt,
    ordne_tueren,
)
from notbeleuchtung.raumerkennung.tueren import TuerOeffnung


def _raum(rid, x0, y0, x1, y1, typ="ZIMMER"):
    return Raum(id=rid, raum_typ=typ,
                polygon_mm=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                flaeche_m2=(x1 - x0) * (y1 - y0) / 1e6)


def test_tuer_zwischen_zwei_raeumen():
    # Zwei Räume, Trennwand bei x=5000, Tür in der Wand (Sehne läuft in y).
    raeume = [_raum("a", 0, 0, 4900, 4000), _raum("b", 5100, 0, 10000, 4000)]
    t = Tuer(id="t1", xy_mm=(5000.0, 2000.0), breite_mm=800)
    o = TuerOeffnung(xy_mm=(5000.0, 2000.0), breite_mm=800, winkel_grad=90.0,
                     quelle="block")
    ordne_tueren([t], [o], raeume, box(0, 0, 10000, 4000))
    assert {t.von_raum, t.nach_raum} == {"a", "b"}


def test_aussentuer_und_kein_raum():
    raeume = [_raum("a", 0, 0, 4900, 4000)]
    kontur = Polygon([(0, 0), (5000, 0), (5000, 4000), (0, 4000)])
    t = Tuer(id="t1", xy_mm=(5000.0, 2000.0), breite_mm=900)
    o = TuerOeffnung(xy_mm=(5000.0, 2000.0), breite_mm=900, winkel_grad=90.0,
                     quelle="arc")
    ordne_tueren([t], [o], raeume, kontur)
    assert {t.von_raum, t.nach_raum} == {"a", AUSSEN}
    # Ohne Kontur wird die freie Seite KEIN_RAUM.
    t2 = Tuer(id="t2", xy_mm=(5000.0, 2000.0), breite_mm=900)
    ordne_tueren([t2], [o], raeume, None)
    assert KEIN_RAUM in (t2.von_raum, t2.nach_raum)


def test_durchgang_ohne_tuerblatt():
    # Zwei Räume, Wand bei x=5000..5200 mit 1.2-m-Lücke (y 1400..2600) und
    # KEINER bekannten Tür → Durchgang > 800 mm mit ohne_tuerblatt=True.
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5200, 0, 10000, 4000)]
    wand = box(5000, 0, 5200, 1400).union(box(5000, 2600, 5200, 4000))
    (d,) = durchgaenge_ohne_tuerblatt(raeume, [], wand)
    assert d.ohne_tuerblatt and d.breite_mm > 800
    assert {d.von_raum, d.nach_raum} == {"a", "b"}


@pytest.mark.parametrize(("typ_a", "typ_b", "anzahl"), [
    ("ZIMMER", "SCHACHT", 0),
    ("LIFT", "GANG", 0),       # gestempelter LIFT, KEIN_RAUM auf der a-Seite
    ("ZIMMER", "ZIMMER", 1),   # Gegenprobe: gleiche Kante bleibt Durchgang
])
def test_kein_durchgang_an_kein_raum(typ_a, typ_b, anzahl):
    # Diagnose Rennweg U13, Slice S5a: SCHACHT/LIFT (Klasse KEIN_RAUM) sind
    # nicht begehbar. 200-mm-Wand mit 1,2-m-Lücke, gemeinsame Kante 2 m, keine
    # bekannte Tür; Raum.nutzungsklasse ist an dieser Stelle noch None.
    raeume = [_raum("a", 0, 0, 5000, 4000, typ_a),
              _raum("b", 5200, 1000, 6700, 3000, typ_b)]
    assert all(r.nutzungsklasse is None for r in raeume)
    wand = box(5000, 0, 5200, 1400).union(box(5000, 2600, 5200, 4000))
    assert len(durchgaenge_ohne_tuerblatt(raeume, [], wand)) == anzahl


def test_durchgang_nicht_wo_tuer_ist():
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5200, 0, 10000, 4000)]
    wand = box(5000, 0, 5200, 1400).union(box(5000, 2600, 5200, 4000))
    tuer = Tuer(id="t1", xy_mm=(5100.0, 2000.0), breite_mm=1200)
    assert durchgaenge_ohne_tuerblatt(raeume, [tuer], wand) == []


# ── S4b: schrittweise Seitenprobe (100/200/300/500 mm) ───────────────────────

def _blocktuer(xy, breite=840.0, winkel=90.0):
    """Block-Tür + zugehörige Öffnung an derselben Lage (Sehne aus ``winkel``)."""
    return (Tuer(id="t1", xy_mm=xy, breite_mm=breite, quelle="block"),
            TuerOeffnung(xy_mm=xy, breite_mm=breite, winkel_grad=winkel,
                         quelle="block"))


def test_stufenprobe_findet_raum_hinter_350er_wand():
    """Sehne auf EINER Wandflanke (ArchiCAD-Muster): die feste 300-mm-Probe
    bleibt 50 mm VOR der Gegenflanke in der 350-mm-Wand stecken und liefert
    KEIN_RAUM. Die Stufen 100/200/300/500 finden den zweiten Raum bei 500 mm.

    Ohne Wand-Union gerufen — es geht hier allein um die Stufen, nicht um das
    Überspringen der Wandkörper (dafür der nächste Test).
    """
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5350, 0, 10000, 4000)]
    t, o = _blocktuer((5000.0, 2000.0))
    ordne_tueren([t], [o], raeume, box(0, 0, 10000, 4000))
    assert {t.von_raum, t.nach_raum} == {"a", "b"}


def test_probe_im_wandkoerper_wird_uebersprungen():
    """Punkte IM Wandkörper zählen nicht — auch nicht als AUSSEN.

    Die 600-mm-Wand ragt über die gedeckte Kontur hinaus: ohne das
    Überspringen wäre die Stufe 500 mm „außerhalb der Kontur" und die Seite
    würde AUSSEN. Mit dem Überspringen bleibt sie KEIN_RAUM und wird gemeldet.

    Zugleich die Grenze des Rückfalls auf den eigenen Raum: erreichbar ist NUR
    ``a`` (der Raum, der den Türpunkt deckt), die Gegenseite steckt bis 500 mm
    im Wandkörper. Genau EINE Seite fällt auf ``a`` zurück — nie beide, sonst
    stünde beidseits derselbe Raum; die andere bleibt KEIN_RAUM mit Vermerk.
    """
    raeume = [_raum("a", 0, 0, 5000, 4000)]
    t, o = _blocktuer((5000.0, 2000.0))
    fehlend: list = []
    ordne_tueren([t], [o], raeume, box(0, 0, 5300, 4000),
                 box(5000, 0, 5600, 4000), fehlend)
    assert (t.von_raum, t.nach_raum) == ("a", KEIN_RAUM)
    assert [(x[0].id, x[1]) for x in fehlend] == [("t1", "-")]


def test_eigener_raum_ragt_durch_die_oeffnung():
    """Der Raum, der den TÜRPUNKT deckt, darf nicht beide Seiten gewinnen.

    Gestempelte Raumpolygone ragen durch die Türöffnung (hier 150 mm in die
    350-mm-Wand). Die 100-mm-Stufe der Gegenseite liegt dann noch in ``a`` —
    ohne Überspringen des eigenen Raums stünde beidseits ``a`` (gemessen an
    Barawitzka EG, Mollgasse EG und Muthgasse E2). Gewertet wird erst der
    fremde Raum ``b`` bei 500 mm; die andere Seite fällt auf ``a`` zurück.
    """
    a = Raum(id="a", raum_typ="ZIMMER", flaeche_m2=20.0, polygon_mm=[
        (0, 0), (5000, 0), (5000, 1600), (5150, 1600), (5150, 2400),
        (5000, 2400), (5000, 4000), (0, 4000)])
    raeume = [a, _raum("b", 5350, 0, 10000, 4000)]
    t, o = _blocktuer((5000.0, 2000.0))
    ordne_tueren([t], [o], raeume, box(0, 0, 10000, 4000))
    assert t.von_raum != t.nach_raum, (t.von_raum, t.nach_raum)
    assert {t.von_raum, t.nach_raum} == {"a", "b"}


def test_raum_bei_200_schlaegt_aussen_bei_100():
    """Ein Raum auf einer späteren Stufe schlägt AUSSEN auf einer früheren.

    Begründete Abweichung vom „erste Stufe entscheidet": am Rennweg OG1 liegt
    der 100-mm-Punkt einer Zimmertür knapp außerhalb der gedeckten Kontur und
    20 mm neben dem Raum, der ihn bei 200 mm deckt. Hier nachgebaut als
    20-mm-Kerbe der Kontur genau am 100-mm-Punkt.
    """
    raeume = [_raum("a", 0, 0, 4900, 4000), _raum("b", 5120, 0, 10000, 4000)]
    kontur = box(0, 0, 10000, 4000).difference(box(5090, 1900, 5110, 2100))
    t, o = _blocktuer((5000.0, 2000.0))
    fehlend: list = []
    ordne_tueren([t], [o], raeume, kontur, None, fehlend)
    assert {t.von_raum, t.nach_raum} == {"a", "b"}
    assert fehlend == []


def test_aussen_bleibt_aussen_ohne_vermerk():
    """Freie Fläche außerhalb der gedeckten Kontur bleibt AUSSEN — und AUSSEN
    ist kein fehlender Befund, also kein ``seite_fehlt``-Vermerk."""
    raeume = [_raum("a", 0, 0, 4900, 4000)]
    t, o = _blocktuer((5000.0, 2000.0), breite=900.0)
    fehlend: list = []
    ordne_tueren([t], [o], raeume, box(0, 0, 5000, 4000), None, fehlend)
    assert {t.von_raum, t.nach_raum} == {"a", AUSSEN}
    assert fehlend == []


# ── S4b: Dublette eines Durchgangs zur Block-Tür ─────────────────────────────

def test_dublette_zur_blocktuer_entfaellt():
    """Ein freier Streifen, der die Sehne einer Block-Tür überlappt, IST deren
    Öffnung — auch wenn sein Schwerpunkt weit außerhalb der 600-mm-Regel liegt
    (Rennweg OG1 T04: Streifen 5711 mm lang, Schwerpunkt 1766 mm von der Tür).

    Gegenprobe im selben Wandsegment: die zweite Wandlücke, die die Sehne NICHT
    berührt, bleibt ein Durchgang.
    """
    raeume = [_raum("a", 0, 0, 5000, 8000), _raum("b", 5400, 0, 10000, 8000)]
    wand = (box(5000, 0, 5400, 500).union(box(5000, 4000, 5400, 4500))
            .union(box(5000, 7500, 5400, 8000)))
    t, o = _blocktuer((5000.0, 1000.0))     # Sehne y 580…1420 auf der a-Flanke
    t.von_raum, t.nach_raum = "a", "b"
    durchgaenge = durchgaenge_ohne_tuerblatt(raeume, [t], wand, [o])
    assert len(durchgaenge) == 1, [(d.xy_mm, d.breite_mm) for d in durchgaenge]
    # Der Streifen an der Tür ist 3500 mm lang, sein Schwerpunkt 1266 mm von
    # der Tür entfernt — die 600-mm-Regel allein lässt ihn stehen.
    assert durchgaenge[0].xy_mm[1] > 4000, "die Lücke AN der Tür ist die Dublette"


def test_dublette_nur_bei_gleichem_raumpaar():
    """Ein Streifen, der die Sehne nur streift, aber ein ANDERES Raumpaar
    verbindet, ist keine Dublette der Tür (Rennweg OG1: der Gang-Durchgang
    neben der Zimmertür überlappt deren Sehnenzone zu 1,3 %, die echte
    Dublette zu 70,7 %).
    """
    raeume = [_raum("a", 0, 0, 5000, 6000),
              _raum("b", 5400, 0, 10000, 1400),
              _raum("c", 5400, 1900, 10000, 6000)]
    wand = (box(5000, 0, 5400, 500).union(box(5000, 2800, 5400, 6000))
            .union(box(5400, 1400, 10000, 1900)))   # Trennwand b|c
    t, o = _blocktuer((5000.0, 1300.0))     # Sehne/Zone y 880…1720
    t.von_raum, t.nach_raum = "a", "b"
    durchgaenge = durchgaenge_ohne_tuerblatt(raeume, [t], wand, [o])
    assert [{d.von_raum, d.nach_raum} for d in durchgaenge] == [{"a", "c"}]


def test_sehnen_zone_verschluckt_oeffnung_hinter_pfeiler_nicht():
    """Der Sehnen-Puffer wirkt nur QUER zur Sehne (``cap_style='flat'``).

    400-mm-Wand, Türlücke y 580…1420, dahinter ein 180-mm-Pfeiler und eine
    echte Öffnung von 2000 mm. Rund gepuffert reichte die Sehnenzone 250 mm
    über das Sehnenende hinaus, überlappte die echte Öffnung und löschte sie
    als vermeintliche Dublette.
    """
    raeume = [_raum("a", 0, 0, 5000, 6000), _raum("b", 5400, 0, 10000, 6000)]
    wand = (box(5000, 0, 5400, 580).union(box(5000, 1420, 5400, 1600))
            .union(box(5000, 3600, 5400, 6000)))     # Pfeiler y 1420…1600
    t, o = _blocktuer((5000.0, 1000.0))     # Sehne/Zone y 580…1420
    t.von_raum, t.nach_raum = "a", "b"
    (d,) = durchgaenge_ohne_tuerblatt(raeume, [t], wand, [o])
    assert d.breite_mm == 2000, (d.xy_mm, d.breite_mm)
    assert d.xy_mm[1] > 1600, "die Türlücke selbst ist kein Durchgang"
