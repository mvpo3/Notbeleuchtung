# tutorial_architektur — Teil 0
> Quelle: tutorial_architektur (buecher) · dieser Teil.

> **Einordnung:** Dies ist das **Tutorial „Vectorworks Architektur“** von ComputerWorks (Copyright © 2019). Es ist KEINE Elektronorm und KEIN ÖNorm-/OVE-Dokument, sondern eine Schritt-für-Schritt-Bedienungsanleitung der CAD-Software Vectorworks anhand der Planung eines Wohnhauses in Süddeutschland (geplant von zickenheiner architekten gmbh – höfler · leisinger · zickenheiner, Lörrach). Relevanz für ElektroPlaner: CAD-Workflow, BIM/IFC, Symbol-/Zubehör-Handhabung, Ebenen-/Klassen-Konzept (auch für Elektroinstallation), Maße der Beispielplanung. Es enthält praktisch keine elektrotechnischen Norm-Fakten (Höhen/Abstände/Schutzbereiche von E-Komponenten).

## Inhalt

### Metadaten / Eckdaten
- Titel: TUTORIAL ARCHITEKTUR (Vectorworks).
- Schutzgebühr: **€ 15,00 / Fr. 20,–**.
- Copyright © **2019** by ComputerWorks. Reproduzieren/Ändern/Umschreiben/Übersetzen ohne schriftliche Genehmigung untersagt.
- Fotos: Rolf Frei (www.inslandgeschaut.de); Visualisierungen: Stephan Mönninghoff.
- 35 Seiten (Seitenmarker „PAGE n/35“).
- Tutorialdateien-Bezug: www.computerworks.eu/vwtutorials sowie Portale Vectorworks Service Select und Campus.

### Inhaltsverzeichnis (mit Seitenzahlen)
- Einleitung — S. 2
- Fotos und Visualisierungen — S. 4
- Die Benutzeroberfläche in Kürze — S. 8
- Schritt 1: Grundlagen importieren — S. 10
- Schritt 2: Wände zeichnen — S. 12
- Schritt 3: Fenster, Türen, Treppen — S. 15
- Schritt 4: 3D-Gebäudemodell — S. 22
- Schritt 5: Schnitt/Ansicht anlegen — S. 25
- Schritt 6: Symbole einfügen — S. 27
- Schritt 7: Grafische Füllungen — S. 28
- Schritt 8: Bemaßung und Beschriftung — S. 33
- Schritt 9: Räume und Flächen — S. 36
- Schritt 10: Visualisieren — S. 39
- Schritt 11: Energos Energieanalyse — S. 44
- Schritt 12: Planlayout — S. 46
- Werkzeuge und Arbeitsweisen — S. 50
- Was kann Vectorworks noch? — S. 58 (Freiform-Modellieren S. 58, Projekt Sharing S. 61, Building Information Modelling (BIM) S. 62, BIMobject S. 63, Marionette S. 64)

### Einleitung (S. 2–3)
- Projekt: Wohnhaus in Süddeutschland; Daten bereitgestellt von Büro Zickenheiner (www.zickenheiner.com) und Bauherr.
- Planung des Tutorial-Gebäudes erfolgt – von wenigen Ausnahmen abgesehen – im **Maßstab 1:100**.
- Vectorworks Architektur: kein Unterschied zwischen 2D- und 3D-Planung; jedes Objekt (Text, Bemaßung etc.) beliebig im Raum einsetzbar. Kombination vordefinierter + frei gezeichneter Elemente.
- Visualisierung via Renderworks (Cinema 4D Render Engine).
- Unterstützte Workflow-Stufen: 2D-Entwurf → Werkplanung → 3D-Modell → Visualisierung.

#### Raumbuch der Beispielplanung (Erdgeschoss-Räume, aus Raumstempeln)
Alle Räume: Höhen **+0,13** (Fertigboden) und **+/- 0,00** (Rohboden); Boden **Pandomo/Fliesen**; Wand **Sichtbeton**; Decke **Abgehängte Bekleidung**.

