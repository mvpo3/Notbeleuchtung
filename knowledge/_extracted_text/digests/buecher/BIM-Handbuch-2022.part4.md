# BIM-Handbuch-2022 — Teil 4
> Quelle: BIM-Handbuch-2022 (buecher) · dieser Teil. Umfasst Kapitel 4 „Datenaustausch“ (Autor: Marcus Wallner), Seiten 160–199 (PDF-Seiten 161–200 von 348).

## Inhalt

### Kapitel 4 — Datenaustausch (S. 160, MARCUS WALLNER)
- Grundvoraussetzung für BIM-basierte Zusammenarbeit = funktionierender Datenaustausch zwischen verschiedensten Professionisten und deren teils sehr unterschiedlichen Softwareanwendungen.
- Jede Software / Herstellerplattform arbeitet mit eigenen Formaten. Beim Umwandeln in offene Dateiformate gehen viele Daten verloren, dafür können offene Formate von den meisten Programmen verarbeitet werden.

### Kapitelgliederung (Inhaltsverzeichnis, S. 161, mit Seitenzahlen)
- Proprietär und/oder offen? — S. 162
  - Proprietäre Formate — S. 162
  - Offene Formate — S. 164
  - open contra closed — S. 165
- BIM und GIS — S. 167
  - 3D-Laserscan — S. 168
  - Punktwolken — S. 171
  - BIM und GIS — S. 173
- Objektorientierte Modellierung — S. 179
  - OOM-Konzept — S. 180
  - Vererbung — S. 184
  - Weitere Beziehungen zwischen Klassen — S. 185
  - Nomenklatur — S. 186
  - bSDD (buildingSMART Data Dictionary) — S. 186
  - ASI-Merkmalserver — S. 188
- IFC (Industry Foundation Classes) — S. 190
  - IFC — S. 192
  - IFC-Versionen — S. 194
  - MVD (Model View Definition) — S. 195
- Literaturverzeichnis — S. 198

---

### Proprietär und/oder offen? (S. 162)
- Das Datenformat steht für openBIM oder closedBIM. Entscheidend für funktionierenden Dateiaustausch = Dateiformat + dessen korrekter Import/Export.
- Grundunterscheidung: offene vs. proprietäre Formate.
- Ein Element (z.B. Außenwand) muss so exportiert werden, dass es nach dem Import in die Software eines anderen Anwenders wieder der gleichen Klasse angehört und mit den gleichen Attributen eingelesen wird.

#### Proprietäre Formate (S. 162)
- „proprietär“ = „im Eigentum befindlich“; juristisch synonym für „urheberrechtlich geschützt“.
- Proprietäre Softwareprodukte / Dateiformate gehören einem Hersteller; nur dieser hat den Quellcode (meist Handelsgeheimnis) und kann die Verwendung honorieren lassen.
- Wenn nur ein Hersteller das Format definiert → proprietär.
- Wird das Format nur von einer Anwendung genutzt → „natives Format“.
- Proprietäre Formate können auch von anderen Herstellern genutzt werden und mit der Zeit zu allgemeinen Standards werden (hochpolitische Vorgänge).
- Beispiel PDF: war ursprünglich proprietär, Acrobat Reader war kostenpflichtig. Vorteil von Anfang an: plattformunabhängig (Brücke zwischen Softwareprodukten UND Betriebssystemen). Durch Offenlegung des Formats + ISO-Zertifizierung machte Adobe aus einem ursprünglich proprietären Format einen der wichtigsten Austausch-Standards.

#### Zitate (S. 163)
- MARKUS HIERMER (Revit-Spezialist): „Für mich ist openBIM keine echte Alternative. Bei der Reduktion von proprietären Datenformaten zu IFC verliere ich zu viele Daten. Solange es geht, arbeite ich im proprietären Format.“
- ING. MAG. ALFRED WASCHL: „IFC ist das Rückgrat von effizienten Datenmodellen. Dieser ISO-Standard ist weltweit gültig und erlaubt transparente Planung auf höchstem Niveau.“

#### Hersteller-Strategien (S. 163)
- Manche Softwarehersteller akzeptieren proprietäre Formate anderer Hersteller. Beispiel: Graphisoft Archicad 24 erlaubt, dass RVT-Dateien als Referenzmodell eingelesen und ausgeschrieben werden. Konkurrent Autodesk macht dies umgekehrt nicht.
- Jeder Hersteller verfolgt eigene Strategie zur Marktanteilsgewinnung; Dateiformate spielen entscheidende Rolle.

#### Tabelle 13 — Vor- und Nachteile der Formate (S. 163)
**Offen:**
- Vorteile: von allen verwendbar; unabhängig.
- Nachteile: größter gemeinsamer Nenner (nicht möglich ohne Datenverlust); Geometrie und Eigenschaftsparameter können „leiden“.

**Proprietär:**
- Vorteile: 100 % der Informationen bleiben erhalten, kein Datenverlust.
- Nachteile: Herstellerabhängigkeit (Insolvenz des Herstellers); Einstellung der Weiterentwicklung; Kosten (Erhöhung der Lizenzgebühren).

#### DWG / DXF (S. 164)
- Am Markt entscheiden nicht immer Sinnhaftigkeit und Qualität.
- DWG = proprietäres CAD-Format der Firma Autodesk. Autodesk lizensiert für DWG-Dateien lediglich eine Lese-/Schreibbibliothek an andere Hersteller.
- Versuche, DWG per Reverse Engineering öffentlich zu machen, gelangen nicht → lange juristische Auseinandersetzungen.
- DXF = ursprünglich von Autodesk als OFFENES Austauschformat für CAD-Dateien angedacht und offen zur Verfügung gestellt.
- Praxis-Paradox: Zum Datenaustausch werden viel öfter DWG-Dateien zugesandt als die dafür eigentlich vorgesehenen DXF-Dateien. DWG (proprietär) ist zum weltweit am häufigsten verwendeten Austauschformat für CAD-Daten geworden.

#### Offene Formate (S. 164)
- Werden i.d.R. durch ein standardisiertes Gremium festgelegt und weiterentwickelt; ohne technische/rechtliche Einschränkungen von allen nutzbar; Quellcode öffentlich.
- Bekannte offene Formate: HTML, CSV. → Es muss nicht immer IFC sein.
- CSV: schon vor BIM für offenen Datenaustausch tabellarischer Daten verwendet.
- Offenes Datenformat bringt immer gewissen Informationsverlust mit sich; transportiert im besten Fall den kleinsten gemeinsamen Nenner. Frage: Braucht man die verlorenen Daten?
- Vorteil offener Formate: in der inhomogenen BIM-Softwarelandschaft teils unverzichtbar, oft einzige Möglichkeit, dass alle Beteiligten Daten austauschen.
- Querverweis: open- und closedBIM → Kapitel 1, S. 42.

