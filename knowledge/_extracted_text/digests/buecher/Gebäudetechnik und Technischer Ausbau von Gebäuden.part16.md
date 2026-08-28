# Gebäudetechnik und Technischer Ausbau von Gebäuden — Teil 16
> Quelle: Gebäudetechnik und Technischer Ausbau von Gebäuden (buecher) · Seiten 641-673.

Abschlussteil des Lehrbuchs von D. Bohne (Springer 2022). Dieser Teil behandelt die dynamische Wirtschaftlichkeitsberechnung von Wärmeerzeugungsvarianten (inkl. konkretes Bürogebäude-Rechenbeispiel), das Themengebiet Smart Home mit Systemkomponenten und Steuerungsszenarien, methodische Vorgehensweise zur Erstellung von Energiekonzepten für Architekturentwürfe, sieben exemplarische Wettbewerbs-Energiekonzepte mit technischen Kennwerten, CO2-Bilanzierung im Gebäudebetrieb mit vollständiger Emissionsfaktor-Tabelle, sowie ein Konzept zum Energiewendehaus. Dazu kommen Serviceteile: Messeinheiten/Stoffwerte und Literaturverzeichnis.

## Inhalt

### 8.6 Dynamische Wirtschaftlichkeitsberechnung — Bürogebäude Berlin (Rechenbeispiel)

**Rahmenbedingungen des Rechenbeispiels:**
- Büroneubau in Berlin, 3.363 m² BGF
- Betrachtungszeitraum: 20 Jahre
- Strombezugspreis: 22 ct/kWh (netto), Erdgas: 7 ct/kWh
- Energiedaten aus thermischer Simulation, dynamische Jahreskosten nach Annuitätenmodell (VDI 2067)
- Preisdynamischer Barwertfaktor berücksichtigt angenommene Preissteigerungen

**Vier untersuchte Varianten der Wärmeerzeugung:**

| Variante | System | Investitionskosten (geschätzt netto) |
|----------|--------|---------------------------------------|
| 1 | Brennwertkessel + Warmwasserpumpenheizung (WWPH) | 184.000 € |
| 2 | BHKW (6 kW el. / 15 kW th.) + Spitzenkessel Brennwert + WWPH | 209.000 € (abzgl. 3.000 € KWK-Förderung) |
| 3 | Allelektrische Widerstandsheizung (Heizmatten im Estrich) | 78.649 € |
| 4 | Elektrische Widerstandsheizung + Li-Ionen-Speicher 500 kWh | 703.648 € |

**Technische Beschreibung Variante 3 + 4:**
- Elektrische Heizmatten im Estrich, Zweileitersystem, kein Wasserleitungsnetz, keine zentrale Wärmeerzeugung
- Variante 4: Lithium-Ionen-Speicher mit 500 kWh Kapazität (entspricht einem Durchschnittstag der Heizperiode), Kosten 1.250 €/kWh Speicherkapazität
- Annahme Nachttarif bei Variante 4: 2 ct/kWh (intelligenter Smart-Grid-Zähler)
- BHKW in Variante 2 auf elektrische Grundlast ausgelegt → vollständiger Eigenverbrauch des erzeugten Stroms; Gutschrift 0,22 €/kWh

**Jahreskosten über 20 Jahre (dynamische Wirtschaftlichkeitsrechnung):**

| Kostenart | V1 WWPH | V2 BHKW | V3 Direktelektr. | V4 Direktelektr.+Speicher |
|-----------|---------|---------|------------------|---------------------------|
| Kapitalgebunden | 207.600 € | 229.600 € | 78.648 € | 703.648 € |
| Bedarfsgebunden | 228.887 € | 161.638 € | 823.994 € | 366.216 € |
| Betriebsgebunden | 7.566 € | 87.939 € | 9.555 € | 161.413 € |
| Einsparung Strom | 0 € | 209.678 € | 0 € | 0 € |
| **Summe** | **444.053 €** | **269.499 €** | **912.197 €** | **1.231.277 €** |

**Schlussfolgerungen aus dem Rechenbeispiel:**
- Günstigste Variante: BHKW (V2) — 40 % günstiger als Standard-V1
- Reine Direktheizung (V3): Jahreskosten mehr als doppelt so hoch wie V1 trotz niedrigster Investition
- Elektrischer Speicher (V4): Dreifache Gesamtkosten; hohe Kapitalkosten können durch Billigstrom nicht kompensiert werden
- Wirtschaftlichkeit von Stromspeichern erst bei drastischer Kostenreduktion unter 400 €/kWh oder durch PV-Ergänzung denkbar
- Wirtschaftlichkeitsberechnungen aus der Planungsphase müssen im Betrieb per Monitoring verifiziert werden

**Instandhaltungskosten-Ansätze (Tab. 8.18 — Nutzungsdauer und Betriebskosten):**
- Betriebsgebundene Kosten setzen sich zusammen aus: Inspektion, Wartung, Instandsetzung, Schwachstellenbeseitigung
- Ansätze erfolgen prozentual oder mit Lohnstundenansätzen je nach Anlagenkomponente

---

### 8.7 Smart Home

**Definition:** Smart Home bezeichnet die vernetzte Steuerung der Haustechnik innerhalb einer Wohneinheit. Einheitliche Definition fehlt; umfasst Energieverbrauchssteuerung, Sicherheitstechnik, Haushaltsgeräte-Integration und Multimedia.

#### Grundkomponenten eines Smart Home Systems

1. **Sensorik** — Datenerfassung (z.B. Raumtemperatur, Bewegung)
2. **Datenübertragung** — kabelgebunden (Bussystem) oder kabellos (Funk)
3. **Datenauswertung + Steuerung** — Soll-Ist-Abgleich, Ausgabe an Aktoren
4. **Smart Home Zentrale (Gateway/Automatisierungsrechner)** — verbindet Komponenten unterschiedlicher Hersteller/Protokolle, Nutzerinterface via WLAN/App

