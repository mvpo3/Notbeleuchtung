"""Integrationstest AStV-Auswertung → Prüfbericht (außerhalb tests/normwissen).

Der positive Nachweis für den Integrationsschritt 2026-09-09 (Enis-Paket v2): die
§ 9-Prüfpunkte aus `normwissen.astv.ArbeitsstaettenWissen` erreichen über
`hauptengine.validierung.pruefbericht` die Befunde — je Gebäudeteil eindeutig
zugeordnet, mit Fundstelle, ungeprüftem Zustand und benötigter Angabe. Dieser
Schritt macht offene Fragen sichtbar; er entscheidet NICHT über die Erforderlichkeit
und ändert keine Platzierung.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import (
    BBox,
    Gebaeudeteil,
    PlatzierungsErgebnis,
    ProjektKontext,
    Raum,
    RaumModell,
)
from notbeleuchtung.hauptengine.validierung import pruefbericht


def _raum() -> RaumModell:
    return RaumModell(
        floor="EG",
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(10000.0, 10000.0)),
        raeume=[Raum(id="r1", raum_typ="GANG",
                     polygon_mm=[(0.0, 0.0), (10000.0, 0.0), (10000.0, 10000.0), (0.0, 10000.0)],
                     ist_fluchtweg=True)],
    )


def _leere_platzierung() -> PlatzierungsErgebnis:
    return PlatzierungsErgebnis(floor="EG", platzierungen=[])


def _teil(tid: str, aschg: bool | None) -> Gebaeudeteil:
    return Gebaeudeteil(id=tid, nutzungsart="SONSTIGES_GEBAEUDE", arbeitsstaette_nach_aschg=aschg)


def _astv_befunde(bericht: dict) -> list[dict]:
    return [b for b in bericht["befunde"] if b["regel"].startswith("AStV")]


def _pruefpunkte(bericht: dict, teil_id: str) -> list[dict]:
    marke = f"[Gebäudeteil {teil_id}]"
    return [b for b in bericht["befunde"]
            if "§ 9 offener Prüfpunkt" in b["regel"] and marke in b["regel"]]


def _reichweite(bericht: dict, teil_id: str) -> list[dict]:
    marke = f"[Gebäudeteil {teil_id}]"
    return [b for b in bericht["befunde"]
            if "Reichweite/Anwendungsbereich" in b["regel"] and marke in b["regel"]]


def _bericht_mit(*teile: Gebaeudeteil) -> dict:
    ctx = ProjektKontext(jurisdiction="AT", gebaeudeteile=list(teile))
    return pruefbericht(_raum(), _leere_platzierung(), projekt_kontext=ctx)


def test_true_drei_offene_pruefpunkte_z1_z2_z3() -> None:
    b = _bericht_mit(_teil("AT-true", True))
    pp = _pruefpunkte(b, "AT-true")
    assert len(pp) == 3, [x["regel"] for x in pp]
    kennungen = " ".join(x["regel"] for x in pp)
    assert "Z 1" in kennungen and "Z 2" in kennungen and "Z 3" in kennungen
    # Fundstelle, ungeprüfter Zustand und benötigte Angabe bleiben erhalten.
    z1 = next(x for x in pp if "Z 1" in x["regel"])
    assert "AStV § 9 Abs. 1 Z 1" in z1["regel"]
    assert "[ungeprueft]" in z1["detail"]
    assert "benötigte Angabe" in z1["detail"]
    assert all(x["status"] == "warnung" for x in pp)


def test_none_pruefpunkte_plus_vorbehalt_unbekannter_status() -> None:
    b = _bericht_mit(_teil("AT-none", None))
    assert len(_pruefpunkte(b, "AT-none")) == 3
    rw = _reichweite(b, "AT-none")
    assert rw, "Reichweite-Vorbehalt fehlt"
    assert "nicht erhoben" in rw[0]["detail"] or "None" in rw[0]["detail"]


def test_false_keine_pruefpunkte_aber_reichweite_bleibt() -> None:
    b = _bericht_mit(_teil("AT-false", False))
    assert _pruefpunkte(b, "AT-false") == []       # keiner der drei § 9-Punkte
    rw = _reichweite(b, "AT-false")
    assert rw, "Reichweite-Vorbehalt muss bei False erhalten bleiben"
    # § 1 Abs. 2: kein Freibrief für Nicht-Arbeitsstätten.
    assert "§ 1 Abs. 2" in rw[0]["detail"] or "außerhalb einer" in rw[0]["detail"]


def test_gemischte_gebaeudeteile_korrekt_zugeordnet() -> None:
    b = _bericht_mit(_teil("T-true", True), _teil("T-none", None), _teil("T-false", False))
    assert len(_pruefpunkte(b, "T-true")) == 3
    assert len(_pruefpunkte(b, "T-none")) == 3
    assert _pruefpunkte(b, "T-false") == []
    # Jeder AStV-Befund trägt genau EINE Gebäudeteil-Marke → eindeutig zugeordnet.
    for bef in _astv_befunde(b):
        marken = [t for t in ("T-true", "T-none", "T-false") if f"[Gebäudeteil {t}]" in bef["regel"]]
        assert len(marken) == 1, bef["regel"]


def test_fehlender_projektkontext_kein_absturz_keine_bewertung() -> None:
    b = pruefbericht(_raum(), _leere_platzierung(), projekt_kontext=None)
    assert _astv_befunde(b) == []
    assert "status" in b and "befunde" in b       # Bericht bleibt wohlgeformt


def test_astv_entscheidet_nicht_ueber_erforderlichkeit() -> None:
    """Kein AStV-Befund behauptet Erfüllung/Erforderlichkeit/Entfall — nur 'offen'."""
    b = _bericht_mit(_teil("T", True))
    for bef in _astv_befunde(b):
        assert bef["status"] == "warnung"
        assert "erforderlich ist" not in bef["detail"].lower()


def test_befund_nennt_die_ebene_der_fundstelle() -> None:
    """Review-Auflage 1 (Enis, 2026-09-09): die Ebene reist mit.

    Ohne sie ist im Prüfbericht nicht erkennbar, ob hinter einem offenen Punkt eine
    Rechtsquelle (A), eine Norm (C) oder eine Fachinformation (D) steht — genau die
    Unterscheidung, die `normwissen/astv.py` sorgfältig führt. Der Wert wird aus
    `AstvPruefpunkt.ebene` übernommen, nicht im Prüfbericht gesetzt.
    """
    from notbeleuchtung.normwissen.astv import ArbeitsstaettenWissen

    bericht = _bericht_mit(_teil("bt_a", True))
    punkte = _pruefpunkte(bericht, "bt_a")
    assert punkte, "ohne Prüfpunkte prüft dieser Test nichts"

    erwartet = {p.kennung: p.ebene for p in ArbeitsstaettenWissen().pruefpunkte(True)}
    for b in punkte:
        kennung = b["regel"].rsplit("(", 1)[1].rstrip(")")
        assert f"[Ebene {erwartet[kennung]}]" in b["regel"], b["regel"]

    # Und alles Bisherige bleibt: Fundstelle, Gebäudeteil-Marke, ungeprüfter Zustand,
    # Abgrenzung.
    eine = punkte[0]
    assert "AStV § 9 Abs. 1" in eine["regel"]
    assert "[Gebäudeteil bt_a]" in eine["regel"]
    assert eine["detail"].startswith("[ungeprueft]")
    assert "Abgrenzung:" in eine["detail"]
    assert eine["status"] == "warnung"
