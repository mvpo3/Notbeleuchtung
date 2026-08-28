# Planung von Elektroanlagen — Teil 15
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 601-640.

Dieser Teil behandelt die technischen Grundlagen und Planungsbeispiele für Photovoltaikanlagen (Berechnungsformeln, Komponentenauswahl, Dimensionierungsbeispiele), ergänzende regenerative Energiesysteme (Brennstoffzellen, Biomasse, Energiespeicher, Smart Grid), Netzanschlussregeln nach EnWG und VDN-Richtlinien sowie ein vollständiges Projektierungsbeispiel einer Industrieanlage mit Verbrauchertabelle und Schaltplanung.

## Inhalt

### 26.3 Photovoltaik — Elektrische Grundformeln

#### Diodenkennlinie und MPP-Gleichungen

Der Strom einer Photovoltaikzelle ergibt sich aus der Überlagerung von Photostrom (IL) und Diodenstrom (I0). Für den Maximum Power Point (MPP) gelten folgende Zusammenhänge:

- Bei Spannung null entspricht der Strom dem Kurzschlussstrom: ISC = IL
- Die Leerlaufspannung ergibt sich aus dem natürlichen Logarithmus des Verhältnisses IL/I0, gewichtet mit dem thermischen Spannungsterm (nkT/q)
- Die Ausgangsleistung an einem beliebigen Kennlinienpunkt: Pout = U × I
- Die MPP-Leistung: PMPP = UMPP × IMPP

Verwendete Konstanten und Größen:
- Boltzmann-Konstante k = 1,38 × 10⁻¹⁹ J/K
- Identitätsfaktor für Silizium n = 2
- Elementarladung q = 1,6 × 10⁻²³ As
- Temperaturspannung UT = 26 mV
- T = Zelltemperatur in K; I0 = Sperrstrom in A; U0C = Leerlaufspannung; U = Zellspannung in V

#### 26.3.2 Füllfaktor

Der Füllfaktor (FF) beschreibt das Verhältnis der tatsächlich nutzbaren maximalen Leistung zum theoretischen Produkt aus Leerlaufspannung und Kurzschlussstrom:

FF = (UMPP × IMPP) / (UL × IK)

Typische Füllfaktor-Werte liegen im Bereich 0,7 bis 0,85.

Berechnungsbeispiel für ein Modul mit Herstellerangaben:
- ISC = 5,75 A, U0C = 44,9 V, Pmax = 185 W
- FF = 185 W / (44,9 V × 5,75 A) = 0,72

#### 26.3.3 Wirkungsgrad

Der Zellwirkungsgrad gibt das Verhältnis der elektrisch erzeugten Leistung zur eingestrahlten Lichtleistung an:

η = Pout / Pin = PMPP / Popt = Pmax / (A × EAM1,5)

Typische Wirkungsgrade:
- Silizium: 13–25 %
- Dünnschicht (Thin Film): 8–15 %

#### 26.3.4 Erzeugte Energie einer Dachfläche

Berechnungsbeispiel: Dachfläche 40 m², Wirkungsgrad 15 %
- Maximalleistung: Pmax = 0,15 × 1000 W/m² × 40 m² = 6 kW
- Jahresertrag: 6 kW × 2,8 × 365 d = 6132 kWh

#### 26.3.5 Reihenschaltung von Solarzellen

Bei Reihenschaltung fließt durch alle Zellen derselbe Strom; die Einzelspannungen addieren sich zur Gesamtspannung. Häufig werden 36 Zellen in Reihe geschaltet, um die Spannung für das Laden eines 48-V-Bleiakkumulators zu optimieren.

- Stromgleichung: I = I1 = I2 = ... = In (alle gleich)
- Spannungsgleichung: U = Summe aller Ui (i = 1 bis n)

#### 26.3.6 Parallelschaltung von Solarzellen

Bei Parallelschaltung liegt an allen Zellen dieselbe Spannung an; die Ströme addieren sich. Da der Einzelzellenstrom bereits über 3 A beträgt und die Spannung unter 0,7 V liegt, wird die Parallelschaltung wegen zu großer ohmscher Verluste selten eingesetzt.

- Spannungsgleichung: U = U1 = U2 = ... = Un (alle gleich)
- Stromgleichung: I = Summe aller Ii (i = 1 bis n)

#### 26.3.7 Kenndaten von Photovoltaikanlagen

Eine PV-Anlage umfasst: Module, Wechselrichter, Laderegler und Speicher.

Die Luftmasse (AM) beeinflusst die Energiestrahlung und hängt von der Luftdichte ab. Standardbetriebsbedingungen: 1000 W/m², 25 °C. Dabei liefert eine Zelle typisch 3 A, 0,5 V, 1,5–1,7 Wp. Häufigste Modulkonfiguration: 60–70 Zellen in vier Reihen, Fläche 0,5–1,3 m².

Einflussfaktoren auf den Ertrag:
- Einfallwinkel und Ausrichtung der Module
- Strom und Leistung sind direkt proportional zur Einstrahlung
- Abschattung hat großen Einfluss; Bypass-Dioden reduzieren Verluste
- Alterung, Verschmutzung und hohe Modultemperatur verringern die Leistung

