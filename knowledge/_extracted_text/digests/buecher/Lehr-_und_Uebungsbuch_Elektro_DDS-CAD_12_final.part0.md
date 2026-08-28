# Lehr-_und_Uebungsbuch_Elektro_DDS-CAD_12_final — Teil 0
> Quelle: Lehr-_und_Uebungsbuch_Elektro_DDS-CAD_12_final (buecher) · dieser Teil.

> **Charakter des Dokuments:** Lehr- und Übungsbuch für die CAD-Software **DDS-CAD 12** (Data Design System GmbH), gerichtet an Lehrende/Bildungsstätten. Es beschreibt **Software-Neuerungen von Version 12 gegenüber Version 11** plus Schritt-für-Schritt-Übungen. Es ist **kein Normen-/Fachliteratur-Dokument** — es enthält **keine ÖNorm-/OVE-Maße, Schutzbereiche, Höhen oder Abstände**. Der einzige konkrete Zahlenwert ist ein Beispiel-Fußbodenaufbau (0,12 m → 0,2 m). Maschinen-Regeln nach Norm-Schema sind daher nahezu nicht vorhanden (siehe unten).

## Inhalt

### Vorwort — "Effizient lernen – effizient planen" (S. 2)
- DDS-CAD 12 als intuitives Planungswerkzeug; Lehr- und Übungsbuch fasst alle Neuerungen von DDS-CAD 12 zusammen, ergänzend zu praktischen Unterrichtsübungen.
- Herausgeber: DDS-Bildungsstättenteam.

### Inhaltsverzeichnis (S. 3) — Seitenanker
- Bemaßung — S. 4
  - Bemaßungstext anpassen — S. 4 (Übung S. 5)
  - Einstellungen für Bemaßungsformate — S. 5 (Übung S. 6)
  - Einstellungen für Einheitenformate — S. 6 (Übung S. 7)
- Modell analysieren — S. 8
  - Meldungen — S. 8
  - Kollisionsprüfung — S. 9 (Übung S. 10)
- Schnitte und Ausschnitte — S. 12
  - Vorlagen für Layouts — S. 12
- Artikeldatenbank — S. 13
  - Elektromobilität — S. 13 (Übung S. 13)
- Verteilerdokumentation — S. 15
  - Seitenumbruch für Stromkreise — S. 15 (Übung S. 15)
  - Brandschutzschalter — S. 17 (Übung S. 17)
- Elektroinstallation — S. 18
  - Abstand zu einer Referenz festlegen — S. 18
  - Symbole neu ausrichten — S. 19 (Übung S. 19)
  - Umgang mit unterschiedlichen Kabeleigenschaften in Verteiler und Arbeitsmodell — S. 21
  - Kabelsegmente bearbeiten — S. 22
  - Kabeleigenschaften bei schreibgeschütztem Verteiler anpassen — S. 23
  - Etagenübergreifende Kabelverlegung — S. 24 (Übung S. 25)
  - Umfassende Rahmendarstellungen — S. 27
  - Objekte nummerieren lassen — S. 28 (Übung S. 29)
  - Erweiterung der Legende um Verlegesysteme — S. 30
- Reporte — S. 31
  - Die Report-Vorschau — S. 31 (Übung S. 32)
- Schemata — S. 33
  - Automatische Systeme — S. 33 (Übung S. 34)

### Bemaßung (S. 4–7)

**Bemaßungstext anpassen (S. 4)**
- DDS-CAD 12 erweitert die bereits vorhandenen Möglichkeiten zur Anpassung des Bemaßungstextes.
- Möglichkeiten: Überschreiben der Maßangabe; ergänzenden Text hinzufügen; vorhandene Maßangabe ersetzen.
- Zusatztext wird im Eingabefeld **‚Bemaßungstext‘** eingegeben.
- Textposition über Dropdown-Menü **‚Text-Position‘**: **‚Über‘, ‚Unter‘, ‚Vor‘, ‚Hinter‘**.
- Schriftgröße der Bemaßung: in DDS-CAD 11 nur projektübergreifend einstellbar; DDS-CAD 12 erlaubt **pro Bemaßungsangabe eine andere Schriftgröße**.

