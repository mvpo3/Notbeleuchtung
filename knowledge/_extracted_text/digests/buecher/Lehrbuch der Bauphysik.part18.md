# Lehrbuch der Bauphysik — Teil 18
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 721-760.

Dieser Teil behandelt zwei größere Themenblöcke: Kapitel 24 beschreibt den Schallimmissionsschutz im Außenbereich — Berechnungsmethodik nach DIN ISO 9613-2, Lärmschutzwände und das deutsche Regelwerk (TA Lärm, BImSchV-Verordnungen, DIN 18005). Kapitel 25/26 leiten den neuen Teil V "Licht" ein und legen die physikalischen Grundlagen der Lichttechnik: elektromagnetisches Spektrum, Strahlungsphysik, Sonnenspektrum und Airmass-Faktor.

## Inhalt

### Literaturliste Kapitel 23 (Raumlufttechnik-Akustik)

Am Beginn des Teils stehen Literaturangaben zum vorhergehenden Kapitel Raumlufttechnik:
- Piening, W. (1937): Schalldämpfung von Ansaug- und Auspuffgeräuschen von Dieselanlagen auf Schiffen. VDI-Zeitschrift 81, Nr. 26.
- DIN 15996:2020-12: Bild- und Tonbearbeitung in Film-, Video- und Rundfunkbetrieben — Grundsätze für den Arbeitsplatz.
- ISO 1996-1:2016-03: Akustik — Beschreibung, Messung und Beurteilung von Umgebungslärm, Teil 1: Grundlegende Größen und Beurteilungsverfahren.
- VDI 2081 Blatt 1:2019-03 und Blatt 2:2019-03: Raumlufttechnik — Geräuscherzeugung und Lärmminderung, mit Beispielband.
- IRT Akustische Information 1.11-1/1995: Höchstzulässige Schalldruckpegel für Dauergeräusche in Hörfunk- und Fernsehstudios.

---

### Kapitel 24 — Schallimmissionsschutz

#### 24.1 Berechnung der Schallausbreitung im Freien

Das Fachgebiet Schallimmissionsschutz befasst sich mit Entstehung, Ausbreitung und Empfang von Schall im Freien. Deutschland verfügt über ein differenziertes Regelwerk, das nach Lärmart (Gewerbe-, Verkehrs-, Freizeitlärm) unterschiedliche Bewertungsmaßstäbe vorsieht — für Betroffene oft schwer nachvollziehbar.

**Einflussgrößen auf den Schallpegel am Empfangspunkt:**
- Schallleistung der Quelle (beschrieben durch Schallleistungspegel L_W)
- Richtwirkung der Quelle (Richtwirkungskorrektur D_C)
- Pegelmindernde Einflüsse entlang des Ausbreitungswegs

**DIN ISO 9613-2:1996 — Geltungsbereich und behandelte Effekte:**

Die Norm erfasst folgende physikalische Effekte der Schallausbreitung:
- Geometrische Ausbreitung (A_div)
- Luftabsorption (A_atm)
- Bodeneffekt (A_gr)
- Reflexion an Flächen (Spiegelquellen)
- Abschirmung durch Hindernisse (A_bar)
- Bebauung, Bewuchs, Industriegelände (informativer Anhang A: A_misc)

Nicht anwendbar ist die Norm für Fluglärm sowie Druckwellen durch Sprengungen oder militärische Anwendungen.

**Grundgleichung der Schallausbreitung (DIN ISO 9613-2, Gl. 24.1):**

Der äquivalente Oktavband-Dauerschalldruckpegel bei Mitwind L_fT(DW) errechnet sich aus:

L_fT(DW) = L_W + D_C − A

wobei A die Gesamtdämpfung ist:

A = A_div + A_atm + A_gr + A_bar + A_misc

Der A-bewertete Langzeit-Mittelungspegel am Empfangspunkt berücksichtigt zusätzlich die meteorologische Korrektur C_met:

L_AT(LT) = L_AT(DW) − C_met

**Günstige Witterungsbedingungen** (Berechnungsgrundlage der Norm):
- Windgeschwindigkeit 1–5 m/s in 3–11 m Höhe über Grund
- Windrichtung innerhalb ±45° zur Verbindungslinie Quellmitte–Empfängermitte

Für energetische Addition mehrerer Quellen und Oktavbänder (j = 1…8, Mittenfrequenzen 63 Hz bis 8000 Hz) gilt die logarithmische Summation der Einzelbeiträge.

#### 24.1.1 Geometrische Dämpfung

A_div = 20 · lg(d/d₀) + 11 dB

Bezugsabstand d₀ = 1 m. Entspricht der bekannten Abstandsgesetz-Formel für eine ungerichtete Punktquelle.

#### 24.1.2 Luftabsorption

A_atm = α · d / 1000

α ist der Luft-Dämpfungskoeffizient in dB/km, stark abhängig von Frequenz, Temperatur und relativer Luftfeuchtigkeit. Einfluss des Luftdrucks auf α ist gering.

**Tabelle: Luft-Dämpfungskoeffizient α [dB/km] für ausgewählte Bedingungen (Tab. 24.1 DIN ISO 9613-2:1996):**

