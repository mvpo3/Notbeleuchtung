# Merge-Gate des Türstapels S4a → S4b → S5b → S7a+S7b → S3b → S5c

Stand: 2026-09-20 (Nachträge: Lesart B zu M17-04-c 2026-09-18; Stapel-Erweiterung, Bedingungen
(7)/(8) und Diagnose S7a/S3b 2026-09-19; Reihenfolge, S7a+S7b, Bedingung (9) und Folgeauftrag
S-KG 2026-09-20) · Owner: Selman (`src/notbeleuchtung/raumerkennung/`) ·
Branch `selman/uebernahme-enis-m17` · Nullmessung auf Code-Stand `f15d03f` (Tranche 1)

**Reihenfolge seit 2026-09-20 (Owner-Ansage, verbindlich, nichts parallel):** S5b →
S7a+S7b (= Leonis' Paket S-W „Wohnung ≠ Fluchtweg", § 6f) → S3b → S5c → Gate → Merge des
Stapels → danach S-KG (Kellergeschosse und Garage) als eigenes Paket (§ 5a). Regeln
unverändert: nur `raumerkennung/`, kein Owner-Package importieren, Contract nur über das
Board, ein Slice ein Commit, kein Merge vor dem Gate.

**Stapel seit 2026-09-18 (Owner-Entscheid nach S4b): S4a → S4b → S5b → S7a → S3b → S5c.**
S7a (Vorraum-Regel, U14/F11) und S3b (Restflächen vor Blocktüren, Owner-Definition) gehören
zum Stapel, weil die Bedingungen (5) und (6) sonst nicht erreichbar sind: **(5) und (6) sind
keine Türprobleme, aber Regressionen gegenüber `main`, die der Stapel selbst ausgelöst hat**
(S4b macht T01 korrekt und kippt damit Vorraum 10,94 über `_verfeinere_gang_privat` in die
Erschließung → Einraum 2 → 2; S4a macht auf OG3 die Blocktüren zu Türen ohne Raumseite →
GRAPH 0). Das Gate bleibt unverändert, (5) und (6) bleiben Merge-Pflicht; § 6 und § 7
enthalten die Diagnose der beiden neuen Scheiben (kein Code).

Die Diagnose (`docs/DIAGNOSE_RENNWEG_RAUMERKENNUNG.md` @ `34b5dd0`, § 5.1/§ 5.3) bindet die
vier Tür-Slices an **ein gemeinsames Merge-Gate**, nennt dafür aber weder Messplan noch
Akzeptanzkriterium; „jeder Slice verschlechtert allein OG1" ist dort viermal „nicht
simuliert". Dieses Dokument macht das Gate **messbar**, bevor ein Slice gebaut wird. Es
ändert nichts an der Erkennung.

Code: `tests/gate/` · Nullmessung: `tests/gate/nullmessung_f15d03f.json` · Regel:
`tests/gate/gate_regel.py::pruefe_gate` · Test: `pytest -m gate tests/gate`.

---

## 1. Messfälle

### 1a. Die 18 Erwartungen aus Beispiel 17 (M17-01 bis M17-06)

Quelle: Enis' Fachreferenz `Raumerkennung_Enis_17_Rennweg_Mauern_Prueffaelle.json` (Paket
außerhalb des Repos, siehe `docs/UEBERNAHME_ENIS_M17.md`; SHA-256
`9b38b258c172507922fec2350efbf03d4386771ee0e58cacf2f38e9bab743d4a`). Die Helfer des Pakets
filtern fest auf M17-01/02 und `raum_6`/`raum_7`; sie werden **nicht** benutzt. Eigene
Messfunktion: `tests/gate/gate_m17.py::messe(ref, raeume, tueren, wandkoerper)` — reine
Funktion auf Contract-Objekten plus den Einzel-Wandkörpern des Laufs (`gate_lauf.erkenne`
greift Plan und `KaskadeErgebnis` mit demselben Wrapper ab wie
`scripts/analyse/raumerkennung_darstellung.py::_erkennen`; das RaumModell führt keine
Wandkörper).

Genau ein Ergebnis je Erwartung, in der Reihenfolge der Referenz: `BESTANDEN`,
`NICHT_BESTANDEN` oder `NICHT_MESSBAR` mit Grund. **Der Nenner bleibt 18.**

Messsemantik je Prüfart (Entscheid des Owners, im Modul-Docstring festgehalten):

| Prüfart | Gemessen wird | BESTANDEN wenn |
|---|---|---|
| `physical_wall_covers_probe` | Einzel-Wandkörper, die die Sonde decken; Raumpolygone, die sie decken | expected true: Wandkörper ja **und** kein Raumpolygon (bewusst strenger als die Referenz, die „außerhalb der Raumfläche" nur bei 01-a/06-a ausdrücklich fordert); expected false: kein Wandkörper |
| `same_room` | Räume an beiden Sonden; bei Fällen mit Route (M17-01): Schnitt Route ∩ Wandkörper | beide Sonden in genau demselben Raum; Route schneidet keinen Wandkörper (> 1 mm) |
| `room_covers_probe` | Zielraum = der eine Raum an der Sonde des positiven checks (M17-06: I) | expected true: genau ein Raum; expected false: Zielraum deckt die Sonde nicht |
| `direct_portal_in_probe_segment` | Räume an A/B; Portale = Türen im Ausschnitt (clip) mit Abstand ≤ `PORTAL_WAND_MM` = 250 mm zum Quellpolygon der markierten Wand — **unabhängig von `von_raum`/`nach_raum`** | A und B in verschiedenen Räumen und kein Portal |
| `wall_contact_preserved` | siehe § 4 | Kontakt (≤ 1 mm) **und** kein Flutungsleck |
| `physical_wall_intersects_route` | Schnittlänge Route ∩ Wandkörper > 1 mm | Messwert = expected |
| `distinct_rooms_connected_by_door` | Räume an A/B; Verbindungen = Türen zwischen beiden Räumen im clip, deren Abstand zur Sonde O ≤ halbe Türbreite ist; **Türverbindung = Verbindung mit Türblatt** | A/B verschieden und genau **eine** Türverbindung. Durchgänge ohne Türblatt zählen nicht (Lesart B, Entscheid Enis 2026-09-18, § 2a); sie bleiben als Dubletten-Kandidaten in den Messwerten |

Unauflösbares wird nie PASS: Sonde in mehreren Raumpolygonen → `NICHT_MESSBAR`; Sonde in
keinem Raum, wo einer erwartet ist → `NICHT_BESTANDEN`. „Physische Wand" ist immer der
Einzel-Wandkörper; die technische `wand_union` (25-mm-Fugenschluss) läuft nur als Messwert
mit. „An dieser Stelle" ist immer das `clip`-Polygon des Falls aus der Referenz.

### 1b. M1 bis M4 der Diagnose auf den 7 Rennweg-Plänen

Die vier Messskripte aus Anhang A.1–A.4 der Diagnose liegen **wortgetreu** unter
`tests/gate/diagnose_skripte/` (programmatisch aus `34b5dd0` extrahiert, per difflib
belegt). Einzige Abweichungen, je Datei im Kopf benannt: Kopfkommentar, `# ruff: noqa`,
`REPO` aus `NOTBEL_REPO` (Pflicht), Cache-Wurzel aus `NOTBEL_GATE_CACHES`, bei A.2–A.4
zusätzlich `import os`. Der Docstring von A.1 nennt wortgetreu noch den alten
Default-Pfad.

Verfahren (`tests/gate/gate_m1_m4.py`): genau das Nachher-Verfahren der Diagnose — die 7
Grundrisse (`Projekte/Rennweg/`, UG/EG/OG1/OG2/OG3/DG1/DG2; nicht DD, nicht Legende)
werden nach `_arbeit/gate/eingang/Rennweg/` kopiert, `raumerkennung_darstellung.py`
erzeugt daraus Stufe-1-Caches unter `_arbeit/gate/<Kurz-SHA>/Rennweg_v0/` (bei
ungesicherten Änderungen in `src/` oder `scripts/`: `<sha>-dirty-<Inhalts-Hash>`), dann
laufen die vier Skripte unverändert und werden auf die **Kopfzahlen** der Tabellen in
Diagnose § 4 reduziert:

| Kennzahl | Bedeutung | im Gate verglichen |
|---|---|---|
| M1.hauptwert | STIEGENHAUS mit achsparalleler Hülle im gedrehten Plan | ja |
| M1.klein_ohne_stempel | STIEGENHAUS < 2 m² ohne Stempel | ja |
| M2.wert | Innenräume (ohne Freiflächen) mit Schnitt > 0,05 m² zum offenen Außenbereich | ja |
| M2.inkl_freiflaechen | dito inkl. Balkon/Terrasse/Loggia | ja |
| M2.offen_m2 | offene Außenfläche | nur berichtet (richtungsoffen) |
| M3.hauptwert | Räume (nicht SCHACHT/LIFT) mit roter Schachtfläche ≥ 0,02 m² | ja |
| M3.rote_flaeche_m2 | rote Schachtfläche in Räumen | ja (Toleranz 0,001 m²) |
| M4.wohnungen | Wohnungen | nur berichtet (richtungsoffen) |
| M4.einraum, M4.datenbefund, M4.darstellungsbefund, M4.privatraum_ohne_wohnung | wie Diagnose § 4 | ja |

**Treue-Beleg:** Auf den Vorher-Caches der Diagnose (Stand `511ad36`) reproduziert die
Reduktion die Tabellen aus § 4 exakt — M1 1 / 6, M2 20 / 24, M3 34 / 11,456 m², M4
15 / 8 / 0 / 1 / 11, je Plan und in allen Summen (zweimal unabhängig nachgerechnet).

### 1c. OG1-Kennzahlen (`tests/gate/gate_og1.py`)

Räume gesamt, UNBEKANNT, Türen gesamt, Türen mit `von_raum == nach_raum` (beide Seiten
gesetzt), Durchgänge ohne Türblatt, Wohnungen, Einraum-Wohnungen — aus dem RaumModell
des OG1-Laufs.

### 1d. OG3-Kennzahlen (`tests/gate/gate_og3.py`, seit S4a)

Rennweg OG3 (`Projekte/Rennweg/OG3 - …dxf`, floor `OG3` wie in `tests/naht/test_soll_rennweg.py`):
Segmente mit `quelle == GRAPH`, Segmente gesamt, Anker gesamt, Anker in Räumen mit
`nutzungsklasse WOHNUNG_PRIVAT` (Definition wie `test_keine_anker_in_wohnung_privat`),
Wohnungen, Einraum-Wohnungen, Türen gesamt, Durchgänge ohne Türblatt, GANG-Räume in
`WOHNUNG_PRIVAT`. Grund: S4a allein verschmilzt auf OG3 zwei Wohnungen, zieht den Gang in
die Wohnung und lässt die Zirkulation von GRAPH auf FALLBACK kippen — genau das muss der
fertige Stapel wieder heilen.

### 1e. Referenz-Verbindungen OG1 (`tests/gate/gate_referenz.py`, seit 2026-09-19)

Owner-Entscheid nach S4b: die von den Fachreferenzen **verneinten** Verbindungen dürfen nach
dem Stapel nicht mehr existieren — als Messfall mit Referenznummer je Verbindung. Räume werden
über `raum_typ` + Fläche (± 0,05 m²) identifiziert, nicht über IDs; passt kein oder mehr als
ein Raum, ist der Fall nicht messbar (`anzahl` None mit Grund). Gezählt werden Türen jeder
Quelle, die beide Räume verbinden.

| Art | Referenz | Verbindung |
|---|---|---|
| verneint | M17-02 / Bsp. 07, 08, 14 | BAD 11,76 ↔ BAD 4,66 |
| verneint | Bsp. 06, 14 | ZIMMER 17,04 ↔ GANG 6,48 |
| verneint | Bsp. 08, 09, 14 | VORRAUM 3,40 (Garderobe) ↔ BAD 4,66 |
| verneint | Bsp. 08, 14 | ZIMMER 10,59 ↔ BAD 4,66 |
| verneint | Bsp. 09, 14 | ZIMMER 16,86 ↔ VORRAUM 3,40 |
| verneint | Bsp. 07, 14 | BAD 11,76 ↔ ZIMMER 17,04 |
| verneint (Zusatz, heute 0) | Bsp. 14 | ZIMMER 16,86 ↔ BALKON 7,51 · ZIMMER 16,11 ↔ BALKON 7,51 · WC 3,50 ↔ STIEGENHAUS 11,21 · GANG 6,48 ↔ STIEGENHAUS 11,21 · GANG 6,48 ↔ BAD 4,66 |
| gefordert | O03 (Bsp. 06, 09, 14) | GANG 6,48 ↔ Wohnküche 73,06 (ohne Raumtyp) |
| gefordert | O04 (Bsp. 06, 09, 14) | GANG 6,48 ↔ ZIMMER 10,59 |
| gefordert | O05 (Bsp. 06, 09, 14) | VORRAUM 2,59 ↔ VORRAUM 3,40 |
| gefordert | O01/O02 (Bsp. 06, 09, 14) | VORRAUM 10,94 ↔ Wohnküche 73,06 — Ersatzfall, solange Bereich E kein eigener Raum ist |

Die „gefordert"-Zeilen sind eine **Ergänzung des Planers** (Bedingung (8)): S5b soll die
verneinten Verbindungen schließen, ohne die geforderten offenen Übergänge mitzunehmen. Die
fünf Zusatz-Paare stehen als Schutz gegen einen Rückschritt.

### Eingabe und Rechenstand

Alle Messungen gegen die getrackten DXF unter `Projekte/Rennweg/` (die Familien-Soll-Tests
lesen seit 2026-09-18 ebenfalls die versionierten Pläne, `tests/plaene.py` — vorher lasen sie
den untracked Ordner `Projekte/_eingang` und skippten in jedem frischen Checkout); die Messung schreibt
je Plan den SHA-256 in `meta.dxf` (OG1 =
`c64e73e30a482d3fe7c38004b726151eb5325e4beb453def4d92dba5afaa245e`, identisch mit der
Referenz-DXF des Pakets). `meta` trägt außerdem `commit_head`, den Tree-Hash von
`src/notbeleuchtung/raumerkennung`, `basis_tree_gleich` (Vergleich mit `f15d03f`),
`contract_version`, `referenz_sha256` und die Toleranzen.

---

## 2. Nullmessung auf f15d03f (das Vorher für den ganzen Stapel)

`tests/gate/nullmessung_f15d03f.json` · gemessen 2026-09-18 · `commit_head` `1827488`
(Doku-Commit über `f15d03f`; `src/`+`scripts/` tree-gleich mit `f15d03f`, Feld
`basis_tree_gleich = true`) · Contract `raum_modell` 1.5.0 · Arbeitsbaum sauber ·
zweiter Lauf bis auf Datum/Laufzeit identisch (deterministisch) · Laufzeit 46 s
(Caches vorhanden).

### 2a. Die 18 Erwartungen

| Erwartung | Status | Befund |
|---|---|---|
| M17-01-a | BESTANDEN | W in Wandkörper 73, in keinem Raumpolygon |
| M17-01-b | BESTANDEN | A und B in `raum_7`; Route schneidet keinen Wandkörper |
| M17-01-c | BESTANDEN | C in keinem Wandkörper (in `raum_7`) |
| M17-02-a | BESTANDEN | W in Wandkörper 72, in keinem Raumpolygon |
| **M17-02-b** | **NICHT_BESTANDEN** | drei Öffnungen an der markierten Wand: `durchgang_11` 1380 mm, `durchgang_12` 1612 mm, `durchgang_13` 3069 mm, alle ohne Türblatt, 74–75 mm von der Wandquelle, `raum_6 ↔ raum_7` |
| M17-02-c | BESTANDEN | siehe § 4: Abstand 3,14 × 10⁻⁸ mm, kein Leck |
| M17-03-a | BESTANDEN | P (Unterzug-Projektion) in keinem Wandkörper |
| M17-03-b | BESTANDEN | W in Wandkörper 132 |
| M17-03-c | BESTANDEN | Route unter dem Unterzug (847 mm) schneidet keinen Wandkörper |
| M17-04-a | BESTANDEN | W in Wandkörper 82 |
| M17-04-b | BESTANDEN | O (Türöffnung) in keinem Wandkörper |
| **M17-04-c** | **NICHT_BESTANDEN** | keine Türverbindung WC ↔ Vorraum: die einzige Verbindung `durchgang_21` ist ein synthetischer Durchgang **ohne Türblatt** (2506 mm, `tuer_detail` wohnungseingang, 534 mm von O) und zählt nach **Lesart B** nicht. Entscheid Enis (2026-09-18, über Selman): gemeint ist die tatsächliche Türöffnung an O zwischen WC und privatem Vorraum, basierend auf dem ArchiCAD-Türblock `Zargentür_1_Fl 10[9]`; dieser Block wird heute nicht als Tür erkannt (U12 → S4a) |
| M17-05-a | BESTANDEN | W in Wandkörper 78 |
| M17-05-b | BESTANDEN | F (Möbel) in keinem Wandkörper |
| M17-05-c | BESTANDEN | F und R in `raum_1` |
| M17-06-a | BESTANDEN | W in Wandkörper 94 |
| M17-06-b | BESTANDEN | I genau in `raum_1` (ZIMMER, 16,11 m²) |
| M17-06-c | BESTANDEN | X liegt nicht im Zielraum `raum_1` (in keinem Raum) |

**Bilanz: 16 BESTANDEN · 2 NICHT_BESTANDEN · 0 NICHT_MESSBAR.** Die Erwartung aus Enis'
Fassung 2 (01-a/b/c und 02-a bestanden, 02-b mit drei Portalen nicht) ist getroffen; die
12 Erwartungen M17-03 bis M17-06 sind hier zum ersten Mal gemessen — 11 bestanden, M17-04-c
nicht (zuerst als NICHT_MESSBAR geführt, mit Enis' Entscheid vom 2026-09-18 zu Lesart B
auf NICHT_BESTANDEN gestellt; die Referenz selbst ist unverändert).

Gegenüber Enis' Fassung 2 ändert sich damit: M17-02-c von OFFEN auf BESTANDEN (durch die
Toleranzentscheidung § 4), M17-04-c von OFFEN auf NICHT_BESTANDEN (Lesart B), die
Gesamtbilanz des Pakets von 4 / 1 / 13 auf 16 / 2 / 0. Die Referenzlabels bleiben
`assistant_plan_interpretation_pending_owner_review`, `training_eligible = false`.

