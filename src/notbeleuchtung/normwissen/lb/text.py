"""text — LB-Dokument → normalisierter Text mit Seitenzuordnung.

`.txt` wird direkt gelesen, `.pdf` über **pypdf** (Lazy-Import: die Abhängigkeit
wird erst beim tatsächlichen PDF-Parsen gebraucht). Es gibt bewusst **keinen**
Runtime-Zwang auf ein lokales `pdftotext`-Binary.

Fail closed: fehlende Datei, unbekannte Endung, fehlendes pypdf oder ein PDF ohne
extrahierbaren Text führen zu `LbNichtLesbar` — nie zu leerem Text, der wie „die
LB sagt nichts" aussähe.

Normalisierung, ohne die Fundstellen zu verlieren: Zeilenstruktur bleibt erhalten
(die Abschnitts- und Bullet-Erkennung hängt daran), aber getrennte Fachbegriffe
werden zusammengezogen — im Original steht `LED- Sicherheitsbeleuchtung` mit
Leerzeichen nach dem Bindestrich, und `KEINE` kann durch einen Zeilenumbruch vom
Begriff getrennt sein.
"""
from __future__ import annotations

import re
from pathlib import Path

from .bericht import LbNichtLesbar

TEXT_ENDUNGEN = {".txt", ".md"}
PDF_ENDUNGEN = {".pdf"}

# „LED- Sicherheitsbeleuchtung" → „LED-Sicherheitsbeleuchtung"
_BINDESTRICH_LUECKE = re.compile(r"(\w)-\s+(?=[A-Za-zÄÖÜäöüß])")
_MEHRFACH_LEER = re.compile(r"[ \t]{2,}")


class Seite:
    """Eine Textseite mit ihrer im Dokument gedruckten Nummer (falls vorhanden)."""

    __slots__ = ("nummer", "text")

    def __init__(self, nummer: int, text: str) -> None:
        self.nummer = nummer
        self.text = text


def lade_seiten(pfad: str | Path) -> list[Seite]:
    """LB-Datei → Seitenliste. Wirft `LbNichtLesbar`, nie leeres Ergebnis."""
    p = Path(pfad)
    if not p.exists() or not p.is_file():
        raise LbNichtLesbar(f"LB-Datei nicht gefunden: {pfad}")
    endung = p.suffix.lower()
    if endung in TEXT_ENDUNGEN:
        seiten = _aus_text(p)
    elif endung in PDF_ENDUNGEN:
        seiten = _aus_pdf(p)
    else:
        raise LbNichtLesbar(
            f"Format nicht unterstützt: '{endung or '(ohne Endung)'}' — "
            f"unterstützt sind {sorted(TEXT_ENDUNGEN | PDF_ENDUNGEN)}"
        )
    if not any(s.text.strip() for s in seiten):
        raise LbNichtLesbar(
            f"Kein extrahierbarer Text in {p.name} — vermutlich ein Scan ohne "
            "Text-Layer. Eine leere LBVorgabe wäre hier gefährlich (nicht "
            "unterscheidbar von 'die LB macht keine Vorgaben')."
        )
    return seiten


def _aus_text(p: Path) -> list[Seite]:
    """Textdatei; Seitenumbrüche via Formfeed, sonst eine einzige Seite."""
    try:
        roh = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise LbNichtLesbar(f"LB-Datei nicht lesbar: {p.name} ({exc})") from exc
    teile = roh.split("\f") if "\f" in roh else [roh]
    return [Seite(i, normalisiere(t)) for i, t in enumerate(teile, start=1)]


def _aus_pdf(p: Path) -> list[Seite]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover — Abhängigkeit ist deklariert
        raise LbNichtLesbar(
            "PDF-Parsing braucht 'pypdf' (deklarierte Projekt-Abhängigkeit): "
            'pip install -e ".[dev,api]"'
        ) from exc
    try:
        reader = PdfReader(str(p))
        seiten = [
            Seite(i, normalisiere(seite.extract_text() or ""))
            for i, seite in enumerate(reader.pages, start=1)
        ]
    except LbNichtLesbar:
        raise
    except Exception as exc:  # defektes/verschlüsseltes PDF
        raise LbNichtLesbar(f"PDF nicht lesbar: {p.name} ({exc})") from exc
    if not seiten:
        raise LbNichtLesbar(f"PDF ohne Seiten: {p.name}")
    return seiten


def normalisiere(text: str) -> str:
    """Vereinheitlicht Whitespace und Bindestrich-Lücken, erhält die Zeilen."""
    text = text.replace(" ", " ").replace("\r\n", "\n").replace("\r", "\n")
    text = _BINDESTRICH_LUECKE.sub(r"\1-", text)
    return "\n".join(_MEHRFACH_LEER.sub(" ", z).rstrip() for z in text.split("\n"))


def als_satzblock(text: str) -> str:
    """Zeilenumbrüche zu Leerzeichen — für Muster, die über Zeilen hinweg greifen.

    Nötig, weil im Original `… ist KEINE\\nLED-Sicherheitsbeleuchtung herzustellen`
    steht: Negation und Begriff sind durch einen Umbruch getrennt.
    """
    return re.sub(r"\s+", " ", text).strip()
