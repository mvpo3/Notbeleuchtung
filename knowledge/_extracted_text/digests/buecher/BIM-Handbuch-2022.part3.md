# BIM-Handbuch-2022 — Teil 3
> Quelle: BIM-Handbuch-2022 (buecher) · dieser Teil. Inhaltlich: Kapitel "BIM-Software" (Softwarelandschaft, Big Player, Softwareversion/Kompatibilität, Software-Kategorien, Viewer, Prüfsoftware, Auswertung/Simulation, Kollaborationsplattformen), "Lizenzpolitik", Literaturverzeichnis und Abschnitt "BIM in der BIG". Hinweis: Dieser Chunk enthält KEINE elektrotechnischen Normwerte (Höhen/Abstände/Schutzbereiche/FI etc.) — er ist ein BIM-Management- und Software-Kapitel.

## Inhalt

### Softwarelandschaft (S.120–123)
- Nur BIM-fähige Software macht BIM praktizierbar; Markt ist noch mitten in der Entwicklung. Keine "eierlegende Wollmilchsau" deckt alle Phasen ab.
- Historischer Vergleich: Umstellung Tusche → CAD dauerte **mehr als 20 Jahre**; CAD → BIM dauert vermutlich **mindestens genauso lange**. Stand: vermutlich **noch nicht einmal die Hälfte** dieses Weges hinter uns.
- Kein eindeutiges Kriterium, was "BIM-Software" ist — nur mehr/weniger BIM-fähige Programme.
- **Zentrales Kriterium = Interoperabilität** (Datenübernahme/Übergabe an andere Programme). Quelle: Hausknecht, Liebich 2016 (Fußnote 94).
- Mögliche Definition: nur Software mit zertifizierter Datenschnittstelle gilt als BIM-Software → dafür kommt nur die **IFC-Zertifizierung von buildingSMART** infrage. (Verweis Kapitel 4, S.190 IFC-Zertifizierung.)
- Problem der Zertifizierung: zu wenige Programme zertifiziert; manche Hersteller bieten IFC-Import/Export an, ohne buildingSMART-Zertifizierung. Hindernis: nach Zertifizierung darf der Hersteller nichts mehr an der Softwareversion ändern (Problem bei Servicepacks).

### Experten-Statements (S.121)
- DI Gustav Spener: BIM kommt für alle Ziviltechniker:innen im großen Stil; Fachplaner (Tragwerk, Gebäudetechnik) haben schon Erfahrung. Infrastruktur (Tunnel, Brücken, Straßen, Schienen) noch überwiegend konventionell; Optimierung der Software und IFC-Integration braucht noch Zeit. Bund/Länder müssen Umfang/Anforderungen/Standards definieren. Große Auftraggeber (ÖBB, ASFINAG, Länder-Abteilungen) treten mit realistischen Erwartungen auf.
- DI Arch. Bmstr. DI Wolfgang Kurz: struktureller Fehler — nicht der Anwender wird gefragt, was er braucht, sondern die Software gibt vor, was geht.

### Rechtstipp (Dr. Volker Mogel, LL.M. Eur.) — Urheberrecht Software (S.123)
- BIM-Software = geistige Schöpfung des Urhebers, urheberrechtlich geschützt: **§ 40a iVm § 2 UrhG**.
- Planungsleistungen des Architekten = Werk der bildenden Kunst, geschützt sofern eigentümliche geistige Schöpfung: **§ 3 UrhG**.
- Bearbeitungen können Schutz wie Originalwerke genießen, unbeschadet des ursprünglichen Urheberrechts: **§ 5 UrhG**.
- Verwertung der Bearbeitung bedarf der Zustimmung des Urhebers des Originalwerks: **§ 14 UrhG**.
- Werk von mehreren Personen = Miturheberschaft; Verfügen bedarf der **Einstimmigkeit**.
- Know-how-Schutz über **UWG**: Nachahmen fremder Leistungen ohne Sonderrechtsschutz ist unlauter bei sittenwidrigen Umständen. Empfehlung: Verschwiegenheitsvereinbarungen, Pönalisierung von Verstößen, Schutz sensibler Daten durch Zugriffsrechte.

### Lebenszyklus (S.124–125)
- Idealtypischer BIM-Workflow: Daten werden entlang des gesamten Lebenszyklus weitergegeben + verfeinert, nicht neu eingegeben (Übernahme über geeignetes Dateiformat).
- BIM noch in Entwicklung: ideal nahe v.a. in frühen Phasen; je später die Projektphase, desto seltener gibt es passende Produkte.
- Abbildung 30: sehr ähnliches Idealbild Lebenszyklus Nemetschek (oben) und Autodesk (unten) (Fußnote 95: Autodesk und Grafisoft).

