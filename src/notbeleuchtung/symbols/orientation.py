"""orientation.py — DER Rotationsrahmen für Richtungs-Symbole (Slice 3.1).

Single Source of Truth für die Frage „wie rotiere ich einen Pfeil-Block, damit
er in eine Ziel-Richtung zeigt". Vorher lebten zwei inkonsistente Rahmen im
Code: `bausteine.richtung_und_rotation` (Achsen-Frame, implizite rechts-Basis)
und der Pfeil-zur-Tür-Pfad (#111, unten-Basis, `+90°`-Formel) — Folge: die
Fallback-Rotation drehte den „nach unten"-Block ins Leere („oben" renderte als
„rechts", Befund 3 des MEGA-Prompts 2026-09-07).

Basisorientierungen GEMESSEN am 2026-09-07 (Raster der Library-Blöcke,
reports/blocks/*.png, Inventar D): der „nach rechts"-Block ist ein echter
X-Spiegel (Basis 0°) — der PORT_LOG-Eintrag stimmt, der mirror_x-Hack ist
Geschichte.
"""
from __future__ import annotations

from notbeleuchtung.symbols import load_symbol_mapping

# Ziel-Richtung → Winkel im Weltkoordinatensystem (rechts = +x = 0°, CCW).
ZIEL_DEG: dict[str, float] = {"rechts": 0.0, "oben": 90.0, "links": 180.0, "unten": 270.0}

# Basisorientierung je Library-Block bei rotation=0 (normalisierte, lowercase
# Blocknamen — `block_names()` der Library normalisiert ebenso). Gemessen, nicht
# geraten: reports/blocks/ (2026-09-07).
_BLOCK_BASE_DEG: dict[str, float] = {
    "notbeleuchtung- richtungspfeil nach unten": 270.0,
    "notbeleuchtung-richtungspfeil nach links": 180.0,
    "notbeleuchtung-richtungspfeil nach rechts": 0.0,
}


def basis_deg(block_name: str) -> float | None:
    """Basisorientierung des Blocks bei rotation=0 — None für richtungslose Blöcke."""
    return _BLOCK_BASE_DEG.get(block_name.strip().lower())


def transformation(catalog_key: str, richtung: str) -> tuple[float, bool]:
    """(rotation_deg, mirror_x), damit der Block des Keys in `richtung` zeigt.

    Kennt der Key keinen Richtungs-Block (Kreis-Symbole, `gerade`/unbekannte
    Richtung), kommt (0, False) — das Symbol ist rotationsneutral bzw. der
    Doppelpfeil-Pfad des Inserters übernimmt. Spiegelung ist nie nötig: die
    Library führt alle drei Basen (links/rechts/unten) als eigene Blöcke.
    """
    ziel = ZIEL_DEG.get(richtung)
    if ziel is None:
        return 0.0, False
    entry = load_symbol_mapping().get(catalog_key) or {}
    basis = basis_deg(str(entry.get("block_name", "")))
    if basis is None:
        return 0.0, False
    return (ziel - basis) % 360.0, False
