# Planung von Elektroanlagen — Teil 13
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 521-560.

Dieser Teil behandelt Kapitel 25 „Grundlagen elektrischer Maschinen" mit Schwerpunkt auf vollständigen Berechnungsbeispielen zu Transformatoren (Einphasen- und Drehstromtypen), Asynchronmaschinen (Betrieb, Steuerung, Anlauf, Frequenzumrichter), Wechselstrommotoren sowie Synchrongeneratoren (Inselbetrieb, Parallelschaltung, Leistungsdiagramm) und Gleichstrommaschinen (Grundgleichungen, Wicklungsarten, Nebenschlussmotor).

## Inhalt

### Transformator-Berechnungsbeispiele (Einphasen)

#### Vollständiges Ersatzschaltbild (Abschn. 25.4.10)
Messgrößen eines 230 V / 3 kVA Einphasentransformators im Leerlauf und Kurzschluss:
- Leerlaufverluste P₁₀ = 40 W, Leerlaufstrom I₁₀ = 1,5 A, Sekundärspannung U₂₀ = 115 V
- Kurzschlussspannung U₁ₖ = 21 V, Kurzschlussverluste P₁ₖ = 125 W

Berechnungsweg:
- Eisenverlustwiderstand: IFe = P₁₀ / U₀ = 40 W / 230 V = 0,174 A
- Magnetisierungsstrom: Iµ = √(I₁₀² − IFe²) = √(1,5² − 0,174²) = 1,489 A
- Hauptreaktanz: Xh = U₀ / Iµ = 230 V / 1,489 A = 154,46 Ω
- Eisenersatzwiderstand: RFe = U₀ / IFe = 230 V / 0,174 A = 1,32 kΩ
- Nennstrom primär: I₁ₙ = S / U₁ₙ = 3 kVA / 230 V = 13 A
- Leerlaufstromanteil: I₁₀ / I₁ₙ = 1,5 A / 13 A = 11,53 % von I₁ₙ
- Leerlauf-Leistungsfaktor: cosφ₁₀ = P₁₀ / (I₁₀ · U₁₀) = 40 W / (1,5 A · 230 V) = 0,116 → φ = 83°
- Kurzschluss-Leistungsfaktor: cosφₖ = Pₖ / (Iₖ · Uₖ) = 125 W / (13 A · 21 V) = 0,457 → φ = 62,8°
- Längsimpedanz Kurzschluss: Zₖ = Uₖ / Iₖ = 21 V / 13 A = 1,61 Ω
- Gesamter Wirkwiderstand: Rₖ = Zₖ · cosφ = 1,61 · 0,457 = 0,735 Ω → R₁ = R'₂ = 0,367 Ω
- Gesamte Streureaktanz: Xₖ = Zₖ · sinφ = 1,61 · 0,889 = 1,43 Ω → X₁σ = X'₂σ = 0,715 Ω
- Übersetzungsverhältnis: ü = 230 V / 115 V = 2
- Bezogene Kurzschlussspannung: uₖ = U₁ₖ / U₁ₙ = 21 V / 230 V = 9,13 %

#### Berechnungsbeispiel Einphasentransformator mit Magnetkreis (Abschn. 25.4.11)
Daten: Eisenkernquerschnitt A = 80×80 mm² = 6400 mm², korniertes Elektroblech, N₁ = 100, N₂ = 10, R₁ = 16 Ω, R₂ = 0,13 mΩ, BFe = 1,7 T.

Frage 1 – Hauptfluss:
- ΦH = BFe · AFe = 1,7 T · 6400·10⁻⁶ m² = 10,88 mWb

Frage 2 – Magnetische Feldstärke und Eisenpermeabilität:
- BFe = 1,7 T → aus Magnetisierungskennlinie folgt HFe = 150 A/m
- Eisenpermeabilität: µFe = BFe / HFe = 1,7 / 150 = 9019 · µ₀

Frage 3 – Gegeninduktivität:
- Mittlere Eisenweglänge: l = 4 × (450 − 80) mm = 1480 mm
- Magnetischer Leitwert: Λh = µFe · AFe / l
- M = N₁ · N₂ · Λh = 100 · 10 · (0,0113 · 6400·10⁻⁶ / 1480) = 48,86 mH

Frage 4 – Haupt-Induktivitäten:
- Primäre Hauptinduktivität: L₁h = (N₁/N₂) · M = (100/10) · 48,86 mH = 488,6 mH
- Sekundäre Hauptinduktivität: L₂h = (N₂/N₁) · M = (10/100) · 48,86 mH = 4,886 mH

Frage 5 – Streuinduktivitäten (Streuverhältnis σ = 0,001):
- Primäre Streuinduktivität: L₁σ = σ · L₁h = 0,001 · 488,6 mH = 0,4886 mH
- Sekundäre Streuinduktivität: L₂σ = σ · L₂h = 0,001 · 4,886 mH = 0,004886 mH

