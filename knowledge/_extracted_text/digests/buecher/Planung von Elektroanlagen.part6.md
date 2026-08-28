# Planung von Elektroanlagen — Teil 6
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 241-280.

Dieser Teil behandelt die abschließenden Aspekte der Kabel- und Leitungsdimensionierung (Kapitel 10), die Bemessung von Schutzleitern und Potentialausgleichsleitern (Kapitel 11), die Berechnung von Blindleistung und Kompensationsanlagen (Kapitel 12) sowie die Grundlagen der Erdungsplanung in Schaltanlagen inklusive Sternpunktbehandlung und Erderarten (Kapitel 13).

## Inhalt

### Umrechnungsfaktoren für abweichende Umgebungstemperaturen (Tabelle 10.6)

Korrekturfaktoren zur Anpassung der Strombelastbarkeit an die tatsächliche Umgebungstemperatur (Referenztemperatur 30 °C):

| Umgebungstemperatur (°C) | 40 °C zul. Betr.temp. | 60 °C | 70 °C | 80 °C | 85 °C | 90 °C |
|---|---|---|---|---|---|---|
| 10 | 1,73 | 1,29 | 1,22 | 1,18 | 1,17 | 1,15 |
| 15 | 1,58 | 1,22 | 1,17 | 1,14 | 1,13 | 1,12 |
| 20 | 1,41 | 1,15 | 1,12 | 1,10 | 1,09 | 1,08 |
| 25 | 1,22 | 1,08 | 1,06 | 1,05 | 1,04 | 1,04 |
| 30 | 1,00 | 1,00 | 1,00 | 1,10 | 1,00 | 1,00 |
| 35 | 0,71 | 0,91 | 0,94 | 0,95 | 0,95 | 0,96 |
| 40 | — | 0,82 | 0,87 | 0,89 | 0,90 | 0,91 |
| 45 | — | 0,71 | 0,79 | 0,84 | 0,85 | 0,87 |
| 50 | — | 0,58 | 0,71 | 0,77 | — | 0,82 |
| 55 | — | 0,41 | 0,61 | 0,71 | — | 0,76 |
| 60 | — | — | 0,50 | 0,63 | — | 0,71 |
| 65 | — | — | 0,35 | 0,55 | — | 0,65 |
| 70 | — | — | — | 0,45 | — | 0,58 |
| 75 | — | — | — | 0,32 | — | 0,50 |
| 80 | — | — | — | — | — | 0,41 |
| 85 | — | — | — | — | — | 0,29 |

### Thermische Kurzschlussfestigkeit — Berechnung

- Bei Kurzschlüssen mit Dauer Tk abweichend von Tkr gilt für den thermisch gleichwertigen Strom: Ith = Ithr · √(Tkr / Tk)
- Alternativ zur Stromgröße kann die thermisch gleichwertige Kurzzeitstromdichte verwendet werden, wenn Sth ≥ Sthr · √(Tkr / Tk) × 1/γ
- Der Faktor γ berücksichtigt Wärmeabgabe an die Isolierung während der Kurzschlussdauer
- Bemessungskurzzeitstromdichte Sthr ergibt sich aus Leiterwerkstoff-Kennwerten (Dichte ρ, spez. Widerstand α₂₀, Anfangs- und Endtemperatur des Leiters)

Begriffe:
- I''k: Anfangskurzschlusswechselstrom (kA)
- Ith: thermisch gleichwertiger Kurzschlussstrom (kA)
- Ithr: Bemessungskurzzeitstrom (kA)
- Tkr: Bemessungskurzschlussdauer (s)
- Tk: tatsächliche Kurzschlussdauer (s)
- Sthr: Bemessungskurzzeitstromdichte (A/mm²)
- Sth: thermisch gleichwertige Kurzzeitstromdichte (A/mm²)
- θe: Leitertemperatur bei Kurzschlussende (°C)
- θb: Leitertemperatur bei Kurzschlussbeginn (°C)
- ρ: Dichte des Stromleiters (g/cm³)
- κ: Stoßfaktor
- α: Temperaturkoeffizient des elektrischen Widerstands (1/°C)
- γ: Faktor für Wärmeabgabe an die Isolierung

### Belastbarkeits-Tabellen (10.7 und 10.8)

- Tabelle 10.7 gibt Belastbarkeitswerte für in Erde verlegte Kabel mit U0/U = 0,6/1 kV nach DIN VDE 0276 Teil 603:2005-01
- Tabelle 10.8 entsprechend für Kabel in Luft verlegt, gleicher Norm

### Querschnittsdimensionierung (Abschnitt 10.7)

