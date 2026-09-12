"""Korpus-Writer: Dedupe auf (plan_id, layer_name), JSONL-Fallback, Schema.

Der Korpus ist Trainingsdaten — Eingang, kein Ergebnis. Deshalb muss eine
Label-Korrektur eine Zeile ERSETZEN, nicht anhängen, und jede Zeile muss ihre
Layout-Version und ihren Plan-Faktor tragen (sonst ist sie später nicht
invalidierbar, wenn sich der mm-Faktor eines Plans ändert).
"""
from __future__ import annotations

import json

import pytest

from notbeleuchtung.raumerkennung import layer_features as lf

_SKALARFELDER = (
    "plan_id", "layer_name", "quelle", "layout_version", "vektor_laenge",
    "zeitstempel", "rolle", "confidence", "modus", "label_quelle",
    "plan_factor", "n_entities", "massstab_verdacht", "variante_verdacht",
    "runde2_belegt", "faktor_plausibel",
)


def _befund(plan_id: str, layer: str, rolle: str = "wand") -> lf.RollenBefund:
    m = lf.LayerMerkmale(
        plan_id=plan_id, layer_name=layer, quelle="msp", n_entities=42,
        n_punkte=84, plan_factor=1000.0, faktor_abhaengig=True,
        faktor_plausibel=True, massstab_verdacht=False, variante_verdacht=False,
        runde2_belegt=True, flaeche_median_m2=12.5, anteil_line=1.0,
        parallel_quote=0.5)
    return lf.RollenBefund(
        plan_id=plan_id, layer_name=layer, rolle=rolle, confidence=0.7,
        modus="BESTAETIGEN", scores={"wand": 0.7}, begruendung="Test",
        merkmale=m)


@pytest.fixture
def jsonl(monkeypatch):
    """pyarrow-Zweig abschalten → JSONL-Fallback erzwingen."""
    monkeypatch.setattr(lf, "_HAT_PYARROW", False)


def test_dedupe_ersetzt_statt_anzuhaengen(tmp_path, jsonl):
    ordner = tmp_path / "corpus"
    lf.schreibe_korpus([_befund("planA", "L1"), _befund("planA", "L2")],
                       lf.LABEL_NAMENSREGEL, ordner=ordner)
    ziel = lf.schreibe_korpus([_befund("planA", "L1", rolle="raumkontur")],
                              lf.LABEL_BESTAETIGT, ordner=ordner)
    zeilen = [json.loads(z) for z in ziel.read_text(encoding="utf-8").splitlines()]
    assert len(zeilen) == 2
    nach_layer = {z["layer_name"]: z for z in zeilen}
    assert nach_layer["L1"]["rolle"] == "raumkontur"
    assert nach_layer["L1"]["label_quelle"] == lf.LABEL_BESTAETIGT
    assert nach_layer["L2"]["rolle"] == "wand"
    assert nach_layer["L2"]["label_quelle"] == lf.LABEL_NAMENSREGEL


def test_jsonl_fallback_und_schema(tmp_path, jsonl):
    ziel = lf.schreibe_korpus([_befund("planA", "L1")], lf.LABEL_NAMENSREGEL,
                              ordner=tmp_path / "corpus")
    assert ziel.name == "layer_labels.jsonl"
    zeile = json.loads(ziel.read_text(encoding="utf-8").splitlines()[0])
    assert set(zeile) == {*_SKALARFELDER, "features"}
    assert tuple(zeile["features"]) == lf.FEATURE_NAMES
    assert len(zeile["features"]) == lf.VECTOR_LEN


def test_layout_version_und_faktor_in_jeder_zeile(tmp_path, jsonl):
    ziel = lf.schreibe_korpus([_befund("planA", "L1"), _befund("planB", "L1")],
                              lf.LABEL_NAMENSREGEL, ordner=tmp_path / "corpus")
    zeilen = [json.loads(z) for z in ziel.read_text(encoding="utf-8").splitlines()]
    assert len(zeilen) == 2          # gleicher Layername, anderer Plan
    for z in zeilen:
        assert z["layout_version"] == lf.FEATURE_LAYOUT_VERSION
        assert z["vektor_laenge"] == lf.VECTOR_LEN
        assert z["plan_factor"] == 1000.0
        assert z["zeitstempel"].endswith("+00:00")


