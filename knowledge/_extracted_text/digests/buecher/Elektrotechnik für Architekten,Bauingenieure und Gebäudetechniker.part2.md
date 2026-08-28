# Elektrotechnik für Architekten,Bauingenieure und Gebäudetechniker — Teil 2
> Quelle: Elektrotechnik für Architekten,Bauingenieure und Gebäudetechniker (buecher) · Seiten 81-120.

Dieser Teil des Lehrbuchs behandelt grundlegende Schaltungstheoreme für Gleichstromkreise (Brückenschaltung, Thevenin, Norton, Superposition), elektrische Quellen (ideal/real), Messverfahren, elektrostatische Felder mit Kondensatoren sowie elektromagnetische Felder mit magnetischen Kenngrößen. Der Fokus liegt auf mathematischen Grundlagen der Elektrotechnik für Nicht-Elektrotechniker.

## Inhalt

### Brückenschaltung (Kapitel 6, Fortsetzung)

- Brückenschaltung dient zur Messung eines unbekannten Widerstands Rx
- Abgleichbedingung: Spannung UAB = 0, wenn das Verhältnis R1/R2 = R3/R4 gilt
- Formel zur Berechnung des Unbekannten: Rx = R3 · R2 / R1

### Thevenin-Theorem (Lineare Ersatzspannungsquelle)

- Anwendungsfall: Verbraucher wechselt, Quelle bleibt konstant → Quelle wird durch Ersatzspannungsquelle vereinfacht
- Strom zwischen Klemmen A und B: IAB = UAB0 / (Ri + R)
- Berechnung des Eingangswiderstands: alle idealen Spannungsquellen werden als Kurzschluss behandelt, alle idealen Stromquellen als Unterbrechung

### Norton-Theorem (Lineare Ersatzstromquelle)

- Ein lineares Netzwerk kann durch eine Parallelschaltung aus Stromquelle und Widerstand ersetzt werden
- Der Strom im Netz entspricht dem Kurzschlussstrom, wenn die unabhängige Quelle unterbrochen ist
- Klemmenspannung: UAB = Ik / (Gi + G)

### Überlagerungssatz / Superpositionstheorem

- Bei mehreren Spannungsquellen in einem Netz mit linearen Bauelementen: Ströme und Spannungen können durch Addition der Einzelwirkungen berechnet werden
- Vorgehen: nacheinander jeweils eine Quelle aktiv lassen, alle anderen zu Null setzen
- Einzelteilströme werden anschließend nach Betrag und Richtung addiert

**Formeln (Zweimaschen-Beispiel mit U1, U2):**
- I21 = R2·U1 / (R1·R2 + R2·R3 + R3·R1)
- I31 = R3·U1 / (R1·R2 + R2·R3 + R3·R1)
- I11 = -I21 - I31
- I12 = R3·U2 / (R1·R2 + R2·R3 + R3·R1)
- I32 = R1·U2 / (R1·R2 + R2·R3 + R3·R1)
- I22 = -I12 - I32
- Resultierende Ströme: I1 = I11 + I12; I2 = I21 + I22; I3 = I31 + I32

---

### Kapitel 7: Elektrische Quellen

#### Grundbegriffe

- Aktive Zweipole halten an ihren Klemmen eine Spannung aufrecht und können durch angeschlossene passive Zweipole (Verbraucher) Strom treiben
- Aktive Zweipole: Spannungsquellen und Stromquellen
- Passive Zweipole: z. B. Ohmsche Widerstände
- Zur Analyse werden Ersatzschaltbilder mit idealisierten Quellen definiert

#### Ideale Spannungsquelle

- Liefert eine feste, von der Belastung unabhängige Spannung (eingeprägte Quellenspannung)
- Innenwiderstand = 0
- Klemmenstrom: I = U / RL, wobei U = Uq konstant

#### Reale Spannungsquelle

- Beispiele: galvanische Elemente, Batterien, Akkumulatoren, Thermoelemente, elektronische Spannungsquellen
- Charakterisierung durch drei Größen:
  - Leerlaufspannung U0
  - Kurzschlussstrom Ik
  - Innenwiderstand Ri
