# Planung von Elektroanlagen — Teil 16
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 641-669.

Dieser Teil enthält den Abschluss des Industrieanlage-Projektierungsbeispiels (Kapitel 28) mit vollständigen Berechnungen für Betriebsstrom, Querschnittsermittlung, Kurzschlussstrom, Innenraumbeleuchtung, Blitzschutz, Kompensation, Transformatorstation und Notstromanlage — gefolgt vom Stichwortverzeichnis des Gesamtwerks.

## Inhalt

### 28.4 Berechnungen — Zuleitung Industrieanlage

#### Betriebsstrom und Querschnittsberechnung

Ausgangsgröße für die Zuleitungsberechnung ist eine zugeführte Leistung von 154,85 kW bei einem Gleichzeitigkeitsfaktor 0,65, woraus sich eine zugeführte Leistung von 100,5 kW ergibt.

Betriebsstromberechnung (Drehstrom):
- Formel: IB = P / (√3 × 400 V × cosφ)
- Eingesetzte Werte: P = 100,5 kW, cosφ = 0,88
- Ergebnis: IB = 164,9 A

Querschnittsberechnung nach Spannungsfall:
- Formel: S = (√3 × IB × l × cosφ) / (κ × ΔU)
- Leitungslänge: 150 m, Bemessungsstrom: 200 A, cosφ = 0,88
- Spezifische Leitfähigkeit Kupfer: 56 m/(Ω·mm²)
- Zulässiger Spannungsfall: 4 V
- Rechnerischer Querschnitt: 204 mm²
- Gewählter Querschnitt: 240 mm²

Überlastschutznachweis (Bedingung IB ≤ In ≤ Iz):
- 165 A ≤ 200 A ≤ 234 A — erfüllt

Tatsächlicher Spannungsfall bei gewähltem Querschnitt:
- u = (√3 × 200 A × 150 m × 0,88) / (56 × 400 V × 240 mm²) = 0,86 %

#### Kurzschlussberechnung — Abschaltnachweis (einpoliger Kurzschluss)

Leitungswiderstände der 240-mm²-Zuleitung (150 m):
- Resistanz Leiter: Rl = 1,24 × (150 / (56 × 240)) = 13,84 mΩ
- Resistanz Schutzleiter RPE: 13,84 mΩ (gleicher Querschnitt)
- Reaktanz: Xl = 2 × 0,08 mΩ/m × 150 m = 24 mΩ
- Kurzschlussimpedanz Leitung: Zk = √(Rl² + Xl²) = 36,63 mΩ

Gesamtimpedanz (Vorimpedanz ZV = 75 mΩ vorausgesetzt):
- ZG = ZV + Zk = 75 mΩ + 36,63 mΩ = 111,63 mΩ

Minimaler einpoliger Kurzschlussstrom:
- I''k1min = (c × Un) / (√3 × ZG) = (0,9 × 400 V) / (√3 × 111,63 mΩ) = 1,86 kA

Abschaltzeitnachweis bei 200-A-NH-Sicherung:
- Auslösezeit der Sicherung bei minimalem Kurzschlussstrom: 1 s
- Zulässige Abschaltzeit: tzul = (k × S / I''k1)² = (115 A·s^0,5/mm² × 240 mm² / 2200 A)² = 157,3 s
- Bedingung erfüllt

#### Kurzschlussberechnung — dreipoliger Kurzschluss

Impedanzrechnung für dreipoligen Kurzschluss (240 mm², 150 m):
- Rl = 150 / (56 × 240) = 0,011 Ω = 11 mΩ
- Xl = 0,08 mΩ/m × 150 m = 12 mΩ
- Zk = √(Rl² + Xl²) = 12 mΩ (vereinfacht, da Xl dominiert)

Anfangs-Kurzschlusswechselstrom (dreipolig):
- I''k3 = (c × Un) / (√3 × Zk) = (1,1 × 400 V) / (√3 × 12 mΩ) = 21,17 kA

