# Notbeleuchtung

**Mission:** Eine Engine, die aus **zwei Inputs** — einem **leeren Architekturplan**
(DXF/DWG) **+ einer Leistungsbeschreibung (LB)** — einen fertigen, ÖNorm-konformen
**Notbeleuchtungsplan** generiert (Rettungszeichen + Sicherheitsleuchten +
Antipanik nach EN 1838, getrennter Sicherheitskreis) → DXF/PDF.

**Nordstern (Produkt):** Chat-Interface — Nutzer lädt Plan (+ LB) hoch → bekommt
den kompletten Notbeleuchtungsplan zurück. `pipeline.run(arch_dxf, lb) → Plan` IST
die Engine; das Chat-Interface ist eine dünne Hülle über der FastAPI (`api/main.py`,
`POST /plan`). Konzept-Kurzform — echte Signatur (`hauptengine/pipeline.py`) ist
bundle-first: `run(bundle, dxf_path, floor, out_path=None, lb_path=None, …) → Output`.

Ausgegliedert aus `elektro-planer` (dort für Notbeleuchtung **eingefroren**; die
Raumerkennung wird portiert, nicht neu gebaut). Voller Status:
[`docs/PROGRAMM_NOTBELEUCHTUNG.md`](docs/PROGRAMM_NOTBELEUCHTUNG.md).

## Owner-Session-Start (WICHTIG für Claude)

Schreibt ein Owner **„Handoff <Name>"** (z.B. „Handoff Enis", „Handoff Selman",
„Handoff Leonis") → **lies sofort `Handoff/<NAME>.md`** (GROSS, z.B.
`Handoff/ENIS.md`) und arbeite exakt danach: wer der Owner ist, sein Package, sein
Contract, sein Slice, das Port-Material im Repo, die Schritte + DoD. Index +
Gemeinsames: `Handoff/README.md`.

Schreibt ein Owner **„Sync"** (oder „GitHub wurde aktualisiert", „zieh den Stand
nach") → **lies sofort `Handoff/SYNC.md`** und arbeite exakt danach. Grundregel dort:
**erst die eigene unversionierte Arbeit sichern, dann holen.** Nie `git reset --hard`,
`git checkout -- .`, `git clean -fd` oder `git stash drop` ohne Ansage des Owners.

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
| **Enis** | `EnisAMG` | `src/notbeleuchtung/normwissen/` | Normwissen (EN 1838/ÖNorm): Lux, Erkennungsweite l=z×h, Höhe, RZ-vs-Antipanik (`data/*.yaml`) **+ LB-Parsing** (2. Input → Contract `LBVorgabe`, explizite Auftraggeber-Vorgaben). |
| **gemeinsam** | alle 3 | `src/notbeleuchtung/hauptengine/` | Integration: **besitzt die Contracts** + Pipeline + Render + API. |
| **gemeinsam** | alle 3 | `src/notbeleuchtung/symbols/` · `wissen/` | Render-seitig geteilt: `symbols/` = Schrack-Library/Orientierung/Photometrie-Katalog (siehe Architektur-Landkarte), `wissen/` = statische YAML-Wissensdaten. |

**LB-Parsing (2. Input) = Enis.** Enis besitzt beide Wissens-Inputs für Leonis: das
statische `NormRegelwerk` (EN 1838/ÖNorm) und die projektspezifische `LBVorgabe`
(aus der LB geparste explizite Vorgaben, die Norm-Defaults übersteuern). Beide über
`normwissen/` (z.B. `normwissen/lb/` für den LB-Parser). Neuer Contract `LBVorgabe`
kommt im Slice „LB-Input".

## Architektur-Regel — Plugin-Modell (BINDEND)

Dependency-Inversion / Ports & Adapters. Die **Hauptengine besitzt die Contracts**
(`hauptengine/contracts/`), die Owner-Packages implementieren die Protocols
(alle definiert in `hauptengine/contracts/ports.py`: `RaumProvider`, `NormProvider`,
`LBProvider`, `Platzierer`, `OibProvider`, `ProviderBundle`). **Kein Owner-Package
importiert ein anderes** — Kommunikation läuft
ausschließlich über die Contract-Objekte, die durch `pipeline.run()` fließen:

```
                 Architekturplan (DXF)        LB (Spec)
                        │                         │
Selman: RaumProvider ─► RaumModell ─┐     ┌─ Enis: LBVorgabe
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
- Ein Approval gilt **nur für den Stand, auf dem es erteilt wurde**. Jeder
  nachgeschobene Commit entwertet es → neu reviewen. Das Gate
  (`.github/workflows/contract-freeze.yml`, Check `contract-freeze`) prüft das
  bei jedem Push.
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
  `CAD_Symbole/Notbeleuchtungssymbole.dxf` (im Repo, `.gitattributes` = binary).
- Board: `docs/PROGRAMM_NOTBELEUCHTUNG.md` · Port-Herkunft: `docs/PORT_LOG.md`.
- Atomare Slices, ein Concern pro Commit, em-dash in der Message.
- Irreversibel (Merge/Push/GitHub-Repo) = explizites User-GO.

## Architektur-Landkarte

- **Provider-Verdrahtung:** `hauptengine/registry.py` = der EINE Ort, wo echte
  Provider an die Ports binden (Lazy-Import → API antwortet 503 statt
  ImportError, solange ein Provider fehlt). Tests nutzen `tests/fakes.py`
  (Fake-Bundle) — grüner E2E heißt nicht „echt verdrahtet".
- **Validierung = QA-Layer:** `hauptengine/validierung.py` fährt die
  Norm-Regel-Suite (Status ok/warnung/fehler, „ungeprüft ≠ erfüllt"); Ergebnis
  fließt in den Prüfbericht. Grüner E2E-Test ≠ valider Plan.
- **symbols/-Ökosystem:** `library.py` (Schrack-DXF-Import: Layer-Rename →
  `din_SIBEL_10_emergency_lighting`, explizite Farben → BYLAYER) ·
  `orientation.py` (DER einzige Rotationsrahmen für Pfeile — gemessene
  Basis-Orientierungen, keine eigenen Konstanten) · `photometrie_katalog.py`
  (`catalog_key` → LDT).
- **Photometrie-Falle:** `c0_azimut_grad` (optische Achse) ≠ `rotation_deg`
  (Symbol-Rotation) — Verwechslung ergab historisch Faktor-7,7-Fehler.
- **Port-Material:** `raumerkennung/_port/` + `normwissen/_port_source/` =
  gestagtes elektro-planer-Material (Referenz zum Adaptieren, kein Scaffold,
  von ruff/setuptools ausgenommen).

## Setup / Tests

```
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e ".[dev,api]"
.venv/Scripts/python.exe -m pytest -q          # Contract + E2E
.venv/Scripts/python.exe -m pytest tests/platzierung/test_x.py -k name  # Einzeltest
.venv/Scripts/python.exe -m pytest -m visual   # Sicht-/Golden-Tests (default DESELEKTIERT via addopts!)
.venv/Scripts/python.exe scripts/gen_schema.py # Schemas regenerieren
ruff check .
.venv/Scripts/python.exe -m uvicorn notbeleuchtung.api.main:app --reload  # API lokal
```

- **Pipeline-Einstieg:** `hauptengine/pipeline.py` (`pipeline.run`) — ruft den
  Lux-Nachweis-Bericht automatisch; wer `place()`+`render_dxf` direkt nutzt, muss
  `render/lux_nachweis_bericht.schreibe_bericht` selbst aufrufen.
- **Skripte:** `scripts/plan_pruefen.py` (Ausgabe-Check), `scripts/dxf_healthcheck.py`
  (Eingabe-DXF: Extents/Versatz), `scripts/projekt_batch_worker.py` (Batch über
  `Projekte/`), `scripts/wissen_index.py` (regeneriert `knowledge/INDEX.md`).
- **Ausgabe-Regel (Owner):** Pläne IMMER als PDF (A0, 1:50) liefern, nie PNG.
- **Test-Struktur:** `tests/contract/` = schnelles Naht-Gate (Pydantic +
  Schema-Drift + Invarianten) · `tests/naht/` = Regressions-E2E gegen echte
  Pläne (Barawitzka/Mollgasse/…).
- **CI:** `contract.yml` (`gen_schema.py --check` + `pytest tests/contract`) ·
  `ci.yml` (ruff + volle Suite + Visual-Smoke `NOTBEL_UPDATE_GOLDEN=1 pytest -m
  visual` — Golden-PNGs sind maschinenspezifisch, nur LOKALES
  Regressionswerkzeug, kein Cross-Plattform-Vergleich).

## Don't

- ❌ Owner-Package importiert anderes Owner-Package (nur `hauptengine.contracts`).
- ❌ Contract ändern ohne Version-Bump + Schema-Regen (Drift-Gate bricht).
- ❌ Leonis parst YAML — er fragt `NormProvider`. Enis pflegt nur `normwissen/data/`.
- ❌ Hardcoden, was in der LB stehen könnte (LB-explizit übersteuert immer).
- ❌ Norm-Werte zurück nach elektro-planer syncen (Freeze ist Feature).
