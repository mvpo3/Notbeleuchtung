# Elektrotechnik für Architekten,Bauingenieure und Gebäudetechniker — Teil 6
> Quelle: Elektrotechnik für Architekten,Bauingenieure und Gebäudetechniker (buecher) · Seiten 241-280.

Dieser Teil des Lehrbuches behandelt Schutzkonzepte in Niederspannungsanlagen (TN- und TT-Systeme, Fehlerstromberechnungen), alle wichtigen Niederspannungsschutzeinrichtungen (MCB, Schmelzsicherungen, RCD, AFDD, MCCB), Übertragungs- und Kabeltechnik sowie die Grundregeln der Kabeldimensionierung nach DIN VDE 0100 und DIN VDE 0298.

## Inhalt

### Kapitel 17 (Fortsetzung): Schutzkonzepte — Erdverbindung und automatische Abschaltung

#### 17.6.1 TN-Systeme

- Im TN-System hängt der Schutz davon ab, dass PEN-Leiter oder Schutzleiter (PE) zuverlässig mit Erde verbunden ist.
- Wird die Erdung durch ein öffentliches Versorgungsnetz bereitgestellt, liegt die Verantwortung für die Erdungsbedingungen außerhalb der Kundenanlage beim Netzbetreiber.
- Neutral- oder Mittelpunkt des Versorgungssystems muss geerdet werden; falls kein Neutral-/Mittelpunkt verfügbar, muss ein Außenleiter geerdet werden.
- Alle berührbaren leitfähigen Anlagenteile (Körper) sind über Schutzleiter mit der Haupterdungsschiene zu verbinden, die wiederum mit dem geerdeten Punkt des Versorgungssystems verbunden ist.
- Abschaltbedingung TN-System (Schleifenimpedanz):
  - Zs ≤ U0 / Ia
  - Zs = Schleifenimpedanz (Ω), U0 = Leiter-Erde-Spannung (V), Ia = Abschaltstrom der Überstrom-Schutzeinrichtung (A)
  - Die Fehlerschleife umfasst: Stromquelle + Außenleiter bis Fehlerort + Schutzleiter vom Fehlerort zurück zur Stromquelle.

#### 17.6.2 TT-Systeme

- Im TT-System fließt der Fehlerstrom als Erdschlussstrom über Erder (Erde) zurück zur Stromquelle.
- Abschaltung erfolgt über vorgeschaltete Überstrom-Schutzeinrichtungen oder RCDs.
- TT-System spielt in industriellen Anwendungen eine untergeordnete Rolle.
- Abschaltbedingung bei Verwendung einer Überstrom-Schutzeinrichtung:
  - Zs ≤ U0 / Ia (identische Form wie TN, jedoch größere Fehlerschleife)
  - Fehlerschleife umfasst: Stromquelle + Außenleiter bis Fehlerort + Schutzleiter der Körper + Erdungsleiter + Anlagenerder + Erder der Stromquelle.
- Abschaltbedingung bei RCD:
  - RA ≤ 50 V / IΔn
  - Bei selektiver RCD: RA ≤ UT / (2 · IΔn)
  - RA = Schutzerdungs-(Ausbreitungs-)widerstand, IΔn = Nennfehlerstrom der RCD

### 17.7 Abschaltzeiten

Maximal zulässige Abschaltzeiten für Endstromkreise bei 400/230 V:

| System | 120 V < U0 ≤ 230 V | 230 V < U0 ≤ 400 V |
|--------|--------------------|--------------------|
| TN     | 0,4 s              | 0,2 s              |
| TT     | 0,2 s              | 0,07 s             |

- Für Verteilerstromkreise im TN-System gilt eine maximale Abschaltzeit von 5 s.
- Für Verteilerstromkreise im TT-System gilt eine maximale Abschaltzeit von 1 s.

Kenngrössen-Vergleich TN vs. TT (Tabelle 17.2):

| Kenngrößen | TN-System | TT-System |
|------------|-----------|-----------|
| Fehlerschleifen-Impedanz | unter 2 Ω | über 200 Ω |
| Fehlerstrom | unter 2 kA | abhängig von Betriebs- und Schutzerdung |
| Berührungsspannung | bis 115 V | 115 V bis 230 V |
| Berührungsstrom (bei 1000 Ω Körperimpedanz) | bis 115 mA | 115 mA bis 230 mA |
| RCD-Pflicht Personenschutz | 30 mA RCD für alle Steckdosenstromkreise | 30 mA RCD für alle Steckdosen- und Lichtstromkreise |
| Leitungsschutz | Überstromschutz-Einrichtungen (z.B. B 16 A LS-Schalter) | Überstromschutz-Einrichtungen (z.B. B 16 A LS-Schalter) |

### 17.8 Schutzklassen

Schutzklassen kennzeichnen den Schutz gegen elektrischen Schlag unter Fehlerbedingungen:

- **Schutzklasse I:** Körper/Gehäuse des Verbrauchers wird mit PE verbunden (z.B. Steckdosen, Motoren).
- **Schutzklasse II:** Körper/Gehäuse nicht mit PE verbunden; der Verbraucher besitzt eine Basisisolierung (z.B. Leuchten). Kein Schutzleiteranschluss.
- **Schutzklasse III:** Betrieb an Kleinspannung bis 50 V — entweder SELV (Safety Extra Low Voltage) oder PELV (Protective Extra Low Voltage) — z.B. Spielzeuge.

### 17.9 Schutzart (IP-Kennzeichnung)

