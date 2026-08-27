"""Contract 2 (NormRegelwerk / Enis) — Snapshot valide + Provider-Konformität."""
import json
from pathlib import Path

import jsonschema

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import (
    NormAnforderung,
    NormProvider,
    NormRegelwerk,
)

SCHEMA = Path("src/notbeleuchtung/hauptengine/contracts/schema/norm_regelwerk.schema.json")
FIXTURE = Path("tests/fixtures/norm_regelwerk_snapshot.json")


def _load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def test_snapshot_parses_and_validates():
    NormRegelwerk.model_validate(_load(FIXTURE))
    jsonschema.validate(instance=_load(FIXTURE), schema=_load(SCHEMA))


def test_provider_satisfies_protocol():
    prov = FakeNormProvider()
    assert isinstance(prov, NormProvider)   # runtime_checkable


def test_provider_query_returns_typed_anforderung():
    prov = FakeNormProvider()
    a = prov.fuer_raum("STIEGENHAUS", True)
    assert isinstance(a, NormAnforderung)
    assert a.klassifikation in ("rz", "antipanik", "sicherheitsleuchte")
    assert a.montagehoehe_mm >= 2000
    assert a.quelle in prov.regelwerk_snapshot().quellen


def test_erkennungsweite_l_gleich_z_mal_h():
    prov = FakeNormProvider()
    # l = z*h; hinterleuchtet z=200, h=0.15 m -> 30 m
    assert prov.erkennungsweite_m(0.15, hinterleuchtet=True) == 30.0
    assert prov.erkennungsweite_m(0.15, hinterleuchtet=False) == 15.0