- Ersatzschaltung: ideale Spannungsquelle in Reihe mit Innenwiderstand
- Leerlaufmessung: UAB = U0 = UQ (keine Last angeschlossen)
- Kurzschlussmessung: Ik = UQ / Ri, dabei UAB = 0
- Innenwiderstand berechnet sich: Ri = U0 / Ik
- Bei linearem Innenwiderstand ergibt sich ein lineares Belastungsdiagramm; bei nichtlinearem Ri entsteht eine gekrümmte Kurve

#### Ideale Stromquelle

- Klemmenstrom I ist unabhängig von der Klemmenspannung → konstanter Strom

#### Reale Stromquelle

- Klemmenstrom sinkt mit wachsender Klemmenspannung

#### Zweipoltheorie

- Zweipol: Schaltung, die nur an zwei Punkten elektrisch zugänglich ist
- Für aktive und passive Zweipole werden jeweils Ersatzschaltbilder gebildet

#### Leistungsbilanz im Grundstromkreis

- Hoher Wirkungsgrad erfordert möglichst kleinen Innenwiderstand des Energieerzeugers (Ri → 0)
- Leistungsanpassung: maximale Leistung am Verbraucher RL wird erreicht, wenn Ri = RL
- Maximale Leistung am Lastwiderstand: PLmax = UQ² / (4 · Ri) = UQ² / (4 · RL)

---

### Kapitel 8: Messung elektrotechnischer Größen

#### Strommessung

- Strommessung erfordert Auftrennen des Stromkreises (Reihenschaltung des Messgeräts)
- Das Messgerät erhöht den Gesamtwiderstand → verfälscht das Ergebnis
- Idealforderung: Innenwiderstand des Strommessers Ri = 0 (praktisch nicht erreichbar, aber oft vernachlässigbar)

#### Spannungsmessung

- Spannungsmessgerät wird parallel zum Messobjekt geschaltet → kein Auftrennen nötig
- Messgerät stört dennoch den Stromkreis
- Idealforderung: Innenwiderstand des Spannungsmessers Ri → ∞
- Vielfachmessgeräte (Multimeter) minimieren Messfehler und bieten oft zusätzlich Widerstandsmessung

#### Spannungsquellen und Innenwiderstand

- Spannungsquellen: Batterien, Akkumulatoren, Generatoren, Transformatoren, Solarzellen, Mikrofone
- Gemeinsames Merkmal: erzeugen Spannung, bei Belastung (Stromlieferung) sinkt Klemmenspannung
- Spannungsabfall über Innenwiderstand steigt mit Belastung; Klemmenspannung sinkt entsprechend
- Im Kurzschlussfall: Strom wird nur durch Ri begrenzt, Klemmenspannung = 0
- Wenn Ri << RL → Quelle verhält sich wie Spannungsquelle
- Wenn Ri >> RL → Quelle verhält sich wie Stromquelle

#### Leistungsmessung bei Drehstrom

- Bei symmetrisch aufgebautem Drehstromnetz: Messung ohne Neutralleiter mit zwei Messgeräten möglich (Aron-Schaltung)
- Alternative: Messung mit Neutralleiter N
- Bei unsymmetrischem Netz: drei Messgeräte erforderlich
- Gesamtleistung: PG = P12 + P32

---

### Kapitel 9: Elektrische Felder

#### Feldtheorie — Grundkonzepte

- Elektrisches Feld: Raumgebiet um Ladungsträger, in dem Kräfte auf andere Ladungen wirken
- Darstellung durch Feldlinien: starten an positiven Ladungen, enden an negativen
- Skalares Feld: nur ein Wert pro Raumpunkt (z. B. elektrische Spannung U, Einheit V)
- Vektorielles Feld: Betrag und Richtung (z. B. elektrische Feldstärke E, Einheit V/m)
- Feldlinien können sich nicht schneiden (in jedem Punkt nur eine Wirkungsrichtung)
- Homogenes Feld: Betrag und Richtung überall gleich; inhomogenes Feld: variiert
- Äquipotentiallinien: Linien gleicher potentieller Energie; entlang dieser Linien wird keine Arbeit verrichtet
- Maxwell (1848) entwickelte die Feldtheorie; vier grundlegende Felder:
  1. Elektrisches Strömungsfeld im Leiter
  2. Elektrostatisches Feld im Nichtleiter
  3. Magnetisches Feld
  4. Elektromagnetisches Feld

