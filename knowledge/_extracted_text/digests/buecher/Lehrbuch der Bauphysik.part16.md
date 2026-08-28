# Lehrbuch der Bauphysik — Teil 16
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 641-680.

Dieser Teil eröffnet Kapitel 22 „Bauakustik" (Autor: Gerrit Höfker, Hochschule Bochum) und behandelt vollständig die Schallübertragung durch Baukonstruktionen, Luftschallübertragung zwischen Räumen und von außen sowie den Beginn der Trittschallübertragung. Der Abschnitt deckt einschalige und zweischalige Bauteile, Massivbau und Holz-/Leichtbau, Türen, Fenster und schwimmende Estriche ab.

## Inhalt

### 22.1 Schallübertragung durch Baukonstruktionen — Grundgrößen

- Der **Transmissionsgrad τ** drückt das Verhältnis der vom Bauteil abgestrahlten Schallleistung P2 zur auftreffenden Leistung P1 aus.
- Das **Schalldämm-Maß R** ergibt sich logarithmisch: R = 10 · lg(P1/P2), Einheit dB.
- Luftschall regt Trennbauteile zu Schwingungen an → Körperschallausbreitung → erneute Luftschallabstrahlung.

#### 22.1.1 Einschalige Bauteile

- Eintreffende Luftschallwellen prägen plattenförmigen Wänden eine erzwungene **Spurwelle** (Biegewelle) auf; deren Wellenlänge hängt von Luftschallwellenlänge und Einfallswinkel ab.
- Freie Biegewellen in der Platte entstehen aus der **Biegesteifigkeit B′**:
  - B′ = E_dyn · d³ / [12 · (1 – μ²)]
  - Poisson-Querkontraktionszahl μ liegt üblicherweise zwischen 0,20 und 0,35.
- Die **Biegewellengeschwindigkeit** ist frequenzabhängig (über Eigenkreisfrequenz ω = 2πf) und hängt von flächenbezogener Masse m′ ab.
- Stimmen Wellenlänge der Spurwelle und freier Biegewelle überein → resonanzartige Amplitudenerhöhung → Transmissionsgrad steigt, Schalldämm-Maß sinkt.
- Die niedrigste Frequenz dieser Übereinstimmung heißt **Koinzidenzgrenzfrequenz fc**:
  - fc = (c² / 2π) · √(m′ / B′) = c² / (π · d) · √[ρ · 12 · (1 – μ²) / E_dyn]
  - Unterhalb fc: Biegewellenlängen kleiner als Luftschallwellenlänge; oberhalb umgekehrt.
- **Hydrodynamischer Kurzschluss**: bei sehr kleinen Biegewellenlängen (dünne Platten) gleichen sich Hoch- und Niederdruckgebiete direkt vor der Platte aus → verminderte Schallabstrahlung → bauakustisch vorteilhaft.

**Koinzidenzgrenzfrequenzen und innere Verlustfaktoren ausgewählter Platten** (Materialdaten aus DIN EN ISO 12354-1 Anhang B und Fasold/Veres):

| Plattenmaterial | ρ (kg/m³) | E_dyn (N/m²) | d (mm) | fc (Hz) | η_int |
|---|---|---|---|---|---|
| Stahlbeton | 2400 | 30 · 10⁹ | 200 | 86 | 0,006 |
| Ziegel | 1400 | 5 · 10⁹ | 240 | 135 | 0,01–0,04 |
| Ziegel | 1400 | 5 · 10⁹ | 115 | 281 | 0,01–0,04 |
| Leichtbeton | 700 | 1,5 · 10⁹ | 240 | 174 | 0,015 |
| Leichtbeton | 700 | 1,5 · 10⁹ | 115 | 363 | 0,015 |
| Kalksandstein | 2000 | 15 · 10⁹ | 240 | 93 | 0,03–0,06 |
| Kalksandstein | 2000 | 15 · 10⁹ | 115 | 194 | 0,03–0,06 |
| Zementestrich | 2200 | 30 · 10⁹ | 50 | 331 | 0,006 |
| Gipskarton | 900 | 3,2 · 10⁹ | 25 | 1296 | 0,03 |
| Gipskarton | 900 | 3,2 · 10⁹ | 12,5 | 2593 | 0,03 |
| Glas | 2500 | 60 · 10⁹ | 6 | 2079 | 0,0006–0,002 |
| Spanplatte | 800 | 2,5 · 10⁹ | 18 | 1921 | 0,01–0,03 |
| Stahlblech | 7800 | 200 · 10⁹ | 1 | 12069 | 0,00002–0,0003 |

**Massegesetz** (Berger, erweitert auf Winkelabhängigkeit):
- Unterhalb fc: Trennimpedanz Z_T = j·ω·m′ (nur Imaginäranteil relevant, Realteil vernachlässigbar).
- Das Schalldämm-Maß steigt je Oktave um 6 dB bei Frequenzverdopplung und um 6 dB bei Masseverdopplung; bei senkrechtem Einfall maximale Werte.
- Vereinfachtes Massegesetz für diffuse Schallfelder (Ersatzeinfallswinkel 45°):
  - R = 20 · lg(f · m′ / c) – 3 dB
- Oberhalb fc (nach Möser):
  - R = 20 · lg(f · m′ / c) + 10 · lg(η · f / fc)
  - Anstieg dann 7,5 dB/Oktave; Masseverdopplung weiterhin +6 dB.

**Gesamtverlustfaktor η_tot** (gemäß DIN EN ISO 12354-1:2017 Anhang C):
- Setzt sich zusammen aus: (1) innere Dämpfung η_int, (2) Abstrahlverluste über Abstrahlgrad σ, (3) Energieableitung in Baukörper über Stoßstellendämm-Maße K_ij und Körperschallabsorptionsgrad α_k.
- Körperschall-Nachhallzeit: T_s = 2,2 / (f · η_tot) in Sekunden.
- Hohlräume in Lochsteinen (z.B. Hochlochziegel) können Dickenresonanzen und damit schlechtere Schalldämmung bewirken; versetzt angeordnete Löcher und Stege bilden akustisch ungünstige Masse-Feder-Systeme.

