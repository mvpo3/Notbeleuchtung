"""objekt_stiege — synthetische Treppe positiv, drei Negative, Block-Fall.

Der Matcher entscheidet ausschließlich über Geometrie: parallele Stufenlinien,
Teilung 250–350 mm, Laufbreite. Kein Blockname (`_STAIR_BLOCK`), kein Layername,
kein Raumpolygon.
"""
from __future__ import annotations

from pathlib import Path

import ezdxf
import pytest

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.objekt_stiege import finde_stiegen

W = "02-TWA-G00"


def _doc():
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4
    doc.layers.add(W)
    msp = doc.modelspace()
    for a, b in [((0, 0), (20000, 0)), ((20000, 0), (20000, 15000)),
                 ((20000, 15000), (0, 15000)), ((0, 15000), (0, 0))]:
        msp.add_line(a, b, dxfattribs={"layer": W})
    return doc


def _treppe(pfad: Path, *, nummern: bool = False, n: int = 10,
            teilung: float = 280.0, laenge: float = 1200.0) -> Path:
    """Muster wie tests/raumerkennung/test_stiegenhaus._plan."""
    doc = _doc()
    doc.layers.add("STG")
    msp = doc.modelspace()
    for i in range(n):
        y = 5300 + i * teilung
        msp.add_line((5900, y), (5900 + laenge, y), dxfattribs={"layer": "STG"})
        if nummern:
            msp.add_text(str(i + 1),
                         dxfattribs={"height": 100, "layer": "01-TXT"}
                         ).set_placement((5900 + laenge + 100, y))
    doc.saveas(str(pfad))
    return pfad


def test_treppe_positiv(tmp_path):
    """10 Stufen, 280 mm Teilung, 1,2 m breit → genau ein Kandidat."""
    kandidaten = finde_stiegen(lade_dxf(_treppe(tmp_path / "stg.dxf")))
    assert len(kandidaten) == 1
    k = kandidaten[0]
    assert k.layer_name == "STG"
    assert k.quelle == "msp"
    assert k.n_stufen == 10
    assert k.teilung_mm == 280.0
    assert k.konsistenz == 1.0
    assert k.winkel_grad == 0.0
    assert 0.0 < k.flaeche_m2 <= 60.0
    assert k.laufrichtung == "unbekannt"        # ohne Nummern und ohne Gehlinie
    # Deckel: ein Fahrradständer ist geometrisch nicht unterscheidbar (Modul-
    # Docstring) → NIE automatisch übernehmen.
    assert k.confidence == 0.84


def test_treppe_richtung_aus_laufnummern(tmp_path):
    kandidaten = finde_stiegen(
        lade_dxf(_treppe(tmp_path / "stg_num.dxf", nummern=True)))
    assert len(kandidaten) == 1
    k = kandidaten[0]
    assert k.laufrichtung == "auf"
    assert k.antritt_mm[1] < k.austritt_mm[1]   # Nummer 1 liegt unten
    assert k.confidence == 0.84                 # Deckel gilt auch mit Nummern


@pytest.mark.parametrize(("name", "kw"), [
    # 6 Linien, Teilung 280 mm, aber nur 280 mm lang (Mollgasse-Lüftungsbefund).
    ("lueftung", {"n": 6, "laenge": 280.0}),
    # Teilung außerhalb des Owner-Fensters 250–350 mm.
    ("teilung_500", {"n": 8, "teilung": 500.0}),
    # Nur das Wandrechteck: 15 000/20 000 mm sind keine Stufenlinien.
    ("nur_wand", {"n": 0}),
])
def test_negative(tmp_path, name, kw):
    assert finde_stiegen(lade_dxf(_treppe(tmp_path / f"{name}.dxf", **kw))) == []


def test_treppe_im_block(tmp_path):
    """Stufen nur in einer Blockdefinition, INSERT auf einem Symbol-Layer.

    Belegt den `_wcs_pts`-Abstieg OHNE `_STAIR_BLOCK`: der Blockname ist
    bedeutungslos.
    """
    doc = _doc()
    doc.layers.add("STG")
    blk = doc.blocks.new("IRGENDWAS")
    for i in range(10):
        blk.add_line((5900, 5300 + i * 280), (7100, 5300 + i * 280),
                     dxfattribs={"layer": "STG"})
    doc.modelspace().add_blockref("IRGENDWAS", (0, 0),
                                  dxfattribs={"layer": "SYMBOL"})
    pfad = tmp_path / "stg_block.dxf"
    doc.saveas(str(pfad))
    kandidaten = finde_stiegen(lade_dxf(pfad))
    assert len(kandidaten) == 1
    k = kandidaten[0]
    assert k.quelle == "block"
    assert k.n_stufen == 10
    assert k.teilung_mm == 280.0
