# OEVE_OENORM_EN__50341 — Teil 5
> Quelle: OEVE_OENORM_EN__50341 (normen) · Teil 5 von 7 (Seiten 201-240 des Dokuments).

---

## Anhang D (Fortsetzung) — Statistische Auswertung von Windmessungen (Seiten 197–200)

### D.3 Beispiel für die Verwendung von C1 und C2

- Messzeitraum: n = 35 Jahre
- Mittelwert jährlicher Extremwerte: 33 m/s
- Variationskoeffizient: v = 0,12
- Wiederkehrperiode T = 50 Jahre → y = 3,9019 (aus Tabelle D.2)
- C1 = 1,1285; C2 = 0,5403 (n = 35, aus Tabelle D.1)
- Bemessungswindgeschwindigkeit: x = 44,8 m/s
- Zum Vergleich: „ideale" Gumbel-Verteilung (C1 = 1,2825, C2 = 0,5772, n → ∞) ergibt x = 43,3 m/s
- Differenz: +3,5 % (reale Verteilung höher als ideale)

### D.4 Berechnung von C1 und C2

Für n Messjahre werden Hilfswerte zi berechnet:
- `zi = -ln(-ln(i/(n+1)))` mit i = 1 bis n

Mittelwert: `z̄ = (1/n) · Σ zi` → C2 = z̄

Standardabweichung: `σz = √[(1/n) · Σ zi² - z̄²]` → C1 = σz

**Berechnungsbeispiel n = 10 (Tabelle D.5):**

| i | z | z² |
|---|-------|------|
| 1 | −0,8746 | 0,7649 |
| 2 | −0,5334 | 0,2845 |
| 3 | −0,2618 | 0,0685 |
| 4 | −0,0115 | 0,0001 |
| 5 | 0,2377 | 0,0565 |
| 6 | 0,5007 | 0,2507 |
| 7 | 0,7941 | 0,6306 |
| 8 | 1,1443 | 1,3094 |
| 9 | 1,6061 | 2,5795 |
| 10 | 2,3506 | 5,5254 |
| **Σ** | **4,9521** | **11,4702** |

Ergebnis:
- z̄ = 0,49521 → **C2 = 0,4952**
- σz = 0,9496 → **C1 = 0,9496**

Grenzwerte für n → ∞: C1 → π/√6 = 1,282549; C2 → 0,577216 (Euler-Zahl)

### Tabelle D.3 — Faktoren K(n, v, T) für Auslegungswerte aus Mittelwerten jährlicher Extremwerte (Auszug)

Wiederkehrdauern T = 3, 50, 150, 500 Jahre; Messzeiträume n = 10…40…∞; Variationskoeffizienten v = 0,10 … 0,70.

**Ausgewählte Werte (T = 50 Jahre):**

| n (Jahre) | v=0,10 | v=0,12 | v=0,20 | v=0,30 | v=0,50 | v=0,70 |
|-----------|--------|--------|--------|--------|--------|--------|
| 10 | 1,36 | 1,43 | 1,72 | 2,08 | 2,79 | 3,51 |
| 20 | 1,32 | 1,38 | 1,64 | 1,95 | 2,59 | 3,23 |
| 35 | 1,30 | 1,36 | 1,60 | 1,89 | 2,49 | 3,09 |
| ∞ | 1,26 | 1,31 | 1,52 | 1,78 | 2,30 | 2,82 |

**Ausgewählte Werte (T = 500 Jahre):**

| n (Jahre) | v=0,10 | v=0,20 | v=0,30 | v=0,50 | v=0,70 |
|-----------|--------|--------|--------|--------|--------|
| 10 | 1,60 | 2,20 | 2,81 | 4,01 | 5,22 |
| 35 | 1,50 | 1,99 | 2,51 | 3,51 | 4,52 |
| ∞ | 1,44 | 1,88 | 2,32 | 3,20 | 4,08 |

### Tabelle D.4 — Umrechnungsfaktoren von 50-Jahre-Extremwerten auf andere Wiederkehrdauern (Auszug)

Wichtig: Für T = 50 Jahre gilt stets Faktor = 1,00 für alle n und v.

**T = 3 Jahre (Umrechnungsfaktoren < 1):**

| n (Jahre) | v=0,10 | v=0,20 | v=0,50 | v=0,70 |
|-----------|--------|--------|--------|--------|
| 10 | 0,77 | 0,63 | 0,43 | 0,37 |
| 35 | 0,80 | 0,67 | 0,47 | 0,40 |
| ∞ | 0,81 | 0,69 | 0,49 | 0,42 |

**T = 150 Jahre:**

| n (Jahre) | v=0,10 | v=0,20 | v=0,50 | v=0,70 |
|-----------|--------|--------|--------|--------|
| 10 | 1,09 | 1,14 | 1,21 | 1,23 |
| 35 | 1,07 | 1,12 | 1,20 | 1,22 |
| ∞ | 1,07 | 1,11 | 1,19 | 1,21 |

**T = 500 Jahre:**

| n (Jahre) | v=0,10 | v=0,20 | v=0,50 | v=0,70 |
|-----------|--------|--------|--------|--------|
| 10 | 1,18 | 1,28 | 1,44 | 1,49 |
| 35 | 1,16 | 1,26 | 1,41 | 1,46 |
| ∞ | 1,14 | 1,24 | 1,39 | 1,45 |

> Nationale Fußnoten (österreichische Fassung): Werte 3,30 (T=150, n=10, v=0,50) und 1,12 (T=150, n=35, v=0,20) wurden in der englischen EN-Fassung irrtümlich abweichend angegeben.

---

## Anhang E (normativ) — Elektrische Anforderungen: Isolationskoordination (Seiten 201–212)

### E.1 Symboldefinitionen

