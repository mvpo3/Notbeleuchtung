# Planung von Elektroanlagen — Teil 4
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 161-200.

Dieser Abschnitt behandelt vollständig das Kapitel 9 zur Spannungsfallberechnung in elektrischen Netzen: mathematische Grundlagen, Näherungsgleichungen und deren Fehleranalyse, Berechnungsmethoden für Gleich-, Wechsel- und Drehstromnetze (NS und HS), zulässige Grenzwerte nach TAB/VDE/NAV, Grenzlängenbedingungen für Schutzmaßnahmen sowie eine umfangreiche Sammlung an durchgerechneten Praxisbeispielen für verschiedene Netztypen und Spannungsebenen.

## Inhalt

### Spannungsfall bei kapazitiver Last und Ferranti-Effekt

- Bei kapazitiver Last (z. B. Kondensatoren, PV-Anlagen mit Überkompensation) dreht das Spannungsdreieck die Richtung — Vorzeichen in Längs- und Querspannungsfall-Gleichungen wechseln.
- Beim Ferranti-Effekt steigt die Spannung am Leitungsende über die Spannung am Anfang an.
- Laut DIN VDE 0100 Beiblatt 5 darf der induktive Anteil X bei Kabeln/Leitungen bis 16 mm² in NS-Anlagen vernachlässigt werden, da gilt X << R.
- Folge: In der NS-Ebene ist der Längsspannungsfall (Ul) die maßgebende Größe; der Querspannungsfall (Uq) ist vernachlässigbar klein.
- Der Längs- und Querspannungsfall entstehen durch den Wirk- und Blindanteil des Stroms:
  - Ul = I · R · cos φ (Längsspannungsfall)
  - Uq = I · X · sin φ (Querspannungsfall)
  - Bei cos φ = 1 vereinfacht sich zu: Ul = I · R
- Blindleistungsursachen im Überblick:
  - Induktiver Blindleistungsbedarf: Motoren, Transformatoren, Freileitungen, Kabel
  - Kapazitive Blindleistungserzeugung: Kondensatoren, Freileitungen, Kabel im Leerlauf
  - Blindleistungen verursachen Verluste, größere Betriebsmittelauslegung, Spannungsänderungen und Spannungsverdrehung
- Merksatz: Induktiver Strom → Spannungsfall (Ib negativ); kapazitiver Strom → Spannungserhöhung (Ib positiv)

### Fehler der Näherungsgleichung (U-Näherung)

- Das Dreiphasensystem lässt sich durch eine π-Schaltung mit den Elementen Wirkwiderstandsbelag R'L (bei 20 °C), induktivem Blindwiderstandsbelag X'L und Betriebskapazität Cb beschreiben; Cb ist wegen geringen Betrags vernachlässigbar.
- Allgemeine Näherungsgleichung für Spannungsfall zwischen Anfang A und Ende E:
  - ΔU = R'L · l · I · cos φ + X'L · l · I · sin φ
- Exakter Spannungsunterschied: ΔUExakt = |UA| − |UE|
- Spannung am Leitungsanfang (exakt):
  - UA = √[(UE + ΔU)² + (X'L · l · I · cos φ − R'L · l · I · sin φ)²]
- Leitungswinkel δ: sin δ = (X'L · l · I · cos φ − R'L · l · I · sin φ) / UA
- Differenzbetrag: ΔUDif = ΔUExakt − ΔU = UA · (1 − cos δ)
- Fehler der Näherungsgleichung: F = (ΔUDif / ΔU) · 100 %
- Der Fehler ist im Bereich cos φ = 1 bis 0,7 gering.

### Cosinussatz (Kapp'sches Dreieck)

- Allgemeiner Cosinussatz für Dreieck mit Seiten a, b, c und Winkel γ gegenüber Seite c:
  - c² = a² + b² − 2 · a · b · cos γ
- Elektrische Ersetzung: a = ULast, b = ULeitung, c = U0, γ = δLast − δLeitung
- Daraus lösbares quadratisches Problem ergibt die Lastspannung:
  - ULast 1/2 = ULeitung · cos(δLast − δLeitung) ± √[(ULeitung · cos(δLast − δLeitung))² − ULeitung² + U0²]

### Unsymmetrische Netze (Vierleiternetz)

- Im Vierleiternetz werden Einphasenverbraucher zwischen Außenleiter und Neutralleiter angeschlossen.
- Unterschiedliche Verbraucherleistungen → unsymmetrische Stromverteilung → Neutralleiterstrom In.
- In den Leitern (a, b, c) entstehen unterschiedliche Spannungsfälle:
  - Leiter-Neutralleiter-Spannungsfälle:
    - Una − Un'a' = Ia · Za + In · Zn
    - Unb − Un'b' = Ib · Zb + In · Zn
    - Unc − Un'c' = Ic · Zc + In · Zn
  - Leiter-Leiter-Spannungsfälle:
    - Uba − Ub'a' = Ia · Za + Ib · Zb (usw.)

#### Rechenbeispiel: Unsymmetrische Verbraucher (Abschn. 9.1.4)
- Gegebene Impedanzen und Ströme (Betragswinkel-Form):
  - Za = 1,2 ∠44° Ω, Ia = 100 ∠−20° A
  - Zb = 1,1 ∠47° Ω, Ib = 90 ∠−130° A
  - Zc = 1 ∠45° Ω, Ia = 80 ∠90° A
  - Zn = 0,5 ∠40° Ω, In = 43,2 ∠−88,8° A
