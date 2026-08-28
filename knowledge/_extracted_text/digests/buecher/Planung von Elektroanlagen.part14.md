# Planung von Elektroanlagen — Teil 14
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 561-600.

Dieser Teil behandelt den Abschluss des Kapitels zu elektrischen Maschinen (Gleichstrommotoren, EC-Motoren, elektrische Antriebe) sowie ein vollständiges Kapitel über regenerative Energiesysteme (Wasserkraft, Windkraft, Photovoltaik-Grundlagen). Die Inhalte sind geprägt von Berechnungsbeispielen und Systemauslegungen für Kraftwerkstechnik und netzgekoppelte Erzeugungsanlagen.

## Inhalt

### Gleichstrommaschinen — Motortypen und Berechnungen

#### Nebenschlussmotor (Abschnitt 25.8)
Charakteristika des GS-Nebenschlussmotors:
- Drehzahlabfall unter Last ist gering
- Drehzahleinstellung möglich über Thyristorschaltungen oder Feldsteller
- Läuft im Leerlauf nicht durch (sicherer Betrieb)
- Erregerwicklung darf während des Betriebs nicht abgeschaltet werden — sonst entstehen unzulässig hohe Drehzahlen und Durchgehen des Motors

**Rechenbeispiel GS-Nebenschlussmotor (Abschnitt 25.8.3):**
Gegebene Motordaten: Nennstrom In = 10 A, Ankerwiderstand RA = 0,8 Ω, Erregerwiderstand RE = 900 Ω, Netzspannung U = 230 V, Bürstenspannung UB = 2 V, mechanische Verluste 60 % der elektrischen Verluste.

Berechnungsschritte:
- Erregerstrom: IE = U / RE = 230 V / 900 Ω = 244,4 mA
- Ankerstrom: IA = IN − IE = 10 A − 0,2444 A = 9,75 A
- Zugeführte Leistung: Pzu = U · In = 230 V · 10 A = 2,3 kW
- Elektrische Verluste (Bürsten + Anker + Erreger): Pvelk = UB · IA + IA² · RA + IE² · RE = 315,51 W
- Mechanische Verluste: Pvmech = 60 % · Pvelk = 126,2 W
- Abgegebene Leistung: Pab = Pzu − Pvelk − Pvmech = 1858,3 W

#### Reihenschlussmotor (Abschnitt 25.8.4)
Erregerwicklung liegt in Reihe zur Ankerwicklung; Erregerstrom IE = Ankerstrom IA. Universalmotoren im Haushaltsbereich basieren auf diesem Prinzip.

Formeln:
- Gegeninduktionsspannung: Ui = U − UB − IA · (RA + RE)
- Vorwiderstand: Rv = (U − UB) / IA − RA − RE
- Anlaufstrom: IA = 1,5 · IN

Eigenschaften:
- Drehzahl ist stark lastabhängig
- Läuft im Leerlauf durch (gefährlich)
- Großes Anlaufmoment (Einsatz in Elektrofahrzeugen)
- Drehzahl-Lastmoment-Verhältnis ist umgekehrt proportional

**Rechenbeispiel Reihenschlussmotor (Abschnitt 25.8.5):**
Gegebene Daten: U = 230 V, Pab = 1,8 kW, η = 0,82, Anlaufstrom = 1,5 · IN, RA = 0,75 Ω, RE = 1,5 Ω, UB = 3 V.

- Zugeführte Leistung: Pzu = 1,8 kW / 0,82 = 2,19 kW
- Nennstrom: IN = Pzu / U = 2,19 kW / 230 V = 9,52 A
- Anlaufstrom: IA = 1,5 · 9,52 A = 14,28 A
- Vorwiderstand: Rv = (230 V − 3 V) / 14,28 A − 0,75 Ω − 1,5 Ω = 13,71 Ω
- Innenspannung: Ui = 230 V − 3 V − 14,28 · (0,75 + 1,5) Ω = 195,87 V

#### Doppelschlussmotor (Abschnitt 25.8.6)
Kombination aus Neben- und Reihenschlusserregung. Vereint das konstante Drehmoment des Nebenschlussmotors mit dem hohen Anzugsmoment des Reihenschlussmotors. Erregerfeld besteht aus einem lastunabhängigen und einem lastabhängigen Anteil. Typische Anwendungen: Stanzen- und Pressmaschinen. Drehmoment liegt zwischen Reihen- und Nebenschlussmotor.