**Übung Bemaßungstexte (S. 5):**
- Steckdose platzieren, ‚Bemaßung‘ erstellen.
- Doppelklick auf Bemaßungstext → Eigenschaften.
- Dropdown ‚Text-Position‘ anpassen.
- ‚Ersetzen‘ wählen, wenn Maßangabe durch Text ersetzt werden soll.
- Dialog ‚Bemaßungstext‘ schließen; Doppelklick auf Bemaßungslinie → Dialog ‚Bemaßung‘.
- Haken aus Checkbox **‚Von Textstil‘** entfernen; Wert in ‚Schriftgröße‘ eingeben.
- Änderung des Fonts ‚Textstil 1‘ wird ignoriert, die eingegebene Schriftgröße wird verwendet.

**Einstellungen für Bemaßungsformate (S. 5–6)**
- DDS-CAD 11: projektspezifische Bemaßungsformate erzeugbar.
- DDS-CAD 12: geänderte Bemaßungsformate als **Voreinstellung für alle neuen Projekte** speicherbar.
- Übung (S. 6): Menüzeile ‚Extras‘ → ‚Optionen‘ → ‚Einstellungen für Bemaßungsformate‘ öffnen → anpassen → Button **‚Einstellungen als Vorlage für neue Projekte speichern‘**.

**Einstellungen für Einheitenformate (S. 6–7)**
- DDS-CAD 11: Einheitenformate nur für aktives Projekt änderbar.
- DDS-CAD 12: angepasste Einheitenformate auf alle neuen Projekte übertragbar.
- Übung (S. 7): ‚Extras‘ → ‚Optionen‘ → ‚Einstellungen für Einheitenformate‘ → anpassen → Button ‚Einstellungen als Vorlage für neue Projekte speichern‘.

### Modell analysieren (S. 8–11)

**Meldungen (S. 8–9)**
- Ab DDS-CAD 12 werden alle modellrelevanten Informationen im Dialog **‚Meldungen‘** aufgelistet.
- Einträge-Typen: **‚Fehler‘, ‚Warnungen‘, ‚Mitteilungen‘, ‚Kollisionen‘**.
- Konflikte (z. B. Kollisionen oder offene Enden) werden sofort erkannt; Korrektur direkt aus dem Meldungsfenster möglich.
- Überprüfung erfolgt **gewerkeübergreifend** für das aktive Modell.
- Plausibilitäts- und Kollisionsprüfungen auch **etagenübergreifend** ausführbar.
- Konflikt in anderem Modell über Kontextmenü direkt aufrufbar → Modell wird geöffnet, Konflikt herangezoomt.
- Angeklickte Meldung wird als „Gelesen“ markiert (Schrift nicht mehr fett); Rechtsklick → Meldungen löschen.
- Angezeigte Spalten/Infos im Dialog: **Gewerk, Beschreibung, Modellname, Raum, Medium, Zeitstempel**.
- Filter-Buttons: Fehler / Warnungen / Mitteilungen / Kollisionen (per Klick aktivieren/deaktivieren).
- Dialog ‚Meldungen‘ standardmäßig aktiviert; deaktivieren/aktivieren über Menüzeile ‚Fenster‘ → ‚Symbolleisten‘.

**Kollisionsprüfung (S. 9–11)**
- Prüft Modell auf Kollisionen, z. B. Rohre gegen Kanäle eingeblendeter Ebenen.
- DDS-CAD 12 erweitert: Prüfung gegen **jedes Bauteil und Objekt**, insbesondere gegen Bauteile eines eingelesenen **IFC-Modells**.
- Prüfung kann durch Angabe von **Abstandswerten** Kollisionen auch im Umkreis erkennen (Beispiel: Steckdose hinter einem Heizkörper geplant).
- Vorgefertigte Konfigurationen verfügbar; kopierbar, individuell anpassbar, speicherbar, löschbar.
- Selbst angelegte Konfigurationen stehen in **allen Projekten** zur Verfügung.
- Aufruf: Menü ‚Extras‘ → ‚Modell analysieren‘; gewünschte Konfiguration wählen → ‚Ausführen‘.
- Ergebnisse erscheinen im Meldungsfenster unter Reiter ‚Kollision‘.
- **HINWEIS (S. 10):** Funktion **‚OpenGL-Modus‘ muss aktiv sein**, um vollen Funktionsumfang zu nutzen.
- Übung (S. 10): Dialog ‚Kollisionsprüfung‘ → ‚+‘ (Neu) → Name vergeben → ‚OK‘ → Checkboxen setzen für zu prüfende Bauteile/Objekte.