- Errechnete Spannungsfälle:
  - Una − Un'a' = 120 ∠24° + 21,6 ∠7,8° = (126,4 + j61,9) V
  - Un'a' = 230 V − (126,4 + j61,9) V = (103,6 − j61,9) V
  - Unb − Un'b' = (65,8 + j76,6) V
  - Un'b' = 230 V − (65,8 + j76,6) V = (164,2 + j76,6) V

### Rechenbeispiele Hochspannungs-Leitungen

#### Beispiel: 20-kV-Freileitung (Abschn. 9.1.5)
- Daten: 20-kV-Freileitung, l = 8 km, A = 70 mm² Al/St
  - R' = 0,435 Ω/km, X' = 0,36 Ω/km, C' = 10,04 nF/km
  - Scheinlast SL = 2,5 MVA, Wirkleistung PL = 1,8 MW
- Berechnete Werte:
  - R = 3,48 Ω, X = 2,88 Ω, C = 80,32 nF, XC = 39,63 kΩ
  - IL = 72,17 A, cos φ = 0,72 (φ = 43,95°)
  - Iw = 51,96 A, Ib = 50,09 A
  - Längsspannungsfall: Ul = Iw · R − Ib · X = 51,96 · 3,48 + 50,09 · 2,88 = 325,08 V
  - Relativer Längsspannungsfall: ul = 325,08 V / (20 kV/√3) · 100 % = 2,82 %
  - Außenleiterspannung (näherungsweise): U1 = 20 kV + √3 · 325,08 V = 20,76 kV
  - Exakte Berechnung: UA = √[(20 kV + 325,08 V · √3)² + (Uq · √3)²] = 20,763 kV
  - Querspannungsfall: Uq = Iw · X + Ib · R = 24,67 V
  - Spannungswinkel: φ = arctan(24,56 V / (20 kV + 325,08 V)) ≈ 0,071°

#### Beispiel: 20-kV-Leitung mit Konstantstrom (Abschn. 9.1.6)
- Daten: I = 380 A, l = 20 km, R' = 0,101 Ω/km, X' = 0,135 Ω/km, cos φ = 0,95, sin φ = 0,32
- Längsspannungsfall: Ul = √3 · 380 A · 20 km · (0,101 · 0,95 + 0,135 · 0,32) = 1,831 kV
- Querspannungsfall: Uq = √3 · 380 A · 20 km · (0,135 · 0,95 − 0,101 · 0,32) = 1,262 kV
- Gesamtspannungsfall: ΔU = 20 kV − √[(20 kV − 1,831 kV)² + 1,262 kV²] = 1787 V

#### Beispiel: 10-kV-Leitung (Abschn. 9.1.7)
- Daten: 10 kV, l = 10 km, R' = 0,319 Ω/km, X' = 0,330 Ω/km, P = 1 MVA, cos φ = 0,8
- Verbraucherstrom: I2 = (46,19 − j34,64) A
- Längsspannungsfall: ΔU = Iw · RL − Ib · XL = 46,19 · 3,19 − 34,64 · 3,3 = 33,03 V
- Relativer Spannungsfall: u = 33,03 V / (10 kV/√3) · 100 % = 0,572 %
- Spannungswinkel: δ = arcsin[(XL · Iw − RL · Ib) / (U2 + Ul)] = 0,4137°

### Berechnungsgleichungen NS-Anlagen (Abschn. 9.3)

