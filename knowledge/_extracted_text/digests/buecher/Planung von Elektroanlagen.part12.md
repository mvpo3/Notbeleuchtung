# Planung von Elektroanlagen — Teil 12
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 481-520.

Dieser Teil behandelt den Abschluss von Kapitel 24 (Schutztechnik: Strom-/Spannungswandler, Staffelplanung, Gesamtbeispiel MS/NS) sowie das vollständige Kapitel 25 (Grundlagen elektrischer Maschinen: physikalische Gesetze, Transformator-Theorie, Berechnungsbeispiele). Schwerpunkte sind Wandlerauslegung mit Formeln und Rechenbeispielen sowie alle Transformator-Kenngrößen inkl. Verluste, Wirtschaftlichkeit und Parallelschaltbedingungen.

## Inhalt

### 24.15 – Strom- und Spannungswandler (Fortsetzung)

- Primär- und Sekundärseite sind galvanisch voneinander getrennt und gegeneinander isoliert.
- Stromwandler betreibt sich im Kurzschluss, Spannungswandler im Leerlauf.
- Messwandler dienen zum Anschluss von Messinstrumenten und Zählern; Schutzwandler werden für den Anschluss von Schutzeinrichtungen verwendet.
- Größe der Schutzwandler wird bestimmt durch: maximalen Kurzschlussstrom + Gesamtbürde (Wandlerinnenbürde + Leitungsbürde + Relaisbürde); zusätzlich ein Überdimensionierungsfaktor für die Gleichstromkomponente des Kurzschlussstromes.
- Genauigkeit Schutzwandler generell 1 % (Klasse 5P).
- Faktor K'SSC des symmetrischen Bemessungskurzschlussstromes so dimensionieren, dass der maximale Kurzschlussstrom ohne Kernsättigung übertragen werden kann (Gleichstromkomponente bleibt dabei unberücksichtigt).
- Typische Spezifikation für Schutzwandler in Verteilungsnetzen: 5P10 / 15 VA oder 5P20 / 10 VA.
- Anforderungen für Schutzstromwandler bei transienten Beanspruchungen: IEC 60044-6.
- Wandlerauslegung für vollständige Sättigungsfreiheit führt zu sehr großen Wandlern — wirtschaftlich oft nicht realisierbar (besonders bei metallgeschotteten Schaltanlagen).
- Numerische Relais tolerieren Sättigung durch integrierte Sättigungsstabilisierungsfunktion.

**Auswahlkriterien Stromwandler:**
- Betriebsspannung in V
- Primärstrom in A
- Sekundärstrom (Standard: 5 A oder 1 A)
- Schutzklasse: 0,1 / 0,5 / 1 / 2 oder 5P10
- Kurzschlussfestigkeit in A
- Überstromfaktor Ith ≤ 100 × In
- Sättigungsfaktor n < 5
- Isolationsspannung in V
- Herstellerdaten

**Berechnungsformeln Stromwandler:**

Effektiver Faktor K'SSC des symmetrischen Kurzschlussstromes:
- K'SSC = KSSC × (Rct + Rb) / (Rct + Rba)
- K'SSC ≥ Ktd × Isccmax / Ipn
- Isccmax = (100 % / ukr%) × IrT

Leitungswiderstand:
- RL = 2 × ρ × l / A
- Rba = RL + RRelais

**Symbolerklärungen:**
- KSSC: Nennüberstromziffer (z. B. bei 5P20 gilt KSSC = 20)
- K'SSC: Betriebsüberstromziffer
- Ktd: transienter Dimensionierungsfaktor
- Issc,max: maximaler Kurzschlussstrom
- Rct: sekundärseitiger DC-Windungswiderstand
- Rb: ohmische Wandlernennbürde
- Rba: angeschlossene ohmsche Bürde (RL + RRelais)
- Tp: Netzzeitkonstante
- l: Leiterlänge in m
- A: Leiterquerschnitt in mm²
- ρ: spezifischer Widerstand in Ω·mm²/m bei 20 °C

**Bürden:**
- Numerische Relais: unter 0,1 VA (bei 1-A-Wandlern)
- Analoge Relais: unter 1 VA
- Mechanische Relais: bis zu 10 VA — bei Kombination mit alten Relais am gleichen Wandlerkreis unbedingt berücksichtigen.

---

### 24.16 – Rechenbeispiel: Auslegung eines Stromwandlers

**Gegebene Motordaten:** PrM = 2 MW, UrM = 6 kV, 50 Hz, IA = 5 × IrM, cos φ = 0,8.
Wandlerdaten: 150/1 A, 10P10, 5 VA, Rct = 1,3 Ω, Leitung 10 m, Querschnitt 2,5 mm².

Normgrundlage: IEC 60044-1 und IEC 60044-6.

Berechnungsgang:
- IrM = 2 MW / (√3 × 6 kV × 0,8) = **240,56 A**
- Anlaufstrom: IA = 5 × IrM = **1202,8 A**
- Transienter Anlaufstrom (Einschaltstrom): IAtrans = 2 × IA = **2405,6 A**
- Einstellwert für den Stromschnellauslöser: I>> = 1,3 × IAtrans = **3127,28 A**
- Einstellwert Zeit: t>> = 50 ms (angenommen)
- Geforderter K'SSC = I>> / Ipn = 3127,28 A / 150 A = **20,84**

