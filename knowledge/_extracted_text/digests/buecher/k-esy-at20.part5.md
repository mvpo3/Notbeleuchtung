# k-esy-at20 — Teil 5
> Quelle: k-esy-at20 (buecher) · Seiten 201-240.

Dieser Teil ist ein **Schrack/ESYLUX-Produktkatalog** für Präsenz- und Bewegungsmelder (Innen + Außen) sowie deren Zubehör. Er ist kein Norm-/Regelwerk-Text, sondern Geräte-Datenblätter mit technischen Tabellen (Erfassungswinkel/-bereich, Spannung, Schaltleistung, Schutzart, Montagehöhe) und Bestelldaten. Inhalt von Teil 5: **DALI-Präsenzmelder** (S. 201–209), **12-36V Bewegungs-/Präsenzmelder** (S. 210–225), **1-10V Präsenzmelder** (S. 226–233) und **Zubehör** (Abdeckungen, Aufputzdosen, Ecksockel; S. 234–240). Relevanz fürs Projekt: konkrete Geräteparameter (Montagehöhe, Erfassungsbereich vs. Fläche, Schaltleistung, Schnittstelle DALI/0-10V/1-10V/potentialfrei), VISIO-50-Kompatibilität und Schaltbild-Logik (Standard / Tasteransteuerung / Master-Slave).

## Inhalt

### DALI-Präsenzmelder (S. 201–209)
Serien FLAT MINI, COMPACT MINI, COMPACT. Gemeinsame Schaltplan-Topologie: separate **DALI Power Supply CU PS DALI** (EC10430008 / Best.-Nr. ESC430008, 230V L/N in, DA+/DA- out), Melder an DA+/DA-, DALI-EVG am selben Bus. Abmessungen CU PS DALI: 48x45x25mm LxBxT, Ø68mm; 55,00 €.

**PD-FLAT 360i/6 mini DALI** (S. 201–202, Best.-Nr. ESP427503, 119,00 €):
- Erfassungswinkel 360°; Betriebsspannung 9,5–22,5 V (DALI-Bus); Leistungsaufnahme 0,3 W
- Master/Slave: JA; Kanäle Licht 1; Kanäle Präsenz/HLK 2
- Einstellbereich Helligkeit 10–2000 lx; Nachlaufzeit Licht ca. 1–15 min
- Umgebungstemperatur -25°C…+50°C; Schutzart IP55; Einstellung per IR-Fernbedienung
- Deckenmontage 360°, empf. Montagehöhe 3 m; Erfassung: Gehbereich/quer ca. Ø8m, frontal ca. Ø5m, Arbeitsbereich ca. Ø3m
- Maßskizze: 25mm / 45mm / 15mm / 33mm

**PD-C 360i/8 mini DALI** (S. 203, ESP427510, 123,00 €):
- 360°, 9,5–22,5 V, 0,3 W, Master/Slave JA, Kanäle Licht 1 / Präsenz-HLK 2, 10–2000 lx, Nachlauf ca. 1–15 min, -25°C…+50°C, IP55, IR-Fernbedienung
- Erfassung: Gehbereich/quer ca. Ø8m, frontal ca. Ø6m (lt. S. 204: Ø4/Ø6/Ø8), Arbeitsbereich ca. Ø3m. Maßskizze: 25/45/15/33mm

**PD-C 360i/8 DUO DALI** (Serie COMPACT, S. 204–205, ESP427442, 147,00 €):
- 360°; Betriebsspannung 230V / 50Hz; Leistungsaufnahme 0,6 W; Master/Slave JA
- Kanäle Licht **2**; Kanäle Präsenz/HLK 0; Einstellbereich Helligkeit 5–2000 lx; Nachlauf ca. 1–15 min
- -25°C…+50°C; Schutzart: IP20 als Unterputz-Version, IP20/IP54 mit Aufputzdose, IP20 als Deckeneinbau-Version
- Einstellung: Einstellregler/Potentiometer **und** IR-Fernbedienung
- Reichweite bis Ø8m, empf. Montagehöhe 3 m; Erfassung Ø4/Ø6/Ø8m. Steuert DALI/DSI EVGs auf konstantes Helligkeitsniveau
- Maßskizze: Ø108mm / Ø60mm / 24mm / 38mm
- Slave: PD-C360/8 Slave weiß (ESP055379, UP, Ø8m, 106,00 €)