- Die Schutzart beschreibt die Güte der Basisisolierung (Basisschutz) gegen Eindringen von Fremdkörpern und Wasser, geregelt nach EN 60529.
- Bezeichnung erfolgt als Buchstaben-Ziffern-Kombination (IP + 2 Ziffern + optionale Buchstaben).
- Beispiel IP 54 C S bedeutet:
  - 5: staubgeschützt
  - 4: geschützt gegen Spritzwasser
  - C: geschützt gegen Zugang mit Werkzeug
  - S: geprüft auf schädliche Wirkungen durch Wassereintritt bei stillstehenden beweglichen Teilen

### 17.10 Fehlerberechnungen

#### 17.10.1 Beispielrechnung TN-System

Gegebene Anlage (nur Ohmsche Widerstände berücksichtigt):
- Gesamtwiderstand: RG = RT + R1 + R2 + R3 = 15,38 mΩ + 2·23 mΩ + 2·20 mΩ + 2·106 mΩ = 313,39 mΩ
- Fehlerstrom: IF = U0 / RG = 230 V / 0,31339 Ω = 734 A
- Fehlerstrom im Schutzleiter (PE): IPE = (RK / (RPE + RK)) · IF = (1000 Ω / (0,106 Ω + 1000 Ω)) · 734 A = 733,92 A
- Berührungsstrom durch den menschlichen Körper: IT = IF − IPE = 734 A − 733,92 A = 80 mA
- Hinweis: Bei diesem Berührungsstrom kann Herzkammerflimmern auftreten, wenn die Einwirkdauer länger als 1 s beträgt.

#### 17.10.2 Beispielrechnung TT-System

Gleiche Anlage, jetzt als TT-System (Fehlerströme fließen über Erde):
- Fehlerstrom im Netz: IF = U0 / (RNetz + RA + RB) = 230 V / (0,178 Ω + 1 Ω + 2 Ω) = 72,37 A
- Fehlerspannung: UF = (RA / (RA + RB)) · U0 = (1 Ω / (1 Ω + 2 Ω)) · 230 V = 76,66 V
- Berührungsspannung: UT = (RPE / (RPE + RA)) · UF = (0,106 Ω / (0,106 Ω + 1 Ω)) · 76,66 V = 7,35 V
- Fehlerstrom im Schutzleiter: IPE = (RK / (RPE + RK + RA)) · IF = (1000 Ω / (0,106 Ω + 1000 Ω + 1 Ω)) · 72,37 A = 72,29 A
- Berührungsstrom Körper: IT = IF − IPE = 72,37 A − 72,29 A = 80 mA

**Sonderfall: unterbrochener Schutzleiter im TT-System:**
- Fehlerspannung: UF = ((RK + RA) / (RK + RA + RB)) · U0 = (1001 Ω / 1003 Ω) · 230 V = 229,54 V
- Berührungsspannung: UT = (RK / (RK + RA)) · UF = (1000 Ω / 1001 Ω) · 229,54 V = 229,31 V
- Körperstrom: IF = U0 / (RK + RA + RB) = 230 V / 1003 Ω = 229,31 mA
- Fazit: Ohne Schutzleiter steigt die Berührungsspannung auf gefährliche Werte (ca. 229 V), während der Fehlerstrom sinkt — Abschaltung ohne RCD nicht möglich.

Verwendete Größen:
- IF = Fehlerstrom in A
- UT = Berührungsspannung (früher UB) in V
- IT = Berührungsstrom (früher IK) in A
- RPE = Widerstand des Schutzleiters in Ω
- RT = Transformatorwiderstand in Ω
- RB = Betriebserdungswiderstand in Ω
- RA = Schutzerdungs-(Ausbreitungs-)widerstand in Ω

---

### Kapitel 18: Niederspannungsschutzeinrichtungen

Schutzeinrichtungen in elektrischen Anlagen schützen Menschen, Kabel/Leitungen und Verbraucher vor gefährlichen Überströmen. Überströme teilen sich in Überlastströme (größer als Bemessungsstrom, im fehlerfreien Betrieb) und Kurzschlussströme (zufällig oder absichtlich, Potential-Differenz fällt auf nahezu null, nach DIN EN 60909-0).

#### 18.1 Leitungsschutzschalter (MCB — Miniature Circuit Breaker)

- MCB nach IEC 60898-1 / VDE 0641-11 kombiniert zwei Auslösertypen:
  - **Thermo-Bimetallauslöser:** für den Überlastbereich (stromabhängig verzögert)
  - **Elektromagnetauslöser (Magnetauslöser):** für den Kurzschlussbereich (unverzögert)
- Einzel-Auslösekennlinien ergeben zusammen die Gesamtauslösekennlinie.
- Anwendung nach Auslösecharakteristik:
  - **B-Charakteristik:** für Beleuchtungs- und Steckdosenstromkreise
  - **C- oder K-Charakteristik:** für Motoren mit hohen Einschaltströmen
- Bemessungsströme: 0,5 A bis 125 A
- Nach Auslösung kann MCB ohne Teilewechsel wieder eingeschaltet werden.

Auslösecharakteristiken mit Auslöseströmen (Tabelle 18.1):

| Charakteristik | Verzögerter thermischer Auslöser I2 (Überlast) | Magnetauslöser I5 (Kurzschluss) |
|---------------|----------------------------------------------|----------------------------------|
| A             | 1,45 · In                                    | 3 · In                           |
| B             | 1,45 · In                                    | 5 · In                           |
| C             | 1,45 · In                                    | 10 · In                          |
| D             | 1,45 · In                                    | 20 · In                          |
| Z             | 1,2 · In                                     | 3 · In                           |
| K             | 1,2 · In                                     | 15 · In                          |
| E             | 1,2 · In                                     | 6,25 · In                        |

