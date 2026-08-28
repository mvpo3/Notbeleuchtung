# Planung von Elektroanlagen — Teil 10
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 401-440.

Dieser Teil schließt das Kapitel Mittelspannungsanlagen mit einem vollständigen Rechenbeispiel zur Barwertmethode ab und behandelt dann Hochspannungsanlagen (Kap. 19), Sammelschienensysteme (Kap. 20) sowie Schalt- und Schutzgeräte sowohl für Mittel- als auch Niederspannung (Kap. 21) einschließlich der Selektivitätsprinzipien (Kap. 22).

## Inhalt

### 18.23.4 Rechenbeispiel Barwertmethode (Transformator-Wirtschaftlichkeit)

Gegebene Eingangsgrößen für die Berechnung:
- Zinssatz z = 8 %, Teuerungsrate = 3 %, Abzinsungsfaktor q = 1,05
- Betrachtungszeitraum t = 40 Jahre
- Jährlicher Lastanstieg g = 1,8 %, daraus Steigerungsfaktor s = (1 + g)² = 1,036
- Höchstleistung im ersten Betriebsjahr = 41 MVA
- Jährliche Arbeitsverlustkosten k = 0,175 Euro/kWh
- Jährliche Einschaltdauer Transformator TB = 8760 h, Lüfter TL = 1000 h
- Verlustfaktor = 0,725
- Zwei Transformatoren (n = 2), Bemessungsleistung 31,5/40 MVA
- Leerlaufverluste je Transformator: 15.000 W (beide Leistungsstufen gleich)
- Kurzschlussverluste je Transformator: 136.000 W (31,5 MVA) / 219.000 W (40 MVA)
- Lüfterverluste je Transformator: 1.900 W

**Barwertfaktoren:**
- Abzinsungsfaktor: q = 1 + (z/100 % − ε/100 %) = 1 + (8 % − 3 %) / 100 % = 1,05
- Barwertfaktor der Anlage ba = q^0 = 1 (Einmalzahlung zum Zeitpunkt t=0)
- Barwertfaktor gleich bleibender Verluste: bo = (q^t − 1) / (q^t × (q − 1)) = 17,16
- Barwertfaktor steigender Verluste: bk = ((s/q)^t − 1) / (s − q) = 23,08

**Gesamtbarwert Variante AV3:**
- Anlagekosten KA3 = 7.200.000 Euro → Barwert KA = 7.200.000 Euro
- Leerlauf- und Lüfterverlustkosten pro Jahr: Ko = n × TB × k × (PFe + PL × TL/TB)
  = 2 × 8760 h × 0,175 Euro/kWh × (15 kW + 1,9 kW × 1000/8760) = 46.655 Euro/a
- Barwert der Leerlauf- und Lüfterverlustkosten: K0 = bo × Ko = 17,16 × 46.655 Euro = 800.599 Euro
- Kurzschlussverlustkosten im ersten Jahr: Kk = TB × k × Verlustfaktor × PCu × (Smax1/SrT)²
  = 8760 h × 0,175 Euro/kWh × 0,575 × 219 kW × (37 MVA / 40 MVA)² = 104.130 Euro
- Barwert der steigenden Kurzschlussverluste: KK = bk × Kk = 23,08 × 104.130 Euro = 2.403.320 Euro
- Gesamtbarwert: K = KA + K0 + KK = 7.200.000 + 800.599 + 2.403.320 = **10.403.919 Euro**

**Entscheidung Lüfter-Beschaffungszeitpunkt:**
- Lüfterpreis bei Sofortlieferung mit Transformator: Kv = 50.000 Euro, 40.000 Euro oder 30.000 Euro
- Marktpreis bei späterer Beschaffung: KL = 75.000 Euro
- Optimaler Verzögerungszeitraum Δt = ln(KL/Kv) / ln(q):
  - Kv = 50.000 Euro → Δt = 8,3 Jahre
  - Kv = 40.000 Euro → Δt = 12,88 Jahre
  - Kv = 30.000 Euro → Δt = 18,78 Jahre
- Schlussfolgerung: Lüfter erst später kaufen, wenn Transformator die Bemessungsleistung innerhalb der berechneten Zeit nicht erreicht

