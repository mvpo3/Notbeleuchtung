# Planung von Elektroanlagen — Teil 5
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 201-240.

Dieser Teil schließt das Kapitel 9 (Spannungsfallberechnung) mit einer langen Reihe numerischer Praxisbeispiele ab und leitet direkt zu Kapitel 10 über, das die Strombelastbarkeit von Kabeln und Leitungen behandelt — inklusive Überlastschutz, Kurzschlussschutz, Häufungs- und Temperaturkorrekturfaktoren sowie thermische Kurzschlussfestigkeit.

## Inhalt

### Kapitel 9 — Weitere Rechenbeispiele zur Spannungsfallberechnung (Seiten 201–231)

#### Beispiel 9.11.6 — Verbraucherdaten, Spannung, Strom, Leistung und Leistungsfaktor (Seite 174–175)

Ein 10 km langes Kabel versorgt einen Verbraucher mit einer Scheinleistung von 1 MVA bei induktivem Leistungsfaktor cos φ = 0,8. Leitungskonstanten: R'L = 0,465 Ω/km, X'L = 0,1 Ω/km, C'b = 0,4 µF/km. Verbraucherspannung exakt 10 kV.

Zwischenergebnisse:
- Wirkleistung am Verbraucher P₂ = 0,8 MW, Blindleistung Q₂ = 0,6 MVAr
- Leitungswiderstände: RL = 4,65 Ω, XL = 1 Ω
- Betriebskapazitäten je Leitungshälfte: Cb/2 = 2 µF
- Kompensierte Blindleistung am Leitungsende: QC2 = 62,8 kVAr

Ergebnisse (Näherungsformel ohne Querspannungsabfall):
- Spannung am Leitungsanfang: U1N = 10,426 kV
- Scheinleistung auf der Leitung: SL = 0,9625 MVA
- Leitungsstrom: IL = 55,5 A
- Verlustleistung Kabel: PV = 43,2 kW
- Blindleistungsbedarf Kabel: QL = 9,27 kVAr
- Kompensierte Blindleistung am Anfang: QC1 = 68,3 kVAr
- Wirkleistung Anfang: P1 = 0,843 MW
- Blindleistung Anfang: Q1 = 0,5878 MVAr
- Scheinleistung Anfang: S1 = 1,028 MVA
- Strom am Anfang: I1 = 57 A
- Leistungsfaktor am Anfang: cos φ = 0,82
- Wirkungsgrad des Kabels: η = 94,87 %

#### Beispiel 9.11.7 — Leiterquerschnitt (Seite 176–177)

Freileitung 6 km, Wirkleistung P₂ = 1 MW, induktive Blindleistung Q₂ = 0,8 MVAr. Speisespannung 10,4 kV, Verbraucherspannung 10 kV, Spannungsdifferenz darf 4 % nicht überschreiten. Stahl-Aluminium-Seile.

Vorgehen: Aus der Spannungsgleichung erhält man die Bedingung R'L + 0,8·X'L ≤ 0,66 Ω/km.

Querschnittsprüfung:
- 50 mm² Al: R'L + 0,8·X'L = 0,737 Ω/km → zu klein
- 70 mm² Al: R'L = 0,465 Ω/km, X'L = 0,34 Ω/km → R'L + 0,8·X'L = 0,737 Ω/km → ebenfalls zu klein
- 95 mm² Al: R'L = 0,342 Ω/km, X'L = 0,33 Ω/km → R'L + 0,8·X'L = 0,606 Ω/km → ausreichend (Spannungsdifferenz bleibt unter 4 %)

Ergebnis: Mindestquerschnitt 95 mm² Al bei dieser Freileitung.

#### Beispiel 9.11.8 — Leistungen an den Knotenpunkten (Seite 178)

Maschennnetz 60 kV, 50 km Freileitung. R'L = 0,34 Ω/km, X'L = 0,4 Ω/km, X'C = 350 kΩ/km. Spannung an Knoten 1: 63 kV, Spannung an Knoten 2: 60 kV (gleichphasig).

Leitungswiderstände: RL = 17 Ω, XL = 20 Ω, XC1 = XC2 = 14 kΩ.

Durch Betriebskapazitäten kompensierte Blindleistungen: QC1 = 0,283 MVAr, QC2 = 0,257 MVAr.

Berechnungsergebnisse:
- Eingespeiste Leistungen in Knoten 2: P₂ = 4,44 MW, Q₂ = 5,50 MVAr, S₂ = 7,1 MVA
- Leitungsstrom: IL = 66 A
- Verlustleistung: PV = 222 kW
- Blindleistungsbedarf Leitung: QL = 261 kVAr
- Leistungsabgabe Knoten 1: P1 = 4,662 MW, Q1 = 5,22 MVAr, S1 = 7 MVA

#### Beispiel 9.11.9 — Spannung an den Kondensatoren (Seite 179)

Drehstromtransformator 10 kV/500 V, SrT = 630 kVA, Leerlaufverluste 1,35 kW, Kurzschlussverluste 8,4 kW, relative Kurzschlussspannung ukr = 4 %. Belastet mit Kondensatorbatterie QC = 540 kVAr, 500 V.

