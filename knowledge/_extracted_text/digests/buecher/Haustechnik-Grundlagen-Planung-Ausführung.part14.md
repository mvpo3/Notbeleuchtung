# Haustechnik-Grundlagen-Planung-Ausführung — Teil 14
> Quelle: Haustechnik-Grundlagen-Planung-Ausführung (buecher) · Seiten 561-600.

Dieser Teil deckt das Ende der Heizlastberechnung nach DIN EN 12831 (Formblätter R/G2/G3) sowie die Kapitel Wärmeerzeugung (Brennstoffe, Verbrennung, Heizwerte, Wärmepreise), Feuerungsanlagen (Feuerstätten, Verbindungsstücke, Hausschornsteine) und den Einstieg in Heizungsanlagen und Jahresbrennstoffbedarf.

## Inhalt

### Raum-Heizlastberechnung — Formblatt R (DIN EN 12831 Beiblatt 1)

#### Raumgeometrie und Eingangsdaten
Die Innentemperatur jedes Raums wird aus dem Vereinbarungs-Formblatt V übernommen. Geometrische Eingangsdaten stammen aus Planunterlagen: Geschosshöhe hG für Transmissionsverluste, Raumhöhe hR = hG minus Deckendicke ergibt das Raumvolumen.

#### Mindestluftwechselzahlen (Tabelle 8.48, DIN EN 12831 Beiblatt 1)

| Raumart | nmin [h⁻¹] |
|---|---|
| Bewohnbarer Raum (Standardfall) | 0,5 |
| Küche < 20 m³ | 1,0 |
| Küche > 20 m³ | 0,5 |
| WC oder Bad mit Fenster | 1,5 |
| Büroraum | 1,0 |
| Besprechungsraum, Schulzimmer | 2,0 |

Innenliegende Bäder und WCs ohne Fenster sind mit Lüftungsanlagen zu berechnen.

#### Höhenkorrekturfaktor εi (Tabelle 8.49)
Formel: εi = max[1; (hi/10)^(4/9)], wobei hi die mittlere Raumhöhe über Erdreichniveau ist.

| Höhe über Erdreich (Raummitte) [m] | εi |
|---|---|
| 0–10 | 1,0 |
| >10–20 | 1,2 |
| >20–30 | 1,5 |
| >30–40 | 1,7 |
| >40–50 | 2,0 |
| >50–60 | 2,1 |
| >60–70 | 2,3 |
| >70–80 | 2,4 |
| >80–90 | 2,6 |
| >90–100 | 2,8 |

Für Wohngebäude mit maximal 4 beheizten Geschossen über Erdreich kann generell εi = 1,0 (Bereich 0–10 m) angesetzt werden.

#### Wirksame Gebäudemasse cwirk (Tabelle 8.50, DIN EN 12831 Beiblatt 1)

| Bauweise | cwirk |
|---|---|
| Leichte Gebäudemasse (abgehängte Decken/aufgeständerte Böden, Leichtbauwände) | 15 Wh/(m³·K) |
| Mittelschwere Gebäudemasse (Betondecken/-böden mit Leichtbauwänden) | 35 Wh/(m³·K) |
| Schwere Gebäudemasse (massiv) | 50 Wh/(m³·K) |

#### Bauteilkennzeichnungen im Formblatt
Himmelsrichtungen in 45°-Schritten im Uhrzeigersinn ab Nord: N, NO, O, SO, S, SW, W, NW; horizontale Bauteile: H.

Bauteilkürzel:
- AF = Außenfenster, AT = Außentür, AW = Außenwand
- DF = Dachfenster, DA = Dach, DE = Decke, FB = Fußboden
- IF = Innenfenster, IT = Innentür, IW = Innenwand

Angrenzungskennzeichen: e = Außenluft, u = unbeheizter Nachbarraum, g = Erdreich, b = beheizter Nachbarraum.

Flächen AW/AF/AT/DF/DA grenzen grundsätzlich an Außenluft — Kennzeichen „e" kann dort entfallen. Innenflächen (z. B. FB über Tordurchfahrt) die an Außenluft grenzen, müssen mit „e" bezeichnet werden.

#### Korrekturfaktoren für Wärmeverlustkoeffizienten

**Korrekturfaktor bu** (unbeheizte Nachbarräume, Tabelle 8.51):

| Unbeheizter Raum | bu |
|---|---|
| Mit einer Außenwand | 0,4 |
| Ohne äußere Türen, mind. zwei Außenwände | 0,5 |
| Mit äußeren Türen, mind. zwei Außenwände (Hallen, Garagen) | 0,6 |
| Mit 3 Außenwänden (externe Treppenhäuser) | 0,8 |
| Innenliegende Treppenräume (geschlossene Bauweise) | 0,4 |
| Keller ohne Fenster/äußere Türen | 0,5 |
| Keller mit Fenster/äußere Türen | 0,8 |
| Dachgeschoss mit hoher Luftwechselrate (Dachziegel, keine luftundurchl. Schicht) | 1,0 |
| Andere nicht gedämmte Dächer | 0,9 |
| Wärmegedämmte Dächer | 0,7 |
| Aufgeständerter Boden (Kriechraum) | 0,8 |

**Korrekturfaktor fg2** (Erdreich): berücksichtigt Differenz zwischen Norm-Außentemperatur θe und Jahresmittel θm,e beim Wärmeverlust ins Erdreich.
fg2 = (θint,i − θm,e) / (θint,i − θe)

**Korrekturfaktor fi,j** (beheizter Nachbarraum mit abweichender Temperatur):
fi,j = (θint,i − θbeheizter Nachbarraum) / (θint,i − θe)

#### Wärmebrückenzuschlag ΔuWB (Tabelle 8.52, DIN EN 12831 Beiblatt 1)

| Wärmebrückenbehandlung | fc (ΔUWB) [W/(m²·K)] |
|---|---|
| Ohne bauseitige Berücksichtigung | 0,10 |
| Ausführung nach DIN 4108 Beiblatt 2 | 0,05 |
| Detaillierter Nachweis nach DIN EN ISO 10211-1 und -2 | berechnet aus Ψ·l / Σ Ak |

