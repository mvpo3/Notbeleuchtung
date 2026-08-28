# AC 26 Grundkurs — Teil 0
> Quelle: AC 26 Grundkurs (buecher) · Seiten 1-40.

Dieses Dokument ist die **GRAPHISOFT Archicad 26 Grundkurs**-Kursunterlage ("BIM orientierte Planung"), ein reines **CAD-Software-Tutorial** für die BIM-Architekturmodellierung — *kein* elektrotechnisches Norm-Dokument (keine ÖNorm/OVE-Inhalte). Teil 0 (S. 1-40) deckt ab: Inhaltsverzeichnis, BIM-Grundlagen, Benutzeroberfläche, Element-Auswahl, Zauberstab, Tastaturkürzel, Projektstart/Geschosseinstellungen sowie den Beginn der 3D-Modellierung (Wände und Decken). Relevanz für ElektroPlaner: Geschosslogik, Bauteil-Höhenkonventionen (OKFF/OKRD, Rohdecke/Bodenaufbau), Referenzlinien-Logik der Wände und Export-Formate (DWG/DXF) — nützlich zum Verständnis, wie Architektur-DXFs entstehen, die als Input dienen.

## Inhalt

### Dokument-Rahmen
- Titel: "ARCHICAD 26 GRUNDKURS — BIM ORIENTIERTE PLANUNG"; Herausgeber GRAPHISOFT Deutschland GmbH, Landaubogen 10, 81373 München.
- Copyright © 2022 GRAPHISOFT; nur für zertifizierte Archicad Tutor:innen/Lehrende an eigene Kursteilnehmer:innen weitergebbar ("Nur für Kursteilnehmer, Weitergabe an Dritte nicht zulässig!").
- Warenzeichen: Archicad (eingetragen), Virtual Building, GDL (Warenzeichen von GRAPHISOFT).
- Gesamtumfang 137 Seiten. Gliederung in Teile A (Grundlagen), B (Modellierung), C (Darstellung), D (Pläne erstellen).

### Inhaltsverzeichnis (Struktur, mit Seitenzahlen)
- **Teil A: Die Grundlagen** (S. 6): 1 Archicad Grundlagen — 1.1 Arbeitsweise (6), 1.2 Benutzeroberfläche (8), 1.3 Konstruktionselemente (11), 1.4 Auswählen (12), 1.5 Zauberstab (16), 1.6 Tastaturkürzel (16).
- **Teil B: Modellierung** (S. 17): 2 Über das Projekt (17); 3 Start ins Projekt — 3.1 Neues Projekt (18), 3.2 Projektpräferenzen (20), 3.3 Geschosseinstellungen (20); 4 3D-Gebäudemodell — 4.1 Wände (23), 4.2 Decken (37), 4.3 Schnitte/Ansichten (42), 4.4 Dach (46), 4.5 Fenster/Türen/Fassade (50), 4.6 Treppe/Geländer (62), 4.7 Möblierung (69), 4.8 Räume (72), 4.9 Bemaßung (78).
- **Teil C: Darstellung** (S. 81): 5 Grundlagen — 5.1 Darstellungs-Schnell-Optionen (81), 5.2 Ebenenkombination (82), 5.3 Stift-Set (84), 5.4 Modelldarstellung (87), 5.5 Grafische Überschreibung (89); 6 Schnitte/Ansichten — 6.1 Einstellungen (93), 6.2 Staffage (95), 6.3 Beispiele (99); 7 3D-Darstellungen/Arbeitsblätter — 7.1 3D-Fenster (100), 7.2 3D-Schnitte (101), 7.3 3D-Dokumente (103), 7.4 Arbeitsblätter (104).
- **Teil D: Pläne erstellen** (S. 107): 8 Ausschnitte — 8.1 Allgemeines (107), 8.2 Erstellen/Bearbeiten (108); 9 Planlayouts — 9.1 Vorbereitung (115), 9.2 Masterlayout (116), 9.3 Layout (119), 9.4 Layoutbuch ordnen (120), 9.5 Inhalte (121), 9.6 Zeichnungen ausrichten (123), 9.7 Druck-Vorbereitung (126); 10 Exportieren/Drucken — 10.1 Publisher (127), 10.2 Publisher-Set (127), 10.3 Publizieren (129), 10.4 Drucken (132); 11 Hilfe (133); 12 Notizen (136).