| Symbol | Bedeutung |
|--------|-----------|
| Del | Mindestabstand Leiter – geerdete Bauteile (Blitz/Schaltstoß) |
| Dpp | Mindestabstand Außenleiter – Außenleiter (Blitz/Schaltstoß) |
| D50Hz_p_p | Mindestabstand Leiter – Leiter bei Betriebsfrequenz |
| D50Hz_p_e | Mindestabstand Leiter – geerdete Teile bei Betriebsfrequenz |
| d | Länge der Funkenstrecke (Schlagweite) |
| dis | Abstand Endpunkte der Isolatorkette |
| Ka | Höhenbeiwert |
| Kcs | Statistischer Koordinationsbeiwert |
| Kg | Funkenstreckenfaktor (für Schaltstöße als Basis) |
| Kg_ff | Blitzstoß-Funkenstreckenfaktor: Kg_ff = 0,74 + 0,26 · Kg |
| Kg_ff_is | Blitzstoß-Funkenstreckenfaktor für Isolatorketten |
| Kg_pf | Betriebsfrequenz-Funkenstreckenfaktor: Kg_pf = 1,35 · Kg − 0,35 · Kg² |
| Kg_sf | Schaltstoß-Funkenstreckenfaktor |
| Kz | Abweichungsfaktor |
| Kz_ff | Abweichungsfaktor Blitz: 0,961 |
| Kz_pf | Abweichungsfaktor Betriebsfrequenz: 0,91 |
| Kz_sf | Abweichungsfaktor Schaltstoß: 0,922 |
| N | Anzahl Standardabweichungen für Urw |
| P(U) | Überschlagswahrscheinlichkeitsfunktion |
| U2%_sf | Schaltstoß-Überspannung mit 2 % Überschreitenswahrscheinlichkeit |
| Ue2%_sf | Wie U2%_sf, Außenleiter–Erde |
| Up2%_sf | Wie U2%_sf, Außenleiter–Außenleiter |
| U100% | 100-%-Stehspannung der Funkenstrecke |
| U50% | 50-%-Stehspannung der Funkenstrecke |
| U50rp | 50-%-Stehspannung Spitze-Platte-Funkenstrecke |
| U50rp_sf | 50-%-Stehspannung Spitze-Platte bei Schaltstößen |
| U50rp_ff | 50-%-Stehspannung Spitze-Platte bei Blitzstößen |
| U50rp_50Hz | 50-%-Stehspannung Spitze-Platte bei Betriebsfrequenz |
| U90% | 90-%-Stehspannung der Funkenstrecke |
| U90%_ff_is | 90-%-Blitzstoßstehspannung der Leitungsisolatorketten |
| Ucw | Koordinationsstehspannung |
| Urp | Repräsentative Überspannung |
| Urw | Erforderliche Stehspannung der Funkenstrecke |
| Us | Höchste effektive Betriebsspannung (kV eff) |
| Z | Standardabweichung der Durchschlagsspannung |
| z | Variationskoeffizient: z = Z/U50% |

### E.2 Isolationskoordination

#### E.2.1 Theoretische Grundlagen
Methode aus ENV 50196, gestützt durch EN 60071-1, EN 60071-2 und CIGRE-Bericht 72.

#### E.2.2 Erforderliche Stehspannung in Luft Urw

**Statistische Beschreibung:** EN 60071-2 empfiehlt modifizierte Weibull-Verteilung; Verteilung bricht bei U50% − 3·Z ab.

**Formeln für Urw:**

- **Transiente Beanspruchungen (Blitz und Schaltstoß):**  
  Urw = U90% = U50% − 1,3·Z

- **Betriebsfrequente Spannungen (deterministisch):**  
  Urw = U100% = U50% − 3·Z

**Standardabweichungen:**
- Blitzstöße: z = 0,03 → Z = 0,03 · U50%
- Schaltstöße: z = 0,06 → Z = 0,06 · U50%
- Betriebsfrequente Spannungen: z = 0,03 → Z = 0,03 · U50%

**Abweichungsfaktoren Kz:** (Tabelle E.1)

| Belastungsart | Urw | Standardabweichung Z | Kz |
|---------------|-----|---------------------|----|
| Blitz | U90% = U50% − 1,3·Z | 0,03·U50% | **Kz_ff = 0,961** |
| Schaltvorgänge | U90% = U50% − 1,3·Z | 0,06·U50% | **Kz_sf = 0,922** |
| Betriebsfrequenz | U100% = U50% − 3·Z | 0,03·U50% | **Kz_pf = 0,910** |

**Funkenstreckenfaktoren:** U50% = Kg · U50rp

Umrechnung auf Schaltstoß-Basis:
- Schaltstoß: Kg_sf = Kg
- Blitzstoß: Kg_ff = 0,74 + 0,26·Kg
- Betriebsfrequenz: Kg_pf = 1,35·Kg − 0,35·Kg²

Gesamtformel: Urw = Kz · Kg · U50rp

**Funkenstreckenfaktoren Tabelle E.2:**

| Anordnung | Kg_sf = Kg |
|-----------|-----------|
| Leiter-Hindernis (Sicherheitsabstand) | **1,30** |
| Leiter-Mastfenster (Trag- oder V-Kette im Fenster) | **1,25** |
| Leiter-Mastkonstruktion (Tragkette am Querträgerende, V-Ketten) | **1,45** |
| Leiter-Leiter (innerer Abstand) | **1,60** |

> Anmerkung: Diese Werte sind beispielhaft; durch Versuche belegte andere Werte sind zulässig. Typische Werte: EN 60071-2, Anhang G.

**U50rp-Formeln für Spitze-Platte-Funkenstrecken:**

- Langsam ansteigende Überspannungen (d ≤ 25 m):  
  U50rp_sf = 1080 · ln(1 + 0,46·d) [kV Scheitel]; d in m

- Schnell ansteigende Überspannungen (Blitz, d ≤ 10 m):  
  U50rp_ff = 530 · d [kV Scheitel]; d in m

- Betriebsfrequente Spannungen:  
  U50rp_50Hz = 750 · 1,2 · ln(1 + 0,55·d)^0,83 [kV Scheitel]; d in m

#### E.2.3 Zu berücksichtigende Überspannungen

- **Schnell ansteigende Überspannungen (Blitz):** für Bereiche I und II nach EN 60071-1
- **Langsam ansteigende Überspannungen (Schaltvorgänge):** für Bereich II nach EN 60071-1

**Repräsentative Überspannungen (Tabelle E.3):**

| Beanspruchungsart | Außenleiter–Erde | Außenleiter–Außenleiter |
|--------------------|------------------|------------------------|
| Blitz | U90%_ff_is | 1,2 · U90%_ff_is |
| Schaltvorgänge | Kcs · Ue2%_sf | 1,4 · Kcs · Ue2%_sf |
| Betriebsfrequenz | √2 · Us / √3 [Scheitelwert] | √2 · Us [Scheitelwert] |

