# Prüfung und Abnahme

## Was bereits geprüft wird

Die Paketprüfung prüft SHA-256, Dateivollständigkeit, 87 Seitenindexeinträge, 32 Beispiele, 134 Merkmale, Seiten-/ID-Verweise, Koordinatengrenzen, Regeln, offene Punkte und 32 Sollfälle. Sie prüft nicht die Qualität einer noch nicht ausgeführten Engine.

Die enthaltene Lern-PDF wurde im vorherigen Arbeitsschritt visuell geprüft und ist bytegleich zur freigegebenen Fassung. In diesem Paket wird sie weder gekürzt noch neu erzeugt.

## Lokale Befehle

Aus dem entpackten Paketordner:

```bash
python3 06_Werkzeuge/pruefe_paket.py
python3 -m unittest discover -s 06_Werkzeuge/tests -v
python3 06_Werkzeuge/pruefe_erkennung.py 05_Pruefung/ergebnis_vorlage.json
```

Der dritte Befehl muss bei der leeren Vorlage **fehlschlagen**: 32 Fälle sind noch nicht ausgeführt. Dies ist Absicht. Ein Dateipaket darf sich nicht selbst eine bestandene Raumerkennung bescheinigen.

Nach einem tatsächlichen Engine-Lauf:

```bash
python3 06_Werkzeuge/pruefe_erkennung.py /pfad/zum/tatsaechlichen_ergebnisbericht.json
```

Windows: `py -3` statt `python3`. Der Prüfer benötigt keine externe Bibliothek. Für optionale Schema-/SVG-Prüfung werden `jsonschema` beziehungsweise `PyMuPDF` verwendet; siehe `06_Werkzeuge/README.md`.

## Fachliche Abnahme der 32 Fälle

Der Adapter liefert alle 32 Fall-IDs genau einmal. Jede erwartete Aussage muss aus realen Ergebnisobjekten bzw. Geometrieprüfungen berechnet werden. Pro Aussage steht ein konkreter Originalbeleg und eine Referenz auf das tatsächliche Engine-/Prüfergebnis. Eine Quelle nur zu nennen oder den PDF-Text als Engine-Antwort zu kopieren genügt nicht.

Mindestbedingungen:

- Keine neu erfundene Verbindung durch Wand, Fensterbrüstung, Schacht oder Absturzsicherung.
- Keine zusätzlichen Räume aus Türbogen, Maßlinie, Gefälle oder Möbelkontur.
- Keine verlorenen belegten freien Zwischenräume durch grobe Möbel-Sammelflächen.
- Raum, freie Fläche, Nutzungszone und Route bleiben verschiedene Ergebnisse.
- Unbekannte Material-, Glas-, Betriebs- oder Geschossangaben bleiben offen.
- Jede Klassifikation und jede kritische Verbindung ist am Original lokalisierbar und in ihrer Wirkung erklärt.

Ein bestandener semantischer Bericht bedeutet zunächst nur, dass die gemeldeten Aussagen konsistent zu den 32 Sollfällen sind. Es bleibt zu prüfen, ob der Adapter die richtigen tatsächlichen Objekte und Geometrien auswertet. Deshalb 32 Detailstellen und Gesamtgeschoss visuell gegen Original und Engine-Overlay vergleichen.

## Zusätzliche Geometrieprüfung im Zielrepo

Prüfe Raum-/Freiflächen auf Gültigkeit, Innenringe und unbeabsichtigte Überschneidungen. Prüfe jeden Portalschnitt gegen feste Sperrflächen. Prüfe Treppen-/Liftkanten gegen Höhen- und Zugangsmodell. Weise physische Engstellen nur mit bestätigter Einheit, Maßstab und Bewegungsprofil nach. Lege Toleranzen projektspezifisch begründet fest; das Paket schreibt keine willkürliche universelle Pixeltoleranz vor.

Die 32 Lehrstellen sind keine Vollinventur. Zähle weder 32 Fälle als 32 Bauteile noch 30 Registerzeilen als Raumanzahl. Für eine vollständige Bestandsabnahme sind alle produktiven Räume, Öffnungen und Flächen des Geschosses gesondert zu prüfen.

## Regressions- und Übertragbarkeitsbericht

Zeige vor/nach der Änderung dieselben Quellen mit demselben Evaluationsumfang. Berichte fehlerhaft, bestanden und ungeprüft getrennt. Bereits bewährte unabhängige Pläne erneut auswerten, wenn die betroffene Logik sie beeinflusst. Ein neuer Plan bekommt eigene Quellbelege; SH22-Koordinaten sind kein allgemeines Erkennungswissen.