### Die "Big Player" (S.126–130)
- Großkonzerne kaufen erfolgreiche kleine Anbieter auf; bauen Step-by-step Portfolio über kompletten BIM-Workflow auf → ideal: Daten im (ggf. proprietären) Format über gesamten Lebenszyklus → komplett im closedBIM. (Verweis Kapitel 4, S.162 Proprietäres Dateiformat.)
- **Vier Großkonzerne: Autodesk, Trimble, Nemetschek, Bentley.** Trimble + Bentley stark in Nordamerika/Australien; deutschsprachiger Markt dominiert von **Nemetschek + Autodesk**.
- Autodesk: rund **100 verschiedene Produkte** inkl. Varianten (Fußnote 96).
- Nemetschek-Besonderheit: zwei sehr ähnliche konkurrierende Produktschienen — **Allplan** und **Archicad** (von der aufgekauften Firma Graphisoft).
- **Umfrage**: zwischen Jänner und Oktober 2021, unter Mitgliedern der ZT Kammer, des Fachverbandes Ingenieurbüros und der Bundesinnung Bau. Insgesamt **26 Softwarehersteller** abgefragt; Mehrfachnennungen möglich.
  - Ausnahme bei Auswahl: **Autodesk AutoCAD** als eigene Antwortmöglichkeit (hohe Verbreitung in Österreich); übrige Autodesk-Programme unter Kategorie "Autodesk".
  - Häufigste Produkte: ZT Kammer + Baumeisterbetriebe → "Nemetschek Group" und "Autodesk". Ingenieurbüros → "Autodesk" führt, "Andere" bereits auf Platz 2.
  - Hersteller mit Anteil unter 4 % in allen Gruppen (nicht im Diagramm, Fußnote 97): SOFTTECH, BAUSOFT INFORMATIK AG, ACCASOFTWARE, BAUPLUS, DATAFLOR AG, CADWORK INFORMATIK, XEOMETRIC, DIETRICH'S, BEXEL CONSULTING, IT-CONCEPT SOFTWARE, SIEMENS, DICAD, NOVA Building, BENTLEY SYSTEMS, TRANSSOFT SOLUTIONS.

#### Tabelle 9: Die "größten" Softwarehersteller (Umsatz 2020, Mitarbeiter:innen, Hauptsitz) — S.130
| Hersteller | Umsatz (2020) | Mitarbeiter:innen | Hauptsitz |
|---|---|---|---|
| Autodesk | ca. 3,26 Mrd. $ | 10.100 | San Rafael (USA) |
| Trimble | ca. 3,15 Mrd. $ | 11.402 | Sunnyvale (USA) |
| Bentley Systems | ca. 800 Mio. $ | 4.104 | Exton (USA) |
| Nemetschek Group | ca. 596,9 Mio. € (ca. 680,5 Mio. $) | 3.074 | München (D) |

Quellen (Fußnoten 99–103, Zugriffsdaten 13.1.2022 bzw. 8.6.2022; Währungsrechner bankenverband.de).

### Zentrale gemeinsame Datenbank (S.131)
- Big Player dominieren auch mit aufsetzenden Drittherstellern; je enger abgestimmt, desto besser die Datenübergabe.
- Optimalfall: kein Export/Import nötig — verlinkte Datei per **"Refresh-Klick" in Echtzeit** aktualisieren.
- Klassischer Weg: Datenübergabe per Datei. High-End-Vision: gemeinsame **Cloud-Datenbank**, auf die alle Programme zugreifen. Eingabeprogramme liefern Daten in DB; andere Programme setzen zur Weiterverarbeitung/Auswertung/Analyse auf. Dahinter Entwicklerplattform (Grafik: **Forge**) für Drittanbieter-Zusatztools. (Abbildung 32, Fußnote 98 Autodesk.)

