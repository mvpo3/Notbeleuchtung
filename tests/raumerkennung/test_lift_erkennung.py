"""lift_erkennung — synthetische Pläne: X-Rechteck, Achsenkreuz, Text, Blockname."""
from __future__ import annotations

from pathlib import Path

import ezdxf
import pytest
from shapely.geometry import Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum
from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.lift_erkennung import finde_lifte, liftschacht_reste


def _basis_doc():
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    # Wand-Rechteck ≥15 m, damit die Skala-Kalibrierung greift.
    w = "02-TWA-G00"
    doc.layers.add(w)
    for a, b in [((0, 0), (20000, 0)), ((20000, 0), (20000, 12000)),
                 ((20000, 12000), (0, 12000)), ((0, 12000), (0, 0))]:
        msp.add_line(a, b, dxfattribs={"layer": w})
    return doc, msp


def _plan(tmp_path: Path, doc):
    p = tmp_path / "lift.dxf"
    doc.saveas(str(p))
    return lade_dxf(p)


def _rect(msp, x0, y0, x1, y1, layer="0"):
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                       close=True, dxfattribs={"layer": layer})


def _stgh() -> list[Raum]:
    """Marker-Evidenz (X/Achsenkreuz) zählt nur in der Erschließung —
    Stiegenhaus-Raum um das Testrechteck (Barawitzka-Befund: Betten/Möbel)."""
    return [Raum(id="stgh_host", raum_typ="STIEGENHAUS",
                 polygon_mm=[(4000, 4000), (9000, 4000), (9000, 9000), (4000, 9000)],
                 flaeche_m2=25.0)]


def test_x_rechteck(tmp_path):
    doc, msp = _basis_doc()
    _rect(msp, 5000, 5000, 6650, 6900)
    msp.add_line((5000, 5000), (6650, 6900))
    msp.add_line((6650, 5000), (5000, 6900))
    lifte = finde_lifte(_plan(tmp_path, doc), _stgh())
    assert len(lifte) == 1
    assert lifte[0].raum_typ == "LIFT"
    assert lifte[0].nutzungsklasse == "KEIN_RAUM"


def test_achsenkreuz(tmp_path):
    doc, msp = _basis_doc()
    _rect(msp, 5000, 5000, 6650, 6900)
    msp.add_line((5825, 5000), (5825, 6900))    # Mittellinien (Mollgasse-Muster)
    msp.add_line((5000, 5950), (6650, 5950))
    lifte = finde_lifte(_plan(tmp_path, doc), _stgh())
    assert len(lifte) == 1


def test_text_pfad(tmp_path):
    doc, msp = _basis_doc()
    _rect(msp, 5000, 5000, 6650, 6900)          # kein Marker im Rechteck
    msp.add_mtext("AUFZUG 8 PERS. 630KG FAHRKABINE 110/140"
                  ).set_location((5900, 6000))
    lifte = finde_lifte(_plan(tmp_path, doc), [])
    assert len(lifte) == 1


def test_blockname(tmp_path):
    doc, msp = _basis_doc()
    blk = doc.blocks.new("LIFT")
    blk.add_lwpolyline([(0, 0), (1650, 0), (1650, 1900), (0, 1900)], close=True)
    msp.add_blockref("LIFT", (5000, 5000))
    lifte = finde_lifte(_plan(tmp_path, doc), [])
    assert len(lifte) == 1


def test_marker_ausserhalb_erschliessung_ist_kein_lift(tmp_path):
    """Barawitzka-Befund: Bett/Möbel mit Diagonalen in einem Wohnraum —
    X-Marker zählt nur in STIEGENHAUS/GANG."""
    doc, msp = _basis_doc()
    _rect(msp, 5000, 5000, 6650, 6900)
    msp.add_line((5000, 5000), (6650, 6900))
    msp.add_line((6650, 5000), (5000, 6900))
    zimmer = Raum(id="z1", raum_typ="SCHLAFZIMMER", flaeche_m2=25.0,
                  polygon_mm=[(4000, 4000), (9000, 4000), (9000, 9000), (4000, 9000)])
    assert finde_lifte(_plan(tmp_path, doc), [zimmer]) == []


def test_leeres_rechteck_ohne_evidenz(tmp_path):
    doc, msp = _basis_doc()
    _rect(msp, 5000, 5000, 6650, 6900)          # Rechteck allein ist kein Lift
    assert finde_lifte(_plan(tmp_path, doc), []) == []


