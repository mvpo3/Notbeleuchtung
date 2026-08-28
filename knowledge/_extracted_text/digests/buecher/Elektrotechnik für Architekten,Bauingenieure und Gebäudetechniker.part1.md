# Elektrotechnik für Architekten,Bauingenieure und Gebäudetechniker — Teil 1
> Quelle: Elektrotechnik für Architekten,Bauingenieure und Gebäudetechniker (buecher) · Seiten 41-80.

Lehrbuch von I. Kasikci (Springer Fachmedien Wiesbaden, 2018) für Architekten, Bauingenieure und Gebäudetechniker. Dieser Teil behandelt die physikalischen Grundbegriffe der Elektrotechnik (Atomaufbau, Strom, Spannung, Widerstand, Leistung) sowie die Grundgesetze (Ohmsches Gesetz, Kirchhoffsche Regeln) und erste Berechnungen von Gleichstromkreisen (Reihen-/Parallelschaltung, Stern-Dreieck-Umwandlung, Brückenschaltung).

## Inhalt

### Kapitel 4: Physikalische Grundbegriffe

#### 4.1 Aufbau der Materie und Ladungen

- Alle Stoffe sind aus Atomen aufgebaut, die als kleinste, unteilbare Einheiten der Materie gelten.
- Atome bestehen aus einem Kern (Neutronen + Protonen) sowie einer Elektronenhülle, die die Elektronen trägt. Grundlage: Bohrsches Atommodell (Schalen K, L, M, N, O, P).
- Unterschied zwischen Elementen: Protonenzahl (Kernladungszahl / Ordnungszahl). Isotope desselben Elements haben gleiche Protonenzahl, aber verschiedene Neutronenzahl.
- Heliumatom als Beispiel:
  - Proton: Ladung Qp = +1,602 · 10⁻¹⁹ As, Masse mp = 1,6726 · 10⁻²⁷ kg
  - Neutron: keine Ladung, Masse mn = 1,6747 · 10⁻²⁷ kg
  - Elektron: Ladung Qe = −1,602 · 10⁻¹⁹ As, Masse me = 9,109 · 10⁻³¹ kg
- Nukleonenzahl = Summe aus Protonen und Neutronen.
- Valenzelektronen auf der äußersten Schale bestimmen das elektrische Verhalten des Atoms und ermöglichen den Stromfluss.
- Atome sind elektrisch neutral: Anzahl Elektronen in der Hülle = Anzahl Protonen im Kern.

**Ladungsbegriff:**
- Ladung besteht aus zählbaren Elementarladungen, Einheit: 1 C (Coulomb).
- 1 Coulomb = Ladungsmenge, die bei 1 A Stromstärke pro Sekunde durch einen Leiterquerschnitt fließt.
- Ladung des Elektrons: Qe = −e = −1,602 · 10⁻¹⁹ As
- Gleichnamige Ladungen stoßen sich ab, ungleichnamige ziehen sich an.
- Ladungen sind an Ladungsträger gebunden und nicht beliebig teilbar.
- Fließt ein Elektron je Sekunde durch den Leiterquerschnitt → Stromstärke I = 1,602 · 10⁻¹⁹ A.
- Messbare Mindestströme heutiger Geräte: kleiner als 10⁻¹⁶ A, entspricht ca. 6250 Elektronen/s bzw. ca. 6 Elektronen/ms.
- Ladungsmenge Q = 1 As enthält ca. 6,3 · 10¹⁸ Elektronen.

**Berechnungsbeispiel: Anzahl der Elektronen bei 1 A**
- Q = I · t = 1 As
- N = Q / e = 1 As / (1,6 · 10⁻¹⁹ As) = 6,24 · 10¹⁸ Elektronen

#### 4.2 Leiter, Halbleiter und Nichtleiter

