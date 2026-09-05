"""Lux-Nachweis: die C-Ebene der Photometrie darf nicht verloren gehen.

Befund vom 05.09.2026: `hauptengine/registry.py::photometrie_i_cd_fn` gab
`lambda gamma: photometrie.intensitaet(gamma)` zurück — der zweite Parameter
blieb auf **0°**. Der Lux-Nachweis rechnete damit jeden Rasterpunkt in der
**C0-Ebene**. Für die Fluchtweg-Default-Leuchte (Corridor-Optik) ist C0 die
stärkste Richtung: bei γ = 60° stehen 149,93 cd gegen 19,53 cd in C90 — ein Punkt
mit tatsächlich 0,39 lx wurde als 3,00 lx gerechnet und bestand einen
1-lx-Grenzwert, den er nicht erfüllt.

⚠️ Betrifft `platzierung/lux.py` (@mvpo3) und `hauptengine/registry.py`
(Integration) — bitte mit reviewen.
"""
from __future__ import annotations

import math

import pytest

from notbeleuchtung.hauptengine.registry import photometrie_i_cd_fn
from notbeleuchtung.normwissen.photometrie import lade_ldt
from notbeleuchtung.platzierung.lux import lux_punkte
from notbeleuchtung.symbols.photometrie_katalog import fluchtweg_default_ldt

H_M = 2.5
GAMMA = 60.0
#: Punktabstand in mm, der genau γ = 60° ergibt (Engine rechnet in mm).
D_MM = H_M * 1000.0 * math.tan(math.radians(GAMMA))


def _corridor():
    pfad = fluchtweg_default_ldt()
    if pfad is None:
        pytest.skip("Photometrie-Katalog nicht vorhanden")
    return pfad


def _e(i_cd_fn, punkt) -> float:
    return lux_punkte([(0.0, 0.0)], [punkt], montagehoehe_m=H_M,
                      i_cd_fn=i_cd_fn, ziel_lux=1.0).min_lux


# ── Anisotrope Optik reagiert auf Richtung ──────────────────────────────────
def test_anisotrope_optik_haengt_von_der_richtung_ab():
    """Gleicher γ, andere C-Ebene → anderer Wert. Vorher waren beide gleich."""
    photo = lade_ldt(str(_corridor()))
    assert not photo.ist_rotationssymmetrisch()
    # Mit zugesicherter Ausrichtung (C0 nach +x) rechnet die Engine die echte Ebene.
    fn = photometrie_i_cd_fn(_corridor(), c0_azimut_grad=0.0)
    e_c0 = _e(fn, (D_MM, 0.0))
    e_c90 = _e(fn, (0.0, D_MM))
    assert e_c0 > e_c90 * 5, f"C0 {e_c0:.3f} lx vs C90 {e_c90:.3f} lx — kaum Unterschied"
    # Gegenprobe zur reinen Photometrie.
    cos3 = math.cos(math.radians(GAMMA)) ** 3
    assert e_c90 == pytest.approx(photo.intensitaet(GAMMA, 90.0) * cos3 / H_M**2, rel=1e-6)


def test_drehung_der_optik_aendert_das_ergebnis():
    """Dieselbe Leuchte, um 90° gedreht → der C0-Punkt wird zum C90-Punkt."""
    ungedreht = photometrie_i_cd_fn(_corridor(), c0_azimut_grad=0.0)
    gedreht = photometrie_i_cd_fn(_corridor(), c0_azimut_grad=90.0)
    assert _e(ungedreht, (D_MM, 0.0)) == pytest.approx(_e(gedreht, (0.0, D_MM)), rel=1e-6)
    assert _e(ungedreht, (D_MM, 0.0)) > _e(gedreht, (D_MM, 0.0)) * 5


# ── Rotationssymmetrische Optik bleibt unverändert ──────────────────────────
def test_rotationssymmetrische_optik_unveraendert():
    """Die Rundlinse ist an den Daten geprüft rotationssymmetrisch — Richtung und
    Drehung dürfen dort nichts ändern (keine Regression für bestehende Pläne)."""
    pfad = _corridor().with_name("sl_nlkbu433_3h_round.ldt")
    if not pfad.exists():
        pytest.skip("Rundlinsen-LDT nicht vorhanden")
    photo = lade_ldt(str(pfad))
    assert photo.ist_rotationssymmetrisch()
    fn = photometrie_i_cd_fn(pfad)
    assert getattr(fn, "rotationssymmetrisch", None) is True
    e_x, e_y = _e(fn, (D_MM, 0.0)), _e(fn, (0.0, D_MM))
    assert e_x == pytest.approx(e_y, rel=1e-9)
    cos3 = math.cos(math.radians(GAMMA)) ** 3
    assert e_x == pytest.approx(photo.intensitaet(GAMMA) * cos3 / H_M**2, rel=1e-6)


