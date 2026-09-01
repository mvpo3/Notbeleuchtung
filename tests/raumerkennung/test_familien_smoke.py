"""Familien-Smoke: der echte Provider liefert auf allen vier CAD-Familien etwas.

Regressionsnetz für die Ausgangs-Kaskade (Board-Ticket B2): vorher lieferten
Fischamender/Barawitzka/Herrenholz **0 Ausgänge**. Bewusst nur ``> 0``-Assertions
— die exakten Zahlen (Mollgasse 192 Räume/4 final_exit, Fischamender 69/1,
Barawitzka 7/6, Herrenholz 474/10) verschieben sich mit jeder Heuristik-Anpassung.

Die realen Pläne sind groß und ggf. untracked → fehlende Datei = ``skip``
(Muster wie in ``conftest.py``). Herrenholz braucht ~20 s zum Parsen.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from notbeleuchtung.raumerkennung.provider import ArchitekturRaumProvider
from notbeleuchtung.raumerkennung.zirkulation import zirkulation_aus_dxf

REPO_ROOT = Path(__file__).resolve().parents[2]

# (Kurzname, Pfad relativ zum Repo, Fluchtweg-Layer erwartet?)
FAMILIEN = [
    ("mollgasse", "Projekte/Mollgasse/Erdgeschoß.dxf", True),
    ("fischamender",
     ("Projekte/BVH Fischamenderstraße/BT1/"
      "260320_938-AR-PP-11000-A_ERDGESCHOSS BT1.dxf"), True),
    # Barawitzka hat nachweislich KEINEN Fluchtweg-Layer → Segmente werden nicht gefordert.
    ("barawitzka", "Projekte/Barawitzkagasse/415_260415_PP_VA_1_3 0 EG.dxf", False),
    ("herrenholz", "Projekte/DXF_Herrenholzgasse/20230228_po_eg_V.dxf", True),
]


@pytest.mark.parametrize(("name", "rel_pfad", "mit_fluchtweg"), FAMILIEN,
                         ids=[f[0] for f in FAMILIEN])
def test_provider_liefert_raeume_und_ausgaenge(name, rel_pfad, mit_fluchtweg):
    pfad = REPO_ROOT / rel_pfad
    if not pfad.exists():
        pytest.skip(f"Realer Plan fehlt: {pfad}")

    modell = ArchitekturRaumProvider().parse(str(pfad), "EG")

    assert len(modell.raeume) > 0, f"{name}: keine Räume erkannt"
    assert len(modell.ausgaenge) > 0, f"{name}: keine Ausgänge erkannt"
    assert all(a.typ in ("final_exit", "stair_exit", "door") for a in modell.ausgaenge)

    if mit_fluchtweg:
        assert len(modell.zirkulation.segmente) > 0, f"{name}: keine Fluchtweg-Segmente"


def test_barawitzka_ohne_fluchtweg_layer():
    """Gegenprobe zur Parametrisierung: Barawitzka trägt keinen Fluchtweg-Layer."""
    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf

    pfad = REPO_ROOT / "Projekte/Barawitzkagasse/415_260415_PP_VA_1_3 0 EG.dxf"
    if not pfad.exists():
        pytest.skip(f"Realer Plan fehlt: {pfad}")
    assert zirkulation_aus_dxf(lade_dxf(pfad)).segmente == []
