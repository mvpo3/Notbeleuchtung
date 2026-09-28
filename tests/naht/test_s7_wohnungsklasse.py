"""Naht-Tests zu S7a+S7b (docs/GATE_TUERSTAPEL.md § 6g) auf echten Plänen.

(d) Reihenfolge-Invarianz: permutierte Raum- UND Türliste liefert dieselben
    Klassen, Wohnungsgruppen, Türrollen, Flags und Segmente — auf Plänen, auf
    denen ein Kandidat wirklich kippt (Rennweg OG1, Barawitzka EG,
    Mollgasse 1OG), und nicht nur unter ``reverse()``.

    Die Läufe setzen an der ECHTEN Produktionseingabe an: ``_eingabe`` greift
    Raum- und Türliste VOR ``bilde_wohnungen`` ab. (Bis Runde 6 hätte ein Lauf
    auf dem fertigen Modell die schon korrigierten Türrollen recycelt; seit E7
    trägt das Modell die rohen Rollen — der Abgriff bleibt, weil er auch
    ``leite_ausgaenge`` und ``fluchtwege`` permutiert fährt.)

(e) Stabilität: kein Kandidat wird mit einer Klasse ausgeliefert, die eine
    Nachrechnung auf dem ausgelieferten Modell widerlegt (§ 6g Schritt 3).

(f) Naht-Zusicherungen: Rennweg UG KINDERWAGENRAUM behält seinen Weg, OG1
    hat weniger als zwei Einraum-Wohnungen, und in keinem Regelgeschoß liegt
    ein Anker in einem Raum der Nutzungsklasse WOHNUNG_PRIVAT.

(g) Die vier Messfälle aus § 6g in der Zählweise, in der § 6g sie definiert
    hat (Stützpunkt im Raumpolygon, nicht Start/Ziel-Zuordnung).
"""
from __future__ import annotations

import copy
import random

import pytest
from shapely.geometry import Point, Polygon

from notbeleuchtung.raumerkennung.fluchtweg import fluchtwege
from notbeleuchtung.raumerkennung.wohnungen import bilde_wohnungen
from notbeleuchtung.raumerkennung.wohnungsklasse import klassifiziere
from plaene import (
    BARAWITZKA_EG,
    MOLLGASSE_1OG,
    MOLLGASSE_EG,
    RENNWEG_DD,
    RENNWEG_DG1,
    RENNWEG_DG2,
    RENNWEG_EG,
    RENNWEG_OG1,
    RENNWEG_OG2,
    RENNWEG_OG3,
    RENNWEG_UG,
    plan,
)


def _eingabe(pfad, floor):
    """``(provider, modell, eingabe)`` — ``eingabe`` trägt alles, was die Kette
    AB ``bilde_wohnungen`` braucht, abgegriffen im Produktionspfad.

    Befund B6: Runde 3 griff nur Räume und Türen ab und reichte ``ausgaenge``
    aus dem UNPERMUTIERTEN Lauf weiter. Damit war ``fluchtwege`` per
    Konstruktion gegen jede Reihenfolgewirkung aus ``leite_ausgaenge``
    geschützt und das grüne Feld „segmente" belegte keine Segment-Invarianz
    des Produktionspfads. Jetzt läuft die ganze Kette permutiert; dazu
    gehören ``hauptausgaenge`` (die Basis des Dedups) und ``flw_enden``."""
    plan(pfad)
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider
    from notbeleuchtung.raumerkennung import provider as P

    eingabe: dict = {}
    echt = {n: getattr(P, n) for n in
            ("hauptausgaenge", "bilde_wohnungen", "leite_ausgaenge", "fluchtwege")}

    def spion_ha(plan_, bounds):
        aus = echt["hauptausgaenge"](plan_, bounds)
        eingabe["ausgaenge_basis"] = copy.deepcopy(aus)
        return aus

    def spion_bw(raeume, tueren, warnungen=None):
        eingabe["raeume"] = copy.deepcopy(raeume)
        eingabe["tueren"] = copy.deepcopy(tueren)
        return echt["bilde_wohnungen"](raeume, tueren, warnungen)

    def spion_la(tueren, raeume, geschoss, flw_enden):
        eingabe["geschoss"] = geschoss
        eingabe["flw_enden"] = copy.deepcopy(flw_enden)
        return echt["leite_ausgaenge"](tueren, raeume, geschoss, flw_enden)

    def spion_fw(raeume, tueren, ausgaenge, bisher, geschoss="",
                 warnungen=None, durchleitung=None):
        eingabe["ausgaenge"] = copy.deepcopy(ausgaenge)
        eingabe["bisher"] = copy.deepcopy(bisher)
        eingabe["geschoss"] = geschoss
        return echt["fluchtwege"](raeume, tueren, ausgaenge, bisher, geschoss,
                                  warnungen, durchleitung)

    P.hauptausgaenge, P.bilde_wohnungen = spion_ha, spion_bw
    P.leite_ausgaenge, P.fluchtwege = spion_la, spion_fw
    try:
        prov = ArchitekturRaumProvider()
        modell = prov.parse(str(pfad), floor)
    finally:
        for n, f in echt.items():
            setattr(P, n, f)
    return prov, modell, eingabe


@pytest.fixture(scope="module")
def og1():
    return _eingabe(RENNWEG_OG1, "OG1")


@pytest.fixture(scope="module")
def ug():
    return _eingabe(RENNWEG_UG, "UG")


@pytest.fixture(scope="module")
def bara():
    return _eingabe(BARAWITZKA_EG, "EG")


@pytest.fixture(scope="module")
def moll1og():
    return _eingabe(MOLLGASSE_1OG, "1OG")


@pytest.fixture(scope="module")
def og2():
    return _eingabe(RENNWEG_OG2, "OG2")


@pytest.fixture(scope="module")
def og3():
    return _eingabe(RENNWEG_OG3, "OG3")


@pytest.fixture(scope="module")
def dg1():
    return _eingabe(RENNWEG_DG1, "DG1")


@pytest.fixture(scope="module")
def dg2():
    return _eingabe(RENNWEG_DG2, "DG2")


@pytest.fixture(scope="module")
def eg():
    return _eingabe(RENNWEG_EG, "EG")


@pytest.fixture(scope="module")
def dd():
    return _eingabe(RENNWEG_DD, "DD")


@pytest.fixture(scope="module")
def moll_eg():
    return _eingabe(MOLLGASSE_EG, "EG")


def anker_in_privat(modell) -> list[str]:
    """Anker, deren Punkt ECHT in einem WOHNUNG_PRIVAT-Raum liegt (gleiche
    Zählweise wie tests/gate/gate_og3.py, Gate-Bedingung (6))."""
    privat = [Polygon(r.polygon_mm) for r in modell.raeume
              if r.nutzungsklasse == "WOHNUNG_PRIVAT" and len(r.polygon_mm) >= 3]
    return [a.id for a in modell.anker
            if any(p.contains(Point(a.xy_mm)) for p in privat)]


def anker_in_entzug(modell) -> list[str]:
    """Anker in einem Raum, dem der Fail-Safe-Riegel das Notlicht ENTZOGEN hat
    (``bestaetigt_privat``). Das ist die Zusicherung von R4: wer seine Leuchten
    verliert, verliert auch seine Anker — und nur er. Ein Raum, der trotz
    Klasse WOHNUNG_PRIVAT sein Notlicht behält (Ankerregel bestätigt nicht),
    SOLL seine Anker behalten."""
    from notbeleuchtung.raumerkennung.wohnungsklasse import bestaetigt_privat

    entzug = bestaetigt_privat(modell.raeume, modell.tueren)
    polys = [Polygon(r.polygon_mm) for r in modell.raeume
             if r.id in entzug and len(r.polygon_mm) >= 3]
    return [a.id for a in modell.anker
            if any(p.contains(Point(a.xy_mm)) for p in polys)]


def fremde_anker_in_privat(modell) -> list[str]:
    """Anker, deren Punkt in einem PRIVAT GEWORDENEN Raum liegt (GANG/VORRAUM
    der Klasse WOHNUNG_PRIVAT — nur deren Klasse ändert S7), der NICHT ihr
    eigener ist (``raum_id``) — die B2-Zählweise. Anker in Zimmern/Bädern
    lagen dort schon auf HEAD 5ac3e0f (DG1 ``raum_4_tuer_5``/``ende_7`` in
    ``raum_1``, Mollgasse EG ``raum_51_tuer_durchgang_25`` in ``raum_33``);
    seit Slice S3b zieht B2 auch sie (``test_og3_keine_anker_in_wohnung_privat``,
    Rennweg OG3 ``rest_3_tuer_tuer_4`` in ZIMMER ``raum_2``)."""
    privat = [(r.id, Polygon(r.polygon_mm)) for r in modell.raeume
              if r.raum_typ in ("GANG", "VORRAUM")
              and r.nutzungsklasse == "WOHNUNG_PRIVAT" and len(r.polygon_mm) >= 3]
    return [a.id for a in modell.anker
            if any(rid != a.raum_id and p.contains(Point(a.xy_mm))
                   for rid, p in privat)]


def stuetzpunkt_segmente(modell, raum_id: str) -> list[str]:
    """Segmente MIT STÜTZPUNKT IM RAUM — die Zählweise, in der § 6g die
    Nebenwirkung „raum_35 10 → 2 Segmente" definiert hat. Die Start/Ziel-
    Zuordnung eines Segments ist eine andere Zahl und deckt den Verlust an
    Zirkulationsabdeckung nicht auf."""
    r = next(x for x in modell.raeume if x.id == raum_id)
    poly = Polygon(r.polygon_mm).buffer(0)
    return sorted({s.segment_id for s in modell.zirkulation.segmente
                   for p in s.polyline_mm if poly.contains(Point(p))})


def startziel_segmente(modell, raum_id: str) -> list[str]:
    """Die ANDERE Zählweise: Segmente, die den Raum als ``start_raum`` oder
    ``ziel_raum`` führen. Für Messfall (i) ist sie mitzuführen, weil das
    Kriterium in BEIDEN Zählweisen verletzt wird."""
    return sorted({s.segment_id for s in modell.zirkulation.segmente
                   if raum_id in (s.start_raum, s.ziel_raum)})


