"""Soll-Tests Mollgasse EG — teilweise schon erreicht, dann scharf.

Ist-Prüfung 2026-09-07 (``ArchitekturRaumProvider().parse(<Projekte/Mollgasse/
Erdgeschoß.dxf>, 'EG')``): **2 STIEGENHAUS-Räume** + **2 LIFT-Räume**
(Fachteil 2: lift_erkennung, Blockname LIFT) → beide Soll-Tests scharf.
Neu (Fachteil 2): Stiegenhaus-Modelle + Anker; kein Anker und keine Leuchte
in Liftpolygonen (beide scharf — das Liftschacht-Ausstanzen nimmt der
Platzierung die Fläche).
"""
import pytest

from plaene import MOLLGASSE_EG as PLAN
from plaene import plan


@pytest.fixture(scope="module")
def provider():
    plan(PLAN)
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ArchitekturRaumProvider()


@pytest.fixture(scope="module")
def rm(provider):
    return provider.parse(str(PLAN), "EG")


def test_zwei_stiegenhaus_raeume(rm):
    """Scharf: Ist 2026-09-06 = 2 STIEGENHAUS (Stempel-Typisierung greift)."""
    stgh = [r for r in rm.raeume if r.raum_typ == "STIEGENHAUS"]
    assert len(stgh) >= 2, f"nur {len(stgh)} STIEGENHAUS-Räume"


def test_soll_zwei_lift_raeume(rm):
    """Scharf seit Fachteil 2: lift_erkennung akzeptiert Blockname LIFT +
    Achsenkreuz (Ist 2026-09-07 = 2 LIFT-Räume aus den LIFT-Blöcken)."""
    lifte = [r for r in rm.raeume if r.raum_typ == "LIFT"]
    assert len(lifte) >= 2, f"nur {len(lifte)} LIFT-Räume"
    assert all(r.nutzungsklasse == "KEIN_RAUM" for r in lifte)


def test_stiegenhaus_modelle(rm):
    """Fachteil 2: je STIEGENHAUS-Raum ein Modell mit Läufen + Verbotszonen."""
    assert len(rm.stiegenhaeuser) >= 2, f"nur {len(rm.stiegenhaeuser)} Stiegenhaus-Modelle"
    for m in rm.stiegenhaeuser:
        assert m.laeufe, f"{m.raum_id}: keine Treppenläufe erkannt"
        assert m.verbotszonen_mm, f"{m.raum_id}: keine Verbotszonen"


def test_keine_anker_in_liftpolygonen(rm):
    """Fachteil 2 scharf: Anker liegen nie im Liftschacht (Verbotszone)."""
    from shapely.geometry import Point, Polygon

    lifte = [Polygon(r.polygon_mm) for r in rm.raeume
             if r.raum_typ == "LIFT" and len(r.polygon_mm) >= 3]
    assert lifte
    assert rm.anker, "keine Anker geliefert"
    drin = [a.id for a in rm.anker
            if any(p.contains(Point(a.xy_mm)) for p in lifte)]
    assert not drin, f"Anker in Liftpolygonen: {drin[:5]}"


def test_soll_hofausgaenge_cluster_a_und_b(rm):
    """Scharf seit Außen-Analyse + Türquellen: der Hof ist AUSSEN (Wege ins
    Freie über die nördl. Grundstücksgrenze + Garagentor-Ostkante), die echten
    Türbögen der Hoftüren (Cluster A Innenhof-Osttrakt, Cluster B Südgarten)
    werden final_exit (Ist 2026-09-07 nach der Grundstücksgrenzen-Regel:
    9 final_exit gesamt)."""
    import math

    final = [a.xy_mm for a in rm.ausgaenge if a.typ == "final_exit"]
    cluster_a = (2689400.0, 1524600.0)   # Türbogen Innenhof-Osttrakt
    cluster_b = (2688620.0, 1511090.0)   # Südgarten-Tür b800
    for name, z in (("Cluster A", cluster_a), ("Cluster B", cluster_b)):
        assert any(math.dist(z, p) < 1500.0 for p in final), (
            f"kein final_exit an {name} {z}")


def test_soll_alle_graph_wege_enden_am_final_exit(rm):
    """Geschoss-Zielregel EG: jeder GRAPH-Weg endet an einem final_exit —
    stair_exit ist nur Zwischenknoten (Ist 2026-09-07: 15/15)."""
    exits = {a.id: a.typ for a in rm.ausgaenge}
    graph = [s for s in rm.zirkulation.segmente if s.quelle == "GRAPH"]
    assert graph, "keine GRAPH-Segmente"
    falsch = [s.segment_id for s in graph
              if exits.get(s.ziel_ausgang or "") != "final_exit"]
    assert not falsch, f"GRAPH-Wege ohne final_exit-Ziel: {falsch[:5]}"


