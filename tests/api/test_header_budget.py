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


# ── Grenzfall: schon die nicht kürzbaren Felder sprengen das Budget ──────────
def _summary_mit_vielen_stufen(n_teile: int = 120, n_hinweise: int = 3) -> dict:
    """`stufen` allein ist größer als das Budget — hier ist nichts mehr kürzbar."""
    return {
        "floor": "4OG",
        "n_symbols": 11,
        "by_kind": {"rz": 7, "sl": 4},
        "n_raeume": 9,
        "rendered": True,
        "oib": {
            "stufen": {f"BAUTEIL-{i:03d}-mit-langem-namen": "review_required"
                       for i in range(n_teile)},
            "raum_genau": False,
            "hinweise": [f"[BT-{i}] Hinweis" for i in range(n_hinweise)],
        },
    }


def test_ueber_budget_trotz_voller_kuerzung_ist_definiert_und_markiert() -> None:
    """Definiertes Verhalten: ausliefern, nichts opfern, **als über Budget markieren**.

    Die nicht kürzbaren Felder tragen den Zustand (Stufen je Gebäudeteil). Sie
    werden nicht geopfert — ein stiller Verlust wäre schlimmer als ein großer
    Header. Damit der Fall nicht als „passt schon" durchgeht, sagen es die Marken.
    """
    kopf = api_main._header_summary(_summary_mit_vielen_stufen())
    roh = api_main._als_header(kopf)

    assert len(roh.encode()) > api_main._HEADER_MAX_BYTES        # Budget verfehlt …
    assert json.loads(roh)                                       # … aber gültiges JSON
    assert len(kopf["oib"]["stufen"]) == 120                     # Zustand vollständig
    assert kopf["header_ueber_budget"] is True
    assert kopf["header_budget_bytes"] == api_main._HEADER_MAX_BYTES
    assert kopf["header_bytes"] == len(roh.encode())
    # Alle Hinweise wurden zurückgehalten — und das steht gezählt im Block.
    assert kopf["oib"]["hinweise"] == []
    assert kopf["oib"]["hinweise_gesamt"] == 3
    assert kopf["oib"]["hinweise_zurueckgehalten"] == 3
    assert kopf["header_gekuerzt"] is True


def test_ohne_kuerzbaren_inhalt_wird_keine_kuerzung_behauptet() -> None:
    """Nichts zu kürzen da → `header_gekuerzt` darf NICHT gesetzt sein."""
    quelle = _summary_mit_vielen_stufen(n_hinweise=0)
    kopf = api_main._header_summary(quelle)

    assert kopf["header_ueber_budget"] is True
    assert "header_gekuerzt" not in kopf
    assert kopf["oib"]["hinweise"] == []


def test_ohne_oib_block_wird_keine_kuerzung_behauptet() -> None:
    """Auch ohne `oib`: Marke sagt „über Budget", nicht „gekürzt"."""
    quelle = {"floor": "4OG", "n_symbols": 11, "rendered": True,
              "by_kind": {f"kind_{i}": i for i in range(400)}}
    kopf = api_main._header_summary(quelle)

    assert kopf["header_ueber_budget"] is True
    assert "header_gekuerzt" not in kopf
    assert len(kopf["by_kind"]) == 400


def test_normale_kuerzung_meldet_kein_ueber_budget() -> None:
    """Gegenprobe: passt es nach der Kürzung, ist `header_ueber_budget` weg."""
    kopf = api_main._header_summary(_summary(n_hinweise=40))

    assert "header_ueber_budget" not in kopf
    assert kopf["header_gekuerzt"] is True


# ── Wohin der Verweis zeigt ─────────────────────────────────────────────────
def test_verweis_sagt_dass_die_vollfassung_nicht_ueber_die_api_erreichbar_ist() -> None:
    """Der Zeiger darf keine Erreichbarkeit vortäuschen, die es nicht gibt.

    `POST /plan` liefert die Plandatei plus diesen Header — einen Endpunkt für den
    Prüfbericht gibt es nicht (offene Lücke L2). Der Text muss das sagen, sonst
    sucht ein Client nach etwas, das die API nicht hergibt.
    """
    kopf = api_main._header_summary(_summary(n_hinweise=40))
    text = kopf["oib"]["hinweise_kuerzung"]

    assert "NICHT ueber die API abrufbar" in text
    assert "L2" in text
    assert "NOTBELEUCHTUNG_HEADER_MAX_BYTES" in text   # der eine Weg, mehr zu bekommen
    assert kopf["header_kuerzung"] == text