#### 18.2 Planungsgrundlagen von Schutzgeräten

- Thermische Auslöser (B und C) sind auf eine Bezugsumgebungstemperatur von 30 °C eingestellt.
- Bei abweichender Umgebungstemperatur ändern sich die Stromwerte um ca. 6 % je 10 °C Temperaturdifferenz.
- Bei dichter Nebeneinandermontage und gleichmäßig hoher Auslastung von FI/LS-Schaltern muss ein Korrekturfaktor berücksichtigt werden (gegenseitige Beeinflussung).
- Bei Belastungen länger als 1 h mit Bemessungsstrom In: Strom mit dem Faktor 0,9 multiplizieren.
- Rechenbeispiel: 8 × 16-A-MCB bei 50 °C Umgebungstemperatur → Belastbarkeit = 14,1 A · 0,9 · 0,85 = 11,38 A.

#### 18.3 Schmelzsicherungen

- NH-Sicherungen (Niederspannungs-Hochleistungssicherungen) nach IEC 60269-2 / VDE 0636-2x besitzen hohes Kurzschlussausschaltvermögen und begrenzen den Kurzschlussstrom durch schnelles Abschmelzen.
- Aufbau: Schmelzdraht aus leicht schmelzbarem Material, eingespannt in Porzellanggehäuse, mit Quarzsand gefüllt (verhindert Außentreten des Schmelzfunkens).
- Drahtdicke bestimmt den Bemessungsstrom.
- Nach dem Ansprechen sind Schmelzsicherungen nicht mehr einsatzfähig (kein Wiedereinschalten möglich).
- Alle Außenleiter müssen mit Sicherungen gleicher Bauart und gleichem Bemessungsstrom abgesichert sein; Überbrückung nicht zulässig.
- Betriebsklassen: Ganzbereichssicherung (Überlast- und Kurzschlussschutz) oder Teilbereichssicherung (nur Kurzschlussschutz).

Drei Bauarten:
1. **NH-System:** Messerkontakte (nur für Fachpersonal, nicht von Laien bedienbar)
2. **D-System (Diazed):** Schraubsicherung (von Laien bedienbar)
3. **D0-System (Neozed):** Schraubsicherung (von Laien bedienbar)

#### 18.4 RCD (Fehlerstromschutzschalter / Fehlerstrom-Schutzeinrichtung)

Funktionsprinzip:
- Im Normalbetrieb heben sich die Magnetfelder der hin- und rückfließenden Ströme gegenseitig auf.
- Bei einem Fehler fließt ein Teil des Stroms nicht über den Rückleiter, sondern über den Schutzleiter/Erde — das verbleibende Magnetfeld induziert eine Spannung, die einen Magnetauslöser betätigt und die Netzspannung abschaltet.

#### 18.5 Auswahl und Installation von RCDs

- Auswahl nach DIN VDE 0100 Teil 530.
- Stromkreise sind so auf RCDs aufzuteilen, dass im Normalbetrieb unerwünschtes Abschalten unwahrscheinlich ist.
- Schutzleiterströme und Erdableitströme auf der Lastseite dürfen zusammen nicht mehr als 0,4-fachen Nennfehlerstrom (IΔn) der RCD betragen; ggf. Aufteilung auf mehrere RCDs erforderlich.
- Bei Einschaltvorgängen können Ableitkapazitäten oder elektromagnetische Störungen zu ungewollten Auslösungen führen (Hinweis auf DIN VDE 0100-535.2.1).
- Überspannungs-Schutzeinrichtungen (SPDs) sind gemäß DIN VDE 0100-534 auf der Versorgungsseite von RCDs anzuordnen (nicht auf der Lastseite).

#### 18.6 Anwendung der RCD in Wohngebäuden

Nach DIN 18015-1 (Planungsgrundlagen):
- Anschlussstellen sind so Stromkreisen zuzuordnen, dass das Abschalten eines Kreises nur einen möglichst kleinen Teil der Kundenanlage abschaltet — maximale Verfügbarkeit für den Nutzer.
- Selektivität zwischen LS-Schaltern und RCDs erfordert Geräte mit entsprechenden Selektiveigenschaften.

Nach DIN 18015-2 (Mindestausstattung Wohngebäude):
- RCDs den Stromkreisen so zuordnen, dass das Auslösen eines einzelnen RCDs nicht zum Ausfall aller Stromkreise führt. Ausnahme: selektive RCDs.
- **Ein zentraler 30-mA-RCD vor der gesamten Wohnungsinstallation ist nach DIN 18015 nicht zulässig.**

#### 18.7 Hauptleitungs-Schutzschalter (SH-Schalter)

- Hauptleitungs-Schutzschalter (SH-Schalter) werden im unteren Anschlussraum des Zählerplatzes anstelle von NH-Sicherungen eingebaut.
- Arbeiten selektiv zu nachgeschalteten Überstrom-Schutzeinrichtungen.

#### 18.8 Fehlerlichtbogen-Schutzeinrichtung (AFDD)

- In elektrischen Anlagen entstehen häufig serielle und parallele Fehlerlichtbögen durch defekte Isolierung aktiver Leiter oder durch lose Verbindungen.
- RCDs können serielle Lichtbögen nicht erkennen, da kein Ableitstrom zur Erde entsteht.
- Überstromschutz-Einrichtungen (ÜSE) können diese Fehlerströme nicht abschalten, da der Auslösestrom zu klein ist.
- AFDDs können beide Lichtbogenarten erkennen und rechtzeitig abschalten.

