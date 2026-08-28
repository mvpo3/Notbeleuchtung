# Grundladen der elektrischen Energietechnik — Teil 7
> Quelle: Grundladen der elektrischen Energietechnik (buecher) · Seiten 281-320.

Dieser Teil schliesst Kapitel 3 (Elektrische Anlagen und Betriebsmittel) mit den Themen Schutztechnik, Stationsautomatisierung und Netzleittechnik ab. Dann beginnt Kapitel 4 (Modellierung und Berechnung) mit Per-Unit-System, Zustandsbegriffen, Fehlerarten und der Methode der symmetrischen Komponenten inklusive Impedanzberechnung.

## Inhalt

### Schutztechnik — Uebersichten nach Schutzobjekten und Geraetegenerationen

**Schutzkriterien (Tab. 3.21) — nach Wirkprinzip:**
- Ueberstromschutz: Sicherungen, IS-Begrenzer, unabhaengiges Maximalstrom-Zeitrelais (UMZ-Relais)
- Vergleichsschutz (Differenzialschutz): Vergleich von Messgroessen, bei Leitungen mit separater Signalleitung
- Distanzschutz: Abstand bzw. Impedanz zum Kurzschlussort
- Erdschlussschutz: Leiter-Erd-Spannungen der gesunden Leiter

**Schutzablauf:** Vom Zeitpunkt der Fehlerdetektion ueber die Ausloesebefehlsgenerierung bis zum Schaltvorgang im Leistungsschalter einschliesslich Lichtbogenloeschung soll der Zeitraum so kurz wie moeglich sein — Minimalwert liegt unterhalb von 100 ms.

**Schutzobjekte (Tab. 3.22) — nach Betriebsmitteln:**
- Generatorschutz: Schutz vor Ueberlast, Unter-/Ueberfrequenz, Untererregung, Schieflast, Rueckleistung sowie Erd- und Kurzschluessen. Generatoren werden bei Netzfehlern zuletzt abgetrennt; bei eigenen Fehlern schnellstmoeglich. Wird mit Turbine, Maschinentransformator und Eigenbedarfsnetz zum Blockschutz zusammengefasst.
- Transformatorschutz: Kombination aus Ueberstrom-, Differenzial- und Buchholzschutz (Buchholzschutz reagiert auf erhoehten Oeldruck durch Windungsschluss)
- Leitungsschutz (= Feldschutz): Ueberstrom-, Differenzial- oder Distanzschutz sowie Synchronueberwachung der Leistungsschalter
- Sammelschienenschutz: Differenzialschutz

**Selektivitaet im NS-Strahlennetz:** In Strahlennetzen der Niederspannungsebene genuegt Ueberstromschutz mit Zeitstaffelung. Beispiel: 10-kV-Netz → HH-Sicherung → 0,4-kV-Netz mit gestaffelten NH-Sicherungen (100 A → 63 A / 40 A → 40 A / 16 A → 10 A). In vermaschten Netzen kommen mehrere Schutzkriterien gleichzeitig zur Anwendung.

**Geraetegenerationen (Tab. 3.23):**
- Elektromechanisch: Dreheisen-, Drehspulen-, Induktionsmesswerke, elektrodynamische Messwerke
- Elektronik: analoge und analog-binaere Verarbeitungsprinzipien — Addierer, Subtrahierer, Multiplizierer, Dividierer, Integrierer, Differenzierer, Komparatoren, Zaehler
- Digitaltechnik: algorithmische Verarbeitungsprinzipien — Zustandsgroessen, numerische Verfahren, fehlerminimierendes und adaptives Messen

Digitale Mikroprozessoren haben die alten Messschaltungen vollstaendig abgeloest. Vorteile: deutlich weniger Platzbedarf in Schaltschraenken, Einbindung in digitale Stations- und Netzleittechnik ueber Bussysteme. Geratefunktions-Codes sind international nach USA-Industriestandard ANSI C 37.2 vereinheitlicht.

