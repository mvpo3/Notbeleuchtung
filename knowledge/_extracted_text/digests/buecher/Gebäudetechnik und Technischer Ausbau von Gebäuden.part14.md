# Gebäudetechnik und Technischer Ausbau von Gebäuden — Teil 14
> Quelle: Gebäudetechnik und Technischer Ausbau von Gebäuden (buecher) · Seiten 561-600.

Dieser Teil behandelt Fernmelde- und Informationstechnik (Kommunikation, Türanlagen, Antennen, Gefahrenmeldung, Datennetzwerke), Grundlagen der Gebäudeautomation (MSR, Bus-Systeme, GA-Systeme) sowie den Beginn des Kapitels Förderanlagen mit Aufzugsanlagen (Planung, Schallschutz, Typen, Abmessungen).

## Inhalt

### 6.2.2 Such- und Signalanlagen — Türöffner- und Türsprechanlagen

**Türöffneranlagen:**
- Standard-Türöffner geben die Türfalle durch einen eingebauten Elektromagneten im Schließblech frei, solange der Knopf gedrückt wird
- Varianten: mit Arretierung (Freigabe für einmaliges Öffnen auch nach Loslassen), mit Aufdruckfeder (Tür springt sichtbar auf), mit Entriegelung (für zeitgesteuerte Freigabe, z.B. Praxisräume)
- Türöffner-Kombinationen für wechselseitige Steuerung: Von mehreren Türen kann jeweils nur eine gleichzeitig geöffnet werden — Anwendung bei Schleusenvorräumen in Labors und Dunkelkammern
- Ruhestrom-Türöffner: umgekehrtes Prinzip — Falle gesperrt solange Spannung anliegt; Stromunterbrechung gibt frei → bei Stromausfall werden Türen entriegelt (Personenschutz/Fluchtweg)
- Türcode-Zutrittssysteme: numerische Tastatur, Kartenleser (Codekarte), Fingerabdruck-Lesegerät, Bluetooth/App-Steuerung; tageszeit- oder wochentagsabhängige Zugangsberechtigung möglich; Codierkartenanlagen ermöglichen einfache Umcodierung statt Schlosswechsel bei Verlust
- Berührungslose Schließanlagen (Transponder): Schlüsselanhänger oder Codekarte wird in ca. 5 cm Abstand vor Leseeinheit geführt; über 4 Millionen Codemöglichkeiten; Auswerteeinheit befindet sich im gesicherten Innenbereich; System ohne Zentrale, jede Tür ist eigenständige Einheit; Fingerabdruck-Erkennung verfügbar, auch für Einfamilienhäuser

**Türsprechanlagen:**
- Pflicht: Mehrfamilienhäuser ab 3 Wohnungen sind gemäß DIN 18 015-2 mit Türsprech- und Türöffneranlagen auszustatten
- Wechselsprechsystem: Sprechrichtung wechselt durch Tastendruck; gleichzeitiges Sprechen nicht möglich; Wandlautsprecher mit Sprechtaste und Türöffnertaste
- Gegensprechsystem: Handapparat mit abnehmbarem Hörer; beide Seiten können gleichzeitig sprechen
- Außensprechstelle enthält Namensschilder, Klingelknöpfe und Briefkästen in einer Frontplatte; Netzanschlussgerät (Transformator 6, 8 oder 12 V) i.d.R. im Stromkreisverteiler untergebracht
- Ab Netzanschluss: Ethernet-Verkabelung, empfohlen CAT-7a, ermöglicht spätere Umrüstung auf IP-basierte Anlagen mit Videoübertragung

**Ethernet-Kabelkategorien:**
- CAT 5: 100 MHz Betriebsfrequenz, Standardkabel für strukturierte Netzwerkverkabelung
- CAT 6: bis 250 MHz, bevorzugt für Sprach- und Datenübertragung
- CAT 6a: bis 500 MHz
- CAT 7 (Klasse F): bis 600 MHz, globaler Standard (außer USA), 4 separat abgeschirmte Aderpaare + Gesamtschirm, für 10-Gigabit-Ethernet geeignet
- CAT 7a (Klasse FA): bis 1000 MHz

**Türsprechanlagen mit Bildübertragung:**
- Kamera mit Weitwinkelobjektiv + Monitor in der Wohnung
- Aktivierung der Kamera automatisch bei Klingelknopfdruck
- Abschaltung automatisch nach Türöffner-Tastendruck oder nach Zeitablauf (50 s bis 3 min)
- Mindesthelligkeit für Kameraaufnahme: ca. 20 lx, sichergestellt durch Dämmerungsschalter oder Schaltuhr mit Außenbeleuchtung (Objektiv nicht anstrahlen!)
- Kameraaufnahmen können aufgezeichnet werden; Anschluss an 230-V-Netz erforderlich
- IP-basierte Einbindung über Bus-Systeme und Smartphone/Tablet via WLAN möglich

**Videoüberwachungsanlagen:**
- Kontrolle schwer einsehbarer Bereiche: Notausgänge, Tiefgaragen, Kurzparkflächen, gefährdete Bereiche
- Von Zentrale ausgehend Leerrohrnetze einplanen (Steuerleitungen + Datenleitungen)
- Übertragung auf mobile Endgeräte und über WLAN möglich; Datenaufzeichnung auf Festplatten

### 6.2.3 Zeitdienstanlagen

- Aufbau klassisch: Hauptuhr (Mutteruhr) + Nebenuhren; DCF77-Funkempfänger angeschlossen (Langwellensender in Mainflingen bei Frankfurt, versorgt Westeuropa mit gesetzlicher Zeit)
- Automatische Sommer-/Winterzeitumstellung durch DCF-Empfänger
- Moderne IP-Uhrenanlagen: IP-Uhren über sternförmige Ethernet-Verkabelung mit PoE (Power over Ethernet) versorgt; kein klassischer Mutteruhrenapparat mehr; PoE-Switche stellen NTP-Protokoll-Signal bereit
- Zeiterfassungsanlagen: elektronische Kartenlesegeräte, RFID-Identifikationssysteme; Erfassung fester und gleitender Arbeitszeiten; gekoppelt mit Zutrittskontrolle (Fingerscanner, elektronischer Schlüssel, Codeschlösser, Radar-Bewegungsmelder)

### 6.2.4 Sprech- und Datenfunksystem (Digitalfunk BOS)

- Pflicht für Gebäude mit hohen Sicherheitsanforderungen: Versammlungsstätten, Gebäude der öffentlichen Sicherheit und Versorgung, besondere Brandschutzauflagen
- Nutzung ausschließlich für Behörden und Organisationen mit Sicherheitsaufgaben (BOS)
- Gebäudebeschaffenheit (Stahlbeton, metallbedampfte Fenster) und Entfernung zur Basisstation können die Innenversorgung einschränken → zusätzliche technische Maßnahmen nötig
- Kleine Gebäude: passive Versorgung durch Außensignal kann ausreichen
- Größere Objekte: komplexe Objektfunkanlage zur Innenverteilung; ggf. eigene Basisstation
- Anforderungen werden im Baugenehmigungsverfahren von der Genehmigungsbehörde festgelegt
- Leitfaden: L-OV der BDBOS (Stand 2019)

### 6.2.5 Fernseh- und Antennenanlagen

**Empfangsarten:**
- Terrestrische Antennen
- Breitband-Kommunikationsanschluss (Kabelfernsehen, BK-Netz)
- Satellitenantennen (Parabolantenne)
- IPTV (Internet Protocol Television)

Leerrohr zwischen oberstem Geschoss und Kellergeschoss empfohlen für spätere Umrüstung ohne Stemmarbeiten.

