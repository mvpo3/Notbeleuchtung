# Planung von Elektroanlagen — Teil 7
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 281-320.

Dieser Teil behandelt den Abschluss des Kapitels Erdungen in Schaltanlagen (Kap. 13) mit Berechnungsformeln, Normenvergleich und mehreren durchgerechneten Beispielen, gefolgt von Kapitel 14 (Blitzschutzanlagen nach IEC 62305) und dem Beginn von Kapitel 15 (Niederspannungsanlagen).

## Inhalt

### 13.3 Erderarten — Formeln für Maschenerder und Ringerder

**Maschenerder (Ersatzradius in Ringform):**
- Durchmesser des Ersatzradius: D = sqrt(4·b·l / π)
- Potentialverteilung: φ(x) = I_E · ρ_E / (π · A) · arcsin(sqrt(A) / (2·x))

**Ringerder (wenn x > D/2):**
- Erdungswiderstand: R_E = ρ_E / (15·D) · ln(8·D/d)
- Potentialverteilung: φ(x) = I_E · ρ_E / (π² · D) · arcsin(D / (2·x))

**Fundamenterder:**
- Erdungswiderstand: R_E = 2·ρ_E / (π·D)
- Ersatzradius in Ringform: D = sqrt(4·b·l / π)

**Weitere Formeln aus der Literatur für Maschenerder:**
- Nach Koch: R_E ≈ 1,5 · ρ_E / (2·D)
- Nach Niemann: R_E ≈ ρ_E/(2·D) + ρ_E/(2·L)
- Nach Langrehr: R_E ≈ 0,5 · ρ_E / sqrt(A)
- Nach Laurent: R_E = ρ_E/4 · sqrt(π/A) + ρ_E/L
- Nach Schwarz: kombinierte Formel mit R1, R2, R12 (Parallelschaltung zweier Widerstandsanteile)

---

### 13.4 Bemessung von Erdungsanlagen

Für die Auslegung sind maßgebend: spezifischer Erdwiderstand, Ausbreitungswiderstand, thermische Belastung, Spannungen an der Anlage.

