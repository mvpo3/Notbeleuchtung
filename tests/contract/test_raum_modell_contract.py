"""Contract 1 (RaumModell / Selman) — Fixture valide gegen Pydantic + JSON-Schema."""
import json
from pathlib import Path

import jsonschema

from notbeleuchtung.hauptengine.contracts import RaumModell

SCHEMA = Path("src/notbeleuchtung/hauptengine/contracts/schema/raum_modell.schema.json")
FIXTURE = Path("tests/fixtures/raum_modell_4og.json")


def _load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def test_fixture_parses_pydantic():
    m = RaumModell.model_validate(_load(FIXTURE))
    assert m.contract == "RaumModell"
    assert m.floor == "4OG"
    assert len(m.zirkulation.segmente) == 5


def test_fixture_valid_against_generated_schema():
    jsonschema.validate(instance=_load(FIXTURE), schema=_load(SCHEMA))


def test_segment_ids_unique():
    m = RaumModell.model_validate(_load(FIXTURE))
    ids = [s.segment_id for s in m.zirkulation.segmente]
    assert len(ids) == len(set(ids))
