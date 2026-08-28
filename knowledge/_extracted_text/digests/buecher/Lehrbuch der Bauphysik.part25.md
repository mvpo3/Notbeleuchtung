# Lehrbuch der Bauphysik — Teil 25
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 1001-1040.

Dieser Teil behandelt die letzten Abschnitte des Brandschutzkapitels: quantitative Bewertung von Rauch- und Brandgaswirkungen auf Personen (Sichtweite, Toxizität, FED-Konzept) sowie das gesamte Kapitel 38 zu mathematischen Brandmodellen — von Handrechenformeln für Plume und Ceiling Jet über Mehrzonenmodelle bis zu CFD-Feldmodellen mit Turbulenz- und Verbrennungssubmodellen.

## Inhalt

### Kap. 37 (Fortsetzung): Sichtweite im Rauch und Personensicherheit

#### Erkennungsweite als Funktion der Rauchdichte

Auswertungen von Rauchversuchen (Jin) zeigen einen im Wesentlichen reziproken Zusammenhang zwischen optischer Rauchdichte und Erkennungsweite S. Zwei Formeln gelten:

- **Nichtreizendes Rauchgas:** S = C / K, mit K < 0,25 m⁻¹
- **Reizendes Rauchgas:** S = (C / K) · [multiplikativer Korrekturfaktor aus log-Term], gültig für K > 0,25 m⁻¹

Messbereich der Jin-Versuche: Betrachter-Objekt-Abstände 5–15 m; Extrapolation bis ca. 0,5 m (Armeslänge) möglich.

**Proportionalitätskonstante C (typische Mittelwerte nach Jin):**
- Selbstleuchtende Hinweiszeichen: C = 8 (Beobachtungsbereich 5–10)
- Lichtreflektierende Hinweiszeichen: C = 3 (Beobachtungsbereich 2–4, je nach Reflexionsgrad)

Ab optischer Rauchdichte DL ≈ 0,1 m⁻¹ zeigen empirische Studien eine deutliche Verlangsamung ortsfremder Personen. Reizende Rauchbestandteile verstärken die Reduktion der Erkennungsweite zusätzlich.

**Leuchtdichte-basierte Formel (Gl. 37.3):**  
S = K⁻¹ · ln(L₀/L)  
Für den Nachweis einer raucharmen Schicht ist eine wahrgenommene Leuchtdichte von 2–5 cd/m² erforderlich. Da Leuchten der Allgemein- und Sicherheitsbeleuchtung im Brandfall rasch in der Rauchschicht liegen, ist dieser Leuchtdichte-Ansatz von besonderer Praxisrelevanz.

#### Anhaltswerte zur Personensicherheit (Tab. 37.1)

Für ingenieurmäßige Brandsicherheitsnachweise existieren quantitative Schutzzielwerte, aufgeteilt nach Aufenthaltsdauer im brandbetroffenen Bereich:

| Beurteilungsgröße | kurze Dauer (<5 min) | mittlere Dauer (<15 min) | längere Dauer (<30 min) |
|---|---|---|---|
| CO-Konzentration | 500 ppm | 200 ppm | 100 ppm |
| CO₂-Konzentration | 3 Vol.-% | 2 Vol.-% | 1 Vol.-% |
| HCN-Konzentration | 40 ppm | 16 ppm | 8 ppm |
| Wärmestrahlung | < 2,5 kW/m² | 2,0 kW/m² | 1,7 kW/m² |
| Gastemperatur | 50 °C | 50 °C | 45 °C |
| Rauchdichte DL | 0,1/0,2 m⁻¹ (¹) | 0,1/0,15 m⁻¹ (¹) | 0,1 m⁻¹ |
| Erkennungsweite | 10–20 m | 10–20 m | 10–20 m |

(¹) Der höhere Wert kann angesetzt werden, wenn der betroffene Bereich übersichtlich strukturiert oder den Personen bekannt ist.

