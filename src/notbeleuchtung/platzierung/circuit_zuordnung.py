"""circuit_zuordnung — zentrale Stromkreis-Vergabe für die fertige Platzierung.

Die Einzel-Strategien setzen `circuit_hint` grob als `AGV-{Gebäude}-F13`: alle Leuchten
eines Gebäudeflügels landen auf **einem** Kreis, Rettungszeichen (Dauerlicht) und
Sicherheits-/Antipanik-Leuchten (Bereitschaftslicht) **gemischt** (Befund F2, #78 aus der
echten Belegungsliste). Praxis (§3b): Dauer- und Bereitschaftslicht gehören auf **getrennte**
Endstromkreise, und je Kreis gilt eine Leuchten-Obergrenze.

Dieser Nach-Pass (läuft in `platzierer.place`, nachdem alle Leuchten stehen) ordnet je
(Gebäude, Schaltungsart) fortlaufende, gedeckelte Kreise zu:
`AGV-{Gebäude}-F13-{DL|BL}-{n}`. Die `F13`-SV-Kennung bleibt erhalten — sie ist die Naht
zur „getrennter Sicherheitskreis"-Prüfung in `validierung`. Render-frei, kein Contract
(rewritet nur das vorhandene Feld `circuit_hint`).
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


def _gebaeude(circuit_hint: str) -> str:
    """Gebäude-/Flügel-Kennung aus dem groben Strategie-Hint (`AGV-<X>-…`); sonst 'A'."""
    m = _GEBAEUDE_RE.match((circuit_hint or "").strip())
    return m.group(1) if m else "A"


def zuordnen(platzierungen: list[Platzierung]) -> list[Platzierung]:
    """Rewritet `circuit_hint` je (Gebäude, Schaltungsart) mit fortlaufender, gedeckelter
    Kreisnummer → `AGV-{Gebäude}-F13-{DL|BL}-{n}`. Mutiert die Eingabe nicht (neue Liste)."""
    kreis_nr: dict[tuple[str, str], int] = {}
    n_im_kreis: dict[tuple[str, str], int] = {}
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
        out.append(p.model_copy(update={"circuit_hint": hint}))
    return out
