"""sonderstellen_strategy — Pflicht-Leuchten an §4.1.2-Stellen + Flag-Räume.

Getestet gegen das 4OG-RaumModell + synthetische Sonderstellen/Flags. Ohne
Sonderstellen und Flags ist die Strategie ein No-op (bit-identische Pläne).
"""
import json
from pathlib import Path

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import RaumModell
from notbeleuchtung.platzierung.sonderstellen_strategy import (
    plan_flag_raeume,
    plan_sonderstellen,
)

FIXTURES = Path(__file__).parents[1] / "fixtures"


def _raum(sonderstellen=(), extra_raeume=()) -> RaumModell:
    data = json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    data["sonderstellen"] = list(sonderstellen)
    data["raeume"].extend(extra_raeume)
    return RaumModell.model_validate(data)


def _stelle(typ: str, xy=(1000.0, 2000.0), sid="s1") -> dict:
    return {"id": sid, "typ": typ, "xy_mm": list(xy), "quelle": "manuell (Test)"}


def test_ohne_sonderstellen_noop():
    assert plan_sonderstellen(_raum(), FakeNormProvider()) == []
    assert plan_flag_raeume(_raum(), FakeNormProvider()) == []


def test_feuerloescher_bekommt_sicherheitsleuchte_an_der_stelle():
    out = plan_sonderstellen(
        _raum(sonderstellen=[_stelle("feuerloescher", (1234.0, 5678.0))]),
        FakeNormProvider(),
    )
    assert len(out) == 1
    p = out[0]
    assert p.kind == "sicherheitsleuchte"
    assert p.xy_mm == (1234.0, 5678.0)      # Leuchte AN der Stelle → „nahe" (≤ 2 m) erfüllt
    assert p.covers_segment == []
    quellen = set(FakeNormProvider().regelwerk_snapshot().quellen)
    assert p.norm_quelle in quellen          # Naht-Invariante


def test_jeder_punkt_typ_bekommt_eine_leuchte():
    stellen = [
        _stelle(t, (float(i * 1000), 0.0), sid=f"s{i}")
        for i, t in enumerate(["feuerloescher", "hydrant", "erste_hilfe", "brandmelder"])
    ]
    out = plan_sonderstellen(_raum(sonderstellen=stellen), FakeNormProvider())
    assert len(out) == 4
    assert all(p.kind == "sicherheitsleuchte" for p in out)
    assert len({p.xy_mm for p in out}) == 4


def test_niveauaenderung_loest_sl_und_rz_aus():
    out = plan_sonderstellen(
        _raum(sonderstellen=[_stelle("niveauaenderung", (500.0, 500.0))]),
        FakeNormProvider(),
    )
    kinds = sorted(p.kind for p in out)
    assert kinds == ["rz", "sicherheitsleuchte"]     # RZ-06 + SL-04, dieselbe Stelle
    assert {p.xy_mm for p in out} == {(500.0, 500.0)}
    rz = next(p for p in out if p.kind == "rz")
    assert rz.richtung == "gerade"                    # beidseitig — Richtung unbestimmt


def test_barrierefreies_wc_bekommt_antipanik():
    wc = {
        "id": "wc_bf", "raum_typ": "WC", "flaeche_m2": 6.0,
        "polygon_mm": [[0.0, 0.0], [3000.0, 0.0], [3000.0, 2000.0], [0.0, 2000.0]],
        "ist_fluchtweg": False, "ist_communal": True, "ist_barrierefrei": True,
    }
    out = plan_flag_raeume(_raum(extra_raeume=[wc]), FakeNormProvider())
    assert len(out) == 1
    p = out[0]
    assert p.kind == "antipanik"
    assert 0.0 <= p.xy_mm[0] <= 3000.0 and 0.0 <= p.xy_mm[1] <= 2000.0


def test_barrierefrei_ohne_flag_keine_leuchte():
    wc = {
        "id": "wc_normal", "raum_typ": "WC", "flaeche_m2": 6.0,
        "polygon_mm": [[0.0, 0.0], [3000.0, 0.0], [3000.0, 2000.0], [0.0, 2000.0]],
        "ist_fluchtweg": False, "ist_communal": True,
    }
    assert plan_flag_raeume(_raum(extra_raeume=[wc]), FakeNormProvider()) == []


def test_barrierefrei_bereits_antipanik_klassifiziert_keine_doppelung():
    # SAAL ist im FakeNorm antipanik-klassifiziert → flaechen_strategy platziert;
    # das Flag darf nicht zusätzlich setzen.
    saal = {
        "id": "saal_bf", "raum_typ": "SAAL", "flaeche_m2": 80.0,
        "polygon_mm": [[0.0, 0.0], [10000.0, 0.0], [10000.0, 8000.0], [0.0, 8000.0]],
        "ist_fluchtweg": False, "ist_communal": True, "ist_barrierefrei": True,
    }
    assert plan_flag_raeume(_raum(extra_raeume=[saal]), FakeNormProvider()) == []


def test_besondere_gefaehrdung_bekommt_sicherheitsleuchte():
    zimmer = {
        "id": "werkstatt", "raum_typ": "ZIMMER", "flaeche_m2": 20.0,
        "polygon_mm": [[0.0, 0.0], [5000.0, 0.0], [5000.0, 4000.0], [0.0, 4000.0]],
        "ist_fluchtweg": False, "ist_communal": False, "besondere_gefaehrdung": True,
    }
    out = plan_flag_raeume(_raum(extra_raeume=[zimmer]), FakeNormProvider())
    assert len(out) == 1
    assert out[0].kind == "sicherheitsleuchte"


def test_besondere_gefaehrdung_bereits_sl_klassifiziert_keine_doppelung():
    # STIEGENHAUS ist sicherheitsleuchten-klassifiziert → flaechen_strategy setzt schon.
    stg = {
        "id": "stg_gef", "raum_typ": "STIEGENHAUS", "flaeche_m2": 15.0,
        "polygon_mm": [[0.0, 0.0], [4000.0, 0.0], [4000.0, 4000.0], [0.0, 4000.0]],
        "ist_fluchtweg": True, "ist_communal": True, "besondere_gefaehrdung": True,
    }
    assert plan_flag_raeume(_raum(extra_raeume=[stg]), FakeNormProvider()) == []


def test_place_integriert_sonderstellen():
    # Ende-zu-Ende durch den echten Platzierer: die Sonderstellen-Leuchte übersteht
    # lb_override/abstand_nachpass/deckungs_zuordnung/circuit_zuordnung.
    from notbeleuchtung.platzierung import NotlichtPlatzierer

    raum = _raum(sonderstellen=[_stelle("feuerloescher", (99999.0, 99999.0))])
    ohne = NotlichtPlatzierer().place(_raum(), FakeNormProvider())
    mit = NotlichtPlatzierer().place(raum, FakeNormProvider())
    assert len(mit.platzierungen) == len(ohne.platzierungen) + 1
    neu = [p for p in mit.platzierungen if p.xy_mm == (99999.0, 99999.0)]
    assert len(neu) == 1 and neu[0].kind == "sicherheitsleuchte"
