# Übernahme des Diagnosepakets M17 von Enis — Rennweg 15, OG1

Stand: 2026-09-18 · Owner: Selman (`src/notbeleuchtung/raumerkennung/`) · Diagnosebasis
`selman/rennweg-stand` @ `f15d03fe1a082c78b180e940b7dcd666fccaf37d`

Dieses Dokument ist die Übernahme eines **lokalen** Pakets von Enis. Es enthält **keine
Paketinhalte**, nur Pfade, Prüfsummen und Verweise. Die Übernahme umfasste ausschließlich
Lesen, Prüfen und Einordnen: **kein neuer Erkennungslauf, keine Algorithmusänderung, kein
Commit, kein Push.** Die einzige Rechnung, die eigenen Code ausführt, ist in Abschnitt 4
offengelegt (eine Einzelfunktion auf exportierter Geometrie, ohne DXF-Parsing).

---

## 1. Wo die Unterlagen liegen

Das Paket liegt **außerhalb des Arbeitsbaums** und wird nicht ins Repository übernommen:

```
Archiv:   C:\Users\selma\Downloads\Telegram Desktop\Uebergabe_Selman_M17_Rennweg_OG1_2026-09-18_0010.zip
Entpackt: D:\KI Projekt\_uebergabe_enis_M17\Uebergabe_Selman_M17_Rennweg_OG1\
```

### Prüfung des Pakets (2026-09-18)

| Prüfung | Ergebnis |
|---|---|
| SHA-256 des Archivs | `6e3ef04255219870ab63dc03ca103a9fec1bec4f7c978d52d494a574a97bc915` — **stimmt** mit der Vorgabe, 19.569.224 Byte |
| `sha256sum -c PRUEFSUMMEN.txt` (aus dem Ordner **über** dem Wurzelordner) | **56 von 56 Dateien OK**, keine Abweichung |
| `PAKET_MANIFEST.json` gegen die entpackten Dateien | **41 von 41 Einträgen** mit passender SHA-256 und Byte-Größe; keine Datei im Ordner ohne Manifest-Eintrag, kein Manifest-Eintrag ohne Datei |
| Bestehende Dateien | keine überschrieben (Zielordner war neu und leer, Entpacken ohne Overwrite-Flag) |

### Welche Datei wofür dient

**Einstieg und Gesamtbild**

| Datei | Zweck |
|---|---|
| `EINSTIEG_SELMAN.md` | Einstiegspunkt der Übergabe: Lesereihenfolge, Diagnosebasis, Statusübersicht, der belegte Fall M17-02-b, Nachrechen-Anleitung |
| `PRUEFSUMMEN.txt` | SHA-256 je Paketdatei (ohne sich selbst) |
| `01_Referenzpaket/README_START_HIER.md` | Einstieg ins Referenzpaket; präzisiert die Arbeitsbasis (`selman/rennweg-stand` statt `main`) |
| `01_Referenzpaket/PAKET_MANIFEST.json` | Inventar des Referenzpakets: 41 Einträge mit Pfad, Bytes, SHA-256, Herkunft |

