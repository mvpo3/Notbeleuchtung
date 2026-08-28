# k-esy-at20 — Teil 3
> Quelle: k-esy-at20 (buecher) · Seiten 121-160.

Dieser Teil ist ein Produktkatalog von Schrack/ESYLUX und behandelt **Innen-Präsenzmelder** (PIR, Decken- und Wandmontage) sowie ab S.154 **KNX-Bewegungs- und Präsenzmelder**. Pro Gerät gibt es Schrack-Info (Funktionsbeschreibung), Erfassungsbereich, Maßskizze, technische Tabelle und Bestellnummern (BEST. NR. / UVP). Relevanz für ElektroPlaner: Symbol-Auswahl, Erfassungsreichweite zur Raumabdeckung, Montagehöhe, Schaltlast (LED/Glüh/Leuchtstoff), Schutzart-Eignung, Master/Slave-Verschaltung.

## Inhalt

### Allgemeine Konventionen (gelten für fast alle PIR-Geräte)
- Erfassungswinkel Decke: **360°**; Wandgeräte: **180°** bzw. KNX-Wand **230°**.
- Betriebsspannung/Frequenz Standard: **230 V / 50 Hz** (KNX-Busgeräte: **29–31 V**, ATMO-O als Ausnahme 230 V).
- Einstellbereich Helligkeit (Dämmerung): **5–2000 lx** (FLAT-KNX: **3–1000 lx**).
- LED-Tauglichkeit: meist über **Wolfram-Vorlaufkontakt**; bei FLAT/BASIC über **Nulldurchgangsschaltung**.
- Standard-Schaltlast Lichtkanal (außer Mini /6): **Glüh/Halogen cos φ 1 = 2300 W / 10 A**; **Fluoreszenz/Kompakt/Leuchtstoff cos φ 0,5 = 1150 VA / 5 A**.
- Relais meist **16 A Hochleistungsrelais (Wolfram-Vorlaufkontakt)**; BASIC-Serie **10 A**.
- Einstellung über **Einstellregler/Potentiometer** und/oder **IR-Fernbedienung**.
- Master/Slave-Logik (Schaltplan-Typen wiederkehrend):
  - **A** = Standardbetrieb.
  - **B** = Standardbetrieb mit zusätzlicher Ansteuerung durch Schließtaster (manuelles Ein/Aus per Taster).
  - **C/D** = Master-Slave-Schaltung: Master schaltet Verbraucher nach Parametern; Slaves dienen nur der Präsenzerfassung und geben Bewegungs-Impuls an Master. Bzw. RC-Filter-Hinweis bei Induktivitäten (Relais, Schütze, Vorschaltgeräte).
- Universelles Zubehör quer durch alle Serien: **ESY-Pen ESP425356 (175,00 €)**, **Mobil-PDi/MDi Service-Fernbedienung ESM425509 (35,00 €)**, **Mobil-PDi/User Endanwender-FB ESM425547 (35,00 €)**, **RC-Filter/Löschglied PD-C ESP426988 (16,00 €)**, **Schutzkorb 180/90 ESM425608 (34,00 €)**, **Schutzkorb 165/70 ESM425615 (32,00 €)**, **Deckeneinbauset PD-C/MD-C ESM425929 (10,00 €)**.

