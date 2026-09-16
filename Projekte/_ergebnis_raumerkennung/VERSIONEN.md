# Raumerkennung — Versionen

Jede neue Raumerkennungs-Ausgabe ist ein eigener Ordner `<Projekt>_vN/`. Ein bestehender
Versionsordner wird nie neu geschrieben; `Rennweg/` ohne Suffix ist v1. Jede Version steht hier
mit dem Code-Stand und den Fixes, auf denen sie gerechnet wurde.

Darstellung in allen Versionen: nur Räume (keine Fluchtwege, keine Ausgänge, keine Platzierung),
Skript `scripts/analyse/raumerkennung_darstellung.py`.

| Version | Ordner | Datum | Commit | Branch | Slices | Pläne |
|---|---|---|---|---|---|--:|
| v1 | [Rennweg/](Rennweg/README.md) | 2026-09-13 | `511ad36` | `main` | keine | 7 |
| v2 | [Rennweg_v2/](Rennweg_v2/README.md) | 2026-09-16 | `59583ff` | `selman/rennweg-stand` | S1, S2, S5a, S3a, S9 | 7 |

## v1 — Rennweg/

- **Stand:** `511ad36` auf `main`, ausgegeben mit Commit `1ad01f4`. Raumerkennung vor der
  Diagnose (`docs/DIAGNOSE_RENNWEG_RAUMERKENNUNG.md`, Branch `selman/diagnose-rennweg`).
- **Fixes:** keine.
- **Eingang:** `Projekte_Leere Architektpläne (Input)/Rennweg/`, 7 Grundrisse (UG, EG, OG1–OG3,
  DG1, DG2). SHA-256 je Plan in `Rennweg/<Plan>/kennzahlen.json`.

## v2 — Rennweg_v2/

- **Stand:** `59583ff` = Integrationsbranch `selman/rennweg-stand`. Basis `origin/main` `2f610cc`,
  darauf die fünf Fix-Branches der ersten Tranche und die versionierte Darstellung gemergt
  (je ein Merge-Commit, alle konfliktfrei).
- **Testschranke auf `59583ff`:** `pytest -q` → 1392 passed, 74 skipped, 2 deselected, 2 xfailed.
- **Eingang:** `Projekte_Leere Architektpläne (Input)/Rennweg.zip` (SHA-256 `9c9f0dc5…9358`), frisch
  entpackt nach `_arbeit/eingang_rennweg_v2/Rennweg/` (Arbeitsverzeichnis, nicht versioniert).
  7 DXF, alle 7 Grundrisse, kein Schnitt, keine Ansicht, keine Legende. SHA-256 je Plan gleich wie v1.
- **Offen vor Merge nach `main`:** Merge-Gates aus Diagnose 5.2 — S1/S2/S9 Messung auf
  Barawitzka, Mollgasse, Muthgasse; S3a Nachmessung nach dem Türstapel.

| Slice | Branch | Kopf | Ursache | Inhalt |
|---|---|---|---|---|
| S1 | `selman/fix-s1-aussen-loch-topologie` | `13243b3` | U7 | Loch-Topologie statt Randtoleranz: ein Loch ohne Außen-Indiz ist nie AUSSEN (F7 = Option A) |
| S2 | `selman/fix-s2-aussen-innenzonen` | `771d078` | U8 | Innen-Zonen werden aus dem Außenbereich ausgeschnitten (Fachregel S-C, F6 = Option 4); gestapelt auf S1 |
| S5a | `selman/fix-s5a-durchgang-guard-kein-raum` | `41ba292` | U13 | kein synthetischer Durchgang ohne Türblatt an KEIN_RAUM-Räumen (SCHACHT/LIFT) |
| S3a | `selman/fix-s3a-rest-schacht-evidenz-vor-treppenmarker` | `6aea78a` | U2 | Schacht-Evidenz im Polygon vor der Treppenmarker-Regel (Komponente < 3 m²); gestapelt auf S5a |
| S9 | `selman/fix-s9-treppe-anhaengen-huelle` | `8fa0613` | U1 | Treppen-Anhang nur bei ungedeckter gedrehter Hülle; die Hülle wird das Polygon |

Zusätzlich gemergt, keine Änderung an der Erkennung: `selman/darstellung-versioniert` (`8699766`) —
Versionsordner, Bildtitel mit Version/Datum/Commit/Slices, Kennzahlen Schächte und
Außenbereich-Überlagerung mit Kanon-Räumen, NISCHE magenta mit Hinweis.