Maßgebliche Kriterien für die Querschnittswahl:
- Thermische Belastbarkeit einschließlich aller Korrekturfaktoren
- Auswahl und Einstellung der zugehörigen Überstromschutzeinrichtungen (ÜSE)
- Kabellänge — begrenzt durch Spannungsfall, erforderliche Wirksamkeit der Schutzmaßnahmen und zulässige Berührungsspannung im Fehlerfall
- Thermische Kurzschlussfestigkeit

Formel für den rechnerischen Kabelquerschnitt (ohne Tabellen-Ableseverfahren):

S₀ = z^α · (IB / (z · f1 · f2 · f3 · f4))^β

Variablenbedeutungen:
- S₀: rechnerischer Kabelquerschnitt
- z: Anzahl parallelgeschalteter Kabel
- IB: Betriebsstrom des Verbrauchers
- f1: Reduktionsfaktor Verlegungsart
- f2: Reduktionsfaktor Umgebungstemperatur
- f3: Reduktionsfaktor Häufung
- f4: Reduktionsfaktor für parallelgeschaltete Kabel (0,95)
- β: Exponent, gilt für alle Kabeltypen = 0,625
- α: konstanter Faktor, abhängig von Cu oder Al

### α-Faktor für Cu- und Al-Kabel (Tabelle 10.10)

| Kabelart | α-Faktor Cu | α-Faktor Al |
|---|---|---|
| 4-adrige und 3½-adrige Kabel | 0,0143 | 0,1214 |
| 1-adrige Kabel gebündelt | 0,0121 | 0,0181 |
| 1-adrige Kabel nebeneinander | 0,0089 | 0,0133 |

### Erwärmungsverlauf bei abweichenden Betriebsarten

- Beim Aussetzbetrieb (periodisches Ein- und Ausschalten) liefert einfache quadratische Mittelwertrechnung keine korrekten Ergebnisse
- Erwärmung verläuft annähernd nach: Δθ = Δθn · (1 − e^(−t/τ₀))
- Begriffe: Δθ = Erwärmung zur Zeit t, Δθn = Enderwärmung, τ₀ = Mindestzeitwert (nach 5·τ₀ wird Endtemperatur erreicht), ED = relative Einschaltdauer, tB = Belastungszeit, ts = Spieldauer

### Mindestzeitwerte τ₀ (Tabelle 10.11)

| Leiterquerschnitt (mm²) | τ₀ Kupfer (s) | τ₀ Aluminium (s) |
|---|---|---|
| 1,5 | 30 | 20 |
| 2,5 | 48 | 30 |
| 4 | 70 | 48 |
| 6 | 100 | 65 |
| 10 | 160 | 105 |
| 16 | 240 | 155 |
| 25 | 350 | 220 |
| 35 | 480 | 305 |
| 50 | 650 | 410 |
| 70 | 850 | 590 |
| 95 | 1200 | 750 |
| 120 | 1400 | 900 |
| 150 | 1700 | 1100 |
| 185 | 2050 | 1300 |
| 240 | 2500 | 1600 |
| 300 | 3100 | 2000 |

### Bemessung von Überstromschutzeinrichtungen (Abschnitt 10.8)

Sicherungsbemessung für Motoranläufe:
- Anlaufstromverhältnis bei herkömmlichen Motoren: Ian / IrM = 5
- Grundbedingung: k · In > Ian, also In > 5 / (k · IrM)
- Für Sicherungen ≤ 50 A: k = 3,5 → In > 1,7 · IrM
- Für Sicherungen ≤ 63 A: k = 5 → In > 1,2 · IrM
- Bei Motorschutzschalter mit magnetischer Schnellauslösung: k = 1,25 für < 63 A, k = 1,35 für > 63 A
- Einstellstrom des Schnellauslösers: Ie > (5 / 1,25) · IrM = 4 · IrM

Kabelauslegungsregeln:
- Sicherungsabgänge ohne eigenen thermischen Überlastschutz → Kabel auf Bemessungsstrom der vorgeschalteten Sicherung auslegen
- Sicherungsabgänge mit getrenntem Überlastschutz (Motorschutzschalter o.ä.) → Kabel für eingestellten Auslösestrom bzw. Motorbemessungsstrom auslegen

#### Beispiel: Kabeldimensionierung Motor (Abschnitt 10.8.1)

Drehstrommotor, periodisch ein-/ausgeschaltet, kühlt sich in Pausen auf Umgebungstemperatur ab.
- Betriebszeit: 5 min, stromlose Pause: 10 min → Spieldauer ts = 15 min
- Bemessungsstrom: 76 A, Cu-Leiter, 40 °C Umgebungstemperatur, gemeinsame Verlegung auf Pritschen
- Relative Einschaltdauer: ED = tB / ts · 100 %

