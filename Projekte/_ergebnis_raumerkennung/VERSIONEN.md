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

## Integrationsstand 2026-09-30

Keine neue Raumerkennungs-Ausgabe: kein Ordner `<Projekt>_vN/`, keine neue Bildausgabe. Dieser
Abschnitt hält den Stand fest, auf dem Leonis die Platzierung testet.

- **Stand:** `bc2ccf0` auf `selman/integration-2026-09-30`. Basis `origin/main` `acdacba`. Der Code-Stand
  ist `ed292e1`, weil `bc2ccf0` nur `docs/` ändert (`src/` und `scripts/` sind baumgleich). Die Merge-Reihe und
  die Konfliktauflösungen stehen in `docs/INTEGRATION_2026-09-30.md`.
- **Slices:**
  - S4a, S4b
  - S5b + S7a + S7b
  - S4c Fassung A (mit S7c, S3b, S5c)
  - VOK-a
  - K2 (M3-Regel NISCHE wie SCHACHT)
  - K3
  - K4 (R1-Aussetzung, Aufenthaltsraum-Sperre)
  - Gate-Doku von `selman/uebernahme-enis-m17`
  - P0 Am Rain: `a845ded` Test rot, `ed292e1` Fix, `bc2ccf0` Doku

  Nicht enthalten ist der K1-Fix Sofa-Feld. Er existiert nicht.
- **Gate:** `pytest -m gate tests/gate` ergibt 3 passed, 1 xfailed. Messung `messung_ed292e1` gegen
  `nullmessung_f15d03f`: **1 Verstoß — (3) `M4.einraum` steigt in DG2 von 0 auf 1.** Er hängt an Enis'
  Board 3 (Blatt-Semantik). M17: 18/18.
- **Suite:** `pytest -rxXs tests/naht tests/raumerkennung tests/gate` ergibt 6 failed, 1216 passed,
  8 skipped, 4 deselected, 14 xfailed, 0 xpassed. Die 6 roten sind bekannt: 3 × WOHNUNG_PRIVAT-Leuchten (Board 1),
  Muthgasse-Türblöcke und die 2 S4c-Pins.
- **Prüfstrecke:** 13 Pläne mit `scripts/plan_pruefen.py` nach `Projekte/_ergebnis/<Plan>/`, alle ohne
  Traceback:
  - die 5 Prüfpläne
  - Mollgasse 1KG und 2KG
  - Am Rain UG, EG, OG1–OG4

  Am Rain UG, EG und OG1–OG3 liefen ohne Plan-Render, weil die Render-Stufe den Arbeitsspeicher
  sprengt. Dort liegen nur `bericht.md` und `raeume.json`. Die Kennzahlen je Plan stehen in
  `Projekte/_ergebnis/VERLAUF.md` im Eintrag „2026-09-30 · Integration selman/integration-2026-09-30 @ bc2ccf0“.
