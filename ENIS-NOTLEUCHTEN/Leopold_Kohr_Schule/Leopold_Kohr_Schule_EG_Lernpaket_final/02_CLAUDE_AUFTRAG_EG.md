# Konkreter Arbeitsauftrag für Claude Code - ausschließlich EG

## Ziel

Nutze das Lernpaket, um die vorhandene Raumerkennung am Original-EG der Leopold-Kohr-Schule nachprüfbar zu verbessern. Verstehe Wände, Türen, Fenster, feste Glasabschlüsse, geometrische Verbindungen und Treppen. Plane in diesem Auftrag keine Notleuchten und ändere keine Normregeln.

## Verbindliche Ausgangsbasis

Lies `00_START_HIER.md`, `01_LERNWISSEN_EG.md`, `daten/08_QUELLEN_EG.json` und die Regeln/Beispiele. Prüfe die beiden Originalprüfsummen. Ermittle das tatsächlich vorhandene Repository, den aktuellen Commit, die Konfiguration und vorhandene Schnittstellen. Erfinde keine Dateipfade, Funktionsnamen oder schon vorhandenen Funktionen.

## Erst Diagnose, dann Änderung

1. Führe einen reproduzierbaren Ausgangslauf auf der Original-DXF aus, sofern die Engine und ihre Voraussetzungen tatsächlich verfügbar sind. Sichere Eingabe, Konfiguration, Codeversion, Protokoll und Ausgabe.
2. Zeige Zwischenstände für Import, Bauteile, Raumflächen, Öffnungen und Verbindungen jeweils als Daten und Overlay auf dem Originalplan.
3. Finde den ersten belegten Fehler. Wähle einen passenden Prüffall aus `daten/05_PRUEFFAELLE_EG.json`. Fälle T02, T03 und T04 sind besonders klare Tür-/Fenster-Gegenproben.
4. Ändere nur die belegte Ursache. Prüfe den Fehlerfall, den zugehörigen Gegenfall und vorhandene relevante Regressionen.
5. Zeige konkret, welche Ausgabe sich verbessert hat. Unbekannte Zustände als unbekannt ausgeben. Eine gültige Polygongeometrie allein beweist keine korrekte Raumerkennung.

## Nicht als fertige Sollgeometrie importieren

Die roten Umrandungen sind **illustrative Suchkonturen**. Sie sind zum Verstehen und Wiederfinden gedacht. Sie enthalten Abstand zur Originalkante und können zusammenhängend mehrere Bauteile umfassen. Verwende sie nicht als fertige Wandmaske, Kollisionsmodell oder trainingsfertige Ground-Truth. Erzeuge bei Bedarf genaue, separat geprüfte Wand-/Tür-/Fensterannotationen aus dem Original-DXF und dokumentiere deren Herkunft.

Auch die Beispiel-ROIs sind rechteckige Suchbereiche, keine Objektkonturen. Die grünen Flächen sind interpretierte Bodenbereiche, keine exakte Körperfreiraummaske. Pfeile, Markierungen und gedachte Schließlagen sind Kommentare und keine Original-CAD-Bauteile.

## Wichtigste fachliche Fehlerklassen

- Türbögen und Fensterbögen unterscheiden; FPH-Bezug zum UG beibehalten.
- Schiebetüren ohne Drehbogen erkennen; Mehrflügler zu einem Portal bündeln.
- Wandöffnungen beim Vereinigen von Wänden erhalten; beidseitigen Anschluss prüfen.
- Technische Durchbrüche, Glasabschlüsse, Lift- und Schachtflächen nicht als freie Wege behandeln.
- Deckenrechteck der Eingangshalle nicht als Innenwand oder Raum verwenden.
- Dünne feste Trennwände und schräge Außenwände nicht verlieren.
- Sackgasse ist nicht automatisch unbegehbar; sie darf nur keine erfundene Durchverbindung erhalten.
- Treppen samt Lauf, Podest und Geschossinstanz erfassen; Höhenziel nicht aus Blattlage erfinden.

## Zusammenarbeit mit dem UG-Arbeitsstrang

Die sechs Anlagen-IDs in `daten/07_TREPPEN_UEBERGABE_EG.json` verwenden. EG-Ergebnisse in einem eigenen Ergebnisordner führen. Keine UG-Dateien überschreiben und keine gemeinsame Übergabedatei gleichzeitig bearbeiten. Beim späteren Zusammenführen pro Anlage Ausgangsplan, Raumkennung, Geometrie, Richtung, Höhen und offenen Punkt vergleichen. Erst belegte Anschlüsse bestätigen.

## Erwartete Übergabe

- Reproduzierbare Startanweisung und tatsächlicher Commit.
- Übersicht der gefundenen Ursachen mit Originalplan-Belegen.
- Nachvollziehbare Änderungen mit Vorher-/Nachher-Overlays und Zwischendaten.
- Ergebnis pro tatsächlich angeschlossenem Prüffall: bestanden, fehlgeschlagen oder nicht ausführbar, jeweils mit Beleg.
- Liste ungeklärter Objekte und beidseitig noch nicht bestätigter Treppenanschlüsse.

Falls Code oder Laufumgebung fehlen, berichte genau diese Lücke. Das Lesen dieses Pakets ist keine nachgewiesene Integration und verbessert für sich allein keinen produktiven Erkennungslauf.


## Ergänzung der überarbeiteten Fassung
Lies `14_AENDERUNGEN_UND_GEHFLAECHEN.md` und `daten/13_BILDANNOTATIONEN_EG.json`. Verwende die Bildpfeile zum Auffinden konkreter Merkmale. Prüfe Portalverbindungen und Körperabstände am Original, bevor grüne Bereiche zu echten Routen werden.

## Freigegebene Übergabe zur Umsetzung

Der aktuelle Startauftrag steht in `CLAUDE_STARTPROMPT_EG.md`. Nach dem Einlesen soll Claude Code im vorhandenen Repository einen belegten Fehler reproduzieren, die Ursache gezielt bearbeiten und den Vorher-/Nachher-Nachweis führen. `18_UMSETZUNG_UND_UEBERGABE_EG.md` legt die Lesereihenfolge und die erwartete Ergebnisdokumentation fest. Die Engine selbst ist nicht im Lernpaket enthalten.
