# k-esy-at20 — Teil 4
> Quelle: k-esy-at20 (buecher) · Seiten 161-200.

Dieses Dokument ist ein Schrack/ESYLUX-Produktkatalog für Bewegungs- und Präsenzmelder. Teil 4 deckt die **KNX-Bewegungs- und Präsenzmelder** (S. 161-187) sowie die **DALI-Präsenzmelder** (S. 188-200) ab — mit vollständigen technischen Tabellen (Erfassungswinkel/-bereich, Reichweite, Spannung, Stromaufnahme, Helligkeitsbereich, Temperatur, Schutzart), Maßskizzen, Bestellnummern und UVP-Preisen (€). Kein Normtext (keine ÖVE/ÖNorm-Paragraphen), sondern Produktdaten — als Geräte-Referenz für Planung (Reichweite/Montagehöhe/Schutzart/IP) relevant.

## Inhalt

### Allgemeine Konventionen / Kürzel
- **Erfassungsbereiche** (typisch bei Decken-Präsenzmeldern, Montagehöhe ~3 m): Präsenz-/Arbeitsbereich (kleinster Ø, sitzende Tätigkeit), Frontal zum Melder (mittlerer Ø), Geh-/Querbereich (größter Ø, quer zum Melder).
- **MASTER/SLAVE**: Geräte als Master oder Slave konfigurierbar.
- **Kanäle**: "Kanäle Licht" (meist 2 bei COMPACT/ATMO, 1 bei FLAT/DALI) + "Kanäle Präsenz/HLK" (1 bei KNX, 2 bei DALI DUO/FLAT).
- **Einstellung**: KNX via ETS (Engineering-Tool-Software) + IR-Fernbedienung; DALI via IR-Fernbedienung.
- **Bus**: KNX (EIB), TP = 2-Draht-Bus.
- Wiederkehrende Zubehör-Bestellnummern: Mobil-PDi/User-Fernbedienung ESM425547 (35 €), Mobil-PDi/MDi-Service-Fernbedienung ESM425509 (35 €), Mobil-PDi/Dali ESP425899 (37 €), ESY-Pen ESP425356 (175 €), Deckeneinbauset PD-C/MD-C360 ESM425929 (10 €), Aufputzdose-C IP20 weiß ESM425370 (11 €), Aufputzdose-C IP54 weiß ESM425905 (13 €), Schutzkorb 180/90 ESM425608 (34 €), Schutzkorb 165/70 ESM425615 (32 €), Deckeneinbau-Set FLAT ESP426889 (11 €).

### KNX — Vergleich BASIC (S. 161)
- **PD 360/8 KNX BASIC** vs **RC 230 KNX** (Auszug):
  - Präsenzbereich Ø 3 m / Ø 3 m; Frontal Ø 6 m / Ø 6 m; Winkel 360° / 230°; Montagehöhe 3 m / 3 m.
  - Kanäle Licht 1 / 1; Master/Slave JA / JA; Helligkeit 5–2000 lx / 5–2000 lx.
  - Nachlaufzeit: 0, 10 s, 1–60 Min (RC 230); Spannung 29–31 V; Leistung 0,2 W; Temp 5 °C…+35 °C; IP40.
  - PD 360/8 BASIC: ESB430442 / 89,00 €. RC 230: ESM015472 / 190,00 €. Ecksockel ESM016110 / 22 €.

### KNX-Innen-Präsenzmelder Serie ATMO — PD-ATMO 360i/8 A,T (S. 162-163)
- Deckeneinbau, 360°, Reichweite bis 8 m Ø, empf. Montagehöhe 3 m.
- **ATMO T**: integrierter Akustiksensor (Wiederaktivierung der Beleuchtung per Geräusch/Zuruf innerhalb max. 8 Sek nach Ausschalten) + Erfassung Umgebungstemperatur.
- **ATMO A**: wie T, zusätzlich Erfassung relative Luftfeuchtigkeit.
- Erfassungsbereich: Quer Ø8 m, Frontal Ø6 m, Arbeitsbereich Ø4 m (Montagehöhe 3 m).
- Maßskizze: Ø108 mm / Ø60 mm, 24 mm, 38 mm.
- Technik: 360°; 29–31 V; 6 mA; Master/Slave JA; Kanäle Licht 2 / Präsenz-HLK 1; Helligkeit 5–2000 lx; Temp 5 °C…+35 °C; **IP20**; IR-Fernbedienung + ETS.
- Bestellung: PD-ATMO 360i/8 **A** KNX ESP427206 / 328,00 €; PD-ATMO 360i/8 **T** KNX ESP427213 / 284,00 €. STORE 3400.
- Zubehör: Aufputzdose-C IP20 weiß ESM425370 (11 €), Aufputzdose-C IP54 ESM425905 (13 €), Deckeneinbauset ESM425929 (10 €), Schutzkorb 180/90 ESM425608 (34 €), Schutzkorb 165/70 ESM425615 (32 €), Mobil-PDi/User ESM425547 (35 €), ESY-Pen ESP425356 (175 €).

