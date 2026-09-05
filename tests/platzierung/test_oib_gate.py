"""oib_gate — Gate-Matrix (fail-closed) + Raum-Scope (v2) + Audit-Summary."""
from __future__ import annotations

import pytest

from notbeleuchtung.hauptengine.contracts import OibBefund, OibErgebnis, RaumReferenz
from notbeleuchtung.platzierung.oib_gate import (
    flaechen_trigger_offen,
    freigegebene_raeume,
    gate_summary,
)


def _erg(stufe: str, i: int = 1, refs: tuple = ()) -> OibErgebnis:
    return OibErgebnis(
        gebaeudeteil_id=f"teil_{i}", stufe=stufe,
        quelle="OIB-RL 2 Tabelle 6", norm_ausgabe="Mai 2023",
        raum_referenzen=[RaumReferenz(floor=f, raum_id=r) for f, r in refs],
    )


def _befund(*stufen: str) -> OibBefund:
    return OibBefund(ergebnisse=[_erg(s, i) for i, s in enumerate(stufen, start=1)])


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


# ── Raum-Scope (v2) ────────────────────────────────────────────────────────────


def test_scope_ohne_befund_ist_global():
    assert freigegebene_raeume(None, "EG") is None


def test_scope_bestaetigend_ohne_referenzen_ist_global():
    b = OibBefund(ergebnisse=[_erg("eingeschraenkt")])
    assert freigegebene_raeume(b, "EG") is None


def test_scope_raum_genau_filtert_nach_geschoss():
    b = OibBefund(ergebnisse=[
        _erg("eingeschraenkt", 1, refs=(("EG", "r1"), ("EG", "r2"), ("1OG", "r9"))),
    ])
    assert freigegebene_raeume(b, "EG") == {"r1", "r2"}
    assert freigegebene_raeume(b, "1OG") == {"r9"}
    assert freigegebene_raeume(b, "2OG") == set()   # Geschoss ohne Referenz → nichts frei


def test_scope_gemischt_ein_teil_ohne_referenzen_ist_global():
    # Ein bestätigender Teil OHNE Zuordnung darf nicht still enger ausgelegt werden.
    b = OibBefund(ergebnisse=[
        _erg("eingeschraenkt", 1, refs=(("EG", "r1"),)),
        _erg("uneingeschraenkt", 2),
    ])
    assert freigegebene_raeume(b, "EG") is None


def test_scope_ignoriert_nicht_bestaetigende_teile():
    # review_required-Referenzen zählen nicht — nur bestätigende Teile scopen.
    b = OibBefund(ergebnisse=[
        _erg("eingeschraenkt", 1, refs=(("EG", "r1"),)),
        _erg("review_required", 2, refs=(("EG", "r7"),)),
    ])
    assert freigegebene_raeume(b, "EG") == {"r1"}


def test_gate_summary_raum_genau_flag_und_hinweis():
    b = OibBefund(ergebnisse=[_erg("eingeschraenkt", 1, refs=(("EG", "r1"),))])
    s = gate_summary(b)
    assert s["flaechen_trigger_gate"] == "offen"
    assert s["raum_genau"] is True
    assert any("raum-genau" in h for h in s["hinweise"])

    s_global = gate_summary(_befund("eingeschraenkt"))
    assert s_global["raum_genau"] is False
    assert any("projekt-global" in h for h in s_global["hinweise"])
