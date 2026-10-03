# REVIEW — Mollgasse-Erklärung vs. Engine (Entscheidungsgrundlage)

Stand 2026-09-30. Quellen: alle Dateien in `_Analyse/` (95 Seiten Bild für Bild
im Detail-Zweitpass, 283 Regel-Aussagen mit Warum, 8 DXF-Analysen mit
Handle-Vollerfassung, echter Engine-Lauf je Geschoss).

## 1. Kurzfazit (10 Sätze)

1. Die Engine kennt die Mollgasse-Regeln fast vollständig: **19 von 35
   Basis-Regeln deckungsgleich (54 %), 6 abweichend, 10 fehlend** — und keine
   einzige Engine-Regel widerspricht dem PDF hart.
2. Die LEUCHTEN-Reproduktion ist trotzdem schwach: **33/97 Referenzleuchten
   gepaart (34 %), nur 13 davon mit richtiger Typ-Familie (13 %)** — die Lücke
   liegt nicht im Regelwissen, sondern in drei konkreten Mechanismen.
3. Mechanismus 1 — **Positions-Konvention** (RW-005/RW-001): der Owner
   platziert im 800–1122-mm-Band vor Stiegenkanten bzw. 735–930 mm raumseitig
   der Tür; die Engine platziert an Graph-Ankern/Wandachsen → systematische
   1–2-m-Distanzen bei sonst richtigen Leuchten.
4. Mechanismus 2 — **Typ-Wahl** (RW-007): die Engine quantisiert den
   Fluchtvektor, der Owner wählt nach Frontalsicht der ankommenden Person;
   das kostet 20 von 33 Paaren den Typ-Match.
5. Mechanismus 3 — **Erkennungs-Nähte**: Kellerabteil-/Garage-Zirkulation
   fehlt (Selman S-KG) → beidseitig 0/8, 2KG/1KG dünn; das ist kein
   Platzierungs-Defekt.
6. Der **Aufheller-Überschuss** (115 überflüssige Symbole, EG allein 48) kommt
   aus der B1-500mm-Regel (Owner-Ansage 09/2026), die im Mollgasse-PDF KEINEN
   Beleg hat — das PDF kennt Zusatzleuchten nur lichtberechnungs-getrieben.
7. Der Detail-Pass hat zwei EXAKTE, bisher unbekannte Owner-Rezepte bewiesen:
   Antipanik sitzt auf der MITTE der Bereichs-Diagonale (Δ23–33 mm) bzw. in
   ACHS-FLUCHTUNG mit der nächsten Notleuchte (Δ24 mm) — beides direkt
   algorithmisierbar.
8. PDF und DXF widersprechen sich nur in Textfehlern (S.57 B↔C verifiziert,
   S.35/36-Duplikat, S.19-Linien) — die Zeichnungen selbst sind regelkonform.
9. Mit den 6 Änderungen aus §3 (Positions-Band, Frontalsicht-Typ,
   Diagonale-Rezept, B1-Drossel, beidseitig-GT-Konvention, OG-Ausnahme) ist
   auf den erkannten Bereichen eine Paar-Quote von grob 70–80 % realistisch;
   die restliche Lücke bis 95 % hängt an Selman (S-KG, Zirkulations-Pfade).
10. Empfehlung: Einbau in 4 Phasen (unten), jede gegen den vorhandenen
    GT-Harness gemessen — kein Big-Bang, Freezes werden je Phase bewusst
    nachgezogen.

## 2. Regel-Tabelle (Klasse · Priorität · Aufwand)