def zirkulationspunkte(modell, raum_id: str) -> int:
    r = next(x for x in modell.raeume if x.id == raum_id)
    poly = Polygon(r.polygon_mm).buffer(0)
    return sum(1 for s in modell.zirkulation.segmente
               for p in s.polyline_mm if poly.contains(Point(p)))


# ── (d) Reihenfolge-Invarianz auf echten Plänen ─────────────────────────────
#: Felder, die S7 selbst erzeugt — hier ist Reihenfolge-Invarianz die
#: Zusicherung des Slices. ``rollen`` sind seit E7 (Runde 7) die ROHEN Rollen
#: des Modells, ``korrigiert`` die daraus abgeleiteten, mit denen der
#: Fluchtweg rechnet.
S7_FELDER = ("klassen", "flags", "wohnung_id", "gruppen", "rollen", "korrigiert",
             "warnungen")
#: Felder, deren Reihenfolgeabhängigkeit VORBESTEHEND ist (``provider.py``
#: legt neue Ausgänge über eine 1500-mm-Dedup-Schleife zusammen, deren
#: Ergebnis an der Listenreihenfolge hängt; auf HEAD 5ac3e0f ist die Wirkung
#: breiter als hier). Sie werden gemessen und benannt, nicht versteckt.
VORBESTEHEND = frozenset({"ausgaenge", "segmente"})
#: Gemessen im Arbeitsbaum UND auf HEAD 5ac3e0f mit DENSELBEN Permutationen
#: (Runde 5, ``_perm_head.py``) — beides im Bericht. Leer = auf diesem Plan
#: hängt auch das Vorbestehende nicht an der Reihenfolge.
VORBESTEHEND_ERWARTET: dict[str, set[str]] = {
    "og1": {"ausgaenge", "segmente"},
    # Runde 4 fehlten diese beiden (Reviewer-Befund Runde 4, Linse Regel):
    "eg": {"ausgaenge", "segmente"},
    "moll_eg": {"segmente"},
}
#: Räume, die die Klassen-Iteration nicht entscheiden konnte und die darum
#: unbestimmt ausgeliefert werden (Schritt 3, Nicht-Konvergenz).
#: Bis Runde 6 waren das 11 Zyklus-Kipper (OG2 raum_9/10, BARA raum_31,
#: MOLL_EG raum_29/57, MOLL_1OG raum_16/19/26/34). Seit den Owner-Entscheiden
#: vom 2026-09-21 nachmittags entscheidet die Regel sie: BARA raum_31 über die
#: Ankerregel auf ROHEN Rollen (Board 7), die Paare als „beide allgemein"
#: (Board 4), Mollgasse 1OG über den Wohnungseingang mit Blatt als Grenze der
#: Flur-Verfeinerung (Board 6). GEMESSEN Runde 7 — wächst die Menge, fällt
#: der Test auf.
KIPPER: dict[str, set[str]] = {
    "og1": set(),
    "og2": set(),
    "og3": set(),
    "ug": set(),
    "eg": set(),
    "bara": set(),
    "moll_eg": set(),
    "moll1og": set(),
    "dg1": set(),
    "dg2": set(),
    "dd": set(),
}
#: R1-Erweiterung A+C (Owner 2026-09-27): „Der gebundene Gang bleibt
#: unbestimmt wie der Loch-Gang" — auch dort, wo Schritt 1–3 ihn als Kandidaten
#: mit Stiegenhaustür allgemein sprechen (``klassifiziere``). Keine
#: Nicht-Konvergenz, sondern eine Owner-Setzung aus (b); GEMESSEN Runde 1 der
#: Erweiterung: nur OG3 ``raum_10``. Wächst oder wandert die Menge, fällt der
#: Test auf.
R1_GEBUNDEN: dict[str, set[str]] = {"og3": {"raum_10"}}
#: Alle Pläne mit Fixture (Muthgasse E2 nicht: ein Parse ~10 min; die
#: Invarianz dort steht im Bericht).
FIXTURE_PLAENE = ["og1", "og2", "og3", "ug", "eg", "dg1", "dg2", "dd", "bara",
                  "moll_eg", "moll1og"]
#: Messfall (i), Runde 7 gemessen. KEIN Zielbild — S7c löst ihn (s.u.).
#: Mollgasse 1OG ``raum_35``: (Stützpunkt-Segmente, Start/Ziel-Segmente),
#: HEAD 5ac3e0f = (10, 17), Runde 6 = (2, 9). Seit Board 6 (Runde 7) sind
#: auch ``raum_19``/``raum_26`` bestätigt privat; die vier Wege, die an ihren
#: inneren Türen starteten (``seg_graph_tuer_29``/``30``/``31``/``32``, aus
#: Bad/WC über den Vorraum zum Stiegenhaus), entfallen — die Wohnungen
#: starten an ``tuer_20``/``tuer_21``. Rennweg OG1: (``raum_14``
#: Stützpunkt-Segmente, ``raum_14`` Zirkulationspunkte, ``rest_2``
#: Start/Ziel), HEAD = (3, 9, 4), Runde 6 = Runde 7.
#: Runde 10 (G4, Owner 2026-09-22: Entzug nur mit Aufenthaltsraum hinter dem
#: Wohnungseingang): ``raum_19``/``raum_26`` (nur Bad/WC) behalten Notlicht,
#: ihre vier Wege kommen zurück — Mollgasse (2, 9) = Runde 6; Rennweg OG1
#: ``raum_12`` (nur Abstellraum/WC) ebenso, die Wege ``seg_graph_tuer_10``/
#: ``11`` laufen wieder durch das Stiegenhaus — OG1 (3, 9, 4) = HEAD, die
#: S7c-Abnahme für OG1 („rest_2 wieder 4, raum_14 Stützpunkte wieder 3").
#: **Planer-Entscheid P1 (Runde 11):** ``MESSFALL_I_MOLL`` steht auf dem
#: Runde-6-Stand (2, 9), NICHT auf HEAD (10, 17). Das ist ausdrücklich eine
#: CHARAKTERISIERUNG (E4 „Zahlen neu messen", Richtung HEAD, kein schlechterer
#: Ist-Wert als die Vorrunde) und KEIN Zielbild; die Abnahme dafür ist S7c:
#: Start/Ziel-Segmente von ``raum_35`` wieder 17, Stützpunkt-Segmente wieder
#: 10, mit der Stiegenhaustür als Start. Erst wenn das erreicht ist, geht die
#: Zahl auf HEAD.
#: **Slice S7c (Owner-GO 2026-09-26; Runde 1 gebaut, Runde 2 präzisiert): die
#: Owner-Abnahme (10, 17) ist mit der gebauten Regel JE STARTTÜR
#: unerreichbar** — die Zahl bleibt darum CHARAKTERISIERUNG auf (2, 9). Ein
#: GRAPH-Segment entsteht je Tür mit korrigierter Rolle ``wohnungseingang``
#: (Start-Regel ``fluchtweg.py:329ff``, ID ``seg_graph_<tuer>``). Die 17
#: Start/Ziel-Segmente von HEAD sind die 17 GRAPH-Segmente des Plans; die 8
#: fehlenden starteten an den 8 INNEREN Türen der bestätigt privaten Vorräume
#: ``raum_2``/``raum_4`` (``tuer_5``/``6``/``7``/``8`` und ``tuer_25``/``28``/
#: ``82``/``83``), und für genau diese sagt die Owner-Regel „die innere Tür
#: wird zimmertuer". Die ÄUSSEREN Türen ``tuer_3``/``tuer_4`` (``raum_35`` ↔
#: ``raum_2``/``raum_4``) tragen roh UND korrigiert schon ``wohnungseingang``
#: und sind schon Start (``seg_graph_tuer_3``/``tuer_4``): 2 Wege, nicht 8.
#: Die 17 kommen nur zurück über (B) die inneren Türen als Start — gegen den
#: Owner-Satz „die innere Tür wird zimmertuer" — oder (C) je innerer Tür ein
#: Duplikat des äußeren Wegs, also eine Änderung der Start-Regel in
#: ``fluchtweg.py``. Keins von beiden ist gebaut; Entscheidung beim Owner
#: (Board-Frage 1, Messung A/B/C im Bericht S7c Runde 2).
#: **Owner-Entscheid 2026-09-26 zu Board-Frage 1: Option A.** (2, 9) ist damit
#: ZIELBILD, kein Charakterisierungswert mehr: „privat heißt keine eigene
#: Zirkulation" (Durchleitungs-Entscheid) gilt unverändert; die 17 stammt aus
#: einem Stand, in dem die Vorräume Erschließung waren, und ist überholt
#: (docs/GATE_TUERSTAPEL.md § 6g.10). B und C sind verworfen.
MESSFALL_I_MOLL = (2, 9)
#: **Slice S5c, Owner-Entscheid F3 (2026-09-27), mit Auflage:** Rennweg OG1
#: steht auf (3, 9, 0), dazu ``rest_1`` Start/Ziel 4 (``MESSFALL_I_OG1_REST_1``).
#: Die 4 an ``rest_2`` (HEAD 5ac3e0f, S7c-Abnahme „rest_2 wieder 4") stammt aus
#: einem Stand, in dem Lifttüren als Ausgänge zählten: ``rest_2`` war der
#: Stiegenhaus-Ring um die Liftkabine, die 4 waren die GRAPH-Wege
#: ``seg_graph_tuer_3``/``10``/``11`` an der Lifttür ``exit_durchgang_8``
#: (208,9 mm vom Schacht) und das FALLBACK-Segment von ``rest_2``. Seit S5c ist
#: ``rest_2`` Liftschacht (Kabinenanteil 0,635, F1/K1_T); dieselben drei Wege
#: enden an der Treppenöffnung ``exit_durchgang_6`` und führen ``rest_1`` als
#: Ziel, dazu dessen FALLBACK — ``rest_1`` = 4. Die Absenkung 4 → 0 ist eine
#: KORREKTUR, keine Bandabsenkung. Überholt, nicht gelöscht: (3, 9, 4) mit
#: ``rest_2`` = 4.
MESSFALL_I_OG1 = (3, 9, 0)
MESSFALL_I_OG1_REST_1 = 4
#: Die acht Wege, die § 6g.8/``bericht_r14.md`` als S7c-Abnahme führt
#: (HEAD-IDs) — mit der gebauten Regel je Starttür unerreichbar, zurück nur
#: über (B) oder (C), s. o. Owner-Entscheid 2026-09-26 (Option A): ihre
#: Abwesenheit ist Zielbild.
S7C_ACHT_WEGE = ("seg_graph_tuer_25", "seg_graph_tuer_28", "seg_graph_tuer_5",
                 "seg_graph_tuer_6", "seg_graph_tuer_7", "seg_graph_tuer_8",
                 "seg_graph_tuer_82", "seg_graph_tuer_83")