**Potentielle Komponenten (nicht abschließend):**
- Tür-/Fensterkontakte, Beleuchtung, E-Mobilität (Wallbox)
- Haustechnische Anlagen (Heizung, Lüftung, Jalousien)
- Haushaltsgeräte, Sicherheitstechnik, Unterhaltungselektronik
- Regenerative Energieversorgung (PV), Sonnenschutz

#### Anwendungsbeispiele / Funktionen

**Thermische Komfortsteuerung:**
- Abwesenheit: Grundtemperatur wird gehalten; bei Ankunft soll Behaglichkeitstemperatur herrschen
- Sensor misst Außen- und Raumtemperatur → Steuerung von Heizung, Jalousien, Fensterlüftung
- Passivhaus-Beispiel: Jalousien öffnen (Vortemperierung im Winter), bei Überhitzungsgefahr wieder schließen + Fenster öffnen
- Energieeinsparung durch Nutzung kostenloser Anergie (Solarstrahlung, Außenluft)

**Komfort-Szenarien ohne Energiebezug:**
- Licht-/Musikwecker zu gewünschter Uhrzeit; Bewegungssensor → Kaffeemaschine aktiviert sich

#### Steuerungsszenarien — Wenn-Dann-Prinzip

- Szenarien funktionieren nach dem Muster: Wenn Ereignis X (externe oder Nutzeraktion) → dann Reaktion Y
- Beispiele: "nach Hause kommen → Licht geht an + Tür öffnet"; "Außentemperatur sinkt → Heizung geht an + Fenster schließen"
- Automationsgrad kann der Nutzer selbst festlegen; selbstlernende Komponenten möglich
- Insellösungen für einzelne Gewerke (nur Heizung, nur Jalousie) ebenfalls möglich

#### Kommunikationsstandards und Steuerungstechnik

**Kabellose Lösungen:**
- WLAN: zu energieaufwändig für Smart Home
- Bluetooth: Reichweite zu gering
- Funkstandards: häufig herstellerpropriätär → Erweiterbarkeit auf Produkte des jeweiligen Herstellers beschränkt

**Kabelgebundene Lösungen:**
- KNX-Standard: weltweit verbreitet, viele Hersteller, auch in Büro-/Verwaltungsgebäuden; nicht für alle Anwendungsfälle optimal, aber kombinierbar mit Spezialsystemen (z.B. DALI für Lichtsteuerung)
- Kabelgebunden bevorzugt (reibungsloser als Funk), bei Bestandsbauten oft nur Funk wirtschaftlich umsetzbar
- Neubau: umfassende Verkabelungsinfrastruktur vorsehen, auch für künftige Funktionen

**Datenverarbeitung:**
- Lokal (Automatisierungsrechner in der Wohneinheit) oder Cloud-Dienstleister
- Smart Home kann als geschlossenes Netz (ohne Internetzugang) geplant werden
- Nutzerinterface: App auf mobilem Endgerät (über Internet) oder lokale Schalter/Endgeräte

---

### 8.8 Energiekonzepte für Architekturentwürfe

#### Methodische Vorgehensweise

**Zeitpunkt:** Energiekonzept idealerweise parallel zum Gebäudeentwurf in früher Planungsphase entwickeln.

**Standortprüfung vorab:**
- Geothermisches Potential (geothermische Karten, Wärmeleitfähigkeit Untergrund, Entnahmekapazität)
- Solarnutzung: Flächen für PV/Solarthermie, Verschattungsanalyse, Gebäudeintegration
- Quartierlösung: Fernwärme/-kälte, ggf. Anschlusszwang
- Kleinwindkraftanlagen (selten, meist nur bei Hochhäusern möglich)

**Schritt 1: Gebäudeentwurf optimieren**
- Wärmeverlustminimierung durch hohen Wärmeschutz
- Thermisches Verhalten analysieren (Sonnenschutz, Speichermasse, Nachtauskühlung)
- Konsequenz: Entwurfsanpassung (z.B. Verzicht auf Deckenabhängungen → höhere Speichermasse)

**Schritt 2: Energiebedarfs-Basisdaten**
- Thermische Simulation → Heizlast und Kühllast abschätzen
- RLT-Anlagen aus Nutzungsanforderungen ableiten; notwendige Luftwechselrate hängt von Schadstoffemissionen der Baustoffe ab
- Weitere elektrische Verbraucher (Beleuchtung, EDV) erfassen und energetisch bewerten

**Schritt 3: Technisches Gesamtkonzept**
- Leistungsdaten für Wärme, Kälte, Strom ermitteln und vergleichen
- Systemauswahl beeinflusst elektrischen Bedarf (z.B. Wärmepumpe = Strombedarf)
- Geothermie + Wärmepumpe: ermöglicht Direktkühlung in Untergrund (Regeneration)
- Ziel: minimaler CO2-Ausstoß im Betrieb, Wirtschaftlichkeitsnachweis über Lebensdauer
- Wirtschaftlichkeit vieler Systeme erst mit angemessenem CO2-Preis darstellbar
- Konzepte müssen im Betrieb durch Monitoring validiert werden

---

#### Wettbewerbs-Beispiel 1: Filmhaus WDR, Köln (Generalsanierung 2013)

**Nutzung:** Büros, TV-/Rundfunk-Studios, Veranstaltungen; 700 Arbeitsplätze

**Energieziel:** Gesamtprimärenergiebedarf ≤ 100 kWh/(m²·a) — entspricht ca. 50 % des Durchschnittswerts vergleichbarer Bürogebäude

**Konstruktion:**
- Aufgeständerte Böden + abgehängte Decken (für Leitungsführung/Flexibilität) → geringe thermische Masse → "flinke" Systeme erforderlich
- Aktivierte Metalldecken in Aufenthaltsräumen: ganzjährige Temperierung 19–22 °C
- Deckenheiz-/Kühlsysteme als Luftdurchlass (Lochblechdurchlässe); höhere Räume: größere Induktion; niedrigere Räume: geringe Induktion

