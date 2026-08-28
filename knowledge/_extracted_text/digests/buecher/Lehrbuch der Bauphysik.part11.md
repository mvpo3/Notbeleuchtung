# Lehrbuch der Bauphysik — Teil 11
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 441-480.

Dieser Teil schließt Kapitel 16 „Komponenten des Außenklimas" ab. Behandelt werden langwellige Abstrahlung geneigter Flächen, Wasserdampfdruck und relative Luftfeuchte, Niederschlag und Wind, Schlagregenberechnung an Gebäudeoberflächen, Testreferenzjahr (TRY) sowie ein softwarebasierter Klimagenerator. Der Autor ist P. Häupl (TU Dresden).

## Inhalt

### 16.2 (Fortsetzung) — Langwellige Abstrahlung horizontaler und geneigter Flächen

- Die langwellige Gesamtabstrahlung einer horizontalen Bauteilfläche ergibt sich aus dem Produkt von Emissionskoeffizient des Bauteils (εB = 0,94), der Stefan-Boltzmann-Konstante (σ = 5,67 × 10⁻⁸ W/m²K⁴), der Bauteiloberflächentemperatur in der vierten Potenz, abzüglich der langwelligen Himmelsgegenstrahlung (Formel 16.26).
- Für geneigte und vertikale Flächen fällt der langwellige Strahlungsverlust geringer aus als bei Horizontalflächen. Grund: Mit zunehmendem Neigungswinkel α (Winkel zwischen Flächennormale und Vertikaler) nimmt der „Sichtanteil" des Himmels ab, während der Anteil gegenüberliegender Gebäude und Bewuchs mit ε ≈ 0,94 zunimmt. Der korrigierte Gesamtabstrahlungswert ergibt sich aus der Formel 16.27, in der der Faktor (0,4 + 0,6 · cos³ α) die Winkelabhängigkeit beschreibt.
- In Mitteleuropa bewegt sich die langwellige Gesamtabstrahlung horizontal zwischen 0 W/m² (bedeckter Himmel im Winter) und −170 W/m² (klarer Himmel im Sommer).
- Jahresmittelwerte der langwelligen Abstrahlung:
  - Cottbus 2014: −46,7 W/m²
  - Dresden 1997: −52,9 W/m²
  - Dresden-Klotzsche (1981–1990): −49,2 W/m²
- Bei vertikalen Flächen sinkt der Maximalwert auf −60 W/m².
- Die langwellige Abstrahlung hängt stark von der Temperatur (über das Stefan-Boltzmann-Gesetz) und dem Bedeckungsgrad ab; der Einfluss der relativen Luftfeuchte (Streuung an Wasserdampfmolekülen) ist schwächer.

### 16.3 — Wasserdampfdruck und relative Luftfeuchtigkeit

Außen- und Raumluft enthalten stets Wasserdampf — ein unsichtbares, geruchloses und ungiftiges Gas. Der Dampfgehalt wird entweder als Massenverhältnis x (kg Wasserdampf / kg Luft) oder als Partialdruck pD (Pa) angegeben. Die relative Luftfeuchte ϕ ist das Verhältnis von tatsächlichem Wasserdampf-Partialdruck pD zum temperaturabhängigen Sättigungsdruck ps (Gl. 16.32).

#### 16.3.1 — Wasserdampfsättigungsdruck

- Der Sättigungsdruck ps ist stark temperaturabhängig und folgt unterschiedlichen Gesetzmäßigkeiten je nach Temperaturbereich:
  - Für θ < 0 °C (Sublimationskurve): Formel 16.29 — ps(θ) = 610,5 · exp(21,87θ / (265,5 + θ)) bzw. alternative Darstellung mit dem Faktor 148,57 und Exponent 12,3.
  - Für θ > 0 °C (Sättigungsdruckkurve): Formel 16.30 — ps(θ) = 610,5 · exp(17,26θ / (237,3 + θ)) bzw. alternative Darstellung über den Faktor 109,8 und 8,02.
  - Beide Bereiche sind mittels Sprungfunktion in Gl. 16.31 zusammengefasst, die den Jahresverlauf des Sättigungsdrucks in der mitteleuropäischen Atmosphäre beschreibt.
- Der Jahresverlauf des Sättigungsdrucks in der Außenluft folgt der Außentemperaturkurve: hohe Werte im Sommer, geringe Werte im Winter.

