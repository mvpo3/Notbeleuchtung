# Farben, Pfeile und Beschriftungen auswerten

Die überarbeitete Fassung enthält zu jedem der 19 Lernfälle eine zusätzliche beschriftete Bildseite. In `../daten/bildmarkierungen.json` stehen die farbig hervorgehobenen Merkmale, die Texte und die Pfeilziele.

## Was die Markierung leistet

Jeder Pfeil endet an einem konkret gemeinten Merkmal des Ausschnitts. Der Text erklärt, was dort zu sehen ist und warum es für die Einordnung relevant ist. Die farbigen Linien und Flächen sind Erläuterungen des Originalplans, keine neu entdeckten CAD-Elemente.

Bei Mauern werden unter anderem Schraffur, Schichtgrenzen, Anschlüsse, raumseitige Kante und Rücksprung hervorgehoben. Bei Türen werden offenes Türblatt, Drehpunkt, Schwenkbogen, Wandöffnung und die geschlossene Stellung getrennt gezeigt.

## Ergänzte geschlossene Türstellung

Die grün gestrichelte Linie in T01–T03 zeigt erklärend, wo das Türblatt beim Schließen liegt. Sie ist eine abgeleitete Pose derselben Tür. Sie darf weder als neue Wand noch als zweite Tür in die Erkennung eingehen. Das Modell soll Blatt, Drehpunkt und Bogen dem gemeinsamen Portal zuordnen.

## Zwei Arten von Bildern

1. **Projektbezogene Originalausschnitte mit Markierungen:** M01–M04, T01–T03, F01–F02, W01–W04 und S01–S06. Die Datei nennt jeweils die tatsächliche Quelle und den Ausschnitt.
2. **Schematische Erklärungen:** F03_SCHEMA zeigt ein allgemeines Fenster in Draufsicht und Schnitt; S07_SEITE zeigt einen aus der Beschriftung erklärten Treppenquerschnitt. Beide sind ausdrücklich keine neue UG-Geometrie.

Das Fensterschema darf keine Fensterposition oder Fensteranzahl im SH22-UG erzeugen. Das Treppenschema darf ohne bestätigte Höhenbindung keine UG–EG-Verbindung erzeugen.

## Koordinaten

Merkmalspunkte sind in einem Ausschnitt auf 0 bis 1 normiert, Ursprung links oben. Die Pfeilziele stehen zusätzlich in PDF-Punkten. Es sind visuell zugeordnete Suchstellen, keine vermessenen CAD-Eckpunkte. Für exakte Geometrie auf Original-DXF bzw. Original-PDF zurückgehen.
