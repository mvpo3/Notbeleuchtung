# Grundladen der elektrischen Energietechnik — Teil 10
> Quelle: Grundladen der elektrischen Energietechnik (buecher) · Seiten 401-440.

Dieser Teil schliesst das Kapitel 5 (Niederspannungsnetze im Gebäude) mit Fehlerstrom-Schutzeinrichtungen und Netzsystemen ab und enthält dann den vollständigen Anhang des Buches: SI-Einheiten, Schreibweisen, Formelzeichen-Verzeichnis, Indizes, Abkürzungsverzeichnis sowie Normen-Referenztabellen für elektrische Maschinen und elektrische Energietechnik.

## Inhalt

### Fehlerstrom-Schutzeinrichtungen: Typen und Auslöseverhalten (Kap. 5, S. 401–403)

- **Typ AC** — erkennt ausschliesslich sinusförmige Wechselfehlerströme (wechselstromsensitiv). Nach DIN VDE 0100-530 nicht für vorgeschriebene Schutzmassnahmen in Deutschland zugelassen; darf kein VDE-Zeichen tragen.
- **Typ A** — erfasst sinusförmige Wechsel- sowie pulsierende Gleichfehlerströme (pulsstromsensitiv). Beherrscht Fehlerstromformen einphasiger Verbraucher mit Elektronik (EVG, Dimmer). Glatte Gleichfehlerströme bis 6 mA führen zur sicheren Auslösung.
- **Typ B** — allstromsensitiv; geeignet für alle Fehlerstromarten wie Typ A, zusätzlich sichere Auslösung bei Frequenzgemischen bis 2 kHz sowie glatten Gleichfehlerströmen bis 10 mA. Deckt Ausgangsseite einphasig angeschlossener Frequenzumrichter (Waschmaschinen, Pumpen) ab.
- **Typ B+** — erfüllt alle Anforderungen von Typ B, ebenfalls allstromsensitiv. Zusätzliche Auslösebedingungen bis 20 kHz definiert (vorbeugender Brandschutz bei Erdfehlerströmen). Im Frequenzbereich bis 20 kHz ist der Auslösestrom auf maximal 420 mA begrenzt.

**Auslöseunabhängigkeit:** Erfassung, Auswertung und Abschaltung erfolgen unabhängig von Netz- oder Hilfsspannung. Nur bei Typ B ist für glatte Gleichfehlerströme eine Netzspannungsversorgung erforderlich. Wechsel- und pulsierende Gleichfehlerströme benötigen keine externe Spannungsversorgung.

**Prüftaste:** Jedes Gerät hat eine Prüftaste, die einen künstlichen Fehlerstrom erzeugt — die Schutzeinrichtung muss daraufhin auslösen.

**Auslösestrom-Nennwert (I∆no):** Der Nicht-Auslösewert beträgt I∆no = 0,5 I∆n. Ein RCCB oder RCBO darf nur auslösen, wenn I∆no ≤ I∆ ≤ I∆n. Üblicher Wert liegt bei I∆ = 0,8 I∆n.

**Auslösezeit:** Beim Bemessungsfehlerstrom muss die Abschaltung innerhalb von 300 ms erfolgen (nach DIN EN 61008-1 / VDE 0664-10). Nur stromstoßfeste selektive Schalter dürfen 0,5 s benötigen.

**Selektivität in Reihenschaltung:** Fehlerstrom-Schutzeinrichtungen können in Reihe geschaltet werden. Dazu müssen Geräte des Typs S eingebaut werden. Empfehlung: mindestens 3-fach höherer Bemessungsfehlerstrom I∆n für nachgeschaltete Einrichtungen. Selektive Geräte Typ S haben eine Stoßstromfestigkeit von mindestens 3 kA. Bei einem CBR (DIN EN 60947-2) gibt es keine selektiven Ausführungen; Selektivität nur über einstellbare Abschaltzeitverzögerungen erreichbar.

**Körperstrom-Wirkungsbereiche (Wechselstrom):** Vier durch die Zeit-Strom-Kennlinie abgegrenzte Bereiche:
1. Bereich 1 — keine spürbaren Wirkungen
2. Bereich 2 — Strom wahrnehmbar; medizinisch schädliche Einwirkungen und Muskelverkrampfungen treten üblicherweise nicht auf
3. Bereich 3 — Blutdrucksteigerungen, Muskelverkrampfungen und Atemnot möglich; Herzkammerflimmern üblicherweise kein Risiko
4. Bereich 4 — Herzkammerflimmern möglich; Herzstillstand, Atemstillstand und Brandverletzungen werden zunehmend wahrscheinlich

Die Schutzwirkung bei 10 mA und 30 mA Bemessungsfehlerstrom wird nicht durch Strombegrenzung, sondern durch schnelle Abschaltung erzielt.

---

### Netzsysteme: Erdungsarten und Kennzeichnung (Kap. 5.3, S. 395–402)

**Grundprinzip Erdverbindungen (nach DIN EN 61293):** Drei Erdverbindungsarten für Netze unter 1 kV, gekennzeichnet durch Buchstaben:

| Buchstabe | Herkunft | Bedeutung | Anwendung |
|-----------|----------|-----------|-----------|
| T | terre (frz.) | direkte Erdung | Spannungsquelle oder Körper direkt geerdet |
| N | neutral | direkte Betriebserde-Verbindung | leitfähige Körper mit Betriebserde verbunden |
| I | isolated | isoliert | alle aktiven Teile isoliert |

- Erster Buchstabe = Erdungsverhältnis der Spannungsquelle (meist Ortsnetztransformator)
- Zweiter Buchstabe = Erdungsverhältnis leitfähiger Körper in der Anlage (nicht zum Betriebsstromkreis gehörig)

**Drei Netzsystem-Grundtypen:** TN-, TT- und IT-System. TN-Netze haben drei Varianten: TN-C, TN-C-S und TN-S.

---

### Erdungen und Erdverbindungen (Kap. 5.3.1, S. 395–396)

**Definition Erden:** Herstellung einer elektrischen Verbindung zwischen einem Punkt der Anlage und dem Erdreich.

**Definition Bezugserde (neutrale Erde):** Bereich im Erdreich, in dem überall dasselbe elektrische Potenzial herrscht — auch bei Erdfehlerströmen. Zwischen zwei beliebigen Punkten dieses Bereichs dürfen keine merklichen Spannungen auftreten. Potenzial festgelegt auf 0 V.

**Erder-Bauformen:**
- Oberflächenerder: z. B. Banderder, Seilerder (flach verlegt, Tiefe < 1 m)
- Tiefenerder: z. B. Staberder, Rohrerder
- Fundamenterder: in Gebäuden (s. Abb. 5.6)