**Terrestrische Antennenanlagen:**
- Empfangssignalleistung unter 0,000.001 W → Filterung, Aufbereitung, Verstärkung nötig
- Aufbau Hochantenne von oben nach unten: LMK-Antenne (Lang-/Mittel-/Kurzwelle) als Stabantenne mit Prasselschutzkugel, UKW-Antennen, Fernsehantennen
- Anordnungsregeln: mind. 5–8 m Abstand zu Nachbarantennen (gegenseitige Abschirmung); auf straßenabgekehrter Seite (weniger Störnebel); möglichst hoch (bessere Feldstärke, weniger Störnebel)
- Abstand zu Starkstromfreileitungen: mind. 1 m
- Befestigung an Schornsteinen: konstruktiv möglich, aber wegen korrosiver Abgase generell zu vermeiden
- Auf Dächern mit weicher Bedachung (Reet, Stroh, Schilf): Antennen verboten; Mindestabstand zu weicher Bedachung: 1 m
- Unterdach-Antennen: Abschirmeffekt, insbesondere bei nasser Dachoberfläche oder Alukaschierungen zwischen Sparren

**DVB-T2:**
- Digitale Hörfunk- und Fernsehübertragung über terrestrische Funkausstrahlung
- Empfänger (DVB-T2 Receiver) i.d.R. in Fernsehgeräten integriert
- In Deutschland seit 2017 nach DVB-T2-Standard (ETSI); Vorgänger DVB-T seit 2009 vollständig digital; konventioneller analoger Fernsehempfang seit 2009 abgeschaltet
- Kostenfreier Empfang ohne Anschluss an zentrale Anlagen

**Antennenbefestigung:**
- Rohrdurchführung durch Dachhaut muss regensicher sein; bei Schuppen-Dächern Dacheinführungsbleche verwenden; bei Flachdächern Hülsenrohre + Manschetten
- Antennenmasten bis 6 m Länge: eingespannter Teil ≥ 1/6 der freien Mastlänge (DIN EN 50 083-1); Biegemoment an Einspannstelle max. 1650 Nm (inkl. Windlast)
- Bei Überschreitung: Statiker hinzuziehen; Ausgangsdaten in DIN EN 50 083-1, Ziff. 11.3

**Antennenkabel:**
- Koaxialkabel in Isolierrohren NW 16 mm bevorzugt
- Koaxialkabel: kunststoffummantelter Leiter mit doppeltem metallischem Abschirmgeflecht
- Verlegung direkt in Putz nicht zulässig; Rohrinstallation erforderlich (auswechselbar gem. DIN 18 015-1)
- Gemeinsame Verlegung mit 230-V-Leitungen in Wandschlitz zulässig: ohne Isolierrohr Mindestabstand 10 mm, besser mind. 30 cm (insbesondere bei Aufzugsanlagen mit hohen Störspannungen)
- Gemeinsame Verlegung mit Fernmeldeanlagen der Telekom im Wandschlitz zulässig, aber NICHT im gemeinsamen Leerrohr
- Antennenträger auf Gebäuden: kurzschlussiger Weg erden (z.B. Fundamenterder); geeignete Erdungsanschlüsse: durchgehende metallische Wasser- oder Heizungsleitungen, leitfähig durchverbundene Stahlskelette/Armierungen (nicht Spannbetonbewehrung), metallische Bekleidungen
- Abwasser- und Regenfallleitungen: meist ungeeignet für ausreichende Erdungsleitung
- Erdung entfällt bei Unterdach-Antennen
- Antennen- und Erdungsleitungen nicht durch Räume mit leichtentzündlichen Stoffen (Heu, Stroh) oder explosionsfähiger Atmosphäre führen

**Antennenanschlussdosen:**
- Nichtwohnungsbau: in Räumen mit informatorischer Funktion (Schulungs-, Konferenz-, Direktionsräume)
- Wohnungen: in allen Räumen vorzusehen; kombinierte Zweibuchsendose für Hörfunk + Fernsehen
- Anzahl nach DIN 18 015-2: bis 3 Aufenthaltsräume (inkl. Küche) mind. 1 Antennensteckdose; ab 4 Aufenthaltsräumen mind. 2; darüber hinaus mind. 3
- Zu jeder Antennensteckdose gehören 3–4 Netzstrom-Steckdosen (230 V) für Unterhaltungselektronik
- Kombination 230 V + Antennendose in gemeinsamem Rahmen nur zulässig wenn nach Entfernen der Abdeckung der Starkstromteil weiterhin berührungsgeschützt bleibt; räumliche Trennung bevorzugt

**Gemeinschaftsantennen-Anlagen:**
- Technisch und wirtschaftlich besser als Einzelantennen; benötigen Verstärkereinrichtung nahe der Empfangsantenne (Stromversorgung über 230-V-Steckdose)
- Verstärker: erschütterungsfrei, nicht zu warm aufstellen; Stromverbrauch über Gemeinschaftszähler
- Drei Verteilernetz-Varianten:
  - Durchschleifverfahren: bevorzugt bis ca. 12 Dosen (6 Doppeldosen) pro Strang
  - Stichleitungsverfahren: besonders bei nachträglichem Einbau in Altbauten
  - Verzweigungsverfahren: wenn Stammleitung nicht ausreicht (größere Objekte)
- Anschlussschnüre Regellänge 1,20 m; bei Mehrfamilienhäusern bauseitig stellen (unabgeschirmte Leitungen stören andere Teilnehmer)
- Erdkabel: 50–80 cm tief in Sand eingebettet, mit Kabelsteinen abgedeckt

**Breitband-Kommunikationsnetz (Kabelfernsehen):**
- Unterirdisch verlegtes BK-Kabelnetz; Übergabepunkt im Keller mit Verstärker (ab ca. 3 Wohneinheiten) und Verteiler
- Sternförmig von Keller zu Wohnungen über Leerrohre + Koaxialkabel
- Verteiler in jederzeit zugänglichen Räumen (Flure, Treppenräume)
- Hausverteilungsanlagen sollen so ausgelegt werden, dass späterer BK-Anschluss möglich ist

**IPTV:** Fernseh- und Rundfunkempfang über DSL oder VDSL; häufig als Triple-Play-Paket (Telefonie + Internet + TV)

**Satellitenantennen:**
- Wichtigste Satelliten für Deutschland: im Südosten, 13° (Norddeutschland) bis 40° (Süddeutschland) Höhe über Horizont
- Quasi-optische Sichtverbindung erforderlich; Geäst stört bereits den Empfang
- Genehmigungspflicht ab bestimmter Größe (keine bundeseinheitliche Regelung); Berlin und NRW: Grenze bei 1,20 m Durchmesser
- Mindestdurchmesser: ca. 60 cm; ab 4 Teilnehmern 75 cm; darüber 90 cm
- Betonsockel mit frostsicherem Fundament empfohlen für Antennen ab 1,20 m; Schneeentfernung im Winter sicherstellen
- Gemeinschaftsanlagen: mehrere Parabolantennen; terrestrische Anlage kann entfallen

### 6.2.6 Gefahrenmelde- und Alarmanlagen

**Allgemein (DIN VDE 0833-1):**
- Gefahrenmeldeanlagen unterscheiden: Brandmeldeanlagen (BMA), Einbruchmeldeanlagen (EMA), Überfallmeldeanlagen (ÜMA)
- VdS-anerkannte Anlagen: müssen VdS-Richtlinien entsprechen und von anerkannten Fachfirmen errichtet werden; VdS-Kennzeichnung mit Anerkennungs-Nr. und Klasse außen am Gerät