1. Abschätzung: 4 × 16 mm² Cu → Iz = 47 A, τ₀ = 240 s
   - ts / τ₀ = 900 / 240 = 3,75 → n = 1,2 → I = 1,2 × 47 = 56 A → reicht nicht aus
2. Abschätzung: 3 × 25/16 mm² Cu → Iz = 63 A, τ₀ = 350 s
   - ts / τ₀ = 900 / 350 = 2,57 → n = 1,2 → I = 2,57 × 63 = 80 A → reicht aus
- Für Dauerbetrieb hätte die Rechnung 3 × 35/16 mm² ergeben

Motor-Kabeltabelle (ohne und mit Umrechnungsfaktoren):

| Parameter | ohne Faktoren | mit Faktoren |
|---|---|---|
| IB | 81,1 A | 81,1 A |
| In | 100 A | 125 A |
| Iz | 96 A | 153,8 A |
| Querschnitt | 25 mm² | 3 × 70/35 mm² |
| Ia | 573 A | 751 A |

#### Beispiel: Leitungsberechnung 100-km-Freileitung (Abschnitt 10.8.2)

Gegeben: 100 km Freileitung, Abnehmerleistung 16 MW, cos φ = 0,6, Querschnitt 185 mm², Blindwiderstand 0,4 Ω/km, Leiterspannung 110 kV

Leiterstrom:
- IL = P / (√3 · U · cos φ) = 16 MW / (√3 · 110 kV · 0,6) = 140 A

Leiterblindwiderstand:
- RL = ρ · l / S = 0,0178 · 100 km / 185 mm² = 9,62 Ω

Verluste:
- Wirkleistungsverluste: Pv = 3 · I² · RL = 3 · (140)² · 9,62 = 565 kW
- Blindleistungsverluste: QL = 3 · I² · XL = 3 · (140)² · 40 × 10⁻³ = 2350 kvar

Eingangsgrößen:
- P1 = P2 + Pv = 16,565 MW
- Q2 = P2 · tan φ₂ = 16 MW · 1,33 = 21,35 MVar
- Q1 = Q2 + QL = 21,35 + 2,35 = 23,7 MVar
- S1 = √(P1² + Q1²) = 28,9 MVA
- cos φ₁ = P1 / S1 = 0,573

### Beispiel: Sicherungsbemessung (Abschnitt 10.9)

Schaltbild mit Transformator und Kabel. Vereinfachte Impedanzwerte aus Diagrammen:
- ZT = 0,03 Ω, ZL (Kabel) = 0,426 Ω/km

Einpoliger Kurzschlussstrom:
- ZL = 2 · l · Z'L = 2 · 0,250 km · 0,426 Ω/km = 0,213 Ω
- ZG = ZT + ZL = 0,03 + 0,213 = 0,243 Ω
- Ik = c · Un / (√3 · ZG) = 0,9 · 400 V / (√3 · 0,243) = 855,33 A

Sicherungsauswahl:
- In ≤ 1,45 · Iz / 1,6 = 1,45 · 310 A / 1,6 = 280,93 A → gewählt: 315 A
- Abschaltbedingung: 1,6 · 310 A = 504 A (muss durch Kurzschlussstrom erfüllt sein)

### Zusammenfassung Kabelberechnung (Abschnitt 10.10)

Leitung ist zentrale Schnittstelle zwischen Erzeuger und Verbraucher. Maßgebliche Normen:
- Zulässige Strombelastbarkeit nach DIN VDE 0298-4
- Überlastschutz: DIN VDE 0100-430
- Kurzschlussschutz: DIN VDE 0100-430
- Spannungsfall: DIN VDE 0100-520, TAB, DIN 18015
- Schutz gegen elektrischen Schlag: DIN VDE 0100-410

Referenznormen (Kapitel 10):
- DIN VDE 0298-4:2013-06 (Strombelastbarkeit feste Verlegung)
- DIN IEC 60364-4-43 / VDE 0100-430:2010-10 (Schutz bei Überstrom)
- DIN VDE 0276-1000:1995-06 (Starkstromkabel — Strombelastbarkeit, Umrechnungsfaktoren)
- DIN VDE 0100-520:2013-06 (Kabel- und Leitungsanlagen)

---

### Kapitel 11: Bemessung des Schutzleiters

Grundlage: DIN VDE 0100 Teil 540. Querschnitt entweder tabellarisch (DIN VDE 0100-540) oder rechnerisch (DIN VDE 0100-430) ermitteln.

