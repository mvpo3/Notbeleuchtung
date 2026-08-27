# Onboarding — Start hier (Selman · Leonis · Enis)

Ihr arbeitet **alle drei gleichzeitig** in eurem eigenen Package. Dank
Fake-Provider-first blockiert keiner den anderen: jeder baut gegen den **Contract**
+ die **Fixtures** der Nachbarn, nie gegen deren halbfertigen Code.

## 0. Einmalig einrichten

```
git clone https://github.com/mvpo3/Notbeleuchtung.git
cd Notbeleuchtung
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e ".[dev,api]"   # Windows
# (macOS/Linux: .venv/bin/python -m pip install -e ".[dev,api]")
.venv/Scripts/python.exe -m pytest -q                     # muss grün sein: 13 passed, 1 skipped
```

Lies zuerst: `CLAUDE.md` (Regeln) · `docs/CONTRACTS.md` (die Naht) ·
`docs/PROGRAMM_NOTBELEUCHTUNG.md` (Board/Status).

## 1. Arbeits-Loop (für alle gleich)

```
git switch -c <dein-name>/<thema>          # Branch: selman/… | leonis/… | enis/…
# nur in DEINEM Package arbeiten
.venv/Scripts/python.exe -m pytest -q      # grün halten
git commit  →  git push  →  PR öffnen
# CODEOWNERS fragt automatisch den richtigen Reviewer, CI (contract+ci) läuft
```

Regeln (aus CLAUDE.md): **kein Owner-Package importiert ein anderes** — nur
`notbeleuchtung.hauptengine.contracts`. Contract ändern = `contract_version` bumpen
+ `python scripts/gen_schema.py` + Approval **aller drei**.

---

## 2. Dein Einstieg je Owner

### Selman — `src/notbeleuchtung/raumerkennung/`  (Contract: **RaumModell**)
- **Ziel:** leerer Architekturplan (DXF) → `RaumModell` (Räume/Türen/Ausgänge/
  Fluchtweg-Zirkulation).
- **Du erfüllst** das Protocol `RaumProvider` (`contracts/ports.py`): `parse(dxf, floor) → RaumModell`.
- **Deine Ziel-Fixture:** `tests/fixtures/raum_modell_4og.json` — dein Parser muss
  am Ende so ein Objekt produzieren (schema-valide).
- **Port-Quelle** (aus elektro-planer, siehe `docs/PORT_LOG.md`): `backend/parsers/*`,
  `backend/engine/walls/*`, `backend/models/{room,component,project}.py` →
  `raumerkennung/_port/`. Test-Pläne liegen in `Projekte/`.
- **Erster Slice (4):** Parser portieren + `ArchitekturRaumProvider` bauen.

### Leonis — `src/notbeleuchtung/platzierung/`  (Contract: **PlatzierungsErgebnis**)
- **Ziel:** Platzierungs-Logik (wie/wann/wo Notbeleuchtungs-Symbole).
- **Du erfüllst** `Platzierer.place(raum, norm) → PlatzierungsErgebnis`.
- **Ziel-Fixture:** `tests/fixtures/platzierung_4og.json` (die 5 echten 4OG-RZ).
- **Port-Quelle:** `backend/diagnostics/inject_communal_stgh.py` →
  `communal_stgh_strategy.py`, `backend/engine/placement_geometry.py` → `geometry.py`.
- **Erster Slice (2):** Communal-STGH-Strategie gegen Fake-Raum + echte Norm.

### Enis — `src/notbeleuchtung/normwissen/`  (Contracts: **NormRegelwerk** + **LBVorgabe**)
- **Ziel:** Normwissen (EN 1838/ÖNorm) **+ LB-Parsing** (2. Input, du machst beide).
- **Du erfüllst** `NormProvider` (Query-API: `fuer_raum`, `fuer_fluchtweg_abschnitt`,
  `erkennungsweite_m` [l=z×h], `regelwerk_snapshot`). Leonis **fragt** dich — er
  parst nie YAML.
- **Ziel-Fixture:** `tests/fixtures/norm_regelwerk_snapshot.json`.
- **Port-Quelle:** `backend/rules/{emergency_lighting_en1838,rz_coverage_oenorm,
  clearance_rules,heights_fachpraxis,circuit_rules_ove_8015,circuit_label_policy}.yaml`
  → `normwissen/data/`.
- **Erster Slice (1):** Norm-YAMLs portieren + `En1838NormProvider`. Danach eigener
  Slice „LB-Input": Contract `LBVorgabe` + LB-Parser (`normwissen/lb/`).

---

## 3. Woran ihr merkt, dass ihr fertig seid (DoD)
Siehe `docs/PROGRAMM_NOTBELEUCHTUNG.md` (Definition-of-Done je Slice). Kurz: dein
echter Provider ersetzt seinen Fake in `tests/fakes.py`, der E2E-Durchstich bleibt
grün, deine Naht-Invarianten (CI) sind grün.
