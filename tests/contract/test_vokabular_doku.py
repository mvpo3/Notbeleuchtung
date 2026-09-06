"""Doku-Drift-Guard: docs/VOKABULAR.md ↔ Maschinen-Kanon der Raumtypen.

Die COORDINATION-Frage „wo ist die Liste kanonisch?" beantwortet das Dokument —
aber nur, solange es nicht lügt. Dieser Guard hält die Raumtyp-Tabelle des
Dokuments deckungsgleich mit `raumerkennung/raumtyp.py` (derselbe Kanon, gegen
den auch Enis' LB-Stützliste geguardet ist, s. `test_lb_raumtyp_naht.py`).
"""
import re
from pathlib import Path

from notbeleuchtung.raumerkennung import raumtyp

DOKU = Path(__file__).parent.parent.parent / "docs" / "VOKABULAR.md"


def _doku_typen() -> set[str]:
    text = DOKU.read_text(encoding="utf-8")
    tabelle = text.split("## 1. Raumtypen")[1].split("## 2.")[0]
    typen = set()
    for zeile in tabelle.splitlines():
        m = re.match(r"\| ([A-ZÄÖÜ_]+) \|", zeile)
        if m and m.group(1) != "RAUMTYP":
            typen.add(m.group(1))
    return typen


def _kanon() -> set[str]:
    return {v[0] for v in raumtyp._TYP_MAP.values()} | {
        v[0] for v in raumtyp._EXTRA_DIRECT.values()
    }


def test_vokabular_doku_deckt_sich_mit_kanon():
    doku, kanon = _doku_typen(), _kanon()
    assert doku - kanon == set(), (
        "VOKABULAR.md listet Typen, die die Raumerkennung nicht vergibt: "
        + repr(sorted(doku - kanon))
    )
    assert kanon - doku == set(), (
        "Raumerkennung vergibt Typen, die in VOKABULAR.md fehlen — Tabelle "
        "nachziehen: " + repr(sorted(kanon - doku))
    )


def test_defensive_synonyme_stimmen_mit_bausteinen():
    """Die im Dokument genannten Defensiv-Synonyme = exakt die Code-Mengen."""
    from notbeleuchtung.platzierung.bausteine import KORRIDOR_TYPEN, WC_TYPEN

    text = DOKU.read_text(encoding="utf-8")
    kanon = _kanon()
    erwartet = (KORRIDOR_TYPEN | WC_TYPEN) - kanon
    for syn in erwartet:
        assert f"`{syn}`" in text, f"Defensiv-Synonym {syn!r} fehlt in VOKABULAR.md"
