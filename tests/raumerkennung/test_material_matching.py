"""material_matching — Signatur + Kontext → Material (Erscheinungsbild ist Wahrheit)."""
from __future__ import annotations

from pathlib import Path

import pytest

from notbeleuchtung.raumerkennung.material_matching import (
    SCHWELLE,
    HatchSignatur,
    MatchSammlung,
    MusterLinie,
    bestimme_material,
    signatur_aus_hatch,
    struktur_klasse,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
RENNWEG_DXF = REPO_ROOT / "Projekte" / "_eingang" / "Rennweg_OG3.dxf"

FP_825 = HatchSignatur(
    "FP_825", (134, 206, 152), 256, None,
    (MusterLinie(45.0, 0.254), MusterLinie(45.0, 0.254, (0.127, -0.127))),
)
# Rennweg-Wandmuster: gleiche Struktur wie FP_825 (45°-solid/dashed-Paar), aber
# Skala mm statt Legendeneinheit und KEIN bgcolor — Abstände zählen nur relativ.
BETON_BEWEHRT = HatchSignatur(
    "BETON_BEWEHRT_SN46", None, 18, (0, 0, 0),
    (MusterLinie(45.0, 100.0, (30.0, -20.0)), MusterLinie(45.0, 100.0, (100.0, 0.0))),
)
INSULATION = HatchSignatur(
    "INSULATION", None, 18, (0, 0, 0),
    (MusterLinie(45.0, 75.0), MusterLinie(45.0, 75.0)),
)
EPS = HatchSignatur(
    "DÄMMSTOFF__POLYSTYROL_EPS", None, 18, (0, 0, 0),
    tuple(
        MusterLinie(w, 51.961, (30.0, -60.0))
        for w in (66.636, 66.636, 126.636, 126.636, 186.636, 186.636)
    ),
)


@pytest.mark.parametrize(
    "sig, layer, erwartet",
    [
        (FP_825, "", "STAHLBETON"),
        # Rennweg: Alias + strukturgleiches 45°-solid/dashed-Paar → STAHLBETON.
        (BETON_BEWEHRT, "New_015 Innenwände", "STAHLBETON"),
        # Alias schlägt Geometrie-Abweichung (INSULATION ist solid, keine Welle).
        (INSULATION, "New_015 Innenwände", "WAERMEDAEMMUNG"),
        (EPS, "New_015 Innenwände", "WAERMEDAEMMUNG"),
    ],
)
def test_rennweg_signaturen(sig, layer, erwartet):
    t = bestimme_material(sig, layer=layer)
    assert t.material == erwartet, t.begruendung
    assert t.score >= SCHWELLE


@pytest.mark.parametrize(
    "bgcolor, erwartet",
    [
        ((255, 83, 83), "ZIEGELMAUERWERK"),
        ((255, 213, 170), "GIPSKARTON_EI0"),
        ((255, 170, 240), "GIPSKARTON_EI30"),
    ],
)
def test_fp822_dreifachbelegung_nur_bgcolor_trennt(bgcolor, erwartet):
    sig = HatchSignatur("FP_822", bgcolor, 256, None, (MusterLinie(45.0, 0.15),))
    t = bestimme_material(sig)
    assert t.material == erwartet, t.begruendung


def test_mollgasse_ansi33_mit_stb_layer():
    sig = HatchSignatur("ANSI33", None, 256, None, (MusterLinie(45.0, 0.05, (0.02, -0.02)),))
    t = bestimme_material(sig, layer="02-FIL-G00-Leg-STB")
    assert t.material == "STAHLBETON", t.begruendung


def test_mollgasse_square_mit_gk_layer():
    sig = HatchSignatur("SQUARE", None, 256, None, (MusterLinie(0.0, 0.03), MusterLinie(90.0, 0.03)))
    t = bestimme_material(sig, layer="02-GK-ORANGE")
    assert t.material.startswith("GIPSKARTON"), t.begruendung


def test_fantasie_signatur_bleibt_unbekannt():
    sig = HatchSignatur(
        "XYZZY_77", None, 7, None,
        (MusterLinie(13.7, 0.4), MusterLinie(51.2, 1.9, (0.1, -0.9, 0.1, -0.3))),
    )
    t = bestimme_material(sig, layer="Layer0")
    assert t.material == "UNBEKANNT"
    assert t.signatur.pattern_name == "XYZZY_77"  # Signatur bleibt am Treffer (Kachel-Export)


def test_solid_farbe_entscheidet():
    # Möbel-/Treppen-SOLID (color 255) darf NICHT als ALU_GLAS durchgehen …
    moebel = bestimme_material(HatchSignatur("SOLID", None, 255, None, ()))
    assert moebel.material == "UNBEKANNT"
    # … das türkise Legenden-SOLID schon.
    glas = bestimme_material(HatchSignatur("SOLID", None, 4, (0, 232, 232), ()))
    assert glas.material == "ALU_GLAS"


def test_struktur_klassen():
    assert struktur_klasse(FP_825) == "paar_sd"
    assert struktur_klasse(BETON_BEWEHRT) == "paar_sd"  # [100, 0] ist faktisch solid
    assert struktur_klasse(INSULATION) == "einfach"
    assert struktur_klasse(EPS) == "welle"
    assert struktur_klasse(HatchSignatur("SOLID", None, 4, None, ())) == "solid"
    assert struktur_klasse(
        HatchSignatur("FP_826", None, 256, None, (MusterLinie(45.0, 0.3), MusterLinie(135.0, 0.3)))
    ) == "kreuz"


def test_matchsammlung_sammelt_unbekannte():
    s = MatchSammlung()
    s.bestimme(FP_825)
    s.bestimme(HatchSignatur("SOLID", None, 255, None, ()), layer="Moebel")
    assert len(s.treffer) == 2
    unbekannt = s.unbekannte()
    assert len(unbekannt) == 1 and unbekannt[0].layer == "Moebel"


def test_rennweg_wall_bloecke_echt():
    """Echte Rennweg-Block-Hatches: die drei Wandmuster landen richtig."""
    if not RENNWEG_DXF.exists():
        pytest.skip(f"Rennweg-DXF fehlt: {RENNWEG_DXF}")
    import ezdxf

    doc = ezdxf.readfile(str(RENNWEG_DXF))
    erwartet = {
        "BETON_BEWEHRT_SN46": "STAHLBETON",
        "INSULATION": "WAERMEDAEMMUNG",
        "DÄMMSTOFF__POLYSTYROL_EPS": "WAERMEDAEMMUNG",
        "FEUERFESTER_STEIN": "SCHACHT",
    }
    gefunden: dict[str, str] = {}
    for blk in doc.blocks:
        if not blk.name.startswith("Wall_"):
            continue
        for h in blk.query("HATCH"):
            name = h.dxf.pattern_name
            if name in erwartet and name not in gefunden:
                gefunden[name] = bestimme_material(
                    signatur_aus_hatch(h), layer=h.dxf.layer
                ).material
    assert gefunden == {k: v for k, v in erwartet.items() if k in gefunden}
    assert set(gefunden) >= {"BETON_BEWEHRT_SN46", "INSULATION"}