Stoßkurzschlussstrom:
- ip = κ × √2 × I''k3 = 1,8 × √2 × 21,17 kA = 53,90 kA

Mechanische Kraft auf die Sammelschiene:
- F = 0,2 × ip² × (l / a) = 0,2 × 53,90² kA² × (2000 cm / 20 cm) = 58.104,2 N

### 28.5 Berechnung der Innenraumbeleuchtung (nach DIN 5035)

#### Raum- und Anforderungsdaten

Raumparameter (Tab. 28.2):
- Raumart: Werkstatt
- Länge: 12 m, Breite: 7 m, Fläche: 84 m²
- Raumhöhe: 3,0 m
- Bewertungsebene über Boden: 0,85 m
- Pendellänge/Abhängung: – (direkte Montage)
- Lichtpunkthöhe: h = H – l – e = 3,0 – 0 – 0,85 = 2,15 m
- Raumindex: k = (a × b) / (h × (a + b)) = (12 × 7) / (2,15 × 19) = 2,05
- Reflexionsgrade Decke/Wände/Boden: 0,5 / 0,3 / 0,1 (bzw. Tabelle 0,5/0,3/0,3)

Beleuchtungsanforderungen nach ASR /3 bzw. DIN 5035 (Tab. 28.3):
- Nennbeleuchtungsstärke En: 300 lx
- Lichtfarbe: nw (neutralweiß)
- Farbwiedergabestufe: 1
- Güteklasse Blendungsbegrenzung: –
- Verminderungsfaktor v: 0,7
- Gleichmäßigkeit g1 = Emin/E: 1:1,5

#### Leuchtendaten (Tab. 28.4)

- Beleuchtungswirkungsgrad ηB: 66 %
- Multiplikator für ηB: M = 1
- Anzahl Lampen je Leuchte: z = 1

#### Lampendaten (Tab. 28.5)

- Lampenleistung ohne Vorschaltgerät: 58 W
- Lampenleistung mit Vorschaltgerät: 66 W
- Lichtfarbe: nw
- Farbwiedergabestufe: 3
- Lichtstrom je Lampe Φ: 5.200 lm

#### Beleuchtungstechnische Ergebnisse (Tab. 28.6)

Erforderliche Leuchtenanzahl:
- n = (En × A × 100 %) / (z × Φ × ηB × M × v)
- n = (300 lx × 84 m² × 100 %) / (1 × 5200 lm × 66 % × 1 × 0,7)
- n = 11 Stück (Mindestanzahl)

Mittlere Beleuchtungsstärke bei gewählter Anzahl N = 15 Leuchten:
- E = (N × z × Φ × ηB × M × v) / (A × 100 %)
- E = (15 × 1 × 5200 lm × 66 % × 0,7) / (84 m² × 100 %) = 490 lx

Leuchtenanordnung:
- Leuchtenabstände quer × längs: 5 m × 3,2 m (gewählt/gegeben)
- Gleichmäßigkeit nach Datenblock: Emin/E ≤ 1:1,5

Anschlussleistung gesamt:
- P = N × z × p = 15 × 1 × 66 W = 792 W (mit Vorschaltgerät)

### 28.5.1 Berechnung der Blitzschutzanlage

Ausbreitungswiderstand des Ringerders:
- Spezifischer Erdungswiderstand: ρE = 300 Ω·m
- Gesamtlänge Ringerder: L = 275 m
- Ringerder-Tiefe: D = L/π = 275/π ≈ 87,5 m
- Formel: RA = ρE / (2π × D) × ln(2πD / d)
  - d = 0,01 m (Erderdurchmesser)
  - RA = (300 Ω·m) / (2π × 87,5 m) × ln(87,5 m / 0,01 m)
  - RA = 3,79 Ω

### 28.5.2 Berechnung der Kompensationsanlage