| Temp. [°C] | rel. Feuchte [%] | 63 Hz | 125 Hz | 250 Hz | 500 Hz | 1 kHz | 2 kHz | 4 kHz | 8 kHz |
|------------|-----------------|-------|--------|--------|--------|-------|-------|-------|-------|
| 10 | 70 | 0,1 | 0,4 | 1,0 | 1,9 | 3,7 | 9,7 | 32,8 | 117 |
| 20 | 70 | 0,1 | 0,3 | 1,1 | 2,8 | 5,0 | 9,0 | 22,9 | 76,6 |
| 30 | 70 | 0,1 | 0,3 | 1,0 | 3,1 | 7,4 | 12,7 | 23,1 | 59,3 |
| 15 | 20 | 0,3 | 0,6 | 1,2 | 2,7 | 8,2 | 28,2 | 88,8 | 202 |
| 15 | 50 | 0,1 | 0,5 | 1,2 | 2,2 | 4,2 | 10,8 | 36,2 | 129 |
| 15 | 80 | 0,1 | 0,3 | 1,1 | 2,4 | 4,1 | 8,3 | 23,7 | 81,8 |

Für andere Witterungsbedingungen: ISO 9613-1:1993. α ist repräsentativ für ortübliche Mittelbedingungen zu wählen.

#### 24.1.3 Bodeneffekt

Der Bodeneffekt (A_gr) erfasst die Überlagerung von direkt einfallendem und am Boden reflektiertem Schall. Die Norm setzt weitgehend ebenes oder gleichmäßig geneigtes Gelände voraus.

**Drei Zonen der Bodendämpfungsermittlung:**
1. Quellennaher Bereich (Ausdehnung: 30 · hs um die Quelle)
2. Empfängernaher Bereich (Ausdehnung: 30 · hr um den Empfänger)
3. Mittelbereich (nur vorhanden wenn projizierter Abstand dp > 30·hs + 30·hr)

Maßgebend sind: hs = Quellenhöhe, hr = Empfängerhöhe, dp = horizontaler Abstand (Projektion auf Bodenebene).

**Bodenfaktor G:**
- G = 0: harter Boden (Straßenpflaster, Wasser, Eis, Beton, Flächen mit geringer Porosität)
- G = 1: poröser Boden (Gras, bepflanzte Böden, Ackerland)
- 0 < G < 1: gemischter Boden, G entspricht dem Anteil porösen Bodens

**Berechnung Bodendämpfung (exemplarisch 500 Hz-Oktavband):**

Gesamtdämpfung: A_gr = A_s + A_r + A_m

Im Sender- und Empfängerbereich (500 Hz):
A_s bzw. A_r = −1,5 + G · c(h)

mit c(h) = 1,5 − e^(−0,46·h) · (1 − e^(−dp/50))·5,14 − 14·e^(−0,46·h)

(wobei h = hs oder h = hr je nach Bereich)

Mittelbereich (alle Oktavbänder gleich):
A_m = −3 · (1 − q_m · G)

mit q_m = 0 wenn dp < 30·hs + 30·hr (kein Mittelbereich)
bzw. q_m = 1 − (30·(hs + hr) / dp) wenn dp ≥ 30·(hs + hr)

**Vereinfachte Formel für A-bewertete Pegel bei überwiegend porösem Boden ohne Reine Töne (Gl. 24.13):**

A_gr = −4,8 − (2·h_m / d) · (17 + 300/d) [dB]

mit h_m = mittlere Höhe des Ausbreitungswegs über dem Boden [m], d = Abstand Quelle–Empfänger [m].

#### 24.1.4 Abschirmung durch Hindernisse

Lärmschutzwände, -wälle und andere Hindernisse bewirken Pegelminderung (Dämpfung durch Abschirmung A_bar). Ein Objekt muss folgende Voraussetzungen erfüllen, um als schallabschirmend berücksichtigt zu werden:
- Flächenbezogene Masse ≥ 10 kg/m²
- Geschlossene Oberfläche ohne wesentliche Risse oder Lücken
- Horizontale Abmessung (senkrecht zur Quelle-Empfänger-Linie) größer als Wellenlänge λ bei der betrachteten Oktavmittenfrequenz

**Abschirmmaß D_Z (Einfachbeugung, Gl. 24.14):**

D_Z = 10 · lg(3 + C₂/λ · z · K_met)

- C₂ = 20 (ohne spezielle Berücksichtigung von Bodenreflexionen)
- C₂ = 40 (mit Spiegelquellen für Bodenreflexionen)
- C₃ = 1 bei Einfachbeugung

**Bei Doppelbeugung (Gl. 24.15):**

C₃ = (1 + (5·λ/e)²) / (1/3 + (5·λ/e)²)

mit λ = Wellenlänge, e = horizontale Breite des Schirms.

**Schirmwert z** (Differenz des Weglängen gebeugt vs. direkt):
- Einfachbeugung: z = d_ss + d_sr − d_a (Gl. 24.16)
- Doppelbeugung: z = d_ss + d_sr + e − d_a (Gl. 24.17)

(d_ss = Abstand Quelle–Schirmoberkante, d_sr = Abstand Schirmoberkante–Empfänger, d_a = direkter Abstand)

**Meteorologischer Korrekturfaktor K_met:**
- Für z > 0: K_met = e^(−(d_ss · d_sr) / (2000·z)) (Gl. 24.18)
- Für z ≤ 0: K_met = 1

**Dämpfung A_bar:**
- Beugung über Oberkante: A_bar = max(D_Z − A_gr; 0) (Gl. 24.19)
- Beugung um senkrechte Kante: A_bar = D_Z (Gl. 24.20)

Hinweis: Bei Berechnung über Oberkante hebt sich die Bodendämpfung A_gr auf — der Bodeneffekt ist bereits im Schirmwert z enthalten. Wenn mehrere Ausbreitungswege (über Kante, um Kante) gleichzeitig vorhanden sind, sind die Beiträge energetisch zu addieren.