#### Rechtstipp — MAG. LUKAS ANDRIEU, LL.M. (Columbia), BSc. (S. 165): Verpflichtung zu (open-)BIM bei öffentlichen Aufträgen + Herstellerunabhängigkeit
- Technische Spezifikationen müssen allen Bewerbern und Bietern gleichen Zugang zum Vergabeverfahren gewähren.
- Öffentliche Auftraggeber, die BIM vorschreiben, müssen beachten: Gebot der neutralen Leistungsbeschreibung, Bietergleichbehandlung, allgemeines Diskriminierungsverbot.
- Vorschreibung einer ganz konkreten BIM-Software ist wohl unzulässig (vgl. **§ 106 Abs 5 BVergG 2018**). Anforderungen an Software → funktional/abstrakt beschreiben.
- In technischen Spezifikationen darf nicht auf bestimmte Herstellung/Herkunft verwiesen werden, wenn dadurch bestimmte Unternehmer begünstigt/ausgeschlossen werden.
- Vergaberechtlich Vorzug für System, in dem Wahl des Bearbeitungswerkzeugs frei + Plattform/Austauschformate herstellerunabhängig → fördert multidisziplinäre Modellbearbeitung durch mehrere Auftragnehmer.
- Aus Rechtssicherheit: Bieter sollten Software selbst wählen dürfen.

#### open contra closed (S. 165)
- Dateiformate entscheiden über openBIM vs. closedBIM.
- closedBIM-Konstellationen: vorwiegend proprietäre Formate. openBIM: offene Dateiformate, meist IFC.
- Reines closedBIM kommt in der Praxis eher selten vor; meist „hybridBIM“: Kernteam arbeitet in closedBIM, restliche Parteien werden über openBIM involviert.

#### Reality-Check open vs. closed (S. 166)
- Teil der Projekte in closedBIM, anderer in openBIM.
- openBIM vor allem im öffentlichen Sektor zunehmend auf dem Vormarsch.
- closedBIM eher im Umfeld großer Baufirmen und Generalunternehmer etabliert.
- closedBIM in Österreich = praktisch immer die Welt rund um die Autodesk-Plattform. In Europa ist Autodesk der einzige Hersteller mit annähernd ausreichender Software-Breite, um mit eigenem (proprietärem) Format über den Großteil der Fachsparten zu agieren.
- openBIM wird in der Region von allen anderen Softwareanbietern favorisiert → mehr verschiedene Produkte im Einsatz.
- Für Pflege/Weiterentwicklung einheitlicher Standards in openBIM ist buildingSMART verantwortlich.
- **Wechsel-Regel:** Ein in closedBIM gestartetes Projekt kann auf openBIM wechseln. Projekte, die in openBIM angelegt sind, können NICHT in closedBIM transformiert werden. (Abbildung 39: Proprietäres und offenes Umfeld bei hybridBIM)

---

### BIM und GIS (S. 167)
- Punktwolke = Datenformat aus dem Vermessungswesen, lässt sich nicht ohne Weiteres in BIM-Datenaustausch integrieren.
- Punktwolken und Vermesser:innen sind in GIS-Systemen zu Hause; Integration zwischen BIM und GIS „steckt noch in den Kinderschuhen“.

#### Rechtstipp — MAG. THOMAS SCHWAB: BIM und Datenschutz (S. 167)
- DSGVO anwendbar, wenn personenbezogene Daten natürlicher Personen ganz/teilweise automatisiert verarbeitet werden. Bei BIM-Projekten ist immer von automatisierter Verarbeitung auszugehen.
- Personenbezogene Daten = alle Informationen, die sich auf identifizierte/identifizierbare natürliche Person beziehen.
- Beispiele bei BIM: Titel, Geschlecht, Name, E-Mail-Adresse, IP-Adressen des zugreifenden Endgeräts, Protokolldaten (Zugriff auf Software, Änderungen u.ä. der Nutzer).
- Quelle Fußnote 110: Eschenbruch/Leupertz, BIM und Recht² (2019), Datenhoheit, Datenschutz, Vertraulichkeiten und Urheberrechte, Rz 63.

#### Praxistipp — Pflichten nach DSGVO (S. 168)
- Einhaltung der Grundsätze der DSGVO
- Verarbeitung nur mit Rechtsgrundlage
- Einhaltung der Informationspflichten der betroffenen Person
- Wahrung der Betroffenenrechte
- Führung des Verarbeitungsverzeichnisses
- Abschluss notwendiger Vereinbarungen mit Auftragsverarbeitern

#### 3D-Laserscan (S. 168)
- Einfache Form des Laserscans = Barcodeleser.
- 3D-Laserscanning in vielen Disziplinen im Vormarsch: Geomorphologie (digitale Höhenmodelle), Agrartechnik (Flächennutzung überwacht), Materialprüfung (Mikrorisse erkannt), Stadtplanung (Entscheidungsgrundlage).
- Im Bauwesen kommen Laserscans normalerweise vom Vermessungsbüro. Klassische Vermessungsgeräte (Tachymeter, Theodolit) werden für Baudokumentation zunehmend durch Laserscanner abgelöst.
- Häufigste Anwendung am Bau: Bestandsaufnahme; auch Qualitätssicherung + Dokumentation (z.B. Installation unter Supermarktdecke einscannen, ehe abgehängte Decke geschlossen wird).

#### Formen des Laserscannens (S. 169–170)
- **Airborne Laserscanning (ALS):** In der Geodäsie ersetzt ALS zunehmend die klassische Fotogrammetrie zur Topografie-Ermittlung. Ursprünglich Flugzeuge/Helikopter, mittlerweile Drohnen im Vormarsch. Riesige erfasste Flächen → enorm große Datenmengen / Abstriche bei Messdichte. **Punktgenauigkeit ALS: meist noch im Dezimeterbereich; mit Drohnen eher Zentimeterbereich.**
- Abbildung 40: Oberflächenmodell; Abbildung 41: Digitales Geländemodell (DGM) mit ALS (Fußnoten 111/112: DI Peter Skalicki-Weixelberger).
- **Terrestrisches Laserscanning (TLS):** für Bestandsaufnahme meist verwendet. Aufnahmeposition normalerweise statisch fixiert. Wegen „Verschattungen“ bei fast jeder Position fast immer mehrere Messungen von verschiedenen Standorten nötig; per Zielmarken später exakt zusammenführbar. **Mit modernen TLS-Systemen Punktgenauigkeit bis zu 1 Millimeter.**
- Abbildung 42/43: Terrestrischer Laserscanner auf Stativ mit Zielmarken; Positionierung ohne Verschattungen (Fußnoten 113: IGMS, TU Graz; 114: Raphael Wieser).
- **Handgeführtes Laserscanning:** wird Anwendungsbereich/Akzeptanz künftig massiv steigern; aktuell geringere Reichweite, empfindlicher.

