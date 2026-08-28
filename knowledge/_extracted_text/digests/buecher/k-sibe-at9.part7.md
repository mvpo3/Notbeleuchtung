# k-sibe-at9 — Teil 7
> Quelle: k-sibe-at9 (buecher) · Seiten 281-320.

Schrack-Produktkatalog/Technik-Handbuch zur Sicherheitsbeleuchtung. Dieser Teil behandelt **Gruppen- und Zentralbatterieanlagen** (LPS = Low Power Systems / CPS = Central Power Systems) der Schrack-Anlagenfamilie (My-, Micro-, Mini-, MiniControl XL, Midi-, Maxi-, MultiControl, MDC) — Konzepte, Systemvergleich, Web-Interface, Einzelleuchtenschaltbarkeit sowie detaillierte technische Daten, Stromkreismodule, Batterien und Bestellnummern. Relevante Normen: OVE E 8101:2019, ÖVE-ÖNORM E 8002-1:2007, EN/ÖVE-ÖNORM EN 50171, EN 50172, EN 50272-2, (ÖVE/ÖNORM) EN 62034, OVE R 12-2.

## Inhalt

### Konzepte: LPS (Low Power System) vs. CPS (Zentralbatterie)
- **Low Power System (LPS, begrenzte Leistung):** Pro Brandabschnitt eine Anlage in einem Betriebsraum, versorgt ausschließlich Not- und Sicherheitsleuchten dieses Brandabschnitts. Dezentrales Konzept → **macht feuerfeste E30-Stromkabel gemäß ÖVE-ÖNORM E 8002-1:2007 und OVE E 8101:2019 überflüssig**. Mehrere LPS per TCP/IP vernetz- und überwachbar. **LPS bis zu einer Ausgangsleistung von 1.500 W zugelassen.**
- **Zentralbatteriesystem (CPS):** Versorgung aller Not-/Sicherheitsleuchten von einem zentralen Punkt; Zentralbatterieanlage im Betriebsraum, Verbindung zu Leuchten mit **feuerfesten E30-Leitungen**. Unterstationen und Unterverteiler anschließbar.
  - **Pro 19"-Schrank: bis zu 96 Stromkreise und 1.920 angeschlossene Leuchten.**
  - **Bis zu 32 Systeme** (auch unterschiedlicher Typen: my, micro, mini, midi, multiControl) per TCP/IP vernetz- und überwachbar → max. **61.440 Leuchten**.

### Gruppenbatterieanlagen (LPS) — Kurzprofile
- **MyControl:** max. 4 Stromkreise / 500 W, 1h / max. 80 Leuchten. Jüngste LPS-Entwicklung, brandabschnittsbezogen, in 2 Varianten/Ausführungen. Via TCP/IP vernetzbar.
- **MicroControl:** max. 6 Stromkreise / 500 W, 1h / 120 Leuchten. Dezentrales LPS bis max. 500 W; entfallende E30-Leitungsanlagen.
- **MiniControl (XL):** max. 12 (32) Stromkreise / 1500 W, 1h / 240 (640) Leuchten. Füllt Bereich zwischen MicroControl und MidiControl; je Brandabschnitt in einem Betriebsraum installiert.

### Zentralbatterieanlagen (CPS) — Kurzprofile
- **MidiControl:** max. 32 Stromkreise / 6.300 W (1h), 2.600 W (3h) oder 1.200 W (8h) / max. 640 Leuchten. Vorkonfiguriert; bis zu **16 DCM-Module für 32 Stromkreise**; Web-Interface; vernetzbar.
- **MaxiControl:** max. 60 frei programmierbare Stromkreise / 1.200 Leuchten. Nach **EN 50171**, 19"-Baugruppensystem, integrierte automatische Prüfeinrichtung. Front-Terminal-Batterien bis **150 Ah**. Einstündige Anlagen bis ca. **20,5 kW** (abzüglich 25% Alterungsreserve). Unterverteilungen/Unterstationen je bis zu **96 Kreisen**.
- **MultiControl:** max. 96 frei programmierbare Stromkreise / 1.920 Leuchten. Nach **EN 50171**, 19"-Baugruppensystem. Wand-/Stand-/Kompaktschränke. Bis zu **32 weitere Unterstationen** je bis zu 96 Kreisen.
- **MDC:** vorkonfiguriertes CPS **ohne Leistungsbegrenzung**. Je nach Gehäuse bis zu **72 Stromkreise à 10 A**, Ladeeinheit bis **17,5 A**, je eine Dauer- und Bereitschaftslichtumschaltung, im Standgehäuse. **Keine Einzelleuchten-/Stromkreisüberwachung möglich**; Schaltbarkeit der Stromkreise nur eingeschränkt / nur mit der jeweiligen Umschaltung. Vernetzbar, Web-Interface.

