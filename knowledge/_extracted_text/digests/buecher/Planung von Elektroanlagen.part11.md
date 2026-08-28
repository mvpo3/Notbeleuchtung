# Planung von Elektroanlagen — Teil 11
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 441-480.

Dieser Teil behandelt Selektivität, Back-up-Schutz, sicherungslose Schaltanlagen sowie Schutztechnik in elektrischen Anlagen (Mittelspannung). Abgedeckt werden UMZ/AMZ-Schutz, Differentialschutz, Distanzschutz, Erdschlussschutz, Transformator-, Sammelschienen-, Motor- und Generatorschutz mit vollständigen Berechnungsbeispielen.

## Inhalt

### 22.7 Back-up-Schutz

- Jede Überstromschutzeinrichtung (ÜSE) muss den Anfangs-Kurzschlusswechselstrom an ihrer Einbaustelle beherrschen können.
- Ist das nicht möglich, wird eine vorgeordnete ÜSE eingesetzt, die sowohl den Abzweig als auch den nachgeschalteten Schutzschalter absichert.
- Das Bemessungsausschaltvermögen der nachgeordneten ÜSE darf dabei kleiner sein als der maximal mögliche Kurzschlussstrom.
- Voraussetzung: Die vorgeordnete ÜSE (z. B. MCB, MCCB oder Sicherung) begrenzt den Kurzschlussstrom strombegrenzend.
- Lösen beide ÜSEs gleichzeitig aus und reduziert die vorgeordnete ÜSE (C1) die Kurzschlussbelastung der nachgeordneten (C22), liegt Back-up-Schutz vor.
- Wo Selektivität nicht zwingend gefordert ist, erlaubt Back-up-Schutz den Einsatz kostengünstigerer Gerätekombinationen mit niedrigerer Kurzschlussfestigkeit.
- Bewertungsgrundlage: DIN VDE 0660 Teil 101 / IEC 947-2.

---

### 23 Sicherungslose Schaltanlagen

Elektrische Anlagen sollen optimalen Schutz bieten, geringe Anschaffungs- und Betriebskosten verursachen sowie wartungsfrei und einfach projektierbar sein. Sie können mit Sicherungen oder mit Leistungsschaltern ausgeführt werden.

#### 23.1 Auswahl der Sicherungen

- NH-Sicherungen mit Charakteristik gL (Bemessungsstrom > 25 A) nach DIN VDE 0636 Teil 21:
  - Auslösestrom: I₂ = 1,6 × In
- Sicherung zum Schutz von Kabeln:
  - I₂ = 1,45 × (1,6 / 1,45) × Iz → vereinfacht: In = 0,90625 × Iz
  - Anschließend ist die nächst kleinere Sicherungsstufe auszuwählen.

#### 23.2 Auswahl der Leistungsschalter

- Nach DIN VDE 0100 Teil 430 darf der Bemessungsstrom der Schutzeinrichtung In gleich der Strombelastbarkeit Iz sein, wenn ein Leistungsschalter nach DIN VDE 0660 Teil 101 verwendet wird.
- Maßgebend ist der Einstellwert des Schalters; es gilt: I₂ = 1,2 × Iz
- Sicherungen haben damit einen rund 40 % höheren Ansprechstrom als Leistungsschalter — sie sind daher für den reinen Überlastschutz nicht geeignet.
- Für Drehstrommotoren mit Y-Anlauf: Einstellstrom des Überlastrelais mit Faktor 0,58 (= 1/√3) gegenüber dem Bemessungsstrom reduzieren.

#### 23.3 Kennlinienvergleich Sicherung vs. Leistungsschalter

Vergleich Abschaltzeiten bei 25-A-Sicherung vs. 16–25-A-Leistungsschalter (NZM):

| Strom | NH-gL Abschaltzeit | NZM Abschaltzeit |
|-------|-------------------|-----------------|
| 500 A | 8 ms              | 8 ms            |
| 150 A | 500 ms            | 8 ms            |