**Reflexionen:** Gut reflektierende Flächen (Fassaden, Dächer) werden als Spiegelquellen modelliert. Die Norm gibt in Tab. 4 Schätzwerte für den Schallreflexionsgrad ρ sowie eine Formel für die Schallleistung der Spiegelquelle an.

#### 24.1.5 Weitere Dämpfungseffekte (A_misc)

Diese im informativen Anhang A der DIN ISO 9613-2:1996 enthaltenen Einflüsse werden häufig überschätzt:

**Bewuchs (A_fol):**
- Wirkung nur bei Unterbrechung der Sichtlinie durch Bewuchs (ähnlich Schallschirm)
- Bei kurzen Distanzen bis 20 m: bis 1 dB/m bei 1000 Hz, bis 3 dB/m bei 8000 Hz
- Bei größeren Distanzen: lediglich 0,06 dB/m bei 1000 Hz bzw. 0,12 dB/m bei 8000 Hz
- Beispiel: Bei 100 m Ausbreitungslänge und 1000 Hz ist nur ca. 6 dB Dämpfung zu erwarten

**Industriegelände (A_site):**
- Streuung durch kleine Elemente wie Rohrleitungen, Ventile, Kästen
- Nur der durch Schallabschirmung (A_bar) noch nicht erfasste Anteil
- Oktavwerte maximal 0,2 dB/m; empfohlener Maximalwert: 10 dB
- Empfehlung: Ermittlung durch Messung aufgrund starker Geländeabhängigkeit

**Bebauung (A_hous):**
- Gilt wenn sowohl Quelle als auch Empfänger im bebauten Gebiet liegen
- Bei hoher Bebauungsdichte dominiert A_hous; bei geringer Dichte dominiert A_gr
- Maximalwert: 10 dB

Berechnung A_hous in zwei Anteilen:

A_hous = A_hous1 + A_hous2

A_hous1 = 0,1 · B · d_b (Gl. 24.22)
mit B = Bebauungsdichte (Verhältnis Gebäudegrundfläche zu Gesamtbaugrundfläche), d_b = Länge des Schallwegs durch das bebaute Gebiet

A_hous2 = 10 · lg(1 − p/100) (Gl. 24.23) mit p = Prozentanteil der Fassadenlänge an Straßen-/Eisenbahn-Gesamtlänge, p ≤ 90 %; gilt für korridorartige Situationen entlang Gebäudereihen; A_hous2 muss kleiner sein als das Einfügungsdämpfungsmaß eines angenommenen Schirms mit mittlerer Gebäudehöhe.

#### 24.1.6 Meteorologische Korrektur

Der meteorologische Korrekturfaktor C_met berücksichtigt Abweichungen von der idealisierten Rechenbedingung (maximal 5 m/s Wind, Mitwindausbreitung):

- C_met = 0 wenn dp ≤ 10·(hs + hr) (Gl. 24.24) — kurze Abstände: kein signifikanter Einfluss der Witterung
- C_met = C₀ · (1 − 10·(hs + hr)/dp) wenn dp > 10·(hs + hr) (Gl. 24.25)

C₀ ist ein ortsabhängiger Faktor in dB, abgeleitet aus lokaler Wetterstatistik (Wind, Temperaturgradient). Erfahrungswerte: C_met zwischen 0 dB und 5 dB; Werte über 2 dB treten selten auf.

#### 24.1.7 Genauigkeit und Gültigkeitsgrenzen

Geschätzte Abweichungen für A-bewertete breitbandige Geräuschquellen (Tab. 24.2 aus Tab. 5 DIN ISO 9613-2:1996):

| Mittlere Höhe h [m] | Abstand 0–100 m | Abstand 100–1000 m |
|---------------------|-----------------|---------------------|
| 0 bis 5 m | ±3 dB | ±3 dB |
| 5 bis 30 m | ±1 dB | ±3 dB |

Zusätzliche Unsicherheit durch Bestimmung des Schallleistungspegels der Quelle. Für Prognosen ist stets von der ungünstigsten Abweichung auszugehen.

---

### 24.2 Lärmschutzwände

Die akustische Wirksamkeit einer Lärmschutzwand wird durch Abschirmmaß D_Z bzw. Dämpfung A_bar beschrieben. Wirksamkeit hängt ab von:
- Wandhöhe
- Wandbreite
- Position von Quelle und Empfangsort relativ zur Wand
- Material der Wand

**Materialanforderung:** Flächengewicht mindestens 10 kg/m² (sichergestellt durch Luftschalldämmung). Materialvielfalt: transparentes Glas oder Kunststoff, Metall, Stein, Holz, begrünte Aufbauten.

**Schallabsorptionsklassen für Lärmschutzwände (ZTV LSW:2006):**

| Klasse | Bezeichnung | Schallabsorption |
|--------|-------------|-----------------|
| A0 | ohne Prüfzeugnis | — |
| A1 | reflektierend | bis 4 dB |
| A2 | absorbierend | 4 dB bis 7 dB |
| A3 | hochabsorbierend | 8 dB bis 11 dB |
| A4 | hochabsorbierend | über 11 dB |

Die Oberflächenbeschaffenheit (absorbierend vs. reflektierend) beeinflusst Reflexionen auf der der Wand gegenüberliegenden Seite, hat aber keinen Einfluss auf die schalldämmende Wirkung selbst.

---

### 24.3 Rechtliche Rahmenbedingungen des Immissionsschutzes