### Gehäuse / Bauform (Seite 290)
- Normkonforme Eigenentwicklungen nach **EN 50171** und **EN 50272-2**. Elektronikkomponenten von Batterie getrennt.
- Lieferbar in 2 separaten Gehäusen (Elektronik + Batterie, Wand- oder Standschrank) oder als **Kombischrank** (beides in einem Gehäuse, interne Schottung).
- Lackierung standardmäßig **Strukturlack RAL 7035**.
- Elektronik als 19"-Einschübe; Schwenkrahmen + Schranktür (180° schwenkbar), optional Klarsichttür.
- Standardgehäuse **Schutzart IP20**; höhere Schutzart (z.B. **IP54**) möglich.
- Anschlussfeld im Schrankinneren auf Montageplatte; kein zusätzlicher Rangierverteiler nötig. Kabeleinführung wahlweise oben/unten. Batterien auf Flachböden.

### Zentraleinheit / Steuerung NLSR (Seiten 292–293)
- Steuereinheit **NLSR** steuert My- bis MultiControl. Merkmale: 19"-Einschubtechnik, SD-Kartenslot (Firmware-Update), Ethernet-Port, integriertes Web-Interface, 2× USB Port 2.0, mehrsprachige Meldetexte, integrierter Boot-Loader, Fernwartung durch Hersteller.
- Konfiguration per Web-Interface oder Standard-USB-Tastatur (Pfeiltasten / 4-Wege-Navigationstasten). USB-Drucker mit **PCL6-Standard** anschließbar. 3 Schnellzugriffstasten unter Display.

### Einzelleuchtenschaltbarkeit (ELS) / Stromkreismodul DCM12E (Seiten 294–295)
- Modul **DCM12E**: Stromkreisbaugruppe für MicroControl, MiniControl (XL), MidiControl, MaxiControl, MultiControl. (MyControl hat fix verbaute, ELS-fähige Baugruppen.)
- Im Gegensatz zu DCM32/42/62 erfolgt **Zuweisung der Betriebsart einzelner Leuchten über die Anlage** (statt DIP-Schalter an der Leuchte). Weitere Funktionen (Dimmstufen, Blinkfunktion, Adressierung) an der Leuchte.
- DCM12E: 2 Stromkreise ("Kreis A"/"Kreis B"), je **max. Ausgangsstrom 1A (250VA)**; Strom-, Stromkreis- und Leuchtenüberwachung.
- **Mischen herkömmlicher Leuchten(-bausteine) mit ELS-fähigen ist NICHT zulässig.**
- 3 Leuchtenbetriebsarten: **Bereitschaftsschaltung** (nur Notbetrieb ein), **Dauerlicht** (dauerhaft ein), **geschaltetes Dauerlicht** (über SAM schaltbar). Leuchtenüberwachung selektiv deaktivierbar (Adressen für Nachrüstung freihalten). **Bis zu 6 Schaltbefehle** je Stromkreis; Gruppen oder Einzelleuchten schaltbar.

### Web-Interface / Visualisierung (Seiten 296–297)
- Abfrage/Steuerung/Wartung von beliebigem PC mit Standardbrowser, auch über Internet (LPS oder CPS). Stromkreisübersicht listet alle DCM-Module + Leuchtenanzahl + Betriebsart + Gebäudeposition.
- Leistungsaufnahme wird beim Anlagentest gemessen, mit Referenzwert verglichen. **Bei einstellbarer Abweichung von 5–50% vom Referenzwert → Stromfehler ausgelöst.**
- Pro Stromkreis bis zu **6 SAM-Schaltungen** zuweisbar.
- Multi-/MaxiControl: Visualisierung ohne Zusatzsoftware; Leuchten per Drag & Drop auf Grundrissplan platzierbar; Pläne im NLSR oder auf NAS ablegbar.