**Anmerkungen zu den Tabellenwerten:**
- HCN-Werte: Streuung hoch; für typische Mischbrandlasten gilt CO:HCN ≈ 12,5:1 als Korrelation mit CO/CO₂
- Gastemperatur bezieht sich auf Luft mit weniger als 10 Vol.-% Wasserdampfgehalt; darf nicht isoliert, ohne gleichzeitige Rauchdichtebewertung, als Sicherheitskriterium herangezogen werden
- Rußkonzentration bei DL = 0,1 m⁻¹ ≈ 25 mg/m³; bei DL = 0,2 m⁻¹ ≈ 50 mg/m³ (massenspezifischer Extinktionskoeffizient Km = 8,7 m²/g)
- Sauerstoffkonzentration wird nicht als eigenständiges Kriterium geführt, da bei Einhaltung der Schadstoffgrenzwerte O₂ deutlich über 15 Vol.-% liegt
- Bei DL ≤ 0,1 m⁻¹ bzw. Erkennungsweite ≥ 10 m kann in der Regel davon ausgegangen werden, dass gleichzeitig die toxischen Grenzwerte eingehalten sind

**Aufenthaltsdauern definieren Zeiträume für:**
- Kurz (<5 min): selbstständige Flucht
- Mittel (5–15 min): Fremdrettung
- Länger (15–30 min): Brandbekämpfung

#### FED-Konzept (Fraktionelle Effektive Dosis)

**Ausbeute (Yield) einer Verbrennungskomponente:**  
Yi(t) = mi(t) / mf(t) [g/g]  
Verhältnis aus erzeugter Komponentenmasse zu umgesetzter Brennstoffmasse; mf umfasst den gesamten Massenverlust (nicht nur chemisch umgesetzten Anteil), bezogen auf die effektive Verbrennungswärme Hc,eff.

**N-Gas-Modell (NIST):**  
Betrachtet N=5 Leitkomponenten: CO, HCN, HCl, HBr, CO₂ und zusätzlich Sauerstoffabnahme. FEDNIST = 1 entspricht 50 % Letalität bei Versuchstieren (Nagetieren). Empirisch ermittelt: 50%-Letalität tritt bei FEDNIST = 1,1 auf (95%-Vertrauensbereich ±0,2).

**Purser-Modell (Stand der Technik für Mensch):**  
FED = 1 entspricht hier Fluchtunfähigkeit (Verwirrung, Bewusstlosigkeit), nicht Tod. Berücksichtigt CO, HCN, O₂-Mangel und CO₂ (letzteres auch als Hyperventilationsverstärker).

Einzelformeln der FED-Komponenten (Konzentrationen: cCO und cHCN in ppm; cCO₂ und cO₂ in Vol.-%):

- **FCO:** proportional zu cCO^1,036 · RMV · Δt / D  
  (Faktor 3,317 × 10⁻⁵; RMV = Atemrate in l/min; D = kritische COHb-Konzentration in Vol.-% bis Bewusstlosigkeit)
- **FHCN:** abhängig von exp(cHCN · Faktor) · Δt, mit Referenzexponent −5,396 und Konzentrationsfaktor 0,023
- **FCO₂:** abhängig von exp(cCO₂ · 0,5189 − 6,1623) · Δt
- **FO₂:** abhängig von exp[(20,9 − cO₂) · 0,54 − 8,13] · Δt

**Typische Referenzwerte (70 kg Erwachsener, leichte körperliche Belastung):**
- D = 30 %, RMV = 25 l/min
- Ruhezustand: D = 40 %, RMV = 8,5 l/min
- Tod tritt bei D ≈ 50 % ein
- Kinder (klein): Zeit bis Bewegungsunfähigkeit ca. Faktor 2 kürzer als Erwachsene

**Gesamtformel für F (Gl. 37.9):**  
F = (FCO + FHCN + FLDirr) · VHyp + FO₂ + FCO₂  
mit Hyperventilationsfaktor VHyp = exp(0,2 · cCO₂) und Fractional Lethal Dose der Reizkomponenten FLDirr als Summe aus Konzentrations-Zeit-Quotienten.