**Rechenbeispiel Doppelschlussmotor (Abschnitt 25.8.7):**
Daten: 230-V-Netz, RSeriel = 0,5 Ω, RW = 0,4 Ω, RParallel = 350 Ω, Ra = 1,2 Ω, UB = 2 V, Gegenspannung UG = 180 V.

- Gesamtinnenreihenwiderstand: Ri = RA + RSeriel + RW = 1,2 + 0,5 + 0,4 = 2,1 Ω
- Nebenschlussstrom: IP = U / RParallel = 230 V / 420 Ω (unter Einbezug RW) = 0,54 A
- Anlaufstrom IA (Leerlauf): IA = (U − UB) / Ri + IP = (230 − 2) / 2,1 + 0,54 = 109,11 A
- Ankerstrom Nennbetrieb: IA = (U − UG − UB) / Ri = (230 − 190 − 2) / 2,1 = 18 A
- Gesamtstrom: I = IA + IP = 18 + 0,54 = 18,54 A
- Abgegebene Leistung (nach Abzug aller Verluste inkl. Reibung 75 W): Pab = 3,668 kW
- Wirkungsgrad: η = Pab / Pzu = 3,668 / 4,255 = 86,2 %

#### Fremderregter Motor (Abschnitt 25.8.8)
Anker und Feldwicklung werden aus zwei getrennten Netzquellen gespeist. Feldspannung kann unabhängig von der Ankerspannung eingestellt werden.

Eigenschaften:
- Zum Anlassen und Drehzahlreduzierung: Ankerspannung absenken
- Zur Drehzahlerhöhung: Erregerspannung verringern
- Drehzahlstabilität bei Lastschwankungen
- Bei niedrigen Drehzahlen: Fremdkühlung erforderlich
- Anwendungen: Seilbahnen, Werkzeugmaschinen, Krane

**Rechenbeispiel Arbeitsmaschine mit Riemenantrieb (Abschnitt 25.8.9):**
Riemenscheibendurchmesser: 300 mm, Riemenzugkraft: 250 N, Motordrehzahl: 800 min⁻¹.
- Drehmoment: M = F · d/2 = 250 N · 150 mm = 37,5 Nm
- Leistung: P = M · n / 9550 = 37,5 Nm · 600 / 9550 = 2,35 kW

### EC-Motoren (Abschnitt 25.9)

EC-Motor (Electronically Commutated) ist ein bürstenloser Gleichstrommotor mit Permanentmagnet und elektronischer Kommutierung über Transistoren. Anschluss direkt am Wechselstromnetz; integrierte Elektronik erzeugt das Drehfeld. Polverhältnis: p = f · 60 / n.

Vorteile gegenüber konventionellen Motoren:
1. Hohes Energieeinsparungspotential durch minimale Verlustleistung und höchsten Wirkungsgrad
2. Integrierte Motorelektronik mit Drehzahlstellung, Regelung, Überwachung und Vernetzung; kein externer Frequenzumrichter oder Transformator erforderlich; EMV- und Netzfilter integriert; geringer Verdrahtungsaufwand
3. Wartungsfreier und langlebiger Betrieb durch Einsatz von Power-Modulen mit weniger Bauteilen
4. Sehr geringe Geräuschentwicklung, besonders im Teillastbetrieb

### Elektrische Antriebe (Abschnitt 25.10)

Elektromotor als Energiewandler: Elektrische Energie → mechanische Energie an der Welle der Arbeitsmaschine.

Leistungsformel:
- P = M · 2π · n (in W bei Nm und 1/s)
- Vereinfacht: P [kW] = M [Nm] · n [1/min] / 9,55 (bzw. 9550 für kW direkt)

Auswahlkriterien für Motoren:
1. Stromart, Netzspannung, Frequenz
2. Bemessungsleistung, Bemessungsdrehzahl, Bemessungsdrehmoment
3. Betriebsverhalten, Betriebsart, Schutzart
4. Anlaufverfahren und Anforderungen der Arbeitsmaschine

Antriebsarten:
1. Feste oder umschaltbare Drehzahl ohne Stromrichter — direktes Netzschalten über Schaltgeräte
2. Regelbare Antriebe: a) Gleichstromantriebe b) Drehfeldantriebe
3. Prozesskoordinierte Antriebssysteme