### Softwareversion / Kompatibilität (S.132–134)
- Neueste Version arbeiten = oft Probleme: Plugins noch nicht verfügbar; fehlende Abwärtskompatibilität.
- **Abwärtskompatibel** = kann ältere Dateiversionen lesen UND in älterer Version speichern.
- **Aufwärtskompatibel** = kann nur ältere Versionen einlesen, nicht als solche ausgeben.
- BIM-Datei einmal in aktuellerer Version geöffnet + gespeichert → **kein Zurück**. Im Gegensatz zu CAD ist BIM-Software so gut wie nie abwärtskompatibel (Abb. 33).
- CAD: dwg kann in wählbarer Version gespeichert werden (z.B. 2007er-dwg oder 2013er-dwg). BIM: aus Version "n" nicht mehr in Version "n-x" speicherbar.
- **Praxistipp (S.133)**: Beim Arbeiten mehrerer Personen in/mit gleicher (auch verknüpfter) Datei müssen alle dieselbe Softwareversion verwenden — sogar denselben **Software-Build** (Updates/Bugfixes/Servicepacks erzeugen mehrere Builds). Unterschiedliche Builds können Zusammenarbeit scheitern lassen.
  - Beispiel: alle in 2019er-Version, eine Person 2020er → speichert in 2020er → andere können nicht mehr öffnen. Manche Software: schon einmaliges Öffnen in aktuellerer Version verhindert Rückkehr.
  - Mehrjähriges Projekt: zwischenzeitliches Hochziehen sorgfältig planen + mit allen abstimmen. Kein schrittweises Hochziehen! Während des Upgrades darf niemand arbeiten; erst Software hochziehen, dann alte Datei in neuer Version öffnen + speichern, dann alle wieder freigeben (am besten Admin + BIM-Manager über ein Wochenende). Schlimmstenfalls Schritt wiederholen, da manche Software nur **um drei Versionen auf einmal** updaten kann.
  - Parallele Installation: viele Lizenzen erlauben Installation älterer Versionen der gleichen Software am selben Rechner — meist vorhergehende Version oder die **letzten drei Versionen** (jeweils nur ein Build). Beispiel: Projekt A vormittags in 2019er, Projekt B nachmittags in 2020er.

### Regionale Verbreitung & Lokalisierung (S.134)
- Software stark in Region ihrer Entwicklung: geografische Nähe von Graphisoft (Ungarn) erklärt große Verbreitung von Archicad in Österreich.
- Lokalisierung: Sprache, landesspezifische Anforderungen (Ausschreibungsregeln, geforderte Plandarstellungen, lokale Berechnungen) → Chance für kleine Hersteller gegen Großkonzerne.

### Software-Kategorien (S.134–139)
- Einteilung möglich entlang Projektverlauf / Phase (Abbildung 34, Fußnote 105: Baldwin 2019, S.131) oder nach Anwendungskategorie (häufigste Einteilung). Wenige Produkte beschränken sich auf ihre Kategorie.

#### Modelliersoftware (S.136–139)
- Beginn eines BIM-Prozesses; erste Kuben mit Merkmalen → schrittweise Verfeinerung von Geometrie + Attributen.
- Viele Produkte (AutoCAD, Vectorworks, Allplan) ursprünglich CAD, umgebaut — teils voll BIM-fähig, teils "BIM-light". Später erschienene Produkte hatten Vorteil (von Beginn BIM-konformer).
- Einsatz nach Fachdisziplin/Region; Autodesk adressiert gesamten **AEC-Bereich (Architecture, Engineering & Construction)** samt Stahlbau.
- Österreich: Großteil der Architektur mit **Archicad**; in Deutschland Anteil **Revit** für Architektur deutlich größer. Revit in Österreich gern von Haustechnik; in Deutschland Haustechnik eher mit **Nova**.

##### Umfrage-Ergebnisse spezielle BIM-Produkte (S.137)
- **ZT Kammer**: Archicad **102 Nennungen = 57 %**; Revit **67 Nennungen = 37 %**; Allplan **30 Nennungen = 17 %**. Tekla und MicroStation kaum genutzt.
- **Ingenieurbüros**: Revit **~56 % (54 Nennungen)**; Allplan **~22 %**; Archicad **19 Nennungen = 20 %** (3. Stelle).
- **Baumeisterbetriebe**: Archicad **54 %**, Allplan **33 %**, Revit **30 %**.
- Nur eines dieser Programme in Verwendung: ZT Kammer ~**87 %**, Ingenieurbüros ~**91 %**, Baumeisterbetriebe ~**84 %** — gleichzeitiger Einsatz mehrerer = Ausnahmefall.
- Differenzierung ZT Arch vs. ZT Ing (Abbildung 36): Architekt:innen verantwortlich für häufige Archicad-Nennungen; restliche ZT (ZT Ing) führen Revit + Allplan vor Archicad. Summe ZT Arch + ZT Ing > ZT gesamt wegen Mehrfachnennungen bei Fachgebieten.
- Sonderkategorien Modelliersoftware: **generische Formfindung** (konzeptionelle Variantenvergleiche zu Projektbeginn) und **grafische Programmiersprache** (parametrische/algorithmische Geometriesteuerung).

