"""stiegenhaus — synthetisches Stiegenhaus: Läufe, Richtung, Podest, Anker."""
from __future__ import annotations

from pathlib import Path

import ezdxf
from shapely.geometry import Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.stiegenhaus import baue_stiegenhaus_modell

# Raum 3×7 m: Lauf mit 10 Stufen (280-mm-Abstand, 1.2 m breit) unten,
# freies Podest oben, Tür an der Nordwand.
RAUM = Raum(id="stgh", raum_typ="STIEGENHAUS",
            polygon_mm=[(5000, 5000), (8000, 5000), (8000, 12000), (5000, 12000)],
            flaeche_m2=21.0)
TUER = Tuer(id="t1", xy_mm=(6500.0, 12000.0), breite_mm=900.0,
            von_raum="gang_1", nach_raum="stgh", tuer_detail="stiegenhaustuer")


def _plan(tmp_path: Path, nummern: bool):
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    w = "02-TWA-G00"
    doc.layers.add(w)
    for a, b in [((0, 0), (20000, 0)), ((20000, 0), (20000, 15000)),
                 ((20000, 15000), (0, 15000)), ((0, 15000), (0, 0))]:
        msp.add_line(a, b, dxfattribs={"layer": w})
    # 10 horizontale Stufenlinien, y = 5300 … 7820 (280 mm Abstand).
    for i in range(10):
        y = 5300 + i * 280
        msp.add_line((5900, y), (7100, y))
        if nummern:
            msp.add_text(str(i + 1), dxfattribs={"height": 100}
                         ).set_placement((7200, y))
    if not nummern:
        # Gehlinie mitten durch den Lauf, von unten (Antritt) nach oben.
        msp.add_line((6500, 5100), (6500, 8100))
    p = tmp_path / "stgh.dxf"
    doc.saveas(str(p))
    return lade_dxf(p)


def test_lauf_aus_nummern(tmp_path):
    modell, anker = baue_stiegenhaus_modell(_plan(tmp_path, True), RAUM, [], [TUER])
    assert len(modell.laeufe) == 1
    lauf = modell.laeufe[0]
    assert lauf.richtung == "auf"
    # Nummer 1 unten → Antritt unten.
    assert lauf.antritt_mm[1] < lauf.austritt_mm[1]
    assert modell.verbotszonen_mm, "Laufpolygon muss Verbotszone sein"
    assert modell.tuer_ids == ["t1"]
    typen = {a.typ for a in anker}
    assert {"PODEST", "ANTRITT", "AUSTRITT", "TUER"} <= typen


def test_lauf_aus_gehlinie(tmp_path):
    modell, _ = baue_stiegenhaus_modell(_plan(tmp_path, False), RAUM, [], [TUER])
    assert len(modell.laeufe) == 1
    assert modell.laeufe[0].richtung == "auf"
    assert modell.laeufe[0].antritt_mm[1] < modell.laeufe[0].austritt_mm[1]


def test_podest_und_lift_verbotszone(tmp_path):
    lift = Raum(id="lift_1", raum_typ="LIFT", nutzungsklasse="KEIN_RAUM",
                polygon_mm=[(5100, 9000), (6600, 9000), (6600, 10900), (5100, 10900)],
                flaeche_m2=2.85)
    modell, anker = baue_stiegenhaus_modell(
        _plan(tmp_path, True), RAUM, [lift], [TUER])
    assert any(p.ist_hauptpodest for p in modell.podeste)
    # Lift-Polygon ist Verbotszone …
    assert any(Polygon(v).equals(Polygon(lift.polygon_mm))
               for v in modell.verbotszonen_mm)
    # … und kein Anker liegt in einer Verbotszone (Läufe/Lift).
    sperren = [Polygon(v) for v in modell.verbotszonen_mm]
    for a in anker:
        if a.typ in ("ANTRITT", "AUSTRITT"):
            continue
        assert not any(s.contains(Point(a.xy_mm)) for s in sperren), a.id


def test_anker_winkel_geliefert(tmp_path):
    _, anker = baue_stiegenhaus_modell(_plan(tmp_path, True), RAUM, [], [TUER])
    tuer = next(a for a in anker if a.typ == "TUER")
    # Tür sitzt in der horizontalen Nordwand → Türwandwinkel 0° (mod 180).
    assert tuer.winkel_grad is not None and abs(tuer.winkel_grad % 180.0) < 1.0
    podest = next(a for a in anker if a.typ == "PODEST")
    assert podest.winkel_grad is not None
    # Fluchtrichtung abwärts = Richtung Antritt (nach unten, ~270°).
    assert tuer.fluchtrichtung_grad is not None
    assert 180.0 < tuer.fluchtrichtung_grad < 360.0