### KNX-Innen-Präsenzmelder Serie ATMO — PD-ATMO 360i/8 O (S. 164-165)
- Design-Deckeneinbau, 360°, ca. 8 m Ø, empf. Montagehöhe 3 m (max. 5 m). Flache Optik, Design-Abdeckungen Kunststoff rund weiß, austauschbar.
- Erfassungsbereich: Quer Ø8 m, Frontal Ø6 m, Präsenzbereich Ø4 m (Montagehöhe 2,5 m).
- Maßskizze: Ø108 mm / Ø60 mm, 24 mm, 51,7 mm, 22,3 mm.
- Technik: 29–31 V (KNX), **230 V/50 Hz (VOC-Sensor)**; **10 mA**; Master/Slave JA; Licht 2 / Präsenz-HLK 1; 5–2000 lx; 360°; Temp 5 °C…+35 °C; **IP20**; IR + ETS.
- Bestellung: ESP427220 / **482,00 €**. STORE 3400.
- Zubehör: Abdeckung quadratisch weiß ESP007248 (8 €), FLAT GLASS RO WH ESP007255 (37 €), FLAT GLASS SQ WH ESP007262 (37 €), Abdeckung rund schwarz ESP428098 (9 €), rund weiß ESP428579 (9 €), Schutzkorb 165/70 ESM425615 (32 €), Deckeneinbau-Set FLAT ESP426889 (11 €), Mobil-PDi/User (35 €), ESY-Pen (175 €).

### KNX-Innen-Präsenzmelder Serie FLAT — PD-FLAT 360i/8 ROUND (S. 166-167)
- Design-Deckeneinbau, 360°, ca. 8 m Ø, Montagehöhe 3 m (max. 5 m). Flache Optik, Abdeckung rund (weiß ESP451706 / schwarz ESP451768).
- Erfassungsbereich: Quer Ø8 m, Frontal Ø6 m, Präsenzbereich Ø4 m (Montagehöhe 2,5 m).
- Maßskizze: Ø94 mm, 30 mm, Ø45 mm, 24 mm.
- Technik: 360°; 29–31 V; 6 mA; Master/Slave JA; Licht 2 / Präsenz-HLK 1; **Helligkeit 3–1000 lx**; Temp 5 °C…+35 °C; **IP20**; IR + ETS.
- Bestellung: ROUND WH ESP451706 / 126,00 €; ROUND BK ESP451768 / 126,00 €. STORE 3400.
- Zubehör wie ATMO O (Abdeckungen, Schutzkorb 165/70, Deckeneinbau-Set FLAT, Mobil-PDi/User, ESY-Pen).

### KNX-Innen-Präsenzmelder Serie FLAT — PD-FLAT 360i/8 SQUARE (S. 168-169)
- Wie ROUND, jedoch Abdeckung quadratisch (weiß ESP451713 / schwarz ESP451775).
- Erfassung: Quer Ø8 m, Frontal Ø6 m, Präsenz Ø4 m (2,5 m). Maßskizze: 77 × 77 mm, 30 mm, Ø45 mm, 24 mm.
- Technik: 360°; 29–31 V; 6 mA; Master/Slave JA; Licht 2 / HLK 1; **3–1000 lx**; 5 °C…+35 °C; IP20.
- Bestellung: SQUARE WH ESP451713 / 126,00 €; SQUARE BK ESP451775 / 126,00 €.
- Zubehör: Abdeckung rund weiß ESP007231 (8 €), FLAT GLASS RO/SQ (je 37 €), Schutzkorb 165/70 (32 €), Deckeneinbau-Set FLAT (11 €), Mobil-PDi/User (35 €), ESY-Pen (175 €).