#### Hauptschutzleiter — Querschnittsberechnung (Abschnitt 11.1)

Für Abschaltzeiten bis 5 s:

SPEN = √(IF² · t) / k

Variablen:
- t: Abschaltzeit der ÜSE (s)
- IF: Fehlerstrom = kleinster Kurzschlussstrom (A)
- k: Materialbeiwert / spezifischer Leiterfaktor (A·√s / mm²)
- S: Leiterquerschnitt (mm²)

Zuordnung Hauptschutzleiter zu Außenleiter (Tabelle 11.1, international genormt):

| Außenleiterquerschnitt S (mm²) | Schutzleiterquerschnitt (mm²) |
|---|---|
| S ≤ 16 | S (gleich wie Außenleiter) |
| 16 < S ≤ 35 | 16 |
| S > 35 | S / 2 |

#### Hauptpotentialausgleichsleiter — Querschnitt (Tabelle 11.2)

| Bedingung | Querschnitt |
|---|---|
| Normalfall | 0,5 · SPEN |
| Mindestwert | 6 mm² Cu |
| Obergrenze | 25 mm² Cu |

#### Schutzleiter zu Betriebsmitteln (Abschnitt 11.2)

Querschnitt des Schutzleiters von Potentialausgleichsschiene zu einzelnen Betriebsmitteln:

SPE = SPEN / 2

#### Schutzpotentialausgleichsleiter (Abschnitt 11.3)

Maßgebend ist der Querschnitt der stärksten abgehenden Leitung vom Hauptverteiler:

SPA = SPE / 2

#### Zusätzlicher Schutzpotentialausgleichsleiter (Abschnitt 11.4)

Notwendig, wenn DIN VDE 0100 Teil 410 nicht eingehalten werden kann, sowie bei Räumen mit erhöhter Gefährdung (z.B. Bäder).

Querschnitte (Tabelle 11.3):

| Verbindung | Querschnitt |
|---|---|
| Zwischen zwei Gehäusen / Körpern | Querschnitt des kleineren Schutzleiters |
| Körper mit fremden leitfähigen Teilen | Halber Querschnitt des zugehörigen Schutzleiters |

Mindestquerschnitt in jedem Fall:
- Mit mechanischem Schutz: 2,5 mm²
- Ohne mechanischen Schutz: 4 mm²

#### Zusammenfassung Schutzleiter (Abschnitt 11.5)

- Schutzleiter leitet Fehlerstrom zur Quelle zurück → ermöglicht schnelle Abschaltung
- Querschnitt nach DIN VDE 0100-540 wählen oder nach DIN VDE 0100-430 berechnen
- Im TT-System können wegen geringerer Erdungsströme kleinere Querschnitte gewählt werden
- Durchgängige Verlegung des Schutzleiters ist unverzichtbar

---

### Kapitel 12: Spannungsänderung und Blindleistung

Blindleistung und Spannungsqualität sind eng miteinander verknüpft; entsprechende Normen und Vorschriften sind einzuhalten.

Netzebenen-Besonderheiten:
- Hochspannung: Wirkwiderstände gegenüber Reaktanzen vernachlässigbar; Transformatoren mit lastverstellbaren Stufenschaltern (380/220 kV, 220/110 kV, 110/20 kV)
- Nieder- und Mittelspannung: Transformatoren 20/0,4 kV ohne lastverstellbare Stufenschalter; nur feste Wicklungsanzapfungen (z.B. ±2,5 % und ±4 %)
- Blindleistung soll am Entstehungsort kompensiert werden; Blindlastfluss über längere Strecken vermeiden

#### Grundbegriffe Blindstromkompensation (Abschnitt 12.1)

- Leistungsfaktor: Kennzeichnung eines Verbrauchers bezüglich Wirkleistungsaufnahme; bei reinen Sinusgrößen 50 Hz gleich dem Verschiebungsfaktor
- Verschiebungsfaktor: Qualitätsbewertungsgröße für Motoren und Antriebe
- Blindleistung: Leistung zum Aufbau elektromagnetischer Felder; wird nicht in nutzbare Energie umgesetzt
- Blindleistungsregler: misst cos φ, gibt Schaltbefehle an Kondensatoren (zu- oder abschalten)
- Kompensation: entlastet Betriebsmittel von Blindstromanteilen, erhöht Leistungsfaktor, erlaubt mehr Wirkleistungsübertragung
- Einzelkompensation: Kondensator direkt an Verbraucherklemmen (z.B. Motor)
- Gruppenkompensation: gemeinsame Kompensationseinrichtung für eine Verbrauchergruppe (z.B. Motorengruppe, Leuchtstofflampen)
- Zentralkompensation: eine Regeleinheit für alle Verbraucher zentral
- Festkompensation: ein oder mehrere Kondensatoren einem Verbraucher fest zugeordnet, ggf. mitgeschaltet

