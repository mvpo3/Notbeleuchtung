# Lehrbuch der Bauphysik — Teil 2
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 81-120.

Dieses Standardwerk zur Bauphysik behandelt in Teil 2 (Seiten 81–120) die Themen Wärmebrücken an Fenstern und Befestigungselementen (Abschluss Kap. 3), Lüftung von Gebäuden (Kap. 4) sowie Wärme- und Energiebilanzen für Bauteile, Räume und Gebäude (Kap. 5). Besonderer Fokus liegt auf Berechnungsverfahren, konkreten Kennwerten und normativen Anforderungen.

## Inhalt

### Fenster-U-Wert (Kap. 3.4.5.2)

Fenster sind bauphysikalisch komplexe Bauteile. Zur Bestimmung des U-Wertes stehen mehrere Methoden zur Verfügung:

- Tabellenwerte nach DIN 4108-4 und DIN EN ISO 10077-1 (Standardfenstergröße B × H = 1,23 × 1,48 m)
- Vereinfachte Berechnung anhand konstruktiver Merkmale nach DIN EN ISO 10077-1
- Numerische Berechnung (Finite-Elemente-Methode) nach DIN EN ISO 10077-2
- Messung im Heizkasten nach DIN EN ISO 12567-1

**Berechnungsformel (vereinfacht nach DIN EN ISO 10077-1):**

Der Gesamt-U-Wert des Fensters (Uw) ergibt sich aus den flächengewichteten Beiträgen von Verglasung (Ag × Ug) und Rahmen (Af × Uf) zuzüglich des linienförmigen Wärmebrückenanteils des Glasabstandshalters (Summe der Ψg-Werte multipliziert mit den jeweiligen Glasumfangslängen ℓg), geteilt durch die Gesamtfläche aus Glas- und Rahmenflächen.

Wichtiger Effekt: Bei gleichem Material sind kleine Fenster energetisch schlechter als große, da der Rahmenanteil proportional zunimmt.

**Tab. 3.1 — Linearer Wärmedurchgangskoeffizient Ψg [W/(m·K)] für Abstandshalter:**

| Hersteller / Typ | Rahmenmaterial | Glasaufbau 4/16/4 | Glasaufbau 4/12/4/12/4 |
|---|---|---|---|
| Konv. Alu-Abstandhalter | Holz | 0,068 | 0,074 |
| Konv. Alu-Abstandhalter | PVC | 0,067 | 0,070 |
| Konv. Alu-Abstandhalter | WGP* | 0,108 | 0,111 |
| Erbslöh (CHROMATECH) | Holz | 0,050 | 0,051 |
| Erbslöh (CHROMATECH) | PVC | 0,050 | 0,049 |
| Erbslöh (CHROMATECH) | WGP* | 0,070 | 0,065 |
| THERMIX | Holz | 0,040 | 0,040 |
| THERMIX | PVC | 0,040 | 0,039 |
| THERMIX | WGP* | 0,053 | 0,048 |

*WGP = Wärmegedämmte Metall-Kunststoff-Verbundprofile

---

### Befestigungselemente als punktförmige Wärmebrücken (Kap. 3.4.6)

Befestigungselemente vorgehängter hinterlüfteter Fassaden erzeugen punktförmige Wärmebrücken, beschrieben durch den Punktwärmedurchgangskoeffizienten χ (Chi). Mit zunehmender Länge des Elements steigt χ, da mehr wärmeübertragende Fläche entsteht.

Minderungsmaßnahmen:
- Wärmedämmende Distanzstücke zwischen Element und Wand
- Ummanteln der Befestigung

**Praktische Berücksichtigung über ΔU-Zuschlag:**
- 4 Befestigungselemente mit 60 mm Länge pro m² bei einer Kalksandsteinwand mit U = 0,29 W/(m²·K) erhöhen den effektiven U-Wert um ca. 35 %
- Regelmäßig auftretende punktförmige Wärmebrücken lassen sich über einen Aufschlag ΔU zum Wärmedurchgangskoeffizienten erfassen

---

### Kapitel 4: Lüftung

#### 4.1 Grundlagen und Anforderungen

Lüftung beeinflusst das thermische Verhalten von Gebäuden und die Raumluftqualität entscheidend. Antriebsarten:
- **Freie/natürliche Lüftung:** Temperaturdifferenzen und Windeinwirkung als Antrieb
- **Mechanische Lüftung:** Einsatz von Ventilatoren (Abluftsystem, Zuluftsystem, Zu-/Abluftsystem)

**Funktionen eines ausreichenden Luftwechsels:**
- Frischluftzufuhr für Personen
- Verbrennungsluftversorgung (z. B. Gasetagenheizung)
- Feuchtigkeitsabfuhr
- Schadstoffabfuhr und Sauerstoffversorgung
- Verhinderung von Schimmelbildung und Bauschäden

