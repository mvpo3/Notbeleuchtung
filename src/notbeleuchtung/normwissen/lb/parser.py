"""parser — Leistungsbeschreibung (Freitext/PDF) → LBVorgabe.

Heuristischer Feld-Extraktor (kein Full-NLP, s. LB_ANALYSE_beispiele.md #4): liest den
LB-Text (PDF via pypdf, sonst Textdatei) und leitet die expliziten Vorgaben ab, die den
Norm-Default übersteuern. Kernfall (Fischa §2.10/2.11, GK4): Stiegenhaus + anschließende
Gänge OHNE Sicherheitsbeleuchtung, SL nur in der Garage — der kanonische „LB übersteuert
Norm"-Fall.

Bereichs-Vokabular mappt auf Selmans RaumModell-Labels (STIEGENHAUS/GANG/GARAGE …), sonst
greift die Regel im Platzierer nicht. Nicht gefundene Felder bleiben `None`/leer →
Norm-Default. `lb_quelle` trägt den Datei-Namen als Audit-Trail.
"""
from __future__ import annotations

import re
from pathlib import Path

from notbeleuchtung.hauptengine.contracts.lb_vorgabe import (
    BereichsRegel,
    LBVorgabe,
    SonderLux,
)

# Deutsche Oberflächenform → kanonisches RaumModell-Label (Selman-Vokabular).
_BEREICH_VOCAB: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"stiegenh|treppenh|\bstiege", re.IGNORECASE), "STIEGENHAUS"),
    (re.compile(r"g[aä]nge?\b|korridor|\bflur", re.IGNORECASE), "GANG"),
    (re.compile(r"garage|tiefgarage|einstellr|stellpl", re.IGNORECASE), "GARAGE"),
    (re.compile(r"technikr", re.IGNORECASE), "TECHNIK"),
    (re.compile(r"lagerr|abstellr", re.IGNORECASE), "LAGER"),
    (re.compile(r"m[üu]llr", re.IGNORECASE), "MUELLRAUM"),
]

_SL = r"(?:sicherheitsbeleuchtung|sicherheitsleuchte|led-sicherheit|notbeleuchtung)"

# Lux-Einheit: Abkürzung „lx" ODER ausgeschriebenes „Lux" (reale LBs mischen beides).
_LUX = r"(?:lx|lux)"
# Plausibilitäts-Caps gegen Fremdzahl-Treffer (s. Docstrings unten).
_LUX_FLUCHTWEG_CAP = 20.0        # EN 1838: Fluchtweg-Mittellinie 1 lx, Antipanik 0,5 lx
_BETRIEBSDAUER_CAP_MIN = 1440    # 24 h — darüber kein Notlicht-Betriebsdauerwert


def _lies_text(pfad: str | Path) -> str:
    """LB-Text laden — PDF via pypdf, sonst Datei als Text."""
    p = Path(pfad)
    if p.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        return "\n".join(page.extract_text() or "" for page in PdfReader(str(p)).pages)
    return p.read_text(encoding="utf-8", errors="ignore")


def _saetze(text: str) -> list[str]:
    """Grobe Satz-Segmentierung: Zeilenumbrüche zu Space (LB-Sätze brechen um), dann `.;!`."""
    flach = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"[.;!]+", flach) if s.strip()]


def _bereiche(text: str) -> tuple[list[BereichsRegel], list[BereichsRegel]]:
    """(inklusion, exklusion): Sätze mit/ohne Sicherheitsbeleuchtung → BereichsRegel."""
    gk = _gebaeudeklasse(text)
    inkl: dict[str, BereichsRegel] = {}
    exkl: dict[str, BereichsRegel] = {}
    for satz in _saetze(text):
        if not re.search(_SL, satz, re.IGNORECASE):
            continue
        treffer = [label for pat, label in _BEREICH_VOCAB if pat.search(satz)]
        if not treffer:
            continue
        # „keine/kein/ohne … Sicherheitsbeleuchtung" = Exklusion, sonst Inklusion.
        ist_exkl = bool(re.search(r"\bkeine?\b|\bohne\b|nicht\s+her", satz, re.IGNORECASE))
        ziel, flag = (exkl, False) if ist_exkl else (inkl, True)
        for label in treffer:
            if label not in ziel:
                ziel[label] = BereichsRegel(
                    raum_typ=label,
                    sicherheitsbeleuchtung=flag,
                    begruendung=gk if (ist_exkl and gk) else None,
                )
    # Kollision (gleicher Typ inkl+exkl): Exklusion (Hard-Override) gewinnt.
    for label in set(inkl) & set(exkl):
        del inkl[label]
    return list(inkl.values()), list(exkl.values())


