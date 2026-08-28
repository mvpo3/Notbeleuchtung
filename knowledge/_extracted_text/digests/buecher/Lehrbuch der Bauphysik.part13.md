# Lehrbuch der Bauphysik — Teil 13
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 521-560.

Dieser Teil behandelt die mathematische Modellierung des Raumluftfeuchte-Jahresgangs (Kapitel 18, Abschn. 18.3–18.5), eine vollständige Beispielrechnung für einen Archivraum (Abschn. 18.4) mit numerischen Eingabeparametern und Ergebnissen, die Beschreibung des Simulationsprogramms CLIMT, dessen Validierung an zwei Testgebäuden sowie den Einstieg in Kapitel 19 (Klimagerechtes Bauen) mit Klimazoneneinteilung und autochthonen Bauweisen.

## Inhalt

### 18.3 Modellierung der Feuchtebilanz — Tages- und Jahresgang der Raumluftfeuchte

Das Berechnungsmodell aus Kapitel 17 (Raumtemperaturen) lässt sich analog auf den Jahres- und Tagesgang des Wasserdampfdrucks und der relativen Raumluftfeuchte übertragen. Das Feuchtemodell ist vergleichsweise einfach, weil Feuchte kaum durch Transmission durch opake Bauteile übertragen wird (Ausnahme: Schlagregen) und keine analoge „Feuchtestrahlung" existiert.

**Größen im Modell (analog zur Energiebilanz):**
- Außen: Wasserdampfdruck pDe, Sättigungsdruck pse, relative Luftfeuchte ϕe
- Innen: pDi, psi, ϕi
- Feuchtespeicherstrom der Raumluft: dmSPL/dt
- Feuchtespeicherstrom der Raumumschließungsflächen und Einrichtungsgegenstände: dmSPi/dt
- Über Lüftung übertragener Feuchtestrom: dmL/dt
- Feuchteübergangsstrom von Raumluft zur Innenfläche: dmÜi/dt
- Feuchtequellstrom innerer Quellen: dmQu/dt

**Bilanzgleichungen (Gln. 18.35–18.39):**
- Gl. (18.35): In der Raumluft gespeicherter Feuchtestrom = CLF · d/dt(pi)
- Gl. (18.36): Von Raumumschließungsflächen und Einrichtungsgegenständen gespeicherter Feuchtestrom = CFi · d/dt(pi)
- Gl. (18.37): Durch Luftumströmung übertragener Feuchtestrom = VL · nL / RD · (pe/Te − pi/Ti)
- Gl. (18.38): Von Raumumschließungsflächen auf-/abgegebener Feuchtestrom = ÜiF · (poi − pi)
- Gl. (18.39): Von inneren Feuchtequellen abgegebener Feuchtestrom = mptV · VL

**Gesamtbilanzgleichungen (Gln. 18.40–18.42):**
- Gl. (18.40): Feuchtebilanz an Außenoberfläche = 0 (für Raumluftfeuchte nicht relevant, entfällt)
- Gl. (18.41): Raumluft-Feuchtebilanz (kombiniert Lüftungsterm, Feuchteübergang, Quellterm)
- Gl. (18.42): Innenflächen-Feuchtebilanz (nur Feuchteübergang, ohne Transmissions- und Strahlungsterme)

**Feuchtespeicherfähigkeit der Raumluft CLF in kg/Pa:**
- Gl. (18.43): CLF = VL / (RD · Ti)
- RD = 462 Ws/(kg·K) — Gaskonstante für Wasserdampf
- nL = Luftwechselrate in 1/h

**Spezifische Lüftungsfeuchteströme LFi und LFe (druckbezogen, Gln. 18.44a/b):**
- LFi = VL · nL / (RD · Ti)
- LFe = VL · nL / (RD · Te)

**Feuchteübertragungswert Raumluft/Raumumschließungsfläche ÜiF in kg/(s·Pa) — Gl. (18.45):**
- Summation über alle j = 1 bis 9 Teilflächen: ÜiF = Σ hcWij · AWij
- Dabei ist 7,9 · 10⁻⁹ ein charakteristischer Umrechnungskoeffizient

**Feuchtequellen:**
Der gesamte Feuchteproduktionsstrom mptV wird vollständig (nicht zur Hälfte wie bei Wärmequellen) an die Raumluft abgegeben.