Lärm gilt rechtlich als schädliche Umwelteinwirkung. Das Bundes-Immissionsschutzgesetz BImSchG (§ 1) stellt den übergeordneten Rahmen. Geräusche werden darin als Emissionsart neben Erschütterungen, Licht, Wärme und Strahlen eingestuft.

**Konkretisierung:** Die TA Lärm (6. Allgemeine Verwaltungsvorschrift zum BImSchG) ist das zentrale Bewertungsinstrument für Gewerbelärm; sie wird in der Praxis weitgehend als Rechtsnorm angewendet, obwohl sie formal nur Verwaltungsvorschrift ist.

**Schnittstellen Schallschutz und Bauleitplanung:**
- DIN 4109:1989 — definiert Lärmpegelbereiche für bauliche Anforderungen an Außenbauteile
- DIN 18005-1:2002 — Schallschutz im Städtebau; enthält Orientierungswerte (Beiblatt 1)
- 16. BImSchV (Verkehrslärmschutzverordnung) — verbindliche Grenzwerte bei Neubau/Änderung von Straßen und Schienenwegen

---

### 24.4 Regelwerke zum Schallimmissionsschutz

#### 24.4.1 Gewerbelärm nach TA Lärm

**Geltungsbereich:** Alle dem BImSchG unterliegenden Anlagen (genehmigungsbedürftig und nicht genehmigungsbedürftig), soweit nicht explizit ausgenommen.

**Ausnahmen — Anlagen für die die TA Lärm nicht gilt:**
- Sportanlagen (18. BImSchV)
- Sonstige nicht genehmigungsbedürftige Freizeitanlagen und Freiluftgaststätten
- Nicht genehmigungsbedürftige landwirtschaftliche Anlagen
- Schießplätze für Waffen ab Kaliber 20 mm
- Tagebaue und Betriebsanlagen dazu
- Baustellen
- Seehafenumschlagsanlagen
- Anlagen für soziale Zwecke

**Maßgebliche Immissionsorte:**
- Bei bebauten Flächen: 0,5 m außerhalb der Mitte des geöffneten Fensters des am stärksten betroffenen schutzbedürftigen Raumes (nach DIN 4109:1989)
- Bei unbebauten Flächen: nächstgelegene schutzbedürftige Räume nach DIN 4109:1989

**Beurteilungspegel L_r (Ziffer A.1.4 TA Lärm, Gl. 24.26):**

L_r = 10 · lg (1/T_r · Σ_j T_j · 10^(0,1·(L_Aeq,j + C_met + K_T,j + K_I,j + K_R,j)))

Terme:
- T_r = Beurteilungszeit (tags: 16 h von 6:00–22:00 Uhr; nachts: lauteste Stunde zwischen 22:00–6:00 Uhr)
- N = Anzahl Teilzeiten
- L_Aeq,j = Mittelungspegel in Teilzeit T_j
- C_met = meteorologische Korrektur nach DIN ISO 9613-2:1996
- K_T,j = Zuschlag für Ton- und Informationshaltigkeit
- K_I,j = Zuschlag für Impulshaltigkeit
- K_R,j = Zuschlag für Tageszeiten mit erhöhter Empfindlichkeit (6 dB)

**Zuschläge:**
- K_T,j (Ton-/Informationshaltigkeit): 3 dB oder 6 dB (kein Zwischenwert); 6 dB wenn Musiktext inhaltlich am Immissionsort verstanden wird; messtechnische Erfassung nach DIN 45681:2005
- K_I,j (Impulshaltigkeit): anhand Erfahrungswerte bei Prognosen
- K_R,j = 6 dB in allgemeinen und reinen Wohngebieten sowie Kurgebieten zu bestimmten Tageszeiten (sowohl bei Messungen als auch Prognosen)

**Tieffrequente Geräusche:** Ermittlung und Bewertung nach DIN 45680:1997.

**Schießgeräusche:** Ermittlung nach VDI 3745 Blatt 1:1993 (Kaliber bis 20 mm), Bewertung nach TA Lärm-Richtwerten zuzüglich meteorologischer Korrektur und K_R.

**Prognosearten:**
- Detaillierte Prognose: Oktavbandweise 63 Hz bis 4000 Hz; alle Schallquellen und Schallausbreitungsrechnung nach DIN ISO 9613-2:1996
- Überschlägige Prognose: Nur A-bewertete Schallleistungspegel, vereinfachte Ausbreitung (A_div + A_atm); ausreichend bei sicherer Unterschreitung der Richtwerte und für Vorplanungen

Schallleistungspegel als Eingangsgröße nach DIN 45635-1:1984 oder DIN EN ISO 3740–3747 ermitteln. Abstrahlung von Industriegebäuden: VDI 2571. Körperschallübertragungen innerhalb von Gebäuden: keine Berechnungsansätze in der TA Lärm vorgegeben.

**Immissionsrichtwerte nach TA Lärm, außerhalb von Gebäuden (Tab. 24.3):**

| Gebietstyp | Tags [dB(A)] | Nachts, lauteste Std. [dB(A)] |
|------------|-------------|-------------------------------|
| Industriegebiete | 70 | 70 |
| Gewerbegebiete | 65 | 50 |
| Kerngebiete, Dorfgebiete, Mischgebiete | 60 | 45 |
| Allgemeine Wohngebiete, Kleinsiedlungsgebiete | 55 | 40 |
| Reine Wohngebiete | 50 | 35 |
| Kurgebiete, Krankenhäuser und Pflegeanstalten | 45 | 35 |