Ziel: Leistungsfaktor von cosφ = 0,88 auf cosφ = 0,95 verbessern.

Benötigte Blindleistung:
- QC = Pmax × (tan φist – tan φsoll)
- QC = 155 kW × (0,5397 – 0,3286) = 32,7 kvar

Benötigte Kondensatorkapazität:
- C = QC / (3 × U² × ω)
- C = 32,7 kvar / (3 × (400 V)² × 314) = 217 µF

### 28.5.3 Planung der Transformatorstation

Grunddaten der Station:
- Versorgungsspannung: 10 kV / 0,4 kV, 50 Hz
- Art: Kleinstation
- Transformator-Nennleistung: 630 kVA
- Anzahl Abgänge: 5
- Abmessungen Gehäuse: 2570 mm (B) × 2100 mm (L) × 2100 mm (H), ca. 1650 mm über Erdniveau

Angewandte Normen und Bestimmungen:
- DIN VDE 0101, DIN VDE 0670 Teil 3, Teil 6, DIN VDE 0670 Teil 500
- PEHLA-Richtlinie Nr. 2
- IEC 265, IEC 298, IEC 694
- TAB (Technische Anschlussbedingungen)

Schutzart nach DIN 40050 / IEC 529:
- Berührungsschutz, Wasser- und Fremdkörperschutz, Schutz vor atmosphärischen Einwirkungen

#### Mittelspannungsteil (Bestückung)

- 1 Stück Lasttrennschalter-Festbauanlage bis 24 kV, isoliert, 1 Transformatorabzweig mit HH-Sicherungen, sammelschienenseitig getrennt, abgangsseitig geerdet
- 1 Stück Drehstrom-Gießharztransformator, verlustarm R10
- 1 Stück Kaltleiter-Temperaturfühler
- 1 Stück Anschlussmöglichkeiten in der Transformatorkammer
- 3 Stück steckbare Spannungsanzeige für 10 kV
- 1 Stück NS-seitiges Verbindungskabel

#### Niederspannungsteil (Bestückung)

- 1 Einschubleistungsschalter, dreipolig, Bemessungsstrom 1000 A, Bemessungsausschaltvermögen 75 kA
- 1 Einschubrahmen für Leistungsschalter bis 1250 A
- 5 NH-Sicherungslasttrennschalter, dreipolig, 125 A
- 5 Sicherungsunterteile, einpolig
- 1 Kupfertrennlaschen, 1000 A
- 1 Aufsteckgriff für Kupfertrennlaschen, Größe 4
- 15 Sicherungseinsätze, Gr-00, 25 A bis 125 A
- 24 Hilfsschütze
- 3 LS-Schalter, 1-polig, 16 A
- 3 LS-Schalter, zweipolig, 16 A
- 3 LS-Schalter, dreipolig, 16 A
- 6 Sicherungssockel, einpolig
- 3 Stromwandler, Reihe 0,5, Nennstrom 1000/5 A, Klasse 1, 15 VA
- 6 Stromwandler, Reihe 0,5, Nennstrom 250/5 A, Klasse 1, 15 VA
- 9 Stromwandler, Reihe 0,5, Nennstrom 160/5 A, Klasse 1, 15 VA
- 3 Strommesser
- 1 Spannungsmesser
- 6 elektronische Energiezähler
- 2 Schalterstellungsanzeiger
- 2 Schwenktaster EIN-AUS
- 6 Koppelrelais
- 6 Zeitrelais
- 1 Installationsverteiler
- 1 Stromschienensystem, fünfpolig, 1000 A (L1, L2, L3, N, PE), aus Flachkupfer, kurzschlussfest
- 1 Zentraler Erdungspunkt, Flachkupfer, 30 × 5 mm
- 1 betriebsfertige Verdrahtung inkl. Befestigungselemente, Klein- und Montagezubehör

#### Abnahmedokumentation Transformatorstation (Pflichtunterlagen)