Berechnungsweg:
- Relativer Wirkspannungsverlust: uRr = Pk/SrT = 8,4/630 = 1,33 %
- Relative Streuspannung: usx = √(ukr² − uRr²) = √(16 − 1,77) % = 3,77 %
- Belastungsgrad: I/IrT = QC/SrT = 540/630 = 0,8575
- Da kapazitiver Strom φ = 90°C voreilend: U'₁/U₂ = 1 − 0,8575·0,0377 = 0,9677
- Sekundärspannung: U₂ = 500 V / 0,9677 = 517,5 V

Anmerkung: Spannungsanstieg durch kapazitive Last; bei geringer Spannungsdifferenz bleibt Stromerhöhung vernachlässigbar.

#### Beispiel 9.11.10 — Spannung an den Motorklemmen (Seite 180–181)

Drehstromtransformator 10 kV/400 V, SrT = 630 kVA (Leerlaufverluste 0,32 kW, Kurzschlussverluste 1,95 kW, ukr = 4 %) mit 300 m Kabel (R'L = 0,22 Ω/km, X'L = 0,09 Ω/km) und Motor 70 kW, 400 V, cos φ = 0,8, η = 92 %.

Motoraufnahme:
- Wirkleistung: P₂ = 70 kW / 0,92 = 76,1 kW
- Blindleistung: Q₂ = P₂·tan φ = 76,1·0,75 = 57 kVAr

Leitungswiderstände: RL = 66 mΩ, XL = 27 mΩ.

Transformatorwiderstände (sekundärseitig):
- uRr = 1,95/100 = 1,95 %, usx = √(16 − 3,8) % = 3,49 %
- RT = 0,0195·400²/10⁵ = 4,95 mΩ, XT = 0,0349·400²/10⁵ = 8,86 mΩ

Gesamtwiderstände: R = 70,95 mΩ, X = 35,86 mΩ.

Spannung an den Motorklemmen (quadratische Gleichung):
- U²₂N − 400·U₂N + 7,44 = 0
- U₂N = 200 + √(200² − 7440) = 200 + 217,8 = 417,8 V

#### Beispiel 9.11.11 — Verbraucherspannung (Seite 182)

Freileitung 20 kV, 7 km (R'L = 0,465 Ω/km, X'L = 0,34 Ω/km, C'b = 0) + Transformator 20 kV/400 V, SrT = 1 MVA, uRr = 1,35 %, ukr = 6 %. Belastung: 800 kVA, induktiver Leistungsfaktor.

Alle Widerstände werden auf Sekundärseite (400 V) umgerechnet (Faktor (U₂N/U₁N)² = (0,4/20)²):
- Freileitungswiderstände: RL = 26 mΩ, XL = 19,04 mΩ
- Transformator: usx = √(36 − 1,82) % = 5,85 %, RT = 2,16 mΩ, XT = 9,36 mΩ
- Gesamtwiderstände: R = 5,41 mΩ, X = 11,74 mΩ

Wirk- und Blindleistung: P₂ = 0,64 MW, Q₂ = 0,48 MVAr. Auf Sekundärseite umgerechnete Speisespannung: U'1N = 0,4 kV.

Quadratische Gleichung ergibt: U₂N = 0,2 + √(0,04 − 0,00998) = 0,2 + 0,173 = 0,373 kV = 373 V.

#### Beispiel 9.11.12 — Verbraucherspannung und Wirkungsgrad der Leitung (Seite 183–184)

Freileitung 20 kV, 8 km (R'L = 0,465 Ω/km, X'L = 0,34 Ω/km, C'b = 0). Last: 800 kVA, cos φind = 0,8. Leitungswiderstände: RL = 3,72 Ω, XL = 2,72 Ω.

**Fall a) ohne Kondensatoren:**
- P₂ = 0,64 MW, Q₂ = 0,48 MVAr
- Quadratische Gleichung → U₂N = 10 + √(100 − 3,69) = 19,81 kV
- Leitungsstrom: IL = 0,8 MVA / (√3 · 19,81 kV) = 23,32 A
- Leitungsverluste: PV = 3 · 23,32² · 3,72 = 6 kW
- Wirkungsgrad: η = 1 − 6/(640 + 6) = 99 %

**Fall b) mit Kondensatorbatterie (Kompensation auf cos φ = 0,95):**
- Reduzierte Blindleistung: Q'₂ = 0,64 MVAr · tan(18,2°) = 0,21 MVAr
- Erforderliche Kondensatorleistung: QC = 0,48 − 0,21 = 0,27 MVAr
- Neue Verbraucherspannung: U₂N = 10 + √(100 − 2,992) = 19 kV (niedrigerer Spannungsanstieg im Netz)
- Neuer Leitungsstrom: I'L = 0,673 MVA / (√3 · 15 kV) = 25,82 A
- Neue Verluste: P'V = 3 · 25,82² · 3,72 = 7,44 kW
- Wirkungsgrad: η' = 1 − 7,44/647,44 = 98,85 %

Hinweis: Kompensation verbessert zwar den Leistungsfaktor, erhöht aber nicht zwingend den Wirkungsgrad der Leitung, da der Strom durch die kapazitive Blindleistung sogar leicht ansteigen kann.

#### Beispiel 9.11.13 — Speisespannung (Seite 184–185)

Freileitung 80 km, R'L = 0,27 Ω/km, X'L = 0,42 Ω/km, X'C = 360 kΩ/km. Verbraucher: U₂N = 110 kV, P₂ = 32 MW, Q₂ = 24 MVAr.