### KNX-Innen-Präsenzmelder Serie FLAT — PD-FLAT 360i/8 LARGE (ROUND) (S. 170-171)
- Design-Deckeneinbau, 360°, ca. 8 m Ø, Montagehöhe 3 m (max. 5 m). Abdeckung Kunststoff Ø104 mm rund weiß.
- Erfassung: Quer Ø8 m, Frontal Ø6 m, Präsenz Ø4 m (2,5 m). Maßskizze: Ø104 mm, 30 mm, Ø60 mm, 24 mm.
- Technik: 360°; 29–31 V; 6 mA; Master/Slave JA; Licht 2 / HLK 1; **3–1000 lx**; 5 °C…+35 °C; IP20.
- Bestellung: PD-FLAT 360i/8 L ROUND WH KNX ESP428685 / 131,00 €.
- Zubehör: Abdeckung rund schwarz ESP428098 (9 €), Aufputzdose-C IP20 weiß ESM425370 (11 €), Deckeneinbau-Set FLAT ESP426889 (11 €), Schutzkorb 165/70 (32 €), Schutzkorb 180/90 (34 €), Mobil-PDi/MDi Service ESM425509 (35 €).

### KNX-Innen-Präsenzmelder Serie COMPACT MINI — PD-C 360i/8 mini (S. 172-173)
- Mini-Deckeneinbau, 360°, bis 8 m Ø, Montagehöhe 3 m.
- Erfassung: Geh-/Quer Ø8 m, Frontal Ø5 m, Arbeitsbereich Ø3 m (Montagehöhe 3 m). Maßskizze: 25 mm, 45 mm, 15 mm, 33 mm.
- Technik: 360°; 29–31 V; 6 mA; Master/Slave JA; Licht 2 / HLK 1; 5–2000 lx; **Temp 5 °C…+50 °C**; **IP55**; IR + ETS.
- Bestellung: PD-C360i/8 mini KNX ws ESP426155 / 146,00 €.
- Zubehör: Spot-Adapter 51/25 ESP426391 (15 €), Mobil-PDi/User (35 €), Mobil-PDi/MDi (35 €), ESY-Pen (175 €).

### KNX-Innen-Präsenzmelder Serie COMPACT MINI — PD-C 360i/12 mini (S. 174-175)
- Mini-Deckeneinbau, 360°, **bis 12 m Ø**, Montagehöhe 3 m.
- Erfassung: Geh-/Quer Ø12 m, Frontal Ø6 m, Arbeitsbereich Ø4 m. Maßskizze: 25 mm, 45 mm, 25 mm, 58 mm.
- Technik: 360°; 29–31 V; 6 mA; Master/Slave JA; Licht 2 / HLK 1; 5–2000 lx; **5 °C…+50 °C**; **IP55**.
- Bestellung: PD-C360i/12 mini KNX ws ESP426162 / 155,00 €.
- Zubehör: Spot-Adapter 51/25 ESP426391 (15 €), Mobil-PDi/User (35 €), Mobil-PDi/MDi (35 €), ESY-Pen (175 €).

### KNX-Innen-Präsenzmelder Serie COMPACT — PD-C 360i/8 UP (S. 176-177)
- Deckeneinbau (UP = Unterputz), 360°, bis 8 m Ø, Montagehöhe 3 m (max. 5 m).
- Erfassung: Geh-/Quer Ø8 m, Frontal Ø6 m, Arbeitsbereich Ø4 m. Maßskizze: Ø108 mm / Ø60 mm, 24 mm, 38 mm.
- Technik: 360°; 29–31 V; 6 mA; Master/Slave JA; Licht 2 / HLK 1; 5–2000 lx; **5 °C…+50 °C**; **IP20**. Legende A = Standardbetrieb.
- Bestellung: PD-C360i/8 KNX weiß UP Ø8m ESP427404 / 145,00 €.
- Zubehör: Aufputzdose-C IP20 weiß ESM425370 (11 €) / silber ESP425387 (20 €), Aufputzdose-C IP54 weiß ESM425905 (13 €) / silber ESP425912 (20 €), Abdeck-Set C360/8 silber ESP425936 (18 €), Deckeneinbauset ESM425929 (10 €), Schutzkorb 180/90 (34 €), 165/70 (32 €), Mobil-PDi/MDi (35 €), ESY-Pen (175 €).

