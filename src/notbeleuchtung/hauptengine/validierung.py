"""validierung — Prüfbericht: EN-1838-Konformität des PlatzierungsErgebnis.

Der „Hard-Stop"-Layer der CLAUDE.md-Entscheidungshierarchie
(`LB-explizit → Referenz-Praxis → EN-1838/ÖNorm → OVE-Verbote (Hard Stop)`): eine
Abnahme-/QA-Schicht, die den fertigen Plan gegen prüfbare Norm-Regeln testet und einen
strukturierten Prüfbericht liefert (kein Fach-Wissen erfinden — nur prüfen, was aus den
Contracts folgt). Reine Analyse, render-frei, kein Contract berührt.

Abgrenzung zum Coverage-Audit (`pipeline._coverage`): Coverage prüft die *Vollständigkeit
der Leuchten-Arten* (wurde SL/Antipanik überhaupt abgeleitet); die Validierung prüft die
*Norm-Konformität* der gesetzten Symbole (Höhe, getrennter Kreis, Fluchtweg-Deckung).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import LBVorgabe, PlatzierungsErgebnis, RaumModell

_MIN_MONTAGEHOEHE_MM = 2000.0   # EN 1838 §4.1 (Montagehöhe ≥ 2 m)
_SV_KENNUNG = "F13"             # getrennter Sicherheitskreis (SV, dauergeschaltet)


@dataclass
class Befund:
    regel: str
    status: str    # "ok" | "warnung" | "fehler"
    detail: str


def pruefe(
    raum: RaumModell, platzierung: PlatzierungsErgebnis, lb: LBVorgabe | None = None
) -> list[Befund]:
    """Prüft die Platzierung gegen die aus den Contracts ableitbaren Norm-Regeln."""
    plzg = platzierung.platzierungen
    befunde: list[Befund] = []

    # 1. Montagehöhe ≥ 2000 mm (EN 1838 §4.1).
    zu_niedrig = [p for p in plzg if p.height_mm < _MIN_MONTAGEHOEHE_MM]
    befunde.append(Befund(
        "Montagehöhe ≥ 2000 mm (EN 1838 §4.1)",
        "fehler" if zu_niedrig else "ok",
        f"{len(zu_niedrig)} Symbol(e) unter 2000 mm" if zu_niedrig else "alle Symbole ≥ 2000 mm",
    ))

    # 2. Getrennter Sicherheitskreis (jedes Symbol trägt eine F13-Kreis-Kennung).
    if plzg:
        ohne_kreis = [p for p in plzg if _SV_KENNUNG not in (p.circuit_hint or "")]
        befunde.append(Befund(
            "Getrennter Sicherheitskreis (EN 1838)",
            "warnung" if ohne_kreis else "ok",
            f"{len(ohne_kreis)} Symbol(e) ohne F13-Kreis" if ohne_kreis
            else "alle Symbole auf getrenntem SV-Kreis",
        ))

    # 3. Fluchtweg-Deckung: jedes Fluchtweg-Segment ist von ≥ 1 RZ gedeckt.
    segmente = {s.segment_id for s in raum.zirkulation.segmente}
    if segmente:
        gedeckt: set[str] = set()
        for p in plzg:
            gedeckt.update(p.covers_segment)
        ungedeckt = segmente - gedeckt
        befunde.append(Befund(
            "Fluchtweg-Deckung durch Rettungszeichen",
            "warnung" if ungedeckt else "ok",
            f"{len(ungedeckt)}/{len(segmente)} Segment(e) ohne RZ" if ungedeckt
            else f"alle {len(segmente)} Segmente gedeckt",
        ))
        # 4. Bei vorhandenem Fluchtweg MUSS mindestens ein Rettungszeichen existieren.
        if not any(p.kind == "rz" for p in plzg):
            befunde.append(Befund(
                "Rettungszeichen vorhanden (Fluchtweg)",
                "fehler",
                "Fluchtwege vorhanden, aber kein Rettungszeichen platziert",
            ))

    return befunde


def gesamtstatus(befunde: list[Befund]) -> str:
    """Gesamt-Status: 'fehler' schlägt 'warnung' schlägt 'ok'."""
    stati = {b.status for b in befunde}
    if "fehler" in stati:
        return "fehler"
    if "warnung" in stati:
        return "warnung"
    return "ok"


def pruefbericht(
    raum: RaumModell, platzierung: PlatzierungsErgebnis, lb: LBVorgabe | None = None
) -> dict:
    """Serialisierbarer Prüfbericht für den Pipeline-/API-Summary."""
    befunde = pruefe(raum, platzierung, lb)
    return {
        "status": gesamtstatus(befunde),
        "befunde": [asdict(b) for b in befunde],
    }
