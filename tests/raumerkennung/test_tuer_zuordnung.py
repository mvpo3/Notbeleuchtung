"""tuer_zuordnung — von_raum/nach_raum aus Probepunkten beidseits der Sehne."""
from __future__ import annotations

import pytest
from shapely.geometry import Polygon, box

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.tuer_zuordnung import (
    _TUER_NAH_MM,
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
    # Slice S5b: die Breite ist das Maß der LÜCKE, nicht mehr die Rechtecklänge
    # des Streifens (die lief mit 4458 mm die ganze Wand ab). Querwände an den
    # Raumenden, damit NUR die Lücke gemessen wird; ohne sie zählen die
    # Stirnkanten mit (eigener Fall: ``test_stirnkante_ohne_querwand``).
    # Gemessen 1198 mm: der Wandverbund wird um ``_KONTAKT_TOL_MM`` GEPUFFERT
    # abgezogen, das kostet an jedem Ende, das an einer Wandflanke liegt, 1 mm.
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5200, 0, 10000, 4000)]
    wand = (box(5000, 0, 5200, 1400).union(box(5000, 2600, 5200, 4000))
            .union(box(4700, -100, 5500, 0)).union(box(4700, 4000, 5500, 4100)))
    (d,) = durchgaenge_ohne_tuerblatt(raeume, [], wand)
    assert d.ohne_tuerblatt and d.breite_mm > 800
    assert {d.von_raum, d.nach_raum} == {"a", "b"}
    assert abs(d.breite_mm - 1198.0) <= 1.0, d.breite_mm


def test_stirnkante_ohne_querwand():
    """Ohne Querwand am Raumende zählt die Stirnkante mit — bekannte Decke.

    Dasselbe Fixture wie ``test_durchgang_ohne_tuerblatt``, nur ohne die
    Querwände: die Kontaktzone ragt über die Raumecken hinaus, und dort liegt
    ein Stück des zur Wand SENKRECHTEN Raumrands frei. Gemessen 1298 mm =
    1200 Lücke + 2 × 49 mm (Kontaktzone 250 − 200 mm Wanddicke, minus dem
    gepufferten Wandabzug). Der Effekt steht hier mit seinem exakten Messwert,
    damit er nicht als Sollwert des Basistests durchgeht.
    """
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5200, 0, 10000, 4000)]
    wand = box(5000, 0, 5200, 1400).union(box(5000, 2600, 5200, 4000))
    (d,) = durchgaenge_ohne_tuerblatt(raeume, [], wand)
    assert abs(d.breite_mm - 1298.0) <= 1.0, d.breite_mm


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
    assert abs(d.breite_mm - 1998.0) <= 1.0, (d.xy_mm, d.breite_mm)
    assert d.xy_mm[1] > 1600, "die Türlücke selbst ist kein Durchgang"


# ── S5b: Querungskriterium (Diagnose U13) ────────────────────────────────────

def test_kein_durchgang_an_wand_ohne_luecke():
    """100-mm-Wand OHNE Lücke → kein Durchgang.

    Die Wand reicht über beide Räume hinaus (so liegt sie im Plan). Die
    Kontaktzone ragt trotzdem 150 mm in jeden Raum; übrig bleiben zwei
    Streifen, die je nur EINEN Raum berühren und zur Gegenseite die volle
    Wanddicke entfernt bleiben. Bis S5b wurde daraus ein Durchgang mit der
    WANDLÄNGE als Breite (Diagnose U13: t = 100/200/240 mm → 4490/4458/4438 mm).
    """
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5100, 0, 10000, 4000)]
    wand = box(5000, -500, 5100, 4500)
    assert durchgaenge_ohne_tuerblatt(raeume, [], wand) == []


