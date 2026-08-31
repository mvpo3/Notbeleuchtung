"""S3 — raumtyp: Stempel → raum_typ + Flags (Point-in-Polygon)."""
from __future__ import annotations

import pytest

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.raumtyp import beschrifte_raeume, raumtyp_flags
from notbeleuchtung.raumerkennung.waende import raeume_aus_waenden


def test_synth_stiegenhaus_zugeordnet(synth_dxf):
    plan = lade_dxf(synth_dxf)
    raeume = beschrifte_raeume(plan, raeume_aus_waenden(plan))
    stgh = [r for r in raeume if r.raum_typ == "STIEGENHAUS"]
    assert len(stgh) == 1                    # Stempel im linken Raum
    assert stgh[0].ist_fluchtweg is True
    assert stgh[0].ist_communal is True
    # rechter Raum hat keinen Stempel → leer
    assert any(r.raum_typ == "" for r in raeume)


@pytest.mark.parametrize(
    "label, erwartet, flucht",
    [
        ("VR", "VORRAUM", True),            # Vorraum-Abkürzung (Fischamender)
        ("AR", "ABSTELLRAUM", False),       # Abstellraum-Abkürzung
        ("TRH BT1 EG", "STIEGENHAUS", True),  # Treppenhaus — sicherheitskritisch
        ("Loggia", "BALKON", False),
    ],
)
def test_oesterr_abkuerzungen_token_exakt(label, erwartet, flucht):
    tf = raumtyp_flags(label)
    assert tf is not None, f"{label!r} sollte typisieren"
    assert tf[0] == erwartet
    assert tf[1] is flucht


@pytest.mark.parametrize("label", ["Garten", "Rasen", "Parkett", "Fahrräder", "Rampe"])
def test_abkuerzung_kein_substring_bleed(label):
    # „ar"/„vr" dürfen NICHT als Substring in Fremdwörtern (Garten, Fahrräder) greifen.
    assert raumtyp_flags(label) is None
