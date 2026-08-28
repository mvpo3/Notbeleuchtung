# Planung von Elektroanlagen — Teil 1
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 41-80.

Das Werk von I. Kasikci (Springer-Verlag Berlin Heidelberg 2018) behandelt die vollständige elektrotechnische Planung von Anlagen. Dieser Teil (Seiten 41–80) deckt die Grundlagenkapitel der Drehstromtechnik ab: unsymmetrische Systeme, komplexe Rechnung, Leistungsbeziehungen im Drehstromsystem, Beispielrechnungen zur Wechselstromtechnik, die Methode der symmetrischen Komponenten sowie die Grundlagen der Kurzschlussstromberechnung nach DIN EN 60909-0 (VDE 0102) inklusive Kurzschlussimpedanzen der Betriebsmittel.

## Inhalt

### 2.5 Unsymmetrische Drehstromsysteme

Unsymmetrische Drehstromsysteme entstehen entweder durch unterschiedliche Erzeugerspannungen (Betrag und Phasenlage verschieden) oder durch ungleiche Lastimpedanzen. In der Praxis werden typischerweise ungleiche Lastimpedanzen betrachtet.

**Unsymmetrische Sternschaltung (mit Neutralleiter):**
- Außenleiterströme ergeben sich aus dem Quotienten der jeweiligen Phasenspannung zur zugehörigen Phasenimpedanz (I1 = U1/ZL1N, I2 = U2/ZL2N, I3 = U3/ZL3N).
- Der Neutralleiterstrom ist die vektorielle Summe aller drei Außenleiterströme: IN = I1 + I2 + I3.

**Unsymmetrische Dreieckschaltung:**
- Strangströme berechnen sich aus den verketteten Spannungen dividiert durch die jeweilige Zweigimpedanz (I12 = U12/Z12, I23 = U23/Z23, I31 = U31/Z31).
- Die komplexen Außenleiterströme werden durch Knotenregel aus den Strangströmen abgeleitet (z.B. I1 = I12 − I31).
- Die Summe aller drei Außenleiterströme ist null: I1 + I2 + I3 = 0.

### 2.6 Verkettungsfaktor

Der Verkettungsfaktor stellt den Zusammenhang zwischen Dreieckschaltung und Sternschaltung her:

- Verhältnis von Dreieckspannung (Außenleiterspannung) zu Sternspannung (Strangspannung) beträgt √3.
- Mathematisch: Udelta/UStern = √3
- Gleiches Verhältnis gilt für Ströme: der Außenleiterstrom ist das √3-Fache des Strangstroms (I = √3 · I_Str).

### 2.7 Zählpfeilsystem

Zur Beschreibung elektrischer Netzwerke werden zwei Zählpfeilsysteme verwendet:

- **Verbraucherzählsystem (VZS):** Spannungs- und Stromzählpfeile werden so gewählt, dass an einem Verbraucher berechnete Wirkleistungen und Blindleistungen positiv ausfallen (Leistungsaufnahme, Spannungsfall); an einem Erzeuger sind sie negativ (Leistungsabgabe, Spannungserzeugung).
- **Erzeugerzählsystem (EZS):** Umgekehrte Konvention.
- Die Festlegung der Richtung ist frei wählbar (willkürlich).

### 3. Einführung in die komplexe Rechnung

#### 3.1 Begriffe und Rechenregeln

Wechselstromgrößen werden mithilfe der komplexen Rechnung behandelt. Grundlage ist die Euler'sche Gleichung, die verschiedene Darstellungsformen komplexer Zahlen ermöglicht.

**Darstellungsformen einer komplexen Zahl Z:**
- Normalform (algebraische Komponentenform): Z = a + jb; Betrag |Z| = √(a² + b²); Realteil a = |Z|·cosα; Imaginärteil b = |Z|·sinα
- Trigonometrische Form: Z = |Z|·(cosα + j·sinα)
- Versorform: Z = |Z| ∠ α
- Exponentialform (Euler): Z = |Z|·e^(jωt)

