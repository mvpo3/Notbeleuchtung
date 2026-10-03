"""geschoss — mehrstufige Bestimmung mit Quelle + fail-closed bei UNBEKANNT.

Owner-Entscheidung 2026-09-13: DATEINAME → SCHRIFTFELD/PLANTEXT → HOEHENKOTE →
UNBEKANNT, jede Stufe mit Quelle; bei UNBEKANNT entsteht KEIN ``final_exit``,
sondern die Warnung „Geschoss unbekannt, Endausgang nicht bestimmbar". Kein
Standardwert EG.

Je Stufe steht hier ein Fall, dazu der Leerstring-Fall Muthgasse_E2, der
UNBEKANNT-Fall ohne ``final_exit`` und die Regression, dass ein BELEGTES
Erdgeschoss seinen ``final_exit`` behält.
"""
from __future__ import annotations

import ezdxf

from notbeleuchtung.hauptengine.contracts.raum_modell import Ausgang, Raum, Tuer
from notbeleuchtung.raumerkennung.ausgaenge import (
    leite_ausgaenge,
    ohne_unzulaessige_final_exits,
)
from notbeleuchtung.raumerkennung.dxf_load import DxfPlan
from notbeleuchtung.raumerkennung.geschoss import (
    GESCHOSS_UNBEKANNT_WARNUNG,
    geschoss_aus,
    geschoss_befund,
    geschoss_bekannt,
)
from notbeleuchtung.raumerkennung.tuer_zuordnung import AUSSEN
from plaene import BARAWITZKA_EG, MUTHGASSE_E2, REPO

# Die versionierten Pläne repo-relativ als STRING — hier ist der DATEINAME die
# Messgröße, die Datei selbst wird nicht gelesen.
BARAWITZKA = BARAWITZKA_EG.relative_to(REPO).as_posix()
MUTHGASSE = MUTHGASSE_E2.relative_to(REPO).as_posix()


def _plan(*modelspace_texte: str, layout: str | None = None) -> DxfPlan:
    """Mini-Plan: Texte im Modelspace, optional ein benanntes Layout."""
    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    for t in modelspace_texte:
        msp.add_mtext(t)
    if layout is not None:
        doc.layouts.new(layout)
    return DxfPlan(doc=doc, space=msp, factor=1.0)


# ── Stufe 1: DATEINAME ──────────────────────────────────────────────────────

def test_stufe_dateiname_kuerzel():
    """(a) Die Kürzel von vorher — unverändert, inkl. Owner-Muster BT1-EG."""
    for pfad, erwartet in [
        (BARAWITZKA, "EG"),
        ("Projekte/OG3 - Rennweg 15.dxf", "3OG"),
        ("Projekte/UG - Rennweg 15.dxf", "UG"),
        ("Projekte/20230228_po_1og_V.dxf", "1OG"),
        ("Projekte/415_260415_PP_VA_1_2 -1 KG.dxf", "KG"),
        ("Projekte/BT1-EG.dxf", "EG"),
    ]:
        b = geschoss_befund(None, pfad)
        assert (b.geschoss, b.quelle) == (erwartet, "dateiname"), pfad
        assert b.beleg, "Beleg fehlt"


def test_stufe_dateiname_deutsche_wortform():
    """(b) Wortformen in BEIDEN Schreibweisen — im Repo so gemessen."""
    for stem, erwartet in [
        ("Erdgeschoß", "EG"),                                   # Mollgasse
        ("1.Obergeschoß", "1OG"),
        ("4.Obergeschoß", "4OG"),
        ("2.Kellergeschoß", "2KG"),
        ("Dachgeschoß", "DG"),
        ("Elektromontageplan_Untergeschoß", "UG"),
        ("260320_938-AR-PP-11000-A_ERDGESCHOSS BT1", "EG"),     # Fischamend
        ("260320_938-AR-PP-11010-A_1.OBERGESCHOSS BT1", "1OG"),
        ("Elektromontageapläne_1-OBERGESCHOSS BT1", "1OG"),
    ]:
        b = geschoss_befund(None, f"Projekte/{stem}.dxf")
        assert (b.geschoss, b.quelle) == (erwartet, "dateiname"), stem