Beispielrechnung Kurzschlussschutz:
- Ausschaltzeit: t_aus = k² × S² / I² = 0,002 s
- Da < 0,1 s: Prüfung nach Stromwärmeimpuls erforderlich
- I² × t_aus = 8,5 × 10⁴ A²s < k² × S² = 1,3 × 10⁶ A²s → Schutz bei Kurzschluss ausreichend

#### 23.4 Vergleich Bauweise mit und ohne Sicherung

Drei Bewertungsbereiche:

**23.4.1 Projektierung**
- Bei Sicherungen: Kurzschlussberechnung an der Einbaustelle entfällt.
- Bei Leistungsschaltern: Kurzschlussberechnung erforderlich, da Bemessungsausschaltvermögen begrenzt ist und mindestens dem Kurzschlussstrom an der Einbaustelle entsprechen muss.
- Sicherungen benötigen zusätzlichen Platz sowie Zubehör (Unterteile, Griffzangen, Ersatzsicherungen).
- Sicherungen bilden eine sichere Trennstelle; bei Leistungsschaltern sind hierfür zusätzliche Maßnahmen nötig.

**23.4.2 Schutzfunktion**
- Leistungsschalter: übernehmen Überlast- und Kurzschlussschutz.
- Sicherungen: übernehmen stets den Kurzschlussschutz.
- Übersteigt der Kurzschlussstrom das Bemessungsausschaltvermögen des Leistungsschalters, wird eine Sicherung vorgeschaltet (Back-up-Funktion).
- Sicherungen können Kurzschlussströme bis zu 100 kA abschalten.

**23.4.3 Bedienung und Wartung**
- Sicherungen: nach Kurzschlussauslösung keine unmittelbare Wiedereinschaltbarkeit.
- Leistungsschalter: nach Kurzschlussauslösung nach DIN EN 60947-1 überprüfbar, instandsetzbar und wiederverwendbar.

**23.4.4 Kostenvergleich**
Zu berücksichtigende Kostenpositionen:
- Anteil Verteilerschrank
- Klemmenkosten
- Installierte Kabelkosten (inkl. doppeltem Kabelanschluss)
- Kosten der Leistungsschalter, Sicherungen oder Schaltersicherungseinheiten

#### 23.5 Beispiel: Einstellung der Kennlinien

Gegeben: 200-A-Leistungsschalter, Betriebsstrom 170 A, einpoliger Kurzschlussstrom am Leitungsende 1700 A.

Einstellfaktoren:
- Überlastrelais: f_L = 170 A / 200 A = 0,85
- Kurzschlussrelais: f_I = 1800 A / 200 A = 8,75 (Rechnungswert 1,05 × Kurzschlussstrom)
- Erdungsschutz G: f_G = 120 A / 200 A = 0,65

---

### 24 Schutztechnik in elektrischen Anlagen

Fehler in elektrischen Netzen erzeugen hohe thermische und dynamische Beanspruchungen. Schutzanforderungen: Zuverlässigkeit, Schnelligkeit, Wirtschaftlichkeit, Selektivität. Kurzschlussberechnung nach DIN VDE 0102 / IEC 60909.

#### 24.1 Umfang der Selektivität

Fehlerarten nach Netztyp:

**Kompensierte Netze:**
- Einpoliger Erdschluss
- Doppelerdschluss
- Kurzschlüsse mit oder ohne Erdberührung

**Netze mit Sternpunkterdung über niederohmige Widerstände:**
- Einpoliger Kurzschluss
- Zwei- und dreipoliger Fehler mit/ohne Erdberührung

Für alle Fehlerarten und Fehlerorte: Haupt- und Reserveschutz erforderlich.

#### 24.2 Auslegung des Netzschutzes

Auslegungsbedingungen:

- **Anregebedingung:** f_b × I_max ≤ I_an ≤ I″_kmin / f_a
  - f_b = Faktor Betriebsbedingungen (1,7 für Leitungen, 2,0 für Transformatoren)
  - f_a = Ansprechsicherheitsfaktor (1,25 bis 2,0)
  - I″_kmin = minimaler einpoliger Kurzschlussstrom
