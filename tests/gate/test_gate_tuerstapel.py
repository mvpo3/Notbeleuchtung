"""Das Türstapel-Gate am echten Plan: Eingabe, Nenner, Gate-Regel.

Der xfail-Test ist das Gate selbst. Er ist ``strict``: solange der Stapel
S4a → S4b → S5b → S5c nicht gebaut ist, schlägt er erwartungsgemäß fehl
(xfailed). Sobald eine Messung das Gate erfüllt, dreht er auf XPASS und die
Suite wird rot — dann wird der Marker entfernt und der Stapel gemerged.

Vorher-Stand ist die eingecheckte ``nullmessung_f15d03f.json``. Die sieben
Rennweg-DXF SIND im Repo getrackt (``Projekte/Rennweg/``, Ausnahme in
``.gitignore``); außerhalb liegt nur das Referenzpaket. Ohne Referenzpaket wird
übersprungen — CI hat es nicht. Ist ``NOTBEL_M17_REFERENZ`` dagegen GESETZT und
zeigt ins Leere, wird NICHT übersprungen, sondern der Test schlägt fehl: ein
Tippfehler im Pfad darf nicht als „Referenz fehlt eben" durchgehen.

Der ganze Modul trägt den Marker ``gate`` (langsam: 7 Caches + voller
Erkennungslauf) und ist per ``addopts`` deselektiert; gezielt: ``pytest -m gate``.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from gate_m1_m4 import PLAENE
from gate_m17 import STATUS, lade_referenz, referenz_pfad
from gate_messung import WURZEL, dxf_pfad, messung
from gate_regel import NENNER, pruefe_gate

pytestmark = pytest.mark.gate

NULLMESSUNG = Path(__file__).resolve().parent / "nullmessung_f15d03f.json"
OG1_SHA256 = "c64e73e30a482d3fe7c38004b726151eb5325e4beb453def4d92dba5afaa245e"


@pytest.fixture(scope="module")
def frische_messung() -> dict:
    """Ein vollständiger Messlauf auf dem heutigen Arbeitsstand."""
    try:
        pfad = referenz_pfad()
    except FileNotFoundError as fehler:
        pytest.fail(f"NOTBEL_M17_REFERENZ ist gesetzt, aber unbrauchbar: {fehler}")
    if pfad is None:
        pytest.skip("Referenz-JSON des Übergabepakets nicht gefunden (NOTBEL_M17_REFERENZ "
                    "setzen; das Paket gehört nicht ins Repo)")
    if not dxf_pfad(WURZEL, "OG1").is_file():
        pytest.skip("Rennweg-Plan OG1 liegt nicht unter Projekte/Rennweg/")
    return messung(WURZEL)


@pytest.fixture(scope="module")
def nullmessung() -> dict:
    return json.loads(NULLMESSUNG.read_text(encoding="utf-8"))


def test_eingabe_dxf_ist_die_referenz_dxf(frische_messung):
    assert frische_messung["meta"]["dxf"]["OG1"] == OG1_SHA256


def test_alle_sieben_dxf_wie_in_der_nullmessung(frische_messung, nullmessung):
    """Gleiche Eingabe oder kein Vergleich — Bedingung (0) der Gate-Regel."""
    jetzt, vorher = frische_messung["meta"]["dxf"], nullmessung["meta"]["dxf"]
    assert sorted(jetzt) == sorted(PLAENE)
    assert {p: jetzt.get(p) for p in PLAENE} == {p: vorher.get(p) for p in PLAENE}


def test_nenner_bleibt_18(frische_messung):
    ids_referenz = [c["id"] for fall in lade_referenz(referenz_pfad())["cases"]
                    for c in fall["checks"]]
    eintraege = frische_messung["m17"]
    assert len(eintraege) == NENNER == len(ids_referenz)
    assert [e["id"] for e in eintraege] == ids_referenz
    for e in eintraege:
        assert e["status"] in STATUS
        if e["status"] != "BESTANDEN":
            assert e["grund"].strip(), f"{e['id']} ohne Grund"


@pytest.mark.xfail(strict=True, raises=AssertionError,
                   reason="Türstapel S4a→S4b→S5b→S5c nicht gebaut — Gate-Regel in "
                          "docs/GATE_TUERSTAPEL.md")
def test_gate_tuerstapel_erfuellt(nullmessung, frische_messung):
    verstoesse = pruefe_gate(nullmessung, frische_messung)
    assert verstoesse == [], "Gate nicht erfüllt:\n" + "\n".join(verstoesse)
