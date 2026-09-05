"""library.py — Loader für CAD_Symbole/E-Symbole.dxf (Port aus elektro-planer).

Portiert aus elektro-planer backend/symbols/schrack_library.py (siehe
docs/PORT_LOG.md). Liest die Schrack-Symbol-Library einmal und cacht sie;
Helfer zum Layer-Sync und Block-Import in ein Output-DXF via
ezdxf.addons.Importer. Der Importer ist per-output_doc und wird NICHT global
gecacht — nur die geladene Library und das validierte Mapping.

Divergenz zum Original: Pfad-Resolution ohne elektro-planer config.py —
explizites Argument → env `NOTBELEUCHTUNG_SYMBOL_LIB` → Aufwärts-Suche nach
`CAD_Symbole/E-Symbole.dxf` ab dieser Datei (src-Layout: Repo-Root).
"""
from __future__ import annotations

import logging
import os
import threading
from pathlib import Path
from typing import Any

import ezdxf
import ezdxf.bbox as ezbbox
from ezdxf.addons import Importer
from ezdxf.document import Drawing
from ezdxf.math import Matrix44

from notbeleuchtung.symbols import load_symbol_mapping

log = logging.getLogger(__name__)

# Kräftiges Schrack-Grün für die Leuchten-Geometrie-Ebene. Die Library führt
# ACI=100, das auf weißem Hintergrund zu dunkel rendert. Ausgabe-Layer folgt dem
# DIN_SIBEL-Schema (din_SIBEL_10_emergency_lighting, siehe dxf_renderer); der
# physische Lib-Layer heißt weiter `E_Sicherheitsbeleuchtung` und wird beim Sync
# auf den DIN_SIBEL-Namen umbenannt (Block-Geometrie liegt auf Layer '0', erbt
# also den INSERT-Layer — kein Umschreiben der Block-Definitionen nötig).
_SAFETY_GREEN_RGB = (30, 180, 80)
_LIB_SAFETY_LAYER = "E_Sicherheitsbeleuchtung"
SAFETY_LAYER = "din_SIBEL_10_emergency_lighting"

# Blaue Hardcode-Farben in Library-Blöcken (z.B. SL-Aufheller: SOLID-HATCH ACI 150).
# Explizite Entity-Farben übergehen den Layer-Grün-Override → beim Import auf
# BYLAYER stellen, damit Notlicht-Geometrie das Schrack-Grün erbt (Block liegt auf
# Layer '0' und erbt den INSERT-Layer). Schwarz/Grün der RZ-Piktogramme bleibt.
_BLAUE_ACI = {5} | set(range(130, 176))
_BYLAYER = 256

_ENV_VAR = "NOTBELEUCHTUNG_SYMBOL_LIB"
_LIB_RELPATH = Path("CAD_Symbole") / "E-Symbole.dxf"

# Pflichtfelder je Mapping-Eintrag (Vokabular kommt aus symbols/__init__.py,
# die Block-Existenz-Validierung gegen die echte Library passiert hier).
_REQUIRED_FIELDS = ("block_name", "label", "category")

# Modul-Cache, lazy unter Lock. RLock, damit load_mapping → load_library
# sich nicht selbst deadlockt.
_lock = threading.RLock()
_library_doc: Drawing | None = None
_mapping: dict[str, dict[str, Any]] | None = None
_normalized_blocks_by_doc: dict[int, set[str]] = {}


def _resolve_library_path(path: Path | str | None = None) -> Path:
    """Erster existierender Kandidat: Arg → env → Aufwärts-Suche ab Datei."""
    candidates: list[Path] = []
    if path is not None:
        candidates.append(Path(path))
    env = os.environ.get(_ENV_VAR)
    if env:
        candidates.append(Path(env))
    for parent in Path(__file__).resolve().parents:
        candidates.append(parent / _LIB_RELPATH)
    for cand in candidates:
        if cand.is_file():
            return cand
    raise FileNotFoundError(
        "Schrack-Library E-Symbole.dxf nicht gefunden. Kandidaten:\n  - "
        + "\n  - ".join(str(c) for c in candidates)
    )


def load_library(path: Path | str | None = None) -> Drawing:
    """E-Symbole.dxf einmal lesen, cachen. Thread-safe.

    `path` wird nur beim ERSTEN Laden berücksichtigt (danach Cache;
    für Tests `reset_cache()`)."""
    global _library_doc
    if _library_doc is not None:
        return _library_doc
    with _lock:
        if _library_doc is None:
            resolved = _resolve_library_path(path)
            log.info("Loading Schrack library: %s", resolved)
            _library_doc = ezdxf.readfile(str(resolved))
    return _library_doc