def test_dachdraufsicht_ist_kein_geschoss():
    """Eine Dachdraufsicht ist kein Geschoss — sie muss UNBEKANNT bleiben."""
    b = geschoss_befund(None, "Projekte/260320_938-AR-PP-11040-A_DACHDRAUFSICHT BT1.dxf")
    assert (b.geschoss, b.quelle) == ("", "unbekannt")


def test_stufe_dateiname_etage_e2_ist_der_leerstring_fall():
    """(c) Muthgasse E2 — der Fall, der vorher "" ergab.

    ``docs/ENIS_STAND_1_5_0.md:51``: „Geschoss E2 = 2. Obergeschoss".
    """
    b = geschoss_befund(None, MUTHGASSE)
    assert (b.geschoss, b.quelle) == ("2OG", "dateiname")
    assert "E2" in b.beleg
    # Auch der lange Dateiname der Ausführungsplan-Familie:
    lang = "M109B_-Plan - AR-AF-A-GR-E9 100 - GRUNDRISS E9"
    assert geschoss_befund(None, f"Projekte/{lang}.dxf").geschoss == "9OG"


def test_echtes_kuerzel_gewinnt_gegen_projektname_e2():
    """„Baufeld E2" ist ein PROJEKT mit 8 Geschossen (Handoff/LEONIS.md:810) —
    ein Geschoss-Kürzel im selben Namen muss gewinnen."""
    b = geschoss_befund(None, "Projekte/Baufeld_E2_UG.dxf")
    assert (b.geschoss, b.quelle) == ("UG", "dateiname")


def test_stufe_floor_geht_nicht_mehr_verloren():
    """Vorher gemessen: floor="E2" + Dateiname ohne Kürzel ergab ""."""
    b = geschoss_befund("E2", MUTHGASSE)
    assert (b.geschoss, b.quelle) == ("2OG", "floor")
    assert geschoss_befund("OG3", "<fake>").quelle == "floor"


# ── Stufe 2: SCHRIFTFELD ────────────────────────────────────────────────────

def test_stufe_schriftfeld_layoutname():
    """Barawitzka trägt das Geschoss im LAYOUTnamen — Paperspace, den
    ``plan.entities()`` nie sieht."""
    plan = _plan(layout="415_260415_PP_VA_1_3 0 EG")
    b = geschoss_befund(None, "Projekte/ohne_kuerzel.dxf", plan)
    assert (b.geschoss, b.quelle) == ("EG", "schriftfeld")
    assert "Layoutname" in b.beleg


# ── Stufe 3: PLANTEXT ───────────────────────────────────────────────────────

def test_stufe_plantext_mtext():
    plan = _plan("ERDGESCHOSS")
    b = geschoss_befund(None, "Projekte/ohne_kuerzel.dxf", plan)
    assert (b.geschoss, b.quelle) == ("EG", "plantext")


def test_stufe_plantext_zaehlt_nur_die_wortform():
    """Der Mollgasse-Fall: neben dem echten ``ERDGESCHOSS`` stehen Höhenlisten
    anderer Geschosse (``HEIGHT=RBVK OG 01``, ``HEIGHT=RBVK KG``). Nur die
    ausgeschriebene Wortform zählt — das blanke Kürzel ist Rauschen."""
    plan = _plan("HEIGHT=RBVK OG 01", "HEIGHT=RDOK EG", "HEIGHT=EG",
                 "ERDGESCHOSS", "HEIGHT=RBVK KG")
    b = geschoss_befund(None, "Projekte/ohne_kuerzel.dxf", plan)
    assert (b.geschoss, b.quelle) == ("EG", "plantext")
    assert "Wortform" in b.beleg


def test_plantext_blankes_kuerzel_entscheidet_nicht():
    """Nur Höhenlisten, keine Wortform → kein Befund (fail closed).

    GEMESSEN 2026-09-13: mit blankem Kürzel kam der 3. Stock der
    Barawitzka-Serie über ``EG 2×`` als Erdgeschoss heraus.
    """
    plan = _plan("HEIGHT=RBVK OG 01", "HEIGHT=EG", "HEIGHT=RBVK KG")
    assert geschoss_befund(None, "Projekte/o.dxf", plan).quelle == "unbekannt"


# ── Stufe 4: HOEHENKOTE ─────────────────────────────────────────────────────

