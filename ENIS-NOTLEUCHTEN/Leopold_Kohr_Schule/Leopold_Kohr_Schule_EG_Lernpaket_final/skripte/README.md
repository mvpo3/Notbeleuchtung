# Werkzeuge

- `python3 skripte/pruefe_paket.py`: Dateistruktur, Bezüge, Originale und Prüfsummen prüfen. Kein Raumerkennungstest.
- `python3 skripte/lese_beispiel.py EG-09`: ein Originalbeispiel lesen.
- `python3 skripte/baue_lernbuch.py`: das vollständige 39-seitige Lernbuch aus den enthaltenen annotierten Bildern und JSON-Texten erneut setzen. Ausgabe ausschließlich unter `_neu_erstellt/`.
- `annotation_data.py`: kuratierte Beschriftungen und normierte Pfeilziele. Absolute Koordinaten im Original-PDF enthält `daten/13_BILDANNOTATIONEN_EG.json`.

Die grünen Flächen, deren Herkunft und die rote Geometrie liegen unter `daten/`. Die Originale bleiben unter `quellen/` unverändert. Die architektonischen Lehransichten sind PDF-Dateien unter `plaene/`.

`herstellung_dokumentation.py` dokumentiert die ursprüngliche Herstellung samt damaligen Arbeitsverzeichnissen; es ist kein portables Startskript. Für den portablen Buchaufbau `baue_lernbuch.py` verwenden.

Aktuelle Inhalte und Nutzerkorrekturen: `../15_UMSETZUNG_DEINER_KORREKTUREN.md`. `herstellung_dokumentation.py` ist eine historische Arbeitsdatei der vorigen Revision; für die aktuelle PDF `baue_lernbuch.py` verwenden.

## Revision 4: Rahmen und Bögen neu erzeugen

Für die PNG-Vorschauen `python3 skripte/erzeuge_markierte_details.py` ausführen. Für die aktuelle PDF zuerst `python3 skripte/erzeuge_markierte_details.py --vector`, danach `python3 skripte/baue_lernbuch.py` ausführen. Der erste Befehl erstellt die 21 in Revision 4 bearbeiteten Detailbilder aus den gespeicherten Koordinaten. Die übrigen Detailbilder und Gesamtpläne sind enthalten und bleiben erhalten. Einzelne aktuelle Details lassen sich etwa mit `python3 skripte/erzeuge_markierte_details.py EG-08 EG-12` neu erzeugen. Der zweite Befehl schreibt das Lernbuch unter `_neu_erstellt/`. Prüfsummen gelten für die ausgelieferte Fassung.

## Scharfe PDF ohne Rasterbilder

`--vector` erzeugt alle 29 Erklärseiten als Vektoren unter `plaene/EG_Erklaerte_Details_Vektor.pdf`. `baue_lernbuch.py` verwendet diese Datei und die ursprünglichen Plan-PDFs. Die PNG-Vorschauen werden nicht in das Lernbuch eingebettet. Siehe `../17_VEKTOREXPORT.md`.
