# Handoff — Selman / Raumerkennung · Arbeitsstand

> **Zweck:** eine neue Session soll ohne Rückfragen weiterarbeiten können.
> Dies ist der **Arbeitsstand**, nicht das Onboarding — Setup, venv und
> Rollenbeschreibung stehen in `Handoff/SELMAN.md`, Sync-Regeln in
> `Handoff/SYNC.md`, Architektur in `CLAUDE.md`.

Stand: **2026-09-13** · Owner Selman (`raumerkennung`)

---

## 1. Wo der Stand liegt

| | |
|---|---|
| Branch | **`selman/geschoss-erkennung`** (gepusht, lokal = remote) |
| Commit | Stand nach dem Rennweg-Durchgang — siehe Commit-Tabelle unten |
| Basis | `c820b68` (origin/main), am 13.09. per `git merge` eingeholt (`fbbc050`) — `git rebase` lehnt der Auto-Modus als destruktiv ab |
| PR | **keiner** — PR #155 wurde am 12.09. von `mvpo3` in main gemergt (`c506662`), der Branch hat seither keinen offenen Kanal |
| Merge | **nicht gemergt, nicht mergen** ohne Owner-Freigabe |

Eigene Commits über `origin/main`:

| SHA | Inhalt |
|---|---|
| `47e9e44` | Geschoss mehrstufig + fail-closed — **ARBEITSSTAND, NICHT FREIGEGEBEN** |
| `4a5e873` | `scripts/analyse/gesamtdarstellung.py` (Werkzeug) |
| `1e642ad` | Gesamtdarstellung aller 83 Repo-Pläne (Bilder, Kennzahlen, Index) |
| `538d8d8` | `scripts/analyse/raumerkennung_darstellung.py` — nur Räume, Ordner für Ordner (§ 2.3) |
| danach | Kommentar-Korrektur im Skript · Ergebnis Rennweg + `BERICHT.md` · dieser Nachtrag |

**Nicht verlieren:** `47e9e44` enthält einen offenen BLOCKER (§ 3). Der Commit
ist bewusst so betitelt, damit ihn niemand für freigegeben hält.

---

## 2. Was zuletzt gebaut wurde

### 2.1 Geschosserkennung (`47e9e44`) — gebaut, geprüft, **nicht freigegeben**

Neues Modul `src/notbeleuchtung/raumerkennung/geschoss.py`:
`GeschossBefund(geschoss, quelle, beleg)`, Stufen `floor → dateiname →
schriftfeld → plantext → hoehenkote → unbekannt`. `geschoss_aus` bleibt als
dünne Hülle mit unveränderter Signatur, alle Bestandsaufrufer laufen weiter.

Was **trägt** (von zwei unabhängigen Gegenprüfungen nachgerechnet):

- **Das Gate**: `ohne_unzulaessige_final_exits(ausgaenge, geschoss)` in
  `ausgaenge.py`, aufgerufen in `provider.py:166` **nach** dem Zusammenlegen —
  die einzige Engstelle, durch die beide `final_exit`-Erzeuger laufen
  (`leite_ausgaenge` und das rein geometrische `footprint.hauptausgaenge`).
  Bei echtem UNBEKANNT entsteht nachweislich kein `final_exit`.
- `fluchtweg.py` erfindet bei UNBEKANNT kein Ziel mehr (vorher fiel es über
  `or ausgaenge` auf einen `stair_exit` zurück und zählte den Weg als erfüllt).
- Die **DATEINAME-Stufe** ist die belastbare: 55 von 83 Plänen, **keine einzige
  Regression** gegenüber dem Ausgangsstand.
- Die beiden stillen `or "EG"` in `plan_pruefen.py` und `uebersicht_karte.py`
  sind weg.
- Contracts und `tests/naht/` unberührt. `1335 passed, 11 skipped, 14 xfailed`.
  `ruff: All checks passed`.

