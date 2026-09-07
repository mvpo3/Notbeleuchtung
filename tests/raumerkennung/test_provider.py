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


def test_doppelfluegel_verschmilzt_aussentor_tueren():
    """Spec 3d: Reihenfolge — Verschmelzen läuft NACH ``aussentor_tueren``,
    darum werden auch zwei benachbarte 'arc_aussen'-Türbögen zu EINER Tür."""
    from shapely.geometry import box

    from notbeleuchtung.raumerkennung.tueren import (
        TuerOeffnung,
        aussentor_tueren,
        verschmelze_doppelfluegel,
    )

    kontur = box(0.0, 0.0, 5000.0, 5000.0)          # Drehpunkte auf der Außenkante
    oeffnungen = [TuerOeffnung(xy_mm=xy, breite_mm=800.0, winkel_grad=0.0,
                               quelle="arc")
                  for xy in ((1000.0, 0.0), (2600.0, 0.0))]
    aussen = aussentor_tueren(oeffnungen, [], kontur)
    assert [t.quelle for t in aussen] == ["arc_aussen", "arc_aussen"]

    wand_segs = [((0.0, 0.0), (5000.0, 0.0))]       # gemeinsame Wand
    verschmolzen = verschmelze_doppelfluegel(aussen, wand_segs)
    assert len(verschmolzen) == 1
    assert verschmolzen[0].quelle == "doppelfluegel"
    assert verschmolzen[0].breite_mm == 1600.0
    assert verschmolzen[0].xy_mm == (1800.0, 0.0)
