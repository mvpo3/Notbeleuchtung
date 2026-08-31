> **Quelle:** Multi-Agent-DoD-Audit (ultracode), 8 Geschosse Mollgasse durch die Engine
> (`run_projekt` + reale LB) → je Geschoss ein Sicht-Auditor-Agent auf dem gerenderten PNG,
> danach Synthese. Reproduzieren: Sammel-PDF unter `output/dod/projekt/` (gitignored).
> Stand 2026-08-31, Prüfer: Leonis (F1) + 8 Audit-Subagenten.
>
> **Update seit Audit:** Der F1-Validierungs-Blocker (P0 #3 — quasi-leere Pläne als
> „ok") ist **behoben** (Regel „Plan-Plausibilität" mit Symboldichte-Gate: DG **und**
> OG→**fehler** — 0-2 Symbole bei >100 Räumen = kein valider Plan). Die restlichen
> F1-Punkte (Legende/Plankopf sichtbar ✓, RZ/SL ✓ verifiziert, Höhenkoten ✓, Schriftfeld-
> Leiste ✓, RZ an Notausgängen ✓) sind erledigt; F2-Punkte (OG/DG-Raumerkennung) offen.

# DoD-Sichtprüfungs-Bericht — Mollgasse Notbeleuchtungsplan (8 Geschosse)

## Gesamturteil

**NEIN — das Gebäude-Plan-Set ist nicht auslieferbar.** Kein einziges der 8 Geschosse ist abnahmefähig. Zwei strukturelle Ursachen dominieren:

1. **F2 (Raumerkennung) liefert flächendeckend keine Raumtypen/Fluchtwege/Ausgänge.** In jedem Geschoss sind praktisch alle Räume typlos (z.B. 254/256, 187/188, 112/112). Ohne Anker kann die Platzierung nichts setzen — 6 der 8 Geschosse sind mit 0–2 Symbolen faktisch leer, das DG rendert nicht einmal einen zusammenhängenden Grundriss.
2. **F1 (Render/Validierung) hat systemische Lücken.** Auf keinem Geschoss sind Legende, Stückliste, Plankopf oder Höhenkoten sichtbar — und der automatische Prüfbericht meldet quasi-leere Pläne (bis hinunter zu 0 Symbolen) als **„ok"** bzw. **„warnung"** statt als Fehler. Ein grüner Status verschleiert damit einen nicht-existenten Plan.

Selbst die „besten" Geschosse (2KG, EG) mit ~30–40 Symbolen scheitern an fehlender Legende/Stückliste/Plankopf/Höhenkoten und generischer Flächenverteilung statt fluchtweg-orientierter Platzierung.

## Geschoss-Übersicht

| Geschoss | Symbole | Räume o. Typ | Leer? | Kernbefund |
|----------|--------:|--------------|:-----:|------------|
| 2KG | 40 | 51/52 | nein | Bestückt, aber Legende/Plankopf/Höhenkoten fehlen; nur 2 RZ, generische Flächenverteilung statt Fluchtweg-Orientierung |
| 1KG | 25 | 62/64 | teilw. | Rechter Flügel plausibel, linker Flügel (~½ Fläche) komplett ohne Notbeleuchtung; nur 2 RZ |
| EG | 31 | 185/192 | nein | Bestückt entlang Gängen; Räume abseits der Korridore unbestückt; Raumzahl durch CAD-Rauschen aufgebläht |
| 1OG | 2 | 252/254 | **ja** | Praktisch leer, 0 RZ; Prüfbericht fälschlich „ok" |
| 2OG | 2 | 254/256 | **ja** | Praktisch leer, 2 isolierte SL; Prüfbericht fälschlich „ok" |
| 3OG | 1 | 187/188 | **ja** | 1 einziges Symbol; Prüfbericht fälschlich „ok" |
| 4OG | 2 | 175/177 | **ja** | Praktisch leer, 0 RZ; Prüfbericht fälschlich „ok" |
| DG | 0 | 112/112 | **ja** | 0 Symbole **und** Grundriss nur fragmentarisch gerendert; Prüfbericht fälschlich „ok" |

## Priorisierte Fix-Liste (dedupliziert, gebäudeweit)

### P0 — Blocker

