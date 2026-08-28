# Lehrbuch der Bauphysik — Teil 4
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 161-200.

Dieser Teil behandelt die Bewertung von Energieeinsparmaßnahmen im Gebäudebestand (Kap. 7) sowie wärmeschutztechnische Anforderungen nach DIN 4108 und dem Gebäudeenergiegesetz 2020 (Kap. 8), einschließlich Mindestwärmeschutz, sommerlichem Wärmeschutz und vollständigem GEG-Nachweisbeispiel für ein Einfamilienhaus.

## Inhalt

### Abschluss Kapitel 6 — Instationäres Wärmeverhalten (Seite 161–166)

- Einfluss des Fensterflächenanteils auf die Raumlufttemperatur: Zwischen 30 % und 70 % Fensterflächenanteil steigt die mittlere Raumlufttemperatur im eingeschwungenen Zustand um etwa 1,5 K, sofern ein dauerhaft wirksamer außenliegender Sonnenschutz vorhanden ist.
- Einschwingverhalten bei Leicht- vs. Schwerbauart: Leichte Bauart zeigt bereits ab Tag 1 deutlich größere Temperaturschwankungen. Schwerbauart liegt anfangs im unteren Bereich der leichten Schwankungsbreite und erreicht erst nach etwa 15 Tagen deren Mittelwert. Im eingeschwungenen Zustand sind die Tagesmitteltemperaturen vergleichbar; die tägliche Schwankungsbreite ist bei Leichtbauart höher.
- Orientierungseinfluss: Tagesmitteltemperaturen für Ost-, Süd- und Westorientierung unterscheiden sich nur gering. Höchstwert nachmittags bei Westkonfiguration: ca. 31,5 °C (Überlagerung von Außentemperatur und Solarstrahlung). Nordorientierung liefert niedrigere Werte, aber nur bei aktiviertem Sonnenschutz; ohne Sonnenschutz lägen Nordwerte höher als die übrigen (da kein Abminderungseffekt).

**Tabelle 6.5 — Interne Wärmequellen bei Wohnnutzung [W]:**

| Quelle | MFH | EFH |
|---|---|---|
| Fernseher | 35 | 35 |
| Kühlschrank | 37 | 25 |
| E-Herd | 14 | 21 |
| Spülmaschine | 5 | 7 |
| Waschen | 4 | 0 |
| Trocknen | 38 | 0 |
| Elektronik | 85 | 85 |
| Kleingeräte | 11 | 17 |
| Personen | 88 | 132 |
| Beleuchtung | 33 | 50 |
| Verdunstung | −50 | −75 |
| Kaltwasser | −10 | −15 |
| **Summe** | **290** | **282** |

---

### Kapitel 7 — Bewertung von Maßnahmen zur Heizenergieeinsparung

#### 7.1 Bauliche Maßnahmen

- Berechnungsgrundlage: Das Heizperiodenbilanzverfahren nach DIN V 4108-6 dient als Basis für überschlägige bauteilbezogene Abschätzungen.
- Formel für bauteilbezogenen Heizwärmebedarf:  
  `Qh,Bauteil = Fx × U × ABauteil × FGt`  
  — mit UIST ergibt sich der Ist-Zustand, mit UNEU der sanierte Zustand.

**Tabelle 7.1 — Berechnungsgrößen (Anlehnung an Heizperiodenbilanzverfahren, SF nach WSchVO 1995):**

| Zeichen | Wert/Einheit | Bedeutung |
|---|---|---|
| Fx | = 1,0 | Außenbauteil (Wand, Fenster, Dach) |
| Fx | = 0,8 | Oberste Geschossdecke, Abseitenwand |
| Fx | = 0,5 | Decken/Wände zu unbeheizten Räumen |
| Fx | = 0,6 | Unterer Gebäudeabschluss (Kellerdecke/-wände, Fußboden auf Erdreich, Flächen beheizter Keller gegen Erdreich) |
| ABauteil | [m²] | Bauteilfläche in Außenmaßen |
| FGt | = 82 kKh/a | Heizperiode 275 Tage, Heizgrenztemperatur 15 °C (nicht saniert) |
| FGt | = 75 kKh/a | Heizperiode 220 Tage, Heizgrenztemperatur 12 °C (teilsaniert) — Standardwert für Überschlagsrechnung |
| FGt | = 66 kKh/a | Heizperiode 185 Tage, Heizgrenztemperatur 10 °C (Neubauniveau) |
| SF | = 0,95 W/(m²K) | Strahlungsgewinnkoeffizient Nordfassade |
| SF | = 1,65 W/(m²K) | Ost-/Westfassade und Dachflächenfenster (Neigung < 15°) |
| SF | = 2,40 W/(m²K) | Südfassade |

- Fenster: Statt des direkten U-Wertes wird ein äquivalenter U-Wert eingesetzt, der passive Solargewinne einbezieht:  
  `UW,eq = UW − g × SF`

#### 7.2 Anlagentechnische Maßnahmen

**Tabelle 7.2 — Endenergie-Aufwandszahlen für Raumheizung und Warmwasserbereitung (ohne Primärenergiefaktoren, ohne elektrische Hilfsenergie):**

