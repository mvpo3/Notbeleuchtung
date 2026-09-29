# Werkzeuge

Alle Werkzeuge arbeiten lokal. Sie greifen nicht auf ein Repository, einen Dienst oder ein KI-Modell zu und führen keine Notbeleuchtungspipeline aus.

## Paket prüfen

`python3 06_Werkzeuge/pruefe_paket.py`

Standardbibliothek, Python 3.10+. Nicht zwischenzeitlich Dateien ändern und anschließend die mitgelieferten Prüfsummen als unverändert bezeichnen. Eigene Engine-Ausgaben außerhalb dieses Referenzpakets speichern oder bewusst in einen Arbeitsordner kopieren.

## Tatsächliches Erkennungsergebnis prüfen

`python3 06_Werkzeuge/pruefe_erkennung.py /pfad/bericht.json`

Erwartet das in `07_Schemata/pruefergebnis.schema.json` beschriebene Ergebnis. Exitcode 0 nur bei vollständigen, gültig belegten und mit dem Soll übereinstimmenden 32 Fällen; sonst 1. Das Programm schreibt einen JSON-Bericht auf stdout, Fehler beim Dateilesen nach stderr.

`evidence_by_claim` enthält je Aussage mindestens einen Eintrag mit `source_id`, `source_locator`, `engine_reference` und `explanation`. Tatsächliche Objekte/Prüfwerte nennen. Der Prüfer kontrolliert Vorhandensein und Mindeststruktur, nicht die Wahrheit frei eingetragener Beschreibungen. Unabhängige Sichtprüfung bleibt erforderlich.

## JSON-Schemata prüfen (optional)

In der bestehenden Projektumgebung mit verfügbarer Bibliothek `jsonschema`:

`python3 06_Werkzeuge/pruefe_schemata.py`

Prüft die mitgelieferten Datensätze gegen Draft 2020-12 sowie den leeren Prüfbericht als zulässige Vorlage. Die inhaltliche Ergebnisprüfung lehnt diese Vorlage anschließend trotzdem als nicht ausgeführt ab. Das sind verschiedene Prüfzwecke.

## Originalbeleg ansehen (optional)

Mit verfügbarer Bibliothek `PyMuPDF`:

`python3 06_Werkzeuge/zeige_beleg.py D01 --output /pfad/D01.svg`

Zeigt den Originalausschnitt mit 1:1 aus den gespeicherten Beleggeometrien nachgezeichneten Linien, Kurven, Punkten und erklärenden Pfeilen. Die Beschriftung nennt jede Farbe lokal. Keine künstlichen Objektkästen. SVG lässt sich im Browser öffnen. Dies ist ein Lernbeleg, kein aus einer Produktionsengine erzeugtes Resultat.

## Prüfwerkzeuge testen

`python3 -m unittest discover -s 06_Werkzeuge/tests -v`

Die Tests prüfen konkrete Fehlerrisiken des Übergabeformats: `not_run` darf nicht bestehen, fehlende Belege dürfen nicht bestehen, falsche Fenster-/Portal-Aussage muss fehlschlagen, Bool und Zahl dürfen nicht gleichgesetzt werden, unbekannte/duplizierte Fälle müssen auffallen, andere Quellenhashes dürfen nicht bestehen. Synthetische Testwerte beweisen keine Architektur-Erkennungsleistung.
