# Prüfung und Ergebnisvergleich

## Paket und Quellen prüfen

```bash
python3 06_Werkzeuge/pruefe_paket.py
python3 06_Werkzeuge/dxf_belege_pruefen.py --out ../SH22_Ergebnisse/quellpruefung.json
```

Die erste Prüfung kontrolliert Dateibestand, SHA-256, JSON-Lesbarkeit und Querverweise. Die zweite öffnet die Original-DXF, kontrolliert neun Linienanker und fünf Textbelege und prüft die Registrierung in PDF-Koordinaten.

Fehlende oder abweichende Dateien zuerst klären. Die Prüfdateien nicht so ändern, dass ein unpassendes Ergebnis plötzlich besteht.

## Engine-Ausgabe exportieren

Der Adapter erzeugt ein JSON gemäß `05_Schemas/engine_ergebnis.schema.json` mit:

- `result_kind: "engine_prediction"`, `floor_id: "1OG"` und der vorgegebenen Koordinatenkennung.
- Der SHA-256 der tatsächlichen Eingabe-DXF aus `04_Daten/quellen.json`.
- `engine_name` als Bezeichnung des tatsächlich ausgeführten Systems beziehungsweise Code-Stands.
- Klassifizierten `features` mit Geometrie und Begründung.
- Bestätigten `portals` mit Öffnungsabschnitt und zwei angrenzenden Flächen-IDs.

Ein leerer Export oder eine unvollständige Platzhalterdatei ist kein Nachweis. Deshalb liegt keine vorgetäuschte fertige Engine-Ausgabe bei.

## Ausgewählte Lernfälle bewerten

```bash
python3 06_Werkzeuge/bewerte_engine_ergebnis.py ../SH22_Ergebnisse/engine_ergebnis.json --out ../SH22_Ergebnisse/vergleich.json
python3 06_Werkzeuge/bewerte_engine_ergebnis.py ../SH22_Ergebnisse/engine_ergebnis.json --case W06
```

Exit-Codes: 0 = alle ausgewählten Aussagen erfüllt, 1 = mindestens eine Aussage nicht erfüllt, 2 = Eingabe- oder Schemafehler.

Die Suite umfasst 37 Aussagen zu Wandstellen, freiem Boden, Möbeln, Innenrand, Quellklassifizierung, Textzuordnung, drei Türportalen, unzulässigen Portalen an Fenstern/Sicherung und einer Treppen-Höhenverbindung.

`walkable_at` betrachtet freie Bodenflächen, `class_at` die Objektklasse am Prüfpunkt. `source_class` prüft die Klassifizierung bestimmter Quellhandles. `label_binding` verlangt die gemeinsame Zuordnung der genannten Textfragmente zu einer Sicherung. `portal_matches` vergleicht den Portalabschnitt einschließlich umgekehrter Endpunktreihenfolge. `height_transition` prüft die Kennzeichnung einer Treppe als Höhenwechsel.

Die Portal-Toleranz von vier PDF-Punkten dient der Registrierung dieses Lernvergleichs. Sie ist keine zulässige reale Bauabweichung. Bei Liniengeometrien erlaubt die Klassenpunktprüfung 0,5 PDF-Punkte Abstand; Flächen werden direkt mit ihren Polygonen geprüft.

Unklare Elemente mit `evidence.status: "uncertain"` erfüllen keine positiven Erkennungsprüfungen. Sie bleiben als offene Kandidaten erhalten. Unsichere Portale werden nicht als aktive Verbindungen gewertet.

## Visuell vergleichen

```bash
python3 06_Werkzeuge/ausschnitte_rendern.py --case W02 --out ../SH22_Pruefbilder --dpi 180
python3 06_Werkzeuge/ausschnitte_rendern.py --case W06 --out ../SH22_Pruefbilder --dpi 180
```

Das Werkzeug rendert den Originalausschnitt und die zugehörige erklärte Lernbuchseite. Die Engine-Ausgabe daneben im selben Koordinatenbezug darstellen. Pixelpositionen eines Screenshots nicht als Originalkoordinaten verwenden.

Bei der manuellen Kontrolle besonders beachten:

1. Vollständiger Wandaufbau und geschlossene Ecken; keine künstlichen Wanddurchgänge.
2. Raumkonturen unabhängig von Möbelstücken und Schwenkbögen.
3. Tatsächliche Öffnungen mit Anschluss an zwei passende freie Bereiche.
4. Fenster ohne gewöhnliche Durchgangskante.
5. Randsicherungen als eigene Klasse und ohne Durchtritt.
6. Durchgängige Gehfläche in Z03 bis an die gezeichnete Sicherung sowie Anschluss an die Treppe.
7. Treppenstufen, Podeste und Höhenwechsel weiterhin erkennbar.
8. Ungeklärte Fälle mit Quelle und Ursache im Bericht.

Zusätzlich die tatsächliche Raumzahl, Raumnamen und komplette Nachbarschaftsstruktur überprüfen. Dafür enthält dieses Paket kein vorgegebenes vollständiges Sollinventar. Ein bestandener Punktvergleich ersetzt diese Gesamtprüfung nicht.

## Ergebnisbericht für den nächsten Schritt

Nenne Code-Stand, Eingabe-SHA, Konfiguration, geänderte Module, bestandene und fehlgeschlagene Aussagen, Vorher/Nachher-Ausschnitte und verbleibende Fehler. Stelle klar, welche Aussagen aus der Quelle kommen und welche neu von der Engine abgeleitet wurden.

Erst anhand dieses konkreten Ergebnisses entscheiden, ob weitere Fehler in Import, Klassifizierung, Flächenbildung oder Verbindungsbildung liegen. Die Notleuchtenplatzierung benötigt diese räumliche Grundlage, wird mit diesem Paket aber nicht selbst implementiert.