**Einspeisekabelbemessung:**
- Transformatornennstrom: IrT = SrT / (√3 × Ub) = 40 MVA / (√3 × 10,5 kV) = 2199 A
- Kabeltyp N2XSY 12/24 kV, Verlegung in Erde, Belastungsgrad m = 0,7
- Anordnung der einadrigen Kabel einzeln, Systemabstand a = 7 cm
- Umgebungstemperatur 20 °C, spezifischer Erdbodenwiderstand 1,0 K·m/W
- Gesamtumrechnungsfaktor 0,85
- Bemessungsbelastbarkeit mit IBb = 350 A → zulässiger Strom: Ir = IBb / Σf = 350 A / 0,85 = 411,76 A
- Erforderlicher Querschnitt nach DIN VDE 0276 Teil 603: 3 × 1 × 185 mm²
- Maximale Übertragungsleistung: Smax = √3 × IB × Un = √3 × 411,76 A × 10,5 kV = 7,488 MVA

---

### 18.24 Zusammenfassung Mittelspannungsanlagen

Mittelspannungsanlagen arbeiten typischerweise auf 10 oder 20 kV und finden Einsatz in der Industrie sowie zur städtischen Energieverteilung. Netztopologien: Stern-, Ring- und Maschennetz. Energie wird über Verteilungstransformatoren übertragen. Einspeise- und Abgangsfelder sind als kompakte, modulare Baueinheiten realisiert. Stationsunterbringung: Fertigbetonzellen, Container oder Sonderräume. Schaltanlagen wahlweise in Metall- oder Isolierstoffkapselung. Einzelne Felder durch Schottungen unterteilt. Schutzeinrichtungen: Überstromschutz, Transformatordifferentialschutz, Distanzschutz. Spannungsauswahl und Sternpunktbehandlung sind zentrale Planungsparameter.

**Referenznormen (Kap. 18):**
- DIN VDE 0101: Starkstromanlagen über 1 kV
- DIN VDE 0105 Teil 1: Betrieb von Starkstromanlagen (prEN 50110)
- DIN VDE 0102: Kurzschlussstromberechnung Drehstromnetze (IEC 60909)
- IEC 62271-200 / VDE 0671-200: Fabrikfertige typgeprüfte Metallanlagen
- IEC 62271-201 / VDE 0671-201: Isolierstoffkapselung
- DIN VDE 0103: Thermische und mechanische Kurzschlussfestigkeit
- DIN VDE 0298: Strombelastbarkeit Kabel/Leitungen
- DIN VDE 0276 Teil 1000: Umrechnungsfaktoren Starkstromkabel
- DIN VDE 0276 Teil 623: Strombelastbarkeit in Erde und Luft
- DIN VDE 0470 Teil 1: Schutzarten durch Gehäuse
- DIN VDE 0414: Messwandler
- DIN VDE 0532: Transformatoren
- DIN VDE 0536: Belastbarkeit Transformatoren
- DIN 42508 Teil 1: Öltransformatoren mit Umsteller
- DIN VDE 0670 Teil 6: Metallgekapselte HS-Schaltanlagen bis 25 kV (IEC 60298)
- DIN VDE 0670 Teil 1000: Wechselstromschaltgeräte über 1 kV
- DIN VDE 0670 Teil 101–108 (IEC 60056): HS-Leistungsschalter
- DIN VDE 0670 Teil 2: Trennschalter und Erdungsschalter (IEC 60129)
- DIN VDE 0670 Teil 301: HS-Lastschalter unter 52 kV (IEC 60265-1)
- DIN VDE 0670 Teil 611: Fabrikfertige Hoch-/Niederspannungsstationen (IEC 61330)
- DIN VDE 0670 Teil 4: Strombegrenzende Sicherungen (IEC 60282)
- DIN VDE 0683 Teil 1,2: Ortsveränderliche Erdungs-/Kurzschlussgeräte (IEC 60529)
- DGUV Vorschrift 3: Unfallverhütungsvorschrift Elektrische Anlagen

---

### Kapitel 19: Hochspannungsanlagen

Hochspannungsanlagen bilden die Schnittstelle zwischen verschiedenen Übertragungsspannungsebenen. Einsatzbereich: Übertragungsnetze bis 800 kV. Grundprinzip: Umspannschaltanlagen mit Sammelschienensystemen verteilen Energie über das Netz. Wichtigste Planungskriterien: Spannungsebene, Einspeisung, Lastabgang, Lastveränderung und (n-1)-Prinzip. Einteilung: luftisolierte Freiluftschaltanlagen und gasisolierte Innenanlagen.