### Schnitte und Ausschnitte (S. 12)

**Vorlagen für Layouts**
- Aus Schnitten und Ausschnitten können Vorlagen für Plot-Layouts generiert werden.
- Bis Version 11: nach Erzeugen eines Schnitts/Ausschnitts musste Vorlage manuell erstellt werden.
- DDS-CAD 12 erzeugt diese **automatisch** nach Erstellen von Ausschnitten und Schnitten; erscheinen direkt im **DDS-Explorer**.

### Artikeldatenbank (S. 13–14)

**Elektromobilität (S. 13)**
- DDS-CAD 12: in Artikelgruppe **‚Dose/Kasten/Hilfsobjekt‘** neue Auswahlmöglichkeit **‚Elektromobilität‘**.
- Zusätzlich zu DDS-Artikeln: Herstellerdatenbank **‚MENNEKES‘** hinzugefügt (manuell hinzuladbar).
- Übung (S. 13): ‚Extras‘ → ‚Herstellerdatenbank laden‘ → Doppelklick auf ‚MENNEKES‘ → ‚OK‘ → separater Eintrag ‚MENNEKES‘ in Artikelgruppe ‚Dose/Kasten/Hilfsobjekt‘.

### Verteilerdokumentation (S. 15–17)

**Seitenumbruch für Stromkreise (S. 15–16)**
- Stromkreise in DDS-CAD 12 intuitiver auf nachfolgende Seite verschiebbar → durch Seitenumbruch.
- Übung (S. 15): Im Stromlaufplan Stromkreis markieren → Kontextmenü (Rechtsklick) → **‚Seitenumbruch vor dem Stromkreis einfügen‘**.
- Entfernen: Stromkreis markieren → Kontextmenü → **‚Seitenumbruch vor dem Stromkreis entfernen‘**.

**Brandschutzschalter (S. 17)**
- DDS-CAD 12: **Brandschutzschalter** in Artikeldatenbank hinzugefügt.
- Kann zu jeder bestehenden Sicherung für die Darstellung im **allpoligen Stromlaufplan** als **Hilfsfunktion** hinzugefügt werden.
- Übung (S. 17): in ‚Stromkreisliste‘ Stromkreis wählen → Doppelklick auf Sicherung → Dialog ‚Bauteil‘ → ‚Hilfsfunktion‘ → Brandschutzschalter wählen → alle Dialoge mit ‚OK‘ → Brandschutzschalter ist Sicherung zugewiesen und in Verteilerdokumentation sichtbar.

### Elektroinstallation (S. 18–30)

**Abstand zu einer Referenz festlegen (S. 18)**
- Ab DDS-CAD 12: oberer oder unterer Abstand der **Einbauhöhe** von Objekten zu einer Referenz eingebbar.
- Bei Änderung von Referenzen (z. B. Fußbodenhöhe oder Deckenhöhe) wird der Abstand zu den Objekten **beibehalten**.
- Funktion **‚Höhe sperren‘**: Objekt bleibt nach Referenzänderung auf seiner vorherigen Einbauhöhe → der vorher definierte Abstand zur Referenz ändert sich dadurch.
- Bei Änderung der Referenz **‚Fertigfußboden (OKFF)‘** behalten alle Objekte den Abstand zur Referenz → korrekte Einbauhöhe.
- Beispiel: im rechten Raum ‚Fußbodenaufbau‘ von **0,12 m auf 0,2 m** geändert; im linken Raum keine Änderung.

