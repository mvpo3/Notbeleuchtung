"""Guard für die Gate-Regel — synthetische Messungen, ohne DXF und ohne Referenz.

Geprüft wird die REGEL, nicht die Erkennung: je Bedingung ein Verstoß-Fall, der
erfüllte Stapel als leere Liste, und die heutige Lage (Nullmessung gegen sich
selbst) als fester Erwartungswert. Die eingecheckte Nullmessung läuft als
letzter Fall mit — sie braucht weder Plan noch Referenzpaket.

Die synthetischen Messungen führen bewusst KEIN ``meta``; Bedingung (0) wird
dann übersprungen. Ihre eigenen Fälle bauen ``meta`` gezielt auf.
"""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from gate_m1_m4 import GATE_KENNZAHLEN, PLAENE
from gate_regel import NENNER, pruefe_gate

NULLMESSUNG = Path(__file__).resolve().parent / "nullmessung_f15d03f.json"
IDS = [f"M17-0{fall}-{check}" for fall in range(1, 7) for check in "abc"]
# Lage der Nullmessung: alles BESTANDEN außer den beiden bekannten Fällen.
NULL_STATUS = {"M17-02-b": "NICHT_BESTANDEN", "M17-04-c": "NICHT_MESSBAR"}


def _messung(status: dict[str, str], einraum: int = 2, a_gleich_b: int = 0) -> dict:
    """Messung im Format von ``gate_messung.messung``; alle Kennzahlen auf 3."""
    m1_m4: dict[str, dict[str, dict[str, float]]] = {}
    for kennzahl in GATE_KENNZAHLEN:
        skript, kopf = kennzahl.split(".")
        for plan in PLAENE:
            m1_m4.setdefault(skript, {}).setdefault(plan, {})[kopf] = 3
    return {
        "meta": {},
        "m17": [{"id": eid, "status": status.get(eid, "BESTANDEN")} for eid in IDS],
        "og1": {"tueren_raum_a_gleich_b": a_gleich_b, "einraum_wohnungen": einraum},
        "m1_m4": m1_m4,
    }


def _nullmessung() -> dict:
    return _messung(NULL_STATUS)


def _erfuellt() -> dict:
    """Nachher-Stand, der das Gate vollständig erfüllt."""
    return _messung({"M17-04-c": "NICHT_MESSBAR"}, einraum=1)


def _mit_meta(messung: dict, **abweichung) -> dict:
    """Dieselbe Messung mit vollständigem ``meta`` — Bedingung (0) greift dann."""
    messung = deepcopy(messung)
    messung["meta"] = {
        "dxf": dict.fromkeys(PLAENE, "sha-gleich"),
        "referenz_sha256": "ref-gleich",
        "toleranzen": {"kontakt_mm": 1.0, "ueberlappung_mm2": 1.0, "portal_wand_mm": 250.0},
        "arbeitsbaum_src_scripts_sauber": True,
    }
    messung["meta"].update(abweichung)
    return messung


def test_nullmessung_gegen_sich_selbst_meldet_genau_zwei_verstoesse():
    verstoesse = pruefe_gate(_nullmessung(), _nullmessung())
    assert len(verstoesse) == 2, verstoesse
    assert verstoesse[0].startswith("(2) M17-02-b ist NICHT_BESTANDEN")
    assert verstoesse[1] == "(5) Einraum-Wohnungen sinken nicht: 2 → 2"


def test_erfuellter_stapel_meldet_nichts():
    assert pruefe_gate(_nullmessung(), _erfuellt()) == []


def test_erfuellter_stapel_mit_meta_meldet_nichts():
    assert pruefe_gate(_mit_meta(_nullmessung()), _mit_meta(_erfuellt())) == []


def test_bestanden_faellt_auf_nicht_bestanden():
    nachher = _erfuellt()
    nachher["m17"][0]["status"] = "NICHT_BESTANDEN"
    assert "(1) M17-01-a fällt von BESTANDEN auf NICHT_BESTANDEN" in pruefe_gate(
        _nullmessung(), nachher)


def test_bestanden_faellt_auf_nicht_messbar():
    nachher = _erfuellt()
    nachher["m17"][0]["status"] = "NICHT_MESSBAR"
    assert "(1) M17-01-a fällt von BESTANDEN auf NICHT_MESSBAR" in pruefe_gate(
        _nullmessung(), nachher)