#### 19.1 Luftisolierte Schaltanlagen (Freiluft)

Freiluftanlagen sind luftisoliert ausgeführt. Die Anlagengröße hängt von Bauweise und Spannungsebene ab. Einzelkomponenten müssen:
- Normalbetriebslasten standhalten
- Ungünstiger Lastverteilung widerstehen
- Schalt- und Kurzschlusskräfte ertragen

Bei kleinen Strömen: Seilsammelschienen aus Al/St oder Aldrey. Bei größeren Strömen: Rohrsammelschienen vorteilhaft.

**Bauweisen nach Spannungsebene:**
- Bis 245 kV, klassische Bauweise: Leitungsabzweige verlaufen oberhalb der Sammelschienen; Vorteile: geringe Feldverteilung, gute Revisierbarkeit der Sammelschienen
- 110 kV: offene Schaltanlagen üblich
- Bis 145 kV, Reihenlängsbauweise: Trenner hintereinander längs zur Sammelschiene; Nachteile: große Feldverteilung, schlechte Revisionsbedingungen
- Bis 245 kV, Reihenquerbauweise: geringe Feldteilung, aber große Bautiefe
- Bis 420 kV, Diagonalbauweise

Erforderliche Komponenten: Trennschalter, Überspannungsableiter, Strom- und Spannungswandler, Leistungsschalter.

#### 19.2 Gasisolierte Schaltanlagen (GIS)

Gasisolierte Hochspannungsschaltanlagen sind für den Innenbetrieb ausgelegt und nach dem Baukastenprinzip aufgebaut. Spannungsbereich: 72,5 bis 800 kV.

Komponenten einer GIS-Anlage (Legende Abb. 19.4):
1. Integrierter Ortssteuerschrank
2. Stromwandler
3. Sammelschiene II mit Trenner und Erdungsschalter
4. Unterbrechungseinheit des Leistungsschalters
5. Sammelschiene I mit Trenner und Erdungsschalter
6. Federspeichereinheit mit Leistungsschaltersteuereinheit
7. Spannungswandler
8. Schnellerder
9. Abgangsfeld
10. Kabelendverschluss

**Vorteile verschiedener Sammelschienenvarianten:**
- Einfaches Sammelschienensystem: kostengünstig, übersichtlich; bei Wartung muss die gesamte Anlage abgeschaltet werden; durch Kuppelschalter können Anlagenteile im Betrieb bleiben
- Parallele Sammelschienen (Doppelsammelschiene): geeigneter für Wartung und Versorgungssicherheit; eine Sammelschiene bleibt stets in Betrieb

---

### Kapitel 20: Sammelschienensysteme

Sammelschienen übernehmen die Verteilung von Strömen auf die angeschlossenen Abzweige. Auswahlkriterien für das System:
- Anzahl der Einspeisungen und Abzweige
- Trennbarkeit der Anlagenteile
- Umschaltmöglichkeit für Verbraucher
- Erfüllung des (n-1)-Kriteriums

#### 20.1 Einfachsammelschiene

Vorteile: kostengünstig, übersichtlicher Aufbau. Nachteil: vollständige Abschaltung bei Wartungs- und Änderungsarbeiten erforderlich. Über Kuppelschalter können einzelne Anlagenteile weiterbetrieben werden.

#### 20.2 Doppelsammelschiene

Vermeidet die Nachteile der Einfachsammelschiene: Energieversorgung bleibt während Wartungsarbeiten vollständig aufrechterhalten. Über eine Umgehungsschiene kann die Anlage im laufenden Betrieb freigeschaltet werden — dabei sind die Messwandler besonders zu beachten.

Ausführungsvarianten der Doppelsammelschiene:
- Festeinbau
- Einschubbauweise
- Rücken-an-Rücken-Aufstellung
- Gegenüber-Aufstellung

Kopplungsvarianten: Längstrennung und Querkupplung.

#### 20.3 Hochstromschaltanlagen

In Kraftwerken stellen die Schaltanlagen zwischen Generator und Blocktransformator besonders hohe Anforderungen an Sicherheit und Verfügbarkeit. Aufgabe: sichere Schaltung der hohen Generatorströme und Sicherstellung der Eigenbedarfsversorgung im Störungsfall.

---

### Kapitel 21: Schalt- und Schutzgeräte

