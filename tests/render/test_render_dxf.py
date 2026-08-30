"""Golden-Fixture-Readback: render_dxf → ezdxf.readfile → Struktur-Asserts."""
from __future__ import annotations

import json
from pathlib import Path

import ezdxf
import pytest

from notbeleuchtung.hauptengine.contracts import PlatzierungsErgebnis, RaumModell
from notbeleuchtung.hauptengine.render import render_dxf
from notbeleuchtung.symbols import library

FIXTURES = Path(__file__).parent.parent / "fixtures"


@pytest.fixture(autouse=True)
def _fresh_cache():
    library.reset_cache()
    yield
    library.reset_cache()


@pytest.fixture()
def contracts() -> tuple[PlatzierungsErgebnis, RaumModell]:
    platzierung = PlatzierungsErgebnis.model_validate(
        json.loads((FIXTURES / "platzierung_4og.json").read_text(encoding="utf-8"))
    )
    raum = RaumModell.model_validate(
        json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    )
    return platzierung, raum


@pytest.fixture()
def rendered(contracts, tmp_path):
    platzierung, raum = contracts
    out = tmp_path / "4og_notbeleuchtung.dxf"
    summary = render_dxf(platzierung, raum, out)
    return platzierung, summary, ezdxf.readfile(str(out))


def test_summary_superset_und_rendered_true(rendered):
    _, summary, _ = rendered
    assert summary["rendered"] is True
    assert summary["floor"] == "4OG"
    assert summary["n_symbols"] == 5
    assert summary["by_kind"] == {"rz": 5}
    assert summary["n_raeume"] == 2
    assert summary["layer"] == "E_Sicherheitsbeleuchtung"
    assert Path(summary["output_path"]).is_file()


def test_ohne_lb_keine_legende(rendered):
    _, summary, doc = rendered
    assert summary["lb_legende_drawn"] is False
    assert not doc.modelspace().query("MTEXT[layer=='E_Notbeleuchtung_Legende']")


def test_stueckliste_zaehlt_symbol_arten(rendered):
    _, summary, doc = rendered
    assert summary["stueckliste_drawn"] is True
    sl = doc.modelspace().query("MTEXT[layer=='E_Notbeleuchtung_Stueckliste']")
    assert len(sl) == 1
    txt = sl[0].text
    assert "STÜCKLISTE" in txt
    assert "Rettungszeichen: 5" in txt   # 4OG-Fixture = 5 RZ
    assert "Summe: 5" in txt


def test_lb_legende_traegt_system_spec(contracts, tmp_path):
    from notbeleuchtung.hauptengine.contracts import LBVorgabe
    platzierung, raum = contracts
    lb = LBVorgabe(
        system_typ="gruppenbatterie", betriebsdauer_min=480, umschaltzeit_max_s=0.5,
        mindest_lux_fluchtweg=1.0, norm_bezug=["EN 1838", "OVE R 12-2"],
        lb_quelle="LB Fischa §2.11",
    )
    out = tmp_path / "mit_lb.dxf"
    summary = render_dxf(platzierung, raum, out, lb)
    assert summary["lb_legende_drawn"] is True
    doc = ezdxf.readfile(str(out))
    legenden = doc.modelspace().query("MTEXT[layer=='E_Notbeleuchtung_Legende']")
    assert len(legenden) == 1
    txt = legenden[0].text
    assert "Gruppenbatterie" in txt
    assert "8 h" in txt                 # 480 min → 8 h
    assert "EN 1838" in txt


def test_fuenf_inserts_auf_sicherheitslayer(rendered):
    platzierung, _, doc = rendered
    inserts = doc.modelspace().query("INSERT")
    assert len(inserts) == 5
    mapping = library.load_mapping()
    expected_blocks = {mapping[p.catalog_key]["block_name"] for p in platzierung.platzierungen}
    for ins in inserts:
        assert ins.dxf.layer == "E_Sicherheitsbeleuchtung"
        assert ins.dxf.name in expected_blocks


def test_positionen_und_mirror_matchen_fixture(rendered):
    platzierung, _, doc = rendered
    inserts = list(doc.modelspace().query("INSERT"))
    by_pos = {(round(i.dxf.insert.x, 1), round(i.dxf.insert.y, 1)): i for i in inserts}
    for p in platzierung.platzierungen:
        key = (round(p.xy_mm[0], 1), round(p.xy_mm[1], 1))
        assert key in by_pos, f"INSERT an {p.xy_mm} fehlt"
        ins = by_pos[key]
        assert ins.dxf.rotation == pytest.approx(p.rotation_deg)
        assert (ins.dxf.xscale < 0) == p.mirror_x  # Fixture-Keys ohne Mapping-mirror
    # RZ nutzen seit dem Richtungs-Fix dedizierte links/rechts-Blöcke (rotation 0,
    # keine Spiegelung) → kein negativer xscale mehr.
    n_mirrored = sum(1 for i in inserts if i.dxf.xscale < 0)
    assert n_mirrored == 0


def test_f13_stromkreis_labels_sichtbar(rendered):
    _, summary, doc = rendered
    texts = {mt.text for mt in doc.modelspace().query("MTEXT")}
    assert any("AGV-A-F13" in t for t in texts)
    assert any("AGV-B-F13" in t for t in texts)
    assert summary["circuit_labels_drawn"] == 5


def test_raum_konturen_und_segmente(rendered):
    _, summary, doc = rendered
    msp = doc.modelspace()
    konturen = [e for e in msp.query("LWPOLYLINE") if e.dxf.layer == "ARCH_Raum"]
    assert len(konturen) >= 2
    assert all(k.closed for k in konturen)
    segmente = [e for e in msp.query("LWPOLYLINE") if e.dxf.layer == "ARCH_Fluchtweg"]
    assert len(segmente) == summary["fluchtweg_segmente_drawn"] >= 1


def test_xdata_stromkreis_am_insert(rendered):
    _, _, doc = rendered
    inserts = doc.modelspace().query("INSERT")
    tagged = 0
    for ins in inserts:
        try:
            xdata = ins.get_xdata("NOTBELEUCHTUNG")
        except ezdxf.lldxf.const.DXFValueError:
            continue
        if any(str(v).startswith("stromkreis=") for _, v in xdata):
            tagged += 1
    assert tagged == 5