**PD-C 360i/24 DUO DALI** (S. 206–207, ESP427459, 172,00 €):
- 360°, 230V/50Hz, 0,6 W, Master/Slave JA, Kanäle Licht 2 / Präsenz-HLK 2, 5–2000 lx, Nachlauf ca. 1–15 min, -25°C…+50°C
- Schutzart wie oben (IP20 UP / IP20-IP54 Aufputz / IP20 Deckeneinbau); IR-Fernbedienung
- Reichweite bis Ø24m, Montagehöhe 3 m; Erfassung: Gehbereich/quer Ø24m, frontal Ø11m, Präsenzbereich Ø8m
- Maßskizze: Ø108 / Ø60 / 24 / 46mm
- Slave: PD-C360/24 Slave weiß (ESP055386, Ø24m, 130,00 €)

**PD-C 360i/32 DUO DALI** (S. 208–209, ESP427787, 192,00 €):
- 360°, 230V/50Hz, 0,6 W, Master/Slave JA, Kanäle Licht 2 / Präsenz-HLK 2, 5–2000 lx, Nachlauf ca. 1–15 min, -25°C…+50°C, Schutzart wie oben, IR-Fernbedienung
- Reichweite bis Ø32m, Montagehöhe 3 m; Erfassung: Gehbereich/quer ca. Ø32m, frontal ca. Ø11m, Arbeitsbereich ca. Ø8m
- Maßskizze: Ø108 / Ø60 / 24 / 46mm
- Slave: PD-C360i/32 Slave (ESP427770, IR 360°, UP, Ø32m, 151,00 €)

**Gemeinsame Schaltbild-Legende (DUO-DALI-Melder):**
- A = Standardbetrieb
- B = Standardbetrieb mit zusätzlicher Ansteuerung durch Schließtaster (Licht per Taster manuell ein-/ausschaltbar)
- C = Master-Slave-Schaltung: Master schaltet Verbraucher je nach Parametern; Slaves dienen nur der Präsenzerfassung und geben bei Bewegung Impuls an Master. **Achtung: max. 10 Slave-Geräte pro Master.**

### 12-36V Bewegungs- und Präsenzmelder (S. 210–225)
Geräte für Gebäudeautomation; **Betriebsspannung 12–36 V Gleich- oder Wechselspannung (AC/DC)**; potentialfreier softwaregesteuerter Schaltausgang (Öffner/Schließer), zu-/abschaltbare Detektionsanzeige, geräuschloses Schalten **bis max. 2A**.

**Auswahlhilfe (S. 211):**
| Typ | Montage | Winkel | Erfassungsbereich | Fläche | Fernbed. | Kanal L/HLK | Schutzart | Seite |
|-----|---------|--------|-------------------|--------|----------|-------------|-----------|-------|
| PD-C 360i/8 mini UC | Deckeneinbau | 360° | Ø8m | bis 50 m² | ✔ | 1/0 | IP55 | 214 |
| PD-C 360i/8 UC | Decke | 360° | Ø8m | bis 50 m² | ✔ | 1/0 | IP20/IP54 | 216 |
| PD-C 180i/16 UC | Wand | 180° | Ø16m | bis 101 m² | ✔ | 1/0 | IP20/IP44 | 218 |
| PD-C 360i/24 UC | Decke | 360° | Ø24m | bis 453 m² | ✔ | 1/0 | IP20/IP54 | 220 |
| RC 230i UC (Bewegungsmelder) | Decke/Wand | 230° | Ø40m | bis 804 m² | ✔ | 1/0 | IP54 | 224 |