#### Elektrisches Strömungsfeld

- Entsteht wenn Stromkreis geschlossen ist → freibewegliche Ladungsträger bewegen sich in Richtung der Kraft
- Elektronen bewegen sich entgegen der definierten Stromrichtung (positive Teilchen)
- Elektrische Stromdichte S proportional zur Feldstärke E; Proportionalitätsfaktor = elektrische Leitfähigkeit κ
- Feldstärke im Leiter: E = U / l
- Stromdichte: S = κ · E
- Temperaturabhängigkeit von Widerständen: Referenztemperatur 20 °C; Werte in DIN-VDE-Tabellen oder Herstellerkatalogen nach Leiterquerschnitt

#### Elektrostatisches Feld

- Ladungen ruhen, Stromdichte → 0
- Elektrische Feldstärke E: Zustand eines Raumes, verursacht durch elektrische Ladungen; Vektorfeld
- Positive Ladungen = Quellen, negative Ladungen = Senken des Feldes

##### Elektrische Spannung und Potential

- Elektrisches Potential φ = auf die Ladung bezogene Arbeit (Wpot / Q)
- Einheit: [φ] = V
- Potentialdifferenz = elektrische Spannung (skalare Größe)
- Spannung ist positiv, wenn Integral in Richtung des elektrischen Feldes berechnet wird
- Arbeit beim Verschieben der Ladung: W12 = F · s = Q · E · s

##### Elektrische Verschiebungsdichte D

- Beschreibt die Ursache des Feldes, unabhängig vom Raumzustand
- Gleiche Richtung wie Feldstärke E
- D = ε0 · εr · E
  - ε0 = elektrische Feldkonstante
  - εr = Materialkonstante (relative Permittivität)

##### Verschiebungsstrom

- Fließt nur bei Ladungs- oder Spannungsänderung am Kondensator
- Ermöglicht Stromfluss trotz nichtleitendem Dielektrikum zwischen den Platten
- iV = dQ/dt = dΦ/dt

##### Kondensator und Kapazität

- Kondensatoren: Bauelemente aus zwei Leitern mit isolierendem Dielektrikum dazwischen
- Einsatz: Glättung von Gleichrichterspannungen, Phasenverschiebung/Kompensation in Wechselstromkreisen, Ladungsspeicherung, HF-Schwingkreise
- Kapazität des Plattenkondensators: C = Q / U = ε0 · εr · A / d
  - A = Plattenfläche, d = Plattenabstand
- Einheit: [C] = F (Farad) = As/V
- Bedingung für homogenes Feld zwischen Platten: d << A (Randfelder vernachlässigbar)
- Gespeicherte Energie: W = ½ · C · U²
- Kondensator speichert Energie (reversibel), Widerstand wandelt Energie irreversibel in Wärme um

**Lade- und Entladevorgang (mit Vorwiderstand R):**
- Ladung: uC(t) = U0 · (1 - e^(-t/τ)); iC(t) = (U/R) · e^(-t/τ); Zeitkonstante τ = R · C
- Entladung: uC(t) = U0 · e^(-t/τ); iC(t) = -(U0/R) · e^(-t/τ)

##### Reihenschaltung von Kondensatoren

- Gleichung: 1/CG = 1/C1 + 1/C2 + 1/C3
- Für zwei Kondensatoren: CG = C1 · C2 / (C1 + C2)
- Gesamtkapazität kleiner als kleinste Einzelkapazität
- Anschaulich: Plattenabstand vergrößert sich, Kapazität sinkt (C ~ 1/d)
- Analog zur Parallelschaltung von Widerständen

##### Parallelschaltung von Kondensatoren

- Gleichung: CG = C1 + C2 + C3
- Gesamtkapazität = Summe der Einzelkapazitäten
- Anschaulich: Plattenfläche vergrößert sich, Kapazität steigt (C ~ A)
- Analog zur Reihenschaltung von Widerständen