Normgrundlage: DIN VDE 0100-420:2016-02 — empfiehlt oder schreibt AFDDs vor für Bereiche mit:
- erhöhter Brandgefahr
- leichter Brandausbreitung
- erhöhter Personengefährdung
- schützenswerten Gütern

**Pflicht AFDDs bis 16 A Betriebsstrom in folgenden Endstromkreisen:**
- Schlafräume, Heime, Tageseinrichtungen
- Schlaf- und Aufenthaltsräume barrierefreier Wohnungen
- Räume/Orte mit Feuerrisiko, brennbaren Baustoffen oder unersetzlichen Gütern

**Empfohlen (keine Pflicht):** Waschmaschinen, Trockner, Geschirrspüler.

Weitere Regelungen:
- In Drehstromkreisen (dreiphasig) ist kein AFDD nach der Norm vorgesehen.
- Funktionsprüfung vom Anwender nicht erforderlich — AFDD führt zyklischen Selbsttest durch.
- Höchster Schutz durch Kombination: AFDD + MCB + RCD.

Technischer Aufbau AFDD:
- Außenleiter und Neutralleiter werden durch das Gerät geführt und geschaltet.
- Außenleiter wird durch zwei getrennte Sensoren geführt: Stromsensor (niederfrequente/netzfrequente Signale) und HF-Sensor (hochfrequente Signale).
- Analogelektronik bereitet Signale vor, Mikrocontroller verarbeitet diese.
- HF-Leistung des Stroms wird im MHz-Bereich abgetastet (RSSI — Received Signal Strength Indication), repräsentiert Lichtbogenleistung bei definierter Frequenz und Bandbreite.
- Erkennt Mikrocontroller Fehlerlichtbogen-Kriterien, erzeugt er Auslösesignal → Arbeitsstromauslöser betätigt Schaltmechanismus → mechanisches Koppelglied betätigt angebauten LS- oder RCD/LS-Schalter.

#### 18.9 Leistungsschalter (MCCB — Molded Case Circuit Breaker)

- Leistungsschalter können alle Ströme ihres Nennbereiches schalten: von kleinen induktiven/kapazitiven Lastströmen bis zum vollen Kurzschlussstrom, auch bei Erdschlüssen.
- Hauptfunktionen: Kurzschlussschutz, Überlastschutz, Fehlerschutz, Schutz gegen Unterspannung.
- Thermische und magnetische Auslöser sind integriert.
- Müssen auch vollkommene Kurzschlüsse sicher abschalten.
- Lichtbogenlöschung bei Niederspannung: schnelles Öffnen der Kontakte, Magnetblassspulen und Löschbleche.

Klassifikation nach IEC 60947-2 / VDE 660-101:
- Bauart: offen oder kompakt
- Einbauart: Festeinbau, steckbar, Einschub
- Bemessungsstrom (max. Nennstrom)
- Strombegrenzung: strombegrenzend (MCCB) oder nicht strombegrenzend (ACB — Air Circuit Breaker)
- Kommunikationsfähigkeit (Datenübertragung in/aus dem Schalter)
- Gebrauchskategorie A oder B nach IEC 60947-2

#### 18.10 Auslöser/Schutzfunktionen des Leistungsschalters

Auslösertypen: thermomagnetische Auslöser (früher elektromechanisch) und elektronische Auslöser (ETU).

Auslösefunktionen mit Bezeichnungen:
- **L (Long Time Delay):** stromabhängig verzögerter Überlastauslöser; optionale Kennlinien je nach Auslösertyp.
- **N (Neutral):** stromabhängig verzögerter Überlastauslöser für Neutralleiter; verfügbar mit 50 % oder 100 % des L-Auslösestroms.
- **I (Instantaneous):** unverzögerter Kurzschlussauslöser (z.B. Magnetauslöser); fest, einstellbar oder mit Off-Funktion erhältlich.
- **S (Short Time Delay):** verzögerter Kurzschlussauslöser für zeitliche Staffelung (Selektivität) mit mehreren Schutzfunktionen in Reihe.

---

### Kapitel 19: Übertragungsmittel

Beschreibt Freileitungen und Kabeltypen für elektrische Energieübertragung.

#### 19.1 Freileitungen

- Freileitungen transportieren elektrische Energie von Erzeugung bis Verteilung.
- Bestandteile: Masten, oberirdisch verlegte Leiter, Isolatoren, Erdungen.
- Mastarten:
  - **Tragmasten:** tragen Leiterseile und Isolatoren bei gerader Leitungsführung
  - **Abspannmasten:** bilden Festpunkte, nehmen zusätzlich horizontale Seilkräfte auf
  - **Endmasten:** eingesetzt beim Übergang von Freileitung auf Kabel
- Tragwerke nach Spannungsebene:
  - Niederspannung: einfache Holzmasten
  - Mittelspannung: Holzmasten und Betonmasten
  - Hoch-/Höchstspannung: Stahlgittermasten
- Leitermaterial: Kupfer wurde bei Nieder- und Mittelspannung weitgehend durch Aluminium ersetzt; Hoch-/Höchstspannung nutzt Aluminium/Stahl-Seile.
- Höchstspannungsanlagen werden heute vorwiegend als Bündelleiter ausgeführt — Einseilleiter erzeugen durch hohe Randfeldstärke Koronaverluste und hochfrequente Störspannungen.

Planungsfragen für Leitungsanlagen (gelten auf allen Spannungsebenen):
- Welche Abnehmerstruktur ist gegeben (Industrie, Gewerbe, Haushalt)?
- Welche zeitliche und örtliche Lastverteilung liegt vor?
- Über welche Entfernung müssen Leistungen übertragen werden?
- Welche Leitungsarten sind wählbar (örtliche Gegebenheiten, Wirtschaftlichkeit)?