**Thermische Hülle:**
- Dreifachverglasung mit hochwertigen Wärmeschutzgläsern
- Integrierter Sonnenschutz im Fensterzwischenraum (reduziert sommerlichen Wärmeeintrag)
- Tageslichtabhängige Lichtsteuerung (reduziert Primärenergiebedarf für Beleuchtung + Kühlung)

**Wärmeerzeugung:** Anschluss an innerstädtisches Fernwärmenetz (fast ausschließlich Abwärme aus KWK)

**Raumlufttechnik (RLT):**
- Auslegung nach hygienischem Mindestluftwechsel: IDA 3, ODA 3
- Volumenstrom: 6 m³/(h·m²) je nach Lüftungseffektivität
- Ventilatoren mind. SFP 2
- Hochleistungs-Wärmerückgewinnung Klasse H1 (DIN EN 13053)
- Zu-/Abluftzentrale im 3. UG mit Rotationswärmetauschern
- Behandlungsstufen: Heizung, Kühlung, Entfeuchtung (nur wo nötig); dezentrale Befeuchter in sensiblen Bereichen
- Sonderbereiche (Produktion, TV-Studio, Rechenzentrum) erhalten eigene RLT-Anlagen
- Fensterlüftung in der Übergangszeit möglich (wenn ODA 3 Feinstaub dies zulässt)

**Kälteversorgung:** Sorptionskältemaschinen, angetrieben durch Fernwärme (auch im Sommer)

**Zentralenflächenbedarf:**
- Gesamtfläche Zentralen: 600–700 m²; davon RLT-Zentrale 300–350 m², Kältezentrale 80 m²
- Luftschächte vertikal: 3 Schächte à 5 m² (Luftleitungen) + 3 m² (andere Leitungen)

**Photovoltaik:**
- 700 m² PV auf Dachfläche (extensiv begrünt für niedrigere Umgebungstemperaturen → besserer PV-Wirkungsgrad)
- Ziel: 90 % des Stromgrundbedarf aus PV
- Li-Ionen-Speicher für Leistungsspitzen-Pufferung

---

#### Wettbewerbs-Beispiel 2: VK-Wesermühlen, Hameln (Denkmalschutz-Umnutzung)

**Objekt:** Pfortmühle der VK-Wesermühlen AG, Hameln (1894); 6-geschossig, Flachdach, Ziegelbau mit Attika; bedeutendes Industriedenkmal

**Nutzungskonzept:** ~18.000 m² Nutzfläche; Wohnen ~8.000 m², Hotel/Kultur/Ausstellung/Skybar ~10.000 m²

**Energiebedarf (prognostiziert):**
- Wärmearbeit: 700.000–800.000 kWh/a
- Strombedarf: 560.000–700.000 kWh/a

**Herzstück: Total-Energie-Verbund-Anlage**
- Elektrische Wärmepumpe mit saisonal gespeicherter Wärme aus ehemaligem Getreidesilo als Wärmequelle (5.000–10.000 m³ Speichergröße)
- Wärmepumpe vollständig durch BHKW-Eigenstromerzeugung betrieben
- Abwärme aus KWK: Hochtemperaturnetz 70–80 °C Vorlauf (direkte Nutzung) + Überschuss in Niedertemperaturspeicher 25–35 °C
- Thermische Solarkollektoren: 500–1.000 m² für saisonale Wärmespeicherung
- Polykristalline PV: ~500 m² auf Dach
- Eigenstromanteil aus KWK + PV: ca. 50 %; mit Elektrospeicher auf ~60 % steigerbar
- Wärmebedarf vollständig durch KWK + solare Saisonspeicherung gedeckt
- Sommerbetrieb: Sorptionsmaschine für Kälteversorgung aus BHKW-Abwärme
- Elektrospeicher: Lithium-Ionen, 100 kWh, puffert 1–2 h Eigenstrombedarf
- **Ergebnis:** Primärenergiereduzierung um 70 % gegenüber vergleichbaren Gebäuden; keine zusätzliche Wärmedämmung der Fassade nötig (denkmalgerecht)

---

#### Wettbewerbs-Beispiel 3: Telekom-Hochhaus Konstanz (Umnutzung zu Wohnhochhaus, Wettbewerb 2019)

**Objekt:** 16-geschossiges Hochhaus, Petershausen/Konstanz; Ergänzungsgrundstück mit Schulsporthalle/Tiefgarage

**Energieziel:** Gering CO2 bei größtmöglicher Behaglichkeit; netzdienlich (regenerativen Überschussstrom aus Netz speichern)

**Gebäudeeigenschaften:**
- Kompakte Form (günstiges A/V-Verhältnis)
- Dreifachglas-Fassade mit integrierten Lüftungselementen
- Klimawandel-Anpassung: Kühlung für Sommer/Übergangszeit eingeplant

**Wärmeerzeugung:**
- Zwei reversible Luft-Wasser-Wärmepumpen (elektrisch angetrieben) im 15. OG
- Wärmequelle: Außenluft (keine Geothermie verfügbar)
- Wärmeverteilung: Warmwasserpumpenheizung + Fußbodenheizung in Wohnungen
- Kühlung: reversible Wärmepumpen liefern temperiertes Wasser für Fußbodenkühlung

**Trinkwarmwasser:**
- Dezentral in Wohneinheiten: Abluft-Warmwasser-Wärmepumpe in Verbindung mit Abluftanlagen innenliegender Bäder

**Photovoltaik:**
- 200 m² PV: deckt Grundlast, ermöglicht im Sommer emissionsfreie solare Kühlung

**Speicherkonzept:**
- Li-Ionen-Speicher (skalierbar) für Lastspitzkappung (netzreaktiv) oder Überschuss-Zwischenspeicherung
- Bei weiterem Überschuss: Power-to-Heat (P2H) → Heißwassererzeugung und -speicherung

---

#### Wettbewerbs-Beispiel 4: Feuer- und Rettungswache Borken (Neubau, Wettbewerb 2021)

**Raumprogramm:** Fahrzeughallen, Werkstätten, Lager, Personal-, Ausbildungs-, Aufenthalts-, Verwaltungs- und Technikräume

