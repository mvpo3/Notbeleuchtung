"""oib_gate — Geltungsbereich je Raum und je Schwelle (OVE 718.560.9.001.AT).

Umgestellt am 05.09.2026 (Enis, Blocker 2, Schritt 6a): statt eines
projekt-globalen Booleans entscheidet der Scope **je Raum**, und die beiden
Schwellen werden **getrennt** ausgewertet. Drei Zustände: `anwendbar`,
`nicht_anwendbar`, `ungeklaert` — „ungeklärt" ist ausdrücklich nicht
„nicht erforderlich".
"""
from __future__ import annotations

import pytest

from notbeleuchtung.hauptengine.contracts import OibBefund, OibErgebnis, RaumReferenz
from notbeleuchtung.platzierung.oib_gate import (
    gate_summary,
    raeume_ohne_geklaerten_scope,
    raum_zuordnung,
    sanitaer_scope,
    unbekannte_raum_referenzen,
    verkehr_scope,
)


def _erg(stufe: str, i: int = 1, refs: tuple = ()) -> OibErgebnis:
    return OibErgebnis(
        gebaeudeteil_id=f"teil_{i}", stufe=stufe,
        quelle="OIB-RL 2 Tabelle 6", norm_ausgabe="Mai 2023",
        raum_referenzen=[RaumReferenz(floor=f, raum_id=r) for f, r in refs],
    )


def _befund(*eintraege: OibErgebnis) -> OibBefund:
    return OibBefund(ergebnisse=list(eintraege))


# ── 8-m²-Trigger (OVE Punkt 1): raumbezogen ─────────────────────────────────
def test_ohne_oib_pfad_nicht_anwendbar():
    """Ohne OIB-Bewertung stehen die scope-gebundenen Zusatz-Trigger nicht in
    Frage — bestehende Pläne ändern sich dadurch nicht."""
    assert sanitaer_scope(None, "EG", "r1") == "nicht_anwendbar"
    assert verkehr_scope(None, "EG", "r1") == "nicht_anwendbar"


@pytest.mark.parametrize("stufe", ["eingeschraenkt", "uneingeschraenkt"])
def test_bestaetigter_teil_ordnet_seine_raeume_zu(stufe):
    """Frage 1 (räumlich) ist damit beantwortet…"""
    b = _befund(_erg(stufe, refs=(("EG", "r1"),)))
    assert raum_zuordnung(b, "EG", "r1") == "bestaetigt"


@pytest.mark.parametrize("stufe", ["eingeschraenkt", "uneingeschraenkt"])
def test_bestaetigte_zuordnung_macht_die_ove_regel_nicht_anwendbar(stufe):
    """…Frage 2 (fachlich) aber nicht: Tabelle 6 belegt die Erforderlichkeit
    einer Sicherheitsbeleuchtung, nicht die „erhöhten Anforderungen nach der Art
    der Nutzung" der OVE-Klausel. R 12-2 liegt nicht vor → ungeklärt, nicht
    anwendbar."""
    b = _befund(_erg(stufe, refs=(("EG", "r1"),)))
    assert sanitaer_scope(b, "EG", "r1") == "ungeklaert"


def test_bestaetigter_teil_gibt_fremde_raeume_nicht_frei():
    """Der Kern der Korrektur: ein bestätigter Gebäudeteil öffnet keine Räume,
    die er nicht referenziert."""
    b = _befund(_erg("eingeschraenkt", refs=(("EG", "r1"),)))
    assert raum_zuordnung(b, "EG", "r2") == "nicht_bestaetigt"
    assert sanitaer_scope(b, "EG", "r2") == "nicht_anwendbar"
    assert sanitaer_scope(b, "1OG", "r1") == "nicht_anwendbar"


def test_review_required_ist_ungeklaert_nicht_nicht_erforderlich():
    b = _befund(_erg("review_required", refs=(("EG", "r1"),)))
    assert raum_zuordnung(b, "EG", "r1") == "ungeklaert"
    assert sanitaer_scope(b, "EG", "r1") == "ungeklaert"


