"""S6 — provider: parse() liefert ein valides RaumModell (Naht zum Contract)."""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import RaumModell
from notbeleuchtung.raumerkennung import ArchitekturRaumProvider


def test_synth_parse_vollstaendig(synth_dxf):
    rm = ArchitekturRaumProvider().parse(str(synth_dxf), "EG")
    assert isinstance(rm, RaumModell)
    assert rm.floor == "EG"
    assert rm.coordinate_system == "mm"
    assert len(rm.raeume) == 2
    assert any(r.raum_typ == "STIEGENHAUS" for r in rm.raeume)
    assert len(rm.tueren) == 1
    assert len(rm.zirkulation.segmente) == 1
    # Contract-Roundtrip (Schema-Konformität)
    RaumModell.model_validate(rm.model_dump(by_alias=True))


def test_mollgasse_parse_valid(mollgasse_eg):
    rm = ArchitekturRaumProvider().parse(str(mollgasse_eg), "EG")
    assert isinstance(rm, RaumModell)
    assert len(rm.tueren) >= 10
    assert len(rm.zirkulation.segmente) > 0
    RaumModell.model_validate(rm.model_dump(by_alias=True))