**Wide Area Monitoring System (WAMS):** Ausgelastete Netze mit knapper Schutzredundanz riskieren kaskadenartig ausloesende Schutzeinrichtungen nach einem Lokalfehler — bis hin zum regionalen oder totalen Stromausfall (Blackout). Dieses Risiko steigt durch volatile stromrichtergekoppelte Erzeuger ohne stabilisierende Schwungmasse. Abhilfe: WAMS (auch SPMS oder Synchrophasor-System genannt). An neuralgischen Netzknoten messen zeitsynchronisierte Phasormessgeraete (PMU — Phasor Measurement Unit) im Abstand von 20 ms die komplexen Amplituden von Strom und Spannung. Daraus werden Spannungs-/Stromzeiger, Netzfrequenz, Frequenzaenderung und Daempfungsgrad berechnet. Die Werte erhalten einen GPS-gesteuerten Zeitstempel und werden an einen Datenkozentrator einer Netzleitstelle uebertragen. Einsatz: Fruehwarnsystem bei sich ankuendigenden Grossstoerungen sowie zur Wiedersynchronisation von Inselnetzen nach Verbundnetzaufspaltung.

---

### 3.5.4 Stationsautomatisierung und Netzleittechnik

**Normenuebersicht (Tab. 3.24) — Auswahl relevanter Normen:**

| Norm | Titel |
|------|-------|
| IEC/DIN EN 60255 (VDE 0435) | Messrelais und Schutzeinrichtungen |
| IEC/DIN EN 60834-1 (VDE 0852) | Fernschutzeinrichtungen — Leistung und Pruefung |
| IEC/DIN EN 60870-5-03 | Fernwirktechnik — Uebertragungsprotokolle |
| IEC/DIN EN 61850 | Kommunikationsnetze und -systeme fuer Automatisierung von Energieanlagen |
| IEC/DIN EN 61869 (VDE 0414) | Messwandler |

**Netzleittechnik als Teildisziplin der MSR-Technik (Mess-, Steuer- und Regelungstechnik):**
Kennzeichnende Eigenschaften:
- Relativ niedrige Uebertragungsbandbreiten
- Weitraeumige Topologie (viele Kilometer Ausdehnung)
- Strenge hierarchische Struktur des Primaerprozesses
- Sehr leistungsfaehige Energiemanagement-Funktionen

Zweck: Ueberwachung und Steuerung des Primaerprozesses. Trotz hohem Automatisierungsgrad sind Netzleitanlagen keine Vollautomaten — qualifiziertes Personal bleibt auch mit KI-Unterstuetzung die letzte Entscheidungsinstanz.

**Vorteile der Netzleittechnik:**
- Stoerungen koennen schneller erkannt, behoben und protokolliert werden
- Schaltmassnahmen werden zentral durchgefuehrt
- Schalthandlungen koennen ueber regelbasierte Verriegelungen ueberprueft (zur Vermeidung von Schaltfehlern) oder vor der Ausfuehrung simuliert werden (mit Grenzwertueberpruefungen)
- (n-1)-Prinzip ist online per Ausfallanalyse pruefbar (Kuerzel CA = Contingency Analysis, SA = Security Analysis)
- Kurzschlussstromniveau kann online ueberwacht werden (Kuerzel SCA = Short Circuit Analysis)
- Statistische Daten werden gesammelt: Zahl der Schaltspiele, Daten fuer BDEW-Stoerungsstatistik, Ereignisprotokolle, Alarmlisten, Kurvengrafiken physikalischer Groessen

**IT-Sicherheit (Cyber Security):** Durch Energiewende und Netzautomatisierung ist die Zahl digitaler Kommunikations- und Steuersysteme deutlich angestiegen, was Angriffspunkte schafft. Sicherheitsmassnahmen definiert in ISO/IEC 27002 und ISO/IEC TR 27019, eingebettet in ein Informationssicherheits-Managementsystem (ISMS) nach ISO/IEC 27001.

**Hierarchischer Aufbau der Netzleitsysteme — drei Ebenen:**
1. **Feldleitebene:** Unterste Schicht, einem Schaltfeld zugeordnet. Bei hohem Automatisierungsgrad eigener Feldrechner fuer Prozessanschluss und Schutzfunktionen. Erfasst Daten von Wandlern und Meldekontakten. Schaltfeld enthaelt: Sammelschienen-Trennschalter, Leistungsschalter, Stromwandler, Spannungswandler, Leitungstrennschalter, Erdungsschalter.
2. **Stationsleitebene:** Weiterverarbeitung durch Applikationen des Stationsleitsystems; Daten werden ueber Fernwirklinien nach oben weitergegeben. Empfangene Befehle werden auf Gueltigkeit geprueft, an Aktoren ausgegeben und quittiert.
3. **Netzleitebene (EMS/DMS):** Besteht aus SCADA-System und Applikationsfunktionsschicht.