Nach DIN VDE 0670 Teil 6 ist eine Schaltanlage definiert als Kombination von Schaltgeräten mit den zugehörigen Steuer-, Mess-, Schutz- und Regeleinrichtungen einschließlich Baugruppen, Verbindungen und tragenden Teilen. Schaltgeräte verbinden, unterbrechen und trennen Stromkreise — sowohl im normalen Betrieb als auch im Fehlerfall.

Auswahlkriterien für Schaltgeräte:
- Freischaltaufgabe (spannungslos schalten)
- Lastschaltung
- Abschalten von Überlast und Kurzschluss
- Personenschutzfunktion

#### 21.1 Hochspannungsschutzgeräte

##### 21.1.1 Unabhängiges Maximalstrom-Zeitrelais (UMZ)

Beim UMZ ist die Auslösezeit unabhängig von der Stromhöhe. Sobald der eingestellte Auslösestrom überschritten wird — unabhängig vom tatsächlichen Betrag — löst das Relais nach der eingestellten Zeitverzögerung aus. Auslöseparameter werden als Strom-Zeit-Paare definiert, z. B. 1,2 A / 0,5 s: Auslösung bei Überschreitung des 1,2-fachen Betriebsstroms nach 0,5 s Verzögerungszeit.

##### 21.1.2 UMZ mit Richtungskriterium

Bei Ringleitungen, mehrfach gespeisten Netzen oder parallel betriebenen Leitungen ist Selektivität mit einfachen Schutzeinrichtungen nicht erreichbar. Hier muss zusätzlich die Richtung des Fehlerstroms ausgewertet werden: nur die von der Quelle oder Sammelschiene zur Fehlerstelle hinfließenden Ströme werden für den Auslöseentscheid herangezogen.

##### 21.1.3 Abhängiges Maximalstrom-Zeitrelais (AMZ)

Das AMZ funktioniert ähnlich wie eine Schmelzsicherung, aber mit dem Unterschied: Die Strom-Zeit-Kennlinie ist nicht durch Materialeigenschaften festgelegt, sondern frei einstellbar und auf die zu schützende Anlage abstimmbar. Die Auslösezeit hängt direkt von der Kurzschlussstromhöhe ab.

##### 21.1.4 Distanzschutz

Anwendung in vermaschten oder mehrfach gespeisten Netzen zum Schutz von Kabeln und Leitungen. Funktionsprinzip: Die im Normalbetrieb vorhandenen Impedanzen der Kabel und Leitungen werden als Referenz eingestellt. Ein Kurzschluss verringert die aus Quellsicht gemessene Impedanz. Das Schutzgerät erkennt darüber den Fehlerort und initiiert das Abschaltsignal.

##### 21.1.5 Differentialschutz

Vergleichsschutz, der Messwerte am Eingang und am Ausgang des zu schützenden Anlagenteils miteinander vergleicht. Wirkt selektiv und bietet sehr guten Schutz für den fehlerbehafteten Bereich.

##### 21.1.6 Leistungsschalter (Mittelspannung)

MS-Leistungsschalter nach IEC 62271-100 / VDE 0671-100 erhalten ihre Schutzfunktion durch vorgelagerte Schutzeinrichtungen:
- Überstromzeitschutz
- Überstromzeitschutz mit Richtungsfunktion
- Differentialschutz

##### 21.1.7 Strom- und Spannungswandler

Wandler transformieren hohe Spannungen und große Ströme auf für Mess- und Schutzzwecke geeignete Werte — betragsmäßig und in der Phasenlage. Stromwandler arbeiten nahezu im Kurzschluss, Spannungswandler nahezu im Leerlauf. Primär- und Sekundärseite sind in fast allen Ausführungen galvanisch getrennt und gegeneinander isoliert.

##### 21.1.8 Lastschalter

Können Ströme bis zu ihrem Bemessungsbetriebsstrom schalten. Kurzschlusseinschalten bis zum Bemessungskurzschlusseinschaltstrom ist möglich. Das Abschalten von Kurzschlussströmen ist jedoch nicht vorgesehen (kurzzeitig ausführbar). Auslegung für hohe Schalthäufigkeit. Kombination von Last- und Trennschalter = Lasttrennschalter.

##### 21.1.9 HH-Sicherungen

HH-Sicherungen (Hochspannung-Hochleistung) nach IEC 60282 / VDE 0670-4 dienen ausschließlich dem Kurzschlussschutz — eine Überlastschutzfunktion fehlt. Für einwandfreies Auslösen ist ein Mindestkurzschlussstrom erforderlich. HH-Sicherungen begrenzen den Stoßkurzschlussstrom. Die Schutzkennnlinie ergibt sich aus dem gewählten Bemessungsstrom.

