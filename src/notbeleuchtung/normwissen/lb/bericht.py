"""LbBericht — Audit-Trail des LB-Parsings (Enis-intern, KEIN Contract).

`LBVorgabe` (Contract) trägt nur Werte, kein Feld für „Konflikt", „nicht
zuordenbar" oder „unaufgelöster Verweis". Genau diese Information darf aber nicht
verloren gehen — sonst liefe die Engine weiter, als hätte die LB nichts gesagt.
Deshalb dieser Bericht: er lebt in `normwissen/` und erzwingt keinen Contract-Bump.

Vier Zustände je Feld:

* `wert`                — explizit in der LB gefunden (mit Fundstelle)
* `nicht_spezifiziert`  — im Notbeleuchtungs-Abschnitt gesucht, nichts gefunden
                          → `None` im Contract → der Norm-Default greift
* `review_informativ`   — Beobachtung ohne Einfluss auf das Ergebnis
* `review_blockierend`  — die Vorgabe ist erkannt, aber nicht zuverlässig
                          anwendbar → `parse_lb()` bricht ab (fail closed)
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Status = Literal["wert", "nicht_spezifiziert", "review_informativ", "review_blockierend"]

DokumentArt = Literal["elektro_lb", "gu_rahmen", "bau_ausstattung", "unbekannt"]


class FeldBefund(BaseModel):
    """Ein Extraktionsbefund mit vollständiger Provenienz."""

    feld: str
    status: Status
    begruendung: str
    datei: str = ""
    abschnitt: str | None = None       # z.B. "2.11 LED-Sicherheitsbeleuchtung (Garage)"
    seite: int | None = None
    anker: str | None = None           # der Textanker, der den Befund ausgelöst hat
    kandidat: str | None = None        # extrahierter Wert als Text (auch wenn blockiert)

    @property
    def blockierend(self) -> bool:
        return self.status == "review_blockierend"

    def fundstelle(self) -> str:
        """Kompakte Quellenangabe für `lb_quelle` und Log-Ausgaben."""
        teile = [self.datei]
        if self.abschnitt:
            teile.append(f"§{self.abschnitt}")
        if self.seite is not None:
            teile.append(f"S. {self.seite}")
        return ", ".join(t for t in teile if t)


class LbBericht(BaseModel):
    """Was der Parser aus einem LB-Dokument gelesen hat — inkl. der Zweifel."""

    datei: str
    dokument_art: DokumentArt = "unbekannt"
    befunde: list[FeldBefund] = Field(default_factory=list)

    def add(self, **kwargs) -> FeldBefund:
        befund = FeldBefund(datei=self.datei, **kwargs)
        self.befunde.append(befund)
        return befund

    @property
    def blockierende(self) -> list[FeldBefund]:
        return [b for b in self.befunde if b.blockierend]

    def fuer_feld(self, feld: str) -> list[FeldBefund]:
        return [b for b in self.befunde if b.feld == feld]

    def als_text(self) -> str:
        """Menschenlesbarer Audit-Bericht."""
        kopf = f"LB-Bericht — {self.datei} (erkannt als: {self.dokument_art})"
        zeilen = [kopf, "=" * len(kopf)]
        for b in self.befunde:
            marke = {"wert": "✓", "nicht_spezifiziert": "·",
                     "review_informativ": "!", "review_blockierend": "✖"}[b.status]
            wert = f" = {b.kandidat}" if b.kandidat else ""
            quelle = b.fundstelle()
            zeilen.append(f"{marke} {b.feld}{wert}")
            zeilen.append(f"    {b.begruendung}")
            if quelle:
                zeilen.append(f"    Fundstelle: {quelle}" + (f" · Anker: „{b.anker}\"" if b.anker else ""))
        if self.blockierende:
            zeilen.append("")
            zeilen.append(f"BLOCKIEREND: {len(self.blockierende)} Befund(e) — parse_lb() bricht ab.")
        return "\n".join(zeilen)


class LbFehler(Exception):
    """Basis: die LB konnte nicht zu einer verlässlichen LBVorgabe verarbeitet werden."""


class LbNichtLesbar(LbFehler):
    """Datei fehlt, Format nicht unterstützt, oder kein extrahierbarer Text.

    Bewusst KEINE leere `LBVorgabe`: die wäre von „LB macht keine Vorgaben"
    nicht unterscheidbar und würde die Engine still norm-getrieben weiterlaufen
    lassen, obwohl ein 2. Input vorliegt.
    """


class LbReviewRequired(LbFehler):
    """Vorgaben erkannt, aber mindestens eine ist nicht zuverlässig anwendbar.

    Trägt den vollständigen `LbBericht` (inkl. Kandidatenwerten), damit der
    Aufrufer genau sieht, was gefunden wurde und warum es blockiert.
    """

    def __init__(self, bericht: LbBericht) -> None:
        self.bericht = bericht
        gruende = "; ".join(f"{b.feld}: {b.begruendung}" for b in bericht.blockierende)
        super().__init__(f"LB erfordert manuelle Prüfung ({bericht.datei}) — {gruende}")
