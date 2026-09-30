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

## P0 Am Rain: „Keine Wand-Entities gefunden" (nach dem Endstand)

**Befund (Leonis):** `provider.parse` bricht auf Am Rain (ARAI5-Dialekt) mit
`ValueError: Keine Wand-Entities gefunden — Layer-Muster prüfen.` ab.

**Leonis lief nicht auf einem alten Stand.** Der Abbruch ließ sich auf dem
Integrationsstand nachstellen. `dxf_load.py`, der Provider-Guard und `wandkoerper.py`
sind auf `origin/main` `acdacba`, auf allen Zweigen der Merge-Reihe und auf
`origin/leonis/demo-l-gebaeude` `8257ff9` byte-gleich. OG4 bricht auf `acdacba` und auf
`aa05143` gleich ab (5,0 s bzw. 5,2 s).

**Ursache.** Die ARAI5-Layer heißen `Wand <Material> <Tragwirkung>` oder schlicht `Wand`.
Keine Alternative von `WALL_PATTERN` trifft sie. Weil `provider.parse` die Kaskade nur bei
erkannten Wand-Entities startete (Guard aus `336fb77`), blieb die Wandkörper-Liste leer, und
der ValueError aus `bounds_mm` wurde erneut geworfen. Die Erscheinungsbild-Erkennung aus
`bbfa734` hätte getragen, sie wurde nur nie aufgerufen. Hinter dem Guard lag eine zweite
Falle: Weltkoordinaten-Blockkopien bei x≈34,6 km. Sie spannen die Wandkörper-Box auf
34,7 km auf. Rechnerisch wären das 15,4 GiB je bool-Array in der Rest-Stufe, und die hat
keine Reißleine.

**Owner-Regel (2026-09-30):** Fehlende Wand-Entities führen zu keinem ValueError. Stattdessen
gibt es eine Warnung, und die Erkennung läuft über das Erscheinungsbild weiter: HATCH
beliebiger Layer, schmale Polygone, Doppellinien.

| Commit | Inhalt |
|--------|--------|
| `a845ded` | Tests zuerst rot: synthetische DXF ohne Wand-Layer mit HATCH-Wänden und einem Fern-Körper (ValueError), Doppellinien auf `Wand Trockenbau` (0 == 1), Fern-Körper-Filter (6 == 5), Naht Am Rain OG4 aus dem getrackten Zip (ValueError) |
| `ed292e1` | Fix, siehe unten |

Was der Fix ändert:

- **`provider.parse`:**
  - Die Kaskade läuft immer.
  - Die Bounds kommen aus den Wandkörpern. Gibt es keine, kommen sie aus allen Entities.
  - Die Warnung `keine_wand_entities` landet in `wand_warnungen`. Wie `tuer_warnungen` ist das
    kein Contract-Feld.
  - Einen ValueError gibt es nur noch bei einer DXF ganz ohne Geometrie.
- **`wandkoerper`:** Nur wenn kein Wand-Layer erkannt ist:
  - Körper, deren Schwerpunkt mehr als 500 m (`_SPAN_MAX_MM`) vom Median-Schwerpunkt entfernt
    liegt, fallen weg.
  - Der Doppellinien-Fallback liest die Layer mit Wand-Hinweis.

  Pläne mit Wand-Layer laufen unverändert.

**Was der Fern-Filter auf Am Rain wegnimmt:** nur Blockkopien auf Layer `0` bei
x 34,58–34,79 km, nichts aus dem Grundriss.
- OG4: 20 von 198 (`*U25` 12, `*U26` 8)
- UG: 294 von 1 015 (Leuchten-Blöcke `SIMA_ET_BELEUCHTUNG_*` der E-Planung)
- EG: 116 von 6 259 (`*U60`, `*U52`, `*U45`)

### Am Rain auf `ed292e1`, jeder Plan allein