**Immissionsrichtwerte innerhalb von Gebäuden** (für im gleichen Gebäude liegenden schutzbedürftigen Raum, unabhängig vom Gebietstyp):
- Tags: 35 dB(A)
- Nachts: 25 dB(A)

**Kurzzeitige Geräuschspitzen:**
- Außerhalb von Gebäuden: tags max. +30 dB(A) und nachts max. +20 dB(A) über dem jeweiligen Richtwert
- Innerhalb von Gebäuden: tags und nachts jeweils max. +10 dB(A) über dem Richtwert

**Seltene Ereignisse:** Richtwerte außerhalb von Gebäuden unabhängig vom Gebietstyp: 70 dB(A) tags, 55 dB(A) nachts.

**Vor-, Zusatz- und Gesamtbelastung:**
- Zusatzbelastung: Anteil der zu beurteilenden Anlage am Gesamtpegel
- Vorbelastung: Immissionen bestehender Anlagen, für die die TA Lärm gilt
- Gesamtbelastung: Summe aus Vor- und Zusatzbelastung
- Öffentliche Straßen, Sportanlagen u. a. Quellen, für die die TA Lärm nicht gilt, bleiben außen vor (Fremdgeräusche)
- Verkehrsgeräusche im Zusammenhang mit dem zu beurteilenden Betrieb werden eingerechnet

#### 24.4.2 Schallschutz im Städtebau — DIN 18005

**Struktur:** DIN 18005-1:2002 (Hinweise zur städtebaulichen Planung), DIN 18005-2 (kartenmäßige Darstellung von Schallimmissionen), Beiblatt 1 (Orientierungswerte).

**Ziel:** Berücksichtigung schalltechnischer Belange in der Bauleitplanung. Für konkrete Bauvorhaben keine unmittelbare Verbindlichkeit, aber Anhaltspunkte.

Enthält keine eigenen Berechnungsverfahren; verweist auf andere Regelwerke; Schallausbreitung nach DIN ISO 9613-2:1996.

**Teilschallquellenverfahren:** Linien- und Flächenschallquellen sind in Teilquellen zu unterteilen, wenn der Abstand zum Empfangspunkt weniger als das Doppelte der maximalen Ausdehnung beträgt. Jede Teilquelle muss eine maximale Ausdehnung kleiner als die Hälfte des Abstands zum Empfangspunkt besitzen. Die Teilbeurteilungspegel werden energetisch summiert:

L_r,ges = 10 · lg(Σ 10^(0,1 · L_r,i))

**Verwendete Regelwerke für verschiedene Schallquellen (nach Tab. 24.4 DIN 18005-1:2002):**

| Schallquelle | Regelwerk |
|--------------|-----------|
| Straßen | RLS 90 |
| Öffentliche Parkplätze | RLS 90 |
| Andere Parkplätze | Parkplatzlärmstudie |
| Schienenverkehr | Schall 03 |
| Rangier-/Umschlagbahnhöfe | Akustik 04 |
| Luftverkehr | Fluglärmgesetz |
| Schiffsverkehr | Modifikation RLS 90 (Ziffer 7.4. DIN 18005-1:2002) |
| Gewerbliche Anlagen | TA Lärm + DIN ISO 9613-2:1996 |
| Sportanlagen | 18. BImSchV |
| Schießanlagen | TA Lärm bzw. VDI 3745 Blatt 1:1993 |
| Freizeitanlagen | Ländervorschriften (z. B. Niedersächsische Freizeitlärm-Richtlinie) |

**Orientierungswerte Beiblatt 1 DIN 18005 (Tab. 24.5), gelten am Rand der Bauflächen:**

| Gebietstyp | Tags [dB(A)] | Nachts Verkehr [dB(A)] | Nachts Gewerbe/Industrie/Freizeit [dB(A)] |
|------------|-------------|----------------------|------------------------------------------|
| Industriegebiete | — | — | — |
| Gewerbegebiete, Kerngebiete | 65 | 55 | 50 |
| Dorfgebiete, Mischgebiete | 60 | 50 | 45 |
| Besondere Wohngebiete | 60 | 45 | 40 |
| Friedhöfe, Kleingärten, Parks | 55 | — | — |
| Allgem. Wohngebiete, Kleinsiedlungsgebiete, Campingplätze | 55 | 45 | 40 |
| Reine Wohngebiete, Wochenendhausgebiete, Ferienhausgebiete | 50 | 40 | 35 |
| Sonstige Sondergebiete | 45–65 | 35–65 | — |

Beurteilungszeit: Tags 6:00–22:00 Uhr, nachts 22:00–6:00 Uhr. Wichtiger Hinweis: Bei Beurteilungspegeln über 45 dB(A) ist ungestörter Schlaf auch bei nur teilweise geöffnetem Fenster nicht mehr möglich.

#### 24.4.3 Weitere Regelwerke

**Verkehrslärmschutzverordnung — 16. BImSchV:**
Rechtlich bindende Immissionsgrenzwerte beim Neubau oder wesentlicher Änderung öffentlicher Straßen und Schienenwege. Im Gegensatz zu TA Lärm (Richtwerte) und DIN 18005 (Orientierungswerte) handelt es sich um echte Grenzwerte.

Berechnungszeiträume: Tags 6:00–22:00 Uhr, Nachts 22:00–6:00 Uhr; Ausbreitungsberechnung analog RLS 90.

**Immissionsgrenzwerte 16. BImSchV (Tab. 24.6), außerhalb von Gebäuden:**