---

### Kapitel 26: Regenerative Energiesysteme

#### Überblick Energieversorgung und erneuerbare Energien (Seiten 570–574)

Strommix-Entwicklung Deutschland:
- Anteil erneuerbarer Energien 2017 an Bruttostromerzeugung: 36,2 %
- PV-Erzeugung 2017: 39,9 TWh (+4,7 % gegenüber 2016), Anteil an erneuerbarer Produktion: 18,3 %
- PV-Zubau 2017: 1678 MW (2016: 1492 MW); Rekordjahr 2012: 8161 MW
- Installierte PV-Leistung Deutschland: über 43,41 GW
- Installierte Windkraftleistung Deutschland: ca. 51,51 GW
- PV + Wind zusammen: fast 90 GW = über 60 % der installierten deutschen Kraftwerksleistung
- Netzlast Deutschland: meist 40–80 GW; Mittelwert 2017: 55,3 GW; Maximum 2017: 73 GW
- Mittlere PV-Einspeisung 2017: 38,4 TWh; Spitzenwert am 27.05.2017 um 13:00 Uhr: 30 GW = 42,7 % der Gesamterzeugung
- Maximale Windeinspeisung 2017: 40 GW am 28.10.2017
- Ziel Bundesregierung bis 2020: 47 % erneuerbare Anteile, bis 2030: 50 %, bis 2050: mindestens 80 %
- Ca. 85 % aller PV-Anlagen sind dezentral im Niederspannungsnetz angeschlossen; Wirkleistungseinspeisung hebt lokale Spannung an → PV-Anlagen müssen Blindleistung bereitstellen

Fossile Kraftwerke:
- Steinkohlekraftwerke: Wirkungsgrad bis 48 %
- Braunkohlekraftwerke: bis 46 %
- Neue Dampfkessel-Erprobung: 250 bar, 550/560 °C; derzeit Test: 270 bar, 580/600 °C; Ziel: 300 bar, 700/720 °C mit η = 50 %
- Erdgas-Effizienz: bereits 58 %
- Gasturbinen-Leistungsgrenze überschritten: 15 MW; neue Entwicklungen bis 300 MW mit Ziel 30 % η

### Wasserkraftwerke (Abschnitt 26.1)

#### Grundprinzip
Potentielle Energie des Wassers wird über Fallrohr in kinetische Energie umgewandelt → Turbine → Generator → elektrische Energie.

Turbinentypen nach Einsatzbereich:
- **Kaplan-Turbine** (Niederdruckturbine, axial): Laufwasserkraftwerke mit geringem Gefälle und großen Wassermengen → Grundlastdeckung
- **Francis-Turbine** (Mitteldruckturbine, radial): Speicherkraftwerke mit mittleren Fallhöhen
- **Pelton-Turbine** (Hochdruckturbine, tangential): sehr große Fallhöhen bei Speicherkraftwerken

Installierte Leistung Wasserkraftwerke (ohne Pumpspeicher): ca. 4,05 GW; erzeugte Jahresarbeit: 20,9 TWh

#### Leistungsberechnung Wasserkraft (Abschnitt 26.1.1)

Formeln:
- Potentielle Energie: Wpot = FG · H = m · g · H
- Masse: m = V · ρ
- Kinetische Energie je Volumen: Wkin = V · ρ · g · H
- Turbinenleistung: P = η · ρ · g · Q · H
- Faustformel (mittlerer Wirkungsgrad): P ≈ 8 · Q · H (Q in m³/s, H in m, P in kW)
- Gesamtwirkungsgrad: ηGes = ηT · ηA · ηG · (1 − ε) mit ε = Eigennutzung
- Spezifische Drehzahl: nsp = n · √Q / H^0,75 (zur Turbinenauswahl)

#### Pumpspeicherkraftwerke (Abschnitt 26.1.2)

Funktionsprinzip: Bei Energieüberschuss wird Wasser vom Unterbecken ins Oberbecken gepumpt (elektrisch → potentiell). Bei Bedarf (Spitzendeckung) erfolgt Rückverstromung.

Wirtschaftlichkeit durch:
- Gute Wirkungsgrade von Turbinen und Pumpen
- Günstige Energiepreise in Schwachlastzeiten

