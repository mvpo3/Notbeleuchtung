# BIM-Handbuch-2022 — Teil 2
> Quelle: BIM-Handbuch-2022 (buecher) · dieser Teil (Seiten 81–120 von 348). Kapitel „Richtig Modellieren“ (Fortsetzung), „Richtiges Modellieren in Infrastrukturprojekten“ (Lukas Hochreiter, HABAU Group) und Beginn Kapitel 3 „BIM-Software“ (Marcus Wallner).

## Inhalt

### Positionierung des Modells (S.80–82)

- Solange alle in einem einzigen Modell arbeiten, gibt es nur eine, für alle gleiche Positionierung. Meist besteht ein BIM-Modell jedoch aus **Überlagerung der Teilmodelle der einzelnen Fachplaner:innen**.
- Zwingende Voraussetzung beim Überlagern: **absolut korrekte Positionierung** — nur dann funktionieren BIM-Funktionalitäten wie die **Kollisionsprüfung**. Besonders beim erstmaligen Überlagern große Sorgfalt walten lassen.

#### Nullpunkte / Projektbasispunkt (S.80, Fußnote 82: BIM Workbook CK)
- Aus der CAD-Planung bekannt: zwei Koordinatensysteme:
  - **Weltkoordinatensystem (WKS)**
  - **Benutzerkoordinatensystem (BKS)**
- Das BKS liegt auf dem WKS. Über den Nullpunkt des BKS wird das Projekt im WKS **georeferenziert**.
- In BIM-Projekten ist der **Projektbasispunkt** der zentrale dreidimensionale Nullpunkt eines jeden Projektes (= Modellursprung).
- Je nach Modelliersoftware wird dieser im **Koordinatensystem des jeweiligen Landes (Gauß-Krüger-Koordinatensystem)** georeferenziert. Mit dieser Georeferenz kann der Einfügepunkt später auf der Baustelle real eingemessen werden.

#### Normalnull (S.80)
- Georeferenzierung des Projektbasispunktes bezüglich Höhe: geografische Höhe wird in **Meter über Meer** angegeben.
- Der Projektbasispunkt wird innerhalb des Projektes meist mit **0,00 m** angesetzt.
- Dieser Punkt weist im Landeskontext zugleich eine Höhe über dem **Normalnull** auf, z. B. **353 m**.
- Normalnull bezieht sich meist auf die mittlere Höhe des Meeresspiegels, ist aber in fast jedem europäischen Land unterschiedlich definiert.
- In **Österreich**: Normalnull = **„Meter über Adria“**.

#### Praxistipp: Wie lege ich den Projektbasispunkt an? (S.81, Fußnote 83: Autodesk Leitfaden S.7)
- Wenn möglich, Projektbasispunkt zu Projektbeginn **genau auf den internen Nullpunkt der Modelliersoftware** legen (Verwechslungen vermeiden).
- **DWG-Dateien besitzen keinen Projektbasispunkt** → werden gerne mit ihrem Ursprung (Nullpunkt des BKS) auf den internen Ursprung der BIM-Software positioniert.
- Wenn Projektbasispunkt = interner Ursprungspunkt = gemeinsamer Austausch-Nullpunkt → wenigste Arbeit / Fehlerquellen.
- Projektbasispunkt sollte **nahe am Bauwerkmodell** liegen. Weit entfernte Position → erhöhte Rechenleistung, Softwareperformance-Einbußen, bei extremen Entfernungen sogar Fehler.
- Günstig: Projektbasispunkt **links unterhalb des Bauwerks**, so dass das Bauwerk im **positiven Bereich der XY-Achsen** liegt.
- Oft wird der Projektbasispunkt auf den **Kreuzungspunkt der Achsen A-A und 1-1** gelegt.
- Position sollte leicht/unmissverständlich beschreibbar sein. Beispiele: Achsenschnittpunkt, linke untere Ecke des Bauwerks, eine Ecke der Grundstücksgrenze.

**Tabelle 1 (S.81): Vorschlag für Angabe Nullpunkt und Projektbasispunkt in AIA bzw. BAP**
| Feld | Wert/Format |
|------|-------------|
| Nullpunkt X/Y, absolut | XX° AA' BB,CC'' / YY° AA' BB,CC'' |
| Nullpunkt Höhe | + 0,00 m über Meer |
| Projektbasispunkt | DIFF XX, DIFF YY, DIFF ZZ |

#### Normalnull-Unterschiede / Georeferenzierung (S.82)
- Deutschland bezieht sich auf den **Pegel in Amsterdam** → Unterschied zu Österreich (Adria) kann schnell **33 cm** betragen.
- Bei grenzüberschreitenden Infrastrukturprojekten ohne Einigung auf gemeinsames Normalnull → erhebliche Probleme.
- Quelle: https://de.wikipedia.org/wiki/Höhe_über_dem_Meeresspiegel
- Beim CAD können mehrere BKS auf dem WKS liegen; bei BIM-Projekten gibt es **nur einen Projektbasispunkt**, zu Projektbeginn festgelegt (oft automatisch über die Datei der Architektur / des Generalplaners).
- Nachfolgende Fachplanungen verlinken zu Beginn als Erstes die Architektendatei → gleicher Nullpunkt + gleiche Nordung.
- **Nullpunkt und Nordung dürfen im Projektverlauf unter keinen Umständen mehr geändert werden.**

#### Nordung (S.82)
- Durch Einfügen der Vermesserdaten ist der **reale Norden (geografischer Norden)** ersichtlich.
- In fast allen Projekten wird im **Projektnorden** gearbeitet: Sicht so gedreht, dass möglichst viele Wände orthogonal liegen (erleichtert Modellieren, mögliche Fehlerquelle).
- Unterschied beider Ansichten definiert über **Drehpunkt** (idealerweise = Projektbasispunkt) und **Winkel**.
- Projektbasispunkt + Winkel zwischen geografischem Norden und Projektnorden **unbedingt im BAP (BIM-Abwicklungsplan) festhalten**.