Beim detaillierten Nachweis: Ψl = längenbezogener Wärmedurchgangskoeffizient der Wärmebrücke nach DIN EN ISO 10211-2; ll = Länge der Wärmebrücke zwischen innen und außen; Ak = Fläche des jeweiligen Bauteils. Witterungskorrekturfaktor el = 1,00 in Deutschland.

#### Äquivalente U-Werte für erdberührte Bauteile (Tabellen 8.53–8.60)

**Uequiv,bf für Kellerfußboden auf Erdreich (z = 0 m, Tabelle 8.54) — Auszug:**

| B' [m] | keine Dämmung | UBoden = 2,0 | UBoden = 1,0 | UBoden = 0,5 | UBoden = 0,25 [W/(m²·K)] |
|---|---|---|---|---|---|
| 2 | 1,30 | 0,77 | 0,55 | 0,33 | 0,17 |
| 4 | 0,88 | 0,59 | 0,45 | 0,30 | 0,17 |
| 6 | 0,68 | 0,48 | 0,38 | 0,27 | 0,17 |
| 8 | 0,55 | 0,41 | 0,33 | 0,25 | 0,16 |
| 10 | 0,47 | 0,36 | 0,30 | 0,23 | 0,15 |
| 12 | 0,41 | 0,32 | 0,27 | 0,21 | 0,14 |
| 14 | 0,37 | 0,29 | 0,24 | 0,19 | 0,14 |
| 16 | 0,33 | 0,26 | 0,22 | 0,18 | 0,13 |
| 18 | 0,31 | 0,24 | 0,21 | 0,17 | 0,12 |
| 20 | 0,28 | 0,22 | 0,19 | 0,16 | 0,12 |

**Uequiv,bf für Kellerfußboden 1,5 m unter Erdbodenniveau (z = 1,5 m, Tabelle 8.56) — Auszug:**

| B' [m] | keine Dämmung | UBoden = 2,0 | UBoden = 1,0 | UBoden = 0,5 | UBoden = 0,25 [W/(m²·K)] |
|---|---|---|---|---|---|
| 2 | 0,86 | 0,58 | 0,44 | 0,28 | 0,16 |
| 4 | 0,64 | 0,48 | 0,38 | 0,26 | 0,16 |
| 6 | 0,52 | 0,40 | 0,33 | 0,25 | 0,15 |
| 8 | 0,44 | 0,35 | 0,29 | 0,23 | 0,15 |
| 10 | 0,38 | 0,31 | 0,26 | 0,21 | 0,14 |
| 12 | 0,34 | 0,28 | 0,24 | 0,19 | 0,14 |
| 14 | 0,30 | 0,25 | 0,22 | 0,18 | 0,13 |
| 16 | 0,28 | 0,23 | 0,20 | 0,17 | 0,12 |
| 18 | 0,25 | 0,22 | 0,19 | 0,16 | 0,12 |
| 20 | 0,24 | 0,20 | 0,18 | 0,15 | 0,11 |

**Uequiv,bf für Kellerfußboden 3,0 m unter Erdbodenniveau (z = 3,0 m, Tabelle 8.58) — Auszug:**

| B' [m] | keine Dämmung | UBoden = 2,0 | UBoden = 1,0 | UBoden = 0,5 | UBoden = 0,25 [W/(m²·K)] |
|---|---|---|---|---|---|
| 2 | 0,63 | 0,46 | 0,35 | 0,24 | 0,14 |
| 4 | 0,51 | 0,40 | 0,33 | 0,24 | 0,14 |
| 6 | 0,43 | 0,35 | 0,29 | 0,22 | 0,14 |
| 8 | 0,37 | 0,31 | 0,26 | 0,21 | 0,14 |
| 10 | 0,32 | 0,27 | 0,24 | 0,19 | 0,13 |
| 12 | 0,29 | 0,25 | 0,22 | 0,18 | 0,13 |
| 14 | 0,26 | 0,23 | 0,20 | 0,17 | 0,12 |
| 16 | 0,24 | 0,21 | 0,19 | 0,16 | 0,12 |
| 18 | 0,22 | 0,20 | 0,18 | 0,15 | 0,11 |
| 20 | 0,21 | 0,18 | 0,16 | 0,14 | 0,11 |

**Uequiv,bw für Kellerwandelemente (Tabelle 8.60) — Wand-U-Wert je Versenktiefe z:**

| Uwand [W/(m²·K)] | z = 0 m | z = 1 m | z = 2 m | z = 3 m |
|---|---|---|---|---|
| 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 0,50 | 0,44 | 0,39 | 0,35 | 0,32 |
| 0,75 | 0,63 | 0,54 | 0,48 | 0,43 |
| 1,00 | 0,81 | 0,68 | 0,59 | 0,53 |
| 1,25 | 0,98 | 0,81 | 0,69 | 0,61 |
| 1,50 | 1,14 | 0,92 | 0,78 | 0,68 |
| 1,75 | 1,28 | 1,02 | 0,85 | 0,74 |
| 2,00 | 1,42 | 1,11 | 0,92 | 0,79 |
| 2,25 | 1,55 | 1,19 | 0,98 | 0,84 |
| 2,50 | 1,67 | 1,27 | 1,04 | 0,88 |
| 2,75 | 1,78 | 1,34 | 1,09 | 0,92 |
| 3,00 | 1,89 | 1,41 | 1,13 | 0,96 |

#### Wärmeverlustkoeffizienten HT je Bauteil-Angrenzung
- Bauteil an Außenluft: HT = ANetto × (e × bu) × Uc
- Bauteil an beheizten Nachbarraum: HT = ANetto × fi,j × U
- Bauteil an Erdreich: HT = ANetto × fg1 × fg2 × GW × Uequiv

fg1 = jährliche Schwankungskorrektur (in Deutschland 1,45); GW = Grundwassereinfluss-Korrekturfaktor (aus Formblatt G 1).

Transmissionswärmeverlust je Bauteil: ΦT = HT × (θint − θe)

#### Lüftungswärmeverlust

Norm-Lüftungswärmeverlust: ΦV,i = HV,i × (θint,i − θe)

Lüftungswärmeverlust-Koeffizient: HV,i = Vi × 0,34 (Wert 0,34 enthält ρ·cp der Luft)

**Natürliche Belüftung:**
- Mindest-Luftvolumenstrom: Vmin = nmin × VR
- Infiltrierender Luftvolumenstrom: Vinf,i = 2 × VR × n50 × ei × εi
  - Faktor 2: worst-case-Annahme (Infiltration nur an einer Gebäudeseite)
