"""S4g — ein Ausgang braucht einen Türbezug, eine Balkontür ist nie Ausgang.

Owner 2026-09-23: „Ein Ausgang ohne Türbezug ist kein Ausgang." Owner-Auftrag
2026-09-30, Punkt 2b: Türbezug = Tür/Öffnung mit Raumseite und Rolle ≠
``balkontuer``; die EG-Ausnahme der Freiflächen-Regel (Mollgasse Südgarten-Tür,
S4g c) bleibt erhalten. Messung und Stand: ``LUECKEN.md`` § 13.
"""
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
    "S4g a offen (LUECKEN.md § 13): footprint.hauptausgaenge liefert exit_1 … exit_4 "
    "ohne Tür. Ohne sie (gemessen) fallen 10 von 14 GRAPH-Wegen weg (exit_4 9, exit_3 1: "
    "‚kein final_exit erreichbar‘), Leuchten 51 → 47, und "
    "test_soll_mollgasse::test_soll_hofausgaenge_cluster_a_und_b wird rot (Cluster A "
    "hängt nur an exit_3; die Hof-Türen tuer_52/tuer_68 haben beidseits raum_51, F-13)."))
def test_soll_mollgasse_eg_kein_ausgang_ohne_tuerbezug(moll):
    """Naht S4g a: ``footprint.hauptausgaenge`` erzeugt ``exit_1`` … ``exit_4``
    ohne Tür (Bogenpaar an der Außenkante)."""
    assert _ohne_tuer(moll) == []


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
