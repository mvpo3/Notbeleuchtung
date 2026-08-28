# Planung von Elektroanlagen — Teil 2
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 81-120.

Dieser Teil behandelt ausschließlich Kapitel 7 (Kurzschluss und Erdschluss im Drehstromnetz), speziell die Abschnitte 7.4 bis 7.6. Themen sind Kurzschlussimpedanzberechnung von Generatoren, Transformatoren, Kabeln und Motoren, Impedanzkorrekturen, Berechnung aller Kurzschlussarten (dreipolig, zweipolig, einpolig, Stoßstrom, Ausschaltstrom, Dauerkurzschlussstrom) sowie umfangreiche Berechnungsbeispiele bis hin zu einem 380-kV-Hochspannungsnetz.

## Inhalt

### 7.4 Kurzschlussimpedanzen der Betriebsmittel

#### 7.4 Synchrongeneratoren — Reaktanzphasen und Impedanzberechnung

Bei einem Kurzschluss am Generator werden drei Zeitphasen unterschieden:

- **Subtransiente Phase:** Tritt unmittelbar nach Kurzschlusseintritt auf, dauert maximal bis 100 ms. Beschrieben durch die subtransiente Reaktanz X''d. Bewirkt sehr hohen Anfangskurzschlussstrom der Wechselstromkomponente, der wegen der kleinen Zeitkonstante schnell abfällt. Berechnung:
  - X''d = x''d · (U²rG / SrG)
- **Transiente Phase:** Kurzschluss dauert an, Ausgleichsvorgänge klingen langsam ab. Zeitbereich zwischen 10 ms und 100 ms. Transiente Reaktanz X'd:
  - X'd = x'd · (U²rG / SrG)
- **Stationäre Phase:** Kurzschlussstrom kann als praktisch konstant angesehen werden, Zeit größer als 10 s. Beschrieben durch Reaktanz Xd (auch: Dauerkurzschlussstrom). Entfernung des Kurzschlussorts zum Generator beeinflusst, wie stark die Phasen ausgeprägt sind:
  - Xd = xd · (U²rG / SrG)

Gesamte Impedanzen des Generators (subtransient, transient, stationär):
- Z''d = √(R²G + X''²d)
- Z'd = √(R²G + X'²d)
- Zd = √(R²G + X²d)

Subtransiente Anfangsspannung (als Sternspannung angegeben, abhängig von Vorbelastung):
- E''q = √[(UrG/√3 · cosφ + RG · IrG)² + (UrG/√3 · sinφ + X''d · IrG)²]

Äquivalent dazu die transiente Spannung E'q (X''d durch X'd ersetzt).

Zugehörige Kurzschlussströme:
- Subtransienter Kurzschlussstrom: I''k = E''q / Z''d
- Transienter Kurzschlussstrom: I'k = E'q / Z'd

