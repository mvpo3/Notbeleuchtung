# Handoff — Leonis (Platzierung + Integration)

> Claude: Du bist die Session von **Leonis**. Owner-Package:
> `src/notbeleuchtung/platzierung/`. GitHub `@mvpo3`. Task: **Issue #2**.
> Du hast als Einziger elektro-planer-Zugriff → du stagst Port-Material für andere.

## STAND (2026-08-29 Session-Ende) — HIER WEITER

**Platzier-Regeln aus dem Wissen kodiert** (Commit `e87a745`, `anker_strategy.py`):
1. **RZ-Dichte = `l = z·h`** — `plan_rettungszeichen_sichtlinie` zieht `max_abstand_mm`
   aus `norm.erkennungsweite_m` (z=200 hinterleuchtet/100 beleuchtet, h=Pikto-Höhe)
   statt geratener 12-m-Konstante. Keine Überproduktion.
2. **`richtung_durch_tuer(tuer_xy, ziel_xy)`** — RZ an Tür/Öffnung entlang der Schwelle,
   Pfeil DURCH die Öffnung in Reiserichtung; überschreibt das Distanz-Gefälle
   (Owner-Korrektur L-Knick). Tests +2, Suite 95 grün. Kein Contract berührt.

⚠️ **Git-Tangle:** dieser Commit + die früheren Platzier-Module (graph/richtungsfeld/
sichtlinie/mittellinie/lux/deckung) liegen auf Branch **`selman/raumerkennung-dxf`**
(nicht `leonis/*`). Integration war als PR #12 geplant. PR #11 stale/superseded.
Vor Weiterarbeit: entwirren — Platzier-Code gehört auf einen `leonis/*`-Branch.

**Echter End-to-End-Durchstich auf Fischamender BT1 1.OG** (F2-Provider → F1-Engine →
DXF in den echten Grundriss). Ergebnis ehrlich geprüft (Determinismus + Sanity):
- ✅ Provider läuft: **59 Raum-Polygone** (39 getypt, 20 Fragmente), **102 Tür-INSERTs**.
- ✅ Engine platziert 10 SL; RZ-Regeln laufen auf echter Geometrie.
- ✅ **DXF-Overlay** (`output/Fischamender_BT1_1OG_MIT_Notbeleuchtung.dxf`, untracked):
  Symbole IN den Original-Grundriss gezeichnet, Original-Einheiten (Meter → Pos+scale
  ÷ factor=1000, scale 0,185), neuer Layer `E_Sicherheitsbeleuchtung`, Original
  unangetastet. Per ezdxf-Preview verifiziert.
- ❌ **2 F2-Bugs gefunden** (in `docs/COORDINATION.md` als Tickets dokumentiert):
  (B1) Tür-**Doppelzählung** — 102 roh → ~60 dedup (jede Tür als 2 ARC-Schwenkbögen);
  (B2) **A_Fluchtweg + Ausgänge werden für die Fischamender-Familie nicht gelesen**
  (`zirkulation_aus_dxf` sucht Mollgasse `09-WEG`, footprint nur Mollgasse-kalibriert)
  → 0 Ausgänge, 0 Zirkulation → RZ-Routing musste stiegenhaus-verankert improvisiert
  werden (Stiegenhaus aus `S-STRS`-Layer lokalisiert, ×factor).

**Erkenntnis:** Platzier-Regeln (l=z·h, Wasserscheide, Pfeil-durch-Tür) sind solide;
der Engpass für vollautomatisch = **F2s Provider auf fremden CAD-Familien** (nicht die
Platzierung). Placement kann erst voll geroutet werden, wenn F2 Fluchtweg/Ausgänge
für die Fischamender-Konvention liefert.

**Nächste Leonis-Tasks:** (1) Git entwirren (Platzier-Code auf `leonis/*`, PR #12/#11
klären). (2) GANG-Raum→Graph-**Fallback** in `platzierung/` erwägen (RZ auch ohne
F2-Fluchtweg-Layer, aus erkannten GANG-Räumen — macht Engine auf mehr Plänen sofort
nutzbar). (3) SL-Symbolgröße justierbar + lux-Verifikation je realem Plan.
Demo-Skripte in `scratchpad`/`output/` (nicht im Repo).

