"""Sonderstellen-Contract-Vorschlag — die Fachaussagen, bevor entschieden wird.

Der Vorschlag ist hier ausführbar, damit über ihn nicht auf dem Papier entschieden
werden muss: die Tests zeigen, welche Regeln er freischaltet, wo er fail closed
bleibt und welche Zahl er ausdrücklich **nicht** als Normwert ausgibt.

Kein Contract ist verändert (`hauptengine/contracts/**` unberührt).
"""
import pytest

from notbeleuchtung.normwissen import (
    PlatzierungsRegelwerk,
    Sonderstelle,
    SonderstellenKatalog,
)
from notbeleuchtung.normwissen.platzierungsregeln import MANUELL_PRUEFEN

K = SonderstellenKatalog()
M = PlatzierungsRegelwerk()


def _stelle(typ: str, **kw) -> Sonderstelle:
    daten = {"id": f"{typ}-1", "typ": typ, "xy_mm": (1000.0, 2000.0)}
    daten.update(kw)
    return Sonderstelle(**daten)


# ── Die geforderten Fälle ───────────────────────────────────────────────────
def test_feuerloescher_aktiviert_seine_regel():
    befund = K.bewerte([_stelle("feuerloescher")])
    assert "SL-06-FEUERLOESCHER" in befund.aktivierte_regeln
    assert K.leuchtenart("feuerloescher") == "sicherheitsleuchte"
    assert K.max_abstand_mm("feuerloescher") == 2000


def test_wandhydrant_ist_eine_eigene_stelle():
    """Die LB nennt Feuerlöscher und Wandhydrant in einem Satz — es sind aber zwei
    Geräte an zwei Orten, jedes mit eigener 2-m-Umgebung."""
    befund = K.bewerte([_stelle("feuerloescher"), _stelle("hydrant")])
    assert set(befund.aktivierte_regeln) == {"SL-06-FEUERLOESCHER", "SL-07-WANDHYDRANT"}
    assert K.eintrag("hydrant")["nicht_zusammenfassen_mit"] == "feuerloescher"


def test_erste_hilfe_ist_eine_eigene_stelle():
    befund = K.bewerte([_stelle("erste_hilfe")])
    assert befund.aktivierte_regeln == ["SL-05-ERSTE-HILFE-STELLE"]
    assert K.beleg("erste_hilfe") == "BELEGT"


def test_unbekannter_typ_geht_in_den_review_statt_verworfen_zu_werden():
    """Eine still verworfene Sonderstelle ist eine verlorene Pflichtstelle."""
    befund = K.bewerte([{"id": "X-1", "typ": "sprinkler", "xy_mm": (0.0, 0.0)}])
    assert befund.aktivierte_regeln == []
    assert befund.blockierend
    assert any("unbekannter Sonderstellen-Typ" in r for r in befund.review)


def test_fehlende_position_geht_in_den_review():
    """Ohne Koordinate ist die 2-m-Regel aus §4.1.2 nicht prüfbar."""
    befund = K.bewerte([{"id": "HY-1", "typ": "hydrant"}])
    assert befund.aktivierte_regeln == []
    assert any("ohne Position" in r for r in befund.review)


def test_projekt_lb_liefert_den_lux_wert_die_norm_die_pflicht():
    """Arbeitsteilung: §4.1.2 begründet die Leuchte, die LB beziffert sie.

    Die LB kann eine Sonderstelle NICHT erzeugen — `SonderLux` trägt `ort` und
    `min_lux`, aber keine Koordinate."""
    assert K.lb_lux("feuerloescher") == 5.0
    assert K.lb_lux("hydrant") == 5.0
    assert "sonder_lux" in K.eintrag("feuerloescher")["lux_anforderung"]["lb_quelle"]
    assert K.heute_erkennbar("elektro_lb_ohne_position") is True
    assert not K.typ_ist_heute_automatisch_erkennbar("feuerloescher")


def test_hard_stops_bleiben_uebergeordnet():
    """Der Vorschlag rührt die unübersteuerbaren Grenzen nicht an: eine Sonderstelle
    erzeugt eine Leuchte, aber Montagehöhe und Betriebsdauer gelten unverändert."""
    stops = {h.id for h in M.hard_stops()}
    assert {"HS-01-MONTAGEHOEHE", "HS-02-BETRIEBSDAUER"} <= stops
    for rid in K.wuerde_freischalten():
        regel = M.regel(rid)
        assert M.rang(regel.decision_source) < M.rang("hard_stop")