#### Tabelle 10: Beispiele Modelliersoftware (Software / Hersteller / Schwerpunkt) — S.139
| Software | Hersteller | Schwerpunkt |
|---|---|---|
| Archicad | Nemetschek (Graphisoft) | Architektur |
| Revit | Autodesk | AEC, Stahlbau |
| Allplan | Nemetschek | Statik, Architektur |
| Civil 3D | Autodesk | Infrastruktur |
| AECOsim Building Designer | Bentley | AEC |
| Vectorworks | Nemetschek | Architektur |
| AutoCAD | Autodesk | Architektur |
| Tekla Structure | Trimble | Statik |
| RFEM/RSTAB | Dlubal | Statik |
| SOFiSTiK | Mensch und Maschine | Statik |
| Nova | Trimble (Plancal) | Haustechnik |
| DDS-CAD | Nemetschek | Haustechnik |
| MagiCAD | Glodon | Haustechnik |
| LiNear | LiNear | Haustechnik |
| Rhinocerus | McNeel | Generische Formfindung |
| Grasshoper | McNeel | Graph. Programmiersprache |
| Dynamo | Autodesk | Graph. Programmiersprache |

#### Viewer (S.140–143)
- Meist kostenlos / abgespeckte Versionen (Solibri, Navisworks); abgelaufene Testversion (Archicad, Allplan, Revit) teils als kostenloser Viewer nutzbar.
- Zweck: Teilmodelle der Fachbereiche zu Koordinations-/Gesamtmodell zusammenführen; meist **IFC-Viewer** (lesen v.a. IFC). Ansichtsmöglichkeiten bis virtueller "walk-through".
- Zusatzfunktionen: Bauteil anklicken → Attribute; eigene Anmerkungen (Marker, Pfeile, Text); schnelles Maße-Prüfen über mobiles Display.
- Statement DI Melanie Wölwitsch: eigene Arbeit regelmäßig prüfen; IFC-Viewer durch Filtern/Isolieren — Zuordnung Bauelemente↔Klassen, Belegung mit Merkmalen wie **isexternal, loadbearing**, richtige Typisierung visuell prüfbar.
- **IFC-Viewer-Nutzung**: obwohl ~Hälfte der ZT Kammer + Ingenieurbüros IFC-Dateiformate verwendet, nutzen nur **29 % (Ingenieurbüros)** bzw. **32 % (ZT Kammer)** IFC-Viewer-Software; Baumeisterbetriebe knapp **42 %** (Abb. 37). Viewer für Good-Practice-Workflow im Grunde notwendig (IFC-Modelle betrachten, Abweichungen kontrollieren).
- Häufigster IFC-Viewer in allen Gruppen: **Solibri**, gefolgt von Autodesk Viewer, BIMcollab ZOOM, Navisworks und BIMVision (letzte drei bei Ingenieurbüros je **14 Nennungen**). BIMVision bei Baumeisterbetrieben am zweithäufigsten. Trimble Connect etwas häufiger bei Ingenieurbüros, open IFC Viewer eher bei ZT Kammer (Abb. 38, Mehrfachauswahl zulässig).

#### Prüfsoftware ("Model Checker") (S.144–145)
- Baut auf Viewer auf; Prüfroutinen werden über Viewer gestartet.
- Bekannteste Prüfung: **Kollisionserkennung (Clash Detection)** — Modelle verschiedener Fachbereiche zusammenführen.
  - **Hard Clashes**: Objekte kollidieren direkt (Rohr ↔ Unterzug, fehlende Durchbrüche für Leitungen).
  - **Soft Clashes**: Objekte kollidieren nicht direkt, z.B. Stütze im Öffnungsradius eines Fensters, Wartungsbereich einer haustechnischen Anlage nicht freigehalten.
- Kollisionserkennung = großer Vorteil BIM vs. CAD (Planungsfehler vermeiden, Kosten sparen). Auch in Modelliersoftware/Kollaborationsplattformen angeboten.
- **Praxistipp**: Soft Clashes werden oft übersehen, erst im Betrieb bemerkt. Freizuhaltende Bereiche immer in Modellierelementen enthalten (z.B. halbtransparenter Kubus, z.B. freizuhaltender Raum vor Türen der Lüftungsanlage).
- Prüfsoftware = Hauptinstrument Qualitätsmanagement: vor Weitergabe Modellierqualität + IFC-Konformität prüfen (Klassifizierungen + Attribute richtig zugewiesen; doppelt übereinanderliegende Elemente erkennbar); BIM-Koordination prüft Teilmodelle auf Passung ins Gesamtmodell.
- Weitere Prüfkriterien: **Barrierefreiheit, Fluchtweglängen, Brandschutzvorschriften, Wände übereinander stehend** u.v.m.; Bauvorschriften meist einfach prüfbar. Rolle bei künftigen digitalen Einreichungen (z.B. **BRISE-Projekt in Wien**).
- Quasi-Monopol zugunsten **Solibri**. Prüfsoftware arbeitet meist mit IFC; wenige (z.B. **Navisworks**) lesen verschiedenste Formate. Erweiterte Funktionen: Trimble Connect (Zusammenarbeit), BIMcollab Zoom (Issue-Management), **Bexel Manager (4D + 5D)**.
- Verweise: Kapitel 4 S.179 (Klassifizierung), Kapitel 2 S.74 (Attribute).