- Hyperventilation ist ab cCO₂ ≥ 2 Vol.-% einzubeziehen
- O₂-Mangel ist ab cO₂ < 13 % zu berücksichtigen
- Für die Bestimmung verfügbarer Räumungszeit: max. F = 0,1 bis 0,3 ansetzen (unterer Wert für besonders sensible Personengruppen)
- Relationen gelten für kurzzeitige starke Belastungen (bis ~1 h, CO ab ~2000 ppm)
- Bei niedrigeren Konzentrationen spielen Sättigungseffekte eine zunehmende Rolle

---

### Kap. 38: Mathematische Brandmodelle

#### Drei Modellklassen

Mathematische Brandsimulationsmodelle gliedern sich in:
1. **Empirisch belegte Ansätze / Handrechenformeln** — aus Experimenten gewonnene vereinfachte Gleichungen für spezifische Problemstellungen (z. B. Flammenhöhen, Wärmestrahlung, Rauchgasmassenströme); Gültigkeitsbereich und Fehlergrenze beachten
2. **Zonenmodelle / Mehrzonenmodelle** — vereinfachte Gleichungssysteme, mit empirischen Ansätzen aus Fundamentalgesetzen abgeleitet
3. **Feldmodelle / CFD (Computational Fluid Dynamics)** — unmittelbar auf Fundamentalgleichungen basierend, höherer Detaillierungsgrad

Unterschied Zonen- vs. Feldmodelle: Feldmodelle berücksichtigen die Impulserhaltung direkt, Zonenmodelle nicht — Strömungen durch Öffnungen müssen daher in Zonenmodellen a priori vorgegeben werden.

---

### 38.1 Handrechenformeln

#### Brandentwicklungsphasen

- **Pre-Flashover:** Abbrandrate und Wärmefreisetzungsrate vom Brandgut bestimmt, freie O₂-Versorgung, quadratischer Anstieg der Wärmefreisetzungsrate mit der Zeit
- **Flashover:** schlagartiger Übergang zum Vollbrand
- **Post-Flashover (Vollbrand):** Raum hat dominanten Einfluss auf das Brandgeschehen

Handrechenformeln gelten nur für die Pre-Flashover-Phase.

#### Mittlere Flammenhöhe

Definition (Zukoski): Höhe, bei der Flammen mehr als 50 % der Zeit vorhanden sind. Entspricht subjektiver Einschätzung des menschlichen Auges. Flammenhöhe schwankt in Frequenzen von 1–3 Hz.

**Heskestad-Korrelation (mittlere Flammenhöhe Lf):**  
Lf = 0,235 · Q^(2/5) − 1,02 · D  
Bei nicht kreisförmiger Brandquelle: D über flächengleiche Kreisfläche bestimmen.

**Radiative Anteil χr der Wärmefreisetzungsrate:** typisch 0,2–0,4; konvektive Wärmefreisetzungsrate Qc = Q · (1 − χr).

#### 38.1.1 Plume ohne Heißgasschicht

**Zukoski-Plume (Gl. 38.3/38.4):**  
Gilt wenn Flammenspitze deutlich von der Rauchgasschichtgrenze entfernt (frühes Brandstadium, hohe Räume, Freilandbrand).

mp = 0,071 · Qc^(1/3) · z^(5/3) [kg/s]  
(mit Standardwerten Ta = 293 K, ρa = 1,1 kg/m³, cp = 1,0 kJ/(kgK), g = 9,81 m/s²)

**Heskestad-Plume:**  
Gute Ergebnisse für Diffusionsflammen (Poolbrand). Virtueller Brandursprung z₀ kompensiert Abweichung von Punktquellannahme:  
z₀ = 0,083 · Q^(2/5) − 1,02 · D  
Bei großer Wärmefreisetzungsrate über kleiner Fläche kann z₀ positiv sein (liegt über Feuerquelle).