Performance Ratio (PR) über das Jahr: PR = (E × GSTC) / (PSTC × G)
- E = Stromproduktion in kWh, GSTC = 1000 W/m², PSTC = Modulleistung bei Standardbedingungen, G = Strahlungssumme

Kenngrössen-Übersicht:
| Symbol | Bedeutung | Einheit |
|--------|-----------|---------|
| Amodul | Modulfläche | m² |
| GSpez | spezifische Einstrahlungsleistung | W/m² |
| IMPP | Strom am MPP | A |
| ISC | Kurzschlussstrom | A |
| PMPP | Leistung am MPP | Wp |
| TMod | Modultemperatur | °C |
| UMPP | Spannung am MPP | V |
| U0C | Leerlaufspannung | V |
| η | Modulwirkungsgrad | % |

Formeln:
- Modulwirkungsgrad: ηModul = PSTC / (1000 W/m² × AModul)
- Spezifischer Ertrag in kWh/kWp: ηSpez = Eac / Pnenn
- Betriebswirkungsgrad: ηB = GModul / (AModul × ηModul)

#### 26.3.8 Wechselrichter

Wechselrichter wandeln DC-Spannung in AC-Spannung um. Anschlussvarianten:
- Modulwechselrichter (ein WR je Modul, Gleichstromkabel entfällt)
- String-Wechselrichter (ein WR je String, häufigste Variante)
- Zentralwechselrichter (Strings parallel im Generatoranschlusskasten zusammengeführt)

Für die Eigennutzung werden Zweirichtungszähler zur getrennten Erfassung von eingespeistem und bezogenem Strom installiert.

Wichtige Bedingung bei Kopplung PV-Anlage/WR: Der Kurzschlussstrom des PV-Generators am MPP muss kleiner sein als der Höchsteingangsstrom des Wechselrichters.

Kenngrössen des Wechselrichters:
| Symbol | Bedeutung | Einheit |
|--------|-----------|---------|
| Pn | Nenneingangsleistung | W |
| Pin | maximale Eingangsleistung | W |
| Pout | maximale Ausgangsleistung | W |
| η | maximaler Wirkungsgrad | % |
| ηEuro | maximaler Euro-Wirkungsgrad | % |
| ISC | Kurzschlussstrom | A |
| PNetz | Netzeinspeisung | W |
| Pv | Standby-Verluste | W |
| Uin | maximale Eingangsspannung (nicht überschreiten) | V |
| Umin | Spannung bei höchster Betriebstemperatur | V |
| Umax | Spannung bei tiefster Betriebstemperatur | V |
| U0Cmax | Leerlaufspannung bei tiefster Betriebstemperatur | V |
| UMPP | MPP-Spannungsbereich | V |
| UMPPTmin | kleinste Betriebsspannung WR-Eingang | V |
| UMPPTmax | größte Betriebsspannung WR-Eingang | V |
| UMAX | maximale Höchstspannung WR | V |
| Un | Nenn- und Einschaltspannung | V |
| Uout | Ausgangsspannung | V |

#### 26.3.9 Komponenten einer Photovoltaikanlage

Vollständige Komponentenliste: Solarmodule, Unterkonstruktionen, Kabel und Leitungen, Laderegler mit Rückstrom-Sperrdiode, Batterien, Wechselrichter, Zähler, Verteilungen im NS-Netz.

#### 26.3.10 Planungsbeispiel: Einfamilienhaus-PV-Anlage

Ausgangsdaten:
- Jahresverbrauch Haushalt: 4000 kWh
- Erwartete jährliche Produktion (Wirkleistungsfaktor 0,75): 0,75 × 4000 = 3000 kWh (im Text: 3430 kWh)
- Anschluss an NS-Netz, Verbindung mit vorhandener Erdungsanlage
- Vertragsleistung: 3 kW
- Dachfläche: 60 m²
- Neigungswinkel: 30°
- Azimut-Winkel: +15°

**Schritt 1 – Panelwahl:**
- Stückleistung 175 W pro Panel
- Benötigte Panelanzahl: 3000 W / 175 W ≈ 17 Panels, Reihenschaltung

Herstellerangaben:
| Größe | Wert |
|-------|------|
| PMPP | 175 W |
| Wirkungsgrad η | 12,8 % |
| UMPP | 23,3 V |
| IMPP | 7,54 A |
| U0C | 29,4 V |
| ISC | 8,02 A |
| Höchstspannung | 1000 V |
| Temperaturkoeffizient Leistung | -0,43 %/°C |
| Temperaturkoeffizient Spannung | -0,107 V/°C |
| Abmessungen | 2000 × 680 × 50 mm |
| Gesamtfläche (17 Panels) | 1,36 m² × 17 = 23 m² |
| Schutzklasse | II |

