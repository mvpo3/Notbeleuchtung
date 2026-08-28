# Handoff — Leonis (Platzierung + Integration)

> Claude: Du bist die Session von **Leonis**. Owner-Package:
> `src/notbeleuchtung/platzierung/`. GitHub `@mvpo3`. Task: **Issue #2**.
> Du hast als Einziger elektro-planer-Zugriff → du stagst Port-Material für andere.

## STAND (zuletzt 2026-08-28 abends) — HIER WEITER

**Slice 2 = gepusht, PR #4 offen** (github.com/mvpo3/Notbeleuchtung/pull/4,
CODEOWNERS-Review + CI abwarten). **knowledge/ (14 Norm-PDFs) liegt auf main**
(gitignore-Ausnahme `!knowledge/**`; Repo ist PRIVATE — wegen der lizenzpflichtigen
Norm-PDFs NICHT public stellen).

**Slice 3 (Render) = DONE (Code), lokal auf `leonis/slice3-render`** (5 atomare
Commits ab `5a86d8b`, zweigt vom Slice-2-Branch ab). `pytest -q` → **40 passed,
0 skipped**, `ruff check .` sauber, E2E asserted `rendered: True`.

Gebaut: `symbols/{library.py, inserter.py}` (Port schrack_library/schrack_inserter,
generativ verschlankt), `hauptengine/render/dxf_renderer.py` (Contract B +
RaumModell → DXF: 5 RZ auf `E_Sicherheitsbeleuchtung`, F13-Stromkreis-Labels mit
Anti-Kollision, Raum-Konturen, Fluchtweg-Segmente, VPORT), `pipeline.run(...,
out_path=)` (ohne out_path weiter `rendered: False` — kompatibel), Tests
`tests/render/` (15 Stück). KEIN Contract angefasst. Design-Entscheide +
Herkunfts-Commits: `docs/PORT_LOG.md` Slice-3-Tabelle; Plan
`~/.claude/plans/handoff-agile-summit.md`.

**Offen für Slice-3-Abschluss:** (1) DoD-Sichtprüfung: generierten DXF gegen
4OG-GU-PDF prüfen (Datei wurde dem User geschickt), (2) User-GO: Branch pushen +
PR (nach/auf PR #4 gestackt). **Danach: Slice 5-Anteil** (dünne FastAPI
`api/main.py POST /plan`) oder Port-Staging für Enis/Selman auf Zuruf.
`layout_template` (Titelblock/PDF) bewusst deferred → PORT_LOG „Geplante Ports".

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
