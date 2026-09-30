"""M3 nimmt NISCHE wie SCHACHT aus (Owner-Entscheid 2026-09-30, K2 Option c).

Synthetisch, ohne echten Plan: ein Cache mit zwei Räumen — der ausgenommene Raum
(SCHACHT bzw. NISCHE) und ein ZIMMER —, in jedem eine rote Kontur. M3 zählt nur
das ZIMMER, rote Fläche nur dessen Kasten. SCHACHT ist die Kontrolle (galt schon
immer), NISCHE die neue Gate-Definition.
"""
from __future__ import annotations

import importlib.util
import json
import pickle
from collections import Counter, defaultdict
from pathlib import Path

import ezdxf
import pytest

SKRIPT = Path(__file__).resolve().parent / "diagnose_skripte" / "m3_schacht_ohne_stanzung.py"


def _quadrat(x0: float, y0: float, seite: float) -> list[tuple[float, float]]:
    return [(x0, y0), (x0 + seite, y0), (x0 + seite, y0 + seite), (x0, y0 + seite)]


def _lade_m3(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("NOTBEL_REPO", str(tmp_path))
    monkeypatch.setenv("NOTBEL_GATE_CACHES", str(tmp_path / "erg"))
    spec = importlib.util.spec_from_file_location("_m3_synthetisch", SKRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("typ", ["SCHACHT", "NISCHE"])
def test_m3_zaehlt_ausgenommenen_raum_nicht(typ, tmp_path, monkeypatch):
    m3 = _lade_m3(tmp_path, monkeypatch)

    doc = ezdxf.new()
    msp = doc.modelspace()
    for x0 in (200.0, 5200.0):  # je 500 x 500 mm = 0,25 m² rot, einer je Raum
        msp.add_lwpolyline(_quadrat(x0, 200.0, 500.0), close=True, dxfattribs={"color": 1})
    doc.saveas(tmp_path / "plan.dxf")

    from notbeleuchtung.raumerkennung import dxf_load
    monkeypatch.setattr(dxf_load, "lade_dxf",
                        lambda pfad: dxf_load.DxfPlan(doc=doc, space=msp, factor=1.0))

    ordner = tmp_path / "erg" / "Synth_v0" / "DG2 - synthetisch"
    ordner.mkdir(parents=True)
    raeume = [
        {"id": "rest_5", "typ": typ, "polygon_mm": _quadrat(0.0, 0.0, 1000.0), "flaeche_m2": 1.0},
        {"id": "raum_5", "typ": "ZIMMER", "polygon_mm": _quadrat(5000.0, 0.0, 1000.0),
         "flaeche_m2": 1.0},
    ]
    (ordner / "_cache.pkl").write_bytes(pickle.dumps({"raeume": raeume}))
    (ordner / "kennzahlen.json").write_text(json.dumps({"dxf": "plan.dxf"}), encoding="utf-8")

    inv = {"tokens": defaultdict(lambda: {"n": 0, "je_plan": Counter(), "layer": Counter(),
                                          "tiefe": Counter(), "texte": Counter(),
                                          "beispiele": []}),
           "normtexte": Counter(), "typen": Counter(), "kontur_farben": Counter(),
           "rot_layer": Counter(), "rot_pfad_top": Counter()}
    rot = m3.messe_plan(ordner / "_cache.pkl", inv)["rot_flaeche_in_raeumen"]

    assert [r["id"] for r in rot["raeume"]] == ["raum_5"]
    assert rot["raeume_n"] == 1
    assert rot["in_raeumen_m2"] == pytest.approx(0.25)
