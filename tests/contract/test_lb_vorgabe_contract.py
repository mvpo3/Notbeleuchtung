"""Contract 6 (LBVorgabe / 2. Input Leistungsbeschreibung) — Modell + Schema.

Contract-Grundlage aus knowledge/extracted/LB_ANALYSE_beispiele.md (reale LBs).
Kein LB-Parser hier (Enis' Lane) — nur die Vorgabe-Struktur + Validierung.
"""
import json
import math
from pathlib import Path

import jsonschema
import pytest
from pydantic import ValidationError

from notbeleuchtung.hauptengine.contracts import (
    BereichsRegel,
    LBVorgabe,
    SonderLux,
)

SCHEMA = Path("src/notbeleuchtung/hauptengine/contracts/schema/lb_vorgabe.schema.json")


def _load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def test_leere_lb_ist_reines_norm_verhalten():
    # Kein 2. Input spezifiziert → alle Felder None/leer → Norm greift.
    lb = LBVorgabe()
    assert lb.contract == "LBVorgabe"
    assert lb.contract_version == "1.0.0"
    assert lb.system_typ is None
    assert lb.bereiche_exklusion == []
    jsonschema.validate(instance=lb.model_dump(mode="json"), schema=_load(SCHEMA))


def test_fischa_gk4_exklusion_stiegenhaus():
    # Kanonischer Override: GK4 → KEINE Sicherheitsbeleuchtung in Stiegenhaus/Gängen.
    lb = LBVorgabe(
        projekt="Fischamender Str. 46",
        system_typ="gruppenbatterie",
        betriebsdauer_min=480,          # 8 Std
        umschaltzeit_max_s=0.5,
        mindest_lux_fluchtweg=1.0,
        bereiche_exklusion=[
            BereichsRegel(raum_typ="STIEGENHAUS", sicherheitsbeleuchtung=False, begruendung="GK4"),
            BereichsRegel(raum_typ="GANG", sicherheitsbeleuchtung=False, begruendung="GK4"),
        ],
        bereiche_inklusion=[BereichsRegel(raum_typ="GARAGE", sicherheitsbeleuchtung=True)],
        sonder_lux=[SonderLux(ort="feuerloescher", min_lux=5.0)],
        rz_stellen=["fluchttuer", "kreuzung", "richtungsaenderung"],
        piktogramm_norm="EN ISO 7010",
        lb_quelle="20241209_E LV Fischa 46.pdf §2.10/2.11",
    )
    assert lb.betriebsdauer_min == 480
    assert {b.raum_typ for b in lb.bereiche_exklusion} == {"STIEGENHAUS", "GANG"}
    jsonschema.validate(instance=lb.model_dump(mode="json"), schema=_load(SCHEMA))


def test_widerspruch_inklusion_exklusion_wird_abgelehnt():
    with pytest.raises(ValidationError):
        LBVorgabe(
            bereiche_inklusion=[BereichsRegel(raum_typ="GANG", sicherheitsbeleuchtung=True)],
            bereiche_exklusion=[BereichsRegel(raum_typ="GANG", sicherheitsbeleuchtung=False)],
        )


def test_leerer_raum_typ_wird_abgelehnt():
    with pytest.raises(ValidationError):
        BereichsRegel(raum_typ="  ", sicherheitsbeleuchtung=True)


@pytest.mark.parametrize("feld,wert", [
    ("betriebsdauer_min", -1),
    ("umschaltzeit_max_s", -0.1),
    ("mindest_lux_fluchtweg", -1.0),
])
def test_negative_werte_werden_abgelehnt(feld, wert):
    with pytest.raises(ValidationError):
        LBVorgabe(**{feld: wert})


@pytest.mark.parametrize("wert", [math.nan, math.inf, -math.inf])
def test_nan_infinity_bei_umschaltzeit_wird_abgelehnt(wert):
    with pytest.raises(ValidationError):
        LBVorgabe(umschaltzeit_max_s=wert)


def test_unbekannter_system_typ_wird_abgelehnt():
    with pytest.raises(ValidationError):
        LBVorgabe(system_typ="dieselaggregat")


def test_unbekannte_rz_stelle_wird_abgelehnt():
    with pytest.raises(ValidationError):
        LBVorgabe(rz_stellen=["im_keller_irgendwo"])
