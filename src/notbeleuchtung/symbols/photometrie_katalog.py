"""photometrie_katalog — catalog_key → Hersteller-LDT (Schrack-Notbetriebs-Photometrie).

Auflösung des Mappings `photometrie_mapping.yaml` auf echte Dateipfade unter
`CAD_Symbole/photometrie/` (Aufwärts-Suche wie bei der Symbol-Library, damit es
im Repo, im entpackten ZIP und im installierten Paketbaum funktioniert).

Konsument ist die Registry (`hauptengine/registry.py`): sie baut daraus das
`i_cd_fn`-Callable für den Lux-Nachweis. Fehlt der Katalog (z.B. schlankes
Deployment ohne CAD_Symbole), liefern die Funktionen `None` — die Engine fällt
dann auf die bisherige isotrope Annahme zurück, nichts bricht.
"""
from __future__ import annotations

from pathlib import Path

import yaml

_MAPPING_DATEI = Path(__file__).parent / "photometrie_mapping.yaml"
_KATALOG_RELPATH = Path("CAD_Symbole") / "photometrie"


def _katalog_dir() -> Path | None:
    """Erster existierender `CAD_Symbole/photometrie`-Ordner (Aufwärts-Suche)."""
    for parent in Path(__file__).resolve().parents:
        kandidat = parent / _KATALOG_RELPATH
        if kandidat.is_dir():
            return kandidat
    return None


def _mapping() -> dict:
    with open(_MAPPING_DATEI, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def ldt_pfad_fuer(catalog_key: str) -> Path | None:
    """LDT-Pfad für einen Symbol-Katalog-Key — None wenn unbekannt/Katalog fehlt."""
    datei = _mapping().get("keys", {}).get(catalog_key)
    kat = _katalog_dir()
    if datei is None or kat is None:
        return None
    pfad = kat / datei
    return pfad if pfad.is_file() else None


def fluchtweg_default_ldt() -> Path | None:
    """LDT der Fluchtweg-Deckungs-Leuchte (Corridor-Optik) — None wenn Katalog fehlt."""
    datei = _mapping().get("fluchtweg_default")
    kat = _katalog_dir()
    if datei is None or kat is None:
        return None
    pfad = kat / datei
    return pfad if pfad.is_file() else None
