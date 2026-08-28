# Lehrbuch der Bauphysik — Teil 3
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 121-160.

Dieser Teil des Lehrbuchs behandelt den Abschluss des Kapitels 5 (Wärme- und Energiebilanzen) mit den Themen Wärmespeicherfähigkeit, Anlagenaufwandszahl, Primärenergiefaktoren und das Berechnungsverfahren nach DIN V 18599 — sowie das vollständige Kapitel 6 zum instationären Wärmeverhalten von Bauteilen und Gebäuden inklusive sommerlichem Wärmeschutz und Einschwingvorgängen.

## Inhalt

### 5.3.4 Wärmespeicherfähigkeit

Die Wärmespeicherfähigkeit eines Gebäudes geht in zwei Berechnungsbereiche ein: die Bestimmung des Ausnutzungsgrades solarer und interner Wärmegewinne sowie die Berechnung der Energieeinsparung durch Nachtabschaltung.

#### 5.3.4.1 Ausnutzungsgrad der Wärmegewinne

Der Ausnutzungsgrad der Wärmequellen η hängt im Wesentlichen vom Verhältnis γ der Wärmequellen zu den Wärmesenken einer Gebäudezone ab:

- γ = Q_source / Q_sink (Formel 5.37)
- Die Zeitkonstante τ einer Gebäudezone ergibt sich aus dem Quotienten der wirksamen Wärmespeicherfähigkeit C_wirk [Wh/K] und dem Wärmetransferkoeffizienten H [W/K] (Formel 5.38), wobei H = HT + HV (Transmission + Lüftung).

Pauschalansätze für C_wirk nach DIN V 4108-6:
- Leichte Gebäude: C_wirk = 15 Wh/(m³·K) × Ve (Bruttovolumen)
- Schwere Gebäude: C_wirk = 50 Wh/(m³·K) × Ve

Detaillierte Berechnung nach Formel 5.39 durch Summation über alle raumluftberührenden Bauteilflächen: C_wirk = Σ(c_i · ρ_i · d_i · A_i)

Maßgebliche Rechenregeln für wirksame Schichtdicken d_i:
- Schichten mit Wärmeleitfähigkeit λ_i ≥ 0,1 W/(m·K), einseitig an Raumluft grenzend: Aufsummierung aller Schichten bis max. Gesamtdicke d_i,max = 0,10 m
- Innenbauteile (beidseitig an Raumluft): halbe Bauteildicke bei Dicke ≤ 20 cm, oder maximal 10 cm bei Dicke > 20 cm; bei mehreren Schichten beidseitig anwenden
- Schichten vor Wärmedämmschichten (z. B. Estrich auf Dämmung), λ_i ≥ 0,1 W/(m·K): nur Schichten bis zur Dämmschicht ansetzen. Als Dämmschicht gilt: λ_i < 0,1 W/(m·K) und R_i > 0,25 (m²·K)/W
- Außenbauteile: Fläche A_i über Außenmaße (Bruttofläche); Innenbauteile: Innenmaße (Nettofläche)

Die so ermittelte Wärmespeicherfähigkeit ist auch für die Einstufung in leichte, mittlere oder schwere Bauart nach DIN 4108-2 (sommerlicher Wärmeschutz) verwendbar.

#### 5.3.4.2 Nachtabschaltung

Energieeinsparung durch Nachtabschaltung wird über ein Detailverfahren ermittelt. Pauschalwerte für C_wirk,NA:
- Leichte Gebäude: C_wirk,NA = 12 Wh/(m³·K) × Ve
- Schwere Gebäude: C_wirk,NA = 18 Wh/(m³·K) × Ve

Bei Verwendung der detaillierten Berechnung: wirksame Schichtdicke der raumluftgrenzenden Schichten maximal 3 cm ansetzen.

Heizunterbrechungsdauer bei Wohngebäuden: 7 Stunden anzusetzen.

---

### 5.3.5 Anlagenaufwandszahl

Die Anlagenaufwandszahl beschreibt die energetische Effizienz der gesamten Versorgungskette — von der Energiequelle bis zur Nutzung im Gebäude.

Verlustarten in der Heizungskette (nach DIN V 4701-10):
- **Abgasverluste** bei fossiler Verbrennung
- **Erzeugungsverluste**: Wärmeabgabe des Kessels an Umgebung
- **Speicherverluste**: abhängig von Aufstellort und Dämmung
- **Verteilverluste**: abhängig von Rohrdämmung, Transportmediumtemperatur und Umgebungstemperatur
- **Übergabeverluste**: abhängig von Heizkörperanordnung und Regelungstechnik
- Hilfsenergie (Strom für Pumpen, Regelung) wird in die Bilanz einbezogen

