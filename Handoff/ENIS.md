# Handoff — Enis (Normwissen + LB)

> Claude: Du bist die Session von **Enis**. Owner-Package:
> `src/notbeleuchtung/normwissen/`. GitHub `@EnisAMG`. Task: **Issue #1**.
> Lies zuerst `CLAUDE.md`, `docs/CONTRACTS.md`, `docs/ONBOARDING.md` (Abschnitt Enis).

## Stand (zuletzt 2026-08-30)

### Wiedereinstieg in 30 Sekunden
1. Branch `enis/slice-1-normprovider`, HEAD-Commit `1ca3c4e` + heutiger Docs-Commit.
   **PR #6 ist offen, CI grün, mergeable** — wartet nur auf Reviews von @mvpo3 und
   @polatselman (CODEOWNERS: der PR fasst `tests/fixtures/` an). **Merge nur mit
   explizitem Owner-GO.**
2. `.venv/bin/python -m pytest -q` muss **55 passed** zeigen; nach einem Merge von
   main ggf. vorher `.venv/bin/python -m pip install -e ".[dev,api]"` (main hat
   `networkx` ergänzt).
3. Nächster fachlicher Schritt: siehe „Was als Nächstes" unten.

### Slice 1 (NormRegelwerk) — ausgeliefert, auf aktuellem main
`En1838NormProvider` (`normwissen/provider.py`) liest `normwissen/data/
en1838_grundwerte.yaml` + `raumtyp_regeln.yaml`, erfüllt das Protocol
`NormProvider`, hardcodet nichts. Am 29.08. auf Leonis' neuen Symbol-Katalog
(PR #7–#10) nachgezogen — Commits `d3cd9b7` (data) + `b343fef` (Fixture):
- **STIEGENHAUS-Raum → `sicherheitsleuchte`** (Aufheller, EN 1838 §4.1) statt `rz`;
  Rettungszeichen hängen an den Fluchtweg-**Segmenten**. Neue Quelle §4.1.
- **GANG + `default`** bieten alle vier Pfeil-Keys an; Richtung wählt Leonis
  (`communal_stgh_strategy::_select_key`).
- **Antipanik** auf Katalog-Key `antipanik_leuchte`; **SAAL `mindest_anzahl: 4`**
  als Raster-Stützstellen (§4.3.1), verteilt via `flaechen_strategy`.
- Snapshot-Fixture **immer** aus dem echten Provider generieren, nie handschreiben:
  `En1838NormProvider().regelwerk_snapshot().model_dump()` → JSON, indent 2.
E2E liefert 7 Symbole (5 rz + 2 sicherheitsleuchte) — exakt main's Erwartung.
`heights_fachpraxis`/`clearance_rules` bewusst NICHT portiert.

### 2026-08-30 — Quellen-Bestandsaufnahme + erste OIB-Analyse (rein lesend)
Neu im Repo (vom Owner heruntergeladen, **alle drei Ordner noch untracked**):
`knowledge/OIB-Richtlinien /` (45 Dateien, Ausgabe Mai 2023, RL 1–7 komplett),
`knowledge/OVE-Fachinformation/` (17 Dateien, E01–E13 + H02),
`knowledge/Österreichische Rechtsquelle/` (1 Datei).
Ergebnisse sind in drei neuen Dokumenten festgehalten:
- **`docs/NORMQUELLEN_AT.md`** — Quellen-Status: was liegt vor (Primär/Sekundär,
  Ebenen A–D), welche aktiven Werte in `normwissen/data/` gegen die vorhandene
  EN-1838-Ausgabe belegt sind und welche nicht, was noch fehlt.
- **`docs/OIB_RL2_TABELLE6.md`** — vollständige Tabelle 6 (20 Zeilen), Punkt 5.4,
  Erläuterungen S.48, Sonderrichtlinien 2.1/2.2/2.3, Begriffsbestimmungen.
- **`docs/SPEC_PROJEKTKONTEXT_OIB.md`** — Spezifikation für Leonis: neuer
  `ProjektKontext`- und `OibErgebnis`-Contract, damit das Normwissen die
  Tabelle-6-Entscheidung überhaupt treffen kann.

**Die drei wichtigsten Befunde:**
1. **Die im Repo zitierte Norm-Ausgabe existiert im Repo nicht.**
   `en1838_grundwerte.yaml` sagt `norm: "ÖNORM EN 1838:2013"`; vorhanden ist
   **ÖNORM EN 1838:2019-11-15** (IDT mit EN 1838:2013-07, Ersatz für 2013-09).
   Inhaltlich deckungsgleich, Bezeichnung nicht. Der YAML-Kommentar zu Antipanik
   nennt bereits die 2019er-Formulierung „im Kernbereich".
2. **Belegt sind:** z=200/100, l=z·h, Dauer 60 min, 1,0 lx (§4.2.1), 0,5 lx
   (§4.3.1), Montagehöhe-Floor 2000. **Unbelegt sind:** `piktogramm_hoehe_default_m
   0.15` (Praxis), `montagehoehe_mm 2400` (Fixture-Übernahme), `mindest_anzahl 1/4`
   (Engineering-Annahmen), Quellenstring „§4.1" (belegbar wäre §4.1.2 b)).
3. **Neue Regelebene entdeckt:** OIB-RL 2 Punkt 5.4 + Tabelle 6 beantwortet die
   Frage „braucht dieses Gebäude überhaupt Sicherheitsbeleuchtung — eingeschränkt
   oder uneingeschränkt?". Diese Ebene fehlt der Engine komplett. Sie braucht
   Gebäudefakten (Nutzungsart, Gebäudeklasse, Fluchtniveau, Betten/Personen/
   Flächen), die weder `RaumModell` noch `pipeline.run()` heute kennen.

### Entscheidungen (2026-08-29/30)
- **Merge PR #6** nur nach Owner-GO; Reviews sind angefragt.
- **Photometrie-Ausnahme:** Leonis darf `normwissen/photometrie/` bauen (LDT/
  EULUMDAT → exakte Lux). Bewusste Ausnahme von der Owner-Grenze, rein additiv,
  kein Contract betroffen. Enis bleibt Owner von `data/` + `provider.py`.
- **Kein Umkehrschluss aus Tabelle 6:** Unterschreiten einer Eingangsschwelle darf
  NIE automatisch „nicht erforderlich" bedeuten → `review_required`. Betroffene
  Zeilen: 1.1, 1.2, 3, 4, 5.1, 6, 9.1, 9.2, 10, 11.1, 11.2 (Liste in der Spec).
- **Keine Normwerte aus Modellwissen**, keine Internetquellen; nur Dokumente, die
  tatsächlich im Repo liegen. Unklare Stellen werden als MANUELL PRÜFEN markiert.
- **Fachinformation ≠ Norm ≠ Rechtsquelle** — Ebenen A–D werden getrennt geführt.

### Offene Punkte
- **PR #6 mergen** (Reviews + GO).
- **Untracked lassen oder committen?** `knowledge/OIB-Richtlinien /`,
  `knowledge/OVE-Fachinformation/`, `knowledge/Österreichische Rechtsquelle/`,
  `Leistungsbeschreibung BSP/` — zusammen mehrere hundert MB PDFs. Noch nicht
  entschieden, deshalb bewusst nicht committed.
- **Zwei Fragen an Leonis** (in der Spec): Norm-Query als Methode auf
  `NormProvider` oder eigenes `OibProvider`-Protocol? Brauchen wir ein
  `GebaeudeModell` für mehrgeschoßige Kennzahlen (`RaumModell` ist geschoßweise)?
- **`norm:`-Bezeichnung in `en1838_grundwerte.yaml`** auf die tatsächlich
  vorliegende Ausgabe 2019-11-15 umstellen — noch nicht gemacht, weil das eine
  fachliche Entscheidung des Owners ist.
- **Verbindlichkeitsanker OIB** (Übernahme ins Landesbaurecht) ungeklärt.
- **Beschaffen:** kostenlos AStV/ASchG/KennV als RIS-Volltext, OVE R 12-2;
  kostenpflichtig ÖNORM EN 1838:2025-03 und OVE/ÖVE EN 50172:2024-11.
- Board-Frage von früher weiterhin offen: 4 Norm-Werte für Wohnungs-Fluchtweg
  ratifizieren (`docs/PROGRAMM_NOTBELEUCHTUNG.md`).

### Was als Nächstes
1. PR #6 durchbringen (Reviews einsammeln, dann GO abwarten, dann mergen).
2. `docs/SPEC_PROJEKTKONTEXT_OIB.md` mit Leonis abstimmen — **er** legt die
   Contracts an (`contracts/**` = 3-Owner-Approval), ich implementiere danach.
3. Erst wenn der Contract steht: `normwissen/data/oib_rl2_tabelle6.yaml` +
   Resolver `normwissen/oib/` bauen (Grenzwerte + Zeilenauswahl + Review-Regeln).
4. Parallel möglich, ohne fremden Contract: die Ausgabe-Bezeichnung und die
   unbelegten Werte in `normwissen/data/` sauber kennzeichnen (Kommentare mit
   Beleg-Status), sobald der Owner entscheidet.
5. LB-Slice (`LBVorgabe` + `normwissen/lb/`) bleibt danach; Material liegt in
   `Leistungsbeschreibung BSP/`, Format erst aus den echten Dokumenten ableiten.

**⚠ Falle beim Skripten:** Der Ordner `knowledge/OIB-Richtlinien ` endet auf ein
**Leerzeichen**, Umlaute in den Unterordnern sind NFD-kodiert → mit `glob` arbeiten,
keine handgetippten Pfade. (Die früher vermuteten `:` in den Namen existieren nicht.)

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
