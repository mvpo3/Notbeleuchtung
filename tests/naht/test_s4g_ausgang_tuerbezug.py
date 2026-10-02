"""S4g — ein Ausgang braucht einen Türbezug, eine Balkontür ist nie Ausgang.

Owner 2026-09-23: „Ein Ausgang ohne Türbezug ist kein Ausgang." Owner-Auftrag
2026-09-30, Punkt 2b: Türbezug = Tür/Öffnung mit Raumseite und Rolle ≠
``balkontuer``; die EG-Ausnahme der Freiflächen-Regel (Mollgasse Südgarten-Tür,
S4g c) bleibt erhalten. Messung und Stand: ``LUECKEN.md`` § 13.

Abschnitt 5 (Owner-Entscheid 6, 2026-10-01, ``docs/AUFTRAG_2026-10-01.md`` § 5):
Ausgang = Übergang ins Freie, mit oder ohne Tür; Innenhof (Loch der äußeren
Gebäudekontur) ist kein Ausgang und kein Fluchtziel; keine Tür-in-1,5-m-Regel.
Die vier Ausgänge ohne Tür (``footprint.hauptausgaenge``) einzeln entschieden:
``LUECKEN.md`` § 27.
"""
import math

import pytest

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.ausgaenge import leite_ausgaenge
from notbeleuchtung.raumerkennung.tuer_zuordnung import AUSSEN
from plaene import MOLLGASSE_EG, RENNWEG_EG, plan


def _parse(pfad, floor):
    plan(pfad)
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ArchitekturRaumProvider().parse(str(pfad), floor)


def _ohne_tuer(modell) -> list[str]:
    """Ausgänge, deren ID (Konvention ``exit_<tuer_id>``) auf keine Tür zeigt."""
    tueren = {t.id for t in modell.tueren}
    return [a.id for a in modell.ausgaenge if a.id.removeprefix("exit_") not in tueren]


@pytest.fixture(scope="module")
def moll():
    return _parse(MOLLGASSE_EG, "EG")


@pytest.mark.xfail(strict=True, reason=(
    "S4g a teilweise (LUECKEN.md § 27, Abschnitt 5): exit_1/exit_2 münden nicht ins Freie "
    "und entfallen; exit_3/exit_4 bleiben ohne Tür, weil sie ins Freie münden (Owner-"
    "Entscheid 6: Ausgang mit oder ohne Tür). Ein türgebundener Ersatz fehlt: tuer_52 "
    "(Stiegenhaus → Garten) und tuer_64/tuer_65 (Laubengang → Garten) haben keine "
    "AUSSEN-Seite, weil die Flutungen raum_51/raum_41 ihre Außenseite decken (F-13). Ohne "
    "exit_3/exit_4 (gemessen § 13) fallen 10 von 14 GRAPH-Wegen weg (exit_4 9, exit_3 1), "
    "und test_soll_mollgasse::test_soll_hofausgaenge_cluster_a_und_b wird rot."))
def test_soll_mollgasse_eg_kein_ausgang_ohne_tuerbezug(moll):
    """Naht S4g a: ``footprint.hauptausgaenge`` erzeugt Ausgänge ohne Tür
    (Bogenpaar an der Außenkante); seit Abschnitt 5 nur noch ``exit_3`` und
    ``exit_4``."""
    assert _ohne_tuer(moll) == []


# Die vier footprint-Ausgänge des Stands fd5dedb, einzeln entschieden
# (LUECKEN.md § 27.3, je ein Bild unter Projekte/_ergebnis/Mollgasse_EG/ausgaenge/).
# Münden nicht ins Freie → kein Ausgang:
_NICHT_INS_FREIE = {
    "exit_1": (2703279.9, 1521765.1),   # Doppeltür EI2 30-C in Loch 0 der Außenkontur
    "exit_2": (2703364.9, 1524050.1),   # zwei fremde Bögen, im Gebäude
}
# Münden in den Garten außerhalb der Außenkontur → bleiben final_exit:
_INS_FREIE = {
    "exit_3": (2689945.7, 1523965.4),
    "exit_4": (2665832.8, 1537216.2),
}


