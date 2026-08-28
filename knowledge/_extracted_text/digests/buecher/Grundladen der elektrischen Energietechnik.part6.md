# Grundladen der elektrischen Energietechnik — Teil 6
> Quelle: Grundladen der elektrischen Energietechnik (buecher) · Seiten 241-280.

Dieser Teil behandelt die Betriebsmittel in Hochspannungsnetzen: Leitungsmodelle unter Belastung, Messwandler (Spannungs- und Stromwandler), Schaltgeräte (Leistungs-, Trenn- und Lastschalter) sowie Schaltanlagen in verschiedenen Bauformen (AIS, GIS, MS-Stationen, Ortsnetzstationen) einschliesslich Netzschutz und Überspannungsschutz.

## Inhalt

### 3.1 Blindleistung auf Hochspannungsleitungen (Seite 241)

- Auf langen Hoch- und Höchstspannungsleitungen verursachen induktive Leitungsreaktanzen bei starker Last erhebliche Blindleistungsbedarfe, begleitet von hohen induktiven Spannungsabfällen längs der Leiter.
- Abhilfe durch Reihenkompensation mit Kondensatorbank: reduziert die Wirkung der Leitungsinduktivität teilweise und verbessert zusätzlich die Netzstabilität.
- Weitere Kompensationsvarianten sind in Abschnitt 3.1.2 des Buches zusammengefasst.

#### Betrieb bei ohmsch-induktiver Belastung

- Transformatoren, Asynchronmotoren und vergleichbare Verbraucher beziehen induktive Blindströme als Magnetisierungsströme.
- Betrachtungsfall: Freileitung am Knoten B wird von einem unterlagerten Netz mit dem Leistungsfaktor cos φ (ohmsch-induktiv) belastet.
- Strom: I = -I_B = I · e^{-jφ}  (Gleichung 3.29)
- Spannungsfall ∆U = U_A - U_B wird in Längs- und Querspannungsfall aufgeteilt: ∆Ul (längs) und ∆Uq (quer), Gleichung 3.30.
- In der Höchstspannungsebene 220/380 kV gilt näherungsweise R'_b ≤ 0,3 · ω · L'_b, daher vereinfachte Formeln:
  - Längsspannungsfall: ∆Ul ≈ X_b · (I · sin φ - I_BE)
  - Querspannungsfall: ∆Uq = U_A · sin ϑ = X_b · I · cos φ  (Gleichung 3.31)
- Hauptursache des Spannungsabfalls: Blindstrom; Wirkstrom bestimmt den Übertragungswinkel ϑ.

#### Freileitungen im Verteilnetz (MS/NS-Ebene, Seite 242)

- In der Mittelspannungs- (MS) und Niederspannungsebene (NS) können bei kurzen Leitungslängen die Betriebskapazitäten C_b im Ersatzschaltbild weggelassen werden.
- Begrenzungsgrössen für die maximal übertragbare Leistung: zulässiger Spannungsfall und zulässige Leitererwärmung.
- Wirkleistungs- und Spannungsstabilität sind in der NS/MS-Ebene kein Thema.

---

### 3.3 Messwandler (Seiten 242-248)

Messwandler (englisch: Instrument Transformers) verbinden die Aussenleiter im Drehstromnetz mit der nachgeschalteten Sekundärtechnik (Messinstrumente, Elektrizitätszähler, Schutzrelais, digitale Feldleitgeräte). Schaltzeichen nach DIN EN 60617.

Zwei Hauptaufgaben:
1. Im Normalbetrieb: Erfassung betriebsfrequenter Wechselströme und -spannungen (Effektivwerte I und U, Phasendifferenz, Wirkleistung).
2. Bei Störungen: Erfassung von Erd- und Kurzschlussströmen sowie Über- und Unterspannungen, damit Schutzeinrichtungen schnell und sicher auslösen.

#### Genauigkeitsklassen (Tab. 3.14)

| Anwendung | VDE-Klasse | IEC-Klasse | ANSI-Klasse |
|---|---|---|---|
| Hochpräzise Messungen | 0,1 | 0,1 | 0,3 |
| Genaue Leistungsmessung und Verrechnungszwecke | 0,2 | 0,2 | 0,3 |
| Verrechnung und genaue Messinstrumente | 0,5 | 0,5 | 0,6 |
| Betriebsmessgeräte (U, I, Leistung, Zähler) | 1 | 1 | 1,2 |
| Strom-/Spannungsmesser, Überstromrelais | 3 | 3 | 1,2 |
| Stromwandler-Schutzkerne | 5P, 10P | 5P, 10P | C, T |
| Spannungswandler-Schutzkerne | 3P, 6P | 3P, 6P | 1, 2 |

- In Deutschland benötigen Wandler für Verrechnungszwecke eine Konformitätserklärung der Physikalisch-Technischen Bundesanstalt (PTB).
- Messwandler sind überwiegend einphasig; im Drehstromnetz werden daher jeweils drei Einheiten benötigt. Dreiphasige Ausführungen sind selten.
- Galvanische Trennung zwischen Hauptstromkreis und Messkreis ist zwingend, um die hohen Spannungen von der Mess- und Schutztechnik fernzuhalten.
- Isolationsmaterialien: öl-getränkte Papierisolation (weit verbreitet bis sehr hohe Spannungen; Ausdehnungsgefäss wegen Wärmedehnung nötig), SF6-Folienisolierung (wird zunehmend durch klimaverträglichere Gase ersetzt), Giessharz (verbreitet in MS-Ebene), keramische Porzellanisolatoren (Nachteil: Brüchigkeit, Explosionsgefahr bei Ölfüllung), Silikonschirm-Verbundisolatoren (geringes Gewicht, nicht brüchig, explosionssicher).
- Eigenverbrauch der nachgeschalteten Geräte wird als Bürde bezeichnet; lag früher zwischen 5 VA und 300 VA. Moderne Stations- und Feldleitsysteme haben eine deutlich kleinere Bürde; Trend hin zu LPIT-Sensoren (Low Power Instrument Transformer):
  - Strommessung: Rogowski-Spulen (IEC 61869-10/-8)
  - Spannungsmessung: kapazitive Teiler (IEC 61869-11/-7)