**Vergleichstabelle RC 230i UC vs. PD-C 360i/8 mini UC (S. 212):**
- RC 230i UC: Erfassung frontal Ø8m; Winkel 230°; empf. Montagehöhe 2,5 m; Kanäle Licht 1; Helligkeit 2–2500 lx; Master/Slave NEIN; max. 8 parallel schaltbare Melder; Betriebsspannung 12–24 V; 0,3 W; -25°C…+55°C; IP54; ESM015649 / 137,00 €. Zubehör: Mobil-RCi-M (ESM016011, 32,00 €), Mobil-RCi (ESM016004, 38,00 €)
- PD-C 360i/8 mini UC: Präsenz Ø3m / frontal Ø5m; 360°; Montagehöhe 3 m; Kanäle Licht 1; Schaltleistung Licht 12–36 V UC (~/=), 2 A; Helligkeit 5–2000 lx; Master/Slave NEIN; 12–36 V; 0,3 W; -25°C…+50°C; IP55; ESP427343 / 131,00 €. Zubehör: Mobil-PDi/MDi (ESM425509, 35,00 €)

**Vergleichstabelle COMPACT-Präsenzmelder (S. 213):**
| Merkmal | PD-C 360i/8 UC | PD-C 360i/24 UC | PD-C 180i/16 UC |
|---------|----------------|------------------|------------------|
| Präsenz / frontal | Ø4m / Ø6m | Ø8m / Ø11m | Ø8m / Ø6m |
| Winkel | 360° | 360° | 180° |
| Montagehöhe | 3 m | 3 m | 1,1 m |
| Kanäle Licht | 1 | 1 | 1 |
| Schaltleistung | 12–36 V UC (~/=), 2 A | 12–36 V UC (~/=), 2 A | 12–36 V UC (~/=), 2 A |
| Helligkeit | 5–2000 lx | 5–2000 lx | 5–2000 lx |
| Master/Slave | NEIN | NEIN | NEIN |
| Spannung | 12–36 V | 12–36 V | 12–36 V |
| Leistung | 0,3 W | 0,3 W | 0,3 W |
| Temp | -25…+50°C | -25…+50°C | -25…+50°C |
| Schutzart | IP20 UP / IP20-IP54 Aufputz / IP20 Deckeneinbau | dito | IP20, IP44 je nach Abdeckung |
| Best.-Nr / Preis | ESP427312 / 140,00 € | ESP427329 / 165,00 € | ESP427305 / 145,00 € |

**PD-C 360i/8 mini UC** (S. 214–215, ESP427343, 131,00 €): 360°, 12–36 V, 0,3 W, Kanäle Licht 1, Helligkeit 5–2000 lx, Kontaktart Schließer/potentialfrei, Schaltleistung 12–36 V UC (~/=) 2 A, -25°C…+50°C, IP55, IR-Fernbedienung. Erfassung Ø3/Ø5/Ø8m, Montagehöhe 3 m. Anschluss: 12-36V UC in (+/-), potentialfreier Ausgang, Output/Lux 0-10V DC, Switch on/off. Maßskizze 25/45/15/33mm. Zubehör: Spot-Adapter 51/25 (ESP426391, 15,00 €).

**PD-C 360i/8 UC** (S. 216–217, ESP427312, 140,00 €): 360°, 12–36 V, 0,3 W, Kanäle Licht 1, 5–2000 lx, Schließer/potentialfrei, 12–36 V UC 2 A, -25°C…+50°C. Schutzart IP20 UP / IP20-IP54 Aufputz / IP20 Deckeneinbau. Schaltplan-Klemmen: A1(+)/A2(-) 12-36V UC, B1/B2, GND, 0-10V DC Ausgang. Erfassung Ø4/Ø6/Ø8m. Maßskizze Ø108/Ø60/24/38mm.