#### 22.1.2 Zweischalige Bauteile

- Bei ausreichend großem Schalenabstand und ohne Nebenwege lassen sich Einzel-Schalldämm-Maße addieren.
- Bei geringem Schalenabstand wirkt die Luftschicht als Feder → **Masse-Feder-System** → Resonanzfrequenz f₀ mit reduzierter Schalldämmung.
- Resonanzfrequenz f₀ des Masse-Feder-Systems:
  - f₀ = (1/2π) · √[s′ · (1/m′₁ + 1/m′₂)]
  - In praxisüblichen Einheiten (s′ in MN/m³, m′ in kg/m²): f₀ = 160 · √[s′ · (1/m′₁ + 1/m′₂)]
- Für **freistehende Vorsatzkonstruktionen** mit Holzständer oder Blechprofilen, Hohlraum ≥ 70 % mit porösem Dämmstoff (Strömungswiderstand 5000–50000 Ns/m⁴) nach DIN 4109-34:2016:
  - f₀ = 160 · 0,80 / d · √[1/m′₁ + 1/m′₂], wobei d in m eingesetzt wird.
- Unterhalb f₀: Schalldämmung wie gleich schweres einschaliges Bauteil.
- Bei Resonanz f₀: Schalldämmung schlechter (Amplitude der angekoppelten Platte > direkt angeregte).
- Bei √2 · f₀: wieder wie einschaliges Bauteil.
- Oberhalb √2 · f₀: Verbesserung gegenüber einschalig mit +40 · lg(f/f₀) dB → Anstieg 18 dB/Oktave.
- Für bauakustische Anwendungen sollte f₀ deutlich unter 100 Hz liegen.
- Hohlraumresonanzen begrenzen bei hohen Frequenzen den tatsächlichen Gewinn gegenüber dem theoretischen Wert.

#### 22.1.3 Zusammengesetzte Bauteile

- Schallübertragung durch mehrere Bauteile (z.B. Wand und Fenster) gleichzeitig: resultierendes Schalldämm-Maß aus flächengewichtetem Mittel der Einzelwerte:
  - R_res = –10 · lg[Σ(Si / S_ges · 10^(–Ri/10))]
- Bauteile mit geringer Schalldämmung bestimmen aufgrund des logarithmischen Zusammenhangs das Gesamtergebnis maßgeblich.

### 22.2 Luftschallübertragung

#### 22.2.1 Luftschallübertragung zwischen Räumen — Übertragungswege und Bewertungsgrößen

**Übertragungswege** (bei Trennwand mit flankierenden Bauteilen):
- Weg **Dd**: direkte Übertragung Trennbauteil → Trennbauteil.
- Weg **Ff**: Flankenbauteil Senderaum → Flankenbauteil Empfangsraum.
- Weg **Fd**: Flankenbauteil Senderaum → Trennbauteil.
- Weg **Df**: Trennbauteil → Flankenbauteil Empfangsraum.
- Bei einer Trennwand mit je zwei flankierenden Wänden und Decken: insgesamt 13 Übertragungswege für Bau-Schalldämm-Maß R′.
- Kraftschlüssige Verbindung zwischen Trennwand und Flankenbauteil = günstig (weniger Flankenübertragung); gerissene Mörtelfugen = ungünstig (höhere Flankenübertragung durch niedriges Stoßstellendämm-Maß).
- Berechnung R′ frequenzabhängig in Oktaven von 125 Hz bis 4 kHz nach DIN EN ISO 12354-1:2017; Computerprogramme üblich.

**Bewertetes Schalldämm-Maß R_w** (Einzahlangabe nach DIN EN ISO 717-1:2021):
- Bezugskurve wird in 1-dB-Schritten gegen Messwertkurve verschoben bis Summe der ungünstigen Abweichungen (Messwert unter Bezugskurve) ≤ 32 dB, aber möglichst nahe daran.
- Einzahlwert = Bezugskurvenwert bei 500 Hz (ganzzahlig); Genauigkeit 0,1 dB möglich.
- Nur Unterschreitungen der Bezugskurve werden gewertet (keine Kompensation).

**Spektrum-Anpassungswerte C und C_tr** (nach DIN EN ISO 717-1:2021):
- C: für Wohnaktivitäten und mittel-/hochfrequente Geräusche (Spektrum 1).
- C_tr: für Stadtverkehr und nieder-/mittelfrequente Geräusche (Spektrum 2).
- Berechnung: frequenzabhängige Differenzen aus vorgegebenem Spektrum und Schalldämm-Maß energetisch addieren, logarithmieren, mit –10 multiplizieren, davon R_w abziehen.

**Bezugskurve und Spektren** (Werte nach DIN EN ISO 717-1:2021, Frequenzen in Hz):

| f (Hz) | Bezugswert R_w (dB) | Spektrum 1 (C) | Spektrum 2 (C_tr) |
|---|---|---|---|
| 100 | 33 | –29 | –20 |
| 125 | 36 | –26 | –20 |
| 160 | 39 | –23 | –18 |
| 200 | 42 | –21 | –16 |
| 250 | 45 | –19 | –15 |
| 315 | 48 | –17 | –14 |
| 400 | 51 | –15 | –13 |
| 500 | 52 | –13 | –12 |
| 630 | 53 | –12 | –11 |
| 800 | 54 | –11 | –9 |
| 1000 | 55 | –10 | –8 |
| 1250 | 56 | –9 | –9 |
| 1600 | 56 | –9 | –10 |
| 2000 | 56 | –9 | –11 |
| 2500 | 56 | –9 | –13 |
| 3150 | 56 | –9 | –15 |

