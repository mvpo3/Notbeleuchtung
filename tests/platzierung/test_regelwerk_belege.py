"""Beleg-Tests je Basis-Regel: die DXF-Handles des Regelwerks existieren real.

Auftrag „Wissensaufbau" Schritt 5.5 — für jede Basis-Regel mindestens ein
automatisierter Test mit Geometrie aus den Referenz-DXFs (Handles als
Testfälle). Asset-Skip-Konvention: ohne knowledge-Checkout wird geskippt.
"""
from __future__ import annotations

import json
from functools import cache
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_WISSEN = _REPO / "knowledge" / "Pläne zeichnen Wissen"
_REGELWERK = _WISSEN / "_Analyse_Regelwerk" / "REGELWERK_Notbeleuchtung.json"

pytestmark = pytest.mark.skipif(
    not _REGELWERK.exists(), reason="Regelwerk-JSON nicht im Checkout (Asset-Skip)"
)


@cache
def _handles(dxf_rel: str) -> frozenset[str]:
    import ezdxf

    pfad = _WISSEN / dxf_rel
    if not pfad.exists():
        return frozenset()
    doc = ezdxf.readfile(str(pfad))
    return frozenset(e.dxf.handle for e in doc.modelspace())


def _basis_regeln() -> list[dict]:
    regeln = json.loads(_REGELWERK.read_text(encoding="utf-8"))
    return [r for r in regeln if r.get("prioritaet") == "basis"]


@pytest.mark.parametrize(
    "regel", _basis_regeln() if _REGELWERK.exists() else [],
    ids=lambda r: r["id"],
)
def test_basis_regel_hat_realen_dxf_beleg(regel: dict):
    belege = regel.get("belege_dxf") or []
    if not belege:
        assert regel.get("beleg_alternativ"), (
            f"{regel['id']}: weder belege_dxf noch beleg_alternativ"
        )
        return
    # mindestens EIN Handle je Regel muss in seiner Quell-DXF real existieren;
    # geprüft wird die erste verifizierbare Datei (Cache über lru_cache).
    geprueft = 0
    for b in belege:
        vorhandene = _handles(b["datei"])
        if not vorhandene:
            continue  # DXF nicht im Checkout — nächster Beleg
        geprueft += 1
        if b.get("handle") in vorhandene:
            return
        if geprueft >= 5:
            break
    if geprueft == 0:
        pytest.skip(f"{regel['id']}: keine Beleg-DXF im Checkout")
    pytest.fail(f"{regel['id']}: keiner der geprüften Handles existiert in den Beleg-DXFs")
