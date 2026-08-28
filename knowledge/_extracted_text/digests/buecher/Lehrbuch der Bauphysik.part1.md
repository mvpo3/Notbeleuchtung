# Lehrbuch der Bauphysik — Teil 1
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 41-80.

Dieses Standardwerk behandelt die physikalischen Grundlagen des baulichen Wärme- und Feuchteschutzes. Teil 1 deckt die Fortsetzung von Kapitel 2 (Wärmetransport: Konvektion, Strahlung, wärmetechnische Kenngrößen) sowie Kapitel 3 (Wärmebrücken: Definitionen, raumseitige Temperaturen, Wärmeverluste, Praxisbeispiele) ab.

## Inhalt

### Dimensionslose Kennzahlen für konvektiven Wärmeübergang

Zur Beschreibung von Wärmetransportvorgängen werden dimensionslose Kennzahlen eingesetzt, die es ermöglichen, Erkenntnisse aus Experimenten (z. B. Windkanalversuche an Modellen) auf allgemeine Bedingungen zu übertragen.

Relevante Kennzahlen:
- **Nusselt-Zahl (Nu):** Verhältnis des konvektiven Wärmeübergangs eines strömenden Mediums zur Wärmeleitung des ruhenden Mediums. Bei ruhender, eindimensionaler Leitung gilt Nu = 1.
- **Grashof-Zahl (Gr):** Verhältnis der Auftriebskraft zu der bremsenden Zähigkeitskraft in einem Fluid; wird für freie Konvektion herangezogen.
- **Prandtl-Zahl (Pr):** Verhältnis von kinematischer Viskosität zur Temperaturleitfähigkeit; ist eine reine Stoffgröße.
- **Rayleigh-Zahl (Ra):** Produkt aus Grashof- und Prandtl-Zahl (Ra = Gr · Pr); dient als komprimierte Schreibweise.
- **Reynolds-Zahl (Re):** Kennzeichnet Strömungsverhältnisse bei erzwungener Konvektion (z. B. Wind oder Ventilatoren); Verhältnis von Trägheits- zu Reibungskräften.

Formeln (Symboldefinitionen):
- l [m] = charakteristische Länge
- w [m/s] = Strömungsgeschwindigkeit
- λ [W/(m·K)] = Wärmeleitfähigkeit
- v [m²/s] = kinematische Viskosität
- η [kg/(m·s)] = dynamische Viskosität
- a [m²/s] = Temperaturleitfähigkeit (a = λ/(cp · ρ))
- cp [J/(kg·K)] = spezifische Wärmekapazität
- Δθ [K] = Temperaturdifferenz
- g [m/s²] = Erdbeschleunigung
- β [1/K] = thermischer Ausdehnungskoeffizient
- θs [K] = Wandoberflächentemperatur
- θu [K] = Lufttemperatur der unbeeinflussten Umgebung

Der konvektive Wärmeübergangskoeffizient ergibt sich zu: hK = Nu · λ / l (Gl. 2.18). Dabei ist λ für die jeweils gültige Bezugstemperatur zu bestimmen.

**Stoffwerte für Luft bei p = 1 bar (Tab. 2.2):**

| θ [°C] | λ [W/(m·K)] | v [10⁻⁶ m²/s] | η [10⁻⁵ kg/(m·s)] | Pr [-] |
|--------|-------------|---------------|-------------------|--------|
| -20    | 0,0226      | 11,78         | 1,620             | 0,72   |
| 0      | 0,0242      | 13,52         | 1,722             | 0,72   |
| 20     | 0,0257      | 15,35         | 1,821             | 0,71   |
| 40     | 0,0272      | 17,26         | 1,917             | 0,71   |
| 60     | 0,0286      | 19,27         | 2,010             | 0,71   |
| 80     | 0,0300      | 21,35         | 2,101             | 0,71   |

### Erzwungene Luftströmung an Bauteilen (Abschn. 2.2.2.1)

Für erzwungene Außenströmung (längsangeströmte Platte) wird die Nusselt-Zahl nach einer kombinierten Formel berechnet (Gl. 2.20). Der Gültigkeitsbereich ist: 10 < Re < 10⁷; 0,6 < Pr < 2000. Die charakteristische Länge ist die Überströmlänge.

Für Reynolds-Zahl gilt Re = w · lü / v (Gl. 2.21), wobei Stoffwerte für die Außenlufttemperatur θu anzusetzen sind.

**Vereinfachte Abschätzungen:**
- Nach Jürges (Re > 5·10⁵, θf ≈ 0 °C): hK = 6,4 · w^0,8 · l^0,2
- Nach Glück (w = 1 m/s, θü = 20 °C, lü = 1 m): hK = 6,9 (bei angegebenen Bedingungen)

