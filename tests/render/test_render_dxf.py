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
    assert summary["layer"] == "din_SIBEL_10_emergency_lighting"
    assert Path(summary["output_path"]).is_file()


def test_ohne_lb_keine_legende(rendered):
    _, summary, doc = rendered
    assert summary["lb_legende_drawn"] is False
    assert not doc.modelspace().query("MTEXT[layer=='din_SIBEL_70_legend_white']")


def test_stueckliste_zaehlt_symbol_arten(rendered):
    _, summary, doc = rendered
    assert summary["stueckliste_drawn"] is True
    sl = doc.modelspace().query("MTEXT[layer=='din_SIBEL_70_legend_green']")
    assert len(sl) == 1
    txt = sl[0].text
    assert "STÜCKLISTE" in txt
    assert "Rettungszeichen: 5" in txt   # 4OG-Fixture = 5 RZ
    assert "Summe: 5" in txt


def test_stromkreis_belegung_je_kreis(rendered):
    _, summary, doc = rendered
    # 4OG-Fixture = 5 RZ auf 2 Kreisen (AGV-A-F13 ×2, AGV-B-F13 ×3), alle DL.
    assert summary["stromkreis_belegung_drawn"] is True
    box = doc.modelspace().query("MTEXT[layer=='din_SIBEL_11_system']")
    assert len(box) == 1
    txt = box[0].text
    assert "STROMKREIS-BELEGUNG" in txt
    # Kompakte Übersicht: je Kreis Anzahl je Art + Schaltungsart + Gesamt (Σ).
    assert "AGV-A-F13: 2× RZ (DL) — Σ2" in txt
    assert "AGV-B-F13: 3× RZ (DL) — Σ3" in txt


def test_belegung_bleibt_kompakt_bei_vielen_leuchten():
    # Regression: die Belegungsliste listete früher JEDE Leuchten-ID pro Kreis → auf
    # realen Plänen 200+-Zeichen-Zeilen, die die feste Info-Box überliefen. Jetzt eine
    # kompakte Zeile je Kreis (Anzahl je Art), unabhängig von der Leuchtenzahl.
    from notbeleuchtung.hauptengine.contracts import Platzierung, PlatzierungsErgebnis
    from notbeleuchtung.hauptengine.render.dxf_renderer import _stromkreis_belegung_text

    plz = [
        Platzierung(xy_mm=(float(i), 0.0), catalog_key="notlicht_ks_stiege", kind="rz",
                    circuit_hint="AGV-A-F13")
        for i in range(15)
    ] + [
        Platzierung(xy_mm=(float(i), 10.0), catalog_key="sicherheitsleuchte_aufheller",
                    kind="sicherheitsleuchte", circuit_hint="AGV-A-F13")
        for i in range(20)
    ]
    txt = _stromkreis_belegung_text(PlatzierungsErgebnis(floor="EG", platzierungen=plz))
    zeilen = txt.split("\\P")
    # 1 Kopfzeile + 1 Zeile für den einen Kreis (nicht 35 IDs), jede Zeile kurz.
    assert len(zeilen) == 2
    assert "AGV-A-F13: 15× RZ (DL) · 20× SL (BL) — Σ35" in zeilen[1]
    assert all(len(z) < 80 for z in zeilen)


def test_schaltungsart_rz_ist_dauerlicht():
    from notbeleuchtung.hauptengine.render.dxf_renderer import _SCHALTUNGSART
    assert _SCHALTUNGSART["rz"] == "DL"                # Dauerlicht (maintained)
    assert _SCHALTUNGSART["sicherheitsleuchte"] == "BL"  # Bereitschaftslicht
    assert _SCHALTUNGSART["antipanik"] == "BL"


def test_hoehenkote_text_komma_notation():
    from notbeleuchtung.hauptengine.render.dxf_renderer import _hoehenkote_text
    assert _hoehenkote_text(2400.0) == "h=2,40"
    assert _hoehenkote_text(2000.0) == "h=2,00"
    assert _hoehenkote_text(3000.0) == "h=3,00"
    assert _hoehenkote_text(2250.0) == "h=2,25"


