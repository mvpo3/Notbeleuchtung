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


def test_lux_nachweis_wf_eine_quelle():
    """F01 / W09: Heatmap-Feld und Nachweis ziehen den Wartungsfaktor aus EINER Quelle
    (`anf.wartungsfaktor`), 0,80 nicht mehr hart. `_lux_feld` skaliert exakt linear mit wf;
    `_wf` liest genau das Norm-Feld (Fallback 1,0)."""
    import numpy as np

    from notbeleuchtung.hauptengine.render.lux_nachweis_bericht import _lux_feld, _wf

    gx, gy = np.meshgrid(np.linspace(0.0, 3000.0, 5), np.linspace(0.0, 3000.0, 5))
    sl = [(1500.0, 1500.0, 0.0)]
    def icd(gamma, c):
        return 45.0  # generische cd im Test
    feld_10 = _lux_feld(gx, gy, sl, icd, 1.0)
    feld_08 = _lux_feld(gx, gy, sl, icd, 0.8)
    assert np.array_equal(feld_08, feld_10 * 0.8)   # WF = einziger linearer Skalar

    class _Anf:
        def __init__(self, wf):
            if wf is not None:
                self.wartungsfaktor = wf

    class _Raum:
        raum_typ, ist_fluchtweg = "GANG", True

    class _Norm:
        def __init__(self, wf):
            self._wf = wf

        def fuer_raum(self, raum_typ, ist_fluchtweg):
            return _Anf(self._wf)

    assert _wf(_Raum(), _Norm(0.57)) == 0.57       # genau das Norm-Feld
    assert _wf(_Raum(), _Norm(None)) == 1.0        # Fallback ohne Feld


def test_deckung_wf_aus_norm():
    """F02 / W09: Der Wartungsfaktor kommt aus EINER Funktion (`wartungsfaktor_aus_norm`)
    statt je eigenem inline-getattr in Deckung/Fachpraxis/Nachweis/Bericht. Exakte Werte,
    Fallback 1,0 (fehlend ODER falsy)."""
    from notbeleuchtung.platzierung.lux import wartungsfaktor_aus_norm

    class _Anf:
        wartungsfaktor = 0.57

    class _AnfNull:
        wartungsfaktor = 0.0

    class _AnfOhne:
        pass

    assert wartungsfaktor_aus_norm(_Anf()) == 0.57
    assert wartungsfaktor_aus_norm(_AnfOhne()) == 1.0   # Feld fehlt → kein MF
    assert wartungsfaktor_aus_norm(_AnfNull()) == 1.0   # 0 falsy → Fallback
    assert isinstance(wartungsfaktor_aus_norm(_Anf()), float)


def test_toiletten_scope_single_source():
    """F05 / W10: Toiletten-Scope §4.3.8 kommt aus EINER Quelle (`bausteine`); die
    vorher dreifach hartkodierten Sets sind weg. Exakte Werte, disjunkt, gleiche Identität
    in beiden Konsumenten (kein kopiertes Set)."""
    from notbeleuchtung.platzierung import bausteine
    from notbeleuchtung.platzierung import sonderstellen_strategy as ss

    assert bausteine.TOILETTE_EINDEUTIG == {"WC", "TOILETTE"}
    assert bausteine.TOILETTE_MEHRDEUTIG == {"SANITAER", "SANITÄR", "BAD", "DUSCHE", "NASSRAUM"}
    assert bausteine.TOILETTE_EINDEUTIG.isdisjoint(bausteine.TOILETTE_MEHRDEUTIG)
    # sonderstellen_strategy konsumiert dasselbe Objekt (Alias, keine Kopie).
    assert ss._TOILETTEN_TYPEN is bausteine.TOILETTE_EINDEUTIG


def test_getrennter_kreis_hardstop():
    """F06 / W13: Ein Symbol ohne F13-SV-Kreis ist ein Hard-Stop (fehler), kein Warnhinweis;
    mit F13 bleibt die Regel 'ok'. Exakte Status-Assertion + gesamtstatus."""
    from notbeleuchtung.hauptengine.contracts import (
        BBox,
        Platzierung,
        PlatzierungsErgebnis,
        RaumModell,
    )
    from notbeleuchtung.hauptengine.validierung import gesamtstatus, pruefe

    raum = RaumModell(floor="X", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(1000.0, 1000.0)))

    def _pruefe(circuit):
        p = Platzierung(xy_mm=(0.0, 0.0), catalog_key="k", kind="rz",
                        height_mm=2400.0, circuit_hint=circuit)
        return pruefe(raum, PlatzierungsErgebnis(floor="X", platzierungen=[p]))

    ohne = _pruefe("AGV-A-F5")
    kreis_ohne = next(b for b in ohne if "Sicherheitskreis" in b.regel)
    assert kreis_ohne.status == "fehler"
    assert gesamtstatus(ohne) == "fehler"

    mit = _pruefe("AGV-A-F13")
    kreis_mit = next(b for b in mit if "Sicherheitskreis" in b.regel)
    assert kreis_mit.status == "ok"


def test_f03_rotation_zur_tuer_ein_helper():
    """F03 / W16: die 4× duplizierte Pfeil-Rotationsformel lebt jetzt in einem Helper.
    Exakte Kardinal-Werte (unten-Block-Basis, atan2+90 auf 90° gerastert)."""
    from notbeleuchtung.platzierung.bausteine import rotation_zur_tuer as r
    assert r(1.0, 0.0) == 90.0     # Ziel rechts
    assert r(0.0, 1.0) == 180.0    # Ziel oben
    assert r(-1.0, 0.0) == 270.0   # Ziel links
    assert r(0.0, -1.0) == 0.0     # Ziel unten