Nennbürde Wandler: Rb = Sn / I²sn = 5 VA / (1 A)² = **5 Ω**

Tatsächliche Bürde (Leitung + Gerät):
- RL = 2 × 0,0175 Ω·mm²/m × 10 m / 2,5 mm² = 0,14 Ω
- R'b = RL + RRelais = 0,14 + 0,1 = **0,24 Ω**

Effektiver Faktor:
- K'SSC = KSSC × (Rct + Rb) / (Rct + R'b) = 10 × (1,3 + 5) / (1,3 + 0,24) = **40,9**

Ergebnis: Geforderter K'SSC = 20,84 — erzielter K'SSC = 40,9 → Wandler **korrekt dimensioniert**.

---

### 24.17 – Rechenbeispiel: Wandlerauslegung für Differentialschutz

Aufgabe: Stromwandler auf Primär- und Sekundärseite eines Transformators für Differentialschutz dimensionieren.

Transformatordaten: 40 MVA, 110 kV / 20 kV, ukr = 14 %.

**Bemessungsströme:**
- IrTHV (110-kV-Seite) = 40 MVA / (√3 × 110 kV) = **210 A**
- IrTLV (20-kV-Seite) = 40 MVA / (√3 × 20 kV) = **1155 A**

**Kurzschlussströme:**
- Isccmax (110 kV) = (100 % / 14 %) × 210 A = **1500 A**
- Isccmax (20 kV) = (100 % / 14 %) × 1155 A = **8250 A**

**Betriebsüberstromziffer (110-kV-Seite):**
- K'scc = Ktd × I''kHV / In,CT = 4 × 2625 A / 300 A = **35**

**Betriebsüberstromziffer (20-kV-Seite):**
- K'scc = Ktd × I''kLV / In,CT = 4 × 14,37 kA / 1250 A = **45,98 ≈ 46**

**Leitungsdaten (50 m, 2,5 mm²):**
- RL = 2 × 0,0179 Ω·mm²/m × 50 m / 2,5 mm² = **0,716 Ω**
- Rba = RL + RRelais = 0,716 + 0,05 = **0,766 Ω**

**Überprüfung Wandler 10P10, 5 VA (Rct = 1 Ω):**
- K'ssc = 10 × (1 + 5) / (1 + 0,766) = **34** < 46 → **Wandler ungeeignet**

**Lösung:** Wandlerleistung auf 10P15, 15 VA erhöhen (Rct = 3 Ω):
- K'ssc = 15 × (3 + 15) / (3 + 0,766) = **71,7** > 46 → **Wandler 1250 A/1 A, 10P15, 15 VA geeignet**

---

### 24.18 – Rechenbeispiel: Projektierung eines Mittelspannungsnetzes

Transformator: 400 kVA, 20/0,4 kV; S''kQmax = 550 MVA; S''kQmin = 300 MVA.

**Kurzschlussströme HV-Seite (20 kV):**
- I''k3max = 550 MVA / (√3 × 20 kV) = **15,9 kA**
- I''k3min = 300 MVA / (√3 × 20 kV) = **8,66 kA**
- I''k2min = (√3/2) × 8,66 kA = **7,5 kA**

**Kabelquerschnitt HV-Seite** (Kurzschlussstromfestigkeit Sthr = 143 A/mm², Referenzzeit tkr = 1 s):
- Für Abschaltzeit 0,1 s: q ≥ 15,9 kA / 143 A/mm² × √(1 s / 0,1 s) ≈ 35,16 mm² → **Normquerschnitt 50 mm²**
- Für Abschaltzeit 0,5 s: q ≥ 15,9 kA / 143 A/mm² × √(1 s / 0,5 s) ≈ 78,62 mm² → **Normquerschnitt 95 mm²**

**Bemessungsströme Transformator:**
- IrTHV = 400 kVA / (√3 × 20 kV) = **11,54 A**
- IrTLV = 400 kVA / (√3 × 0,4 kV) = **577 A**

**Kurzschlussströme LV-Seite (ukr = 4 %):**
- Ik3max = (100 % / 4 %) × 577 A = **14,4 kA**
- Ik2 = (√3/2) × 14,4 kA = **12,5 kA**

**Stromwandler UMZ-Schutz** (50/1 A, 5P10, 10 VA, Rct = 0,2 Ω, RRelais = 0,1 Ω, Leitung 10 m / 1,5 mm²):
- Rb = 10 VA / (1 A)² = **10 Ω**
- RL = 2 × 0,0179 × 10 / 1,5 = **0,24 Ω**
- Rba = 0,24 + 0,1 = **0,34 Ω**
- Geforderter K'scc = 1,1 × 15,9 kA / 50 A = **350**
- Erzielter K'ssc = 10 × (10 + 0,2) / (0,34 + 0,2) = **189** < 350 → **Stabilitätskriterium nicht erfüllt**
- Wandlerleistung auf **10P15, 20 VA** erhöhen.

