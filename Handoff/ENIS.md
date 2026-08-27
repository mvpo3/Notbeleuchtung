# Handoff — Enis (Normwissen + LB)

> Claude: Du bist die Session von **Enis**. Owner-Package:
> `src/notbeleuchtung/normwissen/`. GitHub `@EnisAMG`. Task: **Issue #1**.
> Lies zuerst `CLAUDE.md`, `docs/CONTRACTS.md`, `docs/ONBOARDING.md` (Abschnitt Enis).

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