**Querschnittsberechnung Erdungsleitung (Fehlerströme bis 5 s):**
- Formel über zulässige Kurzschlussstromdichte:
  A = I_K / (σ · sqrt(t_f)) · ln((ϑ_f + ϑ_i) / (ϑ_i + ϑ'))

**Werkstoffkonstanten (Tab. 13.1):**

| Werkstoff | K [A·s/mm²] | ϑ [°C] |
|-----------|-------------|---------|
| Kupfer    | 226         | 235     |
| Aluminium | 146         | 228     |
| Stahl     | 78          | 202     |

**Ströme für Erdungs- und Berührungsspannungen (Tab. 13.2):**

| Netzsystem | EN 50522 | IEEE Std 80 |
|------------|----------|-------------|
| Niederohmig geerdet | w · I_E = I''_k1 | — |
| Kompensiert mit E-Spule | sqrt(I²_Esp + I²_Rest) | — |
| Kompensiert ohne Spule | sqrt(I_Rest) | — |
| Isoliert | sqrt(I_C) | — |

Bei Werkstoffauswahl ist neben der Strombelastbarkeit auch das Korrosionsverhalten zu berücksichtigen. Querschnitt alternativ über Kurzschlussstromdichte: A = I_G / σ

---

### 13.5 Berechnung der Erdungswiderstände

#### 13.5.1 TN-System (NS-Seite)

Grundbedingung: Erdungsspannung darf zulässige Berührungsspannung nicht überschreiten: U_E ≤ U_T

- Mit Erdschlusskompensation: R_E = U_E / I_Rest
- Ohne Erdschlusskompensation: R_E = U_E / I_C
- Kapazitiver Erdschlussstrom: I_C = sqrt(3) · U · ω · C_E
- Induktiver Widerstand der Löschspule: X_L = 1 / (3 · ω · C_E)

#### 13.5.2 TT-System (NS-Seite)

- Mit Erdschlusskompensation: R_E = U_E / I_Rest = 250 V / I_Rest
- Ohne Erdschlusskompensation: R_E = U_E / I_C = 250 V / I_Rest
- Mit niederohmiger Sternpunkterdung: R_E = 1200 V / I_E; wobei I_E = r · I''_k1

---

### 13.6 Gesamterdungswiderstand in NS-Netzen

Bei Außenleiter-Erde-Fehler muss nach DIN VDE 0100 Teil 410 gelten:
- R_B / R_E ≤ 50 V / (U_0 − 50 V)

Erdungswiderstand berechnet via: R_E = ρ_E / (π · L) · ln(2·L / d)

---

### 13.7 Erdschlusslöschspulen — Ausbreitungswiderstand

Bemessungsregeln für Hochspannungsschutzerde:
1. Beim Durchgang des maximalen Erdschlussstroms darf keine Erdungsspannung über 160 V entstehen.
2. In Umspannwerken und Maststationen mit Potentialsteuerung sind Erdungsspannungen bis 250 V zulässig.
3. Beim Zusammenschluss von HS-Schutzerder und NS-Betriebserde darf die Erdungsspannung 50 V nicht überschreiten.
4. Werden diese Grenzwerte nicht eingehalten, müssen HS-Schutzerder und NS-Betriebserde getrennt werden.
5. Mindestabstand zwischen zwei getrennten Erdern: 20 m

Formel: R_E = U_E / sqrt(I²_Esp + I²_Rest)  
mit I_Esp = 325 A, I_Rest = 60 A, U_T = 80 V

---

### 13.8 Zusammenschluss oder Trennung von Erdungsanlagen

- Zusammenschluss von HS-Schutzerder und NS-Betriebserde zulässig, wenn Erdungsspannung ≤ 80 V.
- In geschlossenen Anlagen: Grenzwert ≤ 160 V.
- Bei Nichterfüllung: Erder getrennt verlegen, Mindestabstand 20 m.

---

### 13.9 Hochspannungsschutzerder

#### 13.9.1 Holzmasten mit Schalter
Gerüstteile von Schaltern auf Holzmasten müssen nicht geerdet werden, wenn Vollkernisolatoren eingesetzt sind. Für den unter dem Isolator liegenden Gestängeteil ist ein Steuererder vorzusehen.

#### 13.9.2 Masten mit Schalter
Für Stahlgitter- und Stahlbetonmasten mit aufgesetzten Mastschaltern ist ein kombinierter Steuer- und Schutzerder vorzusehen. Erdungsspannung darf 250 V nicht überschreiten. Bei Überschreitung: Tiefenerder oder Standortisolierung mit Mindestbreite 1,25 m.

#### 13.9.3 Schalt- und Umspannpunkte
In jeder HS-Anlage ist ein Steuererder vorzusehen, der mit den übrigen Schutzerdern verbunden wird. Gas-, Öl- und Postleitungen sind ebenfalls mit dem HS-Schutzerder zu verbinden. Tiefenerder können an den Potentialring angeschlossen werden, wenn der Ziel-Erdungswiderstand nicht erreicht wird. Abstand zwischen Tiefenerdern: mindestens das Doppelte der Tiefenerder-Länge.

---

### 13.10 Niederspannungsbetriebserder

In NS-Ortsnetzen werden TN-C-N-Systeme mit Überstromschutzeinrichtungen eingesetzt, bei denen der PEN-Leiter über die gesamte Länge geerdet wird.

- Kabelnetze: In der Kabelgrube wird feuerverzinkter Bandstahl 40×3 mm verlegt, in jeden Kabelverteilerschrank eingeführt und mit Gehäuse sowie Schutzleiter verbunden.
- In Umspannstationen wird der Sternpunkt unmittelbar, über Widerstand, Spule oder isoliert geerdet.
- Netzausläufer sind im Bereich der letzten 200 m zu erden.
- Gesamterdungswiderstand von ≤ 2 Ω gilt in NS-Netzen (400/230 V) als ausreichend (kein Normwert, aber Praxiswert).
- Alle Erdungsleitungen sind grün-gelb zu kennzeichnen.
- Straßenbeleuchtungsmasten sind im Bereich der letzten 200 m zu erden.
- Im HS-Anlagenbereich: Masten möglichst vermeiden; falls nötig, kein PEN-Leiter am Rohrmast anschließen, Leuchte muss schutzisoliert sein.

---

### 13.11 Ausführung von Erdungsanlagen

Verbindliche Ausführungsregeln:
1. Spezifischen Erdbodenwiderstand vor Errichtung messen.
2. Zugängliche Trennstelle für Prüfzwecke vorsehen.
3. Erder als Oberflächenerder ausführen (soweit möglich).
4. Feuerverzinkter Bandstahl: Abmessungen 30 × 3,5 mm.
5. Verlegtiefe des Bandstahls: 0,5 bis 1,0 m, hochkant.
6. Winkel zwischen benachbarten Strahlern: mindestens 60°.
7. Strahler nach Möglichkeit gleich lang ausführen.
8. Lagepläne für Prüfungen anfertigen.
9. Alle fünf Jahre Sichtprüfung an ausgewählten Umspannpunkten und Masten.
10. Grenzzone "Luft-Erde" beachten.

---

### 13.12 Ersatzmaßnahmen zur zulässigen Berührungsspannung

Wenn die Erdungsanlage die Berührungsspannung nicht allein einhalten kann, gibt es folgende Alternativen:
- **Berührungsschutz:** nichtleitendes Material verwenden.
- **Standortisolierung:** Schotterschicht oder Kunststoffunterlage.
- **Potentialausgleich:** Verbindung aller vom Standort aus berührbaren metallenen Teile, die zu erden sind.
- **Potentialsteuerung:** Oberflächenerder.

---

### 13.13 Eliminierung von Messfehlern

Zwei bewährte Verfahren gegen Fremd- und Störspannungen bei Erdungsspannungsmessungen:

1. **Umpolungsverfahren:**
   - Messung mit netzsynchroner Spannungsquelle
   - Spannung wird um 180° elektrisch umgepolt
   - Symmetriefehler werden durch Polaritätswechsel eliminiert
   - In der stromlosen Pause werden Störspannungen erfasst

2. **Schwebungsverfahren:**
   - Messung mit nicht-netzsynchroner Spannungsquelle
   - Überlagerung mit 50-Hz-Störspannung erzeugt Schwebung im Messwert
   - Nach Messung von Minimum und Maximum lässt sich der Störeinfluss herausrechnen

---

### 13.14 Messung von Erdungsanlagen

Messkategorien:
1. Messung spezifischer Erdbodenwiderstände
2. Messung von Ausbreitungswiderständen bzw. Erdungsimpedanzen:
   - Erdungsmessbrücke: für Einzelerder und kleine Anlagen
   - Strom- und Spannungsmessung: für große Anlagen (z. B. Umspannwerke)
3. Messung von Erdungsspannungen
4. Messung von Berührungsspannungen:
   - Gemessen zwischen ausgewählten Metallteilen und Oberfläche in ca. 1 m Abstand
   - Messgerät mit 1 kΩ Innenwiderstand zur Körperwiderstandsnachbildung
   - Messsonden: Einstecktiefe 10–12 cm; Fußelektroden: Fläche 400 cm², Mindestbelastung 500 N

---

### 13.15 Erdungswiderstände in europäischen Ländern und USA (Tab. 13.3)

| Land | Eigene TR-Station | Haushalte | R_A | R_B |
|------|------------------|-----------|-----|-----|
| Italien | x | TT | ≤ 20 Ω | ≤ 2 Ω |
| Spanien | — | TT und IT | ≤ 20 Ω | ≤ 2 Ω |
| Frankreich | — | TT | ≤ 100 Ω | ≤ 2 Ω |
| Belgien | TN-C-S | TT | ≤ 30 Ω | — |
| Österreich | TN, TT | TT | ≤ 100 Ω | — |
| USA | TN | TN | LV ≤ 25 Ω, HV ≤ 1 Ω | 1–5 Ω |
| UK | TN | TT und TN-C-S | ≤ 200 Ω | ≤ 2 Ω |
| Deutschland | TN | TT und TN | kein Wert | kein Wert (nur Spannungswaage) |
| Niederlande | TN | TN, TT | ≤ 166 Ω | — |
| Irland | — | TT | ≤ 100 Ω | — |
| Norwegen | IT | IT | — | — |
| Schweiz | TN | TT und TN | — | — |

Hinweis: Betriebswiderstand R_B ≤ 2 Ω scheint in vielen Ländern Praxisstandard. Ausbreitungswiderstand R_A richtet sich nach dem Differenzstrom I_n des RCD. Abweichungen alle fünf Jahre prüfen.

---

### 13.16 Erdungsberechnung nach IEEE Std 80

Vorstellung der US-amerikanischen Norm IEEE Std 80-2013 (Leitfaden für Sicherheit in Wechselstrom-Unterwerk-Erdung).

#### 13.16.1 Tolerierbarer Körperstrom

- Fibrillationsschwelle nach Ferris et al.: 100 mA
- Nach Biegelmeier (50 kg Erwachsener): obere Schwelle 500 mA, untere 50 mA
- Tolerierbarer Körperstrom nach Dalziel (Grundlage IEEE Std 80):
  I_B = k / sqrt(t_s), wobei k = sqrt(S_B)
  - k₅₀ = 0,116 (50 kg Person)
  - k₇₀ = 0,157 (70 kg Person)
- Körperstrom 50 kg: I_B = 0,116 / sqrt(t_s)
- Körperstrom 70 kg: I_B = 0,157 / sqrt(t_s)
- Biegelmeier Z-Kurve: 500 mA-Grenze für Zeiten bis 0,2 s; abfallend auf 50 mA bei ≥ 2,0 s

#### 13.16.2 Zulässige Berührungsspannungen

Berechnung der Berührungsspannung (50 kg-Person):
- U_T50 = (1000 + 1,5 · C_s · ρ_s) · 0,116 / sqrt(t_F)

Berechnung der Berührungsspannung (70 kg-Person):
- U_T70 = (1000 + 1,5 · C_s · ρ_s) · 0,157 / sqrt(t_F)

Berechnung der zulässigen Schrittspannung (50 kg):
- U_S50 = (1000 + 6 · C_s · ρ_s) · 0,116 / sqrt(t_F)

Berechnung der zulässigen Schrittspannung (70 kg):
- U_S70 = (1000 + 6 · C_s · ρ_s) · 0,157 / sqrt(t_F)

Maximale Maschenspannung:
- E_m = ρ_E · K_m · K_i · I_G / (L_g + 1,15 · L_r · N_r)

Maximale Schrittspannung:
- E_S = ρ_E · K_s · K_i · I_G / (L_g + 1,15 · L_r · N_r)

#### 13.16.3 Berechnung des Leiterquerschnitts

Querschnitt als Funktion von Leiterstrom und Kurzzeittemperaturanstieg:
- A = I · sqrt(t_c · α_r · ρ_r · 10⁴ / TCAP) / ln[(K₀ + T_m) / (K₀ + T_a)]

#### 13.16.4 Maximaler Maschenfeherstrom

- Symmetrischer Strom: I_g = S_f · I_f
- Maximaler Maschenstrom mit Decrementfaktor: I_G = D_f · I_g

**Decrementfaktoren (Tab. 13.4):**

| Fehlerstromdauer t_F [s] | Decrementfaktor D_F |
|--------------------------|---------------------|
| 0,008 | 1,65 |
| 0,1   | 1,25 |
| 0,25  | 1,10 |
| > 0,5 | 1,0  |

- Teilungsfaktor des Fehlerstroms: S_f = I_g / (3 · I₀)
- Effektiv nichtsymmetrischer Fehlerstrom: I_F = I_g / (3 · I₀)
- Erdungsstrom: I_E = D_f · I_f
- Nullstrom: I₀ = E / [3·R_f + j·(R₁+R₂+R₀) + j·(X₁+X₂+X₀)]

**Größenbezeichnungen:**
- G = Kurzschlussstromdichte [A/mm²], M = Materialkonstante, t_F = Fehlerzeit [s]
- ϑ_e = zulässige Endtemperatur [°C], ϑ_a = Ausgangstemperatur [°C]
- U_E = Erdungsspannung [V], U_T = Berührungsspannung [V], R_E = Erdungswiderstand [Ω]
- I_Rest = Reststrom [A], I_C = kapazitiver Strom [A], w = Erwartungsfaktor (0,7)
- C_E = Erdkapazität [μF], X_L = induktiver Widerstand [Ω], R_B = Gesamterdungswiderstand [Ω]
- U₀ = Leiter-Erde-Spannung [V], r = Reduktionsfaktor, I''_k1 = einpoliger Kurzschlussstrom [A]
- C_s = Reduktionsfaktor bei Schotterschicht, ρ_s = spezifischer Erdbodenwiderstand [Ωm]
- D_F = Decrementfaktor (für t ≥ 0,5 s: D = 1), I₀ = Nullstrom [A]
- TCAP = Wärmekapazität [J/(cm³·°C)], T_m = maximal erlaubte Temperatur [°C], T_a = Umgebungstemperatur [°C]
- X₁, X₂, X₀ = Mit-, Gegen-, Nullreaktanz [Ω]; R₁, R₂, R₀ = entsprechende Resistanzen [Ω]

---

### 13.17 Beispiel: Berechnung einer Erdungsanlage (Umspannanlage)

Gegebene Anlage mit ermitteltem Gesamterdungswiderstand R_E = 0,0634 Ω und verschiedenen Erdfehlerstömen:

| Fehlerstrom | Erdungsspannung U_E | Berührungsspannung U_Tp | Abschaltzeit |
|-------------|--------------------|-----------------------|--------------|
| 1039 A | 65,9 V | 66 V | 10 s |
| 1873 A | 306 V* | 153 V | 0,64 s |
| 20 kA | 1268 V* | 634 V | 0,14 s |
| 300 A | 19,02 V | — | — |

*Höchster Fehlerstrom bestimmt die Relaiseinstellung: 0,14 s.

---

### 13.18 Beispiel: Erdungsanlage einer Transformatorstation

Angaben: ρ_E = 150 Ωm, Leiterduchmesser d = 0,02 m, vier Tiefenerder mit je 1,5 m Länge, Fundamentfläche 24 m × 10 m.

- Ersatzdurchmesser des Fundamenterders: D = sqrt(4·24·10/π) = 17,48 m
- Erdungswiderstand nach Laurent: R_T = ρ_E/(2·π·D) + ρ_E/L = 150/(2·π·17,48) + 150/68 = 6,49 Ω
- Erdungswiderstand nach Fundamenterder-Formel: R_T ≈ 2·ρ_E/(π·D) = 5,46 Ω
- Widerstand der vier Tiefenerder: R_s = ρ_E/(2·π·n·l) · ln(4·L/d) = 22,7 Ω
- Gesamtausbreitungswiderstand (Parallelschaltung): R_A = R_T · R_s / (R_T + R_s) = 4,4 Ω

---

### 13.19 Beispiel: Erdungswiderstand nach IEEE Std 80

Umspannanlage: 912,64 m², zwei 1000-MVA-Transformatoren, Spannungsebenen 154/33,6 kV.

**Netzdaten:**
- 154-kV-Netz: I''_k3 = 31,5 kA, I''_k1 = 25 kA, Abschaltzeit 1 s, 50 Hz, Sternpunkt geerdet, Reduktionsfaktor 0,45
- 33,6-kV-Netz: I''_k3 = 31,5 kA, I''_k1 = 1 kA, Abschaltzeit 1 s, 50 Hz, Sternpunkt geerdet, Reduktionsfaktor 0,45
- Spezifischer Erdungswiderstand ρ_E = 11,93 Ωm

**Querschnitt Erdungsleiter (154 kV, nach IEEE-Formel):**
- I_max = 25 kA, T_m = 300°C (Kupfer), T_a = 30°C, K₀ = 242°C, TCAP = 3,42 J/(cm³·°C), α_r = 0,00381 1/°C, ρ_r = 1,78 μΩ·cm
- Ergebnis: A = 146 mm²

**Querschnitt Erdungsleiter (33,6 kV):**
- Ergebnis: A = 6 mm²

**Maschenerder-Berechnung:**
- ρ_E = 11,93 Ωm, A = 912,64 m², L = 200 m, h = 0,5 m
- Gesamtausbreitungswiderstand: R_g = 0,23 Ω
- Nach EN 50522: R_h = ρ_E/(2·sqrt(A)) = 11,93/(2·sqrt(912,64)) = 0,197 Ω
- Erdungsimpedanz: Z_g = 0,171 Ω

**Strom für den Maschenerder:**
- n = 3, U₀ = 46,1 kV, Z₀ = 25,64 Ω
- I_n = n · 3 · U₀/Z₀ = 1,62 kA
- I_g = 1,63 kA

**Erdungspotentialanhebung:** U_E = I_g · R_g = 376,2 V

**Berührungsspannung:**
- Kritisch: E_t = [1000 + 1,5·C_s·(h_s·k)·ρ_s] · k/sqrt(t_s) = 160 V (mit C_s = 1)
- Berechnet (Leiterabstand D = 6 m, d = 0,014 m, n_a = 6, n_b = 4): E_m = K_m · K_im · ρ_E · I_g / L = 114,9 V
- Ergebnis: E_m < E_t → zulässig

**Schrittspannung:**
- ρ_s = 11,93 Ωm, t_s = 1 s, C_s = 1,0
- Grenzwert: E_step = [1000 + 6·C_s·(h_s·k)·ρ_s] · k/sqrt(t_s) = 168,2 V
- Berechnet (D = 6 m, d = 0,014 m, n_a = 6): E_s = 68,6 V
- Ergebnis: E_s < E_step → zulässig

---

### 13.20 Beispiel: Querschnittsermittlung Erdungsleitung HS-Schaltanlage

Gegeben: Netzkurzschlussleistung 350 MVA, Nennspannung 20 kV, Transformator 630 kVA, u_kr = 6 %, 400 V.

**Fehlerstrom HS-Seite:**
- I''_k2E = S''_kQ / (2·U_n) = 350 MVA / (2·20 kV) = 8,75 kA
- Querschnitt nach DIN VDE 0101 mit σ_G = 180 A/mm² (Fehlerzeit 1 s): S = 8750/180 = 48,61 mm² → gewählt 50 mm²

**Impedanz NS-Seite:**
- Netzimpedanz: Z_Q = c·U²_n / S''_kQ = 1,1·400²/350·10⁶ = 0,5 mΩ
- Transformatorimpedanz: Z_T = u_kr · U²_rT / S_rT = 6%·400²/630·10³ = 15,2 mΩ
- Einpoliger Erdkurzschluss: I''_k1E = c·U_n/(sqrt(3)·(2·Z_Q + Z_T)) = 0,9·400/(sqrt(3)·(1+15,2)·10⁻³) = 12,83 kA
- Querschnitt mit σ_G = 270 A/mm² (Fehlerzeit 0,5 s): S = 12830/270 = 47,51 mm² → gewählt 50 mm²

**Doppelterdschluss:**
- I''_kEE = 0,85 · 12,83 kA = 10,90 kA
- Mit Reduktionsfaktor für Erdkabel: I''_kEE = 0,65 · 10,90 kA = 7,08 kA
- Dieser Strom ist maßgebend für die Querschnittsbemessung.

---

### 13.21 Beispiel: Querschnittsermittlung Sternpunktleitung

Zwei Varianten:

**a) Betriebserdungswiderstand und Schutzerdungswiderstand getrennt verlegt:**
- R_B = 2 Ω, R_A = 20 Ω
- Fehlerstrom: I_F = 230 V / (R_A + R_B) = 230/(2+20) = 10,45 A → gewählt 50 mm²

**b) Betriebserdungs- und Schutzerdungswiderstand zusammengeführt:**
- Fehlerstrom fließt über Transformatorsternpunkt, bei 630-kVA-Trafo: I = 22 kA
- Querschnitt: S = I · sqrt(t) / σ_k = 22000 · sqrt(0,5) / 159 = 107 mm² → gewählt 3 × 40 mm Kupfer