| Anlage | Baualter | EFH | MFH |
|---|---|---|---|
| Standardkessel (auch Holzkessel) | bis 1986 | 1,52 | 1,32 |
| | 1987–1994 | 1,39 | 1,22 |
| | ab 1995 | 1,36 | 1,20 |
| Niedertemperaturkessel Öl/Gas | bis 1986 | 1,24 | 1,16 |
| | 1987–1994 | 1,20 | 1,11 |
| | ab 1995 | 1,14 | 1,06 |
| Gas-Brennwertkessel | bis 1994 | 1,10 | 1,02 |
| | ab 1995 | 1,07 | 1,01 |
| Elektrowärmepumpe Erdreich | bis 1994 | 0,36 | 0,34 |
| | ab 1995 | 0,30 | 0,29 |
| Elektrowärmepumpe Luft | bis 1994 | 0,45 | 0,42 |
| | ab 1995 | 0,42 | 0,41 |
| Elektro-Nachtspeicherheizung | — | 1,1 | — |
| Elektro-Direktheizgerät | — | 1,0 | — |
| Gas-Raumheizer | — | 1,4 | — |
| Ölofen | — | 1,4 | — |
| Kohle- oder Holzofen | — | 1,6 | — |

#### 7.3 Heizenergiebedarf und Heizenergieeinsparung

- Heizenergiebedarf für Wärmeerzeugung (Endenergie ohne Hilfsenergie):  
  `QE* = Qh × e`
- Heizenergieeinsparung:  
  `ΔQE* = QE*,IST − QE*,NEU`
- Bei rein baulichen Maßnahmen (gleiche Anlagentechnik):  
  `ΔQE* = (Qh,Bauteil,IST − Qh,Bauteil,NEU) × e`

#### 7.4 Brennstoffeinsparung

**Tabelle 7.3 — Energiegehalt und Brennstoffkosten (Anhaltswerte):**

| Energieträger | Energiegehalt b | Kosten k [EUR/kWh] |
|---|---|---|
| Braunkohle | 6 kWh/kg | 0,06 |
| Steinkohle | 9 kWh/kg | 0,06 |
| Brennholz | 4 kWh/kg | 0,03 |
| Pellets | 5 kWh/kg | 0,05 |
| Erdgas | 10 kWh/m³ | 0,075 |
| Heizöl | 10 kWh/l | 0,08 |
| Strommix | 1 | 0,30 |
| Fernwärme | 1 | 0,08 |

- Brennstoffeinsparung: `ΔB = ΔQE* / b`
- Energiekosteneinsparung: `ΔK = ΔQE* × k`  
  Bei Energieträgerwechsel: `ΔK = QE*,IST × kIST − QE*,NEU × kNEU`

#### 7.5 Wirtschaftlichkeit und Amortisationszeit

- Dynamische Amortisationszeit (berücksichtigt Energiepreissteigerung + Kapitalverzinsung):  
  `n = ln[j × (q − i) / q + 1] / ln(q / i)`  
  mit  
  `j = Investitionskosten / jährliche Heizkostenersparnis` (statische Amortisationszeit)  
  `i = 1 + Pv/100` (Pv = Energiepreissteigerung in %)  
  `q = 1 + p/100` (p = Zinssatz in %)
- Die Amortisationszeit ist aussagekräftig, wenn sie unter der rechnerischen Nutzungsdauer der betreffenden Komponente liegt (15–30 Jahre je nach Bauteil/Anlage, Quelle VDI 2067).
- Bei ohnehin fälligen Erneuerungen (z. B. defekte Fenster) entstehen keine zusätzlichen Investitionskosten für die Energieeinsparmaßnahme.
- Für Mehrkosten gegenüber gesetzlichem Mindeststandard (GEG) können diese als Investitionskosten angesetzt werden.
- Referenzberechnung: Zinssatz 4 %, inflationsbereinigte Energiepreissteigerung 2 % → Amortisationszeit aus Verhältnis IK/ΔK ablesbar.

#### 7.6 Rechenbeispiele

**Beispiel 1 — Außenwanddämmung:**
- Ausgangszustand: 24 cm Außenwand, U = 1,4 W/(m²K)
- Sanierung: 14 cm Wärmedämmverbundsystem, U = 0,24 W/(m²K)
- Heizwärmebedarf IST (je m², Heizperiode 220 Tage): `1 × 1,4 × 1 × 75 = 105 kWh/a`
- Heizwärmebedarf NEU (je m²): `1 × 0,24 × 1 × 75 = 18 kWh/a`
- Brennwertheizung Öl, Baujahr 2002: e = 1,07 → Heizenergieeinsparung: ca. 93 kWh/(m²·a)
- EFH mit 120 m² Außenwandfläche: Jahreseinsparung Heizenergie ΔQe ≈ 11.170 kWh/a, Brennstoffeinsparung ΔB ≈ 1.170 l Heizöl/a
- Kosteneinsparung: 0,08 EUR/kWh × Energieeinsparung → ca. 890 EUR/a
- Maßnahmenkosten isoliert: ca. 18.000 EUR → Amortisationszeit ca. 26 Jahre
- Maßnahmenkosten kombiniert mit ohnehin nötiger Außenputzerneuerung: ca. 8.000 EUR → Amortisationszeit ca. 11 Jahre

