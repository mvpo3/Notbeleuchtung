# SH22 · 1. OG · Lern- und Umsetzungspaket für Claude Code

Stand: 21.09.2026, nach den Korrekturen an Absturzsicherung und Außenerschließung.

Dieses Paket enthält die Unterlagen, damit Claude Code den Plan lesen, die Beispiele nachvollziehen und die Raumerkennung in der vorhandenen Software gezielt verbessern kann. Es gehört ausschließlich zum **1. Obergeschoss der Leopold-Kohr-Schule / SH22**.

## Einstieg

1. Das gesamte ZIP entpacken und den Ordner für Claude Code zugänglich machen.
2. Claude den Auftrag aus **CLAUDE_AUFTRAG.md** geben. Alle darin genannten Pfade beziehen sich auf diesen Paketordner.
3. Zuerst Paket und Quellen prüfen, dann die bestehende Engine untersuchen und gezielt ändern.
4. Die tatsächlichen Engine-Ergebnisse mit den Lernfällen vergleichen und die Abweichungen dokumentieren.

## Was enthalten ist

| Inhalt | Einstieg |
|---|---|
| Lernbuch, 61 Seiten | `01_PDF/SH22_1OG_Lernbuch.pdf` |
| Gesamtplan mit roten Wand- und Sicherungsmarkierungen | `01_PDF/SH22_1OG_Mauern_Rot.pdf` |
| Gesamtplan mit grünen Gehflächen | `01_PDF/SH22_1OG_Gehflaechen_Gruen.pdf` |
| Unveränderter Originalplan und vollständige Original-DXF | `02_Originalquellen/` |
| Fachliche Regeln und Umsetzungsanleitung | `03_Wissen/` |
| 24 Lernfälle mit Koordinaten und Buchseiten, 15 Regeln, 37 Prüffälle | `04_Daten/` |
| Datenverträge für Lernfälle und Engine-Ausgabe | `05_Schemas/` |
| Ausführbare Prüf-, Koordinaten- und Ausschnittwerkzeuge | `06_Werkzeuge/` |
| Bericht über die Prüfung dieses Pakets | `07_Pruefung/PRUEFBERICHT.md` |

Zusätzlich enthalten: 3.074 Textfragmente mit DXF-Handles, 1.209 ausgewählte Randsicherungslinien, ein komprimierter Geometriekontext und die für die PDF-Markierungen verwendeten Referenzflächen.

## Erste Prüfung

Im entpackten Paketordner:

```bash
python3 06_Werkzeuge/pruefe_paket.py
```

Diese Prüfung benötigt nur Python. Die weiteren Werkzeuge nutzen die Bibliotheken aus `06_Werkzeuge/requirements.txt`; sie sollten in der vorhandenen Projektumgebung oder einer gesonderten virtuellen Umgebung installiert werden.

```bash
python3 -m pip install -r 06_Werkzeuge/requirements.txt
python3 06_Werkzeuge/dxf_belege_pruefen.py
python3 06_Werkzeuge/ausschnitte_rendern.py --case W06 --out ../SH22_Pruefbilder
```

Berichte und Engine-Ergebnisse außerhalb dieses Paketordners ablegen. Dadurch bleibt die Prüfsummenprüfung eindeutig.

## Was „Lernmaterial“ hier bedeutet

Claude liest Regeln, Originalbelege und Gegenbeispiele und überträgt sie in Parser, Geometrieverarbeitung, Klassifizierung und Tests der vorhandenen Engine. Das ZIP trainiert kein Modell automatisch und installiert keine fertige Raumerkennung.

Die enthaltenen Flächen sind die Lernmarkierungen der geprüften PDFs. Sie sind **keine vollständige, vermessene Raumsegmentierung**. Türen und Fenster werden anhand konkreter Beispiele erklärt; eine vollständige Liste aller Türen und Fenster muss die Engine aus der Original-DXF ermitteln. Die vollständige DXF liegt dafür bei.

Die drei Lern-PDFs sind unverändert aus dem zuletzt akzeptierten Arbeitsstand übernommen. Ihre bisherige Bezeichnung „Prüffassung“ und der Hinweis auf das spätere GO bleiben als Teil dieses Dokuments erhalten; dieses Paket ist die anschließend angeforderte Übergabe.