- Kcs = 1,05 für die Berechnung elektrischer Abstände → Überschlagsrisiko ~1×10⁻³
- U90%_ff_is (wenn unbekannt) = Kz_ff · Kg_ff_is · 530 · dis, mit Kz_ff = 0,961

#### E.2.4 Berechnungsformeln
Bedingung: Koordinationsstehspannung Ucw ≥ repräsentative Überspannung Urp

Ucw = Urw / Ka

Die Formeln für Del, Dpp, D50Hz_p_e, D50Hz_p_p sind in **Tabelle E.5** zusammengefasst (Seite 208).

**Tabelle E.5 — Berechnungsformeln:**

| Beanspruchungsart | Del | Dpp |
|--------------------|-----|-----|
| Blitz (schnell anst.) | Del = U90%_ff_is / (Ka · Kz_ff · Kg_ff · 530) | Dpp = 1,2 · U90%_ff_is / (Ka · Kz_ff · Kg_ff · 530) |
| Schaltstoß (langsam, >245 kV) | Del aus: Kcs·Ue2%_sf·Ka·Kz_sf·Kg_sf = 1080·ln(1+0,46·Del/e^1) | Dpp: 1,4-facher Faktor |
| Betriebsfrequenz | D50Hz_p_e = 750/(√3 · Us · Ka · Kz_pf · Kg_pf) ... | D50Hz_p_p analog |

Parameter:
- Ka: Höhenfaktor (Tabelle E.4)
- Kz_ff = 0,961; Kz_sf = 0,922; Kz_pf = 0,91
- Kg_pf = 1,35·Kg − 0,35·Kg²; Us in kV eff

#### E.2.5 Höhenfaktor Ka

Basiswerte für Höhen bis 1000 m. Für andere Höhen:

**Tabelle E.4 — Höhenfaktor Ka:**

| Höhe (m) | bis 200 kV | 201–400 kV | 401–700 kV | 701–1100 kV | über 1100 kV |
|----------|------------|------------|------------|-------------|--------------|
| 0 | 1,000 | 1,000 | 1,000 | 1,000 | 1,000 |
| 100 | 0,994 | 0,995 | 0,997 | 0,998 | 0,999 |
| 300 | 0,982 | 0,985 | 0,990 | 0,993 | 0,996 |
| 500 | 0,970 | 0,975 | 0,982 | 0,987 | 0,992 |
| 1000 | 0,938 | 0,946 | 0,959 | 0,970 | 0,978 |
| 1500 | 0,904 | 0,915 | 0,934 | 0,948 | 0,960 |
| 2000 | 0,870 | 0,883 | 0,906 | 0,923 | 0,938 |
| 2500 | 0,834 | 0,849 | 0,875 | 0,896 | 0,913 |
| 3000 | 0,798 | 0,815 | 0,844 | 0,867 | 0,885 |

> Quelle der Ka-Werte: IEC 61472 „Arbeiten unter Spannung – Kleinste Abstände für die Annäherung".

---

## Anhang F (informativ) — Elektrische Anforderungen: Berechnungsbeispiele (Seiten 209–213)

### F.1 Symboldefinitionen
Analog zu Anhang E (D50Hz, Del, Dpp, Ka, Kcs, Kg_sf, Kz_ff = 0,691, Kz_pf = 0,91, Kz_sf = 0,922, U2%_sf, U90%_ff_is, Us).

> Hinweis: Kz_ff in Anhang F mit 0,691 angegeben (abweichend von 0,961 in Anhang E — textliche Inkonsistenz im Originaldokument).

### F.2 Berechnungsbeispiele

#### F.2.1 Bereich I: 90-kV-Stromkreis mit 6 Kappenisolatoren (1000 m ü. NN)

- Höchste Betriebsspannung: Us = 100 kV
- Schaltüberspannungen: nicht zu berücksichtigen (Bereich I)
- U90%_ff_is = 385 kV (Außenleiter–Erde)
- Höhenfaktoren bei 1000 m:
  - Schnell anst. Ü., AE: Ka = 0,946; AA: Ka = 0,959
  - Betriebsfrequenz: Ka = 0,938

**Außenleiter-Mastfenster (Kg_sf = 1,25):**
- Blitz: Del = 385 / (0,946 × 0,961 × (0,74 + 0,26×1,25) × 530) = **0,75 m**
- Betriebsfrequenz: D50Hz_p_e = **0,21 m**

**Außenleiter–Außenleiter (Kg_sf = 1,60):**
- Blitz: Dpp = 1,2 × 385 / (0,959 × 0,961 × (0,74 + 0,26×1,60) × 530) = **0,82 m**
- Betriebsfrequenz: D50Hz_p_p = **0,30 m**

**Tabelle F.1 — Abstände, 90-kV mit 6 Kappenisolatoren:**

| Anordnung | Kg_sf | Del/Dpp | D50Hz |
|-----------|-------|---------|-------|
| Leiter–Mastfenster | 1,25 | Del = 0,75 m | D50Hz_p_e = 0,21 m |
| Leiter–Mastkonstruktion | 1,45 | Del = 0,71 m | D50Hz_p_e = 0,19 m |
| Leiter–Hindernis | 1,30 | Del = 0,74 m | — |
| Leiter–Leiter | 1,60 | Dpp = 0,82 m | D50Hz_p_p = 0,30 m |

#### F.2.2 Bereich I: 90-kV-Stromkreis mit 9 Kappenisolatoren (1000 m ü. NN)

- Höchste Betriebsspannung: Us = 100 kV (unverändert)
- U90%_ff_is = 557 kV (Außenleiter–Erde)
- Ka für schnell anst. Ü., AE und AA: 0,959

**Außenleiter-Mastfenster (Kg_sf = 1,25):**
- Blitz: Del = 557 / (0,959 × 0,961 × (0,74 + 0,26×1,25) × 530) = **1,07 m**

**Außenleiter–Außenleiter (Kg_sf = 1,60):**
- Blitz: Dpp = **1,18 m**

**Tabelle F.2 — Abstände, 90-kV mit 9 Kappenisolatoren:**

