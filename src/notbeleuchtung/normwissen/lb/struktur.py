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
    """Ein nummerierter LB-Abschnitt mit Überschrift, Text und Fundstellen.

    Jede Zeile trägt die Seite, auf der sie tatsächlich steht. Ein Abschnitt kann
    über mehrere Seiten laufen — die Seite der Überschrift ist dann für einen
    Treffer am Abschnittsende schlicht falsch. Deshalb liefert `seite_fuer()` zu
    jeder Fundstelle im `block` die echte Seite zurück.
    """

    nummer: str
    titel: str
    seite: int                                   # Seite der Überschrift
    eintraege: list[tuple[str, int]] = field(default_factory=list)  # (Zeile, Seite)

    @property
    def zeilen(self) -> list[str]:
        return [z for z, _ in self.eintraege]

    @property
    def text(self) -> str:
        return "\n".join(self.zeilen)

    @property
    def block(self) -> str:
        """Text ohne Zeilenumbrüche — für Muster, die über Zeilen greifen."""
        return self._block_und_index()[0]

    def seite_fuer(self, offset: int) -> int:
        """Seite, auf der das Zeichen an `offset` im `block` steht."""
        _, index = self._block_und_index()
        seite = self.seite
        for start, s in index:
            if start > offset:
                break
            seite = s
        return seite

    def saetze(self) -> list[tuple[str, int]]:
        """(Satz, Seite) — Auswertungseinheiten mit ihrer echten Fundstelle.

        Gemessen wird ab dem ersten *echten* Zeichen: ein Satz beginnt nach dem
        Punkt des vorigen mit einem Trennzeichen, das noch zur vorherigen Zeile
        — und damit womöglich zur vorherigen Seite — gehört.
        """
        ergebnis: list[tuple[str, int]] = []
        for m in re.finditer(r"[^.:]*[.:]|[^.:]+$", self.block):
            roh = m.group(0)
            satz = roh.strip()
            if not satz:
                continue
            vorlauf = len(roh) - len(roh.lstrip())
            ergebnis.append((satz, self.seite_fuer(m.start() + vorlauf)))
        return ergebnis

    def _block_und_index(self) -> tuple[str, list[tuple[int, int]]]:
        """Block-Text + (Offset, Seite)-Index. Wird je Abschnitt einmal gebaut."""
        if getattr(self, "_cache", None) is None or self._cache[2] != len(self.eintraege):
            teile: list[str] = []
            index: list[tuple[int, int]] = []
            pos = 0
            for zeile, seite in self.eintraege:
                z = als_satzblock(zeile)
                if not z:
                    continue
                if teile:
                    pos += 1                     # Trenn-Leerzeichen
                index.append((pos, seite))
                teile.append(z)
                pos += len(z)
            self._cache = (" ".join(teile), index, len(self.eintraege))
        return self._cache[0], self._cache[1]

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
            if kopf and _ist_ueberschrift(kopf.group(2), muster["ueberschrift_max_laenge"]):
                aktuell = Abschnitt(nummer=kopf.group(1), titel=kopf.group(2).strip(),
                                    seite=gedruckt)
                abschnitte.append(aktuell)
                continue
            if aktuell is not None:
                # Zeile MIT ihrer Seite — ein Abschnitt kann über Seiten laufen.
                aktuell.eintraege.append((zeile, gedruckt))
    return abschnitte


def _ist_ueberschrift(rest: str, max_laenge: int) -> bool:
    """Grenzt Überschriften gegen Aufzählungen, Mengen- und Fließtextzeilen ab."""
    rest = rest.strip()
    if not rest or len(rest) > max_laenge:
        return False
    # „2 x Schuko …", „16A", „1 Stk. …" sind Stücklisten, keine Überschriften.
    return not re.match(r'^(?:x\s|Stk\.?|St\.?\s|\d)', rest)


def klassifiziere(volltext: str, arten: dict) -> str:
    """Elektro-LB / GU-Rahmen / Bau-Ausstattung — die Vorgaben stehen im Elektro-Dok.

    Es gewinnt die Art mit den MEISTEN belegten Ankern, nicht die erste, die ihre
    Mindestzahl erreicht: ein GU-Rahmenvertrag erwähnt „Notbeleuchtung" durchaus
    (als Wartungsposition) und würde sonst als Elektro-LB durchgehen.
    """
    klein = volltext.lower()
    kandidaten = [
        (sum(1 for a in cfg["anker"] if a in klein), art)
        for art, cfg in arten.items()
    ]
    erreicht = [
        (n, art) for n, art in kandidaten if n >= arten[art]["mindest_treffer"]
    ]
    if not erreicht:
        return "unbekannt"
    # Bei Gleichstand gewinnt die spezifischere Art (mehr geforderte Anker).
    hoechste = max(n for n, _ in erreicht)
    gleichauf = [art for n, art in erreicht if n == hoechste]
    return max(gleichauf, key=lambda art: arten[art]["mindest_treffer"])


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


def verweise(abschnitte: list[Abschnitt], klassen: dict) -> list[tuple[str, Abschnitt, str, int]]:
    """Verweise auf andere Dokumente, klassifiziert.

    Rückgabe: (Klasse, Abschnitt, gefundener Text, **Seite des Treffers**). Ob
    eine Klasse blockiert, entscheidet der Parser — hier wird nur gefunden.
    """
    kompiliert = {
        klasse: [re.compile(m, re.IGNORECASE) for m in cfg["muster"]]
        for klasse, cfg in klassen.items()
    }
    gefunden: list[tuple[str, Abschnitt, str, int]] = []
    for a in abschnitte:
        block = a.block
        for klasse, muster in kompiliert.items():
            for rx in muster:
                treffer = rx.search(block)
                if treffer:
                    gefunden.append(
                        (klasse, a, treffer.group(0).strip(), a.seite_fuer(treffer.start()))
                    )
                    break
    return gefunden
