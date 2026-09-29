# Auftrag zum Einlesen und Umsetzen

Arbeite mit diesem vollständigen Lernpaket für das **2. OG der Leopold-Kohr-Schule (SH22-LKS)**. Lies zuerst `START_HIER.md`, `CLAUDE.md`, das freigegebene `pdf/2OG_Lernbuch.pdf` und die zugehörigen Markdown-/JSON-Dateien.

Du sollst die Erkennungsmerkmale verstehen und sie anschließend im bestehenden Raumerkennungsprojekt ausprobieren und sinnvoll umsetzen. Bleibe nach dem Einlesen nicht bei einer Zusammenfassung stehen.

1. Prüfe das Paket mit `python3 skripte/pruefe_paket.py`. Ordne Originalquelle, Lernmarkierung und noch ungeprüftes Ergebnis klar zu.
2. Lies die Projektanweisungen und finde den echten Einstiegspunkt der vorhandenen Raumerkennung. Halte Branch/Commit, Arbeitsstand und Aufruf fest. Übernimm keine fremden uncommitteten Änderungen als deine eigenen.
3. Führe zunächst die unveränderte Erkennung auf der enthaltenen Original-2OG-DXF aus, sofern die bestehende Laufzeit verfügbar ist. Bewahre diesen Ausgangslauf für den Vergleich auf.
4. Vergleiche die Ergebnisse mit den 25 Lernbeispielen und dem Originalplan: Mauern, Türen, Fenster, Glas, Absturzsicherungen, Wartungsbereiche, Bodenverbindungen und Treppen. Nutze auch Originaltexte in `daten/roh/texts_pdf.json` und konkrete DXF-Handles.
5. Wähle einen belegten Fehler aus, ermittle seine Ursache und verbessere die passende allgemeine Erkennungsregel. Keine Sonderbehandlung mit hart codierten 2OG-Koordinaten. Die Handkonturen aus diesem Lernpaket nicht einfach als Erkennungsergebnis zurückgeben.
6. Führe den geänderten Lauf aus und kontrolliere betroffene Stellen sowie vorhandene relevante Prüfungen. Ein durch eine echte Wand laufender Weg, ein Fenster als Tür oder ein Geländer als massive Wand darf nicht als Erfolg gelten.
7. Erzeuge einen prüfbaren Ergebnisordner mit Ausgangs- und Ergebnisdaten, farbigem Kontroll-PDF, `BEFUND.md`, `OFFEN.md` und dem reproduzierbaren Aufruf. Fülle die 25 Prüffälle mit Ergebnis und Begründung aus. Das Austauschschema liegt unter `schemata/ERKENNUNGSERGEBNIS.schema.json`; falls das Projekt ein anderes Format nutzt, erhalte dieses und ergänze einen dokumentierten Adapter.

Bei neuen Erklärbildern gelten alle Vorgaben aus dem Lernbuch: rote Mauerkörper, ein geschlossener Rahmen und ein Pfeil je erklärtem Wandstück, direkt markierte Tür-/Fensterlinien, grüne Bodenflächen und weiterhin sichtbare schwarze Stufenlinien.

Nicht belegte Höhen, Anschlussgeschosse, Türzustände oder Körperfreiräume bleiben ausdrücklich offen. Erklärrahmen sind keine Bauteilkonturen. Breitenfragen sind hier geometrische Freiraumfragen und kein neuer baurechtlicher Normenauftrag. Die Notleuchtenplatzierung ist nicht Teil dieses Schritts.

Wenn ein echter Lauf mangels Repository, Einstiegspunkt oder Laufzeit nicht möglich ist, erledige die übrige Quellen-/Codeanalyse und benenne genau den konkreten Blocker. Erfinde keinen erfolgreichen Lauf. Abschließend berichte kurz: was gelesen wurde, was tatsächlich ausgeführt wurde, welche Änderung erfolgt ist, welchen Vergleich es gibt und wo alle Ergebnisdateien liegen.