Zeitabhängige Wechselstromkomponente des Gesamtkurzschlussstroms:
- iacG(t) = (I''k − I'k) · e^(−t/T''d) + (I'k − Ik) · e^(−t/T'd) + Ik

Gleichstromkomponente:
- idcG(t) = √2 · (I''k − I'rG · sinφ) · e^(−t/Tdc)

Stoßkurzschlussstrom als Überlagerung:
- ip(t) = √2 · iac(t) + idc(t)

#### 7.4.5 Rechenbeispiel Generator (10,5 kV / 20 MVA)

Gegeben: SrG = 20 MVA, UrG = 10,5 kV, x''d = 0,2

- X''Gen = x''d · U²rG / SrG = 0,2 · (10,5 kV)² / 20 MVA = 1,1 Ω
- RG = 0,07 · X''d = 0,0772 Ω
- ZG = √(0,0772² + 1,1²) = 1,1 Ω
- Korrekturfaktor: KG = c / (1 + x''d · sinφrG) = 1,1 / (1 + 0,17 · 0,63) = 0,994
- Korrigierte Generatorimpedanz: ZGK = 0,994 · 1,1 Ω = 1,093 Ω

#### 7.4.6 Rechenbeispiel zweiter Generator (0,4 kV / 600 kVA)

Gegeben: x''d = 12 %, SrG = 600 kVA, UrG = 0,4 kV

- XGen = X''d = (12% / 100%) · (0,4 kV)² / 600 kVA = 0,032 Ω
- RGen = 0,15 · X''d = 0,15 · 0,032 Ω = 0,0048 Ω
- Korrekturfaktor: KG = (Un/UrG) · cmax / (1 + X''d · sinφrG) = 1 · 1 / (1 + 0,12 · 0,6) = 0,93
- ZGK = KG · ZG = 0,93 · (0,048 + j0,032) Ω = (0,0445 + j0,0298) Ω
- |ZGK| = √(0,0445² + 0,0298²) = 0,0536 Ω

Für weiteren Generator (21 kV / 250 MVA, x''d = 17 %):
- ZG = 17% · (21 kV)² / (100% · 250 MVA) = 0,30 Ω
- KG = 1,1 / (1 + 0,17 · 0,63) = 0,994
- ZGK = 0,994 · 0,30 Ω = 0,298 Ω

#### 7.4.7 Transformatoren (Zweiwicklungstransformatoren)

Kurzschlussspannung ist die Primärspannung, bei der der Transformator mit kurzgeschlossener Ausgangswicklung bereits seinen Primärstrom aufnimmt. Sie ist ein Maß für die bei Belastung auftretende Spannungsänderung.

Berechnung der Kurzschlussmitimpedanz:
- ZT = ukr · U²rT / (100% · SrT)
- RT = uRr · U²rT / (100% · SrT) = PkrT / (3 · I²rT)
- XT = √(Z²T − R²T)

Sternpunktbehandlung beeinflusst die Fehlergrößen. Im TN-System (bevorzugt in NS-Netzen) fließt Kurzschlussstrom über Erde oder Neutralleiter.

Kennwerte von Drehstromverteilungstransformatoren: entnehmbar aus DIN EN 50464-1, 42503 und 42511.

Schaltgruppe Yyn ist für TN- und TT-Systeme nicht geeignet (oberspannungsseitiger Sternpunkt nicht geerdet).

**Nullwiderstände von NS-Verteiltransformatoren** (Verhältnis Nullsystem zu Mitsystem):

| Schaltgruppe | R(0)T / RT | X(0)T / XT |
|---|---|---|
| Dyn | 1,0 | 0,95 |
| Dzn, Yzn | 0,4 | 0,1 |
| Yyn | 1,0 | 7 × 100 |

Bezeichnungen:
- UrT: Bemessungsspannung (HV- oder LV-Seite)
- IrT: Bemessungsstrom (HV- oder LV-Seite)
- SrT: Bemessungsscheinleistung
- PkrT: gesamte Wicklungsverluste bei Bemessungsstrom
- ukr: Bemessungswert Kurzschlussspannung in %
- uRr: Bemessungswert ohmscher Spannungsfall in %
- R0T: Nullwirkwiderstand, X0T: induktiver Nullwiderstand, RT: Wirkwiderstand, XT: induktiver Widerstand

#### 7.4.8 Rechenbeispiel Transformator (20-kV-Netz, 630 kVA)

Gegeben: SrT1 = 630 kVA, UrTHV = 20 kV, UrTLV = 420 V, Schaltgruppe Dyn5, ukr = 4%, PkrT1 = 6,4 kW, R(0)T/RT = 1,0, X(0)T/XT = 0,95

- ZT = (4% / 100%) · (420 V)² / 630 kVA = 11,2 mΩ
- RT = PkrT · U²rTLV / S²rT = 6,4 kW · (420 V)² / (630 kVA)² = 2,84 mΩ
- uRr = PkrT / SrTLV · 100% = 1,015%
- uxr = √(u²kr − u²Rr) = 3,869%
- XT = √(Z²T − R²T) = 10,83 mΩ
- Korrekturfaktor: KT = 0,95 · cmax / (1 + 0,6 · xT) = 0,95 · 1,05 / (1 + 0,6 · 0,03869) = 0,974
- Korrigierte Transformatorimpedanz: ZTK = ZT · KT = (2,76 + j10,54) mΩ

#### 7.4.9 Rechenbeispiel aus Diagramm (630 kVA, ukr = 4%)

Aus Abb. 7.12 abgeleitet für 630 kVA:
- RT ≈ 3 mΩ, XT ≈ 10 mΩ

#### 7.4.10 Leitungen und Kabel

Kurzschlussimpedanz im Mitsystem aus Leiterdaten, Tabellen, Querschnitten und Mindestabständen:
- Z = RL + jXL
- Ohmscher Widerstand: RL = R'L · l
- Induktiver Widerstand: XL = X'L · l

Für einpoligen Kurzschlussstrom wird nach DIN EN 60909-0 eine Temperaturerhöhung am Ende der Kurzschlussdauer angenommen. PVC-Leitungen und Kabel bei 80 °C:
- R(80°C) = 1,24 · l / (κ · S)

Nullwiderstände:
- R0L = Tabellenwert RL
- X0L = Tabellenwert XL
- Tabellenwerte entnehmbar aus DIN EN 60909-0 Beiblatt 4; bei Hersteller anfragen wenn nichts anderes vorliegt.

**Widerstandswerte bei 20 °C für Cu- und Al-Kabel (Tab. 7.4), in Ω/km:**

| Querschnitt (mm²) | Cu-r | Cu-x | Cu-z | Al-r | Al-x | Al-z |
|---|---|---|---|---|---|---|
| 4 × 1,5 | 12,1 | 0,114 | 12,1 | — | — | — |
| 4 × 2,5 | 7,28 | 0,110 | 7,28 | — | — | — |
| 4 × 4 | 4,56 | 0,106 | 4,56 | — | — | — |
| 4 × 6 | 3,03 | 0,100 | 3,03 | — | — | — |
| 4 × 10 | 1,83 | 0,095 | 1,832 | — | — | — |
| 4 × 16 | 1,15 | 0,0894 | 1,153 | — | — | — |
| 4 × 25 | 0,727 | 0,0878 | 0,7319 | 1,20 | 0,088 | 1,203 |
| 4 × 35 | 0,524 | 0,0851 | 0,530 | 0,876 | 0,086 | 0,880 |
| 4 × 50 | 0,387 | 0,0848 | 0,396 | 0,641 | 0,084 | 0,646 |
| 4 × 70 | 0,268 | 0,0824 | 0,280 | 0,443 | 0,082 | 0,450 |
| 4 × 95 | 0,193 | 0,082 | 0,209 | 0,320 | 0,082 | 0,330 |
| 4 × 120 | 0,153 | 0,0805 | 0,172 | 0,253 | 0,080 | 0,265 |
| 4 × 150 | 0,124 | 0,0805 | 0,147 | 0,206 | 0,080 | 0,220 |
| 4 × 185 | 0,0991 | 0,0803 | 0,127 | 0,164 | 0,080 | 0,182 |
| 4 × 240 | 0,0754 | 0,0799 | 0,109 | 0,125 | 0,079 | 0,147 |
| 4 × 300 | 0,0601 | 0,0798 | 0,999 | 0,100 | 0,079 | 0,127 |

**Null- und Mitimpedanz NYY 4×1×qn (Tab. 7.5), Mitsystemimpedanz Z(1)N = R'(1)N + jX'(1)N in Ω/km:**

| Querschnitt (mm²) | Z(1)N [Ω/km] | R(0)N/R(1)N | X(0)N/X(1)N |
|---|---|---|---|
| 4×1×10r | 1,830 + j0,143 | 4 | 4 |
| 4×1×16r | 1,150 + j0,133 | 4 | 4 |
| 4×1×25rST | 0,727 + j0,119 | 4 | 4 |
| 4×1×35rST | 0,524 + j0,113 | 4 | 4 |
| 4×1×50rST | 0,387 + j0,110 | 4 | 4 |
| 4×1×70rST | 0,268 + j0,102 | 4 | 4 |
| 4×1×95rST | 0,193 + j0,099 | 4 | 4 |
| 4×1×120rST | 0,153 + j0,097 | 4 | 4 |
| 4×1×150rST | 0,124 + j0,097 | 4 | 4 |
| 4×1×185rST | 0,099 + j0,096 | 4 | 4 |
| 4×1×240rST | 0,075 + j0,094 | 4 | 4 |
| 4×1×300rST | 0,060 + j0,091 | 4 | 4 |

(r = rund, ST = verseilt)

**Widerstandswerte bei 80 °C für Cu- und Al-Kabel (Tab. 7.6), in Ω/km:**

| Querschnitt (mm²) | Cu-r | Cu-x | Cu-z | Al-r | Al-x | Al-z |
|---|---|---|---|---|---|---|
| 4 × 1,5 | 15 | 0,115 | 15 | — | — | — |
| 4 × 2,5 | 9,020 | 0,110 | 9,020 | — | — | — |
| 4 × 4 | 5,654 | 0,106 | 5,654 | — | — | — |
| 4 × 6 | 3,757 | 0,100 | 3,758 | — | — | — |
| 4 × 10 | 2,244 | 0,094 | 2,264 | — | — | — |
| 4 × 16 | 1,413 | 0,090 | 1,415 | — | — | — |
| 4 × 25 | 0,895 | 0,086 | 0,899 | 1,680 | 0,086 | 1,682 |
| 4 × 35 | 0,649 | 0,083 | 0,654 | 1,226 | 0,083 | 1,228 |
| 4 × 50 | 0,479 | 0,083 | 0,486 | 0,794 | 0,083 | 0,798 |
| 4 × 70 | 0,332 | 0,082 | 0,341 | 0,551 | 0,082 | 0,557 |
| 4 × 95 | 0,239 | 0,082 | 0,252 | 0,396 | 0,082 | 0,404 |
| 4 × 120 | 0,192 | 0,080 | 0,208 | 0,316 | 0,080 | 0,325 |
| 4 × 150 | 0,153 | 0,080 | 0,172 | 0,257 | 0,080 | 0,270 |
| 4 × 185 | 0,122 | 0,080 | 0,146 | 0,203 | 0,080 | 0,221 |
| 4 × 240 | 0,093 | 0,079 | 0,122 | 0,155 | 0,079 | 0,173 |
| 4 × 300 | 0,074 | 0,079 | 0,108 | 0,124 | 0,079 | 0,147 |

**Widerstandswerte bei 160 °C für Cu- und Al-Kabel (Tab. 7.7), in Ω/km:**

| Querschnitt (mm²) | Cu-r | Cu-x | Cu-z | Al-r | Al-x | Al-z |
|---|---|---|---|---|---|---|
| 4 × 1,5 | 18,876 | 0,114 | 18,876 | — | — | — |
| 4 × 2,5 | 11,356 | 0,110 | 11,356 | — | — | — |
| 4 × 4 | 7,113 | 0,106 | 7,113 | — | — | — |
| 4 × 6 | 4,726 | 0,100 | 4,727 | — | — | — |
| 4 × 10 | 2,824 | 0,0945 | 2,824 | — | — | — |
| 4 × 16 | 1,778 | 0,0895 | 1,780 | — | — | — |
| 4 × 25 | 1,126 | 0,0879 | 1,129 | 1,872 | 0,088 | 1,873 |
| 4 × 35 | 0,817 | 0,0851 | 0,821 | 1,366 | 0,086 | 1,368 |
| 4 × 50 | 0,603 | 0,0848 | 0,608 | 0,999 | 0,084 | 1,002 |
| 4 × 70 | 0,418 | 0,0819 | 0,426 | 0,691 | 0,082 | 0,695 |
| 4 × 95 | 0,301 | 0,0819 | 0,312 | 0,499 | 0,082 | 0,505 |
| 4 × 120 | 0,241 | 0,0804 | 0,254 | 0,394 | 0,080 | 0,402 |

**Quotienten der Wirk- und induktiven Blindwiderstände im Null- und Mitsystem für NAYY und NYY (Tab. 7.8), f = 50 Hz:**

Rückleitung: a = über vierten Leiter, c = über vierten Leiter und Erde

| Querschnitt (mm²) | Cu R0L/RL (a) | Cu R0L/RL (c) | Al R0L/RL (a) | Al R0L/RL (c) | Cu X0L/XL (a) | Cu X0L/XL (c) | Al X0L/XL (a) | Al X0L/XL (c) |
|---|---|---|---|---|---|---|---|---|
| 4 × 1,5 | 4,0 | 1,03 | — | — | 3,99 | 21,28 | — | — |
| 4 × 2,5 | 4,0 | 1,05 | — | — | 4,01 | 21,62 | — | — |
| 4 × 4 | 4,0 | 1,11 | — | — | 3,98 | 21,36 | — | — |
| 4 × 6 | 4,0 | 1,21 | — | — | 4,03 | 21,62 | — | — |
| 4 × 10 | 4,0 | 1,47 | — | — | 4,02 | 20,22 | — | — |
| 4 × 16 | 4,0 | 1,86 | — | — | 3,98 | 17,09 | — | — |
| 4 × 25 | 4,0 | 1,35 | — | — | 4,13 | 12,97 | — | — |
| 4 × 35 | 4,0 | 2,71 | 4,0 | 2,12 | 3,78 | 10,02 | 4,13 | 15,47 |
| 4 × 50 | 4,0 | 2,95 | 4,0 | 2,48 | 3,76 | 7,61 | 3,76 | 11,99 |
| 4 × 70 | 4,0 | 3,18 | 4,0 | 2,84 | 3,66 | 5,68 | 3,66 | 8,63 |
| 4 × 95 | 4,0 | 3,29 | 4,0 | 3,07 | 3,65 | 4,63 | 3,65 | 6,51 |
| 4 × 120 | 4,0 | 3,35 | 4,0 | 3,19 | 3,65 | 4,21 | 3,65 | 5,53 |
| 4 × 150 | 4,0 | 3,38 | 4,0 | 3,26 | 3,65 | 3,94 | 3,65 | 4,86 |
| 4 × 185 | 4,0 | 3,41 | 4,0 | 3,32 | 3,65 | 3,74 | 3,65 | 4,35 |
| 4 × 240 | 4,0 | 3,42 | — | — | 3,67 | 3,62 | — | — |
| 4 × 300 | 4,0 | 3,44 | — | — | 3,66 | 3,52 | — | — |

**Induktive Blindwiderstandsbeläge x in Ω/km im Mitsystem für Freileitungsseile (Tab. 7.9), f = 50 Hz:**

Mittlerer Leiterabstand d in cm: 50 / 60 / 70 / 80 / 90 / 100

| Querschnitt (mm²) | 50 cm | 60 cm | 70 cm | 80 cm | 90 cm | 100 cm |
|---|---|---|---|---|---|---|
| 10 | 0,37 | 0,38 | 0,40 | 0,40 | 0,41 | 0,42 |
| 16 | 0,36 | 0,37 | 0,38 | 0,38 | 0,40 | 0,40 |
| 25 | 0,34 | 0,35 | 0,37 | 0,37 | 0,38 | 0,39 |
| 35 | 0,33 | 0,33 | 0,35 | 0,36 | 0,37 | 0,38 |
| 50 | 0,32 | 0,32 | 0,34 | 0,35 | 0,36 | 0,37 |
| 70 | 0,31 | 0,32 | 0,33 | 0,34 | 0,35 | 0,35 |
| 95 | 0,29 | 0,31 | 0,32 | 0,33 | 0,34 | 0,34 |
| 120 | 0,29 | 0,30 | 0,31 | 0,32 | 0,33 | 0,34 |

**Quotienten für N(A)YCWY-Kabel (Tab. 7.10), f = 50 Hz:**

Rückleitung: a = über Schirm, c = über Schirm und Erde

| Querschnitt (mm²) | Cu R0L/RL (a) | Cu R0L/RL (c) | Al R0L/RL (a) | Al R0L/RL (c) | Cu X0L/XL (a) | Cu X0L/XL (c) | Al X0L/XL (a) | Al X0L/XL (c) |
|---|---|---|---|---|---|---|---|---|
| 3×25/16 | 5,74 | 2,40 | — | — | 1,73 | 18,80 | — | — |
| 3×35/16 | 7,51 | 2,92 | 4,90 | 2,14 | 1,66 | 20,45 | 1,63 | 19,86 |
| 3×50/25 | 6,58 | 3,74 | 4,37 | 2,66 | 1,56 | 14,66 | 1,58 | 14,57 |
| 3×70/35 | 6,86 | 4,69 | 4,55 | 3,25 | 1,65 | 11,20 | 1,46 | 11 |
| 3×95/50 | 6,97 | 5,45 | 4,63 | 3,71 | 1,65 | 7,96 | 1,47 | 7,78 |
| 3×120/70 | 6,21 | 5,42 | 4,18 | 3,70 | 1,65 | 5,28 | 1,42 | 5,03 |
| 3×150/70 | 7,35 | 6,39 | 4,88 | 4,29 | 1,58 | 5,24 | 1,43 | 5,07 |
| 3×185/95 | 6,74 | 6,21 | 4,52 | 4,20 | 1,49 | 3,57 | 1,36 | 3,43 |
| 3×240/120 | 6,81 | 6,44 | — | — | 1,44 | 2,83 | — | — |
| 3×300/150 | 6,77 | 6,50 | — | — | 1,39 | 2,33 | — | — |
| 3×35/35 | 4,0 | 2,92 | 2,80 | 2,15 | 1,75 | 10,90 | 1,59 | 10,52 |
| 3×50/50 | 4,0 | 3,26 | 2,81 | 2,37 | 1,71 | 7,74 | 1,42 | 7,40 |
| 3×70/70 | 4,0 | 3,56 | 2,82 | 2,56 | 1,70 | 5,22 | 1,51 | 5,01 |
| 3×95/95 | 4,0 | 3,73 | 2,83 | 2,67 | 1,76 | 3,77 | 1,51 | 3,53 |
| 3×120/120 | 4,0 | 3,81 | 2,84 | 2,72 | 1,68 | 3,06 | 1,44 | 2,81 |
| 3×150/150 | 4,0 | 3,87 | 2,81 | 2,73 | 1,60 | 2,51 | 1,43 | 2,35 |
| 3×185/185 | 4,0 | 3,90 | 2,87 | 2,81 | 1,68 | 2,33 | 1,36 | 2,00 |

**Wirkwiderstandsbeläge r im Mitsystem für DIN-48201-Freileitungsseile (Tab. 7.11), f = 50 Hz, 20 °C, in Ω/km:**

| Nennquerschnitt (mm²) | Sollquerschnitt Cu (mm²) | Cu-r (Ω/km) | Al-r (Ω/km) |
|---|---|---|---|
| 10 | 10 | 1,804 | 2,855 |
| 16 | 15,9 | 1,134 | 1,795 |
| 25 | 24,2 | 0,745 | 1,18 |
| 35 | 34,4 | 0,524 | 0,83 |
| 50 | 49,5 | 0,364 | 0,577 |
| 70 | 65,8 | 0,276 | 0,436 |
| 95 | 93,2 | 0,195 | 0,308 |
| 120 | 117 | 0,155 | 0,246 |

VPE-Kabel (N2XSY, N(A)2XS2Y): Wechselstromwiderstand R' und induktive Betriebsreaktanz X' im Mitsystem bei f = 50 Hz (Dreieckverlegung) sowie Kapazität C' im Mitsystem — Werte aus Herstellerdiagrammen, Kabeltypen N2XSY und N(A)2XS2Y.

#### 7.4.11 Rechenbeispiel Kabel

Gegeben: l1 = 55 m, S = 2×4×185 mm² Cu, Z'L = (0,101 + j0,080) Ω/km, R(0)L/RL = 4, X(0)L/XL = 3,65

Mitimpedanzen:
- ZL = 0,5 · (0,101 + j0,080) Ω/km · 0,055 km = (2,77 + j2,2) mΩ

Nullimpedanzen:
- R(0)L = 4,0 · RL = 4,0 · 2,77 = 11,08 mΩ
- X(0)L = 3,61 · XL = 3,61 · 2,2 = 7,492 mΩ
- Z(0)L = (11,08 + j7,492) mΩ

#### 7.4.12 Asynchronmotoren

In Industrienetzen werden überwiegend Asynchronmotoren eingesetzt. Bei Kurzschluss liefern sie Beiträge zu:
- Anfangs-Kurzschlusswechselstrom
- Stoßkurzschlussstrom
- Ausschaltwechselstrom
- Bei zweipoligem Fehler auch zum Dauerkurzschlussstrom (abhängig von Einsatz- und Kurzschlussort)

Zwischen Kurzschlussläufer- und Schleifringläufermotoren wird kein Berechnungsunterschied gemacht, da Anlasswiderstände von Schleifringläufern im Betrieb kurzgeschlossen sind.

Motorimpedanz ZM im Mit- und Gegensystem:
- ZM = (1 / (ILR/IrM)) · (UrM / (√3 · IrM)) = (1 / (ILR/IrM)) · (U²rM / SrM)

Anfangs-Kurzschlusswechselstrom des Motors:
- I''kM = c · Un / (√3 · ZM)

Für Niederspannungsmotoren mit Anschlusskabel gilt:
- RM/XM = 0,42 und XM = 0,922 · ZM

Bedingung zur Vernachlässigung von Motoren (ukr = 6%, cosφrM = 0,8, Ian/IrM = 5):
- ΣPrM / ΣSrT ≤ 0,8 · |c · 100 · SrT / S''kQ · 0,3|

**Asynchronmotoren dürfen bei der Kurzschlussberechnung vernachlässigt werden wenn:**
- Motoren in öffentlichen Niederspannungsnetzen
- Motorbeiträge kleiner als 5% des Anfangs-Kurzschlusswechselstromes ohne Motoren
- Motoren durch Verriegelung oder Prozessführung nicht gleichzeitig eingeschaltet
- Motoren speisen über Zweiwicklungstransformatoren auf einen Kurzschluss

Bezeichnungen:
- ILR: Anzugsstrom des Motors
- IrM: Bemessungsstrom des Motors
- UrM: Bemessungsspannung des Motors
- ILR/IrM: Verhältnis Anzugsstrom zu Bemessungsstrom (liegt zwischen 4 und 8)
- ΣPrM: Summe der Bemessungswirkleistungen
- ΣSrT: Summe der Bemessungsscheinleistungen
- S''kQ: Anfangs-Kurzschlusswechselstromleistung
- ZM: Kurzschlussimpedanz des Motors

#### 7.4.13 Rechenbeispiel Motorimpedanz

Gegeben: PrM = 2,3 MW, UrM = 6 kV, cosφrM = 0,86, p/2, Ia/IrM = 5, η = 0,97

- ZM = (η · cosφ / (Ian/IrM)) · (U²rM / PrM) = (1 / (2 · 0,86 · 0,97)) / 5 · (6 kV)² / 2,3 MW = 2,611 Ω
- I''kM = c · Un / (√3 · ZM) = 1,1 · 6 kV / (√3 · 2,611 Ω) = 1,46 kA

#### 7.4.14 Impedanzkorrekturen

Bei der Berechnung des dreipoligen Anfangs-Kurzschlusswechselstromes in Netzen mit Generatoren (mit oder ohne Blocktransformatoren) sind Impedanzkorrekturen einmalig durchzuführen. Korrekturfaktor K berücksichtigt eine höhere Spannung als E''.

**1. Korrekturfaktor für Generatoren (direkt ans Netz angeschlossen):**
- ZGK = KG · ZG = KG · (RG + jX''d)
- KG = (Un / UrG) · cmax / (1 + x''d · sinφrG)
- x''d = X''d / ZrG = X''d · SrG / U²rG (bezogene subtransiente Reaktanz)

Bezeichnungen:
- cmax: Spannungsfaktor
- Un: Nennspannung des Netzes
- UrG: Bemessungsspannung des Generators
- SrG: Bemessungsscheinleistung des Generators
- ZGK: korrigierte Impedanz des Generators
- φrG: Phasenwinkel zwischen UrG/√3 und IrG

**2. Korrekturfaktor für Zweiwicklungstransformatoren:**
- ZTK = KT · ZT (Kurzschlussmitimpedanz: ZT = RT + jXT)
- KT = 0,95 · cmax / (1 + 0,6 · xT)
- xT = XT / (U²rT / SrT) (bezogene Reaktanz des Transformators)

Bezeichnungen wie oben, zusätzlich:
- ukr: Bemessungswert Kurzschlussspannung in %
- uRr: Bemessungswert Wirkanteil der Kurzschlussspannung in %

**3. Korrekturfaktor für Kraftwerksblöcke mit Stufenschalter:**
- ZS = KS · (t²r · ZG + ZTHV)
- KS = (U²nQ / U²rG) · (U²rTLV / U²rTHV) · cmax / (1 + |x''d − xT| · sinφrG)

Bezeichnungen:
- ZS: korrigierte Impedanz Kraftwerksblock mit Stufenschalter (HV-Seite bezogen)
- ZG: subtransiente Impedanz des Generators
- pG: Bereich der Generatorspannungsregelung
- tr: Bemessungsübersetzungsverhältnis des Blocktransformators
- xT: bezogene Reaktanz des Blocktransformators bei Hauptanzapfung
- ZTHV: Impedanz des Blocktransformators (HV-Seite)
- UrQ: Netznennspannung am Anschlusspunkt Q des Kraftwerksblocks

**4. Korrekturfaktor für Kraftwerksblöcke ohne Stufenschalter:**
- ZSO = KSO · (t²r · ZG + ZTHV)
- KSO = (UnQ / (UrG · (1 + pG) · UrTLV / UrTHV · (1 ± pT))) · cmax / (1 + x''d · sinφrG)
- ZSO: korrigierte Impedanz ohne Stufenschalter (HV-Seite bezogen)
- (1 ± pT): wird eingeführt, wenn Blocktransformator Anzapfungen hat und dauernd nutzt; sonst 1 ± pT = 1

**Hinweise zu Impedanzkorrekturen:**
- DIN VDE 0100 Teil 410 enthält maximale Abschaltzeiten für Fehlerschutz beim Schutz durch automatisches Abschalten
- DIN EN 60909-0 regelt die Grundmethoden für drei-, zwei- und einpolige Kurzschlussberechnung
- Bei Transformatoren mit ukr = 6% erhöht sich I''k um maximal 9% durch Impedanzkorrektur
- Bei Transformatoren mit ukr = 4% erhöht sich I''k um maximal 7%
- Einfluss der Kurzschlussleistung auf MS-Seite auf diese Erhöhung ist gering
- Erhöhung sollte nach DIN EN 60909-0 bei Bemessung nach maximalen Kurzschlussströmen bei größeren Transformatorleistungen berücksichtigt werden

---

### 7.5 Berechnung der Kurzschlussströme

#### 7.5.1 Dreipoliger Kurzschluss

Im Gegensatz zu einpoligem und zweipoligem Kurzschluss ist der dreipolige Kurzschluss ein symmetrischer Fehler. Er dient zur Beurteilung des Bemessungsausschaltvermögens von Überstromschutzeinrichtungen.

- I''k3 = I''k = c · Un / (√3 · |Z1|) = c · Un / (√3 · √(R²1 + X²1))

Für einfach gespeisten, generatorfernen Kurzschluss im NS-Netz:
- Rk = RQt + RT + RL
- Xk = XQt + XT + XL
- Zk = √(R²k + X²k)

Bezeichnungen:
- Rk: Summe der in Reihe geschalteten Resistanzen
- Xk: Summe der in Reihe geschalteten Reaktanzen
- Zk: Kurzschlussimpedanz
- cmax: Spannungsfaktor

#### 7.5.2 Rechenbeispiel dreipoliger Kurzschluss (20-kV-Netz)

20-kV-Netz mit I''k = 15 kA:
- ZQ = c · Un / (√3 · I''k) = 1,1 · 20 kV / (√3 · 15 kA) = 0,8468 Ω
- ZQt (umgerechnet auf NS) = ZQ · (20 kV / 110 kV)² = 0,339 mΩ
- ZQt = (0,1 + 1) · ZQt / √(0,1² + 1²) = (0,0337 + j0,337) mΩ

Transformator (630 kVA, ukr = 4%, PkrT = 6,5 kW, UrTLV = 0,41 kV):
- ZT = ukr · U²n / (100% · SrT) = 10,673 mΩ
- RT = PkrT · U²rTLV / SrT = 6,5 kW · 0,41²kV / 630 kVA = 2,753 mΩ
- uRr = PkrT / SrT · 100% = 1,032%
- uxr = √(4² − 1,032²) = 3,865%
- XT = √(ZT² − RT²) = 10,312 mΩ
- ZT = (2,753 + j10,312) mΩ
- KT = 0,95 · 1,1 / (1 + 0,6 · 0,03865) = 0,975
- ZKT = (2,684 + j10,054) mΩ

Leitung (2 parallele Adern, 50 m, rL = 0,077 Ω/km, xL = 0,079 Ω/km):
- ZL = (1/n) · l · (rL + jxL) = (1/2) · 50 m · (0,077 + j0,079) Ω/km = (1,925 + j1,975) mΩ

Gesamtimpedanz an der Fehlerstelle:
- Z(1) = Zk = ZQt + ZTK + ZL = (0,0337 + j0,337) + (2,684 + j10,054) + (1,925 + j1,975)
- Z(1) = (4,6427 + j12,366) mΩ = 13,209 mΩ ∠69,42°

Anfangs-Kurzschlusswechselstrom:
- I''k3max = c · Un / (√3 · |Z(1)|) = 1,1 · 400 V / (√3 · 13,209 mΩ) = 19,232 kA ∠−69,42°

#### 7.5.3 Zweipoliger Kurzschluss

Unsymmetrischer Fehler, der bei IT-Netzen und Asynchronmotoren auftreten kann.

- I''k2 = c · Un / |Z(1) + Z(2)|
- Unter Voraussetzung Z(1) = Z(2): I''k2 = c · Un / (2 · |Z(1)|) = (√3/2) · I''k3

Bezeichnungen:
- Z(1): Kurzschlussmitimpedanz
- Z(2): Kurzschlussgegenimpedanz
- c: Spannungsfaktor

#### 7.5.4 Rechenbeispiel zweipoliger Kurzschluss

I''k3 = 19,232 kA (aus vorherigem Beispiel):
- I''k2 = (√3/2) · I''k3 = 13,6 kA

#### 7.5.5 Einpoliger Kurzschluss

Einpoliger Erdkurzschluss ist ein unsymmetrischer Fehler, berechnet mit symmetrischen Komponenten. In der Praxis am häufigsten vorkommende Fehlerart.

Kleinster einpoliger Kurzschlussstrom ist relevant für:
- Ansprechsicherheit (Abschaltung)
- Einstellung der Überstromschutzeinrichtungen (ÜSE)

Rückleiter: Erde sowie ein Außenleiter (PEN) bzw. Schutzleiter (PE). In der Praxis wird vereinfachtes Verfahren (Schleifenimpedanz) angewandt — bis zu 20% fehlerbehaftet. Abschaltung erfolgt innerhalb von 0,2 s / 0,4 s / 5 s (je nach Querschnitt-ÜSE-Abstimmung).

Berechnung:
- I''k1 = √3 · c · Un / |Z(1) + Z(2) + Z(0)| = √3 · c · Un / |2·Z(1) + Z(0)|
- I''k1 = √3 · c · Un / √((2·R(1) + R(0))² + (2·X(1) + X(0))²)

Summen der Widerstände an der Kurzschlussstelle:
- ΣR = 2RQ + 2RT + 2RK + 2RL1 + 2RL2 + R0T + R0K + R0L1 + R0L2
- ΣX = 2XQ + 2XT + 2XK + 2XL1 + 2XL2 + X0T + X0K + X0L1 + X0L2

Bezeichnungen:
- c: Spannungsfaktor
- Z(1): Kurzschlussmitimpedanz
- Z(0): Kurzschlussnullimpedanz
- RQ, XQ: ohmscher und induktiver Widerstand der Netzeinspeisung
- RT, XT: ohmscher und induktiver Widerstand des Transformators
- RK, XK: ohmscher und induktiver Widerstand des Kabels
- RL1, XL1 / RL2, XL2: Widerstände der Leitungen 1 und 2
- R0T, X0T: Nullwiderstände des Transformators
- R0K, X0K: Nullwiderstände des Kabels
- R0L1, X0L1 / R0L2, X0L2: Nullwiderstände der Leitungen

#### 7.5.6 Rechenbeispiel einpoliger Kurzschluss

Mitimpedanzen aus dreipoligem Beispiel übernommen.

Nullsystembestimmung:
- a) 20-kV-Netz bei Dyn5-Transformator: Nur Mit- und Gegensystem des MS-Netzes bei einpoligen Fehlern im NS-Netz zu berücksichtigen.
- b) Transformator Dyn5: RT(0)/RT(1) = 0,95; XT(0)/XT(1) = 1
  - ZT(0) = (RTK + j0,95 · XTK) = (2,684 + j9,951) mΩ