| RW | Thema | Klasse | Prio | Aufwand |
|---|---|---|---|---|
| RW-001 | Tür-RZ-Versatz raumseitig | AB | **hoch** (jede Tür-Leuchte) | klein (Konstante+Owner-Klärung) |
| RW-005 | 800–1122 mm vor Stiegenkante | AB | **hoch** | mittel |
| RW-007 | Typ nach Frontalsicht | AB | **hoch** (jede Richtungs-Leuchte) | mittel–groß |
| RW-016 | beidseitig (Render 1 Block vs. GT 2 Blöcke; feuert nicht) | AB | **hoch** | klein (Konvention) + Selman (Pfade) |
| RW-029 | AP auf Diagonalen-Mitte | AB | **hoch** (jede AP) | klein–mittel (Rezept liegt vor) |
| RW-031 | Geräte-Wahl je Geschoss | AB | mittel | klein |
| RW-028 | AP-Längsachse drehen | F | mittel | klein |
| RW-033 | OG-Ausnahme I-Gang | F | mittel (Überschuss) | klein–mittel |
| RW-011 | Hindernis-Versatz (Kuppel) | F | niedrig (Input fehlt) | groß |
| RW-015 | Kabeltrasse 450 mm | F | mittel | blockiert (Input) |
| RW-017 | Garage durchquerbar | F | mittel | blockiert (Selman) |
| RW-021 | SV ≠ E-Verteiler-Wand | F | niedrig | mittel |
| RW-035 | Stiegenpfeil-Farbe | F | niedrig | Selman |
| RW-002–004, 006, 008–010, 012–014, 018–020, 022–027, 030, 032, 034 | — | **DG** | — | — |
| Überschuss: B1-Aufheller-500mm | — | **ÜS** | **hoch** (115 Symbole) | klein (Gate/Drossel) |
| Überschuss: Fluchtweg-SL-Reihen | — | ÜS | mittel | mittel (S4-Kalibrierung) |

## 3. Die 10 wichtigsten Änderungen (mit Messpunkt)

| # | Änderung | Zielmodul/Funktion | Regel | Erfolgs-Messpunkt (DXF-Beleg) |
|---|---|---|---|---|
| 1 | B1-Aufheller drosseln: nur nach gescheitertem Lux-Gate statt 1:1 je RZ | `fachpraxis.py` (aufheller-Zweig) | ÜS/RW-030 | EG-Überschuss 48 → <10 (vergleich.json EG) |
| 2 | Stiegen-RZ ins 800–1122-mm-Band vor Antritts-/Austrittskante | `stgh_strategy.plan_stiegenhaus_rz` | RW-005 | 1OG (B) 94FE8, 2OG (B) 85330: Distanz <500 mm |
| 3 | Typ-Wahl nach Frontalsicht der Ankunftsrichtung (Erstleuchte ≤45° zur Normalen) | `bausteine.richtung_und_rotation` + Aufruf-Sites | RW-007 | 4OG-Kette (A) 413A0/(B) 41593: Typ-Match; Typ-Quote 13/33 → >25/33 |
| 4 | AP-Position = Mitte der Bereichs-Diagonale (Mauerkante→Gangecke) | `fachpraxis`/`flaechen_strategy` (neue Konstruktions-Helper) | RW-029 | 2KG (B) 1C707/(C) 1C706: <300 mm statt dm-Abweichung |
| 5 | AP-Achs-Fluchtung mit nächster Fluchtweg-Leuchte + Längsachsen-Rotation | dito + `rotation_deg` für AP | RW-029/028 | 2KG (K) 1C7FB: Achse Δ<100 mm, Rotation vertikal |
| 6 | beidseitig als ZWEI gespiegelte Einzel-Blöcke rendern (GT-Konvention) ODER Vergleich beidseitig-tolerant | `dxf_renderer`/`inserter` bzw. gt_vergleich | RW-016 | 2KG-Gruppen (D) 1C885+1C886, (K) 1C936+1C937 |
| 7 | OG-Ausnahme: 1 STGH + I-Gang → Zusatz-Richtungs-RZ unterdrücken | `sichtkette`/`platzierer` | RW-033 | 1OG/2OG Überschuss 8–10 → ≤3 |
| 8 | Tür-RZ-Versatz: Owner-Klärung 0 mm (Ansage 18.09.) vs. 735–930 mm (PDF-Vermessung), dann Konstante | `bausteine.RZ_INS_RAUM_MM` | RW-001 | EG (D) 20240: Distanz <300 mm |
| 9 | Geräte-Wahl-Vorrang Geschoss (UG→AP, EG–OG→Aufheller) vor Flächen-Heuristik | `fachpraxis._ANTIPANIK_AB_M2`-Zweig | RW-031 | 1KG/2KG AP-Typen = GT-Typen |
| 10 | Kopier-Rest-Filter im GT-Vergleich (2137C-Klasse) + Extraktor-Lücken (Leerzeichen-Kennungen, rote/blaue Marker) | `gt_vergleich`/`extract_erklaerung` | Werkzeug | EG gt_n 17→16 sauber; 1KG-Kennungen D/E gematcht |

## 4. Unklarheiten & Widersprüche → Fragen an dich

