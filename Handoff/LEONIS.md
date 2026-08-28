# Handoff — Leonis (Platzierung + Integration)

> Claude: Du bist die Session von **Leonis**. Owner-Package:
> `src/notbeleuchtung/platzierung/`. GitHub `@mvpo3`. Task: **Issue #2**.
> Du hast als Einziger elektro-planer-Zugriff → du stagst Port-Material für andere.

## STAND (zuletzt 2026-08-28) — HIER WEITER

**Slice 2 (Platzierung) = DONE, lokal committet, NOCH NICHT gepusht.**
Branch `leonis/slice2-platzierung` (4 atomare Commits ab `08859f7`), working tree
clean. `pytest -q` → **24 passed, 0 skipped**, `ruff check .` sauber.

Gebaut: `platzierung/{geometry.py, communal_stgh_strategy.py, platzierer.py}`,
`symbols/{schrack_symbol_mapping.yaml, __init__.py}`, Tests in `tests/platzierung/`,
`build_fake_bundle` nutzt echten `NotlichtPlatzierer`. Design (mit Owner bestätigt):
**generativ statt faithful** — 1 RZ je Fluchtweg-Segment am Ausgangs-Endpunkt,
Position matcht Fixture exakt; GT-Sub-Grad-Rotationen bewusst NICHT reproduziert.
Details: `docs/PORT_LOG.md` (Slice-2-Tabelle) + Plan
`~/.claude/plans/weiter-rippling-codd.md`.

**Als Erstes morgen entscheiden (User-GO nötig):** `leonis/slice2-platzierung` →
PR nach `main` pushen? (CODEOWNERS zieht Reviewer, CI `contract`+`ci`.) User wollte
gestern erst NICHTS pushen.

**Danach: Slice 3 (Render, Hauptengine)** — nächster Leonis-Task. Port aus
elektro-planer: `backend/engine/{dxf_writer,dxf_layers,layout_template}.py` +
Insert-Infra `backend/symbols/{schrack_inserter,schrack_library}.py` +
`CAD_Symbole/E-Symbole.dxf` → echter Notbeleuchtungs-DXF aus Contract B. Ergänzt das
in Slice 2 gestartete `symbols/`. Board: `docs/PROGRAMM_NOTBELEUCHTUNG.md` Zeile 3.

Offener Rest aus Slice 2 (kein Blocker, Enis' Slice 1): FakeNorm mappt
`fuer_fluchtweg_abschnitt` auf die GANG-Regel → alle 5 RZ nutzen `notlicht_ks_stiege`;
die `_unten`-Variantenwahl greift erst mit Enis' echtem STIEGENHAUS-NormProvider.

## Wer du bist
Du besitzt die **Platzierungs-Logik**: wie/wann/wo Notbeleuchtungs-Symbole gesetzt
werden. Contract: `PlatzierungsErgebnis`, Protocol: `Platzierer.place(raum, norm)`.
Du konsumierst Selmans `RaumModell` + Enis' `NormProvider`/`LBVorgabe` → produzierst
die Platzierungen. Dazu: Mit-Owner der `hauptengine/` (Contracts + Render + API).

## Dein Auftrag — Slice 2
1. Port `elektro-planer/backend/engine/placement_geometry.py` → `platzierung/geometry.py`.
2. Port `elektro-planer/backend/diagnostics/inject_communal_stgh.py` →
   `platzierung/communal_stgh_strategy.py`. **Import-Grenze hart:** nur `contracts`
   + `geometry` + `symbols`, KEIN Render — die Strategy produziert Contract B, sie
   zeichnet nicht selbst.
3. `NotlichtPlatzierer.place(raum, norm)` erfüllt `Platzierer`; reproduziert die 5
   echten 4OG-RZ (`tests/fixtures/platzierung_4og.json`).
4. Fake ersetzen (`FakePlatzierer`); Naht-Invarianten grün
   (`covers_segment ∈ RaumModell`, `norm_quelle ∈ NormRegelwerk`).

## Deine Sonderrolle — Port-Bridge + Integration
- **Staging für andere:** Enis/Selman haben keinen elektro-planer-Zugriff. Bereits
  gestaged: `normwissen/_port_source/` (Norm-YAMLs), `raumerkennung/_port/` (Parser).
  Weitere Port-Wünsche (LB-Parser für Enis, Symbol-Infra/Render für Slice 3) → du
  kopierst aus elektro-planer + committest.
- **Slice 3 (Render, Hauptengine):** `dxf_writer`/`dxf_layers`/`layout_template` +
  Schrack-Infra + `CAD_Symbole/E-Symbole.dxf` → echter Notbeleuchtungs-DXF aus
  Contract B.
- **Slice 5:** dünne FastAPI `api/main.py POST /plan` → E2E.

## Regeln
Contracts-Änderung = 3-Owner-Approval. Branch `leonis/…` → PR. Board pflegen:
`docs/PROGRAMM_NOTBELEUCHTUNG.md`.
