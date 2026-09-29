# Claude Code – Übergabe Raumerkennung 2. Untergeschoss

Stand: 24.09.2026. Dieses Paket enthält die **korrigierte 2UG-Fassung** nach den Beanstandungen an Wandfarben, Türteilen und Bodenfüllung. Es ist für die Weiterarbeit an der Raumerkennung gedacht. Andere Geschosse sind nicht enthalten.

## Inhalt und Einstieg

| Datei | Verwendung |
|---|---|
| `CLAUDE_CODE_2UG_START.md` | Diese Übergabe zuerst lesen. |
| `2UG_Raumerkennung_Daten.json` | Interpretierte Flächenkonturen, ausgewählte Original-Vektorpfade, getrennte Türteile, Farben, Regeln, 52 Lernkapitel, Seitenverweise und Prüfstatus. |
| `2UG_Lernbuch_Raumerkennung_markiert.pdf` | 61 Seiten mit 52 ausführlichen Lernkapiteln, Korrekturliste und Originalplanansicht. |
| `2UG_Gehflaechen_und_Bauteile_Grossplan.pdf` | Zwei A2-Seiten: freie Bodenflächen und markierte Bauteile. |

Die beiden PDFs wurden für dieses Paket unverändert aus der überarbeiteten Fassung übernommen. Die JSON ist ein neuer, portabler Export dieser Überarbeitung. Sie ist eine dokumentierte Interpretation, kein vollständig geprüftes CAD-Modell. Die neue Fassung wurde intern kontrolliert; eine ausdrückliche Nutzerfreigabe liegt noch nicht vor.

**Empfohlener Startauftrag an Claude Code:**

> Lies zuerst CLAUDE_CODE_2UG_START.md und die JSON. Verwende die beiden PDFs als visuelle Referenz für die Raumerkennung im 2UG. Prüfe die vorhandene Projektstruktur und setze die dokumentierten Unterscheidungen in der bestehenden Erkennung und Darstellung um. Markiere Bauteile direkt auf ihrer Kontur, trenne Türblatt, Bogen und Zarge und fülle nur die freie Bodenfläche. Begründe Zuordnungen mit den tatsächlichen Planmerkmalen. Halte ungeklärte Höhen, Zugänge und Symbole ausdrücklich offen. Prüfe die hier genannten Fehlerfälle vor der Ausgabe.

## Was aus den Nutzerkorrekturen verbindlich folgt

1. **Wände und Stützen kräftig rot:** Die Farbe muss sichtbar von Orange und Grün unterscheidbar sein. Grün darf nicht in ihre Querschnitte laufen. Markiert wird das Bauteil selbst.
2. **Türteile einzeln:** Türblatt orange; Schwenkbogen blau; Zarge türkis. Das Blatt ist der bewegliche Gegenstand. Der Bogen erklärt die Bewegung und ist kein Bauteil. Die Öffnungsquerlinie darf nicht pauschal als geöffnetes Blatt gelten.
3. **Alle freien Bodenflächen füllen:** Nicht nur eine Weglinie oder einen Korridorstreifen zeichnen. Wände, Stützen, gezeichnete Fahrzeuge, Blattflächen, Gittertrennungen, Schachtgrube und technische Sonderflächen bleiben ausgespart. Treppe und Rampe haben eigene Masken.
4. **Kleine Zeichen ernst nehmen:** Wasserrinne, Rigol, Pumpensumpf und Gitterrost getrennt erklären. Beim Lift Schacht, Grube, Portal und Schwelle unterscheiden. Bei der Treppe Lauf, Stufenkante, Richtung und ebenen Vorbereich unterscheiden.
5. **Erklärungen für Anfänger:** Begriff definieren, konkrete Linien oder Flächen benennen, Zuordnung begründen, ähnliche Zeichen abgrenzen und die Folge für die Bodenfläche erläutern. Keine pauschalen Suchkästen um Türen, Wände oder Fenster.

## Farben

| Bedeutung | Farbe |
|---|---|
| Wand / Stütze | `#C1122F` |
| Türblatt | `#EF7100` |
| Schwenkbogen | `#145BE0` |
| Zarge / symbolischer Portalrahmen | `#008A94` |
| Freier ebener Planboden | `#2AAF79` |
| Treppenbereich / Fahrzeugrampe | `#EDB62C` |
| Stufenkante | `#765100` |
| Rinne / Rost | `#00789B` |
| Belegung / Schacht / technische Aussparung | `#80758B` |
| Gittertrennung | `#283F4A` |
| Stellplatzgliederung | `#7A609C` |

