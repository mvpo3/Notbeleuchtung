"""inserter.py gegen die Golden-Fixture: INSERT-Attribute, XOR-Mirror, XDATA."""
from __future__ import annotations

import json
from pathlib import Path

import ezdxf
import pytest

from notbeleuchtung.hauptengine.contracts import Platzierung, PlatzierungsErgebnis
from notbeleuchtung.symbols import inserter, library

FIXTURES = Path(__file__).parent.parent / "fixtures"


@pytest.fixture(autouse=True)
def _fresh_cache():
    library.reset_cache()
    yield
    library.reset_cache()


@pytest.fixture()
def ergebnis() -> PlatzierungsErgebnis:
    raw = json.loads((FIXTURES / "platzierung_4og.json").read_text(encoding="utf-8"))
    return PlatzierungsErgebnis.model_validate(raw)


def test_insert_fixture_platzierungen(ergebnis):
    doc = ezdxf.new("R2018")
    mapping = library.load_mapping()
    for p in ergebnis.platzierungen:
        ins = inserter.insert_platzierung(doc, p)
        assert ins.dxf.layer == library.SAFETY_LAYER
        assert ins.dxf.name == mapping[p.catalog_key]["block_name"]
        assert ins.dxf.insert.x == pytest.approx(p.xy_mm[0])
        assert ins.dxf.insert.y == pytest.approx(p.xy_mm[1])
        assert ins.dxf.rotation == pytest.approx(p.rotation_deg)
        # Fixture-Keys ohne Mapping-mirror_x → effektive Spiegelung = Contract
        assert (ins.dxf.xscale < 0) == p.mirror_x
        assert ins.dxf.yscale == pytest.approx(inserter.DE_GLOBAL_SCALE)
    inserts = doc.modelspace().query("INSERT")
    assert len(inserts) == 5


def test_xor_mirror_mapping_entry():
    # notlicht_ks_stiege_rechts trägt mirror_x im MAPPING; Contract-mirror_x
    # obendrauf hebt die Spiegelung wieder auf (XOR).
    doc = ezdxf.new("R2018")
    base = {"xy_mm": (0.0, 0.0), "catalog_key": "notlicht_ks_stiege_rechts", "kind": "rz"}
    nur_mapping = inserter.insert_platzierung(doc, Platzierung(**base))
    assert nur_mapping.dxf.xscale < 0
    beide = inserter.insert_platzierung(doc, Platzierung(**base, mirror_x=True))
    assert beide.dxf.xscale > 0


def test_circuit_hint_als_xdata(ergebnis):
    doc = ezdxf.new("R2018")
    p = ergebnis.platzierungen[0]
    ins = inserter.insert_platzierung(doc, p)
    xdata = ins.get_xdata("NOTBELEUCHTUNG")
    assert (1000, f"stromkreis={p.circuit_hint}") in [(c, v) for c, v in xdata]


def test_unbekannter_catalog_key_raises():
    doc = ezdxf.new("R2018")
    p = Platzierung(xy_mm=(0.0, 0.0), catalog_key="gibt_es_nicht", kind="rz")
    with pytest.raises(KeyError):
        inserter.insert_platzierung(doc, p)
