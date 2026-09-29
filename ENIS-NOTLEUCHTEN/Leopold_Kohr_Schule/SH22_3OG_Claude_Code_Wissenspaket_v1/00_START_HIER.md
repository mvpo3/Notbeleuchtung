# SH22 · Leopold-Kohr-Schule · 3. OG
## Wissens- und Umsetzungspaket für Claude Code · Version 1.0

Dieses Paket übergibt die vom Nutzer akzeptierte **87-seitige PDF unverändert**, sämtliche ausführlichen Lerntexte, 32 lokale Lernbeispiele, 134 Einzelmarkierungen, Original-PDF und Original-DXF sowie einen konkreten Umsetzungs- und Prüfauftrag. Freigabe: Der Nutzer hat nach Sichtung der PDF dieses Begleitpaket beauftragt.

**Beginne mit `CLAUDE_CODE_STARTPROMPT.md`.** Es ist der Auftrag, den du in Claude Code zusammen mit dem entpackten Ordner verwendest. Das Paket enthält Wissensgrundlage und ausführbare Prüfwerkzeuge. Die Raumerkennungsengine wurde in dieser Umgebung nicht geändert oder ausgeführt; die Implementierung erfolgt im tatsächlichen Repository.

## Schneller Einstieg

1. ZIP vollständig entpacken. Alle relativen Pfade beziehen sich auf diesen Paketordner.
2. Im Terminal des Paketordners ausführen: `python3 06_Werkzeuge/pruefe_paket.py` (Windows alternativ `py -3`). Dafür ist nur Python 3.10 oder neuer erforderlich.
3. `CLAUDE_CODE_STARTPROMPT.md` an Claude Code geben und den lokalen Paketpfad nennen.
4. Claude liest die aktuellen Regeln im tatsächlichen Zielrepository, ordnet die vorhandene Erkennungspipeline zu und setzt das Wissen dort in überprüfbaren Teilschritten um.
5. Ergebnisse anhand `05_Pruefung/akzeptanzfaelle.json` und der Originalpläne nachweisen. Eine bloße Zusammenfassung der MD-Dateien erfüllt den Umsetzungsauftrag nicht.

## Was liegt wo?

| Pfad | Inhalt / Zweck |
| --- | --- |
| `01_PDF/` | Genau die zuletzt freigegebene PDF, 87 Seiten |
| `02_Originale/` | Originalplan und zugehörige DXF des 3. OG |
| `03_Wissen/LERNBUCH_VOLLSTAENDIG.md` | Vollständiger Autoren-Lerntext, nach PDF-Seiten geordnet |
| `03_Wissen/Beispiele/` | 32 einzeln abrufbare Beweisketten W01 bis G01 |
| `03_Wissen/UMSETZUNGSPLAN.md` | Reihenfolge der Umsetzung und konkrete Nachweise |
| `03_Wissen/DATENVERTRAG.md` | Evidenz, offene Angaben, Geometrie und Raum-/Wegmodell |
| `03_Wissen/FREIE_BODENFLAECHE.md` | Vollständige Bodenflächen, Hindernisse und Portale |
| `03_Wissen/TEXT_UND_HOEHE.md` | Plantextzuordnung, Maßkonventionen, Höhenbezüge |
| `03_Wissen/VISUELLE_AUSGABE.md` | Direkte Linien, Pfeile und flächiges Grün |
| `04_Daten/` | Regeln, Beispiele, Einzelmarkierungen, Textfragmente, Register, offene Punkte |
| `05_Pruefung/` | Sollfälle, leere Ergebnisvorlage, Prüfprotokoll |
| `06_Werkzeuge/` | Offline-Paketprüfung, Ergebnisprüfung und optionale Belegvorschau |
| `07_Schemata/` | Maschinenlesbare JSON-Datenverträge |
| `MANIFEST.json` / `SHA256SUMS.txt` | Vollständigkeit und Prüfsummen |

## Vier Grenzen, die Claude verstehen muss

- Dies ist **SH22 / Leopold-Kohr-Schule / 3. OG**. Mollgasse, Barawitzkagasse, Rennweg und andere Geschosse sind keine Quellen dieses Pakets.
- Die Koordinaten der Lernbelege sind Fundstellen im Originalplan. Ein Bildausschnitt ist **keine Raumkontur**. Die roten/grünen Übersichten sind didaktische Darstellungen und keine millimetergenaue Vermessung.
- Regeln werden aus Merkmalkombinationen verallgemeinert. Die Engine darf keine SH22-Koordinaten, Raum-IDs oder Beispiel-IDs als fest programmierte Erkennungsantworten verwenden.
- Ein Wissenspaket ändert keine Modellgewichte. Erfolg bedeutet: die Engine erzeugt nach der Codeänderung am Originalinput nachvollziehbar bessere Bauteile, Räume, freie Flächen und Verbindungen. Das muss separat gemessen werden.

Die zusätzlichen Projektanhänge aus anderen Projekten wurden nicht als SH22-Fachwissen übernommen. Die mitgelieferten älteren Repository-Anweisungen dienten nur dazu, bestehende Zuständigkeiten und lokale Regeln nicht zu übergehen; sie ersetzen nicht den aktuellen Stand des Zielrepositories.
