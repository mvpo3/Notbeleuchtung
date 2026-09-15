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


def test_lauf_ohne_version_bricht_ab(tmp_path, capsys):
    assert rd.main(_eingang(tmp_path)) == 2
    assert "jede neue Ausgabe als eigener Versionsordner" in capsys.readouterr().err
    assert list((tmp_path / "out").iterdir()) == []