- Maßgeblich ist der größere Wert: Vi = max(Vinf,i; Vmin)

**Mechanische Belüftung — Zuluftanlage:**
- Korrekturfaktor: fV,su = (θint − θsu) / (θint − θe)
- Thermischer Beitrag: Vsu × fV,su

**Mechanische Belüftung — Abluftüberschuss:**
- Überschuss: Vmech,inf = Vex − Vsu (Zuluft Vsu = 0 bei Wohngebäuden)
- Raumweise Aufteilung: Vmech,inf,i = Vmech,inf × Vi / ΣVi
- Korrekturfaktor fV,mech,inf = 1,0 (Außenluft ersetzt Abluftüberschuss direkt)

**Thermisch wirksamer Luftvolumenstrom:**
Vtherm = Vinf + Vsu × fV,su + Vmech,inf × fV,mech,inf

Bedingung: Vtherm = max(Vtherm; Vmin) — hygienischer Mindestluftwechsel ist Untergrenze.

Lüftungswärmeverlust-Koeffizient: HV = 0,34 × Vtherm

#### Heizlasten — Zusammenfassung

- Netto-Heizlast: ΦHL,Netto = ΦT + ΦV
- Zusatz-Aufheizlast bei Heizunterbrechung: ΦRH = AR × fRH
- Normheizlast: ΦHL = ΦHL,Netto + ΦRH (ohne Heizunterbrechung ΦHL = ΦHL,Netto)

### Berechnungsbeispiel Einfamilienreihenhaus Stuttgart (Tabellen 8.61–8.63)

**Gebäudedaten (Formblatt G 1):**
- Gebäudetyp: Einfamilienhaus, moderate Abschirmung, mittelschwere Masse
- cwirk = 35 Wh/(m³·K)
- Norm-Außentemperatur: θe = −12 °C; Jahresmittel: θm,e = +11 °C
- Geometrie: 8,12 m × 9,25 m, Grundfläche 75,11 m², 3 Geschosse, Höhe 9,85 m
- Erdreich: z = 2,60 m; Grundwasser 4,50 m; Umfang P = 16,24 m; B' = 9,25 m; fge = 1,45; GW = 1,15
- Luftdichtheit: n50 = 6 h⁻¹; gleichzeitig wirksamer Lüftungsanteil ξv = 0,5

**Vereinbarungen (Formblatt V) — Innentemperaturen je Raum:**

| Geschoss | Raum | Innentemperatur [°C] | Luftwechsel [h⁻¹] | Wiederaufheizzeit [h] |
|---|---|---|---|---|
| KG | Flur | 15 | 0,5 | — |
| KG | Abstellraum | 10 | 0,5 | — |
| KG | Heizung | 10 | 0,5 | — |
| KG | Hobbyraum | 20 | 0,5 | 4,0 |
| KG | Vorräte | 10 | 0,5 | — |
| EG | Wohnzimmer | 20 | 0,5 | 2,0 |
| EG | Flur | 15 | 0,5 | — |
| EG | Küche | 20 | 1,0 | 2,0 |
| EG | WC | 20 | 1,5 | 2,0 |
| EG | Garderobe | 15 | 0,5 | — |
| EG | Windfang | 15 | 0,5 | — |
| OG | Schlafzimmer | 20 | 0,5 | 2,0 |
| OG | Kinderzimmer (2×) | 20 | 0,5 | 2,0 |
| OG | Flur | 15 | 0,5 | — |
| OG | Bad | 24 | 0,5 | 2,0 |
| OG | Abstellraum | 15 | 0,5 | — |

**Raum-Heizlast Küche EG (Formblatt R 8, Tabelle 8.63):**
- Abmessungen: 4,26 m × 2,51 m; AR = 10,69 m²; hR = 2,56 m; VR = 27,37 m³
- θint = 20 °C; nmin = 1,0 h⁻¹; n50 = 6 h⁻¹ (aus G1); e = 0,03; ε = 1,0
- Höhe über Erdreich = 1,48 m; fRH = 9,3 W/m²
- Bauteile: NW-Außenfenster (U = 1,40 + 0,05 → Uc = 1,45), NW-Außenwand (U = 0,34 + 0,05 → Uc = 0,39), Innentür an Flur 15°C (U = 2,00), Innenwand an Flur (U = 1,88), Fußboden über Keller 10°C (U = 0,66)
- HT gesamt = 5,47 W/K; ΦT = 245 W
- Vmin = 27,37 m³/h; Vinf = 1,64 m³/h → Vtherm = 27,37 m³/h
- HV = 9,31 W/K; ΦV = 298 W
- ΦHL,Netto = 543 W (27,9 W/m²; 10,9 W/m³)
- ΦRH = 99 W; ΦHL = 642 W

### Formblätter G 2 und G 3 — Gebäudezusammenstellung

**Formblatt G 2 (Raumliste):** Zusammenführung aller Raum-Heizlasten mit den Komponenten ΦT,e / ΦT / ΦV,min / ΦV,inf / ΦV,su / ΦV,m,inf / ΦHL,Netto / ΦRH / ΦHL je Raum.

**Formblatt G 3 (Gebäudezusammenstellung):**
- Gesamte Wärmeverlust-Koeffizienten: ΣHT,e; ΣHV; HGeb
- Gesamte Wärmeverluste: ΦT,Geb; ΦV,min,Geb; ΦV,inf,Geb = ξ × ΣΦV,inf; ΦV,su,Geb = (1 − ηV) × ΣΦV,su; ΦV,mech,inf,Geb
- Gebäudeheizlast: Netto-Heizlast ΦN,Geb + Zusatz-Heizleistung ΦRH,Geb = Norm-Gebäudeheizlast ΦHL,Geb
- Spezifische Werte: ΦHL,Geb/AN,Geb [W/m²]; ΦHL,Geb/VN,Geb [W/m³]; Spez. Transmissionswärmeverlust HT' [W/(m²·K)]

---

### Kapitel 8.4 — Wärmeerzeugung

#### 8.4.1 Brennstoffe

