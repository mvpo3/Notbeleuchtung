# ADR-0003 — Blatt-Modus: das Blatt trägt alles

**Status:** bindend · **Datum:** 2026-09-05 (Owner-Fixierung an
`wohnbau_v7_dg_verbessert.dxf`) · Nachtrag 2026-09-06

**Entscheidung:** Liegt die Rivoplan-Vorlage im Repo, werden ALLE Zusatz-Boxen
unterdrückt (LB-Legende, Stückliste, Prüfbericht-Box, Belegungsliste, alter
Plankopf). Befunde leben im Summary/API + als DXF-Zeichnungseigenschaften.
PROJEKT-Feld bleibt leer (Owner trägt ein).

**Nachtrag (Owner-GO 2026-09-06):** EIN Feld IM Blatt ist sanktioniert — das
PRÜFVERMERK-Feld (Status + Zählung + Photometrie-Vorbehalt). Es ist ein
Vermerk, kein Bericht.

**Konsequenz für Tests:** Sichtbarkeits-Tests gezeichneter Boxen laufen auf dem
Fallback-Pfad (`ohne_blatt`-Pattern) — dagegen sind 2026-09-05/06 zwei
Enis-Tests gelaufen.