#### Rechenbeispiele Kondensatoren

**Beispiel 1 (Reihen- und Parallelschaltung mit C1=2 µF, C2=4 µF, C3=6 µF):**
- Reihenschaltung: 1/CG = 1/2 + 1/4 + 1/6 µF = 0,916 µF⁻¹ → CG = 1,09 µF
- Parallelschaltung: CG = 2 + 4 + 6 = 12 µF

**Beispiel 2 (Gemischte Schaltung mit C1=0,1 µF, C2=0,5 µF, C3=0,15 µF, C4=0,2 µF):**
- Ca = C1·C2/(C1+C2) + C3 = (0,1·0,5)/(0,1+0,5) + 0,15 = 0,233 µF
- Cb = Ca·C4/(Ca+C4) = (0,233·0,2)/(0,233+0,2) = 0,107 µF

---

### Kapitel 10: Elektromagnetische Felder

#### Grundlagen und historische Einordnung

- Magnetische Erscheinungen seit Antike bekannt; Thales von Milet (624–546 v. Chr.) beschrieb magnetische Steine aus der Region Magnesia (Kleinasien)
- Chinesische Entdeckung der Richtungswirkung der Magnetnadel, vermutlich 2. Jh. v. Chr.; Magnetkompass gelangte im 12./13. Jh. über Araber nach Europa
- Hans Christian Oerstedt (1777–1851) entdeckte 1820 die magnetische Wirkung des elektrischen Stroms

**Kausale Kette:**
- Ladungen erzeugen elektrische Felder
- Elektrische Felder üben Kräfte auf Ladungen aus
- Bewegen sich Ladungen → elektrischer Strom
- Elektrischer Strom erzeugt Magnetfeld
- Magnetfeld bewirkt Kräfte auf bewegte Ladungen

**Eigenschaften magnetischer Felder:**
- Keine magnetischen Ladungen vorhanden
- Magnetisches Feld ist quellenfrei
- Magnetische Feldlinien sind stets in sich geschlossen
- Magnetisches Feld ist ein quellenfreies Wirbelfeld

**Praktische Bedeutung:**
- Mit geringem Erregeraufwand lassen sich intensive Felder erzeugen
- Basis für wirtschaftliche Energieumwandlung: elektrisch ↔ mechanisch (Motoren, Generatoren)
- Relais und Transformatoren nutzen das Magnetfeld

#### Kraftwirkungen im elektromagnetischen Feld

- Stromdurchflossener Leiter im Magnetfeld erfährt Kraft (Lorentzkraft)
- Für ein Elektron mit Geschwindigkeit v senkrecht zum Magnetfeld: F = e · v · B
- Gesamtkraft auf Leiter = Summe aller Lorentzkräfte
- Bei senkrechter Anordnung von Magnetfeld und Leiter: F = I · l · B
  - F in N; I in A; l = wirksame Leiterlänge in m; B in T
- Einheit: [F] = A · m · Vs/m² = N

**Rechenbeispiel (Kraft zwischen parallelen Leitern):**
- Zwei parallele Leiter, Abstand 2 m, Länge 5 m, Strom 45 kA in gleicher Richtung
- F = k2 · I1 · I2 · l / d = 2 · 10⁻⁷ N/A² · 45000 A · 45000 A · 5 m / 2 m = 1012,5 N

#### Bestimmung der Stromrichtung

- Stromrichtung abhängig von Leiterbewegungsrichtung und Magnetfeldrichtung
- Rechtsschraubenregel (Schraubenregel): Drehrichtung der Schraube gibt Richtung der Feldlinien an

#### Magnetische Feldgrößen

##### Magnetische Feldstärke H

- Ursachengröße des Magnetfelds (analog zu D im elektrischen Feld)
- H = Θ / l (Durchflutung durch Leiterlänge)
- Einheit: [H] = A/m
- Nicht direkt messbar (im Gegensatz zu B), aber wichtig für Feldberechnungen

##### Magnetische Flussdichte B

- Wirkungsgröße des Magnetfelds (analog zu E im elektrischen Feld)
- Entspricht der Feldliniendichte; Dichte = Maß für Kraftwirkung
- B = µ0 · µr · H
  - µ0 = 4 · π · 10⁻⁷ Vs/Am (magnetische Feldkonstante)
  - µr = relative Permeabilität (in Luft: µr = 1)
