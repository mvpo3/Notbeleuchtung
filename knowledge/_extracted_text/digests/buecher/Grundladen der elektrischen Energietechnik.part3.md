# Grundladen der elektrischen Energietechnik — Teil 3
> Quelle: Grundladen der elektrischen Energietechnik (buecher) · Seiten 121-160.

Dieser Teil schliesst Kapitel 1 (Grundlagen der Elektrotechnik) mit den Drehstrom-Leistungsformeln und dem Literaturverzeichnis ab, und eroeffnet Kapitel 2 (Elektrische Maschinen) mit Leistungstransformatoren und dem Einstieg in die Drehstrom-Asynchronmaschine.

## Inhalt

### 1.5 Drehstrom — Experimentelle Verschaltungen (Seiten 121–123)

Drei Versuchsaufbauten am 400-V-Drehstromnetz werden durchgespielt; je zwei in Reihe geschaltete Gluehbirnen bilden die Straenge. Das Netz verhalt sich starr (Ortsnetztransformator-Scheinleistung >> Lastleistung), deshalb bleiben Leiter- und Leiter-Erd-Spannungen konstant.

**Sternschaltung mit isoliertem Sternpunkt**
- Symmetrische Belastung: Strangspannungen je 230 V, Strangstroeme je ca. 123 mA; Knotengleichung I1+I2+I3 = 0
- Unterbrechung eines Strangs (I1 = 0): Leiterspannung U23 treibt Strom durch die beiden verbleibenden Straenge in Reihe; Strangspannung an diesen je 200 V
- Der Sternpunkt Y verschiebt sich; Strangspannung am offenen Strang steigt auf 346 V (= cos30° · U = Leiterspannung); demonstriert asymmetrische Belastung bei symmetrischer Spannungsquelle

**Sternschaltung mit Neutralleiter**
- Anschluss des Neutralleiters haelt alle drei Strangspannungen auf 230 V fest, unabhaengig davon ob ein Strang unterbrochen ist
- Bei Unterbrechung von Strang 1: I2 = I3 = 123 mA bleiben, IN = 123 mA (Kirchhoffsche Knotenregel: I1+I2+I3+IN = 0)
- Schlussfolgerung: Neutralleiter ist zwingend erforderlich, wenn einphasige Verbraucher am Drehstromnetz mit konstanten Steckdosenspannungen betrieben werden sollen

**Dreieckschaltung**
- Symmetrische Belastung: Strangstroeme ca. 163 mA, Leiterstroeome ca. 283 mA
- Verhaeltnis Leiterstrom zu Strangstrom: I/Istr = 2·cos30° = √3
- Unterbrechung eines Strangs: zwei Leiterstroeome entsprechen dann direkt den verbleibenden Strangstroemen

---

### 1.5.3 Symmetrischer Betrieb und elektrische Leistung (Seiten 123–128)

**Bedingungen fuer symmetrischen Betrieb**
Zwei Voraussetzungen muessen gleichzeitig erfuellt sein:
1. Symmetrisches Spannungssystem: alle drei Aussenleiter-Effektivwerte gleich, Phasenverschiebungen je 120°
2. Symmetrische Betriebsmittel (Transformatoren, Leitungen) und symmetrische Verbraucher — Impedanzen in allen drei Straengen identisch

Im symmetrischen Betrieb gilt:
- U12 = U23 = U31 = U (Leiterspannung)
- U1 = U2 = U3 = U/√3 (Strangspannung)
- I1 = I2 = I3 = I (Leiterstrom)
- IN = 0 (Neutralleiterstrom Null)

Das stationaere Verhalten laesst sich durch ein einphasiges Ersatzschaltbild darstellen, in dem Strom = Leiterstrom, Spannung = U/√3, Impedanz = Verbraucherimpedanz in Sternschaltung. Umsetzung im Ersatzschaltbild: P/3, Q/3, S/3 (je ein Drittel der Gesamtleistungen).