| Nr | Raum | Belegungsfläche BF |
|----|------|--------------------|
| 1 | Bad | 13.46 m² |
| 3 | Ankleide | 10.93 m² |
| 4 | Eltern | 13.53 m² |
| 5 | Flur | 15.72 m² |
| 6 | Kind 1 | 13.02 m² |
| 7 | Kind 2 | 13.02 m² |
| 8 | Kind 3 | 13.02 m² |
| 9 | Kinderflur | 8.85 m² |
| 10 | Kinderbad | 4.58 m² |
| 11 | Gäste WC | 2.83 m² |
| 12 | Garderobe | 7.51 m² |
| 13 | Gast / Hobby | 36.48 m² |

> Hinweis: Raum 12 erscheint auf einer Planvariante als „Garderobe“ (7.51 m²) und Raum 13 einmal als „Gast“, einmal als „Hobby“ (jeweils 36.48 m²) — gleiche Nummern, abweichende Bezeichnung in zwei Planständen.

- Treppen-Vermerk im Plan: **„15 STG 18,3 / 26,0“** = 15 Steigungen, Steigung **18,3 cm**, Auftritt **26,0 cm** (wiederholt auf mehreren Plänen).

### Benutzeroberfläche in Kürze (S. 8–9)
Palettenelemente:
- **Methodenzeile** — Methode des gewählten Werkzeugs bestimmen.
- **Konstruktionspalette** — grundlegende Zeichenwerkzeuge.
- **Werkzeuge / Werkzeuggruppen** — einzelne Werkzeuge; Gruppen für branchenspezifische + 3D-Werkzeuge.
- **Menübalken** — Befehle.
- **Zeigerfangpalette** — Punkte, Kanten, Winkel zum Ausrichten festlegen.
- **Attributpalette** — Farben, Füllungen, Liniendicken, Deckkraft.
- **Darstellungszeile** — Ebenen/Klassen aufrufen, zoomen, Ansichten, Maßstab.
- **Infopalette** — aktiviertes Objekt bearbeiten.
- **Navigationspalette** — Klassen, Konstruktionsebenen, Layoutebenen.
- **Zeichenfläche**, **Mitteilungszentrale** (u.a. Service-Pack-Updates), **Zubehör-Manager** (Symbole, Schraffuren, Tabellen, Bilder).
- Online-Handbuch via Menü „Hilfe“ → „Vectorworks-Hilfe“.

### Schritt 1 — Grundlagen importieren (S. 10–11)
1. Datei „01 Grundlagen einlesen.vwx“ öffnen (Ordner „Vectorworks_Dateien“).
2. Menü „Datei“ → „Import“ → „Import DXF/DWG“ → „01 Katastergrundlage.dwg“.
3. „Import“ → „Import Bild“ → „01 Handskizze.jpg“; Kompressionsmethode **„JPEG“**.
4. Skizze mit Werkzeug „Verschieben“ (erste Methode) positionieren: rechte obere Gebäudeecke der Skizze → rechte obere Ecke im Baufenster.
- Datenaustausch-Formate (unterstützt): **PDF, Collada, DXF, DWG, DWF, IFC, SKP, GBXML, EPS, Rhino 3DM, 3DS, STEP** u.v.m.
- Bei importierten PDF mit Vektoren ist Zeigerfang verwendbar.
- Import-Ergebnisse im Unterordner „Schritte Enddateien“.

### Schritt 2 — Wände zeichnen (S. 12–14)
1. Datei „02 Wände zeichnen.vwx“.
2. Werkzeuggruppe „Architektur“ → Werkzeug „Wand, gerade“; Methode „Linker Rand“ (1.) + „Rechteck-Methode“ (8.); Wandstil **„EG Außenwand 1“**.
3. Rechteck von Hilfspunkt X1 (links oben) zu X2 (rechts unten); mit **Alt-Taste** weiteres Rechteck → überlagernde Wandstücke herausschneiden.
4.–5. Weitere Rechtecke mit Alt-Taste → Ecken abschneiden / Wand hinzufügen.
- Innenwände: Klasse „Innenwand“ in Palette „Navigation“ sichtbar stellen (erste Spalte anklicken).
- Wände enthalten bereits Höheninformationen. 3D-Ansicht über Darstellungszeile („2D-Plan“ → z. B. „Rechts vorne oben“) bzw. Menü „Ansicht“ → „Standardansicht“. Darstellungsart **„OpenGL“** (Symbol = Teekanne).
- Dialog „Einstellungen Wand“ (letzte Methode): Stärke/Höhe, automatische Höhenanpassung an Konstruktionsebene, Wandschalen + unterschiedliche Schalenhöhen.