#### 3.3.1 Spannungswandler (Seite 245)

Internationale Bezeichnung: VT (Voltage Transformer). Zwei grundlegende Bauarten:

**Induktive Spannungswandler** (in Europa vorherrschend):
- Einphasige Transformatoren zu Mess- und Schutzzwecken.
- Bis 30 kV zweipolig ausgeführt: Leiter-Leiter-Spannung liegt an der Primärwicklung an.
- Ab 30 kV einpolig: ein Primärwicklungsanschluss am Aussenleiter, der andere wird geerdet; ab 30 kV muss auch an der Sekundärseite ein Anschluss geerdet werden.
- Sekundärwicklung besteht idealerweise aus nur zwei bis drei Lagen und wird im Leerlauf betrieben.
- Optionaler Einbau einer Erdschlusswicklung (da-dn-Wicklung) zur Erfassung einpoliger Erdfehler.
- Bauformen: Giessharzwandler (24 kV), SF6-Modul (123 kV), Ölwandler (245 kV).
- Bei sehr hohen Spannungen hat die Primärwicklung viele Windungen → teure Fertigung.

**Kapazitive Spannungswandler** (weltweit verbreitet in Hoch- und Höchstspannungsebene):
- Kostengünstigere Alternative bei sehr hohen Spannungen.
- Aufbau: Stapel von Kondensatorwicklungen bilden kapazitiven Spannungsteiler; eine Teilspannung U_C2 wird einem induktiven Mittelspannungswandler zugeführt.

#### 3.3.2 Stromwandler (Seiten 246-248)

Internationale Bezeichnung: CT (Current Transformer). Einphasige Transformatoren zu Mess- und Schutzzwecken.

Prinzip:
- Primärwicklung führt den Betriebsstrom eines Leiters im Drehstromnetz; muss auch Kurzschlussströme tragen.
- Wenn Primärleiter direkt durch ringförmigen Eisenkern geführt wird: Primärwicklung hat nur eine Windung.
- Sekundärseite hat viele Windungen; wird idealerweise im Kurzschluss betrieben.
- Wichtig: Sekundärkreis darf nicht unterbrochen werden (Überspannungsgefahr); Schutz durch Überspannungsableiter empfohlen.
- Umschaltbare Stromwandler möglich: primäre Umschaltung in Verhältnissen 1:2 oder 1:2:4 üblich; sekundäre Umschaltung über Anzapfungen.

Zwei Kerntypen:
- **Mess- und Zählkerne**: gehen im Fehlerfall früh in Sättigung, um nachgeschaltete Messtechnik zu schützen.
- **Schutzkerne**: ausgelegt für schnell ansteigende hohe Kurzschlussströme.
- Mehrere Mess- und Schutzkerne können kombiniert werden.
- Kernmaterialien: hochwertiges Siliziumeisen und legiertes Nickeleisen.

Isolationsvarianten und Bauformen nach Spannungsebene (Tab. 3.15):

| Spannungsebene | Isolation | Bauweise | Einsatzort |
|---|---|---|---|
| NS | trocken | Aufsteck-, Wickel- und Kabelumbauwandler | Innenraumanlagen |
| MS | Giessharz | Stützer- und Durchführungswandler | Innenraum- und SF6-Anlagen |
| HS und HöS | Ölpapier und Porzellan | Kessel- und Kopfstromwandler | Freiluftschaltanlagen |
| HöS | SF6 und Verbundwerkstoff (Glasfaser + Silikonkautschuk) | Kopfstromwandler | - |

Bauformen in Freiluftschaltanlagen:
- **Kesselstromwandler (Dead-tank Type / Kreuzringwandler)**: Primärleiter wird von oben nach unten ins geerdete Gehäuse geführt; Sekundärkerne befinden sich unten. Nachteile: höhere Verluste durch langen Primärleiter, begrenzte Kurzschlussströme, aufwendige Isolation. Vorteil: Schwerpunkt liegt tief (Erdbebensicherheit).
- **Kopfstromwandler (Live-tank Type)**: Sekundärkerne oben am Hochspannungsanschluss. Vorteile: kurzer Primärleiter → geringere thermische Verluste, höhere Strom- und Kurzschlusstragfähigkeit, einfachere und robustere Isolation, einsetzbar bis sehr hohe Wechselspannungen.
- **Kombiwandler**: Kopfstromwandler mit nach unten geführtem Hochspannungsanschluss zu einem Messkern → gleichzeitige Erfassung von Strom und Spannung, geringerer Platzbedarf, aber weniger Flexibilität und begrenztes Volumen für Messkerne.
- **Cascade/Eye-bolt Type**: Mischform mit Kernen auf halber Höhe.
- Vakuum-Interrupter-Einheiten: internationale Abkürzung VIU.

---

### 3.4 Schalter (Seiten 243-259)