Temperaturerhöhung im Plume (Heskestad/Delichatisos):  
- Auf der Plume-Achse (r = 0): ΔTp = 25,5 · Qc^(2/3) · (z − z₀)^(−5/3) → Tp = Ta + ΔTp [K]
- Im Flammenbereich (z/Q^(2/5) < 0,08): ΔTp = 78,4 · Q^(2/5) / (z − z₀)
- Im Auftriebsplume-Bereich (z/Q^(2/5) ≥ 0,20): ΔTp = 25,5 · Qc^(2/3) · (z − z₀)^(−5/3)

Heskestad Plume-Massenstrom:  
- Oberhalb der Flammenspitze (z > Lf): mp = 0,071 · Qc^(1/3) · (z − z₀)^(5/3) + 1,92×10⁻³ · Qc
- Innerhalb der Flammen (z < Lf): mp = 0,0056 · Qc

**McCaffrey-Plume:**  
Drei Bereiche entlang der Zentralachse (Tab. 38.1):

| Bereich | z/Qc^(2/5) [m/kW^(2/5)] | η | κ |
|---|---|---|---|
| Ständige Flamme | < 0,08 | 1/2 | 6,8 [m^(1/2)/s] |
| Intermittierende Flamme | 0,08–0,2 | 0 | 1,9 [m/(kW^(1/5)·s)] |
| Auftriebsplume | > 0,2 | −1/3 | 1,1 [m^(4/3)/(kW^(1/3)·s)] |

Temperaturerhöhung: ΔTp = [κ · (z/Qc^(2/5))^η]² · (25,5 · g/(cp · Ta))^(−1)  
Plume-Massenströme (bereichsabhängig, Gl. 38.11a-c):
- Ständige Flamme: mp = 0,010966 · z^0,566 · Qc^0,7736
- Intermittierende Flamme: mp = 0,026080 · z^0,909 · Qc^0,6364
- Auftriebsplume: mp = 0,127493 · z^1,895 · Qc^0,242

McCaffrey-Versuche: Wärmefreisetzungsraten bis 57,5 kW — Vorsicht bei Anwendung auf größere Brände.

**Thomas/Hinkley-Plume:**  
Gilt für flache Brände (Lf/D < 1, mittlere Flammenhöhe kleiner als Branddurchmesser). Flammen tauchen in Rauchgasschicht ein.  
mp = 0,096 · π · D · z^(3/2) · (ρa · g · Ta/Tf)^(1/2)  
Vereinfacht (kreisförmiger Brand, Tf = 1100 K): mp = 0,59 · D · z^(3/2)  
Grundlage: Versuche bis 30 MW Leistung.

#### 38.1.2 Ceiling Jet

Ceiling Jet = relativ schnelle, flache Rauchgasströmung unterhalb der Decke, maßgebend für thermische Auslösung von Wärmemeldern, Sprinklern und RWA-Anlagen.

**Alpert-Korrelationen (Gl. 38.13)** — Basis: Versuche bei Wärmefreisetzungsraten 500 kW bis 100 MW, Deckenhöhen 4,6–15,5 m:

*Temperatur im Ceiling Jet (Tjet) bei Abstand r von der Plumeachse, Höhendifferenz H:*
- r/H ≤ 0,18: Tjet = Ta + 16,9 · Q^(2/3) / H^(5/3)
- r/H > 0,18: Tjet = Ta + 5,38 · (Q/r)^(2/3) / H

*Geschwindigkeit im Ceiling Jet (vjet):*
- r/H ≤ 0,15: vjet = 0,96 · (Q/H)^(1/3)
- r/H > 0,15: vjet = 0,195 · Q^(1/3) · H^(1/2) / r^(5/6)

**Beispielrechnung Ceiling Jet:**  
Ölbrand Q = 2 MW, D = 1,6 m, Deckenhöhe 6 m (Brandfläche auf 2 m Höhe → H = 4 m), Detektoren bei r = 5 m. Da r/H = 5/4 = 1,25 > 0,18:  
Tjet = 25 + 5,38 · (2000/5)^(2/3) / 4 = 98 °C  
Da r/H > 0,15: vjet = 0,195 · 2000^(1/3) · 4^(1/2) / 5^(5/6) = 1,29 m/s