---

### 13.22 Zusammenfassung Erdungsanlagen (Kap. 13)

Erdungsanlagen schützen Personen, Tiere und Sachwerte bei Kurzschlüssen, Blitz- und Schalthandlungen. Zulässige Schritt- und Berührungsspannungen sowie Erdungswiderstände dürfen nicht überschritten werden.

Normative Grundlage:
- NS-Anlagen: DIN 18014 und DIN VDE 0100-540
- HS-Anlagen: DIN EN 50522
- Für Blitzschutzanlagen gilt R_E < 10 Ω (einziger normativ festgelegter Wert)
- In der Praxis wird R < 2 Ω angestrebt (kein Normwert), in der Hochspannung < 1 Ω.

---

## Kapitel 14: Blitzschutzanlagen

Normgrundlage: IEC 62305 (VDE 0185-305) — gilt für Errichtung, Planung und Erweiterung von Blitzschutzanlagen. Enthält keine Aussagen über die Blitzschutzbedürftigkeit von Bauwerken.

### 14.1 Begriffe

- **Ableiter:** Betriebsmittel aus Funkenstrecken und Varistoren; Schutz vor unzulässig hohen Überspannungen. Unterteilt in:
  - Blitzstromableiter: für Direkt- oder Naheinschläge zwischen Blitzschutzzone 0 und 1
  - Überspannungsableiter: für Ferneinschläge und Schaltüberspannungen zwischen Zone 1 und anderen Zonen