Die Euler-Gleichung in Potenzreihendarstellung ergibt: e^(jx) = cos(x) + j·sin(x).

#### 3.2 Rechenregeln für komplexe Zahlen

- Addition/Subtraktion: nur in Komponentenform möglich; Real- und Imaginärteile werden separat addiert/subtrahiert.
- Multiplikation: Beträge werden multipliziert, Phasenwinkel addiert (in Exponentialform).
- Division: Betrag wird dividiert, Phasenwinkel subtrahiert.
- Spezielle Werte: j⁰ = 1; j¹ = j; j² = −1; j³ = −j; j⁴ = 1.

#### 3.3 Komplexe Größen der Wechselstromtechnik

Übertragung der komplexen Rechnung auf die Elektrotechnik:
- Impedanz als komplexe Größe: Z = |Z|·e^(jφ) = R + jX; R = Resistanz (Wirkwiderstand), X = Reaktanz (Blindwiderstand).
- Admittanz: Y = 1/Z = G + jB; G = Konduktanz (Wirkleitwert), B = Suszeptanz (Blindleitwert).
- Spannungszeiger: U = |U|·e^(jφu); Stromzeiger: I = |I|·e^(jφi).
- Erweitertes Ohm'sches Gesetz für Wechselstrom: Z = U/I = (|U|/|I|)·e^(j(φu − φi)).

Vorteile der Zeigerdarstellung:
- Numerische Berechnung mit Real-/Imaginärteil oder Betrag/Phasenlage.
- Grafische Darstellung mit Zeigerdiagrammen.
- Phasenverschiebung = Differenz der Nullphasenwinkel zweier Größen; abhängig von Schaltungsaufbau und Frequenz.

### 4. Leistungen im Drehstromsystem

Spannung und Strom als Momentanwerte im Wechselstromkreis:
- u(t) = Û·cos(ωt + φu); Effektivwert U = Û/√2
- i(t) = Î·cos(ωt + φi); Effektivwert I = Î/√2

**Komplexe Scheinleistung:** S = U·I* = |U|·|I|·e^(j(φu − φi)) = P + jQ

- Wirkleistung P: zeitlicher Mittelwert der Momentanleistung bei ohmscher Last; schwingt nur in eine Richtung um die Nulllinie; P = U·I (bei reiner ohmscher Last).
- Blindleistung Q: entsteht bei 90°-Phasenverschiebung zwischen Spannung und Strom; Momentanleistung schwingt symmetrisch um die Nulllinie; zeitlicher Mittelwert ist null; Q = U·I.
- Die Scheinleistungsformeln gelten sowohl für Stern- als auch für Dreieckschaltungen.

**Praxishinweis:** In jeder elektrischen Anlage sollte der Leistungsfaktor cos(φ) zwischen 0,95 und 1 liegen (Energieeffizienz).

### 5. Beispiele zur Wechselstromtechnik

#### 5.1 Sinusspannung (Beispielrechnung)

Gegeben: u(t) = 50·cos(30t + 10°)
- Amplitude: 50 V
- Periode: T = 2π/ω = 2π/30 = 209,4 ms
- Frequenz: f = 1/T = 4,775 Hz

#### 5.2 Sinusstrom (Beispielrechnung)

Gegeben: i(t) = 8·cos(500t − 25°)
- Amplitude: 8 A
- Kreisfrequenz: ω = 500·π = 1570,8 rad/s
- Frequenz: f = 1/T = 250 Hz

#### 5.3 Komplexe Größe (Beispielrechnungen)

Vereinfachung von Ausdrücken in Polarform und Umrechnung zwischen Darstellungsformen:
- Beispiel: Gegeben U = 5 V, R = 1 Ω, X = 2 Ω → Z = (1 + j2) Ω; |Z| = 2,24 Ω; I = (1 − 2j) A; Phasenwinkel φi = 63,4°.

#### 5.4 Belastung von Drehstromnetzen (Beispiel)