- Spannungsfall = Differenz Leitungsanfangsspannung − Leitungsendspannung (nach Ohm'schem Gesetz)
- Normen: DIN VDE 0100 Teil 520, TAB, DIN 18015, NAV
- Bei Querschnitten bis 25 mm²: Berechnung nur mit Gleichstromwiderstand zulässig
- Bei Querschnitten über 25 mm²: induktiver Blindwiderstand zu berücksichtigen
- Bemessungstemperatur: 30 °C

#### Gleichstrom (Abschn. 9.3.2)
- Leitungswiderstand: RL = 2 · l / (κ · S)
- Spannungsfall: ΔU = 2 · l · I / (κ · S)
- Bei mehrfach belasteter Leitung (gleicher Querschnitt): ΔU = 2 · Σ(I · l) / (κ · S)

#### Einphasenwechselstrom (Abschn. 9.3.3)
- Spannungsfall für einen Abgang: ΔU = 2 · l · I · cos φ / (κ · S)
- Mit mittlerem Leistungsfaktor cos φm: ΔU = 2 · l · I · cos φm / (κ · S)
- Mit Lastmomenten (P · l): ΔU = 2 · Σ(P · l) / (κ · S · U0)

#### Drehstrom (Abschn. 9.3.4)
- Allgemeine Formel (symmetrische Last): ΔU = √3 · I · l · (R'L · cos φ + X'L · sin φ)
- Relativer Spannungsfall: u = √3 · In · l · (1/(κ·S) · cos φ + X'L · sin φ) / Un · 100 %
- Vereinfacht (bis 16 mm², induktiver Anteil vernachlässigt): ΔU = √3 · l · I · cos φ / (κ · S)
- Prozentualer Spannungsfall: u = ΔU / Un · 100 %
- Mehrere Abzweige: u = (R'l + X'l · tan φ) · 100 % / Un² · Σ(P · ln)
- Internationale Formeln für Drehstromnetze:
  - %e = 100 · P · L / (κ · S · Un²)
- Internationale Formeln für Wechselstromnetze:
  - %e = 200 · P · L / (κ · S · Un²)
- Für mehrere Abgänge:
  - %e = 0,074 · (P1·L1/S1 + P2·L2/S2 + ... + Pn·Ln/Sn)
- Für gemischte DS- und WS-Abgänge:
  - %e = 0,0124 · P·L/S + 0,074 · P·L/S

#### Ringleitung (Abschn. 9.3.5)
- Zweiseitig gespeiste Leitung, zur Berechnung wird als gestreckte Leitung aufgetrennt.
- Voraussetzungen: gleicher Leistungsfaktor, gleicher Querschnitt, gleiche Versorgungsspannung.
- Strom am Speisepunkt B: IB = Σ(ILast · L) / LAB
- Strom am Speisepunkt A: IA = ΣILast − IB
- Leistungsfluss: PA = Σ(P · l)B / l, PB = Σ(P · l)A / l

#### Strahlennetz (Abschn. 9.3.6)
- Bei konstantem Querschnitt und verschiedenen Verbrauchern:
  - ΔU = √3 · I · (Rw · cos φ + XL · sin φ)
  - u = √3 · I · (Rw · cos φ + XL · sin φ) / Un · 100 %
  - u = P · l · (R'w + X'L · tan φ) / U² · 100 %
- Verlustleistung: Pv = 3 · I² · Rw
- Gesamtspannungsfall für mehrere Abgänge a, b, c: u = ua + ub + uc

### Durchgerechnete NS-Beispiele

#### Beispiel: NS-Netz Hauptzuleitung (Abschn. 9.1.8)
- Daten: 400/230 V, 50 Hz, Erdkabel l = 150 m, NYY-J 4×120 mm²
  - R' = 0,184 Ω/km, X' = 0,08 Ω/km, PL = 150 kW, cos φ = 0,8
- Verbraucherstrom: I = 150 kW / (√3 · 400 V · 0,8) = 270,63 A
- Längsspannungsfall: Ul = √3 · 270,63 A · 0,150 km · (0,184 · 0,8 + 0,08 · 0,6) = 13,72 V
- Relativer Spannungsfall: u = 13,72 V / 400 V · 100 % = 3,43 %
- Querspannungsfall: Uq = √3 · 270,63 A · 0,150 km · (0,08 · 0,8 − 0,184 · 0,6) = −3,88 V
- Spannungswinkel: δ = arcsin(−3,88 V / (400 V + 3,46 V)) = −0,55° (alternativ arcsin(13,72/(400+3,46)) = 1,946°)

#### Beispiel: Spannungsfall mit Impedanzwinkel (Abschn. 9.1.9)
- Gleiche Leitung wie 9.1.8, aber Verwendung des Impedanzwinkels der Leitung (statt Leistungsfaktor des Verbrauchers):
  - u = √3 · 250 A · 150 m · (0,184 · 0,917 + 0,08 · 0,398) / (400 V) · 100 % = 3,25 %
- Verlustleistung: Pv = 3 · (270,63 A)² · 0,184 Ω/km · 0,150 km = 6,064 kW
- Verlustanteil: pv = 6,064 kW / 150 kW · 100 % = 4 %
- Übertragungswirkungsgrad: η = 150 kW / (150 kW + 6,064 kW) · 100 % = 96,11 %

#### Beispiel: NS-Verbraucher cos φ = 0,8 (Abschn. 9.1.10)
- Daten: 230 V, 50 Hz, 1,5 mm², l = 17 m, PL = 2,7 kW, cos φ = 0,8
- Strom: I = 2,7 kW / (230 V · 0,8) = 14,67 A
- Spannungsfall (vereinfacht, nur R): ΔU = 2 · 17 m · 14,67 A · 0,8 / (1,5 mm² · 56 m/(Ω·mm²)) = 4,75 V
- Relativer Spannungsfall: u = 4,75 V / 230 V · 100 % = 2,065 %
- Längsspannungsfall (mit induktivem Anteil, R' = 12,1 mΩ/m, X' = 0,115 mΩ/m):
  - Ul = 2 · 17 m · 14,67 A · (12,1·10⁻³ · 0,8 + 0,115·10⁻³ · 0,6) = 4,86 V → u = 2,11 %
- Querspannungsfall: Uq = 2 · 17 m · 14,67 A · (0,115·10⁻³ · 0,8 − 12,1·10⁻³ · 0,6) = −3,57 V
- Spannungswinkel: δ = arcsin(−3,57 / (230 + 4,86)) = −0,87°

#### Beispiel: NS-Verbraucher cos φ = 1 (Abschn. 9.1.11)
- Daten: 230 V, 50 Hz, l = 17 m, PL = 2,7 kW, cos φ = 1
- Strom: I = 2,7 kW / (230 V · 1) = 11,74 A
- Spannungsfall: ΔU = 2 · 17 m · 11,74 A · 1 / (1,5 mm² · 56) = 4,75 V → u = 2,06 %

#### Beispiel: Impedanzwinkel vs. Leistungsfaktor (Abschn. 9.1.12)
- Transformator: uRr = 1,2 %, ukr = 6 %
- Freileitung: Zk = (0,155 + j0,284) Ω/km
- Kabel: Zk = (0,153 + j0,080) Ω/km
- Umgeformte Gleichung: Ul = I · R · cos φ · (1 + X/R · tan φE)
- Tabelle Spannungsfallwinkel (Tab. 9.1) — Korrekturwerte bei unterschiedlichen Leistungsfaktoren:

| cos φE | tan φE | Trafo (δ=5°) | Freileitung (δ=1,82°) | Kabel (δ=0,52°) |
|--------|--------|--------------|----------------------|-----------------|
| 0,5    | 1,732  | 9,66         | 4,17                 | 1,9             |
| 0,6    | 1,33   | 7,65         | 3,43                 | 1,7             |
| 0,7    | 1,02   | 6,1          | 2,86                 | 1,53            |
| 0,8    | 0,749  | 4,75         | 2,37                 | 1,4             |
| 0,9    | 0,484  | 3,42         | 1,88                 | 1,25            |

- Schlussfolgerung: Große Impedanzwinkel und schlechte Leistungsfaktoren ergeben die höchsten Spannungsfallwerte; der Blindleistungsanteil ist maßgebend.

### Spannungsfallberechnung in HS-Anlagen (Abschn. 9.2)

- Ersatzschaltbild Freileitung: induktiver und kapazitiver Widerstand nachgebildet, Wirkwiderstand vernachlässigt.
- Leitungsgleichungen (Wellengleichung):
  - Ia = Ie · cosh(γ · l) + Ue/Zw · sinh(γ · l)
  - Ua = Ie · cosh(γ · l) + Ie · Zw · sinh(γ · l)
  - cosh(x) = (ex + e−x) / 2, sinh(x) = (ex − e−x) / 2
- Wellenwiderstand Zw = √[(R'w + jωL') / (jωC'b)] = Zw · e^(jφw)
- Verteilungskonstante γ = √[(R' + jωL') · (G' + jωC')] = α + jβ (Dämpfungsbelag α, Phasenbelag β)
- Spannungsfall am Leitungsanfang (vereinfacht):
  - U'a = U'e + Rw · I + jXL · I
  - Betriebsstrom: I = Pe / (√3 · Un · cos φe)
  - Längsspannungsfall: ΔU' = Rw · I · cos φe + XL · I · sin φe
  - Querspannungsfall: δU' = XL · I · cos φe − Rw · I · sin φe
- In Mittelspannungsanlagen (l ≤ 30 km) und NS-Anlagen hat der Querspannungsfall keine praktische Bedeutung → δU' = U'a − U'e gilt vereinfacht.

### Zulässige Spannungsfall-Grenzwerte

#### Nach TAB (Abschn. 9.4)
Für Wohnbereiche gilt (Tab. 9.2 — Werte nach Leistungsbedarf):

| Leistungsbedarf (kVA) | Maximaler Spannungsfall (%) |
|-----------------------|-----------------------------|
| bis 100               | 0,5                         |
| 100 bis 250           | 1,00                        |
| 250 bis 400           | 1,25                        |
| über 400              | 1,50                        |

- Allgemeine Formel: ΔU = √3 · In · l · cos φ / (κ · S)

#### Nach DIN VDE 0100 Teil 520 (Abschn. 9.5)
Maximaler Spannungsfall zwischen Verteilungsnetz und Anschlusspunkt eines Verbrauchsmittels (Tab. 9.3, DIN VDE 0100-520:2013-06, Tabelle G.52.1):

| Anlagentyp                                              | Beleuchtung (%) | Andere Verbrauchsmittel (%) |
|---------------------------------------------------------|-----------------|-----------------------------|
| a) NS-Anlagen direkt aus öffentlichem Netz versorgt     | 3               | 5                           |
| b) NS-Anlagen aus privatem Energieversorgungsnetz       | 6               | 8                           |

- Spalte a) gilt für Wohnungsbau, sofern DIN 18015 nicht vereinbart wird.
- Spalte b) gilt für Industrie und alle direkt von Transformator versorgten Anlagen.

