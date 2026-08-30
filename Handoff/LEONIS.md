# Handoff — Leonis (Platzierung + Integration)

> Claude: Du bist die Session von **Leonis**. Owner-Package:
> `src/notbeleuchtung/platzierung/`. GitHub `@mvpo3`. Task: **Issue #2**.
> Du hast als Einziger elektro-planer-Zugriff → du stagst Port-Material für andere.

## STAND (2026-08-30 Session-Ende) — HIER WEITER

**Der Nordstern läuft end-to-end auf echten Daten.** Alles unten ist auf `main`
(313 Tests grün, ruff clean, Drift in sync). Beide Fenster (F1+F2) haben heute massiv
geliefert.

**Voll-Real-E2E bewiesen:** echter Mollgasse-EG-Grundriss (`Projekte/Mollgasse/
Erdgeschoß.dxf`, 192 Räume) **+ reale LB-PDF** (`Leistungsbeschreibungen BSP/mo-…Elektro…pdf`)
durch `build_default_bundle()` → **12 RZ + 21 SL**, LB geparst+angewendet, gerendert als
PDF mit Anlagenlegende + Stückliste + Plankopf + Prüfbericht. Reproduzieren:
`run(build_default_bundle(), "Projekte/Mollgasse/Erdgeschoß.dxf", "EG", out_path=…, lb_path=<LB.pdf>)`
→ `render.dxf_zu_pdf(...)`.

**Heute nach main gemergt (F1/Leonis):**
- PDF-Export + `POST /plan?format=pdf` + Legende-Font-Fix (#30)
- Prüfbericht/Validierung (`hauptengine/validierung.py`) — 7 EN-1838-Regeln, sichtbar als
  Plan-Legende (#35/#37/#36)
- Plankopf/Schriftfeld + Stückliste + LB-Anlagenlegende im Render, Metadaten via API (#36)
- **Photometrie-Naht** (#38): `NotlichtPlatzierer(i_cd_fn=…)` + `registry.photometrie_i_cd_fn(ldt)`
  — F2s LDT/Photometrie fließt in die Lux-Deckung (Konstruktor-Injektion, keine Port-Änderung)
- **Multi-Geschoss** (#41): `hauptengine/projekt.py` `run_projekt` + `POST /projekt` →
  Sammel-PDF (ein Blatt je Geschoss)
- **SL-Dichte-Fix** (#42): `mittellinie.leuchten_auf_linie` dünnt gegen ALLE Punkte aus
  (nicht nur den letzten) + `deckung`-Mindestabstand 4 m → Mollgasse 268 → 19 SL

**F2 (anderes Fenster) hat heute auf main gebracht:** B3 Raumtyp-Geometrie
(`raumerkennung/raumtyp` greift jetzt → STIEGENHAUS/GANG typisiert), LB-Parser
(`normwissen/lb/parser.py` → `LbTextProvider`, in `build_default_bundle` verdrahtet),
OIB-Resolver (`normwissen/oib/`), IES-Import (`photometrie/ies.py`).

**Contracts-Stand:** `PlatzierungsErgebnis` 1.1.0 (+`lb_quelle`); neu ProjektKontext/
OibBefund/LBVorgabe (alle 1.0.0, gemergt). Alle auf main.

**Offene Feinschliff-Punkte (kein Blocker):**
1. **LB-Parser Betriebsdauer** — F2s `parser.py` liest „8 Std" nicht (Legende zeigt „0 h").
   F2-Ticket.
2. **Raumtyp-Abdeckung** — nur 5 GANG + 2 STIEGENHAUS von 192 Mollgasse-Räumen getypt;
   185 bleiben untypisiert (Coverage-Audit warnt). Mehr Abdeckung = F2 (raumerkennung).
3. `sonder_lux` (Feuerlöscher ≥5 lx) — braucht Positionen aus F2s Raumerkennung.
4. Echte Schrack-LDT ins Repo → `catalog_key→LDT`-Mapping (F2) → dann greift #38 real.

**Nächste Leonis-Tasks (Vorschlag morgen):** (a) DoD-Sichtprüfung des Real-PDF gegen eine
GU-Referenz; (b) weitere Render-Politur (Höhenkoten, Wände); (c) auf F2-Feinschliff
reagieren. Chat-Interface existiert bereits separat (nicht bauen). Board:
`docs/COORDINATION.md` (2-Fenster) + `docs/PROGRAMM_NOTBELEUCHTUNG.md`. Demo-Skripte +
Real-PDFs liegen in `output/` (gitignored).

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
