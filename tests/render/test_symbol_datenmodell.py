"""Render-Konsumption des Symbol-Datenmodells (v1.2.0) — Contract-Feld vor Synthese.

Reine Text-Helper-Tests (kein DXF nötig): NODEID bevorzugt `luminaire_id`,
Stückliste rendert die Typ-Letter-Legende (#7) sobald alle Platzierungen einen
Letter tragen, Belegungsliste nutzt `schaltungsart` aus dem Contract.
"""
from notbeleuchtung.hauptengine.contracts import Platzierung, PlatzierungsErgebnis
from notbeleuchtung.hauptengine.render.dxf_renderer import (
    _nodeids,
    _stromkreis_belegung_text,
    _stueckliste_text,
)


def _p(kind: str, **kw) -> Platzierung:
    return Platzierung(xy_mm=(0.0, 0.0), catalog_key=kw.pop("key", "k"), kind=kind, **kw)


def _erg(*platzierungen) -> PlatzierungsErgebnis:
    return PlatzierungsErgebnis(floor="4OG", platzierungen=list(platzierungen))


def test_nodeids_bevorzugen_contract_feld_mit_synthese_fallback():
    erg = _erg(
        _p("rz", luminaire_id="RZ-042"),   # vom Platzierer vergeben
        _p("rz"),                           # kein Feld → Synthese zählt weiter
    )
    assert _nodeids(erg) == ["RZ-042", "RZ-002"]


def test_stueckliste_typ_letter_legende():
    erg = _erg(
        _p("rz", key="rz_typ", typ_letter="A"),
        _p("rz", key="rz_typ", typ_letter="A"),
        _p("sicherheitsleuchte", key="sl_typ", typ_letter="B", typ_name="BASIC 2 AP WA"),
    )
    text = _stueckliste_text(erg)
    assert "Typ A: 2× Rettungszeichen — rz_typ" in text          # Produkt-Fallback = Key
    assert "Typ B: 1× Sicherheitsleuchte (Aufheller) — BASIC 2 AP WA" in text
    assert "Summe: 3" in text


def test_stueckliste_fallback_ohne_letters_bleibt_altes_format():
    text = _stueckliste_text(_erg(_p("rz"), _p("antipanik")))
    assert "Rettungszeichen: 1" in text and "Antipanik-Leuchte: 1" in text
    assert "Typ " not in text


def test_belegung_nutzt_contract_schaltungsart():
    # Contract-Feld übersteuert die kind-Heuristik (hier bewusst konträr gesetzt).
    erg = _erg(
        _p("rz", circuit_hint="K1", schaltungsart="BL"),
        _p("sicherheitsleuchte", circuit_hint="K1"),   # ohne Feld → Heuristik BL
    )
    text = _stromkreis_belegung_text(erg)
    assert "1× RZ (BL)" in text
    assert "1× SL (BL)" in text
