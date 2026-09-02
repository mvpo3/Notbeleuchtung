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


def test_lb_wiederholt_den_normwert_und_erzeugt_trotzdem_keine_stelle():
    """Die LB nennt dieselben 5 lx wie §4.1.2 i) — sie begründet sie nicht.

    Unabhängig davon kann die LB eine Sonderstelle NICHT erzeugen: `SonderLux`
    trägt `ort` und `min_lux`, aber keine Koordinate."""
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


# ── Die 5 lx: belegt, aber vertikal ─────────────────────────────────────────
def test_5lx_sind_ein_normwert_aber_vertikal():
    """Korrektur vom 01.09.2026. §4.1.2 h) und i) nennen den Wert ausdrücklich:
    „so dass 5 lx vertikale Beleuchtungsstärke … erreicht werden".

    Die frühere Annahme (§4.1.2 fordere nur die Betonung, die 5 lx stammten aus
    der Projekt-LB) beruhte auf einer unvollständigen Extraktion. Entscheidend
    bleibt die Bezugsfläche: der Wert ist **vertikal am Gerät** und darf nicht
    als horizontales `min_lux` in den Bodenraster laufen.
    """
    for typ in ("feuerloescher", "hydrant", "erste_hilfe", "brandmelder"):
        assert K.norm_lux_vertikal(typ) == 5.0
        assert K.norm_lux_bezugsflaeche(typ) == "vertikal"
        assert not K.lux_ist_ungeklaert(typ)
        assert "§4.1.2" in K.eintrag(typ)["lux_anforderung"]["norm_quelle"]


def test_horizontaler_normwert_bleibt_fuer_jeden_typ_leer():
    """Die Engine rechnet den Lux-Nachweis horizontal am Boden. Fuer diese
    Stellen gibt EN 1838 dort **nichts** her — lieber `None` als eine stille
    Umdeutung des Vertikalwerts (derselbe Kategorienfehler wie Ud gegen Uo)."""
    assert all(K.norm_lux_horizontal(t) is None for t in K.typen())


def test_niveauaenderung_bleibt_ohne_lux_wert():
    """§4.1.2 c) („nahe jeder anderen Niveauänderung") belegt die Pflicht, nennt
    aber — anders als h) und i) — kein Beleuchtungsniveau."""
    assert K.norm_lux_vertikal("niveauaenderung") is None
    assert K.lux_ist_ungeklaert("niveauaenderung")
    befund = K.bewerte([_stelle("niveauaenderung")])
    assert "SL-04-NIVEAUAENDERUNG" in befund.aktivierte_regeln
    assert any(MANUELL_PRUEFEN in r for r in befund.review)


def test_belegte_stelle_erzeugt_keinen_lux_review_mehr():
    """Gegenprobe: wo der Norm-Wert jetzt belegt ist, darf kein Lux-Review mehr
    entstehen — die Pflicht selbst bleibt davon unberührt."""
    befund = K.bewerte([_stelle("feuerloescher")])
    assert "SL-06-FEUERLOESCHER" in befund.aktivierte_regeln
    assert not any("Lux-Niveau" in r for r in befund.review)


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
