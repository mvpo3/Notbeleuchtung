# Normwissen-Übergabe 0908 — Ergebnisbericht

Empfänger: @EnisAMG (normwissen/), @mvpo3 (platzierung/), 3-Owner-Runde
Verfasser: Selman (raumerkennung/)
Stand: 2026-09-09, Branch `selman/extents-ausreisser`
Paket: `C:/Users/selma/Desktop/enis-normwissen-uebergabe-0908-v2` (entpackt vorgefunden)

---

## 1. Kurzfassung

**Was vorliegt.** Enis' Paket v2 ist im Arbeitsbaum: 7 Code-/YAML-Dateien 1:1 übernommen (SHA256 einzeln nachgerechnet), 2 Diffs angewandt. Quell-Commit bei Enis `7ce0d03`, Diff-Basis `4c5df91`, unser Ausgangsstand `ee78ce2`, gesichert im WIP-Commit `a9ab1b6`. Die drei an unsere Lane gerichteten Punkte — natürliche Belichtung, Breitenverlauf des Fluchtwegs, Semantik von `Tuer.breite_mm` — sind auf allen fünf Prüfplänen ausgemessen. Jede Zahl in diesem Bericht stammt aus einem tatsächlich gelaufenen Befehl; alle Zahlen wurden zusätzlich durch einen zweiten, unabhängigen Lauf gegengeprüft, und wo Erstbefund und Verifikation auseinanderfielen, gilt hier die verifizierte Fassung.

**Was entschieden ist.** Nur eines der drei Themen ist Code geworden: `raumerkennung/breitenprofil.py` misst den tatsächlichen Breitenverlauf und ist repariert und getestet (9 passed). Belichtung und Türlichte sind ausgemessen und als Vorschlag formuliert, aber **nicht implementiert** — beide brauchen Felder in `hauptengine/contracts/**`, und der Contract ist eingefroren. Alle Datenmodellangaben in diesem Bericht sind ausdrücklich **VORSCHLAG**, kein Bau.

**Was fehlt.**
- Die Archiv-Prüfsumme des Pakets ist nicht prüfbar (kein `.tar.gz` vorhanden) — Ersatzprüfung siehe § 2.
- Zwei Listeneinträge aus Enis' Diff auf `oib_rl2_tabelle6.yaml` sind bei uns nicht angekommen (§ 3).
- Enis' Test `test_kein_contract_wert_und_kein_konsument` schlug an, weil unser `breitenprofil.py` die RL-4-YAML im Docstring **zitierte** (kein Ladevorgang). Behoben durch Umformulierung der Quellenangabe; Enis' Test selbst unverändert und wieder grün (§ 3.3).
- `breitenprofil.py` hat keinen Produktions-Konsumenten, solange kein Contract-Feld es trägt.
- Die offenen Sachfragen an Enis (Belichtungssemantik, Breitenform im Contract, Türmaß-Zielsemantik) und an Leonis (Verbraucher der Wegbreite, Zusage Platzierung unverändert).

---

## 2. Prüfsummen- und Inhaltsprüfung

### 2.1 Einschränkung: Archiv-Hash nicht prüfbar

Das Paket lag bereits **entpackt** vor; ein `.tar.gz` war nicht vorhanden. Die von Enis genannte Archiv-SHA-256

```
a30221a706df57eaf0c4754583b373e0e984ee7fce8a61bc693dd3a843fe69aa
```

ist deshalb **nicht prüfbar** — nicht widerlegt, sondern mangels Archiv nicht nachrechenbar.

### 2.2 Ersatzprüfung: Einzeldateien

Stattdessen wurden die Einzeldateien gegen die mitgelieferte `SHA256SUMS.txt` geprüft:

| Prüfung | Befehl | Ergebnis |
|---|---|---|
| Paketintegrität | `sha256sum -c SHA256SUMS.txt` | **alle 12 Einträge OK** |
| Übernahme in den Arbeitsbaum | SHA256 der 7 kopierten Dateien einzeln nachgerechnet | **hash-identisch mit dem Paket** |
| Diffs | 2 Diffs angewandt | siehe § 3.2 (eine Teilabweichung) |

### 2.3 Testausgabe zu Enis' Quellenblock (58 Tests)

Lauf mit dem Projekt-venv `D:\KI Projekt\Notbeleuchtung\.venv\Scripts\python.exe` (das System-Python `C:\Program Files\Python310\python.exe` hat kein pytest):

```
..........................................F...............               [100%]
================================== FAILURES ===================================
_________________ test_kein_contract_wert_und_kein_konsument __________________
>       assert treffer == [], treffer
E       AssertionError: ['raumerkennung/breitenprofil.py']
E       assert ['raumerkennu...tenprofil.py'] == []
tests\normwissen\test_quellenblock_e07_rl4.py:183: AssertionError
=========================== short test summary info ===========================
FAILED tests/normwissen/test_quellenblock_e07_rl4.py::test_kein_contract_wert_und_kein_konsument
1 failed, 57 passed in 0.92s
```

**Einordnung.** Kein Sachfehler. Der Test ist ein Wächter „diese YAML hat noch keinen Konsumenten" und prüft per **Textsuche über den Dateiinhalt**, nicht über den Import-/Ladepfad. Getroffen wird `src/notbeleuchtung/raumerkennung/breitenprofil.py`, deren Modul-Docstring (Zeilen 4–7) `normwissen/data/oib_rl4_fluchtwegbreiten.yaml`, Abschnitt `breiten_begriffe`, als Quelle **zitiert**. Ein echter Konsument existiert nicht. **Inzwischen behoben** — siehe § 3.3: Docstring-Quellenangabe umformuliert, Enis' Test unverändert und wieder grün.

### 2.4 Volle Suite

| Lauf | Ergebnis |
|---|---|
| `python -m pytest -q` (Repo-Root, unveränderter Baum) | **1 failed, 1176 passed, 10 skipped, 2 deselected, 9 xfailed** in 1228,44 s |
| `pytest --collect-only -q` | 1196/1198 tests collected |
| `pytest tests/raumerkennung tests/contract -q` | 283 passed, 5 skipped (188,04 s) |
| `ruff check src tests` | All checks passed! |

Der einzige Fehlschlag war der aus § 2.3 und ist behoben (§ 3.3). Nachläufe nach der Korrektur:

| Lauf | Ergebnis |
|---|---|
| `pytest tests/raumerkennung/test_breitenprofil.py tests/normwissen -q` | **353 passed** (34,9 s) |
| `pytest -q` (volle Suite, Repo-Root) | **1177 passed, 10 skipped, 2 deselected, 9 xfailed**, 0 failed (1171,63 s) |

Weitere vorbestehende rote Tests: keine.

---

## 3. Abgleich gegen vorhandenes `normwissen/` und `knowledge/`

### 3.1 Doppelungen

| # | Ort A | Ort B | Art |
|---|---|---|---|
| 1 | `hauptengine/pipeline.py:51` `_AUTO_PRUEF_SCHWELLE = 20` + Hinweistext `:92-99` | `data/astv_arbeitsstaetten.yaml::zwanzig_leuchten` (Z. 305–419) | **Echte Kollision der Bezugseinheit**: Pipeline zählt `len(platzierung.platzierungen)` je **Geschoss**, die Norm (OVE E 8101 560.9.001.AT) meint Sicherheitsleuchten je **zusammenhängendem Gebäudeteil**. Kein Code-Konflikt (die YAML ruft nichts auf). Leonis' Datei — Enis' Vorschlag „Hinweis behalten, als vorläufig kennzeichnen" ist nicht einseitig umzusetzen. |
| 2 | `data/astv_arbeitsstaetten.yaml:307-312` | `data/ove_e07_funktionserhalt.yaml:278-306` | **Paket-interne Doppelung**: OVE E 8101 560.9.2 (max. 20 Leuchten je Endstromkreis, ≤ 60 % Nennstrom) steht wortgleich in zwei neuen Dateien. Redundanz, kein Widerspruch — zwei Pflegeorte. |
| 3 | `astv_arbeitsstaetten.yaml:271` (`⚠_zwei_mal_die_zahl_20`) | `ASTV_E08_ENTSCHEIDUNGSREGELN.md` § 11.1 | **Widerspruch innerhalb des Pakets**: Z. 271 stuft 560.9.001.AT noch als „Ebene D" ein, § 11.1 korrigiert das ausdrücklich auf **Ebene C** (2019 und 2025 wortgleich), und Z. 324 ff. derselben YAML trägt die Korrektur bereits. Z. 271 ist nicht nachgezogen. |

**Themenüberschneidung, sauber abgegrenzt (keine Schlüssel-Kollision):**

| Ort | Gegenstück | Abgrenzung |
|---|---|---|
| `astv_arbeitsstaetten.yaml::ausfuehrung_e08[2]` | `data/en1838_grundwerte.yaml` | E08 5.1 (5 s/50 %, 60 s/100 %, ≥ 60 min, 1 lx) wird nur als **Deckungsvermerk** geführt, nicht als zweiter Wert. |
| `astv_arbeitsstaetten.yaml::ausfuehrung_e08[1]` | `data/sonderstellen.yaml` + `sonderstellen.py` | identische Aufzählung, markiert `status: bestaetigend` / `heute_im_modell: true`. Sonderstellen bleiben auf EN 1838 § 4.1.2 gestützt. |
| `ove_e05_e06_anlagen.yaml::e05` | `oib_rl2_tabelle6.yaml` Z. 11.1 | zwei verschiedene Fragen: E05 = *wie* installieren, OIB = *ob* Sicherheitsbeleuchtung. Nur die OIB-Seite hat einen Verbraucher. |
| `ove_e05_e06_anlagen.yaml::e06` | `en1838_grundwerte.yaml::umschaltzeit` | E06-0,5 s ist ausdrücklich **nicht** die EN-1838-Umschaltzeit; `umschaltzeit_max_s` bleibt 60 s. |

**Kein Konflikt** mit `normwissen/_port_source/*`, `provider.py`, `ove_zusatz.py`, `platzierungsregeln.py`. Die vier neuen YAMLs teilen **keinen Top-Level-Schlüssel** mit einer bestehenden YAML. `knowledge/INDEX.md` führt E-05/E-06/E-07 (Z. 26), E-08 (Z. 40) und die Bildlehren (Z. 30) nur als extrahierte Digests — Quellenverzeichnis, keine Regeln, keine Kollision.

### 3.2 Diff-Konflikte gegen unseren Stand — was erhalten wurde

**Nichts von uns ist verlorengegangen, belegt über Blob-Hashes:**

```
git rev-parse ee78ce2:…/oib_rl2_tabelle6.yaml  →  7c4b21ee9879fcf4f20f6348161e91d0acc07db6
Enis' Diff-Header:                             index 7c4b21e..2decf8e
```

Unsere Basis-Blob ist **identisch** mit Enis' Diff-Basis. Keiner der drei zwischenzeitlichen Commits (`ae9a75a`, `3d60f2b`, `6b9a081`) hat `oib_rl2_tabelle6.yaml` oder `provider.py` seit `4c5df91` verändert. `provider.py`: rekonstruierter Enis-Zielzustand und Arbeitsbaum sind **byteidentisch** (`diff` leer).

**Aber: es ist weniger drin, als geliefert wurde.** Der Ziel-Blob weicht ab (`7c0887c` bei uns vs. `2decf8e` bei Enis). Enis' Diff sauber auf `ee78ce2` angewandt (`APPLY OK`) und gegen den Arbeitsbaum gediffed ergibt genau **eine** Abweichung:

```
@@ -63,8 +63,6 @@   (ausfuehrungs_verweise.eingeschraenkt)
-  - "Bemessungsbetriebsdauer: R 12-2/AC:2019-07-01, Tabelle 5.1 Fußnote a … 1 Stunde gemäß ÖNORM EN 1838 ausreichend …"
-  - "Vorbehalt aus derselben Fußnote a … 'Je nach Nutzung können für besondere Räume und Anlagen weitere Arten der Notbeleuchtung (zB Antipanikbeleuchtung) erforderlich sein.' …"
```

Gegenprobe: `grep -c "Bemessungsbetriebsdauer"` liefert in `ee78ce2`, in `a9ab1b6` und im Arbeitsbaum jeweils **0**.

**Befund:** zwei Listeneinträge unter `ausfuehrungs_verweise.eingeschraenkt` fehlen — der Hunk wurde von Hand nur teilweise übernommen. Beide sind reine Hinweistexte der eingeschränkten Stufe; sie verändern keine Schwelle und keinen Contract-Wert. Nicht blockierend, aber eine Abweichung vom gelieferten Paket. Alle übrigen Hunks (meta-Ausgabenvergleich, `astv_parallelpfad` mit `fundstellen`/`pruefpunkte_kurz`, die 11 R-12-2-Vergleichshinweise, Zeile-10-Texte) sind vollständig angekommen.

### 3.3 Nachtrag — Enis' Konsumenten-Wächter schlug auf unseren Docstring an

`tests/normwissen/test_quellenblock_e07_rl4.py::test_kein_contract_wert_und_kein_konsument`
greppt alle `src/**/*.py` nach den Zeichenketten `ove_e07_funktionserhalt` und
`oib_rl4_fluchtwegbreiten` und verlangt null Treffer. Nach dem Bericht stand ein
Treffer an:

```
AssertionError: ['raumerkennung/breitenprofil.py']
```

Ursache: der **Docstring** von `breitenprofil.py` zitierte die RL-4-YAML wörtlich
mit Dateinamen. Es gab und gibt **keinen Ladevorgang** — das Modul liest die Datei
nicht, importiert nichts aus `normwissen/` und setzt keinen Normwert ein. Der
Wächter prüft Konsum, hier hat er auf eine Quellenangabe in Prosa angeschlagen.

**Behoben** durch Umformulierung der Quellenangabe im Docstring (Verweis auf den
RL-4-Quellenblock in `normwissen/data/` statt auf den wörtlichen Dateinamen).
Enis' Test bleibt **unverändert** und wieder grün — der Wächter ist damit
weiterhin scharf für den Fall, dass ein echter Konsument entsteht.

**Für Enis:** falls die Prosa-Rückverfolgbarkeit wichtiger ist als die
Grep-Genauigkeit, wäre der Wächter besser auf Import-/Ladevorgänge einzugrenzen
(z. B. nur Treffer in `_lade(`/`open(`/`Path(`-Zeilen) statt auf den ganzen
Dateiinhalt. Das ist deine Lane — wir haben den Test nicht angefasst.

---

## 4. Punkt 1 — `natuerlich_belichtet`

### 4.1 Ist-Stand

Das Feld existiert nicht, und es gibt keinen Belichtungs-Code. `grep -rn "natuerlich_belicht\|belicht"` über `src/`, `docs/`, `Handoff/`, `scripts/` ohne `normwissen/` → **0 Treffer**. `Raum` (`hauptengine/contracts/raum_modell.py:66-80`) führt `ist_barrierefrei`, `besondere_gefaehrdung`, `nutzungsklasse`, `wohnung_id` — kein Belichtungsfeld. `CONTRACT_VERSION = "1.3.0"` (Z. 18).

Vier Stellen im Erkennungscode nennen „Fenster", keine davon erkennt eines:

| Datei:Zeile | Inhalt | Bewertung |
|---|---|---|
| `raumerkennung/tueren.py:28` | `_AUSSENTUER = …\|FENSTERT…` | Fenster**tür**-Blöcke werden als Außentür gelesen. Ein Fenster erzeugt nichts. |
| `raumerkennung/wandkoerper.py:37` | `_BAUTEIL_MATERIAL = …\|ALU_GLAS` | einziger Glas-Kanal; landet in `Wandkoerper.material`, wird von keinem Raum-Feld konsumiert. |
| `wandkoerper.py:251-253`, `aussenbereich.py:145` | Aussenkontur „überbrückt Tür-/Fenster-Öffnungen" | Fensteröffnungen werden aktiv zugeschmiert. |
| `tuer_zuordnung.py:170-176` | „Wohnungs-Fensteröffnungen bleiben draußen" | genau die Öffnungen, die der Belichtungsbeleg wären, werden verworfen. |

`dxf_load.py:31-35` (`WALL_PATTERN`) kennt **kein** Fenster-/Glas-Layer-Muster; `material_matching.py:238-245` (`_LAYER_HINWEISE`) keinen GLAS-Hinweis. `ALU_GLAS` (`wissen/materialien.yaml:2-17`, einziges Material mit `bauteilart: GLAS`) trifft nur über die SOLID-Farbsignatur `(4, (0,232,232))`.

**Herkunftskritik zur Materialdatei:** `quellen: [Rennweg]` bezeichnet die Legenden-DXF, nicht den Plan mit dem realen Vorkommen. Gemessene SOLID-Farbzählung: Rennweg_EG `(18)×32, (7)×26, (196,(53,0,106))×2`; Rennweg_OG3 `(255)×11, (18)×6, (196)×2, (7)×2, (9)×1` — die ALU_GLAS-Signatur kommt auf beiden Rennweg-Plänen **0×** vor, auf Muthgasse_E2 **129×** (alle auf Layer `A-WALL-PATT`).

### 4.2 Fensterherkunft je CAD-Familie

| Plan / Familie | Fensterträger | Menge (gemessen) | Besonderheit |
|---|---|---|---|
| **Barawitzka_EG** (ArchiCAD, reine Linien/Hatches) | **keiner** | 0 Layer, 0 Blöcke, **0 INSERTs im Modelspace**, 3 nicht-anonyme Blockdefinitionen | Fenster nicht als Objekt vorhanden. Indirekte Spuren: Layer `…_140 Brüstung`, `…_165 Fassadengestaltung Bänder`, **4 Texte** `Glaswand EI30 + A2` (3×) / `EI60 + A2` (1×). Der Text-Kanal ist kein Barawitzka-Spezifikum: Mollgasse trägt 1, Muthgasse 1 vergleichbaren Text. |
| **Mollgasse_EG** | **Blockname**, direkt im Modelspace | 17 INSERTs: `FENSTER_184-EG` 6, `Fenster Doppelt 196` 5, `FENSTER_120` 2, `FENSTER_204` 2, `FENSTER_214` 1, `Fenstertür-88` 1 | Layer tragen **keinen** Hinweis (`04-SYM-G00-LEG-EP`, `04-STO-G00-LEG-M0`) — eine Layer-Regel greift hier nicht. Einfügepunkt = echte Lage. |
| **Muthgasse_E2** (AIA-Layer) | **Layer + Blockname** | Messskript-Fensterpunkte: `layer:A-GLAZ-CWMG` 455, `block:Fenster 1-flg…` 68+21+2, `layer:A-GLAZ` 27, `layer:A-GLAZ-CURT` 2 → **579**. Modelspace-Layer-Entitäten (unabhängig gezählt): `A-GLAZ-CWMG` 449, `A-GLAZ` 121, `A-GLAZ-IDEN` 109, `A-GLAZ-CURT` 0. `Fenster 1-flg`-INSERTs im Modelspace: 95 | `A-GLAZ-IDEN` (90 MTEXT, 18 INSERT, 1 LINE) ist **Beschriftung** und muss ausgeschlossen werden. Zweiter unabhängiger Kanal: 129 ALU_GLAS-SOLIDs auf `A-WALL-PATT`. |
| **Rennweg_EG** (ArchiCAD) | **INSERT auf `New_Archicad Windows` INNERHALB der `Wall_*`-Blöcke** | 99 `Wall_*`-Blöcke, davon **3** mit Fenstern, **18** Fenster-INSERTs; Familien `Window 27` 11, `Fenster_Halbkreis_Fest` 7 | **Einfügepunkt unbrauchbar:** alle 18 tragen denselben Dummy `(12240439.2 / 356160438.4)`. Die echte Lage steckt in der Geometrie der Blockdefinition (in Weltkoordinaten). |
| **Rennweg_OG3** (ArchiCAD) | dito | 68 `Wall_*`-Blöcke, davon **2** mit Fenstern, **11** Fenster-INSERTs; Familien `2-Flügelfenster 1+1 25` 9, `Window 27` 2 | dito |

