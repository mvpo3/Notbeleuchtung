# Grundladen der elektrischen Energietechnik — Teil 2
> Quelle: Grundladen der elektrischen Energietechnik (buecher) · Seiten 81-120.

Dieser Teil des Lehrbuches schließt das Kapitel zum magnetischen Kreis ab und behandelt anschließend ausführlich den einphasigen Wechselstrom (Kenngrößen, Verbraucher, Leistung, Verluste, Oberschwingungen) sowie den Einstieg in die Drehstromtechnik (Leitungen, Spannungsebenen, Verbraucheranschluss).

## Inhalt

### 1.3 Magnetischer Kreis — Abschluss (Seite 81–82)

- Für eine Ringkernspule mit mittlerem Radius r ≫ Windungsdurchmesser d ist das Feld im Querschnitt A weitgehend homogen → magnetischer Fluss Φ = B · A.
- Zusammenhang Durchflutung Θ und Fluss Φ: Θ = (l / (µ · A)) · Φ, also Θ proportional Φ — das wird als Ohmsches Gesetz des magnetischen Kreises oder Hopkinsonsches Gesetz bezeichnet.
- Magnetischer Widerstand Rm: Θ = Rm · Φ; Einheit [Rm] = A/(Vs) = H⁻¹.
- Magnetischer Leitwert Λm = 1/Rm; Einheit [Λm] = Vs/A = H.
- Zusammenhang mit Induktivität: L = N² / Rm = N² · Λm.
- Ringkernspule: Rm = l / (µ · A) — formal identisch mit dem Widerstandsausdruck für einen langen dünnen Leiter im Gleichstromkreis.
- Ersatzschaltung: Die Durchflutung Θ (= magnetische Spannung) treibt Fluss Φ durch Rm. Kirchhoffsche Regeln und Knotenpotenzialverfahren sind für magnetische Kreise anwendbar, aber bei Eisenkern wegen der nichtlinearen Kennlinie sind die magnetischen Widerstände nicht konstant → Vorsicht.

---

### 1.4 Wechselstrom (Seiten 82–113)

#### 1.4.1 Wechselspannung — Kenngrößen und Darstellung (Seiten 82–85)

**Zeitbereich**

- Wechselspannung entsteht durch gleichförmige Drehbewegung der Synchrongeneratoren → sinusförmiger Verlauf: u(t) = û · sin(ωt + φu).
- Begriffsklärung:
  - u(t): Augenblickswert (Momentanwert), Einheit V
  - û: Amplitude (auch Maximalwert, Scheitelwert, Spitzenwert), Einheit V
  - ωt + φu: Phasenwinkel (Phase), dimensionslos (rad)
  - ω = 2πf: Kreisfrequenz, Einheit s⁻¹
  - f: Frequenz, Einheit Hz
  - T = 1/f: Periodendauer, Einheit s
  - φu: Nullphasenwinkel der Spannung, Einheit rad
- Bei f = 50 Hz beträgt die Periodendauer T = 20 ms.
- Darstellung als Liniendiagramm (über t oder über ωt) mittels Oszillograf.
- Arithmetischer Mittelwert über eine Periode = null → deshalb wird der Effektivwert eingeführt.
- **Effektivwert** Ieff: Wechselstrom, der im ohmschen Widerstand im zeitlichen Mittel gleiche Wärmeverluste wie ein Gleichstrom erzeugt.
  - Definition: Ieff = √(1/T · ∫₀ᵀ i²(t) dt) — quadratischer Mittelwert (RMS).
  - Mittlere Leistung: P = R · Ieff².
  - Effektivwert Spannung analog: Ueff = √(1/T · ∫₀ᵀ u²(t) dt).
  - Für sinusförmige Größen gilt: Ueff = û / √2.
  - Netzspannung an der Steckdose: Effektivwert 230 V → Amplitude û = √2 · 230 V ≈ 325 V.
  - Internationales Kürzel: RMS (Root Mean Square).
  - Im weiteren Text wird der Index „eff" weggelassen, da keine Verwechslungsgefahr mit Gleichstromgrößen besteht.

**Bildbereich (komplexe Zeiger)**