#### Praxistipp: Koordinationskörper (S.83, Fußnote 84: Autodesk Leitfaden S.8; http://www.vrame.com/know-how/empfehlungen/)
- Zu Beginn Koordinationsdatei mit Nullpunkt, Nordung (evtl. Raster) an alle Beteiligten verteilen.
- Am Nullpunkt kann ein **Koordinationskörper** sitzen: meist **Pyramide mit quadratischer Grundfläche**, Spitze auf dem Nullpunkt, quadratische Grundfläche folgt der Nordung.
- Beim Zusammenführen der Teilmodelle optisch kontrollierbar, ob die Pyramiden übereinanderliegen.

### Vertikale Gliederung (S.84–90)

#### Einteilung nach Geschossen (S.84, Fußnote 85: Autodesk Revit IFC Handbuch S.9)
- Orientierung am genormten **IFC-Schema** → gliedert das Modell eindeutig nach Geschossen.
- Geschosse = **IfcBuildingStorey**, gebildet durch Ebenen. In den meisten Modelliersoftwareprodukten bildet jede Ebene (nicht Referenzebene) automatisch ein neues Geschoss → nur **eine Ebene pro Geschoss** modellieren.
- Geschosse bilden Grundlage für Grundrisse; fast alle Objekte werden über den Einfügepunkt einem Geschoss zugewiesen.
- Bauablaufplanung (z. B. Betonierabschnitte) und Nomenklatur von Räumen/Türen beruhen auf Geschossen.
- IFC-Verortungsstruktur Hochbau: https://standards.buildingsmart.org/IFC/DEV/IFC4_3/RC1/HTML/schema/ifcproductextension/lexical/ifcbuildingstorey.htm

#### Geschoss-Null: OK Rohdecke (S.85)
- Architektur bezieht sich auf **Oberkante Fertigfußboden (OK FB)** (z. B. Brüstungshöhen, Räume).
- Statik rechnet meist in der **Tragwerksebene in der Schwerlinie** zwischen Oberkante Rohdecke (OK RD) und Unterkante Rohdecke (UK RD).
- Durchgesetzt (auch wegen IFC-Struktur): als **geschossbildende Ebene projektübergreifend die Oberkante Rohdecke (OK RD)** verwenden.
- Wichtig für Gebäudetechnik: Läge die Ebene auf OK Fußboden, wären alle Leitungen/Rohre im Fußboden dem **darunterliegenden** Geschoss zugeordnet.
- In **Revit** haben Ebenen ein zusätzliches Attribut **„Gebäudegeschoss“**; nur wenn angekreuzt, bildet die Ebene eine neue IfcBuildingStorey.
- Unterscheidung: **Geschossebenen (IfcBuildingStorey)** vs. **Modellierebenen**. Ohne Attributierung behilft man sich mit Referenzebenen.
- Modellierebene **Unterkante abgehängte Decke (UK AD)** sinnvollerweise im Teilmodell des Haustechnikers anlegen.

#### Praxistipp + Benennung Geschosse/Ebenen (S.87)
- Projektübergreifend von Anfang an auf **OK RD als geschossbildende Ebene** einigen; weitere Modellierebenen je nach Bedarf nur in Fachmodellen.

**Tabelle 2 (S.87): Benennungsvorschlag Geschosse/Ebenen**
| Abkürzung | Geschoss | Ebene |
|-----------|----------|-------|
| OG02_OKFF | 2. Obergeschoss | Oberkante Fertigfußboden |
| OG02_OKRD | 2. Obergeschoss | Oberkante Rohdecke (geschossbildend) |
| OG01_UKRD | 1. Obergeschoss | Unterkante Rohdecke |
| OG01_OKFF | 1. Obergeschoss | Oberkante Fertigfußbodenlage |
| OG01_OKRD | 1. Obergeschoss | Oberkante Rohdecke (geschossbildend) |
| EG01_UKRD | Erdgeschoss | Unterkante Rohdecke |
| EG01_UKAD | Erdgeschoss | Unterkante abgehängte Decke |
| EG01_OKFF | Erdgeschoss | Oberkante Fertigfußboden |
| EG01_OKRD | Erdgeschoss | Oberkante Rohdecke (geschossbildend) |
| UG01_UKRD | 1. Untergeschoss | Unterkante Rohdecke |
| UG01_OKFF | 1. Untergeschoss | Oberkante Fertigfußboden |
| UG01_OKFU | 1. Untergeschoss | Oberkante Fundament (geschossbildend) |

- Wände sollten möglichst **nicht über Geschosse hinwegreichen**, immer geschossweise unterteilen. Trennlinien in Ansichten über Funktion „Verbinden“ aufheben.
- Vorteil: Betonmenge je Geschoss leicht ermittelbar → Bauzeitplan ableitbar.

#### Versatz entlang der Z-Achse (S.88, Fußnote 87)
- **Niemals den Einfügepunkt OK RD EG0 mit einem Versatz von 3 m wählen** → stattdessen Einfügepunkt direkt ins richtige Geschoss setzen (z. B. **OK RD OG1 ohne Versatz**).