- **Ableitvermögen:** Leistungsfähigkeit des Ableiters:
  1. Blitzprüfstrom I_imp → Anforderungsklasse B
  2. Stoßströme I_sn oder I_max → Anforderungsklassen A und C
  3. Kombinierter Stoß U₀c → Anforderungsklasse D
- **Bemessungsspannung:** maximale Betriebsspannung, für die der Ableiter ausgelegt ist und seine Kenndaten erfüllt
- **Blitzschutzsystem:** verhindert physikalische Schäden durch direkte Einschläge
- **Schutzpegel:** kennzeichnet die Fähigkeit des Ableiters, Störungen auf einen ungefährlichen Spannungswert zu begrenzen
- **Überspannungsschutzgerät (SPD):** begrenzt transiente Überspannungen und leitet Stoßströme ab

IEC 62305 regelt: Blitzschutzklassen, äußerer Blitzschutz, Erder, Näherungsbestimmungen, Blitzschutzpotentialausgleich.

Blitzschutzanlagen umfassen:
1. Äußerer Blitzschutz
2. Innerer Blitzschutz
3. Überspannungsschutz elektronischer Geräte

---

### 14.2 Äußerer Blitzschutz

Alle Einrichtungen zum Auffangen und Ableiten des Blitzstroms in die Erdungsanlage. Bestandteile:
- Fangeinrichtung
- Ableitungen
- Erdungsanlage