### Schritt 3 — Fenster, Türen, Treppen (S. 15–21)
**Intelligente Objekte:** Fenster, Türen, Treppen sind parametrisch; reagieren auf Änderungen (Fenster passen sich Wandstärke an; Detaillierungsgrad maßstabsabhängig). 2D-/3D-Inhalte unabhängig anzeigbar; als Symbole speicherbar.

**Fenster anlegen (Datei „03 Fenster einfügen.vwx“):**
- Werkzeug „Fenster“ doppelklicken → Dialog „Neues Fenster“.
- Reiter „Basiseinstellungen“ → Vorgabe „Fe Innen 2FlgS Eckig“; Werte:
  - **Breite außen: 2,310 m**
  - **Höhe außen: 0,925 m**
  - **Abstand Brüstungshöhe: 1,53 m**
  - **Einfügepunkt: Mitte**
- Reiter „Weitere Einstellungen“: Rahmen „Darstellung vereinfacht“, Allgemein → Rahmen → „Standard“; unter „Brüstung/Sturz“ Option „Für alle Maßstäbe“ deaktivieren, „Darstellung vereinfacht“; Außen+Innen „Brüstung“ statt „Bank“.
- Methode 2 „In Bezug auf Referenzpunkt einsetzen“. Drei Klicks: Referenzpunkt / Wand / Außenseite.
- Abstand zum Referenzpunkt: **3,50 m**.
- Bearbeitung über Werkzeug „Aktivieren“ + Infopalette; z. B. Fensterbreite auf **1,00 m** verkleinern.
- Tipp Zoom: Taste **„Y“** = temporäre Vergrößerung am Mauszeiger.
- Türen-Einsetzen funktioniert analog zu Fenstern (Werkzeug „Tür“, Werkzeuggruppe „Architektur“).

**Treppe einfügen (Datei „03 Treppe einfügen.vwx“):**
- Treppe als 2D- und wahlweise 3D-Objekt. Zubehör-Manager → Symbole/Intelligente Objekte → „Treppe EG“ doppelklicken; erste + letzte Methode → mit definiertem Einfügepunkt setzen; roter Hilfspunkt „Startpunkt Treppe“.
- Dialog „Einstellungen Treppe“ → „Detaileinstellungen“:
  - **Geschosshöhe: 2,75 m** (Schloss verriegeln)
  - **Auftrittbreite: 0,26 m** (Schloss verriegeln)
  - **Treppenbreite: 1,00 m**
  - **Anzahl Steigungen: 15** (Schloss verriegeln)
  - **Austrittstufe aktivieren, Wert 0,26 m**
- Option „Minimal-/Maximalwerte berücksichtigen“: Spielraum für Auftritt, Steigung, Schrittmaß, Steigungswinkel (Dialog „Minimalwerte und Maximalwerte“).
- „2D-Darstellung“: Unteres Geschoss Treppenbruch „Unten durchgezogen, oben gestrichelt“; Oberes Geschoss Haken, Ebene „OG“, „kein Treppenbruch“.

### Schritt 4 — 3D-Gebäudemodell (S. 22–24)
- Datei „04 3D_Modell.vwx“. Standardansichten via Darstellungszeile / Menü „Ansicht“ → „Standardansichten“; z. B. „Rechts vorne oben“ = Taste **„3“** (Ziffernblock).
- Erdgeschoss in Perspektive von oben rechts, Darstellungsart „OpenGL“.
- Menü „Ansicht“ → „Ebenendarstellung“ → „Zeigen und ausrichten“.
- Werkzeuggruppe „Visualisieren“: „Ansicht rotieren/durchlaufen/verschieben“.
- VR/Webview-Funktionen (VR-Brillen): www.computerworks.eu/virtual-reality.
- BIM/Open-BIM-Hinweis; IFC-Schnittstelle (Verweis S. 63 / www.computerworks.eu/bim).

