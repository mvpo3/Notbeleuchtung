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