**IEC 61850 — globaler Standard:** Geht ueber reine Kommunikationsprotokoll-Standardisierung hinaus. Bietet Substation Configuration Language (SCL) mit XML-basierter Syntax fuer effiziente Beschreibung, Konfiguration und Verwaltung. Verbessert Interoperabilitaet, Effizienz und Zuverlaessigkeit. Definiert auch objektorientiertes Datenmodell fuer elektrische Betriebsmittel entsprechend dem hierarchischen Aufbau.

**SCADA-System — Datentypen:**
- Messwerte / Analogwerte: Spannung U, Strom I, Wirkleistung P, Blindleistung Q, Stufenstellungen
- Meldungen / Binaerwerte (Indications): Schalterstellungen von Leistungsschaltern
- Zaehlwerte aus Impulszaehlern
- Zustandsmerkmale / Status-Flags: nachgefuehrt, Datenerfassung blockiert
- Berechnete oder nachgefuehrte Ersatzwerte fuer nicht ferngemeldete Daten
- Befehle: Leistungsschalter oeffnen/schliessen
- Sollwerte: U_soll fuer lokale Spannungsregelung

Vor dem Abspeichern in die Prozessdatenbank verarbeitet das SCADA-System jeden Analogmesswert: Umwandlung in technische Einheiten, Grenzwertueberpruefung (upper alarm limit, upper warning limit, lower warning limit, lower alarm limit mit Deadband), Nullbereichsverarbeitung und Gradientenueberwachung.

Alle Ereignisse von Schalt- und Schutzgeraeten werden mit Zeitstempel protokolliert. Bestimmte Ereignisse werden als Alarme definiert — diese muessen explizit vom Bediener quittiert werden (akustischer Alarm moeglich).

**Schaltprogramme / Schaltsequenzen:** Ermoeglicht koordiniertes Steuern mehrerer Betriebsmittel mit Sicherheitspruefungen und Verzoegerungszeiten. Typisches Beispiel: Zu-/Abschalten von Kabeln oder Freileitungen auf Sammelschiene (erfordert korrekte Reihenfolge von Trennern und Leistungsschaltern). Verriegelungsfunktionen weisen unerlaubte Befehle ab; fuer Test-/Notsituationen koennen sie umgangen werden.

**Energiemanagement-System (EMS / PAS / HEO) — drei Bereiche:**
- Generation Management System (GMS): Einsatzplanung und Betrieb konventioneller Kraftwerke
- Energy Management System (EMS): Fuehrung der Uebertragungsnetze
- Distribution Management System (DMS): Fuehrung der Verteilnetze

Applikationen sind primaerprozessabhaengig. Hersteller modularisieren und skalieren zunehmend, aber massgeschneiderte Loesungen fuer einzelne Netzbetreiber existieren weiterhin.

---

### Kapitel 4 — Modellierung und Berechnung: Einfuehrung

Kapitel 4 behandelt: Simulation ungestoerter und gestoerter Betriebszustaende, Symmetrische Komponenten, Ersatzschaltbilder, Leistungsflussrechnung, einpolige Erdfehler und Kurzschlussstromberechnung.

**Per-Unit-System (bezogene Groessen):**
Bezogene Groessen sind dimensionslos, gekennzeichnet mit Kuerzel pu (per unit). Vorteile:
- Spannungswerte liegen in der Naehe von 1
- Viele Groessen bewegen sich in relativ engen Grenzen; fehlerhafte Werte leichter erkennbar
- Beim Rechnen ueber mehrere Spannungsebenen koennen ideale Transformatoren im Ersatzschaltbild weggelassen werden

Zwei Bezugsgroessen sind frei waehlbar, die uebrigen folgen daraus. Uebliche Basiswahl:
- Bezugsspannung U_B (Leiter-Leiter-Spannung)
- Bezugsscheinleistung S_B (dreiphasige Leistung)

Daraus ergeben sich:
- Bezugsstrom: I_B = S_B / (√3 · U_B)
- Bezugsscheinwiderstand: Z_B = U_B / (√3 · I_B) = U_B² / S_B