### Systemvergleichstabelle (Seite 298)

| Merkmal | MyControl (MY) | MicroControl (ML) | MiniControl (MN) | MiniControl XL (MNX) | MidiControl (MD) | MaxiControl (MCX) | MultiControl (MC) | MDC |
|---|---|---|---|---|---|---|---|---|
| Gehäuse (HxBxT mm) | 900×450×125 | 660×350×230 | 1100×500×230 | 1470×570×230** | 1950×600×450 | verschieden | verschieden | verschieden |
| max. Stromkreise | 4 (+1)* | 6 (+1)* | 12 (+1)* | 32** | 32 | 60 | 96 | 72 |
| max. Strom im Endstromkreis | 2A | 3A | 3A | 4A | 6A* | 6A* | 6A* | – |
| mögliche Stromkreismodule | – | DCM12-E/32 | DCM12-E/32 | DCM12-E/42 | DCM12-E/32/42/62 | (s. Modulliste) | (s. Modulliste) | D01 / LSS |
| Anlagentyp | LPS / CPS | LPS | LPS | LPS | CPS | CPS | CPS | (CPS) |
| max. Anschlussleistung AC (Gesamt) | 800 VA | 2.000 VA | 2.000 VA | 2.000 VA | 7.000 VA | 43.000 VA | 43.000 VA | – |
| max. Anschlussleistung DC (Gesamt) | 500W/1h, 210W/3h, 90W/8h | 500W/1h, 200W/3h, 80W/8h | 1.500W/1h, 500W/3h, 300W/8h | (s. XL-Daten) | 6.324W/1h, 2.598W/3h, 1.194W/8h | 17.000W/1h, 7.380W/3h, 2.970W/8h | 40.000 W | 40.000 W |

\* Ein zusätzlicher Stromkreis ist als Standard immer integriert. \*\* MiniControl XL Gehäuse: 1470×570×230 mm.
- Weitere Merkmalszeilen (für alle zutreffend bzw. optional markiert): Automatische Prüfeinrichtung gemäß **DIN EN 62034**, zusatzleitungslose Einzelleuchtenüberwachung und Schaltbarkeit, frei programmierbare Stromkreise, Vernetzbarkeit mehrerer Systeme (optional), Steuerung/Überwachung per Web-Interface, Gebäudevisualisierung im Web-Interface, Unterstationen/-verteiler möglich.

### Systemauslegung — Batterietypen je Versorgungszeit (Seite 299)
- **Leuchten LED – Stromaufnahme bei 216V DC Betrieb 100%:** LED 1W → Aufnahme 2W; LED 2W → 3W; LED 3W → 4,5W; LED 4W → 5,5W; LED 5W → 6,5W.
- Batterietyp-Zuordnung (OGiV-Serie) nach Leistung/Versorgungszeit (1h/3h/8h), je mit Angabe der Anzahl Lade-/Batteriemodule (LDM):
  - **MyControl (≤4):** 350W/145W/65W → OGiV 1236 LP (1 LDM); 500W/200W/90W → OGiV 1252 LP.
  - **MicroControl (≤6):** 500W/200W/90W → OGiV 1252 LP.
  - **MiniControl (≤12):** 1500W/500W/300W → OGiV 12170 LP; 650W/250W/90W → OGiV 1270 LP; 1260W/500W/190W → OGiV 12120 LP; 1500W/500W/300W → OGiV 12170 LP.
  - **MiniControl XL (≤32):** 1500W/500W/300W → OGiV 12170 LP.
  - **MidiControl (≤32):** 2678W/1227W/531W → OGiV 12260 LP; 2575W/1250W/566W → OGiV 12280 L; 3421W/1411W/635W → OGiV 12330 LP; 4061W/1630W/719W → OGiV 12400 LP; 4579W/1884W/862W → OGiV 12450 LP; 6324W/2598W/1194W → OGiV 12550 LP.
  - **MaxiControl (≤60):** 5858W/2471W/1145W → OGiV 12550 FT; 7914W/3300W/1560W → OGiV 12800 FT; 11180W/4717W/2074W → OGiV 121000 FTP; 17021W/7379W/2972W → OGiV 121500 FTP.
  - **MultiControl (≤96):** 6307W/2540W/1175W → OGiV 12600 LP; 6739W/2661W/1270W → OGiV 12650 LP; 7500W/3421W/1547W → OGiV 12750 LP; 8001W/3577W/1646W → OGiV 12800 LW/LPL; 8381W/3767W/1814W → OGiV 12900 LP; 10489W/4164W/2039W → OGiV 121000 LP; 12563W/5063W/2350W → OGiV 121200 LPS; 13478W/6083W/2730W → OGiV 121340 LP; 15068W/6342W/3041W → OGiV 121500 LP; 23501W/9677W/4147W → OGiV 122000 LP; 24365W/10472W/5028W → OGiV 122600 LP.
