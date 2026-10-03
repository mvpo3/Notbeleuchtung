# Codex-Review-Brief — das ZIEL kennen, dann reviewen

Dieser Brief wird jedem `codex review` als Prompt-Kontext mitgegeben (via stdin
`-`), damit Codex **ziel-gerichtet** prüft: nicht nur Code-Korrektheit, sondern ob
die Änderung die Engine näher an die **fertigen Experten-Notbeleuchtungspläne**
bringt — und was der nächste beste Schritt dorthin ist.

## Mission (das Ziel)

Die Engine erzeugt aus **leerem Architekturplan (DXF) + Leistungsbeschreibung (LB)**
einen ÖNorm/EN-1838-konformen **Notbeleuchtungsplan** (Rettungszeichen +
Sicherheitsleuchten + Antipanik, getrennter Sicherheitskreis). Das SOLL ist, die
von Profis gezeichneten **fertigen** Pläne zu reproduzieren.

## Die fertigen Pläne = das Soll (hier liegt das Ziel)

Primär **Mollgasse** (8 Geschosse, autoritativer Lehrsatz, mit Mess-Harness):
- Experten-Erklärungs-DXF (fertiger Notbeleuchtungsplan):
  `knowledge/Pläne zeichnen Wissen/Mollgasse-Notbeleuchtungserklärung/WHA_MOL_<G>_Notbeleuchtung_Erklärung.dxf`
  + 95-S-Lehr-PDF `Notbeleuchtungen zeichnen.pdf`.
- **Text-Form (für dich, Codex, direkt lesbar)** im `_Analyse/`-Ordner daneben:
  - `REGELWERK_Mollgasse.md` — die Zeichenregeln des fertigen Plans (RW-001..035).
  - `ANALYSE_DXF_<G>.md` — die SOLL-Platzierungen je Geschoss (Handle, Position,
    Pfeilrichtung, Welt-Pfeil) der fertigen Pläne.
  - `ANALYSE_PDF.md` — 283 Warum-Regeln; `REVIEW.md` — Ist-vs-Soll-Analyse;
    `GEGENPRUEFUNG_ENGINE.md` — Regel-Deckung Engine↔Experte.

Weitere fertige Referenzen (im selben `knowledge/Pläne zeichnen Wissen/`):
- **Hausfeld** (`_Analyse_Regelwerk/ANALYSE_Hausfeld.md`) — WÄCHTER: NICHT
  down-dominant (2DG 3/3 RZ `left`); eine „Stiegen-RZ⇒down"-Heuristik bricht hier.
- Tomaschek (Schule, eigene Raumtypen), Am Rain (Bestands-/Quellen-Disziplin),
  Baufeld-E2-UG (Lehrlayer-GT, Flucht hinauf).

## Der gemessene Ist↔Soll-Abstand (so weißt du, wo wir stehen)

Harness `scripts/analyse/mollgasse_gt_vergleich.py <G>` → leerer Plan → Engine
`pipeline.run` ↔ Experten-GT (`tests/fixtures/mollgasse_gt/<G>.json`), Ausgabe
`Projekte/_ergebnis/Mollgasse_GT/<G>/{bericht.md,vergleich.json}`:
Kennzahlen **gepaart / typ_match / fehlt / überflüssig / Paarungs-Distanz**.
Aktueller Stand (grob): ~33/97 gepaart, ~13 typ_match über 8 Geschosse.

## Lane-Grenzen (was ist wessen Baustelle)

- **Leonis = `src/notbeleuchtung/platzierung/`** (diese Lane). Nur hier fixen.
- **Selman = `raumerkennung/`** (Räume/Türen/Ausgänge/Zirkulation). Vieles am
  GT-Abstand ist Selman-gegated: leerer Zirkulations-Knotengraph (`nodes/edges`),
  KG-/Garage-Erkennung, Ausgänge außerhalb Raumpolygonen, beidseitig-Wasserscheide.
- **Enis = `normwissen/`** (Norm-Werte/LB). Leonis parst kein YAML, fragt den
  NormProvider.
- Voller Einbau-Stand + was Selman-/Enis-gegated ist:
  `docs/EINBAU_FAHRPLAN_Platzierungslogik_2026-10-03.md`.
- Empirisch bestätigt (2026-10-03): die großen Stiegen-RZ-Distanzen sind
  Ausgangsachsen-/directional-Miss (Selman-Knotengraph + M3-Teil-2), KEIN
  Leonis-Band-Tweak (S-C verworfen).

## Regelquellen-Vorrang (schlägt Codex)

`CLAUDE.md` · `docs/{PROGRAMM_NOTBELEUCHTUNG,COORDINATION,VOKABULAR,CONTRACTS}.md`
+ `docs/adr/` · Norm (`normwissen/data/*.yaml`, `platzierung/regelwerk.py` +
`data/notbeleuchtung_regeln.json`) · Verträge (`hauptengine/contracts/*.py`).
Ein Codex-Finding, das eine Regelquelle verletzt, wird mit Begründung verworfen.

## Was dein Review zeigen soll (zusätzlich zu Bugs)

1. **Korrektheit:** echte Bugs/Regressions der Änderung.
2. **Ziel-Richtung:** bringt die Änderung die Platzierung NÄHER an den fertigen
   Experten-Plan (gepaart/typ_match/Distanz) oder weiter weg? Woran erkennbar?
3. **Nächster Schritt:** der höchstwertige NÄCHSTE Leonis-Schritt Richtung Ziel,
   mit Beleg (Regel-ID RW-###, GT-Fall, Datei:Zeile).
4. **Lane-Abgrenzung:** was am verbleibenden Abstand Selman-/Enis-gegated ist (nicht
   in dieser Lane fixbar) — klar benennen, nicht als Leonis-To-do ausgeben.
