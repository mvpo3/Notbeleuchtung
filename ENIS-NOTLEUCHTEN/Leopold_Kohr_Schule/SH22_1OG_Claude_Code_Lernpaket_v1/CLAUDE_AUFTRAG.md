# Auftrag an Claude Code

Wir verbessern die Raumerkennung unserer vorhandenen Software anhand dieses Lernpakets für **SH22, 1. OG**. Lies die Unterlagen, vollziehe die Planbelege nach und versuche anschließend, die passenden Verbesserungen in der bestehenden Engine umzusetzen.

## 1. Unterlagen und Projekt verstehen

- Lies `START_HIER.md`, anschließend alle fünf Dokumente in `03_Wissen/`.
- Prüfe das Paket mit `06_Werkzeuge/pruefe_paket.py` und die Quellanker mit `06_Werkzeuge/dxf_belege_pruefen.py`.
- Lies das Lernbuch und die zugehörigen JSON-Fälle. Beginne mit W06 auf Seite 7, M05 auf Seiten 20–21, M06 auf Seiten 22–23 und W02 auf Seiten 38–39. Danach Mauern, Türen, Fenster, Wege, Treppen und Lift vollständig durchgehen.
- Untersuche im tatsächlichen Software-Repository die geltenden Projektanweisungen und den bisherigen Ablauf von DXF-Import, Einheiten, Raumkonturen, Öffnungserkennung und Verbindungen. Verwende vorhandene Module und Tests. Erfinde keine Schnittstellen oder angeblich vorhandenen Dateien.
- Ist der Paketordner der einzige zugängliche Ordner, analysiere zunächst die Quellen und dokumentiere den benötigten Repository-Pfad. Behaupte keine Engine-Integration ohne Zugriff auf die Engine.

## 2. Bestehendes Verhalten messen

Verwende genau die enthaltene Original-DXF. Erzeuge einen nachvollziehbaren Ausgangslauf der Engine. Lege Ergebnis und Vorschau außerhalb des Lernpakets ab und dokumentiere verwendeten Code-Stand, Konfiguration, Eingabedatei und Einheiten.

Unterscheide dabei:

1. Wandkörper und Stützen als feste Bauteile.
2. Geländer, Brüstungen und Absturzsicherungen als eigene Barrierenart.
3. Türen als bestätigte Öffnungen mit Anschlag, Blatt und gegebenenfalls Bogen.
4. Fenster als Fassadenelemente; ein Flügelbogen macht daraus keine Personentür.
5. Freien Boden und Erreichbarkeit; ein Endraum kann begehbar sein, obwohl dort kein weiterer Durchgang liegt.
6. Treppen als Höhenverbindungen und Liftkabine, Schacht sowie Haltestelle als unterschiedliche Elemente.
7. Möblierung als Hindernis innerhalb eines Raumes, ohne daraus zusätzliche Räume zu bilden.
8. Texte, Elektrodiagonalen, Maßlinien und projizierte Konturen als gesonderte Planinformationen.

## 3. Die Korrekturen umsetzen

- Lies benachbarte Beschriftungen mit und ordne sie dem richtigen Bauteil zu. Beim zentralen Innenbereich steht ausdrücklich **„Absturzsicherung raumhoch“**. Diese Sicherung verhindert den Durchtritt; sie ist als eigene Klasse zu behandeln.
- Verwandle die beanstandete Untersichtskontur bei F1.04 nicht in eine Wand. Prüfe dafür Darstellungsebene, Anschlüsse, Text und Geometrie gemeinsam.
- Erzeuge aus dem Wort „Pflanzentrog“ keine frei gewählte rechteckige Sperrfläche. Die frühere breite weiße Maske in Z03 ist entfernt. Die Gehfläche reicht bis zur Randsicherung und schließt an die Treppe an.
- Ein Türbogen ist keine feste Barriere. Eine Fensteröffnung ist kein gewöhnlicher Durchgang. Eine dünne feste Trennwand bleibt eine Barriere.
- Harte Koordinaten oder SH22-Handles dürfen als Regressionseingaben verwendet werden, aber nicht als allgemeiner Erkennungsalgorithmus. Leite übertragbare Regeln ab und prüfe sie am Original.

## 4. In kleinen Schritten in die Engine übernehmen

Bearbeite zuerst den belegten Fehler in der vorhandenen Verarbeitung. Füge eine passende Regression hinzu, implementiere den kleinsten sinnvollen Fix und vergleiche anschließend denselben Eingabestand. Wiederhole dies für weitere unabhängige Fehler.

Nutze `05_Schemas/engine_ergebnis.schema.json` als Exportvertrag für einen Adapter aus der bestehenden Engine. Das ist ein Prüfvertrag; die internen Datenmodelle müssen dafür nicht vollständig ersetzt werden. Registriere die Ausgabe in das angegebene PDF-Koordinatensystem.

```bash
python3 06_Werkzeuge/bewerte_engine_ergebnis.py ../SH22_Engine/engine_ergebnis.json --out ../SH22_Engine/vergleich.json
```

Die 37 Prüffälle decken ausgewählte Fehler ab. Prüfe zusätzlich die tatsächlichen Raumkonturen, Nachbarschaften und Öffnungen im gesamten Geschoss. Ein Bestehen der Punktproben beweist keine vollständige Raumerkennung.

## 5. Ergebnis liefern

Dokumentiere:

- Welche Module und Regeln du geändert hast und warum.
- Den Vergleich vor und nach der Änderung, mit demselben Quellplan.
- Prüfergebnis und visuelle Ausschnitte für die behandelten Lernfälle.
- Noch falsche oder unklare Stellen mit Planposition, konkretem Beleg und Ursache.
- Ob Türen beide angrenzenden Bereiche tatsächlich verbinden und ob Treppen als Höhenwechsel behandelt werden.

Lass die Originale und dieses Lernpaket als unveränderte Referenz erhalten. Ein Engine-Versuch und sein tatsächliches Ergebnis müssen klar von den gelieferten Lernmarkierungen unterscheidbar bleiben. Arbeite zunächst an der Raumerkennung; die Notleuchtenplatzierung ist ein anschließender, separater Schritt.