| Gebietstyp | Tags [dB(A)] | Nachts, lauteste Std. [dB(A)] |
|------------|-------------|-------------------------------|
| Gewerbegebiete | 69 | 59 |
| Kerngebiete, Dorfgebiete, Mischgebiete | 64 | 54 |
| Reine und allgemeine Wohngebiete, Kleinsiedlungsgebiete | 59 | 49 |
| Krankenhäuser, Schulen, Kurheime, Altenheime | 57 | 47 |

Bei Grenzwertüberschreitung entstehen Ansprüche auf aktive und ggf. passive Lärmschutzmaßnahmen am Gebäude.

**Verkehrswege-Schallschutzmaßnahmenverordnung — 24. BImSchV:**
Regelt bauliche Schallschutzmaßnahmen, wenn die Grenzwerte der 16. BImSchV überschritten werden. Verfahren zur Berechnung des erforderlichen bewerteten Schalldämm-Maßes R'_w,res der gesamten Außenfläche. Besonderheiten:
- Korrektursummanden je nach Raumnutzung (Schlafraum weniger als Wohnraum, Konferenzraum, Großraumbüro)
- Weiterer Korrektursummand für Verkehrswegetyp
- Einbau von Lüftungseinrichtungen gilt als bauliche Verbesserung
- Verbindung zwischen Verkehrslärmimmissionen und erforderlichen bauakustischen Maßnahmen

**Sportanlagenlärmschutzverordnung — 18. BImSchV:**
Gilt für Neubau und Betrieb ortsfester Einrichtungen zur Sportausübung (Fußballstadien, Schwimmbäder, Turnhallen, Tennisplätze etc.). Abgrenzungsfragen bestehen bei Skateboardanlagen, Bowling-Bahnen, Erlebnisbädern. Einrichtungen in räumlicher und betrieblicher Verbindung (Vereinsheime, Spielplätze) werden miteinbezogen.

**Immissionsrichtwerte 18. BImSchV außerhalb von Gebäuden (Tab. 24.7):**

| Gebietstyp | Tags außerhalb Ruhezeit [dB(A)] | Tags innerhalb Ruhezeit [dB(A)] | Nachts [dB(A)] |
|------------|--------------------------------|--------------------------------|----------------|
| Gewerbegebiete | 65 | 60 | 50 |
| Kerngebiete, Dorf-, Mischgebiete | 60 | 55 | 45 |
| Allgemeine Wohngebiete, Kleinsiedlungsgebiete | 55 | 50 | 40 |
| Reine Wohngebiete | 50 | 45 | 35 |
| Kurgebiete, Krankenhäuser, Pflegeanstalten | 45 | 45 | 35 |
| Industriegebiete | keine Werte | — | — |

Für Aufenthaltsräume in baulich (nicht betrieblich) verbundenen Wohngebäuden: tags 35 dB(A), nachts 25 dB(A).

Kurzzeitige Geräuschspitzen: außerhalb Gebäude tags +30 dB(A), nachts +20 dB(A); innerhalb Gebäude tags und nachts +10 dB(A) über Richtwerten.

**Bezugszeiträume der 18. BImSchV (Tab. 24.8):**

| | Werktags | Sonn- und Feiertage |
|---|----------|---------------------|
| Tags | 6:00–22:00 Uhr | 7:00–22:00 Uhr |
| Nachts | 0:00–6:00 Uhr und 22:00–24:00 Uhr | 0:00–7:00 Uhr und 22:00–24:00 Uhr |
| Ruhezeit | 6:00–8:00 Uhr und 20:00–22:00 Uhr | 7:00–9:00 Uhr, 13:00–15:00 Uhr, 20:00–22:00 Uhr |

Hinweis zur Ruhezeit 13:00–15:00 Uhr an Sonn- und Feiertagen: Nur relevant wenn Gesamtnutzungsdauer der Sportanlage zwischen 9:00–20:00 Uhr an dem Tag mehr als 4 Stunden beträgt. Ruhezeiten wirken als Absenkung des Richtwerts um 5 dB(A) (anders als TA Lärm, die einen Zuschlag von 6 dB(A) für Ruhezeiten ansetzt).

**RLS 90 (Richtlinien für Lärmschutz an Straßen):**
Berechnungsverfahren für Schallabstrahlung von Straßen auf Basis von Verkehrszahlen, zulässiger Geschwindigkeit, Fahrbahnbeschaffenheit und Steigung. Ergänzungen für offenporige Deckschichten (Flüsterasphalt). Enthält auch Emissionsansätze für Parkplätze sowie Vorgaben zur Berücksichtigung von Lärmschutzwänden/-wällen. Wird von TA Lärm und DIN 18005-1:2002 referenziert.

**Parkplatzlärmstudie (Bayerisches Landesamt für Umwelt, 6. Aufl. 2007):**
Verfahren zur Berechnung von Schallemissionen aus Parkplätzen und Parkhäusern. Empirisch abgeleitete Emissionsansätze, differenziert nach Parkplatztyp (Wohnanlage, P+R, Gaststätte). Enthält auch kurzzeitige Ereignisse (Türenzuschlagen, Kofferraumschlagen, Überfahren von Regenrinnen). Abweichung von der Studie nur im begründeten Einzelfall nach DIN 18005-1:2002.

**Schall 03 und Akustik 04:**
- Schall 03: Richtlinie für Schallimmissionsberechnungen von Schienenwegen (Zugarten, Bremsbauarten, Zuglängen, Geschwindigkeiten)
- Akustik 04: Richtlinie für Rangier- und Umschlagbahnhöfe, mit Schallquellenkatalog für Gleisbremsen, Kurvenquietschen, Hemmschuhaufläufe