#### 16.3.2 — Relative Luftfeuchtigkeit

- Die relative Luftfeuchte ϕ ist das Verhältnis pD / ps (Gl. 16.32).
- Für den Jahresgang in Dresden 1997 wurde eine harmonische Näherungsfunktion (Gl. 16.33) angepasst:
  - Jahresmittelwert ϕ₀ = 78 %
  - Amplitude Δϕ = 11 %
  - Jahreszeitverschiebung tα = −5 Tage
- Im Winter ist die relative Luftfeuchte der Außenluft grundsätzlich hoch (niedriger Sättigungsdruck bei tiefen Temperaturen). Im Sommer schwankt sie zwischen 25 % und 100 %, da der Sättigungsdruck größeren tagestemperaturbedingten Variationen unterliegt.

#### 16.3.3 — Tatsächlicher Wasserdampfdruck (Partialdruck)

- Der tatsächliche Partialdruck des Wasserdampfes pD(t) ergibt sich nach Gl. 16.34a und 16.34b aus dem Produkt von Sättigungsdruck und relativer Luftfeuchte (mit Faktor 0,01 für den Prozentbezug).
- Für das Analytische Referenzklima ARY (Gl. 16.35) gelten folgende Kennwerte für den Partialdruck-Jahresgang:
  - Jahresmittelwert pem = 1290 Pa
  - Druckamplitude des Jahresganges Δpea = 580 Pa
  - Jahreszeitverschiebung ta = 15 Tage
  - Witterungsbedingte Amplitude Δpp = 500 Pa
  - Tagesamplitude Δped = 200 Pa
- Übersteigt der berechnete Partialdruck den Sättigungsdruck, wird mittels der Heavisidschen Sprungfunktion Φ pD auf ps gesetzt (Gl. 16.36).
- Die relative Luftfeuchte des Referenzklimas ARY folgt aus pD / ps (Gl. 16.37), multipliziert mit 100 für den Prozentwert.
- Während eines Niederschlagsereignisses (N > 0) steigt die relative Luftfeuchte laut Korrekturformel 16.39 auf mindestens 95 %; die Sprungfunktion Φ stellt das sicher.
- Die Darstellung von Lufttemperatur über Partialdruck als Häufigkeitswolke (Abb. 16.61) entspricht einem Enthalpie-Wassergehalt-Diagramm (h-x-Diagramm); die untere Grenzkurve ist die Sättigungsdruckkurve.

### 16.4 — Niederschlag und Wind

#### 16.4.1 — Regenstromdichte

- Niederschlag und Wind sind stochastische, jahres- und witterungsabhängige Größen.
- Die Regenstromdichte gR = dmR / (dt · A) hat die Einheit kg/m²s; als Volumenstromdichte N = dVR / (dt · A) in m³/m²s oder l/m²h.
- In Mitteleuropa treten die größten Regenmengen im Sommer auf.
- Jahresniederschlagsmengen aus Messdaten:
  - Dresden 1997: 0,635 m³/m² (= 635 mm)
  - ARY (Analytisches Referenzklima): 0,612 m³/m²
  - Dresden-Klotzsche (Mittelwerte 1981–1990): 0,668 m³/m²
  - Cottbus 2014: 0,513 m³/m² (niederschlagsarme Stadt; niederschlagsarme Monate Juni und Juli)
- Bei einem Niederschlagsereignis (Gl. 16.39) steigt die relative Luftfeuchte auf mindestens 95 % — modifizierte Version der Luftfeuchteformel 16.37.
- Klimagebiet-Einteilung nach jährlicher Niederschlagsmenge (Tab. 16.8a):
  - Gebiet 1: N < 600 mm — niedrige Belastung
  - Gebiet 2: 600 mm < N < 800 mm — mittlere Belastung
  - Gebiet 3: N > 800 mm — hohe Belastung

#### 16.4.2 — Windgeschwindigkeit und Windrichtung