**Brandmeldeanlagen (BMA):**

Automatische Brandmelder:
- Deckenbereich des Schutzraums; runde Elemente ca. 4–11 cm Durchmesser
- 1 Melder je ca. 20–80 m² Grundfläche als Richtwert
- In Luftkanälen oder Kabelböden: Revisionsöffnungen erforderlich

| Meldertyp | Wirkprinzip | Besonderheiten |
|---|---|---|
| Ionisationsrauchmelder | Verbrennungsgase (Frühwarnung) | Ungeeignet: >+50°C, <−20°C, Luftgeschwindigkeit >5–10 m/s, starke Erschütterungen |
| Optischer Rauchmelder (Streulicht) | Sichtbarer Rauch, etwas später als Ionisation | Reagiert auch auf PVC-Kabelrauch; häufig mit Ionisationsmeldern kombiniert |
| Flammenmelder | Flackerfrequenzen offener Flammen | Erst bei offenen Flammen; meist mit Rauchmeldern kombiniert |
| Thermomaximal-Melder (Schmelzlot) | Auslösetemperatur meist 70°C (ca. 50 K über Raumtemperatur) | Kaum Fehlalarme, reagiert träge; mit Rauch-/Flammenmeldern kombiniert |
| Thermodifferential-Melder | Temperaturanstieg z.B. 10 K/min über mind. 2 min oder 1 K/min über mind. 30 min | Geeignet für Räume mit stark schwankenden Temperaturen; mit Thermomaximalmeldern kombiniert |
| 3D-/4D-Brandmelder | Mehrere Sensorprinzipien kombiniert | Dezentrale Intelligenz, eigenständige Branderkennung; Fehlalarmrate nahezu null; Nutzungsänderung erfordert meist keine Anlagenänderung |

Nichtautomatische Brandmelder: Rot gekennzeichnete Druckknopfmelder unter Glas; je Geschoss im Treppenraumbereich oder an Fluchtwegen; wo großer Personenverkehr ist, kann auf automatische Melder verzichtet werden (z.B. Versammlungsstätten)

**Brandmeldezentralen:**
- Nehmen Stör- und Alarmmeldungen entgegen; steuern: Feuerschutztüren/Brandklappen in Luftkanälen, Sprinkleranlagen, Notstrom- und Druckerhöhungsanlagen
- Standort: beim Pförtner oder Kontrollinstanz; direkte oder vermittelte Weiterleitung an Feuerwehr
- Feuerwehreinsatzpläne vorzuhalten
- Notstromversorgung: bei Netzausfall 72 Stunden durch wartungsfreie Batterien sichergestellt
- BMA-Leitungen gemeinsam mit anderen Leitungen: rote Kennzeichnung an Klemmen, Abzweigdosen und Verteiler

**Einbruchmeldeanlagen (EMA):**

Vier Gruppen:
1. Freigeländeüberwachung (Perimeter)
2. Gebäudeaußenhaut (Wände, Fenster, Türen)
3. Innenräume
4. Gegenstände (Objektüberwachung)

Vier Sicherheitsgrade gem. DIN VDE 0833-3 und DIN EN 50 131-1:
- Grad 1: niedriger Sicherheitsgrad
- Grad 2: niedriger bis mittlerer Sicherheitsgrad
- Grad 3: mittlerer bis hoher Sicherheitsgrad
- Grad 4: hoher Sicherheitsgrad

**Freigeländeüberwachung:**
- Zäune mit zug- und druckempfindlichen Sensoren
- Unterirdisch verlegte HF-Kabelpaare (elektromagnetisches Feld); Abstand zu Elektroleitungen und metallischen Rohrleitungen/Zäunen: 1,5–2 m; Detektionszone zwischen Kabeln ca. 1,50 m Breite, 15–30 cm Tiefe
- Infrarot-, Ultraschall- oder Mikrowellenschranken
- Passiv-Infrarotmelder im Freien: nur Abschreckung, NICHT an EMA anschließen; Montage ca. 2,5 m Höhe; Einschaltdauer: 15 s bis 15 min einstellbar; Reichweite frontal ca. 16 m, seitlich ca. 6 m; Erfassungswinkel einstellbar bis 220°; Mindestabstand zu geschalteter Beleuchtung: 1,5 m

**Fensterschutz:**
- Magnetkontakte (Reed-Kontakte): ca. 10 cm lange stabförmige Teile; Kontaktteil am Rahmen, Magnetteil am Flügel; nichtferromagnetisches Befestigungsmaterial; Maximalabstand: 20 mm; sabotagesichere Varianten mit zweitem Kontakt für Fremdmagnet
- Rundriegelkontakte: ca. 8 mm/30 mm Durchmesser; verdeckt in Fälzen anordbar
- Aufdruckbolzen: bei VdS-Klassen B und C für Fenster (unverriegelte Flügel werden aufgedrückt; für Türen ungeeignet wegen Falle)
- Schließblechkontakte (Riegelschaltkontakte): kontrollieren ob Riegel ausgefahren (Türen); Bodenriegelkontakte für Ganzglastüren

**Glasbruchmelder:**

Passive Glasbruchmelder:
- Schachtelgröße (ca. Streichholzschachtelgröße); auf Scheibeninnenseite geklebt
- Reagieren auf Schallspektrum hoher Frequenzen beim Bersten
- Überwachungsradius: max. 1,5 m (unabhängig von Glasdicke)
- Abstand zum Rahmen: mind. 2 cm; flexible Anschlusskabel bandseitig verlegen
- Nur für Doppelverglasungen (Isolierglas, Doppelfenster); außerhalb Handbereich auch Einscheibenverglasung
- Ungeeignet für: Verbundsicherheitsglas, Strukturglas, Glas mit Drahteinlage

Aktive Glasbruchmelder:
- Zwei Kriterien müssen gleichzeitig erfüllt sein: Glasbruch-Frequenzauswertung + Glasveränderungsauswertung (ständige Schwingungsüberprüfung)
- Für alle Glasarten geeignet, teils auch Verbundglas
- Überwachungsradius: max. ca. 4 m; überwachte Fläche: max. ca. 50 m²; Abstand zum Rahmen mind. 5 cm

Akustische Glasbruchmelder:
- Mehrere Scheiben/Fenster mit einem Gerät überwachbar (inkl. Sprossen, Oberlichter, Dachfenster)
- Deckenmontage möglich; max. Abstand zur Glasfläche: ca. 3,5 m
- Reagiert auf Klirrfrequenzen beim Bruch + Splitter auf Boden + Druckänderung im Raum
- Abmessungen: ca. 7×10×4 cm; min. Abstand 0,40 m von Unterkante Melder zu Oberkante Glasfläche
- Ungeeignet für Sicherheitsverbundglas und drahtverstärkte Gläser
- Nicht gegenüber Ultraschallquellen montieren; nur für VdS-Klassen A und B zugelassen

**Alarmglas:**
- Variante 1 — Alarmdrahteinlage: Verbundsicherheitsglas mit mäanderförmigem Feinsilberdraht in Folienschicht; Fadenabstand 2–10 cm; bei Glasbruch reißt Draht → Alarm; hoher mechanischer Widerstand
- Variante 2 — Alarmschleife (Alarmspinne): Verbundsicherheitsglas innen + Einscheiben-Sicherheitsglas außen; in oberer Ecke eingebrannte elektrische Leiterschleife; bei Zerstörung zerfällt Außenscheibe in Krümel → Stromkreis unterbrochen → Alarm
- Transport/Lagerung: Alarmscheiben dürfen NICHT auf Anschlussstelle gestellt werden