##### 21.1.10 Trennschalter, Erdungsschalter und Überspannungsschutzgeräte

**Trennschalter:** Schalten spannungslos (stromlos); dienen Wartung, Erweiterung und Umschaltung. Pflicht: sichtbare Trennstrecke mit vorgeschriebenen Mindestabständen, erkennbar per Sichtkontakt oder kraftschlüssig gekoppelter Anzeigevorrichtung.

**Erdungsschalter:** Verbinden Anlage für Wartungs- und Revisionsarbeiten mit Erde. Ein Schalterpol liegt dauerhaft auf Erdpotential. Praxis: Dreistellungsschalter EIN-AUS-GEERDET.

**Überspannung:** Kurzzeitig zwischen Außenleitern oder gegen Erde auftretende Spannung, die die Betriebsspannung übersteigt. Überspannungsschutzgeräte begrenzen diese schnell. Ausführungen: Ventilableiter und Metalloxidableiter, die sich in Aufbau und Wirkung bei verschiedenen Überspannungsformen unterscheiden.

#### 21.2 Niederspannungsschutzgeräte

Überstromschutzeinrichtungen (ÜSE) schützen Leitungen und Kabel. Auswahlkriterien:
- Art des Betriebsmittels
- Leitungs- bzw. Kabeltyp und Querschnitt
- Bemessungsausschaltvermögen
- Selektivitätsanforderungen

**Begriffsdefinitionen:**
- Dauerstrom: Strom, den eine ÜSE im normalen Betriebs- und Umgebungszustand dauerhaft führen kann
- Einstellstrom: Wert, auf den z. B. der Überstromauslöser eingestellt wird
- Kurzschlussfestigkeit: Widerstandsfähigkeit einer ÜSE im geschlossenen Zustand gegen dynamische und thermische Beanspruchungen im Kurzschlussfall
- Überstrom: jeder Strom oberhalb des Bemessungsstroms (sowohl Überlast als auch Kurzschluss)
- Überlastauslöser: Schutz gegen Überlast (Kennzeichnung Ir)
- Magnetischer Auslöser: Schutz gegen Kurzschluss (Kennzeichnung IrM)
- Unverzögerter Auslöser: spricht ohne beabsichtigte Zeitverzögerung an

##### 21.2.1 Leitungsschutzschalter (MCB)

MCB (Miniature Circuit Breaker) nach IEC 60898-1 / VDE 0641-11 kombinieren Thermobimetallauslöser (Überlastschutz) und Elektromagnetauslöser (Kurzschlussschutz). Nach Fehlerbeseitigung durch den Anlagenbetreiber sofort wieder einschaltbar ohne Teileaustausch.

**Auslösecharakteristiken und Abschaltströme (Tabelle 21.1):**

| Charakteristik | Thermisch I2 (verzögert) | Magnetisch I5 (unverzögert) |
|---|---|---|
| A | 1,45 × In | 3 × In |
| B | 1,45 × In | 5 × In |
| C | 1,45 × In | 10 × In |
| D | 1,45 × In | 20 × In |
| Z | 1,2 × In | 3 × In |
| K | 1,2 × In | 15 × In |
| E | 1,2 × In | 6,25 × In |

**Anwendungsgebiete nach Charakteristik (Tabelle 21.2):**

| Charakteristik | Anwendung | Bemessungsstrom-Bereich |
|---|---|---|
| A | Messkreise, Wandler, Steckdosen, Lichtstromkreise | 1–40 A |
| B | Hauptsächlich Wohnbauten | 6–50 A |
| C | Höhere Einschaltströme, Motoren, Lampen | 0,3–63 A |
| D | Impulsbetriebsmittel, Transformatoren, Kapazitäten | 0,5–50 A |
| K | Motorstromkreise | 6–63 A |

- Beleuchtungs- und Steckdosenstromkreise: B-Charakteristik
- Motoren mit hohen Einschaltströmen: C- oder K-Charakteristik
- Herstellungsbereich: Bemessungsströme 0,5 bis 125 A

##### 21.2.2 Belastbarkeit von Leitungsschutzschaltern (Temperaturabhängigkeit)

Bei der Montage ist die Umgebungstemperatur zu beachten. Zulässige Dauerstromwerte sinken mit steigender Temperatur (Tabelle 21.3):