- Für Dresden 1997 betragen: mittlere Windgeschwindigkeit vmittel = 2,73 m/s, mittlere Windrichtung 178° (überwiegend Westen).
- Das ARY-Referenzklima für Windgeschwindigkeit vref(t) wird durch Gl. 16.40 mathematisch simuliert; der Jahresmittelwert des ARY beträgt 3,01 m/s.
- Dieser Mittelwert liegt der Berechnung des konvektiven Wärmeübergangs an Außenoberflächen und der Abschätzung windbedingter Luftwechselraten zugrunde.
- Die Windrichtung für das ARY (Gl. 16.41) ergibt einen Jahresmittelwert wmittel = 114,5° (gezählt ab Ostrichtung = 0° gegen Uhrzeigersinn), was vorwiegend Westwinden entspricht.
- In Dresden 1997 dominierten Südwest-, Nordwest- und Nordostwinde.
- Cottbus 2014: mittlere Windgeschwindigkeit 1,57 m/s, mittlere Windrichtung 148° — ebenfalls überwiegend Westen, aber gleichmäßigere Verteilung und geringere Geschwindigkeiten.
- Windniederschlagsindex (WNI) nach Gl. 16.42: WNI = N · v [m²/s]; Einteilung:
  - Gebiet 1: WNI < 2 — niedrige Belastung
  - Gebiet 2: 2 < WNI < 3 — mittlere Belastung
  - Gebiet 3: WNI > 3 — hohe Belastung
- Wind beeinflusst Druckverhältnisse am Gebäude, Durchströmung, Luftwechselrate und Lüftungswärmeverlust in der Heizperiode bzw. Raumtemperatur im Sommer. In Kombination mit Niederschlag wird die Schlagregenbeanspruchung (kapillare Wasseraufnahme von Wetterschutzschichten und Fugenabdichtungen) quantifizierbar.

### 16.5 — Gebäudeumströmung und Schlagregenbelastung

Aus Niederschlagsmenge, Windgeschwindigkeit und Windrichtung wird die Schlagregenstromdichte (Normalkomponente der Regenstromdichte auf die Bauteiloberfläche) ohne CFD-Simulation näherungsweise berechnet.

#### Physik der Regentropfen im Windfeld

- Auf einen Regentropfen wirken drei Kräfte: Schwerkraft Fg = ρW · (4/3)π · r³ · g, horizontale Windkraft Fw = c · ρL · π · r² · vL², Reibungskraft Fr = c · ρL · π · r² · vR².
  - Wasserdichte ρW = 1000 kg/m³
  - Erdbeschleunigung g = 9,81 m/s²
  - Luftdichte ρL = 1,24 kg/m³
  - Widerstandsbeiwert c (für Regentropfen c = 0,3)
- Aus dem Kräftegleichgewicht (Gl. 16.43) folgen:
  - Resultierende Regengeschwindigkeit vR (Gl. 16.44)
  - Vertikaler Richtungswinkel αv zur Bauteiloberfläche (Gl. 16.45)
- Ohne Wind (vL = 0): Regen fällt senkrecht (cos αv = 0, αv = π/2); Falltropfengeschwindigkeit vR₀ = 8,39 m/s bei r = 1 mm, c = 0,3.
- Der mittlere Regentropfenradius wächst mit der vierten Wurzel aus der Regenstromdichte (Gl. 16.51); die mittlere Regengeschwindigkeit wächst mit der achten Wurzel aus der Regenstromdichte (Gl. 16.52).

#### Normalkomponente der Schlagregenstromdichte

- Die Normalkomponente gRhn der auf eine (vertikale) Bauteilfläche auftreffenden Regenstromdichte hängt zusätzlich vom Windrichtungswinkel β zur Nordrichtung ab (Gl. 16.46):
  - gRhn = gR · cos αv · cos(β − π/2)
- Die Regenstromdichte gR im freien Feld ergibt sich für den allgemeinen Fall (Gl. 16.48, 16.49) und vereinfacht ohne Wind (Gl. 16.50).

#### Abminderung durch Gebäudegrenzschicht

- Nahe der Gebäudeoberfläche werden Regentropfen durch die Strömungsgrenzschicht abgebremst. Dies mindert die tatsächlich auftreffende Schlagregenstromdichte ab.
- Die abgeminderte Schlagregenstromdichte gRhs = DR · gRh (Gl. 16.53, 16.57).
- Grenzschichtbreite L nach Gl. 16.59 aus dem mechanischen Energieerhaltungssatz (Bewegungsenergie der Luft im Grenzschichtvolumen abzüglich Reibungsarbeit).
- Abminderungsfaktor DR nach Gl. 16.61: DR = exp(−E · v_L^0,25 · (gR/3600)^n / H).
  - E: Gebäudeparameter in kg^(1/4) m²/s^(1/2), betragsmäßig E = 0,5 · lbrems
  - vL in m/s, gR in kg/m²h
  - H: Gebäudehöhe bzw. Abstand des Aufpunktes vom Staupunkt auf der Luvseite in m
  - n = 0,25 (Exponent)
  - lbrems: kleinste Seite der Luvfläche