def _lauf(eingabe, permutation):
    """Die ganze Kette ab ``bilde_wohnungen`` permutiert (Befund B6) — inklusive
    ``leite_ausgaenge`` und der Dedup-Schleife aus ``provider.py``."""
    from notbeleuchtung.raumerkennung.ausgaenge import (
        leite_ausgaenge,
        ohne_unzulaessige_final_exits,
    )

    raeume = copy.deepcopy(eingabe["raeume"])
    tueren = copy.deepcopy(eingabe["tueren"])
    permutation(raeume, tueren)
    geschoss = eingabe["geschoss"]
    warnungen: list[str] = []
    wohnungen = bilde_wohnungen(raeume, tueren, warnungen)
    neue, _ = leite_ausgaenge(tueren, raeume, geschoss,
                              copy.deepcopy(eingabe["flw_enden"]))
    vorhandene = copy.deepcopy(eingabe["ausgaenge_basis"])
    for a in neue:                      # wörtlich die Schleife aus provider.py
        if not any(a.typ == v.typ
                   and abs(a.xy_mm[0] - v.xy_mm[0])
                   + abs(a.xy_mm[1] - v.xy_mm[1]) < 1500.0
                   for v in vorhandene):
            vorhandene.append(a)
    ausgaenge = ohne_unzulaessige_final_exits(vorhandene, geschoss)
    segmente = fluchtwege(raeume, tueren, ausgaenge,
                          copy.deepcopy(eingabe["bisher"]), geschoss)
    from notbeleuchtung.raumerkennung.wohnungsklasse import korrigierte_rollen
    return {
        "klassen": {r.id: r.nutzungsklasse for r in raeume},
        "flags": {r.id: (r.ist_fluchtweg, r.ist_communal) for r in raeume},
        "wohnung_id": {r.id: r.wohnung_id for r in raeume},
        "gruppen": sorted(tuple(sorted(w.raum_ids)) for w in wohnungen),
        "rollen": {t.id: t.tuer_detail for t in tueren},
        "korrigiert": korrigierte_rollen(raeume, tueren),
        "warnungen": sorted(warnungen),
        "ausgaenge": sorted((a.typ, round(a.xy_mm[0], 3), round(a.xy_mm[1], 3))
                            for a in ausgaenge),
        "segmente": {s.segment_id: (s.quelle, s.start_raum, s.ziel_raum,
                                    s.ziel_ausgang,
                                    [(round(x, 3), round(y, 3))
                                     for x, y in s.polyline_mm])
                     for s in segmente},
    }


def _rev_raeume(r, t):
    r.reverse()


def _rev_tueren(r, t):
    t.reverse()


def _rev_beide(r, t):
    r.reverse()
    t.reverse()


def _shuffle(seed):
    def mische(r, t):
        random.Random(seed).shuffle(r)
        random.Random(seed).shuffle(t)
    mische.__name__ = f"_shuffle{seed}"
    return mische


#: Sechs Permutationen (Reviewer-Befund Runde 4: mindestens sechs).
PERMUTATIONEN = [_rev_raeume, _rev_tueren, _rev_beide, _shuffle(7),
                 _shuffle(11), _shuffle(23)]
#: Ein Lauf je (Plan, Permutation) — die Invarianz- und die
#: Vorbestehend-Prüfung teilen sich die Läufe.
_LAEUFE: dict = {}


def _gecacht(plan_name, eingabe, permutation):
    schluessel = (plan_name, permutation.__name__)
    if schluessel not in _LAEUFE:
        _LAEUFE[schluessel] = _lauf(eingabe, permutation)
    return _LAEUFE[schluessel]


def _identitaet(r, t):
    return None


@pytest.mark.parametrize("plan_name", FIXTURE_PLAENE)
@pytest.mark.parametrize("permutation", PERMUTATIONEN,
                         ids=lambda f: f.__name__.lstrip("_"))
def test_reihenfolge_invariant_s7(plan_name, permutation, request):
    """Befund B6: die Permutation setzt VOR ``leite_ausgaenge`` an, die ganze
    Kette läuft permutiert. Geprüft wird die S7-Wirkung — Klassen, Flags,
    ``wohnung_id``, Wohnungsgruppen, Türrollen, Warnliste.

    Runde 4 war auf genau die sechs Pläne parametrisiert, auf denen die
    Reihenfolge nichts ausmachte (Reviewer-Befund Runde 4: Rennweg OG2,
    Mollgasse EG und Muthgasse E2 hingen an ihr, Ursache Gauß-Seidel in
    ``_verfeinere_gang_privat``). Jetzt: alle Pläne mit Fixture, sechs
    Permutationen."""
    _, _, eingabe = request.getfixturevalue(plan_name)
    identitaet = _gecacht(plan_name, eingabe, _identitaet)
    permutiert = _gecacht(plan_name, eingabe, permutation)
    for feld in S7_FELDER:
        assert identitaet[feld] == permutiert[feld], (
            f"{plan_name}/{permutation.__name__}: {feld} hängt an der Reihenfolge")


@pytest.mark.parametrize("plan_name", FIXTURE_PLAENE)
@pytest.mark.parametrize("permutation", PERMUTATIONEN,
                         ids=lambda f: f.__name__.lstrip("_"))
def test_reihenfolge_vorbestehend_benannt(plan_name, permutation, request):
    """CHARAKTERISIERUNG, kein S7-Kriterium. ``ausgaenge`` und ``segmente``
    hängen über die Dedup-Schleife in ``provider.py`` an der Türreihenfolge —
    das ist VORBESTEHEND (auf HEAD 5ac3e0f mit denselben Permutationen
    gemessen, s. Bericht). Der Test versteckt das nicht, sondern nagelt fest,
    WELCHE Pläne betroffen sind; wandert die Menge, fällt er auf."""
    _, _, eingabe = request.getfixturevalue(plan_name)
    identitaet = _gecacht(plan_name, eingabe, _identitaet)
    permutiert = _gecacht(plan_name, eingabe, permutation)
    abweichend = {f for f in VORBESTEHEND
                  if identitaet[f] != permutiert[f]}
    assert abweichend <= VORBESTEHEND_ERWARTET.get(plan_name, set()), (
        f"{plan_name}/{permutation.__name__}: NEUE Abweichung {abweichend} — "
        "das wäre eine S7-Wirkung, keine vorbestehende")


# ── (e) Stabilität: der ausgelieferte Zustand ist ein Fixpunkt ─────────────
@pytest.mark.parametrize("plan_name", FIXTURE_PLAENE)
def test_bilde_wohnungen_ist_idempotent(plan_name, request):
    """Befund B1: eine zweite Auswertung von ``bilde_wohnungen`` auf dem
    AUSGELIEFERTEN Modell muss denselben Zustand liefern. In Runde 3 kippte
    dabei Barawitzka EG ``raum_30`` mit Periode 2 von ALLGEMEIN auf PRIVAT
    (Flags [0,0] → Notlicht weg) und zurück; auf HEAD 5ac3e0f passiert das
    nicht. Geprüft wird der volle Zustand: Klassen, Flags, ``wohnung_id``,
    Türrollen, Wohnungsgruppen.

    Reviewer-Hinweis Runde 5 (Linse Regel): verglichen wird auch das
    AUSGELIEFERTE Modell mit Lauf 1 (nicht nur Lauf 1 mit Lauf 2), und die
    Warntexte — seit Runde 6 rechnet der Grund eines Zyklus die Fixpunkte
    der Regel nach, er muss beim Nachrechnen gleich bleiben."""
    prov, modell, _ = request.getfixturevalue(plan_name)
    raeume = copy.deepcopy(modell.raeume)
    tueren = copy.deepcopy(modell.tueren)

    def zustand():
        gruppen: dict[str, list[str]] = {}
        for r in raeume:
            if r.wohnung_id:
                gruppen.setdefault(r.wohnung_id, []).append(r.id)
        return ({r.id: (r.nutzungsklasse, r.ist_fluchtweg, r.ist_communal,
                        r.wohnung_id) for r in raeume},
                {t.id: t.tuer_detail for t in tueren},
                sorted(tuple(sorted(x)) for x in gruppen.values()))

    null = zustand()
    # Alle Warnungen aus ``bilde_wohnungen`` (unbestimmt:, seit Runde 8 auch
    # loch:) — ohne die Durchleitungs-Zeilen, die erst ``fluchtwege`` anhängt.
    ausgeliefert = sorted(w for w in prov.wohnungsklasse_warnungen
                          if not w.startswith("durchleitung:"))
    warn_eins: list[str] = []
    bilde_wohnungen(raeume, tueren, warn_eins)
    eins = zustand()
    warn_zwei: list[str] = []
    bilde_wohnungen(raeume, tueren, warn_zwei)
    zwei = zustand()
    for vorher, nachher, was in ((null, eins, "ausgeliefert → Lauf 1"),
                                 (eins, zwei, "Lauf 1 → Lauf 2")):
        assert vorher[0] == nachher[0], f"{was}: Klassen/Flags/wohnung_id kippen"
        assert vorher[1] == nachher[1], f"{was}: Türrollen kippen"
        assert vorher[2] == nachher[2], f"{was}: Wohnungsgruppen kippen"
    assert sorted(warn_eins) == ausgeliefert, "ausgeliefert → Lauf 1: Warntexte"
    assert sorted(warn_zwei) == ausgeliefert, "Lauf 1 → Lauf 2: Warntexte"