Bei Inbetriebnahme und Abnahme sind folgende Unterlagen zu liefern:
- Blockschaltbild
- Übersichtsschaltplan
- Stromlaufplan
- Gerätestückliste
- Klemmenplan
- Geräteaufbauzeichnung
- Kabelplan
- Kabeltrassenplan
- Installationsplan
- Werkprüfprotokoll
- Berechnungen
- Messungen
- Betriebsanleitungen
- Funktionsbeschreibungen

### 28.5.4 Planung der Notstromanlage

#### Allgemeine Anforderungen und Leistungsumfang

Planungsumfang umfasst:
1. Liefern und Anschließen des Generators
2. Installation der Betriebserdung
3. Installation der Energie- und Steuerleitungen zur NSHV
4. Installation der Schalt- und Steuereinrichtungen
5. Installation des Aggregatzubehörs
6. Ausführung von Betonarbeiten
7. Installation des Treibstofftanks
8. Installation der Startbatterien
9. Installation der Abgasschalldämpfer
10. Installation des Zubehörs für Motor-Generatorüberwachung
11. Ausführung von Erdarbeiten
12. Inbetriebnahme und Funktionsprüfung

Versorgungsspannung: 230/400 V, 50 Hz

Schutzmaßnahmen:
- Schutz durch Abschaltung oder Meldung im TN-System mit Hauptpotentialausgleich
- Schutzisolierung

#### Technische Daten des Notstromaggregats

Notstromaggregat nach DIN 6280, Ausführungsklasse 2 und DIN VDE 0108:
- Bemessungsleistung: 100 kVA
- Leistungsfaktor cosφ: 0,8
- Bemessungsspannung: 400/230 V
- Bemessungsfrequenz: 50 Hz

Dieselmotor nach DIN 6271:
- Dauerleistung: 88 kW (10 % überlastbar)
- Nenndrehzahl: 1500 U/min
- Kraftstoffverbrauch: Angabe bei 4/4 Last
- Anlassvorrichtung: Elektrostart

Generator nach DIN VDE 0530:
- Bemessungsleistung: 100 kVA
- Leistungsfaktor cosφ: 0,8
- Bemessungsspannung: 400/230 V
- Bauart: selbsterregte und selbstregelnde Innenpolsynchronmaschine, bürstenlos, mit umlaufenden Dioden
- Erregergenerator als Außenpolmaschine mit elektronischem Spannungsregler
- Dämpferkäfig vorhanden
- Kupferwicklung, feuchtigkeits- und tropenfest imprägniert

Starterbatterie:
- Typ: Panzerplattenbatterie nach VDE 0108
- Spannung: 24 V
- Kapazität: 72 Ah
- Ausführung im Kunststoffträger mit Dämm- und Befestigungsplatten

Notstromsteuerungsschrank:
- Norm: DIN VDE 0108
- Gehäuse: Standschaltschrank, Stahlblechkonstruktion, grundiert, lackiert RAL 7032
- Schutzart: IP 43
- Ausführung: Montageplatte, Installationskanäle, Verdrahtung mit Schaltlitze, Kabeleinführung von unten

#### Automatische Netzüberwachung (Microcontroller-basiert)

Integrierte Überwachungs- und Steuerfunktionen:
- Sensorkreise für Drehzahlerfassung
- Messung der Netz-/Generatorfrequenz
- Messung der Netz-/Generatorspannung in allen drei Leitern
- Überwachung der Phasenfolge beider Spannungssysteme
- Quarzgesteuertes Frequenznormal für 50 Hz
- Zusätzliche Schnittstelle für Lichtwellenleiteranschluss
- Anschluss von Leittechnikgeräten für Daten- und Befehlsaustausch
- Erhöhter Einstellkomfort über PC-Schnittstelle

Anwählbare Betriebsarten (je mit Leuchtmelder):
- Aus (Entsperren)
- Hand
- Automatik
- Probe
- Start
- Lampentest
- Alarm Aus