**Oberlichter/Lichtkuppeln:** `OBERLICHT|LICHTKUPPEL|SKYLIGHT|DACHFENSTER` liefert auf allen fünf Plänen **0** Treffer (Layer, Blöcke, Texte) und im gesamten Repo 0.

### 4.3 Ist-Zahlen über die fünf Pläne

Messskript: `…/scratchpad/_belichtung_ist.py` (drei Ableitungen, die sich nur in `PLAENE` bzw. Blocktiefe unterscheiden). Datenquelle: **Provider-Lauf über die echten DXF** (`ArchitekturRaumProvider().parse`), nicht die eingecheckten `raeume.json`. Unabhängig nachgemessen: alle Werte bit-genau reproduziert.

| Plan | Räume | True | False | None | FENSTER | TUER_AUSSEN | GLASWAND | OBERLICHT | GEOM_UMSCHL. | KEINE | Fensterpunkte |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Barawitzka_EG | 50 | 20 | 13 | 17 | 0 | 20 | 0 | 0 | 13 | 17 | 0 |
| Mollgasse_EG | 64 | 22 | 36 | 6 | 16 | 6 | 0 | 0 | 36 | 6 | 17 |
| Muthgasse_E2 | 114 | 87 | 27 | 0 | 51 | 36 | 0 | 0 | 27 | 0 | 579 |
| Rennweg_EG | 22 | 7 | 12 | 3 | 5 | 2 | 0 | 0 | 12 | 3 | 18 |
| Rennweg_OG3 | 15 | 5 | 6 | 4 | 4 | 1 | 0 | 0 | 6 | 4 | 11 |
| **Summe** | **265** | **141** | **94** | **30** | **76** | **65** | **0** | **0** | **94** | **30** | **625** |

AUSSEN-Räume (BALKON/TERRASSE, `nutzungsklasse == "AUSSEN"`) und Balkontüren, verifizierte Fassung:

| Plan | AUSSEN-Räume | `tuer_detail == "balkontuer"` |
|---|---:|---:|
| Barawitzka_EG | 9 | 11 |
| Mollgasse_EG | 1 | 0 |
| Muthgasse_E2 | 14 | 35 |
| Rennweg_EG | 2 | 1 |
| Rennweg_OG3 | 1 | 1 |

**Was an diesen Zahlen nicht belastbar ist:**

1. **`GLASWAND` überall 0** ist eine Berichtsform, kein Sachbefund: das Skript meldet den *ersten* Beleg in der Reihenfolge FENSTER > TUER_AUSSEN > GLASWAND > OBERLICHT; auf Muthgasse hatten alle glasbegrenzten Räume bereits einen Fenster- oder Türbeleg. GLASWAND ist als eigenständige Quelle **ungemessen**, nicht „nicht vorhanden".
2. **`TUER_AUSSEN` überzeichnet.** Gezählt wurde `ist_notausgang OR tuer_detail ∈ {balkontuer, hauseingang}`. Barawitzka (106 Türen): 11 `balkontuer` + 1 `hauseingang` + 12 `ist_notausgang` ohne Detail. Eine Notausgangstür ins Freie ist **kein** Belichtungsbeleg — Barawitzkas 20 True stehen allein auf einer Tür-Heuristik.
3. **`False` auf Barawitzka unzulässig.** Die 13 False dort entstehen aus „kein Beleg + keine Außenwandberührung" — bei einem Plan mit null Fensterobjekten ist das fehlende Erhebung, kein belegtes Fehlen. Nach der Regel in § 4.4 müssen alle 50 Barawitzka-Räume `None` sein.
4. **Toleranz nicht kalibriert.** „Beleg liegt am Raum" = Fensterpunkt im 500-mm-Puffer des Raumpolygons. Gesetzt, nicht kalibriert; Außenwände > 500 mm können einen Beleg verlieren.
5. **Rennweg-Koordinatenfalle.** Der erste Lauf ergab Rennweg 0 FENSTER (Dummy-Einfügepunkt, 304 m vom nächsten Raum). Erst die Auswertung der Blockgeometrie ergab 5/4. Mollgasse blieb dabei bit-gleich (22/36/6) — Gegenprobe, dass der Sonderpfad keine andere Familie verschiebt.
6. **Raumzahlen weichen von `Projekte/_ergebnis/*/raeume.json` ab** (dort 48/85/110/21/14): andere Zählebene (`plan_pruefen`, Commit `50f9f40`).
7. **Laufzeit Muthgasse** 608,9 s bzw. 670,2 s im Zweitlauf. Eine im Erstbefund genannte Speicherangabe („7,3 GB Working Set") und eine Laufzeitangabe („> 45 min Abbruch") sind **nicht messbar**: keines der Skripte instrumentiert Speicher (`grep psutil|memory|resource` → kein Treffer), und die Zeitstempel der Session-Artefakte geben ein 45-Minuten-Fenster nicht her. Beide Angaben sind aus diesem Bericht gestrichen.
8. Die im Erstbefund als „rohe Ausgabe" gezeigte Fenster-Herkunft war teilweise von Hand aggregiert. Die Zahlen in § 4.2 sind die verifizierten Werte.

### 4.4 Vorschlag (nicht implementiert)

**`natuerlich_belichtet: bool | None`, Default `None`.**

`True` nur bei positivem Beleg am Raum:

1. Fensteröffnung in einer Außenwand (Fensterobjekt je Familie, § 4.2) im Kontaktband Raum↔Außenwand.
2. Balkon-/Terrassentür (`tuer_detail == "balkontuer"`, oder Tür zu einem Raum mit `nutzungsklasse == "AUSSEN"`). **`ist_notausgang` allein zählt nicht.**
3. Oberlicht/Lichtkuppel — auf keinem Plan vorhanden, Kanal bleibt vorgesehen.
4. Glaskonstruktion `ALU_GLAS` als Wandkörper an der Raumgrenze.
5. AUSSEN-Nachbarfläche über Verglasung.

`False` nur bei belegtem Fehlen:

```
False := belichtung_vollstaendigkeit == VOLLSTAENDIG
         UND kein Beleg 1–5
         UND (keine Außenwandberührung ODER keine Glasfläche an der Außenwand)
```

Ausdrücklich: **nie `False`, nur weil keine Fenster erkannt wurden.**

`None` = Default: Auswertung fehlt, ist unvollständig, oder der Raum hat kein verwertbares Polygon.

**`belichtung_quelle`** — `Literal["FENSTER","TUER_AUSSEN","GLASWAND","OBERLICHT","GEOMETRIE_UMSCHLOSSEN","KEINE"] | None`, Default `None`. Bei mehreren Belegen der stärkste (FENSTER > OBERLICHT > GLASWAND > TUER_AUSSEN); `GEOMETRIE_UMSCHLOSSEN` nur zu `False`, `KEINE` nur zu `None`. Analog zu `Tuer.quelle` (`raum_modell.py:98`).

**`belichtung_vollstaendigkeit`** — `Literal["VOLLSTAENDIG","TEILWEISE","UNGEPRUEFT"] | None`, Default `None`. Eine **Plan-Eigenschaft**, kein Raumurteil, und die einzige Bremse gegen ein falsches `False`:

| Plan | Vorschlag | Begründung (gemessen) |
|---|---|---|
| Muthgasse_E2 | **VOLLSTAENDIG** | zwei unabhängige Kanäle (579 Fensterpunkte + 129 ALU_GLAS-Körper); 0 Räume mit Quelle `KEINE` |
| Mollgasse_EG | **TEILWEISE** | 17 Fensterblöcke bei 64 Räumen, nur ein Blockname-Kanal (Layer ohne Hinweis), 6 Räume `KEINE` |
| Rennweg_EG / OG3 | **TEILWEISE** | Fenster nur in 3/99 bzw. 2/68 `Wall_*`-Blöcken; 18 bzw. 11 Fenster bei 22 bzw. 15 Räumen; Lage nur über den Sonderpfad Blockgeometrie |
| Barawitzka_EG | **TEILWEISE** (neu, § 4.5; vorher UNGEPRUEFT) | ein tragender Kanal: 24 Fensteröffnungen über die Rahmen-/Scheiben-Signatur, 0 Falschtreffer auf den vier Vergleichsplänen. Kein zweiter Kanal, kein Referenzbestand auf diesem Plan, 4 `Glaswand`-Texte unerfasst → nicht VOLLSTAENDIG, `False` bleibt dort ausgeschlossen |

Contract-Folge (**VORSCHLAG**, siehe § 8): drei additive Felder in `Raum`, alle Default `None`, `CONTRACT_VERSION` 1.3.0 → 1.4.0, Schema-Regenerierung `scripts/gen_schema.py`. Kein Erzeuger bricht. Ob `belichtung_vollstaendigkeit` besser auf `RaumModell`-Ebene sitzt (es ist eine Plan-Eigenschaft), ist eine Owner-Entscheidung und hier bewusst offen gelassen.

### 4.5 Punkt 5 — Fensterdarstellung in der Barawitzka-Familie

Ausgangsfrage: Barawitzka trägt kein Fensterobjekt (§ 4.2). Trägt stattdessen
ein **Erscheinungsbild**? Geprüft wurden sechs Hypothesen; fünf tragen nicht,
eine trägt.

#### 4.5.1 Geprüfte Hypothesen

| Hypothese | geprüft wie | Ergebnis (gemessen) |
|---|---|---|
| **A — Layer `…_140 Brüstung`** | alle Entities des Layers, Länge/BBox/Linetype je Entity (`_bara_layer.py`, `_bara_geo.py`) | **trägt nicht.** 123 Entities (LWPOLYLINE 64, LINE 35, WIPEOUT 17, HATCH 7), aber nur **2 räumliche Cluster** auf dem ganzen 20 × 34 m-Grundriss: (6.8–11.0 / −22.5) und (15.1 / −17.1…−15.1). Linetype `Untersicht`, Bauteiltiefen 120/190 mm → Geländer-/Absturzsicherungsdetail, kein flächendeckender Fensterkanal. |
| **B — Layer `…_165 Fassadengestaltung Bänder`** | dito | **trägt nicht.** 21 Entities = 3 Objekte: eine 18.985 × 0.850 m LWPOLYLINE (Fassadenband/Vordach), eine 5.890 × 0.470 m SOLID-Fläche, ein 150 × 50 mm Detail bei (12.19 / −21.5). Keine Wiederholung entlang der Fassade. |
| **C — Glaskonstruktion laut `wissen/materialien.yaml` (ALU_GLAS, SOLID-Farbsignatur `(4,(0,232,232))`)** | `bestimme_material(signatur_aus_hatch(h), layer=…)` über alle HATCHes aller 5 Pläne (`_bara_alu.py`) | **trägt auf Barawitzka nicht — Vorbefund § 4.1 verifiziert.** Alle 5162 HATCHes sind `SOLID`, `bestimme_material` liefert **5162× `UNBEKANNT`**, `ALU_GLAS` **0×**. Gegenwert Muthgasse_E2: **129×**; Mollgasse / Rennweg EG / OG3 je 0. |
| **D — eigenes Hatch-Muster oder eigene Linienart für Glas** | `Counter(pattern_name)`, `Counter(linetype)` (`_bara_alu.py`) | **trägt nicht.** Hatch-Muster ausschließlich `SOLID` (5162). Linetypes: `Continuous 29940, Untersicht 905, Schnittlinie 645, Wipeout_Contour 334, Achse 245, Strichlinie eng 139, Baufluchtlinie 126, Punkt 1_1 118, Untersicht 1_1 89, Dampfsperre 35` — **keine Glas-/Verglasungs-Linienart**. |
| **E — Wandunterbrechung allein (Öffnung ohne Objekt)** | `finde_wandkoerper` → Union der 595 Außenwandkörper, morphologisches Closing `buffer(800).buffer(-800)`, Differenz = Lücken; Inhalt je Lücke nach Layer/Typ (`_bara_oeffnung.py`, `_bara_inhalt.py`) | **trägt allein nicht.** 174 Rohlücken → 33 formplausible Kandidaten (Kurzseite 80–700 mm, Länge 300–6000 mm), Inhalt unspezifisch (Bodenaufbau, Bemaßung, Entwässerung). Zusätzlich schließt `d = 800 mm` Öffnungen > 1600 mm nicht — das Verfahren übersieht gerade die breiten Fenster. |
| **F — Rahmenpaar mit parallelen Scheibenlinien in der Wandunterbrechung** | Entity-Dump einzelner Öffnungen (`_bara_dump.py`), Renderings (`_bara_render.py`), dann Detektor über alle 5 Pläne | **trägt.** § 4.5.2 |

#### 4.5.2 Das tragende Muster

Entity-Dump einer einzelnen Wandöffnung, Layer `0._EG PP_2_110 Wand Aussen`:

```
Element A  Rahmenrechteck  x 0.600–1.927 , y −14.870 / −14.780   (1327 × 90 mm)
           Innenlinien     y = −14.835 und −14.815               (Abstand 20 mm, volle Länge 1.328 m)
           kein ARC        →  reines Fenster
Element B  Rahmenrechteck  x 2.148–2.835 , y −14.845 / −14.755   ( 687 × 90 mm)
           Innenlinien     y = −14.810 und −14.790               (Abstand 20 mm, volle Länge 0.688 m)
           ARC center=(2.925,−14.755) r=868 mm  →  Fenster-/Balkontür
```

Die Wandschraffur (SOLID-HATCH) ist an diesen Stellen unterbrochen; die
Elemente liegen in der Lücke. Daraus die Signatur (implementiert in
`raumerkennung/fenster_signatur.py`):

1. **Wand-Layer**, Hauptvariante des Plans (`WALL_PATTERN` + `_varianten_prefix`);
   Segmente aus `LINE`/`LWPOLYLINE`, ≥ 100 mm, in mm.
2. **Rahmenpaar**: zwei parallele Segmente (Winkeltoleranz 1°), Normalabstand
   **80–100 mm** (`RAHMEN_MM`; gemessen 80/81/90 mm), Längsüberlappung
   **≥ 300 mm** (`MIN_LAENGE_MM`).
3. **Scheiben**: **≥ 2** weitere parallele Segmente mit Normalabstand zwischen
   15 % und 85 % der Rahmentiefe, Längsüberlappung ≥ 60 % der Rahmenlänge
   (gemessener Scheibenabstand durchweg 20 mm).
4. **Öffnungsbedingung**: Mittelpunkt liegt **nicht** in der Union der
   Wandkörper (`finde_wandkoerper` → `unary_union`), also in der
   Wandunterbrechung statt in geschlossener Wand.
5. **Clustern**: < 200 mm Mittelpunktsabstand = ein Element.
6. **Türabgrenzung**: `ARC` mit Radius 500–1500 mm, Zentrum ≤ halbe
   Öffnungsbreite + 400 mm → `hat_tuerbogen = True` (Fenster-/Balkontür).

**Ausbeute Barawitzka_EG** (`_p6_fenster.py`, Modulfunktion
`finde_fensteroeffnungen`): 1689 gescannte Wandsegmente → **24 Fensteröffnungen**,
**alle 24 auf `0._EG PP_2_110 Wand Aussen`**, Rahmentiefen {80, 81, 90} mm.
Öffnungsbreiten in mm:
`305, 310, 400, 442, 455, 460, 460, 460, 460, 688, 700, 700, 700, 700, 700, 700, 755, 760, 760, 905, 960, 960, 1185, 1328`.
Davon **13 mit Türbogen** (Fenster-/Balkontür), **11 ohne** (reines Fenster).
Räumliche Verteilung: drei Fassadenabschnitte (y ≈ −15, −21.5, −30/−31.5);
Nord-, Ost- und Westwand tragen 0 Kandidaten — die Nordwand ist im Rendering
durchgehend schraffiert mit zwei Türbögen (Hauseingänge), also fensterlos.
Konsistent mit einem Baulücken-EG.

#### 4.5.3 Gegenprobe auf den vier anderen Plänen

Referenzbestand = Fenster-INSERTs (`FENSTER|WINDOW|GLAZ|VERGLAS`, Blockabstieg
Tiefe ≤ 3) + Entities auf `*GLAZ*`-Layern ohne `IDEN`. „Falschtreffer" =
Kandidat ohne Referenzfenster im 1000-mm-Umkreis.

| Plan | gescannte Wandsegmente | Treffer | Referenzfenster | **Falschtreffer** |
|---|---:|---:|---:|---:|
| Barawitzka_EG | 1689 | **24** | 0 (keine vorhanden) | nicht kreuzvalidierbar |
| Mollgasse_EG | 930 | **0** | 17 | **0** |
| Muthgasse_E2 | 3155 | **0** | 5126 | **0** |
| Rennweg_EG | **0** | 0 | 464 | 0 — s. u. |
| Rennweg_OG3 | **0** | 0 | 604 | 0 — s. u. |

Die Signatur erzeugt auf keinem der vier anderen Pläne einen Treffer:
**0 Falschtreffer**. Sie ist Barawitzka-spezifisch, aber nicht schädlich.

**Warum die volle Signatur nötig ist** — zwei Zwischenstufen, gemessen und
verworfen:

- **Nur Scheiben-Doppellinie (15–25 mm), ohne Rahmenpaar** (`_glasdoppel.py`,
  `_kreuz.py`): Barawitzka 25 Cluster, Mollgasse 9, Muthgasse 32.
  Kreuzvalidierung: Mollgasse **0 von 9** ≤ 2000 mm an einem echten
  Fensterblock; Muthgasse **9 von 32** ≤ 500 mm an einem GLAZ-Punkt →
  überwiegend Falschtreffer (Wandaufbau-Schichtlinien).
- **Doppellinie + Öffnungsbedingung, ohne Rahmenpaar** (`_kreuz2.py`):
  Mollgasse 8 Cluster, **0** an einem Referenzfenster; Muthgasse 16 Cluster,
  **3** an einem Referenzfenster. Immer noch überwiegend falsch.
- Gap-Histogramm über Barawitzka bei geöffnetem Fenster 3–80 mm
  (`_gap_hist.py`): `5 mm:80, 25:12, 65:16, 75:15, 50:11, 12:10 …` — der
  20-mm-Scheibenabstand ist im Wandaufbau kein Alleinstellungsmerkmal. Erst
  das 90-mm-Rahmenpaar macht die Signatur eindeutig.

**Einschränkung Rennweg (wichtig):** `wandsegmente()` liefert auf Rennweg_EG
und Rennweg_OG3 **0 Segmente** — die Wände stecken dort in den
`Wall_*`-Blockdefinitionen, die der Scan nicht betritt. Die 0 in der Tabelle
heißt für Rennweg **„nicht gesucht", nicht „nicht vorhanden"**. Für Mollgasse
und Muthgasse (930 bzw. 3155 gescannte Segmente) ist die 0 ein echter Befund.

**Nicht erfasster Restkanal auf Barawitzka:** die 4 `Glaswand`-Texte liegen bei
(14.94 / −16.40), (12.46 / −16.67), (13.78 / −20.98), (14.80 / −0.83). Abstand
zum jeweils nächsten Kandidaten: **10586, 9565, 5993, 3034 mm** — die
Rahmensignatur erfasst sie **nicht**. Diese 4 Glaswände bleiben ein eigener,
ungemessener Kanal.