@pytest.mark.parametrize("plan_name", FIXTURE_PLAENE)
def test_kandidatenklasse_ist_fixpunkt_der_eigenen_regel(plan_name, request):
    """Dieselbe Zusicherung auf der Klassenebene, jetzt SCHARF.

    Der Reviewer hat gezeigt, dass die Runde-3-Fassung
    (``r.nutzungsklasse in (nach, None)``) nach Konstruktion nicht
    fehlschlagen konnte: ein widersprechender Raum wurde zuvor auf ``None``
    gesetzt, also war die Bedingung immer erfüllt. Jetzt wird die Menge der
    Räume, die dem Fixpunkt widersprechen, GEGEN DIE GEMESSENE MENGE geprüft
    — sie darf weder wachsen noch wandern. Alles andere muss exakt gleich
    sein, und jeder Kipper muss mit Grund im Bericht stehen. Dazu kommen die
    nach R1 gebundenen Gänge (``R1_GEBUNDEN``, Owner 2026-09-27): ebenfalls
    unbestimmt, mit ihrem eigenen Grund."""
    prov, modell, _ = request.getfixturevalue(plan_name)
    nach, _ = klassifiziere(modell.raeume, modell.tueren)
    abweichung = {r.id for r in modell.raeume
                  if r.id in nach and r.nutzungsklasse != nach[r.id]}
    r1 = R1_GEBUNDEN.get(plan_name, set())
    assert abweichung == (KIPPER[plan_name] | r1) & set(nach), (
        f"{plan_name}: Kipper-Menge gewandert — {sorted(abweichung)}")
    for rid in abweichung:
        r = next(x for x in modell.raeume if x.id == rid)
        assert r.nutzungsklasse is None, f"{rid} widerspricht, ist aber gesetzt"
        if rid in r1:
            assert [w for w in prov.wohnungsklasse_warnungen
                    if w.startswith(f"unbestimmt: {rid} — R1: Wohnungsflur")], (
                f"{rid}: nicht im Bericht")
            continue
        assert [w for w in prov.wohnungsklasse_warnungen
                if rid in w and "Schritt 3" in w], f"{rid}: nicht im Bericht"


@pytest.mark.parametrize("plan_name", FIXTURE_PLAENE)
def test_kipper_menge_ist_gemessen(plan_name, request):
    """Nicht-Konvergenz (Schritt 3) trifft genau die gemessene Menge je Plan —
    seit Runde 7 auf allen Plänen mit Fixture keinen Raum. Jeder dennoch
    unbestimmte Raum behält beide Flags."""
    prov, modell, _ = request.getfixturevalue(plan_name)
    kipper = {w.split(" — ")[0].removeprefix("unbestimmt: ")
              for w in prov.wohnungsklasse_warnungen
              if w.startswith("unbestimmt:") and "Schritt 3" in w}
    assert kipper == KIPPER[plan_name], f"{plan_name}: {sorted(kipper)}"
    for r in modell.raeume:
        if r.id in kipper:
            assert r.nutzungsklasse is None
            assert (r.ist_fluchtweg, r.ist_communal) == (True, True), r.id


_A, _P = "ALLGEMEIN_ERSCHLIESSUNG", "WOHNUNG_PRIVAT"


@pytest.mark.parametrize("plan_name,raum_id,klasse,flags", [
    # Board 5 / E6: transitiv (Kellergang zum Kinderwagenraum), 0 Wohnungen.
    ("ug", "raum_12", _A, (True, True)),
    ("dg2", "raum_6", _A, (True, True)),
    ("moll_eg", "raum_7", _A, (True, True)),
    # Bis Slice S3b Loch-Räume nach rohen Türen (Owner 2026-09-22, G1.2):
    # ``raum_9`` allgemein, ``raum_10`` unbestimmt. S3b schließt das Loch —
    # die 940er Blocktür ``tuer_1`` erreicht das Stiegenhaus ``rest_1`` (roh
    # ``wohnungseingang`` mit Blatt), die Ankerregel bestätigt alle vier
    # privat, G4 belegt → Flags 00 wie OG1 ``raum_4``/``5``/``8`` (die Zahl
    # folgt der Regel, § 6g.10). Wohnungen: ``OG2_NACH_S3B``.
    ("og2", "raum_4", _P, (False, False)),
    ("og2", "raum_5", _P, (False, False)),
    ("og2", "raum_9", _P, (False, False)),
    ("og2", "raum_10", _P, (False, False)),
    # Board 4: zwei Fixpunkte, kein voller Beleg → Tiebreak, allgemein.
    ("moll_eg", "raum_29", _A, (True, True)),
    ("moll_eg", "raum_57", _A, (True, True)),
    # Beleg vor Tiebreak (Owner 2026-09-22, G2): der private Fixpunkt macht
    # Rennweg OG1 ``raum_4``/``raum_5`` voll ankerbestätigt privat — er gilt
    # (Runde 9, L1: allgemein — verworfen).
    ("og1", "raum_4", _P, (False, False)),
    ("og1", "raum_5", _P, (False, False)),
    # Board 6 / E8: Wohnungseingang mit Blatt begrenzt die Flur-Verfeinerung
    # — privat. Entzogen wird seit G4 (Owner 2026-09-22) aber nur, wo hinter
    # dem Wohnungseingang ein Aufenthaltsraum liegt: ``raum_16`` allein,
    # ``raum_19`` mit Bad/WC, ``raum_26`` mit Bad/WC → Notlicht bleibt.
    ("moll1og", "raum_16", _P, (True, True)),
    ("moll1og", "raum_19", _P, (True, True)),
    ("moll1og", "raum_26", _P, (True, True)),
    ("moll1og", "raum_34", _A, (True, True)),
    # G4 wörtlich (Owner 2026-09-22, UG ``raum_6``): hinter dem
    # Wohnungseingang nur Abstellraum bzw. Abstellraum und WC → Notlicht
    # bleibt, obwohl ankerbestätigt privat.
    ("ug", "raum_6", _P, (True, True)),
    ("og1", "raum_12", _P, (True, True)),
    # Board 7 / E7: Ankerregel auf rohen Rollen.
    ("bara", "raum_31", _A, (True, True)),
    ("dg2", "raum_1", None, (True, True)),
])
def test_r7_klasse_nach_den_owner_entscheiden(plan_name, raum_id, klasse, flags,
                                              request):
    """Die Erwartungen aus den Owner-Entscheiden vom 2026-09-21 nachmittags
    und 2026-09-22, Raum für Raum auf den echten Plänen. Flags (False, False)
    nur, wo die Ankerregel auf den ROHEN Rollen PRIVAT bestätigt (Board 6)
    UND hinter dem Wohnungseingang ein Aufenthaltsraum liegt (G4). DG2 ``raum_1`` war bis Runde 6 nur auf den korrigierten Rollen
    bestätigt — roh trennt ihn nur die blattlose ``durchgang_5`` vom
    Stiegenhaus, er behält sein Notlicht."""
    from notbeleuchtung.raumerkennung.wohnungsklasse import bestaetigt_privat

    _, modell, _ = request.getfixturevalue(plan_name)
    r = next(x for x in modell.raeume if x.id == raum_id)
    assert r.nutzungsklasse == klasse, f"{raum_id}: {r.nutzungsklasse}"
    assert (r.ist_fluchtweg, r.ist_communal) == flags, raum_id
    assert (raum_id in bestaetigt_privat(modell.raeume, modell.tueren)) == (
        flags == (False, False)), raum_id


# ── (f) Naht ────────────────────────────────────────────────────────────────
def test_kinderwagenraum_behaelt_seinen_weg(ug):
    """§ 6g Messfall (ii). Rennweg UG: der KINDERWAGENRAUM (21,49 m²) muss
    weiter an einem Fluchtweg-Segment hängen — die Durchleitung darf ihn nicht
    abhängen."""
    _, modell, _ = ug
    kiwa = [r for r in modell.raeume if r.raum_typ == "KINDERWAGENRAUM"
            and len(r.polygon_mm) >= 3]
    assert kiwa, "kein KINDERWAGENRAUM im UG erkannt"
    polys = [Polygon(r.polygon_mm).buffer(0) for r in kiwa]
    treffer = [s.segment_id for s in modell.zirkulation.segmente
               for p in s.polyline_mm
               if any(q.distance(Point(p)) < 1.0 for q in polys)]
    assert treffer, "KINDERWAGENRAUM ohne Fluchtweg-Segment"


#: Die vom Stiegenhaus über keine Tür erreichbaren Räume (Messfall S4c/S3b)
#: auf den Rennweg-Plänen, nach dem Owner-Grundsatz 2026-09-22 (G1.2,
#: „Wohnung folgt rohen Türen"), gemessen Runde 10: über eine rohe Zimmertür
#: an ihre Wohnung gebunden → in ihr, unbestimmt (``None``, Menge = ihre
#: Wohnung); nur über rohe Wohnungseingänge angebunden → Erschließung,
#: allgemein, keine Wohnung (Menge = die Räume hinter diesen Eingängen, jede
#: ihrer Wohnungen hat einen Eingang). Bis Runde 9 waren alle allgemein
#: (E5 Satz 2, aufgehoben).
#:
#: **Runde 11, Owner-Entscheid R1 (2026-09-22):** „Ein Loch-GANG, hinter dessen
#: rohen Wohnungseingängen NUR Einzelräume liegen (jede dahinterliegende
#: Raumgruppe hat genau einen Raum), bildet mit diesen Räumen EINE Wohnung; er
#: selbst bleibt für (a) unbestimmt mit Notlicht (Flags 11)." Das trifft
#: Rennweg OG3 ``raum_10``: seine vier rohen Wohnungseingänge führen zu
#: ``raum_1`` KÜCHE, ``raum_4`` ZIMMER, ``raum_6`` BAD und ``raum_7``
#: ABSTELLRAUM, jeder für sich allein. Er ist damit unbestimmt IN der Wohnung
#: ``{raum_1, raum_4, raum_6, raum_7, raum_10}`` — wie auf HEAD 5ac3e0f — statt
#: Erschließung mit vier Einraum-Wohnungen dahinter (Runde 10, Gate (3) OG3).
#: Rennweg OG2 ``raum_9`` blieb Erschließung: hinter ``durchgang_8`` liegt
#: eine mehrräumige Wohnung, die Bedingung „NUR Einzelräume" ist verletzt.
#: **Slice S3b (2026-09-26):** OG2 ist kein Loch mehr (``tuer_1`` erreicht das
#: Stiegenhaus) — die vier OG2-Zeilen stehen seither in ``OG2_NACH_S3B``. OG3
#: ``raum_10`` ebenfalls nicht: ``tuer_5`` (940 mm, Blatt) erreicht das
#: STIEGENHAUS ``rest_3``, roh ``stiegenhaustuer``.
#: **R1-Erweiterung, Fassung A+C (Owner 2026-09-27):** der Gang bindet
#: trotzdem — sein Zugang ist nur diese Stiegenhaustür mit Blatt (A), hinter
#: ihm liegen Küche/Zimmer UND Bad/Abstellraum als Einzelräume (C) — und
#: bleibt wie der Loch-Gang unbestimmt: „der Gang gehört zur Wohnung, ist aber
#: kein Beleg für eine eigene Wohnung; unbestimmt heißt Notlicht bleibt". Der
#: Bericht führt ihn als ``r1:``-Zeile, nicht mehr als ``loch:``-Zeile.
R1_GANG_ROH = {
    ("og3", "raum_10"): (None, {"raum_1", "raum_4", "raum_6", "raum_7", "raum_10"}),
}