- Einheit: [B] = Vs/m² = Wb/m² = T (Tesla)
- Grenzwert für 50-Hz-Netze: 100 µT

##### Magnetischer Fluss Φ

- Gesamtzahl der magnetischen Feldlinien durch eine Fläche A in homogenem Feld
- Φ = B · A
- Einheit: [Φ] = T · m² = Vs (Weber)

##### Durchflutungsgesetz

- Magnetischer Fluss wird durch elektrischen Strom verursacht
- Magnetische Wirkung proportional zu Strom I und Windungszahl N
- Magnetische Durchflutung: Θ = I · N (Einheit: A)
- Durchflutungsgesetz (Umlaufintegral): ∮ H · ds = µ · ΣIi
- Ströme in Richtung des Normalvektors (Rechtschraubensinn) sind positiv
- Summe aller Wirkungen (B) auf dem Umlauf = Summe aller Ursachen (I) innerhalb der erfassten Fläche
- Θ = ΣIi = ∮ H · ds

**Zusammenfassung Analogien:**
| Elektrisches Feld | Magnetisches Feld |
|---|---|
| Elektrische Spannung: ∫ E · ds = U | Durchflutung: ∮ H · ds = Θ |
| Elektrische Teilspannungen: ∫ H · ds = V12 | — |

##### Magnetischer Kreis

- Analog zum elektrischen Kreis: Spannung treibt Strom durch Widerstand (U = R · I)
- Beim magnetischen Kreis bleiben Feldlinien im Material geschlossen
- Durchflutung als "Antrieb": Θ = Φ · Rm (Rm = magnetischer Widerstand)
- Magnetischer Leitwert (Permeanz): Λ = 1/Rm; Einheit: [Λ] = Vs/A
- Ohmsches Gesetz des magnetischen Kreises: Φ = Θ · Λ
- Berechnung mit Kirchhoffschen Gleichungen analog zum elektrischen Kreis möglich

**Rechenbeispiel (magnetischer Kreis mit Luftspalt):**
- Eisenkern: Querschnittsfläche A = 10 cm², Länge lFe = 100 cm, µr,Fe = 1000
- Luftspalt: Länge lLuft = 1 mm, µr,Luft = 1
- Gesamtmagnetwiderstand: Rm,ges = Rm,Luft + Rm,Fe (Reihenschaltung)
  - Rm,ges = lLuft/(µ0 · µr,Luft · A) + lFe/(µ0 · µr,Fe · A) = 80,3 · 10³² A/Vs

#### Magnetische Eigenschaften der Materie

##### Ferromagnetismus

- Ferromagnetische Stoffe (z. B. Eisen Fe) haben große verstärkende Wirkung auf das Magnetfeld
- Permeabilitätszahl µr >> 1:
  - Eisen, unlegiert: µr > 6000
  - Elektroblech: µr > 6500
- Hysterese-Erscheinung: nach erstmaliger Magnetisierung bis Sättigung und Abschalten des Erregerstroms verbleibt Remanenzflussdichte Br im Kern
- Entmagnetisierung erfordert Energiezufuhr oder ein entgegengesetztes Feld
- Koerzitivfeldstärke -Hc: bei dieser Feldstärke wird die Flussdichte im Kern wieder B = 0
- Wechselstromdurchfluss führt zu periodischem Durchlaufen der Hystereseschleife

##### Paramagnetismus

- Paramagnetische Stoffe (z. B. Aluminium Al): ungeordnete magnetische Dipole, zeigen ohne äußeres Feld keine magnetische Wirkung
- Im äußeren Feld richten sich Dipole in Feldrichtung aus → schwache Verstärkung
- Permeabilitätszahl µr geringfügig größer als 1

##### Diamagnetismus

- Diamagnetische Stoffe (z. B. Kupfer Cu): überlagerte Kreisströme zweier entgegengesetzt umlaufender Elektronen heben sich auf
- Permeabilitätszahl µr < 1 (leichte Abschwächung des Magnetfelds)