#### 4.5.4 Was gebaut ist — und was ausdrücklich nicht

Gebaut: `src/notbeleuchtung/raumerkennung/fenster_signatur.py` mit
`wandsegmente(plan)`, `finde_rahmenfenster(segmente, wandflaeche)` (rein
geometrisch, ohne DXF) und `finde_fensteroeffnungen(plan)`; Rückgabetyp
`Fensteroeffnung` (Modul-eigen). Tests:
`tests/raumerkennung/test_fenster_signatur.py`, 7 Fälle auf synthetischer
Geometrie, jeder gegen die zurückgebaute Regel rot geprüft (§ 4.5.5).

**Kein Contract-Touch.** Die drei Belichtungsfelder (§ 4.4) bleiben VORSCHLAG;
der Owner hat für diesen Punkt keine Contract-Änderung beauftragt. Die
Erkennung ist deshalb ohne Contract-Feld messbar und prüfbar — sie schreibt
nichts an `Raum`.

Was `None` mit Quelle `UNBEKANNT` bleiben muss, weil es nicht gemessen ist:

- die **Zuordnung der 24 Öffnungen zu Räumen** (kein Provider-Lauf, keine
  Kontaktband-Prüfung Raum↔Außenwand durchgeführt),
- die **4 Glaswände** (eigener, unerfasster Kanal),
- ob die 24 den Fensterbestand des EG **vollständig** abdecken — auf
  Barawitzka gibt es keinen unabhängigen Referenzbestand, gegen den sich das
  prüfen ließe.

Daraus die Höherstufung Barawitzka `UNGEPRUEFT` → **TEILWEISE** (§ 4.4),
nicht `VOLLSTAENDIG`: § 4.3 Punkt 3 gilt unverändert, `False` bleibt auf
Barawitzka ausgeschlossen. Die übrigen vier Pläne behalten ihre Stufe — die
Signatur fügt dort nichts hinzu (0 Treffer), und für Rennweg ist sie nicht
geprüft, also kein Grund zur Höherstufung.

#### 4.5.5 Läufe

```
.venv/Scripts/python.exe -m pytest tests/raumerkennung/test_fenster_signatur.py -q -p no:randomly
7 passed in 1.09s
```

Rot-Probe (`_p6_rot.py`, jede Regel einzeln zurückgebaut):

```
== SCHEIBEN_MIN = 0 ==            ohne_scheibenlinien: ROT | eine_scheibenlinie: ROT
== RAHMEN_MM = (10, 1000) ==      falsche_rahmentiefe: ROT
== Oeffnungsbedingung aus ==      in_geschlossener_wand: ROT
== MIN_LAENGE_MM = 100 ==         zu_kurz: ROT
```

---

## 5. Punkt 2 — Breitenverlauf

### 5.1 Was umgesetzt ist

`src/notbeleuchtung/raumerkennung/breitenprofil.py` (+ `tests/raumerkennung/test_breitenprofil.py`). Umfang: `git diff --stat` = **2 Dateien, +62/−21**, ausschließlich in `raumerkennung/`, **kein Contract-Touch**.

Vorgefunden war das Modul inhaltlich vollständig, aber auf realen Plänen nicht lauffähig — Suite rot:

```
......F                                                                  [100%]
E       AssertionError: assert False
E        +  where False = Breitenprofil(segment_id='seg_z', …, messbar=False, grund='nur_tuer_oder_eckpunkte').messbar
FAILED tests/raumerkennung/test_breitenprofil.py::test_skelett_zickzack_gilt_nicht_als_richtungswechsel
1 failed, 6 passed in 4.15s
```

Drei Ursachen und ihre Behebung:

| Befund | Ursache | Fix |
|---|---|---|
| Suite rot | `_innere_vertex_laufmeter` maß den Knick zwischen *benachbarten* Stützpunkten; ein Skelett-Zickzack von 20 mm auf 200 mm ergibt 22,6° > `ECKE_MIN_GRAD=20` → jeder Stützpunkt galt als Ecke | Knick über ein Fenster `ECKE_FENSTER_MM = 500` (Sehne via `linie.interpolate`) |
| Eckfenster fraß reale Profile | `_markiere` setzte das Ausblendfenster gleich der an der Ecke gemessenen, dort aufgeblähten Breite. Gemessen an `Rennweg_EG/seg_graph_durchgang_18`: **60 von 68** Punkten verworfen, Segment nicht messbar | Eckfenster = `min(lokale Breite, Median aller Breiten / 2)` |
| Schiefe Normale | `_richtung` nahm die lokale Segment-Tangente; ±20 mm Skelett-Wackeln kippen sie um 11,3°, Breite systematisch zu groß (1200 → 1223,8 mm) | Einheits-Tangente als Sehne über dasselbe Fenster; Restfehler 1200,8 mm |

Wirkung der Änderung (messbare Segmente, vorher → nachher, jeweils gegen das HEAD-Modul gemessen):

| Plan | vorher | nachher |
|---|---:|---:|
| Barawitzka_EG | 11 | 12 |
| Rennweg_EG | 3 | 6 |
| Mollgasse_EG | 84 | 86 |
| Mollgasse, Variante „nur Median-Deckel ohne `min()`" | — | 81 |

Die `min()`-Kombination ist also nötig: ein reiner Median-Deckel hätte Mollgasse auf 81 gedrückt.

Weiter umgesetzt: `Abschnitt.quelle: str = "gemessen"` (Audit-Trail, nie ein Normwert), `_median` nach oben gezogen, zwei neue Tests (`test_abschnitt_traegt_quelle_gemessen`, `test_ecke_in_einen_saal_loescht_nicht_das_ganze_profil`).

Nicht angefasst: der Zweig `wandkante_fehlt` (`breitenprofil.py:193-194`, `breite >= 2*reichweite - 1e-6`) ist bei geschlossenen Shapely-Polygonen unerreichbar; er bleibt als Guard stehen, ohne erfundenen Test.

Testausgabe danach:

```
.........                                                                [100%]
9 passed in 1.34s
```

Regression: `pytest tests/raumerkennung tests/contract -q` → `283 passed, 5 skipped in 188,04s`. `ruff check src tests` → `All checks passed!`

**Kein Normwert im Modul.** Einzige Zahlkonstanten: `SCHRITT_MM 100`, `TOLERANZ_MM 100`, `MIN_ABSCHNITT_MM 500`, `TUER_RADIUS_MM 400`, `ECKE_MIN_GRAD 20`, `ECKE_FENSTER_MM 500` — Messparameter. Kein Default und kein Mittelwert ersetzt eine fehlende Messung; `_median` läuft nur über tatsächlich gemessene Werte.

**Anbindung: es gibt keine.** `grep -rn "breitenprofil\|Breitenprofil" --include=*.py` findet außerhalb von Modul und eigenem Test genau einen Treffer, und der ist eine Textprüfung am Normwissen-YAML (`tests/normwissen/test_quellenblock_e07_rl4.py:328`), keine Code-Anbindung. Der Provider ruft das Modul nicht. Zur Anbindung fehlt (a) ein Feld am `FluchtwegSegment` (§ 5.5) und (b) im Provider die Zuordnung Segment → durchlaufene Raumpolygone + zugehörige Türen, die für die Messung im Skript nachgebaut wurde.

### 5.2 Darstellung

Die drei Breitenbegriffe aus `oib_rl4_fluchtwegbreiten.yaml::breiten_begriffe` werden im Modul getrennt gehalten:

| Größe | Im Modul | Zulässige Verwendung |
|---|---|---|
| erforderliche Mindestbreite (OIB RL 4, **Fertigmaß**) | kommt nicht vor | nur Vergleichsmaßstab in `normwissen/`, **nie** Eingang der Lichtrechnung |
| örtliche Engstelle | `engstellen` mit `position_mm`/`breite_mm`/`laenge_mm`, plus `breite_min_mm` | Prüfung gegen die Mindestbreite. **Nicht** als Breite des Abschnitts — das würde breitere Bereiche aus der Bewertung entfernen, wo EN 1838 § 4.2.1 Satz 3 Streifenbetrachtung oder Antipanik verlangt |
| tatsächliche Breite entlang des Weges | `breitenprofil` (Abtastung alle 100 mm) und `abschnitte` konstanter Breite (Toleranz 100 mm, Mindestlänge 500 mm, Median statt Mittelwert, zu kurze Läufe an den Nachbarn, nie ein gemischter Wert) | **einziger** zulässiger Eingang der Lichtrechnung |

Ergänzend: `tuerpunkte` als eigene Liste (gehen weder in `abschnitte` noch in `breite_min_mm`), `breite_messbar` + `grund` statt Ersatzwert.

### 5.3 Ist-Zahlen je Plan

Skript `…/scratchpad/_breitenprofil_ist.py` (ArchitekturRaumProvider → `modell.zirkulation.segmente`; Fläche = alle `Raum.polygon_mm`, die das Segment schneiden).

**Korrektur gegenüber dem Erstlauf:** das Skript rief `parse(..., "EG")` **hartkodiert für alle fünf Pläne**. `geschoss_aus` (`tuer_typisierung.py:65-73`) nimmt den `floor`-Parameter vor dem Dateinamen, d. h. Rennweg_OG3 wurde als Erdgeschoss verarbeitet (`ist_erdgeschoss` True statt False, final_exit- statt stair_exit-Logik). Nur Rennweg_OG3 ist betroffen; Muthgasse_E2 mit `floor=""` gegengeprüft: unverändert 155/102/44/9. Die Tabelle zeigt die korrigierte Fassung.

| Plan | Segmente | messbar | nicht messbar | Achse n. ermittelbar | `flaeche_fehlt` | `wandkante_fehlt` | `nur_tuer_oder_eckpunkte` | s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Barawitzka_EG | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 10,4 |
| Mollgasse_EG | 126 | 86 | 40 | 0 | 17 | 0 | 23 | 34,4 |
| Muthgasse_E2 | 155 | 102 | 53 | 0 | 44 | 0 | 9 | 663,9 |
| Rennweg_EG | 9 | 6 | 3 | 0 | 0 | 0 | 3 | 2,9 |
| Rennweg_OG3 | 5 | 3 | 2 | 0 | 0 | 0 | 2 | nicht messbar\* |
| **Summe** | **307** | **209 (68,1 %)** | **98** | **0** | **61** | **0** | **37** | |

\* Der korrigierte OG3-Lauf lief über `_floor_check.py`, das keine Zeit ausgibt — Laufzeit **nicht messbar**, wird nicht geschätzt. Der fehlerhafte Lauf mit `floor="EG"` ergab 6/2/4 in 2,1 s.

Gründe, Lesart:

- `flaeche_fehlt` (61) = kein erkanntes Raumpolygon schneidet die Segmentachse. Erkennungslücke, entspricht „Raum nicht geschlossen" — **unsere Lane**, nicht die Breitenmessung.
- `nur_tuer_oder_eckpunkte` (37) = jeder Abtastpunkt ist Türdurchgang oder liegt im Eckfenster, also keine gültige Gangbreite. Bei GRAPH-Segmenten, die diagonal Tür-zu-Tür durch Räume laufen, fachlich korrekt „keine Gangbreite".
- `achse_nicht_ermittelbar` und `wandkante_fehlt` kamen auf keinem der fünf Pläne vor.

### 5.4 Belegprofile

Voll: `…/scratchpad/_profil_barawitzka.txt`, `…/scratchpad/_profil_mollgasse.txt`. Beide unabhängig neu erzeugt und byteidentisch reproduziert.

| Segment | Länge mm | Messpunkte | ECKE | TUER | ohne Messung | `breite_min_mm` |
|---|---:|---:|---:|---:|---:|---:|
| Barawitzka_EG · `seg_graph_durchgang_11` | 20242,7 | 204 | 140 | 4 | 6 | 712,5 |
| Mollgasse_EG · `seg_graph_durchgang_17` | 26757,7 | 269 | 234 | 8 | 8 | 1335,8 |

**Barawitzka_EG · `seg_graph_durchgang_11`:**

```
ABSCHNITTE   10000.0 – 12150.0 : 1420.0 mm (gemessen)
             12150.0 – 15250.0 : 1210.0 mm
             15250.0 – 17450.0 : 1505.0 mm
             17450.0 – 19900.0 : 1755.0 mm
ENGSTELLEN   10000.0 : 1210.0 mm / 100.0 mm lang   ·   19900.0 : 712.5 mm / 100.0 mm
TUERPUNKTE   0.0:1407.6  ·  3700.0:571.0  ·  6700.0:392.1  ·  20000.0:496.2
```

**Mollgasse_EG · `seg_graph_durchgang_17`:**

```
ABSCHNITTE   13200.0 – 14950.0 : 1335.8 mm (gemessen)
             14950.0 – 15600.0 : 7153.1 mm
ENGSTELLEN   (keine)
TUERPUNKTE   0.0:4721.2 · 13700.0…14200.0:1335.8 (6 Punkte) · 26757.7:1126.7
```

Vorbehalt zum Mollgasse-Beleg: die Abschnitte decken nur 2,4 m von 26,8 m ab, weil **234 von 269** Punkten im Eckfenster liegen — das Segment ist ein Tür-zu-Tür-Weg quer durch weite Räume, kein Gang. Das ist die verbleibende Hauptschwäche der Abdeckung, keine Fehlmessung.

### 5.5 Contract-Darstellung (VORSCHLAG, nicht implementiert)

Rein additiv an `FluchtwegSegment` in `hauptengine/contracts/raum_modell.py`, gleiche Machart wie `Tuer.quelle`/`untypisiert_grund` in v1.3.0 — jedes Feld hat einen Default, kein Erzeuger und keine Fixture bricht:

```python
class BreitenAbschnitt(BaseModel):
    von_m: float
    bis_m: float
    breite_mm: float
    quelle: str = "gemessen"          # Audit-Trail; NIE ein Normwert

class BreitenEngstelle(BaseModel):
    position_m: float
    xy_mm: XY
    breite_mm: float
    laenge_mm: float

class FluchtwegSegment(BaseModel):
    ...                                # unverändert
    # v1.4.0 — tatsaechlicher Breitenverlauf. ALLES optional:
    # None = nicht gemessen, [] = gemessen ohne Fund. Beides ist NICHT 0.
    breitenprofil: list[tuple[float, float]] | None = None   # (laufmeter_m, breite_mm)
    abschnitte: list[BreitenAbschnitt] = Field(default_factory=list)
    engstellen: list[BreitenEngstelle] = Field(default_factory=list)
    breite_min_mm: float | None = None
    breite_messbar: bool | None = None      # None = nicht versucht
    breite_grund: str | None = None
```

Optionalität konkret: (a) Skalare `| None = None` statt `0.0` — ein fehlender Wert darf nie als „0 mm breit" oder als Normwert lesbar sein; (b) Listen mit `default_factory=list`, `[]` = „gemessen, keine Engstelle", unterschieden von „nie gemessen" über `breite_messbar`; (c) `breite_messbar` dreistufig; (d) `contract_version` 1.3.0 → 1.4.0 plus `python scripts/gen_schema.py`, sonst Drift-Gate rot. Kollisionsgeprüft: `FluchtwegSegment` hat heute kein Feld `abschnitte`/`engstellen`/`breitenprofil`; `quelle` ist am Segment bereits als `Literal["LINIE","GRAPH","FALLBACK"]` belegt — der Vorschlag setzt `quelle` nur auf `BreitenAbschnitt`.

---

## 6. Punkt 3 — `Tuer.breite_mm`

`Tuer.breite_mm: float = 0.0` (`hauptengine/contracts/raum_modell.py:86`). **Neun** Code-Pfade schreiben in dieses eine Feld:

| # | Datei:Zeile | Wie die Zahl entsteht | Was sie physikalisch ist |
|---|---|---|---|
| 1 | `tueren.py:68` → `_breite_mm()` `:45-58` | erste Zahl im Blocknamen, 60–130 → ×10, oder 600–1300 direkt | Nennmaß aus dem Namen |
| 2 | `tueren.py:80/83` (`_arc_tueren`) | `radius * plan.factor` | **Schwenkradius** des Türblatt-ARC |
| 3 | `tueren.py:141` (`tuer_oeffnungen`) | `_breite_mm(name) or _blattbreite_aus_block(e, factor)` (`:110-126`) | Nennmaß **oder** ARC-Radius |
| 4 | `tueren.py:156` | freistehender ARC im `_walk`, auch in Blockdefinitionen | Schwenkradius |
| 5 | `tueren.py:204` (`aussentor_tueren`) | ARC-Radius aus `TuerOeffnung` | Schwenkradius |
| 6 | `tueren.py:259` (`verschmelze_doppelfluegel`) | `t1.breite_mm + t2.breite_mm` | **Summe zweier Schwenkradien** |
| 7 | `tueren.py:309` (`text_tueren`) | fest `0.0` | **keine Messung** |
| 8 | `tuer_zuordnung.py:157` / `:218` | Langseite des `minimum_rotated_rectangle` der freien Kontaktzone | gemessene **Wandöffnung (Rohbaulichte)** |
| 9 | `provider.py:92` | `Tuer(… breite_mm=o.breite_mm …)` aus `k.tueroeffnungen`, wenn `tueren_aus_dxf` leer ist | **der Rennweg-Pfad** (EG + OG3 = 68 der 629 Türen) |

**Präzisierung zur Aufgabenformulierung:** Der Code misst bei Bogen-Türen **nicht die Sehne**, sondern den **Radius** (`tueren.py:80/83`; `tests/raumerkennung/test_tueren.py:36` sagt wörtlich „Breite = Schwenkradius"). Die Sehne eines 90°-Bogens wäre r·√2. Der Radius entspricht der Türblattbreite — sachlich richtiger als die Sehne, aber ein Wertename `GEOMETRIE_SEHNE` wäre irreführend; unten daher `GEOMETRIE_SCHWENKRADIUS`.

`ATTRIBUT` kommt heute nirgends vor — kein Code liest DXF-ATTRIBs für die Breite. `STANDARDWERT` existiert genau einmal, außerhalb des Contracts: `hauptengine/render/dxf_renderer.py:524` `breite = t.breite_mm or 900.0` — der Renderer erfindet still 900 mm (`grep -rn "or 900" src scripts` → genau ein Treffer).

### 6.1 Frage 1 — Ist die Herkunft je Tür nachvollziehbar? → **Nein.**

`Tuer.quelle` (`raum_modell.py:98`) trägt die **Erkennungs**-Quelle, nicht die Herkunft der Breite. `quelle="block"` steht sowohl für Pfad 1 (Nennmaß aus dem Namen) als auch für Pfad 3 (ARC-Radius aus der Blockdefinition, wenn `_breite_mm` nichts fand — das `or` in `:141`). Aus dem Modell allein nicht entscheidbar. `quelle="doppelfluegel"` sagt nicht, dass die Breite eine Summe ist. Zusätzlich überschreiben `tuer_typisierung.py:191` und `:241` das Feld (`f"{t.quelle}+text:…"`, `"+windfang"`) — `quelle` ist bereits ein zusammengesetzter Audit-String, kein Enum.

Messung je Plan (`…/scratchpad/_tuer_quelle_ist.py`, Herkunft durch Instrumentierung von `tueren._blattbreite_aus_block` rekonstruiert; unabhängig nachgelaufen, Zeile für Zeile identisch):

| Plan | Türen | GEOM_OEFFNUNG | GEOM_SCHWENKRADIUS | GEOM_SUMME | BLOCKNAME | keine Messung (0.0) |
|---|---:|---:|---:|---:|---:|---:|
| Barawitzka_EG | 106 | 68 | 36 | 2 | 0 | 0 |
| Mollgasse_EG | 147 | 76 | 27 | 0 | 40 | 4 |
| Muthgasse_E2 | 308 | 162 | 1 \* | 0 | 18 \* | 127 |
| Rennweg_EG | 41 | 30 | 10 | 0 | 0 | 1 |
| Rennweg_OG3 | 27 | 24 | 3 | 0 | 0 | 0 |
| **Summe** | **629** | **360 (57 %)** | **77 (12 %)** | **2** | **58 (9 %)** | **132 (21 %)** |

\* **Strittig / auf ±1 unsicher:** die Aufteilung BLOCKNAME/SCHWENKRADIUS bei `quelle="block"` beruht auf einem Positions-Match ±1 mm plus Wert-Toleranz 1,5 mm. Für Mollgasse deckt sie sich exakt mit dem unabhängigen DXF-Scan (40 = 40). Für Muthgasse nicht: der Scan zählt 19 Blöcke mit Namensbreite, das Modell 18 BLOCKNAME + 1 GEOMETRIE_SCHWENKRADIUS.

Vier Herkünfte plus „keine Messung" im selben Feld, ohne Unterscheidungsmerkmal. Enis' Befund (`oib_rl4_fluchtwegbreiten.yaml::tuerbreite_herkunft`, „mindestens drei Bedeutungen") ist am Ist-Stand **bestätigt und um eine vierte erweitert** — die Doppelflügel-Summe.