**PD-C 180i/16 UC** (Wandmontage, S. 218–219, ESP427305, 145,00 €): 180°, 12–36 V, 0,3 W, Master/Slave NEIN, Kanäle Licht 1, 5–2000 lx, Schließer/potentialfrei, -25°C…+50°C, IP20/IP44 je nach Abdeckung. Erfassung: Gehbereich/quer Ø16m, frontal Ø12m, Präsenzbereich Ø8m; vertikal 1,1m/2,2m; Montagehöhe-Referenz 1,1 m. Maßskizze 70/70/55/25/45mm. **VISIO-50-kompatibel**: VISIO 50 Bewegungsmelder-Abdeckung für MD180 mit Sonderrahmen 55x55mm (ESM055270, 15,20 €) + Sonder-Rahmen 1-fach 55x55mm (EV105021, 2,49 €). Diverse Abdeckungen IP20 (ESM055102/119/126/140, 13–16,00 €), Aufputzdose IP44 (ESM055164, 37,00 €).

**PD-C 360i/24 UC** (S. 220–221, ESP427329, 165,00 €): 360°, 12–36 V, 0,3 W, Master/Slave JA, Kanäle Licht 1, 5–2000 lx, Schließer/potentialfrei, 12–36 V UC 2 A, -25°C…+50°C, IP20 UP / IP20-IP54 Aufputz / IP20 Deckeneinbau. Erfassung Gehbereich/quer Ø24m, frontal Ø11m, Präsenzbereich Ø8m, Montagehöhe 3 m. Schaltplan-Klemmen A1(+)/A1(-), B1/B2, GND, S/S, 0-10V DC. Maßskizze Ø108/Ø60/24/46mm.

**MD-C 360i/6 mini 12V** (Innen-Bewegungsmelder, S. 222–223, ESP425776, 87,00 €): 360°, Betriebsspannung **12–13,2 V**, 0,3 W, Master/Slave NEIN, Kanäle Licht 1, Helligkeit 10–2000 lx, Schließer/potentialfrei, -25°C…+50°C, **IP65**. Anwendung: kleine Feuchträume, Toiletten, kleine Büros, Flure, Caravan, Automobil. Erfassung quer Ø6m / frontal Ø2,5m (Ø2,5/Ø6m), Montagehöhe 3 m. Werksprogramm fest hinterlegt. Schaltpläne A=Standardbetrieb PNP, B=NPN. Maßskizze 20/36/11/25mm. Zubehör: Spot-Adapter 51/20 (ESP426384, 14,00 €).

