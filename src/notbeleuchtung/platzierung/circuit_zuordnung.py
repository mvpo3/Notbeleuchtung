"""circuit_zuordnung — zentrale Stromkreis-Vergabe für die fertige Platzierung.

Die Einzel-Strategien setzen `circuit_hint` grob als `AGV-{Gebäude}-F13`: alle Leuchten
eines Gebäudeflügels landen auf **einem** Kreis, Rettungszeichen (Dauerlicht) und
Sicherheits-/Antipanik-Leuchten (Bereitschaftslicht) **gemischt** (Befund F2, #78 aus der
echten Belegungsliste). Praxis (§3b): Dauer- und Bereitschaftslicht gehören auf **getrennte**
Endstromkreise, und je Kreis gilt eine Leuchten-Obergrenze.

Dieser Nach-Pass (läuft in `platzierer.place`, nachdem alle Leuchten stehen) ordnet je
(Gebäude, Schaltungsart) fortlaufende, gedeckelte Kreise zu:
`AGV-{Gebäude}-F13-{DL|BL}-{n}`. Die `F13`-SV-Kennung bleibt erhalten — sie ist die Naht
zur „getrennter Sicherheitskreis"-Prüfung in `validierung`. Render-frei.

Seit `PlatzierungsErgebnis` v1.2.0 füllt der Pass zusätzlich das Symbol-Datenmodell
(Digest #6), weil er als letzter die endgültige Reihenfolge sieht:
`schaltungsart` (DL/BL — bisher nur eine Render-Heuristik), `luminaire_id`
(RZ-001/SL-002/…, dasselbe Schema, das der Render bisher synthetisierte) und
`typ_letter` (Legenden-Letter A/B/… je `catalog_key`, Reihenfolge des ersten
Auftretens — Grundlage der Typ-Letter-Stückliste #7).
"""
from __future__ import annotations

import re

from notbeleuchtung.hauptengine.contracts import Platzierung

# Schaltungsart je Leuchtenart: Rettungszeichen = Dauerlicht (maintained, muss immer
# leuchten), Sicherheits-/Antipanik-Leuchten = Bereitschaftslicht (non-maintained).
_SCHALTUNGSART = {"rz": "DL", "sicherheitsleuchte": "BL", "antipanik": "BL"}

# Leuchten-Obergrenze je Endstromkreis. PLATZHALTER: die echte Grenze ist strombasiert
# (§3b, Leuchten-Nennstrom gegen den Kreis-Schutz, Größenordnung 115/350 mA) und braucht
# die Produkt-Stromaufnahme je Leuchte — die liegt erst mit dem erweiterten Symbol-
# Datenmodell (Digest-Empfehlung #6) bzw. aus der LB vor. Bis dahin ein konservativer,
# klar benannter Stückzahl-Deckel.
_MAX_LEUCHTEN_JE_KREIS = 20

_AGV_SV_F = 13  # SV-Kennung (getrennter Sicherheitskreis) — Naht-Invariante zu validierung.
_GEBAEUDE_RE = re.compile(r"AGV-([A-Za-z0-9]+)-")

# Kurz-Codes für die Leuchten-ID (identisch zum bisherigen Render-Schema).
_KIND_CODE = {"rz": "RZ", "sicherheitsleuchte": "SL", "antipanik": "AP"}

_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _typ_letter(index: int) -> str:
    """Legenden-Letter je catalog_key: A..Z, danach T27, T28, … (nie mehrdeutig)."""
    return _LETTERS[index] if index < len(_LETTERS) else f"T{index + 1}"


def _gebaeude(circuit_hint: str) -> str:
    """Gebäude-/Flügel-Kennung aus dem groben Strategie-Hint (`AGV-<X>-…`); sonst 'A'."""
    m = _GEBAEUDE_RE.match((circuit_hint or "").strip())
    return m.group(1) if m else "A"


def zuordnen(platzierungen: list[Platzierung]) -> list[Platzierung]:
    """Rewritet `circuit_hint` je (Gebäude, Schaltungsart) mit fortlaufender, gedeckelter
    Kreisnummer → `AGV-{Gebäude}-F13-{DL|BL}-{n}` und füllt das Symbol-Datenmodell
    (`schaltungsart`, `luminaire_id`, `typ_letter`). Mutiert die Eingabe nicht."""
    kreis_nr: dict[tuple[str, str], int] = {}
    n_im_kreis: dict[tuple[str, str], int] = {}
    id_zaehler: dict[str, int] = {}
    letter_je_key: dict[str, str] = {}
    out: list[Platzierung] = []
    for p in platzierungen:
        art = _SCHALTUNGSART.get(p.kind, "BL")
        key = (_gebaeude(p.circuit_hint), art)
        if key not in kreis_nr:
            kreis_nr[key], n_im_kreis[key] = 1, 0
        if n_im_kreis[key] >= _MAX_LEUCHTEN_JE_KREIS:
            kreis_nr[key] += 1
            n_im_kreis[key] = 0
        n_im_kreis[key] += 1
        hint = f"AGV-{key[0]}-F{_AGV_SV_F}-{art}-{kreis_nr[key]}"

        code = _KIND_CODE.get(p.kind, "XX")
        id_zaehler[code] = id_zaehler.get(code, 0) + 1
        if p.catalog_key not in letter_je_key:
            letter_je_key[p.catalog_key] = _typ_letter(len(letter_je_key))
        out.append(p.model_copy(update={
            "circuit_hint": hint,
            "schaltungsart": art,
            "luminaire_id": f"{code}-{id_zaehler[code]:03d}",
            "typ_letter": letter_je_key[p.catalog_key],
        }))
    return out
