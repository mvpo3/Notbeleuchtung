"""Contract 5 (OibBefund/OibErgebnis / OIB-Pfad-Output) — Modell + Schema.

Nur Contract-Grundlage: KEINE Tabelle-6-Grenzwerte, kein Resolver.
"""
import json
from pathlib import Path

import jsonschema

from notbeleuchtung.hauptengine.contracts import (
    OibBefund,
    OibErgebnis,
    RaumReferenz,
)

SCHEMA = Path("src/notbeleuchtung/hauptengine/contracts/schema/oib_ergebnis.schema.json")


def _load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def test_leerer_befund_baubar_und_schema_valide():
    befund = OibBefund()
    assert befund.contract == "OibBefund"
    assert befund.contract_version == "1.1.0"
    assert befund.ergebnisse == []
    jsonschema.validate(instance=befund.model_dump(mode="json"), schema=_load(SCHEMA))


# 10 -------------------------------------------------------------------------------
def test_review_required_kann_fehlende_fakten_tragen():
    erg = OibErgebnis(
        gebaeudeteil_id="wohnteil",
        stufe="review_required",
        quelle="OIB-RL 2",
        norm_ausgabe="2019",
        fehlende_fakten=["netto_grundflaeche_m2", "gebaeudeklasse"],
    )
    assert erg.stufe == "review_required"
    assert "gebaeudeklasse" in erg.fehlende_fakten

    befund = OibBefund(
        ergebnisse=[erg],
        nicht_zugeordnete_raum_referenzen=[RaumReferenz(floor="EG", raum_id="r9")],
    )
    jsonschema.validate(instance=befund.model_dump(mode="json"), schema=_load(SCHEMA))
    assert befund.nicht_zugeordnete_raum_referenzen[0].raum_id == "r9"
