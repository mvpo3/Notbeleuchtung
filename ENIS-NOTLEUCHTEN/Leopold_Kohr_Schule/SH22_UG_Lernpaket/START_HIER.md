# SH22 · Untergeschoss · Lernpaket

**Beginne mit `plaene/SH22_UG_Alle_Mauern_Rot.pdf`. Mauern sind rot markiert.**

Dieses Paket erklärt ausschließlich das Untergeschoss der Leopold-Kohr-Schule (SH22): Mauern, Türen, Fenster, freie Wege und Treppen. Die überarbeitete Fassung enthält ein **54-seitiges Lernbuch**, den roten Gesamtplan und zusätzlich den **Gesamtplan mit grün gefüllten Bodenflächen**. Zu allen 19 projektbezogenen Lernfällen gibt es jetzt eine zusätzliche Seite mit farbigen Merkmalen, Pfeilen und direkt zugeordneten Beschriftungen. Die Quell-DXF und der Quell-PDF-Export sind unverändert enthalten.

## Für dich

1. `SH22_UG_Lernbuch.pdf` öffnen. Die erste Seite zeigt wie bisher den gesamten UG-Plan mit roten Mauern. Seiten 2–3 zeigen und erklären die grünen Bodenflächen. Danach folgen die Bereichsübersicht und die Detaillektionen mit jeweils einer direkt beschrifteten Bildseite.
2. Für große Vergrößerungen `plaene/SH22_UG_Alle_Mauern_Rot.pdf` verwenden. Die Originalgeometrie bleibt als Vektorgrafik erhalten.
3. Bei jedem Detail Beobachtung, Begründung, Folge und offene Frage zusammen lesen.
4. Für den grünen Gesamtplan `plaene/SH22_UG_Begehbare_Flaechen_Gruen.pdf` öffnen. Treppen sind grün hinterlegt; Stufen und Lauflinien bleiben schwarz sichtbar. Die markierten Endbereiche E1–E6 werden im Buch erklärt.

## Für Claude Code

Paket in einen eigenen Ordner entpacken. Diesen Auftrag mit dem tatsächlichen Pfad verwenden:

> Lies zuerst `<PAKETPFAD>/START_HIER.md`, danach `<PAKETPFAD>/CLAUDE_CODE_AUFTRAG.md`. Arbeite nur am SH22-Untergeschoss. Lies die sieben Dateien unter `wissen/`, verwende `daten/lernfaelle.json`, `daten/bildmarkierungen.json` und die Originalquellen. Beantworte jeden Lernfall mit sichtbaren Belegen und offenen Fragen. Prüfe deine Antworten gegen `pruefung/erwartungen.json`. Behandle die roten und grünen Markierungen als Lernhilfen, nicht als exakte Kollisionsgeometrie.

Bei späterer Arbeit am Rivoplan-Code gelten zuerst der aktuelle Repositorystand und seine Projektanweisungen. Bestehende `CLAUDE.md`-Dateien nicht mit diesem Lernpaket überschreiben.

## Inhalt

| Pfad | Zweck |
|---|---|
| `SH22_UG_Lernbuch.pdf` | Durchgehendes Lernbuch mit Originalausschnitten |
| `plaene/SH22_UG_Alle_Mauern_Rot.pdf` | Vollständiger UG-Plan mit roter Wandumrandung |
| `plaene/SH22_UG_Begehbare_Flaechen_Gruen.pdf` | Grün gefüllte Bodenflächen, schwarze Treppen und erklärte Endbereiche |
| `quellen/` | Original-DXF, Original-PDF und SHA-256-Nachweise |
| `wissen/` | Sieben Fachdateien zu Mauern, Türen, Fenstern, Wegen, Treppen und den neuen Bildmarkierungen |
| `lektionen/` | Einzelne ausführliche Lernfälle als Markdown |
| `bilder/` | Original- und Rotfassungen der Ausschnitte, ein Wegebeispiel |
| `bilder/beschriftet/` | Große Bildseiten mit farbigen Merkmalen, Pfeilen und Texten |
| `bilder/gruen/` | Acht grüne Bereichsausschnitte zum Vergrößern |
| `daten/lernfaelle.json` | Lernfälle mit Belegen, Sollantworten und Fehlinterpretationen |
| `daten/ausschnitte.json` | Eindeutige PDF-Koordinaten und Seitenbezüge |
| `daten/rote_markierungen.json` | Ungefähre rote Umrandungen, ausdrücklich keine Kollisionsmaske |
| `daten/bildmarkierungen.json` | Merkmale und Pfeilziele der 19 beschrifteten Lernbilder |
| `daten/gruene_flaechen.json` | Ungefähre grüne Flächen, ausgesparte Bereiche und Endmarken |
| `daten/ergebnis.schema.json` | Struktur für Claude-Antworten |
| `pruefung/erwartungen.json` | Noch auszuführende Aufgaben für Claude bzw. den Projektcode |
| `pruefung/PRUEFBERICHT.md` | Tatsächlich durchgeführte Paketprüfung |
| `werkzeuge/paket_pruefen.py` | Lokale Dateiintegrität und Datenkonsistenz prüfen |

## Vier wichtige Leseregeln

- Rot zeigt erkannte Wand- und Mauerbereiche sowie feste Stützen. Die Umrandung hat einen kleinen Darstellungsabstand. Höhe, Projektion und tatsächliche Begehbarkeit werden zusätzlich geprüft.
- Türen sind geplante Zugangsmöglichkeiten. Ihr aktueller Öffnungs- oder Sperrzustand ist aus diesem Blatt nicht bekannt.
- Grün ist eine geometrische Lernmarkierung bei nutzbaren Türen. Heller grüne Räume sind nicht automatisch Durchläufe; die Körperbreite und alle beweglichen Hindernisse sind damit nicht vermessen.
- Im geprüften UG-Blatt ist kein Fenster eindeutig lokalisiert. Das ist eine dokumentierte offene Zuordnung, kein Beweis für ein fensterloses Gebäude. Absolute Geschossanschlüsse der Treppen bleiben ebenfalls zu bestätigen.

Das Paket ist Lern- und Arbeitsmaterial. Es enthält keine Behauptung, dass Claude dadurch dauerhaft trainiert wurde oder dass eine Softwarekorrektur bereits umgesetzt ist.

## Korrektur K1 vom 21.09.2026

Der bei Punkt 2 auf Buchseite 39 gezeigte Bereich ist laut Nutzerbestätigung begehbar. Die Aussage und Markierung sind auf Seiten 12, 38 und 39 sowie im grünen Gesamtplan korrigiert. W04, Sollantwort und Bildmarkierungen wurden angepasst. Quelle: `daten/nutzerkorrekturen.json`. Die grüne Beispielmarkierung ist keine neue Wand oder vollständige Flächengrenze.