- Harmonische Schwingung = Projektion einer gleichförmigen Kreisbewegung auf die imaginäre Achse: u(t) = Im(û · e^(jωt) · e^(jφu)).
- Im stationären Zustand (konstante Frequenz, Amplituden, Nullphasenwinkel) wird die Drehbewegung bei t = 0 eingefroren → ruhender Zeiger in der komplexen Ebene.
- Aus Amplitudenzeigern werden Effektivwertzeiger: U = U · e^(jφu), I = I · e^(jφi).
- Versorzahldarstellung: e^(jα) wird mit ∠α notiert; Beispiel: U = 12 V · e^(j38°) = 12 V ∠38°.
- Rechenvorteile komplexer Darstellung: Differenzialgleichungen werden zu algebraischen Gleichungen.

---

#### 1.4.2 Wechselstromverbraucher — komplexe Widerstände (Seiten 85–94)

**Phasendifferenz**

- Nach Abklingen von Einschaltvorgängen fließt stationärer Wechselstrom i(t) durch den Verbraucher; Strom und Spannung können unterschiedliche Nullphasenwinkel φi und φu haben.
- Phasenverschiebungswinkel (Phasendifferenz): φ = φu − φi.
  - 0 < φ ≤ π/2: Spannung eilt Strom voraus.
  - φ = 0: Spannung und Strom in Phase.
  - −π/2 ≤ φ < 0: Spannung eilt Strom nach (bzw. Strom eilt Spannung voraus).

**Impedanz und Admittanz**

- Verallgemeinertes Ohmsches Gesetz im Bildbereich: U = Z · I.
- Impedanz Z (komplexer Widerstand): Z = (U/I) · e^(j(φu−φi)) = Z · e^(jφ).
  - Betrag Z = U/I: Scheinwiderstand, Einheit Ω.
  - Arithmetische Form: Z = R + jX (R = Wirkwiderstand/Resistanz, X = Blindwiderstand/Reaktanz).
  - Umrechnung Polarform ↔ arithmetische Form: Z = √(R² + X²); φ = arctan(X/R); R = Z·cosφ; X = Z·sinφ.
- Admittanz Y (komplexer Leitwert): Y = 1/Z = G + jB.
  - Y = Z⁻¹; Betrag Y = 1/Z: Scheinleitwert.
  - G: Wirkleitwert (Konduktanz); B: Blindleitwert (Suszeptanz).
  - Einheit: [Y] = [G] = [B] = Ω⁻¹ = Siemens (S).

**Reihen- und Parallelschaltung komplexer Widerstände**

- Reihenschaltung: Zges = Z1 + Z2; Yges = (Y1·Y2)/(Y1+Y2); Gesamtspannung U = U1 + U2; Spannungsteilerregel: U1/U = Z1/Z = Z1/(Z1+Z2).
- Parallelschaltung: Yges = Y1 + Y2; Zges = (Z1·Z2)/(Z1+Z2); Gesamtstrom I = I1 + I2; Stromteilerregel: I1/I = Y1/Y = Z/(Z1) = Z2/(Z1+Z2); I1/I2 = Y1/Y2 = Z2/Z1.

**Vier Grundverbraucher (Tabelle 1.7 — passive Zweipole im Wechselstromkreis)**

| Größe | Wirkwiderstand R | Induktivität L | Kapazität C | Allgemein |
|---|---|---|---|---|
| Grundgesetz (Zeit) | u = R·i | u = L·di/dt | i = C·du/dt | — |
| Phasendifferenz | φ = 0 | φ = +π/2 | φ = −π/2 | −π/2 ≤ φ ≤ +π/2 |
| Ohmsches Gesetz (Zeiger) | U = R·I | U = jωL·I | U = I/(jωC) | U = Z·I |
| Impedanz Z | Z = R | Z = jωL = jXL | Z = 1/(jωC) = jXC | Z = R+jX = Z·e^(jφ) |
| Blindwiderstand X | — | XL = ωL | XC = −1/(ωC) | — |
| Scheinwiderstand Z | Z = R | ZL = ωL | ZC = 1/(ωC) | Z = √(R²+X²) |
| Admittanz Y | Y = 1/R = G | Y = 1/(jωL) = jBL | Y = jωC = jBC | Y = G+jB = Y·e^(−jφ) |
| Blindleitwert B | — | BL = −1/(ωL) | BC = ωC | — |
| Scheinleitwert Y | Y = G | YL = 1/(ωL) | YC = ωC | Y = √(G²+B²) |