**Energieziel:** Hoher Selbsterzeugungsgrad; Teilnahme am zukünftigen Smart-Energie-Verbund mit P2H

**Gebäude und Speichermasse:**
- Kompakte Form, hochwärmegedämmte Fassade, Dreifachglas (nicht zu hoher Glasanteil)
- Keine Deckenabhängung → hohe Speicherwirkung → Temperierung nur an wenigen Jahrestagen nötig
- Bauteilaktivierung (Betondecken): Heizen/Kühlen via Systemtemperaturen max. 35 °C (Heizfall), min. 17 °C (Kühlfall)
- Nachtauskühlung zur zusätzlichen Entlastung
- P2H-Funktion: Überschussstrom aus Netz (Grid Support Coefficient als Messsignal) in Bauteilen speichern statt Warmwasserspeicher

**Wärme- und Kälteerzeugung:**
- Fernwärmeanschluss (niedriger Primärenergiekennzahl) für Grundwärmeversorgung
- Sorptionskältemaschine aus Fernwärme (Sommer)
- Kompressionskältemaschine mit PV-Solarstrom bei Überschussstrom (solare Kühlung)

**Stromversorgung:**
- PV-Anlage (Schwerpunkt Sommer/Übergangszeit)
- Recycelfähige Redox-Flow-Speicher als Tages-Energiepuffer
- Regenwasserspeicher für Sonderfunktionen

**RLT:**
- Kontrollierte Raumlufttechnik für das gesamte Gebäude
- Hygienekonzept mit Fokus auf Raumströmung und Filterstufen (u.a. Virenübertragungsprävention, z.B. Covid-19)

---

#### Wettbewerbs-Beispiel 5: Polizeiwache Siegen (PPP-Neubau, Wettbewerb 2020)

**Raumprogramm:** ~6.546 m², ~340 Mitarbeiter (teils Schichtbetrieb); mindestens 240 Stellplätze, 6 Carports, 15 Garagen

**Gebäude:**
- Kompakte Form, hochwärmegedämmte Fassade, Dreifachverglasung
- Kein Deckenabhang → bessere Speicherfähigkeit; Bauteilaktivierung für Heizung, Kühlung, Nachtauskühlung, Energiespeicherung
- Systemtemperaturen: Heizen max. 35 °C, Kühlen min. 17 °C (geringe Strahlungsasymmetrie → hohe Behaglichkeit)
- Grid Support Coefficient als Messsignal für Energiemanagement

**Wärme- und Kälteerzeugung:**
- Reversible Wärmepumpen (Erdsonden-Geothermie: Heizung und direkte Kühlung)
- Ggf. zusätzliche Kompressionskältemaschinen
- PV-Anlage + Redox-Flow-Speicher (Tagesspeicher); solare Kühlung im Sommer

**Ziel:** Maximaler Eigenstromeinsatz aus PV mit Speicherung

**RLT:** Kontrollierte Raumlufttechnik, Hygienekonzept (Luftbelastung am Standort, Covid-19-Prävention)

---

#### Wettbewerbs-Beispiel 6: Stadtschloss Berlin / Humboldt Forum (Wettbewerb 2010)

**Nutzung:** Museum (Ethnologisches Museum + Museum für Asiatische Kunst), ~17.500 m² Ausstellungsfläche, 2 Lose

**Anforderungen:** Hohe Behaglichkeit (geringe Temperaturunterschiede an Oberflächen), gute Luftqualität, kontrollierte Feuchte

**Raumkonditionierung:**
- Großflächige Flächenheiz-/Kühlsysteme: Kapillarrohrmatten im Putz, abgependelte Deckensysteme oder Wandheizsysteme je nach Raum
- Einfache Verwaltungsräume: RLT mit einer thermodynamischen Behandlungsstufe
- Museumsräume mit hohen Anforderungen: RLT mit drei bis vier Behandlungsstufen
- Reiner Mindestluftwechsel: Quellluftzuführung; klimatisierte Räume: Mischluftprinzip
- Zuluft über Decke oder Doppelboden (Quellluftsystem)
- Wärmerückgewinnung per Rotationswärmetauscher: bis zu 80 % Wärmerückgewinnung aus Abluft
- Ventilatoren mind. SPF 1
- Hochwertige Wärmerückgewinnung Klasse H1 (optimierte Kanalnetze)
- LED-Beleuchtung überwiegend

**Energieversorgung:**
- Vorlauftemperatur für Flächenheizung: max. 35 °C; Kühltemperaturen: 17–18 °C (ermöglichen regenerative Energie)
- Grundwassernutzung thermisch: Direktkühlung über Saug-/Schluckbrunnen, zweiter Kreislauf für Flächenheizung/-kühlung
- Absorptionswärmepumpe für Heizbetrieb (Wärmequelle Grundwasser, Vorlauf 35–37 °C → hohe Jahresarbeitszahl)
- Fernwärme für Spitzenbedarf und bei unzureichendem Grundwasserkältepotential
- Reversible Wärmepumpen für Kälteerzeugung (Absorbtionstechnik bei Bedarf)
- KWK (BHKW mit Biodiesel): deckt Stromgrundlast; Abwärme in Wärmekreislauf eingebunden
- **Primärenergiebedarf:** unter 150 kWh/(h·a) — ca. 50 % unterhalb der damaligen EnEV
- Erneuerbarer Energieanteil: bis zu 75 % aus Grundwasser geplant

**Agora:**
- Fußbodentemperierungssystem für leichte Heiz-/Kühlfunktion
- Nebenräume: Flachheizkörper
- Lichtsysteme mit tageslichtabhängiger Steuerung

---

#### Wettbewerbs-Beispiel 7: Stadtsparkasse Iserlohn (Generalsanierung, Wettbewerb 2015)

**Objekt:** Hauptstelle Sparkasse Iserlohn, Stadtkern; Erbaut 1936, seither mehrfach erweitert

