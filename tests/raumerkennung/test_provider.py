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


def test_mollgasse_leer_parse_ausgaenge(mollgasse_blank_eg):
    # Echter Input (Meter) → kalibriert; Ausgänge aus Außentüren, nicht Weg-Enden.
    rm = ArchitekturRaumProvider().parse(str(mollgasse_blank_eg), "EG")
    assert isinstance(rm, RaumModell)
    assert len(rm.ausgaenge) >= 1
    # Seit Fachteil 1 (tuer_typisierung/ausgaenge) liefert das EG zusätzlich
    # stair_exits (Stiegenhaustüren) — der Pin »alle final_exit« galt nur,
    # solange stair_exit keinen Producer hatte (GT-MOLL-EG-05).
    final = [a for a in rm.ausgaenge if a.typ == "final_exit"]
    assert len(final) >= 1
    # Obergrenze gegen Müll-Heuristiken (alt: 11 Weg-Endpunkte als Ausgänge).
    # Seit den zusätzlichen Türquellen (Außen-Analyse: Hof-/Gartentüren
    # Cluster A+B, Außenwand-Öffnungen der Durchfahrten) liegt das Ist bei 13
    # begründeten final_exits (jede Tür trägt `quelle`) — Deckel mitgezogen.
    assert len(final) <= 16
    RaumModell.model_validate(rm.model_dump(by_alias=True))