#### Nach NAV § 13 (Abschn. 9.6)
- Laut Niederspannungsanschlussverordnung (NAV): In den Leitungen zwischen Ende des Hausanschlusses und dem Zähler darf der Spannungsfall — bezogen auf den Nennstrom der vorgeschalteten Sicherung — maximal 0,5 % betragen.

#### Berechnung des maximal zulässigen Spannungsfalls (Abschn. 9.7)
- Für Wohnbereiche: abhängig von der Leistung nach DIN 18015 Teil 1.
- Für andere Anlagen: DIN VDE 0100 Teil 520 fordert maximal 8 % Spannungsfall.
- Drehstrom-Formel:
  - ΔU = √3 · I · l · (R'L · cos φ + X'L · sin φ)
  - u (%) = √3 · I · l · (R'L · cos φ + X'L · sin φ) · 100 % / Un
  - Zulässige Leitungslänge: l = ΔU / [√3 · I · (R'L · cos φ + X'L · sin φ)]
- Mit Wirkleistungsangabe: Δu = Pw · l · (R'L · cos φ + X'L · sin φ) · 10³ / (Un · cos φ)
- Werte für cos φ und sin φ (Tab. 9.4):

| cos φ | sin φ |
|-------|-------|
| 1,0   | 0     |
| 0,9   | 0,436 |
| 0,8   | 0,6   |
| 0,7   | 0,714 |