#### Strukturierte vs. unstrukturierte Punktwolken (S. 171)
- Mobile Scanner → nur unstrukturierte Punktwolken.
- Terrestrische Scanner → strukturierte Punktwolken (durch fixen Messstandort Information, wo der Punkt herkommt).

#### Tabelle 14 — Kostenlose 3D-Viewer für Punktwolken (S. 171)
- Cloudcompare (MAC): https://asmaloney.com/software/
- Cloudcompare (WIN): https://www.danielgm.net/cc/
- Meshlab (WIN & MAC): https://www.meshlab.net/#download
- GOM Inspect (WIN): https://www.gom.com/de/3d-software/gom-inspect-suite/systemunabhaengige-inspektionssoftware/3d-inspektion.html

#### Nutzen 3D-Laserscanning (S. 171)
- Größter Vorteil: hohe Messgenauigkeit → genauere Planungsgrundlage; vermeidet teure Planungsfehler; bessere Machbarkeits-Entscheidungsgrundlage.
- Bei großflächigen/komplexeren Geometrien inzwischen kostengünstiger und schneller als herkömmliche Methoden.
- Inhaltlich neue Möglichkeiten: Erfassung von TGA-Leitungen, unregelmäßigen Altbauoberflächen.

#### Punktwolken (S. 171)
- Punktwolke = Rohform der von 3D-Laserscannern gelieferten Daten. Laser erfasst alle materiellen Bereiche (Wände, Installationsleitungen, Straßen).
- Für jeden abgetasteten Materialbereich = ein Messpunkt; Summe = Wolke mit verdichteten Bereichen.
- Jeder Punkt im **xyz-Koordinatensystem** genau verortet.
- Zusätzliche Attribute je nach Scanner: Vektor zur Orientierung, RGB-Wert (Farbe), Helligkeitswert, Aufnahmezeitpunkt, Messgenauigkeit.
- Hauptproblem: unglaublich große Datenmenge (Performance-Herausforderung). Ursachen: Unmenge an Punkten + Objektgröße (Städte/Infrastruktur).
- **Eine mittelgroße Punktwolke setzt sich schnell aus einigen hundert Millionen Punkten zusammen.**
- Spezielle Out-of-Core-Algorithmen nötig; sehr großer Arbeitsspeicher + möglichst mehrere schnelle SSD-Festplatten.

#### Reality-Check — Automatische Objekterkennung Punktwolke (S. 172)
- Nicht so einfach wie Werbung verspricht.
- Im Extremfall werden „innerhalb kürzester Zeit bis zu **80 %** automatische Elementerkennung“ versprochen → Welten von der Realität entfernt, „unseriöse Irreführung“.

#### Punktwolken-Workflow (S. 172)
- Empfänger dürfen/können oft keine derart großen Dateien annehmen (Sicherheitsbedingungen großer Konzerne/Behörden).
- **Regel:** In BIM-Dateien sollten Punktwolken IMMER nur verknüpft und NIE importiert werden. Dafür zentraler Ablageort nötig, auf den alle zugreifen.
- Workflow: Bereich mit 3D-Laserscanner einscannen → Einlesen in Modelliersoftware („as-built-modelling-workflow“) noch nicht vollständig automatisiert → nur Teilbereiche als BIM-Objekt erkennbar.
- Punktwolkendaten zuerst in 3D-Scansoftware einlesen, dann mit richtigen Einstellungen in Modelliersoftware exportieren. Vorsicht: richtige Einstellungen/Dateiformate selten beim ersten Versuch → trial-and-error.
- In 3D-Scannersoftware: Daten „gesäubert“ (Filterung, z.B. bewegliche Objekte herausrechnen) → dann **Registrierung** = automatisches/manuelles Zusammensetzen (Überlagern) mehrerer Scan-Files zu einer Punktwolke.

#### Weitere Software-Funktionalitäten (S. 173)
- Liste der Programme: https://de.wikipedia.org/wiki/Liste_von_Programmen_zur_Punktwolkenverarbeitung
- **Regionalisieren:** Aufteilen für kleinere Bearbeitungsbereiche (bessere Performance), z.B. Aufsplitten in Geschosse.
- **Vermaschen:** Punkte polygonalisieren → Geländeoberflächen.
- Manche Software interpretiert Schnitte/Grundrisse im DWG-Format.
- Halbautomatisierte Elementerkennung: Grundproblem — Scan liefert nur gesamtheitliche Oberfläche, keine einzelnen Körper; stark abhängig vom hinterlegten Elementkatalog (meist Standardprodukte aus Heimatland des Herstellers → österreichische Produkte selten erkannt).
- Beim heutigen Stand müssen Punktwolkendaten zum größten Teil in der Modelliersoftware nachmodelliert werden. Manche Software bietet Plugins für gebräuchlichste Modelliersoftware (paralleles Modellieren mit Elementkategorien).
- Problem: unübersichtliche Anzahl von Dateiformaten für Punktwolken (viele Hersteller, kein einheitliches Format für Modelliersoftware-Verknüpfung). Standardformat dürfte noch viele Jahre dauern → künftig evtl. „intelligentere Punktwolken“ mit AI-Technologien für zuverlässigere Elementzuordnung.

#### BIM und GIS — Koordinatensysteme (S. 173)
- In gescannter Punktwolke richten sich Punkte (xyz) an einem **kartesischen Projektkoordinatensystem (PCS)** aus.
- Bei großflächigen Infrastruktur-Scans ab gewisser Größe muss die **Erdkrümmung** einbezogen werden. Einige 3D-Scannersoftwares wandeln kartesische Punktwolke in georeferenzierte um → erdbezogenes Koordinatensystem wie **Gauß-Krüger-System**.