#### Bestückung Notstromsteuerung nach DIN VDE 0108

- 1 Netzschalter, vierpolig, motorbetätigter Leistungsschalter mit Arbeitsstromauslöser
- 1 Generatorschalter, vierpolig, motorbetätigter Leistungsschalter mit Arbeitsstromauslöser
- 1 Überlastungsschutz mit thermisch verzögertem Bimetallauslöser
- 1 Kurzschlussstromüberwachung mit einstellbarer Verzögerung
- 1 Elektronisches Ladegerät für Blei- bzw. NC-Starterbatterie mit IU-Kennlinie und automatischer Umschaltung auf Ausgleichsladung mit Batteriespannungswächter
- 1 Elektrischer Warngeber mit automatischer Abstellung
- 1 NOT-AUS-Druckschalter mit Schlüsselentriegelung
- 1 Potentiometer für Spannungsstellbereich
- 1 Steuerung für motorbetätigte Jalousien
- 1 Spannungsmesser 0–500 V
- 3 Spannungsmesserumschalter siebenstufig
- 1 Bimetallstrommesser mit Schleppzeiger
- 1 Zeigerfrequenzmesser 45–55 Hz
- 1 Wirkleistungsmesser für unsymmetrische Belastung
- 1 Betriebsstundenzähler
- 1 Öldruckmesser
- 1 Kühlwasser- bzw. Zylinderkopftemperaturmesser
- 1 Batteriespannungsmesser
- 1 Batterieladestrommesser

#### Verkabelung im Aggregateraum

Kabelarten zwischen Notstromschaltschrank und Dieselaggregat sowie zu sonstigen Verbrauchern:
- Generatorkabel
- Steuerkabel
- Batteriekabel
- Zu- und Abluftjalousien
- Kraftstoffpumpen
- Kühleinrichtung
- Steuereinrichtung
- Störmeldekabel

#### Kraftstoffversorgung

- Tank: 600-Liter-Kraftstoff-Stahlwandtank, einwandig, mit Konsolen, Flüssigkeitssichtrohr, absperrbar
- Stahlabwanne als Auffangbehälter
- Kraftstoffleitungssystem: zwischen Tank und Dieselmotor innerhalb des Aggregateraums, vorschriftsgemäß
- Beschilderung und Beschriftungen für Tankanlagen und Aggregateraum, vorschriftsgemäß
- Tauchsonde für Kraftstoffmangelanzeige
- Handflügelpumpe mit 3 m Kunststoffschlauch

#### Zu- und Abluftanlage

Zuluftseite:
- Wetterschutz- und Vogelschutzgitter
- Zuluftjalousie mit Motorbetätigung
- Zuluftschalldämpfer: abgestimmt auf Luftmenge und Frequenzspektrum, Dämpfung bei 1000 Hz: 37 dB

Abluftseite:
- Wetterschutz- und Vogelschutzgitter
- Abluftjalousie mit Motorbetätigung
- Abluftschalldämpfer: Dämpfung der Geräusche nach außen, bei 1000 Hz: 37 dB, Querschnitt nach erforderlicher Luftmenge

Abgasanlage:
- Abgas-Hochleistungsschalldämpfer mittlerer Dämpfung: 40 dB, NW 100
- Abgasleitung aus DIN-Edelstahlrohr, Werkstoffnummer 1.4571 (V4A), Abmessung 114,3 × 2 mm, mit Kompensatoren und Entwässerungseinrichtung

#### Zubehör für Wartung und Prüfung der Starterbatterie

Wartungszubehör (Lieferumfang):
- 1 Heber
- 1 Messglasröhrchen
- 1 Messglas
- 1 Fülltrichter
- 1 Thermometer
- 1 Voltmeter 0–30 V
- 1 Polmutterschlüssel
- 1 Nachfüllgefäß
- 1 Wartungsanleitung für die Batterie