Temperaturgrenzen Panel: –10 °C bis +70 °C. Spannungsvariationen gegenüber Standardbedingungen (25 °C):
- Maximale Leerlaufspannung: 29,4 V + 0,107 × (25 + 10) = 33,13 V
- Mindestspannung MPP: 23,3 V – 0,107 × (70 – 25) = 18,5 V
- Höchstspannung MPP: 23,3 V + 0,017 × (25 + 10) = 27,03 V (hier Koeffizient 0,017 laut Quelle)
- 120 %-Leerlaufspannung: 1,2 × 29,4 V = 35,28 V > 33,13 V (erfüllt)

Elektrische Strangeigenschaften (17 Panels Reihe):
- Spannung MPP: 17 × 23,3 V = 396 V
- Strom MPP: 7,54 A
- Maximaler Kurzschlussstrom: 1,25 × 8,02 A = 10 A
- Maximale Leerlaufspannung: 17 × 35,28 V = 599,8 V
- Mindestspannung MPP: 17 × 18,5 V = 314,58 V
- Höchstspannung MPP: 17 × 27,03 V = 459,5 V

**Schritt 2 – Wahl des Wechselrichters:**
- Bis 4,7 kW einphasig, darüber dreiphasig
- Dimensionierungsregel: 0,8 × PPV < PWR,dc < 1,2 × PPV

Gewählter WR:
| Größe | Wert |
|-------|------|
| Bemessungsleistung Eingang | 3150 W |
| Betriebsspannungsbereich | 203–600 V |
| Höchstspannung DC-Seite | 680 V |
| Höchsteingangsstrom | 11,5 A |
| Höchstausgangsleistung AC | 3000 W |
| Bemessungsspannung AC | 230 V |
| Leistungsfaktor | 1 |
| Maximaler Wirkungsgrad | 95,5 % |
| Europäischer Wirkungsgrad | 94,8 % |

Prüfungen:
- Leerlaufspannung Strang < WR-Höchstspannung: 599,7 V < 680 V ✓
- Mindest-MPP-Spannung Strang > MPPT-Mindestspannung WR: 314,58 V > 203 V ✓
- Größte MPP-Spannung Strang < MPPT-Höchstspannung WR: 459,5 V < 600 V ✓
- Maximaler Kurzschlussstrom Strang < WR-Eingangstoleranz: 10 A < 11,5 A ✓

**Schritt 3 – Wahl der Leitungen:**
Zu beachtende Bedingungen (nach DIN VDE 0100-430, DIN VDE 0298-4): Umgebungstemperatur, Verlegeart, Strombelastbarkeit, Spannungsfall, Betriebstemperatur.

Schutzeinrichtungs-Bemessung:
- Wenn Fehlerstrom < Betriebsstrom → keine Schutzeinrichtung nötig
- Andernfalls: Bemessungsstrom SE = 1,56 × ISC (Faktor 1,56 = 1,25 × Leistungserhöhungsfaktor)

Gewählte Leitung: 2,5 mm²
- Bemessungsspannung: 600/1000 V AC, 1500 V DC
- Betriebstemperaturbereich: –40 °C bis +90 °C
- Strombelastbarkeit frei in Luft: 35 A
- Korrekturfaktor: 0,91
- Höchsttemperatur: 120 °C

Zulässige Strombelastbarkeit: Iz = 0,9 × 0,91 × 35 A = 29 A
Bedingung: 29 A > 1,25 × ISC = 10 A ✓

**Schritt 4 – Spannungsfall:**
Berechnung über alle Leitungsabschnitte:
- Formel: u = (Pmax × (ρ₁ × l₁ + ρ₂ × 2 × L₂ + ρ₃ × 2 × L₃)) / (A × U²) × 100 %
- Ergebnis: u = 3000 W × (0,021 × 16 + 0,018 × 2 × 15 + 0,018 × 2 × 1) / (2,5 mm² × 396² V²) × 100 % = 0,7 %

**Schritt 5 – Schalt- und Schutzeinrichtungen:**
Maßgebliche Normen: DIN EN 60947-4-1 (VDE 0660-102), IEC TS 62257-7-1.

Anforderungen:
- Lasttrennschalter auf DC- und AC-Seite verpflichtend
- Anschlusskasten muss Warnsignal für anliegende Spannung enthalten
- Überlastschutz kann entfallen wenn Kabelbelastbarkeit ≥ 1,25 × ISC

**Schritt 6 – Erdungsmaßnahmen:**
- Erdung nach DIN VDE 0100 Teil 540 und 712 (TN, TT oder IT-System möglich)
- AC- und DC-Seite getrennt erden
- Blitzschutz und Schutzpotentialausgleich nach IEC 62305 (VDE 0185-305)

#### 26.3.11 Dimensionierungsbeispiel: Größerer Wechselrichter

Ausgangsdaten: 32 Strings à 8 Module, je 180 Wp; WR-Parameter: UWR,MPP,max = 480 V, UWR,MPP,min = 180 V, U0C,max = 600 V, maximale Eingangsleistung 6500 W.