- Alle Stoffe enthalten Elektronen und Protonen als Grundbestandteile.
- **Leiter:** Stoffe mit gut frei beweglichen Ladungsträgern. Metalle wie Kupfer, Silber und Gold sind typische Leiter; in einem Leiter befinden sich ca. 10²³ freie Elektronen/cm³.
- **Nichtleiter / Isolatoren:** Ladungsträger sind praktisch nicht frei beweglich. Beispiele: Porzellan, Seide, Hartgummi, Papier, Baumwolle, Glas, bestimmte Keramiken, Quarz.
- **Halbleiter:** Germanium und Silizium besitzen kaum freie Ladungsträger. Durch Dotierung mit Fremdatomen lässt sich die Leitfähigkeit gezielt erhöhen.
  - Äußere Elektronenschale bei Halbleitern nicht vollständig besetzt (4 Elektronen).
  - **n-Halbleiter:** Fünfwertige Atome (z.B. Arsen, Antimon, Phosphor) als Elektronendonatoren in Siliziumgitter eingebaut → freie bewegliche Elektronen entstehen. Das überschüssige Donatorelektron kann bereits durch geringe thermische Energie (Zimmertemperatur) ins Leitungsband gehoben werden.
  - **p-Halbleiter:** Dreiwertige Atome (z.B. Gallium, Indium, Aluminium, Bor) als Elektronenakzeptoren → Elektronenfehlstellen (Löcher, Defektelektronen) entstehen, die wie positive bewegliche Ladungsträger wirken.

#### 4.3 Elektrischer Strom

- Bewegliche Ladungsträger in Leitern sind Elektronen und Ionen.
- Bei Temperaturen über dem absoluten Nullpunkt befinden sich freie Ladungsträger in dauernder ungeordneter Bewegung → kein gerichteter Ladungstransport ohne äußere Ursache.
- Gerichtetes Wandern aller beweglichen Ladungsträger (positive in eine Richtung, negative entgegengesetzt) bezeichnet man als elektrischen Strom.
- Allgemeine Definition der Stromstärke: I = ΔQ / Δt
- Gleichstrom (zeitlich konstant): I = Q / t
- Wechselstrom (zeitlich veränderlich): i(t) = dq(t) / dt
- Einheit der elektrischen Stromstärke: [I] = A (Ampere)
- Elektrischer Strom ist Ladungstransport; Ursache ist eine gerichtete Kraftwirkung auf die Ladungsträger.
- **Technische Stromrichtung:** gleich der Wanderungsrichtung positiver Ladungsträger, entgegen der Wanderungsrichtung negativer Ladungsträger (Elektronen).

**Tabelle: Typische Stromstärken**

| Verbraucher / Ereignis | Stromstärke |
|---|---|
| Taschenrechner | 100 µA |
| E-Herd | 8 A |
| Waschmaschine | 9 A |
| Motor | 20 A |
| Transformator | 900 A |
| Blitz | 100 kA |

#### 4.4 Wirkungen des elektrischen Stromes

Elektrischer Strom ist gefährlich. Folgende Wirkungen und Gefahren sind für Lebewesen und Anlagen relevant:

1. **Magnetische Wirkung:** Jeder stromdurchflossene Leiter erzeugt ein begleitendes Magnetfeld.
2. **Thermische Wirkung:** Strom erzeugt Wärme durch Umsatz elektrischer Leistung im Widerstand.
   - Wärmemenge: W = I² · R · t
   - Verlustleistung: P = I² · R = U² / R
3. **Chemische Wirkung:** In Flüssigkeiten (Elektrolyten = Lösungen aus Salzen, Säuren, Basen mit guter Leitfähigkeit) löst Strom chemische Veränderungen aus — dieser Vorgang heißt Elektrolyse.
4. **Optische Wirkung:** In Gasen kann Strom Leuchterscheinungen hervorrufen.
5. **Biologische Wirkung (Gefahr):** Ionenstrom transportiert Signale in biologischen Systemen. Stromschlag!
   - Entscheidend für den menschlichen Körper ist die Stromstärke, abhängig von Spannung und Einwirkdauer.
   - Körperwiderstand: jeder Arm und jedes Bein mindestens 500 Ω; Gesamtbereich 1000 Ω bis 3000 Ω.
   - Bei angenommenem Körperwiderstand von 1000 Ω und maximaler Berührungsspannung 50 V → Strom 50 mA.
   - An einer 230-V-Steckdose bei 1000 Ω Körperwiderstand: 230 V / 1000 Ω = 230 mA → tödlich.
   - Für Wechselstrom nach IEC 479 im Bereich 15 Hz bis 100 Hz wurden vier gefährliche Wirkungsbereiche definiert (Bild 4.10 im Original).
   - Bei höheren Frequenzen geringere Gefahr, da Ströme durch Stromverdrängung an der Körperoberfläche fließen.