Gilt im Normalbetrieb fuer fast alle Hochspannungsnetze; Ausnahmen: Niederspannungsnetze mit unterschiedlichen Stroemstaerken in den Leitern, Erdschluss im 10-kV-Kabelnetz.

**Wirkleistung, Blindleistung, Scheinleistung**

Momentanleistung eines einzelnen Strangs:
- pstr(t) = pWstr(t) + pBstr(t)
- Wirkanteil: Pstr = Ustr·Istr·cosφ
- Blindanteil: Qstr = Ustr·Istr·sinφ

Gesamtleistung des Drehstromverbrauchers = Summe der drei Strangleistungen. Entscheidende Eigenschaft: Die momentanen Blindleistungen der drei Straenge heben sich zu jedem Zeitpunkt gegenseitig auf (pB1+pB2+pB3 = 0). Daraus folgt, dass die Gesamtleistung p(t) = pW1(t)+pW2(t)+pW3(t) im symmetrischen Betrieb zu jedem Zeitpunkt konstant ist.

Bedeutung fuer die Praxis: Einphasige Wechselstromverbraucher erzeugen eine Leistungspendelung mit doppelter Netzfrequenz, die Generatoren und Turbinen periodisch belastet. Drehstrom-Synchrongeneratoren arbeiten dagegen mit konstantem Drehmoment, solange die Netzfrequenz exakt auf 50 Hz geregelt wird. Das ermoeglicht den Einsatz hocheffizienter Dampf- und Gasturbinen.

Gesamte Wirkleistung (gilt fuer Stern- und Dreieckschaltung gleichermassen):
- P = √3 · U · I · cosφ

Zusammenhang Stern/Dreieck bei Widerstandsstrae ngen:
- Sternschaltung: Ustr = U/√3, Istr = I
- Dreieckschaltung: Ustr = U, Istr = I/√3
- Leistungsverhaeltnis: PDreieck / PStern = 3 (bei gleicher Impedanz Z)

Blindleistung: Q = √3 · U · I · sinφ

Scheinleistung: S = √3 · U · I

Zusammenhang: S² = P² + Q², S = √(P²+Q²)

Komplexe Scheinleistung: S = P + jQ

Bei asymmetrischem Verbraucher (unterschiedliche Impedanzen in den Zweigen): Leistungen der Einzelstraenge addieren — S = U1·I1* + U2·I2* + U3·I3* = (P1+P2+P3) + j(Q1+Q2+Q3)

---

### Literaturverzeichnis Kapitel 1 (Seiten 128–137)

Verzeichnis der Quellen fuer Kapitel 1, umfasst Werke aus den Bereichen Grundlagen der Elektrotechnik (Albach, Bauckholt, Boeck, Buettner, Clausert, Fuehrer/Heidemann/Nerreter, Hagmann, Harriehausen/Schwarzenau, Hering, Howing, Karaali, Kories/Schmidt-Walter, Kral, Marinescu, Meier/Stubbe, Nelles, Nerreter, Paul/Paul, Philippow, Pregla, Scholz, Stiny/Poppe u.a.), Aufgabensammlungen, Formelsammlungen, Mess- und Materialtechnik sowie Energieversorgung. Ausserdem Web-Quellen (TransnetBW, RWE, Hitachi Energy, Stadtwerke Kiel, Siemens Energy) und Fachliteratur zu Power Quality, Netzrueckwirkungen, Supraleitung und Quantenmechanik.

---

### 2 Elektrische Maschinen — Einfuehrung (Seiten 138–139)

Kapitel 2 behandelt drei klassische Maschinentypen:
- **Leistungstransformatoren** (ruhende elektrische Maschinen, zusammen mit Drosselspulen)
- **Drehstrom-Asynchronmaschinen** (rotierende Maschine)
- **Drehstrom-Synchronmaschinen** (rotierende Maschine)