### 2.2 Gesamtdarstellung (`4a5e873`, `1e642ad`)

`scripts/analyse/gesamtdarstellung.py` — ein großes Bild je Plan (≥ 2000 px,
Legende in eigenem Streifen), `kennzahlen.json` je Plan, und
**`Projekte/_ergebnis/index.html`** zum Durchklicken (statisch, offline).

Wiederverwendung statt Neubau: Rotation/Zoom/Cluster aus `uebersicht_karte`,
Türbögen/Ausgangskreise/Segmentfarben aus `plan_pruefen` (Bild `05_fluchtweg`).

Lauf über **alle 83 DXF**, 113,8 min: **75 ausgewertet, 8 nicht auswertbar**.
78,4 MB Bilder; `Projekte/_ergebnis` wuchs von 16 MB auf 96 MB.

Zwei bewusste Abweichungen von der Owner-Vorgabe, im Code begründet:
`ist_notausgang` ist ein **Flag neben** `tuer_detail`, darum bleibt die
Kombination `HE/NA`; und `AUSSEN_GESCHLOSSEN` existiert im Contract nicht —
dafür dienen die geschlossenen Innenhöfe aus `provider.letzte_aussenbereiche`.

Neustart des Laufs:
`.venv/Scripts/python.exe scripts/analyse/gesamtdarstellung.py`
(nur Index: `--nur-index`, ein Plan: `<pfad.dxf>`).

### 2.3 Raumerkennungs-Darstellung Rennweg (`538d8d8`) — nur messen, nichts repariert

Owner-Auftrag 13.09. abends: reiner Raumerkennungs-Output ohne Fluchtwege,
Ausgänge, Türtypen und Platzierung; Owner-Farbtabelle; Stempel, die nicht im
zugeordneten Raum liegen, als Linie. Auf Owner-Korrektur **nur `Rennweg.zip`**
aus `Projekte_Leere Architektpläne (Input)/` (7 DXF), nicht alle 59 Eingangspläne.

- Werkzeug: `scripts/analyse/raumerkennung_darstellung.py --ordner Rennweg`.
  Stempel→Raum ist die echte Zuordnung (`KaskadeErgebnis.zuordnungen`), nicht
  Punkt-in-Polygon wie in `gesamtdarstellung`.
- Ergebnis: **`Projekte/_ergebnis_raumerkennung/index.html`**, Befunde in
  **`Projekte/_ergebnis_raumerkennung/BERICHT.md`**. Für Leonis und Enis im
  GitHub-Browser: `README.md` je Ordner mit eingebetteten Bildern (`511ad36`).
  Gegenprobe auf reinem `origin/main`: alle Owner-Kennzahlen identisch. 7/7 ausgewertet ·
  125 Räume · 19 UNBEKANNT · 94 mit Stempel · 1 Abweichung > 10 % · 15 Wohnungen.
- Geprüft vor dem Commit: Review-Workflow (4 Linsen, je 3 Skeptiker, 18 Befunde
  am Skript bestätigt und behoben), Sichtprüfung aller 8 Bilder,
  Headless-Chrome-Screenshot beider Index-Seiten.
- Testschranke nach dem Merge von `c820b68`, volle Suite **allein** auf `f97d1e1`:
  **1420 passed, 11 skipped, 14 xfailed, 0 failed** (19:53 min), `ruff check .`
  grün. Ein erster Lauf parallel zum 59er-Probelauf ergab 2 failed + 12 errors,
  alle `MemoryError` (Muthgasse-/Mollgasse-Fixtures, `test_extents_ausreisser_kein_oom`);
  dieselben Dateien einzeln: 22 passed, 4 xfailed.

Nebenbefunde aus dem **verworfenen** Probelauf über alle 59 Eingangspläne
(Stand `fbbc050`, nicht committet — die Ergebnisse lagen nur im Session-Scratchpad):