Einflussgrößen der Leitungsbemessung:
- mechanische Festigkeit
- thermische Beanspruchung
- Spannungsfall
- Verlustleistung
- Abschaltbedingungen

#### 19.2 Kabel und Leitungen

- Aderkennzeichnung von Starkstromkabeln/-leitungen nach VDE 0293-308:2003-01; gilt europaweit für Kabel und Leitungen bis 1 kV für feste und flexible Verlegung in und am Gebäude.
- Grundaufbau jedes Kabels: Leiter + Isolierung + Schutzmantel (Werkstoffe und Ausführungen variieren).
- Leiterwerkstoff: Kupfer und Aluminium.
- Leiteraufbau: ein- oder mehrdrahtig; Querschnittsform rund, oval, sektorförmig oder hohl.
- Ab 25 mm² Cu: ausschließlich mehrdrahtig ausgeführt (Biegefähigkeit).
- Leitungen feindrahtiger als Kabel (für flexiblen Einsatz vorgesehen).

Typenbezeichnung Starkstromkabel (Beispiele):
- Bauartbezeichnung: NYCWY, NYY oder NYM
- Leiterbezeichnung/Querschnitt: z.B. 4 × 120 mm²
- Bemessungsspannung: z.B. 20 kV oder 400 V

Buchstabenkurzzeichen nach DIN VDE 0250 für Leitungen (Auswahl):

| Buchstabe | Bedeutung |
|-----------|-----------|
| A | Ader, Aluminium-Umhüllung, Aluminiumader |
| B | Bleimantelleitung |
| C | konzentrische Leiter (abgeschirmt) |
| D | Drillingsleitung |
| F | feindrahtig, Fassungsader, Flachleitung |
| G | Gummihülle, 2-G-Silikonkautschuk (erhöhte Wärmebeständigkeit) |
| H | Hülle |
| I | Verlegung im Putz |
| (J) | Zusatz bei Mehraderleitungen mit gn-ge-Schutzleiter |
| K | Korrosionsschutz |
| L | für leichte mechanische Beanspruchung (z.B. Leuchtrö­hren) |
| M | Mantel, mittlere mechanische Beanspruchung |
| N | Normleitung |
| (0) | Zusatz bei Mehraderleitungen ohne gn-ge-Schutzleiter |
| Ö | ölfest |
| P | Papierumhüllung |
| R | Rohrdraht, gefalzte oder gerillte Rohrumhüllung |
| S | Schnur, Segeltuchhülle, schwere mechanische Beanspruchung |
| T | Trosse |
| U | Umhüllung / unflammbar bzw. flammwidrig |
| V | Verdrahtungsleitung, verdrehbeanspruchungsfest |
| W | wetterfest |
| Y | Kunststoffisolierung (Thermoplaste wie PVC) |
| Z | Zinkmantel, Zwillingsader, Zugentlastung |

Buchstabenkurzzeichen nach DIN VDE 0271 für Kabel (Auswahl):

| Buchstabe | Bedeutung |
|-----------|-----------|
| A (nach N) | Al-Leiter; (am Ende) Außenhülle aus Jute |
| B | Stahlbandbewehrung |
| C | konzentrischer Leiter |
| CE | Einzeladerschirmung |
| D | Druckbandage aus Metallbändern |
| E (nach N) | Einzeladerschirmung |
| fl | flammwidrig |
| Gb | Stahlbandgegenwendel |
| H | Kabel mit metallisierten Einzeladern (Höchstädter Kabel) |
| K | Kabel mit Bleimantel |
| L | glatter Aluminiummantel |
| N | Normkabel |
| O | offene Stahldrahtbewehrung |
| Ö | Ölkabel |
| Q | Beflecht­ung aus verzinktem Stahldraht |
| R | Runddrahtbewehrung, Rostschutzanstrich |
| S | Kupferschirm (6 mm²) für Berührungsschutz oder Fehlerstr­omleitung |
| u | unmagnetisierbar |
| WK | Stahlwellenmantel |
| W | Kupferwellenmantel |
| w | wärmebeständig |
| 2X | Isolierung aus vernetztem Polyethylen (VPE) |
| Y | Kunststoffisolierung |
| 2Y | Isolierung aus thermoplastischem Polyethylen (PE) |
| YY | Kunststoffaußenmantel |
| Z | Bewehrung aus Stahlprofildraht |

Leiterbezeichnungsfarben:
- Außenleiter: L1, L2, L3
- Neutralleiter N: hellblau
- Schutzleiter PE(N): gelb/grün

Verwendungstabelle für Kabeltypen (Tabelle 19.1):

| Kabeltyp | Verwendung |
|----------|------------|
| Mantelleitung NYM | in Rohren, auf/in/unter Putz, in trockenen, feuchten und nassen Räumen, im Mauerwerk und Beton; vor direkter Sonnenstrahlung schützen |
| Kunststoffkabel NYY | im Erdreich und im Wasser sowie in Innenräumen |
| Kommunikationsleitung J-Y(St)Y | Sprech- und Nebenstellenanlagen; vor direkter Sonnenstrahlung schützen |
| MSR-Leitung PYCYM | Geschirmte, paarig verseilte Leitung für Mess- und Regelzwecke |
| Busleitung YCYM | Europäischer Installationsbus (KNX/EIB); vor direkter Sonnenstrahlung schützen |
| Lichtwellenleiter LWL | Digitale Übertragung (z.B. ISDN) |
| Twisted-Pair-Leitung | 8, 24 oder 48 isolierte Adern (verdrillte Aderpaare) |
| Gummischlauchleitung H05RR-F | geringe mechanische Belastung, für Haushaltsgeräte und Büromaschinen |
| Kunststoffkabel mit konzentrischem Schutzleiter | Energiekabel für Hausanschlüsse und Straßenbeleuchtungsanlagen |
| Dreimantelkabel NAKBA | Energiekabel für Mittelspannungsanlagen |

