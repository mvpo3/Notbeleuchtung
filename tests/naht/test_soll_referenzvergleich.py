"""Soll-Test Referenzvergleich — eigene Platzierung gegen den Fachplaner-Plan.

Referenz: din_support_ReMi_Barawitzkagasse (EG-Frame, 11 Leuchten; Frame-Offset
(-48.44, -39.04) m, docs/REFERENZ_PLATZIERUNG.md §1). Treffer = eigene Leuchte
≤1 m UND Rotations-Δ ≤10° (Panel-Achse mod 180) an einer Referenzleuchte.
Matching/Extraktion = dieselben Funktionen wie die Prüfstrecke
(scripts/plan_pruefen.py, 07_referenzvergleich.png) — eine Quelle der Wahrheit.

Zielbild (xfail strict): ≥80 % Trefferquote. Kippt der xfail (XPASS), Test
scharf drehen.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

from plaene import BARAWITZKA_EG as PLAN
from plaene import plan

REPO = Path(__file__).resolve().parents[2]
REFERENZ = (REPO / "DIN-Notbeleuchtungspläne(Beispiele)"
            / "din_support_ReMi_Barawitzkagasse_28.04.2026.dxf")


def _lade_plan_pruefen():
    spec = importlib.util.spec_from_file_location(
        "plan_pruefen", REPO / "scripts" / "plan_pruefen.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["plan_pruefen"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def quote():
    plan(PLAN)
    if not REFERENZ.exists():                    # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Asset nicht vorhanden: {REFERENZ}")
    from notbeleuchtung.hauptengine.registry import build_default_bundle

    pp = _lade_plan_pruefen()
    bundle = build_default_bundle()
    modell = bundle.raum.parse(str(PLAN), "EG")
    platz = bundle.platzierer.place(modell, bundle.norm, None)
    refs = pp._referenz_leuchten("Barawitzka_EG", modell.bounds_mm)
    assert refs, "keine Referenz-Leuchten im EG-Frame gefunden"
    treffer, fehlend, _ueber = pp._referenz_match(refs, platz)
    basis = len(treffer) + len(fehlend)
    return len(treffer) / basis if basis else 0.0


@pytest.mark.xfail(
    strict=True,
    reason="Zielbild: ≥80 % der Fachplaner-EG-Leuchten haben ein eigenes "
    "Gegenstück (≤1 m, Rotation ≤10°) — die Platzierungs-Strategien sind "
    "noch nicht referenz-deckend",
)
def test_soll_referenz_trefferquote(quote):
    assert quote >= 0.80, f"Trefferquote {quote * 100:.0f} % < 80 %"