**Typische erforderliche Luftwechselraten:** 0,4 bis 1,0 h⁻¹ je nach Feuchteproduktion, Temperaturen, Wärmeschutz und Größe der Wohneinheit

**Normative Vorgaben:**
- DIN-Fachbericht 4108-8: Luftwechsel zur Vermeidung von Schimmelpilzwachstum
- DIN 1946-6: Nennluftwechsel 0,4 bis 0,8 h⁻¹ je nach Wohnungsgröße
- Gebäudeenergiegesetz (GEG): 0,6 bis 0,7-facher Luftwechsel bei freier Lüftung für Nachweis des Lüftungswärmebedarfs
- Bei modernen Gebäuden: Lüftungswärmeverluste bis zu 50 % der Gesamtwärmeverluste

---

#### 4.1 Infiltration

Infiltration bezeichnet den Luftaustausch über ungewollte Undichtheiten in der Gebäudehülle (fehlerhafte Fensterabdichtungen, Bauteilanschlüsse, Durchdringungen wie Kaminöffnungen).

**Negative Folgen von Infiltration:**
- Kein planmäßig dimensionierter Luftaustausch möglich
- Zugerscheinungen (lokale Komforteinbußen)
- Risiko von Bauteilschäden durch unkontrolliert durchströmende feuchte Luft
- Erhöhter Heizenergiebedarf
- Beeinträchtigung des Betriebs von Lüftungsanlagen (besonders mit Wärmerückgewinnung)

**Blower-Door-Verfahren zur Dichtigkeitsprüfung:**
- Einbau eines Ventilators in eine Gebäudeöffnung (z. B. Haustür)
- Erzeugung von Über- oder Unterdruck im Gebäude
- Messgröße: Luftwechsel n50 bei 50 Pa Druckdifferenz (bezogen auf Luftvolumen)

**Grenzwerte nach DIN 4108-7:**
- Gebäude ohne Lüftungsanlagen: n50 ≤ 3,0 h⁻¹
- Gebäude mit Lüftungsanlagen: n50 ≤ 1,5 h⁻¹
- Prüfung nach Nationalem Anhang der DIN EN ISO 9972:2018-12

**Durchschnittlicher Infiltrations-Luftwechsel:** 0,07 bis 0,7 h⁻¹ (Neubau: kleiner Wert; undichte ältere Gebäude: hoher Wert)

**Schwachstellen der Luftdichtheitsschicht (v. a. Holzbau):**
- Steckdosen in Innen- und Außenwänden
- Leuchteninstallationen in Decken
- Fußboden-/Wandanschlüsse bei bodentiefen Türen/Fenstern
- Übergänge zwischen Bauteilen (Wand/Dachanschluss)
- Durchdringungen (Kamin, Lüftungsrohre)

**Planungskonzept Luftdichtheitsebene (DIN 4108-7):**
- Umlaufende Dichtungsebene, die ohne Unterbrechung durch alle Bauteile führt (Planungsprinzip: Stift ohne Absetzen nachzeichnen)
- Folienanschlüsse an Mauerwerk: dauerhaft feste Verbindung + spannungsfreier Anschluss notwendig
- Durchdringungen: vorkonfektionierte Manschetten als Abdichtungslösung

---

#### 4.2 Fensterlüftung

Einflussfaktoren auf den Fensterluftwechsel: Gebäudeform/-lage, Fenstergröße und Öffnungsmöglichkeiten, meteorologische Bedingungen, Nutzerverhalten. Antriebskräfte sind Druckdifferenzen durch Wind, Temperaturdifferenzen Raum/Außen oder beides kombiniert.

##### 4.2.1 Einseitige Fensterlüftung

Nur eine Außenseite des Raums hat ein Fenster. Im Winterfall: kalte dichtere Luft tritt unten ein, wärmere leichtere Luft verlässt den Raum oben.

**Berechnungsformel für den Luftvolumenstrom V [m³/h]:**

V = Al × Θ × 3600 × (C1 × u² + C2 × H × Δθ + C3)^(1/2)

Variablen:
- Al: lichte Öffnungsfläche des Fensters [m²]
- Θ: Durchflussverhältnis [-] (abhängig von Fensteröffnungsweite)
- u: Windgeschwindigkeit [m/s]
- H: Höhe der lichten Fensteröffnung [m]
- Δθ: Temperaturdifferenz innen/außen [K]

Koeffizienten für übliche Dreh-/Kippfenster:
- C1 = 0,0056 [-]
- C2 = 0,0037 [m/(s²·K)]
- C3 = 0,012 [m²/s²]

**Tab. 4.1 — Durchflussverhältnisse Θ in Abhängigkeit von Fensteröffnungsweite:**

| Kippfenster Öffnungsweite [cm] | Θ [-] | Drehfenster Öffnungsweite | Θ [-] |
|---|---|---|---|
| 2 | 0,0715 | 5 cm | 0,1948 |
| 4 | 0,0943 | 10 cm | 0,2890 |
| 6 | 0,1204 | 15 cm | 0,3850 |
| 8 | 0,1426 | 45° | 0,8208 |
| 10 | 0,1752 | 90° | 1 |
| 12 | 0,2036 | | |
| 14 | 0,2172 | | |