**RC 230i UC** (12-24V Außen-Bewegungsmelder, S. 224–225, ESM015649, 137,00 €): Betriebsspannung 12–24 V, 0,3 W, Master/Slave NEIN, Kanäle Licht 1, Helligkeit 2–2500 lx, Kontaktart Schließer/**potentialbehaftet**, Erfassungswinkel 230°, -25°C…+55°C, IP54, Einstellung Potentiometer + IR. **360° Unterkriechschutz** (abschaltbar per Fernbedienung), Reichweite Ø40m, frontal ca. Ø16m, Gehbereich/quer ca. Ø6m; vertikal 2,5m/3m/6m/8m; "blue mode"-Programmierung. Maßskizze 135/105/78mm. Zubehör: RC Ecksockel (ESM016110/127/134/141, 22–24,00 €), RC-Filter/Löschglied PD-C (ESP426988, 16,00 €).

### 1-10V Präsenzmelder (S. 226–233)
Serie COMPACT; **Betriebsspannung 230V / 50Hz**, Steuerausgang **1-10V =/50 mA**; LED-tauglich durch **Wolfram-Vorlaufkontakt (16A Hochleistungsrelais)**; Schaltleistung Licht: 230 V/50 Hz, 16 A Relais, 2300 W/10 A (cos φ = 1), 1150 VA/5 A (cos φ = 0,5).

**Auswahlhilfe (S. 227):**
| Typ | Montage | Winkel | Bereich | Fläche | Kanal L/HLK | Schutzart | Seite |
|-----|---------|--------|---------|--------|-------------|-----------|-------|
| PD-C 360i/8 DIM | Decke | 360° | Ø8m | bis 50 m² | 1/0 | IP20/IP54 | 230 |
| PD-C 360i/24 DIM | Decke | 360° | Ø24m | bis 453 m² | 1/0 | IP20/IP54 | 232 |

**PD-C 360i/8 DIM** (Vergleichstabelle S. 228; Datenblatt S. 230–231; ESP426711, 136,00 €):
- 360°, Ø8m, 230 V / 50 Hz, Steuerausgang 1–10 V =/50 mA, empf. Montagehöhe 3 m (max. 5 m), Decke/Unterputzmontage
- Kanäle Licht 1 (Datenblatt S.231: Kanäle Licht 2 / Präsenz-HLK 1), LED-tauglich (Wolfram-Vorlaufkontakt), Helligkeit 5–2000 lx
- Schaltleistung Licht 230 V/50 Hz, 16 A Relais, 2300 W/10 A (cos φ=1), 1150 VA/5 A (cos φ=0,5)
- Kontaktart Schließer/potentialbehaftet; Master/Slave JA; max. 10 parallel schaltbare Melder; fernbedienbar; 0,3 W; -25°C…+50°C
- Schutzart IP20 UP / IP54 Aufputz / IP20 Deckeneinbau; Einstellung Potentiometer + IR. Erfassung Ø4/Ø6/Ø8m. Maßskizze Ø108/Ø60/24/38mm
- Slave: PD-C360/8 Slave weiß (ESP055379, 106,00 €)

**PD-C 360i/24 DIM** (Vergleichstabelle S. 229; Datenblatt S. 232–233; ESP426704, 161,00 €):
- 360°, Ø24m, 230 V / 50 Hz, Steuerausgang 1–10 V =/50 mA, Montagehöhe 3 m (max. 5 m), Decke/Unterputz
- Kanäle Licht 1, LED-tauglich (Wolfram-Vorlaufkontakt), 5–2000 lx, Schaltleistung wie PD-C 360i/8 DIM (16 A Relais, 2300 W/10 A, 1150 VA/5 A)
- Kontaktart Schließer/potentialbehaftet; Master/Slave JA; max. 10 parallel; 0,3 W; -25°C…+50°C; IP20 UP / IP54 Aufputz / IP20 Deckeneinbau
- Erfassung: quer Ø24m, frontal Ø11m, Präsenzbereich Ø8m. Maßskizze Ø108/Ø60/24/46mm
- **PD-C 360i/24 DIMplus** (ESP425783, 157,00 €): wie DIM, jedoch mit zusätzlichem Schaltkontakt (Kanal 2 HLK) zum Schalten einer weiteren Lichtquelle oder zur Ansteuerung von Heizung/Lüftung/Klima abhängig von Anwesenheit; Ø32m
- Slave: PD-C360/24 Slave weiß (ESP055386, 130,00 €)

**Gemeinsame Schaltbild-Legende (DIM):** A=Standardbetrieb; B=Standardbetrieb mit zusätzlicher Ansteuerung durch Schließtaster (manuell ein-/ausschaltbar); C=Master-Slave, **max. 10 Slaves pro Master**.

### Zubehör (S. 234–240)
Abdeckungen, Aufputzdosen, Ecksockel/Eckwinkel, Abdeck-Sets. Auswahl mit Best.-Nr. und UVP:

- **Abdeckung FLAT ROUND** (Serie FLAT, Kunststoff matt; weiß/schwarz/betongrau): rund weiß ESP007231, schwarz ESP007279, grau ESP007316 — je 8,00 €. Glas-Variante FLAT GLASS RO (WH/BK/GREY: ESP007255/293/323) je 37,00 €.
- **Abdeckung FLAT SQUARE** (weiß/schwarz): quadratisch weiß ESP007248, schwarz ESP007286 — je 8,00 €. Glas FLAT GLASS SQ (WH ESP007262 / BK ESP007309) je 37,00 €.
- **Abdeckung LARGE FLAT ROUND** (Durchmesser 104mm, weiß/schwarz): ESP428579 / ESP428098 — je 9,00 €.
- **Aufputzdose IP20/IP44** für Wandmelder Serien Basic/Standard/Compact, Membran-Leitungseinführung 3-fach: ESM055164 (IP44, MD180i/R, MD180i/T, MD/PD180, weiß) 37,00 €. IP44 nur in Kombination mit Abdeckung ESM055270.
- **Aufputzdose IP54** für viele Decken-MD/PD-Melder, doppelte Membran-Leitungseinführung: ESM425400, 14,00 €.
- **Aufputzdose-C IP20** (Serie MD-C/PD-C, 4-fache Leitungseinführung): silber ESP425387 (20,00 €), weiß ESM425370 (11,00 €).
- **Aufputzdose-C IP54** (Serie MD-C/PD-C, 2-fache Leitungseinführung): silber ESP425912 (20,00 €), weiß ESM425905 (13,00 €).
- **Abdeckung IP44** für Wandmelder Basic/Standard/Compact (Feuchträume: Bäder, Garagen, Keller; vertikale Ausblendung mit Kappe; erhöhter Sabotageschutz durch Inbus-Edelstahlschrauben): ESM055157 (MD180i/R, MD180i/T, MD/PD180, weiß) 34,00 €.
- **Ecksockel RC-Serie** (Innen-/Außeneckmontage): weiß ESM016110, braun ESM016127, schwarz ESM016134 je 22,00 €, Edelstahloptik ESM016141 24,00 €.
- **Eckwinkel MD-Serie**: weiß ESM025518, braun ESM025525 — je 8,00 €.
- **Abdeckkappen Serie MD-W** (für MD-W200i): weiß ESM041099, braun ESM041105, schwarz ESM041112 je 13,00 €, Edelstahloptik ESM041129 15,00 €.
- **Abdeck-Sets** (Abdeckblende + Designring, silber): allg. ESM425455 (15,00 €); für PD-C360/8 + MD-C360/8 ESP425936 (18,00 €); für PD-C360/24 + MD-C360/24 ESP425431 (18,00 €).
- **VISIO-50-kompatible Abdeckung** (Schalterprogramm VISIO 50): VISIO 50 Bewegungsmelder Abdeckung für MD180 mit Sonderrahmen 55x55mm ESM055270 (15,20 €), kombinierbar mit VISIO-Sonderrahmen 55x55mm 1-fach EV105021 (2,49 €), 2-fach EV105022 (5,23 €), 3-fach EV105023 (8,05 €).
- **Abdeckung IP20 MD/PD 180** (vertikale Ausblendung mit Kappe): cremeweiß ESM055126, weiß ESM055102, signalweiß ESM055119 je 13,00 €; Edelstahloptik ESM055140, anthrazit ESM055133 je 16,00 €.

### Durchgängige Fernbedienungen / Tools (alle Serien)
- Mobil-PDi/User Endanwender-FB (ESM425547, 35,00 €), Mobil-PDi/Dali Service-FB (ESP425899, 37,00 €), Mobil-PDi/plus Service-FB silber/grün-metallic (ESM425530, 35,00 €), Mobil-PDi/MDi Service-FB (ESM425509, 35,00 €)
- Mobil-RCi-M (ESM016011, 32,00 €), Mobil-RCi (ESM016004, 38,00 €)
- DALI-Schaltmodule SW DALI Full/Semi Automation (UP, IP20): ESP427473 / ESP427480, je 43,00 €
- ESY-Pen (ESP425356, 175,00 €) — durchgängiges Konfigurations-Tool
- Schutzkorb 180/90 (ESM425608, 34,00 €), Schutzkorb 165/70 (ESM425615, 32,00 €); Deckeneinbauset PD-C/MD-C360 weiß (ESM425929, 10,00 €)