WR-Datenwerte:
- Nennleistung DC: 5265 W, max. Leistung DC: 5525 W
- Betriebsspannungsbereich: 100–600 V DC
- MPP-Spannungsbereich: 180–480 V DC
- Maximale Spannung: 600 V DC
- Eingänge: 2 Stränge, Nennstrom 2 × 15 A = 30 A
- Ausgang max. Leistung: 5259 W, max. Strom: 25 A
- Europäischer Wirkungsgrad: 94,5 % bei 400 V, max. Wirkungsgrad: 95,5 %

Berechnungsschritte:

1. Leistungsanpassung:
   - PPV = 32 × 180 Wp = 5,76 kWp
   - PWR,dc,min = 0,8 × 5,76 = 4,6 kWp
   - PWR,dc,max = 1,2 × 5,76 = 6,912 kWp
   - Mit Modultoleranzen (±5 %): PWR,dc,min = 0,8 × 1,05 × PPV = 4,838 kWp; PWR,dc,max = 1,2 × 0,95 × PPV = 6,567 kWp

2. Maximalspannung bei –10 °C:
   - U0C bei 25 °C (Standardbed.): 8 × 45,2 V = 361,6 V
   - Spannungskorrektur für –10 °C: ΔU = (–10 – 25) × (–0,381/K) × U0C = 48,1 V
   - Korrigierte U0C,–10°C = 361,6 + 48,1 = 409,7 V < 600 V ✓

3. MPP-Spannungsbereich:
   - UMPP = 8 × 36,3 V = 290,4 V
   - Korrektur –10 °C: ΔU = 38,6 V → UMPP,–10°C = 329 V < 480 V ✓
   - Korrektur –70 °C: ΔU = –49,7 V → UMPP,–70°C = 240,7 V > 180 V ✓
   - IMPP = 2 × 4,96 A < 15 A ✓

#### 26.3.12 Dimensionierungsbeispiel: Kleinerer Wechselrichter mit MPP-Prüfung

Ausgangsdaten: 15 Module, PMPP = 54 W, UMPP = 20 V, U0C = 22 V, STC 25 °C, Temperaturkoeffizient αU = –0,45 %/°C, Eingangsspannungsbereich WR: 200–400 V DC, MPP-Regelbereich: 240–340 V, maximale Eingangsleistung: 900 W.

1. Leistungsanpassung:
   - PPV = 15 × 54 Wp = 810 Wp
   - PWR,dc,min = 0,8 × 810 = 648 Wp; PWR,dc,max = 1,2 × 810 = 972 Wp → Leistung liegt im Bereich ✓

2. Maximalspannung:
   - Umax,PV = 15 × 22 V × [1 + (–0,45%/100) × (–10 – 25)] = 381,98 V < 400 V ✓

3. MPP-Spannungsbereich:
   - UMPP,PV,max bei –10 °C = 15 × 20 V × [1 + (–0,45%/100) × (–10 – 25)] = 347,25 V > 340 V **Überschreitung**
   - UMPP,PV,min bei +70 °C = 15 × 20 V × [1 + (–0,45%/100) × (70 – 25)] = 239,25 V < 240 V **Unterschreitung**

Ergebnis: Konfiguration ist nicht in Ordnung, da der MPP-Spannungsbereich sowohl über- als auch unterschritten wird.

#### 26.3.13 Planung von Photovoltaikanlagen: Netzgekoppelt vs. Inselanlage

Zwei grundsätzliche Betriebsarten:

**Netzgekoppelte Anlagen:** Betrieb als Kleinkraftwerk im Verbund mit dem Versorgungsnetz. Nicht selbst verbrauchte Energie wird ins Niederspannungsnetz eingespeist; das Netz dient quasi als Speicher.

**Inselanlagen:** Einsatz dort, wo kein allgemeines Stromnetz vorhanden ist. Überschüssige Energie wird in Akkumulatoren zwischengespeichert. Schwachpunkt: begrenzte Akkulebensdauer, hoher Wartungsaufwand, Selbstentladung. Konkurrenzfähig nur gegenüber anderen dezentralen Erzeugern (z.B. Dieselaggregaten), nicht gegenüber Netzstrom. Empfehlung: Wenn Netz vorhanden, immer netzgekoppelte Anlage bevorzugen.

#### 26.3.14 Prüfungen von Photovoltaikanlagen

Nach IEC 61215 werden thermische und elektrische Kenngrößen von PV-Modulen geprüft:

- Sichtprüfung
- Leistung unter Standardtestbedingungen
- Messung der Temperaturkoeffizienten
- Leistung bei NOCT (Nominal Operating Cell Temperature)
- Leistung bei niedriger Bestrahlungsstärke
- Dauerprüfung unter Freilandbedingungen
- Hot-Spot-Dauerprüfung
- UV-Prüfung
- Elektrische Funktionsprüfung
- Isolationsprüfung von Leitungen
- Schutzleiterprüfungen
- Temperaturwechselprüfung
- Feuchte-Frost-Prüfung
- Mechanische Widerstandsfähigkeit der Anschlüsse
- Mechanische Belastungsprüfung
- Hagelprüfung
- Verlustberechnungen
- Test der Auslösezeiten von Q/U-Schutz

#### 26.3.15 Anschlussbeurteilung einer PV-Anlage (Rechenbeispiel)