### Schritt 5 — Schnitt/Ansicht anlegen (S. 25–26)
- Datei „05 Schnitt anlegen.vwx“. Menü „Ansicht“ → „Schnitt anlegen“; Schnittlinie zwischen zwei Hilfspunkten, Blickrichtung per Mausbewegung, Doppelklick.
- Dialog: Ebene **„110 Schnitt A-A“** (Layoutebene); Option „Zeichnungsbeschriftung anlegen“ aus.
- „Ebenensichtbarkeiten“: alle „(Zeichnungsebene)“ auf „Sichtbar“; Detaillierungsgrad wählen.
- „Einstellungen“ → „Attribute“: „Schnittflächen einzeln anzeigen“, „Originalattribute der Objekte verwenden“, optional „Schalen mit gleicher Füllung zusammenfügen“ → zeigt hinterlegte Schraffuren etc.
- **Höhenkoten:** Werkzeug „Kotenbemaßung“ (Werkzeuggruppe „Bemaßung/Beschriftung“); erste Methode; Nullkote = Referenzpunkt festlegen, dann weitere Koten.

### Schritt 6 — Symbole einfügen (S. 27)
- Datei „06 Symbole einfügen.vwx“. Zubehör-Manager → Zubehörtyp „Symbole/Intelligente Objekte“.
- Beispiel-Symbol: **„Bett 090x200 ModuQueen“** doppelklicken → Werkzeug „Symbol“; erste Methode „Einfügen“; Drehen per Mausbewegung.
- Symbol nur 1× als Definition gespeichert (egal wie oft eingesetzt); Doppelklick → bearbeiten. Vectorworks liefert „tausende“ vordefinierte Symbole; Hersteller-Zubehör über Service-Select-Portal.

### Schritt 7 — Grafische Füllungen (S. 28–32)
**Verläufe** (Datei „07 Grafische Fuellungen.vwx“): Zubehörtyp „Verläufe“; „Verlauf Wasser“ auf Schwimmbecken; „Verlaufzuweisung“ (Attributepalette) → Werte **x-Startpunkt 1, y-Startpunkt -5, Rotation 30°**; Art von „Linear“ auf „Radial“. Werkzeug „Füllung und Material bearbeiten“ zum Verschieben/Skalieren; Reglern unterschiedliche Deckkraft zuweisbar.
**Bildfüllungen:** Bild „Terr.-Platten 50…“ per Drag&Drop auf Terrassenboden; „Füllung und Material bearbeiten“ anpassen. Badezimmer oben links: Bildfüllung „Keramik 14 RBF“.
**Mosaike:** Füllart für wiederholende Muster; alle 2D-Objekte/Bilder nutzbar. Mosaik auf Rechteck unter Badewanne; Geometrie bearbeiten, Füllfarbe „Solid“ + Farbe.
**Transparenz/Deckkraft:** Boden Hobbyraum Fülldeckkraft **60 %**; Gebäudeschatten-Polygon Fülldeckkraft **30 %**. Deckkraft auch zentral pro Klasse einstellbar.
- Lieferumfang: Hunderte Füll-Grafiken (Attributpalette / Zubehör-Manager „Vectorworks-Bibliotheken“).