### BIM-Grundlagen und Arbeitsweise (Kap. 1.1)
- BIM = Building Information Model: keine Software, sondern Planungs-/Arbeitsmethode; Grundlage ist ein digitales Gebäudemodell aus **3D-Bauteilen**, die Eigenschaften (Material, Dimension, Kosten) tragen und bei Änderungen automatisch aktualisiert werden.
- EU-Staaten fordern BIM-Einsatz für Planung/Umsetzung aller **öffentlichen Bauprojekte**.
- Kerngrundsatz: "Das Gebäude wird so modelliert, wie es gebaut wird" — Archicad simuliert das Bauen (Wände, Decken, Dächer etc.). Alle Pläne (Grundrisse, Schnitte, Ansichten, Perspektiven, Mengen, Stücklisten, Raumbücher, Volumen) werden aus dem virtuellen Gebäudemodell generiert.
- Bauelemente werden **geschossweise** zusammengefügt; aus Geschossen → Gebäude → bei Großprojekten Gebäudegruppe. 2D-Ergänzung (Bemaßung, Etiketten) für Dokumentation.
- **Navigator** (rechter Bildschirmrand), vier Reiter:
  - **Projekt-Mappe**: rohes Gebäudemodell inkl. aller generierten Sichten + BIM-Dokumente (Listen, Auswertungen); Darstellungseinstellungen NICHT vordefiniert, übernimmt zuletzt verwendete.
  - **Ausschnitt-Mappe**: vordefinierte Darstellung eines Modell-Teils — legt fest: sichtbare Ebenen, Maßstab, Stift-Set, Bemaßungseinstellungen, Modelldarstellung u.v.m. Ändert nur ANGEZEIGTEN INHALT + ART DER DARSTELLUNG, nicht das Modell selbst.
  - **Layoutbuch**: Pläne mit fester Größe (z.B. DIN A0), befüllt mit Ausschnitten + Plankopf/Beschriftung.
  - **Publisher-Set**: Massen-Export/Druck vieler Layouts; Formate u.a. **PDF, DWG, DXF, JPEG**.