Anlagendaten:
- Anschlussleistung: 20 kW
- Kabellänge: 50 m
- Querschnitt: NYY-J 4 × 35 mm²
- Netz-Kurzschlussleistung: 100 MVA
- Transformator: 400 kVA, uk = 4 %, PCu = 4,6 kW
- Kabel: NAYY 4 × 95 mm², R = 0,32 Ω/km, X = 0,082 Ω/km
- Freileitung Al 70: R = 0,436 Ω/km, X = 0,309 Ω/km

Berechnung der Netzkurzschlussleistung am Anschlusspunkt:

1. Netzimpedanz: ZN = U² / SkVN = 400² V / 100 MVA = 1,6 mΩ
   - Mit R/X = 0,5: RN = 0,72 mΩ, XN = 1,43 mΩ

2. Transformatorimpedanz: ZT = U² / SkrT = 400² / 400 kVA = 16 mΩ
   - RT = U² × PCu / SkrT² = 4,6 mΩ
   - XT = √(ZT² – RT²) = 15,3 mΩ

3. Kabelimpedanz: XL = 16,4 mΩ, RL = 64 mΩ

4. Gesamtimpedanzen: XkV = 125,8 mΩ, RkV = 200,1 mΩ, ZkV = 236,4 mΩ
   - Kurzschlussleistung: SkV = U² / ZkV = 676,8 kVA

5. Spannungsänderung cos φ = 1: ua = 20 kW × 200,1 mΩ / (400 V)² = 2,5 %

6. Spannungsänderung cos φ = 0,90: ua = 20 kW × (200,1 mΩ × 0,9 – 125,8 mΩ × 0,44) / (400 V)² = 1,73 %

7. Bemessung der Betriebsmittel:
   - Scheinleistung: SAmax = 20 kW / 0,9 = 22,2 kVA
   - Maximaler Einspeisestrom: IAmax = 22,2 kVA / (√3 × 400 V) = 32,1 A

8. Kurzschlussstrom der PV-Anlage: 32 A

9. Netzrückwirkung (kimax = 1,2): ua = 1,2 × 22,5 kVA / 676,8 kVA = 4 %
   - Ergebnis: Schnelle Spannungsänderung im unzulässigen Bereich → genaue Betrachtung notwendig
   - Anschluss kann zugelassen werden, wenn Anlage der Standardkennlinie cos φ(P) entspricht

#### 26.3.16 Brennstoffzellen

Aufbau: Drei Bauteile — Brennstoffelektrode (Anode), Elektrolyt, Luft-/Sauerstoffelektrode (Kathode).
Reaktionsgleichung: H₂ + O → H₂O + 2e⁻

#### 26.3.17 Biogas und Biomasse

Für die Stromerzeugung aus Biomasse verwendete Brennstoffe: Biogas, Holz, Stroh, Hausmüll, Klärgas, Deponiegas.

Allgemeine Biomasse-Erzeugungsgleichung: H_m2O + CO₂ + YM + E → C_mkHmOn + H_m2O + O₂ + MB

#### 26.3.18 Biomasse-Berechnungsbeispiel: Dorf mit 15.000 Einwohnern

Ausgangsdaten: 12.000 Tonnen Biomasse/Jahr

1. Jährliche Energieproduktion:
   - 0,25 × 12.000 × 9 × 10⁹ / (3600 × 10³) kWh = 7,5 × 10⁶ kWh = 7500 MWh/Jahr

2. Generatorleistung bei Lastfaktor 80 %:
   - Betriebsstunden: 0,8 × 365 × 24 h = 7008 h/Jahr
   - Durchschnittliche Leistung: 7,5 × 10⁶ kWh / 7008 h = 1070 kW (Minimalwert für Generatorauslegung)

3. Gesamtleistungsbedarf des Dorfes (Haushalt 4000 kWh/a):
   - 15.000 × 4000 kWh = 60 × 10⁶ kWh = 60 MWh/Jahr

### 26.4 Energiespeicherung

#### 26.4.1 Druckluftspeicher

Druckluftspeicheranlagen nutzen in Kavernen oder Gasturbinen komprimierte Luft als Energiespeicher. Bei ausreichendem Energieangebot (Schwachlast) wird Druckluft eingespeichert; bei Spitzenlast steht diese Energie zur Turbinenbeschleunigung zur Verfügung.

#### 26.4.2 Lithium-Ionen-Batterien

Elektrochemische Stromquellen mit sehr hoher Energiedichte. Typische Anwendungsbereiche: Kameras, Laptop-Computer. Im Netzbereich zunehmend für stationäre Speicheranwendungen.

#### 26.4.3 Blei-Säure-Batterien

Weitverbreitetste Speichertechnologie:
- Energiedichte: ca. 40 kg/kWh oder 20 l/kWh
- Speichereffizienz: 80–90 %
- Lebensdauer: 3–12 Jahre
- Anwendungen: Fahrzeugstarterbatterien, Stabilisierung von Verteilnetzen

#### 26.4.4 Superkondensatoren

