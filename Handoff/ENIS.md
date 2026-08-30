# Handoff — Enis (Normwissen + LB)

> Claude: Du bist die Session von **Enis**. Owner-Package:
> `src/notbeleuchtung/normwissen/`. GitHub `@EnisAMG`.
> Lies zuerst `CLAUDE.md`, `docs/CONTRACTS.md`, `docs/ONBOARDING.md` (Abschnitt Enis).

## Stand (2026-08-30, abends — Tagesabschluss)

### Wiedereinstieg in 60 Sekunden
1. Branch **`enis/lb-parser`**, HEAD `86adfa9`, sauber auf `origin/main` (`b1a33e6`)
   rebased. Working Tree clean, **kein Rebase aktiv, keine Konflikte offen.**
2. ⚠ **Der Branch ist NICHT mergefähig und nicht lauffähig.** Die öffentliche API
   steht auf der Enis-Fassung (`LbParser`), `registry.build_default_bundle()` auf
   main importiert aber `LbTextProvider` → `import notbeleuchtung` bricht. Das ist
   der bewusst offen gelassene Stopp-Punkt, **nicht** ein Fehler.
3. Erster Schritt morgen: **API-Integration** (Abschnitt „MORGEN ZUERST").
4. `enis/lb-parser` ist gegenüber `origin/enis/lb-parser` **divergiert** (der alte
   Push saß auf altem main). Ein späterer Push braucht `--force-with-lease` —
   heute bewusst NICHT gemacht.

## MORGEN ZUERST

1. `git fetch origin` — aktuellen `origin/main` prüfen.
2. **KEINEN neuen Rebase** starten, solange sich main nicht erneut geändert hat.
3. **API-Integration** (eigener Commit). Die fail-closed Enis-Implementierung
   bleibt die fachliche Basis, die öffentliche main-API bleibt erhalten:
   - `LbParser` → **`LbTextProvider`** umbenennen
   - Modul-Funktion **`parse_lb(lb_path: str)`** ergänzen/erhalten
   - `registry.build_default_bundle()` mit `lb=LbTextProvider()` **unverändert lassen**
   - Registry-/Pipeline-Verdrahtung von Leonis **nicht** zurückdrehen
   - zusätzlich exportieren: `LbBericht`, `FeldBefund`, `LbFehler`,
     `LbNichtLesbar`, `LbReviewRequired`
   - **keine** Contract-Änderung
4. **Testdateien fachlich zusammenführen** (main + Enis).
   Unbedingt erhalten: **`test_registry_bundle_hat_lb_provider`**, die sinnvollen
   main-Regressionstests, und alle Enis-Tests (Fail-Closed, Audit, Seiten, Quellen).
   Doppelte Tests zusammenführen statt beide behalten. Keine Tests still löschen.
   **NICHT künstlich erfüllen** (alle fachlich widerlegt, siehe unten):
   Fischa → 480 min · 0,5 s · 1 lx · 5 lx · EN ISO 7010 · 24 h → 1440 min.
5. **Regressionstest:** ein synthetischer Text „Störung innerhalb 24 Stunden
   beheben" darf **niemals** `betriebsdauer_min=1440` erzeugen; `betriebsdauer_min`
   bleibt `None`, wenn keine Betriebsdauer im Notbeleuchtungs-Kontext steht.
6. Verifizieren:
   ```
   .venv/bin/python -c "import notbeleuchtung; print('import ok')"
   .venv/bin/python -m pytest tests/normwissen/test_lb_parser.py -q
   .venv/bin/python -m pytest -q
   .venv/bin/python scripts/gen_schema.py --check
   .venv/bin/ruff check .
   ```
7. **Echte lokale PDFs gegenprüfen** (`Leistungsbeschreibung BSP/`, gitignored):
   - *Fischa*: keine mo-Elektro-Skalare · kein 1440-min-False-Positive · GARAGE
     blockiert · Systemtyp-Konflikt sichtbar · Seiten korrekt (§2.10/§2.11 = S. 37)
   - *mo-Elektro*: 480 min · 0,5 s · 1,0 lx · Feuerlöscher/Wandhydrant 5 lx ·
     EN ISO 7010 · Seiten korrekt
8. Erst wenn alles grün: `git diff --stat origin/main...HEAD` prüfen.
9. Erst mit **explizitem User-GO**: `git push --force-with-lease` (der Branch wurde
   durch den Rebase neu geschrieben).
10. Danach PR öffnen — **nicht** automatisch mergen.

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

## LB-Parser — implementiert, API-Integration offen
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
- Letzter grüner Stand **vor** dem Rebase: **296 passed / 5 skipped** (39 LB-Tests),
  schema in sync, ruff sauber. Nach dem Rebase erst nach der API-Integration
  wieder aussagekräftig (siehe Stopp-Punkt oben).

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
- **LB-API-Integration** (Stopp-Punkt, siehe „MORGEN ZUERST").
- **Prozess:** `normwissen/` ist per CODEOWNERS Enis' Lane; #14, #22, #23 und #40
  gingen ohne Enis-Approval durch. Team-Frage, keine technische.
- **GARAGE/TECHNIKRAUM/LAGER** werden von der Raumerkennung nicht erzeugt
  (`raumerkennung/raumtyp.py` kennt 13 Werte) → LB-Regeln dafür sind im Platzierer
  wirkungslos. Befund liegt bei @polatselman.
- **ÖNORM B 1800:2013-08-01** beschaffen → schaltet Tabelle-6-Zeilen 2 und 10 frei.
- Weiter offen: AStV/ASchG/KennV als RIS-Volltext, OVE R 12-2, EN 1838:2025-03,
  EN 50172:2024-11; 4 Norm-Werte für Wohnungs-Fluchtweg ratifizieren.

## 0. Setup — Claude, führe das ZUERST für den Nutzer aus

1. **Arbeitsordner prüfen:** Repo-Root `Notbeleuchtung/` (`pyproject.toml` +
   `CLAUDE.md` liegen hier). Sonst → Nutzer bitten, den Ordner zu öffnen.
2. **venv + Installation:** Mac/Linux `python3 -m venv .venv` →
   `.venv/bin/python -m pip install -e ".[dev,api]"` (Windows:
   `.venv\Scripts\python.exe`). Python ≥ 3.11 nötig.
3. **Achtung Testzahl:** auf `main` ist die Suite grün. Auf `enis/lb-parser`
   schlägt sie bis zur API-Integration fehl (`registry` importiert
   `LbTextProvider`, der Branch exportiert noch `LbParser`) — **das ist erwartet.**
4. Cursor: Ordner als Workspace öffnen, `.venv` als Interpreter wählen.

## Wer du bist
Du besitzt die Wissens-Inputs für Leonis' Platzierung:
1. **NormRegelwerk** — EN 1838/ÖNorm (`En1838NormProvider`). **Steht, auf main.**
2. **OibBefund** — OIB-RL 2 Tabelle 6 (`OibRl2Provider`). **Steht, auf main.**
3. **LBVorgabe** — die Leistungsbeschreibung als 2. Input (`normwissen/lb/`).
   **Implementiert auf `enis/lb-parser`, API-Integration offen.**

Leonis **fragt** dich über die Query-APIs — er parst nie YAML.

## Regeln
Nur `normwissen/` + `hauptengine.contracts` importieren. Contract ändern =
`contract_version` bump + `python scripts/gen_schema.py` + 3-Owner-Approval.
Branch `enis/…` → PR. Irreversibles (Merge/Push/Force-Push) nur mit explizitem
User-GO.
