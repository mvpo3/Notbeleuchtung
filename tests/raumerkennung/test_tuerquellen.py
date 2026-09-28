"""Türquellen (Fachteil): Doppelflügel, Außentor-Bögen, Text-Türen, Windfang,
Garagentor-Endausgang, untypisiert_grund."""
from __future__ import annotations

import math

import ezdxf
import pytest
from shapely.geometry import box

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.ausgaenge import leite_ausgaenge
from notbeleuchtung.raumerkennung.dxf_load import DxfPlan
from notbeleuchtung.raumerkennung.tuer_typisierung import typisiere_tueren
from notbeleuchtung.raumerkennung.tuer_zuordnung import aussen_durchgaenge
from notbeleuchtung.raumerkennung.tueren import (
    TuerOeffnung,
    aussentor_tueren,
    text_tueren,
    tuer_oeffnungen,
    tuer_texte,
    verschmelze_doppelfluegel,
)


def _arc_tuer(tid, xy, b):
    return Tuer(id=tid, xy_mm=xy, breite_mm=b, quelle="arc")


# ── (d) Doppelflügel ─────────────────────────────────────────────────────────
def test_doppelfluegel_an_gemeinsamer_wand_wird_eine_tuer():
    wand = [((0.0, 0.0), (10000.0, 0.0))]
    t = verschmelze_doppelfluegel(
        [_arc_tuer("a", (4000.0, 0.0), 900.0), _arc_tuer("b", (5800.0, 0.0), 950.0)],
        wand)
    assert len(t) == 1
    assert t[0].quelle == "doppelfluegel"
    assert t[0].breite_mm == 1850.0
    assert t[0].xy_mm == (4900.0, 0.0)


def test_gegenueberliegende_gangtueren_werden_nicht_verschmolzen():
    # Verbindung senkrecht zur Wand → keine gemeinsame Wand → keine Doppeltür.
    waende = [((0.0, 0.0), (10000.0, 0.0)), ((0.0, 1800.0), (10000.0, 1800.0))]
    t = verschmelze_doppelfluegel(
        [_arc_tuer("a", (4000.0, 0.0), 900.0), _arc_tuer("b", (4000.0, 1800.0), 900.0)],
        waende)
    assert [x.id for x in t] == ["a", "b"]


def _bogen(xy, r, zu, auf):
    """Schwenkbogen am Drehpunkt ``xy``: Blatt geschlossen in Richtung ``zu``,
    offen in Richtung ``auf`` (Grad) — die Endpunkte, die ``tuer_oeffnungen``
    aus dem ARC liest."""
    enden = tuple((xy[0] + r * math.cos(math.radians(w)),
                   xy[1] + r * math.sin(math.radians(w))) for w in (zu, auf))
    return TuerOeffnung(xy_mm=xy, breite_mm=r, winkel_grad=float(zu),
                        quelle="arc", blatt_enden=enden)


def test_echte_doppeltuer_mit_boegen_bleibt_eine_tuer():
    """S4c: beide Blätter schließen zueinander (Drehpunkte an den Enden der
    gemeinsamen Öffnung) → weiter EINE Tür."""
    oeff = [_bogen((4000.0, 0.0), 900.0, 0, 90), _bogen((5800.0, 0.0), 900.0, 180, 90)]
    t = verschmelze_doppelfluegel(
        [_arc_tuer("a", (4000.0, 0.0), 900.0), _arc_tuer("b", (5800.0, 0.0), 900.0)],
        [((0.0, 0.0), (10000.0, 0.0))], oeff)
    assert [(x.quelle, x.breite_mm, x.xy_mm) for x in t] == [
        ("doppelfluegel", 1800.0, (4900.0, 0.0))]


def test_zwei_einzeltueren_nebeneinander_werden_nicht_verschmolzen():
    """S4c, Barawitzka EG ``tuer_14``/``tuer_15`` (KINDERWAGENRAUM | ABSTELLRAUM
    25,67): Abstand = Summe der Radien, Verbindung ∥ Wand — aber beide Blätter
    schließen VONEINANDER WEG. Zwei Öffnungen, keine Doppeltür."""
    oeff = [_bogen((4000.0, 0.0), 900.0, 180, 270), _bogen((5800.0, 0.0), 900.0, 0, 270)]
    t = verschmelze_doppelfluegel(
        [_arc_tuer("a", (4000.0, 0.0), 900.0), _arc_tuer("b", (5800.0, 0.0), 900.0)],
        [((0.0, 0.0), (10000.0, 0.0))], oeff)
    assert [x.id for x in t] == ["a", "b"]