Formeln:
- Pumpenleistung: PP = Q · h / (102 · ηP) [MW]
- Gesamtwirkungsgrad: ηGes = ηT · ηG · ηP · ηM

Variablen: ηT = Turbinenwirkungsgrad, ηG = Generatorwirkungsgrad, ηP = Pumpenwirkungsgrad, ηM = Motorwirkungsgrad, Q = Wasserdurchsatz [m³/s], H = Fallhöhe [m], ρ = 10³ kg/m³, g = 9,81 m/s²

**Rechenbeispiel Pumpspeicherkraftwerk (Abschnitt 26.1.3):**
Gegeben: SrG = 250 MVA, cos φ = 0,8, ηT = 86 %, ηP = 82 %, ηG = 93 %, ηM = 91,5 %, Nutzgefälle h = 650 m.

1. Turbinenleistung: PT = SG · cos φ / ηG = 250 MVA · 0,8 / 0,93 = 215 MW
2. Pumpenleistung: PP = SG · cos φ · ηM = 250 MVA · 0,8 · 0,915 = 183 MW
3. Gesamtwirkungsgrad: ηGes = ηM · ηT · ηP · ηG = 60 %
4. Speichervolumen für 4 h: VT = PT · t · 102 / (ηT · h) = 215 MW · 4 · 3600 s · 102 / (0,86 · 650) = 565.000 m³

### Windkraft (Abschnitt 26.2)

#### Grundlagen Windenergienutzung (Abschnitt 26.2.1)

Installierte Windkraftleistung Deutschland: ca. 33 GW → Deckung von 8,9 % des deutschen Strombedarfs.

Physikalische Grundformeln:
- Kinetische Energie: Ekin = ½ · m · v²
- Windleistung über Fläche A: PWind = ½ · (ρ · A · v) · v² = ½ · ρ · A · v³
- Über Rotordurchmesser: PWind = (1/8) · ρ · π · D² · v³
- Windkraftanlage: PWKA = PWind · cp = (1/8) · ρ · π · D² · v³ · cp

Wichtige Erkenntnisse:
- Windleistung steigt quadratisch mit Rotordurchmesser und kubisch mit Windgeschwindigkeit
- Theoretisch maximaler Leistungsbeiwert cp: 59,2 % (Betz-Limit) — Luft kann nicht vollständig abgebremst werden
- Reale maximale cp-Werte: ca. 50 % (Reibungsverluste an Rotorblättern, Blattspitre und Drall)
- Schnelllaufzahl λ = R · Ω / v_Wind (Verhältnis Blattspitzengeschwindigkeit zu Windgeschwindigkeit)
- Optimale Schnelllaufzahl für 3-Blatt-Anlagen: λ = 6
- Betriebsschnelllaufzahl üblicher WKA: 6 bis 7
- Variabel drehende Anlagen passen Rotordrehzahl den aktuellen Windverhältnissen an

#### Konstruktiver Aufbau von Windkraftanlagen (Abschnitt 26.2.2)

Standardkonzept: Auftriebsläufer mit horizontaler Drehachse, 3 Rotorblätter.
- Rotorblätter an Nabe verankert, verdrehbar um Längsachse (Pitch-Regelung)
- Verbindung Rotor → Generator über Welle und Getriebe
- Getriebeloses Konzept (z.B. Enercon): Nabe direkt mit Generatorläufer verbunden
- Maschinenhaus drehbar auf Turm gelagert (Windnachführung, Sturmsicherung)
- Rotordurchmesser moderne WKA: 80–180 m
- Turmhöhen: 80–140 m
- Elektrischer Leistungsbereich: 1–8 MW

#### Anlagenbeispiele (Abschnitt 26.2.3)

Einschaltwindgeschwindigkeit: 3 m/s; Abschaltwindgeschwindigkeit: 25 m/s.
Rotordurchmesser Beispielanlagen: 115–130 m; Turmhöhen: 90–150 m.
- Anlage 1: ausgelegt für hohe Windgeschwindigkeiten
- Anlage 2 und 3: auch für Schwachwindstandorte geeignet

Pitch-Regelung: Bei zunehmender Windgeschwindigkeit über Auslegungsgeschwindigkeit werden Rotorblätter aus dem Wind gedreht → Schnelllaufzahl und Wirkungsgrad nehmen bewusst ab.