Leitungswiderstände: RL = 21,6 Ω, XL = 33,6 Ω, XC2 = 9 kΩ.
Kapazitive Blindleistung Leitungsende: QC2 = 110²·10⁶/9000 = 1,345 MVAr.

**Fall a) ohne Kondensatorbatterie:**
- U1N = 110 + (32·21,6 + 22,655·33,6)/110 = 110 + 13,23 = 123,23 kV

**Fall b) mit Kondensatorbatterie von 12 MVAr am Verbraucher:**
- Q'₂ − QC2 = 24 − 1,345 − 12 = 10,655 MVAr
- U1N = 110 + (32·21,6 + 10,655·33,6)/110 = 110 + 9,55 = 119,55 kV

Kondensatoren reduzieren die erforderliche Speisespannung erheblich.

#### Beispiel 9.11.14 — Wellenwiderstand, natürlicher Strom und natürliche Leistung (Seite 185)

Freileitung 380 kV, 300 km. Leitungskonstanten: R' = 0,034 Ω/km, X'L = 0,27 Ω/km, G' = 0,017 µS/km, B'C = 4,32 µS/km.

**Fall a) R' = 0, G' = 0 (verlustlos):**
- Wellenwiderstand: ZL = √(X'L/B'C) = √(0,27/(4,32·10⁻⁶)) = 250 Ω
- Natürlicher Strom: Inat = 380 kV / (√3 · 250) = 880 A
- Natürliche Leistung: Pnat = 380² / 250 = 577,5 MW

**Fall b) R' ≠ 0, G' ≠ 0 (reale Leitung):**
- ZL = √((0,034 + j0,27) / (0,017 + j4,32)·10⁻⁶) = 251 Ω · e^(j3,5°)
- Inat = 877 A · e^(−j3,5°)
- Snat = 575 MVA · e^(j3,5°) = (574 − j35) MVA (kleiner kapazitiver Blindleistungsanteil)

Schlussfolgerung: Unterschied zwischen verlustloser und realer Berechnung ist bei Freileitungen praktisch gering.

#### Beispiel 9.11.15 — Spannung am Ende der Freileitung im Leerlauf (Seite 186–187)

Freileitung 380 kV im Leerlauf, Spannung am Anfang 380 kV.

**Fall a) ohne Wirkwiderstände:**
- β·l = √(X'L·C'b) · l = 1,08·10⁻³/km · 300 km = 0,324 rad = 18,6°
- U₂N = 380/cos(18,6°) = 380/0,948 = 400,8 kV (Ferranti-Effekt: Spannung am Ende höher)
- Netzstrom I₁ = j279 A (rein kapazitiv, eilt Spannung um 90° vor)

**Fall b) mit Wirkwiderständen:**
- U₂N ≈ 400,6 kV (nahezu gleich)
- I₁ ≈ j279 A (kaum Unterschied)

Ladestrom beträgt 32 % des natürlichen Stroms der Freileitung.

#### Beispiel 9.11.16 — Stromverteilung bei Kurzschluss am Leitungsende (Seite 188)

Freileitung 380 kV, kurzgeschlossen am Ende.

**Fall a) verlustlos:**
- I₂ = U₁ / (j·ZL·sin(β·l)) → betragsmäßig 2,76 kA, kapazitiv
- I₁ = I₂·cos(β·l) = j2,62 kA

**Fall b) mit Verlusten:**
- I₂ = 2,735 kA · e^(j82,6°)
- I₁ = 2,59 kA · e^(j82,1°)

Ergebnis: Leitungskapazitäten kompensieren einen Teil des überwiegend induktiven Kurzschlussstroms; Strom am Anfang deshalb kleiner als am Ende. Unterschiede verlustlos/verlustbehaftet gering.

#### Beispiel 9.11.17 — Spannung am Anfang bei natürlicher Last (Seite 188)

Freileitung 380 kV mit natürlicher Leistung belastet, Verbraucher mit 380 kV versorgt.

**Fall a) verlustlos:**
- U₁ = U₂N · e^(jβl) → Betrag = 380 kV, Phasenvoreilung 18,6°

**Fall b) mit Verlusten:**
- U₁ = 380 kV · e^(0,97+j0,326) = 389 kV · e^(j18,6°)
- Zur Deckung der Leitungsverluste muss Netzspannung um etwa 2,4 % erhöht werden.

#### Beispiel 9.11.18 — Wellenwiderstand und natürliche Leistung eines Ölkabels (Seite 189)

Ölkabel 110 kV, 50 km. Leitungskonstanten: R' = 0,08 Ω/km, X'L = 0,12 Ω/km, C' = 0,31 µF/km.

**Fall a) verlustlos:**
- ZL = √(X'L/(ω·C')) = √(0,12/(314·0,31·10⁻⁶)) = 35 Ω
- Inat = 110 kV / (√3·35 Ω) = 1,815 kA
- Pnat = 110²/35 = 346 MW

**Fall b) mit Wirkwiderstand:**
- ZL = √((0,08 + j0,12) / (j314·0,31·10⁻⁶)) = 38,45 Ω · e^(j16,85°)
- Inat = 1,65 kA · e^(−j16,85°)
- Snat = 314 MVA · e^(j16,85°) = (301 − j91,4) MVA

Hinweis: Unterschiede zwischen verlustlos und verlustbehaftet betragen hier ca. 10 %; bei Kabeln ist die Vernachlässigung des Wirkwiderstands daher im Allgemeinen nicht zulässig. Maximaler zulässiger Strom dieses Kabels: 575 A → Betrieb mit natürlicher Leistung (1,815 kA) nicht möglich.