**Energieziel:** Primärenergiebedarf ≤ 100 kWh/(m²·a) — ca. 50 % des Durchschnitts vergleichbarer Gebäude

**Konstruktion:**
- Abgehängte Deckensysteme (hohe Installationsdichte) → geringe thermische Masse → "flinke" Systeme
- Aktivierte Metalldecken in Aufenthaltsräumen: Temperaturbereich 19–22 °C ganzjährig
- Deckenheiz-/Kühlsysteme gleichzeitig als Luftdurchlässe (Lochblechdurchlässe)
- Alternative: Deckenfries mit Über-Kopf-Zuluftführung; Abluft über Überströmung in Flur-Deckenzone

**Wärmeerzeugung:** Fernwärme aus Müllheizkraftwerk Iserlohn (Primärenergiefaktor 0)

**RLT:**
- Mindestluftwechsel: IDA 2, ODA 2
- Volumenstrom: 6 m³/(h·m²) je nach Lüftungseffektivität
- Ventilatoren mind. SFP 2; Wärmerückgewinnung Klasse H1 (DIN EN 13053); Rotationswärmetauscher
- Zu-/Abluftzentrale auf Dach oder im Untergeschoss (je nach optimierter Kanalführung)
- Behandlungsstufen: Heizung, Kühlung, Entfeuchtung bei Bedarf; dezentrale Befeuchter
- CO2-gesteuerte Außenluft-Steuerung bei stark schwankender Personenfrequenz
- Fensterlüftung in Übergangszeit (ODA 2 Feinstaub permissiv)
- Kassenhalle und besondere Bereiche: eigene RLT-Anlagen

**Kälteversorgung:**
- Sorptionskältemaschinen aus Fernwärme (ganzjährig → ganzjährige Fernwärmenutzung)
- Wahl zwischen Absorptions- oder Adsorptionstechnik je nach Sommersystemtemperaturen der Fernwärme

**Photovoltaik:**
- 250 m² PV auf begrüntem Dach (reduzierte Umgebungstemperaturen → höherer Wirkungsgrad)
- 90 % des Dauerstrombedarfs (Grundlast) aus PV
- Li-Ionen-Speicher für Leistungsspitzen-Pufferung
- Sonnenschutz im Fensterzwischenraum (Kühllastreduzierung)

---

#### Wettbewerbs-Beispiel 8: Konrad-Adenauer-Stiftung Berlin (Erweiterungsbau, Wettbewerb 2014)

**Raumprogramm:** HNF ~3.500 m²; 5 Obergeschosse + 1 UG; BGF oberirdisch ~4.800 m²; Geschosshöhen 3,42 m; Raumhöhe 3,05 m; Stützweite 5,40 m; Ausbauraster 1,35 m; Traufhöhe 18,75 m

**Konstruktion:**
- Aufgeständerte Böden + nicht abgehängte massive Betondecken (hohe thermische Speichermasse)
- Nachtauskühlung als Strategie

**Lüftung:**
- Dezentrale Lüftungsgeräte in Unterbodenmodulen (Umluft + Außenluft-Anschluss)
- Außenluft wird verdeckt aus vorgesetzter Fassade entnommen
- Zweileitersystem im Doppelboden: transportiert entweder Wärme oder Kälte zur Nachtemperierung der Zuluft
- Wärmerückgewinnung in dezentralen Geräten; geeignet für Nachtauskühlung; individuelle Raumsteuerung
- Ventilatoren: Effizienzklasse SPF 1
- In Übergangszeit: Verzicht auf RLT; Fensterlüftung

**Wärmeerzeugung:** Fernwärmenetz (92,9 % aus KWK-Abwärme laut Betreiber Vattenfall)

**Kälteerzeugung (optional):**
- Adiabate Verdunstungskühlung: Regenwasserzisterne unterirdisch; Dachflächen-Regenwasser gespeichert; Temperierung 19–21 °C für Zweileitersystem
- Oder Sorptionskältemaschine aus Fernwärme
- Regenwasser auch für Nichttrinkwasserversorgung (WCs, Urinale); Überlauf versickert über Rigole

**Photovoltaik:**
- Grundlast-Auslegung: voraussichtlich 27 kW → entspricht 180–200 m² PV auf dem Dach
- Strom vollständig im Gebäude selbst genutzt (kein Netzeinspeis)
- Li-Ionen-Speicher empfohlen zur Eigenverbrauchssteigerung
- LED-Technik; tageslichtabhängige Lichtsteuerung; außenliegender Sonnenschutz

---

#### Wettbewerbs-Beispiel 9: Pressevertriebszentrum Rheinland (Studie 2012)

**Objekt:** Halle (Kommission, Remission, Nachlieferung) + Verwaltungsgebäude; dynamische Logistik 24/7

**Hallenkennwerte:**
- Regalbereich allgemein max. 2,20 m Höhe; Euro-Paletten-Regale bis ca. 3,50 m

**Herausforderungen:**
- Halle und Verwaltung haben unterschiedliche thermische Anforderungen
- Geothermie: nur mit hohen Investitionen nutzbar (ungeeignete Bodenverhältnisse)
- Thermische Simulation: Kühlung im Sommer notwendig
- BHKW mit 40–50 kW elektrischer Leistung: wirtschaftlich nach weniger als 3 Jahren

**Zwei Lösungskonzepte (Varianten):**

**a) Luftgeführte Lösung:**
- Solare Luftkollektoren auf Hallendach → Zuluftvorwärmung (kontrolliertes Lüftungssystem)
- Adiabate Verdunstungskühlung aus Regenwassersammlung (geringe Primärenergie)
- Luft als einziger Wärmeträger in beiden Gebäudeteilen
- BHKW-Abwärme über geschlossene Warmwasserpumpenanlage zu RLT-Geräten
- Verwaltungsgebäude in Passivhausqualität mit luftgeführtem System

**b) Wassergeführte Lösung:**
- Bauteilaktivierung für Bürogebäude
- Warmwassergeführte Strahlungssysteme (Deckenstrahlplatten) in der Halle
- BHKW + Absorptionsmaschine für Kälteerzeugung im Sommer (aus BHKW-Abwärme)