**Schießlärm — VDI 3745 Blatt 1:1993:**
Verfahren für Messung und Bewertung von Schießanlagenimmissionen. Besondere Zeitcharakteristik (kurze, hochenergetische Knalle) erfordert angepasste Mess- und Bewertungsmethodik. Jede Variation der Emissionssituation (Waffenart, Kaliber, Munition, Schussrichtung) ist als eigene Emissionssituation zu erfassen.

**Freizeitlärm-Richtlinien:**
Ländersache — bundesweit nicht einheitlich. Typische Regelungsgegenstände: Volksfeste, Traditionsveranstaltungen, Rockveranstaltungen, Abenteuerspielplätze, Hundedressurplätze, Freizeit- und Vergnügungsparks, Sommerrodelbahnen, Zirkusse.
- Niedersächsische Freizeitlärm-Richtlinie: lehnt sich an TA Lärm an, mit zwei Abweichungen (Ruhezeitenzuschläge, 18 statt 10 seltene Ereignisse)
- Nordrhein-Westfalen: umfassendere Regelung mit weiteren Abweichungen

**Weitere Emissionsquellen-Studien (Tab. 24.9):**

| Dokument | Anwendungsbereich |
|----------|-------------------|
| Sächsische Freizeitlärmstudie | Rummelplätze, Volksfeste, Freiluftkonzerte, Freilichtbühnen, Zirkusse, Modellflugzeuge, Hundedressurplätze, Märkte, Freizeit-/Vergnügungsparks, Abenteuerspielplätze, Wasserskianlagen, Vereins-/Bürgerhäuser, Sommerrodelbahnen |
| Sportanlagen und Sportgeräte | Menschen-/Publikumsgeräusche, Fußball, Hockey, American Football, Tennis, Eishockey, Publikumseislauf, Eisstockschießen, Sommerstockbahnen, Freibäder/Spaß-Anlagen, Leichtathletik, Bolzplätze, Parkplätze |
| Hessen Heft 1 | Anlagen zur Abfallbehandlung/-verwertung und Kläranlagen |
| Hessen Heft 2 | Bagger, Kleinlader, Raupen, Walzen, Rüttler, Stampfer, Fugenschneider, Motorrollbesen u. a. Geräte in verschiedenen Betriebszuständen |
| Hessen Heft 3 | LKW-Betriebsgeräusche, Fahrgeräusche, Einkaufswagen, Handhubwagen auf verschiedenen Oberflächen |
| Hessen Heft 247 | Baumaschinen: Bagger, Lader, Raupen, Presslufthämmer, Bohrgeräte, Sägen |
| Hessen Heft 275 | Tankstellen-Aktivitäten: PKW-Türen, Kofferraum, Tankdeckel |
| Leitfaden LKW-Be/Entladung | Muldenkipper, Containerabsetzen, Silofahrzeuge, Gabelstapler und weitere Geräusche |

#### 24.4.4 Maßgeblicher Außenlärmpegel nach DIN 4109

DIN 4109:1989 unterscheidet für die Dimensionierung von Außenbauteilen nach Lärmart:
- Straßenverkehr
- Schienenverkehr
- Wasserverkehr
- Luftverkehr
- Gewerbe- und Industrieanlagen

Straßen-, Schienen- und Wasserverkehrslärm werden nach DIN 18005-1:2002 bestimmt. Dem errechneten Beurteilungspegel für Straßen- und Schienenverkehr ist ein Korrekturwert von +3 dB(A) hinzuzuaddieren. Luftverkehrslärm richtet sich nach dem Gesetz zum Schutz gegen Fluglärm. Gewerbelärm nach TA Lärm. Bei Überlagerung verschiedener Quellen werden die Beiträge addiert. Ermittlung grundsätzlich rechnerisch; Messungen nur im Ausnahmefall.

---

### Kapitel 25 — Einführung in Teil V: Licht

Der neue Teil V des Lehrbuchs behandelt Beleuchtung als physiologische Notwendigkeit. Tageslicht ist tagsüber die primäre Lichtquelle; Kunstlicht ergänzt bei Nacht und bei unzureichendem Tageslicht.

**Grundsätzliche Zusammenhänge:**
- Tageslichtplanung und Kunstlichtplanung sind voneinander abhängig (Gestaltung der Raumoberflächen beeinflusst Lichtverteilung; Fensteranordnung und Leuchtenanordnung greifen ineinander)
- Tageslichtplanung hat Vorrang und beeinflusst Gebäudeausrichtung, Größe und Anordnung der Öffnungen sowie die Nutzung und den Schutz vor Sonnenenergie
- Energetische und klimatische Aspekte sind bereits bei einfachsten Öffnungen relevant (Wärmeverluste im Winter, Rauchableitung bei Feuerstellen)

**Kriterien guter Raumbeleuchtung** (gelten gleichwertig für Tages- und Kunstlicht):
- Ausreichende Beleuchtungsstärken
- Geeignete Lichtführung und -verteilung im Raum
- Blendfreiheit
- Reichhaltiges Frequenzspektrum des Lichts

Ökonomische Randbedingungen sind als Anreiz für effiziente Lösungen zu verstehen (z. B. starre Blenden nach Süden als kostengünstigerer Sonnenschutz gegenüber beweglichen Anlagen; Indirektbeleuchtung statt teurer blendungsfreier Leuchten).

---