| Anordnung | Kg_sf | Del/Dpp |
|-----------|-------|---------|
| Leiter–Mastfenster | 1,25 | Del = 1,07 m |
| Leiter–Mastkonstruktion | 1,45 | Del = 1,02 m |
| Leiter–Hindernis | 1,30 | Del = 1,06 m |
| Leiter–Leiter | 1,60 | Dpp = 1,18 m |

> Anmerkung: Die Abstandswerte für 6 vs. 9 Isolatoren zeigen, dass el. Abstände für die gleiche Nennspannung je nach Leitungsisolation sehr unterschiedlich sind. Daher enthält Tabelle 5.2 Abstandswerte je Blitzstehstoßspannung.

#### F.2.3 Bereich II: 400-kV-Stromkreis (1000 m ü. NN)

- Höchste Betriebsspannung: Us = 420 kV
- Isolatorketten: 19 Kappenisolatoren
- U90%_ff_is = 1550 kV (schnell ansteigende Ü., AE)
- Kcs · U2%_sf = 1,05 × 1050 = **1103 kV** (AE, Schaltstoß)
- 1,4 · Kcs · U2%_sf = 1,4 × 1,05 × 1050 = **1544 kV** (AA, Schaltstoß)
- Höhenfaktoren bei 1000 m:
  - Langsam und schnell anst.: Ka = 0,978 (AE und AA)
  - Betriebsfrequenz: AE Ka = 0,946; AA Ka = 0,959

**Außenleiter-Mastfenster (Kg_sf = 1,25):**
- Blitz: Del = **2,92 m**
- Schaltstoß: Del = **3,20 m** (maßgebend)
- Betriebsfrequenz: D50Hz_p_e = **0,75 m**

**Außenleiter–Außenleiter (Kg_sf = 1,60):**
- Blitz: Dpp = **3,23 m**
- Schaltstoß: Dpp = **3,68 m** (maßgebend)
- Betriebsfrequenz: D50Hz_p_p = **1,17 m**

**Tabelle F.3 — Abstände, 400-kV-Stromkreis:**

| Beanspruchung | Leiter–Mastfenster (1,25) | Leiter–Mastkonstruktion (1,45) | Leiter–Hindernis (1,30) | Leiter–Leiter (1,60) |
|---------------|--------------------------|-------------------------------|------------------------|----------------------|
| Blitz Del/Dpp | Del = 2,92 m | Del = 2,78 m | Del = 2,89 m | Dpp = 3,23 m |
| Schaltstoß Del/Dpp | Del = 3,20 m | Del = 2,57 m | Del = 3,02 m | Dpp = 3,68 m |
| D50Hz | D50Hz_p_e = 0,75 m | D50Hz_p_e = 0,70 m | — | D50Hz_p_p = 1,17 m |

> Fazit: Bei 400 kV sind Schaltüberspannungen maßgebend, ausgenommen Del bei Kg_sf = 1,45 (durch Blitz bestimmt).

---

## Anhang G (normativ) — Erdungsanlagen: Bemessung (Seiten 214–227)

### G.1 Symboldefinitionen

| Symbol | Bedeutung |
|--------|-----------|
| A | Querschnitt Erdungsleiter oder Erder (mm²) |
| G | Kurzschlussstromdichte Erdungsleiter (A/mm²) |
| I | Leiterstrom in A (Effektivwert) |
| IB | Körperstrom |
| Id | Dauerstrom im Erdungsleiter |
| IE | Erdrückstrom |
| IEW | Strom im Erdseil (ausgeglichener Zustand) |
| K | Werkstoffkonstante (As1/2/mm²) |
| Ra | Zusätzlicher Widerstand (Ra = Ra1 + Ra2) |
| Ra1 | Widerstand des Schuhwerks |
| Ra2 | Ausbreitungswiderstand des Standortes |
| r | Reduktionsfaktor der Erdseile (Schirmfaktor) |
| s | Profilumfang (Leiter mit Rechteckquerschnitt) |
| tF | Fehlerdauer in s |
| UD | Potentialdifferenz (Spannungsquelle im Berührungskreis) |
| UT | Berührungsspannung in V |
| UTp | Zulässige Berührungsspannung |
| ZB | Gesamte Körperimpedanz in Ω |
| ZEW-E | Eigenimpedanz des Erdseiles |
| ZML-EW | Gegenimpedanz Leiter–Erdseil |
| β | Reziprokwert des Widerstand-Temperaturkoeffizienten bei 0 °C |
| θi | Anfangstemperatur des Erders (°C) |
| θf | Endtemperatur des Erders (°C) |
| ρE | Spezifischer Erdwiderstand nahe der Oberfläche (Ω·m) |
| 3I0 | Summe der Nullströme |

### G.2 Mindestmaße von Erdern (Tabelle G.1)

**Tabelle G.1 — Mindestabmessungen von Erdern und Schutzüberzügen:**

| Material | Art des Erders | Kerndurchmesser (mm) | Kernquerschnitt (mm²) | Beschichtungsdicke (mm) | Einzel (µm) | Mittel (µm) |
|----------|---------------|---------------------|----------------------|------------------------|-------------|-------------|
| Feuerverzinkter Stahl | Band | — | 90 | 3 | 63 | 70 |
| Feuerverzinkter Stahl | Profile (inkl. Platten) | — | 90 | 3 | 63 | 70 |
| Feuerverzinkter Stahl | Rohr | 25 | — | 2 | 47 | 55 |
| Feuerverzinkter Stahl | Rundstab Tiefenerder | 16 | — | — | 63 | 70 |
| Feuerverzinkter Stahl | Rundstab Oberflächenerder | 10 | — | — | — | 50 |
| Stahl mit Bleimantel | Runddraht Oberflächenerder | 8 | — | — | 1000 | — |
| Stahl mit extrudiertem Kupferüberzug | Rundstab Tiefenerder | 15 | — | — | 2000 | — |
| Stahl mit elektrolytischem Kupferüberzug | Rundstab Erdungsstäbe | 14,2 | — | — | 90 | 100 |
| Kupfer blank | Band | — | 50 | 2 | — | — |
| Kupfer blank | Runddraht Oberflächenerder | — | 25 c) | — | — | — |
| Kupfer blank | Verseiltes Kabel | 1,8 d) | 25 | — | — | — |
| Kupfer blank | Rohr | 20 | — | 2 | — | — |
| Kupfer verzinnt | Seil | 1,8 d) | 25 | — | 1 | 5 |
| Kupfer verzinkt | Band | — | 50 | 2 | 20 | 40 |
| Kupfer verzinkt | Seil | 1,8 d) | 25 | — | — | — |
| Kupfer mit Bleimantel | Runddraht | — | 25 | — | 1000 | — |