def load_mapping() -> dict[str, dict[str, Any]]:
    """Validiertes catalog_key → Block-Spec-Mapping, einmal geladen.

    Validiert jeden Eintrag:
      - alle Pflichtfelder vorhanden (block_name, label, category)
      - block_name referenziert einen real existierenden Library-Block

    Raises ValueError mit ALLEN Verstößen beim ersten Aufruf (fail-loud).
    """
    global _mapping
    if _mapping is not None:
        return _mapping
    with _lock:
        if _mapping is not None:
            return _mapping
        raw = load_symbol_mapping()
        lib = load_library()
        block_names = set(lib.blocks.block_names())
        errors: list[str] = []
        for key, entry in raw.items():
            if not isinstance(entry, dict):
                errors.append(f"{key!r}: entry is not a mapping")
                continue
            for field in _REQUIRED_FIELDS:
                if field not in entry:
                    errors.append(f"{key!r}: missing field {field!r}")
            block = entry.get("block_name")
            if block and block not in block_names:
                errors.append(f"{key!r}: block {block!r} not present in library")
        if errors:
            raise ValueError(
                "Schrack mapping validation failed:\n  - " + "\n  - ".join(errors)
            )
        _mapping = raw
    return _mapping


def sync_layers(output_doc: Drawing) -> int:
    """Schrack-Layer (mit Original-RGB) ins output_doc kopieren.

    Idempotent. Der physische Lib-Layer `E_Sicherheitsbeleuchtung` wird auf den
    DIN_SIBEL-Ausgabenamen (`din_SIBEL_10_emergency_lighting`) umbenannt und auf
    kräftiges Schrack-Grün (30, 180, 80) übersteuert, damit Notlicht-Symbole
    sichtbar rendern.

    Returns
    -------
    int
        Anzahl neu angelegter Layer.
    """
    lib = load_library()
    added = 0
    for layer in lib.layers:
        name = layer.dxf.name
        out_name = SAFETY_LAYER if name == _LIB_SAFETY_LAYER else name
        if out_name in output_doc.layers:
            continue
        new = output_doc.layers.add(out_name)
        try:
            new.dxf.color = layer.dxf.color
        except AttributeError:
            pass
        src_tc = getattr(layer.dxf, "true_color", None)
        if src_tc is not None:
            new.dxf.true_color = src_tc
        if out_name == SAFETY_LAYER:
            r, g, b = _SAFETY_GREEN_RGB
            new.dxf.true_color = (r << 16) | (g << 8) | b
        added += 1
    return added


def import_block(output_doc: Drawing, block_name: str) -> None:
    """Einen Block aus der Library ins output_doc importieren.

    Idempotent. Nutzt ezdxf.addons.Importer; finalize() nur bei echtem
    Import. Importierte Block-Definitionen werden einmal pro Output-Dokument
    re-origin'd, sodass das Glyph-Bbox-Zentrum am INSERT-Punkt sitzt.
    """
    if block_name not in output_doc.blocks:
        lib = load_library()
        if block_name not in lib.blocks:
            raise KeyError(f"Block {block_name!r} not in Schrack library")
        importer = Importer(lib, output_doc)
        importer.import_block(block_name)
        importer.finalize()
    _normalize_block_origin_recursive(output_doc, block_name, visiting=set())


def _normalized_blocks_for(output_doc: Drawing) -> set[str]:
    """Persistenter Normalisierungs-Status je Output-Dokument."""
    return _normalized_blocks_by_doc.setdefault(id(output_doc), set())


def _normalize_block_origin_recursive(
    output_doc: Drawing,
    block_name: str,
    *,
    visiting: set[str],
) -> None:
    """Block-Geometrie verschieben, sodass das Bbox-Zentrum auf (0, 0) liegt."""
    normalized = _normalized_blocks_for(output_doc)
    if block_name in normalized:
        return
    if block_name in visiting:
        log.warning("Skipping cyclic Schrack block reference at %s", block_name)
        return
    if block_name not in output_doc.blocks:
        return

    visiting.add(block_name)
    block = output_doc.blocks[block_name]

    # Abhängigkeiten zuerst: Parents mit verschachtelten INSERTs werden erst
    # zentriert, wenn ihre Kinder stabil sind (deterministisch).
    for entity in list(block):
        if entity.dxftype() != "INSERT":
            continue
        _normalize_block_origin_recursive(
            output_doc,
            entity.dxf.name,
            visiting=visiting,
        )

    extents = ezbbox.extents(block, fast=True)
    if extents.has_data:
        center = extents.center
        if center.x or center.y or center.z:
            matrix = Matrix44.translate(-center.x, -center.y, -center.z)
            for entity in list(block):
                entity.transform(matrix)

    # Blaue Hardcode-Farben → BYLAYER (läuft wie die Zentrierung genau einmal
    # je Block/Output-Dokument, daher hier statt in import_block).
    for entity in list(block):
        if getattr(entity.dxf, "color", None) in _BLAUE_ACI:
            entity.dxf.color = _BYLAYER
            entity.dxf.discard("true_color")

    visiting.remove(block_name)
    normalized.add(block_name)


def reset_cache() -> None:
    """Cache (Library + Mapping + Normalisierungs-Status) leeren. Test-only."""
    global _library_doc, _mapping, _normalized_blocks_by_doc
    with _lock:
        _library_doc = None
        _mapping = None
        _normalized_blocks_by_doc = {}
