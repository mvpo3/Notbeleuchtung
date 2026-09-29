# Arbeitsauftrag: Raumerkennung im SH22-Untergeschoss

## Ziel

Begründe am Originalplan, welche Bauteile den freien Raum begrenzen, an welchen Stellen echte Öffnungen bestehen und welche Verbindungen daraus folgen. Arbeite ausschließlich im UG. Die Raumnutzung und einzelne Sanitärgegenstände sind hier keine Lernziele.

## Verbindliche Reihenfolge

1. `quellen/QUELLEN.json` und `daten/koordinaten.json` lesen. Originaldateien und SHA-256 prüfen. Keine Ausschnittkoordinaten aus anderen PDF-Exporten übernehmen.
2. `plaene/SH22_UG_Alle_Mauern_Rot.pdf` ansehen. Alle acht Bereiche Z01–Z08 in `daten/ausschnitte.json` prüfen: außen herum, dann innere Trennwände, schmale Nebenbereiche und Randbereiche.
3. `wissen/01_MAUERN.md` bis `wissen/05_TREPPEN.md` lesen. Zugehörige Detaillektionen und Originalbilder öffnen.
   Anschließend `wissen/06_GRUENE_FLAECHEN.md` und `wissen/07_BESCHRIFTETE_BILDER.md` lesen. Bei jedem der 19 Fälle die beschriftete Bildseite zusätzlich zum Original prüfen. Pfeile, Farben und Tür-Schließstellungen sind Lernmarkierungen und keine zusätzlichen CAD-Objekte.
4. Die Lernfälle aus `daten/lernfaelle.json` bearbeiten. Zu jeder Entscheidung konkrete Bildmerkmale und den Quellenausschnitt nennen.
5. Die Antwort gegen `pruefung/erwartungen.json` prüfen. Abweichungen sichtbar erklären; keine Sollantwort als ausgeführten Softwaretest ausgeben.

## Erkennungslogik

- Wandkörper aus Rändern, Materialmustern, Anschlüssen und örtlicher Darstellung ableiten. Quelllayer sind Hinweise, keine vollständigen semantischen Klassen.
- Türen aus Wandöffnung, Flügel, Anschlag, Schwenkbogen und lokalen Angaben gemeinsam erkennen. Ein Bogen ist nicht grundsätzlich eine Tür.
- Fenster nur bei ausreichenden Öffnungs- und Rahmenbelegen bestätigen. Mehrere parallele Linien reichen nicht. `daten/fensterstatus.json` erhalten, solange keine neuen Belege vorliegen.
- Freie Flächen, Raumgrenzen und Verbindungen getrennt modellieren. Eine virtuelle Trennlinie im Türportal schließt Räume, darf aber die Türverbindung nicht blockieren.
- Ein Weg braucht belegten Boden, Platz und Übergänge. Nicht durch Wände, Glasflächen, Schächte, Treppenaugen oder ungeklärte Blattbereiche routen.
- Treppen benötigen Stufenfolge und passenden Kontext. Richtung im Bild, Aufstiegsdarstellung und absoluter Höhenanschluss sind verschiedene Informationen.
- Brüstungen und Handläufe separat erfassen. Nicht raumhoch bedeutet nicht frei durchgehbar.

## Antwortformat

Das Schema `daten/ergebnis.schema.json` verwenden. Ein plausibles Beispiel liegt in `daten/beispielantwort_T01.json`. Pro Fall angeben:

1. Fall-ID und Objektrolle;
2. konkrete sichtbare Belege;
3. Quell-PDF, Blatt und Ausschnittkoordinaten, gegebenenfalls DXF-Handles;
4. Art der Begehbarkeit bzw. Verbindung;
5. offene Fragen und ausgeschlossene Fehlinterpretationen.

Für komplexe Ausschnitte mehrere Objektantworten erstellen. Ein Ausschnitt ist kein einzelnes Objekt und kein Raum-Polygon. Nicht belegte Höhen und Verbindungen nicht mit Standardwerten auffüllen. Keine scheinpräzisen Wahrscheinlichkeiten erfinden.

## Wenn daraus Codeänderungen entstehen

Vor einer Änderung den tatsächlichen aktuellen Projektstand und die dortigen Anweisungen lesen. Das Paket behauptet keinen geprüften aktuellen Commit. Die JSON-Fälle sind Eingaben und Erwartungsreferenzen, kein vorhandener Adapter für eine bestimmte Codebasis. Eine konkrete Integration muss die verfügbaren Funktionen und Datenstrukturen des aktuellen Repositorys verwenden.

Exakte Geometrie aus den Originalkanten ermitteln. Die rote Lernmarkierung nicht als Trainingswahrheit für Pixelmasken, Raumflächen oder Kollisionsgeometrie übernehmen. Für die Körperbreite eine explizite Anforderung verwenden, keine pauschal erfundene Breite. Türen zustandsabhängig behandeln; unklare Geschossanschlüsse bleiben offen.

Dasselbe gilt für die neuen grünen Flächen: Sie sind eine planbezogene Lesehilfe, keine vermessene Freigabe jeder Stelle für einen bestimmten Körper. Das Fensterschema F03 und das Treppenschema S07 erzeugen keine neuen Projektobjekte oder Geschossanschlüsse.

## Abschlusskriterien

- Alle Lernfälle besitzen eine belegte Antwort oder eine begründete offene Zuordnung.
- Keine Route quert nachgewiesenes Mauerwerk oder einen Schacht.
- Türöffnungen bleiben als Verbindungen erhalten, ohne die Räume zu verschmelzen.
- Kein Fenster und keine UG–EG-Treppenkante wurde ohne Beleg ergänzt.
- Tatsächlich ausgeführte Prüfungen und noch offene Aufgaben werden getrennt berichtet.

## Korrektur K1 vom 21.09.2026

Der bei Punkt 2 auf Buchseite 39 gezeigte Bereich ist laut Nutzerbestätigung begehbar. Die Aussage und Markierung sind auf Seiten 12, 38 und 39 sowie im grünen Gesamtplan korrigiert. W04, Sollantwort und Bildmarkierungen wurden angepasst. Quelle: `daten/nutzerkorrekturen.json`. Die grüne Beispielmarkierung ist keine neue Wand oder vollständige Flächengrenze.