Ein Schalter ermöglicht mehrmaliges Unterbrechen und Schliessen einer Strombahn, ausgelöst durch Handsteuerung oder automatisierte Impulse (z.B. digitales Feldleitgerät). Im Drehstromnetz dreiphasig ausgeführt; Einzelphase eines Schalters wird als Pol bezeichnet.

Aufgaben technischer Schalter:
- Im Schaltprozess: Öffnen oder Schliessen der Leiterbahn (Ein-/Ausschalten des Stroms).
- Im eingeschalteten Zustand: dauerhaftes Führen von Betriebsströmen und Tragen hoher Fehlerströme über definierten Zeitraum.
- Im ausgeschalteten Zustand: sicheres Isolieren von hohen Spannungen.

Anwendungen: Schalten von Stromkreisen (Leitungen, Umspanner, Lasten, Kompensationseinrichtungen), Isolation oder Erdung von Anlagenteilen, Sammelschienenwechsel. Bei Störungen: schnelles Unterbrechen von Kurzschlussströmen.

Konstruktive Auslegungskriterien: Netznominalspannung (dielektrische Isolation), Bemessungsstrom (Querschnitte der Leiterbahnen), Schaltvermögen (Lichtbogenlöschverfahren), geologische und klimatische Verhältnisse (Temperaturen, Feuchtigkeit, Staub, Erdbebengefahr).

Normen für Schaltgeräte (Tab. 3.16):

| IEC / DIN EN | VDE | Bereich |
|---|---|---|
| 60947 | 0660 | Niederspannungs-Schaltgeräte |
| 60282 | 0670 | Hochspannungssicherungen |
| 62271 | 0671 | HS-Schaltgeräte und -Schaltanlagen |

Schaltzeichen nach IEC / DIN EN 60617-7 (Tab. 3.17): idealer Schalter (offen/geschlossen), Leistungsschalter (heute und früher), Trennschalter, Erdungsschalter, Last- und Lasttrennschalter, Sicherung, Sicherungs-Lasttrennschalter.

Schalterarten im Überblick:
- **Leistungsschalter**: höchste Anforderungen; schalten Betriebsströme und leerlaufende Leitungen ein, Betriebsströme bei jedem Leistungsfaktor aus sowie Kurzschlussströme aus. Optional: Schalten von Doppelerdschlüssen, Phasenoppositionen, Kondensatorbatterien, automatische Wiedereinschaltung (AWE). Bei Generatorschaltern: Nennausschaltstrom bis 300 kA (Effektivwert), Einschaltstrom bis 825 kA.
- **Trennschalter (Trenner / Leerschalter)**: in Reihe vor und hinter Leistungsschalter; bilden im geöffneten Zustand eine dielektrische Isolationsstrecke längs. Isoliervermögen muss deutlich über Leiter-Erde-Isolation liegen. Können nur kleine Restströme unterbrechen (nach DIN VDE 0671-102: max. 0,5 A bei Bemessungsspannungen bis 420 kV). Im geschlossenen Zustand müssen sie Betriebs- und Kurzschlussströme bis zur Abschaltung führen. Typen: Drehtrenner, Hebeltrenner, Scherentrenner (Greifertrenner).
- **Erdungsschalter (Erder)**: erden und kurzschliessen abgeschaltete Anlagenteile. Manche sind einschaltfest. Freiluft-Erdungsschalter in HS/HöS-Ebene sind nicht einschaltfest verfügbar.
- **Lastschalter (MS-Ebene)**: günstigere Alternative; können nur Lastströme schalten, nicht Kurzschlussströme.
- **Lasttrennschalter**: Kombination aus Last- und Trennschalter; erfüllt Anforderungen beider.
- **Sicherungs-Lasttrennschalter**: Lasttrennschalter zusätzlich mit Sicherungen ausgerüstet.

#### 3.4.1 Ideale vs. technische Schalter (Seite 244)

Ein idealer Schalter öffnet/schliesst augenblicklich, ist widerstandslos im geschlossenen Zustand, kann beliebige Stromstärken unterbrechen und die offene Schaltstrecke ist perfekt isolierend.

Technische Schalter weichen von diesen idealisierten Eigenschaften ab. Ihre Ersatzschaltbilder sind komplex; für Schaltzeichen werden vereinfachend ideale Schalter verwendet.

#### 3.4.2 Leistungsschalter (Seiten 244-249)

Nur Wechselstromschalter werden hier betrachtet. Lichtbogenlöschung gelingt nur, wenn der Wechselstrom einen Nulldurchgang hat. Das Unterbrechen hoher Gleichströme ist technisch deutlich schwieriger (erfordert künstlichen Stromnulldurchgang). Erster hybrider HVDC-Leistungsschalter 2012 präsentiert.

Entwicklung der Löschmittel (historisch ab ca. 1890):
- Um 1890: erste wasser- und ölgefüllte Leistungsschalter.
- Ölarme Leistungsschalter: gemilderte Explosions- und Brandgefahr.
- Druckluftschalter (HS/HöS): beseitigten Brand- und Explosionsgefahr; erforderten aber leistungsstarke Kompressoren, waren sehr laut und wartungsaufwendig (Undichtigkeiten bei Kälte).
- SF6-Schalter und Vakuumschalter: heute vorherrschend.
- Künftig: SF6 wird EU-weit durch alternative Gase ersetzt (F-Gas-Verordnung).

