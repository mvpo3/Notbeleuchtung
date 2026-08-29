"""raumlayer — Räume aus dediziertem Raum-Layer (Polygon + Stempel)."""
from __future__ import annotations

import ezdxf

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.raumlayer import hat_raum_layer, raeume_aus_layer


def _build_room_layer_dxf(path):
    """Mini-DXF mit Raum-Layer ``810 Raum``: geschlossenes Polygon + Stempel."""
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4  # mm
    msp = doc.modelspace()
    for lyr in ("02-TWA-G00-LEG-M0", "810 Raum"):
        if lyr not in doc.layers:
            doc.layers.add(lyr)
    # Wand-Rechteck (für Skala/Bounds)
    W = "02-TWA-G00-LEG-M0"
    corners = [(0, 0), (18000, 0), (18000, 12000), (0, 12000)]
    for i in range(4):
        msp.add_line(corners[i], corners[(i + 1) % 4], dxfattribs={"layer": W})
    # Raum-Polygon (geschlossene LWPOLYLINE) + Stempel im Polygon
    msp.add_lwpolyline([(1000, 1000), (8000, 1000), (8000, 9000), (1000, 9000)],
                       close=True, dxfattribs={"layer": "810 Raum"})
    msp.add_mtext("Wohnzimmer", dxfattribs={"layer": "810 Raum"}).set_location((4000, 5000))
    doc.saveas(str(path))
    return path


def test_raeume_aus_raum_layer(tmp_path):
    p = _build_room_layer_dxf(tmp_path / "room.dxf")
    plan = lade_dxf(p)
    assert hat_raum_layer(plan) is True
    raeume = raeume_aus_layer(plan)
    assert len(raeume) == 1
    r = raeume[0]
    assert r.raum_typ == "WOHNZIMMER"          # Stempel → classify_room
    assert abs(r.flaeche_m2 - 7000 * 8000 / 1e6) < 0.1  # 7×8 m = 56 m²
    assert len(r.polygon_mm) >= 4


def test_mollgasse_hat_keinen_raum_layer(synth_dxf):
    # Synth/Mollgasse: kein Raum-Layer → Reader liefert [] (Provider nutzt Fallback).
    assert raeume_aus_layer(lade_dxf(synth_dxf)) == []