- Wichtiger Hinweis: Das verfügbare Drehmoment eines Asynchronmotors sinkt quadratisch mit der Spannung. Bei 10 % Spannungsfall während des Anlaufs steht nur noch etwa das 1,8-fache Bemessungsmoment zur Verfügung (bei NS-Normmotoren).

### Grenzlänge für Schutzmaßnahmen (Abschn. 9.8)

- Schutzanforderungen nach DIN VDE 0100 Teil 410 (Abschnitt 413: Schutz durch Abschaltung).
- Bedingung: Querschnitt muss so bemessen sein, dass bei vollkommenem Kurzschluss (Außenleiter gegen Schutzleiter) mindestens der Abschaltstrom Ia der vorgeschalteten Überstromschutzeinrichtung (ÜSE) fließt.
- IT-System: Bei zweitem Isolationsfehler in zwei verschiedenen Außenleitern muss mindestens eine ÜSE auslösen.
- Im Fehlerfall muss gelten: I''kmin ≥ Ia (kleinster Kurzschlussstrom ≥ Abschaltstrom)
- Maximale Leitungslänge nach ÜSE für WS-Verbraucher (Drehstrom):
  - lz = c · Un · 10³ / (√3 · Ikerf · Zv) − 2 / z'l
- Für WS-Verbraucher (Einphasenwechselstrom):
  - lz = κ · S · 10³ · U0 · 10³ / (I''k1min − Zv) / 2·(κ/3)
- Vereinfacht nach DIN VDE 0100 Beiblatt 5:
  - lmax = lnorm · Un / IB
- Formelzeichen:
  - Ikerf = Abschaltstrom der ÜSE oder kleinster einpoliger Kurzschlussstrom (A)
  - z'l = Schleifenimpedanz der Leitung nach der ÜSE (mΩ/m)
  - U0 = Spannung gegen Erde (V)
  - lmax = maximale Leitungslänge (m)
  - lnorm = normierte Leitungslänge (m)
  - Un = Nennspannung der Anlage (V)
  - IB = Betriebsstrom (A)
  - κ = Leitwert (m/(Ω·mm²))
  - S = Leiterquerschnitt (mm²)
  - Zv = Vorimpedanz (mΩ)

### Grenzlänge aus Berührungsspannung (Abschn. 9.9)

- Der Spannungsfall am Schutzleiter durch den Abschaltstrom im Fehlerfall darf die zulässige Berührungsspannung UT nicht dauerhaft überschreiten.
- Grenzlänge für Berührungsspannung:
  - l = UT / (Ia · √((R'PE)² + (X'PE)²))

### Bedingungen für maximale Leitungslängen (Abschn. 9.10)

- Elektrische Anlagen müssen für Normal- und Fehlerbetrieb ausgelegt sein (sicherheits- und funktionstechnisch).
- Maßgebende Bedingungen:
  - Begrenzung des maximal zulässigen Spannungsfalls
  - Einhaltung des Berührungsschutzes (Personensicherheit + Brandschutz)
  - Ausreichend großer Kurzschlussstrom im Fehlerfall
  - Zulässige Berührungsspannung am Schutzleiter im Fehlerfall
  - Sicherstellung von Überlast- und Kurzschlussschutz

#### Beispiel: Zulässige Kabellänge eines Motors (Abschn. 9.10.1)
- Kabel: NYY 3×70/35 mm², zulässiger Spannungsfall: 4 %, nach DIN VDE 0100 Beiblatt 5
- Normierte Länge für 1 A Bemessungsstrom: lnorm = 17,4 m (Tabelle A.23 DIN VDE 0100 Beiblatt 5)
- Bemessungsstrom des Motors: Ir = 81,1 A (Leistungsschild: 85 A)
- Berechnung der maximalen Kabellänge:
  - lmax = lnorm · Un / Ir · u% = 17,4 m · 400 V / 81,1 A · 4 % = 327,53 m
- Prüfung: Betriebslänge l ≤ 327,53 m → 4 % Spannungsfall eingehalten

#### Beispiel: Spannungsfall Motorzuleitung (Abschn. 9.10.2)
- Motor: 15 kW, 400 V, η = 0,84, cos φ = 0,85; Zuleitung: 65 m; zulässiger Spannungsfall: 3 %
- Aufnahmestrom:
  - S = 15000 W / (0,85 · 0,84) = 21008 VA
  - I = 21008 VA / (√3 · 400 V) = 30,32 A
- Querschnitt der Zuleitung:
  - S = √3 · 30,32 A · 65 m · 0,85 / (56 · 12 V) = 4,317 mm² → gewählt: 6 mm²
- Tatsächlicher Spannungsfall bei 6 mm²:
  - ΔU = √3 · 30,32 A · 65 m · 0,85 / (56 · 6 mm²) = 8,635 V
  - u = 8,635 V / 400 V · 100 % = 2,15 % (< 3 % → zulässig)
- Leistungsverlust:
  - PV% = √3 · 30,32 A · 65 m · 100 / (56 · 6 mm² · 400 V · 0,85) = 2,98 %

### Weitere Berechnungsbeispiele NS-Anlagen