**Gasschalter (SF6):**
- SF6 ist seit über 40 Jahren bewährt: chemisch stabil, hohe dielektrische Festigkeit, grosse Wärmeleitfähigkeit.
- Geschlossene Schaltkammer mit ausreichender SF6-Füllung für gesamte Lebensdauer.
- Drücke in der Hochspannung: 6 bis 8 bar üblich.
- Undichtigkeitsrate laut Herstellerangabe: unter 0,1 %/Jahr.
- Bei sehr kalten Umgebungen: Heizungen erforderlich, damit SF6 nicht verflüssigt.
- Lichtbogenbildung beim Öffnen der Kontakte: Plasma aus ionisierten Gasen und verdampften Metallpartikeln bei ca. 20 000 K und Drücken bis 10 MPa.
- Löschprinzip: Am Stromnulldurchgang wird Gas rasch gekühlt → Rekombination der Ionen → sinkende Leitfähigkeit; gleichzeitig werden Kontakte sehr schnell auseinander bewegt. Beide Massnahmen sollen Rückzündung verhindern.
- Transient Recovery Voltage (TRV): unmittelbar nach erfolgreicher Löschung entsteht transiente Einschwingspannung, die rasch abklingt und in netzfrequente Wechselspannung übergeht.
- Löschmethoden:
  - **Blaskolbenprinzip (Puffer-Schalter)**: Verdichten von Gas im Kompressionsvolumen erzeugt erforderlichen Löschdruck. Heute kaum mehr verfügbar.
  - **Selbstkompressionsprinzip (Auto-Puffer)**: Bei kleinen Strömen ähnlich wie Blaskolbenprinzip; bei hohen Kurzschlussströmen wird Lichtbogenenergie genutzt, um Gasstrom zur Löschung zu verstärken. Kommt mit deutlich weniger Antriebsenergie aus. Eingesetzt bis Bemessungsspannung 420 kV und Bemessungsstrom 80 kA.
- Antriebe: Kontaktbeschleunigung in Grössenordnung 100 g. Zwei verbreitete Typen:
  - **Federspeicherantriebe**: wirtschaftlich, robust, wenige bewegliche Teile, langlebig. Verfügbar von 72,5 kV bis 800 kV. Wartungsfreiheit für ca. 25 Jahre oder 6000 Schaltspiele garantiert. AWE mit mehrfachen Schaltzyklen möglich.
  - **Elektrohydraulische Antriebe**: in HS- und HöS-Freiluftgeräten heute kaum mehr erhältlich.
- Konstruktionsvarianten:
  - **Dead-Tank-Design**: Schaltstrecken in geerdetem, SF6-gefülltem Aluminiumtank; je zwei Durchführungen pro Pol. Verbreitet in Nordamerika.
  - **Live-Tank-Design**: Schaltkammer auf Hochspannungspotenzial; günstiger, geringere SF6-Füllung, weniger Platzbedarf. In Europa bevorzugt.
  - Einkammerschalter bis ca. 300 kV (bei deutschen Netzbetreibern in Freilufttechnik); Zwei- und Mehrkammerschalter bei höheren Spannungen (je Pol mehrere Kammern in Reihe). Parallel zu jeder Unterbrechungseinheit manchmal Steuerkondensatoren für gleichmässige Spannungsaufteilung.

**Vakuumschalter:**
- In der MS-Ebene heute vorherrschend (SF6-Schalter spielen dort kaum noch eine Rolle). Zunehmend auch in der HS-Ebene als Alternative zu SF6-Schaltern.
- Einsatz auch als Generatorschalter, Schalter für Kondensatorbänke, Stufenschalter für Transformatoren.
- Schaltkammer: Vakuum mit Druck unter 10^{-7} hPa → sehr gute Isolation und schnelle Verfestigung der Schaltstrecke.
- Kompakte Bauweise, sehr wartungsarm.
- Antriebe: Federspeicherantriebe oder permanent magnetische Antriebe.
- Mechanische Lebensdauer: 30 000 Schaltspiele (Close-Open).
- Lichtbogenbildung durch Metalldampf-Emission aus den Kontaktoberflächen beim Öffnen. Lichtbogentypen je nach Bemessungsausschaltstrom: diffus, kontrahiert oder rotierend.

#### 3.4.3 Trennschalter (Seite 249)

Auch Trenner oder Leerschalter genannt. Unterbrechen kleine kapazitive Restströme nach Öffnung des Leistungsschalters. Grenzwert nach DIN VDE 0671-102: max. 0,5 A bei Bemessungsspannungen bis 420 kV.

Konstruktionstypen: Drehtrenner, Hebeltrenner, Scherentrenner (auch Greifertrenner).

Erdungsschalter: als Anbauerder an Trennschalter oder freistehend.

In luftisolierten Schaltanlagen: geöffnete Trennschalter und geschlossene Erdungsschalter für Personal gut sichtbar. In gasisolierten Schaltanlagen und Generatorleistungsschaltern: Sichtfenster zur Augenprüfung der Schaltstellung. Schaltstellung auch via Meldekontakte ablesbar.

---

### 3.5 Schaltanlagen (Seiten 251-271)

Schaltanlagen schliessen und unterbrechen Stromkreise über Leistungsschalter (Freileitungen und Kabel). Sammelschienen bilden die Knotenpunkte im Drehstromnetz. Mit Umspannern: Umspannanlage (Umspannwerke, Umspannstationen, Ortsnetzstationen). In manchen Schaltanlagen: Steuerung der Spannung und Wirkleistung an Netzknoten (z.B. Umspanner mit Stufenschaltern). Sekundärtechnik (Schutztechnik, Feld-, Stations- und Netzleittechnik) ebenfalls in Schaltanlagen untergebracht.