### Schritt 8 — Bemaßung und Beschriftung (S. 33–35)
- Bemaßung des Grundrisses im **Maßstab 1:50** (maßstabsabhängige Darstellung zeigt Wandschalen detailliert).
- Plan-Disclaimer: „Die Pläne sind vom Auftragnehmer verantwortlich zu prüfen. Maße sind am Bau zu nehmen und zu kontrollieren. Dieser Plan gilt nur in Verbindung mit den übrigen Ausführungsplänen des Architekten, den Plänen des Statikers, der Projektingenieure und der Fachfirmen.“
- Datei „08 Bemassung Beschriftung.vwx“. Text → „Textformatierung“ z. B. **Arial, 12 Punkt**.
- Werkzeug „Bemaßung Automatisch“ (Werkzeuggruppe „Bemaßung/Beschriftung“); Option „Schriftgröße anpassen“ deaktivieren; Methode 5 „Wände“ für Außenbemaßung; Methode 1+3 für Innenbemaßung.
- Bemaßungen sind **assoziativ** (passen sich Objektänderungen an und umgekehrt; Maßzahl überschreiben verschiebt z. B. Fenster). Rechtsklick auf Kettenbemaßung → Einfügen/Löschen/Bearbeiten. Manuelle Bemaßung: „Bemaßung horizontal und vertikal“.
- Beispiel-Bemaßungswerte aus dem Plan (Auswahl, Meter): Gesamtbreite 16.07; Felder 7.13 / 8.94; 6.79 / 8.12; Wandstärken-Maße u. a. **0,34 / 0,41 / 0,10** (34/41/10 cm); Fenster-/Öffnungsmaße u. a. 2.31, 0.925 (925), 0.80, 2.03, 4.625, 1.705, 2.54, 9.40, 8.72; Treppe „15 STG 18,3 / 26,0“; weitere Maße 13.76, 12.94, 2.64, 5.44, 1.65, 2.53 usw.

### Schritt 9 — Räume und Flächen (S. 36–38)
- Datei „09 Raeume_Flaechen.vwx“. Werkzeug „Raum“ (Werkzeuggruppe „Architektur“), Methode 3 „Anlegen“.
- Einstellungsdialog „Raumstempel 1“: Raumstempel-Klasse „Raumstempel“; Raumstempel-Symbol **„Raumstempel 10-SIA II“**.
- Raumobjekt in wandumgrenzten Raum klicken → passt sich automatisch an, zeigt Fläche.
- Infopalette: „Beläge verwenden“ → Oberflächenmaterialien für Wände/Decken/Fußboden; „Beläge zuweisen“. „Nummerierung“ → Raumnummer (manuell/automatisiert). „Funktion“ → Raumbezeichnung; „Liste bearbeiten“ für eigene Funktionen.
- Raumstempel über Modifikationspunkt verschiebbar.
- **Raumliste:** Menü „Extras“ → „Tabelle anlegen“ → Vorgabe **„Arch-Raumliste vereinfacht“**. Aktualisieren über Tabellenmenü „Datei“ → „Aktualisieren“ (durchsucht Zeichnung, bringt Zellen auf neuesten Stand).
- (Beispielraumbuch identisch zum Einleitungsbuch; siehe oben — Raum 13 hier „Hobby“.)

### Schritt 10 — Visualisieren (S. 39–43)
- Datei „10 Visualisieren.vwx“. Rendersoftware **Renderworks** (Cinema-4D-Render-Kern).
- Zubehör-Manager „Materialien 3D“; Material „Beton - Terrassenplatten“ bearbeiten (Kanäle: Farbe, Spiegelung, Transparenz, Relief; prozedurale Shader: Noise, Fresnel, Steinpflaster).
- Material zuweisen via Infopalette „Rendern“ → „Material auf“ = „Oben“.
- Darstellungsart „Renderworks“ (Menü „Ansicht“ → „Darstellungsart“). Weitere: „Drahtmodell“, „OpenGL“, „Renderworks schnell“.
- **Renderstile** (gespeicherte Rendereinstellungen, Drag&Drop), z. B. „Realistisch weisses Gipsmodell“.
- **Kamera:** Werkzeug „Kamera“ (Werkzeuggruppe „Visualisieren“); Leitlinie Hilfspunkt A→B (A = Augenhöhe, B = Blickpunkthöhe); **Blickwinkel auf 90°** erhöhen; „Kamera aktivieren“.
- „Ansichtsbereich anlegen“ (Menü „Ansicht“) auf Layoutebene; Darstellungsart unter „Hintergrund Darstellungsart“.
- Performance-Beispiel: Ansichtsbereich „Titel“ benötigt auf **Core-i7, 2.8 GHz, 16 GB RAM** ca. **95 Sekunden** Renderzeit.