| In (A) | 30°C | 35°C | 40°C | 45°C | 50°C | 55°C | 60°C |
|---|---|---|---|---|---|---|---|
| 6 | 6 | 5,6 | 5,3 | 5,0 | 4,6 | 4,2 | 3,8 |
| 10 | 10 | 9,4 | 8,8 | 8,0 | 7,5 | 7,0 | 6,4 |
| 16 | 16 | 15 | 14 | 13 | 12 | 11 | 10 |
| 20 | 20 | 18,5 | 17,5 | 16,5 | 15 | 14 | 13 |
| 25 | 25 | 23,5 | 22 | 20,5 | 19 | 17,5 | 16 |
| 32 | 32 | 30 | 28 | 26 | 24 | 22 | 20 |
| 40 | 40 | 37,5 | 35 | 33 | 30 | 28 | 25 |
| 50 | 50 | 47 | 44 | 41 | 38 | 35 | 32 |
| 63 | 63 | 59 | 55 | 51 | 48 | 44 | 40 |

##### 21.2.3 Nebeneinander montierte LS-Schalter

Durch gegenseitige Wärmeentwicklung reduziert sich die Belastbarkeit bei eng nebeneinander montierten LS-Schaltern. Korrekturfaktoren (Tabelle 21.4, gilt für 1-polige, 2-polige, 3-polige und 3+N-Ausführungen):

| Anzahl LS-Schalter nebeneinander | Korrekturfaktor |
|---|---|
| 1 | 1,00 |
| 2–3 | 0,95 |
| 4–5 | 0,90 |
| > 6 | 0,85 |

##### 21.2.4 Schmelzsicherungen

**NH-Sicherungen** nach IEC 60269-2 / VDE 0636-2x: hohes Kurzschlussausschaltvermögen; begrenzen durch rasches Abschmelzen den Kurzschlussstrom stark. Aufbau: Schmelzdraht aus leicht schmelzbarem Material in einem Porzellangehäuse, gefüllt mit Quarzsand (verhindert Außenaustreten des Schmelzfunkens). Drahtdicke abhängig vom Nennstrom.

Betriebsklassen:
- Ganzbereichssicherung (gG): Überlast- und Kurzschlussschutz
- Teilbereichssicherung (aM): nur Kurzschlussschutz

Bauartgruppen:
1. NH-System: Messerkontakte (nicht für Laien bedienbar)
2. D-System (Diazed): Schraubsicherung (für Laien bedienbar)
3. D0-System (Neozed): Schraubsicherung (für Laien bedienbar)

##### 21.2.5 RCD (Fehlerstromschutzschalter)

Funktionsprinzip: Im fehlerfreien Betrieb erzeugen hinein- und rückfließende Ströme Magnetfelder, die sich gegenseitig aufheben. Bei einem Isolationsfehler fließt ein Teil des Stroms nicht über den Rückleiter, sondern über den Schutzleiter ab. Das verbleibende Differenzmagnetfeld induziert eine Spannung, die einen magnetischen Auslöser betätigt und die Netzspannung abschaltet.

##### 21.2.6 Auswahl und Errichtung von RCDs (DIN VDE 0100 Teil 530)

RCDs müssen so ausgewählt und Stromkreisen zugeordnet werden, dass unerwünschte Auslösungen im Normalbetrieb unwahrscheinlich sind. Regelung:
- Schutzleiterströme und Erdableitströme auf der Lastseite des RCD dürfen zusammen maximal 0,4-fache des Bemessungsfehlerstroms betragen
- Bei Überschreitung: Aufteilung auf mehrere RCDs erforderlich
- Einschaltvorgänge können durch Aufladen von Ableitkapazitäten oder elektromagnetische Störungen zu unerwünschten Auslösungen führen
- Überspannungsschutzgeräte (SPDs) sind auf der Versorgungsseite des RCD anzuordnen (Bezug: DIN VDE 0100-534)

##### 21.2.7 RCD in Wohngebäuden nach DIN 18015-1 und DIN 18015-2

Zuordnung von Anschlussstellen zu Stromkreisen so vornehmen, dass im Fehlerfall oder bei manueller Abschaltung nur ein kleiner Anlagenteil abgeschaltet wird — maximale Verfügbarkeit für den Nutzer.