**Schallpegeldifferenzen** (alternativ zu R′):
- **Norm-Schallpegeldifferenz D_n**: Korrektur über äquivalente Schallabsorptionsfläche A des Empfangsraums; Bezugsabsorptionsfläche A₀ = 10 m² für Wohnräume.
- **Standard-Schallpegeldifferenz D_nT**: Korrektur über Nachhallzeit T des Empfangsraums; Bezugsnachhallzeit T₀ = 0,5 s für Wohnräume.
- Umrechnung D_nT aus R′w mit Empfangsraumvolumen V_E:
  - D_nT = R′ + 10 · lg(V_E / (0,16 · S_S)) = R′ + 10 · lg(V_E / (0,32 · T₀ · S_S))

**Formel für Bau-Schalldämm-Maß** (vereinfachtes Verfahren nach DIN EN ISO 12354-1 / DIN 4109-2):
- R′_w = –10 · lg[10^(–R_Dd,w/10) + Σ(F/f_n · 10^(–R_Ff,w/10)) + Σ(F/f_n · 10^(–R_Fd,w/10)) + Σ(F/f_n · 10^(–R_Df,w/10))]

**Norm-Gliederung DIN 4109 (2016/2018):**
- DIN 4109-2:2018 — rechnerische Nachweise
- DIN 4109-31 bis 36:2016 — Bauteilkataloge (Massivbau, Holz-/Leicht-/Trockenbau, Vorsatzkonstruktionen, Elemente/Fenster/Türen/Vorhangfassaden, gebäudetechnische Anlagen)

#### 22.2.2 Luftschallübertragung im Massivbau

**Bewertetes Schalldämm-Maß für Massivbauteile** (DIN 4109-32:2016):

Für Beton, Kalksandstein, Mauerziegel, Verfüllsteine bei 65 kg/m² < m′_ges < 720 kg/m²:
- R_w = 30,9 · lg(m′_ges / m′₀) – 22,2 dB, mit m′₀ = 1 kg/m²

Für **Leichtbeton** bei 140 kg/m² < m′_ges < 480 kg/m²:
- R_w = 30,9 · lg(m′_ges / m′₀) – 20,2 dB

Für **Porenbeton** bei 50 kg/m² < m′_ges < 150 kg/m²:
- R_w = 32,6 · lg(m′_ges / m′₀) – 22,5 dB

Für **Porenbeton** bei 150 kg/m² < m′_ges < 300 kg/m²:
- R_w = 26,1 · lg(m′_ges / m′₀) – 8,4 dB

**Rohdichten für Flächenmassen-Ermittlung** (nach DIN 4109-32:2016):

| Konstruktion | Rohdichte |
|---|---|
| Mauerwerk Normalmörtel | ρ_w = 900 · RDK + 100 (2,2 ≥ RDK ≥ 0,35) |
| Mauerwerk Leichtmörtel | ρ_w = 900 · RDK + 50 (1,0 ≥ RDK ≥ 0,35) |
| Mauerwerk Dünnbettmörtel | ρ_w = 1000 · RDK – 100 (RDK > 1,0); –50 / –25 (RDK ≤ 1,0 je nach Klassenbreite) |
| Hohlblocksteine umgekehrt, Sand/Normalmörtel gefüllt | RDK + 0,4 |
| Füllsteine | ρ_w,res = ρ_Stein · V_Stege + ρ_Beton · V_Füll |
| Stahlbeton bewehrt verdichtet | 2400 kg/m³ |
| Stahlbeton unbewehrt verdichtet | 2350 kg/m³ |
| Aufbeton unbewehrt unverdichtet | 2100 kg/m³ |
| Zementestrich unbewehrt | 2000 kg/m³ |
| Gips- und Dünnlagenputze | 1000 kg/m³ |
| Kalk- und Kalkzementputze | 1600 kg/m³ |
| Leichtputze | 900 kg/m³ |
| Wärmedämmputze | 250 kg/m³ |

**Korrekturwert K_E** bei teilweise/vollständig entkoppelten Bauteilen (nach DIN 4109-32:2016):

| m′_ges (kg/m²) | Anzahl entkoppelter Kanten n | K_E (dB) |
|---|---|---|
| ≤ 150 | 2 ≤ n ≤ 3 | 2 |
| ≤ 150 | 4 | 4 |
| > 150 | 2 ≤ n ≤ 3 | 3 |
| > 150 | 4 | 6 |

**Verbesserungsmaß ΔR_w durch Vorsatzkonstruktionen** (nach DIN 4109-34:2016, abhängig von Resonanzfrequenz f₀):

| f₀ (Hz) | ΔR_w (dB) |
|---|---|
| 30 ≤ f₀ ≤ 160 | max(0; 74,4 – 20 · lg f₀ – 0,5 · R_w) |
| 200 | –1 |
| 250 | –3 |
| 315 | –5 |
| 400 | –7 |
| 500 | –9 |
| 630 ≤ f₀ ≤ 1600 | –10 |
| 1600 < f₀ ≤ 5000 | –5 |

- Vorsatzkonstruktionen beidseitig an Trennbauteil: Verbesserung der besseren Seite voll + halbe Verbesserung der anderen Seite; bei negativen Verbesserungen beide halbiert addiert.

**Flankenschalldämm-Maße** für Wege Ff, Fd, Df werden aus Einzelschalldämm-Maßen der beteiligten Bauteile plus Stoßstellendämm-Maß K_ij sowie Geometriekorrektur (Trennbauteilfläche S_S, Kopplungslänge l_f, Bezugskopplungslänge l₀ = 1 m) ermittelt (DIN 4109-32:2016).