def test_hoehenkoten_label_gezeichnet(rendered):
    _, summary, doc = rendered
    # 4OG-Fixture = 5 Symbole, alle mit Default-Montagehöhe 2400 mm.
    assert summary["hoehenkoten_drawn"] == 5
    koten = doc.modelspace().query("MTEXT[layer=='din_SIBEL_52_info']")
    assert len(koten) == 5
    assert all(k.text == "h=2,40" for k in koten)


def test_nodeid_annotation_je_leuchte(rendered):
    _, summary, doc = rendered
    # 4OG-Fixture = 5 RZ → NODEID RZ-001..RZ-005, je Symbol genau ein MTEXT.
    # Zweite Zeile = Stromkreisnummer Anlage/Kreis/Adresse (Profi-Plan LABELING1).
    assert summary["nodeids_drawn"] == 5
    ids = doc.modelspace().query("MTEXT[layer=='din_SIBEL_63_luminaire_ID']")
    assert len(ids) == 5
    zeilen = [m.text.split("\\P") for m in ids]
    assert sorted(z[0] for z in zeilen) == ["RZ-001", "RZ-002", "RZ-003", "RZ-004", "RZ-005"]
    # 2 Kreise (AGV-A-F13 ×2 → Anlage 1, AGV-B-F13 ×3 → Anlage 2), je Kreis 1.
    assert summary["stromkreisnummern_drawn"] == 5
    assert sorted(z[1] for z in zeilen) == ["1/1/1", "1/1/2", "2/1/1", "2/1/2", "2/1/3"]


def _p_sk(kind: str, hint: str):
    from notbeleuchtung.hauptengine.contracts import Platzierung
    key = "notlicht_ks_stiege" if kind == "rz" else "sicherheitsleuchte_aufheller"
    return Platzierung(xy_mm=(0.0, 0.0), catalog_key=key, kind=kind, circuit_hint=hint)


def test_stromkreisnummern_dl_bl_getrennte_kreise():
    # circuit_zuordnung-Hints: DL und BL sind getrennte Kreise derselben Anlage.
    from notbeleuchtung.hauptengine.render.dxf_renderer import _stromkreisnummern
    plz = PlatzierungsErgebnis(floor="EG", platzierungen=[
        _p_sk("rz", "AGV-A-F13-DL-1"),
        _p_sk("sicherheitsleuchte", "AGV-A-F13-BL-1"),
        _p_sk("rz", "AGV-A-F13-DL-1"),
    ])
    assert _stromkreisnummern(plz) == ["1/1/1", "1/2/1", "1/1/2"]


def test_stromkreisnummern_cap_rollover_wird_neuer_kreis():
    # Deckel in circuit_zuordnung (20/Kreis) → -DL-2-Hint = eigener Kreis.
    from notbeleuchtung.hauptengine.render.dxf_renderer import _stromkreisnummern
    plz = PlatzierungsErgebnis(floor="EG", platzierungen=[
        _p_sk("rz", "AGV-A-F13-DL-1"),
        _p_sk("rz", "AGV-A-F13-DL-2"),
        _p_sk("rz", "AGV-A-F13-DL-2"),
    ])
    assert _stromkreisnummern(plz) == ["1/1/1", "1/2/1", "1/2/2"]


def test_stromkreisnummern_gebaeude_b_ist_anlage_2_und_ohne_hint_leer():
    from notbeleuchtung.hauptengine.render.dxf_renderer import _stromkreisnummern
    plz = PlatzierungsErgebnis(floor="EG", platzierungen=[
        _p_sk("rz", "AGV-B-F13-DL-1"),
        _p_sk("rz", ""),
        _p_sk("rz", "kein-agv-format"),
    ])
    # Gebäude B → Anlage 2; unparsbarer Hint → Anlage 1; leerer Hint → kein Label.
    assert _stromkreisnummern(plz) == ["2/1/1", "", "1/1/1"]


