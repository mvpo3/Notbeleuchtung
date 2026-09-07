"""gang_anker — Anker entlang der Gang-Mittelachse (reine Geometrie)."""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts.raum_modell import (
    FluchtwegSegment,
    Raum,
    Tuer,
)
from notbeleuchtung.raumerkennung.gang_anker import anker_fuer_gang

# Gerader Gang 30×2 m mit zwei Türen und einem Fluchtweg-Segment zum Ausgang.
GANG = Raum(id="gang_1", raum_typ="GANG",
            polygon_mm=[(0, 0), (30000, 0), (30000, 2000), (0, 2000)],
            flaeche_m2=60.0, ist_fluchtweg=True)
TUEREN = [
    Tuer(id="t1", xy_mm=(5000.0, 0.0), von_raum="gang_1", nach_raum="raum_9"),
    Tuer(id="t2", xy_mm=(20000.0, 2000.0), von_raum="raum_8", nach_raum="gang_1"),
    Tuer(id="t9", xy_mm=(90000.0, 90000.0), von_raum="a", nach_raum="b"),  # fremd
]
SEG = FluchtwegSegment(
    segment_id="seg_graph_t1", reason="exit", quelle="GRAPH",
    polyline_mm=[(5000.0, 1000.0), (29000.0, 1000.0)], laenge_mm=24000.0,
    ziel_ausgang="exit_t2")


def test_anker_typen_und_lage():
    anker = anker_fuer_gang(GANG, TUEREN, [SEG])
    typen = {a.typ for a in anker}
    assert {"TUER", "ENDE", "STRECKE"} <= typen
    assert all(a.raum_id == "gang_1" for a in anker)
    # Fremde Tür t9 erzeugt keinen Anker.
    tuer_anker = [a for a in anker if a.typ == "TUER"]
    assert len(tuer_anker) == 2
    # TUER-Anker = Lot auf die Mittelachse (y ≈ 1000).
    assert all(abs(a.xy_mm[1] - 1000.0) < 300.0 for a in tuer_anker)


def test_tuerwandwinkel_und_fluchtrichtung():
    anker = anker_fuer_gang(GANG, TUEREN, [SEG])
    tuer = [a for a in anker if a.typ == "TUER"]
    # Türen sitzen in horizontalen Wänden → Wandwinkel 0° (mod 180).
    assert all(a.winkel_grad is not None and a.winkel_grad % 180.0 < 1.0
               for a in tuer)
    # Segment läuft nach +x zum Ausgang → Fluchtrichtung ≈ 0°/360°.
    for a in tuer:
        f = a.fluchtrichtung_grad
        assert f is not None and (f < 10.0 or f > 350.0)


def test_strecke_alle_10m():
    anker = anker_fuer_gang(GANG, TUEREN, [SEG])
    strecken = [a for a in anker if a.typ == "STRECKE"]
    assert 1 <= len(strecken) <= 3          # 30-m-Gang → ~2 Zwischenpunkte


def test_richtungswechsel_im_l_gang():
    l_gang = Raum(id="gang_l", raum_typ="GANG", flaeche_m2=56.0,
                  polygon_mm=[(0, 0), (20000, 0), (20000, 12000), (18000, 12000),
                              (18000, 2000), (0, 2000)])
    anker = anker_fuer_gang(l_gang, [], [])
    assert any(a.typ == "RICHTUNGSWECHSEL" for a in anker), (
        "L-Gang muss einen Richtungswechsel-Anker liefern")


def test_degenerierter_raum():
    assert anker_fuer_gang(
        Raum(id="x", raum_typ="GANG", polygon_mm=[]), [], []) == []