#### 14.2.1 Fangeinrichtung

Besteht aus Fangleitungen und Fangstangen. Drei Methoden zur Lagebestimmung:
1. Schutzwinkelmethode (α) — für einfache Formen
2. Blitzkugelmethode (Radius r) — für komplizierte Fälle
3. Maschenmethode (w) — für ebene Flächen

#### 14.2.2 Ermittlung der Blitzschutzklasse

Wirkungsgrad: E = 1 − N_c / N_d, mit N_c = zulässige kritische Einschläge/Jahr, N_d = Einschlaghäufigkeit in die Anlage/Jahr.

**Blitzschutzklassen (Tab. 14.1):**

| Klasse | Kugelradius [m] | Maschenweite [m] | Wirkungsgrad [%] |
|--------|----------------|------------------|------------------|
| I      | 20             | 5 × 5            | 98               |
| II     | 30             | 10 × 10          | 95               |
| III    | 45             | 15 × 15          | 90               |
| IV     | 60             | 20 × 20          | 80               |

**Einschlaghäufigkeit — Komponenten:**

Faktor A (Gebäudekonstruktion): A = A1 · A2 · A3 · A4

**Gebäudekonstruktionsdaten (Tab. 14.2):**

| Bauart der Wände | A1 |
|------------------|----|
| Bewehrter Ortbeton / durchgehende Metallfassade | 5 |
| Leitend verbundene Fertigteile / Stahl-/Betonkonstruktion | 4 |
| Mauerwerk, Beton ohne Bewehrung, nicht verbundene Fertigteile | 0,5 |
| Holzfachwerk oder andere Baustoffe | 0,1 |