- Hinweis: Für Midi-, Maxi- und MultiControl auch **Panzerplattenbatterien OPzV Longlife 20 Jahre** verfügbar (siehe Seite 370).

### MyControl MY — Detail (Seiten 300–303)
- LPS, Dezentralisierung pro Brandabschnitt; gemäß ÖVE E 8002-1:2007 bzw. OVE E 8101 und **OVE R 12-2** Reduzierung von E30-Leitungsanlagen.
- Umschaltbetrieb **230VAC / 216VDC**. Batteriesätze: **18× 12V / 3,6 Ah** → 350W/1h, 145W/3h, 65W/8h (inkl. 25% Alterungsreserve); **18× 12V / 5,2 Ah** → 500W/1h, 210W/3h, 90W/8h.
- **4+1 Stromkreise**, jede Umschaltung unabhängig, separat **zweipolig abgesichert**. 4 interne Lichtschalterabfrage-Eingänge (24V–255V DC bzw. 220/230V AC).
- IO-Modul: 3 potentialfreie Umschaltkontakte; verpolungstoleranter Multispannungseingang (24–255VDC bzw. 200–255VAC). 24V-Lüfter-Anschluss. **CCIF**-Ruhestromschleife (überwacht Phasenwächter/Netzüberwachung auf Kurzschluss/Kabelbruch). Überwachte Busschnittstelle.
- **max. Anschlussleistung 250 W je Stromkreis** (Standardleuchten 230V AC/DC). Integriertes **Prüfbuch bis 30.000 Einträge**, automatische Prüfeinrichtung laut **ÖVE EN 62034:2013-02**.
- Eigenschaften: nach **ÖVE/ÖNORM EN 50171**, Sicherheitsbeleuchtung nach **EN 50172, E 8002-1, OVE E 8101**; Verwaltung/Fehleranzeige **bis 20 Leuchten je Stromkreis**; 4 Hauptstromkreise + 1 Dauer-/Bereitschaftskreis **max. 150VA**; externe Module NLSAM24/NLMCLM/NLMCT15 über **RS485**; je Stromkreis **bis 6 Schalteingänge**; Vernetzung über Ethernet optional.
  - SAM (integriert): 4 Lichtschaltereingänge (24–250 VDC, 220/230 VAC), 3 Schaltungsarten.
  - IO-Modul: 3 Relaisausgänge **230V / 6A** potentialfreie Wechselkontakte; 1 galv. getrennter Schalteingang.
- **Technische Daten:** Montage Wand/Stand; Gehäuse Stahlblech/Aluminiumrahmen; optional Brandschutzgehäuse E30; Gehäuse **900×450×125 mm**, E30-Gehäuse **1228×728×295 mm**; **IP20 / Schutzklasse I**; Netz **230V AC ±10% 50/60Hz**; Umschaltbetrieb 230VAC/216VDC ±15%; Abgangskreise 4+1 mit Umschaltung Dauer/Bereitschaft je Kreis; Batterie OGiV (NLMY3: 18×12V/3,6Ah; NLMY5: 18×12V/5,2Ah); max. Anschlussleistung **AC 800VA**; DC: NLMY3 1h 1,62A/350W, 3h 0,67A/145W, 8h 0,3A/65W; NLMY5 1h 2,31A/500W, 3h 0,97A/200W, 8h 0,42A/90W.
  - Verlustleistung Leerlauf Netzbetrieb: Starkladung 70W, Erhaltungsladung 45W; Batteriebetrieb 20W.
  - **Netzsicherung T6,3A; empfohlene Vorsicherung 16A.** Anschlussquerschnitte: Netzleitungen **1,5–4 mm² starr**, Endstromkreise **1,5–2,5 mm² starr**.
  - Gewicht NLMY3 48kg, NLMY5 50kg (inkl. Batterien); E30-Schrank 115kg. **Umgebungstemp. 10°–35°C**.
