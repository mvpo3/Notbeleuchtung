"""Soll-Tests Rennweg OG3 — seit Fachteil 1 (Tür-Zuordnung/-Typisierung,
Wohnungen, Ausgänge, Fluchtwege) größtenteils SCHARF (2026-09-06: Ist =
13 Türen mit Detail, 1 stiegenhaustuer → stair_exit, 0 final_exit im OG,
3 GRAPH-Segmente, 2 Wohnungen).

Seit Fachteil 2 auch die Lift-Erkennung scharf (textbasierter Pfad) sowie
Anker-/Stiegenhaus-Zusicherungen. Gemessen wird auf den versionierten Plänen
unter ``Projekte/Rennweg/`` (siehe ``tests/plaene.py``).

Plan-Befunde (2026-09): 11 Zargentüren in Wall-Blöcken (T1..T11), zwei Stiegen
(Stair_1 mit Laufnummern 1-20, Stair_2 mit 1-6), keine FLW-Linien.
"""
import pytest

from plaene import RENNWEG_EG as PLAN_EG
from plaene import RENNWEG_OG3 as PLAN
from plaene import plan


@pytest.fixture(scope="module")
def rm():
    plan(PLAN)
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ArchitekturRaumProvider().parse(str(PLAN), "OG3")


def test_soll_stair_exit_statt_final_exit(rm):
    """OG3 ist ein Regelgeschoß: Ausgang = Stiegenhaustür, kein Ausgang ins Freie."""
    stair = [a for a in rm.ausgaenge if a.typ == "stair_exit"]
    final = [a for a in rm.ausgaenge if a.typ == "final_exit"]
    assert len(stair) >= 1, "kein stair_exit erkannt"
    assert len(final) == 0, f"{len(final)} final_exit im Obergeschoß"


@pytest.mark.xfail(
    strict=True, raises=AssertionError,
    reason="S4a allein, Türstapel unvollständig, muss vor Merge XPASS sein — "
           "Gate-Bedingung (6) in docs/GATE_TUERSTAPEL.md")
def test_soll_segmente_aus_graph(rm):
    """Ohne FLW-Linien im Plan müssen Segmente aus dem Zirkulationsgraphen kommen."""
    graph = [s for s in rm.zirkulation.segmente if s.quelle == "GRAPH"]
    assert len(graph) >= 1, "kein Segment mit quelle GRAPH"


def test_soll_tueren_mit_detail(rm):
    """11 Zargentüren (T1..T11) sollen eine Tür-Rolle tragen."""
    mit_detail = [t for t in rm.tueren if t.tuer_detail is not None]
    assert len(mit_detail) >= 11, f"nur {len(mit_detail)} Türen mit tuer_detail"


def test_soll_lift_raum(rm):
    """Scharf seit Fachteil 2: textbasierter Pfad (MTEXT »AUFZUG …« →
    rotierter Kabinenumriss als minimales umschreibendes Rechteck)."""
    lifte = [r for r in rm.raeume if r.raum_typ == "LIFT"]
    assert len(lifte) >= 1, "kein LIFT-Raum erkannt"
    assert all(r.nutzungsklasse == "KEIN_RAUM" for r in lifte)


def test_soll_wohnungs_gruppe(rm):
    """Mindestens eine Wohnung als wohnung_id-Gruppe (T7 = Wohnungseingang-Kandidat)."""
    gruppen = {r.wohnung_id for r in rm.raeume if r.wohnung_id}
    assert len(gruppen) >= 1, "keine wohnung_id-Gruppe gebildet"


def test_soll_keine_leuchten_in_wohnung_privat():
    """Pipeline-Smoke: kein Notlicht-Symbol in WOHNUNG_PRIVAT-Räumen."""
    plan(PLAN)
    from shapely.geometry import Point, Polygon

    from notbeleuchtung.hauptengine.pipeline import run
    from notbeleuchtung.hauptengine.registry import build_default_bundle

    ergebnis = run(build_default_bundle(), str(PLAN), "OG3")
    privat = [
        Polygon(r.polygon_mm)
        for r in ergebnis.raum.raeume
        if r.nutzungsklasse == "WOHNUNG_PRIVAT" and len(r.polygon_mm) >= 3
    ]
    assert privat, "kein Raum mit nutzungsklasse WOHNUNG_PRIVAT"
    drin = [
        p.kind
        for p in ergebnis.platzierung.platzierungen
        if any(poly.covers(Point(p.xy_mm)) for poly in privat)
    ]
    assert not drin, f"{len(drin)} Leuchte(n) in WOHNUNG_PRIVAT: {drin[:5]}"


