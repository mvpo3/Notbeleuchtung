"""Symbol-Infrastruktur — catalog_key → Schrack-CAD-Block.

Slice 2: nur das Mapping-Vokabular (`schrack_symbol_mapping.yaml`), gegen das die
Naht-Invariante `catalog_key ∈ Mapping` prüft. Die echte Insert-/Render-Infra
(E-Symbole.dxf, insert_symbol) kommt mit dem Render-Slice (3) in `hauptengine/`.
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
