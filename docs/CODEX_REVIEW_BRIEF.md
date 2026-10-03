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

## Der Plan-Output = NUR die Notbeleuchtungs-SYMBOLE (WICHTIGSTE Abgrenzung)

Das SOLL, das die Engine reproduziert, sind **ausschließlich die Notbeleuchtungs-
SYMBOLE** — die Leuchten selbst:

- **Rettungszeichen (RZ / „Notleuchten")** — die Pfeil-Piktogramme (`kind="rz"`,
  Blöcke `RIVO_ARR_down/left/right/bothsided`). Zählen: Position, **Pfeilrichtung/
  Rotation**, Typ (down/left/right/beidseitig), Montageart (Wand/Decke).
- **Sicherheitsleuchten (SL)** inkl. **Aufheller** (`kind="sicherheitsleuchte"`) —
  Wegbeleuchtung/Aufhellung.
- **Antipanikleuchten** (`kind="antipanik"`) — Flächen/Sichtblockade.

Je Symbol: Position, Typ, Pfeil/Rotation, Montageart, Stromkreis (getrennter
SV-Kreis), Montagehöhe. Der GT-Vergleich (`mollgasse_gt_vergleich`) paart **nur
diese Symbolklassen** (rz / sicherheitsleuchte / antipanik).

**NICHT Teil des Outputs — reine ERKLÄRUNGS-OVERLAYS** (nur für die Erklärungs-
PDFs/-DXFs; NICHT als Soll werten, NICHT reproduzieren, kein Mangel wenn sie im
Engine-Output fehlen):

- grüne **Fluchtweg-Linien** (Fluchtweg-Achse; Layer `Fluchtlinien_*`),
- türkise **Sichtlinien** (ACI 4 „was die Person sieht"; Layer `*WEG_*INTERPRETATION`),
- grüne **Menschensymbole** / Läufer + deren Blickrichtungen (Layer `LEHR_MENSCH_*`,
  `LEHRPERSON_*`),
- Kennungen (A)/(B)/…, rote Bestands-Raumlabels, gelbe Konstruktions-Hilfslinien.

Diese erklären WARUM ein Symbol so sitzt (Didaktik). Ein Review darf sie **nie** als
Ziel-Output oder als fehlendes Engine-Element behandeln.

## Wie ein korrekter Notbeleuchtungsplan aussieht — Punkte zu beachten

Prüf-Kriterien für die Symbol-Platzierung (Norm/Referenz-Praxis; Beleg je Punkt in
`REGELWERK_Mollgasse.md`/`notbeleuchtung_regeln.json`/`validierung.py`):

1. **RZ an jedem Notausgang** (final_exit/stair_exit) — EN 1838 §4.1.2 g.
2. **Tür-RZ mittig auf der Tür**, Pfeil ins Rauminnere bzw. zum Fluchtweg (RW-001);
   KEIN fixer Raum-Versatz (Owner 2026-10-03).
3. **RZ-Pfeiltyp = Frontalsicht der ankommenden Person**, NICHT Weltrichtung
   (RW-006/007 = „M3"): weißer Balken zur Person, Pfeil kann entgegen der
   Gehrichtung zeigen. Block-Variante (links/rechts/unten) ≠ Weltrichtung.
4. **Erster-Blick-Regel**: beim Verlassen jedes Raums/jeder Wohnung muss ≥1 Leuchte
   sichtbar sein; **Sichtkette** — jede Leuchte sieht die nächste (RW-008/NB-R12).
5. **Stiegen-RZ** in Lauf-/Abstiegsrichtung; **UG flüchtet HINAUF** (RW-004/005/013).
6. **Antipanik** bei Sichtblockade (L-/U-Form) bzw. Flächen (EN 1838 §4.3), nicht
   pauschal nach m²; Position = Diagonalen-Mitte (RW-029).
7. **beidseitig** nur an echten Wasserscheiden — **EIN Block** `RIVO_ARR_bothsided`
   (RW-016, Owner 2026-10-03), nicht zwei Einzel-RZ.
8. **Keine Leuchten in privaten Wohnräumen** (`WOHNUNG_PRIVAT`); Wohnungs-Gänge ohne
   Fluchtweg/Communal bekommen keine Korridor-Aufheller.
9. **Getrennter Sicherheitskreis** (F13-Kennung je Symbol), **Montagehöhe ≥ 2 m**,
   **2-Leuchten-Redundanz** je Fluchtweg-Abschnitt (EN 50172).
10. **Keine Symbole in Lift/Schacht**; Außenleuchte am letzten Ausgang (§4.1.2 b).

Ziel ist, dass die Symbol-Platzierung der Engine die der fertigen Experten-Pläne
trifft (Position/Typ/Pfeil) — gemessen über gepaart / typ_match / Distanz.

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