WS-Verbraucher: P₁ = 2,5 kW, cos(φ) = 0,85
- Betriebsstrom: I = P/(U₀·cos(φ)) = 2500/(230·0,85) = 12,78 A
- Impedanz: Z = 230/12,78 = 18 Ω (Realteil R = 13,71 Ω; Imaginärteil X = 11,65 Ω)

#### 5.5 Symmetrisches System (Beispiel)

Gegeben: 400 V, Z = (6 − j8) Ω
- Ströme: I1 = 44 A ∠53,13°; I2 = 44 A ∠−66,87°; I3 = 44 A ∠173,13°

#### 5.6 & 5.7 Komplexe Zahl in Polar- und Exponentialform

- Z = (6 + j8) Ω → Betrag 10 Ω, φ = arctan(8/6) = 53,13° → Polarform: 10∠53,13°; Exponentialform: 10·e^(j53,13°)
- u(t) = 325 V·cos(ωt + 60°); Ueff = 230 V, φ = 60° → Exponentialform: 230 V·e^(j60°); Komponentenform: (115,19 + j186) V

#### 5.8 Stern-Dreieck-Schaltung (Beispiel)

Berechnung der Strangströme bei unterschiedlichen Impedanzwinkeln:
- IAB = 400 V∠30°/50 Ω = 8 A∠30°
- IBC = 400 V∠−90°/50∠−90° = 8 A∠0°
- ICA = 400 V∠150°/50∠90° = 8 A∠60°

#### 5.9 Stern-Stern-Schaltung (Beispiel)

Berechnung von Leiterströmen und Neutralleiterstrom bei unterschiedlichen Phasenimpedanzen:
- Ia = 230 V∠0°/15 Ω = 15,33 A∠0°
- Ib = 230 V∠−120°/(10 + j5) Ω = 20,57 A∠−93,44°
- Ic = 230 V∠−120°/(6 − j8) Ω = 23 A∠−66,87°
- Neutralleiterstrom: IN = −(Ia + Ib + Ic) = (24,65 + j0,51) A = 24,65 A∠98,68°

#### 5.10 Mehrfachlast (Beispiel)

Last 1: P = 30 kW, cos(φ) = 0,6 (induktiv): S1 = 50 kVA; Q1 = 40 kvar; Komplexleistung S1 = (30 + j40) kVA
Last 2: Q = 45 kvar, cos(φ) = 0,8: S2 = 75 kVA; P2 = 60 kW; Komplexleistung S2 = (60 + j45) kVA

Gesamtleistung: S = (90 + j85) kVA = 123,8 kVA∠43,36°
- Strom Last 1: IL1 = 50 kVA/(√3·400 V) = 72,16 A
- Strom Last 2: IL2 = 85 kVA/(√3·400 V) = 122,68 A
- Gesamtstrom: IG = S/(√3·U) = 178,69 A

### 6. Symmetrische Komponenten

#### 6.0 Grundprinzip und Drehoperator

Die Methode der symmetrischen Komponenten dient zur Berechnung unsymmetrischer Fehler in Drehstromnetzen. Grundlage ist ein Drehoperator — eine komplexe Zahl mit Betrag 1, deren Multiplikation mit einem Zeiger diesen dreht ohne seinen Betrag zu ändern.

Im Drehstromsystem sind die Winkel 120° und 240° von besonderer Bedeutung. Der Drehoperator für 120° wird mit „a" bezeichnet:
- a = e^(j120°) = −1/2·(1 − j√3)
- a² = e^(j240°) = −1/2·(1 + j√3)
- a³ = 1
- Summe: 1 + a + a² = 0

Mithilfe dieser Drehoperatoren lassen sich die drei Phasenspannungen in der komplexen Zahlenebene darstellen: UR = UR; US = a²·UR; UT = a·UR.

Außenleiterspannungen im symmetrischen System:
- URS = UR − US = √3·UR·e^(j30°)
- UST = US − UT = √3·UR·e^(j270°)
- UTR = UT − UR = √3·UR·e^(j150°)

#### 6.1 Mit-, Gegen- und Nullsystem

Das Dreiphasensystem wird in drei unabhängige einpolige Systeme zerlegt:

**Mitsystem (Index 1 oder m):**
- Symmetrisches mitlaufendes Drehstromsystem in normaler Phasenlage.
- Ersatzschaltung und Betriebsmitteldaten identisch mit der einpoligen Ersatzschaltung zur Berechnung des dreipoligen Kurzschlusses.
- Genügt für symmetrische Fehler (dreipoliger Kurzschluss).

**Gegensystem (Index 2 oder i):**
- Symmetrisches gegenlaufendes Drehstromsystem.
- Für ruhende Betriebsmittel (Freileitungen, Kabel, Transformatoren) gilt: Gegenimpedanz = Mitimpedanz.
- Bei drehenden Maschinen: Gegenimpedanz kann kleiner als Mitimpedanz sein.

**Nullsystem (Index 0):**
- Drei Ströme gleicher Größe und gleicher Phasenlage.
- Rückleitung über einen vierten Leiter; im Rückleiter fließt der dreifache Nullstrom.
- Berücksichtigung der Sternpunktschaltung: ungeerdet / über Erdschlusslöschspule geerdet / über Widerstand oder Reaktanz geerdet / direkt geerdet.

**Berechnungsschritte für unsymmetrische Fehler:**
1. Drehstromnetz mit Fehler im RST-Raum zeichnen.
2. Fehlerbedingungen aufstellen.
3. Einphasiges Ersatzschaltbild im Komponentenraum (120-Raum) zeichnen.
4. Ströme und Spannungen im Komponentenraum berechnen.
5. Unsymmetrische Fehlerströme in den Originalraum (RST) rücktransformieren.

**Transformation RST ↔ Komponentenraum:**
- Rücktransformation (Komponentenraum → Original): IRST = T · I120
- Transformation (Original → Komponentenraum): I120 = S · IRST mit S = T⁻¹
- Komponentenströme: I0 = 1/3·(IR + IS + IT); I1 = 1/3·(IR + a·IS + a²·IT); I2 = 1/3·(IR + a²·IS + a·IT)

#### 6.2 Impedanzen der symmetrischen Komponenten

Jedem Komponentensystem wird eine eigene Impedanz zugeordnet:
- Mitimpedanz Z(1) = U(1)/I(1): entspricht der Impedanz einer einphasigen Ersatzschaltung im symmetrischen Betrieb; Summe der Impedanzen von Freileitungen, Maschinen und Bauelementen im Leiter.
- Gegenimpedanz Z(2) = U(2)/I(2): messtechnisch mit Gegensystemspannung bestimmt; bei passiven Betriebsmitteln gleich Z(1).
- Nullimpedanz Z(0) = U(0)/I(0): einphasig gemessen; drei Leiter werden parallel geschaltet; keine Phasenverschiebung zwischen den Einzelkomponenten.

Die Quellenspannung im Drehstromnetz tritt nur im Mitsystem auf und wird für Berechnungen auf den Wert c·Un/√3 gesetzt.

#### 6.3 Berechnungsbeispiele zu symmetrischen Komponenten

**6.3.1 Komponentenströme in einem Vierleiternetz:**
Gegeben: IR = 25 A, cos(φ) = 0,5 (induktiv); IS = 50 A, cos(φ) = 0,6 (kapazitiv); IT = 35 A, cos(φ) = 0,8 (induktiv)
- Nullstrom: I0 = 8,45 A∠27,37°
- Mitsystemstrom: I1 = 23 A∠−16,05°
- Gegensystemstrom: I2 = 29,58 A∠125,34°
- Neutralleiterstrom: IN = 3·I0 = 25,35 A∠27,37°

**6.3.2 Einpoliger Kurzschlussstrom:**
Gegeben: I''k1 = 30 kA·e^(j80°); IL2 = IL3 = 0
- I(0) = I(1) = I(2) = 10 kA·e^(j80°)

**6.3.3 Zweipoliger Kurzschlussstrom:**
Gegeben: I''k2 = 50 kA zwischen L1 und L2; IL1 = 0; IL2 = −j50 kA; IL3 = +j50 kA
- I(0) = 0
- I(1) = −j28,867 kA; I(2) = +j28,867 kA