#### Beispiel 9.11.19 — Spannung am Ende des Kabels im Leerlauf (Seite 190)

Ölkabel 110 kV, Anfangsspannung 110 kV, Leerlauf.

**Fall a) verlustlos:**
- ω·√(L'·C')·l = 0,171 rad = 9,8°
- U₂N = 110 kV / cos(9,8°) = 111,6 kV (1,45 % höher als am Anfang)
- Netzstrom: I₁ = j313 A (rein kapazitiv ≈ 55 % des zulässigen Stroms)

**Fall b) mit Wirkwiderstand:**
- U₂N ≈ 111,6 kV (nahezu unverändert)
- I₁ ≈ j310 A (Unterschied vernachlässigbar)

#### Beispiel 9.11.20 — Strom bei Kurzschluss am Kabelende (Seite 191)

Ölkabel 110 kV, Kurzschluss am Ende, Anfangsspannung 110 kV.

**Fall a) verlustlos:**
- I₂ = 110 kV / (√3·35 Ω·0,17) = j10,67 kA
- I₁ = j10,51 kA

**Fall b) mit Wirkwiderstand:**
- I₂ = 8,85 kA · e^(j56,65°)
- I₁ = 8,71 kA · e^(j56,65°)

Wichtig: Wirkwiderstand von Kabeln setzt den Kurzschlussstrom deutlich herab (hier ca. 17 % Reduktion gegenüber verlustloser Berechnung).

#### Beispiel 9.11.21 — Spannung und Strom am Kabelanfang bei Wirkstrombelastung (Seite 192)

Ölkabel 110 kV, Verbraucherwirkstrom 400 A, Endspannung 110 kV.

**Fall a) verlustlos:**
- U₁N = 108,3 kV (Netzstrom mit kapazitiver Komponente I₁ = 500 A · e^(−j38°))

**Fall b) mit Wirkwiderstand:**
- U₁N = 111,2 kV, I₁ = 503 A · e^(−j38,4°)

Netzstrom enthält beachtliche kapazitive Komponente durch hohe Kabelkapazitäten. Belastung liegt nahe Leerlaufbereich im Vergleich mit natürlicher Kabelleistung.

#### Beispiel 9.11.22 — Strom und Spannung bei induktiver Last (Seite 193–194)

Ölkabel 110 kV, Verbraucherstrom 400 A bei cos φind = 0,8, Endspannung 110 kV.

Bezugsgröße U₂ = 63,5 kV, I₂ = (320 − j240) A.

**Fall a) verlustlos:**
- U₁N = 110,85 kV, I₁ = (315 − j72) A = 324 A · e^(−j12,85°)

**Fall b) mit Wirkwiderstand:**
- U₁N = 113 kV, I₁ = (317 + j75) A = 326 A · e^(j13,3°)

Induktive Verbraucherstromkomponente kompensiert einen großen Teil der kapazitiven Netzstromkomponente → Betrag des Netzstroms deutlich kleiner als bei rein ohmscher Last.

Schlussfolgerung aus den Kabelbeispielen 9.11.15–9.11.22:
- Einfluss des Wirkwiderstands bei Kabeln ist bis auf Kurzschlussströme gering
- Berechnungen mit Leitungsgleichungen sehr aufwendig; bei 50 km ausreichend, konzentrierte Schaltelemente zu verwenden
- Ladestrom bei Kabeln beachtlich und erreicht schnell thermische Belastungsgrenze → nur kurze Kabellängen für Leerlaufbetrieb geeignet

#### Beispiel 9.11.23 — Ausbreitungsgeschwindigkeit auf dem Kabel (Seite 194)

Für das Ölkabel (X'L = 0,12 Ω/km, C' = 0,31 µF/km) ergibt sich:

- Wellenlänge: λ = 2π / β = 2π / (ω·√(L'·C')) = 1.835 km
- Ausbreitungsgeschwindigkeit: v = λ/T = λ·f = 1.835 km · 50/s = 91.750 km/s
- Das entspricht v = 0,306·c (rund ein Drittel der Lichtgeschwindigkeit)
- Im freien Raum bei 50 Hz: Wellenlänge 6.000 km bei Lichtgeschwindigkeit c

#### Beispiel 9.11.24 — Ladestromkompensationsdrossel für die Freileitung (Seite 195–196)

Ziel: Spannung am Freileitungsende im Leerlauf auf 380 kV begrenzen (Ferranti-Effekt unterdrücken). Wirkwiderstände werden vernachlässigt.

Berechnung:
- Sternspannung: U₂ = 380/√3 = 220 kV
- Drossel-Kompensationsstrom: IDr = 220 kV · (1 − 0,948) / (250 Ω · 0,319) = 143 A (kapazitiv/induktiv)
- Drosselreaktanz: XDr = 220 kV / 143 A = 1,54 kΩ
- Drosselblindleistung: QDr = 3 · 220 kV · 143 A = 94,5 MVAr
- Strom am Leitungsanfang: I₁ = j145 A (kapazitiv)

Die Drossel am Leitungsende kompensiert die kapazitive Blindleistung der hinteren Leitungshälfte; die vordere Hälfte wird vom Netz gespeist. Strom in Leitungsmitte = 0.

Drosselleistung entspricht einer Transformator-Baugröße von 47,25 MVA (Drossel hat nur eine Wicklung).

