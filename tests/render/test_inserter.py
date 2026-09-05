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


def test_xor_mirror_mapping_entry(monkeypatch):
    # Mapping-Level mirror_x XOR Contract-mirror_x. Synthetischer Eintrag, damit
    # der Test nicht davon abhängt, ob gerade ein kuratiertes Symbol mirror_x nutzt
    # (die Pfeil-Blöcke sind seit dem Rechts-Fix alle unge­spiegelt gemappt).
    fake = dict(library.load_mapping())
    fake["_mirror_probe"] = {
        "block_name": "notbeleuchtung- richtungspfeil nach unten",
        "label": "probe",
        "category": "notlicht",
        "mirror_x": True,
    }
    monkeypatch.setattr(library, "load_mapping", lambda: fake)
    doc = ezdxf.new("R2018")
    base = {"xy_mm": (0.0, 0.0), "catalog_key": "_mirror_probe", "kind": "rz"}
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


def test_gerade_zeichnet_beidseitigen_doppelpfeil():
    # richtung="gerade" (beidseitiger RZ, Wasserscheide) → zwei horizontale Pfeile
    # (links + rechts) am selben Punkt, gemeinsam rotiert. Zurück kommt der linke.
    doc = ezdxf.new("R2018")
    mapping = library.load_mapping()
    p = Platzierung(
        xy_mm=(1000.0, 2000.0), catalog_key="notlicht_ks_stiege", kind="rz",
        richtung="gerade", rotation_deg=90.0,
    )
    primary = inserter.insert_platzierung(doc, p)

    inserts = doc.modelspace().query("INSERT")
    assert len(inserts) == 2
    namen = {ins.dxf.name for ins in inserts}
    assert namen == {
        mapping["notlicht_ks_stiege_links"]["block_name"],
        mapping["notlicht_ks_stiege_rechts"]["block_name"],
    }
    # beide teilen Punkt + Rotation (Fluchtweg-Achse)
    for ins in inserts:
        assert ins.dxf.insert.x == pytest.approx(1000.0)
        assert ins.dxf.insert.y == pytest.approx(2000.0)
        assert ins.dxf.rotation == pytest.approx(90.0)
        assert ins.dxf.layer == library.SAFETY_LAYER
    # primärer (zurückgegebener) Insert = linker Pfeil
    assert primary.dxf.name == mapping["notlicht_ks_stiege_links"]["block_name"]


def test_gerade_xdata_nur_auf_primaerem_pfeil():
    doc = ezdxf.new("R2018")
    p = Platzierung(
        xy_mm=(0.0, 0.0), catalog_key="notlicht_ks_stiege", kind="rz",
        richtung="gerade", circuit_hint="AGV-A-F13",
    )
    primary = inserter.insert_platzierung(doc, p)
    # genau ein Insert trägt den Stromkreis-XDATA-Tag
    getaggt = [
        ins for ins in doc.modelspace().query("INSERT")
        if ins.has_xdata("NOTBELEUCHTUNG")
    ]
    assert len(getaggt) == 1
    assert getaggt[0] is primary
    xdata = primary.get_xdata("NOTBELEUCHTUNG")
    assert (1000, "stromkreis=AGV-A-F13") in [(c, v) for c, v in xdata]


@pytest.mark.parametrize(
    "catalog_key,kind",
    [("sicherheitsleuchte_aufheller", "sicherheitsleuchte"), ("antipanik_leuchte", "antipanik")],
)
def test_gerade_nur_bei_rz_doppelpfeil(catalog_key, kind):
    # Sicherheitsleuchte + Antipanik tragen ebenfalls richtung="gerade" (= keine
    # Richtung), sind aber KEINE Pfeil-Zeichen → EIN eigenes Katalog-Symbol, nicht
    # zwei RZ-Richtungspfeile (Regression: Doppelpfeil-Gate darf nur für kind=="rz").
    doc = ezdxf.new("R2018")
    mapping = library.load_mapping()
    p = Platzierung(xy_mm=(0.0, 0.0), catalog_key=catalog_key, kind=kind, richtung="gerade")
    ins = inserter.insert_platzierung(doc, p)

    inserts = doc.modelspace().query("INSERT")
    assert len(inserts) == 1
    assert ins.dxf.name == mapping[catalog_key]["block_name"]


def test_sl_aufheller_kein_hardcode_blau():
    # Der Lib-Block trägt einen SOLID-HATCH mit expliziter Farbe ACI 150 (blau),
    # die den Layer-Grün-Override übergeht — Notlicht muss grün rendern. Import
    # stellt blaue Hardcode-Farben auf BYLAYER (erbt Schrack-Grün des INSERT-Layers).
    doc = ezdxf.new("R2018")
    library.sync_layers(doc)
    p = Platzierung(xy_mm=(0.0, 0.0), catalog_key="sicherheitsleuchte_aufheller",
                    kind="sicherheitsleuchte")
    ins = inserter.insert_platzierung(doc, p)

    # Rekursiv über den Block-Baum (der kleine Aufheller verschachtelt den alten
    # Kreis-Block @ Scale 0.394): nirgends darf eine blaue Hardcode-Farbe bleiben.
    def entities(name):
        for e in doc.blocks[name]:
            yield e
            if e.dxftype() == "INSERT":
                yield from entities(e.dxf.name)

    alle = list(entities(ins.dxf.name))
    farben = {e.dxftype(): e.dxf.color for e in alle}
    assert farben["HATCH"] == 256  # BYLAYER statt ACI 150
    assert not any(getattr(e.dxf, "color", None) in library._BLAUE_ACI for e in alle)