---

### 24.19 – Erstellung eines Staffelplans

Grundregeln für Relaiseinstellungen und Staffelplanerstellung:

**Netzplan erstellen (Einspeisestation):**
1. Leitungslänge und Kabeltyp
2. Primär- und Sekundärimpedanz der Leitung
3. Relaistyp und Zusatzrelais
4. Nummerierung der Relais
5. Stromwandlerübersetzung
6. Betriebsmäßige Trennstellen
7. Bezeichnung der Schutzstationen
8. Zeiten der Schutzrelais

**Staffelmaschen festlegen:**
1. Kleinste Impedanz der Leitung festlegen
2. Trennstellen bleiben unberücksichtigt

**Besonderheiten:**
- Doppelleitungen berücksichtigen
- Vergleichsschutz einbeziehen
- Maximale Abschaltzeiten vom Netzbetreiber beachten
- Sonderabnehmer berücksichtigen

**Staffelplan zeichnen:**
1. Staffelmaschen an der einspeisenden Sammelschiene auftrennen
2. Zwischenstationen einzeichnen
3. Impedanz von Doppelleitungen gestrichelt darstellen
4. Datenliste erstellen

---

### 24.20 – Gesamtbeispiel mit HS- und NS-Netzen

Zusammenfassung der wichtigsten Schutzfunktionen im HS- und NS-Bereich mit Staffelplänen verschiedener Schutzgeräte. Nach Lastfluss- und Kurzschlussberechnung werden die Schutzgeräteströme auf Zeit-Überstrom-Diagrammen dargestellt (Staffelkennlinien für Distanzschutz).

---

### 24.21 – Zusammenfassung Schutztechnik

- Fehler verursachen hohe dynamische und thermische Beanspruchungen sowie Beeinträchtigungen der Energieversorgung.
- Jeder Fehler ist schnellstmöglich abzuschalten; Schutz von Menschen und Tieren vor gefährlichen Stromwirkungen ist Pflicht.
- Anforderungen an Schutzeinrichtungen: **Zuverlässigkeit, Schnelligkeit, Wirtschaftlichkeit, Selektivität**.
- In Mittelspannungsnetzen sind Betriebsmittel hohen thermischen und dynamischen Beanspruchungen ausgesetzt — Planungs- und Projektierungsvorschriften müssen eingehalten werden.

---

### 25.1 – Grundlagen elektrischer Maschinen: Einführung

Elektrische Maschinen (Generatoren, Transformatoren, Motoren) kommen in Kraftwerken, Industrie, Gewerbe, Landwirtschaft, Büros, Haushalten, Bahnen, Kraftfahrzeugen und Schiffen vor. Leistungsspanne: mW bis MW.

Energiebereitstellung als Gleichstrom, Einphasenwechselstrom oder Dreiphasenwechselstrom. Asynchronmotoren sind in der Industrie am häufigsten verbreitet.

Alle elektrischen Maschinen nutzen magnetische Effekte durch Elektronenbewegung. Für rotierende Maschinen: Spannungserzeugung + Drehmomenterzeugung. Für Transformatoren: Nutzung des sich ändernden magnetischen Flusses in Leiterschleifen.

Kapitelinhalte:
1. Physikalische Gesetze der Energieumwandlung
2. Funktion des Transformators
3. Verschiedene Motortypen
4. Anwendungsbereiche elektrischer Maschinen

---

### 25.2 – Physikalische Gesetze elektrischer Maschinen

**1. Induktionsgesetz:**
- Wird eine Leiterschleife mit Geschwindigkeit v in einem Magnetfeld (Flussdichte B) bewegt, ändert sich der umfasste magnetische Fluss Φ → Spannungsinduktion.
- Formel: ui = N × dΦ/dt oder ui = B × l × v
- Allgemein: Φ = B × A × cos(ωt) → ui = B × A × ω × sin(ωt) = Umax × sin(ωt)
- Größere Spannungen durch: mehr Windungen N, größere Flussdichte B, längere wirksame Leiterlänge l, höhere Geschwindigkeit v.

**2. Durchflutungsgesetz:**
- Elektrische Ströme erzeugen magnetische Felder.
- Im Inneren der Spule: homogenes Feld; außen: inhomogenes Feld.
- Das Linienintegral der Feldstärke H entlang einer geschlossenen Linie C entspricht dem gesamten elektrischen Strom N×I (Durchflutung Θ):
  - ∮ H·dl = Θ = N×I = H1×l1 + H2×l2 + ... + Hn×ln

**3. Kraftwirkung:**
- Ladungsbewegung quer zum Leiter → Spannungsinduktion im Leiter → Maschinendrehung.
- Auf stromdurchflossene Leiterschleife im Magnetfeld wirkt Kraft: F = I × (l × B)
- Bei Rotation: M = F × r (Drehmoment)
- Kraft zwischen senkrecht aufeinanderstehenden Feld und Leiter: F = l × I × B
- Kraft zwischen Polschuhen: F = A × B² / (2 × μ₀)
- Kraft zwischen zwei parallelen stromdurchflossenen Leitern im Abstand a: F = I1 × I2 × μ₀ × l / (2 × π × a) — kann an Sammelschienen und Anlagen zu erheblichen Zerstörungen führen.

