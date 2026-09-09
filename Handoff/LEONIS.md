# Handoff — Leonis (Platzierung + Integration)

> Claude: Du bist die Session von **Leonis**. Owner-Package:
> `src/notbeleuchtung/platzierung/`. GitHub `@mvpo3`. Task: **Issue #2**.
> Du hast als Einziger elektro-planer-Zugriff → du stagst Port-Material für andere.

## STAND (2026-09-10) — MULTI-SLICE Wissens-/Normabgleich, Phase 3 LÄUFT (Branch `leonis/wissensabgleich-engine`)

**AKTIVE AUFGABE. Hier weitermachen.** Owner-Task: Wissens-/Normabgleich + Verbesserung
Platzierungslogik & Lichtberechnung. Multi-Phasen mit STOP-Gates. Branch
`leonis/wissensabgleich-engine`, basiert auf main `fd65839`. **Noch NICHTS gepusht.**

**Bindende Regeln (Owner):** Scope FIX_SRC/FIX_YAML/FIX_CONTRACTS/FIX_FIXTURES = JA.
Contract-Touch → `contract_version`-Bump + `scripts/gen_schema.py` + Protokoll in
`docs/audit/HANDOFF_B_ENIS.md` (Protokoll, KEINE Freigabe-Anfrage). Je Fix: 3–8 Z. Pseudocode +
Dateiliste VOR Code · ein Fix = ein Commit (em-dash, Fix-ID im Betreff) · ein Test mit EXAKTER
Assertion (keine Toleranz) · neue Regeln über NormProvider-Lookup, nicht als Konstante · nach
jedem Fix `pytest -q` + `ruff check .` grün, sonst Fix zurücknehmen statt Test anpassen.
**STOP-Gates nur drei:** nach Phase 0 · nach Phase 2 (beide passiert) · **vor Push/Merge** (da
stehe ich bald). Dazwischen durchziehen. **Push/PR/Merge nur auf explizites Owner-GO.**

**Noch bindende Prompt-Regeln (v.a. Block 3):**
- **Entscheidungs-Hierarchie:** LB-explizit → Referenz-Praxis → EN-1838/ÖNorm-Default → OVE-Verbote
  (Hard Stop). LB übersteuert Norm-Default. Audit-Trail: `norm_quelle`/`lb_quelle`.
- **Geltungs-Regel (je Befund GENAU EIN Tag):** `[AT-verbindlich]` (OVE E 8101:2025 · ÖNORM EN 1838) /
  `[AT-Referenzpraxis]` / `[DE-only]`. **Ohne Tag ist der Befund ungültig.** DE-only wird NIE Default,
  nur Referenz-Praxis-Fallback (z.B. F11 60/8 m², F13, F14).
- **Beleg-Regel:** jeder Befund/Fix braucht `datei.py:zeile`, `Plan X, S.n` oder Regel-ID; sonst in
  Abschnitt „Unbelegt". Bei Fremdmaterial P1 zitieren, NICHT ins Repo kopieren.
- **Inputs:** P1 = `"DIN-Notbeleuchtungspläne(Beispiele)"` (Fremd, DIN/DE — nur lesen/zitieren; Pfade
  mit Klammern+Umlauten in der Shell QUOTEN). P2 = `knowledge/`. P3 = Repo (main-Stand).
- **Am STOP liefern:** Commit-Liste + Sichtprüfungs-Abweichungen (`docs/audit/07_sichtpruefung.md`).

**Audit liegt in `docs/audit/`** (untracked, auf Platte): `REPORT.md`, `FIX_PLAN.md`,
`01_plan_forensik/02_wissens_coverage/03_engine_ist/05_widersprueche/06_naht_owner_matrix.md`.
`FIX_PLAN.md` = die Fix-Liste F01–F18 + mein Vote. **Zugesagt: Block 1+2+3 (F01–F14). Block 4
(F15–F18) = Handoff, NICHT bauen.**

**COMMITS auf dem Branch (git log):**
- `238d0d1` F04 — Redundanz-Reichweite aus `norm.erkennungsweite_m` statt Konstante (W08)
- `9c277a3` F03 — Pfeil-Rotation `bausteine.rotation_zur_tuer` (4× Dup → 1) (W16)
- `0c37b90` F01 — Wartungsfaktor im Lux-Nachweis-Bericht aus EINER Quelle, 0,80 nicht hart (W09)
- `cec7d05` F02 — Wartungsfaktor `lux.wartungsfaktor_aus_norm` (5× getattr → 1 Helper) (W09)
- `72662f5` **W-LIB** (Extra-Fund) — `symbols/library.py` Normalisierungs-Cache per Doc-Objekt
  (`WeakKeyDictionary`) statt `id(doc)`. **Root Cause eines Ordering-Flakes** (render/test_pfeilrichtung
  kippte je nach Suite-Ordering) **+ echter Batch-Render-Bug** (id()-Reuse nach GC → un-zentrierte
  Blöcke). Ohne den Fix ist der Vollauf ordnungsabhängig rot. Regression: `tests/render/test_library_cache.py`.
- `23e3918` F05 — Toiletten-Scope §4.3.8 aus EINER Quelle `bausteine.TOILETTE_EINDEUTIG/_MEHRDEUTIG`
  (vorher 3× hart in sonderstellen_strategy + validierung) (W10)
- `db8cac3` docs — dieser Handoff-STAND
- `859bfdc` F06 — getrennter Kreis Warnung→**fehler** (Hard-Stop, W13). **BLOCK 1 KOMPLETT.**

**Voller `pytest` zuletzt GRÜN: 1026 passed, 36 skipped** (nach Lib-Fix deterministisch). ruff clean.

**NÄCHSTE SCHRITTE (in Reihenfolge):**
1. ~~F06 committen~~ ✅ erledigt (`859bfdc`). **Block 1 = F01–F06 + W-LIB fertig.**
2. **Block 2 (HIER WEITER):** **F08** (erkennungsweite_m im `place()`-Pfad verdrahten ODER sichtlinie-Pfad
   `plan_rettungszeichen_sichtlinie` als deaktiviert dokumentieren — er ist test-only, nicht im
   place-Pfad; W17, Dep F03) → **F07** (≥2-Leuchten-Redundanz-Garantie je Abschnitt + Prüf-Hard-Fail;
   W19, Dep F04, **Verhaltensänderung = dichter → E2E-Sichtprüfung nötig**). Dateien: platzierer.py/
   anker_strategy.py bzw. deckung.py/validierung.py.
3. **Block 3 (🟨, berührt `normwissen/data` → HANDOFF_B_ENIS.md protokollieren):** **F09** Wartungsfaktor
   innen 0,80 [AT-verbindlich] / außen 0,57 [AT-Referenzpraxis] — **Contract-Feld
   `NormAnforderung.wartungsfaktor` ergänzen (norm_regelwerk.py, CONTRACT_VERSION 1.2.0→bump) +
   `gen_schema.py` + YAML füllen + provider.py liest es**. F02 hat den Konsum-Hook schon gelegt
   (`lux.wartungsfaktor_aus_norm`) → F09 füllt nur die Quelle, dann greift 0,80 überall gleichzeitig.
   **ACHTUNG Golden-Shift:** 0,80 < 1,0 → dichtere SL-Platzierung → E2E-Symbolzahlen ändern sich →
   Golden bewusst nachziehen (inhaltlich nötig, norm-korrekt) + voller pytest. Dann **F11** (Antipanik-
   Trigger 60/8 m² als Referenz-Praxis in `ove_e8101_zusatz.yaml`, OVE-scope-gated), **F12**
   (seitenselektiver Randbereich), **F13** (Stiege podest-gestaffelte Höhe), **F14** (grün=RZ/gelb=SL
   Layer). **F10 (Blendungsgrenzen f(h)) HÄNGT an Enis' cd-Werten → wird Handoff, nicht Fix.**
4. **Phase 4 Verify:** `.venv/Scripts/python.exe -m pytest -q` (voll, ~8 min) · `gen_schema.py` (falls
   Contract) · `ruff check .` · E2E: neues DXF rendern vs. 4OG-GU-PDF → **`docs/audit/07_sichtpruefung.md`**
   (Abweichungen dokumentieren).
5. **STOP vor Push.** Commit-Liste + Sichtprüfungs-Abweichungen an Owner. **Push/PR/Merge nur auf GO.**

**FALLEN / gelernt in dieser Session:**
- **Voller `pytest` ~8 min** — nur an Verhaltens-Fixes (F07/F09) + einmal in Phase 4 nötig, sonst
  targeted. Läuft via `run_in_background`, Notification abwarten (nicht pollen).
- **`git commit` Heredoc scheiterte in PS** → Message in scratchpad-Datei + `git commit -F`.
- **NIE `git add -A`** (zieht scratchpad/.bak/Zips rein). Nur die Fix-Dateien einzeln stagen.
  `docs/audit/` ist noch untracked (bewusst; am Ende committen oder Owner fragen).
- **W-LIB-Lektion:** Wenn ein Render-/Symbol-Test ordnungsabhängig kippt, Verdacht `id()`-gekeyter
  Cache in `symbols/library.py` (jetzt gefixt). platzierung+render-Kombo war der schnelle Repro.