**Feuchtespeicherung der Innenflächen CiF in kg/Pa = s²/m (Gl. 18.46):**
- CiF = Σ (tsp/2)^(1/2) · π · δL · μ⁻¹ · ρW · wh / ps · AWij
- tsp = Eindringzeit des hygrischen Signals in s
- ρW = 10³ kg/m³ (Wasserdichte)
- δL = 1,85 · 10⁻¹⁰ s (Dampfleitfähigkeit in Luft)
- μ⁻¹ = Wasserdampfleitfähigkeit im porösen Baustoff
- wh = Anstieg der sorptionsgebundenen Feuchte bei Erhöhung von rel. Luftfeuchte 40 % → 80 %, in m³Feuchte/m³Material
- ps = Wasserdampfsättigungsdruck an der absorbierenden Oberfläche bei Temperatur θoi (Pa)
- AWij = absorbierende Raumumschließungsfläche bzw. Einrichtungsgegenstände-Oberfläche in m²

**Zeitschrittlösung (j → j+1, Gl. 18.47):**
- Wasserdampfdruck an Innenfläche poi,j+1 = poi,LIM,j + (poi,j − poi,LIM,j) · exp(−1/βFj)
- poi,LIM,j = Grenzwert des Drucks nach unendlich langer Zeit
- βFj = Zeitkonstante des Feuchteeinstellvorgangs im Zeitschritt j+1

**Grenzwert poi,LIM,j (Gl. 18.48):**
- poi,LIM,j ≈ pe,j + (mptV · RD · Ti) / nL,j

**Zeitkonstante βFj (Gl. 18.49):**
- βFj = CiF / (RD · Ti · (VL · nL,j + 1/ÜiF)⁻¹)

**Sättigungsdruck der Außenluft pse,j (Gl. 18.50):**
- Für positive Außentemperaturen θe,j: pse,j = 610,5 · exp(17,26 · θe,j / (237,3 + θe,j))
- Für negative Außentemperaturen: pse,j = 610,5 · exp(21,87 · θe,j / (265,5 + θe,j))
- Die Sprungfunktion Φ = 1 für positive, 0 für negative Argumente

**Wasserdampfdruck der Außenluft pe,j (Gl. 18.51):**
- pe,j = ϕe,j · pse,j

**Wasserdampfdruck der Raumluft pi,j+1 (Gl. 18.52):**
- Aus Kombination von Oberflächenwert po,j+1 mit Lüftungsterm und Feuchteübergangswert ÜiF

**Relative Raumluftfeuchte ϕi,j+1 (Gl. 18.53):**
- ϕi,j+1 = pi,j+1 / psi,j+1

Damit lässt sich aus bekannten Werten zum Zeitpunkt j der nächste Stundenstand berechnen — ohne Iteration. Die Lüftungsrate n(j) kann manuell oder klimagesteuert vorgegeben werden.

---

### 18.4 Beispielrechnung für einen wärme- und feuchteträgen Archivraum

**Raumgeometrie und Grundparameter:**
- Grundfläche: An = 200 m²
- Raumhöhe: h = 3 m
- Raumvolumen: VI = 600 m³
- Westfenster: Af = 5 m² (Verhältnis Af/An = 5/200 = 0,025)
- Lage: Zwischengeschoss (keine Dachflächen)
- Außenklima: Klimadatei Dresden 1997 (stündliche Messwerte)
- Ziel: möglichst konstantes Raumklima ohne aufwendige Klimatisierung

#### 18.4.1 Raum- und Bauteilparameter

**Wärmeübergangswerte:**

| Größe | Wert |
|---|---|
| αi (innen, gesamt) | 7,5 W/(m²·K) |
| αic (innen, konvektiv) | 2,2 W/(m²·K) |
| αe (außen) | 14 W/(m²·K) |
| Ri (Innenübergangswiderstand) | 0,133 m²·K/W |
| Re (Außenübergangswiderstand) | 0,071 m²·K/W |

**Außenwanddaten (nur Westwand vorhanden):**

| Richtung | Fläche (m²) | Dichte (kg/m³) | U-Wert (W/m²K) | Absorptionskoeff. | U'-Wert ohne Überg. (W/m²K) |
|---|---|---|---|---|---|
| Süd | 0 | 1000 | 0,5 | 0,6 | 0,557 |
| West | 25 | 2100 | 0,3 | 0,6 | 0,320 |
| Nord | 0 | 1400 | 0,4 | 0,3 | 0,436 |
| Ost | 0 | 1000 | 0,5 | 0,5 | 0,557 |

**Dachflächen:** keine (Zwischengeschoss), Platzhalterwerte: Ad1 = Ad2 = 0

**Gesamtdurchlassgrad Fenster (Westfenster):**
- Berechnet aus Verschattungsgrad, Glasdurchlasskoeffizient und Rahmenfaktor
- Jahresabhängig: sf1 = 0,193 ... sf5 = 0,070 (verschiedene Winkelkonfigurationen)

**Innenbauteile:**