**4. Drehmoment:**
- M = F × r
- P = M × 2πn

**Symbolerklärungen:**
- B: Flussdichte in T; I: Stromstärke in A; N: Windungszahl; z: Leiteranzahl; l: Leiterlänge in m; r: Radius in m; F: Kraft in Nm; M: Drehmoment in Nm; U0: induzierte Spannung in V; dΦ: Flussänderung in Wb; dt: Zeitänderung in s

Beide Effekte (Induktion + Kraft) sind bei Motor und Generator vorhanden; induzierte Spannung und speisende Spannung sind entgegengerichtet.

---

### 25.3 – Transformator

Transformatoren sind elektrische Energiewandler, die Spannung und Stromstärke ändern. Wirkungsgrad meist über 95 % (Energieumwandlung innerhalb des gleichen Mediums).

**Klassifikation:**
- Kleintransformatoren: bis ca. 1000 V
- Großtransformatoren: über 1000 V
- Weitere Unterteilung nach Bauart: explosionsgeschützt, Verteil-, Gießharztransformatoren usw.

**Drehstromtransformatoren** werden eingesetzt in: mittleren und größeren Betrieben, großen Büro-/Verwaltungsgebäuden, Krankenhäusern, Flughäfen, Bahnbetrieben — als Verteiltransformatoren zur Anpassung von Spannung, Strom, Frequenz und Leistung.

**Energiequelle:** Direkt aus Mittel- oder Niederspannungsnetzen der EVU.

**Häufigste Bauarten:** Öl- und Gießharztransformatoren. Gießharz kann auch dort aufgestellt werden, wo Öltransformatoren aus Sicherheitsgründen nicht erlaubt sind.

**Anwendungen über Spannungswandlung hinaus:**
- Nachrichtentechnik: Übertrager zur Kleinstspannungserzeugung
- Messtechnik: Messwandler für Strom- und Spannungsmessung

**Transformatortypen nach Einsatz:**
1. Maschinentransformatoren in Kraftwerken (Generatorspannung → Hochspannung)
2. Netzkupplungstransformatoren (Energieaustausch zwischen Verbundnetzen)
3. Netztransformatoren (Hochspannung → Mittelspannung)
4. Verteilungstransformatoren (Energieversorgung NS-Verbraucher)

---

#### 25.3.1 – Grundgleichungen von Transformatoren

Aufbau: Eisenkern (magnetische Kopplung) + Wicklungen auf Primär- und Sekundärseite.

**Induzierte Spannung (Eingangsseite):**
- U10 = 4,44 × f × N1 × B̂1 × AFe

**Induzierte Spannung (Ausgangsseite):**
- U20 = 4,44 × f × N2 × B̂1 × AFe

**Idealer Transformator** (keine Verluste, kein Leerlaufstrom, keine Streuung):
- Spannungsverhältnis im Leerlauf: U1/U2 = N1/N2
- Stromverhältnis (umgekehrt proportional): I1/I2 = N2/N1
- Übersetzungsverhältnis nach DIN VDE 0532: ü = U1/U2 = N1/N2
- Als Übertrager: Z1 = U1/I1 ; Z2 = U2/I2

**Spannungsgleichungen (realer Transformator):**
- U1 = R1×I1 + jX'1×I1 + jXh×(I1 + I'2)
- U'2 = R'2×I'2 + jX'2×I'2 + jXh×(I1 + I'2)
- Leerlaufstrom: I0 = I1 − I'2 = Iμ + IFe

**Symbolerklärungen:**
- U1/U2: Eingangs-/Ausgangsspannung in V; N1/N2: Windungszahlen; I1/I2: Ströme in A; ü: Übersetzungsverhältnis; U0: Leerlaufspannung; f: Frequenz in Hz; A: Eisenquerschnitt in m²; B̂: magnetische Flussdichte in Vs; Z1/Z2: Scheinwiderstände in Ω

---

#### 25.3.2 – Verluste im Transformator

**1. Leerlaufverluste (Eisenverluste):**
- Messung im Leerlaufversuch.
- PFe = P0Cu + PWirbel + PHysterese
- Eisenverlustwiderstand: RFe ≈ U1/I1 × cos φ
- Primärer Bemessungsstrom: I1N = S / (√3 × U1N)
- Nach DIN 42500: Leerlaufstrom I0 = 0,018 × IN
- Eisenverluststrom: IFe = P0 / (√3 × U1N)
- Magnetisierungsstrom: Iμ = √(I²0 − I²Fe)

**2. Kurzschlussverluste (Kupferverluste):**
- Messung im Kurzschlussversuch: Ausgangswicklung kurzgeschlossen, Eingangsspannung bis Bemessungsstrom hochgefahren.
- Kupferverluste: PCu = I²1N × R1 + I²2N × R2
- Kurzschlussimpedanz: Z1k = √(R²1k + X²1k)
  - R1k = R1 + R'2
  - X1k = X'1 + X'2
  - tan φk = X1k / R1k
  - Uk = Z1k × I1k