**Sprinkler-Aktivierungszeit (Evans, Gl. 38.14):**  
tD,akt = (RTI / vjet^(1/2)) · ln[(Tjet − Ta) / (Tjet − TD,akt)]  
mit RTI = Response Time Index [m·s^(0,5)], TD,akt = Auslösetemperatur des Sprinklers.  
Beispiel: RTI = 100, TD,akt = 74 °C → tD,akt = (100/1,29^(1/2)) · ln[(98−25)/(98−74)] = 98,1 Sekunden

#### 38.1.3 Plume mit Heißgasschicht — Anwendungsbeispiel Rauchableitung

Iteratives Verfahren zur Dimensionierung natürlicher Rauchableitung (nach ISO/DIS 16735):

**Beispiel-Randbedingungen:**
- Raumhöhe H = 8 m, Grundfläche ABoden = 100 m²
- Deckenöffnungsfläche AÖffnung Decke = 2 m²
- Türöffnungsfläche AÖffnung Tür = 4 m²
- Wärmefreisetzungsrate Q = 300 kW, radiativer Anteil χ = 0,333
- Branddurchmesser D = 1 m
- Umgebungstemperatur Ta = 20 °C, ρa = 1,205 kg/m³, cp = 1,0 kJ/(kgK)
- Betonwände: dWand = 0,3 m, λ = 0,0015 kW/(mK), ρ = 1800 kg/m³, cp,Wand = 1,126 kJ/(kgK)

**Iterationsablauf (Konvergenz nach 4 Schritten → zs = 3,36 m, Ts = 37,5 °C):**

1. Startschätzung: zs = H/2 = 4 m
2. Plume-Massenstrom bei zs = 4 m: mp = 0,076 · (1−χ)^(1/3) · Q^(1/3) · zs^(5/3) = 4,48 kg/s
3. Effektiver Wärmetransferkoeffizient (Gl. 38.17, mit tc = 1000 s): hWand = 0,049 kW/(m²K) [wenn dWand ≥ λ·(4tc/ρ·cp)^(1/2)]
4. Rauchgasschicht-Temperatur: Ts = Q / (cp · mp + hWand · AWand) + Ta = 37,5 °C
5. Rauchdichte: ρs = 353 / (Ts + 273) = 1,137 kg/m³
6. Druckdifferenz an zs (Strömungskoeffizient CD = 0,7): Δp = (1/(2·ρa)) · (mp/(CD · AÖffnung Tür))² = 1,06 Pa
7. Massenstrom durch horizontale Deckenöffnung (Gl. 38.6):  
   me = CD · AÖffnung Decke · [2·ρs·(ρa−ρs)/ρa · (g·(H−zs) − Δp/ρa)]^(1/2) = 2,68 kg/s
8. Korrektur von zs mit (me + mp)/2 für numerische Stabilität → Iteration bis me = mp

Kontrolle: Flammenhöhe Lf = 0,235 · 300^(2/5) − 1,02 · 1 = 1,28 m (unterhalb zs = 3,36 m, Zukoski-Formel anwendbar).

---

### 38.2 Wärme- und Massenbilanzmodelle

#### Grundprinzip

Historisch für Vollbrandmodelle (Ein-Zonenmodell, post-Flashover) entwickelt; aus deren Einschränkungen resultierten Mehrzonenmodelle.

#### 38.2.1 Mehrzonenmodelle

Grundannahmen:
- Zwei stabile Gasschichten im Brandraum: heiße obere Rauchgasschicht und kühlere untere Luftschicht (rauchfrei oder raucharm)
- Trennung durch imaginäre horizontale Fläche, die Massenaustausch verhindert (außer Plume-Massenstrom und Sondereffekte)
- Jede Schicht hat eine einheitliche mittlere Temperatur
- Fluide in den Zonen werden als ruhend angenommen (außer Plume, Ceiling Jet, Ventilationsöffnungen)
- Druck P nur als Funktion der Höhe und Zeit
- Wandwärmeabgabe über eindimensionale instationäre Wärmeleitungsgleichung