#### Generatorsysteme (Abschnitt 26.2.4)

Drehzahlvariable Generatorsysteme im Einsatz:

**Doppeltgespeister Asynchrongenerator:**
- Läufer über Umrichter mit Netz verbunden
- Regelbar in Rotordrehzahl und Blindleistungsabgabe/-aufnahme
- Übersynchron: Rotordrehzahl > Netzfrequenz → Leistungsabgabe über Umrichter ins Netz
- Untersynchron: Rotordrehzahl < Netzfrequenz → Leistungszufuhr zum Läufer
- Umrichtergröße: nur ca. 1/3 der Bemessungsleistung des Stators erforderlich (Vorteil)

**Fremderregter Synchrongenerator (mit Vollumrichter):**
- Vollständige Entkopplung der Rotordrehzahl von der Netzfrequenz
- Gleichstrom für Läufermagnetfeld über Gleichrichter erzeugt
- Höchste Regelbarkeit

**Permanenterregter Synchrongenerator (mit Vollumrichter):**
- Dauermagnete im Läufer → kein Gleichstrom für Magnetfeld nötig
- Nachteil: Umrichter muss für die gesamte Generatorbemessungsleistung ausgelegt werden

#### Standortauswahl-Beispiel (Abschnitt 26.2.5)

Vergleich drei WKA an einem süddeutschen Standort:

| WKA | Nennleistung | Jahresertrag [MWh] | Kapazitätsfaktor [%] |
|---|---|---|---|
| Anlage 1 | 7,5 MW | 14.525 | 22 |
| Anlage 2 | 3 MW | 8.155 | 32 |
| Anlage 3 | 3,3 MW | 9.378 | 32 |

Fazit: Anlage 1 hat höchsten Absolutertrag, aber schlechten Kapazitätsfaktor → nicht standortgerecht. Anlage 2 und 3 mit je 32 % Auslastung deutlich besser für diesen Schwachwindstandort. Endauswahl nach wirtschaftlichen Kriterien.

Formel Kapazitätsfaktor: c = Wel,a / (Pn · 8760 h)
Formel Ertrag je Geschwindigkeitsklasse: Wel,GK = tGK · PWKA,GK

#### Parkverkabelung — Berechnungsbeispiel (Abschnitt 26.2.6)

Windpark mit 3 WKA à 3 MW, Transformatoren im Turm auf 20 kV, Netzanschluss 110 kV.

Betriebsströmberechnungen:
- Abschnitt 1 (1 WKA): IB = Pn / (√3 · Un · cos φ) = 3000 kW / (√3 · 20 kV · 0,9) = 96,23 A
- Abschnitt 2 (2 WKA): 2 · 96,23 = 192,45 A
- Abschnitt 3 (3 WKA): 3 · 96,23 = 288,68 A

Kabelauswahl Aluminiumleiter NA2XS2Y:

| Querschnitt [mm²] | Strombelastbarkeit [A] | Leiterwiderstand [Ω/km] | Betriebsinduktivität [Ω/km] |
|---|---|---|---|
| 50 | 171 | 0,641 | 0,129 |
| 70 | 208 | 0,443 | 0,123 |
| 150 | 315 | 0,206 | 0,116 |

Gewählte Kabel: Abschnitte 1 und 2 → NA2XS2Y 3 × 70 mm²; Netzanschluss (Abschnitt 3) → NA2XS2Y 3 × 150 mm².

Transformatorwahl: Bemessungsleistung 12 MVA, ukr = 11 %. Scheinleistung Windpark: S = ΣPwka / cos φ = 9 MW / 0,9 = 10 MVA.

Spannungsfälle:
- Abschnitt 1: ΔU = √3 · l · IAbschnitt1 · (R' · cos φ + X' · sin φ) = 29 V
- Abschnitt 2: ΔU = √3 · 0,411 km · 92,45 A · (0,443 · 0,9 + 0,123 · 0,43) = 62 V
- Abschnitt 3: ΔU = √3 · 0,867 km · 288,68 A · (0,206 · 0,9 + 0,116 · 0,43) = 103 V
- Gesamtspannungsfall: ΔUGes = 29 + 62 + 103 = 194 V = 0,97 % (bezogen auf 20 kV)