| Bauteil | Fläche (m²) | Dichte (kg/m³) |
|---|---|---|
| Innenwand 1 | 60 | 1600 |
| Innenwand 2 | 25 | 2100 |
| Innenwand 3 | 60 | 1600 |
| Innenwand 4 | 30 | 1600 |
| Decke | 200 | 1400 |
| Fußboden | 200 | 1400 |

- Gesamte innere Raumumschließungsfläche Aoi = 580 m²

**Speicherwirksame Massen (Eindringtiefe thermisches Signal):**
- Speicherzeit: tsp = 3600 · 10 · 24 s (10 Tage)
- λ = 0,7 W/(m·K), ρ = 1500 kg/m³, c = 1000 Ws/(kg·K)
- Bücher: cB = 900 Ws/(kg·K)
- Thermische Eindringtiefe: xE = 0,358 m

**Speicherwirksame Massen im Einzelnen:**
- Innenwände: mwi = 5,265 · 10⁶ kg (mit Faktor 0,18 für wirksame Schicht)
- Außenwände (West): mwe = 9,45 · 10⁵ kg
- Decke: mde = 5,04 · 10⁶ kg (nicht Schreibfehler: 5040 × 10³ in Quelle)
- Fußboden: mn = 5,04 · 10⁶ kg
- Bücher: mB = 6 · 10⁴ kg
- Gesamte speicherwirksame Masse: mi = 2,229 · 10⁷ kg
- Gesamte thermische Speicherkapazität Ci = 2,169 · 10¹¹ Ws/K
- Außenseitige Speicherkapazität Ce = 9,45 · 10⁹ Ws/K
- Spezifische Masse: (mi + mwe) / An = 1,162 · 10⁵ kg/m²

**Spezifische Transmissionswärmeströme:**
- Opake Außenwände T'W = 7991 W/K (Westwand kwe2' · Awe2 dominiert)
- Fenster Tf = 9000 W/K

**Spezifische Übergangswärmeströme:**
- Üi (Innen, nur konvektiv) = αic · Aoi = 2,2 · 580 = 1276 W/K
- Üe (Außen) = αe · (Σ Dach- und Wandflächen) = 14 · 25 = 350 W/K

#### 18.4.2 Außenklimatische Belastung des Raumes

**Klimamatrix Dresden (Beispiel Tag 101, Stunden 2424–2448):**
Spaltenbezeichnungen der Klimamatrix KD:
- Spalte 0: Zeit in h
- Spalte 1: Außenlufttemperatur in °C
- Spalte 2: Relative Luftfeuchtigkeit in %
- Spalte 3: Direkte Strahlung in W/m²
- Spalte 4: Diffuse Strahlung in W/m²
- Spalte 5: Niederschlag in m³/(m²·h)
- Spalte 6: Windgeschwindigkeit in m/s
- Spalte 7: Windrichtung in °

**Ausgewählte Stundenwerte Tag 101 (Stunden 2424–2448):**

| Stunde | Temp (°C) | rel.Feuchte (%) | Direkt (W/m²) | Diffus (W/m²) | Niederschl. | Wind (m/s) | Richtung (°) |
|---|---|---|---|---|---|---|---|
| 2424 | 3,35 | 75,61 | 0 | 0 | 0 | 8,30 | 262,60 |
| 2427 | 2,94 | 76,48 | 0 | 0 | 0 | 7,20 | 269,50 |
| 2431 | 3,05 | 82,59 | 4,53 | 45,78 | 0 | 5,80 | 270,10 |
| 2435 | 4,78 | 75,55 | 324,10 | 183,40 | 0 | 10,40 | 277,70 |
| 2438 | 6,92 | 62,38 | 284,90 | 260,10 | 0 | 8,40 | 278,80 |
| 2442 | 5,34 | 75,40 | 18,82 | 44,34 | 0 | 5,30 | 12,00 |
| 2446 | 1,74 | 91,06 | 0 | 0 | 0 | 0,50 | 320,80 |
| 2448 | 1,16 | 84,40 | 0 | 0 | 0 | 0,20 | 315,10 |

