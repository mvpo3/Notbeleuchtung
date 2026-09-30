"""raumerkennung_darstellung — Außen-Überlagerungs-Kennzahl und Versionsordner-Sperre."""
import json
import sys
from pathlib import Path

from shapely.geometry import box

sys.path.insert(0, str(Path(__file__).parents[2] / "scripts" / "analyse"))
import raumerkennung_darstellung as rd


def _raum(rid, typ, x0, y0, x1, y1):
    return {"id": rid, "typ": typ, "polygon_mm": list(box(x0, y0, x1, y1).exterior.coords)[:-1],
            "flaeche_m2": (x1 - x0) * (y1 - y0) / 1e6}


def test_aussen_ueberlagerung_nur_kanon_raeume_ueber_schwelle():
    # Außen offen: x 0..10 m, y 3..4 m; Innenhof: x 20..30 m, y 0..10 m (mm).
    cache = {
        "raeume": [
            _raum("zimmer", "ZIMMER", 0, 0, 4000, 4000),         # offen 4 m² → zählt
            _raum("gang", "GANG", 19500, 0, 21000, 1000),        # Innenhof 1 m² → zählt
            _raum("terrasse", "TERRASSE", 5000, 0, 9000, 4000),  # AUSSEN → zählt nicht
            _raum("unbek", "", 9800, 3000, 10000, 4000),         # UNBEKANNT → zählt nicht
            _raum("bad", "BAD", 9800, 3800, 10000, 5000),        # 0,2×0,2 = 0,04 m² → nicht
        ],
        "aussen_offen": [box(0, 3000, 10000, 4000).wkb],
        "aussen_geschlossen": [box(20000, 0, 30000, 10000).wkb],
    }
    polys = {r["id"]: rd._polygon(r["polygon_mm"]) for r in cache["raeume"]}
    liste = rd._aussen_kanon(cache, polys)
    assert [e["id"] for e in liste] == ["zimmer", "gang"]
    assert liste[0] == {"id": "zimmer", "typ": "ZIMMER", "flaeche_m2": 16.0,
                        "schnitt_offen_m2": 4.0, "schnitt_geschlossen_m2": 0.0}
    assert liste[1]["schnitt_offen_m2"] == 0.0 and liste[1]["schnitt_geschlossen_m2"] == 1.0


def _eingang(tmp_path):
    (tmp_path / "eingang" / "Rennweg").mkdir(parents=True)
    (tmp_path / "eingang" / "Rennweg" / "UG.dxf").write_text("0\nEOF\n", encoding="utf-8")
    return ["--eingang", str(tmp_path / "eingang"), "--out", str(tmp_path / "out"),
            "--ordner", "Rennweg", "--worker", "1"]


def test_versionsordner_mit_kennzahlen_bricht_ab(tmp_path, capsys):
    args = _eingang(tmp_path)
    kz = tmp_path / "out" / "Rennweg_v2" / "UG" / "kennzahlen.json"
    kz.parent.mkdir(parents=True)
    kz.write_text(json.dumps({"status": "ok", "version": "v2"}), encoding="utf-8")
    vorher = kz.read_bytes()

    assert rd.main([*args, "--version", "v2", "--slices", "keine", "--neu"]) == 2
    assert "Rennweg_v2 enthält schon kennzahlen.json" in capsys.readouterr().err
    assert kz.read_bytes() == vorher
    assert sorted(p.name for p in (tmp_path / "out").iterdir()) == ["Rennweg_v2"]


def test_version_aktuell_ist_gueltig_und_ebenso_gesperrt(tmp_path, capsys):
    assert rd._ordner_version("Rennweg_aktuell") == "aktuell"
    assert rd._ordner_version("Rennweg_v3") == "v3" and rd._ordner_version("Rennweg") == "v1"
    args = _eingang(tmp_path)
    kz = tmp_path / "out" / "Rennweg_aktuell" / "UG" / "kennzahlen.json"
    kz.parent.mkdir(parents=True)
    kz.write_text(json.dumps({"status": "ok", "version": "aktuell"}), encoding="utf-8")
    assert rd.main([*args, "--version", "aktuell", "--slices", "keine", "--neu"]) == 2
    assert "Rennweg_aktuell enthält schon kennzahlen.json" in capsys.readouterr().err