def test_gangtueren_gegenueber_an_der_laibung_werden_nicht_verschmolzen():
    """S4c, Barawitzka EG ``tuer_17``/``tuer_22`` (ABSTELLRAUM 1,98 | ZIMMER
    10,45 über den VORRAUM): die Drehpunkte sitzen an der Laibung, die nächste
    Wandlinie ist die Laibungsfläche QUER zur Wand — sie steht parallel zur
    Verbindung, die Wand-Kollinearität greift nicht. Das Blatt von ``b``
    schließt nicht zu ``a`` hin → zwei Türen."""
    oeff = [_bogen((0.0, 0.0), 830.0, 0, 270), _bogen((0.0, -1660.0), 830.0, 0, 270)]
    laibungen = [((0.0, 0.0), (0.0, 250.0)), ((0.0, -1660.0), (0.0, -1910.0))]
    tueren = [_arc_tuer("a", (0.0, 0.0), 830.0), _arc_tuer("b", (0.0, -1660.0), 830.0)]
    # ohne Bogen-Endpunkte (alte Signatur) verschmilzt das Paar wie bisher
    assert [x.quelle for x in verschmelze_doppelfluegel(list(tueren), laibungen)] == [
        "doppelfluegel"]
    assert [x.id for x in verschmelze_doppelfluegel(tueren, laibungen, oeff)] == ["a", "b"]


def test_tuer_oeffnungen_tragen_die_bogen_endpunkte():
    doc = ezdxf.new()
    msp = doc.modelspace()
    msp.add_arc(center=(1000.0, 0.0), radius=900.0, start_angle=0.0, end_angle=90.0)
    (o,) = tuer_oeffnungen(DxfPlan(doc=doc, space=msp, factor=1.0))
    assert o.quelle == "arc"
    assert [tuple(round(v, 6) for v in p) for p in o.blatt_enden] == [
        (1900.0, 0.0), (1000.0, 900.0)]


# ── Türbögen an der AUSSEN-Grenze ────────────────────────────────────────────
def test_aussentor_aus_bogen_an_der_kontur():
    kontur = box(0, 0, 10000, 10000)
    oeff = [
        TuerOeffnung(xy_mm=(10000.0, 5000.0), breite_mm=900.0,
                     winkel_grad=0.0, quelle="arc"),          # an der Kante
        TuerOeffnung(xy_mm=(5000.0, 5000.0), breite_mm=900.0,
                     winkel_grad=0.0, quelle="arc"),          # innen
    ]
    neu = aussentor_tueren(oeff, [], kontur)
    assert [t.xy_mm for t in neu] == [(10000.0, 5000.0)]
    assert neu[0].quelle == "arc_aussen"
    # eine bestehende Tür deckt die Öffnung → nichts Neues:
    schon = [Tuer(id="t", xy_mm=(10000.0, 5100.0), breite_mm=900.0)]
    assert aussentor_tueren(oeff, schon, kontur) == []


# ── (a) Öffnung in der Außenwand ─────────────────────────────────────────────
def _gang_mit_wandluecke(nase_mm=300.0):
    """Gang 0..6000×0..2000, rundum 600er-Wand; oben eine 1340-mm-Lücke, in
    die der Gang ``nase_mm`` hineinragt (wie Raumpolygone, die in die
    Türöffnung zurückgedehnt sind). S5c/F5: ohne Nase erreicht der freie Teil
    in der 600er-Wand den Raum nicht (Zwischenstück, § 9d), mit 200 mm Nase
    endet er an der Kontur ohne Außenanteil."""
    gang = Raum(id="g", raum_typ="GANG",
                polygon_mm=[(0, 0), (6000, 0), (6000, 2000), (3340, 2000),
                            (3340, 2000 + nase_mm), (2000, 2000 + nase_mm),
                            (2000, 2000), (0, 2000)])
    wand = (box(-600, -600, 6600, 0)
            .union(box(-600, 0, 0, 2600)).union(box(6000, 0, 6600, 2600))
            .union(box(-600, 2000, 2000, 2600)).union(box(3340, 2000, 6600, 2600)))
    return gang, wand, box(-600, -600, 6600, 2600)