Begruendungen fuer die Relevanz:
- Transformatoren verbessern den Wirkungsgrad der Energieubertragung: Hochsetzen der Betriebsspannung reduziert bei gleicher Scheinleistung den Strom → geringere Stromwaermeverluste R·I²
- Elektrische Energie wird (ausser durch Photovoltaik) ausschliesslich mit rotierenden Maschinen erzeugt (Synchron- und Asynchrongeneratoren)
- Elektromotoren eroeffnen hohe Drehmomente aus dem Stillstand und praezise Automatisierung technischer Prozesse; Drehstrom-Asynchronmotoren sehr verbreitet

**Normen fuer elektrische Maschinen:**

| Norm | VDE-Nr. | Gegenstand |
|------|---------|-----------|
| DIN EN 60034 | VDE 0530 | Umlaufende elektrische Maschinen |
| DIN EN 60076 | VDE 0532 | Transformatoren und Drosselspulen |

**Kennzeichnungen nach DIN EN 50216:**

| Code | Bedeutung |
|------|-----------|
| IC-Code (International Cooling) | Kuehlverfahren, siehe Tab. A.12 |
| IM-Code (International Mounting) | Bauformen, Aufstellungsarten |
| IP-Code (International Protection) | Schutz gegen Eindringen fester Koerper und Wasser, siehe Tab. A.13 |

**Betriebsarten rotierender Maschinen:**

| Betriebsart | Index | Kenngroesse | Eigenschaft |
|-------------|-------|-------------|-------------|
| Stillstand | — | n = 0 | Pzu = Pab = 0 |
| Leerlauf | 0 | n0 = Leerlaufdrehzahl | Pab = 0, Pzu ≠ 0 (interne Verluste) |
| Bemessungsbetrieb | r (rated value) | Ir = Bemessungsstrom | maximale zul. elektr. Leistung ohne Beeintraechtigung |

Hinweis: Leerlauf bedeutet, die Maschine gibt keine mechanische Leistung ab (Pab = 0), nimmt aber wegen interner Verluste etwas elektrische Wirkleistung auf (Pzu ≠ 0).

Bemessungsbetrieb (frueher: Nennbetrieb) — maximale dauernd zulassige Beanspruchung ohne Funktionsbeeintraechtigung, gilt ebenso fuer ruhende Maschinen. Index r (rated) in diesem Buch durchgehend verwendet; Alternativ-Index N nach frueherer DIN 1304. Es gibt zehn Bemessungsbetriebsarten S1 bis S10 nach EN 60034-1 (S1 = Dauerbetrieb, S2 = Kurzzeitbetrieb, S3 = periodischer Aussetzbetrieb usw.).

Kenngroessen fuer Bemessungsbetrieb stehen auf dem Leistungsschild (Typenschild). Bei Transformatoren = Bemessungsscheinleistung (ans Netz abgegebene Scheinleistung); bei Motoren = mechanische Wirkleistung an der Welle. Positiver Drehsinn = Uhrzeigersinn bei Blick auf das freie Wellenende (Rechtslauf).

**Energiewandler-Typen:**
- Generatoren: mechanisch → elektrisch
- Leistungstransformatoren: elektrisch → elektrisch (Spannungsebene-Wandlung)
- Motoren: elektrisch → mechanisch (Rueckspeisung beim Bremsen = Nutzbremsen/Rekuperation)

Wirkungsgrad: η = Pab/Pzu = Pab/(Pab+Pδ) mit Verlusten Pδ = Pδe + Pδm

Elektrische Verluste: Pδe = PCu + PFe + PHl
- PCu = Kupfer-/Joule-/Ohmsche Verluste / Stromwaermeverluste
- PFe = Eisenverluste (Hysterese + Wirbelstrom)
- PHl = Halbleiterverluste (periodisches Schalten und Filtern)

Mechanische Verluste Pδm: Lagerreibung, Luefterverluste, evtl. Getriebe — entfallen bei ruhenden Maschinen.

Wirkungsgrad-Charakteristik: Maximum liegt bei 50–75 % der Bemessungsleistung, im Bemessungsbetrieb liegt er sehr nah am Maximum. Wachstumsgesetz: groessere Maschine = besserer Wirkungsgrad.