Weitere Melder:
- Überwachungsfolien: 6–10 mm breite Metallstreifen, unter Tapeten oder unter Lichtkuppeln als Strompfad
- Fadenzugkontaktmelder: dünne Drahtverspannungen; bei Auslenken oder Reißen → Alarm; max. zulässige Drahtlänge gem. VdS: 3 m; unter Lichtkuppeln, in Lüftungsschächten, Kabelkanälen

**Wandschutz:**
- Durchbruchmelder (Alarmdrahttapeten): parallele Kupferdrähte in bituminiertem PE-beschichtetem Papier; Drähte reißen bei Mauerdurchbruch → Alarm; gute Fehlalarmsicherheit
- Überwachungsfolien: 6–10 mm breite Metallstreifen unter Tapeten (Leichtwände)
- Körperschallmelder: reagieren auf Bohrer, Meißel, Trennscheibe, Sauerstofflanze an Massivwänden; bevorzugt für Tresorräume; hoher Widerstandszeitwert; bei Umwelteinflüssen (Fahrzeuge, U-Bahn) Sensibilität reduzieren; gem. VdS: von außen zugängliche Flächen NICHT mit Körperschallmeldern überwachen

**Innenraumüberwachung — Bewegungsmelder:**

Passive Infrarot-Bewegungsmelder (PIR):
- Sensor reagiert auf Änderungen der Wärmestrahlung; fächerförmige Aufteilung in empfindliche/unempfindliche Zonen
- Keine Tiere im Überwachungsbereich; kein Anstrahlen des Melders; nicht auf reflektierende Gegenstände richten
- Fehlalarmquellen: Fußbodenheizung, Ventilatoren, Lüftungsöffnungen, Elektrospeicherheizung
- Montage: obere Raumecke an Außenwand, nach unten geneigt reduziert Fehlalarme
- Nicht auf Außenfenster/-türen ausrichten; mehrere Melder in einem Raum ohne gegenseitige Beeinflussung möglich
- Erfassungsbereich: bis 220° breitflächig oder schmale Schneisen; Vorhangmelder: Raumtrennung bis 5×5 m Fläche (Wand-zu-Wand, Boden-zu-Decke)

Ultraschall-Bewegungsmelder:
- Aktiv: sendet und empfängt akustische Wellen im unhörbaren Bereich (Doppler-Prinzip)
- Dreidimensionaler ovaler Erfassungsbereich; einstellbare begrenzte Reichweite
- Fehlalarmquellen: Luftturbulenzen, Thermostatventile, Druckluftgeräte, pendelnde Schilder/Leuchten
- Wegen Störanfälligkeit fast nur noch als Dualmelder (kombiniert mit IR) eingesetzt

Dual-Bewegungsmelder: Kombination IR + Ultraschall oder Mikrowellen; Alarm erst bei übereinstimmender Erkennung beider Systeme

Mikrowellen-Bewegungsmelder (Radarmelder):
- Gleiche Wirkung wie Ultraschall, aber mit elektromagnetischen Hochfrequenzwellen
- Durchdringen nichtmetallisches Material → Vorsicht bei dünnen Wänden, Glas (Straßenverkehr, Aufzüge, Abwasserrohre können ungewollt ansprechen)
- Absolute Raumbegrenzung nur bei Faradayschem Käfig; selten in Innenräumen eingesetzt

Lichtschranken:
- Infrarotlicht-Sender + IR-Empfänger; Unterbrechung → Alarm; durch Spiegel zu Gittern umlenken
- Fallenmelder in Fluren: ca. 50–60 cm über Boden; Reichweite Innenmontage 100–150 m
- Nicht direkt von Sonnenlicht bescheinen; impulsweise zerhackte Strahlung verhindert Überlistung durch Taschenlampe
- Fehlalarmquellen: Luftströmungen, Staub, schneller Temperaturwechsel

**Objektüberwachung:**
- Magnetkontakte, Körperschallmelder (für Panzerschränke)
- Bildermelder: zug- und schubempfindliche Sensoren reagieren auf Gewichtsveränderung (Bild/Objekt)
- Faseroptische Melder: Glasfaser-Lichtwellenleiter mit gepulstem Licht; Beschädigung → Signalabschwächung → Alarm; max. Länge ca. 3000 m
- Kapazitive Feldüberwachung: statisches hoch- oder niederfrequentes Wechselfeld zwischen Objekt und metallischer Umgebung; Annäherung einer Person verändert Feldverhältnisse → Alarm; hohe Anlagekosten → nur für sehr hochwertige Objekte (Panzerschränke); Boden und Wände mit Blech/Metallfolie/Drahtgeflecht abschirmen

Kontaktmattenmelder: unter Teppichbelägen; zuverlässig gegen Erschütterungen, Luftturbulenzen, Temperatureinflüsse; geringe Überlistungsmöglichkeit; hohe Überwachungsqualität

**Überfallmelder:**
- Druckknopfmelder; stiller oder externer Alarm (Sirenen + Blinkleuchte)
- Für Außenstehende nicht erkennbar (z.B. Kassenraum); Fußkontaktschienen durch Anheben der Fußspitze betätigbar
- Wohnungen: im Schlafraum oder Eingangsbereich

**Übertragungswege:**
- Leitungsverbindungen oder Funk; Ruhestromprinzip: Leitungen ständig von Strom durchflossen; Unterbrechung oder Veränderung wird sofort registriert
- Wechselnde Modulation erhöht Sabotagesicherheit; Sabotagemeldelinien überwachen Meldelinien selbst (gemeinsame Umhüllung)
- Leitungen in Leerrohren verlegen; eigenes Leerrohrnetz (nicht mit anderen Schwachstromsystemen teilen)
- Abstand zu 230/400-V-Leitungen: mind. 30 cm (ggf. mehr)
- Kabelverbindungen: gelötet (nicht geklemmt, da Klemmverbindungen Sicherheitsanforderungen nicht genügen)
- Empfehlung: GMA bei Neubauten frühzeitig planen (Leitungskosten ≈ so groß wie übrige Anlageteile)

**Schalteinrichtungen:**
- Scharfschaltung bei Verlassen/Betreten des Objekts
- Interne Scharfschaltung: Schlüssel + Tastatur am Zentralgerät; Verzögerungszeit ca. 20 s bis mehrere Minuten; Alarm nach Ablauf
- Blockschloss (externe/zwangsläufige Scharfschaltung): kombiniert mechanisches Türschloss + elektronische Scharfschaltung; Scharfschalten nur bei betriebsbereiter Anlage und geschlossenen Fenstern/Türen möglich; nur von außen; ergänzend Türcodegerät (geistiger Verschluss) für Klassen 3 und 4
- Blockschloss-Variante: Zugangskontrolle auf bestimmte Personen, Tage, Uhrzeiten; Protokollierung des Schließvorgangs
- Kontaktschloss: Zylinderschließvorrichtung neben der Tür; nur für Klasse 1
- Riegelschaltschloss: mechanisches Türschloss + elektronische Scharfschaltung kombiniert; preisgünstige Alternative zu Blockschloss für private Nutzung; nur VdS-Klasse A (keine Zwangsläufigkeit)

**Zentralen:**
- Vergleichende Beurteilung einlaufender Meldungen; Lokalisierung des Alarmorts
- Wartungsfreie Batterien im Gehäuse: unterbrechungslose Versorgung bei Netzausfall
- Gehäuse sabotageüberwacht; an massiver Wand befestigen; muss selbst im Überwachungsbereich eines Einbruchmelders liegen
- Betriebsspannung meist 12 V (aus 230-V-Netz); eigener Stromkreis