Bezogene synchrone Laengsreaktanz des Drehstrom-Synchrongenerators: x_d = X_d / Z_B = X_d · S_B / U_B²

Bei Verwendung der Bemessungswerte als Bezugsgroessen: x_d = X_d · S_r / U_r²  (S_r = dreiphasige Bemessungsscheinleistung, U_r = Leiter-Leiter-Bemessungsspannung). Bezogene Groessen: kleine Formelbuchstaben; absolute Groessen: grosse Formelbuchstaben.

---

### Stationaere und Dynamische Betriebszustaende

**Stationaerer Zustand:** Wenn laengere Zeit keine Stoerungen aufgetreten sind, sind Frequenz, Amplituden und Nullphasenwinkel der Wechselstroeme und -spannungen konstant. Mathematische Beschreibung: Bildbereich mit Effektivwertzeigern und stationaeren Ersatzschaltbildern.

**Quasistationaerer Zustand:** Schalthandlungen oder Fehler (Kurzschluesse) stoeren das Netz. Bei Eintreten einer Stoerung aendern sich Phasenlage und Amplitude — aber niemals sprunghaft, sondern stetig. Elektromechanische Schwingungen der Polraeder von Synchronmaschinen aendern Amplituden und Nullphasenwinkel langsam. Deren Frequenz liegt unterhalb von 50 Hz → bezeichnet als Subsynchrone Resonanz (SSR — Sub-Synchronous Resonance).

**Dynamischer Zustand (transient/subtransient):** Bei drastischen Aenderungen, die nach kurzer Zeit abklingen, spricht man von transienten oder subtransienten Vorgaengen. Beispiel: subtransiente Reaktanz X''_d des Drehstrom-Synchrongenerators.

---

### Fehlerarten in elektrischen Netzen

**Ursachen von Fehlern:** Alterung von Betriebsmitteln, Feuchteaufnahme in Isoliermaterialien, Durchschlag durch Temperatur, Schalt- oder Blitzueberspannungen, Resonanzen, Wettereinfluessel (Wind, Schnee, Eis, Salzgehalt im Nebel), Temperaturschwankungen, Fremdeinwirkungen (Tiere, Bagger, Erntemaschinen, menschliches Versagen).

**Grundeinteilung:**
- Kurzschluesse (Querfehler): leitende Verbindungen zwischen Leitern L1, L2, L3 oder N; metallischer Kurzschluss wenn kein Uebergangswiderstand im Fehlerstromkreis
- Erdfehler (Querfehler): mindestens ein Leiter L1/L2/L3 mit Erdkontakt
- Unterbrechungen (Laengsfehler)

**Kurzschlussarten (Abb. 4.2, Netze mit geerdetem Sternpunkt):**
1. Dreipoliger KS: alle drei Leiter L1/L2/L3 — symmetrischer Fehler
2. Zweipoliger KS ohne Erdberuehrung: zwei Leiter verbunden
3. Einpoliger KS: Aussenleiter mit Neutralleiter verbunden; tritt nur in der NS-Ebene bei TN- oder TT-Systemen auf
4. Einpoliger Erdfehler (Erdkurzschluss): Isolationsfehler Aussenleiter-Erde in Netzen mit niederohmig geerdetem Transformatorsternpunkt — sehr hoher Fehlerstrom, schnellstmoeglich abschalten
5. Zweipoliger KS mit Erdberuehrung: zwei Erdschluesse am selben Ort an verschiedenen Leitern
6. Leiterschluss: fehlerhafte Verbindung zwischen Leitern mit nennenswiertem Widerstand im Fehlerstromkreis
7. Koerperschluss: leitende Verbindung zwischen metallischem Koerper und aktiven Teilen
8. Leiterunterbrechung (Laengsfehler)

**Erdschluss vs. Erdkurzschluss:**
- Erdschluss: tritt in Netzen mit isolierten Transformatorsternpunkten oder bei Erdschlussloesch­spulen auf — Fehlerstrom klein genug, kann zeitlich toleriert werden
- Erdkurzschluss: Netze mit niederohmig geerdetem Sternpunkt — sehr hoher Fehlerstrom, muss sofort abgeschaltet werden