### Kapitel 26 — Grundlagen der Lichttechnik

#### 26.1 Elektromagnetische Strahlung

Licht ist elektromagnetische Strahlung, gewichtet mit der spektralen Helligkeitsempfindlichkeit des menschlichen Auges. Die Empfindlichkeitskurve geht beidseitig asymptotisch gegen null: von 380 nm (kurzwellige Grenze) bis 780 nm (langwellige Grenze), mit Maximum im Grünbereich.

Für Beleuchtungsfragen relevant sind zusätzlich:
- UV-Bereich: 100–380 nm
- IR-Bereich: 780–3000 nm

**Elektromagnetisches Spektrum mit Wellenlängenbereichen (Tab. 26.1):**

| Bezeichnung | Wellenlänge |
|-------------|-------------|
| Gammastrahlen | < 0,005 nm |
| Röntgenstrahlen | 0,005–10 nm |
| Extremes UV | 10–100 nm |
| UV-C | 100–280 nm |
| UV-B | 280–315 nm |
| UV-A | 315–380 nm |
| Sichtbares Licht (VIS) | 380–780 nm |
| Nahes Infrarot IR-A | 780–1400 nm |
| IR-B | 1400–3000 nm |
| Mittleres u. Fernes Infrarot IR-C | 3000 nm–1 mm |
| Mikrowellen | 1 mm–1 m |
| Radiowellen | 1 m–10 km |
| Niederfrequenz | 10 km–100.000 km |

**Photonen und Energie:**
Licht kann im Korpuskelmodell als Photonenstrom beschrieben werden. Photonenenergie: E_Photon = h · ν (h = Plancksche Konstante). Kurzwellige Photonen sind energiereicher (UV) als langwellige (IR), dennoch kann die Strahlungsintensität im IR-Bereich wegen der höheren Photonendichte hoch sein. Beispiel Sonne: UV-Anteil wenige, aber energiereiche Photonen mit geringer Intensität; IR-Anteil viele, aber energiearme Photonen mit hoher Intensität.

UV-Strahlung wird in der Literatur teils als "UV-Licht" bezeichnet, obwohl nicht sichtbar. Körperreaktionen: UV → Hautrötung/Bräunung, Zellschäden; IR → Wärmeempfindung.

**Strahlungsphysikalische Grundgrößen:**
- Strahlungsleistung / Energiefluss Φ_e: P [W] = Energie [J] / Zeit [s] (Gl. 26.1)
- Strahlungsenergie Q_e: Q_e [J bzw. W·s] = Φ_e [W] · Zeit [s] (Gl. 26.2)
- Strahlungsintensität / Strahlungsflussdichte: [W/m²] = Strahlungsfluss / Fläche A [m²] (Gl. 26.4)

Hinweis: Bestrahlungsstärke und flächenspezifische Abstrahlung haben dieselbe Einheit W/m²; ihr Zusammenhang ist Basis der lichttechnischen Größen.

#### 26.2 Sonnenspektrum — Temperaturstrahler

Die Sonne verhält sich wie ein idealer Temperaturstrahler (Schwarzer Strahler / Planckscher Strahler). Das extraterrestrische Sonnenspektrum stimmt weitgehend mit dem theoretischen Planckschen Strahlungsverlauf überein; Abweichungen entstehen durch besondere Emissionsprozesse der Sonne. Das terrestrische Spektrum weicht stärker ab durch Absorptions- und Streuprozesse in der Atmosphäre.

**Aufteilung der terrestrischen Sonnenstrahlung:**
- UV: 5 %
- Sichtbares Licht: 45 %
- Infrarot: 50 %

#### 26.2.1 Solarkonstante und Airmass-Faktor

**Solarkonstante I₀:** Bestrahlungsstärke außerhalb der Atmosphäre, I₀ ≈ 1350 W/m².

**Airmass-Faktor AM:** Maß für die zu durchdringende Atmosphärenschicht in Abhängigkeit vom Sonnenstand. Definiert als Verhältnis der bei gegebenem Zenitwinkel durchdrungenen Schichtdicke L zur minimalen Schichtdicke L₀ (Sonne im Zenit):

AM = L / L₀

Näherungsformel für Zenitwinkel z < 75° auf Normalnull und in gemäßigten Höhen:

AM = 1 / cos(z)   (Gl. 26.6)

Mit zunehmendem Zenitwinkel (Sonne tiefer am Horizont) steigt AM. Für z > 75° sind Modelle mit Erdkrümmungskorrektur erforderlich.

**Klassifizierung der Airmass-Faktoren mit horizontalen Bestrahlungsstärken (Tab. 26.2):**

| Zenitwinkel | AM-Klasse | Klassifizierung | Bestrahlungsstärke horizontal [W/m²] |
|-------------|-----------|-----------------|--------------------------------------|
| — | AM0 | Außerhalb der Atmosphäre | 1350 |
| 0°–23° | AM1–AM1,1 | Sonnenstand im Zenit, Tropenregionen | 1042–1021 |
| 48° | AM1,5 | Gemäßigte Breiten | 931 |
| 60°–70° | AM2–AM3 | Hohe Breitengrade (z. B. Nordeuropa) | 842–713 |

Zenitwinkel ist der Winkel zwischen Sonnenstand und Zenit (senkrechter Punkt über Beobachter). Der Zenit ist nicht identisch mit dem Kulminationspunkt (Sonnenhöchststand für einen gegebenen Ort); die Sonne kann nur zwischen nördlichem und südlichem Wendekreis tatsächlich im Zenit stehen.