> Fußnoten:  
> a) Nicht zum direkten Einbetten in Beton geeignet.  
> b) Band: gewalzt oder geschnitten mit abgerundeten Kanten.  
> c) Unter extremen Bedingungen mit sehr geringer Korrosions-/Beschädigungsgefahr: 16 mm² zulässig.  
> d) Durchmesser des Einzeldrahtes.

### G.3 Berechnung der Stromtragfähigkeit

**Für Fehlerströme < 5 s (IEC 60724):**

`A = I · √tF · (1/K) · √ln((β + θf)/(β + θi))`

Parameter:
- A: Querschnitt in mm²
- I: Fehlerstrom in A (Effektivwert)
- tF: Fehlerstromdauer in s
- K: Werkstoffkonstante (Tabelle G.2)
- β: Kehrwert des Temperaturkoeffizienten bei 0 °C
- θi: Anfangstemperatur (default 20 °C Bodenumgebungstemperatur in 1 m Tiefe, wenn keine NNA/Projektspez. vorhanden)
- θf: Endtemperatur in °C

**Tabelle G.2 — Werkstoffkonstanten:**

| Werkstoff | β (°C) | K (As1/2/mm²) |
|-----------|--------|---------------|
| Kupfer | 234,5 | 226 |
| Aluminium | 228,0 | 148 |
| Stahl | 202,0 | 78 |

**Kurzschlussstromdichte G:**
- Aus Bild G.4 ablesen für Anfangstemperatur 20 °C, Endtemperatur bis 300 °C
- Kurvenbezeichnungen:
  - Kurve 1: Kupfer blank oder verzinkt (θf = 300 °C)
  - Kurve 2: Kupfer verzinnt oder mit Bleimantel (θf = 150 °C)
  - Kurve 3: Aluminium (nur Erdungsleiter, θf = 300 °C)
  - Kurve 4: Feuerverzinkter Stahl (θf = 300 °C)

**Für länger andauernde Fehlerströme** (isolierter/erdschlusskompensierter Sternpunkt): Dauerströme aus Bild G.5 (Kurven 1–4).

**Tabelle G.3 — Umrechnungsfaktoren Dauerstrom für abweichende Endtemperaturen (Basis: 300 °C):**

| Endtemperatur (°C) | Umrechnungsfaktor |
|--------------------|------------------|
| 400 | 1,20 |
| 350 | 1,10 |
| 300 | 1,00 |
| 250 | 0,90 |
| 200 | 0,80 |
| 150 | 0,70 |
| 100 | 0,60 |

> Hinweis: Für isolierte Leiter und Leiter in Beton sind geringere Endtemperaturen empfohlen.

### G.4 Berührungsspannung und Körperstrom

#### G.4.1 Berechnungsgrundlagen

Annahmen (für Hochspannungsanlagen):
- Strompfad: Hand → Füße
- 50-%-Wahrscheinlichkeit für Körperimpedanzwert
- 5-%-Wahrscheinlichkeit für Herzkammerflimmern
- Keine zusätzlichen Widerstände

Grundlage: IEC 60479-1, Kurve c2 von Bild 5 (Strompfad linke Hand → beide Füße)

**Tabelle G.6 — Zulässiger Körperstrom IB abhängig von Fehlerdauer tF:**

| tF (s) | IB (mA) |
|--------|---------|
| 0,05 | 900 |
| 0,10 | 750 |
| 0,20 | 600 |
| 0,50 | 200 |
| 1,00 | 80 |
| 2,00 | 60 |
| 5,00 | 51 |
| 10,00 | 50 |

**Tabelle G.7 — Gesamte Körperimpedanz ZB abhängig von Berührungsspannung UT (50 %-Wahrscheinlichkeit; Strompfad Hand–Hand oder Hand–Fuß):**

| UT (V) | ZB (Ω) |
|--------|--------|
| 25 | 3250 |
| 50 | 2625 |
| 75 | 2200 |
| 100 | 1875 |
| 125 | 1625 |
| 220 | 1350 |
| 700 | 1100 |
| 1000 | 1050 |

Korrekturfaktor für Strompfad Hand → Füße (statt Hand–Hand): **0,75** auf ZB.

**Tabelle G.8 — Fehlerdauer tF und zulässige Berührungsspannung UTp:**

| tF (s) | UTp (V) |
|--------|---------|
| 0,05 | 735 |
| 0,10 | 633 |
| 0,20 | 528 |
| 0,50 | 204 |
| 1,00 | 107 |
| 2,00 | 90 |
| 5,00 | 81 |
| 10,00 | 80 |

#### G.4.2 Berechnung mit zusätzlichen Widerständen (Tabelle G.10)

- Strompfad: linke Hand – beide Füße
- Körperimpedanz-Wahrscheinlichkeit: 50 %
- Kurve: c2 in Bild 14 von IEC 60479-1
- Zusätzlicher Widerstand: Ra = Ra1 + Ra2 = Ra1 + 1,5 · ρE
  - Ra1 = Schuhwerk-Widerstand
  - Ra2 = Erdausbreitungswiderstand des Standortes (1,5 · ρE)

**Berechnungsablauf:**
1. UTp(tF) aus Tabelle G.8 oder Kurve UD1 in Bild 6-2
2. ZB(UTp) aus Tabellen G.6 und G.7 (Interpolation)
3. IB = UTp / ZB
4. UD(tF) = UTp(tF) · (1 + Ra/ZB)

Typische Ra-Werte aus Bild 6-2:
- Ra = 0 Ω
- Ra = 1750 Ω (Ra1 = 1000 Ω, ρE = 500 Ω·m)
- Ra = 4000 Ω (Ra1 = 1000 Ω, ρE = 2000 Ω·m)
- Ra = 7000 Ω (Ra1 = 1000 Ω, ρE = 4000 Ω·m)