- **Ausschaltzeitbedingung:** t_ag ≤ t_ag,zul (Bemessungskurzzeitstrom in MS-Schaltanlagen: 1 s, Gesamtausschaltzeit t_ag ≤ 1,0 s)
- **Belastbarkeitsbedingung:** I_max ≤ I_zul
- **Spannungsfallbedingung:** u_max ≤ u_zul
- **Kurzschlussstrombedingungen:**
  - I_a,max ≤ I_an (= Isc, Bemessungskurzschlussausschaltstrom)
  - I_s,max ≤ I_en (= Ima, Bemessungskurzschlusseinschaltstrom)
  - I_th,max ≤ I_th,zul (thermisch wirksamer Kurzschlussstrom)

**Schutzzweck:**
1. Minimierung von Stromunterbrechungen
2. Minimierung von Anlagenschäden
3. Personenschutz

**Anforderungen an Schutzgeräte:**
- Verlässlichkeit, Selektivität, Geschwindigkeit, Wirtschaftlichkeit, Einfachheit

**Gerätekomponenten:** Relais, Schutzeinrichtungen, Mess- und Schutztransformatoren

**Schutzrelais-Gruppen:** unverzögerte Relais; Zeitrelais

**Überwachungsparameter:** Spannung (Über-/Unterspannung), Strom (Überstrom/offener Stromkreis), Frequenz (Über-/Unterfrequenz)

#### 24.3 Leitungsschutz

##### 24.3.1 UMZ-Schutz (Unabhängiger Überstromzeitschutz)

- Einsatz in strahlenförmig aufgebauten Versorgungs- und Industrienetzen.
- Relais werden in den Stromkreis (Primärrelais) oder über Stromwandler (Sekundärrelais) angeschlossen.
- Beim Ansprechen startet das Zeitrelais; nach Ablauf gibt es das AUS-Kommando.
- Zeitstaffelung: Kommandozeiten steigen zur Einspeisestelle hin an.
- Digitale Schutzgeräte: phasengemeinsame Messung; einsetzbar als UMZ oder AMZ.
- Stufen des UMZ:
  - Überstromstufe (I >): mit parametrierbarer Auslösezeit
  - Hochstromstufe (I >>): mit parametrierbarer Auslösezeit
  - Schnellauslösestufe (I >>>): arbeitet mit Augenblickswerten, löst unverzüglich aus
- Auslösebedingung: I_bmax ≤ I_an ≤ I_k1min
- Rückfallverhältnis: f_R = I_r / I_an ≤ 1
- Auslösezeit UMZ: t = C × t_p (C = einstellbarer Faktor 1, 2 oder 4)
- Nachteil UMZ: Größter Kurzschlussstrom tritt an der Quelle mit größter Zeitstaffelung auf.

##### 24.3.2 Beispiele zu UMZ

- Staffelung beginnt mit kleinster Zeitstufe und steigt zur Quelle.

##### 24.3.3 AMZ-Schutz (Abhängiger Überstromzeitschutz / Inverse-time)

- Kennlinie: fallend — höherer Strom → kürzere Auslösezeit.
- Auslösezeit abhängig von Stromhöhe; Kennlinie enthält Wertepaar (z. B. 1,3 × IN für 1 s Auslösezeit).
- Normen für Kennlinien: British Standard (Normal inverse, Very inverse, Extremely inverse); IEC 255-4 / BS 142.
- Vorteil: bei steigendem Strom kürzere Zeiten — günstig für selektive Staffelung.
- Voraussetzung selektive Staffelung: definierte Einspeisung (Problematik bei Doppelsammelschienenanlagen).
- In Deutschland wenig verbreitet.
- Kennlinienverschiebung durch Änderung von T_p und I_p möglich.

Auslösezeit Normal Inverse Relais:
- t = k × 0,14 / [(I / I_B)^0,02 − 1] (s)
  - k = Kennlinienfaktor
  - I = Fehlerstrom (A)
  - I_B = Einstellwert des Stroms (A)
  - C = einstellbarer Faktor (1, 2 oder 4)

##### 24.3.4 Beispiele zu AMZ

Netz mit Einspeisung (S″_kQ = 4,4 MVA, U_nQ = 20 kV) und Transformator T1 (40 MVA, u_kr = 10 %, u_Rr = 2 %) sowie drei Leitungen L1/L2/L3 und Transformator T2 (630 kVA, u_kr = 4 %, u_Rr = 1 %, 0,4 kV).