def test_aussen_durchgang_allgemeinraum_ohne_tuerblatt():
    """Die Signatur trägt KEIN Geschoss: die Geschossregel für Wandöffnungen
    (»im Obergeschoss ist eine Fassadenlücke ein Fenster«) ist ein eigener
    Concern — Diagnose Z.1271-1274 weist ``aussen_durchgaenge`` dem Slice S5c
    zu. S5c (Owner-Entscheid F5, 2026-09-27) prüft statt eines Geschosses die
    Querung: die Lücke zählt, weil der freie Teil am Gang anliegt und über die
    Kontur hinausreicht (24 % außerhalb)."""
    gang, wand, kontur = _gang_mit_wandluecke()
    neu = aussen_durchgaenge([gang], [], wand, kontur)
    assert len(neu) == 1
    t = neu[0]
    assert t.ohne_tuerblatt and t.nach_raum == "AUSSEN" and t.von_raum == "g"
    assert t.quelle == "oeffnung_aussenwand"
    assert 2000.0 <= t.xy_mm[0] <= 3340.0
    # WOHNUNG-Raum: keine Tür aus der Fensteröffnung.
    zi = Raum(id="z", raum_typ="ZIMMER",
              polygon_mm=[(0, 0), (6000, 0), (6000, 2000), (0, 2000)])
    assert aussen_durchgaenge([zi], [], wand, kontur) == []



def _schmaler_gang(wand_mm, luecke):
    """Gang 1600 × 2000, Seiten und Boden 600er-Wand, oben ``wand_mm``;
    mit ``luecke`` eine 1000-mm-Öffnung mittig in der oberen Wand."""
    oben = (box(0, 2000, 300, 2000 + wand_mm).union(box(1300, 2000, 1600, 2000 + wand_mm))
            if luecke else box(0, 2000, 1600, 2000 + wand_mm))
    wand = (box(-600, -600, 2200, 0).union(box(-600, 0, 0, 2000 + wand_mm))
            .union(box(1600, 0, 2200, 2000 + wand_mm)).union(oben))
    gang = Raum(id="g", raum_typ="GANG",
                polygon_mm=[(0, 0), (1600, 0), (1600, 2000), (0, 2000)])
    return gang, wand, box(-600, -600, 2200, 2000 + wand_mm)


@pytest.mark.parametrize(("luecke", "anzahl"), [
    (True, 1),     # durchgehend: am Raum, 30 % außerhalb der Kontur
    (False, 0),    # geschlossen: Außenstreifen (300 mm vom Raum) + Innenstreifen (0 % außen)
])
def test_aussenoeffnung_quert_die_wand(luecke, anzahl):
    """S5c, Owner-Entscheid F5 (P_A2 wie § 8a): Außenöffnung ist nur, was vom
    Raum durch die Außenwand ins Freie reicht. Vor einer geschlossenen 300er-Wand
    liegen zwei freie Teile — der Außenstreifen erreicht den Raum nicht, der
    Innenstreifen die Außenkante nicht (vorher: der Außenstreifen war Öffnung)."""
    gang, wand, kontur = _schmaler_gang(300, luecke)
    assert len(aussen_durchgaenge([gang], [], wand, kontur)) == anzahl


@pytest.mark.parametrize(("nase_mm", "anzahl"), [
    (200.0, 0),    # endet an der Kontur, 0 % außerhalb (Muster MOLL_EG _10 / raum_51)
    (230.0, 0),    # 7,9 % außerhalb
    (250.0, 1),    # 13,0 % außerhalb
])
def test_aussenanteil_schwelle(nase_mm, anzahl):
    """S5c, Owner-Entscheid F5: zusätzlich ≥ 10 % des freien Teils außerhalb der
    gedeckten Kontur — ein Innenstreifen, der die Kante nur berührt, ist keine
    Öffnung ins Freie."""
    gang, wand, kontur = _gang_mit_wandluecke(nase_mm)
    assert len(aussen_durchgaenge([gang], [], wand, kontur)) == anzahl

# ── (b) Text-Türen + Text-Typisierung ────────────────────────────────────────
def _text_plan(text: str, xy):
    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    msp.add_text(text, dxfattribs={"insert": xy})
    return DxfPlan(doc=doc, space=msp, factor=1.0)