**Strahlungsberechnung für vertikale Westwand (α = 90°, β = 270° = West):**
- Deklinationswinkel δ(t): nach Gl. (16.15), mit Breitengrad χ = 52° (Dresden)
- Zeitindex j = 1 bis 8756 (stündliche Jahresschritte), t(j) = j/24 (Tageszahl)
- Höhenwinkel h(t): nach Gl. (16.14)
- Azimutwinkel A(t): nach Gl. (16.16)
- Sonnenscheindauer-/Tageslängenfunktion D(t): nach Gl. (16.8) als Sprungfunktion Φ(h)
- Winkelhilfsfunktion B(t,α,β): Gl. (16.18) — multipliziert Horizontalstrahlung → Strahlung auf geneigte/orientierte Fläche
- Eigenverschattungsfunktion SE(t,α,β): Gl. (16.19) — berücksichtigt Abschattung durch das Bauteil selbst
- Direkte Strahlungswärmestromdichte auf beliebige Fläche: Gdir(j,β) = Gab(j) · B(j,β) · [cos(α) · D(j) + SE(j,β) · sin(α)], Gl. (16.20)
- Gesamtstrahlungswärmestromdichte auf beliebige Fläche (direkt + diffus): Gl. (16.21)
  - Diffusanteil mit Faktoraufteilung 0,65 (Himmel) + 0,35 (Reflex)
- Strahlungswärmestrom durch Westfenster: Sf(j,β) = sf(j) · Af2 · GR(j,β) in W
- Jahresabhängiger Gesamtdurchlassgrad des Westfensters sf(j) mit sinusförmigem Jahresgang (Verschattungsänderung)
- Von Westwand absorbierter Gesamtwärmestrom SW(j,β) = aW · Awe2 · GR(j,β) in W (davon geht ein Teil nach innen, ein Teil an Umgebung)
- Jahresgang des Lüftungswärmestroms L(j) mit cosinusförmiger Abhängigkeit von Außentemperatur (Grundlüftung 0,3/h, Jahresamplitude 0,2)

#### 18.4.3 Berechnung der Raumtemperaturen

**Heizregelung (raumlufttemperaturgesteuert):**
- Heizfaktor: k = 2100 W/K
- Einschalt-Grenztemperatur der Raumluft: Ti1 = 20,5 °C
- Anfangstemperatur: Ti0 = 21,0 °C
- Heizleistung: I(j) = k · (Ti0 − Ti1) · Φ(Ti0 − Ti,j) — springt ein, wenn Raumluft unter 20,5 °C

**Einstellkoeffizient b(j) (thermische Trägheit):**
- Berechnet aus Speicherkapazitäten Ci, Ce, Wärmeübergangswerten Üi, Üe, Transmissionswärmestrom T'W, Lüftungswärmestrom L(j) und Fenster Tf

**Ergebnisse Raumlufttemperatur:**
- Raumlufttemperatur Ti,j+1 nach Gl. (18.34) berechnet, schwankt zwischen 20 °C und 23 °C
- Außenlufttemperatur zeigt deutlich stärkere Schwankungen (Dresden-Klimadaten)
- Erkenntnis: In Räumen mit guter Wärmedämmung, hoher speicherwirksamer Bauwerksmasse, kleiner Fensterfläche und guter Außenverschattung lässt sich in Mitteleuropa ein stabiles thermisches Raumklima ohne Klimaanlage erzielen

**Spezifischer mittlerer Heizwärmeverbrauch:**
- Gesamtheizarbeit: IHm = Σ I(j) für j = 1 bis 8756 = 968.542 W·h
- Spezifischer Jahresheizwärmebedarf: qm = IHm / (An · 8756/24) = 42.422 Wh/m² ≈ 42,4 kWh/(m²·a)

#### 18.4.4 Berechnung der relativen Luftfeuchtigkeit im Raum

**Eingabedaten für die Feuchteberechnung:**

| Parameter | Symbol | Wert | Einheit |
|---|---|---|---|
| Wasserdampfleitfähigkeit Luft | δL | 1,85 · 10⁻¹⁰ | s |
| Dampfdiffusionskoeffizient Baustoff | μ | 5 | — |
| Hygroskopizität Baustoff | wh | 0,08 | m³/m³ |
| Dichte Wasser | ρW | 1000 | kg/m³ |
| Konvektiver Wärmeübergangskoeff. innen | hiC | 2,2 | W/(m²·K) |
| Umrechnungskoeff. thermisch → hygrisch | b0 | 79 · 10⁻⁹ | (kg·K)/(W·s·Pa) |
| Gaskonstante Wasserdampf | RD | 462 | Ws/(kg·K) |
| Innere feuchtspeichernde Fläche (inkl. Bücher) | AoiB | 16.000 | m² |
| Raumvolumen | VI | 600 | m³ |
| Hygrische Eindring-/Speicherzeit | Tsp | 24 · 3600 · 10 | s |
| Zeitschritt | t1 | 3600 | s |
| Absolute Raumtemperatur | Ti | 293 | K |
| Sättigungsdruck bei Ti = 293 K | PS | 2336 | Pa |
| Feuchteproduktionsrate innere Quellen | mptV | 0,0005 | kg/(m³·h) |
| Anfangswert Wasserdampfdruck Innenfläche | p0j | 1330 | Pa |