**Alarmierung:**
- Extern: Sirene + Blinkleuchte (örtlich abschreckend); intern (Personen im Objekt); still (telefonisch)
- Über 90% aller Alarme privater EMA sind Fehlalarme → nur hochwertige Anlagen installieren
- Standardbestückung: mind. 2 getrennte akustische Signalgeber (mind. 3 m Höhe) + optischer Signalgeber
- Akustische Signalgeber: max. 3 min aktiv
- Optische Signale (Blink-/Blitzleuchten, Außenbeleuchtung): zeitlich unbegrenzt, bis manuelle Rückstellung
- Stiller Alarm / Fernalarm: Wählgerät ruft automatisch vorprogrammierte Teilnehmer (Nachbarschaft, Überwachungsdienst)

Alarmübertragungsoptionen:
- Nur externer Alarm: keine Sicherheit dass Hilfe kommt
- AWAG (Automatisches Telefonwähl- und Ansagegerät): ruft Nachbarn/Hausmeister an; nicht protokolliert; von Überwachungsfirmen für gewerbliche Objekte meist nicht akzeptiert
- AWUG (Automatisches Wähl- und Übertragungsgerät): Vertrag mit Überwachungsunternehmen; codierte Zuordnung; überträgt: scharf/unscharf, Störungen, Voralarm, Einbruch, Überfall, Routineruf; protokolliert + quittiert; mehrmals täglich Testanrufe
- Festverbindung: angemietete Telekom-Leitungen direkt zur Notrufzentrale; sicherste Methode; nur für besonders schutzbedürftige Objekte (Banken, Juweliere)

**EMA-Symbole gem. VdS-Richtlinie 2135 (Auswahl):**
- MK: Magnetkontakt; Gmak: akustischer Glasbruchmelder; Gmp: passiver Glasbruchmelder; Gma: aktiver Glasbruchmelder; KM: Körperschallmelder; ADG: Alarmglas; FÜ: Flächenüberwachung; LS: Lichtschranke; LV: Lichtschrankenvorhang; MS: Mikrowellenschranke; HFS: Hochfrequenzschranke; FK: Fadenzugkontakt; BM: Bildermelder; SK: Schließblechkontakt; SE: Blockschloss; SG: geistige Schalteinrichtung; AB: Aufdruckbolzen; DM: Druckmelder; FM: Feldänderungsmelder; IM: IR-Bewegungsmelder; IMM: Mikrowellen-Bewegungsmelder; UM: Ultraschall-Bewegungsmelder; DU: Dualmelder; ÜM: Überfallmelder; DK: Druckknopfmelder; V: Verteiler; ABF: abgesetztes Bedienfeld; AT: Anzeigetableau; EMZ: Einbruchmeldezentrale; ÜG: Übertragungsgerät (AWUG); EV: Energieversorgung; RE: Registriereinrichtung; SA: akustischer Signalgeber; SR: Sirene; SO: optischer Signalgeber (Rundumleuchte/Blitzleuchte)

**Einrichtung und Instandhaltung:**
- Frühzeitig mit VdS-zugelassenem Errichter, Überwachungsunternehmen und Versicherungsgeber abstimmen
- Wartungsintervalle: Klasse 1 jährlich; Klassen 2–4 vierteljährlich

### 6.2.7 Übertragungsnetze/Datentechnik

**Intranet:** Unternehmensinterne digitale Kommunikationsplattform; digitaler Campus; integration mobiler Endgeräte über Apps; geeignet für hybride Arbeitsmodelle

**Strukturierte Verkabelung:**
Drei Bereiche:
- Primärbereich (Backbone): Gebäudeverteiler ↔ Standortverteiler; überwiegend Lichtwellenleiterkabel
- Sekundärbereich: Standortverteiler ↔ Etagenverteiler; Kupferkabel oder LWL
- Tertiärbereich (Etagenverkabelung): Etagenverteiler ↔ Datenanschlussdosen; max. Länge ca. 90 m

Netzformen: sternförmig, ringförmig, Baumstruktur, vermascht (höchste Sicherheit)

Dienste: Sprach-/Daten-/Bildübertragung, Zutrittskontrolle/Zeiterfassung, MSR Gebäudetechnik, Beleuchtungssteuerung, Gebäudeüberwachung

**Anforderungen Räumlichkeiten:**
- Etagenverteiler-Schränke: Tiefe 100 cm; Arbeitsbereich vorn mind. 120 cm, hinten mind. 80 cm (Einzelfall 60 cm)
- Serverschränke: oft 120 cm Tiefe
- Verteilungsräume: mind. mechanisch be- und entlüften; ggf. klimatisieren je nach Anzahl aktiver Komponenten
- EDV-Hauptverteilerraum/Serverraum: Doppelboden + Klimatisierung zwingend; je nach Sensibilität mit BMA und ggf. Löschanlage; ggf. Zutrittskontrolle/EMA; Zusatzraum für USV, Stromversorgung, Lüftung/Klima (ggf. redundant)

### 6.3 Gebäudeautomation

#### 6.3.1 Mess-, Steuer- und Regelungstechnik

Aufgaben MSR:
- Überwachung und Sicherung gebäudetechnischer Prozesse (Raumklima)
- Stabilisierung und Führung aller Prozesse
- Optimierung ausgewählter Prozesse
- Energieeffizienter Anlagenbetrieb

Geregelte Größen in HLK: Temperatur, Feuchte, Druck von Luft und Wasser; weitere Regelungen: Volumenstrom, Feuchte, Kessel- und Kälteanlagen, thermische Speicher

**Steuerung vs. Regelung:**
- Steuerung: gerichtete Wirkung ohne Rückkopplung; Ausgangsgröße aus Eingangsgröße nach fester Gesetzmäßigkeit (Beispiele: Heizkurve — Vorlauftemperatur-Sollwert aus Außentemperatur; Zeitpläne — Sollwertvorgabe nach Wochentag/Tageszeit)
- Regelung: Regelgröße wird laufend gemessen, mit Sollwert (Führungsgröße) verglichen; bei Abweichung: Stellgröße anpassen bis Sollwert wieder erreicht; Regelkreis = geschlossener Wirkungskreis; Messumformer verstärkt und linearisiert Messgröße → Einheitssignale 0/4…20 mA oder 0…10 V

Wirksinn (Polarität): direkt (Regelgröße ↑ → Stellgröße ↑); invers (Regelgröße ↑ → Stellgröße ↓)

Drei Grundformen stetiger Regler:
- P-Regler (proportional, mit Ausgleich)
- I-Regler (integral, ohne Ausgleich)
- D-Regler (differenzierend)

Abgeleitete Reglerarten: P, I, PI, PD, PID

**Regler ohne Hilfsenergie:**
- Messenergiegewonnene Kraft zur Stellglied-Positionierung; direkt am Stellort eingebaut
- Thermostatische Heizkörperventile: Flüssigkeits- oder Festkörper-Ausdehnungssystem treibt Stelleinrichtung an; Vorspannung Rückstellfeder = Sollwertvorgabe

**Pneumatische Regelung:**
- Einsatz in explosionsgefährdeten Bereichen (kein Funken); erhöhte Anforderungen an Stellgeschwindigkeit/Krafteinsatz
- Industrielle Einheitsregler: pneumatisches Standardsignal 0,2–1,0 bar
- Heute kaum noch gegenüber digitalen Systemen gerechtfertigt

**Digitale Regler (Tabelle 6.32 — Leistungsmerkmale):**