**Beispiel 2 — Fenstererneuerung:**
- Alt: Einfachverglasung, UW = 4,7 W/(m²K), g = 0,87; UW,eq (Ost/West) = 3,3 W/(m²K)
- Neu: Wärmeschutzverglasung, UW = 1,3 W/(m²K), g = 0,60; UW,eq (Ost/West) = 0,3 W/(m²K)
- Heizwärmebedarf IST (je m², 220 Tage): `1 × 3,3 × 1 × 75 = 248 kWh/a`
- Heizwärmebedarf NEU (je m²): `1 × 0,3 × 1 × 75 = 23 kWh/a`
- Brennwertheizung Gas, Baujahr 2002: e = 1,07 → Einsparung 240 kWh/(m²·a)
- EFH mit 25 m² Fensterfläche: Jahreseinsparung ΔQE ≈ 6.000 kWh/a, ΔB ≈ 600 m³ Erdgas/a
- Kosteneinsparung: 0,075 EUR/kWh → ca. 450 EUR/a
- Maßnahmenkosten ca. 10.000 EUR → Amortisationszeit ca. 28 Jahre

---

### Kapitel 8 — Wärmeschutztechnische Anforderungen

#### 8.1 Mindestwärmeschutz nach DIN 4108

- Vorschriften unterteilen sich in:
  - **Mindestwärmeschutz** (DIN 4108 „Wärmeschutz und Energie-Einsparungen in Gebäuden")
  - **Energiesparender Wärmeschutz** (Gebäudeenergiegesetz GEG)

#### 8.1.1 Mindestwärmedurchlasswiderstände

- Nichttransparente Außenbauteile von Aufenthaltsräumen mit flächenbezogener Gesamtmasse ≥ 100 kg/m² müssen folgende Mindestwärmedurchlasswiderstände R einhalten:

**Tabelle 8.1 — Mindestwerte Wärmedurchlasswiderstand R [m²·K/W]:**

| Nr. | Bauteilart | Beschreibung | R [m²·K/W] |
|---|---|---|---|
| 1 | Wände beheizter Räume | gegen Außenluft, Erdreich, Tiefgaragen, unbeheizte Räume | 1,2 (bei niedrig beheizt: 0,55) |
| 2 | Dachschrägen beheizter Räume | gegen Außenluft | 1,2 |
| 3.1 | Decken nach oben / Flachdächer | gegen Außenluft | 1,2 |
| 3.2 | Decken nach oben | zu belüfteten Räumen zwischen Dachschräge und Abseitenwand (ausgebauter Dachraum) | 0,90 |
| 3.3 | Decken nach oben | zu unbeheizten Räumen, bekriechbaren oder niedrigeren Räumen | 0,90 |
| 3.4 | Decken nach oben | zu Räumen zwischen gedämmten Dachschrägen und Abseitenwänden | 0,35 |
| 4.1 | Decken beheizter Räume nach unten | gegen Außenluft, Tiefgarage, Garagen, Durchfahrten, belüftete Kriechkeller | 1,75 |
| 4.2 | Decken nach unten | gegen unbeheizten Kellerraum | 0,90 |
| 4.3/4.4 | Unterer Abschluss | Sohlplatte / Erdreich bis 5 m Raumtiefe; über nicht belüfteten Kriechkeller | — |
| 5.1 | Treppenraumwände | zwischen beheiztem Raum und direkt/indirekt beheiztem Treppenraum (wenn alle übrigen TR-Bauteile Tab. 8.3 erfüllen) | 0,07 |
| 5.2 | Treppenraumwände | zwischen beheiztem Raum und indirekt beheiztem TR, wenn nicht alle anderen TR-Bauteile Anforderungen erfüllen | 0,25 |
| 5.3 | Oberer/unterer Abschluss TR | beheizter oder indirekt beheizter Treppenraum | wie Bauteile beheizter Räume |
| 6.1 | Wohnungs-/Gebäudetrennwände | zwischen beheizten Räumen | 0,07 |
| 6.2 | Wohnungstrenndecken | zwischen Räumen unterschiedlicher Nutzung | 0,35 |

- Bauteile mit flächenbezogener Gesamtmasse < 100 kg/m²: erhöhte Anforderung R ≥ 1,75 m²·K/W.
- Bei Rahmen-/Skelettbauart und Pfosten-Riegel-Fassaden gilt der Mindestwert nur für den Gefachbereich; für das gesamte Bauteil zusätzlich im Mittel R ≥ 1,0 m²·K/W.
- Rollladenkästen: Gleiches gilt; für den Rollladenkasten-Deckel: R ≥ 0,55 m²·K/W.
- Mindestwärmeschutz muss an jeder Stelle vorhanden sein, einschließlich Nischen unter Fenstern, Brüstungen, Fensterstürze, Wandbereiche hinter Heizkörpern, Rohrkanälen und in Außenwänden geführten wasserführenden Leitungen.
- Opake Ausfachungen transparenter Bauteile (Vorhangfassaden, Pfosten-Riegel, Glasdächer, Fenster, Fenstertüren): R ≥ 1,2 m²·K/W (= Up ≤ 0,73 W/(m²·K)).
- Rahmen dieser Bauteile: Uf ≤ 2,9 W/(m²·K) nach DIN EN ISO 10077-1.
- Transparente Teile der thermischen Hülle: mindestens Isolierglas oder zwei Glasscheiben (Verbundfenster, Kastenfenster).
- Berechnungsverfahren: Wärmedurchlasswiderstand/Wärmedurchgangskoeffizient nach DIN EN ISO 6946; Bemessungswerte der Baustoffe aus DIN 4108-4, DIN EN ISO 10456 oder bauaufsichtlichen Regelungen.
- Bei der Berechnung von R werden nur Schichten bis zur Bauwerks- oder Dachabdichtung berücksichtigt.

**Sonderregelungen Umkehrdächer (Dämmung aus XPS über Abdichtung, mit Kies- oder Betonplattenbelag):**

| Anteil Wärmedurchlasswiderstand raumseitig zur Abdichtung [%] | Zuschlagswert ΔU [W/(m²·K)] |
|---|---|
| unter 10 | 0,05 |
| 10 bis 50 | 0,03 |
| über 50 | 0 |

- Bei leichter Unterkonstruktion (< 250 kg/m²): Wärmedurchlasswiderstand unterhalb der Abdichtung mindestens 0,15 m²·K/W.
- Perimeterdämmung (außenliegende Dämmung erdberührender Flächen, außer unter Gründungen, aus XPS oder Schaumglas, nicht dauerhaft im Grundwasser): wird in Wärmedurchgangskoeffizient einbezogen.

#### 8.1.2 Schimmelpilzschutz

- Anforderung: Temperaturfaktor fRsi ≥ 0,70 an der ungünstigsten Stelle → Mindest-Oberflächentemperatur innen θsi ≥ 12,6 °C.
- Ausgenommen: Fenster.
- Randbedingungen für den Nachweis:
  - Innenlufttemperatur: 20 °C
  - Relative Luftfeuchte innen: 50 %
  - Kritische Oberflächenluftfeuchtigkeit für Schimmelpilz (nach DIN EN ISO 13788): φsi = 80 %
  - Außenlufttemperatur: −5 °C
  - Wärmeübergangswiderstand innen (beheizte Räume): Rsi = 0,25 m²·K/W
  - Wärmeübergangswiderstand innen (unbeheizte Räume): Rsi = 0,17 m²·K/W
  - Wärmeübergangswiderstand außen: Rse = 0,04 m²·K/W

---

#### 8.2 Sommerlicher Wärmeschutz nach DIN 4108-2

##### 8.2.1 Klimaregionen

- Deutschland ist in drei Sommer-Klimaregionen unterteilt (nach Abb. 8.2):
  - Region A (gemäßigt)
  - Region B (mittleres Anforderungsniveau)
  - Region C (höchstes Anforderungsniveau)
- Bei Zweifelsfällen gelten folgende Zuordnungsregeln:
  - Zwischen A und B → nach B
  - Zwischen B und C → nach C
  - Zwischen A und C → nach C

##### 8.2.2 Nachweisverfahren

**Verzicht auf Nachweis möglich, wenn:**

a) Grundflächenbezogener Fensterflächenanteil fWG unter folgendem Grenzwert:

| Fensterneigung | Orientierung | fWG-Grenzwert [%] |
|---|---|---|
| > 60° bis 90° | NW über S bis NO | 10 |
| > 60° bis 90° | Alle anderen Nordorientierungen | 15 |
| 0° bis 60° | Alle Orientierungen | 7 |

b) Wohngebäude mit fWG ≤ 35 %, Fenster in Ost-, Süd- oder Westlage mit außenliegendem Sonnenschutz:
  - FC ≤ 0,30 bei Glas mit g > 0,40
  - FC ≤ 0,35 bei Glas mit g ≤ 0,40
  — Gilt nicht für Glasvorbauten (Wintergärten).

**Räume mit unbeheizten Glasvorbauten:**

- Belüftung nur über Glasvorbau: Nachweis gilt als erfüllt, wenn Glasvorbau Sonnenschutz FC ≤ 0,35 hat und Lüftungsöffnungen im obersten und untersten Glasbereich zusammen ≥ 10 % der Glasfläche umfassen; sonst Nachweis mit Sonneneintragskennwertverfahren.
- Belüftung nicht (oder nicht nur) über Glasvorbau: Nachweis kann geführt werden, als wäre der Glasvorbau nicht vorhanden; bei thermischer Simulation ist Vorbau einzubeziehen.

**Allgemeine Berechnungsrandbedingungen:**

- Raumtiefe: maximale Ansatztiefe = 3× lichte Raumhöhe; bei gegenüberliegenden Fassaden keine Begrenzung, wenn Fassadenabstand ≤ 6× lichte Raumhöhe; bei größerem Abstand: zwei separate Raumbereiche nachweisen.
- Fensterfläche AW: lichtes Rohbaumaß = Blendrahmenaußenmaß + Einbaufuge (ohne Putz). Bei Dachflächenfenstern: Außenmaß des Blendrahmens.
- Das vereinfachte Sonneneintragskennwert-Verfahren basiert auf einem Fensterrahmenanteil von 30 %; bei stark abweichenden Rahmenanteilen ist thermische Simulation erforderlich.
- Das vereinfachte Verfahren ist nicht anwendbar bei Doppelfassaden oder transparenten Wärmedämmsystemen (TWD).