Verluste für Lüftung und Trinkwarmwasserbereitung werden analog erfasst. Bei Zu-/Abluftanlagen mit Wärmerückgewinnung wird der zurückgewonnene Wärmeanteil aus der Abluft dem Gebäude gutgeschrieben. Wärmeverluste des Warmwasserspeichers und der Warmwasserleitungen können als nutzbare Wärme für die Raumheizung angerechnet werden.

**Drei Berechnungswege für die Anlagenaufwandszahl:**

1. **Diagrammverfahren** (DIN V 4701-10): Primärenergiebedarf in Abhängigkeit von Gebäudenutzfläche und Jahres-Heizwärmebedarf q_h für ein spezifiziertes Anlagensystem
2. **Tabellenverfahren**: Kenndaten von Standardprodukten aus Norm-Anhang; einfaches Schema; entspricht unterem energetischen Niveau marktüblicher Systeme
3. **Ausführliches Rechenverfahren**: Herstellerdaten des Wärmeerzeugers oder genaue Rohrleitungskenntnis erforderlich; führt in der Regel zu günstigeren Anlagenaufwandszahlen. Mischung der Verfahren möglich (z. B. Erzeugeraufwandszahl nach ausführlichem Verfahren, dann im Tabellenverfahren einsetzen)

**Beispiel-Anlagenkonfiguration (Tab. 5.4) nach DIN V 4701-10:**

| Bereich | Funktion | Konfiguration |
|---|---|---|
| Trinkwasser | Verteilung | innerhalb thermischer Hülle, mit Zirkulation |
| Trinkwasser | Speicherung | bivalenter Solarspeicher, innerhalb thermischer Hülle |
| Trinkwasser | Erzeugung | zentral, Brennwertkessel + Flachkollektor |
| Heizung | Übergabe | Radiatoren an Außenwand, Thermostatventile 1 K |
| Heizung | Verteilung | horizontal innerhalb thermischer Hülle, innenliegende Stränge, geregelte Pumpen |
| Heizung | Speicherung | keine |
| Heizung | Erzeugung | Brennwertkessel 55/45 °C, innerhalb thermischer Hülle |
| Lüftung | Übergabe | Lufttemperaturen < 20 °C |
| Lüftung | Verteilung | beheizt, Wärmerückgewinnung durch Wärmeübertrager |
| Lüftung | Erzeugung | Abluft/Zuluft mit WRG 80 %, Luftwechsel 0,4 h⁻¹, zentral, DC-Ventilatoren |

---

### 5.3.6 Energetische Bewertung von Anlagensystemen nach DIN V 18599

Alternativ zu DIN V 4701-10 ist eine Bewertung nach DIN V 18599 möglich. Dieses Verfahren ist komplexer und genauer, gilt für Alt- und Neubauten gleichermaßen. Ein Diagrammverfahren und die Anlagenaufwandszahl als Begriff sind darin nicht enthalten.

**Vergleich DIN V 4701-10 vs. DIN V 18599 (Tab. 5.5):**

| Aspekt | DIN V 4701-10 | DIN V 18599 |
|---|---|---|
| Bilanzverfahren | Monatsbilanz (baulich) | Monatsbilanz (baulich und anlagentechnisch) |
| Gewerketrennung | Heizwärmebedarf und Aufwandszahl getrennt | keine Trennung |
| Trinkwarmwasser-Nutzenergie | pauschal 12,5 kWh/(m²·a) | abhängig von Nettogrundfläche der versorgten Wohneinheiten |
| Interne Wärmeeinträge | pauschal 5 W/m² | nach Nutzung differenziert: EFH 1,9 W/m², MFH 3,8 W/m² |
| Energiebezug | Heizwert | Brennwert |
| Anlagentechnik-Wärmeeinträge | pauschal angenommen | iterativ ermittelt |
| Bestandsanlagen | in anderen Normenteilen / PAS | integriert |

---

### 5.3.7 Einflussgrößen auf den Primärenergiebedarf von Wohngebäuden

Ausgangsfall: Einfamilienhaus mit Q_P = 40,8 kWh/(m²·a) (Berechnungen nach DIN V 4108-6 + DIN V 4701-10)

#### 5.3.7.1 Bauliche Einflüsse

- Verbesserter baulicher Wärmeschutz: Reduktion um ca. 7 kWh/(m²·a)
- Schlechteres Wärmeschutzniveau: Erhöhung um ca. 7 kWh/(m²·a)
- Wärmebrückenkorrekturwert U_WB = 0 W/(m²·K) (optimierte Details): Q_P ≈ 37 kWh/(m²·a)
- Schlechte Wärmebrücken U_WB = 0,10 W/(m²·K): Anstieg um ca. 15 kWh/(m²·a) gegenüber dem obigen Wert
- Unzureichende Luftdichtheit (n = 0,7 h⁻¹ statt gefordert nach DIN 4108-7, ohne Zu-/Abluftanlage): Q_P = 59,5 kWh/(m²·a)
- Einfluss der Bauart (schwer/leicht) bei 7 Stunden Nachtabschaltung: ca. 4 % Vorteil für Schwerbauweise (pauschale Ansätze nach DIN V 4108-6)

