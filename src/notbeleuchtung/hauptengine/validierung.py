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
_AUSGANG_RZ_RADIUS_MM = 4000.0  # RZ gilt als „am Ausgang", wenn ≤ 4 m entfernt
_KOLLISION_MM = 250.0           # zwei Symbole näher als das = Kollision/Doppelung
_MIN_RAEUME_PLAUSIBEL = 15      # ab so vielen Räumen ist ein (fast) leerer Plan unplausibel


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


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

    rz = [p for p in plzg if p.kind == "rz"]

    # 5. Rettungszeichen an jedem Notausgang (EN 1838 §4.1.2 g).
    notausgaenge = [a for a in raum.ausgaenge if a.typ in ("final_exit", "stair_exit")]
    if notausgaenge:
        ohne_rz = [
            a for a in notausgaenge
            if not any(_dist(a.xy_mm, p.xy_mm) <= _AUSGANG_RZ_RADIUS_MM for p in rz)
        ]
        befunde.append(Befund(
            "Rettungszeichen an Notausgängen (EN 1838 §4.1.2 g)",
            "warnung" if ohne_rz else "ok",
            f"{len(ohne_rz)}/{len(notausgaenge)} Notausgang/-gänge ohne RZ in Reichweite" if ohne_rz
            else f"alle {len(notausgaenge)} Notausgänge mit RZ",
        ))

    # 6. Jedes Rettungszeichen trägt eine Pfeilrichtung (EN ISO 7010, Erkennbarkeit).
    if rz:
        ohne_richtung = [p for p in rz if p.richtung is None]
        befunde.append(Befund(
            "Rettungszeichen-Richtung gesetzt",
            "warnung" if ohne_richtung else "ok",
            f"{len(ohne_richtung)} RZ ohne Pfeilrichtung" if ohne_richtung
            else "alle RZ mit Pfeilrichtung",
        ))

    # 7. Keine Symbol-Kollision/Doppelplatzierung (unter Mindestabstand).
    if len(plzg) > 1:
        kollisionen = sum(
            1
            for i in range(len(plzg))
            for j in range(i + 1, len(plzg))
            if _dist(plzg[i].xy_mm, plzg[j].xy_mm) < _KOLLISION_MM
        )
        befunde.append(Befund(
            "Keine Symbol-Kollision",
            "warnung" if kollisionen else "ok",
            f"{kollisionen} Symbol-Paar(e) unter {_KOLLISION_MM:g} mm" if kollisionen
            else "keine Doppelplatzierungen",
        ))

    # 8. Plan-Plausibilität (Vollständigkeit): ein Grundriss mit vielen Räumen, aber
    #    (fast) ohne Notbeleuchtung ist kein valider Plan. Fängt den Fall, den die
    #    Fluchtweg-Regeln (3/4) NICHT sehen — nämlich wenn gar keine Segmente erkannt
    #    wurden (Raumerkennung liefert keine Fluchtwege/Typen): sonst bestünde ein
    #    quasi-leeres Ergebnis (0-2 Symbole bei >100 Räumen) die Prüfung als „ok".
    n_raeume = len(raum.raeume)
    if n_raeume >= _MIN_RAEUME_PLAUSIBEL:
        if not plzg:
            befunde.append(Befund(
                "Plan-Plausibilität (Vollständigkeit)",
                "fehler",
                f"{n_raeume} Räume, aber kein Notbeleuchtungs-Symbol platziert "
                "(Raumerkennung liefert evtl. keine Fluchtwege/Raumtypen)",
            ))
        elif not rz:
            befunde.append(Befund(
                "Plan-Plausibilität (Vollständigkeit)",
                "warnung",
                f"{n_raeume} Räume, aber kein Rettungszeichen platziert "
                "(kein erkannter Fluchtweg/Ausgang?)",
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