def test_stiegenhaus_modell_mit_laufrichtung(rm):
    """Fachteil 2: Stiegenhaus-Modell mit Läufen; Laufnummern 1..20 geben
    mindestens einem Lauf die Richtung »auf«."""
    assert len(rm.stiegenhaeuser) >= 1
    m = rm.stiegenhaeuser[0]
    assert len(m.laeufe) >= 2, f"nur {len(m.laeufe)} Treppenläufe"
    assert any(lf.richtung == "auf" for lf in m.laeufe), "keine Laufrichtung erkannt"
    assert m.verbotszonen_mm


@pytest.fixture(scope="module")
def rm_eg():
    plan(PLAN_EG)
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ArchitekturRaumProvider().parse(str(PLAN_EG), "EG")


def test_soll_eg_final_exit_via_text(rm_eg):
    """Rennweg EG (Plan-Befund 2026-09: 'TÜRSCHLIESSER'-Text an einer
    1340-mm-Lücke der Außenwand, KEIN Schwenkbogen, KEIN Block): die
    Text-Türquelle (b) liefert die Tür, die Typisierung macht sie zum
    hauseingang → ≥ 1 final_exit (Ist 2026-09-07: 3)."""
    final = [a for a in rm_eg.ausgaenge if a.typ == "final_exit"]
    assert final, "kein final_exit im EG"
    quellen = {t.id: (t.quelle or "") for t in rm_eg.tueren}
    begruendet = [a for a in final
                  if "text:" in quellen.get(a.id.removeprefix("exit_"), "")
                  or "windfang" in quellen.get(a.id.removeprefix("exit_"), "")]
    assert begruendet, "kein final_exit mit Text-/Windfang-Begründung"


def test_soll_eg_wege_enden_am_final_exit(rm_eg):
    """Geschoss-Zielregel: im EG endet jeder GRAPH-Weg an einem final_exit."""
    exits = {a.id: a.typ for a in rm_eg.ausgaenge}
    graph = [s for s in rm_eg.zirkulation.segmente if s.quelle == "GRAPH"]
    assert graph, "keine GRAPH-Segmente im EG"
    falsch = [s.segment_id for s in graph
              if exits.get(s.ziel_ausgang or "") != "final_exit"]
    assert not falsch, f"GRAPH-Wege ohne final_exit-Ziel: {falsch[:5]}"


@pytest.mark.xfail(
    strict=True,
    reason="Soll ≥ 90 % typisierte Türen je Familie — Ist Rennweg EG "
    "2026-09-07: 54 % (Gründe-Tabelle in bericht.md)",
)
def test_soll_eg_90_prozent_tueren_typisiert(rm_eg):
    typ = sum(1 for t in rm_eg.tueren if t.tuer_detail)
    assert rm_eg.tueren and typ / len(rm_eg.tueren) >= 0.9, (
        f"nur {typ}/{len(rm_eg.tueren)} Türen typisiert")


@pytest.mark.xfail(
    strict=True, raises=AssertionError,
    reason="S4a allein, Türstapel unvollständig, muss vor Merge XPASS sein — "
           "Gate-Bedingung (6) in docs/GATE_TUERSTAPEL.md")
def test_keine_anker_in_wohnung_privat(rm):
    """Fachteil 2: Anker nur in Erschließung (Stiegenhaus/Gang), nie in
    WOHNUNG_PRIVAT-Räumen."""
    from shapely.geometry import Point, Polygon

    assert rm.anker, "keine Anker geliefert"
    privat = [Polygon(r.polygon_mm) for r in rm.raeume
              if r.nutzungsklasse == "WOHNUNG_PRIVAT" and len(r.polygon_mm) >= 3]
    assert privat
    drin = [a.id for a in rm.anker
            if any(p.contains(Point(a.xy_mm)) for p in privat)]
    assert not drin, f"Anker in WOHNUNG_PRIVAT: {drin[:5]}"