Richtwerte maximale Wirkungsgrade Elektromotoren:
- 1 W bis 100 W: η = 0,1 bis 0,5
- 1 kW bis 100 kW: η = 0,75 bis 0,85
- 500 kW bis 10 MW: η = 0,93 bis 0,96

Oekodesign-Verordnung EU: Leistungstransformatoren oberhalb 200 MVA → Wirkungsgrad > 99,5 %; Mittelspannungstransformatoren etwas darunter.

---

### 2.1 Leistungstransformatoren (Seiten 141–160)

Leistungstransformatoren werden in der Energietechnik haeufig als Umspanner bezeichnet. Sie bilden die senkrechten Verbindungen zwischen den Spannungsebenen im Netz.

**Einsatzgebiete und Bemessungsgroessen:**

| Ort | Bezeichnung | Bemessungsleistung (typisch) |
|-----|-------------|------------------------------|
| Kraftwerke | Maschinen-/Blocktransformator, Eigenbedarfs- und Anfahrtransformator | bis ca. 1500 MVA |
| Umspannwerke/Umspannstationen | Verteilertransformator | 25–63 MVA, 100–350 MVA |
| Netzstationen | Ortsnetztransformator | 100 kVA bis >2000 kVA |
| HGÜ-Stationen | HGÜ-Transformatoren | bis >2000 MVA |
| Phasenschieber | Phasenschiebertransformatoren | >2000 MVA |

Ortsnetztransformatoren sind vielfach standardisiert (100 kVA bis >2000 kVA). Blocktransformatoren bis ca. 1500 MVA. HGÜ-Transformatoren verbinden das Drehstromnetz mit Gleichstromleitungen.

**Anforderungen an Umspanner:**
- Verluste so gering wie moeglich
- Ertragen zeitweiliger Ueberbeanspruchungen ohne Eigenschaden
- Geringer Wartungsaufwand und niedrige Ausfallrate
- Hohe Lebensdauer (deutlich ueber 40 Jahre tatsaechlich erreichbar)
- Akzeptable Geraeuschentwicklung
- HGUe-Transformatoren: zusaetzlich Traegheit von Gleich- und Oberschwingungsstreoemen

**Voll- vs. Spartransformator:**
- Volltransformator: Wicklungen galvanisch getrennt; gesamte Leistung wird ueber magnetischen Kreis uebertragen
- Spartransformator: OS- und US-Wicklung teilen einen gemeinsamen Wicklungsteil (Parallelwicklung); nur ein Teil der Gesamtscheinleistung U1·I1 laeuft ueber den Magnetkreis → Material-, Gewichts- und Kostenersparnis
- Spartransformatoren nur sinnvoll, wenn beide Spannungsebenen nah beieinander liegen
- Nachteil Spartransformator: Stoerspannungsverlagerungen von der OS-Seite koennen sich auf die US-Seite uebertragen → deshalb nur zur Kupplung von Netzen mit niederohmiger Sternpunkterdung zugelassen
- Offshore-Windparks (z.B. 155 kV/33 kV — Spannungsebenen weit auseinander): dort Volltransformatoren

Einphasige Zweiwicklungstransformatoren: bei der Deutschen Bahn oder als HGUe-Transformatoren. Im Drehstromnetz meist dreiphasige Volltransformatoren. Bei sehr grossen Leistungen: drei einphasige Trafos zur Drehstrom-Transformatorbank zusammengeschaltet (Wicklungen dann jeweils im Stern).

**Wicklungsaufbau:**
- OS-Wicklung: hoehere Windungszahl, kleiner Leiterquerschnitt
- US-Wicklung: kleine Windungszahl, groessere Leiterquerschnitte
- Indexierung: OS-Seite Index 1, US-Seite Index 2; Wicklungsenden mit nachfolgender 1 oder 2 (z.B. 1U1, 1U2)
- Dreiwicklungstransformatoren: dritte Wicklung fuer Anschluss weiterer Spannungsebene, Eigenbedarf, Kompensationsdrosselspule oder Ausgleichswicklung (Dreieck-Tertiärwicklung)

---

### 2.1.1 Aufbau von Leistungstransformatoren (Seiten 144–148)