**Funktion der Erdungsarten:**
- Netzbetriebserdung: Erdung aktiver Teile im elektrischen Energienetz
- Schutzerdung (PE, Protective Earth): Schutz vor elektrischem Schlag; leitfähige berührbare Gehäuse (Körper) werden über Schutzleiter an die Potenzialausgleichsschiene angeschlossen, die mit dem Fundamenterder verbunden ist. Auch als Schutzpotenzialausgleich bezeichnet.
- Funktionserdung (FE, Functional Earth): Erdung für andere Zwecke, z. B. wenn Schutzerdung die EMV nicht sicherstellen kann.

**Erdungswiderstand:** Widerstand zwischen Bezugserde und Potenzialausgleichsschiene (= Haupterdungsschiene). Setzt sich zusammen aus Ausbreitungswiderstand des Erders und dem Widerstand des Erdungsleiters.

---

### TN-Netze (Kap. 5.3.2, S. 397–399)

Dritter Kennbuchstabe bei TN-Systemen:
- C (combined) = Neutral- und Schutzleiter kombiniert in einem Leiter (PEN-Leiter)
- S (separated) = Neutral- und Schutzleiter getrennt geführt

**TN-C-System:**
- Im gesamten System sind Neutral- und Schutzleiterfunktion im PEN-Leiter vereint.
- Leitfähige Körper der Anlage direkt mit der Betriebserdung verbunden.
- Bei Körperschluss: Abschaltung durch Überstrom-Schutzeinrichtung.
- Einsatz von Fehlerstrom-Schutzeinrichtungen nicht sinnvoll.
- Entscheidender Nachteil: Unterbrechung des PEN-Leiters setzt das Metallgehäuse unter volle Netzspannung gegen Erde → Lebensgefahr (wenn Geräteschalter geschlossen ist).
- Diese Netze waren bis Mitte der 1960er Jahre in Haushalten verbreitet (früher: "klassische Nullung" oder "Nullung ohne besonderen Schutzleiter"). Heute noch in der Industrie anzutreffen.

**TN-C-S-System:**
- In einem Teil des Systems sind Neutral- und Schutzleiter kombiniert (PEN), im anderen Teil getrennt (N + PE).
- Standard für Neuinstallationen. Vom 0,4-kV-Verteilnetz kommt ein vieradriges Kabel ins Gebäude; in der Verteilung dann fünf Leiter.
- Trennpunkt PEN → PE + N sollte nach Vorschrift im Hausanschlusskasten liegen (manchmal auch im Schaltschrank).
- Niedrige Schleifenimpedanz ermöglicht sehr schnelle Abschaltung beim Einsatz eines RCD.
- Fällt ein RCD aus, besteht bei eingehaltenen Abschaltbedingungen für Überstrom-Schutzeinrichtungen noch ein zusätzlicher Schutz.
- Vorteil für Verteilnetzbetreiber: Durch Einbeziehung der Fundamenterder aller Kundenanlagen entsteht ein grossflächiges (globales) Erdungssystem; dadurch kann die Anzahl geerdeter Kabelverteilerschränke ausserhalb der Gebäude reduziert werden.

**TN-S-System:**
- Im gesamten System ist ein separater Schutzleiter verlegt.
- Es darf nur einen zentralen Verbindungspunkt zwischen PE und N geben: den zentralen Erdungspunkt (ZEP) auf der Unterspannungsseite des Transformators.
- Typische Anwendung: Rechenzentren (Transformator in Hand des Anschlussnehmers; auf FI-Schutzschalter wird verzichtet, um hohe Verfügbarkeit zu sichern).
- Verteilnetzbetreiber betreiben keine TN-S-Netze.

---

### TT-Netze (Kap. 5.3.3, S. 399–401)

- Auf der Unterspannungsseite des Transformators geerdet; N-Leiter angeschlossen.
- Schutzleiter PE wird nicht über N geerdet, sondern vor Ort mit einem Anlagenerder verbunden → im gesamten System von N getrennt.
- Wegen unterschiedlicher Erdungswiderstände RA und RB kann eine kleine Spannung (~1 V) zwischen PE und N anliegen.
- Vorteil: Blitzüberspannung, die über den N-Leiter einer Freileitung ins Gebäude gelangt, erreicht nicht die metallischen Gehäuse oder Rohrleitungen → lebensgefährliche Berührungsspannungen vermieden. Mit zunehmender Verkabelung öffentlicher NS-Netze verliert dieser Vorteil an Bedeutung.
- Nachteil: Schutzerdung problematisch; für schnelles Ansprechen der Überstrom-Schutzeinrichtung sind sehr hohe Ströme nötig, was sehr niedrige Erdungswiderstände voraussetzt — in der Praxis kaum erreichbar. Sanierung bestehender Fundamenterdung meist nicht vertretbar → Rückgriff auf Fehlerstrom-Schutzschaltung.
- TT-Systeme noch in vielen deutschen Verteilnetzen sowie anderen europäischen Ländern vorhanden. TT- und TN-C-S-Systeme werden oft parallel betrieben.

---

### IT- und I-Netze (Kap. 5.3.4, S. 401–402)

- Sternpunkt des Transformators ist isoliert; hochohmige Erdung zulässig.
- Keine direkte Verbindung zwischen aktiven Leitern und geerdeten Teilen.
- Bei einem einfachen Körper- oder Erdschluss: Fehlerstrom schliesst sich über Erdkapazitäten CE und Isolationswiderstände der gesunden Leiter. Die Scheinwiderstände ZE = (ωCE)⁻¹ sind bei kurzen NS-Leitungen gross → Fehlerströme niedrig → Schritt- und Berührungsspannungen klein.
- Folge: Bei einem ersten Fehler können IT-Netze weiter betrieben werden (anders als TN- oder TT-Systeme). Es erfolgt lediglich eine Meldung vom Isolationsüberwachungsgerät (Isolationswächter).
- Auch bei Überstrom wird bei einem einzigen Fehler nicht sofort abgeschaltet. Erst bei einem zweiten, ungünstig liegenden Fehler schaltet ein Fehlerstrom-Schutzschalter oder eine Überstrom-Schutzeinrichtung ab.
- Typische Anwendungen: Operationsräume in Krankenhäusern, Flugzeuge, U-Boote, mobile Bordnetze (I-Systeme ohne Erdverbindung).
- Die Kapazität des Zylinderkondensators berechnet sich zu C = 2π ε l / ln(r₂/r₁) und steigt mit der Leiterlänge l.

---