Bauarten:
- **AIS (Air Isolated Switchgear)**: luftisolierte Schaltanlagen; klassische Wahl; in HS/HöS-Bereich grosser Platzbedarf wegen grossen Isolationsabständen.
- **GIS (Gas Isolated Switchgear)**: metallgekapselte gasisolierte Schaltanlagen seit 1967; Anwendung auf Offshore-Plattformen, in Kavernen von Wasserkraftanlagen, in städtischer Umgebung. Deutliche Platzersparnis gegenüber AIS. SF6 als Isoliergas bewährt; moderne GIS benötigen in HS-Ebene nur noch ca. ein Drittel der Fläche früher GIS. SF6-freie GIS in Entwicklung.
- **MTS (Mixed Technology Substation)**: hybride Schaltanlagen mit Integration von gasisolierten Anlagenteilen in bestehende luftisolierte Stationen.
- Mobile Schaltfelder und mobile Stationen mit gasisolierten Komponenten ebenfalls verfügbar.

Sicherheitsanforderungen an Schaltanlagen:
- AIS-Stationen: kein vollständiger Schutz gegen direktes Berühren möglich → abgeschlossene elektrische Betriebsstätte mit Zugang nur für unterwiesene Personen.
- Geeignete Abstände, Kapselungen, Abschottungen und Abdeckungen von Hochspannung führenden Teilen.
- Wartungs-/Instandsetzungsarbeiten: die 5 Sicherheitsregeln (Tab. 5.4) beachten.

Weitere Anforderungen an Schaltanlagen:
- Widerstandsfähigkeit gegen Wind, Temperaturschwankungen, Luftdruck, Luftfeuchte, Hochwasser, Tauwasser, Erdbeben, Verschmutzung, Korrosion.
- Freiluftanlagen: leicht wartbar. Gekapselte Anlagen: praktisch wartungsfrei.
- Einfache Erweiterbarkeit erwünscht (jedoch oft herausfordernd bei historisch gewachsenen Netzen).
- Störlichtbogen-Schutz: Bei Isolationsversagen im Innenraum → explosionsartige Drucksteigerung und Hitze. Wände daher mit Druckentlastungsklappen/-kanälen versehen; GIS mit Berstscheiben.
- Erdungsnetz, Überspannungsableiter, Blitzschutzeinrichtungen.
- Mechanische Festigkeit der Leiter gegen elektromagnetische Kräfte bei Kurzschluss.
- Kurzschlussstrombegrenzung, wenn Ausschaltvermögen der Leistungsschalter überschritten: Sammelschienentrennung oder Teilnetzbildung.

Instandhaltungsstrategien (Asset Management):
- **Ereignisorientiert**: Reaktion nur auf Ausfall; Reparatur oder Ersatz danach. Elementarste Strategie, bei niedrigen Stromausfallkosten sinnvoll.
- **Zeitorientiert**: präventiver Austausch von Verschleissteilen oder Betriebsmitteln in zeitlich festgelegten Abständen. Kostenintensiv, sehr hohe Verfügbarkeit.
- **Zustandsorientiert**: regelmässige Inspektionen zur Erfassung des Alterungszustands; rechtzeitiger Austausch vor Ausfall. Trend: Schaltanlagenmonitoring und digitaler Zwilling.
- **Zuverlässigkeitsorientiert**: berücksichtigt neben Alterungszustand auch Bedeutung der Komponente für die Gesamtzuverlässigkeit.
- Zukünftig: KI-Methoden zur Entscheidungsunterstützung beim Ersatzzeitpunkt.

#### 3.5.1 Schaltungen (Seiten 253-259)

Schaltungsdarstellungen im Drehstromnetz üblicherweise einphasig (alle Komponenten sind real dreifach vorhanden).

Kernelemente: Sammelschienensysteme (Einfach-, Doppel-, Dreifachsammelschienen). Mehrere Sammelschienen und Leistungsschalter pro Feld erhöhen Versorgungssicherheit, Verfügbarkeit und Flexibilität.

**Schaltfelder (Abzweige):**
- Freileitungsfeld: Leistungsschalter mit ein oder mehreren Sammelschienentrennschaltern auf einer Seite und einem Längstrennschalter auf der anderen Seite. Als Querelement: Erdungsschalter (Arbeitserder) zum Schutz gegen kapazitive Restladungen, induktive Einstreuungen und einlaufende Überspannungen bei Wartungsarbeiten. Optional: Stromwandler und Spannungswandler.
- Transformatorfeld: Leistungsschalter, ein oder mehrere Sammelschienentrennschalter, Stromwandler zwingend. Erdungsschalter nicht immer vorhanden. Überspannungsableiter auf beiden Seiten des Umspanners.

Schaltabfolge beim Ausschalten einer Leitung: zuerst Leistungsschalter öffnen → dann Sammelschienentrenner und Längstrenner öffnen → zuletzt Erdungsschalter schliessen. Einschalten in umgekehrter Reihenfolge. Mechanische und logische Verriegelungen verhindern Fehlschaltungen (z.B. Erden einer eingeschalteten Leitung).

**Kraftwerkseinspeisungen (Seite 256):**
- Zwischen Unterspannungsseite des Maschinentransformators und Generator: Leistungsschalter mit zwei Trennschaltern.
- Generatorsammelschienen-Spannung bis ca. 27 kV → sehr hohe Betriebsströme.
- Generatorsammelschiene und Eigenbedarfsnetz: isolierter Sternpunkt.