- c) NS-Kabel (gebündelte Verlegung): RL(0)/RL(1) = 4; XL(0)/XL(1) = 4
  - ZL(0) = (4 · RL(1) + j4 · XL(1)) mΩ = (7,7 + j7,9) mΩ

Gesamtnullsystem:
- Z(0) = ZT(0) + ZL(0) = (2,684 + j9,551) + (7,7 + j7,9) = (10,384 + j17,451) mΩ

Berechnung maximaler einpoliger Kurzschlussstrom:
- Z(1) = Z(2) = Zk = (4,6427 + j12,366) mΩ
- Z(0) = (10,384 + j17,451) mΩ
- I''k1 = cmin · √3 · Un / |2·Z(1) + Z(0)| = 0,9 · √3 · 400 V / |(19,669 + j42,183) mΩ|
- |2·Z(1) + Z(0)| = 46,544 mΩ ∠65°
- I''k1 = 13,4 kA ∠−65°

#### 7.5.7 Stoßkurzschlussstrom

Relevant für:
- Dynamische Beanspruchung elektrischer Anlagen
- Einschaltvermögen von Schaltgeräten

Berechnung:
- ip = κ · √2 · I''k; κ = f(Rk/Xk)
- Näherungsgleichung: κ = 1,02 + 0,98 · e^(−3R/X)
- Alternativ: κ aus Diagramm (Abb. 7.26 nach DIN EN 60909-0)