def test_vereinige_hoehere_layout_version_gewinnt():
    """Ein Korpus-Ziel über den Suffix-Wechsel: lf-2 schlägt lf-1, egal welche Quelle.

    Ohne diese Regel überschreibt eine alte JSONL-Zeile eine neue Parquet-Zeile
    (oder umgekehrt) und der Korpus mischt lautlos zwei Layouts.
    """
    def zeile(layer: str, version: str, rolle: str) -> dict:
        return {"plan_id": "A", "layer_name": layer, "layout_version": version,
                "rolle": rolle, "features": {}}

    alt = zeile("L1", "lf-1", "wand")
    neu = zeile("L1", "lf-2", "rest")
    fremd = zeile("L2", "lf-1", "wand")
    for quellen in (([alt, fremd], [neu]), ([neu], [alt, fremd])):
        v = lf._vereinige(*quellen)
        assert set(v) == {("A", "L1"), ("A", "L2")}
        assert v[("A", "L1")]["rolle"] == "rest"     # lf-2 gewinnt beidseitig
        assert v[("A", "L2")]["layout_version"] == "lf-1"


def test_parquet_uebernimmt_jsonl_und_legt_sie_ab(tmp_path, monkeypatch):
    """Der erste `pip install -e .[layerml]` darf JSONL-Zeilen nicht verwaisen.

    pyarrow fehlt hier, deshalb ist NUR die Serialisierung gestubbt (JSONL-Bytes
    unter dem .parquet-Namen); geprüft wird die Übernahme und das Umbenennen.
    """
    ordner = tmp_path / "corpus"
    monkeypatch.setattr(lf, "_HAT_PYARROW", False)
    jsonl = lf.schreibe_korpus([_befund("planA", "L1")], lf.LABEL_NAMENSREGEL,
                               ordner=ordner)
    assert jsonl.name == "layer_labels.jsonl"

    def lies(p):
        return ([json.loads(z) for z in p.read_text(encoding="utf-8").splitlines() if z]
                if p.exists() else [])

    def schreib(ziel, zeilen):
        ziel.write_text("".join(json.dumps(z, ensure_ascii=False) + "\n"
                                for z in zeilen), encoding="utf-8")

    monkeypatch.setattr(lf, "_HAT_PYARROW", True)
    monkeypatch.setattr(lf, "_lies_datei", lies)
    monkeypatch.setattr(lf, "_schreibe_atomar", schreib)
    parquet = lf.schreibe_korpus([_befund("planB", "L9")], lf.LABEL_BESTAETIGT,
                                 ordner=ordner)

    assert parquet.name == "layer_labels.parquet"
    assert {(z["plan_id"], z["layer_name"]) for z in lies(parquet)} == {
        ("planA", "L1"), ("planB", "L9")}          # JSONL-Zeile übernommen
    assert not jsonl.exists()
    abgelegt = ordner / "layer_labels.jsonl.abgelegt"
    assert abgelegt.exists()                       # umbenannt, NICHT gelöscht
    assert [z["layer_name"] for z in lies(abgelegt)] == ["L1"]


def test_parquet_schema_gleich(tmp_path):
    """Gleiche Feldnamen wie JSONL, nur spaltig (`f_<name>`) — skippt ohne pyarrow."""
    pytest.importorskip("pyarrow")
    import pyarrow.parquet as pq
    ziel = lf.schreibe_korpus([_befund("planA", "L1")], lf.LABEL_NAMENSREGEL,
                              ordner=tmp_path / "corpus")
    assert ziel.name == "layer_labels.parquet"
    spalten = set(pq.read_table(ziel).column_names)
    assert spalten == {*_SKALARFELDER, *(f"f_{n}" for n in lf.FEATURE_NAMES)}