def test_durchgang_breite_entlang_der_grenze():
    """900-mm-Lücke in derselben 100-mm-Wand → genau EIN Durchgang, 898 mm.

    Gemessen wird die gemeinsame Grenze (Raumrand im Streifen, ohne
    Wandkörper), nicht das umschließende Rechteck: dessen Langseite ist auch
    hier die ganze Wand (4490 mm). Die Räume sind rundum von Wandkörpern
    begrenzt (Querwände oben/unten) — sonst ragt die Kontaktzone über die
    Raumecken hinaus und die Stirnkanten zählten mit.

    898 statt 900: systematisch −2 · ``_KONTAKT_TOL_MM``, wo die Öffnung an
    Wandflanken endet (gepufferter Wandabzug, je 1 mm pro Ende). Die Schwelle
    ``_DURCHGANG_MIN_MM`` rechnet diesen Verlust heraus.
    """
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5100, 0, 10000, 4000)]
    wand = (box(5000, -500, 5100, 1550).union(box(5000, 2450, 5100, 4500))
            .union(box(4800, -100, 5300, 0)).union(box(4800, 4000, 5300, 4100)))
    (d,) = durchgaenge_ohne_tuerblatt(raeume, [], wand)
    assert {d.von_raum, d.nach_raum} == {"a", "b"}
    assert abs(d.breite_mm - 898.0) <= 1.0, d.breite_mm


def test_splitter_quert_nicht():
    """Ein 2 mm dünner freier Streifen quert nicht (Fläche < Breite ·
    ``_SPLITTER_MM``).

    Das Fixture ist SYNTHETISCH: zwei 498 mm entfernte Räume ohne Wandkörper
    dazwischen, die Kontaktzone bleibt ein 2-mm-Band. Gemessen: Kontakt erfüllt,
    Breite 4002 mm, Fläche 8040,7 mm² < 4002 · 25 mm = 100 050 mm² — also
    Splitter, nicht 800-mm-Regel; Abstand zur Schwelle Faktor 12. Die Absenkung
    von 50 auf 25 mm (Referenz-Übergang O01/O02) rührt daran nicht.

    Die realen 2-mm-Bänder der Diagnose U13 (Rennweg EG KÜCHE 9,27 | MÜLLRAUM
    12,92, Raumabstand 250,0 mm; DG2 ``raum_7`` | ``rest_4``, 108,7 mm) treffen
    das NICHT: dort steht ein Wandkörper, frei bleiben 0,0 bzw. 0,4 mm², und sie
    scheitern schon am Kontaktkriterium.
    """
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5498, 0, 10000, 4000)]
    wand = box(0, -600, 10000, -100)          # Wandkörper nur außen herum
    assert durchgaenge_ohne_tuerblatt(raeume, [], wand) == []


def test_abstandsdeckel_ohne_wandkoerper():
    """Bekannte DECKE der Splitter-Regel — kein Zielbild.

    Sie wirkt als Abstandsdeckel d ≤ 500 − ``_SPLITTER_MM``: fehlt zwischen zwei
    460 mm entfernten Räumen der Wandkörper ganz, quert das 40-mm-Band der
    Kontaktzone über die volle Raumlänge. Gemessen: mit 25 ein Durchgang über
    3998 mm, mit der alten 50 keiner; bei 476 mm Abstand keiner. Fixture wie
    ``test_durchgang_in_dicker_wand_ist_kein_splitter``, ohne den Wandkörper
    dazwischen.
    """
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5460, 0, 10460, 4000)]
    quer = box(4700, -100, 5760, 0).union(box(4700, 4000, 5760, 4100))
    (d,) = durchgaenge_ohne_tuerblatt(raeume, [], quer)
    assert abs(d.breite_mm - 3998.0) <= 1.0, d.breite_mm
    weit = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5476, 0, 10476, 4000)]
    quer_weit = box(4700, -100, 5776, 0).union(box(4700, 4000, 5776, 4100))
    assert durchgaenge_ohne_tuerblatt(weit, [], quer_weit) == []


