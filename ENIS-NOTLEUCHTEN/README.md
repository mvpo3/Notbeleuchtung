# ENIS-NOTLEUCHTEN — Wissenssammlung für Raumerkennung und Notbeleuchtung

Von Enis zusammengestellt, damit **Selman (Raumerkennung)** und **Leonis (Platzierung)**
daraus lernen können, wie Räume, Türen, Ausgänge und Fluchtwege in Architekturplänen
richtig erkannt werden. Außerdem enthält sie die Vorschriften, auf denen die
Notbeleuchtungsplanung aufbaut. Der Ordner ist Nachschlage- und Lernmaterial. Er ist kein
Produktcode und kein Contract, und die Pipeline liest ihn nicht automatisch.

## Inhalt

| Ordner / Datei | Inhalt |
|---|---|
| `OIB Richtlinie …` / `OIB-Richtlinie …` (15 Ordner) | OIB-Richtlinien 1–7, Ausgabe Mai 2023, jeweils mit Erläuterungen und Änderungen, dazu Begriffsbestimmungen, zitierte Normen und Leitfäden |
| `Wissen vom Interent/` | Notbeleuchtung Österreich, Antipanikleuchte, Raumerkennung (Lernbuch und Buch Architektur) |
| `Wissen vom Internet Pt2/` | Grundrisse lesen, Plandarstellung (ÖNORM A 6240, Lernskripte), `OIB/` Kurzfassungen, `Schulwissen/` (ÖNORM A/B-Blätter, EN 13501-2 u. a.) |
| `Aichholz/Lernen/<Geschoss>/` | Raumerkennungs-Lernbücher zur Kontrolle je Geschoss (1UG … 4.OG, DG) |
| `Leopold_Kohr_Schule/` | Lernbücher und Lernpakete je Geschoss (UG, EG, 1OG, 2OG, 3OG): Anleitungen für Claude Code, Originalquellen (DXF), Daten (JSON/GeoJSON), Bilder, Skripte, Prüfsummen |
| `J.pdf` | Einzeldokument |

Jedes Lernpaket unter `Leopold_Kohr_Schule/` hat eine eigene Startdatei
(`START_HIER.md`, `00_START_HIER.md` oder `CLAUDE.md`), mit der man anfangen sollte.

## Hinweise

- **Umbenannt:** Auf dem Mac trugen die OIB-Ordner einen Doppelpunkt im Namen
  (`OIB-Richtlinie 2:Brandschutz`). Windows verbietet `:`, deshalb steht hier ` - `
  (`OIB-Richtlinie 2 - Brandschutz`). Leerzeichen am Namensende wurden entfernt. Sonst ist
  der Ordner unverändert: Alle Dateien sind bytegleich, per SHA-256 geprüft. Nur die
  `.DS_Store`-Dateien wurden weggelassen.
- **Fehlt bewusst:** `Buch1/Buch_rekonstruiert.pdf` („Darstellung und Gestaltung —
  Rekonstruktion aus Fotos", 428 Seiten, 351 MB). Es überschreitet das GitHub-Limit von
  100 MB je Datei und wird später separat hochgeladen.
- **`.gitignore`:** Das Repo ignoriert `*.pdf` und `*.dxf`, weil diese Endungen sonst für
  Engine-Ausgaben stehen. Neue Dateien in diesem Ordner deshalb mit `git add -f` hinzufügen.