#### Beispiel: Spannungsfall eines Stranges / Straßenverteilung (Abschn. 9.3.7)
- Last: 40 kW bei 125 m = 5000 kWm; 28 kW bei 210 m = 5880 kWm → Summe: 10880 kWm
- Widerstandsbeläge: R = 0,327 Ω/km, X = 0,319 Ω/km, cos φ = 0,8
- Spannungsfall im Endpunkt E:
  - ΔU = Σ(Pw · l) · (R · cos φ + X · sin φ) / (Un · cos φ)
  - ΔU = 10880 kWm · (0,327 · 0,8 + 0,319 · 0,6) / (400 V · 0,8) = 15,4 V
  - u = 15,4 V / 400 V · 100 % = 3,85 %

#### Beispiel: Spannungsfall Ringnetz (Abschn. 9.3.8)
- Netz mit 4 Lasten (9 kW bei 100 m, 12 kW bei 155 m, 25 kW bei 275 m, 18 kW bei 320 m), Gesamtlänge 420 m
- Verlagerung auf Einspeisung B:
  - Pw = (100·9 + 155·12 + 275·25 + 320·18) kWm / 420 m = 36,65 kW
- Lastmomente gesamt: 36,65 · 100 + 18,65 · 145 = 3665 + 2704,25 = 6369,25 kWm
- Spannungsfall: ΔU = 6369,25 kWm · (0,327 · 0,8 + 0,319 · 0,6) / (400 V · 0,8) = 9 V
- u = 9 V / 400 V · 100 % = 2,25 %

#### Beispiel: Bestimmung der Übertragungslänge (Abschn. 9.3.9)
- Daten: 100 kW, cos φ = 0,85, NAYY-J 4×150 mm², max. Spannungsfall 5 % (20 V)
- Widerstandsbeläge: R = 0,249 Ω/km, X = 0,080 Ω/km
- Maximale Leitungslänge:
  - l = Un · u · cos φ / (Pw · (R · cos φ + X · sin φ))
  - l = 400 V · 20 % · 0,85 / (100 kW · (0,249 · 0,85 + 0,080 · 0,52)) = 44,88 m

#### Beispiel: Wechselstrom-Motor (Abschn. 9.3.10)
- Daten: 230 V, cos φ = 0,8, I = 16 A, l = 30 m, NYM-J 3×1,5 mm²
- ΔU = 224 · 30 m · 16 A · 0,8 / (54 · 1,5 mm²) = 10,62 V → u = 10,62 V / 230 V · 100 % = 4,62 %

#### Beispiel: Freileitung (Abschn. 9.3.11)
- Daten: l = 200 m, 4×50 mm², I = 100 A, cos φ = 0,9, Al: κ = 34 m/(Ω·mm²), xL = 0,33 mΩ/m
- u = 173 · 200 m · 100 A / 400 V · (1,12 / (34 · 50) · 0,9 + 0,33/1000 · 0,44) = 6,4 %

#### Beispiel: Einspeisung zur Schule (Abschn. 9.3.12)
- Kabeltyp: NKBA 3×185/95 mm², l = 410 m, R = 0,105 Ω/km, X = 0,084 Ω/km, max. u < 5 %, cos φ = 0,9
- Zulässiger Strom: I = 20 V / (√3 · 410 m · (0,105 · 0,9 + 0,084 · 0,435)) = 215 A
- Übertragbare Scheinleistung: S = √3 · 400 V · 215 A = 149 kVA

#### Beispiel: Gebäudeversorgung (Abschn. 9.3.13)
- Berechnung des Gesamtspannungsfalls einer Gebäudeinstallation nach Abb. 9.15:
  - u = 0,124 · (94050 W · 30 m · 0,43 / 35 mm²) + 0,074 · (7536 W · 9 m / 10 mm² + 2500 W · 7 m / 2,5 mm²) = 1,43 % < 1,5 %
- Betriebsstrom: IB = 94050 W · 0,60 / (√3 · 400 V · 0,9) = 90,5 A < 155 A
- Kabelauswahl: NYY-J 3×35+25 mm²

#### Beispiel: Hauptverteilung 600 kW (Abschn. 9.3.14)
- Daten: 600 kW, l = 32 m (gerechnet mit 25 m), 4×120 mm²
- u = 100 · N · L / (κ · S · U²) = 100 · 600 kW · 25 m · 10³ / (56 · 120 mm² · 144400 V) = 0,412 % < 5 %

#### Beispiel: Straßenbeleuchtung (Abschn. 9.3.15)
- Querschnitt 10 mm², 220 V-Netz (220² = 48400 V²):
  - u = (200 / (56 · 10 · 48400)) · (55 · 1625 W + 362 m · 437 W) = 1,82 % < 5 %

#### Beispiel: Verlustberechnung (Abschn. 9.3.18)
- l = 0,15 km, R' = 0,184 Ω/km, Pe = 150 kW, cos φ = 0,8
- Verlustanteil: p = l · R'w · Pe / (Un² · cos²φ) · 100 % = 4,04 %
- Absolute Verluste: Pv = 4,04 % · 150 kW / 100 % = 6,06 kW

#### Beispiel: DS-Pumpenmotor (Abschn. 9.3.19)
- Motor: 7,5 kW Abgabeleistung, l = 105 m, Erdkabel 4×4 mm², η = 0,85, cos φ = 0,8
- Scheinleistung: S = 7500 W / (0,85 · 0,8) = 11029 VA
- Aufnahmestrom: I = 11029 VA / (√3 · 400 V) = 15,9 A
- Spannungsfall: ΔU = √3 · 105 m · 15,9 A · 0,8 / (56 Ω·mm²/m · 4 mm²) = 10,3 V
- Leistungsverlust: PV% = √3 · 105 m · 15,9 A · 100 % / (56 · 4 mm² · 400 V · 0,8) = 4 %

