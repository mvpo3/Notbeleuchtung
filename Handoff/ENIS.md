# Handoff — Enis (Normwissen + LB)

> Claude: Du bist die Session von **Enis**. Owner-Package:
> `src/notbeleuchtung/normwissen/`. GitHub `@EnisAMG`.
> Lies zuerst `CLAUDE.md`, `docs/CONTRACTS.md`, `docs/ONBOARDING.md` (Abschnitt Enis).

## Stand (2026-08-31 — LB-Naht geschlossen)

### Wiedereinstieg in 60 Sekunden
1. Branch **`enis/lb-parser`**, auf `origin/main` (`9d3c080`) rebased. Working Tree
   clean, kein Rebase aktiv, **Suite grün: 422 passed / 5 skipped**, ruff sauber,
   Schema in sync.
2. Der Stopp-Punkt vom 30.08. ist aufgelöst: `registry.build_default_bundle()`
   liefert wieder einen `LbTextProvider`, `import notbeleuchtung` und der Bundle-Bau
   laufen.
3. **Nicht gepusht.** `enis/lb-parser` ist gegenüber `origin/enis/lb-parser`
   divergiert (Rebase). Push braucht `--force-with-lease` + explizites User-GO.
4. Sicherungs-Ref vor dem Rebase: **`backup/lb-parser-vor-rebase-0831`** (`5398dc6`),
   lokal. Löschen, sobald der PR durch ist.

## MORGEN ZUERST
1. `git fetch origin` — main bewegt sich derzeit schnell (30 Commits an einem Tag).
2. `git diff --stat origin/main...HEAD` prüfen, dann PR öffnen.
3. Push nur mit GO: `git push --force-with-lease`. **Nicht** automatisch mergen.
4. Danach mit Leonis klären (steht in `docs/COORDINATION.md`):
   - `pipeline.py:100` ruft `bundle.lb.parse_lb()` ungeschützt → `LbReviewRequired`
     schlägt heute als HTTP 500 durch. Vorschlag: `api/main.py` fängt `LbFehler`
     und antwortet 422 mit `bericht.als_text()`. Gemeinsame Fläche, nicht im PR.
   - `tests/fixtures/lb/fischa_lb.txt` trägt weiterhin den Titel „Projekt Fischa 46",
     obwohl sie die mo-Elektro-Skalare enthält. 3-Owner-Lane, **nicht angefasst**.

## Was am 31.08. passiert ist (5 Commits)
Rebase auf `9d3c080`; Konflikte nur in `lb/parser.py` und `test_lb_parser.py`,
beide zugunsten der fail-closed Fassung aufgelöst. Dann:

1. **LB-API** — `LbParser` → `LbTextProvider`, Modul-`parse_lb`/`parse_bericht`
   ergänzt (Default-Provider per `lru_cache`). `registry.py`/`pipeline.py`/
   `contracts/**`/`api/**` unangetastet.
2. **Raumtyp-Vokabular** — PR #49/#57 haben GARAGE/TECHNIK/LAGER/MUELLRAUM/KELLER
   eingeführt; die LB-Stützliste war gedriftet und blockierte weiterhin. Jetzt
   deckungsgleich, `TECHNIKRAUM`→`TECHNIK`, `LAGER` und `MUELLRAUM` getrennt.
   Neues Drift-Gate `tests/contract/test_lb_raumtyp_naht.py`.
3. **Feld-Lücken gegen main** — `projekt`, `batterie_standort` (neuer Extraktor,
   findet beide realen Fälle, die main verfehlt), Sonder-Lux in `feuerloescher` +
   `hydrant` getrennt, Norm-Schreibweise `OVE E 8101` wie im OIB-Datensatz,
   Inhaltsverzeichnis-Zeilen zählen nicht mehr als Fundstelle.