#### Tabelle 11: Beispiele Prüfungssoftware — S.145
| Software | Hersteller | Schwerpunkt |
|---|---|---|
| Solibri | Nemetschek | Modellzusammenführung, Qualitätsprüfung |
| Navisworks | Autodesk | Modellzusammenführung, 4D |
| BIMcollab Zoom | Kubus | Modellzusammenführung, Qualitätsprüfung |

#### Software für Auswertungen und Simulationen (S.146–147)
- Greifen auf Daten geprüfter Modelle zurück. Erste Auswertung = **Mengenermittlung** (heute weitgehend automatisch, sofern sauber modelliert); wunschgemäß unterteilte Bauteillisten leicht erstellbar. (Verweis Kapitel 7, S.305 Mengenermittlung.)
- Technische Berechnungen: Statik = **FEM-Software (Finite-Elemente-Methode)**; Haustechnik = Heiz- und Kühllastberechnungen; Bauphysik = Tageslichtsimulationen, Energieausweise, Strömungssimulationen, Wärmebrückenberechnungen; Rendern = Simulation auf Modellbasis.
- **4D**: Import Projektzeitplan + Modell → Bauablaufsimulationen (visuelle Machbarkeitsprüfung), oft nur ein zusätzlicher Parameter nötig.
- **5D**: meist **AVA-Software (Ausschreibung, Vergabe und Abrechnung)**. Mengen aus Modelliersoftware übergebbar — von tabellarischem Einlesen bis stetigem Refreshing (je nach Kompatibilität).
- Schwierigkeiten: Ausgangsmodell muss zur Auswertung passen. Beispiele Architektur- vs. Bauphysik-/Haustechnikmodell:
  - Schacht: Architektur = pro Geschoss in Räume unterteilt; Haustechnik = durchgehender Raum über alle Geschosse.
  - Abgehängte Decken: im Architekturmodell kein extra Raum.
  - Wände in Einzelschichten modelliert → mehrere "Außenwände" mit einzelnen **U-Werten** → Energieberechnungen kommen meist nicht zurecht.
  - Kellerwand für Bauphysik horizontal in erdanliegenden + oberirdischen Anteil geteilt → für Architektur Arbeitserschwernis (mehrteilige Wand, Fenster nur per Workaround setzbar).
  - Bauphysikwerte in Architekturmodelle eingepflegt finden schwer Weg zurück in Bauphysikprogramme (mangelnde Kompatibilität). Quelle: Arch. DI Christine Horner (Fußnote 106).

#### Kollaborationsplattformen (S.147)
- Brauchen "Datendrehscheibe"; größtes Entwicklungspotenzial. Aktuell viele Funktionen in Stand-alone-Produkten → künftig cloudbasierte Gesamtlösungen mit zentraler Datenbank.
- Diese Plattformen = **CDE (common data environment)**. Funktionen wie Dokumentenmanagement, Projektmanagement, Controlling werden Stück für Stück Bestandteil des CDE. (Verweis Kapitel 5, S.224 CDE.)

### Lizenzpolitik (S.148–156)
- BIM-fähige Software i.d.R. **kommerzielle Software** (keine Freeware/Open Source). Anschaffungs- + jährliche Servicekosten teuer. Lizenzmodelle unterschiedlich, komplex, ändern sich teils monatlich.

#### Mieten oder kaufen (S.149–152)
- Kaufen naturgemäß billiger als mieten; weitere Kriterien: sofortige steuerliche Abschreibbarkeit, Liquidität (sofortige Vollzahlung schwächt Liquidität), Eigentumsübergang (wichtig bei eigentumsgebundenen Förderungen).
- Vorteil Mieten = Flexibilität (idealerweise nur Genutztes bezahlt; Fußnote 107 architektur-online.com). Miete meist ab **einem Monat**; Mietpreis höher bei kürzerer Laufzeit; Kostentransparenz oft eingeschränkt; Risiko Mietpreiserhöhungen. Geeignet zum Abfedern von Auftragsflauten/-spitzen.
- Bei Miete meist alle Updates + Erweiterungen inkludiert; IT-Dienstleistungen (Konfiguration/Installation) größtenteils ausgelagert.
- **SaaS (Software as a Service)**: browserbasiert über Cloud; Voraussetzung gute Internetverbindung (Problem bei Infrastrukturprojekten am Land mit mobilen Geräten).
- Miete meist "all inclusive"; oft zusätzlich Service/Update, Cloud-Speicher, Render-Rechenleistung → beim Vergleich Miete vs. Kauf berücksichtigen.
- Nachteil Miete: keine Wahl der Version mehr (problematisch bei Team-/Mehrprojektarbeit). (Verweis Kapitel 3, S.224 Softwareversion.)