#### 4.5 Beispiele: Stromstärke

**Beispiel 4.5.1 – Stromstärke aus Ladungsfluss:**
- Durch einen Cu-Leiter fließen pro Sekunde 4,4 mC.
- I = Q / t = 4,4 mC / 1 s = 4,4 mA

**Beispiel 4.5.2 – Ladung und Stromstärke aus Elektronenbewegung:**
- Innerhalb von 2 s werden 1,87 · 10¹⁹ Elektronen bewegt.
- Ladung: Q = n · e = 1,87 · 10¹⁹ · 1,602 · 10⁻¹⁹ C ≈ 3 As
- Stromstärke: I = Q / t = 3 As / 2 s = 1,5 A

#### 4.6 Stromdichte

- Strombelastbarkeit von Kabeln ist in DIN-VDE-Vorschriften tabelliert.
- Stromdichte S bei zylindrischem Leiter mit Querschnittsfläche A und Strom I: S = I / A
- Einheit: [S] = A/m² oder praktisch A/mm²
- Stromdichte ist Maß für die thermische Belastbarkeit von Kabeln und Leitungen.

#### 4.7 Beispiele: Stromdichte

**Beispiel 4.7.1 – Leuchtstofflampe:**
- 58-W-Leuchtstofflampe, Leitungsquerschnitt 1,5 mm², Strom 0,252 A, Spannung 230 V.
- Stromdichte: J = 0,252 A / 1,5 mm² = 0,168 A/mm²

**Beispiel 4.7.2 – Fundamenterder:**
- Abmessungen 30 mm × 3,5 mm → Querschnitt 105 mm²; Fehlerstrom 350 A.
- Stromdichte: J = 350 A / 105 mm² = 3,33 A/mm²

#### 4.8 Elektrische Spannung

- In einem Leiter bewegen sich Elektronen ungerichtet; geordnete Bewegung entsteht nur durch eine Spannungsquelle als treibende Kraft.
- Um eine Ladung von Punkt A nach Punkt B zu verschieben, ist Arbeit W_zu erforderlich → elektrisches Feld baut sich auf → elektrische Spannung U entsteht.
- Spannung zwischen A und B: U_AB = (W_A − W_B) / Q = W_AB / Q
- Kraft auf die Ladung: F = Q · E → E = F / Q
- Spannung im homogenen Feld: U = E · l = F · l / Q
- Einheit der Spannung: [U] = V (Volt) = W / A = Ws / As
- Spannung entsteht durch Ladungstrennung; Ausgleichsbestreben der Ladungen ist die elektrische Spannung.
- Spannung kann erzeugt werden durch: Reibung (Plastikstab an Wolltuch), elektromagnetische Induktion, Kombination von Stoffen mit speziellen chemischen Eigenschaften, lichtelektrischen Effekt.
- **Wichtiger Hinweis:** In elektrischen Anlagen darf der gesamte Spannungsfall ±10 % nicht überschreiten. Spannung und Spannungsfall haben dasselbe Symbol, dieselbe Einheit und werden mit denselben Messgeräten erfasst.

**Tabelle: Typische Spannungen**

| Verbraucher / Ereignis | Spannung |
|---|---|
| Primärzelle | 1,5 V |
| Haushalt (Wechselstromnetz) | 230 V |
| Motor (Drehstromnetz) | 400 V |
| Freileitungen | 20 kV, 110 kV, 220 kV, 380 kV |
| Blitz | 200 kV |

#### 4.9 Beispiele: Elektrische Spannung