def test_text_tuer_entsteht_nur_ohne_gezeichnete_tuer():
    plan = _text_plan("TÜRSCHLIESSER", (1000, 1000))
    assert tuer_texte(plan) == [("TÜRSCHLIESSER", (1000.0, 1000.0))]
    neu = text_tueren(plan, [])
    assert len(neu) == 1 and neu[0].quelle == "text:TÜRSCHLIESSER"
    schon = [Tuer(id="t", xy_mm=(1400.0, 1000.0), breite_mm=900.0)]
    assert text_tueren(plan, schon) == []


def test_spec_textwoerter_eingang_e1_bst_rwa():
    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    for i, txt in enumerate(("Eingang", "Eingangsbereich", "E1", "E2", "BST",
                             "RWA", "ABSTAND", "BE12")):
        msp.add_text(txt, dxfattribs={"insert": (i * 5000, 0)})
    plan = DxfPlan(doc=doc, space=msp, factor=1.0)
    assert [t for t, _ in tuer_texte(plan)] == [
        "Eingang", "Eingangsbereich", "E1", "E2", "BST", "RWA"]


def test_tuerschliesser_text_macht_hauseingang_im_eg():
    t = Tuer(id="t1", xy_mm=(0.0, 0.0), breite_mm=1100.0,
             von_raum="KEIN_RAUM", nach_raum="AUSSEN", quelle="text:TÜRSCHLIESSER")
    typisiere_tueren([t], [], "EG",
                     tuer_texte=[("TÜRSCHLIESSER", (200.0, 0.0))])
    assert t.tuer_detail == "hauseingang"


def test_notausgang_text_setzt_flag():
    t = Tuer(id="t1", xy_mm=(0.0, 0.0), breite_mm=900.0,
             von_raum="KEIN_RAUM", nach_raum="AUSSEN")
    typisiere_tueren([t], [], "OG1",
                     tuer_texte=[("NOTAUSGANG", (300.0, 0.0))])
    assert t.ist_notausgang


# ── Notausgang-Zusatz auch bei untypisiertem Innenraum ───────────────────────
def test_fluchtwegende_an_aussentuer_untypisierter_raum():
    r = Raum(id="r", raum_typ="", polygon_mm=[(0, 0), (5000, 0), (5000, 5000), (0, 5000)])
    t = Tuer(id="t1", xy_mm=(5000.0, 2500.0), breite_mm=1000.0,
             von_raum="r", nach_raum="AUSSEN")
    typisiere_tueren([t], [r], "EG", fluchtweg_enden=[(4000.0, 2500.0)])
    assert t.ist_notausgang
    aus, _ = leite_ausgaenge([t], [r], "EG")
    assert [a.typ for a in aus] == ["final_exit"]


# ── (c) Windfang ─────────────────────────────────────────────────────────────
def test_windfang_aussentuer_wird_hauseingang():
    wf = Raum(id="wf", raum_typ="GANG", flaeche_m2=5.0,
              polygon_mm=[(0, 0), (2500, 0), (2500, 2000), (0, 2000)])
    innen = Tuer(id="ti", xy_mm=(0.0, 1000.0), von_raum="gang", nach_raum="wf")
    aussen = Tuer(id="ta", xy_mm=(2500.0, 1000.0), von_raum="wf", nach_raum="AUSSEN")
    typisiere_tueren([innen, aussen], [wf], "EG")
    assert aussen.tuer_detail == "hauseingang" and aussen.ist_notausgang
    assert "windfang" in (aussen.quelle or "")
    assert innen.tuer_detail != "hauseingang"


# ── (e) Garagentor ───────────────────────────────────────────────────────────
def test_garagentor_nur_mit_fluchtwegende_endausgang():
    g = Raum(id="g", raum_typ="GARAGE",
             polygon_mm=[(0, 0), (10000, 0), (10000, 10000), (0, 10000)])
    tor = Tuer(id="tor", xy_mm=(10000.0, 5000.0), breite_mm=2500.0,
               von_raum="g", nach_raum="AUSSEN")
    typisiere_tueren([tor], [g], "EG")
    assert tor.tuer_detail == "garagentor"
    ohne, _ = leite_ausgaenge([tor], [g], "EG", fluchtweg_enden=[])
    assert ohne == []
    mit, _ = leite_ausgaenge([tor], [g], "EG",
                             fluchtweg_enden=[(9000.0, 5000.0)])
    assert [a.typ for a in mit] == ["final_exit"]