def test_nicht_messbar_wird_nicht_bestanden_ist_kein_verstoss():
    """Owner-Regel zählt nur Verluste von BESTANDEN — M17-04-c trug nie einen Beleg."""
    nachher = _messung({"M17-04-c": "NICHT_BESTANDEN"}, einraum=1)
    assert pruefe_gate(_nullmessung(), nachher) == []


def test_wand_nicht_mehr_erkannt_ist_verstoss_gegen_zwei_und_eins():
    nachher = _erfuellt()
    nachher["m17"][IDS.index("M17-02-a")]["status"] = "NICHT_BESTANDEN"
    verstoesse = pruefe_gate(_nullmessung(), nachher)
    assert any(v.startswith("(1) M17-02-a") for v in verstoesse)
    assert any(v.startswith("(2) M17-02-a") for v in verstoesse)


def test_kennzahl_steigt_in_einem_plan():
    nachher = deepcopy(_erfuellt())
    nachher["m1_m4"]["M3"]["OG1"]["hauptwert"] = 4
    assert pruefe_gate(_nullmessung(), nachher) == ["(3) M3.hauptwert steigt in OG1: 3 → 4"]


def test_kennzahl_sinkt_ist_kein_verstoss():
    nachher = deepcopy(_erfuellt())
    nachher["m1_m4"]["M3"]["OG1"]["hauptwert"] = 0
    assert pruefe_gate(_nullmessung(), nachher) == []


def test_flaeche_steigt_innerhalb_der_toleranz_ist_kein_verstoss():
    vorher, nachher = deepcopy(_nullmessung()), deepcopy(_erfuellt())
    vorher["m1_m4"]["M3"]["OG1"]["rote_flaeche_m2"] = 12.5
    nachher["m1_m4"]["M3"]["OG1"]["rote_flaeche_m2"] = 12.5009
    assert pruefe_gate(vorher, nachher) == []


def test_flaeche_steigt_ueber_die_toleranz_ist_verstoss():
    vorher, nachher = deepcopy(_nullmessung()), deepcopy(_erfuellt())
    vorher["m1_m4"]["M3"]["OG1"]["rote_flaeche_m2"] = 12.5
    nachher["m1_m4"]["M3"]["OG1"]["rote_flaeche_m2"] = 12.52
    assert pruefe_gate(vorher, nachher) == [
        "(3) M3.rote_flaeche_m2 steigt in OG1: 12.5 → 12.52"]


def test_tueren_raum_a_gleich_b_groesser_null():
    nachher = _messung({"M17-04-c": "NICHT_MESSBAR"}, einraum=1, a_gleich_b=2)
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(4) Türen mit raum_a == raum_b: 2, erwartet: 0"]


def test_einraum_wohnungen_gleich_ist_verstoss():
    nachher = _messung({"M17-04-c": "NICHT_MESSBAR"}, einraum=2)
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(5) Einraum-Wohnungen sinken nicht: 2 → 2"]


def test_fehlende_id_aendert_nenner_und_ist_verstoss():
    nachher = _erfuellt()
    nachher["m17"] = [e for e in nachher["m17"] if e["id"] != "M17-05-b"]
    verstoesse = pruefe_gate(_nullmessung(), nachher)
    assert f"(1) Nenner: 17 Erwartungen gemessen, erwartet sind {NENNER}" in verstoesse
    assert any("fehlend ['M17-05-b']" in v for v in verstoesse)
    assert "(1) M17-05-b fällt von BESTANDEN auf nicht gemessen" in verstoesse


# ----------------------------------------------- (0) Vergleichbarkeit

def test_abweichende_dxf_ist_verstoss_null():
    vorher = _mit_meta(_nullmessung())
    nachher = _mit_meta(_erfuellt(), dxf={**dict.fromkeys(PLAENE, "sha-gleich"),
                                          "OG2": "sha-anders"})
    assert pruefe_gate(vorher, nachher) == [
        "(0) andere Eingabe-DXF für OG2: sha-gleich → sha-anders"]


