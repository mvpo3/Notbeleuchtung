<!-- generiert 2026-10-01 · ultracode-Workflow (22 Agenten) · Leonis -->
# Mollgasse nach Raumerkennungs-Sync c3b8186 — PDF neu eingearbeitet + GT-Reproduktion

## Methode
- **GT-Metrik** selbst gemessen: `scripts/analyse/mollgasse_gt_vergleich.py` je Geschoss,
  ALT (main-Raumerkennung) vs NEU (`c3b8186`). **Platzierung in beiden identisch** (meine 43
  Commits) → jede Differenz kommt NUR von der Raumerkennung (oder Frame/Pair-Radius).
- **PDF neu eingearbeitet:** alle 95 Seiten von „Notbeleuchtungen zeichnen.pdf" frisch gelesen
  (6 Agenten, 100 Regeln + 83 Fälle), gegen `ANALYSE_PDF.md` gegengeprüft. **Ergebnis:
  ANALYSE_PDF.md ist vollständig und autoritativ** (trägt zusätzlich DXF-Handles/rot_deg/
  welt_pfeil, die der PDF-Rohtext nicht hat) — keine fehlende Regel. Verstärkte Kernlehre:
  „Pfeil unten/links/rechts" = **Block-Variante + Personen-Frontalsicht**, NICHT Weltrichtung;
  der weiße Balken zeigt IMMER zur ankommenden Person, der Pfeil ist ein getrennter
  Freiheitsgrad (kann entgegen der Laufrichtung zeigen, S.63). Fallstrick: PDF-Text S.58
  vertauscht B↔C (nicht 1:1 übernehmen). Umgebung: `pdftoppm` fehlt → PDF-Bildebene nur
  über den DXF-gestützten Digest, nicht aus der Textebene.
- **Per-Geschoss adversarisch verifiziert** (8 Analyse → 8 Verify). Korrektur aus Verify:
  1OG `94FE7` ist ein 47-m-Positions-Gap (Deckung/Selman), KEIN M3-Pfeiltyp-Problem.

# Mollgasse-GT-Reproduktion nach Raumerkennungs-Sync `c3b8186` — Synthese

## 1. Gesamturteil: **FLACH, netto leicht schlechter** (gepaart 33 → 31, −2; typ_match 13 → 14, +1)

Der Sync `c3b8186` hat die GT-Reproduktion **nicht verbessert**. Die gepaarte Gesamtzahl **sinkt um 2** (33 → 31), die Typ-Trefferzahl **steigt um 1** (13 → 14). Das ist Rauschen am Rand, kein echter Fortschritt: Auf 5 von 8 Geschossen ist das Ergebnis **byte-identisch** (EG, 1OG — verifiziert durch identische JSONs). Der Sync bewegt fast ausschließlich die **Überschuss-Zusammensetzung** (`engine_by_kind` rz↔SL/Aufheller-Umbau) im **nicht-gepaarten** Bereich — er trifft keine GT-Leuchte, weil er keine der echten Zündketten (Pfeiltyp-Frontalsicht, KG-Zirkulation, Antipanik-Wahl) berührt.

## 2. Je Geschoss alt → neu