| Leistungsmerkmal | Vorteil |
|---|---|
| Parallele Regelkreise über einen Regler | Reduzierter Hardware- und Installationsaufwand |
| Integrierte DDC-Funktionsmodule + grafische Konfiguration | Einfache Konfigurierbarkeit |
| Freie Auswahl Regelkreise zur Inbetriebnahme | Fehlerkorrektur vor Ort |
| Standalone-Betrieb mit Echtzeituhr, Zeitprogrammen | Zuverlässige nutzungsabhängige Vorgaben |
| Zusätzliche Rechenvorgänge und Ablaufsequenzen | Keine zusätzliche Hardware im Schaltschrank |
| E/A-Erweiterungsmodule für analoge und binäre Ein-/Ausgänge | Ein Gerät für viele Anwendungen, geringere Kosten |
| Integrierte Bedienblende mit LCD-Display | Lokale Anzeige und Handeingriff |
| Peer-to-Peer-Kommunikation (bis 30 Regler am Bus) | Wirtschaftliche Installation; abgestimmte Steuerung auch ohne Leitzentrale |
| Anbindung an Feldbusse und Automationsnetzwerke | Kommunikation mit anderen Busteilnehmern; Fernbedienung via Internet |
| Datenaufzeichnung | Liegenschaftsbetrieb, Energiemanagement, Fernüberwachung |
| Reduziertes Geräteprogramm | Weniger Fehlbestellungen, geringere Ersatzteilbestände |

Unterschied AS und SPS: Automationsstation (AS) = herstellerspezifische Sprache + vorgefertigte Applikationsmodule → schneller; SPS = IEC 61131-3-standardisierte Programmiersprachen, kürzere Verarbeitungszyklen

Digitale Regler: tasten Messwerte in regelmäßigen Abständen ab (kein kontinuierliches Messen); zwischenzeitlich Rechenvorgänge

Funktionsliste nach VDI 3814 Blatt 4.3 umfasst: physikalische Ein-/Ausgabefunktionen, Zeitpläne, Kalender, Alarm-/Ereignismeldungen, Datenaufzeichnung, Logik-/Zeit-/arithmetische Berechnungen, Regelungsfunktionen, Optimierungsfunktionen, Beleuchtungsfunktionen, Sonnenschutzfunktionen; Bedien- und Anzeigefunktionen; Grafik, Dynamisierung, Historiendatenbank

#### 6.3.2 Bus-Systeme

**Definition:** Bus verbindet alle Anlagen und Komponenten; ermöglicht Meldungen, Zustandsabfragen und Befehle; begrenzt in örtlicher Ausdehnung und Teilnehmerzahl → Netzwerkaufbau mit Segmenten nötig (Repeater, Bridges, Router zum Filtern)

Übertragungsmedien:
- Leitergebunden: metallisch (Twisted-Pair-Kupfer, Koaxialkabel); nichtmetallisch (Lichtwellenleiter)
- Leiterungebunden: hochfrequente magnetische Wellen (Funk/WLAN); Infrarotübertragung; Stromnetz (Powerline)

Vorteile Bus-Systeme:
- Geringer Verdrahtungsaufwand
- Geringer Geräteaufwand (Rundsteuerempfänger, Maximumwächter, Zeitschaltuhren, Lastabwurfrelais entfallen)
- Reduzierung der Brandlast (relevant in Rettungswegen)
- Kürzere Montagezeiten
- Energieeinsparung
- Keine Eingriffe in Verdrahtung bei Nutzungsänderung
- Einfache Netzerweiterungen
- Weniger Bedienungspersonal

**Hierarchie nach DIN 16484-2:**
- Feldebene: Sensoren, Aktoren, parametrierbare anwendungsspezifische Regel-/Steuereinheiten (z.B. Raumthermostat mit Sollwertverteilung und Raumtemperaturanzeige); Informationsaustausch zwischen Raumklima und Anlagentechnik
- Automationsebene: frei programmierbare leistungsfähige Automationsstationen; Steuern, Regeln, Überwachen, Aufzeichnen, übergeordnete Optimierungsaufgaben
- Managementebene: Bedien- und Engineeringstationen; zentrale Bedienung der Gebäudetechnik; Koordinierung und Ergebnisanalyse
- Verwaltungsebene (praktische Erweiterung): Anbindung an kerngeschäftliche Systeme (Analyserechner für Produktqualität, Hotelmanagementsysteme, Flugplanrechner)

**Standardisierte Protokolle:**
- BACnet (Building Automation and Control Network): ANSI/ASHRAE Standard 135; DIN EN ISO 16484-5; dominiert Automations- und Managementebene; unterstützt IP-Kommunikation; breite Objekttypenvielfalt
- LonWorks (Local Operating Network): Echelon Corporation; EN 14908 Control Network Protocol (seit 2005 europäisch genormt); Bandbreite 4,9 kBit/s bis 1 MBit/s; max. 32.285 Netzwerkknoten; auf Automationsebene weitgehend von BACnet verdrängt; hohe Anforderungen an Inbetriebnahme und Instandhaltung
- KNX (Konnex): EN 50090, ISO/IEC 14543; Zusammenführung von EIB, EHS und Batibus; Standard für Haus- und Gebäudesystemtechnik; besonders relevant für: Schalten von Leuchten, Jalousien, Stellantriebe Heizkörperventile, Schalter und Bediengeräte; weniger geeignet für zeitkritische Automationsaufgaben wie Druckregelung
- DALI (Digital Addressable Lighting Interface): Ansteuerung elektronischer Vorschaltgeräte, Beleuchtungsbereich
- SMI (Standard Motor Interface): Ansteuerung von Jalousiemotoren
- M-Bus (Meter Bus): Verbrauchsmessung Wärme, Gas, Strom, Wasser
- EnOcean, Modbus, OPC: weitere im Einsatz

#### 6.3.3 Gebäudeautomationssysteme (GA-Systeme)

- GA-System: mehrere Automationsstationen und MSR-Systeme verbunden mit Management- und Bedieneinrichtungen (MBE) über Datenübertragungsnetz
- Besteht aus: Bediengeräten, Serverstationen, Ausgabegeräten
- Analoge Systeme: hoher Aufwand für Datenerfassung und zentralverarbeitung; Bus-Systeme ermöglichen einfache zentrale Überwachung

Typische GA-Funktionen:
- Kontrolle der Außenluftrate bei RLT
- Raumtemperaturkontrolle
- Nutzung freier Kühlung
- Steuerung unterschiedlicher Wärme-/Kälteerzeugungssysteme
- Wärme-Kälte-Verschiebung
- Verbesserung der Jahresnutzungsgrade
- Überwachung CO₂-Konzentration
- Jalousiesteuerung
- Lastabwurfsteuerung
- Wärme- und Kältespeicherung
- Nachtauskühlung

---

## Kapitel 7: Förderanlagen — 7.1 Aufzugsanlagen (Seiten 583–600)

### Planung von Aufzugsanlagen

- Aufzüge sind primäre Elemente der Gebäudeplanung; zentrale Lage, i.d.R. gemeinsam mit Treppen und Installationsschächten im Gebäudekern
- Verkehrsberechnung (auch überschläglich) zur Ermittlung von Anzahl und Art der Aufzüge
- Öffentliche Gebäude: Richtlinie "Aufzug 2022" des Arbeitskreises Maschinen- und Elektrotechnik staatlicher und kommunaler Verwaltungen (Stand Jan. 2022)