- **Aichholz und Am Rain: `Keine Wand-Entities`** auf 7 von 9 bzw. 6 von 6 Plänen.
  Es sind echte Grundrisse, aber `dxf_load.WALL_PATTERN` greift nicht. Gemessene
  Layernamen: Aichholz `1-zwischenwand`, `5-stahlbeton`, `1-stb`; Am Rain
  `Wand Beton tragend`, `Wand Mauerwerk tragend`, `Wand Trockenbau`,
  `Wand brüstungshoch`. Aichholz 1DG und 1OG endeten nach 2 s mit Exitcode 1
  ohne Ergebnis — Ursache nicht gesichert, lief unter Speicherdruck.
- **Baufeld E2:** 6 von 8 Plänen `MemoryError`, während 4 Worker parallel liefen
  (ein Worker gemessen bei 9,2 GB). Das Skript hat dafür jetzt ein Byte-Budget.
- **Papierbereich-Drehung:** alle 7 Barawitzka- und alle 8 Baufeld-E2-Pläne tragen
  VIEWPORTs mit View-Twist ≠ 0. Das Skript dreht nur in 90°-Schritten aus dem
  Modelspace — für diese Ordner ist „wie geplottet" **nicht** erfüllt.
  Rennweg hat keine Viewports.
- `plan_pruefen._rotation` lieferte auf allen 35 erkannten Plänen 0°; der
  90°-Zweig des Skripts ist nie gelaufen.

---

## 3. Die vier offenen Entscheidungen zur Geschosserkennung

**Der Owner entscheidet, nicht die Session.** Bis dahin bleibt `47e9e44`
ungemergt. Grund: die drei Plan-Stufen lesen ein Geschoss aus Text, der nicht
aussagt, *welches Blatt* vorliegt. Zweimal wurde ein Fix versucht, zweimal war
er nur eine Verschiebung (Schriftfeld → Plantext).

| # | Entscheidung | Belegte Lage |
|---|---|---|
| **1** | **Plan-Stufen SCHRIFTFELD und PLANTEXT streichen?** | Dateiname (55/83) und Höhenkote sind belastbar, die Textstufen nicht. Ohne sie bleiben mehr Pläne UNBEKANNT — fail-closed, also die sichere Richtung, aber eine Abweichung von der ursprünglichen Reihenfolge. |
| **2** | **„*n*. Stock" als Muster aufnehmen?** | Barawitzka `1 St`/`2 St`/`3 St` tragen ihr Geschoss als „1.Stock PP STG1" im Plankopf. `STOCK` ist bewusst **kein** Muster (wäre eine neue Wortform ohne Owner-Deckung). Mit ihr wären die drei Blätter sauber belegt statt UNBEKANNT bzw. falsch. |
| **3** | **`api/main.py:125` Default `Form("EG")` auf leer?** | Stufe 0 (`floor`) schlägt alle anderen. Jeder Upload über `POST /plan` ohne gesetztes Formularfeld ist damit ein ausgangsfähiges Erdgeschoss — Schnitt, Legende und Symbolbibliothek eingeschlossen. Das ist die Naht zur Hauptengine, nicht mein Package allein. |
| **4** | **`_MIND_KOTEN = 3` bestätigen oder kippen?** | Setzung des Umsetzers, im Code als solche markiert (neben den als OWNER-SETZUNG markierten Schwellen +3 m / −1 m). Ohne sie entschied auf zwei Blättern **eine einzige Kote** das Geschoss. |

### Der offene BLOCKER, live und sicherheitsrelevant

`Projekte/Barawitzkagasse/415_260415_PP_VA_1_6 3 St.dxf` liefert **`EG`
(Quelle `plantext`)** und trägt damit **7 `final_exit` auf einem 3. Stock, ohne
jede Warnung**.