### G.5 Messung von Berührungsspannungen

Methode: **Strom-Sonden-Methode** (H.4 verweist darauf)

**Verfahren 1 (Messung mit Körperwiderstand 1 kΩ):**
- Messelektrodenfläche (Füße): 400 cm² gesamt; Auflagekraft ≥ 500 N
- Alternative: Sonde mindestens 20 cm tief eingetrieben
- Elektroden-Abstand zur Anlage: 1 m
- Bei Beton/trockenem Boden: Elektrode auf feuchtem Tuch oder Wasserfilm
- Schnellüberblick: Voltmeter mit hohem Innenwiderstand + 10 cm tiefe Sonde

**Verfahren 2 (Messung der Quellspannung UD):**
- Voltmeter mit hoher Impedanz
- Elektrode in 1 m Abstand vom exponierten Teil
- Weitere Berechnung nach G.4.2

### G.6 Reduktionsfaktor durch Erdseile

#### G.6.1 Allgemeines
Erdseile übernehmen Teil des Erdfehlerstroms → wirksame Entlastung der Erdungsanlage.

Reduktionsfaktor r:
`r = IE / 3I0 = (3I0 – IEW) / 3I0`

Für ausgeglichene Stromverteilung:
`r = (ZEW-E – ZML-EW) / ZEW-E = 1 – (ZML-EW / ZEW-E)`

- Je geringer der Abstand Leiter–Erdseil → r kleiner (bessere Reduktion)
- Je niederohmiger das Erdseil → r kleiner (bessere Reduktion)

#### G.6.2 Wertebereiche
- Reduktionsfaktoren: **0,2 bis 1,0**
- Abhängig von: Leitungsgeometrie, Anordnung Erdseile, Erdwiderstand, Anzahl Erdseile, Erdseile-Widerstand

---

## Anhang H (informativ) — Erdungsanlagen: Grundlagen, Berechnungen, Messungen (Seiten 214–232)

### H.1 Symboldefinitionen

| Symbol | Bedeutung |
|--------|-----------|
| D | L/π — Durchmesser des Ringerders |
| d | Durchmesser verseilter Erder oder halbe Breite Erdband / Tiefenerder-Durchmesser |
| I0 | Nullstrom während des Fehlers |
| IE | Erdfehlerstrom |
| Im | Gemessener Prüfstrom |
| L | Länge des Erdbandes / Tiefenerders |
| RE | Erdausbreitungswiderstand |
| RER | Ausbreitungswiderstand Ringerder |
| RES | Ausbreitungswiderstand Banderder |
| Rt | Mastfußausbreitungswiderstand |
| r | Reduktionsfaktor Erdseile |
| UE | Erdungsspannung |
| Uem | Gemessene Spannung Erdungsanlage–Bezugserde-Sonde |
| ZE | Erdimpedanz |
| ZS | Erdseilimpedanz eines Spannfeldes |
| ρE | Spezifischer Erdwiderstand (Ω·m) |

### H.2 Grundlagen für den Nachweis

#### H.2.1 Spezifischer Erdwiderstand (Tabelle H.1)

| Bodenart | ρE (Ω·m) |
|----------|---------|
| Sumpfboden | 5 bis 40 |
| Lehm, Ton, Humus | 20 bis 200 |
| Sand | 200 bis 2500 |
| Kies | 2000 bis 3000 |
| Verwitterter Fels | meist unter 1000 |
| Sandstein | 2000 bis 3000 |
| Granit | bis zu 50.000 |
| Moräne | bis zu 30.000 |

> Hinweis: ρE ändert sich mit Bodenfeuchtigkeit (zeitliche Schwankungen in den oberen Metern), Tiefe und Bodenart.

#### H.2.2 Erdausbreitungswiderstand

RE hängt hauptsächlich von der **Länge** des Erders ab (weniger vom Querschnitt).

**Formeln:**
- **Banderder:** RES = (ρE / πL) · ln(2L/d)
- **Ringerder:** RER = (ρE / π²D) · ln(2πD/d)
  - D = L/π (Durchmesser des Ringerders)
  - d = Seildurchmesser oder halbe Bandbreite (Annahme: 15 mm)

- **Tiefenerder (senkrecht):** RE = (ρE / 2πL) · ln(4L/d)
  - d = Tiefenerder-Durchmesser (Annahme: 20 mm)

- **Vermaschter Erder:** RE ≈ ρE / (2D), D = Durchmesser eines flächengleichen Kreises

### H.3 Einbau von Erdern und Erdungsleitern

#### H.3.1 Einbau von Erdern

**Oberflächenerder (H.3.1.1):**
- Verlegung in Grabensohle / Baugrube
- Mit leicht gestampftem Boden umgeben
- Kein direkter Kontakt mit Steinen/Kies
- Korrodierender Boden durch geeignetes Verfüllmaterial ersetzen

**Tiefenerder (H.3.1.2):**
- Mindestabstand zwischen Einzeltiefenerdern: ≥ Erderlänge
- Geeignete Werkzeuge zur Schadenvermeidung beim Eintreiben

**Verbindung der Erder (H.3.1.3):**
- Ausreichend für elektrische Leitfähigkeit und mechanische/thermische Festigkeit
- Korrosionsbeständig, kein galvanisches Element bilden
- Verbindungen mechanisch so fest wie die Stäbe selbst
- Bei Verbindung verschiedener Metalle: dauerhafter Schutz vor Elektrolytkontakt

#### H.3.2 Einbau von Erdungsleitern

**Verlegung (H.3.2.1) — so kurz wie möglich. Methoden:**
- **Eingegrabene isolierte Erdungsleiter:** nur Schutz gegen mechanische Schäden erforderlich
- **Zugänglich verlegte Erdungsleiter:** außerhalb Boden, bei Beschädigungsgefahr schützen
- **In Beton eingebettete Erdungsleiter:** zulässig; leicht zugängliche Klemmen an beiden Enden
- Korrosionsschutz besonders an Übergang blank–Boden/Beton beachten

**Verbindungen (H.3.2.2):**
- Gute elektrische Leitfähigkeit (keine unzulässige Temperaturerhöhung)
- Nicht locker werdend; gegen Korrosion geschützt
- Schutz vor Elektrolytkontakt bei unterschiedlichen Metallen
- Verbindungen ohne Werkzeug nicht lösbar