**Höchstspannungsschaltanlage mit Umgehungssammelschiene:**
- Doppelsammelschienensystem (SS1, SS2) mit Querkupplung (Leistungsschalter 11).
- Umgehungssammelschiene (SS3 = Bypass) ermöglicht, einzelne Abzweige (Leistungsschalter und Wandler) im Betrieb freizuschalten.
- Längstrennung (SS4) ermöglicht galvanische Netzaufteilung zur Kurzschlussstrombegrenzung.

**380/110-kV-Umspannwerk (Seite 256):**
- Auf 380-kV- und 110-kV-Seite je ein Doppelsammelschienensystem mit Querkupplung.
- US-Seite zusätzlich mit Längstrennung für flexible Netzgebietsaufteilung.
- Aus Redundanzgründen zwei Umspanner. Schaltgruppe typischerweise YNyn0 mit Tertiärwicklung (Ausgleichswicklung in Dreieck); Tertiärwicklung kann 20/0,4-kV-Eigenbedarfstransformator versorgen.

**110/10-kV-Umspannstation (Seite 257-258):**
- 110-kV-Netze oft als Ring mit Verzweigungen; H-Schaltung mit einfacher Sammelschiene auf der 110-kV-Seite zum Einschleifen in den Ring.
- MS-Seite: Einfachsammelschienensystem mit Längskupplung (Leistungsschalter für Schaltmassnahme auch im Fehlerfall).
- Umspanner-Scheinleistungen: selten über 50 MVA; Schaltgruppe YNd5 oder YNd11.
- Eigenbedarfstransformator 10/0,4-kV mit Schaltgruppe ZNyn5+d; Zickzackschaltung auf OS-Seite trägt Erdschlusslöschspule.
- Erdschlusslöschspulen alternativ am HS/MS-Umspanner; in manchen Fällen gänzlich weggelassen. MS-Netzsternpunkte: isoliert oder direkt geerdet (Tab. 4.11).

**Ortsnetzstationen (MS/NS-Übergang, Seite 258-259):**
- Schaltelemente: Lasttrennschalter; Kurzschlussschutz durch HH-Sicherungen.
- Bauweisen: Maststation (bei Freileitungen), Turmstation oder gemauertes Gebäude (je nach Eigentums- und Platzverhältnissen), unterirdisch (z.B. unter Fussgängerzone).
- Heute: gasisolierte MS-Schaltanlagen als Standard bei Neuanlagen.

#### 3.5.2 Bauweise (Seiten 259-267)

**Konventionelle Freiluftschaltanlagen:**
- Sammelschienen als Seil oder Rohr. Seile aus Einfach- oder Bündelleiter erfordern Portalkonstruktionen für Abspannketten. Rohrleiter auf Stützisolatoren mit Stahlkonstruktionen. Sammelschienen oben oder unten angeordnet.
- Bauweisen-Bezeichnungen leiten sich aus Anordnung der Sammelschienentrenner, Felder und Anzahl der Leistungsschalter pro Feld ab.
- **Diagonalbauweise** (verbreitet in 245-kV- und 420-kV-Anlagen): Sammelschienentrennschalter diagonal unter den Sammelschienen, Sammelschienen oben. Vorteil: bei ausgeschaltetem Abzweig auch Sammelschienen-Trennschalter spannungsfrei und zugänglich.
- **Reihenlängsbauweise**: Rohrsammelschienen; Pole der Sammelschienen-Trennschalter in Reihe längs zu den Sammelschienen. Anwendung bei Sammelschienenströmen über 3 kA. Geringster Gerüstkonstruktionsaufwand, übersichtliche Anlage.
- Abmassbeispiel Freiluft-Schaltanlage 380 kV (Abb. 3.100): Feldabstände 9,0 / 22,0 / 39,0 m; Tiefe ca. 20,0 / 90,0 m; Abstände zur Umzäunung 18,0 m.
- Abmassbeispiel 123-kV-Freiluftanlage (Abb. 3.102): Feldbreite 10,0 m + 10,0 m; Tiefe 48,0 m; diverse Höhenmasse 3,5 / 7,5 / 20,0 / 7,5 / 9,5 / 5,0 / 8,5 m.

**Gasisolierte metallgekapselte Schaltanlagen (GIS) (Seiten 262-265):**
- Betriebsspannungen bis 1100 kV, Ausschaltstrom bis 80 kA.
- Vorteile: geringer Flächen- und Raumbedarf, sicherer Berührungsschutz, geringer Wartungsaufwand, lange Lebensdauer ca. 40 Jahre; unempfindlich gegen Wind, Wetter, Staub.
- Modulbauweise: Sammelschienen, Leistungsschalter, Trennschalter, Wandler, Kabelendverschlüsse, Verbindungselemente in geerdeten, gasgedichteten Kapselungen.
- Vormontage und Prüfung ganzer Einheiten oder Felder im Werk möglich → kurze Montagezeiten auf der Baustelle.
- Moderne GIS in HS-Ebene benötigen nur noch ca. ein Drittel der Fläche früher GIS.
- Kapselungsmaterial: Aluminiumguss oder geschweisste Aluminiumbleche (geringes Gewicht, korrosionsbeständig, nicht magnetisierbar → reduzierte Wirbelstromverluste).
- Bis 170 kV: dreiphasige Kapselung. Bei höheren Spannungen: einphasige, dreiphasige oder kombinierte Versionen.
- SF6 als Isoliergas: Druck 3 bis 6 bar; IEC-Norm: Leckrate max. 0,5 %/Jahr; viele Hersteller unter 0,1 %/Jahr.
- Treibhauspotenzial (GWP) von SF6: durch EU-Richtlinie 2024/573 (F-Gas-Verordnung) Fristen bis zum vollständigen Verbot gesetzt. Wartung, Reparatur und Erweiterung bestehender SF6-Schaltanlagen bleiben auch nach Verbotsdatum erlaubt.

