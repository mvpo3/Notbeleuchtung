# Handoff — Enis (Normwissen + LB)

> Claude: Du bist die Session von **Enis**. Owner-Package:
> `src/notbeleuchtung/normwissen/`. GitHub `@EnisAMG`.
> Lies zuerst `CLAUDE.md`, `docs/CONTRACTS.md`, `docs/ONBOARDING.md` (Abschnitt Enis).

## Stand (2026-09-01)

### Wiedereinstieg in 60 Sekunden
1. **`main` ist am 01.09. weit gelaufen** — 25 Commits, PRs #71–#80, von `026f7c4`
   auf `f92010f`. Fast-Forward war konfliktfrei, es ging nichts verloren.
2. **`NormRegelwerk` steht auf Contract v1.1.0** (PR #72) — vier neue optionale
   Felder in Enis' Wissens-Naht; PR #80 konsumiert sie bereits. **Enis' Approval
   fehlte** (nur @polatselman hat approved, gemerged von @mvpo3).
3. **Track B ist gefüllt**, Branch `enis/norm-trackB-werte`, drei Commits,
   **kein Contract berührt**. Suite **517 passed / 5 skipped**, Schema in sync,
   ruff sauber. Mollgasse-EG-Durchstich unverändert: 15 RZ + 21 SL, Status `ok`.
4. **Zwei Blocker, beide nicht technisch:** das 3-Owner-GO für den
   Sonderstellen-Contract (seit 31.08., **null Reaktion**) und die Entscheidung
   über ein Scope-Gate für die Flächen-Schwellen.

## 🔴 MORGEN ZUERST

```
1. git fetch origin
2. git log --oneline -1 origin/main        # heute: f92010f — hat sich main bewegt?
3. gh pr list --state all --limit 10       # ist enis/norm-trackB-werte gemerged?
4. git show origin/main:docs/COORDINATION.md | head -40
```

**5. Ist der Track-B-PR noch offen?** Er wartet auf User-GO für Push + PR
(`enis/norm-trackB-werte`, drei Commits). Inhalt siehe „Erledigt am 01.09."

**6. Haben @mvpo3 / @polatselman auf die drei Punkte im COORDINATION-Log
   vom 01.09. reagiert?**
   - **40/10-Korrektur** — akzeptiert? Dann korrigiert Leonis die Docstrings in
     `hauptengine/contracts/norm_regelwerk.py` und `platzierung/lux.py`.
     **Nicht selbst anfassen** (3-Owner-Lane bzw. fremdes Package).
   - **Scope-Gate für `flaechen_schwellen`** — wenn GO für das Gating über
     `OibRl2Provider`: die 8 m² (OVE E 8101 `718.560.9.001.AT`) und 60 m²
     (nur Flughäfen/Bahnhöfe) füllen, **erst dann**. Ohne Gate bleiben sie `None`.
   - **Sonderstellen-GO (Option A)** — bei GO: Contract **nicht selbst ändern**,
     Umsetzung mit Leonis koordinieren (`docs/SPEC_SONDERSTELLEN_CONTRACT.md` §7),
     danach in Track B die 8 Regeln in `platzierung_regeln.yaml` von
     `input_fehlt` auf `unterstuetzt` ziehen — schrittweise, je Regel mit Test.

**7. Ohne GO nicht warten — Track-B-eigene Domain-Lücken, nach Wert sortiert:**
   1. **Lux-Niveau an hervorgehobenen Stellen** — §4.1.2 belegt die
      Hervorhebungspflicht (Leuchte ≤ 2 m), nennt aber keinen Wert. Der
      EN-1838-Volltext liegt jetzt greifbar in
      `knowledge/_extracted_text/normen/` → gegen §4.1.2 **und** die AT-Quellen
      (OVE E 8101, ÖVE/ÖNORM E 8002-1, Fachinfo E-08) prüfen. Findet sich nichts,
      ist `MANUELL_PRUEFEN` in `sonderstellen.yaml` **belegt-negativ** statt nur
      ungeprüft — das ist selbst ein Ergebnis.
   2. **Wegbreite > 2 m / Randstreifen 0,5 m** (§4.2.1, §4.3.1, Anhang B)
      fachlich strukturieren. `lux_raster` hat schon `rand_mm=500` — der
      Randstreifen ist auf Leonis' Seite implementiert, aber ohne Norm-Ref.
   3. **Niveauänderung** gegen den §4.1.2-Originalwortlaut verifizieren
      (unsere Extraktion nennt Treppen, die reale LB nennt Niveauänderungen).
   4. **Quellenlage OVE R 12-2 / OVE E 8350 / TRVB E 102** verbessern.
   5. **`MANUELL_PRUEFEN`-Fälle reduzieren** (10 Review-Regeln in der Matrix).
   6. **Ground-Truth-Quellen aufbauen** — ein bestückter realer
      Notbeleuchtungsplan fehlt im Repo weiterhin komplett.

## ERLEDIGT am 01.09.2026 — Track-B-Norm-Werte (Branch `enis/norm-trackB-werte`)

**Auftrag** (PR #81, COORDINATION 01.09.): die v1.1.0-Felder in `normwissen/data`
füllen, damit Leonis' bereits gemergte Konsumption scharf wird. **Ergebnis: zwei
Felder gefüllt, zwei bewusst leer — und vier Quellen-Fehler in PR #72 gefunden.**

### Vier Korrekturen (am Volltext geprüft, `knowledge/_extracted_text/normen/`)

| Annahme in PR #72 / `lux.py` / COORDINATION | Normtext |
|---|---|
| Ud „40 Rettungsweg / **10 Antipanik**" | §4.2.2 **1:40** · §4.3.2 **1:40** — wortgleich |
| die „10" gehöre zu Antipanik | §4.4.2: **Uo ≥ 0,1** für Arbeitsplätze mit besonderer Gefährdung — Uo (min:mittel) ≠ Ud (min:max) |
| `flaechen_schwellen` = „EN 1838 §4.3" | 60 m² / 8 m² kommen in EN 1838 **nicht vor**; §4.3.8 nennt Behinderten-Toiletten **ohne** Flächenmaß |
| `umschaltzeit_max_s` als Skalar | §4.2.6/§4.3.6/§5.4.6: **zweistufig** — 50 % in 5 s, 100 % in 60 s |

Die Docstrings in `hauptengine/contracts/norm_regelwerk.py` und
`platzierung/lux.py` tragen die 40/10-Angabe weiter — beide **nicht** in Enis'
Lane, deshalb gemeldet statt korrigiert.

### Gefüllt
- `gleichmaessigkeit.rettungsweg: 40.0` (§4.2.2) · `gleichmaessigkeit.antipanik:
  40.0` (§4.3.2), je Regel über ein neues `gleichmaessigkeit_ref` in
  `raumtyp_regeln.yaml`.
- `umschaltzeit.vollwert_s: 60.0` (§4.2.6/§4.3.6/§5.4.6). `halbwert_s: 5.0`
  bleibt in der YAML sichtbar, hat aber **kein Contract-Feld** → offene Lücke.
- Aufheller/Betonungsleuchten (§4.1): **kein** Ud-Wert — die Norm nennt keinen.

Beides **inert**: 40 ergibt über `ud_min_aus_norm` exakt den bisherigen Default
1/40; `umschaltzeit_max_s` greift nur gegen einen LB-Wert. Durchstich Mollgasse
EG vorher/nachher identisch (15 RZ + 21 SL, `ok`, 7 Befunde) — nachgewiesen,
nicht angenommen.

### Bewusst NICHT gefüllt
- **`flaechen_schwellen`.** 60 m² / 8 m² sind belegt — in **OVE E 8101:2019
  `718.560.9.001.AT`** und **ÖVE/ÖNORM E 8002-1**, dort aber **scope-gebunden**
  (8 m² nur bei „erhöhten Anforderungen nach der Art der Nutzung", 60 m² nur für
  Flughäfen/Bahnhöfe; der allgemeine 60-m²-Satz ist eine **ANMERKUNG** in einer
  Begriffsbestimmung). Das Contract-Feld wirkt **global**. Vorschlag an die 3
  Owner: den Trigger über den vorhandenen **`OibRl2Provider`** gaten.
- **`arbeitsplatz_lux`** (§4.4.1, 10 % / mind. 15 lx): belegt, aber ohne Raumtyp
  „Arbeitsplatz mit besonderer Gefährdung" wäre der Wert toter Code → Track C.

### Naht bewusst unangetastet
`NormRegelwerk.quellen` bleibt bei den drei bisherigen Strings — die neuen
Fundstellen (§4.2.2/§4.3.2/§4.2.6) sind Naht-Invariante mit 3-Owner-Blast-Radius
(`docs/NORMQUELLEN_AT.md` 2a) und stehen deshalb nur in der YAML.
`tests/fixtures/norm_regelwerk_snapshot.json` ebenfalls nicht angefasst (3-Owner)
→ `FakeNormProvider` liefert weiter `None`, die Fake-Tests üben den Fallback.
Das ist gewollt.

**Belege im Repo:** `docs/NORMQUELLEN_AT.md` Abschnitt **2b** (volle Prüftabelle
+ Scope-Tabelle der AT-Quellen), COORDINATION-Log 01.09. (drei Einträge:
Werte + Korrekturen · Sonderstellen-Nachfassen · Approval-Prozess).

## 🚧 Blocker 1 — 3-Owner-GO für den Sonderstellen-Contract

Unverändert seit 31.08. PR #69 hat **0 Reviews, 0 Kommentare**, keine Reaktion im
Log. Zweite Entscheidungsbitte steht im COORDINATION-Log vom 01.09.

**Empfohlen: Option A** — generisches `sonderstellen[]` (Feuerlöscher ·
Wandhydrant · Erste-Hilfe-Stelle · Brandmelder · Niveauänderung) plus
`ist_barrierefrei` (§4.3.8) und `besondere_gefaehrdung` (§4.4.1) auf `Raum`.
Rein additiv, schaltet **exakt** die 8 blockierten Placement-Regeln frei, vier
davon belegte Pflichtstellen aus §4.1.2. Ohne sie bleibt jeder erzeugte Plan in
diesem Punkt unvollständig, **ohne dass man es der Ausgabe ansieht**.

**Neu dazugekommen:** `besondere_gefaehrdung` ist zugleich die Voraussetzung
dafür, dass das seit v1.1.0 existierende Contract-Feld `arbeitsplatz_lux`
überhaupt einen Auslöser bekommt. Die beiden Themen hängen zusammen.

## 🚧 Blocker 2 — Scope-Gate für die Flächen-Schwellen

Neu am 01.09. `flaechen_schwellen` ist im Contract global, die belegten Werte
sind es nicht. Solange kein Gate entschieden ist, bleiben beide Felder `None` —
Leonis' `_ist_flaechen_antipanik` ist damit inert. Details oben + Abschnitt 2b.

## ⚠️ Prozess — Approvals in der `normwissen`-Lane

`normwissen/` ist per CODEOWNERS Enis' Lane. **#14, #22, #23, #40** gingen ohne
Enis-Approval durch; **#72** war zusätzlich im eigenen PR-Text als „braucht
3-Owner-Approval" deklariert und trägt trotzdem nur **ein** Approval
(@polatselman), gemerged von @mvpo3. Genau dieser PR hat die vier Quellen-Fehler
transportiert — ein Review aus der Normwissen-Lane hätte sie vor dem Merge
gefunden. Als sachlicher Team-Punkt im COORDINATION-Log vom 01.09. festgehalten.
Der Contract selbst ist inhaltlich in Ordnung und wird nicht zurückgedreht.

## Erledigt am 31.08.2026

### A. LB-Parser / 2. Input — **vollständig auf `main`** (PR #60)
Echter `LBProvider.parse_lb` über `normwissen/lb/`, fail closed. Rebase auf
`9d3c080`, API-Naht auf die main-Namen (`LbTextProvider` + Modul-`parse_lb`/
`parse_bericht`), `registry.py` unangetastet.

- **Raumtyp-Vokabular synchronisiert** (PR #49/#57 hatten GARAGE/TECHNIK/LAGER/
  MUELLRAUM/KELLER eingeführt, die LB-Stützliste war gedriftet): `TECHNIKRAUM` →
  `TECHNIK`, `LAGER` ≠ `MUELLRAUM`. Neues Drift-Gate
  `tests/contract/test_lb_raumtyp_naht.py`. Erst dadurch parsen beide realen
  Elektro-LBs überhaupt durch.
- **main-Härtungen übernommen** (#45/#56) + fünf Feld-Lücken geschlossen:
  `projekt`, `batterie_standort`, Sonder-Lux-Split feuerloescher/hydrant,
  Norm-Schreibweise `OVE E 8101`, Inhaltsverzeichnis-Filter im Audit-Trail.
- **Drei echte Fehler beim Test-Merge gefunden und behoben:** `OverflowError` bei
  langer Ziffernfolge · verlorener Fluchtweg-Lux ohne Quantor („Auf dem Fluchtweg
  1 lx") · verlorene Bereichsregel, wenn die Aussage in der **Überschrift** steht.
- Alle 16 main-Tests übernommen + 1440-Regression.

### B. API — `lb_review` erreicht den Client (PR #67)
`pipeline.run()` setzte `render_summary["lb_review"]`, `api/main.py` filterte es
über `_SUMMARY_HEADER_KEYS` wieder weg → der Client bekam einen normal aussehenden
Plan, ohne zu erfahren, dass die LB-Vorgaben **nicht** angewendet wurden. Fail
closed brach an der Auslieferungs-Schicht ab.

`/plan` **und** `/projekt` gefixt (letzterer hatte dieselbe Lücke), Review-Meldung
im Header bei 600 Zeichen gekappt (`gekuerzt: true`). Vier E2E-Tests, gegen den Fix
verifiziert.

### C. Placement-Decision-Matrix (PR #68)
`normwissen/data/platzierung_regeln.yaml` + Query-API `PlatzierungsRegelwerk`:
**25 Regeln** (11 RZ, 14 SL) + **4 Hard Stops**. Auslöser → Leuchtenart,
Positionierungsziel, Orientierung, Abstand/Lux, Priorität, Ausnahmen,
Konfliktregel, Quelle, Normreferenz, Review-Flag, Decision-Source.

Hierarchie maschinenlesbar: `hard_stop > lb_explizit > referenz_praxis >
norm_default`; `gewinner()` gibt bei Gleichstand `None` = Review. Keine zweite
Regelwelt — Zahlen bleiben in `en1838_grundwerte.yaml`, referenziert über `*_ref`.

Ground-Truth-/Auslöser-Analyse Mollgasse EG: 7 Fälle, vier greifen, drei halten
eine Lücke fest. 27 Domain-Tests + 9 Ground-Truth-Tests.

### D. Sonderstellen-Spezifikation (PR #69) — **Contract NICHT geändert**
`normwissen/data/sonderstellen.yaml` + `SonderstellenKatalog` + 17 Tests +
`docs/SPEC_SONDERSTELLEN_CONTRACT.md`. Der Vorschlag ist ausführbar gemacht, damit
nicht auf dem Papier entschieden werden muss.

**Empfehlung Option A:** generisches `RaumModell.sonderstellen[]` (Typen
`feuerloescher`, `hydrant`, `erste_hilfe`, `brandmelder`, `niveauaenderung`) plus
zwei Raum-Flags `ist_barrierefrei` (§4.3.8) und `besondere_gefaehrdung` (§4.4.1).
Schaltet **exakt** die 8 blockierten Placement-Regeln frei — ein Test hält die
Gleichheit fest. Rein additiv, alle Felder mit Default.

## Fachliche Entscheidungen vom 31.08. — weiterhin bindend

- **Die 5 lx an Feuerlöscher/Wandhydrant sind KEIN pauschaler EN-1838-Normwert.**
  Normativ belegt ist die **Hervorhebungspflicht** (§4.1.2, Leuchte ≤ 2 m). Der
  konkrete Wert stammt aus der Projekt-LB (§5.1.23) und kommt über
  `LBVorgabe.sonder_lux`. `SonderstellenKatalog.norm_lux()` gibt für **jeden** Typ
  `None`; zwei Tests nageln das fest. **Nicht aufweichen.**
- **Feuerlöscher und Wandhydrant bleiben getrennt** — zwei Geräte, zwei Orte, zwei
  2-m-Umgebungen, auch wenn die LB sie in einem Satz nennt.
- **Unsichere oder widersprüchliche Normfälle bleiben `MANUELL_PRUEFEN` / Review.**
  Eine Regel ohne Fundstelle darf nie als Norm-Default durchgehen — die Invariante
  `test_ohne_normbeleg_kein_stiller_norm_default` erzwingt das.
- **Ground Truth wird nie erfunden.** Im Mollgasse-Material liegt **kein**
  professionell fertig gezeichneter Notbeleuchtungsplan: die Architekturpläne haben
  0 Notbeleuchtungs-Layer, „Mollgasse Notbeleuchtung" ist ein 5,8-kB-Screenshot,
  der DIN-Referenzplan (PR #66) ist eine Symbol-Bibliothek mit 0 platzierten
  INSERTs. Die Ground-Truth-Fälle beschreiben deshalb die **Auslöser-Lage**, nicht
  ein Soll-Ergebnis.
- **`stair_exit` wird von der Raumerkennung nicht erzeugt** (Mollgasse EG/1OG/1KG
  geprüft: 0 `stair_exit`, 0 `stair`-Knoten — trotz zwei STIEGENHAUS-Räumen im EG).
  Blockiert `RZ-05` und `RZ-07` auf echten Plänen. Befund liegt bei
  **@polatselman**; die Matrix führt beide Regeln ehrlich als `teilweise`.
- **Track-B-Regeln bleiben maschinenlesbar und quellengebunden.** Fachwerte in
  YAML, Python nur Mechanik. Jede Regel trägt `quelle`, `norm_ref` und `beleg`.

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

## LB-Parser — vollständig auf `main` (PR #60)
`normwissen/lb/{text,struktur,felder,parser,
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
- Stand auf `main` (31.08., Tagesende): **486 passed / 5 skipped**, Schema in
  sync, ruff sauber.

## ✔ ERLEDIGT — Kritischer Befund vom 30./31.08.: Kollision mit PR #40

> **Behoben und auf `main`.** Der 1440-False-Positive ist beidseitig weg (main durch
> `facabe0`, Enis durch das Anker-Gating + `plausibel_max`); Regressionstest
> `test_stoerungsfrist_erzeugt_keine_betriebsdauer`. Der Eintrag bleibt als Beleg
> stehen — die Fixture `tests/fixtures/lb/fischa_lb.txt` trägt weiterhin die falsche
> „Projekt Fischa 46"-Zuschreibung (3-Owner-Lane, bewusst nicht angefasst).


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

## Historie — Rebase vom 31.08. (abgeschlossen)
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
- 🚧 **3-Owner-GO für den Sonderstellen-Contract** — siehe Blocker 1.
- 🚧 **Scope-Gate für `flaechen_schwellen`** — siehe Blocker 2.
- 🚧 **Track-B-PR** `enis/norm-trackB-werte` wartet auf User-GO für Push + PR.
- **`umschaltzeit_max_s` bildet nur eine Stufe ab** — die Norm ist zweistufig
  (50 % in 5 s, 100 % in 60 s). Die 5-s-Stufe hat kein Contract-Feld; ob sie eins
  bekommt, ist eine 3-Owner-Frage. Bis dahin steht sie nur in der YAML.
- **Lux-Niveau an hervorgehobenen Stellen** (§4.1.2 nennt keines) — Normquelle
  beschaffen. Wichtigster fachlicher Punkt.
- **Niveauänderung** gegen den §4.1.2-Originalwortlaut verifizieren.
- **`stair_exit` fehlt** in der Raumerkennung → blockiert `RZ-05`/`RZ-07`
  (@polatselman).
- **Quellenlage** OVE R 12-2 / OVE E 8350 / TRVB E 102 (nur Nennung, kein Volltext)
  · `vorschriftenkurzuebersicht-at.pdf` ist AES-verschlüsselt, nicht auswertbar.
- **Wegbreite > 2 m / Randstreifen 0,5 m** (§4.2.1/§4.3.1, Anhang B) nicht modelliert.
- **`tests/fixtures/lb/fischa_lb.txt`** trägt weiterhin die falsche Quellenzuordnung
  (3-Owner-Lane, bewusst nicht angefasst) — mit Leonis zu klären.
- **ÖNORM B 1800:2013-08-01** beschaffen → schaltet Tabelle-6-Zeilen 2 und 10 frei.
- Weiter offen: AStV/ASchG/KennV als RIS-Volltext, EN 1838:2025-03,
  EN 50172:2024-11; 4 Norm-Werte für Wohnungs-Fluchtweg ratifizieren.
- **Prozess:** `normwissen/` ist per CODEOWNERS Enis' Lane; #14, #22, #23, #40 und
  **#72** gingen ohne Enis-Approval durch — siehe Abschnitt „Prozess" oben.
- **Aufräumbar:** alle `enis/*`-Branches sind vollständig in `main`; der lokale Ref
  `backup/lb-parser-vor-rebase-0831` hat seinen Zweck erfüllt.

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
   **Steht, auf main.**
4. **Placement-Decision-Matrix** — `PlatzierungsRegelwerk` (25 Regeln + 4 Hard
   Stops). **Steht, auf main.** Contract-Kandidat, noch nicht im Ports-Protocol.
5. **Sonderstellen-Katalog** — `SonderstellenKatalog`. **Vorschlag, wartet auf GO.**

Seit Contract v1.1.0 liefert `NormRegelwerk` zusätzlich `gleichmaessigkeit_max`
und `umschaltzeit_max_s` (gefüllt) sowie `flaechen_schwellen` und
`arbeitsplatz_lux` (bewusst leer, s. Blocker 2 bzw. Track C).

Leonis **fragt** dich über die Query-APIs — er parst nie YAML.

## Regeln
Nur `normwissen/` + `hauptengine.contracts` importieren. Contract ändern =
`contract_version` bump + `python scripts/gen_schema.py` + 3-Owner-Approval.
Branch `enis/…` → PR. Irreversibles (Merge/Push/Force-Push) nur mit explizitem
User-GO.