| Dachkonstruktion | A2 |
|------------------|----|
| Stahl | 4 |
| Stahlbeton | 2 |
| Stahlbetonfertigteile | 0,5 |
| Holz | 0,1 |

| Dachdeckung | A3 |
|-------------|----|
| Bewehrter Beton | 4 |
| Blech | 2 |
| Ziegel, Schiefer | 1 |
| Kunststofffolien, Dachpappe, Kiespressdach | 0,5 |
| Weichdächer | 0,05 |

| Dachaufbauten | A4 |
|---------------|----|
| Keine Dachaufbauten | 1,0 |
| Nicht geerdete Metallteile, Antennen | 0,5 |
| Elektrogeräte | 0,2 |
| Empfindliche elektrische Dachaufbauten (Rinnenheizung, Temperaturfühler) | 0,1 |

Faktor B (Nutzung/Inhalt): B = B1 · B2 · B3 · B4

**Gebäudenutzung und -inhalt (Tab. 14.3):**

| Nutzung durch Personen | B1 |
|------------------------|----|
| Keine Panikgefahr | 1,0 |
| Mäßige Panikgefahr | 0,1 |
| Große Panikgefahr | 0,01 |

| Art des Gebäudeinhalts | B2 |
|------------------------|----|
| Nicht brennbar, schwer entflammbar | 1,0 |
| Entflammbar | 0,2 |
| Explosionsfähige Anlage | 0,1 |
| Explosionsgefährdete Anlage | 0,01 |
| Kerntechnische Anlage | 0,01 |

| Wert des Gebäudeinhalts | B3 |
|-------------------------|----|
| Einfache Einrichtung | 1,0 |
| Wertvolle Einrichtung | 0,2 |
| Besonders wertvolle Einrichtung | 0,1 |
| Unersetzliche Einrichtung | 0,01 |

| Schadensverringerungsmaßnahmen | B4 |
|--------------------------------|----|
| Automatische Feuerlöscheinrichtung | 10 |
| Feuerhemmende Einrichtungen | 5 |
| Feuermeldeeinrichtungen | 2 |
| Keine Maßnahmen | 1 |

Faktor C (Folgeschäden): C = C1 · C2 · C3

**Folgeschäden (Tab. 14.4):**

| Umweltgefährdung | C1 |
|------------------|----|
| Keine | 1,0 |
| Mäßig | 0,5 |
| Hoch | 0,1 |
| Sehr hoch | 0,01 |

| Ausfall wichtiger Versorgungsleitungen | C2 |
|----------------------------------------|----|
| Kein Ausfall | 1,0 |
| Erheblicher Ausfall | 0,1 |
| Sehr hoher Ausfall | 0,01 |

| Sonstige Folgeschäden | C3 |
|-----------------------|----|
| Geringe | 1,0 |
| Wertvolle Einrichtung | 0,2 |
| Mäßige | 0,5 |
| Hohe | 0,1 |
| Sehr hohe | 0,01 |

Gesamthäufigkeit: D = A · B · C

**Direkte Einschlaghäufigkeit:**
N_d = N_g · A_e · C_e / 10⁶

