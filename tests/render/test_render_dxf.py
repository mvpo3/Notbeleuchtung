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
def ohne_blatt(monkeypatch):
    """Blatt-Vorlage deaktivieren → Fallback-Pfad (Schriftfeld-Boxen) testbar."""
    from notbeleuchtung.hauptengine.render import dxf_renderer as dr
    monkeypatch.setitem(dr._blatt_vorlage_cache, "doc", None)
    yield
    dr._blatt_vorlage_cache.clear()


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
def rendered(contracts, tmp_path, ohne_blatt):
    # Box-/Legacy-Pfad (Blatt-Vorlage aus): die meisten Struktur-Tests prüfen die
    # Schriftfeld-Boxen; der Blatt-Modus hat eigene Tests (test_blatt_modus_*).
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
    # Owner-Vorlage aktiv: die Symbol-Legende wird in `Vorlage_Legende` GEFÜLLT
    # (Sektion „Legende Notbeleuchtung"), die separate Stücklisten-Box entfällt.
    _, summary, doc = rendered
    assert summary["vorlage_drawn"] is True
    assert summary["vorlage_legende_gefuellt"] is True
    assert summary["stueckliste_drawn"] is False
    texte = " ".join(m.text for m in
                     doc.modelspace().query("MTEXT[layer=='din_SIBEL_70_legend_green']"))
    assert "5x Typ RZ" in texte and "Rettungszeichen" in texte


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
    # Schriftfeld-Leiste: Belegungs-Box bleibt gerahmt (Rahmen + Text auf demselben
    # Layer); die Stückliste lebt jetzt in der Owner-Vorlage.
    _, _, doc = rendered
    msp = doc.modelspace()
    assert msp.query("LWPOLYLINE[layer=='din_SIBEL_11_system']")
    assert msp.query("MTEXT[layer=='din_SIBEL_11_system']")


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


def test_plankopf_metadaten_ueberschreiben(contracts, tmp_path, ohne_blatt):
    platzierung, raum = contracts
    out = tmp_path / "meta.dxf"
    render_dxf(platzierung, raum, out,
               plankopf={"projekt": "Wohnbau X", "datum": "2026-08-30", "ersteller": "Leonis"})
    doc = ezdxf.readfile(str(out))
    txt = doc.modelspace().query("MTEXT[layer=='din_SIBEL_99_titleblock']")[0].text
    assert "Projekt: Wohnbau X" in txt
    assert "Datum: 2026-08-30" in txt
    assert "Erstellt: Leonis" in txt


def test_pruefbericht_legende(contracts, tmp_path, ohne_blatt):
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


def test_lb_legende_traegt_system_spec(contracts, tmp_path, ohne_blatt):
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
    # Plan-Symbole tragen Stromkreis-XDATA — Blatt-/Vorlagen-Deko nicht.
    inserts = [e for e in doc.modelspace().query("INSERT")
               if e.has_xdata("NOTBELEUCHTUNG")]
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


def test_keine_agv_labels_am_symbol(rendered):
    # Owner-Entscheidung 2026-09-05: AGV-Stromkreis-Label je Symbol ist unnötig —
    # die Kreis-Info tragen Anlage/Kreis/Adresse (NODEID-Zweitzeile) + Belegungsliste.
    _, _summary, doc = rendered
    assert "din_SIBEL_61_labeling" not in doc.layers
    belegung = doc.modelspace().query("MTEXT[layer=='din_SIBEL_11_system']")
    assert belegung and "AGV-A-F13" in belegung[0].text  # Info lebt in der Liste weiter


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
    _, summary, doc = rendered
    n_tueren = summary["tueren_drawn"]
    assert n_tueren >= 1
    linien = doc.modelspace().query("LINE[layer=='ARCH_Tuer']")
    boegen = doc.modelspace().query("ARC[layer=='ARCH_Tuer']")
    assert len(boegen) == n_tueren          # 1 Schwenkbogen je Tür
    assert len(linien) >= 2 * n_tueren      # Schwelle + Blatt (+ Notausgang-Doppel)