@pytest.mark.parametrize("plan_name,raum_id", sorted(R1_GANG_ROH))
def test_loch_raum_folgt_rohen_tueren(plan_name, raum_id, request):
    """G1.2 und R1 auf den echten Plänen (der Testname stammt aus der Zeit, in
    der ``raum_10`` ein Loch-Raum war; § 6g.8/§ 7e führen ihn so): der Gang
    gehört nach rohen Türen zu seiner Wohnung, bleibt für (a) unbestimmt mit
    eigenem Grund, behält beide Flags, und die Bindung steht im Bericht als
    ``r1:``-Zeile mit ihrem Zugang ``tuer_5`` — keine ``loch:``-Zeile."""
    prov, modell, _ = request.getfixturevalue(plan_name)
    klasse, menge = R1_GANG_ROH[(plan_name, raum_id)]
    r = next(x for x in modell.raeume if x.id == raum_id)
    assert r.nutzungsklasse == klasse, r.nutzungsklasse
    assert (r.ist_fluchtweg, r.ist_communal) == (True, True)
    assert {x.id for x in modell.raeume
            if x.wohnung_id and x.wohnung_id == r.wohnung_id} == menge
    warn = prov.wohnungsklasse_warnungen
    assert [w for w in warn if w.startswith(f"unbestimmt: {raum_id} — ")
            and "Wohnungsflur hinter Stiegenhaustür" in w], raum_id
    assert [w for w in warn if w.startswith(f"r1: {raum_id} — ") and "tuer_5" in w
            and "nur Einzelräume" in w and "(R1)" in w], raum_id
    assert not [w for w in warn if w.startswith(f"loch: {raum_id} — ")], raum_id


#: Slice S3b (2026-09-26) schließt das OG2-Loch (bis dahin ``LOCH_ROH``, heute
#: ``R1_GANG_ROH``): die
#: 940er Blocktür ``tuer_1`` (STIEGENHAUS ``rest_1`` ↔ VORRAUM ``raum_4``, roh
#: ``wohnungseingang`` mit Blatt) hat jetzt beide Seiten; die Ankerregel sagt
#: für ``raum_4``/``5``/``9``/``10`` „nur über die Wohnungseingangstür tuer_1
#: (mit Türblatt) erreichbar". Die Wohnung (b) folgt den rohen Türen:
#: ``raum_4``/``5`` wie bis S3b mit ``raum_3``/``raum_6`` hinter ``tuer_1``;
#: ``raum_9``/``10`` in der Wohnung jenseits des untypisierten ``raum_2``
#: (59,53 m², R2: gehört zu keiner Wohnung, Wohnküchen-Verdacht) — ohne
#: Wohnungseingang, raummengengleich HEAD 5ac3e0f. Wer den Kanon-Punkt
#: WOHNKÜCHE entscheidet (@EnisAMG), entscheidet diese Grenze mit — wie bei
#: OG1 ``raum_10`` (§ 6g.10), kein S3b-Rückfall.
_OG2_HINTER_TUER_1 = {"raum_3", "raum_4", "raum_5", "raum_6"}
_OG2_JENSEITS_RAUM_2 = {"raum_1", "raum_7", "raum_8", "raum_9", "raum_10",
                        "raum_11", "raum_12", "raum_15", "raum_16"}
OG2_NACH_S3B = {"raum_4": _OG2_HINTER_TUER_1, "raum_5": _OG2_HINTER_TUER_1,
                "raum_9": _OG2_JENSEITS_RAUM_2, "raum_10": _OG2_JENSEITS_RAUM_2}


@pytest.mark.parametrize("raum_id", sorted(OG2_NACH_S3B))
def test_og2_loch_von_s3b_geschlossen(raum_id, og2):
    """Wohnung nach rohen Türen und kein ``loch:`` mehr im Bericht — Klasse
    und Flags bindet ``test_r7_klasse_nach_den_owner_entscheiden``."""
    prov, modell, _ = og2
    r = next(x for x in modell.raeume if x.id == raum_id)
    assert {x.id for x in modell.raeume
            if x.wohnung_id and x.wohnung_id == r.wohnung_id} == OG2_NACH_S3B[raum_id]
    assert not [w for w in prov.wohnungsklasse_warnungen
                if w.startswith(f"loch: {raum_id} — ")], raum_id


def test_moll_eg_raum_23_behaelt_seine_wege(moll_eg):
    """Reviewer Runde 7 (Linse Naht, blockierend 4): Mollgasse EG ``raum_23``
    VORRAUM 7,91 m² ist unbestimmt (vom Stiegenhaus nur durch die blattlose
    Öffnung ``durchgang_13`` getrennt), behält Flags 11 — verlor in Runde 7
    aber 9 von 10 Zirkulationspunkten: er zählte als Loch zur Wohnung {23,
    24, 26}, ``tuer_9``/``tuer_11`` wurden Zimmertüren, die Wege aus WC
    ``raum_26`` und Abstellraum ``raum_24`` durch ihn entfielen. „Wer sein
    Notlicht behält, behält auch seine Zirkulation": ein nur blattlos
    getrennter Raum zählt für die korrigierten Rollen (Fluchtweg, Frage (a))
    als Erschließung. Soll = Runde 6 (= HEAD): 10 Punkte, 3
    Stützpunkt-Segmente. Die WOHNUNG folgt seit dem Owner-Grundsatz
    2026-09-22 den rohen Türen (b): hinter dem Wohnungseingang ``tuer_20``
    MIT Blatt gehört ``raum_23`` mit WC und Abstellraum zu einer Wohnung —
    das ändert keine Rolle, an der ein Weg startet."""
    _, modell, _ = moll_eg
    r = next(x for x in modell.raeume if x.id == "raum_23")
    assert r.nutzungsklasse is None
    assert (r.ist_fluchtweg, r.ist_communal) == (True, True)
    assert {x.id for x in modell.raeume
            if x.wohnung_id and x.wohnung_id == r.wohnung_id} == {
        "raum_23", "raum_24", "raum_26"}
    segmente = stuetzpunkt_segmente(modell, "raum_23")
    assert {"seg_graph_tuer_9", "seg_graph_tuer_11"} <= set(segmente), segmente
    assert len(segmente) >= 3, segmente
    assert zirkulationspunkte(modell, "raum_23") >= 10


#: Stützpunkt-Segmente je GANG/VORRAUM, der auf HEAD 5ac3e0f, in Runde 6 oder
#: Runde 7 unbestimmt war oder vom Stiegenhaus über KEINE Tür erreichbar ist
#: (Messfall S4c/S3b) — das Maximum aus HEAD und Runde 6, gemessen
#: (``m_vorher_*``/``m_r6_*``). Muthgasse E2 hat keine Fixture.
STUETZ_SOLL: dict[str, dict[str, int]] = {
    "og2": {"raum_4": 0, "raum_5": 0, "raum_9": 1, "raum_10": 0},
    "og3": {"raum_10": 1},
    "dg1": {"raum_4": 1},
    "dg2": {"raum_1": 0},
    "bara": {"raum_9": 0, "raum_12": 0, "raum_31": 0},
    # raum_55: S5c/F5 — seine Hauseingangs-Öffnung aussenoeffnung_8 (Streifen
    # zwischen Wandkörpern) fällt, der GANG wird unbestimmt (ALLG → None).
    # Gemessen 5ac3e0f / Runde 6 / S5c-Nachher je 3 (seg_13, seg_16, seg_17).
    "moll_eg": {"raum_23": 3, "raum_29": 0, "raum_49": 0, "raum_55": 3,
                "raum_57": 0},
    "moll1og": {"raum_16": 1, "raum_19": 2, "raum_26": 2, "raum_34": 17,
                "raum_52": 1, "raum_57": 0, "raum_59": 0, "raum_65": 1},
}


@pytest.mark.parametrize("plan_name", FIXTURE_PLAENE)
def test_unbestimmter_raum_behaelt_seine_stuetzpunkt_segmente(plan_name, request):
    """Naht-Wächter (Reviewer Runde 7, Linse Naht, blockierend 4): der
    entfernte ``test_kipper_behaelt_seine_zirkulation`` bewachte „unbestimmt
    ⇒ Zirkulation bleibt" nur auf Mollgasse 1OG. Jetzt auf allen Plänen mit
    Fixture: JEDER unbestimmte GANG/VORRAUM und jeder Loch-Raum (Messfall
    S4c/S3b — er behält immer sein Notlicht) hat mindestens so viele
    Stützpunkt-Segmente wie auf HEAD bzw. in Runde 6. Ein unbestimmter Raum
    ohne gemessenes Soll fällt auf — dann erst messen, nicht raten."""
    from notbeleuchtung.raumerkennung.wohnungsklasse import ankerurteil

    _, modell, _ = request.getfixturevalue(plan_name)
    urteil = ankerurteil(modell.raeume, modell.tueren)
    pruefen = {r.id for r in modell.raeume if r.raum_typ in ("GANG", "VORRAUM")
               and (r.nutzungsklasse is None or "über keine Tür" in urteil[r.id][1])}
    soll = STUETZ_SOLL.get(plan_name, {})
    assert not pruefen - set(soll), f"{plan_name}: ohne Soll {sorted(pruefen - set(soll))}"
    zu_wenig = {rid: (len(stuetzpunkt_segmente(modell, rid)), soll[rid])
                for rid in sorted(pruefen)
                if len(stuetzpunkt_segmente(modell, rid)) < soll[rid]}
    assert not zu_wenig, f"{plan_name}: (ist, soll) {zu_wenig}"