**Aktive Teile:**
- Wicklungen (Kupfer, bei kleineren Trafos Aluminium)
- Eisenkern
- Feststoffisolierung aus Zellulose

**Oelisolierung (Oeltransformator):**
- Kessel aus Stahlblech, gefuellt mit Isolier- und Kuehloel
- Meistens hochraffiniertes Mineraloel; alternativ Silikonoel (nicht brennbar) oder Ester (schwer brennbar)
- Vollsynthetisches Oel auf Erdgasbasis: verlaengerte Oellebensdauer, seit ca. 10 Jahren auch bei Grosstransformatoren
- Pflanzenoele (Raps, Soja, Sonnenblumen) ebenfalls moeglich
- Maximal zulaessige Temperatur Mineraloel: 100 °C im Normalbetrieb; bis 115 °C in Ueberlast nach DIN EN 60076-7
- Empfehlung: fuer lange Lebensdauer deutlich unter 100 °C bleiben
- Kuehlsysteme: passive und aktive Kuehler, Ventilatoren, Umwaelzpumpen bei Grosstransformatoren
- Hoeher- und Hochspannungsebene: ausschliesslich Oeltransformatoren
- Mittelspannungsebene: in brandsensitiven Anlagen oder aus Umweltschutzgruenden Giessharztransformatoren bis ca. 40 MVA oder seltener SF6-Ausfuehrungen

**Feuchtekontrolle:** Feststoffisolierung muss trocken bleiben → Trockenoefen; Fertigungsprozess: aktive Teile bis zu 2 Wochen im Vakuum getrocknet.

**Eisenkern:**
- Aufgebaut aus bis zu 30 000 Einzelblechen
- Blechdicke bei grossen Leistungstransformatoren: 0,2 bis 0,23 mm
- Einzelbleche gegeneinander elektrisch isoliert (fruehher Papier/Lack; heute duenne Silikat-Phosphatschicht beim Auswalzen) → bis zu 8000 Schichten uebereinander
- Material: weichmagnetische Eisen-Silizium-Legierungen (schmaale Hysterese → geringe Ummagnetisierungsverluste)
- Grosse Transformatoren: Kuehlkanaele erforderlich; Bleche werden bandagiert (Geraeuschminderung); optional akustische Daemmplatten am Gehaeuse

Bauformen:
- Kerntransformator: alle Schenkel bewickelt
- Manteltransformator: unbewickelte Schenkel vorhanden
- Joch = waagerechte Segmente des Eisenkerns, Schenkel = senkrechte Segmente
- Drehstromtransformatoren meist unsymmetrisch; symmetrische Ausfuehrung selten
- Bei kleineren Leistungen: 3-Schenkel-Bauform
- Bei groesseren Leistungen: 5-Schenkel-Bauform (kleinere Jochquerschnitte → Transport mit Bahn moeglich; zulaessige Hoehe Bahnprofil = 4,65 m ueber Schienenoberkante)
- Transport begrenzt auf ca. 600 t ohne Oel (Oel wird erst am Aufstellungsort eingebuellt); Kernmassen bis 300 t, Wicklungsmassen bis 70 t
- Kompakte Drehstromtransformatoren bis ca. 1000 MVA; darueber hinaus: drei einphasige Einzeltransformatoren lieferbar und vor Ort zu Bank verschaltet

**Wicklungen:**
- Zylinderwicklung, konzentrisch um Schenkel; US-Wicklung innen, OS-Wicklung aussen (Isolationsgruenden)
- Bis ca. 120 kV: Lagenwicklungen (preisguestiger); ab hoehere Spannungen: Scheibenspulenwicklungen
- Kleine Stroeme: papierisolierte Einfachleiter
- Grosse Stroeme: Drillleiter (lackisolierte Teilleiter mit wechselnden Positionen im Buendel → Stromstaerken werden gemittelt, Skineffekte reduziert)
- Wicklungen mit Druckringen zusammengepresst (Radialkraefte bei Kurzschlussstreoemen koennen stark sein; Scheiben und Lagen duerfen ihre Position nicht aendern)
- Durchfuehrungen: Isolation durch das geerdete Gehaeuse; Schirmringe zur Feldsteuerung; homogenes E-Feld angestrebt
- Isolationsarten Durchfuehrungen: OIP (oelimpraegtiertes Papier mit Porzellan), RIP (harzimpraegniertes Papier), RIS (harzimpraegniertes Kunststoffvlies) mit Silikon-Verbundisolatoren