**Stoßstellendämm-Maße K_ij** in Abhängigkeit des logarithmischen Masseverhältnisses M_i = lg(m′_i / m′_j):
- Dickenwechsel: K_12 = 5 – M²/5
- Eckstoß: K_12 = 2,7 – M²/2,7
- Kreuzstoß gerader Durchgang: K_13 = 8,7 – M²/17,1 + 0,182 (für M ≤ 5,7)
- Kreuzstoß gerader Durchgang (alt.): K_13 = 9,6 – M²/11 · 0,182 (für M > 0)
- Kreuzstoß Ecke: K_12 = 5,7 – M²/15,4
- T-Stoß gerader Durchgang: K_13 = 5,7 – M²/14,1 + 0,215 (für M ≤ 5,7)
- T-Stoß gerader Durchgang (alt.): K_13 = 8 – M²/6,8 · 0,215 (für M > 0)
- T-Stoß Ecke: K_12 = 4,7 – M²/5,7
- Mindestwert K_ij,min: K_ij,min = 10 · lg(l_f / l₀) – 10 · lg(√(S_i · S_j))

**Elastische Entkopplung** (Steifigkeitsbereich 20 MN/m² ≤ E/t ≤ 200 MN/m²):
- K_ij,E = K_ij (starr) + ΔK_ij, wobei ΔK_ij = 36 – 15 · lg(E/t)

**Besonderheiten Mauerwerk aus Lochsteinen**: Schalldämmung durch Labormessung zu ermitteln; Laborwerte auf massivbautypischen Bauverlustfaktor η_Bau,ref korrigieren → Prüfberichte geben R_w,Bau,ref an.

**Zweischalige Haustrennwände** (Berechnungsverfahren nach DIN 4109 BB1:1989 mit Modifikationen, da keine geeigneten Daten nach DIN 4109-2:2018 für unvollständig getrennte Schalen):
- Gilt für Trennfugendicke d ≥ 30 mm.
- Basis-Schalldämm-Maß aus Gesamtflächenmasse beider Schalen m′_Tr,ges: R_w,l = 28 · lg(m′_Tr,ges) – 18
- Endwert: R′_w,2 = R_w,l + ΔR_w,Tr + K
- ΔR_w,Tr aus Tabelle abhängig von Trennungssituation.
- Korrekturwert K (nur für Zeile 1 Tab. 22.7, wenn m′_Tr,l < m′_f,m): K = 0,6 · lg(m′_Tr,l / m′_f,m) – 5,5
- Ab Trennfugendicke d ≥ 50 mm: ΔR_w,Tr um 2 dB höher als Tabellenwert.

**Zweischaligkeitszuschläge ΔR_w,Tr** (nach DIN 4109-2:2018, Trennfuge d ≥ 30 mm):

| Übertragungssituation | ΔR_w,Tr (dB) |
|---|---|
| Schalen + flankierende Bauteile ab OK Bodenplatte getrennt (EG, unterkellert) | 12 |
| Durchgehende Außenwände (EG, unterkellert) | 9 |
| Durchgehende Außenwände (KG) | 3 |
| Schalen + Außenwände + Bodenplatte getrennt (EG, nicht unterkellert) | 9 |
| Schalen + Außenwände getrennt, Bodenplatte getrennt auf gemeinsamem Fundament (EG, nicht unterkellert) | 6 |
| Schalen + Außenwände getrennt, Bodenplatte durchgehend m′ ≥ 575 kg/m² (EG, nicht unterkellert) | 6 |

**Berechnungsbeispiel: Vertikale Luftschallübertragung Massivbau** (Tab. 22.6, nach DIN 4109-2:2018):
- Decke: 180 mm Stahlbetondecke (ρ = 2400 kg/m³) mit 45 mm Zementestrich auf Dämmung (s′ = 10 MN/m³).
- Flanke 1 (Außenwand): 175 mm Kalksandstein (ρ_w = 1700 kg/m³) innen verputzt, außen WDVS.
- Flanke 2 + 3 (Innenwände): je 115 mm Kalksandstein (ρ = 1700 kg/m³) beidseitig verputzt.
- Flanke 4 (Wohnungstrennwand): 240 mm Kalksandstein (ρ = 1700 kg/m³) beidseitig verputzt.
- Raumhöhe 2,5 m; Trennbauteilfläche S_S = 14,2 m².
- Rohdecke flächenbezogene Masse m′ = 432 kg/m².
- Direkt-Schalldämm-Maß Rohdecke R_s,w = 59,2 dB.
- Resonanzfrequenz Vorsatzkonstruktion f₀ = 58,6 Hz → Verbesserung ΔR_Dd,w = 9,4 dB → R_Dd,w = 68,6 dB.
- Flanken-Kopplungslängen: Flanke 1 = 4,65 m, Flanke 2 = 3,05 m, Flanke 3 = 4,65 m, Flanke 4 = 3,05 m.
- Flächenbezogene Massen Flanken: F1 = 308 kg/m², F2 = 216 kg/m², F3 = 216 kg/m², F4 = 428 kg/m².
- Direktschalldämm-Maße R_w Flanken: F1 = 54,7 dB, F2 = 49,9 dB, F3 = 49,9 dB, F4 = 59,1 dB.
- Verbesserung ΔR_Df,w durch Vorsatzkonstruktion: 9,4 dB für alle Flanken.
- Stoßstellentypen: F1 = T-Stoß starr, F2–F4 = Kreuzstoß starr.
- Stoßstellendämm-Maß K_Ff: F1 = 7,9 dB, F2 = 12,9 dB, F3 = 12,9 dB, F4 = 8,8 dB.
- Stoßstellendämm-Maß K_Fd: F1 = 4,8 dB, F2 = 7,1 dB, F3 = 7,1 dB, F4 = 5,7 dB.
- Stoßstellendämm-Maß K_Df: F1 = 4,8 dB, F2 = 7,1 dB, F3 = 7,1 dB, F4 = 5,7 dB.
- Flankenschalldämm-Maß R_Ff,w: F1 = 67,4 dB, F2 = 69,5 dB, F3 = 67,7 dB, F4 = 74,6 dB.
- Flankenschalldämm-Maß R_Fd,w: F1 = 66,6 dB, F2 = 68,3 dB, F3 = 66,5 dB, F4 = 71,5 dB.
- Flankenschalldämm-Maß R_Df,w: F1 = 76,0 dB, F2 = 77,8 dB, F3 = 75,9 dB, F4 = 81,0 dB.
- Bau-Schalldämm-Maß R′_w = 58,6 dB.
- Standard-Schallpegeldifferenz D_nT,w = 57,7 dB.
- Sicherheitsbeiwert u_prog = 2 dB → Vergleichswert R′_w – u_prog = 56,6 dB.