Wirtschaftliche Vorteile der Kompensation:
- Einsparung von Blindstromkosten
- Einsparung von Investitionskosten
- Senkung der Spitzenleistung
- Entlastung der Kraftwerke
- Spannungshaltung im Netz
- Verringerung erforderlicher Kabel-/Leitungsquerschnitte

Nichtlineare Verbraucher (Stromrichter, Dimmer, Lichtbogenöfen, Induktionsöfen) erzeugen Oberschwingungen → Maßnahmen gegen Oberschwingungen und Leistungsfaktorverbesserung müssen gemeinsam betrachtet werden.

#### Berechnung der Blindleistung (Abschnitt 12.3)

Grundgrößen nach DIN 40 110:
- Rein ohmsche Verbraucher: P = U · I (Spannung und Strom in Phase)
- Ohmsch-induktive Verbraucher: P = U · Iw, Q = U · IL
- Gesamtstrom: I = √(Iw² + IL²)
- Scheinleistung: S = √(P² + Q²)
- Leistungsfaktor: cos φ = P / S
- Bei verzerrtem Strom: λ = |P| / S = g · cos φ (g = Grundschwingungsgehalt)

Blindleistungsverbesserung (cos φ₁ → cos φ₂):
- QC = P · (tan φ₁ − tan φ₂)
- tan φ = √((1 − cos²φ) / cos²φ)

Kapazität des Kompensationskondensators:
- C = QC / (Un² · 2π · f)
- Bei Dreieckschaltung: CY = C / 3

Vereinfachungen:
- Bei 400 V, 50 Hz: CY ≈ 20 · QC (μF bei QC in kvar)
- Bei 230 V, 50 Hz: CY ≈ 60 · QC

#### Mittlere Leistungsfaktoren nach Anlagenarten (Tabelle 12.1)

| Anlagentyp | Leistungsfaktor |
|---|---|
| Bäckereien, Brauereien, Fleischereien, Kühlhäuser | 0,60–0,70 |
| Molkereien | 0,60–0,80 |
| Mühlen | 0,60–0,70 |
| Sägewerke, Sperrholzfabriken | 0,60–0,70 |
| Trockenanlagen | 0,80–0,90 |
| Möbel- und Bautischlereien | 0,60–0,70 |
| Kompressoren | 0,60–0,70 |
| Ventilatoren | 0,70–0,80 |
| Gießereien | 0,60–0,70 |
| Krananlagen | 0,50–0,60 |
| Wasserpumpen | 0,80–0,85 |
| Kfz-Werkstätten | 0,70–0,80 |
| Mechanische Werkstätten | 0,50–0,60 |

#### Planungsablauf für Kompensationsanlagen (Abschnitt 12.4)

Sieben Schritte:
1. Wahl der Kompensationsart (Einzel-, Gruppen- oder Zentralkompensation)
2. Ermittlung der Anlagendaten
3. Auswahl der Verdrosselung
4. Berechnung der erforderlichen Kompensationsleistung
5. Klärung der Umgebungs- und Aufstellungsbedingungen
6. Ermittlung der Kompensationsmodule
7. Ansteuerung der Kondensatorstufen

#### Berechnungsbeispiel: Kompensation einer Anlage (Abschnitt 12.5)

Gegeben: 120 kW, cos φ = 0,74 (φ₁ = 42,26°)

1. Kompensation auf cos φ = 1:
   - QC = 120 kW · tan 42,26° = 109 kvar

2. Kompensation auf cos φ = 0,95 (φ₂ = 18,19°):
   - QC = 120 kW · (tan 42,26° − tan 18,19°) = 69,6 kvar

3. Kapazitäten bei 400 V, 50 Hz:
   - Dreieckschaltung: C = 69,6 kvar / (3 · 400² · 2π · 50) = 461 μF
   - Sternschaltung: CY = 3 · C = 1383 μF

#### Berechnungsbeispiel: Transformator-Einzelkompensation (Abschnitt 12.6)

Gegeben: 630 kVA, 20/0,4 kV, ukr = 6 %

1. Kompensation bei Leerlauf (i₀ = 3 %):
   - Q₀ = (i₀ / 100) · SrT = 3 % / 100 · 630 kVA = 18,9 kvar