def _gebaeudeklasse(text: str) -> str | None:
    m = re.search(r"\bGK\s?([1-5])\b|Geb[äa]udeklasse\s+([1-5])", text, re.IGNORECASE)
    if not m:
        return None
    return f"GK{m.group(1) or m.group(2)}"


def _betriebsdauer_min(text: str) -> int | None:
    """Notlicht-Betriebsdauer (Minuten) — nur im Batterie-/Betriebsdauer-Kontext.

    Härtet gegen Fremdzahlen ohne Notlicht-Bezug: „24 Stunden nach Verständigung"
    (Gewährleistung), „123 H SCHLUSSER" (bare-`h` an Fremdwort) und „…Batterie des
    Notrufsystems … 24 Stunden" (fremdes Batteriesystem) werden verworfen — im Fenster
    muss `(nenn)betriebsdauer|auszulegen` stehen und **kein** `notruf`. Bare `h` nur
    direkt an der Ziffer (`8h`), nie `\\s+h`. Dezimal erlaubt (8,5 Std → 510). Werte
    über _BETRIEBSDAUER_CAP_MIN (24 h) sind implausibel.
    """
    # Ganzzahl auf 1–4 Stellen begrenzt: sonst macht eine sehr lange Ziffernfolge
    # float()=inf → round(inf*60) crasht. Der Cap 1440 (24 h) fängt Reste ab.
    muster = r"(\d{1,4}(?:[.,]\d{1,2})?)(?:\s*(?:Std\.?|Stunden)|h)\b"
    for m in re.finditer(muster, text, re.IGNORECASE):
        fenster = text[max(0, m.start() - 80): m.end() + 20]
        if not re.search(r"betriebsdauer|auszulegen", fenster, re.IGNORECASE):
            continue
        # notruf nur lokal am Treffer prüfen (nicht über 80er-Fenster in Nachbarsatz bluten).
        if re.search(r"notruf", text[max(0, m.start() - 40): m.end() + 10], re.IGNORECASE):
            continue
        minuten = round(float(m.group(1).replace(",", ".")) * 60)
        if minuten > _BETRIEBSDAUER_CAP_MIN:
            continue
        return minuten
    return None


def _umschaltzeit_s(text: str) -> float | None:
    m = re.search(r"[<≤]\s*([0-9]+(?:[.,][0-9]+)?)\s*s\b", text)
    return float(m.group(1).replace(",", ".")) if m else None


def _mindest_lux_fluchtweg(text: str) -> float | None:
    """Fluchtweg-Mindestbeleuchtungsstärke (lx) — nur im Fluchtweg-Kontext.

    `_mindest_lux` alt griff das erste `\\d+ lx` im Doc (mo-Elektro: „200 lx"
    Aufzugsvorplatz). Neu: der Wert muss im Fenster `fluchtweg|rettungsweg|
    orientierungsbeleuchtung` stehen und darf nicht bei `feuerl|hydrant` liegen
    (das ist Sonder-Lux). Ein direkt links vorangestelltes `antipanik` disqualifiziert
    den Wert (Antipanik 0,5 lx ist eine andere Größe als die Fluchtweg-Mittellinie
    1 lx) — sonst zöge `min()` den Antipanik-Wert. Nimmt das Minimum der verbleibenden
    Kandidaten (EN-1838-Mindestwert; reale LBs nennen „1 Lux" mehrfach) und verwirft
    Werte über _LUX_FLUCHTWEG_CAP.
    """
    kandidaten: list[float] = []
    for m in re.finditer(r"(\d+(?:[.,]\d+)?)\s*" + _LUX + r"\b", text, re.IGNORECASE):
        fenster = text[max(0, m.start() - 70): m.end() + 15]
        if not re.search(r"fluchtweg|rettungsweg|orientierungsbeleuchtung",
                         fenster, re.IGNORECASE):
            continue
        if re.search(r"feuerl|hydrant", fenster, re.IGNORECASE):
            continue
        # Antipanik-Wert (0,5 lx) direkt links vom Zahlwert → nicht die Fluchtweg-Größe.
        if re.search(r"antipanik", text[max(0, m.start() - 60): m.start()], re.IGNORECASE):
            continue
        wert = float(m.group(1).replace(",", "."))
        if wert <= _LUX_FLUCHTWEG_CAP:
            kandidaten.append(wert)
    return min(kandidaten) if kandidaten else None


