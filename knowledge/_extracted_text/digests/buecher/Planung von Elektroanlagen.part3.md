# Planung von Elektroanlagen — Teil 3
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 121-160.

Dieser Teil des Fachbuchs von Ismail Kasikci umfasst den Abschluss von Kapitel 7 (Kurzschluss- und Erdschlussberechnungen im Drehstromnetz) mit umfangreichen Berechnungsbeispielen sowie Kapitel 8 (Lastflussrechnung) und den Beginn von Kapitel 9 (Spannungsfallberechnung). Der Schwerpunkt liegt auf numerischen Beispielen zur Kurzschlussstromberechnung an realen Netztopologien und der Einführung in Lastflussverfahren.

## Inhalt

### 7.6 Berechnungsbeispiele für Kurzschlussströme (Fortsetzung)

#### 7.6.2 Beispiel: Mehrgeneratorennetz 380-kV-Ebene (Seite 121–122)

Gegeben sind mehrere Generatoren mit folgenden Nennleistungen und Reaktanzen:
- Generator 5: Sn5 = 856 MW, cos φ = 0,8 → Sn = 1070 MVA, XG5 = 20 %, XG5 = 27 mΩ
- Generator 6: Sn6 = 600 MW, cos φ = 0,8 → Sn = 750 MVA, XG6 = 20 %, XG6 = 38,5 mΩ
- Generator 7: Sn7 = 875 MW, cos φ = 0,8 → Sn = 1094 MVA, XG7 = 20 %, XG7 = 26,4 mΩ

Berechnung der Lastströme (Nennspannung Un = 380 kV):
- In1 = 2469 A (P = 1300 MW), Iw1 = 1975 A, Ib1 = 1481 A
- In2 = 1662 A (P = 875 MW), Iw2 = 1330 A, Ib2 = 997 A
- In3 = 1140 A (P = 600 MW), Iw3 = 912 A, Ib3 = 684 A
- In4 = 1626 A (P = 856 MW), Iw4 = 130 A, Ib4 = 976 A
- In5 = 3175 A (P = 1673 MW), Iw5 = 2542 A, Ib5 = 1906 A
- In6 = 1899 A (P = 1000 MW), Iw6 = 1519 A, Ib6 = 1139 A
- In7 = 474 A (P = 250 MW), Iw7 = 380 A, Ib7 = 285 A
- In8 = 950 A (P = 500 MW), Iw8 = 760 A, Ib8 = 570 A

Gesamtimpedanzen des Systems:
- XG = x"d · U²n / (100 % · Sn) = 20 % · (400 V)² / (100 % · 1625 MVA) = 19,7 mΩ
- XT = ukr · U²n / (100 % · SrT) = 15 % · (400 V)² / (100 % · 812,5 MVA) = 29,5 mΩ
- XTges = 15 mΩ
- Z1 = XG + XT + Xl = 19,7 + 15 + 10 = 44,7 mΩ
- XT0 = 0,8 · XTges = 12 mΩ; X0l = 3,5 · X1l = 35 mΩ
- Verhältnisse: Z2/Z0 = 44,7/47 = 0,95; Z2/Z1 = 44,7/44,7 = 1

Kurzschlussströme:
- I"k3 = c · Un / (√3 · Zk) = 1,1 · 380 kV / (√3 · 44,7 mΩ) = 5,4 kA
- I"k2 = √3 · c · Un / Zges = √3 · 1,1 · 380 kV / 136,4 mΩ = 1,77 kA
- I"k1 = √3 · c · Un / |2·Z1 + Z0| = 1,1 · 380 kV / 89 mΩ = 2,71 kA

#### 7.6.3 Beispiel: Netzschaltbild mit zwei Transformatoren (Seiten 123–128)