### Anhang A.1 — Schreibweisen (S. 407–421)

#### SI-Einheiten (A.1.1)

- Das SI-System wurde in deutsches Recht übernommen durch das Gesetz über Einheiten im Messwesen vom 2. Juli 1969 und die Ausführungsverordnung vom 26. Juni 1970.
- 1985 novelliert aufgrund einer EG-Richtlinie von 1981; SI-Definitionen wurden entfernt, Verweis auf DIN 1301-1 (Ausgabe Dezember 1985).
- Seit dem Weltmetrologietag am 20. Mai 2019 gelten neue SI-Definitionen, basierend auf sieben festgelegten Naturkonstanten (CODATA-Ausgleichsrechnung 2017).

**Festgelegte Naturkonstanten (Tab. A.2):**

| Konstante | Wert | Beschreibung |
|-----------|------|-------------|
| Δν | 9 192 631 770 s⁻¹ | Hyperfeinstrukturübergangsfrequenz des ¹³³Cs-Grundzustands |
| c₀ | 299 792 458 m/s | Lichtgeschwindigkeit im Vakuum |
| h | 6,626 070 15 · 10⁻³⁴ J·s | Planck-Konstante |
| e | 1,602 176 634 · 10⁻¹⁹ C | Elementarladung |
| k | 1,380 649 · 10⁻²³ J/K | Boltzmann-Konstante |
| Nₐ | 6,022 140 76 · 10²³ mol⁻¹ | Avogadro-Konstante |
| Kcd | 683 cd·sr·kg⁻¹·m⁻²·s³ | Photometrisches Strahlungsäquivalent bei 540 · 10¹² Hz |

**SI-Basiseinheiten (Tab. A.3):**

| Grösse | Einheitenname | Zeichen | Definition |
|--------|--------------|---------|-----------|
| Zeit | Sekunde | s | 1 s = 9 192 631 770 / Δν |
| Länge | Meter | m | 1 m = (c₀ / 299 792 458) s |
| Masse | Kilogramm | kg | 1 kg = (h / 6,626 070 15) · 10³⁴ m⁻² s |
| Stromstärke | Ampere | A | 1 A = (e / 1,602 176 634) · 10¹⁹ s⁻¹ |
| Temperatur | Kelvin | K | 1 K = (1,380 649 / k) · 10⁻²³ kg m² s⁻² |
| Stoffmenge | Mol | mol | 1 mol = 6,022 140 76 · 10²³ / Nₐ |
| Lichtstärke | Candela | cd | 1 cd = (Kcd / 683) kg m² s⁻³ sr⁻¹ |

Hinweis: Das Urkilogramm (Platin-Iridium-Zylinder in Paris, 130 Jahre in Verwendung) ist damit abgelöst. Ein Kilogramm wird nun über das Plancksche Wirkungsquantum h definiert.

**SI-Vorsätze (Tab. A.4) — vollständige Liste:**

| Potenz | Name | Zeichen | Potenz | Name | Zeichen |
|--------|------|---------|--------|------|---------|
| 10³⁰ | Quetta | Q | 10⁻¹ | Dezi | d |
| 10²⁷ | Ronna | R | 10⁻² | Zenti | c |
| 10²⁴ | Yotta | Y | 10⁻³ | Milli | m |
| 10²¹ | Zetta | Z | 10⁻⁶ | Mikro | µ |
| 10¹⁸ | Exa | E | 10⁻⁹ | Nano | n |
| 10¹⁵ | Peta | P | 10⁻¹² | Piko | p |
| 10¹² | Tera | T | 10⁻¹⁵ | Femto | f |
| 10⁹ | Giga | G | 10⁻¹⁸ | Atto | a |
| 10⁶ | Mega | M | 10⁻²¹ | Zepto | z |
| 10³ | Kilo | k | 10⁻²⁴ | Yocto | y |
| 10² | Hekto | h | 10⁻²⁷ | Ronto | r |
| 10¹ | Deka | da | 10⁻³⁰ | Quekto | q |

SI-Einheiten müssen exakt so geschrieben werden wie in Gesetz und Norm angegeben; zusätzliche Kennzeichen (z. B. Indizes) sind nicht gestattet.

---

#### Konventionen (A.1.2)

- Abkürzungen, Kennzeichnungen, Zahlen, mathematische Funktionen und physikalische Einheiten: Steilschrift (aufrecht)
- Skalare Grössen: kursiv (unabhängig davon, ob dimensionslos oder nicht)
- Vektoren: kursiv + fett; keine Pfeilschreibweise
- Tensoren: kommen nicht vor
- Physikalische Einheit einer Grösse G: eckige Klammern [G]; Zahlenwert: geschweifte Klammern {G}
- Differenzen physikalischer Grössen: Δ-Kennzeichnung
- Multiplikation physikalischer Einheiten oder skalarer Grössen: ohne eigenes Zeichen (Ausnahme: Zahlen + Zehnerpotenzen → Multiplikationspunkt "·")
- Skalarprodukt: grundsätzlich mit "·"
- Kreuzprodukt/Vektorprodukt: "×"
- Ableitungen: bevorzugt Leibnitz-Schreibweise (d/dt)
- Laufindizes: kursiv; Iterationsschritte (k-ter Schritt): kursiv, rechts unten
- Linearer Zusammenhang: "~"
- Zählpfeilgrössen: skalare Grössen mit Vorzeichen; Reihenfolge der Indizes legt Vorzeichen fest
- Amplituden von Wechselgrössen: Zirkumflex (û)
- Komplexe Grössen: unterstrichen; Betrag einer komplexen Zahl: nicht unterstrichen
- Konjugiert komplexe Grössen: Zeichen "*"
- Arithmetischer Mittelwert einer zeitabhängigen Grösse x: x̄ (Querstrich)
- Allgemeine zeitabhängige Grössen: kleingeschrieben; zeitunabhängige/konstante Grössen: grossgeschrieben
- Grossschreibung für absolute Grössen, Kleinschreibung für dimensionslose (pu-)Grössen

---

#### Formelzeichen (A.1.3) — vollständige Liste

**Griechische Buchstaben (Tab. A.5):**
α (alpha), β (beta), γ/Γ (gamma), δ/Δ (delta), ε/E (epsilon), ζ/Z (zeta), η/H (eta), θ/ϑ/Θ (theta), ι/I (jota), κ/K (kappa), λ/Λ (lambda), µ/M (my), ν/N (ny), ξ/Ξ (xi), o/O (omikron), π/Π (pi), ρ/P (rho), σ/Σ (sigma), τ/T (tau), υ/Υ (ypsilon), φ/ϕ/Φ (phi), χ/X (chi), ψ/Ψ (psi), ω/Ω (omega)