2. Kompensation bei 70 % Belastung:
   - QT = Q₀ + (ukr / 100) · (n · SrT / SrT)² · SrT
   - QT = 18,9 + (6% / 100) · (0,7)² · 630 = 37,422 kvar

#### Berechnungsbeispiel: Resonanzgefahr bei Kondensatoren (Abschnitt 12.7)

Maximale Kondensatorleistung zur Vermeidung von Resonanzerscheinungen:
- QC < SrT · 100 / (h² · ukr)

Beispiel: Resonanz bis 13. Oberschwingung vermeiden:
- QC < 630 kVA · 100 / (13² · 6 %) = 62,13 kvar
- Kondensatorleistung muss unterhalb dieses Wertes bleiben

#### Berechnungsbeispiel: Gesamtanlage mit Leistungsfaktorerhöhung (Abschnitt 12.8)

Gegeben: P = 550 kW, cos φ₁ = 0,73

Vor Kompensation:
- S = 550 / 0,73 = 753,42 kVA (überschreitet Trafo-Nennleistung → Anlage überlastet)
- I = 550 / (√3 · 400 · 0,73) = 1087,47 A

Nach Kompensation auf cos φ₂ = 0,98:
- S = 550 / 0,98 = 561,22 kVA (Trafo nicht mehr überlastet)
- I = 550 / (√3 · 400 · 0,98) = 810 A

Erforderliche Kompensationsleistung:
- QC = 550 kW · (tan 47,9° − tan 12,75°) = 511,58 kvar

---

### Kapitel 13: Erdungen in Schaltanlagen

#### Begriffe (Abschnitt 13.1)

- Erde: Bezeichnung für Ort oder Stoff (Erdboden als elektrischer Leiter)
- Bezugserde: neutrale Erde außerhalb des Einflussbereichs des Erders
- Erder: leitfähiges Teil, das in die Erde eingeschlagen wird und mit ihr elektrischen Kontakt hat
- Erden: Verbinden leitfähiger Teile mit der Erde über eine Erdungsanlage
- Erdungsanlage: Gesamtheit aller miteinander verbundenen Erder
- Ausbreitungswiderstand: Wirkwiderstand zwischen der Erdungsanlage und der Bezugserde
- Erdungsspannung: Potentialdifferenz zwischen Erdungsanlage und Bezugserde
- Berührungsspannung: jener Teil der Erdungsspannung, den ein Mensch gleichzeitig berühren kann
- Schrittspannung: jener Teil der Erdungsspannung, der bei einem Schrittabstand von 1 m überbrückt werden kann
- Potentialsteuerung: gezielte Beeinflussung des Erdpotentials durch zusätzliche Erder
- Erdkurzschlussstrom: tritt in Netzen mit niederohmiger Sternpunkterdung auf
- Erdfehlerstrom: Strom, der an der Fehlerstelle vom Betriebsstromkreis zur Erde oder zu geerdeten Teilen übertritt
- Kapazitiver Erdkurzschlussstrom: entsteht in Netzen mit isoliertem Sternpunkt
- Erdschlussreststrom: entsteht in Netzen mit Erdschlusskompensation
- Erdungsstrom: Gesamtstrom, der über die Erdungsimpedanz in die Erde fließt
- Niederspannungsbetriebserder: für Betrieb des NS-Netzes notwendige Erdung des Neutralleiters, dient auch Personenschutz gegen Berührungsspannung
- Hochspannungsschutzerder: unmittelbare Erdung nicht zum Betriebsstromkreis gehöriger leitfähiger Teile, Schutz gegen Berührungs- und Schrittspannung

Erdungsarten: Schutzerdung, Betriebserdung, Blitzschutzerdung

Normen für Planung und Projektierung von Erdungsanlagen in Hochspannungsanlagen:
EN 50522, DIN VDE 0141, DIN VDE 0100, DIN VDE 0101, DIN VDE 0102, DIN VDE 0150, DIN VDE 0151, IEC 62305 (VDE 0185-305), EN 50423, EN 50341, DIN 18104

#### Erdung eines Umspannwerks (Abschnitt 13.1.1)

Auslegungsparameter:
- Höhe des Fehlerstroms abhängig von der Sternpunktbehandlung
- Spezifischer Erdwiderstand
- Fehlerdauer

Bei niederohmiger Sternpunkterdung: Erdfehlerstrom fließt teilweise über Transformatorsternpunkt und Erdseile zurück; nur Erdungsstrom verursacht Potentialanhebung.