def test_ueberlappende_raeume_queren_nicht():
    """Überlappende Raumpolygone sind keine Öffnung.

    Begründungsfall HISTORISCH (Diagnose U13, damaliger Stand): DG2 ``raum_7`` |
    ``stiegenhaus_2`` überlappten 2,36 m² → „Öffnung" 5,43 m². Im heutigen Stand
    gibt es am Rennweg kein Raumpaar mit Überlappung > 1 mm² und am DG2 keinen
    ``stiegenhaus_2``; der heutige echte Fall steht in
    ``test_raum_vollstaendig_im_anderen_quert_nicht``.
    """
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 4800, 0, 10000, 4000)]
    wand = box(5000, -500, 5100, 4500)
    assert durchgaenge_ohne_tuerblatt(raeume, [], wand) == []


# ── S5b-Korrektur: Berührungsrauschen und Wandabzug ──────────────────────────

@pytest.mark.parametrize("ueberstand", [0.0, 1e-5])
def test_beruehrende_raeume_sind_eine_oeffnung(ueberstand):
    """Räume, die sich entlang der Öffnung BERÜHREN, geben einen Durchgang.

    Gestempelte Nachbarräume treffen sich auf der Wandmitte: die Schnittfläche
    ist 0 oder ein Sliver aus der Quellpräzision. Der Test ``> 0`` verwarf auf
    vier gemessenen Plänen 23 Raumpaare; 22 davon waren Berührungsrauschen —
    alle unter 0,2 mm² (21 unter 0,06 mm², größter 0,197 mm² bei Muthgasse
    ZIMMER 1,17 ↔ ZIMMER 2,72), 16 davon laut senkrechter Wandsonde
    Wandlücken ≥ 700 mm. 100-mm-Wand auf der gemeinsamen Kante, 1200-mm-Lücke,
    Querwände an den Raumenden; gemessen 1198 mm (je 1 mm Pufferverlust pro
    Wandflanke).
    """
    raeume = [_raum("a", 0, 0, 5000, 4000),
              _raum("b", 5000 - ueberstand, 0, 10000, 4000)]
    ueberlappung = (Polygon(raeume[0].polygon_mm)
                    .intersection(Polygon(raeume[1].polygon_mm)).area)
    assert ueberlappung <= 0.05, ueberlappung
    wand = (box(4950, -500, 5050, 1400).union(box(4950, 2600, 5050, 4500))
            .union(box(4700, -100, 5300, 0)).union(box(4700, 4000, 5300, 4100)))
    (d,) = durchgaenge_ohne_tuerblatt(raeume, [], wand)
    assert {d.von_raum, d.nach_raum} == {"a", "b"}
    assert abs(d.breite_mm - 1198.0) <= 1.0, d.breite_mm


def test_ueberstand_ueber_der_toleranz_quert_nicht():
    """Pinnt ``_UEBERLAPPUNG_TOL_MM2`` nach oben.

    Fixture wie ``test_beruehrende_raeume_sind_eine_oeffnung``, aber mit
    0,01 mm Überstand auf der 4 m langen gemeinsamen Kante: gemessen 40 mm²
    Schnittfläche, 40-fach über der Toleranz — das Raumpaar fällt heraus. Die
    Toleranz darf also nicht beliebig wachsen.
    """
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 4999.99, 0, 10000, 4000)]
    ueberlappung = (Polygon(raeume[0].polygon_mm)
                    .intersection(Polygon(raeume[1].polygon_mm)).area)
    assert abs(ueberlappung - 40.0) <= 0.1, ueberlappung
    wand = (box(4950, -500, 5050, 1400).union(box(4950, 2600, 5050, 4500))
            .union(box(4700, -100, 5300, 0)).union(box(4700, 4000, 5300, 4100)))
    assert durchgaenge_ohne_tuerblatt(raeume, [], wand) == []