**Relative Kurzschlussspannung uk:**
- uk = (Uk / U1) × 100 %
- uk ist Maß für den Innenwiderstand des Transformators.
- Kleines uk → geringer Innenwiderstand → **spannungssteif** (geringe Spannungsänderung bei Belastung).
- Großes uk → hoher Innenwiderstand → **spannungsweich** (starkes Spannungsabsinken bei Last, aber kleinerer Sekundärfehlerstrom → schont Betriebsmittel).

**Weitere Formeln:**
- Relativer Wirkanteil: uR = R1k × I1k / U1N
- Relativer Blindanteil: ux = X1k × I1k / U1N
- uk = √(u²R + u²x)
- Leistungsfaktor: cos φk = Rk / Xk
- Dauerkurzschlussstrom: Ik = P1N / (uk × √3 × U1)

---

#### 25.3.3 – Belastung von Transformatoren

Spannungsänderung bei Belastung = Differenz zwischen Nennspannung einer Wicklung und der Spannung, die bei bestimmter Last und bestimmtem Leistungsfaktor entsteht.

Spannungsänderung in %:
- uφ = n × u'φ + (1/2) × n × u''φ² / 100
- u'φ = uRr × cos φ + uxr × sin φ
- u''φ = uRr × sin φ − uxr × cos φ
- Ohmscher Spannungsfall: uRr = Pk / Sr × 100
- Streuspannung: uxr = √(u²zr − u²Rr)

**Teillastfaktor:** n = √(p × (p−1) × P0 / Pk)

**n-1-Prinzip (Ausfallsicherheit):**
- Szul ≤ (n−1) × k × ΣSrT / n
- Installierte Transformatorleistung: ΣSrT ≥ n × Smax / ((n−1) × k)
- Transformatorbemessungsleistung: SrT = ΣSrT / n

**Symbolerklärungen:**
- uRr: ohmscher Spannungsfall in %; uxr: Streuspannung in %; n: Teillastfaktor; p: Anzahl parallelgeschalteter Transformatoren; P0: Leerlaufverluste in W; Pk: Kurzschlussverluste in W; Szul: zulässige Leistung für n-1; k: Belastbarkeitsfaktor.

---

#### 25.3.4 – Schaltgruppen von Transformatoren

Schaltung = Verbindung von Wicklungssträngen zu einer Wicklung.
- Großbuchstaben: Oberspannungsseite (HV)
- Kleinbuchstaben: Unterspannungsseite (LV)
- HV und LV können in Stern (Y/y) oder Dreieck (D/d) geschaltet werden.
- Art der Sternpunkterdung ist wichtig für Dimensionierung elektrischer Anlagen.
- Schaltgruppenziffer gibt an: Vielfaches von 30°, um das der Zeiger der LV-Seite dem der HV-Seite (im Gegenuhrzeigersinn) nacheilt.

---

#### 25.3.5 – Parallelschaltung von Transformatoren

**Bedingungen für Parallelschaltung:**
1. Ober- und Unterspannungen sowie Frequenzen müssen gleich sein.
2. Kurzschlussspannungen dürfen höchstens **10 %** voneinander abweichen.
3. Nennleistungsverhältnis kleiner als **3:1**.
4. Schaltgruppe muss gleich sein. (Bei Nichterfüllung: Kennzahlen 5→11 oder 6→0 können um 6 angepasst werden.)

**Lastverteilung bei gleichen uk:**
- SL1 = ΣSrT × SrT1 / ΣSrT (proportional zur Bemessungsleistung)

**Lastverteilung bei ungleichen uk:**
- SL1 = SrT1 × (ukrm / ukr1) × (ΣSGL / ΣSrT)
- Mittlere Kurzschlussspannung: ukrm = ΣSrT / (SrT1/ukr1 + SrT2/ukr2 + ...)

**Symbolerklärungen:**
- SrT1/SrT2: Bemessungsleistungen in kW; ukr1/ukr2: Kurzschlussspannungen in %; SL1/SL2: Lastabgaben in kW; SrT: Summe Bemessungsleistungen; ukrm: mittlere Kurzschlussspannung; SGL: Gesamtlast in kW.

---

#### 25.3.6 – Wirkungsgrad von Transformatoren

Wirkungsgrad bei beliebiger Belastung n:
- η = 100 % − [(P0 + n² × Pk) / (n × SrT × cos φ + P0)] × 100 %

**Maximaler Wirkungsgrad** tritt auf, wenn P0 = n² × Pk gilt, d. h. bei Belastungsfaktor:
- n = √(P0 / Pk)

**Gesamtverluste bei beliebiger Belastung:**
- Pv = P0 + n² × Pk

---

#### 25.3.7 – Wirtschaftlichkeit von Transformatoren

**Jährliche Gesamtkosten:**
- KJ = KA + KU + K(P0/Pk)