Ursache am Plan gemessen: der Modelspace führt **2× „Erdgeschoß\PTop 01"**
(ein Wohnungsverzeichnis) gegen **2× „2. Stock"**. „Stock" ist kein Muster, die
Wortform gewinnt. Nebenbefund: Blattname (`3 St`) und Plankopf (`2. Stock`)
widersprechen sich — der Plan ist mit den vorhandenen Mustern **nicht sicher
bestimmbar**.

Gegenprobe im selben Haus, beides korrekt:
`2 St` → `OG` über Höhenkote · `1 St` → UNBEKANNT, fail-closed, 0 `final_exit`.

Weitere bestätigte Schwächen derselben Wurzel (eigene Läufe):
`"Zubau 2026 Obergeschoss"` → **`6OG`** (Jahreszahl wird Geschossnummer) ·
`"Leiter wird im Kellergeschoss untergebracht"` → `KG` ·
`_mehrheit` gibt bei Gleichstand 2:2:2:2 ein `1OG` mit `unbekannt=False`
zurück — ein Gleichstand ist das Gegenteil eines Belegs ·
`_ist_nicht_plan` läuft **hinter** der Dateiname-Stufe, „Schnitt A-A EG.dxf"
bekommt weiter ein `EG`.

### Testlücke, noch nicht geschlossen

Der volle Testlauf ist **grün (1335 passed)** — **beide BLOCKER liefen daran
vorbei.** Kein Test fängt einen erfundenen Beleg, und
`test_stufe_hoehenkote_nullnah_ist_erdgeschoss` **verlangt** sogar den
EG-Fallthrough, den der Owner verboten hat. Vorbild für den fehlenden Riegel
liegt im Repo: `tests/contract/test_keine_erfundenen_masse.py` (samt
Schutzschalter-Test, der anschlägt, wenn der Riegel ins Leere prüft).

---

## 4. Offene Befunde aus dem Index — alle selbst gemessen

Quelle: die 75 `Projekte/_ergebnis/*/kennzahlen.json`, Stand `1e642ad`.
Nichts davon ist behoben; dieser Durchgang war **nur Darstellung**.

### 4.1 Wohnungseingang-zu-Wohnung-Missverhältnis — 30 von 75 Plänen

Türen werden als `wohnungseingang` erkannt, aber nicht zu Wohnungen
zusammengefasst. Die Wohnungsbildung greift auf diesen Plänen praktisch nicht.

| Plan | `wohnungseingang` | Wohnungen | Verhältnis |
|---|--:|--:|--:|
| `260320_938-AR-PP-21000-A_ERDGESCHOSS BT2` | 42 | 1 | 42,0 |
| `260320_938-AR-PP-11020-A_2.OBERGESCHOSS BT1` | 82 | 2 | 41,0 |
| `Elektromontageapläne_2-OBERGESCHOSS BT1` | 90 | 3 | 30,0 |
| `260320_938-AR-PP-11010-A_1.OBERGESCHOSS BT1` | 53 | 2 | 26,5 |
| `260320_938-AR-PP-11000-A_ERDGESCHOSS BT1` | 79 | 3 | 26,3 |

Schwelle der Auswertung: ≥ 3 Wohnungseingänge je Wohnung. Gesamt **30 von 75**.

### 4.2 `final_exit` in Keller- und Untergeschossen — 4 von 7 Plänen, 11 Ausgänge

Ein Kellergeschoss mit Endausgang ins Freie ist fachlich zu prüfen; das Gate
sperrt heute nur Obergeschosse und UNBEKANNT.

| Plan | Geschoss | `final_exit` |
|---|---|--:|
| `260320_938-AR-PP-11990-A_UNTERGESCHOSS BT1` | UG | 4 |
| `Elektromontageplan_Untergeschoß` | UG | 3 |
| `1.Kellergeschoß` | 1KG | 2 |
| `2.Kellergeschoß` | 2KG | 2 |

### 4.3 „3 St" als EG

Siehe § 3 — derselbe Befund, hier als Index-Eintrag sichtbar: Geschoss `EG`,
Quelle `plantext`, **7 `final_exit`**.

