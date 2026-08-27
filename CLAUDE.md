# Notbeleuchtung

Dediziertes Backend: Architektplan (DXF) → ÖNorm-konforme **Notbeleuchtung**
(Rettungszeichen + Sicherheitsleuchten + Antipanik, EN 1838) → getrennter
Sicherheitskreis → DXF/PDF. Ausgegliedert aus `elektro-planer` (dort für
Notbeleuchtung **eingefroren**; die Raumerkennung wurde portiert, nicht neu gebaut).

## Team & Owner-Grenzen (Top-Level-Packages)

| Owner | GitHub | Package | Verantwortung |
|-------|--------|---------|---------------|
| **Selman** | `officialsmptrades-beep` | `src/notbeleuchtung/raumerkennung/` | Grundriss-DXF → RaumModell (Räume/Türen/Ausgänge/Zirkulation). Portierter Parser in `_port/`. |
| **Leonis** | `mvpo3` | `src/notbeleuchtung/platzierung/` | Platzierungs-Logik: wie/wann/wo Notbeleuchtungs-Symbole. Konsumiert Raum + Norm → PlatzierungsErgebnis. |
| **Enis** | `EnisAMG` | `src/notbeleuchtung/normwissen/` | Normwissen (EN 1838/ÖNorm): Lux, Erkennungsweite l=z×h, Höhe, RZ-vs-Antipanik. Pflegt `normwissen/data/*.yaml`. |
| **gemeinsam** | alle 3 | `src/notbeleuchtung/hauptengine/` | Integration: **besitzt die Contracts** + Pipeline + Render. |

## Architektur-Regel (BINDEND)

Dependency-Inversion / Ports & Adapters. Die **Hauptengine besitzt die 3 Contracts**
(`hauptengine/contracts/`), die Owner-Packages implementieren die Protocols
(`ports.py`). **Kein Owner-Package importiert ein anderes** — Kommunikation läuft
ausschließlich über die Contract-Objekte, die durch `pipeline.run()` fließen:

```
Selman: RaumProvider ─► RaumModell ─┐
                                     ├─► Leonis: Platzierer(Raum, Norm) ─► PlatzierungsErgebnis ─► Render → DXF
Enis:   NormProvider ─► NormRegelwerk┘
```

## Contract-Freeze-Regel (BINDEND)

- Contracts = **Pydantic** (`hauptengine/contracts/*.py`) = Single Source of Truth.
  JSON-Schema wird daraus generiert: `python scripts/gen_schema.py`.
- Contract-Änderung → `contract_version` bumpen + Schema regenerieren + committen.
  Das Drift-Gate (`tests/contract/test_schema_drift.py`) bricht sonst.
- `hauptengine/contracts/**` ändern = **Approval aller 3 Owner** (CODEOWNERS).
  Eigenes Package = eigenes Approval → schnelle Parallelarbeit, nur die Naht ist
  konsens-gebunden.
- Naht-Invarianten (CI, `tests/contract/`): `covers_segment ∈ RaumModell.segmente`
  (Leonis↔Selman) · `norm_quelle ∈ NormRegelwerk.quellen` (Leonis↔Enis) ·
  `catalog_key ∈ schrack_symbol_mapping.yaml`.

## Arbeitsweise

- **Fake-Provider-first:** der E2E-Durchstich (`tests/e2e/test_4og_durchstich.py`)
  ist ab Slice 0 grün (Fakes liefern die Golden-Fixtures). Pro Slice wird ein Fake
  gegen einen echten Provider getauscht — nie Big-Bang.
- Jeder Owner liefert seine „ich-produziere"-Fixture in `tests/fixtures/` und testet
  gegen die „ich-brauche"-Fixtures der Upstreams.
- Board: `docs/PROGRAMM_NOTBELEUCHTUNG.md` (Status je Owner + Contract-Version-Tabelle).
- Port-Herkunft: `docs/PORT_LOG.md` (welcher elektro-planer-Commit, welche Divergenz).
- Atomare Slices, ein Concern pro Commit, em-dash in der Message.
- Irreversibel (Merge/Push/GitHub-Repo) = explizites User-GO.

## Setup / Tests

```
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e ".[dev,api]"
.venv/Scripts/python.exe -m pytest -q          # Contract + E2E
.venv/Scripts/python.exe scripts/gen_schema.py # Schemas regenerieren
ruff check .
```

## Don't

- ❌ Owner-Package importiert anderes Owner-Package (nur `hauptengine.contracts`).
- ❌ Contract ändern ohne Version-Bump + Schema-Regen (Drift-Gate bricht).
- ❌ Leonis parst YAML — er fragt `NormProvider`. Enis pflegt nur `normwissen/data/`.
- ❌ Norm-Werte zurück nach elektro-planer syncen (Freeze ist Feature).