- Ohmscher Widerstand R: Strom und Spannung phasengleich (φ = 0); ZR = R reell; U = R·I.
- Induktivität L: Spannung eilt Strom um +90° vor; ZL = jωL (rein imaginär); XL = ZL = ωL; U = ωL·I (Effektivwerte); supraleitende Spule wäre ideale Induktivität, konventionelle Spulen aus Cu/Al haben Leiterwiderstand → φ merklich unter 90°.
- Kapazität C: Strom eilt Spannung um +90° vor (φ = −π/2); ZC = −j/(ωC); XC = −1/(ωC) (negativ); ZC = 1/(ωC) (positiv); I = ωC·U.
- Ohmsch-induktiver Verbraucher: φ zwischen 0 und +π/2; Praxisbeispiel: Asynchronmotor.
  - Reihenschaltung (RS, LS): Z = RS + jωLS; Z = √(RS² + ω²LS²); U = √(UR² + UL²).
  - Parallelschaltung (RP, LP): Y = 1/RP − j·1/(ωLP); Y = √(GP² + BP²); I = √(IR² + IL²).
- Scheinwiderstände frequenzabhängig: ZL(ω) = ωL; ZC(ω) = 1/(ωC).

---

#### 1.4.3 Elektrische Leistung, Wirkungsgrad und Blindleistungskompensation (Seiten 95–104)

**Momentanleistung und ihre Anteile**

- Momentanleistung: p(t) = u(t) · i(t); bei sinusförmigen Größen schwingt p(t) mit doppelter Frequenz (2ω) und halber Periodendauer.
- Zerlegung: p(t) = pW(t) + pB(t).
  - Momentane Wirkleistung: pW(t) = UI·cosφ · (1 − cos(2ωt)).
  - Momentane Blindleistung: pB(t) = UI·sinφ · sin(2ωt).
- pW(t) ist zu jedem Zeitpunkt ≥ 0 — irreversible Energieumwandlung (Wärme, Licht, Bewegung).
- pB(t) pendelt zwischen Quelle und Verbraucher (magnetisches/elektrisches Feld); zeitlicher Mittelwert = 0.

**Wirkleistung P**

- P = (2/T) · ∫₀^(T/2) p(t) dt = UI · cosφ; Einheit Watt (W).
- Im Verbraucherzählpfeilsystem (VZS): P ≥ 0 bei Verbrauchern (−π/2 ≤ φ ≤ π/2); P < 0 bei Erzeugern (z. B. PV-Anlage über Wechselrichter einphasig am NS-Netz).
- |P| = Amplitude von pW(t).

**Blindleistung Q**

- Q = UI · sinφ; Einheit Var (Volt-Ampere-reaktiv; franz. volt-ampère réactif), in der Literatur auch „var".
- Vorzeichen: Q > 0 bei induktivem Verbraucher (φ > 0); Q < 0 bei kapazitivem Verbraucher.
- Blindleistung kann dem Stromkreis weder entzogen noch zugeführt werden — deshalb ist die Bezeichnung „Blindleistungsverbrauch/-erzeugung" unzulässig; besser: Blindleistungsbedarf.
- |Q| = Amplitude von pB(t).

**Scheinleistung S**

- S = UI (ohne Berücksichtigung der Phasenlage); Einheit VA (Volt-Ampere); S ≥ 0.
- Beziehung: S² = P² + Q²; S = √(P² + Q²).
- Komplexe Scheinleistung S = U · I* = UI · e^(jφ) = P + jQ.
- Leistungsdreieck: P = Realteil, Q = Imaginärteil, S = Betrag.

**Leistungsfaktor (Wirkleistungsfaktor) λ**

- λ = |P| / S; Wertebereich 0 ≤ λ ≤ 1 (dimensionslos).
- Für sinusförmige Strom/Spannung und Verbraucher: λ = cosφ.
- Weitere Kennzahlen bei Sinusform: Verschiebungsfaktor |P|/S = |cosφ|; Wirkfaktor P/S; Blindfaktor Q/S; Verlustfaktor P/Q.
- **Tabelle 1.8 — Leistungskenngrößen verschiedener Verbraucher:**

| | R | L | C | Allgemein |
|---|---|---|---|---|
| P | P = UI | P = 0 | P = 0 | P = UI·cosφ |
| Q | Q = 0 | Q = UI | Q = −UI | Q = UI·sinφ |
| S | S = P | S = Q | S = −Q | S = UI |
| λ | λ = 1 | λ = 0 | λ = 0 | λ = cosφ |

- Berechnung der komplexen Scheinleistung S für linearen Verbraucher mit Impedanz Z: S = U²/Z* oder S = Z·I².
- Reihenschaltung (RS, XS = ωLS): P = RS·I²; Q = XS·I².
- Parallelschaltung (RP, XP = ωLP): P = U²/RP; Q = U²/XP.