#### Tabelle 12: Vereinfachte Übersicht Software-Lizenzformate — S.150/151
Spalten = Lizenzformate (Mieten-Gruppe: **Mieten**; Kaufen-Gruppe: **Mietkauf, Leasing, Finanzkauf (Ratenzahlung Hersteller), Finanzkauf (Bankkredit), Kauf auf Rechnung**).
| Kriterium | Mieten | Mietkauf | Leasing | Finanzkauf (Raten Hersteller) | Finanzkauf (Bankkredit) | Kauf auf Rechnung |
|---|---|---|---|---|---|---|
| Gesamtkosten | teurer | eher billiger | eher billiger | eher billiger | eher billiger | am billigsten |
| Auslastungsschwankungen (flexibles Reagieren) | schnelles + flexibles Reagieren möglich | kaum möglich | kaum möglich | kaum möglich | kaum möglich | kaum möglich |
| Steuerlich absetzbar | laufende Betriebsausgabe | laufende Betriebsausgabe | laufende Betriebsausgabe | evtl. möglich | nur längerfristig | nur längerfristig |
| Liquidität | verbessert | verbessert | verbessert | gering verbessert | kaum verbessert | nachteilig |
| Eigentum | nein | ja | nein (meist Leasinggesellschaft) | ja | ja | ja |

#### Sparmöglichkeiten / Gebrauchtsoftware (S.151–152)
- Aktionen, **Umsteigerrabatte** (bei Wechsel auf Konkurrenzprodukt), Gelegenheiten bei Lizenzmodellwechsel, **Existenzgründerrabatte** für neue Büros. Auf Zusatzservices (Hotline, Cloud) + integrierte Updates achten.
- **Gebrauchtsoftware**: meist nur Lizenz/Nutzungsrecht verkauft (Eigentum bleibt Hersteller). Genau prüfen — **25 bis 70 % Ersparnis** möglich.
- EuGH-Grundsatzurteil: Gebrauchtsoftwarekäufer hat Anspruch auf Updates + Support (Fußnote 108). Nur aus bekannten Quellen / spezialisierten größeren Plattformen kaufen (Raubkopie-Risiko).
- Geeignete Plattformen: www.2ndsoft.at, www.lizenzdirekt.com, www.software-reuse.eu, www.softwarebuddies.eu/, www.usedsoft.com.

#### Rechtstipp (Dr. Volker Mogel) — Lizenzrecht (S.152)
- Bauherr + alle Projektbeteiligten sollten Lizenzen für alle Nutzer + genutzten Endgeräte haben.
- **Zeitlich unbeschränkte Werknutzungsberechtigung = Softwarekaufvertrag**; **zeitlich beschränkte "Lizenz" = Softwaremietvertrag**.
- Bei Miete: Software muss während gesamter Projektlaufzeit verfügbar sein; Vermieter muss vertragsgemäßen Gebrauch ermöglichen + während Mietdauer aufrechterhalten; separate Wartungs-/Pflegevereinbarung **nicht** notwendig (für weitergehende Leistungen wie Weiterentwicklungen/Upgrades aber sinnvoll). Anbieter kann Überlassung an Wartungsvertrag koppeln.
- Empfehlung: vertraglich + praktisch **Zugriff auf Quellcode** sichern; um Insolvenzverwalter-Zugriff zu entziehen, Quellcodekopie bei einem **"Escrow Agent"** hinterlegen (bei Cloud: gespiegelter Server).