**Feste Brennstoffe:**
- Braunkohle: hauptsächlich als Briketts für Einzelöfen
- Steinkohle: Flamm-/Fettkohlen → Gas + Koks; Ess-/Magerkohle + Anthrazit → Ofenheizung
- Koks: rauch- und rußfreie Verbrennung; gleichmäßig regelbarer Abbrand; optimal für Dauerbrennkessel mit Thermostatregelung; zerfällt im Feuer nicht
- Holz (inkl. Pellets/Briketts): nachwachsend; für Kamin, Kaminofen, Kachelöfen und Zentralheizungskessel zunehmend verbreitet

**Flüssige Brennstoffe** (hauptsächlich Kohlenwasserstoffgemische):
- Heizöl EL (extra leichtflüssig): keine Vorwärmung nötig; für Ölöfen sowie klein-/mittelgroße Heizungen; Schwefelgehalt ca. 0,5 %
- Heizöl L (leichtflüssig): Vorwärmung kann nötig sein
- Heizöl S (schwerflüssig): muss für Transport und Verbrennung vorgewärmt werden; für Großheizanlagen ≥ 1200 kW und Industriefeuerungen; Schwefelgehalt ca. 2,8 %
- Heizöl verbrennt nicht flüssig — muss durch Verdampfen (Ölöfen) oder Zerstäuben (Kessel) aufbereitet werden
- Taupunkt der Heizölabgase: 120–160 °C (erhöht durch Schwefelgehalt; Koksfeuerstätte nur ca. 50 °C) — Taupunktunterschreitung vermeiden (Tieftemperaturkorrosion)

**Gasförmige Brennstoffe** (nach DIN 1340):
- 1. Gasfamilie (Kurzzeichen S): Stadtgas, Ferngase — hoher H₂-Anteil, giftig (CO-Gehalt), wesentlich leichter als Luft
- 2. Gasfamilie (N): Erdgase, synthetische Erdgase — hauptsächlich Methan CH₄; leichter als Luft; schwerer als Stadtgas
- 3. Gasfamilie (F): Flüssiggase nach DIN 51622 — Nebenprodukt Erdölraffination; zu 95 % Propan/Butan oder Mischung; wesentlich schwerer als Luft; unter Druck verflüssigt
- 4. Gasfamilie: Kohlenwasserstoff-Luft-Gemische aus Flüssiggas oder Erdgas + Luft
- DVGW-Arbeitsblatt G 260 normiert die Gasfamilien

**Sonstige Energiequellen:**
- Elektrischer Strom: kein Brennstoff, reine Energieumwandlung ohne Verbrennungsrückstände
- Sonnenenergie: Strahlungsleistung an Erdoberfläche max. 1000 W/m² (Gebirge), 900 W/m² (Land), 800 W/m² (Großstadt); stark schwankend; Deutschland ca. 1300–1900 h/Jahr Sonnenschein (Südeuropa/Nordafrika ca. 4000 h/Jahr)
- Umweltenergie: Wärme aus Außenluft, Erdboden oder Grundwasser (8–12 °C, konstant); ca. 75 % kostenlose Umweltenergie, ca. 25 % Antriebsenergie nötig
- Kernenergie: nur in Kraftwerken nutzbar; Kernfusion als künftige Option

#### 8.4.2 Verbrennung

Verbrennung ist eine chemische Reaktion (Oxidation) brennbarer Bestandteile mit Luftsauerstoff, die ab einer Mindesttemperatur unter Flammenbildung und starker Wärmeentwicklung abläuft.

**Verbrennungsablauf fester Brennstoffe:**
1. Verdampfung des Wassers im Brennstoff
2. Ab ca. 250 °C: Abspaltung flüchtiger Bestandteile (schwere Kohlenwasserstoffe)
3. Verbrennung im gasförmigen Zustand
4. Ab > 1100 °C: Sublimation des verbleibenden Kohlenstoffs (fest → gasförmig → Verbrennung)

Flüssige Brennstoffe müssen verdampfen; Reaktion beginnt im Übergang flüssig/gasförmig.
Gasförmige Brennstoffe reagieren direkt mit Sauerstoff.

**Zündtemperaturen (Tabelle 8.66):**

| Brennstoff | Zündtemperatur [°C] |
|---|---|
| Streichholz | 170 |
| Rohbraunkohle | 200–240 |
| Holz | 200–300 |
| Torf, trocken | 225 |
| Fettkohle | ca. 250 |
| Holzkohle | 300–425 |
| Anthrazit | ca. 485 |
| Koks | 550–600 |
| Heizöl S | ca. 340 |
| Heizöl EL | 230–245 |
| Butan | 430 |
| Propan | ca. 500 |
| Stadtgas | ca. 450 |
| Erdgas | ca. 650 |

**Vollkommene Verbrennung:** Alle brennbaren Anteile C, H₂, S werden zu CO₂, H₂O und SO₂ oxidiert. In der Praxis nicht vollständig erreichbar (außer bei Elektro-Energieumwandlung).

**Unvollkommene Verbrennung:** Entsteht durch Sauerstoffmangel, schlechte Gasdurchmischung oder zu niedrige Feuerraumtemperaturen. Erzeugt giftiges CO statt CO₂. Energieverlust: 1 kg C → CO: ca. 2,8 kWh; 1 kg C → CO₂: ca. 9,4 kWh.

**Luftüberschuss n:**
n = tatsächliche Luftmenge / theoretischer Luftbedarf = max CO₂ / CO₂ gemessen (> 1)

- Anthrazit/Koks: n = 1,4; CO₂-Gehalt 14–15 %
- Heizöl: n = 1,05–1,4; CO₂-Gehalt 12–14 %
- Brenngase Gebläsebrenner: n = 1,05–1,35; CO₂-Gehalt 10–12 %
- Atmosphärische Brenner: CO₂-Gehalt 7–10 %

Zu hoher Luftüberschuss senkt Verbrennungstemperatur und erhöht Abwärmeverluste. Zu niedriger Luftüberschuss → unvollkommene Verbrennung → CO + Ruß.

**Feuerungswirkungsgrad ηF (Verhältnis nutzbare/zugeführte Wärme):**
- Offene Kamine: 5–10 %
- Einzelöfen (feste Brennstoffe) und Ölöfen: 70–85 %
- Einzelöfen (Gas): 80–85 %
- Heizkessel: 70–85 %

