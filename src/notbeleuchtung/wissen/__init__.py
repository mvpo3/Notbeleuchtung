"""wissen — projektübergreifendes Materialwörterbuch (Legenden-Signaturen).

Prinzip: das Erscheinungsbild ist die Wahrheit. Ein Material trägt seine
verifizierten Signaturen (Hatch-Muster, Füllfarbe, Linien-/Symbol-Marker) plus
Aliasnamen (Glob erlaubt) aus allen bekannten Projekten. Musternamen allein
sind NIE die Zuordnung — FP_822 trägt drei Materialien.

Grenze: der Loader liest nur ``materialien.yaml``; Matching macht
``raumerkennung.material_matching``, Pflege ``raumerkennung.legende_import``.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import yaml

log = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent

BAUTEILARTEN = (
    "WAND_TRAGEND", "WAND_LEICHT", "DAEMMUNG", "GLAS", "SCHACHT", "MARKIERUNG",
    "UNBEKANNT",  # Legendenimport ohne zuordenbares Wörterbuch-Material
)


@dataclass(frozen=True)
class Material:
    """Ein Wörterbuch-Material: Bezeichnung + Bauteilart + Signaturen + Aliasnamen."""

    bezeichnung: str
    bauteilart: str
    brandschutz: str | None = None       # EI0 | EI30 | EI90 | None
    semantik: str | None = None          # z.B. BRANDABSCHNITT / FLUCHTWEG
    aliasnamen: tuple[str, ...] = ()
    signaturen: tuple[dict, ...] = ()
    quellen: tuple[str, ...] = ()


def lade_materialien(data_dir: Path | None = None) -> list[Material]:
    """materialien.yaml → typisierte Materialien. ``data_dir`` nur für Tests."""
    pfad = (data_dir or DATA_DIR) / "materialien.yaml"
    with open(pfad, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh) or {}
    out: list[Material] = []
    for m in doc.get("materialien", []):
        if m["bezeichnung"].upper() == "BETON":
            # BETON ist KEIN eigenes Material — Signatur identisch zu STAHLBETON.
            log.warning(
                "materialien.yaml führt BETON als eigenes Material — "
                "gehört als Alias zu STAHLBETON"
            )
        out.append(Material(
            bezeichnung=m["bezeichnung"],
            bauteilart=m["bauteilart"],
            brandschutz=m.get("brandschutz"),
            semantik=m.get("semantik"),
            aliasnamen=tuple(m.get("aliasnamen", ())),
            signaturen=tuple(m.get("signaturen", ())),
            quellen=tuple(m.get("quellen", ())),
        ))
    return out