##### 8.2.3 Sonneneintragskennwert-Verfahren

**Vorhandener Sonneneintragskennwert:**

`Svorh = Σ(Aw,j × gtotal,j) / AG`

- Aw: Fensterfläche [m²]
- gtotal = g × FC (vereinfacht nach Gl. 8.3; alternativ nach DIN EN ISO 52022-1/-2 oder DIN EN 410)
- AG: Nettogrundfläche [m²]
- Bei baulicher Verschattung: Modifikation von gtotal über Teilbestrahlungsfaktoren FS gemäß DIN V 18599-2, Anhang A.2 (Sommerfall; keine Mehrfachberücksichtigung einzelner Einflüsse)

**Zulässiger Sonneneintragskennwert:**

`Szul = Σ Sx` (Summe anteiliger Kennwerte S1 bis S6)

Nachweis erfüllt, wenn Svorh ≤ Szul.

**Tabelle 8.4 — Abminderungsfaktoren FC für fest installierte Sonnenschutzvorrichtungen:**

| Nr. | Sonnenschutzvorrichtung | 2-fach Sonnenschutzglas | 3-fach WD-Glas | 2-fach WD-Glas |
|---|---|---|---|---|
| 1 | Ohne Sonnenschutz | 1,00 | 1,00 | 1,00 |
| 2.1 | Innenliegend, weiß/hochreflektierend (Transparenz ≤ 10 %, Reflexion ≥ 60 %) | 0,65 | 0,70 | 0,65 |
| 2.2 | Innenliegend, helle Farben / geringe Transparenz (< 15 %) | 0,75 | 0,80 | 0,75 |
| 2.3 | Innenliegend, dunkle Farben / höhere Transparenz | 0,90 | 0,90 | 0,85 |
| 3.1.1 | Außen: Fensterläden / Rollläden, ¾ geschlossen | 0,35 | 0,30 | 0,30 |
| 3.1.2 | Außen: Fensterläden / Rollläden, geschlossen | 0,15 | 0,10 | 0,10 |
| 3.2.1 | Außen: Jalousie / Raffstore, 45° Lamellenstellung | 0,30 | 0,25 | 0,25 |
| 3.2.2 | Außen: Jalousie / Raffstore, 10° Lamellenstellung | 0,20 | 0,15 | 0,15 |
| 3.3 | Außen: Markise, parallel zur Verglasung | 0,30 | 0,25 | 0,25 |
| 3.4 | Vordächer, Markisen allgemein, freistehende Lamellen | 0,55 | 0,50 | 0,50 |

- Dekorative Vorhänge gelten nicht als Sonnenschutzvorrichtung.
- Für Markisen/Vordächer (Zeile 3.4): FC-Wert gilt nur, wenn keine direkte Besonnung des Fensters erfolgt:
  - Südorientierung: Abdeckwinkel β ≥ 50°
  - Ost-/Westorientierung: β ≥ 85° und γ ≥ 115°
  - Zwischenorientierungen: β ≥ 80°
  - Winkelbereiche je Orientierung: ±22,5°

**Tabelle 8.5 — Anteilige Sonneneintragskennwerte Sx:**

| Komponente | Parameter | Wohngebäude A/B/C | Nichtwohngebäude A/B/C |
|---|---|---|---|
| S1 – ohne Nachtlüftung | leicht | 0,071 / 0,056 / 0,041 | 0,013 / 0,007 / 0,000 |
| S1 – ohne Nachtlüftung | mittel | 0,080 / 0,067 / 0,054 | 0,020 / 0,013 / 0,006 |
| S1 – ohne Nachtlüftung | schwer | 0,087 / 0,074 / 0,061 | 0,025 / 0,018 / 0,011 |
| S1 – erhöhte Nachtlüftung (n ≥ 2 h⁻¹) | leicht | 0,098 / 0,088 / 0,078 | 0,071 / 0,060 / 0,048 |
| S1 – erhöhte Nachtlüftung (n ≥ 2 h⁻¹) | mittel | 0,114 / 0,103 / 0,092 | 0,089 / 0,081 / 0,072 |
| S1 – erhöhte Nachtlüftung (n ≥ 2 h⁻¹) | schwer | 0,125 / 0,113 / 0,101 | 0,101 / 0,092 / 0,083 |
| S1 – hohe Nachtlüftung (n ≥ 5 h⁻¹) | leicht | 0,128 / 0,117 / 0,105 | 0,090 / 0,082 / 0,074 |
| S1 – hohe Nachtlüftung (n ≥ 5 h⁻¹) | mittel | 0,160 / 0,152 / 0,143 | 0,135 / 0,124 / 0,113 |
| S1 – hohe Nachtlüftung (n ≥ 5 h⁻¹) | schwer | 0,181 / 0,171 / 0,160 | 0,170 / 0,158 / 0,145 |
| S2 – Fensterflächenkorrektur | Wohngebäude | a = 0,060; b = 0,231 | a = 0,030; b = 0,115 |
| S3 – Sonnenschutzglas (g ≤ 0,40) | | +0,03 (flächenanteilig) | |
| S4 – Geneigte Fenster (0°–60°, fWG ≤ 0,15) | | −0,035 × fneig | |
| S5 – Nordfenster / dauerhaft verschattet | | +0,10 × fnord | |
| S6 – Passive Kühlung | leicht / mittel / schwer | +0,02 / +0,04 / +0,06 | |