### Benutzeroberfläche (Kap. 1.2)
- Hinweis (österreichische Sprachversion, Arbeitsumgebungsprofil "Profil Architektur 26"): **Transparentpausenpalette** wird nicht angezeigt → über Fenster > Paletten > Transparentpausenpalette aktivieren.
- Paletten/Symbolleisten über Menü **Fenster** ein-/ausblenden.
- **Konstruktionsraster**: Grundeinstellung 1 m × 1 m (graues Raster), Orientierung beim Zeichnen; ein-/ausschalten über Ansicht > Konstruktionsraster darstellen.
- **Rasterfang** (Ansicht > Rasterfang): fängt nur noch Rasterpunkte; normalerweise AUS, nur bei Bedarf ein.
- Paletten per Cursor an Kante vergrößern/verkleinern; Untermenüs durch graues Dreieck gekennzeichnet.
- **Navigation/Maus**: Zoom = Scrollrad; Scrollrad gedrückt halten = Bildschirm verschieben (Cursor → Hand). Empfehlung: Drei-Tasten-Maus, Touchpad abgeraten.
- **3D-Fenster** öffnen: Tab "3D", Shortcut **Strg+3** (WIN) / **Cmd+3** (MAC), oder Doppelklick auf Allgemeine Perspektive/Axonometrie. Befehle unten links: Zoom, Optimieren (alle Elemente sichtbar; **Strg+0**/**Cmd+0**), Orbit (Drehen um Zielpunkt; temporär: Shift + Mausrad drücken/ziehen), Verschieben (Mausrad gedrückt ziehen). Zurück ins 2D: **Strg+2** / **Cmd+2**.
- **Statusanzeige**: horizontale Leiste unten, gibt Hinweise zu nächsten Arbeitsschritten; über Fenster > Paletten > Statusanzeige.
- **Intelligenter Cursor** — Cursorformen:
  - Pfeil-Werkzeug: Auswahl/Aktivierung (weiß = nur Morph-Unterelemente, schwarz = normal).
  - Fadenkreuz: in leerem Bereich.
  - Weißer Bleistift: Zeichnen über freier Stelle.
  - Längsgestreifter Bleistift: Cursor über einer Kante.
  - Dickes Häkchen: auf Knotenpunkt einer Referenzlinie.
  - Schwarzer Bleistift: an Knotenpunkt eines Bauteils.
  - Dünner Mercedesstern: beliebige Kante anderer Elemente.
  - Dicker Mercedesstern: auf Referenzlinie einer Wand / Referenzachse eines Unterzugs.

### Konstruktionselemente (Kap. 1.3)
- Virtuelles Gebäude besteht aus Konstruktionselementen (Wände, Decken, Dach, Fenster …); jedes hat ein eigenes Werkzeug.
- **Werkzeug-Grundeinstellungen** öffnen: Werkzeug wählen + Einstellungsdialog im Infofenster links oben (A) ODER Doppelklick aufs Werkzeug (B). Ganz unten wird die **Ebene** festgelegt (logische Trennung/Ordnung der Modell-Elemente).

### Element-Auswahl (Kap. 1.4)
- **Pfeil-Werkzeug**: Auswahl/Aktivierung; zurück zum Pfeil mehrfach **Esc** oder Taste **P**.
- Bauteil aktivieren: Klick auf Kante/Eckpunkt → wird grün. Mehrfachauswahl: **Shift** gedrückt halten.
- **Schnellauswahl** (Magnet-Symbol): aktiviert → Bauteil an beliebiger Stelle markierbar; deaktiviert → nur an Außenkanten/Eckpunkten. Meist dauerhaft AN. Temporär deaktivieren: **Leertaste** gedrückt halten (hilfreich, um nicht ungewollt Decken/Schraffuren im Hintergrund zu greifen).
- **Tab-Taste** (links neben Q): bei mehreren übereinanderliegenden Elementen das gewünschte wählen (Magnet/Schnellauswahl muss aktiv sein); Linksklick wählt das hervorgehobene aus. Deaktivieren: in leeren Bereich klicken oder Esc.
- **Auswahl in 3D**: gewünschte Elemente aktivieren, dann Strg+3/Cmd+3 → nur aktivierte sichtbar. Kontextmenü: "Auswahl/Markierungsrahmen im 3D anzeigen" bzw. "Alles in 3D anzeigen".
- **Auswahlrahmen**: Pfeil-Werkzeug aktivieren → außerhalb der Gruppe klicken → Cursor nach unten rechts ziehen (Rahmen) → Klick bestätigt; alle Elemente im Rahmen werden aktiviert.
- **Alle Elemente aktivieren**: Bearbeiten > Alle Elemente aktivieren oder **Strg+A**/**Cmd+A** (auch außerhalb des sichtbaren Bereichs; Pfeil-Werkzeug muss aktiv sein).
- **Alle Elemente einer Werkzeugart**: Werkzeug (z.B. Wand) aktivieren, dann Strg+A/Cmd+A → wählt alle Elemente dieses Werkzeugtyps.
- **Markierungsrahmen** definiert eine Fläche zur Teilbearbeitung/3D-Anzeige (gestrichelte Linie); Abbruch mit Esc. Zwei Einstellungen im Infofenster:
  - **Auswahlmethoden**: dünner Markierungsrahmen = nur aktuelles Geschoss; dicker Markierungsrahmen = alle Geschosse.
  - **Geometriemethoden**: Polygon (freie Form), Rechteck, Gedrehtes Rechteck (beliebiger Winkel).

### Zauberstab (Kap. 1.5) und Tastaturkürzel (Kap. 1.6)
- **Zauberstab**: zeichnet die Form eines vorhandenen Elements nach → neues Element (besonders für Kurven/Kreise). Anwendung: Werkzeug (z.B. Decke) aktivieren + **Leertaste gedrückt halten** → Cursor wird Zauberstab.
- **Tastaturkürzel** werden bei Menü-Aufrufen mit angezeigt; die wichtigsten für Windows/Mac sind als PDF herunterladbar.

### Über das Beispielprojekt (Kap. 2)
- Beispielprojekt basiert auf **Quinta Monroy** (Architekt Alejandro Aravena / Studio ELEMENTAL, Chile; Pritzker-Preisträger), als Open-Source veröffentlicht; im Kurs auf ein fiktives Baufeld im deutschsprachigen Raum übertragen.
- Quinta Monroy = Social-Housing-Projekt, Iquique/Chile: 100 Familien ohne Umsiedelung; Förderung reichte für ~**30 m² Wohnraum/Familie**; Prinzip "Incremental housing" — Erweiterung der anfänglichen 30 m² auf **72 m²**. Dreistöckige Gebäude, je 2 Familien.
- Architekt Aravena: geb. 1967 Santiago de Chile; Büro ELEMENTAL seit 2001 (mit Arteaga, Cerda, Oddó, Torres).

### Projektstart (Kap. 3.1)
- Startfenster-Optionen: Neu…, Suchen…, Teamwork… ; zeigt zuletzt geöffnete Projekte.
- **Projektvorlagen** (deutsche Version, zwei Standard-Vorlagen):
  - **Geschoss OK FF**: Unterkante jedes Geschosses = Oberkante Fertigfußboden.
  - **Geschoss OK RD**: Unterkante jedes Geschosses = Oberkante Rohdecke.
  - Kurs verwendet "01 Archicad Beispiel-Vorlage - Geschoss OK FF.tpl"; österreichische Version: "01 Archicad 26 Vorlage.tpl".
- **Arbeitsumgebungs-Profil**: legt verfügbare Menüs/Werkzeuge + Darstellung fest. Kurs nutzt **Profil Architektur 26**. Nachträglich änderbar: Optionen > Arbeitsumgebung > Profil Anwenden > Profil Architektur 26.

### Projektpräferenzen (Kap. 3.2)
- Menü **Optionen > Projektpräferenzen**: Grundeinstellungen zu Bemaßung, Berechnung, Konstruktion etc. — vor Konstruktionsbeginn prüfen.
- **Arbeitseinheiten**: Einheit für Längen/Winkel. Standard Modellbereich = **Meter**; Layout-Bereich separat einstellbar; gelten projektweit.

### Geschosseinstellungen und -aufbau (Kap. 3.3)
- Modell ist nach Geschossen mit definierter Geschosshöhe organisiert (übereinandergestapelt = Gesamtmodell).
- **Bauteil-Zuordnung zu Geschossen**:
  - Geschoss enthält alle Bauteile von **UK Rohdecke unter** dem aktuellen Geschoss bis **UK Rohdecke über** dem Geschoss.
  - Dachgeschoss: alle Bauteile zwischen UK Rohdecke des darunterliegenden Geschosses und **OK Firstes**.
  - Für Fundamente meist ein eigenes Geschoss empfehlenswert.
- **Höhenkote**: OKFF = 0,00 ODER OKRD = 0,00 (projektübergreifend konsistent halten); im Kursprojekt **OKFF = 0,00**.
- Wände beginnen/enden immer auf **OK Rohdecke** (z.B. -0,10 im aktuellen → -0,10 im darüberliegenden Geschoss). Ausnahme oberstes Geschoss: Wände enden an/über OK First.
- **Geschosshöhen im Kursprojekt** (Planung > Geschosseinstellungen):
  - EG: **2,65 m**
  - OG: **2,65 m**
  - DG: **3,10 m** (über OG einfügen via "Darüber einfügen")
  - Fundamente: **1,50 m**

### Wände — Grundlagen und Erstellung (Kap. 4.1)
- **Wand-Referenzlinie**: dicke blaue Linie bei aktivierter Wand; sichert saubere Verschneidungen (Schraffuren) — Referenzlinien sollten immer aufeinandertreffen. Position bestimmt Oberflächenmaterial Außen-/Innenseite + Fangpunkte/Kanten. Lage festlegen über Infofenster/Teilfenster "Lage der Referenzlinie" oder Taste **C** (zyklisch beim Zeichnen).
- **Außenwände EG** (Doppelklick Wand-Werkzeug):
  - Wandoberkante: verknüpft mit 1.OG, Abstand **-0,10**; Ursprungsgeschoss 0. EG, Abstand **-0,10**.
  - Baustoff: **TRAGENDE BAUTEILE**.
  - Wandstärke: **0,245** m.
  - Ebene: **10 Wand außen**.
  - Erklärung: Außenwände immer OK Rohdecke → OK Rohdecke; stehen auf Rohboden auf, Wandbekleidung über Deckenkante hinweg. Abstand 10 cm wegen geplantem 10 cm Bodenaufbau (OK Rohboden bei -0,10).
- **Geometriemethoden Wand**: per Schaltfläche im Infofenster (kleinen schwarzen Pfeil gedrückt halten → Pop-Up). Außenwände hier: Geometriemethode **Rechteckig**, Referenzlinie **Außen**; Ecken des inneren roten Hilfsrechtecks anklicken. Rotes Hilfsrechteck danach als Polylinie (Tab-Taste durchschalten) auswählen + Entf löschen.
- **Innenwände EG** (nichttragende Trennwände):
  - Oberkante zum 1.OG: Abstand **-0,24** (Bodenaufbau 10 cm + Decke 14 cm → 24 cm unter OG).
  - Baustoff: **BAUTEIL**.
  - Wandstärke: **0,10** m.
  - Ebene: **10 Wand innen**.
- **Abstand-zu-Bezugspunkt-Eingabe**: Cursor auf Innenecke legen (nicht klicken, warten → blauer Kreis = Bezugspunkt), **X**-Taste, Wert (z.B. 1,45) eingeben, dann **"-"-Taste** → Cursor 1,45 m nach links. WICHTIG: Vorzeichen **nach** dem Zahlenwert eingeben (bestimmt Abstand vom Bezugspunkt; ohne Vorzeichen → Abstand zum absoluten Nullpunkt).
- Wandlänge per Tastatur (z.B. "3,6" für 3,6 m), Enter; Referenzlinienlage ggf. mit **C** umstellen; weiterer Abschnitt z.B. "0,7" → Enter, letzten Punkt erneut klicken = fertig.
- **Schacht**: Wanddicke auf **0,15** m ändern; auf Referenzlinien-Position achten.
- **Transparentpause** (für Konstruktion deckungsgleich über unterem Geschoss): Rechtsklick im Navigator aufs Geschoss > "Als Transparentpause anzeigen" → Geschoss als unveränderbare Zeichnungsgrundlage. **Transparentpausenpalette** (rechts unten): ein/aus, zwei Schieberegler (Intensität Transparentpause vs. aktives Fenster), Farbe änderbar.
- **Eigenschaften übernehmen (Pipette)**: **Alt-Taste** gedrückt + Wand anklicken → Wand-Werkzeug + alle Einstellungen übernommen.
- **Außenwände OG**: Pipette von EG-Außenwand, Geometriemethode Rechteckig, Eckpunkt oben links → untere Wandkante, **Tab** zur Längen-Eingabe, "3,49" + Enter.
- **Außenwände DG**: analog OG (Pipette), Wandhöhe nach Vorgabe anpassen, Geometriemethode Rechteckig (Eckpunkt oben links → unten rechts).
- **Innenwände OG/DG kopieren**: Element von Geschoss zu Geschoss kopierbar (Höhen bezogen aufs Geschoss bleiben erhalten). Schacht im EG wählen → Kopieren **Strg+C**/**Cmd+C** → ins OG wechseln → Einfügen **Strg+V**/**Cmd+V** (erscheint im "Ameisenrahmen" an Originalposition; verschiebbar; außerhalb des Rahmens klicken = endgültig platzieren).
- **DG-Schacht-Höhe**: Oberkante "Nicht verknüpft", Wandhöhe **3,2 m**.
- **DG-Innenwand**: Pipette vom DG-Schacht, Wanddicke auf **0,10** m, Geometriemethode **Gerade/Einfach**; Mauszeiger Innenecke rechts oben → Eingabe **"Y 1,9 -"** (Cursor 1,9 m nach unten), Enter; Referenzlinie-Lage ggf. mit **C**; Wand bis gegenüberliegende Außenwand verlängern.
- **Bearbeitungsbefehle** (Menü Bearbeiten / Standard-Symbolleiste):
  - **Trimmen**: Strg (WIN) / Cmd (MAC) gedrückt halten — schneidet überstehendes Stück eines linearen Elements ab.
  - **Splitten**: Strg+Ö (WIN) / Cmd+Ö (MAC) — teilt Element entlang Achse/Kante.
  - **Anpassen**: Strg+Ä (WIN) / Cmd+Ä (MAC) — kürzt/verlängert bis zu vorgegebener Achse/Kante.
  - **Verbinden**: Alt+V (WIN) / Ctrl+V (MAC) — verlängert/kürzt zwei lineare Elemente zur Verschneidung.

### Decken (Kap. 4.2)
- Decke = Rohdecke + Bodenaufbau; Wände stehen meist auf Rohdecke, Bodenaufbau/-belag je Raumnutzung (Bad, Küche, Wohnzimmer) verschieden → Rohdecke und Bodenaufbau separat modellieren (beides Decken-Werkzeug).
- **Bodenplatte EG**:
  - Deckenstärke **0,20** m, Abstand zum Ursprungsgeschoss **-0,10**.
  - Struktur **Einfach**, Baustoff **TRAGENDE BAUTEILE**.
  - Ebene **20 Decke**.
  - Erstellung: **Leertaste** (Zauberstab) → Klick auf beliebige Außenkante einer Außenwand → Decke automatisch entlang Gebäude-Außenkante.
- **3D-Kontrolle**: Pfeilwerkzeug, Strg+A/Cmd+A (alle EG-Elemente), Strg+3/Cmd+3 ins 3D. Freifläche, die Decke verdeckt: auswählen → Rechtsklick > **Auswahl ausblenden** (Befehl erst ab Archicad 25). Decken auch im 3D-Fenster erstellbar (manuell + Zauberstab).
- **Rohdecke EG↔OG**: im OG mit EG als Transparentpause (deckt überstehenden EG-Teil). Ursprungsgeschoss automatisch 1.OG; Deckenstärke auf **0,14** m; Geometriemethode **Rechteckig**; Eckpunkte (Fangpunkt-Häkchen) oben links → EG-Eckpunkt unten rechts.
- **Rohdecke OG↔DG**: im DG, gleiche Deckeneinstellungen + Zauberstab.
- Endergebnis im 3D-Fenster prüfen (Strg+3 / Cmd+3).