#### 5.3.7.2 Anlagentechnische Einflüsse

- Niedertemperatur-Heizsystem statt Brennwert: Erhöhung um ca. 4 kWh/(m²·a)
- Rohrleitungen im nicht beheizten statt beheizten Bereich: Q_P = 44,7 kWh/(m²·a)
- Sole/Wasser-Wärmepumpe: Absenkung des Q_P um rd. 40 % (wegen geringerem Primärenergiefaktor für Strom)

#### 5.3.7.3 Nutzungsbedingte Einflüsse

- Berechnungs-Raumlufttemperatur-Standard: 19 °C (räumliche Teilbeheizung berücksichtigt)
- Mittlere Raumlufttemperatur 17 °C: Q_P = 32,1 kWh/(m²·a)
- Mittlere Raumlufttemperatur 21 °C: Erhöhung um ca. 10 kWh/(m²·a) bzw. rd. 24 % gegenüber Ausgangsfall
- Standortspezifische Klimadaten Mannheim (Region 12, Referenzort): Reduktion um ca. 10 kWh/(m²·a)
- Klimadaten Hof (Region 10, kälterer Standort): Q_P = 51,6 kWh/(m²·a)

---

### 5.3.5 / Tab. 5.3 Primärenergiefaktoren nach GEG 2020

Primärenergiefaktoren für den nicht erneuerbaren Anteil (auszugsweise):

| Energieträger / Kategorie | Primärenergiefaktor |
|---|---|
| Heizöl | 1,1 |
| Erdgas | 1,1 |
| Flüssiggas | 1,1 |
| Steinkohle | 1,1 |
| Braunkohle | 1,2 |
| Biogas | 1,1 |
| Bioöl | 1,1 |
| Holz | 0,2 |
| Netzstrom | 1,8 |
| Strom gebäudenah (PV oder Wind) | 0,0 |
| Verdrängungsstrommix für KWK | 2,8 |
| Erdwärme, Geothermie, Solarthermie, Umgebungswärme | 0,0 |
| Erdkälte, Umgebungskälte | 0,0 |
| Abwärme | 0,0 |
| Wärme aus gebäudeintegrierter KWK | nach DIN V 18599-9:2018-09, Verfahren B |
| Siedlungsabfälle | 0,0 |

Erläuterung: Der Primärenergiefaktor für Holz beträgt 0,2, weil der im Holz gespeicherte Energieinhalt als erneuerbarer Anteil gilt (nachwachsend) — nur Aufbereitungs- und Transportaufwand (20 %) zählen als nicht erneuerbar. Für Heizöl EL bedeutet der Faktor 1,1, dass bei der Bereitstellung von 1 Liter Heizöl (Förderung, Raffination, Transport) zusätzlich 10 % Primärenergie aufgewendet werden.

---

### 5.4 Gebäudebilanzen für Nichtwohngebäude (DIN V 18599)

Berechnungsverfahren nach DIN V 18599 ermöglicht die Beurteilung aller Energiemengen für Heizung, Warmwasserbereitung, raumlufttechnische Konditionierung und Beleuchtung. Gegenseitige Beeinflussung von Energieströmen wird berücksichtigt. Nutzungsrandbedingungen sind normativ festgelegt (unabhängig von individuellem Nutzerverhalten und lokalen Klimadaten).

Anwendbar für:
- Wohn- und Nichtwohnbauten
- Neubauten und Bestandsbauten

Einsatzzwecke:
- Öffentlich-rechtlicher Nachweis nach GEG (mit teilweise festgelegten Randbedingungen)
- Allgemeine ingenieurmäßige Energiebedarfsbilanzierung (frei wählbare Randbedingungen)
- Bedarfs-Verbrauchs-Abgleich (frei wählbare Randbedingungen)

DIN V 18599 besteht aus 13 Teilen:
- Teil 1: Allgemeine Bilanzierungsverfahren, Begriffe, Zonierung und Energieträgerbewertung
- Teil 2: Nutzenergiebedarf für Heizen und Kühlen von Gebäudezonen
- Teil 3: Nutzenergiebedarf für energetische Luftaufbereitung
- Teil 4: Nutz- und Endenergiebedarf für Beleuchtung
- Teil 5: Endenergiebedarf von Heizsystemen
- Teil 6: Endenergiebedarf von Wohnungslüftungsanlagen und Luftheizungsanlagen (Wohnungsbau)
- Teil 7: Endenergiebedarf von Raumlufttechnik- und Klimakältesystemen (Nichtwohnungsbau)
- Teil 8: Nutz- und Endenergiebedarf von Warmwasserbereitungssystemen
- Teil 9: End- und Primärenergiebedarf von KWK-Anlagen
- Teil 10: Nutzungsrandbedingungen, Klimadaten
- Teil 11: Gebäudeautomation
- Teil 12: Tabellenverfahren Wohngebäude
- Teil 13: Tabellenverfahren Nichtwohngebäude