### Serie COMPACT — PD-C 360i/24 DUOplus (S.121–123)
**PD-C 360i/24 DUOplus-FM (Aufputz, ESP426803, 192,00 €)** und **DUOplus-SM (ESP426810, 192,00 €)**:
- 360°, Deckenmontage, Reichweite **Ø24 m**, empfohlene Montagehöhe **3 m**.
- Steuert **2 unabhängige Beleuchtungszonen** (Fensterbereich + Innenbereich) tageslicht- und anwesenheitsabhängig.
- Zusätzlicher Schaltkontakt **Kanal 3 HLK** für weitere Lichtquelle oder Heizung/Lüftung/Klima.
- Leistungsaufnahme **0,3 W**; Einschaltstrom **800 A / 200 µs**.
- Kanäle Licht **2**, Kontaktart Licht Schließer/potenzialbehaftet, Nachlaufzeit Licht Impuls/ca. **1–30 min**.
- Kanäle Präsenz/HLK **1**, Kontaktart Schließer/potenzialfrei, Nachlaufzeit HLK ca. **1–30 min**.
- Master/Slave **JA (max. 10 Slaves)**; parallel schaltbare Melder **0**.
- Umgebungstemperatur **−25 °C…+50 °C**; **Schutzart IP20**.
- Erfassungsbereich: Gehbereich/quer **Ø24 m**, frontal **Ø11 m**, Präsenzbereich **Ø8 m**.
- Maßskizze: **Ø108 mm**, Höhe 28 mm / 46 mm.
- Zubehör u.a.: Deckeneinbau-Set ESP426896 (19,00 €), Abdeck-Set silber ESP425431 (18,00 €).

### Serie COMPACT — PD-C 360i/40 Corridor / Warehouse (S.124–125)
- **Corridor (ESP428180, 143,00 €)**: 360°, große Reichweite **bis 40 m in Korridoren/Gängen**, empf. Montagehöhe **3 m**, max. Montagehöhe **10 m**.
- **Warehouse (ESP423062, auf Anfrage)**: empf. Montagehöhe **10 m**, max. **15 m**; Reichweite bis **40 m Länge × 4 m Breite**, für Lagerhallen.
- Leistungsaufnahme **0,3 W**; Einschaltstrom **800 A / 200 µs**; Kanäle Licht **1**; Schaltlast 2300 W/10 A bzw. 1150 VA/5 A.
- Kanäle Präsenz/HLK **0**; Master/Slave **JA (max. 10 Slaves)**; **IP20**; −25 °C…+50 °C.
- Erfassung Corridor: quer ca. **Ø40 m**, frontal ca. **Ø20 m**, Präsenz ca. **Ø8 m**.
- Maßskizze: Ø108 mm.
- Zubehör: Aufputzdose-C IP20 (ESM425370 11,00 € / silber ESP425387 20,00 €), Aufputzdose-C IP54 (ESM425905 13,00 € / silber ESP425912 20,00 €).

### Serie COMPACT EXPRESS — PD-CE 360i/8 (S.126–127)
- **ESP510700, 153,00 €** (Slave PD-CE 360/8 ESP510748, 132,00 €).
- 360°, Deckeneinbau, Reichweite **Ø8 m**, empf. Montagehöhe **3 m**, max. **5 m**; für kleine Räume/Durchgänge mit Tageslicht.
- Leistungsaufnahme **0,3 W**; Einschaltstrom **800 A / 200 µs**; Kanäle Licht 1; Schaltlast 2300 W/10 A / 1150 VA/5 A.
- Master/Slave **JA (max. 10 Slaves)**; **Schutzart IP40**; −25 °C…+50 °C.
- Schaltpläne A/B/C/D (D = Master-Slave). RC-Filter bei Induktivitäten erforderlich.
- Erfassung: quer ca. Ø8 m, frontal ca. Ø6 m, Arbeitsbereich ca. Ø4 m.
- Maßskizze: Ø82 mm / Ø68 mm; Höhen 67 mm / 32 mm; Leitungslänge 1000 mm.

### Serie COMPACT EXPRESS — PD-CE 360i/24 (S.128–129)
- **ESP510724, 176,00 €** (Slave PD-CE 360/24 ESP510755, 154,00 €).
- 360°, Deckeneinbau, Reichweite **Ø24 m**; für Büros, Klassenzimmer, Konferenzräume; auch große Höhen **bis 10 m** (Sport-/Lagerhallen).
- **0,3 W**; Einschaltstrom **800 A / 200 µs**; Kanäle Licht 1; Schaltlast 2300 W/10 A / 1150 VA/5 A.
- Master/Slave **JA (max. 10 Slaves)**; **IP40**; −25 °C…+50 °C.
- Erfassung: quer Ø24 m, frontal Ø11 m, Präsenz Ø8 m. Maßskizze Ø82/Ø68 mm, 67/32 mm.

