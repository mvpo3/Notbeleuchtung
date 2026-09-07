"""tuer_typisierung — Regelkette + Geschoss-Helper."""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.tuer_typisierung import (
    geschoss_aus,
    ist_erdgeschoss,
    ist_obergeschoss,
    typisiere_tueren,
)
from notbeleuchtung.raumerkennung.tuer_zuordnung import AUSSEN

RAEUME = [
    Raum(id="gang", raum_typ="GANG"),
    Raum(id="stgh", raum_typ="STIEGENHAUS"),
    Raum(id="zi1", raum_typ="ZIMMER"),
    Raum(id="zi2", raum_typ="SCHLAFZIMMER"),
    Raum(id="gar1", raum_typ="GARAGE"),
    Raum(id="gar2", raum_typ="GARAGE"),
]


def _t(von, nach, breite=900.0, **kw):
    return Tuer(id="t", xy_mm=(0.0, 0.0), breite_mm=breite,
                von_raum=von, nach_raum=nach, **kw)


def _detail(tuer, geschoss="EG", **kw):
    typisiere_tueren([tuer], RAEUME, geschoss, **kw)
    return tuer.tuer_detail


def test_geschoss_aus():
    assert geschoss_aus("OG3", None) == "OG3"
    assert geschoss_aus(None, "Projekte/OG3 - Rennweg 15.dxf") == "OG3"
    assert geschoss_aus(None, "Erdgeschoss_EG.dxf") == "EG"
    assert geschoss_aus(None, None) == ""
    assert ist_erdgeschoss("EG") and not ist_erdgeschoss("OG3")
    assert ist_obergeschoss("OG3") and not ist_obergeschoss("EG")


def test_hauseingang_nur_im_eg():
    assert _detail(_t(AUSSEN, "gang")) == "hauseingang"
    assert _detail(_t(AUSSEN, "gang"), geschoss="OG3") is None


def test_notausgang_zusatz_doppelfluegel_und_flw_ende():
    t = _t(AUSSEN, "gang", breite=1800)          # Doppelflügel > 1.4 m
    _detail(t)
    assert t.ist_notausgang
    t2 = _t(AUSSEN, "gang")
    _detail(t2, fluchtweg_enden=[(200.0, 0.0)])  # FLW-Linie endet an der Tür
    assert t2.ist_notausgang


def test_balkontuer_nie_ausgang():
    t = _t(AUSSEN, "zi1", ist_notausgang=True)
    assert _detail(t) == "balkontuer" and not t.ist_notausgang


def test_stiegenhaus_seiten():
    assert _detail(_t("stgh", "zi1")) == "wohnungseingang"
    assert _detail(_t("stgh", "gang")) == "stiegenhaustuer"


def test_zimmer_und_wohnungseingang():
    assert _detail(_t("zi1", "zi2")) == "zimmertuer"
    assert _detail(_t("gang", "zi1")) == "wohnungseingang"


def test_garagentor_und_brandschutz():
    assert _detail(_t("gar1", "gar2", breite=2500)) == "garagentor"
    assert _detail(_t("gar1", "gar2", breite=1000)) is None
    # Brandschutz nur für sonst untypisierte Türen (Ketten-Priorität).
    assert _detail(_t("gar1", "gar2", breite=1000),
                   brandschutz_hinweise=[(100.0, 0.0)]) == "brandschutztuer"
    assert _detail(_t("gang", "zi1"),
                   brandschutz_hinweise=[(100.0, 0.0)]) == "wohnungseingang"