#### 7.5.8 Rechenbeispiel Stoßkurzschlussstrom

I''k3 = 19,232 kA; Z(1) = (4,6427 + j12,366) mΩ → R/X = 0,375 → aus Diagramm: κ = 1,4

- ip = κ · √2 · I''k = 1,4 · √2 · 19,232 kA = 38 kA

#### 7.5.9 Rechenbeispiel: Berechnung aller Kurzschlussarten (NS-Netz)

Netzimpedanzen:
- Z1 = Z2 = (0,0039 + j0,0154) Ω
- Z0 = (0,0038 + j0,0140) Ω

**a) Größte Kurzschlussströme an Fehlerstelle A (cmax = 1,1):**
- |Z1| = 0,0159 Ω
- I''k3 = 1,1 · 0,4 kV / (√3 · 0,0159 Ω) = 14,5 kA
- I''k2 = (√3/2) · I''k3 = 12,65 kA
- I''k1 = (√3 · 1,1 · 0,4 kV) / 0,0463 Ω = 15 kA (x1 + x2 + x0 = 0,0463 Ω)

**b) Kleinste Kurzschlussströme (cmin = 0,9):**
- I''k3 = 1,1 · 0,4 kV / (√3 · 0,0159 Ω) = 6,4 kA
- I''k2 = (√3/2) · I''k3 = 5,5 kA
- I''k1 = (√3 · 0,9 · 0,4 kV) / 0,0463 Ω = 13,46 kA

