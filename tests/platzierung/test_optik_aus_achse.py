"""Optik-Ausrichtung aus der Korridor-Achse — der Weg zurück zum vollen Nachweis.

Nach dem C-Ebenen-Fix (#117) rechnete die Engine ohne zugesicherte Optik-
Ausrichtung konservativ (Minimum über alle C-Ebenen) und jeder Corridor-Plan
trug WARNUNG. Diese Naht schließt die Lücke Leonis-seitig: der Fluchtweg-
Verdichter kennt die Korridor-Achse je Leuchte (`leuchten_auf_linie_mit_
richtung`), rechnet den Lux-Nachweis mit der C-Ebene relativ zu dieser
Ausrichtung und schreibt denselben Azimut als Montage-Rotation an die
Platzierung — der Plan selbst ist die Zusicherung.

Naht @EnisAMG: `registry.default_photometrie(optik_aus_achse=True)` +
Befund-Text; `build_default_bundle` hat den Modus per Default an.
"""
from __future__ import annotations

import math

import pytest

from notbeleuchtung.hauptengine.registry import default_photometrie, photometrie_i_cd_fn
from notbeleuchtung.platzierung.lux import lux_punkte
from notbeleuchtung.platzierung.mittellinie import leuchten_auf_linie_mit_richtung

H_M = 2.5
GAMMA = 60.0
D_MM = H_M * 1000.0 * math.tan(math.radians(GAMMA))

#: liegender Gang 20 m × 2 m
GANG = [(0.0, 0.0), (20000.0, 0.0), (20000.0, 2000.0), (0.0, 2000.0)]


def _corridor_ldt():
    from notbeleuchtung.symbols.photometrie_katalog import fluchtweg_default_ldt
    pfad = fluchtweg_default_ldt()
    if pfad is None:
        pytest.skip("Photometrie-Katalog nicht vorhanden")
    return pfad


# ── Achsen-Azimut je Kandidat ───────────────────────────────────────────────
def test_kandidaten_tragen_gang_achse():
    kandidaten = leuchten_auf_linie_mit_richtung(GANG, 8000.0)
    assert kandidaten, "keine Kandidaten auf dem Gang"
    for _x, _y, az in kandidaten:
        # liegender Gang → Tangente längs x (0° oder 180°)
        assert min(az % 180.0, 180.0 - az % 180.0) < 15.0, f"Azimut {az}° quer zum Gang"


# ── Leuchten-Tripel: C-Ebene relativ zur Optik ──────────────────────────────
def test_leuchten_azimut_dreht_die_c_ebene():
    """Leuchte mit Azimut 90° + Punkt in +y = Punkt liegt in der C0-Keule.
    Identisch zur um 90° gedrehten Welt (Gegenprobe zu Enis' Drehungstest)."""
    fn = photometrie_i_cd_fn(_corridor_ldt(), c0_azimut_grad=0.0)
    e_c0_welt = lux_punkte([(0.0, 0.0)], [(D_MM, 0.0)], montagehoehe_m=H_M,
                           i_cd_fn=fn, ziel_lux=1.0).min_lux
    e_azimut = lux_punkte([(0.0, 0.0, 90.0)], [(0.0, D_MM)], montagehoehe_m=H_M,
                          i_cd_fn=fn, ziel_lux=1.0).min_lux
    assert e_azimut == pytest.approx(e_c0_welt, rel=1e-6)
    # Ohne Azimut wäre derselbe Punkt die schwache C90-Richtung.
    e_ohne = lux_punkte([(0.0, 0.0)], [(0.0, D_MM)], montagehoehe_m=H_M,
                        i_cd_fn=fn, ziel_lux=1.0).min_lux
    assert e_azimut > e_ohne * 5


# ── Registry-Naht ───────────────────────────────────────────────────────────
def test_optik_aus_achse_traegt_vollen_nachweis():
    fn, befund = default_photometrie(_corridor_ldt(), optik_aus_achse=True)
    assert befund.vollstaendiger_nachweis is True
    assert befund.ausrichtung_zugesichert is True
    assert befund.status == "ok"
    assert "Korridor-Achse" in befund.hinweis
    assert befund.einschraenkungen == ()
    # Callable rechnet direkt I(γ, C-relativ) …
    assert fn(GAMMA, 0.0) > fn(GAMMA, 90.0) * 5
    # … und bleibt ohne Richtung konservativ (Minimum über C).
    assert fn(GAMMA, None) == pytest.approx(fn(GAMMA, 90.0), rel=0.2)


def test_optik_aus_achse_ohne_ausrichtung_bleibt_konservativ():
    """Ohne den Modus (explizit False) bleibt der #117-Stand: Warnung."""
    _fn, befund = default_photometrie(_corridor_ldt(), optik_aus_achse=False)
    assert befund.vollstaendiger_nachweis is False
    assert befund.status == "warnung"


def test_optik_aus_achse_und_c0_schliessen_sich_aus():
    with pytest.raises(ValueError):
        default_photometrie(_corridor_ldt(), optik_aus_achse=True, c0_azimut_grad=45.0)


# ── Platzierung: Rotation = gerechnete Ausrichtung ──────────────────────────
def test_fluchtweg_sl_rotation_folgt_der_achse():
    from fakes import FakeNormProvider
    from notbeleuchtung.hauptengine.contracts import BBox, Raum, RaumModell
    from notbeleuchtung.platzierung.deckung import verdichte_fluchtweg

    raum = RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(20000.0, 2000.0)),
        raeume=[Raum(id="gang", raum_typ="GANG", polygon_mm=GANG, ist_fluchtweg=True)],
    )
    fn = photometrie_i_cd_fn(_corridor_ldt(), c0_azimut_grad=0.0)
    sls = verdichte_fluchtweg(raum, FakeNormProvider(), i_cd_fn=fn)
    assert sls, "keine SL auf dem Gang"
    for p in sls:
        assert min(p.rotation_deg % 180.0, 180.0 - p.rotation_deg % 180.0) < 15.0, (
            f"SL-Rotation {p.rotation_deg}° folgt nicht der Gang-Achse"
        )
