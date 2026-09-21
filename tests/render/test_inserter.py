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
        # Migration Phase A: Skala je Registry-Eintrag (scale_abs, kalibriert an
        # den Owner-Erklärungsplänen) statt globalem DE-Faktor.
        entry = mapping[p.catalog_key]
        erwartet = float(entry.get(
            "scale_abs", inserter.DE_GLOBAL_SCALE * float(entry.get("scale", 1.0))))
        assert ins.dxf.yscale == pytest.approx(erwartet)
    inserts = doc.modelspace().query("INSERT")
    assert len(inserts) == 5


def test_xor_mirror_mapping_entry(monkeypatch):
    # Mapping-Level mirror_x XOR Contract-mirror_x. Synthetischer Eintrag, damit
    # der Test nicht davon abhängt, ob gerade ein kuratiertes Symbol mirror_x nutzt
    # (die Pfeil-Blöcke sind seit dem Rechts-Fix alle unge­spiegelt gemappt).
    fake = dict(library.load_mapping())
    fake["_mirror_probe"] = {
        "block_name": "RIVO_ARR_down",
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


def test_gerade_zeichnet_echten_beidseitig_block():
    # richtung="gerade" (beidseitiger RZ, Wasserscheide) → EIN echter
    # Rivoplan-Beidseitig-Block am Punkt, rotiert um die Fluchtweg-Achse
    # (Rivoplan-Master 2026-09-20; ersetzt die links+rechts-Komposition).
    doc = ezdxf.new("R2018")
    mapping = library.load_mapping()
    p = Platzierung(
        xy_mm=(1000.0, 2000.0), catalog_key="notlicht_ks_stiege", kind="rz",
        richtung="gerade", rotation_deg=90.0,
    )
    primary = inserter.insert_platzierung(doc, p)

    inserts = doc.modelspace().query("INSERT")
    assert len(inserts) == 1
    assert primary.dxf.name == mapping["notlicht_ks_beidseitig"]["block_name"]
    assert primary.dxf.insert.x == pytest.approx(1000.0)
    assert primary.dxf.insert.y == pytest.approx(2000.0)
    assert primary.dxf.rotation == pytest.approx(90.0)
    assert primary.dxf.layer == library.SAFETY_LAYER
    assert primary.dxf.yscale == pytest.approx(
        float(mapping["notlicht_ks_beidseitig"]["scale_abs"]))


def test_gerade_xdata_am_beidseitig_block():
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
def test_gerade_nur_bei_rz_beidseitig(catalog_key, kind):
    # Sicherheitsleuchte + Antipanik tragen ebenfalls richtung="gerade" (= keine
    # Richtung), sind aber KEINE Pfeil-Zeichen → EIN eigenes Katalog-Symbol, nicht
    # der RZ-Beidseitig-Block (Regression: Beidseitig-Gate darf nur für kind=="rz").
    doc = ezdxf.new("R2018")
    mapping = library.load_mapping()
    p = Platzierung(xy_mm=(0.0, 0.0), catalog_key=catalog_key, kind=kind, richtung="gerade")
    ins = inserter.insert_platzierung(doc, p)

    inserts = doc.modelspace().query("INSERT")
    assert len(inserts) == 1
    assert ins.dxf.name == mapping[catalog_key]["block_name"]


def test_sl_aufheller_farbe_wie_owner_symbol():
    """Bibliotheks-Update 2026-09-21 („Erscheinungsbild ist Wahrheit"): der
    RIVO_Aufheller der neuen Owner-Bibliothek RIVO_NL_Symbole.dxf ist ein Kreis
    mit grünem Rand (CIRCLE ACI 3) und BYLAYER-Füllung (SOLID-HATCH ACI 256) —
    auf dem Notlicht-Layer rendert er grün. Owner-Entscheid 2026-09-21: „grün ist
    ok" (der frühere Blau-Aufheller ACI 150 ist Geschichte). Die Library-Farben
    werden beim Import NICHT umgeschrieben — der Block trägt seine Farbe selbst."""
    doc = ezdxf.new("R2018")
    library.sync_layers(doc)
    p = Platzierung(xy_mm=(0.0, 0.0), catalog_key="sicherheitsleuchte_aufheller",
                    kind="sicherheitsleuchte")
    ins = inserter.insert_platzierung(doc, p)

    def entities(name):
        for e in doc.blocks[name]:
            yield e
            if e.dxftype() == "INSERT":
                yield from entities(e.dxf.name)

    alle = list(entities(ins.dxf.name))
    farben = {e.dxftype(): e.dxf.color for e in alle}
    assert farben["HATCH"] == 256   # BYLAYER-Füllung → Notlicht-Layer (grün)
    assert farben["CIRCLE"] == 3    # grüner Rand (Owner-Symbol)