- N_g = mittlere jährliche Erdblitzdichte [Einschläge/km²·Jahr]
- A_e = äquivalente Fangfläche für freistehendes rechtwinkeliges Gebäude: A_e = L·W + 6·H·(L+W) + 9·π·H²
- C_e = Umgebungskoeffizient

**Umgebungskoeffizienten (Tab. 14.5):**

| Relative Lage | C_e |
|---------------|-----|
| Im großen Gebiet mit gleich hohen oder höheren Gebäuden/Bäumen | 0,25 |
| Umgeben von kleineren Gebäuden | 0,5 |
| Freistehend, keine Objekte innerhalb 3·H | 1 |
| Freistehend auf Bergspitze oder Kuppe | 2 |

#### 14.2.3 Ableitung

Ableitungen verbinden Fangeinrichtung und Erdungsanlage elektrisch leitend. Anforderungen:
- Trennstellen für Mess- und Prüfzwecke vorzusehen
- Mindestens zwei Ableitungen pro Gebäude
- Symmetrisches Gebäude: ungerade Ableitungsanzahl um 1 erhöhen; gerade bleibt unverändert
- Unsymmetrisches Gebäude: ermittelte Anzahl bleibt unverändert
- Gebäude mit Satteldächern bis 12 m Länge/Breite: gerade Anzahl bleibt unverändert

#### 14.2.4 Erdungsanlage

Flächenhafte Erdungsanlage für jede Blitzschutzanlage erforderlich. Kein bestimmter Erdungswiderstand gefordert; in der Praxis gilt R_E ≤ 10 Ω als ausreichend.

IEC 62305 unterscheidet zwei Anordnungstypen:

**Typ A:**
- Oberflächenerder
- Tiefenerder

**Typ B:**
- Ringerder
- Fundamenterder

**1. Oberflächenerder:**
- Verlegetiefe: 0,5 bis 0,8 m
- Mindestlänge: 20 m
- Ausbreitungswiderstand: R_E = ρ_E/(π·L) · ln(2·L/d)
- Näherungsformel (L ≥ 10 m): R_E ≈ 2·ρ_E/L

**2. Tiefenerder:**
- Senkrecht verlegt, Länge 9 m, Abstand ≥ 1 m zur baulichen Anlage
- Ausbreitungswiderstand: R_E = ρ_E/(2·π·L) · ln(4·L/d)
- Näherungsformel: R_E ≈ ρ_E/L

**3. Ringerder:**
- Oberflächenerder, Tiefe 0,5 m, geschlossener Ring, Abstand 1 m zur Anlage
- Werkstoffe und Mindestmaße nach DIN VDE 0185 Teil 1 Tab. 2
- Ausbreitungswiderstand: R_E = ρ_E/(2·π²·D) · ln(2·D/d)
- Näherungsformel: R_E ≈ 2·ρ_E/(3·D)
- D = 1,13·sqrt(A) (A = umschlossene Fläche)

**4. Fundamenterder:**
- Nach DIN 18014 in Betonfundament eingebettet; geeignet für Blitzschutz-, Elektro- und Fernmeldeanlagen
- Als geschlossener Ring auszuführen
- Maschenweite: max. 20 m × 20 m
- Material: Bandstahl mindestens 30 mm × 3,5 mm oder Rundstahl mindestens Ø 10 mm
- Hochkant verlegen
- Stahl darf verzinkt oder unverzinkt sein
- Betonüberdeckung: mindestens 5 cm
- Abstandshalter zur Lagerung vorsehen
- Schutz gegen Feuchtigkeitseindringen erforderlich
- Verbindungen über Kreuzverbinder oder Keilverbinder
- Anschlussfahnen müssen gegen Korrosion geschützt sein
- Näherungsformel Ausbreitungswiderstand: R_E ≈ 2·ρ_E/(π·D), mit D = sqrt(4·L·B/π)

#### 14.2.5 Trennungsabstand

Trennungsabstand von Fangeinrichtungen und Ableitungen zu Metallinstallationen muss durch Vergrößerung des Abstands an Näherungsstellen eingehalten werden (Brandgefahr und Anlagenzerstörung sonst möglich).

Formel: s = k_i · k_c / k_m · l

- s = Trennungsabstand [m]
- k_c = geometrieabhängiger Stromaufteilungskoeffizient (Tab. 14.6)
- k_m = materialabhängiger Koeffizient (Tab. 14.7)
- k_i = schutzklassenabhängiger Koeffizient (Tab. 14.7)
- l = Länge entlang Fangeinrichtung oder Ableitung

**Koeffizient k_c (Tab. 14.6):**

| Anzahl Ableitungen | k_c |
|--------------------|-----|
| 1 | 1 |
| 2 | 0,66 |
| > 3 | 0,44 |

**Koeffizienten k_i und k_m (Tab. 14.7):**

| LPS-Schutzklasse | k_i | Material | k_m |
|------------------|-----|----------|-----|
| I | 0,08 | Luft | 1 |
| II | 0,06 | Feststoff | 0,5 |
| III–IV | 0,04 | — | — |

Drei Varianten für Stromaufteilungskoeffizient k_c:
1. Freistehende Fangmasten mit dazwischenliegenden Fangseilen oder Fangleitung auf First mit Ableitungen: k_c = (c + f)/(2·c + f)
2. Vermaschtes Fangleitungsnetz auf Flachdach, kein Ringleiter: k_c = 1/(2·n) + 0,1 + 0,2 · (r_c/h)^(1/3)
3. Vermaschtes Netz mit einem oder mehreren Ringleitern