**Symbole neu ausrichten (S. 19–20)**
- DDS-CAD 11: Objekte auf Linie einfügbar, spätere Änderungen nur über Umwege.
- DDS-CAD 12: völlig neue Funktion zur Objektausrichtung → effizienteres Neuausrichten.
- Beispiel: Wandauslassleuchten auf einer Wand platziert; nach Löschen einzelner Objekte Neuausrichtung möglich.
- Übung (S. 19–20): Objekte auf Linie platzieren, einzelne löschen → zu verschiebende Objekte markieren → Rechtsklick → ‚Ausrichtung‘ → **‚Gleichmäßig horizontal‘** → Objekte werden neu ausgerichtet.

**Umgang mit unterschiedlichen Kabeleigenschaften in Verteiler und Arbeitsmodell (S. 21)**
- DDS-CAD 11: Änderung von Kabeleigenschaften in Installationszeichnung und Verteilerdokumentation möglich, aber beim Öffnen der Installationszeichnung nur Info-Anzeige, kein Eingreifen.
- DDS-CAD 12: Dialog ‚Meldungen‘ erlaubt Wahl, ob Änderungen aus der Verteilerdokumentation übernommen oder bestehende Eigenschaften der Installationszeichnung beibehalten werden.
- Übernehmen: im Fenster ‚Meldungen‘ auf Beschreibung mit Verteilersymbol klicken → Kontextmenü → **‚Kabeleigenschaften übertragen: Stromkreisliste -> Installiertes Kabel‘**.

**Kabelsegmente bearbeiten (S. 22–23)**
- DDS-CAD 11: Kabelsegmente nicht losgelöst vom ‚Zuleitungskabel‘ veränderbar; Änderung an einem Segment wirkte auf komplettes gezeichnetes Kabel.
- DDS-CAD 12: Eigenschaften von Segmenten anpassbar ohne ‚Zuleitungskabel‘ oder Abzweige zu ändern.
- Beispiel: Brückenkabel in Leerrohr einziehen → Doppelklick auf Kabel → Checkbox **‚Leerrohr‘** aktivieren → ‚OK‘ → Folgeabfrage mit ‚Ja‘ bestätigen. DDS-CAD 12 fragt bei weiterer Änderung nicht erneut nach.

**Kabeleigenschaften bei schreibgeschütztem Verteiler anpassen (S. 23)**
- DDS-CAD 12: Ändern von Kabeleigenschaften in Installationszeichnung jederzeit möglich, auch bei geöffneter Verteilerdokumentation.
- Schreibschutz des Verteilers bleibt im Kabel-Dialog sichtbar; Editieren dennoch möglich; Änderungen werden im Dialog ‚Meldungen‘ gelistet.

**Etagenübergreifende Kabelverlegung (S. 24–26)**
- DDS-CAD 12: **kein Hilfssymbol mehr nötig**; Verlegung so intuitiv wie Kabeltrassenplanung.
- Kabel/Kabelstrang im Kontextmenü in oberer oder unterer Etage beendbar.
- Ermöglicht korrekte **Steigetrassenbelegung** in allen Etagen bei voller **Spannungsfall- und Längenkontrolle**.
- Neue Symbole für Übergabepunkte (Kabelstrang links / Kabel rechts); Farbdarstellung der Übergabepunkte ändert sich nach Übernahme/Beenden.
- In Kabeleigenschaften: **Gesamtlänge** überprüfbar, auch wenn Teilstrecken auf mehreren Etagen liegen.
- **Stückliste** erfasst nach wie vor **nur Kabel, die im Arbeitsmodell geplant** wurden.
- Übung (S. 25–26): Kabel ‚Zeichnen‘ aus Verteiler starten (alternativ Kabelstrang) → Linksklick auf Fixpunkt am Übergabepunkt → Kontextmenü → ‚In der oberen Etage beenden‘ bzw. ‚In der unteren Etage beenden‘ → ‚ESC‘ → erzeugtes Symbol anklicken → ‚Etage öffnen und Zoom auf Übergabepunkt‘ → Übergabepunkt mit Linksklick markieren → ‚Kabelstrang/Kabel aus der unteren Etage weiterführen‘ → zum Zielpunkt verlegen → ‚ESC‘.