def test_ausstanzen_aus_stiegenhaus(tmp_path):
    doc, msp = _basis_doc()
    _rect(msp, 5000, 5000, 6650, 6900)
    msp.add_line((5000, 5000), (6650, 6900))
    msp.add_line((6650, 5000), (5000, 6900))
    stgh = Raum(id="stgh_1", raum_typ="STIEGENHAUS",
                polygon_mm=[(4000, 4000), (9000, 4000), (9000, 9000), (4000, 9000)],
                flaeche_m2=25.0)
    raeume = [stgh]
    lifte = finde_lifte(_plan(tmp_path, doc), raeume)
    assert len(lifte) == 1
    assert lifte[0] in raeume                    # angehängt
    poly = Polygon(stgh.polygon_mm)
    assert not poly.contains(Point(5825, 5950)), "Lift nicht ausgestanzt"
    assert stgh.flaeche_m2 == pytest.approx(25.0 - 1.65 * 1.9, rel=0.05)


def _lift_mit_text(msp):
    """Kabine 1650 × 1900 mm (3,135 m²) mit Lift-Text, wie Rennweg (nur MTEXT)."""
    _rect(msp, 5000, 5000, 6650, 6900)
    msp.add_mtext("AUFZUG 8 PERS.").set_location((5900, 6000))


def _rest(x1, typ="STIEGENHAUS"):
    return Raum(id="rest_1", raum_typ=typ, ist_fluchtweg=True, ist_communal=True,
                polygon_mm=[(5000, 5000), (x1, 5000), (x1, 6900), (5000, 6900)],
                flaeche_m2=(x1 - 5000) * 1.9 / 1000)


@pytest.mark.parametrize(("x1", "typ", "flags"), [
    (8000, "SCHACHT", (False, False)),        # Kabinenanteil 1650/3000 = 0,55
    (8667, "STIEGENHAUS", (True, True)),      # Kabinenanteil 1650/3667 = 0,45
])
def test_liftschacht_rest_ab_mehr_als_halber_kabine(tmp_path, x1, typ, flags):
    """S5c, Owner-Entscheid F1 (K1_T): eine Stiegenhausfläche, die zu mehr als
    der Hälfte Liftkabine ist, ist Liftschacht (Rennweg-Schachtreste 0,635–0,684,
    Muthgasse 0,551/0,574; Stiegenhaus-Reste mit innenliegendem Lift ≤ 0,204)."""
    doc, msp = _basis_doc()
    _lift_mit_text(msp)
    rest = _rest(x1)
    ids = liftschacht_reste(_plan(tmp_path, doc), [rest])
    assert (rest.raum_typ, (rest.ist_fluchtweg, rest.ist_communal)) == (typ, flags)
    assert ids == (["rest_1"] if typ == "SCHACHT" else [])


def test_liftschacht_nur_aus_stiegenhaus(tmp_path):
    """Die Regel typisiert nur STIEGENHAUS um — ein Gang mit 0,55 bleibt Gang."""
    doc, msp = _basis_doc()
    _lift_mit_text(msp)
    gang = _rest(8000, "GANG")
    assert liftschacht_reste(_plan(tmp_path, doc), [gang]) == []
    assert gang.raum_typ == "GANG"


def test_liftschacht_rest_bleibt_ungestanzt_lift_bleibt(tmp_path):
    """Nach K1_T findet ``finde_lifte`` die Kabine weiter (Text-Evidenz) und
    stanzt den SCHACHT-Rest nicht aus — ausgestanzt wird nur STIEGENHAUS."""
    doc, msp = _basis_doc()
    _lift_mit_text(msp)
    plan = _plan(tmp_path, doc)
    rest = _rest(8000)
    raeume = [rest]
    liftschacht_reste(plan, raeume)
    vorher = list(rest.polygon_mm)
    assert len(finde_lifte(plan, raeume)) == 1
    assert rest.polygon_mm == vorher and rest.bereinigung == []


def test_marker_kabine_im_liftschacht_rest_bleibt_lift(tmp_path):
    """Muthgasse E2 (gemessen, S5c r1): die Kabinen ``lift_4``/``lift_5`` sind
    nur per Marker belegt, und Marker zählen nur in der Erschließung. Nach K1_T
    ist ihr Rest SCHACHT — ohne die durchgereichten IDs fände ``finde_lifte``
    die Kabine nicht mehr."""
    doc, msp = _basis_doc()
    _rect(msp, 5000, 5000, 6650, 6900)
    msp.add_line((5000, 5000), (6650, 6900))
    msp.add_line((6650, 5000), (5000, 6900))
    plan = _plan(tmp_path, doc)
    raeume = [_rest(8000)]
    ids = liftschacht_reste(plan, raeume)
    assert ids == ["rest_1"]
    assert len(finde_lifte(plan, raeume, ids)) == 1