**Berechnungsbeispiel: Horizontale Luftschallübertragung Reihenhaustrennwand** (Tab. 22.8):
- Zweischalige Haustrennwand (nicht unterkellert): 2 × 175 mm Kalksandstein (ρ_w = 1700 kg/m³) verputzt, 50 mm Trennfuge vollflächig mit Mineralfaserdämmung.
- Flanken alle mit Trennung im Bereich der Haustrennwand; Flanke 4 (Bodenplatte): 300 mm Stahlbeton mit schwimmendem Estrich und Fundamenttrennung.
- S_S = 10,1 m²; m′₁ = m′₂ = 308 kg/m².
- R_w,1 (aus Flächenmasse) = 60,1 dB; Fugenbreite 50 mm.
- Mittlere flächenbezogene Masse Flanken m′_f,m = 352 kg/m²; Korrekturwert K = 0 dB.
- Zweischaligkeitszuschlag ΔR_w,Tr = 11 dB (Trennung der Schalen + Außenwände + Bodenplatte, nicht unterkellert + Fugenbreite ≥ 50 mm → 9+2).
- R′_w,2 = 71,1 dB; D_nT,w = 71,8 dB; u_prog = 2 dB → Vergleichswert = 69,1 dB.

#### 22.2.3 Luftschallübertragung im Holz-/Leicht- und Trockenbau

- Holz-/Leicht- und Trockenbau umfasst: lasttragenden Stützen, Trockenbaukonstruktionen für Innenausbau, leichte nicht tragende Fassaden, Holzrahmen- und Holztafelbauweise.
- Keine Biegesteifverbindung zwischen Bauteilen → nur Direktweg Dd und Flankenweg Ff relevant.
- Berechnung nicht direkt aus Konstruktionszeichnungen möglich (zu viele Einflussgrößen).
- Rückgriff auf Messwerte aus Prüfständen (DIN 4109-33:2016 oder eigene Prüfberichte); Messwerte an Bausituation anpassen.
- Faustformel Abschätzung: Bauteile mit R_w bzw. D_n,f,w jeweils ≥ 5 dB über Ziel-R′_w wählen.
- Genaue Berechnung: R′_w aus Direkt-R_Dd,w plus Flanken-R_Ff,w.
- Flankenschalldämm-Maß R_Ff,w aus Norm-Flankenschallpegeldifferenz D_n,f,w adaptiert mit tatsächlicher Geometrie: R_Ff,w = D_n,f,w + 10 · lg(l_f / l₀) – 10 · lg(l_lab / l₀) – 10 · lg(A_lab / A₀)
- Bezugsgrößen nach DIN 4109-2:2018: A₀ = 10 m²; l_lab = 4,5 m (Decken/Böden), 2,8 m (Wände).
- Bei Räumen ohne gemeinsame Trennfläche (diagonal): bewertete Norm-Schallpegeldifferenz D_w aus allen Flanken.
- Skelettbau mit Pfosten-Riegel-Fassade: Pfostenbreite ca. 50 mm < Trennwandbreite 75–125 mm → **Fassadenanschlussschwerter** erforderlich; schwere Platten und ggf. Bleche/Schwerfolien einbauen.
- Metallständerwand unterbrochen durch Massivbauteil ≥ 350 kg/m²: D_n,f,w = 76 dB annehmbar.
- Trennung über Holzbalken- oder Massivholzdecke: D_n,f,w = 67 dB ansetzen.

**Tab. 22.10 — Bewertete Schalldämm-Maße R_w für Innenwände** (nach DIN 4109-33:2016):

| Aufbau (innen → außen) | R_w (dB) |
|---|---|
| 12,5 mm GK / 40 mm MW / 60 mm Holzständer / 12,5 mm GK | 38 |
| 2×12,5 mm GK / 40 mm MW / 60 mm Holzständer / 2×12,5 mm GK | 43 |
| 12,5 mm GK / 40 mm MW / 50 mm Metallständer / 12,5 mm GK | 41 |
| 2×12,5 mm GK / 60 mm MW / 75 mm Metallständer / 2×12,5 mm GK | 51 |
| 2×12,5 mm GK schwer / 2×40 mm MW / 2×50 mm Metallständer getrennt / 2×12,5 mm GK schwer | 60 |

**Tab. 22.11 — Bewertete Norm-Flankenschallpegeldifferenz D_n,f,w für Metallständerwände** (DIN 4109-33:2016):

| Aufbau | D_n,f,w (dB) |
|---|---|
| 12,5 mm GK innen / MW / 50 mm Metallständer | 53 |
| Mit 2×12,5 mm GK | 56 |
| 12,5 mm Beplankung durch Fuge getrennt | 57 |
| 2×12,5 mm Beplankung durch Fuge getrennt | 60 |
| 12,5 mm GK innen / MW / 100 mm Metallständer | 65 |

**Tab. 22.12 — Norm-Flankenschallpegeldifferenz D_n,f,w schwimmende Estriche** (DIN 4109-33:2016):

| Konstruktion | D_n,f,w (dB) |
|---|---|
| Einfach-/Doppelständerwand (Holz/Metall) auf durchlaufendem schwimmendem Estrich (Zement oder Calciumsulfat) | 40 |
| Einfach-/Doppelständerwand auf schwimmendem Estrich mit Trennfuge unter der Wand | 57 |
| Einfach-/Doppelständerwand auf schwimmendem Estrich mit Trennfuge seitlich der Wand | < 57 |
| Estrich konstruktiv getrennt auf Massivdecken | nach DIN 4109-2:2016 |
| Auf Holzbalkendecken | 67 dB (DIN 4109-BB1:1989 + 2 dB) |
| Wand auf Hohlraumboden / mit Trennfuge | abhängig von Schallübertragung in Hohlraum |

