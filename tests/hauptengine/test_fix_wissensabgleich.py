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


def test_f03_rotation_zur_tuer_ein_helper():
    """F03 / W16: die 4× duplizierte Pfeil-Rotationsformel lebt jetzt in einem Helper.
    Exakte Kardinal-Werte (unten-Block-Basis, atan2+90 auf 90° gerastert)."""
    from notbeleuchtung.platzierung.bausteine import rotation_zur_tuer as r
    assert r(1.0, 0.0) == 90.0     # Ziel rechts
    assert r(0.0, 1.0) == 180.0    # Ziel oben
    assert r(-1.0, 0.0) == 270.0   # Ziel links
    assert r(0.0, -1.0) == 0.0     # Ziel unten
