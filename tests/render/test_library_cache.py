"""library-Cache — Isolations-Regression für den Block-Normalisierungs-Status.

Aufgedeckt bei der Verifikation des Wissensabgleich-Branches: der Cache war per
`id(output_doc)` gekeyt. Eine id() ist nur unter LEBENDEN Objekten eindeutig — wird
ein früherer ezdxf-Drawing GC'd, kann ein späterer dieselbe id() erben und würde das
stale „schon normalisiert"-Set erben. Folge: Blöcke bleiben un-zentriert (falsche
Geometrie in Tests, die Blöcke sequentiell importieren, UND im Batch-Rendering
mehrerer Pläne je Prozess). Fix: WeakKeyDictionary, gekeyt am Doc-Objekt.
"""
import gc
import weakref

import ezdxf

from notbeleuchtung.symbols import library, load_symbol_mapping


def test_normalisierung_cache_ist_weak_und_stirbt_mit_dem_doc():
    """Exakte Mechanik: Eintrag existiert nach Import, verschwindet mit dem Doc →
    keine id()-Erbschaft möglich."""
    library.reset_cache()
    assert isinstance(library._normalized_blocks_by_doc, weakref.WeakKeyDictionary)
    block = load_symbol_mapping()["notlicht_ks_stiege_rechts"]["block_name"]

    doc = ezdxf.new("R2018")
    library.import_block(doc, block)
    assert doc in library._normalized_blocks_by_doc
    assert block in library._normalized_blocks_by_doc[doc]

    del doc
    gc.collect()
    assert len(library._normalized_blocks_by_doc) == 0
    library.reset_cache()