**Impedanzberechnung Einspeisung:**
- Z_Q = c × U²_nQ / S″_kQ = 1,1 × (20 kV)² / 4,4 MVA = 100 mΩ → Z_Qt = 0,352 Ω
- X_Qt = 0,995 × 0,352 = 0,35 Ω; R_Qt = 0,1 × 0,35 = 0,035 Ω

**Impedanzberechnung T1:**
- Z_T = (u_kr / 100) × U²_rT / S_rT = (10 % / 100) × (20 kV)² / 40 MVA = 1 Ω
- R_T = (2 % / 100) × (20 kV)² / 40 MVA = 0,2 Ω
- X_T = √(Z²_T − R²_T) = √(1² − 0,2²) = 0,98 Ω

**Leitungsimpedanzen:**
- L1: r₀ = 0,1 Ω/km × 6 km → R_L1 = 0,6 Ω; x₀ = 0,32 Ω/km × 6 km → X_L1 = 1,92 Ω
- L2: R_L2 = 0,15 × 4 = 0,6 Ω; X_L2 = 0,32 × 4 = 1,28 Ω
- L3: R_L3 = 0,2 × 5 = 1,0 Ω; X_L3 = 0,32 × 5 = 1,6 Ω

**Impedanzberechnung T2 (20 kV-Seite):**
- Z_T = (4 % / 100) × (0,4 kV)² / 630 kVA = 25,4 mΩ
- R_T = (1 % / 100) × (0,4 kV)² / 630 kVA = 6,35 mΩ
- X_T = √(25,4² − 6,35²) = 26,18 mΩ (auf 20 kV umgerechnet)

**Dreipolige Kurzschlussströme (I″_k3):**

| Ort | Z_k (Ω) | I″_k3 |
|-----|---------|-------|
| Anfang L1 | 1,09 | 11,65 kA |
| Ende L1 | 3,10 | 4,1 kA |
| Ende L2 | 4,5 | 2,82 kA |
| Ende L3 | 6,34 | 2,0 kA |
| Primär T2 | 6,34 | 0,4 kA |

**Zweipolige Kurzschlussströme (I″_k2min):**

| Ort | I″_k2min |
|-----|---------|
| Anfang L1 | 9,17 kA |
| Ende L1 | 3,23 kA |
| Ende L2 | 2,22 kA |
| Ende L3 | 1,58 kA |
| Primär T2 | 0,3 kA |

**Einstellung UMZ-Relais:**
- I_rT2 = S_rT2 / (√3 × U_n) = 630 kVA / (√3 × 20 kV) = 18,2 A
- I_an > = I″_k2min_Tr2 / 1,5 = 200 A → Sekundärwert bei K_n = 40 A/1 A: 5 A
- I_e > ≥ 2 × 18,2 A / (40/1) = 0,91 A → I_e > = 1 A; t_UMZ = 0,5 s
- I_an >> = 1,2 × I″_k3max_Tr2 = 480 A → I_e >> = 12 A; t = 0,1 s
- I_an >> ≥ I″_k2min_L3 / 1,5 = 1053 A → I_e >> = 26 A (Kontrolle)
- Endergebnis UMZ: I_e > = 1 A, t = 0,5 s; I_e >> = 12 A, t = 0,1 s

**AMZ-Relaiseinstellungen (Extremely inverse, k = 0,3 s):**

| Relais | Fehlerort | I″_k3max / (K_n × I_e) | Auslösezeit t |
|--------|-----------|----------------------|--------------|
| AMZ4 | Ende L3 | 2000 A / (250×1,2) = 6,67 | ≤ 0,4 s |
| AMZ4 | Anfang L3 | 2820 A / (250×1,2) = 9,4 | ≤ 0,22 s |
| AMZ3 | Ende L2 | 2820 A / (400×1,2) = 5,87 | ≤ 0,5 s |
| AMZ3 | Anfang L2 | 4100 A / (250×1,2) = 8,54 | ≤ 0,27 s |
| AMZ2 | Ende L1 | 4100 A / (750×1,2) = 4,55 | ≤ 0,9 s |
| AMZ2 | Anfang L1 | 11650 A / (750×1,2) = 12,84 | ≤ 0,12 s |
| AMZ1 | Anfang L1 | 11650 A / (1200×1,2) = 8,1 | k=0,5 → ≤ 0,48 s |