---

### 8.9 CO2-Bilanzierung Gebäudebetrieb

**Treibhauspotential (GWP):** Maßzahl für den relativen Beitrag einer Emission zur globalen Erwärmung, bezogen auf CO2 (= 1) als Referenz. Abkürzung CO2e (equivalent), gemäß Kyoto-Protokoll.

**Treibhauspotentiale wichtiger Gase:**

| Gas | Formel | CO2e (Kyoto) |
|-----|--------|--------------|
| Kohlenstoffdioxid | CO2 | 1 |
| Methan | CH4 | 21 |
| Distickstoffoxid (Lachgas) | N2O | 310 |
| Schwefelhexafluorid | SF6 | 23.900 |

**Emissionsfaktoren nach Gebäudeenergiegesetz (GEG) — Tab. 8.21:**

| Nr. | Kategorie | Energieträger | Emissionsfaktor [g CO2-Äquivalent/kWh] |
|-----|-----------|---------------|----------------------------------------|
| 1 | Fossile Brennstoffe | Heizöl | 310 |
| 2 | | Erdgas | 240 |
| 3 | | Flüssiggas | 270 |
| 4 | | Steinkohle | 400 |
| 5 | | Braunkohle | 430 |
| 6 | Biogene Brennstoffe | Biogas | 140 |
| 7 | | Biogas, gebäudenah erzeugt | 75 |
| 8 | | Biogenes Flüssiggas | 180 |
| 9 | | Bioöl | 210 |
| 10 | | Bioöl, gebäudenah erzeugt | 105 |
| 11 | | Holz | 20 |
| 12 | Strom | Netzbezogen | 560 |
| 13 | | Gebäudenah erzeugt (PV oder Wind) | 0 |
| 14 | | Verdrängungsstrommix | 860 |
| 15 | Wärme/Kälte | Erdwärme, Geothermie, Solarthermie, Umgebungswärme | 0 |
| 16 | | Erdkälte, Umgebungskälte | 0 |
| 17 | | Abwärme aus Prozessen | 40 |
| 18 | | Wärme aus KWK, gebäudeintegriert/gebäudenah | nach DIN V 18599-9:2018-09 |
| 19 | | Wärme aus Verbrennung von Siedlungsabfällen | 20 |
| 20 | Nah-/Fernwärme aus KWK, KWK-Deckungsanteil ≥ 70 % | Brennstoff Steinkohle/Braunkohle | 300 |
| 21 | | Gas-/Flüssigbrennstoffe | 180 |
| 22 | | Erneuerbarer Brennstoff | 40 |
| 23 | Nah-/Fernwärme aus Heizwerken | Brennstoff Steinkohle/Braunkohle | 400 |
| 24 | | Gas-/Flüssigbrennstoffe | 300 |
| 25 | | Erneuerbare Brennstoffe | 60 |

**Berechnungslogik:** Summe der Energieverbrauchswerte multipliziert mit jeweiligem Emissionsfaktor des Energieträgers.

**Klimapositives Gebäude:** Definition = ausgeglichene oder negative CO2-Jahresbilanz im Betrieb; Einspeisung von PV-Überschussstrom wird als vermiedene CO2-Emission bilanziert (subtrahiert).

**CO2-Preisentwicklung:**
- 2021: erstmals 25 €/t CO2
- 2022: 30 €/t CO2
- Bis 2025: kontinuierlicher Anstieg auf 55 €/t CO2
- 2026: Zertifikatehandel; Preis im Rahmen 55–65 €/t
- Ab 2027: keine Festpreise oder Ober-/Untergrenzen mehr; Marktpreis

---

### 8.10 Energiekonzept für ein Energiewendehaus

**Transformationsziele:**
- 2030: ca. 65 % des Strombedarfs aus erneuerbaren Quellen
- 2045: Energie hauptsächlich aus Erneuerbaren (Wind, Wasser, Sonne, Geothermie, nachwachsende Rohstoffe)
- Gebäude: ca. 35 % der gesamten Endenergie → Schlüsselrolle

**Anforderungen an adaptive Gebäudeenergiesysteme:**
- Netzdienlichkeit: auf Überschussenergie aus dem Netz mit Speichertechnik reagieren
- Smart Meter Rollout: für neue Gebäude ab 6.000 kWh/a jetzt verpflichtend; ab 2032 für alle Gebäude
- Stromspeicher + ggf. Wärmespeicher für Regelung der Energiezu-/abflüsse (Digitale Messtechnik)

**Wasserstoff als Speichermedium:**
- Überdimensionierte PV → Elektrolyseur → Wasserstoffspeicher (Druckflaschen, außerhalb des Hauses) → Brennstoffzelle → Strom + Wärme
- Ab 1,5 kW Elektrolyseur-Leistung: Anlagen für Wohnhäuser verfügbar
- Systembestandteile: PV, Elektrolyseur, Wasserstoffspeicher, Wärmespeicher, Batterie

**Biogas-Potentiale bis 2050:**
- Erdgas: aktuell ca. 44 % des Primärenergieträgermix privater Haushalte
- Substituierbar durch heimische Grüngaserzeugung: bis zu ~400 TWh bis 2050 (ca. Hälfte des heutigen Gasbedarfs)
- Davon bis zu 250 TWh/a aus Biogasen (anaerobe Vergärung von Speiseabfällen, Ernteresten, Gülle, Abfallholz) + Energie-/Winterpflanzen
- Synthetische Kraftstoffe (Wasserstoff, Methan) aus überschüssigem Strom: weiteres Potential

**Idealbild Energiewendehaus:**
- Elektrische Grundversorgung: Brennstoffzelle (mit Biogas), stromgeführt betrieben
- Abwärme der Brennstoffzelle: Heizsystem
- Überschussstrom: in Batterien gepuffert
- Elektrische Wärmepumpe: Heizen und Kühlen
- PV-Anlage: an Batterien angeschlossen (weiterer Eigenstrombeitrag)
- Ziel: größten Teil des Stroms selbst erzeugen, anfallende Abwärme vollständig nutzen

