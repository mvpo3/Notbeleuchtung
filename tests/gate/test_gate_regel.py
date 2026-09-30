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
# Lage der Nullmessung: alles BESTANDEN außer den beiden bekannten roten Fällen
# (M17-04-c seit Lesart B, Enis 2026-09-18: NICHT_BESTANDEN statt NICHT_MESSBAR).
NULL_STATUS = {"M17-02-b": "NICHT_BESTANDEN", "M17-04-c": "NICHT_BESTANDEN"}


def _referenz(verneint: dict | None = None, gefordert: dict | None = None) -> dict:
    """Referenz-Abschnitt im Format von ``gate_referenz.verbindungen``.

    Ein verneinter Fall (0 Verbindungen) und ein geforderter (1 Verbindung) —
    so, wie (7) und (8) sie verlangen. Die Argumente überschreiben einzelne
    Felder des jeweiligen Eintrags."""
    eintrag_verneint = {
        "referenz": "M17-02 / Bsp. 07, 08, 14",
        "raum_a": {"raum_typ": "BAD", "flaeche_m2": 11.76, "id": "raum_7"},
        "raum_b": {"raum_typ": "BAD", "flaeche_m2": 4.66, "id": "raum_6"},
        "anzahl": 0, "ids": [], "quellen": {}, "ohne_tuerblatt": 0,
        "grund": "", "zusatz": False,
    }
    eintrag_gefordert = {
        "referenz": "O03 (Bsp. 06, 09, 14)",
        "raum_a": {"raum_typ": "GANG", "flaeche_m2": 6.48, "id": "raum_8"},
        "raum_b": {"raum_typ": "", "flaeche_m2": 73.06, "id": "raum_10"},
        "anzahl": 1, "ids": ["durchgang_17"], "quellen": {"durchgang": 1},
        "ohne_tuerblatt": 1, "grund": "", "hinweis": "",
    }
    eintrag_verneint.update(verneint or {})
    eintrag_gefordert.update(gefordert or {})
    return {"verneint": [eintrag_verneint], "gefordert": [eintrag_gefordert]}


def _barawitzka(**abweichung) -> dict:
    """Barawitzka-Abschnitt im Format von ``gate_barawitzka.verbindung_abstellraum``.

    Die Vorgabe ist der ZIELZUSTAND (eine Verbindung), nicht die heutige Lage:
    heute ist (10) verletzt (``anzahl`` 0) und dreht erst mit dem S4a-Rest
    (Doppelflügel-Paarung)."""
    eintrag = {
        "raum": {"raum_typ": "ABSTELLRAUM", "flaeche_m2": 1.98, "id": "raum_28"},
        "bezeichnung": "ABSTELLRAUM 1.98 m²",
        "anzahl": 1, "ids": ["tuer_38"], "grund": "",
        "naechste_tuer": {"id": "tuer_38", "quelle": "doppelfluegel", "breite_mm": 1660.0,
                          "tuer_detail": None, "abstand_mm": 0.0},
        "doppelfluegel_nah": [],
    }
    eintrag.update(abweichung)
    return eintrag


def _messung(status: dict[str, str], einraum: int = 2, a_gleich_b: int = 0,
             graph: int = 5, anker_privat: int = 0, referenz: dict | None = None,
             barawitzka: dict | None = None) -> dict:
    """Messung im Format von ``gate_messung.messung``; alle Kennzahlen auf 3.

    ``graph``/``anker_privat`` sind die Werte für Bedingung (6); die Vorgaben
    entsprechen der Lage der Nullmessung, dort ist (6) erfüllt. ``referenz``
    ist der Abschnitt für (7)/(8), ``barawitzka`` der für (10); beide Vorgaben
    erfüllen ihre Bedingung."""
    m1_m4: dict[str, dict[str, dict[str, float]]] = {}
    for kennzahl in GATE_KENNZAHLEN:
        skript, kopf = kennzahl.split(".")
        for plan in PLAENE:
            m1_m4.setdefault(skript, {}).setdefault(plan, {})[kopf] = 3
    return {
        "meta": {},
        "m17": [{"id": eid, "status": status.get(eid, "BESTANDEN")} for eid in IDS],
        "og1": {"tueren_raum_a_gleich_b": a_gleich_b, "einraum_wohnungen": einraum},
        "og3": {"segmente_graph": graph, "anker_in_wohnung_privat": anker_privat},
        "referenz": referenz if referenz is not None else _referenz(),
        "barawitzka": barawitzka if barawitzka is not None else _barawitzka(),
        "m1_m4": m1_m4,
    }