# ── UG: Kellerausgang ins Freie ist final_exit ───────────────────────────────
def test_ug_notausgangstuer_ins_freie_ist_final_exit():
    t = Tuer(id="t1", xy_mm=(0.0, 0.0), breite_mm=900.0, ist_notausgang=True,
             von_raum="KEIN_RAUM", nach_raum="AUSSEN")
    aus, _ = leite_ausgaenge([t], [], "UG")
    assert [a.typ for a in aus] == ["final_exit"]
    aus_og, _ = leite_ausgaenge([t], [], "OG2")
    assert aus_og == []


# ── (5) untypisiert_grund ────────────────────────────────────────────────────
def test_untypisiert_gruende():
    schacht = Raum(id="s", raum_typ="SCHACHT", polygon_mm=[])
    leer_a = Raum(id="a", raum_typ="", polygon_mm=[])
    leer_b = Raum(id="b", raum_typ="", polygon_mm=[])
    t1 = Tuer(id="t1", xy_mm=(0, 0), von_raum="s", nach_raum="a")
    t2 = Tuer(id="t2", xy_mm=(0, 0), von_raum="KEIN_RAUM", nach_raum="KEIN_RAUM")
    t3 = Tuer(id="t3", xy_mm=(0, 0), von_raum="a", nach_raum="KEIN_RAUM")
    t4 = Tuer(id="t4", xy_mm=(0, 0), von_raum="a", nach_raum="b")
    typisiere_tueren([t1, t2, t3, t4], [schacht, leer_a, leer_b], "EG")
    assert t1.untypisiert_grund == "tuer_in_schacht"
    assert t2.untypisiert_grund == "tuer_ins_nichts"
    assert t3.untypisiert_grund == "kein_nachbarraum"
    assert t4.untypisiert_grund == "beide_seiten_untypisiert"


def test_windfang_mit_drei_tueren():
    # durchgaenge_ohne_tuerblatt hängt eine dritte Tür an den Windfang —
    # die Regel greift trotzdem (genau eine Tür nach AUSSEN).
    wf = Raum(id="wf", raum_typ="GANG", flaeche_m2=5.0,
              polygon_mm=[(0, 0), (2500, 0), (2500, 2000), (0, 2000)])
    innen = Tuer(id="ti", xy_mm=(0.0, 1000.0), von_raum="gang", nach_raum="wf")
    innen2 = Tuer(id="ti2", xy_mm=(1200.0, 0.0), von_raum="wf", nach_raum="gang2")
    aussen = Tuer(id="ta", xy_mm=(2500.0, 1000.0), von_raum="wf", nach_raum="AUSSEN")
    typisiere_tueren([innen, innen2, aussen], [wf], "EG")
    assert aussen.tuer_detail == "hauseingang" and aussen.ist_notausgang
    assert "windfang" in (aussen.quelle or "")


# ── Guard: TERRASSE im geschlossenen Hof ist kein Weg ins Freie ──────────────
def test_terrassentuer_im_geschlossenen_hof_kein_hauseingang():
    """Barawitzka EG: STIEGENHAUS ↔ TERRASSE (im ummauerten Hof). Ohne die
    Hof-Geometrie bleibt es beim Bestandsverhalten (hauseingang), mit ihr
    entfällt der Endausgang."""
    sh = Raum(id="sh", raum_typ="STIEGENHAUS",
              polygon_mm=[(0, 0), (5000, 0), (5000, 5000), (0, 5000)])
    hof = Raum(id="hof", raum_typ="TERRASSE",
               polygon_mm=[(5000, 0), (12000, 0), (12000, 5000), (5000, 5000)])
    def _tuer():
        return Tuer(id="t", xy_mm=(5000.0, 2500.0), breite_mm=1000.0,
                    von_raum="sh", nach_raum="hof")
    ohne = _tuer()
    typisiere_tueren([ohne], [sh, hof], "EG")
    # ZURUECKGEDREHT 2026-09-12: hier stand kurzzeitig `== "balkontuer"`, weil
    # die Freiflaechen-Regel zuerst auch im EG griff. Das war falsch — sie
    # gilt nur ausserhalb des Erdgeschosses (Owner: im EG mit Ausgang ins
    # Gelaende bleiben Freiflaechen moeglich). Die urspruengliche Erwartung
    # ist damit wieder die richtige.
    assert ohne.tuer_detail == "hauseingang"

    mit = _tuer()
    typisiere_tueren([mit], [sh, hof], "EG",
                     kein_weg_ins_freie=box(5000, 0, 12000, 5000))
    assert mit.tuer_detail != "hauseingang"