**1. Kapitalkosten:**
- KA = A × r/100
- Annuitätenfaktor: r = p × qⁿ / (qⁿ − 1)
- q = 1 + p/100
- Symbole: A: Anschaffungspreis; r: prozentualer Kapitalkostensatz (Zinsen + Abschreibung); p: Zinssatz in %/Jahr; n: Abschreibungsdauer in Jahren; KU: Unterhaltungskosten.

**2. Betriebskosten:**

Leerlaufkosten (Eisenverluste) — fallen während gesamter Betriebszeit an:
- KP0 = (kL + ka × TB) × P0

Kurzschlussverlustkosten (Kupferverluste) über Jahresbelastungskurve:
- KCu = KPk = (kL + ka × δ × TB) × (Smax/SrT) × Pk

Weitere zu berücksichtigende Kosten: Magnetisierungsblindleistung + Hilfsbetriebe.

**Symbolerklärungen:**
- kL: Leistungskosten in €/kW; ka: Arbeitskosten in €/kWh; TB: Einschaltdauer in h/Jahr; m: Belastungsgrad; δ: Verlustfaktor; P0: Leerlaufverluste in kW; Smax: Spitzenwert Jahresbelastungskurve in kVA; SrT: Transformatorbemessungsleistung in kVA.

**3. Kapitalisierte Verlustwerte (für Wirtschaftlichkeitsvergleich):**
- Anfangskapital: Kk = A + kapitalisierte P0 + kapitalisierte Pk
- Kk = A + (kL + ka×TB)×(100/r)×P0 + (kL + ka×δ×TB)×(Smax/SrT)×(100/r)×Pk
- Vereinfacht (mit vorgegebenen fP0, fPk): Kk = A + fP0 × P0 + fPk × Pk

Jahresbenutzungsdauer und Verlustfaktor:
- Tm = Jahresarbeit / Höchstbelastung
- m = Tm / TB

---

#### 25.3.8 – Schutz von Transformatoren

**Tab. 25.1 — HH-Sicherungsnennströme nach DIN VDE 0670 Teil 402** (Zuordnung zu Transformatorbemessungsleistungen, Umgebungstemperatur ≤ +40 °C, max. Kurzschlussdauer 2 s):

| Un | 100 kVA | 315 kVA | 500 kVA | 630 kVA | 800 kVA | 1000 kVA |
|----|---------|---------|---------|---------|---------|----------|
| 10/12 kV | 16 A | 40 A | 63 A | 80 A | 100 A | 125 A |
| 20/24 kV | 10 A | 25 A | 31,5 A | 40 A | 63 A | 63 A |

(ukr nach DIN VDE 0532 / IEC 76-5 gilt für ukr = 4 % und ukr = 6 %)

Transformator nach DIN 42503 mit 25 % verringerten Leerlaufverlusten ist zu bevorzugen.

---

#### 25.3.9 – Auswahl von Transformatoren

- Kenndaten durch Netzanforderungen und Einsatzort bestimmt.
- Ermittelte Wirkleistung mit Leistungsfaktor auf Bemessungsleistung (kVA) umrechnen.
- In **Verteilungsnetzen** wird ukr = 4 % bevorzugt (geringer Spannungsfall).
- In **Industrienetzen** wird ebenfalls ukr = 4 % bevorzugt.
- Leerlaufverluste: konstant, lastunabhängig (Ursache: Ummagnetisierung des Eisens).
- Kurzschlussverluste: Stromwärmeverluste in Wicklungen + Streufeldverluste → quadratisch mit Belastung veränderlich.
- Öl- und Gießharztransformatoren nach Kundenanforderungen in verschiedenen Bereichen.

**Tab. 25.2 — Bemessungsdaten von Transformatoren (Auszug):**

*Öl-Verteilungstransformatoren nach DIN 42500 T1, 50 Hz, 400 V:*

| SrT (kVA) | UrTOS (kV) | ukr (%) | Schaltgruppe | IrT (A) | I''k (kA) | Pk75 (W) | P0 (W) |
|-----------|-----------|---------|--------------|---------|-----------|----------|--------|
| 50 | 20 | 4 | Yzn5 | 73 | 1,8 | 1350 | 190 |
| 100 | 20 | 4 | Yzn5 | 145 | 3,6 | 2150 | 320 |
| 160 | 20 | 4 | Dyn5 | 231 | 5,7 | 3100 | 460 |
| 250 | 20 | 4 | Dyn5 | 361 | 8,9 | 4200 | 650 |
| 400 | 20 | 4 | Dyn5 | 578 | 14,2 | 6000 | 930 |
| 630 | 20 | 4 | Dyn5 | 910 | 22,1 | 8400 | 1300 |
| 630 | 20 | 6 | Dyn5 | 910 | 14,8 | 8700 | 1200 |
| 1000 | 20 | 6 | Dyn5 | 1444 | 23,2 | 13000 | 1700 |
| 1600 | 20 | 6 | Dyn5 | 2310 | 36,4 | 20000 | 2600 |
| 2500 | 20 | 6 | Dyn5 | 3609 | 55,3 | 29000 | 3500 |

*GEAFOL-Gießharztransformatoren nach DIN 42523, 50 Hz, 400 V:*