Rechtliche Grundlagen:
- Europäische Aufzugsrichtlinie 2014/33/EU
- Maschinenrichtlinie RL 2006/42/EG
- Zwölfte Verordnung zum Produktsicherheitsgesetz (12. ProdSV) zur Umsetzung 2014/33/EU
- DIN EN 81: Sicherheitsregeln für Konstruktion und Einbau von Aufzügen
- DIN ISO 8100-30: Personenaufzüge in Wohngebäuden und anderen Gebäuden

**Aufzugspflicht nach Bundesland (Auswahl):**
- Baden-Württemberg, Bayern, Brandenburg, Hamburg, Hessen, Mecklenburg-Vorpommern, Saarland, Sachsen, Sachsen-Anhalt, Schleswig-Holstein, Thüringen: ab Gebäudehöhe >13 m (Bayern: ab 13 m über Fußboden Aufenthaltsraum, entspricht Musterbauordnung)
- Berlin: ab 4 oberirdischen Geschossen
- Bremen: ab Gesamthöhe >10,25 m
- Niedersachsen: ab >12,25 m über Eingangsebene
- NRW, Rheinland-Pfalz: ab >5 Geschossen über Geländeoberfläche

Mindestanforderungen:
- Mindest-Fahrkorbgrundfläche: 1,10 m × 2,10 m
- Fahrkorbgrundfläche für Rollstuhl: 1,10 × 1,40 m
- Lichte Mindest-Türbreite für Krankentragen/Rollstühle: 90 cm
- Hochhäuser: mind. 2 Aufzüge vorzusehen
- Bewegungsfläche vor Fahrschachtzugängen für Krankentragen: mind. 2,30 m Tiefe; Wohngebäude: mind. 1,50 m; Nichtwohngebäude: mind. 1,5-fache Fahrkorbtiefe
- Öffentliche Gebäude (DIN 18 040): mind. 1 Aufzug rollstuhlgeeignet, Fahrkorbgrundfläche ≥ 1,10 × 1,40 m, lichte Türbreite mind. 90 cm; Bewegungsfläche vor Türen mind. 1,50 × 1,50 m; KEINE Anordnung gegenüber abwärtsführenden Treppen/Rampen
- Ab 5 bzw. 6 Geschossen (landesrechtlich): Fahrkorb 1,10 × 2,10 m für Krankentrage vorgeschrieben

### Schallschutz bei Aufzugsanlagen

- Schallübertragung von Fahrkorb, Türen, Schalt-/Anfahrgeräuschen auf Aufenthaltsräume
- Schachtwände: flächenbezogene Masse nach DIN 8989 Tab. 4 einhalten (Tab. 7.2)
- Sicherer Schallschutz: vollständige Trennung Schacht vom Baukörper durch Trennfuge mind. 3 cm Breite
- Keine schutzbedürftigen Räume an einschalige Schachtwände angrenzend
- Schallschutzverantwortung: Rohbauausführung + Planung (nicht Aufzugslieferant)
- Nachträgliche Verbesserungsmaßnahmen i.d.R. nicht erfolgreich

**Grenzwerte nach DIN 4109:**
- Wohn-/Schlafräume: max. 30 dB(A) durch Fahrbetrieb
- Unterrichts- und Arbeitsräume: max. 35 dB(A)
- Gilt auch für Kranken-/Hotelzimmer und sonstige nachts genutzte Aufenthaltsräume im Nichtwohnungsbau
- DIN 8989: Schallschutz bei Aufzügen bis 2500 kg Nutzlast und max. 4 m/s Beschleunigung; höhere Werte: Einzelfallprüfung

**Schallemissionskennwerte Tabelle 7.1 (max. Beschleunigungspegel, einzuschalige Bauteile, Situation A/B/C):**

Schallschutzziel DIN 4109 LAFmax,n ≤ 30 dB:
- Raumvolumen bis 31,25 m³ → Oktave 63 Hz: A=90 dB, B=75 dB, C=85 dB; 125 Hz: A=86/B=71/C=81; 250 Hz: A=85/B=70/C=80; 500 Hz: A=85/B=70/C=80
- Raumvolumen bis 62,5 m³: Werte je 3 dB geringer
- Raumvolumen bis 125 m³: nochmals 3 dB geringer

Max. A-bewerteter Schalldruckpegel:
- Triebwerksraum: 80 dB(A) / 77 dB(A) / 74 dB(A) (Klasse A/B/C)
- Im Schacht (Aufzüge mit TWR): 65 dB(A) für alle Klassen
- Im Schacht (ohne TWR): 75/72/69 dB(A)
- Vor Schachttüren beim Öffnen/Schließen: 65/62/59 dB(A)
- Vor Schachttüren bei Vorbeifahrt: 65/62/59 dB(A)

**Flächenbezogene Massen Tab. 7.2 (Bauteilanforderungen):**

| Bauteil | Einschalig | Zweischalig Innen/Außen |
|---|---|---|
| Schachtwände (Situation A, DIN 4109 ≤30 dB, bis 31,25 m³) | 490 kg/m² (Situation A), 580 kg/m² (Situation B) | Innen 380 kg/m², Außen 250 kg/m² |
| TWR-Wände (Situation B) | 490 kg/m² | — |
| Treppenraumwand | 380 kg/m² | — |
| Unmittelbar verbundene Decken (Situation B) | 300 kg/m² | — |
| Flankierende Wände (Situation B) | 220 kg/m² | — |
| Zweischaliger Schacht: Schalenabstand ≥ 30 mm + Mineralwolledämmplatten DIN EN 13162 WTH nach DIN 4108-10 |

### Sicherheit

- Seilaufzüge: mehrere mehrlitzige Seile; Sicherheitsfaktor gem. DIN EN 81-1; Beispiel: 2 Seile = Faktor 16, 3 Seile = Faktor 12
- Notfall-Auslösung: bei Überschreitung der Nenngeschwindigkeit um 15% → automatische Fangvorrichtung (Notbremsung)
- Fangvorrichtung unabhängig von Elektrik → auch bei Stromausfall wirksam
- Fangbremsen (Fangkeile) unter Kabinenboden gegen Führungsschienen → sanfter Nothalt
- Prüfintervall: alle 2 Jahre durch Sachverständige

### Aufzugskategorien nach DIN ISO 8100-30

- Kategorie I: Personenaufzüge; 450 kg Nennlast (Person allein oder Rollstuhl ohne Begleitperson); 630 kg für Rollstuhl + Begleitperson; 1000 kg für Krankentragen mit abnehmbaren Griffen, Särge, Möbel, Rollstuhl mit Wendekreis
- Kategorie II: Personenaufzüge mit Gütertransport; Abmessungen wie Kategorie I oder VI
- Kategorie III: Aufzüge für Gesundheitsfürsorge (Krankenhäuser); 2500 kg für Krankenhausbetten mit medizinischer Ausrüstung + Personal; 2000 kg für Betten 1000 mm × 2300 mm (ohne Bedienungspersonal)
- Kategorie VI: Intensive Nutzung, hauptsächlich Hochhäuser >15 Stockwerke; Nenngeschwindigkeit mind. 2,5 m/s; detaillierte Verkehrsberechnung für genaue Werte

**Personenaufzüge für Wohngebäude (DIN ISO 8100-30):**
- Kleiner Aufzug: 320 und 450 kg; Fahrkorbgrundfläche 0,9 × 1,0 m bzw. 1,0 × 1,2 m; NICHT für Kinderwagen/Rollstühle geeignet; nur ausnahmsweise vorsehen
- Mittlerer Aufzug: 630 kg; Fahrkorbgrundfläche 1,10 × 1,40 m; geeignet für Kinderwagen und Rollstühle
- Großer Aufzug: 1000 kg; Fahrkorbgrundfläche 1,10 × 2,10 m; für Krankentragen und Möbel
- Triebwerksraumloser Aufzug ist heute Standard im Wohnhausbau (maschinenraumlos): kompakt, geräuscharm (kein Getriebe), energiesparend, frequenzumrichtergesteuert; Schachtkopf ab 2400 mm; Steuerung in Schaltschrank am Gang oder in Türzargenformat
- Mind. 1 Fahrkorb mit Grundfläche 1,10 × 2,10 m für Krankentrage; Förderkapazität 13 Plätze ausreichend für ca. 260 Personen (je 20 pro Haltestelle)