#### Einzelplatzlizenz vs. Netzwerklizenz (S.153–154)
- **Einzelplatzlizenz**: über **Endbenutzer-Lizenzvertrag (EULA)**; früher Hardware-Dongle/Software-Key, heute meist "Klick" zur EULA-Annahme. Für genau definierten Arbeitsplatz; manche Firmen erlauben Wechsel Workstation ↔ Laptop mit einer Lizenz.
- **Netzwerklizenz (floating licence)**: volumensbezogen; Lizenzen über Lizenzserver entlehnen/zurückgeben. Obergrenze gleichzeitiger Entlehnungen am Server hinterlegen (sonst Nachzahlungen). Homeoffice ohne Hardware → **Remote-Desktop** auf Serverrechenleistung. Disziplin beim Zurückgeben nötig; Mischung Volllizenzen + "light"-Lizenzen möglich; manche Software nach Testablauf noch als kostenloser Viewer.
- **Autodesk**: Umstellung auf **"named-user"-Lizenzen** — Identifizierung über Userkonto (Benutzername + Passwort) + ggf. Mobilnummer (**Zwei-Faktor-Identifizierung**), nicht mehr Seriennummer. Empfehlung: nicht persönliche Mailadresse, sondern z.B. arbeitsplatz1@unserbuero.at (Kündigungsfall).
- Produktpolitik ändert sich häufig (Produkte zusammengelegt/umbenannt, neue Bundles, überschneidende Funktionen). Firma **Artaker** bietet eigene Schulung zu "Autodesk-Lizenzen" (Fußnote 109).

#### Praxistipp Support/Umfeld (S.155)
- Servicevertrag ≠ Rundum-Sorglos-Paket: Schulungen, Bürostandard, aktuelle Probleme. Hersteller-Hotline oft weniger hilfreich als guter Reseller / erfahrene:r BIM-Berater:in. Community Pages einschreiben.
- Community Pages:
  - Revit: blogs.autodesk.com/revit/, blogs.autodesk.com/bimblog/
  - Archicad: hey-Archicad.de, www.a-null.com/blog/
  - Allplan: blog.allplan.com/de, connect.allplan.com/de/forum/forum-start.html, www.allplan.com/at/bim/bim-guides/

#### Checkliste (Zeitpunkt Kauf) (S.156)
- Was soll die Software können?
- Können mehrere (ältere) Versionen der gleichen Software installiert werden?
- Welche Dateiformate können importiert/exportiert werden?
- Ist die Software für IFC-Import und -Export zertifiziert?
- Welche direkten Schnittstellen zu anderen Produkten/Datenbanken?
- Welche Lizenzverträge gibt es?
- Lizenz wechselseitig Workstation ↔ Laptop nutzbar?
- Wie weit geht die Software auf lokale Besonderheiten ein?
- Welche Bibliotheken gibt es schon?

### Literaturverzeichnis (S.157)
- Baldwin, Mark: *Der BIM-Manager. Praktische Anleitung für das BIM-Projektmanagement*, 2. Auflage (2019), DIN Deutsches Institut für Normung e.V., Mensch und Maschine (Hrsg.); Beuth Verlag Berlin (**ISBN 978-3-410-29440-5**).
- Hausknecht, Kerstin; Liebich, Thomas (2016): *BIM-Kompendium: Building Information Modeling als neue Planungsmethode*; Fraunhofer IRB Verlag (**ISBN 978-3-8167-9489-9**).
- architektur-online.com/kolumnen/edv/buero-software-mieten-oder-kaufen (Zugriff 10.12.2021).

### BIM – Building Information Modeling – in der BIG (S.158–159)
- **Bundesimmobiliengesellschaft m.b.H. (BIG)** beschäftigt sich seit längerem intensiv mit BIM. Interne Vorgaben **österreichweit einheitlich**, um Dienstleistern gleichartige Standards zu geben. Großes Bestandsportfolio (Schulen, Universitäten, Spezialimmobilien wie Justizanstalten, Gerichts-/Polizeigebäude, Büro-/Wohnbauten) berücksichtigt.
- BIG-Architekturwettbewerbe (Pilotprojekte): BIM noch keine Anforderung/Zugangskriterium; Ziel beste architektonische Lösung. Teilnehmer verpflichten sich im Auftragsfall zur Planung/Abwicklung nach BIM-Vorgaben der BIG. Ausgewähltes Projekt = **"openBIM"-Projekt über alle Leistungsphasen**.
- Unterstützung: BIM-Projektsteuerung auf BIG-Seite; gemeinsame **Modellierkolloquien** mit BIM-Gesamtkoordinator + BIM-Fachkoordinatoren des Auftragnehmers; BIG-Prüfregeln werden nach Beauftragung dem Auftragnehmer zur Verfügung gestellt (Qualitätssicherung).
- Erwartung an Auftragnehmer: Einbringen, Investition in Know-how, positive Mitwirkung.
- openBIM zwingend; geschuldete Leistungen über **IFC (Industry Foundation Classes)** bereitstellen. Planungsbüros arbeiten in gewohnter Software an Fachmodellen → Koordinations-/Gesamtmodelle abgestimmt + optimiert.
- Alle BIG-BIM-Projekte im Status **"Pilotprojekt"**; mehrere laufend. Fokus: durchgängiger BIM-basierter Planungsprozess inkl. Anforderungen aus Objekt- und Facilitymanagement von Beginn an. Daten für die **Betriebsphase = Kern der Informationsanforderung**.
- Ziel Pilotprojekte: Wissen aufbauen, Mehrwert generieren, als innovatives Unternehmen positionieren; Grundlagen anpassen/ergänzen.
- Prozesse (Modellkoordination, Koordinationssitzungen) nicht neu, aber strukturiert + festgeschrieben in BIM-Regelwerken.
- Rücksicht auf Strukturen der österreichischen Wirtschaft / KMU-Landschaft; aktives Interesse ausführender Unternehmen vorausgesetzt.
- **Datenhoheit verbleibt im Verantwortungsbereich der BIG.** BIG-Vertreter wirken in BIM-Arbeitsgruppen und bei **Austrian Standards** mit.