def test_kreuzcheck_findet_endpunkte_an_der_aussenkante(provider, rm):
    """Scharf: der Kreuzcheck findet die Grad-1-WEG-Enden an der Gebäude-
    kante (Ist 2026-09-07: 43, davon Cluster A+B) und liefert je ungedecktem
    Endpunkt einen notausgang_kandidat (Prüf-Output, kein Ausgang)."""
    kc = provider.letzter_kreuzcheck
    assert len(kc.endpunkte_aussenkante) >= 10
    assert len(kc.kandidaten) == len(kc.warnungen)
    # Kandidaten sind KEINE Ausgänge: keine Contract-Ausgangs-ID nötig.
    assert all(k.typ == "notausgang_kandidat" for k in kc.kandidaten)


@pytest.mark.xfail(
    strict=True,
    reason="Soll: final_exit-Menge deckt JEDEN Grad-1-Linien-Endpunkt an der "
    "Außenkante (final_exit == Endpunktzahl) — Ist 2026-09-07: 3/43 gedeckt, "
    "40 Kandidaten (der 09-WEG-Layer zeichnet viele Doppellinien-Stummel; "
    "Dedup/Clustering der Endpunkte ist als offene Frage notiert)",
)
def test_soll_jeder_endpunkt_an_der_kante_hat_final_exit(provider, rm):
    kc = provider.letzter_kreuzcheck
    assert kc.endpunkte_aussenkante, "keine Endpunkte an der Außenkante"
    assert not kc.warnungen, (
        f"{len(kc.warnungen)}/{len(kc.endpunkte_aussenkante)} Endpunkte "
        "ohne final_exit")


@pytest.mark.xfail(
    strict=True,
    reason="Soll ≥ 90 % typisierte Türen je Familie — Ist Mollgasse EG "
    "2026-09-07: 48 % (Haupt-Grund unbekannte_kombination: Nachbarräume ohne "
    "Kanon-Typ; Gründe-Tabelle in bericht.md)",
)
def test_soll_90_prozent_tueren_typisiert(rm):
    typ = sum(1 for t in rm.tueren if t.tuer_detail)
    assert rm.tueren and typ / len(rm.tueren) >= 0.9, (
        f"nur {typ}/{len(rm.tueren)} Türen typisiert")


def test_soll_keine_leuchten_in_liftpolygonen():
    """Scharf (Ist 2026-09-07 = 0): seit dem Liftschacht-Ausstanzen aus den
    STIEGENHAUS-Polygonen platziert die Pipeline keine Leuchte mehr im
    Liftpolygon. Verbotszonen-Konsum in der Platzierung bleibt trotzdem
    Fachteil 3 (Leonis) — dieser Test friert den Ist-Zustand ein."""
    if not PLAN.exists():                        # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {PLAN}")
    from shapely.geometry import Point, Polygon

    from notbeleuchtung.hauptengine.pipeline import run
    from notbeleuchtung.hauptengine.registry import build_default_bundle

    ergebnis = run(build_default_bundle(), str(PLAN), "EG")
    lifte = [Polygon(r.polygon_mm) for r in ergebnis.raum.raeume
             if r.raum_typ == "LIFT" and len(r.polygon_mm) >= 3]
    assert lifte
    drin = [p.kind for p in ergebnis.platzierung.platzierungen
            if any(lp.covers(Point(p.xy_mm)) for lp in lifte)]
    assert not drin, f"{len(drin)} Leuchte(n) im Liftschacht: {drin[:5]}"


@pytest.mark.xfail(
    strict=True,
    reason="Soll (Spec 6): final_exit = Anzahl der 09-WEG-Endpunkte an der "
    "Außenkante — Ist 2026-09-07 (selbst gemessen): 9 final_exit gegen 43 "
    "Endpunkte an der Außenkante (103 LINIE-Segmente; der 09-WEG-Layer "
    "zeichnet Doppellinien-Stummel, Dedup/Clustering der Endpunkte offen).",
)
def test_soll_final_exit_anzahl_gleich_endpunkte_an_der_kante(provider, rm):
    kc = provider.letzter_kreuzcheck
    assert kc.endpunkte_aussenkante, "keine Endpunkte an der Außenkante"
    final = [a for a in rm.ausgaenge if a.typ == "final_exit"]
    assert len(final) == len(kc.endpunkte_aussenkante), (
        f"{len(final)} final_exit gegen {len(kc.endpunkte_aussenkante)} "
        "Endpunkte an der Außenkante")