## STAND (2026-08-28 Session-Ende) — Historie

**Slice 2 (PR #4) + Slice 3 (PR #5) = GEMERGT nach `main`.** `pytest -q` auf main →
**40 passed, 0 skipped**, `ruff check .` sauber, E2E `rendered: True`.
Branches `leonis/slice2-platzierung` + `leonis/slice3-render` noch da (nicht gelöscht).

**Wissensbasis auf main** (`knowledge/`): 20 Norm-/Praxis-PDFs + `extracted/` (18
Digests, Regel-Tabellen), `extracted/bildlehren/` (visuelle Analyse), Synthese
`extracted/PLATZIERUNGS_KONZEPTE.md`, `extracted/aus_elektroplaner/` (5 gefilterte
elektro-planer-Digests inkl. Schrack-Katalog + OVE E 8101:2025-Deltas) + kompletter
Rohimport `_extracted_text/`. Repo ist PRIVATE — lizenzpflichtige Norm-PDFs, NICHT
public stellen.

Slice 3 gebaut: `symbols/{library.py, inserter.py}`, `hauptengine/render/dxf_renderer.py`
(Contract B + RaumModell → DXF: 5 RZ auf `E_Sicherheitsbeleuchtung`, F13-Labels,
Raum-Konturen, VPORT), `pipeline.run(..., out_path=)`. KEIN Contract angefasst.
PORT_LOG Slice-3-Tabelle.

**Projekte auf main:** neues Projekt **Baufeld E2** als `Projekte/Baufeld_E2.zip`
(56 MB, 8 DXF-Etagenpläne). Roh war 756 MB, 4 DXF > 100 MB GitHub-Limit → DXF
komprimiert auf ~6%, daher Zip. Rohordner `Projekte/Baufeld E2/` ist gitignored
(bleibt lokal). Enis/Selman: einmal entpacken. E8101-2025-PDF liegt auch auf main.

**Entscheidungen dieser Session (nicht neu aufrollen):**
- **Kein Git-LFS.** Geprüft: 923 MB Binär ≈ ganzes Free-LFS-Limit (1 GB Speicher +
  1 GB/Mon Bandbreite); Migration = Historie-Umschreiben + Force-Push (alle neu
  klonen). Aufwand/Kosten > Nutzen → bleibt bei normalem Git. Falls Repo später
  stört: `_extracted_text` (53 MB) ist lokal verzichtbar (Wert in Digests), Roh-CAD
  projektweise zippen wie Baufeld E2.
- **NetworkX = gratis** (BSD-3). Andock-Analyse gemacht: `zirkulation.{nodes,edges}`
  ist aktuell UNGENUTZT (Platzierer nutzt nur `segmente`), Fixture-Graph zu dünn
  (2 stair-nodes). NetworkX lohnt erst mit Selmans echtem Graph (Slice 4) + Leonis'
  Schicht 1 (Kreuzungs-Anker via `degree>=3`) / Schicht 5 (Deckung/Distanz via
  `single_source_dijkstra`). Dann: neues Modul `platzierung/graph.py` + Dep in
  pyproject. **Jetzt noch nicht einbauen.**

**Nächste Leonis-Tasks:** (1) DoD-Sichtprüfung generierter DXF vs. 4OG-GU-PDF (offen),
(2) **Slice 5-Anteil** dünne FastAPI `api/main.py POST /plan` → E2E, oder Port-Staging
für Enis/Selman auf Zuruf. `layout_template` (Titelblock/PDF) deferred → PORT_LOG.
Neue Erkenntnisse fürs Normwissen (Enis): OVE E 8101:2025 neues Verbot RCD/AFDD in
Sicherheitskreisen (Hard-Stop), Schrack-Erkennungsweiten je Leuchtenfamilie.
Platzierer-Ausbau-Fahrplan (Anker→Linie→Fläche→Deckung): `extracted/PLATZIERUNGS_KONZEPTE.md`.

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