Werkzeugsatz für Wartung und kleine Reparaturen:
- Schlüssel (DIN 895): 6×8, 10×12, 13×14, 17×19, 22×24 mm
- 1 Schraubendreher
- 1 Kombizange

#### Sonstige Anforderungen

Schallschutz-Ausrüstung: Ohrschützer, Dämmwert mindestens 20 dB, mit Kopfbügel und Wandhalter.

Notleuchte im Aggregateraum:
- Batterie: Nickel-Cadmium, Entladedauer 3 Stunden
- Ausführung: gasdichte Zellen, vollautomatische Aufladung
- Zwei Glühlampen umschaltbar: 5 W oder 1,5 W

Handfeuerlöscher:
- Geeignet für alle Brandklassen
- Füllmenge: 6 kg
- Mit Befestigungskonsole

#### Lastprobelauf und Abnahme

Probelaufprogramm (mit Widerständen des Auftragnehmers):
- 70 % Last, Dauer: 2,5 Stunden
- 100 % Last, Dauer: 1,0 Stunde
- 110 % Last, Dauer: 0,5 Stunden
- Protokollierung aller Werte

Inbetriebnahme und Funktionsprüfung nach DIN VDE 0100, Teil 600.

#### Gebäudeeinführungskabel (gas- und wasserdichte Wanddurchführung)

- 1 NYCWY 3 × 120 SM/70
- 1 NYY 5 × 4 mm²
- 1 NYY 24 × 2,5 mm²
- 1 Bandstahl 30 × 3,5 mm²

Potentialausgleichschiene nach VDE 0618 Teil 1:
- Material: Klemmschienen 10 × 10 mm aus Messing, vernickelt
- Reihenklemmen aus Stahl, galvanisch verzinkt
- Abdeckhauben: 217 × 63 × 66,5 mm, schlagfestes Polystyrol grau RAL 7035
- Anschlussmöglichkeiten:
  - 7 Leitungen 2,5–25 mm²
  - 2 Leitungen 25–95 mm²
  - 1 Flachbandleitung max. 30 × 4 mm
- Anschluss an bauseitigen Fundamenterder inklusive

### Stichwortverzeichnis (Auszug wichtiger Begriffe mit Seitenreferenzen)

Das Gesamtwerk enthält ein umfassendes Stichwortverzeichnis. Nachfolgend die fachlich relevanten Einträge für Elektroplanung:

#### A–D
- Ableiter (Überspannungsableiter): 277; Ableiterauswahl: 371; Ableitvermögen: 277
- Abschaltbedingung: 336; IT-System: 342; TN-System: 336; TT-System: 340
- Abschaltzeit: 337
- AMZ (abhängiges Maximalstrom-Zeitrelais): 393; AMZ-Schutz: 434
- Anfangs-Kurzschlusswechselstrom: 41; Ausschaltwechselstrom: 41, 81
- Anlaufverfahren: 515; Asynchronmotor: 67, 511, 512
- Ausbreitungswiderstand: 239; von Ringerdern: 285
- Back-up-Schutz: 419; Banderder: 254
- Belastbarkeit bei Kurzschluss: 188; im ungestörten Betrieb: 209
- Berührungsspannung: 163, 239; Betriebserder: 260
- Biomasse: 601; Blei-Säure-Batterie: 602; Blindleistung: 230
- Blitzschutzanlage: 277; Blitzschutzklasse: 279; Blitzschutzsystem: 277
- Brennstoffzellen: 601
- Dauerkurzschlussstrom: 41, 83; Differentialschutz: 395, 442
- Distanzschutz: 395, 443; Doppelsammelschiene: 389