### Serie COMPACT MINI — PD-C 360i/6 mini (S.130–131)
- **ESM425868, 114,00 €**.
- 360°, Deckeneinbau- und **Wandmontage**, Reichweite **Ø6 m**; für kleine Räume, Toiletten, kleine Büros, Flure.
- Neue universale ESYLUX-Klemmtechnik (Einbau in Decken, Markenschalter-Rahmen, Leuchten, UP-Dosen, Schränke).
- Leistungsaufnahme **0,2 W**; **Einschaltstrom 30 A / 20 ms** (kleiner als andere Mini!); Kanäle Licht 1.
- **Schaltlast reduziert: Glüh/Halogen 690 W / 3 A; Fluoreszenz 345 VA / 1,5 A.**
- **Master/Slave NEIN**; **Anzahl parallel schaltbarer Melder 10**; **Schutzart IP65** (höchste in der Mini-Reihe); −25 °C…+50 °C.
- Erfassung: quer ca. Ø6 m, Arbeitsbereich ca. Ø2,5 m. Maßskizze 20/36 mm, 11/25 mm.
- Zubehör: Spot-Adapter 51/20 ESP426384 (14,00 €).

### Serie COMPACT MINI — PD-C 360i/8 mini (S.132–133)
- **ESP426025, 127,00 €** (Slave PD-C 360/8 mini ESP426063, 105,00 €).
- 360°, Deckeneinbau, Reichweite **Ø8 m**; 0,2 W; Einschaltstrom **800 A / 200 µs**.
- Nachlaufzeit Licht Impuls/ca. **1–15 min**; Schaltlast 2300 W/10 A / 1150 VA/5 A.
- Master/Slave **JA (max. 10 Slaves)**; **Schutzart IP55**; −25 °C…+50 °C.
- Erfassung: quer ca. Ø8 m, frontal ca. Ø5 m, Arbeitsbereich ca. Ø3 m. Maßskizze 25/45 mm, 15/33 mm.
- Zubehör: Spot-Adapter 51/25 ESP426391 (15,00 €).

### Serie COMPACT MINI — PD-C 360i/8 mini-3m (S.134–135)
- **ESP427015, 140,00 €** (Slave ESP426063, 105,00 €).
- Wie /8 mini, jedoch **feste Anschlussleitung 300 cm**; Reichweite Ø8 m; 0,2 W; Einschaltstrom 800 A/200 µs.
- Nachlaufzeit Licht Impuls/ca. **1–15 min**; Master/Slave JA (max. 10); **IP55**; −25 °C…+50 °C.
- Erfassung quer Ø8 m / frontal Ø5 m / Arbeitsbereich Ø3 m.

### Serie COMPACT MINI — PD-C 360i/12 mini (S.136–137)
- **ESP426032, 136,00 €**.
- 360°, Deckeneinbau, Reichweite **Ø12 m**; für größere Räume/Büros/Flure mit Tageslicht.
- 0,2 W; Einschaltstrom **800 A / 200 µs**; Nachlaufzeit Licht ca. **1–30 min**; Schaltlast 2300 W/10 A / 1150 VA/5 A.
- Master/Slave **JA (max. 10 Slaves)**; **IP55**; −25 °C…+50 °C.
- Erfassung: quer ca. Ø12 m, frontal ca. Ø6 m, Arbeitsbereich ca. Ø4 m. Maßskizze 25/45 mm, 25/58 mm.

### Serie STANDARD — PD 360i/8 (S.138–139)
- **Master ESM425004, 139,00 €** (Slave PD 360/8 ESM425028, 106,00 €).
- 360°, Deckenmontage, Reichweite **Ø8 m**; **Leistungsaufnahme 1 W** (höher als COMPACT-Serie).
- Einschaltstrom 800 A/200 µs; Nachlaufzeit Licht Impuls/ca. **15 sek – 30 min**; 16-A-Relais Glüh 2300 W/10 A; Fluoreszenz 1150 VA/5 A.
- **Kanäle Präsenz/HLK 1**, Kontaktart **potenzialfrei, 230 V~/2 A, 24 V=/2 A**, Nachlaufzeit HLK Impuls/ca. **5–120 min**.
- Master/Slave **JA (max. 6 Slaves)** (nicht 10!); **Umgebungstemperatur 0 °C…+50 °C**.
- **Schutzart IP20 (Unterputz-Version), IP54 mit Aufputzdose.**
- Erfassung: quer ca. Ø8 m, frontal ca. Ø4 m, Arbeitsbereich ca. Ø3 m. Maßskizze Ø140 mm / Ø60 mm, 15/48 mm.
- Zubehör: Aufputzdose IP54 ESM425400 (14,00 €), Abdeck-Set ESM425455 (15,00 €).