##### 4.2.2 Querlüftung

Fenster in gegenüberliegenden Fassaden; zusätzlich zum Temperatur- und Windanteil tritt Strömung durch das Gebäude hinzu. Zweiter Strömungswiderstand durch zweite Öffnung muss berücksichtigt werden.

**Koeffizienten für Kippfenster bei Querlüftung:**
- C1 = 0,01965 [-]
- C2 = 1,896 × 10⁻³ [m/(s²·K)]
- C3 = 0,01706 [m²/s²]
- C4 = 0,0194 [-]

**Rechenbeispiel Querlüftung:**
- 2 gegenüberliegende Fenster mit je Al = 1 m², H = 1 m
- Kippstellung 10 cm: Θ = 0,1752
- Bedingungen: θi = 20 °C, θe = 0 °C, u = 2 m/s
- Ergebnis: VZu = 355 m³/h

---

#### 4.3 Mechanische Lüftung

Mechanische Lüftungsanlagen liefern eine einstellbare, weitgehend witterungsunabhängige Luftmenge. Vorteil gegenüber Fensterlüftung: deutlich geringere Schallbelästigung durch Außenlärm.

##### 4.3.1 Abluftanlagen

Zentral oder dezentral arbeitende Systeme, die Luft aus geruchs-, feuchte- oder schadstoffbelasteten Räumen abführen. Mechanisch erzeugter Unterdruck ca. 4 Pa bewirkt Nachströmen der Luft durch definierte Zuluftöffnungen.

**Bestandteile einer zentralen Abluftanlage:**
- Zentralgerät mit Ventilator (Ventilatorbox)
- Rohrsystem mit Schalldämpfern und Filtern
- Abluftventile in den Ablufträumen (ggf. feuchtegeregelt)
- Nachströmöffnungen

Dezentrale Variante: Einzelventilatoren in Toiletten oder Küchen (Dunstabzugshauben). Abluft kann über Wärmepumpe energetisch genutzt werden (Heizungsunterstützung oder Warmwasserbereitung).

##### 4.3.2 Zu-/Abluftanlagen

Be- und Entlüftung über jeweils eigene Ventilatoren. Kernvorteil: Bei zentraler Anordnung mit Wärmetauscher kann der Abluft Wärme entnommen und der Zuluft zugeführt werden (Wärmerückgewinnung).

**Bestandteile einer Zu-/Abluftanlage mit Wärmerückgewinnung:**
- Zentralgerät mit Zu- und Abluftventilatoren sowie Wärmeübertrager (z. B. Kreuzstrom-Plattenwärmeübertrager)
- Zuluftkanalsystem zu Wohn- und Schlafräumen
- Abluftkanalsystem von Ablufträumen (Bad, Küche, WC)
- Luftein- und -auslässe
- Schalldämpfer und Filter im Kanalsystem

**Wärmerückgewinnung (WRG):**
- Wärmerückgewinnungsgrad: Gütemerkmal der Anlage; gute Anlagen > 80 %
- Vorzugsweise Gleichstromventilatoren für geringen Stromeinsatz
- Hydraulisch optimiertes Kanalsystem erforderlich
- Voraussetzung: besonders dichte Gebäudehülle
- Keine Zugerscheinungen wie bei Fensterlüftung oder Abluftanlagen

---

### Kapitel 5: Wärme- und Energiebilanzen

#### 5.1 Bauteilbilanzen

##### 5.1.1 Strahlungsbilanz für Fensterglas

Sonneneinstrahlung auf Fensterglas teilt sich in drei Anteile auf:
- **Reflexion R (oder ρ):** zurückgeworfene Strahlung
- **Absorption A (oder α):** im Glas aufgenommene Energie → Glaserwärmung
- **Transmission T (oder τ):** direkt durchgelassene Strahlung in den Raum

Grundbeziehung: R + A + T = 1

Der absorbierte Anteil wird teils nach innen (sekundärer Wärmeabgabegrad qi) und teils nach außen (qe) abgegeben: α = qi + qe

**Gesamtenergiedurchlassgrad g** fasst direkte Transmission τ und sekundäre Wärmeabgabe nach innen qi zusammen:
g = τ + qi

Die Wärmestromdichte q durch die Verglasung:
q = U × (θi − θe) − g × I

Für eine Einzelscheibe:
g = τ + α × U / he

**Berechnungsbeziehungen für Zweischeibenglas:**
- Gesamttransmission: τ = τ1 × τ2 / (1 − ρ1 × ρ2)
- Gesamtreflexion: ρ = ρ1 + τ1² × ρ2 / (1 − ρ1 × ρ2)
- Absorption in Scheibe 1 (außen): αe = α1 + τ1 × α1 × ρ2 / (1 − ρ1 × ρ2)
- Absorption in Scheibe 2 (innen): αi = τ1 × α2 / (1 − ρ1 × ρ2)

