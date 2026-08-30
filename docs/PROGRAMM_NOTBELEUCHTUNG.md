# Programm-Board „Notbeleuchtung" — lebender Status (Single Source of Truth)

**Start:** 2026-08-27 · Board gewinnt bei Drift gegen GitHub-Projects. Jeder Owner
pflegt seine Zeilen + committet.

## Nordstern (Produkt-Ziel — alles läuft hierauf zu)

**Chat-Interface: Nutzer lädt seinen Plan hoch → bekommt einen kompletten
Notbeleuchtungsplan zurück.** Ende-zu-Ende, idiotensicher.

```
Chat-UI (Plan-Upload) ──HTTP──► FastAPI POST /plan ──► hauptengine.pipeline.run() ──► Notbeleuchtungsplan (DXF/PDF) zurück
```

`pipeline.run(dxf) → Plan` IST die ganze Engine (Selman→Leonis→Enis→Render). Das
Chat-Interface ist eine dünne Hülle über der API — die API (`api/main.py`) ist die
Auslieferungs-Naht. Reihenfolge: erst Engine E2E grün (Slice 0–5), dann die
Chat-Hülle (Slice 6). **Offen:** Frontend-Owner — die 3 aktuellen Owner sind alle
Backend (Raumerkennung/Platzierung/Normwissen). Entscheiden, wenn Engine steht.

## Contract-Version-Tabelle (die wichtigste Sync-Info)

| Contract | Owner-Produzent | Konsumenten | Version | Schema | Eingefroren |
|----------|-----------------|-------------|---------|--------|-------------|
| **RaumModell** | Selman | Leonis, Render | 1.0.0 | `contracts/schema/raum_modell.schema.json` | 2026-08-27 (Slice 0) |
| **NormRegelwerk** | Enis | Leonis | 1.0.0 | `contracts/schema/norm_regelwerk.schema.json` | 2026-08-27 (Slice 0) |
| **PlatzierungsErgebnis** | Leonis | Render | 1.0.0 | `contracts/schema/platzierung_ergebnis.schema.json` | 2026-08-27 (Slice 0) |
| **ProjektKontext** | Enis (Input) | OibProvider | 1.0.0 | `contracts/schema/projekt_kontext.schema.json` | 2026-08-30 (OIB-Grundlage) |
| **OibBefund** | OibProvider | Hauptengine | 1.0.0 | `contracts/schema/oib_ergebnis.schema.json` | 2026-08-30 (OIB-Grundlage) |

Contract-Änderung → `contract_version` bumpen, `python scripts/gen_schema.py`,
committen, Zeile hier updaten, 3-Owner-Approval (CODEOWNERS auf `contracts/**`).

## Status-Matrix

| Item | Slice | Owner | Status | Stand |
|------|-------|-------|--------|-------|
| Repo-Skelett + 3 Contracts + Fake-Durchstich | 0 | Leonis | **DONE** (13✓/1s) | 2026-08-27 |
| Enis echt: Norm-YAMLs portieren + `En1838NormProvider` | 1 | Enis | **DONE** (PR #6 offen, auf main nachgezogen, 55✓) | 2026-08-29 |
| Leonis echt: `communal_stgh_strategy` + `geometry` + `NotlichtPlatzierer` (Fake-Raum, echte Norm ab PR #6) | 2 | Leonis | **MERGED** (PR #4, 24✓) | 2026-08-28 |
| Render echt: `dxf_renderer` + Schrack-Infra (`symbols/{library,inserter}.py`) + `CAD_Symbole/E-Symbole.dxf` | 3 | Leonis/Render | **MERGED** (PR #5, 40✓; GU-PDF-Sichtprüfung offen) | 2026-08-28 |
| Selman echt: Parser-Port → `raumerkennung/_port/` + `ArchitekturRaumProvider` | 4 | Selman | TODO | — |
| Grüner E2E (echte 4OG-DXF) + dünne FastAPI `POST /plan` | 5 | alle | TODO | — |
| **Chat-Interface** (Plan-Upload → Notbeleuchtungsplan zurück) — Nordstern | 6 | Frontend-Owner offen | TODO | — |

**Legende:** TODO · WIP · BLOCKED · DONE.

## Offene Cross-Naht-Fragen

- (Enis) 4 Norm-Werte für Wohnungs-Fluchtweg ratifizieren: Fluchtweg-Definition
  Wohnung · F13-Wohnungs-Allokation · Erkennungsweite `l=z×h` (welche Höhe h) ·
  Antipanik 0,5 lx vs Rettungsweg 1 lx. (Übernommen aus elektro-planer H-20.)

- (Enis/Leonis) **Photometrie-Ausnahme (entschieden 2026-08-29):** Leonis baut
  `normwissen/photometrie/` (LDT/EULUMDAT → exakte Lux) im Enis-Package. Bewusste
  Ausnahme von der Owner-Grenze; rein additiv, kein Contract betroffen. Enis
  bleibt Owner von `normwissen/data/` + `provider.py`.

## Definition-of-Done je Slice
- **1 (Enis):** `NormProvider`-Konformitätstest grün, Werte aus `normwissen/data/`.
- **2 (Leonis):** `PlatzierungsErgebnis` schema-valide, Naht-Invarianten grün,
  reproduziert die 5 4OG-Referenz-RZ (Typ+Richtung+Grobposition).
- **3 (Render):** sichtbarer Notbeleuchtungs-DXF, Layer `E_Sicherheitsbeleuchtung`,
  F13-Kreis, gegen 4OG-GU-PDF geprüft.
- **4 (Selman):** echtes RaumModell aus 4OG-DXF, schema-identisch zur Fixture.
- **5:** `tests/e2e` echte DXF → DXF; API `POST /plan`.