**Beispiel 4.9.1 – Arbeit:**
- Ladung 30 µC, Kraft 6 mN, Strecke 60 mm.
- W = F · s = 6 mN · 0,06 m = 0,36 mJ

**Beispiel 4.9.2 – Spannung:**
- U = W / Q = 0,36 mJ / 0,03 mC = 12 V

#### 4.10 Elektrischer Widerstand

- Elektronen stoßen beim Fließen mit Atomen des Leiters zusammen → Bremsung → Wärmeentstehung.
- Stromfluss proportional zum Leiterquerschnitt.
- Technische Stromflussrichtung: von + nach − im äußeren Stromkreis; Elektronen fließen von − nach +.
- Ein Stromkreis besteht aus: Spannungsquelle, Verbindungsleitungen (ggf. Schaltelemente und Messgeräte), Verbraucher.
- Begriff Widerstand hat zwei Bedeutungen:
  1. Physikalische Größe eines Leiters, gemessen in Ω.
  2. Bauelement, bei dem diese Größe technisch im Vordergrund steht.
- Ohmsches Gesetz aus Stromdichte und elektrischer Feldstärke hergeleitet:
  - S = κ · E (spezifische Leitfähigkeit κ)
  - I / A = κ · U / l → U = (l / (κ · A)) · I = R · I
- Widerstandsformel: R = ρ · l / A = l / (κ · A)
  - Widerstand direkt proportional zur Leitungslänge, umgekehrt proportional zum Querschnitt.
- Einheit: [R] = Ω (Ohm)
- Spezifischer Widerstand: ρ = 1 / κ; Einheit: Ω·mm²/m
- Elektrischer Leitwert: G = 1 / R; Einheit: [G] = 1 Siemens (S)
- Temperaturabhängigkeit des Widerstands: R_T = R_20 · [1 + α₂₀ · (ϑ₂ − ϑ₁)]
  - Temperaturkoeffizient für Kupfer: α₂₀ = 3,9 · 10⁻³ K⁻¹
  - Mit steigender Temperatur steigt der Widerstand des Leiters.

#### 4.11 Beispiele: Elektrischer Widerstand

**Beispiel 4.11.1 – Stromkreiswiderstand:**
- I = 5 A, U = 230 V → R = U / I = 230 V / 5 A = 46 Ω

**Beispiel 4.11.2 – Leitwert:**
- Heizspirale R = 40 Ω → G = 1 / 40 Ω = 25 mS

**Beispiel 4.11.3 – Widerstand und Spannungsfall einer Leitung:**
- Cu-Leitung, l = 15 m, A = 2,5 mm², I = 12 A.
- R = l / (κ · A) = 10 m / (56 m/(Ω·mm²) · 2,5 mm²) = 107 mΩ (Hinweis: im Text steht 15 m, Formelberechnung nutzt 10 m — so in der Quelle)
- Spannungsfall: U = R · I = 107 mΩ · 12 A = 1,29 V

#### 4.12 Strom- und Spannungszählpfeile

- Richtung von Spannung und Strom in einem Stromkreis (Quelle → Leitung → Verbraucher) werden mit Zählpfeilen angegeben; ohne Zählpfeile ist eine eindeutige Darstellung nicht möglich.

#### 4.13 Erzeuger- und Verbraucherzählpfeile

- In Schaltplänen werden Spannungen und Ströme durch Zählpfeile dargestellt.
- **Erzeugerpfeilsystem:** Spannungs- und Stromzeiger zeigen in entgegengesetzte Richtung; Leistung P < 0.
- **Verbraucherpfeilsystem:** Spannungs- und Stromzeiger zeigen in gleiche Richtung; Leistung P > 0.
- Begriff Tor (port) für Klemmen: Eintor (oneport) = Zweipol.

#### 4.14 Elektrische Leistung, Arbeit und Energie