def _nullmessung() -> dict:
    return _messung(NULL_STATUS)


def _erfuellt() -> dict:
    """Nachher-Stand, der das Gate vollständig erfüllt — beide roten Fälle gedreht."""
    return _messung({}, einraum=1)


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


# ----------------------------------------------- (6) Rennweg OG3

def test_og3_ohne_graph_segment_ist_verstoss_sechs():
    nachher = _messung({}, einraum=1, graph=0)
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(6) Rennweg OG3 ohne GRAPH-Segment: segmente_graph=0, erwartet: >= 1"]


def test_og3_anker_in_wohnung_privat_ist_verstoss_sechs():
    nachher = _messung({}, einraum=1, anker_privat=1)
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(6) Anker in WOHNUNG_PRIVAT (Rennweg OG3): 1, erwartet: 0"]


def test_fehlender_og3_abschnitt_ist_verstoss_sechs():
    nachher = _erfuellt()
    del nachher["og3"]
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(6) Rennweg OG3 nicht gemessen — Abschnitt »og3« fehlt"]


def test_og3_erfuellt_meldet_nichts():
    """(6) ist heute schon erfüllt — GRAPH-Segmente da, kein Anker im Privaten."""
    assert pruefe_gate(_nullmessung(), _erfuellt()) == []


def test_nullmessung_gegen_sich_selbst_meldet_genau_drei_verstoesse():
    verstoesse = pruefe_gate(_nullmessung(), _nullmessung())
    assert len(verstoesse) == 3, verstoesse
    assert verstoesse[0].startswith("(2) M17-02-b ist NICHT_BESTANDEN")
    assert verstoesse[1].startswith("(2) M17-04-c ist NICHT_BESTANDEN")
    assert verstoesse[2] == "(5) Einraum-Wohnungen sinken nicht: 2 → 2"


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
    """Owner-Regel zählt nur Verluste von BESTANDEN — wer keinen Beleg trug, verliert keinen."""
    vorher = _messung({**NULL_STATUS, "M17-05-a": "NICHT_MESSBAR"})
    nachher = _messung({"M17-05-a": "NICHT_BESTANDEN"}, einraum=1)
    assert pruefe_gate(vorher, nachher) == []


def test_nur_02b_dreht_verletzt_bedingung_zwei_weiterhin():
    """Lesart B: BEIDE roten Fälle müssen drehen, 02-b allein reicht nicht."""
    nachher = _messung({"M17-04-c": "NICHT_BESTANDEN"}, einraum=1)
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(2) M17-04-c ist NICHT_BESTANDEN, erwartet: BESTANDEN"]


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
    nachher = _messung({}, einraum=1, a_gleich_b=2)
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(4) Türen mit raum_a == raum_b: 2, erwartet: 0"]


def test_einraum_wohnungen_gleich_ist_verstoss():
    nachher = _messung({}, einraum=2)
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(5) Einraum-Wohnungen sinken nicht: 2 → 2"]


def test_fehlende_id_aendert_nenner_und_ist_verstoss():
    nachher = _erfuellt()
    nachher["m17"] = [e for e in nachher["m17"] if e["id"] != "M17-05-b"]
    verstoesse = pruefe_gate(_nullmessung(), nachher)
    assert f"(1) Nenner: 17 Erwartungen gemessen, erwartet sind {NENNER}" in verstoesse
    assert any("fehlend ['M17-05-b']" in v for v in verstoesse)
    assert "(1) M17-05-b fällt von BESTANDEN auf nicht gemessen" in verstoesse


# -------------------------------- (7)/(8) Referenz-Verbindungen im OG1

def test_referenz_erfuellt_meldet_nichts():
    """Keine verneinte Verbindung, geforderter Übergang da — (7) und (8) schweigen."""
    assert pruefe_gate(_nullmessung(), _erfuellt()) == []