Verbrennungsverluste entstehen durch: Abgasverluste (unverbrannte Kohlenwasserstoffe), Abwärmeverluste (heiße Abgase durch Schornstein; Abgastemperatur-Richtwerte: ca. 200 °C bei Kohleöfen, < 400 °C bei Ölöfen, < 300 °C bei Kleinkesseln, 180–250 °C bei größeren Kesseln), Nachströmungsverluste (Falschluft), Verluste durch unverbrannte Rückstände fester Brennstoffe.

Gesamtwirkungsgrad = Feuerungswirkungsgrad × Anlage-Regelwirkungsgrad (85–98 %) × Verteilungswirkungsgrad.

#### 8.4.3 Brennstoffheizwert

- Heizwert Hu: Wärmemenge bei vollständiger Verbrennung von 1 kg Brennstoff, Anfangs-/Endtemperatur +25 °C, entstandenes Wasser dampfförmig (nach DIN 5499)
- Heizwert Hu,n: Wärmemenge für 1 Normkubikmeter Gas unter gleichen Bedingungen
- Betriebsheizwert Hu,B: bezieht sich auf 1 m³ Gas im Betriebszustand (Mess-/Verbrauchsstelle); ca. 7 % kleiner als Hu,n

**Heizwerte Hu verschiedener Brennstoffe (Tabelle 8.67, Mittelwerte):**

| Feste Brennstoffe | kWh/kg | Flüssige | kWh/kg (kWh/l) | Gasförmige | kWh/m³ |
|---|---|---|---|---|---|
| Holz, lufttrocken | 4,1 | Heizöl EL | 10,0 kWh/l | Wassergas | 3,0 |
| Braunkohlenbriketts | 5,6 | Heizöl S | 11,2 | Generatorgas | 1,4 |
| Steinkohle (Saar) | 8,0 | Propan | 12,9 | Stadtgas | 5,0 |
| Steinkohle (Westf.) | 8,7 | Butan | 12,7 | Erdgas | 8,8 |
| Anthrazit | 9,1 | | | Methan | 10,0 |
| Koks | 8,0 | | | Propan | 25,9 |
| | | | | Butan | 34,3 |

#### 8.4.4 Wärmepreis

Nutzwärmepreis [EUR/1000 kWh] = P × 3600 / (Hu × η)

Zahlenbeispiel (Wärmepreis 50,00 EUR/1000 kWh bei folgenden Brennstoffpreisen):
- Nachtstrom: Hu = 1 kWh/kWh → 0,10 EUR/kWh
- Stadtgas: Hu,n = 5,0 kWh/m³ → 0,45 EUR/m³
- Braunkohlebriketts: Hu = 5,6 kWh/kg → 0,35 EUR/kg
- Zechenkoks: Hu = 8,0 kWh/kg → 0,45 EUR/kg
- Erdgas: Hu,n = 8,8 kWh/m³ → 0,45 EUR/m³
- Anthrazit: Hu = 9,1 kWh/kg → 0,50 EUR/kg
- Heizöl EL: Hu = 10,0 kWh/l → 0,55 EUR/l
- Heizöl S: Hu = 11,2 kWh/kg → 0,45 EUR/kg
- Propan: Hu = 12,9 kWh/kg → 0,85 EUR/kg

---

### Kapitel 8.5 — Feuerungsanlagen

Eine Feuerungsanlage besteht aus Feuerstätte + Schornstein + Verbindungsstücken.

#### 8.5.1 Feuerstätten

Anforderungen: hohe Brennstoffausnutzung, gute Regelbarkeit, Langlebigkeit, einfache Bedienung, sauberer Betrieb.

Bestandteile:
- **Feuerraum:** ausreichend groß für vollständige Gasverbrennung (besonders bei langflammigen Brennstoffen wichtig)
- **Rost:** trägt feste Brennstoffe; ermöglicht Verbrennungsluftzutritt von unten; Größe/Form je nach Brennstoff; Rüttelroste erleichtern Entaschen
- **Regelvorrichtungen:** wirken nur bei dicht schließenden Feuer- und Aschentüren
- **Feuerzüge:** leiten Heizwärme an Heizflächen; ausreichend zugängliche Reinigungsöffnungen erforderlich; lange Züge erfordern guten Schornsteinzug → für Dachgeschossräume ungeeignet
- **Aschenraum:** für Aschenbehälter

#### 8.5.2 Verbindungsstücke (DIN V 18160-1)

Verbindungsstücke sind Leitungen (Rauchrohre, Abgasrohre), Kanäle (Rauchkanäle, Abgaskanäle) und Fänge (Rauchfänge, Abgasfänge), die Abgase in den Schornstein leiten.

**Abgasrohre** (DIN 1298, hitze- und feuerbeständiger Stahl oder Aluminium):
- Möglichst kurz und ansteigend zum Schornstein führen
- Ohne Wärmeschutz max. 2,5 m; für Ölöfen Einzelheizung max. 1,0 m
- In unbeheizten Nebenräumen: Wärmedämmung auf ganzer Länge
- Steigung mindestens 10 %, besser 30–45 %
- Wanddicken nach DIN 1298 je nach Nenndurchmesser:
  - Stahl bei festen/flüssigen/gasförmigen Brennstoffen mit Gebläse: NW 60–130 mm → 0,6 mm; darüber 0,7–3 mm
  - Stahl bei gasförmigen Brennstoffen ohne Gebläse: NW 60–160 mm → 0,6 mm; darüber 0,8–3 mm
  - Aluminium: 0,7–2 mm
- Reinigungsöffnungen in jedem Kniestück
- Kontrollöffnung gemäß Bundesimmissionsschutzgesetz für messpflichtige Feuerstätten

**Rauchfüchse (Abgaskanäle):**
- In voller Länge gegen Wärmeverluste und Feuchtigkeit schützen
- Querschnitt 10 % größer als zugehöriger Schornsteinquerschnitt
- Reinigungsöffnungen max. alle 2 m

**Mindestabstände Abgasrohre zu Bauteilen/Verkleidungen (Tabelle 8.71):**

| Bauteil/Verkleidung | Ohne Strahlungsschutz | Mit Strahlungsschutz |
|---|---|---|
| Nicht brennbare Baustoffe (ohne Verkleidung oder mit nicht brennbarer Verkleidung) | 40 cm | 20 cm |
| Brennbare/schwer entflammbare Baustoffe, nicht feuerhemmend | 40 cm | 20 cm |
| Brennbare/schwer entflammbare Baustoffe, mind. feuerhemmend | 20 cm | 10 cm |
| Türbekleidungen brennbar/schwer entflammbar, Tapeten | 20 cm | 10 cm |

