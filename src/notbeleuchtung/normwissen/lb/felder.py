"""felder — Extraktoren für die einzelnen LBVorgabe-Felder.

Deterministisch und quellengebunden: jede Funktion bekommt bereits gefilterten
Text (nur Notbeleuchtungs-Abschnitte) und liefert Wert **plus** den Textanker,
der ihn ausgelöst hat. Alle Muster, Einheiten und Vokabeln kommen aus
`data/lb_extraktion.yaml` — hier steht kein Fachwort.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .struktur import Abschnitt


@dataclass(frozen=True)
class Treffer:
    """Ein extrahierter Kandidat mit Provenienz.

    `seite` ist die Seite des TREFFERS, nicht die des Abschnittsanfangs — bei
    seitenübergreifenden Abschnitten wäre letztere falsch.
    """

    wert: object
    anker: str
    abschnitt: Abschnitt
    seite: int


def _zahl(roh: str) -> float:
    """„0,5" → 0.5 — deutsches Dezimalkomma."""
    return float(roh.replace(",", "."))


def zahl_feld(abschnitte: list[Abschnitt], cfg: dict) -> Treffer | None:
    """Zahl + Einheit im Umfeld eines Fachworts; erster Treffer gewinnt.

    Zwei optionale Schutzgitter aus der Konfiguration:

    * `ausschluss` — Regexe, die im Fenster um den Treffer NICHT vorkommen dürfen.
      Damit lässt sich eine benachbarte, aber andere Größe abwehren (Antipanik
      0,5 lx ist nicht die Fluchtweg-Mittellinie 1 lx).
    * `plausibel_max` — Obergrenze in der Zielgröße. Was darüber liegt, ist keine
      Notlicht-Angabe mehr, sondern eine Fremdzahl.

    Ein verworfener Treffer beendet die Suche nicht — das nächste Muster bzw. der
    nächste Abschnitt darf noch greifen.
    """
    einheiten = {k.lower(): v for k, v in cfg.get("einheiten", {}).items()}
    ausschluss = [re.compile(r, re.IGNORECASE) for r in cfg.get("ausschluss", [])]
    fenster = cfg.get("ausschluss_fenster", 60)
    grenze = cfg.get("plausibel_max")
    for a in abschnitte:
        block = a.block
        for m in cfg["muster"]:
            for treffer in re.finditer(m["regex"], block, re.IGNORECASE):
                umfeld = block[max(0, treffer.start() - fenster): treffer.end()]
                if any(rx.search(umfeld) for rx in ausschluss):
                    continue
                wert = _zahl(treffer.group(1))
                gruppe = m.get("einheit_gruppe")
                if gruppe:
                    einheit = (treffer.group(gruppe) or "").strip().lower()
                    faktor = einheiten.get(einheit)
                    if faktor is None:
                        continue      # unbekannte Einheit → lieber nichts als falsch
                    wert *= faktor
                if grenze is not None and wert > grenze:
                    continue
                return Treffer(wert=wert, anker=treffer.group(0).strip(), abschnitt=a,
                               seite=a.seite_fuer(treffer.start()))
    return None


def enum_feld(abschnitte: list[Abschnitt], cfg: dict) -> list[Treffer]:
    """Alle belegten Enum-Werte. Mehr als einer = Konflikt (nicht auflösen!)."""
    ausschluss = [s.lower() for s in cfg.get("ausschluss", [])]
    gefunden: dict[str, Treffer] = {}
    for a in abschnitte:
        klein = a.block.lower()
        for wert, anker_liste in cfg["werte"].items():
            if wert in gefunden:
                continue
            for anker in anker_liste:
                pos = klein.find(anker)
                if pos < 0:
                    continue
                umfeld = klein[max(0, pos - 60):pos + 60]
                if any(x in umfeld for x in ausschluss):
                    continue          # Homonym (Sanitär, PV, Rauchmelder)
                gefunden[wert] = Treffer(wert=wert, anker=anker, abschnitt=a,
                                         seite=a.seite_fuer(pos))
                break
    return list(gefunden.values())


def stellen(abschnitte: list[Abschnitt], cfg: dict) -> list[Treffer]:
    """Rettungszeichen-Stellen (RzStelle-Literale) per Vorkommensprüfung."""
    gefunden: dict[str, Treffer] = {}
    for a in abschnitte:
        klein = a.block.lower()
        for wert, anker_liste in cfg.items():
            if wert in gefunden:
                continue
            for anker in anker_liste:
                pos = klein.find(anker)
                if pos >= 0:
                    gefunden[wert] = Treffer(wert=wert, anker=anker, abschnitt=a,
                                             seite=a.seite_fuer(pos))
                    break
    return list(gefunden.values())


def sonder_lux(abschnitte: list[Abschnitt], regeln: list[dict]) -> list[Treffer]:
    """Erhöhte Mindest-Lux an einem Ort (z.B. Feuerlöscher ≥ 5 lx)."""
    ergebnis: list[Treffer] = []
    for a in abschnitte:
        block = a.block
        for regel in regeln:
            treffer = re.search(regel["regex"], block, re.IGNORECASE)
            if treffer:
                ergebnis.append(
                    Treffer(wert=(regel["ort"], _zahl(treffer.group(1))),
                            anker=treffer.group(0).strip(), abschnitt=a,
                            seite=a.seite_fuer(treffer.start()))
                )
    return ergebnis


