# 06 — Naht- und Owner-Matrix (A5)

Prüfung: Sind Enis · Leonis · Selman zueinander grün? Belege am Code (`datei:zeile`),
nicht am Board. Geltungs-Tag ist hier strukturell → Owner-Tag je Befund.

Owner-Grenzen (CLAUDE.md): Selman=`raumerkennung/`, Leonis=`platzierung/`,
Enis=`normwissen/`, gemeinsam=`hauptengine/` (Contracts + Pipeline + Render + Validierung).

---

## 1. Naht-Invarianten — greifen sie echt oder nur gegen Fakes?

### (a) `covers_segment ∈ RaumModell.zirkulation.segmente` (Leonis ↔ Selman)

| Ort | Provider | Beleg |
|-----|----------|-------|
| Contract-Test | **Fixtures** (JSON, kein Provider) | `tests/contract/test_platzierung_contract.py:49-56` — lädt `platzierung_4og.json` + `raum_modell_4og.json`, prüft `seg in {s.segment_id …}`. |
| E2E Fake | **echter Leonis-Placer + FakeRaum** | `tests/e2e/test_4og_durchstich.py:33-37` — `run(build_fake_bundle())`, `set(p.covers_segment) <= known`. `build_fake_bundle` nutzt echten `NotlichtPlatzierer` + `En1838NormProvider`, nur Raum ist Fake (`tests/fakes.py:106-112`). |
| E2E Real | **echter Selman-Provider** (kein expliziter Invarianten-Assert) | `tests/e2e/test_mollgasse_eg_durchstich.py:37` läuft `build_default_bundle()` auf `ArchitekturRaumProvider`; der Assert `covers_segment ⊆ segmente` wird dort NICHT wiederholt (nur Kollision/Symbolzahl). |

Konsum echt: `platzierung/deckungs_zuordnung.py:85` bindet RZ an `raum.zirkulation.segmente`.
Selman füllt `zirkulation` echt (`raumerkennung/provider.py:85,120-123`).

**🟢 grün** — Invariante wird gegen den echten Placer geprüft (4OG), und der einzige
Erzeuger von `covers_segment` (`deckungs_zuordnung`) zieht die IDs direkt aus dem
konsumierten RaumModell → strukturell nicht verletzbar. Owner: Leonis↔Selman.
Rest-Risiko (🟡-Note): auf der einzigen Real-Selman-Strecke (Mollgasse) wird der
Assert nicht wiederholt — er hängt an der Fixture-Topologie.

### (b) `norm_quelle ∈ NormRegelwerk.quellen` (Leonis ↔ Enis)

| Ort | Provider | Beleg |
|-----|----------|-------|
| Contract-Test | **Fixtures** | `tests/contract/test_platzierung_contract.py:59-65` — `platzierung_4og.json` gegen `norm_regelwerk_snapshot.json`, strikt. |
| Placer-Test | **echter Placer + FakeNorm**, mit Ausnahme-Whitelist | `tests/platzierung/test_platzierer.py:80-92` — `NotlichtPlatzierer().place(raum, FakeNormProvider())`; Assert `p.norm_quelle in quellen OR startswith(("fachpraxis:","Referenz-Praxis:"))`. |
| Enis-Seite | **echter NormProvider** | `tests/normwissen/test_sonderstellen_anforderung.py:226`, `tests/normwissen/test_norm_werte.py:102-113` prüfen, dass jede ausgegebene Norm-Quelle in `regelwerk_snapshot().quellen` liegt. |

**Kernbefund (Bruchstelle):** Der echte Placer emittiert `norm_quelle`-Werte, die
NICHT aus Enis' Regelwerk stammen:
- `fachpraxis.py:45` `QUELLE_AUFHELLER = "fachpraxis: aufheller-500mm"` (gesetzt `:225`),
- `fachpraxis.py:65` `QUELLE_TUERLEUCHTE` (gesetzt `:315`),
- `Referenz-Praxis:`-Präfix (Technik-/Müll-SL).