Arbeiten auf DC-Basis, sehr schnelle Energieaufnahme und -abgabe. Trotz geringer Energiedichte hohe Leistungsdichte. Wegen kleiner Einzelzellspannung werden sie in Reihe geschaltet, um die gewünschte Gesamtspannung zu erreichen.

### 26.5 Smart Grid

Ein Smart Grid ist ein elektrisches Netz, das sämtliche angeschlossene Akteure — Erzeuger, Verbraucher und Speicher — intelligent koordiniert, um Effizienz, Nachhaltigkeit, ökologische Verträglichkeit und Versorgungszuverlässigkeit zu gewährleisten.

### 27 Netzanschlussregeln

#### 27.1 Allgemeines zum Netzanschluss

Rechtlicher Rahmen: Energiewirtschaftsgesetz (EnWG).

Zentrale Paragraphen:
- § 1 EnWG: Gebot der sicheren, preisgünstigen und umweltverträglichen Stromversorgung im Allgemeininteresse
- § 4 EnWG: Versorgungspflicht der Elektrizitätsversorgungsunternehmen gemäß § 1
- § 6 EnWG: Randbedingungen für den verhandelten Netzzugang inkl. Netznutzungsentgelte
- § 10 EnWG: Pflicht der Energieversorgungsunternehmen zur öffentlichen Bekanntgabe allgemeiner Bedingungen und Tarife sowie zur diskriminierungsfreien Versorgung aller Anschlussnehmer in Niederspannung, soweit wirtschaftlich zumutbar

Planungsermessen des Netzbetreibers: Dieser hat prognostisches Ermessen bei Festlegung von Anschlussort und Spannungsebene. Ein Anschluss an beliebiger Netzstelle ohne Berücksichtigung der Netzauslastung kann aus dem EnWG nicht abgeleitet werden.

Bei bestehenden Anschlüssen: Anspruch auf Direktanschluss an höhere Spannungsebene besteht nicht, wenn der vorhandene Anschluss ausreichend dimensioniert ist. Änderungsanspruch entsteht nur bei Diskriminierung gegenüber anderen Kunden oder wenn der bestehende Anschluss die angemeldete Leistung nicht mehr übertragen kann.

Solidarprinzip: Kostenoptimierung einzelner Anschlussnehmer liegt nicht im Interesse der Gesamtheit. Netzbetreiber müssen gesamtwirtschaftlich planen. Verlagerung von NS-Ebene (Netzebene 7) in übergeordnete Netzebenen erhöht die Kosten für die verbleibenden NS-Nutzer.

Netzebenen-Systematik: Netzebene 1 (höchste) bis Netzebene 7 (niedrigste), jeweils durch Spannungsniveau definiert.

#### 27.2 Netzebene 7 (Niederspannungsnetz 400 V)

| Parameter | Wert/Eigentumsregel |
|-----------|---------------------|
| Anschlusspunkt | Ortsnetzkabel, Kabelverteilerschrank oder Station |
| Anschluss- und Hausanschlusskabel | Eigentum des Netzbetreibers |
| Zählung | beim Kunden |
| Eigentumsgrenze | Abgangsklemmen Hausanschlusskasten |
| Maximale Anschlussleistung | 0–199 kW, cos φ = 0,9 |

#### 27.3 Netzebene 6 (Umspannung 10/30 kV auf 400 V)

| Parameter | Wert/Eigentumsregel |
|-----------|---------------------|
| Anschlusspunkt | Ortsnetz-Transformatorstation, Abgangsklemmen 1-kV-Verteilung |
| Transformatorstation/Trafo | Eigentum des Netzbetreibers |
| Anschluss-/Installationskabel | Eigentum des Kunden, nur auf Kundengrundstück (nicht über öffentliche Verkehrsfläche) |
| Hausanschluss | nicht vorhanden bzw. Kundeneigentum |
| Zählung | in Station, an der Übergabe-Eigentumsgrenze |
| Eigentumsgrenze | NS-seitige Abgangsklemmen der Transformatorstation |
| Wartung Station | Netzbetreiber |
| Maximale Anschlussleistung | 200–399 kW, cos φ = 0,9 |

#### 27.4 Netzebene 5 (Mittelspannungsnetz 10–30 kV)

| Parameter | Wert/Eigentumsregel |
|-----------|---------------------|
| Transformatorstation | auf Kundengrundstück |
| Stationsgebäude und E-Anlagen | Kundeneigentum |
| Trafo | Kundeneigentum oder Miettrafo |
| Zählung | immer MS-Zählung an der Übergabestelle |
| 20-kV-Zuleitung | Eigentum des Netzbetreibers |
| NS-Kabel | nicht über öffentliche Verkehrsfläche |
| Wartung Station | durch Kunden |
| Anlagenverantwortliche Elektrofachkraft | stellt der Kunde |
| Eigentumsgrenze | 20-kV-Endverschluss des Zuleitungskabels |
| Maximale Anschlussleistung | 400–9.999 kW, cos φ = 0,9 |

Weitere Netzebenen:
- Netzebene 1: 380 kV und 220 kV
- Netzebene 2: Umspannung 380/220 kV auf 110 kV
- Netzebene 3: 110 kV
- Netzebene 4: Umspannung 110 kV auf 10–30 kV

