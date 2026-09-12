# 07 — Sichtprüfung & Verify (Wissensabgleich, Branch `leonis/wissensabgleich-engine`)

Stand 2026-09-10, **vor Push** (STOP-Gate). Basis main `fd65839`.

## Verify-Batterie (Phase 4)
- **Voller `pytest`:** **1032 passed, 36 skipped, 2 deselected** (zuletzt nach F13). Grün.
- **Contract-Drift-Gate:** grün. `scripts/gen_schema.py` gelaufen; Schema in sync.
  Contract-Bumps: **1.2.0 → 1.3.0 (F09)** → **1.4.0 (F13)**, beide additiv (neue optionale
  Felder, keine Breaking Changes).
- **ruff:** getrackter Code clean. (29 Treffer ausschließlich in `scratchpad/` = untracked
  Demo-Skripte, nicht Teil der Commits.)
- **E2E-Durchstich:** `tests/e2e/test_familien_durchstich.py` (Mollgasse/Fischamender/
  Herrenholz/Barawitzka) + `test_wohnbau_durchstich.py` + `test_mollgasse_eg_durchstich.py`
  laufen grün durch `pipeline.run` — Prüfstatus `ok`, Symbolzahlen unverändert.

## Sichtprüfungs-Abweichungen ggü. 4OG-GU / Fixtures
**Keine.** Alle vier gebauten Fixes sind auf den vorhandenen Fixtures **verhaltens-inert**
(kein Golden-Shift, kein geändertes DXF/PDF):
- **F07** (≥2-Redundanz): `garantiere_redundanz` ist segment-genau/minimal → No-op, wo schon
  ≥2 Leuchten je Abschnitt liegen (Barawitzka etc. erfüllen das). Hard-Fail greift nur bei
  echten Unterversorgungen.
- **F09** (Wartungsfaktor 0,80): Fixtures sind min-abstand-gebunden → SL-Zahl unverändert;
  Wirkung nur in den Nachweis-Zahlen (maintained values).
- **F11** (Flächen-Trigger 60/8): OVE-scope-gated + fail-closed → inert ohne OIB-Scope.
- **F13** (10-m-Warnung): Fixture-Montagehöhen ≤ 2400 mm → Regel meldet überall „ok".

→ Eine visuelle AutoCAD-Sichtprüfung eines frischen Renders gegen das 4OG-GU-PDF ist damit
ohne erwartete Delta; der end-to-end-Render-Pfad ist über die E2E-Durchstiche abgesichert.
Ein voller Projekt-Batch-Render läuft im Owner-Terminal (`!`), da Hintergrund-Renders hier
gekillt werden — bei Bedarf nach dem Push.

## Gebaute Fixes (Commit-Liste Block 2 + 3)
| Fix | Commit | Art | Contract |
|-----|--------|-----|----------|
| F08 | `b49e968` | docs + Test (erkennungsweite Prod-Pfad belegt, sichtlinie test-only) | — |
| F07 | `0d06660` | **Verhalten** (Redundanz-Garantie + Hard-Fail) | — |
| F09 | `8e60044` | Wartungsfaktor 0,80/0,57 aus Norm | **1.3.0** |
| F11 | `f33ec9b` | Flächen-Trigger 60/8 gefüllt (Owner-Entscheid) | — |
| F14 | `1390c06` | Regression-Test Layer grün/gelb | — |
| F13 | `7320e1b` | RZ-10-m-Warnung | **1.4.0** |

## NICHT gebaut — bewusste Abweichungen / Handoffs
- **F12 (Randbereich seitenselektiv)** — **SKIP** (Owner-Entscheid 2026-09-10). Kollidiert mit
  Enis' dokumentierter §4.3.1-Lesart (`en1838_grundwerte.yaml`: 0,5-m-Randstreifen bewusst
  **umlaufend**) und änderte den Antipanik-Pass/Fail. **Braucht Norm-Abstimmung mit Enis**
  (Befund A3: seitenselektiv vs. umlaufend belegen), bevor `lux.lux_raster` angefasst wird.
- **F13 Podest-gestaffelte Höhe** — Handoff. `Podest` trägt keine Elevation → Contract/
  3-Owner + Selman-Befüllung nötig. Gebaut wurde nur die obere 10-m-Warnung.
- **F10 (Blendungsgrenzen f(h))** — Handoff. Hängt an Enis' h-abhängigen cd/m²-Grenzwerten
  (W04, EN 1838 §4.1); ohne die Werte kein Fix.
- **F15–F18** — Block 4, wie zugesagt NICHT gebaut (3-Owner/Selman): `decision_source`-Contract
  (F15), Selman-Provider für Sonderstellen/Möbel/Flags (F16), vertikaler Nachweistyp (F17),
  totes YAML verdrahten/deklarieren (F18).

## Offene Review-Punkte für den Owner (am STOP)
1. **F11** wurde auf deinen Wunsch gefüllt, obwohl Enis die Schwellen bewusst leer hielt
   (Guard-Tests nachgezogen, Protokoll in `HANDOFF_B_ENIS.md`). **Gemeinsam ansehen** — v.a.
   ob der `verkehr_scope` je `anwendbar` werden soll (heute nie → Antipanik-60-m² faktisch
   weiter inert) und ob das Scope-Gate-Design aus `BLOCKER2_FLAECHEN_SCOPE.md` nachzuziehen ist.
2. **Zwei Contract-Bumps** (1.3.0 F09, 1.4.0 F13) berühren `hauptengine/contracts` = 3-Owner-
   CODEOWNERS. Beide additiv + in `HANDOFF_B_ENIS.md` protokolliert (keine Freigabe-Anfrage
   laut Prompt) — bei Push brauchen sie dennoch Enis'/Selmans Kenntnisnahme.