### KNX-Innen-Präsenzmelder Serie COMPACT — PD-C 360i/24 UP / ECO (S. 178-179)
- Deckeneinbau, 360°, **bis 24 m Ø**, Montagehöhe 3 m (Komfort). ECO-Variante + Standard-Variante mit HLK-Kanal. Optimal mit Funktion "Schalten" für Installation in großen Höhen bis 10 m (z. B. Sport-/Lagerhallen).
- Erfassung: Geh-/Quer Ø24 m, Frontal Ø11 m, Präsenzbereich Ø8 m. Maßskizze: Ø108 mm / Ø60 mm, 24 mm, 46 mm.
- Technik: 360°; 29–31 V; 6 mA; Master/Slave JA; Licht 2 / HLK 1; 5–2000 lx; 5 °C…+50 °C; IP20.
- Bestellung: PD-C360i/24 KNX **ECO** ESP427435 / 153,00 €; PD-C360i/24 KNX weiß UP ESP427428 / 170,00 €.
- Zubehör: Aufputzdosen (IP20 weiß 11 €, IP20 silber 20 €, IP54 weiß 13 €, IP54 silber 20 €), Abdeck-Set C360/24 silber ESP425431 (18 €), Deckeneinbauset (10 €), Schutzkorb 165/70 (32 €), Mobil-PDi/MDi (35 €), Mobil-PDi/User (35 €), ESY-Pen (175 €).

### KNX-Innen-Präsenzmelder Serie COMPACT — PD-C 360i/32 UP (S. 180-181)
- Deckeneinbau, 360°, **bis 32 m Ø**, Montagehöhe 3 m (Komfort). Optimal mit "Schalten" für große Höhen bis 10 m (Sport-/Lagerhallen).
- Erfassung: Geh-/Quer Ø32 m, Frontal Ø11 m, Arbeitsbereich Ø8 m. Maßskizze: Ø108 mm / Ø60 mm, 24 mm, 46 mm.
- Technik: 360°; 29–31 V; 6 mA; Master/Slave JA; Licht 2 / HLK 1; 5–2000 lx; 5 °C…+50 °C; IP20.
- Bestellung: PD-C360i/32 KNX UP weiß Ø32m ESP427794 / 190,00 €.
- Zubehör: Aufputzdosen (IP20 weiß/silber, IP54 weiß/silber), Abdeck-Set C360/24 silber ESP425431 (18 €), Deckeneinbauset (10 €), Schutzkorb 180/90 (34 €), 165/70 (32 €), Mobil-PDi/MDi (35 €), Mobil-PDi/User (35 €), ESY-Pen (175 €).

### KNX-Innen-Präsenzmelder Serie COMPACT — PD-C 180i ECO (Wandmontage) (S. 182-183)
- 180°-Präsenzmelder für **Wandmontage**, bis 16 m Ø, empf. Montagehöhe 1,1–2,2 m.
- Varianten: **PD-C 180i/16 Touch** (Touch-Bedienung am Melder), **PD-C 180i KNX** (mit Akustiksensor), **PD-C180i KNX ECO** (ohne Akustiksensor).
- Erfassung: Geh-/Quer Ø16 m, Frontal Ø12 m, Arbeitsbereich Ø8 m. Maßskizze: 70 mm, 63 mm, 34 mm, 61 mm, 70 mm.
- Technik: 180°; 29–31 V; 6 mA; Master/Slave JA; Licht 2 / HLK 1; 5–2000 lx; 5 °C…+50 °C; **IP20, IP44 je nach Abdeckung (optional)**.
- Bestellung: PD-C180i KNX ECO (1 Kanal, ohne Akustiksensor) ESP426452 / 132,00 €; PD-C180i KNX (2 Kanal, mit Akustiksensor) ESP426445 / 149,00 €; PD-C 180i/16 Touch KNX (180°, Ø16m, IP40, weiß) ESP460104 / 163,00 €.
- Zubehör: VISIO 50 Bewegungsmelder-Abdeckung für MD180 mit Sonderrahmen 55×55 mm ESM055270 (15,20 €), Sonder-Rahmen 1-fach 55×55 mm EV105021 (2,49 €, STORE 3100), Abdeckungen IP20 MD180i/R,MD180i/T,MD/PD180: weiß ESM055102 (13 €), signalweiß ESM055119 (13 €), cremeweiß ESM055126 (13 €), Edelstahloptik ESM055140 (16 €), Mobil-PDi/User (35 €), ESY-Pen (175 €).