**Feuchtekapazität CiF der Innenflächen + Bücher:**
- CiF = (Tsp/2)^(1/2) · π · δL · μ⁻¹ · ρW · wh / PS · AoiB
- CiF = 4,723 kg/Pa

**Feuchteübergangswert ÜiF:**
- ÜiF = b0 · hiC · AoiB = 79 · 10⁻⁹ · 2,2 · 16000 = 2,781 · 10⁻³ kg/(s·Pa)

**Luftwechselrate:** nL(j) = L(j) / (VI · 0,34) — abgeleitet aus spezifischem Lüftungswärmestrom L(j)

**Hygrischer Einstellkoeffizient βF(j) und Einstellzeit τF(j):**
- βF(j) = 1 / (CiF · (RD · Ti / (VI · nL(j)) + 1/ÜiF)) [1/s]
- τF(j) = 1/βF(j) · 1/3600 [h]

**Zeitschrittberechnung Wasserdampfdruck an Innenfläche po (Gl. 18.47 angewandt):**
- po(j+1) = (poi,LIM + (p(j) · (Ti,j+1 + 273) / (Ti + 273) + mptV · RD · Ti / nL(j))) · (1 − exp(−βF(j) · t1))

**Wasserdampfdruck der Raumluft pi(j+1):**
- Aus Gewichtung von po(j+1) mit ÜiF und Lüftungsterm VL · nL(j) / (RD · Ti)

**Ergebnisse relative Raumluftfeuchte:**
- Raumluftfeuchte liegt deutlich gedämpfter als Außenluftfeuchte
- Ohne Bücher würde die Raumluftfeuchte zwischen 38 % und 74 % schwanken
- Mit Büchern als hygrischer Speichermasse deutlich geringere Schwankungsbreite
- Etwas höhere Werte im Herbst können durch leicht erhöhte Heizung gedämpft werden

---

### 18.5 Nutzerfreundliche Umsetzung — Programm CLIMT

CLIMT (CLimate-Indoor-Moisture-Temperature) implementiert den in Abschn. 18.2–18.3 entwickelten Algorithmus als Windows-Programm (Visual Studio 2008, Win32-API, ohne Zusatzbibliotheken, getestet auf Windows 7). Berechnet stündliche Jahreswerte von Raumlufttemperatur und relativer Raumluftfeuchte.

#### 18.5.1 Programmbeschreibung CLIMT

**Programmdateien (alle im selben Ordner):**

| Datei | Funktion |
|---|---|
| climt.exe | Ausführbare Hauptdatei |
| setup.ini | Initialisierung |
| fenster.fst | Konstruktionsbeschreibungen transparente Bauteile |
| baustoffe.bst | Baustoffdatensätze |
| klima.bin | Klimadatensatz (Binärformat) |
| klimagenerator.exe | Tool zur Erstellung von Klimadatensätzen |
| kgsetup.ini | Initialisierung Klimagenerator |
| climt_hilfe.chm | Hilfedatei mit Einführungsbeispiel |

**Projektdateien (je Anwendungsfall):**

| Datei | Inhalt |
|---|---|
| projektname.prj | Projektinitialisierung |
| projektname.tre | Strukturdefinition |
| projektname.elm | Bauteildefinitionen |
| projektname.mat | Opake Bauteilkonstruktionen |
| projektname.cal | Zeitabschnittdefinitionen |
| projektname.rb | Randbedingungseinstellungen |
| projektname.gtv | Grenztemperaturverlauf |

**Benutzeroberfläche:**
- Hauptfenster mit Hauptmenü und Ergebnisdiagramm
- x-Achse einstellbar von 1 Stunde bis 1 Jahr
- Zwei unabhängig skalierbare y-Achsen, je bis zu 3 Kurven gleichzeitig
- Verfügbare Kurvengrößen: Raumlufttemperatur (°C), Mittlere Innenoberflächentemperatur (°C), Gefühlte Temperatur (°C), Außentemperatur (°C), Relative Innenluftfeuchte (%), Relative Außenluftfeuchte (%), Globalstrahlung (W/m²), Heizleistung (W), Leistung innerer Wärmequellen ohne Heizung (W), Solarstrahlungsleistung durch Fenster (W), Lüftungswärmestrom (W)
- Messwerte für Temperatur und relative Feuchte aus externer Textdatei einlesbar (für Vergleich mit Messung)

**Raumdefinition:**
- Eingabe: Volumen und Grundfläche
- Interne Abbildung als Baumdatenstruktur mit 3 Hierarchieebenen: Bauteil → Teilelemente (z.B. Fenster, Türen) → Unter-Teilelemente (z.B. Glasteile in Türen)
- Untergeordnete Elemente erben Richtung und Neigung vom übergeordneten Bauteil

