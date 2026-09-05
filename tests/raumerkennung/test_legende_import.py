"""legende_import — Baulegende.dxf → Materialwörterbuch (additiv, idempotent)."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

from notbeleuchtung.raumerkennung.legende_import import importiere_legende, norm_label
from notbeleuchtung.wissen import DATA_DIR, lade_materialien

REPO_ROOT = Path(__file__).resolve().parents[2]
BAULEGENDE = REPO_ROOT / "Projekte" / "Rennweg" / "Legende" / "Baulegende.dxf"

ERWARTETE_MATERIALIEN = {
    "ALU_GLAS", "BRANDABSCHNITT", "FLUCHTWEGLAENGE",
    "GIPSKARTON_EI0", "GIPSKARTON_EI30", "GIPSKARTON_EI90",
    "SCHACHT", "STAHLBETON", "TROCKENSTEIGLEITUNG",
    "WAERMEDAEMMUNG", "YTONG", "ZIEGELMAUERWERK",
}


@pytest.fixture
def baulegende() -> Path:
    if not BAULEGENDE.exists():
        pytest.skip(f"Baulegende fehlt: {BAULEGENDE}")
    return BAULEGENDE


@pytest.fixture
def yaml_kopie(tmp_path) -> Path:
    ziel = tmp_path / "materialien.yaml"
    shutil.copy(DATA_DIR / "materialien.yaml", ziel)
    return ziel


def test_startbestand_laedt_12_materialien():
    mats = lade_materialien()
    assert {m.bezeichnung for m in mats} == ERWARTETE_MATERIALIEN
    stb = next(m for m in mats if m.bezeichnung == "STAHLBETON")
    assert "BETON" in stb.aliasnamen  # BETON ist Alias, kein eigenes Material
    assert stb.bauteilart == "WAND_TRAGEND"
    assert next(m for m in mats if m.bezeichnung == "GIPSKARTON_EI30").brandschutz == "EI30"
    assert next(m for m in mats if m.bezeichnung == "ALU_GLAS").bauteilart == "GLAS"
    assert next(m for m in mats if m.bezeichnung == "BRANDABSCHNITT").semantik == "BRANDABSCHNITT"


def test_import_reproduziert_13_eintraege(baulegende, yaml_kopie):
    erg = importiere_legende(baulegende, "Rennweg", yaml_kopie)
    # 13 Muster-Einträge + Zusatzzeile 'LÄNGE TSL' — alle auf die 12 Materialien.
    assert erg.eintraege == {
        "ALU GLASKONSTRUKTIONEN": "ALU_GLAS",
        "BETON": "STAHLBETON",
        "BRANDABSCHNITT": "BRANDABSCHNITT",
        "FLUCHTWEGSLAENGE": "FLUCHTWEGLAENGE",
        "GIPSKARTONSTAENDERWAND EI0": "GIPSKARTON_EI0",
        "GIPSKARTONSTAENDERWAND EI30": "GIPSKARTON_EI30",
        "GIPSKARTONSTAENDERWAND EI90": "GIPSKARTON_EI90",
        "LAENGE TSL": "TROCKENSTEIGLEITUNG",
        "SCHAECHTE ELEKTRO HKLS DD BD": "SCHACHT",
        "STAHLBETON": "STAHLBETON",
        "TROCKENSTEIGLEITUNG": "TROCKENSTEIGLEITUNG",
        "WAERMEDAEMMUNG": "WAERMEDAEMMUNG",
        "YTONG": "YTONG",
        "ZIEGELMAUERWERK": "ZIEGELMAUERWERK",
    }
    assert erg.neue_materialien == 0  # Startbestand deckt die ganze Legende


def test_import_beton_warnung(baulegende, yaml_kopie):
    erg = importiere_legende(baulegende, "Rennweg", yaml_kopie)
    assert any("BETON" in w and "STAHLBETON" in w for w in erg.warnungen)


def test_fp822_dreifachbelegung_getrennt(baulegende, yaml_kopie):
    """FP_822 trägt drei Materialien — nur bgcolor unterscheidet sie."""
    importiere_legende(baulegende, "Rennweg", yaml_kopie)
    doc = yaml.safe_load(yaml_kopie.read_text(encoding="utf-8"))
    bg = {}
    for m in doc["materialien"]:
        for s in m["signaturen"]:
            if s.get("pattern_name") == "FP_822":
                bg[m["bezeichnung"]] = tuple(s["bgcolor"])
    assert bg == {
        "ZIEGELMAUERWERK": (255, 83, 83),
        "GIPSKARTON_EI0": (255, 213, 170),
        "GIPSKARTON_EI30": (255, 170, 240),
    }


def test_import_idempotent(baulegende, yaml_kopie):
    erg1 = importiere_legende(baulegende, "Rennweg", yaml_kopie)
    stand = yaml_kopie.read_text(encoding="utf-8")
    erg2 = importiere_legende(baulegende, "Rennweg", yaml_kopie)
    assert erg2.geaendert is False
    assert erg2.neue_signaturen == erg2.neue_aliasnamen == erg2.neue_materialien == 0
    assert yaml_kopie.read_text(encoding="utf-8") == stand
    assert erg1.eintraege == erg2.eintraege


def test_import_fuellt_geleerten_bestand(baulegende, yaml_kopie):
    """Signaturen aus dem Bestand löschen → Import stellt sie aus der Legende her."""
    doc = yaml.safe_load(yaml_kopie.read_text(encoding="utf-8"))
    for m in doc["materialien"]:
        m["signaturen"] = []
    yaml_kopie.write_text(
        yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    erg = importiere_legende(baulegende, "Rennweg", yaml_kopie)
    assert erg.geaendert is True and erg.neue_signaturen >= 13
    neu = yaml_kopie.read_text(encoding="utf-8")
    referenz = (DATA_DIR / "materialien.yaml").read_text(encoding="utf-8")
    assert neu == referenz  # exakt der ausgelieferte Startbestand


def test_norm_label():
    assert norm_label("GIPSKARTONSTÄNDERWAND EI90") == "GIPSKARTONSTAENDERWAND EI90"
    assert norm_label("FSTZ. ") == "FSTZ"
    assert norm_label("Schächte(Elektro,HKLS,DD,BD)") == "SCHAECHTE ELEKTRO HKLS DD BD"
