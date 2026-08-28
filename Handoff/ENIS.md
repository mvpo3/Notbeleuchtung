# Handoff — Enis (Normwissen + LB)

> Claude: Du bist die Session von **Enis**. Owner-Package:
> `src/notbeleuchtung/normwissen/`. GitHub `@EnisAMG`. Task: **Issue #1**.
> Lies zuerst `CLAUDE.md`, `docs/CONTRACTS.md`, `docs/ONBOARDING.md` (Abschnitt Enis).

## Stand (zuletzt 2026-08-28, Abend)

**Slice 1 (NormRegelwerk) AUSGELIEFERT** — Branch `enis/slice-1-normprovider`
gepusht, **PR #6 offen** (https://github.com/mvpo3/Notbeleuchtung/pull/6), CI
`ci` + `contract` grün, mergeable. Wartet nur noch auf Reviews: der PR fasst
`tests/fixtures/` an → CODEOWNERS verlangt **alle drei Owner** (@mvpo3,
@polatselman), nicht nur Enis.

Gebaut: `En1838NormProvider` (`normwissen/provider.py`) liest
`normwissen/data/en1838_grundwerte.yaml` + `raumtyp_regeln.yaml`, erfüllt das
Protocol `NormProvider`, hardcodet nichts. Snapshot-Fixture
`tests/fixtures/norm_regelwerk_snapshot.json` aus echtem Provider regeneriert
(`quellen` = {§4.2.1, §4.3.1}). `heights_fachpraxis`/`clearance_rules` bewusst
NICHT portiert (Steckdosen-Höhen bzw. Track-A Wand-Mechanik, kein NB-Normwissen).

**Main ist zwischenzeitlich weitergelaufen:** Leonis hat Slice 2 (PR #4,
`NotlichtPlatzierer`) und Slice 3 (PR #5, `dxf_renderer` + Schrack-Infra)
gemergt, dazu `knowledge/` (Norm-PDFs + Digests). Main wurde in den Branch
gemergt (`000b68e`), Konflikte aufgelöst:
`build_fake_bundle()` bindet jetzt **beide** echten Provider (Norm + Platzierer),
nur der Raum bleibt Fake bis Slice 4. `FakeNormProvider` bleibt als Nachbar-Double
für `tests/platzierung/` stehen. Tests nach Merge: **40 passed**, ruff sauber,
Schema in sync.

**Nächste Session:** PR #6 Reviews einsammeln + mergen, dann Slice „LB-Input"
(siehe unten). Der LB-Parser braucht eine **echte Leistungsbeschreibung** — Enis
legt sie ab (Vorschlag `Projekte/<Projekt>/LB/`); ohne echtes Dokument wird kein
Format erfunden. Nützlich für den Slice: `knowledge/` (Norm-Digests aus Leonis'
PR #5) — dort steht Referenz-Praxis-Material, das der LB-Hierarchie-Ebene
„Referenz-Praxis" entspricht.

**⚠ Setup-Falle (Mac):** Projekt braucht **Python ≥ 3.11** (System hatte nur
3.9.6 → editable install bricht). Fix war `brew install python@3.12`, dann venv
mit `/opt/homebrew/bin/python3.12 -m venv .venv`. Auf Mac: `.venv/bin/python`
(nicht `.venv\Scripts\python.exe` — das ist Windows).

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
Du besitzt **beide Wissens-Inputs** für Leonis' Platzierung:
1. **NormRegelwerk** — statisches EN-1838/ÖNorm-Wissen (Lux, Erkennungsweite l=z×h,
   Montagehöhe, RZ-vs-Antipanik, Dauer).
2. **LBVorgabe** — die Leistungsbeschreibung (2. Input) in explizite Vorgaben
   geparst, die Norm-Defaults übersteuern (Hierarchie: LB → Referenz → Norm → OVE).

Leonis **fragt** dich über die Query-API — er parst nie YAML.

## Dein Auftrag — Slice 1 (NormRegelwerk)
1. **Port-Material sichten:** `normwissen/_port_source/` (von Leonis gestaged, roh
   aus elektro-planer). Kern: `emergency_lighting_en1838.yaml` (l=z×h, z=200/100,
   Lux 1.0/0.5, Höhe ≥2000, Dauer 60), `rz_coverage_oenorm.yaml`,
   `heights_fachpraxis.yaml` (Notlicht-Höhen), `clearance_rules.yaml`.
2. **Kuratieren** → `normwissen/data/` (nur was Notbeleuchtung braucht, nicht 1:1).
3. **`En1838NormProvider`** (`normwissen/provider.py`) erfüllt das Protocol
   `NormProvider` (`hauptengine/contracts/ports.py`):
   `fuer_raum`, `fuer_fluchtweg_abschnitt`, `erkennungsweite_m`, `regelwerk_snapshot`.
   Liest die YAMLs, hardcodet nichts. Jede `NormAnforderung.quelle` = echte
   Norm-Fundstelle (Audit-Trail).
4. **Fake ersetzen:** `tests/fakes.py` `FakeNormProvider` → echt (oder registry
   verdrahten). `pytest -q` bleibt grün; `tests/contract/test_norm_regelwerk_contract.py`
   grün.

**DoD:** `NormProvider`-Konformität grün, Werte aus `data/`, E2E-Durchstich grün.

## Danach — Slice „LB-Input" (dein 2. Contract)
Neuer Contract `LBVorgabe` + LB-Parser (`normwissen/lb/`): LB (PDF/Text) → explizite
Vorgaben. Contract erst mit Leonis+Selman freezen (CODEOWNERS auf `contracts/**` =
alle drei). Referenz-LB-Parsing-Logik gibt es in elektro-planer — bei Bedarf
Leonis um Staging bitten (du hast dort keinen Zugriff).

## Regeln
Nur `normwissen/` + `hauptengine.contracts` importieren. Contract ändern =
`contract_version` bump + `python scripts/gen_schema.py` + 3-Owner-Approval.
Branch `enis/…` → PR.