def test_og1_einraum_wohnungen_unter_zwei(og1):
    _, modell, _ = og1
    je_wohnung: dict[str, int] = {}
    for r in modell.raeume:
        if r.wohnung_id:
            je_wohnung[r.wohnung_id] = je_wohnung.get(r.wohnung_id, 0) + 1
    einraum = [w for w, n in je_wohnung.items() if n == 1]
    assert len(einraum) < 2, f"{len(einraum)} Einraum-Wohnungen: {sorted(einraum)}"


#: ALLE gemessenen Pläne außer Muthgasse E2 (ein Parse dort ~10 min; die Zahl
#: steht in der Messung des Berichts, nicht in der Testsuite).
ALLE_PLAENE = [
    (RENNWEG_UG, "UG"), (RENNWEG_EG, "EG"), (RENNWEG_OG1, "OG1"),
    (RENNWEG_OG2, "OG2"), (RENNWEG_OG3, "OG3"), (RENNWEG_DG1, "DG1"),
    (RENNWEG_DG2, "DG2"), (RENNWEG_DD, "DD"), (BARAWITZKA_EG, "EG_BARA"),
    (MOLLGASSE_EG, "EG_MOLL"), (MOLLGASSE_1OG, "1OG_MOLL"),
]


@pytest.mark.parametrize("pfad,floor", ALLE_PLAENE,
                         ids=[n for _, n in ALLE_PLAENE])
def test_keine_anker_wo_das_notlicht_entzogen_wurde(pfad, floor):
    """R4 unter dem Fail-Safe-Riegel, auf ALLEN gemessenen Plänen.

    Befund B2: Runde 3 hat genau die vier Pläne parametrisiert, auf denen die
    Zahl 0 war, während auf Mollgasse 1OG VIER NEUE Anker entstanden
    (``raum_2``/``4``/``69``/``72``, je 0 → 1) — Stiegenhaus-Türanker, die
    geometrisch in den privat gewordenen Vorraum fallen. Gemessen wird die
    Menge, der das Notlicht ENTZOGEN wurde; wer seine Leuchten behält, soll
    seine Anker behalten (Rennweg DG1 ``raum_8`` ist dieser Fall — Klasse
    WOHNUNG_PRIVAT laut Schritt 2, Notlicht trotzdem, weil die Ankerregel
    nicht bestätigt)."""
    _, modell, _ = _eingabe(pfad, floor.split("_")[0])
    drin = anker_in_entzug(modell)
    assert not drin, f"{floor}: {len(drin)} Anker im Notlicht-Entzug: {drin}"
    # B2 wörtlich: kein FREMDER Anker (etwa ein Stiegenhaus-Türanker) liegt
    # in einem privat gewordenen Raum — auch nicht in einem, den die
    # Ankerregel nicht bestätigt. Dessen EIGENE Anker bleiben (Grundsatz).
    fremd = fremde_anker_in_privat(modell)
    assert not fremd, f"{floor}: {len(fremd)} fremde Anker in WOHNUNG_PRIVAT: {fremd}"


def test_og3_keine_anker_in_wohnung_privat():
    """Gate-Bedingung (6), zweiter Teil, wörtlich: Rennweg OG3
    ``anker_in_wohnung_privat == 0`` — die geometrische Zählweise aus
    ``tests/gate/gate_og3.py``, unabhängig vom Riegel."""
    _, modell, _ = _eingabe(RENNWEG_OG3, "OG3")
    drin = anker_in_privat(modell)
    assert not drin, f"OG3: {len(drin)} Anker in WOHNUNG_PRIVAT: {drin}"


#: Wohnungen OHNE Wohnungseingang, die schon auf HEAD 5ac3e0f so gebildet
#: werden (gemessen, ``m_vorher_UG.json``: ``top_2`` = raum_3, ``top_3`` =
#: raum_5) — vorbestehend, nicht Sache dieses Slices; benannt statt versteckt.
#:
#: **Runde 14, OG3:** dort sind es alle DREI Wohnungen, raummengengleich HEAD
#: (``m_vorher_OG3.json``: ``{1,4,6,7,10}`` — ``tuer_5`` führt nach KEIN_RAUM
#: —, ``{2,8}``, ``{3,5}``). OG3 stand bis Runde 13 in keiner der beiden
#: Eingangsprüfungen: ``test_loch_raum_folgt_rohen_tueren`` prüft keine
#: Eingänge (sein Sollwert für ``raum_10`` ist ``None``, R1). Die Abnahme
#: „keine neue Wohnung ohne Eingang" hing für OG3 damit allein an der
#: Messung; hier ist sie gebunden. Seit S3b trägt ``tuer_5`` roh
#: ``stiegenhaustuer`` (kein Wohnungseingang, Owner: nicht (b)) — mit der
#: R1-Erweiterung A+C (Owner 2026-09-27) bleibt ``{1,4,6,7,10}`` eine Wohnung
#: ohne Eingang, wie auf HEAD.
VORBESTEHEND_OHNE_EINGANG: dict[str, set[frozenset[str]]] = {
    "ug": {frozenset({"raum_3"}), frozenset({"raum_5"})},
    "og3": {frozenset({"raum_1", "raum_4", "raum_6", "raum_7", "raum_10"}),
            frozenset({"raum_2", "raum_8"}), frozenset({"raum_3", "raum_5"})},
}


@pytest.mark.parametrize("plan_name", ["dg1", "dg2", "og3", "ug"])
def test_jede_wohnung_hat_einen_wohnungseingang(plan_name, request):
    """§ 6g Schritt 3, KONSERVATIV, im PRODUKTIONSPFAD: ein unbestimmter Raum
    darf keine Wohnungsgrenze auflösen.

    Fällt ein Kandidat auf ``nutzungsklasse = None``, verliert er in der
    Rollenkorrektur seine Zugehörigkeit zur Vergleichsmenge
    ``ALLGEMEIN_ERSCHLIESSUNG`` — die Tür zum Nachbarzimmer bleibt dann
    ``zimmertuer``, die Wohnung hinter ihr hat keinen Eingang mehr und damit
    keinen Fluchtweg-Start. Gemessen betraf das DG1 ``top_1`` und DG2
    ``top_1``/``top_2``. ``ist_wohnungsintern`` nennt einen unbestimmten Raum
    ausdrücklich NICHT privat; dann darf er auch die Grenze nicht auflösen.

    Seit E7 (Runde 7) trägt das Modell die rohen Rollen; der Wohnungseingang,
    an dem der Fluchtweg startet, ist die KORRIGIERTE Rolle."""
    from notbeleuchtung.raumerkennung.wohnungsklasse import korrigierte_rollen

    _, modell, _ = request.getfixturevalue(plan_name)
    rollen = korrigierte_rollen(modell.raeume, modell.tueren)
    gruppen: dict[str, set[str]] = {}
    for r in modell.raeume:
        if r.wohnung_id:
            gruppen.setdefault(r.wohnung_id, set()).add(r.id)
    assert gruppen, f"{plan_name}: keine Wohnung gebildet"
    ohne = []
    for wid, rids in sorted(gruppen.items()):
        eingaenge = [t.id for t in modell.tueren
                     if rollen[t.id] == "wohnungseingang"
                     and len({t.von_raum, t.nach_raum} & rids) == 1]
        if not eingaenge and frozenset(rids) not in \
                VORBESTEHEND_OHNE_EINGANG.get(plan_name, set()):
            ohne.append(f"{wid}={sorted(rids)}")
    assert not ohne, f"{plan_name}: Wohnung(en) ohne Wohnungseingang: {ohne}"


def test_bara_raum_19_behaelt_klasse_und_zirkulation(bara):
    """Barawitzka EG ``raum_19`` VORRAUM 3,42 m² war bis zum abgebrochenen
    Stand von Runde 4 ein Kipper (Klasse → Türrolle → Klasse, unbestimmt). Seit die Rollenkorrektur jede Runde von der ROHEN Rolle
    ausgeht, entscheidet Schritt 2 ihn stabil: zwei Wohnungen → ALLGEMEIN,
    wie auf HEAD 5ac3e0f — mit 10 Zirkulationspunkten und 4
    Stützpunkt-Segmenten wie dort. Die WOHNUNG folgt seit dem Owner-Grundsatz
    2026-09-22 den rohen Türen (b): hinter dem Wohnungseingang ``tuer_28`` MIT
    Blatt gehört er mit Küche, Abstellraum, ``raum_30`` und Bad zu einer
    Wohnung; Klasse und Notlicht (a) ändert das nicht."""
    _, modell, _ = bara
    r19 = next(r for r in modell.raeume if r.id == "raum_19")
    assert r19.nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"
    assert (r19.ist_fluchtweg, r19.ist_communal) == (True, True)
    assert {x.id for x in modell.raeume
            if x.wohnung_id and x.wohnung_id == r19.wohnung_id} == {
        "raum_5", "raum_7", "raum_19", "raum_20", "raum_30", "raum_40"}
    assert zirkulationspunkte(modell, "raum_19") == 10
    assert len(stuetzpunkt_segmente(modell, "raum_19")) == 4


def test_korrigierte_rollen_sind_eine_funktion_von_klasse_und_roher_rolle(moll1og):
    """E7.3: die korrigierten Rollen entstehen genau einmal aus der fertigen
    Klassifikation und den ROHEN Rollen — auf dem ausgelieferten Modell
    nachgerechnet sind sie dieselben, mit denen ``fluchtwege`` gerechnet hat
    (Starttüren der GRAPH-Segmente). Mollgasse 1OG ``tuer_14``/``20``/``21``
    (roh ``wohnungseingang`` zwischen ``raum_34`` und den seit Board 6
    privaten Vorräumen) bleiben Wohnungseingänge und Fluchtweg-Starts."""
    from notbeleuchtung.raumerkennung.wohnungsklasse import korrigierte_rollen

    _, modell, _ = moll1og
    rollen = korrigierte_rollen(modell.raeume, modell.tueren)
    segmente = {s.segment_id for s in modell.zirkulation.segmente}
    for tid in ("tuer_14", "tuer_20", "tuer_21"):
        assert rollen[tid] == "wohnungseingang", (tid, rollen[tid])
        assert next(t for t in modell.tueren if t.id == tid).tuer_detail == \
            "wohnungseingang"
        assert f"seg_graph_{tid}" in segmente, tid