# ── Die Zahl, die kein Normwert ist ─────────────────────────────────────────
def test_5lx_wird_nie_als_normwert_ausgegeben():
    """Der Kernfehler, den dieser Katalog verhindern soll: §4.1.2 belegt die
    Hervorhebungspflicht, nennt aber kein Beleuchtungsniveau. Die 5 lx stammen aus
    einer Projekt-LB."""
    for typ in ("feuerloescher", "hydrant"):
        assert K.norm_lux(typ) is None, f"{typ}: es gibt keinen belegten Norm-Lux-Wert"
        assert K.lux_ist_ungeklaert(typ)
        # Der Wert existiert — aber ausschliesslich mit LB-Herkunft.
        assert K.lb_lux(typ) == 5.0
        assert "LB" in K.eintrag(typ)["lux_anforderung"]["lb_quelle"]
    # Die Pflicht bleibt trotzdem bestehen — sie hängt nicht am Lux-Wert.
    befund = K.bewerte([_stelle("feuerloescher")])
    assert "SL-06-FEUERLOESCHER" in befund.aktivierte_regeln
    assert any(MANUELL_PRUEFEN in r for r in befund.review)


def test_kein_typ_hat_heute_einen_belegten_norm_lux_wert():
    assert all(K.norm_lux(t) is None for t in K.typen())


# ── Zuschnitt des Vorschlags ────────────────────────────────────────────────
def test_vorschlag_schaltet_genau_die_blockierten_regeln_frei():
    blockiert = {r.id for r in M.blockiert_durch_contract()}
    assert K.wuerde_freischalten() == blockiert, (
        "der Vorschlag soll die Contract-Lücke exakt schließen — nicht weniger "
        "(Lücke bliebe) und nicht mehr (Feld ohne Bedarf)")


def test_kein_typ_ohne_regel():
    """Aufnahme-Regel: ein Typ steht nur im Katalog, wenn eine Regel ihn braucht."""
    for typ in K.typen():
        assert K.eintrag(typ)["aktiviert_regeln"], typ


def test_raumeigenschaften_sind_keine_punkte():
    """Barrierefreiheit (§4.3.8) und besondere Gefährdung (§4.4.1) hängen an einem
    Raum bzw. einer Fläche — ein Punkt-Modell könnte sie nicht ausdrücken."""
    attribute = K.raum_attribute()
    assert set(attribute) == {"ist_barrierefrei", "besondere_gefaehrdung"}
    assert set(attribute) & set(K.typen()) == set()
    assert attribute["besondere_gefaehrdung"]["offen"], "Teilflächen-Gefährdung bleibt offen"


def test_jede_genannte_regel_id_existiert_in_der_matrix():
    for rid in K.wuerde_freischalten():
        M.regel(rid)


# ── Datenquellen: nichts als automatisch erkennbar behaupten ────────────────
def test_kein_typ_ist_heute_automatisch_erkennbar():
    """Ehrlichkeits-Invariante. Der Architekturplan führt keine Sonderstellen
    (an Mollgasse geprüft), die LB kennt keine Koordinaten, und einen bestückten
    Elektroplan gibt es im Repo nicht — es existiert also kein erprobter Parser."""
    assert not any(K.typ_ist_heute_automatisch_erkennbar(t) for t in K.typen())


def test_architekturplan_ist_als_nicht_tragfaehig_markiert():
    assert K.heute_erkennbar("architektur_dxf_heute") is False
    assert K.heute_erkennbar("elektroplan_kuenftig") is False
    assert K.heute_erkennbar("manuell") is True


def test_beobachtetes_symbol_ohne_regel_wird_nicht_aufgenommen():
    """Die Notrufsprechstelle steht im professionellen Plan, aber keine Regel
    braucht sie — also ist sie kein Typ, sondern eine Notiz."""
    beobachtet = K._cfg["beobachtet_ohne_regel"]
    assert beobachtet and "Notrufstelle" in beobachtet[0]["symbol"]
    assert "notrufstelle" not in K.typen()


def test_unbekannter_typ_im_katalog_wirft():
    with pytest.raises(KeyError):
        K.eintrag("gibts_nicht")
