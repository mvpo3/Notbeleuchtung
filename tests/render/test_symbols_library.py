"""Real-Asset-Naht: symbols/library.py gegen CAD_Symbole/Notbeleuchtungssymbole_neu+.dxf.

Migration Phase A (2026-09-18): die neue Owner-Bibliothek ist die einzige
Symbolquelle. Sichert die Kette Registry-YAML → Library-Block ab, BEVOR der
Renderer sie konsumiert: jeder block_name muss in der Library existieren
(case-insensitiv — DXF-Blocknamen sind case-insensitiv), Layer-Sync liefert das
Vorlagen-Layer-Grün, Block-Import ist idempotent + origin-normalisiert, und die
effektive WELTGRÖSSE jedes Symbols (native Extents × scale_abs) liegt im
plausiblen Band (der alte native-units-Guard passt nicht mehr: die neue Lib
führt gewollt groß-native Blöcke wie RIVO-RZ-ARR_right mit 463 units, die
scale_abs auf ~636 mm Welt bringt).
"""
from __future__ import annotations

import ezdxf
import ezdxf.bbox as ezbbox
import pytest

from notbeleuchtung.symbols import library, load_symbol_mapping
from notbeleuchtung.symbols.inserter import DE_GLOBAL_SCALE


@pytest.fixture(autouse=True)
def _fresh_cache():
    library.reset_cache()
    yield
    library.reset_cache()


def test_library_resolves_and_loads():
    doc = library.load_library()
    assert len(list(doc.blocks.block_names())) > 0
    # Die aufgelöste Datei ist die neue Owner-Bibliothek.
    assert "rivo-sibel-arr-down" in {n.lower() for n in doc.blocks.block_names()}


def test_every_mapping_block_exists_in_library():
    # load_mapping() validiert selbst fail-loud — hier zusätzlich explizit,
    # damit der Testname den Verstoß benennt.
    mapping = library.load_mapping()
    names = {n.lower() for n in library.load_library().blocks.block_names()}
    for key, entry in mapping.items():
        assert entry["block_name"].lower() in names, f"{key}: {entry['block_name']!r} fehlt"
    # Mapping-Vokabular identisch mit dem der Naht-Invariante (Slice 2)
    assert set(mapping.keys()) == set(load_symbol_mapping().keys())


def test_sync_layers_adds_safety_layer_green():
    doc = ezdxf.new("R2018")
    added = library.sync_layers(doc)
    assert added > 0
    layer = doc.layers.get(library.SAFETY_LAYER)
    r, g, b = (30, 179, 80)   # true_color des Vorlagen-Layers (0x1EB350)
    assert layer.dxf.true_color == (r << 16) | (g << 8) | b
    # Idempotent
    assert library.sync_layers(doc) == 0


def test_import_block_idempotent_and_origin_normalized():
    doc = ezdxf.new("R2018")
    block_name = "RIVO-SIBEL-ARR-down"
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


# Weltgrößen-Band in mm: kleinstes Symbol = Aufheller/Spot (~97 mm), größtes =
# RZ-Schild (~636 mm) — gemessen an den Owner-Erklärungsplänen (Mollgasse).
_WELT_MIN_MM = 50.0
_WELT_MAX_MM = 1500.0


def test_every_mapping_block_weltgroesse_in_band():
    # Kurations-Guard-Nachfolger: kein Registry-Key darf ein Symbol in
    # unplausible Weltgröße skalieren (Fehlkalibrierung scale_abs / korrupte
    # Block-Extents fallen hier auf).
    doc = library.load_library()
    for key, entry in library.load_mapping().items():
        if entry.get("category") == "vorlage":
            continue   # Plan-Vorlage ist bewusst großformatig (kein Punktsymbol)
        block = doc.blocks[entry["block_name"]]
        extents = ezbbox.extents(block, fast=True)
        assert extents.has_data, f"{key}: {entry['block_name']!r} ohne Geometrie"
        size = extents.extmax - extents.extmin
        scale = float(entry.get("scale_abs", DE_GLOBAL_SCALE * float(entry.get("scale", 1.0))))
        welt = max(size.x, size.y) * scale
        assert _WELT_MIN_MM < welt < _WELT_MAX_MM, (
            f"{key}: {entry['block_name']!r} Weltgröße {welt:.0f} mm "
            f"(nativ {size.x:.1f}×{size.y:.1f} × scale {scale:g}) außerhalb Band"
        )


@pytest.mark.parametrize(
    "catalog_key",
    ["sicherheitsleuchte_aufheller", "antipanik_leuchte", "sicherheitsleuchte_spot"],
)
def test_new_categories_import(catalog_key):
    # Kategorien (Kind sicherheitsleuchte/antipanik) laden echte Blocks +
    # werden beim Import origin-normalisiert (INSERT-fähig am Platzierungspunkt).
    block_name = library.load_mapping()[catalog_key]["block_name"]
    doc = ezdxf.new("R2018")
    library.import_block(doc, block_name)
    assert block_name in doc.blocks
    extents = ezbbox.extents(doc.blocks[block_name], fast=True)
    assert extents.has_data
    assert abs(extents.center.x) < 0.01
    assert abs(extents.center.y) < 0.01


def test_aufheller_bleibt_blau():
    """Migration Phase A: die Library-Farben werden beim Import NICHT mehr
    umgeschrieben — der Owner-Aufheller ist ein voll BLAU gefüllter Kreis
    (HATCH ACI 150), das Erscheinungsbild ist Wahrheit."""
    doc = ezdxf.new("R2018")
    library.import_block(doc, "Sicherheitsleuchte Aufheller")
    farben = [getattr(e.dxf, "color", None) for e in doc.blocks["Sicherheitsleuchte Aufheller"]]
    assert 150 in farben