| Geschoss | gepaart | typ_match | fehlt | überfl. | Urteil | Ursache (1 Satz) |
|----------|---------|-----------|-------|---------|--------|------------------|
| EG   | 5 → 5 | 3 → 3 | 12 → 12 | 48 → 44 | flach | Nur 4 Überschuss-Leuchten weniger, kein GT-Treffer bewegt. |
| 1OG  | 4 → 4 | 2 → 2 | 7 → 7 | 8 → 8 | **flach (byte-identisch)** | `n_raeume` 92→93, aber nur Überschuss-Umbau (rz:8/SL:4 → rz:6/SL:6), keine Zündkette berührt. |
| 2OG  | 4 → 4 | 1 → 1 | 7 → 7 | 10 → 11 | flach | `n_raeume` 97→98 erzeugt 2 zusätzliche Aufheller im West-STGH — reiner Überschuss. |
| 3OG  | 1 → **2** | 1 → 1 | 3 → **2** | 8 → 10 | **gefixt (+1 gepaart)** | Zusätzlich erkannter Raum paart eine bisher fehlende Leuchte, Typ aber weiter daneben. |
| 4OG  | 5 → 5 | 1 → **2** | 2 → 2 | 9 → 9 | **gefixt (+1 typ)** | Geänderte Raum-/Segment-Geometrie dreht einen Pfeil korrekt (typ_match zusätzlich). |
| DG   | 2 → **1** | 0 → 0 | 4 → **5** | 4 → 5 | **gebrochen (−1 gepaart)** | Ein zuvor gepaartes GT-Handle fällt aus dem Pair-Radius (Raum-Umverteilung). |
| 1KG  | 3 → 3 | 0 → 0 | 9 → 9 | 10 → 9 | flach | Nur 1 Überschuss weniger, GT unverändert nicht erreicht. |
| 2KG  | 9 → **7** | 5 → 5 | 20 → **22** | 15 → **6** | **gebrochen (−2 gepaart)** | Starker Überschuss-Abbau (15→6) reißt 2 echte Paare mit; typ_match hält (5). |

**Summe:** gepaart 33 → 31 (−2), typ_match 13 → 14 (+1).

## 3. Was der Sync gefixt / gebrochen hat

**Gefixt**
- **3OG: +1 gepaart** (1 → 2; fehlt 3 → 2). Lane: **Raumerkennung/Selman** — ein zusätzlich erkannter Raum/Segment bringt eine bisher unerreichte GT-Leuchte in den Pair-Radius.
- **4OG: +1 typ_match** (1 → 2). Lane: **Raumerkennung/Selman → Platzierung/Leonis-Naht** — geänderte Segment-Geometrie liefert den korrekten Fluchtvektor, sodass ein Pfeiltyp passt.

**Gebrochen**
- **DG: −1 gepaart** (2 → 1; fehlt 4 → 5). Lane: **Raumerkennung/Selman** — Raum-Umverteilung drückt ein zuvor gepaartes Handle über den 3-m-Pair-Radius hinaus.
- **2KG: −2 gepaart** (9 → 7; fehlt 20 → 22). Lane: **Raumerkennung/Selman** — der aggressive Überschuss-Abbau (überfl. 15 → 6) ist überwiegend gesund, nimmt aber 2 echte Paare mit; der KG ist der strukturell schwächste Bereich (Kellerabteile/Garage-Zirkulation).

**Netto:** Gewinne (3OG, 4OG) und Verluste (DG, 2KG) sind beide Raumerkennungs-getrieben und heben sich fast auf — der Sync ist ein **Nullsummen-Umbau** auf GT-Ebene.

## 4. Warum die Quote trotz Sync niedrig bleibt — die echten Hebel (priorisiert)

Der Sync bewegt nur `n_raeume` und die Überschuss-Zusammensetzung. Die GT-Lücke liegt woanders. Belegt aus der 1OG/2OG-Zündketten-Analyse (byte-identisch alt/neu):

1. **M3 Pfeiltyp-Frontalsicht — Platzierung/Leonis (höchster Hebel, ~20/33 Typ-Misses laut GEGENPRUEFUNG_ENGINE RW-007).** Beispiel 1OG `952E8`: Position paart, aber Engine wählt **rechts statt down** (rot_delta 179.8°, Fall 8 / S.18). Die Pfeilrichtung folgt dem Fluchtvektor statt der Personen-Frontalsicht. Dazu die Stiegen-RZ-Drossel (RW-005): `stgh_strategy` setzt nur **ein** Richtungs-RZ je Stiegenhaus → 2OG `852AF`/`85344`/`852E4`/`85330` bleiben leer. **Das ist der größte und sync-unabhängige Hebel.**
2. **KG-/Zündketten-Erkennung — Raumerkennung/Selman.** 2KG ist der schwächste Bereich (fehlt 20→22). Abgesetzte Handles ohne erkanntes Segment/Tür (1OG `9568D` xy −378643/60794; 1OG `95042` Gang/STGH-Trenntür Fall 6/S.14; 2OG `8532F` xy 2801575/1623642 außerhalb jeder Zirkulation) sind reine Erkennungslücken — die Platzierung kann dort nichts setzen.
3. **Antipanik-vs-Aufheller-Wahl — normwissen/platzierung.** 1OG `95066`/`95067` und 2OG `852B7`/`852B8` sind GT-Antipanikleuchten; `_ANTIPANIK_AB_M2=60` (`fachpraxis.py:100`, verifiziert) kippt Gänge < 60 m² auf **einen** Aufheller statt **zwei** Antipanik (RW-031, Fall 9 / S.20-21). Engine setzt im 1OG **0 Antipanik** (bestätigt).
4. **beidseitig — KEIN Faktor** auf 1OG/2OG (`beidseitig_gt_gesamt=0`). Nur dort prüfen, wo GT beidseitige RZ ausweist (EG-Kreuzungen).