- In einem stromdurchflossenen Kabel entsteht ein Widerstand, der Wärme erzeugt → Stromarbeit wird verrichtet.
- Leistung: P = U · I; Einheit [P] = W (Watt) = 1 V · 1 A
- Elektrische Arbeit W: Maß für die entstandene Wärmemenge; entspricht Leistung über eine bestimmte Zeit. W = P · t; Einheit: [W] = Ws (Wattsekunde) = Joule (J) = Nm
- Energie: Fähigkeit, Arbeit zu verrichten; unterschieden in potenzielle und kinetische Energie; gleiche Formelzeichen und Einheiten wie Arbeit.

#### 4.15 Wirkungsgrad

- Die von einem elektrischen Verbraucher aufgenommene Leistung (P_zu) setzt sich zusammen aus genutztem Anteil (P_ab) und nicht nutzbarem Verlustanteil (P_v), der meist als Wärme abgeführt wird.
- Wirkungsgrad: η = P_ab / P_zu = (P_ab / P_zu) · 100 %

**Tabelle: Typische Leistungen**

| Verbraucher | Leistung |
|---|---|
| Atomkraftwerk | 1200 MW |
| Haushalt | 6 kW |
| Drehstrom-Motor | 5,5 kW |
| Leuchtstofflampe | 58 W |
| Steckdose (einfach) | 200 W |
| Kühlschrank | 150 W |
| Fernseher | 100 W |

#### 4.16 Beispiele: Elektrische Leistung

**Beispiel 4.16.1 – Pumpe:**
- 200 l Wasser/min werden 50 m hochgefördert.
- P = ρ · V · g · s / t = 1 kg/dm³ · 200 dm³ · 9,81 m/s² · 50 m / 60 s = 1,635 kW

**Beispiel 4.16.2 – Hebebühne:**
- Auto 1,5 t wird in 3 s auf 1,5 m gehoben.
- P = F · s / t = 1500 kg · 9,81 m/s² · 1,5 m / 3 s = 7,35 kW

**Beispiel 4.16.3 – Lampen parallel:**
- Halogenglühlampe (cos φ = 1), I_Betrieb = 0,5 A, U = 230 V.
- P = U · I = 230 V · 0,5 A = 115 W
- Zweite gleiche Lampe parallel → P_ges = 230 W; I_ges = P / U = 230 W / 230 V = 1 A

**Beispiel 4.16.4 – Lampen in Reihe:**
- Einzellampe: 0,5 A, 230 V → R = U / I = 230 V / 0,5 A = 460 Ω
- Zwei Lampen in Reihe: R_ges = 920 Ω; I_ges = 230 V / 920 Ω = 0,250 A; P = 57,5 W
- Fazit: Reihenschaltung liefert weniger Leistung und weniger Licht als Parallelschaltung.

#### 4.17 Beispiele: Strom, Spannung und Widerstand

**Beispiel 4.17.1 – Widerstandswerte eines Kupferdrahts:**
- A = 1,5 mm², l = 10 m, ρ_Cu = 0,01786 Ω·mm²/m
- Spezifischer Leitwert: κ = 1 / ρ = 56 m/(Ω·mm²)
- Widerstand: R = ρ · l / A = 0,01786 · 10 / 1,5 = 119 mΩ
- Leitwert: G = 1 / R = 8,40 S

**Beispiel 4.17.2 – Glühlampe:**
- U = 12 V, I = 500 mA (Gleichstrom).
- a) Leistung: P = U · I = 12 V · 0,5 A = 6 W
- b) Energie in einer Stunde: W = P · t = 6 W · 3600 s = 21600 Ws = 21,6 kJ = 0,006 kWh

#### 4.18 Analogiebetrachtungen: Flüssigkeitskreis — Stromkreis

Vergleich der Verhältnisse in Heizungstechnik und Elektrotechnik:

**Tabelle: Analogie Flüssigkeitskreis ↔ Stromkreis**

| Flüssigkeitskreis | Stromkreis |
|---|---|
| Pumpe | Spannungsquelle |
| Rohrleitungen | Stromleitungen |
| Strömungswiderstand | Elektrischer Widerstand |
| Mengenmesser | Strommesser |
| Druckdifferenzmesser | Spannungsmesser |
| Volumenstrom | Elektrischer Strom |

---

