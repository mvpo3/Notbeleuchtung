# AC 26 Grundkurs — Teil 2
> Quelle: AC 26 Grundkurs (buecher) · Seiten 81-120.

Dies ist ein **Archicad-26-Grundkurs** (GRAPHISOFT Deutschland GmbH, Hochschul-/Studierenden-Kurs, „Nur für Kursteilnehmer"). Es handelt sich **nicht** um ein Norm-/OVE-Dokument, sondern um eine CAD-Software-Anleitung. Teil 2 deckt **TEIL C: DARSTELLUNG** (Grundlagen der Darstellung, Schnitte & Ansichten, 3D-Darstellungen & Arbeitsblätter) und den Beginn von **TEIL D: PLÄNE ERSTELLEN** (Ausschnitte, Planlayouts) ab. Inhalt ist Workflow- und Bedienwissen für Architektur-Plandarstellung in Archicad; technische Zahlenwerte sind softwarebezogen (Stiftnummern, Strichstärken in Pt, Maßstäbe, Blattformate, Ränder in mm). Diese Daten können für die Plandarstellung/Layout-Konventionen relevant sein, enthalten aber keine elektrotechnischen Normwerte.

## Inhalt

### 5 Grundlagen der Darstellung — Kursdatei `gk_ac26_kursdatei02.pln`
- Prinzip: Grundriss wird **nie doppelt gezeichnet**; ein Modell wird unterschiedlich dargestellt → Änderungen schlagen automatisch in alle Zeichnungen durch.

#### 5.1 Darstellungs-Schnell-Optionen
- Schnell-Optionen-Leiste am **unteren Bildschirmrand**; bei zu geringer Bildschirmauflösung als Palette via Menü **Fenster > Paletten > Schnell-Optionen**.
- Klick auf Symbol → Einstellungsfenster; Klick auf Text → Voreinstellung wählen.
- Anwendbar in allen Fenstern: Grundriss, Ansicht, Schnitte, Detail, Arbeitsblatt, 3D-Fenster.
- Schnell-Optionen zeigen die aktuell gültigen Einstellungen des aktiven Fensters. Zum dauerhaften Speichern/Platzieren auf Layout → **Ausschnitte** anlegen (Kapitel 8).
- **Überblick der 9 Schnell-Optionen:**
  - **Maßstab** — Darstellungsmaßstab des Fensters; Schriftgröße von Texten und Raumstempeln passt sich automatisch an.
  - **Ebenenkombination** — welche Ebenen wie (Drahtmodell, schattiert) dargestellt werden.
  - **Strukturdarstellung** — bei mehrschichtigen Bauteilen: komplette Struktur / Aufbau ohne Bekleidungen / nur Kern.
  - **Stift-Set** — Farben und Strichstärken.
  - **Modelldarstellung** — Detaillierungsgrad des Gebäudemodells.
  - **Grafische Überschreibung** — Elemente hervorheben/anders darstellen ohne Änderung der Grundeinstellungen.
  - **Umbau-Filter** — bei Umbau-Projekten Phasen filtern (Bestand, Abbruch, Neubau, Endzustand).
  - **Bemaßung** — Bemaßungseinstellungen je Fenster; Maße nach **DIN / ÖNORM** oder anders.

#### 5.2 Ebenenkombination
- Ebenen sortieren Elemente logisch (Bemaßungen, Möbel, Außenwände, Innenwände …) → leicht filter-/ein-/ausblendbar.
- Ebeneneinstellungen-Fenster: **Verzeichnisansicht** (Ordner + Drag&Drop) oder **Listenansicht** (alphabetisch, alle Ordner).
- Pro Ebene einstellbar: sperren/entsperren (Schloss), ein-/ausblenden (Auge), 3D als Drahtmodell/schattiert (3D-Symbol), Verschneidungsgruppe (Zahl — legt fest, mit welchen anderen Ebenen Bauteile sich verschneiden).
- Links: vorhandene Ebenenkombinationen (gespeicherte Einstellungssätze).
- **Eigene Kombination erstellen:** Ebenen im aktuellen Fenster einstellen → Ebeneneinstellungen öffnen → links **Neu…** → Namen vergeben → 2× **OK**. Danach direkt in Schnell-Optionen wählbar.
- **Kombination anpassen:** Ebenen-Einstellungen öffnen → links Kombination wählen → Ebenen ändern (z.B. Ebene **85 Schnitt Marker** ausblenden) → **Aktualisieren** → **OK**.

#### 5.3 Stift-Set
- Jeder Stift ist durch **Nummer, Strichstärke und Farbe** definiert. Gleiche Stiftnummer kann in verschiedenen Stift-Sets andere Strichstärke/Farbe haben.
- Empfehlung: **mindestens für die ersten 9 Stifte** konsequent die Strichstärken der Tuschestifte verwenden — in allen Stift-Sets gleich.
- Echte Strichstärke anzeigen: Rechtsklick in leeren Bereich → **Echte Linienstärke**.
- **Eigenes Stift-Set anlegen (Beispiel Schraffurfarbe):**
  - Stift **Nr. 10** im Stift-Set **02 S/W 1:100/1:200** wählen — in der deutschen Archicad-Sprachversion der Standardstift aller Baustoffschraffuren.
  - Farbfeld → gewünschte Farbe (z.B. Grauton) per RGB-Werte/Farbspektrum → OK.
  - **Speichern als… > Individuelles Stift-Set speichern als** → Name → Speichern → OK. Danach werden alle Baustoffschraffuren grau.
- **Stift-Set anpassen (Haarlinien):** Haarlinien (sehr feine Linien) wirken für Entwurfspräsentationen elegant.
  - Stifte **Nr. 1** (Standard für Objekte und Aufsichtslinien) und **Nr. 10** (Standard für Schraffuren) markieren (Mehrfachauswahl mit Cmd/Strg).
  - Strichstärke auf **0,25 Pt** ändern.
  - **Speichern als…** → bestehendes Stift-Set **überschreiben** → OK.

#### 5.4 Modelldarstellung
- Legt Detaillierungsgrad von Konstruktionselementen/Objekten in jedem Bearbeitungsfenster fest.
- Beispiel-Voreinstellungen: **01 Beispiel Entwurf**, **04 Beispiel Genehmigungsplanung**, **05 Beispiel Ausführungsplanung**.
- Empfehlung: passende Voreinstellung wählen → **duplizieren** → anpassen.
- **Eigene erstellen:** Voreinstellung **04 Beispiel Genehmigungsplanung** wählen → **Neu…** → Name (z.B. „Projekt-Präsentation") → OK (dupliziert die Einstellungen).
- **Anpassen (Beispiel):** Bereich **Treppen-Optionen** anpassen (Treppen ohne Text); Bereich **Weitere Einstellungen der Bibliothekselemente** → **Türöffnungslinie** (gerade, dünne Öffnungslinie) → OK. Ergebnis: Treppen ohne Text, Türen mit gerader dünner Öffnungslinie.

#### 5.5 Grafische Überschreibung
- Hebt Bauteile nach Kriterien hervor / stellt sie anders dar — **ohne** Bauteileinstellungen zu ändern (nur Darstellung im aktuellen Fenster).
- Beispiel-Voreinstellungen: **70 Raum Kategorienfarbe** (Räume nach Kategorie einfärben), **60 Bauteile schwarz** (alle geschnittenen Elemente schwarz).
- Zurücksetzen: **Keine Überschreibungen**.
- **Eigene erstellen (Beispiel „Entwurf – Außenanlagen grau"):**
  - Vorbereitung: Ebene **60 Ausstattung außen** einblenden (Gartenwände + Bodenbelagsschraffuren); Ebenenkombination **Grundriss-ohne-Bemaßung** aktualisieren.
  - Links: bestehende Überschreibungen; rechts: zugeordnete Regeln.
  - **Neu… > Neue Kombination** → Name „Entwurf - Außenanlagen grau" → OK.
  - **Neue Regel hinzufügen > Neue Regel** → Name „Außenanlagen grau" → OK.
  - Regel-Einstellungen (drei Punkte): Kriterien (2A) definieren, Überschreibung (2B) definieren.
  - Kriterium: **Element-Typ ist gleich Alle Typen**; zusätzliches Kriterium über **Hinzufügen… → „Ebene"**: **Ist gleich Ebene 60 Ausstattung außen**.
  - Überschreibung: Haken bei **Linie / Marker / Textstift** → Stift **Nr. 93 (hellgrau)**; **Schraffurvordergrundstift** ebenfalls Stift **Nr. 93** für Zeichnungsschraffuren (1. Symbol) und Schnittschraffuren (3. Symbol); Option **Nur Stiftfarbe überschreiben** → OK → OK.
- **Anpassen:** Im Einstellungsfenster weitere Regeln hinzufügen (A), neue Regel (B), bestehende über drei Punkte (C), alle Regeln über **Regeln bearbeiten…** (D).

### 6 Schnitte und Ansichten
- Schnitte und Ansichten funktionieren gleich; alle Einstellungen gelten für beide.

#### 6.1 Schnitt- und Ansichts-Einstellungen
- Öffnen: Doppelklick im Navigator. Beispiel **Schnitt A-A** mit Ebenenkombination **Schnitte/Ansichten** (Gelände eingeblendet, Möblierung ausgeblendet).
- Zugang zu Schnitt-Einstellungen: über Grundeinstellungen des Schnitt-Werkzeugs (vor Erstellung) oder Rechtsklick im Navigator → **Schnitt-Einstellungen…**.
- **Art des Schnitt-Markers:**
  - **Quell-Marker** — erzeugt einen Schnitt (Hauptanwendung).
  - **Verknüpfter Marker** — erzeugt keinen Schnitt; Referenz auf anderen Ausschnitt/Blickpunkt/Zeichnung.
  - **Nicht-verknüpfter Marker** — individueller Text, erzeugt keinen Schnitt.
- **Schnitt-Status (nur Quell-Schnittmarker):**
  - **Automatisches Wiederaufbauen (Modell)** — Schnitt wird bei jedem Öffnen automatisch aktualisiert, falls Grundriss geändert.
  - **Manuelles Wiederaufbauen (Modell)** — nur über **Anhand des Modells neu aufbauen** (Kontextmenü) aktualisiert.
  - **2D-Zeichnung** — Elemente in 2D-Zeichnungselemente zerlegt, nicht mit Grundriss verknüpft, kein automatischer Modell-Neuaufbau (manuell aktualisierbar).
- **Auf Geschoss zeigen** (nur Quell): auf welchen Geschossen Schnitt-Marker und Schnittlinien gezeigt werden.
- **Horizontaler Bereich** (Tiefe des Grundrissabschnitts):
  - **Unendlich** — alle Elemente hinter der Schnittlinie (sofern nicht verdeckt).
  - **Begrenzt** — nur Elemente zwischen Schnittlinie und Begrenzungslinie.
  - **Keine Tiefe** — nur Elemente, durch die die Schnittlinie verläuft.
- **Vertikaler Bereich** (Höhe):
  - **Unendlich** — gesamte Projekthöhe.
  - **Begrenzt** — Höhenwerte für obere und untere Begrenzung eingebbar.
- **Modelldarstellung von Schnitten:** Stifte für geschnittene/ungeschnittene Elemente, Schatten im Schnitt, unterschiedliche Darstellung verschiedener Sichtbereiche → reduziert 2D-Nachbearbeitung.

#### 6.2 Staffage
- Belebung von Schnitt/Ansicht: Hintergrund, Bäume, Menschen, Objekte; ergänzt durch Schraffuren, Linien, Objekte, Beschriftungen, Bilder.
- **Hintergrund einfügen:** Zeichnungs-Werkzeug aktivieren → in Zeichenfläche klicken → **Lokales Dateisystem > Suchen** → Bild öffnen. Eckpunkt anklicken → Pet-Palette (Position/Größe/Form). Bei Bild vor dem Schnitt: Rechtsklick → in Darstellungsreihenfolge nach hinten schieben. Transparenter: weiße transparente Schraffur über das Bild und unter den Gebäudeschnitt legen.
- **Bäume einfügen:** Objekt-Werkzeug-Einstellungen (Doppelklick) → Bibliotheksordner **1.03 Aussenbereich und Staffage (Deutschland)** bzw. **7. Umgebung (Österreich)** → Unterordner **Pflanzen 26** → **Laubbäume 26** → Laubbaum-Typ (z.B. Ahorn). Ebene **60 Pflanzen außen**, Dimensionen einstellen. **2D-Darstellung → Ansichtstypen: symbolische Seitenansicht** (alternativ Seitenansicht für realistisch); Symboltyp + Kontur/Schraffur wählen → OK. Hinter Gebäude legen, Größe über pinke Hotspots.
- **Menschen einfügen** (erklären Nutzungsart & Dimensionen): Objekt-Werkzeug-Einstellungen → DE: Ordner **1.04 2D Planung und Symbole 26 > Aussenbereich und Staffage 26 > Menschen 26**; AT: **8. Menschen und Fahrzeuge > Menschen Kontur 26**. Figur wählen → Ansichtstyp **Vorderansicht** → 2D-Darstellung (Stifte, Kontur, Schraffur) → Ebene **50 Staffage** → OK → platzieren.

#### 6.3 Beispiele
- Beispiel-Abbildungen für gestaltete Schnitte/Ansichten via Schnell-Optionen, Schnitt-/Ansichtseinstellungen und Staffage (nur Bilder, kein Textinhalt).

### 7 3D-Darstellungen und Arbeitsblätter

#### 7.1 3D-Fenster einrichten
- 3D-Fenster öffnen (Allgemeine Perspektive); Navigation: Orbit, Pan, Rundgang.
- Genaue Ausrichtung: Rechtsklick in leeren Bereich → **Standort & Projektionsart**.
- **Perspektiv-Einstellungen** (Blickpunkt-Position) bzw. **Axonometrie-Einstellungen** (Winkel, Achsenlängen, Sonnenstand exakt festlegbar).
- Ziel des Kapitels: Konzeptzeichnung über 3D-Schnitte, 3D-Dokumente, Arbeitsblätter.

#### 7.2 3D-Schnitte
- Erstellbar im 3D-Fenster und in 2D-Fenstern (Grundriss/Schnitt/Ansicht).
- **Erstellen:** Schaltfläche **3D-Schnitt ausführen** (Standard-Symbolleiste) → Scheren-Symbole an Rändern. Für individuelle Schnittebene: Rechtsklick auf Scheren-Symbol → **Eigene Schnittebene erstellen** → Seitenwand des 3D-Modells anklicken → violette Schnittebene mit Maus bewegen → linksklicken → **Fertigstellen**.
- **Temporär:** Schnitt deaktivierbar über erneuten Klick auf **3D-Schnitt ausführen** (Modell bleibt erhalten).
- Zweiter 3D-Schnitt (Freifläche kürzen): Scherensymbol am rechten Rand (wird zum Papierkorb-Symbol), Schnittebene bewegen → Klick → **Fertigstellen**.

#### 7.3 3D-Dokumente
- 3D-Dokument = als Dokument gespeicherte Projektsicht auf das 3D-Modell; 2D-Elemente (Bemaßungen, Etiketten, Text, Schraffuren) ergänzbar. Änderungen am 3D-Modell werden automatisch übertragen. Eigene Modelldarstellung. Erstellbar aus 3D-Fenster oder Grundriss.
- **Erstellen:** Rechtsklick in leeren Bereich → **Neues 3D-Dokument aus 3D…** → **Referenz-ID „2.4"**, Name „3D-Schnitt 3D-Dokument" → **Erstellen**. Ablage: Ordner **3D-Dokumente** in der Projektmappe.
- **Anpassen:** Rechtsklick → **3D-Dokument-Einstellungen** → Bereich **Modelldarstellung** einstellen → OK.

#### 7.4 Arbeitsblätter
- Dienen der Erstellung/Bearbeitung von **2D-Zeichnungen**; nur 2D-Werkzeuge verfügbar.
- Anwendungsfälle: externe 2D-Zeichnungen platzieren (z.B. Vermessungs-/Lageplan; via Transparentpause unterlegen); eigene 2D-Zeichnungen (Diagramme, Legenden); modellbasierte Zeichnungen in 2D bearbeiten (Konstruktions-Elemente werden in 2D-Linien/Schraffuren/Text zerlegt).
- **Wichtig:** Modellbasierte Arbeitsblätter aktualisieren sich **nicht automatisch** bei Modelländerungen. Empfehlung: so viel wie möglich im Modellbereich (Geschosse, Ansichten, Schnitte, 3D-Dokumente) bearbeiten; Arbeitsblatt erst bei Erreichen der Grenzen erstellen.
- Manueller Neuaufbau: **Anhand des Ursprungs-Ausschnittes neu aufbauen** — setzt gelöschte/geänderte (modellgebundene) Elemente in Modell-Zustand zurück; neu hinzugefügte Elemente bleiben unverändert. Tipp: ein-/ausblendbare Ebenen nutzen.
- **Erstellen:** Arbeitsblatt-Werkzeug (Bereich Sichten) → Grundeinstellungen → **Referenz-ID „AB-01"**, Name „3D-Schnitt Arbeitsblatt" → Status **Ein neues Arbeitsblatt erstellen** → OK → Geometriemethode **Rechteckig** → Rechteck über komplette 3D-Dokument-Zeichnung ziehen → letzter Klick platziert Arbeitsblatt-Marker.
- **Nachbearbeiten:** Zeichnung in 2D-Elemente zerlegt → störende Linien löschen, Schraffuren ändern.

### TEIL D: PLÄNE ERSTELLEN

### 8 Ausschnitte

#### 8.1 Allgemeines
- Ausschnitt = gespeicherte spezielle Sichtweise auf das Projekt (Projekt selbst unverändert). Gespeicherte Darstellungs-Optionen: **Ebenenkombination, Maßstab, Strukturdarstellung, Stift-Set, Modelldarstellung, Grafische Überschreibung, Umbau-Filter**.
- Ablage: 2. Registerkarte des Navigators = **Ausschnitt-Mappe**. Arbeit in Projekt- und Ausschnitt-Mappe gleichermaßen möglich (gleiches Modell).
- **Zwei Gründe:** (1) Zeitersparnis — Darstellungs-Schnell-Optionen pro Ausschnitt hinterlegt, ein Doppelklick statt manuellem Neueinstellen. (2) Layouts erstellen benötigt Ausschnitte.
- Neu hinzugefügte Elemente erscheinen im Ausschnitt evtl. nicht (liegen auf ausgeblendeter Ebene). Empfehlung: alle Ausschnitte frühzeitig anlegen.

#### 8.2 Ausschnitte erstellen und bearbeiten
- **Einzelnen Ausschnitt erstellen:** Zeichnung öffnen (z.B. Arbeitsblatt **AB-01 Konzept**) → Schnell-Optionen einstellen: **Maßstab 1:200**, **Stift-Set: Stift-Set braun**, **Grafische Überschreibungen: keine Überschreibungen** → auf linkes Piktogramm zoomen → Ausschnitt-Mappe → **Aktuellen Ausschnitt sichern…** → Name „Konzept Modulbau" → Einstellungen im Bereich Allgemein prüfen.
  - **Hinweis (wichtig):** Beim Anlegen darf nie das Wort **„Individuell"** in den Einstellungen stehen — eine individuelle Kombination gilt nur temporär; immer unter neuer/benannter Kombination speichern.
  - Häkchen **„Zoom und Drehung beim Öffnen dieses Ausschnitts ignorieren"** im Bereich 2D/3D-Dokumente **entfernen** (aktiviert würde der Ausschnitt im zuletzt aktiven Zoom statt im gespeicherten Zoom öffnen) → **Erstellen**.
  - Zweiter Ausschnitt „Konzept Erweiterbarkeit" (zweites Piktogramm, gleiche Einstellungen, Häkchen ebenfalls entfernen). Doppelklick wechselt zwischen Ausschnitten, Fenster zoomt jeweils.
- **Ausschnitt aus 3D-Fenster:** Ins 3D-Fenster → Ebenenkombination **Schnitte/Ansichten** + Stift-Set **Schraffuren grau** → **Aktuellen Ausschnitt sichern…** → Reiter **Nur 3D**: **3D-Fenster** wählen → **Erstellen**. Weiterer Ausschnitt „Außenperspektive Rendering" mit anderer Nur-3D-Einstellung: erzeugt beim Öffnen ein aktuelles Rendering (z.B. Bleistiftzeichnungs-Stil oder photorealistisch).
- **Ausschnitte ordnen/löschen:** Löschen von Ausschnitten verliert **keine** Modellinhalte (nur die voreingestellte Darstellung); Löschen von **Zeichnungen aus der Projektmappe** → unwiederbringlicher Verlust. Mehrfachauswahl mit Umschalt-Taste.
- **Ordner erstellen:** **Neuer Ordner…** (z.B. „Konzeptdarstellung"); Ausschnitte per Drag&Drop einsortieren/umordnen; Auf-/Zuklappen über grauen Pfeil.
- **Ordner klonen:** ganze Ordner (Geschosse, Schnitte, Ansichten, Arbeitsblätter) klonen → **selbstaktualisierend**: bei Hinzufügen/Löschen eines Schnitts/Geschosses in der Projektmappe wird Ausschnitt mit-aktualisiert.
  - **Geschosse klonen (Beispiel):** Grundriss (z.B. EG) öffnen → einstellen: **Maßstab 1:100**, **Ebenenkombination Grundriss-ohne-Bemaßung**, **Strukturdarstellung Komplettes Modell**, **Stift-Set braun**, **Modelldarstellung Projekt-Präsentation**, **Grafische Überschreibung Keine Überschreibungen**, auf Grundriss zoomen → **Ordner klonen** → Ordner **Geschosse** wählen → Schnell-Optionen/Zoom prüfen (gelten für alle Grundrisse) → **Klonen**. Kleiner schwarzer Pfeil unten links = geklonter Ordner.
  - Verzeichnisse **Schnitte** und **Ansichten** ebenso klonen, dabei Ebenenkombination auf **Schnitte/Ansichten** ändern.
- **Ausschnitt-Einstellungen bearbeiten — zwei Wege:**
  - **A: Ausschnitt-Einstellungen** — Rechtsklick auf Ausschnitt → Einstellungen ändern (z.B. Stift-Set auf **Schraffuren grau**) → OK.
  - **B: Neudefinieren** — Ausschnitt öffnen → Fenster einstellen → Rechtsklick → **Neudefinieren mit aktuellen Fenster-Einstellungen**. Besonders geeignet zum Ändern des **Zoom** (bei Variante A nur eingeschränkt möglich).

### 9 Planlayouts

#### 9.1 Vorbereitung
- Datei von Optionen/Varianten befreien (verkleinert Datei); sicherheitshalber unter neuem Namen speichern.
- Im Lage-/Landschaftsplan möglichst **2D-Bäume** (symbolhafte Ansichten) verwenden; viele 3D-Bäume beeinträchtigen die Rechnerleistung.
- Geeignetes Papierformat wählen, Layoutschema skizzieren, alle Zeichnungen als Ausschnitte angelegt haben.
- **Arbeitseinheit:** Modellbereich in **Meter** (Eingabe „3,00" = 3 m Wand). Layout-Bereich kann separate Einheit haben — Menü **Optionen > Projektpräferenzen > Arbeitseinheiten**; in der Kursdatei ist im Layout **Millimeter** eingestellt (alle Werte in mm).

#### 9.2 Das Masterlayout
- Jedes Layout basiert auf einem Masterlayout (legt Blattgröße fest + gemeinsame Elemente wie Plankopf, Logo, Name).
- Layoutbuch: Masterlayouts = graues Layout-Symbol, Layouts = weißes Symbol.
- **Masterlayout erstellen:** **Neues Masterlayout…** → Name (z.B. „Endabgabe Projekt") → Blattformat **A1**, Ausrichtung **Querformat** → Layout-Ränder gleichmäßig **30 mm** → Option **Als Grundeinstellung für neue Layouts verwenden** → **Erstellen**.
- **Gestaltungsraster einrichten:** Ziel-Raster **4 Spalten × 3 Zeilen/Reihen**, gleichmäßiger Rand (blaue Linie) **30 mm**.
  - Methoden: **A** Einrichtungs-Raster in Masterlayout-Einstellungen (hier verwendet); **B** Konstruktionsraster (Menü Ansicht > Konstruktionsraster darstellen / Raster-Einstellungen); **C** orange Hilfslinien; **D** Raster mit Linien-Werkzeug zeichnen.
  - Vorgehen (A): Masterlayout-Einstellungen → Reiter **Zeichnungsplatzierung** → Option **Zeichnungen an einem Raster ausrichten und zuordnen** aktivieren → **Einrichtungs-Raster…** → **4 Spalten, 3 Reihen** → Rasterliniendarstellung **Alle sichtbar** → OK → OK.

#### 9.3 Das Layout
- **Layout erstellen:** Layoutbuch → **Neues Layout** → **Eigene ID-Nr.** (eigene oder leer) → Name (z.B. „Titelseite") → Masterlayout **Endabgabe Projekt** als Grundlage → **Erstellen**.
- Zweites Layout „Grundrisse-Schnitte-Ansichten" analog (Schritte 1–5).

#### 9.4 Layoutbuch ordnen
- **Untergruppe erstellen:** **Neue Untergruppe…** → **Eigene ID-Nr.** (frei lassen) → Name (z.B. „Endabgabe") → **Erstellen**.
- **Sortieren:** Layouts per Drag&Drop in Untergruppen; Reihenfolge änderbar; Mehrfachauswahl mit Umschalt-/Cmd-/Strg-Taste.
- **Elemente löschen:** Beispiel-Layouts/-Untergruppen im Layoutbuch auswählen → **Löschen**. Löschen im Layoutbuch ist **nicht widerrufbar**.

### Hinweis zur Einordnung für ElektroPlaner
- Reines Archicad-Bedienwissen, keine OVE/ÖNORM-Elektroregeln. Übertragbar evtl.: Layout-/Plankopf-Konventionen (A1 Querformat, 30 mm Rand, Maßstäbe **1:100 / 1:200**), Stift-/Strichstärken-Disziplin (erste 9 Stifte konsistent, Haarlinie 0,25 Pt, Schraffurstift Nr. 10, Hellgrau Nr. 93), sowie die Ebenen-/Darstellungs-Logik (Modell einmal, viele Darstellungen via Ausschnitte/Überschreibungen) als Vorbild für DXF-Layer- und Darstellungs-Konzepte.