---

#### 24.4 Thermischer Überlastschutz

- Auslösezeit bestimmt durch eingestellte Wärmezeitkonstante τ des Schutzobjekts und Auslösegrenzwert.
- Auslösezeit beim Überlastschutz (Grundformel):
  - t = 35 / [(I / I_p)² − 1] × t_p
- Auslösezeit mit vollkommenem Gedächtnis nach IEC 255-8:
  - t = τ × ln[(I/I_p)² − (I_vor/I_p)²] / [(I/I_p)² − k]
  - τ = 3,55 × t_p; t_p = Zeitmultiplikator; I_vor = Vorlaststrom; I = Überlaststrom; I_p = Einstellstrom

---

#### 24.5 Differentialschutz

- Prinzip: Überwachung des Stroms am Leitungsanfang und -ende; Abweichung → Auslösung.
- Abschaltung streng selektiv in Schnellzeit (< 0,1 s).
- Kein Zeitstaffelplan erforderlich.
- Zwischen den Wandlern wird eine Kommunikationsleitung verlegt.
- Reserveschutz zusätzlich erforderlich.
- Beim Zuschalten eines Transformators: 100-Hz-Rush-Ströme möglich.
- Zwischen HV und LV: Anpassungen für Schaltgruppen, Transformatorübersetzung und Wandlerübersetzung notwendig.

#### 24.6 Beispiel zum Differentialschutz

Transformatordaten: 40 MVA, Yd5, 110 kV / 20 kV, u_k = 10 %
Wandlerdaten: 200 A / 1 A (HV), 1200 A / 5 A (LV)

Berechnungen:
- I_HV = 40 MVA / (√3 × 110 kV × 1,1) = 191 A → Mittelwert mit Stufenschalterbereich: 212 A
- I_LV = 40 MVA / (√3 × 20 kV) = 1155 A
- Sekundärstrom HV-Wandler: 212 A / (200/1) = 1,06 A
- Sekundärstrom LV-Wandler: 1155 A / (1200/5) = 4,81 A
- Korrektur wegen Dreieckswicklung: 4,81 × √3 = 2,78 A (Dreieck → Stern)
- Wandlerübersetzungsverhältnis Zwischenstromwandler: 2,78 A / 1,06 A = 2,62

---

#### 24.7 Distanzschutz

- Einsatz in mehrseitig gespeisten und vermaschten Netzen ohne Hilfsverbindung.
- Fehlerstelle wird über Impedanzmessung (aus Kurzschlussstrom und Spannung) und Auslösebereich erfasst.
- Nur Distanzschutz erfüllt gleichzeitig Selektivität und Schnelligkeit.
- Stufenkennlinien der einzelnen Relais dürfen sich nirgends schneiden.
- Distanzeinstellung auf 85–95 % der Streckenlänge begrenzt (Kennlinienüberschneidung).
- Erforderliche Daten für Staffelplan: Leitungslänge, Leitungstyp, Leitungsimpedanz, Wandlerdaten, Relaistyp, Netzkonfiguration.

**Einstellregeln:**
- Sofortige Auslösung (Schnellstufe): Z < 0,85 × Z_L
- Auslösung mit Staffelzeitverzögerung (t_v = 0,3 bis 0,5 s): Z > 0,85 × Z_L

**Stufeneinstellungen (praxisbewährt bei geringen Impedanzabständen):**
- Stufe 1: Z₁ = 0,85 × Z_AB
- Stufe 2: Z₂ = 0,85 × Z_AB + 0,72 × Z_BC
- Stufe 3: Z₃ = 0,85 × Z_AB + 0,72 × Z_BC + 0,61 × Z_CD
- Stufe 4: Z₄ = 0,85 × Z_AB + 0,72 × Z_BC + 0,61 × Z_CD + 0,52 × Z_CD