Selektivität zwischen hintereinandergeschalteten ÜSE und FI-Schutzschaltern erfordert Geräte mit entsprechenden Selektiveigenschaften.

**DIN 18015-2 (Mindestausstattung Wohngebäude):**
- RCDs müssen so auf Stromkreise verteilt werden, dass Auslösung eines einzelnen FI-Schutzschalters nicht zum Ausfall aller Stromkreise führt
- Ausnahme: selektive Fehlerstromschutzschalter
- Zentraler 30-mA-RCD vor der gesamten Wohnungsinstallation ist nach DIN 18015 **nicht zulässig**

##### 21.2.8 Hauptleitungsschutzschalter (SH-Schalter)

Werden im unteren Anschlussraum des Zählerplatzes eingebaut. Arbeiten selektiv zu vor- und nachgeschalteten ÜSE. Unterstützen nachgeschaltete Schutzeinrichtungen im Kurzschlussfall und begrenzen die Kurzschlussbelastungsenergie der elektrischen Anlage.

##### 21.2.9 Motorstarter (DIN VDE 0660 Teil 104 / IEC 292)

Zwei Ausführungsarten:

**Motorstarter mit Sicherungen:**
- Motorschutzrelais F3: Überlastschutz
- Sicherung F1: Kurzschlussschutz
- Hilfsschalter wird vom Überlastauslöser erst nach Überschreiten einer Mindestzeit betätigt und löst dann allpolig aus

**Motorschutzschalter mit Leistungsschalter:**
- Überlastschutz: Bimetall
- Kurzschlussschutz: magnetischer Schnellauslöser
- Beide Auslöser wirken auf gemeinsames Schaltschloss → allpoliger Auslösung
- Hat Trennereigenschaften, einsetzbar als Hauptschalter

**Einstellbereiche von Motorschutzschaltern bis 11 kW (Tabelle 21.5):**

| Bemessungsdauerstrom Iu (A) | Überlastauslöser Ir (A) | Kurzschlussauslöser IrM (A) | Maximale Motorleistung (AC-3) bei 400 V (kW) |
|---|---|---|---|
| 0,6 | 0,4–0,6 | 5–8 | 0,25 |
| 1 | 0,63–1,0 | 8–14 | 0,37–0,55 |
| 1,6 | 1,0–1,6 | 14–22 | 0,75 |
| 2,5 | 1,6–2,5 | 20–35 | 1,1 |
| 4 | 2,5–4,0 | 35–55 | 1,5–2,2 |
| 6,3 | 4,0–6,3 | 50–80 | 3–4 |
| 10 | 6,3–10 | 80–140 | 7,5 |
| 16 | 10–16 | 130–220 | 12,5 |
| 20 | 16–20 | 200–350 | 15 |
| 32 | 24–32 | 275–425 | 22 |
| 40 | 32–40 | 350–500 | 30 |

##### 21.2.10 Leistungsschalter (MCCB / ACB)

Können alle Ströme im Rahmen ihrer Bemessungswerte schalten — von induktiven/kapazitiven Lastströmen bis zum vollen Kurzschlussstrom, auch bei Netzfehlerbedingungen wie Erdschluss. Normbasis: IEC 60947-2 / VDE 0660-101.

Einsatzbereiche: Kurzschlussschutz, Überlastschutz, Fehlerschutz, Unterspannungsschutz von Anlagen, Motoren, Kabeln und Leitungen.

Lichtbogenlöschung bei Niederspannung: schnelles Kontaktöffnen, Magnetblassspulen, Löschbleche.

Unterscheidungsmerkmale:
- Bauart: offen (ACB) oder kompakt (MCCB)
- Einbauart: Festeinbau, steckbar, Einschub
- Bemessungsstrom (maximaler Nennstrom)
- Strombegrenzung: MCCB (Molded Case Circuit Breaker, strombegrenzend) vs. ACB (Air Circuit Breaker, nicht strombegrenzend)
- Schutzfunktionen und Kommunikationsfähigkeit (Datenübertragung in/aus dem Schalter)
- Gebrauchskategorie A oder B nach IEC 60947-2

##### 21.2.11 Auslöser und Schutzfunktionen für Leistungsschalter

Auslösertypen:
- **TMTU** (thermomagnetischer Auslöser): entweder fest eingestellt oder variabel einstellbar
- **ETU** (elektronischer Auslöser): stets einstellbar; kann im Schalter integriert oder als separater Baustein geliefert werden

