# AC 26 Grundkurs — Teil 3
> Quelle: AC 26 Grundkurs (buecher) · Seiten 121-137.

Dies ist ein GRAPHISOFT-Archicad-26-Grundkursskript (CAD-Bedienungsanleitung, Bildungsversion), kein Elektroplanungs- oder ÖNorm/OVE-Dokument. Teil 3 (Seiten 121–137) deckt die Kapitel 9.5–9.7 (Planlayouts: Inhalte hinzufügen/bearbeiten, Druckvorbereitung), Kapitel 10 (Exportieren und Drucken mit dem Publisher) und Kapitel 11 (Hilfe/Support) ab und schließt mit Notizenseiten. **Hinweis:** Es sind KEINE elektrotechnischen Normwerte, Schutzbereiche, Querschnitte, Höhen oder OVE/ÖNorm-Inhalte enthalten — der Wissensgehalt ist reine Archicad-Software-Bedienung. Nachfolgend werden die Bedienschritte und Programmkonventionen dennoch vollständig festgehalten.

## Inhalt

### 9.5 Inhalte hinzufügen und bearbeiten (Planlayouts)
- 2D-Werkzeuge zum Anreichern von Layouts: Text, Schraffur, Linie. Zusätzlich platzierbar: Ausschnitte aus der Ausschnitt-Mappe sowie externe Zeichnungen.
- **Layout vs. Masterlayout:**
  - Elemente, die auf ALLEN zugehörigen Layouts an gleicher Stelle erscheinen sollen → auf das **Masterlayout** legen (spart Arbeit).
  - Elemente, die nur auf EINEM bestimmten Layout erscheinen sollen → dem **Layout** selbst hinzufügen.
- Masterlayout-Elemente werden auf zugehörigen Layouts standardmäßig **rot** dargestellt (nur Bildschirmdarstellung; im Ausdruck erscheinen sie in Original-Farbe). Die rote Einfärbung erleichtert die Unterscheidung.
- Einfärbung deaktivieren: Menü **Optionen > Arbeitsumgebung > Bildschirm-Optionen**, Haken bei „Einheitliche Farbe für Master-Elemente auf dem Layout" entfernen. (Im Skript bleibt die Einfärbung aktiv.)

#### Ausschnitte platzieren
- **Mit dem Zeichnungs-Werkzeug:**
  1. Layout „Titelseite" öffnen.
  2. Zeichnungs-Werkzeug im Werkzeugkasten unter **Dokumentation** aktivieren.
  3. Cursor an Zielstelle im Layout klicken.
  4. Im Menü den Ausschnitt „A-05 Ansicht Süd - Titelbild" wählen.
  5. Mit Klick auf **Platzieren** bestätigen.