### KNX-Innen-Präsenzmelder Serie BASIC — PD 360/8 (S. 184-185)
- Decken-Präsenzmelder, 360°, bis 8 m Ø, Montagehöhe 3 m (Komfort).
- Erfassung: Geh-/Quer Ø8 m, Frontal Ø6 m, Präsenzbereich Ø4 m (Montagehöhe 2,5 m). Maßskizze: Ø101 mm, 33 mm.
- Technik: 360°; 29–31 V; 6 mA; Master/Slave JA; Licht 2 / HLK 1; 5–2000 lx; 5 °C…+50 °C; **IP40**; nur ETS (keine IR-Fernbedienung gelistet).
- Bestellung: PD 360/8 KNX Basic (360°, Ø8m, IP40, weiß) ESB430442 / 89,00 €.
- Zubehör: Schutzkorb 180/90 (34 €), 165/70 (32 €), Deckeneinbauset ESM425929 (10 €).

### KNX-Außen-Präsenzmelder Serie RC 230 (S. 186-187)
- Außen-Bewegungsmelder, **230°** Erfassung, große Reichweite, **360° Unterkriechschutz** (lückenlose Erfassung).
- Erfassung: 360°-Unterkriechschutz Ø40 m, Frontal Ø16 m, Geh-/Quer Ø6 m; Montagehöhe 2,5 m. Maßskizze: 135 mm, 105 mm, 78 mm.
- Technik: 230°; 29–31 V; 6 mA; Master/Slave JA; Licht 2 / HLK 1; **Helligkeit 2–1000 lx**; **Temp -25 °C…+55 °C**; **IP54**; nur ETS.
- Bestellung: RC 230i KNX Aufputz IP54 weiß ESM015472 / 190,00 €.
- Zubehör: RC Ecksockel weiß (RCI-Serie) ESM016110 / 22,00 €.

### DALI-Präsenzmelder — Auswahlhilfe (S. 188-189)
Übersicht nach Katalogseite:
| Typ | Montage | Winkel | Ø | Fläche | Kanal L/HLK | IP | Seite |
|-----|---------|--------|----|--------|------|----|----|
| PD-FLAT 360i/8 ROUND DALI | Deckeneinbau | 360° | Ø8 m | bis 50 m² | 1/2 | IP20 | 196 |
| PD-FLAT 360i/8 SQUARE DALI | Deckeneinbau | 360° | Ø8 m | bis 50 m² | 1/2 | IP20 | 198 |
| PD-FLAT 360i/6 mini DALI | Deckeneinbau | 360° | Ø6 m | bis 28 m² | 1/2 | IP55 | 200 |
| PD-C 360i/8 mini DALI | Deckeneinbau | 360° | Ø8 m | bis 50 m² | 1/2 | IP55 | 202 |
| PD-C 360i/8 DUO DALI | Decke | 360° | Ø8 m | bis 50 m² | 2/2 | IP20/IP54 | 204 |
| PD-C 360i/24 DUO DALI | Decke | 360° | Ø24 m | bis 453 m² | 2/2 | IP20/IP54 | 206 |
| PD-C 360i/32 DUO DALI | Decke | 360° | Ø32 m | bis 805 m² | 2/2 | IP20/IP54 | 208 |
(Alle fernbedienbar.)

### DALI Vergleichstabelle Serie COMPACT — PD-C 360i/8 DUO DALI (S. 190)
- Präsenzbereich Ø4 m; Frontal Ø6 m; 360°; Montagehöhe 3 m; Licht 2 / Präsenz-HLK 2; 5–2000 lx; Nachlaufzeit Präsenz ca. 1–15 Min; fernbedienbar JA; **230 V/50 Hz**; Master/Slave JA; parallel schaltbare Melder 0; **Leistung 0,6 W**; **Temp -25 °C…+50 °C**; Schutzart IP20 (Unterputz), IP20/IP54 (Aufputzdose), IP20 (Deckeneinbau).
- Artikel: ESP427442 / 147,00 €.
- Zubehör: Aufputzdose-C IP20 weiß ESM425370 (11 €), IP54 weiß ESM425905 (13 €), IP20 silber ESP425387 (20 €), IP54 silber ESM425905 (13 €), Abdeck-Set C360/8 ESP425936 (18 €), Deckeneinbau-Set-C ESM425929 (10 €), Mobil-PDi/User (35 €), Mobil-PDi/Dali ESP425899 (37 €), ESY-Pen (175 €).

