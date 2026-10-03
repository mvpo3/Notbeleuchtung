# KONFLIKTE — Widersprüche zur Mollgasse-Basis + Prüffälle + Datei-Protokoll

Stand: 2026-09-29. Regel: Widerspricht ein Projekt der Mollgasse-Basis, wird der
widersprechende Inhalt NICHT ins Regelwerk übernommen, sondern hier protokolliert.

## 1. Echte Widersprüche

### K-01 — Mollgasse-PDF S.57: Antipanik (B) ↔ (C) Textvertauschung
- **Projekt/Seite:** Mollgasse S.57 (2KG), im Seitenbild 2026-09-29 VERIFIZIERT.
- **Befund:** Die Textbeschreibungen von Antipanik (B) und (C) gehören jeweils zur
  anderen Leuchte — Bild-(B) liegt horizontal auf der gelben Diagonale
  (= C-Methode); das „vertikal ausgerichtete" Exemplar ist erst (C) auf S.59.
- **Verletzte Basis-Regel:** keine (PDF-interner Textfehler; Regelgehalt —
  Diagonale-Methode + Längsausrichtung — bleibt gültig und ist als RW-028/RW-029
  übernommen).
- **Soll:** Textblöcke B↔C tauschen. **An Owner gemeldet** (offene_fragen.md
  #27–34, seit 2026-09-20 offen).

**Sonst: 0 Widersprüche in 538 Seiten** — Projekte 2–5 bestätigen die
Mollgasse-Basis durchgängig (353 bestätigende Seiten); alles Abweichende war
Neues ohne Widerspruch (→ Ergänzungsregeln RW-101–RW-131).

## 2. Prüffälle (KEINE Regelwerk-Konflikte — visuelle Gegenprüfung nötig)

| # | Projekt | Stelle | Befund | Verdacht |
|---|---------|--------|--------|----------|
| P-01 | Baufeld E2 UG | Handle `9362D` (RIVO_ARR_down, Welt-Pfeil 90°) | bestes Personen-Delta 113°, kein Blickkeil im 4-m-Umkreis (nächster 4634 mm) | Kandidat Rotations-Abweichung ODER regelgebende Person außerhalb 12-m-Radius — Crop-Prüfung |
| P-02 | Baufeld E2 UG | Handle `822D2` (RIVO_ARR_down, Welt-Pfeil 90°) | bestes Delta 61° (Toleranz 60°), Blickkeil 430 mm vorhanden | grenzwertig — vermutlich ok (Keil bestätigt Position) |
| P-03 | Tomaschek SG | Kennungen SG-009, SG-020 | Kennung vorhanden, keine Leuchte < 2 m im Extrakt (77 Leuchten vs. 84 Kennungen) | Extraktions-/Inventar-Lücke (Alias? nested Block?) |
| P-04 | Tomaschek OG | OG-021 (PDF: down 270°) | nahe der Kennung nicht auffindbar; nur bothsided `1B618` am Knoten | Inventar-Lücke oder PDF-Kennungs-Versatz |
| P-05 | Tomaschek EG | EG-027/EG-028 (Sanitärknoten) | PDF beschreibt Paar down-270° + bothsided-180°; Inventar hat dort nur EIN RZ (`209D4`, rot 0°) | PDF↔DXF-Versionsstand |
| P-06 | Mollgasse 2KG | (N) S.94 | Text „Pfeil nach rechts", DXF `ARR-left` rot 179.84 — dargestellte Richtung (links) stimmt | Block-Familien-Benennung im Text ungenau; bestätigt Regel #8 (nie rohe rot lesen) |
| P-07 | Hausfeld UG | 37 DXF-Leuchten vs. 35 physisch lt. PDF | 2 Legendenmuster (HF-UG-RZ-001/AP-001) + 2 abgesetzte Instanzen (`60572`/`60592`, x≈70,7 m) | Legenden-/Zweitdarstellung — bei Validierung ausfiltern |

## 3. PDF-Text ↔ DXF desselben Projekts

- Nur P-05/P-06 (oben). Kein weiterer Fall in 538 Seiten.

## 4. Datei-Protokoll (Auftrag: fehlende/doppelte Dateien)

- **Alle 23 Muster-DXFs + 4 PDFs vorhanden und lesbar** (0 Lesefehler).
- Projekt 5 (Auftrags-Platzhalter „[PROJEKTNAME]"): per Beschreibung eindeutig
  als **Baufeld E2** identifiziert (`Baufeld E2 Notbeleuchtung zeichnen\
  Notbeleuchtungspläne_UG_RIVO_mit_Lehrlayern.dxf` — türkise Blickkeile
  `E2_LEHR_WEG_B_INTERPRETATION`, 118 grüne Personen, keine PDF).
- Am Rain: EG doppelt (`EG_Erklaerung` + `RIVO_Symbole`) → Erklär-Fassung genutzt;
  Sammel-DXF `…Alle_Geschosse_RIVO_Zusammenfuehrung…` bewusst ausgelassen
  (Dubletten-Gefahr). SIMA_ET-Zweitwelt ignoriert (Owner-Vorgabe).
- Mollgasse DG: `.dwg`-Zwilling + `.bak`-Dateien ignoriert, nur `.dxf` gelesen.
- Am Rain trägt TEILSTAND-Charakter: keine Lehr-Linien/Personen — Bewertung dort
  über PDF + RIVO-Symbole; unersetzte Bestands-SL (STANDARD_SL/SPOT) sind
  KEINE Konflikte, sondern dokumentierte offene Positionen (RW-123/RW-127).

## 5. Nicht zuordenbare Bilder

- Keine. Alle 538 Seiten einem Projekt/Bereich zugeordnet (Deckblätter/Register/
  Variantenkataloge als `kein_regelgehalt` protokolliert — je ANALYSE_<P>.md).
