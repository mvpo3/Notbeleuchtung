"""lift_erkennung — synthetische Pläne: X-Rechteck, Achsenkreuz, Text, Blockname."""
from __future__ import annotations

from pathlib import Path

import ezdxf
import pytest
from shapely.geometry import Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum
from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.lift_erkennung import finde_lifte


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