Maximale Spannung auf der Leitung:
- Ux = 220 kV·cos(β·x) + 35,8 kV·sin(β·x)
- Maximum bei β·x = 9,23° (d.h. rund in Leitungsmitte)
- Uxmax = 222,87 kV → ca. 1,3 % über Anfangs- und Endspannung

#### Beispiel 9.11.25 — Wirk- und Blindleistung am Anfang der Freileitung bei Vollast (Seite 197)

Freileitung 380 kV, Endlast: S₂ = 660 MVA, cos φind = 0,8, U₂N = 380 kV (U₂ = 220 kV).

I₂ = 660 MVA / (3·220 kV) = 1.000 A · e^(−j36,9°) = (800 − j600) A.

Ergebnisse:
- U₁ = (264,5 + j58,9) kV = 271 kV · e^(j12,5°) → U₁N = 470 kV
- I₁ = (767 − j286) A = 820 A · e^(−j20,45°)
- S₁ = 3·271 kV·820 A · e^(−j32,95°) = (561 + j363) MVA → P₁ = 561 MW, Q₁ = 363 MVAr

Spannungsunterschied zwischen Anfang (470 kV) und Ende (380 kV) beträchtlich → ständige Spannungsregelung bei Laständerungen notwendig.

#### Beispiel 9.11.26 — Kondensatorleistung zur Spannungsreduktion (Seite 198)

Kompensation der induktiven Blindleistung des Verbrauchers auf cos φ = 0,95:
- QL = 660 MVA · 0,6 = 396 MVAr
- Zielblindleistung: Q'L = 528 MW · tan(18,2°) = 174 MVAr
- Kondensatorleistung: QC = 396 − 174 = 222 MVAr
- Neuer Verbraucherstrom: I₂ = 842 A · e^(−j18,2°) = (800 − j264) A

#### Beispiel 9.11.27 — Leitungsparameter einer 20-kV-Freileitung (Seite 199)

Gegeben: 20-kV-Freileitung, l = 8 km, A = 70 mm² Al/St.
Leitungskonstanten: R' = 0,435 Ω/km, X' = 0,36 Ω/km, C' = 10,04 nF/km.
Last am Leitungsende: SL = 2,5 MVA, PL = 1,8 MW, U₂ = 20,2 kV.

Berechnete Leitungsparameter:
- R = 8·0,435 = 3,48 Ω
- X = 8·0,36 = 2,88 Ω
- C = 8·10,04 = 80,32 nF, XC = 1/(ω·C) = 39,63 kΩ

Lastgrößen:
- IL = 2,5 MVA / (√3·20 kV) = 72,17 A
- cos φ = 1,8/2,5 = 0,72 → φ = 43,95°
- Iw = 51,96 A, Ib = √(72,17² − 51,96²) = 50,09 A

Spannungsfall:
- Komplexer Spannungsfall: Uz = IL · √(R² + X²) = 326 V · e^(j43,95°)
- Längsspannungsfall: Uzl = Iw·R − Ib·X = 51,96·3,48 − 50,09·2,88 = 325,08 V (korrekter Wert: Iw·R + Ib·X mit korrekten Vorzeichen)
- Relativer Längsspannungsfall: ul = 325,08 / (20 kV/√3) = 2,82 %
- Spannung Leitungsanfang: U₁ = 20,2 kV + √3·325,08 V = 20,76 kV
- Exakte Berechnung: U₁ = √((U₂ + Uzl·√3)² + (Uzq·√3)²) = 20,763 kV
- Querspannungsfall: Uzq = 24,69 V
- Spannungswinkel: φ = arctan(24,56/(20.200 + 325,08)) = 0,071°

#### Beispiel 9.11.28 — Leitungsparameter eines 110-kV-Ölkabels (Seite 200–201)

Gegeben: 110-kV-Einleiter-Ölkabel, l = 30 km, A = 240 mm² Al/St.
R' = 0,138 Ω/km, X' = 0,148 Ω/km, C'b = 0,31 µF/km.
Last: SL = 100 MVA, PL = 100 MW (cos φ = 1), U₂ = 112 kV.

Berechnete Parameter:
- R = 30·0,138 = 4,14 Ω
- X = 30·0,148 = 4,44 Ω
- C = 30·0,31 = 9,3 µF, XC = 1/(ω·C) = 342,27 Ω, XC/2 = 648,54 Ω (je Leitungshälfte)

Lastgrößen:
- IL = 100 MVA / (√3·110 kV) = 524,86 A

Ohne Berücksichtigung der Kapazitäten:
- Uzl = R·Iw = 4,14·524,86 = 2172,92 V (da cos φ = 1, kein Blindstrom)
- U₁ = √((112 kV + Uzl·√3)² + (Uzq·√3)²) = 115,834 kV → U₁Y = 66,88 kV
- Relativer Spannungsfall: ul = 1,997 %

Mit Berücksichtigung der Betriebskapazitäten:
- Kapazitiver Strom: IXC/2 = (110 kV/√3) / 684,54 Ω = +j92,776 A
- Gesamtstrom: I = 524,86 − j92,776 = 533 A · e^(j10°)
- Uz = 533 A · e^(j10°) · 6,07 Ω · e^(j57°) = 3235 V · e^(j67°)
- Uzl = 1761,12 V, Uzq = 2713,96 V
- U₁ = 115,15 kV → U₁Y = 66,88 kV
- Relativer Spannungsfall: ul = 1761,12 V / (110 kV/√3) = 2,773 %
- Spannungswinkel: φ = arctan(2713,96 / (110 kV/√3 + 1761,12)) = 2,34°

