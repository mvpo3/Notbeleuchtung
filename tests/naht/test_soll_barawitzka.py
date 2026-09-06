"""Soll-Tests Barawitzka EG — final_exit + brandschutztuer seit Fachteil 1
SCHARF; Rest Zielbild (xfail strict).

WICHTIGER PLAN-BEFUND (Analyse 2026-09, s. docs/OFFENE_FRAGEN.md): die 16
Farbe-96-Linien sind KATASTERGRENZEN (Layer »Kataster Grenzen«), KEINE
Fluchtweg-Linien; Farbe 30 = Wand-/Bau-Layer. Explizite FLW-Linien existieren
in diesem Plan NICHT — die Erwartung »≥16 Segmente quelle LINIE« ist mit
diesem Plan nicht erfüllbar. Der Test bleibt trotzdem als xfail stehen: die
Quelle »explizite Fluchtweg-Linie« wird generisch gebaut (Layer-Muster
FLW/09-WEG + materialien.yaml-Semantik FLUCHTWEG; Farbe 96 nur, wenn der
Layer nicht Kataster/Grenze/verm enthält) und greift auf anderen Plänen.
Brandschutz real: Layer »0._EG PP_2_970 Brandschutz« + 6 Texte
»Glaswand EI30 + A2« → Kandidaten für brandschutztuer.
"""
from pathlib import Path

import pytest

PLAN = Path("Projekte/_eingang/Barawitzka_EG.dxf")


@pytest.fixture(scope="module")
def rm():
    if not PLAN.exists():                        # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {PLAN}")
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ArchitekturRaumProvider().parse(str(PLAN), "EG")


def test_soll_final_exit(rm):
    """Scharf seit Fachteil 1: hauseingang-Typisierung → final_exit im EG."""
    assert any(a.typ == "final_exit" for a in rm.ausgaenge), "kein final_exit"


@pytest.mark.xfail(
    strict=True,
    reason="Plan hat KEINE FLW-Linien (Farbe 96 = Katastergrenzen) — s. Modul-Docstring",
)
def test_soll_segmente_aus_expliziten_linien(rm):
    linie = [s for s in rm.zirkulation.segmente if s.quelle == "LINIE"]
    assert len(linie) >= 16, f"nur {len(linie)} Segmente mit quelle LINIE"


def test_soll_brandschutztuer(rm):
    """Scharf seit Fachteil 1: EI30-Texte in 500 mm → brandschutztuer."""
    bst = [t for t in rm.tueren if t.tuer_detail == "brandschutztuer"]
    assert len(bst) >= 1, "keine Brandschutztür erkannt"


@pytest.mark.xfail(strict=True, reason="Stempel-Deckung heute typisiert ≥30 (E2E-Pin), Soll 41")
def test_soll_41_raeume_mit_stempel(rm):
    typisiert = [r for r in rm.raeume if r.raum_typ]
    assert len(typisiert) >= 41, f"nur {len(typisiert)} Räume mit Stempel typisiert"
