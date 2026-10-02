# KI-Cache der Zweitmeinung (Raumerkennung, Abschnitt 3)

Gespeicherte Antworten der KI-Zweitmeinung je Geschoss (`raumerkennung/ki_zweitmeinung.py`,
Owner-Auftrag 2026-10-01 § 3, Entscheid 3). Gleiche Frage → keine neue Anfrage; Suite und
Gate rufen die KI nie live auf, sie lesen nur hier.

- **Ort:** die Engine liest den Cache zur Laufzeit, also weder unter `tests/` noch im
  Paket; `knowledge/` ist der getrackte Ort für Wissensdaten außerhalb des Codes
  (`scripts/wissen_index.py` indiziert hier nur `extracted/**/*.md`).
- **Schlüssel = Pfad:** `<plan>_<sha16>/<geschoss>_<quadrant|ganz>_<backend>_<modell>_v<prompt>.json`
  — Plan-Datei (SHA-256 des Inhalts, 16 Hex), Geschoss, Quadrant, Backend, Modell,
  Prompt-Version. Ändert sich eine Zutat, entsteht ein neuer Eintrag; alte bleiben. Die
  Eichung (Stempel abgedeckt, `KiKonfig.stempel_abdecken`) ist eine eigene Frage und trägt
  die Kennung `v<prompt>-eichung` — sie liest nie die Antwort des Normallaufs.
- **Inhalt:** `schluessel`, `gespeichert` (UTC), `raeume` (gültig: raum_id, raum_typ aus dem
  Kanon `docs/VOKABULAR.md` § 1 oder UNBESTIMMT, sicherheit 0–1, bestaetigt, begruendung),
  `verworfen` (Räume außerhalb Kanon / unbekannte ID), `roh` (Antworttext). Beim Lesen wird
  `roh` neu geprüft — ein strengerer Kanon wirkt ohne neuen Aufruf.
- **Nie gecacht:** Fehler (Limit, Login, Zeitüberschreitung, Format) — sie werden beim
  nächsten Lauf neu gefragt. Keine lokalen Pfade, keine Login-Daten, kein Key.