### Ringnetz — Querschnittsberechnung (Abschn. 9.3.17)
- Daten: Drei Lasten (10 kW bei 120 m, 30 kW bei 200 m, 40 kW bei 300 m), Gesamtlänge 620 m
- Lastaufteilung auf Einspeisung B:
  - Pb = (10 kW · 120 m + 30 kW · 200 m + 40 kW · 300 m) / 620 m = 63,75 kW
  - Pa = 90 kW − 63,75 kW = 26,25 kW
- Berechnung Einzellasten am Trennpunkt:
  - P2a = 26,25 − 20 = 6,25 kW; P2b = 63,75 − 40 = 23,75 kW; P2 = 30 kW
- Lastmomente (symmetrisch auf beide Seiten): je 3650 kWm
- Betriebsstrom: I = 63,75 kW / (√3 · 400 V · 0,8) = 115 A → Querschnitt 25 mm² ausreichend

### Hochspannungsbeispiele (Abschn. 9.11)

#### Beispiel: Energieübertragung 400 V vs. 220 kV (Abschn. 9.11.1)
- Übertragung: 2,3 MW über 5 km, cos φ = 0,8, zulässiger Spannungsfall 10 %
- Niederspannung 400 V:
  - I1 = 2,3 MW / (√3 · 400 V · 0,8) = 4149,7 A
  - RL1 = 40 V / 4149,7 A = 9,64 mΩ
  - Querschnitt: A1 = 5000 m / (56 · 9,64 mΩ) = 9262 mm² (wirtschaftlich nicht sinnvoll)
- Hochspannung 220 kV:
  - I2 = 2,3 MW / (√3 · 220 kV · 3 · 0,8) = 7,55 A
  - RL2 = 22000 V / 7,55 A = 2933,33 Ω
  - Querschnitt: A2 = 5000 m / (56 · 2933,33) = 0,0304 mm²
- Schlussfolgerung: Wirtschaftliche Übertragung über große Strecken erfordert hohe Spannung.

#### Beispiel: Modellberechnungen mit Admittanz-, T- und Pi-Modell (Abschn. 9.11.2)
- Daten: 40 MW, 220 kV, 125 km, 50 Hz, cos φ = 0,9
  - Z = (35 + j140) Ω, Y = 400 × 10⁻⁶ ∠90° Ω⁻¹
- Spannung gegen Erde: U1 = 220 kV / √3 = 127 kV
- Betriebsstrom: IR = 40 MW / (√3 · 220 kV · 0,9) = 116,6 A → IR = (104,9 − j50,72) A

**Admittanzmodell:**
- Kapazitiver Ladestrom: IC = j400 × 10⁻⁶ · 127 × 10³ = j50,8 A (∠90°)
- Leitungsstrom: IL = (104,9 − j0,08) A
- Spannungsfall: ΔU1 = (3660,3 + j14688,8) V
- Einspeisespannung: UE = 127000 V + ΔU1 = (130660 + j14688) V = 131,4 kV ∠6,37°
- Einspeisestrom: IE = 105 A ∠0,043°
- Leistungsfaktor am Einspeisepunkt: cos(6,37° − 0,043°) = 0,0993 (Hinweis: im Original unplausibel, vermutlich Druckfehler)
- Einspeiseleistung: PE = √3 · 227 kV · 105 A · 0,0993 = 41,2 MW
- Wirkungsgrad: η = 40 MW / 41,2 MW · 100 % = 97 %

**T-Modell:**
- Spannungsfall erste Leitungshälfte: ΔU1 = (5785 + j6455) V
- Spannung Leitungsmitte: UM = 127000 + (5785 + j6455) = (132785 + j6455) V
- Aufladungsstrom: IC = (−2,58 + j53,1) A
- Einspeisestrom: IE = (102,3 + j2,38) A
- Einspeisespannung: UE = 135 kV ∠5,72°
- Leistungsfaktor: cos(5,72° − 1,33°) = 0,997
- Einspeiseleistung: PE = √3 · 233,9 kV · 102,3 A · 0,997 = 41,32 MW
- Wirkungsgrad: η = 40 / 41,32 · 100 % = 96,8 %

**Pi-Modell:**
- Kapazitiver Strom am Leitungsende: I2C = j25,4 A
- Leitungsstrom: IL = (104,9 + j25,32) A
- Spannungsfall: ΔU1 = (7216,3 + j13799) V
- Einspeisespannung: UE = 134,9 kV ∠5,87°
- Aufladestrom Leitungsanfang: I1C = (2,76 + j26,84) A
- Einspeisestrom: IE = (102,14 + j1,52) A
- Leistungsfaktor: cos(5,87° − 0,852°) = 0,996
- Einspeiseleistung: PE = √3 · 233,6 kV · 102,14 A · 0,996 = 41,16 MW
- Wirkungsgrad: η = 40 / 41,16 · 100 % = 97,1 %