#### 5.4.1 Energiebedarf des Gebäudes (Teil 1)

Endenergien werden nach Energieträgern (Strom, Brennstoffe, Fern-/Nahwärme) getrennt ausgewiesen. Gesamte Endenergie eines Nichtwohngebäudes:

Q_f = Q_h,f + Q_h*,f + Q_c,f + Q_c*,f + Q_m*,f + Q_w,f + Q_l,f + W_f

| Symbol | Einheit | Bedeutung |
|---|---|---|
| Q_h,f | kWh/a | Endenergie Heizsystem |
| Q_h*,f | kWh/a | Endenergie RLT-Heizfunktion |
| Q_c,f | kWh/a | Endenergie Kühlsystem |
| Q_c*,f | kWh/a | Endenergie RLT-Kühlfunktion |
| Q_m*,f | kWh/a | Endenergie Befeuchtung |
| Q_w,f | kWh/a | Endenergie Trinkwarmwasser |
| Q_l,f | kWh/a | Endenergie Beleuchtung |
| W_f | kWh/a | Endenergie Hilfsenergien |

Brennwertbezogener Primärenergiebedarf: Q_p,HS = Σ(Q_f,j × f_p,j) über alle Energieträger j.

#### 5.4.2 Nutzenergiebilanz einer Gebäudezone (Teil 2)

Grundlage für Heizwärme- und Kältebedarf. Wärmebedarf ergibt sich aus Wärmesenken (z. B. Transmissionsverluste) und mit Ausnutzungsgrad gewichteten Wärmequellen (z. B. Solargewinne). Ausnutzungsgrad abhängig von Verhältnis Quellen/Senken und thermischer Masse. Kühlbedarf = Anteil der für Heizzwecke nicht nutzbaren Wärmeeinträge, die durch Kühlung abgeführt werden müssen.

#### 5.4.3 Nutzenergiebilanz der Luftaufbereitung (Teil 3)

Energieaufwand für Konditionierung von Außenluft auf Zuluftbedingungen (Erwärmen, Kühlen, Befeuchten). Für Standardanlagen (von einfacher Zu-/Abluft mit Vorerwärmung bis zur Vollklimaanlage mit Wärmetauscher, Vorheizung, Kühlung, Befeuchtung und Nachheizung) sind spezifische Aufwände in tabellarischer Form in der Norm hinterlegt. Mit Kenntnis von Zuluftvolumenströmen, Zulufttemperaturen und Betriebszeiten einfache Quantifizierung möglich.

#### 5.4.4 Beleuchtung (Teil 4)

Endenergiebedarf für Beleuchtung Q_l,f (Formel 5.42):

Q_l,f = p · [a_TL · (t_eff,Nacht + t_eff,Tag,TL) + a_KTL · (t_eff,Nacht + t_eff,Tag,KTL)]

| Symbol | Einheit | Bedeutung |
|---|---|---|
| p | W/m² | spezifische elektrische Bewertungsleistung |
| a_TL | m² | Teilfläche mit Tageslichtversorgung |
| a_KTL | m² | Teilfläche ohne Tageslichtversorgung |
| t_eff,Tag,TL | h | effektive Betriebszeit im tageslichtversorgten Bereich, Tagzeit |
| t_eff,Tag,KTL | h | effektive Betriebszeit im nicht tageslichtversorgten Bereich, Tagzeit |
| t_eff,Nacht | h | effektive Betriebszeit, Nachtzeit |

Unterscheidung: Bereich mit Tageslichtöffnung (Fensterfläche) vs. innenliegender Flur ohne Tageslicht. Tagzeit = Zeitraum zwischen Sonnenaufgang und Sonnenuntergang. Effektive Betriebszeiten berücksichtigen Tageslichtnutzungsgrad, Sonnen-/Blendschutzvorrichtungen und Steuerungsmöglichkeiten.

#### 5.4.5 Heizung und Warmwasserbereitung (Teil 5 / 8)

Verfahren analog dem in Abschn. 5.3 beschriebenen, mit Unterschieden gemäß Tab. 5.5 (Brennwertbezug statt Heizwertbezug, iterative Wärmeeintrag-Bestimmung).

#### 5.4.6 Raumlufttechnik- und Klimakältesysteme (Teil 7)

Ausgehend von Nutzenergiebedarf Raumkühlung (Teil 2) und Außenluftaufbereitung (Teil 3) werden Übergabe- und Verteilverluste berechnet. Endenergie für Klimakälte über Kennwerttabellen:
- Nennkälteleistungszahl (EER)
- Mittlerer Teillastfaktor (PLV), ermittelt aus stündlichen Berechnungen des Teilllastverhaltens