#### Umgang mit uneinheitlichen Geschossen (S.89, Fußnote 88: http://standards.buildingsmart.org/)
- Keine generelle Lösung; oft durch Aufteilung in **Bauabschnitte** lösbar.
- Splitlevels / Hangbauten: Geschossfestlegung schwierig. Z. B. kann die Geschossebene OK RD OG1 die Wände eines hangaufwärts gelegenen EG-Halbgeschosses halbieren (untere Hälfte → EG, obere → OG1).
- Mögliche Strategie: Unterteilung in **zwei Modelle** (Modell über Basisgeschoss + Modell für Zwischengeschosse), bei Bedarf in eine Koordinationsdatei einspielen.

#### Verortung im Infrastrukturbereich (S.90)
- Im Infrastrukturbereich sind die Dimensionen meist deutlich größer als im Hochbau; meist kein kartesisches Koordinatensystem rund um einen Projektbasispunkt, sondern Bezug auf **Gauß-Krüger-Koordinatensystem** / GIS-Welt.
- Verortung nach Geschossen ergibt keinen Sinn → eher **linien- oder oberflächenbasiert**, im **IFC 2x3 noch nicht vorgesehen**.
- Infrastruktur zu Beginn der BIM-Entwicklung vernachlässigt; erst mit **IFC4** schrittweise erste Standards.
  - **IFC4.1** und **IFC4.2** ermöglichen Infrastrukturprojekte.
  - Mit **IFC4.1** wurden **Terrassierung** und **Alignement** eingeführt.
  - „Richtig rund“ erst mit **IFC4.3** oder **IFC5** → eigene Erweiterungen für **IFC-Road, IFC-Rail, IFC-Bridge, IFC-Tunnel**.
- Abbildung 22 (S.91, Fußnote 89: Eichler, C.C. et al., BIMcert Handbuch S.69): Ausblick Neustrukturierung des **IfcSpatialStructureElement** in IFC4.3.

### Bezüge (S.92–93)
- Beim Modellieren wird jedes Objekt bewusst/kontrolliert einer bestimmten Position zugewiesen — nicht zwingend absolut, oft relativ zu übergeordneten Objekten/Linien/Flächen.
- Typische Bezüge: **Rasterlinien, Ebenen, Grundstücksgrenzen**; im weitesten Sinn auch ein anderes Objekt (Geschossdecke, Wand).
- Einzufügendes Objekt: Einfügepunkt bzw. Einfügelinie (= Referenz-/Basislinie) am Bezug fixieren.
- Bezüge nur innerhalb des eigenen Modells und zu anderen verknüpften Fachmodellen erstellen.
- **Statik**: bevorzugt die **Mittelachse** (Lastabtragung); bei Querschnittsänderung beidseitig gleich → Lastabtragungsachse bleibt mittig. Bei sich verschlankenden Außenwänden liegen Mittelachsen nicht mehr übereinander (Wandstärken nach innen aufgetragen, Fassade bleibt eben).
- **Architektur**: baut z. B. genau an der Grundstücksgrenze → Einfügeachse der Wand am Rand, exakt auf Grenzlinie fixiert; bei Wandstärken-Änderung variiert sie ins Grundstück hinein, Gebäude bleibt an der Grenze.
- **Haustechnik**: meist **UK RD oder abgehängte Decke** als Bezugsebene.

### Modelliertechniken (S.93–95)

#### Abstand zu Bezügen / Haustechnik (S.93)
- Entscheidend ist der **Abstand der Kanäle/Leitungen** zu den Bezügen.
- In der haustechnischen Planung wird mit zentraler Entwurfslinie begonnen; manche Software setzt nur die **Mittelachse** des Objekts in Bezug → bei Dimensionsvergrößerung Kollisionsgefahr (Oberkante reicht in die Decke). Haustechnik muss die **halbe Kanal-/Rohrdimension addieren**.

#### Objekt als Bezug (S.93)
- Auch ein BIM-Objekt kann Bezug für ein anderes sein: Jede **Tür / jedes Fenster** wird in Bezug auf eine **Wand** positioniert.
- Datentechnisch: Klasse Wand steht in **Kompositionsbeziehung** zur Klasse Fenster; Fenster hat Einfügepunkt in der Wand. Wird die Wand verschoben, verschiebt sich das Fenster mit (bleibt innerhalb der Wand an gleicher Position). Gleiches Prinzip: Dachgaube auf dem Dach.

#### Raster (S.93–94, Verweis Kapitel 4 S.182)
- Raster bieten optimale Bezüge → wären idealerweise von Beginn an im Modell.
- In der Praxis wird das Raster erst später festgelegt und nachgepflegt → nicht alle Objekte haben einen Rasterbezug (Gefahr, sie bei Bezugsänderungen zu vergessen).
- Nach Festlegung: **Rasterlinien dürfen — wie Projektbasispunkt und Nordung — im Projektverlauf nicht mehr geändert werden.** Weitere Rasterlinien können bei Bedarf ergänzt werden.
- Zitat (S.93, Fußnote 90: Eichler, C.C. et al., BIMcert Handbuch S.115): *„Wir modellieren so, wie gebaut wird.“* — DI (FH) Christoph C. Eichler.

#### Dynamisches Modellieren (S.94)
- BIM bietet (anders als CAD) **dynamisches Modellieren** auf Basis von Bezügen → Modell horizontal/vertikal wie eine **Ziehharmonika** zusammen-/auseinanderschieben.
- Bei sauberer/intelligenter Anlage: Änderung eines Bezugs passt mit einem Klick alle daran orientierten Objekte an.
- Vertikale Bezüge über Modellierebenen, horizontale z. B. über das Raster.
- Beispiel: Ändert sich die Geschossdecken-Stärke → durch Verschieben der Modellierebene UK RD werden alle Wände/Ausbauelemente automatisch angepasst, **vorausgesetzt** die obere Abhängigkeit der Wände wurde an UK RD geknüpft.
- Dynamisches Modellieren beruht auf **Parametern** (spezielle Ausprägung von Attributen). Hohe Kunst beim Entwerfen: intelligenter/variabler Algorithmus (**generatives Design**), der mehrere Entwurfsoptionen offenhält; Vergleich über Simulationssoftware.