Berechnung der Netzeinspeisung (UnQ = 110 kV, S"kQ = 2000 MVA):
- ZQ = 1,1 · (110 kV)² / 2000 MVA = 6,655 Ω
- RQ = 0,1 · XQ (nach DIN VDE 0102)
- XQ = ZQ / 1,005 = 6,62 Ω
- ZQ = 0,662 + j6,62 Ω

Impedanzen einer 45-km-Freileitung:
- ZL1 = 45 km · (0,2374 + j0,408) Ω/km = (10,683 + j18,36) Ω

Transformation auf Niederspannungsseite (Übersetzungsverhältnis 21 kV / 115 kV):
- Z' = Z · (UrT1LV / UrT1HV)² = (11,345 + j24,98) Ω · (21/115)² = (0,38 + j0,83) Ω

Transformator T1 (SrT1 = 40 MVA, UrT1LV = 21 kV, ukr = 12 %, uRr = 0,5 %):
- uxrT1 = √(ukr² - uRr²) = √(12² - 0,5²) % = 11,99 %
- RT1 = uRrT1/100 % · U²rT1LV/SrT1 = 0,5 %/100 % · (21 kV)²/40 MVA = 0,0551 Ω
- XT1 = uxrT1/100 % · U²rT1LV/SrT1 = 11,99 %/100 % · (21 kV)²/40 MVA = 1,322 Ω
- ZT1 = (0,0551 + j1,322) Ω

Gesamtimpedanz bis Fehlerstelle F1:
- Zk1 = Z' + ZT1 = (0,4351 + j2,152) Ω → |Zk1| = 2,196 Ω
- I"k3 = 1,1 · 20 kV / (√3 · 2,196 Ω) = 5,79 kA

Stoßkurzschlussstrom an F1:
- R/X = 0,4351/2,152 = 0,2 → κ = 1,554
- ip = κ · √2 · I"k3 = 1,558 · √2 · 5,79 kA = 12,94 kA
- S"k3 = √3 · 20 kV · 5,79 kA = 200,6 MVA

Impedanzen an Fehlerstelle F2 (zusätzlich 4-km-Erdkabel, r0 = 0,157 Ω/km, x0 = 0,072 Ω/km):
- ZK1 = 4 km · (0,157 + j0,072) Ω/km = (0,628 + j0,288) Ω
- ZG2 = Zk1 + ZK1 = (1,0631 + j2,44) Ω
- Transformation auf 0,4 kV: ZG1' = (0,000425 + j0,000976) Ω

Transformator T2 (SrT2 = 630 kVA, UrT2LV = 0,4 kV, ukr = 6 %, uRr = 1,5 %):
- uxrT2 = √(6² - 1,5²) % = 5,81 %
- RT2 = 1,5 %/100 % · (0,4 kV)²/630 kVA = 0,0038 Ω
- XT2 = 5,81 %/100 % · (0,4 kV)²/630 kVA = 0,0148 Ω
- ZkF2 = √(0,00423² + 0,0158²) = 0,0164 Ω
- I"k3(F2) = 1,1 · 0,4 kV / (√3 · 0,0164 Ω) = 15,489 kA

Stoßkurzschlussstrom an F2:
- R/X = 0,00423/0,0158 = 0,27 → κ = 1,46
- ip3 = 1,42 · √2 · 15,489 kA = 31,1 kA

Impedanzen an Fehlerstelle F3 (Kabel 65 m, r0 = 0,197 Ω/km, x0 = 0,082 Ω/km):
- Zk3 = 0,065 km · (0,197 + j0,082) Ω/km = (0,0128 + j0,00533) Ω
- ZF3 = (0,01703 + j0,02113) Ω → |ZF3| = 0,0271 Ω
- I"k3(F3) = 1,1 · 0,4 kV / (√3 · 0,0271 Ω) = 9,52 kA

Stoßkurzschlussstrom an F3:
- R/X = 0,01703/0,02113 = 0,8 → κ = 1,1
- ip3 = 1,1 · √2 · 9,52 kA = 14,8 kA

#### 7.6.4 Beispiel: Generatornaher Kurzschluss (Seite 127)

Generator angeschlossen über 75-km-Kabel:
- SrG = 40 MVA, UnG = 10,5 kV, x"d = 34,5 %, x'd = 200 % (gesättigt)
- RL = r0 · l = 0,157 Ω/km · 75 km = 11,775 Ω
- XL = x0 · l = 0,080 Ω/km · 75 km = 6 Ω
- X"d = x"d · U²n / SrG = 34,5 % · (10 kV)² / (100 % · 40 MVA) = 0,863 Ω
- RsG = 0,07 · X"d = 0,07 · 0,863 Ω = 0,0604 Ω
- Zk = 11,83 + j6,86 Ω → |Zk| = 13,68 Ω
- I"k3 = 1,1 · 10 kV / (√3 · 13,68 Ω) = 464 A

#### 7.6.5 Beispiel: Fremdnetz über Transformator (Seiten 128–129)

Gegebene Größen: S"kQ = 2500 MVA, SrT = 40 MVA, ukr = 11,9 %, uRr = 0,5 %, Un = 20 kV:
- ZQt = c · U²n / S"kQ = 1,1 · (20 kV)² / 2500 MVA = 0,176 Ω
- XQt = 0,995 · 0,22 Ω = 0,175 Ω
- RQt = 0,1 · XQt = 0,0175 Ω
- ZT = ukr · U²n / (100 % · SrT) = 11,9 % · (20 kV)² / (100 % · 40 MVA) = 1,19 Ω
- XT = √(12² - 0,5²) % / 100 % · (20 kV)² / 400 MVA = 1,189 Ω
- RT = 0,5 % · (20 kV)² / (100 % · 40 MVA) = 0,05 Ω
- Gesamtimpedanz: Zk = (0,0675 + j1,364) Ω → |Zk| = 1,365 Ω
- I"k3 = 1,1 · 20 kV / (√3 · 1,365 Ω) = 9,3 kA

#### 7.6.6 Beispiel: Parallelschaltung von Generatoren und Transformatoren (Seiten 129–131)

220-kV-Netz, zwei Generatoren + zwei Transformatoren parallel:
- X"d (Generator) = x"d/100 % · (1,05 · 220 kV)² / 1020 MVA = 13,6 Ω; xd = 0,26
- XT = ukr/100 % · (220 kV)² / SrT = 0,17 · (220 kV)² / 980 MVA = 8,4 Ω
- Freileitung: R = r0 · l = 0,070 Ω/km · 50 km = 3,5 Ω; X = x0 · l = 0,403 Ω/km · 50 km = 20,15 Ω; Z = 20,45 Ω
- Gesamtimpedanz (Parallelschaltung je zwei Betriebsmittel):
  Zk = 1/2 · X"d + 1/2 · XT + 1/2 · Z = 31,45 Ω
- I"k3 = 1,1 · 220 kV / (√3 · 31,45 Ω) = 4,44 kA

#### 7.6.7 Beispiel: Hochspannungsmotor-Beitrag zum Kurzschlussstrom (Seiten 131–132)

20/6-kV-Netz, Motor angeschlossen:
- Netzeinspeisung (S"kQ = 500 MVA, transformiert auf 6-kV-Ebene):
  XQt = c · U²nQ / S"kQ · (UrM/UrT)² = 1,1 · (20 kV)² / 500 MVA · (6/20)² = 0,0792 Ω
- Freileitung (z0 = 0,33 Ω/km, l = 20 km, transformiert):
  ZFt = 0,33 Ω/km · 20 km · (6/20)² = 0,594 Ω
- Transformator (SrT = 2 MVA, ukr = 6 %, UrT = 6 kV):
  ZT = 6 %/100 % · (6 kV)² / 2 MVA = 1,08 Ω
- Gesamtimpedanz bis Motor: ZG = 0,0792 + 0,594 + 1,08 = 1,7532 Ω
- Motorimpedanz (PrM = 2,3 MW, UrM = 6 kV, Ian/IrM = 5, cos φ = 0,85, η = 0,98):
  Zm = η · cos φ / (Ian/IrM) · U²rM/PrM = 0,98 · 0,85 / 5 · (6 kV)² / 2,3 MW = 2,6 Ω
- Gesamtimpedanz am Motor: Zk = 1,7532 + 2,6 = 4,36 Ω (nur Mitimpedanz)
- Kurzschlussstrom am Motor: I"kM = 1,1 · 6 kV / (√3 · 4,36 Ω) = 0,874 kA
- S"k = √3 · 6 kV · 0,874 kA = 9 MVA

Ausschaltstrom für t = 0,1 s:
- IrM = PrM / (√3 · Un · η · cos φ) = 2,3 MW / (√3 · 6 kV · 0,85 · 0,98) = 266 A
- μ-Faktor: μ = 0,62 + 0,72 · e^(-0,32 · I"kM/IrM) = 0,62 + 0,72 · e^(-0,32 · 874/266) = 0,87
- q-Faktor (Motorleistung/Polpaarzahl = 2,3/2 = 1,15 MVA):
  q = 0,57 + 0,12 · ln(m/μ), wobei m = 2,3 → q = 0,708
- Ausschaltstrom: Ia = μ · q · I"kM = 0,87 · 0,708 · 0,874 kA = 521,72 A

#### 7.6.8 Beispiel: Industrienetz mit verschiedenen Netznennspannungen (Seiten 132–136)

Großes Industrienetz mit vier Motoren an unterschiedlichen Spannungsebenen.

Berechnungspunkt A (10-kV-Ebene):
- ZQt (Netzeinspeisung auf Punkt A transformiert) = 0,044 Ω
- ZT1LV = ukrT1/100 % · U²rT1LV/SrT1 = 0,381 Ω
- X"d (Generator) = x"d/100 % · U²rG/SrG = 26,46 Ω
- XM1t (Motor 1, transformiert) = (1/(Ian/IrM)) · U²rM1/SrM1 · (UrT1LV/UrT1HV) = 10 Ω
- ZT2HV = ukrT2/100 % · U²rT2HV/SrT2 = 3 Ω
- Gesamtimpedanz ohne NS-Motoren: ZkA = [(ZQt + ZT1) ‖ X"d ‖ (ZT2HV + XM1t)]
  Z = [(0,425) ‖ 26,46 ‖ (13)] Ω = 0,4052 Ω
- Strom: I"kA = 1,1 · 10 kV / (√3 · 0,4052 mΩ) = 15,67 kA

Berechnungspunkt B (6-kV-Ebene):
- ZQt (doppelt transformiert): 0,0158 Ω
- ZT1t = 12 %/100 % · (6 kV)² / 31,5 MVA = 0,1371 Ω
- X"d(Generator) = 12 %/100 % · (1,05 · 6 kV)² / 500 kVA = 9,5256 Ω
- XM1 = 1/(Ian/IrM) · U²nM1/SrM1 = 1/5 · (6 kV)² / 2 MVA = 3,6 Ω
- ZT2 = 6 %/100 % · (6 kV)² / 2 MVA = 1,08 Ω
- ZT3 = 6 %/100 % · (400 V)² / 630 kVA = 3,4286 Ω
- Gesamtimpedanz ohne NS-Motoren:
  ZkB = [[(ZQtt + ZT1t) ‖ X"dt + ZT2LV] ‖ XM1]
  Z = [[0,1529 ‖ 9,5256 + 1,08] ‖ 3,6] Ω = 0,917 Ω
- I"kB = 1,1 · 10 kV / (√3 · 0,917 mΩ) = 4,155 kA

Ersatzmotor für NS-Motoren (Summe):
- SrMers = Σ SrM = 160 kW + 250 kW + 75 kW = 593,58 kVA (η und cos φ berücksichtigt)
- IrMers = SrMers / (√3 · Un) = 593,58 kVA / (√3 · 400 V) = 856,8 A
- XMers = Un / (Ian/IrMers) = (6 kV)² / (5 · 593,58 kVA) = 12,1298 Ω

#### 7.6.9 Thermische Kurzschlussfestigkeit eines Kabels (Seiten 134–136)

Für κ = 1,8 erhält man m = 0,42; aus I"k/Ik = 23,55 kA / 8,5 kA = 2,77 ergibt sich n = 0,4.

Äquivalenter Thermischer Kurzzeitstrom:
- Ith = I"k · √(m + n) = 23,55 kA · √(0,42 + 0,4) = 21,32 kA

Bemessungskurzzeitstromdichte für das Kabel: Sth = 140 A/mm²

Mindestquerschnitt:
- S = Ith · √(tk/tkr) / Sth = 21,32 kA · √(1 s / s) / (140 A/mm²) = 152,3 mm²
- Ergebnis: Querschnitt von 152,35 mm² ist ausreichend.

#### 7.6.10 Motoranschluss 400-kW-Motor am Hauptverteiler (Seiten 136–138)

Transformator: R = 0,68 mΩ, X = 3,78 mΩ, Z = 3,84 mΩ

Kabel (120 m, r0 = 0,348 Ω/km, x0 = 0,151 Ω/km):
- R = r0 · l = 0,348 Ω/km · 0,120 km = 41,76 mΩ
- X = x0 · l = 0,151 Ω/km · 0,120 km = 18,12 mΩ
- Rk = 42,44 mΩ; Xk = 21,9 mΩ; Zk = √(Rk² + Xk²) = 47,76 mΩ

Dreipoliger Kurzschlussstrom:
- I"k3 = 1,1 · 400 V / (√3 · 47,76 mΩ) = 5,31 kA (Korrektur: Wert im Buch 5,31 kA)

Stoßstrom:
- R/X = 42,44/21,89 = 1,94 → κ = 1,023
- ip = κ · √2 · I"k3 = 7,68 kA

Dynamische Kraft an der Sammelschiene (Leiterabstand a = 0,01 m, Leiterlänge l = 1 m):
- F = μ0/(2π) · ip² · l/a · 0,102 = 4π·10⁻⁷ / 2 · (7,68 kA)² · 1/0,01 · 0,102 = 3,77 N

#### 7.6.11 Berechnung der Daten von Hochspannungsmotoren (Seiten 137–140)

Sechs Hochspannungsmotoren angeschlossen; Berechnung im %/MVA-System:
- Netzreaktanz: ZQ = c · 100 % / S"kQ = 1,1 · 100 % / 2000 MVA = 0,055 %/MVA
- Transformator: ZT = ukr/SrT = 15 % / 125 MVA = 0,12 %/MVA
- Generator: XG = x"d/SrG = 12 % / 125 MVA = 0,096 %/MVA
- Asynchronmotor (6 Motoren à 2,5 MVA, Ian/IrM = 5):
  XM = 1/(Ian/IrM · SrM) · 100 % = 1/(5 · 6 · 2,5 MVA) · 100 % = 1,33 %/MVA
- Gesamtimpedanz: ZkF = [(ZQ + ZT) ‖ XG ‖ XM] = [(0,175) ‖ 0,096 ‖ 1,33] = 0,0592 %/MVA

Kurzschlussleistung an Fehlerstelle F1:
- S"F1 = 1,1 · 100 % / ZF1 = 1,1 · 100 % / 0,0592 %/MVA = 1858,1 MVA

Aufteilung der Einspeisebeiträge:
- Anteil ASM: S"kM = 0,062 / (0,062 + 1,33) · 1858,1 MVA = 82,76 MVA
- Anteil Generator: S"kG = 0,75 / (0,175 + 0,096) · (1858,1 - 82,76) MVA = 1146 MVA
- Anteil Netz: S"kQ = 0,096 / (0,175 + 0,096) · (1858,1 - 82,76) MVA = 628,9 MVA

Ermittlung μ- und q-Faktoren für t = 0,1 s:
- Motoren: S"kM/SrM = 82,76 MVA / (6 · 2,5 MVA) = 5,52 → μ = 0,74
- Generator: S"kG/SrG = 1146 MVA / 125 MVA = 9,17 → μ = 0,65
- q-Faktor (Motorleistung/Polpaarzahl = 2,5 MVA/2 = 1,25 MVA) → q = 0,6

Ausschaltleistungen:
- SaG = μ · S"kG = 0,65 · 51 MVA = 33 MVA (Bezugsbasis 51 MVA)
- SaM = μ · q · S"kM = 0,74 · 0,65 · 13,75 MVA = 6,61 MVA

Kurzschlussströme an Fehlerstelle F (Un = 6 kV):
- I"k3 = S"k / (√3 · Un) = 1858,1 MVA / (√3 · 6 kV) = 178,8 kA
- ip = κ · √2 · I"k3 = 2 · √2 · 7,6 kA = 505 kA (κ = 2 angenommen)
- Ausschaltstrom: Ia = Sa / (√3 · Un) = 628,9 MVA / (√3 · 6 kV) = 60,58 kA

#### 7.6.12 Niederspannungsstrahlennetz (Seiten 139–149)

Vollständiges Berechnungsbeispiel für ein NS-Netz mit Transformator, vier Kabeln/Freileitungen und zwei Motoren.

Netzdaten:
- Netzeinspeisung: UnQ = 20 kV, I"kQmax = 28,9 kA (cQmax = 1,1), I"kQmin = 23,12 kA (cQmin = 1,0)
- Transformator T: SrT = 630 kVA, UrTOS = 20 kV, UrTUS = 0,4 kV, ukrT = 4 %, uRrT = 1,03 %
- Nullimpedanzverhältnisse: R(0)T/RTUS = 1; X(0)T/XTUS = 0,95

Kabeldaten (Tabelle 7.15 paraphrasiert):

| Kabel | Querschnitt | r0 (mΩ/km) | x0 (mΩ/km) | Länge (m) | R(0)/R | X(0)/X |
|-------|-------------|-------------|-------------|-----------|--------|--------|
| L1    | 3×300 mm²  | 62          | 105         | 3200      | —      | —      |
| L2    | 2×(4×185 mm²) | 101      | 80          | 18        | 4      | 3,65   |
| L3    | 4×95 mm²   | 267         | 82          | 15        | 4      | 3,65   |
| L4    | 5×10 mm²   | 1810        | 94          | 35        | 4      | 4,02   |

Motordaten (Tabelle 7.16 paraphrasiert):

| Motor | PrM (kW) | cos φrM | ηrM |
|-------|----------|---------|-----|
| M1    | 200      | 0,88    | 0,93 |
| M2    | 160      | 0,88    | 0,93 |

**Berechnung der größten Ströme — Hochspannungsseite (cQmax = 1,1):**
- ZQ = cQ · UnQ / (√3 · I"kQmax) = 1,1 · 20 kV / (√3 · 28,9 kA) = 440 mΩ
- XQ = 0,995 · 440 mΩ = 437,8 mΩ; RQ = 0,1 · XQ = 43,78 mΩ
- RL1 = r0L · l = 62 mΩ/km · 3,2 km = 198,4 mΩ; XL1 = 105 mΩ/km · 3,2 km = 336 mΩ
- Übersetzungsverhältnis: tr = 20 kV / 0,4 kV = 50
- Gesamtimpedanzen OS transformiert auf US:
  ΣRHVt = 1/tr² · ΣRHV = 0,0968 mΩ; ΣXHVt = 1/tr² · ΣXHV = 0,3095 mΩ

**Transformatormitimpedanz auf Niederspannungsseite (größte Ströme):**
- ZTUS = 4 %/100 % · (0,4 kV)² / 630 kVA = 10,16 mΩ
- RTUS = 1,15 %/100 % · (0,4 kV)² / 630 kVA = 2,69 mΩ (Hinweis: uRrT-Korrektur)
- XTUS = √(ZTUS² - RTUS²) = √(10,15² - 2,61²) mΩ = 9,8 mΩ (Wert aus Berechnung)

**NS-Leitungsimpedanzen (größte Ströme):**
- L2 (zwei parallel): RL2 = 1/2 · 101 mΩ/km · 0,018 km = 0,909 mΩ; XL2 = 1/2 · 80 mΩ/km · 0,018 km = 0,72 mΩ
- L3: RL3 = 267 mΩ/km · 0,015 km = 4 mΩ; XL3 = 82 mΩ/km · 0,015 km = 1,23 mΩ
- L4: RL4 = 1810 mΩ/km · 0,035 km = 63,35 mΩ; XL4 = 94 mΩ/km · 0,035 km = 3,29 mΩ

**Berechnete Impedanzen und dreipolige Kurzschlussströme (Tabelle 7.17 paraphrasiert):**

Kumulierte Impedanzen (Zeilen = aufeinanderfolgende Netzabschnitte):

| Zeile | Betriebsmittel | Rk (mΩ) | Xk (mΩ) | Zk (mΩ) |
|-------|----------------|---------|---------|---------|
| 1     | ΣZOSt          | 0,0969  | 0,3095  | —       |
| 2     | T1 LV          | 2,69    | 10,16   | —       |
| 3     | 1+2            | 2,787   | 10,47   | 10,83   |
| 4     | L2             | 0,909   | 0,72    | —       |
| 5     | 3+4            | 3,7     | 11,19   | 11,78   |
| 6     | L3             | 4       | 1,23    | —       |
| 7     | 5+6            | 7,7     | 12,42   | 14,61   |
| 8     | L4             | 63,35   | 3,29    | —       |
| 9     | 7+8            | 70,05   | 15,71   | 72,77   |

**Größte dreipolige Ströme (Zeilen 3, 5, 7, 9):**

| Stelle | I"k (kA) | R/X   | κ    | ip (kA) |
|--------|----------|-------|------|---------|
| F1 (1+2) | 21,32  | 0,266 | 1,42 | 42,8   |
| F2 (3+4) | 19,6   | 0,33  | 1,4  | 38,8   |
| F3 (5+6) | 15,81  | 0,62  | 1,18 | 26,4   |
| F4 (7+8) | 3,17   | 4,5   | 1,0  | 4,48   |

**Größte zweipolige Ströme:** I"k2 = (√3/2) · I"k3; ip2 = (√3/2) · ip

| Stelle | I"k2 (kA) | ip2 (kA) |
|--------|-----------|----------|
| F1     | 18,46     | 37,07    |
| F2     | 16,97     | 33,6     |
| F3     | 13,69     | 22,86    |
| F4     | 2,75      | 3,88     |

**Transformatornullimpedanz:**
- R(0)T = R(0)T/RTUS · RTUS = 1 · 2,69 mΩ = 2,69 mΩ
- X(0)T = X(0)T/XTUS · XTUS = 0,95 · 9,8 mΩ = 9,31 mΩ

**NS-Nullimpedanzen der Leitungen (größte Ströme):**
- L2: R(0)L2 = 4 · RL2 = 4 · 0,909 mΩ = 3,6 mΩ; X(0)L2 = 3,65 · XL2 = 3,65 · 0,72 mΩ = 2,6 mΩ
- L3: R(0)L3 = 4 · 4 mΩ = 16 mΩ; X(0)L3 = 3,65 · 1,23 mΩ = 4,49 mΩ
- L4: R(0)L4 = 4 · 63,35 mΩ = 253,4 mΩ; X(0)L4 = 4,02 · 3,29 mΩ = 13,23 mΩ

**Größte einpolige Ströme (Tabelle 7.18 paraphrasiert):**

Mitimpedanzen und Nullimpedanzen kumuliert, resultierende Gesamtimpedanz:
- Formel: R = 2·R(1) + R(0); X = 2·X(1) + X(0); Z = √(R² + X²)

| Zeile  | R (mΩ)  | X (mΩ) | Z (mΩ) |
|--------|---------|--------|--------|
| 1+2    | 8,264   | 30,25  | 31,36  |
| 3+4    | 13,69   | 34,29  | 36,92  |
| 5+6    | 37,69   | 38,07  | 53,57  |
| 7+8    | 417,79  | 61,05  | 422,23 |

| Stelle | I"k1 (kA) | κ    | ip1 (kA) |
|--------|-----------|------|----------|
| F1     | 22,09     | 1,42 | 44,4     |
| F2     | 18,77     | 1,4  | 37,2     |
| F3     | 12,93     | 1,18 | 20,66    |
| F4     | 1,64      | 1,0  | 2,32     |

**Motorenbeitrag (Asynchronmotoren):**
- Bedingung: ΣIrM · 0,01 ≤ I"k (un-maßgeblich falls kleiner)
- SrM1 = PrM1 / (ηrM · cos φrM) = 200 kW / (0,93 · 0,88) = 244 kVA
- SrM2 = 160 kW / (0,93 · 0,88) = 195,5 kVA
- ΣSrMi = 439,5 kVA; ΣIrMi = 0,6344 kA (an Stelle F2, Un = 0,4 kV)

**Berechnung für kleinste Ströme (cQmin = 1,0, I"kQmin = 23,12 kA):**

Netzeinspeisung:
- ZQ = 1,0 · 20 kV / (√3 · 23,12 kA) = 499,44 mΩ (Buch: 549,38 mΩ bei cQ = 1,1, tatsächlich cQmin = 1,0 in der Beschriftung aber cQ = 1,1 in der Formel laut Text)
- XQ = 0,995 · ZQ = 546,63 mΩ; RQ = 0,1 · XQ = 54,66 mΩ
- RL1(korr.) = 1,24 · 198,4 mΩ = 246 mΩ (Temperaturkorrekturfaktor)

NS-Leitungen (kleinste Ströme, Temperaturkorrektur 1,24):
- L2 (zwei parallel): RL = 1,24 · 0,909 mΩ = 1,13 mΩ
- L3: RL = 1,24 · 4 mΩ = 4,96 mΩ
- L4: RL = 1,24 · 63,35 mΩ = 78,554 mΩ

NS-Nullimpedanzen (kleinste Ströme):
- L2: R(0) = 4 · 1,13 mΩ = 4,52 mΩ; X(0) = 3,65 · 0,72 mΩ = 2,6 mΩ
- L3: R(0) = 4 · 4,96 mΩ = 19,84 mΩ; X(0) = 3,65 · 1,23 mΩ = 4,49 mΩ
- L4: R(0) = 4 · 78,554 mΩ = 314,2 mΩ; X(0) = 4,02 · 3,29 mΩ = 13,23 mΩ

**Kleinste dreipolige Ströme (Tabelle 7.19 paraphrasiert):**

| Zeile  | Rk (mΩ) | Xk (mΩ) | Zk (mΩ) |
|--------|---------|---------|---------|
| 1+2    | 2,8     | 10,13   | 10,51   |
| 3+4    | 3,93    | 10,85   | 11,54   |
| 5+6    | 8,89    | 12      | 15,01   |
| 7+8    | 87,44   | 15,4    | 88,78   |

| Stelle | I"k (kA) | R/X  | κ    | ip (kA) |
|--------|----------|------|------|---------|
| F1     | 20,87    | 0,28 | 1,48 | 43,7    |
| F2     | 19       | 0,36 | 1,07 | 28,75   |
| F3     | 14,6     | 0,74 | 1,18 | 24,4    |
| F4     | 2,47     | 5,7  | 1,01 | 3,53    |

**Kleinste zweipolige Ströme:**

| Stelle | I"k2 (kA) | ip2 (kA) |
|--------|-----------|----------|
| F1     | 18,1      | 37,8     |
| F2     | 16,5      | 24,9     |
| F3     | 12,6      | 21,13    |
| F4     | 2,14      | 3,1      |

**Kleinste einpolige Ströme (c = cmin = 0,9, Tabelle 7.20 paraphrasiert):**

Resultierende Gesamtimpedanzen:

| Zeile  | R (mΩ)  | X (mΩ) | Z (mΩ) |
|--------|---------|--------|--------|
| 1+2    | 82,9    | 29,57  | 30,7   |
| 3+4    | 15,07   | 33,6   | 36,8   |
| 5+6    | 44,83   | 40,6   | 60,5   |
| 7+8    | 516,13  | 60,43  | 519,7  |

| Stelle | I"k1 (kA) | κ    | ip1 (kA) |
|--------|-----------|------|----------|
| F1     | 21,44     | 1,48 | 44,9     |
| F2     | 17,89     | 1,07 | 27,16    |
| F3     | 10,89     | 1,18 | 18,2     |
| F4     | 1,27      | 1,01 | 1,8      |

#### 7.6.13 Berechnung mit bezogenen Größen (Seiten 149)

Gleiche Aufgabe (Un = 20 kV, Zk = 3 Ω, c = 1,1) in drei verschiedenen Systemen:

**V, A, Ω-System (absolut):**
- I"k3 = c · Un / (√3 · Zk) = 1,1 · 20 kV / (√3 · 3 Ω) = 4,23 kA

**Per-Unit-System (pu):**
- Bezugsgrößen: UB = Un = 20 kV, SB = 100 MVA
- un = Un/UB = 1 p.u.
- zk = Zk · SB/U²B = 3 Ω · 100 MVA / (20 kV)² = 0,75 p.u.
- I"k3 = c · un / (√3 · zk) = 0,847 p.u. → I"k3 = 0,847 · SB/UB = 4,23 kA

**%/MVA-System:**
- zk = Zk · 100 % / U²n = 0,75 · 100 %/MVA
- I"k3 = c · 100 % / (√3 · zk) = 84,678 MVA (als Leistungsgröße)
- I"k3 = ik3 · 1/Un = 4,23 kA

### 7.7 Zusammenfassung Kurzschlussberechnung (Seite 150)

- Aus technischen und wirtschaftlichen Überlegungen muss die Kurzschlussberechnung für drei- und einpolige Fehler durchgeführt werden, um die dynamische Kurzschlussfestigkeit der Anlage zu prüfen und die Abschaltverhältnisse zu beurteilen.
- Bei Fehlern dürfen weder Personen noch Betriebsmittel gefährdet werden.
- Die Norm DIN EN 60909-0:2016-12 (= VDE 0102:2016-12) hat sich als Berechnungsstandard in der Praxis durchgesetzt.
- Bei komplexen Netzen sind Softwareprogramme unerlässlich; Tabellen und Diagramme unterstützen die händische Normanwendung.

**Normative Grundlagen (Literatur Kapitel 7):**
- DIN EN 60909-0 (VDE 0102):2016-12 — Kurzschlussströmberechnung in Drehstromnetzen
- Oeding/Oswald: Elektrische Kraftwerke und Netze, 8. Aufl., Springer 2017
- Heuck/Dettmann/Schulz: Elektrische Energieversorgung, 8. Aufl., Vieweg+Teubner
- Schwab: Elektroenergiesysteme, 5. Aufl. 2017
- Kasikci: Kurzschlussstromberechnung nach DIN EN 60909, 5. Aufl., Expert-Verlag 2016
- Beiblätter 1–4 zu DIN VDE 0102 (Beispiele, Anwendungsleitfaden, Faktoren)

---

### Kapitel 8: Lastflussrechnung

#### 8.1 Begriffe und Knotentypen (Seiten 151–152)

Ziel der Lastflussrechnung ist die Ermittlung der komplexen Spannungen an allen Netzknoten sowie der Leistungsflüsse auf den Verbindungselementen (Freileitungen, Kabel, Transformatoren).

Lastflussberechnungen werden für zwei Lastzustände durchgeführt:
- Starklast (maximale Belastung)
- Schwachlast (minimale Belastung)

Es werden drei Knotenarten unterschieden:

**Slack-Knoten (Ausgleichsknoten):**
- Nur Spannungsbetrag und Phasenwinkel sind vorgegeben.
- Wirk- und Blindleistung stellen sich so ein, dass im gesamten Netz Leistungsgleichgewicht herrscht.
- Funktion: Ausgleich der Leistungsdifferenz nach Berechnung der Strom- und Spannungsverteilung.

**Lastknoten (P,Q-Knoten):**
- Die komplexe Aufnahmeleistung (Wirk- und Blindleistung) ist vorgegeben und bleibt während der Berechnung konstant.
- Das Spannungsabhängigkeitsverhalten der Verbraucher (konstanter Strom oder konstante Impedanz) ist zu berücksichtigen.

**Generatorknoten (Einspeiseknoten, P,V-Knoten):**
- Spannungsbetrag und Wirkleistungseinspeisung werden fest vorgegeben.
- Blindleistungsgrenzen aus dem Betriebsdiagramm des Generators werden häufig berücksichtigt.

Knotentypen-Übersicht (Tabelle 8.1 paraphrasiert):

| Knotenbezeichnung | Vorgegebene Größen | Gesuchte Größen | Typische Anwendung |
|-------------------|--------------------|-----------------|-------------------|
| Slack-Knoten      | U, φu              | P, Q            | Bezugsknoten      |
| Einspeiseknoten   | U, P               | φ, Q            | Generatoreinspeisungen |
| Negativer Verbraucherknoten | P, Q   | U, φ            | Einspeisung als Last modelliert |
| Verbraucherknoten | P, Q               | U, φ            | Verbraucher mit spannungsabhängigen Leistungen |

#### 8.2 Einführung in die Lastflussberechnung (Seiten 152–153)

Die stationäre Strom- und Spannungsverteilung im Netz wird durch die Lastflussrechnung bestimmt. Damit lassen sich folgende Fragestellungen beantworten:
- Leistungsverteilung und Optimierung im Netz
- Spannungsniveau an allen Netzknoten
- Überlastung von Betriebsmitteln
- Netzverhalten bei Generator- oder Verbraucherausfall
- Verlustminimierung
- Optimale Transformatorstufenstellung

Für Planung, Erweiterung oder Änderung einer Energieversorgungsanlage ist die Lastflussrechnung ein wesentliches Hilfsmittel. Mit ihr können ermittelt werden:
- Strom-Spannungs-Verhalten der Energieversorgung
- Spannungshaltung im Netz
- Auslastung der Kraftwerke
- Blindleistungszustand des Netzes
- Höchst- und Schwachlastzustände

Voraussetzungen für eine Lastflussberechnung:
- Symmetrischer Netzaufbau und -betrieb (einphasige Nachbildung durch R, L, C-Ersatzschaltungen)
- Lastmodellierung als: (1) konstante Impedanz, (2) konstanter Strom oder (3) konstante Leistung

Das Knotenpunktverfahren beschreibt das Netzverhalten; Knoten werden eingeteilt in Last-/Verbraucherknoten und Einspeise-/Generatorknoten. Am Slack-Knoten müssen Spannungsbetrag und Phasenwinkel bekannt sein; dort stellen sich Wirk- und Blindleistung so ein, dass im gesamten Netz Leistungsgleichgewicht besteht.

Verwendetes Lösungsverfahren in diesem Kapitel: ausschließlich Newton-Raphson-Methode.

#### 8.3 Notation der mathematischen Größen (Seiten 153–154)

Grundlegende Beschreibungsgrößen für elektrische Anlagen im Lastflusskontext:

Stromvektor am Knoten K über Admittanzmatrix YK:
- iK = YK · uK

Last an einem Knoten durch Scheinleistung:
- Si = Pi + j·Qi

Last als Impedanz oder Admittanz nachgebildet:
- Zi = U²i / Si
- Yi = Si / U²i

Last als konstanter Strom:
- Ii = Si / Ui

Knotenadmittanzmatrix (Matrizenform, n×n, symmetrisch):
- [Yij] · [Ui] = [Ii]
- Diagonalelemente Yij = Summe aller Admittanzen am Knoten i (positive Vorzeichen)
- Nebendiagonalelemente Yij (i ≠ j) = negative Summe der Zweigadmittanzen zwischen i und j; Null wenn keine direkte Verbindung besteht.

#### 8.4 Newton-Raphson-Verfahren (Seiten 154–157)

Das Newton-Raphson-Verfahren löst nichtlineare Gleichungssysteme der Form f(x) = 0 iterativ.

Prinzip:
- Die nichtlineare Funktion f(x) wird in eine Taylor-Reihe entwickelt und nach dem linearen Term abgebrochen.
- Rekursionsformel: x^(k+1) = x^k - f(x^k) / [df(x^k)/dx]
- Konvergenzkriterium: |x^(k+1) - x^k| < ε

Ablauf der Lastflussberechnung mit Newton-Raphson:
1. Aufstellung der Knotenadmittanzmatrix Y aus der Netztopologie.
2. Startwerte: Nennspannungen an Last-/Generatorknoten als Anfangsspannungen.
3. Berechnung von Wirk- und Blindleistungen an den Knoten; Abweichungen von den Sollwerten ermitteln.
4. Falls Abweichung unter Grenzwert → Iteration beendet, Lastfluss berechnet.
5. Sonst: Knotenpunktströme aus aktuellen Leistungen berechnen, Jacobi-Matrix bestimmen, korrigierten Spannungsvektor bilden → neue Leistungen → weiter bis Konvergenz.
6. Slack-Knoten wird nicht iteriert (Spannung dort bekannt und festgehalten).

**Beispiel 8.4.1: Lastflussberechnung Spannungsfall auf Leitung (Seite 156):**
- UV = zV / (zV + zL) · 100 % = 84,94 % (Spannung am Leitungsende in % der Netzspannung)
- i = UV / (√3 · zV) = 339,76 V / (√3 · 2,2 Ω) = 89,16 A
- Q = U²V / zV = (339,76 V)² / 2,2 Ω = 52,471 kvar (Blindleistung am Leitungsende)

**Beispiel 8.4.2: Anwendung Newton-Raphson auf f(x) = x + sin(x) - 2 = 0 (Seite 157):**
- Ableitung: f'(x) = 1 + cos(x)
- Rekursion: x^(k+1) = x^k - (x^k + sin(x^k) - 2) / (1 + cos(x^k))
- Startwert x0 = 0:

| Iterationsschritt k | x^k       |
|---------------------|-----------|
| 0                   | 0         |
| 1                   | 1         |
| 2                   | 1,103     |
| 3                   | 1,110606  |

Konvergenz nach 3 Schritten.

#### 8.5 Zusammenfassung Lastflussrechnung (Seite 157)

- Der Lastfluss stellt einen konkreten stationären Betriebszustand einer elektrischen Anlage dar.
- Mithilfe von Computerprogrammen können Netze simuliert und die Auslastung an jedem Knoten bestimmt werden.

**Normative Grundlagen und Literatur (Kapitel 8):**
- Oeding/Oswald: Elektrische Kraftwerke und Netze, 8. Aufl., Springer 2017
- Heuck/Dettmann/Schulz: Elektrische Energieversorgung, 8. Aufl., Vieweg+Teubner
- Schwab: Elektroenergiesysteme, 5. Aufl. 2017
- DIN EN 60909-0 (VDE 0102):2016-12

---

### Kapitel 9: Spannungsfallberechnung — Grundlagen (Seiten 158–160)

#### 9.1 Grundlagen und Ersatzschaltbild

Der Abschnitt behandelt ein Berechnungsverfahren für Spannungsdifferenzen in elektrischen Netzen; anwendbar auf Nieder- und Mittelspannungsleitungen (Freileitungen und Kabel).

Randbedingungen:
- Elektrisch kurze Leitung wird vorausgesetzt.
- Betriebskapazitäten sind vernachlässigbar klein.
- Ersatzschaltbild: Wirkwiderstand RL + Blindwiderstand XL in Reihe.
- Verbraucher sind vorwiegend oder ausschließlich ohmsch-induktiv: Strom eilt Spannung um Winkel φ nach.
- Der Spannungsfall darf die in DIN VDE und DIN-Normen festgelegten Grenzwerte nicht überschreiten.

Spannungsbeziehung an der Leitung (Leitungsstrom IA = IL = IE):
- UA = UE + IE · ZL mit ZL = RL + j·XL (Spannung am Leitungsanfang)

Strom mit induktiver und kapazitiver Blindkomponente:
- IE = Iw + j·Ib
- Wirkstrom: Iw = IE · cos φ
- Blindstrom: Ib = IE · sin φ

Spannungsfall allgemein:
- ΔU = IE · (RL + j·XL)
- ΔU = (Iw + j·Ib) · (RL + j·XL)
- ΔU = (Iw·RL - Ib·XL) + j·(Iw·XL + Ib·RL)

Längs- und Querspannungsfall (bezogen auf Strangspannung):
- ΔUl = IE·RL·cos φE + IE·XL·sin φE
- ΔUq = IE·XL·cos φE - IE·RL·sin φE

Beziehung zwischen Anfangs- und Endspannung:
- U²A = (UE + ΔUl)² + ΔU²q
- UE = √(U²A - ΔU²q) - ΔUl

Leitungswinkel (Stabilitätswinkel):
- δ = φA - φE = arctan(ΔUq / UA) = arctan(ΔUq / (UE + ΔUl))

Vereinfachung für Niederspannung: Querspannungsfall ΔUq sehr klein → vernachlässigbar.

Wenn die Leistung am Leitungsende (SE, QE) statt des Stroms bekannt ist:
- IL = (SE - j·QE) / (√3 · Un)

Relativer Spannungsfall (auf Nennspannung am Leitungsanfang bezogen):
- u = ΔUl / UA · 100 %