Beispiel SF6-Umspannstation 110/10 kV (Abb. 3.105):
- Umspanner aussen unter Überdachung (Blitzeinschlag unwahrscheinlich → auf Überspannungsableiter am Umspanner kann verzichtet werden).
- Einpoliger Anschluss OS-Seite an SF6-Schaltanlage 110 kV. US-Seite über Kabel in einpolig gekapselte 10-kV-SF6-Schaltanlage.
- Am Eingang der 110-kV-Freileitung Überspannungsschutz empfohlen.

**MS-Schaltanlagen (Seiten 264-266):**

MS-Netze unterteilt in:
- **Primäre Verteilebene**: Bemessungsströme bis 4 kA, Kurzschlussströme bis 63 kA. Leistungsschalter vorherrschend; Feldkonfigurationen eher projektspezifisch.
- **Sekundäre Verteilebene**: Bemessungsströme unter 1,25 kA, Kurzschlussströme unter 25 kA. Meist Lasttrennschalter mit HH-Sicherungen, teilweise auch Leistungsschalter. Standardlösungen verbreitet.

Auswahlkriterien MS-Schaltanlage: Netznominalspannung, Kurzschlussstrom, Leitungsparameter (Kabel oder Freileitung), Sternpunktbehandlung, klimatische Verhältnisse, Entscheidung zwischen luft- und gasisolierter Technik.

Vor-/Nachteile AIS vs. GIS (Tab. 3.18):

| Kriterium | AIS | GIS |
|---|---|---|
| Herstellungskosten | + (günstiger) | - (teurer) |
| Standardisierte Wandler | + (verwendbar) | - (eingeschränkt) |
| Maximaler Betriebsstrom | + (höher) | - |
| Wartungsaufwand | - (mehr) | + (weniger) |
| Zugänglichkeit, Komponentenaustausch | + (besser) | - |
| Einfluss der Umgebung | - (empfindlicher) | + (unempfindlicher) |
| Platzbedarf | - (mehr) | + (weniger) |
| Lebenszykluskosten (LCC) | - | + |

LSC-Klassen (Loss of Service Continuity) für metallgekapselte Schaltanlagen (Tab. 3.19):

| Klasse | Bedeutung |
|---|---|
| LSC1 | Öffnung eines Schaltraums erfordert vollständige Abschaltung und Erdung der gesamten Anlage |
| LSC2 | Öffnung eines Schaltraums ermöglicht Weiterbetrieb benachbarter Felder |
| LSC2A | Öffnung eines Schaltraums: Sammelschiene des Feldes darf weiter unter Spannung stehen |
| LSC2B | Öffnung eines Schaltraums: Sammelschiene und Kabelanschluss des Feldes dürfen weiter unter Spannung stehen |

Metallgekapselte MS-Schaltfelder typgeprüft nach DIN EN 62271-200 (VDE 0671 Teil 200). Feldtypen: Abgangsfelder (mit Leistungsschalter oder Lastschalter und Sicherungen), Einspeisefelder, Kuppelfelder, Transformatorfelder, Motorschaltfelder, Verrechnungsfelder, Blindstromkompensationsfelder.

**Kompaktstationen (Seite 266-267):**
- Typgeprüft nach IEC 62271-202.
- Fabrikfertig, standardisiert; Transport per LKW, Aufstellung per Kran.
- Von aussen zugänglich, nicht begehbar; geringer Flächenbedarf.
- Aufbau einer Kompaktstation 10/0,4 kV (Abb. 3.108): Kabelabzweige 10 kV, SF6-Lastschaltanlage 10 kV, Einschübe mit HH-Sicherungen, Transformator, Schaltanlage 0,4 kV, Kabelabzweige 0,4 kV.

**Digitale und aktive Ortsnetzstationen (Seite 267):**
- Anforderungen im Zuge der Energiewende: motorangetriebene fernsteuerbare Lasttrennschalter, Messwertaufnehmer zur Leistungsflussüberwachung, Kurzschluss- und Erdschlussrichtungsschutz, eigenversorgte Fernwirk-/Steuereinheiten mit wartungsfreier Batterie und Ladegleichrichter, Kommunikationseinheiten mit Gateway-Funktion.
- Steigender Platzbedarf durch grössere Ortsnetztransformator-Scheinleistungen → Neubauten zunehmend als begehbare Trafostationen.

#### 3.5.3 Netzschutz (Seiten 267-271)

Netzschutz umfasst:
- Überspannungsschutz und Isolationskoordination.
- Schutztechnik gegen Überströme (Überlast-, Erdschluss-, Kurzschlussströme).
- Daneben: Schutzeinrichtungen für Schieflast, Leistungspendelungen, Unterspannung, Unterfrequenz, Erwärmung, Strömungsstillstand (nicht vertieft behandelt).

Normen für Überspannungsschutz (Tab. 3.20):

| Norm | VDE | Bereich |
|---|---|---|
| IEC/DIN EN 60664 | VDE 0110 | Isolationskoordination für Betriebsmittel in NS-Stromversorgungssystemen |
| IEC/DIN EN 60071 | VDE 0111 | Isolationskoordination für Nennspannungen über 1 kV |