Formeln:
- IE = rE · (IF − IN) (Erdungsstrom im Umspannwerk)
- IF = 3 · I₀ + IN (Fehlerstrom gesamt)
- UE ≥ 2 · UT (Erdungsspannung ≥ doppelte Berührungsspannung)
- ZE = 1 / (1/RES + n · 1/Z₁) (Erdungsimpedanz)
- Vereinfachte Berechnung: RE = UE / I''k1min mit I''k1min = √3 · cmin · Un / (2Z₁ + Z₀)
- UE = IE · ZE

Variablen:
- I₀: Nullstrom
- IF: Fehlerstrom
- IE: Erdungsstrom
- rE: Reduktionsfaktor
- RES: Ausbreitungswiderstand der Masche
- Z₁: Kettenleiterimpedanz
- n: Anzahl der abgehenden Leitungen

#### Berechnung der zulässigen Berührungsspannung (Abschnitt 13.1.2)

- Wirkungsbereiche von Körperströmen und Körperinnenimpedanzen nach IEC 60479-1
- Höchste zulässige Berührungsspannung in NS- und HS-Netzen nach IEC 60479-1 und EN 50522
- Maximal zulässige Dauerberührungsspannung in der Hochspannung: 80 V ab einer Fehlerdauer von 5 s
- Kurzzeitig sind mehrere 100 V zulässig (bei niederohmiger oder erdschlusskompensierter Sternpunkterdung)
- In Netzen mit isolierter Sternpunkterdung: Berührungsspannung begrenzt auf 80 V für Fehlerdauern > 10 s

Berechnungsformel (zulässige Berührungsspannung):
- UTp = IB(tf) · (1/HF) · ZT(UT) · BF

Mit Zusatzwiderständen (Leerlaufberührungsspannung):
- UvTp = IB(tf) · (1/HF) · (ZT(UT) · BF + RH + RF)

Variablen:
- IB: zulässiger Körperstrom, abhängig von Fehlerdauer (EN 50522 Tab. B.1)
- UTp: zulässige Berührungsspannung (EN 50522 Abb. B.4)
- UvTp: zulässige Leerlauf-Berührungsspannung
- RH: zusätzlicher Handwiderstand
- RF: zusätzlicher Fußwiderstand (EN 50522 Abb. B.2)
- tf: Fehlerdauer
- ZT: Körperimpedanz (EN 50522 Tab. B.2)
- BF: Korrekturfaktor für Körperimpedanz

#### Auslegungsverfahren der Erdungsanlage (Abschnitt 13.1.3)

Vorgehen:
1. Spezifischen Erdwiderstand messen
2. Gesamtimpedanz der Erde aus Erdfehlerstromanteil berechnen
3. Erdungsspannung bestimmt zulässige Berührungsspannung
4. Bei globalem Erdungssystem gilt UE ≤ 2 · UTp immer → keine nennenswerten Berührungs-/Potentialdifferenzen

#### Art der Sternpunkterdung (Abschnitt 13.2)

Sternpunktbehandlung beeinflusst Nullimpedanz des Netzes und damit das Verhalten bei Erdfehlern (einpoliger Fehler tritt häufig auf). Stationärer Netzbetrieb bleibt unberührt.

Transformator-Nullimpedanzen im Vergleich:
- Stern-Dreieck: Nullimpedanz ≈ 0,8–1,0 × Mitimpedanz
- Stern-Zickzack: Nullimpedanz ≈ 1/10 der Mitimpedanz
- Stern-Stern mit Dreiecksausgleichswicklung (1/3 der Durchgangsleistung): bis 2,4 × Mitimpedanz
- Dreischenkel Stern-Stern ohne Ausgleichswicklung: 5–10 × Mitimpedanz (Streuflussproblematik → nicht für Systemerdung)
- Mantel- oder drei 1-Phasen-Transformatoren in Stern-Stern: Nullimpedanz ≈ Leerlaufimpedanz → ungeeignet für Systemerdung

Geeignete Transformatorkonfigurationen für Erdschlussspulen oder niederohmige Widerstände:
- Stern-Dreieck-Schaltung
- Stern-Stern mit tertiärer Dreieckwicklung

Sternpunktbildner (Zickzackspulen):
- Große Leerlaufimpedanz, kleine Nullimpedanz
- Kann mit erhöhter Nullreaktanz zur Strombegrenzung ausgelegt werden; dann direkte Erdung möglich
- In Mittelspannungsnetzen kann Sternpunktbildner zusätzlich als Netztransformator dienen (mit Sekundärwicklung)

Sternpunktbehandlung beeinflusst:
- Berührungs-, Schritt- und Erderspannungen
- Einpolige Kurzschlussströme
- Spannungsbeanspruchung

