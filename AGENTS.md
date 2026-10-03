# AGENTS.md — Projekt-Instruktion für Codex

Dieses Projekt baut eine Engine, die aus **leerem Architekturplan (DXF) + LB**
einen ÖNorm/EN-1838-konformen **Notbeleuchtungsplan** erzeugt. Die vollen
Arbeitsregeln stehen in **`CLAUDE.md`** (Owner-Grenzen, Contracts, Verifikations-
strecke, Don'ts) — lies sie als Projekt-Kontext.

## Für CODE-REVIEWS (BINDEND)

**Vor jedem Review `docs/CODEX_REVIEW_BRIEF.md` lesen.** Der Brief gibt dir das
ZIEL: die fertigen Experten-Notbeleuchtungspläne (Mollgasse-Erklär-DXF + Analyse-
Docs als Soll), den gemessenen Ist↔Soll-Abstand (GT-Harness
`scripts/analyse/mollgasse_gt_vergleich.py`), die Lane-Grenzen und was dein Review
zeigen soll.

**Kern-Abgrenzung (Vision):** Der Plan-Output = NUR die Notbeleuchtungs-**Symbole**
(Rettungszeichen/Notleuchten, Sicherheitsleuchten/Aufheller, Antipanikleuchten) —
mit korrekter Position, Pfeilrichtung und Typ. Die grünen Fluchtweg-Linien,
türkisen Sichtlinien und grünen Menschensymbole in den Erklär-Plänen sind reine
**Erklärungs-Overlays** (für die PDFs), KEIN Plan-Element und KEIN Review-Ziel.
Details + „welche Punkte ein Notbeleuchtungsplan beachten muss" stehen im Brief.

Reviewe ziel-gerichtet, nicht nur Code-Korrektheit:
1. echte Bugs/Regressions der Änderung;
2. bringt die Änderung die Platzierung NÄHER an den fertigen Experten-Plan
   (gepaart/typ_match/Distanz) oder weiter weg;
3. der höchstwertige NÄCHSTE Schritt in der Leonis-Lane
   (`src/notbeleuchtung/platzierung/`) Richtung Ziel, mit Beleg (RW-### / GT-Fall /
   Datei:Zeile);
4. was am verbleibenden Abstand Selman- (`raumerkennung/`) oder Enis-
   (`normwissen/`) gegated ist — klar abgrenzen, NICHT als Leonis-To-do ausgeben.

## Vorrang (schlägt Codex-Rat)

Regelquellen aus `CLAUDE.md` (Norm-YAML, `platzierung/regelwerk.py` +
`data/notbeleuchtung_regeln.json`, Contracts). Ein Finding, das eine Regelquelle
verletzt, wird mit Begründung verworfen.