#### 27.5 Kriterien für Anschluss in höherer Netzebene

Richtwert für Mittelspannungsanschluss: mindestens 350 kVA (abgeleitet aus Standardortsnetzstationsgröße ≥ 400 kVA und tatsächlicher Auslastung).

In Bereichen mit hoher Versorgungsdichte (Standardortsnetzstation > 400 kVA Bemessungsleistung) kann der Richtwert deutlich höher liegen.

Wechsel von Netzebene 7 in Netzebene 5 ist nur sinnvoll, wenn der Netzbetreiber-Richtwert überschritten wird und die Leistung aus dem NS-Netz nicht mehr bereitgestellt werden kann.

Ausnahmefälle (Abweichung von Richtwerten möglich):
- Anschlusssituation nicht vergleichbar mit Mehrheit der NS-Anschlüsse mit Leistungsmessung
- Spannungsqualitätsbeeinträchtigung in Netzebene 7 durch Netzrückwirkungen
- Betriebsmittel in Kundenanlage mit Spannungsanforderungen > 0,4 kV
- Zu erwartende Netzentwicklung unter Berücksichtigung der Anschlusspflicht

Maßgebliche Normen (Literaturhinweise): TAB Niederspannung, VDE-AR-N 4105 (Erzeugungsanlagen am NS-Netz), E VDE-AR-N 4100 (TAB NS).

### 28 Projektierung einer Industrieanlage

#### 28.1 Beschreibung der Anlage

Einspeisung: Transformatorstation mit 10-kV-Hochspannungsanschluss über Erdkabel.
Netzspannung: 400/230 V, 50 Hz.
Schutzmaßnahmen: (1) Abschaltschutz im TN-S-System, (2) Schutzpotentialausgleich und RCD.

Hauptverteilung (NSHV):
- Separater Neutral- und Schutzleiter
- Einspeisung von unten oder oben, Abgänge nach oben
- Licht- und Steckdosenstromkreise getrennt
- Jedes Kabel/Leitung an eigener gekennzeichneter Klemme (inkl. N und PE)
- Jeder Klemmensatz enthält Zu- und Abgangsklemmen sowie N-Trenn- und PE-Klemmen
- Maximaler Spannungsfall: Werte gemäß DIN VDE 0100-520, Tabelle G.52.1
- Spannungsfall Hauptzuleitung: maximal 1 %
- Zuleitung in Erde verlegt
- Transformatorstation: 150 m entfernt, Vorimpedanz 75 m

Elektroraum: Hauptverteiler als Standverteiler.
WC/Duschraum: 21-kW-Warmwasserdurchlauferhitzer installiert.
Motorantriebe bis 16 A: sicherungslose Abzweige; Wartungsschalter vorzusehen.
Gleichzeitiges Anlaufen bei Spannungswiederkehr: ausgeschlossen.
Verlegung: Stahlpanzerrohre von OK Fußboden bis 1,0 m darüber.
Einbauhöhen: Schalter 1,05 m, Steckdosen 0,30 m über Fertigfußboden.
Abzweigdosen: stets zugänglich.
Leitungsverlegung: Kabelkanal oder unter Putz.
Umgebungstemperatur: durchgehend 30 °C.

Geplante Erweiterung: Verbraucher 7,5 kW, 400 V, 50 Hz, cos φ = 0,82 am Westtor; Verlegeart B2, 5 Leitungen gehäuft, Temperaturerhöhung 40 °C.
Gleichzeitigkeitsfaktor Gesamtanlage: 0,65.

Beleuchtungsanlage: Deckenanbauleuchten innen, Feuchtraumleuchten an Ausgängen; Schaltung über Taster (Stromstoßschalter und Schütze).

Notbeleuchtung: EXIT-Leuchten in Dauerschaltung für Fluchtwege und Ausgänge; zusätzlich zwei Notlichtstrahler mit Steckdosen.

Potentialausgleichsanlage: Alle Metallkonstruktionen und Bauteile (Technikraum, WC, Dusche) in den Potentialausgleich nach DIN VDE 0100-540 und DIN VDE 0185 einbeziehen.

Erdungsanlage: Bandstahl 30 × 3,5 mm als Ringerder; Anschluss an Haupterdungsklemme (HEK); alle Heizungs- und Wasserleitungen mit HEK verbinden.

#### 28.2 Anzuwendende Vorschriften

- Elektrische Leitungsanlagen in Gebäuden: DIN 18382
- Technische Anschlussbedingungen (TAB)
- Unfallverhütungsvorschriften (DUVG Vorschrift 3)
- Elektrische Anlagen in Gebäuden: DIN 18015
- Blitzschutzanlagen: DIN VDE 0185
- Innenraumbeleuchtung mit künstlichem Licht: DIN 5035
- DIN VDE 0100, DIN VDE 0102, DIN VDE 0660-500, DIN VDE 0298-4, DIN VDE 0276-603 und -1000