- Vergleich der drei Modelle: T- und Pi-Modell weichen geringfügig voneinander ab. Admittanzmodell ist weniger genau, aber schneller in der Berechnung. Modellwahl ist stark von der verfügbaren Rechenzeit abhängig.

#### Beispiel: Ersatzschaltbild 10-kV-Freileitung (10 km) (Abschn. 9.11.3)
- Daten: 10 kV, l = 10 km, Querschnitt 25/4 mm² (25 mm² Al, 4 mm² Stahl), Leiter nebeneinander
- Wirkwiderstandsbelag: R' = 32,5 / 25 = 1,3 Ω/km → R = 1,3 · 10 = 13 Ω
- Leiterabstand bei 10 kV: 0,8 m erforderlich; Leiterradius: 3,4 mm
- Mittlerer geometrischer Abstand: a = ³√(0,8 · 0,8 · 1,6 m) = 1,01 m
- Induktivitätsbelag: L' = 0,2 mH · ln(101 cm / 0,34 cm + 0,25) / km = 1,19 mH/km → L = 11,9 mH
- Induktiver Blindwiderstand: XL = ω · L = 2π · 50 · 11,9 mH = 3,74 Ω
- Betriebskapazitätsbelag: C'b = 55,6 nF / (ln(297) · km) = 9,75 nF/km → Cb = 97,5 nF
- Kapazitiver Strom: IC = ω · (Cb/2) · (UN/√3) = 314 · 49 · 10⁻⁹ · 10000/√3 = 89 mA
- Dauerbelastbarkeit der Leitung: 125 A → kapazitiver Strom vernachlässigbar
- Betriebskapazität kann in diesem Fall weggelassen werden; Ersatzschaltbild entspricht dann einer Drossel mit relativ hohem Wirkwiderstand.

#### Beispiel: Ersatzschaltbild 110-kV-Freileitung (100 km) (Abschn. 9.11.4)
- Daten: 110 kV, l = 100 km, Querschnitt 150/25 mm² (150 mm² Al, 25 mm² Stahl), Leiter nebeneinander
- Wirkwiderstandsbelag: R' = 32,5 / 150 = 0,216 Ω/km → R = 21,6 Ω
- Leiterabstand bei 110 kV: 3,6 m; Leiterradius: 8,55 mm
- Mittlerer geometrischer Abstand: a = ³√(3,6 · 3,68 · 7,2 m) = 4,53 m
- Induktivitätsbelag: L' = 0,2 mH · ln(453 cm / 0,853 cm + 0,25) / km = 1,3 mH/km → L = 0,13 H
- Induktiver Blindwiderstand: XL = 2π · 50 · 0,13 H = 40,9 Ω
- Betriebskapazitätsbelag: C'b = 55,6 nF / (ln(532) · km) = 8,9 nF/km → Cb = 0,89 μF
- Kapazitiver Strom: IC = 314 · 0,445 · 10⁻⁶ · 110/√3 kV = 8,9 A
- Dauerbelastbarkeit: 470 A → bei Belastung mit mindestens 20 % des zulässigen Dauerstroms kann Betriebskapazität vernachlässigt werden.
- Vergleich 10 kV / 110 kV: Induktivitäten und Kapazitäten je Leitungslänge weichen trotz mehr als zehnfach höherer Spannung nur geringfügig voneinander ab.

#### Beispiel: Verbraucherdaten, Spannung und Leistungsfaktor (Abschn. 9.11.5)
- Daten: 1 MVA bei cos φ = 0,8 (ind.), l = 10 km, Einspeisespannung 10,4 kV
  - R'L = 0,465 Ω/km, X'L = 0,34 Ω/km, X'C = 295 kΩ/km
- Verbraucher-Wirkleistung: P2 = 0,8 MW; Blindleistung: Q2 = 0,6 MVAr
- Leitungswiderstände: RL = 4,65 Ω, XL = 3,4 Ω
- Blindwiderstände der Betriebskapazitäten (Anfang und Ende parallel):
  - XC = 2 · 295 kΩ/km / 10 km = 59 kΩ
- Kapazitive Blindleistung am Leitungsende (bei geschätzter U2N ≈ 10 kV):
  - QC2 = (10 kV)² / 59 kΩ = 1,69 kVAr → gegenüber Q2 vernachlässigbar
- Vereinfachte Berechnung der Verbraucherspannung (ohne Querspannungsfall):
  - Gleichung: U1N = U2N + (P2 · RL + Q2 · XL) / U2N
  - 10,4 = U2N + (0,8 · 4,65 + 0,6 · 3,4) / U2N = U2N + 5,76 / U2N
  - Quadratische Gleichung: U²2N − 10,4 · U2N + 5,76 = 0
  - Lösung: U2N = 5,2 + √(27 − 5,76) = 5,2 + 4,61 = 9,81 kV
- Leitungsstrom: I1 = IL = I2 = 10⁶ VA / (√3 · 9,81 kV) = 58,75 A
- Spannungswinkel:
  - sin(δ) = (P2 · XL − Q2 · RL) / (U1N · U2N) = (0,8 · 3,4 − 0,6 · 4,65) / (10 · 9,81) = 0,0007 → δ ≈ 0,04°
  - Spannungen sind praktisch in Phase → Leistungsfaktor am Anfang = cos φ = 0,8 (wie am Ende)
- Scheinleistung am Leitungsanfang: S1 = √3 · 10,4 kV · 58,75 A = 1,06 MVA