4. **Test-Merge** — alle 16 main-Tests übernommen (Mapping im Test-Modul), dabei
   drei echte Fehler gefunden und behoben: `OverflowError` bei langer Ziffernfolge,
   verlorener Fluchtweg-Lux ohne Quantor („Auf dem Fluchtweg 1 lx"), verlorene
   Bereichsregel, wenn die Aussage in der **Überschrift** steht. Plus die
   1440-Regression aus dem Handoff.
5. **Docs** — `docs/COORDINATION.md`: Stand, Vergleichstabelle gegen main, offene
   Naht-Fragen.

### Gegenprüfung an den 4 echten PDFs (`Leistungsbeschreibung BSP/`, gitignored)
| PDF | Ergebnis |
|---|---|
| Fischa 46 | OK · Exkl STIEGENHAUS+GANG (GK4) · Inkl GARAGE · Gruppenbatterie/Technikraum · Systemtyp-Widerspruch bleibt Review · **keine** 1440, **keine** mo-Elektro-Skalare · §2.10/§2.11 S. 37 |
| mo-Elektro | OK · 480 min · 0,5 s · 1,0 lx · Feuerlöscher+Hydrant 5 lx · ÖNORM EN ISO 7010 · Zählerraum · 6 Bereiche inkl. LAGER · §5.1.23 S. 37 |
| GU-Rahmen | blockiert (kein Notbeleuchtungs-Abschnitt + ausgelagerter Verweis) — richtig |
| mo-Bau | blockiert (kein Notbeleuchtungs-Abschnitt) — richtig |

### Wo dieser Branch main fachlich korrigiert
Fischa-Systemtyp wird nicht mehr geraten · GU-Rahmen erfindet keine Bereichsregeln
mehr · mo-Bau liefert keine leere `LBVorgabe` mehr · mo-Elektro verliert die
Umschaltzeit nicht mehr · `batterie_standort` wird tatsächlich gefüllt. Details in
`docs/COORDINATION.md`.

## OIB-Resolver — fertig, auf main
PR #32 gemerged (`564b7e9`). `normwissen/oib/` + `data/oib_rl2_tabelle6.yaml`
implementieren OIB-RL 2 Punkt 5.4 + Tabelle 6 (18 auswertbare Zeilen), erfüllen
`OibProvider.bewerte_oib`. Alle Schwellenwerte in YAML, nichts in Python hardcodiert.
Fail-closed-Regeln: kein Umkehrschluss · `nicht_erforderlich` wird nie ausgegeben ·
fehlender Fakt → `review_required` + `fehlende_fakten` · blockierende Unsicherheit
schlägt Rechnen (Kandidatenstufe nur im Audit).

**Offene Primärquelle:** ÖNORM B 1800:2013-08-01 — die OIB-Dokumente definieren die
Netto-Grundfläche nicht selbst, sondern verweisen dorthin (Begriffsbestimmungen
Norm-S. 7). Solange sie fehlt, bleiben **Zeile 2 und Zeile 10** Review-Fälle.
**Zeile 11.2** bleibt Review, weil sie im Original keinen Fußnoten-Marker trägt
(am PDF bestätigt). Details: `docs/NORMQUELLEN_AT.md` Abschnitt 4 + Zeile-0-Eintrag.

## LB-Parser — implementiert, API-Integration erledigt
Auf `enis/lb-parser` (5 Commits): `normwissen/lb/{text,struktur,felder,parser,
bericht}.py` + `data/lb_extraktion.yaml`, PDF-Support über **pypdf** (in
`pyproject.toml` ergänzt, Lazy-Import — kein Zwang auf ein `pdftotext`-Binary).

- **Fail closed:** `parse_lb()` liefert eine `LBVorgabe` nur ohne blockierenden
  Befund, sonst `LbReviewRequired` (mit vollem `LbBericht`) bzw. `LbNichtLesbar`.
  Blockierend: nicht lesbar · kein Notbeleuchtungs-Abschnitt · ausgelagerter
  Verweis ohne eigene Vorgaben · Raumtyp, den die Raumerkennung nicht erzeugt ·
  Raumtyp gleichzeitig ein- und ausgeschlossen.
- **Datengetrieben:** alle Anker, Muster, Einheiten und das Raumtyp-Vokabular in
  `data/lb_extraktion.yaml` — Python enthält nur die Mechanik.
- **Audit-Trail seitengenau:** jeder Befund trägt die Seite des **Treffers**, nicht
  die des Abschnittsanfangs (`Abschnitt.seite_fuer(offset)`).
- **Normverweise erzeugen nie Werte** · Systemtyp-Widerspruch → kein Wert, Review ·
  Kontext-Gating als Homonym-Abwehr (Brausebatterie/Kabinennotbeleuchtung).
- Test-Fixtures unter `tests/normwissen/lb_fixtures/` sind **synthetisch und
  anonymisiert**. Kein Kundendokument im Repo; die echten PDFs bleiben gitignored.
- Grüner Stand nach Rebase + Integration (31.08.): **422 passed / 5 skipped**
  (59 LB-Tests), Schema in sync, ruff sauber.

## ⚠ Kritischer Befund von heute — Kollision mit PR #40

Leonis hat **PR #40 „normwissen — ② LB-Parser"** nach main gemerged — in der
CODEOWNERS-Lane `@EnisAMG` — und über `registry.build_default_bundle()` **aktiv
verdrahtet**. Am **echten** Fischa-PDF erzeugt dieser Parser:

```
betriebsdauer_min = 1440      ← FALSE POSITIVE, sicherheitsrelevant
system_typ        = zentralbatterie   ← wählt still eine Seite des Widerspruchs
bereiche_inklusion = [GARAGE]         ← stiller No-op im Platzierer
```

`_betriebsdauer_min()` sucht `(\d+)\s*(?:Std|Stunden|h)` im **gesamten** Dokument
und trifft „Störungsbehebung binnen 24 h" (S. 12) → 24 × 60 = **1440**. Fischa
spezifiziert **keine** Betriebsdauer. Als `LBVorgabe.betriebsdauer_min` übersteuert
dieser erfundene Wert nach der Hierarchie `LB-explizit → Norm` den EN-1838-Default
von 60 min. Die fail-closed Implementierung muss das verhindern.

**Belegte Quellenzuordnung (am Original geprüft):** Fischa enthält **keine**
480 min, **keine** 0,5 s, **kein** 1 lx, **keine** 5 lx Feuerlöscher und **kein**
EN ISO 7010 (`lux`/`lx`, „Umschaltzeit", „Betriebsdauer", „Feuerlöscher", „7010“ =
je 0 Treffer; genannt ist ÖNORM Z 1000). Diese Werte stammen aus
`mo-leistungsbeschreibung_Elektro_240718.pdf` §5.1.23.

**Fischa liefert tatsächlich:** Exklusion STIEGENHAUS + GANG (GK4, §2.10 S. 37) ·
Inklusion GARAGE (§2.11) · Überwachung Einzelleuchte · Prüfung WEB · Fabrikat
DIN-Sicherheitstechnik Concept-LED (§2.21 S. 42) · Normbezüge ÖVE 8101 / R 12-2 /
EN 1838 / ÖNORM Z 1000 · **widersprüchliche Systemtyp-Angaben** (Gruppenbatterie
S. 19 vs. Zentralbatterie S. 42).

`tests/fixtures/lb/fischa_lb.txt` und die zugehörigen main-Tests tragen diese
falsche Quellenzuordnung. **Die Fixture wurde NICHT verändert** — sie liegt in der
3-Owner-CODEOWNERS-Lane. Der Befund ist nur dokumentiert und **muss mit Leonis
koordiniert werden** (Eintrag in `docs/COORDINATION.md`).

## Rebase von heute — was passiert ist
`enis/lb-parser` wurde auf `origin/main` (`b1a33e6`) rebased. Konflikte gab es
ausschließlich im LB-Hauptcommit, in genau vier Dateien:

| Datei | Auflösung |
|---|---|
| `src/notbeleuchtung/normwissen/__init__.py` | Enis-Version (Zwischenstand — API-Integration folgt) |
| `src/notbeleuchtung/normwissen/lb/__init__.py` | Enis-Version (dito) |
| `src/notbeleuchtung/normwissen/lb/parser.py` | **Enis fail-closed Implementierung** |
| `tests/normwissen/test_lb_parser.py` | Enis-Version als Basis (Merge mit main-Tests folgt) |

Die drei Folge-Commits (Docs · Verweis-Logik · Seiten-Audit) liefen **ohne neue
Konflikte** durch. Die Umbenennung auf die main-API wurde bewusst **nicht** während
des Rebase gemacht, um Folgekonflikte zu vermeiden.

## Entscheidungen (weiterhin gültig)
- **Norm-Ausgabe-Drift** (`ÖNORM EN 1838:2013` vs. real vorliegende 2019-11-15):
  nur im YAML gekennzeichnet, nicht umgestellt — der String ist Naht-Invariante
  (Blast-Radius: `docs/NORMQUELLEN_AT.md` Abschnitt 2a).
- **Photometrie-Ausnahme:** Leonis baut `normwissen/photometrie/` im Enis-Package.
- **`OibProvider` = Enis** (Tabelle-6-Schwellenwerte sind Normwissen).
- **Kein Umkehrschluss**, **nichts raten**, **blockierende Unsicherheit schlägt
  Rechnen** — gilt für OIB **und** LB.

## Offene Punkte
- **LB-PR öffnen** (Code fertig, Push braucht GO — siehe „MORGEN ZUERST").
- **`LbReviewRequired` → HTTP-Antwort**: `pipeline.py:100` ruft ungeschützt auf.
  Gemeinsame Fläche, mit Leonis zu klären.
- **Prozess:** `normwissen/` ist per CODEOWNERS Enis' Lane; #14, #22, #23 und #40
  gingen ohne Enis-Approval durch. Team-Frage, keine technische.
- ~~GARAGE/TECHNIKRAUM/LAGER werden von der Raumerkennung nicht erzeugt~~ —
  **erledigt** durch PR #49/#57; die LB-Stützliste ist nachgezogen und per
  `tests/contract/test_lb_raumtyp_naht.py` gegen erneutes Driften gesichert.
- **ÖNORM B 1800:2013-08-01** beschaffen → schaltet Tabelle-6-Zeilen 2 und 10 frei.
- Weiter offen: AStV/ASchG/KennV als RIS-Volltext, OVE R 12-2, EN 1838:2025-03,
  EN 50172:2024-11; 4 Norm-Werte für Wohnungs-Fluchtweg ratifizieren.

## 0. Setup — Claude, führe das ZUERST für den Nutzer aus

1. **Arbeitsordner prüfen:** Repo-Root `Notbeleuchtung/` (`pyproject.toml` +
   `CLAUDE.md` liegen hier). Sonst → Nutzer bitten, den Ordner zu öffnen.
2. **venv + Installation:** Mac/Linux `python3 -m venv .venv` →
   `.venv/bin/python -m pip install -e ".[dev,api]"` (Windows:
   `.venv\Scripts\python.exe`). Python ≥ 3.11 nötig.
3. **Testzahl:** Suite auf beiden Branches grün. Falls `tests/api/…pdf…` bricht:
   `matplotlib` fehlt im venv → `.venv/bin/python -m pip install -e ".[dev,api]"`.
4. Cursor: Ordner als Workspace öffnen, `.venv` als Interpreter wählen.

## Wer du bist
Du besitzt die Wissens-Inputs für Leonis' Platzierung:
1. **NormRegelwerk** — EN 1838/ÖNorm (`En1838NormProvider`). **Steht, auf main.**
2. **OibBefund** — OIB-RL 2 Tabelle 6 (`OibRl2Provider`). **Steht, auf main.**
3. **LBVorgabe** — die Leistungsbeschreibung als 2. Input (`normwissen/lb/`).
   **Fertig auf `enis/lb-parser`, PR offen.**

Leonis **fragt** dich über die Query-APIs — er parst nie YAML.

## Regeln
Nur `normwissen/` + `hauptengine.contracts` importieren. Contract ändern =
`contract_version` bump + `python scripts/gen_schema.py` + 3-Owner-Approval.
Branch `enis/…` → PR. Irreversibles (Merge/Push/Force-Push) nur mit explizitem
User-GO.
