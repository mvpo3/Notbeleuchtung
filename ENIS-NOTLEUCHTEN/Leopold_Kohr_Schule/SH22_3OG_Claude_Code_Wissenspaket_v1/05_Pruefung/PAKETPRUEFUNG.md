# Prüfung des Übergabepakets · 23.09.2026

Die folgenden Prüfungen wurden bei der Erstellung tatsächlich durchgeführt:

- Die freigegebene 87-seitige PDF ist bytegleich enthalten. SHA-256: `108f4c5b5524baf6673cce3a75e2007598db25f5511a6771e4be785bfea6d040`.
- Original-PDF und zugehörige 3.-OG-DXF sind mit ihren eigenen Prüfsummen enthalten.
- 32 Lernbeispiele, 134 Merkmale und die Seiten-/Datei-/Regelverweise wurden auf Konsistenz geprüft.
- Alle 134 exportierten Markierungen stimmen in Merkmal, PDF-Seite, Anzahl der gezeichneten Pfade und Anzahl der Originalpfad-Indizes mit dem finalen Annotationsprüfbestand überein.
- Alle sechs JSON-Schema-Definitionen wurden formal geprüft; fünf zugeordnete JSON-Datensätze bestanden die vollständige Schema-Prüfung.
- Zwölf synthetische Tests des Ergebnisprüfers bestanden. Sie prüfen Berichtskonsistenz und gezielte Fehlermeldungen, keine Architektur-Erkennung.
- Der absichtlich leere Engine-Bericht wurde korrekt abgelehnt: 0 bestandene, 32 nicht ausgeführte/fehlgeschlagene Fälle, Exitcode 1.
- Die optionale D01-Quellenvorschau wurde erzeugt und visuell kontrolliert.
- Manifest und Paketprüfsummen bestanden die Integritätsprüfung. Das Archiv wird aus genau den verzeichneten Dateien erzeugt.

Eine reale Projektengine wurde hier nicht ausgeführt. Es wurden keine Änderungen am Repository, keine trainierten Modellgewichte und keine gemessene Erkennungsquote geliefert. Diese Nachweise entstehen erst durch die Umsetzung und Prüfung in Claude Code. Die beigefügten 104 Soll-Aussagen sind ein konkreter Prüfauftrag, kein bereits erzieltes Softwareergebnis.