### Schritt 11 — Energos Energieanalyse (S. 44–45)
- Datei „11 Energos.vwx“. Energos = dynamisches Messinstrument für Energieanalyse; farbcodierte Grafiken; Energieeffizienz schon in Entwurfsphase.
- Energielabel aktivieren → Infopalette „Energos“.
- Wohnzimmerfenster: Rahmentyp **„Wiegand DW Plus“**; Verglasungstyp **„dreifach Verglasung 9 - 4/15/4/15/4 (Ar)“** (3-fach, Glas-/Argon-Aufbau).
- Rechte Außenwand: Checkbox „Berechneten U-Wert ignorieren“ deaktivieren.
- Energielabel „Aktualisieren“ → Gesamtenergiebedarf reduziert. Info: www.computerworks.eu/energos.

### Schritt 12 — Planlayout (S. 46–49)
- Datei „12 Planlayout.vwx“. Layoutebenen für verschiedene Ausschnitte/Maßstäbe/Ansichten; definieren Druckeinstellungen.
- Ebene „01 [Layout]“; OG einblenden über aktive Ebene „OG-Fertigboden (Zeichnungsebene)“.
- „Ansichtsbereich anlegen“ (Menü „Ansicht“); Detaillierungsgrad „Tief“; auf Punkt „OG“ schieben.
- Dachaufsicht-Ansichtsbereich: **Maßstab 1:500**; „Ebenensichtbarkeiten“ → Konstruktionsebene „Lageplan“ sichtbar.
- Layoutebene „02 Baueingabe“: Ansichtsbereich auf „Rechts vorne oben“; „Hintergrund Darstellungsart“ Drahtmodell → OpenGL → „Aktualisieren“.

### Werkzeuge und Arbeitsweisen (S. 50–57)
- **Menüs/Befehle:** über hundert Befehle; wirken meist auf aktivierte Objekte.
- **Paletten** (Menü „Fenster“): enthalten Werkzeuge/Funktionen. Tastenkürzel via „Arbeitsumgebung anpassen“ (Menü „Extras“ → „Arbeitsumgebung“).
- **Darstellungszeile:** Klassen/Ebenen/Ansichten/Darstellungsarten, Zoom, Drehen, Maßstab; konfigurierbar über schwarzes Dreieck rechts.
- **Methodenzeile:** zeigt aktives Werkzeug + Methoden (z. B. Rechteck über Diagonale, Mittelpunkt, Seitenmitte, gedreht). Zusatzeinstellungen über Einstellungs-Symbol.
- **Infopalette:** Objekte nachträglich verändern (z. B. Kreis „Radius“; Wand „Dicke“/„Schalen“); Datenbank-Verknüpfung; Texturen. Öffnen via „Fenster“ → „Paletten“ → „Informationen“.
- **Navigationspalette:** Strukturelemente (Ebenen, Klassen, Ansichtsbereiche, Darstellungen, Referenzen) anlegen/bearbeiten.
- **Zubehör-Manager:** Verwaltung von grafischen Elementen (Bilder, Farbverläufe, Schraffuren, Mosaike, Textformatierungen, Texturen, Renderstile), mehrfach genutzten Objekten (Fenster, Türen, Tische, Pflanzen, Scheinwerfer, Symbole), schalenverknüpften Bauteilen (Wände, Böden, Decken), Datenbanken/Tabellen. Öffnen: Fenster > Paletten > Zubehör-Manager.
- **Attributpalette:** Füllfarbe, Füllung, Stift, Stiftfarbe, Deckkraft Füllung/Stift, Linien, Schlagschatten, Linienendzeichen. Beispiel: rote Füllung, schwarze Kontur **0.10 mm**, Deckkraft Füllung **50 %**, Stift **100 %**. Farbverläufe/Bildfüllungen/Mosaike erst über Zubehör-Manager anlegen. Ohne aktives Objekt = Grundeinstellung für neue Objekte.
- **Zeigerfangpalette:** Fangpunkte, Hilfslinien-Einblendung, Rasterausrichtung.
- **Intelligenter Zeiger:** zeigt Koordinaten, relativen Winkel, Dimensionen (Beispielanzeige: Δx 2,00 m / Δy -3,00 m; L 4,00 m / W 30°; „Ausrichten 90° / Ausrichten 0°“; „Oben Links L 1,17 m W 0,00°“).
- **Lupe (Taste Y):** temporäre Vergrößerung.
- **Röntgenblick (Taste R):** alles halbtransparent → verdeckte Objekte aktivierbar.