Strahlungsschutz z. B. = wärmerückstrahlende Metalle mit ≥ 5 cm Abstand vom Bauteil.
Rauchrohre dürfen nicht durch Einbauschränke geführt werden.

**Feuerstättenanschlüsse:**
- Eigener Schornstein bei: Nennwärmeleistung > 20 kW (Gas: > 30 kW); Gebäude > 5 Vollgeschosse; offene Kamine; Feuerstätten mit Gebläsebrenner; raumluftunabhängige Feuerstätten; Aufstellräume mit ständig offener Verbindung zum Freien
- Gemeinsamer Schornstein: bis 3 Feuerstätten für feste/flüssige Brennstoffe mit je ≤ 20 kW, oder bis 3 Gasfeuerstätten mit je ≤ 30 kW; eigene Verbindungsstücke je Feuerstätte; Einführungen nicht auf gleicher Höhe; Abstand unterste/oberste Einführung max. 6,5 m

**Drosselvorrichtungen:** in Abgasstutzen zulässig für feste/flüssige Brennstoffe ohne Gebläse; Öffnungen im oberen/mittleren Teil ≥ 3 % der Querschnittsfläche und ≥ 20 cm².

**Absperrvorrichtungen:** für flüssige/gasförmige Feuerstätten mit Gebläse, gasförmige ohne Gebläse, offene Holz-/Gaskamine.

**Nebenluftvorrichtungen:** an Schornsteinen nur im Aufstellraum der Feuerstätte; mind. 40 cm über Schornsteinsohle.

**Rußabsperrer:** nur bei festen/flüssigen Brennstoffen; nur Handbetätigung.

#### 8.5.3 Hausschornsteine (DIN V 18160-1)

Ausschließliche Funktion: Abgase über Dach ins Freie befördern.

##### 8.5.3.1 Allgemeine Bestimmungen

**Schornsteinhöhen:**
- Eigener Schornstein: wirksame Mindesthöhe (Rost/Brenner bis Mündung) = 4 m
- Gemeinsamer Schornstein: mind. 5 m für feste/flüssige Brennstoffe; mind. 4 m für Gas

**Schornsteinquerschnitt:**
- Kreisförmige oder quadratische Querschnitte bevorzugt (strömungstechnisch günstig, kleinere Abkühlfläche)
- Rechteckige Querschnitte: Seitenverhältnis max. 2:3
- Lichter Mindestquerschnitt: 100 cm²
- Kleinste Seitenlänge: mind. 10 cm (gemauert: mind. 13,5 cm)
- Abgasgeschwindigkeit bei kleinster Wärmeleistung ≥ 0,5 m/s (sonst Durchfeuchtung/Kaltlufteinbrüche)

**Bemessungsformel (Redtenbacher, Überschlag):**
A = 2,6 × Q / (n × √H) [m²]
- Q = Kesselleistung [kW], H = Schornsteinhöhe [m]
- n ≈ 900 (Holz), ≈ 1600 (Koks), ≈ 1800 (Öl oder Gas)

Genaue Berechnung nach DIN EN 13384 (und -2) für Heizkessel ≥ 48 kW.

**Hausschornstein-Tabelle für häusliche Feuerstätten ≤ 48 kW (Tabelle 8.74):**

| Querschnitt (Mauerstein) | Rundquerschnitt | Gesamtnennheizleistung [kW] | Max. kleine Feuerstätten | Max. Heizkessel |
|---|---|---|---|---|
| 10/10 (100 cm²) | ∅10 (ca. 80 cm²) | — | — | — |
| 13,5/13,5 (180 cm²) | ∅13,5 (ca. 140 cm²) | ≤ 18 | ≤ 2 | 1 |
| 13,5/20 (270 cm²) | ∅16,5 (ca. 210 cm²) | 12–30 | 3–4 | 2 |
| 20/20 (400 cm²) | ∅20 (ca. 310 cm²) | 24–48 | 5–8 | 4 |

Für Formstück-Schornsteine (DIN 18150-1) darf Gesamtnennheizleistung um bis zu 25 % erhöht werden. Kleine Feuerstätten = ≤ 9 kW.

Für Regionen mit weicher Bedachung (Stroh/Reet) oder schutzbedürftiger Umgebung: Schornstein mind. 20/20 cm oder ∅ 20 cm + Funkenschutz.

**Schornsteinmündung:**
- Bei geneigten Dächern möglichst am First
- Überragt höchste Dachkante bei Dachneigung > 20° um mind. 40 cm
- Weichdächer (Stroh/Reet): mind. 80 cm über Dachkante
- Flachdächer und Dächer ≤ 20° Neigung: mind. 1 m Abstand von Dachfläche
- Über Brüstungen: mind. 1 m über Brüstungsoberkante
- Dachaufbauten weniger als 1,5-fache Höhe entfernt: mind. 1 m überragen
- Nicht in unmittelbarer Nähe von Fenstern und Balkonen

**Reinigungsöffnungen:**
- Mindestens 20 cm unterhalb des untersten Feuerstättenanschlusses
- Zusätzlich im Dachraum wenn Reinigung von der Mündung nicht möglich
- Bei gezogenen Schornsteinen: in Nähe der Knickstellen
- Mindestmaße: 10 cm breit × 18 cm hoch
- Dicht verschließbar, wärmegedämmt, aus nicht brennbaren Baustoffen, mit Prüfzeichen

**Schornsteinkopf:**
- Abdeckplatte mind. 8 cm dick (Fertig- oder Ortbeton), bündig mit Außenflächen
- Fuge zwischen Kopfmauerwerk und Abdeckplatte: dauerelastisch abdichten
- Längenänderung ca. 2 mm je steigendem Meter Schornsteinhöhe → Dehnfugenbleche vorsehen

**Schornsteinwangen (gemauert):** mind. 11,5 cm; bei > 400 cm² Querschnitt: 24 cm. Freiliegende Wangen in Außenwänden: mind. 24 cm + Dämmung. Keine Schlitze, Dübel, Anker, Mauerhaken in Wangen.

