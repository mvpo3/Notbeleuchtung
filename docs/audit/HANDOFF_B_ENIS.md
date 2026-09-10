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

---

## F11 — Antipanik-Flächen-Schwellen 60 m² / 8 m² gefüllt  (W11, A1 F15)

**⚠️ Owner-Entscheid 2026-09-10: bewusst GEFÜLLT, obwohl Enis sie bewusst leer hielt.**
Kein Contract-Bump (Felder `FlaechenSchwellen.antipanik_min_m2`/`wc_sanitaer_min_m2`
existierten schon seit v1.2.0). **Bitte gegenprüfen** — das war deine offene 3-Owner-/
Scope-Gate-Frage (`docs/proposals/BLOCKER2_FLAECHEN_SCOPE.md`).

**YAML** (`normwissen/data/en1838_grundwerte.yaml`): neue Sektion `flaechen_schwellen:
{antipanik_min_m2: 60.0, wc_sanitaer_min_m2: 8.0, quelle: "OVE E 8101:2019 718.560.9.001.AT"}`.
Ersetzt den vorherigen „NICHT hier modelliert"-Kommentar.

**Provider** (`normwissen/provider.py`): neues `_flaechen_schwellen()` baut
`FlaechenSchwellen` aus der YAML; die Quelle wird in `NormRegelwerk.quellen` aufgenommen
(Naht-Invariante `FlaechenSchwellen.quelle ∈ quellen`). `FlaechenSchwellen` jetzt aus
`hauptengine.contracts` exportiert (`__init__`).

**Geltung / Beleg:** `[AT-Referenzpraxis]`. 60/8 m² stehen **NICHT in EN 1838**; belegt in
OVE E 8101:2019 718.560.9.001.AT (Sanitär ab 8 m²) bzw. Referenz-Praxis (Antipanik ~60 m²).

**Warum das NICHT global wirkt:** Der Konsument `flaechen_strategy._flaechen_trigger_greift`
ist **OVE-scope-gated + fail-closed** — er feuert nur, wenn `sanitaer_scope`/`verkehr_scope`
(aus dem OibBefund) `== "anwendbar"`. Wohn-/Bürofixtures ohne diesen OIB-Scope → Trigger
bleibt inert. Voller `pytest` grün, KEIN Golden-Shift (keine Fixture trägt den OVE-Scope).

**Nachgezogene Guard-Tests (Enis' Lane — Owner-autorisiert):**
- `test_norm_werte.test_flaechen_schwellen_bleiben_ohne_en_1838_beleg_leer` →
  `test_flaechen_schwellen_gefuellt_als_ove_referenzpraxis` (60/8 + Quelle + ∈ quellen).
- `test_ove_zusatz_erforderlichkeit.test_schwellen_bleiben_leer` →
  `test_schwellen_gefuellt_aber_scope_gated`.
- `test_quellen_sind_die_drei_raumregeln_plus_die_sonderstellen` um die OVE-Quelle ergänzt.
- Neuer Fix-Test `test_antipanik_trigger_referenzpraxis` (Schwellen-Grenzen exakt).

**Offen für Enis / 3-Owner:** Der `verkehr_scope` liefert heute nie `anwendbar`
(Raumkategorien fehlen im RaumModell) → die 60-m²-Antipanik-Schwelle ist faktisch weiter
inert, bis der Scope real bewertbar wird. `sanitaer_scope` wäre für Verkaufsstätten
> 3.000 m² begründbar. Das eigentliche Scope-Gate-Design (`BLOCKER2_FLAECHEN_SCOPE.md`)
bleibt deine/3-Owner-Entscheidung — hier sind nur die Werte + der Audit-Trail gesetzt.

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