**Tab. 22.13 — D_n,f,w von Unterdecken unter Massivdecken** (DIN 4109-33:2016):

| Konstruktion | D_n,f,w (dB) |
|---|---|
| Trennwand an Unterdecke GK einlagig, 40 mm MW, durchlaufend ohne Fuge | 49 |
| Trennwand an Unterdecke GK einlagig, 40 mm MW, Fugenschnitt ≥ 3 mm im Trennwandbereich | 54 |
| Trennwand an Unterdecke GK zweilagig, 40 mm MW, Trennung in Trennwanddicke | 59 |
| Trennwandanschluss an Massivdecke, Unterdecke GK zweilagig, 40 mm MW | 65 |

**Berechnungsbeispiel: Horizontale Luftschallübertragung Holz-/Leichtbau** (Tab. 22.9):
- Trennwand: 75 mm Metallständer, 60 mm Dämmstoff, beidseitig doppellagig 12,5 mm GK.
- Flanke 1 (Außenwand): Holztafelwand mit Vorsatzschale, Vorsatzschale durch Trennwand unterbrochen.
- Flanke 2 (Innenwand): 50 mm Metallständer, 40 mm Dämmstoff, doppellagig beplankt, durchgehende Fuge an Innenbeplankung.
- Flanke 3 (Decke): Holzbalkendecke mit biegeweicher Unterdecke, Fuge im Trennwandanschluss.
- Flanke 4 (Boden): Holzbalkendecke mit schwimmendem Estrich, durch Trennwand unterbrochen.
- Raumtiefe Empfangsraum 6,25 m; S_S = 12,5 m².
- R_Dd,w = 51,0 dB.
- Kopplungslängen: Flanke 1+2 je 2,50 m (l_lab 2,80 m); Flanke 3+4 je 5,00 m (l_lab 4,50 m).
- D_n,f,w: F1 = 68,0 dB, F2 = 60,0 dB, F3 = 54,0 dB, F4 = 67,0 dB.
- R_Ff,w: F1 = 69,5 dB, F2 = 61,5 dB, F3 = 54,5 dB, F4 = 67,5 dB.
- R′_w = 49,0 dB; D_nT,w = 48,1 dB; u_prog = 2 dB → Vergleichswert = 47,0 dB.

#### 22.2.4 Luftschallübertragung von Außenlärm

- Bei Außenwänden und Fassaden: keine beidseitig diffusen Schallfelder → Schalldämmung hängt von Einfallswinkel ab.
- Bau-Schalldämm-Maß Fassade nach DIN EN ISO 12354-3:2017: R′ = R′_45° + 1 dB (Einfallswinkel ϑ = 45°).
- Bei Verkehrslärm als Hauptquelle: R′_tr,s = R′_w (mit Spektrum-Anpassungswert C_tr).
- Berechnung nach DIN 4109-2:2018: diffuser Schalleinfall angenommen; Gesamtfassade aus Einzelelementen (Wand, Fenster, Rolladenkästen, Einbauelemente) + Flanken.
- Flankenübertragung nur zu berücksichtigen, wenn R_w (Außenbauteil) ≥ 50 dB UND R′_w,ges ≥ 40 dB.
- Für Fassadenelemente mit Norm-Schallpegeldifferenz D_n,e,w: R_e,i,w = D_n,e,w + 10 · lg(S_i / A₀).
- Auf Fassadenfläche bezogenes Schalldämm-Maß Einzelbauteil: R_e,i,w = R_i,w + 10 · lg(S_i / S_s).
- **Fugen** (z.B. Bauanschlussfugen Fenster): über bewertetes Fugenschalldämm-Maß R_s,w,k berücksichtigt (bezogen auf 1 m² Fläche und 1 m Fugenlänge). Regelung: Fugenschalldämm-Maß muss mindestens 10 dB über Schalldämm-Maß des Einbauteils liegen.
- **Lüftungsöffnungen**: bei niedrigen Anforderungen problemlos integrierbar; bei höheren Anforderungen schallgedämmte Öffnungen mit Absorptionsschalldämpfern; bei sehr hohen Anforderungen nur zentrale RLT-Anlage.
- Öffenbare Fenster mit Innenpegelanforderungen: Spaltbegrenzungen + schallabsorbierende Laibungen kombinieren (Anhaltswerte z.B. Hamburger Leitfaden Lärm).
- Dachkonstruktionen: Messwerte aus Prüfständen erforderlich.

**Tab. 22.15 — Schalldämmung von Dachkonstruktionen** (nach DIN 4109-33:2016):

| Aufbau | R_w (C; C_tr) |
|---|---|
| Dach Zwischensparrendämmung: Dachsteine / Lattung / Folie / 120–180 mm MW zwischen Sparren (≥600 mm) / Folie / Lattung / 12,5 mm GK | 50 (–3; –9) dB |
| Dach Zwischensparrendämmung: Biberschwanz Doppeldeckung / ≥200 mm MW / Folie / MW zwischen Lattung / 2×12,5 mm GF | 59 (–4; –11) dB |
| Dach Aufsparrendämmung: ≥100 mm Hartschaum (EPS/XPS/PUR) / Folie / ≥19 mm Holzwerkstoffplatte / sichtbare Sparren | 34 (–2; –6) dB |
| Dach Aufsparrendämmung mit Beschwerungslage m′ ≥ 20 kg/m²: Biberschwanz Doppeldeckung / ≥100 mm Hartschaum / Folie / ≥19 mm Holzwerkstoffplatte / sichtbare Sparren | 40 (–2; –7) dB |
| Stahltrapezblechdach (1,0 mm Stahlblech) | 25 dB |
| Stahltrapezblechdach (0,75 mm Stahlblech + 100 mm Mineralfaser) | 40 dB |
| Stahltrapezblechdach (0,75 mm außen + 0,88 mm Lochblech 28% innen + 100 mm Mineralfaser) | 34 dB |