**6.3.4 Symmetrische Last:**
Gegeben: U1 = 230 V∠0°; U2 = 230 V∠−120°; U3 = 230 V∠−240°; Z1 = Z2 = Z3 = (20 + j20) Ω
- Alle drei Ströme: I = 8,13 A (mit 120°-Versatz); I1 = 8,13 A∠−45°; I2 = 8,13 A∠−165°; I3 = 8,13 A∠−285°

**6.3.5 Unsymmetrische Fehler:**
Gegeben: IR = (4,7 + j2,4) A; IS = (1,6 + j2,3) A; IT = (1,8 − j1,7) A
- I(0) = (1,5 − j0,4) A; I(1) = (1,77 + j2,24) A; I(2) = (1,43 + j0,62) A

**6.3.6 Generatorspannungen:**
Drei Generatorspannungen mit U = 120 V Effektivwert:
- U1 = 120 V∠0°
- U2 = 120 V∠−120° = (−60 + j103,92) V (cos(−120°) = −0,5; sin(−120°) = −√3/2)
- U3 = 120 V∠−240° = (−60 − j103,92) V

**6.3.7 Zusammenfassung Drehstromsystem:**
- Generatoren erzeugen Spannungen mit 120°-Versatz bei gleicher Frequenz und gleichem Betrag.
- Summe der Momentanwerte ist stets null.
- Dreiphasige Systeme können in Stern oder Dreieck geschaltet werden; bei symmetrischer Last genügen drei Leiter; für Einphasenwechselstromverbraucher werden vier Leiter benötigt.
- Wirkleistung wird in andere Energieformen umgewandelt; Blindleistung pendelt zwischen Erzeuger und Verbraucher (Auf- und Abbau magnetischer Felder) und verursacht dabei Verluste.
- Empfohlener Leistungsfaktor in elektrischen Anlagen: 0,95 bis 1.

### 7. Kurzschluss und Erdschluss im Drehstromnetz (DIN EN 60909-0 / VDE 0102:2016-12)

Weltweit maßgebende Norm für Kurzschlussstromberechnung: IEC 60909-0 (europäisch umgesetzt als DIN EN 60909-0 / VDE 0102).

#### 7.1 Begriffe und Definitionen

| Begriff | Definition |
|---|---|
| Kurzschlussstrom | Strom hervorgerufen durch einen Kurzschluss in einem elektrischen Netz |
| Anfangs-Kurzschlusswechselstrom I''k | Effektivwert des Wechselstromkurzschlussstroms im Augenblick des Kurzschlusseintritts bei unveränderter Kurzschlussimpedanz |
| Anfangs-Kurzschlusswechselstromleistung S''k | Fiktive Rechengröße |
| Stoßkurzschlussstrom ip | Größtmöglicher Augenblickswert des Kurzschlussstroms |
| Dauerkurzschlussstrom Ik | Effektivwert des Kurzschlusswechselstroms nach vollständigem Abklingen aller Ausgleichsvorgänge |
| Gleichstromglied iDC | Mittelwert der Hüllkurven des Kurzschlussstroms, klingt langsam auf null ab |
| Ausschaltwechselstrom Ia | Effektivwert des Kurzschlussstroms zum Zeitpunkt der ersten Kontakttrennung |
| Ersatzspannungsquelle c·Un/√3 | Spannung an der Kurzschlussstelle (Mitsystem), einzige wirksame Spannung zur Kurzschlussstromberechnung |
| Spannungsfaktor c | Verhältnis Ersatzspannungsquelle zu Netznennspannung Un/√3 |
| Generatorferner Kurzschluss | Symmetrische Wechselstromkomponente bleibt im Wesentlichen konstant |
| Generatornaher Kurzschluss | Symmetrische Wechselstromkomponente nicht konstant; Anfangskurzschlussstrom > 2-facher Bemessungsstrom der Synchronmaschine |

