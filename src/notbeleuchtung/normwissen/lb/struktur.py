"""struktur — Seiten → Abschnittsbaum, Dokumentart, Notbeleuchtungs-Abschnitte.

Alle vier untersuchten LBs sind Prosa mit hierarchischer Nummerierung
(`2.10`, `5.1.23`) — keine LV-Positionen. Der Abschnitt ist damit die natürliche
Extraktionseinheit **und** die Fundstelle für den Audit-Trail.

Warum die Abschnitts-Filterung entscheidend ist: sie ist die Homonym-Abwehr.
„Brausebatterie" (Sanitär), „Kabinennotbeleuchtung" (Aufzug) und der PV-Speicher
„LiFePO4" enthalten alle Anker-Wörter — sie liegen aber außerhalb der
Notbeleuchtungs-Abschnitte und können deshalb kein Feld setzen.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .text import Seite, als_satzblock


@dataclass
class Abschnitt:
    """Ein nummerierter LB-Abschnitt mit Überschrift, Text und Fundstelle."""

    nummer: str
    titel: str
    seite: int
    zeilen: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n".join(self.zeilen)

    @property
    def block(self) -> str:
        """Text ohne Zeilenumbrüche — für Muster, die über Zeilen greifen."""
        return als_satzblock(self.text)

    @property
    def fundstelle(self) -> str:
        return f"{self.nummer} {self.titel}".strip()


def baue_abschnitte(seiten: list[Seite], muster: dict) -> list[Abschnitt]:
    """Seiten → Abschnittsliste. Text vor der ersten Überschrift wird verworfen."""
    ueberschrift = re.compile(muster["abschnitt_muster"])
    seiten_nr = re.compile(muster["seite_muster"])
    abschnitte: list[Abschnitt] = []
    aktuell: Abschnitt | None = None

    for seite in seiten:
        zeilen = seite.text.split("\n")
        # Die gedruckte Seitenzahl VORAB bestimmen: je nach Extraktor steht die
        # Kopf-/Fußzeile mal vor, mal nach dem Inhalt. Ein Nachziehen in
        # Leserichtung läge bei seitenübergreifenden Abschnitten um eins daneben.
        gedruckt = seite.nummer
        for zeile in zeilen:
            treffer = seiten_nr.search(zeile)
            if treffer:
                gedruckt = int(treffer.group(1))
                break

        for zeile in zeilen:
            if seiten_nr.search(zeile):
                continue
            kopf = ueberschrift.match(zeile)
            if kopf and _ist_ueberschrift(kopf.group(2)):
                aktuell = Abschnitt(nummer=kopf.group(1), titel=kopf.group(2).strip(),
                                    seite=gedruckt)
                abschnitte.append(aktuell)
                continue
            if aktuell is not None:
                aktuell.zeilen.append(zeile)
    return abschnitte


def _ist_ueberschrift(rest: str) -> bool:
    """Grenzt Überschriften gegen Aufzählungen und Mengenzeilen ab."""
    rest = rest.strip()
    if not rest or len(rest) > 120:
        return False
    # „2 x Schuko …", „16A", „1 Stk. …" sind Stücklisten, keine Überschriften.
    return not re.match(r'^(?:x\s|Stk\.?|St\.?\s|\d)', rest)


def klassifiziere(volltext: str, arten: dict) -> str:
    """Elektro-LB / GU-Rahmen / Bau-Ausstattung — die Vorgaben stehen im Elektro-Dok."""
    klein = volltext.lower()
    treffer = {
        art: sum(1 for a in cfg["anker"] if a in klein)
        for art, cfg in arten.items()
    }
    # Elektro gewinnt bei Gleichstand: nur dort stehen technische Vorgaben.
    for art in ("elektro_lb", "gu_rahmen", "bau_ausstattung"):
        cfg = arten.get(art)
        if cfg and treffer.get(art, 0) >= cfg["mindest_treffer"]:
            return art
    return "unbekannt"


def sl_abschnitte(abschnitte: list[Abschnitt], anker: list[str],
                  ausschluss: list[str]) -> list[Abschnitt]:
    """Nur Abschnitte, deren ÜBERSCHRIFT Notbeleuchtung betrifft."""
    treffer = []
    for a in abschnitte:
        titel = a.titel.lower()
        if any(x in titel for x in ausschluss):
            continue
        if any(k in titel for k in anker):
            treffer.append(a)
    return treffer


def offene_verweise(abschnitte: list[Abschnitt], muster: list[str]) -> list[tuple[Abschnitt, str]]:
    """Verweise auf fremde Dokumente, die hier nicht auflösbar sind."""
    gefunden: list[tuple[Abschnitt, str]] = []
    kompiliert = [re.compile(m, re.IGNORECASE) for m in muster]
    for a in abschnitte:
        block = a.block
        for rx in kompiliert:
            treffer = rx.search(block)
            if treffer:
                gefunden.append((a, treffer.group(0).strip()))
                break
    return gefunden