#### Beispiel 9.11.29 — Vier Fälle des Leistungsfaktors (Seite 201)

Für eine zweipolige Leitung mit Wirkwiderstand RL und Reaktanz XL gilt allgemein:
ΔU = 2·RL·I·cos φ ± 2·XL·I·sin φ

Die vier Sonderfälle:
1. Rein ohmsch (φ = 0°, cos φ = 1): ΔU = 2·RL·I
2. Rein induktiv (φ = 90°, sin φ = 1): ΔU = 2·XL·I (positives Vorzeichen)
3. Rein kapazitiv (φ = −90°, sin φ = −1): ΔU = −2·XL·I (Spannungserhöhung)
4. Lastwinkel gleich Impedanzwinkel φL = φZ: Sonderfall für maximale Wirkleistungsübertragung

### Kapitel 9.12 — Zusammenfassung der Spannungsfallberechnung (Seiten 202–204)

#### Normen und Grenzwerte

- Zulässiger Spannungsfall ist zentrales Kriterium für ordnungsgemäße Funktion elektrischer Betriebsmittel
- NAV (Niederspannungsanschlussverordnung): maximal 3 % nach dem Zählerplatz
- DIN 18015-1:2007-09: maximal 3 % zwischen Messeinrichtung und Verbrauchsmittel — gilt ausschließlich für Wohngebäude oder ähnliche Bereiche
- DIN IEC 60364-5-52 (VDE 0100-520):2013-06 bzw. IEC 60364-5-52:2009: Empfehlungen in Abhängigkeit vom Anschlusspunkt und Verbrauchsmittel, unterschieden nach:
  - a) NS-Anlagen direkt aus öffentlichem Netz versorgt
  - b) NS-Anlagen aus privatem Versorgungsnetz versorgt
- DIN IEC 60038 (VDE 0175):2012-04: Bei automatisch geregeltem MS-Transformator kann am MS-Verteilungsknoten von einer Versorgungsspannung innerhalb der zulässigen Toleranz ausgegangen werden → maximal 10 % Spannungsfall von MS-Anschlussklemmen des Verteilungsnetztransformators bis Verbraucheranlage verfügbar
- Untergrenze: Verbraucherspannung soll unter Normalbedingungen nicht mehr als 4 % unter der Bemessungsspannung liegen
- Motorische Verbraucher im stationären Betrieb: maximaler Spannungsfall über Anschlusskabel häufig auf 2 % begrenzt, um sicheren Motoranlauf zu gewährleisten

#### Methodische Hinweise

- Spannungsfallberechnung ist ein iterativer Prozess zur Modellierung des Leistungsflusses an jedem Netzknoten
- Verbraucher werden als PQ-Knoten (Wirk-/Blindleistung) oder Slack-Knoten (Spannung Betrag/Winkel) abgebildet
- Unterschiedliche Formeln und Vorgehensweisen möglich; Normen können keine Berechnungsmethode vorschreiben, nur Grenzwerte angeben
- Messung der Vorimpedanzen oder Kurzschlussströme vor Ort empfohlen; Annahmen führen häufig zu falschen Ergebnissen
- Alternative Methode: Berechnung des Spannungsfalls aus Kabeldaten (R- und X-Beläge) mit Bemessungsstrom der Schutzeinrichtung und Impedanzwinkel — ohne Kenntnis des tatsächlichen Betriebsstroms und Leistungsfaktors
- Messungen zeigen: Anlagen zeigen zunehmend kapazitives Verhalten → Spannung am Anschlusspunkt wird erhöht
- Größere Leistungsfaktoren bei 50 Hz und kleineren Leitungsquerschnitten liefern günstigere Ergebnisse; induktive Widerstandsbeläge spielen bei Niederspannungsleitungen kaum eine Rolle
- Spannungsfallkoordination muss für jeden Stromkreis projektspezifisch festgelegt werden; Spannungsfallwerte sollten ausdrücklich in Ausschreibungen und Verträgen vereinbart werden, um spätere Rechtsstreitigkeiten zu vermeiden

#### Literatur (Kapitel 9)

1. I. Kasikci: Sechsteiliger Fachbeitrag „Zulässige Längen von Kabeln und Leitungen nach Beiblatt 5" der DIN VDE 0100, 2017–2018
2. I. Kasikci, N. Pantenburg: VDE-Seminar-Projektierung von Niederspannungsanlagen, Offenbach, 2018
3. I. Kasikci, N. Pantenburg: Koordination des Spannungsfalls in Niederspannungsnetzen Teil 1 und 2, 2015
4. I. Kasikci: Projektierung von Niederspannungsanlagen, 3. Auflage, Hüthig-Pflaum-Verlag, 2010, ISBN 978-3-8101-0274-4
5. A.J. Schwab: Elektroenergiesysteme, 5. Auflage 2017, ISBN 978-3-662-55315-2
6. DIN VDE 0100-520 (VDE 0100-520:2013-06): Errichten von Niederspannungsanlagen — Teil 5-52: Auswahl und Errichtung elektrischer Betriebsmittel
7. D. Oeding, B.R. Oswald: Elektrische Kraftwerke und Netze, 8. Auflage 2017, ISBN 978-3-662-52702-3
8. ABB: ABB Schaltanlagen Handbuch, 12. Auflage, Cornelsen, ISBN 3-589-24112-8
9. Beiblatt 2 zu DIN VDE 0100-520: Zulässige Strombelastbarkeit, Schutz bei Überlast, maximal zulässige Kabel- und Leitungslängen zur Einhaltung des zulässigen Spannungsfalls und der Abschaltbedingungen
10. Beiblatt 5: Zulässige Längen von Kabeln und Leitungen unter Berücksichtigung des Schutzes bei indirektem Berühren, des Schutzes bei Kurzschluss und des Spannungsfalls