1. **Tür-RZ-Versatz:** Deine Ansage 18.09. „Wandlinie, kein Sollwert" vs.
   PDF-Vermessung 735–930 mm raumseitig — was gilt für den Einbau? (#8 oben)
2. **B1-Aufheller-500mm:** Owner-Ansage 09/2026 vs. Mollgasse-PDF (Zusatzlicht
   nur per Lichtberechnung). Drosseln auf Lux-Gate-only? (#1 oben — größter
   einzelner Hebel gegen die 115 Überschüsse)
3. **S.57/58 B↔C-Textfehler** (verifiziert) — PDF korrigieren?
4. **S.35/36:** Falsch-Leuchte trägt im DXF Kennung (D) statt (B), S.36-Text
   ist Duplikat — Korrektur?
5. **S.1 vs. S.6:** „Haupteingangstür" für zwei verschiedene Westtüren
   (20286 vs. 20240) — Benennung klären.
6. **Unerklärte DXF-Leuchten** (8532F 2OG; 78DFD-Szene 3OG; 206DB/206D6
   DG-West; (D) 1BFC3 1KG): bewusst ausgelassen oder PDF-Erweiterung?
7. **beidseitig-Konvention:** GT zeichnet 2 gespiegelte Blöcke, Engine rendert
   1 bothsided-Block — welches Ziel-Format für Produktionspläne?
8. **FREIHEIT/KEINE-FREIHEIT** (S.77) — Bedeutung weiter offen (seit 09/18).

## 5. Einbau-Plan in Phasen (je Phase: Messlauf `mollgasse_gt_vergleich.py`)

| Phase | Inhalt | Abhängigkeit | Validierungskriterium (8 Geschosse) |
|---|---|---|---|
| **M1** | #1 B1-Drossel + #10 Werkzeug-Fixes | keine | Überschuss 115 → <40; gepaart stabil ≥33/97 |
| **M2** | #2 Stiegen-Band + #8 Tür-Versatz (nach Owner-Antwort) + #4/#5 AP-Rezepte | Frage 1/2 | gepaart ≥55/97; Median-Distanz <600 mm |
| **M3** | #3 Frontalsicht-Typ + #7 OG-Ausnahme + #6 beidseitig-Konvention | M2 | Typ-Match ≥70 % der Paare; beidseitig ≥4/8 |
| **M4** | Selman-Pakete S-KG (Kellerabteile/Garage/Zirkulation) + GT-Re-Run | Selman | gepaart ≥80/97 (≈83 %); Rest-Analyse für 95 % |

Freezes (`tests/naht/test_mollgasse_gt.py`, Goldens) werden je Phase EINMAL
bewusst nachgezogen — mit deinem GO pro Phase.

## 6. Risiken (wo falscher Einbau bestehende Ergebnisse verschlechtert)

1. **B1-Drossel (#1)** senkt auch Fischamend-/Wohnbau-Symbolzahlen — dort sind
   v2/v3-Stückzahlen von dir abgenommen; Bänder brechen KONTROLLIERT (Re-Render
   + neue Abnahme nötig).
2. **Frontalsicht-Typ (#3)** kippt Rotations-Golden `platzierung_4og.json` und
   alle Pfeil-Bänder; die 4OG-Lehrbeispiele (S.31–36 inkl. dokumentierter
   Falsch-Varianten) sind dafür die Test-Basis — ohne sie droht genau der
   „Seitenansicht"-Fehler, den das PDF als falsch zeigt.
3. **Stiegen-Band (#2)** verschiebt STGH-RZ in ALLEN Projekten (din-Referenz
   R8, Hausfeld-Knick-Fälle) — Hausfeld 2DG ist heute 3/3, darf nicht kippen →
   Hausfeld-Validierung in jede Phase aufnehmen.
4. **OG-Ausnahme (#7)** darf nur bei WIRKLICH eindeutigen I-Gängen feuern —
   falsch generalisiert löscht sie Pflicht-RZ (EN-1838-Hard-Stop-Risiko); Guard:
   nur wenn Sichtkette OHNE das RZ geschlossen bleibt.
5. **beidseitig als 2 Blöcke (#6)** ändert Legende/Stückliste (Zählweise!) —
   Render- und Zähl-Logik müssen synchron umgestellt werden.
6. **AP-Diagonale (#4/5)** ohne Raum-Polygon-Qualität (Zacken-Räume,
   Mollgasse-Fragmente) kann Außen-Positionen erzeugen — Guard: Punkt-in-Raum
   -Prüfung + Fallback auf heutiges Zentrum.