#### 7.5.10 Ausschaltwechselstrom

Ausschaltwechselstrom ist der Effektivwert der symmetrischen Wechselstromkomponente des erwarteten Kurzschlussstromes im Moment der Kontakttrennung des erstlöschenden Pols einer Überstromschutzeinrichtung.

**1. Für Synchronmaschinen (SM):**
- Ia = μ · I''kG
- Wenn Ia = I''k: μ = 1 (generatorferner Kurzschluss); gilt wenn I''k3/IrG ≥ 2
- Wenn Ia < I''k (generatornaher Kurzschluss): gilt wenn I''k3/IrG ≥ 2
- In der Praxis: Mindestschaltverzug 0,1 s

**2. Für Asynchronmaschinen:**
- Ia = μ · q · I''kM
- μ abhängig von I''k/IrG einzelner Kurzschlussquellen und Mindestschaltverzug tmin
- q abhängig von Motorleistung je Polpaar
- Faktoren μ und q aus Diagrammen nach DIN EN 60909-0

**3. Für Netzeinspeisungen:**
- IaQ = I''kQ
- μ-Faktor aus Diagramm nach DIN EN 60909-0

#### 7.5.11 Dauerkurzschlussstrom

Unterscheidung zwischen maximalem (Ikmax) und minimalem (Ikmin) Dauerkurzschlussstrom. Ikmin gilt für maximale Erregerspannung der SM bei konstanter ungeregelter Leerlaufspannung.