### 4.4 Dubletten in `Projekte/_eingang/` — 4 von 5

Vier der fünf Prüfstrecken-Pläne sind **byte-identisch** (SHA-256) mit einem
Plan im Projektordner und wurden im Lauf **doppelt gerechnet**:

| SHA-256 (gekürzt) | `_eingang` | Original |
|---|---|---|
| `76ed8b45…` | `Barawitzka_EG` | `Projekte/Barawitzkagasse/415_260415_PP_VA_1_3 0 EG.dxf` |
| `7044ff3b…` | `Rennweg_EG` | `Projekte/Rennweg/EG - Rennweg 15_….dxf` |
| `4a0b6608…` | `Mollgasse_EG` | `Projekte/Mollgasse/Erdgeschoß.dxf` |
| `d840674b…` | `Muthgasse_E2` | `Projekte/…/M109B_… GRUNDRISS E2.dxf` |

`Rennweg_OG3` hat **keinen** inhaltsgleichen Partner im Lauf.

### 4.5 Nicht-Grundrisse im Lauf — 8 Pläne

Alle scheitern mit `ValueError: Keine Wand-Entities gefunden — Layer-Muster
prüfen.` und stehen **mit vollem Traceback im Index** (nicht übersprungen —
Owner-Vorgabe „ich will sehen, wo es gar nicht läuft"):

`Baulegende`, `Baulegende (Legende)`, `E-Symbole`, `E-Symbole-clean`,
`Notbeleuchtungssymbole`, `Notbeleuchtungspläne-Vorlage`,
`din Planungsunterstützung_Stromkreisnummer`,
`din_support_ReMi_Barawitzkagasse_28.04.2026`.

**Achtung Stolperfalle:** `Baulegende.dxf` existiert **zweimal** im Repo
(`Projekte/Rennweg/Legende/` und `Vorlagen-Legende/`). Beide schrieben
ursprünglich in denselben Ausgabeordner — 83 Läufe ergaben 82 Index-Einträge,
ein Plan verschwand lautlos. Behoben über `_ausgabename`, das bei Kollision den
übergeordneten Ordner anhängt.

### 4.6 Stempel auf falschem Raum — Sichtbefund, nicht gemessen

Am kleinsten Plan (`Projekte/EG_Grundriss_DE_NEU.dxf`) im Bild sichtbar:

- Stempel **„BAD/WC" mit 6,9 m²** sitzt auf einem **22,5 m²** großen Raum, der
  als **`ZIMMER`** typisiert ist. Beschriftung im Bild: `BAD/WC · ZIMMER ·
  22.5 m² (6.9)`.
- Wohnungsstempel **„Top 1" mit 55,4 m²** wird einem **13,3 m²**-Raum
  zugeordnet: `Top 1 · ? · 13.3 m² (55.4)`.

Beides bleibt im Bild stehen statt geglättet zu werden. Die Zuordnung läuft in
`gesamtdarstellung._stempel_je_raum` über Punkt-in-Polygon von
`Stempel.position_mm` — der Befund liegt aber **vor** der Darstellung, in der
Stempel-Raum-Zuordnung der Erkennung (`stempel_anker.py`). Noch nicht gemessen,
auf wie vielen Plänen das auftritt.

### 4.7 Nachmessung zu 4.6 — mit der echten Zuordnung

Mit `KaskadeErgebnis.zuordnungen` statt Punkt-in-Polygon (Erkennung wie `538d8d8`):

- „BAD/WC" 6,93 m² ist **keinem Raum zugeordnet** (`kein_polygon`); er liegt nur
  geometrisch im 22,5-m²-ZIMMER. Das ZIMMER trägt den Stempel „ZIMMER" 11,89 m²
  (`flutung_unsicher`, +89 %). Die Aussage in 4.6 „BAD/WC sitzt auf dem ZIMMER"
  war ein Artefakt der Darstellung, nicht der Erkennung.
- „Top 1" 55,36 m² → UNBEKANNT 13,3 m² ist bestätigt (`flutung_unsicher`):
  der Wohnungsstempel wird wie ein Raumstempel geflutet.

---

## 5. Ältere offene Entscheidungen (aus der ZERFALL/SCHLITZ-Prüfung)

Dokument: `docs/ZERFALL_SCHLITZ_PRUEFUNG.md` (in `main`, über PR #155).
Vier Owner-Entscheidungen sind dort weiterhin offen:

1. Welche Menge waren die **5,72 m²**? Im Repo nicht reproduzierbar.
2. Ab welcher **freien Breite und Fläche** ist ein Restkörper Nutzfläche?
   Betrifft 59 Flächen / 6,92 m²; die 500 mm sind eine Setzung, das Repo
   definiert keine Begehbarkeitsbreite.
3. Dürfen die **7 (a)-Stücke unter der Rauschschwelle** (Σ 0,945 mm²) als
   zulässig entfallen gelten?
4. Was geschieht mit den **5 (c)-Flächen / 9,471117 m²**? Der Auftrag sagt
   „muss einem Raum zugeschlagen werden" — **zugeschlagen wurde nichts**, das
   wäre eine Änderung in `bereinigung.py`.

---

## 6. Regeln, die in dieser Lane gelten

- **Nichts löschen, immer neue Version danebenlegen.** Keine destruktiven
  git-Operationen (`reset --hard`, `checkout -- .`, `clean -fd`, Force-Push).
- **Guard-Bänder in `tests/naht/`** werden nie aus dem Ist hergeleitet und nie
  hochgezogen. Geht dort ein Test rot: melden, nicht anpassen.
- **`hauptengine/contracts/**` = Approval aller drei Owner** auf dem aktuellen
  `head_sha`; jeder nachgeschobene Commit entwertet ein erteiltes Approval.
- **Kein Wrapper-Exitcode als Beleg** — Testlog lesen. In dieser Arbeit wurde
  zweimal ein `1 failed` nur so gefunden.
- **Jede Kennzahl mit dem Commit-SHA**, auf dem sie erhoben wurde.
- **Nichts erfinden**: keine geschätzten Zahlen, keine ausgedachten Raumtypen.
  Wo eine Zuordnung nicht eindeutig belegbar ist: offenlassen, nicht als
  zulässig deklarieren.

---

## 7. Was als Nächstes ansteht

1. **Owner-Entscheidungen 1–4** aus § 3 einholen. Ohne sie bleibt `47e9e44`
   liegen — der BLOCKER (3. Stock mit 7 Endausgängen) ist sicherheitsrelevant.
2. Danach **Testriegel gegen erfundene Belege** nachziehen (§ 3, Vorbild
   `tests/contract/test_keine_erfundenen_masse.py`) und
   `test_stufe_hoehenkote_nullnah_ist_erdgeschoss` korrigieren — der Test
   zementiert heute den verbotenen EG-Fallthrough.
3. Die Befunde aus § 4 sind **Darstellung, nicht Diagnose** — jeder braucht
   noch eine eigene Messung, bevor er repariert wird.
4. **Kanalfrage**: der Branch hat keinen offenen PR. Ob ein Nachfolge-PR
   aufgemacht wird, entscheidet der Owner.
5. **Rennweg-Befunde** aus `Projekte/_ergebnis_raumerkennung/BERICHT.md` § 2
   priorisieren — vor allem Einraum-„Wohnungen" (8 von 15) und Außenbereiche
   auf Räumen (bis 122,6 m² je Plan). Jeder Befund braucht vor einer Reparatur
   einen Test, der ihn fängt.
6. Weitere Eingangsordner nur mit `--ordner <Name>` rechnen und nicht parallel
   zur Testsuite (MemoryError). Für Barawitzka und Baufeld E2 ist die
   Papierbereich-Drehung offen (2.3).
