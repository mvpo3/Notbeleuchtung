"""wohnungsumriss — liegt ein Raum im Umriss einer Wohnung? (Kontrolle, K3)

Umriss = die Räume einer Wohnung samt dem, was zwischen ihnen und der
Gebäudehülle liegt: jeder Nachbarraum bis Wanddicke gehört zu derselben
Wohnung (Schacht/Lift und Freiflächen zählen nicht mit), jede Tür des Raums
führt in diese Wohnung. Die Funktion liest ``wohnung_id`` und setzt nichts.
"""
from __future__ import annotations

import pytest

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.wohnungsumriss import umschliessende_wohnung


def _q(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _r(rid, typ, poly, wohnung=None, klasse=None):
    return Raum(id=rid, raum_typ=typ, polygon_mm=poly, wohnung_id=wohnung,
                nutzungsklasse=klasse)


def _bucht():
    """x in einer Bucht von top_1 an der Fassade (links nichts): unten ZIMMER,
    rechts GANG, oben BAD — Abstände 0 bis 150 mm wie Rennweg OG3."""
    return [_r("x", "", _q(0, 1000, 2000, 3000)),
            _r("zi", "ZIMMER", _q(0, -3000, 5000, 900), "top_1", "WOHNUNG_PRIVAT"),
            _r("gang", "GANG", _q(2000, 1000, 3500, 3000), "top_1", "WOHNUNG_PRIVAT"),
            _r("bad", "BAD", _q(0, 3150, 3500, 5000), "top_1", "WOHNUNG_PRIVAT")]


def test_bucht_an_der_fassade_liegt_im_umriss():
    raeume = _bucht()
    tueren = [Tuer(id="t", xy_mm=(2000.0, 2000.0), von_raum="x", nach_raum="gang")]
    wid, grund = umschliessende_wohnung(raeume[0], raeume, tueren)
    assert wid == "top_1", grund


@pytest.mark.parametrize(("wohnung", "klasse"), [
    ("top_2", "WOHNUNG_PRIVAT"), (None, "ALLGEMEIN_ERSCHLIESSUNG"), (None, None)])
def test_fremder_nachbar_nimmt_aus_dem_umriss(wohnung, klasse):
    raeume = _bucht()
    raeume[2] = _r("gang", "GANG", _q(2000, 1000, 3500, 3000), wohnung, klasse)
    wid, grund = umschliessende_wohnung(raeume[0], raeume, [])
    assert wid is None
    assert "gang" in grund


def test_schacht_lift_und_balkon_zaehlen_nicht():
    raeume = _bucht() + [
        _r("schacht", "SCHACHT", _q(-900, 1000, -100, 2000), None, "KEIN_RAUM"),
        _r("balkon", "BALKON", _q(-3000, 2000, -100, 3000), None, "AUSSEN")]
    assert umschliessende_wohnung(raeume[0], raeume, [])[0] == "top_1"


def test_nachbar_hinter_dicker_wand_zaehlt_nicht():
    raeume = _bucht() + [_r("stgh", "STIEGENHAUS", _q(-3000, 1000, -600, 3000), None,
                            "ALLGEMEIN_ERSCHLIESSUNG")]
    assert umschliessende_wohnung(raeume[0], raeume, [])[0] == "top_1"
    raeume[-1] = _r("stgh", "STIEGENHAUS", _q(-3000, 1000, -400, 3000), None,
                    "ALLGEMEIN_ERSCHLIESSUNG")
    assert umschliessende_wohnung(raeume[0], raeume, [])[0] is None


@pytest.mark.parametrize("andere", ["AUSSEN", "KEIN_RAUM", None])
def test_tuer_aus_der_wohnung_hinaus_nimmt_aus_dem_umriss(andere):
    """Eine Tür ins Freie oder ins Unerkannte: der Raum ist nicht belegt
    wohnungsintern — im Zweifel bleibt er, was er war (Notlicht bleibt)."""
    raeume = _bucht()
    tueren = [Tuer(id="t9", xy_mm=(0.0, 2000.0), von_raum="x", nach_raum=andere)]
    wid, grund = umschliessende_wohnung(raeume[0], raeume, tueren)
    assert wid is None
    assert "t9" in grund


def test_ohne_nachbarn_kein_umriss():
    raeume = [_r("x", "", _q(0, 0, 2000, 2000))]
    assert umschliessende_wohnung(raeume[0], raeume, [])[0] is None
