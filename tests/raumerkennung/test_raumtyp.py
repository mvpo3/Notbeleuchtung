"""S3 — raumtyp: Stempel → raum_typ + Flags (Point-in-Polygon)."""
from __future__ import annotations

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.raumtyp import beschrifte_raeume
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
