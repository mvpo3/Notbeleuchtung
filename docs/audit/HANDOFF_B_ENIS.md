# HANDOFF B — an Enis (normwissen-Lane)

**Protokoll, keine Freigabe-Anfrage.** Der Owner hat die Contract-/YAML-Berührungen für
die Block-3-Fixes des Branches `leonis/wissensabgleich-engine` vorab autorisiert. Diese
Datei hält fest, was Leonis in Enis' Lane (`hauptengine/contracts/**`, `normwissen/data/**`,
`normwissen/provider.py`) angefasst hat, damit Enis es abnehmen / weiterpflegen kann.

Geltungs-Tags: `[AT-verbindlich]` (OVE E 8101:2025 · ÖNORM EN 1838) · `[AT-Referenzpraxis]` ·
`[DE-only]`. Beleg je Eintrag.

---

## F09 — Wartungsfaktor (Maintenance Factor) innen 0,80 / außen 0,57  (W07, A1 F02)

**Commit:** siehe `git log` (fix(F09)). **Contract-Bump 1.2.0 → 1.3.0**, Schema regeneriert.

**Contract** (`hauptengine/contracts/norm_regelwerk.py`):
- Neues Feld `NormAnforderung.wartungsfaktor: float | None = None` (additiv, default None =
  inert → Konsument rechnet 1,0). `CONTRACT_VERSION` 1.2.0 → **1.3.0**. `scripts/gen_schema.py`
  gelaufen → `schema/norm_regelwerk.schema.json` nachgezogen (Drift-Gate grün).

**YAML** (`normwissen/data/en1838_grundwerte.yaml`):
- Neue Sektion `wartungsfaktor: {innen: 0.80, aussen: 0.57}`.

**Provider** (`normwissen/provider.py`):
- `_anforderung_aus_regel` setzt `wartungsfaktor = _wartungsfaktor_innen()` (liest
  `wartungsfaktor.innen`). Regel-basierte Räume sind alle **innen**.

**Geltung / Beleg — WICHTIG (Abweichung vom ursprünglichen Plan-Tag):**
- Tag = **`[AT-Referenzpraxis]`**, NICHT `[AT-verbindlich]`. Begründung: Der Wartungsfaktor
  ist in **EN 1838 NICHT beziffert** (die Norm-Lux sind bereits maintained values; der Plan
  mit MF zu rechnen ist fachlich zwingend, aber die konkreten 0,80/0,57 sind Fachpraxis).
  Beleg = `knowledge/extracted/LICHTBERECHNUNG_REFERENZ.md` (3 echte Relux/DIALux-Profi-
  Reports: 0,80 innen / 0,57 außen). Die YAML selbst dokumentiert (Z. 136–147), dass solche
  Werte nicht in EN 1838 stehen — deshalb ehrlich als `[PRAXIS]` markiert.
- **Offen für Enis:** Wenn eine AT-verbindliche Quelle für den MF existiert (OVE E 8101 /
  ÖVE E 8002?), Tag + Quelle schärfen. Bis dahin Referenzpraxis.

**Außen-Wert (0,57) ist dokumentiert, aber (noch) inert:** Die Engine rechnet Lux nur
**innen** (Korridor-Deckung, Aufheller, Nachweis). `aussen_strategy.plan_aussenleuchten`
platziert die SL vor dem Schlussausgang **bedingungslos** (kein Lux-Nachweis) und zieht
`_referenz(norm, "sicherheitsleuchte")` — es gibt keinen separaten Außen-Query. Der 0,57-Wert
bekommt erst Wirkung, wenn ein Außen-Lux-Nachweis existiert (künftiger Slice / Enis-Naht).

**Wirkung gemessen:** voller `pytest` = **1029 passed / 36 skipped**, KEIN Golden-Shift.
Die E2E-Fixtures sind min-abstand-gebunden → 0,80 ändert die SL-**Zahl** nicht; der Wert
fließt aber in den **Lux-Nachweis-Bericht** (maintained values, 0,80×). Platzierung bit-
stabil, Nachweis-Zahlen korrekt gesenkt.

**F11 (Antipanik-Flächen-Schwellen 60/8 m²) — ZURÜCKGENOMMEN (Owner-Entscheid 2026-09-10):**
nach dem Sync von origin/main kollidierte die Füllung mit Enis' NEUEN Guard-Tests
(`test_astv_arbeitsstaetten`, `test_quellenblock_e07_rl4`: `flaechen_schwellen is None`).
Der Owner hat F11 daraufhin revertet → `flaechen_schwellen` bleibt leer (None), Enis'
Guards grün. Das Scope-Gate (`BLOCKER2_FLAECHEN_SCOPE.md`) bleibt die offene 3-Owner-Frage.

---

## F13 — RZ-Montagehöhen-Schranke 10 m (weiche Warnung)  (W01, A1 F07/08)

**Contract-Bump 1.3.0 → 1.4.0**, Schema regeneriert.

**Contract** (`norm_regelwerk.py`): additives Feld `NormAnforderung.montagehoehe_max_mm:
int | None = None`. `CONTRACT_VERSION` 1.3.0 → **1.4.0** + `gen_schema.py`.

**YAML** (`en1838_grundwerte.yaml`): `rz_montagehoehe_max_mm: 10000`.

**Provider** (`provider.py`): `_rz_montagehoehe_max_mm()` → in jede `NormAnforderung`.

**validierung** (`validierung.py`): neue Regel **1b** — RZ mit `height_mm > montagehoehe_max`
geben eine **WEICHE Warnung** (kein Hard-Stop; real bis 10,8 m gebaut, Barawitzka). Grenzwert
aus `_rz_hoehe_max_mm(norm)` (Norm-Lookup via `fuer_raum`), None → Regel inaktiv.

**Geltung:** `[AT-Referenzpraxis]` (EN 1838 §5.5 l=z·h stützt das Prinzip; der 10-m-Wert
selbst ist Praxis, nicht beziffert). Inert auf aktuellen Fixtures (Höhen ≤ 2400 mm).

**NICHT gebaut — Handoff an Selman/3-Owner:** die **podest-gestaffelte Montagehöhe** selbst.
Grund: `Podest` (`raum_modell.py`) trägt **keine Elevation/Höhe** — nur `polygon_mm` +
`ist_hauptpodest`. Ohne Podest-Höhe je Geschoss kann die Staffelung nicht datengetrieben
gesetzt werden. Braucht ein Höhenfeld am `Podest`/`Treppenlauf`-Contract (3-Owner) +
Selman-Befüllung. Bis dahin bleibt der Norm-Floor (2000 mm) Untergrenze und die 10-m-Warnung
der obere Guard.