Frage 6 – T-Ersatzschaltbild (auf Primärseite umgerechnet):
- R'₂ = ü² · R₂ = (100/10)² · 0,13 mΩ → Wert gemäß Übersetzungsverhältnis
- L'₂h = ü² · L₂h = 488,6 mH
- Primäre Streureaktanz: X₁σ = 2π·f · L₁σ = 0,1535 Ω (bei 50 Hz)
- Hauptreaktanz: Xh = 2π·f · L₁h = 153,5 Ω
- Sekundäre Streureaktanz (umgerechnet): X'₂σ = ü² · X₂σ = 0,1535 Ω

#### Betriebsberechnungen desselben Transformators (Abschn. 25.4.12)
Nennspannung primär U₁N = 350 V, Nennstrom I₁N = 80 A.

Frage 1 – Nennscheinleistung: SN = U₁N · I₁N = 350 V · 80 A = 28 kVA

Frage 2 – Sekundäre Nennwerte:
- U₂N = U₁N / ü = 350 V / 10 = 35 V
- I₂N = I₁N · ü = 80 A · 10 = 800 A

Frage 3 – Primärer Leerlaufstrom:
- I₁₀ = U₁ / √(R₁² + (X₁σ + Xh)²) = 350 V / √(0,016² + (0,1535 + 153,5)²) = 2,28 A

Frage 4 – Sekundärspannung im Leerlauf:
- U'₂₀ = Xh · I₁₀ = 153,5 Ω · 2,28 A = 349,65 V → U₂₀ = 349,65 V / 10 = 34,97 V

Frage 5 – Kurzschlussströme:
- I₁ₖ = U₁ / √((R₁ + R₂)² + (X₁σ + X₂σ)²) = 350 V / √(0,029² + 0,307²) = 1135 A
- I₂ₖ = I'₁ₖ · ü = 1135 A · 10 = 11350 A