**Physikalische Grössen und Einheiten:**

| Zeichen | Bedeutung | SI-Einheit |
|---------|-----------|-----------|
| α | Winkel, Phasenanschnittswinkel, Schaltwinkel DSG | rad |
| αₙ | linearer Widerstandskoeffizient | K⁻¹ |
| βₙ | quadratischer Widerstandskoeffizient | K⁻² |
| δ | Luftspaltlänge EM / Verlustwinkel / Nullphasenwinkel Wechselspannung | m / rad |
| δE | Erdfehlerfaktor | 1 |
| ε | Permittivität | As/(Vm) |
| ε₀ | elektrische Feldkonstante ≈ 8,854 · 10⁻¹² As/(Vm) | F/m |
| εr | Dielektrizitätszahl | 1 |
| η | Wirkungsgrad | 100 % |
| ϑ | Temperatur | °C |
| θ | Winkel, Polradstellung DSG | rad |
| Θ | elektrische Durchflutung | A |
| κ | Faktor Stosskurzschlussstrom / spezifischer elektrischer Leitwert | 1 / S·m |
| λ | Wellenlänge / Leistungsfaktor / Faktor Dauerkurzschlussstrom / Eigenwert | m / 1 / s⁻¹ |
| Λm | magnetischer Leitwert | Vs/A = H |
| µ | Faktor Ausschaltwechselstrom / Permeabilität | 1 / Vs/(Am) |
| µ₀ | magnetische Feldkonstante = 4π · 10⁻⁷ Vs/(Am) | H/m |
| µr | Permeabilitätszahl | 1 |
| σ | Oberflächenladungsdichte | As/m² |
| τ | Zeitkonstante | s |
| φ | elektrisches Potenzial / Phasendifferenz φ = φu − φi | V / rad |
| φi | Nullphasenwinkel Wechselstrom | rad |
| φu | Nullphasenwinkel Wechselspannung | rad |
| Φ | magnetischer Fluss = Induktionsfluss | Wb = Vs |
| χe | elektrische Suszeptibilität | 1 |
| χm | magnetische Suszeptibilität | 1 |
| ω | Kreisfrequenz = Winkelgeschwindigkeit | s⁻¹ |
| a | Abstand, mittlerer Leiterabstand | m |
| a (Vektor) | Beschleunigung | m/s² |
| a, a² | Drehoperatoren | 1 |
| A | Fläche, Querschnittsfläche | m² |
| b | Zahl der Bündelleiter | 1 |
| B | Blindleitwert = Suszeptanz / Materialkonstante NTC | S |
| B (Vektor) | magnetische Flussdichte | T = Vs/m² |
| c | Ausbreitungsgeschwindigkeit Licht / Spannungsfaktor | m/s / 1 |
| c₀ | Vakuumlichtgeschwindigkeit | m/s |
| C | elektrische Kapazität | F = As/V |
| cosφ | Verschiebungsfaktor | 1 |
| D | Verzerrungsblindleistung D = Qd | Var |
| D (Vektor) | elektrische Erregung = dielektrische Verschiebung | As/m² |
| e | Elementarladung ≈ 1,602 · 10⁻¹⁹ C / relative Bestrahlungsstärke | C / 100 % |
| E | Bestrahlungsstärke = Strahlungsflussdichte / synchrone Spannung = Up/√3 | W/m² / V |
| E (Vektor) | elektrische Feldstärke | V/m |
| f | Frequenz | Hz |
| F | Kraft | N |
| g | Fallbeschleunigung ≈ 9,81 m/s² / Gleichzeitigkeitsfaktor | m/s² / 1 |
| gi | Grundschwingungsgehalt Strom | 1 |
| gu | Grundschwingungsgehalt Spannung | 1 |
| G | Wirkleitwert = Konduktanz | S = Ω⁻¹ |
| h | Höhe / Planksches Wirkungsquantum | m / J·s |
| H | magnetische Feldstärke | A/m |
| i = i(t) | elektrischer Strom (allgemein) | A |
| i | Übersetzungsverhältnis Getriebe | 1 |
| I | Gleichstromstärke, Effektivwert Wechselstrom | A |
| I (unterstrichen) | komplexer Effektivwert | A |
| j | imaginäre Einheit j = √−1 | 1 |
| j | elektrische Stromdichte | A/mm² |
| J | Betrag Massenträgheitsmoment / mittlere Stromdichte | kg·m² / A/mm² |
| k | Boltzmann-Konstante / K-Faktor DMS / Zahl Knoten / Kopplungsgrad Trafo | J/K / 1 |
| ki | Klirrfaktor Strom | 1 |
| ku | Klirrfaktor Spannung | 1 |
| KM | Maschinenleistungszahl | W·s |
| KN | Netzleistungszahl | W·s |
| l | Länge | m |
| L | Induktivität, Selbstinduktivität | H = Vs/A |
| m | Masse / Zahl Maschen / Phasenzahl / Faktor Wärmeeffekt DC-Anteil | kg / 1 |
| M | Gegeninduktivität | H = Vs/A |
| M (Vektor) | Drehmoment M = r × F / Magnetisierung | N·m / A/m |
| n | Drehzahl = Drehfrequenz | min⁻¹ |
| N | Windungszahl | 1 |
| p = p(t) | momentane Leistung | W |
| p | Polpaarzahl | 1 |
| pB(t) | momentane Blindleistung | W |
| pW(t) | momentane Wirkleistung | W |
| pe | elektrisches Dipolmoment | C·m |
| pm | magnetisches Dipolmoment | A·m² |
| P | elektrische Leistung Gleichstrom, Wirkleistung | W |
| P (Vektor) | elektrische Polarisation | As/m² |
| Q | elektrische Ladung / Güte / Blindleistung | C = As / 1 / Var |
| Qd | Verzerrungsblindleistung = D | Var |
| r | Radius / differenzieller Widerstand | m / Ω |
| R | elektrischer Widerstand, Wirkwiderstand | Ω |
| RH | Hall-Konstante | m³/C |
| Rm | magnetischer Widerstand | H⁻¹ = A/(Vs) |
| s | Schlupf Asynchronmaschine | 1 |
| sM | Statik Synchronmaschine | 1 |
| S | Scheinleistung | VA |
| S (unterstrichen) | komplexe Scheinleistung | VA |
| t | Zeit | s |
| T | Temperatur / Zeitkonstante | K / s⁻¹ |
| T (Vektor) | Drehmoment (torque) | N·m |
| TS | Transformationsmatrix symmetrische Komponenten | — |
| tanδ | Verlustfaktor | 1 |
| u = u(t) | elektrische Spannung (allgemein) | V |
| uk | relative Kurzschlussspannung | pu |
| U | Gleichspannung, Effektivwert Wechselspannung | V |
| U (unterstrichen) | komplexer Effektivwert | V |
| Up | Polradspannung | V |
| ü (unterstrichen) | komplexes Übersetzungsverhältnis | 1 |
| v | Geschwindigkeit | m/s |
| V | Volumen | m³ |
| W | Energie, Arbeit | J |
| xd | bezogene synchrone Reaktanz | pu |
| X | Reaktanz = Blindwiderstand | Ω |
| Xd | synchrone Reaktanz | Ω |
| Y | Scheinleitwert | S |
| Y (unterstrichen) | Admittanz = komplexer Leitwert | S |
| Z | Scheinwiderstand | Ω |
| Z (unterstrichen) | Impedanz = komplexer Widerstand | Ω |