#### Netzanbindung WKA (Abschnitt 26.2.9)

Für WKA-Netzanbindung gilt grundsätzlich: ΣS''k / S²WKA ≥ 30

Für WKA mit Gleichstromzwischenkreis (Vollumrichter): ΣS''k / S²WKA ≥ 250

#### Erdungssystem WKA (Abschnitt 26.2.10)

- Vier Ringerder im Fundament, verteilt auf verschiedene Positionen
- Material: feuerverzinkter Bandstahl, Mindestquerschnitt 100 mm² (3,5 × 30 mm), untereinander durch Fundamenterderverbinder verbunden
- Am Übergang Fundament/Erdreich: nicht-rostender Stahl V4A, Mindestquerschnitt 100 mm²
- Im Erdreich: V4A-Bandstahl, blankes oder verzinntes Kupferseil zulässig
- Geforderter maximaler Erdungswiderstand: 10 Ω (über Fundamenterder allein oder mit Zusatzerdern)
- Zentraler Anschlusspunkt aller nicht aktiven Metallteile: Haupterdungsklemme (HEK)
- HEK ist direkt mit dem Sternpunkt des Anlagentransformators verbunden
- HEK-Position: innerhalb Niederspannungsverteilung oder an Ölwanne (je nach Anlagentyp)
- Schutzpotentialausgleich innerhalb der WEA wird über die HEK hergestellt
- Fremde Anlagen (z.B. Übergabe-/Transformatorstation), die elektrisch mit der WEA verbunden sind, werden mit der Erdungsanlage der WEA verbunden

E-Modul (Turm) bestehend aus drei Ebenen: untere Ebene, mittlere Ebene (Eingangsebene) und obere Ebene; Turmfuß durch Trennwand in Niederspannungs- und Mittelspannungsbereich aufgeteilt.

#### Beispiel: Windleistungsberechnung (Abschnitt 26.2.11)

Windgeschwindigkeit 25 km/h = 6,94 m/s:
- Pw = 0,61 · v³ = 0,61 · (6,94)³ = 203,89 W/m²

Anmerkung: Diese Leistung ist in der Praxis nicht vollständig nutzbar. Der theoretisch mögliche Anteil der Windleistung, der in mechanische Energie umgewandelt werden kann, beträgt 59 %. Jährliche Windleistung näherungsweise: Pa ≈ 3,2 · v³ · A.

Kapazitätsfaktor c bei gutem Anlagenbetrieb: 0,30 bis 0,35.

#### Beispiel: Generator-Transformator-Berechnung (Abschnitt 26.2.12)

WKA-Daten: Bemessungsleistung 2,3 MW, 400 V, 50 Hz.
- Generatorbemessungsstrom HS-Seite: IrG = SrG / (√3 · UrG) = 4275 A
- Maximaler Anfangskurzschlussstrom: 4500 A mit 9 Leistungsschränken

Transformator: SrT = 40 MVA, 110 kV, ukr = 12 %.
- Bemessungsstrom HS-Seite (110 kV): IrT = 40 MVA / (√3 · 110 kV) = 210 A
- Bemessungsstrom NS-Seite (20 kV): IrT = 40 MVA / (√3 · 20 kV) = 1154,7 A

#### Beispiel: Kurzschlussleistungsberechnung (Abschnitt 26.2.13)

Gegebene Systemdaten: S''kQ = 8 GVA (110 kV-Netz), Transformator: SrT = 20 MVA, ukr = 12 %, uRr = 0,05 %, PKr = 10 kW; Kabel: 20 km NA2XS(F)2Y 150 mm², R'l = 0,207 Ω/km, X'l = 0,121 Ω/km.