Dampfbefeuchtungssysteme: Kennwerte nach Dampferzeugungsart für Endenergie-Berechnung.

#### 5.4.7 Nutzungsrandbedingungen (Teil 10)

Erstmals normativ: Richtwerte für 43 Nutzungsarten in einer Tabelle. Enthält:
- Nutzungs- und Betriebszeiten
- Beleuchtungsrandbedingungen
- Raumklimarandbedingungen
- Wärmequellen
- Nutzenergiebedarf Trinkwarmwasser (für ausgewählte Nutzungen)

#### 5.4.8 Gebäudeautomation (Teil 11)

Einfluss von Steuerung, Regelung und Gebäudeautomation auf den Energiebedarf. Automationsklassen umfassen Steuer-, Regel- und Automationsfunktionen für Heizungs-, Trinkwarmwasser-, Lüftungs-, Klima- und Beleuchtungsanlagen.

#### 5.4.9 Tabellenverfahren (Teile 12 und 13)

Teil 12: Bewertung von Neu- und Bestandsbauten im Wohngebäudebereich (mit Einschränkungen gegenüber dem allgemeinen Verfahren).

Teil 13: Anwendbar für einzonige, ungekühlte Nichtwohngebäude mit Nettogrundfläche ≤ 5000 m², zulässige Gebäudetypen:
- Bürogebäude (ggf. mit Verkauf, Gewerbebetrieb oder Gaststätte)
- Groß- und Einzelhandel max. 1000 m² NF (nur mit Büro-, Lager- oder Verkehrsflächen als Nebennutzung)
- Gewerbebetriebe max. 1000 m² NF (nur mit Büro-, Lager-, Sanitär- oder Verkehrsflächen als Nebennutzung)
- Schulen, Turnhallen, Kindergärten und -tagesstätten
- Beherbergungsstätten ohne Schwimmhalle, Sauna oder Wellnessbereich
- Bibliotheken

---

## Kapitel 6: Instationäres Wärmeverhalten von Bauteilen und Gebäuden

### 6.1 Instationäres Wärmeverhalten von Bauteilen

Stationäre Wärmeleitung setzt gleichbleibende Temperaturen auf beiden Seiten und keine Wärmequellen/-senken im Bauteil voraus — Bedingungen, die im Baupraxis kaum eingehalten werden. Instationäre Randbedingungen entstehen durch:
- Tagesgang der Solarstrahlung und Außenlufttemperatur
- Zeitlich variable interne Wärmequellen
- Unterschiedliches Lüftungsverhalten
- Unterbrochener Heizbetrieb (Nachtabschaltung oder -absenkung)

Berechnung des Wärmetransports unter Berücksichtigung des Wärmespeicherterms nach der 1-dimensionalen Fourierschen Differentialgleichung ohne Quellterm (Formel 6.1):

ρ · c · ∂θ/∂t = ∂/∂x(λ · ∂θ/∂x)

#### 6.1.1 Wärmespeicherung

Baukonstruktionen und Einrichtungsgegenstände nehmen bei Erwärmung Wärme auf und geben sie bei Abkühlung ab. Die Fähigkeit zur Wärmeaufnahme hängt ab von:
- Spezifischer Wärmekapazität c des Materials
- Masse (Rohdichte ρ) des Materials
- Temperaturdifferenz zwischen Bauteil und Umgebung

Gespeicherte Wärmemenge (Formel 6.2): Q = c · ρ · V · Δθ

**Spezifische Wärmekapazität und Rohdichte ausgewählter Baumaterialien (Tab. 6.1):**

| Material | c [Wh/(kg·K)] | ρ [kg/m³] | c·ρ [Wh/(m³·K)] |
|---|---|---|---|
| Wasser | 1,163 | 1000 | 1163 |
| Beton | 0,278 | 2400 | 667 |
| Hartschaum | 0,403 | 35 | 14 |
| Holz | 0,444 | 700 | 311 |
| Luft | 0,278 | 1,23 | 0,34 |

Weitere Stoffdaten in DIN EN ISO 10456 und VDI-Wärmeatlas. Begriff „Rohdichte" in der Bauphysik: Masse eines porösen Materials bezogen auf das Gesamtvolumen einschließlich Poren und Hohlräume.

**Praxisbeispiele für Wärmespeicherung:**
- 1 m³ Luft benötigt eine Temperaturerhöhung von 294 K, um 100 Wh zu speichern
- 1 m³ Beton: nur 0,14 K Temperaturveränderung bei 100 Wh Wärmezufuhr
- 30 cm Betonbauteil: ca. 2,0 kWh/m² für Temperaturerhöhung von 10 °C auf 20 °C
- 4 cm Hartschaum: ca. 0,04 kWh/m² für dieselbe Temperaturerhöhung
- Beton (30 cm Kern) + beidseitig 4 cm Hartschaum: ca. 2,01 kWh/m² — Beton dominiert die Speicherfähigkeit