Aufgaben der Erdung:
- Schutz vor Kurz- und Erdschlüssen bei 50 Hz
- Schutz vor transienten Vorgängen (Blitz, Schalthandlungen)

Nach EN 50522 und DIN VDE 0228 werden vier Arten der Sternpunktbehandlung unterschieden:

##### 13.2.1 Isolierte Sternpunkterdung

- Erdschlussstrom fließt über die Erdkapazitäten CE der fehlerfreien Leiter
- Einsatzgebiet: kleine Mittelspannungsnetze
- Kleine Erdkapazitäten → kleine Erdschlussströme, die in kleinen Netzen meist von selbst verlöschen
- Jedoch können hohe transiente Überspannungen auftreten
- Fehlerfreie Leiter-Erde-Spannungen steigen auf verkettete Leiterspannungen an
- Kapazitiver Erdschlussstrom: 10 A < ICE ≤ 35 A
- ICE = 3 · ω · CE · c · Un / √3

##### 13.2.2 Kompensierte Sternpunkterdung (Erdschlusskompensation)

- Sternpunkt über Erdschlussspule (Petersen-Spule) mit Erde verbunden
- Löschgrenze bestimmt Übergang isoliert → kompensiert; Differenz ca. 20 A
- Löschung durch auf Netzkapazität abgestimmte Induktivität der Erdschlussdrossel
- An Fehlerstelle fließt nur Erdschlussreststrom
- Fehlerfreie Leiter-Erde-Spannungen steigen ebenfalls auf verkettete Werte
- Löschgrenzen nach DIN VDE 0228: 20-kV-Netze → 60 A; 110-kV-Netze → 130 A
- IC = 3 · ω · CE · c · Un / √3; IL = c · Un / (√3 · ω · L)
- Resonanzbedingung: ω · LE = 1 / (3 · ω · CE)
- Reststrom: Ir = √((ICE − IL)² + Iw² + ΣI²w)
- Im Idealfall (v = 0): Ir(v=0) = 0,08 · ICE
- Zulässiger Erdungswiderstand: RE ≤ UE / Ir ≤ 2 · UT / Ir

##### 13.2.3 Niederohmige Sternpunkterdung (direkte Sternpunkterdung)

- Sternpunkt eines oder mehrerer Transformatoren direkt geerdet
- Netzschutz muss bei Erdschluss automatische Abschaltung sicherstellen
- In HS-Netzen: Erdfehlerströme durch Wirk- oder Blindwiderstand auf unter 2 kA begrenzt
- Einsatz in Freileitungsnetzen oder gemischten Netzen (kurzzeitig niederohmige Erdung)
- In Niederspannung: Sternpunkt direkt geerdet, Fehlerdauer < 1 s
- I''k1 = √3 · cmin · Un / (2 · Z₁ + Z₀)

#### Erderarten (Abschnitt 13.3)

Berechnungsgrundlage: Halbkugelerder mit Fehlerstrom IE, der gleichmäßig in alle Richtungen abfließt.

Erdungsspannung: UE = RE · IE (nimmt mit Entfernung vom Fehlerort ab)

Schrittspannung im Potentialfeld im Abstand r:
- US = IE · ρE / (2π) · (1/r₁ − 1/r₂)

Wichtige Erderarten:
- Fundamenterder: in Beton eingebettet, großflächiger Erdkontakt
- Oberflächenerder: Verlegung bis 1 m Tiefe (z.B. Band- oder Maschenerder)
- Tiefenerder: lotrecht in großen Tiefen verlegt
- Steuererder: vorwiegend zur Potentialsteuerung
- Natürlicher Erder: steht direkt oder über Beton mit Erde oder Wasser in Verbindung; unter Bedingungen als Erder nutzbar

Ausbreitungswiderstände:

**a) Tiefenerder** (wenn x >> d):
- RE = ρE / (2π · l) · ln(4l / d)
- Potentialverteilung: φx = IE · ρE / (2π · l) · ln[l/x + √(1 + (l/x)²)]

**b) Banderder**:
- RE = ρE / (π · l) · ln(2l / d)
- Potentialverteilung: φx = IE · ρE / (π · l) · ln[(l/2) / √(h² + x²) + √(1 + (l/(2√(h² + x²)))²)]
- Vereinfacht (l ≤ 10 m): RA = 2 · ρE / l
- Vereinfacht (l > 10 m): RA = 3 · ρE / l

**c) Maschenerder**:
- RE ≈ ρE / (2D) + ρE / ltotal
  (D = äquivalenter Kreisdurchmesser, ltotal = Gesamtlänge der Maschen-Leiter)