### 2b. M1 bis M4 (Kopfzahlen je Plan)

| Plan | M1 haupt / klein | M2 wert / inkl. Freifl. / offen m² | M3 haupt / rot m² | M4 Whg / Einraum / Daten / Darst. / privat o. Whg |
|---|---|---|---|---|
| UG | 0 / 1 | 0 / 0 / 23,19 | 4 / 1,204 | 4 / 4 / 0 / 0 / 1 |
| EG | 0 / 1 | 0 / 0 / 0 | 3 / 1,807 | 2 / 1 / 0 / 0 / 1 |
| OG1 | 0 / 1 | 0 / 1 / 25,19 | 6 / 1,544 | 3 / 2 / 0 / 0 / 2 |
| OG2 | 0 / 0 | 0 / 2 / 30,08 | 5 / 1,574 | 2 / 1 / 0 / 0 / 3 |
| OG3 | 0 / 0 | 0 / 0 / 1,99 | 3 / 1,442 | 2 / 0 / 0 / 0 / 0 |
| DG1 | 0 / 1 | 0 / 0 / 2,77 | 7 / 1,415 | 1 / 0 / 0 / 0 / 2 |
| DG2 | 0 / 1 | 2 / 3 / 40,57 | 4 / 1,260 | 1 / 0 / 0 / 0 / 2 |
| **Summe** | **0 / 5** | **2 / 6 / 123,79** | **32 / 10,246** | **15 / 8 / 0 / 0 / 11** |

Zum Vergleich der Vorher-Stand der Diagnose (`511ad36`, vor Tranche 1): M1 1 / 6, M2
20 / 24 / 442,01, M3 34 / 11,456, M4 15 / 8 / 0 / 1 / 11. Die Diagnose erwartete nach
S1+S2 für M2 genau `wert = 2` (DG2 `raum_2`, `raum_4`) — getroffen.

### 2c. OG1

Räume 18 · UNBEKANNT 1 · Türen 28 · Türen mit `von_raum == nach_raum` **0** · Durchgänge
ohne Türblatt 26 · Wohnungen 3 · Einraum-Wohnungen **2** (`top_2` = Abstellraum 4,52 m²,
`top_3` = WC 3,50 m²).

### 2d. OG3 (Nullmessung nachgemessen am 2026-09-18, Code weiterhin tree-gleich f15d03f)

Segmente GRAPH **5** (von 5) · Anker 16, davon **0** in WOHNUNG_PRIVAT · Wohnungen 2 ·
Einraum 0 · Türen 23 · Durchgänge ohne Türblatt 20 · GANG in WOHNUNG_PRIVAT 0.
Bedingung (6) ist auf f15d03f erfüllt; nach S4a allein steht sie auf GRAPH 0 / Anker 8
(siehe Board 2026-09-18).

### 2e. Referenz-Verbindungen (Nullmessung nachgemessen am 2026-09-19, Code tree-gleich f15d03f)

Sechs der elf verneinten Verbindungen bestehen, zusammen **8** Türen, alle Durchgänge ohne
Türblatt: BAD 11,76 ↔ BAD 4,66 **3** (`durchgang_11/12/13`, M17-02-b) · ZIMMER 17,04 ↔ GANG
6,48 1 · VORRAUM 3,40 ↔ BAD 4,66 1 · ZIMMER 10,59 ↔ BAD 4,66 1 · ZIMMER 16,86 ↔ VORRAUM 3,40 1 ·
BAD 11,76 ↔ ZIMMER 17,04 1. Die fünf Zusatz-Paare stehen auf 0. Alle vier geforderten
Übergänge bestehen (je 1 Durchgang ohne Türblatt). Die Nullmessung wurde dafür neu
geschrieben (`commit_head` `a788e47`, `basis_tree_gleich = true`); gegenüber der Datei vom
2026-09-18 unterscheidet sie sich nur um `meta.datum`, `meta.laufzeit_s`, `meta.commit_head`
und den neuen Abschnitt `referenz` — keine M17-, M1–M4-, OG1- oder OG3-Zahl hat sich bewegt.

---

## 3. Gate-Regel

Der Stapel **S4a → S4b → S5b → S7a+S7b → S3b → S5c wird nur gemeinsam gemergt**, und nur wenn
`pruefe_gate(nullmessung, messung)` **keinen** Verstoß liefert:

