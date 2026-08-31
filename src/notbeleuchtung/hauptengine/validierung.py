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
_AUSGANG_RZ_RADIUS_MM = 2000.0  # EN 1838: „nahe" = < 2 m → RZ gilt als „am Ausgang"
_KOLLISION_MM = 250.0           # zwei Symbole näher als das = Kollision/Doppelung
_MIN_RAEUME_PLAUSIBEL = 15      # ab so vielen Räumen ist ein (fast) leerer Plan unplausibel
_QUASI_LEER_SYMBOLE = 2         # DoD: bis so wenige Symbole …
_QUASI_LEER_RAEUME = 100        # … bei so vielen Räumen = quasi-leer → Fehler (nicht nur Warnung)
_AUFHELLER_ARTEN = {"sicherheitsleuchte", "antipanik"}  # flächige LB-relevante Leuchten


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def _point_in_polygon(pt: tuple[float, float], poly: list[tuple[float, float]]) -> bool:
    """Ray-Casting (ungerade Kreuzungszahl = innen). Lokal gehalten, damit die QA-
    Schicht dependency-leicht bleibt (kein `platzierung`-Import in der Hauptengine)."""
    x, y = pt
    drin = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            drin = not drin
        j = i
    return drin


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
    #    Nur wenn KEINE Segmente erkannt wurden — sonst decken Regel 3/4 den Fall schon
    #    ab und Regel 8 wäre eine redundante Doppelmeldung.
    n_raeume = len(raum.raeume)
    if n_raeume >= _MIN_RAEUME_PLAUSIBEL and not segmente:
        if not plzg:
            befunde.append(Befund(
                "Plan-Plausibilität (Vollständigkeit)",
                "fehler",
                f"{n_raeume} Räume, aber kein Notbeleuchtungs-Symbol platziert "
                "(Raumerkennung liefert evtl. keine Fluchtwege/Raumtypen)",
            ))
        elif n_raeume > _QUASI_LEER_RAEUME and len(plzg) <= _QUASI_LEER_SYMBOLE:
            # DoD-Kriterium: 0-2 Symbole bei >100 Räumen = kein valider Plan → Fehler.
            befunde.append(Befund(
                "Plan-Plausibilität (Vollständigkeit)",
                "fehler",
                f"nur {len(plzg)} Symbol(e) auf {n_raeume} Räumen — quasi-leerer Plan "
                "(Raumerkennung liefert evtl. keine Fluchtwege/Raumtypen)",
            ))
        elif not rz:
            befunde.append(Befund(
                "Plan-Plausibilität (Vollständigkeit)",
                "warnung",
                f"{n_raeume} Räume, aber kein Rettungszeichen platziert "
                "(kein erkannter Fluchtweg/Ausgang?)",
            ))

    # 9./10. LB-Konformität — die oberste Hierarchie-Ebene (LB-explizit übersteuert
    # Norm). Prüft, dass der Plan die expliziten Auftraggeber-Vorgaben einhält; würde
    # z.B. eine nicht-feuernde lb_override-Regel (Label-Naht) als Fehler sichtbar machen.
    if lb is not None:
        befunde.extend(_lb_konformitaet(raum, plzg, lb))

    return befunde


def _lb_konformitaet(
    raum: RaumModell, plzg: list, lb: LBVorgabe
) -> list[Befund]:
    """LB-Exklusion (kein Aufheller in ausgeschlossenem Raumtyp) + LB-Inklusion
    (geforderter Raumtyp trägt ≥ 1 Aufheller). Nur Räume mit gültigem Polygon."""
    befunde: list[Befund] = []
    aufheller = [p for p in plzg if p.kind in _AUFHELLER_ARTEN]

    # 9. LB-Exklusion: „KEINE Sicherheitsbeleuchtung in Raumtyp X" ist ein Hard-Override.
    excl_typen = {b.raum_typ.upper() for b in lb.bereiche_exklusion if not b.sicherheitsbeleuchtung}
    excl_raeume = [
        r for r in raum.raeume if r.raum_typ.upper() in excl_typen and len(r.polygon_mm) >= 3
    ]
    if excl_raeume:
        verletzt = [
            p for p in aufheller
            if any(_point_in_polygon(p.xy_mm, r.polygon_mm) for r in excl_raeume)
        ]
        befunde.append(Befund(
            "LB-Exklusion respektiert (LB übersteuert Norm)",
            "fehler" if verletzt else "ok",
            f"{len(verletzt)} Aufheller-Leuchte(n) in LB-ausgeschlossenem Raumtyp "
            f"{sorted(excl_typen)}" if verletzt
            else f"keine Aufheller in {len(excl_raeume)} ausgeschlossenen Raum/Räumen",
        ))

    # 10. LB-Inklusion: LB verlangt SL in Raumtyp Y, obwohl die Norm dort keine vorsieht.
    incl_typen = {b.raum_typ.upper() for b in lb.bereiche_inklusion if b.sicherheitsbeleuchtung}
    incl_raeume = [
        r for r in raum.raeume if r.raum_typ.upper() in incl_typen and len(r.polygon_mm) >= 3
    ]
    if incl_raeume:
        ohne = [
            r for r in incl_raeume
            if not any(_point_in_polygon(p.xy_mm, r.polygon_mm) for p in aufheller)
        ]
        befunde.append(Befund(
            "LB-Inklusion erfüllt (geforderte Sicherheitsleuchte vorhanden)",
            "fehler" if ohne else "ok",
            f"{len(ohne)}/{len(incl_raeume)} LB-geforderte(r) Raum/Räume ohne "
            "Sicherheitsleuchte" if ohne
            else f"alle {len(incl_raeume)} LB-geforderten Räume mit Sicherheitsleuchte",
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
