# Übertragung in eine vorhandene Engine

Dieses Dokument beschreibt einen anschlussfähigen Ablauf. Die Namen der vorhandenen Softwaremodule sind nicht bekannt und werden deshalb nicht vorgegeben.

## 1. Eingang erhalten

Die Original-DXF mit SHA-256 und Einheitenheader erfassen. Modelspace, Blöcke/INSERTs, Layer, Linientypen, geometrische Transformationen und Textfragmente berücksichtigen. Bei verschachtelten Blöcken den Instanzpfad und die Blocktransformation mitführen; ein Blockinhalt-Handle allein identifiziert keine einzelne Instanz.

Der beiliegende Geometriekontext enthält nur bestimmte Top-Level-Typen. Er ist eine Lesehilfe. Der produktive Import muss die vollständige DXF verwenden.

Intern möglichst CAD-Koordinaten und Original-Handles bewahren. Für den Vergleich mit diesem Paket einen Adapter in PDF-Punkte ergänzen. Die Registrierung nicht auf andere Pläne übertragen.

## 2. Geometrie und Bedeutung getrennt verarbeiten

Zunächst Linien, Kurven, Füllungen, Texte, Öffnungen und mögliche Konturen erfassen. Danach aus mehreren Belegen eine Bauteilklasse ableiten. So kann eine geometrisch gleiche Linie je nach Anschluss und Beschriftung als Wandkante, Geländer, Fensterrahmen oder Annotation eingeordnet werden.

Beispielhafte interne Trennung:

| Ebene | Inhalt |
|---|---|
| Quelle | Handle, Instanzpfad, Typ, Layer, Linientyp, originale Geometrie |
| Interpretation | Klasse, Geschoss, Höhenbezug, Begründung, Unsicherheit |
| Raumbegrenzung | Welche Bauteile begrenzen den Raum beziehungsweise Bereich? |
| Bewegungsbegrenzung | Wo verhindert ein Bauteil den Durchtritt? |
| Begehbare Fläche | Boden abzüglich tatsächlicher Hindernisse |
| Verbindungen | Bestätigte Tür, freier Durchgang, Treppen- oder Liftverbindung |

Ein Raum kann mehrere freie Bodenstücke um Möbel herum enthalten. Nicht jede freie Komponente ist ein eigenständiger Raum. Umgekehrt kann ein durchgängiger Gang mehrere funktionale Bereiche enthalten, ohne dass eine dünne Belagslinie eine Wand bildet.

## 3. Texte zuordnen

Benachbarte Textfragmente zu lesbaren Angaben zusammenführen, ohne die ursprünglichen Handles zu verlieren. Distanz ist ein Kandidatenmerkmal. Die Zuordnung zusätzlich anhand von Ausrichtung, Führungslinie, Lage zum Rand und passendem Bauteil prüfen.

Bei W02 gehören die Textfragmente `8720B` und `8720C` zum Hinweis „Absturzsicherung raumhoch“. Die Linien `8556D`, `85576`, `85578`, `8557A` bilden den im Lernplan hervorgehobenen Innenrand. Diese Liste ist ein konkreter Beleg für SH22. Die allgemeine Regel lautet: Bauteiltext und zugehörige Kontur zusammen klassifizieren.

Bei W06 darf das Fragment `87211` („Pflanzentrog“) nicht allein eine rechteckige Sperrmaske erzeugen. Wenn Text und Kontur widersprüchlich oder unvollständig sind, die Zuordnung als offen speichern. Keine unbemerkte Fülloperation über einen beliebigen Textrahmen ausführen.

## 4. Barrieren und Öffnungen

Wandkörper mit ihrer vollständigen Dicke modellieren. Durchgänge nur an belegten Öffnungen erzeugen. Dünne feste Trennwände und Randsicherungen dürfen geometrisch schmal sein und trotzdem eine Verbindung unterbinden.

Türblatt und Bogen als Merkmale der Tür erfassen. Erst die Öffnung und ihr beidseitiger Bodenanschluss begründen die Verbindung. Doppelte Flügel zu einem Portal zusammenführen, sofern Anschläge und gemeinsame Öffnung dazu passen.

Fenster separat klassifizieren. Ein ähnlicher Bogen darf keine identische Wirkung im Wegenetz auslösen. Möblierung, Treppenbruch, Elektroangaben und Unteransichten ebenfalls nicht ungeprüft als Wandbarrieren übernehmen.

## 5. Flächen und Verbindungen bilden

Raumkonturen aus räumlichen Begrenzungen ableiten. Begehbare Flächen innerhalb dieser Bereiche separat ermitteln. Hindernisse ausschneiden, ohne dadurch automatisch einen neuen Raum zu erzeugen. Bei Öffnungen prüfen, ob tatsächlich freie Flächen auf beiden Seiten anschließen.

Die Verbindungsstruktur soll mindestens enthalten: angrenzende Bereiche, Portalgeometrie, Verbindungstyp, Geschossbezug und Evidenz. Ein geometrisch naher Raum ist ohne bestätigte Öffnung noch kein Nachbar im Wegenetz.

Treppen als Höhenverbindungen behandeln. Ein unbekanntes Zielgeschoss als unbekannt speichern. Liftzugang und dynamisch vorhandene Kabine getrennt vom Schacht betrachten.

## 6. Fehlerorientiert ändern

Für jede Änderung einen belegten Fehler wählen, z. B.:

1. Ausgangslauf färbt die Projektion bei M05 als Wand ein.
2. Quelle und Lernfall zeigen, welche Merkmale die Fehleinordnung verursachen.
3. Einen Test an der betreffenden Import-/Klassifizierungsfunktion ergänzen.
4. Die Regel allgemein korrigieren.
5. Ausgangsplan erneut verarbeiten und Vorher/Nachher vergleichen.
6. Andere vergleichbare Konturen im Geschoss gezielt prüfen, damit der Fix keine echten Wände entfernt.

Koordinatenlisten aus dem Lernpaket dürfen in Regressionen vorkommen. Sie dürfen nicht als Ersatz für Erkennung in der produktiven Engine landen. Gleiches gilt für feste SH22-Layer- oder Handle-Ausnahmen ohne begründete übertragbare Regel.

## 7. Prüfadapter

Das Schema `05_Schemas/engine_ergebnis.schema.json` ist eine externe Vergleichsschnittstelle. Ein Adapter kann die vorhandenen Engine-Objekte dorthin exportieren.

- `features` enthält klassifizierte Objekte in lokalen PDF-Koordinaten.
- `walkable_area` ist die freie Bodenfläche. `room` kann die gesamte Raumkontur einschließlich belegter Stellflächen beschreiben.
- Treppen dürfen sowohl eine eigene `stair`-Geometrie mit `properties.height_transition=true` als auch eine begehbare Teilfläche besitzen.
- `evidence.status=uncertain` bleibt als offener Befund erhalten und erfüllt keinen positiven Prüffall.
- `evidence.source_handles` und `label_handles` verknüpfen Entscheidungen mit der Quelle.
- `portals` enthält echte Tür- oder Durchgangsabschnitte und genau zwei unterschiedliche angrenzende Flächen-IDs.
- `target_floor_id` kann bei Treppen in `properties` als `null` geführt werden, solange der Geschossanschluss nicht belegt ist.

Die Engine darf intern andere Einheiten, Klassenbezeichnungen und Strukturen verwenden. Der Adapter übersetzt sie nachvollziehbar. Die Lernfälle liefern keine neue Pflichtarchitektur für das gesamte Produkt.