def erstes_muster(abschnitte: list[Abschnitt], muster: str | list[str]) -> Treffer | None:
    """Generischer Einzeltreffer (Piktogramm-Norm, Funktionserhalt, Batterie-Standort).

    Mehrere Muster werden in Deklarationsreihenfolge probiert — das erste, das
    greift, gewinnt. Greift keines, gibt es keinen Wert (nichts raten).
    """
    liste = [muster] if isinstance(muster, str) else muster
    for a in abschnitte:
        for m in liste:
            treffer = re.search(m, a.block, re.IGNORECASE)
            if treffer:
                return Treffer(wert=treffer.group(1).strip(), anker=treffer.group(0).strip(),
                               abschnitt=a, seite=a.seite_fuer(treffer.start()))
    return None


def norm_bezug(abschnitte: list[Abschnitt], cfg: dict) -> list[Treffer]:
    """Zitierte Regelwerke — reine Nennung, NIE eine Wertübernahme.

    Eine LB, die „EN 1838" nennt, hat damit KEINE Lux-Zahl und KEINE Dauer
    vorgegeben. Der Normbezug ist Dokumentation, kein Wert.
    """
    gefunden: dict[str, Treffer] = {}
    for a in abschnitte:
        block = a.block
        for name, muster_liste in cfg.items():
            if name in gefunden:
                continue
            for m in muster_liste:
                treffer = re.search(m, block, re.IGNORECASE)
                if treffer:
                    gefunden[name] = Treffer(wert=name, anker=treffer.group(0).strip(),
                                             abschnitt=a, seite=a.seite_fuer(treffer.start()))
                    break
    return list(gefunden.values())


# ── Bereiche (Exklusion / Inklusion) ───────────────────────────────────────

@dataclass(frozen=True)
class BereichsTreffer:
    raum_typ: str
    sicherheitsbeleuchtung: bool
    begruendung: str | None
    anker: str
    abschnitt: Abschnitt
    seite: int


_WORTANFANG = r"(?<![A-Za-zÄÖÜäöüß])"


def _raum_typen(text: str, vokabular: dict[str, list[str]]) -> list[tuple[str, str]]:
    """(raum_typ, gefundener Begriff) — Treffer nur am WORTANFANG.

    Ohne diese Grenze macht „Not-aus-**gang**" aus jedem Notausgang einen GANG
    und „Ein-**gang**" ebenso — ein stiller Fehlklassifikations-Pfad. Komposita,
    die wirklich gemeint sind (`fluchtgänge`, `wohnungsgänge`), stehen deshalb
    ausgeschrieben im Vokabular. Längere Begriffe zuerst, damit der spezifischere
    gewinnt.
    """
    klein = text.lower()
    ergebnis: list[tuple[str, str]] = []
    for typ, begriffe in vokabular.items():
        for b in sorted(begriffe, key=len, reverse=True):
            if re.search(_WORTANFANG + re.escape(b), klein):
                ergebnis.append((typ, b))
                break
    return ergebnis


def bereiche(abschnitte: list[Abschnitt], cfg: dict) -> list[BereichsTreffer]:
    """Wo verlangt oder verbietet die LB Sicherheitsbeleuchtung?

    Auswertungseinheit ist der Satz bzw. die Aufzählungszeile. Eine Einheit mit
    Negation (`KEINE … herzustellen`) ergibt eine Exklusion, eine Einheit mit
    positivem Muster (`… wird in … ausgeführt`) eine Inklusion. Aufzählungszeilen
    innerhalb eines Notbeleuchtungs-Abschnitts gelten als Inklusion — das ist das
    Listen-Idiom „In folgenden Bereichen werden … installiert:".
    """
    vokabular = cfg["raum_typ_vokabular"]
    negation = [re.compile(m) for m in cfg["negation_muster"]]
    inklusion = [re.compile(m, re.IGNORECASE) for m in cfg["inklusion_muster"]]
    bullet = re.compile(cfg["struktur"]["bullet_muster"])
    begruendung_rx = re.compile(cfg["begruendung_muster"])

    ergebnis: dict[tuple[str, bool], BereichsTreffer] = {}

    for a in abschnitte:
        # Auswertungseinheiten MIT ihrer Seite: Aufzählungszeilen direkt aus den
        # Zeilen-Einträgen, Sätze über den Offset-Index des Blocks.
        einheiten: list[tuple[str, int]] = [
            (m.group(1), seite) for z, seite in a.eintraege if (m := bullet.match(z))
        ]
        bullets = {t for t, _ in einheiten}
        einheiten += a.saetze()
        # Die Überschrift ist selbst eine Auswertungseinheit: reale LBs stecken die
        # ganze Aussage hinein („2.11 In der Garage ist eine LED-Sicherheits-
        # beleuchtung herzustellen."). Sie steht dann in KEINEM Satz des Blocks.
        einheiten.append((a.titel, a.seite))

        for einheit, seite in einheiten:
            typen = _raum_typen(einheit, vokabular)
            if not typen:
                # Die Überschrift kann den Bereich tragen: „…beleuchtung (Garage)".
                typen = _raum_typen(a.titel, vokabular)
                if not typen or not any(rx.search(einheit) for rx in inklusion):
                    continue
            negativ = any(rx.search(einheit) for rx in negation)
            positiv = any(rx.search(einheit) for rx in inklusion) or einheit in bullets
            if not negativ and not positiv:
                continue
            grund = begruendung_rx.search(einheit) or begruendung_rx.search(a.block)
            for typ, begriff in typen:
                schluessel = (typ, not negativ)
                if schluessel in ergebnis:
                    continue
                ergebnis[schluessel] = BereichsTreffer(
                    raum_typ=typ,
                    sicherheitsbeleuchtung=not negativ,
                    begruendung=grund.group(1).replace(" ", "") if grund else None,
                    anker=begriff,
                    abschnitt=a,
                    seite=seite,
                )
    return list(ergebnis.values())