---

#### Indizes (A.1.4)

Tiefer gestellte Indizes, die sich auf physikalische Grössen beziehen, sind kursiv (auch Laufindizes und Iterationszähler). Alle anderen Indizes steilschriftlich.

**Bedeutungskategorien (Tab. A.7):**
- Physikalische Grössen (kursiv): C, i, L, R, u — z. B. uR, φu
- Zustand: a, an, b, e, ist, k, n, nat, p, r, u — z. B. Pnat, Ir, Un
- Betriebsmittel: D, G, L, M, N, T — z. B. UN
- Bezugs- oder Fehlerstelle: E, F, N, OS, US, U, V, W — z. B. UOS
- Teil einer elektr. Maschine: 1, 2, 3, a, d, f, l, p, q, s — z. B. Ia, If

**Indexkonvention in der elektrischen Energietechnik:** kleiner Index = Zustand; grosser Index = Betriebsmittel oder Bezugs-/Fehlerstelle. Der Bemessungsbetrieb-Index N (nach DIN 1304 Teil 7 für elektr. Maschinen üblich) wird in diesem Buch nicht verwendet, um Verwechslungen zu vermeiden. Rotor der elektr. Maschine wird nicht mit r gekennzeichnet (Verwechslungsgefahr mit Bemessungsbetrieb). Stator Synchronmaschine: Index a; Stator Asynchronmaschine: Index s.

**Spezielle Index-Bedeutungen (Auswahl):**
- 0: Anfangswert / Leerlaufbetrieb / Nullsystem / Vakuum
- 1: OS-Seite Transformator / Mitsystem
- 2: US-Seite Transformator / Gegensystem
- 3: Tertiärseite Dreiwickler
- 35: Wert bei 35 °C
- δ: Verluste (Pδ = Pzu − Pab)
- Δ: Dreiecksgrösse / Differenz (z. B. I∆n = Nennfehlerstrom RCD)
- µ: Eisen/Magnetisierung (Iµ = Magnetisierungsstrom)
- σ: Streuung (X1σ = Streureaktanz)
- a: Anfahren der EM / Anker / Ausschaltwert
- A: Amperemeter / Anlage / Arbeitsmaschine
- ab: abgeführte/abgegebene Grösse
- ac: alternating current
- an: Anlaufen/Anfahren
- Al: Aluminium
- b: ungestörter Betrieb / Ausschalten (breaking)
- B: Berührung / Belastung / Betriebserdung / Bezugsgrösse / Blind-
- C: Coulomb / kapazitiv
- Cu: Kupfer
- d: Durchschlag / Verzerrung (distortio) / Längsachse
- D: Drosselspule / Durchlassstrom
- dc: direct current
- e: Elektron / Erdschluss/Erdfehler
- E: Erde/Bezugserde / Erder
- f: frei / Erregersystem (field)
- F: Fehlerstelle
- Fe: Eisen
- g: Lücke (gap)
- G: Getriebe / Generator
- h: Haupt-
- i: innen / induziert / elektrischer Strom
- J: Joule
- k: Kippen / Kurzschluss
- k1, k2, k2E, k3, kEE: ein-, zwei-, zweipolig mit Erde, dreipolig, Doppelerdschluss
- K: Kabel / Körper des Menschen / Knoten
- l: Läufer = Rotor
- L: Lorentz / Leiter / Leitung / Lichtbogen
- L: induktiv
- L1: Leiter im Drehstromnetz
- m: Messgrösse / magnetisch / mechanisch
- M: Motor / mechanisch
- max: maximal; min: minimal; mech: mechanisch
- n: Nennwert/Nominalwert; N: elektrisches Netz / Neutralleiter
- nat: natürlicher Betrieb
- OS: Oberspannungsseite
- p: Proton / polarisiert / Polrad / Stossspitze (peak)
- PE: Schutzleiter; PEN: Neutralleiter mit Schutzfunktion
- q: Quellen- / Querachse
- r: relativ / Bemessungsbetrieb
- R: zurückbleiben (remanere) / ohmsch; RES: restlich
- s: Schmelzen / synchroner Betrieb / Stator
- S: Sprung / Schritt / Sättigung / symmetrische Komponenten
- sc: Kurzschluss (short circuit); soll: Sollwert; str: Strang
- th: thermisch
- T: Transformator / Turbine / Berührung (touch)
- u: elektrische Spannung; U: Anschluss U
- US: Unterspannungsseite
- V: Verbraucher / Voltmeter / Anschluss V
- W: Wirk- / Anschluss W
- Y: Sternpunkt
- zu: zugeführte Grösse

**Hochgestellte Indizes:**
- *: konjugiert komplex
- ': transformierte Grösse / längenbezogene Grösse / transiente Grössen
- '': subtransiente Grösse

**Reihenfolge der Indizes** (nach DIN 1304 Teil 3):
1. Komponentensystem (1, 2, 0)
2. Zustand (ggf. mit Suffix Kurzschlussart)
3. Betriebsmittel
4. Unterscheidung gleicher Betriebsmittel
5. Bezugsstelle (OS, US, HV, LV)

Bei elektrischen Maschinen (nach DIN 1304 Teil 7): 1. Teil der Maschine, 2. Zusätze (σ, h).

---

### Abkürzungsverzeichnis (A.1.5, S. 421–427)

Vollständige Liste der verwendeten Abkürzungen:

