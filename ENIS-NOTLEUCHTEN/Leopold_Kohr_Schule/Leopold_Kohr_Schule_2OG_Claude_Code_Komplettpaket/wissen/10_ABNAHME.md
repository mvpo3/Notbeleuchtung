# Was als nachvollziehbares Ergebnis zählt

## Paketprüfung

`skripte/pruefe_paket.py` prüft Dateivollständigkeit, Hashes, JSON-Strukturen, Beispiele, Rahmen und Pfadverweise. Mit `--erweitert` werden PDF-Seiten/Vectorstatus, Geometrien und das Ergebnisformat geprüft. Das ist eine Paketprüfung, kein Qualitätswert der Raumerkennung.

## Fachliche Kontrolle des späteren Versuchs

- Quelle und Geschoss stimmen, der Ausgangslauf und der geänderte Lauf sind vorhanden.
- Wände/Öffnungen werden am Original belegt; es gibt keine durch Handmasken kaschierte Erkennung.
- Die jeweils betroffenen Fälle aus `daten/11_PRUEFFAELLE.json` wurden mit Ausgangs- und Folgestand verglichen.
- Neue oder geänderte Verbindungen laufen nicht ohne Öffnungsbeleg durch feste Grenzen.
- Fenster, Glas, Brüstung, Absturzsicherung, Wartungsbereich, Aufzug und Treppe bleiben getrennt.
- Die Unsicherheit eines Höhen- oder Türzustands wird sichtbar und nicht durch einen plausibel klingenden Wert ersetzt.
- Die vorgeschlagenen Verbesserungen sind allgemein und nicht auf diese Planrechtecke festgeschrieben.

Für eine quantitative Trefferquote fehlen vollständige unabhängig annotierte Objektgrenzen und ein vollständiger Verbindungsgraph. Daher keine erfundene Genauigkeit in Prozent angeben. Konturanzahl, JSON-Validität oder grüne Pixel sind kein Ersatz für den Vergleich.

## Ergebnisdateien

`vorlagen/BEFUND.md` und `vorlagen/OFFEN.md` geben eine Struktur vor. `vorlagen/ERGEBNIS_VORLAGE.json` steht ausdrücklich auf `nicht_ausgefuehrt`. Erst tatsächliche Daten ändern diesen Status. `skripte/pruefe_erkennung.py` prüft Format und Referenzen, nicht die geometrische Wahrheit der Erkennung.