**Rechenbeispiel Zweischeiben-Wärmedämmglas:**
- Ug = 1,1 W/(m²·K); R = 0,74 (m²·K)/W; τ = 0,54; αe = 0,09; αi = 0,06
- he = 23 W/(m²·K) (normativer Wert)
- Berechnung: g = 0,54 + 1,1 × (0,09 + 0,06) / 23 + 0,06 × 0,74 = 0,60

**Typische g-Werte:**
- Zweischeiben-Wärmedämmglas: ca. 0,48 bis 0,72
- Dreischeiben-Wärmedämmglas: ca. 0,50 bis 0,60
- Sonnenschutzglas, 2-scheibig: ca. 0,25 bis 0,48
- Sonnenschutzglas, 3-scheibig: ca. 0,16 bis 0,34

##### 5.1.2 Strahlungsbilanz für opake Bauteile

Opake Bauteile (Außenwände, Dächer) weisen keine Transmission auf. Der Gesamtenergiedurchlassgrad vereinfacht sich zu:
g = α × U / he

**Rechenbeispiel Außenwand:**
- UAW = 0,28 W/(m²·K); α = 0,5
- g = 0,28 × 0,5 / 23 = 0,006
- Der g-Wert opaker Bauteile ist damit deutlich kleiner als bei Fensterglas.

##### 5.1.3 Äquivalenter Wärmedurchgangskoeffizient

Im Winter erzeugen transparente Bauteile gleichzeitig Wärmesenken (U-Wert) und Wärmequellen (g-Wert). Der äquivalente Wärmedurchgangskoeffizient Ueq fasst beide Effekte zusammen:

Stationärer Fall: Ueq = U − g × I / (θi − θe)

Für Betrachtungen über die gesamte Heizperiode wird ein Strahlungsgewinnkoeffizient SF eingeführt:
Ueq,W = UW − g × SF

**Strahlungsgewinnkoeffizienten SF für vereinfachte Berechnung:**
- Südorientierung: SF = 2,4 W/(m²·K)
- Ost-/Westorientierung: SF = 1,65 W/(m²·K)
- Nordorientierung: SF = 0,95 W/(m²·K)

**Rechenbeispiel für Zweischeiben-WDG (UW = 1,3 W/(m²·K), g = 0,6):**
- Ueq,Süd = 1,3 − 0,6 × 2,4 = −0,14 W/(m²·K) → Netto-Wärmegewinn im Winter
- Ueq,Ost/West = 1,3 − 0,6 × 1,65 = 0,31 W/(m²·K) → ähnlich wie gut gedämmte Außenwand
- Ueq,Nord = 1,3 − 0,6 × 0,95 = 0,73 W/(m²·K) → deutlich schlechter

##### 5.1.4 Wärmetransport in Hohlräumen

In Bauteilhohlräumen (Installationsschichten im Holzbau, mehrschalige Wände, Scheibenzwischenräume) wirken alle drei Wärmetransportmechanismen: Wärmeleitung, Konvektion und Strahlung.

Für praktische Anwendungen wird der Wärmedurchlasswiderstand der Hohlraumschicht normativ vorgegeben (abhängig von Dicke und Lage horizontal/vertikal).

**Berechnung des Wärmedurchlasswiderstands R im Hohlraum:**

R = d / (Nu × λ) + [σ × Tm³ × (1/ε1 + 1/ε2 − 1)]⁻¹

Mit:
- λ: Wärmeleitfähigkeit des Gases [W/(m·K)]
- d: Spaltbreite [m]
- σ = 5,67 × 10⁻⁸ W/(m²·K⁴) (Stefan-Boltzmann-Konstante)
- Tm: absolute mittlere Temperatur im Hohlraum [K]
- ε1, ε2: Emissionsgrade der Oberflächen [-]

**Nusselt-Zahl für Hohlräume in Baukonstruktionen:**
Nu = 1 + 1,1 × Ra^0,024 / (Ra + 10100)^1,39 (nach Literaturquelle [3])

**Ergebnisse aus Berechnungen (Tm = 283 K, Temperaturdifferenz 5 K):**
- Ab ca. 4 cm Schichtdicke ist der Wärmedurchlasswiderstand weitgehend konstant
- Bei ε1 = ε2 = 0,9: R ≈ 0,18 (m²·K)/W
- Kleine Emissionskoeffizienten (Low-ε-Oberflächen) erhöhen R erheblich
- Konstruktionsprinzip „Luftschicht-Dämmung": hintereinander angeordnete Luftschichten von 2–4 cm Dicke, getrennt durch Folien mit kleinem ε

**Gasfüllungen für Fensterscheibenzwischenräume — Stoffwerte nach DIN EN 673 (Tab. 5.1):**

