"""ausgaenge — final_exit/stair_exit aus typisierten Türen."""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.ausgaenge import leite_ausgaenge
from notbeleuchtung.raumerkennung.tuer_zuordnung import AUSSEN

RAEUME = [Raum(id="gang", raum_typ="GANG"), Raum(id="stgh", raum_typ="STIEGENHAUS"),
          Raum(id="zi", raum_typ="ZIMMER")]


def _t(tid, von, nach, detail=None, notaus=False):
    return Tuer(id=tid, xy_mm=(0.0, 0.0), von_raum=von, nach_raum=nach,
                tuer_detail=detail, ist_notausgang=notaus)


def test_final_exit_nur_im_eg():
    tueren = [_t("t1", AUSSEN, "gang", "hauseingang"),
              _t("t2", AUSSEN, "gang", None, notaus=True)]
    out, warn = leite_ausgaenge(tueren, RAEUME, "EG")
    assert [(a.id, a.typ) for a in out] == [("exit_t1", "final_exit"),
                                           ("exit_t2", "final_exit")]
    assert warn == []
    out_og, warn_og = leite_ausgaenge(tueren, RAEUME, "OG3")
    assert out_og == []
    assert warn_og and warn_og[0].gescheiterte_regeln


def test_stair_exit_aus_stiegenhaustuer():
    tueren = [_t("t1", "gang", "stgh", "stiegenhaustuer"),
              # Wohnungseingang direkt ins Stiegenhaus ist KEIN Geschossausgang.
              _t("t2", "zi", "stgh", "wohnungseingang")]
    out, _ = leite_ausgaenge(tueren, RAEUME, "OG3")
    assert [(a.id, a.typ) for a in out] == [("exit_t1", "stair_exit")]


def test_warnung_bei_keinem_ausgang():
    out, warn = leite_ausgaenge([_t("t1", "zi", "gang", "wohnungseingang")],
                                RAEUME, "EG")
    assert out == [] and len(warn) == 1
    assert warn[0].geschoss == "EG"
    assert len(warn[0].gescheiterte_regeln) == 2