- S2-Formel: `S2 = a − b × fWG` (fWG = AW/AG)
  - S2 positiv bei fWG < 25 %, negativ bei fWG > 25 % (Referenz-Fensterflächenanteil für S1 ist ca. 25 %)
- S3 bei gemischten Fensterflächen: `S3 = 0,03 × AW,gtot≤0,40 / AW,gesamt`
- S4: fneig = AW,neig / AW,gesamt
- S5: fnord = AW,nord / AW,gesamt (Fenster NO bis NW, Neigung > 60°, oder dauerhaft selbstverschattet)

**Bauarteinstufung:**
- Leicht: Cwirk/AG < 50 Wh/(K·m²)
- Mittel: 50 ≤ Cwirk/AG ≤ 130 Wh/(K·m²)
- Schwer: Cwirk/AG > 130 Wh/(K·m²)
- Berechnung der wirksamen Wärmekapazität: `Cwirk = Σ(ci × ρi × di × Ai)` nach DIN EN ISO 13786 (Periodendauer 1 Tag)

Vereinfachte Bauartzuordnung:
- **Mittel:** Stahlbetondecke + massive Innen- und Außenbauteile (ρ ≥ 600 kg/m³) + keine innenliegende Dämmung + keine abgehängte/abgedeckte Decke + keine hohen Räume (> 4,5 m)
- **Schwer:** wie mittel, aber ρ > 1.600 kg/m³
- Holzbau → üblicherweise leicht; Porenbeton bis ~700 kg/m³ → mittel; Beton/Kalksandstein → schwer

**Beispielrechnung Sonneneintragskennwert (Standort Kassel, Wohngebäude):**
- Randbedingungen: g = 0,58; FC = 1 (kein Sonnenschutz); AW = 7,65 m²; AG = 20,25 m²
- Vorhandener SEK: Svorh = (7,65 × 0,58 × 1) / 20,25 = 0,219
- Cwirk-Berechnung für den Raum (Tabelle):

| Bauteil | Baustoff | c [J/(kg·K)] | ρ [kg/m³] | d [m] | A [m²] | Cwirk [Wh/K] |
|---|---|---|---|---|---|---|
| AW | Gipsputz | 1000 | 1400 | 0,015 | 17,55 | 102,4 |
| AW | KS-MW | 1000 | 1600 | 0,085 | 17,55 | 663 |
| Decke | Kalkgipsputz | 1000 | 1400 | 0,01 | 20,25 | 78,75 |
| Decke | Betondecke | 1000 | 2400 | 0,09 | 20,25 | 1215 |
| Boden | Estrich | 1000 | 2000 | 0,05 | 20,25 | 562,5 |
| IW | Kalkgipsputz | 1000 | 1400 | 0,01 | 23,31 | 90,65 |
| IW | KS-MW | 1000 | 1600 | 0,058 | 23,31 | 600,88 |
| Tür | Holz | 1000 | 500 | 0,02 | 1,89 | 5,25 |
| **Summe** | | | | | | **3318,4 Wh/K** |

- Cwirk/AG = 3318,4 / 20,25 = 163,9 Wh/(m²·K) → Bauart **schwer**
- Aus Tab. 8.5 (Klimaregion B, erhöhte Nachtlüftung n ≥ 2 h⁻¹, schwer): S1 = 0,113
- fWG = 7,65 / 20,25 = 0,378 → S2 = 0,060 − 0,231 × 0,378 = −0,0273
- S3 bis S6 = 0 (kein Sonnenschutzglas, Neigung 90°, keine Nordfenster, keine passive Kühlung)
- Szul = 0,113 − 0,0273 = 0,0857
- Nachweis: Svorh = 0,219 > Szul = 0,0857 → **nicht erfüllt** ohne Sonnenschutz
- Mit außenliegendem Sonnenschutz FC = 0,25: Svorh = (7,65 × 0,58 × 0,25) / 20,25 = 0,0548 ≤ 0,0857 → **erfüllt**

---

#### 8.3 Gebäudeenergiegesetz 2020 (GEG)

##### 8.3.1 Entwicklungsgeschichte und Einführung

