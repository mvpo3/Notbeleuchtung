"""Real-Asset-Naht: symbols/library.py gegen die echte CAD_Symbole/E-Symbole.dxf.

Sichert die Kette Mapping-YAML → Library-Block ab, BEVOR der Renderer sie
konsumiert: jeder block_name muss in der Library existieren (Blocknamen mit
Leerzeichen driften sonst still), Layer-Sync liefert das DoD-Layer-Grün,
Block-Import ist idempotent + origin-normalisiert.
"""
from __future__ import annotations

import ezdxf
import ezdxf.bbox as ezbbox
import pytest

from notbeleuchtung.symbols import library, load_symbol_mapping


@pytest.fixture(autouse=True)
def _fresh_cache():
    library.reset_cache()
    yield
    library.reset_cache()


def test_library_resolves_and_loads():
    doc = library.load_library()
    assert len(list(doc.blocks.block_names())) > 0


def test_every_mapping_block_exists_in_library():
    # load_mapping() validiert selbst fail-loud — hier zusätzlich explizit,
    # damit der Testname den Verstoß benennt.
    mapping = library.load_mapping()
    names = set(library.load_library().blocks.block_names())
    for key, entry in mapping.items():
        assert entry["block_name"] in names, f"{key}: {entry['block_name']!r} fehlt"
    # Mapping-Vokabular identisch mit dem der Naht-Invariante (Slice 2)
    assert set(mapping.keys()) == set(load_symbol_mapping().keys())


def test_sync_layers_adds_safety_layer_green():
    doc = ezdxf.new("R2018")
    added = library.sync_layers(doc)
    assert added > 0
    layer = doc.layers.get(library.SAFETY_LAYER)
    r, g, b = (30, 180, 80)
    assert layer.dxf.true_color == (r << 16) | (g << 8) | b
    # Idempotent
    assert library.sync_layers(doc) == 0


def test_import_block_idempotent_and_origin_normalized():
    doc = ezdxf.new("R2018")
    block_name = "notbeleuchtung richtungspfeil nach unten"
    library.import_block(doc, block_name)
    library.import_block(doc, block_name)  # zweiter Aufruf = No-op
    extents = ezbbox.extents(doc.blocks[block_name], fast=True)
    assert extents.has_data
    assert abs(extents.center.x) < 0.01
    assert abs(extents.center.y) < 0.01


def test_import_unknown_block_raises():
    doc = ezdxf.new("R2018")
    with pytest.raises(KeyError):
        library.import_block(doc, "gibt-es-nicht")


# In-Band-Extents-Grenze (units): die Lib enthält korrupte Blocks („nach rechts"
# 2606×2300) und Legenden („RETTUNGSZEICHEN" 861×4945) — beide weit jenseits. Die
# kuratierten Symbole liegen bei 1–11 units.
_IN_BAND_MAX = 50.0


def test_every_mapping_block_is_in_band():
    # Kurations-Guard: kein Mapping-Key darf auf einen korrupten/Legenden-Block
    # zeigen. Fängt versehentliches Mappen fehlskalierter Blocks.
    doc = library.load_library()
    for key, entry in library.load_mapping().items():
        block = doc.blocks[entry["block_name"]]
        extents = ezbbox.extents(block, fast=True)
        assert extents.has_data, f"{key}: {entry['block_name']!r} ohne Geometrie"
        size = extents.extmax - extents.extmin
        assert max(size.x, size.y) < _IN_BAND_MAX, (
            f"{key}: {entry['block_name']!r} out-of-band "
            f"({size.x:.1f}×{size.y:.1f} units) — korrupt/Legende?"
        )


@pytest.mark.parametrize("catalog_key", ["sicherheitsleuchte_stiege", "antipanik_wannenleuchte"])
def test_new_categories_import(catalog_key):
    # Neue Kategorien (Kind sicherheitsleuchte/antipanik) laden echte Blocks +
    # werden beim Import origin-normalisiert (INSERT-fähig am Platzierungspunkt).
    block_name = library.load_mapping()[catalog_key]["block_name"]
    doc = ezdxf.new("R2018")
    library.import_block(doc, block_name)
    assert block_name in doc.blocks
    extents = ezbbox.extents(doc.blocks[block_name], fast=True)
    assert extents.has_data
    assert abs(extents.center.x) < 0.01
    assert abs(extents.center.y) < 0.01