1. **[F2 · hoch] OG-/DG-Geschosse fast leer wegen fehlender Raumerkennung.** Über alle Obergeschosse und das DG (1OG, 2OG, 3OG, 4OG, DG) sowie den linken Flügel des 1KG klassifiziert die Raumerkennung praktisch nichts (typlose Räume durchgängig >98 %, DG 112/112). Ohne Raumtypen/Fluchtwege/Ausgänge hat die Platzierung keine Anker → 0–2 Symbole pro Geschoss. **Wurzelursache der Leere im gesamten Set.**
2. **[F2 · hoch] DG-Grundriss nur fragmentarisch gerendert.** Nur vereinzelte, unverbundene Wandsegmente, keine geschlossenen Räume für 112 gemeldete Räume — Geometrie-Extraktion für dieses Geschoss defekt.
3. **[F1 · hoch] Validierungs-Lücke: quasi-leere Pläne werden als „ok"/„warnung" durchgewunken.** 1OG/2OG/3OG/4OG/DG melden „ok" bei 0–2 Symbolen; 2KG/1KG „warnung" trotz fehlender RZ-Bestückung und halb-leerem Geschoss. Ein Mindest-Deckungs-Gate fehlt.

### P1 — Abnahme-relevant (jedes Geschoss)

4. **[F1 · hoch] Legende / Stückliste / Plankopf fehlen im Render** — auf **allen 8 Geschossen**. Ohne Symbol-Schlüssel + Plankopf ist kein Plan abnahmefähig (Symbolarten nicht dekodierbar).
5. **[F1 · hoch] Symbolarten visuell nicht unterscheidbar** (2KG): RZ und SL rendern als identische blaue Punkte, keine RZ-Piktogramme, keine Fluchtrichtungspfeile. Betrifft jedes bestückte Geschoss.
6. **[F2 · hoch] Fehlende RZ-Bestückung an Ausgängen/Fluchtwegen** (2KG 2 RZ, 1KG 2 RZ, OG/DG 0 RZ). Folge fehlender Ausgangs-/Zirkulationsdaten — RZ werden nicht gezielt an Türen/Ausgängen gesetzt.
7. **[F2 · mittel] Generische Flächenverteilung statt fluchtweg-/ausgangs-orientierter Platzierung** (2KG, EG): Symbole raum-für-raum bzw. nur entlang Korridoren; Nutzräume abseits der Gänge bleiben unbestückt.

### P2 — Norm-Nachweis / Qualität

8. **[F1 · mittel] Höhenkoten (h=2,40 o.ä.) fehlen an allen Symbolen** — auf allen Geschossen. EN-1838/ÖNorm-Nachweis der Montagehöhe / Erkennungsweite l=z×h nicht am Symbol dokumentiert.
9. **[F1 · mittel] Prüfbericht-Textblock nicht im Render sichtbar** (EG u.a.): Prüfstatus/Warnungen erscheinen nicht auf dem Blatt.
10. **[F2 · mittel] Raumzahl durch CAD-Rauschen aufgebläht** (EG 192 Räume): Wand-Slivers/Hatch-Fragmente treiben die Raumzahl hoch und verwässern die Typ-Deckungs-Quote.

## F1-sofort (ohne F2 umsetzbar)

Leonis kann diese drei Punkte unabhängig von der Raumerkennung angehen — sie schließen die F1-Lücken, die den kaputten Zustand aktuell verschleiern:

1. **Prüfbericht muss quasi-leere Pläne als Fehler melden — ja.** Ein Mindest-Deckungs-Gate einführen: Bei 0–2 Symbolen und >100 gemeldeten Räumen (bzw. Symboldichte pro Fläche/Raum unter Schwelle, keine RZ an vorhandenen Ausgängen) darf der Status **nicht „ok"** sein, sondern muss auf **Fehler/rot** kippen. Das betrifft sofort 5 Geschosse (1OG/2OG/3OG/4OG/DG) und macht den strukturellen F2-Defekt sichtbar statt ihn grün zu übermalen. Höchste Sofort-Priorität.
2. **Legende + Stückliste + Plankopf ins Render aufnehmen** — als feste Blattelemente, unabhängig vom Symbol-Content. Damit werden die bestückten Geschosse (2KG/EG/1KG) überhaupt erst abnahmefähig darstellbar.
3. **Symbolart-Differenzierung im Render** — RZ mit Piktogramm + Fluchtrichtungspfeil, SL als eigenes Symbol, plus Höhenkote (h=…) am Symbol. Beseitigt die „alle Punkte blau"-Undekodierbarkeit und liefert den Höhen-Nachweis, beides rein auf der Render-Seite.
