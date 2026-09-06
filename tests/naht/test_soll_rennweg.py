"""Soll-Tests Rennweg OG3 — Zielbild der Erkennung, heute noch nicht erreicht.

Alle Einzeltests sind ``xfail(strict=True)``: erfüllt die Erkennung ein Soll,
wird der Test XPASS → Suite bricht → das xfail wird im selben Commit scharf
geschaltet. Skip-Gate, wenn das CAD-Asset fehlt (CI ohne Projekte/).

Plan-Befunde (2026-09): 11 Zargentüren in Wall-Blöcken (T1..T11), zwei Stiegen
(Stair_1 mit Laufnummern 1-20, Stair_2 mit 1-6), Lift NUR als MTEXT
»AUFZUG 8 PERS. …« ohne X-Rechteck, keine FLW-Linien. stair_exit hat heute
keinen Producer (GT-MOLL-EG-05), tuer_detail/wohnung_id/nutzungsklasse sind
v1.2.0-Felder ohne Befüllung.
"""
from pathlib import Path

import pytest

PLAN = Path("Projekte/_eingang/Rennweg_OG3.dxf")


@pytest.fixture(scope="module")
def rm():
    if not PLAN.exists():                        # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {PLAN}")
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ArchitekturRaumProvider().parse(str(PLAN), "OG3")


@pytest.mark.xfail(strict=True, reason="stair_exit hat keinen Producer (GT-MOLL-EG-05)")
def test_soll_stair_exit_statt_final_exit(rm):
    """OG3 ist ein Regelgeschoß: Ausgang = Stiegenhaustür, kein Ausgang ins Freie."""
    stair = [a for a in rm.ausgaenge if a.typ == "stair_exit"]
    final = [a for a in rm.ausgaenge if a.typ == "final_exit"]
    assert len(stair) >= 1, "kein stair_exit erkannt"
    assert len(final) == 0, f"{len(final)} final_exit im Obergeschoß"


@pytest.mark.xfail(strict=True, reason="Segment-Herkunft (quelle) wird noch nicht gesetzt")
def test_soll_segmente_aus_graph(rm):
    """Ohne FLW-Linien im Plan müssen Segmente aus dem Zirkulationsgraphen kommen."""
    graph = [s for s in rm.zirkulation.segmente if s.quelle == "GRAPH"]
    assert len(graph) >= 1, "kein Segment mit quelle GRAPH"


@pytest.mark.xfail(strict=True, reason="tuer_detail wird noch nicht klassifiziert")
def test_soll_tueren_mit_detail(rm):
    """11 Zargentüren (T1..T11) sollen eine Tür-Rolle tragen."""
    mit_detail = [t for t in rm.tueren if t.tuer_detail is not None]
    assert len(mit_detail) >= 11, f"nur {len(mit_detail)} Türen mit tuer_detail"


@pytest.mark.xfail(strict=True, reason="Lift-Erkennung textbasiert (MTEXT AUFZUG) fehlt")
def test_soll_lift_raum(rm):
    """Lift existiert nur als MTEXT »AUFZUG …« + nächstes Rechteck 1.0-2.8 m."""
    lifte = [r for r in rm.raeume if r.raum_typ == "LIFT"]
    assert len(lifte) >= 1, "kein LIFT-Raum erkannt"


@pytest.mark.xfail(strict=True, reason="Wohnungsbildung (wohnung_id) fehlt")
def test_soll_wohnungs_gruppe(rm):
    """Mindestens eine Wohnung als wohnung_id-Gruppe (T7 = Wohnungseingang-Kandidat)."""
    gruppen = {r.wohnung_id for r in rm.raeume if r.wohnung_id}
    assert len(gruppen) >= 1, "keine wohnung_id-Gruppe gebildet"


@pytest.mark.xfail(strict=True, reason="nutzungsklasse wird noch nicht gesetzt")
def test_soll_keine_leuchten_in_wohnung_privat():
    """Pipeline-Smoke: kein Notlicht-Symbol in WOHNUNG_PRIVAT-Räumen."""
    if not PLAN.exists():                        # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {PLAN}")
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
