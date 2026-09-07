"""Soll-Tests Mollgasse EG — teilweise schon erreicht, dann scharf.

Ist-Prüfung 2026-09-07 (``ArchitekturRaumProvider().parse('Projekte/_eingang/
Mollgasse_EG.dxf', 'EG')``): **2 STIEGENHAUS-Räume** + **2 LIFT-Räume**
(Fachteil 2: lift_erkennung, Blockname LIFT) → beide Soll-Tests scharf.
Neu (Fachteil 2): Stiegenhaus-Modelle + Anker; kein Anker und keine Leuchte
in Liftpolygonen (beide scharf — das Liftschacht-Ausstanzen nimmt der
Platzierung die Fläche).
"""
from pathlib import Path

import pytest

PLAN = Path("Projekte/_eingang/Mollgasse_EG.dxf")


@pytest.fixture(scope="module")
def rm():
    if not PLAN.exists():                        # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {PLAN}")
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ArchitekturRaumProvider().parse(str(PLAN), "EG")


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