**Überspannungsableiter:**
- Aufgabe (Isolationskoordination): Isoliervermögen der Anlagen in jeder Spannungsebene quantitativ festlegen und mit Überspannungsableitern abstimmen; Primärtechnik-Massnahme, die nach Planungsabschluss nicht mehr angepasst werden muss.
- Einbauort: praktisch immer zwischen Leiter und Erde oder Sternpunkt und Erde.
- Räumlich begrenzter Schutzbereich:
  - HöS-Ebene: zu schützendes Objekt max. 30 m vom Ableiter entfernt.
  - MS-Ebene: max. 15 m.
  - Holzmastleitungen: max. 3 m.

Technisch zwei Varianten:

**Ventilableiter:**
- Aufbau: luftdicht gekapselte Funkenstrecke + Siliziumkarbid (SiC)-Widerstand in Reihe.
- Funkenstrecke: Reihenschaltung von Funkenstrecken-Elementen (Keramikgehäuse mit zwei winklig angeordneten Flachelektroden).
- R-C-Steuerelemente parallel zu Funkenstrecken-Elementen für gleichmässige Spannungsaufteilung.
- In HöS-Ebene: Abschirmung im Kopfbereich zur Steuerung der elektrischen Feldverteilung.
- Abmasse Beispiele: 380-kV-Ventilableiter ca. 4,2 m Höhe; 110-kV-Ventilableiter ca. 1,3 m Höhe.

**Metalloxidableiter:**
- Verwenden spannungsabhängige Widerstände = Varistoren (Kofferwort aus englisch "variable resistor"; VDR = Voltage Dependent Resistor).
- Varistormaterialien: Siliziumkarbid (SiC) oder Zinkoxid (ZnO) als Halbleiter.
- Verhalten: bei Nennspannung isolierend; bei deutlicher Spannungserhöhung schlagartiger Stromanstieg (charakteristische I-U-Kennlinie).
- Aufbau: Widerstandssäulen aus vielen ZnO-Scheiben in Porzellanüberwurf; volle Leiter-Erd-Spannung liegt an → kleiner Reststrom ca. 1 mA im Normalbetrieb.
- Steuerringe sorgen für gleichmässige Feldverteilung.
- Auch in SF6-Kapselung verfügbar (SF6-Ausführung).

**Überspannungsschutz in Gebäude-Niederspannungsanlagen (Seite 270):**
- Sinnvoll, wenn Netzbetreiber mit NS-Freileitungen versorgt (bei NS-Kabeln treten Blitzüberspannungen nicht auf, Schaltüberspannungen selten).
- Einbauort im Schaltschrank (nach Hausanschlusskasten, vor/nach Zähler + RCD 30 mA).
- Wirkungsweise: Varistoren bilden bei Überspannung Kurzschluss zur Potenzialausgleichsschiene → Überspannung sicher über Fundamenterder ableiten, ohne unterlagerte Stromkreise zu beeinflussen.
- Anschlussprinzip: Überspannungsableiter zwischen L1/L2/L3/N und PE; Potenzialausgleichsschiene verbunden mit Fundamenterder (25 mm² Cu), Wasserzähler, Heizung, Wasserleitung, Gasleitung.

**Schutztechnik (Seite 271):**
- Schutz vor Überströmen: Überlast-, Erdschluss- und Kurzschlussströme.
- Verhalten nach Fehlertyp:
  - Zeitweise Überlastung → nur Meldung/Warnung an Netzführung; Betriebspersonal entscheidet.
  - Erdschlussströme → werden begrenzte Zeit toleriert (solange Stromstärken im Rahmen); zunächst nur Meldung. Bei Folgefehler (Doppelerdschluss) → hohe Kurzschlussströme → autonome Reaktion der Schutztechnik.
  - Kurzschlüsse → autonome, vollautomatische Abschaltung ohne menschliche Beteiligung.
- Schutztechnik ist besondere Form der Automatisierungstechnik; zählt zur Sekundärtechnik.

Fünf Grundprinzipien für die Abschaltung von Kurzschlüssen:
1. **Sensitiv**: Fehler muss zuverlässig erkannt werden; vorteilhaft, wenn sich Betriebs- und Kurzschlussströme deutlich unterscheiden.
2. **Schnell**: Optimum: Stromkreisunterbrechung bevor Stoszkurzschlussstrom Maximalwert erreicht.
3. **Sicher**: funktionsredundante Auslegung sinnvoll (Haupt- und Reserveschutz); Ausfall eines Schutzgeräts wird durch vorgelagerte Schaltgeräte oder parallel arbeitende Fehlererfassungseinrichtungen kompensiert.
4. **Selektiv**: möglichst nur fehlerbehaftete Komponenten herausgetrennt, Rest des Netzes bleibt versorgt.
5. **Wirtschaftlich**: Kostenbetrachtung der technischen Lösung.

Messprinzip Schutztechnik:
- Schutzeinrichtungen messen und überwachen: Strom, Spannung, Impedanz, Leistungsflussrichtung, Temperatur (Schutzkriterien).
- Bei Grenzwertüber-/-unterschreitung: Schutzanregung.
- In NS-Netzen: Automaten mit Primärauslöser (im LS-Schalter: Bimetall- und Magnetauslöser, durchflossen vom Betriebsstrom; Sicherungen in NS und MS).
- Ab Hochspannung: keine Primärauslöser mehr; Messung und Überwachung über Strom- und Spannungswandler; analoge Signale werden weitergeleitet zur Verarbeitung (Ende des abgedeckten Textbereichs).
