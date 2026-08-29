"""Slice 2 — der echte NotlichtPlatzierer reproduziert die 5 echten 4OG-RZ.

Akzeptanz = **Struktur-Match** (Owner-Entscheid: generativ statt faithful): Position,
Anzahl, kind, covers_segment, norm_quelle ∈ Regelwerk, catalog_key ∈ Mapping. Die
exakten Sub-Grad-Rotationen des Fixtures (180.1° …) sind DXF-Extraktions-Artefakte
und werden bewusst NICHT geprüft — der Platzierer leitet die Orientierung generativ
aus der Segment-Geometrie ab.
"""
import json
from pathlib import Path

from fakes import FakeNormProvider, FakeRaumProvider
from notbeleuchtung.hauptengine.contracts import (
    NormRegelwerk,
    Platzierer,
    PlatzierungsErgebnis,
)
from notbeleuchtung.platzierung import NotlichtPlatzierer
from notbeleuchtung.symbols import catalog_keys

FIXTURES = Path(__file__).parents[1] / "fixtures"


def _load(name: str) -> dict:
    with open(FIXTURES / name, encoding="utf-8") as fh:
        return json.load(fh)


def _place() -> PlatzierungsErgebnis:
    raum = FakeRaumProvider().parse("<fake>", "4OG")
    return NotlichtPlatzierer().place(raum, FakeNormProvider())


def test_erfuellt_platzierer_protocol():
    assert isinstance(NotlichtPlatzierer(), Platzierer)


def test_reproduziert_fuenf_rettungszeichen():
    out = _place()
    assert out.floor == "4OG"
    rz = [p for p in out.platzierungen if p.kind == "rz"]
    assert len(rz) == 5


def test_platziert_aufheller_je_stiegenhaus():
    # Beide STIEGENHÄUSER sind norm-seitig 'sicherheitsleuchte' → je 1 Aufheller
    # am Raum-Zentrum, mit Kein-Segment-Bindung.
    out = _place()
    sl = [p for p in out.platzierungen if p.kind == "sicherheitsleuchte"]
    assert len(sl) == 2
    assert all(p.catalog_key == "sicherheitsleuchte_aufheller" for p in sl)
    assert all(p.covers_segment == [] for p in sl)


def test_rz_nutzen_direktionale_bloecke():
    # Richtungs-Fix: rechts/links-RZ tragen den dedizierten Block, ohne Rotation/Spiegelung.
    out = _place()
    for p in out.platzierungen:
        if p.kind == "rz" and p.richtung in {"links", "rechts"}:
            assert p.catalog_key == f"notlicht_ks_stiege_{p.richtung}"
            assert p.rotation_deg == 0.0
            assert p.mirror_x is False


def test_positionen_und_covers_matchen_fixture():
    out = _place()
    fixture = PlatzierungsErgebnis.model_validate(_load("platzierung_4og.json"))

    # Golden ist RZ-only → nur die RZ-Platzierungen vergleichen.
    got = {tuple(p.xy_mm): tuple(p.covers_segment) for p in out.platzierungen if p.kind == "rz"}
    want = {tuple(p.xy_mm): tuple(p.covers_segment) for p in fixture.platzierungen}
    assert got == want


def test_naht_norm_quelle_und_catalog_key():
    out = _place()
    quellen = set(NormRegelwerk.model_validate(_load("norm_regelwerk_snapshot.json")).quellen)
    keys = catalog_keys()
    for p in out.platzierungen:
        assert p.norm_quelle in quellen, f"norm_quelle {p.norm_quelle!r} nicht im Regelwerk"
        assert p.catalog_key in keys, f"catalog_key {p.catalog_key!r} fehlt im Mapping"
        if p.kind == "rz":
            assert set(p.covers_segment)  # jedes RZ deckt genau sein Segment
        else:
            assert p.covers_segment == []  # Raum-Leuchten sind nicht segmentgebunden


def test_richtung_ist_gueltiger_kardinal():
    """Orientierung generativ (Kardinal), nicht die GT-Sub-Grad-Werte."""
    out = _place()
    for p in out.platzierungen:
        assert p.richtung in {"links", "rechts", "oben", "unten", "gerade"}
        assert p.rotation_deg in {0.0, 90.0, 180.0, 270.0}