- Gesetzliche Grundlage: Energieeinspargesetz 1976 → Wärmeschutzverordnung/Heizungsanlagenverordnung 2002 → Energieeinsparverordnung (EnEV) 2002 → EnEV 2007 (neues NWG-Nachweisverfahren nach DIN V 18599, Referenzgebäudeverfahren, Energieausweis-Pflicht bei Verkauf/Vermietung) → EnEV 2009 (Anforderungsverschärfung: Primärenergiebedarf −30 %, U-Werte bei Bauteiländerungen −30 %, Gebäudehülle −15 %; Referenzgebäudeverfahren auch für WG; DIN V 18599 alternativ für WG) → EnEV 2014/2016 (Primärenergiebedarf −25 %, Transmissionswärmeverluste −20 % ggü. EnEV 2009) → GEG 2020.
- GEG 2020: Niedrigstenergiegebäude = Jahres-Primärenergiebedarf um 25 % unter Referenzgebäude. Anforderungsniveau gegenüber EnEV 2016 unverändert.
- Weiterentwicklung im GEG bis 2025 erwartet.

##### 8.3.2 Wohngebäude Neubau

**Anforderungsgrößen:**
- Jahres-Primärenergiebedarf QP
- Spezifischer Transmissionswärmeverlust HT′ (mittlerer Wärmedurchgangskoeffizient, bezogen auf wärmeübertragende Umfassungsfläche)

**Referenzgebäudeverfahren:**
1. Gleiche Gebäudegeometrie, Ausrichtung, Fenstergröße wie das geplante Gebäude.
2. Gebäudehülle mit Referenz-U-Werten (Tab. 8.6) + Referenzanlagentechnik ausstatten.
3. Jahres-Primärenergiebedarf des Referenzgebäudes berechnen → zulässiger Wert = 75 % davon (also −25 %).
4. Tatsächlich geplantes Gebäude mit tatsächlicher Ausführung muss diesen Wert einhalten.

**Tabelle 8.6 — Referenzausführung Wohngebäude GEG 2020:**

| Nr. | Bauteil/System | Referenzwert |
|---|---|---|
| 1.1 | Außenwand, Geschossdecke gegen Außenluft | U = 0,28 W/(m²·K) |
| 1.2 | Außenwand gegen Erdreich, Bodenplatte, Wände/Decken zu unbeheizten Räumen (außer 1.1) | U = 0,35 W/(m²·K) |
| 1.3 | Dach, oberste Geschossdecke, Wände zu Abseiten | U = 0,20 W/(m²·K) |
| 1.4 | Fenster, Fenstertüren | U = 1,3 W/(m²·K); g = 0,60 |
| 1.5 | Dachflächenfenster | U = 1,4 W/(m²·K); g = 0,60 |
| 1.6 | Lichtkuppeln | U = 2,7 W/(m²·K); g = 0,64 |
| 1.7 | Außentüren | U = 1,8 W/(m²·K) |
| 2 | Wärmebrückenzuschlag (für alle Bauteile 1.1–1.7) | ΔUWB = 0,05 W/(m²·K) |
| 3 | Luftdichtheit | DIN V 4108-6: mit Dichtheitsprüfung; DIN V 18599-2: Kategorie I |

##### 8.3.2.2 Berechnungsbeispiel Wohngebäude EFH (GEG 2020)

Gebäudedaten:
- Freistehendes EFH, Keller + DG beheizt, Spitzboden unbeheizt
- Außenvolumen Ve = 669,00 m³
- Geschosshöhe hG = 2,75 m → fG = 0,32
- Nutzfläche AN = fG × Ve = 214,08 m²
- Anzahl Wohneinheiten: 1; Anzahl Geschosse: 2

Transmissionswärmeverluste (Auswahl Einzelbauteile):

| Bauteil | Orientierung | Neigung | Fläche [m²] | U [W/(m²·K)] | Fx | U·A·Fx [W/K] |
|---|---|---|---|---|---|---|
| AW 1 (Außenwand) | Nord | 90° | 30,30 | 0,18 | 1,0 | 5,45 |
| AW 2 | Süd | 90° | 23,30 | 0,18 | 1,0 | 4,19 |
| AW 3 | Ost | 90° | 50,70 | 0,18 | 1,0 | 9,13 |
| W 1 (Fenster) | Nord | 90° | 5,50 | 0,90 | 1,0 | 4,95 |
| W 2 | Süd | 90° | 12,50 | 0,90 | 1,0 | 11,25 |
| W 3 | Ost | 90° | 13,20 | 0,90 | 1,0 | 11,88 |
| T 1 (Haustür) | Ost | 90° | 2,10 | 1,8 | 1,0 | 3,78 |
| D 1 (Dach) | Ost | 45° | 84,90 | 0,18 | 1,0 | 15,28 |
| OG 1 (oberste Geschossdecke) | — | — | 36,00 | 0,18 | 0,8 | 5,18 |
| G 1 (Erdreich) | — | — | 96,00 | 0,3 | 0,45 | 12,96 |
| G 2 | — | — | 100,00 | 0,3 | 0,6 | 18,00 |

- Summe Hüllfläche A = 454,50 m²
- Spezifischer Transmissionswärmeverlust Bauteilflächen: HT = 102,06 W/K
- Wärmebrückenkorrektur: ΔUWB = 0,025 W/(m²·K) (detailliert nach DIN EN ISO 10211-2)  
  (Optionen: pauschal 0,10; optimiert Kat. A 0,05; optimiert Kat. B 0,03; detailliert = Eingabe)
- Gesamter spezifischer Transmissionswärmeverlust: HT = 102,06 + 0,025 × 454,50 = **113,42 W/K**
- Transmissionswärmeverlust: QT = 0,024 × HT × (19 − θe) × t = **9.394 kWh/a**