### Kapitel 5: Grundgesetze der Elektrotechnik

#### 5.1 Das Ohmsche Gesetz

- In einem Stromkreis mit ohmschen Widerständen sind Spannung und Strom linear voneinander abhängig: bei Variation der Spannung U ändert sich der Strom I proportional.
- Proportionalitätsbeziehung: U ~ I
- Proportionalitätskonstante = Widerstand: R = U / I
- Ohmsches Gesetz: U = R · I (Georg Simon Ohm, 1789–1864, Entdeckung 1826)
- Widerstand R ist im Allgemeinen konstant.

#### 5.2 Die Kirchhoffschen Gesetze

**Vier wichtige Begriffe:**
1. **Netzwerk:** Gesamtheit einer Schaltung aus Elementen, die mit Leitungen verbunden sind.
2. **Knoten:** Verbindungspunkt zweier oder mehrerer Leitungen.
3. **Zweig:** Leitungszug zwischen zwei Knoten.
4. **Masche:** Jeder geschlossene Umlauf von einem Netzwerkpunkt auf beliebigem Weg zurück zum Ausgangspunkt.

#### 5.2.1 Erster Kirchhoffscher Satz (Knotenregel)

- In einem Knotenpunkt können keine Ladungen verschwinden oder neu entstehen.
- Summe aller zufließenden Ströme = Summe aller abfließenden Ströme.
- Formal: ΣI = 0 im Knoten (zufließende Ströme positiv, abfließende negativ).
- I₁ − I₂ − I₃ = 0 → I₁ = I₂ + I₃
- Daraus ableitbar: **Stromteilerregel** bei Parallelschaltung zweier Widerstände R₁ und R₂:
  - I_R1 = I_ges · R₂ / (R₁ + R₂)
  - I_R2 = I_ges · R₁ / (R₁ + R₂)
  - R_ges = R₁ · R₂ / (R₁ + R₂)

#### 5.2.2 Beispiel zum 1. Kirchhoffschen Satz

- Knotenpunkt a: I₁ − I₂ − I₃ = 0 → I₂ = I₁ − I₃ = 2 A
- Knotenpunkt b: I₂ + I₄ − I₆ = 0 → I₄ = I₆ − I₂ = −1 A
- Knotenpunkt c: I₃ − I₄ − I₅ = 0 → I₅ = I₃ − I₄ = 2 A

#### 5.2.3 Zweiter Kirchhoffscher Satz (Maschenregel)

- In einer Masche ist die Summe aller Zweigspannungen gleich null: ΣU = 0.
- Zählregel: Spannungen, deren Zählpfeile in Richtung des Maschenumlaufs zeigen → positiv; entgegengesetzt → negativ.
- U_R1 + U_R2 − U_Q = 0 → U_Q = U_R1 + U_R2
- Daraus ableitbar: **Spannungsteilerregel:**
  - U_R1 = U_Q · R₁ / (R₁ + R₂)
  - U_R2 = U_Q · R₂ / (R₁ + R₂)

#### 5.2.4 Beispiel zum 2. Kirchhoffschen Satz

- Masche 1: U₁ − U₂ + U_Q = 0 → U_Q = U₁ + U₂; U₁ = U_Q − U₂ = 4 V
- Masche 2: −U₂ + (−U₃) − U₄ = 0 → U₃ = U₂ − U₄ = 6 V
- Masche 3: U_Q = U₁ + U₃ + U₄ = 4 V + 6 V + 2 V = 12 V ✓

---

### Kapitel 6: Berechnung von Gleichstromkreisen

- Gleichstromgrößen sind zeitunabhängig und werden mit Großbuchstaben bezeichnet.
- Jeder elektrische Stromkreis besteht aus Erzeuger (Quelle), Verbraucher und verbindender Leitung.
- Für Berechnungen werden reale Elemente durch Symbole ersetzt und Zählpfeile eingetragen.
- Grundkenntnisse für Gleichstromberechnungen: Ohmsches Gesetz, Kirchhoffsche Gesetze, Eigenschaften von Widerstand/Kondensator/Spule, Anwendung in elektrischen Netzwerken.
- Themen: Reihen-/Parallelschaltungen von Widerständen, Ersatzspannungsquellen/-stromquellen, Kurzschluss-/Leerlaufdaten, Wirkungsgrad, Netzwerkberechnungen.