**Bauteiltypen (Einstellmöglichkeiten):**
- Opake Außenfläche: Beaufschlagung mit Außenklima, Absorption der Solarstrahlung, thermische und hygrische Speicherung der oberflächennahen Schicht
- Transparente Außenfläche: Außenklima + Solardurchlass entsprechend vorgegebenem Gesamtenergiedurchlassgrad
- Innenfläche: Nur als Wärme- und Feuchtespeicher (aktive Schicht bis zur thermischen/hygrischen Eindringtiefe)
- Interne Speicherkapazität: Einrichtungsgegenstände analog zur Innenfläche

**Orientierungseinstellungen:**
- 5 Neigungswinkel gegen Horizontale wählbar: 0°, 30°, 45°, 60°, 90°
- 8 Himmelsrichtungen: N, S, O, W, NO, NW, SO, SW
- Festverschattungswert: fixer Abminderungsfaktor für Fremdverschattung (Nachbarbebauung, Baumbewuchs, Sonnensegel)
- Variable Fensterverschattung: getrennt behandelt, nicht im Festverschattungswert enthalten
- Nach jeder Eingabeänderung automatische Neuberechnung mit Vorschaugrafik

**Bauteilkonstruktionsbeschreibungen:**
- Opake Bauteile: Schichtaufbau (je Schicht: Dicke + Verweis auf Baustoffdatensatz), bis zu 40 Konstruktions-Platzhalter verfügbar
- Transparente Bauteile: Bezeichnung + Gesamtenergiedurchlassgrad + U-Wert der Verglasung (W/(m²·K)) + Rahmenanteil (%)

**Klimadaten:**
- Erzeugung mit klimagenerator.exe aus Textdatei mit 8760 Zeilen (eine je Stunde/Jahr)
- Pflichtparameter je Stunde: Außenlufttemperatur, relative Außenluftfeuchte, Globalstrahlung (alternativ Direkt- + Diffusstrahlung)
- Falls nur Globalstrahlung vorhanden: Zerlegung in Direkt-/Diffusanteil nach Gl. (16.21) oder Erbs-Korrelation
- Klimadateien müssen als .bin-Dateien im Programmverzeichnis vorliegen
- Langwellige Abstrahlung wird nach Abschn. 16.23 berücksichtigt

**Luftwechselrate (Modellierungsoptionen):**
- Detailliert: Jahresverlauf aus Zeitabschnitten → Tagtypen → Stundensegmente (je mit Luftwechselwert)
- Vereinfacht: vordefinierte Jahresverlauffunktion aktivierbar
- Alternativ: Einlesen einer Textdatei mit 8760 Stundenwerten

**Heizungsmodell:**
- Lineare Heizkennlinie mit Parametern Heizfaktor, Grundleistung, Ausschalttemperatur
- Wahlweise basierend auf Außenlufttemperatur + Strahlungseintrag oder Innenraumlufttemperatur
- Alternativ: Zeitabschnitt → Tagtyp → Stundensegment-Definition mit je eigener Heizkennlinie

**Innere Wärmequellen (Definition je Stundensegment):**
- Personenanzahl, Wärmeabgabe pro Person (als Tätigkeitsmerkmal oder freie Zahleneingabe)
- Beleuchtungswärmestrom (grundflächenbezogene Vorgabewerte je Raumnutzungstyp hinterlegt)
- Sonstige Wärmequellen (freier Wert)

**Innere Feuchtequellen (analog zu Wärmequellen):**
- Personenanzahl + aktivitätsabhängige Feuchteabgabe des Menschen
- Volumenbasierte Vorgabewerte für verschiedene Feuchtebelastungsgruppen wählbar

**Fensterverschattung (Modellierungsoptionen):**
- Zeitabhängig und/oder strahlungsabhängig (kombinierbar)
- Je Stundensegment: fester Verschattungsgrad + Aktivierungsgrenzwert (Strahlungsschwellwert)
- Überschreitet auftreffender Strahlungswärmestrom den Grenzwert → Verschattungsgrad wird aktiviert
- Je 4 Haupthimmelsrichtungen ein eigenes Verschattungsmodell
- Abweichungen zwischen Fenstern gleicher Richtung aber unterschiedlicher Neigung möglich

**Ergebnisdarstellung:**
- Alle Ergebnisgrößen grafisch durch Anklicken einer Kurve abrufbar
- Export als Textdatei möglich
- Druckausgabe aller Berechnungsergebnisse und Eingaben

#### 18.5.2 Ermittlung des Raumklimas in zwei Testgebäuden

**Testgebäude 1 — Schwimmendes Haus, Partwitzer See (Südbrandenburg), errichtet 2006:**