- Ikmax = λmax · IrG
- Ikmin = λmin · IrG

Faktor λ hängt ab von I''kG/IrG, der Erregung und dem Typ der Synchronmaschine (Turbogenerator oder Schenkelpolgenerator). Grenzwerte λmax und λmin aus Diagramm (Abb. 7.30 nach DIN EN 60909-0):
- Obere Kurven: für Turbogeneratoren gültig
- Untere Kurven: für Schenkelpolgeneratoren gültig

#### 7.5.12 Mehrfach einseitig gespeiste Kurzschlüsse

Verfahren der Ersatzstromquelle an der Fehlerstelle anzuwenden. Anfangs-Kurzschlusswechselstrom I''k ist die Summe der Teilkurzschlussströme an der Fehlerstelle.

- I''k = I''kT + I''kS + I''kM
- ip = ipT + ipS + ipM
- Ib = IbT + IbS + IbM
- Ik = IkS + IkT

#### 7.5.13 Thermische und dynamische Kurzschlussfestigkeit

Elektrische Betriebsmittel (Sammelschienen, ÜSE, Kabel und Leitungen) werden im Kurzschlussfall thermisch und mechanisch stark beansprucht.

Für Kurzschlussdauer TK ergibt sich der thermisch gleichwertige Kurzschlussstrom Ith:
- Joule-Integral: ∫i²dt = I''²k · (m + n) · Tk = I²th · Tk
- Ith = I''k · √(m + n)
- m: Faktor für Wärmeeffekt des Gleichstromgliedes bei Drehstrom und Einphasenwechselstrom
- n: Faktor für Wärmeeffekt des Wechselstromgliedes bei dreipoligem Kurzschluss
- Faktoren m und n aus Diagramm (Abb. 7.32 nach DIN EN 60909-0)