**Druckverhältnisse im Brandverlauf (4 Fälle):**
- Fall A: kurz nach Brandbeginn, keine neutrale Ebene zn, kalte Raumluft strömt nach außen
- Fall B: ständiger Überdruck, bereits heiße Gase ausströmend ("stratified case")
- Fall C: negative und positive Druckdifferenzen über der Öffnung → neutrale Ebene bei Höhe zn; häufig modellierter Normalfall → Entwicklung zum Vollbrand
- Fall D: Vollbrand, zs = 0, Gaswechsel durch zn und Tg bestimmt ("well mixed")

Die Lage der neutralen Ebene (zn) muss nicht mit der Rauchgasschichtgrenze (zs) übereinstimmen.

**Massenbilanz (Gl. 38.18–38.22):**

mg (ausströmende Gasmenge) − ma (eintretende Luft) + mf (Abbrandrate) = 0

Ausströmender Gasmassenstrom (Öffnung, Höhe Hn bis H₀):  
mg = Cd · W · (2/3) · ρa · (2g·(Tg−Ta)/Ta)^(1/2) · Tg^(1/2) · (H₀ − Hn)^(3/2) ... [integrierte Form]  
(Cd = Einengungsfaktor ≈ 0,7; W = Öffnungsbreite in m; Hn = Höhe der neutralen Ebene)

Einströmender Luftmassenstrom (Höhe Hd bis Hn):  
ma enthält zwei Terme für Einströmung in beide Schichten.

Verknüpfung Abbrandrate und Wärmefreisetzungsrate:  
mf = Q / (A · ΔHc)

Abbrandrate und Plume-Massenstrom:  
mp = mf + ment (ment = Einmischungsrate von Luftmasse)

Für die meisten Brennstoffe: ca. 3000 kJ Wärme je kg zugeführter Luft (Sauerstoff).

**Erhaltung der Spezies:**  
Für CO₂, CO, HCN, Rußpartikel: Bilanzierung über Spezies-Erhaltungssatz und experimentell bestimmte Ausbeuten (Yields) der Brennstoffe.

**Energiebilanz (1. Hauptsatz):**

*Kaltgasschicht (Gl. 38.23a):*  
d(ml · El)/dt = ma · ha − ml · hl + ment · hl − Ql − Pl · dVl/dt  
- El: gespeicherte Energie pro kg in Kaltgasschicht
- ha/hl: Enthalpie einströmender Luft / Kaltgasschicht
- Ql: Netto-Wärmeabgabe der Wände zur Kaltgasschicht

*Heißgasschicht (Gl. 38.23b):*  
d(mg · Eg)/dt = mf · hf − ment · hg − mg · hg − Qg − Pg · dVg/dt  
- Eg: gespeicherte Energie pro kg in Heißgasschicht
- hf: Enthalpie der Brennstoffgase bei Tf
- hg: Enthalpie der Heißgasschicht bei Tg
- Qg: Netto-Wärmeabgabe der Wände zur Heißgasschicht

#### 38.2.2 Mehrraum-Mehrzonenmodelle

Erweiterung auf mehrere Räume mit unterschiedlichen Ventilationsöffnungen. Abflüsse aus einem Raum sind Zuflüsse des benachbarten Raums. Numerisch aufwändiger, Konvergenzrisiko steigt.

**Räume im Sinne des Rechenmodells:**
- Brand- oder Rauchabschnitte
- Einzelne baulich ausgebildete Räume
- Segmente zur Unterteilung eines Raums
- Hallenbereiche oder Räume mit Teilabtrennungen