def test_lauf_ohne_version_bricht_ab(tmp_path, capsys):
    assert rd.main(_eingang(tmp_path)) == 2
    assert "jede neue Ausgabe als eigener Versionsordner" in capsys.readouterr().err
    assert list((tmp_path / "out").iterdir()) == []


def _kz_cache(tueren):
    raeume = [{**_raum(rid, typ, x, 0, x + 2000, 2000), "wohnung_id": w}
              for rid, typ, x, w in (("a1", "ZIMMER", 0, "W1"), ("a2", "BAD", 2000, "W1"),
                                     ("b1", "ZIMMER", 5000, "W3"), ("c1", "KÜCHE", 8000, "W2"),
                                     ("l", "LIFT", 11000, None), ("s", "SCHACHT", 14000, None))]
    cache = {"raeume": raeume, "stempel": [], "aussen_offen": [], "aussen_geschlossen": [],
             "zuordnung_quelle": "Erkennung", "raeume_nicht_gezeigt": 0, "geschoss": "OG1",
             "geschoss_quelle": "test", "kein_umriss": False, "rotation_vermerk": ""}
    if tueren is not None:
        cache["tueren"] = tueren
    return cache


def test_kennzahlen_einraum_tueren_lifte():
    tueren = [{"tuer_detail": d, "ohne_tuerblatt": o}
              for d, o in (("zimmertuer", False), (None, True), (None, False),
                           ("wohnungseingang", False), ("zimmertuer", False))]
    kz = rd._kennzahlen(_kz_cache(tueren), [])
    assert kz["einraum_wohnungen"] == 2 and kz["einraum_wohnungen_liste"] == ["W2", "W3"]
    assert kz["tueren_gesamt"] == 5 and kz["tueren_typisiert"] == 3
    assert kz["durchgaenge_ohne_tuerblatt"] == 1
    # nach Anzahl absteigend, bei Gleichstand nach Name
    assert list(kz["tueren_je_typ"].items()) == [
        ("untypisiert", 2), ("zimmertuer", 2), ("wohnungseingang", 1)]
    assert kz["lifte_erkannt"] == 1 and kz["schaechte_erkannt"] == 1


def test_kennzahlen_alter_cache_ohne_tueren_ist_none_nicht_null():
    kz = rd._kennzahlen(_kz_cache(None), [])
    for k in ("tueren_gesamt", "tueren_typisiert", "tueren_je_typ", "durchgaenge_ohne_tuerblatt"):
        assert kz[k] is None, k
    # Tabellen lesen auch eine v2-kennzahlen.json ohne die neuen Schlüssel.
    v2 = {k: v for k, v in kz.items() if k not in (
        "einraum_wohnungen", "einraum_wohnungen_liste", "lifte_erkannt")}
    v2.update(status="ok", laufzeit_s={"gesamt": 1, "erkennung": 1, "zeichnen": 0})
    zeilen = {label: wert for label, wert, _ in rd._owner_zeilen(v2)}
    assert zeilen["Türen gesamt (inkl. Durchgänge)"] == "—"
    assert zeilen["Einraum-Wohnungen"] == "—" and zeilen["Lifte erkannt"] == "—"
    (_d, _kz, _s, werte), = rd._uebersicht([(Path("OG1"), v2)])
    assert len(werte) == len(rd._UEB_KOPF) - 2