| SrT (kVA) | UrTOS (kV) | ukr (%) | Schaltgruppe | IrT (A) | I''k (kA) | Pk75 (W) | P0 (W) |
|-----------|-----------|---------|--------------|---------|-----------|----------|--------|
| 100 | 10 | 4 | Dyn5 | 144 | 3,6 | 1600 | 440 |
| 100 | 20 | 6 | Dyn5 | 144 | 2,4 | 1800 | 330 |
| 160 | 10 | 4 | Dyn5 | 230 | 5,75 | 2300 | 610 |
| 160 | 20 | 6 | Dyn5 | 230 | 3,8 | 2500 | 480 |
| 250 | 10 | 4 | Dyn5 | 360 | 9 | 3000 | 820 |
| 250 | 20 | 6 | Dyn5 | 360 | 6 | 3100 | 650 |
| 400 | 10 | 4 | Dyn5 | 589 | 14,7 | 4300 | 1150 |
| 400 | 20 | 6 | Dyn5 | 589 | 9,8 | 4100 | 1200 |
| 630 | 10 | 4 | Dyn5 | 910 | 22,7 | 6400 | 1500 |
| 630 | 20 | 6 | Dyn5 | 910 | 15 | 6400 | 1250 |
| 1000 | 20 | 6 | Dyn5 | 1444 | 24 | 8900 | 2200 |
| 1600 | 20 | 6 | Dyn5 | 2312 | 38,5 | 11000 | 2400 |
| 2500 | 20 | 6 | Dyn5 | 3600 | 60 | 17600 | 3600 |

**Tab. 25.3 — Leistungsschild Beispiel (Typ: DOTUL 1600 H/20, Baujahr 2012):**
- Norm: DIN 42500, DIN VDE 0530
- Bemessungsleistung: 1600 kVA
- Art: Öl; Frequenz: 50 Hz
- Schaltgruppe: Dyn5
- Strangspannungen HV: 20.800 V / 20.000 V / 19.200 V (3 Anzapfungen)
- Nennspannung LV: 400 V; Reihe: 20 N/0,6
- Kühlungsart: ONAN
- Bemessungsströme: 2309 A / 46,2 A
- Gewicht: 3,64 t; Isolierung Mineralöl: 0,87 t
- Kurzschlussspannung: 6 %
- Dauerkurzschlussstrom: 0,770 kA; max. KS-Dauer: 4 s
- Betrieb: DB; Schutzgrad: IP 54
- Leerlaufverluste: 1200 W; Kurzschlussverluste: 14.000 W

---

### 25.4 – Rechenbeispiele zu Transformatoren

#### 25.4.1 – Beispiel: Übertragung elektrischer Energie

Aufgabe: 2,3 MW über 5 km übertragen, Spannungsebenen 400 V und 220 kV, cos φ = 0,8, Spannungsfall 10 %.

**Bei 400 V (Niederspannung):**
- I1 = 2,3 MW / (√3 × 400 V × 0,8) = **4149,7 A**
- Leiterwiderstand: RL1 = 40 V / 4149,7 A = **9,64 mΩ**
- Leiterquerschnitt: AL1 = 5000 m / (56 m/Ω·mm² × 9,64 mΩ) = **9262 mm²**

**Bei 220 kV (Hochspannung):**
- I2 = 2,3 MW / (√3 × 220 kV × 0,8) = **7,55 A**
- Leiterwiderstand: RL2 = 22.000 V / 7,55 A = **2933,33 Ω**
- Leiterquerschnitt: AL2 = 5000 m / (56 × 2933,33) = **0,0304 mm²**

Fazit: Wirtschaftliche Energieübertragung über große Distanzen erfordert hohe Spannungen — Transformatoren übernehmen diese Aufgabe.

---

#### 25.4.2 – Beispiel: Spannungsänderung von Transformatoren

Gegebene Daten: SrT = 400 kVA, 6 kV/400 V, ukr = 6 %, Kurzschlussverluste = 7800 W.
Gesucht: Sekundäre Klemmenspannung bei Nennlast, cos φ = 0,8 induktiv.

- uRr = 7800 W / 400.000 VA = **1,95 %**
- uxr = √(6² − 1,95²) = **5,7 %**
- u'φ = uRr × cos φ + uxr × sin φ = 1,95×0,8 + 5,7×0,6 = **4,98 %**
- u''φ = uRr × sin φ − uxr × cos φ = 1,95×0,6 − 5,7×0,8 = **−3,39 %** (Vorzeichen beachten)
- ug = u'φ + 0,5 × u''φ²/100 = **5,04 %** (Kapp'sches Dreieck)
- Sekundärspannung: U2 = U20 − ug×U20/100 = **380 V**

---

#### 25.4.3 – Beispiel: Lastverteilung bei Parallelschaltung

Drei parallelgeschaltete Transformatoren:
- SrT1 = 400 kVA, ukr1 = 4 %
- SrT2 = 630 kVA, ukr2 = 4 %
- SrT3 = 800 kVA, ukr3 = 6 %

Mittlere Kurzschlussspannung:
- ukrm = 1830 kVA / (400/4 + 630/4 + 800/6) ≈ **4,68 %**