Konstruktive Beschreibung:
- Schwimmender Betonponton als Fundament
- Außenhülle: Stahltragwerk mit Holz- und Gipskartonbeplankung + Mineralwolledämmung
- Dachverkleidung: verzinktes Stahlblech, außen mit Sonnensegel verschattet
- Außenwände: Lärchenholzverkleidung
- Bodenrahmen: schwimmend gelagert, Holzbeplankt, Mineralwolle-Dämmung
- Fußbodenbelag: Fliesen (EG) und Parkett (OG)
- Fenster und Glastüren: Zweischeibenwärmeschutzverglasung mit Argonfüllung
- Innenwände: Massivholzbauweise
- Zwei Geschosse: Eingangsflur, Sanitärraum, Schlafzimmer, Wohnraum
- Wohnraum über beide Geschosse, thermisch am stärksten belastet

**Maße des untersuchten Wohnraums:**
- Volumen: 69,80 m³
- Grundfläche: 18,40 m²
- Innenwände: 17,76 m²
- Opake Außenwände: Süd 8,5 m², Ost 19,03 m², West 20,13 m²
- Fensterflächen: Süd 6,76 m², Ost 1,20 m²
- Dachfläche: 14,55 m²
- Anteil zur Terrasse: 3,85 m²
- Zwischendecke: 7,52 m²
- Küchentrennwand: 2,38 m²
- Südverglasung weitgehend außen verschattet, Ostfenster unverschattet

**Heizungsausstattung:**
- Zwei raumthermostatgeregelte Elektroheizgeräte zu je 1,5 kW → max. 3 kW Gesamtleistung
- In CLIMT: innenraumtemperaturgeregelt, Leistungsbegrenzung 3 kW
- Heizfaktor je Tagtyp: 40 W/(m²·K)

**Unterschiedliche Solltemperaturphasen (Thermostateinstellungen im Jahr 2008):**
- Frostschutz: 6 °C
- Heizperiode unbewohnt: 14 °C
- Bewohnte Perioden: 21 °C bis 24 °C

**Luftwechselraten:**
- Heizperiode (unbewohnt): konstant 0,3/h bis 0,5/h
- Sommer (genutzt): 00:00–07:00 Uhr: 0,7/h; 07:00–20:00 Uhr: 3,0/h; 20:00–24:00 Uhr: 0,7/h
- Erhöhte Nachtlüftung zur Kühlung wurde von Urlaubern offenbar nicht praktiziert

**Belegungsprofil und innere Quellen:**
- Januar/Februar: unbewohnt (14 °C Heizung)
- März/April: sporadisch an Wochenenden
- Mai–Oktober: fast durchgehend mit Urlaubern unterschiedlicher Nutzungsgewohnheiten
- November/Dezember: Instandsetzungsarbeiten, Stromversorgung teils unterbrochen → Frostschutz 6 °C
- Bei Belegung Heizperiode: 07:00–24:00 Uhr 2 Personen
- Bei Belegung Sommer: 07:00–09:00, 11:00–13:00, 19:00–24:00 Uhr 2 Personen
- Zusätzliche Quellen für Küche/Wohnraum 11:00–13:00 und 19:00–24:00 Uhr
- Leistung innerer Wärmequellen: 100 W bis 500 W
- Feuchteabgabe Normalnutzung: 0,07 kg/h; während Kochen/Abwaschen: + 0,56 kg/h
- Dauerwärmequellen (Kühlschrank, Warmwasserbereitung etc.) als Konstante

**Validierungsergebnis Raumlufttemperatur:**
- Vergleich CLIMT-Rechnung vs. Messwerte vs. TRNSYS-Rechnung
- Übereinstimmung als nahezu perfekt eingestuft
- Sowohl Absolutwerte, Amplituden der Schwankungen als auch thermisches Trägheitsverhalten stimmen überein
- Lüftungsregime wurde vereinfacht nachgestellt

**Validierungsergebnis relative Luftfeuchtigkeit:**
- Übereinstimmung weniger perfekt als bei Temperatur, aber befriedigend
- Raumluftfeuchte reagiert empfindlicher auf Lüftung, Temperaturschwankungen und innere Feuchtequellen
- Feuchtspeichernde Eigenschaften der Innenflächen gehen korrekt in die Rechnung ein