| Nr. | Bedingung | Umsetzung |
|---|---|---|
| (0) | Vergleichbarkeit | gleiche DXF (alle 7 SHA-256), gleiche Referenz-JSON, gleiche Toleranzen; Arbeitsbaum `src/`+`scripts/` sauber |
| (1) | keine der 18 Erwartungen fällt von BESTANDEN auf NICHT_BESTANDEN | Nenner 18, IDs und Reihenfolge wie die Referenz; ein Abrutschen von BESTANDEN auf NICHT_MESSBAR zählt ebenfalls als Verstoß (sichere Seite). NICHT_MESSBAR → NICHT_BESTANDEN ist kein Verstoß (heute M17-04-c, sobald Enis' Antwort vorliegt) |
| (2) | **beide roten Fälle drehen**: M17-02-b **und** M17-04-c auf BESTANDEN | die drei Durchgänge an der Bad-Wand verschwinden, die WC-Tür an O wird als Tür mit Türblatt erkannt, **und** M17-02-a bleibt BESTANDEN (die Wand bleibt erkannt) |
| (3) | M1 bis M4 steigen nirgends | je Plan und je Gate-Kennzahl (§ 1b) nachher ≤ vorher; Ganzzahlen exakt, `M3.rote_flaeche_m2` mit 0,001 m² Toleranz; fehlende oder ungültige Werte (NaN, bool, negativ) sind Verstöße |
| (4) | Türen mit `von_raum == nach_raum` null | OG1 |
| (5) | Einraum-Wohnungen auf OG1 sinken | nachher < 2 |
| (6) | Rennweg OG3: Fluchtweg-Ableitung intakt | `segmente_graph ≥ 1` **und** `anker_in_wohnung_privat == 0` (Owner-Entscheid 2026-09-18 nach S4a) — wörtlich die Aussage der beiden Tests `test_soll_segmente_aus_graph` und `test_keine_anker_in_wohnung_privat` in `tests/naht/test_soll_rennweg.py`, die auf dem Stapel-Branch als strict-xfail geführt werden („S4a allein, Türstapel unvollständig, muss vor Merge XPASS sein"); das Gate prüft die Zahlen selbst (`tests/gate/gate_og3.py`), damit es nicht am Marker hängt |
| (7) | OG1: keine von der Referenz **verneinte** Verbindung besteht | `anzahl == 0` für jeden Eintrag aus `gate_referenz.VERNEINT` (§ 1e), Zusatz-Paare eingeschlossen; nicht auflösbarer Raum (`anzahl` None) oder fehlender Abschnitt = Verstoß (Owner-Entscheid 2026-09-18 nach S4b) |
| (8) | OG1: jeder von der Referenz **geforderte** offene Übergang besteht | `anzahl ≥ 1` für O03, O04, O05 und den Ersatzfall O01/O02 (§ 1e); Ergänzung des Planers, damit S5b keine geforderten Übergänge löscht; None = Verstoß |
| (9) | Mollgasse 1OG: keine Zirkulation in der Wohnung | `python scripts/analyse/mollgasse_gt_vergleich.py 1OG` gegen `tests/fixtures/mollgasse_gt/`: Zirkulationspunkte in ZIMMER, BAD, WC und privatem VORRAUM = 0 (Owner-Ansage 2026-09-20, Abnahme von S7a+S7b, § 6f). Vorher-Wert laut Leonis: VORRAUM 69, ZIMMER 3, dazu WC/BAD/AR — **nicht selbst gemessen**. **Noch nicht in `gate_regel.py` verdrahtet:** Skript, Fixtures und Leonis' Bericht liegen am 2026-09-20 weder auf `origin/main` noch auf einem anderen Remote-Branch; bis sie im Baum sind, ist (9) Doku-Pflicht, keine geprüfte Regel |

Zur Nummer: die Owner-Ansage vom 2026-09-20 nennt die Mollgasse-Abnahme „Bedingung (7)".
(7) und (8) sind seit `dd3cfdc` mit den Referenz-Verbindungen belegt; die Mollgasse-Abnahme
läuft deshalb als **(9)**, damit keine bestehende Nummer ihre Bedeutung wechselt. (5) bleibt
daneben Abnahme von S7a+S7b (Einraum-Wohnungen auf OG1 sinken).

Zwischenstände der einzelnen Slices werden gemessen und berichtet (`python
tests/gate/gate_messung.py --out <datei.json>`, dann `pruefe_gate`), aber **nicht
gemergt** — auch nicht bei Verbesserung. (5) und (6) bleiben Merge-Pflicht, obwohl der
Türstapel im engen Sinn sie nicht heilen kann — dafür stehen S7a und S3b im Stapel.

Heute liefert `pruefe_gate(nullmessung, nullmessung)` genau neun Verstöße:
`(2) M17-02-b ist NICHT_BESTANDEN`, `(2) M17-04-c ist NICHT_BESTANDEN`,
`(5) Einraum-Wohnungen sinken nicht: 2 → 2` und sechs Verstöße gegen (7) — die sechs
bestehenden verneinten Verbindungen aus § 2e (zusammen 8 Durchgänge). (8) ist auf f15d03f
erfüllt.

**Test:** `tests/gate/test_gate_tuerstapel.py::test_gate_tuerstapel_erfuellt` ist
`xfail(strict=True, raises=AssertionError)`. Er bleibt rot-per-Design (XFAIL), bis der
Stapel das Gate erfüllt; dann dreht er auf XPASS, der strenge Marker lässt die Suite
fehlschlagen, der Marker wird entfernt und der Stapel gemergt. Infrastrukturfehler
(Exception statt AssertionError) gehen nicht als XFAIL durch. Die Gate-Tests tragen den
Marker `gate` und sind — wie `visual` — in der normalen Suite deselektiert
(`pytest -m gate tests/gate`, ~45 s mit vorhandenen Caches, ~2,5 min kalt). Ohne
Referenzpaket (CI) werden sie übersprungen; ist `NOTBEL_M17_REFERENZ` gesetzt, aber
ungültig, schlagen sie fehl statt still zu skippen.

---

## 4. Toleranzen und die Entscheidung zu M17-02-c

Enis' Fassung 2 ließ M17-02-c offen, weil die Kontaktprädikate am T-Knoten zwischen
ungerundeter Quell- und gerundeter Exportpräzision kippen (3,14 × 10⁻⁸ mm /
`intersects = False` gegen 0,0 mm / 0,0034 mm² Überlappung).

**Entscheidung (Owner, 2026-09-18), im Gate festgehalten** (`gate_m17.py`, `meta.toleranzen`,
von Bedingung (0) verglichen):

| Wert | Bedeutung |
|---|---|
| `KONTAKT_TOL_MM = 1,0` | Zwei Wandkörper gelten als anschließend, wenn ihr Abstand ≤ 1 mm ist; der Knotenpunkt J muss beiden Körpern ≤ 1 mm nahe sein |
| `UEBERLAPPUNG_TOL_MM2 = 1,0` | Überlappung ≤ 1 mm² gilt als Berührung; mehr wird als „Durchdringung" vermerkt, bricht den Kontakt aber nicht |
| `PORTAL_WAND_MM = 250,0` | Abstand Tür ↔ Wandquelle, bis zu dem eine Tür „an der markierten Wand" liegt (= `tuer_zuordnung._KONTAKT_MM`) |

Gemessen wird **auf der Quellpräzision im Speicher** (`Wandkoerper.polygon_mm` des Laufs),
nie auf exportierten oder gerundeten Werten; die Messwerte werden signifikant gespeichert
(3,14e-08, nicht 0,000).

Zweiter Teil „kein Flutungsleck": freie Fläche = `clip` minus alle Einzel-Wandkörper, jeder
um 0,5 mm gepuffert (Spalte bis zur Toleranz gelten als geschlossen); Leck = ein
zusammenhängender freier Teil schneidet sowohl das kleine Bad (`raum_6`) als auch das
große Bad (`raum_7`) mit je > 1 mm².

**Ergebnis auf f15d03f:** Körper 72 (`27C6`) und 73 (`27CF`) je mit Deckung 1,0 zur Quelle
erkannt; Abstand 3,14 × 10⁻⁸ mm, J-Abstände 0,0 / 5,9 × 10⁻⁸ mm, Überlappung 0 mm²,
`intersects`/`touches` beide False (also keine Berührung im exakten Sinn, aber weit unter
der Toleranz). Vier freie Teile im Ausschnitt, keiner verbindet beide Bäder →
**kein Flutungsleck → M17-02-c BESTANDEN.**

---

## 5. Was dieses Gate nicht ist

- Kein Slice ist gebaut; die Erkennung ist unverändert (`src/` und `scripts/` unberührt,
  `basis_tree_gleich = true`).
- Sechs geprüfte Stellen eines Geschosses plus vier Kennzahlen sind kein Nachweis für
  andere Pläne. Die Merge-Gates von Tranche 1 (S1/S2/S9 auf Barawitzka, Mollgasse,
  Muthgasse; S3a-Nachmessung nach dem Türstapel) bleiben offen und werden hier nicht
  ersetzt.
- Die Referenz ist Fachreferenz, kein freigegebener Prüfkorpus; nichts davon liegt im
  Repository (nur Hashes, IDs, Prüfarten und Handles der ohnehin getrackten DXF).
- Auf diesem Branch ist weiterhin kein Slice gebaut. S4a, S4b und S5b liegen auf ihren
  eigenen Branches (`selman/fix-s4a-tuerbloecke`, `selman/fix-s4b-seitenprobe`,
  `selman/fix-s5b-querung`), jeweils gemessen, keiner gemergt.

---

## 5a. Folgeauftrag nach dem Stapel-Merge: S-KG — Kellergeschosse und Garage (vorgemerkt, kein Code)

Owner-Ansage 2026-09-20, aus Leonis' Paket. **Nicht Teil des Stapels, nicht Teil dieses
Gates**; S-KG beginnt erst, wenn der Stapel gemergt ist. Spiegel in `docs/OFFENE_FRAGEN.md`.

1. **Einlagerungsräume:** Stempel „ER" plus Nummer, Raumtyp KELLERABTEIL. Befund 2026-09-20:
   KELLERABTEIL steht **nicht** im Kanon — `docs/VOKABULAR.md` kennt den Typ nicht,
   `raumtyp.py` bildet den Text „kellerabteil" auf den Kanon-Typ `KELLER` ab. Also Vorschlag
   über das Board, nicht still einführen. Das vom Owner genannte Muster
   (`knowledge/Pläne zeichnen Wissen/Mollgasse-Notbeleuchtungserklärung/`) liegt am
   2026-09-20 nicht im Baum.
2. **Garage-Zirkulation:** Fahrgassen und Gehbereiche begehbar, Motorrad-Stellflächen
   durchquerbar; Doppelparker, PKW-Stellplätze und Gruben nicht (NB-R17 in
   `knowledge/notbeleuchtung/regeln.md`, Stempel stehen im Plan). NB-R17 ist am 2026-09-20
   in `knowledge/` dieses Baums nicht auffindbar — kommt mit Leonis' Paket.
3. **Gebäudehälften Mollgasse / Anastasius-Grün-Gasse:** Zirkulation je Hälfte
   zusammenhängend, Trennung ist die Gebäudewand, EG als Referenz. Abbildung über
   Graph-Komponenten, kein neues Contract-Feld.
4. **Treppenläufe im KG** bleiben wie verifiziert (1KG 2×4, 2KG 4/0/3).

Abnahme: `mollgasse_gt_vergleich.py 1KG` und `2KG` — KELLERABTEIL > 0, Segmente zweistellig,
„fehlt" im 2KG deutlich unter 20 (laut Owner heute 20 von 29 Experten-Leuchten unerreichbar;
nicht selbst gemessen, Skript nicht im Baum).

---

## 5b. Übergabe Leonis — die „nicht-im-Merge"-Pakete (eingetragen 2026-09-23, Selman)

**Vermerk:** nach 12-Pläne-Gate-Merge, Quelle Leonis, HEAD `8257ff9`
(`docs/HANDOFF_SELMAN_NICHT_IM_MERGE.md` auf `leonis/demo-l-gebaeude`).
**Reihenfolge:** Der laufende Türstapel (S7a/b/c, dann S4e, S4c, S3b, S5c, Gate-Lauf, Merge) bleibt
unverändert vorne. Die drei Pakete sind Folgeaufträge, sie werden jetzt nicht gebaut.

Owner-Ansage im Wortlaut:

> Reihenfolge der drei Pakete: S-KG → S4d → WOHNKÜCHE. Bei jedem gilt: nach meinem Stand pinge ich Leonis, er fährt Consumer- und Naht-Prüfung plus GT-Re-Run. Kein Contract-Touch nötig; falls doch, erst in docs/COORDINATION.md, 3-Owner.
>
> 1. S-KG (Kellergeschosse + Garage), größter Hebel für die GT-Quote. Soll: KELLERABTEIL erkennen (Stempel "ER"), Garage-Zirkulation (NB-R17: Motorrad durchquerbar, Doppelparker/PKW/Gruben nicht), Gebäudehälften zusammenhängend. Leonis' Engine-Vorlauf NB-R13 (UG flüchtet hinauf) steht, sobald ich liefere, platziert die Engine ohne weiteren Leonis-Bau. Abnahme: python scripts/analyse/mollgasse_gt_vergleich.py 1KG 2KG → KELLERABTEIL > 0, Zirk-Segmente zweistellig, "fehlt" im 2KG < 20. Material: docs/COORDINATION.md §S-KG, knowledge/notbeleuchtung/abgleich/{1KG,2KG}/, GT-Fixtures tests/fixtures/mollgasse_gt/{1KG,2KG}.json.
> 2. S4d (Balkontür): Balkontüren dürfen nicht als final_exit zählen, Wurzel der dünnen Fluchtwege. Leonis' Consumer-Seite (ist_echte_tuer, R2) ist gebaut und freigegeben. Nach meinem Fix Leonis pingen, er re-testet Elektroplan v9+ und die E2E-Bänder.
> 3. KINDERZIMMER/WOHNKÜCHE: KINDERZIMMER ist schon Kanon (falls es hakt, ist es ein Token). WOHNKÜCHE neu: ich lege RoomType.WOHNKUECHE plus Erkennungs-Token an, Alias mit Leonis gegenprüfen, Enis macht die Norm, gemeinsam mergen (test_lb_raumtyp_naht.py guardet beide Richtungen).

**Planer-Vermerk 2026-09-23 (Zitat oben unverändert):** Die Nummer „S4d" war doppelt vergeben.
Leonis behält **S4d** (Balkontür-Folgeregel, auf dieser Seite bereits gebaut). Das Selman-Paket
„ArchiCAD-Türblöcke / Rectangular Door Opening" heißt ab jetzt **S4f**; die drei Restlöcher aus
Leonis' Regel (`provider.py:102`, `ausgaenge.py:69`, EG-Ausnahme `tuer_68`) laufen als **S4g**.
Beide stehen in `docs/OFFENE_FRAGEN.md`. KINDERZIMMER ist erledigt (Kanon mit zwei
Erkennungswegen), der geplante Slice entfällt. WOHNKÜCHE: Stempel-Messung erst nach dem
Gate-Merge, bis dahin nur ein grober Anhalt (54 typlose Räume über 12 Pläne, belegter Fall
Rennweg OG1 `raum_10` mit 73,06 m²).

---

## 6. Diagnose S7a — Vorraum mit Stiegenhaustür wird Erschließung (U14/F11, kein Code)

Gemessen am 2026-09-19 auf Code-Stand `1e5e5ac` (S4a+S4b, also **vor** S5b) über alle
10 Prüfpläne (7 Rennweg-Geschosse, Barawitzka EG, Mollgasse EG, Muthgasse E2), je Plan ein
In-Memory-Lauf (`ArchitekturRaumProvider.parse` plus Abgriff des Zustands vor
`bilde_wohnungen`; kein Output erzeugt — die Regel „kein Pipeline-Rerun in Diagnosen" ist
damit gewahrt). Die F11-Regel wurde in einem Scratch-Skript nachgebildet und
`bilde_wohnungen` mit ausgetauschter Verfeinerung gefahren; die Originalfunktion
reproduziert auf dem abgegriffenen Zustand die Klassen des Endmodells auf allen 10 Plänen.

### 6a. Die Stelle

`wohnungen.py:32-55`, `_verfeinere_gang_privat`, entscheidend Z. 48-52:

```python
fremd = andere in by_id and (
    by_id[andere].raum_typ == "STIEGENHAUS"
    or _klasse(by_id[andere]) not in ("WOHNUNG_PRIVAT", None))
if andere == AUSSEN or fremd:
    privat_ok = False
```

Jeder GANG/VORRAUM mit **einer einzigen** Tür zu STIEGENHAUS, AUSSEN oder einer
Nicht-Privat-Klasse wird `ALLGEMEIN_ERSCHLIESSUNG` (Z. 53-55); Türblatt, Breite, Richtung
und Zahl der erschlossenen Wohnungen spielen keine Rolle. Folgen in Laufreihenfolge:
`provider.py:167` typisiert die Türen **vor** `bilde_wohnungen` (`:172`) mit den statischen
Klassen (VR↔STIEGENHAUS → `wohnungseingang`, `tuer_typisierung.py:190-191`);
`wohnungen.py:61-64` setzt Defaults und verfeinert **einmal in Raumreihenfolge** über einen
Mischzustand (statische Defaults, progressiv überschrieben — weder rein statisch noch
Fixpunkt); `:66` bildet die Privat-Menge danach; `:71-80` stuft `wohnungseingang` zwischen
zwei Privaten zu `zimmertuer` und `zimmertuer` mit genau einer privaten Seite zu
`wohnungseingang` — **nicht** zurückgestuft wird ein `wohnungseingang` zwischen zwei
allgemeinen Räumen (OG1 `tuer_3` trägt ihn heute, beide Seiten allgemein → S7c); `:82-93`
verbindet nur privat↔privat, ein allgemein gewordener Vorraum **trennt** die Gruppen;
`:95-112` macht jede Gruppe zu `top_n` ohne Mindestkriterium (U16). Konsumenten der Rollen:
`ausgaenge.py:74-76` (`stiegenhaustuer`/`brandschutztuer` → `stair_exit`),
`fluchtweg.py:288-289` (`wohnungseingang` = Fluchtweg-Start).

### 6b. Die Regel (Owner/F11), wie sie nachgebildet wurde

Vorraum mit Stiegenhaustür ist PRIVAT, die Stiegenhaustür sein Wohnungseingang; ALLGEMEIN
nur, wenn er vom Stiegenhaus **ohne Wohnungseingang erreichbar** ist (offener Übergang) UND
mindestens **zwei Wohnungen oder ein Ausgang** darüber erschlossen werden. Nachgebildet mit
diesen Festlegungen (jede davon ist eine offene Entscheidung, § 6e):

- „offener Übergang": Lesart (a) **direkt** = eigene Tür zum STIEGENHAUS mit
  `ohne_tuerblatt`; Lesart (b) **Kette** = vom STIEGENHAUS nur über `ohne_tuerblatt`-Türen
  erreichbar. Bei 8 von 9 Kandidaten fallen sie zusammen; Barawitzka `raum_19` VR 3,42
  (Stiegenhaustür `tuer_28` = Bogen **mit** Blatt 960 mm) ist nur unter (b) allgemein
  (Kette STIEGENHAUS → ABSTELLRAUM 1,42 → VORRAUM 5,11 → VORRAUM 3,42, alle ohne Blatt).
- „Wohnungen": getrennte private Komponenten, die über Türen am Raum hängen, **jede
  Komponente zählt, auch ein einzelnes WC/AR** (Modellierungsannahme; OG1 AR 4,52 + WC 3,50
  → 2 Gruppen für Vorraum 10,94).
- „Ausgang": eigene Tür nach `AUSSEN` (eine TERRASSE-Raumtür zählt nicht).
- Geltungsbereich: **V1 (wörtlich)** ersetzt die heutige Regel für alle GANG/VORRAUM;
  **V2 (eng)** nur für GANG/VORRAUM mit Stiegenhaustür.
- Zählbasis der Gruppen: „heutig" (Klassen des Endmodells), „statisch"
  (`nutzungsklasse_fuer`) und „Fixpunkt" (Regel iterativ auf ihr Ergebnis; konvergiert auf
  allen 10 Plänen in ≤ 4 Iterationen). Die Tabellen unten stehen auf „heutig".