def test_titel_mit_und_ohne_basis():
    cache = {"geschoss": "OG1", "geschoss_quelle": "Dateiname"}
    meta = {"version": "v3", "datum": "2026-09-28", "slices": ["S1", "S2"]}
    ohne = rd._titel("Rennweg", "OG1", cache, "abc1234", meta)
    mit = rd._titel("Rennweg", "OG1", cache, "abc1234", {**meta, "basis": "aa05143"})
    assert "Commit abc1234 · Slices S1, S2" in ohne and "Stapel" not in ohne
    assert "Commit abc1234 (Stapel aa05143) · Slices S1, S2" in mit


def test_vergleich_links_aus_dateiname(tmp_path):
    (tmp_path / "VERGLEICH_v2_v3.md").write_text("x", encoding="utf-8")
    assert rd._vergleich_links(tmp_path) == [("Vergleich v2 → v3", "VERGLEICH_v2_v3.md")]


def test_kategorie_unbestimmter_gang_ist_magenta():
    """§ 6g Schritt 3: ein GANG/VORRAUM ohne entschiedene Klasse wird magenta
    ausgewiesen statt still als „Gang allgemein" gezeichnet — und nur er:
    ein NISCHE-Raum hat ebenfalls keine Nutzungsklasse und bleibt „nische"."""
    assert rd._kategorie("GANG", None) == "unbestimmt"
    assert rd._kategorie("VORRAUM", None) == "unbestimmt"
    assert rd._kategorie("GANG", "ALLGEMEIN_ERSCHLIESSUNG") == "gang"
    assert rd._kategorie("GANG", "WOHNUNG_PRIVAT") == "gang_whg"
    assert rd._kategorie("NISCHE", None) == "nische"
    assert rd._kategorie("", None) == "unbekannt"
    assert rd._KAT["unbestimmt"][1] == "#ff00ff"


def _schacht_plan(ordner: Path, name: str, geschoss: str, schaechte: list[tuple[str, float]]):
    """Plan-Unterordner mit kennzahlen.json (ok) und _cache.pkl (SCHACHT-Räume bei x)."""
    import pickle
    d = ordner / name
    d.mkdir(parents=True)
    (d / "kennzahlen.json").write_text(json.dumps({"status": "ok"}), encoding="utf-8")
    raeume = [_raum(rid, "SCHACHT", x, 0, x + 1000, 1000) for rid, x in schaechte]
    (d / "_cache.pkl").write_bytes(pickle.dumps({"raeume": raeume, "geschoss": geschoss}))


def test_schaechte_md_zahl_je_geschoss_lagen_und_warnung(tmp_path):
    """Slice K2, Owner-Regel b: SCHAECHTE.md je Projektordner — Schachtzahl je
    Geschoss (unten → oben, DG1 vor DG2 über den Namen), Lagen mit belegten
    Geschossen, Warnung für das Geschoss dazwischen."""
    ordner = tmp_path / "Rennweg_aktuell"
    _schacht_plan(ordner, "DG2 - x", "DG", [("r4", 0.0)])
    _schacht_plan(ordner, "DG1 - x", "DG", [("r3", 100.0), ("r1", 50000.0)])
    _schacht_plan(ordner, "OG2 - x", "2OG", [])
    _schacht_plan(ordner, "OG1 - x", "1OG", [("r2", 0.0)])
    ziel = rd._schaechte_md(ordner, rd._eintraege(ordner))
    text = ziel.read_text(encoding="utf-8")
    assert ziel.name == "SCHAECHTE.md"
    zeilen = [z for z in text.splitlines() if z.split(" | ")[0].endswith(" - x")]
    assert [z.split(" | ")[:3] for z in zeilen] == [
        ["| OG1 - x", "1OG", "1"], ["| OG2 - x", "2OG", "0"],
        ["| DG1 - x", "DG", "2"], ["| DG2 - x", "DG", "1"]]
    assert "| (500, 500) | OG1 - x, DG1 - x, DG2 - x | r2, r3, r4 |" in text
    assert "Schacht erwartet, nicht gefunden: OG2 - x bei (500, 500)" in text