**Schornsteinzungen (innere Wände):** mind. 11,5 cm.

##### 8.5.3.2 Bauarten

**Einschalige Schornsteine:** aus Mauersteinen/Formsteinen; Rauchgastemperatur 190–400 °C erforderlich; in unbeheizten Dachräumen und über Dach: zusätzliche Wärmedämmung.

**Mehrschalige Formstück-Schornsteine (meist dreischalig nach DIN 18 147-1 bis -5):**
- Innenrohre: Leichtbeton, unglasierte/glasierte Schamotte, Edelstahl oder Glas
- Leichtbeton-Innenrohrformstücke (DIN 18 147-3 und 18 150-1): für feste/gasförmige Brennstoffe, Abgastemperatur ≥ 190 °C
- Schamotte-Innenrohre: für moderne Heizungsanlagen ≥ 140 °C Abgastemperatur
- Glasierte Schamotteinnenrohre: bei extremen Abgastemperaturen ab 60 °C; Kondensatschalen nötig
- Wärmedämmung: nicht brennbare Mineralwollplatten oder Dämmstoffschichten nach DIN 18 147-5
- Ummantelung (Außenschale): Mauerwerk oder Leichtbeton-Formsteine

**Versottungsgefahr:** Beschädigung durch Säuren/Basen aus Kondensation von Abgas-Wasserdampf an Schornsteininnenflächen. Kritische Taupunkttemperaturen: Wasserdampf ca. 50 °C, Säuren ca. 100–130 °C je nach Brennstoff. Risikoerhöht bei zu großen Schornsteinquerschnitten und Wechsel von Öl- auf Gasfeuerung.

**Wärmedurchlasswiderstandsgruppen (Tabelle 8.83, DIN V 18160-1):**

| Gruppe | Wärmedurchlasswiderstand [m²·K/W] | Beispiele |
|---|---|---|
| I | ≥ 0,65 | Die meisten mehrschaligen Schornsteinsysteme |
| II | 0,22–0,64 | Isolierte Edelstahlschornsteine ohne Ummauerung |
| III | 0,12–0,21 | Gemauerte und einschalige Formsteinschornsteine |
| IV | < 0,12 | — (rechnerischer Nachweis erforderlich) |

Bezugsgröße: innere Oberfläche, mittlere Temperatur 200 °C. Rechnerischer Nachweis nach DIN EN 13384-1/-2 erforderlich.

##### 8.5.3.3 Einrichtungen für Schornsteinfegerarbeiten (DIN 18160-5)

**Zugangswege (Laufstege/Trittflächen/Einzeltritte):**
- Laufstege: mind. 25 cm breit; max. seitliche Neigung 3°; unterhalb des Firstes
- Abstand Laufstegflächen untereinander: max. 5 cm
- Neigung > 20 °: Trittleisten erforderlich; Laufstege > 30° unzulässig
- Abstand Trittflächen in Dachneigung: max. 75 cm; bei Dachneigung > 45°: max. 50 cm
- Einzeltritte: versetzt in Falllinie, Abstand max. 40 cm

**Leitern/Steigeisen:**
- Anlegeleitern: nur bis 5 m Höhenunterschied (gegen Abrutschen gesichert)
- Steigeisen: nur bis 2 m Höhenunterschied; an Abgasanlagen montiert: unzulässig
- Steigleitern > 5 m: Absturzsicherung; > 10 m: besondere Steigschutzeinrichtungen nach DIN EN 353-1/-2

**Standflächen — 4 Klassen:**
- Klasse A: an der Mündung; max. 1,10 m unterhalb der Mündung; mind. 25 × 40 cm; oder zwei Einzelstandflächen à 13 × 40 cm
- Klasse B: an Reinigungsöffnung ≤ 5 m unterhalb Mündung; Reinigungsöffnungs-UK 40 cm bis 1,40 m über Standfläche; mind. 50 × 50 cm
- Klasse C: nur bei Abgasanlagen ∅ ≤ 20 cm mit ausschließlich Gasfeuerstätten gleicher Nutzungseinheit; max. zweimalige Schrägführung um max. 30°; sonst wie B
- Klasse D: wie B (UK der Reinigungsöffnung 40 cm bis 1,40 m; 50 × 50 cm Fläche)

**Durchsteigöffnungen:**
- Mindestlichtmaß: 60 × 80 cm
- Kleinformatige Dacheindeckungen (Dachsteine, Ziegel, Schiefer, Faserzement) bis 60° Neigung: 42 × 52 cm ausreichend
- Dachgaubenfenster: nutzbar als Durchsteigöffnung wenn mind. 60 cm × 1,20 m

**Absturzsicherungen:**
- Dachneigung ≤ 60°: Geländer einseitig wenn Höhe > 2 m über tragfähiger Fläche
- Dachneigung > 60°: immer Geländer
- Geländer: Holm + Stützen; seitlicher Abstand 15 cm; Höhe 1,10 m
- Verkehrswege < 50 cm Breite unter Dach: Geländer einseitig wenn > 2 m Höhe

**Abstand von Leitungen:** Elektrische Freileitungen, Antennenanlagen, Fernsprechtleitungen und Blitzschutzanlagen dürfen Zugang und Reinigung nicht behindern. Sicherheitsabstände nach DIN VDE 0210 und DIN VDE 0211.

---

### Kapitel 8.6 — Heizungsanlagen

#### 8.6.1 Aufgaben
Zieltemperatur in Aufenthaltsräumen: 20–24 °C in Raummitte, 1,50 m über Fußboden (Tabelle 8.42). Heizungsanlagen ersetzen kontinuierlich die durch Bauteile und Fensterfugen abfließende Wärme.

#### 8.6.2 Wirkungsweisen

**Konvektionsheizung (Luftheizung):**
- Erwärmte Luft steigt auf (spezifisch leichter), verteilt sich an Decke, kühlt ab, sinkt zum Boden zurück
- Luft speichert nur 0,36 Wh/(m³·K); Mauerwerk ca. 430 Wh/(m³·K) → starke Luftumwälzung und höhere Lufttemperatur als Wandtemperatur erforderlich
- Probleme: Temperaturunterschiede zwischen überhitzter oberer Zone und kaltem Boden; Zugbelästigung durch Luftbewegung; träge Aufheizung der Wandoberflächen

