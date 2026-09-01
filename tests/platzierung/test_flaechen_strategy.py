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


def test_antipanik_raster_im_saal():
    # SAAL mindest_anzahl=4 → 2×2-Raster über die Fläche (nicht 1 Zentroid).
    out = plan_antipanik(_raum_mit_saal(), FakeNormProvider())
    assert len(out) == 4
    for p in out:
        assert p.kind == "antipanik"
        assert p.catalog_key == "antipanik_leuchte"
        assert p.covers_segment == []
        assert p.norm_quelle == "ÖNORM EN 1838:2013 §4.3.1"
        # innerhalb des SAAL-Rechtecks (0..10000 × 0..8000)
        assert 0.0 <= p.xy_mm[0] <= 10000.0 and 0.0 <= p.xy_mm[1] <= 8000.0
    assert len({p.xy_mm for p in out}) == 4  # 4 verschiedene Positionen


def test_keine_antipanik_ohne_qualifizierten_raum():
    # Reines 4OG (nur STIEGENHÄUSER) → keine Antipanik-Fläche.
    data = json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    out = plan_antipanik(RaumModell.model_validate(data), FakeNormProvider())
    assert out == []


def _fake_mit_schwelle(*, antipanik_min_m2=None, wc_min_m2=None) -> FakeNormProvider:
    """FakeNorm, dessen flaechen_schwellen belegt sind (simuliert Enis' spätere Werte)."""
    fake = FakeNormProvider()
    fake._snapshot.flaechen_schwellen.antipanik_min_m2 = antipanik_min_m2
    fake._snapshot.flaechen_schwellen.wc_sanitaer_min_m2 = wc_min_m2
    return fake


def _raum_mit_zusatzraum(raum_typ: str, flaeche_m2: float, poly: list) -> RaumModell:
    data = json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    data["raeume"].append(
        {
            "id": "zusatz_1", "raum_typ": raum_typ, "polygon_mm": poly,
            "flaeche_m2": flaeche_m2, "ist_fluchtweg": False, "ist_communal": True,
        }
    )
    return RaumModell.model_validate(data)


def test_flaechen_trigger_antipanik_ueber_schwelle():
    # LAGER ist NICHT antipanik-typisiert → ohne Schwelle keine Antipanik (Trigger inert).
    poly = [[0.0, 0.0], [12000.0, 0.0], [12000.0, 10000.0], [0.0, 10000.0]]  # 120 m²
    raum = _raum_mit_zusatzraum("LAGER", 120.0, poly)
    assert plan_antipanik(raum, FakeNormProvider()) == []       # flaechen_schwellen=None

    mit = plan_antipanik(raum, _fake_mit_schwelle(antipanik_min_m2=60.0))
    assert mit                                                  # 120 m² ≥ 60 → getriggert
    for p in mit:
        assert p.kind == "antipanik"
        assert p.catalog_key == "antipanik_leuchte"             # aus der Norm-Antipanik-Regel
        assert p.norm_quelle == "ÖNORM EN 1838:2013 §4.3.1"


def test_flaechen_trigger_wc_ueber_schwelle():
    poly = [[0.0, 0.0], [4000.0, 0.0], [4000.0, 3000.0], [0.0, 3000.0]]  # 12 m²
    raum = _raum_mit_zusatzraum("WC", 12.0, poly)
    # Nur Antipanik-Schwelle (60 m²): das 12-m²-WC reißt sie NICHT → kein Trigger.
    assert plan_antipanik(raum, _fake_mit_schwelle(antipanik_min_m2=60.0)) == []
    # WC-Schwelle 8 m²: 12 m² ≥ 8 → antipanik-relevant.
    assert plan_antipanik(raum, _fake_mit_schwelle(wc_min_m2=8.0))


def test_antipanik_verdichtet_grosse_halle_bis_lux():
    # 40×40-m-Halle: das Norm-Grundraster (mindest_anzahl) erreicht 0,5 lx NICHT →
    # der EN-1838-Lux-Nachweis verdichtet über das Grundraster hinaus (A2).
    data = json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    poly = [[0.0, 0.0], [40000.0, 0.0], [40000.0, 40000.0], [0.0, 40000.0]]
    data["raeume"].append(
        {
            "id": "halle_1",
            "raum_typ": "SAAL",
            "polygon_mm": poly,
            "flaeche_m2": 1600.0,
            "ist_fluchtweg": False,
            "ist_communal": True,
        }
    )
    out = plan_antipanik(RaumModell.model_validate(data), FakeNormProvider())
    assert len(out) > 4  # über das mindest_anzahl-Raster hinaus verdichtet

    # Der 0,5-lx-Nachweis hält mit den verdichteten Positionen (mit der Norm-Montagehöhe).
    from notbeleuchtung.platzierung.geometry import _bbox
    from notbeleuchtung.platzierung.lux import lux_raster

    anf = FakeNormProvider().fuer_raum("SAAL", False)
    res = lux_raster(
        [p.xy_mm for p in out], _bbox(poly),
        montagehoehe_m=anf.montagehoehe_mm / 1000.0, ziel_lux=anf.min_lux,
    )
    assert res.erfuellt_min