def test_stueckliste_mit_symbol_spalte(ohne_blatt):
    # Profi-Legende (din ACAD_TABLE): je Typ-Zeile das echte Katalog-Symbol klein
    # in der Stücklisten-Box (nur im Typ-Letter-Pfad, Symbol-Datenmodell v1.2.0).
    from notbeleuchtung.hauptengine.contracts import Platzierung, PlatzierungsErgebnis, RaumModell

    raum = RaumModell.model_validate(
        json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8")))
    plz = PlatzierungsErgebnis(floor="4OG", platzierungen=[
        Platzierung(xy_mm=(-70000.0, 20000.0), catalog_key="notlicht_ks_stiege_unten",
                    kind="rz", typ_letter="A", typ_name="Concept 2 RZ1"),
        Platzierung(xy_mm=(-60000.0, 20000.0), catalog_key="sicherheitsleuchte_aufheller",
                    kind="sicherheitsleuchte", typ_letter="D", typ_name="Concept 2 AP3"),
    ])
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "legende.dxf"
        summary = render_dxf(plz, raum, out)
        doc = ezdxf.readfile(str(out))
    # Symbol-Legende lebt jetzt IN der Owner-Vorlage (Stücklisten-Box entfällt).
    assert summary["vorlage_legende_gefuellt"] is True
    assert summary["stueckliste_drawn"] is False
    max_x = raum.bounds_mm.max_xy[0]
    legenden_syms = [e for e in doc.modelspace().query("INSERT")
                     if e.dxf.insert.x > max_x + 1500
                     and e.dxf.name != "vorlage_legende"
                     and not e.has_xdata("NOTBELEUCHTUNG")]
    assert len(legenden_syms) >= 2   # Vorlagen- + Blatt-Legende bestücken beide
    texte = " ".join(m.text for m in doc.modelspace().query("MTEXT"))
    assert "Typ A" in texte and "Typ D" in texte and "Concept 2 AP3" in texte


def test_anlagen_symbol_nur_bei_lb_system_typ(ohne_blatt):
    # LB-explizit: Gruppenbatterie-Symbol erscheint NUR wenn die LB einen system_typ
    # deklariert UND ein Technik-/Batterieraum erkannt ist (kein geratener Standort).
    import tempfile

    from notbeleuchtung.hauptengine.contracts import (
        LBVorgabe,
        Platzierung,
        PlatzierungsErgebnis,
        Raum,
        RaumModell,
    )

    raum = RaumModell.model_validate(
        json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8")))
    raum.raeume.append(Raum(
        id="technik", raum_typ="TECHNIK",
        polygon_mm=[(-50000.0, 5000.0), (-45000.0, 5000.0),
                    (-45000.0, 10000.0), (-50000.0, 10000.0)],
    ))
    plz = PlatzierungsErgebnis(floor="4OG", platzierungen=[
        Platzierung(xy_mm=(-70000.0, 20000.0), catalog_key="notlicht_ks_stiege", kind="rz")])
    lb = LBVorgabe(system_typ="gruppenbatterie", batterie_standort="UG Zählerraum",
                   lb_quelle="Test")
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "a.dxf"
        mit = render_dxf(plz, raum, out, lb)
        doc = ezdxf.readfile(str(out))
        ohne = render_dxf(plz, raum, Path(tmp) / "b.dxf", None)
    assert mit["anlage_drawn"] is True and ohne["anlage_drawn"] is False
    # Die ANLAGE steht im Technikraum (−50000..−45000) — Blatt-Legende liegt außerhalb.
    syms = [e for e in doc.modelspace().query("INSERT")
            if e.dxf.name == "gruppenbatterie" and -51000 < e.dxf.insert.x < -44000]
    assert len(syms) == 1
    texte = " ".join(m.text for m in doc.modelspace().query("MTEXT"))
    assert "SV-Anlage 1" in texte and "UG Zählerraum" in texte



def test_blatt_modus_ersetzt_alle_boxen(contracts, tmp_path):
    # Owner-Fixierung (wohnbau_v7_dg_verbessert.dxf): mit Blatt-Vorlage trägt das
    # Blatt ALLES — keine Schriftfeld-Boxen, kein Legenden-Anhang daneben.
    platzierung, raum = contracts
    out = tmp_path / "blatt.dxf"
    summary = render_dxf(platzierung, raum, out, pruefung={"status": "ok", "befunde": []})
    doc = ezdxf.readfile(str(out))
    assert summary["blatt_layout_drawn"] is True
    assert summary["pruefbericht_drawn"] is False
    assert summary["stromkreis_belegung_drawn"] is False
    assert summary["stueckliste_drawn"] is False
    msp = doc.modelspace()
    assert not msp.query("LWPOLYLINE[layer=='din_SIBEL_99_inspection']")
    assert not msp.query("LWPOLYLINE[layer=='din_SIBEL_11_system']")
    assert not [e for e in msp.query("INSERT") if e.dxf.name == "vorlage_legende"]
    # Blatt-Rahmen + gefüllte Blatt-Legende existieren
    assert msp.query("LWPOLYLINE[layer=='din_SIBEL_99_titleblock']")
    blatt_syms = [e for e in msp.query("INSERT") if not e.has_xdata("NOTBELEUCHTUNG")]
    assert len(blatt_syms) >= 5   # Legenden-Symbole der Blatt-Spalte
