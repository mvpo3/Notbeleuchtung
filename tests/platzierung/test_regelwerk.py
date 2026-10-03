"""Tests für platzierung.regelwerk — Regeln-als-Daten + Umsetzungs-Vollständigkeit.

Naht-Schutz: das Modul parst NUR die eigene data-JSON (Referenz-Praxis-Lane),
kein Enis-YAML. Die knowledge-Fassung (Superset mit Belegen) wird, wo im
Checkout vorhanden, auf ID-Konsistenz gegengeprüft.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from notbeleuchtung.platzierung import regelwerk

_KNOWLEDGE_JSON = (
    Path(__file__).resolve().parents[2]
    / "knowledge" / "Pläne zeichnen Wissen" / "_Analyse_Regelwerk"
    / "REGELWERK_Notbeleuchtung.json"
)


def test_laedt_und_ids_eindeutig():
    regeln = regelwerk.alle()
    assert len(regeln) >= 27, "mindestens die 27 migrierten Basis-Regeln"
    assert all(rid.startswith("RW-") for rid in regeln)
    # frozen: Regel-Datensätze sind unveränderlich
    r = regelwerk.regel("RW-006")
    with pytest.raises(AttributeError):
        r.thema = "x"  # type: ignore[misc]


def test_basis_regeln_migriert_mit_nb_ref():
    basis = regelwerk.basis_regeln()
    assert len(basis) >= 27
    nb_refs = {r.nb_ref for r in basis if r.nb_ref}
    assert {"NB-R01", "NB-R06", "NB-R13", "NB-R16", "NB-R27"} <= nb_refs


def test_jede_basis_regel_hat_umsetzung_oder_begruendung():
    """Auftrags-Gate Schritt 5.3: jede Basis-Regel ist entweder im Code
    verankert (UMSETZUNG) oder mit dokumentiertem Grund nicht umsetzbar."""
    for r in regelwerk.basis_regeln():
        ok = r.id in regelwerk.UMSETZUNG or r.id in regelwerk.NICHT_UMSETZBAR
        assert ok, f"{r.id} ({r.thema}): weder UMSETZUNG noch NICHT_UMSETZBAR"
    doppelt = set(regelwerk.UMSETZUNG) & set(regelwerk.NICHT_UMSETZBAR)
    assert not doppelt, f"Regeln doppelt gemappt: {doppelt}"


def test_jede_ergaenzungsregel_ist_klassifiziert():
    """Review 2026-10-03: auch die Ergänzungsregeln (RW-101..131) sind vollständig
    als UMSETZUNG (gebaut) oder NICHT_UMSETZBAR (Grund/Lane) klassifiziert — die
    „dokumentiert vs. umgesetzt"-Lücke endete vorher bei RW-035. Wächst das
    Regelwerk, fällt der Test auf, bis die neue Regel eingeordnet ist."""
    ergaenzung = [r for r in regelwerk.alle().values() if not r.ist_basis]
    assert ergaenzung, "keine Ergänzungsregeln geladen"
    for r in ergaenzung:
        ok = r.id in regelwerk.UMSETZUNG or r.id in regelwerk.NICHT_UMSETZBAR
        assert ok, f"{r.id} ({r.thema}): weder UMSETZUNG noch NICHT_UMSETZBAR"


def test_quelle_string_traegt_praxis_praefix():
    q = regelwerk.quelle("RW-006")
    assert q.startswith(regelwerk.PRAXIS_PREFIX)
    assert "RW-006" in q


@pytest.mark.skipif(not _KNOWLEDGE_JSON.exists(), reason="knowledge-Fassung nicht im Checkout")
def test_engine_json_ist_teilmenge_der_knowledge_fassung():
    knowledge = {r["id"] for r in json.loads(_KNOWLEDGE_JSON.read_text(encoding="utf-8"))}
    engine = set(regelwerk.alle())
    fehlen = engine - knowledge
    assert not fehlen, f"Engine-Regeln ohne knowledge-Quelle: {sorted(fehlen)}"