#### Modellierregeln / Modellierleitfaden (S.94–95, Fußnote 91: ÖNORM A 6241-2 S.12)
- Unterschiedliche Modelliermethoden → divergierende Fachmodelle → Probleme beim Zusammensetzen. Modellierleitfaden sichert praxisnahe, durchgängig nutzbare Modelle.
- Leitfäden von Softwareherstellern enthalten deren BIM-Strategie → kritisch prüfen.
- In **Österreich zuerst an Anhang A (Modellierleitfaden) der ÖNORM A 6241-2:2015** halten.
- „Eierlegende Wollmilchsau“ (universeller Leitfaden für alle) gibt es nicht; nicht 1:1 von Projekt zu Projekt übertragbar — auf Projekt/Bauherrn anpassen; kann Bestandteil der **Verträge (AIA)** zur Vergabe einer Planungsleistung sein.

#### Arbeiten mit Platzhaltern (S.95)
- Am Projektanfang sind Objektinformationen dürftig. Statt eine falsche Tür → ein allgemeines Türobjekt einsetzen.
- Im Entwurfsstadium: Objekt **„Tür allgemein“**; in der Ausführungsplanung Platzhalter ersetzen, z. B. alle Türen mit L-Zarge auswählen und durch **„Tür Metallzarge“** ersetzen.

### Detaillierungsgrad / LOD (S.96–101)

#### Fortschreitende Detaillierung (S.96)
- BIM-Objekt verfügt zu Planungsbeginn noch nicht über alle Informationen; Informationstiefe vervollständigt sich Schritt für Schritt über die Projektphasen.
- Festgehalten in **AIA (Auftraggeber-Informationsanforderungen)** und **BAP (BIM-Ausführungsplan)**.
- Beispiel **mataTGA der TU Graz**: für unzählige TGA-Komponenten auf Basis der IFC-Struktur Attribute erhoben und Leistungsphasen zugeordnet; **LOI-Definitionen als Excel-Tabellen**, Anwendungsprozess als **BPMN-Modell**, passende **Solibri Prüfregeln**. http://www.metatga.org/ergebnisse/

#### LOD – Level of Development (S.96–97)
- In BIM wird immer im **Maßstab 1:1** gearbeitet → eigener Kriterienkatalog für Detaillierungsgrad nötig.
- Detaillierungsgrad von BIM-Objekten über **LOD** gesteuert; ein LOD-Katalog ist nicht für jedes Projekt gleichermaßen geeignet.
- In den AIA einigen, welcher LOD von wem in welcher Phase gefordert wird; über BAP nachjustieren.
- Bauwerkselemente kennzeichnen sich primär durch **Geometrie** und **Attribute** → **LoG (Level of Geometry)** und **LoI (Level of Information)** sind die zwei Urbestandteile des LOD; zusätzlich **LoC (Level of Coordination)**.
- **Formel (S.97):** `LOD = LoG (Level of Geometry) + LoI (Level of Information) + LoC (Level of Coordination)`
- Bei Modellen spricht man streng genommen nicht vom LOD, sondern vom **Reifegrad** (hier bezogen auf BIM-Objekte). Verweise: Kapitel 5 S.234; AIA/BAP.

#### LoX / Begriffsabgrenzung (S.97, Fußnote 92: https://www.bimpedia.eu/)
- Viele Begriffe: LOD, LoD, LoI, LoG, LoC, LoL, LOIN …
- **LOD** = Oberbegriff (Level of Development); **LoD** = Detaillierungsgrad der Geometrie (Level of Detail). Großes/kleines „o“ ist bedeutsam.
- Häufige Falschverwendung von LOD als „Level of Detail“ oder „Level of Definition“.
- In Österreich: Plattform 4.0 (mit ÖIAV, ÖBV, TU Wien) → Broschüre **„Begriffe zu BIM und Digitalisierung“**. Buch orientiert sich daran, verwendet aber statt **LoD** synonym **LoG (Level of Geometry)** (geringere Verwechslungsgefahr).