Lüftungswärmeverluste:
- Beheiztes Luftvolumen (Gebäude bis 3 Vollgeschosse): V = 0,76 × Ve = 508,44 m³
- Außenluftwechsel bei Dichtheitsprüfung/Fensterlüftung: n = 0,60 h⁻¹  
  (ohne Dichtheitsprüfung: 0,70; mit Zu-/Abluftanlage: 0,60; Abluftanlage: 0,40+0,15=0,55; bedarfsgeführt: 0,35+0,15=0,50)
- Spezifischer Lüftungswärmeverlust: HV = 0,34 × 0,60 × 508,44 = **103,72 W/K**
- Lüftungswärmeverlust: QV = **8.591 kWh/a**

Wärmegewinne:
- Solare Gewinne transparenter Bauteile (3 Fensterflächen à g = 0,55, FS = 0,9, FF = 0,7): Qs,t = **6.802 kWh/a**
- Solare Gewinne opaker Bauteile (αi = 0,5 für alle Flächen): Qs,op = **222 kWh/a**
- Interne Wärmegewinne: qi = 5 W/m² → Qi = 0,024 × 5 × 214,08 × tM = **9.377 kWh/a**

Wirksame Wärmespeicherfähigkeit:
- Schwere Bauweise (Volumenbezug): Cwirk,η' = 50 Wh/(m³·K) → Cwirk,η = 50 × 669 = 33.450 Wh/K  
  (leicht: 15 Wh/(m³·K); alternativ detailliert: 60 Wh/(m³·K))
- Bei Nachtabschaltung: schwer → 18 Wh/(m³·K) → Cwirk,NA = 12.042 Wh/K  
  (leicht: 12 Wh/(m³·K); detailliert: 20 Wh/(m³·K))

Jahres-Heizwärmebedarf:
- Gesamtwärmeverlust ohne Nachtabschaltung: Ql = **17.985 kWh/a**
- Mit 7 h Nachtabschaltung (nach DIN V 4108-6 Anh. C): Ql,NA = **17.472 kWh/a**
- Ql* (abzgl. solare Gewinne opak): **17.249 kWh/a**
- Summe transparente + interne Gewinne: Qg = **16.179 kWh/a**
- Numerischer Parameter: a = 1 + (Cwirk,η / (HT + HV)) / 16 h = **10,63**
- Jahres-Heizwärmebedarf: Qh = **7.726 kWh/a**
- Flächenbezogen: qh = Qh / AN = **36,09 kWh/(m²·a)**

Anlagentechnik und Primärenergie:
- Anlage 32 aus DIN V 4701-10 Bbl. 1: Brennwert-Kessel (verbessert), 55/45 °C, zentrales Verteilsystem innerhalb thermischer Hülle, innenliegende Stränge, geregelte Pumpe, hydraulischer Abgleich, GEG 2020 Dämmung
- Trinkwarmwasser: gemeinsam mit Heizung, Solaranlage, indirekt beheizter Speicher, ohne Zirkulation
- Lüftung: keine Anlage
- Primärenergie-Aufwandszahl: eP = 0,84
- Jahres-Primärenergiebedarf: QP = eP × (qh + 12,5) = 0,84 × (36,09 + 12,5) = **40,80 kWh/(m²·a)**
- CO₂-Äquivalent: 9,79 kg/(m²·a)

Nachweise:
- Referenz-Primärenergiebedarf: qP,Ref = **66,03 kWh/(m²·a)**
- Zulässiger Jahres-Primärenergiebedarf: qP,max = 0,75 × 66,03 = **49,53 kWh/(m²·a)**
- Vorhanden: 40,80 ≤ 49,53 → **erfüllt** → Energieeffizienzklasse **A**
- Spezifischer Transmissionswärmeverlust: HT′,vorh = HT / A = 113,42 / 454,50 = **0,250 W/(m²·K)**
- Zulässiger Wert (aus Referenz): HT′,max = **0,341 W/(m²·K)**
- 0,250 ≤ 0,341 → **erfüllt**

##### 8.3.3 Nichtwohngebäude Neubau

- Anforderungen analog Referenzgebäudeverfahren: Gebäude mit tatsächlicher Geometrie + Referenz-Wärmeschutz/-Anlagentechnik → Jahres-Primärenergiebedarf berechnen → max. zulässiger Wert = 75 % davon.
- Referenzausführung umfasst: Wärmeschutz der Gebäudehülle sowie Anlagentechnik für Heizung, Kühlung, Warmwasser, Raumlufttechnik und Beleuchtung.
- Berechnungsverfahren: DIN V 18599 (Grundzüge in Kap. 5).
- Aspekte Wärmebrücken, Luftdichtheit, Mindestluftwechsel, sommerlicher Wärmeschutz: prinzipiell wie bei Wohngebäuden im GEG 2020. Gilt auch für Änderungen und Nachrüstungen im Bestand.
- Beispiele für drei Gebäudetypen (aus GEG-Referenzanforderungen): Bürogebäude, Schule, Hotel (Ergebnisse folgen im nächsten Teil).