Auslöserbezeichnungen nach Schutzfunktion:
- **L** (Long Time Delay): stromabhängig verzögerter Überlastschutz, mit Thermobimetallcharakteristik; optionale Kennlinien je nach Typ verfügbar
- **N** (Neutral): Neutralleiterschutz, stromabhängig verzögert; Empfindlichkeit wahlweise 50 % oder 100 % des Überlastauslösers L
- **I** (Instantaneous): unverzögerter Kurzschlussschutz (Magnetauslöser); verfügbar mit fester, einstellbarer oder abschaltbarer Funktion
- **S** (Short Time Delay): zeitselektiver Kurzschlussschutz für die zeitliche Staffelung in Reihenschaltung; bei hoher Kurzschlussbelastung ist zusätzlich I-Auslöser erforderlich, um innerhalb der thermischen Belastungsgrenze zu bleiben

---

### Kapitel 22: Selektivität und Back-up-Schutz

Selektivität liegt nach DIN VDE 0636 Teil 1 vor, wenn bei einem Kurzschluss- oder Überlaststrom ausschließlich das Schutzgerät abschaltet, das dem fehlerbehafteten Betriebsmittel unmittelbar vorgeschaltet ist. Bedingungen für die Koordinierung von in Reihe liegenden ÜSE:
- Im Fehlerfall darf nur die der Fehlerstelle am nächsten liegende ÜSE auslösen
- Stromspitzen dürfen nicht zu Fehler-Abschaltungen führen

#### 22.1 Selektivität zwischen zwei Leistungsschaltern

Zwei Gebrauchskategorien:
1. Nicht für Selektivität ausgelegt
2. Für Selektivität ausgelegt

**Stromselektivität:** Kurzschlussstrom des vorgeschalteten Leistungsschalters (Ik1a'') größer als der des nachgeschalteten (Ik1b'')  
**Zeitselektivität:** Auslösung über Sperrsignal und Kommunikationsleitung, wenn Ik1a'' ≤ Ik1b''

#### 22.2 Leistungsschalter vorgeschaltet vor Sicherung

Selektivitätsbedingungen ergeben sich aus den Zeit-Strom-Kennlinien beider Geräte. Getrennte Betrachtung von Überlastbereich und Kurzschlussbereich erforderlich.

#### 22.3 Sicherung vorgeschaltet vor Leistungsschalter

Selektivität ist gegeben, wenn vorgeschriebene Sicherheitsabstände in den Kennlinien eingehalten werden (Überlast- und Kurzschlussbereich getrennt beurteilen).

#### 22.4 Selektivität zwischen zwei Sicherungen

Voraussetzungen:
- Zeit-Strom-Kennlinien (Streubänder) dürfen sich nicht berühren
- Alterung von Sicherungen vermindert Selektivitätseigenschaften

Ab Sicherungsgröße In ≥ 25 A gilt:
- **Stromselektivitätsbedingung:** In1 ≥ 1,6 × In2
- Bei höheren Kurzschlussströmen gilt diese Nennstrombedingung nicht mehr; dann sind Stromwärmewerte zu vergleichen:
  - **Allgemeine Bedingung:** ∫I²·dt (vorgesch.) ≥ 1,6 × ∫I²·dt (nachgesch.)

#### 22.5 Sicherung vorgeschaltet vor Leitungsschutzschalter

**Überlastbereich:**
- B-Charakteristik: In1 ≥ 2,5 × In2
- C-Charakteristik: In1 ≥ 4 × In2

**Kurzschlussbereich:**
- Selektivitätsbedingung: ∫I²·dt (Sicherung) > ∫I²·dt (LS-Schalter)

#### 22.6 Selektivität zwischen zwei Leitungsschutzschaltern

Stromselektivität zwischen zwei LS-Schaltern ist generell nicht erreichbar, weil die Kurzschlussströme weit über den magnetischen Abschaltströmen beider Geräte liegen. Im Überlastbereich sind die Kennlinien für alle LS-Schalter mit gleicher Charakteristik identisch.

Bei parallel gespeisten Einspeisungen:
- Kurzschlussstrom an der Sammelschiene muss berechnet werden
- Kurzschlussstromaufteilung auf parallel liegende Quellen ist zu berücksichtigen
- Sicherheitsabstand von mindestens 100 ms zwischen der Auslösekennlinie des S-Auslösers und der Schmelzzeit-Strom-Kennlinie der NH-Sicherung ist einzuhalten