---

### 2.1.2 Elektrische Eigenschaften von Drehstromtransformatoren (Seiten 139–150)

**Bemessungsuebersetzung:**
Der Bemessungsuebersetzungsverhaeltnis ür eines Drehstromtransformators ist das Verhaeltnis der Aussenleiterspannungen im Leerlauf:
- ür = U1UV / U2UV = U1VW / U2VW = U1WU / U2WU

Im Betrieb ergibt sich ein belastungsabhaengiger interner Spannungsfall; hier wird vereinfachend konstante Uebersetzung angenommen.

**Schaltgruppen:**
Wicklungsstrange koennen im Stern (Y/y), Dreieck (D/d) oder Zickzack (Z/z) verschaltet werden; Sternpunkt kann herausgefuehrt werden.

Kennzeichnung nach EN 60076 (fruehher VDE 0532):
- Erster Buchstabe gross = Oberspannungsseite
- Zweiter Buchstabe klein = Unterspannungsseite

Kennbuchstaben nach EN 60076-1:

| Symbol | Bedeutung |
|--------|-----------|
| Y, y | Sternschaltung |
| D, d | Dreieckschaltung |
| Z, z | Zickzackschaltung |
| N, n | Sternpunkt herausgefuehrt |
| a | Spartransformator |
| III, iii | unverschaltet |

Kennzahl k ∈ {0, 5, 6, 11}: Vielfaches von 30°, um das die US-Zeiger den OS-Zeigern nacheilen. Faktor: e^(jk·30°). Beispiel Yd11: k=11, Nachlauf = 11 × 30° = 330°; komplexe Uebersetzung ü = (√3 · N1/N2) · e^(j330°).

Insgesamt 12 Schaltgruppen:

| k | Schaltgruppen |
|---|--------------|
| 0 | Dd0, Yy0, Dz0 |
| 5 | Dy5, Yd5, Yz5 |
| 6 | Dd6, Yy6, Dz6 |
| 11 | Dy11, Yd11, Yz11 |

In Deutschland bevorzugte Schaltgruppen:
- Blocktransformatoren: YNd5
- Netzkupplungstransformatoren: meist YNyn0
- Verteilertransformatoren: YNyn0 und YNd5
- Ortsnetztransformatoren: meist Dyn5

Wahl der Verschaltungsart:
- Hohe Spannungen → Sternschaltung bevorzugt: Isolation nur fuer 1/√3-fache Aussenleiterspannung noetig
- Hohe Stroeme → Dreieckschaltung vorteilhaft: Wicklungsstrang traegt nur 1/√3-fachen Aussenleiterstrom → kleinere Leiterquerschnitte moeglich
- Unterhalb 30 kV: Kupfereinsparung durch Dreieck vorteilhafter als Isolationseinsparung durch Stern

**Sternpunktbelastbarkeit:** Faehigkeit, den Bemessungsstrom der Wicklung dauerhaft im Sternpunkt zu fuehren. Erforderlich bei:
- Einphasiger Einspeisung oder Last im NS-Netz
- Anschluss einer Erdschluessloeschspule
- Niederohmiger Erdung des Sternpunkts

Bei unsymmetrischer Belastung (NS-Netz mit zufaellig eingeschalteten Einphasigverbrauchern und Erzeugern) sind nur Schaltgruppen mit 100 % belastbarem sekundaerseitigem Sternpunkt zulaessig: Dyn5, Dyn11, Dzn0, Yzn5, YNzn5. In Deutschland hauptsaechlich Yzn5 und Dyn5. Yzn5 wurden in den 1960er und fruehen 1970er Jahren verbaut (Bemessungsscheinleistung bis 200 kVA), sind aber wegen hoeherer Kosten und groesserer Verluste nicht mehr im Neueinsatz.