**Wirkungsgrad der Energieübertragung**

- Erhöhter Blindleistungsbedarf (induktiver Blindstrom) verursacht zusätzliche Stromwärmeverluste auf der Leitung → verschlechtert Wirkungsgrad.
- Ersatzschaltbild: Spannungsquelle − Leitung (RL) − Verbraucher (Pab).
- Wirkungsgrad: η = Pab / (Pab + Pδ) = 1 / (1 + RL·Pab / (UV·cosφ)²).
- Einflussgrößen auf η:
  1. Vom Verbraucher aufgenommene Wirkleistung Pab (vorgegeben, wird bezahlt).
  2. Leiterwiderstand RL = ρ·l/A (wenig Spielraum; Supraleiter wäre optimal, aber wegen Kühlaufwand unwirtschaftlich; größere Querschnitte → kleineres RL, aber Kostenfrage Amortisation über Lebensdauer; Freileitungsseile müssen auf Rollen transportiert und aufgehängt werden; Kabel brauchen Biegeradien).
  3. Spannung am Verbraucher UV (hohe Betriebsspannung → geringere Ströme → weniger Verluste → erfordert Leistungstransformatoren).
  4. Leistungsfaktor cosφ (höherer λ → besserer Wirkungsgrad; ideal λ = 1).

**Blindleistungskompensation**

- Technische Anschlussbedingungen (TAB) der Verteilnetzbetreiber: Leistungsfaktor einer Verbrauchereinheit muss zwischen 0,9 und 1,0 liegen.
- Haushalte: erfahrungsgemäß λ ≈ 0,9 → keine weiteren Maßnahmen erforderlich.
- Handwerk/Industrie: bei λ < 0,9 meist Blindleistungskompensation mit Leistungskondensatoren (auch Blindstromkompensation genannt) oder Bezahlung der Blindarbeit über Blindleistungszähler.
- Leistungskondensatoren werden typischerweise parallel zu den Verbrauchern geschaltet (Reihenkom pensation möglich, aber selten).
- Durch Regelkreise können einzelne Kondensatoren im laufenden Betrieb zu- oder abgeschaltet werden.
- **Vollständige Kompensation:** λ = 1; pB(t) = 0; kapazitive und induktive Blindleistung gleich groß, entgegengesetzt → kein Blindstrom auf der Zuleitung; nur Wirkleistung aus dem Netz.
- **Unvollständige Kompensation (üblich):** λ oft genau auf 0,9 eingestellt — Gründe:
  1. Ersparnis bei Kondensatoren.
  2. Kurve η(cosφ) zwischen 0,9 und 1,0 sehr flach (Beispielrechnung: RL = 1 Ω, Pab = 1 kW, UV = 230 V).
  3. Überkompensation vermeiden: Anlage würde wie ohmsch-kapazitiver Verbraucher wirken → Spannungserhöhungen möglich, wenn Netz-Induktivität und Kapazität Schwingkreis bilden.
  4. Überkompensierte Asynchronmotoren können bei Netzabschaltung in Selbsterregung geraten → bis zum Stillstand gefährliche Überspannungen.
- Erforderliche kapazitive Blindleistung: QC = Q2 − Q1 = P · (tanφ2 − tanφ1).
- Benötigte Kapazität: C = −QC / (ω·U²) = P·(tanφ1 − tanφ2) / (2πf·U²).
- Kompensationsarten:
  - Zentralkompensation (im Schaltschrank): einfach und günstig, aber Blindströme belasten Leitungen zwischen Verbrauchern und Kondensator → ggf. größere Querschnitte nötig; Blindstromverluste zahlt Anschlussnehmer.
  - Gruppenkompensation (mehrere Verbraucher zusammen).
  - Einzelkompensation (pro Verbraucher): aufwendiger, aber Blindströme auf Zuleitungen entfallen.

**Verluste im Wechselstromkreis**

Wechselstrom hat gegenüber Gleichstrom zusätzliche Verluste bei Transformatoren, Leitungen und Kondensatoren:

- **Leistungstransformatoren:**
  - Kupferverluste: Stromwärmeverluste der Wicklungen.
  - Eisenverluste (Kern):
    - Hystereseverluste (Umorientierungsverluste): Elementarmagnete müssen sich mit Netzfrequenz umorientieren; mittlere Wärmeleistung PH ~ f; Reduktion durch Weichmagnete (schmale Hysteresekurve).
    - Wirbelstromverluste: Wechselfeld induziert quer zur Flussrichtung Spannungen → wirbelförmige Ströme im Material; mittlere Wärmeleistung PW ~ f²; Reduktion durch gegeneinander elektrisch isolierte dünne Eisenbleche.