- Bestellnummern: **NLMY3** (4 Kreise, max. 80 Leuchten = 20/Kreis, 350W/1h, mit 18× OGiV 12V 3,6Ah); **NLMY5** (4 Kreise, 80 Leuchten, 500W/1h, 18× OGiV 12V 5,2Ah). Zubehör u.a.: NLMCLM (3-Phasen-Netzüberwachung Bus), NLMCT15/NLMCT15S (Meldetableau LCD, mit/ohne Schlüsselschalter), NLPC2300 (3-Phasen PC230), NLSAM08 (8 Eingänge), NLSAM24 (8 Eingänge inkl. Netzwächter), **NLMYE30** (E30-Schrank, 1228×728×295 mm, RAL7035, Schutzart II, IP54, 115kg).

### MicroControl MI — Detail (Seiten 304–307)
- LPS für 1-/3-/8-stündige Betriebsdauer; Umschaltbetrieb 230VAC/216VDC; bis **6 Hauptstromkreise (+1 Standard)**.
- Eigenschaften: nach EN 50171 / EN 50172 / E 8002-1 / OVE E 8101; autom. Prüfeinrichtung **EN 62034**; 19"-Einschub; Prüfbuch **>5 Jahre**; bis 20 Leuchten/Stromkreis; max. 6 Hauptstromkreise als **650VA (DCM32)**-Einschub + 1 Dauer-/Bereitschaftskreis **max. 150VA**; kompatibel zu **NLDCM12E**; **TÜV Rheinland zertifiziert ID: 1111212721**.
  - SAM: **8 Lichtschaltereingänge** (24–250 VDC, 220/230 VAC); 3 Schaltungsarten.
  - IO-Modul: **7 Relaisausgänge 230V / 6A**; 4 galv. getrennte Schalteingänge; interne CAN-Busanbindung.
- **Technische Daten:** Wand/Stand; Stahlblech RAL 7035; Gehäuse **630×350×230 mm**, E30 **918×711×345 mm**; IP20/I; Netz 230V AC ±10%; Abgangskreise max. 6+1; Batterie OGiV **216V DC (18×12V/5,2Ah)**; **AC max. 2000VA**; DC 1h 2,31A/500W, 3h 0,92A/200W, 8h 0,37A/90W.
  - Verlust Netz: Stark 70W / Erhaltung 45W; Batterie 20W. **Netzsicherung 10A; Vorsicherung 20A.** Netz 1,5–4mm², Endkreise 1,5–2,5mm². Gewicht 57kg (E30 70kg). Umgebung 10–35°C.
- **Stromkreismodule:** DCM12E – 4×F5A – 1A / 2×300VA; DCM32 – 4×F5A – 3A / 2×650VA.
- Bestellnummern: NLMI100A (ohne Einschübe, erweiterbar 6 Kreise/120 Leuchten), NLMI102A (2 Kreise/40), NLMI104A (4/80), NLMI106A (6/120). Zubehör u.a. NLDCM12E (2×1A/300VA, 4×F5A), NLDCM32 (2×3A/650VA, 5A), NLPLXMIC (Plexiglasabdeckung), NLMIE30 (E30-Schrank 918×711×345, IP54, 70kg), NLBD04E (externer Drucker), NLLUINT/NLLUINTFM (Ersatzlüfter/Filtermatte E30).

### MiniControl MN — Detail (Seiten 308–311)
- LPS 1-/3-/8h; bis **12 Hauptstromkreise (+1 Standard)**; Umschaltbetrieb 230VAC/216VDC.
- Eigenschaften: max. 12 Hauptstromkreise mit **650VA (DCM32 Standard)** oder **860VA (DCM42 optional)**, + 1 Dauer-/Bereitschaftskreis max. 150VA; bis 20 Leuchten/Kreis; Einzelleuchten-/Stromkreisüberwachung ohne Zusatzleitung; kompatibel NLDCM12E; **TÜV Rheinland ID: 1111212721**.
  - SAM: 8 Lichtschaltereingänge (24–250 VDC, 220/230 VAC), Spannungsversorgung 230V/50Hz, 3 Schaltungsarten. IO: 7 Relaisausgänge 230V/6A; 4 galv. getrennte Schalteingänge; CAN-Bus. CCIF Ruhestromschleife.