### DALI Vergleichstabelle COMPACT — PD-C 360i/24 DUO vs /32 DUO (S. 191 + S. 194)
- **PD-C 360i/24 DUO DALI**: Präsenz Ø8 m; Frontal Ø11 m; 360°; Montagehöhe 3 m; Licht 2 / HLK 2; 5–2000 lx; Nachlauf 1–15 Min; fernbedienbar JA; 230 V/50 Hz; Master/Slave JA; parallel 0; 0,6 W; -25 °C…+50 °C; IP20 / IP20-IP54 / IP20. Artikel **ESP427459 / 172,00 €**.
- **PD-C 360i/32 DUO DALI**: Präsenz Ø8 m; Frontal Ø11 m; 360°; 3 m; Licht 2 / HLK 2; 5–2000 lx; 1–15 Min; 230 V/50 Hz; 0,6 W; -25 °C…+50 °C; gleiche IP-Angaben. Artikel **ESP427787 / 192,00 €**.
- Zubehör für /24 + /32 identisch zu /8 DUO (Aufputzdosen, Abdeck-Set, Deckeneinbau-Set-C, Mobil-PDi/User 35 €, Mobil-PDi/Dali 37 €, ESY-Pen 175 €).

### DALI Vergleichstabelle Serie FLAT — ROUND vs SQUARE (S. 192)
- **PD-FLAT 360i/8 ROUND DALI** und **SQUARE DALI** (identische Werte):
  - Präsenz Ø4 m; Frontal Ø6 m; 360°; **Montagehöhe 2,5 m**; **Licht 1 / Präsenz-HLK 2**; **Helligkeit 3–1000 lx**; **Nachlaufzeit deaktiviert / ca. 1–240 Min**; Kontaktart Bus-System; Master/Slave JA; parallel 0; fernbedienbar JA; **Betriebsspannung 9,5–22,5 V**; **Leistung 0,3 W**; **Temp 0 °C…+50 °C**; **IP20**.
  - ROUND: ESP427541 / 108,00 €; SQUARE: ESP427558 / 108,00 €.
  - Zubehör: Deckeneinbau-Set FLAT ESP426889 (11 €, nur ROUND gelistet), Mobil-PDi/User (35 €), Mobil-PDi/Dali (37 €), ESY-Pen (175 €).

### DALI Vergleichstabelle FLAT mini + COMPACT mini (S. 193 + S. 195)
- **PD-FLAT 360i/6 mini DALI**: Präsenz Ø2,5 m; Frontal Ø6 m; 360°; 3 m; Licht 1 / HLK 2; **10–2000 lx**; Nachlauf deaktiviert / 1–240 Min; Bus-System; Master/Slave JA; parallel 0; fernbedienbar JA; **9,5–22,5 V**; **0,3 W**; **0 °C…+50 °C**; **IP55**. Artikel ESP427503 / 119,00 €.
- **PD-FLAT 360i/8 mini DALI**: Präsenz Ø3 m; Frontal Ø5 m; 360°; 3 m; Licht 1 / HLK 2; 10–2000 lx; deaktiviert / 1–240 Min; Bus-System; Master/Slave JA; parallel 0; 9,5–22,5 V; 0,3 W; **-25 °C…+50 °C**; IP55. Artikel ESP427510 / 123,00 €.
- **PD-C 360i/8 mini DALI** (S. 195): Präsenz Ø3 m; Frontal Ø5 m; 360°; 3 m; Licht 1 / HLK 2; 10–2000 lx; **Nachlauf ca. 1–15 Min**; fernbedienbar JA (über DALI); 9,5–22,5 V; 0,3 W; **-25 °C…+50 °C**; **IP55**. Artikel ESP427510 (im FLAT-mini-Block; vgl. ESP427503 für /6 mini) — Mobil-PDi/User (35 €), Mobil-PDi/Dali (37 €), ESY-Pen (175 €).