Die strikte Invariante würde daran brechen; sie ist per **dokumentierter Ausnahme**
entschärft (`test_platzierer.py:89`). Enis bestätigt die offene Naht selbst in
`platzierung/bausteine.py:91-97`: „die Naht-Invariante `norm_quelle ∈ quellen` lässt
die echten Fundstellen (§4.1.2 c/h/i, §4.3.8, §4.4.1) heute nicht zu; Enis liefert
Referenz-Anforderungen je Sonderstellen-Typ nach (eigener 3-Owner-PR)". Enis' Provider
mergt bereits `self._sonderstellen.quellen()` additiv rein (`normwissen/provider.py:407-409`),
aber die Leonis-Fachpraxis-Strings sind bewusst kein Norm-Wissen.

**🟡 gelb** — Invariante gegen echten Placer geprüft, ABER durch zwei Owner-Präfixe
(`fachpraxis:`, `Referenz-Praxis:`) durchlöchert; diese sind kein Norm-Audit-Trail und
haben (noch) kein eigenes `decision_source`-Feld. Solange sauber (Contract-TODO für
`decision_source`). Owner: Leonis (emittiert) ↔ Enis (Regelwerk).

### (c) `catalog_key ∈ schrack_symbol_mapping.yaml`

| Ort | Provider | Beleg |
|-----|----------|-------|
| Contract-Test | **Fixtures** (skip wenn Mapping fehlt) | `tests/contract/test_platzierung_contract.py:68-77`. |
| Placer-Test | **echter Placer** gegen echtes Mapping | `tests/platzierung/test_platzierer.py:83,93` — `keys = catalog_keys()` (echte `symbols/schrack_symbol_mapping.yaml`, 49 Keys), Assert für JEDE Platzierung. Zusätzlich `tests/platzierung/test_sichtlinie.py:86-89`. |

**🟢 grün** — stärkste der drei Nähte: gegen den echten Placer UND das echte Mapping
geprüft, ohne Ausnahme. Owner: Leonis ↔ gemeinsam (`symbols/`).

---

## 2. Von der Platzierung konsumierte RaumModell-Felder, die Selmans Provider evtl. nicht garantiert

Basis: `ArchitekturRaumProvider.parse` (`raumerkennung/provider.py:146-155`) gibt
zurück: `raeume, tueren, ausgaenge, zirkulation, stiegenhaeuser, anker`.
**NICHT** gesetzt: `sonderstellen`. Raum-Flags werden gesetzt, aber je Herkunft unterschiedlich.