**Umfassende Rahmendarstellungen (S. 27)**
- DDS-CAD 12: umfassende Rahmendarstellungen zur Anzeige von Informationen an Objekten, z. B. **Meldergruppe und -nummer für BMA-Multisensoren**.
- An aktuelle Normen angepasst (Normen nicht namentlich genannt).
- Rahmenauswahl beim klassischen Symboltext und bei der Nummerierung verfügbar.

**Objekte nummerieren lassen (S. 28–29)**
- Funktion **‚Symbolnummerierung‘**: Objekten eine Nummer zuweisen.
- DDS-CAD 12: alle vergebenen Nummern anzeigbar; Neusortierung per Drag & Drop.
- Anwendbar bei allen Objekten mit aktivierter Nummerierung, z. B. **Steckdosen, Leuchten, Datendosen**.
- Übung (S. 29): platziertes Objekt markieren → Kontextmenü → ‚Markierten Typ aus Bereich filtern‘ → alle umzunummerierenden Objekte markieren → Kontextmenü → ‚Neu nummerieren‘ → Einträge per Drag & Drop verschieben → Kontextmenü → ‚Alle neu nummerieren‘.

**Erweiterung der Legende um Verlegesysteme (S. 30)**
- Alle in einem Drucklayout sichtbaren Objekte können in einer Legende gelistet werden.
- DDS-CAD 12: Legendeninhalte um **Verlegesysteme** erweitert; Verhalten identisch zu Objekten im Installationsplan — sobald im Drucklayout sichtbar, in ‚Legende‘ gelistet.

### Reporte (S. 31–32)

**Die Report-Vorschau (S. 31)**
- Reporte ermöglichen detaillierte Auflistung von Informationen.
- Ab DDS-CAD 12: Vorschau zeigt Inhalte und erlaubt Darstellungsanpassungen; **Deckblatt mit projektrelevanten Informationen** zu jedem Report hinzufügbar.
- Button **‚Reporte‘** in allen Dialogen, in denen ein Report aufrufbar ist — bis Version 11 hieß dieser Button **‚Drucken‘**.
- Übung (S. 32): Zeichnung öffnen → Symbolleiste ‚Stückliste erstellen‘ → ‚Reporte‘ → Report wählen und Inhalt bestimmen → in PDF exportieren bzw. an Drucker senden.

### Schemata (S. 33–35)

**Automatische Systeme (S. 33–35)**
- Highlight Version 12: **automatische Schemaerstellung** verschiedener Systeme aus einer Installationszeichnung.
- Automatische Schemazeichnungen für folgende Systeme:
  - Brandmelde-Systeme
  - Datennetzwerk-Systeme
  - Energieversorgungs-Systeme
  - Sicherheitsbeleuchtungs-Systeme
- In generierte Schemazeichnungen werden übernommen/angezeigt: **Etagen, Raumnamen, Stromkreisnummern, ggf. vorhandene Nummerierungen**.
- Möglich: Verschieben von Objekten und Ergänzen zusätzlicher Informationen.
- Registerkarte **‚Systeme‘** im Dockingfenster: informiert über aktuelles System, alle Objekte und Kabelverbindungen; Objekte/Kabelverbindungen per Klick auf das Auge aus-/anschaltbar.
- Übung (S. 34–35): Dockingfenster Registerkarte ‚Systeme‘ wählen (falls nicht verfügbar: ‚Fenster‘ → ‚Symbolleisten‘ → ‚Systeme‘ aktivieren) → System wählen (z. B. ‚Brandmelde-System‘) → Kontextmenü → ‚Schema generieren‘ → Speicher-Abfrage mit ‚Ja‘ bestätigen → DDS-CAD schlägt neuen Zeichnungsnamen vor (Beispiel ‚05‘; restliche Namensteile an DDS-CAD-Namenskonvention gebunden, nicht änderbar) → optional Kommentar im Feld ‚Beschreibung‘ → ‚OK‘ → Schemazeichnung wird geöffnet.
- **HINWEIS (S. 35):** Automatische Schemagenerierung steht **ausschließlich in der Lizenz E-11** zur Verfügung.

### Kontakt / Impressum (S. 36)
- **Deutschland:** Data Design System GmbH, Lüdinghauser Straße 3, 59387 Ascheberg. T +49 2593 8249 0 · E lehrende@dds-cad.de · W www.dds-cad.de
- **Österreich:** Data Design System GmbH, Kornstraße 8/1, 4060 Leonding. T +43 732 672 800 · E lehrende@dds-cad.at · W www.dds-cad.at
- DDS ist Mitglied der Open-BIM-Initiative.