**Ursachen von Kurzschlüssen in elektrischen Anlagen:**
- Isolationsdurchbruch durch Alterung
- Übertemperatur von Leitern/Isolation durch zu hohe Belastungsströme oder Umgebungstemperaturen
- Dauernde Überspannungen oder Teilentladungen
- Überschläge durch Feuchtigkeit in Verbindung mit Luftverschmutzung (besonders an Isolatoren)
- Mechanische Beschädigung der Isolation (Baustellen, hoch beanspruchte Handgeräte)
- Menschliches Versagen (Fehlschaltungen, leitfähige Gegenstände, Nichtbeachten von Sicherheitsregeln)

**Auswirkungen von Kurzschlussströmen:**
- Thermische und dynamische Beanspruchung von Betriebsmitteln (Kabel, Leitungen, Sammelschienen, Schalt- und Schutzgeräte)
- Druckbelastung in gekapselten Schaltanlagen durch Störlichtbögen
- Entstehung von Überspannungen und gefährlichen Berührungsspannungen
- Gefährdung von Menschen und Tieren
- Zerstörung von Anlagenteilen
- Unterbrechung der Energieversorgung
- Verringerung von Sicherheit und Zuverlässigkeit der Stromversorgung

**Kurzschlussarten:**
1. Dreipoliger Kurzschluss
2. Zweipoliger Kurzschluss ohne Erdberührung
3. Zweipoliger Kurzschluss mit Erdberührung
4. Einpoliger Erdkurzschluss
5. Doppelerdkurzschluss (kapazitiver Erdschlussstrom ICE; Erdschlussreststrom IRest)

Für vollständige Berechnungen genügen in den meisten Fällen der Anfangs-Kurzschlusswechselstrom I''k und der Stoßkurzschlussstrom ip.

#### 7.2 Knotenpunktverfahren

Berechnung der Fehlerströme in einfachen oder vermaschten Netzstrukturen:
- Ausgangspunkt ist das Ersatzschaltbild aller Betriebsmittel mit den Kirchhoff'schen Gesetzen.
- Kurzschlussstromberechnung ist ein lineares Problem → Lösung mit linearen Gleichungssystemen.
- Knotenpunktadmittanzmatrix Y verknüpft Knotenströme mit Knotenspannungen: i = Y·u.
- Alle Impedanzen werden auf die Unterspannungsseite der Transformatoren umgerechnet.
- Im Gegensatz zur Lastflussberechnung ist keine Iteration erforderlich.
- Anfangs-Kurzschlusswechselstrom am Knotenpunkt i: I''ki = −c·Un/(√3·Zii)
- Knotenspannungen: Uk = Zki · I''ki

#### 7.3 Verfahren der Ersatzspannungsquelle

Grundprinzip (nach DIN EN 60909-0):
- Der dreipolige Anfangs-Kurzschlusswechselstrom I''k3 ist maßgebend für die Bemessung auf thermische und dynamische Beanspruchungen.
- Vereinfachungsannahme: Berechnung unabhängig vom aktuellen Betriebszustand und zukünftigen Lastflüssen.
- Alle Netzeinspeisungen, Generatoren und Motoren werden hinter ihren inneren Reaktanzen kurzgeschlossen.
- Die Ersatzspannungsquelle c·Un/√3 ist die einzige treibende Spannung im Netz.
- Größter Kurzschlussstrom I''k3: für Bemessung der Betriebsmittel maßgebend.
- Kleinster Kurzschlussstrom I''k1: maßgebend für Schutzmaßnahme „Schutz durch Abschaltung" und Einstellung des Netzschutzes.
- Kurzschlussimpedanz an der Fehlerstelle: Zk = (RQt + RT + RL) + j(XQt + XT + XL)

**Spannungsfaktor c nach DIN EN 60909-0:2016-12 (Tab. 7.1):**

| Netznennspannung Un | cmax (größter KS-Strom) | cmin (kleinster KS-Strom) |
|---|---|---|
| Niederspannung 100 V bis 1000 V (Toleranz ±6 %) | 1,05 | 0,95 |
| Niederspannung 100 V bis 1000 V (Toleranz ±10 %) | 1,10 | 0,90 |
| Hochspannung > 1 kV bis 380 kV | 1,10 | 1,00 |