| Abkürzung | Bedeutung |
|-----------|-----------|
| ABB | Asea Brown Boveri Ltd |
| AC | Alternating Current |
| AG | Aktiengesellschaft |
| AGC | Automated Generation Control |
| AI / KI | Artificial Intelligence / Künstliche Intelligenz |
| AIS | Air Isolated Switchgear |
| ANSI | American National Standards Institute |
| AP | Arbeitspunkt |
| ARESS | Asynchronous Rotating Energy System Stabilizer |
| ASC | Advanced Series Compensation |
| ATP | Alternative Transient Program |
| AWE | Automatische Wiedereinschaltung |
| BDEW | Bundesverband der Energie- und Wasserwirtschaft e. V. |
| BET | Blockeigenbedarfstransformator |
| BMWK | Bundesministerium für Wirtschaft und Klimaschutz |
| BSD | Bildungs- und Servicezentrum GmbH in Dresden |
| BT | Blocktransformator oder Bipolar-Transistor |
| CA / SA | Contingency Analysis / Security Analysis |
| CBR | Circuit-Breaker incorporating Residual current protection |
| CEER | Council of European Energy Regulators |
| CEN | Comité Européen de Normalisation (Europ. Komitee für Normung) |
| CENELEC | Comité Européen de Normalisation Électrotechnique |
| CODATA | Committee on Data of the International Science Council |
| CT | Current Transformer |
| DAG | Drehstrom-Asynchrongenerator |
| DAM | Drehstrom-Asynchronmaschine |
| DC | Direct Current |
| DFT | Diskrete Fourier Transform |
| DIN | Deutsches Institut für Normung e. V. |
| DMS | Distribution Management System oder Dehnungsmessstreifen |
| DPF | Dispatcher Power Flow |
| DSG | Drehstrom-Synchrongenerator |
| DSM | Drehstrom-Synchronmaschine |
| DSO | Distribution System Operator = Verteilnetzbetreiber |
| E-STATCOM | Energy Static Synchronous Compensator |
| EAM | Energie aus der Mitte |
| EC | electronically commutated |
| EEG | Erneuerbare-Energien-Gesetz |
| EG | Europäische Gemeinschaft |
| EHV | Extra High Voltage |
| ELV | Extra Low Voltage |
| EM | Elektrische Maschine |
| EMS / PAS / HEO | Energy Management System / Power Application Software / Höhere Entscheidungs- und Optimierungsfunktionen |
| EMTP | Electromagnetic Transients Program |
| EMV | elektromagnetische Verträglichkeit |
| EN | Europäische Norm (CEN, CENELEC, ETSI) |
| ENTSO-E | European Network of Transmission System Operators for Electricity |
| EPR | Earth Potential Rise |
| ETSI | European Telecommunications Standards Institute |
| EU | Europäische Union |
| EZS | Erzeugerzählpfeilsystem |
| FACTS | Flexible AC Transmission Systems |
| FE | Functional Earth |
| FFT | Fast Fourier Transform |
| FI | F für Fehlerstrom, I für elektrische Stromstärke |
| FNN | Forum Netzbetrieb/Netztechnik im VDE |
| FSC | Fixed Series Capacitors |
| GIL | Gasisolierte Rohrleiter |
| GIS | Gas Isolated Switchgear |
| GMS | Generation Management System |
| GPS | Global Positioning System |
| GTO | Gate Turn-Off |
| GuD | Gas und Dampf |
| GWP | Global Warming Potential |
| HAK | Hausanschlusskasten |
| HGÜ / HVDC | Hochspannungs-Gleichstrom-Übertragung / High Voltage Direct Current |
| HH | Hochspannungs-Hochleistungs- |
| HOSPE | hochohmige Sternpunkterdung |
| HS | Hochspannung (72 kV < U ≤ 125 kV) |
| HTLS | High Temperature Low Sag |
| HTS | Hochtemperatur-Supraleiter |
| HV | High Voltage |
| HöS | Höchstspannung (U > 125 kV) |
| IC | International Cooling |
| IEC | International Electrotechnical Commission |
| IEEE | Institute of Electrical and Electronics Engineers |
| IGBT | Insulated-Gate Bipolar Transistor |
| IGC / IGCT | Integrated Gate-Commutated (Thyristor) |
| IM | International Mounting |
| IP | Internet Protocol oder International Protection |
| ISMS | Informationssicherheits-Managementsystem |
| ISO | International Organization for Standardization |
| IT | Informationstechnologie |
| KE | Kurzerdung |
| KNOSPE | kurzzeitige niederohmige Sternpunkterdung |
| KS | Kurzschluss |
| KU | Kurzunterbrechung |
| KVS | Kabelverteilerschrank |
| LB | Leitungsband |
| LDR | Light Dependent Resistor |
| LED | Light-Emitting Diode |
| LFC | Load Flow Calculation |
| LPIT | Low Power Instrument Transformer |
| LS | Leitungsschutz |
| LSC | Loss of Service Continuity |
| LV | Low Voltage |
| LVR | Line Voltage Regulator |
| MCB | Miniature Circuit Breaker |
| MRCD | Modular Residual Current protective Device |
| MS | Mittelspannung (1 kV < U ≤ 72 kV) |
| MSC | Mechanical Switched Condensator |
| MSCDN | Mechanical Switched Condensator with Damping Network |
| MSR | Mechanical Switched Reactor / Messen Steuern Regeln |
| MTS | Mixed Technology Substation |
| MV | Medium Voltage |
| NETOMAC | Network Torsion Machine Control |
| NH | Niederspannungs-Hochleistungs- |
| NOSPE | niederohmige Sternpunkterdung |
| NS | Niederspannung (U ≤ 1 kV) |
| NSD / SE | Network State Determination / State Estimation |
| NT | Netzkuppeltransformator |
| NTC / PTC | Negative / Positive Temperature Coefficient |
| OIP | Oil-Impregnated Paper |
| OLTC | On-Load Tap Changer |
| OPF | Optimal Power Flow |
| OS | Oberspannungsseite vom Transformator |
| OSPE | ohne Sternpunkterdung = isolierter Sternpunkt |
| OT | Ortsnetztransformator |
| PAR | Phase Angle Regulator |
| PE | Protective Earth |
| PEL | Protective Earth Line DC/AC |
| PELV | Protective Extra Low Voltage |
| PEM | Protective Earth Mid-Point DC |
| PEN | Protective Earth Neutral |
| PMU | Phase Measurement Unit |
| PQ | Power Quality |
| PST | Phasenschiebertransformator |
| PTB | Physikalisch-Technische Bundesanstalt |
| PV | Photovoltaik |
| RCBO | Residual current operated Circuit-Breaker with Overcurrent protection |
| RCCB | Residual Current operated Circuit-Breaker without overcurrent protection |
| RCD | Residual Current protective Device = FI-Schutzschalter |
| RCM | Residual Current Monitor |
| RESPE | Resonanz-Sternpunkterdung |
| RIP / RIS | Resin-Impregnated Paper / Resin Impregnated Synthetics |
| RMS / TRMS | Root Mean Square / True Root Mean Square |
| RONT | regelbarer Ortsnetztransformator |
| SCA | asymmetrische Kurzschlussanalyse |
| SCADA | Supervisory Control and Data Acquisition |
| SCESS | Super Capacitor Energy Storage System |
| SCL | Substation Configuration Language |
| SELV | Safety Extra Low Voltage |
| SI | Système International d'unités = Internationales Einheitensystem |
| SLS | Selektiver Leitungsschutzschalter |
| SPMS | Synchronized Phase Measurement System |
| SPS | Synchrophasor System |
| SSR | Sub-Synchronous Resonance |
| SSSC | Static Synchronous Series Compensator |
| STATCOM | Static Synchronous Compensator |
| SVC | Static Var Compensator |
| TAB | Technische Anschlussbedingungen |
| TCR | Thyristor Controlled Reactor |
| TCSC | Thyristor Controlled Series Capacitor |
| TCSR | Thyristor Controlled Series Reactor |
| THDC | Total Harmonic Distortion Current |
| TRV | Transient Recovery Voltage |
| TSC | Thyristor Switched Capacitor |
| TSO / ÜNB | Transmission System Operator / Übertragungsnetzbetreiber |
| TSSC | Thyristor-Switched Series Capacitor |
| UC | Thermal Unit Commitment |
| UHV / UHVDC | Ultra High Voltage / Ultra High Voltage Direct Current |
| UMZ | unabhängiger Maximalstromzeitschutz |
| UPFC | Unified Power Flow Controller |
| US | Unterspannungsseite vom Transformator |
| USV | unterbrechungsfreie Stromversorgung |
| VB | Valenzband |
| VDE | Verband der Elektrotechnik Elektronik Informationstechnik e. V. |
| VDEW | Verband der Elektrizitätswirtschaft |
| VDN | Verein der Netzbetreiber e. V. beim VDEW |
| VDR | Voltage Dependent Resistor |
| VFD | Variable Frequency Drive |
| VIU | Vakuum Interrupter Unit |
| VNB | Verteilnetzbetreiber |
| VSC | Voltage Source Converter |
| VT | Voltage Transformer / Verteiltransformator |
| VZS | Verbraucherzählpfeilsystem |
| WAMS | Wide Area Monitoring System |
| WKA | Windkraftanlage |
| XML | Extensible Markup Language |
| ZEP | zentraler Erdungspunkt |
| ZVEI | Zentralverband Elektrotechnik- und Elektronikindustrie e. V. |