#### LOD 100–500 (350) (S.98–99)
- LOD-Katalog ursprünglich vom **American Institute of Architects (2008)**, laufend aktualisiert; aktuelle Spezifizierung auf **BIMFORUM.ORG** (https://bimforum.org/lod/).
- Gemäß BIM-Forum: **6 Levels von 100 bis 500**.
- **Level 350**: beschreibt nur Level 300 nach Abstimmung der Fachmodelle → betrifft nur den **LoC**; LoG und LoI ident mit Level 300.
- Im **LOD 400** ist der LoG meist **detaillierter als im LOD 500**, weil im LOD 500 die Geometrie nur noch **„as built“** abgebildet wird (z. B. Laserscan), während im LOD 400 Wände mit Bewehrung und Schalung dargestellt sind.

**Tabelle 3 (S.98): LOD 100–500 (350)**
| LOD | Bedeutung |
|-----|-----------|
| LOD 100 | Konzeptionelle Darstellung |
| LOD 200 | Dimensionen und Größe maßgeblicher Bauteile |
| LOD 300 | Ausschreibungsreife Angaben mit Spezifikation |
| LOD 350 | 300 mit anderen Teilmodellen koordiniert |
| LOD 400 | Fabrikationsreife Ausführungsplanung |
| LOD 500 | As-built-Dokumentation der ausgeführten Elemente |

- Modelliersoftware-Stufen stimmen nicht mit LOD-Levels überein. Beispiel **Revit**: für Objekte (Familien) nur drei Darstellungsstufen **grob, mittel, fein**.

#### LoG – Level of Geometry (S.99–100, Fußnote 93: Swiss BIM LOIN-Definition (LOD) 07/2018 S.25)
- LoG = Detaillierungsgrad der geometrischen Körper.
- Zwei Gründe gegen 100 % detailgetreue Modellierung: (1) **Zeit/Kosten** (volle 3D-Detaillierung wird i. d. R. nie vergütet); (2) **Rechnerleistung** (jede Ecke/Kante/Fläche kostet Performance).
- Beispiel **Pumpe (TGA)**: zu Anfang abstrakter Quader (+ evtl. zweiter Quader für Montage-/Wartungsbereich); **ab Level 300** genaue Positionen der Anschlusspunkte, Anschlussdimensionen als **Attribute**. Niemals Verschraubungen, Krümmungen, einzelne Schalter in 3D modellieren.
- Entscheidung: was als 3D-Objekt, was als 2D-Detail/Attributbeschreibung. Modellierphilosophien weichen stark ab (Beispiel Attika).
- Zitat (S.100): *„Wir modellieren so viel wie nötig, so wenig wie möglich.“* — Markus Hiermer.

#### LoI – Level of Information (S.100–101)
- LoI legt fest, welche **alphanumerischen Attribute** für die Bauteile zu welchem Zeitpunkt und in welcher Tiefe benötigt werden.
- Vorteil, wenn schon bekannt ist, welche Auswertungen später gefordert sind.
- Für Wartung/Betrieb kommen nach Fertigstellung weitere Attribute hinzu → manche sprechen von **LOD 600**.
- Teilmodell nicht mit allen Daten überfrachten; nur den jeweils benötigten Datensatz speichern. Sinnvoll: eigenes Modell nur mit betriebsnötigen Daten übergeben.

#### LoC – Level of Coordination (S.101)
- Zu vereinbarten Zeitpunkten werden Fachmodelle überlagert und auf **Kollisionen** geprüft (vor BIM nicht automatisiert möglich → Kostenersparnis).
- LoC umfasst nicht nur klassische Bauteil-Kollisionen, sondern auch Kollisionen mit **Wartungs-/Montagebereichen** sowie die Prüfung der **Barrierefreiheit**.

### Objektbibliotheken (S.102–106)

#### Software-Bibliotheken / Bürostandard (S.102–103)
- Mit der Modelliersoftware kommt eine erste landesspezifische Objekt-Bibliothek + erstes Klassifizierungssystem; reicht schnell nicht aus → eigener Bürostandard nötig.

**Tabelle 4 (S.102): Bezeichnung von BIM-Objekten je Software**
| Software | Bezeichnung |
|----------|-------------|
| Allplan | Smart Objects |
| Archicad | GDL-Objekte |
| Revit | Familien |

- Detaillierungsgrad für alle Objekte nach gleichen Kriterien; gleiche Objekttypen → gleiche Parameter (Attribute); mehrfach vorkommende Parameter eindeutig definieren und in **projektspezifischen Parameterlisten** festhalten. Beispiel: Parameter „Breite“ präzisieren als „Wandstärke“, „Rohbaulichte“, „Rahmenstärke“. **In jedem Projekt eine Parameterliste.**
- Empfehlung: **„BIM-Bibliothekar:in“** im Büro, der/die neue Objekte einpflegt, adaptiert, Standards wartet und Daten strukturiert am Server ablegt.

#### Praxistipp: IP / Datenweitergabe (S.103, https://de.graitec.com/powerpack-for-revit/)
- Kopieren proprietärer Objekte ist möglich, aber müssen erst an Büro-/Projektstandard angepasst werden (hoher Aufwand).
- Eigentlicher Wert liegt nicht in einzelnen Objekten, sondern in jahrelanger Abstimmung und Umgangswissen → open-source-Gedanke erwägen.
- Wer Kopieren ausschließen will: Daten nur in allgemeinen Austauschformaten wie **IFC** weitergeben.
- **Wasserzeichen**: Software-Plugins schreiben Wasserzeichen in proprietäre Dateien; Schutz erschwert Plagiat nur (Sourcecode bereinigbar, Nachzeichnen schneller als bei null beginnen).

#### Nomenklatur (S.104)
- Aus verschiedenen Bibliotheken: gleiches Objekt heißt „Fenster“, „window“, „Festverglasung“ → innerhalb eines Projektes muss die Bezeichnung **immer eindeutig** sein (gilt auch für Parameternamen). **Parameterliste je Projekt unumgänglich.**
- Bei Zusammenarbeit treffen verschiedene Bürostandards aufeinander → idealerweise gemeinsamer Standard, sonst Bürovorlagen aufeinander abstimmen + per kleinem Testlauf prüfen.

#### Allgemeine Bibliotheken (S.104)
- Objekte aus Bibliotheken machen oft mehr Arbeit als Selbermodellieren (Kompatibilität zum Bürostandard: Nomenklatur, Parameter, LOD-Umgang anpassen).
- **Lokalisierung**-Gefahr bei standardisierten Bauteilen mit länderspezifischen Standardmaßen.
  - Beispiel **Stahlzargentür**: Deutschland-Objektdatei bietet Typ mit **885 mm Breite**, in **Österreich** sollte dieser Typ **800 mm Breite** haben.

#### Herstellerbibliotheken (S.105)
- Schon zu CAD-Zeiten platzierten Hersteller produktspezifische **dxf-/dwg-Dateien** früh in Projekten (schwer ersetzbar). Gleiches Spiel bei BIM-Objekten.
- Bei **öffentlichen Ausschreibungen** problematisch: geforderte **Produktneutralität** evtl. nicht mehr gegeben → im Extremfall Ausschluss.
- Hersteller-Objekte bringen fast immer ein **Performanceproblem** (Geometrie viel zu groß detailliert; schlimmstenfalls 3D-Gravur von Logo/Name → No-Go). Vor Verwendung Geometrie kräftig säubern.

### Literaturverzeichnis (Kapitel „Richtig Modellieren“, S.106–107)
- Autodesk, Revit IFC Handbuch (2018); http://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcbuilding.htm (Zugriff 10.12.2021)
- Borrmann, André; König, Markus; Koch, Christian; Beetz, Jakob (Hrsg.) (2015): Building Information Modeling. Technologische Grundlagen und industrielle Praxis. Berlin/Heidelberg, Springer-Verlag (ISBN 978-3-658-05605-6)
- buildingSMART, IFC Infra Overall Architecture Project, Documentation and Guidelines (Final 01/03/2017)
- buildingSMART Switzerland, Swiss BIM LOIN-Definition (LOD) Verständigung, 07/2018
- Eichler (2016), BIM-Leitfaden 2, Struktur und Funktion; https://www.bimpedia.eu/artikel/1005-lod-level-of-development (Zugriff 10.12.2021) (ISBN 978-3-937654-99-7)
- Eichler, C. et al., BIMcert Handbuch (2021); http://www.buildingsmart.co.at/wp-content/uploads/2021/07/BIMcert-Handbuch-2021-eBook.pdf (Zugriff 28.3.2022)
- Horner (2021), BIM Reality Check: „Mixed BIM“ – die gelebte Praxis
- Hiermer, Markus, Autodesk Revit, Leitfaden für die BIM Modellierung in Revit, Version 1.0
- ÖNORM A 6241-2:2015. Digitale Bauwerksdokumentation – Teil 2: Building Information Modeling (BIM) – Level 3-iBIM

### Richtiges Modellieren in Infrastrukturprojekten (Lukas Hochreiter, HABAU Group; S.108–117)

#### Informationsanforderungen / Modelldetaillierung (S.108)
- BIM-Modellierung ≠ 3D-Modellierung; BIM-Modell zeichnet sich durch **Informationsgehalt** und **strukturierte Datenhaltung** aus.
- Begriffe: **LOD** (Level of Development), **LOI** (Level of Information), **LOG** (Level of Geometrie), **LOIN** (Level of Information Needed) — definieren Modelldetaillierung je Projektphase/Anwendungsfall.
- Es gibt **noch keinen national oder international gültigen Standard für Modelldetaillierung** → an klassische Projektphasen anlehnen.

**Tabelle 5 (S.108): Modelldetaillierung und LOD**
| Projektphase | Bezug zu LOD | Beschreibung |
|--------------|--------------|--------------|
| Bestand (Grundlage) | vgl. LOD 100 | Altbestand, Grundlage |
| Entwurf | vgl. LOD 200 | Entwurfsmodell |
| Ausschreibung | vgl. LOD 300 | Ausschreibungsmodell |
| Ausführung | vgl. LOD 400 | Ausführungsmodell |
| Bestandsmodell (Übergabe) | vgl. LOD 500 | As-Built-Modell |

#### Modellstrukturierung (S.110–111)
- Aufteilung örtlich und fachlich; Strukturierung in **Teilmodelle** (untergliederbar in **Fachmodelle**). Modellstrukturplan ist projektunabhängig, für alle Gewerke der Infrastruktur erweiterbar.
- **Strukturierungsmöglichkeiten:**
  1. **Dateinamen-Bezeichnungskonvention** — Beispiel: `A02_STR_FL_EP_A400_AN1_V02.ifc`
  2. **IFC-Strukturbaum** — Hierarchie über `ifcSite`, `ifcBuilding`, `ifcBuildingStorey`, `ifcSpace`. **IFC 5** soll eine „overall-architecture“ für alle Bereiche bringen und den Hochbau erweitern.
  3. **Gliederung über Merkmale** — strukturgebende Merkmale zum Filtern/für Auswahlmengen.
- Für gängige BIM-Anwendungsfälle (Bauzeitplanung **4D**, Kostenermittlung **5D**, Dokumentenverlinkung): sowohl örtliche (projektspezifische) Gliederung in **„Locationcodes“ (LOC)** als auch fachliche (projektunabhängige) Gliederung in **„Bauteilcodes“ (BTC)**. In Infrastruktur fachliche Strukturierung zusätzlich im IFC-Strukturbaum aufbauen.

**Tabelle 6 (S.111): Überblick strukturgebende Merkmale — BTC (Bauteilcode) / LOC (Locationcode)**
| BTC – Bauteilcode | LOC – Locationcode |
|-------------------|--------------------|
| 01_Teilmodell | 01_Bauwerksbezeichnung |
| 02_Fachmodell | 02_Abschnitt |
| 03_Gewerk | 03_Zonierung |
| 04_Bauteilgruppe | 04_Hauptgliederungselement |
| 05_Element | 05_Ausrichtung |
| 06_Material | — |

#### Geometrische Anforderungen (S.112)
- BIM-Modelle bestehen primär aus **Volumenkörpern und Flächen** (für Mengen-/Kostenermittlung **5D**).
- Wichtig: Ausführungsmodell aus **demselben CAD-Modell** exportieren wie die 2D-Ausführungspläne → **Planableitung aus dem Modell / Plankonsistenz**.
- In Infrastruktur müssen Modelle **globale Koordinaten entsprechend der Vermessung** aufweisen, damit Teilmodelle im Koordinationsmodell zusammenpassen.

#### Projektbasispunkt und Referenzierung (S.112)
- Georeferenzierung über Definition eines Projektbasispunkts ist Voraussetzung für Prüfungen wie Kollisionskontrolle.
- Lage des Projektnullpunkts **ca. in der Mitte des Projekts** (gleiche Entfernung zu allen Projektgrenzen).
- Wert des Projektnullpunkts auf einen **runden Wert** auf-/abrunden (**runden auf volle 5 oder 10 m**).

**Tabelle 7 (S.112): Definition Projektbasispunkt**
| System | Amtliches Koordinatensystem | Lokales Koordinatensystem |
|--------|------------------------------|----------------------------|
| Rechtswert | 4.555.730 (Beispielwert) | 0,000 |
| Hochwert | 5.848.910 (Beispielwert) | 0,000 |
| Bezugshöhe | 0,000 (müA) | 0,000 |

#### Modellunterteilung (S.113)
- Straßenbauwerk = Linienbauwerk über große Entfernung → Bauteile in **Achsrichtung** unterteilen.
- Neben Bauabschnitten zusätzlich regelmäßige Unterteilung nach **Straßenkilometer in volle Kilometer** („Zonierung“ nach Straßenkilometrierung); Lieferobjekte (IFC) kilometerweise ausgegeben; Abbildung geometrisch + über Locationcode „Zonierung“.

**Tabelle 8 (S.113): Unterteilung des Modells nach Straßenkilometer**
| Unterteilung | Kilometer von | Kilometer bis |
|--------------|---------------|---------------|
| Z01 | Km022+675 | Km023+000 |
| Z02 | Km023+000 | Km024+000 |
| Z03 | Km024+000 | Km025+000 |
| Z04 | Km025+000 | Km026+000 |
| Z05 | Km026+000 | Km027+000 |
| Z06 | Km027+000 | Km028+000 |
| Z07 | Km028+000 | Km028+175 |

#### Geometrische Detaillierung / Tessellierung (S.114–116)
- Elemente innerhalb einer Zone nach **Regelabstand** unterteilen: **5 m-, 10 m-, 15 m- oder 25 m-Stationierung** (in IFC über „Composite-Elemente“).
- Praxis: Stationierung des **Oberbaus in 5 m- bzw. 10 m-Abschnitte**; beim **Erdbau** Stationierung analog zur klassischen Planung von **15 bis 25 m** ausreichend.
- Bauteiltrennung bedeutet nicht, dass Volumenkörper zwischen Stationen nicht genauer detailliert sind. In modernen Straßenplanungssystemen sind Stationierung und Genauigkeit der **„Tessellierung“** (Punkte/Dreiecke, die einen Körper definieren) beim IFC-Export festlegbar → folgen Urgelände/Planung statt bloßer linearer Interpolation zwischen 2 Profilen.
- Bauteile fachlich/geometrisch richtig trennen; Gliederung über Merkmale + IFC-Strukturbaum.
- Im **Einschnittsbereich** Abtrag als „Aushubkörper“/„Erdkörper“ modellieren; „Abtragskörper“ und „Neubau“-Elemente liegen lagemäßig übereinander.
- Geometrische Detaillierung wird z. B. bei der **ASFiNAG** in einem **„BIM-Modellierungsleitfaden“** gewerkspezifisch je Teil-/Fachmodell beschrieben.

### Kapitel 3 — BIM-Software (Marcus Wallner; S.118–119)
- Bei CAD ist die Software eher ein Werkzeug; bei **BIM** geht es um **Eingabe, Verarbeitung und Auswertung** der Daten.
- Daten/Datensätze stecken in **Datenbanken** hinter den Softwareprodukten/Dateien; idealerweise fortschreibend über alle Projektphasen/den gesamten Lebenszyklus.
- **Kapitelinhalt (S.120):** Softwarelandschaft (120), Lebenszyklus (124), Die „Big Player“ (126), Softwareversion (132), Software-Kategorien (134), Modelliersoftware (136), Viewer (140), Prüfsoftware (144), Software für Auswertungen und Simulationen (146), Kollaborationsplattformen (147), Lizenzpolitik (148), Mieten oder kaufen (149), Einzelplatzlizenz oder Netzwerklizenz (153), Literaturverzeichnis (157).

## Maschinen-Regeln

- [HÖHE] Projektbasispunkt im Projekt meist mit 0,00 m angesetzt (S.80)
- [DEFINITION] Normalnull = mittlere Höhe des Meeresspiegels; in Österreich „Meter über Adria“ (S.80)
- [ABSTAND] Höhenunterschied Normalnull Österreich (Adria) ↔ Deutschland (Pegel Amsterdam) ≈ 33 cm (S.82)
- [DEFINITION] Beispiel Höhe Projektbasispunkt über Normalnull = 353 m (S.80)
- [PFLICHT] Nullpunkt und Nordung dürfen im Projektverlauf unter keinen Umständen mehr geändert werden (S.82)
- [PFLICHT] Rasterlinien dürfen nach Festlegung — wie Projektbasispunkt und Nordung — im Projektverlauf nicht mehr geändert werden (S.93–94)
- [PFLICHT] Projektbasispunkt + Winkel zwischen geografischem Norden und Projektnorden unbedingt im BAP festhalten (S.82)
- [DEFINITION] Projektbasispunkt = zentraler dreidimensionaler Nullpunkt / Modellursprung eines BIM-Projekts (S.80)
- [DEFINITION] Georeferenzierung im Koordinatensystem des Landes = Gauß-Krüger-Koordinatensystem (S.80, S.90)
- [PFLICHT] Projektbasispunkt nahe am Bauwerkmodell (weit entfernt → Performanceeinbußen, bei extremen Entfernungen Fehler) (S.81)
- [PFLICHT] Projektbasispunkt günstig links unterhalb des Bauwerks → Bauwerk im positiven XY-Bereich; oft auf Achsenkreuzung A-A / 1-1 (S.81)
- [SYMBOL] Koordinationskörper = Pyramide mit quadratischer Grundfläche; Spitze auf dem Nullpunkt, Grundfläche folgt der Nordung (S.83)
- [DEFINITION] Geschoss = IfcBuildingStorey; je Geschoss nur eine Ebene modellieren (S.84)
- [PFLICHT] Geschossbildende Ebene projektübergreifend = Oberkante Rohdecke (OK RD) (S.85, S.87)
- [DEFINITION] In Revit bildet eine Ebene nur dann eine IfcBuildingStorey, wenn Attribut „Gebäudegeschoss“ angekreuzt ist (S.85)
- [PFLICHT] Modellierebene UK AD (Unterkante abgehängte Decke) im Teilmodell des Haustechnikers anlegen (S.85)
- [PFLICHT] Wände nicht über Geschosse hinwegreichen lassen → geschossweise unterteilen (S.87)
- [PFLICHT] Einfügepunkt direkt ins richtige Geschoss setzen, nie mit Versatz (kein OK RD EG0 + 3 m Versatz, sondern OK RD OG1 ohne Versatz) (S.88)
- [DEFINITION] Geschoss-/Ebenen-Benennung (Tabelle 2): z. B. OG01_OKRD, OG01_OKFF, OG01_UKRD, EG01_UKAD, UG01_OKFU (S.87)
- [DEFINITION] IFC4.1 führte Terrassierung und Alignement ein; IFC4.1/4.2 ermöglichen Infrastruktur; IFC4.3/IFC5 → IFC-Road/Rail/Bridge/Tunnel (S.90)
- [DEFINITION] Infrastruktur-Verortung linien-/oberflächenbasiert, in IFC 2x3 noch nicht vorgesehen (S.90)
- [DEFINITION] Statik-Bezug = Mittelachse (Lastabtragung); Architektur-Bezug = Grundstücksgrenze/Wandrand; Haustechnik-Bezug = UK RD oder abgehängte Decke (S.92)
- [ABSTAND] Haustechnik: halbe Kanal-/Rohrdimension zur Mittelachse addieren, um Kollision mit der Decke zu vermeiden (S.93)
- [DEFINITION] LOD = LoG (Level of Geometry) + LoI (Level of Information) + LoC (Level of Coordination) (S.97)
- [DEFINITION] LOD-Stufen: 100 Konzept, 200 Dimensionen maßgeblicher Bauteile, 300 ausschreibungsreif mit Spezifikation, 350 = 300 koordiniert, 400 fabrikationsreife Ausführungsplanung, 500 As-built (S.98)
- [DEFINITION] LOD 350 betrifft nur LoC; LoG/LoI ident mit LOD 300 (S.98)
- [DEFINITION] LOD 400 LoG meist detaillierter als LOD 500 (500 = as built, z. B. Laserscan) (S.98)
- [DEFINITION] Mögliches LOD 600 für nachträgliche Betriebs-/Wartungsattribute (S.100–101)
- [DEFINITION] LoC umfasst Bauteil-Kollisionen + Wartungs-/Montagebereich-Kollisionen + Barrierefreiheitsprüfung (S.101)
- [DEFINITION] Revit-Objektdarstellung nur drei Stufen: grob, mittel, fein (S.99)
- [DEFINITION] BIM-Objektbezeichnungen je Software: Allplan = Smart Objects, Archicad = GDL-Objekte, Revit = Familien (S.102)
- [ABSTAND] Stahlzargentür Standardbreite: Deutschland 885 mm, Österreich 800 mm (S.104)
- [PFLICHT] In jedem Projekt eine Parameterliste; Objekt-/Parameternamen müssen projektweit eindeutig sein (S.102, S.104)
- [PFLICHT] Bei öffentlichen Ausschreibungen Produktneutralität wahren → Herstellerobjekte können sonst zum Ausschluss führen (S.105)
- [FRIST] American Institute of Architects definierte LOD-Katalog erstmals 2008 (S.98)
- [ABSTAND] Infrastruktur-Projektnullpunkt auf vollen 5 oder 10 m runden, ca. in der Mitte des Projekts (S.112)
- [ABSTAND] Stationierung Oberbau 5 m bzw. 10 m, Erdbau 15–25 m; Regelabstände 5/10/15/25 m (S.114–116)
- [DEFINITION] Infrastruktur-Strukturmerkmale: Bauteilcode BTC (Teilmodell/Fachmodell/Gewerk/Bauteilgruppe/Element/Material) + Locationcode LOC (Bauwerksbezeichnung/Abschnitt/Zonierung/Hauptgliederungselement/Ausrichtung) (S.111)
- [DEFINITION] IFC-Strukturbaum-Hierarchie: ifcSite > ifcBuilding > ifcBuildingStorey > ifcSpace; IFC5 = overall-architecture (S.111)
- [PFLICHT] Ausführungsmodell aus demselben CAD-Modell wie 2D-Ausführungspläne exportieren (Plankonsistenz) (S.112)
- [DEFINITION] Zonierung nach Straßenkilometer in volle Kilometer (Tabelle 8, z. B. Z01 Km022+675–Km023+000) (S.113)
- [PFLICHT] In Österreich Modellierleitfaden: Anhang A der ÖNORM A 6241-2:2015 (S.95)
- [DEFINITION] ÖNORM A 6241-2:2015 = Digitale Bauwerksdokumentation Teil 2: BIM – Level 3-iBIM (S.107)