Die Farben dienen der Erklärung. Sie sind keine universellen CAD-Erkennungsmerkmale. Gleiche Farbe bedeutet nicht zwangsläufig gleiche Objektklasse: Treppe und Rampe sind getrennte Geometrien. Detailviolett und die beiden allgemeinen Fensterschemata werden auf ihrer jeweiligen Seite gesondert erklärt.

## JSON und Koordinaten richtig verwenden

- `geometries` enthält elf Polygon-/MultiPolygon-Masken. Ihre inneren Ringe sind Löcher und müssen beim Füllen erhalten bleiben. `walls` fasst Wände und Stützen zusammen; es gibt keine geprüfte Einzelbauteil-ID für jede Säule. `floor` hat mehrere Teile, die **keine Raum-IDs** darstellen.
- `doors` trennt fünf Blatt-/Bogenpaare. `vector_paths` enthält dazu ausgewählte Linien, Bézierkurven, Rechtecke und Vierecke aus der Quelle. Jeder Linien-/Kurvenabschnitt hat einen eigenen Startpunkt. Getrennte Abschnitte nicht durch erfundene Linien verbinden.
- `path_groups` ordnet Rahmenprofile, Drehanschluss, Stufenkanten, Portal, Schwelle und Roststriche zu. Die Pfadindizes sind lokale Indizes des damaligen PyMuPDF-Exports, keine stabilen CAD-Handles.
- `lessons` enthält alle 52 Lernkapitel mit Buchseite und Ausschnitt. `evidence_scope = general_educational_schema` bedeutet: allgemeine Erläuterung, **kein erkanntes Bauteil im 2UG**. Dies betrifft die Fensterschemata auf Seiten 50 und 51.
- Koordinaten beziehen sich auf die **ursprüngliche PDF-Seite**, normiert auf Breite 1800. Ursprung oben links; X nach rechts, Y nach unten. Einheiten sind weder Meter noch Rasterpixel. Umrechnung zu ursprünglichen PDF-Seitenpunkten: `x_pdf = x * (3370/1800)`, entsprechend für Y. Die Originalseite misst 3370 × 2580 PDF-Punkte.
- Für die Gesamtansichten enthält `pdf_placements` die Umrechnung auf Seitenkoordinaten der mitgelieferten PDFs. Bei `[a,b,c,d,e,f]` gilt `X = a*x + c*y + e`, `Y = b*x + d*y + f`. Die Angaben gelten nur im jeweiligen Clip. Buch-Detailseiten besitzen andere Ausschnitte und Skalierungen; deren JSON-Koordinaten nicht unverändert auf eine Buchseite zeichnen.
- Für einen Rasterexport mit DPI gilt zusätzlich `Pixel = PDF-Seitenpunkt * DPI/72`. Das ist nur eine Darstellungsumrechnung und liefert keine Gebäudemaße.
- Die Original-PDF `2UG_ohne_Masse(1).pdf` ist **keine fünfte Datei im ZIP**. Seite 61 zeigt den Gebäudeausschnitt in Originalfarben ohne Lernmarkierungen. Die SHA-256 der ursprünglichen Quelldatei ist in der JSON dokumentiert.

Minimaler Einstieg:

```python
import json
from pathlib import Path

data = json.loads(Path("2UG_Raumerkennung_Daten.json").read_text(encoding="utf-8"))
masks = {item["id"]: item for item in data["geometries"]}
floor_geometry = masks["floor"]["geometry"]
doors = data["doors"]
```

Zum Beispiel kann Shapely `shape(floor_geometry)` die lokalen Polygonkoordinaten lesen. Geografische Standardannahmen eines GeoJSON-Kartenviewers wären hier falsch.

## Planbezogene Befunde und offene Punkte

**Türen:** Zwei detaillierte Schleusentüren, ein einfaches Symbol im unteren Abstellbereich, eine über dem Treppenlauf dargestellte Gitteröffnung und eine Revisionsöffnung sind gesondert erfasst. Die Gitteröffnung über den Stufen hat keine bestätigte Höhenzuordnung. Eine Wartungsöffnung ist kein bestätigter regulärer Durchgang. Aus keinem Symbol allein folgen geprüfte Zugangsrechte, eine dauerhafte Offenstellung oder lichte Durchgangsmaße. Drei symbolische Blätter haben nur eine schmale Maskierungsbreite; diese nicht als reale Blattdicke ausgeben.

