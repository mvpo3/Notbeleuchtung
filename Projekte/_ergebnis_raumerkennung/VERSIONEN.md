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

## Lückenstand 2026-09-30

Keine neue Raumerkennungs-Ausgabe: kein Ordner `<Projekt>_vN/`, keine neue Darstellung mit
`scripts/analyse/raumerkennung_darstellung.py`. Dieser Abschnitt hält den Stand fest, auf dem die Lücken aus
`LUECKEN.md` geschlossen bzw. offen geführt sind.

- **Stand:** Branch `luecken-2026-09-30` von `selman/integration-2026-09-30` @ `0434392` (PR #160 offen). Kopf der
  Messung `e0c820d`; der Code-Stand ist `6fe0bb8`, weil `e0c820d` nur `LUECKEN.md` ändert. Die Prüfstrecken-Ergebnisse
  stehen in Commit `8080655`.
- **Punkte** (je ein Commit mit Test, Fix und `LUECKEN.md`-Eintrag; Doku-Punkte ohne Test):
  - 2a `b849dd0`: leerer oder defekter Plan → Warnung und Weiterlauf statt Abbruch (offen: R1-01, `nan`/`inf`- oder
    Phantom-Koordinate)
  - 2b `2016268`: S4g b/c, Balkontür nie `final_exit`, Messfall Südgarten Mollgasse EG; S4g a offen (STOPP)
  - 2c `27de6a0`: K4-privater Loch-Raum zählt für korrigierte Rollen privat, 277 fälschlich gekippte Rollen → 0
  - 2d `22cd85e`: freie Fläche im Wohnungsumriss bekommt einen Raum (4 Zuschläge, 12 neue Räume UNBEKANNT)
  - 2e `d63bc4c`: Entscheidung B, kein Contract-Feld `durchleitung`, Board-Antrag geschlossen (nur Doku)
  - 2f `27478ca`: RAM der Prüfstrecke (Flutmasken als Ausschnitt, Raster-Obergrenze der R-Stufe, Render mit
    Mindeststrich und GC, EG-Restweg einmal je Lauf)
  - 2g `755e06c` (O-04), `5779ef6` (R-05 a), `6fe0bb8` (D-04): Warnungen im Bericht; `e0c820d` Am Rain OG4, F-03 und
    ZERFALL gemessen und offen
- **Gate:** `pytest -m gate tests/gate` ergibt 3 passed, 1 xfailed. Messung `messung_e0c820d` gegen
  `nullmessung_f15d03f`: **1 Verstoß — (3) `M4.einraum` steigt in DG2 von 0 auf 1** (Enis' Board 3). M17: 18/18.
- **Suite:** `pytest -q -rxXs` (voll) ergibt 6 failed, 2255 passed, 11 skipped, 6 deselected, 15 xfailed, 0 xpassed. Die
  6 roten sind bekannt: 3 × WOHNUNG_PRIVAT-Leuchten (Board 1), Muthgasse-Türblöcke und die 2 S4c-Pins (S4c nicht
  angefasst).
- **Prüfstrecke:** 13 Pläne mit `scripts/plan_pruefen.py` in **einem** Lauf mit Plan-Render nach
  `Projekte/_ergebnis/<Plan>/`, Exit 0, Prozess-Spitze 4,18 GB, 4 808 s. Am Rain UG, EG und OG1–OG3 haben damit
  erstmals Bilder. Die Kennzahlen je Plan stehen in `Projekte/_ergebnis/VERLAUF.md` im Eintrag
  „2026-09-30 · Lücken luecken-2026-09-30 @ e0c820d“.

## Phase A 2026-10-01

Keine neue Raumerkennungs-Ausgabe: kein Ordner `<Projekt>_vN/`, keine neue Darstellung mit
`scripts/analyse/raumerkennung_darstellung.py`. Dieser Abschnitt hält den Stand fest, gegen den Phase B (KI an) des
Owner-Auftrags 2026-10-01 (`docs/AUFTRAG_2026-10-01.md`) gemessen wird.

- **Stand:** Branch `luecken-2026-09-30`, Code-Stand `d39a3cf` (Kopf der Phase A). Die Prüfstrecken-Ergebnisse mit
  KI aus stehen in Commit `7727d60` (Vergleichsbasis für Phase B). Leonis testet weiter auf `c3b8186`; der Commit ist
  nicht umgeschrieben. Nichts gepusht.
- **Punkte** (je ein Commit mit Test, Fix und `LUECKEN.md`-Eintrag; Doku-Punkte ohne Test):
  - Abschnitt 0 `dad7bbd`: die 12 `frei_*` aus 2d mit Tabelle und Ausschnittbildern
  - Abschnitt 1 `8748e24`: Kürzel im Raumpolygon sind Typbeleg; Am Rain OG4 `rest_2` „STGH“ → STIEGENHAUS
  - Abschnitt 2 `5f15955`: Stempel vor UNBEKANNT (7 der 12 `frei_*` typisiert)
  - Abschnitt 3 `be9cc57` (Teil A) und `ccd3f96` (Teil B): KI-Zweitmeinung ohne Live-Aufrufe — Schnittstelle, Backends
    `codex_abo`/`openai_api`, Konfiguration, Cache, Entscheidungsregeln, Herkunfts-Ausweis im Bericht
  - Abschnitt 4 `fd5dedb`: Entities mit `nan`/`inf`/> 1e9 mm beim Laden verwerfen, Warnung mit Layer und Handle
  - Abschnitt 5 `54ba4b3`: Ausgang ohne Tür nur, wenn er ins Freie mündet, nie in den Innenhof
  - Abschnitt 6 `9f727a5`: Maßstab über die Tür kalibriert, sonst „Maßstab unsicher“ ohne Leuchten
  - Abo-Regel `d39a3cf`: KI nur über das ChatGPT-Abo
  - Reviews `b61cb4d` (0–2), `7ea3024` (3), `57b013f` (4–6)
- **Gate:** `pytest -m gate tests/gate` ergibt 3 passed, 1 xfailed. Messung `messung_d39a3cf` gegen
  `nullmessung_f15d03f`: **1 Verstoß — (3) `M4.einraum` steigt in DG2 von 0 auf 1** (Enis' Board 3). M17: 18/18.
- **Suite:** `pytest -q -rxXs` (voll) ergibt 7 failed, 2424 passed, 12 skipped, 6 deselected, 15 xfailed, 0 xpassed. Die
  6 erwarteten roten (3 × WOHNUNG_PRIVAT-Leuchten, Muthgasse-Türblöcke, 2 S4c-Pins) und der seit `LUECKEN.md` § 26.4
  bekannte Wächter-Fehlalarm `test_kein_contract_wert_und_kein_konsument` (Codex-Binärsuche, vor dem Push in Phase B).
- **Prüfstrecke:** 13 Pläne mit `scripts/plan_pruefen.py` in **einem** Lauf mit Plan-Render und KI aus nach
  `Projekte/_ergebnis/<Plan>/`, Exit 0, Prozess-Spitze 4,18 GB, 4 806 s. Gegen `c3b8186`: 56 Typwechsel (alle von ohne
  Typ), Ausgänge `final_exit` 16 → 14 und `stair_exit` 23 → 39, Leuchten 560 → 593, kein Maßstab-Faktor geändert.
  Die Kennzahlen je Plan stehen in `Projekte/_ergebnis/VERLAUF.md` im Eintrag
  „2026-10-02 · Phase A Auftrag 2026-10-01 @ 7727d60“, die Liste je Raum, Ausgang und Leuchte in `LUECKEN.md` § 30.