#### 6.1.2 Vergleich von Konstruktionen — Auf- und Abheizverhalten

Drei exemplarische Konstruktionen für Innen- und Außenwand:
1. Massivbeton (schwer)
2. Dämmstoff (leicht)
3. Betonkern mit beidseitiger Dämmschicht (geschichtet)

**Aufheizverhalten Innenwand (sprunghafter Temperaturanstieg von 10 °C auf 20 °C):**
- Beton: Kerntemperatur nach 2 Stunden nahezu unverändert; Oberflächentemperatur steigt langsam; erst nach ca. 48 h wird Raumlufttemperatur annähernd erreicht
- Dämmstoff: Reaktion sehr schnell; bereits nach 1 Stunde auch im Kern annähernd Raumlufttemperatur
- Beton + Dämmstoff: schneller Temperaturanstieg an Oberflächen; Kern auch nach 48 h noch sehr niedrig

**Auskühlverhalten Innenwand:** Umgekehrte Verläufe — schwere Konstruktion träge, leichte und geschichtete schnell reagierend an Oberflächen

**Periodische Randbedingungen Innenwand:**
- Beton: Temperaturschwankung im Kern und an Oberfläche max. ±3 K gegenüber Mitteltemperatur 20 °C
- Dämmstoff (leicht): sehr große Temperaturschwankungen im Kern und besonders an Oberflächen
- Geschichtete Konstruktion: äußerst geringe Schwankungen im Kern; Oberflächen folgen Raumlufttemperatur schnell

**Außenwand-Aufheizverhalten:**
- Stahlbeton: raumseitige Oberflächentemperatur im Ausgangszustand vergleichsweise niedrig; langsamer Temperaturanstieg bei Heizung
- Dämmstoff: schnelle Reaktion der raumseitigen Oberfläche; nach kurzer Zeit nahe Raumlufttemperatur
- Geschichtete Konstruktion: Oberflächentemperaturen nahe Umgebungstemperatur; Kerntemperatur schwankt wenig

**Praktische Schlussfolgerungen:**
- Für Wärmespeicherfähigkeit bei instationären Bedingungen: Materialschichten an der Bauteiloberfläche sind entscheidend
- Bei instationärem Heizbetrieb (Nachtabschaltung): leichte Konstruktion vorteilhaft — geringer Wärmeeintrag zum Aufwärmen, Oberflächentemperatur erreicht schnell behagliche Werte; beim Absenken schnelles Abfallen, wenig Entspeicherung → geringerer Energiebedarf für Raumheizung
- Nachtabsenkung/-abschaltung bei Wohngebäuden: üblicherweise 8 Stunden; Bürogebäude: bis 14 Stunden. Geschichtete Konstruktion verhält sich dabei bezüglich Wärmeaufnahme ähnlich wie ein leichtes Bauteil
- Im Sommer: Betonkonstruktion günstiger — solare Wärmeeinträge können in die schwere Masse eingespeichert werden, was Raumlufttemperaturen dämpft

---

### 6.2 Instationäres Heizen und Überheizungseffekte

Der U-Wert beschreibt den Wärmedurchgang unter stationären Bedingungen. Wärmespeicherfähigkeit und Masse des Bauteils gehen nicht in den U-Wert ein. Solare Einstrahlung auf Außenbauteile während der Heizperiode ist im U-Wert nicht berücksichtigt.

Bei Außenwänden unterschiedlicher Masse, aber gleichem U-Wert, unter Einfluss von Sonneneinstrahlung an einem strahlungsreichen Wintertag (DIN 4710):
- Leichte Konstruktion (I): ausgeprägter Tagesgang der Wärmestromdichte an der Innenseite
- Schwere Konstruktionen: vergleichsweise geringe Schwankungen
- Tagesmittelwert der Wärmestromdichte ist bei allen Bauarten identisch: 5,2 W/m²

Fazit: Transmissionswärmestrom durch opake Außenbauteile bei gleichen stationären oder instationären Randbedingungen korrekt durch U-Wert beschreibbar — gilt für schwere und leichte Bauweise. Ausnahme: aperiodische Randbedingungen (z. B. plötzlicher Kälteeinbruch): schwere Wand bleibt länger wärmer, Wärmeverluste steigen langsamer. Beim Witterungsumschwung kehrt sich der Effekt um; im Mittel kein Unterschied.

**Überheizungseffekte (abhängige Raumtemperatur):**