---

### Anhang A.2 — Normen und ergänzendes Material (S. 428–432)

#### Normen für elektrische Maschinen (Tab. A.2.1)

| IEC-Norm | DIN-Norm | VDE-Norm | Inhalt |
|----------|----------|----------|--------|
| IEC 38 | DIN IEC 38 | — | Normspannungen |
| IEC 60076 | DIN EN 60076 | VDE 0532 | Leistungstransformatoren |
| IEC 34-1 / IEC 85 | DIN EN 60034-1 | VDE 0530-1 | Drehende elektrische Maschinen, allgemeine Bestimmungen |
| IEC 34-6 | DIN EN 60034-6 | VDE 0530-6 | Kühlverfahren, IC-Code |
| IEC 34-8 | DIN EN 60034-8 | VDE 0530-8 | Anschlussbedingungen und Drehsinn |
| IEC 34-9 | DIN EN 60034-9 | VDE 0530-9 | Geräuschemissionen, Grenzwerte |
| IEC 34-12 | DIN EN 60034-12 | VDE 0530-12 | Anlaufverhalten von Käfigläufermotoren |
| IEC 34-7 | DIN IEC 34-7 | — | IM-Code, Bauformen umlaufender Maschinen |
| IEC 72 | DIN 42673 | — | IM-Code, Anbaumasse und Leistungszuordnungen bei IM B3 |
| IEC 72 | DIN 42677 | — | IM-Code, Anbaumasse für IM B5, IM B10, IM B14 |
| IEC 79-0 | DIN EN 50014 | VDE 0170/0171-1 | Explosionsschutz, allgemeine Bestimmungen |
| IEC 79-1 | DIN EN 50018 | VDE 0170/0171-5 | Explosionsschutz, druckfeste Kapselung "d" |
| IEC 79-7 | DIN EN 50019 | VDE 0170/0171-6 | Explosionsschutz, erhöhte Sicherheit "e" |
| IEC 60529 / IEC 34-5 | DIN EN 60529 / DIN VDE 0470 | — | IP-Code, Schutz gegen Berühren und Wasser |

#### Leistungsschild drehender elektrischer Maschinen (nach EN 60034-1, Abb. A.1)

Pflichtfelder des Leistungsschilds:
- Feld 1: Hersteller/Firmenzeichen
- Feld 2: Typ/Bezeichnung der Maschine
- Feld 3: Stromart mit Schaltzeichen nach DIN 40710 (Gleichstrom: –; Einphasen-WS: 1~; Zweiphasen-WS: 2~; Dreiphasen-WS: 3~; Sechsphasen-WS: 6~; Mischstrom: ~)
- Feld 4: Fertigungsnummer/sonstige Kennzeichen
- Feld 5: Schaltart der Wicklung bei Wechselstrommaschinen
- Feld 6: Bemessungsspannung (V)
- Feld 7: Bemessungsstrom (A)
- Feld 8: Bemessungsleistung (kW/W für Motoren, Gleichstrom- und Induktionsgeneratoren; kVA für Synchrongeneratoren und Blindleistungsmaschinen)
- Feld 9: Einheit der Leistung
- Feld 10: Bemessungsbetriebsart (Dauerbetrieb S1: kein Vermerk)
- Feld 11: Leistungsfaktor cosφ (bei Synchron- und Blindleistungsmaschinen, die Blindleistung aufnehmen sollen: Zusatz "u" für untererregt)
- Feld 12: Erregerspannung/Läuferstillstandsspannung (je nach Maschinentyp: Gleichstrommaschinen = Bemessungserregerspannung bei Fremderregung; Synchronmaschinen = Bemessungserregerspannung; Induktionsmaschinen mit Schleifringläufer = Läuferstillstandsspannung)
- Feld 13: Drehrichtung auf Antriebsseite gesehen (Rechtslauf →, Linkslauf ←)
- Feld 14: Bemessungsdrehzahl und ggf. zulässige Überdrehzahl/Schleuderdrehzahl; bei Motoren mit Drehzahleinstellung zulässige Höchstdrehzahlen; bei Getriebemotoren: Bemessungsdrehzahl n1 des Motors und Enddrehzahl n2 des Getriebes
- Feld 15: Bemessungsfrequenz bei Wechselstrommaschinen (Hz)
- Feld 16: Erregung (Abk. "Err") bei Gleichstrommaschinen/Synchronmaschinen/Einanker-Umformern; Läufer ("Lfr") bei Asynchronmaschinen
- Feld 17: Schaltart der Läuferwicklung (wenn keine Dreiphasenschaltung)
- Feld 18: Erregerstrom/Läuferstrom bei Bemessungsbetrieb (je nach Maschinentyp)
- Feld 19: Wärmeklasse (Kennbuchstaben Y, A, E, B, F, H, C) oder Grenz-Übertemperatur
- Feld 20: Schutzart nach IP-Code (DIN 40050)
- Feld 21: angenähertes Gewicht in t (nur wenn Gesamtgewicht > 1 t)
- Feld 22+23: Zusätzliche Vermerke (z. B. VDE 0530/… mit Jahreszahl)