- **Technische Daten:** Wand/Stand; Stahlblech RAL 7035; Gehäuse **1100×500×230 mm**, E30 **1388×861×345 mm**; IP20/I; Netz 230V AC ±10%; Abgangskreise max. 12; Batterie OGiV: NLMN102A–112A **18×12V/17Ah**, NLMN102A05 **18×12V/5,2Ah**; **AC max. 2000VA**.
  - DC: NLMN102A–112A 1h 6,94A/1500W, 3h 2,31A/500W, 8h 1,38A/300W; NLMN102A05 1h 2,31A/500W, 3h 0,92A/200W, 8h 0,42A/90W.
  - Verlust Netz: Stark 77W / Erhaltung 52W; Batterie 25W. **Netzsicherung 10A; Vorsicherung 20A.** Netz 1,5–4mm², Endkreise 1,5–2,5mm². Gewicht NLMN102A–112A 136kg, NLMN102A05 73kg (E30 115kg). Umgebung 10–35°C.
- **Stromkreismodule:** DCM12E (4×F5A, 1A/2×300VA), DCM32 (4×F5A, 3A/2×650VA).
- Bestellnummern: NLMN100A (erweiterbar 12 Kreise/240 Leuchten), NLMN100A05 (500W 1h / 200W 3h), NLMN104A (4/80), NLMN106A (6/120), NLMN108A (8/160), NLMN110A (max. 200 Leuchten), NLMN112A (12/240). Zubehör u.a. NLDCM42 (2×4A/860VA, 6,3A), NLPLXMIN, NLMNE30 (E30 1388×861×345, IP54, 115kg).

### MiniControl XL (MN..X) — Detail (Seiten 312–315)
- LPS 1-/3-/8h; bis **32 Hauptstromkreise**; je Brandabschnitt im Betriebsraum; 3 Batterieausstattungen 17Ah/12Ah/7Ah.
- Eigenschaften: max. 32 Hauptstromkreise mit 650VA (DCM32) oder 860VA (DCM42); bis 20 Leuchten/Kreis; kompatibel NLDCM12E; verschließbare Polycarbonatabdeckung optional; **TÜV Rheinland ID: 1111212721**. SAM 8 Eingänge, IO 7 Relaisausgänge 230V/6A + 4 Schalteingänge, CAN, CCIF.
- **Technische Daten:** Wand/Stand; Stahlblech RAL 7035; Gehäuse **1470×571×230 mm**, E30 **1828×908×395 mm**; IP20/I; Netz 230V AC ±10%; max. 32 Kreise; Batterie OGiV: NLMN100X **18×12V/17Ah**, NLMN100X12 **18×12V/12Ah**, NLMN100X07 **18×12V/7Ah**; **AC max. 2000VA**.
  - DC: NLMN100X 1h 6,94A/1500W, 3h 2,31A/500W, 8h 1,38A/300W; NLMN100X12 1h 5,83A/1260W, 3h 2,31A/500W, 8h 0,88A/190W; NLMN100X07 1h 3,01A/650W, 3h 1,16A/250W, 8h 0,42A/90W.
  - Verlust Netz: Stark 91W / Erhaltung 66W; Batterie 40W. **Netzsicherung 16A; Vorsicherung 25A.** Netz **2,5–6mm² starr**, Endkreise 1,5–2,5mm². Gewicht NLMN100X 176kg, X12 143kg, X07 120kg (E30 140kg). Umgebung 10–35°C.
- **Stromkreismodule:** DCM12E (1A/2×300VA), DCM32 (3A/2×650VA).
- Bestellnummern: NLMN100X (1500W/500W/300W, erw. 32 Kreise/640 Leuchten), NLMN100X12 (1300W/500W/230W), NLMN100X07 (700W/300W/130W). Notwendiges Zubehör NLDCM12E/32/42; NLMNXLE30 (E30-Schrank 1828×908×365 mm — Abweichung Außenmaß; RAL7035, Schutzart II, IP54, 220kg).