Wenn Raumtemperatur von der Bauart abhängt (Überheizung durch Solare Einstrahlung oder Nachtabsenkung), gelten nicht mehr identische Randbedingungen. Primär die thermisch aktivierbare Masse der Innenbauteile (nicht der Außenwand) spielt die wesentliche Rolle.

Beispiel Tagesgang (Sollwert tagsüber 20 °C, ab 22:00 Nachtabsenkung):
- Schwere Konstruktion: Nachtabsenkung bis 17,3 °C; Überheizung (ab ca. 14:00 Uhr) bis 21 °C
- Leichte Konstruktion: Nachtabsenkung bis 16,3 °C; Überheizung bis 21,7 °C
- Operative Temperatur (Mittelwert aus Oberflächen- und Raumlufttemperatur) steigt bei Leichtbau schneller und erreicht höheres Tagesmaximum

Einflüsse auf Überheizung:
- Solarstrahlungsangebot (Standort)
- Fenstergröße und Vorhandensein/Betätigung von Verschattung
- Wärmeschutzniveau und Lüftungswärmeverluste (schlechtes Wärmeschutzniveau + hoher Lüftungswärmeverlust = weniger ausgeprägte Überheizung)

Wirkung der Nachtabsenkung abhängig von:
- Dauer der Heizunterbrechung: Wohnungsbau meist 8 Stunden, Bürobau bis ca. 14 Stunden
- Wärmeschutzniveau: schlechter = stärker wirkende Nachtabsenkung
- Wärmespeicherfähigkeit: schwere Bauteile kühlen langsamer, Raumlufttemperatur sinkt nicht so tief
- Thermische Trägheit des Heizsystems

Praxisregel: Ohne Überheizung + Nachtabsenkung → Leichtbauweise energetisch günstiger. Ohne Nachtabsenkung + mit Überheizungen → Schwerbauweise günstiger. Entscheidend ist das Verhältnis Wärmeverluste zu Wärmegewinnen (solar + intern): Je kleiner dieses Verhältnis, desto günstiger die Schwerbauweise. Milde Winter → Schwerbauweise vorteilhaft; kalte Winter → Leichtbauweise vorteilhaft.

---

### 6.3 Sommerliches Wärmeverhalten

#### 6.3.1 Einschwingvorgang

Einflussfaktoren auf sommerliches Wärmeverhalten:

**Von außen:**
- Solarstrahlung (direkt, diffus, reflektiert)
- Außenlufttemperatur

**Von innen:**
- Interne Wärmequellen (Personen, Geräte)

Physikalische Vorgänge:
- Sonneneinstrahlung trifft auf Gebäudehüllfläche → teilweise Reflexion, teilweise Absorption → absorbierter Anteil wird zu Wärme umgewandelt → Abgabe nach außen (Konvektion, Strahlung) und Leitung in Bauteil
- Bei transparenten Bauteilen: direkter Strahlungsdurchtritt ins Gebäudeinnere → Absorption durch Raumumschließungsflächen

**Gesamtenergiedurchlassgrad g (g-Wert):** Verhältnis von in den Raum gelangender Energie zur gesamten auf das Glas treffenden Sonnenenergie. Hängt von Glasart ab:
- Sonnenschutzglas: g ≈ 0,25
- Standard Wärmeschutzglas: g bis ca. 0,7

**Abminderungsfaktor F_C** für Sonnenschutzvorrichtungen (Tab. 6.2, Werte aus DIN 4108-2):

Innen liegende / zwischen Scheiben liegende Vorrichtungen:
| Glastyp | Ohne Schutz | Innenrollo / Innenjalousie | Rollo zwischen Scheiben |
|---|---|---|---|
| 2-fach WDG | 1,0 | 0,65–0,85¹ | – |
| 3-fach WDG | 1,0 | 0,70–0,90¹ | – |
| 2-fach SSG | 1,0 | 0,65–0,90¹ | – |

Außen liegende Vorrichtungen:
| Glastyp | Jalousie/Raffstore 45° | Jalousie 10° | Rollläden/Klappläden (geschlossen) | Markise parallel zum Glas |
|---|---|---|---|---|
| 2-fach WDG | 0,25 | 0,15 | 0,10 | 0,25 |
| 3-fach WDG | 0,25 | 0,15 | 0,10 | 0,25 |
| 2-fach SSG | 0,30 | 0,20 | 0,15 | 0,30 |

¹ Werte abhängig von Farbe und Transparenz der Schutzvorrichtung
WDG = Wärmedämmglas; SSG = Sonnenschutzglas

Genauere Kennwerte mit DIN EN ISO 52022-1 und -2 bestimmbar.

Strahlungsbelastung vertikaler Fenster: Ost- und Westorientierung > Südorientierung im Sommer; Nordfassade empfängt am wenigsten.