### Serie STANDARD — PD 360i/24 (S.140–141)
- **Master ESM425103, 172,00 €** (Slave PD 360/24 ESM425127, 137,00 €).
- 360°, Deckenmontage, Reichweite **Ø24 m**, empf. Montagehöhe **3 m**; **1 W**.
- **Einschaltstrom 450 A / 20 µs**; Nachlaufzeit Licht Impuls/ca. **15 sek – 30 min**; Schaltlast 2300 W/10 A / 1150 VA/5 A.
- Kanäle Präsenz/HLK **1**, Kontaktart **potenzialfrei, 230 V~/2 A, 24 V=/2 A**, Nachlaufzeit HLK **5–120 min**.
- Master/Slave **JA (max. 6 Slaves)**; **0 °C…+50 °C**; **IP20 (UP) / IP54 (mit Aufputzdose)**.
- Erfassung: quer ca. Ø24 m, frontal ca. Ø8 m, Arbeitsbereich ca. Ø6 m. Maßskizze Ø140 mm/Ø60 mm, 15/60 mm.

### Serie STANDARD — PD 180i/R Wand-Präsenzmelder (S.142–143)
- **Master ESM410017, 131,00 €** (Slave MD/PD 180 ESM410024, 103,00 €, Reichweite 8 m).
- **180° Erfassung, Wandmontage**; automatische Lichtsteuerung anwesenheits-/tageslichtabhängig; 16-A-Relais.
- **1 W**; Einschaltstrom 800 A/200 µs; Nachlaufzeit Licht Impuls/ca. **12 sek – 60 min**; Schaltlast 2300 W/10 A / 1150 VA/5 A.
- Kanäle Präsenz/HLK **1**, Kontaktart Schließer/potenzialfrei, Nachlaufzeit HLK **5–120 min**.
- Master/Slave **JA (max. 6 Slaves)**; **0 °C…+50 °C**; **Schutzart IP20, IP44 je nach Abdeckung**.
- Erfassung bei Montagehöhe 1,1 m / 2,2 m: quer **Ø16 m**, frontal **Ø12 m**, Präsenzbereich **Ø8 m**.
- Maßskizze 70/63 mm, 34/61/70 mm.
- Zubehör (VISIO-50-relevant!): **VISIO 50 Bewegungsmelder-Abdeckung für MD180 mit Sonderrahmen 55×55 mm ESM055270 (15,20 €)**; Sonder-Rahmen 1-fach (Zentralplattenmaß 55×55 mm) EV105021 (2,49 €); Aufputzdose IP44 ESM055164 (37,00 €); Abdeckungen IP44/IP20 in diversen Farben (signalweiß/cremeweiß/Edelstahloptik) ESM055xxx (13,00–34,00 €).

### Serie FLAT — PD-FLAT 360i/8 ROUND/SQUARE (S.144–145)
- Design-Präsenzmelder, Reichweite ca. **Ø8 m**, empf. Montagehöhe **2,5 m**.
- **1 Kanal, Schalten, mit Nulldurchgangsschaltung optimiert für LED-Leuchten**; Master/Slave (Parallelschaltung).
- Flache Optik, austauschbare Design-Abdeckungen Kunststoff rund/weiß (alternativ Glas, quadratisch, schwarz).
- 0,3 W; **Einschaltstrom 78 A / 5 ms**; Kontaktart Schließer/potenzialbehaftet; **parallel schaltbare Melder 10**; Nachlaufzeit Licht **1–30 min**; Schaltlast 2300 W/10 A / 1150 VA/5 A.
- **0 °C…+50 °C**; **IP20**.
- Varianten/Preise je 113,00 €: ROUND WH ESP427930, ROUND BK ESP427954, SQUARE WH ESP427923, SQUARE BK ESP427947.
- Erfassung: quer ca. Ø8 m, frontal ca. Ø6 m, Präsenzbereich ca. Ø4 m. Maßskizze Ø94 mm / Ø60 mm.
- Glas-Abdeckungen FLAT GLASS (rund/quadratisch, WH/BK/GREY) ESP007xxx je 37,00 €; Deckeneinbau-Set FLAT ESP426889 (11,00 €).