#### BIM vs. GIS — Grundlegende Unterschiede (S. 174–177)
- BIM-Modell: spielt in einem Projektkoordinatensystem ab. GIS-basiertes Modell: bezieht sich auf Koordinatensystem der realen Welt.
- GIS NICHT einfach als perfektes Repository (verwaltetes Verzeichnis) für BIM nutzbar.
- Beide behandeln 3D-Objekte, beruhen aber auf unterschiedlichen Herangehensweisen → Daten nicht ohne Weiteres zwischen Systemen synchronisierbar.
- Abbildung 44: unterschiedliche Modellierungsparadigmen, IFC vs. CityGML (Fußnote 115: Nagel/Stadler/Kolbe 2009, Geoweb 2009, Vancouver, 27–31 July 2009, ISPRS).
- **BIM:** Modellieren startet mit Idee für Bauwerk; konstruktive Elemente + Attribute → digitales Modell VOR Errichtung. Implizite Geometrieerstellung durch parametrische Elemente (CSG = Constructive Solid Geometry).
- **GIS:** bildet reale Welt (Bestand) ab; meist nur topografische Abstraktion sichtbarer Oberflächen. Explizite Geometrieerstellung durch Akkumulation aller umschließenden Begrenzungsflächen (B-Rep). GIS-Objekte durch Vermessen der Realität (explizit) → meist nur sichtbare Oberflächen mit Orientierung Vorder-/Rückseite.
- Zitat DI PETER SKALICKI-WEIXELBERGER (S. 175): „Bei der Landebahn des Flughafens Graz (**Länge 3.000 m**) liegt aufgrund der Erdkrümmung der **Höhenunterschied im Dezimeter-Bereich**.“
- Querverweis Grundlagen der Geometrie → Kapitel 2, S. 76.
- **LOD (Level of Development) BIM:** Stufen 100 bis 500; Element wird schrittweise in Geometrie verfeinert + erhält mehr Attribute.
- **LOD im GIS:** bezieht sich nicht auf Entwicklungsstand der Elemente, sondern auf Grad der Generalisierung — vom Regionalmodell (viele Details weggelassen) über Bauwerksmodell zum Innenraummodell.
- Abbildung 49 (S. 180): Drei in Revit als Geschossdecke erstellte Elemente → bei IFC-Export unterschiedliche Klassen: **IfcRoof** (Flachdach), **IfcSlab** (Geschossdecke), **IfcFooting** (Fundamentplatte).
- BIM-Objekte werden i.d.R. mit impliziten Verfahren erstellt (geometrisches Konstruktionsverfahren nachvollziehbar; einfaches Parametrisieren, z.B. Länge ändern). Schwierig: implizit erstellte historisch verformte Wandoberfläche nachbilden.

#### Reality-Check — Zusammenarbeit BIM und GIS (S. 176)
- BIM → GIS: Objekte in Oberflächen zerlegen, die meisten Attribute als Datenverlust abschreiben.
- GIS → BIM: zusammengehörende Oberflächen zu Objekt/Element sammeln, manuell jedes Objekt richtiger Kategorie zuweisen, dann benötigte Attribute ermitteln/anfügen.
- Momentan sehr mühsam; künftig viel Entwicklungsarbeit nötig (Brücken in GIS, Lagepläne in BIM).
- Abbildung 46: Bei BIM→GIS-Umwandlung Informationsverlust (z.B. Wärmeleitfähigkeit einzelner Wandflächen sinnlos).
- Abbildung 47: Bei GIS→BIM unklar, zu welcher Wand der Überschneidungsbereich im T-Stoß / welche Wandflächen zu welcher Wand gehören.

#### Nutzen BIM+GIS-Verbindung (S. 177–178)
- Praxis braucht Daten aus beiden Welten; Verbindung BIM-Objekte + GIS-Standortdaten bei fast jedem Projekt gewünscht.
- Beispiel: freies Grundstück in Großstadt bebauen → Fragen zu Erschließung/Baustellenlogistik; Planer wollen wissen, welche Leitungen am/rund um Grundstück verlegt sind.
- Heute noch nicht alle Leitungen digital erfasst. Vision: künftige digitale GIS-Pläne mit allen Leitungen als klassifizierbare BIM-Objekte; aktuell nicht einmal alle dafür benötigten IFC-Klassen und Attribute spezifiziert.

#### Tabelle 15 — Unterschiede zwischen BIM und GIS (S. 178)
| Merkmal | BIM | GIS |
|---|---|---|
| Bestimmendes Koordinatensystem | Kartesisches Projektkoordinatensystem | Georeferenziertes Weltkoordinatensystem |
| Modell | Modell zukünftig geplanter Objekte | Modell bereits bestehender Objekte |
| Standard für Austausch | IFC | CityGML |
| Skalenbereich | Gebäude | Stadt, Landschaft |
| Detaillierungsgrad | LOD 100 – LOD 500 | LOD 1 – LOD 4 |
| Objekte | als Volumenelemente | als einzelne Flächen |
| Geometrie | Implizite Verfahren | Explizite Verfahren |

- Abbildung 48: GIS- und BIM-Daten in einem Modell (Fußnote 117: computer-spezial.de).

---

### Objektorientierte Modellierung (S. 179)
- Daten brauchen Systematiken/Schemata zur Ordnung; je strukturierter, desto höhere Qualität + Verwertbarkeit.
- **Klassifizierung** = Wissensstruktur, die abstrakte Elemente (Objekte) über Auswahl/Filterung entsprechenden Kategorien (Klassen) zuordnet. Über übereinstimmende Merkmale (Attribute) werden Objekte (auch immateriell, z.B. Prozesse, Rollen) abgegrenzt/zugewiesen.
- Ohne Klassifizierungssysteme kein BIM-konformes Arbeiten. Klassen = Grundlage für funktionierenden Datenaustausch. Eine exportierte Tür sollte beim Import wieder als Tür klassifiziert werden. Nicht-klassenzugeordnete Daten gehen beim Austausch verloren.
- Objekte von Anfang an richtiger Klasse zuweisen (oft automatisch durch Typenauswahl/ausgereifte Templates). Wand wird meist automatisch korrekt zugeordnet. Bei „Decke“ ist spezielle Zuweisung nötig — kann Bodenplatte, Fußbodenaufbau, Geschossdecke, abgehängte Decke oder Flachdach sein.
- Klassifizierungssysteme sollten projektübergreifend gültig sein, nicht erst während eines Projektes entstehen.
- Weltweit mehrere Institutionen arbeiten an Klassifizierungen, aber nicht alle an universell gültigem Schema → Projektbeteiligte müssen sich vor Projektbeginn auf gemeinsames Schema einigen.
- Querverweis: Projekt aufsetzen + Templates → Kapitel 2, S. 86.

#### OOM-Konzept (S. 180)
- Objektorientierte Modellierung = ursprünglich Konzept aus Softwareprogrammierung; von Bauwirtschaft für Einteilung in Klassen/Objekte + Beziehungen übernommen.
- **Eine Instanz einer Klasse = Objekt.** Objekt kann reales Bauteil sein (Wand, Fenster, Lüftungskanal) oder abstrakt (Rolle, Raum, Bedingung, Last).