**Vorschlag `breite_quelle`** (nicht implementiert):

```python
BreiteQuelle = Literal[
    "BLOCKNAME",                # tueren.py:45 — Nennmass aus dem Namen
    "GEOMETRIE_SCHWENKRADIUS",  # ARC-Radius (tueren.py:83, :118, :156, :204)
    "GEOMETRIE_SUMME",          # verschmelze_doppelfluegel
    "GEOMETRIE_OEFFNUNG",       # tuer_zuordnung.py:157/:218 — Wandoeffnung
    "ATTRIBUT",                 # heute unbenutzt, reserviert
    "STANDARDWERT",             # heute nur dxf_renderer.py:524 — gehoert nicht ins Modell
    "UNBEKANNT",
]
```

### 6.2 Frage 2 — Ist die nutzbare Durchgangslichte bekannt? → **Nein**, mit einer Einschränkung.

Keiner der heutigen Werte **ist** die Lichte:

- **BLOCKNAME (58):** Bestell-/Nennmaß. Ob 80 cm Zargenlichte, Blattbreite oder Rohbau gemeint ist, sagt der Name nicht.
- **GEOMETRIE_SCHWENKRADIUS (77):** Türblattbreite. Die Lichte bei 90° geöffnetem Blatt ist kleiner (Anschlag, Blattdicke, Zargenfalz) — um wie viel, steht im Plan nicht. **Keine belegte Umrechnung.**
- **GEOMETRIE_OEFFNUNG (360, die Mehrheit):** Rohbauöffnung ohne Zarge, systematisch **größer** als die Lichte. Genau die Richtung, vor der Enis warnt („fiele systematisch zu günstig aus").
- **GEOMETRIE_SUMME (2):** zwei Radien ohne Abzug des Mittelstoßes.

**Einschränkung, ausdrücklich als strittig gekennzeichnet:** bei den 18 Muthgasse-BLOCKNAME-Türen tragen die Blocknamen selbst DL-Notation (`…_1DF_90x200`, `… - DL - 800 x 2490`, DL = Durchgangslichte), und `_breite_mm()` zieht die 900/950 genau daraus (`7x …_1DF_90x200 → 900.0`, `5x …_1DF_95x200 → 950.0`). Wenn die DL-Lesart dieser Namen gilt, ist `breite_mm` dort die Durchgangslichte, und die Aussage „in keinem der 629 Fälle" ist zu eng. Die Lesart ist eine Interpretation, kein Beleg — sie zu bestätigen oder zu verwerfen ist eine Frage an Enis (§ 8).

**Zargen-/Anschlag-Angaben in den echten DXF (gemessen, Modelspace-Scan):**

| Plan | Layer | Blocknamen | ATTRIBs an Tür-Blöcken |
|---|---|---|---|
| Barawitzka_EG | keine | keine | **nicht messbar — 0 Tür-Blöcke im Modelspace** |
| Mollgasse_EG | `02-DIM-G00-LEG-ROHBAU` | `TÜR-BLOCKZARGE-90_STUMPF`, `-100_STUMPF`, `-SCHACHT_125` | keine (44 INSERTs `<ohne ATTRIB>`) |
| Muthgasse_E2 | keine | `TU DF 1 - Umfassungszarge flächenbündig - DL - 800 x 2490 …` (8 Varianten) | keine (106 INSERTs `<ohne ATTRIB>`) |
| Rennweg_EG | keine | `Zargentür_1_Fl 10[2,3,5,7]` | **nicht messbar — 0 Tür-Blöcke im Modelspace; der Scan geht nicht in Blockdefinitionen** |
| Rennweg_OG3 | keine | `Zargentür_1_Fl 10[1…8]` | **nicht messbar — dito** |

Der Zargentyp steht teils im Namen (`_STUMPF`, „Umfassungszarge flächenbündig"), das **Anschlagmaß nirgends**. Ohne Zargen- und Anschlagmaß ist die Lichte aus der Zeichnung nicht ableitbar. Der Layername `…-LEG-ROHBAU` in Mollgasse belegt die Gegenrichtung: dort ist Rohbau bemaßt, nicht Fertigmaß.

**Fund: Muthgasse trägt die Durchgangslichte — als Beschriftung.** 83 Blöcke heißen `HNP_Beschriftung Türen - AF 50 - Durchgangslichte_ Nummer_ Brandschutz…`. Sie werden von `_ist_tuer_block` als Türen erkannt und landen mit `breite_mm = 0.0` im Modell. Gemessen: 7 Blockdefinitionen, Inhalt `7x <LINE>` (nur Führungslinie), keine ATTDEFs, 83 INSERTs ohne ATTRIBs. Der Wert steht als freier Text daneben (`…/scratchpad/_lichte_texte.py`, echte Ausgabe, Top 6):

```
Durchgangslichte-Fahnen: 83   TEXT/MTEXT im Plan: 2060
Fahnen ohne Text <=1500mm: 0
    3x 200@99mm  | 90@147mm    | 30@242mm
    3x 200@99mm  | 90@147mm    | 30@341mm
    3x 210@103mm | 90@149mm    | E90@368mm
    3x 200@103mm | 150,5@198mm | 30-C@346mm
    2x 200@99mm  | 95@147mm    | 30@341mm
    2x 200@99mm  | 121@163mm   | 30-C@346mm
```

Ableitbare Paare (Breite/Höhe in cm, als **Interpretation** gekennzeichnet, gestützt durch die identische Notation in den Blocknamen): **90/200, 90/210, 95/200, 80/200, 82/200, 121/200, 150,5/200**. Die Engine liest sie nicht; genau diese Türen bekommen heute `0.0`.

**Vorschlag `lichte_mm`** (nicht implementiert):

```python
lichte_mm: int | None = None      # nutzbare Durchgangslichte (Fertigmass)
lichte_quelle: str | None = None  # z.B. "text:90/200", "blockname:DL 800x2490"
```

Regeln: (1) `lichte_mm` bleibt `None`, solange kein Beleg im Plan existiert — nie aus `breite_mm` abgeleitet, kein Abschlag, kein Faktor. (2) `breite_mm` bleibt das gemessene Maß, `breite_quelle` sagt welches. (3) Norm-Prüfungen gegen OIB RL 4 Punkt 2.7.1/2.8.1 dürfen **ausschließlich** `lichte_mm` verwenden; `None` heißt „nicht nachgewiesen", nie „unterschritten". `int` statt `float`, weil eine Lichte aus einer Beschriftung in ganzen mm kommt.

### 6.3 Frage 3 — `0.0` → `None`

| Plan | Türen | `breite_mm == 0.0` | davon aus `text_tueren` | `is None` |
|---|---:|---:|---:|---:|
| Barawitzka_EG | 106 | 0 | 0 | 0 |
| Mollgasse_EG | 147 | 4 | 0 | 0 |
| Muthgasse_E2 | 308 | **127 (41 %)** | 40 | 0 |
| Rennweg_EG | 41 | 1 | 1 | 0 |
| Rennweg_OG3 | 27 | 0 | 0 | 0 |
| **Summe** | **629** | **132 (21 %)** | **41** | **0** |

`None` kommt nie vor — der Contract-Default ist `0.0`, `float` lässt `None` nicht zu (belegt: `Tuer(breite_mm=None)` → `ValidationError: Input should be a valid number`).

Ursache der Nullen (`…/scratchpad/_tuer_null_grund.py`, reiner DXF-Scan):

| Plan | Tür-Blöcke | mit Breite | ohne (0.0) |
|---|---:|---:|---:|
| Barawitzka_EG | 0 | 0 | 0 |
| Mollgasse_EG | 44 | 40 | 4 (2× `WET`, 2× `WET_AUSSEN`) |
| Muthgasse_E2 | 106 | 19 | 87 |
| Rennweg_EG | 0 | 0 | 0 |
| Rennweg_OG3 | 0 | 0 | 0 |

Muthgasse, alle 87: 52× + 28× + 3× `HNP_Beschriftung Türen … Durchgangslichte…` (= 83 Fahnen), 1× `TU_SF_1_Schiebetüre Aufgesetzt - ML_8785x2525`, 1× `FE TÜR 4 tlg - waagrecht geteilt…`, 2× `HNP_Wanddurchbruch - WDB Montageöffnung` (Öffnungs-Marker).

Das Bild ist eindeutig: **die 0.0 sind fast nie „schmale Tür", sondern „nicht gemessen"** — bei Muthgasse überwiegend Beschriftungs-Fahnen, die überhaupt keine Türen sind. Die vier Mollgasse-Fälle sind echte Wohnungseingangstüren, deren Name keine Zahl trägt.

**Migration (Vorschlag, Reihenfolge zwingend):**

**Schritt 0 — Konsumenten None-fest machen** (vor jeder Contract-Änderung, für sich lauffähig, mit `0.0` **und** `None` grün):

- `tuer_typisierung.py:142` → `(t.breite_mm or 0.0) > _DOPPELFLUEGEL_MM`
- `tuer_typisierung.py:161` → dito für `_GARAGENTOR_MM`
- `tueren.py:235` → `t.breite_mm is not None and _ARC_MIN_MM < t.breite_mm < _ARC_MAX_MM`
- `tueren.py:245` → nur bei beiden `is not None` verschmelzen
- `rest_komponenten.py:140` → `max(_TUER_RAND_MM, t.breite_mm or 0.0)`
- `scripts/plan_pruefen.py:684` → dito
- `dxf_renderer.py:524` braucht keine Änderung (`None or 900.0 == 900.0`), sollte den erfundenen Default aber sichtbar machen statt still setzen.

**Schritt 1** — Contract additiv (`breite_mm: float | None = None`, `breite_quelle`, `lichte_mm`, `lichte_quelle`) + `scripts/gen_schema.py`. **Schritt 2** — Erzeuger umstellen. **Schritt 3** — Fixtures/Referenz-JSON. **Schritt 4** — `lichte_mm` befüllen und dabei die 83 Fahnen als Türen verwerfen (eigener Slice).

**Testauswirkung — gemessen an einem probeweise geänderten und danach vollständig zurückgebauten Baum** (MD5 beider Dateien identisch zum Ausgangsstand, `git diff` leer):

| | Umfang | Ergebnis |
|---|---|---|
| Baseline | **319 Tests (27 % der Suite)**, Auswahl nicht dokumentiert | 1 failed, 313 passed, 5 skipped (164 s) |
| Probe (`None`) | dieselben 319 | 4 failed, 310 passed, 5 skipped (151 s) |
| Volle Suite, unveränderter Baum (unabhängig) | 1196 collected, 2 deselected | 1 failed, 1176 passed, 10 skipped, 9 xfailed (1228 s) |

**Einschränkung, ausdrücklich:** Der None-Probelauf umfasste 319 von 1196 Tests. Nicht erhoben sind damit u. a. `tests/platzierung` (262), `tests/hauptengine` (116), `tests/render` (88), `tests/naht` (51), `tests/e2e` (25), `tests/api` (22) und der Großteil von `tests/normwissen` (344). Der Satz „der Bruch ist klein und vollständig durch Schritt 0 abgedeckt" gilt **nur für die 319 gelaufenen Tests**.

Die drei zusätzlichen Fehler der Probe:

| Test | Ursache |
|---|---|
| `tests/raumerkennung/test_tuerquellen.py::test_windfang_aussentuer_wird_hauseingang` | `TypeError: '>' not supported between 'NoneType' and 'float'` @ `tuer_typisierung.py:142` |
| `tests/raumerkennung/test_tuerquellen.py::test_windfang_mit_drei_tueren` | dieselbe Stelle |
| `tests/contract/test_schema_drift.py::test_schema_in_sync` | `gen_schema.py --check` meldet Drift — Schema muss mitregeneriert werden |

Der vierte Fehler ist der vorbestehende aus § 2.3. Kein Test assertiert `breite_mm == 0.0` als Bedeutung; die Tests auf Zahlen (`test_tueren.py:14` `== 800.0`, `:36` `== 900.0`, `:46` `600 ≤ b ≤ 1300`, `test_tuer_zuordnung.py:52` `> 800`, `test_provider.py:69` `== 1600.0`) setzen ihre Werte selbst und bleiben gültig.

### 6.4 Nachtrag 2026-09-10 — Migration UMGESETZT (Contract v1.4.0)

Punkt 2 ist jetzt Code, nicht mehr Vorschlag. `CONTRACT_VERSION` **1.3.0 → 1.4.0**,
Schema regeneriert, Drift-Gate grün. Alles additiv mit Default — bestehende Erzeuger
brechen nicht, die vier Fixtures mit `contract_version 1.1.0` laden unverändert.

Neue Felder an `Tuer` (`hauptengine/contracts/raum_modell.py`):

| Feld | Typ | Bedeutung |
|---|---|---|
| `breite_mm` | `float \| None = None` | **None = nicht gemessen** (vorher `0.0`) |
| `breite_quelle` | `BreiteQuelle = "UNBEKANNT"` | `BLOCKNAME`, `GEOMETRIE_SCHWENKRADIUS`, `GEOMETRIE_SUMME`, `GEOMETRIE_OEFFNUNG`, `ATTRIBUT` (reserviert, kein Erzeuger), `STANDARDWERT` (Reserve, gehört nicht ins Modell), `UNBEKANNT` |
| `breite_grund` | `str \| None = None` | warum keine Messung — nur bei `UNBEKANNT` |
| `lichte_mm` | `int \| None = None` | Durchgangslichte; **bleibt None**, kein Erzeuger, nie aus `breite_mm` abgeleitet |

Alle neun Schreibpfade setzen `breite_quelle` mit; `_breite_mm()` und
`_blattbreite_aus_block()` geben `None` statt `0.0`; `text_tueren` schreibt
`breite_mm=None, breite_quelle="UNBEKANNT", breite_grund="nur Text-Beleg, keine
Geometrie"`. Konsumenten sind None-fest (Schritt 0 aus § 6.3, vollständig
umgesetzt), `plan_pruefen.py` weist `—` plus eine eigene Spalte `Breiten-Quelle`
aus statt zu formatieren. `lichte_quelle` ist **nicht** angelegt — ohne Erzeuger
wäre es ein totes Feld; kommt mit dem `lichte_mm`-Slice.

**Ist-Verteilung nach der Migration, gemessen über die fünf Prüfpläne**
(`…/scratchpad/_breite_quelle_nachher.py|.json`, Provider-Parse, 2026-09-10;
612 Türen — nicht mehr 629, weil die 83 Muthgasse-Beschriftungsfahnen seit
Commit `8b35e53` keine Türen mehr sind):

| Plan | Türen | BLOCKNAME | GEO_SCHWENKRADIUS | GEO_SUMME | GEO_OEFFNUNG | UNBEKANNT |
|---|---:|---:|---:|---:|---:|---:|
| Rennweg_OG3 | 27 | 0 | 3 | 0 | 24 | 0 |
| Rennweg_EG | 41 | 0 | 10 | 0 | 30 | 1 |
| Barawitzka_EG | 106 | 0 | 36 | **2** | 68 | 0 |
| Mollgasse_EG | 147 | 40 | 27 | 0 | 76 | 4 |
| Muthgasse_E2 | 291 | 18 | 28 | 0 | 170 | 75 |
| **Summe** | **612** | **58** | **104** | **2** | **368** | **80** |

Drei Gegenproben, alle 0: **keine** Tür trägt `breite_mm == 0.0`, **keine** Tür
mit `breite_mm is None` steht ohne `breite_grund` da, und `lichte_mm` ist auf
keiner der 612 Türen gesetzt.

`dxf_renderer.py:524` (`t.breite_mm or 900.0`) ist **unverändert** — Leonis' Lane,
nicht einseitig angefasst. Nach der Migration ist das der einzige Ort, der ein Maß
erfindet, und er tut es jetzt für alle `None`-Türen statt nur für die `0.0`.

**Vorschlag an @EnisAMG (deine Lane, von uns NICHT geändert) — vierter Befund.**
`oib_rl4_fluchtwegbreiten.yaml::tuerbreite_herkunft` führt drei `befunde`, gemessen
sind **vier** Herkünfte. Kleinste ehrliche Anpassung:

1. Vierten Befund ergänzen: `pfad: "tueren.py:259 :: verschmelze_doppelfluegel"`,
   `was:` „Summe zweier Schwenkradien zweier Türblätter, ohne Abzug des
   Mittelstoßes — eine vierte Herkunft im selben Feld"; `geprueft_gegen:` auf den
   aktuellen Stand nachziehen; in `folge:` und `vor_jeder_pruefung_zu_klaeren[0]`
   „drei" → „vier".
2. `tests/normwissen/test_quellenblock_e07_rl4.py:301`: `== 3` → `== 4`.
   Ausdrücklich **nicht** `>= 3` — die Zahl ist eine gemessene Aussage über den
   Code und soll scharf gepinnt bleiben, damit ein fünfter Schreibpfad wieder rot
   wird.
3. Docstring-Satz „mindestens drei Bedeutungen" (Z. 288-296) → „vier Bedeutungen
   plus 0.0/None = keine Messung", sonst steht die Begründung des Tests falsch da.

Status heute: Zeile 301 ist **grün**, weil wir die YAML nicht angefasst haben und
die Fixtures unverändert sind (Zeile 307 prüft Fixture-Werte `{900, 1000, 1400}` —
sie wird erst rot, wenn eine Fixture `"breite_mm": null` trägt, also im
Fixture-Schritt). Belegzahlen für den vierten Befund: 629 Türen / fünf Pläne,
davon 360 `GEOMETRIE_OEFFNUNG`, 77 `GEOMETRIE_SCHWENKRADIUS`, 58 `BLOCKNAME`,
**2 `GEOMETRIE_SUMME`** (Barawitzka_EG), 132 ohne Messung.

Offen und von der YAML-Ergänzung nicht berührt: dein Befund nennt
`tuer_zuordnung.py:155`, tatsächlich schreiben dort **zwei** Stellen (`:157`
`durchgaenge_ohne_tuerblatt` und `:218` `aussen_durchgaenge`). Wir zählen sie als
**einen** Befund (gleiche Herkunft `GEOMETRIE_OEFFNUNG`, gleiches Verfahren) —
zählst du sie getrennt, steht am Ende `== 5`.

---

## 7. Was ist umgesetzt / was fehlt

### 7.1 Stand 2026-09-09 — **vorher**, unverändert stehen gelassen

Die folgende Tabelle ist der Stand bei Abgabe des Berichts. Sie bleibt als
Vergleichsmaßstab; der Ist-Stand nach den Schritten 1-6 steht in § 7.2, die
Zahlen dazu in § 10.

| Punkt | Umgesetzt (Stand 2026-09-09, vorher) | Fehlt (Stand 2026-09-09, vorher) |
|---|---|---|
| **0 — Paketübernahme** | 7 Dateien hash-identisch im Arbeitsbaum, 2 Diffs angewandt, WIP-Commit `a9ab1b6` | Archiv-Hash nicht prüfbar (§ 2.1); 2 Listeneinträge aus dem `oib_rl2_tabelle6.yaml`-Diff nicht angekommen (§ 3.2); Widerspruch `astv_arbeitsstaetten.yaml:271` vs. § 11.1 nicht nachgezogen (Enis' Datei) |
| **1 — natürliche Belichtung** | Ist-Stand vollständig erhoben, alle 5 Pläne gemessen, Fensterherkunft je Familie belegt, Regeln True/False/None und drei Feldvorschläge formuliert. **Code für Punkt 5:** `raumerkennung/fenster_signatur.py` erkennt die Barawitzka-Fensterdarstellung nach Erscheinungsbild (24 Öffnungen, 0 Falschtreffer auf den 4 Vergleichsplänen), 7 Tests grün, kein Contract-Touch (§ 4.5) | **Kein Belichtungs-Code am Raum.** Contract-Felder `natuerlich_belichtet`, `belichtung_quelle`, `belichtung_vollstaendigkeit` sind Vorschlag. GLASWAND als eigenständige Quelle ungemessen, 500-mm-Toleranz unkalibriert, Arbeitsraum-Eigenschaft (AStV § 1 Abs. 4) fehlt vollständig |
| **2 — Breitenverlauf** | `breitenprofil.py` repariert (3 Ursachen), +62/−21 in 2 Dateien, 9 Tests grün, 283 passed / 5 skipped in der Regression, ruff grün, alle 5 Pläne gemessen, 2 Belegprofile | **Keine Anbindung**: kein Provider-Aufruf, kein Contract-Feld. `FluchtwegSegment`-Ergänzung ist Vorschlag. 61 Segmente ohne schneidendes Raumpolygon (unsere Lane). Eckfenster verwirft auf GRAPH-Segmenten weiter den Großteil des Profils |
| **3 — `Tuer.breite_mm`** | 9 Schreibpfade belegt, Herkunft je Plan über 629 Türen ausgezählt, Ursache der 132 Nullen belegt, DL-Beschriftungsfund Muthgasse, Migrationsreihenfolge + gemessene Bruchstellen | **Kein Code.** `breite_quelle`, `lichte_mm`, `lichte_quelle`, `breite_mm: float \| None` sind Vorschlag. Schritt 0 (None-Festigkeit der Konsumenten) nicht ausgeführt. Testauswirkung nur auf 27 % der Suite erhoben. ATTRIB-Befund für Barawitzka/Rennweg nicht messbar. Muthgasse-Aufteilung BLOCKNAME/SCHWENKRADIUS auf ±1 unsicher |
| **Querschnitt** | Enis' Test `test_kein_contract_wert_und_kein_konsument` wieder grün — Docstring-Quellenangabe in `breitenprofil.py` umformuliert, Test selbst unverändert (§ 3.3) | Entscheidung offen, ob der Wächter dauerhaft per Substring über Dateiinhalte prüfen soll (Enis' Lane) |

### 7.2 Ist-Stand 2026-09-10 nach den Schritten 1-6

Alle Zahlen aus tatsächlich gelaufenen Befehlen, Belege in § 10. Commits auf
`selman/extents-ausreisser`, **kein Push**: `8b35e53` · `58cd3a0` · `1ddb752` ·
`9141a3c` · `e9837b0` (+ dieser Abschluss-Commit).

| Punkt | Ist 2026-09-10 | Was weiterhin fehlt |
|---|---|---|
| **0 — Paketübernahme** | unverändert | unverändert (§ 7.1) |
| **1 — natürliche Belichtung** | `raumerkennung/fenster_signatur.py` im Baum, 24 Barawitzka-Fensteröffnungen, **0 Falschtreffer** auf den vier Vergleichsplänen, 7 Tests grün. `belichtung_vollstaendigkeit` Barawitzka UNGEPRUEFT → **TEILWEISE** (§ 4.4) | weiterhin **kein Belichtungs-Code am Raum**, kein Contract-Feld, keine Raumzuordnung der 24 Öffnungen, Rennweg EG/OG3 nicht gesucht (0 Wandsegmente), 4 `Glaswand`-Texte unerfasst |
| **2 — Breitenverlauf** | messbare Segmente **209/307 (68,1 %) → 287/307 (93,5 %)** (§ 10.4). Neue öffentliche Funktion `begrenzende_flaechen`, `SNAP_MM = 200` verschiebt den **Messort**, nicht das Polygon; zweiter Deckel `ECKE_FENSTER_MM` gegen Eckfenster. 13 Tests grün | weiterhin **keine Anbindung**: kein Provider-Aufruf, kein Contract-Feld am `FluchtwegSegment`. 20 Restsegmente einzeln belegt (12x `flaeche_fehlt` Mollgasse-Laubengang/Hofwege, 8x `nur_tuer_oder_eckpunkte`) |
| **3 — `Tuer.breite_mm`** | **umgesetzt**, `raum_modell` 1.3.0 → **1.4.0**: `breite_mm: float \| None`, `breite_quelle`, `breite_grund`, `lichte_mm`. Alle neun Schreibpfade setzen die Quelle, alle Konsumenten None-fest, Drift-Gate grün. Ist über 612 Türen: 58 BLOCKNAME / 104 SCHWENKRADIUS / 2 SUMME / 368 OEFFNUNG / 80 UNBEKANNT, **0** Türen mit `0.0`, **0** ohne `breite_grund`, **0** mit gesetztem `lichte_mm` (§ 6.4) | `lichte_mm` hat **keinen Erzeuger** und bleibt `None`; `lichte_quelle` bewusst nicht angelegt. YAML-Nachtrag (vierter Befund) + `test_quellenblock_e07_rl4.py:301` `== 3` → `== 4` liegen bei @EnisAMG. 3-Owner-Approval für 1.4.0 steht aus |
| **4 — erfundene Maße (neu)** | `tests/contract/test_keine_erfundenen_masse.py` (3 Tests, AST über `src/**`, Messfeldliste aus den Contracts selbst), gegen drei Probeverletzungen einzeln rot geprüft. `dxf_renderer.py` `900.0` → benannte Konstante `_ZEICHEN_ERSATZBREITE_MM`, **identischer Wert, identisches Bild** | eine Zahl über zwei Zuweisungen sieht der Riegel nicht (keine Datenflussanalyse; Muster kommt im Baum nicht vor). Eine benannte Konstante umgeht ihn absichtlich. Sichtbare Kennzeichnung ungemessener Türen im Render: @mvpo3, offen |
| **5 — Beschriftungsfahnen (neu)** | `_DOOR_EXCLUDE` um `BESCHRIFT`; Muthgasse **308 → 291 Türen**, 83 Phantom-`TuerOeffnung`en weg, `_verworfene_bloecke` als nachvollziehbarer Zähler (166 = 83 x 2 Einstiege). Andere vier Pläne: 0 | **stair_exit Muthgasse 12 → 5** — 5 davon waren Fahnen, aber **3 echte Türen haben ihre Typisierung verloren**, Ursache nicht aufgeklärt. Als strict-xfail `test_soll_stair_exits` sichtbar gehalten, Band **nicht** abgesenkt |
| **Querschnitt** | volle Suite **1199 passed, 10 skipped, 2 deselected, 10 xfailed, 0 XPASS** (1648,74 s); Prüfstrecke über alle fünf Pläne gelaufen (§ 10.2) | die 10 strict-xfails stehen unverändert (§ 10.5). `tests/raumerkennung/test_tueren.py::test_mollgasse_tueren` **skippt** weiter (DXF `Projekte/Mollgasse Notbeleuchtung/WHA_MOL_EG.dxf` fehlt im Arbeitsbaum) |

---

## 8. Abstimmungsbedarf

Alle Datenmodellangaben unten sind **VORSCHLAG**. `hauptengine/contracts/**` ist eingefroren (Konsensregel: beide Fenster + Version-Bump + `gen_schema` + 3-Owner-Approval). Nichts davon ist implementiert, und keine Contract-Ergänzung ist zwingend — sie sind **optional** in dem Sinn, dass ohne sie die betroffene Prüfung schlicht bei `ungeprueft` / `nicht messbar` bleibt, statt falsch zu werden.

### 8.1 Von @EnisAMG (normwissen/)

1. **Belichtung, Semantik:** Genügt eine Glaskonstruktion ohne erkannte Öffnung (ALU_GLAS-Wand) als „natürlich belichtet" i. S. v. AStV § 9 Abs. 1 Z 1, oder verlangt Z 1 eine Belichtungs*fläche* mit Außenbezug? Zählt eine **Balkontür** als Belichtungsfläche oder nur als Weg?
2. **Belichtung, Unvollständigkeit:** Darf ein Raum in einem nur `TEILWEISE` erhobenen Plan `True` tragen, oder muss er `None` bleiben? Deine § 9.3-Forderung („der Unterschied muss im Modell erkennbar sein") verlangt neben dem bool ein Vollständigkeitsmerkmal — reicht `bool | None` plus `belichtung_vollstaendigkeit`, oder willst du das Merkmal anders schneiden (z. B. Fensterfläche in m²)?
3. **Belichtung, Bezugsobjekt:** § 9.4 sagt, Z 1 knüpft an Raum **und** Fluchtweg-Abschnitt. Feld nur an `Raum`, oder zusätzlich an `FluchtwegSegment`?
4. **Belichtung, zweiter Eingang:** die **Arbeitsraum-Eigenschaft** (AStV § 1 Abs. 4) fehlt vollständig. Der Nutzungsklassen-Kanon (`nutzungsklasse.py:12-42`) kennt keinen Arbeitsraum-Typ. Ohne sie bleibt Z 1 auch mit `natuerlich_belichtet` `ungeprueft`. (Verwandt: `GESCHAEFTSLOKAL` ist seit 2026-09-08 unbeantwortet.)
5. **Breite, Form im Contract:** § 9.1 lässt zwei Wege zu (Abschnitte konstanter Breite **oder** Breitenprofil). Ein `breite_mm: float | None` am Segment kann das Profil nicht tragen. Welche der drei Größen landet in welcher Form im Contract? Bitte auch § 5.2/5.5 gegenlesen: taugt `abschnitte` (tatsächliche Breite) vs. `engstellen` (örtliche Engstelle) so als Nachweisgrundlage? Wir setzen keinen Normwert ein, auch nicht als Fallback.
6. **Breite, Version:** dein Proposal `WEGBREITE_RANDSTREIFEN.md` nennt `raum_modell` 1.1.0 → 1.2.0; Ist ist **1.3.0**. Additiv wäre der Bump 1.3.0 → **1.4.0**. Bleibt der Vorschlag inhaltlich stehen?
7. **Breite, Vokabular:** welche Werte erwartet RL-4-Tabelle 1 für Gangart/Treppenart (Hauptgang/Nebengang, Haupt-/Wohnungs-/Nebentreppe), damit unsere Typisierung darauf mappen kann?
8. **Tür, Zielsemantik:** Nennmaß behalten und ein zweites Feld „nutzbare Durchgangslichte" ergänzen, oder ein Herkunfts-Enum am bestehenden Feld? Existiert eine **belegte** Umrechnung Nennmaß → Durchgangslichte (heute: nein)? Unsere Position: wenn nur `breite_quelle=GEOMETRIE_OEFFNUNG` vorliegt, bleibt `lichte_mm` `None`.
9. **Tür, DL-Notation:** gilt die Lesart, dass `…_1DF_90x200` und `… - DL - 800 x 2490` die Durchgangslichte nennen? Davon hängt ab, ob § 6.2 für 18 Muthgasse-Türen anders lautet (dort als strittig gekennzeichnet).
10. **Tür, YAML-Nachtrag:** `tuerbreite_herkunft` nennt **drei** Herkünfte; gemessen sind es **vier** plus „keine Messung" — die Doppelflügel-Summe (`tueren.py:259`) fehlt. **Achtung:** `tests/normwissen/test_quellenblock_e07_rl4.py:301` pinnt `assert len(herkunft["befunde"]) == 3` — die Ergänzung macht diesen Test rot.
11. **Tür, Zwei-Türen-Regel:** RL 4 Punkt 2.8.1 („Abstand ≤ 20 cm = eine Tür") kollidiert konzeptionell mit `verschmelze_doppelfluegel` (`_DOPPEL_TOL_MM = 300`). Wer besitzt die Zusammenfassung — Erkennung oder Prüfung?
12. **Dein Test:** `test_kein_contract_wert_und_kein_konsument` prüft per Substring über Dateiinhalte und traf damit eine bloße Docstring-Quellenangabe in `breitenprofil.py` (kein Ladevorgang). Wir haben die **Quellenangabe umformuliert**, deinen Test **nicht angefasst** — er ist wieder grün und weiter scharf. Frage an dich: soll der Wächter dauerhaft auf Import-/Ladepfad prüfen statt auf Substring? Dann wäre die wörtliche Dateiangabe im Docstring wieder möglich.

### 8.2 Von @mvpo3 (Leonis, platzierung/)

1. **Verbraucher der Wegbreite.** `WEGBREITE_RANDSTREIFEN.md` § 4b adressiert dich: `deckung.py::verdichte_fluchtweg` ersetzt die Breite heute durch `min(bounds[2]-bounds[0], bounds[3]-bounds[1])`. Ohne Zusage, das gegen `weg_nachweis(...)` zu tauschen, hätte ein Contract-Feld keinen Verbraucher — dasselbe Muster wie `RaumModell.anker` (erzeugt, geprüft, nie gelesen).
2. **Detailtiefe.** Brauchst du das volle 100-mm-Profil, oder reichen `abschnitte` + `engstellen` + `breite_min_mm`? Davon hängt ab, ob `breitenprofil` überhaupt in den Contract muss.
3. **Platzierung unverändert.** Bestätigung, dass die drei Belichtungsfelder die Platzierung nicht verändern (Enis' Testfall 4.1). Der Nutzungsklassen-Filter greift heute nur in `platzierung/flaechen_strategy.py:155-167` — ein neues Raumfeld darf dort keinen zweiten stillen Pfad öffnen.
4. **`breite_mm = None` erreicht die Platzierung.** Heute nutzt `platzierung/` das Feld nicht direkt (eigene `breite_mm`-Parameter in `deckung.py`/`lux_nachweis.py`; `tests/platzierung/test_aussen_strategy.py:61` setzt es selbst). Vor Schritt 2 bitte bestätigen, dass keine neue Nutzung geplant ist.
5. **Aufrufer für `ArbeitsstaettenWissen`.** ASTV § 6.4: der gehört in `hauptengine/validierung.py` — Hauptengine, Abstimmung, nicht einseitig. Ohne Aufrufer erscheint ein Belichtungsfeld in keinem Prüfbericht.
6. **Gegenleistung, die bei uns liegt:** Spikey-Polygone Mollgasse `raum_41`/`raum_55` (deine Naht ② an uns). Das ist die Gegenrichtung derselben Naht — bei einer Mittellinie in Zacken wäre auch jedes Breitenprofil dort unbrauchbar.

### 8.3 Für die 3-Owner-Runde

Alles additiv, alle Felder mit Default, `CONTRACT_VERSION` 1.3.0 → 1.4.0, `scripts/gen_schema.py` ist Pflichtteil (Drift-Gate belegt rot):

| Ziel | Felder | Zwingend? |
|---|---|---|
| `Raum` | `natuerlich_belichtet: bool \| None`, `belichtung_quelle`, `belichtung_vollstaendigkeit` | optional — ohne sie bleibt AStV § 9 Z 1 `ungeprueft` |
| `FluchtwegSegment` | `breitenprofil`, `abschnitte`, `engstellen`, `breite_min_mm`, `breite_messbar`, `breite_grund` | optional — ohne sie bleibt `breitenprofil.py` unangebunden |
| `Tuer` | `breite_mm: float \| None`, `breite_quelle`, `lichte_mm`, `lichte_quelle` | optional — ohne sie bleibt RL 4 Punkt 2.7.1/2.8.1 `blockiert_bis_semantik_geklaert` |

Zwei Punkte außerhalb der Contract-Frage, die die Runde kennen sollte:

- `dxf_renderer.py:524` erfindet still 900 mm Türbreite. Heute unsichtbar; sollte mindestens im Prüfbericht auftauchen.
- Die 83 Muthgasse-Beschriftungsfahnen sind **keine Türen** und blähen `RaumModell.tueren` um rund 27 % auf (308 statt ~225). Eigenständiger Erkennungs-Bug, unabhängig von der Breitenfrage — unsere Lane.

---

## 9. Anhang

### 9.1 Messskripte und Rohausgaben

Alle temporär, im Scratchpad `C:/Users/selma/AppData/Local/Temp/claude/D--KI-Projekt/8fc32369-9bee-42cd-9e07-20d9eeb9eff5/scratchpad/`, Dateinamen mit `_`-Prefix. Interpreter durchgehend `D:/KI Projekt/Notbeleuchtung/.venv/Scripts/python.exe` (das globale `python` hat weder pytest noch shapely noch ezdxf).

| Thema | Skript | Ausgabe |
|---|---|---|
| Belichtung | `_belichtung_ist.py` (+ Ableitungen `_belichtung_ist_fast4.py`, `_belichtung_ist_rennweg.py`, `_belichtung_ist_muth.py`), `_fenster_scan.py` | inline, § 4.3 |
| Fensterdarstellung Barawitzka (§ 4.5) | `_bara_ist.py`, `_bara_layer.py`, `_bara_geo.py`, `_bara_oeffnung.py`, `_bara_inhalt.py`, `_bara_dump.py`, `_bara_render.py`, `_bara_alu.py`, `_bara_glastext.py`, `_glasdoppel.py`, `_gap_hist.py`, `_kreuz.py`, `_kreuz2.py`, `_rahmen.py`, `_rahmen2.py`, `_bara_marker.py`, `_p6_fenster.py` (Modullauf), `_p6_rot.py` (Rot-Probe) | inline, § 4.5; Bilder `_bara_uebersicht.png`, `_bara_w1.png`, `_bara_nord.png`, `_bara_marker.png` |
| Belichtung, Verifikation | `_v_fast.py`, `_v_muth.py`, `_adv_check.py`, `_adv_check2.py`, `_adv_check3.py`, `_adv_muth_nk.py` | `_v_muth.out` |
| Breitenprofil | `_breitenprofil_ist.py`, `_floor_check.py`, `_alt_lauf.py`, `_alt_seg18.py`, `_zickzack_vergleich.py`, `_var/_bp_nur_deckel.py`, `_alt/` (HEAD-Stand via `git show`) | `_nachmessung.json`, `_breitlauf.txt`, `_muth_floor.txt` |
| Belegprofile | (aus `_breitenprofil_ist.py`) | `_profil_barawitzka.txt`, `_profil_mollgasse.txt`, `_orig_profil_*.txt` |
| Tür | `_tuer_quelle_ist.py`, `_tuer_null_grund.py`, `_lichte_beschriftung.py`, `_lichte_texte.py`, `_none_bruchstellen.py` | `_baseline.txt`, `_probe.txt`, `_v_quelle.txt`, `_v_baseline.txt`, `_v_baseline_err.txt` |
| Tür, Probelauf-Backups | — | `_bak_raum_modell.py`, `_bak_tueren.py` (Restore verifiziert, MD5 identisch, `git diff` leer) |

Die fünf Prüfpläne sind die DXF in `Projekte/_eingang/`, identisch mit der Prüfstrecke laut `Handoff/SELMAN.md:71-76` und `docs/COORDINATION.md:316`: **Barawitzka_EG, Mollgasse_EG, Muthgasse_E2, Rennweg_EG, Rennweg_OG3**.

### 9.2 Belegprofile

Vollständig in `_profil_barawitzka.txt` und `_profil_mollgasse.txt`; die zitierten Abschnitte, Engstellen, Türpunkte und `breite_min_mm` stehen in § 5.4. Beide Dateien wurden unabhängig neu erzeugt und sind byteidentisch zur ersten Fassung (`diff` leer) — die Messung ist deterministisch.

### 9.3 Nicht messbar geblieben

| Angabe | Grund |
|---|---|
| Archiv-SHA-256 `a30221a7…` | kein `.tar.gz` vorhanden (§ 2.1) |
| Laufzeit des korrigierten Rennweg_OG3-Breitenlaufs | `_floor_check.py` gibt keine Zeit aus; wird nicht geschätzt (§ 5.3) |
| Speicherverbrauch des Muthgasse-Belichtungslaufs | kein Skript instrumentiert Speicher (§ 4.3 Pkt. 7) |
| GLASWAND als eigenständige Belichtungsquelle | von der Belegreihenfolge verdeckt (§ 4.3 Pkt. 1) |
| Oberlichter/Lichtkuppeln | auf keinem der fünf Pläne vorhanden |
| Zuordnung der 24 Barawitzka-Fensteröffnungen zu Räumen | kein Provider-Lauf, keine Kontaktband-Prüfung durchgeführt (§ 4.5.4) |
| Vollständigkeit des Barawitzka-Fensterbestands | kein unabhängiger Referenzbestand auf diesem Plan (§ 4.5.3) |
| Rahmensignatur auf Rennweg_EG / OG3 | `wandsegmente()` liefert dort 0 Segmente (Wände in `Wall_*`-Blöcken) — nicht gesucht, nicht widerlegt (§ 4.5.3) |
| Die 4 `Glaswand`-Texte auf Barawitzka als Belichtungsbeleg | 3034–10586 mm vom nächsten Kandidaten, eigener unerfasster Kanal (§ 4.5.3) |
| Kalibrierung der 500-mm-Belegtoleranz | nicht durchgeführt |
| ATTRIBs an Tür-Blöcken, Barawitzka + Rennweg EG/OG3 | 0 Tür-Blöcke im Modelspace; der Scan geht nicht in Blockdefinitionen (§ 6.2) |
| Testauswirkung der `None`-Migration auf 877 der 1196 Tests | Probelauf umfasste nur 319 Tests (§ 6.3) |
| Ob `origin/main` remote weitergelaufen ist | kein `git fetch` ausgeführt; `origin/main = fd65839` ist der lokal gespiegelte Stand |

---

## 10. Nachtrag 2026-09-10 — Abschluss: Prüfstreckenlauf, Suite, xfail-Bilanz

Dieser Abschnitt schreibt die Zahlen der §§ 4–6 fort. **Alte Zahlen sind nicht
gelöscht** — sie stehen dort, wo sie erhoben wurden, und werden hier als
„vorher" zitiert.

### 10.1 Was gelaufen ist

| Lauf | Befehl | Ergebnis |
|---|---|---|
| Prüfstrecke | `.venv/Scripts/python.exe scripts/plan_pruefen.py` (alle fünf DXF in `Projekte/_eingang/`) | exit 0, fünf Pläne, Rohlog `…/scratchpad/_s6_pruefstrecke.log` |
| Volle Suite | `.venv/Scripts/python.exe -m pytest -q -rX` | `1199 passed, 10 skipped, 2 deselected, 10 xfailed, 2 warnings in 1648.74s (0:27:28)`, Rohlog `…/scratchpad/_s6_pytest.log` |

Beide Läufe liefen gleichzeitig auf derselben Maschine. Das verzerrt **nur die
Laufzeiten**, nicht die Ergebnisse; die Muthgasse-Laufzeit ist deshalb nicht mit
dem Vorbefund vergleichbar (siehe § 10.2, Fußnote).

### 10.2 Prüfstrecke — Ist je Plan (Lauf `2026-09-10 04:48 · e9837b0`)

| Plan | Stempel | Räume | Restflächen | Türen typisiert | Ausgänge | Segmente | Wohnungen | RZ / SL | Laufzeit |
|---|---:|---:|---:|---|---|---|---:|---|---:|
| Barawitzka_EG | 38 | 38 | 10 | 55/106 | final_exit 1 | GRAPH 11, FALLBACK 1 | 7 | 3 / 4 | 312,0 s |
| Mollgasse_EG | 83 | 83 | 2 | 70/147 | final_exit 9, stair_exit 4 | LINIE 103, GRAPH 19, FALLBACK 4 | 8 | 30 / 35 | 369,1 s |
| Muthgasse_E2 | 99 | 99 | 11 | **206/291** | final_exit 5, stair_exit 5 | LINIE 139, GRAPH 5, FALLBACK 2 | 8 | 65 / 28 | 2116,4 s\* |
| Rennweg_EG | 19 | 19 | 2 | 24/41 | final_exit 3, stair_exit 5 | GRAPH 8, FALLBACK 1 | 2 | 5 / 10 | 55,5 s |
| Rennweg_OG3 | 10 | 10 | 4 | 15/27 | stair_exit 1 | GRAPH 5 | 2 | 1 / 2 | 50,5 s |

\* Muthgasse lief parallel zur vollen Suite. Der Vorbefund ohne Parallellast war
**1838 s**; die Differenz ist Lastkontext und **keine** Messung der Pipeline.
Legendenabdeckung unverändert (90,3 % / 99,9 % / 99,4 % / 100,0 % / 100,0 %),
IoU-Mittel weiterhin `—` (keine Referenz-JSON neben den DXF).

**Veränderung gegen den letzten Vollauf `ab0ad51` (2026-09-09): nur Muthgasse_E2
bewegt sich.**

| Größe (Muthgasse_E2) | vorher `ab0ad51` | jetzt `e9837b0` |
|---|---:|---:|
| Türen typisiert / gesamt | 219/308 | **206/291** |
| Räume gesamt | 102 | 101 |
| Räume mit Stempel | 91 | 90 |
| Kaskade F | 21 | 20 |
| `final_exit` | 2 | 5 |
| `stair_exit` | 12 | **5** |
| Segmente GRAPH / FALLBACK | 15 / 1 | 5 / 2 |
| Wohnungen | 7 | 8 |

Barawitzka_EG (55/106), Mollgasse_EG (70/147), Rennweg_EG (24/41) und
Rennweg_OG3 (15/27) sind **identisch zum Vorlauf** — der Fahnen-Ausschluss und die
`None`-Migration verändern dort nichts, wie in §§ 6.4 und 10.3 gemessen.

Der **Rückgang der Typisierungsquote** auf Muthgasse ist rechnerisch:
219/308 = 71,1 % → 206/291 = 70,8 %. Der strict-xfail auf ≥ 90 % bleibt xfail.

**`stair_exit` 12 → 5, offener Befund, nicht geglättet.** 5 der früheren
Kandidaten waren Beschriftungsfahnen, also erfundene Ausgänge. Aber **3 echte
Türen haben ihre Typisierung verloren**; die Ursache liegt in der
Tür-Typisierung, nicht im Fahnen-Ausschluss, und ist **nicht aufgeklärt**. Das
Band wurde deshalb nicht abgesenkt, sondern als strict-xfail
`tests/naht/test_soll_muthgasse.py::test_soll_stair_exits` sichtbar gehalten.

### 10.3 Punkt 3 — Türbreiten, Ist nach der Migration

Unverändert die in § 6.4 belegte Verteilung über **612 Türen** (58 BLOCKNAME /
104 GEOMETRIE_SCHWENKRADIUS / 2 GEOMETRIE_SUMME / 368 GEOMETRIE_OEFFNUNG /
80 UNBEKANNT), gegen **vorher 629 Türen** mit 132 stillen Nullen. Die drei
Gegenproben bleiben 0/0/0. Der Prüfstreckenbericht weist die Spalte
„Breiten-Quelle" jetzt aus und schreibt `—` statt einer Zahl, wo nichts gemessen
ist — belegt durch den Lauf in § 10.2, nicht mehr nur durch die Nachbildung
`_pruefbericht_none.py` (die Einschränkung aus Schritt 2 ist damit erledigt).

### 10.4 Punkt 2 — Breitenprofil, Ist

| Plan | vorher (§ 5.3) | jetzt |
|---|---:|---:|
| Barawitzka_EG | 12/12 | 12/12 |
| Mollgasse_EG | 86/126 | 107/126 |
| Muthgasse_E2 | 102/155 | **154/155** |
| Rennweg_EG | 6/9 | 9/9 |
| Rennweg_OG3 | 3/5 | 5/5 |
| **Summe** | **209/307 (68,1 %)** | **287/307 (93,5 %)** |

`flaeche_fehlt` 61 → 12 (alle Mollgasse_EG), `nur_tuer_oder_eckpunkte` 37 → 8.
Die 20 Restsegmente sind in `Projekte/_ergebnis/VERLAUF.md` (Block „Schritt 4")
namentlich belegt. Kein Ersatzwert, kein Normwert, kein Mittelwert ist an ihre
Stelle getreten — sie bleiben `None` **mit Grund**.

### 10.5 XFAIL-Bilanz — **kein einziger xfail ist zu XPASS gekippt**

`pytest -q -rX` meldet `10 xfailed` und **keine** XPASS-Zeile. Alle zehn strict-
xfails sind unverändert rot-per-Design:

| Test | Datei:Zeile |
|---|---|
| `test_soll_explizite_linien_vorhanden` | `tests/naht/test_soll_barawitzka.py:65` |
| `test_soll_90_prozent_tueren_typisiert` | `tests/naht/test_soll_barawitzka.py:76` |
| `test_soll_16_endpunkte_an_der_aussenkante_gedeckt` | `tests/naht/test_soll_barawitzka.py:104` |
| `test_soll_jeder_endpunkt_an_der_kante_hat_final_exit` | `tests/naht/test_soll_mollgasse.py:111` |
| `test_soll_90_prozent_tueren_typisiert` | `tests/naht/test_soll_mollgasse.py:125` |
| `test_soll_final_exit_anzahl_gleich_endpunkte_an_der_kante` | `tests/naht/test_soll_mollgasse.py:159` |
| `test_soll_stair_exits` | `tests/naht/test_soll_muthgasse.py:107` |
| `test_soll_90_prozent_tueren_typisiert` | `tests/naht/test_soll_muthgasse.py:128` |
| `test_soll_eg_90_prozent_tueren_typisiert` | `tests/naht/test_soll_rennweg.py:138` |
| `test_soll_referenz_trefferquote` | `tests/naht/test_soll_referenzvergleich.py:57` |

Neu hinzugekommen gegenüber dem Ausgangsstand (9 xfailed) ist genau einer:
`test_soll_stair_exits` (Schritt 1) — ein **zusätzlich sichtbar gemachter**
Befund, kein Zielbild, das gefallen wäre. Zu XPASS gekippt ist **keiner**; das
wäre bei strict-xfail auch ein Suite-Fehler und die Suite ist grün.

### 10.6 Was in diesem Schritt ausdrücklich nicht gemacht wurde

- Kein Push, kein PR, kein Merge nach `origin` — der Owner gibt das GO separat.
- Enis' YAML und `tests/normwissen/test_quellenblock_e07_rl4.py:301` **nicht**
  angefasst (§ 6.4 Vorschlag steht, Zeile 301 ist heute grün).
- `dxf_renderer.py` über die benannte Konstante hinaus nicht angefasst
  (@mvpo3' Lane), `lux_nachweis_bericht.py:329/:333` nur gemeldet.
- Die 3 verlorenen Muthgasse-Türtypisierungen (§ 10.2) nicht aufgeklärt.
- Die Nennerfrage Muthgasse `A-DETL` (§ 5) nicht entschieden — sie ist eine
  Entscheidung, keine Messung.

---

## 11. Nachtrag 2026-09-10 — die „3 verlorenen Türtypisierungen" (Muthgasse E2)

Offen aus § 10.6. Aufgeklärt durch **zwei tatsächlich gelaufene Provider-Parses
derselben DXF** aus zwei git-worktrees: Stand **`0d7c5db`** (= `8b35e53^`, vor
dem Fahnen-Ausschluss) gegen **`1d9c03a`** (HEAD). Belege:
`_p2_vorher.json` / `_p2_nachher.json` (+ `.log`), Diff `_p2_diff.py/.json`,
Detailauswertung `_p2_detail.py`, Geometrie `_p2_geo.py`, DXF-Blockebene
`_p2_bloecke.py/.json` im Session-Scratchpad; Worktree `D:/nbwt_vorher`
(detached auf `0d7c5db`, nichts gelöscht).

### 11.1 Gesamtbild beider Stände

| | vorher `0d7c5db` | nachher `1d9c03a` |
|---|---|---|
| Türen | 308 | 291 |
| Räume | 114 | 113 |
| `stair_exit` | 12 | 5 |
| `final_exit` | 2 | 5 |
| Parse-Dauer | 862 s | 859 s |

### 11.2 Die „3 echten Türen" gibt es nicht — die 3 war eine Saldo-Zahl

Kandidaten (`tuer_detail ∈ {stiegenhaustuer, brandschutztuer}` mit Stiegenhaus-
Seite): vorher 15, nachher 7; 15 − 5 Fahnen − 7 = 3. Das ist Arithmetik, keine
Mengendifferenz. **Lagebezogen** (die IDs `durchgang_N` verschieben sich
zwischen den Ständen und sind kein Schlüssel) sind es: **11 Ausgänge weg,
1 geblieben, 4 neu** (`exit_tuer_118`, `exit_durchgang_148`, `_165`, `_168`).
Von den 11 sind 5 Beschriftungs-Fahnen und 6 Kontaktzonen-Artefakte.

### 11.3 Je Tür: Position, beide Nachbarräume, greifende Regel vorher / warum nicht mehr

**Die 5 Fahnen** (Layer `A-DOOR-IDEN`, Blockdef = genau 1 LINE, kein ARC,
`breite_mm = 0.0`; nächster ARC 2,3–5,0 m entfernt mit r = 125 mm, unter
`_ARC_MIN_MM` = 600 → kein Türblatt). Alle liefen über
`tuer_typisierung.py:154-156` (Regel 3b: STIEGENHAUS-Typ auf einer Seite,
ALLGEMEIN_ERSCHLIESSUNG auf der anderen) → `stiegenhaustuer`, dann
`ausgaenge.py:62-64` → `stair_exit`:

| Ausgang vorher | xy_mm | von → nach (vorher) | warum jetzt nicht mehr |
|---|---|---|---|
| `exit_tuer_75` | 331792,5 / 104258,3 | raum_88 STIEGENHAUS → raum_88 STIEGENHAUS | INSERT fällt aus `_DOOR_EXCLUDE` (BESCHRIFT) — ist gar keine Tür mehr |
| `exit_tuer_76` | 332814,0 / 102739,8 | raum_88 → raum_88 | dito |
| `exit_tuer_77` | 333811,1 / 101257,4 | raum_88 → raum_88 | dito |
| `exit_tuer_98` | 339310,4 / 102745,1 | raum_88 → raum_88 | dito |
| `exit_tuer_99` | 338412,1 / 106674,3 | raum_95 GANG → stiegenhaus_2 STIEGENHAUS | dito |

Bei **vier von fünf** war `von_raum == nach_raum == raum_88`: die Regel feuerte,
weil beide Seiten **derselbe** Raum sind. Das ist ein eigener Regel-Nebenbefund
(siehe § 11.6).

**Die 6 Nicht-Fahnen** — alle `quelle="durchgang"`, `ohne_tuerblatt=True`, alle
aus `tuer_zuordnung.py:120-161` (`durchgaenge_ohne_tuerblatt`: Kontaktzone
`pa.buffer(250) ∩ pb.buffer(250)`; bei **überlappenden** Polygonen ist das die
ganze Überlappung, und die Langseite ihres `minimum_rotated_rectangle` wird zur
„Breite"). Regel vorher immer `tuer_typisierung.py:154-156` → `stiegenhaustuer`,
`ausgaenge.py:62-64` → `stair_exit`:

| Ausgang vorher | xy_mm | „Breite" | Nachbarräume VORHER | Nachbarräume NACHHER | warum die Regel jetzt nicht mehr greift |
|---|---|---|---|---|---|
| `exit_durchgang_103` | 330938,7 / 107255,8 | 2861 mm | raum_46 GANG / ALLGEMEIN_ERSCHLIESSUNG — raum_88 STIEGENHAUS (41,3 m²) | Tür existiert nicht mehr | `durchgaenge_ohne_tuerblatt` erzeugt dort keine Öffnung mehr: `raum_88` liegt nicht mehr an dieser Stelle |
| `exit_durchgang_150` | 335184,8 / 104728,5 | **4862 mm** | raum_88 STIEGENHAUS — stiegenhaus_1 STIEGENHAUS (11,2 m²) | Tür weg; 695 mm daneben `durchgang_166` (stiegenhaus_1 ↔ stiegenhaus_5) | Regel greift bei `durchgang_166` weiter, der Ausgang fällt aber im **Dedupe `provider.py:148-157`** (1500 mm Manhattan, L1 = 1269 mm zu `exit_durchgang_165`) |
| `exit_durchgang_151` | 337596,3 / 102640,4 | 1601 mm | raum_88 STIEGENHAUS — stiegenhaus_1 STIEGENHAUS | keine Tür | Kontaktzone entfällt mit dem Artefakt-Raum |
| `exit_durchgang_152` | 337206,9 / 106980,6 | 1062 mm | raum_88 STIEGENHAUS — stiegenhaus_2 STIEGENHAUS (7,9 m²) | keine Tür | dito |
| `exit_durchgang_154` | 337042,5 / 105349,2 | **4807 mm** | raum_88 STIEGENHAUS — stiegenhaus_2 STIEGENHAUS | keine Tür | dito |
| `exit_durchgang_160` | 336186,8 / 103692,1 | 968 mm | stiegenhaus_1 STIEGENHAUS — stiegenhaus_8 STIEGENHAUS (0,2 m², = 100 % `lift_5`) | `durchgang_167`, d = 0 mm, identische Räume, `tuer_detail=stiegenhaustuer` | Regel greift unverändert; fällt im **Dedupe** (L1 = 1435 mm zu `exit_durchgang_165`) |

Geblieben ist genau einer: `exit_durchgang_161` (291600 / 108599, 2082 mm,
stiegenhaus_6 ↔ stiegenhaus_7) — nachher `durchgang_169`.

Ein 4,8-m-Türblatt gibt es nicht: **keine** dieser 6 war eine Tür.

### 11.4 Ursache ist der Raumsatz, nicht die Türzuordnung — und die NEUE Ermittlung ist die richtige

- `tuer_zuordnung.py` ist zwischen beiden Ständen **byte-identisch**; `8b35e53`
  ändert in `src/` nur `tueren.py` (eine Regex-Zeile). Auch
  `tuer_typisierung.py` ist unverändert — es gibt **keinen Regressionsfehler**
  in der Typisierung zu beheben.
- Von den 225 Nicht-Fahnen-Türen vorher sind 170 lagegleich (< 5 mm) auch
  nachher da; nur 16 haben andere Nachbarräume, 14 davon wegen geänderter
  Räume/Umnummerierung (raum_95 GANG 34,7 → raum_94 GANG 18,1 m²; raum_88
  41,3 → 20,7 m²).
- Der Unterschied sitzt im **Raumsatz**: `rest_komponenten.py` zeichnet
  Türöffnungen als Trennstempel in die Wandmaske. Die 83 Phantom-Öffnungen
  waren 83 falsche Trennstempel → die Restfläche wurde anders zerschnitten.

**Geometrie-Beleg (kein Testergebnis):** VORHER war `raum_88` ein REST-Raum mit
**693 Polygonpunkten**, 41,3 m², bbox 329757…341861 × 97621…108017 (12,1 × 10,4 m).
Er überlappte gleichzeitig fünf gestempelte STIEGENHAUS-Polygone (28–41 %)
**und** verschluckte `raum_79`/LIFT zu 99 %. Ein Raum kann nicht gleichzeitig
fünf andere Räume und ein Aufzugsschacht sein. NACHHER liegt `raum_88`
(20,7 m², bbox 328771…336507 × 93978…101814) an anderer Stelle und überlappt
**kein** STIEGENHAUS-Polygon mehr. → Die alte Nachbarraum-Ermittlung war falsch,
die neue ist richtig; es ist nichts zu reparieren und nichts zurückzunehmen.

### 11.5 Der echte Defekt — und was mit dem Band geschieht

**Härtester Einzelbeleg:** von den 18 Türen, die an ihrer Position einen echten
`A-DOOR`/`A-GLAZ`-Block tragen (Blockdef 8–110 LINEs, Türblatt-ARC
r = 900/950/1020 mm), hat **in beiden Ständen 0** eine STIEGENHAUS-Seite.
Keine der 12 alten und keine der 5 heutigen `stair_exit` sitzt an einem echten
Türblatt. Nächster Abstand einer echten Blocktür zu einem STIEGENHAUS-Polygon:
vorher 1281 mm, nachher 0 mm (1 Stück).

Konkreter Ansatzpunkt, gemessen: `tuer_50` (nachher) bei 334453 / 106403,
`quelle="arc_aussen+text:E2-VF-12a"`, `von_raum=stiegenhaus_1` (STIEGENHAUS),
`nach_raum=raum_65` — bleibt untypisiert, weil `raum_65` keinen `raum_typ`
trägt. Eine echte Tür an einem echten Stiegenhaus, die an der **Raumtypisierung
der Gegenseite** scheitert, nicht an der Türregel.

**Entscheidung zum Band `>= 9`:** das Zielbild stammt aus `ebf867a`
(2026-09-07), gesetzt nach der Konvention „Bänder knapp unter Ist", Ist damals
12 — und von diesen 12 entsprach keine einzige einem echten Türblatt. Die 9 ist
ein eingefrorener Falschpositiv-Stand, kein Fachziel. **Abgesenkt wurde es
trotzdem nicht:** der einzige durch Messung gedeckte Wert wäre die 5, und die
ist der Ist-Stand selbst — aus dem Ist abgeleitete Bänder sind in diesem Auftrag
ausgeschlossen, und auch die 5 ruht auf denselben Artefakten.
`test_soll_stair_exits` bleibt darum strict-xfail mit unverändertem Band;
korrigiert wurde nur die **Begründung** (der alte `reason` behauptete „3 echte
Türen haben ihre Typisierung verloren" — das ist widerlegt).

Neu dazu, mit belegtem Zielwert statt Zählband:

| Test | Art | Ist | Soll |
|---|---|---|---|
| `test_soll_echte_blocktueren_im_modell` | grün, Klammer | 18 Türen auf `A-DOOR`/`A-GLAZ`-INSERTs, davon 16 mit Türblatt-Breite (8× 900, 5× 950, 3× 1000 mm); `tuer_8` und `tuer_17` haben `breite_mm=None` mit `breite_quelle='UNBEKANNT'` — regelkonform, kein Fehler | ≥ 15 Türen, ≥ 14 mit Breite |
| `test_soll_stair_exit_aus_echter_blocktuer` | **strict-xfail** | 0 von 5 | ≥ 1 |

Der Zielwert 1 ist nicht aus dem Ist abgeleitet, sondern aus einer benennbaren
echten Stiegenhaustür im Plan (`tuer_50`, oben).

### 11.6 Nebenbefunde (ohne Bezug zu `8b35e53`, nicht angefasst)

- `provider.py:148-157` entkoppelt die Kennzahl von den Türen: 1500-mm-Manhattan-
  Dedupe, vorher 15 Kandidaten → 12 Ausgänge, nachher 7 → 5. Die Zahl misst
  Positions-Cluster, nicht Türen.
- `tuer_typisierung.py:152-156` feuert auch bei `von_raum == nach_raum`
  (4 der 5 Fahnen, und heute `exit_tuer_118` mit
  `von_raum == nach_raum == stiegenhaus_2`). Eine Tür von einem Raum in denselben
  Raum sollte keine `stiegenhaustuer` sein.
- Die 9 STIEGENHAUS-Polygone sind höchstens 4 verschiedene Kerne:
  `stiegenhaus_1 ≡ _5` (100 % Überlappung), `_2 ≡ _3 ≡ _4` (100 %), `_6`, `_7`,
  plus `_8` (0,2 m², = 100 % `lift_5`). Vorher wie nachher gleich defekt.

Die Zeilenangabe `tests/naht/test_soll_muthgasse.py:107` in § 10.5 ist durch
diesen Nachtrag verschoben; `test_soll_stair_exits` bleibt xfail, es kommt genau
ein weiterer strict-xfail hinzu (`test_soll_stair_exit_aus_echter_blocktuer`).

### 11.7 Testlauf (wörtlich)

`.venv/Scripts/python.exe -m pytest tests/naht/test_soll_muthgasse.py -q -rA`:

```
.....x.x.x.                                                              [100%]
PASSED tests/naht/test_soll_muthgasse.py::test_soll_faktor_kalibrierung_x10
PASSED tests/naht/test_soll_muthgasse.py::test_soll_wand_layer_erkannt
PASSED tests/naht/test_soll_muthgasse.py::test_soll_98_stempel_mit_flaeche_und_typ
PASSED tests/naht/test_soll_muthgasse.py::test_soll_wandkoerper_band
PASSED tests/naht/test_soll_muthgasse.py::test_soll_raeume_tueren_ausgaenge
PASSED tests/naht/test_soll_muthgasse.py::test_soll_echte_blocktueren_im_modell
PASSED tests/naht/test_soll_muthgasse.py::test_soll_raeume_flaechendeckend_typisiert
PASSED tests/naht/test_soll_muthgasse.py::test_soll_keine_beschriftungsfahnen_als_tueren
XFAIL tests/naht/test_soll_muthgasse.py::test_soll_stair_exits
XFAIL tests/naht/test_soll_muthgasse.py::test_soll_stair_exit_aus_echter_blocktuer
XFAIL tests/naht/test_soll_muthgasse.py::test_soll_90_prozent_tueren_typisiert
8 passed, 3 xfailed in 597.21s (0:09:57)
```

Der AST-Riegel bleibt grün: `pytest tests/contract/test_keine_erfundenen_masse.py -q`
→ `3 passed in 1.50s`. `ruff check tests/naht/test_soll_muthgasse.py` →
`All checks passed!`. Im ersten Lauf (600,77 s) war
`test_soll_echte_blocktueren_im_modell` rot, weil er zunächst von jeder
Blocktür eine Breite verlangte — `tuer_8` und `tuer_17` haben
`breite_mm=None` mit Quelle `UNBEKANNT`. Die **Erwartung** war falsch, nicht
der Code; korrigiert auf ≥ 14 von 18. **Kein Code in `src/` wurde geändert**
— der Befund ist Test- und Berichtsarbeit.

---

## 12. Nachtrag 2026-09-10 — Abschluss Schritt 3: lastfreie Prüfstrecke, volle Suite, XFAIL-Bilanz

Schreibt § 10 fort. **Die Zahlen aus § 10 bleiben unverändert stehen** und werden
hier als „vorher" zitiert. Stand: `47df2d9` auf `selman/extents-ausreisser`,
**kein Push**.

### 12.1 Was gelaufen ist

| Lauf | Befehl | Ergebnis |
|---|---|---|
| Prüfstrecke | `.venv/Scripts/python.exe scripts/plan_pruefen.py` (alle fünf DXF in `Projekte/_eingang/`) | exit 0, fünf Pläne, Rohlog `…/scratchpad/_s3_pruefstrecke.log` |
| Volle Suite | `.venv/Scripts/python.exe -m pytest -q -rX` | `1200 passed, 10 skipped, 2 deselected, 11 xfailed, 2 warnings in 1148.43s (0:19:08)`, exit 0, Rohlog `…/scratchpad/_s3_pytest.log` |

**Diesmal nacheinander, nicht gleichzeitig.** Der Kritikpunkt aus § 10.1 ist damit
erledigt: die Laufzeiten unten sind echte Messwerte ohne Parallellast.

### 12.2 Prüfstrecke — Ist je Plan (Lauf `2026-09-10 13:35 · 47df2d9`)

| Plan | Stempel | Räume | Restflächen | Türen typisiert | Ausgänge | Segmente | Wohnungen | RZ / SL | Laufzeit |
|---|---:|---:|---:|---|---|---|---:|---|---:|
| Barawitzka_EG | 38 | 38 | 10 | 55/106 | final_exit 1 | GRAPH 11, FALLBACK 1 | 7 | 3 / 4 | 263,6 s |
| Mollgasse_EG | 83 | 83 | 2 | 70/147 | final_exit 9, stair_exit 4 | LINIE 103, GRAPH 19, FALLBACK 4 | 8 | 30 / 35 | 288,2 s |
| Muthgasse_E2 | 99 | 99 | 11 | 206/291 | final_exit 5, stair_exit 5 | LINIE 139, GRAPH 5, FALLBACK 2 | 8 | 65 / 28 | **1852,4 s** |
| Rennweg_EG | 19 | 19 | 2 | 24/41 | final_exit 3, stair_exit 5 | GRAPH 8, FALLBACK 1 | 2 | 5 / 10 | 58,3 s |
| Rennweg_OG3 | 10 | 10 | 4 | 15/27 | stair_exit 1 | GRAPH 5 | 2 | 1 / 2 | 51,6 s |

Legendenabdeckung unverändert (90,3 / 99,9 / 99,4 / 100,0 / 100,0 %). IoU-Mittel
weiterhin `—`: es liegt **keine** `<planname>.referenz.json` neben den DXF in
`Projekte/_eingang/`, also wird kein IoU berechnet — keine fehlende Messung, die
irgendwo ersetzt worden wäre. Flags 2 / 37 / 26 / 0 / 0. Unbekannte Muster
3 / 2 / 5 / 0 / 0. Referenzvergleich nur Barawitzka_EG: 2 Treffer / 9 fehlend /
5 überzählig (18 %). Alles unverändert gegen § 10.2.

### 12.3 Delta gegen den Lauf `e9837b0` (2026-09-10 04:48)

**Kennzahlen: kein einziger Wert bewegt sich, auf keinem der fünf Pläne.**
Stempel, Räume, Restflächen, Kaskade, Türen typisiert, Ausgänge, Segmente,
Wohnungen, Leuchten, Legendenabdeckung, Referenzvergleich — alle identisch zu
§ 10.2. Das ist das erwartete Ergebnis: die Schritte 1 und 2 dieses Auftrags
haben **keinen Code in `src/`** geändert (Schritt 1 nur
`tests/naht/test_soll_muthgasse.py` + Bericht, Schritt 2 nur
`docs/OFFENE_FRAGEN.md`).

**Laufzeiten dagegen schon** — und genau das ist der Punkt:

| Plan | § 10.2 (parallel zur Suite) | jetzt (lastfrei) | Delta |
|---|---:|---:|---:|
| Barawitzka_EG | 312,0 s | 263,6 s | −48,4 s |
| Mollgasse_EG | 369,1 s | 288,2 s | −80,9 s |
| Muthgasse_E2 | 2116,4 s | **1852,4 s** | −264,0 s |
| Rennweg_EG | 55,5 s | 58,3 s | +2,8 s |
| Rennweg_OG3 | 50,5 s | 51,6 s | +1,1 s |

Muthgasse liegt lastfrei bei **1852,4 s** gegen den lastfreien Vorbefund
**1838 s** (2026-09-09): **+14,4 s = +0,8 %**. Damit ist belegt, was § 10.2 nur
vermutet hat — die 2116,4 s waren Lastkontext, keine Verschlechterung der
Pipeline. Die Fußnote aus § 10.2 ist erledigt.

### 12.4 Volle Suite — Delta gegen § 10.1

| | vorher (§ 10.1) | jetzt |
|---|---|---|
| passed | 1199 | **1200** |
| skipped | 10 | 10 |
| deselected | 2 | 2 |
| xfailed | 10 | **11** |
| XPASS | 0 | **0** |
| failed | 0 | 0 |
| Laufzeit | 1648,74 s (27:28) | 1148,43 s (19:08) |

Die beiden neuen Einträge kommen beide aus Schritt 1 dieses Auftrags und beide
aus `tests/naht/test_soll_muthgasse.py`: `test_soll_echte_blocktueren_im_modell`
(**passed**, +1) und `test_soll_stair_exit_aus_echter_blocktuer` (**xfail**, +1).
Die kürzere Laufzeit ist derselbe Lasteffekt wie in § 12.3, in die andere
Richtung: der Vorlauf lief parallel zur Prüfstrecke.

### 12.5 XFAIL-BILANZ — 11 strict-xfails, **kein einziger zu XPASS gedreht**

`pytest -q -rX` meldet `11 xfailed` und **keine** XPASS-Zeile (`-rX` würde jede
ausweisen). Bei `strict=True` wäre ein XPASS ein Suite-Fehler; die Suite ist
grün.

| # | Test | Datei:Zeile | Warum er xfail ist |
|---|---|---|---|
| 1 | `test_soll_explizite_linien_vorhanden` | `tests/naht/test_soll_barawitzka.py:65` | Der Plan hat keine expliziten Fluchtweg-Linien — die 16 Farbe-96-Linien sind Katastergrenzen; das Zielbild wartet auf einen Plan-Nachtrag des Fachplaners, nicht auf Code. |
| 2 | `test_soll_90_prozent_tueren_typisiert` | `tests/naht/test_soll_barawitzka.py:76` | Soll ≥ 90 % typisierte Türen je Familie, Ist 55/106 — Hauptlücke `unbekannte_kombination` / `kein_nachbarraum`. |
| 3 | `test_soll_16_endpunkte_an_der_aussenkante_gedeckt` | `tests/naht/test_soll_barawitzka.py:104` | Folgt aus #1: ohne echte FLW-Linien gibt es 0 Endpunkte an der Außenkante, also auch 0 gedeckte. |
| 4 | `test_soll_jeder_endpunkt_an_der_kante_hat_final_exit` | `tests/naht/test_soll_mollgasse.py:111` | Der `09-WEG`-Layer zeichnet Doppellinien-Stummel; ohne Dedup/Clustering der Endpunkte deckt die `final_exit`-Menge nur einen Bruchteil der Kandidaten. |
| 5 | `test_soll_90_prozent_tueren_typisiert` | `tests/naht/test_soll_mollgasse.py:125` | Soll ≥ 90 %, Ist 70/147 — Nachbarräume ohne Kanon-Typ. |
| 6 | `test_soll_final_exit_anzahl_gleich_endpunkte_an_der_kante` | `tests/naht/test_soll_mollgasse.py:159` | Dieselbe Ursache wie #4, als Zählgleichung formuliert: 9 `final_exit` gegen 43 Endpunkte. |
| 7 | `test_soll_stair_exits` | `tests/naht/test_soll_muthgasse.py:112` | Soll ≥ 9 `stair_exit`, Ist 5. Band **bewusst nicht abgesenkt** — der einzige durch Messung gedeckte Ersatzwert wäre der Ist-Stand selbst, und aus dem Ist abgeleitete Bänder sind hier verboten (§ 11.5). |
| 8 | `test_soll_stair_exit_aus_echter_blocktuer` | `tests/naht/test_soll_muthgasse.py:187` | Der fachlich belegte Ersatz zu #7: Soll ≥ 1 `stair_exit` an einer echten `A-DOOR`/`A-GLAZ`-Blocktür, Ist 0 von 5 — alle fünf ruhen auf Kontaktzonen-Artefakten. Zielwert aus `tuer_50`, nicht aus dem Ist. **Korrigiert in § 13.7: `tuer_50` ist keine Blocktür (780,5 mm zum nächsten `A-DOOR`-INSERT), der Anker ist widerlegt; Band unverändert.** |
| 9 | `test_soll_90_prozent_tueren_typisiert` | `tests/naht/test_soll_muthgasse.py:230` | Soll ≥ 90 %, Ist 206/291 = 70,8 % — Türen ohne typisierte Gegenseite. |
| 10 | `test_soll_referenz_trefferquote` | `tests/naht/test_soll_referenzvergleich.py:57` | Zielbild ≥ 80 % Deckung gegen die Fachplaner-Leuchten, Ist 18 % — die Platzierungs-Strategien (Lane @mvpo3) sind noch nicht referenz-deckend. |
| 11 | `test_soll_eg_90_prozent_tueren_typisiert` | `tests/naht/test_soll_rennweg.py:138` | Soll ≥ 90 %, Ist 24/41 — Gründe-Tabelle in `bericht.md`. |

**Ausdrücklich, weil danach gefragt wurde:**

- **Zu XPASS gedreht wurde in diesem Auftrag KEIN xfail.** Nicht einer. Es gibt
  keine XPASS-Zeile im Log.
- **Abgesenkt oder sonst geändert wurde in diesem Auftrag KEIN Zielband.** Das
  Band von `test_soll_stair_exits` steht unverändert bei `>= 9`, obwohl die
  Analyse aus Schritt 1 eine Absenkung auf 5 vorgeschlagen hatte — abgelehnt,
  Begründung in § 11.5. Geändert wurde dort nur der `reason`-Text (er behauptete
  eine widerlegte Ursache) und ein Docstring.
- **Neu hinzugekommen ist genau einer:** #8, ein **zusätzlich sichtbar
  gemachter** Befund mit einem aus `tuer_50` abgeleiteten, nicht aus dem Ist
  abgeleiteten Zielwert. Kein Zielbild ist gefallen.
- Damit: 9 xfails im Ausgangsstand → 10 nach dem Abschluss-Schritt der
  Vorrunde (`test_soll_stair_exits`) → **11** nach Schritt 1 dieses Auftrags.

### 12.6 Was in diesem Schritt ausdrücklich nicht gemacht wurde

- Kein Push, kein PR, kein Merge — der Owner gibt das GO separat.
- **Keine Contract-Änderung.** `hauptengine/contracts/**` ist unberührt; der
  laufende Bump `raum_modell` 1.3.0 → 1.4.0 wartet weiter auf das Approval von
  @EnisAMG.
- Kein Code in `src/` geändert — dieser Schritt ist Messung und Bericht.
- Die offenen Befunde aus § 10.6 und § 11.6 bleiben offen: die 3 Nebenbefunde
  (Manhattan-Dedupe, Regel bei `von_raum == nach_raum`, 9 STIEGENHAUS-Polygone =
  höchstens 4 Kerne), die Nennerfrage Muthgasse `A-DETL`, die 12
  Mollgasse-Segmente ohne lichtes Polygon (`docs/OFFENE_FRAGEN.md`, mit der
  Fluchtwegbreiten-Frage an @EnisAMG).

---

## 13. Nachtrag 2026-09-10 — Punkt 3 des Owner-Auftrags: `raum_65` (Muthgasse E2)

Auftrag: „Wenn der Typ ableitbar ist, umsetzen und den Test scharf schalten."
**Ergebnis: nicht umgesetzt, xfail bleibt.** Der Typ ist im Plan belegt, aber
das passende Label existiert im Kanon nicht — die Festlegung gehört in
`normwissen/` (@EnisAMG), nicht in `raumerkennung/`. Begründung unten, Fragen
in `docs/OFFENE_FRAGEN.md`.

Codestand `c7b52df`. `git diff --stat 1d9c03a..HEAD -- src/` ist leer, deshalb
ist der Vorsessions-Provider-Dump `_p2_nachher.json` (291 Türen / 113 Räume)
für HEAD gültig und wurde wiederverwendet statt neu zu parsen.
Prüfstrecken-Zahlen aus `Projekte/_ergebnis/*/raeume.json` (Lauf `47df2d9`,
2026-09-10 13:35). Messskripte (Session-Scratchpad, alle nur lesend, in diesem
Schritt erneut gelaufen): `_r65_umfeld.py`, `_r65_vokabular.py`, `_r65_vf.py`,
`_r65_tuer50.py`, `_r65_falschtreffer.py`, `_untyp_tabelle.py`.

### 13.1 Steckbrief `raum_65`

| Feld | Wert | Beleg |
|---|---|---|
| Fläche | 13,04 m² | `raeume.json`, `_p2_nachher.json` |
| Polygon | 15 Punkte, bbox 333153…337815 × 106351…111004 mm (4,66 × 4,65 m), L-förmig um den Stiegenkern | `_r65_umfeld.py` |
| Zentrum | 335 283 / 108 862 mm | `bericht.md:126` |
| Kaskaden-Zweig | **L** (`raeume_aus_layer`), `flag=kein_stempel` | `raeume.json` `quelle:"L"` |
| DXF-Herkunft | LWPOLYLINE Handle `73B8`, Layer `A-AREA-BNDY`, closed, 15 Stützpunkte, IoU 1,0000 gegen das Modell-Polygon | `_r65_umfeld.py` |
| `raum_typ` | `''` (leer) | Dump |
| `nutzungsklasse` | `None` | Dump |
| Nachbarn (≤ 300 mm) | `stiegenhaus_1…5` (STIEGENHAUS, je 0 mm), `raum_46` GANG (180 mm), `raum_52` (untypisiert, 180 mm), `raum_89` BAD (267 mm) | `_r65_umfeld.py` |
| Türen | 7 (`tuer_50`, `tuer_91`, `tuer_119`, `durchgang_120/140/141/142`), 3× `unbekannte_kombination`, 3× `beide_seiten_untypisiert` | `bericht.md:538,579,607,729,749-751` |

Im Polygon liegen 49 Texte; vier davon bilden auf `A-AREA-IDEN` die vollständige
Stempelgruppe: `E2-VF-11a` (Nummer), `Schl.` (Name), `13,04 m²` (Fläche,
deckungsgleich mit dem Polygon), `Ker.Bel.` (Belag) — alle vier innerhalb
194–360 mm zueinander, weit innerhalb des Stempelradius von 1500 mm.

### 13.2 Geprüfte Ursachen — drei widerlegt, eine belegt

- **„Kein Stempel im Polygon" — widerlegt.** Der Stempel ist vollständig und
  liegt mittendrin (Abstand 0 mm).
- **„Kein Polygon aus Layer oder HATCH" — widerlegt.** Echtes geschlossenes
  Architekten-Polygon auf `A-AREA-BNDY` (im Kanon der Raum-Layer,
  `raumlayer.py:34-35`), IoU 1,0. Der Plan hat 160 solche Entities und 0 HATCH
  auf Raum-Layern.
- **„Restfläche ohne greifende Regel" — strukturell ausgeschlossen.**
  `rest_komponenten.komponenten_ohne_stempel` sieht `raum_65` nie:
  `kaskade.py:145` übergibt alle L/H/F-Polygone als `belegte`,
  `rest_komponenten.py:147-152` maskiert sie (100 mm Puffer) aus dem Raster.
  Muthgasse hat folgerichtig R:0; die drei Geometrieregeln
  (`rest_komponenten.py:89-102`) laufen für `raum_65` nie.
  `nutzungsklasse.py:54-56` ist reine Nachschlagetabelle `raum_typ →
  Nutzungsklasse` und liefert ohne `raum_typ` `None`.
- **Vokabular-Lücke — das ist die Ursache, belegter Regelpfad.**
  `stempel_anker.finde_stempel` (`:230-245`) sieht `A-AREA-IDEN` layerunabhängig,
  Anker ist der m²-Text. `Ker.Bel.` wird als Belag erkannt; Kandidaten bleiben
  `Schl.` und `E2-VF-11a`. In `stempel_anker.py:219-221` gilt
  `name_frag = next((f for f in kandidaten if _typ(f[0])), None)` und bei `None`
  ein `continue`. Gemessen: `raumtyp_flags('Schl.') = None`,
  `raumtyp_flags('E2-VF-11a') = None`, `classify_room('Schl.') =
  RoomType.UNKNOWN` — `schl` steht in keinem der drei Wörterbücher
  (`raumtyp.py` `_EXTRA_LABELS:65`, `_EXTRA_DIRECT:95`, `_EXTRA_OVERRIDE:125`).
  ⇒ Es entsteht **gar kein `Stempel`**, deshalb `flag=kein_stempel`, deshalb
  kein `Zuordnung`-Eintrag, deshalb greift die Rückschreibung
  `kaskade.py:118-128` nicht.

Dasselbe Muster trifft alle zehn untypisierten Muthgasse-Räume — jeder trägt
einen vollständigen `A-AREA-IDEN`-Stempel mit einem Namen außerhalb des Kanons:
`Vorr.` (raum_48/59/70), `SR` (raum_52/71), `Schrankr.` (raum_61), `Schl.`
(raum_65/67), `Aufzug 1`/`Aufzug 2` (raum_77/78).

**Der Code hat sich korrekt verhalten: er hat einen Text nicht erfunden, den er
nicht kennt.**

### 13.3 Was der Plan über `raum_65` hergibt

- Name `Schl.`, Nummer `E2-VF-11a`.
- Das Nummernpräfix `VF` trägt in diesem Plan ausschließlich Verkehrsflächen
  (`_r65_vf.py`, über alle nummerierten Stempelgruppen): `E2-VF-12` = `STGH`,
  `E2-VF-13a/b/c` = `Gang`, `E2-VF-15a/b/c` = `Aufzug 1`/`Aufzug 2`/`FW-Aufzug`,
  `E2-VF-12a` = `Podest 2.OG/1.OG`, `E3-VF-12b/c` = `Stiege`, `E2-VF-11a/b` =
  `Schl.`. **Null** Wohnungsräume unter `VF`; Wohnungsräume tragen durchweg eine
  Top-Nummer (`E2-7-…`, `E2-9-…`), Nutzflächen `NF`.
- Umfeld stützt dasselbe: 13,04 m², direkt an fünf STIEGENHAUS-Polygonen und an
  `raum_46` GANG, mit `EI ₂ 30-C`-Türtexten an beiden Durchgängen.
- ⇒ `Schl.` = **Schleuse** (Brandschutzschleuse vor dem Stiegenhaus), nicht
  Schlafzimmer. Ein Schlafzimmer trüge eine Top-Nummer und keinen `Ker.Bel.`
  zwischen zwei Brandschutztüren.

### 13.4 Warum trotzdem kein Code in unserer Lane

1. `SCHLEUSE` existiert im Kanon nicht (`docs/VOKABULAR.md` § 1, Zeilen 17–39
   vollständig geprüft). Ein neuer Kanon-Typ plus Nutzungsklasse plus
   Notlicht-Konsum ist `normwissen/` (@EnisAMG) bzw. `platzierung/` (@mvpo3).
2. Die Abkürzung `Schl.` löst der *Leser* auf, nicht der Plan — sie wird
   nirgends ausgeschrieben. Ein Wörterbucheintrag `schl → …` ist eine fachliche
   Festlegung, keine Messung.
3. Ersatzweise `GANG` zu setzen wäre genau das verbotene Raten: eine Schleuse
   ist kein Gang, und der Unterschied entscheidet über die Nutzungsklasse und
   damit über eine Leuchte an falscher Stelle.

**Untypisiert ist für `raum_65` das korrekte Ergebnis, solange die
Vokabular-Frage offen ist.**

### 13.5 Falschtreffer-Messung (der (c)-Teil, vorsorglich)

`_r65_falschtreffer.py`, token-exakt über alle Texte und ATTRIBs aller fünf
Pläne. „Falschtreffer" = Treffer ohne m²-Nachbar, also kein Raumstempel:

| Kandidat-Token | Bara. | Moll. | Muth. | Renn_EG | Renn_OG3 | Falschtreffer |
|---|--:|--:|--:|--:|--:|---|
| `schl` | 0 | 0 | 2 (`Schl.`) | 0 | 0 | **0 auf allen fünf Plänen** |
| `vorr` | 0 | 0 | 9 (`Vorr.`) | 0 | 0 | 0 |
| `schrankr` | 0 | 0 | 1 | 0 | 0 | 0 |
| `sr` | 1 | 1 | 3 | 0 | 0 | 0 |
| `aufzug` | 10 | 2 | 3 | 1 | 1 | **11** (Kabinen-/Bedienfeldtexte, Maßketten) |
| `stiege` | 4 | 0 | 4 | 0 | 0 | **4** (Barawitzka `STIEGE 2 EINGANG`) |
| `podest` | 0 | 8 | 1 | 0 | 0 | **4** (Höhenkoten `FOK PODEST = +1.18`) |

Ein Eintrag `schl` erzeugte auf den anderen vier Plänen null Falschtreffer. Das
Risiko liegt also nicht in der Regel, sondern im **Label**: welcher Kanon-Typ
und welche Nutzungsklasse einer Schleuse zustehen. `aufzug`, `stiege`, `podest`
sind dagegen echte (c)-Fälle und ohne m²-Kontextbedingung nicht sicher.

### 13.6 Untypisierte Räume über alle fünf Pläne (`_untyp_tabelle.py`)

Quelle `Projekte/_ergebnis/<Plan>/raeume.json`, Lauf `47df2d9`. „Untypisiert" =
`typ` leer oder `UNBEKANNT`. „ohne Zweig" = Stempel ohne Polygon
(`flag=kein_polygon`).

| Plan | Räume ges. | untypisiert | % | untypisiert je Zweig | Räume je Zweig |
|---|--:|--:|--:|---|---|
| Barawitzka_EG | 48 | 6 | 12,5 % | L:1 H:4 F:0 R:1 | L:2 H:40 F:2 R:3 |
| Mollgasse_EG | 85 | 28 | 32,9 % | L:0 H:8 F:11 R:0 + 9 ohne Zweig | L:0 H:10 F:52 R:0 |
| Muthgasse_E2 | 110 | 10 | 9,1 % | L:10 H:0 F:0 R:0 | L:80 H:1 F:20 R:0 |
| Rennweg_EG | 21 | 5 | 23,8 % | L:5 H:0 F:0 R:0 | L:19 H:0 F:0 R:2 |
| Rennweg_OG3 | 14 | 1 | 7,1 % | L:0 H:0 F:0 R:1 | L:10 H:0 F:0 R:4 |
| **Summe** | **278** | **50** | **18,0 %** | | |

Charakter der Lücken:

- **Barawitzka**: 5 × `kein_stempel` + 1 R-Rest 3,40 m².
- **Mollgasse**: fast alles Vokabular/Außenraum — `EIGENGARTEN TOP 1-3`,
  `GESCHÄFTSLOKAL`, `KLEINKINDERSPIELPLATZ`, `PODEST`, `GEHWEG`, `VORPLATZ`,
  `STAUDENBEET`, `GARAGENRAMPE`, `AUFZUG 8 PERS.`, `SR`; 9 davon ohne Polygon.
- **Muthgasse**: ausschließlich L-Zweig, ausschließlich `kein_stempel`,
  ausschließlich die Vokabular-Lücke aus § 13.2.
- **Rennweg_EG**: 5 × Vokabular (`Müllplatz`, `Geschäftslokal 1`,
  `GESCHÄFTLOKAL`, `Zugangsweg`, `Garageneinfahrt`), alle `flag=ok` — Polygon
  und Fläche korrekt, nur der Typ fehlt.
- **Rennweg_OG3**: 1 R-Rest 10,09 m².

**Abgleich mit der Prüfstrecken-Kennzahl „Rest typisiert / untypisiert".**
`scripts/plan_pruefen.py:1399-1400` zählt über `rest_r`, und `rest_r` ist
ausschließlich der R-Zweig (`kaskade.py:151`). Die Kennzahl misst also nicht
„untypisierte Räume", sondern „untypisierte Rest-Komponenten". Gegenprobe aus
denselben `raeume.json`:

| Plan | R-Räume | gemessen typisiert / untypisiert | VERLAUF.md `47df2d9` |
|---|--:|---|---|
| Barawitzka_EG | 3 | 2 / 1 | „2 / 1" ✔ |
| Mollgasse_EG | 0 | 0 / 0 | „0 / 0" ✔ |
| Muthgasse_E2 | 0 | 0 / 0 | „0 / 0" ✔ |
| Rennweg_EG | 2 | 2 / 0 | „2 / 0" ✔ |
| Rennweg_OG3 | 4 | 3 / 1 | „3 / 1" ✔ |

Fünf von fünf identisch — die Kennzahl ist richtig, sie beantwortet nur eine
andere Frage. Muthgasse meldet „0 / 0" und hat gleichzeitig 10 untypisierte
Räume, weil alle 10 aus dem L-Zweig kommen und der R-Zweig leer ist. Auch
„Restflächen 11" ist etwas anderes: `rest_n` (`:1406`) = `restflaechen(...) +
rest_r` = Polygone ohne Stempel aus allen Zweigen = 10 L + 1 H. *Nebenbefund,
nicht Teil des Auftrags:* der Kennzahlname ist für das Gemessene irreführend;
Umbenennen wäre Prüfstrecken-Kosmetik und wurde hier nicht angefasst.

### 13.7 Korrektur an § 11.5 / § 12.5: `tuer_50` ist keine Blocktür

Der strict-xfail `test_soll_stair_exit_aus_echter_blocktuer`
(`tests/naht/test_soll_muthgasse.py`) zählt über `_tueren_auf_blocktuer` nur
Türen, die auf einem `A-DOOR`/`A-GLAZ`-INSERT ± 2 mm sitzen. Gemessen
(`_r65_tuer50.py`, 209 solche INSERTs im Plan):

```
A-DOOR/A-GLAZ-INSERTs: 209
tuer_50 @(334453,106403) auf Blocktuer: False []
   naechster A-DOOR/A-GLAZ-INSERT: (334077, 107087,
   'HNP_T_BZ_2-DF - HNP_T44_BZ-A_A_EI_30-C_2DF_150_5x200-V455-E 2 - FOK AF 300',
   'A-DOOR') d=780.5 mm
```

`tuer_50` stammt aus `quelle='arc_aussen+text:E2-VF-12a'`, also aus einem ARC,
nicht aus einem Block-INSERT. Die Aussage in § 11.5 („wäre der Typ da, gäbe es
mindestens einen `stair_exit` aus einer echten Blocktür") und der daraus
abgeleitete Zielwert-Anker in § 12.5 Zeile #8 beruhen auf einer Verwechslung:
dort war „nächster Abstand einer echten Blocktür zu einem STIEGENHAUS-*Polygon*
= 0 mm" gemessen — das ist `tuer_22`, und ihr 0-mm-Nachbar ist `raum_88`, der
Artefaktraum aus § 11.4, nicht `stiegenhaus_1`.

Vollzähliger Gegenbeweis, alle 18 echten Blocktüren mit ihren Nachbarn
(`_r65_tuer50.py`): `tuer_1` WC→GANG, `tuer_2` KEIN_RAUM→BAD, `tuer_3`
ZIMMER→KEIN_RAUM, `tuer_4` KEIN_RAUM→KÜCHE, `tuer_5/6` GANG→KÜCHE, `tuer_7`
GANG→VORRAUM, `tuer_8` BALKON→KÜCHE, `tuer_9` KEIN_RAUM→VORRAUM, `tuer_10`
GANG→ABSTELLRAUM, `tuer_11/12/13` GANG→raum_70/59/48 (untypisiert, alle
`Vorr.`), `tuer_14/15` KÜCHE→AUSSEN, `tuer_16` ZIMMER→AUSSEN, `tuer_17`
AUSSEN→ZIMMER, `tuer_22` BAD→GANG. **Keine einzige hat eine STIEGENHAUS-Seite.**
Die drei mit untypisierter Gegenseite hätten mit einem Typ `VORRAUM`
(`WOHNUNG_PRIVAT`) `wohnungseingang` und damit ebenfalls keinen `stair_exit`.

**Folge: Ein Typ auf `raum_65` hätte diesen xfail auch dann nicht gedreht, wenn
wir ihn hätten setzen dürfen.** Der Test bleibt strict-xfail; Band unverändert,
nicht abgesenkt. Geändert wurden nur `reason` und Docstring, weil beide eine
widerlegte Ursache behaupteten.

Ergänzend für `test_soll_stair_exits` (Band ≥ 9) gemessen, was ein Typ auf
`raum_65` über `tuer_typisierung.py:152-156` / `ausgaenge.py:62-64` bewirken
würde:

| hypothetischer Typ | Nutzungsklasse | Wirkung auf `tuer_50` |
|---|---|---|
| GANG / STIEGENHAUS / AUFZUGSVORPLATZ | ALLGEMEIN_ERSCHLIESSUNG | `stiegenhaustuer` → +1 `stair_exit` |
| VORRAUM | WOHNUNG_PRIVAT | `wohnungseingang` → kein `stair_exit` |
| ABSTELLRAUM | WOHNUNG_PRIVAT | kein `stair_exit` |

### 13.8 Was in diesem Schritt gemacht und was nicht gemacht wurde

Gemacht: Messung, dieser Befund, die Vokabular-Fragen in
`docs/OFFENE_FRAGEN.md`, Korrektur von `reason` und Docstring des xfail.

Nicht gemacht: keine Änderung an `raumtyp.py`, `nutzungsklasse.py`,
`stempel_anker.py` oder sonst in `src/`; kein xfail scharf geschaltet; kein
Zielband geändert; keine Contract-Änderung (`hauptengine/contracts/**`
unberührt, `raum_modell` 1.4.0 wartet weiter auf das Approval von @EnisAMG);
kein Push, kein PR, kein Merge.