## Maschinen-Regeln

> Hinweis: Dieses Dokument ist ein Software-Tutorial ohne Norm-Vorgaben. Es enthält keine ÖNorm/OVE-Höhen, -Abstände oder -Schutzbereiche. Nur ein konkreter Maßwert (Beispiel-Fußbodenaufbau) und einige produkt-/funktionsbezogene Fakten sind extrahierbar.

- [HÖHE] Beispiel-Fußbodenaufbau im Schulungsprojekt von 0,12 m auf 0,2 m geändert; Objekte behalten bei Referenzänderung den Abstand zur Referenz ‚Fertigfußboden (OKFF)‘ und damit die korrekte Einbauhöhe (DDS-CAD 12, S. 18).
- [ABSTAND] Einbauhöhe von Objekten als oberer/unterer Abstand zu einer Referenz definierbar; Funktion ‚Höhe sperren‘ hält die absolute Einbauhöhe konstant, wodurch sich der Abstand zur Referenz ändert (DDS-CAD 12, S. 18).
- [ABSTAND] Kollisionsprüfung erkennt durch Angabe von Abstandswerten Kollisionen auch im Umkreis von Objekten (Beispiel: Steckdose hinter Heizkörper) (DDS-CAD 12, S. 9).
- [DEFINITION] Brandschutzschalter = Hilfsfunktion, die zu einer bestehenden Sicherung hinzugefügt und im allpoligen Stromlaufplan dargestellt wird (DDS-CAD 12, S. 17).
- [DEFINITION] ‚Elektromobilität‘ = neue Auswahlmöglichkeit in der Artikelgruppe ‚Dose/Kasten/Hilfsobjekt‘; Herstellerdatenbank MENNEKES manuell zuladbar (DDS-CAD 12, S. 13).
- [DEFINITION] Stromkreis-Seitenumbruch = Verschiebung eines Stromkreises auf die nächste Seite des Stromlaufplans via Kontextmenü ‚Seitenumbruch vor dem Stromkreis einfügen/entfernen‘ (DDS-CAD 12, S. 15).
- [DEFINITION] Automatische Schemaerstellung für 4 Systemtypen: Brandmelde-, Datennetzwerk-, Energieversorgungs- und Sicherheitsbeleuchtungs-Systeme; übernimmt Etagen, Raumnamen, Stromkreisnummern, Nummerierungen (DDS-CAD 12, S. 33).
- [PFLICHT] Für den vollen Funktionsumfang der Kollisionsprüfung muss der ‚OpenGL-Modus‘ aktiv sein (DDS-CAD 12, S. 10).
- [PFLICHT] Automatische Schemagenerierung nur in Lizenz E-11 verfügbar (DDS-CAD 12, S. 35).
- [STROMKREIS] Etagenübergreifende Kabelverlegung erlaubt korrekte Steigetrassenbelegung in allen Etagen bei voller Spannungsfall- und Längenkontrolle; Gesamtlänge auch über mehrere Etagen prüfbar; Stückliste erfasst nur im Arbeitsmodell geplante Kabel (DDS-CAD 12, S. 24–25).
- [LEITUNG/QUERSCHNITT] Kabelsegmente einzeln anpassbar ohne Zuleitungskabel/Abzweige zu ändern; einzelnes Segment (z. B. Brückenkabel) per Checkbox ‚Leerrohr‘ als in Leerrohr eingezogen kennzeichenbar (DDS-CAD 12, S. 22).
- [SYMBOL] Umfassende Rahmendarstellungen zeigen Informationen an Objekten, z. B. Meldergruppe und -nummer für BMA-Multisensoren; an aktuelle Normen angepasst (Normen nicht benannt) (DDS-CAD 12, S. 27).
- [SYMBOL] Symbolnummerierung verfügbar für Objekte wie Steckdosen, Leuchten, Datendosen; Neusortierung per Drag & Drop (DDS-CAD 12, S. 28).