| Feld | Konsument (Beleg) | Vom echten Provider gefüllt? | Ampel |
|------|-------------------|------------------------------|-------|
| `zirkulation.segmente` | `deckungs_zuordnung.py:85`, `communal_stgh_strategy.py:60`, `validierung.py:139` | Ja — `zirkulation_aus_dxf` (`provider.py:85`) + Fallback `fluchtwege()` (`provider.py:122`) | 🟢 |
| `zirkulation.nodes` | `anker_strategy.py:48,255`, `graph.build_circulation_graph` (`platzierer.py:50`) | **Nur bei 09-WEG-Plänen** — `zirkulation.py:85-89`. Fallback `fluchtwege()` liefert nur segmente, keine nodes/edges (`fluchtweg.py:168`, kein Node/Edge). Auf Mollgasse leer. | 🟡 |
| `zirkulation.edges` | `graph.py:34`, `richtungsfeld.py:66` (via `build_circulation_graph`, `platzierer.py:50`) | **Nur bei 09-WEG-Plänen** (`zirkulation.py:90-95`); Fallback-Fluchtwege füllen keine edges → auf Nicht-09-WEG-Plänen leer | 🟡 |
| `anker` | `platzierer.py:42` → `plan_rettungszeichen_anker`; `_node_positions` mischt Ausgänge dazu (`anker_strategy.py:48-49`) | Ja — direkt (`provider.py:130-145`, `anker_fuer_gang`/`baue_stiegenhaus_modell`), unabhängig von nodes/edges | 🟢 |
| `stiegenhaeuser[].verbotszonen_mm` | `verbotszonen_nachpass.py:54-60` | Teilweise — `baue_stiegenhaus_modell` (`provider.py:135`) liefert das Modell; `verbotszonen_mm` leer ⇒ Nachpass ist No-op (dokumentiert `verbotszonen_nachpass.py:15`). Ob Selman Zonen füllt = ungeprüft hier. | 🟡 |
| `nutzungsklasse` | `flaechen_strategy.py:160-163` (WOHNUNG_PRIVAT-Skip) | Ja — `wohnungen.bilde_wohnungen` (`provider.py:107`, statischer Default + Wohnungslogik `wohnungen.py:59`) | 🟢 |
| `ist_communal` | `flaechen_strategy.py:165` | Konsumiert; Füllung durch Selman im Code nicht am Provider-Top belegt (Flag-Default False) | 🟡 |
| `besondere_gefaehrdung` | `sonderstellen_strategy.py:186`, `validierung.py:338`, `pipeline.py:105` | Default False; kein Erzeuger im Provider gesehen → praktisch immer False (nur über Fixture/LB) | 🟡 |
| `ist_barrierefrei` | `sonderstellen_strategy.py:179`, `validierung.py:360`, `pipeline.py:105` | Default False; kein Provider-Erzeuger gesehen | 🟡 |
| `sonderstellen` | `sonderstellen_strategy.py:125-133`, `validierung.py:318`, `pipeline.py:104` | **NEIN** — der echte Provider setzt `sonderstellen` nie (`grep "sonderstellen=" raumerkennung/*.py` = leer). Contract-Doc sagt schon: heute nicht auto-erkennbar (`raum_modell.py:54-56`). Konsequenz: `plan_sonderstellen` läuft auf echten Plänen immer über leere Liste. | 🔴 |

**Kernbefund:** Drei Konsum-Pfade sind auf echten Plänen faktisch tot, weil Selmans
Provider die Felder nicht produziert: `sonderstellen` (nie gesetzt → 🔴), sowie die
Raum-Flags `ist_barrierefrei`/`besondere_gefaehrdung` (kein Provider-Erzeuger → default
False). `zirkulation.nodes/edges` nur auf 09-WEG-Plänen — Mollgasse & Co. fahren den
Anker-Pfad ohne Graph. Alle sind **fail-safe** (leer/No-op, kein Crash), aber die
zugehörige Norm-Logik (§4.1.2 h/i, §4.3.8, §4.4.1; graph-basierte Richtung) bleibt auf
Realdaten ungeprüft. Owner: Selman (Erzeugung) ↔ Leonis (Konsum).

---

## 3. Contract-Felder, die niemand konsumiert

Grep über `src/` (ohne `__pycache__`, Schema, Contract-Definition):

| Feld | Status | Beleg |
|------|--------|-------|
| `Tuer.tuer_detail` | Konsumiert — aber **nur Selman-intern** (nicht downstream) | `raumerkennung/ausgaenge.py:45,49`, `fluchtweg.py:229`, `wohnungen.py:73`. Kein Konsum in `platzierung/`/render. |
| `Tuer.ohne_tuerblatt` | Nur Selman-intern gesetzt, downstream **unkonsumiert** | erzeugt `tuer_zuordnung.py:156`; kein Leser in platzierung/render/validierung |
| `Raum.wohnung_id` | Nur Selman-intern gesetzt, downstream **unkonsumiert** | `wohnungen.py:111`; kein Konsum in platzierung/render/validierung |
| `zirkulation.edges` | Konsumiert (`graph.py:34` via `build_circulation_graph`) — s. Abschnitt 2, aber real oft leer | live über `platzierer.py:50` |