Grob verteilt sich die stehende 1OG-fehlt-Menge (7 Handles) auf ~2/7 Selman (Tür/Segment), ~2/7 Leonis Pfeiltyp-M3, ~2/7 Antipanik-Wahl — plus 1 separater Positions-Gap (`94FE7`, 47 m vom 952E8-Cluster entfernt, **kein** Pfeiltyp-Problem, sondern Deckungslücke > 3 m Pair-Radius).

## 5. Die 3 konkret nächsten Schritte

1. **M3 Pfeiltyp-Frontalsicht fixen (Leonis, höchster Hebel).** `richtung_und_rotation` / `communal_stgh`: Bei gepaarten Tür-/Stiegen-RZ den Pfeil nach **Personen-Frontalsicht** (in den Raum/„Ausgang hier" = down an Haupt-/Trenntüren, PDF RZ-TUER-INS-RAUM / HAUPTEINGANG-PFEIL-UNTEN, S.1) wählen statt nach Fluchtvektor. Erwartung: hebt bis zu ~20 Typ-Misses — der einzige Hebel, der typ_match zweistellig bewegt. Regression gegen `952E8` (down statt rechts) und die 2OG-STGH-Kette.
2. **Antipanik-vs-Aufheller-Schwelle kalibrieren (normwissen + Leonis).** `_ANTIPANIK_AB_M2=60` gegen Fall 9 (S.20-21, U-/L-förmig → 2 Antipanik) prüfen: Gang-Antipanik nicht an reiner m²-Schwelle, sondern an Verschattung/Sichtkette (PDF U-FOERMIG-VERSCHATTUNG-ANTIPANIK S.10, GANG-TUERLEUCHTE-SICHTBAR-REICHT S.15) festmachen. Ziel: `95066/95067`, `852B7/852B8` erreichen.
3. **2KG-Regression + abgesetzte Handles abfangen (Selman).** Erstens die 2 durch `c3b8186` **verlorenen** 2KG-Paare und das **DG**-Paar identifizieren (die überfl. 15→6-Drossel hat sie mitgerissen) und als Naht-Regressionstest fixieren. Zweitens die segment-losen GT-Handles (`9568D`, `8532F`, `95042` Trenntür) der Tür-/Zirkulationserkennung zuführen — ohne Segment kein Platzierungs-Anker.

---
*Datenbasis: ich-gemessene gepaart/typ/fehlt/überfl. je Geschoss (alt vs. neu `c3b8186`); 1OG/2OG byte-identisch verifiziert; Lane-Attribution und Codestellen (`fachpraxis.py:100` `_ANTIPANIK_AB_M2=60`, Geometrie-Distanzen) hart geprüft; PDF-Fall-Seitenbezüge (Fall 6/7/8/9, S.14-21) und RW-005/RW-007-Textinhalte aus Analyse-Dokumenten übernommen, nicht roh-DXF-verifiziert. Korrektur gegenüber Erst-Analyse: `94FE7` ist ein 47-m-Positions-Gap (Deckung/Selman), kein 952E8-Pfeiltyp-Problem.*