#### 6.1 Reihenschaltung von Widerständen

- Bei Reihenschaltung fließt durch alle Widerstände derselbe Strom.
- Gesamtspannung = Summe der Einzelspannungen (Spannungsfälle).
- U₀ = I · (R₁ + R₂ + R₃) = I · R_ges
- Gesamtwiderstand: R_ges = R₁ + R₂ + R₃ + … + Rn (Summe der Einzelwiderstände)

**Beispiel 6.1.1 – Reihenschaltung zweier Kabeln:**
- Kabel 1: 1,15 Ω/m; Kabel 2: 0,387 Ω/m bei 2 °C (induktive Widerstände vernachlässigt)
- R_ges = 1,15 Ω + 0,387 Ω = 1,497 Ω

**Beispiel 6.1.2 – Reihenschaltung von Lampen:**
- 40-W-Lampe, U = 230 V → I = P / U = 40 W / 230 V = 174 mA
- Widerstand: R = P / I² = 40 W / (174 mA)² = 1321 Ω
- Zwei Lampen in Reihe: R_ges = 2642 Ω → I = 230 V / 2642 Ω = 87,06 mA
- Ergebnis: Betriebsstrom halbiert sich → Lampen werden dunkler.

**Beispiel 6.1.3 – Quellenspannung aus Spannungsfall:**
- Laststrom jeweils 5 A; Quellenspannung ergibt sich aus U_Q = U₁ + U₂ mit U = I_L · R.

#### 6.2 Parallelschaltung von Widerständen

- An jedem Widerstand liegt dieselbe Spannung an.
- Gesamtstrom = Summe der Einzelströme.
- Kehrwert des Gesamtwiderstands: 1/R_ges = 1/R₁ + 1/R₂ + 1/R₃
- Äquivalent mit Leitwerten: G_ges = G₁ + G₂ + G₃

**Beispiel 6.2.1/6.2.2 – Parallelschaltung:**
- Abzweig 1 (R = 20 Ω): I = 230 V / 20 Ω = 11,5 A
- Abzweig 2 (R = 40 Ω): I = 230 V / 40 Ω = 5,75 A
- Gesamtstrom: I_ges = 11,5 A + 5,75 A = 17,25 A
- Gesamtwiderstand: R_ges = (20 Ω · 40 Ω) / (20 Ω + 40 Ω) = 13,33 Ω
- Probe: I_ges = 230 V / 13,33 Ω = 17,25 A ✓ (beide Verfahren liefern identisches Ergebnis)

#### 6.3 Stern-Dreieck-Umwandlung

- Stromkreise, die weder reine Reihen- noch Parallelschaltungen sind, werden in Stern-Dreieck-Konfiguration umgerechnet und vereinfacht.

**Umwandlung Stern → Dreieck:**
- R₁₂ = R₁₀ + R₂₀ + R₁₀ · R₂₀ / R₃₀
- R₂₃ = R₃₀ + R₂₀ + R₃₀ · R₂₀ / R₁₀
- R₃₁ = R₃₀ + R₁₀ + R₃₀ · R₁₀ / R₂₀

**Umwandlung Dreieck → Stern:**
- R₁₀ = R₁₂ · R₃₁ / (R₁₂ + R₂₃ + R₃₁)
- R₂₀ = R₂₃ · R₁₂ / (R₁₂ + R₂₃ + R₃₁)
- R₃₀ = R₂₃ · R₃₁ / (R₁₂ + R₂₃ + R₃₁)

#### 6.4 Wheatstonesche Brückenschaltung

- Besteht aus vier Widerständen: je zwei in Reihenschaltung, parallel an einer Spannungsquelle angeschlossen.
- Bei abgeglichener Brückenschaltung: sind drei Widerstände bekannt, lässt sich der vierte berechnen.