### DALI-Innen-Präsenzmelder Serie FLAT — PD-FLAT 360i/8 ROUND DALI (S. 196-197)
- Design-Präsenzmelder, ausgezeichnete Erfassung mind. 8 m Ø, flache Optik, austauschbare Abdeckungen (rund/quadratisch, Glas, weiß/schwarz).
- Erfassung: Quer Ø8 m, Frontal Ø6 m, Präsenzbereich Ø4 m (Montagehöhe 2,5 m). Maßskizze: Ø94 mm, 30 mm, Ø60 mm, 24 mm.
- Technik: 360°; **9,5–22,5 V**; **0,3 W**; Master/Slave JA (über DALI); **Licht 1 / Präsenz-HLK 2**; 3–1000 lx; **Nachlaufzeit Licht ca. 1–15 Min**; **-25 °C…+50 °C**; IP20; IR-Fernbedienung.
- Schaltpläne: A = Standardbetrieb, B = Master/Slave-Modus. Beteiligt: DALI Power Supply **CU PS DALI EC10430008**, DALI EVG, Klemmen DA+/DA-/L/N, Taster S1/S2.
- Bestellung: ROUND WH ESP427541 / 108,00 €; ROUND BK ESP427916 / 108,00 €.
- Zubehör: Abdeckung quadratisch weiß ESP007248 (8 €), FLAT GLASS RO WH ESP007255 (37 €), FLAT GLASS SQ WH ESP007262 (37 €), Abdeckung rund schwarz ESP428098 (9 €), rund weiß ESP428579 (9 €), **SW DALI Full Automation** (DALI-Schaltmodul UP, IP20) ESP427473 (43 €), **SW DALI Semi Automation** ESP427480 (43 €), Deckeneinbau-Set FLAT (11 €), Schutzkorb 165/70 (32 €), 180/90 (34 €), Mobil-PDi/Dali (37 €), **CU PS DALI** (48×45×25 mm L×B×T, Ø68 mm) ESC430008 (55 €), ESY-Pen (175 €).

### DALI-Innen-Präsenzmelder Serie FLAT — PD-FLAT 360i/8 SQUARE DALI (S. 198-199)
- Wie ROUND, Abdeckung quadratisch austauschbar (alternativ rund/Glas/weiß/schwarz).
- Erfassung: Quer Ø8 m, Frontal Ø6 m, Präsenz Ø4 m (2,5 m). Maßskizze: 77 × 77 mm, 30 mm, Ø60 mm, 24 mm.
- Technik: 360°; 9,5–22,5 V; 0,3 W; Master/Slave JA (über DALI); Licht 1 / HLK 2; 3–1000 lx; Nachlauf Licht ca. 1–15 Min; -25 °C…+50 °C; IP20; IR.
- Schaltpläne A/B wie ROUND (CU PS DALI, DALI EVG, S1/S2).
- Bestellung: SQUARE WH ESP427558 / 108,00 €; SQUARE BK ESP427909 / 108,00 €.
- Zubehör: Abdeckung rund weiß ESP007231 (8 €), FLAT GLASS RO/SQ (je 37 €), SW DALI Full ESP427473 (43 €), SW DALI Semi ESP427480 (43 €), Schutzkorb 165/70 (32 €), 180/90 (34 €), Mobil-PDi/Dali (37 €), ESY-Pen (175 €).

### DALI-Innen-Präsenzmelder Serie FLAT MINI — PD-FLAT 360i/6 (S. 200)
- 360° Deckenmontage, bis 6 m Ø, Montagehöhe 3 m. Flache Linse **nur 3 mm Aufbauhöhe**.
- Automatische Lichtsteuerung von DALI-EVGs auf konstantes Helligkeitsniveau (Anwesenheit + Tageslicht, mit DALI-Ausgang); kombinierbar mit DALI-Tastern; HLK + potentialfreier Kontakt möglich i.V.m. DALI Switch von ESYLUX.
- Erfassung: Geh-/Quer Ø6 m, Arbeitsbereich Ø2,5 m (Montagehöhe 3 m). Maßskizze: 20 mm, 36 mm, **3 mm**, 25 mm.
- (Bestellnr. PD-FLAT 360i/6 mini DALI ESP427503 / 119,00 € — vgl. Vergleichstabelle S. 193/195.)