### H.4 Messungen an Erdungsanlagen

#### H.4.1 Messung spezifischer Erdwiderstände
Methode: **Vier-Sonden-Methode** (z.B. Wenner-Methode)
→ Bestimmung für unterschiedliche Tiefen möglich

#### H.4.2 Messung Ausbreitungswiderstand / Erdungsimpedanz

**a) Erdungsmessbrücke:**
- Für Erder und Erdungsanlagen kleiner/mittlerer Ausdehnung
- Frequenz ≤ 150 Hz
- Abstand Sonde vom Erder: ≥ 2,5-fache größte Ausdehnung, mindestens 20 m
- Abstand Hilfselektrode: ≥ 4-fache, mindestens 4 m

**b) Hochfrequenz-Erdungs-Messgerät:**
- Messung Erdwiderstand einzelner Mast ohne Erdseil-Abheben
- Frequenz des Messstroms hoch genug → Kettenimpedanz des Erdseils vernachlässigbar

**c) Strom-Spannungs-Methode:**
- Für große Erdungsanlagen und bei Potentialverschleppung
- Prüfstrom Im bei Netzfrequenz; Mindestabstand Erdungsanlage–ferner Erder: **5 km**
- Prüfstrom empfohlen > 50 A (um Störspannungen zu überbieten)
- Innenwiderstand Voltmeter ≥ 10-facher Erdausbreitungswiderstand der Sonde

Formel: ZE = Uem / (r · Im)
- Uem: gemessene Spannung Erdungsanlage–Bezugserde-Sonde
- Im: gemessener Versuchsstrom
- r: Reduktionsfaktor (Freileitungen ohne Erdseile: r = 1)

#### H.4.3 Bestimmung der Erdungsspannung

UE = ZE · IE

Näherungsformel für ZE mit Berücksichtigung Erdseile und Nachbarmaste:
`ZE = 0,25 · ZS + ZS · (ZS + 4·Rt) · Rt / (ZS + 4·Rt)` (vereinfacht)

Erdstrom: IE = r · 3 · I0

---

## Anhang J (normativ) — Stahlgittermaste (Seiten 229–240)

Verweise auf ENV 1993-1-1 (in Klammern angegeben).

### J.1 Symboldefinitionen

| Symbol | Bedeutung |
|--------|-----------|
| A | Querschnittsfläche / Bruttoquerschnittsfläche |
| Aeff | Nutz-Querschnittsfläche von Schrauben |
| Anet | Nettoquerschnitt bei Bohrungen |
| AS | Zugquerschnittsfläche Schrauben |
| b | Nennbreite |
| beff | Wirksame Breite eines Winkelschenkels |
| c | Abstand zwischen Bindeblechen |
| d | Schraubendurchmesser |
| d0 | Bohrungsdurchmesser |
| E | Elastizitätsmodul |
| e1 | Endabstand Bohrungsmitte – nächstes Profilende |
| e2 | Endabstand Bohrungsmitte – nächster Profilrand |
| F | Horizontale Einzellast |
| fu | Zugfestigkeit |
| fub | Zugfestigkeit Schrauben |
| fy | Streckgrenze |
| fyd | Auslegungsstreckgrenze = fy/γM1 |
| i | Trägheitsradius um Bezugsachse |
| L | Netzlänge |
| m | Anzahl der Winkelprofile |
| McRd | Bemessungsbiegemoment |
| Msd | Biegemoment im Querschnitt |
| N | Axiale Kraft |
| Nd | Druckkraft (Kraft im Druckstab) |
| NR,d | Bemessungswert Knickbeanspruchbarkeit |
| Nsd | Bemessungswert Zug- oder Druckkraft im Querschnitt |
| P1 | Bohrungsabstand in Lastrichtung |
| P | Bohrungsabstand rechtwinklig zur Stabachse |
| Sd | Zugkraft / Kraft im Stützstab (Zug oder Druck) |
| s | Versetzter Abstand (aufeinanderfolgende Bohrungen) |
| t | Dicke |
| Weff | Wirksames Widerstandsmoment |
| γM1 | Teilsicherheitsbeiwert (Biegung, Zug, Knicken) |
| γM2 | Teilsicherheitsbeiwert (Nettoquerschnitt an Schraubenbohrungen) |
| γMb | Teilsicherheitsbeiwert (Schraubenverbindungen) |
| λ | Schlankheitsgrad (maßgebende Knicklast) |
| λeff | Wirksamer Schlankheitsgrad |
| λ̄ | Dimensionsloser Schlankheitsgrad |
| λp | Breiten-Dicken-Verhältnis b/t |
| ρ | Reduktionsbeiwert |
| χ | Reduktionsfaktor |

### J.2 Einstufung in Querschnittsklassen (ENV 1993-1-1, Abschnitt 5.3)

#### J.2.1 Grundlagen
- Norm behandelt ausschließlich Winkelstähle (warm gewalzt oder kalt geformt)
- Winkelstähle = am häufigsten verwendete Stabform für Freileitungsmaste

#### J.2.2 Einstufung
Alle Querschnitte gehören **Klasse 3 oder 4** nach ENV 1993-1-1, 5.3.2.

#### J.2.3 Wirksame Querschnittswerte (druckbeanspruchte Stäbe)

Grundlage: wirksame Schenkelbreite beff

Berechnung:
- λp = b/t
- λ̄p = λp / (28,4 · ε · √Kσ) mit Kσ = 0,43 und ε = √(235/fy); fy in MPa
- beff = ρ · b

**Abminderungsbeiwert ρ für gewalzte Winkelstähle:**
- λ̄p ≤ 0,91: ρ = 1
- 0,91 < λ̄p ≤ 1,213: ρ = 2 − λ̄p/0,91
- λ̄p > 1,213: ρ = 0,98/λ̄p²

**Abminderungsbeiwert ρ für kalt geformte Winkelstähle:**
- λ̄p ≤ 0,809: ρ = 1
- 0,809 < λ̄p ≤ 1,213: ρ = (5 − λ̄p/0,404)/3
- λ̄p > 1,213: ρ = 0,98/λ̄p²