**Ausgleichswicklungen (Tertiärwicklungen):**
Im Dreieck verschaltete Tertiärwicklungen ohne herausgefuehrte Anschluesse → Kennzeichnung als z.B. YNyn0+d. Im HS/MS-Bereich haeufig, bei Ortsnetztransformatoren selten. Vorteil: In erdschlusskompensierte Netzen koennen damit groessere Erdschlussspulen eingebaut werden (ohne Ausgleichswicklung: Spule nur bis 30 % des Bemessungsstroms des Umspanners tragfaehig). Falls Tertiärwicklung als Leistungswicklung ausgefuehrt: z.B. Schaltgruppe YNyn0d5.

**Netz-Schaltgruppen-Uebersicht** (Versorgungnetz nach Abb. 2.17):
- Blocktransformator (BT): YNd5, 300–400 MVA
- Blockeigenbedarfstransformator (BET): YNdd, 100–350 MVA
- Netzkuppeltransformator (NT): YNyn0 (YNyn0+d), 600–715 MVA
- Verteilertransformator (VT): YNyn0, YNd5, 25–63 MVA
- Ortsnetztransformator (OT): Dyn5, Yzn5, 250/400/630/1000/1600 kVA

**Parallelschaltung von Umspannern — Bedingungen:**
- Identische Bemessungsspannungen, -frequenz und Uebersetzungsverhaeltnis
- Gleiche Schaltgruppen (Ausnahme: Kennzahlen 5 und 11 koennen kombiniert werden, wenn an einem Transformator zwei Anschluesse getauscht werden)
- Relative Kurzschlussspannungen sollten um nicht mehr als 10 % vom Mittelwert abweichen (bei groesseren Abweichungen: Drosselspule vor dem Transformator mit kleinerer Kurzschlussspannung)
- Verhaeltnis der Bemessungsscheinleistungen nicht groesser als 3:1

**Ersatzschaltbild:**
Vollstaendiges T-Ersatzschaltbild des dreiphasigen Zweiwicklungstransformators enthaelt:
- Primaerseitig: R1 (Wicklungswiderstand), X1σ (Streuinduktivitaet)
- Querzweig: RFe (Eisenverluste), Xh (Hauptinduktivitaet)
- Sekundaerseitig (auf OS-Seite transformiert): R'2, X'2σ
- Transformation: I'2 = I2/ü, U'2 = ü·U2

Vereinfachtes Kurzschlussersatzschaltbild (Kappsches Ersatzschaltbild) fuer Leistungsfluss- und Kurzschlussstromberechnungen:
- Querzweig (RFe, Xh) entfaellt bei Volllast und Kurzschluss (Strom dominiert)
- Verbleibende Groessen: Rk = R1 + R'2, Xk = X1σ + X'2σ
- Kurzschlussimpedanz: Zk = Rk + jXk

**Relative Kurzschlussspannung uk:**
Wichtige Kenngrösse des Transformators. Dimensionslos, gibt maximalen relativen internen Spannungsfall (gemessen im Kurzschlussversuch) an:
- uk = U1k / U1r (Verhaeltnis Kurzschlussspannung zu Bemessungsspannung OS)
- uk entspricht der pu-Groesse (Per-Unit) zk = Zk · Sr / U²1r
- Hat Wirk- und Blindanteil: uk = √(u²R + u²X)
- uR = rk = Rk · Sr / U²1r
- uX = xk = Xk · Sr / U²1r
- Fuer grosse Umspanner gilt 1 % ≤ Rk/Xk ≤ 8 % → Wirkanteil vernachlaessigbar → uk ≈ xk

Richtwerte uk und uR fuer Drehstromtransformatoren nach Spannungsebene:

| U1r / kV | Sr / MVA | uk / % | uR / % |
|----------|----------|--------|--------|
| 6–20 | 0,1 | 3,5–8,8 | 2,1–2,8 |
| 30 | 0,5 | 6–8,8 | 1,6–1,8 |
| 60 | 1,25 | 7–10 | 1,4–1,5 |
| 110 | 3,15 | 10–12 | 1,0–1,2 |
| 220 | 10,0 | 11–14 | 0,72–0,86 |
| 400 | 31,5 | 15–17 | 0,54–0,66 |

Umspanner in Uebertragungsnetzen: hoehere uk-Werte bevorzugt (kleinere Kurzschlussstroeme), aber dadurch interner Spannungsfall bei Vollast bis zu 20 % der Bemessungsspannung.

**Stufenstellung und Leistungssteuerung:**

Windungsverhaeltnis N1/N2 kann in diskreten Stufen veraendert werden:

- **Umsteller (Off-circuit tap changer):** manuell, nur im spannungslosen Zustand; in konventionellen Ortsnetztransformatoren; Einstellung bei Inbetriebnahme, Anpassung bei Bedarf
- **Laststufenschalter OLTC (On-load tap changer):** Windungsverhältnis veränderbar unter Last, manuell oder automatisch geregelt; Verstellung bis ±22 % gegenueber Bemessungsubersetzung
- **Regelbare Ortsnetztransformatoren RONT:** mit Vakuumschaltern; im Zuge der Energiewende / Smart Grid eingesetzt

Arten der Spannungsregelung:

| Typ | Phasendifferenz ΔU | Wirkung |
|-----|-------------------|---------|
| Laengsregeltransformator | 0° | Nur Spannungsaenderung; veraendert Blindleistungen an Netzknoten |
| Schraegregeltransformator | ±30° oder ±60° | Spannungs- und Wirkleistungssteuerung; treibt Ringstreoeme auf parallelen Leitungen |
| Querregeltransformator / Phasenschieber (PST, PAR) | ±90° | Reine Wirkleistungssteuerung; seriell eingebunden; gleiche Spannungsebene auf beiden Seiten |

Phasenschiebertransformatoren koennen Engpaesse, Ueberlastung und Stoerfaelle auf parallelen Leitungen vermeiden. Moegliche Umkehr des Phasenwinkels durch Vorwaehler (Umdrehung der Zusatzspannung um 180°).

Neuartige Ausfuehrang: UPFC (Unified Power Flow Controller) — leistungselektronische Bauelemente statt gestufter Zusatztransformator; kontinuierliche Verstellung; ermoeglicht gleichzeitig serielle/parallele Blindleistungskompensation und Wirkleistungssteuerung ohne Schalten von Kondensatoren oder Drosselspulen.

---

### 2.2 Drehstrom-Asynchronmaschinen — Einfuehrung (Seiten 159–160)

Vorteile der Drehstrom-Asynchronmaschine (DAM):
- Keine Kohlebuersten, keine Kommutatorringe, keine Positionssensoren noetig → preisguestig
- Selbstanlaufend, wartungsarm, robust
- Weltweit schaetzungsweise ueber 50 % aller Antriebsmaschinen sind Drehstrom-Asynchronmotoren
- Hauptsaechlich in drehzahlstarren Antrieben; durch leistungsfaehige Wechselrichter auch in drehzahlvariablen Antrieben
- In Versorgungs- und Gebaeudetechnik bei kleinen und mittleren Leistungen zunehmend durch EC-Motoren verdraengt (hoeherer Dauerbetriebs-Wirkungsgrad)

Als Generator: in kleinen Wasserkraftanlagen und Windkraftanlagen (Konkurrenz zum Drehstrom-Synchrongenerator).

Leistungsklassen von Asynchronmotoren:

| Leistungsbereich | Stranganzahl | Spannung |
|-----------------|-------------|---------|
| 0,1 W bis 0,5 kW | einsträngig | 230 V |
| 0,5 kW bis 1 MW | dreistraengig | 400 V, 500 V, 690 V |
| 200 kW bis 15 MW | dreistraengig | 400 V, 500 V, 690 V, 3 kV, 6 kV |
