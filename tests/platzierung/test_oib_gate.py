"""oib_gate — Gate-Matrix (projekt-global, fail-closed) + Audit-Summary."""
from __future__ import annotations

import pytest

from notbeleuchtung.hauptengine.contracts import OibBefund, OibErgebnis
from notbeleuchtung.platzierung.oib_gate import flaechen_trigger_offen, gate_summary


def _befund(*stufen: str) -> OibBefund:
    return OibBefund(
        ergebnisse=[
            OibErgebnis(
                gebaeudeteil_id=f"teil_{i}", stufe=s,
                quelle="OIB-RL 2 Tabelle 6", norm_ausgabe="Mai 2023",
            )
            for i, s in enumerate(stufen, start=1)
        ]
    )


@pytest.mark.parametrize(
    ("stufen", "offen"),
    [
        (("eingeschraenkt",), True),
        (("uneingeschraenkt",), True),
        (("review_required",), False),          # fail-closed
        (("nicht_erforderlich",), False),
        ((), False),                             # leerer Befund
        (("review_required", "eingeschraenkt"), True),  # EIN bestätigter Teil genügt
    ],
)
def test_gate_matrix(stufen, offen):
    assert flaechen_trigger_offen(_befund(*stufen)) is offen


def test_gate_zu_ohne_befund():
    assert flaechen_trigger_offen(None) is False


def test_gate_summary_offen():
    s = gate_summary(_befund("eingeschraenkt", "review_required"))
    assert s["flaechen_trigger_gate"] == "offen"
    assert s["stufen"] == {"teil_1": "eingeschraenkt", "teil_2": "review_required"}
    # v1-Hinweis (projekt-global) immer dabei.
    assert any("projekt-global" in h for h in s["hinweise"])


def test_gate_summary_zu_bei_review_nennt_grund():
    s = gate_summary(_befund("review_required"))
    assert s["flaechen_trigger_gate"] == "zu"
    assert any("review_required" in h for h in s["hinweise"])