### MidiControl MD — Detail (CPS, Seiten 316–320)
- Vorkonfiguriertes CPS mit zusatzleitungsloser Einzelleuchtenüberwachung, frei programmierbaren Stromkreisen, **5-Jahres-Prüfbuch**. Wahlweise 1 oder 2 Lader zu 2,5A. Max. mit **55Ah**: 5300W/1h, 2300W/3h, 1000W/8h (Schrack-Info-Text; technische Daten s.u. mit 6324W/1h für 55Ah).
- Bis zu **16 DCM-Module DCM42** für 32 Stromkreise à max. **4A / 864VA**. Alternativ DCM12E (2×1,1A / 2×250VA) mit "EL"-Leuchten für zentrale Einzelschaltbarkeit. Jedes Modul 2 Abgangskreise à bis 20 Leuchten → bis **640 Leuchten**.
- Betriebsarten je Kreis: Dauerlicht, Bereitschaftslicht, geschaltetes Dauerlicht oder **Treppenlicht**.
- Vernetzung: bis 32 Anlagen per TCP/IP → max. **1024 Stromkreise / 20.480 Leuchten**.
- Eigenschaften: nach EN 50171/EN 50172/E 8002-1/OVE E 8101; autom. Prüfeinrichtung EN 62034; mikroprozessorgesteuert; 5-Jahres-Prüfergebnisse; LCD-Klartext, mehrsprachig, passwortgeschützt; USB-Tastatur; **MultiMediaCard** für Updates; Ethernet; adaptive Stromüberwachung + **selektive Isolationsprüfung** der Endstromkreise; bis 32 Endstromkreise/19"-Schrank; **IUTQ-Ladekennlinie**; integrierter Standsockel; abgesicherte Service-Steckdose; **TÜV Rheinland ID: 1111212721**. SAM 8 Eingänge, IO 7 Relaisausgänge 230V/6A + 4 Schalteingänge, CAN, CCIF.
- **Technische Daten:** Montage Stand; Stahlblech RAL 7035; **1950×600×450 mm** inkl. Standsockel; IP20/I; Netz **3×230V AC ±10% 50/60Hz**; Ausgang 230V AC / 216V DC; max. 32 Kreise; Batterie (nicht enthalten) OGiV/OGi/OPzV; **AC max. 8140VA**.
  - DC nach Batterie (1h/3h/8h): 17Ah(LPS) 1500W/500W/185W; 26Ah 2678W/1227W/531W; 33Ah 3421W/1411W/635W; 40Ah 4061W/1630W/719W; 45Ah 4579W/1884W/862W; 55Ah 6324W/2598W/1194W (alle inkl. 25% Alterungsreserve).
  - Verlust Netz: NLMD0100 Stark 90W/Erhaltung 65W; NLMD0200 Stark 140W/Erhaltung 90W. Batterie 40W. **Netzsicherung 20A; Vorsicherung 35A.** Netz **2,5–16mm² starr**, Endkreise 1,5–2,5mm². Gewicht NLMD0100 105kg / NLMD0200 110kg (ohne Batterien).
  - Batteriesatz-Gewichte (216V DC, 18×12V): 17Ah 99kg, 26Ah 166kg, 33Ah 175kg, 40Ah 248kg, 45Ah 263kg, 55Ah 310kg. Umgebung 10–35°C.
- **Stromkreismodule:** DCM12E (4×F5A, 1A/2×300VA), DCM32 (4×F5A, 3A/2×650VA), DCM42 (4×F6,3A, 4A/2×860VA).
- Bestellnummern: NLMD0100 (Lader 2,5A, max. 32 Stromkreise, ohne Einschübe/Batterien), NLMD0200 (Lader 5A). Batteriesätze 216V (18 Stk. Longlife OGiV, C20): NLBAS017 (17Ah), NLBAS026 (26Ah), NLBAS028 (30Ah), NLBAS033 (34Ah), NLBAS040 (42Ah), NLBAS045 (47Ah), NLBAS055 (61Ah). Zubehör u.a. NLPLXMD, NLMCLM, NLPC2300, NLMCT15/S, NLSAM24/24M/08, NLMCBD04 (Einbaudrucker Midi/Maxi/Multi), NLMCMODBUS (GLT Modbus Gateway), NLMCXML (XML-Datenschnittstelle), NLWES852 (5-Port Switch 10/100), NLWES882 (8-Port Switch), NLBTLMD184 (Einzelblockbatterieüberwachung Bat-Logg® für 18 Batterien 17–55Ah), NLBTLSENS4 (Ersatzsensor Bat-Logg®).