def test_verneinte_verbindung_besteht_ist_verstoss_sieben():
    nachher = _messung({}, einraum=1, referenz=_referenz(verneint={
        "anzahl": 3, "ids": ["durchgang_11", "durchgang_12", "durchgang_13"],
        "quellen": {"durchgang": 3}, "ohne_tuerblatt": 3}))
    assert pruefe_gate(_nullmessung(), nachher) == [
        ("(7) verneinte Verbindung besteht (M17-02 / Bsp. 07, 08, 14): "
         "BAD 11.76 m² ↔ BAD 4.66 m² — 3 Tür(en) "
         "['durchgang_11', 'durchgang_12', 'durchgang_13']")]


def test_verneinte_zusatz_verbindung_zaehlt_ebenfalls():
    """Die Nachbarschaften aus Bsp. 14 (``zusatz``) sind keine Ausnahme von (7)."""
    nachher = _messung({}, einraum=1, referenz=_referenz(verneint={
        "referenz": "Bsp. 14", "zusatz": True,
        "raum_a": {"raum_typ": "GANG", "flaeche_m2": 6.48, "id": "raum_8"},
        "raum_b": {"raum_typ": "STIEGENHAUS", "flaeche_m2": 11.21, "id": "raum_14"},
        "anzahl": 1, "ids": ["durchgang_99"]}))
    assert pruefe_gate(_nullmessung(), nachher) == [
        ("(7) verneinte Verbindung besteht (Bsp. 14): "
         "GANG 6.48 m² ↔ STIEGENHAUS 11.21 m² — 1 Tür(en) ['durchgang_99']")]


def test_nicht_aufloesbarer_raum_ist_verstoss_sieben():
    """``anzahl`` None heißt: nicht gemessen — und damit Verstoß, kein Freispruch."""
    nachher = _messung({}, einraum=1, referenz=_referenz(verneint={
        "raum_b": {"raum_typ": "BAD", "flaeche_m2": 4.66, "id": None},
        "anzahl": None, "grund": "kein Raum BAD 4.66 m² (±0.05 m²) im Modell"}))
    assert pruefe_gate(_nullmessung(), nachher) == [
        ("(7) verneinte Verbindung nicht messbar (M17-02 / Bsp. 07, 08, 14): "
         "BAD 11.76 m² ↔ BAD 4.66 m² — kein Raum BAD 4.66 m² (±0.05 m²) im Modell")]


def test_geforderter_uebergang_fehlt_ist_verstoss_acht():
    nachher = _messung({}, einraum=1,
                       referenz=_referenz(gefordert={"anzahl": 0, "ids": [], "quellen": {},
                                                     "ohne_tuerblatt": 0}))
    assert pruefe_gate(_nullmessung(), nachher) == [
        ("(8) geforderter Übergang fehlt (O03 (Bsp. 06, 09, 14)): "
         "GANG 6.48 m² ↔ (ohne Typ) 73.06 m²")]


def test_geforderter_uebergang_nicht_messbar_ist_verstoss_acht():
    nachher = _messung({}, einraum=1, referenz=_referenz(gefordert={
        "raum_a": {"raum_typ": "GANG", "flaeche_m2": 6.48, "id": None},
        "anzahl": None, "ids": [], "quellen": {}, "ohne_tuerblatt": 0,
        "grund": "2 Räume passen auf GANG 6.48 m²: ['raum_8', 'raum_9']"}))
    assert pruefe_gate(_nullmessung(), nachher) == [
        ("(8) geforderter Übergang nicht messbar (O03 (Bsp. 06, 09, 14)): "
         "GANG 6.48 m² ↔ (ohne Typ) 73.06 m² — "
         "2 Räume passen auf GANG 6.48 m²: ['raum_8', 'raum_9']")]


def test_fehlender_referenz_abschnitt_ist_verstoss_sieben_und_acht():
    nachher = _erfuellt()
    del nachher["referenz"]
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(7) verneinte Verbindungen nicht gemessen — Abschnitt »referenz.verneint« fehlt",
        "(8) geforderte Übergänge nicht gemessen — Abschnitt »referenz.gefordert« fehlt"]


# --------------------------------------- (10) Barawitzka EG ABSTELLRAUM 1,98 m²

def test_barawitzka_ohne_verbindung_ist_verstoss_zehn():
    """Das ist die HEUTIGE Lage: S5b nimmt dem Raum den letzten Durchgang, seine
    echte Tür steckt als Fehlpaarung im Doppelflügel 1660 mm. Die Bedingung dreht
    erst mit dem S4a-Rest — kein Slice dieses Branches heilt sie."""
    nachher = _messung({}, einraum=1, barawitzka=_barawitzka(anzahl=0, ids=[]))
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(10) Barawitzka EG ABSTELLRAUM 1.98 m² ohne Verbindung: 0 Tür(en)"]