#### Reality-Check — Was ist ein BIM-Objekt? (S. 181)
- Softwaretechnisch: BIM-Objekt = Instanz einer Klasse eines BIM-Informationsmodells. → Alle Modellelemente eines digitalen Bauwerksmodells sind BIM-Objekte (digitale Bausteine / digitale Abbildung von Bauteilen).
- BIM-Objekte enthalten geometrische + alphanumerische Informationen, zueinander in Beziehung gesetzt + auswertbar (z.B. Bauteillisten). Sollte alle Infos zum Entwerfen, Finden, Spezifizieren, Analysieren aufnehmen.
- Vereinbarte Detaillierungs- + Informationsgrade (**LOD/LOI**) sollen sich im BIM-Objekt widerspiegeln (Fußnote 118: baunetzwissen.de).
- Abbildung 50: Objekte am Beispiel einer Wand (Fußnote 119: Bormann et al., S. 30).

#### UML-Darstellung von Klassen/Objekten (S. 182)
- In einer Klasse werden ähnliche Objekte zusammengefasst.
- Notation: **UML (Unified Modeling Language)**, ISO-zertifiziert.
- **Klassendiagramm (Abb. 51):** in drei Abschnitte geteiltes Rechteck. Oben: Name der Klasse (z.B. Wand). Zweiter Bereich: Attribute (Eigenschaften/Merkmale), durch Doppelpunkt vom Datentyp getrennt. Dritter Bereich: Methoden (Operationen) — im BIM meist leer (nur statische Daten, keine Funktionalitäten ausgetauscht).
- **Objektdiagramm (Abb. 52):** einzelne Ausprägungen einer Klasse = Objekte (z.B. Wand 1, Öffnung 1, Öffnung 2). Nur zwei Felder. Oben: Objektname + (Doppelpunkt) zugehörige Klasse, unterstrichen zur Erkennung als Objekt. Zweites Feld: alle Attribute aus Klassendiagramm mit „=“-Zeichen + Wert.
- Alle Objekte einer Klasse besitzen genau die gleichen Attribute; Attributwerte individuell. Funktioniert nur, wenn der angegebene Wert dem angegebenen Datentyp entspricht.

#### Tabelle 16 — Datentypen und deren zulässige Einheiten (S. 183)
| Kategorie | Typ | Beispiele |
|---|---|---|
| Primitive Typen | Ganzzahl (INT, INTEGER, LONG) | -123, 0, 2, 875 |
| | Gleitpunktzahl (FLOAT, DOUBLE) | -1.234, 1.234e02 |
| | Wahrheitswert (BOOL, BOOLEAN, LOGICAL) | true (0), false (1) |
| | Zeichen (CHAR, CHARACTER) | a, A, α, 7, ≥, ∞ |
| Aufzählungstypen | Aufzählung (ENUM, ENUMERATION) | Farbe := {BLAU, GRUEN, ROT, GELB}; Längeneinheit := {MM, CM, DM, M, KM}; Betonfestigkeitsklasse := {C12/15, C16/20, …, C100/115} |
| Feldtyp | Feld/Reihung (ARRAY), endliche indexbasierte Folge von Werten eines Basistyps | 3D-Vektor := ARRAY(1..3) of DOUBLE, z.B. [-1.23, 4.56e-5, 123.45] |
| Komplexe Typen | Klasse (CLASS, STRUCT), endliche Menge an Attributen unterschiedlichen Typs | Klasse Datum := {tag:INT, monat:INT, jahr:INT}, z.B. {15, 2, 2012} |
| | Liste/Folge (LIST), (un-)endliche indexbasierte Folge von Werten eines komplexen Typs | Öffnungsliste := LIST of CLASS(Oeffnung), z.B. [O1, O2] |
| | Menge (SET), (un-)endliche unsortierte Menge von Werten eines komplexen Typs | Öffnungsmenge := SET of CLASS(Oeffnung), z.B. {O1, O2} |

- Besitzen alle Objekte einer Klasse für ein Attribut den gleichen Wert → kein Objektattribut mehr, sondern Klassenattribut.
- In Modelliersoftware: statt Objekt-/Klassenattribut spricht man von **Instanz- und Typmerkmalen**.

#### Vererbung (S. 184)
- Wichtigste Verknüpfung = Vererbung. Basisklasse (= Elternklasse, Oberklasse, Superklasse) vererbt alle Attribute an eine/mehrere abgeleitete Klassen (= Kindklasse, Unterklasse, Subklasse).
- Abgeleitete Klassen haben meist weitere eigene Attribute → Spezialisierung. Basisklassen = Generalisierungen.
- Praxisbeispiel Hierarchie: Basisklasse „Wand“ → nach Material in Unterklassen (Betonwand, Mauerwerkswand …). Betonwand → nach Herstellung spezialisiert (**Höhe kleiner oder größer 3 m**). Weitere Spezialisierung Innen-/Außenwand (Bauphysiker-Interessen).
- Nicht jedes Mal neue Klasse nötig: z.B. Statiker durch Attribut **tragend/nichttragend** berücksichtigen. Auswertungen über Klassenzuordnung und/oder Attributwerte filterbar.
- Von Basisklasse vererbte Attribute = in abgeleiteter Klasse automatisch Typ-Attribute; neue Attribute = Instanz-Attribute.
- Klassenstruktur schon vor Modellierstart überlegen; mit Erfahrung jedes neuen Projektes verfeinern. Am besten im Template der Modelliersoftware mitführen.
- Abbildung 53: Vererbung Wand → Betonwand → über 3 m → Außenwand (Fußnote 120: Bormann et al., S. 52).

#### Weitere Beziehungen zwischen Klassen (S. 185–186)
- **Assoziation:** einfachste Verknüpfung, dargestellt durch Linie zwischen Klassen. Präzisierbar durch **Multiplizitäten** (wie viele Objekte einer Klasse mit wie vielen Objekten einer anderen verknüpft). Schreibweise: `0..2` = 0–2 Objekte verknüpft; `*` = beliebig viele Objekte. (Abb. 54, Fußnote 121: Bormann et al., S. 54)
- **Aggregation:** besondere Form der Assoziation, Ganze-Teil-Beziehung. Objekt Klasse 1 hat/besitzt Objekt Klasse 2, beide können unabhängig voneinander existieren. Darstellung: **leere Raute** am Ende der Verbindungslinie. (Abb. 55, Fußnote 122: Bormann et al., S. 54)
- **Komposition:** Sonderform der Aggregation — Klasse kann NICHT mehr unabhängig von der ersten existieren. Darstellung: **volle Raute**. (Abb. 56, Fußnote 123: Bormann et al., S. 55)