def test_dg1_raum_8_behaelt_sein_notlicht_ohne_ankerbestaetigung(dg1):
    """E3, vierter Punkt, auf dem echten Plan: DG1 ``raum_8`` VORRAUM 8,94 m²
    macht Schritt 2 privat (eine Wohnung, kein Ausgang, kein Nebenraum), die
    ANKERREGEL bestätigt das aber nicht — er ist vom Stiegenhaus nur durch die
    blattlose Öffnung ``durchgang_6`` getrennt. Also behält er beide Flags und
    damit sein Notlicht — UND seine Zirkulation (Option W, Runde 5).

    Die Vorrunde nagelte hier den Verlust fest (Zirkulation 3 → 0,
    ``seg_graph_durchgang_3`` weg — Start im WOHNZIMMER ``raum_1`` —,
    STIEGENHAUS ``rest_2`` 17 → 11): die Rollenkorrektur machte
    ``durchgang_3`` zur Zimmertür. Reviewer-Befund Runde 4 (Linse
    Sicherheit): Fail-Safe verletzt. Soll = HEAD 5ac3e0f.

    **Slice S5c, Owner-Entscheid B1 (2026-09-28):** ``rest_2`` steht auf 0.
    Die 17 (HEAD 5ac3e0f) sind überholt — Phantom-Ausgang im Liftschacht, seit
    S5c entfallen: sie waren die GRAPH-Wege zum Phantom-Ausgang
    ``exit_durchgang_9`` mit Ziel ``rest_3``, und ``rest_3`` ist seit S5c
    Liftschacht (Kabinenanteil 0,684, F1/K1_T). Der verbleibende Weg
    ``seg_graph_durchgang_3`` endet an der Stiegenhaus-Öffnung
    ``exit_durchgang_6`` und läuft nicht mehr durch ``rest_2``. Die Absenkung
    17 → 0 ist eine KORREKTUR, keine Bandabsenkung. Überholt, nicht gelöscht:
    ``rest_2`` = 17."""
    _, modell, _ = dg1
    r8 = next(r for r in modell.raeume if r.id == "raum_8")
    assert r8.nutzungsklasse == "WOHNUNG_PRIVAT"
    assert (r8.ist_fluchtweg, r8.ist_communal) == (True, True)
    assert "seg_graph_durchgang_3" in {s.segment_id
                                       for s in modell.zirkulation.segmente}
    assert zirkulationspunkte(modell, "raum_8") == 3
    assert zirkulationspunkte(modell, "rest_2") == 0  # 17 überholt (S5c, B1)


def test_ug_raum_12_behaelt_die_wege_durch_ihn(ug):
    """Reviewer-Befund Runde 4 (Linse Sicherheit): Rennweg UG ``raum_12`` GANG
    5,35 m² macht Schritt 2 privat, die Ankerregel sagt allgemein (über
    ``tuer_7``) — er behält sein Notlicht, verlor aber auf dem Stand der
    Vorrunde Zirkulation 15 → 12: ``tuer_3`` (WC ``raum_15``) wurde Zimmertür,
    ``seg_graph_tuer_3`` fiel weg, STIEGENHAUS ``raum_16`` Start/Ziel 5 → 4,
    und ``{raum_12, raum_15}`` wurde eine Wohnung ohne Eingang. Soll = HEAD
    5ac3e0f. Seit Board 5 (Runde 7) ist ``raum_12`` auch der KLASSE nach
    ALLGEMEIN: er erschließt über ``raum_10`` den Kinderwagenraum.

    Runde 7, Board 6: der VORRAUM ``raum_6`` hinter ``tuer_8`` (Wohnungs-
    eingang MIT Blatt vom allgemeinen ``raum_10``) ist bestätigt privat. Der
    Weg ``seg_graph_tuer_11`` aus dem ABSTELLRAUM ``raum_7`` dahinter
    entfällt (``tuer_11`` ist jetzt eine Zimmertür derselben Wohnung); die
    Wohnung startet an ``tuer_8``, und dieser Weg läuft weiter durch
    ``raum_10`` und ``raum_12``. Darum Zirkulationspunkte in ``raum_12``
    HEAD 15 → 11 und Start/Ziel am STIEGENHAUS 5 → 4 — gemessen, im Bericht
    Runde 7 als Abweichung begründet.

    Runde 10 (G4, Owner 2026-09-22): hinter ``tuer_8`` liegt nur der
    Abstellraum — kein Aufenthaltsraum, also KEIN Entzug. ``raum_6`` behält
    Notlicht und damit seine Zirkulation; ``tuer_11`` ist für den Fluchtweg
    wieder ein Wohnungseingang, ``seg_graph_tuer_11`` ist zurück: wieder
    HEAD, 15 Zirkulationspunkte und Start/Ziel 5."""
    from notbeleuchtung.raumerkennung.wohnungsklasse import korrigierte_rollen

    _, modell, _ = ug
    assert "seg_graph_tuer_3" in {s.segment_id
                                  for s in modell.zirkulation.segmente}
    assert stuetzpunkt_segmente(modell, "raum_12") == [
        "seg_graph_tuer_11", "seg_graph_tuer_2", "seg_graph_tuer_3", "seg_graph_tuer_8"]
    assert zirkulationspunkte(modell, "raum_12") == 15
    assert len(startziel_segmente(modell, "raum_16")) == 5
    t3 = next(t for t in modell.tueren if t.id == "tuer_3")
    assert t3.tuer_detail == "wohnungseingang"
    assert korrigierte_rollen(modell.raeume, modell.tueren)["tuer_3"] == \
        "wohnungseingang"


def test_bara_raum_30_wird_nicht_von_der_auswertungsreihenfolge_entschieden(bara):
    """Barawitzka EG ``raum_30`` VORRAUM 5,11 m² ist KEIN Kandidat (keine
    Stiegenhaustür) — über ihn entscheidet ``_verfeinere_gang_privat``, und in
    Runde 3 kippte er je nach Auswertungsreihenfolge zwischen ALLGEMEIN und
    PRIVAT (Befund B1, Periode 2, Flags dann [0,0] → Notlicht weg). Im
    abgebrochenen Stand von Runde 4 wurde er als Kipper unbestimmt geführt;
    seit die Rollenkorrektur von der rohen Rolle ausgeht, hat die Kette einen
    Fixpunkt und er bleibt, was er auf HEAD war: ALLGEMEIN, beide Flags,
    4 Zirkulationspunkte und sein Segment. Seine WOHNUNG folgt den rohen
    Türen (Owner 2026-09-22, b): über Zimmertüren hinter ``tuer_28``."""
    _, modell, _ = bara
    r30 = next(r for r in modell.raeume if r.id == "raum_30")
    assert r30.nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"
    assert (r30.ist_fluchtweg, r30.ist_communal) == (True, True)
    r19 = next(r for r in modell.raeume if r.id == "raum_19")
    assert r30.wohnung_id is not None and r30.wohnung_id == r19.wohnung_id
    assert stuetzpunkt_segmente(modell, "raum_30") == ["seg_graph_tuer_35"]
    assert zirkulationspunkte(modell, "raum_30") == 4


def test_ug_meldet_keinen_unerreichbaren_final_exit(ug):
    """§ 6g Messfall (iii): die drei „kein final_exit erreichbar" (tuer_2,
    tuer_8, tuer_11), die ohne Durchleitung entstanden, dürfen nicht
    auftreten."""
    prov, _, _ = ug
    assert not [w for w in prov.fluchtweg_warnungen
                if "kein final_exit erreichbar" in w], prov.fluchtweg_warnungen


# ── S7b-Abnahme: Leuchten (nicht Anker) in WOHNUNG_PRIVAT ───────────────────
@pytest.mark.parametrize("pfad,floor", [
    (RENNWEG_OG1, "OG1"), (RENNWEG_OG2, "OG2"),
    (RENNWEG_OG3, "OG3"), (RENNWEG_DG1, "DG1"),
])
def test_keine_leuchten_in_wohnung_privat(pfad, floor):
    """Die ABNAHMEZAHL von S7b („privat heißt keine Notbeleuchtung") ist die
    Zahl der LEUCHTEN in WOHNUNG_PRIVAT, nicht die der Anker.

    ``tests/naht/test_soll_rennweg.py::test_soll_keine_leuchten_in_wohnung_privat``
    fährt nur OG3; OG1/OG2/DG1 sind unbewacht. Der Test ist auf OG1 GEMESSEN
    ROT: der wohnungsinterne GANG ``raum_8`` (6,48 m², schon vor dem Slice
    WOHNUNG_PRIVAT) bekommt durch R4 zwei Sicherheitsleuchten, wo vorher null
    standen — R4 nimmt ihm Segment und Anker, damit fällt das stützende RZ weg
    und ``platzierung/deckung.py::verdichte_fluchtweg`` wählt seine Korridore
    allein über ``raum_typ``, ohne ``nutzungsklasse`` und ohne die Flags. Die
    Datei gehört Leonis (Board-Frage); hier wird der Stand NICHT grün gebogen
    und NICHT als xfail versteckt."""
    plan(pfad)
    from notbeleuchtung.hauptengine.pipeline import run
    from notbeleuchtung.hauptengine.registry import build_default_bundle

    ergebnis = run(build_default_bundle(), str(pfad), floor)
    privat = [(r.id, Polygon(r.polygon_mm).buffer(0))
              for r in ergebnis.raum.raeume
              if r.nutzungsklasse == "WOHNUNG_PRIVAT" and len(r.polygon_mm) >= 3]
    drin = [f"{rid}:{p.kind}" for p in ergebnis.platzierung.platzierungen
            for rid, poly in privat if poly.covers(Point(p.xy_mm))]
    assert not drin, f"{floor}: {len(drin)} Leuchte(n) in WOHNUNG_PRIVAT: {drin}"


