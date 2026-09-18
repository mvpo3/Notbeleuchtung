"""Versionierte Architekturpläne der Prüf-Familien — eine Quelle der Wahrheit.

Die Familien-Soll-Tests lasen früher ``Projekte/_eingang/<Kurzname>.dxf``. Der
Ordner ist untracked, also fehlte er in jedem frischen Checkout und die Tests
skippten still — die Zusicherungen liefen faktisch nie. Hier stehen stattdessen
die per git GETRACKTEN Original-Pläne unter ``Projekte/``: byteidentisch mit den
bisherigen Eingangs-Kopien (Ausnahme ``RENNWEG_OG3``: dort weichen nur die
Header ``$TDUPDATE``/``$TDUUPDATE`` ab, die Geometrie ist gleich).

Weil die Dateien zum Repo gehören, ist ein fehlender Plan ein Fehler und kein
Grund zum Überspringen — ``plan()`` lässt den Test darum ``fail``en.

``Projekte/_eingang`` bleibt unangetastet (Ad-hoc-Läufe).
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

BARAWITZKA_EG = REPO / "Projekte/Barawitzkagasse/415_260415_PP_VA_1_3 0 EG.dxf"
MOLLGASSE_EG = REPO / "Projekte/Mollgasse/Erdgeschoß.dxf"
MUTHGASSE_E2 = (REPO / "Projekte/Pläne 19., Muthgasse 109B - 2026-05-07_13-12"
                / "Architekt" / "Ausführungsplan"
                / "M109B_-Plan - AR-AF-A-GR-E2 100 - GRUNDRISS E2.dxf")
RENNWEG_EG = REPO / "Projekte/Rennweg/EG - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf"
RENNWEG_OG3 = REPO / "Projekte/Rennweg/OG3 - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf"


def plan(pfad: Path) -> Path:
    """Den Plan-Pfad durchreichen — fehlt die Datei, schlägt der Test fehl."""
    if not pfad.is_file():
        pytest.fail(f"Versionierter Plan fehlt: {pfad} — Repo unvollständig ausgecheckt?")
    return pfad