**Grenzen der Zonenmodelle:**  
Stabile Zwei-Schicht-Voraussetzung gilt nicht mehr bei sehr großen Räumen. Erfahrungswert: Bis 3600 m² Grundfläche wurden in Experimenten stabile Schichtungen beobachtet; für größere Flächen fehlen Daten. Abstand Rauchgasgrenze zu Zuluftöffnungen muss ausreichend groß sein (sinkende Rauchgastemperatur → sinkende Schichtungsstabilität). Orientierung an DIN 18232-2.

---

### 38.3 Feldmodelle für die Brandsimulation (CFD)

#### 38.3.1 Erhaltungsgleichungen

Vier gekoppelte partielle Differentialgleichungen (Tensor-Notation, kartesische Koordinaten):

- **Gesamtmasse (Gl. 38.24a):** ∂ρ/∂t + ∂(ρui)/∂xi = 0  
  (Massenerhaltung: Dichteänderung = Netto-Massenfluss am Kontrollvolumen)

- **Komponentenmassen (Gl. 38.24b):** ∂(ρYα)/∂t + ∂(ρui·Yα)/∂xi + ∂jαi/∂xi = mα"  
  (Yα = Massenanteil Komponente α; mα" = chemischer Produktionsterm)

- **Impuls (Gl. 38.24c):** ∂(ρui)/∂t + ∂(ρui·uj)/∂xj = −∂p/∂xi + ∂τij/∂xj + fi  
  (Entspricht Newtons 2. Gesetz: Masse × Beschleunigung = Druckgradient + Reibung τij + Volumenkräfte fi wie Auftrieb)

- **Energie (Gl. 38.24d):** ∂(ρh)/∂t + ∂(ρui·h)/∂xi = Dp/Dt + ∂(τij·uj)/∂xj − ∂qi/∂xi + ε"  
  (h = spezifische Enthalpie; qi = Wärmestromdichte; ε" = Strahlungsquellterm)  
  In Brandsimulationen: Druckterm und Dissipationsterm vernachlässigbar, außer bei stark geschlossenen Räumen

#### 38.3.2 Vereinfachungen und Zustandsgleichungen

**Zustandsgleichung ideales Gas:**  
p = ρ · R · T / W  
W = Σ(Yα/Mα)^(−1) (mittleres Molekulargewicht aus Massenanteilen und Molekulargewichten der Komponenten)

**Newton'sches Fluid:**  
Schubspannung τij linear mit Geschwindigkeitsgradient (Scherung) verknüpft, mit dynamischer Viskosität μ (Gl. 38.28, Stokes-Beziehung: 2μ + 3μV = 0).

**Fick'sches Gesetz (Diffusion):**  
jαi = −ρ · Dα · ∂Yα/∂xi [Diffusionsmassenfluss]

**Fourier'sches Gesetz (Wärmefluss):**  
q"i = −λ · ∂T/∂xi + Σ(hα · jαi)  
(Dufour-Effekt vernachlässigbar)

**Niedergeschwindigkeitsannahme (low-Mach-number, für CFD-Brandmodelle üblich):**
- Druckschwankungen thermodynamisch vernachlässigbar
- Dissipation durch Reibung vernachlässigbar
- Dp/Dt ≈ dp/dt ≈ 0 bei fehlender signifikanter zeitlicher Druckänderung
- Kinetischer Energieanteil vernachlässigbar: H = h + u²/2 ≈ h

Kontinuumsannahme gilt, solange charakteristische Strömungslänge ls >> mittlere freie Weglänge L des Gases (L/η << 1, mit Kolmogorov-Länge η als kleinstes Längenmaß).

#### 38.3.3 Turbulenzmodellierung

**DNS (Direkte numerische Simulation):**  
Keine Modifikation der Gleichungen, alle Zeit- und Längenmaße direkt aufgelöst. Gitterauflösung < 1 mm erforderlich → für Raumbrände derzeit nicht wirtschaftlich.

**RANS (Reynolds-Averaged Navier-Stokes):**  
Zeitgemittelte Form der Erhaltungsgleichungen. Zerlegung jeder Größe φ in Mittelwert und Fluktuation: φ(x,t) = φ̄(x,t) + φ'(x,t). Mittlere Komponente variiert im Sekundenbereich, Fluktuationen im Millisekunden-Bereich.  
Turbulenzschließung: **k-ε-Modell** (Standardansatz kommerzieller CFD-Programme) — zwei zusätzliche Transportgleichungen für turbulente kinetische Energie k und Dissipationsrate ε; nicht aufgelöste Turbulenzen als Diffusionsterme (Eddy-Viskosität) modelliert.

**LES (Large Eddy Simulation):**  
Räumliche Filterung statt Zeitmittelung. Große Wirbel direkt simuliert, kleine Wirbel (Subgrid-Scale SGS) durch Modelle erfasst (z. B. Smagorinsky-Modell, 1963). Kein k-ε erforderlich, bessere Strömungscharakteristik, aber höhere Anforderungen an Gitterauflösung; Genauigkeit stark gitterabhängig.

#### 38.3.4 Quellterme und Randbedingungen

**Verbrennung:**  
Einfachster Ansatz: Wärmefreisetzung in fest definiertem Volumen, ohne Chemie — ausreichend für gut ventilierte Brände (Rauchtransport). Wenn O₂-Verfügbarkeit wichtig oder Gaszusammensetzung für Strahlungsmodell benötigt wird, ist ein Verbrennungssubmodell erforderlich.

Häufiger Ansatz: einstufige (schnelle) Reaktion → Brennstoff + O₂ → CO₂ + H₂O + Ruß + CO (Nebenkomponenten aus Experimenten). Für CO-Vorhersage nicht ausreichend.

- **RANS: Eddy-Breakup-Ansatz** (Spalding; Magnussen/Hjertager): Brennstoffverbrauch durch Rate der molekularen Vermischung kontrolliert, proportional zur Dissipationsrate der turbulenten Wirbel
- **LES: Mixture-Fraction-Ansatz (Mischungsbruch Z):** Feldvariable 0–1; Z = 1 reiner Brennstoff, Z = 0 reine Luft; Massenbrüche der Komponenten als Funktion von Z (Abb. 38.12 zeigt Beispiel für Ethen C₂H₄)

**Strahlungswärme:**  
Einfachste Näherung: Gas ohne Streuung, graues Gas (spektralunabhängig). Für Feuer angemessen, da Ruß dominanter Emitter/Absorber mit quasi-kontinuierlichem Spektrum. Bei stark abweichendem Verhalten: spektralabhängige Strahlungsintensität erforderlich.

**Massenrandbedingungen (Öffnungen, Lüftung):**  
Freie/offene Randbedingungen an Berechnungsdomänengrenzen, oder zeitlich vorgegebene Volumenströme/Geschwindigkeiten (mechanische Ventilation). Brennende Objekte: Brennstoffgase als Massenstrom aus Oberfläche vorgegeben.

**Impulsrandbedingungen (Wandfunktionen):**  
No-Slip-Bedingung an Festkörperoberflächen (Fluss = 0 direkt an Oberfläche). Wandfunktion: logarithmischer Ansatz für tangentiale Geschwindigkeitskomponente als Funktion des Normalenabstands → empirische Beziehung zwischen Wandscherspannung und aufgelösten Variablen am nächsten Gitterpunkt → Quellterme für jede Gleichung.

**Energierandbedingungen (konvektiver Wärmetransfer):**  
Konvektive Wärmetransferrate zur Wand:  
q"c = hc · (Tg − Tw)  
mit Tg = Gastemperatur am Gitterpunkt, Tw = Wandtemperatur, hc = konvektiver Wärmetransferkoeffizient.  
hc kann konstant angenommen werden (wie in Zonenmodellen) oder als Funktion des lokalen Strömungsfelds berechnet werden. Zu Brandbeginn: Wände auf Umgebungstemperatur → maximaler Wärmetransfer; mit steigenden Wandtemperaturen sinkt die Transferrate. Modellierung der Pyrolyse (brennende Oberflächen) ist noch Forschungsgegenstand.