def test_nicht_erforderlich_ist_nicht_anwendbar():
    b = _befund(_erg("nicht_erforderlich", refs=(("EG", "r1"),)))
    assert raum_zuordnung(b, "EG", "r1") == "nicht_bestaetigt"
    assert sanitaer_scope(b, "EG", "r1") == "nicht_anwendbar"


def test_bestaetigter_teil_ohne_zuordnung_macht_ungeklaert_statt_alles_frei():
    """Früher: Rückfall auf „alle Räume". Jetzt: der Raum ist ungeklärt — weder
    freigegeben noch stillschweigend ausgeschlossen."""
    b = _befund(_erg("eingeschraenkt"))
    assert raum_zuordnung(b, "EG", "r1") == "ungeklaert"
    assert sanitaer_scope(b, "EG", "r1") == "ungeklaert"


def test_gemischte_nutzung_trennt_die_teile():
    """Verkaufsteil bestätigt (mit Zuordnung), Wohnteil review_required (mit
    Zuordnung): jeder Raum bekommt die Aussage SEINES Teils."""
    b = _befund(
        _erg("eingeschraenkt", 1, refs=(("EG", "wc_verkauf"),)),
        _erg("review_required", 2, refs=(("EG", "wc_wohnen"),)),
    )
    assert raum_zuordnung(b, "EG", "wc_verkauf") == "bestaetigt"
    assert raum_zuordnung(b, "EG", "wc_wohnen") == "ungeklaert"
    assert raum_zuordnung(b, "EG", "halle") == "nicht_bestaetigt"
    # Fachlich bleibt selbst der zugeordnete Raum ungeklärt (Nutzungs-Scope).
    assert sanitaer_scope(b, "EG", "wc_verkauf") == "ungeklaert"
    assert sanitaer_scope(b, "EG", "halle") == "nicht_anwendbar"


# ── Widersprüchliche Zuordnung ──────────────────────────────────────────────
def test_bestaetigter_teil_ueberstimmt_einen_ungeklaerten_nicht():
    """Derselbe Raum hängt an zwei Gebäudeteilen mit verschiedenen Ergebnissen.
    Das ist zu klären, nicht stillschweigend zugunsten der Freigabe zu lösen."""
    b = _befund(
        _erg("eingeschraenkt", 1, refs=(("EG", "r1"),)),
        _erg("review_required", 2, refs=(("EG", "r1"),)),
    )
    assert sanitaer_scope(b, "EG", "r1") == "ungeklaert"


def test_bestaetigt_und_verneint_ist_ebenfalls_ungeklaert():
    b = _befund(
        _erg("eingeschraenkt", 1, refs=(("EG", "r1"),)),
        _erg("nicht_erforderlich", 2, refs=(("EG", "r1"),)),
    )
    assert sanitaer_scope(b, "EG", "r1") == "ungeklaert"


def test_zwei_bestaetigende_teile_sind_kein_widerspruch():
    b = _befund(
        _erg("eingeschraenkt", 1, refs=(("EG", "r1"),)),
        _erg("uneingeschraenkt", 2, refs=(("EG", "r1"),)),
    )
    assert raum_zuordnung(b, "EG", "r1") == "bestaetigt"


def test_widerspruch_taucht_als_ungeklaert_im_bericht_auf():
    b = _befund(
        _erg("eingeschraenkt", 1, refs=(("EG", "r1"),)),
        _erg("review_required", 2, refs=(("EG", "r1"),)),
    )
    assert raeume_ohne_geklaerten_scope(b, "EG", ["r1"]) == ["r1"]


# ── Ungültige Raumreferenzen ────────────────────────────────────────────────
def test_referenz_auf_unbekannten_raum_gibt_nichts_frei():
    """Eine ins Leere zeigende Zuordnung darf keine Freigabe erzeugen — und der
    real vorhandene Raum bleibt ohne Zuordnung, also ungeklärt."""
    b = _befund(_erg("eingeschraenkt", refs=(("EG", "gibt_es_nicht"),)))
    assert sanitaer_scope(b, "EG", "r1") == "nicht_anwendbar"
    assert raum_zuordnung(b, "EG", "gibt_es_nicht") == "bestaetigt"  # Raum existiert nicht
    assert unbekannte_raum_referenzen(b, "EG", ["r1"]) == ["gibt_es_nicht"]
    hinweise = " ".join(gate_summary(b, "EG", ["r1"])["hinweise"])
    assert "unbekannte Räume" in hinweise


