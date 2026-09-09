"""Guard: Referenz-Extraktion + Matching der Prüfstrecke (scripts/plan_pruefen.py).

test_soll_referenzvergleich.py verankert nur das ZIELBILD (≥80 % Trefferquote,
xfail strict) — es läuft auf echten CAD-Assets und ist rot per Design. Bricht
dagegen das Matching selbst (Frame-Offset verrutscht, Rotations-Normalisierung
mod 180 fällt weg, Greedy vergibt eine eigene Leuchte doppelt), fällt das
nirgends auf: die Quote sinkt einfach, der xfail bleibt xfail.

Hier deshalb synthetische Leuchten-Listen ohne CAD-Asset: Offset m→mm,
Fenster-Filter, Layer→kind, Rotation mod 180, Treffer-Toleranzen (1 m / 10°),
fehlende und überzählige Leuchten.
"""
import importlib.util
import sys
from pathlib import Path

import ezdxf
import pytest

from notbeleuchtung.hauptengine.contracts import Platzierung, PlatzierungsErgebnis

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def pp():
    spec = importlib.util.spec_from_file_location(
        "plan_pruefen", REPO / "scripts" / "plan_pruefen.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["plan_pruefen"] = mod
    spec.loader.exec_module(mod)
    return mod


def _platz(*leuchten) -> PlatzierungsErgebnis:
    """leuchten: (x_mm, y_mm, rotation_deg)."""
    return PlatzierungsErgebnis(
        floor="T",
        platzierungen=[
            Platzierung(xy_mm=(x, y), rotation_deg=rot, kind="rz",
                        catalog_key="notlicht_ks_stiege")
            for x, y, rot in leuchten
        ],
    )


def _ref(x, y, rot=0.0, kind="rz", typ="A"):
    return {"x": x, "y": y, "rot": rot, "block": "REF", "typ": typ, "kind": kind}


# ---------------------------------------------------------------- Extraktion

def test_referenz_leuchten_offset_fenster_und_layer(pp, tmp_path, monkeypatch):
    """Frame: nur INSERTs im Fenster, nur gemappte Layer, + Offset (m) × 1000."""
    doc = ezdxf.new("R2018")
    for layer in pp._REF_LAYER_KIND:
        doc.layers.add(layer)
    doc.layers.add("irgendein_anderer_layer")
    msp = doc.modelspace()
    doc.blocks.new("REFBLOCK")
    msp.add_blockref("REFBLOCK", (50_000.0, 10_000.0),
                     dxfattribs={"layer": "din_SIBEL_10_emergency_lighting",
                                 "rotation": -90.0})
    msp.add_blockref("REFBLOCK", (50_000.0, 12_000.0),
                     dxfattribs={"layer": "din_SIBEL_10_emergency_lighting_yellow"})
    # außerhalb des Fensters
    msp.add_blockref("REFBLOCK", (10_000.0, 10_000.0),
                     dxfattribs={"layer": "din_SIBEL_10_emergency_lighting"})
    # ungemappter Layer
    msp.add_blockref("REFBLOCK", (50_000.0, 11_000.0),
                     dxfattribs={"layer": "irgendein_anderer_layer"})
    pfad = tmp_path / "ref.dxf"
    doc.saveas(pfad)

    monkeypatch.setattr(pp, "_REFERENZ_DXF", pfad)
    monkeypatch.setattr(pp, "_REFERENZ_FRAME",
                        {"T": ((-1.5, 2.0), (45_000.0, 5_000.0, 70_000.0, 45_000.0))})

    refs = pp._referenz_leuchten("T", None)
    assert [(r["x"], r["y"], r["kind"], r["rot"]) for r in refs] == [
        (48_500.0, 12_000.0, "rz", 270.0),
        (48_500.0, 14_000.0, "sicherheitsleuchte", 0.0),
    ]


def test_referenz_leuchten_unbekannter_frame_ist_leer(pp):
    assert pp._referenz_leuchten("gibt_es_nicht", None) == []


# ------------------------------------------------------------------ Matching

def test_treffer_innerhalb_toleranz(pp):
    refs = [_ref(0.0, 0.0, rot=0.0)]
    treffer, fehlend, ueber = pp._referenz_match(refs, _platz((900.0, 0.0, 9.0)))
    assert len(treffer) == 1 and not fehlend and not ueber
    r, p, d = treffer[0]
    assert r is refs[0] and p.xy_mm == (900.0, 0.0) and d == pytest.approx(900.0)


def test_rotation_mod_180_ist_treffer(pp):
    """Panel-Achse: 180° gedreht ist dieselbe Achse, 90° nicht."""
    refs = [_ref(0.0, 0.0, rot=0.0)]
    treffer, _f, _u = pp._referenz_match(refs, _platz((0.0, 0.0, 180.0)))
    assert len(treffer) == 1
    treffer, fehlend, ueber = pp._referenz_match(refs, _platz((0.0, 0.0, 90.0)))
    assert not treffer and len(fehlend) == 1 and len(ueber) == 1


def test_abstand_und_winkel_grenzen(pp):
    """>1 m oder >10° → kein Treffer, die eigene Leuchte wird überzählig."""
    for eigene in ((1100.0, 0.0, 0.0), (0.0, 0.0, 11.0)):
        treffer, fehlend, ueber = pp._referenz_match([_ref(0.0, 0.0)], _platz(eigene))
        assert not treffer and len(fehlend) == 1 and len(ueber) == 1, eigene


def test_fehlende_und_ueberzaehlige(pp):
    refs = [_ref(0.0, 0.0), _ref(50_000.0, 0.0, typ="B")]
    treffer, fehlend, ueber = pp._referenz_match(
        refs, _platz((100.0, 0.0, 0.0), (80_000.0, 0.0, 0.0)))
    assert len(treffer) == 1
    assert [r["typ"] for r in fehlend] == ["B"]
    assert [p.xy_mm for p in ueber] == [(80_000.0, 0.0)]


def test_greedy_vergibt_jede_eigene_leuchte_nur_einmal(pp):
    """Zwei Referenzen, eine eigene Leuchte in Reichweite beider: erste Referenz
    (Listenreihenfolge) gewinnt, die zweite bleibt fehlend."""
    refs = [_ref(0.0, 0.0), _ref(1000.0, 0.0, typ="B")]
    treffer, fehlend, ueber = pp._referenz_match(refs, _platz((900.0, 0.0, 0.0)))
    assert len(treffer) == 1 and treffer[0][0] is refs[0]
    assert [r["typ"] for r in fehlend] == ["B"] and not ueber


def test_greedy_nimmt_die_naechste_freie(pp):
    refs = [_ref(0.0, 0.0)]
    treffer, _f, ueber = pp._referenz_match(
        refs, _platz((900.0, 0.0, 0.0), (100.0, 0.0, 0.0)))
    assert treffer[0][1].xy_mm == (100.0, 0.0)
    assert [p.xy_mm for p in ueber] == [(900.0, 0.0)]


def test_system_leuchten_zaehlen_nicht(pp):
    """Controller (kind='system') sind keine Referenz-Leuchten."""
    treffer, fehlend, ueber = pp._referenz_match(
        [_ref(0.0, 0.0, kind="system")], _platz())
    assert not treffer and not fehlend and not ueber