#### 24.8 Messverfahren der Impedanzen

- Strom und Spannung werden zwischen allen Außenleitern gemessen, daraus Impedanz gebildet.
- Liegt gemessene Fehlerimpedanz innerhalb des Auslösekreises → AUS-Kommando mit eingestellter Zeit.
- Distanzschutzgerät stellt für weitere Leitungsabschnitte einen Reserveschutz.
- Leitungsimpedanz: Z_L = (U_L1 − U_L2) / (I_L1 − I_L2) = Z′₁ × l_L = R′₀ × l_L + j × X′₀ × l_L
- Beim einpoligen Erdschluss (L1-Erde): Erdkompensationsfaktor k_E = (Z′_E / Z′₁) = (Z′₀ − Z′₁) / (3 × Z′₁)
- Lichtbogenwiderstand (mit Sicherheitsfaktor s = 2 bis 4): R_Lb = 1800 × l_Lb / I_kmin × s

#### 24.9 Beispiele zum Distanzschutz

Netz mit Einspeisung (S″_kQ = 200 MVA, U_n = 20 kV) und drei Leitungen (6 km, 12 km, 24 km, Z′_L = 0,42 Ω/km).

**Stufenimpedanzen für drei Relais (Relais A, B, C) — Tabelle:**

| Relais | Stufe | wirksame Leitungslänge | Z_Primär | Z_Sekundär |
|--------|-------|------------------------|----------|------------|
| A | 1 | 0,9 × 6 km = 5,4 km | 2,268 Ω | 0,9 A |
| A | 2 | 0,8 × (6 + 0,9 × 12) km = 13,44 km | 6,64 Ω | 2,25 A |
| A | 3 | 0,8 × [6 + 0,8 × (0,9 × 24)] km = 26,3 km | 11 Ω | 4,24 A |
| B | 1 | 0,9 × 12 km = 10,8 km | 4,54 Ω | 1,82 A |
| B | 2 | 0,8 × (12 + 0,9 × 24) km = 26,88 km | 11,28 Ω | 4,5 A |
| C | 1 | 0,9 × 24 km = 21,6 km | 9 Ω | 3,6 A |

**Kurzschlussstrom an Sammelschiene:**
- I_kmax = S″_kQ / (√3 × U_n) = 200 MVA / (√3 × 20 kV) = 5,78 kA

**Impedanz an Fehlerstelle (0,85 × 3 km × Z′_L):**
- Z_L = 0,85 × 3 × (0,196 + j0,116) Ω = (0,5 + j0,3) Ω

**Netzimpedanz:**
- X_N = c × U_N / (√3 × I_kmax,n) = 2,2 Ω
- R_N = X_N / (ω × T_N) = 2,2 / (314 × 0,1) = 0,07 Ω
- Z_N = (0,07 + j2,2) Ω = 2,201 Ω ∠88°

**Kurzschlussstrom Fehlerstelle:**
- I_kmax = 1,1 × 20 kV / (√3 × |Z_G|) = 5 kA

**Wandlerauswahl:**
- Spannungswandler: K_NU = 20000 V / 100 V = 200
- Stromwandler: K_NI = 400 A / 5 A = 80
- Impedanzübersetzung: K_NZ = K_NU / K_NI = Z₁ / Z₂ → Sekundärimpedanz = (K_NU/K_NI) × Z_Primär × (100/20000) = 0,4 × Z_Primär

**Wandlerauslegung für Schutzaufgabe:**
- Netzzeitkonstante: 14 ms
- Messzeit: 35 ms
- Überdimensionierungsfaktor: 5,04
- Erforderlicher Betriebsüberstromfaktor: K′_SSC = 5,04 × 5000 A / 300 A = 84
- Leiterquerschnitt 2,5 mm²: R_L = 2 × 5 m / (56 m/mm² × 2,5 mm²) = 0,07 Ω
- Betriebsbürde: R_B = R_R + R_L = 0,1 + 0,07 = 0,17 Ω
- Bemessungsbürde: R_bn = 10 VA / 1 A² = 10 Ω
- Genauigkeitsgrenzfaktor: K′_SSC = K_SSC × (R_ct + R_bn) / (R_ct + R_B) = 10 × (1 + 10) / (1 + 0,17) = 94
- Ausgewählter Wandler: K′_SSC = 94 → Wandler für Schutzaufgabe geeignet.

