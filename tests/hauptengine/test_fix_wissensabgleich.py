"""Fix-Tests des Branches leonis/wissensabgleich-engine.

Je Fix eine maschinelle, exakte Assertion (keine Toleranzbereiche). Befund-IDs
verweisen auf docs/audit/FIX_PLAN.md bzw. 05_widersprueche.md.
"""
from __future__ import annotations


def test_f04_redundanz_radius_kommt_aus_der_norm():
    """F04 / W08: Die Redundanz-Reichweite ist nicht mehr die Konstante 30000, sondern
    `norm.erkennungsweite_m(0,15, hinterleuchtet)*1000`. Ohne Provider: Fallback-Konstante."""
    from notbeleuchtung.hauptengine.validierung import (
        _REDUNDANZ_REICHWEITE_MM,
        _redundanz_radius_mm,
    )

    class _StubNorm:
        def erkennungsweite_m(self, piktogramm_hoehe_m, hinterleuchtet):
            return 12.0  # bewusst != 30 m Default

    assert _redundanz_radius_mm(_StubNorm()) == 12000.0
    assert _redundanz_radius_mm(None) == _REDUNDANZ_REICHWEITE_MM
