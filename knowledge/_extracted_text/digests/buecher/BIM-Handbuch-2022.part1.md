# BIM-Handbuch-2022 — Teil 1
> Quelle: BIM-Handbuch-2022 (buecher) · dieser Teil. Abdeckung: S. 40–79 (PDF-Seiten 41/348 bis 80/348). Inhalt: Grundlagen-Kapitel (BIM-Definition, Einsatzformen, das „I" in BIM, Forderung/Rechtslage, Standards/Normen, Vorteile, BIM einführen, IFC-basierter BIM-Standard Österreich) sowie Beginn Kapitel 2 „Richtig Modellieren".

## Inhalt

### Was ist BIM? Einsatzformen (S. 40–43, PAGE 41–44)
- **BIM-Definitionen (Zitate):**
  - „BIM ist eine über alle Planungs-, Bau- und Lifecycle-Prozesse übergreifende Managementmethode zur digitalen Transformation des zukünftigen Gebäudebestandes."
  - „BIM ist ein Managementprozess zur digitalen Transformation der Planungs- und Bauwirtschaft." (Arch. DI Heinz Plöderl)
  - „Es muss nicht immer ‚big fat BIM' – BIM über alle Leistungsphasen – sein, auch aus einzelnen BIM-Teilmodellen können bereits wertvolle Benefits gezogen werden." (Arch. DI Christine Horner)
- **Vier Einsatzformen (zwei Begriffspaare):**
  - **little BIM:** Anwender:innen arbeiten in *ihrer* Fachdisziplin mit *ihrer* Software.
  - **big BIM:** Mehrere Anwender:innen *unterschiedlicher* Fachdisziplinen arbeiten in ihrer Software.
  - **closedBIM:** herstellerspezifische Formate bzw. eine bestimmte technologische Plattform (BIM-Software / Softwarefamilie).
  - **openBIM:** unterschiedliche Softwareprodukte; Austausch/Integration über *offene Schnittstellen bzw. neutrale Austauschformate*.
  - Einsatzformen lassen sich **nicht 1:1 den Leveln zuordnen** — fließende Übergänge je nach Projekt/Konstellation (Abbildung 1).
  - Empfehlung für Einsteiger:innen: erste „Gehversuche" in **little closedBIM**, später Richtung „open" und „big" weiterentwickeln.
- **ÖBB BIM-Reifegradwürfel (Abbildung 2):** drei Dimensionen — Funktionalität/Umfang (Little/Big), Standardisierung (open/closed), Prozessphasen (Planen/Bauen/Betreiben).
  - Präferenz **big openBIM** bei Infrastrukturbetreibern: Managen von Informationen über gesamten Lebenszyklus.
  - **Lesbarkeitsanforderung: Daten müssen auch nach mehr als 80 Jahren noch lesbar und verarbeitbar sein** → herstellereigene Dateiformate erfüllen das meist nicht → offenes, standardisiertes Format (openBIM) unerlässlich.
  - **ASFINAG, ÖBB-Infrastruktur AG und Bundesimmobiliengesellschaft m.b.H. (BIG) setzen auf openBIM.**

### Stimmen zu openBIM (S. 42–44, PAGE 44–45)
- Ing. Sabine Hruschka (ASFINAG): Open BIM = Bereitstellung von Daten unabhängig vom Softwareprodukt; flexible Reaktion auf technische Neuentwicklungen.
- BIG: BIM nur erfolgreich, wenn keine „Einschränkungen" — muss in openBIM gedacht/gelebt werden.
- BR h.c. DI Klaus Thürriedl: Einsatz für offenen, leistbaren BIM-Zugang (national + EU); freie Softwarewahl; openBIM fördert Netzwerkgedanken.
- Arch. DI Michael Strobl / Arch. DI Thomas Hoppe: openBIM = transparenter, kooperativer Planungsprozess; warnt vor industriegesteuertem Produkt mit teuren Softwareabhängigkeiten.

### Das „I" in BIM — Information (S. 45–46, PAGE 46–47)
- Das „I" steht **nicht** nur für 3D-geometrische Information, sondern für *alle* klassifizierten, zugeordneten, strukturierten Informationen, die in Datenbanken ablegbar sind.
- Unterschied zu „flacher" CAD-Planung: BIM-Daten besitzen **parametrische Faktoren / auslesbare Attribute** über die Geometrie hinaus.
  - In 2D: Wand = Linien + Flächen; Elemente „wissen" nicht, dass sie gemeinsam eine Wand bilden — weder **U-Wert**, **Feuerwiderstandsklasse** noch **Schallschutz** sind digital verknüpft.
- **Bedingung:** Fachwissen muss vorhanden sein, um Werte einem Element zuzuordnen; Eintrag nur durch im jeweiligen Fachbereich qualifiziertes Personal. Falsche/mangelhafte Information wird durch bloße BIM-Anwendung *nicht* aufgewertet.
- Vorteil: automatisierte Prüfroutinen deklarieren unschlüssige Daten.
- Daten sind beim BIM **parametrisch, dynamisch, attribuiert und strukturiert**; Ablage in zentraler Datenbank = **Common Data Environment (CDE)** (Fußnote 59) → jederzeitiger Abruf der aktuellen Planung.

### Wird BIM schon gefordert? (S. 47–48, PAGE 48–49)
- Frühe Treiber: US-Institutionen, z.B. **General Services Administration (GSA)**.
- **Großbritannien: 2016 verpflichtende Anwendung eingeführt** → großer Schub.
- Einige EU-Regierungen folgten, BIM zumindest für öffentliche Projekte verpflichtend.
- **Österreich: derzeit (noch) keine gesetzliche Verpflichtung**, aber bei öffentlichen/halböffentlichen Projekten meist gefordert oder bessere Reihung im Vergabeverfahren; Basis-Know-how bei Mitarbeiter:innenprofilen zunehmend nachzuweisen.
- Rechtsgrundlage: **RL 2014/24/EU des Europäischen Parlaments und des Rates vom 26. Februar 2014** (Vergabe-Richtlinie), Abs. 1 zit. (Grundsätze: freier Warenverkehr, Niederlassungs-/Dienstleistungsfreiheit, Gleichbehandlung, Nichtdiskriminierung, gegenseitige Anerkennung, Verhältnismäßigkeit, Transparenz).

### Rechtstipp — BIM & öffentliche Auftraggeber/Vergaberecht (S. 48, PAGE 49)
- Frage: Zulässigkeit von BIM bei öffentlichen Ausschreibungen nach **BVergG 2018**.
- **Art. 2 Abs. 4 Vergabe-RL 2014/24/EU:** Nutzung spezifischer elektronischer Instrumente ist für öffentliche Bauaufträge/Wettbewerbe in EU-Mitgliedsstaaten (inkl. Österreich) *zulässigerweise zwingend vorschreibbar* → Vorschreibung von BIM steht europarechtlich offen.
- Fehlende BIM-spezifische vergaberechtliche Grundlagen in Österreich = (noch) Hemmschuh bei öffentlichen Infrastrukturprojekten. Bundesregierung: öffentlichen Auftraggebern steht frei, BIM vorzusehen.
- Quellen (Fußnoten): Abs. 2 RL 2014/24/EU (öffentliche Auftragsvergabe als marktwirtschaftliches Instrument, KMU-Teilnahme); Neuhauser, RdU-UT 2020/16, S. 77; parlamentarische Anfrage 2049/AB 27. GP. Autoren: Dr. Georg Seebacher und Mag. Lukas Andrieu, LL.M. (Columbia), BSc.

### Welche Standards gibt es bereits? (S. 49–51, PAGE 50–52)
- Standards = Kern für Gelingen eines BIM-Projekts (Kollaboration). Elemente müssen exakt so ankommen wie exportiert: gleiche Kategorie, gleiche Eigenschaften, gleiche Menge, gleicher Entwicklungsstand.
- **Vier Ebenen der Standardisierung (Abbildung 4):** Software → Modell → Methode → übergeordnetes BIM-Management (regelt Organisation + Schnittstellen).
- Offene Standards = Grundlage für **produktneutrale Ausschreibungen**.
- **buildingSMART:** unabhängiger internationaler Verein, weltweiter Entwickler von openBIM-Standards. Standards sollen zur Norm erhoben werden (Rechtssicherheit) → wurden zu **ISO-Normen**.
  - **ISO 16739:2013 bzw. ISO 16739-1:2018** = Standard für **Industry Foundation Classes (IFC)** (Fußnote 62).
  - IFC = buildingSMART-Datenmodell, allgemeines Datenschema für Informationsaustausch zwischen proprietären Software-Anwendungen; primäres Datenmodell für Bauwerksmodelle.
- **Österreich — freeBIM:** Forschungsgruppe Universität Innsbruck + **Austrian Standards International (ASI)** → Merkmalserver entwickelt (Fußnote 63: freebim.at, Zugriff 21.10.2021).
- **Klassifizierungsmodell des ASI-Merkmalservers = Grundlage für nationale BIM-Norm ÖNORM A 6241-2.** Weiterentwicklung des ASI-Merkmalservers könnte erneut Normvorlage werden.
- Abbildung 5: Übersicht wichtigster internationaler/nationaler Normen + Richtlinien für BIM.

### (Erwartete) Vorteile durch den Einsatz von BIM (S. 52–61, PAGE 53–62)
- Umstellung = kompletter Methodenwechsel, anfangs spürbarer Aufwand; step-by-step Implementierung → **Quick-Wins** schon mit ersten kleinen Änderungen.
- **Exemplarische Vorteile (ohne Reihung):** besseres Projektverständnis (Massen-/Visualisierungsmodelle „nebenbei"); detailliertere Entscheidungsgrundlage; Teilautomatisierung von Prozessen; weniger Fehler/Versäumnisse (geometrische Fehler augenscheinlicher als in 2D); verbesserte Zusammenarbeit Bauherr/Planende; Imagesteigerung; weniger Nacharbeiten; Steigerung der Datenqualität; Vermeidung von Mehrfachangaben; bessere Kostenkontrolle/-sicherheit; Vermarktung neuer Geschäftsmodelle; Angebot neuer Leistungen; Sicherung von Folgeaufträgen.

#### Fehlervermeidung (S. 54, PAGE 55)
- BIM-Ansichten/Listen basieren immer auf aktuellem 3D-Modell → keine widersprüchlichen Angaben zwischen Plänen. Bereits beim Umstieg auf 3D ein „schneller Gewinn".
- Nachvollziehbarkeit von Änderungen bleibt Problem (wie in 2D) ohne Markierung.
- **Prüfsoftware/Prüfregeln — Beispiele:**
  - Fenster/Türen: ob sie 90° aufschlagen können bzw. ob eine Stütze vor dem Fenster steht.
  - Ob **Feuerwiderstandsklasse einer Tür mit der ihrer Wand übereinstimmt**.
  - Ob **Brüstungen die geforderte Absturzhöhe erfüllen**.
  - Ob Elemente doppelt übereinanderliegen.
  - Prüfroutinen müssen projekt-/fragestellungsspezifisch angepasst werden, inkl. aktueller orts- und normentechnischer Ansprüche.

#### Kollaboration (S. 55–56, PAGE 56–57)
- Fachplaner:innen-Bedürfnisse früh berücksichtigen → frühzeitige Kollisionserkennung.
- Gleichzeitiges Arbeiten am zentralen Fachmodell; **Gesamtmodell = Koordinationsmodell**.
- **BCF (BIM Collaboration Format):** regelt Kommunikation bei Mängelabarbeitung; **Point of View** (Blickwinkel im Modell) + Screenshots; **Issue-Management** dokumentiert Zuständigkeit/Nachvollziehbarkeit.

#### Visualisierung (S. 55–56, PAGE 57)
- Aktueller Planungsstand jederzeit visualisierbar; Bauherr/Nutzer:innen besser eingebunden (Bsp. Gastronomie-Pächter optimiert Raumaufteilung; **Wiener Hauptbahnhof: Testpersonen mit VR-Brillen** zur Prüfung der Beschilderung/Wegfindung).
- Fachmodelle werden stetig ausgetauscht/überlagert → Problemzonen, kritische Knoten, Konflikte frühzeitig erkennbar.

#### Kollisionskontrolle (S. 56–57, PAGE 57–58)
- Automatisierte Prüfung überlagerter Fachmodelle (Bsp. Lüftungskanal schneidet tragenden Unterzug → erkannt + gemeldet). Konfliktlisten zielgerichtet abarbeiten; Mensch beurteilt mit Fachwissen (Falschmeldungen filtern). Konfliktzahl sollte mit Projektfortschritt sinken.

#### Verfügbarkeit (S. 57, PAGE 58)
- Informationen jederzeit/überall verfügbar (Echtzeit, vom Büro aus); ortsunabhängiges Planen.
- **Rollen- und Berechtigungssystem:** regelt Zugriff bzw. Lese-/Schreibrechte.
- **SOLL-IST-Vergleiche direkt auf der Baustelle** via Tablet (Position/Perspektive im 3D-Modell vs. Gebautes). Voraussetzung: leistungsfähiges WLAN auf Baustelle (Fußnote 67).

#### Arbeits- und Zeitersparnisse (S. 57–58, PAGE 58–59)
- Saubere Modellierung früher Phasen zahlt sich bei Änderungen aus.
- **Geschossübergreifende Bauteile** (Treppen, Rampen, Geländer, Schächte) brauchen erhöhte Aufmerksamkeit: Änderung der z-Koordinate (z.B. zusätzliche Stufe) kann x-/y-Koordinaten beeinflussen → Konsequenzen: Verschiebung von Wänden, **verringerte Fluchtwegsbreiten**, **Unterschreitung erforderlicher Abstände**.
- **Dynamische Modellierung:** Wand-Oberkanten an Geschossdecke geknüpft → ändern sich automatisch mit.
- **Grafische Überschreibung:** aus Grundriss schnell zugehöriger **Brandschutzplan**; Grundriss-Änderung fließt automatisch ein.
- Kategorien bilden → Massenänderung mit einem Befehl; z.B. alle Steckdosen rot einfärben für Bauherrenbesprechung.
- Architekturmodell-Update → Haustechnikmodell anpassen; Architekturmodell-Nachführung entfällt für Fachplanung Haustechnik.
- Ziel (noch nicht durchgängig): Datenübergabe von Phase zu Phase über gesamten Lebenszyklus (auch für spätere Sanierungen/Umbauten).

#### Auswertungen und Simulationen (S. 58–59, PAGE 59–60)
- Teilautomatisierte Auswertungen mit Echtzeitqualität; **Mengenauswertungen** = wichtigste/häufigste. Korrekte Modellierung kritisch (Decken/Wände-Übergänge, Durchbrüche, Öffnungen) — sonst Fehlzählung.
- **Simulation** = rechnerisches Nachahmen realer/geplanter Situationen mit computerbasiertem Rechenmodell.
  - Bsp.: **Windsimulation** (Formoptimierung schlanker hoher Bauwerke); **Beleuchtungssimulation** (genug Einbauleuchten planen); **Fluchtwegsituation** für öffentliche Gebäude (Stadien, Veranstaltungsräume) via Simulation + Sensitivitätsanalysen.
  - Länderspezifische Unterschiede müssen abgebildet werden. Grundsatz: **„garbage in = garbage out"**.

#### Kosten (S. 59–60, PAGE 61)
- BIM-Potenzial: Fehler reduzieren, Ausführungsvarianten untersuchen, Ausschreibung/Abrechnung erleichtern, Unsicherheiten bei Mengen/Qualitäten reduzieren.
- Mittel-/langfristig verlässlichere **Kostenschätzung, Kostenberechnung, Kostenanschlag**.
- Wirtschaftliche Gesamtvorteile (Sundermeier et al.): bei standardisierbaren Bauvorhaben (Fertighäuser, Einzelhandel Lebensmittel-/Fachmarktsegment, Produktions-/Logistikobjekte, Bürobauten) + komplexen Großprojekten → **Skaleneffekte + Verbundeffekte** (Abbildung 6).

#### Transparenz (S. 60, PAGE 62)
- BIM definiert klar: **wer, was, wann, in welcher Qualität** liefert; klare Schnittstellen; gemeinsame Plattform mit dokumentierten Vorgängen; Projektfortschritt via Auswertungen/Berichte abrufbar; Versionsvergleich.
- Festlegung über **Auftraggeberinformationsanforderungen (AIA)** und **BIM-Abwicklungsplan (BAP)**. (Verweis: Kapitel 5, S. 234)

### BIM einführen (S. 61–64, PAGE 63–65)
- Vorab eigene Bürosituation analysieren — Schlüsselfragen:
  - Welche Software/Hardware + Funktionen?
  - BIM-Kompetenzen des Personals?
  - Anforderungen der Kunden?
  - Reicht die Internetverbindung? (Fußnote 72: viel Datenaustausch, oft cloudbasiert, Baustellendaten)
- CAD-Software, die zu BIM-fähig entwickelt wurde, evtl. weiternutzbar — aber **Zertifizierung für IFC-Austausch nötig**.
- Meist **mehrere Softwarelizenzen pro Arbeitsplatz** (Modelliersoftware + Kollaboration + ggf. Prüfsoftware); engere Updatezyklen. Prüf-/Kollaborationssoftware nicht zwingend pro Arbeitsplatz (Fußnote 73).
- **Hardware-Empfehlungen:** bestehende Arbeitsplätze oft ausreichend, Server meist Upgrade nötig; **SSD-Festplatte empfohlen**; Grafikkarte + Arbeitsspeicher wesentlich; **zweiter Bildschirm** als wesentliche Erleichterung.
- Nicht bei Aus-/Weiterbildung sparen; Erlerntes zwischen Schulungen praxisgerecht erproben.
- Ohne BIM-Erfahrung im Team kaum Einführung ohne externe Hilfe (externe Berater:innen als Ansprechperson).
- Kleinere Büros oft leichter/flexibler als größere.
- **Ziele:** kurz-/mittelfristig setzen (richtiges Modellieren, korrekter Datenaustausch, Modellprüfungen); schrittweise; klar definiert, erreichbar, messbar; **Minimalprinzip** (geringster Aufwand, größter Nutzen).
- **Pilotprojekt:** laufendes Projekt (selbstständig ausprobieren) oder gemeinsames Pilotprojekt mit Auftraggeber. Einführungsphase meist **little closedBIM** (intern, nicht beauftragt/Vertragsbestandteil).

### Literaturverzeichnis Grundlagen (S. 64–65, PAGE 65–66)
- Schlüsselwerke u.a.: Hofstadler/Motzko (Hrsg.), *Agile Digitalisierung im Baubetrieb*, Springer Vieweg 2021 (ISBN 978-3-658-34106-0); Borrmann/König/Koch/Beetz (Hrsg.), *Building Information Modeling*, Springer 2015 (ISBN 978-3-658-05605-6); Wiese (2019), *BIM-Prozess kompakt* (ISBN 978-3-481-03840-3).
- **ÖNORM A 6241-2:2015** — Digitale Bauwerksdokumentation – Teil 2: Building Information Modeling (BIM) – Level 3-iBIM.
- RL 2014/24/EU; Studien: McKinsey (2017) *Reinventing Construction*, Roland Berger (2016), EYGM (2021) Hochbauprognose.

### Vorbild IFC-basierter BIM-Standard Österreich (S. 66–67, PAGE 67–68)
- **ÖN 19650-1:** BIM = Methodik, um aus Sicht des Bestellenden den Informationskreislauf (Anforderungen) in Inputs/Outputs festzulegen.
- **ÖN 29481:** Grundlage für **Information Delivery Manual (IDM)** — an IFC orientierte standardisierte Beschreibung von Informationsanforderungen über Lebenszyklusprozesse.
- Modellierung von Bauwerksinformationen = digitale Infos für Planung, Entwurf, Bau, Betrieb, **Rückbau**.
- **ASI-Merkmalserver** unterstützt Erstellung des IDM.
- **ÖN 6241-2 (ÖNORM A 6241-2):** nationale Systematik; **Phasenmodell** regelt geometrische + alphanumerische Inhalte virtueller Gebäudemodelle. Merkmale (Modellelemente: bauphysikalische Kennwerte, statische Eigenschaften, Materialien) in Abstimmung mit IFC entwickelt.
- ASI-Merkmalserver bildet Phasenmodell in öffentlich zugängliche Datenbank ab: Elemente (Wände, Decken, Stützen) + Merkmale (bei Wänden: Länge, Höhe, Stärke). Merkmale können einer **Leistungsphase** zugeordnet werden → (1) Merkmal-Definition klargestellt, (2) Verantwortlichkeit eindeutig zuordenbar, (3) international anschlussfähiger IFC-basierter BIM-Standard Österreich.
- **EN 17412-1:** befasst sich mit Qualität der Daten / **Datentiefe** → Minimalanforderung + minimale Datenqualität, kombinierbar mit Vergütungsmodell. Geometrische Qualität nicht vorweggenommen.
- ÖN-6241-2-Normungsansatz beeinflusst **VDI- und CEN-Norm**. (Bernhard L. Wieland, Bundeskammer der Ziviltechniker:innen)
- Grundsatz: Planende entscheiden selbst über Informationsdichte; projektbezogen vereinbarbar. Kein Zwang, mehr Daten zu liefern als bezahlt; tiefergehende Datendichte = gesondert definieren/beauftragen/abgelten.

### Informations-Box: IDM & MVD (BuildingSMART) (S. 67, PAGE 68)
- **BuildingSMART:** internationale Nonprofit-Organisation, definiert **IFC** für BIM-Datenaustausch im Bauwesen.
- **IDM (Information Delivery Manual):** ISO-zertifizierte (**ISO 29481-1 und -2**) BuildingSMART-Methode zur Beschreibung von Informationsanforderungen im Lebenszyklus; umfasst Ausmaß + Spezifikationen jener Infos, die ein Akteur zu einem bestimmten Zeitpunkt/Arbeitsprozess bereitstellen muss.
- **MVD (Model View Definition):** technische Spezifikation in Bezug zu definierter IFC-Version; Grundlage für IFC Import-/Exportfunktionen; legt benötigte Teilmenge des IFC-Datenmodells fest, um **Exchange Requirements** zu erfüllen; Teilmodell-Austausch möglich.
  - **Dateiformat: `*.mvdxml`** (XML-Format); Informationsmodell als XML-Schema-Definition.
  - **MVD-Beispiele:** IFC2x3 Coordination View 2.0, IFC2x3 FM Handover View, IFC2x3 Structural Analysis View, IFC4 Reference View, IFC4 Design Transfer View.

---

## Kapitel 2 — Richtig Modellieren (Autor: Marcus Wallner) (S. 68 ff., PAGE 69 ff.)

### Einführung (S. 68, PAGE 69)
- Modellieren = grundsätzlicher Unterschied zur CAD-Arbeitsweise: nicht mehr 2D-Ansichten zeichnen, sondern aus **Bauteilkatalogen** ein 3D-Modell erstellen, aus dem 2D-Pläne automatisch generiert werden.
- Bauteile haben Attribute (Daten). „Gewissenhaftes und möglichst fehlerfreies Modellieren ist die Grundvoraussetzung für BIM — ohne korrekte Modelle funktioniert BIM nicht."

### Kapitel-2-Inhaltsverzeichnis (Seitenanker, PAGE 70)
- Zeichnung versus Modell S. 70 · Attribute S. 74 · Geometrische Grundlagen S. 76 · Knotenausbildung S. 79 · Positionierung des Modells S. 80 · Nullpunkte Projektbasispunkt S. 80 · Normalnull S. 80 · Nordung S. 82 · Vertikale Gliederung S. 84 · Einteilung nach Geschossen S. 84 · Umgang mit uneinheitlichen Geschossen S. 89 · Verortung im Infrastrukturbereich S. 90 · Modelliertechniken S. 92 · Bezüge S. 92 · Objekt als Bezug S. 93 · Raster S. 93 · Dynamisches Modellieren S. 94 · Modellierregeln S. 94 · Arbeiten mit Platzhaltern S. 95 · Detaillierungsgrad S. 96 · LOD – Level of Development S. 96 · LoX S. 97 · LOD 100–500 S. 98 · LoG – Level of Geometry S. 99 · LoI – Level of Information S. 100 · LoC – Level of Coordination S. 101 · Objektbibliotheken S. 102 · Bürostandard S. 102 · Nomenklatur S. 104 · Allgemeine Bibliotheken S. 104 · Herstellerbibliotheken S. 105 · Literaturverzeichnis S. 106.

### Zeichnung versus Modell (S. 70–73, PAGE 71–74)
- 2D-Pläne = aus dem BIM-Modell abrufbare **Echtzeit-Projektionen**; bei gleichzeitiger Generierung passen Maße aller Pläne genau zueinander.
- 3D-Modell = Ausgangsbasis; generierte Pläne zunächst „nackt" (ohne Beschriftung). Unbemaßter/unbeschrifteter Plan = de facto wertlos.
- **Automatische Beschriftungsblöcke:** Raumstempel, Durchbruchsbeschriftung, Brüstungshöhe, Höhenkoten — Wert automatisch aus Modell-Parametrik.
- **Modelliersoftware** = Produkte zur Erstellung BIM-fähiger Fachmodelle (Verweis Kapitel 3, S. 136).
- „Wir zeichnen nicht mehr, wir modellieren": Bauteile von Anfang an als dreidimensionale Objekte; Objekte haben Geometrie + semantische Infos (Attribute, Mengen, Parameter, intelligente Verhaltensregeln).
- BIM-Software erkennt anhand der **Hierarchie der Schichten**, wie diese sich an der Ecke verschneiden (Abbildung 9).
- Empfehlung (Arch. DI Martin Gruber): in früher Projektphase Modellierung auf notwendiges Minimum reduzieren; eigene Entwurfsphasen-Bauteile mit nur nötigster Information, später durch detailliertere ersetzen (vermeidet falsche Objektinformationen + Haftungsthematik).

### Attribute (S. 74–75, PAGE 75–76)
- BIM-Objekt = Geometrie + **alphanumerische Attribute**. Synonyme: Attribut / Merkmal / Eigenschaft.
  - buildingSMART/**bSDD (buildingSMART data directory):** Begriff „Attribut".
  - Software/Dateiformate: „Eigenschaften"; Österreich (wegen Merkmalserver): „Merkmale".
- „alphanumerisch" = mögliche **Datentypen**, die der Attributwert annehmen kann; auch Boolean „wahr/falsch" (z.B. Attribut „tragend") oder vordefinierte **Feuerwiderstandsklassen**.
- **Praxistipp:** Im **IFC-Schema werden Attribute durch Property Sets ausgetauscht.**
- Attribute = Grundlage für Simulationen, Bauteillisten, Auswertungen.
- **GUID (Globally Unique Identifier):** jeder Objektinstanz in der Modelliersoftware zugewiesen → weltweit eindeutige Zuordnung; ermöglicht Attribute aus verschiedenen Modellen gleichen Klassen zuzuordnen + in Datenbanken zu verarbeiten (z.B. Wandmengen aus Teilmodellen addieren).
- Ein Attribut = Name (Bezeichnung) + Datentyp mit gültigem Wertebereich. **Eindeutige Attributsliste pro Projekt zwingend** — gleiches Attribut darf nicht unter verschiedenen Namen auftauchen, sonst funktionieren Auswertungen nicht.
- Verweise: Kapitel 4 — bSDD S. 186; BIM-Objekt S. 181; Merkmalserver S. 188; Datentyp S. 183.

### Geometrische Grundlagen (S. 76–78, PAGE 77–79)
- **Zwei Verfahren der Geometrieerzeugung:**
  1. **Explizites Verfahren (Flächenmodell / Boundary Representation, Brep):** beschreibt Volumen über seine Oberflächen via Hierarchie der Grenzbeziehungen **Körper → Fläche → Kante → Vertex**. Typisches Beispiel: Geländeoberfläche (Abb. 12).
  2. **Implizites Verfahren (Körpermodell / Constructive Solid Geometry, CSG):** prozedural, Abfolge von Konstruktionsschritten (Erstellungsgeschichte). Aus primitiven Grundkörpern (**Quader, Zylinder, Prisma, Pyramide, Kugel, Kegel**) über **Boolesche Operationen (Vereinigung, Differenz, Schnittmenge)**. **Extrusion, Rotation, Sweep, Loft** zählen ebenfalls zu CSG.
- **Vergleich:** Implizit braucht mehr Rechenleistung, hat aber **geringere Datenmengen beim Austausch** als explizit; CSG-Konstruktionsschritte jederzeit rückgängig/neu konstruierbar — Fehlergefahr, wenn rückgängig gemachte Schritte mit anderen Objekten verkettet sind.
- Häufigste CSG-Fehler: Zielsystem unterstützt nicht alle Operationen des Ausgangssystems bzw. führt sie nicht gleich aus (Fußnote 81: Borrmann 2015, S. 30).

### Knotenausbildung (S. 79, PAGE 80)
- Automatische Knotenberechnung bei verschneidenden Wänden/Decken.
- Einfachster Fall: **T-förmiges Auftreffen** zweier Wände → Überlagerung; Software rechnet **Boolesche Differenz** + legt ggf. unsichtbaren **Subtraktionskörper** an.
- Komplexe Knoten (viele Wände/Decken) = fehleranfälliger. **Hierarchie/Verdrängung:** Beton verdrängt Wärmedämmung, diese verdrängt Putz.
- Bei unterschiedlichen Betonqualitäten am Knoten kann automatische Generierung versagen → manuelle Nacharbeit (Änderung der Reihenfolge der CSG-Verfahren).
- Abbildung 15: T-Stoß mit richtiger und falsch berechneter Geometrie.

## Maschinen-Regeln

- [FRIST] BIM-Daten müssen auch nach mehr als 80 Jahren noch lesbar und verarbeitbar sein → openBIM/offenes Format erforderlich (ÖBB-Sicht, S. 42, PAGE 43).
- [PFLICHT] Großbritannien: seit 2016 verpflichtende BIM-Anwendung (S. 47, PAGE 48).
- [PFLICHT] Österreich: keine gesetzliche BIM-Verpflichtung, aber bei öffentlichen/halböffentlichen Projekten meist gefordert / bessere Vergabe-Reihung (S. 47, PAGE 48).
- [PFLICHT] Nutzung spezifischer elektronischer Instrumente für öffentliche Bauaufträge/Wettbewerbe ist zwingend vorschreibbar — Art. 2 Abs. 4 Vergabe-RL 2014/24/EU (S. 48, PAGE 49).
- [PFLICHT] Öffentliche Auftragsvergabe nach den Grundsätzen RL 2014/24/EU vom 26.02.2014 (freier Warenverkehr, Niederlassungs-/Dienstleistungsfreiheit, Gleichbehandlung, Nichtdiskriminierung, gegenseitige Anerkennung, Verhältnismäßigkeit, Transparenz) (S. 47, PAGE 48).
- [PFLICHT] Bei BIM-Austausch müssen Elemente in identischer Ausgestaltung ankommen: gleiche Kategorie, gleiche Eigenschaften, gleiche Menge, gleicher Entwicklungsstand (S. 49, PAGE 50).
- [PFLICHT] Für IFC-Datenaustausch ist eine Software-Zertifizierung (IFC-Format) notwendig (S. 62, PAGE 63).
- [PFLICHT] Pro Projekt muss eine eindeutige Attributsliste existieren; gleiches Attribut darf nicht unter verschiedenen Namen vorkommen — sonst keine funktionierenden Auswertungen (S. 75, PAGE 76).
- [PFLICHT] Prüfregel: Feuerwiderstandsklasse einer Tür muss mit der ihrer Wand übereinstimmen (S. 54, PAGE 55).
- [PFLICHT] Prüfregel: Brüstungen müssen die geforderte Absturzhöhe erfüllen (S. 54, PAGE 55).
- [PFLICHT] Prüfregel: Fenster/Türen müssen 90° aufschlagen können (keine Stütze vor dem Fenster) (S. 54, PAGE 55).
- [DEFINITION] little BIM = Anwender in eigener Fachdisziplin mit eigener Software; big BIM = mehrere Fachdisziplinen in ihrer Software (S. 41, PAGE 42).
- [DEFINITION] closedBIM = herstellerspezifische Formate/Plattform; openBIM = unterschiedliche Software + offene Schnittstellen/neutrale Austauschformate (S. 41, PAGE 42).
- [DEFINITION] IFC (Industry Foundation Classes) = buildingSMART-Datenschema für Informationsaustausch zwischen proprietärer Software; standardisiert in ISO 16739:2013 bzw. ISO 16739-1:2018 (S. 50, PAGE 51, Fußnote 62).
- [DEFINITION] CDE = Common Data Environment, zentrale BIM-Datenbank (S. 46, PAGE 47, Fußnote 59).
- [DEFINITION] AIA = Auftraggeberinformationsanforderungen; BAP = BIM-Abwicklungsplan (S. 60, PAGE 62).
- [DEFINITION] IDM (Information Delivery Manual) = ISO-29481-1/-2-zertifizierte BuildingSMART-Methode zur Beschreibung von Informationsanforderungen im Lebenszyklus (S. 66–67, PAGE 67–68; ÖN 29481).
- [DEFINITION] MVD (Model View Definition) = technische Spezifikation zu einer IFC-Version; Dateiformat `*.mvdxml`; legt IFC-Teilmenge für Exchange Requirements fest (S. 67, PAGE 68).
- [DEFINITION] GUID = Globally Unique Identifier, jeder BIM-Objektinstanz zugewiesen, weltweit eindeutige Zuordnung (S. 75, PAGE 76).
- [DEFINITION] Brep (Boundary Representation) = explizites Flächenmodell (Hierarchie Körper→Fläche→Kante→Vertex) (S. 76, PAGE 77).
- [DEFINITION] CSG (Constructive Solid Geometry) = implizites Körpermodell aus Grundkörpern (Quader/Zylinder/Prisma/Pyramide/Kugel/Kegel) via Boolescher Operationen (Vereinigung/Differenz/Schnittmenge) + Extrusion/Rotation/Sweep/Loft (S. 77, PAGE 78).
- [DEFINITION] Attribut = Name + Datentyp mit gültigem Wertebereich; im IFC-Schema über Property Sets ausgetauscht (S. 74–75, PAGE 75–76).
- [DEFINITION] BCF = BIM Collaboration Format, regelt Kommunikation bei Mängel-/Issue-Abarbeitung (S. 55, PAGE 56).
- [DEFINITION] Simulation = rechnerisches Nachahmen realer/geplanter Situationen mit computerbasiertem Rechenmodell; Grundsatz „garbage in = garbage out" (S. 58–59, PAGE 60).
- [DEFINITION] Norm ÖNORM A 6241-2:2015 = Digitale Bauwerksdokumentation Teil 2: BIM Level 3-iBIM; Phasenmodell für geometrische + alphanumerische Modellinhalte (S. 65/66, PAGE 66/67).
- [DEFINITION] Norm EN 17412-1 = Datenqualität/Datentiefe; definiert Minimalanforderung + minimale Datenqualität (S. 66, PAGE 67).
- [DEFINITION] Norm ÖN 19650-1 = BIM-Methodik: Informationskreislauf in Inputs/Outputs aus Bestellersicht (S. 66, PAGE 67).
- [DEFINITION] Knotenausbildung T-Stoß = Boolesche Differenz + ggf. unsichtbarer Subtraktionskörper; Verdrängungs-Hierarchie Beton → Wärmedämmung → Putz (S. 79, PAGE 80).

BIM-Handbuch-2022 part1: 30 Regeln — BIM-Grundlagen und Modellieren