| Plan | Ergebnis | Räume | Türen | Ausgänge | wohnung_id | Stiegenhäuser | Wandkörper | Warnungen | parse | Peak Working Set |
|------|----------|-------|-------|----------|------------|---------------|------------|-----------|-------|------------------|
| OG4 | ok | 27 | 58 | 0 | 11 | 0 | 178 | `keine_wand_entities`; Ausgang: „kein Geschossausgang ableitbar"; 23 `seite_fehlt` | 21,8 s | 0,43 GB |
| UG | ok | 82 | 295 | 6 (2 final_exit, 4 stair_exit) | 7 | 7 | 721 | `keine_wand_entities`; 10 Fluchtweg („kein final_exit erreichbar"); 159 `seite_fehlt` | 110,0 s | 3,91 GB |
| EG | ok | 136 | 317 | 3 (2 final_exit, 1 stair_exit) | 50 | 3 | 6 143 | `keine_wand_entities`; 13 Fluchtweg („kein final_exit erreichbar"); 186 `seite_fehlt` | 485,8 s | 6,30 GB |

Die UG- und EG-Läufe stammen vom Arbeitsbaum vor der letzten Textänderung der Warnung.
Die Logik war für Pläne ohne Wand-Layer dieselbe. OG4 lief auf dem Endstand noch einmal:
Die Zahlen sind gleich.

**Noch nicht abnahmefähig:**
- OG4 hat 0 Ausgänge und kein Stiegenhaus, obwohl der Plan die Layer `Treppe` und `Aufzug` trägt.
- Die OG4-Bounds enden bei x 63,6 m. Die Wand-Linien reichen bis 78,1 m, und der Teil
  dahinter hat keine Hatch-Wandkörper. Das ist nicht weiter untersucht.
- EG braucht 8 min und 6,3 GB.
- OG1–OG3 wurden nicht gemessen.

### Prüfpläne und Gate auf `ed292e1`

- **12 Prüfpläne feldgleich:** Rennweg UG/EG/OG1/OG2/OG3/DG1/DG2/DD, Barawitzka EG,
  Mollgasse EG/1OG und Muthgasse E2. Jeder Plan hat 49/49 Schlüssel gleich (Räume, Türen,
  Rollen, Wohnungen, Segmente, Ausgänge, Anker, Platzierung). Verglichen wurde vorher
  `a845ded` gegen nachher. Muthgasse lief jeweils allein.
- **`pytest tests/raumerkennung tests/contract`:** 867 passed, 6 skipped, 2 xfailed. Das
  sind die 863 von `b20b4e5` plus 4 neue Tests.
- **`pytest -m gate tests/gate`:** 3 passed, 1 xfailed.
- **Messung `_arbeit/gate/messung_ed292e1.json`** (nicht versioniert, `src`/`scripts`
  sauber), `pruefe_gate` gegen `nullmessung_f15d03f`: **1 Verstoß**, (3) `M4.einraum`
  steigt in DG2 von 0 auf 1. M17 ist 18/18. Alle Abschnitte gleichen `messung_b20b4e5.json`.
- `ruff check .`: All checks passed.

### Am Rain in der Prüfstrecke

- Die Quelle ist das getrackte Zip `Projekte/Am Rain.zip` mit 6 DXF:
  `Am Rain/ARAI5_FE_XEL_ZZ_MOP_<Geschoss>_00NN_V_0N.dxf`.
- Eine getrackte DXF-Kopie unter `Projekte/` gibt es nicht. Darum hat `tests/plaene.py`
  keinen Eintrag. Die Naht `test_naht_am_rain_og4_parse_ohne_abbruch` entpackt OG4 aus dem Zip.
- Arbeitskopien für Ad-hoc-Läufe liegen in `Projekte/_eingang/AmRain_<Geschoss>.dxf`
  (UG, EG, OG1–OG4). Sie sind untracked und CRC-gleich mit dem Zip.
- **Wichtig für Läufe:** Am-Rain-Läufe laufen einzeln, und nichts läuft parallel dazu
  (EG 6,3 GB).

### Offen (Owner)

- Soll `Wand brüstungshoch` als raumbildende Wand zählen? Heute zählen ihre Hatches über den
  Wand-Hinweis.
- `_NEGATIV_LAYER` trifft „Moeblierung" und „Möblierung" nicht. Im EG zählen die
  Freiraum-Hatches `KFLD-04_…Moeblierung-Bank` und `…-Pergola` deshalb als Wandkörper.
- Das UG ist als leerer Architekturplan abgelegt, enthält aber schon E-Planung
  (45 `SIMA_ET_SIBEL_Sicherheitsleuchte`).

## Gegenprüfung auf `9f38f58` (unabhängig nachgemessen)

Code-Stand `9f38f58` = `ed292e1` (`git diff ed292e1 9f38f58 -- src scripts tests` leer).
Jeder Lauf allein, nichts parallel.

**Inhalt.** `git merge-base --is-ancestor <sha> HEAD` ist für jeden Slice-Kopf wahr:
`3e95974`, `1e5e5ac`, `1f3c8ff` (und `bface2b`), `e979957` (und `1eed916`), `4f85492`,
`76de2be`, `aa05143`, `60c671a`, `c2d4e33` (und `381c033`, `de31621`), `f682c77`,
`fac7118` (und `5bd4ff2`), `e5f6274`. K1 `558dee3` ist KEIN Vorfahr. Der Diff
`origin/main..HEAD` über `hauptengine/`, `platzierung/` und `normwissen/` ist leer,
`gen_schema.py --check` meldet „schema in sync“, `ruff check .` ist grün. Jeder Merge-Commit
wurde gegen `git merge-tree --write-tree` seiner beiden Eltern verglichen: nur K3
(`provider.py`, `docs/SLICES_K1_K4.md`) und K4 (`docs/SLICES_K1_K4.md`) weichen ab, genau die
oben beschriebenen Konfliktauflösungen.

**Volle Suite** (`pytest -rfxXs`, 27:34 min): `6 failed, 2223 passed, 11 skipped,
6 deselected, 14 xfailed`, 0 xpassed. Das sind die 2219 von `b20b4e5` plus die 4 P0-Tests.
Rot sind die 4 bekannten Tests und die 2 S4c-Pins. Beide Pins scheitern auf `e979957` allein
mit derselben Ausgabe (`raum_29` zusätzlich, `seg_graph_tuer_27` zusätzlich). Die
xfail- und skip-Listen sind dieselben wie oben. Die skip-Zeile `test_provider.py` steht jetzt
bei `:25` statt `:21`, weil der P0-Commit dort Importe ergänzt.

**Bänder.** In `tests/` stehen auf `origin/main` 14 xfail-Marker, auf HEAD 15. Neu ist nur
der strict-Marker von `test_gate_tuerstapel_erfuellt`; kein Marker ist entfernt oder
entschärft. Die einzige gesenkte Schwelle im Diff ist das Stiegenhaus-Band in
`test_soll_muthgasse.py::test_soll_raeume_tueren_ausgaenge` (≥ 5 → ≥ 3). Es kommt aus S5c,
nicht aus der Integration: Owner-Entscheid B2, `docs/GATE_TUERSTAPEL.md:2304`, im Test
begründet. Die übrigen geänderten Zusicherungen folgen Owner-Regeln der Slices (K2 NISCHE
statt SCHACHT, E7 rohe Rollen) und sind keine Schwellen.

**Gate.** `pytest -m gate tests/gate` ergibt 3 passed und 1 xfailed. Die Messung
`_arbeit/gate/messung_9f38f58.json` (Arbeitsbaum `src`/`scripts` sauber) ist ohne `meta`
gleich `messung_b20b4e5.json`. `pruefe_gate` gegen die Nullmessung `f15d03f` meldet
**1 Verstoß: (3) `M4.einraum` DG2 0 → 1** (Enis' Board 3). Einzelwerte:
- M17 18/18
- (10) `raum_28` 1 Tür (`tuer_17`, arc, 830 mm, zimmertuer)
- (6) OG3 5 GRAPH-Segmente, 0 Anker in `WOHNUNG_PRIVAT`
- (11) DG1 2 Ausgänge, 0 durch den Liftschacht; zur Information UG, EG und OG1 ebenfalls je 0
- M3 DG2 4 Räume / 1,26 m²

**Stichprobe Prüfstrecke.** Für Rennweg_OG3, Mollgasse_1KG, AmRain_OG4 und Barawitzka_EG
wurde die Kennzahlen-Tabelle aus `raeume.json` und `bericht.md` nachgerechnet. Alle Werte
stimmen: Räume mit Polygon, davon ohne Typ, Stempel ohne Polygon, Wohnungen, Türen,
Ausgänge, Segmente, Leuchten-Summe, Warnungen und Laufzeit. Die Aufteilung rz/SL steht nicht
in den Dateien. Geprüft ist dort nur die Summe.

### Naht für Leonis: was am Code gilt

Die Aussagen stammen aus dem Übergabe-Auftrag. Geprüft ist der Code auf `9f38f58`. Die
„Probe“ ist ein `provider.parse` auf Rennweg UG/EG/OG1/OG2/OG3/DG1/DG2/DD und Mollgasse
EG/1OG.

| Aussage | Befund | Beleg |
|---|---|---|
| Nutzungsklassen WOHNUNG_PRIVAT, ALLGEMEIN_ERSCHLIESSUNG, ALLGEMEIN_NEBENRAUM, KEIN_RAUM, UNBESTIMMT | **gilt nicht wörtlich** | Der Contract kennt `WOHNUNG_PRIVAT`, `ALLGEMEIN_ERSCHLIESSUNG`, `ALLGEMEIN_NEBENRAUM`, `AUSSEN` und `KEIN_RAUM` (`raum_modell.py:22-25`). Einen Wert „UNBESTIMMT“ gibt es nicht: unbestimmt heißt `nutzungsklasse is None` (`raum_modell.py:124-125`, `wohnungsklasse.py:58`). `AUSSEN` (BALKON, TERRASSE, `nutzungsklasse.py:41-43`) fehlt in der Liste. |
| `wohnung_id` | **gilt** | Die ID kommt nur aus rohen Türen, `top_1..n` nach der kleinsten Raum-ID (`wohnungen.py:3-6`, `:354-360`). Die Klasse ändert keine Wohnung. |
| `tuer_detail` und korrigierte Türrollen, „277 kippen auf Wohnungseingang“ | **gilt nicht** | `tuer_detail` bleibt die ROHE Rolle (`wohnungsklasse.py:21`, `:698-705`). Die korrigierten Rollen stehen nicht im Modell. Nur `fluchtweg.py:329` und `plan_pruefen.py:1281` lesen sie. Die Platzierung liest `tuer_detail`, also die rohe Rolle (`platzierung/fachpraxis.py:400`, `:461`, `:524`). Die 277 ist überholt: nach dem K4-Nachzug sind es netto **270** gegen `f682c77` (`docs/SLICES_K1_K4.md:1345`, `:1358`). Das ist ein Delta der korrigierten Rollen, kein Modellfeld. Es kippt in beide Richtungen, Probe Mollgasse 1OG: 10 × zimmertuer → wohnungseingang, 9 × wohnungseingang → zimmertuer. |
| LIFT und SCHACHT sind KEIN_RAUM, ausgestanzt, kein Ausgang durch den Liftschacht | **gilt**, mit zwei Zusätzen | LIFT ist `KEIN_RAUM` und wird aus STIEGENHAUS gestanzt (`lift_erkennung.py:187-222`). SCHACHT wird `KEIN_RAUM` (`nutzungsklasse.py:45-46`, `wohnungen.py:195-196`). In der Probe tragen alle LIFT/SCHACHT `KEIN_RAUM`. Gate (11) siehe oben. Die S5c-Liftschacht-Reste bleiben ungestanzt, sie sind eigene Räume (`lift_erkennung.py:242-244`). **Neu an der Naht (K2):** eine türlose Fläche < 3 m² ohne Schacht-Beleg ist jetzt `NISCHE` mit `nutzungsklasse None` und Flags 00, NICHT `KEIN_RAUM` (`rest_komponenten.py:216-223`; Rennweg DG2 `rest_5`, 1,42 m²). Auf der Konsumentenseite stehen im Lauf auf `bc2ccf0` noch Leuchten in LIFT/SCHACHT (VERLAUF: Muthgasse_E2 und Mollgasse_2KG je 1 in LIFT, AmRain_OG1 1 in SCHACHT). |
| final_exit nur mit Türbezug und Geschoss, Balkontüren kein Ausgang | **teilweise** | **Geschoss gilt:** fail closed, kein final_exit im OG oder bei unbekanntem Geschoss (`ausgaenge.py:116-128`). **Türbezug gilt nicht:** `footprint.hauptausgaenge` erzeugt final_exit ohne Tür (`provider.py:175`, `footprint.py:123-135`), und die überleben im EG/UG. Beispiel: Mollgasse EG `exit_1` … `exit_4`, 4 von 8 final_exit. Das ist der offene Punkt S4g a (`docs/OFFENE_FRAGEN.md:1576-1579`). Ein final_exit kann auch an einer Tür ohne Rolle hängen, über `ist_notausgang` ins Freie (`ausgaenge.py:84-85`). Beispiel: Mollgasse EG `exit_tuer_67` (roh `None`, AUSSEN\|`raum_61`) ist die gewollte EG-Ausnahme Südgarten-Tür (`tuer_typisierung.py:179` `not eg`, S4g c). **Balkontür gilt:** `balkontuer` setzt `ist_notausgang=False`, und ein Türtext dreht das nicht zurück (`tuer_typisierung.py:179-189`, `:225-227`). In der Probe ist keine balkontuer ein Ausgang. **Zusatz:** Hat ein OG sonst keinen Ausgang, wird der rohe Wohnungseingang ins Stiegenhaus zum stair_exit (S5c F2, `ausgaenge.py:50-59`, `:91-92`). Beispiele: Rennweg DG1 `exit_durchgang_6`/`_7`, DG2 `exit_durchgang_4`/`_5`/`_6`. |
| Fluchtweg-Segmente mit `durchleitung=True` durch private Räume | **gilt nicht** | `FluchtwegSegment` hat kein Feld `durchleitung` (`raum_modell.py:184-196`). Das Feld ist nur ein Board-Antrag (`provider.py:104-107`). Erkennbar ist eine Durchleitung so: ein GRAPH-Segment läuft durch einen `WOHNUNG_PRIVAT`-Raum mit Flags 00 als Direktlinie Tür → Tür, ohne Stützpunkt, und dieser Raum ist nie `start_raum` oder `ziel_raum` (`fluchtweg.py:20-27`, `:382-399`). Dazu schreibt die Prüfstrecke die Zeile `durchleitung: seg_graph_<tür> …` (`provider.wohnungsklasse_warnungen`, `bericht.md`). Gemessen gibt es 0 Durchleitungen: in allen 13 Berichten der Prüfstrecke und in der Probe. |
| Private Vorräume zählen nicht als Erschließung, Mollgasse 1OG `raum_35` hat 9 statt 17 Start/Ziel-Segmente | **gilt** | Probe: `raum_35` ist STIEGENHAUS mit 9 Start/Ziel-Segmenten. `raum_2` und `raum_4` sind VORRAUM, `WOHNUNG_PRIVAT`, Flags 00. `test_messfall_i_stiegenhaus_raum_35` ist grün (`MESSFALL_I_MOLL = (2, 9)`, `tests/naht/test_s7_wohnungsklasse.py:322`). Begründung: die 8 inneren Türen der ankerbestätigt privaten Vorräume sind Zimmertüren, Owner Option A vom 2026-09-26 (`docs/GATE_TUERSTAPEL.md:1198`, `:1204-1210`). `raum_35` ist das Stiegenhaus, nicht der Vorraum. |
| UNBESTIMMT-Räume behalten Notlicht (Flags 11) | **gilt mit Einschränkung** | Entzogen wird nur über `bestaetigt_privat` (`wohnungsklasse.py:406-435`). Unbestimmte GANG/VORRAUM tragen Flags 11 (`wohnungsklasse.py:945`). Probe: Rennweg OG3 `raum_10`, Mollgasse EG 2 VORRAUM und 1 GANG. **Unbestimmte Räume anderer Typen tragen Flags 00:** untypisierte Räume und NISCHE, in der Probe z.B. Rennweg UG 11, Mollgasse EG 11, Mollgasse 1OG 8. Ihr Notlicht behalten sie trotzdem, weil `flaechen_strategy.py:162-166` nur `WOHNUNG_PRIVAT` ohne Flags auslässt. Umgekehrt gibt es `WOHNUNG_PRIVAT` MIT Flags 11 (K4): Rennweg DG1 `raum_4`/`raum_8`, DG2 `raum_1`, Mollgasse 1OG 5 Räume. Die Platzierung muss also die Flags lesen, nicht nur die Klasse. |