def test_raum_vollstaendig_im_anderen_quert_nicht():
    """Ein Raum GANZ in einem anderen ist keine Öffnung (Muthgasse E2: KÜCHE
    2,55 m² liegt vollständig in KÜCHE — der einzige echte Überlappungsfall der
    Ursachenmessung). 2,56 m² Überlappung, sechs Größenordnungen über der
    Toleranz; ohne die Regel ergäbe der Innenrand einen 6400-mm-Durchgang."""
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 1000, 1000, 2600, 2600)]
    wand = box(0, -600, 10000, -100)
    assert durchgaenge_ohne_tuerblatt(raeume, [], wand) == []


@pytest.mark.parametrize("versatz", [1e-6, 0.001, 0.01, 0.1, 0.5])
def test_raumkante_neben_der_wandflanke(versatz):
    """Liegt der Raumrand NEBEN der Wandflanke, misst ``_grenz_breite`` trotzdem
    die Öffnung — nicht den ganzen Raumrand.

    In echten Plänen liegen Raumrand und Wandflanke nur bis auf Quellpräzision
    aufeinander. Genau dafür wird der Wandverbund GEPUFFERT abgezogen:
    ``line.difference(polygon)`` entfernt den Raumrand sonst nur, wenn er exakt
    auf der geschlossenen Wandfläche liegt. Ohne Puffer maß dieselbe Lage
    4000 mm — die volle Rohlänge des Raumrands — und erklärte eine 300-mm-Nische
    zum Durchgang (Diagnose U13, Artefaktklasse).

    Der Puffer ist 1 mm FEST und deckt darum nur Versätze < 1 mm; die Decke
    steht in ``test_raumkante_weiter_als_der_wandpuffer``. Reale Pläne bleiben
    nicht darunter: am Rennweg OG3 (eigener Lauf, Paar WC 1,51 ↔ ZIMMER 45,36)
    liegen 1667 der 1794 gezählten mm 1–3 mm neben dem Wandkörper.

    Zwei Fälle in einer 100-mm-Wand mit Querwänden an den Raumenden: eine
    300-mm-Nische ist KEIN Durchgang, eine 1200-mm-Lücke misst 1198 mm.
    """
    quer = box(4800, -100, 5300, 0).union(box(4800, 4000, 5300, 4100))
    raeume = [_raum("a", 0, 0, 5000 - versatz, 4000),
              _raum("b", 5100 + versatz, 0, 10000, 4000)]
    nische = (box(5000, -500, 5100, 1850).union(box(5000, 2150, 5100, 4500))
              .union(quer))
    assert durchgaenge_ohne_tuerblatt(raeume, [], nische) == []
    luecke = (box(5000, -500, 5100, 1400).union(box(5000, 2600, 5100, 4500))
              .union(quer))
    (d,) = durchgaenge_ohne_tuerblatt(raeume, [], luecke)
    assert abs(d.breite_mm - 1198.0) <= 1.0, d.breite_mm


def test_raumkante_weiter_als_der_wandpuffer():
    """Bekannte DECKE des festen 1-mm-Wandpuffers — kein Zielbild.

    Fixture wie ``test_raumkante_neben_der_wandflanke``, aber der Raumrand liegt
    1,1 mm neben der Wandflanke, also weiter als ``_KONTAKT_TOL_MM`` deckt. Der
    Rand bleibt dann stehen und wird in voller Rohlänge gezählt: die
    300-mm-Nische, die bei 1,0 mm Versatz noch KEIN Durchgang ist, wird zum
    3998-mm-Durchgang (eigener Lauf: 0,5/0,9/1,0 mm → kein Durchgang; 1,1/1,5/
    2,0 mm → 3998 mm). Reale Pläne liegen über dieser Decke — Rennweg OG3, Paar
    WC 1,51 ↔ ZIMMER 45,36: 1667 der 1794 gezählten mm liegen 1–3 mm neben dem
    Wandkörper.
    """
    quer = box(4800, -100, 5300, 0).union(box(4800, 4000, 5300, 4100))
    raeume = [_raum("a", 0, 0, 5000 - 1.1, 4000),
              _raum("b", 5100 + 1.1, 0, 10000, 4000)]
    nische = (box(5000, -500, 5100, 1850).union(box(5000, 2150, 5100, 4500))
              .union(quer))
    (d,) = durchgaenge_ohne_tuerblatt(raeume, [], nische)
    assert abs(d.breite_mm - 3998.0) <= 1.0, d.breite_mm