---

#### 24.10 Erdschlussschutz

- Die Art der Sternpunktbehandlung beeinflusst Fehlerstromgröße und Spannungserhöhungen.
- **Isoliertes Netz:** Erdschlussströme sehr klein, gespeist aus Kapazitäten der gesunden Leiter; Spannung der gesunden Leiter steigt auf verkettete Spannung.
  - Erfassung: kapazitive Richtungsrelais, angeschlossen an offene Dreieckwicklung des Spannungswandlers; Nullspannung wird gemessen.
  - Nullstrommessung: Stromwandler in Holmgreen-Schaltung oder Kabelumbauwandler (Summenstrom).
- **Kompensiertes Netz:** Drossel im Netzsternpunkt eingebaut (Petersen-Spule).
  - Induktiver Strom der Spule kompensiert kapazitiven Fehlerstrom.
  - Bei exakter Abstimmung fließt nur ohmscher Erdschlussreststrom (dient der Fehlerortung).
  - Fehlerstrom: I_CE = j × ω × C₀ × √3 × U_N
  - Gültigkeitsbereich Erdschluss: 10 A ≤ I_CE ≤ 35 A
  - Restfehlerstrom: I_Rest = (3 % bis 5 %) × I_CE
  - Drossel-Reaktanz: X_D = 1 / (3 × ω × I_CE)
- **Niederohmig geerdetes Netz:** Erdfehler = Kurzschluss → sofortige Abschaltung durch Kurzschlussschutz.
  - Erdkurzschlussstrom in Mittelspannung typisch auf max. 1,5 kA oder 2 kA begrenzt (über Widerstand).
  - Mindestkurzschlussstrom (einpolig) für Schutzauslegung: I″_k1min = √3 × c_min × U_n / (Z₁ + Z₀ + Z₀)

---

#### 24.11 Transformatorschutz

Schutzarten für innere und äußere Fehler:

- **Differentialschutz:** Überwachung Ein- und Ausgangsstrom; erfasst Kurzschlüsse und Erdschlüsse.
- **Buchholzschutz:** Wicklungs- und Windungsschlüsse, Ölverluste.
- **Überstromschutz:** Kurzschlüsse und Erdschlüsse; Einstellung abhängig vom Transformator-Bemessungsstrom.
- **Überlastschutz:** Thermorelais mit thermischem Abbild des Transformators.
- **Distanzschutz:** Kurzschlüsse und Erdschlüsse (Reserve).

**Praktische Anwendung nach Leistungsklasse:**
- Bis 630 kVA: HH-Sicherung mit Lasttrennschalter
- Ab 630 kVA: Leistungsschalter mit UMZ

**UMZ-Einstellungen (zweistufige Kennlinie):**
- Überstromstufe: I > = 1,2 bis 1,5 × I_N; t₁ > abhängig von vorgelagertem Schutzrelais (Reserveschutz)
- Hochstromstufe: I >> = 1,5 × I_k; t_I >> = 0,05 bis 0,1 s

**Differentialschutz-Eigenschaften:**
- Streng selektiv (nur Bereich zwischen Stromwandlern)
- Auf HV-Seite immer Reserveschutz (UMZ oder Distanzschutz) erforderlich
- Eigenschaften bei Zwei-/Dreiwicklertransformatoren:
  - Schaltgruppen- und Übersetzungsanpassung
  - Einsatz unabhängig von Sternpunktbehandlung
  - Schnellauslösung bei stromstarken Fehlern
  - Stabilisierung gegen Einschaltbruch mit 2. Oberschwingung
  - Stabilisierung gegen Übererregung mit 5. Oberschwingung