---

### 14.3 Innerer Blitzschutz

Umfasst:
- Blitzschutz- und Schutzpotentialausgleich
- Beseitigung von Näherungen
- Überspannungsschutz als zusätzliche Maßnahme

#### 14.3.1 EMV-Blitzschutzzonenkonzept

Vier Bereiche werden unterschieden:
1. Äußerer Blitzschutz
2. Gebäudeschirmung
3. Raumschirmung
4. Geräteschirmung

Grundprinzip: Raumabschirmung.

#### 14.3.2 Überspannungsschutz

Zusätzliche Maßnahme zum Schutz elektrischer Geräte. Bei Blitzstromableitern: Anforderungsklassen nach DIN VDE 0675 Teil 6 einhalten. Ableiter auf kürzestem Weg mit Potentialausgleichsschiene verbinden.

DIN VDE 0100-534: Anforderungen für Auswahl und Errichtung von Überspannungsschutzeinrichtungen (SPDs) gegen transiente Überspannungen infolge atmosphärischer Entladungen, wenn SPD-Errichtung nach DIN VDE 0100-443 gefordert ist. SPDs mindestens Typ 2 müssen so nah wie möglich am Speisepunkt der elektrischen Anlage errichtet werden.

**Anschlussquerschnitte von Ableitern (Tab. 14.8):**

| Netz-/Vorsicherung | bis 125 A | 160 und 200 A | 250 A |
|--------------------|-----------|---------------|-------|
| PVC-Kupfer Typ B | 16 mm² | 25 mm² | 35 mm² |
| PVC-Kupfer Typ C | 16 mm² | 25 mm² | 35 mm² |
| Wenn A < 16 mm²: B = A |

Dreistufiges Schutzkonzept (IEC 664 A / DIN VDE 0110-1):
- Stufe a: Blitzstromableiter
- Stufe b: Überspannungsableiter
- Stufe c: Geräteschutz

---

### 14.4 Zusammenfassung Blitzschutzanlagen (Kap. 14)

Blitzeinschläge verursachen jährlich Millionenschäden; öffentliche Gebäude sind gegen Blitz zu schützen, Überspannungsableiter in jedem Gebäude zu installieren. Für die Entscheidung über Blitzschutznotwendigkeit ist nach DIN EN 62305 immer ein Risikomanagement durchzuführen.

---

## Kapitel 15: Niederspannungsanlagen (Beginn)

### 15.1 Anwendungsbereich und Grundanforderungen

Niederspannungsanlagen finden Einsatz in Industrie, Hochhäusern, Wohnungen, Bürogebäuden, Motor Control Centern sowie Klima- und Heizungsanlagen bis 1 kV. Einspeisung aus 20-kV- oder 10-kV-Netz.

- Bemessungsspannung: 400/230 V, 50 Hz (Standard)
- Industrie-Sonderfall: 690 V für Motor Control Center
- Schienenverteiler in Industrie und Hochhäusern: Vorteile sind großer Energietransport, geringe Brandlast, geringer Spannungsfall
- Einfamilienwohnungen bis 63 A: Installationsverteiler in der Wand
- Größere Leistungen: Standverteiler
- Noch größere Abnehmerleistungen können direkt von der Ortsnetzstation versorgt werden

**Anforderungen an NS-Schaltanlagen:**
- Netz möglichst einfach und übersichtlich
- Optimaler Schutz der eingebauten Geräte
- Gute Versorgungssicherheit und geringe Netzverluste
- Bedienungs- und wartungsfreundlich
- Gute Versorgungsqualität, geringer Oberschwingungsgehalt
- Strahlenform bevorzugt
- Projektbezogene Vorschriften beachten

Nach IEC 61439-2 (VDE 0660-600-2) zeichnen sich NS-Schaltanlagen durch Kombinationsmöglichkeiten verschiedener Einbautechniken und variabler innerer Unterteilung aus:
- Feld 1: Leistungsschalter bis 6300 A (Einspeisung, Kupplung, Abgang)
- Feld 2: Abzweige in Festeinbau, Einschub- oder Stecktechnik
- Feld 3: Kabelabgänge in Stecktechnik (Austausch im Betrieb möglich)
- Feld 4: Festeinbautechnik
- Feld 5: Leistentechnik, Geräte fest angeschlossen
- Feld 6: z. B. Zentralkompensation

**Netzausführung und Kabelquerschnitte:**
- NS-Anlagen als Strahlennetz ausgeführt
- Zuleitung: NAYY 4×150 mm² (max. Belastung 250 A) oder NYY 4×120 mm²
- Hausanschluss: meist NAYY 4×35 mm²
- Überstromschutz: NH-Sicherungen in verschiedenen Größen
- Transformator-Bemessungsleistung typisch 630 kVA
- Bis zur Trennsäule: max. 20 Hausanschlüsse oder 40 Wohneinheiten
- Spannungsfall bis Hausanschlusskasten: Verantwortung des Netzbetreibers

NS-Anlagen kommen bis 1000 V AC bzw. 1500 V DC vor. Ausführungsformen: Strahlen-, Ring- und Maschennetze. Einspeisung über Verteilungstransformator oder Generator.
