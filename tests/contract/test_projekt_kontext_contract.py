"""Contract 4 (ProjektKontext / OIB-RL 2 Tabelle 6) — Modell-Validierung + Naht.

Nur Contract-/Testgrundlage: KEINE Tabelle-6-Grenzwerte, kein Resolver.
"""
import json
import math
from pathlib import Path

import jsonschema
import pytest
from pydantic import ValidationError

from notbeleuchtung.hauptengine.contracts import (
    Gebaeudeteil,
    ProjektKontext,
    RaumModell,
    RaumReferenz,
)

SCHEMA = Path("src/notbeleuchtung/hauptengine/contracts/schema/projekt_kontext.schema.json")
RAUM_FIXTURE = Path("tests/fixtures/raum_modell_4og.json")


def _load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def _wohnteil(**over) -> dict:
    return {"id": "wohnteil", "nutzungsart": "WOHNGEBAEUDE", "gebaeudeklasse": "GK4",
            "netto_grundflaeche_m2": 1200.0, **over}


def _garage(**over) -> dict:
    return {"id": "garage", "nutzungsart": "GARAGE", "nutzflaeche_garage_m2": 250.0, **over}


# 1 --------------------------------------------------------------------------------
def test_gueltiger_projektkontext_wohnteil_plus_garage():
    pk = ProjektKontext(
        jurisdiction="AT", bundesland="W",
        gebaeudeteile=[Gebaeudeteil(**_wohnteil()), Gebaeudeteil(**_garage())],
    )
    assert pk.contract == "ProjektKontext"
    assert pk.contract_version == "1.0.0"
    assert [g.id for g in pk.gebaeudeteile] == ["wohnteil", "garage"]
    # Fixture ist auch schema-valide.
    jsonschema.validate(instance=pk.model_dump(mode="json"), schema=_load(SCHEMA))


# 2 --------------------------------------------------------------------------------
def test_raumreferenzen_ueber_mehrere_geschosse():
    teil = Gebaeudeteil(**_wohnteil(raum_referenzen=[
        RaumReferenz(floor="EG", raum_id="r1"),
        RaumReferenz(floor="1OG", raum_id="r1"),   # gleiche raum_id, anderes Geschoss
        RaumReferenz(floor="1OG", raum_id="r2"),
    ]))
    floors = {r.floor for r in teil.raum_referenzen}
    assert floors == {"EG", "1OG"}


# 3 --------------------------------------------------------------------------------
def test_doppelte_gebaeudeteil_id_wird_abgelehnt():
    with pytest.raises(ValidationError):
        ProjektKontext(gebaeudeteile=[
            Gebaeudeteil(**_wohnteil(id="x")),
            Gebaeudeteil(**_garage(id="x")),
        ])


# 4 / 5 ----------------------------------------------------------------------------
def test_leere_raum_id_wird_abgelehnt():
    with pytest.raises(ValidationError):
        RaumReferenz(floor="EG", raum_id="")


def test_leeres_floor_wird_abgelehnt():
    with pytest.raises(ValidationError):
        RaumReferenz(floor="  ", raum_id="r1")


def test_leere_gebaeudeteil_id_wird_abgelehnt():
    with pytest.raises(ValidationError):
        Gebaeudeteil(**_wohnteil(id=""))


# 6 --------------------------------------------------------------------------------
@pytest.mark.parametrize("feld", ["netto_grundflaeche_m2", "verkaufsflaeche_m2",
                                  "nutzflaeche_garage_m2", "fluchtniveau_m"])
def test_negative_flaeche_oder_hoehe_wird_abgelehnt(feld):
    with pytest.raises(ValidationError):
        Gebaeudeteil(**_wohnteil(**{feld: -1.0}))


# 7 --------------------------------------------------------------------------------
@pytest.mark.parametrize("feld", ["betten_anzahl", "schlafplaetze_anzahl",
                                  "verabreichungsplaetze_anzahl", "personen_anzahl_bestimmt"])
def test_negative_zaehlwerte_werden_abgelehnt(feld):
    with pytest.raises(ValidationError):
        Gebaeudeteil(**_wohnteil(**{feld: -1}))


# 8 --------------------------------------------------------------------------------
@pytest.mark.parametrize("feld", ["netto_grundflaeche_m2", "fluchtniveau_m"])
@pytest.mark.parametrize("wert", [math.nan, math.inf, -math.inf])
def test_nan_infinity_bei_flaeche_oder_fluchtniveau_wird_abgelehnt(feld, wert):
    with pytest.raises(ValidationError):
        Gebaeudeteil(**_wohnteil(**{feld: wert}))


# 9 --------------------------------------------------------------------------------
def test_none_bei_optionalen_fachwerten_bleibt_erlaubt():
    teil = Gebaeudeteil(id="t", nutzungsart="SONSTIGES_GEBAEUDE")
    assert teil.gebaeudeklasse is None
    assert teil.fluchtniveau_m is None
    assert teil.netto_grundflaeche_m2 is None
    assert teil.betten_anzahl is None
    assert teil.arbeitsstaette_nach_aschg is None
    assert teil.lage_zur_wohnung is None


# G — Naht zum RaumModell (nur Contract-/Testgrundlage, kein Resolver) --------------
def test_naht_raumreferenz_gegen_raummodell():
    raum = RaumModell.model_validate(_load(RAUM_FIXTURE))
    bekannte_ids = {r.id for r in raum.raeume}
    teil = Gebaeudeteil(id="wohnteil", nutzungsart="WOHNGEBAEUDE", raum_referenzen=[
        RaumReferenz(floor=raum.floor, raum_id="stgh_a"),
    ])
    for ref in teil.raum_referenzen:
        # Diese Invariante wird später im OIB-Resolver global geprüft:
        assert ref.floor == raum.floor
        assert ref.raum_id in bekannte_ids