---

### Kapitel 10 — Strombelastbarkeit von Kabeln und Leitungen (ab Seite 205)

Relevante Normen: DIN VDE 0100 Teil 430, DIN VDE 0298 Teil 4, DIN VDE 0276 Teil 1000, DIN VDE 0276 Teil 603.

Grundsatz: Kabel und Leitungen müssen gegen Überlast und Kurzschluss geschützt sein. Die Strombelastbarkeit wird durch Verlegeart, Umgebungstemperatur und Häufung bestimmt.

Schutzeinrichtungen müssen so gewählt und koordiniert sein, dass Schutz sowohl im Normalbetrieb als auch im Fehlerfall sichergestellt ist.

Bemessungsgrundlagen: Überlastschutz, Kurzschlussschutz, Strombelastbarkeit unter Verlegebedingungen und Spannungsfall müssen gemeinsam berücksichtigt werden.

#### 10.1 Schutz bei Überlast

Für die Koordination von Leitern und Überstromschutzeinrichtungen müssen zwei Bedingungen erfüllt sein:

**Nennstromregel (Gl. 10.1):**
IB ≤ In ≤ Iz

**Auslöseregel (Gl. 10.2):**
I₂ ≤ 1,45 · Iz

Dabei bedeuten:
- IB = Betriebsstrom in A (vorgesehener Betriebsstrom zur Bestimmung der Mindest-Dauerbelastbarkeit, abhängig von Art, Gebrauchsdauer und Anzahl der Verbraucher)
- In = Nennstrom der Schutzeinrichtung in A
- Iz = zulässige Strombelastbarkeit des Leiters in A
- I₂ = Auslösestrom in A (muss vom Hersteller angegeben oder in Produktnormen festgelegt sein)

#### 10.2 Beispiel: Schutz bei Überlast

Verbraucher: P = 100 kW, cos φ = 0,8. Kabel Verlegeart C, l = 45 m.

Betriebsstrom: IB = P / (√3·Un·cos φ) = 100 kW / (√3·400 V·0,8) = 180 A.

Dimensionierung nach DIN VDE 0100 Teil 430:
- Gewählte Sicherung: In = 200 A
- Zulässige Strombelastbarkeit aus Tab. 10.2: Iz = 223 A

Nennstromregel: 180 A ≤ 200 A ≤ 223 A ✓

Auslöseregel (für Sicherung, I₂ = 1,6·In):
- 1,6·200 A = 320 A ≤ 1,45·223 A = 323,35 A ✓

Ergebnis: Überlastschutz erfüllt.

#### 10.3 Schutz bei Kurzschluss

Der unbeeinflusste Kurzschlussstrom ist an jeder relevanten Stelle der Anlage zu bestimmen — durch Berechnung oder Messung. Am Speisepunkt kann er beim Netzbetreiber erfragt werden.

Für Kurzschlüsse bis einschließlich 5 s Dauer gilt die zulässige Ausschaltzeit (Gl. 10.3):

tzu = (k · S / I''k1min)²

Dabei:
- tzu = zulässige Ausschaltzeit bzw. Kurzschlussdauer in s
- I''k1min = kleinster Kurzschlussstrom (Fehlerstrom) in A
- k = Materialbeiwert (spezifischer Leiterfaktor) in A·√s/mm²: PVC-Leiter Cu: 115, Al: 76
- S = Leiterquerschnitt in mm²

Für Ausschaltzeiten < 100 ms gilt stattdessen der Stromwärmevergleich (Gl. 10.4):
A² · J²thr > I² · ta

Die Schutzeinrichtungen (ÜSE = Überstromschutzeinrichtungen) und ihre Auslöseströme nach Tab. 10.1:

| Charakteristik | Thermischer Auslöser I₂ | Magnetischer Auslöser I₅ |
|---|---|---|
| Z | 1,2·In | 3·In |
| A | 1,45·In | 3·In |
| B | 1,45·In | 5·In |
| C | 1,45·In | 10·In |
| D | 1,45·In | 20·In |
| K | 1,2·In | 15·In |
| E | 1,2·In | 6,25·In |

Die Ausschaltzeit der ÜSE (ta) darf die maximal zulässige Ausschaltzeit (tzu) nicht überschreiten.

#### 10.4 Beispiel: Schutz bei Kurzschluss

Kabel 50 mm² Cu, Kurzschlussstrom am Leitungsende I''k1 = 4,5 kA.

Nachweis der Kurzschlussfestigkeit:
tzu = (k·S / I''k1)² = (115·50 / 4500)² = (1,278)² = 1,63 s

Da Ausschaltzeit der Schutzeinrichtung kleiner als 1,63 s sein muss — bei üblichen Schutzeinrichtungen erfüllt.