Dynamische Beanspruchung durch Kurzschlussströme erzeugt Kräfte, die Anlagen zerstören und Betriebspersonal gefährden können.

Größtmögliche Kraft zwischen Hauptleitern (Leiterlänge l, Leiterabstand a):
- F = 0,2 · i²p · (l/a)

Bezeichnungen:
- m: Wärmewirkung des Gleichstromgliedes
- n: Wärmewirkung des Wechselstromgliedes
- F: Stromkraft zwischen den Leitern
- ip: Stoßkurzschlussstrom
- Ith: Kurzzeitstrom
- I''k: Anfangs-Kurzschlussstrom
- l: Leiterlänge, a: Leiterabstand

#### 7.5.14 Berechnung der Mehrfachfehler

Kurzschlussschutz des Verteilertransformators auf Primärseite üblicherweise als Kombination aus HH-Sicherungen und Lasttrennschalter oder Leistungsschalter mit Schutzrelais. Auf Sekundärseite: NH-Sicherungen oder Leistungsschalter.

Bei Auswahl der ÜSE muss Selektivität zwischen primär- und sekundärseitiger ÜSE gewährleistet sein.

Kleinste Kurzschlussströme (I''kL1, I''kL2, I''kL3, I''kN) auf NS-Seite und Teilkurzschlussströme (I''kL2HV, I''kL3HV) auf HS-Seite bei Leiterunterbrechung auf HV-Seite nach DIN EN 60909-0:

- I''kv = α · c · Un / (√3 · |ZQt + KT·ZT + ZL + β·(KT·Z(0)T + Z(0)L)|)

**Faktoren α und β zur Berechnung der Kurzschlussströme (Tab. 7.12):**

| Kurzschluss an Fehlerstelle | Dreipolig L1,L2,L3 | Zweipolig mit Erde L1,L3,N(E) | Zweipolig mit Erde L1,L2,N(E) | Einpolig L2,N(E) |
|---|---|---|---|---|
| Betroffene Leiter NS | L1,L2,L3 (N) | L2,L3,N(E) | — | L1,L2,L3,N(E) |
| Faktor β | 0 | 2 | 0,5 | 0,5 |
| α für I''kL1 (LV) | 0,5 | 0,5 | — | — |
| α für I''kL2 (LV) | 1,0 | — | 1,5 | 1,5 |
| α für I''kL3 (LV) | 0,5 | 1,5 | — | — |
| α für I''kN (LV) | — | 3,0 | 1,5 | 1,5 |
| α für I''kL2HV | 1/tr | — | — | — |
| α für I''kL3HV | √3/2 · (1/tr) | — | — | — |

Bezeichnungen:
- v: für L1,L2,L3,N(E) auf NS-Seite und L2HV, L3HV auf HV-Seite
- ZQt + KT·ZT + ZL: resultierende Impedanz im Mitsystem auf NS-Seite
- KT·Z(0)T + Z(0)L: resultierende Impedanz im Nullsystem auf NS-Seite
- α, β: Faktoren nach Tab. 7.12

---

### 7.6 Beispiele zur Kurzschlussberechnung

#### 7.6.1 Kurzschlussfestigkeit eines Kabels

Aufgabe: NYCWY-Einspeisekabel mit maximalem Querschnitt 3×240/120 mm² Cu für NS-Schaltanlage mit Ir = 1200 A dimensionieren. Umgebungstemperatur 40 °C, Verlegung auf Kabelpritsche. Transformator 20/0,4 kV, SrT = 1600 kVA, ukr = 6%.