Berechnungsgang auf 20-kV-Ebene:
- Netzimpedanz 110 kV: ZQN = c · U²n / S''kQ = 1,1 · 110² / 8000 = 1,66 Ω
- Umrechnung auf 20 kV: ZQN,20kV = ZQN · ü² = 0,055 Ω
- Transformatorimpedanz: ZT = ukr · (UrT)² / (100 % · SrT) = 12 % · (20 kV)² / (100 % · 20 MVA) = 2,4 Ω
- Transformatorwirkwiderstand: RT = uRr · (UrT)² / (100 % · SrT) = 0,5 % · (20 kV)² / (100 % · 20 MVA) = 0,1 Ω
- Transformatorreaktanz: XT = √(ZT² − RT²) = 2,39 Ω
- Kabelwirkwiderstand: Rl = R'l · l = 0,207 · 20 = 4,14 Ω
- Kabelreaktanz: Xl = X'l · l = 0,121 · 20 = 2,42 Ω; Zl = 4,8 Ω
- Gesamtimpedanz: ZG = ZQN,20kV + ZT + Zl = 7,255 Ω
- Kurzschlussleistung: SKV = U²kV / ZG = (20 kV)² / 7,255 Ω = 55,13 MVA

#### Beispiel: Anschlussgesuch WKA (Abschnitt 26.2.14)

20-kV-Netz: SKV = 150 MVA, φ = 70°. WKA: Pn = 2 MW, Anlage 1, cos φ = 0,95, Flickerbeiwert c = 4, φWKA = 11°, Schaltstromfaktor ki = 1,7, Bemessungsstrom = 2887 A.

Nachweis-Schritte:

1. Scheinleistung für Betriebsmittel-Bemessung (600 min): SAmax = ΣPrG · p600 / cos φ = 2 MW · 1 / 0,95 = 2,126 MVA; IAmax = 2,126 MVA / (√3 · 20 kV) = 61,27 A

2. Zulässige Spannungsänderung: uAn = SAmax · cos(φKV + φ) / SKV = 2,126 · 0,95 / 150 = 1,34 % < 2 % ✓

3. Betriebsmittel 10-min-Wert: SAmax = 2 MW · 1,01 / 0,95 = 2,126 MVA (identisch)

4. Spannungsanhebung 1-min-Wert: SAmax,1min = PrG · p1min / cos φ = 2 · 1,05 / 0,95 = 2,21 MVA; kkl = SKV / SAmax,1min = 150 / 2,21 = 67 > 50 ✓

5. Kurzschlussfestigkeit: SKVres = SKV + 6 · PrG / cos φ = 150 + 6 · 2 / 0,95 = 162,63 MVA; Ires = 162,63 / (√3 · 20) = 4,69 kA → Betriebsmittel müssen für diesen Strom ausgelegt sein

6. Schaltbedingte Spannungsänderungen: d = ki,max · SrE / (cos φ · SKV) = 1,7 · 2 / (0,95 · 150) = 2,3 % < 3 % ✓

7. Kurzschlussfestigkeit des Kabels (NA2XS(F)2Y 150 mm²): Stromdichte Jth = 94 A/mm², Abschaltzeit Tk = 1 s; Ithr = S · Jth = 150 mm² · 94 A/mm² = 14,1 kA; Ith(Tk) = Ithr / √Tk = 14,14 kA ✓

8. Oberschwingungsbeurteilung: SKV / SA = 300 · (150 MVA / 2,126 MVA) = 70,55 < 300 → Filterkreise erforderlich

9. Langzeitflicker: Plt = c · SrG / SKV = 20 · 2 / (0,95 · 150) = 0,28 < 0,46 → zulässig. Anschluss bewilligt, aber Filterkreise einzubauen.

### Photovoltaik (Abschnitt 26.3)

#### Betriebsarten von PV-Anlagen

**Inselbetrieb:** In sich geschlossenes, lokal begrenztes System. Anwendungen: Schiff, Berghütte. Problem: Versorgungssicherheit bei fehlender Sonneneinstrahlung → Energiespeicherung erforderlich. Gleichstromproduktion → Akkumulator → ggf. Wechselrichter für Wechselstromverbraucher.

**Netzbetrieb:** Einspeisung in überregionales Energieversorgungsnetz; Verbraucher beziehen Energie aus dem Netz.

#### Physikalische Grundlagen der Solarzelle

Funktionsprinzip: Photovoltaischer (innerer lichtelektrischer) Effekt — Strahlungsenergie (Photonen) direkt in elektrische Energie umgewandelt.

Drei Voraussetzungen:
1. Strahlung muss vom Material absorbiert werden
2. Lichtabsorption muss zur Erzeugung beweglicher negativer und positiver Ladungsträger führen
3. Die Ladungsträger müssen getrennt werden