## Maschinen-Regeln

- [PFLICHT] BIM-Software gilt nur dann als zertifiziert BIM-fähig, wenn sie über die IFC-Zertifizierung von buildingSMART verfügt (BIM-Handbuch-2022 Teil 3, S.120, Kap.4 S.190).
- [PFLICHT] Bei gemeinsamer/verknüpfter BIM-Datei müssen alle Beteiligten dieselbe Softwareversion UND denselben Software-Build verwenden (Praxistipp, S.133).
- [DEFINITION] Abwärtskompatibel = Software liest ältere Dateiversionen UND speichert in älterer Version; aufwärtskompatibel = liest nur ältere Versionen, gibt sie nicht aus (S.132).
- [DEFINITION] Hard Clash = direkte Objektkollision (z.B. Rohr ↔ Unterzug, fehlende Leitungsdurchbrüche); Soft Clash = keine direkte Kollision, aber Funktionsverletzung (z.B. Stütze im Fenster-Öffnungsradius, Wartungsbereich nicht freigehalten) (S.144).
- [DEFINITION] CDE = common data environment, cloudbasierte zentrale Datenplattform für Dokumenten-/Projektmanagement, Controlling etc. (S.147, Kap.5 S.224).
- [DEFINITION] AEC = Architecture, Engineering & Construction (S.136).
- [DEFINITION] AVA = Ausschreibung, Vergabe und Abrechnung (5D-Software) (S.146).
- [DEFINITION] SaaS = Software as a Service, browserbasiert über Cloud, setzt gute Internetverbindung voraus (S.149).
- [DEFINITION] Softwarekaufvertrag = zeitlich unbeschränkte Werknutzungsberechtigung; Softwaremietvertrag = zeitlich beschränkte Lizenz (Rechtstipp, S.152).
- [DEFINITION] Einzelplatzlizenz via EULA (Endbenutzer-Lizenzvertrag) für definierten Arbeitsplatz; Netzwerklizenz (floating licence) = volumensbezogen über Lizenzserver entlehnt (S.153).
- [DEFINITION] Named-user-Lizenz (Autodesk) = Identifizierung über Userkonto + ggf. Zwei-Faktor (Mobilnummer) statt Seriennummer (S.154).
- [FRIST] Manche BIM-Software kann eine Datei nur um maximal drei Versionen auf einmal aktualisieren (S.133).
- [FRIST] Parallelinstallation der gleichen Software meist nur für die letzten drei Versionen (jeweils ein Build) erlaubt (S.133).
- [FRIST] Softwaremiete üblicherweise ab einem Monat möglich (S.149).
- [FRIST] Gebrauchtsoftwarekauf erlaubt 25 bis 70 % Ersparnis; EuGH: Anspruch auf Updates + Support (S.151–152).
- [PFLICHT] Bei Netzwerklizenzen Obergrenze gleichzeitiger Lizenzentlehnungen am Server hinterlegen (sonst Nachzahlungen) (S.153).
- [PFLICHT] Empfehlung Quellcode-Zugriff vertraglich sichern, ggf. Hinterlegung bei Escrow Agent / gespiegeltem Server (Rechtstipp, S.152).
- [PFLICHT] In der BIG: geschuldete Leistungen über IFC bereitstellen; Abwicklung als openBIM über alle Leistungsphasen; Datenhoheit verbleibt bei der BIG (S.158–159).
- [DEFINITION] Urheberrechtlicher Schutz BIM-Software § 40a iVm § 2 UrhG; Architektenleistung § 3 UrhG; Bearbeitungen § 5 UrhG; Bearbeiterverwertung Zustimmung § 14 UrhG; Miturheberschaft = Einstimmigkeit (Rechtstipp, S.123).