**Thermische Belastbarkeit:**
- Anzahl parallele Kabel: z = Ir / (Iz · f) = 1200 A / (258 A · 0,95) = 4,9 → 5 parallele Kabel erforderlich

**Thermische Kurzschlussfestigkeit:**
- I''k = c · 100 · SrT / (√3 · ukr · UrT) = 1,1 · 100 · 1600 kVA / (√3 · 6 · 400 V) = 42,4 kA
- Nach DIN VDE 0103 Abb. 10: m = 0,45 mit κ = 1,8, Kurzschlussdauer tk = 100 ms
- Ith = I''k · √(m + n) = 42,4 kA · √(0,45 + 1) = 51 kA
- Thermische Stromdichte: Sth = Sthr · (1/√(tkr/tk)) = 115 A/mm² · (1/√(1s / 0,1s)) = 364 A/mm²
- Mindestquerschnitt: Smin = Ith / Sth = 46360 A / 364 A/mm² = 140 mm²

Ergebnis: gewählter Querschnitt 240 mm² ist ausreichend.

#### 7.6.2 Ermittlung der Kurzschlussströme in einem 380-kV-Hochspannungsnetz

**Leitungsdaten (Tab. 7.13):**
- Spannung: 380 kV
- Leitertyp: Al/St 2×550/70 mm²
- Leiterdurchmesser d = 32,4 mm
- Mittlerer Leiterabstand D = 10 m
- Einzelleiterradius r = 16,2 mm

**Äquivalenter Bündelleiterradius:**
- rb = √(n_p · r · R_n−1) = √(2² · 16,2 · 20) = 8,05 cm

**Induktiver Blindwiderstandsbelag:**
- Mittlerer geometrischer Abstand: d = ∛(d12 · d23 · d31) = ∛(10 · 10 · 10) = 10 m
- d' = ∛(d'12 · d'23 · d'31) = ∛(10 · 10 · 10) = 10 m
- d'' = ∛(d''11 · d''22 · d''33) = ∛(20 · 20 · 20) = 20 m
- L'b = (μ0 / 2π) · [ln(d·d' / (rb·d'')) + 1/(4·n)] mit μ0 = 4π·10⁻⁴ H/km
- L'b = 850 mH/km → X'l = ω·Lb = 267 mΩ/km

**Kapazitiver Blindwiderstandsbelag:**
- C'b = 2π·ε0 / ln(d·d' / (r·d'')) mit 2π·ε0 = 10⁻⁶/18 F/km
- C'b = 13,5 nF/km → X'c = 1/(ω·Cb) = 236 kΩ/km

**Ohmscher Widerstandsbelag:**
- R = 1/(κ·S) = 1/(36 m/mm² · 550 mm²) = 0,0505 Ω/km
- Bei Zweierbündel: R' = 0,025 Ω/km

**Gesamtnetzdaten (Tab. 7.14):**

| Leitung | Länge (km) | Cb (μF) | CE (μF) | X (Ω) | R (mΩ) |
|---|---|---|---|---|---|
| A | 110 | 1,43 | 0,715 | 29,3 | 2,75 |
| B | 118 | 1,53 | 0,765 | 31 | 2,95 |
| C | 120 | 1,56 | 0,78 | 32 | 3 |
| D | 90 | 1,17 | 0,585 | 24 | 2,25 |
| E | 58 | 0,754 | 0,377 | 15 | 1,45 |
| F | 60 | 0,78 | 0,39 | 16 | 1,5 |
| G | 90 | 1,17 | 0,585 | 24 | 2,25 |
| H | 70 | 0,91 | 0,455 | 18,6 | 1,75 |
| I | 140 | 1,82 | 0,91 | 37 | 3,5 |
| K | 115 | 1,5 | 0,75 | 30 | 2,9 |

**Maschinendaten der Einspeisungen:**
- Generatordaten: X''d = 20%, X2 = 15%, X0 = 5%, cosφ = 0,8, Spannungen 10 × 20 kV
- Transformatoren: Stern/Dreieck, ukr = 15%, X0 = X1, Z0 = Z1
- Annahmen: 20% aller Motoren speisen bei Kurzschluss zurück, Ian = 5·IrM
- Kraftwerksmotoren: X''d = 20%, X2 = 25%, X0 = 10%

**Reaktanzberechnung Einspeisungen:**

Einspeisung 1 (1300 MW, cosφ = 0,8):
- SrG = 1300 MW / 0,8 = 1625 MVA; 5% reserve = 81,25 MVA
- XG1 = (20%/100%) · (380 kV)² / 1625 MVA = 17,8 Ω; X''d = 356 Ω, X1 = 16,9 Ω

Einspeisung 2 (250 MW):
- SrG = 250 MW / 0,8 = 312,5 MVA; 5% = 15,6 MVA
- XG2 = (20%/100%) · (380 kV)² / 312,5 MVA = 92,4 Ω; X''d = 1851 Ω, X1 = 88 Ω

Einspeisung 3 (1000 MW):
- SrG = 1250 MVA; XG3 = 23,1 Ω; X''d = 462 Ω, X1 = 22 Ω

Einspeisung 4 (1673 MW):
- SrG = 2091 MVA; XG4 = 13,8 Ω; X''d = 276,2 Ω, X1 = 13 Ω

Einspeisung 5 (856 MW):
- SrG = 1070 MVA; XG5 = (20%/100%) · (380 kV)² / 1070 MVA; X''d = 540 Ω, X1 = 25,7 Ω

**Abnahmen (Motoren):**

Abnahme 1 (500 MW):
- SrM = 625 MVA; 20% = 125 MVA; X''d = 231 Ω, X1 = 38,5 Ω

Abnahme 2 (600 MW):
- SrM = 750 MVA; 20% = 150 MVA; X''d = 192,5 Ω, X1 = 32 Ω

Abnahme 3 (875 MW):
- SrM = 1094 MVA; 20% = 219 MVA; X''d = 131,8 Ω, X1 = 22 Ω

**Formel zur Reaktanzberechnung elektrischer Maschinen:**
- X''d = (x''d% / 100%) · (U²n / SrM)
- Reaktanz von Asynchronmaschinen aus Anzugsstrom: XM = U²n / (Ian/IrM)

**Formel für Leistung/Scheinleistung:**
- Pn = Sn · cosφ → Sn1 = Pn / cosφ = 1300 MW / 0,8 = 1625 MVA
- XG1 = X''d/100% · U²n/Sn = 20%/100% · (380 kV)²/1625 MVA = 17,8 Ω
- XG2 = 20%/100% · (380 kV)²/312,5 MVA = 92,4 Ω
- XG3 = 20%/100% · (380 kV)²/1250 MVA = 23,1 Ω
- XG4 = 20%/100% · (380 kV)²/2091 MVA = 13,8 Ω
