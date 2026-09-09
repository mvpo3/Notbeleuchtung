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
- Enis' Test `test_kein_contract_wert_und_kein_konsument` ist rot, weil unser `breitenprofil.py` die RL-4-YAML im Docstring **zitiert**. Nicht einseitig geändert — es ist Enis' Test.
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

**Einordnung.** Kein Sachfehler. Der Test ist ein Wächter „diese YAML hat noch keinen Konsumenten" und prüft per **Textsuche über den Dateiinhalt**, nicht über den Import-/Ladepfad. Getroffen wird `src/notbeleuchtung/raumerkennung/breitenprofil.py`, deren Modul-Docstring (Zeilen 4–7) `normwissen/data/oib_rl4_fluchtwegbreiten.yaml`, Abschnitt `breiten_begriffe`, als Quelle **zitiert**. Ein echter Konsument existiert nicht. Vorschlag zur Entscheidung mit Enis: Prüfung auf Import statt auf Substring, oder Docstring-Referenz umformulieren. Nicht einseitig geändert.

### 2.4 Volle Suite

| Lauf | Ergebnis |
|---|---|
| `python -m pytest -q` (Repo-Root, unveränderter Baum) | **1 failed, 1176 passed, 10 skipped, 2 deselected, 9 xfailed** in 1228,44 s |
| `pytest --collect-only -q` | 1196/1198 tests collected |
| `pytest tests/raumerkennung tests/contract -q` | 283 passed, 5 skipped (188,04 s) |
| `ruff check src tests` | All checks passed! |

Der einzige Fehlschlag ist der aus § 2.3. Weitere vorbestehende rote Tests: keine.

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
| Barawitzka_EG | **UNGEPRUEFT** | 0 Fenster-Layer, 0 Fenster-Blöcke, 0 INSERTs im Modelspace; einziges Glas-Signal 4 Texte |

Contract-Folge (**VORSCHLAG**, siehe § 8): drei additive Felder in `Raum`, alle Default `None`, `CONTRACT_VERSION` 1.3.0 → 1.4.0, Schema-Regenerierung `scripts/gen_schema.py`. Kein Erzeuger bricht. Ob `belichtung_vollstaendigkeit` besser auf `RaumModell`-Ebene sitzt (es ist eine Plan-Eigenschaft), ist eine Owner-Entscheidung und hier bewusst offen gelassen.

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

---

## 7. Was ist umgesetzt / was fehlt

| Punkt | Umgesetzt | Fehlt |
|---|---|---|
| **0 — Paketübernahme** | 7 Dateien hash-identisch im Arbeitsbaum, 2 Diffs angewandt, WIP-Commit `a9ab1b6` | Archiv-Hash nicht prüfbar (§ 2.1); 2 Listeneinträge aus dem `oib_rl2_tabelle6.yaml`-Diff nicht angekommen (§ 3.2); Widerspruch `astv_arbeitsstaetten.yaml:271` vs. § 11.1 nicht nachgezogen (Enis' Datei) |
| **1 — natürliche Belichtung** | Ist-Stand vollständig erhoben, alle 5 Pläne gemessen, Fensterherkunft je Familie belegt, Regeln True/False/None und drei Feldvorschläge formuliert | **Kein Code.** Contract-Felder `natuerlich_belichtet`, `belichtung_quelle`, `belichtung_vollstaendigkeit` sind Vorschlag. GLASWAND als eigenständige Quelle ungemessen, 500-mm-Toleranz unkalibriert, Arbeitsraum-Eigenschaft (AStV § 1 Abs. 4) fehlt vollständig |
| **2 — Breitenverlauf** | `breitenprofil.py` repariert (3 Ursachen), +62/−21 in 2 Dateien, 9 Tests grün, 283 passed / 5 skipped in der Regression, ruff grün, alle 5 Pläne gemessen, 2 Belegprofile | **Keine Anbindung**: kein Provider-Aufruf, kein Contract-Feld. `FluchtwegSegment`-Ergänzung ist Vorschlag. 61 Segmente ohne schneidendes Raumpolygon (unsere Lane). Eckfenster verwirft auf GRAPH-Segmenten weiter den Großteil des Profils |
| **3 — `Tuer.breite_mm`** | 9 Schreibpfade belegt, Herkunft je Plan über 629 Türen ausgezählt, Ursache der 132 Nullen belegt, DL-Beschriftungsfund Muthgasse, Migrationsreihenfolge + gemessene Bruchstellen | **Kein Code.** `breite_quelle`, `lichte_mm`, `lichte_quelle`, `breite_mm: float \| None` sind Vorschlag. Schritt 0 (None-Festigkeit der Konsumenten) nicht ausgeführt. Testauswirkung nur auf 27 % der Suite erhoben. ATTRIB-Befund für Barawitzka/Rennweg nicht messbar. Muthgasse-Aufteilung BLOCKNAME/SCHWENKRADIUS auf ±1 unsicher |
| **Querschnitt** | — | Enis' Test `test_kein_contract_wert_und_kein_konsument` rot (§ 2.3), nicht einseitig geändert |

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
12. **Dein Test:** `test_kein_contract_wert_und_kein_konsument` prüft per Substring über Dateiinhalte und trifft eine bloße Docstring-Quellenangabe. Import-/Ladepfad-Prüfung statt Substring, oder sollen wir die Referenz aus dem Docstring nehmen? Nicht einseitig geändert.

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
| Kalibrierung der 500-mm-Belegtoleranz | nicht durchgeführt |
| ATTRIBs an Tür-Blöcken, Barawitzka + Rennweg EG/OG3 | 0 Tür-Blöcke im Modelspace; der Scan geht nicht in Blockdefinitionen (§ 6.2) |
| Testauswirkung der `None`-Migration auf 877 der 1196 Tests | Probelauf umfasste nur 319 Tests (§ 6.3) |
| Ob `origin/main` remote weitergelaufen ist | kein `git fetch` ausgeführt; `origin/main = fd65839` ist der lokal gespiegelte Stand |