#### Kühlverfahren IC-Code (nach EN 60034-6, Tab. A.12)

| Kennziffer | Bedeutung |
|-----------|-----------|
| Erste Kennziffer 0 | Maschine mit freiem Luftein- und -austritt |
| Erste Kennziffer 4 | oberflächengekühlte Maschine, Kühlmittel Umgebungsluft |
| Zweite Kennziffer 0 | Selbstkühlung |
| Zweite Kennziffer 1 | Eigenkühlung |
| Zweite Kennziffer 6 | Fremdkühlung durch angebaute Belüftungseinrichtung (unabhängig von der Maschine) |

#### Schutzarten IP-Code (nach DIN EN 60529 / VDE 0470, Tab. A.13)

| Ziffer | Berührungsschutz (Personen) | Schutz gegen Fremdkörper | Wasserschutz |
|--------|---------------------------|--------------------------|--------------|
| 0 | kein Schutz | kein Schutz | kein Schutz |
| 1 | Handrücken | ≥ 50 mm Durchmesser | senkrecht tropfendes Wasser |
| 2 | Finger | ≥ 12,5 mm Durchmesser | schräg (15°) tropfendes Wasser |
| 3 | Werkzeuge | ≥ 2,5 mm Durchmesser | Sprühwasser schräg bis 60° |
| 4 | Draht | ≥ 1,0 mm Durchmesser | Spritzwasser aus allen Richtungen |
| 5 | Draht | staubgeschützt | Strahlwasser |
| 6 | Draht | staubdicht | starkes Strahlwasser |
| 7 | — | — | zeitweiliges Untertauchen in Wasser |
| 8 | — | — | dauerndes Untertauchen in Wasser (5 bar) |

#### Normen für elektrische Energietechnik (S. 440, Tab. A.2.1 Forts.)

| IEC-Norm | VDE-Norm | Inhalt |
|----------|----------|--------|
| IEC 60038 | VDE 0175-1 | CENELEC-Normspannungen |
| IEC 60051 ff | DIN EN 60051 ff | direkt wirkend anzeigende analoge elektrische Messgeräte |
| IEC 60071-1 | VDE 0111-1 | Isolationskoordination — Begriffe, Grundsätze, Anforderungen |
| IEC 60076-1 | VDE 0532-76-1 | Leistungstransformatoren — Allgemeines |
| IEC 60076-2 | VDE 0532-76-2 | Leistungstransformatoren — Übertemperaturen (flüssigkeitsgefüllt) |
| IEC 60076-3 | VDE 0532-76-3 | Leistungstransformatoren — Isolationspegel, Spannungsprüfungen, Abstände in Luft |
| IEC 60076-5 | VDE 0532-76-5 | Leistungstransformatoren — Kurzschlussfestigkeit |
| IEC 60076-7 | VDE 0532-76-7 | Leistungstransformatoren — Belastung ölgefüllter Transformatoren |
| IEC 60076-10 | VDE 0532-76-10 | Leistungstransformatoren — Geräuschpegel |
| IEC 60076-11 | VDE 0532-76-11 | Leistungstransformatoren — Trockentransformatoren |
| IEC 60076-20 | VDE 0532-76-20 | Leistungstransformatoren — Energieeffizienz |
| IEC 60146-1-1 | VDE 0558-11 | Halbleiter-Stromrichter — Allgemeine Anforderungen und netzgeführte Stromrichter |
| IEC 60255-1 | VDE 0435-300 | Messrelais und Schutzeinrichtungen — Allgemeine Anforderungen |
| IEC 60269-1 | VDE 0636-1 | Niederspannungssicherungen — Allgemeine Anforderungen |
| IEC 60269-2 | VDE 0636-2 | Niederspannungssicherungen — Anforderungen für Elektrofachkräfte (industrieller Gebrauch) |
| IEC 60282-1 | VDE 0670-4 | Hochspannungssicherungen — strombegrenzende Sicherungen |
| IEC 60287-1-1 | — | Elektrische Kabel — Strombelastbarkeitsberechnung (100%-Lastfaktor), Verluste |
| IEC 60287-3-2 | — | Elektrische Kabel — ökonomische Optimierung der Leiterquerschnitte |
| IEC 60364 | VDE 0100 | Errichten von Niederspannungsanlagen |
| IEC 60364-1 | VDE 0100-100 | Niederspannungsanlagen — Allgemeine Grundsätze, Merkmale, Begriffe |
| IEC 60364-4-41 | VDE 0100-410 | Niederspannungsanlagen — Schutz gegen elektrischen Schlag |
| IEC 60364-4-42 | VDE 0100-420 | Starkstromanlagen bis 1000 V — Schutz gegen thermische Auswirkungen |

---

### Anlaufströme bei Drehstrom-Asynchronmaschinen (Abb. A.2, S. 431)

- Abgebildet werden Anlaufströmverläufe einer vierpoligen DAM in drei Schaltungsarten (Leerlauf):
  - Stern-Schaltung: Einschaltvorgang, Zeitachse 0–2 s, Stromamplitude ±15 A
  - Dreieck-Schaltung: Einschaltvorgang, Zeitachse 0–2 s, Stromamplitude ±15 A
  - Manuelle Stern-Dreieck-Umschaltung: Zeitachse 0–2 s, Umschaltzeitpunkt sichtbar, Amplitude ±15 A
- Der Vergleich zeigt die unterschiedlichen Anlaufstromspitzen der drei Varianten und den Einschwingvorgang beim Umschalten (Quelle: Florian Segger, 10.01.2020).
