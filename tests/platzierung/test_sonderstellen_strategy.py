"""sonderstellen_strategy — Pflicht-Leuchten an §4.1.2-Stellen + Flag-Räume.

Getestet gegen das 4OG-RaumModell + synthetische Sonderstellen/Flags. Ohne
Sonderstellen und Flags ist die Strategie ein No-op (bit-identische Pläne).
"""
import json
from pathlib import Path

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import LBVorgabe, RaumModell
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


# ── Niveauänderung: §4.1.2 c) belegt die Leuchte, nicht das Zeichen ────────
# Korrektur 05.09.2026 (Enis). Die Einleitung von §4.1.2 (Norm-S.8) verlangt an den
# aufgezählten Stellen Sicherheitsleuchten; d) verlangt nur, dass VORHANDENE
# Sicherheitszeichen beleuchtet werden. Ein RZ entsteht daher nur aus einer
# expliziten LB-Vorgabe — und trägt dann lb_quelle statt norm_quelle.

def _niveau_raum():
    return _raum(sonderstellen=[_stelle("niveauaenderung", (500.0, 500.0))])


def test_niveauaenderung_ohne_lb_nur_sicherheitsleuchte():
    out = plan_sonderstellen(_niveau_raum(), FakeNormProvider())
    assert [p.kind for p in out] == ["sicherheitsleuchte"]
    assert out[0].xy_mm == (500.0, 500.0)
    assert out[0].norm_quelle in set(FakeNormProvider().regelwerk_snapshot().quellen)


def test_niveauaenderung_mit_unpassender_lb_kein_rz():
    """Eine LB, die RZ nur an Kreuzungen fordert, begründet hier nichts."""
    lb = LBVorgabe(rz_stellen=["kreuzung"], lb_quelle="LB-Test §1")
    out = plan_sonderstellen(_niveau_raum(), FakeNormProvider(), lb)
    assert [p.kind for p in out] == ["sicherheitsleuchte"]


def test_niveauaenderung_mit_expliziter_lb_erzeugt_rz_mit_lb_quelle():
    lb = LBVorgabe(rz_stellen=["niveauaenderung"], lb_quelle="Elektro-LB §5.1.23")
    out = plan_sonderstellen(_niveau_raum(), FakeNormProvider(), lb)
    kinds = sorted(p.kind for p in out)
    assert kinds == ["rz", "sicherheitsleuchte"]
    assert {p.xy_mm for p in out} == {(500.0, 500.0)}
    rz = next(p for p in out if p.kind == "rz")
    assert rz.richtung == "gerade"                    # beidseitig — Richtung unbestimmt
    # Provenienz: die LB begründet es, nicht die Norm.
    assert rz.lb_quelle == "Elektro-LB §5.1.23"
    assert rz.norm_quelle == ""
    # Die Sicherheitsleuchte bleibt norm-begründet.
    sl = next(p for p in out if p.kind == "sicherheitsleuchte")
    assert sl.norm_quelle and sl.lb_quelle == ""


def test_lb_ohne_eigene_quelle_bekommt_sprechenden_fallback():
    lb = LBVorgabe(rz_stellen=["niveauaenderung"])
    rz = next(
        p for p in plan_sonderstellen(_niveau_raum(), FakeNormProvider(), lb)
        if p.kind == "rz"
    )
    assert "rz_stellen" in rz.lb_quelle


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


def test_barrierefreies_zimmer_loest_4_3_8_nicht_aus():
    """§4.3.8 nennt „Toiletten für Menschen mit Behinderung" (Norm-S.11) — das Flag
    allein genügt nicht. Andere Anforderungen an den Raum bleiben unberührt; sie
    kommen aus den übrigen Strategien, nicht aus diesem Auslöser."""
    zimmer = {
        "id": "zimmer_bf", "raum_typ": "ZIMMER", "flaeche_m2": 24.0,
        "polygon_mm": [[0.0, 0.0], [6000.0, 0.0], [6000.0, 4000.0], [0.0, 4000.0]],
        "ist_fluchtweg": False, "ist_communal": False, "ist_barrierefrei": True,
    }
    assert plan_flag_raeume(_raum(extra_raeume=[zimmer]), FakeNormProvider()) == []


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


def test_nachpass_haelt_zugeordnete_sicherheitsleuchte_unter_2m():
    """Der Abstands-Nachpass darf die Pflicht-Leuchte nudgen — die Norm-ANMERKUNG
    „nahe ≤ 2 m" (§4.1.2) muss NACH dem Nachpass halten.

    Geschärft am 05.09. (Enis): geprüft wird die **der Anforderung zugeordnete
    Leuchtenart** — eine Sicherheitsleuchte. Ein zufällig benachbartes
    Rettungszeichen erfüllt §4.1.2 nicht und darf den Test nicht bestehen lassen.
    Zwei Stellen 100 mm auseinander provozieren Merge/Nudge an der Naht.
    """
    from notbeleuchtung.platzierung import NotlichtPlatzierer

    stellen = [
        _stelle("feuerloescher", (99999.0, 99999.0), sid="s1"),
        _stelle("hydrant", (99999.0, 99899.0), sid="s2"),
    ]
    raum = _raum(sonderstellen=stellen)
    ergebnis = NotlichtPlatzierer().place(raum, FakeNormProvider())
    for s in raum.sonderstellen:
        kandidaten = [
            p for p in ergebnis.platzierungen if p.kind == "sicherheitsleuchte"
        ]
        assert kandidaten, f"Stelle {s.id}: gar keine Sicherheitsleuchte im Plan"
        dist = min(_abstand(p.xy_mm, s.xy_mm) for p in kandidaten)
        assert dist <= 2000.0, (
            f"Stelle {s.id}: nächste SICHERHEITSLEUCHTE {dist:.0f} mm entfernt"
        )


def test_benachbartes_rz_erfuellt_die_2m_regel_nicht():
    """Gegenprobe zur Testschärfung: ein RZ in der Nähe zählt nicht als Erfüllung.

    Ohne LB entsteht an einer Niveauänderung nur eine Sicherheitsleuchte; wäre die
    Zuordnung art-blind, würde ein beliebiges RZ aus einer anderen Strategie den
    Nachweis vortäuschen.
    """
    from notbeleuchtung.platzierung import NotlichtPlatzierer

    stelle = _stelle("niveauaenderung", (99999.0, 99999.0), sid="s_niveau")
    raum = _raum(sonderstellen=[stelle])
    plz = NotlichtPlatzierer().place(raum, FakeNormProvider()).platzierungen
    nah = [p for p in plz if _abstand(p.xy_mm, (99999.0, 99999.0)) <= 2000.0]
    assert nah, "keine Leuchte an der Stelle"
    assert any(p.kind == "sicherheitsleuchte" for p in nah)
    # Ohne LB darf dort kein Rettungszeichen stehen (§4.1.2 c) belegt keines).
    assert not any(p.kind == "rz" for p in nah)


def _abstand(a, b) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