def test_stufe_hoehenkote_ueber_drei_meter_ist_obergeschoss():
    """Muthgasse-Form ``FOK +7,45`` / ``FBOK +9,05``. Schwelle 3 m =
    Owner-Setzung."""
    plan = _plan("FOK +7,45", "FBOK +9,05", "RDOK +8,87")
    b = geschoss_befund(None, "Projekte/ohne_kuerzel.dxf", plan)
    assert (b.geschoss, b.quelle) == ("OG", "hoehenkote")
    assert "Owner-Setzung" in b.beleg


def test_stufe_hoehenkote_nullnah_ist_KEIN_erdgeschoss_mehr():
    """Früher ``else: geschoss = "EG"`` — der verbotene Standardwert.

    Zwischen den Schwellen ist die Kote kein Befund. Barawitzka ``1 St`` liegt
    mit Median +2,88 m genau dort und ist ein echtes Obergeschoss.
    """
    plan = _plan("FBOK -0,15", "FBOK -0,18", "FBOK -0,20")
    assert geschoss_befund(None, "Projekte/o.dxf", plan).quelle == "unbekannt"


def test_stufe_hoehenkote_tief_ist_keller():
    plan = _plan("FOK -2,80", "RDOK -3,05", "FOK -2,95")
    assert geschoss_befund(None, "Projekte/o.dxf", plan).geschoss == "KG"


def test_hoehenkote_ignoriert_sturzkoten():
    """``STUK`` ist eine Sturzunterkante, keine Geschosshöhe — im Erdgeschoss
    steht sie bei +2,05 m und würde die 3-m-Schwelle verfälschen."""
    plan = _plan("STUK +2,05", "STUK= +11,13")
    assert geschoss_befund(None, "Projekte/o.dxf", plan).quelle == "unbekannt"


def test_reihenfolge_dateiname_vor_plan():
    """Die Stufen sind kurzschlüssig: der Dateiname entscheidet, der Plantext
    kommt nicht mehr dran."""
    plan = _plan("ERDGESCHOSS", "FOK +7,45")
    b = geschoss_befund(None, "Projekte/OG3 - Rennweg 15.dxf", plan)
    assert (b.geschoss, b.quelle) == ("3OG", "dateiname")


# ── Stufe 5: UNBEKANNT + fail-closed ────────────────────────────────────────

def test_stufe_unbekannt_ohne_jede_quelle():
    b = geschoss_befund(None, None)
    assert (b.geschoss, b.quelle) == ("", "unbekannt")
    assert b.beleg == GESCHOSS_UNBEKANNT_WARNUNG
    assert b.unbekannt and not geschoss_bekannt(b.geschoss)


def _haustuer() -> Tuer:
    return Tuer(id="t1", xy_mm=(0.0, 0.0), breite_mm=1500.0,
                von_raum=AUSSEN, nach_raum="gang", tuer_detail="hauseingang")


_RAEUME = [Raum(id="gang", raum_typ="GANG"),
           Raum(id="stgh", raum_typ="STIEGENHAUS")]


def test_fail_closed_unbekanntes_geschoss_erzeugt_keinen_final_exit():
    """Der Kern der Owner-Entscheidung: kein final_exit, dafür die Warnung."""
    out, warn = leite_ausgaenge([_haustuer()], _RAEUME, "")
    assert [a.typ for a in out] == []
    assert any(w.grund == GESCHOSS_UNBEKANNT_WARNUNG for w in warn)


def test_fail_closed_warnung_auch_wenn_ein_stair_exit_bleibt():
    """Die Warnung darf nicht daran hängen, dass GAR kein Ausgang entsteht —
    ein Obergeschoss-Plan ohne erkanntes Geschoss hat stair_exits."""
    tueren = [_haustuer(),
              Tuer(id="t2", xy_mm=(0.0, 0.0), von_raum="gang",
                   nach_raum="stgh", tuer_detail="stiegenhaustuer")]
    out, warn = leite_ausgaenge(tueren, _RAEUME, "")
    assert [a.typ for a in out] == ["stair_exit"]
    assert [w.grund for w in warn] == [GESCHOSS_UNBEKANNT_WARNUNG]