Hinweis: cmax·Un darf die höchste Betriebsspannung Um für Betriebsmittel nicht überschreiten.

Einführung des Spannungsfaktors c ist notwendig wegen:
- Unterschiedlichen Betriebsspannungen im Netz
- Subtransientem Verhalten von Generatoren, Kraftwerksblöcken und Motoren
- Vernachlässigung von Lasten und Leitungskapazitäten
- Vernachlässigung des stationären Betriebszustandes

**Bedingungen für kleinste Kurzschlussströme:**
- Spannungsfaktor cmin verwenden.
- Motoren vernachlässigen.
- Wirkwiderstände von Leitungen bei Kurzschlussendtemperatur einführen.
- Netzschaltung und minimale Kraftwerks-/Netzeinspeisungen wählen (→ I''kQmin / ZQmax).

**Bedingungen für größte Kurzschlussströme:**
- Spannungsfaktor cmax verwenden.
- Netzschaltung und maximale Kraftwerks-/Netzeinspeisungen wählen.
- Bei Verwendung von Ersatzimpedanzen ZQ: kleinste Kurzschlussimpedanz wählen (= größter Kurzschlussstrom der Netzeinspeisung).
- Motoren berücksichtigen.
- Wirkwiderstände von Leitungen bei 20 °C einführen.

#### 7.4 Kurzschlussimpedanzen der Betriebsmittel

**7.4.1 Netzeinspeisung:**

Netzinnenimpedanz ZQ am Anschlusspunkt Q:
- Berechnung aus Anfangs-Kurzschlusswechselstromleistung S''kQ oder Anfangs-Kurzschlusswechselstrom I''kQ:
  - S''kQ = √3·UnQ·I''kQ
  - ZQ = c·UnQ/(√3·I''kQ) = c·U²nQ/S''kQ
- Wenn RQ/XQ bekannt: XQ = ZQ/√(1 + (RQ/XQ)²)
- Maximaler/minimaler Einspeisstrom:
  - I''kQmax = cmax·UnQ/(√3·ZQmin)
  - I''kQmin = cmin·UnQ/(√3·ZQmax)
- Umrechnung auf Unterspannungsseite des Transformators: ZQt = (c·UnQ/(√3·I''kQ))·(1/t²r)
- Wenn RQ nicht bekannt: XQ = 0,995·ZQ; RQ = 0,1·XQ

Symbole: UnQ = Nennspannung Anschlusspunkt; S''kQ = Anfangs-Kurzschlusswechselleistung; I''kQ = Anfangs-Kurzschlusswechselstrom; tr = Bemessungsübersetzungsverhältnis bei Hauptanzapfung.

**7.4.2 Beispiel: Netzeinspeisung 110-kV-Netz**

Gegeben: UnQ = 20 kV (Unterspannungsseite); I''kQ = 10 kA; cmax = 1,1; RQ = 0,1·XQ; XQ = 0,995·ZQ; Übersetzungsverhältnis 110 kV/20 kV

Ergebnisse:
- ZQt = 1,1·110 kV/10 kA·(20/110)² = 0,23 Ω
- XQt = 0,995·0,23 = 0,228 Ω
- RQt = 0,1·0,228 = 0,0228 Ω
- ZQt = (0,0228 + j0,228) Ω

**7.4.3 Synchrongeneratoren:**

Die Kurzschlussströme werden hauptsächlich durch die Reaktanz der Synchrongeneratoren bestimmt. Die Reaktanz verändert sich zeitlich in drei Phasen (subtransient → transient → stationär); besonders in der Anfangsphase entstehen sehr hohe Kurzschlussströme.

Für die Berechnung des Anfangs-Kurzschlusswechselstroms I''kG wird der subtransiente Teil verwendet (Ersatzschaltung mit E'').