**Konkretes Beispielgebäude (Berlin, gebaut 2019–2021):**
- Brennstoffzelle: SOFC (Festoxid-Brennstoffzelle, oxidkeramisch), stromgeführt, elektrischer Wirkungsgrad > 60 %, ganzjährig
- Gasversorgung: 100 % zertifiziertes Biogas (CO2-neutral aus Herstellung + Transport)
- Stromspeicher: Vanadium-Redox-Flow-Batterien (Lithium-frei, ressourcenschonend)
- Überschussstrom aus Brennstoffzelle + PV: in Redox-Flow-Batterien; kein Netzeinspeis (Netzentlastung)
- Wärmepumpe für Heizen und Kühlen; Strom dafür aus Brennstoffzelle
- E-Mobilität: 2 Wallboxen integriert; bei Bidirektional-Laden könnten Elektroauto-Batterien (~140 kWh) als Puffer für mehrere Tage dienen (bidirektionale Steckersysteme in Europa noch nicht üblich)

**Skalierbarkeit und Adaptivität:**
- Batteriekapazität verdreifacht: alle Leistungsspitzen (Aufzug, Herd) versorgbar
- Gasversorgung kritisch → vollständig elektrischer Betrieb (ohne Brennstoffzelle) möglich mit wenigen Hydraulik-Änderungen
- PV-Anlage verdreifacht + Elektrolyseur → Wasserstoffbevorratung, Brennstoffzelle ohne externe Gasliefer­ung
- Energiemonitoring (2021) bestätigt Simulationen und Auslegungen

---

### Serviceteil: Messeinheiten und Stoffwerte

**Flächeninhalt:**
- 1 Ar = 100 m²; 1 ha (Hektar) = 100 Ar = 10.000 m²

**Druck:**
- 1 bar = 10 N/cm² = 10⁵ N/m² = 10⁵ Pa = 1.000 hPa
- 1 bar = 10,2 m Wassersäule
- 1 mm Wassersäule = 9,81 Pa

**Energie/Arbeit/Wärmemenge:**
- 1 J = 1 Nm = 1 Ws = 1 kg·m²/s²
- 1 kWh = 3,6 × 10⁶ Ws (= 3,6 MJ)

**Leistung/Wärmestrom:**
- 1 W = 1 J/s = 1 Nm/s = 1 V·A

**Temperatur:**
- 0 K = −273 °C (absoluter Nullpunkt)
- 273 K = 0 °C (Gefrierpunkt Wasser)
- 373 K = +100 °C (Siedepunkt Wasser)

**Wärmetechnische Kenngrößen:**
- Wärmeleitfähigkeit λ: W/(m·K)
- Wärmedurchgangskoeffizient U: W/(m²·K)
- Wärmedurchlasswiderstand 1/Λ: m²·(K/W)
- Wärmeübergangskoeffizient α: W/(m²·K)

**Dezimale Einheitenvorsätze:**

| Vorsatz | Zeichen | Faktor |
|---------|---------|--------|
| Deka | da | 10¹ |
| Hekto | h | 10² |
| Kilo | k | 10³ |
| Mega | M | 10⁶ |
| Giga | G | 10⁹ |
| Tera | T | 10¹² |
| Dezi | d | 10⁻¹ |
| Centi | c | 10⁻² |
| Milli | m | 10⁻³ |
| Mikro | µ | 10⁻⁶ |
| Nano | n | 10⁻⁹ |
| Piko | p | 10⁻¹² |

Vollständige Vorsatzliste nach DIN 1301 (Exa E 10¹⁸ bis Atto a 10⁻¹⁸).

**Dichte von Festkörpern bei 20 °C:**
- Roheisen: 6,7–7,8 kg/dm³
- Kupfer: 8,3–9,0 kg/dm³
- Beton, leicht: 0,7–1,5 kg/dm³
- Gips (gegossen): 1,0 kg/dm³
- Holz, frisch (Eiche): 0,9–1,2 kg/dm³
- Sandstein: 2,2–2,7 kg/dm³
- Ton: 1,6–2,6 kg/dm³

**Dichte von Luft (trocken, 1 bar):**
- 0 °C: 1,275 kg/m³
- 20 °C: 1,188 kg/m³
- 100 °C: 0,933 kg/m³
- 1.000 °C: 0,273 kg/m³

**Dichte von Flüssigkeiten bei 20 °C:**
- Heizöl EL: 0,8 kg/dm³
- Wasser bei 4 °C: 1,0 kg/dm³
- Eis bei 0 °C: 0,916 kg/dm³

**Spezifische Wärmekapazität:**
- Aluminium: 0,942 kJ/(kg·K)
- Eisen (0–1.000 °C): 0,71 kJ/(kg·K)
- Ziegelstein: 0,84 kJ/(kg·K)
- Holz, Fichte: 2,70 kJ/(kg·K)
- Wasser: 4,182 kJ/(kg·K)
- Luft: 1,0 kJ/(kg·K)

**Brennstoffe — Heizwert, Brennwert, CO2-Emission bei vollständiger Verbrennung:**

| Brennstoff | Heizwert | Brennwert | CO2-Emission (kg/kWh, Heizwert) | CO2-Emission (kg/kWh, Brennwert) |
|------------|----------|-----------|----------------------------------|-----------------------------------|
| Steinkohle | 8,14 kWh/kg | 8,41 kWh/kg | 0,350 | 0,339 |
| Heizöl EL | 10,08 kWh/l | 10,57 kWh/l | 0,312 | 0,298 |
| Erdgas L | 8,87 kWh/m³ | 9,76 kWh/m³ | 0,200 | 0,182 |
| Erdgas H | 10,42 kWh/m³ | 11,42 kWh/m³ | 0,200 | 0,182 |

**Energieeinheiten-Umrechnung:**
- 1 J = 2,778 × 10⁻⁷ kWh
- 1 kWh = 3,6 × 10⁶ J