Gültig sind alle Normen in neuester Ausgabe, einschließlich aller ab 01.01.2018 erschienenen Neufassungen, Bezugs- und Ersatznormen.

Vorgesehene Aufgaben (Projektierungsumfang):
1. Motor- und Geräteanschlüsse in Grundrissplan einzeichnen
2. Verbrauchertabelle vervollständigen
3. Normgerechter Übersichtsschaltplan der Transformatorstation
4. Normgerechter Übersichtsschaltplan der Hauptverteilung nach DIN 40719-5
5. Berechnung der Hauptleitungen
6. Prüfung der Wirksamkeit der Schutzmaßnahmen
7. Berechnung der Anschlussleistung der Anlage
8. Ermittlung der Leuchtenanzahl nach Wirkungsgradverfahren
9. Lichtinstallation vollständig in Grundrissplan übertragen
10. Ausbreitungswiderstand des Ringerders berechnen (ρE = 300 Ωm)
11. Blitzschutzanlage nach DIN VDE 0185 planen
12. Blindleistungskompensation für cos φ = 0,95 berechnen
13. Neue Transformatorstation 630 kVA, 4 %, 10/0,4 kV, 50 Hz planen
14. Notstromanlage 100 kVA planen

#### 28.3 Verbrauchertabelle

Vollständige Leistungsermittlung der Anlage (Tab. 28.1):

| Nr. | Gerät | Pab (kW) | cos φ | Pauf (kW) | Qzu (kvar) | IB (A) | Ie (A) | In (A) | S (mm²) |
|-----|-------|----------|-------|-----------|------------|--------|--------|--------|---------|
| 01 | Ventilator (8-pol) | 0,22 | 0,85 | 1,410 | 1,175 | 2,4 | 2,4 | 10 | 4 × 1,5 |
| 02 | Kompressor (2-pol) | 4 | 0,82 | 4,760 | 2,560 | 8,6 | 8,6 | 20 | 4 × 4 |
| 03 | Antrieb (4/2-pol) | 0,7 / 0,85 | 0,83 / 0,85 | 1,4 | 1,0 | 8,4 / 2,4 | — | 10 | 4 × 1,5 |
| 04 | Förderpumpe (4-pol) | 45 | 0,83 | 54,87 | 35,43 | 95,4 | 55,3 | 100 | 2 × 4 × 35 |
| 05 | Warmwasserspeicher | 21 | — | 21 | — | 30,3 | — | 35 | 5 × 10 |
| 06 | Schleifmaschine | 7,5 | 0,80 | — | 17,6 | 10,2 | — | 20 | 7 × 2,5 |
| 07 | Tischfräse | 2,5 | 0,78 | 2,49 | 5,65 | 5,65 | — | 10 | 7 × 4 |
| 08 | Sägemaschine | 5,5 | 0,85 | 4,27 | 11,7 | 4,7 | — | 16 | 7 × 4 |
| 09 | Waschplatz | 5,5 | — | 5,16 | — | 12,4 | — | 25 | 4 × 4 |
| 10 | Lüfter | 5,5 | 0,80 | 1,41 | 8,17 | — | — | 16 | 5 × 2,5 (3P+N+PE) |
| 11 | Steckdosen | — | — | 1,41 | 8,17 | — | — | 16 | 3 × 2,5 |
| 12 | Notlichtgerät 1 | 1,5 | — | — | 8,7 | — | — | 16 | 3 × 2,5 |
| 13 | Notlichtgerät 2 | 1,5 | — | — | 8,7 | — | — | 16 | 3 × 2,5 |
| 14 | Steckdosen | — | — | 0,84 | 6,1 | — | — | 16 | 3 × 2,5 |
| 15 | Steckdosen | — | 0,80 | 3,3 | 2,48 | 5,95 | — | 16 | 5 × 2,5 (3P+N+PE) |
| 16 | Hebebühne | 3,7 | 0,75 | 4,08 | 8,9 | 8,9 | — | 16 | 5 × 2,5 (3P+N+PE) |
| 17 | EXIT | 1,1 | — | — | — | — | — | 10 | 3 × 1,5 |
| 18 | Steckdosen | — | — | 1,41 | 8,17 | — | — | 16 | 3 × 2,5 |
| 19 | Beleuchtung (ganze Anlage) | — | 0,95 | — | — | — | — | 10 | 3 × 1,5 |
| 20 | Verbraucher Westtor | 7,5 | 0,82 | 5,23 | 16,1 | — | — | 20 | 5 × 6 |
| 21 | Heizung | 12 | — | — | 17,3 | — | — | 16 | 3 × 2,5 |

Summen:
- Zugeführte Gesamtwirkleistung: 142,65 kW
- Zugeführte Gesamtblindleistung: 82,78 kvar

#### 28.4 Berechnungen — Leistungsermittlung

Aus der Verbrauchertabelle ergibt sich:
- Blindleistungsbedarf: Qmax = 82,78 kvar
- Wirkleistung gesamt inkl. Heizung: 142,65 + 12 = 154,65 kW
- Leistungsfaktor der Gesamtanlage: tan φ = 82,78 / 154,65 = 0,535 → cos φ = 0,88