**Fachreferenzen (Enis' Plandeutung, kein Testergebnis)**

| Datei | Zweck |
|---|---|
| `01_Referenzpaket/01_Fachreferenzen/Raumerkennung_Enis_01..13_*.md/.pdf` | Je ein Raum bzw. Bereich des OG1 (Stiegenhaus, WC, Abstellraum, Wohnküche, drei Zimmer, Gang, zwei Bäder, Vorraum/Garderobe, Balkon) mit markierter Kontur in PDF-Punkten, Stempelwert aus dem Plan und fachlicher Aussage |
| `…_14_Rennweg_Gesamtuebersicht.md/.pdf` | Zusammenführung 01–13: 16 Bereiche R01–R16, 10 Türbeziehungen T01–T10, 5 offene Übergänge O01–O05, Zwischenbereich E ungeklärt, dokumentierte Geometriedifferenz O03 |
| `…_15_Rennweg_Mauern.md/.pdf`, `…_16_Rennweg_WC_Mauergrenzen.md/.pdf` | Mauer-Kapitel: welche Linien Wand sind und welche nicht (Projektion, Schwelle, Türblatt, Schrank, Geländer) |
| `…_17_Rennweg_Mauern_Prueffaelle.md/.pdf/.json` | **Der Prüffall-Datensatz.** Sechs Fälle M17-01 bis M17-06 mit je drei Erwartungen (18 IDs), Sonden in PDF-Punkten und WCS, 16 aufgelöste DXF-Handles mit INSERT-Pfaden, Koordinatenbrücke `pdf_xy = linear · wcs_xy + translation` (Rotation 23,363542°, max. Registrierungsfehler 3,5 × 10⁻⁵ pt) |
| `01_Referenzpaket/02_Plangrundlage/OG1-Rennweg15-2026-06-12.dxf` | Eingabe-DXF, SHA-256 `c64e73e3…245e`, 4.072.038 Byte |
| `01_Referenzpaket/02_Plangrundlage/Rennweg_1OG_ohne_Masse.pdf` | Plan-PDF, auf das sich alle Referenzkoordinaten beziehen (SHA-256 `e8252f2f…3bb1`) |
| `01_Referenzpaket/03_Selman_Referenzausgabe_59583ff/` | Unsere eigene Ausgabe als Vergleichsgrundlage: `Rennweg_v2_OG1_uebersicht.png` (umbenanntes `uebersicht.png`) und `quelle.json` mit Branch, `retrieved_commit`, `calculation_commit`, Bild-Blob und Kennzahlen |
| `01_Referenzpaket/00_Auftrag/…Diagnoseauftrag_M17_01_02_2026-09-17.md` | **Historischer** Arbeitsauftrag. Hintergrund, nicht erneut auszuführen; in Teilen durch Fassung 2 überholt (Abschnitt 6) |

**Diagnose Fassung 2 (maßgeblicher Abschluss)**

| Datei | Zweck |
|---|---|
| `02_Diagnose_Fassung2/README.md` | Lauf-Identität, was gemacht und was nicht gemacht wurde, Laufumgebung, Reproduktionsbefehle |
| `02_Diagnose_Fassung2/BEFUND.md` | Die sechs Prüfungen mit Soll/Ist/Status, der Nachweis zu M17-02-b bis zur Codestelle, Korrekturen gegenüber Fassung 1 |
| `02_Diagnose_Fassung2/OFFEN.md` | Was offen bleibt, Gesamtbilanz 4/1/13, bewusst nicht Entschiedenes |
| `02_Diagnose_Fassung2/SICHERUNGSINFO.md` | Verhältnis der drei Sicherungsordner auf Enis' Rechner (Fassung 1, abgebrochener Lauf, Fassung 2) |
| `02_Diagnose_Fassung2/export/m17_export.json` | 468 KB Diagnoseexport: Plan, Geschoss, 196 Wandkörper, technische Wand-Union (Puffer 25 mm), Kaskade `L:15 H:0 F:0 R:2`, 18 Räume, 28 Türen, Sonden, T-Knoten |
| `02_Diagnose_Fassung2/export/m17_kontaktzone.json` | Kontaktzone `raum_6`/`raum_7`, die vier freien Streifen mit Abstand zu **beiden** Räumen, Zuordnung zu den Durchgängen |
| `02_Diagnose_Fassung2/bilder/M17_Planvergleich.pdf` | Vier-Feld-Planvergleich, stellt dar und bewertet nicht |
| `02_Diagnose_Fassung2/helfer/m17_export.py` | **Einziges** Skript mit Erkennungslauf (`provider.parse`, Monkeypatch wie in `raumerkennung_darstellung._erkennen`) |
| `…/helfer/m17_kontaktzone.py`, `m17_praezision.py`, `m17_bild.py` | Rechnen auf dem Export; aus unserem Code lesen sie nur die Konstante `tuer_zuordnung._KONTAKT_MM`. `m17_praezision.py` liest zusätzlich die DXF direkt per `ezdxf.readfile` (kein Pipelinelauf) |
| `…/helfer/m17_nachmessung.py` | Rechnet ohne jeden Import aus `notbeleuchtung` |

**Unabhängige Prüfung**

| Datei | Zweck |
|---|---|
| `03_Review/Raumerkennungenis_Review_M17_01_02_2026-09-17.md` | Review der Fassung 1: bestätigt vier Prüfungen und den Fehlbefund, stuft M17-02-c herunter, listet zwölf Korrekturforderungen. Fassung 2 antwortet darauf |

Nicht im Paket: **Fassung 1** der Diagnose (liegt nur in Enis' Sicherung
`_sicherung/2026-09-17_2225_m17-diagnose/`). Alle Aussagen über Fassung 1 sind Zitate in
Review und Fassung 2 und an der Quelle hier nicht prüfbar.

---

## 2. Diagnosebasis gegen unseren Stand

| Gegenstand | Angabe des Pakets | Gemessen am 2026-09-18 |
|---|---|---|
| Branch/Commit | `selman/rennweg-stand` @ `f15d03fe…f37d` | **identisch** — und `f15d03f` ist heute der Branch-Kopf, lokal wie auf `origin`; Worktree `D:\KI Projekt\nb-wt\rennweg-stand` sauber |
| Rechenstand | `59583ff` (Tranche 1: S1, S2, S5a, S3a, S9) | `59583ff7200…3bf5` ist Vorfahre des Kopfs; zwischen `59583ff` und `f15d03f` **keine** Änderung in `src/notbeleuchtung/raumerkennung/` (nur Rennweg_v2-Artefakte und `docs/COORDINATION.md`) |
| Vergleichsbasis | `main` = `2f610ccc…0040` | `origin/main` steht unverändert auf diesem Commit |
| Contract | `raum_modell` 1.5.0 | `CONTRACT_VERSION = "1.5.0"` (`hauptengine/contracts/raum_modell.py`), gleicher Default im generierten Schema, identisch auf `main` und auf dem Branch |
| Eingabe-DXF | SHA-256 `c64e73e3…245e`, 4.072.038 Byte | **identisch** — Paketdatei, Arbeitskopie und das auf `origin/main` getrackte Blob `5bc7c2db…1098` unter `Projekte/Rennweg/OG1 - …dxf`; auch der OG1-Eintrag in der getrackten `Projekte_Leere Architektpläne (Input)/Rennweg.zip` hat denselben Hash |

**Die historische Messbasis bleibt damit gültig und wird von nichts ersetzt.**

Drei Punkte, die man beim Weiterarbeiten kennen muss:

1. **Der Haupt-Checkout ist nicht der Diagnosestand.** `D:\KI Projekt\Notbeleuchtung` steht
   auf `selman/fix-s1-aussen-loch-topologie` @ `13243b3` — einem **älteren** Punkt derselben
   Linie, ohne Tranche 1. Wer dort misst, misst nicht die Diagnosebasis. Für alles zu M17
   gilt der Worktree `D:\KI Projekt\nb-wt\rennweg-stand`.
2. **Die Diagnose-Doku liegt in keinem Checkout.** `docs/DIAGNOSE_RENNWEG_RAUMERKENNUNG.md`
   existiert nur auf `selman/diagnose-rennweg` @ `34b5dd0` (433.823 Byte) und ist nicht
   Vorfahre von `selman/rennweg-stand`. Lesen per
   `git show 34b5dd0:docs/DIAGNOSE_RENNWEG_RAUMERKENNUNG.md`.
3. **Zeilenangaben der Diagnose sind gegen `main` geschrieben.** Sie nennt
   `tuer_zuordnung.py:133-160`; durch den S5a-Guard (+5 Zeilen) liegt
   `durchgaenge_ohne_tuerblatt` heute bei **120–166**, `aussen_durchgaenge` ab 174.

---

## 3. Was mein aktueller Code gegenüber `f15d03f` schon enthält

**Nichts.** Gegenüber der Diagnosebasis enthält der heutige Stand **keine** Änderung in
`src/notbeleuchtung/raumerkennung/`:

```
git diff f15d03fe1a082c78b180e940b7dcd666fccaf37d..HEAD -- src/notbeleuchtung/raumerkennung/   → leer
git diff HEAD..f15d03fe1a082c78b180e940b7dcd666fccaf37d -- src/notbeleuchtung/raumerkennung/   → leer
git status --porcelain (Worktree rennweg-stand)                                                 → leer
```

Relevant ist deshalb nicht der Abstand zur Diagnosebasis, sondern **was Tranche 1 gegenüber
`main` in genau diesem Bereich bereits geändert hat** — denn das entscheidet, ob der Befund
schon teilweise behoben ist:

| Datei | Änderung gegenüber `main` `2f610cc` | Wirkung auf M17-02-b |
|---|---|---|
| `tuer_zuordnung.py` (+14 Zeilen) | **S5a**: `durchgaenge_ohne_tuerblatt` überspringt Paare, bei denen eine Seite `nutzungsklasse_fuer(raum_typ) == KEIN_RAUM` ist (SCHACHT/LIFT). Dazu ein reiner Docstring-Zusatz in `aussen_durchgaenge` (offener Punkt U8/S5c/F8) | **keine** — `raum_6` und `raum_7` sind beide BAD → `WOHNUNG_PRIVAT`, der Guard greift nicht |
| `provider.py` (+10) | **S2**: `erkenne_aussenbereiche(plan, k.wandkoerper, waehle_innen_zonen(plan, raeume, k.zuordnungen))` | keine; die Türkette ist unverändert, `durchgaenge_ohne_tuerblatt` wird weiterhin in Zeile 143 gerufen |
| `aussenbereich.py` (+162), `geometrie_typ.py` (+82), `rest_komponenten.py` (+47) | S1, S2, S9, S3a | keine Berührung mit der Durchgangsregel |

**Von U13 ist nur der Guard (S5a) gebaut.** Das Querungs-/Kontaktkriterium — S5b für
`durchgaenge_ohne_tuerblatt`, S5c für `aussen_durchgaenge` — ist **nicht** implementiert; für
S4a, S4b, S5b und S5c existiert im Repo weder Branch noch Worktree. Wer „Tranche 1 hat U13
behandelt" liest, darf daraus nicht schließen, die Scheinkanten-Ursache sei weg.

---

## 4. Belastbar belegte Ergebnisse

### 4.1 M17-02-b — selbst nachgerechnet, nicht übernommen

**Methode (offengelegt).** Kein Erkennungslauf: kein `provider.parse`, keine Pipeline, kein
`scripts/analyse/*`, keine Ausgabe unter `Projekte/_ergebnis*`. Gerechnet wurde auf den
Ringen aus `m17_export.json` (Räume, protokollierte Wand-Union) mit dem heutigen Code des
Worktrees `rennweg-stand`; dabei lief **eine** Einzelfunktion in-memory:
`tuer_zuordnung.durchgaenge_ohne_tuerblatt(raeume, tueren, wand_union)`. Skript im
Scratchpad, nicht im Repo.

Schritt 1 — Streifen wie im Code gebildet (`_KONTAKT_MM = 250,0`):

```
Abstand raum_6 ↔ raum_7 (Exportringe)     :   99,999928 mm
Kontaktzone (je +250 mm gepuffert)        :    1,296030048 m²
davon nicht von der Wand-Union bedeckt    :    0,933471053 m²  in 4 Streifen
```

| Streifen | Fläche m² | Rechteck L × K mm | Abstand `raum_6` | Abstand `raum_7` | beidseitig frei | ≥ 800 mm |
|--:|--:|--:|--:|--:|---|---|
| 0 | 0,034612312 | 357,84 × 140,75 | 99,999988 | 99,999922 | **nein** | nein |
| 1 | 0,206919284 | 1381,26 × 150,00 | 99,999959 | 0,000000 | **nein** | ja |
| 2 | 0,241360228 | 1610,94 × 150,00 | 99,999934 | 0,000000 | **nein** | ja |
| 3 | 0,450579228 | 3068,22 × 149,74 | 0,000000 | 99,999930 | **nein** | ja |

Schritt 2 — die heutige Funktion direkt aufgerufen: **3 Durchgänge**, `raum_6 → raum_7`,
alle `ohne_tuerblatt=True`, Breiten 1381 / 1611 / 3068 mm. Gegen den Export zugeordnet:

| meine Rechnung | Export | Schwerpunktabstand | Breite (meine / Export) |
|---|---|--:|---|
| `durchgang_1` | `durchgang_11` | 4,4 × 10⁻⁵ mm | 1381 / 1380 mm |
| `durchgang_2` | `durchgang_12` | 4,8 × 10⁻⁵ mm | 1611 / 1612 mm |
| `durchgang_3` | `durchgang_13` | 5,6 × 10⁻⁵ mm | 3068 / 3069 mm |

Die 1-mm-Differenzen der Breiten sind dieselbe numerische Empfindlichkeit des minimal
rotierten Rechtecks, die Fassung 2 mit „bis 3,2 mm" benennt; sie betrifft nur das Maß, nicht
die Aussage.

**Codeseitiger Grund, am heutigen Stand gelesen** (`tuer_zuordnung.py:120-166`): Ein Paar
erzeugt einen Durchgang, wenn beide Räume ein Polygon haben, keiner die Klasse `KEIN_RAUM`
trägt (S5a), ihr Abstand ≤ 500 mm ist, ein freier Teil der gepufferten Kontaktzone
existiert, dessen umschließendes Rechteck ≥ 800 mm misst, und im Umkreis von 600 mm keine
bekannte Tür liegt. **Ein Kontakt- oder Querungsprädikat gibt es nicht** — der freie Teil
wird weder auf Berührung mit beiden Raumpolygonen noch auf Durchstoßen der Wand geprüft; es
fehlen ebenso Mindestfläche gegen Splitter und Überlappungsausschluss. Weil die Kontaktzone
beidseits um 250 mm puffert, die Trennwand aber nur 100 mm dick ist, bleiben zwangsläufig
Streifen **auf je einer Raumseite** übrig.

**Ergebnis: Zuordnung zu S5b (Ursache U13, Teil „Kriterium") bestätigt.** Der Befund ist
kein neuer Fehler, sondern der nachrechenbare Beleg für einen bereits geplanten, nicht
gebauten Slice. Die Diagnose formuliert S5b genau so: „zählt nur ein freier Teil, der die
Wand zwischen beiden Räumen quert … Splitter (Fläche < Breite · 50 mm) und Überlappungen
queren nicht" (`34b5dd0:docs/DIAGNOSE_RENNWEG_RAUMERKENNUNG.md` § 5.2). Ein Widerspruch
ergibt sich nicht.

**Bindend für jeden Fix:** S5b steht im Türstapel **S4a → S4b → S5b → S5c** mit **einem
gemeinsamen Merge-Gate** (§ 5.1 Gate-Spalte; § 5.3 Punkt 3: „weil jeder allein OG1
verschlechtert"). Ein isolierter Fix ist nicht merge-reif. Ein bestandener M17-Fall erfüllt
außerdem **keines** der Merge-Gates von Tranche 1.

### 4.2 Die weiteren belegten Punkte

| Befund | Beleg |
|---|---|
| M17-01-a/-b/-c und M17-02-a **BESTANDEN** | `BEFUND.md` Prüftabelle; unabhängig bestätigt im Review (Tabelle „Nachgerechnete Prüfungen") |
| Die Trennwand ist vollständig erkannt und 100 mm dick | Wandkörper 72 (`27C6`) und 73 (`27CF`), beide `breite_mm = 100.0`, Quellzuordnung über Flächendeckung `anteil_quelle = anteil_körper = 1,0`; zusätzlich die von mir gemessenen 99,999928 mm Raumabstand |
| Beide Bäder stammen aus der L-Stufe (Raum-Layer), die Raster-Flutung war nicht beteiligt, keine Bereinigung | `m17_export.json`: `kaskade.quelle_je_raum.raum_6/raum_7 = "L"`, `polygon_roh_vorhanden = false`, `bereinigung = []` |
| Eingabe- und Ausgabeidentität der Referenzausgabe | `quelle.json`: `branch`, `retrieved_commit` `f15d03fe…`, `calculation_commit` `59583ff`, Bild-Blob `42108a8b…`; Bildtitel und Legendenzählung des PNG passen dazu |
| Keine menschliche Freigabe, keine Trainingseignung | `label_status = assistant_plan_interpretation_pending_owner_review` und `training_eligible = false` in allen sechs Fällen der Referenz-JSON, dazu `execution_policy.no_model_training_without_human_labels = true`; ebenso in MD, PDF und Begleittexten. **Diese Kennzeichnung wird hier unverändert übernommen** — das Paket ist Fachreferenz, kein freigegebener Prüfkorpus und kein Trainingsmaterial |

### 4.3 Bilanz der 18 Erwartungen — mit einer Einschränkung

**4 BESTANDEN · 1 NICHT_BESTANDEN · 13 OFFEN**, die 13 aufgeteilt in 12 nie gemessene
(M17-03 bis M17-06) und 1 bearbeitete, aber nicht abschließend belegte (M17-02-c). Nenner
bleibt 18.

Einschränkung, die man beim Lesen des Pakets kennen muss: **die Fachreferenz-JSON selbst
trägt diese Bilanz nicht.** Dort steht bei allen 18 Erwartungen weiterhin
`software_result = "not_measured"`. Die Bilanz existiert nur in den Fassung-2-Dokumenten.
Das ist kein Widerspruch in der Sache (die JSON ist die ältere Vorlage, sie wurde bewusst
nicht angefasst), aber wer nur die JSON liest, sieht 0 gemessen.

---

## 5. Was offen bleibt

1. **M17-02-c — Kontaktprädikate am T-Knoten.** Die exakten Prädikate kippen mit dem
   Datenstand: ungerundete Quellgeometrie `distance = 3,142787 × 10⁻⁸ mm`,
   `intersects = False`; gerundete Exportringe (4 Dezimalstellen) `0,0 mm` und Überlappung
   `0,0033892 mm²`; sogar die Zuordnung des Randpunkts J wechselt zwischen `27C6` und
   `27CF`. Eine **bauliche Lücke folgt daraus nicht** — gegenüber 100 mm Wand ist der
   Unterschied bedeutungslos —, ein exakt gemessener Kontakt der Laufgeometrie aber auch
   nicht. Der zweite Teil des Solls („kein Flutungsleck") wurde **nie geprüft**. Zum
   Schließen fehlt entweder die ungerundete Laufgeometrie oder eine ausdrücklich begründete
   numerische Toleranz, plus ein definierter Flutungstest. Nebenbefund: `m17_export.json`
   enthält den unaufgelösten Widerspruch `abstand_der_koerper_mm = 0.0` bei
   `beruehren = false`; die Erklärung steht nur in `BEFUND.md`.
2. **Laufzeit 0,9 s gegen 11,6 s.** `m17_export.json:laufzeit_s = 0.9` misst
   `ArchitekturRaumProvider()` + `provider.parse` ohne Rendern. Die 11,6 s stehen in
   `quelle.json` unter `metrics.laufzeit_s.erkennung` (daneben `zeichnen` 3,7, `gesamt`
   15,3) und stammen aus unserem Darstellungslauf. Ob dieselbe Messgröße gemeint ist, ist
   ohne neuen Lauf nicht entscheidbar. Der Wert 13,6 s aus Fassung 1 hat keine Quelle und
   wurde gestrichen — er taucht in keiner Paketdatei auf.
3. **Die 12 ungeprüften Erwartungen** M17-03 (Unterzug), M17-04 (WC-Tür), M17-05 (Schrank),
   M17-06 (schräge Wand), je drei. Vor einer Messung müssen die Helfer angepasst werden: sie
   filtern hart auf M17-01/M17-02 bzw. `raum_6`/`raum_7` und liefen sonst durch, ohne das
   Richtige zu messen.
4. **Union-Abweichung 37,234 mm².** Zwischen protokollierter Wand-Union und der
   Rekonstruktion aus den Exportringen: symmetrische Differenz 37,234 mm², Hausdorff-Abstand
   0,03357 mm, `equals = False` (Flächen 45,922614 gegen 45,922638 m²). Ursache nicht
   untersucht; die rekonstruierte Operationsfolge entspricht nicht wörtlich dem
   Produktionscode. Ob vor dem Export ein `buffer(0)` griff, ist im Artefakt nicht vermerkt.
5. **Rechteckmaße bis 3,2 mm.** Zwischen zwei Berechnungen derselben Geometrie weichen die
   Maße des minimal rotierten Rechtecks ab (Streifen 0: 143,9 → 140,7 mm); meine eigene
   Rechnung zeigt dieselbe Empfindlichkeit im Millimeterbereich. Bei Weltkoordinaten der
   Größenordnung 1,25 × 10⁷ / 3,56 × 10⁸ ist das erwartbar. Flächen und Raumabstände sind
   stabil; die Aussage über den fehlenden beidseitigen Raumkontakt hängt nicht daran. Der
   Fassung-1-Vergleichswert liegt nicht im Paket und ist hier nicht nachprüfbar.
6. **Artefakt-Lücken.** `m17_export.json` führt weder Commit noch DXF-Hash noch
   Contract-Version maschinenlesbar mit; der in `m17_export.py` ergänzte
   Metadatenblock wirkt erst bei künftigen Läufen und erfasst die Contract-Version auch dann
   nicht. Maschinenlesbar belegt sind Commit und DXF-Hash nur über `quelle.json`.
7. **Merge-Gates von Tranche 1 unverändert offen:** S1/S2/S9-Messung auf Barawitzka,
   Mollgasse, Muthgasse; S3a-Nachmessung nach dem Türstapel.
8. **Das gemeinsame Merge-Gate des Türstapels ist benannt, aber nicht ausformuliert.** § 5.1
   nennt nur „Türstapel S4a → S4b → S5b → S5c, ein Merge-Gate"; Messplan, Akzeptanzkriterien
   und Testpläne fehlen — anders als bei S1/S2. Zudem ist „jeder Slice verschlechtert allein
   OG1" in § 5.2 nicht durchgemessen (S4a/S4b/S5b/S5c je „nicht simuliert").
9. **Fachfragen F1–F20** sind nicht Gegenstand dieser Runde und wurden nicht implizit
   beantwortet. Für S5b ist F10 laut § 5.1 nicht blockierend.
10. **Nebenbefund aus dem Lauf:** `RuntimeWarning: invalid value encountered in
    oriented_envelope` (shapely) aus der Kurzseiten-Bestimmung bei entarteter Geometrie —
    ohne Auswirkung auf die sechs Prüfungen, nicht untersucht. Ergänzend aufgefallen: die
    Kurzseite von Körper 73 (`27CF`) ergibt über das minimal rotierte Rechteck nachgerechnet
    1800,2 × 97,5 mm statt der in `BEFUND.md` pauschal genannten 100,0 mm; das Feld
    `breite_mm` ist 100,0. Für die Prüfungen ohne Folge, beim Zitieren aber zu trennen.

---

## 6. Ursprüngliche Angaben und spätere Korrekturen

| Ursprünglich | Korrigiert |
|---|---|
| Auftrag: „18/18 offen, ein Erkennungsfehler ist bisher nicht bewiesen" | Fassung 2: 4 BESTANDEN, 1 NICHT_BESTANDEN, 13 OFFEN; der Fehlbefund M17-02-b ist gemessen und unabhängig bestätigt |
| Auftrag: `main 2f610cc` als Ausgangsstand | Codebasis ist `selman/rennweg-stand` @ `f15d03f`; `main` bleibt nur Vergleichsbasis |
| Auftrag: Handle-/INSERT-Zuordnung der Wandkörper „muss ergänzt werden" | Nicht ergänzt, sondern rein geometrisch über Flächendeckung gelöst; Contract unverändert |
| Fassung 1: M17-02-c BESTANDEN | Fassung 2: **OFFEN** |
| Fassung 1: Laufzeit 13,6 s | Ersatzlos gestrichen (keine Quelle); belegt ist nur 0,9 s |
| Fassung 1: „`distance = 0.0` exakt", „200,0 mm Schnittlänge", „J ∈ Körper 73" | 200,00005 mm ist der **Umfang** eines Überlappungspolygons, keine Kontaktstrecke; Prädikate und J-Zuordnung datenstandsabhängig |
| Fassung 1: „exakt identische Schwerpunkte" | 4,4–5,6 × 10⁻⁵ mm — innerhalb der Exportpräzision, nicht identisch |
| Fassung 1: Union-Gegenprobe nur über die Fläche | Geometrisch: symmetrische Differenz 37,234 mm², keine Identität |
| Fassung 1: Winkelvergleich Öffnungsachse ↔ Wandkante als Fix-Variante | **Zurückgezogen** — als eigenständiges Kriterium nicht verlässlich; verlangt ist eine zusammenhängende freie Verbindung zwischen beiden Raumseiten |
| Fassung 1: `m17_kontaktzone.json` ohne dokumentierten Erzeuger | Erzeuger `m17_kontaktzone.py` nachgeliefert |

---

## 7. Nächster Entwicklungsschritt — abgeleitet, nicht ausgeführt

**Vorschlag: das gemeinsame Merge-Gate des Türstapels ausformulieren und die M17-Fälle als
dessen Messfälle verankern — bevor eine Zeile an `durchgaenge_ohne_tuerblatt` geändert wird.**

Begründung:

- Der Befund ist geklärt, der Fix ist es nicht. S5b ist inhaltlich beschrieben („nur ein
  Teil, der quert"), aber **die Abnahmebedingung fehlt**: Für S1 und S2 gibt es Messpläne
  und Akzeptanzkriterien, für den Türstapel steht nur „ein Merge-Gate". Ohne ausformuliertes
  Gate lässt sich weder entscheiden, wann der Stapel fertig ist, noch, ob ein einzelner
  Slice den Plan verschlechtert.
- Die Behauptung „jeder Slice verschlechtert allein OG1" ist Erwartung, nicht Messung
  (§ 5.2: viermal „nicht simuliert"). Genau diese Lücke macht einen isolierten S5b-Fix
  riskant — und genau sie lässt sich mit In-Memory-Vergleichen auf OG1, DG2 und EG schließen,
  wie die Diagnose es für S5b ohnehin vorsieht.
- Das Paket liefert dafür den ersten belastbaren Fall: M17-02-b ist ein **negativer**
  Gegenfall (geschlossene 100-mm-Wand darf keinen Durchgang ergeben), und die vier
  bestandenen Prüfungen sind **positive** Gegenfälle (freies Wandende, T-Anschluss). Beides
  ist reproduzierbar und bindet das Kriterium an echte Geometrie statt an eine Schwelle.
- Ein isolierter Fix ist aus dieser Diagnose heraus ausdrücklich nicht merge-reif; die
  Reihenfolge `S4a → S4b → S5b → S5c` ist gesetzt, weil das Querungskriterium auf den
  Türbefund aufsetzt (`tuer_n`, Türnähe-Filter 600 mm). S5b vor S4a/S4b zu bauen, hieße das
  Kriterium gegen einen Türbestand zu prüfen, der sich danach ändert.

Konkrete, jeweils eigenständig zu beauftragende Schritte in dieser Reihenfolge:

1. **Gate schreiben** (Doku, kein Code): Messgrößen je Plan (Anzahl `ohne_tuerblatt`-Türen,
   davon an Wänden < 250 mm), Akzeptanzkriterien für OG1/DG2/EG, Pflichttests, und die
   Festlegung, dass gemeinsam gemergt wird.
2. **Regressionsfälle aus M17** in `tests/` — negativer Fall M17-02-b, positive Fälle
   M17-01-a/-b/-c und M17-02-a, gespeist aus der Referenzgeometrie. Eigener Auftrag, eigenes
   Package, ohne Aufnahme der Referenz in einen Trainingskorpus.
3. **S4a**, dann **S4b**, dann **S5b**, dann **S5c** — je eigener Branch, Test zuerst rot,
   ein Concern pro Commit, Merge erst nach dem gemeinsamen Gate.
4. Unabhängig davon offen und nicht durch M17 erledigt: die Merge-Gates von Tranche 1 und
   die Entscheidung, ob `docs/DIAGNOSE_RENNWEG_RAUMERKENNUNG.md` (`34b5dd0`) in die
   Arbeitslinie gemergt wird — derzeit zitieren Code-Kommentare eine Datei, die in keinem
   Checkout liegt.

M17-02-c, der Laufzeitvergleich und die zwölf ungeprüften Erwartungen brauchen jeweils einen
eigenen Auftrag; keiner davon blockiert Schritt 1.

---

## 8. Grenzen dieser Übernahme

- Gelesen, geprüft, eingeordnet — **nicht** ausgeführt: kein `provider.parse`, keine
  Pipeline, kein `pytest`, kein Skript aus `scripts/analyse/`, keine Ausgabe unter
  `Projekte/_ergebnis*`, keine Änderung an Erkennungscode, Contract, Tests oder Korpus.
  Einzige Ausnahme und oben offengelegt: der In-Memory-Aufruf von
  `durchgaenge_ohne_tuerblatt` auf exportierter Geometrie (Abschnitt 4.1).
- Keine Paketdatei wurde ins Repository kopiert; dieses Dokument enthält nur Pfade und
  Verweise.
- Die Lauf-Identität des Diagnoselaufs (detached Worktree auf Enis' Rechner) ist Begleittext,
  nicht maschinenlesbar im Artefakt — das gilt auch nach dieser Prüfung.
- Die Referenzlabels bleiben `assistant_plan_interpretation_pending_owner_review` und
  `training_eligible = false`. Es wird **keine** menschliche Freigabe behauptet und nichts
  davon geht in Trainingsdaten.
- Ein bestandener M17-Fall erfüllt kein Merge-Gate; sechs geprüfte Stellen eines Geschosses
  sind keine Qualitätsaussage über die Raumerkennung.