- **Elektrische Leitungen und Kabel:**
  - Skin-Effekt: Zeitlich veränderliches Magnetfeld des Wechselstroms erzeugt Wirbelströme → überlagern sich mit Wechselstrom → Stromdichte am Rand der Querschnittsfläche höher als innen (Stromverdrängung). Folge: Generatorsammelschienen in konventionellen Kraftwerken als Röhren ausgeführt.
  - Proximity-Effekt: In Spulen induzieren Wechselfelder benachbarter Leiter zusätzlich Wirbelströme.
  - Wechselstromwiderstand: RL = ρ·l/A + ΔR (größer als im Gleichstromkreis); ΔR nicht analytisch berechenbar → Herstellerangaben oder Messwerte notwendig.

- **Kondensatoren — dielektrische Verluste Pδ:**
  - Leckstromverluste (mangelhafte Isolierung) + Umorientierungsverluste (elektrische Dipole im Wechselfeld).
  - Ersatzschaltbild: Parallelwiderstand Rδ zu idealem Kondensator C.
  - Verlustfaktor: |P/Q| = tanδ = IR/IC (δ = Verlustwinkel).
  - Güte (Gütefaktor, Q-Faktor) = 1/tanδ.

---

#### 1.4.4 Oberschwingungen (Seiten 97–113)

**Netzrückwirkungen und Spannungsqualität**

- Erzeuger, Betriebsmittel und Verbraucher können Abweichungen von Spannungsamplitude sowie Spannungs- und Stromform verursachen. Kategorien nach Norm:
  - Harmonische, Zwischenharmonische und Subharmonische.
  - Spannungsschwankungen mit eventueller Flickerwirkung.
  - Transiente Überspannungen.
  - Spannungsunsymmetrien.
  - Spannungseinbrüche und Spannungsausfälle.
- Qualitätsniveau der Versorgungsspannung geregelt in europäischer Norm **EN 50160** (Merkmale der Spannung in öffentlichen Elektrizitätsversorgungsnetzen).
- Spannungsband laut EN 50160: ±10 % um Un; kurzzeitige Spannungsänderungen < ±10 % (schnell) oder < 5 % (langsam); Spannungseinbruch: >1 % bis <90 % für bis zu 3 min (kurz) oder >3 min (lang); transiente Überspannungen: 1 µs bis einige ms; Flicker: bis einige Sekunden.

**Flicker**

- Elektrische Spannungsschwankungen, die zu subjektiv sichtbarer Leuchtdichteschwankung bei ungeregelten Leuchtmitteln führen (Leuchtstofflampen, Glühlampen).
- Elektronisch geregelte Leuchtmittel (LED, Kompaktleuchtstofflampen) zeigen keinen wahrnehmbaren Flicker.

**Ursachen von Oberschwingungen (Tabelle 1.9)**

| Ursache | Schaltungstyp | Gerätebeispiele | k=2 % | k=3 % | k=4 % | k=5 % | k=7 % |
|---|---|---|---|---|---|---|---|
| Sättigung | nichtlinear | Kleinmotoren | — | 3…10 | — | 1…5 | — |
| Magnetisierungsstrom | nichtlinear | Transformator | — | 25…55 | — | 8…30 | 2…10 |
| Gasentladung | nichtlinear | Leuchtstofflampe | 1…2 | 8…20 | — | 2…3 | 1…2 |
| Lichtbogenofen | nichtlinear | Lichtbogenofen | 5…12 | 6…12 | 2…5 | 3…7 | 1…3 |
| Einweggleichrichter ohmsch | Schalter | Leistungshalbierung (Fön, Heizdecke) | 42 | — | 8 | — | — |
| Einweggleichrichter kapazitiv | Schalter | einfache Netzgeräte, Unterhaltungselektronik | 70…90 | 40…60 | 35…50 | 25…50 | 12…25 |
| Zweiweggleichrichter kapazitiv | Schalter | TV, Monitor, PC, Motorantriebe | — | 65…80 | — | 50…70 | 25…35 |

(Ik/I1 in % = Oberschwingungs-Effektivwert der k-ten Ordnung bezogen auf Grundschwingung)

