"""Placement-Decision-Matrix — die fachlichen Entscheidungen, festgenagelt.

Diese Tests prüfen keine Mechanik, sondern **Fachaussagen**: dass ein Ausgang ein
Rettungszeichen auslöst, dass eine Treppe zusätzlich beleuchtet wird, dass ein
5-lx-Wert am Feuerlöscher als LB-Wert und nicht als Norm-Wert geführt wird, und
dass unklare Fälle in den Review gehen statt in einen stillen Default.

Sie sind damit auch das Gitter gegen die zwei Fehlerarten, die in diesem Projekt
schon real aufgetreten sind: eine erfundene Zahl, die als Norm-Wert durchgeht, und
eine erkannte Anforderung, die still verloren geht.
"""
import pytest

from notbeleuchtung.normwissen import PlatzierungsRegelwerk
from notbeleuchtung.normwissen.platzierungsregeln import MANUELL_PRUEFEN

W = PlatzierungsRegelwerk()


# ── Rettungszeichen ─────────────────────────────────────────────────────────
def test_ausgang_erzeugt_rettungszeichen():
    """Notausgang und letzter Ausgang ins Freie sind die höchstpriorisierten
    RZ-Anker (EN 1838 §4.1.2, Coverage-Schritt 1)."""
    for rid in ("RZ-01-NOTAUSGANG", "RZ-02-AUSGANG-INS-FREIE", "RZ-07-AUSGANG-STIEGENHAUS"):
        r = W.regel(rid)
        assert r.leuchtenart == "rz"
        assert r.prioritaet == 1, "Ausgänge werden zuerst bestückt"
        assert r.erzeugt_leuchte


def test_letzter_ausgang_weist_nicht_weiter():
    """Am Ausgang ins Freie ist das Ziel erreicht — Pfeil nach unten, keine
    Richtungsvariante."""
    r = W.regel("RZ-02-AUSGANG-INS-FREIE")
    assert "unten" in r.orientierung


def test_richtungsaenderung_erzeugt_richtungszeichen():
    r = W.regel("RZ-03-RICHTUNGSAENDERUNG")
    assert r.leuchtenart == "rz"
    assert "links" in r.orientierung and "rechts" in r.orientierung
    assert r.abstand["max_horizontal_zum_punkt_mm"] == 2000


def test_kreuzung_erzeugt_rettungszeichen_und_sicherheitsleuchte():
    """Das Zeichen weist, die Leuchte beleuchtet — an derselben Kreuzung beides."""
    assert W.regel("RZ-04-KREUZUNG").leuchtenart == "rz"
    assert W.regel("SL-03-KREUZUNG").leuchtenart == "sicherheitsleuchte"


def test_nicht_jede_tuer_bekommt_ein_rettungszeichen():
    """Abgrenzungsregel: die Coverage-Reihenfolge nennt Türen ins Freie und
    Stiegenhaustüren — nicht jede Wohnungstür. Eine RZ je Tür wäre erfunden."""
    r = W.regel("RZ-08-TUER-AM-FLUCHTWEG")
    assert r.leuchtenart == "keine"
    assert not r.erzeugt_leuchte


def test_sichtachse_folgt_der_erkennungsweite_formel():
    """Der 30-m-Default ist l = z·h mit z=200 (hinterleuchtet) und h=0,15 m —
    keine freie Zahl."""
    a = W.regel("RZ-09-SICHTACHSE-AUFFUELLEN").abstand
    assert a["formel"] == "l = z * h"
    assert a["default_max_sichtachse_m"] == 30
    assert "en1838_grundwerte" in a["z_ref"] and "en1838_grundwerte" in a["h_ref"]


# ── Sicherheitsleuchten ─────────────────────────────────────────────────────
def test_treppe_erzeugt_sicherheitsbeleuchtung():
    """EN 1838 §4.1.2 b): nahe Treppen, um jede Stufe direkt zu beleuchten."""
    r = W.regel("SL-02-TREPPE")
    assert r.leuchtenart == "sicherheitsleuchte"
    assert r.beleg == "BELEGT"
    assert r.abstand["max_horizontal_zum_punkt_mm"] == 2000
    assert r.norm_ref.startswith("ÖNORM EN 1838")