**Planstruktur:**
- Jedes Objekt liegt auf einer **Ebene** und in einer **Klasse**. Neues Dokument enthält „Konstruktionsebene-1“ und Klassen „Keine“ + „Bemaßung“.
- **Konstruktionsebene** = wo (z. B. „Erdgeschoss“, „Obergeschoss“, „Dach“).
- **Klasse** = was/Verwendung (z. B. „Außenwände“, „Möblierung“, „Sanitär“, „Zuluft“, „Abluft“, „Gas-/Wasserinstallation“).
- Ebenen/Klassen ein-/ausblendbar; **„mit nur einem Klick ebenenübergreifend alle Angaben zur Elektroinstallation sichtbar machen“** oder alle Rohbau-Infos. (Direkt relevant für E-Plan-Layer-Konzept.)
- Sichtbarkeit: sichtbar / unsichtbar / grau (wenig sichtbar); Status im Fenster „Organisation“ (Menü „Extras“). Darstellungskombination über „Ebenendarstellung“/„Klassendarstellung“ (Menü „Ansicht“).
- Empfehlung: Klassendarstellung „Zeigen, ausrichten und bearbeiten“ belassen.

**Symbole & Gruppen:**
- Symbole = Zubehör, als Instanz eingesetzt, kaum Speicherplatz, halten Plan „schlank“. „Symbol anlegen“ (Menü „Ändern“). Änderung der Symboldefinition wirkt auf alle Instanzen. Wände „erkennen“ Symbole → Türen/Fenster automatisch eingesetzt.
- Gruppe: „Ändern“ → „Gruppen“ → „Gruppieren“.
- Intelligente Objekte = parametrisch, z. B. Fenster/Türen/Treppen.
- Hilfe: „Vectorworks-Hilfe“ (Menü „Hilfe“); „Direkthilfe“ → Funktion anklicken → passende Handbuchstelle.

### Was kann Vectorworks noch? (S. 58–64)
**Freiform-Modellieren (S. 58–60):** Modellierkern **Parasolid**. Datei „13_Modellieren.vwx“. Werkzeug „NURBS-Kurve“, Einstellung **2°**; Werkzeuge „Kurvenverbindung“, „Hohlkörper“ (Materialstärke), „Verrunden 3D“ (Kantenverrundung). Darstellung Drahtmodell → OpenGL.
**Projekt Sharing (S. 61):** Multi-User-Lösung; alle am selben Projektfile, gleiche Klassen/Symbole; Projektleiter regelt Berechtigungen; keine Extra-Server-Software. www.computerworks.eu/projekt-sharing.
**BIM (S. 62):** Gebäude als 3D-Modell, alle Daten vernetzt; daraus alle Grundrisse/Ansichten/Schnitte/Mengen; Bauteile mit Datenbank verknüpft. **Open BIM** = Initiative von „buildingSMART“ + Softwareanbietern; Austauschformat **IFC (Industry Foundation Classes)**; jedem Objekt IFC-Objekttyp zuweisbar. www.computerworks.eu/bim.
**BIMobject (S. 63):** Zugriff auf über **3 Millionen** BIM-Objekte (echte Herstellerobjekte inkl. Artikel-Nr.); Download auch in AutoCAD-, SketchUp-, 3DS-Format; kostenlos. www.bimobject.com.
**Marionette (S. 64):** grafisches Scripting-Tool, basiert auf **Python**, ohne Code-Zeile schreiben; parametrische Objekte/Varianten. www.computerworks.eu/marionette.

### Impressum (S. 35)
- Vectorworks = eingetragene Marke von Vectorworks, Inc. (Teil der Nemetschek Group). Für Windows und Mac OS.
- ComputerWorks GmbH, Schwarzwaldstraße 67, 79539 Lörrach, Tel. +49 (0)7621/4018-0, info@computerworks.de, www.computerworks.de.
- ComputerWorks AG, Florenz-Strasse 1e, 4142 Münchenstein (Schweiz), Tel. +41 (0)61 337 30 00, info@computerworks.ch, www.computerworks.ch.