- Nichtlineare Kennlinie (z. B. Varistor i = k·u³): erzeugt bei sinusförmiger Spannung nichtsinusförmigen Strom mit Oberschwingungen (im Beispiel: 3. Harmonische bei Varistor).
- Periodi sch arbeitende Schalter: Dimmer (Phasenanschnittwinkel α steuerbar), Frequenzumrichter, Wechselrichter (Windkraft, Solar, HGÜ, Motorsteuerungen) erzeugen ebenfalls Oberschwingungen.
- Starke Stromverzerrungen bei Schaltnetzteilen typisch (Messbild: Strom i(t) eines Schaltnetzteils, Zeitbereich 0–40 ms).
- Oberschwingungsströme bewirken Spannungsabfälle an Netzimpedanzen → auch Spannungen verformt.

**Fourierreihen und Kenngrößen (Harmonische Analyse)**

- Periodisches Signal f(t) als Fourierreihe: f(t) = a0 + Σ(k=1→∞)[ak·cos(kωt) + bk·sin(kωt)].
- Gleichanteil: a0 = (1/T)·∫₀ᵀ f(t) dt.
- Fourierkoeffizienten: ak = (2/T)·∫₀ᵀ f(t)·cos(kωt) dt; bk = (2/T)·∫₀ᵀ f(t)·sin(kωt) dt.
- Numerische Berechnung: DFT (Diskrete Fourier-Transformation) mit trigonometrischer Interpolation oder FFT (Fast Fourier Transform).
- Alternative Fourierreihendarstellung: f(t) = a0 + Σ(k=1→∞) ck·sin(kωt + φk); Amplitude k-ter Oberwelle: ck = √(ak² + bk²); Phasenlage: tanφk = ak/bk.
- Amplitudenspektrum: Auftragung der Amplituden ck über Ordnungszahl k.
- Effektivwerte der k-ten Teilschwingung: Ik = ûk/√2; Uk = ûk/√2.
- Gleichanteile: I0, U0 (entsprechen a0).
- Gesamteffektivwerte: I = √(Σk=0→∞ Ik²); U = √(Σk=0→∞ Uk²).
- Messgeräte mit TRMS (True RMS) berücksichtigen Oberschwingungsanteile am Effektivwert.
- **Grundschwingungsgehalt** (für Größen ohne Gleichanteil): gi = I1/I; gu = U1/U.
- **Oberschwingungsgehalt / Klirrfaktor** (THDC — Total Harmonic Distortion Current):
  - ki = (1/I)·√(Σk=2→∞ Ik²) = √(I² − I1²)/I = √(1 − gi²).
  - Entsprechend für Spannungen: ku = √(1 − gu²).
  - In der Praxis wird der Laufindex k auf 40 oder 50 begrenzt.

**Elektrische Leistung mit Oberschwingungen**

- Fall 1: Nur Strom enthält Oberwellen, Spannung sinusförmig (u(t) = √2·U·sin(ωt + φu)):
  - Wirkleistung: P = U·I1·cosφ1 (nur Grundschwingungsanteil des Stroms trägt zur Wirkleistung bei).
  - Scheinleistung: S = U·I = U·√(Σk=1→∞ Ik²).
  - Blindleistung: Q = √(S² − P²) (mit ± Vorzeichen).
  - Zerlegung Q in zwei Anteile:
    - Grundschwingungsblindleistung (Verschiebungsblindleistung): Q1 = U·I1·sinφ1.
    - Verzerrungsblindleistung (Verzerrungsleistung, Oberschwingungsblindleistung, auch mit Formelbuchstabe D): Qd = U·√(Σk=2→∞ Ik²).
    - Gesamt-Blindleistung: Q = √(Q1² + Qd²).
  - Dreidimensionales Leistungsdiagramm: P, Q1, Qd, Q, S, S1 (= U·I1 = Grundschwingungs-Scheinleistung).

- Fall 2: Beide, Strom und Spannung, enthalten signifikante Oberwellen:
  - u(t) = Σk=1→∞ √2·Uk·cos(kωt + φuk); i(t) = Σk=1→∞ √2·Ik·cos(kωt + φik).
  - Gesamte Wirkleistung: P = Σk=1→∞ Pk = Σk=1→∞ Uk·Ik·cosφk (Grundschwingungswirkleistung P1 + Oberschwingungswirkleistungen Pk für k ≥ 2).
  - In diesem Fall existieren Grundschwingungs- und Verzerrungsblindleistung nicht getrennt; Blindleistung nach Q = ±√(S² − P²) definiert.

**Gefahren durch Oberschwingungen und Abhilfemaßnahmen**

