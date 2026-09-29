# Paketprüfung · 21.09.2026

## Durchgeführt

- Original-PDF und Original-DXF: SHA-256-Abgleich mit den UG-Quellverweisen aus dem vorhandenen V3-Paket. Übereinstimmung bei beiden Dateien.
- Acht überlappende Bereiche des gesamten UG-Plans visuell betrachtet. Außen- und Innenwände, Türstellen, Treppenbereiche und die Randbereiche wurden am Originalkontext geprüft.
- Alle 54 Buchseiten gerendert und in Seitenübersichten visuell geprüft; die 19 beschrifteten Lernbilder und die neuen Schemen zusätzlich groß betrachtet. Eine versetzte Treppenmarkierung wurde auf die Originalgeometrie korrigiert. Keine abgeschnittenen Textblöcke oder überdeckten Lerntexte festgestellt.
- Türdetail und Treppen-Seitenansicht zusätzlich mit Poppler gerendert. Der bestehende rote Wandplan ist unverändert. Der grüne Gesamtplan wurde in acht Bereichen visuell geprüft; die Treppen-Querlinien und Lauflinien bleiben schwarz sichtbar.
- Alle 91 PNG-Dateien geöffnet und vollständig dekodiert.
- PDF-Seitenzahl, Seiten-IDs und 54 Lesezeichen auf Konsistenz geprüft.
- JSON-Syntax sowie das Antwortschema nach JSON Schema Draft 2020-12 geprüft; die Beispielantwort T01 erfüllt das Schema.
- Paketdateien, SHA-256, lokale Markdown-Verweise, Ausschnittgrenzen sowie Zuordnung der 19 Lernfälle zu den 19 Erwartungsfällen und 19 beschrifteten Bildern mit `werkzeuge/paket_pruefen.py` geprüft. Die acht grünen Bildausschnitte und sechs erklärten Endmarken sind referenziert.
- Die grüne Flächengeometrie überschneidet sich nicht mit den verwendeten roten Wandflächen. Dies ist ein Konsistenztest dieser Lernmarkierungen, keine unabhängig geprüfte Kollisions- oder Körperbreitenberechnung.
- Original-PDF, Original-DXF und separater roter Wandplan sind bytegleich zur vorherigen ZIP. Die Grafik der ersten Buchseite blieb erhalten; nur die Seitenzählung wurde aktualisiert.

## Genauigkeit der roten Markierungen

Die roten Umrandungen sind ungefähre Lernmarkierungen um Materialdarstellungen, einschließlich fester Stützen. Sie wurden aus zerlegten Mustern der Originalzeichnung gewonnen und in acht Bereichen visuell betrachtet. Sie bilden keine unabhängig vermessene, pixelgenau vollständige Wandmaske. Eine zusammenhängende Umrandung kann mehrere Wände umfassen; ihre Anzahl ist keine Wandanzahl.

Feine Schichtgrenzen, Öffnungsbreiten und Raumflächen sind an den Originalkanten auszuwerten. Bauteile mit ungeklärter Höhenlage können nicht allein anhand der roten Farbe als raumhohe Sperre auf jedem Niveau gelten.

## Genauigkeit der grünen Markierungen

Grün kennzeichnet dargestellte Boden-, Gang- und Treppenbereiche bei nutzbaren Türen. Die Flächen wurden aus ausgewählten Bodenbereichen abzüglich der ungefähren Wandumrandungen, Lift-/Schachtbereiche und ausgewählter fester Einbauten erstellt. Ihre Genauigkeit reicht zum erklärenden Lesen des Plans, nicht zum automatischen Nachweis eines menschlichen Bewegungsraums. Die Farbabstufung ist keine zusätzliche Raumgrenze.

Die Endmarken E1–E6 erklären konkrete Situationen; sie sind kein vollständiger Wegegraph. Ein Endbereich kann betreten werden, obwohl er keine weitere Verbindung bietet. Die zwei Zusatzschemen zeigen Fenstermerkmale und einen Treppenlauf von der Seite; sie sind ausdrücklich keine neuen vermessenen UG-Bauteile.

## Offen und ausdrücklich nicht als geprüft ausgegeben

| Frage | Stand |
|---|---|
| Eindeutige Fensterpositionen im UG | Keine bestätigt; Regeln und Gegenbeispiele dokumentiert |
| Absolute Anfangs-/Endhöhen der Treppen | Anschlussabgleich mit Schnitt, Legende oder Nachbargeschoss erforderlich |
| Heutiger Öffnungs- und Sperrzustand der Türen | Aus der Quelle nicht bekannt |
| Körperbezogene freie Wegbreite | Nicht berechnet; keine pauschale Mindestbreite erfunden |
| Vollständiger Wegegraph / Ausgangs- oder Fluchtwegnachweis | Nicht Bestandteil des Lernpakets |
| Aktueller Rivoplan-Commit und Implementierung | In dieser Paketprüfung nicht verifiziert oder geändert |
| Claude-Code-Leistung an den Lernfällen | Erwartungsreferenzen vorhanden, noch kein Modelltest ausgeführt |

`pruefung/erwartungen.json` enthält Sollantworten für eine spätere Auswertung. Die Integritätsprüfung des Pakets ist keine Erfolgsmessung der Raumerkennungssoftware.

## Erneut prüfen

Im entpackten Paket ausführen:

```bash
python3 werkzeuge/paket_pruefen.py
```

Das Skript benötigt nur die Python-Standardbibliothek und prüft die ausgelieferten Dateien, nicht den Projektcode. `MANIFEST.json` enthält alle Paketdateien außer sich selbst.

## Nachprüfung zur Nutzerkorrektur K1

K1 beruht auf einer ausdrücklichen Nutzerbestätigung, nicht auf einer unabhängigen Ortsbesichtigung. Die Seiten 2, 3, 12, 38, 39 und 54 sowie die veränderten grünen Ausschnitte wurden erneut gerendert und visuell geprüft. Die grüne Beispielstelle überschneidet sich nicht mit den verwendeten roten Wandflächen. Paketintegrität und Verweise wurden nach Aktualisierung erneut geprüft.