### Serie FLAT — PD-FLAT-E 360i/8 ROUND (S.146–147)
- **ESP428555, 117,00 €**; inkl. **PD-FLAT Einbaudose**; sonst wie FLAT ROUND.
- Ø8 m, 2,5 m Montagehöhe; 1 Kanal Nulldurchgang LED-optimiert; Master/Slave; 0,3 W; Einschaltstrom 78 A/5 ms; parallel 10; **IP20**; 0 °C…+50 °C.
- Maßskizze Ø63/6 mm, 70 mm; Ø94 mm.

### Serie FLAT — PD-FLAT 360i/8 LARGE ROUND (S.148–149)
- **ESP428623, 117,00 €**.
- Wie FLAT ROUND, größere runde Abdeckung; Ø8 m; 2,5 m; Nulldurchgang LED-optimiert; Master/Slave; 0,3 W; 78 A/5 ms; parallel 10; Nachlaufzeit **1–30 min**; **IP20**; 0 °C…+50 °C.
- Maßskizze **Ø104 mm** / Ø60 mm, 30/24 mm.

### Serie BASIC — PD 360i/8 BASIC (S.150–151)
- Varianten: **PD 360i/8 Basic ESB430435 (88,00 €)**, **PD 360/8 Basic ESB430411 (76,00 €, nicht fernbedienbar)**, **PD 360i/8 Basic SMB ESB430473 (93,00 €, größerer Verdrahtungsraum)**, **PD 360/8 Basic SMB ESB430480 (80,00 €)**.
- 360°, Deckenmontage, Reichweite **Ø8 m**, empf. Montagehöhe **3 m**; **10-A-Hochleistungsrelais**; **Nulldurchgangsschaltung** für schonendes Schalten; Werkseinstellung.
- 0,2 W; Einschaltstrom **78 A / 5 ms**; Kanäle Licht 1; **parallel schaltbare Melder 6**; Nachlaufzeit Licht **15 sek – 30 min**; Schaltlast 2300 W/10 A / 1150 VA/5 A.
- Kanäle Präsenz/HLK 0; Master/Slave **JA (max. 6 Slaves)**; **0 °C…+50 °C**; **IP40**.
- Erfassung: quer ca. Ø8 m, frontal ca. Ø6 m, Präsenzbereich ca. Ø4 m. Maßskizze Ø101 mm, 33 mm (Basic) bzw. 50 mm (SMB).

### Serie BASIC — PD 360i/24 BASIC (S.152–153)
- Varianten: **PD 360i/24 Basic ESB430879 (120,00 €)**, **PD 360/24 Basic ESB430855 (107,00 €)**, **PD 360i/24 Basic SMB ESB430916 (125,00 €)**, **PD 360/24 Basic SMB ESB430893 (112,00 €)**.
- 360°, Deckenmontage, Reichweite **Ø24 m**, empf. Montagehöhe **3 m**; **10-A-Relais**; Nulldurchgangsschaltung.
- 0,2 W; Einschaltstrom 78 A/5 ms; Kanäle Licht 1; **parallel schaltbare Melder 6**; **Master/Slave NEIN**; Nachlaufzeit Licht **15 sek – 30 min**; Schaltlast 2300 W/10 A / 1150 VA/5 A; **IP40**; 0 °C…+50 °C.
- Erfassung: quer ca. Ø24 m, frontal ca. Ø11 m, Präsenzbereich ca. Ø8 m. Maßskizze Ø101 mm, 53 mm (Basic) / 73 mm (SMB).