**Asymmetrische Erdfehler in Netzen mit isolierten Sternpunkten (Abb. 4.4):**
- Erdschluss: ein Leiter mit Erde
- Doppelerdschluss: zwei Erdschluesse an verschiedenen Leitern und verschiedenen Orten

**Statistische Haeufigkeit (Tab. 4.1 — FNN-Daten 2013-2016, Anteile in Prozent):**

| Fehlerart | MS (1 kV < Un ≤ 72,5 kV) | HS (72,5 kV < Un ≤ 125 kV) | HoS (> 125 kV) |
|-----------|--------------------------|-----------------------------|-|
| Einpolig | 35,4 % | 91,3 % | 89,7 % |
| Zweipolig | 16,5 % | 1,8 % | 8,4 % |
| Dreipolig | 9,6 % | 0,7 % | 1,3 % |
| Unbekannt | 38,5 % | 6,2 % | 0,6 % |

Einpolige Fehler treten bei HS und HoS mit Abstand am haeufigsten auf (rund 90 %). Bei MS dominiert die Kategorie "unbekannt".

**Mehrfachfehler:** Gleichzeitiges Auftreten mehrerer Quer- oder Laengsfehler; typisches Beispiel ist der Doppelerdschluss.

---

### Modellbildung und numerische Loesungsverfahren

**Softwareeinsatz:** Wegen der grossen Anzahl von Betriebsmitteln in realen Netzen wird auf leistungsfaehige Software zurueckgegriffen. Beispiel-Mengengeruest (Tab. 4.2 — Netzleittechnik-Projekt China Light and Power Hongkong):

| Kategorie | Anzahl |
|-----------|--------|
| Single line pictures | 1 400 |
| Main stations | 120 |
| Substations | 18 000 |
| Transmission lines | 30 000 |
| Transformers | 357 |
| Switches | 66 000 |
| Measurements | 33 000 |
| Indications | 58 000 |

**Mathematische Einordnung der Berechnungsverfahren (Tab. 4.3):**
- Kurzschlussstromberechnung (SCA): numerische Loesung eines linearen, spaerlich besetzten Gleichungssystems → U = Y⁻¹ · I
- Leistungsflussberechnung (DPF): iterative Loesung eines quadratischen Gleichungssystems (nichtlinear) → Δx_{ν+1} = -J⁻¹_ν · Δy_ν (Newton-Verfahren)
- Zustandsestimation (SE): ueberbestimmt → J = r^T · R⁻¹ · r → Min (Methode der kleinsten Quadrate)
- Leistungsflussoptimierung (OPF): nichtlinear, unterbestimmt, Minimierung einer Zielfunktion
- Transiente Stabilitaet / Dynamische Ausgleichsvorgaenge: nichtlinear, stetig, zeitdiskret → dx/dt = A·x + b
- Statische Stabilitaet: linear im Kleinen → Eigenwertberechnung A-λE = 0

Kurzschlussstromberechnung und Zustandsestimation sind stationaer/quasistationaer; transiente Stabilitaet ist dynamisch.

---

### 4.1 Symmetrische Komponenten

**Motivation:** Im Normalbetrieb ist das Drehstromnetz symmetrisch. Bei asymmetrischen Fehlern (Erdschluesse im MS-Netz, einpolige Kurzschluesse) bewaehrt sich die Berechnung mit symmetrischen Komponenten. Die Methode ist international standardisiert und Grundlage fuer Schutz- und Netzberechnungen. Weitere Komponentensysteme existieren (Raumzeiger, Park-Komponenten, Diagonalkomponenten).

**Eigenschaften der Transformation in symmetrische Komponenten:**
- Linear: linearer Strom-Spannungs-Zusammenhang bleibt erhalten
- Vollstaendige physikalische Entkopplung der Gleichungssysteme fuer symmetrisch aufgebaute Betriebsmittel
- Im symmetrischen Betrieb ist nur das Mitsystem wirksam

#### 4.1.1 Elektrische Stroeme — Zerlegung

Drei asymmetrische Leiterstroemzeiger IL1, IL2, IL3 werden in drei symmetrische Teilsysteme (nach DIN 1304-3 mit Indizes 1, 2, 0) zerlegt:

- **Mitsystem (Index 1):** symmetrisches Zeigersystem mit rechtsdrehender Phasenfolge (Rechtsdrehfeld)
- **Gegensystem (Index 2):** symmetrisches Zeigersystem mit entgegengesetzter Phasenfolge (Linksdrehfeld)
- **Nullsystem (Index 0):** alle drei Zeiger haben gleiche Phasenlage