- **Mit Drag&Drop:** Im Navigator die Ausschnitt-Mappe öffnen und gewünschten Ausschnitt per Drag&Drop auf das Layout ziehen (z. B. Ausschnitt „AB-01 Konzept Modulbau" mit gedrückter linker Maustaste in Rasterfeld A1). Beide Methoden liefern dasselbe Ergebnis.
- **Zeichnungsrahmen:** Die Punktlinie um Ausschnitte = „Zeichnungsrahmen", nur Bildschirmdarstellung, erscheint NICHT im Ausdruck. Ein-/Ausschalten: Menü **Ansicht > Bildschirmdarstellungsoptionen > Zeichnungsrahmen**.

#### Aktualisierungsmodus
- Platzierte Ausschnitte können bei Änderungen aktualisiert werden; je Zeichnung wählbar: **Manuell** oder **Automatisch**.
- Grundeinstellungen der Zeichnung öffnen mit Shortcut **Cmd+T (MAC)** bzw. **Strg+T (WIN)** → dort aktuellen Aktualisierungsmodus sehen/ändern.
- Empfehlung: Zeichnungen auf **Automatisch** stellen, damit Layouts stets aktuell sind.

#### Mehrere Ausschnitte gleichzeitig platzieren
- Mit gedrückter **Umschalt-Taste** mehrere Ausschnitte markieren und per Drag&Drop auf das Layout ziehen. Da im Masterlayout eingestellt ist, dass Zeichnungen bei Platzierung am Raster ausgerichtet werden, ordnen sie sich automatisch am Raster an.

#### Externe Zeichnungen hinzufügen
- Weitere Planinhalte (Hersteller-Details/-Pläne als PDF oder DWG, externe Bilder) lassen sich ebenfalls mit dem Zeichnungs-Werkzeug auf das Layout legen.
- **PDF-/DWG-Dateien:** per Drag&Drop aus Finder/Explorer auf das Layout ziehen. Bei mehrseitiger PDF wird nach der Dateiauswahl zur Seitenauswahl aufgefordert. Nach dem Platzieren haben sie den Aktualisierungsmodus **Manuell aktualisieren** (jederzeit änderbar).
- **Bild-Dateien:** per Drag&Drop möglich, werden aber mit dem **Bild-Werkzeug** eingefügt → beschränkte Bearbeitungsmöglichkeiten. Besser stattdessen die Platzierung per Zeichnungs-Werkzeug verwenden.

### 9.6 Zeichnungen bearbeiten und ausrichten
- Platzierte Ausschnitte müssen geordnet und am Gestaltungsraster ausgerichtet werden.
- Befehle dazu in der **Pet-Palette**: erscheint, wenn man eine Zeichnung auswählt und erneut darauf klickt. Je nach Klickpunkt unterschiedliche Bearbeitungsmöglichkeiten:
  - **Ecke** des Zeichnungsrahmens
  - **Kante** des Zeichnungsrahmens
  - **Innerhalb** des Zeichnungsrahmens

#### 2D-Zeichenelemente hinzufügen
- Layout ergänzbar mit Schraffuren, Linien, Text.
- **Text einfügen:**
  1. Text-Werkzeug im Bereich **Dokumentation** auswählen, Grundeinstellungen öffnen.
  2. Einstellungen vornehmen, mit **OK** bestätigen.
  3. Auf beliebige Stelle des Layouts klicken.
  4. Cursor nach rechts unten ziehen → rechteckiges Textfeld aufziehen, erneut klicken.
  5. Text-Editor öffnet sich: Text eingeben und Erscheinung einstellen (Schriftart, Schriftgröße, Fett, Kursiv etc.).
  6. Mit linker Maustaste außerhalb des Textfeldes klicken → Text fertig.
  - Nachträgliche Bearbeitung: Doppelklick auf den Text öffnet den Text-Editor erneut.
- **Auto-Texte:** Platzhalter, deren Inhalt automatisch eingetragen und bei Änderungen automatisch angepasst wird.
  1. Im Text-Editor Befehl **Auto-Text einfügen** klicken.
  2. Verzeichnis aller verfügbaren Auto-Texte öffnet sich; z. B. in der Suchzeile „Datum" eingeben.
  3. Autotext **System: Datum (kurz)** wählen.
  4. **Hinzufügen** klicken.
  5. Autotext erscheint grau hinterlegt im Editor, zeigt das aktuelle Datum.
- **Schraffuren einfügen** (Layout „Grundrisse-Schnitte-Ansichten"):
  1. Schraffur-Werkzeug im Bereich **Dokumentation** aktivieren, Grundeinstellungen öffnen.
  2. Passende Schraffur wählen (auch Texturschraffur möglich).
  3. Mit **OK** bestätigen.
  4. Geometriemethode **Rechteckig** aktivieren, mit zwei Klicks rechteckige Fläche zeichnen; alternativ Abmessungen per Tastatur eingeben und mit **Enter** bestätigen.

### 9.7 Vorbereitung für den Druck
- Vor Druck/PDF-Export: Rasterlinien des Gestaltungsrasters ausblenden, damit sie nicht erscheinen.
- Vorgehen: Einstellungen des Masterlayouts „Endabgabe Projekt" öffnen → Schaltfläche **Einrichtungs-Raster (1)** → im Dialog Rasterliniendarstellung auf **Alle ausblenden (2)** → beide Einstellungsfenster mit **OK (3+4)** schließen.
- Die Feldbeschriftung (A1, A2 usw.) erscheint nur am Bildschirm, NICHT im Ausdruck.

### 10 Exportieren und Drucken

#### 10.1 Was ist der Publisher?
- Layouts speichern/drucken auch über **Ablage > Sichern als** bzw. **Drucken** möglich, bei mehreren Layouts aber umständlich.
- **Publisher:** zeit- und arbeitssparendes Tool, um viele Layouts an einen zuvor definierten Ort zu exportieren oder zu drucken.
- Verfügbare Dateiformate u. a.: **PDF, DWG, DXF, JPEG**.
- Publisher-Sets befinden sich im **vierten und letzten Reiter** des Navigators.

#### 10.2 Publisher-Set einrichten
1. Im Navigator in Reiter **Publisher-Sets** wechseln.
2. Über Klick auf Pfeilsymbol **Eine Stufe höher** zur Übersicht der Publisher-Sets gelangen.
3. Mit **Neues Publisher-Set** ein neues Set erstellen.
4. Namen vergeben, z. B. „Endabgabe Export".
5. **Erstellen** klicken.
6. Neues Set erscheint im Navigator → mit Doppelklick öffnen.
7. Set ist leer; zu exportierende Layouts via **Organisator** einordnen → rechts oben **Projekt-Auswahl > Organisator anzeigen**.
8. Organisator = zwei nebeneinander angeordnete Navigator-Fenster → erlaubt Layouts aus dem Layoutbuch per Drag&Drop ins Publisher-Set. Links das **Layoutbuch**, rechts das Publisher-Set „Endabgabe Export" öffnen.
9. Beide Layouts „Titelseite" und „Grundrisse-Schnitte-Ansichten" per Drag&Drop ins Set ziehen → werden mit PDF-Symbol angezeigt.
10. Organisator schließen; beide Pläne im Publisher markieren → unten Dateiformat (A) wählen; bei Bedarf Dokument-Optionen (B) einstellen.

#### 10.3 Pläne publizieren
1. Vor dem ersten Publizieren Speicherort festlegen: Rechtsklick auf ein Publisher-Element → **Einstellungen**.
2. Schaltfläche **Suchen…** → lokales Dateisystem wählen.
3. Zum Speicherort navigieren → **Auswählen** → Publisher-Set-Einstellungen mit **OK** bestätigen.
4. Vor dem Publizieren auswählen, welches Layout publiziert werden soll.
5. Schaltfläche **Publizieren** klicken.
- Ergebnis: Layouts werden in eine PDF-Datei gespeichert; ein **Abschlussbericht** zeigt Erfolg/Misserfolg.

#### Verknüpfungen (Layout-Untergruppen im Publisher)
- Neben Layouts können auch Untergruppen aus dem Layoutbuch hinzugefügt werden. Zwei Methoden:
- **A: Drag&Drop** — Untergruppe per Drag&Drop ins Publisher-Set ziehen → erstellt einen Ordner, der NICHT mit der Layoutbuch-Untergruppe verknüpft ist. Der Ordner enthält nur die zum Zeitpunkt vorhandenen Pläne; später hinzugefügte Layouts erscheinen NICHT automatisch. Einzelne Elemente aus dem Publisher-Ordner löschbar.
- **B: Verknüpfung erstellen** — Layoutbuch links, Publisher-Set „Endabgabe Export" rechts anordnen; Untergruppe „Endabgabe" wählen (1) → Schaltfläche **Verknüpfung erstellen (2)** → erzeugt im Set einen verknüpften Ordner (3). Erkennbar an kleinem schwarzem Pfeil + bläulicher Einfärbung des Ordner-Symbols. Alle Änderungen an der Untergruppe (Hinzufügen/Entfernen von Layouts) werden automatisch in den verknüpften Publisher-Ordner übernommen.

#### Verzeichnisstruktur erstellen
- Pläne im Publisher-Set mit Ordnern/Unterordnern so sortieren, wie sie auf dem Rechner erscheinen sollen (z. B. je ein Ordner „PDF" und „DWG", beide Pläne im entsprechenden Format hinzufügen). Nach **Publizieren** wird dieselbe Ordnerstruktur am Rechner erzeugt.
- Voraussetzung: in den Publisher-Set-Einstellungen Option **Verzeichnisstruktur beibehalten/erzeugen** aktivieren.
- **Pläne in einer PDF-Datei zusammenfassen:** PDFs verschiedener Blattformate in einer Datei sicherbar. Ordner „PDF" im Publisher wählen → Option **In einer PDF-Datei zusammenführen** aktivieren (Ordner-Symbol ändert sich).

#### 10.4 Pläne drucken
- Drucken ohne vorheriges PDF-Publizieren möglich, direkt aus Archicad.
- Befehle **Drucken…** und **Plotten…** im Menü **Ablage**; dort auch Einstellungen (z. B. Papierformat).
- Alternativ über den Publisher drucken/plotten: in den Publisher-Set-Einstellungen Ausgabeform **Drucken** oder **Plotten** wählen; weitere Einstellungen im Bereich **Format**.

### 11 Hilfe
- **Archicad Hilfe:** Menü **Hilfe > Archicad Hilfe**. Online → Help Center (Filme, Artikel, Handbücher); offline → interne Archicad Hilfe (muss bei Installation mitinstalliert werden). Suchfunktion empfohlen. Kontexthilfe per Rechtsklick auf Schaltflächen/Einstellungsfenster → Befehl **Hilfe (MAC)** bzw. **Was ist das? (WIN)** → führt zum passenden Online-Handbuch-Artikel.
- **Archicad Forum:** deutschsprachiges Anwenderforum, rund um die Uhr kostenlose Hilfe von Anwendern, GRAPHISOFT-Mitarbeitern/-Partnern. URL: https://forum.graphisoft.de/ . Unterforum „Tutorials" mit Anleitungsfilmen.
- **WILDCADS-Kurstermine für Tutor:innen:** https://wildcads.graphisoft.de/archicad-kurse-und-workshops/
- **Kurstermine für Lehrende:** https://graphisoft.com/de/studium-und-ausbildung/dozenten-und-lehrkraefte/schulungen-dozenten und .../at/...
- **Onlinekurse für Studierende:** kostenlos, Datei herunterladen, mit Archicad-Studentenversion öffnen. https://wildcads.graphisoft.de/support-und-schulung/archicad-onlinekurse/
- **BIMcloud für Studierende (wildcads.bimcloud):** Team-Bearbeitung von Archicad-Projekten, serverseitige Speicherung, ortsunabhängig. Laufzeit **1–2 Semester**. Voraussetzung: Internetverbindung + Archicad-Bildungsversion. https://wildcads.graphisoft.de/wildcads-bimcloud/
- **Archicad YouTube-Kanal:** https://www.youtube.com/user/PMGraphisoft

#### GRAPHISOFT Support
- **Für Lehrende und Archicad-Tutor:innen** (kostenfreier Telefon-Support):
  - Deutschland: **0800 0 478255**
  - Österreich: **0800 010 200**
  - Hotline-Zeiten: Mo–Do **8.00–18.00 Uhr**, Fr **8.00–15.00 Uhr**.
- **Für Studierende und Schüler:innen** (kostenpflichtiger Hotline-Support, dringende Fälle):
  - Deutschland: **0900 547 8255** (0,99 €/Min. aus dem deutschen Festnetz)
  - Österreich: **0900 410 242** (1,36 €/Min. aus dem österreichischen Festnetz)
  - Hotline-Zeiten: Mo–Do **10.00–12.00 Uhr und 14.00–16.00 Uhr**, Fr **10.00–12.00 Uhr und 13.30–15.00 Uhr**.
- Support nur für **Archicad 25–26**; ältere Versionen ausgeschlossen. Technischer Support leistet keine Telefon-Schulung — vorab Handbuch/Forum/Help Center/Schulungsunterlagen prüfen.
- Hinweis: Für Anrufe aus Mobilfunknetzen werden bis auf Weiteres keine 0900-/0180x-Rufnummern angeboten (keine garantierte Kostenfreiheit in der Warteschleife).

### 12 Notizen
- Seiten 136–137: leere Notizenseiten (kein Fachinhalt).

---
**Relevanz für ElektroPlaner:** gering bis keine. Einziger praktisch verwertbarer Punkt: Archicad kann Layouts/Pläne über den Publisher in den Formaten **PDF, DWG, DXF und JPEG** exportieren (DXF/DWG-Schnittstelle relevant für CAD-Austausch). Keine ÖNorm-, OVE-, Höhen-, Querschnitts- oder Schutzbereichsangaben enthalten.