- **Naht-Grenzen (aus Audit):** `sonderstellen.raumtyp_scope`/YAML-Vokabular liegt am konkreten
  `OveZusatzKatalog`, NICHT am 4-Methoden-Port `NormProvider` (ports.py:43). Consumer an die YAML zu
  hängen braucht neue Port-Methode = contracts/** = 3-Owner → F15/F16-Handoff. `norm_quelle`-Praxis-
  Präfixe brechen die Naht-Invariante → decision_source-Contract = F15.

## STAND (2026-09-08, Session-Ende F1 SPÄT) — Master-Plan durch, Skills/Tools, #129-Salvage, Demo

**origin/main ≈ `97a5f3a`.** Kompletter Master-Plan (plan-Datei `.claude/plans/deep-strolling-naur.md`)
abgearbeitet + Tooling. Alles gemergt außer den Vorschlägen unten. Suite grün, ruff clean.

**Heute auf main gebracht:**
- **6-Branch-Stack + Rotations-Fork** gemergt (#132 ausgabeluecken · #133 slice-4.1 · **#134
  slice-3.1 = Fork-Sieger, orientation.py Ein-Rahmen kanonisch** · #135 slice-2.3 fachpraxis ·
  #136 slice-3.4 layout · #137 tuerleuchte). „ZIP-Landmine" war Phantom (Rebase zog main's ZIP).
- **3 Konsum-Slices:** #138 `lux.py` Extents-Cap (8 Mio) · #139 `verbotszonen_nachpass` (S1) ·
  #140 `flaechen_strategy` WOHNUNG_PRIVAT-Skip (S2).
- **Türleuchten-KORREKTUR #141** (Owner): TECHNIK/MUELL/KINDERWAGEN → **RZ an der Tür** (Pfeil
  zur Tür) statt SL; mittige Zusatzleuchte NUR wenn groß/L-Form (Aufheller <60 m² / Antipanik ≥60).
- **Skills (Projekt, `.claude/skills/`, via Sync bei allen 3):** `plan-verify` (generieren+prüfen),
  `sync-review` (Fremd-PR-Review), `wissen` (Second-Brain, Norm nur zitieren nie umschreiben).
  **Tools:** `scripts/dxf_healthcheck.py` (Eingabe-DXF-Gesundheit, kapselt 4OG-Diagnose),
  `scripts/wissen_index.py` (+`knowledge/INDEX.md`), `scripts/norm_coverage.py` (Wissens-Konsum
  je Plan: norm/praxis/unbegruendet). Alle mit Tests, ruff clean.
- **Enis L1/L3** 2× Windows-gegengeprüft (`19c987d`→Issue #131; **`0b66485` rebased → „zur
  Übernahme empfohlen"**, 101 passed, T1/L2 separat).

**OFFEN für nächste Session (nichts blockierter Leonis-Code):**
1. **#146 = Salvage von Selmans #129** (`selman/grundstuecksgrenze-hof-neu`): aktuelles main +
   Contract v1.3.0 (`Tuer.quelle`/`untypisiert_grund`) + Selmans raumerkennung, **Rotations-Teil
   gedroppt** (durch 3.1 ersetzt), Ruff gefixt. 1044+7 grün, schema in sync. **Contract=3-Owner →
   Enis+Selman-Approval, nicht einseitig mergen.** Kommentar auf #129 zeigt auf #146; Selman muss
   raumerkennung fachlich abnehmen + ggf. #129 schließen.
2. **Baufeld 4OG** = Koordinaten-Versatz (61 % Entities bei y≈347.535 km, `dxf_healthcheck`
   flaggt NO-GO). Fix = User-AutoCAD-`MOVE`/`PURGE` ODER Selman `rest_komponenten` ausreißer-robust
   (`_geschoss_extents`-Muster). 7/8 Geschosse sauber + renderbar (`scripts/projekt_batch_worker.py`
   im OWNER-Terminal via `!` — Hintergrund-Renders werden hier gekillt).
3. **Demo-/Grundriss-Lektion** (Owner-Feedback, Memory `demo-grundriss-grenze.md`): synthetische
   Grundrisse selbst zeichnen ist schwach (Stiegenhaus MUSS an den Gang = Fluchtziel!). Für echte
   Pläne realen Architektur-DXF nutzen. **Lichtberechnung = `render/lux_nachweis_bericht.
   schreibe_bericht`** (NICHT `render_dxf`; `pipeline.run` ruft es auto — bei place()+render_dxf
   selbst aufrufen). Demo-Skripte `scratchpad/demo_l/gen3.py`+`render3.py`.
4. **Türleuchte-Detail offen:** B1-Aufheller hinter dem Tür-RZ behalten oder ausnehmen (Owner).
5. **Phase 6:** `decision_source`-Contract (3-Owner), A1-Format.

---

## STAND (2026-09-08, Session-Ende F2) — Lichtberechnung IN der Hauptengine + Platzierungs-Fixes

**origin/main = `f6a753b`.** Alles gepusht/gemergt, `leonis/f2-work` == main. F2-Worktree
war Arbeitsort; **F1 zieht `git pull` und hat das volle Paket.** Kein Contract-Touch,
ganze Suite grün (contract 53 · platzierung 253 · normwissen/naht/hauptengine 395 · e2e 24),
ruff clean, kein Schema-Drift.

**Was neu auf main ist (diese Session):**
1. **Lichtberechnung IN der Hauptengine** (Owner-Wunsch „immer je Plan"): neues
   `hauptengine/render/lux_nachweis_bericht.py::schreibe_bericht` — DIALux-artige Rivoplan-
   Nachweis-Seite aus dem FERTIGEN `PlatzierungsErgebnis` (Falschfarben-Feld + EN-1838-
   Nachweis + polare LVK + Logo, robust bei vielen Fluchtwegen). Verdrahtet: `pipeline.
   _run_mit_quelle` schreibt `<out>.nachweis.png` + `render_summary["lux_nachweis"]`
   (try/except, nie plan-brechend); `projekt._merge_pdf` hängt die Seite je Geschoss ins
   Sammel-PDF. **Test:** `run_projekt(..., pdf=True)` → PDF = Plan-Seite + Nachweis-Seite je
   Geschoss (end-to-end auf Mollgasse EG verifiziert). `scripts/lux_nachweis_bericht.py` = CLI.
2. **Aufheller lux-bedingt** (`fachpraxis.aufheller_je_rz` +norm/+i_cd_fn): setzt Aufheller
   nur wo E < min_lux — nur mit echter Photometrie (ohne LDT bedingungslos). Antipanik+
   Fluchtweg waren schon lux-getrieben.
3. **Deckungs-Fix** (`abstand_nachpass`): SL-Dublette (<2 m) wird nur noch im GLEICHEN Raum
   gemergt — vorher verlor ein Korridor seine einzige Fluchtweg-SL an den Nachbarn → dunkel
   (Mollgasse raum_34). Jetzt kein Korridor mehr ohne SL (9/12→10/12). + Perf-Guard.
4. **Wissen:** `knowledge/extracted/LICHTBERECHNUNG_REFERENZ.md` (3 echte Profi-Reports:
   MF 0,80/0,57, ohne Reflexion, Mittellinie≥1+Mittelfläche≥0,5, Ud≥1:40). Wartungsfaktor-
   Mechanismus liegt **inert** in `lux.py`/`deckung.py` (Default 1,0).

**Offene Nähte (keine Bugs — „loose ends"):** ① **Enis:** Feld `NormAnforderung.wartungsfaktor`
+ Werte 0,80/0,57 füllen → dann rechnet die Engine wie die Profis (bis dahin Bericht zeigt MF,
Rechnung ignoriert ihn). ② **Selman:** 2 Mollgasse-Korridore (raum_41/55) = 494-Punkt-Spikey-
Polygone → Mittellinie in Zacken → Nachweis scheitert (Erkennungs-Sache). ③ **Testschuld
(Leonis):** Bericht hat nur Smoke-Test, kein Inhalts-Test; reimplementiert `_rw_stats` statt
`lux_nachweis.nachweis_fluchtweg`; Asset-Pfade repo-relativ (pip-Paket fände Logo/LDT nicht).
④ Alte Backlog-Branches sind stale/Fork-blockiert (`git cherry` geprüft) — **nichts zu mergen.**

## STAND (2026-09-07, GANZ SPÄT/Session-Ende 3) — Enis-L1/L3-Review + Selman-Antwort

**Enis' gemeinsame L1/L3-Fassung reviewt** (Commit `8801aa6`, Branch
`enis/l1-l3-gemeinsam-0907`, Basis meine `bf1f965`). Bundle kam als
`Documents/enis-l1-l3-8801aa6.bundle`. **Verdikt: „Vor Übernahme 1 Fix nötig".**
- **Bestätigt (alles gut):** L1/AStV (`oib_gate.py` byte-identisch), Datenweg
  validierung→pruefung→Renderer (erweitert um `oib_lage`: unterscheidet kein-
  ProjektKontext / kein-OIB / Befund-ohne-Gebäudeteile), `review_required`→
  UNGEKLÄRT, Vorbehalt „Erforderlichkeit, keine Konformitätsaussage", Kürzung hält
  UNGEKLÄRT+Anzahl+„Zusammenfassung", kein Berichts-Verweis, **Platzierungen
  UNVERÄNDERT** (`platzierung/` komplett unangetastet). 168 passed.
- **BLOCKER (bei Enis):** `dxf_renderer.py` `_VERMERK_EINHEIT_JE_ZEICHEN=0.96`
  **unterschätzt** die echte Breite (ezdxf `text_size` misst hier ~1,29/Zeichen)
  → sein Guard `test_zeichenbreite_stimmt_mit_der_gemessenen_breite` ist ROT
  (77-Zeichen-Zeile: 73,92 geschätzt vs 99,13 gemessen). Fix-Empfehlung: Breite im
  Render direkt mit `text_size` MESSEN statt fester Faktor (umgebungsunabhängig).
  **Prompt an Enis raus.** Bei Nachlieferung (Push/Bundle) = 2-Minuten-Recheck (nur
  der eine Test), dann „zur Übernahme empfohlen".
- **Review-Technik gelernt:** geteilter venv-Editable-Install überschattet einen
  Worktree (Import kam aus main-src trotz PYTHONPATH — PEP-660-Meta-Finder). Lösung:
  `pip install -e <worktree> --no-deps` temporär, testen, `pip install -e <main>`
  restaurieren. Worktree via `git worktree add <dir> <sha>` (detached), danach
  `git worktree remove --force`. Alles restauriert, meine Branches unversehrt;
  `enis/l1-l3-gemeinsam-0907` liegt lokal als Referenz (nicht von mir gepusht).

**Selman-Frage (Foto): Überdachung vor Haupt-Ein/Ausgang für Außen-Aufheller.**
Meine Antwort: **Feld `Ausgang.ueberdacht` NICHT bauen.** `aussen_strategy.
plan_aussenleuchten` setzt die SL 1 m vor JEDEN final_exit **bedingungslos** — sie
liest keine Überdachungs-Info, der Contract hat kein solches Feld. Ein Fund
(Barawitzka 0,707 m²) ist zu dünn für 3-Owner. Als Prüfstrecken-Befund stehen
lassen; bei echter Norm-/Praxis-Regel später wieder aufgreifen. (Owner: keine
COORDINATION-Notiz nötig.)

## STAND (2026-09-07, SPÄT/Session-Ende 2) — ALLES GEPUSHT + neue Owner-Regeln + Baufeld-Assets

**main = origin (synchron). ALLE Leonis-Branches sind auf GitHub gepusht** (Owner-GO
„pushe alles"). Nichts gemergt außer #127. Reihenfolge/Reviews stehen aus.

**Branches auf origin (ungemergt, warten auf Owner-Review/PRs):**
- **MEGA-Stack** (gestapelt main→4.1→3.1→2.3→3.4): `slice-4.1-mollgasse-ug-referenz`
  · `slice-3.1-pfeilrichtung` · `slice-2.3-fachpraxis-tuer-aufheller` ·
  `slice-3.4-layout-vorlage-1-50`. Inhalt siehe `reports/mega_run_2026-09-07.md`.
- `leonis/ausgabeluecken-oib-astv` (`bf1f965`): AStV-Hinweise + OIB-Stufe erreichen
  die Ausgabe (L1/L3-Fixes für Enis) + Blatt-Worst-Case-Test. **Enis holt via
  `git fetch origin leonis/ausgabeluecken-oib-astv`** (Bundle war gestern der Notweg,
  jetzt obsolet).
- `leonis/tuerleuchte-technik-muell` (`acf9896`): **NEUE Owner-Regeln** — TECHNIK/
  MUELLRAUM/KINDERWAGENRAUM bekommen eine **Antipanik-Sicherheitsleuchte an der Tür**
  (Symbol `antipanik_leuchte` = din-AP3-Universalleuchte, kind=sicherheitsleuchte,
  Rolle≠Produkt). „immer" = Referenz-Praxis (SL-13 + INOTEC HB2026 5lx + EN 1838:2025
  §5.4 + LB §5.1.23; norm-seitig KEINE Pflicht — Web+Knowledge recherchiert).
  **Bewusst NUR KINDERWAGENRAUM, nicht ABSTELLRAUM** (gemeinsamer ≠ privater Raum).
- `leonis/gang-pfeil-zur-tuer-wip` = **PR #128** (offen, CI grün, wartet auf Merge-GO).

**Ultracode-Review** (heute) aller Tagesarbeit: 0 Blocker, 3 Quality-Befunde gefixt
(fachpraxis fail-closed · analyse crops verdrahtet · Blatt-Banden-Worst-Case-Test).
3.1-Rotationsrahmen numerisch als korrekt bestätigt, Ausgabelücken als output-only
verifiziert. Details: die 3 Fix-Commits auf den jeweiligen Branches.

**Baufeld-E2-Pläne ERNEUERT vom Owner + auf main gepusht** (`b1f27ed`): zwei Zips in
`Projekte/` (DXF-only, ohne .bak, je 48 MB — Zip-Muster wegen GitHub-100-MB-Limit):
`Baufeld_E2.zip` (leere Architekturpläne = Selman-Input, 8 Geschosse, ersetzt alt) +
`Baufeld_E2_Notbeleuchtungsplaene.zip` (Soll/Referenz, neu). Entpacken nach
`Projekte/Baufeld E2/` bzw. `Projekte/Baufeld E2 Notbeleuchtungspläne/`. **OB die
neuen DXF den 347-km-Extents-Ausreißer (Batch-Blocker!) noch haben, ist UNGEPRÜFT** —
morgen zuerst `ArchitekturRaumProvider().parse` auf 4OG testen, bevor Batch neu läuft.

**OFFEN für nächste Session:**
1. **PRs für die 6 Branches anlegen** (Stack-Reihenfolge!) + #128 mergen — Owner-GO.
2. **Selman-Nähte** (in docs/COORDINATION.md 2026-09-07 protokolliert): (a) Baufeld-
   Extents-Ausreißer (347 km → TiB-Crash) — jetzt mit NEUEN Plänen re-testen; (b)
   Kinderwagenraum-Typ geht in raumtyp.py verloren (`kinderwagen→ABSTELLRAUM`) → die
   Türleuchten-Regel greift auf echten Plänen erst, wenn Selman `KINDERWAGENRAUM` als
   Typ erhält (evtl. VOKABULAR-Ergänzung, 3-Owner).
3. **Enis-Naht:** Türleuchten-Regel liegt inhaltlich in seiner normwissen-Lane (SL-13,
   dort LB-explizit) — sauberer über NormProvider statt in platzierung/fachpraxis.py.
4. **Baufeld-Batch** 1OG/3OG/4OG/6OG neu fahren, sobald Extents geklärt (UG/EG/5OG
   waren geliefert, aber gegen die ALTEN Pläne).
5. Offene Detailfrage Türleuchte: eine Leuchte an der Tür genügt, oder 5 lx
   ganzflächig (Technik, INOTEC/EN §5.4)?

## STAND (2026-09-07, Session-Ende) — Sync + #127 + MEGA-Run (4 Slices auf Branches)

**main lokal = origin + cbad667 (COORDINATION, UNGEPUSHT — Owner-GO zum Push holen).**

**Erledigt heute:**
1. **Sync:** Selman pushte 7 Commits direkt auf main — Fachteile 1–3 (Tür-Zuordnung/
   Typisierung, Lift/Stiegenhaus/Anker/Verbotszonen, Prüfstrecke 05/06) inkl.
   **RaumModell v1.2.0** (additiv: `tuer_detail`, Segment-`quelle/ziel_ausgang`,
   `Anker.fluchtrichtung_grad`, `StiegenhausModell.verbotszonen_mm`). Suite 896 grün
   (+2 XPASS s.u.).
2. **#127 GEMERGT** (Owner-GO; vorher Ruff-Fix am Batch-Worker — CI-Lint war rot).
3. **PR #128 offen, CI grün, Owner sagte WARTEN** (Pfeil-zur-Tür im GANG-Fallback +
   Baufeld-Soll-xfails entstrickt — die kippen lokal als XPASS(strict), weil Selmans
   Erkennung am Baufeld jetzt Ausgänge+Segmente liefert).
4. **5OG-Reklamation FAKTISCH GELÖST durch Selmans Naht:** 5OG läuft im Anker-Pfad
   (689/689 Türen mit von/nach_raum, 262 Segmente) → 12 RZ rotationsrichtig, ok.
5. **Baufeld-Batch:** 5OG geliefert (DXF+PDF, %%EOF ok; UG/EG von gestern).
   **1OG/3OG/4OG/6OG BLOCKIERT:** Quell-Pläne tragen Hauptinhalt bei y≈347.535 km
   (Basispunkt-Versatz!) → `stempel_flutung.py:227` will 2,56-TiB-Raster (4OG fatal),
   `rest_komponenten` fängt es (1OG), aber **`place` mahlt am 1OG >50 min** (Phantom-
   Extents im Lux/Raster-Pfad = auch Leonis-Robustheits-Kandidat!). Befund an
   @polatselman in docs/COORDINATION.md (Log 2026-09-07). Ops: Baufeld NIE parallel
   rendern (RAM); >10-min-Renders via Monitor-Tool als Langläufer.
6. **MEGA-Prompt (Owner: „wörtlich alle 4"), alle 4 Slices fertig, gestapelt,
   UNGEPUSHT** (Vorgabe: kein Push/Merge/PR — Owner reviewt je Slice):
   `slice-4.1-mollgasse-ug-referenz` (2e24832: GU-Plan-Referenz 1KG 11 RZ / 2KG
   30 RZ+2 SL, Fixtures + docs/analyse/, kein Aufheller-Typ im GU-Plan!) →
   `slice-3.1-pfeilrichtung` (1ab3b63: symbols/orientation.py = EIN Rotations-
   rahmen; Befund „oben rendert rechts" gefixt; rechts-Block ist echter X-Spiegel
   — PORT_LOG stimmt) → `slice-2.3-fachpraxis…` (754145a: **G3 = Tür-RZ-links-Regel
   nach Messung VERWORFEN** (Owner in-Session), **G4 = Aufheller B1 auf Owner-Wort
   GEBAUT**: je RZ ein Aufheller 500 mm Richtung Rauminneres, `fachpraxis.py`,
   norm_quelle-Präfix `fachpraxis:`) → `slice-3.4-layout-vorlage-1-50` (995f5c7:
   opt-in `template_path`, Layout1-Viewport exakt 1:50, G5/G6 als Fehlerklassen;
   Vorlage hat KEINE ATTRIBs). Report: `reports/mega_run_2026-09-07.md` (gitignored).
   Suite auf 3.4-Spitze: **952 grün**, ruff clean.

**OFFEN für morgen:** ① Owner-Review der 4 Slice-Branches (Reihenfolge!) + #128 ·
② cbad667 + Handoff-Commit pushen (GO) · ③ Baufeld-Rest nach Selmans Extents-Fix ·
④ A1 weiter offen · ⑤ Leonis-Kandidaten: Verbotszonen-Konsum (`stiegenhaeuser[].
verbotszonen_mm`, Selman-Zuruf in docs/OFFENE_FRAGEN.md — Leuchten auf Treppenläufen!)
+ `nutzungsklasse`-Konsum (4 Leuchten in WOHNUNG_PRIVAT) + place-Robustheit gegen
Phantom-Extents · ⑥ handoff(contracts): `decision_source`-Feld (3-Owner).

## STAND (2026-09-06, Session-Ende ~22:30) — MORGEN HIER WEITER

**Tagesbilanz: 11 Merges (#116–#126), 738→853 grün.** Abend-Session drehte sich
um Output-Qualität auf schweren Fremdplänen (Rennweg committet, Baufeld E2).

**OFFENE FÄDEN für morgen (Reihenfolge):**
1. **PR #127 mergen** (2 Commits: Unterlage nur sichtbare Layer — Baufeld hatte
   95 % Entities auf frozen/off! · Continuous-Linetype-Zwang — Strichlinien ×
   Millionen-mm-Koordinaten ließen matplotlib >10 min hängen, mit Fix 37 s).
   CI von Commit 2 noch prüfen (`gh pr checks 127`), dann Owner-GO.
2. **WIP-Branch `leonis/gang-pfeil-zur-tuer-wip`** (auf #127 gestackt):
   Owner-Reklamation Baufeld-5OG — alle 18 RZ rotation=0, Pfeil-zur-Tür-Regel
   (#111) lebte nur im Anker-Pfad, Fremdfamilien laufen im GANG-Fallback.
   Fix gebaut (Ziel-Tür je Gang: Notausgang>Stiegenhaus; Punkte zum Ziel
   geordnet; letztes RZ unten-Block rotiert zur Tür), 177 Tests grün — ABER am
   5OG wirkungslos (weiter 0°). **Diagnose offen:** tragen Baufeld-Türen
   von_raum/nach_raum? (Skript stand, Owner brach für Feierabend ab.) Falls
   Referenzen fehlen → Geometrie-Fallback (Tür am Gang-Polygon-Rand) oder
   Selman-Naht.
3. **Baufeld-E2-Batch fortsetzen:** fertig+verifiziert nur UG+EG (DXF+PDF in
   output/, Integritäts-Check!). Werkzeug jetzt versioniert:
   `scripts/projekt_batch_worker.py <FLOOR...>` (Scratchpad-Lektion). Rest:
   1OG–6OG. **Vor Versand IMMER PDF-Integrität prüfen (%%EOF)** — heute ging
   eine Abbruch-Leiche an den Owner raus.
4. **A1-Format:** Owner-Antwort offen (A1-Probe von EG geschickt; wenn GO →
   alle Groß-Projekte A1 + evtl. Default je Plangröße).
5. **Selman baut die Nahttests** (Owner-Ansage!): Regel-Deckungs-Guard +
   Soll-Tests je Familie — NICHT Leonis-Aufgabe, aber Reviews erwartbar.
   Kontext: main..origin nach seinen Pushes checken.

**Neue Erkenntnisse/Fallen heute Abend (Merke!):**
- Sandbox killt parallele Hintergrund-Prozessgruppen (`&`+`wait`) — Einzel-
  prozesse via run_in_background überleben; Parallelität nur über getrennte
  Task-Aufrufe.
- matplotlib-PDF-Killer war NICHT Entity-Menge (26k rekursiv = harmlos),
  sondern **Strichlinien-Linetypes** bei Millionen-Koordinaten (Bisection-
  bewiesen). ADR-würdig, steckt im #127-Commit-Text.
- din-Produkte: AP3-LDT NICHT öffentlich → Owner-Anfrage (QUELLEN.md).
- Enis' 5-Punkte-Photometrie-Paket: Leonis-Positionen beim Owner (Memory),
  wartet auf Enis' nächsten Schritt.

## STAND (2026-09-06, Spätnacht) — #122–#126 GEMERGT: Unterlage, Kontext, Vokabular

**main = #126-Merge, 853 grün.** Nach #121 kamen FÜNF weitere Merges:
- **#122** Spot-Symbol (din STANDARD_SPOT geometrietreu nachgebaut, Owner nahm
  es sofort in seine Vorlage-v2 auf!) + Engine-Nachzug auf die Owner-Vorlage v2
  (Spalte x 2086..2291, Planfenster=VIEWPORT → Engine zeichnet Rahmen selbst,
  Owner-INSERTs in Legende werden mitkopiert, Prüfvermerk-Bande 596..614,5).
  Wohnbau-Fixture fing den Vorlagen-Umbau sofort (4 rote Tests) — Zweck erfüllt.
- **#123** Architektur-Slice platzierung/: `bausteine.py` (verkappte Common-Lib
  entwirrt, wortgleich) + `PlatzierungsKontext` (Schluss mit Parameter-Fädelei;
  Enis' nächste Nähte = 1 Feld). Mollgasse bit-identisch.
- **#124** `docs/VOKABULAR.md` (kanonische 19 Raumtypen + Naht-Glossar, Doku-
  Drift-Guard `test_vokabular_doku.py`) + `docs/adr/` (6 Bindend-Entscheidungen).
  Idee aus mattpocock/skills domain-modeling adaptiert; Rest der Suite verworfen.
- **#125** **PDF-Default WEISS** (Owner-Regel; dunkel bleibt Option, Goldens hell).
- **#126** **Architektur-Unterlage**: Original-Linienwerk (ezdxf-Importer inkl.
  Blöcke, ohne Text/Bemaßung/HATCH) als graue Layer unterm Grün; Skala-Erkennung
  1/10/25,4/1000; fail-open; Pipeline hält DWG-Konvertat bis Render. PLUS
  `_geschoss_extents` Ausreißer-robust: Rennweg-Erkennung liefert Phantom-Raum
  am Quell-Plankopf (755 m Spannweite!) → Fenster clustert um größten Raum
  (@polatselman gemeldet). Rennweg 8/8 verifiziert — sieht jetzt aus wie ein
  echter Montageplan.
- **Assets:** Rennweg 15 alle 8 Geschosse committet (`Projekte/Rennweg/`).
  AP3-LDT-Anfrage an din bleibt Owner-Aktion (QUELLEN.md).
- Enis' 5-Punkte-Photometrie-Paket: Leonis-Positionen mündlich an Owner
  übergeben (Memory hat Details); Stiegenhaus-Nachweislücke verifiziert.

## STAND (2026-09-06, Nacht) — #121 GEMERGT: Per-Familie-Photometrie

**main = #121-Merge, 846 grün.** AP3-Session mit zwei Ergebnissen:
- **AP3-LDT extern blockiert:** din (Dietmar Nocker) gibt die Concept-2-AP3-
  Photometrie nicht öffentlich heraus — Produktdatenportal
  (productdata.din-notlicht.com, Backend cigateway) nur Datenblätter, kein
  Relux/DIALux-Eintrag. **Owner-Aktion: LDT beim Hersteller anfragen**
  (Artikel 9020095009 Concept 2 AP3 PLC24) — dokumentiert in
  `CAD_Symbole/photometrie/QUELLEN.md`. Kommt sie: Datei + 1 YAML-Zeile.
- **Per-Familie-Naht verdrahtet** (#121): `ldt_pfad_fuer` war toter Code, der
  Antipanik-0,5-lx-Nachweis rechnete isotrop trotz Rundlinsen-LDT im Katalog.
  Neu: `registry.photometrie_je_key()` (dedupe je Datei) →
  `NotlichtPlatzierer(i_cd_fn_je_key)` → `plan_antipanik` → `_antipanik_punkte`.
  Ohne Zuordnung bit-identisch; Fluchtweg bleibt bewusst auf fluchtweg_default
  (Corridor + Achsen-Azimut #119). Mollgasse unverändert RZ 15/SL 32/ok.

**Tagesbilanz 2026-09-06: SECHS Merges** (#116 Verkaufsstätten · #117 C-Ebene ·
#118 Blatt-Prüfvermerk · #119 Optik-aus-Achse · #120 Wohnbau-Fixture · #121
Per-Familie-Photometrie), 738→846 grün.

**Nächste Kandidaten:** SPOT-Grafik · Blatt-Feld-Feinschliff auf Enis-Zuruf ·
AP3-LDT einpflegen sobald vom Hersteller da · der große Hebel bleibt Selmans
Kaskade-Verdrahtung (Barawitzka 2→47, Mollgasse 62 echte Polygone warten im
Prüfstrecken-Stand; E2E-Bänder kippen dann).

## STAND (2026-09-06, Spätabend) — #120 GEMERGT: Wohnbau-E2E-Fixture

**main = #120-Merge, 841 grün.** Handoff-Kandidat „Wohnbau einfrieren" erledigt:
- **Befund vorweg:** `spec_builder_v8.py` + `wohnbau_spec.json` waren im
  Session-Scratchpad und sind VERLOREN. Rekonstruiert aus den Owner-
  abgenommenen `output/wohnbau_v8_*.dxf` (lokal untracked, existieren noch).
- `tests/fixtures/raum_modell_wohnbau_{eg,1og,dg}.json` (EG 9 Räume/6 Türen ·
  1OG 21/17 · DG 16/12, je 1 Notausgang→final_exit) + `scripts/
  extract_wohnbau_fixture.py` (Extraktor = neue Quelle; Lernpunkt: Generatoren
  NIE nur im Scratchpad). Treue bewiesen: v8-RZ-Muster exakt reproduziert.
- `tests/e2e/test_wohnbau_durchstich.py` — 11 Tests: Bänder (heute EG 4RZ+4SL ·
  1OG/DG 4+7), Blatt-Fixierung #115, Prüfvermerk #118, Regel-15-ok #119,
  Außenleuchte, PDF-Smoke. Owner-Ausgabeweg bricht ab jetzt in CI, nicht in
  AutoCAD.

**Nächste Kandidaten:** AP3-LDT · Per-Familie-LDT-Mapping (catalog_key→LDT) ·
SPOT-Grafik · Selman-Kaskade-Verdrahtung abwarten (E2E-Bänder kippen dann).

## STAND (2026-09-06, Abend) — #119 GEMERGT: Optik aus Achse, Pläne wieder ok

**main = #119-Merge, 830 grün.** Der c0_azimut-Kandidat aus dem #117-Review ist
umgesetzt — die #117-Dauerwarnung ist Geschichte:
- **`leuchten_auf_linie_mit_richtung`** (mittellinie): Kandidaten tragen den
  lokalen Achsen-Azimut (Skelett-Tangente).
- **`lux`**: Leuchten-Items `(x,y)` ODER `(x,y,optik_azimut)` → C-Ebene RELATIV
  zur Optik-C0; `max_leuchtenabstand_mm(optik_entlang_reihe=True)` nutzt die
  C0-Keule für den Reihen-Startwert. NICHT mit globalem c0-Callable kombinieren
  (Doppel-Drehung, im Docstring gewarnt).
- **`deckung.verdichte_fluchtweg`**: rechnet mit Azimut-Tripeln, schreibt den
  Azimut als `rotation_deg` (Symbol=Kreis → visuell unverändert; Plan = die
  Montage-/Ausrichtungs-Zusicherung).
- **`registry.optik_aus_achse`** (Default an im default_bundle): Callable
  `I(γ,C-relativ)`, Befund vollständig mit ehrlichem Hinweis; ohne Azimut
  weiter konservativ Minimum über C (Flächen-SL, lux_bericht = Untergrenze).
- **Mollgasse EG: 36→32 SL, Prüfstatus warnung→ok** (32 = richtungsrichtig,
  zwischen C0-Bug 28 und Minimum 36; E2E-Docstring erklärt alle drei Stände).
- Enis im PR getaggt (sein rotation_deg-Vorbehalt adressiert: abgeleitet →
  gerechnet → vermerkt). Offen aus seiner Lane ggf. Befund-Text-Feinschliff.

## STAND (2026-09-06, Nachmittag) — #118 GEMERGT: Blatt-Feld PRÜFVERMERK

**main = #118-Merge, 824 grün.** Owner-GO + visuelle Abnahme (Mollgasse-EG-DXF in
`output/mollgasse_eg_pruefvermerk.dxf|pdf`, AutoCAD-geprüft, „passt"):
- **`_blatt_pruefvermerk`** — Feld IM Blatt, freie Bande der rechten Vorlagen-
  Spalte (y 566..596; Legenden-Unterkante 595,9 / PLANNUMMER-Linie 563,5
  vermessen): Titel + Status farbcodiert (ok 3/warnung 30/fehler 1) + Zählung +
  Photometrie-Vorbehalt (#117-Naht) + Summary-Verweis. Ohne `pruefung` entfällt
  es. Summary-Key `pruefvermerk_am_blatt`.
- Owner-Fixierung „keine Zusatz-Boxen" unberührt (`pruefbericht_drawn=False`).
- **Enis-Naht Regel 13/15 damit GEKLÄRT: Sichtbarkeit AM BLATT existiert.**
- Zwei Fallen dokumentiert: Vorlagen-TEXT-Font kann kein `·`/`—` (Kästchen →
  ASCII-Trenner) · ezdxf-Matplotlib braucht `BackgroundPolicy.WHITE`, sonst ist
  Farbe 7 weiß-auf-weiß (Projekt-`pdf_export` hat das schon).

**Auch heute: Selmans Prüfstrecken-Sprung gesichtet** (Artifact + `Projekte/
_ergebnis/`): Kaskade Layer→HATCH→Stempel-Flutung→Rest. **Barawitzka 2→47
Räume, Mollgasse 62 ECHTE Polygone (51 Flutung) = Gap-Healing-Blocker faktisch
geknackt**, Rennweg OG3 als 6. Familie (10/10). Noch Prüfstrecken-/Provider-
Stand — sobald Selman das in `ArchitekturRaumProvider` verdrahtet, kippen die
E2E-Bänder (Kipp-Anleitungen liegen bereit) und Mollgasse-Platzierung ändert
sich deutlich (Flächen-Trigger!).

## STAND (2026-09-06, Vormittag) — Sync-Session: Enis' #116+#117 reviewt + GEMERGT

**main `8248126`, 822 grün, ruff clean, kein Contract.** Owner-Ansage „mach mal
Sync alles" + Volles GO. Ablauf:

- **Selman-Pull:** 8 Raumerkennung-Commits (HATCH-Polygone, Stempel-Flutung,
  Wandkörper/Türöffnungen, Prüfstrecken-Kaskade L/H/F/R) — 777 grün, nichts
  Leonis-seitiges gekippt.
- **#117 (C-Ebene im Lux-Nachweis) reviewt (APPROVE) + GEMERGT.** Wichtiger
  Enis-Fix in MEINER Lane (`platzierung/lux.py`): bis dahin rechnete jeder
  Rasterpunkt in der C0-Ebene der LDT (Corridor-Optik: γ=60° → 149,93 cd C0 vs.
  19,53 cd C90, Faktor 7,7 zu optimistisch → falsch bestandene 1-lx-Nachweise).
  Jetzt: `(γ, C)`-Callable; ohne zugesicherte Optik-Ausrichtung konservativ
  **Minimum über alle C-Ebenen** (`rotation_deg` = CAD-Symbol-Rotation, NICHT
  Optik!). `PhotometrieBefund`/`BundleMitPhotometrie` + Prüfbericht-**Regel 15**
  + DXF-Zeichnungseigenschaft (DWGPROPS statt Box — respektiert Blatt-Fixierung).
  **Konsequenz: Mollgasse EG jetzt RZ=15/SL=36 (28→36) und Status `warnung`** —
  JEDER Plan mit Corridor-Default-LDT trägt WARNUNG, bis Ausrichtung Input wird.
- **#116 (OVE R 12-2 Verkaufsstätten-Vorprüfung, Regel 14) reviewt (APPROVE),
  Branch REPARIERT + GEMERGT:** Basis war pre-#115 → CI-grün stale; sein
  Sichtbarkeitstest erwartete die Prüfbericht-Box, die der Blatt-Modus
  unterdrückt (Regel-13-Naht, wieder!). Fix von mir auf seinen Branch gepusht:
  main-Merge + Union-Konfliktauflösung (`pruefbericht(..., photometrie=…,
  projekt_kontext=…)` — Enis hatte 14/15 vorausschauend disjunkt nummeriert) +
  Test auf Fallback-Pfad (`_blatt_vorlage_cache["doc"]=None`-Pattern).
- **Merke:** Enis-PRs künftig zuerst auf Basis prüfen (`git merge-base`) — das
  war der zweite Blatt-Naht-Testbruch; die CI-Falle „vor Merge origin/main
  reinmergen" gilt weiter.

**Neuer Leonis-Kandidat (aus #117-Review, meine Lane):** der Platzierer KENNT
die Fluchtweg-Achse beim SL-Verdichten — Corridor-Optik wird längs des Gangs
montiert. `c0_azimut` aus der Verdichtungs-Richtung ableiten und als zugesicherte
Ausrichtung an `build_default_bundle`/Registry geben → voller Nachweis statt
konservativem Minimum, Pläne wieder `ok` statt `warnung` (und vermutlich SL
36→~28 zurück). Braucht Naht-Absprache mit Enis (wie kommt die Richtung je
Leuchte in die Photometrie — heute ist `c0_azimut_grad` global je Bundle!).

**Nächste Kandidaten sonst (unverändert):** Wohnbau-Demo als E2E-Fixture
einfrieren? · Blatt-Feld für Prüf-/Statusvermerk (Enis-Naht, jetzt auch
Photometrie-Hinweis) · SPOT-Grafik · AP3-LDT.

## STAND (2026-09-05, Session-Ende) — #115 GEMERGT: Blatt-Modus fixiert

**PR #115 GEMERGT** (main `a584bc6`, **738 grün** — Enis' Abend-PRs #109/#110/#113/#114
sind eingeflossen). Das Nacht-Paket, alles Owner-getrieben am 3-Geschoss-Wohnbau
(`scratchpad/spec_builder_v8.py` + `wohnbau_spec.json`, Output `output/wohnbau_v8_*`):

- **Blatt-Modus (Rivoplan-Vorlage) ist DER Ausgabeweg**: `Vorlagen-Legende/
  Notbeleuchtungspläne-Vorlage.dxf` jetzt VERSIONIERT; liegt sie im Repo, baut
  `_baue_blatt_layout` das Blatt im Modelspace (Paperspace-Viewports rendert ezdxf
  nicht maßstabstreu) — Grundriss ins Planfenster skaliert (Geschoss-Extents),
  Legenden-Symbolspalte bestückt, PLANINHALT=Geschoss.
- **Owner-Fixierung (aus `wohnbau_v7_dg_verbessert.dxf`)**: im Blatt-Modus KEINE
  Zusatz-Boxen — LB-Legende, Stückliste, Prüfbericht-Box, Belegungsliste, alter
  Plankopf, Vorlage-Anhang alle unterdrückt; das Blatt trägt alles. Prüfbericht/
  Belegung bleiben im Summary/API. Box-Pfad existiert nur noch als Fallback ohne
  Vorlage (Tests: Fixture `ohne_blatt` patcht `_blatt_vorlage_cache["doc"]=None`).
- **PROJEKT-Platzhaltertext raus** (lief über die Spalte; Owner trägt selbst ein).
- **Rivoplan-Logo**: Vorlage referenzierte das PNG absolut in Owner-Downloads →
  Repo-Kopie `Vorlagen-Legende/rivoplan_logo.png`, IMAGE wird beim Blatt-Bau
  skaliert mitkopiert. Zwei PDF-Backend-Fixes in `pdf_export`: AxesImage ohne
  extent (savefig-tight-Crash) + **ezdxf spiegelt IMAGEs vertikal** (Logo stand
  kopfüber; empirisch an der Vorlage verifiziert, AutoCAD war immer korrekt).
- **PDF-Ausschnitt hält jetzt wirklich** (`aspect adjustable='box'` statt datalim;
  matplotlib ignorierte set_xlim) — `dxf_zu_pdf(..., ausschnitt=blatt_bbox)`.
- **Naht-Notiz Enis**: sein neuer Regel-13-Sichtbarkeitstest (Prüfbericht muss
  gezeichnet sein) kollidierte mit der Blatt-Fixierung → Test läuft jetzt auf dem
  Fallback-Pfad; im Blatt-Modus lebt der Befund in Summary/API. Falls Enis
  Sichtbarkeit AM BLATT will → Owner-Entscheidung nötig (Blatt-Feld dafür?).

**Nächste Kandidaten:** Wohnbau-Demo als E2E-Fixture einfrieren? · Blatt-Feld für
Prüf-/Statusvermerk (Enis-Naht) · SPOT-Grafik · AP3-LDT · Enis-Follow-ups (EW
produktabhängig, Blendungs-I_max, Quellen-Naht).

## STAND (2026-09-05, Spätabend) — #112 GEMERGT: Vorlage + Legende + Anlage

**PR #112 GEMERGT** (main `6b1d49c`, **681 grün**), das Abend-Paket:
- **Stückliste = Profi-Legende mit Symbol-Spalte** (din-ACAD_TABLE-Vorbild; je
  Typ-Zeile das Katalog-Symbol klein voran; Fallback ohne typ_letter unverändert).
- **Gruppenbatterie-/SV-Anlagen-Symbol** (neuer Owner-Block): LB-explizit gezeichnet
  (`lb.system_typ` gesetzt) im Technik-/Batterieraum, Label + `batterie_standort`.
- **Owner-Plan-VORLAGE** (`Vorlage_Legende`, 415×550 units): JEDER generierte Plan
  bekommt den Legenden-Rahmen rechts (auto-skaliert auf Grundriss-Höhe). In-Band-
  Guard nimmt `category: vorlage` aus; Visual-Goldens bewusst regeneriert.
- Library-Update committet (inkl. mitgekommener Elektro-Blöcke aus E-Symbole).
- Wissens-Nachträge im `STROMKREISNUMMER_DWG.md`: Voll-Analyse (SIBEL-Farb-Layer,
  Symbol-Größen ~1 m, 18 Attribute dekodiert, Legende MIT Zubehör-Artikeln,
  System-GUID→Anlage) + **Symbol→Produkt-Zuordnung web-verifiziert: din nutzt die
  ANTIPANIKLEUCHTE AP3 als Universal-Leuchte** (Rolle ≠ Produkt; SPOT = SL-Rolle).
- `Vorlagen-Legende/Baulegende.*` auf main für Selman (EI-Klassen-Vokabular).
Offen: SPOT-Grafik (nice-to-have) · AP3-LDT in Photometrie-Katalog falls DIN-
Produktwahl · Enis-Follow-ups (EW produktabhängig, Blendungs-I_max, Quellen-Naht).

## STAND (2026-09-05, Abend) — Owner-Feedback-Session + #111 GEMERGT — HIER WEITER

**Alles auf main** (`97b8a1d`, **679 grün** inkl. Selmans neuem
`test_stempel_anker.py` — AIA-Kipp-Anleitung wird schon konsumiert!). Nach den
Rettungs-Merges #105/#106/#107/#108 kam die große **Owner-Feedback-Session am
H-Testgebäude** (synthetisches RaumModell, `scratchpad/demo_h_v*.py`) — der Owner
korrigierte DXF-Outputs in AutoCAD, wir lasen die Deltas aus und machten
Engine-Regeln daraus. **PR #111 GEMERGT** mit:
- **Tür-Rendering** (`_draw_tueren`: Schwelle+Blatt+Schwenkbogen, Notausgang
  doppelt; Wandrichtung = nächste Polygon-Kante).
- **Außenleuchte §4.1.2 b** (`aussen_strategy`: SL 1 m außerhalb jedes final_exit).
- **Pfeil-zur-Tür-Regel** (Owner-DXF-Korrektur): Ausgangs-RZ = unten-Block,
  rotiert zur Tür (Anlauf-Richtung wenn RZ auf Türposition).
- **Höhenkoten KOMPLETT raus** (Owner: projektabhängig) + **AGV-Stromkreis-Label
  je Symbol raus** (Owner: unnötig — Info lebt in Anlage/Kreis/Adresse-Zeile +
  Belegungsliste + XDATA).
- **Fluchtweg-Segmente in Notlicht-Grün** (true_color 30/180/80).
- **SL-Dubletten < 2 m mergen** (Owner-„falsch"-Marker: Sonderstellen-SL neben
  Verdichtungs-SL) — `abstand_nachpass._DUBLETTEN_ABSTAND_MM`.
- **Beschriftungs-Anti-Kollision gegen SYMBOLE** (Owner-Referenzbilder
  richtig/falsch-beschriftung-platziert.png): NODEID-Label Seitenwechsel +
  Stromkreis-Label-Kandidaten (war: Label lief durch Nachbar-Aufheller).
Offene Wissens-Gaps (Enis-Lane, in #111 protokolliert): produktabhängige
Erkennungsweite (z=100/200), Blendungs-I_max-Tabellen. Audit-Fehlalarm
dokumentiert: Kreuzungs-Pfeile waren korrekt (Dijkstra-Gefälle existiert).

## STAND (2026-09-05, Nachmittag) — Contract-Merges + Lost-Merge-Rettung

**Gemergt heute:** #101 · #102 · #104 (kleiner Aufheller) + durch Enis/Selman die
drei Contract-PRs **#93/#87/#96** (RaumModell v1.1.0 · NormRegelwerk v1.2.0 ·
PlatzierungsErgebnis v1.2.0). main `6a22b9a`+, 572 grün.

**⚠️ Lost-Merge-Vorfall:** die vier Konsum-PRs #88/#92/#95/#98 wurden in ihre
BASIS-Branches gemergt — Code erreichte main nie (COORDINATION-Log). Rettung als
saubere Neuschnitte, **4 offene PRs, Merge-Reihenfolge #105 → #106 → #107, #108
unabhängig**:
- **#105** = #98-Ersatz: Symbol-Datenmodell-Konsum (luminaire_id/schaltungsart/
  typ_letter + Typ-Letter-Stückliste), 580 grün.
- **#106** = #95-Ersatz + **Enis' Review komplett eingearbeitet** (Fallback-
  Kennzeichnung `_referenz` + hinweise; Prüfregeln 12/12b manuell-prüfen für
  §4.1.2-h/i-Stellen + besondere_gefaehrdung; ≤2-m-Nachpass-Test), 586 grün.
- **#107** = #88+#92-Ersatz: OIB-Gate (fail-closed + raum-genau) + ProjektKontext
  über HTTP; enthält #106-Commits (Diff schrumpft nach deren Merge), 613 grün.
- **#108** = Verdichtungs-Fix (Owner: „zu viele Aufheller"): Nachweis auf
  Mittellinie §4.2.1 + photometrischer Start-Abstand (`lux_punkte`/
  `max_leuchtenabstand_mm`) — **Mollgasse 28→18 SL**, alles ok, 572 grün.

**Weitere Kanonisierung heute:** Symbol-Library = `Notbeleuchtungssymbole.dxf`
(klein-Aufheller 342 mm; Blau-ACI→BYLAYER-Grün) · Produkt-Digest
`PRODUKTE_SCHRACK_DIN.md` (Schrack 21 Familien + DIN komplett; Cap 20 bestätigt,
EW 20m = S2-Scheibe, 8h≈halber Lichtstrom) · Muthgasse-Digest (AIA-Layer =
Crash-Ursache, FLW-L parsebar, Kipp-Anleitung an Selman) · Aushang-Digest mit
AT-Norm-Vergleich · Architektur-Diagramm `docs/architektur.png/svg` + Skript.

## STAND (2026-09-05, Vormittag) — #101 + #102 GEMERGT

**Beide PRs auf main** (`ee562e6`, **572 grün**, ruff clean, kein Contract):
- **#101 GEMERGT** (User-GO, DWG-Input via ODA + Muthgasse 5. Familie).
- **#102 GEMERGT** (User-GO): Stromkreisnummer-Labels **+ drei Owner-Feedback-
  Nachfixes in-Session**:
  1. Label-Position: NODEID-Offset **je Symbolart** (gemessene Halbbreite RZ 290/
     SL 435 + 280 Clearance) — erst mittig im Symbol, dann zu weit, jetzt knapp
     daneben; Höhenkote 150→90 (= Label-Größe).
  2. **SL rendert grün statt blau**: Library-Blöcke tragen explizite Blau-Farben
     (HATCH ACI 150), die den Layer-Grün-Override übergehen → `library.py` stellt
     blaue ACIs beim Import auf BYLAYER (+Regressionstest).
  3. **Kanonische Symbol-Library = `CAD_Symbole/Notbeleuchtungssymbole.dxf`**
     (Owner-Entscheidung: NUR noch diese Symbole; kuratierter 5-Block-Extrakt +
     Legende, gleiche Geometrie wie E-Symbole-Teilmenge). `_LIB_RELPATH`
     umgestellt, `sync_layers` legt den Grün-Layer immer an (neue Lib hat keinen
     Safety-Layer), Mapping: „unten"-Pfeil heißt neu `notbeleuchtung- richtungspfeil
     nach unten` (mit Bindestrich; `block_names()` normalisiert lowercase!).
     E-Symbole.dxf = nur noch Herkunfts-Referenz. `.gitignore`-Ausnahme.
- Lokaler Merge-Pull war von AutoCAD-File-Lock blockiert (User musste DXF
  schließen) + Stash-Roundtrip wegen identischer Working-Tree-Files.
- **Uncommitted lokal:** `E-Symbole.dxf`/`.bak` von AutoCAD modifiziert (Engine
  liest sie nicht mehr — Owner entscheidet committen/verwerfen); Muthgasse-ZIP.

Slice-Inhalt #102 (Kern):
- Digest-Empfehlung #1 (`STROMKREISNUMMER_DWG.md`): **Zuweisungs-Pass existierte
  schon** (`platzierung/circuit_zuordnung.py`, Cap 20 + DL/BL) — gefehlt hat nur
  das Profi-Format **Anlage/Kreis/Adresse** (LABELING1) am Symbol.
- Neu `dxf_renderer.py::_stromkreisnummern` (render-seitig deterministisch aus
  `circuit_hint`, robust für alte + neue Hint-Form) + zweizeiliges NODEID-Label
  `RZ-001` / `1/1/1` (User-Entscheidung: NODEID bleibt) +
  `stromkreisnummern_drawn`-Summary.
- Mollgasse-EG-Realdaten-Check: 43/43 Labels zweizeilig, Kreis-Summen 1:1 gleich
  Belegungsliste, Cap-Rollover sichtbar (BL-Kreis exakt 20 → Kreis 3).
- Wenn #96 (v1.2.0 `luminaire_id`) mal gemergt ist: Ableitung kann vom Render in
  den Platzierungs-Pass wandern (Follow-up, kein Blocker).

Danach: 3-Owner-Stacks warten weiter auf Enis+Selman (#87/#88/#92 · #93/#95 ·
#96/#98); unblockierter Leonis-Backlog sonst leer — Kandidat Tool-Recherche #2
Docling ist Enis' Lane.

## STAND (2026-09-04, Session-Ende) — DWG-Input-Slice (ODA)

**PR #101 offen** (`leonis/dwg-input-odafc`, gepusht mit User-GO, kein Contract,
**568 grün lokal**, ruff clean; CI beim Session-Ende: contracts ✅, test lief noch —
**morgen zuerst `gh pr checks 101` prüfen, dann Merge nur mit User-GO**).
Danach nächste Kandidaten: Tool-Recherche #2 Docling (Enis-Empfehlung) / warten
auf Approvals der 3-Owner-Stacks — unblockierter Leonis-Backlog ist sonst leer;
neue Idee aus dem Digest: Stromkreis-Zuweisungs-Pass (Anlage/Kreis/Adresse,
Cap ≈20, siehe `STROMKREISNUMMER_DWG.md`-Empfehlung #1).

Tool-Recherche-Kandidat #1 umgesetzt:
- **`hauptengine/dwg_input.py`** — ODA-File-Converter-Wrapper: Discovery der
  versionierten Installations-Ordner (`C:\Program Files\ODA\*\ODAFileConverter.exe`;
  odafc-Default kennt nur den unversionierten Pfad → `is_installed()` war False),
  `stelle_dxf_bereit` (DXF passthrough = bit-identisch, DWG konvertiert R2018),
  `OdaKonverterFehlt` mit Download-Hinweis. Lokal installiert: ODA 27.1.0.
- **Pipeline + API:** `run()` nimmt `.dwg` (Konvertat im TemporaryDirectory);
  `/plan` + `/projekt` nehmen DWG-Uploads, fehlender Konverter → **503**.
- **Tests:** erstes **skip-if-Tool**-Pattern (`tests/hauptengine/test_dwg_input.py`,
  8 neue inkl. Mini-DWG-Pipeline-Roundtrip gegen 4OG-Golden + API-503).
- **Muthgasse 109B = 5. CAD-Familie:** `Projekte/Pläne 19., Muthgasse 109B - …/`
  (9 Etagen E2–E9+DD, DWG→DXF ersetzt wie vom Owner gewünscht, PDFs als Soll;
  Original-ZIP lokal untracked). Sondiert: **Crash-Klasse — kein Wand-Layer-Muster
  greift, `bounds_mm` bricht ab**; im E2E-Netz als raises-Assert gepinnt
  (Kipp-Anleitung für Selman). `.gitignore`-Ausnahmen für den Ordner + knowledge-DXF.
- **Wissens-Gap zu:** `STROMKREISNUMMER_DWG.md` — Nummern-Schema
  **Anlage/Stromkreis/Adresse** (`LABELING1`), 2× Gruppenbatterie SU 6P NET E30 à
  6 Kreise, **Cap ≈20 Leuchten/Kreis**, `IsBLString`=DL/BL (bestätigt #96),
  Typ-Letter A–P, DIN-`#v1`-Obfuskierung = XOR 0xFF auf Base64. Engine-Follow-up
  darin: Stromkreis-Zuweisungs-Pass im Format Anlage/Kreis/Adresse (NODEID-Naht).
- Housekeeping: `WETTBEWERB_ENDRA_AI.md` + Referenzfoto Hotel-Fluchtwegplan committet.

## STAND (2026-09-03, F2-Abschluss)

**F2-Session komplett gemergt (main `c915a55`, 551 grün, ruff clean, kein Contract):**
- **#84** — Abstands-Nachpass + Mollgasse-Real-Data-E2E (Handoff-Auftrag, Union-Merge mit #85).
- **#90** — Prüfregel **10b**: LB-Bereichsregel ohne matchenden Raum = Warnung (vorher dreifach
  stiller No-op). Real bewiesen: Fischa-LB auf Mollgasse → `GARAGE`-Warnung.
- **#91** — disconnected-graph-Anker: Kreuzung ohne erreichbaren Ausgang zeigt Luftlinie zum
  nächsten Ausgang statt fabriziertem „unten" (relevant für B2-Klasse).
- **#94** — Prüfregel **8b**: ≥15 Räume + Symbole, aber 0 Ausgänge/0 Segmente erkannt →
  „UNGEPRÜFT ≠ erfüllt"-Warnung (Fischamender lief vorher als „ok" durch!). + E2E-Netz
  Fischamender EG + Herrenholz EG (`tests/e2e/test_familien_durchstich.py`).
- **#97** — Prüfregel **8c**: ≥30 Türen bei <15 Räumen = Erkennung widersprüchlich →
  Warnung (Barawitzka: 116 Türen/2 Räume/0 Symbole war „ok"). + Barawitzka im E2E-Netz.

**E2E-Regressionsnetz deckt jetzt alle 4 Familien** (Mollgasse · Fischamender · Herrenholz ·
Barawitzka) mit ehrlichen Ist-Stand-Bändern + Kipp-Anleitungen für Selmans Fixes.
Sondierungs-Fakten: Fischa EG 69 Räume(69 typed)/120 Türen/0 Ausgänge/0 Segmente/8RZ+14SL ·
Herrenholz EG 473/140/0/0/0 Symbole · Barawitzka EG 2/116/0/0/0.

**Unblockierter F2-Backlog = LEER.** Es warten nur noch die drei F1-3-Owner-Stacks
(#87→#88→#92 OIB · #93→#95 Sonderstellen · #96→#98 Symbol-Datenmodell) auf
**Approvals von Enis + Selman** — Owner-Entscheidung „nicht ohne Approvals mergen"
ist protokolliert (2026-09-03). N2 Weglänge-Deckung bleibt vertagt (2× protokolliert).

**Tool-Recherche (2026-09-03), Integrations-Kandidaten priorisiert:**
1. **ODA File Converter** via `ezdxf.addons.odafc` → DWG-Input (kleinster Slice, Hauptengine;
   Backlog-Punkt `Stromkreisnummer.dwg` löst sich mit). Konverter = externes Gratis-Programm.
2. **Docling** (IBM, open source) → echtes PDF-LB-Parsing als Vorstufe vor Enis' Regel-Parser
   (Tabellen/Struktur statt Rohtext). Empfehlung an @EnisAMG.
3. **ifcopenshell** → BIM-Pfad, Spike liegt in `spikes/ifc_raum_spike.py` (IfcSpace/IfcDoor →
   RaumModell-Contract). Fertigste Vorlage, Owner @polatselman.
4. **Radiance/honeybee** → nur als Golden-Referenz im Test zur Validierung von `lux_raster`
   (nicht Laufzeit). **luxpy = GPLv3** (nur Dev-Tool). **CubiCasa5k-ML = non-commercial-Lizenz
   + Raster→Vektor-Problem** (nur als Selman-Fallback-Spike denkbar).

## STAND (2026-09-02) — F1: Quellen-Korrekturen + OIB-Gate

**F1-Session: Quellen-Korrekturen + OIB-Gate.** main war `b96ea50` (#84 gemergt, 535 grün,
Mollgasse-Real-Data-E2E an Bord). Der im Nacht-STAND geforderte **Regress-Check nach #83 ist
erledigt** (COORDINATION-Eintrag: Mollgasse EG unverändert 15 RZ + 21 SL, ok) — Track B ist
aktiv, aber mit Ud=40 (s.u.) bit-identisch zum alten Default.

**Drei PRs dieser Session:**
- **PR #87** (`leonis/oib-gate-contract`, **3-Owner, WARTET auf Enis + Selman**):
  `NormRegelwerk` v1.2.0 — `FlaechenSchwellen.quelle` (additiv), Quellen-Doku-Korrektur
  (60/8 m² = OVE E 8101/E 8002-1, scope-gebunden, NICHT EN 1838), `ProviderBundle.oib`,
  `Platzierer.place(…, *, oib: OibBefund | None = None)`.
- **PR #88** (`leonis/oib-gate-konsum`, stacked auf #87): neues `platzierung/oib_gate.py`
  (v1 projekt-global, **fail-closed**: nur `eingeschraenkt`/`uneingeschraenkt` öffnet),
  Flächen-Trigger nur bei offenem Gate, `pipeline.run(…, projekt_kontext=…)` +
  `OibRl2Provider` in der Registry + `render_summary["oib"]`-Audit. Ohne ProjektKontext
  bit-identisch (Mollgasse-E2E unverändert grün). 550 passed.
- **Dieser PR** (`leonis/quellen-korrekturen`, Leonis-Lane): Ud-Doku-Fix in `lux.py`,
  Handoff-Korrekturen, COORDINATION-Antwort an Enis + **Sonderstellen-GO**.

**WICHTIGE fachliche Korrektur (Enis, von mir übernommen): Antipanik-Ud ist 40, nicht 10**
(§4.2.2/§4.3.2 wortgleich „1:40"; die „10" war Uo≥0,1 aus §4.4.2 = anderes Maß). Ältere
STAND-Blöcke unten, die „Antipanik 1:10" versprechen, sind in diesem Punkt überholt.

**Owner-Entscheidung protokolliert: Sonderstellen-Contract Option A hat das Leonis-GO**
(2 von 3 Stimmen mit Enis; wartet auf @polatselman). **Follow-up @EnisAMG:**
`flaechen_schwellen` (Werte + `quelle`) füllen + `provider._snapshot` so erweitern, dass
die Schwellen-Quelle in `quellen` landet — dann aktiviert sich der Flächen-Trigger, sobald
ein ProjektKontext mit bestätigter OIB-Erforderlichkeit mitgegeben wird.

## STAND (2026-09-01, Nacht)

**Alles Leonis-seitige ist auf `main` (`6bf7c6a`), keine offenen Leonis-PRs.** Seit dem
Abend-Stand dazugekommen und gemergt:
- **#82** — Integrations-Artefakte für Host-/Demo-Apps: `examples/demo_run.py` (ein Aufruf
  `build_default_bundle()` + `pipeline.run()` → RaumModell + Platzierung → DXF/PDF; verifiziert
  Mollgasse EG 192 Räume / 15 RZ + 21 SL / ok) + `docs/INTEGRATION.md` (Install, Einstiegspunkt,
  Output-Shape, PDF, Wissens-Inventar, HTTP-Alternative). Kein Produktivcode.
- **#81** — dieser Handoff (vorheriger STAND).

**Selman-Übergabe:** ZIP `Notbeleuchtung_Hauptengine.zip` (komplette Engine + `normwissen/data`
+ `knowledge/extracted` + `CAD_Symbole/E-Symbole.dxf` + Beispielplan + `PROMPT_SELMAN.md`) liegt
auf User-Desktop/Documents. **Wichtiger Bau-Lernpunkt:** der Render-Schritt braucht
`CAD_Symbole/E-Symbole.dxf` (Schrack-Library) im Baum — sonst `_resolve_library_path`-Fehler.
Verifiziert durch Frisch-Entpacken + Lauf. Für Updates zieht Selman einfach `main`.

**In-flight (Enis): PR #83 offen** — „Track-B-Norm-Werte gefüllt (Ud + Umschaltzeit) + vier
Quellen-Korrekturen". Füllt `normwissen/data` (en1838_grundwerte etc.) + provider.py = **die
Aktivierung meiner Track-B-Konsumption** (kein Contract/Schema berührt). **Leonis-Action nach
#83-Merge:** Regress-Check erneut fahren (`scratchpad/verify_mollgasse.py`) — der Mollgasse-Plan
ist dann NICHT mehr garantiert bit-identisch (Antipanik-Ud 1:40→1:10, evtl. Flächen-Trigger),
das ist gewollt; prüfen, dass er weiterhin plausibel/ok ist. Enis' PR selbst = sein Merge.

**Raumerkennung-Generalität (unverändert der zentrale Blocker, Selmans Package):** die Engine
läuft auf fast jedem DXF durch, ERKENNT aber primär Mollgasse-nahe CAD-Konventionen (Layer per
Regex hardcoded: `09-WEG`/`A_Fluchtweg`, `810 Raum`/`A_Raeume`, `0N-TXT`, Wandmuster). Fremde
Familien → degradiert (typlos → RZ-only/leer) oder Crash (0 Wand-Layer). Reifegrad: Mollgasse EG
~gut, OG/DG fast leer, Fischamender Räume gut aber Fluchtweg-Bug B2 (0 Ausgänge), Herrenholz/
Baufeld 100% getypt. = Selman-Arbeit, nicht F1.

## STAND (2026-09-01, spät) — Abstands-Nachpass (PR #84)

**PR #84 (`leonis/abstand-nachpass`, off `main` nach #81/#82 rebased, kein Contract).**
**519 grün**, ruff clean, Schema kein Drift.

Neuer letzter Geometrie-Pass `platzierung/abstand_nachpass.py` (`entzerre`, in `place` nach
`lb_override`, vor `deckungs_zuordnung`): löst Symbol-Kollisionen an der **Strategie-Naht**
auf — gleich-artige Dubletten mergen, verschieden-artige nudgen (Prio `rz>sl>antipanik`, im
Raumpolygon, **nie eine Leuchte löschen**). Jede Strategie deduplizierte bisher nur intern.

**Ehrlich einordnen (nicht überverkaufen):** DOD-Befund #5 (1 Paar < 250 mm) **reproduziert
auf aktuellem `main` nicht mehr** (mit LB verifiziert: 36 Symbole, 0 Kollisionen mit UND
ohne den Pass). Der Nachpass ist daher **Defense-in-depth** (Kollisionsfreiheit invariant
statt zufällig), auf Mollgasse EG aktuell ein **No-op**. Der eigentliche Wert liegt im
**neuen Real-Data-Regressionstest** `tests/e2e/test_mollgasse_eg_durchstich.py` (skip-if-
Asset) — schließt die Fixture-Lücke, an der bisher jeder Real-Plan-Bug durchrutschte (nur
das dünne 4OG-Fake wurde getestet). +11 Tests. **Housekeeping:** PR #78 (überholt von #79)
geschlossen.

**Nächste unblockierte Platzierungs-Kandidaten** (aus 2 Explore-Sweeps, kein Contract, keine
Fremd-Owner-Daten): LB-Vokabular-Mismatch-Warnung (deckt tote `lb_override`-Regeln auf),
disconnected-graph-Anker (`graph.py`/`anker_strategy`), Validierungs-Randfälle. Weglänge-
statt-Luftlinie-Deckung bleibt vertagt (braucht Selmans reicheren Graph im Contract).

## STAND (2026-09-01, Abend)

**Track B (Konsumption) ist auf `main`** (`f92010f`, PR #80 gemergt; PR #72 = `NormRegelwerk`
v1.1.0 davor gemergt `8d6fe23`). **513 grün**, ruff clean, Schema kein Drift = **kein Contract**.
Leonis liest jetzt die neuen abfragbaren Norm-Felder — **defensiv**: solange Enis' Werte `None`
sind, ist der Plan bit-identisch (Mollgasse EG unverändert **15 RZ + 21 SL, Prüfstatus ok**):
- **A** `lux.py` — `lux_raster` bekommt `ud_min`; `deckung.py` + `flaechen_strategy.py` leiten ihn
  über `ud_min_aus_norm(anf.gleichmaessigkeit_max)` ab (Hardcode `1/40` weg). ~~Aktiv → Antipanik
  1:10~~ **KORRIGIERT 2026-09-02: Antipanik-Ud ist ebenfalls 40 (§4.3.2), nicht 10.**
- **B** `flaechen_strategy.py` — liest `regelwerk_snapshot().flaechen_schwellen`: Fläche ≥
  `antipanik_min_m2` / WC ≥ `wc_sanitaer_min_m2` → antipanik-pflichtig (EN 1838 §4.3). Reiner
  **Zusatz**-Trigger; Antipanik-Parameter aus Enis' eigener Antipanik-Regel (`_antipanik_referenz`).
- **D** `hauptengine/validierung.py` — `pruefe(…, norm=…)` (keyword-only): Regel **Umschaltzeit ≤
  Norm-Höchstwert** (LB `umschaltzeit_max_s` vs. strengster Norm-Wert). Pipeline reicht `bundle.norm`.

### → Damit Enis & Selman weiterbauen können (NÄCHSTE Schritte)
- **@EnisAMG — Track B aktivieren:** die Konsum-Logik steht, sie ist nur inert weil die Werte fehlen.
  In `normwissen/data` füllen → aktiviert sich automatisch. **KORRIGIERT 2026-09-02 (Enis' Befund
  übernommen):** `gleichmaessigkeit_max` = **40 für Rettungsweg UND Antipanik** (§4.2.2/§4.3.2; die
  „10" war Uo aus §4.4.2 — von Enis in #83 bereits so gefüllt); `flaechen_schwellen` (≈60/8 m²)
  stammen aus **OVE E 8101/E 8002-1** (scope-gebunden, nicht EN 1838) → werden erst mit dem
  OIB-Gate (#87/#88) gefahrlos füllbar; `umschaltzeit_max_s` = 60-s-Vollwert (in #83 gefüllt).
- **@polatselman — Track C (braucht Contract):** (1) neuer Raumtyp „Arbeitsplatz mit besonderer
  Gefährdung" (EN 1838 §4.4) → schaltet die schon im Contract liegende `arbeitsplatz_lux` (15/5 lx)
  frei; heute bewusst NICHT verdrahtet (wäre toter Code ohne den Raumtyp). (2) Pflicht-POIs
  (Aufzug/Erste-Hilfe/Löschgerät/BMZ) → `anker_strategy` setzt Pflicht-RZ. Beides = 3-Owner.

**Doku/Naht:** COORDINATION.md trägt den vollen Befund (Log-Eintrag 2026-09-01, Hinweis an Enis +
Track-C-Blocker). Verifikations-Skript für den Regress-Check: `scratchpad/verify_mollgasse.py`
(build_default_bundle → Mollgasse EG → RZ/SL-Zähler + Prüfstatus).

## STAND (2026-09-01, früher) — Historie: Track A

**Norm-Integration Platzierung, Track A** (PR #71 **gemergt**). Der Platzierungscode achtet beim
Setzen auf die schon in `normwissen/data` kodierten Werte statt zu hardcoden:
- **A1** `deckung.py` — Fluchtweg-`ziel_lux` aus `anf.min_lux` (norm-belegt) statt Konstante 1,0.
- **A2** `flaechen_strategy.py` — **Antipanik verdichtet bis 0,5-lx-Nachweis** (`_antipanik_punkte`),
  der 0,5-lx-Norm-Wert war vorher tot. Kleine Räume unverändert, große Halle verdichtet (Cap).
- **A3** `hauptengine/validierung.py` — **2-Leuchten-Redundanz je Fluchtweg-Abschnitt** (EN 50172),
  Warnung (kein Hard-Fail). Mollgasse EG erfüllt sie (alle 103 Abschnitte ≥ 2).
- **A4** `lux.py` — Fallback-Höhe 2,5→2,0 m (EN-Mindesthöhe), produktive Aufrufer geben Norm-Höhe.

## STAND (2026-08-31 Session-Ende)

**Alles auf `main` (166c234), 434 Tests grün, ruff clean, Drift-Gate sauber, kein
Contract berührt.** Mollgasse EG ist ein **voll-konformer Plan** (Prüfbericht **ok**:
15 RZ + 21 SL, 4/4 Notausgänge, 0 Kollisionen, 103 Segmente gedeckt, LB-Inklusion).
OG/DG bleiben fast leer — **Wurzel = F2-Raumerkennung** liefert dort ~0 Typen/Fluchtwege
(Gap-Healing-Blocker, Owner-Entscheidung), **kein F1-Fehler**.

**Heute F1 gemergt (PRs #46–#64):** Höhenkoten (h=2,40) · DoD-Visual-Golden-Harness
(`pytest -m visual`) + CI-Raster-Smoke · **covers_segment-Fix** (geometrische Deckung,
real 0→103) · **Plausibilitäts-Regel + Symboldichte-Gate** (quasi-leer = fehler) ·
**Farb-7-Fix** (Legende/Plankopf im Hell-PDF sichtbar) · **RZ an jedem Notausgang**
(§4.1.2 g, auch graphlos) + sichtlinie-Symmetrie + **Anker-Dedup** (keine
Doppelplatzierung) · **Schriftfeld-Leiste** (Info-Blöcke in gerahmter rechter Spalte) ·
2× ultracode-**Gesamtaudit** (adversarial, 7+7 bestätigte Fixes) · **Auto-Prüfeinrichtungs-
Hinweis** (EN 62034 > 20 Leuchten) · Norm-Sofort-Wins („nahe" < 2 m; z=100/200 single-source).

**NEU: Wissensbasis für die Hauptengine** — `knowledge/extracted/
PROFI_DIN_PLAN_UND_VORSCHRIFTEN.md` (aus echtem Profi-DIN-Plan Barawitzkagasse +
AT/DE-Vorschriften extrahiert). Enthält **15 priorisierte Engine-Empfehlungen** mit
Owner + Aufwand — die Roadmap für den nächsten Hauptengine-Ausbau.

### → Hauptengine-Roadmap für das Team (aus dem Digest, gemeinsames Package)

Die Hauptengine (`src/notbeleuchtung/hauptengine/`) ist gemeinsam (alle 3 Owner). Nächste
Ausbaustufen, damit Enis/Selman + Leonis integriert weiterbauen:

- **Contract-Erweiterung (3-Owner-Konsens nötig, `hauptengine/contracts/`):**
  Symbol-Datenmodell reicher — `Platzierung` um `TYPENAME`/`TYPENUMBER`(Legenden-Letter)/
  `luminaire_ID`/`MountingMethod`/`Technology`/**`Schaltungsart`(DL/BL)** erweitern (Digest
  #6). Speist Stückliste-als-Typ-Letter-Legende (#7) + QR/NODEID (#9). `richtung=beidseitig`
  existiert bereits als `richtung="gerade"` → **kein Contract nötig**, nur Render-Symbol.
- **Enis (normwissen):** EN-1838-Lux-Grenzwerte als `NormRegelwerk`-Werte kodieren (Digest #3:
  1/0,5/15/5 lx + Gleichmäßigkeiten) · Anwendungsfall-Klassifikation GK/Nutzung/Fläche →
  OIB-Stufe + Betriebsdauer (1/3/8/24 h) + Stromquelle aus LB (#11) · z pro Symbol liefern (#4).
- **Selman (raumerkennung):** hervorzuhebende Stellen (BMZ/Erste-Hilfe/Löschgeräte) +
  Pflicht-Platzierungspunkte (Treppen/Niveau-/Richtungsänderung/Aufzugsflur) im RaumModell
  erkennen (#10) · flächenbasierte Trigger (Antipanik ≥ 60 m², WC > 8 m²) (#12) · **Mollgasse
  Gap-Healing** (echte Raum-Polygone) = der Gebäude-Blocker.
- **Render/Hauptengine (F1-nah):** DIN_SIBEL-Layer-Schema statt Ad-hoc-Layer (#2) ·
  Beidseitig-Pfeil-Symbol für `richtung="gerade"` · getrennter Sicherheitskreis modellieren
  (Geschoß/Brandabschnitt, NODEID, Stromkreis-Belegungsliste kompatibel zu `1.xlsx`) (#14).

**Offene F1-Follow-ups (F2-abhängig):** Deckungs-LOS echt (Weglänge im Zirkulationsgraph
statt Luftlinie — braucht Selmans Graph/Wände) · KELLER in LB-Naht adressierbar (Vokabular-
Symmetrie). Gaps in der Wissens-Extraktion: `Stromkreisnummer.dwg` (ODA-Konverter nötig).

---

## STAND (2026-08-29 Session-Ende) — Historie

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