Widerstandswerte für Generatoren:
- Niederspannungsgeneratoren (UrG < 1000 V): RG = 0,15·X''d
- Hochspannungsgeneratoren (UrG > 1 kV) mit SrG ≥ 100 MVA: RG = 0,05·X''d
- Hochspannungsgeneratoren (UrG > 1 kV) mit SrG < 100 MVA: RG = 0,07·X''d

Subtransiente Reaktanz: X''d = x''d·U²rG/(100%·SrG)

Die Faktoren 0,15/0,05/0,07 berücksichtigen das Abklingen des Kurzschlusswechselstroms während der ersten Halbperiode.

Symbole: X''d = subtransiente Reaktanz; x''d = bezogene subtransiente Reaktanz in %; RG = Ständerresistanz; ZG = Generatorimpedanz.

**Typische Reaktanzwerte von Synchronmaschinen (Tab. 7.2):**

| Reaktanz | Turbogenerator | Schenkelpolgenerator mit Dämpferwicklung | Schenkelpolgenerator ohne Dämpferwicklung |
|---|---|---|---|
| Anfangsreaktanz x''d (gesättigt) | 9–22 % | 12–30 % | 20–40 % |
| Übergangsreaktanz x'd (gesättigt) | 14–35 % | 20–45 % | 20–40 % |
| Synchronreaktanz xd (ungesättigt) | 140–300 % | 80–180 % | 80–180 % |
| Gegenreaktanz x2 | 9–22 % | 12–30 % | 20–40 % |
| Nullreaktanz x0 | 3–10 % | 5–20 % | 5–25 % |

Anmerkungen zur Tabelle:
- Dämpferwicklung gilt für lamellierte Polschuhe mit vollständiger Dämpferwicklung und auch für massive Polschuhe mit Laschenverbindungen.
- Steigende x''d-Werte mit steigenden Maschinenleistungen; kleinere Werte bei NS-Generatoren.
- Höhere x''d-Werte bei Schenkelpolgeneratoren ohne Dämpferwicklung gelten für Langsamläufer (n < 375 min⁻¹).
- Bei sehr großen Maschinen (über 1000 MVA): x'd bis 40–45 %.
- Gesättigte Synchronreaktanzwerte sind 5–20 % kleiner als ungesättigte.
- Allgemeine Näherung für Gegenreaktanz: x2 ≈ 0,5·(x''d + x''q); gilt auch für transienten Vorgang.
- Nullreaktanz hängt von der Sehnung der Wicklung ab.

**7.4.4 Dreipoliger Kurzschluss am Generator:**

Zeitlicher Verlauf des Kurzschlussstroms bei Kurzschluss an den Generatorklemmen:
- Anfangs: größter Stoßkurzschlussstrom (Überlagerung subtransienter, transienter und stationärer Anteile mit Gleichstromglied).
- Abklingen zum Dauerkurzschlussstrom.

Die Ströme in der Dämpferwicklung klingen sehr schnell ab (große Wirkwiderstände) → subtransienter Vorgang. Durch veränderte magnetische Verhältnisse in Läuferteilen werden Spannungen induziert, die auf den Ständer zurückwirken.

Mathematischer Ausdruck für den Kurzschlussstrom bei maximaler Gleichstromverlagerung:

ik = √2·[(I''k − I'k)·e^(−t/T''d)·sin(ωt − α) + (I'k − Ik)·e^(−t/T'd)·sin(ωt − α) + Ik·sin(ωt − α) + I''k·e^(−t/Tdc)·sin(α)]

Diese Formel enthält vier Anteile:
1. Subtransienter Anteil (schnelles Abklingen mit Zeitkonstante T''d)
2. Transienter Anteil (mittleres Abklingen mit Zeitkonstante T'd)
3. Dauerkurzschlussstrom Ik (stationärer Anteil)
4. Gleichstromglied (klingt mit Zeitkonstante Tdc ab)

Aus dem Zeitverlauf wird für die Dimensionierung von Generator und Schutzgeräten der Stoßkurzschlussstrom ip (dynamische Beanspruchung) abgeleitet.