def test_luecke_genau_an_der_800er_schwelle():
    """Eine 800-mm-Lücke ist ein Durchgang, eine 798-mm-Lücke nicht.

    Der gepufferte Wandabzug kostet jede Öffnung, die an Wandflanken endet,
    systematisch 2 mm. Barawitzka EG KÜCHE ↔ VORRAUM: echte Lücke 800,0 mm,
    gemessen 798,0 → fiel an der rohen 800-mm-Schwelle heraus. Darum vergleicht
    ``durchgaenge_ohne_tuerblatt`` gegen ``_DURCHGANG_MIN_MM − 3 · tol``
    (2 mm Pufferverlust + 1 mm Quellpräzision) statt den Abzug zu entschärfen.

    Fixture wie in ``test_durchgang_breite_entlang_der_grenze`` (Querwände an
    den Raumenden). Gemessenes Fenster: 798,0er-Lücke → keine, 798,9er → keine,
    799er → 797, 800er → 798. Die Gegenprobe steht hier auf der 798er-Lücke,
    weil sie die Schwelle von unten festnagelt: mit 790 mm überlebte jede
    Absenkung bis 789 mm.

    NICHT zugesichert ist der Unterschied −2 vs −3 · tol (das zusätzliche 1 mm
    Quellpräzision): die 799er-Lücke sitzt mit 797,0 < 797,0 auf einem
    Float-Gleichstand. Eine echte 799-mm-Öffnung zählt seit der Absenkung mit —
    darum sagt der Funktions-Docstring „ab 800 mm Nennmaß (gemessen ≥ 797 mm)".
    """
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5100, 0, 10000, 4000)]
    quer = box(4800, -100, 5300, 0).union(box(4800, 4000, 5300, 4100))
    wand = (box(5000, -500, 5100, 1600).union(box(5000, 2400, 5100, 4500))
            .union(quer))
    (d,) = durchgaenge_ohne_tuerblatt(raeume, [], wand)
    assert abs(d.breite_mm - 798.0) <= 1.0, d.breite_mm
    schmal = (box(5000, -500, 5100, 1601).union(box(5000, 2399, 5100, 4500))
              .union(quer))
    assert durchgaenge_ohne_tuerblatt(raeume, [], schmal) == []