### KNX Bewegungs- und Präsenzmelder — Auswahlhilfe (S.154–155)
Übersichtstabelle (Montageart · Winkel · Präsenz Ø · Erfassung Ø · max. Fläche · Fernbedienbar · Kanal Licht/HLK · Schutzart · Typ · Katalogseite):
- Deckeneinbau · 360° · Ø6 m · Ø8 m · bis 50 m² · ✔ · 2/1 · IP20 · **PD-ATMO 360i/8 A KNX** · S.162
- Deckeneinbau · 360° · Ø6 m · Ø8 m · bis 50 m² · ✔ · 2/1 · IP20 · **PD-ATMO 360i/8 T KNX** · S.162
- Deckeneinbau · 360° · Ø6 m · Ø8 m · bis 50 m² · ✔ · 2/1 · IP20 · **PD-ATMO 360i/8 O KNX** · S.164
- Deckeneinbau · 360° · Ø6 m · Ø8 m · bis 50 m² · ✔ · 2/1 · IP20 · **PD-FLAT 360i/8 ROUND KNX** · S.166
- Deckeneinbau · 360° · Ø6 m · Ø8 m · bis 50 m² · ✔ · 2/1 · IP20 · **PD-FLAT 360i/8 SQUARE KNX** · S.168
- Deckeneinbau · 360° · Ø6 m · Ø8 m · bis 50 m² · ✔ · 2/1 · IP20 · **PD-FLAT 360i/8 LARGE ROUND KNX** · S.170
- Deckeneinbau · 360° · Ø5 m · Ø8 m · bis 50 m² · ✔ · 2/1 · IP55 · **PD-C 360i/8 mini KNX** · S.172
- Deckeneinbau · 360° · Ø4 m · Ø12 m · bis 113 m² · ✔ · 2/1 · IP55 · **PD-C 360i/12 mini KNX** · S.174
- Deckeneinbau · 360° · Ø6 m · Ø8 m · bis 50 m² · ✔ · 2/1 · IP20 · **PD-C 360i/8 KNX UP** · S.176
- Deckeneinbau · 360° · Ø11 m · Ø24 m · bis 453 m² · ✔ · 2/0 · IP20 · **PD-C 360i/24 KNX ECO UP** · S.178
- Deckeneinbau · 360° · Ø8 m · Ø32 m · bis 805 m² · ✔ · 2/1 · IP20 · **PD-C 360i/32 KNX UP** · S.180
- Wand · 180° · Ø8 m · Ø16 m · bis 101 m² · ✔ · 2/0 · IP20/IP44 · **PD-C 180i/16 Touch KNX** · S.182
- Deckenaufbau · 360° · Ø6 m · Ø8 m · bis 50 m² · − · 1/0 · IP40 · **PD 360/8 KNX BASIC** · S.184
- Bewegungsmelder Decke/Wand · 230° · Ø8 m · Ø40 m · bis 804 m² · − · 2/1 · IP54 · **RC 230 KNX** · S.186

### KNX Vergleichstabelle Serie ATMO (S.156)
**PD-ATMO 360i/8 A / T / O KNX** — Erfassung frontal Ø6 m, quer Ø8 m, 360°, empf. Montagehöhe **3 m**; Kanäle Licht **2**; Helligkeit **5–2000 lx**; Kanäle Präsenz/HLK **1**; Nachlaufzeit Präsenz **0, 1–60 min, 12 h**; Master/Slave JA (konfigurierbar als Master oder Slave); Fernbedienbar JA; **Umgebungstemperatur 5 °C…+35 °C** (enger Bereich); **IP20**.
- Betriebsspannung: A = **29–31 V** (Busgerät), 0,2 W; T = **230 V/50 Hz**, 0,3 W; O ebenfalls 230 V-Klasse.
- Artikel: A **ESP427206 / 328,00 €**, T **ESP427213 / 284,00 €**, O **ESP427220 / 482,00 €**.
- Zubehör: Deckeneinbau-Set-C ESM425929 (10,00 €), Mobil-PDi/User ESM425547 (35,00 €), ESY-Pen ESP425356 (175,00 €).