## Maschinen-Regeln

> Hinweis: Dieses Dokument ist ein CAD-Software-Tutorial, KEINE Elektronorm. Die nachfolgenden Fakten sind Maße/Parameter der Beispiel-Architekturplanung bzw. CAD-Konventionen — keine OVE/ÖNorm-Elektroregeln. Es gibt keine elektrotechnischen Schutzbereiche, FI/RCD-, Leitungs- oder Steckdosen-Vorgaben in diesem Chunk.

- [HÖHE] Fenster (Vorgabe „Fe Innen 2FlgS Eckig“): Höhe außen 0,925 m, Breite außen 2,310 m, Brüstungshöhe 1,53 m (Schritt 3, S. 16)
- [HÖHE] Treppe Geschosshöhe 2,75 m (Schritt 3, S. 20)
- [HÖHE] Treppe Steigung 18,3 cm bei 15 Steigungen (Planvermerk „15 STG 18,3/26,0“, S. 3/33/36)
- [ABSTAND] Treppen-Auftrittbreite 0,26 cm → 0,26 m; Austrittstufe 0,26 m (Schritt 3, S. 20)
- [ABSTAND] Treppe Auftritt 26,0 cm (Planvermerk „15 STG 18,3/26,0“, S. 3/33/36)
- [ABSTAND] Treppenbreite 1,00 m; Anzahl Steigungen 15 (Schritt 3, S. 20)
- [ABSTAND] Beispiel-Fenster-Einsetzabstand zum Referenzpunkt 3,50 m; korrigierte Fensterbreite 1,00 m (Schritt 3, S. 16–17)
- [ABSTAND] Wandstärken-Bemaßungen der Beispielplanung u. a. 0,34 m / 0,41 m / 0,10 m (Schritt 8, S. 33–34)
- [DEFINITION] Standard-Planungsmaßstab Tutorial-Gebäude 1:100; Bemaßung 1:50; Dachaufsicht 1:500 (Einleitung S. 2; Schritt 8 S. 33; Schritt 12 S. 47)
- [DEFINITION] Raum-Höhenkoten: Fertigboden +0,13 m, Rohboden +/-0,00 m (alle EG-Räume, S. 3/36)
- [DEFINITION] Klasse = Objekttyp/Verwendung (z. B. „Sanitär“, „Gas-/Wasserinstallation“, „Elektroinstallation“); Konstruktionsebene = Geschoss-Lage; Elektroinstallation ebenenübergreifend per Klick einblendbar (Werkzeuge/Arbeitsweisen, S. 55)
- [DEFINITION] IFC (Industry Foundation Classes) = Open-BIM-Austauschformat; jedem Objekt IFC-Objekttyp zuweisbar (BIM, S. 62)
- [DEFINITION] Import-/Austauschformate: PDF, Collada, DXF, DWG, DWF, IFC, SKP, GBXML, EPS, Rhino 3DM, 3DS, STEP (Schritt 1, S. 11)
- [DEFINITION] Symbol = einmal als Definition gespeicherte, mehrfach instanziierbare Objektgruppe; Symboldefinition-Änderung wirkt auf alle Instanzen (Schritt 6 S. 27 / Werkzeuge S. 56)
- [SYMBOL] Möbel-Beispielsymbol „Bett 090x200 ModuQueen“ (Schritt 6, S. 27)
- [DEFINITION] Energos-Verglasung Wohnzimmerfenster: 3-fach „9 - 4/15/4/15/4 (Ar)“, Rahmentyp „Wiegand DW Plus“ (Schritt 11, S. 44)
- [DEFINITION] Attribut-Beispiel: Konturlinie 0,10 mm, Füll-Deckkraft 50 %, Stift-Deckkraft 100 % (Werkzeuge/Arbeitsweisen, S. 53)

tutorial_architektur part0: 17 Regeln — CAD-Tutorial Vectorworks (keine Elektronorm)