#### 19.3 Kurzschlussbelastbarkeit von Kabeln

Kabeltemperaturen für PVC- und VPE-isolierte Kabel (Tabelle 19.2):

| Isolierung | Kabeltyp / Nennspannung | Betriebstemperatur (°C) | Endtemperatur (°C) | Bemessungs-Kurzzeitstromdichte für 1 s (Cu A/mm²) |
|-----------|------------------------|------------------------|--------------------|----------------------------------------------------|
| PVC | Ein- und mehradrige Kabel, 0,6 kV / 1–3,6 kV / 6 kV, ≤300 mm² | 70 | 160 | 115 |
| VPE | Ein- und mehradrige Kabel, 0,6 kV / 1–3,6 kV / 6 kV, ≤300 mm² | 90 | 250 | 143 |

---

### Kapitel 20: Kenngrößen elektrischer Leitungen

Elektrische Energie muss verlustarm übertragen werden; korrekte Planung und Normbeachtung sind dabei erforderlich. Freileitungen, Leitungen und Kabel für Drehstrom besitzen Ohmschen, induktiven und kapazitiven Widerstand. In Nieder- und Mittelspannung werden Ohmscher und induktiver Widerstand berücksichtigt; in der Hochspannung kommen zusätzlich Leiter-Erd-Kapazitäten und Betriebskapazitäten hinzu.

#### 20.1 Wirkwiderstand

- Der Wirkwiderstand Rw ergibt sich aus dem Gleichstromwiderstand plus Zusatzwiderstand (Stromverdrängung im Leiter und Wirbelströme im Metallmantel) bei Wechsel-/Drehstrom.
- Widerstand bei 20 °C: R₂₀°C = l / (κ · S) = ρ · l / S
  - l = Leitungslänge in m, S = Querschnitt in mm², ρ = spezifischer Widerstand, κ = Leitwert
- Temperaturabhängigkeit: Rϑ = R₂₀°C · [1 + α · (ϑ − 20 °C)]
  - α = Temperaturkoeffizient, ϑ = Endtemperatur

#### 20.2 Induktivität

- Leitungen haben aufgrund magnetischer Wechselfelder bei Wechselstrom eine Induktivität L und damit einen induktiven Widerstand XL.
- XL = ω · L
- Längenbe­zogene Induktivität: Induktivitätsbelag L' in H/km oder mH/m
- XL' = ω · L'

#### 20.3 Kapazität

- Freileitungen haben gegeneinander und gegenüber Erde unterschiedliche Potentiale; daraus entsteht eine Erdkapazität CE.
- Betriebskapazität: Cb = CE + 3 · Cg = 2π · ε · l / ln(ā / r0)
- Kapazitätsbelag C' in F/km; kapazitiver Widerstand: XC = l / (ω · Cb' · l)
- Betriebskapazitätswerte sind beim Hersteller zu erfragen.

Wichtige Größen:
- l = Kabellänge in m, S = Querschnitt in mm²
- ρ = spezifischer Widerstand, κ = Leitwert, α = Temperaturkoeffizient, ϑ = Endtemperatur
- XL = induktiver Widerstand, CE = Erdkapazität, Cb = Betriebskapazität

Wenn keine Herstellerangaben vorliegen, können folgende Tabellenwerte verwendet werden:

**Tabelle 20.1: Widerstandswerte bei 20 °C für Cu- und Al-Kabel und -Leitungen (Ω/km)**

| Querschnitt S (mm²) | Cu Resistanz r | Cu Reaktanz x | Cu Impedanz z | Al Resistanz r | Al Reaktanz x | Al Impedanz z |
|--------------------|---------------|--------------|--------------|---------------|--------------|--------------|
| 4 × 1,5 | 12,1 | 0,114 | 12,1 | — | — | — |
| 4 × 2,5 | 7,28 | 0,110 | 7,28 | — | — | — |
| 4 × 4 | 4,56 | 0,106 | 4,56 | — | — | — |
| 4 × 6 | 3,03 | 0,100 | 3,03 | — | — | — |
| 4 × 10 | 1,83 | 0,095 | 1,832 | — | — | — |
| 4 × 16 | 1,15 | 0,0894 | 1,153 | — | — | — |
| 4 × 25 | 0,727 | 0,0878 | 0,7319 | 1,20 | 0,088 | 1,203 |
| 4 × 35 | 0,524 | 0,0851 | 0,530 | 0,876 | 0,086 | 0,880 |
| 4 × 50 | 0,387 | 0,0848 | 0,396 | 0,641 | 0,084 | 0,646 |
| 4 × 70 | 0,268 | 0,0824 | 0,280 | 0,443 | 0,082 | 0,450 |
| 4 × 95 | 0,193 | 0,082 | 0,209 | 0,320 | 0,082 | 0,330 |
| 4 × 120 | 0,153 | 0,0805 | 0,172 | 0,253 | 0,080 | 0,265 |
| 4 × 150 | 0,124 | 0,0805 | 0,147 | 0,206 | 0,080 | 0,220 |
| 4 × 185 | 0,0991 | 0,0803 | 0,127 | 0,164 | 0,080 | 0,182 |
| 4 × 240 | 0,0754 | 0,0799 | 0,109 | 0,125 | 0,079 | 0,147 |
| 4 × 300 | 0,0601 | 0,0798 | 0,999 | 0,100 | 0,079 | 0,127 |