**Berechnungsbeispiel: Fassade** (Tab. 22.14):
- Außenwand 365 mm Ziegel mit integrierter Dämmfüllung, beidseitig verputzt (R_w,Bau,ref = 51,9 dB).
- Fenster R_w = 35 dB; Fugenschalldämm-Maß mindestens 10 dB über Fenster.
- Rolladenkasten D_n,e,w = 50 dB.
- Flankenübertragung vernachlässigbar; Raumtiefe 3,1 m; S_S = 11,6 m².
- Flächen: Außenwand 7,5 m², Fenster 3,4 m².
- Auf Fassadenfläche bezogenes Schalldämm-Maß: Außenwand R_e,w = 49,8 dB, Fenster 40,3 dB, Rolladenkasten 50,7 dB.
- Gesamt R′_w,ges = 39,5 dB; D_nT,w,ges = 39,4 dB; u_prog = 2 dB → Vergleichswert = 37,5 dB.

#### 22.2.5 Schalldämmung von Türen

- Anforderungen je nach Einsatzbereich variabel; Konstruktionsmerkmale betreffen Türblatt, Türzarge, Anschluss an Baukörper, Anzahl und Art der Dichtungen, Bodendichtung.
- Flächenbezogene Masse m′ des Türblatts maßgebend für erreichbares R.
- Koinzidenzgrenzfrequenz fc liegt bei üblichen Türblattdicken in ungünstigem Frequenzbereich → schlechte Einzelschalldämmung.
- Verbesserung: Schichten mehrerer dünner Platten (hohe fc) mit nur punktueller Verbindung (Biegesteifigkeit nicht erhöhen).
- Alternative: mehrschalige Türblätter (Holz oder Stahl mit Mineralwollefüllung) → Resonanzfrequenzeinbruch beachten.
- Zentrale Bedeutung der **Dichtungen**: Mehrfachverriegelung, automatisch absenkende Bodendichtungen oder Schleppdichtungen mit Höckerschwelle.
- Schwimmende Estriche/Hohlraumböden unter Tür trennen; Bodendichtung nicht auf Teppich absenken (Flankenübertragung über Estrich begrenzt erreichbares R).
- Zarge als Schallnebenweg: Stahlzargen vermörteln; Holzzargen mit Mineralwolle hinterfüllen und beidseitig dauerelastisch verfugen. Aushärtende Montageschäume ungeeignet.
- Sicherheitsbeiwert nach DIN 4109-2:2016: u_prog = 5 dB für Türen.
- Doppeltüren mit großem Gegenseitigem Abstand: hohe Schalldämmung durch niedrige Resonanzfrequenz des Luftraums; Laibung zusätzlich schallabsorbierend verkleiden sinnvoll.

**Tab. 22.16 — Konstruktionsmerkmale Türen mit Schallschutzanforderungen** (nach Sälzer et al.):

| Erf. R_w (Bau) | Labor-R_w Türblatt | Zargenanforderungen | Dichtungsebenen | Bodendichtung | Sonstiges |
|---|---|---|---|---|---|
| 30 dB | 37 dB | Holzzarge beids. gedichtet + MW, oder Stahlzarge vermörtelt | 1 | 1 Absenkdichtung | normale Bänder |
| 35 dB | 42 dB | Holzzarge beschwert + MW, oder Stahlzarge hohe Masse, vermörtelt | 2 | 1 Absenkdichtung | starke Bänder |
| 40 dB | 47 dB | wie 35 dB | 2 | 1 Absenkdichtung | starke Bänder; individuelle Einmessung + Feinjustierung |
| ≥ 40 dB | – | Spezialtüren oder Doppeltüren | – | – | individuelle Einmessung |

#### 22.2.6 Schalldämmung von Fenstern

**Fensterkonstruktionsarten:**
- Einfachverglasung: Innenbereich; flächenbezogene Masse m′ maßgebend; bei zu dicken Scheiben Koinzidenzeinbruch. Verbundsicherheitsgläser (Laminat aus mehreren Gläsern + Folie) erhöhen innere Dämpfung → bauakustisch positiv.
- **Zweifachverglasung**: Masse-Feder-System; Resonanzfrequenzeinbruch durch vergleichsweise geringe Scheibendicken und kleinen Zwischenraum deutlich im relevanten Frequenzbereich. Optimierungsmaßnahmen:
  - Möglichst großer Scheibenabstand (niedrigere f₀) — jedoch Wärmedurchgang U verschlechtert sich.
  - Unterschiedliche Scheibendicken verwenden (Koinzidenzfrequenzen der Scheiben nicht überlagern).
  - Bedämpfung durch PVB-Folien oder Gießharz (Verbundglas 2×4 mm Float + PVB → R_w ≈ 38 dB); Temperaturabhängigkeit beachten.
- **Dreifachverglasung**: drei Scheiben + zwei Luftschichten → mehrere Resonanzfrequenzen; bei ungünstigem Zusammenfallen schlechtere Schalldämmung als Zweifach; Optimierung durch unterschiedliche Scheibendicken und -abstände.
- **Kastenfenster**: zwei separate Fenster in großem Abstand eingebaut; für sehr hohe Anforderungen (z.B. Rundfunkstudios) geeignet.
- Weitere Einflüsse auf Schalldämmung: Rahmenart, Anzahl Dichtungsebenen und Verriegelungspunkte, Bauanschlussfugenausführung (schallabsorbierendes Material zwischen Luft- und Windschutzfolie; Montageschäume mit hoher Steifigkeit ungeeignet).