def _system_typ(text: str) -> str | None:
    for surface, canon in (("zentralbatterie", "zentralbatterie"),
                           ("gruppenbatterie", "gruppenbatterie"),
                           ("einzelbatterie", "einzelbatterie")):
        if re.search(surface, text, re.IGNORECASE):
            return canon
    return None


def _batterie_standort(text: str) -> str | None:
    """Standort der (Gruppen-/Zentral-)Batterie — nur wenn nahe `batterie` ein `im/in <Raum>`
    steht (Fischa: „Gruppenbatterie im Technikraum" → „Technikraum"). Nichts raten: ohne
    belegtes Muster None. Whitespace flach (LB-Sätze brechen um)."""
    flach = re.sub(r"\s+", " ", text)
    # Standort muss raum-artig sein (…raum / Keller…) — sonst greift „Batterien in
    # Einzelleuchten" → „Einzelleuchten". Kein Raum-Wort in Reichweite → None.
    m = re.search(
        r"batterie\w*\s+(?:im|in\s+(?:dem|der)?)\s*([A-ZÄÖÜ][\wäöüß-]*raum|Keller[\wäöüß-]*)",
        flach,
        re.IGNORECASE,
    )
    return m.group(1) if m else None


def _ueberwachung(text: str) -> str | None:
    if re.search(r"einzelleuchten?überwach|einzelleuchten?\b", text, re.IGNORECASE):
        return "einzelleuchte"
    if re.search(r"zentral.?überwach", text, re.IGNORECASE):
        return "zentral"
    return None


def _pruefung(text: str) -> str | None:
    if re.search(r"\bweb\b|web-?basiert|controller.*lan|lan.*controller", text, re.IGNORECASE):
        return "web"
    if re.search(r"automatische?\s+(?:pr[üu]f|test)", text, re.IGNORECASE):
        return "automatisch"
    return None


def _sonder_lux(text: str) -> list[SonderLux]:
    # Whitespace flach: reale LBs brechen „…situiert werden.\n(mindestens 5 Lux)" um.
    flach = re.sub(r"\s+", " ", text)
    out: list[SonderLux] = []
    for surface, ort in ((r"feuerl(?:ö|oe|o)scher", "feuerloescher"), (r"hydrant", "hydrant")):
        m = re.search(surface + r".{0,110}?(\d+(?:[.,]\d+)?)\s*" + _LUX + r"\b",
                      flach, re.IGNORECASE)
        if m:
            out.append(SonderLux(ort=ort, min_lux=float(m.group(1).replace(",", "."))))
    return out


def _norm_bezug(text: str) -> list[str]:
    muster = [
        (r"EN\s?ISO\s?7010", "EN ISO 7010"),
        (r"EN\s?1838", "EN 1838"),
        (r"[ÖO]VE\s?E?\s?8101", "OVE E 8101"),
        (r"R\s?12-?2", "OVE R 12-2"),
        (r"[ÖO]NORM\s?Z\s?1000", "ÖNORM Z1000"),
        (r"EN\s?IEC\s?62485", "EN IEC 62485-2"),
    ]
    return [canon for pat, canon in muster if re.search(pat, text, re.IGNORECASE)]


def _piktogramm(text: str) -> str | None:
    return "EN ISO 7010" if re.search(r"EN\s?ISO\s?7010", text, re.IGNORECASE) else None


def parse_lb(lb_path: str) -> LBVorgabe:
    """Leistungsbeschreibung (PDF/Text) → LBVorgabe (explizite, norm-übersteuernde Vorgaben)."""
    text = _lies_text(lb_path)
    inkl, exkl = _bereiche(text)
    return LBVorgabe(
        projekt=Path(lb_path).stem,
        system_typ=_system_typ(text),
        batterie_standort=_batterie_standort(text),
        betriebsdauer_min=_betriebsdauer_min(text),
        umschaltzeit_max_s=_umschaltzeit_s(text),
        mindest_lux_fluchtweg=_mindest_lux_fluchtweg(text),
        ueberwachung=_ueberwachung(text),
        pruefung=_pruefung(text),
        piktogramm_norm=_piktogramm(text),
        bereiche_inklusion=inkl,
        bereiche_exklusion=exkl,
        sonder_lux=_sonder_lux(text),
        norm_bezug=_norm_bezug(text),
        lb_quelle=Path(lb_path).name,
    )


class LbTextProvider:
    """Erfüllt das ``LBProvider``-Protocol (``parse_lb(lb_path) -> LBVorgabe``)."""

    def parse_lb(self, lb_path: str) -> LBVorgabe:
        return parse_lb(lb_path)
