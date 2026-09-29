# Prüfung des Übergabepakets

Stand: 21.09.2026. Gegenstand: SH22, 1. OG.

## Übernommene Unterlagen

Vier PDFs sind enthalten: das 61-seitige Lernbuch, der rote Gesamtplan, der grüne Gesamtplan und der einseitige Originalplan. Die drei Lern-PDFs entsprechen bytegenau den zuletzt bereitgestellten Fassungen. Die vollständige Original-DXF liegt ebenfalls bei.

## Daten und Belege

- 24 Lernfälle, 15 Regeln und 37 ausgewählte Prüfaussagen.
- 3074 originale Textfragmente und 1209 ausgewählte Randsicherungselemente.
- Lernfälle gegen das beigefügte JSON-Schema geprüft; Fall-IDs und Buchseiten abgeglichen.
- Neun originale DXF-Linienanker und fünf Textbelege erfolgreich geprüft.
- Größter Unterschied bei den geprüften Linienankern: 0 PDF-Punkte.
- Koordinatenumrechnung in beide Richtungen geprüft.
- Die geänderten PDF-Stellen wurden während ihrer Erstellung visuell kontrolliert. In diesem Paket wurden die PDFs unverändert übernommen.

## Mitgelieferte Werkzeuge

Die Python-Dateien wurden syntaktisch geprüft. Die Bewertung wurde mit kontrollierten Referenzfixtures für W06 (3 Aussagen) und W02 (7 Aussagen) erprobt. Ein fehlender Boden, eine fehlende Textzuordnung zur Absturzsicherung und eine falsche Quell-SHA wurden gezielt als Fehler erkannt. Dies prüft das Werkzeug, nicht eine echte Engine.

Der Ausschnittrenderer wurde für W06 mit Originalausschnitt und Lernbuchseite ausgeführt. Details der Quellen- und Werkzeugprüfung stehen in `quellpruefung.json` und `werkzeugpruefung.json`.

Geprüfte Laufzeit: Python 3.12.14, ezdxf 1.4.4, Shapely 2.1.2, PyMuPDF 1.26.6, jsonschema 4.26.0.

## Vollständigkeit selbst prüfen

`MANIFEST.json` dokumentiert den Dateibestand. `SHA256SUMS.txt` umfasst alle ausgelieferten Dateien außer sich selbst. Der Prüfsummenbestand wird nach Erstellung des Pakets kontrolliert; die ZIP wird zusätzlich auf CRC-Fehler und identischen Dateiinhalt geprüft.

```bash
python3 06_Werkzeuge/pruefe_paket.py
```

## Noch kein Engine-Ergebnis

Es wurde keine Engine des Nutzers gestartet oder geändert. Das Paket enthält keinen behaupteten erfolgreichen Erkennungslauf. Die vollständige Raumsegmentierung, das Öffnungsinventar und die Integration in das tatsächliche Repository sind der anschließende Auftrag an Claude Code.