Halbleiterphysik (Bändermodell):
- Elektronen in Atomen besetzen Orbitale mit diskreten Energieniveaus (Quantentheorie / Bohr-Sommerfeld)
- Im Kristall überlappen Orbitale benachbarter Atome → Elektronen nicht mehr auf Einzelatome lokalisiert
- Energieniveaus verbreitern sich zu Energiebändern (erlaubte Bereiche) und verbotene Lücken
- Valenzband: letztes vollbesetztes Band
- Leitungsband: bei T = 0 K vollständig unbesetzt
- Bandlückenenergie: charakteristische Größe für Halbleiter, entscheidend für PV-Funktion

Anregungsmechanismus:
- Elektronen vom Valenz- ins Leitungsband: thermisch oder optisch möglich
- Mindestenergie: Bandlückenenergie des Materials
- Photon muss mindestens die Energie h · f ≥ E_Bandlücke besitzen
- Photonenergie hängt nicht von Lichtintensität, sondern von Frequenz/Wellenlänge ab

**Rechenbeispiel Photon-Energie:**
Photon mit Wellenlänge 550 nm:
E = h · c / λ = 6,63 × 10⁻³⁴ Js · 3 × 10⁸ m/s / (550 × 10⁻⁹ m) = 3,62 × 10⁻¹⁹ J

Verluste bei Silizium-Solarzellen:
- 24 % der Sonnenlicht-Photonen haben zu wenig Energie für Elektron/Loch-Paar-Erzeugung
- 33 % der Photonen haben zu viel Energie (Überschuss geht verloren)
- 15 % Verluste durch technologische Ursachen
- Weitere Verluste durch: Reflexion an Zelloberfläche, Abschattung durch Kontakte, Rekombination im Volumen und an der Oberfläche, Inkongruenz von Maximalstrom und Maximalspannung, ohmsche Widerstände

Betriebliche Einflüsse auf PV-Zelle: Serienwiderstand (schlechte Lötstellen), Parallelwiderstand (Kurzschluss), Bestrahlungsstärke, Temperatur, Verschattung, String-Verschaltung.

Hot-Spot: Defekte oder abgeschattete Zellen erzeugen keine PV-Energie, bilden hochohmigen Widerstand, erwärmen sich stark und können dauerhaft beschädigt werden → Gegenmaßnahme: Parallelschalten von Bypass-Dioden.

Erstbelichtungsverlust: Zellen, die einwandfrei erscheinen, können unter erster Belichtung bis zu 10 % der Sollleistung verlieren.

#### Silizium-Solarzelltypen

| Typ | Struktur | Wirkungsgrad | Bemerkung |
|---|---|---|---|
| Monokristallin | Einziger Si-Kristall | ca. 15–25 % | Höchster Wirkungsgrad, aufwändige Herstellung |
| Polykristallin | Viele kleine Si-Kristalle | ca. 14–16 % | Günstigere Herstellung, derzeit auf Platz 2 |
| Amorph | Ungeordnete Si-Atome | ca. halber Wert gegenüber monokristallin | Sehr dünn, kostengünstig, Einsatz in Taschenrechnern und Uhren |

#### pn-Übergang der Solarzelle (Abschnitt 26.3.1)

**p-Dotierung:** Einbau von dreiwertigem Bor in Si-Gitter → ein Si-Elektron findet kein Paarelektron → Loch (Defektelektron/Leerstelle) entsteht. Material wird p-leitend, bleibt elektrisch neutral (Protonenzahl = Elektronenzahl).

**n-Dotierung:** Einbau von fünfwertigem Phosphor in Si-Gitter → ein Elektron findet kein Paarelektron → freies Elektron (Störstelle) entsteht.

**pn-Übergang:**
- Kontakt von p- und n-Bereich → Elektronen diffundieren aus n-Bereich in Löcher des p-Bereichs
- Entstehung eines elektrischen Feldes in der Sperrschicht (Raumladungszone)
- Diffusionsspannung UD entsteht; bei Silizium: UD ≈ 0,7 V
- Diodenwirkung: Strom fließt nur in einer Richtung
- Bei Belichtung: Elektronen/Loch-Paare entstehen → inneres Feld trennt sie; Elektronen fließen in n-Bereich, Löcher in p-Bereich → Photostrom
- Ausgangsspannung der Zelle abhängig vom Abstand Valenz- zu Leitungsband (= Bandlückenenergie)