**Berechnung R_w,Fenster** nach DIN 4109-35:2016:
- R_w,Fenster = R_w,Glas + K_AH + K_RA + K_S + K_FV + K_F,1.5 + K_F,3 + K_Sp
  - K_AH: Korrektur Aluminium-Holzfenster
  - K_RA: Korrektur Rahmenanteil > 30 %
  - K_S: Korrektur zweiflügelig ohne Mittelpfosten
  - K_FV: Korrektur Festverglasung mit erhöhtem Scheibenanteil
  - K_F,1.5: Korrektur Fensterfläche < 1,5 m²
  - K_F,3: Korrektur Fensterfläche > 3 m² (= –2 dB)
  - K_Sp: Korrektur glasteilende Sprossen

**Tab. 22.17 — Schalldämm-Maße von Fenstern** (DIN 4109-35:2016):

| Ziel-R_w | Glasaufbau | Scheibenabstand | Dichtungen | Korrekturen |
|---|---|---|---|---|
| 30 dB | Gesamtglasdicke ≥ 6 mm, R_w,Glas ≥ 30 dB | ≥ 12 mm | 1 umlaufend | – |
| 35 dB | Aufbau ≥ 6 mm + 4 mm, R_w,Glas ≥ 32 dB | ≥ 12 mm | 1 umlaufend | K_BA = –2 dB, K_FV = –1 dB |
| 40 dB | R_w,P,Glas ≥ 40 dB | – | 2 umlaufend | K_BA = –2 dB, K_F,1.5 = –1 dB, K_Sp = –1 dB |
| 45 dB | R_w,P,Glas ≥ 51 dB | – | 2 umlaufend | K_RA = 0, K_S = –2 dB, K_fv = +1 dB, K_F,1.5 = –1 dB, K_Sp = –2 dB |

**Schallschutzklassen für Fenster** nach VDI 2719:1987 (Klassenbreite 5 dB):

| Schallschutzklasse | R_w,R am Bau (dB) | R_w,P im Labor (dB) |
|---|---|---|
| 1 | 25–29 | ≥ 27 |
| 2 | 30–34 | ≥ 32 |
| 3 | 35–39 | ≥ 37 |
| 4 | 40–44 | ≥ 42 |
| 5 | 45–49 | ≥ 47 |
| 6 | ≥ 50 | ≥ 52 |

### 22.3 Trittschallübertragung

#### 22.3.1 Trittschallübertragung in Räumen — Grundprinzipien

- Beim Begehen einer Decke entsteht impulsartige Anregung im gesamten Frequenzbereich.
- Jede Rohdecke (Massivbeton oder Holzbalken) bietet für sich unzureichenden Trittschallschutz.
- Ergänzender Deckenaufbau zwingend: schwimmender Estrich oder weichfedernder Bodenbelag.
- **Schwimmender Estrich** = Standardlösung; Nutzer kann Bodenbelag frei wählen.
- Estrich muss tatsächlich frei schwimmen auf elastischer Zwischenschicht; kleinste Schallbrücken führen zu deutlich erhöhten Pegeln im Empfangsraum.
- Resonanzfrequenz f₀ des schwimmenden Estrichs (Masse-Feder-System): für ausreichenden Trittschallschutz im Wohnungsbau angestrebter Bereich ca. 70 Hz.
- Verbesserung der Trittschalldämmung setzt ab √2 · f₀ ein.
- Messgröße: **Norm-Trittschallhammerwerk** (genormte Schallquelle); Norm-Trittschallpegel liegt weit über realem Gehhschallpegel → Vergleichbarkeit der Konstruktionen.
- Berechnungsfrequenzbereich: 125 Hz bis 4 kHz in Oktaven; Detail nach DIN EN ISO 12354-2:2017.

**Bewerteter Norm-Trittschallpegel L′n,w** (Einzahlangabe nach DIN EN ISO 717-2:2021):
- Bezugskurve in 1-dB-Schritten verschoben bis Summe der ungünstigen Abweichungen (Messwert über Bezugskurve) ≤ 32 dB; Einzahlwert = Bezugskurvenwert bei 500 Hz; Genauigkeit 0,1 dB möglich.
- Nur Überschreitungen der Bezugskurve gewertet; keine Kompensation.
- Spektrum-Anpassungswert C_I: frequenzabhängige Norm-Trittschallpegel energetisch addieren, runden → minus 15 dB, minus L′n,w.

**Bezugskurve Trittschall** (nach DIN EN ISO 717-2:2021):

| f (Hz) | Bezugswert L_n,w (dB) | f (Hz) | Bezugswert L_n,w (dB) |
|---|---|---|---|
| 100 | 62 | 630 | 59 |
| 125 | 62 | 800 | 58 |
| 160 | 62 | 1000 | 57 |
| 200 | 62 | 1250 | 54 |
| 250 | 62 | 1600 | 51 |
| 315 | 62 | 2000 | 48 |
| 400 | 61 | 2500 | 45 |
| 500 | 60 | 3150 | 42 |

**Norm-Schallpegeldifferenzen Trittschall:**
- **Norm-Trittschallpegel L′n**: bezogen auf äquivalente Schallabsorptionsfläche A des Empfangsraums (A₀ = 10 m²).
- **Standard-Trittschallpegel L′nT**: bezogen auf Nachhallzeit T (T₀ = 0,5 s).
- Umrechnung: L′nT = L′n + 10 · lg(A / A₀) + 10 · lg(T / T₀) (vereinfacht aus Raumvolumen V_E).

#### 22.3.2 Trittschallübertragung von Massivdecken

Berechnung bewerteter Norm-Trittschallpegel L′n,w nach DIN 4109-2:2018:

- Übereinanderliegende Räume: L′n,w = L_n,eq,0,w – ΔL_w + K
  - L_n,eq,0,w = äquivalenter bewerteter Norm-Trittschallpegel der Rohdecke
  - ΔL_w = Trittschallminderung der Deckenauflage
  - K = Korrekturwert für Flankenübertragung im Empfangsraum

- Nicht übereinanderliegende Räume: L′n,w = L_n,eq,0,w – ΔL_w + K_T
  - K_T = Korrekturwert für abweichende Übertragungssituation (Tab. 22.20)