- Im Normalfall liegt DR zwischen 0 und 0,3.

#### Berechnungsbeispiele Schlagregen (Gl. 16.62)

**Beispiel 1: Riegel (Cottbus 2014, Zehnminutenfile)**
- Gebäude: Höhe h = 20 m, Breite l = 100 m, oberer Eckpunkt H = 54 m (= √(50² + 20²)), Bremsweg = h = 20 m
- Gebäudeparameter E = 10 kg^(1/4) m²/s^(1/2)
- Wandstellungen: i = 1 Ost, i = 2 Süd, i = 3 West, i = 4 Nord
- Negative Schlagregenmengen werden durch die Φ-Funktion ausgeschlossen.
- Ergebnis: In Mitteleuropa wird die Westwand am stärksten, die Ostwand am schwächsten belastet.
- Jahressummen (Abb. 16.83 Cottbus 2014):
  - Ostwand: 42,5 kg/m²
  - Nordwand: 79,7 kg/m²
  - Westwand: 111,4 kg/m²
  - Südwand: 71,6 kg/m²

**Beispiel 2: Hochhaus (Dresden 1997, Stundendatei)**
- Gebäude: Höhe h = 60 m, Breite l = 50 m, oberer Eckpunkt H = 65 m (= √(25² + 60²)), Bremsweg = l = 50 m
- Gebäudeparameter E = 25 kg^(1/4) m²/s^(1/2)
- Jahressummenwerte aus gemessenem Klima Dresden 1997 (in kg/m²):
  - Ostwand: 22,96
  - Südwand: 30,99
  - Westwand: 113,41
  - Nordwand: 47,44
- Jahressummenwerte aus ARY (in kg/m²):
  - Ostwand: 54,9
  - Südwand: 106,7
  - Westwand: 134,2
  - Nordwand: 103,5

**Vergleich mit CFD-Modell Blocken [37] (Tab. 16.9)**
Schlagregenstromdichte Jahressummen in kg/m²a auf der Westseite:

| Gebäudetyp | Dresden 1997 (Rh = 553 mm/a) | TRY Bremerhaven (Rh = 784 mm/a) | TRY München (Rh = 1066 mm/a) |
|---|---|---|---|
| h=20m, l=100m, H=54m (lowslab_Pos1) — Gl. 16.62 | 167 | 227 | 364 |
| h=60m, l=50m, H=65m (highslab_Pos1) — Gl. 16.62 | 113 | 152 | 211 |
| highslab_Pos1 nach Blocken [37] | 112 | 164 | 222 |
| lowslab_Pos1 nach Blocken [37] | 178 | 317 | 358 |

- Die ASHRAE-Norm liefert ca. doppelt so hohe Werte wie Gl. 16.62.
- Das in WUFI implementierte Modell liefert nur ca. halb so große Jahressummen.
- Gl. 16.62 eignet sich als bauklimatische Randbedingung für hygrothermische Gebäude- und Bauteilsimulation.
- Für eine präzise Auswertung sollte ein Zehnminutenfile verwendet werden; die vektorielle Mittelung der Windgeschwindigkeit auf Stundenwerte führt zu geringeren Schlagregenbelastungen (Abb. 16.83).

### 16.6 — Testreferenzjahr (TRY)