### 6c. Blast Radius (Zählbasis „heutig")

| Plan | Whg heute | Einraum heute | Whg V1 | Einraum V1 | Whg V2 | Einraum V2 | Kipp A→P V1 | Kipp A→P V2 |
|---|---|---|---|---|---|---|---|---|
| Rennweg UG | 4 | 4 | 2 | 1 | 4 | 3 | 3 | 1 |
| Rennweg EG | 2 | 1 | 2 | 1 | 2 | 1 | 1 | 1 |
| Rennweg OG1 | 3 | 2 | 2 | 0 | 2 | 0 | 1 | 1 |
| Rennweg OG2 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| Rennweg OG3 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| Rennweg DG1 | 1 | 0 | 3 | 0 | 1 | 0 | 1 | 1 |
| Rennweg DG2 | 1 | 0 | 1 | 0 | 1 | 0 | 2 | 2 |
| Barawitzka EG | 6 | 4 | 8 | 6 | 6 | 4 | 0 | 0 |
| Mollgasse EG | 9 | 2 | 12 | 5 | 10 | 3 | 7 | 1 |
| Muthgasse E2 | 7 | 3 | 7 | 3 | 7 | 3 | 2 | 0 |

„Kipp A→P" = heute ALLGEMEIN_ERSCHLIESSUNG, nach Regel privat (das Risiko). **V1 kippt 17
Räume A→P** (18 auf Basis „statisch", 16 im Fixpunkt) und 4 P→A, darunter Mollgasse
`raum_34` GANG 6,92 **mit Hauseingang** (`tuer_16` → AUSSEN) und Rennweg UG GANG 8,30 —
V1 ist gefährlich. **V2 kippt 7** (6 im Fixpunkt), 0 P→A.

Nur **neun** GANG/VORRAUM mit Stiegenhaustür gibt es über alle 10 Pläne. Die 7 Kipp-Fälle
unter V2: Rennweg UG `raum_12` GANG 5,35 (`tuer_7` 940 mm **mit Blatt**, heute
`stiegenhaustuer`); Rennweg EG `raum_6` VR 21,03 (`durchgang_14` 2600 mm offen + Garage);
Rennweg OG1 `raum_12` VR 10,94 (`tuer_3` 940 mm **mit Blatt**, T01); Rennweg DG1 `raum_8`
VR 8,94 (3 Durchgänge zu `rest_2`/`rest_3` STIEGENHAUS, alle ohne Blatt); Rennweg DG2
`raum_6` VR/Büro 15,96 (2 Durchgänge zu `rest_1`/`rest_3`, dazu TERRASSE-Tür) und `raum_7`
VR 15,20 (**5** Durchgänge zu `rest_1/3/4`, ohne Blatt — **hängt an der Zählbasis**: 1/2/2
Gruppen für heutig/statisch/Fixpunkt); Mollgasse `raum_7` VR 8,17 (`durchgang_10` zum
STIEGENHAUS, **7690 mm** breit). Allgemein bleiben Rennweg EG `raum_16` GANG 7,36 (offener
Übergang + Hauseingang, stabil) und Barawitzka `raum_19` (nicht stabil, s. o.).

**Türblätter:** von den 14 Stiegenhaustüren der 7 Kipp-Räume sind **12 ohne Türblatt**
(Durchgänge 1114–7690 mm), nur UG `tuer_7` und OG1 `tuer_3` haben eines. S7a steht damit
überwiegend auf Öffnungen, die S5b/S5c entscheiden (F10); auf DG1/DG2 führen sie zusätzlich
zu REST-Komponenten (S3b). 14 Türen würden Wohnungseingang: UG `tuer_7`, EG `durchgang_14`,
OG1 `tuer_3`, DG1 `durchgang_9/10/11`, DG2 `durchgang_10/11` und `durchgang_12–16`,
Mollgasse `durchgang_10`. Rollenwechsel unter V2: 12 × `wohnungseingang → zimmertuer`
(UG `tuer_3`; EG `durchgang_2/5/7/8`; OG1 `tuer_10/11`; DG1 `durchgang_3`; DG2
`tuer_1/2/3`, `durchgang_3`), kein Wechsel von/nach `stiegenhaustuer`.

Die drei genannten Geschosse konkret: **OG1** — Vorraum 10,94 → privat (stabil über alle
Zählbasen), `top_2` = AR 4,52 + VR 10,94 + WC 3,50 mit Eingang `tuer_3`, **Wohnungen 3 → 2,
Einraum 2 → 0** (Bedingung (5) erreichbar), aber die neue `top_2` hat keinen Aufenthaltsraum
(F12/S7b). **OG3** — die Regel ändert nichts (einziger Kandidat GANG 9,38 ohne
Stiegenhaus-Tür; das Stiegenhaus ist `rest_3`/`rest_4`, keine Tür erreicht es → S3b).
**DG2** — Basis „heutig": `raum_6` und `raum_7` privat, `top_1` wächst von 4 auf 6 Räume,
1 Wohnung / 0 Einraum, 4 Rollen kippen; Basis „statisch"/Fixpunkt: nur `raum_6` kippt →
2 Wohnungen / 1 Einraum.

### 6d. Risiken (gemessen)

1. **„Verlorenes Notlicht" tritt auf den 10 Plänen nicht ein.** Der einzige Klassenfilter
   der Platzierung (`flaechen_strategy.py:162-167`) verlangt `WOHNUNG_PRIVAT` **und** `not
   ist_fluchtweg` **und** `not ist_communal`; GANG/VORRAUM tragen beide Flags statisch
   (`raumtyp.py:29-30`), alle 7 Kipp-Räume haben `ist_fluchtweg = ist_communal = True`.
   Der Satz der Diagnose (U14) gilt nur, wenn zusätzlich diese Flags fallen.
2. **Ein `stair_exit` steht auf dem Spiel.** Unter V2 ändert sich keine Rolle von/nach
   `stiegenhaustuer`. Der zweite Halbsatz der Regel („die Stiegenhaustür ist sein
   Wohnungseingang") ist aber im Code nicht vorhanden: `wohnungen.py:75-80` stuft nur
   `zimmertuer` hoch. Rennweg UG `tuer_7` bliebe `stiegenhaustuer`, die neue `top_1` (GANG
   5,35 + WC 6,17) hätte keinen Eingang; wird der Halbsatz gebaut, wird `tuer_7`
   `wohnungseingang` und der `stair_exit` dort entfällt — der sicherheitsrelevante Punkt
   von S7a liegt in der Rollen-, nicht in der Klassenregel.
3. **Fluchtweg-Starts wandern**: 12 Türen verlieren `wohnungseingang`; ob Segmente dadurch
   ein Ziel verlieren, ist nicht gemessen.

### 6e. Offene Entscheidungen (nicht entschieden)

(a) Geltungsbereich V1 oder V2 (17 zu 7 Kipp-Fälle). (b) Was ist eine „Stiegenhaustür"
— 12 von 14 sind Durchgänge ohne Blatt (bis 7,69 m), teils zu REST-Komponenten; Barawitzka
`raum_19` hängt an Lesart direkt/Kette. (c) Rollenregel: Stiegenhaustür des privat
gewordenen Vorraums → `wohnungseingang` (Owner-Wortlaut, kostet den `stair_exit` an UG
`tuer_7`) oder `stiegenhaustuer` (Wohnung ohne Eingang) → S7c. (d) Wohnungen ohne
Aufenthaltsraum (OG1 `top_2`, UG `top_1`, Mollgasse `top_10` neu) → F12/S7b; zählen sie in
„mindestens zwei Wohnungen"? (e) Mehrere Stiegenhaustüren (DG2 `raum_7` 5, DG1 `raum_8` 3):
welche ist „der" Eingang? (f) DG2 `raum_6` mit TERRASSE-Tür: zählt sie als Ausgang? (g)
Zählbasis heutig/statisch/Fixpunkt — die Regel ist zirkulär; der Fixpunkt löst es technisch,
ist aber eine Festlegung; der heutige Code macht keines von dreien (Reihenfolgeabhängigkeit).

### 6f. Erweiterung zu S7a+S7b — „Wohnung ≠ Fluchtweg" (Owner-Ansage 2026-09-20, Leonis' Paket S-W)

Gleiche Wurzel wie S7a (F11): Vorraum mit Stiegenhaustür ist privat, die Stiegenhaustür ist
sein Wohnungseingang. Der Owner bekräftigt damit den Wortlaut aus § 6b; die in § 6e offenen
Festlegungen bleiben vor dem Bau zu treffen. Dazu aus Leonis' Paket, als ein Slice-Paar:

1. Wohnungen als Einheiten trennen — die Umrisse existieren bereits.
2. Zirkulation an der Wohnungseingangstür stoppen: kein Fluchtweg-Segment hinter die
   Wohnungstür.
3. `ist_fluchtweg` und `ist_communal` differenzieren: wohnungsinterne GANG und VORRAUM
   bekommen beides `False`. Das sind bestehende Felder, keine Contract-Änderung. Fehlt doch
   ein Feld: erst ins Board, nicht bauen.
4. Fluchtweg-Segmente nur auf communal-Gängen und Stiegenhäusern.

**Folge für § 6d Punkt 1:** Dort tritt „verlorenes Notlicht" nur deshalb nicht ein, weil
GANG/VORRAUM beide Flags heute statisch tragen (`raumtyp.py`) und der Klassenfilter der
Platzierung zusätzlich `not ist_fluchtweg` und `not ist_communal` verlangt. Mit Punkt 3
fällt dieser Schutz für wohnungsinterne Gänge und Vorräume **gewollt** weg — die sieben
Kipp-Räume aus § 6c fallen dann unter den Klassenfilter. Das ist der Zweck des Pakets,
macht aber die Klassenregel sicherheitsrelevant: vor dem Bau je Kipp-Raum gegen den Plan
prüfen, dass er wirklich wohnungsintern ist (12 der 14 Stiegenhaustüren sind Durchgänge
ohne Türblatt, § 6c).

**Testdaten zusätzlich zu Rennweg:** `Projekte_Leere Architektpläne (Input)/Mollgasse/`,
8 Geschosse (im Repo als `Mollgasse.zip` getrackt), in Metern gezeichnet bei INSUNITS mm.
Laut Leonis greift die ×1000-Kalibrierung dort bereits korrekt — **im Slice zu prüfen**,
hier nicht gemessen.

**Abnahme:** Gate-Bedingung (9) (§ 3) und weiterhin (5). Leonis' Unterlagen (Board-Eintrag
2026-09-20, `MOLLGASSE_RIVOPLAN_GT_BERICHT` § K, `scripts/analyse/mollgasse_gt_vergleich.py`,
`tests/fixtures/mollgasse_gt/`) liegen am 2026-09-20 auf keinem Remote-Branch; der Wortlaut
oben stammt aus der Owner-Ansage.

### 6g. Das Verfahren für S7a+S7b — der gebaute Stand (Owner-Entscheide 2026-09-21 und 2026-09-22)

**Diese Fassung ersetzt die Fassung vom 2026-09-20.** Sie beschreibt den Code der vier
Commits auf `5ac3e0f`: `b77cadf` (Tests zuerst), `d2cb2ef` (die Regel), `6515689`
(strict-xfail von `test_keine_anker_in_wohnung_privat` entfernt, der Marker ist XPASS),
`e617fd1` (Prüfstrecke: unbestimmte Räume magenta, Tiebreak- und Loch-Zeilen im Bericht).
Alle Zeilenangaben beziehen sich auf `e617fd1`.

Zwei Sätze der bisherigen Fassung sind **aufgehoben**:

- **2026-09-20, Schritt 1:** „ein Raum, der vom Stiegenhaus ohne Wohnungseingangstür
  erreichbar ist, ist ALLGEMEIN". Der Owner hat seine eigene Formulierung am 2026-09-21
  korrigiert: F11 ist ein **UND**, die Erreichbarkeit ist bloß die Voraussetzung
  (§ 6g.2).
- **2026-09-21, E5 Satz 2** (Planer-Auslegung, nicht Owner-Wortlaut): „Ein unbestimmter
  Raum darf keine Wohnung ohne Eingang erzeugen; wenn doch, gilt er als allgemein."
  **Aufgehoben am 2026-09-22** — der Satz hat eine Notlicht-Regel (a) auf die
  Wohnungsbildung (b) wirken lassen und die Wohnungen auf OG2, OG3, DG1, Barawitzka und
  Muthgasse zerteilt (Gate 4 → 12). „Keine neue Wohnung ohne Eingang" bleibt als
  **Mess-Abnahme** (§ 6g.7), nicht als Regel im Code.

Unverändert weiter gültig aus der Fassung 2026-09-20: die Begründung der Zweistufigkeit
(die Regel aus § 6b ist **zirkulär** — „erschließt zwei Wohnungen" hängt an den Klassen der
Nachbarn, die daran hängen, ob dieser Gang allgemein ist; Mollgasse 1OG `raum_34` GANG
16,99 m² entschied sich unter zwei Zählbasen gegensätzlich, Segmente 22 → 3 bzw. 22 → 10),
Schritt 3 („unbestimmt statt Raten", konservativ behandelt), der Reihenfolge-Test, die
**Durchleitung** und der Board-Antrag auf ein Segment-Feld `durchleitung`. Ebenfalls weiter
gültig: die Zahlen in § 6c stammen von Code-Stand `1e5e5ac`, also **vor** S5b, und sind vor
dem Bau neu gemessen worden.

#### 6g.1 Die Trennung: (a) Notlicht, (b) Wohnungszugehörigkeit

Owner Selman, 2026-09-22, wörtlich:

> Es sind zwei getrennte Fragen, die nie vermischt werden:
> (a) Bekommt der Raum Notlicht? Entscheidet fail-safe: im Zweifel ja. Nur hierfür gilt
> der Board-4-Satz „bei zwei Fixpunkten gilt der allgemeine".
> (b) Zu welcher Wohnung gehört der Raum? Entscheiden ausschließlich rohe Türen:
> Wohnungseingang ist Grenze, Zimmertür ist innen. Board 4 gilt hierfür nie. Eine Regel zu
> (a) darf keine Wohnung zerteilen.

Darüber steht weiter der Grundsatz aus dem Auftrag der Runde 4: **„Im Zweifel Notlicht
behalten. Fehlendes Notlicht ist gefährlich, überflüssiges nur teurer."** Wo eine Regel
nicht greift oder sich widerspricht, wird nicht entzogen.

Im Code sind die beiden Fragen durch **verschiedene Funktionen mit verschiedener Eingabe**
getrennt (Planer-Vorgabe G1):

| Frage | Funktion | liest | liest nachweislich **nicht** |
|---|---|---|---|
| **(b)** Wohnung | `wohnungsklasse.wohnungszugehoerigkeit` (`wohnungsklasse.py:576`) | `raum_typ`, Tür-Topologie, **rohe** `tuer_detail`, Türblatt, STIEGENHAUS und Türen ins Freie als Ursprung | `nutzungsklasse`, `ist_fluchtweg`/`ist_communal`, `wohnung_id`, korrigierte Rollen, jedes Ergebnis von Schritt 1/2/3, den Fixpunkt-Tiebreak |
| **(a)** Notlicht | `klassifiziere` (`:383`), die Iteration in `wohnungen.bilde_wohnungen` (`wohnungen.py:152`), `bestaetigt_privat` (`:405`), `setze_wohnungsflags` (`:762`) | Klassen, Flags, Riegel, Tiebreak, Beleg-Kriterium | — (darf (b) nicht ändern) |

`bilde_wohnungen` ruft (b) **zuerst und einmal** auf; die Wohnungsgruppen und ihre Eingänge
stehen damit fest, bevor irgendeine Klasse berechnet wird. Beleg: der Naht-Test
`test_r10_wohnung_liest_weder_klasse_noch_tiebreak` fährt 21 Muster mit **verfälschten**
Klassen, Flags und `wohnung_id` und umgedrehtem Tiebreak — die Wohnungszugehörigkeit ist
identisch (21 × grün, Runden 10–14).

#### 6g.2 Schritt 1 / Schritt 2 / Schritt 3 in der gültigen Fassung

**Geltungsbereich V2 (eng), unverändert:** nur GANG/VORRAUM mit mindestens einer Tür zu
einem STIEGENHAUS (`kandidaten`, `wohnungsklasse.py:123`). Für alle anderen GANG/VORRAUM
bleibt `wohnungen._verfeinere_gang_privat` zuständig — unter demselben Riegel.

**Schritt 1 — Ankerregel, ohne Iteration** (`ankerurteil` `:193`, `schritt1` `:233`).
Erreichbarkeit vom STIEGENHAUS über Türen, reine Topologie plus Türtyp; die Funktion
bekommt Raum-IDs und Türen, keine Klassen. Sie entscheidet **nur PRIVAT endgültig**
(E1, das UND aus F11: „ALLGEMEIN nur, wenn vom Stiegenhaus ohne Wohnungseingang erreichbar
UND mindestens zwei Wohnungen oder ein Ausgang darüber erschlossen werden"):

| Befund der Ankerregel | Folge |
|---|---|
| nur über eine `wohnungseingang`-Tür **mit Türblatt** erreichbar | `WOHNUNG_PRIVAT`, endgültig |
| ohne Wohnungseingang erreichbar | nur die erste Hälfte von F11 — **offen** an Schritt 2 |
| nur durch eine **blattlose** Öffnung getrennt | offen an Schritt 2 (E1: „eine blattlose Öffnung schließt keine Wohnung ab") |
| über keine Tür erreichbar (Loch-Raum) | offen; siehe § 6g.5 |

Schritt 1 spricht niemanden privat, den der Riegel sperrt (§ 6g.4).

**Schritt 2 — Erschließungsregel** (`schritt2_urteil` `:335`, `schritt2` `:352`) auf allem,
was Schritt 1 offen lässt. `PRIVAT` genau dann, wenn der Raum **genau eine** Wohnung
erschließt und nichts Allgemeines: keinen Ausgang ins Freie, keinen Raum der Nutzungsklasse
`ALLGEMEIN_NEBENRAUM` (die Menge steht in `nutzungsklasse.py` — Kellerabteil, Keller,
Technik, Müll, Fahrrad, Kinderwagen, Waschküche, Lager), keine zweite Wohnung. Sonst
`ALLGEMEIN` — **auch bei null Wohnungen** (Board 5: „Ein Raum, der null Wohnungen
erschließt (Podest, Foyer), kann nicht privat sein"). Der Nebenraum-Zweig ist die
Owner-Erweiterung vom 2026-09-21 mit der Begründung: in UG/KG gibt es keine Wohnungen — ein
Kellergang würde sonst privat und verlöre sein Notlicht.

„Erschließt" ist **transitiv** definiert (Board 5, `_erschliesst` `:280`): Ziel Z ist von X
erschlossen, wenn Z von X über Türen erreichbar ist und **alle Zwischenräume nicht privat**
sind. Eine erreichte Wohnung zählt und **beendet den Weg dort** (nicht in die Wohnung
hinein); jede getrennte private Komponente zählt als eigene Wohnung, auch ein einzelnes WC.
**Das STIEGENHAUS ist Ursprung, nicht Durchgang** (Planer-Auslegung, im Bericht
ausgewiesen): was nur über das Stiegenhaus erreichbar ist, erschließt das Stiegenhaus, nicht
X. `stair_exit` zählt nicht als Ausgang, nur eine Tür ins Freie.

Iteriert wird bis zum Fixpunkt, **Start bei ALLGEMEIN** (Board 4: von mehreren Fixpunkten
gilt der, der Notlicht behält), Deckel `DECKEL = 10` Runden (`:109`), jede Runde aus
demselben Schnappschuss (Jacobi). Pendelt die Iteration, starten die pendelnden Räume neu
bei ALLGEMEIN.

**Schritt 3 — unbestimmt statt Raten.** Erreicht die Iteration keinen Fixpunkt, bleibt
`nutzungsklasse` `None` (Contract: „None/leer = unbestimmt") und der Grund geht als Warnung
in den Prüfbericht; die Meldung behauptet **nur, was gemessen ist** („die Iteration erreicht
in 10 Runden keinen Fixpunkt; ob die Regel einen hat, ist nicht geprüft"). Ein unbestimmter
Raum wird konservativ behandelt: er ist nicht privat, verliert weder Leuchte noch Anker,
bleibt Knoten im Fluchtweg-Graph und behält seine Stützpunkte (`volle_knoten` `:739`; ohne
das fiel Barawitzka EG `raum_30` aus dem Graph). Auf den 12 Prüfplänen sind **14 Räume
unbestimmt**, alle mit Flags 11 und einer Warnzeile; keiner verliert Anker, Zirkulation,
Stützpunkte oder Leuchten gegenüber HEAD `5ac3e0f`. In allen drei Darstellungen sind sie
**magenta** (`e617fd1`).

#### 6g.3 Fixpunkt-Wahl: physischer Beleg vor Tiebreak

Owner 2026-09-22, Rangfolge bei Konflikt: **der physische Beleg geht dem Fixpunkt-Tiebreak
vor.** Physischer Beleg heißt: ein Wohnungseingang mit Türblatt, und die Ankerregel
bestätigt die strittigen Räume **ausnahmslos** und lässt keinen offen. Der Tiebreak aus
Board 4 („von mehreren Fixpunkten gilt der, der Notlicht behält") gilt nur, wo kein
physischer Beleg entscheidet.

Umsetzung (G2, `wohnungen.py:286-330`): bleiben nach der ersten Iteration **ankerprivate**
Räume allgemein, läuft die Iteration erneut mit ihnen privat gestartet — erst alle
zusammen, dann je Gruppe benachbarter beweglicher Räume (`_gruppen`), jeweils **ab dem
erreichten Stand**, nicht ab ALLGEMEIN (ohne diesen Startstand fiel ein voll belegter
Fixpunkt zusammen — gemessen in 13 von 20 000 Zufallstopologien). Ist das Ergebnis ein
Fixpunkt, in dem **alle** abweichenden Räume privat und ankerbestätigt sind und keiner offen
bleibt, gilt er. Sonst gilt der allgemeine, und jeder solche Raum bekommt eine
`tiebreak:`-Zeile mit Grund. Die Probe läuft nur, wenn der ganze Plan einen Fixpunkt
erreicht hat; pendelt ein fremder Teil, gilt überall der Tiebreak (als `ponytail:`-Deckel
vermerkt, `wohnungen.py:297-299`, Richtung sicher: Notlicht bleibt).

**Wo das real entscheidet, auf den 12 Plänen:**

- **Beleg gewinnt:** Rennweg OG1 `raum_4`/`raum_5` werden `WOHNUNG_PRIVAT` (Flags 00),
  `bestaetigt_privat` = {`raum_4`, `raum_5`, `raum_8`}; auf OG1 steht **keine**
  `tiebreak:`-Zeile.
- **Tiebreak entscheidet:** **genau ein Fall** über alle 12 Pläne — Mollgasse EG `raum_57`
  VORRAUM 7,78 m². Grund in der Warnzeile: die Ankerregel urteilt privat, es wurde aber
  **kein voll ankerbestätigter Fixpunkt gefunden**; ob daneben ein zweiter Fixpunkt
  besteht, ist nicht geprüft. Der Raum bleibt `ALLGEMEIN_ERSCHLIESSUNG` mit Flags 11,
  behält also sein Notlicht. Die Zeile behauptet ausdrücklich keinen zweiten Fixpunkt — die
  Zeugensuche des Reviewers fand keinen (0 von 12 Dumps, Planer-Korrektur P4).

Der Planer-Entscheid P3 (die Probe startet ab dem erreichten Stand) ist **kein
„fail-safe only"**-Eingriff: in 40 000 Zufallsplänen unterscheidet er 54 Klassen, in 31
davon **entzieht** er Notlicht, das der Vorstand behielt. Richtig ist: **P3 setzt G2 durch,
und G2 stellt den physischen Beleg über den Fail-Safe-Tiebreak.** Auf den 12 Prüfplänen ist
P3 wirkungslos (Klassen und Flags 12/12 unverändert).

#### 6g.4 Riegel (G3), Entzugs-Kriterium (G4) und die Lesart von „bestätigt"

**Riegel (G3), Owner 2026-09-22 wörtlich:** „Ein Raum mit Hauseingang, Tür ins Freie oder
Tür zu einem allgemeinen Nebenraum ist in **keinem** Schritt PRIVAT, auch nicht in Schritt 1
und nicht an der E8-Grenze." Umgesetzt in `riegel_nie_privat` (`:250`); gelesen werden nur
Raumtyp, Tür-Topologie und rohe Rolle. Auf den 12 Plänen greift der Riegel bei **8 Räumen**,
alle `ALLGEMEIN_ERSCHLIESSUNG` mit Flags 11. **Offengelegte Asymmetrie:** „Tür ins Freie"
zählt hier **jede** Tür nach AUSSEN, auch eine Balkontür; der (b)-Ursprung in
`wohnungszugehoerigkeit` schließt die Balkontür ausdrücklich aus. Die Richtung ist sicher
(der Riegel nimmt kein Notlicht, er verhindert nur den Entzug), und auf den 12 Prüfplänen
hat kein GANG/VORRAUM eine Balkontür.

**Entzugs-Kriterium.** Notlicht (beide Flags `False`, R3, und keine eigenen Anker/Leuchten,
R4) wird **nur** entzogen, wenn alle vier Bedingungen zusammen zutreffen:

1. Klasse `WOHNUNG_PRIVAT`,
2. die **Ankerregel auf den ROHEN Rollen** urteilt privat (Wohnungseingang mit Türblatt),
3. **G4 (Owner 2026-09-22):** in derselben Wohnung nach (b) liegt mindestens ein
   **Aufenthaltsraum** — `AUFENTHALTSRAUM` = {ZIMMER, WOHNZIMMER, SCHLAFZIMMER, KÜCHE}
   (`:107`, Kanon-Namen aus `raumtyp.py`). Bad, WC, Abstellraum oder untypisierte Räume
   allein belegen keine Wohnung, dort bleibt Notlicht. **Keine Geschossregel** (die
   Geschosserkennung liefert auf 41 von 62 Plänen nichts).
4. kein Riegel nach G3.

**Lesart „bestätigt", für diese Doku festgeschrieben** (Owner 2026-09-22): *bestätigt =
Klasse `WOHNUNG_PRIVAT` **∧** Ankerregel auf rohen Rollen privat.* Das sind die Bedingungen
1 und 2, im Code die Zwischenmenge `kandidat` in `bestaetigt_privat` (`:405`).

**Wichtig für jeden, der den Code gegen diesen Text liest** (Naht-Urteil R13, Punkt (d)):
die Code-Funktion `bestaetigt_privat` meint die um **G4 und den Riegel verengte** Menge,
also `kandidat ∩ belegt − riegel`. Sie ist **enger** als die Owner-Lesart. Gemessen auf
Mollgasse 1OG: Owner-Lesart 11 Räume (`raum_2`, `4`, `5`, `16`, `19`, `26`, `37`, `42`,
`63`, `69`, `72`), Code-Menge 6 (`raum_2`, `4`, `5`, `37`, `42`, `63`). Enger heißt weniger
Entzug, also fail-safe; beide Verengungen sind selbst Owner-Entscheide vom 2026-09-22. Wer
eine Zusicherung mit dem Wort „bestätigt" formuliert, muss deshalb sagen, **welche** der
beiden Mengen er meint — ein Guard, dessen Wirkung an der Lesart eines Wortes hängt, ist
kein Guard (§ 6g.9).

`bestaetigt_privat` liegt ohne eigenen `raum_typ`-Filter **ganz in GANG/VORRAUM**, und zwar
**per Konstruktion**: `ankerurteil` überspringt jeden Nicht-Scope-Raum, der Default ist
`A_UNKLAR`. Ein zusätzliches `and r.raum_typ in SCOPE_TYPEN` wäre ein beweisbarer No-Op und
ist darum nur als Kommentar an der Stelle vermerkt, nicht als Bedingung.

#### 6g.5 Loch-Räume und die R1-Regel (Loch-GANG zu Einzelräumen)

**Loch-Raum** = GANG/VORRAUM, den die Ankerregel vom Stiegenhaus über **keine** Tür
erreicht (`loch_raeume` `:466`). Owner 2026-09-21: „das ist ein Tür- oder Raumerkennungsloch,
kein Klassifikationsproblem" (Messfall für S4c und S3b). Nicht dazu gehört der nur durch
eine blattlose Öffnung getrennte Raum (E1; Mollgasse EG `raum_23`).

Für (b) gilt (Owner-Fragebogen 2026-09-22): ein Loch-Raum, der über eine **rohe Zimmertür**
an eine Wohnung gebunden ist, gehört zu dieser Wohnung und bleibt für (a) unbestimmt **mit**
Notlicht (Flags 11). Ein Loch-Raum, der nur über **rohe Wohnungseingänge** angebunden ist,
ist Erschließung und für (a) allgemein.

**R1 (Owner-Entscheid 2026-09-22), Ausnahme davon:** *Ein Loch-**GANG**, hinter dessen rohen
Wohnungseingängen **nur Einzelräume** liegen (jede dahinterliegende Raumgruppe hat genau
einen Raum), bildet mit diesen Räumen **eine** Wohnung; er selbst bleibt für (a) unbestimmt
mit Notlicht.* Umgesetzt in `_loch_gang_einzelraeume` (`:549`) — reine Topologie der rohen
Türen, liest keine Klasse.

Grund für die Regel: die rohe Rolle `wohnungseingang` ist bei GANG-Türen **kein physischer
Beleg**. `tuer_typisierung.py:197` (Regel 5) setzt sie allein aus dem Raumtyp-Paar
`ALLGEMEIN_ERSCHLIESSUNG × WOHNUNG_PRIVAT`, und im Kanon ist GANG statisch allgemein,
VORRAUM statisch privat. Ein Wohnungsflur vom Typ GANG trägt roh daher an **jeder** Tür
einen „Wohnungseingang"; ein Loch-VORRAUM bindet über Zimmertüren, ein Loch-GANG nie. Die
Wurzel ist ein Erkennungsfehler, keine Klassenfrage — sie wird in Slice **S4e** behoben
(§ 6g.8); R1 bleibt daneben in Kraft und fängt die Fälle, die S4e nicht klärt.

| Fall | Befund |
|---|---|
| **Messfall Rennweg OG3 `raum_10`** GANG | hinter den vier rohen Wohnungseingängen liegen nur Einzelräume (`durchgang_1` → `raum_1` KÜCHE 38,35 m² blattlos, `tuer_11` → `raum_4` ZIMMER 23,27 m², `tuer_13` → `raum_6` BAD 6,01 m², `tuer_14` → `raum_7` ABSTELLRAUM 3,51 m²). R1 bindet: **eine** Wohnung `{raum_1, raum_4, raum_6, raum_7, raum_10}` wie HEAD, Einraum 0, `raum_10` selbst unbestimmt mit Flags 11 und eigener Begründung in der Warnzeile. Ohne R1 wären es 6 Wohnungen und 4 Einraum-Wohnungen |
| **Gegenfall Muthgasse E2 `raum_94`** GANG | bleibt Erschließung, weil hinter seinen rohen Wohnungseingängen **mehrräumige** Wohnungen liegen (6 Kandidaten-Türen, u. a. `tuer_7` → `raum_51` VORRAUM) |

Auf den 12 Plänen gibt es **16 Loch-Räume**: 10 über rohe Zimmertür gebunden, **1 nach R1**
(OG3 `raum_10`), 5 Erschließung ohne Wohnung (OG2 `raum_9`, MOLL_1OG `raum_52`/`raum_65`,
MUTH `raum_46`/`raum_94`).

**R1 kann strukturell nie an einen GANG/VORRAUM binden** (spart dem nächsten Prüfer den
Grenzfall): ein Loch-GANG ist vom Stiegenhaus über keine Tür erreichbar, also ist jeder Raum
hinter seinen rohen Wohnungseingängen ebenfalls unerreichbar; ist dieser Nachbar
GANG/VORRAUM, ist er selbst Loch-Raum und liegt in der freien, nicht in der gebundenen Menge
(keine Gruppengröße, keine Bindung); kommt er über eine rohe Zimmertür in die gebundene
Menge, ist seine Gruppe ≥ 2 und die Bedingung „nur Einzelräume" ist verletzt. Verifiziert mit
2 Konstruktionen und 2 258 R1-Bindungen in 40 000 Zufallsplänen, **0 mit
GANG/VORRAUM-Nachbar**; auf OG3 sind die Nachbarn von `raum_10` KÜCHE, ZIMMER, BAD und
ABSTELLRAUM.

**R2 (Owner 2026-09-22):** ein **untypisierter** Raum gehört nie zu einer Wohnung („kein
Beleg", passend zu G4). Die Folgen sind akzeptiert und hier benannt: MOLL_1OG `raum_69` wird
eine Einraum-Wohnung, Rennweg OG1 `raum_10` (73,06 m², Wohnküchen-Stempel) bleibt ohne
Wohnung.

#### 6g.6 Einbahn (Board 7): rohe Rolle → Klasse → korrigierte Rolle → Fluchtweg

Owner Board 7: „Die Ankerregel liest nur rohe Türrollen, nie Raumklassen und nie korrigierte
Rollen. Korrigierte Rollen (S7c, Wohnungseingang wandert nach außen) entstehen danach aus
der fertigen Klassifikation und werden nur für Fluchtweg und Zirkulation verwendet. Die
Richtung ist einseitig: rohe Rolle → Klasse → korrigierte Rolle → Fluchtweg, nie zurück."

Gebaut ist Entscheidung **(i)**: die korrigierten Rollen werden **nicht** in `tuer_detail`
persistiert.

- **Wo sie entstehen:** `wohnungsklasse.korrigierte_rollen` (`:646`), genau einmal, aus der
  fertigen Klassifikation und den rohen Rollen. Eine Zimmertür oder ein Wohnungseingang
  zwischen zwei Räumen der Wohnungsmenge ist eine Zimmertür; zwischen Wohnung und
  Erschließung ein Wohnungseingang; sonst bleibt die rohe Rolle.
- **Sie stehen nicht im Modell:** das ausgelieferte `tuer_detail` trägt die **rohe** Rolle.
  Damit liest ein zweiter Lauf dieselbe Eingabe und ist automatisch idempotent. Belegt über
  11 Pläne: die ausgelieferten `tuer_detail` sind zwischen zwei unabhängigen vollen Läufen
  feldgleich (90 186 Felder, 0 Abweichungen).
- **Wer sie liest:** nur `fluchtweg.py` — Segment-Starts (`fluchtweg.py:329`), die
  Durchleitung (`:247`, `durchleitung_raeume` `:755`) und die weichen Knoten (`:252`,
  `volle_knoten` `:739`). Sonst niemand.

**Durchleitung (Owner-Entscheid 2026-09-20, weiter gültig und jetzt gebaut).** Privat heißt
keine Notbeleuchtung und keine eigene Zirkulation — **kein Loch im Graph**: ein privat
gewordener Erschließungsraum bleibt Knoten für Wege zwischen zwei allgemeinen Räumen (nur
wenn das Raumpolygon die Strecke deckt), bekommt aber keine eigenen Stützpunkte, Anker oder
Leuchten. Ohne das zerreißen Wege — gemessen: Mollgasse 1OG STIEGENHAUS `raum_35` 10 → 2
Segmente, Rennweg UG KINDERWAGENRAUM verliert sein einziges, drei neue
`fluchtweg_warnungen` „kein final_exit erreichbar". Messfall (ii) (KINDERWAGENRAUM behält
seinen Weg) und (iii) (die drei Warnungen verschwinden) sind erfüllt und im Naht-Test
gebunden; Messfall (i) bleibt Charakterisierung für **S7c** (§ 6g.8); Messfall (iv)
Mollgasse 1OG `raum_34` entscheidet Schritt 2 mit **3 Wohnungen → ALLGEMEIN**, Flags 11.

**Board-Antrag weiter offen (blockiert den Slice nicht):** durchgeleitete Segmente sollen
`durchleitung=True` tragen. `FluchtwegSegment.quelle` ist
`Literal["LINIE", "GRAPH", "FALLBACK"] | None`; ein neuer Wert oder ein neues Feld ist eine
Contract-Änderung mit Approval aller drei Owner. Der Slice baut die **Wirkung** und weist die
Durchleitung als Prüfstrecken-Warnung aus (Muster `tuer_warnungen`, `provider.py:176-178`).

**Lesehilfe für Dumps** (hat in zwei Reviews Scheinabweichungen erzeugt): in den
Messdumps des Slices steht unter `tueren[…]["detail"]` die **ROHE** Rolle und unter
`korrigiert` die korrigierte — auf 628 Türen weichen 41 voneinander ab. Legt ein Werkzeug
unter `detail` die korrigierte Rolle ab, entstehen beim Quervergleich genau diese 41
Scheinabweichungen. Die Leuchten der Pipeline-Dumps stehen unter `raum.raeume`, nicht unter
`raeume`; ein Zugriff auf `raeume` liefert stillschweigend 0 Leuchten statt 7.

#### 6g.7 Messung und Abnahme auf dem sauberen Baum `e617fd1`

Grundlage: 12 Pläne einzeln geparst (7 Rennweg-Geschosse, Barawitzka EG, Dachdraufsicht,
Mollgasse EG und 1OG, Muthgasse E2), volle Pipeline auf 11 Plänen (Muthgasse ohne
Platzierung), Gate-Messung und Gate-Prüfung gegen `tests/gate/nullmessung_f15d03f.json`.
Zwei unabhängige volle Läufe stimmen in 9 863 Messschlüsseln und 90 186 Pipeline-Feldern
überein (0 Abweichungen), das Gate in allen Kennzahlen.

**Gate: 3 Verstöße, keiner neu.** Der Verstoß **(0)** („Nachher-Stand mit unsauberem
Arbeitsbaum unter `src/` oder `scripts/` gemessen") ist mit dem Commit weggefallen; die
Menge der Sachverstöße ist unverändert die des Stands R6:

```
(3) M4.einraum steigt in DG2: 0 → 1
(6) Rennweg OG3 ohne GRAPH-Segment: segmente_graph=0, erwartet: >= 1
(10) Barawitzka EG ABSTELLRAUM 1.98 m² ohne Verbindung: 0 Tür(en)
```

Alle drei sind **vorbestehend** (schon auf den Ständen R6 und R10–R14). Gegen den Stand R10
weichen genau vier Schlüssel ab, alle auf OG3 und alle durch R1 (`M4.OG3.einraum` 4 → 0,
`M4.OG3.wohnungen` 6 → 3, `og3.einraum_wohnungen` 4 → 0, `og3.wohnungen` 6 → 3); gegen R6
drei Schlüssel, keiner in die schlechtere Richtung.

**Notlicht-Verlierer (Flags 00): 9 Räume, 47,71 m²** — je Raum sind alle vier Bedingungen
aus § 6g.4 ausgewiesen:

| Plan | Raum | Typ | m² | Anker roh privat über | Aufenthaltsraum in der (b)-Wohnung |
|---|---|---|---|---|---|
| OG1 | `raum_4` | VORRAUM | 3,40 | `tuer_3` mit Blatt | `top_1`: `raum_1`/`2`/`3` ZIMMER |
| OG1 | `raum_5` | VORRAUM | 2,59 | `tuer_3` | `top_1` |
| OG1 | `raum_8` | GANG | 6,48 | `tuer_3` | `top_1` |
| MOLL_1OG | `raum_2` | VORRAUM | 7,07 | `tuer_3` | `top_1`: `raum_1`/`36` KÜCHE, `raum_6`/`10`/`30`/`31`/`90` ZIMMER |
| MOLL_1OG | `raum_4` | VORRAUM | 6,45 | `tuer_4` | `top_1` |
| MOLL_1OG | `raum_5` | GANG | 4,73 | `tuer_4` | `top_1` |
| MOLL_1OG | `raum_37` | VORRAUM | 7,18 | `tuer_44` | `top_14`: `raum_87` ZIMMER |
| MOLL_1OG | `raum_42` | GANG | 5,69 | `tuer_44` | `top_15`: `raum_38`/`41`/`85` ZIMMER |
| MOLL_1OG | `raum_63` | VORRAUM | 4,12 | `tuer_49` | `top_16`: `raum_43` ZIMMER, `raum_61` KÜCHE |

Kein Riegel bei einem der neun. Gegenüber dem früheren Stand mit 13 Verlierern sind DG2
`raum_1`, MOLL_1OG `raum_69`, MOLL_1OG `raum_72` und OG1 `raum_12` **weggefallen**; neu ist
keiner.

**Ankerprivat und trotzdem alles behalten: 9 Räume**, je mit Grund — das ist die
Gegenrichtung derselben Regel und der Beleg, dass die Verengung aus § 6g.4 wirkt:

| Plan | Raum | Typ | m² | Klasse | Grund, warum nichts entzogen wird |
|---|---|---|---|---|---|
| UG | `raum_6` | VORRAUM | 4,77 | `WOHNUNG_PRIVAT` | G4: kein Aufenthaltsraum in `top_4` |
| OG1 | `raum_12` | VORRAUM | 10,94 | `WOHNUNG_PRIVAT` | G4 (`top_2`; der Raum trägt einen Wohnküchen-Stempel, siehe § 6g.8) |
| MOLL_1OG | `raum_16` | VORRAUM | 3,96 | `WOHNUNG_PRIVAT` | G4 (`top_5`) |
| MOLL_1OG | `raum_19` | VORRAUM | 8,21 | `WOHNUNG_PRIVAT` | G4 (`top_7`) |
| MOLL_1OG | `raum_26` | VORRAUM | 6,88 | `WOHNUNG_PRIVAT` | G4 (`top_12`) |
| MOLL_1OG | `raum_69` | VORRAUM | 4,66 | `WOHNUNG_PRIVAT` | G4 (`top_28`) |
| MOLL_1OG | `raum_72` | VORRAUM | 5,06 | `WOHNUNG_PRIVAT` | G4 (`top_30`) |
| MOLL_EG | `raum_34` | GANG | 6,92 | `ALLGEMEIN_ERSCHLIESSUNG` | Riegel G3: Tür ins Freie `tuer_16` → nie privat |
| MOLL_EG | `raum_57` | VORRAUM | 7,78 | `ALLGEMEIN_ERSCHLIESSUNG` | Tiebreak (§ 6g.3), kein voll ankerbestätigter Fixpunkt |

Alle neun tragen Flags 11. `raum_69` und `raum_72` sind nach der Owner-Lesart aus § 6g.4
„bestätigt" und fallen **allein über G4** aus der Code-Menge — das ist der Fall, an dem das
doppelt belegte Wort hängt.

**Einraum-Abnahme nach R3** („keine Einraum-Wohnung, die HEAD nicht hatte — außer den
benannten; weniger als HEAD ist erlaubt, wenn die Ursache aus rohen Türen belegt ist"):
erfüllt, **genau die vier zugelassenen Neuzugänge**, kein fünfter.

| Plan | Einraum HEAD → jetzt | neu gegenüber HEAD | weg gegenüber HEAD |
|---|---|---|---|
| UG | 4 → 3 | – | `raum_7` |
| EG | 1 → 1 | – | – |
| OG1 | 3 → 1 | – | `raum_11`, `raum_13` |
| OG2 / OG3 / DG1 / DD | 0 → 0 | – | – |
| DG2 | 1 → 1 | – | – |
| BARA | 8 → 6 | – | `raum_40`, `raum_5` |
| MOLL_EG | 15 → 15 | `raum_18` ZIMMER, `raum_20` ZIMMER | `raum_24`, `raum_26` |
| MOLL_1OG | 26 → 19 | `raum_16` VORRAUM, `raum_69` VORRAUM | `raum_12`, `raum_20`, `raum_21`, `raum_28`, `raum_29`, `raum_62`, `raum_73`, `raum_82`, `raum_86` |
| MUTH_E2 | 15 → 13 | – | `raum_45`, `raum_89` |

**Keine neue Wohnung ohne Eingang gegenüber HEAD: 12/12** (0 Zeilen „neu gegenüber HEAD").
Rennweg OG3 hat wie HEAD 3 eingangslose Wohnungen von 3, alle drei raummengengleich, und ist
**seit `b77cadf` auch im Test gebunden** (`test_jede_wohnung_hat_einen_wohnungseingang[og3]`
mit `VORBESTEHEND_OHNE_EINGANG["og3"]`). Einschränkung, damit eine spätere Runde daraus keine
Deckung liest, die es nicht gibt: **für OG3 ist die Eingangs-Hälfte der Zusicherung inert** —
alle drei Wohnungen stehen in der Ausnahmeliste, geprüft wird dort nur die Mengenidentität
der eingangslosen Wohnungen.

**Anker in `WOHNUNG_PRIVAT`** (geometrische Zählweise von `tests/gate/gate_og3.py`), je
Plan: DG1 **2** (`raum_4_ende_7`, `raum_4_tuer_5`, beide HEAD-vorbestehend), MOLL_EG **1**
(`raum_51_tuer_durchgang_25`, HEAD-vorbestehend), **alle übrigen 0** — insbesondere OG3 0
(damit ist der Anker-Teil der Gate-Bedingung (6) erfüllt, und der strict-xfail-Marker von
`tests/naht/test_soll_rennweg.py::test_keine_anker_in_wohnung_privat` ist in `6515689`
entfernt) und Mollgasse 1OG 0 (§ 6g.9). Anker gesamt, Ausgänge und Segmente je Quelle sind
auf 12/12 gleich HEAD, bis auf die Messfall-(i)-Segmente. Fußnote zur Ankerzahl: die
Kopfzahl zählt **nach** dem Liftschacht-Filter (`provider.py:230-235`); vier Pläne haben
davor je einen Anker mehr — UG 20/21, OG3 17/18, DG1 15/16, MOLL_EG 144/145.

**Was der Slice nicht erreicht:** über 11 Pläne stehen noch **7 Leuchten in 5 Räumen der
Klasse `WOHNUNG_PRIVAT`** (HEAD 19 → 7), alle in Räumen mit Flags 00, vier davon von diesem
Slice selbst entzogen: OG1 `raum_8` 2 SL, OG3 `raum_4` 1 SL (ZIMMER, HEAD-gleich), MOLL_EG
`raum_18` 2 RZ, MOLL_1OG `raum_42` 1 SL, MOLL_1OG `raum_5` 1 SL. Ursache liegt in
`platzierung/deckung.py` — das Package liest die Flags nicht (Board 1, § 6g.8). Zwei der
vier roten `tests/naht`-Meldungen hängen daran; die Mollgasse-Fälle sind heute **nicht**
vom Test gefangen, weil eine Parametrisierung auf Mollgasse drei neue Rotmeldungen erzeugen
würde.

#### 6g.8 Verbliebene Gate-Verstöße, Slice-Zuordnung und Merge-Reife

| # | Ursache (gemessen) | Zuordnung |
|---|---|---|
| **(6)** | Rennweg OG3 `segmente_graph = 0` — Fluchtweg-Graph, nicht Klassifikation. Der Anker-Teil derselben Bedingung ist erfüllt (0 Anker in `WOHNUNG_PRIVAT` auf OG3) | **S7c** (Rolle wandert nach außen) und **S3b** (Restflächen enden vor den Blocktüren; auf OG3 ist das Stiegenhaus `rest_3`/`rest_4`, keine Tür erreicht es, § 6c) |
| **(10)** | Barawitzka EG ABSTELLRAUM 1,98 m² ohne Verbindung, `raum_28` — Türerkennung | **S4c** |
| **(3)** | `M4.einraum` DG2 0 → 1: `raum_5` ZIMMER bildet die Einraum-Wohnung `top_2`, weil VORRAUM `raum_7` Erschließung ist und `raum_5` nur über `tuer_1` an ihm hängt; die Wohnungsgrenze (b) fällt damit auf `tuer_1` | **offen** — keine S7-Regel heilt sie |

Zu **(3)** im Einzelnen, weil die Zuordnung eine Entscheidung braucht: der Verstoß ist
gegenüber der Nullmessung `f15d03f` entstanden, aber **vorbestehend gegenüber HEAD
`5ac3e0f`** (DG2 Einraum = 1 auf HEAD, R6, R10 und jetzt). Die Wurzel ist dieselbe wie bei
R1 und Regel 5: eine **rohe** Rolle `wohnungseingang`, die kein physischer Beleg ist. Auf
DG2 tragen `durchgang_3`–`durchgang_6` zwischen den VORRÄUMEN `raum_6`/`raum_7` und den
Stiegenhäusern `rest_1`/`rest_3`/`rest_4` die Rolle `wohnungseingang`, sind aber **blattlose
Durchgänge** (1 263–5 379 mm) — nach E1 schließt eine blattlose Öffnung keine Wohnung ab,
die Flut geht durch, `raum_7` ist Erschließung, und `raum_5` bleibt allein.

**Planer-Einordnung 2026-09-25 (nach der Messung des Reviewers):** **S4e scheidet aus** —
die Rolle sitzt hier nicht auf einer Regel-5-Tür (GANG × privater Raum), sondern auf
blattlosen Durchgängen an VORRÄUMEN; die S4e-Ausgangsmessung zählt auf DG2 **0/0**
Regel-5-Türen. Die Wurzel ist die **Blatt-Semantik**: eine blattlose Öffnung trägt die
Rolle `wohnungseingang`, schließt aber nach E1 keine Wohnung ab. Kandidaten für die Heilung
sind daher **Board 3 (Blatt-Semantik, @EnisAMG)** und **S5c** (die blattlosen Öffnungen);
`tuer_1` selbst ist roh `zimmertuer`, an ihr ist nichts zu heilen. Alternative bleibt eine
benannte Owner-Ausnahme für DG2. **Keine neue S7-Regel** — der Wert ist gegenüber HEAD
unverändert.

**Was bis zur Merge-Reife des Stapels noch fehlt** (der Stapel wird nur gemeinsam gemergt,
§ 1 dieser Datei):

- **S7c** — Messfall (i): die Rolle `wohnungseingang` muss an die **äußere** Tür wandern
  (Vorraum → Stiegenhaus bzw. → allgemeiner Gang). Abnahme, damit sie nicht verloren geht:
  Mollgasse 1OG `raum_35` Start/Ziel-Segmente wieder 17, Rennweg OG1 `raum_14` wieder 4 an
  `rest_2`, die acht Wege über das Stiegenhaus wieder da — mit der Stiegenhaustür als Start.
  Solange S7c fehlt, führt `tests/naht` beide Werte als **Charakterisierung** (kein xfail,
  nicht grün gebogen); OG1 liegt bereits wieder auf den HEAD-Werten.
- **S4e** (Owner R5) — Regel 5 der Türtypisierung einschränken: eine Tür GANG → privater
  Raum wird nur dann roh zum Wohnungseingang, wenn der Gang selbst allgemein erschlossen
  ist, also vom Stiegenhaus ohne Wohnungseingang erreichbar. Ausgangsmessung liegt vor:
  **70 Regel-5-Türen, davon 46 S4e-Kandidaten** über 12 Pläne — UG 2/0 · EG 0/0 · OG1 2/2 ·
  OG2 2/2 · OG3 4/4 · DG1 4/4 · DG2 0/0 · DD 0/0 · BARA 0/0 · MOLL_EG 27/13 ·
  MOLL_1OG 16/13 · MUTH_E2 13/8. Größte Nester: MUTH `raum_94` 6 · OG2 `raum_9` 6 ·
  MOLL_1OG `raum_42` 5. Blast Radius über alle 12 Pläne ist Teil von S4e.
- **S4c** — heilt Gate (10) (Barawitzka `raum_28`).
- **S3b** — heilt die andere Hälfte von Gate (6) (OG3 `segmente_graph = 0`).
- **S5c** — die blattlosen Öffnungen, auf denen S7a überwiegend steht (F10; 12 der 14
  Stiegenhaustüren der Kipp-Räume sind Durchgänge, § 6c).
- **Board 1 an @mvpo3 (Leonis):** `platzierung/deckung.py` liest die Flags nicht. Einzelliste
  der 5 Räume / 7 Leuchten in § 6g.7. Nichts davon liegt in diesem Slice — fremdes Package.
- **Board-Punkt an @EnisAMG (Enis): WOHNKÜCHE in den Kanon.** Größenordnung gemessen:
  **28 Räume auf 7 von 12 Plänen** (24 heute KÜCHE, 3 untypisiert, 1 GANG) plus 6 Randlagen.
  **Die 28 sind eine UNTERGRENZE** — beide Messungen suchen denselben Stamm „Wohnk…";
  Stempel wie „WoKue" oder „W-Küche" fände keine von beiden. Die Folgen hängen an zwei
  Entscheidungen (wo der Eintrag greift, ob `nutzungsklasse._MAP` mitgeführt wird): heute
  gewinnt bei einem Eintrag **hinter** `classify_room` weiter der Kompositum-Kopf „…küche"
  → KÜCHE, es ändert sich nichts. Notlicht kostet nur der Eintrag, der auch die umlautlose
  Stempelschreibweise `Wohnkche` abdeckt (Rennweg OG1 `raum_10`, 73,06 m² → `raum_12`
  verliert sein Notlicht); die vom Owner gemeinte Hypothese („die Stempelräume bekommen den
  Typ") kostet **2 Räume / 88,01 m²** — OG1 `raum_12` (10,94 m²) und MOLL_EG `raum_41`
  (77,07 m², Raum des `final_exit` `exit_4`, 7 Leuchten). Bis zur Entscheidung ist WOHNKÜCHE
  **kein** Aufenthaltsraum: fail-safe, das Notlicht bleibt.
- **KINDERZIMMER** (Owner R4): steht im Kanon und **wird** Aufenthaltsraum — als eigener
  Slice **nach** dem Stapel, nicht hier. Auf den 12 Plänen heute 0 Fälle, Wirkung 0; der
  Kommentar über `AUFENTHALTSRAUM` (`wohnungsklasse.py:100-106`) zeigt darauf.
- Die **8 strict-xfail-Marker** in `test_soll_rennweg.py`/`test_soll_muthgasse.py` müssen
  vor dem Merge XPASS drehen; die 4 roten `tests/naht`-Meldungen müssen weg sein (2 davon
  Board 1, 1 S5b-Türblöcke Muthgasse, 1 dieselbe Leuchte wie eine der beiden).

#### 6g.9 Planer-Entscheid 2026-09-25 zu P2 — Weg (ii), der Guard bleibt unverändert

`anker_aus_privat_ziehen` (`wohnungsklasse.py:792`, gerufen in `provider.py:229`) zieht
Türanker des Stiegenhauses, die geometrisch in einen privat gewordenen Nachbarraum fallen,
auf die Seite ihres **eigenen** Raums — es streicht sie nicht. Planer-Korrektur **P2** wollte
die Sperrmenge dieser Funktion von „Klasse `WOHNUNG_PRIVAT`" auf „`bestaetigt_privat`"
umstellen, und der Planer-Entscheid dazu (Weg (i)) sah vor, den Naht-Guard
`test_keine_anker_wo_das_notlicht_entzogen_wurde` umzuschreiben und P2 zu bauen.

**Dieser Entscheid ist am 2026-09-25 ZURÜCKGENOMMEN. Es gilt Weg (ii): P2 ist nicht gebaut,
der Guard bleibt in beiden Zusicherungen wörtlich unverändert.** Begründung, in der Form, in
der die Urteile sie gemessen haben:

1. **Die vorgeschlagene neue Guard-Fassung wäre eine Tautologie.** „Fremde Anker in einem
   *bestätigt* privaten Raum" ist eine echte **Teilmenge** der ersten Zusicherung desselben
   Tests (alle Anker in `bestaetigt_privat` — nicht nur die fremden) und kann deshalb nie
   fallen, solange die erste grün ist. Das gilt **per Konstruktion**, weil
   `bestaetigt_privat` strukturell in GANG/VORRAUM liegt (§ 6g.4), und ist zusätzlich
   gemessen: auf 6/6 geprüften Plänen ist die neue Fassung in **beiden** Ständen 0 — auch auf
   Mollgasse 1OG, wo die heutige Fassung mit P2 von 0 auf 2 geht.
2. **Netto wäre der Umbau der Wegfall des einzigen Bandes über die 8 unbestätigt privaten
   Räume** (UG `raum_6`, OG1 `raum_12`, DG1 `raum_8`, MOLL_1OG `raum_16`/`19`/`26`/`69`/
   `72`). Das übrige Deckungsinventar ist OG3-gebunden, und OG3 hat `bestaetigt_privat` und
   `unbestaetigt_privat` **leer** — dort ist der Stand mit und ohne P2 in allen Zählweisen
   gleich.
3. **Die Begründung des Entscheids trägt nicht: `anker_aus_privat_ziehen` entzieht nichts.**
   Die Anker gehören dem STIEGENHAUS (`raum_64` auf Mollgasse 1OG); MOLL_1OG `raum_69` und
   `raum_72` haben keine eigenen Anker, behalten in beiden Lesarten Flags 11, ihre
   Zirkulation und ihre Leuchten, und die Ankerzahl ist in beiden Ständen 47. Der
   Owner-Grundsatz zum Entzug entscheidet diesen Fall also nicht. **Was P2 messbar ändert,
   ist allein die Abnahmezahl des Slices:** „Anker in `WOHNUNG_PRIVAT`" (geometrische
   Zählweise `tests/gate/gate_og3.py`) steigt auf Mollgasse 1OG von **0 auf 2**. Ein
   schlechterer Ist-Wert ohne Gegenleistung ist keine zulässige Richtung.

Zusätzlich gemessen: P2 macht **vier** Zusicherungen in **zwei** Dateien rot (drei
Unit-Zusicherungen im Abschnitt „(j) B2" von `tests/raumerkennung/test_wohnungsklasse.py` —
eine davon, `test_fremder_anker_wird_auch_aus_unbestaetigt_privatem_raum_gezogen`, sagt die
Gegenthese im Namen — und `test_keine_anker_wo_das_notlicht_entzogen_wurde[1OG_MOLL]` in
`tests/naht/test_s7_wohnungsklasse.py`). P2 ist also **nutzlos, nicht schädlich**: auf
12/12 Plänen gewinnt kein Raum einen Anker, eine Zirkulation, ein Notlicht oder eine
Leuchte. Und nach der Owner-Lesart aus § 6g.4 („bestätigt = Klasse PRIVAT ∧ Ankerregel roh
PRIVAT") wäre die neu gefasste Zusicherung mit P2 **selbst rot**, weil `raum_69`/`raum_72`
nach diesem Wortlaut bestätigt privat sind (§ 6g.7).

**Ausdrücklich festgehalten, damit die Gegenmeinung nicht verloren geht:** die Review-Linse
*Regel* hat empfohlen, **P2 zu bauen, aber mit einer anderen Guard-Fassung** („die Sache
selbst ist richtig und kostet nachweislich nichts — nur die Fassung des Guards ist falsch";
Vorschlag: die zweite Zusicherung behalten und die zwei Anker als benannte Ausnahme
abziehen). Diese Linse hat ihre Korrektur in der Folgerunde selbst zurückgezogen, weil sie
nur **eine von vier** Zusicherungen geheilt hätte. Soll P2 später doch kommen, darf die
zweite Zusicherung nicht durch eine Teilmenge der ersten ersetzt werden, sondern nur durch
eine Zusicherung mit eigenem Inhalt (etwa ein gemessenes Höchstband „Anker in
`WOHNUNG_PRIVAT`, geometrische Gate-Zählweise, je Plan ≤ heutiger Wert" über alle 12 Pläne)
— und die drei B2-Unit-Zusicherungen müssen ausdrücklich mitentschieden werden.

---

## 7. Diagnose S3b — Restflächen enden vor den Blocktüren (Owner-Definition, kein Code)

**Namenskollision:** Das „S3b" der Diagnose (`34b5dd0`, türloser Kleinrest vor
Treppenmarker, U2/Liftringe) ist etwas anderes; für diesen Punkt sollte der Owner ein
eigenes Kürzel vergeben. Gemessen am 2026-09-19 auf `1e5e5ac` über alle 10 Prüfpläne
(In-Memory, kein Output; dazu ein Stufenlauf OG3 `lade_dxf → raeume_aus_kaskade →
typisiere_geometrisch → finde_lifte → parse`).

### 7a. Codestellen

- **Versiegelung in der Restflächen-Stufe:** `rest_komponenten.py:176-184` (aus
  `kaskade.py:178`): je Türöffnung eine Scheibe mit Radius
  `max(1, round(max(600, breite_mm)/50)) · 50 mm` — **850 mm** für 840-mm-, **950 mm** für
  940-mm-Türen, 600 mm ohne Breite. Weitere Schrumpfquellen: `:160` Außenkontur 1000 mm,
  `:185-190` belegte Raumpolygone + 100 mm, `:199/202` alles < 1 m² entfällt.
- **Erosion/Rückdehnung:** Raster 50 mm (`rest_komponenten.py:148`,
  `stempel_flutung.py:232`). Die **Flutungsstufe** versiegelt in Stufen 600/900/1200/1500 mm
  (`stempel_flutung.py:124-136`) und **dehnt zurück** (`:174-193`, geodätischer Watershed +
  Lochfüllung). **Genau diese Rückdehnung fehlt in `rest_komponenten.komponenten_ohne_stempel`**
  — die erodierte Maske wird direkt gelabelt (`:195`) und vektorisiert.
- **Vektorisierung:** `stempel_flutung._vektorisiere` (`:202-219`), größte Kontur,
  `simplify(25 mm)`, `snap(…, wand_union.boundary, 50 mm)` — der Snap schließt 850–950 mm
  nicht. Kein nachträglicher Puffer.
- **Sichtbar** in `tuer_zuordnung.ordne_tueren` (Probe 100/200/300/500 mm, `_seite`
  Z. 105-134): Raum 850 mm entfernt → `KEIN_RAUM` → `seite_fehlt` (`provider.py:154-157`).

### 7b. Messung: Abstand Probepunkt (Sehnenmitte ± 100 mm) → nächstes Raumpolygon, Blocktüren

| Plan | Blocktüren | Seiten | min | median | max | Seiten > 250 mm | beide ≤ 250 | davon 2 versch. Räume | seite_fehlt |
|---|---|---|---|---|---|---|---|---|---|
| Rennweg UG | 15 | 30 | 0 | 20,0 | 318,8 | 1 | 14 | 13 | 0 |
| Rennweg EG | 6 | 12 | 0 | 0 | 124,3 | 0 | 6 | 3 | 2 |
| Rennweg OG1 | 9 | 18 | 0 | 0 | 80,0 | 0 | 9 | 8 | 0 |
| Rennweg OG2 | 9 | 18 | 0 | 0 | 80,0 | 0 | 9 | 8 | 1 |
| Rennweg OG3 | 11 | 22 | 0 | 20,5 | 866,6 | 3 | 8 | 4 | 7 |
| Rennweg DG1 | 5 | 10 | 0 | 0 | 20,0 | 0 | 5 | 5 | 0 |
| Rennweg DG2 | 4 | 8 | 0 | 10,0 | 20,8 | 0 | 4 | 4 | 0 |
| Barawitzka EG | 0 | — | — | — | — | — | — | — | — |
| Mollgasse EG | 43 | 86 | 0 | 0 | 107,7 | 0 | 43 | 35 | 8 |
| Muthgasse E2 | 15 | 30 | 0 | 0 | 879,3 | 2 | 13 | 10 | 2 |
| **Summe** | **117** | | | | | | **111 (95 %)** | **90 (77 %)** | |

Barawitzka EG hat keine Blocktür (alle 99 Türen aus Bögen, Durchgängen, Texten) — ein Gate
über Blocktüren ist dort leer. **Offen:** meint „beidseits ein Raum ≤ 250 mm" zwei
**verschiedene** Räume (90/117) oder genügt derselbe (111/117; bei 21 Türen ragt ein
gestempeltes Polygon durch die Öffnung, `_seite` schließt den eigenen Raum bewusst aus)?

Die 6 Blocktüren mit einer Seite > 250 mm: OG3 `tuer_6` (867/814 mm zu `rest_3`/`rest_4`),
`tuer_12` (854/813 mm zu `rest_4`/`rest_3`), `tuer_9` (656/660 mm zu WC `raum_8`; gemeinte
Nachbarn `rest_5`/`rest_6` bei 811/839 mm); Muthgasse `tuer_20` (850/879 mm, Breite None)
und `tuer_21` (325 mm, Breite None); Rennweg UG `tuer_7` (319 mm zu GANG 5,35). OG3
`seite_fehlt`: 13 Seiten = 7 Blocktüren (`tuer_4/5/6/8/9/10/12`, 10 Seiten) + 2 Bogentüren
(`tuer_2/3`, 3 Seiten); die nächste REST-Komponente beginnt je 810–968 mm entfernt
(`rest_3` STIEGENHAUS: 905/917/926/938 mm zu `tuer_12/4/5/6`; `rest_4`: 906/946/968 mm;
`rest_5` SCHACHT: 811/823/831 mm; `rest_6`: 826/839/945 mm). `rest_3` misst nach
`raeume_aus_kaskade` 4,68 m² und im Endmodell 2,94 m² — die Differenz ist die
LIFT_SCHACHT-Stanzung in `finde_lifte` (`lift_erkennung.py:195-212`, `lift_1` 1,73 m²),
die Türabstände sind auf allen Stufen bitgleich.

**Abstand der REST-Konturen zur Wand, getrennt nach „≤ 1,5 m von einer Blocktür" / „sonst"**
(OG3): `rest_4` an Türen median 33 / max 618 mm, sonst median 6,6 / max 38,7 mm; `rest_3`
an Türen median 300 / max 906 mm, sonst median 35 / max 300 mm; `rest_6` an Türen median
82 / max 831 mm, sonst median 16 / max 49 mm; `rest_1`/`rest_2` (keine Blocktür in
Siegelreichweite) überall 0 mm. **Die Lücke sitzt nur an den Türen.**

### 7c. Hypothesenprüfung

Vorhersage: der Rand einer REST-Komponente liegt genau `r = max(1, round(max(600,
Breite)/50)) · 50 mm` vom Türmittelpunkt, weil der Kreisstempel nie zurückgedehnt wird.
Über **79 Paare** REST-Raum × Blocktür ≤ 3 m aus 9 Plänen unterschreitet **kein einziges**
den Siegelradius um mehr als 44,7 mm (< 1 Rasterzelle; dazu `simplify(25)` und Snap 50 mm);
die 18 Paare, bei denen die Tür wirklich an der Komponente liegt, streuen um −9,9 mm
(−44,7 … +95,3 mm) um den vorhergesagten Radius; Probepunkt 950 − 100 = 850 mm erwartet,
gemessen 814/814/854/867 mm an `tuer_6`/`tuer_12`. **Die Owner-Hypothese ist gestützt.**
Ausgeschlossen: „Wandkörper-Union deckt die Fläche" (abseits der Türen 0–39 mm an der
Wand); `bereinigung` Regel 2 (greift auf OG3 nicht, Liste leer); Lift-Stanzung (0,0 mm
Änderung der Türabstände). „Zonenlayer fehlt" erklärt, **warum** die Flächen REST sind,
nicht die Lücke — geflutete Räume desselben Plans liegen 0–80 mm an den Türen, weil die
Flutung zurückdehnt. **Nicht erklärt** (eigene Ursachen): Muthgasse `tuer_20`/`tuer_21`
(0 REST-Räume, Breite None, Flanke→Raum 626/886 mm quer zur Vorhersage) und Rennweg UG
`tuer_7` (319 mm, knapp über der Schwelle).

### 7d. Risiken und offene Entscheidungen

- Ursache sitzt in `rest_komponenten.komponenten_ohne_stempel`, nicht in der Türlogik. Eine
  Rückdehnung analog `stempel_flutung.py:174-193` vergrößert alle REST-Polygone — berührt
  `bereinigung` Regel 1/2, die LIFT_SCHACHT-Stanzung, `_MIN_M2`, die `rest_N`-Nummerierung
  und die SCHACHT-/GANG-Typregeln (`rest_komponenten._typisiere`, `tuer_n` im 600-mm-Rand);
  OG3 `rest_1`/`rest_2` (1,16/1,15 m²) stehen 0,15 m² über der Entfallschwelle.
- Der Siegelradius hängt an `max(600, Türbreite)`; bei ArchiCAD-Blöcken ist die Breite der
  Blattradius 840/940 mm (F18) — eine Antwort auf F18 verschiebt die Lücke direkt.
- Zählweise des Ziels „beidseits ein Raum innerhalb 250 mm" (77 % oder 95 % heute) ist offen;
  Barawitzka liefert keinen Messwert.