#### E–H
- EC-Motor: 545; Eigenerzeugeranlage: 331; Einfachsammelschiene: 389
- Einpoliger Erdkurzschluss: 76; Erder: 239, 253, 255, 283, 285
- Erderarten: 252, 255, 283; Erdfehlerstrom: 239; Erdkapazität: 249
- Erdkurzschlussstrom: 239; Erdschlusskompensation: 257
- Erdschlussreststrom: 239; Erdschlussschutz: 450, 457
- Erdung: 239, 363, 568; Erdungsanlage: 239, 282; Erdungsspannung: 239
- Erdungsstrom: 239; Erdungswiderstand: 340
- Fangeinrichtung: 279; Fehlerstromschutzschalter: 404
- Frequenzumrichter: 517; Fundamenterder: 253, 255, 285
- Gasisolierte Schaltanlage: 356; Generatorschutz: 457
- Gleichzeitigkeitsfaktor: 313; HH-Sicherung: 361, 396
- Hochspannungsanlage: 383; HOAI: 303

#### I–N
- Industrieanlage: 613; Innenraum-Schaltfelder: 364
- Inselbetrieb: 575; Isolationskoordination: 368; IT-System: 342
- Kabelliste: 306; Kippmoment: 514; Kompensation: 230
- Kurzschluss: 74, 207; Kurzschlussarten: 43; Kurzschlussfestigkeit: 87, 398
- Kurzschlussimpedanz: 48; Kurzschlussleistung: 365; Kurzschlussstrom: 41
- Lastflussrechnung: 123; Lastschalter: 360, 396; Lasttrennschalter: 360
- Lasttrennschalteranlage: 366; Leitungsschutzschalter: 398
- Lithium-Ionen-Batterie: 602; Löschspule: 258
- Magnetischer Auslöser: 398; Maschenerder: 254; Medizingerätesicherheit: 303
- Mittelspannungsanlage: 351; Motorschutz: 407, 456; Motorschutzschalter: 407
- Nennstromregel: 205; Netzanbindung: 568; Netzanschlussregeln: 607
- Netzplanung: 364; Netzrückwirkungen: 331; Netzschutz: 429
- Niederspannungsanlage: 293; Notstromanlage: 630

#### O–S
- Oberflächenerder: 253, 284; Ölarme Schalter: 360
- Photovoltaik: 574; Potentialausgleichsleiter: 227; Projektierung: 426
- Pumpspeicherkraftwerke: 556
- Ringerder: 285; Rotor: 567
- Sammelschiene: 389, 383; Sammelschienenschutz: 455
- Schaltanlage gasisoliert: 386; luftisoliert: 383
- Schmelzsicherung: 403; Schrittspannung: 239
- Schutz durch Abschaltung: 333; gegen elektrischen Schlag: 333
- Schutzleiter: 225, 227; Schutzmaßnahmen: 331; Schutzrelais: 431
- Selektivität: 331, 413; Sternpunktbehandlung: 57, 365
- Sternpunkterdung: 247; isolierte: 249; kompensierte: 250; niederohmige: 251
- Stoßkurzschlussstrom: 41, 79; Strombelastbarkeit: 205
- Synchrongenerator: 50, 523; Synchronisation: 528

#### T–Z
- TAB (Technische Anschlussbedingungen): 331
- Thermische Kurzschlussfestigkeit: 214; thermischer Überlastschutz: 441
- Tiefenerder: 254, 284; TN-System: 335; Transformator: 56, 363, 478
- Transformatorschutz: 452; TT-System: 339
- Überlastauslöser: 398; Übersichtsschaltplan: 305, 307
- Überspannungsableiter: 361; Überspannungsschutz: 288
- UMZ (unabhängiges Maximalstrom-Zeitrelais): 394; UMZ-Schutz: 432
- Vakuumschalter: 360; Vakuumschütze: 360
- VDE-Beiblätter: 301; VDE-Leitlinien: 301; VDE-Vornormen: 301
- Wasserkraft: 553; Wechselrichter: 586; Windkraft: 558
- ZEP (zentraler Erdungspunkt): 347; zweipoliger Kurzschluss: 74