- Aus langjährigen Messungen aller Klimakomponenten, Wetterbeobachtungen und gewichteten Mittelwerten erstellt die Meteorologie synthetische Klimajahre — sogenannte Testreferenzjahre (Test Reference Year, TRY) für alle Städte und Klimagebiete der Erde.
- Ein TRY enthält Stundenwerte für: Außenlufttemperatur, direkte kurzwellige Strahlung, diffuse kurzwellige Strahlung, kurzwellige Gesamtstrahlung, langwellige Gesamtstrahlung (bestehend aus langwelliger Abstrahlung und langwelliger Himmelsgegenstrahlung/Umgebungsstrahlung), relative Luftfeuchte, Windrichtung, Windgeschwindigkeit sowie Niederschlag auf eine Horizontalfläche.
- Jahresmittelwerte für TRY Essen:
  - Außenlufttemperatur θm = 9,6 °C
  - Direkte kurzwellige Strahlung Gdir,m = 43,8 W/m²
  - Diffuse kurzwellige Strahlung Gdif,m = 59,4 W/m²
  - Langwellige Gesamtabstrahlung Glang,m = −47,0 W/m²
  - Windgeschwindigkeit vm = 3,5 m/s
  - Windrichtung wm = 126° (Südwestwind)
  - Gesamtniederschlagsmenge Nm = 919 mm
- Das Temperaturfile TRY Essen korrespondiert gut mit dem Jahresgang nach dem ARY (mit geringfügig modifizierten Parametern gegenüber Dresden).

### 16.7 — Klimagenerator

- Alle Berechnungsformeln für die Außenklimakomponenten (Abschnitte 16.1–16.5) sind in C++ implementiert und zu einem Klimagenerator zusammengeführt.
- Eingabe: Eine Klimamatrix im txt-Format mit Stundenwerten für Außenlufttemperatur, relative Luftfeuchte, direkte kurzwellige Strahlung, diffuse kurzwellige Strahlung, Niederschlag, Windgeschwindigkeit und Windrichtung (entspricht Tab. 16.1a oder jeden sechsten Wert aus Tab. 16.1b).
- Ausgabe: Stundenwerte aller gebäuderelevanten Klimabelastungen im txt-Format:
  - Kurzwellige Gesamtstrahlung auf beliebig ausgerichtete und geneigte Flächen
  - Langwellige Abstrahlung
  - Schlagregenbelastung auf beliebig ausgerichtete Vertikalflächen
  - Außenlufttemperatur und relative Luftfeuchte
- Eingabeparameter für Bauteilstellung: Ausrichtungswinkel, Neigungswinkel, sowie E und H (Gebäudegeometriekennwerte für Schlagregen).
- Der Klimagenerator erzeugt auch grafische Darstellungen der Ergebnisse.
- Beispielausgabe (Abb. 16.94): Verlauf von relativer Luftfeuchte, Temperatur, Gesamtstrahlung auf eine Ostwand und Niederschlag für 5.–7. Juni in Dresden 1997.

### Literatur (Kapitel 16, Auswahl der normativen und programmspezifischen Referenzen)

- DIN 4108-03: Wärmeschutz und Energieeinsparung in Gebäuden, Teil 3 Feuchtigkeitsschutz. Beuth Verlag, Berlin 2001.
- DIN 4108, Teil 6: Berechnung des Jahresheizwärme- und Jahresheizenergiebedarfs. Beuth Verlag, Berlin 2000.
- DIN 18599 (01–09): Energetische Bewertung von Gebäuden — Nutz-, End- und Primärenergiebedarfsberechnung für Heizung, Kühlung, Lüftung, Trinkwarmwasser und Beleuchtung. Beuth Verlag, Berlin 2006.
- DIN EN ISO 13792: Wärmetechnisches Verhalten von Gebäuden — sommerliche Raumtemperaturen ohne Anlagentechnik — Allgemeine Kriterien für vereinfachte Berechnungsverfahren. Beuth Verlag, Berlin 1997.
- Blümel et al.: Entwicklung von Testreferenzjahren (TRY) für Klimagebiete der Bundesrepublik Deutschland, BMFT-Bericht TB-T-86-051, 1986.
- Deutscher Wetterdienst: Testreferenzjahre für Deutschland für mittlere und extreme Witterungsverhältnisse TRY. Eigenverlag DWD, Offenbach 2004.
- METEONORM Version 6.1: Globale meteorologische Datenbank für Ingenieure, Planer und Universitäten. Bern 2009.
- Künzel/Holm: WUFI 4.1 — Wärme- und Feuchtesimulation instationär. Holzkirchen 2007.
- Nicolai/Grunewald: DELPHIN 5 — Gekoppelter Wärme-Luft-Feuchte-Salztransport. TU Dresden 2009.
- Häupl, P.: Bauphysik — Klima, Wärme, Feuchte, Schall. Ernst & Sohn, Berlin 2008.
