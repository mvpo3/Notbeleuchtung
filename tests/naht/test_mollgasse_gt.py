"""Mollgasse-Ground-Truth-Regression (Owner-Auftrag 2026-09-20).

Die GT-Fixtures (`tests/fixtures/mollgasse_gt/<G>.json`) sind die eingefrorene
Mess-Basis des Experten-Abgleichs (Extraktor: `scripts/analyse/
mollgasse_gt_extract.py`, Vergleich: `mollgasse_gt_vergleich.py`). Dieser Test
friert die Kennzahlen exakt ein — kippt der Extraktor oder ändert jemand die
Fixtures unbemerkt, bricht er. Der Voll-Vergleich Engine↔GT (pipeline.run auf
den leeren Plänen, Minuten je Geschoss) bleibt bewusst im Analyse-Skript;
gegen die Erklärungs-DXFs re-extrahiert wird nur, wenn die Assets lokal
liegen (Asset-Skip-Konvention).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
GT = REPO / "tests" / "fixtures" / "mollgasse_gt"
ERKL = REPO / "knowledge" / "Pläne zeichnen Wissen" / "Mollgasse-Notbeleuchtungserklärung"

# Eingefrorene Mess-Basis 2026-09-20 (EG = Owner-Fassung 20.09., bereinigt).
_SOLL = {
    # geschoss: (n_leuchten, n_beidseitig_gruppen)
    "EG": (18, 1), "1OG": (11, 0), "2OG": (11, 0), "3OG": (4, 0),
    "4OG": (7, 0), "DG": (6, 0), "1KG": (14, 1), "2KG": (36, 6),
}


@pytest.mark.parametrize("geschoss", sorted(_SOLL))
def test_gt_fixture_kennzahlen_exakt(geschoss):
    daten = json.loads((GT / f"{geschoss}.json").read_text(encoding="utf-8"))
    n_soll, beidseitig_soll = _SOLL[geschoss]
    assert daten["n_leuchten"] == n_soll
    assert daten["n_beidseitig_gruppen"] == beidseitig_soll
    assert len(daten["leuchten"]) == n_soll
    # Jede Leuchte trägt die Mess-Pflichtfelder (bbox-Zentrum, Rotation).
    for leuchte in daten["leuchten"]:
        assert leuchte["xy_mm"] is not None, leuchte["handle"]
        assert "rot_deg" in leuchte and "xscale" in leuchte


def test_gt_richtungs_rz_haben_welt_pfeil():
    for geschoss in _SOLL:
        daten = json.loads((GT / f"{geschoss}.json").read_text(encoding="utf-8"))
        for leuchte in daten["leuchten"]:
            if leuchte["typ"] == "rz":
                assert leuchte["welt_pfeil_deg"] is not None, (
                    geschoss, leuchte["handle"])


def test_extraktor_reproduziert_eg():
    dxf = ERKL / "WHA_MOL_EG_Notbeleuchtung_Erklärung.dxf"
    if not dxf.is_file():
        pytest.skip("Mollgasse-Erklärungs-DXF nicht im Checkout (Asset lokal)")
    import sys
    sys.path.insert(0, str(REPO / "scripts" / "analyse"))
    from mollgasse_gt_extract import extrahiere

    frisch = extrahiere("EG")
    fixture = json.loads((GT / "EG.json").read_text(encoding="utf-8"))
    assert frisch["n_leuchten"] == fixture["n_leuchten"]
    assert frisch["n_beidseitig_gruppen"] == fixture["n_beidseitig_gruppen"]
    assert {le["handle"] for le in frisch["leuchten"]} == {
        le["handle"] for le in fixture["leuchten"]}