Außenlufttemperatur: beeinflusst konvektive Wärmeabgabe der Außenbauteile und Lüftungsrichtung — bei Nacht (Außenluft < Raumluft) wird Wärme abgeführt, tagsüber (Außenluft > Raumluft) wird Wärme zugeführt.

Interne Wärmequellen: können fallweise dominieren (z. B. Serverraum), spielen im üblichen Wohn- und Bürobau meist untergeordnete Rolle.

**Einschwingvorgang (Beschreibung):**
Nach einer Schlechtwetterperiode (geringe Strahlung, niedrige Außentemperaturen) steigt bei Schönwetterbeginn die mittlere Raumlufttemperatur exponentiell an, die Tages-Temperaturschwankung wird größer. Theoretisch eingeschwungen nach unendlich vielen Tagen; praktisch nach Abklingen von 90 % des Einschwingvorgangs in 2 bis 12 Tagen. Temperaturschwankungsbreite im Tagesgang bleibt während des gesamten Einschwingvorgangs annähernd konstant. Im eingeschwungenen Zustand hängt die Mitteltemperatur bei Räumen ohne nennenswerte interne Wärmeeinträge vom Fenster-Strahlungseintrag und den Lüftungs-/Transmissionswärmeströmen ab.

#### 6.3.2 Auswirkung von Einflussgrößen auf die Raumtemperatur im Sommer

Untersuchungsparameter für ein Einzonenmodell (Prüfraum nach DIN EN ISO 13791):

| Parameter | Varianten |
|---|---|
| Sonnenschutz | ohne; ideal (g_total = 0); real (F_C = 0,2) |
| Luftwechsel Tag/Nacht | 0,5/0,5 h⁻¹; 5/5 h⁻¹; 0,5/5 h⁻¹ |
| Fensterflächenanteil | 30; 50; 70; 100 % der Fassade |
| Interne Wärmequellen | 0; 50; 100 Wh/(m²·d) |
| Bauart | leicht; schwer |
| Fassadenorientierung | Nord; Ost; Süd; West |

**Geometrie des Prüfraum-Einzonenmodells (Tab. 6.3 und 6.4):**
- Maße: B = 3,6 m, L = 5,5 m, h = 2,8 m
- Fassadenfläche (gesamt): 10,1 m²
- Nutzfläche: 19,8 m²
- Volumen: 55,4 m³
- Außenwand: U = 0,28 W/(m²·K), Absorptionsgrad α = 0,5
- Fenster: U = 1,3 W/(m²·K), g⊥ = 0,60

**Ergebnisse der Parameterstudien (Einschwingverhalten über 20 Tage):**

Sonnenschutz: elementar bedeutsam. Mit realem Sonnenschutz (F_C = 0,2, permanent geschlossen): Tagesmitteltemperatur rd. 31 °C, nahe Außentemperaturniveau. Ohne Sonnenschutz: unvertretbar hohe Temperaturen. Bei idealem Sonnenschutz (F_C = 0): Anstieg resultiert ausschließlich aus erhöhter Außenlufttemperatur.

Luftwechsel: Einschwingverhalten und eingeschwungenes Niveau stark beeinflusst. Erhöhter Luftwechsel senkt Tagesmitteltemperatur. Hoher Tagesluftwechsel kann in den ersten 4 Tagen einer Schönwetterperiode Tagesmaximum erhöhen (Wärmeeintrag in noch kühles Gebäude). Tägliche Temperaturschwankung nimmt mit steigendem Luftwechsel zu. Nächtlicher Luftwechsel bei gleichzeitig geringem Tagesluftwechsel führt zu niedrigsten Raumtemperaturen und kleinster Tages-Schwankung → grundsätzlich anzustreben.

Interne Wärmequellen: Unterschied von jeweils 50 Wh/(m²·d) führt im eingeschwungenen Zustand zu Temperaturdifferenz von rd. 2 K.

Normative interne Wärmequellen für Wohngebäude:
- Einfamilienhaus: 50 Wh/(m²·d) (Belegungsdichte 45 m²/Person, Gesamtfläche 135 m², 3 Personen, 282 W · 24 h/d / 135 m²; Waschmaschine, Trockner und separater Kühlschrank im Keller)
- Mehrfamilienhaus: 100 Wh/(m²·d) (Belegungsdichte 35 m²/Person, Gesamtfläche 70 m², 2 Personen)
- Einzelbüroraum: mittlerer Wärmeeintrag (Personen + Arbeitsmittel Computer/Bildschirm/Drucker + Beleuchtung) rd. 120 Wh/(m²·d)

Hinweis: Einsatz stromsparender Elektrogeräte verbessert nicht nur Energieeffizienz, sondern auch sommerliches Wärmeverhalten von Aufenthaltsräumen.

Fenstergröße: Mit zunehmendem Fensterflächenanteil steigt Temperaturniveau der Raumluft sowohl während des Einschwingvorgangs als auch im eingeschwungenen Zustand.