- Probleme durch Oberschwingungsströme innerhalb der Anlage oder im Versorgungsnetz:
  - Überbeanspruchung von Kompensationskondensatoren.
  - Überlastung von Neutralleitern.
  - Überhitzung von Transformatoren.
  - Fehlauslösung oder Zerstörung von FI-Schutzschaltern.
  - Skineffekte (höhere Verluste).
  - Überhitzung und Hochlaufschwierigkeiten von Drehfeldmotoren (durch Oberschwingungsspannungen).
- Methoden zur Begrenzung/Reduktion von Oberwellen:
  1. Passive Filter (abgestimmte Filterkreise auf bestimmte Ordnungszahlen, z. B. I5, I7, I11, I13 bei 250, 350, 550, 650 Hz).
  2. Trenntransformatoren und Oberschwingungs-Reduktionstransformatoren.
  3. Aktive Filter.
- Weiterführende Literatur zum Thema Spannungsqualität (Power Quality, PQ) sind in [101–111] verwiesen.

---

### 1.5 Drehstrom (Seiten 113–120)

Drehstromtechnik ist weltweit maßgeblich für die Energiefortleitung; auch mit der Energiewende bleibt das so. Wechselstrom = einphasiger Wechselstrom; Drehstrom = dreiphasiger Wechselstrom.

#### 1.5.1 Leitungen — Kennzeichnung der Leiter (Seiten 113–116)

- Drehstromleitung: drei Außenleiter L1, L2, L3 (Dreileitersystem). Alte Kennzeichnung R, S, T heute kaum gebräuchlich. Im Handwerk/bei Netzbetreibern wird ein einzelner Außenleiter oft als „Phase" bezeichnet.
- Niederspannungsebene: vierter Leiter — Neutralleiter N (früher Mittelleiter) → Vierleitersystem.
- Alle anderen Spannungsebenen: nur drei Leiter.
- Schutzleiter-Varianten:
  - Freileitungen: Erdseil.
  - Kabel: PE-Leiter (Protective Earth).
  - 5-Leiternetz: N und PE separat verlegt.
  - PEN-Leiter (Protective Earth Neutral): kombiniert Schutz- und Neutralleiterfunktion; früher Nullleiter genannt.

**Tabelle 1.10 — Kennzeichnung der Leiter:**

| Leiter | Kürzel | Farbe der Isolation |
|---|---|---|
| Außenleiter | L1/L2/L3 | alles außer: grün-gelb, grün, gelb, mehrfarbig |
| Neutralleiter (früher Mittelleiter) | N | in der Regel hellblau |
| Schutzleiter | PE | grün-gelb, zwingend |
| PEN-Leiter (früher Nullleiter) | PEN | grün-gelb, zwingend |

- Außenleiter + Neutralleiter gehören zum Betriebsstromkreis.
- Schutzleiter haben je nach Einbauort unterschiedliche Namen (Hauptschutzleiter/Hauptpotenzialausgleichsleiter, Potenzialausgleichsleiter, Haupterdungsleiter, Erder) — nach [117].
- Schaltpläne: statt Kürzel auch Schaltzeichen zur Leiterkennzeichnung verwendbar.

**Leitergrößen Spannung und Strom**

- Zwischen L1, L2, L3: drei sinusförmige Außenleiterspannungen (Leiter-Leiter-Spannungen, verkettete Spannungen, Dreieckspannungen; z. B. uL1L2(t) oder vereinfacht u12(t)).
- Phasenverschiebung der drei Spannungen untereinander: 2π/3 = 120°.
- Zwei Phasenfolgenmöglichkeiten: Rechtsdrehfeld (Maxima in Reihenfolge nach Abb. 1.131) und Linksdrehfeld (durch Vertauschen zweier beliebiger Anschlüsse).
- Maschenregel für die drei Außenleiterspannungen: u12(t) + u23(t) + u31(t) = 0 (im Zeigerbild: U12 + U23 + U31 = 0).
- Zeigerbild: U12 = U12·e^(j0°); U23 = U23·e^(−j120°); U31 = U31·e^(−j240°).
- Netznominalspannung Un (in Deutschland statt Bemessungsspannung Ur); Spannungsband: ΔU/Un < ±10 %.

**Tabelle 1.11 — Netznominalspannungen Un und maximale Spannungen Umax nach DIN IEC 60038:**

| Spannungsebene | Kürzel | Un / kV | Umax / kV |
|---|---|---|---|
| Höchstspannung | HöS | 380 | 420 |
| Hochspannung | HS | 110 | 123 |
| Mittelspannung | MS | 20 | 23 |
| Mittelspannung | MS | 10 | 12 |
| Niederspannung | NS | 0,4 | — |

