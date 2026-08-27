# Notbeleuchtung

**Mission:** Eine Engine, die aus **zwei Inputs** — einem **leeren Architekturplan**
(DXF/DWG) **+ einer Leistungsbeschreibung (LB)** — einen fertigen, ÖNorm-konformen
**Notbeleuchtungsplan** generiert (Rettungszeichen + Sicherheitsleuchten +
Antipanik nach EN 1838, getrennter Sicherheitskreis) → DXF/PDF.

**Nordstern (Produkt):** Chat-Interface — Nutzer lädt Plan (+ LB) hoch → bekommt
den kompletten Notbeleuchtungsplan zurück. `pipeline.run(arch_dxf, lb) → Plan` IST
die Engine; das Chat-Interface ist eine dünne Hülle über der FastAPI (`api/main.py`,
`POST /plan`).

Ausgegliedert aus `elektro-planer` (dort für Notbeleuchtung **eingefroren**; die
Raumerkennung wird portiert, nicht neu gebaut). Voller Status:
[`docs/PROGRAMM_NOTBELEUCHTUNG.md`](docs/PROGRAMM_NOTBELEUCHTUNG.md).

## Die zwei Inputs

1. **Leerer Architekturplan** (DXF/DWG) → Selman erkennt Räume/Türen/Ausgänge/
   Fluchtweg-Zirkulation (RaumModell).
2. **Leistungsbeschreibung (LB)** → projektspezifische, EXPLIZITE Vorgaben des
   Auftraggebers (welche Notbeleuchtung, Produkte, Stückzahlen, Sonderwünsche).
   Übersteuert Norm-Defaults (siehe Architektur-Regel).

## Architektur-Regel — Entscheidungs-Hierarchie (BINDEND)

```
LB-explizit  →  Referenz-Praxis  →  EN-1838/ÖNorm-Default  →  OVE-Verbote (Hard Stop)
```
LB-Werte übersteuern Norm-Defaults. Nichts hardcoden, was in der LB stehen könnte.
OVE/EN-Verbote sind Hard Stops. Jede Platzierung trägt ihre Entscheidungs-Quelle
(`norm_quelle` / künftig `lb_quelle`) als Audit-Trail.

## Team & Owner-Grenzen (Top-Level-Packages)

| Owner | GitHub | Package | Verantwortung |
|-------|--------|---------|---------------|
| **Selman** | `polatselman` | `src/notbeleuchtung/raumerkennung/` | Leerer Architekturplan (DXF) → RaumModell (Räume/Türen/Ausgänge/Zirkulation). Portierter Parser in `_port/`. |
| **Leonis** | `mvpo3` | `src/notbeleuchtung/platzierung/` | Platzierungs-Logik: wie/wann/wo Notbeleuchtungs-Symbole. Konsumiert Raum + Norm + LB → PlatzierungsErgebnis. |
| **Enis** | `EnisAMG` | `src/notbeleuchtung/normwissen/` | Normwissen (EN 1838/ÖNorm): Lux, Erkennungsweite l=z×h, Höhe, RZ-vs-Antipanik. Pflegt `normwissen/data/*.yaml`. |
| **gemeinsam** | alle 3 | `src/notbeleuchtung/hauptengine/` | Integration: **besitzt die Contracts** + Pipeline + Render + API. |

**LB-Parsing (2. Input) — Owner noch offen.** Neues Modul (Kandidat `src/
notbeleuchtung/lb/` mit Contract `LBVorgabe`), das die LB in explizite Vorgaben
parst, die Leonis' Platzierung übersteuern. Zuordnung entscheiden, bevor Slice
„LB-Input" startet (Kandidat: Enis, da fachnah — oder eigener Owner).

## Architektur-Regel — Plugin-Modell (BINDEND)

Dependency-Inversion / Ports & Adapters. Die **Hauptengine besitzt die Contracts**
(`hauptengine/contracts/`), die Owner-Packages implementieren die Protocols
(`ports.py`). **Kein Owner-Package importiert ein anderes** — Kommunikation läuft
ausschließlich über die Contract-Objekte, die durch `pipeline.run()` fließen:

```
                 Architekturplan (DXF)        LB (Spec)
                        │                         │
Selman: RaumProvider ─► RaumModell ─┐     ┌─ LBVorgabe (Owner offen)
                                     ├─────┤
Enis:   NormProvider ─► NormRegelwerk┘     └─► Leonis: Platzierer(Raum, Norm, LB)
                                                     │
                                                     ▼  PlatzierungsErgebnis
                                          Hauptengine: Render → Notbeleuchtungsplan (DXF/PDF)
                                                     │
                                          api POST /plan ──► Chat-Interface
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
- **CAD-Assets:** leere Architekturpläne in `Projekte/`, Schrack-Library in
  `CAD_Symbole/E-Symbole.dxf` (im Repo, `.gitattributes` = binary).
- Board: `docs/PROGRAMM_NOTBELEUCHTUNG.md` · Port-Herkunft: `docs/PORT_LOG.md`.
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
- ❌ Hardcoden, was in der LB stehen könnte (LB-explizit übersteuert immer).
- ❌ Norm-Werte zurück nach elektro-planer syncen (Freeze ist Feature).