def test_mollgasse_eg_innenhof_doppeltuer_ist_kein_ausgang(moll):
    """Owner-Entscheid 6: der Innenhof ist kein Ausgang und kein Fluchtziel.
    ``exit_1`` (Doppeltür aus dem Osttrakt in Loch 0 der Außenkontur) und
    ``exit_2`` (zwei fremde Bögen im Gebäude) münden nicht ins Freie: kein
    ``final_exit`` in 1,5 m, kein Fluchtweg mit diesem Ziel."""
    final = [a.xy_mm for a in moll.ausgaenge if a.typ == "final_exit"]
    nah = {k: [p for p in final if math.dist(p, xy) < 1500.0]
           for k, xy in _NICHT_INS_FREIE.items()}
    assert not any(nah.values()), nah
    ziele = {s.ziel_ausgang for s in moll.zirkulation.segmente}
    assert not ziele & set(_NICHT_INS_FREIE), ziele


def test_mollgasse_eg_durchgang_ins_freie_bleibt_final_exit(moll):
    """Owner-Entscheid 6: ein Ausgang braucht keine Tür. ``exit_3``/``exit_4``
    münden in den Garten außerhalb der Außenkontur und bleiben ``final_exit``;
    ebenso die Öffnung ohne Türblatt ``aussenoeffnung_1`` (AUSSEN-Seite)."""
    aus = {a.id: a for a in moll.ausgaenge}
    for k, xy in _INS_FREIE.items():
        assert k in aus and aus[k].typ == "final_exit", (k, sorted(aus))
        assert math.dist(aus[k].xy_mm, xy) < 1.0, (k, aus[k].xy_mm)
    assert aus["exit_aussenoeffnung_1"].typ == "final_exit"
    t = next(t for t in moll.tueren if t.id == "aussenoeffnung_1")
    assert t.ohne_tuerblatt is True
    assert AUSSEN in (t.von_raum, t.nach_raum)


def test_mollgasse_eg_messfall_suedgarten_und_hoftuer(moll):
    """Messfall S4g c (Owner 2026-09-23, vor dem Bau): die Südgarten-Tür
    ``tuer_67`` (AUSSEN | ``raum_61`` TERRASSE, Cluster B) bleibt ``final_exit``
    über ``ist_notausgang`` — die Freiflächen-Regel greift im EG nicht; die
    Hof-Tür ``tuer_68`` bleibt ``stair_exit``."""
    typ = {a.id: a.typ for a in moll.ausgaenge}
    assert typ.get("exit_tuer_67") == "final_exit"
    assert typ.get("exit_tuer_68") == "stair_exit"
    t67 = next(t for t in moll.tueren if t.id == "tuer_67")
    raum = {r.id: r for r in moll.raeume}
    seiten = {t67.von_raum, t67.nach_raum}
    assert AUSSEN in seiten
    (innen,) = seiten - {AUSSEN}
    assert raum[innen].raum_typ == "TERRASSE"
    assert t67.ist_notausgang is True
    assert t67.tuer_detail != "balkontuer"


def test_rennweg_eg_behaelt_seine_zwei_final_exit():
    rm = _parse(RENNWEG_EG, "EG")
    assert sorted(a.id for a in rm.ausgaenge if a.typ == "final_exit") == [
        "exit_tuer_18", "exit_tuer_8"]
    assert _ohne_tuer(rm) == []


def test_balkontuer_ist_nie_final_exit():
    """S4g b: die Kette endet in ``leite_ausgaenge``. Eine ``balkontuer`` ins
    Freie wird kein ``final_exit`` — auch dann nicht, wenn ein späterer Schritt
    (``markiere_windfang`` setzt ``ist_notausgang`` ohne Blick auf die Rolle)
    das Notausgang-Flag wieder setzt."""
    raeume = [Raum(id="wz", raum_typ="WOHNZIMMER"), Raum(id="gang", raum_typ="GANG")]
    tueren = [Tuer(id="t1", xy_mm=(0.0, 0.0), von_raum=AUSSEN, nach_raum="wz",
                   tuer_detail="balkontuer", ist_notausgang=True),
              Tuer(id="t2", xy_mm=(5000.0, 0.0), von_raum=AUSSEN, nach_raum="gang",
                   tuer_detail="hauseingang")]
    out, _ = leite_ausgaenge(tueren, raeume, "EG")
    assert [(a.id, a.typ) for a in out] == [("exit_t2", "final_exit")]