**Strahlungsheizung:**
- Wände/Decken/Mobiliar werden durch Strahlung/Leitung aufgeheizt und erwärmen dann die Luft
- Lufttemperatur liegt unter der Strahlungstemperatur der Umgebung
- Vorteile: rasch einsetzende Behaglichkeit trotz langsamem Temperaturanstieg; gleichmäßigere Temperaturverteilung; geringere tatsächliche Wärmeverluste als bei Konvektion; entspricht besser dem Berechnungsverfahren nach DIN EN 12831

**Lufttemperaturprofile (Abbildung 8.86) verschiedener Heizungsarten:**
FH = Fußbodenheizung, DH = Deckenheizung, HA = Radiator an Außenwand unter Fenster, RI = Radiator an Innenwand, K = Kachelofenheizung, E = Eiserner Ofen, S = Schwerkraftluftheizung Auslass Innenwand, P = Perimeter-Luftheizung

---

### Kapitel 8.7 — Jahres-Brennstoffbedarf

#### 8.7.1 Überschlägliche Ermittlung

**Methode 1 — nach Normheizlast:**
Bj = n × ΦHL
- Bj = Jahresbrennstoffbedarf [l, kg, m³ oder kWh]
- ΦHL = Normheizlast [kW]
- n-Faktoren je Brennstoff:
  - Heizöl EL (Hu = 10,0 kWh/l): n = 170–190
  - Koks (Hu = 8,0 kWh/kg): n = 270–320
  - Stadtgas (Hu = 5,0 kWh/m³): n = 310–335
  - Stadtgas bei Etagenheizung: n = 285–310
  - Erdgas (Hu = 8,8 kWh/m³): n = 180–220
  - Elektrischer Strom: n = 1000
- Zuschlag 10 % für Anlagen mit Warmwasserbereitung

**Methode 2 — nach Rauminhalt/Fläche:**

| Brennstoff | Je m³ beheizter Raum | Je m² beheizte Fläche |
|---|---|---|
| Ölfeuerung | 8–12 l/m³ | 20–30 l/m² |
| Koksfeuerung | 12–18 kg/m³ | 30–45 kg/m² |
| Stadtgas (Hu = 5,0 kWh/m³) | 13–22 m³/m³ | 33–55 m³/m² |
| Erdgas (Hu = 8,8 kWh/m³) | 9–13 m³/m³ | 23–33 m³/m² |

Untere Werte gelten für: Warmwasser-Zentralheizung, neue Kessel, Nachtabsenkung, gute automatische Regelung, Wärmeschutz nach DIN 4108-1/-2, Stadtlage.

#### 8.7.2 Ermittlung mit Jahresbenutzungsstunden

Formel: Bj = ΦHL × hj / (Hu × η)

- hj = Jahresbenutzungsstunden [h/Jahr]
- n aus Abschnitt 8.7.1 entspricht hj / (Hu × η)

**Jahresnutzungsgrade ηa von Kesselanlagen ab Baujahr 1980 (Tabelle 8.87):**

| Kesselleistung [kW] | Feste Brennstoffe | Öl ohne Gebläse | Öl mit Gebläse | Gas |
|---|---|---|---|---|
| bis 50 | 74–78 % | 81–83 % | 82–89 % | 83–92 % |
| 50–120 | 78–81 % | 84–86 % | 85–91 % | 86–94 % |
| 120–350 | 84 % | 86 % | 91 % | 89–95 % |
| 350–1200 | 85 % | 86 % | 91 % | 89–95 % |

Ältere Kessel: 5–15 % schlechtere Nutzungsgrade. Brennwertkessel (Gas): 4–8 % bessere Nutzungsgrade.

Verteilungswirkungsgrad ηV je nach Wärmedämmung und Verlegung: 90–98 %.

**Jahresbenutzungsstunden für Nachtstrom-Speicherheizung:** hj ≈ 1150–1300 h/Jahr (inkl. Sommerbetrieb Mai–September).

**Jahresbenutzungsstunden hj für Wohnbauten (Tabelle 8.88) bei min ta = −15 °C, GT = 3400 oder min ta = −12 °C, GT = 3100 oder min ta = −18 °C, GT = 3700:**

| Gebäudeart | hj [h/Jahr] |
|---|---|
| Einfamilienhaus, freistehend, 1–1,5-geschossig | 1600 |
| Als Doppelhaus | 1520 |
| Als Reihenhaus | 1470 |
| Reihenhaus mit Mietwohnungen, 2–2,5-geschossig | 1630 |
| Reihenhaus mit Mietwohnungen, 3–3,5-geschossig | 1570 |
| Reihenhaus mit Mietwohnungen, 4–4,5-geschossig | 1550 |
| Wohnblock > 18 WE, 3–3,5-geschossig | 1620 |
| Wohnblock > 24 WE, 4–4,5-geschossig | 1570 |
| Wohnhochhaus (im Mittel) | ca. 1580 |

In hj sind ca. 155 Sommerbenutzungsstunden (Mai–September) enthalten.

**Definitionen:**
- GT = Jahres-Gradtagzahl = Anzahl Heiztage × (tim − tam); tim = 19 °C für Wohngebäude; Heizperiode = Tage mit mittlerer Außentemperatur ≤ +12 °C
- min ta = tiefste mittlere Außentemperatur nach DIN EN 12831

**Korrekturfaktoren für andere Klimaverhältnisse (Tabelle 8.89):**

| GT | 2800 | 2900 | 3100 | 3200 | 3300 | 3400 | 3500 | 3600 | 3700 | 3800 | 3900 | 4000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| f | 0,82 | 0,85 | 0,91 | 0,94 | 0,97 | 1,00 | 1,03 | 1,06 | 1,09 | 1,12 | 1,15 | 1,18 |

Bei min ta = −12 °C (statt −15 °C): f = 0,92; bei min ta = −18 °C: f = 1,09.

#### 8.7.3 Ermittlung über spezifischen Wärmebedarf
Jahres-Heizlast ΦHL,j, Jahresbrennstoffbedarf Bj und Jahresbrennostoffkosten lassen sich aus dem spezifischen Wärmebedarf in kW/m² Wohnfläche kombiniert mit Jahresbenutzungsstunden ermitteln (Diagramm/Tabelle 8.90 — Inhalt folgt in nächstem Teil).