def test_800er_tuerluecke_haengt_an_regel_a_b():
    """Eine echte 800-mm-TÜRlücke hält die Breitenschwelle nicht mehr auf.

    Folge der Absenkung 800 → 797: die Lücke einer BEKANNTEN Tür besteht die
    Breitenprüfung jetzt mit 798 mm. Sitzt die Tür am Wandende, läuft der freie
    Streifen die ganze dünne Wand entlang und sein Schwerpunkt liegt weit weg
    (gemessen: y 2906 bei Tür y 800 → 2106 mm) — Regel (a) mit ``_TUER_NAH_MM``
    greift dort nicht. Es hält nur noch Regel (b), die Sehnenzone einer
    Block-Tür MIT Breite.

    Gemessen an diesem Fixture (100-mm-Wand, Raum 6000 mm lang, Lücke
    y 400…1200, Tür in der Lücke): block MIT Breite → [], arc → 798 mm,
    block OHNE Breite → 798 mm.

    Der arc-Zweig ist eine bekannte DECKE, kein Zielbild. Sie ist älter als die
    Schwellenabsenkung: dieselbe Dublette entsteht mit einer 900-mm-Lücke auch
    bei der alten Schwelle (eigener Lauf, 800-mm-Schwelle: 898 mm). Und sie ist
    nicht selten — von den 84 Türen der 8 Rennweg-Pläne haben 30 keine
    Sehnenzone (22 arc, 5 block ohne Breite, 3 Text-Kombinationen). Der
    Ausbaupfad (eigener Slice) ist, Regel (a) gegen die gemessene
    Öffnungskante zu prüfen statt gegen den Schwerpunkt des freien Teils.
    """
    quer = box(4800, -100, 5300, 0).union(box(4800, 6000, 5300, 6100))
    raeume = [_raum("a", 0, 0, 5000, 6000), _raum("b", 5100, 0, 10000, 6000)]
    wand = (box(5000, -500, 5100, 400).union(box(5000, 1200, 5100, 6500))
            .union(quer))
    t, o = _blocktuer((5050.0, 800.0), breite=800.0)
    t.von_raum, t.nach_raum = "a", "b"
    assert durchgaenge_ohne_tuerblatt(raeume, [t], wand, [o]) == []

    arc = Tuer(id="t1", xy_mm=(5050.0, 800.0), breite_mm=800.0, quelle="arc")
    arc.von_raum, arc.nach_raum = "a", "b"
    oa = TuerOeffnung(xy_mm=(5050.0, 800.0), breite_mm=800.0, winkel_grad=90.0,
                      quelle="arc")
    (d,) = durchgaenge_ohne_tuerblatt(raeume, [arc], wand, [oa])
    assert abs(d.breite_mm - 798.0) <= 1.0, d.breite_mm
    assert d.xy_mm[1] - 800.0 > _TUER_NAH_MM, d.xy_mm


def test_durchgang_in_dicker_wand_ist_kein_splitter():
    """Eine 1200-mm-Lücke in einer 460-mm-Wand ist ein Durchgang, kein Splitter.

    Anlass Rennweg OG1, Referenz O01/O02 (VORRAUM 10,94 m² ↔ Wohnküche
    73,06 m²): die Räume stehen 450 mm auseinander, und die Kontaktzone ist bei
    Raumabstand d ein Band der Dicke 2 · ``_KONTAKT_MM`` − d — dort also genau
    50,0 mm, die alte Splitter-Dicke selbst. Gemessen (eigener Lauf, OG1): freier
    Teil 50,0 × 1200,0 mm, Fläche 60 000,0 mm², Breite 1198,06 mm → Schwelle bei
    50 mm wäre 59 903 mm², Reserve 97 mm² = 0,16 %. Der Übergang entsteht dort
    auch mit 50 mm noch (die OG1-Durchgangsliste ist mit 50 und 25 identisch) —
    er hängt nur an 1 mm Breiten-Messrauschen. Die Splitter-Regel trennt
    2-mm-Bänder (siehe ``test_splitter_quert_nicht``) von echten Öffnungen und
    darf nicht so eng an einer echten Öffnung liegen.

    Das Fixture nimmt 460 mm statt der 450 mm des Anlasses: bei 450 mm misst
    ``_grenz_breite`` gepuffert 1198 mm, die Schwelle bei 50 mm läge also bei
    59 900 mm² < 60 000 mm² freier Fläche — der Fall wäre mit 50 mm GRÜN (100 mm²
    Reserve) und taugt nicht als Rot-Beleg. Bei 460 mm ist das Band 40 mm dick,
    die freie Fläche 48 000 mm², die Breite 1198,0 mm — mit 50 mm ein Splitter
    (Schwelle 59 900 mm²), mit 25 mm nicht (29 950 mm²).
    """
    quer = box(4700, -100, 5760, 0).union(box(4700, 4000, 5760, 4100))
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5460, 0, 10460, 4000)]
    wand = (box(5000, -500, 5460, 1400).union(box(5000, 2600, 5460, 4500))
            .union(quer))
    (d,) = durchgaenge_ohne_tuerblatt(raeume, [], wand)
    assert {d.von_raum, d.nach_raum} == {"a", "b"}
    assert abs(d.breite_mm - 1198.0) <= 1.0, d.breite_mm


# ── S4c Fassung A: andere Bogenrichtung nur für verbindungslose Zielräume ─────