def test_treppen_rz_ersetzt_die_sicherheitsleuchte_nicht():
    assert "ersetzt" in W.regel("RZ-05-TREPPE").konfliktregel


def test_feuerloescher_5lx_ist_ein_lb_wert_kein_normwert():
    """Der kritische Fall: 5 lx am Feuerlöscher stehen in der realen Elektro-LB,
    NICHT in EN 1838. Die Betonungspflicht ist belegt, der Lux-Wert nicht — also
    wird er als LB-Wert geführt und der fehlende Norm-Beleg bleibt sichtbar."""
    r = W.regel("SL-06-FEUERLOESCHER")
    assert r.abstand["min_lux_lb_typisch"] == 5.0
    assert "kein Norm-Default" in r.abstand["min_lux_quelle"]
    assert MANUELL_PRUEFEN in r.norm_ref
    assert r.review_erforderlich is True
    # Die Leuchte selbst bleibt trotzdem Pflicht (§4.1.2), nur ihr Lux-Niveau ist offen.
    assert r.leuchtenart == "sicherheitsleuchte"
    assert r.abstand["max_horizontal_zum_punkt_mm"] == 2000


def test_wandhydrant_ist_eine_eigene_stelle():
    """Die LB nennt Feuerlöscher und Wandhydrant in einem Satz — der Platzierer
    verankert aber an jedem Gerät einzeln."""
    r = W.regel("SL-07-WANDHYDRANT")
    assert r.leuchtenart == "sicherheitsleuchte"
    assert r.abstand["min_lux_lb_typisch"] == 5.0
    assert "GETRENNTE" in r.konfliktregel


def test_antipanik_ist_eine_flaechenanforderung():
    r = W.regel("SL-09-ANTIPANIK-FLAECHE")
    assert r.leuchtenart == "antipanik"
    assert r.abstand["min_lux_ref"].endswith("lux.antipanik")
    assert "photometrische" in r.konfliktregel.lower()


def test_besondere_gefaehrdung_hat_den_hoechsten_lux_anspruch():
    r = W.regel("SL-11-BESONDERE-GEFAEHRDUNG")
    assert r.abstand["min_lux"] == 15.0
    assert r.abstand["min_prozent_der_arbeitsplatz_beleuchtung"] == 10
    assert r.beleg == "BELEGT"


# ── Fail closed: Unklares wird nicht still entschieden ──────────────────────
def test_unklare_fluchtwegfuehrung_erzeugt_review_statt_leuchte():
    r = W.regel("RZ-11-FLUCHTWEG-UNKLAR")
    assert r.leuchtenart == "keine"
    assert r.review_erforderlich is True
    assert r.decision_source == "hard_stop"
    assert r.prioritaet == 0, "schlägt jede andere RZ-Regel"


def test_widerspruch_wird_nicht_ausgewuerfelt():
    r = W.regel("SL-14-WIDERSPRUCH")
    assert r.leuchtenart == "keine"
    assert r.review_erforderlich is True


def test_gleichstand_hat_keinen_gewinner():
    """Zwei Regeln derselben Quelle und Priorität → `None`. Das heißt Review,
    nicht „irgendeine nehmen"."""
    a, b = W.regel("SL-06-FEUERLOESCHER"), W.regel("SL-07-WANDHYDRANT")
    assert a.decision_source == b.decision_source and a.prioritaet == b.prioritaet
    assert W.gewinner(a, b) is None


# ── Entscheidungs-Hierarchie (CLAUDE.md) ────────────────────────────────────
def test_lb_explizit_uebersteuert_norm_default():
    """Die LB schließt Sicherheitsbeleuchtung im Stiegenhaus aus (Fischa GK4) —
    das übersteuert den Norm-Default, solange keine Pflicht dagegensteht."""
    lb = W.regel("SL-12-GARAGE")                 # decision_source: lb_explizit
    norm = W.regel("SL-01-FLUCHTWEG-MITTELLINIE")  # decision_source: norm_default
    assert W.rang(lb.decision_source) > W.rang(norm.decision_source)
    assert W.gewinner(lb, norm) is lb