**Tabelle 20.2: Widerstandswerte bei 160 °C für Cu- und Al-Kabel und -Leitungen (Ω/km)**

| Querschnitt S (mm²) | Cu Resistanz r | Cu Reaktanz x | Cu Impedanz z | Al Resistanz r | Al Reaktanz x | Al Impedanz z |
|--------------------|---------------|--------------|--------------|---------------|--------------|--------------|
| 4 × 1,5 | 18,876 | 0,114 | 18,876 | — | — | — |
| 4 × 2,5 | 11,356 | 0,110 | 11,356 | — | — | — |
| 4 × 4 | 7,113 | 0,106 | 7,113 | — | — | — |
| 4 × 6 | 4,726 | 0,100 | 4,727 | — | — | — |
| 4 × 10 | 2,824 | 0,0945 | 2,824 | — | — | — |
| 4 × 16 | 1,778 | 0,0895 | 1,780 | — | — | — |
| 4 × 25 | 1,126 | 0,0879 | 1,129 | 1,872 | 0,088 | 1,873 |
| 4 × 35 | 0,817 | 0,0851 | 0,821 | 1,366 | 0,086 | 1,368 |
| 4 × 50 | 0,603 | 0,0848 | 0,608 | 0,999 | 0,084 | 1,002 |
| 4 × 70 | 0,418 | 0,0819 | 0,426 | 0,691 | 0,082 | 0,695 |
| 4 × 95 | 0,301 | 0,0819 | 0,312 | 0,499 | 0,082 | 0,505 |
| 4 × 120 | 0,241 | 0,0804 | 0,254 | 0,394 | 0,080 | 0,402 |

---

### Kapitel 21: Grundregeln der Kabeldimensionierung

Wichtigste Planungsaufgabe: richtige Bemessung von Kabel- und Leitungsanlagen. Vier Schritte:
1. Bemessungsregeln von Kabeln und Leitungen verstehen
2. Einflussgrößen berücksichtigen: Verlegeart, Umgebungstemperatur, Häufung
3. Querschnitte auswählen
4. Schutzeinrichtungen einsetzen

Kabel müssen DIN-VDE-Vorschriften erfüllen; Kennzeichnung über VDE-Leitfaden oder „harmonisiert" sowie über Daten des Kabelherstellers. Schutz von Kabeln und Leitungen ist in DIN VDE 0100 Teil 430 geregelt.

Einflussgrößen der Leitungsbemessung:
- Mechanische Festigkeit (Bauart und Verlegung)
- Thermische Beanspruchung (Betrieb und Störfall)
- Spannungsfall (Leitungsquerschnitt und maximal zulässige Länge)
- Leitungsverlust (Wirtschaftlichkeit)
- Abschaltbedingungen (Schutz)

#### 21.1 Schutz von Kabeln und Leitungen — Grundregeln

Vier Schutzprinzipien:

1. **Überlastschutz:** Kabel dimensionieren für maximalen Betriebsstrom IB oder Nennstrom In bzw. Einstellwert der Überlastschutzeinrichtung.
2. **Kurzschlussschutz:** Kabel muss die Wärmebelastung eines Kurzschlusses ertragen, unter Berücksichtigung der vorhandenen Kurzschlussschutzeinrichtung.
3. **Schutz durch Abschaltung (TN-Netze):** Querschnitt so wählen, dass die eingebaute Überstromschutzeinrichtung Fehler zwischen Außenleiter und Schutzleiter/PEN-Leiter automatisch in den vorgegebenen Zeiten abschaltet.
4. **Spannungsfall:** Bei Kabelbemessung den maximal zulässigen Spannungsfall für Verbraucher berücksichtigen.

10-stufige Vorgehensweise für Bemessung und Koordination eines Stromkreises:
1. Dreipoliger Kurzschlussstrom I"k3 am Stromkreisanfang nach DIN EN 60909-0 berechnen
2. Bemessungsstrom In der Schutzeinrichtung oder Einstellstrom Ie des Leistungsschalters bestimmen
3. Betriebsstrom IB des Stromkreises aus Wirkleistung ermitteln
4. Leiterquerschnitt A bestimmen
5. Querschnitt prüfen auf Überlast- und Kurzschlussschutz nach DIN VDE 0100-430 (Bemessungsregeln, Verlegeart, Reduktionsfaktoren, Häufung, Umgebungstemperaturen)
6. Maximal zulässige Leitungslänge prüfen nach DIN VDE 0100-520 Beiblatt 2
7. Spannungsfall prüfen nach DIN VDE 0100-520 oder DIN 18015
8. Selektivität prüfen nach DIN VDE 0100-530, DIN VDE 0100-710, DIN VDE 0100-718
9. Erstprüfung nach DIN VDE 0100-600
10. Dokumentation der Anlage

#### 21.2 Allgemeine Anforderungen

Kabel und Leitungen müssen durch Überstrom-Schutzeinrichtungen gegen übermäßige Erwärmung geschützt werden — sowohl durch betriebsmäßige Überlast als auch bei vollkommenem Kurzschluss.

Kategorien von Überstrom-Schutzeinrichtungen:
1. Schutz bei Überlast UND Kurzschluss: Leitungsschutzsicherungen, Leitungsschutzschalter, Leistungsschalter, Motorschutzschalter
2. Nur Überlastschutz: Schütz mit ausschließlich Überlastauslöser
3. Nur Kurzschlussschutz: Teilbereichssicherungen zum Geräteschutz; Leistungsschalter nur mit Schnellauslösern

