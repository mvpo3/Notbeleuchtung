# Handoff — Selman (Raumerkennung)

> Claude: Du bist die Session von **Selman**. Owner-Package:
> `src/notbeleuchtung/raumerkennung/`. GitHub `@polatselman`. Task: **Issue #3**.
> Lies zuerst `CLAUDE.md`, `docs/CONTRACTS.md`, `docs/ONBOARDING.md` (Abschnitt Selman).

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