# ── (g) Messfälle (i) und (iv) in der Zählweise aus § 6g ────────────────────
def test_messfall_i_stiegenhaus_raum_35(moll1og):
    """ZIELBILD seit Owner-Entscheid 2026-09-26 (Board-Frage 1, Option A) —
    S7c Runde 1 hat die Owner-Regel gebaut und die alte Abnahmezahl 17 NICHT
    erreicht; mit der gebauten Regel ist sie
    je Starttür unerreichbar (ein GRAPH-Segment je Tür mit korrigierter Rolle
    ``wohnungseingang``, ``fluchtweg.py:329ff``, ID ``seg_graph_<tuer>``).
    17 nur über (B) innere Türen als Start — gegen den Owner-Satz „die innere
    Tür wird zimmertuer" — oder (C) je innerer Tür ein Duplikat des äußeren
    Wegs, Start-Regel in ``fluchtweg.py`` (``MESSFALL_I_MOLL``,
    Board-Frage 1).

    § 6g Messfall (i), Mollgasse 1OG STIEGENHAUS ``raum_35``. Das Kriterium ist
    in BEIDEN Zählweisen verfehlt; keine davon rettet es. Ursache ist nicht die
    Durchleitung, sondern R2: die Wohnungseingangstüren hinter den privat
    gewordenen Vorräumen ``raum_2``/``raum_4`` werden zu ``zimmertuer`` und
    fallen als Fluchtweg-Start weg; ihre Wege liefen durch das Stiegenhaus.

    Owner-Diagnose 2026-09-21 (zweite Hälfte von F11, „die Stiegenhaustür ist
    sein Wohnungseingang"): wird ein Vorraum privat, muss die Rolle
    ``wohnungseingang`` an die ÄUSSERE Tür WANDERN (Vorraum → Stiegenhaus bzw.
    Vorraum → allgemeiner Gang) — es reicht nicht, die innere Tür zur
    ``zimmertuer`` zu machen. Abnahme von S7c: Start/Ziel-Segmente wieder 17,
    die acht Wege über das Stiegenhaus wieder da, jetzt mit der Stiegenhaustür
    als Start.

    **Gemessen in S7c Runde 1:** die Wanderung ist auf diesem Plan bereits
    erledigt — ``tuer_3``/``tuer_4`` tragen roh und korrigiert
    ``wohnungseingang`` und sind Start. Sie liefert zwei Wege statt acht, die
    Zahl bleibt 9. Hier wird NICHTS grün gebogen und NICHTS als xfail
    versteckt."""
    _, modell, _ = moll1og
    assert len(stuetzpunkt_segmente(modell, "raum_35")) == MESSFALL_I_MOLL[0]
    assert len(startziel_segmente(modell, "raum_35")) == MESSFALL_I_MOLL[1]


def test_messfall_i_acht_wege_ueber_das_stiegenhaus(moll1og):
    """Der dritte Owner-Punkt der S7c-Abnahme, aufgeschlüsselt und GEMESSEN:
    „die acht Wege über das Stiegenhaus zurück, jetzt mit der Stiegenhaustür als
    Start."

    Die zweite Hälfte des Satzes ist ERFÜLLT und wird hier festgehalten: die
    Stiegenhaustüren ``tuer_3``/``tuer_4`` (STIEGENHAUS ``raum_35`` ↔ die
    bestätigt privaten Vorräume ``raum_2``/``raum_4``) sind Fluchtweg-Start,
    ihre Wege ``seg_graph_tuer_3``/``tuer_4`` laufen durch das Stiegenhaus zum
    ``stair_exit``. Die Rolle ist dort auch nicht erst gewandert — sie sitzt roh
    auf der äußeren Tür (Regel 3 der Türtypisierung, STIEGENHAUS × VORRAUM).

    Die erste Hälfte („die ACHT Wege") ist NICHT erfüllt und mit der gebauten
    Regel je Starttür unerreichbar: die acht Wege starteten an den acht
    INNEREN Türen derselben zwei Vorräume, und für die sagt die Regel
    ``zimmertuer``. Ein GRAPH-Segment entsteht je Tür mit korrigierter Rolle
    ``wohnungseingang`` (``fluchtweg.py:329ff``, ID ``seg_graph_<tuer>``),
    die zwei äußeren Türen liefern also zwei Wege, nicht acht. Zurück kämen
    die acht nur über (B) die inneren Türen als Start — gegen den Owner-Satz
    „die innere Tür wird zimmertuer" — oder (C) je innerer Tür ein Duplikat
    des äußeren Wegs (Start-Regel in ``fluchtweg.py``). Diese Zusicherung hält
    beide Befunde fest, damit die Zahl nicht unbemerkt wandert.

    Owner-Entscheid 2026-09-26 (Board-Frage 1, Option A): die Abwesenheit der
    acht Wege ist ZIELBILD — ihre Startpunkte waren innere Türen privater
    Vorräume, und „privat heißt keine eigene Zirkulation" (§ 6g.10)."""
    _, modell, _ = moll1og
    ids = {s.segment_id for s in modell.zirkulation.segmente}
    assert {"seg_graph_tuer_3", "seg_graph_tuer_4"} <= ids, sorted(ids)
    assert [s for s in S7C_ACHT_WEGE if s in ids] == []


def test_messfall_i_auch_auf_rennweg_og1(og1):
    """Befund B3: derselbe Messfall ist AUCH auf Rennweg OG1 verfehlt, im
    Runde-3-Bericht stand nur der Mollgasse-Fall. Gemessen wurde dort
    STIEGENHAUS ``raum_14`` (Stützpunkt-Segmente 3 → 1, Zirkulationspunkte
    9 → 3) und ``rest_2`` (Start/Ziel 4 → 2).

    **Slice S7c: ZIELBILD** („Rennweg OG1 ``raum_14`` wieder 4 an ``rest_2``",
    Owner-GO 2026-09-26). Seit Runde 10 (G4) liegen alle drei Zahlen schon
    wieder auf HEAD — die Zusicherung hält sie dort fest.

    Die 4 hängen an Option W von ``raum_12`` (``top_2`` = AR/VR/WC ohne
    Aufenthaltsraum, weil ``raum_10`` untypisiert ist): ``tuer_10``/``tuer_11``
    sind korrigiert Wohnungseingänge und Start. Mit typisierter Wohnküche
    (Kanon-Punkt WOHNKÜCHE, @Enis) wird ``raum_12`` bestätigt privat und
    ``rest_2`` gemessen 2 (S7c Runde 2, § 6) — das wäre dann Folge des
    Kanons, kein S7c-Rückfall.

    **Slice S5c (Owner F3):** ``rest_2`` ist Liftschacht, seine 4 waren
    Lifttür-Wege (überholt, s. ``MESSFALL_I_OG1``); dieselben Wege enden an
    ``exit_durchgang_6`` und führen ``rest_1`` als Start/Ziel."""
    _, modell, _ = og1
    assert (len(stuetzpunkt_segmente(modell, "raum_14")),
            zirkulationspunkte(modell, "raum_14"),
            len(startziel_segmente(modell, "rest_2"))) == MESSFALL_I_OG1
    assert len(startziel_segmente(modell, "rest_1")) == MESSFALL_I_OG1_REST_1


def test_messfall_iv_gang_raum_34(moll1og):
    """§ 6g Messfall (iv), Mollgasse 1OG ``raum_34`` GANG 16,99 m².

    Die ANKERREGEL erreicht ihn über ``durchgang_10`` OHNE Wohnungseingang.
    Bis Runde 6 ohne Fixpunkt (unbestimmt): Schritt 2 zählte seine Vorräume
    ``raum_16``/``19``/``26`` nur, solange sie privat waren, und die
    Flur-Verfeinerung machte sie allgemein, sobald er allgemein war. Seit
    Board 6 (Owner 2026-09-21) begrenzen die Wohnungseingänge MIT Blatt
    ``tuer_14``/``20``/``21`` die Flur-Verfeinerung: die Vorräume sind
    privat, ``raum_34`` erschließt drei Wohnungen → ALLGEMEIN. Er behält
    beide Flags und seine 8 Anker, und die Wege aus allen drei Wohnungen
    laufen weiter durch ihn (``seg_graph_tuer_14``/``20``/``21``).
    Stützpunkt-Segmente HEAD 17 → Runde 6 9 → Runde 7 5: weggefallen sind
    in Runde 7 die Wege, die in Bad/WC HINTER den jetzt bestätigt privaten
    Vorräumen starteten (``seg_graph_tuer_29``/``30``/``31``/``32``) —
    derselbe Weg ab dem Wohnungseingang bleibt. Die Start/Ziel-Zuordnung
    (Runde 6: 3) liegt jetzt beim privaten Vorraum statt bei ``raum_34``
    (``start_raum`` ist die Seite, die kein Knoten ist). Die übrige
    Differenz zu HEAD ist Messfall (i), S7c.

    Runde 10 (G4, Owner 2026-09-22): hinter ``tuer_14``/``20``/``21`` liegen
    nur Bad und WC bzw. nichts — kein Aufenthaltsraum, also KEIN Entzug. Die
    Vorräume behalten Notlicht und Zirkulation; die vier Wege aus Bad/WC
    (``seg_graph_tuer_29``/``30``/``31``/``32``) laufen wieder durch
    ``raum_34``, und die Vorräume sind wieder Knoten: Stützpunkt-Segmente 9,
    Start/Ziel 3 — beides wieder Runde 6.

    **Slice S7c, Runde 1:** der Owner nennt ``raum_34`` Stützpunkt-Segmente
    wieder 17 als Abnahme. Die acht fehlenden sind die acht Wege des
    Messfalls (i); mit der gebauten Regel sind sie je Starttür unerreichbar
    (ein GRAPH-Segment je Tür mit korrigierter Rolle ``wohnungseingang``,
    ``fluchtweg.py:329ff``) und kämen nur über (B) oder (C) zurück (bei
    ``MESSFALL_I_MOLL``). Die 9 sind seit Owner-Entscheid 2026-09-26 (Option A)
    ZIELBILD — gemessen nach S7c unverändert. Start/Ziel 3 ist HEAD =
    Runde 6."""
    prov, modell, _ = moll1og
    r34 = next(r for r in modell.raeume if r.id == "raum_34")
    assert r34.nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"
    assert (r34.ist_fluchtweg, r34.ist_communal) == (True, True)
    assert r34.wohnung_id is None
    assert stuetzpunkt_segmente(modell, "raum_34") == [
        "seg_graph_tuer_14", "seg_graph_tuer_20", "seg_graph_tuer_21",
        "seg_graph_tuer_29", "seg_graph_tuer_3", "seg_graph_tuer_30",
        "seg_graph_tuer_31", "seg_graph_tuer_32", "seg_graph_tuer_4"]
    assert len(startziel_segmente(modell, "raum_34")) == 3
    assert len([a for a in modell.anker if a.raum_id == "raum_34"]) == 8
    assert not [w for w in prov.wohnungsklasse_warnungen
                if w.startswith("unbestimmt: raum_34 ")]