Aufgenommene Leistungen:
- SrT1 = 400 × 4,68 % / 4 % = **468 kVA** (Überlast!)
- SrT2 = 630 × 4,68 % / 4 % = **737,1 kVA** (Überlast!)
- SrT3 = 800 × 4,68 % / 6 % = **624 kVA**

Transformator 1 und 2 sind überlastet → Aufstellung eines weiteren Transformators (250 kVA) empfohlen.

---

#### 25.4.4 – Beispiel: Berechnung von Verlustleistungen

Netz: 150 MW; Spannungsebenen 400 V und 20 kV.

- I (bei 400 V) = 150 MW / (√3 × 400 V) = **216,5 A**
- I (bei 20 kV) = 150 MW / (√3 × 20 kV) = **4,33 A**

Verlustleistungen bei 20 kV (R = 0,039 Ω, X = 0,029 Ω):
- PV = 3 × (4,33)² × 0,039 = **2,19 MW** (ohmsch)
- QV = 3 × (4,33)² × 0,029 = **1,63 MW** (induktiv)

Verlustleistungen bei 400 V (R = 0,3825 Ω, X = 0,02 Ω):
- PV = 3 × (216,5)² × 0,3825 = **17,92 kW** (ohmsch)
- QV = 3 × (216,5)² × 0,02 = **937,4 W** (induktiv)

---

#### 25.4.5 – Beispiel: Wirtschaftlichkeit — Teillastfaktor

Gegebene Daten: 20/0,4 kV, SrT = 630 kVA, P0 = 800 W, PkrT = 6750 W, ukr = 6 %, Dyn5.

Teillastfaktor für wirtschaftliches Zuschalten:
- Formel: a = √(n × (n−1) × P0 / PkrT)

**Mit n = 2 Transformatoren:**
- a = √(2 × 1 × 800 / 6750) = **0,486**
- Wirtschaftliche Zuschaltschwelle: SG = 0,486 × 630 kVA = **306,18 kVA**

**Mit n = 3 Transformatoren:**
- a = √(3 × 2 × 800 / 6750) = **0,843**
- Wirtschaftliche Zuschaltschwelle: SG = 0,843 × 630 kVA = **531,09 kVA**

→ Zweiter Transformator wirtschaftlich bei 306,18 kVA zuschalten; dritter bei 531,09 kVA.

---

#### 25.4.6 – Beispiel: Jahreswirkungsgrad

Daten: SrT = 630 kVA, ukr = 4 %, P0 = 860 W, PkrT = 6500 W.
Einschaltdauer: tB = 8760 h/Jahr (Dauereinschaltung), Belastungszeit: tE = 1800 h, cos φ = 0,85.

- Wab = 630 kVA × 0,85 × 8760 h = **4.690.980 kWh**
- WFe = 860 W × 8760 h = **7533,6 kWh**
- WCu = 6500 W × 1800 h = **11.700 kWh**
- Jahreswirkungsgrad: η = 4.690.980 / (4.690.980 + 7533,6 + 11.700) = **0,995 (99,5 %)**

---

#### 25.4.7 – Beispiel: Wirkungsgrad bei Teillast

Daten: SrT = 630 kVA, ukr = 6 %, P0 = 0,8 kW, PkrT = 6,75 kW, cos φ = 0,8, Belastungsfaktor a = 0,5.

- η = 100 % − [(0,8 kW + 0,5² × 6,75 kW) / (0,5 × 630 kVA × 0,8 + 0,8 kW)] × 100 %
- η = **99,99 %**

---

#### 25.4.8 – Beispiel: Schaltgruppen und Windungszahlen

Ausgang: Dy-Transformator, HV-Strangspannung = 10 kV, N1 = 1905 Windungen; LV-Strangspannung = 231 V, N2 = 44 Windungen.

Windungszahlen bei anderen Schaltungen:

**Fall a) Yy:**
- HV: UStr = 10 kV / √3 → N1 = 1905 / √3 = **1100 Windungen**
- LV: UStr = 231 V → N2 = **44 Windungen**

**Fall b) Yd:**
- HV: UStr → N1 = **1100 Windungen**
- LV: UStr = 231 V × √3 → N2 = 44 × √3 = **76 Windungen**

**Fall c) Yz:**
- HV: UStr → N1 = **1100 Windungen**
- LV: UStr = (2/√3) × 231 V → N2 = (2/√3) × 44 = **51 Windungen**

**Fall d) Dz:**
- HV: N1 = **1905 Windungen**
- LV: UStr = (2/3) × 231 V → N2 = (2/3) × 44 = **30 Windungen**

---

#### 25.4.9 – Beispiel: Berechnung der Transformatorgrößen

Gegebene Daten: 630 kVA, 20 kV/0,4 kV, ukr = 4 %, Dyn5, cos φk = 0,6.

**Fall a) Strangspannungen:**
- HV (Dreieck): UStr1 = UL1 = **20 kV**
- LV (Stern): UStr2 = 400 V / √3 = **231 V**

**Fall b) Windungsverhältnis:**
- N1/N2 = UStr1 / UStr2 = 20.000 V / 231 V = **86,58**