**Personenaufzüge im Nichtwohnungsbau:**
- Normale Nutzung: für Büros, Hotels bis max. 15 Etagen
- Intensive Nutzung: Hochhäuser >15 Etagen; Geschwindigkeit mind. 2,5 m/s
- Max. 3 Aufzüge nebeneinander; weitere gegenüberliegend
- Nicht im Durchgangsbereich; Nebenschluss zu Verkehrswegen; ausreichende Bewegungsfläche
- Bewegungsfläche: mind. 1,5-fache Fahrkorbtiefe vor Fahrschachttürwand; nebeneinander: 1,5-fach, jedoch mind. 2,40 m; gegenüberliegend: mind. Summe beider Fahrkorbtiefen, max. 4,50 m

**Feuerwehraufzüge:**
- In einigen Bundesländern ab bestimmter Hochhaushöhe pflicht; eigener Fahrschacht; exklusiv für Feuerwehr (nicht für Gebäudenutzer)
- Haltestelle in jedem Geschoss; Fahrkorbgrundfläche Breite × Tiefe: 1,10 × 2,10 m; Nennlast ab ca. 1800 kg; Zugangsbreite mind. 90 cm; Vorräume für Krankentrage ausreichend
- Lichte Mindestmaße Fahrkorb nach DIN EN 81-72: 1,10 × 2,10 m
- Stromleitungen baulich von anderen Aufzügen getrennt und besonders gegen Brand geschützt; Ersatzstromanlage für sicheren Betrieb; ggf. Druckbelüftung Schächte

### Bauliche Ausbildung Aufzugsschächte

- Fahrkorb + Gegengewicht in Führungsschienen; Fahrkorb: Stahlrahmen mit nicht brennbarem Material; Fangvorrichtungen gegen Absturz (oben + unten)
- Breitkörbe: breite Türöffnung für schnelle Be-/Entladevorgänge; Tiefkörbe: für Krankentragen und große Lasten; Übereck-Anordnung: wechselnde Zugänge um 90°
- Gegengewicht: gleicht Fahrkorbgewicht + ½ zulässige Nutzlast aus (spart Antriebsenergie, verbessert Reibungsschluss Seil/Treibscheibe)
- Aufzugsschächte: abgeschlossene röhrenförmige Brandabschnitte; bis 3 Aufzüge in einem Schacht (Bauaufsichtsrecht Länder); innerhalb Gebäude feuerbeständig: 24 cm Mauerwerk oder 25 cm Stahlbeton
- Türen T90: feuerhemmend, aber NICHT rauchdicht; Fahrschachttüren können F90 kaum erfüllen
- Ohne eigenen Schacht im Treppenraum (umkleidet): landesrechtlich bis 5 bzw. 6 Geschosse zulässig
- Nicht für Aufzug benötigte Kabel/Rohrleitungen: NICHT in den Fahrschacht
- Ventilationsöffnungen: ca. 1% der Schachtgrundfläche → ins Freie oder in TWR
- Rauchabzugsöffnungen: mind. 2,5% der Schachtgrundfläche (Brandenburg: mind. 5% oder ≥ 0,2 m²); ≥ 0,1 m²; direkt oder über Schacht ins Freie; motorisch-betriebene wärmegedämmte Lamellen (GEG-Kit) zur Wärmeverlust-Vermeidung

Schachtanker/Befestigung:
- Ankerschienen für Führungsschienen in 2,00–2,50 m Abständen (nur angeschweißte/geschraubte Anker, NICHT durchgesteckte)
- Gemauerte Schächte: Rüstlöcher ca. 15 × 15 cm, 0,5 m unterhalb jeder Haltestelle (mind. 4 je Bühne); weitere 2 m unterhalb Schachtdecke
- Rüstbodenhalterungen entfallen, wenn Firma mobile Arbeitsplattformen einsetzt

**Schachtgrube:**
- Tiefe je nach Betriebsgeschwindigkeit und Tragfähigkeit: 1,40–2,80 m (kleinere Maße möglich)
- Ab 1,50 m–2,50 m: unfallsicherer Abstieg je Aufzug erforderlich
- Ab 2,50 m Tiefe: seitlicher Zugang mit kontaktgesicherter Tür (Zugangstür mind. 1,40 m Höhe)
- Schächte NICHT über begehbaren Räumen; wenn unvermeidbar: Schachtgrubensohle für mind. 500 kg/m² Verkehrslast bemessen; Gegengewicht mit Fangvorrichtung oder Pfeiler darunter

**Schachtkopf:**
- Abstand Oberkante Fußboden oberstes Haltepunkt bis Schachtdecke: 3,70–4,40 m (oder kleiner) für Betriebsgeschwindigkeiten bis 1 m/s → Schachtdecke ragt über oberste Geschossdecke hinaus

**Normmaße Personenaufzüge für Wohnungsbau Tab. 7.3 (firmenneutral, DIN ISO 8100-30):**
- Fahrkorbhöhe h4: 2,20 m
- Fahrkorb-/Schachttürenhöhe h3: 2,00 m (320/450 kg), 2,10 m (630/1000 kg)
- Schachtgrubenteife d3: 0,40 m/s → 1,40 m; 0,63–1,0 m/s → 1,60 m; 2,0 m/s → 1,75 m; 2,5 m/s → 2,20 m
- Schachtkopfhöhe h1: 0,40 m/s → 3,60 m; 0,63–1,0 m/s → 3,70 m; 1,6 m/s → 3,80 m; 2,0 m/s → 4,30 m; 2,5 m/s → 5,00 m

**Normmaße Personenaufzüge für Nichtwohnungsbau Tab. 7.4 (DIN ISO 8100-300):**
- Fahrkorbhöhe h4: 2,20 m (630 kg), 2,30 m (800–2000 kg), 2,40 m (intensive Nutzung)
- Schachttürenhöhe h3: 2,10 m
- Schachtgrubenteife d3: 0,63 m/s → 1,40 m; 1,0/1,6 m/s → 1,60 m; 2,0 m/s → 1,75 m; 2,5 m/s → 2,20 m; 3,0 m/s → 3,20 m; 3,5 m/s → 3,40 m; 4,0 m/s → 3,80 m; 5,0 m/s → 3,80 m; 6,0 m/s → 4,00 m
- Schachtkopfhöhe h1: 0,63 m/s → 3,80/4,20 m; 1,0/1,6 m/s → 4,00/4,20 m; 2,0 m/s → 4,40 m; 2,5 m/s → 5,00/5,20/5,50 m; 3,0 m/s → 5,50 m; 3,5 m/s → 5,70 m; 4,0/5,0 m/s → 5,70 m; 6,0 m/s → 6,20 m

Bei gemeinsamen Schächten für Aufzugsgruppen: 20 cm für Konstruktion zwischen 2 Fahrbahnen zu Mindestschachtbreiten für Einzelaufzüge hinzuzurechnen

**Personen-Umlaufaufzüge (Paternoster):** Seit 1974 gem. früherer AufzV nicht mehr errichtbar; bestehende Anlagen dürfen weiter betrieben werden.
