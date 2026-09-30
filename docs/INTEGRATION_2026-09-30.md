# Integrationsstand 2026-09-30 — alle fertigen Raumerkennungs-Slices auf einem Branch

**Branch:** `selman/integration-2026-09-30`, abgezweigt von `origin/main` `acdacba`.
**Zweck:** ein Stand, auf dem Leonis die Platzierung gegen die zusammengeführte
Raumerkennung testen kann. Nichts Neues gebaut — nur zusammengeführt und geprüft.
**Code-Stand der Messungen:** `b20b4e5` (letzter Merge). Der Commit mit dieser Datei
ändert nur `docs/`.

Fremde Packages sind unberührt: `git diff acdacba b20b4e5` über
`src/notbeleuchtung/hauptengine`, `platzierung` und `normwissen` ist leer. Die Contracts
sind unverändert (`gen_schema.py --check`: „schema in sync", `contract_version` 1.5.0).

## Merge-Reihe

Jeder Merge `git merge --no-ff`, ein Merge-Commit je Schritt. Nach jedem Merge
`pytest tests/raumerkennung tests/contract` und `pytest -m gate tests/gate`.

| # | Slice | Quelle (Kopf) | Merge-Commit | Konflikte | raumerkennung + contract | `-m gate` |
|---|-------|---------------|--------------|-----------|--------------------------|-----------|
| 1 | S4a | `selman/fix-s4a-tuerbloecke` `3e95974` (46 Commits, inkl. Tranche 1 und Gate-Gerüst) | `1b0dbf1` | keine (`pyproject.toml` automatisch: ENIS-Ausschluss aus main + Marker `gate`) | 432 passed, 6 skipped, 2 xfailed | 3 passed, 1 xfailed |
| 2 | S4b | `selman/fix-s4b-seitenprobe` `1e5e5ac` | `0b74bbf` | keine | 440 passed, 6 skipped, 2 xfailed | 3 passed, 1 xfailed |
| 3 | S5b + S7a + S7b | `selman/fix-s5b-querung` `1f3c8ff` (25 Commits) | `ea986c7` | keine | 698 passed, 6 skipped, 2 xfailed | 3 passed, 1 xfailed |
| 4 | S4c Fassung A | `selman/fix-s4c-doppelfluegel` `e979957` (43 Commits) | `47f7d85` | keine | 770 passed, 6 skipped, 2 xfailed | 3 passed, 1 xfailed |
| 5 | S7c | `4f85492` | — | Vorfahr von `47f7d85` (kam mit S4c) | — | — |
| 6 | S3b | `76de2be` | — | Vorfahr von `47f7d85` (kam mit S4c) | — | — |
| 7 | S5c | `aa05143` | — | Vorfahr von `47f7d85` (kam mit S4c) | — | — |
| 8 | VOK-a | `selman/fix-svok-schreibweise` `60c671a` | `e872d46` | keine (`docs/COORDINATION.md` automatisch) | 775 passed, 6 skipped, 2 xfailed | 3 passed, 1 xfailed |
| 9 | K2 (M3-Regel NISCHE wie SCHACHT) | `selman/fix-k2-schacht-beleg` `c2d4e33` (inkl. Darstellungsskripte `de31621`) | `55c3af7` | keine (`docs/GATE_TUERSTAPEL.md` M3-Definition automatisch) | 792 passed, 6 skipped, 2 xfailed | 3 passed, 1 xfailed |
| 10 | K3 | `selman/fix-k3-sanitaer-bad` `f682c77` | `c5fa624` | `provider.py`, `docs/SLICES_K1_K4.md` — aufgelöst, siehe unten | 839 passed, 6 skipped, 2 xfailed | 3 passed, 1 xfailed |
| 11 | K4 (R1-Aussetzung, Aufenthaltsraum-Sperre) | `selman/fix-k4-klasse-gang-vorraum` `fac7118` | `b20b4e5` | `docs/SLICES_K1_K4.md` — aufgelöst, siehe unten | 863 passed, 6 skipped, 2 xfailed | 3 passed, 1 xfailed |
| 12 | Gate-Doku | `selman/uebernahme-enis-m17` `e5f6274` | — | Vorfahr von `1f3c8ff` (kam mit Schritt 3) | — | — |

Weggelassen: **K1-Fix Sofa-Feld** — existiert nicht. K1 („Möbel sind keine Wände")
hatte eine falsche Prämisse, es wurde nichts gebaut (Bericht auf
`selman/fix-k1-moebel-keine-wand` `558dee3`).

Hinweis zu Schritt 3: `selman/fix-s5b-querung` steht inzwischen auf `bface2b` (reiner
Doku-Commit auf `1f3c8ff`). Gemerged wurde wie beauftragt `1f3c8ff`. `bface2b` ist
Vorfahr von S4c und kam mit Schritt 4 herein.

### Konfliktauflösungen

**`src/notbeleuchtung/raumerkennung/provider.py` (K3):** K3 zieht die Kette
Türzuordnung → Liftschacht-Reste → Durchgänge → Türrollen → Wohnungen in den Helfer
`_tueren_und_wohnungen`. Den Helfer nutzen sowohl der Sanitär-Probelauf auf Kopien als
auch der reguläre Lauf. S4c Fassung A hatte in genau diesem Block zwei Änderungen:
`andere_bogenrichtung` nach den Durchgängen und die `seite_fehlt`-Warnungen dahinter,
gefiltert auf Türen mit einer KEIN_RAUM-Seite.

Aufgelöst wurde so: Die K3-Struktur bleibt, und beide S4c-Schritte stehen unverändert
im Helfer, nach `aussen_durchgaenge` und vor `typisiere_tueren`. Damit laufen sie in
der Probe und im regulären Lauf gleich. Der Diff gegen `f682c77` besteht genau aus den
S4c-Änderungen.

Vor dem Commit liefen ruff sowie `test_sanitaer`, `test_wohnungsumriss`,
`test_tuer_zuordnung` und `test_tuerquellen` (109 passed). Dazu liefen die Naht-Tests
`test_k3_sanitaer_bad` und `test_soll_barawitzka` (13 passed, 3 xfailed).

**`docs/SLICES_K1_K4.md` (K3 add/add, K4 content):** Die Datei setzt sich so zusammen:
- Kopf aus K2
- ein Hinweis zum Integrationsstand
- Abschnitt K2 wörtlich aus `c2d4e33`
- Abschnitte K3 und K4 wörtlich aus `fac7118`

Dass die Abschnitte wörtlich übernommen sind, ist per `diff` geprüft.

## Endstand auf `b20b4e5`

### Volle Suite (allein gelaufen, 28 min)

`6 failed, 2219 passed, 11 skipped, 6 deselected, 14 xfailed` — 0 xpassed.

Rote Tests:

| Test | Einordnung |
|------|-----------|
| `tests/naht/test_s7_wohnungsklasse.py::test_keine_leuchten_in_wohnung_privat[pfad0-OG1]` | bekannt rot, Board 1 Leonis |
| `tests/naht/test_s7_wohnungsklasse.py::test_keine_leuchten_in_wohnung_privat[pfad1-OG2]` | bekannt rot, Board 1 Leonis |
| `tests/naht/test_s7_wohnungsklasse.py::test_keine_leuchten_in_wohnung_privat[pfad3-DG1]` | bekannt rot, Board 1 Leonis |
| `tests/naht/test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell` | bekannt rot (30 von 72 gegen Band ≥ 40) |
| `tests/naht/test_s7_wohnungsklasse.py::test_bara_raum_19_behaelt_klasse_und_zirkulation` | rot seit S4c Fassung A, im S4c-Nachzug gemeldet: `raum_29` (WC) zusätzlich in der Wohnung |
| `tests/naht/test_s7_wohnungsklasse.py::test_bara_raum_30_wird_nicht_von_der_auswertungsreihenfolge_entschieden` | rot seit S4c Fassung A, im S4c-Nachzug gemeldet: zusätzliches Segment `seg_graph_tuer_27` ab WC `raum_29` |

Die beiden S4c-Pins scheitern auf `e979957` (S4c allein) mit denselben
Assertion-Ausgaben. Es ist also kein Merge-Fehler. Nicht angepasst (Bänder nicht
absenken, Owner-Frage aus dem S4c-Nachzug).

### Gate (Türstapel)

- `pytest -m gate tests/gate`: 3 passed, 1 xfailed
  (`test_gate_tuerstapel_erfuellt`, erwartet solange (3) offen).
- Messung `_arbeit/gate/messung_b20b4e5.json` (nicht versioniert), Arbeitsbaum
  `src/`/`scripts/` sauber, `pruefe_gate` gegen `tests/gate/nullmessung_f15d03f.json`:
  **1 Verstoß — (3) `M4.einraum` steigt in DG2: 0 → 1.** Er hängt an Enis' Board 3
  (Blatt-Semantik).
- (10) Barawitzka ABSTELLRAUM 1,98 m² (`raum_28`): 1 Tür (`tuer_17`, arc, 830 mm,
  zimmertuer). Grün.
- (6) Rennweg OG3: 5 GRAPH-Segmente, 0 Anker in WOHNUNG_PRIVAT. Grün.
- (11) Rennweg DG1: 2 Ausgänge, 0 durch den Liftschacht. Grün.
- M3 DG2: 4 Räume / 1,26 m², gleich der Nullmessung (K2-Regel NISCHE wie SCHACHT).
- M17: 18/18 BESTANDEN.

### xfail und skip (volle Suite, `-rxXs`)

xfailed (14):
- `tests/naht/test_soll_barawitzka.py`: `test_soll_explizite_linien_vorhanden`,
  `test_soll_90_prozent_tueren_typisiert`, `test_soll_16_endpunkte_an_der_aussenkante_gedeckt`
- `tests/naht/test_soll_mollgasse.py`: `test_soll_jeder_endpunkt_an_der_kante_hat_final_exit`,
  `test_soll_90_prozent_tueren_typisiert`, `test_soll_final_exit_anzahl_gleich_endpunkte_an_der_kante`
- `tests/naht/test_soll_muthgasse.py`: `test_soll_jeder_plan_tuerblock_ist_tuer`,
  `test_soll_stair_exits`, `test_soll_stair_exit_aus_echter_blocktuer`,
  `test_soll_90_prozent_tueren_typisiert`
- `tests/naht/test_soll_referenzvergleich.py::test_soll_referenz_trefferquote`
- `tests/naht/test_soll_rennweg.py::test_soll_eg_90_prozent_tueren_typisiert`
- `tests/raumerkennung/test_ausgang_freiflaeche.py::test_soll_sentinel_aussen_ist_entscheidbar`
- `tests/raumerkennung/test_belichtung_grundlage.py::test_soll_natuerlich_belichtet_bleibt_none_ohne_grundlage`

Dazu im Gate-Lauf: `tests/gate/test_gate_tuerstapel.py::test_gate_tuerstapel_erfuellt`.

skipped (11):
- `tests/e2e/test_familien_durchstich.py:94` (Herrenholz-Erwartung)
- `tests/hauptengine/test_dwg_input.py:29` ×2 (ODA File Converter fehlt)
- `tests/naht/test_soll_baufeld.py:26/32` (Baufeld E2 nicht entpackt)
- `tests/raumerkennung/test_layer_korpus.py:137` (pyarrow fehlt)
- `tests/raumerkennung/test_dxf_load.py:15`, `test_provider.py:21`, `test_tueren.py:41`,
  `test_waende.py:18`, `test_zirkulation.py:18` (Mollgasse-Notbeleuchtungs-DXF
  `WHA_MOL_EG.dxf` nicht im Repo)

### Lint und Contract-Drift

- `ruff check .`: All checks passed.
- `scripts/gen_schema.py --check`: schema in sync.
