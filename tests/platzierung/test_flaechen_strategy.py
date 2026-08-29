"""flaechen_strategy — raum-bezogene Sicherheitsleuchten + Antipanik.

Norm-getrieben: die Klassifikation kommt aus FakeNorm (STIEGENHAUS→sicherheitsleuchte,
SAAL→antipanik). Getestet gegen das 4OG-RaumModell, um einen SAAL erweitert, damit
BEIDE Arten in einem Lauf entstehen.
"""
import json
from pathlib import Path

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import RaumModell
from notbeleuchtung.platzierung.flaechen_strategy import (
    plan_antipanik,
    plan_sicherheitsleuchten,
)

FIXTURES = Path(__file__).parents[1] / "fixtures"


def _raum_mit_saal() -> RaumModell:
    data = json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    data["raeume"].append(
        {
            "id": "saal_1",
            "raum_typ": "SAAL",
            "polygon_mm": [[0.0, 0.0], [10000.0, 0.0], [10000.0, 8000.0], [0.0, 8000.0]],
            "flaeche_m2": 80.0,
            "ist_fluchtweg": False,
            "ist_communal": True,
        }
    )
    return RaumModell.model_validate(data)


def test_sicherheitsleuchten_je_stiegenhaus():
    out = plan_sicherheitsleuchten(_raum_mit_saal(), FakeNormProvider())
    assert len(out) == 2  # 2 STIEGENHÄUSER, SAAL ist antipanik → nicht hier
    for p in out:
        assert p.kind == "sicherheitsleuchte"
        assert p.catalog_key == "sicherheitsleuchte_aufheller"
        assert p.covers_segment == []
        assert p.circuit_hint.endswith("-F13")


def test_antipanik_im_saal_am_zentrum():
    out = plan_antipanik(_raum_mit_saal(), FakeNormProvider())
    assert len(out) == 1
    p = out[0]
    assert p.kind == "antipanik"
    assert p.catalog_key == "antipanik_leuchte"
    assert p.xy_mm == (5000.0, 4000.0)  # Rechteck-Zentrum des SAAL
    assert p.covers_segment == []
    assert p.norm_quelle == "ÖNORM EN 1838:2013 §4.3.1"


def test_keine_antipanik_ohne_qualifizierten_raum():
    # Reines 4OG (nur STIEGENHÄUSER) → keine Antipanik-Fläche.
    data = json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    out = plan_antipanik(RaumModell.model_validate(data), FakeNormProvider())
    assert out == []