**Kernbefund:** `tuer_detail`, `ohne_tuerblatt`, `wohnung_id` sind reine Selman-**interne**
Zwischenergebnisse, die durch den Contract nach außen wandern, aber von keinem
Downstream-Owner (Leonis/Render/Validierung) gelesen werden. Kein toter Ballast im
Sinne von „nie gesetzt", aber Contract-Fläche ohne Cross-Owner-Konsum. Owner: gemeinsam
(Contracts) — Kandidaten für „intern vs. Contract"-Aufräumung, keine Bruchstelle.

---

## 4. Import-Grenzen (CLAUDE.md-Hard-Regel: nur `hauptengine.contracts`)

Grep aller `from notbeleuchtung.<pkg>`-Imports quer über die drei Owner-Packages:

- `platzierung/` → importiert **nur** `hauptengine.contracts` + `notbeleuchtung.symbols`
  (`bausteine.py:105-106`, `symbols/orientation.py` in `.../…:16`). `symbols/` ist
  KEIN Owner-Package (shared Infra, gemeinsam), importiert selbst kein Owner-Package
  (Grep leer) → **kein Zyklus, kein Verstoß**.
- `raumerkennung/` → `hauptengine.contracts` + `notbeleuchtung.wissen`
  (`provider.py`-Nachbarn: `.../…:25,27`). `wissen/` ist shared Infra (nur YAML-Loader),
  kein Owner-Package → **kein Verstoß**.
- `normwissen/` → **nur** `hauptengine.contracts` (Grep nach anderen Owner-Imports leer).
- Kein Owner importiert einen anderen Owner (drei gezielte Greps auf
  `platzierung`/`raumerkennung`/`normwissen` untereinander = **alle leer**).

**🟢 grün** — Import-Grenzen sauber. Die zwei Nicht-Contract-Imports (`symbols`,
`wissen`) sind gemeinsame Infrastruktur ohne Rück-Import auf Owner-Packages; sie
verletzen die „nur contracts"-Regel im Buchstaben, aber nicht im Geist (kein
Owner↔Owner-Kopplung). Owner: alle drei.

---

## 5. Wo hängt die Platzierung noch am FakeNorm statt am echten `En1838NormProvider`?

**Live gegen echten NormProvider:**
- E2E `build_fake_bundle` nutzt `En1838NormProvider` + echten `NotlichtPlatzierer`
  (`tests/fakes.py:107-112`); nur Raum ist Fake. Also läuft die **Leonis↔Enis-Naht im
  4OG-Durchstich echt** (`test_4og_durchstich.py`).
- `build_default_bundle` (`registry.py:215-241`) verdrahtet alle drei echt; Mollgasse-
  & Familien-E2E laufen darüber (`test_mollgasse_eg_durchstich.py:37`,
  `test_familien_durchstich.py:40`). Pipeline reicht den Placer-Output in `pruefbericht`
  (`pipeline.py:192`).

**Noch am FakeNorm (Unit-Ebene):** Praktisch alle `tests/platzierung/*`-Unit-Tests
übergeben `FakeNormProvider()` (Snapshot-Fixture `norm_regelwerk_snapshot.json`):
`test_anker_strategy.py`, `test_aussen_strategy.py`, `test_deckung.py`,
`test_deckungs_zuordnung.py`, `test_sonderstellen_strategy.py`, `test_gang_strategy.py`,
`test_platzierer.py:31` u.a. Das ist by-design (Owner testet gegen Nachbar-Double,
`fakes.py:44-47`).

**Was dadurch NICHT gegen echte Norm-Werte getestet ist:**
- **Sonderstellen-Anforderungen** (§4.1.2 h/i, §4.3.8, §4.4.1): der Placer-Pfad läuft
  in Unit-Tests gegen FakeNorm; auf Realdaten läuft er gar nicht, weil Selman
  `sonderstellen` nie füllt (Abschnitt 2, 🔴). Doppelte Nicht-Deckung: weder echte
  Norm-Werte noch echte Geometrie treffen diese Regeln.