**Lift:** Der Plan nennt die Zone SCHACHTGRUBE. Eine Kabine wird dort nicht ergänzt. Das Portal ist ausdrücklich symbolisch gezeichnet; die Schwellenangabe ersetzt keinen bemaßten Schnitt. Die Schachtfläche bleibt aus dem grünen Boden ausgeschlossen.

**Treppe:** Gelb beschreibt die Stufenzone, Braun die Kanten. Der ebene Vorbereich ist grün. Überlagerte Projektionen dürfen nicht zu doppelten Stufen oder zu einem ebenen Durchgang mitten im Lauf führen. Höhen, genaue Stufenzahl und Handlaufgeometrie sind nicht vollständig bestimmt.

**Entwässerung:** Rinnenstreifen und Rost-/Sumpffelder werden getrennt erfasst. Die Masken dürfen sich an einem Rost in einer Rinne überlappen. Polygonteilzahl ist keine Anlagenanzahl. Übergehbarkeit, Tiefe, Lastklasse, Fließrichtung und Pumpenausstattung nicht ergänzen, wenn sie nicht belegt sind.

**Fenster:** Kein gewöhnliches Fenster ist in dieser 2UG-Auswertung eindeutig bestätigt. Technische Lüftungs- oder Durchbruchzeichen sind kein Ersatzbeleg. Die beiden Fensterschemata erklären Rahmen, Flügel, Glas, Brüstung und Fensterbank allgemein.

**Boden:** Grün ist freier Planboden unter den beschriebenen Annahmen. Es ist kein bestätigter sicherer Fußweg oder barrierefreier Weg. Die Fahrzeugrampe bleibt separat. Ein offener Raumgraph, Höhenbeziehungen und Zugangsbedingungen müssen eigenständig geprüft werden. Text, Stellplatznummern, Wolken und Pfeile sind keine physischen Hindernisse.

## Wichtige Seiten

| Thema | Lernbuchseiten |
|---|---|
| Farben, Leseregeln, Gesamtflächen | 2–5 |
| Wände, Stützen, Stellplätze, Fahrzeuge | 6–12 |
| Türblatt, Bogen, Rahmen, Bänder, Schleuse | 13–20 |
| Treppe, Stufen, Höhen, Gitterwand | 21–26 |
| Lift und Schachtgrube | 27–31 |
| Rampe, Fahrradbereich, Metallgitter | 32–37 |
| Wasserrinnen, Rigol, Pumpensumpf, Rost | 38–42 |
| Technische Zeichen und Aussparungen | 43–48 |
| Fensterprüfung und allgemeine Fensterschemata | 49–51 |
| Bodenprüfung und Erkennungskontrolle | 52–57 |
| Änderungen, Kontrollblatt, Quellen, Originalansicht | 58–61 |

## Prüfung vor der nächsten Ausgabe

Die korrigierten Flächen sind geometrisch gültig. Die freie Bodenmaske hat innerhalb der dokumentierten numerischen Toleranz keine Flächenüberschneidung mit Wänden, Schacht, technischen Aussparungen, Belegungen, Rinnen, Sumpffeldern, Türblattmasken, Gittertrennungen, Treppe oder Rampe. Das prüft die Konsistenz dieser Interpretation; es beweist nicht automatisch die richtige Erkennung jedes Bauteils.

Bei Änderungen insbesondere prüfen:

1. Kein Grün auf Wänden oder Stützen; keine Löcher durch Text oder Stellplatznummern.
2. Reales Türblatt, Schwenkbogen und Rahmen getrennt; kein pauschal ausgefüllter Kreissektor.
3. Schachtgrube und Fahrzeugbelegung ausgespart; Sonderflächen bleiben getrennt.
4. Keine erfundenen Fenster, Kabinen, Maße, Höhen oder Durchgänge aus uneindeutigen Symbolen.
5. Keine Raumverbindung durch geschlossene Wand/Gitter oder allein aufgrund gleicher Bodenfarbe.
6. Ausgabe in Gesamtansicht und an den beanstandeten Detailstellen visuell prüfen; Farben und Erklärungen müssen zueinander passen.

PDF-Dateigrößen, Seitenzahlen und SHA-256-Prüfsummen stehen in der JSON unter `files`. Das ZIP enthält genau die vier oben genannten Dateien.