#### 10.5 Strombelastbarkeit

##### 10.5.1 Belastbarkeit im ungestörten Betrieb

Die zulässige Strombelastbarkeit ergibt sich durch Korrekturfaktoren aus der Tabellengröße (Gl. 10.5–10.7):

Iz = Ir · f1 · f2 · … · fn

Iz = Ir · Πf

Iz ≥ IB

Dabei:
- Iz = tatsächliche Strombelastbarkeit unter Betriebsbedingungen in A
- Ir = Tabellen-Belastbarkeit bei Standardbedingungen in A
- f1 = Korrekturfaktor für abweichende Temperatur
- f2 = Korrekturfaktor für Häufung
- … fn = weitere Korrekturfaktoren (z.B. vieladrige Leitungen)
- IB = Belastung im ungestörten Betrieb

Normbasis der Tabellen: DIN VDE 0298 Teil 4 „Empfohlene Werte für die Strombelastbarkeit von Kabeln und Leitungen für feste Verlegung in Gebäuden und von flexiblen Leitungen" sowie DIN VDE 0276 Teil 1000 „Strombelastbarkeit, Allgemeines, Umrechnungsfaktoren".

**Tab. 10.2** gilt für: Kabel und Leitungen, Verlegearten A1, A2, B1, B2 und C, Leiter Cu oder Al, Betriebstemperatur 70 °C, Umgebungstemperatur 30 °C. Weitere Verlegearten: DIN VDE 0298-4.

**Tab. 10.3** gilt für: Verlegearten D, E, F und G, Leiter Cu oder Al, Betriebstemperatur 70 °C, Umgebungstemperatur 30 °C in Luft, 20 °C im Erdboden. Quelle: DIN VDE 0298:2003-08.

**Tab. 10.4**: Umrechnungsfaktoren für Häufung — auf der Wand, im Rohr und Kanal, auf dem Fußboden und unter der Decke. Quelle: DIN VDE 0298:2003-08.

**Tab. 10.5**: Umrechnungsfaktoren für Häufung von mehradrigen Kabeln und Leitungen auf Kabelwannen und -pritschen. Quelle: DIN VDE 0298:2003-08.

##### 10.5.2 Beispiel: Zuleitung einer Verteilung

Gegeben: IB = 170 A, In = 200 A gG/NH00, Verlegeart C (ein- oder mehradrige Kabel/Mantelleitungen frei auf der Wand), 3 belastete Adern, Umgebungstemperatur 25 °C, Häufung: 2 Systeme.

Korrekturfaktoren: f1 (Temperatur) = 1,06, f2 (Wandverlegung, 2 Kabel) = 0,94.

Aus der Bemessungsregel:
Iz = In / (f1·f2) = 200 / (1,06·0,94) = 200,72 A

Aus der Auslöseregel:
Iz = I₂ / (1,45·f1·f2) = (200·1,6) / (1,45·1,06·0,94) = 220,68 A

Maßgebende Iz = 220,68 A → aus Tab. 10.2, Spalte 11: Kabeltyp NYY-J 4×95 mm² mit Ir = 223 A.

##### 10.5.3 Beispiel: Kabelbemessung eines Motors

Drehstrommotor direkt an Hauptverteilung. Verlegung auf Kabelpritsche mit 5 nebeneinanderliegenden Kabeln. Umgebungstemperatur 45 °C.

Vorgehen:
- Aus Tab. 10.3: Basisstrombelastbarkeit bei direkter Verlegung: Ir = 96 A → Querschnitt 25 mm²
- Korrekturfaktor für Häufung (5 Kabel auf Pritsche): f1 = 0,79 (Tab. 10.5)
- Korrekturfaktor für Temperatur (45 °C): f2 = 0,79 (Tab. 10.6)
- Tatsächliche Belastbarkeit: Iz = 96·0,79·0,79 = verringert → Querschnitt muss erhöht werden
- Vollständige Bemessung mit und ohne Korrekturfaktoren in Tab. 10.9 dargestellt

##### 10.5.4 Beispiel: Überprüfung der Stromwärmewerte

Ausschaltzeit der Sicherung < 100 ms → Stromwärmevergleich nach Gl. 10.4 erforderlich.

Kabel 3×70 mm²:
- Zulässiger Stromwärmewert: A²·J²thr = 6,48·10⁷ A²·s
- Durchlasswert 125-A-Sicherung: 9,13·10⁴ A²·s

Da 6,48·10⁷ A²·s >> 9,13·10⁴ A²·s ist Gl. 10.4 erfüllt.

#### 10.6 Thermische Kurzschlussfestigkeit

Nach DIN VDE 0103 gilt für die thermische Kurzschlussfestigkeit elektrischer Betriebsmittel:

Thermischer Äquivalenzkurzschlussstrom (Gl. 10.8):
Ith = I''k · √(m + n)

Wärmewirkung des Gleichstromglieds (Gl. 10.9):
m = (1 / (2·Tk·ln(κ − 1))) · [e^(4·f·Tk·ln(κ−1)) − 1]

Für Kurzschlussdauer Tk > 1 s kann m = 0 gesetzt werden.

Der Faktor n ist die Wärmewirkung der Wechselstromkomponente. Bei generatorferner Einspeisung: n = 1.

Bedingung für ausreichende thermische Kurzschlussfestigkeit (Gl. 10.10):
Für Tk ≤ Tkr gilt: Ith ≤ Ithr