def _bogentuer_vor_abstellraum(typ_a="ABSTELLRAUM", id_a="a"):
    """Nachbau Barawitzka EG ``tuer_17`` (Gate § 10b): VORRAUM ``v`` südlich,
    Zielraum ``a`` nördlich einer 200-mm-Wand mit 830er Öffnung (x 1000..1830).
    Drehpunkt an der Laibung (1000, 3000); der ARC läuft 270° → 360°: der
    START zeigt auf das OFFENE Blatt (Süd, frei im VORRAUM), das ENDE liegt als
    geschlossenes Blatt an der Wand (Ost). Die Sehne aus dem Startwinkel legt
    die Normale entlang der Wand → ``v`` | KEIN_RAUM."""
    raeume = [_raum("v", 0, 0, 4000, 3000, "VORRAUM"),
              _raum(id_a, 0, 3200, 1500, 5000, typ_a)]
    wand = box(0, 3000, 1000, 3200).union(box(1830, 3000, 4000, 3200))
    kontur = box(0, 0, 4000, 5000)
    t = Tuer(id="t1", xy_mm=(1000.0, 3000.0), breite_mm=830, quelle="arc")
    o = TuerOeffnung(xy_mm=(1000.0, 3000.0), breite_mm=830, winkel_grad=270.0,
                     quelle="arc", blatt_enden=((1000.0, 2170.0), (1830.0, 3000.0)))
    ordne_tueren([t], [o], raeume, kontur, wand)
    assert sorted((t.von_raum, t.nach_raum)) == sorted(("v", KEIN_RAUM))
    return t, o, raeume, kontur, wand


def test_andere_bogenrichtung_verbindet_verbindungslosen_raum():
    """Gate (10): bleibt eine Seite KEIN_RAUM und wäre der Raum hinter der
    Tür sonst ohne jede Verbindung, gilt die Sehne aus dem ENDwinkel — die
    zugeordnete Seite ``v`` bleibt, ``a`` kommt dazu."""
    from notbeleuchtung.raumerkennung.tuer_zuordnung import andere_bogenrichtung

    t, o, raeume, kontur, wand = _bogentuer_vor_abstellraum()
    assert andere_bogenrichtung([t], [o], raeume, kontur, wand) == [t]
    assert sorted((t.von_raum, t.nach_raum)) == ["a", "v"]


def test_andere_bogenrichtung_nicht_wenn_zielraum_verbunden():
    """Hat ``a`` schon irgendeine Verbindung, bleibt die Tür, wie sie ist —
    die Regel füllt nur Lücken, sie korrigiert die Sehne nicht allgemein."""
    from notbeleuchtung.raumerkennung.tuer_zuordnung import andere_bogenrichtung

    t, o, raeume, kontur, wand = _bogentuer_vor_abstellraum()
    andere = Tuer(id="t2", xy_mm=(200.0, 3100.0), breite_mm=800,
                  von_raum="a", nach_raum="v")
    assert andere_bogenrichtung([t, andere], [o], raeume, kontur, wand) == []
    assert sorted((t.von_raum, t.nach_raum)) == sorted(("v", KEIN_RAUM))


@pytest.mark.parametrize(("typ_a", "id_a"), [("SCHACHT", "a"), ("", "rest_1")])
def test_andere_bogenrichtung_nicht_in_schacht_oder_untypisierten_rest(typ_a, id_a):
    """SCHACHT (nicht begehbar) und untypisierte ``rest``-Flächen sind keine
    Zielseite, auch wenn sie verbindungslos sind."""
    from notbeleuchtung.raumerkennung.tuer_zuordnung import andere_bogenrichtung

    t, o, raeume, kontur, wand = _bogentuer_vor_abstellraum(typ_a, id_a)
    assert andere_bogenrichtung([t], [o], raeume, kontur, wand) == []
    assert sorted((t.von_raum, t.nach_raum)) == sorted(("v", KEIN_RAUM))
