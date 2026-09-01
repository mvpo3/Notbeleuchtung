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
| **NormRegelwerk** | Enis | Leonis | 1.1.0 | `contracts/schema/norm_regelwerk.schema.json` | 2026-09-01 (+Track-B-Felder, PR-prep) |
| **PlatzierungsErgebnis** | Leonis | Render | 1.1.0 | `contracts/schema/platzierung_ergebnis.schema.json` | 2026-08-30 (+lb_quelle) |
| **ProjektKontext** | Enis (Input) | OibProvider | 1.0.0 | `contracts/schema/projekt_kontext.schema.json` | 2026-08-30 (OIB-Grundlage) |
| **OibBefund** | OibProvider | Hauptengine | 1.0.0 | `contracts/schema/oib_ergebnis.schema.json` | 2026-08-30 (OIB-Grundlage) |
| **LBVorgabe** (2. Input) | Enis (Parser) | Leonis | 1.0.0 | `contracts/schema/lb_vorgabe.schema.json` | 2026-08-30 (LB-Input-Grundlage) |

Contract-Änderung → `contract_version` bumpen, `python scripts/gen_schema.py`,
committen, Zeile hier updaten, 3-Owner-Approval (CODEOWNERS auf `contracts/**`).

## Status-Matrix

| Item | Slice | Owner | Status | Stand |
|------|-------|-------|--------|-------|
| Repo-Skelett + 3 Contracts + Fake-Durchstich | 0 | Leonis | **DONE** (13✓/1s) | 2026-08-27 |
| Enis echt: Norm-YAMLs portieren + `En1838NormProvider` | 1 | Enis | **MERGED** (PR #6 → `4c40050`) | 2026-08-30 |
| Leonis echt: `communal_stgh_strategy` + `geometry` + `NotlichtPlatzierer` (Fake-Raum, echte Norm ab PR #6) | 2 | Leonis | **MERGED** (PR #4, 24✓) | 2026-08-28 |
| Render echt: `dxf_renderer` + Schrack-Infra (`symbols/{library,inserter}.py`) + `CAD_Symbole/E-Symbole.dxf` | 3 | Leonis/Render | **MERGED** (PR #5, 40✓; GU-PDF-Sichtprüfung offen) | 2026-08-28 |
| Selman echt: Parser-Port → `raumerkennung/_port/` + `ArchitekturRaumProvider` | 4 | Selman | TODO | — |
| Grüner E2E (echte 4OG-DXF) + dünne FastAPI `POST /plan` | 5 | alle | TODO | — |
| **Chat-Interface** (Plan-Upload → Notbeleuchtungsplan zurück) — Nordstern | 6 | Frontend-Owner offen | TODO | — |
| Enis: OIB-Resolver — `data/oib_rl2_tabelle6.yaml` + `normwissen/oib/` erfüllt `OibProvider` | — | **Enis** | **MERGED** (PR #32 → `564b7e9`). Offen: `ProviderBundle.oib` ist noch nicht verdrahtet (Hauptengine) | 2026-08-30 |
| Enis: LB-Parser — `normwissen/lb/` erfüllt `LBProvider.parse_lb` | — | **Enis** | **MERGED** (PR #60 → `758b9f9`) — fail closed, API-Naht `LbTextProvider`/`parse_lb`, Raumtyp-Vokabular synchronisiert, an 4 realen LB-PDFs gegengeprüft. Follow-up `lb_review` an der API-Grenze: **MERGED** (PR #67) | 2026-08-31 |

| Enis: Placement-Decision-Matrix — `data/platzierung_regeln.yaml` + `PlatzierungsRegelwerk` | — | **Enis** | **DONE** — 25 Regeln + 4 Hard Stops, 27 Domain-Tests, 7 Ground-Truth-Fälle. Track-A-Vorrat + Contract-Vorschlag in `docs/PLACEMENT_DECISION_MATRIX.md` | 2026-08-31 |

| Enis: Sonderstellen-Contract — Spec + Katalog + Tests | — | **Enis** (Entscheidung: 3 Owner) | **BLOCKED** — Vorschlag fertig (`docs/SPEC_SONDERSTELLEN_CONTRACT.md`), wartet auf 3-Owner-GO; schaltet 8 Placement-Regeln frei | 2026-08-31 |

**Legende:** TODO · WIP · BLOCKED · DONE.

**Zuständigkeit `OibProvider` (2026-08-30 festgelegt):** Enis. Die
Tabelle-6-Schwellenwerte sind Normwissen und gehören nach `normwissen/data/` —
gleiche Begründung wie bei `NormProvider`. Der `ProjektKontext` ist dagegen
**Projektinput** (Hauptengine/LB), nicht Normwissen: „Projektinput sagt, was
gebaut wird; Normwissen sagt, was das bedeutet."

## Offene Cross-Naht-Fragen

- (Enis) 4 Norm-Werte für Wohnungs-Fluchtweg ratifizieren: Fluchtweg-Definition
  Wohnung · F13-Wohnungs-Allokation · Erkennungsweite `l=z×h` (welche Höhe h) ·
  Antipanik 0,5 lx vs Rettungsweg 1 lx. (Übernommen aus elektro-planer H-20.)

- (Enis→Leonis) ~~**ProjektKontext-Contract fehlt**~~ — **erledigt durch PR #14**
  (`ProjektKontext`/`Gebaeudeteil`/`RaumReferenz`/`OibErgebnis`/`OibBefund` +
  `OibProvider`). Abweichungen gegenüber der Spec und die verbleibenden offenen
  Punkte stehen in `docs/SPEC_PROJEKTKONTEXT_OIB.md` Abschnitt 0. Fachliche
  Grundlage `docs/OIB_RL2_TABELLE6.md`, Quellenstatus `docs/NORMQUELLEN_AT.md`
  (Quell-PDFs liegen seit 2026-08-30 unter `knowledge/OIB-Richtlinien/` im Repo).

- (Leonis→alle) **`LBVorgabe` und `OibBefund` haben keinen Abnehmer:**
  `pipeline.run()` nimmt weder LB noch `ProjektKontext`, `ProviderBundle` hat
  weder `lb`- noch `oib`-Feld. Selbst fertige Provider aus `normwissen/` könnten
  heute nicht wirken. PR #23 verdrahtet die LB-Hälfte (`ports.py` + `pipeline.py`)
  ⇒ 3-Owner-Approval; die OIB-Hälfte ist danach noch offen.

- (Enis→Leonis) **LB-Vokabular:** `BereichsRegel.raum_typ` muss exakt auf Selmans
  `RaumModell.raum_typ` mappen (`STIEGENHAUS`/`GANG`/`GARAGE`), sonst greift die
  Exklusion im Platzierer nie. Vor dem LB-Parser-Slice festzurren.

- (Enis) **Norm-Ausgabe-Drift:** `normwissen/data/en1838_grundwerte.yaml` zitiert
  ÖNORM EN 1838:2013; im Repo liegt die Ausgabe **2019-11-15** (IDT EN 1838:2013-07).
  Inhaltlich deckungsgleich, Bezeichnung offen. **Entschieden 2026-08-30:** vorerst
  nur im YAML als Beleg-Status gekennzeichnet, nicht umgestellt — der String ist
  Naht-Invariante und hängt an `tests/fixtures/*` (3-Owner), `tests/fakes.py`, einer
  Leonis-Assertion und dem Contract-Default in `norm_regelwerk.py`
  (Blast-Radius: `docs/NORMQUELLEN_AT.md` Abschnitt 2a) ⇒ eigener koordinierter
  Slice. EN 1838:2025-03 und EN 50172:2024-11 fehlen weiterhin (kostenpflichtig).

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