**Berechnungsbeispiel erzwungene Konvektion (Außenwand):**
- Wandlänge: 10 m, Windgeschwindigkeit: 4 m/s, Außenlufttemperatur: 0 °C
- Stoffwerte bei 0 °C: λ = 0,0242 W/(m·K), v = 13,52·10⁻⁶ m²/s, Pr = 0,72
- Re = 4 × 10 / (13,52·10⁻⁶) = 2.958.580
- Nu ≈ 4604,8
- hK = 4604,8 × 0,0242 / 10 = 11,1 W/(m²·K)
- Vereinfacht nach Jürges: hK = 12,2 W/(m²·K)

### Freie Strömung an Wänden und Decken (Abschn. 2.2.2.2)

Bei freier Konvektion (Auftriebsströmung) wird hK über die Rayleigh-Zahl und die Prandtl-Zahl bestimmt.

**Senkrechte Wände:** Charakteristische Länge = Wandhöhe H. Nusselt-Zahl nach Gl. 2.25. Die Rayleigh-Zahl für Luft als ideales Gas:

Ra = g · H³ · Δθ / [(θu + 273) · v²] · Pr (Gl. 2.26)

Variablen:
- θu [°C] = Temperatur der ungestörten Umgebungsluft
- θs [°C] = Wandtemperatur
- θG [°C] = mittlere Grenzschichttemperatur (θu + θs)/2
- Δθ [K] = |θs – θu|
- H [m] = Wandhöhe
- L, B [m] = Länge, Breite (für Decken)

**Waagerechte Bauteile (Decken):** Charakteristische Länge l = (2 · L · B) / (L + B) (Fläche geteilt durch halben Perimeter).

Für Wärmestrom nach oben (turbulent, ohne äußeren Einfluss): Nu = 0,155 · Ra^0,333 (Gl. 2.28)
Für Wärmestrom nach unten (laminar, ohne äußeren Einfluss): Nu = 0,485 · Ra^0,2 (Gl. 2.29)

**Vereinfachte Formeln für hK als Funktion der Temperaturdifferenz Δθ:**
- Vertikale Fläche: hK = 1,6 · Δθ^0,3 (Gl. 2.31)
- Horizontale Fläche, Wärmestrom aufwärts: hK = 2 · Δθ^0,31 (Gl. 2.32)
- Horizontale Fläche, Wärmestrom abwärts (Luftschichtung): hK = 0,54 · Δθ^0,31 (Gl. 2.33)

**Berechnungsbeispiel freie Konvektion (Innenwand):**
- Wandhöhe H = 2,7 m, Wandtemperatur θs = 17 °C, Raumluft θu = 20 °C
- Mittlere Grenzschichttemperatur θG = 18,5 °C
- Stoffwerte: λ = 0,0256 W/(m·K), v = 15,2·10⁻⁶ m²/s, Pr = 0,71
- Ra ≈ 6,048·10⁹
- Nu ≈ 218,44
- hK = 218,44 × 0,0256 / 2,7 = 2,1 W/(m²·K)
- Näherungsformel: hK = 1,6 × 3^0,3 = 2,2 W/(m²·K)

### Strahlung (Abschn. 2.2.3)

Wärmetransport durch Strahlung erfolgt über elektromagnetische Wellen und ist — anders als Leitung und Konvektion — nicht an ein Trägermedium gebunden; er findet auch im Vakuum statt.

**Unterscheidung nach Wellenlänge:**
- Kurzwellige Strahlung (Solarstrahlung): 7 % UV (< 380 nm), 47 % sichtbar (380–780 nm), 46 % langwellig-solar (780–3000 nm)
- Langwellige Strahlung (Wärmestrahlung): 3 µm (= 3000 nm) bis 800 µm

Auf einen Körper treffende Strahlung verteilt sich auf Reflexion (ρ), Absorption (α) und Transmission (τ): ρ + α + τ = 1. Bei opaken Bauteilen gilt τ = 0, daher ρ + α = 1.

### Schwarzer Strahler (Abschn. 2.2.3.1)

Der schwarze Körper ist ein theoretisches Vergleichsmodell, das bei gegebener Temperatur die maximal mögliche Strahlungsintensität abgibt. Die spektrale Strahlungsintensität Iλ folgt dem Planck'schen Strahlungsgesetz (Gl. 2.35):
- C1 = 3,7418·10⁻¹⁶ W·m² (1. Strahlungskonstante)
- C2 = 1,438·10⁻² K·m (2. Strahlungskonstante)