- **Umschaltzeit / Track-B-Werte** (Ud, Flächen-Trigger, Umschaltzeit): `validierung.py`
  liest sie aus `regelwerk_snapshot()`; skippt, wenn Enis-Werte `None` (`validierung.py:92-103,298-300`).
  Ob echte Werte greifen, hängt an `normwissen/data/*.yaml` — nicht am Placer-Test.
- **`erkennungsweite_m` / Deckungsdichte**: FakeNorm rechnet aus Snapshot-`z`-Werten
  (`fakes.py:71-74`); die echte l=z·h-Dichte auf Realgeometrie ist nur über Mollgasse-
  Symbolzahl-Band indirekt abgesichert (`test_mollgasse_eg_durchstich.py:89-90`, weites
  Band 15..44).

**🟡 gelb** — Leonis↔Enis-Naht ist im 4OG-Durchstich echt verdrahtet (kein FakeNorm im
E2E). Aber die norm-anspruchsvollen Regeln (Sonderstellen, Track-B-Schwellen) sind auf
Unit-FakeNorm beschränkt und/oder durch Selmans fehlende Feld-Erzeugung (`sonderstellen`)
auf Realdaten überhaupt nicht ausgeübt. Owner: Leonis (Placer-Tests) ↔ Enis (Werte) ↔
Selman (`sonderstellen`-Erzeugung).

---

## Zusammenfassung / Ampeln

| Naht | Ampel | Kernbefund | Owner | Beleg |
|------|-------|-----------|-------|-------|
| (a) covers_segment | 🟢 | Gegen echten Placer geprüft; IDs strukturell aus konsumiertem Raum | Leonis↔Selman | `test_platzierung_contract.py:49`, `test_4og_durchstich.py:33`, `deckungs_zuordnung.py:85` |
| (b) norm_quelle | 🟡 | Invariante durch Owner-Präfixe `fachpraxis:`/`Referenz-Praxis:` durchlöchert (kein Norm-Trail, kein `decision_source`-Feld) | Leonis↔Enis | `test_platzierer.py:89-90`, `fachpraxis.py:45,65`, `bausteine.py:91-97` |
| (c) catalog_key | 🟢 | Gegen echten Placer + echtes Mapping, ohne Ausnahme | Leonis↔gemeinsam | `test_platzierer.py:93` |
| Feld `sonderstellen` | 🔴 | Von Leonis konsumiert, von Selmans Provider NIE gesetzt → tot auf Realdaten | Selman↔Leonis | `provider.py` (kein `sonderstellen=`), `sonderstellen_strategy.py:125` |
| Felder nodes/edges | 🟡 | Nur auf 09-WEG-Plänen gefüllt; Fallback-Fluchtwege liefern keine → Mollgasse leer | Selman↔Leonis | `zirkulation.py:85-95`, `fluchtweg.py:168` |
| Felder Flags (barrierefrei/gefährdung) | 🟡 | Konsumiert, kein Provider-Erzeuger → default False auf Realdaten | Selman↔Leonis | `sonderstellen_strategy.py:179,186` |
| Import-Grenzen | 🟢 | Sauber; `symbols`/`wissen` = shared, kein Owner↔Owner | alle | Greps leer |
| Unkonsumierte Contract-Fläche | 🟡 | `tuer_detail`/`ohne_tuerblatt`/`wohnung_id` nur Selman-intern | gemeinsam | s. Abschnitt 3 |
| FakeNorm-Abhängigkeit | 🟡 | Leonis↔Enis im 4OG-E2E echt; Sonderstellen/Track-B nur Unit-FakeNorm | Leonis↔Enis↔Selman | `fakes.py:107`, `test_platzierer.py:31` |

## Unbelegt
- Ob Selmans Provider `verbotszonen_mm` / `ist_communal` / `ist_barrierefrei` in
  bestimmten Kaskaden-Pfaden doch füllt, wurde nicht bis in jeden Kaskaden-Zweig
  verfolgt (nur `provider.py`-Top + direkte Erzeuger geprüft). Für `sonderstellen`
  ist die Aussage belegt (Grep `sonderstellen=` in `raumerkennung/*.py` leer).