**Testgebäude 2 — Magazingebäude Bibliothek Magdeburg:**
- Archivraum: Zielklima 15 °C < Temperatur < 20 °C; 40 % < rel.Luftfeuchte < 55 %
- Außenklima: Magdeburg 2012
- Berechnung mit CLIMT: Einhalten der Zielparameter bestätigt
- Übereinstimmung CLIMT-Rechnung mit Messwerten (Temperatur + rel. Luftfeuchte): nahezu perfekt
- Wenn Archivgut halbiert (geringere Feuchtespeicherkapazität): rel. Luftfeuchte schwankt zwischen 40 % und 65 % (unzulässig hoch)
- Stabilisierung durch einfache mechanische Lüftung + Heizung + große hygrische Speichermasse des Archivguts
- Fensterloser massiver Bau → geringe außenklimatische Belastung

**Literaturverweise Kapitel 18 (Auswahl):**
- Aronin: Climate and Architecture, Reinhold Publ. Corp., New York, 1953
- Glück: Wärmetechnisches Raummodell, C.F. Müller Verlag, Heidelberg, 1997
- Petzold: Raumlufttemperaturen, 2. Aufl., Verlag Technik, 1983
- Petzold: Wärmelast, 2. Aufl., Verlag Technik, 1980
- Hansel: Dokumentation CLIMT, Hochschule Lausitz, 2011 (unveröffentlicht)
- Klein: TRNSYS — Transient System Simulation Program, Madison USA, 2000
- Häupl: Bauphysik — Klima, Wärme, Feuchte, Schall, 550 S., Ernst & Sohn, Berlin, 2008
- Häupl, Bishara, Hansel: Modell und Programm CLIMT, Bauphysik H. 3, S. 185–206, Ernst & Sohn, 2010
- Schuhmacher: Digitale Simulation regenerativer elektrischer Energieversorgungssysteme, Diss. Univ. Oldenburg, 1991

---

### 19 Klimagerechtes Bauen (Einstieg, Abschn. 19.1–19.3)

#### 19.1 Klimazonen der Erde

**Begriffsklärungen:**
- Wetter: lokale Konditionen (Sonneneinstrahlung, Lufttemperatur, Wind, Niederschlag, Luftfeuchte) über kurzen Zeitraum (Stunden bis wenige Tage)
- Witterung: entsprechende Beschreibung über längeren Zeitraum, bis zu jahreszeitlicher Erscheinung
- Klima: statistisch aufbereitetes Durchschnittswetter über mehrere Jahrzehnte (klassisch 30 Jahre, gemäß IPCC-Definition)
- Für Bauwesen relevant: v.a. Außenlufttemperatur und daran gekoppelte relative Luftfeuchte

**Klimaklassifizierung:**
- Primäre Grundlage: Sonneneinstrahlung → Solarzonen der Erde
- Tatsächliches Klima abhängig von weiteren Faktoren: Wasserkörper, Höhenlage, Vegetation
- Gängige Klassifikationen: nach Neef, Flohn, Köppen, Troll und Pfaffen

**Skalenebenen des Klimas:**
- Makroklima: kontinentale und globale Zusammenhänge
- Mesoklima: klimatische Eigenschaften einzelner Länder oder großflächiger Landesteile (Abmessungen mehrere hundert km bis zu ausgeprägten Landschaften)
- Mikroklima: ausgeprägt lokale Klimaerscheinungen (begrenzte Stadtquartiere, innerhalb eines Gebäudes)

**Vereinfachte Klimazoneneinteilung für Bauzwecke:**
- Kalt (polar/subpolar)
- Gemäßigt
- Arid
- Tropisch

#### 19.2 Autochthone Bauweisen und Architektur

**Lebensbedingungen und Klimazonen:**
- Günstigstes Klima für Menschen: mediterranes Klima (Mittelmeerraum)
- Primäres Bauziel: Überleben in unveränderlichem Klima durch Schutz vor widrigen Witterungen
- Verwendung lokal verfügbarer regenerativer Baustoffressourcen
- Anforderung an Bautechnik: hohe Effizienz (auch Energieeffizienz im Dauerbetrieb)
- Erweiterung: reines Schutzbedürfnis → Komfortansprüche

**Autochthones Bauen:**
- Bezeichnet den grundlegenden, überall angewendeten Ansatz des Bauens aus lokalen Mitteln
- Behaglichkeitsvorstellungen aus europäischer Sicht sind kein Maßstab — es geht primär ums Überleben
- Architektur als Kunstform des Bauens: nach [4] historisch Privileg einer kleinen reichen Elite, die sich über Energieeffizienz und Unterhaltskosten hinwegsetzen konnte

#### 19.3 Kalte Klimazone

**Merkmale:**
- Polare und subpolare Gebiete der Erde
- Extrem niedrige Temperaturen über lange Zeiträume
- Kurze Hochtemperaturintervalle (Sommer) als Ausnahme
- [Detailausführungen folgen im weiteren Teil des Kapitels 19, außerhalb dieser Seiten]