> beff dient zur Berechnung von Aeff und Weff. Kaltverformte Winkelstähle können alternativ nach ENV 1993-1-3 behandelt werden.

### J.3 Querschnitt

#### J.3.1 Bruttoquerschnitt
- Bestimmung mit Nennwerten der Abmessungen
- Lochschwächungen für Befestigungen **müssen nicht** abgezogen werden
- Stoßmaterial darf **nicht** mitgerechnet werden

#### J.3.2 Nettofläche
1. Beide Schenkel angeschlossen: Nettofläche = Summe der Nettoflächen beider Schenkel
2. Allgemein: Bruttofläche minus alle Bohrungen
3. Versetzte Bohrungen: zwei Werte berechnen, kleinerer maßgebend:
   - Wert 1: alle Bohrungen in senkrechtem Schnitt abziehen
   - Wert 2: alle Bohrungen längs einer Zick-Zack-Linie abziehen, für Schrägabstand s ≠ 0 Wert `s²t/(4p)` addieren
     - s = Abstand Mittelpunkte versetzter Bohrungen in Stablängsachse
     - p = Abstand rechtwinklig zur Stablängsachse
4. Nur ein Schenkel angeschlossen: Nettofläche = Nettofläche angeschlossener Schenkel + ½ Fläche des freien Schenkels
5. Nur eine Schraube: Nettofläche des angeschlossenen Schenkels

### J.4 Nachweis der Querschnittsbeanspruchbarkeit

#### J.4.1 Zugbelastung

**Beide Schenkel angeschlossen:**  
Nsd ≤ 0,9 · Anet · fu / γM2

**Ein angeschlossener Schenkel mit einer Schraube:**  
Nsd = (b1 − d0) · t · fu / γM2

**Ein angeschlossener Schenkel mit zwei oder mehr Schrauben:**  
Nsd = [(b1 − d0) + b2/2] · t · fu / γM2

Für Schweißverbindungen: ENV 1993-1-1, Abschnitt 6.6.10.

#### J.4.2 Druckbelastung
Nsd ≤ Aeff · fy / γM1

#### J.4.3 Biegemoment
McRd = Weff · fy / γM1

#### J.4.4 Biegung und axiale Kräfte
Kriterium:  
Nsd/(Aeff·fyd) + Msd_yy/(Weff_yy·fyd) + Msd_zz/(Weff_zz·fyd) ≤ 1

- Nur druckbeanspruchte Querschnittsteile bei Ermittlung von Aeff und Weff berücksichtigen

### J.5 Nachweis der Knickbeanspruchbarkeit

#### J.5.1.1 Biegeknicken

Bedingung: Nd / NR,d ≤ 1

Bemessungsknickbeanspruchbarkeit:  
NR,d = χ · Aeff · fy / γM1

Abminderungsbeiwert χ aus ENV 1993-1-1, Formel 5.46, abhängig von λ, E, fy und Knickspannungslinie.

**Bemessungsverfahren — nur Berechnung:**
- Knickspannungslinie: ENV 1993-1-1, Abschnitt 5.5.1 mit Imperfektionsbeiwert **α = 0,49**
- Schlankheit λ nach J.6 und J.7 (eingerahmte Werte können durch NNA ersetzt werden)
- Bezogene Schlankheit: λ̄ = λ/π · √(fy·Aeff/(E·A))

**Bemessungsverfahren — Berechnung + Belastungsprüfung im Originalmaßstab:**
- Knickspannungslinie **b** aus ENV 1993-1-1, 5.5.1
- Schlankheit λ nach J.6 und J.7 ohne Änderung eingerahmter Werte
- Wirksame Schlankheit λeff nach J.8 und J.9

> NNA oder Projektspezifikation legen Umfang erforderlicher Belastungsversuche fest.

#### J.5.1.2 Biegedrillknicken

Für gleichschenklige Winkel (Näherungsformel):  
λ_Biegedrill = (b/t) · √(5·Aeff·fy/(π·E·A))

#### J.5.2–J.5.4 Weitere Nachweise
- Biegedrillknicken von Biegeträgern: ENV 1993-1-1, 5.5.2
- Biegung + axiale Zugkraft: ENV 1993-1-1, 5.5.3
- Biegung + axiale Druckkraft: ENV 1993-1-1, 5.5.4 (unter Berücksichtigung J.5.1)

### J.6 Knicklänge von Stäben

#### J.6.1 Allgemeines
Knicklänge und Tragfähigkeit hängen von der Art der Ausfachung ab. Maßgebende Schlankheit λ für die zutreffende Knickform nach J.6.2 und J.6.3.

#### J.6.2 Eckstiele und Gurte

- Empfohlener **größter Schlankheitsgrad: 120** für Eckstiele und Gurte
- Üblicherweise einteilige Profile (mehrteilige: J.6.4)

**Schlankheitsgrade für einfache Stäbe (Bild J.3):**
- Eckstiele mit symmetrischer Ausfachung (a), (b): λ = **1,0 · L/ivv**
- Eckstiele mit Zwischenausfachungen (c): λ = **1,0 · L/iyy**
- Eckstiele mit versetzten Ausfachungen (d): λ = **1,0 · L/iyy**

#### J.6.3 Ausfachungsarten

**Allgemeines:**
- Primäre Diagonalausfachungen: Bild J.4
- Sekundäre Ausfachungen zur Unterteilung der primären Ausfachung/Eckstiele: Bild J.5
- **Größter Schlankheitsgrad primäre Diagonalstäbe: 200**
- **Größter Schlankheitsgrad sekundäre Ausfachungsstäbe: 240**
- Winkel zwischen Eckstielen und Diagonalen: **mindestens 15°**
- Bei langen Stäben: Biegespannungen infolge Windeinwirkung zusätzlich zu axialen Lasten berücksichtigen

**Einfache Diagonalen (J.6.3.2):**
- Einfache Diagonalausfachung (Bild J.4a): λ = **1,0 · L/ivv**
- Fall Bild J.4(b): λ = 1,0 · L1/ivv und λ = 1,0 · L2/iyy

---

*Ende Teil 5 (Seiten 201–240) — Teil 6 enthält die Fortsetzung der Stahlgittermast-Anhänge sowie weitere nationale Anhänge.*
