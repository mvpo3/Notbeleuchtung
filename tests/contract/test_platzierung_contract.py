"""Contract 3 (PlatzierungsErgebnis / Leonis) — Fixture valide + Naht-Invarianten.

Die Naht-Invarianten sind der Kern von „alle drei kommunizieren": eine Platzierung
darf nur Segmente/Quellen referenzieren, die Selman/Enis tatsächlich geliefert
haben; ein catalog_key muss im Schrack-Mapping existieren.
"""
import json
from pathlib import Path

import jsonschema
import pytest
import yaml

from notbeleuchtung.hauptengine.contracts import (
    NormRegelwerk,
    Platzierung,
    PlatzierungsErgebnis,
    RaumModell,
)

SCHEMA = Path("src/notbeleuchtung/hauptengine/contracts/schema/platzierung_ergebnis.schema.json")
PLATZ = Path("tests/fixtures/platzierung_4og.json")
RAUM = Path("tests/fixtures/raum_modell_4og.json")
NORM = Path("tests/fixtures/norm_regelwerk_snapshot.json")
MAPPING = Path("src/notbeleuchtung/symbols/schrack_symbol_mapping.yaml")


def _load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def test_fixture_parses_and_validates():
    PlatzierungsErgebnis.model_validate(_load(PLATZ))
    jsonschema.validate(instance=_load(PLATZ), schema=_load(SCHEMA))


def test_lb_quelle_default_leer_und_setzbar():
    """1.1.0: Platzierung trägt LB-Provenienz (2. Input). Default leer = rein norm-getrieben."""
    p = Platzierung(xy_mm=(0.0, 0.0), catalog_key="k", kind="rz")
    assert p.lb_quelle == ""
    p2 = Platzierung(xy_mm=(0.0, 0.0), catalog_key="k", kind="sicherheitsleuchte",
                     lb_quelle="LB Fischa §2.11")
    assert p2.lb_quelle == "LB Fischa §2.11"
    # Alte Fixture (ohne lb_quelle) bleibt gültig — additiv/abwärtskompatibel.
    assert all(p.lb_quelle == "" for p in PlatzierungsErgebnis.model_validate(_load(PLATZ)).platzierungen)


def test_naht_covers_segment_in_raummodell():
    """Leonis ↔ Selman: jedes covers_segment ist ein segment_id aus dem RaumModell."""
    plaz = PlatzierungsErgebnis.model_validate(_load(PLATZ))
    raum = RaumModell.model_validate(_load(RAUM))
    valid = {s.segment_id for s in raum.zirkulation.segmente}
    for p in plaz.platzierungen:
        for seg in p.covers_segment:
            assert seg in valid, f"covers_segment {seg!r} fehlt im RaumModell"


def test_naht_norm_quelle_in_regelwerk():
    """Leonis ↔ Enis: jede norm_quelle stammt aus dem NormRegelwerk."""
    plaz = PlatzierungsErgebnis.model_validate(_load(PLATZ))
    norm = NormRegelwerk.model_validate(_load(NORM))
    quellen = set(norm.quellen)
    for p in plaz.platzierungen:
        assert p.norm_quelle in quellen, f"norm_quelle {p.norm_quelle!r} nicht im Regelwerk"


def test_naht_catalog_key_in_mapping():
    """catalog_key ∈ Schrack-Mapping. Skip bis das Mapping portiert ist (Slice 2/3)."""
    if not MAPPING.exists():
        pytest.skip("schrack_symbol_mapping.yaml noch nicht portiert (Slice 2/3)")
    with open(MAPPING, encoding="utf-8") as fh:
        mapping = yaml.safe_load(fh) or {}
    keys = set(mapping.keys())
    plaz = PlatzierungsErgebnis.model_validate(_load(PLATZ))
    for p in plaz.platzierungen:
        assert p.catalog_key in keys, f"catalog_key {p.catalog_key!r} fehlt im Mapping"
