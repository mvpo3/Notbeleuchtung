# Handoff — Enis (Normwissen + LB)

> Claude: Du bist die Session von **Enis**. Owner-Package:
> `src/notbeleuchtung/normwissen/`. GitHub `@EnisAMG`. Task: **Issue #1**.
> Lies zuerst `CLAUDE.md`, `docs/CONTRACTS.md`, `docs/ONBOARDING.md` (Abschnitt Enis).

## Stand (zuletzt 2026-08-29)

**Slice 1 (NormRegelwerk) fertig, PR #6 auf aktuellem main** — Branch
`enis/slice-1-normprovider`, PR https://github.com/mvpo3/Notbeleuchtung/pull/6.
Wartet auf Reviews: der PR fasst `tests/fixtures/` an → CODEOWNERS verlangt
**alle drei Owner** (@mvpo3, @polatselman). Merge erst nach Owner-GO.

Gebaut: `En1838NormProvider` (`normwissen/provider.py`) liest
`normwissen/data/en1838_grundwerte.yaml` + `raumtyp_regeln.yaml`, erfüllt das
Protocol `NormProvider`, hardcodet nichts. `heights_fachpraxis`/`clearance_rules`
bewusst NICHT portiert (Steckdosen-Höhen bzw. Track-A Wand-Mechanik, kein
NB-Normwissen).

**Nachzug auf main (PR #7–#10, Leonis):** main hatte den Symbol-Katalog umgebaut
und dabei Enis' Fixture `norm_regelwerk_snapshot.json` fake-first vorweggenommen.
Am 29.08. nachgezogen (Commits `d3cd9b7` + `b343fef`), damit der ECHTE Provider
liefert, was Platzierer + Renderer heute erwarten:
- **STIEGENHAUS-Raum → `sicherheitsleuchte`** (Aufheller, EN 1838 §4.1), nicht
  mehr `rz`. Rettungszeichen hängen an den Fluchtweg-**Segmenten**
  (`fuer_fluchtweg_abschnitt` → GANG-Regel) — der Raum selbst braucht die
  Betonungs-Leuchte. Neue Audit-Quelle `§4.1` in `quellen`.
- **GANG + `default`** bieten alle vier Pfeil-Keys an (`notlicht_ks_stiege`,
  `_unten`, `_links`, `_rechts`); die Laufrichtung wählt Leonis
  (`communal_stgh_strategy::_select_key`), die Norm gibt nur die Menge vor.
- **Antipanik** auf den echten Katalog-Key `antipanik_leuchte`; **SAAL
  `mindest_anzahl: 4`** = Raster-Stützstellen für die Flächen-Anforderung
  §4.3.1 (`flaechen_strategy` verteilt sie über `grid_points`).
- Snapshot-Fixture aus dem echten Provider neu generiert (nie handschreiben:
  `En1838NormProvider().regelwerk_snapshot().model_dump()` → JSON, indent 2).

Tests nach Merge: **55 passed**, ruff sauber, Schema in sync. E2E-Durchstich
liefert 7 Symbole (5 rz + 2 sicherheitsleuchte) — genau das, was main erwartet.
⚠ `pip install -e ".[dev,api]"` nach dem Merge nötig (main hat `networkx`
ergänzt), sonst bricht die Test-Collection.

**Owner-Grenze Photometrie (Owner-Entscheid 2026-08-29):** Leonis darf das
LDT/Photometrie-Modul unter `src/notbeleuchtung/normwissen/photometrie/` bauen
(Branch `leonis/ldt-photometrie`, siehe `docs/COORDINATION.md` in PR #11) —
bewusste Ausnahme von „ein Owner = ein Package". Enis bleibt Owner der
Norm-Regeln (`data/`, `provider.py`); das Photometrie-Modul ist rein additiv und
berührt keinen Contract.

**Nächster Slice — „LB-Input":** Material liegt jetzt vor in
`Leistungsbeschreibung BSP/` (4 echte PDFs, untracked):
`mo-leistungsbeschreibung_Elektro_240718.pdf` (Elektro-LV, der direkte
Kandidat), `250116_GU Leistungsbeschreibung.pdf`, `20241209_E LV Fischa 46.pdf`,
`mo-Bau-_und_Ausstattungsbeschreibung_…pdf`. Vorgehen: PDFs sichten → welche
Aussagen sind EXPLIZITE Vorgaben (Produkt, Stückzahl, Dauer, Sonderwunsch) →
daraus Contract `LBVorgabe` (3-Owner-Freeze + `gen_schema.py`) + Parser
`normwissen/lb/`. Format aus den echten Dokumenten ableiten, nichts erfinden.
Ergänzend: `knowledge/` (Norm-Digests + Referenz-Praxis-Analysen von Leonis).
Beim Start klären: LB-PDFs ins Repo committen oder `.gitignore`?

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