# ── Der falsche positive Nachweis ist verhindert ────────────────────────────
def test_reproduzierter_falscher_nachweis_wird_verhindert():
    """Der Punkt in C90-Richtung erfüllt 1 lx NICHT. Vorher meldete der
    produktive Pfad 2,999 lx (C0-Annahme) und ließ ihn bestehen."""
    photo = lade_ldt(str(_corridor()))
    cos3 = math.cos(math.radians(GAMMA)) ** 3
    e_wahr = photo.intensitaet(GAMMA, 90.0) * cos3 / H_M**2
    e_c0_annahme = photo.intensitaet(GAMMA, 0.0) * cos3 / H_M**2
    assert e_wahr < 1.0 < e_c0_annahme          # genau die Falle

    # Ohne zugesicherte Ausrichtung: konservativ (kleinste Lichtstärke über C).
    fn = photometrie_i_cd_fn(_corridor())
    ergebnis = lux_punkte([(0.0, 0.0)], [(0.0, D_MM)], montagehoehe_m=H_M,
                          i_cd_fn=fn, ziel_lux=1.0)
    assert ergebnis.erfuellt_min is False, "1 lx dürfen hier nicht bestehen"
    assert ergebnis.min_lux <= e_wahr + 1e-9    # unterschätzt nie

    # Mit zugesicherter Ausrichtung ebenfalls nicht bestanden.
    fn_ausgerichtet = photometrie_i_cd_fn(_corridor(), c0_azimut_grad=0.0)
    assert lux_punkte([(0.0, 0.0)], [(0.0, D_MM)], montagehoehe_m=H_M,
                      i_cd_fn=fn_ausgerichtet, ziel_lux=1.0).erfuellt_min is False


def test_konservativer_zweig_ist_kein_mittelwert_und_kein_fester_c_winkel():
    photo = lade_ldt(str(_corridor()))
    fn = photometrie_i_cd_fn(_corridor())
    werte = [photo.intensitaet(GAMMA, c) for c in range(0, 360, 15)]
    assert fn(GAMMA) == pytest.approx(photo.min_intensitaet(GAMMA), rel=1e-9)
    assert fn(GAMMA) < sum(werte) / len(werte)      # kein Mittelwert
    assert fn(GAMMA) < photo.intensitaet(GAMMA, 0.0)  # kein fester C0


# ── Fehlende Daten erzeugen keinen behaupteten Nachweis ─────────────────────
def test_fehlende_ausrichtung_wird_als_unvollstaendig_ausgewiesen():
    """Ohne zugesicherte Optik-Ausrichtung wird konservativ gerechnet — und das
    Callable sagt es, damit der Plan es nicht als vollen Nachweis führt."""
    fn = photometrie_i_cd_fn(_corridor())
    assert getattr(fn, "rotationssymmetrisch", None) is False
    hinweis = getattr(fn, "hinweis", "")
    assert "NICHT zugesichert" in hinweis
    assert "kein vollständiger Nachweis" in hinweis
    assert "CAD-Symbol-Rotation" in hinweis


def test_fehlende_photometrie_erzeugt_keinen_nachweis():
    """Kein stiller Rückfall: eine fehlende LDT bricht ab."""
    with pytest.raises((FileNotFoundError, OSError)):
        photometrie_i_cd_fn(_corridor().with_name("gibt_es_nicht.ldt"))


def test_altes_einparametriges_callable_bleibt_nutzbar():
    """Fakes/Tests mit `i_cd_fn(γ)` dürfen nicht brechen."""
    e = _e(lambda gamma: 200.0, (D_MM, 0.0))
    cos3 = math.cos(math.radians(GAMMA)) ** 3
    assert e == pytest.approx(200.0 * cos3 / H_M**2, rel=1e-9)