def test_info_blocks_sind_gerahmte_boxen(rendered):
    # Schriftfeld-Leiste: Stückliste ist jetzt eine gerahmte Box (Rahmen + Text auf
    # demselben Layer), nicht mehr freier Text neben dem Grundriss.
    _, _, doc = rendered
    msp = doc.modelspace()
    assert msp.query("LWPOLYLINE[layer=='din_SIBEL_70_legend_green']")
    assert msp.query("MTEXT[layer=='din_SIBEL_70_legend_green']")


def test_plankopf_rahmen_und_felder(rendered):
    _, summary, doc = rendered
    assert summary["plankopf_drawn"] is True
    msp = doc.modelspace()
    # Rahmen (geschlossene LWPOLYLINE) + Text auf dem Plankopf-Layer.
    assert msp.query("LWPOLYLINE[layer=='din_SIBEL_99_titleblock']")
    kopf = msp.query("MTEXT[layer=='din_SIBEL_99_titleblock']")
    assert len(kopf) == 1
    txt = kopf[0].text
    assert "NOTBELEUCHTUNGSPLAN" in txt
    assert "Geschoss: 4OG" in txt
    assert "Maßstab: 1:100" in txt


def test_plankopf_metadaten_ueberschreiben(contracts, tmp_path):
    platzierung, raum = contracts
    out = tmp_path / "meta.dxf"
    render_dxf(platzierung, raum, out,
               plankopf={"projekt": "Wohnbau X", "datum": "2026-08-30", "ersteller": "Leonis"})
    doc = ezdxf.readfile(str(out))
    txt = doc.modelspace().query("MTEXT[layer=='din_SIBEL_99_titleblock']")[0].text
    assert "Projekt: Wohnbau X" in txt
    assert "Datum: 2026-08-30" in txt
    assert "Erstellt: Leonis" in txt


def test_pruefbericht_legende(contracts, tmp_path):
    platzierung, raum = contracts
    pruef = {"status": "warnung", "befunde": [
        {"regel": "Montagehöhe ≥ 2000 mm (EN 1838 §4.1)", "status": "ok", "detail": "alle Symbole ≥ 2000 mm"},
        {"regel": "Fluchtweg-Deckung durch Rettungszeichen", "status": "warnung", "detail": "1/5 Segment(e) ohne RZ"},
    ]}
    out = tmp_path / "pruef.dxf"
    summary = render_dxf(platzierung, raum, out, pruefung=pruef)
    assert summary["pruefbericht_drawn"] is True
    doc = ezdxf.readfile(str(out))
    pb = doc.modelspace().query("MTEXT[layer=='din_SIBEL_99_inspection']")
    assert len(pb) == 1
    txt = pb[0].text
    assert "PRÜFBERICHT (EN 1838): WARNUNG" in txt
    assert "[WARNUNG]" in txt and "Fluchtweg-Deckung" in txt


def test_ohne_pruefung_keine_pruefbericht_legende(rendered):
    _, summary, doc = rendered
    assert summary["pruefbericht_drawn"] is False
    assert not doc.modelspace().query("MTEXT[layer=='din_SIBEL_99_inspection']")


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
    legenden = doc.modelspace().query("MTEXT[layer=='din_SIBEL_70_legend_white']")
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
        assert ins.dxf.layer == "din_SIBEL_10_emergency_lighting"
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


def test_tueren_werden_gezeichnet(rendered):
    # Gap-Audit H-Gebäude: raum.tueren wurde vom Render ignoriert — Türen (Schwelle +
    # Blatt + Schwenkbogen) müssen auf ARCH_Tuer erscheinen; Notausgänge doppelt.
    contracts_pl, summary, doc = rendered
    n_tueren = summary["tueren_drawn"]
    assert n_tueren >= 1
    linien = doc.modelspace().query("LINE[layer=='ARCH_Tuer']")
    boegen = doc.modelspace().query("ARC[layer=='ARCH_Tuer']")
    assert len(boegen) == n_tueren          # 1 Schwenkbogen je Tür
    assert len(linien) >= 2 * n_tueren      # Schwelle + Blatt (+ Notausgang-Doppel)