def test_fail_closed_greift_auch_fuer_footprint_ausgaenge():
    """``footprint.hauptausgaenge`` erzeugt final_exit OHNE Geschossbezug
    (``provider.py:102``). Der Filter ist die Stelle, durch die BEIDE Erzeuger
    laufen."""
    aus = [Ausgang(id="exit_1", xy_mm=(0.0, 0.0), typ="final_exit"),
           Ausgang(id="exit_t9", xy_mm=(0.0, 0.0), typ="stair_exit")]
    assert [a.id for a in ohne_unzulaessige_final_exits(aus, "")] == ["exit_t9"]
    assert [a.id for a in ohne_unzulaessige_final_exits(aus, "OG3")] == ["exit_t9"]
    # Belegtes Erdgeschoss/Keller behält seinen Endausgang:
    assert len(ohne_unzulaessige_final_exits(aus, "EG")) == 2
    assert len(ohne_unzulaessige_final_exits(aus, "UG")) == 2


# ── Regression: belegtes Erdgeschoss behält seinen final_exit ───────────────

def test_belegtes_erdgeschoss_behaelt_final_exit():
    out, warn = leite_ausgaenge([_haustuer()], _RAEUME, "EG")
    assert [(a.id, a.typ) for a in out] == [("exit_t1", "final_exit")]
    assert warn == []


def test_geschoss_aus_huelle_bleibt_fuer_bestandsaufrufer():
    """Die alte Schnittstelle bleibt — nur der Leerstring-Fall ist jetzt
    entschieden."""
    assert geschoss_aus("OG3", None) == "3OG"
    assert geschoss_aus(None, "Projekte/OG3 - Rennweg 15.dxf") == "3OG"
    assert geschoss_aus(None, "Erdgeschoss_EG.dxf") == "EG"
    assert geschoss_aus(None, None) == ""
    assert geschoss_aus("E2", MUTHGASSE) == "2OG"


# ── Blocker 1: freier Plankopf-Text erfindet kein Geschoss ──────────────

def _plankopf(layout: str, *texte: str) -> DxfPlan:
    """Plan, dessen Texte im PAPERSPACE-Layout stehen (= Schriftfeld)."""
    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    lay = (doc.layouts.get(layout) if layout in doc.layouts
           else doc.layouts.new(layout))
    for t in texte:
        lay.add_mtext(t)
    return DxfPlan(doc=doc, space=doc.modelspace(), factor=1.0)


def test_plankopf_katastralgemeinde_und_rechtsform_sind_kein_keller():
    """Der Fall Barawitzka 1. Stock — wörtlich aus dem Plan gemessen.

    ``KG.: 01503 Heiligenstadt`` ist die KATASTRALGEMEINDE, ``Toga 2
    Immobilienverwaltungs GmbH & Co KG`` die RECHTSFORM. Beide stehen auf JEDEM
    Blatt der Serie. Vorher machten sie den 1. Stock zu ``KG`` — mit vier
    ``final_exit`` und ohne eine einzige Warnung, während der eigene Plankopf
    desselben Blattes ``1.Stock PP STG1`` sagt. Ein erfundenes Geschoss ist
    schlimmer als UNBEKANNT: es verhindert das fail-closed.
    """
    plan = _plankopf("415_260415_PP_VA_1_4 1 St",
                     "KG.: 01503 Heiligenstadt",
                     "Toga 2 Immobilienverwaltungs GmbH & Co KG",
                     "1.Stock PP STG1")
    b = geschoss_befund(None, "Projekte/415_260415_PP_VA_1_4 1 St.dxf", plan)
    assert b.geschoss == "", f"erfundenes Geschoss {b.geschoss!r}: {b.beleg}"
    assert b.quelle == "unbekannt"


def test_plankopf_wortform_entscheidet_weiter():
    """Die ausgeschriebene Wortform bleibt gültig — nur das BLANKE Kürzel aus
    Fließtext ist raus."""
    plan = _plankopf("Layout1", "Planinhalt:", "Grundriss Erdgeschoss")
    b = geschoss_befund(None, "Projekte/ohne_kuerzel.dxf", plan)
    assert (b.geschoss, b.quelle) == ("EG", "schriftfeld")
    assert "Plankopf-Wortform" in b.beleg