def test_barawitzka_nicht_messbar_ist_verstoss_zehn():
    """``anzahl`` None heißt: nicht gemessen — und damit Verstoß, kein Freispruch."""
    nachher = _messung({}, einraum=1, barawitzka=_barawitzka(
        anzahl=None, ids=[], naechste_tuer=None,
        grund="kein Raum ABSTELLRAUM 1.98 m² (±0.05 m²) im Modell"))
    assert pruefe_gate(_nullmessung(), nachher) == [
        ("(10) Barawitzka EG ABSTELLRAUM 1.98 m² nicht messbar — "
         "kein Raum ABSTELLRAUM 1.98 m² (±0.05 m²) im Modell")]


def test_fehlender_barawitzka_abschnitt_im_nachher_ist_verstoss_zehn():
    nachher = _erfuellt()
    del nachher["barawitzka"]
    assert pruefe_gate(_nullmessung(), nachher) == [
        "(10) Barawitzka EG nicht gemessen — Abschnitt »barawitzka« fehlt"]


def test_fehlender_barawitzka_abschnitt_im_vorher_ist_kein_absturz():
    """(10) misst nur den Nachher-Stand: eine Vorher-Messung ohne den Abschnitt
    (die eingecheckte Nullmessung) bleibt prüfbar — fail closed nur nach hinten."""
    vorher = _nullmessung()
    del vorher["barawitzka"]
    assert pruefe_gate(vorher, _erfuellt()) == []


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
    """Die eingecheckte Nullmessung ist der Vorher-Stand — heute fehlen (2), (5), (7), (10).

    Die sechs (7)-Verstöße sind die acht Türverbindungen, die die Referenz
    verneint (dreimal zwischen den Bädern, fünfmal einzeln); (8) ist heute
    erfüllt, alle vier geforderten Übergänge stehen. Der (10)-Verstoß ist die
    Nullmessung selbst: sie stammt von VOR dem Messfall und führt den Abschnitt
    ``barawitzka`` nicht — als Nachher-Stand gelesen ist das ein Verstoß (fail
    closed), als Vorher-Stand kein Absturz. Neun Verstöße waren es, bevor (10)
    dazukam. Diese Erwartung ist die LAGE, nicht die Regel — dreht S5b die Fälle,
    schrumpft die Liste hier."""
    null = json.loads(NULLMESSUNG.read_text(encoding="utf-8"))
    verstoesse = pruefe_gate(null, deepcopy(null))
    assert verstoesse == [
        "(2) M17-02-b ist NICHT_BESTANDEN, erwartet: BESTANDEN",
        "(2) M17-04-c ist NICHT_BESTANDEN, erwartet: BESTANDEN",
        "(5) Einraum-Wohnungen sinken nicht: 2 → 2",
        ("(7) verneinte Verbindung besteht (M17-02 / Bsp. 07, 08, 14): "
         "BAD 11.76 m² ↔ BAD 4.66 m² — 3 Tür(en) "
         "['durchgang_11', 'durchgang_12', 'durchgang_13']"),
        ("(7) verneinte Verbindung besteht (Bsp. 06, 14): "
         "ZIMMER 17.04 m² ↔ GANG 6.48 m² — 1 Tür(en) ['durchgang_16']"),
        ("(7) verneinte Verbindung besteht (Bsp. 08, 09, 14): "
         "VORRAUM 3.4 m² ↔ BAD 4.66 m² — 1 Tür(en) ['durchgang_9']"),
        ("(7) verneinte Verbindung besteht (Bsp. 08, 14): "
         "ZIMMER 10.59 m² ↔ BAD 4.66 m² — 1 Tür(en) ['durchgang_3']"),
        ("(7) verneinte Verbindung besteht (Bsp. 09, 14): "
         "ZIMMER 16.86 m² ↔ VORRAUM 3.4 m² — 1 Tür(en) ['durchgang_6']"),
        ("(7) verneinte Verbindung besteht (Bsp. 07, 14): "
         "BAD 11.76 m² ↔ ZIMMER 17.04 m² — 1 Tür(en) ['durchgang_15']"),
        "(10) Barawitzka EG nicht gemessen — Abschnitt »barawitzka« fehlt",
    ]