def test_fehlender_plan_in_meta_dxf_ist_verstoss_null():
    nachher = _mit_meta(_erfuellt())
    del nachher["meta"]["dxf"]["DG2"]
    assert pruefe_gate(_mit_meta(_nullmessung()), nachher) == [
        "(0) andere Eingabe-DXF für DG2: sha-gleich → fehlt"]


def test_abweichende_referenz_ist_verstoss_null():
    nachher = _mit_meta(_erfuellt(), referenz_sha256="ref-anders")
    assert pruefe_gate(_mit_meta(_nullmessung()), nachher) == [
        "(0) anderes Referenzpaket: ref-gleich → ref-anders"]


def test_abweichende_toleranz_ist_verstoss_null():
    nachher = _mit_meta(_erfuellt(), toleranzen={"kontakt_mm": 5.0})
    verstoesse = pruefe_gate(_mit_meta(_nullmessung()), nachher)
    assert len(verstoesse) == 1 and verstoesse[0].startswith("(0) andere Toleranzen:")


def test_dirty_arbeitsbaum_im_nachher_ist_verstoss_null():
    nachher = _mit_meta(_erfuellt(), arbeitsbaum_src_scripts_sauber=False)
    verstoesse = pruefe_gate(_mit_meta(_nullmessung()), nachher)
    assert len(verstoesse) == 1
    assert verstoesse[0].startswith("(0) Nachher-Stand mit unsauberem Arbeitsbaum")


def test_fehlendes_sauber_flag_im_nachher_ist_verstoss_null():
    nachher = _mit_meta(_erfuellt())
    del nachher["meta"]["arbeitsbaum_src_scripts_sauber"]
    assert any(v.startswith("(0) Nachher-Stand mit unsauberem Arbeitsbaum")
               for v in pruefe_gate(_mit_meta(_nullmessung()), nachher))


def test_ohne_meta_wird_bedingung_null_uebersprungen():
    """Eine Seite ohne meta: die Regel bleibt prüfbar, (0) schweigt."""
    assert pruefe_gate(_nullmessung(), _mit_meta(_erfuellt())) == []


# ----------------------------------------- (3) Vollständigkeit beidseitig

def test_fehlende_kennzahl_im_nachher_ist_verstoss():
    nachher = deepcopy(_erfuellt())
    del nachher["m1_m4"]["M2"]["DG2"]
    assert "(3) M2.wert fehlt im Nachher-Stand für Plan DG2" in pruefe_gate(
        _nullmessung(), nachher)


def test_fehlender_plan_im_vorher_ist_verstoss():
    vorher = deepcopy(_nullmessung())
    del vorher["m1_m4"]["M1"]["EG"]
    verstoesse = pruefe_gate(vorher, _erfuellt())
    assert "(3) M1.hauptwert fehlt im Vorher-Stand für Plan EG" in verstoesse
    assert "(3) M1.klein_ohne_stempel fehlt im Vorher-Stand für Plan EG" in verstoesse


def test_nan_als_kennzahl_ist_verstoss():
    nachher = deepcopy(_erfuellt())
    nachher["m1_m4"]["M3"]["OG1"]["rote_flaeche_m2"] = float("nan")
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(3) M3.rote_flaeche_m2 in OG1 ist keine Zahl ≥ 0: nachher nan"]


def test_bool_als_kennzahl_ist_verstoss():
    nachher = deepcopy(_erfuellt())
    nachher["m1_m4"]["M4"]["UG"]["einraum"] = True
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(3) M4.einraum in UG ist keine Zahl ≥ 0: nachher True"]


def test_negative_kennzahl_ist_verstoss():
    nachher = deepcopy(_erfuellt())
    nachher["m1_m4"]["M2"]["UG"]["wert"] = -1
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(3) M2.wert in UG ist keine Zahl ≥ 0: nachher -1"]


def test_echte_nullmessung_gegen_sich_selbst():
    """Die eingecheckte Nullmessung ist der Vorher-Stand — heute fehlen (2) und (5)."""
    null = json.loads(NULLMESSUNG.read_text(encoding="utf-8"))
    verstoesse = pruefe_gate(null, deepcopy(null))
    assert verstoesse == [
        "(2) M17-02-b ist NICHT_BESTANDEN, erwartet: BESTANDEN",
        "(5) Einraum-Wohnungen sinken nicht: 2 → 2",
    ]