#### Nomenklatur (S. 186)
- In Praxis oft zu wenig Wert auf klar verständliche, funktionale Nomenklatur gelegt.
- Schlechtes Beispiel: „Wa-B-h>3-au“. Besser: „wand_beton_hoeheueber320cm_aussenwand“.
- IT-Verarbeitungsregeln: keine Sonderzeichen; Umlaute ä/ü/ö/ß als ae/ue/oe/ss; nur Unterstrich (_) als Trennzeichen; alles in Kleinbuchstaben.

#### bSDD (buildingSMART Data Dictionary) (S. 186–188)
- BIM-Objekte = Klassen-zugeordnete, mit Attributen versehene Objekte (nicht bloß 3D-Geometrien).
- Problem gleiche Sache, verschiedene Begriffe: Architekt „Isolierfaktor“, Bauphysiker „U-Wert“, Hersteller „Wärmeleitfähigkeit“ — alle meinen dasselbe. In BIM-Projekt einheitlicher Begriff nötig.
- Internationale Projekte: „Tür“ vs. „door“ vs. „Tuer“ — Suche nach Klasse „Tür“ erfasst „door“/„Tuer“-Objekte nicht → fatale Folgen.
- bSDD = Wörterbuch für Klassen + Attribute mit „Google-Translate-Funktion“; von buildingSMART entwickelt, laufend weiterentwickelt, als Cloud Service offen (openBIM).
- Eindeutige ID für alle Klassen/Attribute im Hintergrund → landesspezifische Darstellungen verweisen immer auf richtige Klasse.
- **Norm: ISO 12006-3** = Basis für das bSDD.
- Suche: https://search.bsdd.buildingsmart.org/  (Abb. 57: Klasse „door“ im bSDD)
- bSDD derzeit nur in sehr wenigen Softwareprodukten integriert; BIM noch mehr „trial-and-error“ als „plug-and-play“. Übersetzung Modelliersoftware-Klassen → IFC-Klassen des bSDD ist für Einsteiger Herausforderung.
- Für Hochbau weit ausgearbeitet; für Infrastruktur meist nur Arbeitsgruppen; Landschaftsarchitektur fast nichts. In TGA vorbildlich im Projekt **metaTGA der TU Graz** ausgearbeitet (http://www.metatga.org/).

#### ASI-Merkmalserver (S. 188–189)
- Forschungsgruppe **freeBIM** an Universität Innsbruck leistete vor >5 Jahren Pionierarbeit; Österreich Vorreiter in europäischer Entwicklung.
- Merkmalserver = Grundlage für nationale + europäische Normengebung; essenzieller Bestandteil der **ÖNORM A 6241-2**.
- Merkmalserver = Datenbank zur Sammlung „Eigenschaften von Bauteilen und Materialien“; Ziel: beschreibende Eigenschaften mit bSDD abgleichen + um nicht vorhandene Werte ergänzen (Fußnote 125: http://db.freebim.at).
- Zugang als Open Source für jedermann; Abb. 58/59: Bauteileigenschaften im Merkmalserver (Fußnoten 126/127: db.freebim.at).

---

### IFC (Industry Foundation Classes) (S. 190)
- Anerkannte Standards = wichtiger Faktor für Industrie-Weiterentwicklung. Standard für Austausch in openBIM-Prozessen = IFC.
- IFC = offener, internationaler Standard der Bauindustrie, von buildingSMART definiert + kontinuierlich weiterentwickelt.
- Streng genommen ist IFC KEIN Dateiformat, sondern nur ein **Schema**, das Geometrie, Daten und Beziehungen transportiert.

#### buildingSMART (S. 190)
- buildingSMART international (bSi) = weltweite Dachorganisation; erarbeitet offene Standards + Zertifizierungsrichtlinien für Digitalisierung im Bauwesen; offizielle Interessensvertretung von openBIM.
- In >20 Ländern nationale Niederlassungen („Chapters“). **Austrian Chapter Anfang 2018 gegründet.**
- buildingSMART Austria (bSA): setzt sich für openBIM in Österreich ein; closedBIM wird von bSA als nicht zukunftsträchtig gesehen und ignoriert.
- bSi-Fokus ursprünglich Gebäudedomäne; in letzten Jahren erweitert auf Städte + Infrastruktur.
- www.buildingsmart.co.at

#### Zertifizierung (S. 190–192)
- bSi testet Softwareprodukte auf korrekten IFC-Import + -Export → Import und Export werden GETRENNT zertifiziert (Produkte mit nur Import oder nur Export möglich).
- Zertifikate separat für **IFC 2x3** und **IFC4**. Für IFC4 fast keine Produkte zertifiziert, viele Zertifizierungen in Bearbeitung; für **IFC 4.1 gibt es noch gar nichts**. → Fortschritte von IFC4 und höher faktisch noch kaum umsetzbar.
- Zertifizierungs-Teilnehmer: https://technical.buildingsmart.org/services/certification/ifc-certification-participants/

#### Tabelle 17 — Weitere von bSI betreute Standards (S. 191)
| Name | Beschreibung | Standard |
|---|---|---|
| IFC | Industry Foundation Classes — branchenspezifisches Datenmodellschema | ISO 16739 |
| IDM | Information Delivery Manual — Methode zur Definition/Dokumentation von Geschäftsprozessen und Datenanforderungen | ISO 29481-1, ISO 29481-2 |
| MVD | Model View Definition — Datenmodellaustauschspezifikation | buildingSMART MVD |
| BCF | BIM Collaboration Format — modellbasierte, softwareunabhängige Kommunikationsprotokolle | buildingSMART BCF |
| bSDD | buildingSMART Data Dictionary — Standardbibliothek mit allg. Definitionen von BIM-Objekten und ihren Attributen | buildingSMART bSDD |

#### Personen-/Firmenzertifizierung (S. 192)
- bSi zertifiziert auch Personen + Firmen. Firmen: Professional Certification (angedacht); Personen: Individual Certification.
- bSi ist momentan einzige Institution mit weltweit anerkanntem BIM-Zertifikat **Level A (Basiskenntnisse)**.
- Aufbauend führt bSA Zertifizierungen ein: **Level B (BIM-Koordination)** und **Level C (BIM-Projektsteuerung)**.
- Abb. 60: Ausbildungspyramiden bSI und bSA.

#### IFC — Funktionsweise (S. 192–193)
- IFC = „das PDF von BIM“. Analogie Word/PDF: native Datei direkt editierbar (mit Programm); PDF nur kommentierbar, Änderung beim Urheber anfordern.
- IFC = eingefrorene Momentaufnahme der Originaldatei, nutzbar für Kollisionserkennung, Kostenschätzungen, Simulationen. Nie zum Editieren durch Empfänger gedacht.
- IFC transportiert NICHT den eigentlichen Modellinhalt, sondern referenziert nur darauf → alle Fachplaner behalten Rolle der Eigentümer ihres Teilmodells; Verantwortungen klar abgrenzbar.
- Typischer Austausch (Abb. 61/62, Fußnoten 128/129: Baldwin): Sender → IFC-Datei an Empfänger → Empfänger verlinkt + prüft → bei Änderungsbedarf Änderungsanfrage (z.B. per BCF) an Sender → Sender liefert überarbeitete Datei wieder als IFC.

#### IFC-Versionen (S. 194)
- Beim IFC noch relativ viel Bewegung; buildingSMART arbeitet laufend an verbesserten Versionen.
- Erste IFC-Versionen unterscheiden sich wesentlich von Nachfolgern und sind nicht miteinander kompatibel. **Ab Version 2x** baute jede Version auf der vorangehenden auf und erweiterte sie → Kern-Kompatibilität mit Vorgängerversion.
- **IFC2x3** (2006 offiziell veröffentlicht) wird derzeit am häufigsten verwendet; dafür am meisten Software für Import + Export zertifiziert.
- **IFC4:** bessere Übergabe komplexer Geometrien. **2013 wurde IFC4 offizieller ISO-Standard (ISO 16739:2013)**, trotzdem noch nicht Praxis-Standard (meiste Software noch nicht für IFC4 zertifiziert).
- Einführung von BIM = mehrere Jahrzehnte andauernder Prozess.
- Abb. 63: Neustrukturierung des IfcSpatialStructureElement (Verortungsstruktur) in **IFC4.3** (Fußnote 130: buildingSMART.de).

#### MVD (Model View Definition) (S. 195)
- Beim Abspeichern eines IFC aus proprietärer Datei muss nicht immer alles gleich sein; via MVDs nur erforderliche Teilinhalte transportieren.
- MVD = Unterspezifikation des gesamten IFC-Schemas, spezialisiert für bestimmte Anforderung/Workflow.
- Für jede IFC-Version gibt es von buildingSMART standardisierte MVDs; eigene projektspezifische MVD theoretisch möglich, meist greift man auf bSi-Vorgaben zurück.
- **IFC2x3:** Coordination View am häufigsten verwendet (optimiert für Austausch + Koordination von Modellen). Insgesamt 4 weitere offizielle MVDs von bSi.
- **IFC4:** derzeit zwei offizielle MVDs:
  - **IFC4 Reference View:** Nachfolger der IFC2x3 Coordination View, ausschließlich zur Referenzierung (alle Rechte beim Urheber); Geometrie mit tessellierten Oberflächen für geringere Dateigröße optimiert.
  - **IFC4 Design Transfer View:** erstmals Gedanke des IFC-Roundtrip; bessere geometrische Beschreibung (advanced BREPs); für Übergabe einzelner detaillierter Elemente zur Weiterbearbeitung (z.B. Architekt übergibt tragende Betonelemente an Statiker → Fugen + Fugenbänder einarbeiten).
- MVD-Datenbank: https://technical.buildingsmart.org/standards/ifc/mvd/mvd-database/
- **Norm: ISO 16739:2013**
- Abb. 64: Weiterentwicklung MVDs und IFC.

#### IFC richtig exportieren (S. 196–197)
- Essenziellste Aufgabe: richtiges Abspeichern von IFC-Dateien (welche Einstellungen für gutes IFC?) → trial-and-error.
- Video-Tutorials (YouTube-Channel) für die drei wichtigsten Modelliersoftwareprodukte: **Archicad, Revit, Allplan**.
- **Export:** Klasse der Ursprungssoftware muss über eine **Mappingtable** in entsprechende IFC-Klasse übersetzt werden. **Import:** IFC-Klasse über Mappingtable in Klasse der Zielsoftware umwandeln.
- Querverweis: Grundlagen der Geometrie → Kapitel 2, S. 76.
- Abb. 65: Verschiedene MVDs desselben Gebäudes (Fußnote 131: Autodesk, Revit IFC Handbuch, 02/2018). Abb. 66: Mappingtables für Export und Import bei IFC.

### Literaturverzeichnis (S. 198–199)
- Baldwin, Mark: Der BIM-Manager, Praktische Anleitung für das BIM-Projektmanagement, 2. Auflage (2019), DIN Deutsches Institut für Normung e.V., Mensch und Maschine (Hrsg.), Beuth Verlag Berlin (ISBN 978-3-410-29440-5).
- http://db.freebim.at (Zugriff 10.12.2021).
- Borrmann, André; König, Markus; Koch, Christian; Beetz, Jakob (Hrsg.) (2015): Building Information Modeling. Technologische Grundlagen und industrielle Praxis. Berlin, Heidelberg, Springer-Verlag (ISBN 978-3-658-05605-6).
- https://www.computer-spezial.de/artikel/integration-von-gis-und-bim_3434779.html (Zugriff 10.12.2021).
- Kaden, Robert; Clemen, Christian; Seuß, Robert; Blankenbach, Jörg; Becker, Ralf; Eichhorn, Andreas; Donaubauer, Andreas; Kolbe, Thomas H.; Gruber, Ulrich (Hrsg.): Leitfaden Geodäsie und BIM, Version 2.1 (2020), DVW-Merkblatt 11-2020, DVW e.V. – Gesellschaft für Geodäsie, Geoinformation und Landmanagement; Runder Tisch GIS e.V.

---

## Maschinen-Regeln

- [DEFINITION] Proprietäres Format = nur ein Hersteller definiert das Format; Quellcode = Handelsgeheimnis; nur dieser kann Nutzung honorieren (S. 162).
- [DEFINITION] Natives Format = proprietäres Format, das nur von einer einzigen Anwendung genutzt wird (S. 162).
- [DEFINITION] Offenes Dateiformat = durch standardisiertes Gremium festgelegt/weiterentwickelt, ohne technische/rechtliche Einschränkungen nutzbar, Quellcode öffentlich; Beispiele HTML, CSV (S. 164).
- [DEFINITION] DWG = proprietäres CAD-Format der Firma Autodesk; Autodesk lizensiert nur eine Lese-/Schreibbibliothek (S. 164).
- [DEFINITION] DXF = ursprünglich von Autodesk als offenes CAD-Austauschformat angedacht und offen bereitgestellt (S. 164).
- [PFLICHT] Vorschreibung einer konkreten BIM-Software bei öffentlichen Aufträgen wohl unzulässig; Software funktional/abstrakt beschreiben (§ 106 Abs 5 BVergG 2018, S. 165).
- [PFLICHT] Technische Spezifikationen dürfen nicht auf bestimmte Herstellung/Herkunft verweisen, wenn dadurch Unternehmer begünstigt/ausgeschlossen werden (Rechtstipp, S. 165).
- [PFLICHT] Bei BIM-Projekten DSGVO anwendbar (immer automatisierte Verarbeitung anzunehmen) — Pflichten: DSGVO-Grundsätze, Rechtsgrundlage, Informationspflichten, Betroffenenrechte, Verarbeitungsverzeichnis, Auftragsverarbeiter-Vereinbarungen (S. 167–168).
- [DEFINITION] Wechsel-Regel openBIM/closedBIM: closedBIM→openBIM möglich; openBIM→closedBIM NICHT transformierbar (S. 166).
- [DEFINITION] hybridBIM = Kernteam in closedBIM, restliche Parteien über openBIM involviert (S. 165).
- [ABSTAND] Punktgenauigkeit Airborne Laserscanning (ALS): meist Dezimeterbereich, mit Drohnen Zentimeterbereich (S. 169).
- [ABSTAND] Punktgenauigkeit modernes Terrestrisches Laserscanning (TLS): bis zu 1 Millimeter (S. 170).
- [DEFINITION] Mobile Scanner liefern unstrukturierte, terrestrische Scanner strukturierte Punktwolken (S. 171).
- [DEFINITION] Punktwolke = Rohform der 3D-Laserscanner-Daten; jeder Punkt in xyz-Koordinatensystem verortet; optionale Attribute: Orientierungsvektor, RGB, Helligkeit, Aufnahmezeitpunkt, Messgenauigkeit (S. 171).
- [PFLICHT] In BIM-Dateien Punktwolken immer nur VERKNÜPFEN, nie IMPORTIEREN; zentraler Ablageort für alle nötig (S. 172).
- [DEFINITION] Mittelgroße Punktwolke = einige hundert Millionen Punkte; braucht Out-of-Core-Algorithmen, großen RAM, mehrere schnelle SSDs (S. 171–172).
- [DEFINITION] Registrierung = automatisches/manuelles Zusammensetzen mehrerer Scan-Files zu einer Punktwolke (S. 172).
- [DEFINITION] BIM-Koordinatensystem = kartesisches Projektkoordinatensystem (PCS); ab großer Größe Erdkrümmung einbeziehen → georeferenziert (z.B. Gauß-Krüger-System) (S. 173).
- [DEFINITION] LOD BIM = Level of Development, Stufen 100–500; LOD GIS = Generalisierungsgrad, Stufen 1–4 (S. 175–178, Tabelle 15).
- [DEFINITION] BIM-Standardaustausch = IFC; GIS-Standardaustausch = CityGML (Tabelle 15, S. 178).
- [DEFINITION] BIM-Geometrie = implizite Verfahren (CSG, parametrisch, Volumenelemente); GIS-Geometrie = explizite Verfahren (B-Rep, einzelne Flächen) (S. 174–178).
- [DEFINITION] BIM-Objekt = Instanz einer Klasse eines BIM-Informationsmodells; enthält geometrische + alphanumerische Infos; spiegelt LOD/LOI wider (S. 181).
- [DEFINITION] Vererbung = Basisklasse (Eltern-/Ober-/Superklasse) vererbt Attribute an abgeleitete Klassen (Kind-/Unter-/Subklasse = Spezialisierung); vererbte Attribute = Typ-Attribute, neue = Instanz-Attribute (S. 184).
- [DEFINITION] Multiplizität-Schreibweise UML: `0..2` = 0–2 verknüpfte Objekte; `*` = beliebig viele (S. 186).
- [DEFINITION] Aggregation = Ganze-Teil-Beziehung mit unabhängiger Existenz, leere Raute; Komposition = abhängige Existenz, volle Raute (S. 185–186).
- [PFLICHT] Nomenklatur: keine Sonderzeichen; ä/ü/ö/ß → ae/ue/oe/ss; nur Unterstrich (_) als Trennzeichen; alles Kleinbuchstaben (S. 186).
- [DEFINITION] bSDD (buildingSMART Data Dictionary) = Klassen-/Attribut-Wörterbuch mit eindeutigen IDs; Basis-Norm ISO 12006-3 (S. 186–188).
- [DEFINITION] ASI-Merkmalserver = Datenbank für Eigenschaften von Bauteilen/Materialien; essenzieller Bestandteil der ÖNORM A 6241-2; Grundlage freeBIM/Uni Innsbruck (S. 188).
- [DEFINITION] IFC = offenes Schema (kein Dateiformat) für Geometrie, Daten, Beziehungen; Standard ISO 16739 (S. 190, Tabelle 17).
- [FRIST] Austrian Chapter von buildingSMART Anfang 2018 gegründet; buildingSMART in >20 Ländern (S. 190).
- [DEFINITION] bSi-Zertifizierungs-Level: A = Basiskenntnisse (bSi); B = BIM-Koordination, C = BIM-Projektsteuerung (bSA) (S. 192).
- [PFLICHT] IFC-Zertifizierung: Import und Export getrennt zertifiziert; separat für IFC 2x3 und IFC4 (S. 190–191).
- [DEFINITION] Standards von bSI (Tabelle 17): IFC=ISO 16739; IDM=ISO 29481-1/-2; MVD=buildingSMART MVD; BCF=buildingSMART BCF; bSDD=buildingSMART bSDD (S. 191).
- [FRIST] IFC2x3 = 2006 veröffentlicht, derzeit am häufigsten verwendet; IFC4 = 2013 offizieller ISO-Standard (ISO 16739:2013); IFC 4.1 noch keine Zertifizierung; IFC4.3 neue Verortungsstruktur (S. 194).
- [DEFINITION] Ab IFC-Version 2x Kern-Kompatibilität zur Vorgängerversion; frühere Versionen untereinander inkompatibel (S. 194).
- [DEFINITION] MVD = Unterspezifikation des IFC-Schemas für bestimmten Workflow; IFC2x3 Coordination View (+4 weitere); IFC4 Reference View (Referenzierung, tessellierte Oberflächen) + Design Transfer View (Roundtrip, advanced BREPs) (S. 195).
- [PFLICHT] IFC-Export: Ursprungssoftware-Klasse über Mappingtable → IFC-Klasse; Import: IFC-Klasse über Mappingtable → Zielsoftware-Klasse (S. 196).