Mit zunehmendem Temperaturniveau verschiebt sich das Intensitätsmaximum zu kürzeren Wellenlängen (Wien'sches Verschiebungsgesetz). Die äquivalente Sonnentemperatur beträgt ca. 5800 K mit Intensitätsmaximum bei λ ≈ 0,5 µm.

Integration über alle Wellenlängen ergibt die Strahlungs-Wärmestromdichte des schwarzen Körpers:
- qS = σ · T⁴ (Gl. 2.36)
- σ = 5,67·10⁻⁸ W/(m²·K⁴) (Stefan-Boltzmann-Konstante)
- Alternativ: qS = CS · (T/100)⁴ mit CS = 5,67 W/(m²·K⁴)

### Realer Strahler (Abschn. 2.2.3.2)

Reale Oberflächen strahlen weniger als der schwarze Körper. Das Verhältnis wird durch den Emissionsgrad ε ausgedrückt (schwarzer Körper: ε = 1, realer Körper: ε < 1). Gemäß dem Kirchhoff'schen Gesetz gilt ε = α (Emissionsgrad = Absorptionsgrad).

Bei kurzwelliger Strahlung treten geringere Absorptionsgrade auf als bei langwelliger Strahlung — das Kirchhoff'sche Gesetz gilt daher nur eingeschränkt, wenn beide Strahlungsarten gemeinsam betrachtet werden.

Wärmestromdichte einer realen Oberfläche: q = ε · CS · (T/100)⁴ (Gl. 2.39)

**Emissions- und Absorptionsgrade verschiedener Materialien (Tab. 2.3):**

| Material | Emissionsgrad ε (Wärmestrahlung θ ≈ 20 °C) | Absorptionsgrad α (Sonnenstrahlung) |
|----------|----------------------------------------------|--------------------------------------|
| Sichtbackstein rot | 0,93 | 0,54 |
| Dachziegel dunkelbraun | 0,94 | 0,76 |
| Kalksandstein | 0,96 | 0,60 |
| Beton glatt | 0,96 | 0,55 |
| Kunststoff-Verputz weiß | 0,97 | 0,36 |
| Mineralischer Verputz grau | 0,97 | 0,65 |
| Aluminium, anodisiert/eloxiert | 0,90 | 0,20–0,40 |
| Poliertes Aluminium | 0,02–0,04 | 0,10–0,40 |
| Fensterglas | 0,90 | 0,04–0,40 (je nach Durchlässigkeit) |

### Wärmeaustausch zwischen Flächen (Abschn. 2.2.3.3)

Der Strahlungswärmestrom q12 zwischen zwei Flächen (A1 mit T1, ε1 und A2 mit T2, ε2) hängt von Temperaturen, Emissionsgraden und der geometrischen Anordnung ab.

Die geometrische Größe wird als **Einstrahlzahl φ12** (auch Sichtfaktor oder Formfaktor) bezeichnet. Rechenregeln:
- **Reziprozitätsbeziehung:** A1 · φ12 = A2 · φ21 (Gl. 2.44)
- **Summationsbeziehung:** Im geschlossenen Raum ist die Summe aller Einstrahlzahlen gleich 1 (Gl. 2.45)
- **Zerlegungsgesetz:** Eine Fläche A1 kann in Teilflächen zerlegt werden; die Einstrahlzahlen addieren sich entsprechend der Flächenanteile (Gl. 2.46, 2.47)

Für beliebige Flächen mit ε1 und ε2 > 0,8: C12 = ε1 · ε2 · CS (Gl. 2.42)

Allgemeiner Strahlungswärmestrom: q12 = φ12 · C12 · [(T1/100)⁴ – (T2/100)⁴] (Gl. 2.43)

Für zwei planparallele Flächen mit großer Ausdehnung gegenüber dem Abstand (mit Reflexionskorrektur):
q12 = CS / (1/ε1 + 1/ε2 – 1) · [(T1/100)⁴ – (T2/100)⁴] (Gl. 2.48)

### Strahlungsbedingter Wärmeübergangskoeffizient (Abschn. 2.2.3.4)

Zur vereinfachten Berechnung werden Materialoberflächeneigenschaften und geometrische Verhältnisse in einem strahlungsbedingten Wärmeübergangskoeffizienten hS zusammengefasst, sodass die Strahlungswärmestromdichte analog zur Konvektion formuliert werden kann: q12 = qS = hS · (θS1 – θS2) (Gl. 2.50).

### Wärmetechnische Kenngrößen für Bauteile (Abschn. 2.3)

Für die bauliche Praxis werden die Transportmechanismen in handhabbare Kenngrößen für den winterlichen Wärmeschutz zusammengefasst:
- Wärmeübergangswiderstand (surface resistance)
- Wärmedurchlasswiderstand
- Wärmedurchgangswiderstand
- Wärmedurchgangskoeffizient (U-Wert)

### Wärmeübergangswiderstand (Abschn. 2.3.1)

Konvektion und Strahlung werden im Gesamt-Wärmeübergangskoeffizienten hges = hK + hS zusammengefasst (Gl. 2.51).

Der Wärmeübergangswiderstand Rs ist der Kehrwert: Rs = 1/hges (Gl. 2.52).

Unterscheidung: Rsi (innen, surface inside) und Rse (außen, surface exterior).

**Bemessungswerte der Wärmeübergangswiderstände nach DIN EN ISO 6946 (Tab. 2.4):**

| Richtung des Wärmestroms | Rsi [(m²·K)/W] | Rse [(m²·K)/W] |
|--------------------------|----------------|----------------|
| Aufwärts (> 30° zur Horizontalen) | 0,10 | 0,04 |
| Horizontal (≤ 30° zur Horizontalen) | 0,13 | 0,04 |
| Abwärts | 0,17 | 0,04 |

Hinweis: Die Werte gelten für ebene Oberflächen. Beim Steildach ist die Dachneigung zu beachten (Abb. 2.16).

### Wärmedurchlasswiderstand (Abschn. 2.3.2)

#### Homogene Bauteilschichten

Für eine homogene Schicht gilt: R = d / λ (Gl. 2.53) mit d [m] = Schichtdicke und λ [W/(m·K)] = Wärmeleitfähigkeit.

Für mehrschichtige Bauteile: R = Σ (di / λi) (Gl. 2.54)

#### Luftschichten

Luftschichten werden nach Belüftungsgrad unterschieden: ruhend, schwach belüftet, stark belüftet. Für die letzten beiden Fälle wird auf DIN EN ISO 6946 verwiesen.

Eine ruhende Luftschicht liegt vor, wenn der Luftraum vollständig von der Umgebung abgeschlossen ist.

**Wärmedurchlasswiderstand ruhender Luftschichten (Tab. 2.5) — Oberflächen mit hohem Emissionsgrad:**

| Dicke [mm] | Aufwärts [m²K/W] | Horizontal [m²K/W] | Abwärts [m²K/W] |
|------------|-------------------|---------------------|------------------|
| 0  | 0,00 | 0,00 | 0,00 |
| 5  | 0,11 | 0,11 | 0,11 |
| 7  | 0,13 | 0,13 | 0,13 |
| 10 | 0,15 | 0,15 | 0,15 |
| 15 | 0,16 | 0,17 | 0,17 |
| 25 | 0,16 | 0,18 | 0,19 |
| 50 | 0,16 | 0,18 | 0,21 |
| 100 | 0,16 | 0,18 | 0,22 |
| 300 | 0,16 | 0,18 | 0,23 |

### Wärmedurchgangswiderstand (Abschn. 2.3.3)

Der Wärmedurchgangswiderstand RT ist die Summe aller Widerstände:
RT = Rsi + R1 + R2 + ... + Rn + Rse (Gl. 2.55)

### Wärmedurchgangskoeffizient — U-Wert (Abschn. 2.3.4)

#### Homogene Schichten

Ein Bauteil gilt als homogen, wenn in jeder Ebene quer zur Wärmestromrichtung einheitliches Material vorliegt (z. B. Flachdach mit Betondecke + Dämmschicht + Abdichtung, oder Mauerwerk mit vollflächig aufgeklebter Dämmung + Putz).

U = 1 / (Rsi + R1 + R2 + ... + Rn + Rse) (Gl. 2.56) bzw. U = 1 / RT (Gl. 2.57)

#### Inhomogene Schichten (Abschn. 2.3.4.2)

Bei inhomogenen Schichten (z. B. Sparren mit Zwischendämmung, eingebettete Stahlteile) wird der U-Wert über die Mittelwertbildung aus **oberem Grenzwert RT'** und **unterem Grenzwert RT''** bestimmt:

RT = (RT' + RT'') / 2 (Gl. 2.58)

**Oberer Grenzwert RT':** Berechnung des Wärmedurchgangswiderstands für jeden Abschnitt in Wärmestromrichtung (z. B. Abschnitt a: Sparren, Abschnitt b: Gefach). Anschließend flächenanteilig gewichten:
1/RT' = fa/RT,a + fb/RT,b + ... mit fa + fb + ... = 1,0 (Gl. 2.62)

**Unterer Grenzwert RT'':** In jeder Schicht wird der flächenanteilig gemittelte Wärmedurchlasswiderstand bestimmt, dann werden alle Schichten summiert:
1/Rj = fa/Ra,j + fb/Rb,j + ... (Gl. 2.64)

**Berechnungsbeispiel inhomogenes Bauteil:**
- Aufbau: Spanplatte (homogen, λ = 0,13 W/(m·K)) | inhomogene Schicht: Dämmstoff (A, λ = 0,04 W/(m·K)) neben Holz (B, λ = 0,13 W/(m·K)) | Spanplatte (homogen, λ = 0,13 W/(m·K))
- Schichtdicken: Spanplatten je 10 mm, Dämmstoff/Holz 180 mm; Breitenanteile: fa = 0,7 (Dämmung), fb = 0,3... (gemäß fa = 0,8/(0,7+0,8) nein — fa = 0,8, fb = 0,2 in den Rechenwerten)
- Oberer Grenzwert: RT,a = 4,978 m²K/W, RT,b = 1,862 m²K/W → 1/RT' = 0,875/4,978 + 0,125/1,862 → RT' = 4,12 m²K/W
- Unterer Grenzwert RT'' = 3,99 m²K/W
- Mittelwert RT = (4,12 + 3,99) / 2 = 4,06 m²K/W
- U = 1/4,06 = 0,25 W/(m²·K)

### Stationärer Temperaturverlauf im mehrschichtigen Bauteil (Abschn. 2.4)

#### Berechnung (Abschn. 2.4.1)

Im stationären Zustand gilt für die Wärmestromdichte: q = U · (θi – θe) (Gl. 2.65). Die Wärmestromdichte ist an jeder Stelle eines Bauteils gleich — von der Raumluft über alle Schichten bis zur Außenluft. Der Wärmetransport kann schrittweise aufgeteilt werden in inneren Übergang, Schicht 1, Schicht 2, usw., äußeren Übergang.

Aus diesen Schritten lassen sich die Temperaturen an Oberflächen und Schichtgrenzen ableiten. Für die raumseitige Oberflächentemperatur gilt: θsi = θi – q/hges,i; für jede Schichtgrenze: θ1/2 = θsi – q · d1/λ1; usw.

#### Grafisches Verfahren (Abschn. 2.4.2)

Alternativ kann der Temperaturverlauf grafisch ermittelt werden: Man trägt die Temperaturdifferenz (θi – θe) über dem Wärmedurchgangswiderstand auf. Im „thermischen Maßstab" ergibt sich eine Gerade, aus der Schichttemperaturen abgelesen werden können.

**Berechnungsbeispiel (Wand mit Außendämmung, Abb. 2.18):**
- Schicht 1: Gipsputz λ1 = 0,51 W/(m·K), d = 15 mm
- Schicht 2: Mauerwerk λ2 = 0,16 W/(m·K), d = 240 mm
- Schicht 3: Dämmung λ3 = 0,035 W/(m·K), d = 100 mm
- Schicht 4: Vormauerschale λ4 = 0,68 W/(m·K), d = 115 mm
- Randbedingungen: θi = 20 °C, θe = −10 °C; Rsi = 0,13, Rse = 0,04
- U = 0,212 W/(m²·K)
- Wärmestromdichte: q = 0,212 × (20 – (−10)) = 6,36 W/m²
- θsi = 20 – 6,36 × 0,13/1 ≈ 19,17 °C
- Schichttemperaturen (sequenziell): θ1/2 = 18,99 °C; θ2/3 = 9,47 °C; θ3/4 = −8,67 °C; θ4/se = −9,75 °C; θe = −10 °C

---

## Kapitel 3: Wärmebrücken (Seiten 44–59)

### Einführung

Gut dämmende Bauteile allein reichen nicht für guten Wärmeschutz; Bauteilanschlüsse müssen ebenso behandelt werden. An Anschlussdetails entstehen erhöhte Wärmeabflüsse und niedrigere raumseitige Oberflächentemperaturen, was zu zusätzlichen Wärmeverlusten und dem Risiko von Tauwasser- und Schimmelpilzbildung führt. Bei sehr gut gedämmten Bauteilen wirkt sich der Wärmebrückeneffekt besonders stark aus; bei innen gedämmten Konstruktionen kann er bis zu einem Drittel des gesamten Transmissionswärmeverlustes ausmachen. Tiefere Innenoberflächen- und gleichzeitig höhere Außenoberflächentemperaturen lassen sich mit Infrarot-Thermografie sichtbar machen (typische Schwachstellen: Stürze über Fenstern, Außenecken).

### Begriffsbestimmung (Abschn. 3.1)

Wärmebrücken sind örtlich begrenzte Zonen in der wärmeübertragenden Gebäudehülle, an denen gegenüber regulärem Wandaufbau ein erhöhter Wärmefluss auftritt, verbunden mit tieferer raumseitiger Oberflächentemperatur.

Typen:
- **Geometriebedingte Wärmebrücken:** entstehen bei Wechsel der Bauteildicke oder Unterschieden zwischen Außen- und Innenmaß (z. B. Außenwandecken)
- **Materialbedingte Wärmebrücken:** entstehen durch Materialwechsel in der Konstruktion (z. B. Sparren neben Gefach im Steildach, Stahlbetonstützen in Mauerwerkswänden, einbindende Geschossdecken)
- Häufig überlagern sich beide Typen (z. B. Fenster- oder Dachanschluss)

Hinweis: Weitere Begriffe wie „massenstrombedingter" oder „umgebungsbedingter" Wärmebrückeneffekt (z. B. abgehängte Decken, Möblierung) finden sich gelegentlich, werden jedoch in normativen Bewertungen nicht berücksichtigt.

Normative Grundlage für Wärmebrückenberechnungen: **DIN EN ISO 10211** [3]. Zur quantitativen Bestimmung kommen Wärmebrückenkataloge (z. B. [2]) oder numerische Rechenverfahren (FEM, FDM) zum Einsatz. Bei Katalogen ist das Erscheinungsjahr und die zugrundeliegenden Normen-Randbedingungen zu beachten.

### Raumseitige Oberflächentemperaturen (Abschn. 3.2)

Der bekannteste Wärmebrückeneffekt ist Schimmelpilzbefall. Zur Bewertung des Schimmelpilzrisikos wird die minimale raumseitige Oberflächentemperatur benötigt. Da absolute Temperaturen von Randwerten abhängen, wird stattdessen der **Temperaturfaktor fRsi** (auch: Temperaturdifferenzen-Quotient, früher f oder Θ) aus DIN EN ISO 10211 verwendet.

Definition:
fRsi = (θsi – θe) / (θi – θe) (Gl. 3.1)

Berechnung der raumseitigen Oberflächentemperatur:
θsi = fRsi · (θi – θe) + θe (Gl. 3.2)

**Anforderung nach DIN 4108-2, Kapitel 6:**
- Zur Vermeidung von Schimmelpilzbildung gilt: **fRsi ≥ 0,7** (Fenster ausgenommen; für Fenster: DIN EN ISO 13788)
- Maßgebliche Randbedingungen: θi = 20 °C, θe = −5 °C, φ = 50 %
- Bei fRsi = 0,7 ergibt sich: θsi = 0,7 × (20 – (−5)) + (−5) = **12,6 °C**

**Berechnungsbeispiel Fensterlaibung:**
- Fensteranschluss an ungedämmtes Mauerwerk: fRsi = 0,56
- θsi = 0,56 × (20 – (−5)) + (−5) = 9,0 °C → deutlich unter der zulässigen Mindesttemperatur von 12,6 °C → Schimmelpilzbefall an der Laibung ist unvermeidbar
- Fensteranschluss mit zusätzlicher Innendämmung, aber fehlender Laibungsdämmung: fRsi = 0,48 → θsi = nur 7 °C → Schimmelgefahr bereits bei sehr niedrigen Raumluftfeuchten

**Maximale zulässige Raumluftfeuchte** (Gl. 3.3 — gilt für 0 °C ≤ fRsi · (θi – θe) ≤ 30 °C):
φmax ≤ 0,8 · [109,8 · fRsi · (θi – θe) + 109,8] / (θi + 8,02) · 100 %

Für den Fensteranschluss (fRsi = 0,56, θi = 20 °C, θe = −5 °C):
φmax ≤ 40 %

Bei unsachgemäßer Sanierung (fRsi = 0,48, fehlende Laibungsdämmung):
φmax ≤ 34 %

**Biologische Grundlagen Schimmelpilz:**
- Pilzsporen sind permanent in der Umgebungsluft vorhanden und gelangen durch Kleidung oder Lebensmittel in Wohnungen
- Wesentliche Faktoren für Schimmelwachstum: geeigneter Nährboden (z. B. Tapeten, Kleister, Farben, Haushaltsschmutz) und ausreichend hohe Feuchte
- Schimmelpilze benötigen keine Taupunktsunterschreitung; es reichen Oberflächentemperaturen aus, bei denen sich lokal eine relative Feuchte von 80 % einstellt
- Pilze können ihren Stoffwechsel vorübergehend unterbrechen und bei günstigen Bedingungen erneut aktivieren

**Vermeidungsmaßnahmen:**
- Nutzungsbedingt: ausreichendes Beheizen und Lüften zur Begrenzung der Raumluftfeuchte
- Baulich: möglichst hohe raumseitige Oberflächentemperaturen in Anschlussdetails anstreben
- Strukturell: Substratentzug (z. B. Tapete in Fensterlaibung entfernen, lackieren) und Ermöglichung regelmäßiger Reinigung

### Wärmeverluste durch Wärmebrücken (Abschn. 3.3)

Zusätzliche Transmissionswärmeverluste werden mit Wärmebrückenverlustkoeffizienten beschrieben:
- **Ψ [W/(m·K)]** = längenbezogener Wärmebrückenverlustkoeffizient für linienförmige Wärmebrücken (pro laufenden Meter Einflusslänge)
- **χ [W/K]** = punktbezogener Wärmebrückenverlustkoeffizient für punktförmige Wärmebrücken (z. B. Drahtanker, Konsolen)

Der **Ψ-Wert** beschreibt analog zu U-Werten bei Flächenbauteilen den Wärmebrückenverlust im Bereich von Linienwärmebrücken. Er ergibt sich aus der Differenz zwischen dem tatsächlichen mehrdimensionalen Wärmestrom und dem eindimensionalen Bilanzierungsansatz (U · A):

ΔH = Φ/Δθ – U · A (Gl. 3.4)

Für A = a · b mit b = 1 m und Δθ = 1 K:
Ψ = H/a – U · a (Gl. 3.5)

In DIN EN ISO 10211: Ψ = L2D – Σ(Ui · ℓi) (Gl. 3.6), mit L2D = thermischer Leitwert 2D [W/K].

**Symboldefinitionen:**
- H [W/K] = temperaturspezifischer Wärmeverlust
- Φ [W] = Wärmestrom
- U [W/(m²·K)] = U-Wert des betrachteten Flächenbauteils
- L2D [W/K] = thermischer Leitwert, zweidimensional
- ℓi [m] = Einflusslänge

#### Negative Ψ-Werte (Abschn. 3.3.1)

Negative Ψ-Werte können zwei Ursachen haben:

1. **Geometrisch bedingt:** Im Eckbereich ist die Wärmestromdichte geringer als im ebenen Wandbereich. Bei außenmaßbezogener Bilanzierung wird die thermische Hüllfläche zu großzügig angesetzt; bei Berücksichtigung außenmaßbezogener Ψ-Werte wird dieser Fehler kompensiert. Betroffen sind z. B. Außenecken, Dachanschlüsse (Ortgänge, Traufen), Sockelanschlüsse. Wenn der Geometrieeinfluss größer ist als der stofflich-konstruktive, wird der außenmaßbezogene Ψ-Wert negativ. Innenmaßbezogene Ψ-Werte bei geometrischen Wärmebrücken sind grundsätzlich positiv; außenmaßbezogene können negativ sein.

2. **Überkompensation:** Wenn Wärmebrückenstellen mehr gedämmt werden als energetisch notwendig (z. B. starke Überdämmung von Fensterblendrahmen, Zusatzdämmung bei Geschossdeckeneinbindungen oder Stützen in monolithischen Wandkonstruktionen), können negative Ψ-Werte entstehen.

Innenmaßbezogene Ψ-Werte lassen sich stets auf Außenmaßbezug umrechnen; die Umkehrung (Außen → Innen) ist nicht immer möglich.

#### Bilanz der Transmissionswärmeverluste (Abschn. 3.3.2)

Der spezifische Transmissionswärmeverlust HT eines Gebäudes:

HT = Σ(Fi · Ui · Ai) + Σ(Fj · Ψj · ℓj) + Σ(Fk · χk) (Gl. 3.7)

- F = Temperaturkorrekturfaktor des Bauteils oder der Wärmebrücke
- U = U-Wert [W/(m²·K)]
- A = Bauteilfläche [m²]
- Ψ = längenbezogener Wärmedurchgangskoeffizient [W/(m·K)]
- χ = punktbezogener Wärmedurchgangskoeffizient [W/K]
- ℓ = Länge der Wärmebrücke [m]

Wichtig: Wärmebrücken können sich bezüglich Oberflächentemperatur und Wärmeverlusten sehr unterschiedlich auswirken. Zwei Konstruktionen mit identischen Ψ-Werten können stark unterschiedliche fRsi-Werte aufweisen (und umgekehrt). Seit EnEV 2002 ist der Wärmebrückeneinfluss im Nachweis nach dem Gebäudeenergiegesetz verpflichtend zu berücksichtigen. Ebenso bei der Heizlastberechnung nach DIN EN 12831.

### Praxisbeispiele (Abschn. 3.4)

#### 3.4.1 Innenwandanschluss — geneigtes Dach

Einbindung einer Innenwand in eine Dachfläche ohne oberseitige Dämmung (d = 0 cm) führt zu Ψ-Werten von **0,29 W/(m·K)**. Diese Wärmebrücke entspricht einer fiktiven Dachvergrößerung um beidseitig **1,26 m** Randstreifen. Der Wärmebrückeneinfluss lässt sich durch Hinzufügen einer oberseitigen Dämmung (Variation d) erheblich reduzieren.

#### 3.4.2 Dachanschluss — Ortgang

An einem typischen Ortganganschluss wird der fRsi-Wert durch die Dicke der Mauerkronendämmung (a) und die Dicke des Wärmedämmverbundsystems (b) beeinflusst:
- Die Dicke des WDVS-Systems b hat im betrachteten Bereich keinen signifikanten Einfluss auf fRsi und Ψ-Wert.
- Bereits **20 mm Wärmedämmung der Mauerkrone** halbieren den Ψ-Wert mehr als; der fRsi-Wert erreicht mit 0,734 bereits den Mindestwert von 0,7.
- Praktische Erkenntnis: Geringe Dämmstärken an der richtigen Stelle erzielen bereits große energetische Effekte.

#### 3.4.3 Sockelanschluss

Für einen Sockelanschluss (Abb. 3.14) gelten folgende Erkenntnisse bei Variation von Dicke des WDVS (a) und Länge der Sockeldämmung (b):
- Die WDVS-Dicke a hat weder auf fRsi noch auf Ψ nennenswerten Einfluss.
- Ungedämmte oder unzureichende Ausführungen (b < 300 mm) führen zu deutlichem Schimmelpilzrisiko und vergleichsweise hohen Wärmeverlusten.
- Ab einer Sockeldämmlänge b = **300 mm** liegen fRsi-Werte oberhalb des Grenzwerts 0,7.
- Das energetisch-praktische Optimum liegt bei ca. **b = 500 mm**.

#### 3.4.4 Balkonplatte

**Außengedämmte Variante (Abb. 3.15, Ψ-Werte innenmaßbezogen):**
- Bei ungedämmter Balkonplatte (a = 0, b = 0) treten keine kritischen Innenoberflächentemperaturen auf.
- Nur beidseitig (oben und unten) gedämmte Balkonplatten verbessern sowohl Oberflächentemperatur als auch Wärmeverlust.
- Einseitige Dämmung ist praktisch wirkungslos.

**Innengedämmte Variante (Abb. 3.16):**
- Bei ungedämmter Balkonplatte (a = 0, b = 0) tritt bei üblichem Mauerwerk (Ausnahme: λ = 0,21 W/(m·K)) immer fRsi < 0,7 auf — kritische Innenoberflächentemperatur.
- Auch hier gilt: Nur beidseitige Dämmung verbessert beide Kennwerte.
- Geringere Wärmeleitfähigkeit des Wandbaustoffs verbessert den Ψ-Wert; für die Innenoberflächentemperatur ist hingegen eine hohe Wärmeleitfähigkeit eher nachteilig.

#### 3.4.5 Fenster

**Fensteranschluss (Abschn. 3.4.5.1):**
Bei einem Fensteranschluss in einer Holzbauwand überlagern sich der Wärmebrückeneinfluss des Konstruktionsholzes (Stiel) und des Fensteranschlages. Bei thermisch günstiger Montageposition werden die Wärmebrückenverluste ab einer Rahmendämmstärke von ca. **40 mm** ausreichend reduziert. Aus architektonischer Sicht ist ein Kompromiss zwischen sichtbarer Blendrahmenbreite und energetischem Optimum erforderlich.

Empfehlung: Außendämmung a ≥ **60 mm**, um auch den Wärmebrückeneinfluss aller Konstruktionshölzer im Regelwandaufbau zu kompensieren. Mehrschalige Holzbauwände mit U-Wert < 0,2 W/(m²·K) und a > 100 mm erfüllen diese Anforderungen.

---

### Normreferenzen (Kapitel 2 + 3)

- **DIN 4108-4:2020-11** — Wärmeschutz im Hochbau: Wärme- und feuchteschutztechnische Kennwerte
- **DIN EN ISO 10456:2010-05** — Baustoffe: tabellierte Bemessungswerte und Bestimmungsverfahren
- **DIN EN ISO 6946:2018-03** — Bauteile: Wärmedurchlasswiderstand und U-Wert, Berechnungsverfahren
- **DIN EN ISO 10211** — Wärmebrücken: Berechnungsverfahren (normative Grundlage)
- **DIN 4108-2** — Wärmeschutz: Anforderungen an fRsi ≥ 0,7, Randbedingungen θi = 20 °C, θe = −5 °C, φ = 50 %
- **DIN EN ISO 13788** — Wärme- und feuchtetechnisches Verhalten: Tauwasser, speziell für Fenster
- **DIN EN 12831** — Heizlastberechnung: Wärmebrückeneinfluss ist einzubeziehen

### Materialdaten aus Tab. 2.1 (Fortsetzung — Wärmeleitfähigkeiten)

| Stoff | Rohdichte ρ [kg/m³] | λ-Bemessungswert [W/(m·K)] |
|-------|---------------------|---------------------------|
| Buche, Eiche | (800) | 0,20 |
| Sperrholz | (800) | 0,15 |
| Holzspan-Flachpressplatten | (700) | 0,13 |
| Harte Holzfaserplatten | (1000) | 0,17 |
| Kunststoffbeläge (z. B. PVC) | (1500) | 0,23 |
| Bitumendachbahnen / nackte Bitumenbahnen | (1200) | 0,17 (n. DIN 52128) |
| Lose Schüttungen aus porigen Stoffen | ≤ 100 bis ≤ 1500 | 0,060 bis 0,27 |
| Lose Schüttungen (Sand, Kies, Splitt, trocken) | (1800) | 0,70 |
| Glas | (2500) | 0,80 |
| Metalle | − | 15 bis 380 |

Hinweis: Werte in Klammern dienen nur zur Ermittlung der flächenbezogenen Masse (z. B. für sommerlichen Wärmeschutznachweis).