- Historisch: 220-kV-Ebene noch vorhanden, wird schrittweise zurückgebaut.
- Sonderspannungen MS für Hochspannungsmotoren, Kraftwerkseigenbedarf, Öfen, Elektrolyseanlagen: 6 kV, 30 kV, 60 kV.
- Manche industrielle motorische Verbraucher: NS 500 V.
- Ortsnetzstationen: Bindeglied zwischen MS- und NS-Netz; Ortsnetztransformator — Unterspannungsseite meist in Sternschaltung; Sternpunkt → Neutralleiter; Sternspannungen = Leiter-Erd-Spannungen (z. B. UL1N = U1N = U1).
- Phasenverschiebung Leiter-Erd-Spannungen untereinander: ±120°; Zeiger bilden Stern → Leiterspannungen bilden gleichseitiges Dreieck (Maschenregel).
- Verhältnis Dreiecks- zu Sternspannungen: UΔ/UY = 2·cos30° = √3 (Verkettungsfaktor).
- Beispiel Zeigerbild: Eine Leiterspannung + zwei Leiter-Erdspannungen bilden gleichschenkliges Dreieck; Leiterspannungszeiger 30° versetzt gegenüber Sternspannungszeigern.
- Außenleiterströme: in drei Leitern L1, L2, L3 (= Sterngrößen, mit Phasenverschiebung zur Sternspannung bei λ < 1).
- Bei gleichmäßiger Belastung: Außenleiterströme untereinander ±120° phasenverschoben, gleiche Effektivwerte.
- In der NS-Ebene möglich: unterschiedliche Effektivwerte der drei Leiterströme bei unsymmetrisch angeschlossenen einphasigen Verbrauchern und Erzeugern.
- Vollständige Bezeichnungen für Leiterströme/-spannungen in Drehstromnetz (mit drei Außenleitern) und Einphasennetz (gespeist aus Drehstromnetz) gemäß Abb. 1.135.

#### 1.5.2 Drehstrom-Verbraucher — Dreieck- und Sternschaltung (Seiten 119–120)

- Drehstromverbraucher-Beispiele: Elektrische Durchlauferhitzer, Elektroherde, Drehstrommotoren.
- Anschlusspunkte von Drehstromverbrauchern: U, V, W (und ggf. N).

**Tabelle 1.12 — Kürzel für Außenleiter und Betriebsmittelanschlüsse:**

| Stromart | Leiter | Kürzel Leiterkennz. | Kürzel Geräteanschluss |
|---|---|---|---|
| Wechselstrom | Außenleiter 1 | L1 | U |
| Wechselstrom | Außenleiter 2 | L2 | V |
| Wechselstrom | Außenleiter 3 | L3 | W |
| Wechselstrom | Neutralleiter | N | N |
| Gleichstrom | positiver Leiter | L+ (C) | L+ (C) |
| Gleichstrom | negativer Leiter | L− (D) | L− (D) |
| Gleichstrom | Mittelleiter | M | M |
| Schutz | Schutzleiter | PE | PE |
| Schutz | PEN-Leiter | PEN | — |
| — | Erde | E | E |
| — | fremdspannungsfreie Erde | TE | TE |
| — | Masse | MM | MM |

- Verbraucher besteht aus drei Strängen (z. B. beim Drehstrom-Asynchronmotor: drei Spulen im Stator, Spulenachsen räumlich je 120° verdreht).
- Zwei Verschaltungsarten:

  **Dreieckschaltung:**
  - Strangimpedanzen Z12, Z23, Z31 zwischen Anschlusspunkten.
  - An den Strängen liegen die Außenleiterspannungen an.

  **Sternschaltung:**
  - Strangimpedanzen Z1, Z2, Z3.
  - Durch die Stränge fließen die Außenleiterströme.

- Umwandlung Dreieck → Stern (Dreieck-Stern-Transformation):
  - Z1 = (Z12·Z31) / (Z12 + Z23 + Z31)
  - Z2 = (Z23·Z12) / (Z12 + Z23 + Z31)
  - Z3 = (Z31·Z23) / (Z12 + Z23 + Z31)

- Umwandlung Stern → Dreieck (Stern-Dreieck-Transformation):
  - Z12 = Z1 + Z2 + Z1·Z2/Z3
  - Z23 = Z2 + Z3 + Z2·Z3/Z1
  - Z31 = Z3 + Z1 + Z3·Z1/Z2