Innerhalb jedes Teilsystems sind die Zeigerlangen gleich; zwischen den drei Systemen koennen sich Laengen und Phasenlage unterscheiden.

**Drehoperator:** a = e^{j120°} und a² = e^{j240°}. Multiplikation dreht den Zeiger um 120° bzw. 240°. Es gilt: a² + a + 1 = 0.

**Zerlegt ergibt sich:**
```
IL1 = I1L1 + I2L1 + I0L1
IL2 = a²·I1L1 + a·I2L1 + I0L1
IL3 = a·I1L1 + a²·I2L1 + I0L1
```

**Matrizenform:** IL = T_S · IS

Transformationsmatrix T_S (3x3):
```
     [1   1   1]
T_S = [a²  a   1]
     [a   a²  1]
```

Ruecktransformation: IS = T_S⁻¹ · IL

Inverse Transformationsmatrix T_S⁻¹ = (1/3) · [[1, a, a²], [1, a², a], [1, 1, 1]]

Es gilt: T_S · T_S⁻¹ = T_S⁻¹ · T_S = E (Einheitsmatrix). Die Methode ist auf alle Groessen des Drehstromsystems anwendbar (auch Spannungen).

#### 4.1.2 Impedanzen und elektrische Leistungen — Kompensationsdrosselspule

**Anwendungsbeispiel Drosselspule:** Drossel mit Anschluessen fuer L1, L2, L3 und Neutralleiter. Durch geeignete Dimensionierung der Luftspalte im Eisenkern annaehernd symmetrische elektrische Eigenschaften.

**Spannungsgleichungen (verlustfrei, ohne Kapazitaet):**

```
[UL1]         [L   -M   -M]   [IL1]
[UL2] = jω · [-M   L   -M] · [IL2]
[UL3]         [-M  -M    L]   [IL3]
```

L = Selbstinduktivitaet, M = Gegeninduktivitaet.

**Impedanzmatrix:** Mit Selbstimpedanz Z_s = jωL und Gegenimpedanz Z_g = -jωM:

Z_L (diagonal-symmetrisch):
```
     [Zs  Zg  Zg]
Z_L = [Zg  Zs  Zg]
     [Zg  Zg  Zs]
```

Kompaktform: U_L = Z_L · I_L

**Transformation in symmetrische Komponenten:**
U_S = T_S⁻¹ · U_L = T_S⁻¹ · Z_L · T_S · IS = Z_S · IS

Die transformierte Impedanzmatrix Z_S = T_S⁻¹ · Z_L · T_S hat aufgrund der Eigenschaft a² + a + 1 = 0 Diagonalform:

```
     [Zs-Zg    0      0  ]   [Z1  0   0 ]
Z_S = [0     Zs-Zg    0  ] = [0   Z2  0 ]
     [0        0   Zs+2Zg]   [0   0   Z0]
```

Bezeichnungen:
- Z1 = Zs - Zg = Mitimpedanz
- Z2 = Zs - Zg = Gegenimpedanz (= Z1 bei symmetrischer Drossel)
- Z0 = Zs + 2·Zg = Nullimpedanz

**Spannungsgleichungen in Komponentenform:**
```
[U1L1]   [Z1  0   0 ]   [I1L1]
[U2L1] = [0   Z2  0 ] · [I2L1]
[U0L1]   [0   0   Z0]   [I0L1]
```

Mit-, Gegen- und Nullsystem sind fuer symmetrische Betriebsmittel vollstaendig entkoppelt.

**Neutralleiterstrom:** I_N = IL1 + IL2 + IL3 = 3 · I0L1. Ohne Neutralleiter ist die Summe null und das Nullsystem entfaellt — nur Mit- und Gegensystem sind massgebend.

**Messung der Komponentenimpedanzen:**
- Mitimpedanz Z1: Rechtsdrehfeld anlegen
- Gegenimpedanz Z2: Linksdrehfeld anlegen (Drehrichtung des dreiphasigen Synchrongenerators umkehren oder zwei Wechselspannungsanschluesse vertauschen)
- Die Messschaltungen fuer Mit- und Gegensystem sind identisch; nur die Phasenfolge aendert sich