| Gas | Temp. [°C] | Dichte ρ [kg/m³] | Dyn. Viskosität η [kg/(m·s)] | Wärmeleitfähigkeit λ [W/(m·K)] | Wärmekapazität c [J/(kg·K)] |
|---|---|---|---|---|---|
| Luft | −10 | 1,326 | 1,661×10⁻⁵ | 2,366×10⁻² | 1,008×10³ |
| Luft | 0 | 1,277 | 1,711×10⁻⁵ | 2,416×10⁻² | — |
| Luft | 10 | 1,232 | 1,761×10⁻⁵ | 2,496×10⁻² | — |
| Luft | 20 | 1,189 | 1,811×10⁻⁵ | 2,576×10⁻² | — |
| Argon | −10 | 1,829 | 2,038×10⁻⁵ | 1,584×10⁻² | 0,519×10³ |
| Argon | 0 | 1,762 | 2,101×10⁻⁵ | 1,634×10⁻² | — |
| Argon | 10 | 1,699 | 2,164×10⁻⁵ | 1,684×10⁻² | — |
| Argon | 20 | 1,640 | 2,228×10⁻⁵ | 1,734×10⁻² | — |
| SF6 (Schwefelhexafluorid) | −10 | 6,844 | 1,383×10⁻⁵ | 1,119×10⁻² | 0,614×10³ |
| SF6 | 0 | 6,602 | 1,421×10⁻⁵ | 1,197×10⁻² | — |
| SF6 | 10 | 6,360 | 1,459×10⁻⁵ | 1,275×10⁻² | — |
| SF6 | 20 | 6,118 | 1,497×10⁻⁵ | 1,354×10⁻² | — |
| Krypton | −10 | 3,832 | 2,260×10⁻⁵ | 0,842×10⁻² | 0,245×10³ |
| Krypton | 0 | 3,690 | 2,330×10⁻⁵ | 0,870×10⁻² | — |
| Krypton | 10 | 3,560 | 2,400×10⁻⁵ | 0,900×10⁻² | — |
| Krypton | 20 | 3,430 | 2,470×10⁻⁵ | 0,926×10⁻² | — |
| Xenon | −10 | 6,121 | 2,078×10⁻⁵ | 0,494×10⁻² | 0,161×10³ |
| Xenon | 0 | 5,897 | 2,152×10⁻⁵ | 0,512×10⁻² | — |
| Xenon | 10 | 5,689 | 2,226×10⁻⁵ | 0,529×10⁻² | — |
| Xenon | 20 | 5,495 | 2,299×10⁻⁵ | 0,546×10⁻² | — |

**U-Wert-Richtwerte für Verglasungstypen:**
- Altbau-Isolierglas (Luft, keine Beschichtung): ca. 2,8 W/(m²·K)
- Modernes Wärmeschutzglas: Argon-Füllung + Low-ε-Beschichtung (ε = 0,04); wirtschaftlich günstig gegenüber Krypton/Xenon (trotz niedrigerer λ dieser Edelgase)
- Dreischeiben-WDG: U-Wert sinkt mit zunehmender Zwischenraumbreite; aus baukonstruktiven Gründen sind sehr große Scheibenabstände begrenzt

Nusselt-Zahl für Scheibenzwischenräume nach DIN EN 673:
Nu = 0,035 × Ra^0,38

Randbedingungen für U-Wert-Berechnung nach DIN EN 673:
- Mittlere Temperatur im Gasraum: 283 K
- Temperaturdifferenz äußere Glasflächen: 15 K
- Innerer Wärmeübergangskoeffizient: 8 W/(m²·K)
- Äußerer Wärmeübergangskoeffizient: 23 W/(m²·K)
- Emissionskoeffizient unbeschichtetes Glas: 0,837
- Glasdicke: je 4 mm
- Wärmeleitfähigkeit Glas: 1 W/(m·K)

---

#### 5.2 Raumbilanzen

Das thermische Verhalten eines Raums entsteht aus dem Zusammenwirken externer und interner Einflussgrößen:

**Externe Einflüsse:**
- Strahlungsenergie durch Fenster (trifft auf innere Oberflächen und Einrichtungsgegenstände)
- Wärmequellen im Fensterglas oder am Sonnenschutz durch absorbierte Strahlung
- Transmissionswärme durch Fenster und Außenbauteile
- Luftaustausch zwischen Raum und Außenluft

**Interne Einflüsse:**
- Wärmequellen und -senken im Raum
- Transmissionswärme durch Innenbauteile aus Nachbarräumen
- Luftaustausch mit Nachbarräumen
- Langwelliger Strahlungsaustausch zwischen Raumoberflächen

**Raumbilanz-Grundgleichung:**
(VL × ρL × cL + VSp × ρSp × cSp) × Δθi/Δt = W + Qi − ΦT − ΦL

