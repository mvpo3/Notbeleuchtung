"""Symbol-Infrastruktur — catalog_key → Schrack-CAD-Block.

Slice 2: das Mapping-Vokabular (`schrack_symbol_mapping.yaml`), gegen das die
Naht-Invariante `catalog_key ∈ Mapping` prüft. Slice 3: echte Insert-Infra in
`library.py` (E-Symbole.dxf-Loader, Layer-Sync, Block-Import) + `inserter.py`
(Platzierung → INSERT).

WICHTIG: Dieses `__init__` bleibt ezdxf-frei — platzierung/ importiert nur die
Mapping-Funktionen hier und lädt damit nie transitiv ezdxf/die CAD-Library.
"""
from __future__ import annotations

from pathlib import Path

import yaml

MAPPING_PATH = Path(__file__).with_name("schrack_symbol_mapping.yaml")


def load_symbol_mapping() -> dict[str, dict]:
    """Das catalog_key → Block-Spec-Mapping (Single Source für gültige Keys)."""
    with open(MAPPING_PATH, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def catalog_keys() -> set[str]:
    """Menge aller gültigen catalog_keys (für die Naht-Invariante)."""
    return set(load_symbol_mapping().keys())