def test_layoutname_darf_das_kuerzel_weiter_tragen():
    """Der Layoutname benennt das BLATT, nicht den Fließtext — Barawitzka EG
    hängt daran."""
    plan = _plankopf("415_260415_PP_VA_1_3 0 EG", "KG.: 01503 Heiligenstadt")
    b = geschoss_befund(None, "Projekte/ohne_kuerzel.dxf", plan)
    assert (b.geschoss, b.quelle) == ("EG", "schriftfeld")
    assert "Layoutname" in b.beleg


# ── Blocker 2: Blätter, die kein Geschoss SIND ──────────────────────

def test_schnitt_lageplan_symbolbibliothek_bleiben_unbekannt():
    """Ein Schnitt, ein Lageplan und eine Symbolbibliothek SIND kein Geschoss.

    Sie tragen den Plankopf ihrer Serie, also lieferten die Plan-Stufen dort
    das Geschoss des PROJEKTS statt des Blattes. Der Plan ist hier absichtlich
    so bestückt, dass ALLE drei Plan-Stufen zuschlagen würden.
    """
    for stem in ["415_260415_PP_VA_RB_2_1 Schn A",
                 "415_260415_PP_VA_1_10 Lageplan",
                 "415_260415_PP_VA_1_9 DD STG1",
                 "Notbeleuchtungssymbole",
                 "Notbeleuchtungspläne-Vorlage",
                 "Baulegende",
                 "20230228_po_dd_V",
                 "260320_938-AR-PP-11040-A_DACHDRAUFSICHT BT1"]:
        plan = _plan("ERDGESCHOSS", "FOK +7,45", "FOK +7,50", "FOK +7,55")
        b = geschoss_befund(None, f"Projekte/{stem}.dxf", plan)
        assert (b.geschoss, b.quelle) == ("", "unbekannt"), stem


def test_echter_grundriss_bleibt_unberuehrt():
    """Der Nicht-Plan-Marker darf keinen echten Grundriss treffen."""
    plan = _plan("ERDGESCHOSS")
    for stem in ["260320_938-AR-PP-11030-A_DACHGESCHOSS BT1",
                 "M109B_-Plan - AR-AF-A-GR-E2 100 - GRUNDRISS E2",
                 "Erdgeschoß", "1.Obergeschoß"]:
        b = geschoss_befund(None, f"Projekte/{stem}.dxf", plan)
        assert b.geschoss, f"{stem} hat sein Geschoss verloren"


# ── MAJOR: kein Standardwert EG aus der Höhenkote ───────────────────

def test_hoehenkote_zwischen_den_schwellen_ist_kein_befund():
    """Barawitzka ``1 St``: Median +2,88 m aus 10 Koten — ein echtes
    Obergeschoss. Vorher fing ``else: geschoss = "EG"`` das als
    ausgangsfähiges Erdgeschoss ab."""
    plan = _plan("FOK +2,88", "FOK +2,90", "FBOK +2,86")
    assert geschoss_befund(None, "Projekte/o.dxf", plan).quelle == "unbekannt"


def test_hoehenkote_urteilt_nicht_bei_einer_einzigen_kote():
    """``…1_9 DD STG1`` (n=1, +18,01 m) und ``…GRUNDRISS DD`` (n=1, +33,53 m)
    wurden von genau EINER Kote entschieden."""
    plan = _plan("FOK +18,01")
    assert geschoss_befund(None, "Projekte/o.dxf", plan).quelle == "unbekannt"


# ── MINOR: EINE Schreibweise ─────────────────────────────────

def test_eine_kanonische_schreibweise_ziffer_vorn():
    """Ziffer VORN — so führen es die Fixtures (``"floor": "1OG"``, ``"4OG"``,
    ``"1KG"``), die Renderer-Tabelle und die API. ``OG1`` wäre die zweite
    Schreibweise für dasselbe Geschoss."""
    assert geschoss_aus(None, "Projekte/OG3 - Rennweg 15.dxf") == "3OG"
    assert geschoss_aus(None, "Projekte/20230228_po_1og_V.dxf") == "1OG"
    assert geschoss_aus(None, "Projekte/1.Obergeschoß.dxf") == "1OG"
    assert geschoss_aus(None, MUTHGASSE) == "2OG"
    assert geschoss_aus(None, "Projekte/2.Kellergeschoß.dxf") == "2KG"