**Beispiel Stromwandlerauswahl für Differentialschutz (630 kVA, 20 kV / 0,4 kV):**
- I_rT,HV = 630 kVA / (√3 × 20 kV) = 18,18 A → Stromwandler 1: 30 A / 5 A
- I_rT,LV = 630 kVA / (√3 × 0,4 kV) = 909 A → Stromwandler 2: 1000 A / 5 A
- Sekundärströme: HV: 18,18 × (5/30) = 3,03 A; LV: 909 × (5/1000) = 4,54 A
- Übersetzungsverhältnis Zwischenstromwandler: 3,03 A / 4,54 A

---

#### 24.12 Sammelschienenschutz

- Aufgabe: selektiver, sicherer und schneller Schutz bei Sammelschienenkurzschlüssen und Schaltversagen.
- Einsetzbar bei unterschiedlichsten Sammelschienenkonfigurationen.
- Eigenschaften:
  - Erfassung und Abschaltung von Kurzschlüssen im Kuppelfeld (zwischen Stromwandler und Leistungsschalter) durch Strommessung und gezielte Verstimmung
  - Selektive Fehlererfassung
  - Auswertung des Differentialstroms
- Überstromschutzgeräte in den Abgängen zeitlich gestaffelt; Auslösezeit zur Sammelschiene hin zunehmend.
- **Rückwertige Verriegelung:** bei Fehler F2 (Abgang) werden alle Schutzgeräte angeregt; schnelle Stufe I >> (50 ms Verzögerung) in der Einspeisung wird blockiert; nächstgelegener Schutz löst aus.
- Bei Fehler auf der Sammelschiene selbst: Geräte in den Abgängen zeigen keine Überstromanregung.
- Bei mehrfacher Einspeisung (Motoren/Generatoren): richtungsabhängige Anregung auf Abgängen erforderlich.

---

#### 24.13 Hochspannungsmotorschutz

Fehlerursachen und Auswirkungen:
- Überlast (I_Last > I_Bemessungs): erhöhte Verluste und Temperaturen
- Blockierung (Stillstand): fehlende Belüftung → schnelle Erwärmung
- Spannungsabsenkung: Leistungsrückfluss, Drehmoment- und Drehzahlabnahme
- Spannungsunsymmetrie: durch unsymmetrische Lasten
- Interne Fehler: Kurzschluss und Erdschluss in der Wicklung

**Integrierte Schutzfunktionen:**
1. **Thermischer Überlastschutz** (Ständer- und Läuferkreis): nach IEC 255 Teil 8 / DIN VDE 0435 Teil 3011; Gerät erkennt automatisch Betriebszustand (Stillstand / Hochlauf / Betrieb) und passt Erwärmungs- und Abkühlzeitkonstanten an.
2. **Kurzschlussschutz:** phasenselektiv; digitale Filterung zur Grundwellenerkennung; Einschaltbruch wird beherrscht.
3. **Erdschlussschutz:** Im starr geerdeten Netz ist jeder einpolige Isolationsdurchbruch ein Kurzschluss; Erdstromeingang überwacht diesen Fehler.
4. **Schieflastschutz (Unsymmetrieschutz):** Auswertung des Gegensystemanteils des Ständerstroms; erfasst Spannungsunsymmetrien und Phasenausfall.

---

#### 24.14 Generatorschutz

Fehlerarten analog Motorschutz: Überlast, innerer Kurzschluss, Unsymmetrie. Kurzschlüsse an Generatorklemmen: behandelt in Abschn. 7.4.4.

Kriterien für Schutzumfang:
- Bemessungsleistung und Bauart der Maschine
- Bedeutung der Maschine in der Energieerzeugung
- Kraftwerkstechnologie und Antriebsenergie
- Richtlinien und Anforderungen des Betreibers

**Funktionsumfang Generatorschutzgerät:**
- Überstromzeitschutz
- Überlastschutz
- Rückleistungsschutz
- Untererregungsschutz
- Über- und Unterspannungsschutz
- Über- und Unterfrequenzschutz
- Schieflastschutz
- Erdschlussrichtungsschutz
- Windungsschlussschutz
- Läufererdschlussschutz
- Überspannungsschutz

---

#### 24.15 Strom- und Spannungswandler

- Aufgabe: hohe Ströme und Spannungen auf einheitliche, messbare Werte transformieren (Primär- und Sekundärseite galvanisch getrennt).