Frage 6 – Bezogene Kurzschlussspannung:
- uR = (R₁ + R'₂) · I₁N / U₁N = 0,029 · 80 / 350 = 0,0066
- uX = (X₁σ + X'₂σ) · I₁N / U₁N = 0,307 · 80 / 350 = 0,0702
- uₖ = √(uR² + uX²) = √(0,0066² + 0,0702²) = 0,0705

Frage 7 – Wirkungsgrad (PFe = 160 W, cosφ₂ = 1):
- Kupferverluste: PCu = (R₁ + R'₂) · I²₁N = 0,029 · 80² = 185,6 W
- Gesamtverluste: Pd = 185,6 W + 160 W = 345,6 W
- η = SN · cosφ₂ / (SN · cosφ₂ + Pd) = 28000 · 1 / (28000 + 345,6) = 98,7 %

#### Drehstromtransformator (Abschn. 25.4.13)
Daten: SrT = 160 kVA, 20 kV / 400 V, f = 50 Hz, Schaltgruppe Yyn6, Kernquerschnitt A = 130 mm², Flussdichte B = 1,6 T.

Frage 1 – Windungszahlen:
- Übersetzungsverhältnis: ü = U₁/U₂ = 50
- Hauptfluss: Φ = A · B = 0,013 m² · 1,6 T = 20,8 mWb
- Primärseite (Y): U₁ = U₁V / √3 = 20000 / √3 = 11550 V
  N₁ = U₁ / (√2 · 2π · f · Φ) = 11550 V / (√2 · 2π · 50 · 20,8·10⁻³) = 2500 Windungen
- Sekundärseite (y): U₂ = 400 V / √3 = 231 V
  N₂ = 231 V / (√2 · 2π · 50 · 20,8·10⁻³) = 50 Windungen

Frage 2 – Ströme und Stromdichten:
- Primärstrom: I₁N = SrT / (√3 · U₁N) = 160 kVA / (√3 · 20 kV) = 4,62 A
- Sekundärstrom: I₂N = SrT / (√3 · U₂N) = 160 kVA / (√3 · 400 V) = 231 A
- Primäre Kupferfläche ACu1 = 1,6 mm², Stromdichte J₁ = 4,62 A / 1,6 mm² = 2,89 A/mm²
- Sekundäre Kupferfläche ACu2 = 79 mm², Stromdichte J₂ = 231 A / 79 mm² = 2,92 A/mm²

Wicklungswiderstände (mittlere Windungslängen):
- Oberspannungsseite: lm,HV = (257 + 203) mm / 2 · π = 723 mm → R₁ = 0,723 m · 2500 / (57 · 1,6 mm²) = 19,82 Ω
- Unterspannungsseite: lm,LV = (173 + 148) mm / 2 · π = 504 mm → R₂ = 0,504 · 50 / (57 · 79) = 0,0056 Ω

Frage 3 – Ummagnetisierungsverluste (Verlustziffer ν = 0,45 W/kg bei 50 Hz, 1 T; Stahldichte ρ = 7900 kg/m³):
- Eisenvolumen: V = AFe · (3 · LK + 2 · LJ) = 0,013 · (3 · 0,48 + 2 · 0,72) = 0,0374 m³
- Eisenmasse: m = ρ · V = 7900 · 0,034 = 296 kg
- Eisenverluste: PFe = (BK/1T)² · ν · m = (1,6)² · 0,45 W/kg · 296 kg = 340 W

Frage 4 – T-Ersatzschaltbild (bezogene Größen auf Primärseite):
- Eisenersatzwiderstand: RFe = 3 · U²h / PFe = 3 · (11547 V)² / 340 W = 1176 kΩ
- Sekundärwiderstand umgerechnet: R'₂ = ü² · R₂ = 50² · 0,0056 Ω = 14 Ω
- Bemessungsimpedanz: ZN = U₁N / I₁N = 11550 V / 4,6 A = 2510 Ω
- Bezogene Strangwiderstände: r₁ = R₁/ZN = 19,8/2510 = 0,18 %; r'₂ = 14/2510 = 0,6 %; r₁ + r'₂ = 1,4 %
- Bezogene Streureaktanzen: x'₁σ = x'₂σ = 2 % → x₁σ + x'₂σ = 4 %
- Bezogene Eisenreaktanz: xFe = 46853 %; Hauptreaktanz: xh = 114860 %
- Hinweis: xFe und xh können außer im Leerlauf vernachlässigt werden → vereinfachtes Ersatzschaltbild für Nennbetrieb

---

### Asynchronmaschinen (Abschn. 25.5)

#### Grundprinzip
Asynchronmotoren (ASM) sind die in der Praxis am meisten eingesetzten Motortypen. Sie zeichnen sich durch Wartungsarmut, Robustheit und einfache Bauweise aus. Der Ständer trägt die ruhende Feldwicklung, die dreiphasig an ein Drehstromnetz angeschlossen ist. Der Läufer dreht sich mit einer Drehzahl, die gegenüber der Ständerdrehfeldfrequenz um den Schlupfwert zurückbleibt.

Vorteile:
- Hohe Schutzarten realisierbar
- Wartungsarm und kostengünstig
- Normierte Leistungsstufen und Bauformen

Nachteile:
- Fixe Drehzahlen (ohne Frequenzumrichter)
- Hohe Blindstromaufnahme
- Großer Anlaufstrom bei Direkteinschaltung

Das vollständige Ersatzschaltbild enthält Widerstände R₁ und R'₂ für Kupferverluste in Ständer und Läufer, RFe für Eisenverluste sowie Streufluss-Reaktanzen X₁σ und X'₂σ. Hauptgleichungen des Ersatzschaltbildes:
- U₁ = R₁ · I₁ + jX₁σ · I₁ + jXh · (I₁ + I'₂)
- U'₂ = R'₂ · I'₂ + jX'₂σ · I'₂ + jXh · (I₁ + I'₂)
- Uh = jXh · (I₁ + I'₂) = jXh · Im = j·ω·N₁·Φh

Bei kurzgeschlossenen Sekundärklemmen gilt: 0 = R'₂/s · I'₂ + jX'₂σ · I'₂ + jXh · (I₁ + I'₂), wobei R'₂/s = R'₂ + R'₂ · (1-s)/s.

#### Entstehung des Drehfeldes (Abschn. 25.5.2)
Das Ständerdrehfeld entsteht durch zwei notwendige Bedingungen:
1. Die drei Phasenströme müssen zeitlich um jeweils 120° gegeneinander verschoben sein.
2. Die Spulen müssen räumlich um je 120° versetzt angeordnet sein.

Das so entstehende Drehfeld ist räumlich rotierend, symmetrisch und kreisförmig.

#### Drehmomentverlauf (Abschn. 25.5.3)
Beim Hochlauf sinkt das Drehmoment zunächst, steigt dann auf den Maximalwert (Kippmoment), der bei 85–95 % der Nenndrehzahl erreicht wird. Drehleistung: P = M · ω = M · 2π · n.

Kloßsche Formel (Drehmoment-Schlupf-Beziehung):
M / Mₖ = 2 / (s/sₖ + sₖ/s)

#### Schlupf (Abschn. 25.5.4)
- Schlupf s = (n₁ − n₂) / n₁ · 100 %
- Läuferdrehzahl: n₂ = n₁ · (1 − s)
- Schlupfdrehzahl: ns = n₁ − n₂
- s ... Schlupf in %; n₁ ... synchrone Drehzahl in min⁻¹; n₂ ... Läuferdrehzahl in min⁻¹; ns ... Schlupfdrehzahl in min⁻¹
- Der Schlupf ist proportional zur Belastung und umgekehrt proportional zum Quadrat der Spannung.

#### Anlaufverfahren (Abschn. 25.5.5)
Stern-Dreieck-Anlasser als häufigste Methode zur Strombegrenzung beim Hochlauf:
- Überlastschutz liegt in Reihe mit der Ständerwicklung → Einstellung auf Phasenstrom = Bemessungsstrom / √3
- Kurzschlussschutz durch Sicherungen oder Motorschutzschalter (thermisch und magnetisch)
- Laut TAB 2012 können ohne Anmeldung angeschlossen werden:
  - Drehstrommotoren mit Anlaufstrom IA ≤ 60 A oder P ≤ 4 kW (Dreieck) bzw. P ≤ 12 kW (Stern-Dreieck)
  - Einphasenwechselstrommotoren mit IA ≤ 60 A oder P ≤ 1,4 kW

#### Steuerverfahren (Abschn. 25.5.6)
Drehzahl nach: n = (1 − s) · f₁ / p. Drei Steuerverfahren:
1. Schlupfvergrößerung
2. Änderung der Polzahl 2p
3. Frequenzänderung (mit Frequenzumrichter)

#### Motorwahl und Kenndaten (Abschn. 25.5.7)
Schutzart gemäß IEC-Publ. 34-5 (IP-Kennzeichnung, zwei Ziffern). Motorabmessungen hängen vom Drehmoment ab, nicht von der Bemessungsleistung. Netzspannung muss mit Motornenndaten übereinstimmen.

Typische Kenngrößen von Asynchronmaschinen:
| Kenngröße | Typischer Bereich |
|---|---|
| Anlaufstrom ILR | 3 ... 8 × IrM |
| Anlaufmoment MA | 1,5 ... 3 × MN |
| Kippmoment MK | 2 ... 3 × MN |
| Leerlaufstrom I₀ | 0,5 ... 0,8 × IN |
| Leistungsfaktor cosφ | 0,4 ... 0,9 |

#### Frequenzumrichter (Abschn. 25.5.8)
Aufbau: netzseitiger Gleichrichter → Gleichspannungszwischenkreis → maschinenseitiger dreiphasiger Wechselrichter. Der Wechselrichter schaltet die Zwischenkreisspannung nach dem Pulsweitenmodulationsverfahren (PWM) mit hoher Frequenz auf die Maschine.

Regelgesetze:
- Für konstantes Magnetfeld: Spannung proportional zur Frequenz (U ∼ f)
- Drehzahl proportional zur Frequenz: n = f · N / p

Leistungsgleichungen für Asynchronmaschinen:
- Aufgenommene Wirkleistung: Pzu = Pab / η
- Aufgenommene Scheinleistung: S = Pab / (η · cosφ)
- Aufgenommene Blindleistung: Q = Pab · tanφ / η
- Drehstromaufnahme: I = Pzu / (√3 · UrM · cosφ)
- Drehstrom-Wirkleistung: Pzu = √3 · U · I · cosφ; Pab = √3 · U · I · cosφ · η
- Einphasen-Wirkleistung: Pzu = U · I · cosφ; Pab = U · I · cosφ · η

---

### Wechselstrommotoren — Einphasenausführung (Abschn. 25.6)

Einphasenwechselstrommotoren arbeiten am 230-V-Netz. Zur Drehfelderzeugung benötigen sie Hilfseinrichtungen (Drosseln, Widerstände, Kondensatoren) für die notwendige Stromverschiebung. Die Wicklungen sind räumlich um 90° versetzt, was zu elliptischen Drehfeldern führt.

Aufbau: Haupt- und Hilfsstrang mit Kondensator oder Drossel. Nachteile:
- Kein Selbstanlauf
- Leistung nur ca. ein Drittel gegenüber Drehstrom-ASM
- Schlechter Leistungsfaktor
- Geringer Wirkungsgrad

Steinmetz-Schaltung: Dreiphasenmotor am Einphasennetz mit Kondensatoren. Ergibt höhere Leistung und besseren Leistungsfaktor. Richtwert Kondensatorgröße: CB = 75 µF je kW bei 230 V (nach DIN 48501). Drehrichtungsumkehr durch Umschalten des Kondensators mit zweipoligem Wechselschalter.

#### Berechnungsbeispiele Asynchronmotor

**Beispiel 25.6.1 – Leistungsabgabe:**
Motor mit η = 83 %, aufgenommene Leistung 18,5 kW → abgegebene Leistung: Pab = 18,5 kW · 0,83 = 15,355 kW

**Beispiel 25.6.2 – Leistungsaufnahme:**
Schilddaten: U = 400 V, I = 4,9 A, cosφ = 0,75 → Pauf = √3 · 400 V · 4,9 A · 0,75 = 2,546 kW

**Beispiel 25.6.3 – Vollständige Schildberechnung:**
Daten: n = 1445 min⁻¹, p = 2, P = 11 kW, IN = 24 A, U = 400 V, f = 50 Hz, cosφ = 0,78, Ia = 4 × IN

1. Synchrondrehzahl n₁ = 1500 min⁻¹; Schlupfdrehzahl ns = 1500 − 1445 = 55 min⁻¹; Schlupf s = (1500 − 1445)/1500 · 100 % = 3,67 %
2. Wirkungsgrad: η = P / (√3 · U · I · cosφ) = 11 kW / (√3 · 400 · 24 · 0,78) = 0,848 = 84,8 %
3. Anlaufstrom: Ia = 4 · 24 A = 96 A

**Beispiel 25.6.4 – Stern-Dreieck-Anlauf:**
Schilddaten: P = 7,5 kW, IN = 15,6 A, IA = 6,9 × IN, U = 400 V, η = 0,86, cosφ = 0,85

1. Anlaufstrom: IA = 6,9 · 15,6 A = 107,64 A
2. Stern-Dreieck-Strom: ID = IA · (1/√3) ≈ IA · 0,58 = 107,64 A · 0,58 = 35,88 A (Faktor 1/3 der Dreieck-Leistung)
3. Zugeführte Wirkleistung: Pzu = Pab / η = 7,5 kW / 0,86 = 8,72 kW
4. Zugeführte Scheinleistung: Sauf = Pab / (η · cosφ) = 7,5 kW / (0,86 · 0,85) = 10,26 kVA
5. Zugeführte Blindleistung: Qauf = Pab · tanφ / η = 7,5 kW · 0,62 / 0,86 = 5,39 kVar
6. Aufnahmestrom: Iauf = Pzu / (√3 · 400 V · 0,86 · 0,85) = 8,72 kW / (√3 · 400 · 0,86 · 0,85) = 15,58 A

**Beispiel 25.6.5 – Transformator speist drei Motoren:**
3 × 250 kW, cosφ = 0,83. Gesamtwirklast: P = 750 kW

- Scheinleistung: S = P / cosφ = 750 kW / 0,83 = 903,61 kVA
- Blindleistung: Q = P · tanφ = 750 kW · 0,67 = 502,5 kVar
- Bei cosφ = 1: S = P, Q = 0
- Bei cosφ = 0,98: Q = P · tanφ = 750 · 0,2 = 150 kVar → Kondensator muss 150 kVar liefern
- Erforderliche Kapazität: C = Q / (U² · 2πf) = 150000 Var / (400² · 2π · 50) = 298 µF

---

### Synchrongeneratoren (Abschn. 25.7)

#### Grundprinzip
Generatoren kommen hauptsächlich in Kraftwerken zum Einsatz:
- Vollpolläufer → thermische Kraftwerke
- Schenkelpolläufer → Wasserkraftanlagen

Der Läufer (Rotor) wird über Schleifringe elektrisch erregt, baut ein zweipoliges Magnetfeld auf (Polrad). Durch Erregerstromanpassung kann die Klemmenspannung geregelt werden. Die Ständerspulen U, V, W sind um 120° versetzt angeordnet.

Drehzahlgleichung: n = f / p (n in min⁻¹, f in Hz, p = Polpaarzahl)

Spannungsgleichung (vereinfachtes Ersatzschaltbild): U₁ = Up + I₁ · (R₁ + jXd)

Dabei: Synchronreaktanz Xd = Streureaktanz X₁σ + Hauptreaktanz X₁h. R₁ ist viel kleiner als X₁σ.

Wirkleistung: P₁ = Ustr · I₁ · cosφ = Ustr · Up / Xd · sinϑ

Drehmoment: Pmech = Pelk = ω · M = √3 · U · I · cosφ

Polradwinkel-Zusammenhang: Pmech = Ustr · Up / Xd · sinϑ = Mkipp · sinϑ

Bemessungsleistung: SrG = √3 · UrG · IrG

Wirkleistungsformel: P = 3 · E · UQ / Xd · sinφ

Blindleistungsformel: Q = UQ / Xd + E · U / Xd · cosφ

Größendefinitionen:
- SrG ... Bemessungsleistung des Generators [MVA]
- UrG ... Bemessungsspannung [kV]
- U₁ ... Klemmenspannung [V]
- Up ... Polradspannung [V]
- I₁ ... Klemmenstrom [A]
- Xd ... Synchronreaktanz [Ω]
- φ ... Phasenwinkel zwischen I₁ und U₁
- ϑ ... Polradwinkel

Polradspannung wird durch Erregerfluss erzeugt: Up = N₁ · jω · Φp = L₁h · jω · Ie

#### Leistungsdiagramm des Turbogenerators (Abschn. 25.7.2)
Das Leistungsdiagramm (Abb. 25.35) zeigt zulässige Betriebsbereiche mit folgenden Grenzen:
1. Grenze der Bemessungsleistung
2. Grenze durch maximale Erregerströme (Ie-Begrenzung)
3. Grenze der Turbinenleistung (Pmax-Begrenzung)
4. Statische Stabilitätsgrenze
5. Praktische statische Stabilitätsgrenze (ϑ-Begrenzung)
6. Grenze des Generatorbetriebs

Wichtige Zusammenhänge:
- Induktive Blindleistung Qind wird durch Erregerstrom Ie begrenzt
- Pmax hängt von Antriebsleistung und Kühlung ab
- Jeder Betriebszustand (P, Q) erreichbar durch Kombination aus Erregerstrom- und Antriebsleistungsregelung

#### Betriebsarten (Abschn. 25.7.3)

**Inselbetrieb:**
Synchrongeneratoren im Inselbetrieb dienen als Notstromaggregate für kritische Einrichtungen (Krankenhäuser, Kraftwerkseigenbedarf). Bei Kernkraftwerken: Gesamtleistung der Notstromaggregate generell um 100 % über dem Abfahrbedarf (Sicherheitsreserve). Weitere Anwendungen: Schiffe, Bohrinseln, abgelegene Gehöfte, Forschungsstationen.

Regelverhalten im Inselbetrieb:
- Frequenz = ausschließlich durch Generatordrehzahl bestimmt → Lastsprünge führen zu Frequenzschwankungen
- Lastabfall → Generator beschleunigt → Frequenz steigt
- Lastzunahme → Generator bremst → Frequenz sinkt
- Netzspannung = durch Erregung festgelegt: Erregerstrom erhöhen → Spannung steigt; Erregerstrom senken → Spannung sinkt

**Synchronisation (Parallelschaltung):**
Vor dem Zuschalten eines Synchrongenerators auf das Verbundnetz müssen vier Bedingungen erfüllt sein:
1. Gleiche Frequenz zwischen Generator und Netz
2. Gleiche Spannungsamplituden
3. Gleiche Phasenlage
4. Gleiche Phasenfolge

Betriebsarten nach dem Zuschalten:
- Antriebsleistung erhöhen → Wirkleistungsabgabe ins Netz (Generatorbetrieb)
- Antriebsleistung verringern → Wirkleistungsaufnahme aus dem Netz (Motorbetrieb → Synchronmotor)
- Übererregung (höherer Erregerstrom) → Polradspannung steigt → induktive Blindleistung ins Netz
- Untererregung (geringerer Erregerstrom) → Polradspannung sinkt → induktive Blindleistung aus dem Netz aufgenommen

Netzfrequenz im Verbundnetz:
- Wichtigste Regelgröße ist die Frequenz (50 Hz Nennwert)
- Unterschreitung 49,8 Hz → Lastverteiler wird alarmiert, Kraftwerksreserven eingesetzt
- Unterschreitung 49,4 Hz → gezielte Lastabwürfe von unkritischen Verbrauchern
- Unterschreitung 48,8 Hz → Verbundnetz wird aufgetrennt

Statische Stabilität: Alle ans Verbundnetz gekoppelten Maschinen müssen synchron laufen (gleiche Frequenz). Die statische Stabilität ist entscheidend für das Betriebsverhalten von Kraftwerksblöcken, die über Blocktransformatoren auf Hochspannungsnetze speisen.

#### Berechnungsbeispiele Synchrongeneratoren

**Beispiel 25.7.4 – Polradwinkel:**
Turbogenerator: PrG = 300 MVA, UrG = 19 kV, cosφ = 0,85, f = 50 Hz, n = 3000 min⁻¹, xd = 200 %, x'd = 21 %, x''d = 17 %, IE/IE0 = 2,3

Kurzschlussstrom: Ik = (IE/IE0) · UrG / (√3 · xd) = 19,9 kA

sinϑrG = PrG / (√3 · UrG · Ik) = 0,276 → ϑrG = 16°

**Beispiel 25.7.5 – Leistungsdiagramm:**
Turbogenerator: PrG = 100 MW, cosφrG = 0,8, UrG = 10,5 kV

- SrG = PrG / cosφrG = 100 MW / 0,8 = 125 MVA
- IrG = SrG / (√3 · UrG) = 125 MVA / (√3 · 10,5 kV) = 6873,21 A
- Komplexe Leistung: SrG = 125 MVA · (0,8 + j0,6) = 100 MW + j75 MVAr

**Beispiel 25.7.6 – Vollpolsynchrongenerator (Zeigerdiagramm):**
Daten: SrG = 21 MVA, UN = 10,4 kV, xd = 160 %, n = 1500 U/min, Betrieb mit 80 % Nennstrom, cosφind = 0,866

- Klemmenspannung (Strang): U = 10,4 kV / √3 = 6 kV
- Strom: I = 0,8 · SrG / (√3 · UN) = 0,8 · 21 MVA / (√3 · 10,4 kV) = 933 A, eilt U um φ = 30° nach
- Spannungsfall an Hauptreaktanz: I · Xd = 0,8 · xd · U = 0,8 · 1,6 · 6 kV = 7,68 kV (Winkel 120° zu U)
- Polradspannung (Cosinus-Satz): Uq² = U² + (I·Xd)² − 2·U·I·Xd·cos(120°) = 6² + 7,68² + 2·6·7,68·0,5 = 141 kV² → Uq = 11,88 kV (Strangwert), verketteter Wert UqN = 20,6 kV
- Lastwinkel (Sinus-Satz): sinβ = sin(120°) · I·Xd / Uq = 0,866 · 7,68/11,88 → β = 34°

**Beispiel 25.7.7 – Vollpolsynchronmotor (Motorbetrieb):**
Gleiche Maschinendaten wie oben, Nennstrom, Wirkleistungsaufnahme aus Netz: 16,8 MW, induktive Blindleistungsaufnahme: 12,6 MVAr

- Wirkstrom: Iw = 16,8 MW / (√3 · 10,4 kV) = 933 A
- Blindstrom: Ib = 12,6 MVAr / (√3 · 10,4 kV) = 700 A
- Gesamtstrom: I = √(933² + 700²) = 1165 A = IN
- Winkel φ: I eilt U nach
- Spannungsfall: IN · Xd = xd · U = 1,6 · 6 kV = 9,6 kV
- Polradspannung: Uq² = U² + I²N · X²d − 2·U·IN·Xd·cos(53,1°) = 6² + 9,6² − 2·6·9,6·0,6 = 59,3 kV² → Uq = 7,7 kV, verketteter Wert UqN = 13,33 kV
- Lastwinkel: sinβ / sin(53,1°) = IN·Xd / Uq → β = 85,83°
- Anmerkung: Dieser Betriebszustand ist ungünstig, da praktisch keine Überlastbarkeit verbleibt und der Motor induktive Blindleistung aufnimmt statt abzugeben. Synchronmotoren sollen normalerweise induktive Blindleistung zur Kompensation anderer Motoren liefern.

**Beispiel 25.7.8 – Drehmoment und Kippmoment:**
Dieselbe Maschine (SrM = 21 MVA, UN = 10,4 kV, xd = 160 %, n = 1500 U/min), Nennstrom bei cosφind

- Elektrische Gleichung: Pel = √3 · UN · IN · cosφ = SrG · cosφ = Pmech = 2π · n · M
- Nennmoment: M = SrM · cosφ / (2π · n) = 0,8 · 21 MW · 60 s / (2π · 1500) = 107 kNm
- Für Kippmoment: Mk = 3 · U · Uq / (2π · n · xd)
- Polradspannung (bei cosφind, Winkel 126,94° zu Spannungsfall): Uq² = 6² + 9,6² + 2·6·9,6·0,6 = 197 kV² → Uq = 14,1 kV
- Kippmoment: Mk = 3 · 14,1 kV · 1165 A · 60 s / (2π · 1500 · 1,6) = 196 kNm
- Lastwinkel: sinβ = M / Mk = 107/196 → β = 33°
- Überlastbarkeit: Mk / M = 196 / 107 = 1,83

**Beispiel 25.7.9 – Phasenschieberbetrieb (Polradspannung):**
Daten: SrG = 21 MVA, UN = 10,4 kV, xd = 160 %, n = 1500 U/min

Bei reinem Blindleistungsbetrieb sind Polradspannung und Klemmenspannung phasengleich.
- Klemmenspannung (Strang): U = 10,4 kV / √3 = 6 kV
- Spannungsfall Hauptreaktanz bei Nennstrom: IN · Xd = xd · U = 1,6 · 6 kV = 9,6 kV
- Für induktive Blindleistungsabgabe (Strom eilt 90° nach): Uq = U + IN · Xd = 6 + 9,6 = 15,6 kV (Strang), UqN = 27,05 kV (verkettet) → auf diesen Wert muss Erregerwicklung ausgelegt sein

Für kapazitive Blindleistungsabgabe bei minimaler Polradspannung Uq,min = 1,56 kV (Strang = 1,56/√3 = 0,9 kV):
- Spannungsfall bei minimaler Polradspannung: I · Xd = U − Uq = 6 − 0,9 = 5,1 kV
- Stromverhältnis: I / IN = (I · Xd) / (IN · Xd) = 5,1 / 9,6 = 0,532
- Maximal zulässige kapazitive Blindleistung: Qc = 0,532 · SrG = 0,532 · 21 MVAr = 11,15 MVAr

**Beispiel 25.7.10 – Fragen und Antworten zum Synchrongenerator:**

Frage: Synchronmotor SrM = 10 MVA, UN = 10,4 kV, xd = 160 %, n = 1500 U/min nimmt 8 MW Wirkleistung auf und gibt 6 MVAr induktive Blindleistung ab. Steigerung auf 8 MVAr Blindleistung erforderlich.
Antwort: Erhöhung der Polradspannung (durch mehr Erregerstrom) nötig. Um Ständerwicklung nicht zu überlasten, muss Wirklast gleichzeitig auf 6 MW reduziert werden, damit Nennscheinleistung von 10 MVA nicht überschritten wird.

Frage: Was passiert, wenn einem speisenden Synchrongenerator die Dampfzufuhr unterbrochen wird?
Antwort: Synchrondrehzahl bleibt erhalten, Maschine entnimmt dem Netz geringe Wirkleistung für Eigenverluste → geht in Motorbetrieb über. Für die Synchronmaschine selbst kein unmittelbarer Schaden; wegen Schutz der Turbine muss aber schnellstmöglich abgeschaltet und stillgesetzt werden.

Frage: Was passiert, wenn der Generator durch Bedienungsfehler vom Netz getrennt wird?
Antwort: Turbine gibt weiterhin Leistung ab, Generator kann sie nicht ins Netz weitergeben → Umwandlung in kinetische Energie → Drehzahlanstieg. Schnellschluss des Dampfventils wegen Zentrifugalkraftgefahr unbedingt notwendig.

Frage: Was passiert bei dreipoligem Klemmenkurzschluss am Generator?
Antwort: Ersatzschaltbild zeigt hohen induktiven Blindwiderstand, praktisch keinen Wirkwiderstand → Leistung kann nicht umgesetzt werden, wird in kinetische Energie umgewandelt → Drehzahlanstieg. Sofortige Abschaltung des Kurzschlussstroms und Dampfventilschnellschluss notwendig.

**Beispiel 25.7.11 – Fehlsynchronisierung:**
Turbogenerator SrG = 21 MVA, UN = 10,4 kV, xd = 160 %, n = 1500 U/min. Generatorspannung versehentlich auf 12,4 kV eingestellt (soll 10,4 kV sein), alle anderen Synchronisierbedingungen erfüllt.

Bei korrekter Synchronisierung fließt kein Strom beim Zuschalten. Hier entspricht die Fehlsynchronisierung gleichzeitig dem Setzen einer erhöhten Polradspannung. Der entstehende Strom:
- I / IN = (UqN − UN) / (xd · UN) = (12,4 − 10,4) kV / (1,6 · 10,4 kV) = 0,12
- Erzeugte Blindleistung: QL = 0,12 · SrG = 0,12 · 21 MVAr = 2,52 MVAr → Maschine speist diese induktive Blindleistung ins Netz, für die Maschine selbst problemlos.

---

### Gleichstrommaschinen (Abschn. 25.8)

#### Aufbau und Prinzip
GS-Maschinen bestehen aus:
- Ständer: massives Eisen, trägt Erregerwicklung (Erregerfeld)
- Läufer (Anker): geblecht (wegen Stromwendung), trägt Ankerwicklung
- Kollektor/Stromwender: sorgt dafür, dass die Stromrichtung im Läufer umgekehrt wird, wenn Ständer- und Läuferfeld einander gegenüberstehen → fortlaufende Drehbewegung

Einsatzgebiete: Werkzeugmaschinen, Hebezeuge und Kranantriebe, Traktionsantriebe, Walzwerke, Elektrowerkzeuge, Haushaltsgeräte (als Universalmotoren).

Eigenschaften von Gleichstrommotoren:
- Stufenlose Drehzahlregelung (feinstufig)
- Gleichbleibende Drehzahl bei wechselnder Last
- Hohes Drehmoment
- Hohe Schalthäufigkeit zulässig
- Kurzzeitige Überlastbarkeit

#### Grundgleichungen der GS-Maschine
- Induzierte (Gegen-)Spannung (entsteht im Anker): Uq = c · Φ · ω = c · Φ · 2π · n
- Drehzahl: n = Uq / (c · Φ · 2π)
- Kraftwirkung auf Leiter: F = B · I · l · z
- Drehmoment: M = c · Φ · IA
- Klemmenspannung: UA = Uq + IA · RA

Allgemeine Betriebsgleichungen (mit Maschinenkonstante k):
- Induzierte Spannung: Ui = k · n · Φ
- Drehmoment: M = k · IA · Φ
- Fluss proportional zu Erregerstrom: Φ ∼ IE
- Induzierte Spannung proportional zu Drehzahl: Ui ∼ n
- Klemmenspannung: U = Ui + IA · RA

Größendefinitionen:
- U₀ ... induzierte Spannung [V]
- U ... Netzspannung [V]
- B ... Flussdichte [T]
- l ... Leiterlänge [m]
- v ... Geschwindigkeit [m/s]
- z ... Zahl der Leiter
- F ... Kraft [Nm]
- Φ ... magnetischer Fluss [Vs]
- n ... Drehzahl [min⁻¹]
- IA ... Ankerstrom [A]
- IE ... Erregerstrom [A]
- RA ... Ankerwiderstand [Ω]
- c ... Maschinenkonstante

#### Wicklungsarten (Abschn. 25.8.1)
Anker- und Erregerkreis enthalten ohmsche und induktive Widerstände. Die Schaltung von Anker- und Erregerspulen bestimmt das Betriebsverhalten. Laut DIN VDE 0530 Teil 8 gibt es folgende Wicklungsarten:
1. Ankerwicklung: erzeugt magnetische Ankerquerfelder
2. Feldwicklung: erzeugt magnetische Hauptfelder zwischen Hauptpolschuhen
3. Wendepolwicklung: erzeugt Felder, die dem Ankerquerfeld entgegenwirken
4. Kompensationswicklung: verhindert Feldverzerrungen im Bereich der Hauptpole

Anschlussbezeichnungen nach DIN VDE 0570 und DIN 42401:
| Buchstabe | Wicklung |
|---|---|
| A | Ankerwicklung |
| B | Wendepolwicklung |
| C | Kompensationswicklung |
| D | Reihenschlusswicklung |
| E | Nebenschlusswicklung |
| F | Fremderregte Wicklung |
| L+ | Positiver Leiter |
| L− | Negativer Leiter |
| M | Mittelleiter |

#### Nebenschlussmotor (Abschn. 25.8.2)
Die Erregerwicklung liegt parallel zur Ankerwicklung an gleicher Spannung. Dadurch bleiben Erregerstrom und Hauptfluss lastunabhängig und konstant (typische Anwendung: Werkzeugmaschinen).

Grundgleichungen:
- Knotenpunktstrom: I = IA ± IE (+ für Generator, − je nach Betrieb)
- Spannungsgleichgewicht: U − UB − Ui − IA · RA = 0
