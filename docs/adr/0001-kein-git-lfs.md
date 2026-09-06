# ADR-0001 — Kein Git-LFS

**Status:** bindend · **Datum:** 2026-08-28 · **Owner:** Leonis (User-GO)

**Kontext:** ~923 MB Binär-Assets (CAD, Norm-PDFs) im privaten Repo.

**Entscheidung:** Kein LFS. Große Roh-CAD-Bestände projektweise zippen
(Muster: `Projekte/Baufeld_E2.zip`); `_extracted_text/` ist lokal verzichtbar.

**Begründung:** Free-LFS-Limits (1 GB Storage + 1 GB/Monat Bandbreite) wären
sofort erschöpft; Migration = Historie-Umschreiben + Force-Push für alle.

**Kippen kostet:** Neu-Klonen aller drei Owner + Force-Push-Fenster.