Variablen:
- ΦT: Transmissionswärmestrom zwischen Luft und Umschließungsflächen [W]
- ΦL: Lüftungswärmestrom [W]
- Qi: interne Wärmesenken/-quellen [W]
- W: Heiz- oder Kühlleistung [W]
- θi: Raumlufttemperatur [°C]

Wärmeaustausch mit Umschließungsflächen:
ΦT = Σj (hi,j × Aj × (θi − θsi,j))

Lüftungswärmestrom:
ΦL = n × V × c × ρ × (θi − θe)

Für den Sommerfall (Raumlufttemperatur gesucht) und Winterfall (Heiz-/Kühlleistung gesucht) können die Gleichungen entsprechend umgestellt werden.

---

#### 5.3 Zonen-/Gebäudebilanzen

Mehrere Räume mit gleicher oder ähnlicher Nutzung, gleichen Raumtemperaturen und gleichen Anlagensystemen werden zu einer Zone zusammengefasst. Das folgende stationäre Bilanzverfahren gilt primär für Wohngebäude; Bilanzzeitraum ist typischerweise Monat oder Jahr; Ergebnis in kWh/a bzw. kWh/(m²·a).

##### 5.3.1 Endenergiebedarf

Bilanzgleichung für den Endenergiebedarf QE:
QE = Qh + Qw + Qt − Qr

- Qh: Heizwärmebedarf [kWh/a] = Nutzwärmebedarf; beschreibt wärmeschutztechnische Qualität der Gebäudehülle; wird durch Bilanzierung von Transmissions- und Lüftungsverlusten abzüglich solarer und interner Gewinne ermittelt
- Qw: Warmwasserwärmebedarf [kWh/a]; Pauschalwert für vereinfachte Berechnungen nach GEG: 12,5 kWh/(m²·a); basiert auf 23 Liter pro Person pro Tag bei 50 °C Wassertemperatur
- Qt: Anlagentechnische Wärmeverluste [kWh/a] (Rohrwärmeverluste in unbeheizten Kellern, Speicherverluste, Abgasverluste)
- Qr: Nutzung von Umweltwärme [kWh/a] (z. B. Erdwärme über Wärmepumpe; solare Einträge durch transparente Bauteile sind NICHT in Qr enthalten, sondern in Qh)

Die Endenergie umfasst auch Hilfsenergie (Strom für Pumpen, Regelung) und wird an der Gebäudehülle übergeben — das ist der Betrag, den der Verbraucher zahlt.

##### 5.3.2 Primärenergiebedarf

Primärenergie berücksichtigt zusätzlich die vorgelagerten Prozessketten: Gewinnung, Umwandlung und Transport des Energieträgers außerhalb der Systemgrenze Gebäude. Eignung als Kenngröße für ökologische Bewertung (z. B. CO₂-Emissionen).

Berechnung nach DIN V 4701-10 über Anlagen-Aufwandszahl eP (= Kehrwert des Nutzungsgrads):
QP = (Qh + QW) × eP

##### 5.3.3 Berechnung des Heizwärmebedarfs

Berechnungsverfahren nach DIN V 4108-6; für GEG-Nachweis ausschließlich das Monatsbilanzverfahren zulässig.

**Monatsweise Verlust-Gewinn-Bilanz:**
Qh,M = Q1,M − ηm × Qg,M

- Q1,M: monatlicher Verlust
- Qg,M: monatlicher Gewinn
- ηm: monatlicher Ausnutzungsgrad

**Monatliche Verluste (Transmission + Lüftung):**
Q1,M = (HT + HV) × (θi − θe) × tM × 0,024

- HT: spezifischer Transmissionswärmeverlust [W/K]
- HV: spezifischer Lüftungswärmeverlust [W/K]
- θe: mittlere monatliche Außentemperatur [°C]
- θi: Soll-Innentemperatur (mittlere Gebäudeinnentemperatur) [°C]
- tM × 0,024: Anzahl Tage × Umrechnungsfaktor (0,024 kWh = 1 Wd)

**Monatliche Wärmegewinne:**
Qg,M = 0,024 × (Φs,M + Φi,M)

- Φs,M: mittlerer monatlicher Solarstrahlungsgewinn [W]
- Φi,M: Wärmegewinn aus internen Quellen [W]

###### 5.3.3.1 Transmissionswärmeverluste

Berechnung unter Berücksichtigung von Bauteilflächen, U-Werten, Temperatur-Korrekturfaktoren und Wärmebrücken (linienförmig; punktförmige werden meist vernachlässigt):

HT = Σi (Fi × Ui × Ai) + Σj (Fj × ℓj × Ψj)

Alternativ über pauschalen Wärmebrückenkorrekturwert ΔUWB:
HT = Σi (Fi × Ui × Ai) + ΔUWB × Ages