**Druckeinheiten-Umrechnung:**
- 1 Pa = 10⁻⁵ bar = 0,102 m WS
- 1 bar = 10⁵ Pa = 10² kPa = 1,02 × 10⁴ m WS
- 1 mbar = 1 hPa = 10⁻³ bar = 10,2 mm WS

**Umrechnung alter Maßeinheiten:**
- Kraft: 1 kp = 9,81 N
- Druck: 1 kp/cm² = 0,981 bar = 10.000 mm WS
- Wärmeleistung: 1 kcal = 1,16 W = 4,19 kJ
- Wärmemenge: 1 Wh = 0,86 kcal; 1 kWh = 860 kcal/h
- Wärmeleitfähigkeit: 1 kcal/(m·h) = 1,16 W/(m·K)
- Wärmeübergang: 1 kcal/(m²·h·°C) = 1,16 W/(m²·K)
- Wärmeübergangswiderstand: 1 m²·h·°C/kcal = 0,86 m²·K/W

---

### Literaturverzeichnis (Auswahl nach Themengebiet)

**Grundlagen (u.a.):**
- Daniels K.: Gebäudetechnik (3. Aufl. 2000, Oldenbourg)
- Recknagel/Sprenger/Schramek: Taschenbuch Heizung-Klimatechnik (80. Aufl. 2021/22, Oldenbourg)
- Neufert E./P.: Bauentwurfslehre (43. Aufl. 2021, Springer Wiesbaden)
- Laasch T./E.: Haustechnik (13. Aufl. 2013, Springer Vieweg)

**Wärme- und Kälteversorgung:**
- Bohne D.: Ökologische Gebäudetechnik (1. Aufl. 2004, Kohlhammer)
- Feist W.: Gestaltungsgrundlagen Passivhäuser (2011)
- Ochsner K.: Wärmepumpen in der Heizungstechnik (5. Aufl. 2015, VDE)
- Kaltschmitt/Streiker/Wiese: Erneuerbare Energien und Systemtechnik (6. Aufl. 2020, Springer)

**Elektrotechnik:**
- Hösl/Ayx/Busch: Die vorschriftsmäßige Elektroinstallation (21. Aufl. 2016, VDE)
- Trommer/Hampe: Blitzschutzanlagen (3. Aufl. 2004, Hüthig)
- Waldner P.: Grundlagen elektrotechnische/elektronische Gebäudeausrüstung (2. Aufl. 2002, Werner)

**Normen und Gesetze:** DIN, VDI, VDE unter www.beuth.de; Gesetze unter www.umwelt-online.de

**Energiekonzepte:**
- Fisch/Möws/Zieger: Solarstadt (2001, Kohlhammer)
- Fisch et al.: EnergiePLUS – Gebäude und Quartiere als erneuerbare Energiequellen (IGS TU Braunschweig 2014)
- Wesselak/Voswinckel: Photovoltaik (2012, Springer Heidelberg)

---

### Stichwortverzeichnis (ausgewählte technische Einträge mit Seitenangaben aus dem Buch)

Das vollständige Stichwortverzeichnis (Seiten 665–669) umfasst alle Kapitelthemen A–Z. Relevante Einträge für Elektrotechnik/Gebäudetechnik-Praxis (Auswahl):

- Ausstattungswerte für Wohnungen (476)
- Batterieanlagen (498); Batteriebehälter (224)
- Beleuchtungsanlagen (503); Beleuchtungsstärke (504); Beleuchtungsniveau und Gleichmäßigkeit (519)
- Blitzschutz- und Erdungsanlagen (535); Blitzstrom-Ableiter (541); äußerer/innerer Blitzschutz (536/540)
- Brandmeldeanlagen BMA (563); Brandmelder automatische (563); Brandmeldezentralen (564)
- Einbruchmeldeanlagen EMA (564)
- Elektrische Direktheizung (337); elektrische Fußbodenspeicherheizung (336); elektrische Raumheizsysteme (335)
- Elektroinstallationen im Wohnungsbau, raumspezifische (471); Elektro-Installationsplan Wohnung (475)
- Fehlerstromschutzschalter (456)
- Fernmelde- und Informationstechnik (552); Fernseh- und Antennenanlage (559)
- Gebäudeautomation (577); Gebäudeleittechnik (327)
- Installationszonen (462); Installationszonen für elektrische Installationen (463)
- Kennzeichnung der 3 Schutzklassen von Elektrogeräten (489)
- Kinderschutz-Steckdosen (469)
- Leitungsführung im Nichtwohnungsbau (489); Leitungsführung und -Verlegung (461)
- Leitungsmaterial (458); Mantelleitung NYM (460); Kunststoffkabel NYY (461)
- Mess-, Steuer- und Regelungstechnik (577)
- Niederspannungsanlagen (452); Niederspannungsanschluss 230/400 V (446)
- Notbeleuchtung (498); Notstromversorgungsanlagen (498); zentrale Notstrombatterien (500)
- Photovoltaikanlagen (542, 625); Fassadenintegration PV (546)
- Potentialausgleichsschiene (483, 484); Fundamenterder (482, 539)
- Rettungszeichen-Leuchten (499); Sicherheitsbeleuchtung mit Einzelbatterien (501)
- Schalter und Steckdosen (465); Schalterarten (466); Schalterbetätigungsarten (467)
- Sicherheitsleuchten (499)
- Smart Home (638)
- Stromkreise (456); Stromnetze (454); Stromspeicher (626); Strombedarf für Gebäude (620)
- Stromerzeugung und -speicherung (625)
- Such- und Signalanlagen (556); Türöffneranlagen (556); Türsprechanlagen (557)
- Telekommunikationsanlage (552); Zeitdienstanlagen (558)
- Überspannungs-Ableiter (541); Überstrom-Schutzeinrichtungen (456)
- USV-Anlagen (503)
- Zähleranlagen bei Niederspannungseinspeisung (452); dezentrale/zentrale Zähleranlage (453/453)