def test_unbekannte_referenzen_stehen_im_summary():
    b = _befund(_erg("eingeschraenkt", refs=(("EG", "x1"), ("EG", "r1"))))
    block = gate_summary(b, "EG", ["r1"])
    assert block["unbekannte_raum_referenzen"] == ["x1"]
    assert block["raum_zuordnung"]["bestaetigt"] == 1    # r1 bleibt korrekt zugeordnet
    assert block["sanitaer_scope"]["anwendbar"] == 0     # fachlich trotzdem ungeklärt


# ── 60-m²-Trigger (OVE Punkt 3): heute nie anwendbar ────────────────────────
@pytest.mark.parametrize("stufe", ["eingeschraenkt", "uneingeschraenkt", "review_required"])
def test_verkehr_scope_wird_nie_aus_anderen_nutzungen_abgeleitet(stufe):
    """Punkt 3 gilt nur für verkehrstechnische Einrichtungen. Die Nutzungsart ist
    im OibBefund nicht zugesichert (nur Audit-Dict) und die Raumkategorie fehlt
    im RaumModell → nie `anwendbar`, aber auch nicht still „nicht erforderlich"."""
    b = _befund(_erg(stufe, refs=(("EG", "r1"),)))
    assert verkehr_scope(b, "EG", "r1") == "ungeklaert"


# ── Sichtbarkeit ────────────────────────────────────────────────────────────
def test_ungeklaerte_raeume_werden_aufgelistet():
    """r1 ist räumlich zugeordnet, fachlich aber ebenfalls ungeklärt; r2 ist schon
    räumlich offen; r3 ist gar nicht erfasst."""
    b = _befund(
        _erg("eingeschraenkt", 1, refs=(("EG", "r1"),)),
        _erg("review_required", 2, refs=(("EG", "r2"),)),
    )
    assert raeume_ohne_geklaerten_scope(b, "EG", ["r1", "r2", "r3"]) == ["r1", "r2"]


def test_ungeklaert_bleibt_sichtbar_obwohl_ein_anderer_teil_bestaetigt_ist():
    """Genau der Fall, der vorher lautlos verschwand."""
    b = _befund(_erg("eingeschraenkt", 1), _erg("review_required", 2))
    assert raeume_ohne_geklaerten_scope(b, "EG", ["r1"]) == ["r1"]
    hinweise = " ".join(gate_summary(b, "EG", ["r1"])["hinweise"])
    assert "UNGEKLÄRT" in hinweise and "review_required" in hinweise


def test_summary_zaehlt_die_scope_zustaende():
    b = _befund(
        _erg("eingeschraenkt", 1, refs=(("EG", "r1"),)),
        _erg("review_required", 2, refs=(("EG", "r2"),)),
    )
    block = gate_summary(b, "EG", ["r1", "r2", "r3"])
    assert block["raum_zuordnung"] == {
        "bestaetigt": 1, "nicht_bestaetigt": 1, "ungeklaert": 1
    }
    # Fachlich: nie „anwendbar", solange der Nutzungs-Scope nicht belegt ist.
    assert block["sanitaer_scope"] == {
        "anwendbar": 0, "nicht_anwendbar": 1, "ungeklaert": 2
    }
    assert any("Anwendbarkeit" in h for h in block["hinweise"])
    assert block["verkehr_scope"]["anwendbar"] == 0
    assert block["stufen"] == {"teil_1": "eingeschraenkt", "teil_2": "review_required"}


def test_summary_nennt_den_verkehrs_vorbehalt_immer():
    b = _befund(_erg("eingeschraenkt", refs=(("EG", "r1"),)))
    assert any("60-m²" in h for h in gate_summary(b, "EG", ["r1"])["hinweise"])
