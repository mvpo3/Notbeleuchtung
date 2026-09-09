"""X-Notbeleuchtung — Größenbudget des Response-Headers (Review-Auflage 2, 2026-09-09).

Der Header wächst mit jedem Gebäudeteil: der `oib`-Block trägt die Provider-Hinweise
je Gebäudeteil (AStV-Parallelpfad, Stufen, Vorbehalte). Gemessen am echten HTTP-Lauf
liefert uvicorn auch 25 KB aus — die Kappung hier ist deshalb **keine** Server-,
sondern eine Kompatibilitätsgrenze (Proxy-/Gateway-Puffer, Default 4 KiB, per
`NOTBELEUCHTUNG_HEADER_MAX_BYTES` anhebbar).

Was diese Tests festhalten:
  * das Budget wird eingehalten,
  * die Ausgabe bleibt gültiges, für die bestehenden Verbraucher lesbares JSON,
  * eine Kürzung ist **sichtbar** und **gezählt** — offene Vorbehalte verschwinden
    nicht unbemerkt,
  * `stufen` und `lb_review` werden **nie** geopfert,
  * der interne Prüfbericht bleibt unverändert.
"""
from __future__ import annotations

import json

import pytest

from notbeleuchtung.api import main as api_main


def _summary(n_hinweise: int, hinweis_laenge: int = 400) -> dict:
    """Ein render_summary mit steuerbar großem `oib`-Block."""
    return {
        "floor": "4OG",
        "n_symbols": 11,
        "by_kind": {"rz": 7, "sl": 4},
        "n_raeume": 9,
        "rendered": True,
        "oib": {
            "stufen": {f"BT-{i}": "eingeschraenkt" for i in range(4)},
            "raum_genau": False,
            "hinweise": [f"[BT-{i}] " + "H" * hinweis_laenge for i in range(n_hinweise)],
            "raum_zuordnung": {"bestaetigt": 0, "nicht_bestaetigt": 0, "ungeklaert": 9},
        },
    }


def test_kleiner_header_bleibt_unangetastet() -> None:
    """Unter Budget wird nichts gekürzt und nichts markiert."""
    quelle = _summary(n_hinweise=2, hinweis_laenge=50)
    kopf = api_main._header_summary(quelle)

    assert "header_gekuerzt" not in kopf
    assert "hinweise_gekuerzt" not in kopf["oib"]
    assert len(kopf["oib"]["hinweise"]) == 2


def test_grosser_header_bleibt_im_budget_und_lesbar() -> None:
    kopf = api_main._header_summary(_summary(n_hinweise=40))
    roh = api_main._als_header(kopf)

    assert len(roh.encode()) <= api_main._HEADER_MAX_BYTES
    # Gültiges JSON und die Felder, auf die bestehende Verbraucher zugreifen.
    wieder = json.loads(roh)
    assert wieder["floor"] == "4OG"
    assert wieder["n_symbols"] == 11
    assert wieder["by_kind"] == {"rz": 7, "sl": 4}
    assert wieder["oib"]["stufen"] == {f"BT-{i}": "eingeschraenkt" for i in range(4)}
    assert wieder["oib"]["raum_zuordnung"]["ungeklaert"] == 9


def test_kuerzung_ist_sichtbar_und_gezaehlt() -> None:
    """Kein stiller Verlust: die Zahl der zurückgehaltenen Hinweise steht im Block."""
    kopf = api_main._header_summary(_summary(n_hinweise=40))
    oib = kopf["oib"]

    assert kopf["header_gekuerzt"] is True
    assert oib["hinweise_gekuerzt"] is True
    assert oib["hinweise_gesamt"] == 40
    assert oib["hinweise_uebertragen"] == len(oib["hinweise"])
    assert oib["hinweise_zurueckgehalten"] == 40 - oib["hinweise_uebertragen"]
    assert oib["hinweise_zurueckgehalten"] > 0
    # Der Zeiger auf die vollständige Fassung fehlt nie.
    assert "Pruefbericht" in oib["hinweise_kuerzung"] or "pruefung" in oib["hinweise_kuerzung"]


def test_uebertragene_hinweise_behalten_ihre_reihenfolge() -> None:
    kopf = api_main._header_summary(_summary(n_hinweise=40))
    uebertragen = kopf["oib"]["hinweise"]
    original = _summary(n_hinweise=40)["oib"]["hinweise"]

    assert uebertragen == original[: len(uebertragen)]


def test_stufen_werden_nie_geopfert() -> None:
    """Auch wenn gar kein Hinweis mehr passt: der Zustand selbst bleibt im Header."""
    kopf = api_main._header_summary(_summary(n_hinweise=200, hinweis_laenge=800))

    assert kopf["oib"]["stufen"], "Stufen je Gebäudeteil müssen erhalten bleiben"
    assert kopf["oib"]["hinweise_gesamt"] == 200
    assert kopf["header_gekuerzt"] is True


def test_lb_review_bleibt_erhalten() -> None:
    """Fail-closed-Signal darf durch die Kürzung nicht verschwinden."""
    quelle = _summary(n_hinweise=40)
    quelle["lb_review"] = {"grund": "LbReviewRequired", "meldung": "M" * 2000}
    kopf = api_main._header_summary(quelle)

    assert kopf["lb_review"]["grund"] == "LbReviewRequired"
    assert kopf["lb_review"]["gekuerzt"] is True
    assert len(api_main._als_header(kopf).encode()) <= api_main._HEADER_MAX_BYTES


def test_interner_pruefbericht_bleibt_unveraendert() -> None:
    """Gekürzt wird nur die Header-Kopie — die Quelle bleibt vollständig."""
    quelle = _summary(n_hinweise=40)
    vorher = json.dumps(quelle, sort_keys=True)

    api_main._header_summary(quelle)

    assert json.dumps(quelle, sort_keys=True) == vorher
    assert len(quelle["oib"]["hinweise"]) == 40


def test_budget_ist_konfigurierbar(monkeypatch: pytest.MonkeyPatch) -> None:
    """Erlaubt die Betriebsumgebung mehr, wird auch mehr übertragen."""
    quelle = _summary(n_hinweise=40)
    eng = api_main._header_summary(quelle)

    monkeypatch.setattr(api_main, "_HEADER_MAX_BYTES", 32768)
    weit = api_main._header_summary(quelle)

    assert len(weit["oib"]["hinweise"]) > len(eng["oib"]["hinweise"])
    assert "header_gekuerzt" not in weit

    monkeypatch.setattr(api_main, "_HEADER_MAX_BYTES", 0)  # abgeschaltet
    aus = api_main._header_summary(quelle)
    assert len(aus["oib"]["hinweise"]) == 40
