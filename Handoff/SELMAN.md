# Handoff — Selman (Raumerkennung)

> Claude: Du bist die Session von **Selman**. Owner-Package:
> `src/notbeleuchtung/raumerkennung/`. GitHub `@polatselman`. Task: **Issue #3**.
> Lies zuerst `CLAUDE.md`, `docs/CONTRACTS.md`, `docs/ONBOARDING.md` (Abschnitt Selman).

## 0. Setup — Claude, führe das ZUERST für den Nutzer aus

Du bist ein Agent — **führe diese Schritte selbst aus**, frag nicht lang nach.

1. **Prüfe den Arbeitsordner:** du musst im Repo-Root `Notbeleuchtung/` sein
   (`pyproject.toml` + `CLAUDE.md` liegen hier). Wenn nicht → sag dem Nutzer:
   „Öffne den Ordner `Notbeleuchtung` (Cursor: File → Open Folder → Notbeleuchtung)
   und starte mich dort neu." Erst weiter, wenn der Ordner stimmt.
2. **venv + Installation:**
   - Windows: `python -m venv .venv` → `.venv\Scripts\python.exe -m pip install -e ".[dev,api]"`
   - Mac/Linux: `python3 -m venv .venv` → `.venv/bin/python -m pip install -e ".[dev,api]"`
3. **Tests grün prüfen:** `.venv\Scripts\python.exe -m pytest -q` → muss zeigen
   **`13 passed, 1 skipped`**. Wenn nicht → stopp + melde dem Nutzer den Fehler.
4. **Cursor-Hinweis für den Nutzer:** Ordner `Notbeleuchtung` als Workspace öffnen
   und `.venv` als Python-Interpreter wählen (unten rechts / Command Palette
   „Python: Select Interpreter" → `.venv`).

Erst wenn Setup grün ist → weiter mit dem Auftrag unten.

## Wer du bist
Du machst den **1. Input**: leerer Architekturplan (DXF/DWG) → **RaumModell**
(Räume/Türen/Ausgänge/Fluchtweg-Zirkulation). Reine Geometrie/Topologie — KEIN
Norm-Urteil (das macht Enis/Leonis). Dein Contract: `RaumModell`
(`hauptengine/contracts/raum_modell.py`), dein Protocol: `RaumProvider`.

## Dein Auftrag — Slice 4 (größter Port, deshalb solide angehen)
Das Port-Material liegt schon im Repo (Leonis hat es gestaged, du hast keinen
elektro-planer-Zugriff): **`raumerkennung/_port/`** (~14,4k LOC — `parsers/`,
`engine_walls/`, `models/`). Es ist ROH und läuft noch nicht (alte Imports). Deine
Aufgabe (Details: `raumerkennung/_port/README.md`):

1. **Imports umbiegen** auf die neue Struktur (`engine.walls` → `._port.engine_walls`,
   `parsers.x` → `._port.parsers.x`).
2. **`config.py`-Kopplung brechen:** harte Mollgasse-Pfade (`CANONICAL_BLANK_DIR`,
   Referenz-DXF) optional/`.env`; nur `RULES_DIR`/`resolve_rule_path` behalten.
3. **Zirkular-Import** `keller_geometry` ↔ `architecture_dxf` sauber trennen.
4. **`ArchitekturRaumProvider.parse(dxf, floor)`** (`raumerkennung/provider.py`)
   erfüllt `RaumProvider` → liefert ein `RaumModell`, schema-gleich zu
   `tests/fixtures/raum_modell_4og.json`. Test-Pläne: `Projekte/`.
5. **Fake ersetzen:** `tests/fakes.py` `FakeRaumProvider` → echt; E2E mit echter
   4OG-DXF grün.

**Tipp:** nicht alles auf einmal. Erst `architecture_dxf` + `keller_geometry`
importierbar machen → Räume/Türen extrahieren → dann Fluchtweg-Zirkulation
(`segmente`) füllen. Zwischendrin `pytest -q` grün halten.

**DoD:** echtes RaumModell aus 4OG-DXF, schema-identisch zur Fixture;
`tests/contract/test_raum_modell_contract.py` grün.

## Regeln
Nur `raumerkennung/` + `hauptengine.contracts` importieren (der `_port`-Code darf
intern untereinander importieren). Contract ändern = version bump + gen_schema +
3-Owner-Approval. Branch `selman/…` → PR.

## STAND (append-only, neueste oben) — für nahtloses Weitermachen

### 2026-08-29 — S0 fertig (Branch `selman/raumerkennung-dxf`)
**Ansatz (entschieden):** NICHT die 14.4k-LOC `_port/` reanimieren, sondern schlanker
Neubau in `raumerkennung/`, der die *sauberen* Port-Helfer wiederverwendet:
- `._port.parsers.room_faces.extract_room_faces` — Wand-Segmente → Raum-Polygone (pure).
- `._port.models.room.classify_room` + `GERMAN_ROOM_TYPE_MAP` — Stempel→RoomType (pure).
Plan-Datei: `.claude/plans/du-bist-fenster-delightful-wozniak.md`.

**Gebaut:** `provider.py` (`ArchitekturRaumProvider.parse` Stub, erfüllt Protocol),
`__init__.py` export, `tests/raumerkennung/{conftest,test_scaffold}.py`. Suite grün
(69 passed). Baseline-Info: volle Suite ist heute **69** (nicht mehr 13/1 aus Handoff).

**Datenlage (DXF-Inspektion):** Mollgasse `Projekte/Mollgasse Notbeleuchtung/WHA_MOL_*.dxf`
= mm ($INSUNITS=4, Koords ~65k). Layer: Wände `02-TWA*/02-ZWA*/02-WDA*`, Text
`01-/03-/05-TXT*` (MTEXT), Türen `TÜR-80_*` (INSERT auf `05-SYM*`), Fluchtweg `09-WEG*`.
Baufeld E2 = Meter + andere Taxonomie (110/120/130-Blöcke) → deferred.

**Nächster Schritt:** S1 `dxf_load.py` — ezdxf öffnen, Modelspace/Wrapper-INSERT,
$INSUNITS→mm-Faktor, Layer-Prefix-Filter, `bounds_mm`. Test gegen `WHA_MOL_EG.dxf` (skipif).

**Naht-Warnung:** E2E NICHT auf echten Provider umstellen — 4OG-Golden (neg. Koords,
7 Symbole) matcht keinen echten DXF. Fake-Swap erst mit kuratierter neuer Golden + F1.