def test_hierarchie_reihenfolge_wie_in_claude_md():
    assert (W.rang("hard_stop") > W.rang("lb_explizit")
            > W.rang("referenz_praxis") > W.rang("norm_default"))


def test_normative_pflicht_wird_nicht_durch_fachpraxis_deaktiviert():
    """Ein Hard Stop schlägt Fachpraxis UND explizite LB-Vorgabe."""
    stop = W.regel("RZ-11-FLUCHTWEG-UNKLAR")     # hard_stop
    praxis = W.regel("RZ-10-BEIDSEITIGE-RICHTUNG")  # referenz_praxis
    lb = W.regel("RZ-06-NIVEAUAENDERUNG")        # lb_explizit
    assert W.gewinner(stop, praxis) is stop
    assert W.gewinner(stop, lb) is stop


def test_lb_exklusion_gegen_normative_pflicht_ist_ein_konflikt():
    """Schließt die LB einen Bereich aus, für den der OIB-Befund
    Sicherheitsbeleuchtung fordert, wird weder still verzichtet noch still
    platziert."""
    hs = {h.id: h for h in W.hard_stops()}["HS-03-LB-EXKLUSION-GEGEN-PFLICHT"]
    assert "REVIEW" in hs.aufloesung
    assert "nicht_erforderlich" in hs.hinweis, "fehlender OIB-Befund ist kein Freibrief"


def test_hard_stops_sind_belegt_und_beschreiben_ihre_verletzung():
    for h in W.hard_stops():
        assert h.verletzung, f"{h.id} sagt nicht, was die Verletzung ist"
        assert h.quelle


def test_montagehoehe_und_dauer_verweisen_auf_die_grundwerte():
    """Keine zweite Wahrheit: die Hard Stops tragen keine eigenen Zahlen."""
    stops = {h.id: h for h in W.hard_stops()}
    assert stops["HS-01-MONTAGEHOEHE"].wert_ref.endswith("montagehoehe_min_mm")
    assert stops["HS-02-BETRIEBSDAUER"].wert_ref.endswith("dauer_min")


# ── Invarianten über die ganze Matrix ───────────────────────────────────────
def test_regel_ids_sind_eindeutig():
    ids = [r.id for r in W.alle()]
    assert len(ids) == len(set(ids))


def test_ohne_normbeleg_kein_stiller_norm_default():
    """Die zentrale Ehrlichkeits-Invariante: eine Regel ohne Norm-Fundstelle darf
    nicht als Norm-Default durchgehen. Entweder sie steht auf einer anderen
    Entscheidungs-Stufe (LB/Praxis) oder sie verlangt Review."""
    for r in W.alle():
        if MANUELL_PRUEFEN in r.norm_ref and r.decision_source == "norm_default":
            assert r.review_erforderlich, (
                f"{r.id}: kein Norm-Beleg, aber als Norm-Default ohne Review geführt")


def test_belegte_regeln_nennen_eine_fundstelle():
    for r in W.alle():
        if r.beleg == "BELEGT":
            assert r.norm_ref.startswith("ÖNORM EN 1838"), r.id


def test_input_fehlt_regeln_sind_als_blockiert_gefuehrt():
    """Was die Engine nicht sehen kann, darf sie nicht heuristisch erfinden —
    diese Regeln sind explizit als Contract-blockiert markiert."""
    blockiert = {r.id for r in W.blockiert_durch_contract()}
    assert blockiert, "die Matrix muss die Contract-Lücke sichtbar führen"
    for r in W.alle():
        assert (r.engine_status == "input_fehlt") == (r.id in blockiert)
    # Die Brandschutz-/Erste-Hilfe-Stellen aus EN 1838 §4.1.2 sind der Kern der Lücke.
    assert {"SL-05-ERSTE-HILFE-STELLE", "SL-06-FEUERLOESCHER",
            "SL-07-WANDHYDRANT", "SL-08-BRANDMELDER"} <= blockiert


def test_regeln_ohne_leuchte_erzeugen_nichts():
    for r in W.alle():
        if r.leuchtenart == "keine":
            assert not r.erzeugt_leuchte


def test_unbekannte_regel_id_wirft():
    with pytest.raises(KeyError):
        W.regel("GIBTS-NICHT")