### KNX Vergleichstabelle Serie FLAT (S.157)
**PD-FLAT 360i/8 ROUND/SQUARE/LARGE ROUND KNX** — Präsenz Ø4 m, frontal Ø6 m, 360°, Montagehöhe **2,5 m**; Kanäle Licht **2**; **Helligkeit 3–1000 lx**; Kanäle Präsenz/HLK **1**; Nachlaufzeit Präsenz **0, 1–60 min, 12 h**; Master/Slave JA (konfigurierbar); Fernbedienbar JA; Betriebsspannung **29–31 V**; 0,2 W; **5 °C…+35 °C**; **IP20**.
- Artikel: ROUND **ESP451706 / 126,00 €**, SQUARE **ESP451713 / 126,00 €**, LARGE ROUND **ESP428685 / 131,00 €**.
- Zubehör: Deckeneinbau-Set FLAT ESP426889 (11,00 €), Mobil-PDi/User 35,00 €, ESY-Pen 175,00 €.

### KNX Vergleichstabelle Serie COMPACT MINI (S.158)
**PD-C 360i/8 mini KNX** vs. **PD-C 360i/12 mini KNX** — Präsenz Ø3 m / Ø4 m; frontal Ø5 m / Ø6 m; 360°; Montagehöhe **3 m**; Kanäle Licht **2**; Master/Slave JA (konfigurierbar); Helligkeit **5–2000 lx**; Kanäle Präsenz/HLK **1**; Nachlaufzeit Präsenz **deaktiviert / 30 s – 12 h**; Fernbedienbar JA; Betriebsspannung **29–31 V**; 0,2 W; **5 °C…+50 °C**; **IP55**.
- Artikel: /8 **ESP426155 / 146,00 €**, /12 **ESP426162 / 155,00 €**.
- Zubehör: Spot-Adapter 51/25 ESP426391 (15,00 €), Mobil-PDi/User & /MDi je 35,00 €, ESY-Pen 175,00 €.

### KNX Vergleichstabelle Serie COMPACT (S.159–160)
**PD-C 360i/8 KNX UP · PD-C 360i/32 KNX UP · PD-C 360i/24 KNX ECO UP**:
- Präsenz Ø4 m / Ø8 m / Ø8 m; frontal Ø6 m / Ø11 m / Ø11 m; 360°; Montagehöhe je **3 m**; Kanäle Licht **2**; Master/Slave JA (konfigurierbar); Helligkeit **5–2000 lx**; Kanäle Präsenz/HLK **1**.
- Nachlaufzeit Präsenz: /8 = **0, 30 s, 1 min, 12 h**; /32 = **10 s – 1 h**; /24 ECO = **0, 1–60 min, 12 h**.
- Betriebsspannung **29–31 V**; 0,2 W; **5 °C…+50 °C**; **IP20**.
- Artikel: /8 **ESP427404 / 145,00 €**, /32 **ESP427794 / 190,00 €**, /24 ECO **ESP427435 / 153,00 €**.
- Zubehör u.a.: Abdeck-Set ESP425936 (18,00 €) bzw. ESP425431 (18,00 €), Deckeneinbau-Set-C ESM425929 (10,00 €).

**PD-C 180i KNX ECO (Wand, S.160)** — Präsenz Ø8 m, frontal Ø6 m, **180°**, Montagehöhe **1,1 m**; Kanäle Licht **2**; Master/Slave JA (konfigurierbar); Helligkeit 5–2000 lx; Kanäle Präsenz/HLK **1**; Nachlaufzeit Präsenz **0, 1–60 min, 12 h**; Fernbedienbar JA; **29–31 V**; 0,2 W; **5 °C…+50 °C**; **IP20/IP44**.
- Artikel **ESP426452 / 132,00 €**; Zubehör: Abdeckung IP20-SKK ESM055270 (15,20 €), Mobil-PDi/User 35,00 €, ESY-Pen 175,00 €.