**Wärmebrückenkorrekturwert ΔUWB:**
- Standardwert: 0,10 W/(m²·K)
- Bei Verwendung von Regelkonstruktionen entsprechend DIN 4108 Beiblatt 2, Kategorie A: 0,05 W/(m²·K)
- Bei ausschließlicher Verwendung von Details der Kategorie B (energetisch und feuchteschutztechnisch höherwertig): 0,03 W/(m²·K)

**Tab. 5.2 — Temperatur-Korrekturfaktoren Fx für verschiedene Bauteile:**

| Bauteil / Wärmestromweg | Symbol | Fx |
|---|---|---|
| Außenwand | Faw | 1,0 |
| Dach (als Systemgrenze) | Fd | 1,0 |
| Dachgeschossdecke (nicht ausgebauter Dachraum) | Fd | 0,8 |
| Abseitenwand (Drempel) | Fu | 0,8 |
| Wände und Decken zu unbeheizten Räumen | Fu | 0,5 |
| Wände und Decken zu niedrig beheizten Räumen | Fnb | 0,35 |
| Wände/Decken zu unbeheiztem Glasvorbau – Einfachverglasung | fu | 0,8 |
| Wände/Decken zu unbeheiztem Glasvorbau – Zweischeibenverglasung | fu | 0,7 |
| Wände/Decken zu unbeheiztem Glasvorbau – Wärmeschutzverglasung | fu | 0,5 |
| Fußboden beheizter Keller (B' < 5 m, Rf ≤ 1) | Fg = Fbf | 0,30 |
| Fußboden beheizter Keller (B' < 5 m, Rf > 1) | Fg = Fbf | 0,45 |
| Fußboden beheizter Keller (B' 5–10 m, Rf ≤ 1) | Fg = Fbf | 0,25 |
| Fußboden beheizter Keller (B' 5–10 m, Rf > 1) | Fg = Fbf | 0,40 |
| Fußboden beheizter Keller (B' > 10 m, Rf ≤ 1) | Fg = Fbf | 0,20 |
| Fußboden beheizter Keller (B' > 10 m, Rf > 1) | Fg = Fbf | 0,35 |
| Wand beheizter Keller (alle B', Rw ≤ 1) | FG = Fbw | 0,40 |
| Wand beheizter Keller (alle B', Rw > 1) | FG = Fbw | 0,60 |
| Fußboden auf Erdreich ohne Randdämmung (B' < 5 m, Rf ≤ 1) | FG = Fbw | 0,45 |
| Fußboden auf Erdreich ohne Randdämmung (B' < 5 m, Rf > 1) | FG = Fbw | 0,50 |
| Fußboden auf Erdreich ohne Randdämmung (B' 5–10 m, Rf ≤ 1) | FG = Fbw | 0,40 |
| Fußboden auf Erdreich ohne Randdämmung (B' 5–10 m, Rf > 1) | FG = Fbw | 0,50 |
| Fußboden auf Erdreich ohne Randdämmung (B' > 10 m, Rf ≤ 1) | FG = Fbw | 0,25 |
| Fußboden auf Erdreich ohne Randdämmung (B' > 10 m, Rf > 1) | FG = Fbw | 0,35 |
| Fußboden auf Erdreich mit Randdämmung 2 m waagerecht (B' < 5 m) | Fg = Fbf | 0,30 |
| Fußboden auf Erdreich mit Randdämmung 2 m senkrecht (B' < 5 m) | FG = Fbw | 0,25 |
| Fußboden auf Erdreich mit Randdämmung 2 m waagerecht (B' 5–10 m) | Fg = Fbf | 0,25 |
| Fußboden auf Erdreich mit Randdämmung 2 m senkrecht (B' 5–10 m) | FG = Fbw | 0,20 |
| Fußboden auf Erdreich mit Randdämmung 2 m waagerecht (B' > 10 m) | Fg = Fbf | 0,20 |
| Fußboden auf Erdreich mit Randdämmung 2 m senkrecht (B' > 10 m) | FG = Fbw | 0,15 |
| Kellerdecke zum unbeheizten Keller mit Perimeterdämmung (B' < 5 m) | Fg | 0,55 |
| Kellerdecke ohne Perimeterdämmung (B' < 5 m) | Fg | 0,70 |
| Kellerdecke mit Perimeterdämmung (B' 5–10 m) | Fg | 0,50 |
| Kellerdecke ohne Perimeterdämmung (B' 5–10 m) | Fg | 0,65 |
| Kellerdecke mit Perimeterdämmung (B' > 10 m) | Fg | 0,45 |
| Kellerdecke ohne Perimeterdämmung (B' > 10 m) | Fg | 0,55 |
| Aufgeständerter Fußboden | Fg | 0,90 |
| Niedrig beheizte Räume (12–19 °C) Bodenplatte (B' < 5 m, Rf ≤ 1) | Fg | 0,20 |
| Niedrig beheizte Räume Bodenplatte (B' < 5 m, Rf > 1) | Fg | 0,55 |
| Niedrig beheizte Räume Bodenplatte (B' 5–10 m, Rf ≤ 1) | Fg | 0,15 |
| Niedrig beheizte Räume Bodenplatte (B' 5–10 m, Rf > 1) | Fg | 0,50 |
| Niedrig beheizte Räume Bodenplatte (B' > 10 m, Rf ≤ 1) | Fg | 0,10 |
| Niedrig beheizte Räume Bodenplatte (B' > 10 m, Rf > 1) | Fg | 0,35 |

Hinweise zu Tab. 5.2:
- B' = Ag / (0,5 × P); Rf = Wärmedurchlasswiderstand Bodenplatte; Rw = Wärmedurchlasswiderstand Kellerwand
- Bei fließendem Grundwasser: Temperatur-Abminderungsfaktoren um 15 % erhöhen
- Randdämmung: Wärmedurchlasswiderstand > 2 m²K/W; Bodenplatte ungedämmt
- Kellerdecke mit Trittschalldämmung: UKD < 0,5 W/(m²K); Kellerfußboden ungedämmt
- Niedrig beheizte Räume: Innentemperatur 12 °C bis 19 °C

###### 5.3.3.2 Lüftungswärmeverluste

HV = n × V × ρL × cpL

Mit: ρL × cpL = 0,34 Wh/(m³·K)

**Ansatz für den Luftwechsel n je nach System:**
- Natürliche Lüftung, Luftdichtheit nicht geprüft: n = 0,7 h⁻¹
- Natürliche Lüftung, Luftdichtheit messtechnisch nachgewiesen: n = 0,6 h⁻¹
- Zu-/Abluftanlage mit Wärmerückgewinnung: n = 0,6 h⁻¹
- Abluftanlage: n = 0,55 h⁻¹
- Bei mechanischer Lüftungsanlage: messtechnische Prüfung der Gebäudedichtheit zwingend

###### 5.3.3.3 Solare Wärmegewinne

Für transparente Außenbauteile:
Φs,M = Σ (Ij × Fs,j × FC,j × Ff,i × g,i × Ai)

Für opake Außenbauteile (inkl. langwelliger Abstrahlung):
Φs = Σ (Ai × Ui × Re × (αs,i × Ij × Fs,j − hr,i × Δθer))

Variablen:
- I: Strahlungsintensität [W/m²]
- Fs: Minderungsfaktor für Verschattung [-]
- FC: Minderungsfaktor für Sonnenschutz [-]
- Ff: Minderungsfaktor für Rahmenanteil [-]
- g: wirksamer Gesamtenergiedurchlassgrad [-]
- A: Fläche des Bauteils [m²]
- Re = Rse: Wärmeübergangswiderstand außen [(m²·K)/W]
- αs: Absorptionsgrad des opaken Bauteils [-]
- hr: äußerer Abstrahlungskoeffizient [W/(m²·K)]
- Δθer: Temperaturdifferenz Außenluft/Himmel [K]

###### 5.3.3.4 Interne Wärmegewinne

Interne Wärmegewinne resultieren aus Wärmeabgabe von Personen und elektrischen Geräten (vgl. Kap. 6):

Φi = qi × AB

Mit:
- qi: mittlere interne Wärmegewinne [W/m²]
- AB: Bezugsfläche [m²]

---

### Normreferenzen dieses Teils

- DIN 4108-2:2013-02 — Mindestanforderungen Wärmeschutz
- DIN 4108-4:2020-11 — Bemessungswerte Wärme- und Feuchteschutz
- DIN 4108-7:2011-01 — Luftdichtheit von Gebäuden
- DIN 4108 Beiblatt 2 — Musterlösungen Wärmebrücken (Kategorien A und B)
- DIN-Fachbericht 4108-8:2010-09 — Schimmelwachstum in Wohngebäuden
- DIN V 4108-6 — Heizwärmebedarfsberechnung (Monatsbilanzverfahren)
- DIN V 4701-10 — Anlagen-Aufwandszahl / Primärenergiebedarf
- DIN 1946-6:2019-12 — Lüftung von Wohnungen, Nennluftwechsel
- DIN EN ISO 9972:2018-12 — Luftdurchlässigkeit von Gebäuden (Blower-Door)
- DIN EN ISO 10077-1:2020-10 — Fenster-U-Wert allgemein
- DIN EN ISO 10077-2:2018-01 — Fenster-U-Wert numerisch
- DIN EN ISO 10211:2018-04 — Wärmebrücken, detaillierte Berechnung
- DIN EN ISO 12567-1:2010-12 — Heizkasten-Messung Fenster
- DIN EN ISO 13788:2013-05 — Oberflächentemperatur, Tauwasser
- DIN EN 673 — Scheibenzwischenraum, Gasstoffwerte, Nusselt-Zahl
- DIN EN 12831:2003-08 — Norm-Heizlast
- Gebäudeenergiegesetz (GEG), Bundesgesetzblatt 2020, Nr. 37