Zuordnungsbedingungen nach DIN VDE 0100 Teil 430:

Nennstromregel:
- IB ≤ In ≤ IZ
  - IB = Betriebsstrom (Auslegungsstrom des Stromkreises)
  - In = Bemessungsstrom der Schutzeinrichtung
  - IZ = zulässige Strombelastbarkeit des Kabels/der Leitung

Großer Prüfstrom I2:
- I2 ≤ 1,45 · IZ
  - I2 = großer Prüfstrom (Auslösestrom unter festgelegten Bedingungen)

Überlastschutz kann bestimmt werden: nach Tabellen, durch Berechnung oder aus der Strombelastbarkeit.

Zulässige Abschaltzeit bei Kurzschluss (gilt bis 5 s):
- tzul. = (k · S / I"k1)²
  - tzul. = zulässige Ausschaltzeit oder Kurzschlussdauer in s
  - I"k1 = kleinster Kurzschlussstrom (Fehlerstrom) in A
  - k = Faktor abhängig von Leitermaterial, Anfangs- und Endtemperaturen (A·√s/mm²)
  - S = Leiterquerschnitt in mm²
- Es muss immer gelten: tzul. > tab (tab = tatsächliche Abschaltzeit der ÜSE)

#### 21.3 Überstromanwendungen

- Auf Überlast-Schutzeinrichtung darf verzichtet werden, wenn deren Auslösung eine Gefahr bedeuten würde — z.B. bei Erregerstromkreisen rotierender Maschinen, Speisestromkreisen von Hubmagneten oder Sekundärstromkreisen von Stromwandlern.
- Ausschaltvermögen muss mindestens dem größten Kurzschlussstrom am Einbauort entsprechen.
- Schutzeinrichtungen für Überlast werden am Anfang jedes Stromkreises und an allen Stellen eingebaut, wo sich die Strombelastbarkeit verringert.
- Ausschaltzeit darf nicht länger sein als die Zeit, in der der Kurzschlussstrom die Leiter auf die zulässige Kurzschlusstemperatur erwärmt.
- In öffentlichen, im Erdreich verlegten Verteilungsnetzen dürfen Kurzschlussschutzeinrichtungen entfallen.
- Klingeltrafos und Schweißtrafos bieten durch ihre Bauart inhärent eine Überstrombegrenzung.
- Überstrom-Schutzeinrichtungen für Drehstrommotoren müssen alle Außenleiter trennen.

#### 21.4 Technische Anschlussbedingungen

1. **Koordination von Schutzeinrichtungen:**
   - Planer und Errichter müssen Selektivität zwischen Schutzeinrichtungen in der Kundenanlage und denen im Hauptstromversorgungssystem sowie den Hausanschlusssicherungen sicherstellen.
   - In Hauptstromversorgungssystemen sind Schutzeinrichtungen nach DIN VDE 0100-530 selektiv auszuführen.

2. **Stromkreisverteiler:**
   - Anschlussstellen für Verbrauchsgeräte so auf Stromkreise verteilen, dass das Abschalten eines Kreises nur einen Teil der Kundenanlage abschaltet — maximale Verfügbarkeit für den Anschlussnutzer.

3. **Überlastschutz:** Kabel für größten Betriebsstrom der Verbraucher, Einstellwert der Überlastschutzeinrichtung und Nennstrom der Schutzeinrichtung dimensionieren.

4. **Einflussgrößen Belastbarkeit:**
   - Betriebsart und Leiterquerschnitt
   - Kabel- und Leitungsaufbau
   - Verlegebedingungen
   - Umgebungsbedingungen

5. **Bestimmung der Strombelastbarkeit IZ:**
   - Leiterwiderstand pro Längeneinheit (Leitermaterial, Querschnitt)
   - Maximale Temperaturbelastbarkeit der Leiterisolierung
   - Umgebungstemperatur
   - Verlegeart (Wärmeabgabe an Umgebung)
   - Anzahl belasteter Adern, Leiterhäufung (gegenseitige Beeinflussung mehrerer Leiter)

6. **Bemessungsregeln:**
   - Überlastschutz erfüllt, wenn Nennstromregel (IB ≤ In ≤ IZ) eingehalten ist; Auslösestrom I2 darf maximal 45 % größer sein als IZ, oder die ÜSE muss beim 1,45-fachen Strom spätestens nach 1 h auslösen.
   - Kurzschlussströme müssen durch ÜSE abgeschaltet werden, bevor sie für Leiterisolierung, Verbindungsstellen und Umgebung schädliche Erwärmung oder mechanische Wirkungen erzeugen; nur vollkommene Kurzschlussströme werden dabei betrachtet.

#### 21.5 Anordnung der Schutzeinrichtungen

- Ausschaltvermögen der Schutzeinrichtung muss mindestens dem größten dreipoligen Kurzschlussstrom am Einbauort entsprechen.
- Kurzschlussschutz jeweils am Anfang jedes Stromkreises und an jeder weiteren Stelle, wo der vorgeschaltete Kurzschlussschutz nicht mehr ausreichend ist.
- Ausschaltzeit bei vollkommenem Kurzschluss (t < 5 s) muss kürzer sein als die Zeit, in der dieser Strom die Leiter auf die zulässige Kurzschlusstemperatur erwärmt.
- Tabellen 21.3 bis 21.8 (entnommen aus DIN VDE 0298 Teil 4 und DIN VDE 0276 Teil 1000) geben empfohlene Strombelastbarkeitswerte für Kabel und Leitungen bei fester Verlegung in Gebäuden sowie für flexible Leitungen, inklusive Umrechnungsfaktoren.
