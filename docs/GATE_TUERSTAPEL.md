# Merge-Gate des Türstapels S4a → S4b → S5b → S4c → S7a+S7b → S3b → S5c

Stand: 2026-09-20 (Nachträge: Lesart B zu M17-04-c 2026-09-18; Stapel-Erweiterung, Bedingungen
(7)/(8) und Diagnose S7a/S3b 2026-09-19; Reihenfolge, S7a+S7b, Bedingung (9) und Folgeauftrag
S-KG 2026-09-20; Bedingung (10) Barawitzka, Entscheide zu § 8a und § 8b 2026-09-20) ·
Owner: Selman (`src/notbeleuchtung/raumerkennung/`) ·
Branch `selman/uebernahme-enis-m17` · Nullmessung auf Code-Stand `f15d03f` (Tranche 1)

**Reihenfolge seit 2026-09-20 (Owner-Ansage, verbindlich, nichts parallel):** S5b → **S4c** →
S7a+S7b (= Leonis' Paket S-W „Wohnung ≠ Fluchtweg", § 6f) → S3b → S5c → Gate → Merge des
Stapels → danach S-KG (Kellergeschosse und Garage) als eigenes Paket (§ 5a) und S-MST
(Maßstab-Kontrolle, `docs/OFFENE_FRAGEN.md`). Regeln unverändert: nur `raumerkennung/`, kein
Owner-Package importieren, Contract nur über das Board, ein Slice ein Commit, kein Merge vor
dem Gate.

**S4c** ist der S4a-Rest: die Doppelflügel-Fehlpaarung, die auf Barawitzka EG die echte Tür des
ABSTELLRAUMS 1,98 m² verschluckt (§ 1f). Der Slice kam am 2026-09-20 in den Stapel, weil der
Owner die zugehörige Bedingung **(10) als Merge-Pflicht** entschieden hat — ohne S4c ist das
Gate nicht erfüllbar.

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

### 1f. Barawitzka EG — ABSTELLRAUM 1,98 m² (`tests/gate/gate_barawitzka.py`, seit 2026-09-20)

Der einzige Messfall außerhalb der Rennweg-Familie (Owner-Entscheid 2026-09-20, Bedingung
(10)). Von den acht Räumen, die S5b auf 0 Verbindungen fallen lässt (§ 8e), ist dies der
einzige mit einer **echten Tür ohne Ersatz**: die 830er Bogenöffnung hat keine eigene Tür,
sie steckt als Fehlpaarung zweier Einzeltüren im „doppelfluegel" 1660 mm (S4a-Rest). Gemessen
auf dem versionierten Plan `Projekte/Barawitzkagasse/…EG.dxf`, floor `EG` — derselbe Plan und
derselbe Weg über `tests/plaene.py`, den `tests/naht/test_soll_barawitzka.py` nimmt.

Gezählt werden die Türen, die den Raum als `von_raum` oder `nach_raum` führen; daneben stehen
als Messwerte die nächste erkannte Tür überhaupt (id, quelle, Breite, Abstand zum Raumpolygon)
und die „doppelfluegel"-Türen innerhalb von 2 m. Der Raum wird wie in § 1e über `raum_typ` +
Fläche (± 0,05 m²) aufgelöst, nicht über die ID; passt kein oder mehr als ein Raum, ist der
Fall nicht messbar (`anzahl` None mit Grund). **Ist 2026-09-20 auf `826b157`:** `raum_28`,
**0 Verbindungen**, nächste Tür `tuer_38` (quelle `doppelfluegel`, 1660 mm) 967,1 mm entfernt
— die Bedingung ist heute verletzt und dreht erst mit dem S4a-Rest.

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
| (10) | Barawitzka EG: der ABSTELLRAUM 1,98 m² hat mindestens eine Verbindung | `barawitzka.anzahl ≥ 1` (§ 1f, `tests/gate/gate_barawitzka.py`); `anzahl` None oder fehlender Abschnitt = Verstoß. Owner-Entscheid 2026-09-20 nach dem Blast Radius: **heute verletzt** (0 Verbindungen), zu drehen ist sie vom S4a-Rest (Doppelflügel-Paarung), nicht von S7 — festgehalten, damit sie nicht untergeht. Gemessen wird nur der Nachher-Stand; die eingecheckte Nullmessung stammt von vor dem Messfall und führt den Abschnitt nicht: als Vorher-Stand ist das kein Absturz, als Nachher-Stand ein Verstoß (fail closed) |

Zur Nummer: die Owner-Ansage vom 2026-09-20 nennt die Mollgasse-Abnahme „Bedingung (7)".
(7) und (8) sind seit `dd3cfdc` mit den Referenz-Verbindungen belegt; die Mollgasse-Abnahme
läuft deshalb als **(9)**, damit keine bestehende Nummer ihre Bedeutung wechselt. (5) bleibt
daneben Abnahme von S7a+S7b (Einraum-Wohnungen auf OG1 sinken).

Zwischenstände der einzelnen Slices werden gemessen und berichtet (`python
tests/gate/gate_messung.py --out <datei.json>`, dann `pruefe_gate`), aber **nicht
gemergt** — auch nicht bei Verbesserung. (5) und (6) bleiben Merge-Pflicht, obwohl der
Türstapel im engen Sinn sie nicht heilen kann — dafür stehen S7a und S3b im Stapel.

Heute liefert `pruefe_gate(nullmessung, nullmessung)` genau zehn Verstöße:
`(2) M17-02-b ist NICHT_BESTANDEN`, `(2) M17-04-c ist NICHT_BESTANDEN`,
`(5) Einraum-Wohnungen sinken nicht: 2 → 2`, sechs Verstöße gegen (7) — die sechs
bestehenden verneinten Verbindungen aus § 2e (zusammen 8 Durchgänge) — und
`(10) Barawitzka EG nicht gemessen — Abschnitt »barawitzka« fehlt`, weil die Nullmessung
von vor diesem Messfall stammt und nicht neu geschrieben wird (neun waren es, bevor (10)
dazukam). (8) ist auf f15d03f erfüllt.

**Test:** `tests/gate/test_gate_tuerstapel.py::test_gate_tuerstapel_erfuellt` ist
`xfail(strict=True, raises=AssertionError)`. Er bleibt rot-per-Design (XFAIL), bis der
Stapel das Gate erfüllt; dann dreht er auf XPASS, der strenge Marker lässt die Suite
fehlschlagen, der Marker wird entfernt und der Stapel gemergt. Infrastrukturfehler
(Exception statt AssertionError) gehen nicht als XFAIL durch. Die Gate-Tests tragen den
Marker `gate` und sind — wie `visual` — in der normalen Suite deselektiert
(`pytest -m gate tests/gate`; mit dem Barawitzka-Messfall aus § 1f gemessen 2026-09-20:
47,2 s mit vorhandenen Caches, 86,2 s wenn die M1-M4-Caches erst gebaut werden — der
Barawitzka-Parse kostet davon 10,6 s). Ohne
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

### 6g. Das Verfahren für S7a+S7b (Owner-Entscheid 2026-09-20, verbindlich)

Die Regel aus § 6b ist **zirkulär**: „erschließt zwei Wohnungen" hängt davon ab, ob die
Nachbarn privat sind, was davon abhängt, ob dieser Gang allgemein ist. Die Messung vom
2026-09-20 hat gezeigt, wie teuer das ist — dieselbe Regel, zwei Zählbasen, gegensätzliche
Ergebnisse für ein ganzes Geschoss (Mollgasse 1OG `raum_34` GANG 16,99 m²: gegen die
verfeinerte Klasse 0 private Gruppen → privat, Segmente 22 → 3; gegen die statische Klasse
3 Gruppen → allgemein, Segmente 22 → 10). Der Owner löst das **zweistufig**:

1. **Anker zuerst, ohne Iteration.** Erreichbarkeit vom STIEGENHAUS über Türen: ein Raum, der
   nur über eine Wohnungseingangstür erreichbar ist, ist PRIVAT; ein Raum, der vom Stiegenhaus
   ohne Wohnungseingangstür erreichbar ist, ist ALLGEMEIN. Das ist Geometrie und Türtyp, **keine
   Raumklasse** — und damit reihenfolgeunabhängig. Schritt 1 liest keine `nutzungsklasse`.
2. **Zwei-Wohnungen-Regel nur auf die Räume, die Schritt 1 nicht entschieden hat**, auf der
   Basis von Schritt 1, iterativ bis zum Fixpunkt, **Deckel 10 Runden**.
3. **Unbestimmt statt Raten.** Oszilliert ein Raum nach Schritt 2, oder erreicht Schritt 1 ihn
   nicht, wird er als **unbestimmt** geführt — mit Grund, im Bericht aufgelistet, in der
   Darstellung magenta. Keine willkürliche Festlegung. Ohne Contract-Änderung möglich:
   `Raum.nutzungsklasse` ist `Nutzungsklasse | None` und der Contract nennt „None/leer =
   unbestimmt". **Aber** `wohnungen._klasse()` und `fluchtweg._klasse()` fallen bei `None`
   heute still auf `nutzungsklasse_fuer(raum_typ)` zurück und machen aus unbestimmt genau die
   willkürliche Festlegung — diese Stellen gehören zum Slice. Ein unbestimmter Raum wird
   konservativ behandelt: er verliert weder Leuchte noch Anker und reißt den Graph nicht auf.
4. **Test:** Ergebnis identisch bei umgekehrter Raum- **und** Türreihenfolge. Für Mollgasse 1OG
   `raum_34` ist im Bericht auszuweisen, welcher Schritt entschieden hat, über welche Tür, plus
   Segmente, Anker und Wohnungen.

**Durchleitung (Owner-Entscheid 2026-09-20).** Privat heißt **keine Notbeleuchtung und keine
eigene Zirkulation — kein Loch im Graph.** Eigene Regel in `fluchtweg.py`: ein privater Raum
bleibt Knoten für Wege zwischen zwei communalen Räumen, bekommt aber selbst keine
Segment-Stützpunkte, keine Anker, keine Leuchten. Grund ist eine gemessene Nebenwirkung: ohne
Durchleitung fällt ein kippender Vorraum als Knoten aus `fluchtweg.py` (`erschliessung`) und
zerreißt Wege zwischen zwei communalen Räumen — Mollgasse 1OG STIEGENHAUS `raum_35` 10 → 2
Segmente, Rennweg UG KINDERWAGENRAUM 21,49 m² verliert sein einziges, und die Engine meldet
drei neue `fluchtweg_warnungen` „kein final_exit erreichbar".

Vier Messfälle für die Abnahme: (i) Mollgasse 1OG STIEGENHAUS `raum_35` behält seine Segmente;
(ii) Rennweg UG KINDERWAGENRAUM behält seinen Weg; (iii) die drei neuen „kein final_exit
erreichbar" verschwinden; (iv) `raum_34` wie in Punkt 4.

**Board-Antrag (offen, blockiert den Slice nicht):** der Owner will durchgeleitete Segmente mit
`durchleitung=True` markiert sehen. `FluchtwegSegment.quelle` ist
`Literal["LINIE", "GRAPH", "FALLBACK"] | None`; ein neuer Wert oder ein neues Feld ist eine
Contract-Änderung mit Approval aller drei Owner und Schema-Regen. Der Slice baut deshalb die
**Wirkung** und weist die Durchleitung als Provider-Warnung aus (Muster `tuer_warnungen`); das
Feld wird über das Board beantragt.

**Nicht mehr gültig:** die Zahlen in § 6c stammen von Code-Stand `1e5e5ac`, also **vor** S5b.
S5b hat über die zehn Prüfpläne 204 Durchgänge entfernt (§ 8e); die Kipp-Mengen und
Wohnungszahlen haben sich dadurch verschoben. Vor dem Bau wurde am 2026-09-20 neu gemessen.

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

---

## 8. S5b — Messung, Korrektur, Blast Radius und offene Punkte (Stand 2026-09-20, Branch `selman/fix-s5b-querung`, Code `94b7480`)

S5b (Diagnose U13) gibt `durchgaenge_ohne_tuerblatt` ein Querungsprädikat: ein freier
Streifen ist nur dann ein Durchgang, wenn er **beide** Raumseiten erreicht; die Breite wird
entlang der gemeinsamen Grenze gemessen statt als Rechtecklänge des Streifens. § 8a und § 8b
waren die zwei Punkte, die vor den Merge auf den Tisch gehörten — beide sind seit dem
2026-09-20 entschieden (§ 8a übernommen, § 8b als strict-xfail markiert); § 8c bis § 8f tragen die
Korrektur vom 2026-09-20, die Gate-Messung, den Blast Radius über alle Familien und die
dabei gefundenen offenen Befunde nach.

### 8a. Kontaktgrenze — dieselbe Toleranz, angewandt auf das Band in der Wandmitte

**Entschieden (Owner, 2026-09-20): übernommen.** Maßgeblich sind die in § 4 festgelegten
Toleranzen des Gates — `KONTAKT_TOL_MM = 1,0` · `UEBERLAPPUNG_TOL_MM2 = 1,0` ·
`PORTAL_WAND_MM = 250,0`, gemessen auf der Quellpräzision im Speicher, nie auf exportierten
oder gerundeten Werten. § 8a stellt ihnen **keine zweite Zahl** daneben, sondern verweist auf
sie.

Gebaut ist `tuer_zuordnung._kontakt_grenze(abstand) = max(0, abstand − 250) + 1,0`. Beide
Konstanten darin sind die aus § 4: die 250 mm sind die halbe Wanddicke `PORTAL_WAND_MM`
(im Code `_KONTAKT_MM` — derselbe Radius, mit dem die Erkennung eine Tür einer Wand zuordnet
und mit dem das Gate zurückmisst), die 1,0 mm sind `KONTAKT_TOL_MM`. Die Kontaktzone ist
`pa.buffer(250) ∩ pb.buffer(250)`; bei Raumabstand *d* > 250 mm liegt sie als Band **in der
Wandmitte** und hat zu beiden Räumen den Abstand *d* − 250 (`zone.distance(pa) =
zone.distance(pb)`: 0 mm bei *d* = 100, 50 mm bei *d* = 300, 200 mm bei *d* = 450). Die
Grenze ist damit nichts anderes als **dieselbe 1-mm-Kontakttoleranz, angewandt auf dieses
Band** statt direkt auf das Raumpolygon: der freie Teil muss das Band bis auf `KONTAKT_TOL_MM`
durchspannen. Der Summand *d* − 250 ist keine Toleranz, sondern die Lage des Bandes.

Auf die Raumpolygone gerechnet wäre ein fester 1-mm-Wert ab Wänden über `PORTAL_WAND_MM` nie
erfüllbar und löschte jede Öffnung in einer dickeren Wand — am Rennweg OG1 die geforderten
Übergänge O01/O02 (VORRAUM 10,94 ↔ Wohnküche 73,06 m², *d* = 450 mm) und T08 (ZIMMER 10,59 ↔
BALKON 7,51 m², *d* = 400 mm) sowie drei Unit-Tests an einer 400-mm-Wand. Nach oben ist die
Grenze durch § 4 gedeckelt: die Zone ist leer, sobald *d* die doppelte halbe Wanddicke
erreicht (in der Praxis früher, § 8c K3) — ein freier Teil kann deshalb nie weiter von einem
Raum entfernt liegen als `PORTAL_WAND_MM` plus `KONTAKT_TOL_MM`, und das ist genau der
Radius, in dem das Gate selbst eine Tür noch „an der markierten Wand" zählt (§ 1a,
`direct_portal_in_probe_segment`).

Bis *d* = 250 mm gilt das Kriterium wörtlich (1 mm zum Raum), darüber lautet es „der Streifen
durchspannt das Band ganz" — dieselbe Aussage „die Querung führt nicht durch Wandkörper".
Die Zone bleibt unverändert bei `buffer(250)`; die Schlitz-/Asymmetrie-Varianten der
Diagnose sind **nicht** gebaut.

**Fachlicher Abgleich (Planer, 2026-09-20, gegen § 4 und `tests/gate/gate_m17.py`):** keine
Abweichung von den Gate-Toleranzen — es sind dieselben zwei Konstanten, auf derselben
Quellpräzision, nur auf die abgeleitete Geometrie (Band) statt auf das Raumpolygon angewandt,
und nach oben durch dieselben Konstanten gedeckelt. Eine Board-Frage entsteht daraus nicht.
Unberührt davon bleibt offen, **welcher** Abstand *d* in die Grenze geht (globaler
Paarabstand statt lokaler) — § 8f Punkt 1.

Den Nebeneffekt, den die Diagnose (`34b5dd0`, Cluster K5, Liste „Nicht übernehmen") dem
absoluten Filter vorhält — er löscht den echten Wohnungseingang OG1 `durchgang_22`, dessen
freier Teil je 100 mm von beiden Räumen liegt —, hat das Prädikat bei *d* ≤ 250 mm ebenso.
Die Stelle bleibt trotzdem verbunden: seit S4a steht dort die Blocktür `tuer_3` (940 mm,
STIEGENHAUS 11,21 ↔ VORRAUM 10,94), und ein Durchgang daneben wäre seit S4b Dublette. Genau
dafür wird der Stapel nur gemeinsam gemessen und gemergt.

### 8b. Bekannter Stapelrest — drei rote Familien-Soll-Tests

Mit S5b fallen Durchgänge weg, die heute die **einzige** Modellvertretung einer echten Tür
sind. Drei Tests in `tests/naht` sind dadurch rot (vorbestehend rot bleiben
`test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell` und
`test_soll_rennweg.py::test_soll_keine_leuchten_in_wohnung_privat`):

| Test | Ist nach S5b | Ursache |
|---|---|---|
| `test_soll_barawitzka.py::test_soll_brandschutztuer` | 0 statt ≥ 1 | die `brandschutztuer` hing an `durchgang_8` (`rest_2` ↔ (leer) 31,25). Nachgemessen 2026-09-20: die Türen dort **sind** erkannt (Bogentüren `tuer_26` 900 und `tuer_12` 1003), ihnen fehlt die Raumseite — das REST-Polygon endet 858 / 981 mm vor ihnen → S3b an Bogentüren, nicht „kein erkannter Block" |
| `test_soll_rennweg.py::test_soll_stair_exit_statt_final_exit` (OG3) | 0 stair_exit | OG3-Restflächen enden 860–1000 mm vor den Blocktüren → S3b |
| `test_soll_rennweg.py::test_soll_tueren_mit_detail` (OG3) | 7 statt ≥ 11 | dieselbe Ursache; die Diagnose nennt „≥ 11 heute nur über Durchgänge grün" |

Gleiche Ursache ohne eigenen Test: Räume, die auf **0 Verbindungen** fallen — Liste je Raum
mit Befund und heilendem Slice in § 8e (Stand nach der Korrektur: acht Räume; die übrigen
sechs Rennweg-Geschosse verlieren keinen Raum ganz). Volle Suite auf `94b7480`: 5 failed
(diese drei und die zwei vorbestehenden), 1544 passed, 16 xfailed, kein XPASS.

**Entschieden (Owner, 2026-09-20):** nicht bewusst rot lassen, sondern markieren. Die drei
Tests tragen seither `@pytest.mark.xfail(strict=True, raises=AssertionError, reason="Türstapel
unvollständig (S7a/S7b/S3b ausstehend), muss vor Merge XPASS sein")` — dasselbe Muster wie
`test_soll_segmente_aus_graph`/`test_keine_anker_in_wohnung_privat` (Bedingung (6)). Weil der
Marker `strict` ist, müssen sie nach S7a/S7b/S3b auf XPASS drehen, sonst wird die Suite rot.
Geändert wurden **nur die Dekoratorzeilen**: Guard-Bänder, Fixtures und Testkörper bleiben
unverändert, abgesenkt wird nichts. Beleg 2026-09-20 auf `826b157`
(`pytest tests/naht/test_soll_rennweg.py tests/naht/test_soll_barawitzka.py`): `1 failed,
8 passed, 9 xfailed` — die drei laufen als XFAIL, der vorbestehend rote
`test_soll_keine_leuchten_in_wohnung_privat` bleibt rot.

### 8c. Korrektur nach dem Blast Radius (2026-09-20, Test `ddf90e1`, Fix `94b7480`)

Der erste Blast Radius über alle Familien zeigte zwei Fehler in S5bs **eigenem** neuen Code,
dazu eine Kantenlage am geforderten Übergang O01/O02. Drei Hebel, sonst nur Kommentare
(AST-Vergleich gegen `67527da`):

| Hebel | Änderung | Anlass (gemessen) | Wirkung über 11 Pläne |
|---|---|---|---|
| K1 | Überlappung `> 0` → `> 1,0 mm²` | `> 0` entschied nach Gleitkomma-Rauschen. Auf vier Plänen (OG3, Barawitzka, Mollgasse, Muthgasse) verloren 23 Raumpaare ihren Durchgang; 22 davon mit < 0,2 mm² Überlappung (21 < 0,06 mm², größter 0,197 mm²), 16 davon laut senkrechter Wandsonde Wandlücken ≥ 700 mm. Der 23. ist eine echte Überlappung von 2,55 m² (Muthgasse KÜCHE in KÜCHE) und bleibt verworfen | +17 Durchgänge (Barawitzka 2, Mollgasse 5, Muthgasse 9, DD 1), alle mit Raumabstand 0 |
| K2 | Breitenschwelle 800 → 800 − 3 · 1 mm; der Wandabzug bleibt gepuffert | der 1-mm-Wandpuffer kostet jede an Wandflanken endende Öffnung 2 mm: Barawitzka KÜCHE 20,47 ↔ VORRAUM 3,87, echte 800-mm-Lücke ohne Türbogen, gemessen 798 mm | +1 Durchgang (genau dieser). Ein Kandidat am OG1 (VORRAUM 2,59 ↔ BAD 4,66, 798,06 mm — die Türlücke der Blocktür `tuer_8` ohne Breite) hängt jetzt allein an Regel (a), 284 mm Schwerpunktabstand |
| K3 | `_SPLITTER_MM` 50 → 25 | O01/O02 liegt an einer 450-mm-Wand; die Kontaktzone ist dort ein 50,0-mm-Band = alte Splitter-Schwelle, Reserve 97 mm² = 0,16 % (mit 25: 100,3 %). Am EG hängen drei weitere Durchgänge an derselben Kante (effektive Dicke 51,3 / 51,7 / 59,5 mm) | keine — K3 dreht auf 11 Plänen keine Entscheidung. Preis: die Regel wirkt als Abstandsdeckel d ≤ 500 − Splitter, er wandert von 450 auf 475 mm; fehlt in diesem Fenster der Wandkörper, entsteht ein raumlanger Durchgang (als Decke getestet) |

**Verworfene Bauart von K2:** den Wandverbund ungepuffert abziehen. Am Rennweg blähte das 59
von 120 Breiten um mehr als 100 mm auf (OG1 O05 948 → 1774 mm, OG2 GANG 6,06 ↔ VORRAUM 4,92
1548 → 4055 mm), erzeugte am UG zwei Durchgänge durch lückenlose 100-mm-Wände (1810 und
1552 mm) und kippte O01/O02 über die Splitter-Kante.

**Wirkung am Rennweg:** auf den 7 Prüfgeschossen ist das Modell nach der Korrektur **strikt
identisch** mit `67527da` (Türen samt id/xy/Detail, Räume, Wohnungen, Ausgänge). Die ganze
Wirkung liegt in den drei anderen Familien und auf der DD.

**Einordnung der 18 Rückkehrer** (unabhängiger Prüfer; eigene Parses für Barawitzka,
Mollgasse und DD, Muthgasse nur aus den Messdaten): `67527da` → `94b7480` ist rein additiv,
kein Durchgang entfällt, keine Dublette im strengen Sinn (bekannte Tür am selben Raumpaar).
Von den 9 prüfbaren sind **3 echt** — die K2-Öffnung, Barawitzka TERRASSE 5,98 ↔ BALKON 7,29
und Mollgasse GANG 19,46 ↔ GANG 77,07 (beides Außenflächen) — und **6 Altartefakte der
vorgelagerten Raumerkennung**, die es schon vor S5b gab: Mollgasse „ABSTELLRAUM 24,57" ist
eine HLS-Schraffur und zugleich Wandkörper (3 Durchgänge); Rennweg DD, Mollgasse VORRAUM 8,17
↔ „STIEGENHAUS" (Außenanlage) und Barawitzka Treppenlauf 5,72 zählen den Umfang des kleineren
Polygons als Breite (9472 / 14200 / 6943 mm). Muthgasse (9): 1 Artefakt (Nebenzeichnung rund
347 m außerhalb des Grundrisses), 1 Verdacht (ZIMMER 14,02 ↔ KÜCHE 24,62: gezählt 2325 mm,
Sonde 202 mm), 7 nicht entscheidbar. K1 stellt also den Stand vor S5b wieder her und belegt
**keine** neue echte Innenöffnung; es bleibt, weil ein Kriterium nicht an 1e-18 mm² hängen darf.

### 8d. Gate-Messung auf `94b7480` (sauberer Arbeitsbaum)

`python tests/gate/gate_messung.py`, `arbeitsbaum_src_scripts_sauber = true`.
`pruefe_gate(nullmessung, messung)` liefert **5 Verstöße**: (3) M4.einraum OG1 2 → 3,
(3) M4.einraum DG2 0 → 1, (5) Einraum 2 → 3, (6) `segmente_graph` 0, (6) Anker in
WOHNUNG_PRIVAT 3. **Erfüllt:** (0); (1); (2) — beide roten Fälle gedreht, **18 von 18
BESTANDEN**, M17-02-a bleibt BESTANDEN; (4); (7) alle elf verneinten Verbindungen 0;
(8) alle vier geforderten Übergänge ≥ 1. `pytest -m gate tests/gate`: 3 passed, 1 xfailed
(per Design).

**Nachtrag 2026-09-20 (Bedingung (10) dazu):** derselbe Lauf auf `826b157` liefert **6
Verstöße** — die fünf oben plus `(10) Barawitzka EG ABSTELLRAUM 1.98 m² ohne Verbindung:
0 Tür(en)` (§ 1f). Die Zahl ist gewollt: (10) hält einen Befund fest, den kein Slice dieses
Branches heilt. `pytest -m gate tests/gate` bleibt unverändert 3 passed, 1 xfailed.

| Nullmessung → S4b → S5b | OG1 | OG3 |
|---|---|---|
| Türen gesamt | 28 → 28 → 20 | 23 → 27 → 17 |
| Durchgänge ohne Türblatt | 26 → 17 → 9 | 20 → 13 → 3 |
| Wohnungen | 3 → 3 → 4 | 2 → 1 → 3 |
| Einraum-Wohnungen | 2 → 2 → 3 | 0 → 0 → 0 |
| GRAPH-Segmente | — | 5 → 0 → 0 |
| Anker in WOHNUNG_PRIVAT | — | 0 → 3 → 3 |
| Türen mit `von_raum == nach_raum` | 0 → 0 → 0 | — |

M1 bis M3 unverändert auf allen 7 Plänen. M4 gegen die Nullmessung: OG1 Wohnungen 3 → 4 /
Einraum 2 → 3; DG2 1 → 2 / 0 → 1; OG2 Einraum 1 → 0 und `privatraum_ohne_wohnung` 3 → 1;
OG3 Wohnungen 2 → 3.

**(3) ist neu mit S5b** und kein Türproblem im engen Sinn. OG1 `top_4` = ZIMMER 17,04: es
hing vor S5b nur über zwei von der Referenz **verneinte** Durchgänge (zu BAD 11,76 und GANG
6,48) an der Wohnung; seine echte Tür T04 (`tuer_5`, Block 840) führt in die Wohnküche
73,06, die **keinen Raumtyp** und damit keine Klasse trägt — dort endet die Wohnungsbildung.
DG2 ZIMMER 19,60: vorher über einen 3437-mm-Durchgang an VORRAUM 10,84, jetzt nur noch
`tuer_1` zum VORRAUM 15,20, der ALLGEMEIN_ERSCHLIESSUNG ist (S7a-Kandidat `raum_7`, § 6c,
abhängig von der Zählbasis). § 6c ist vor S5b gemessen; ob S7a auf dem S5b-Stand (3) und (5)
heilt, ist nicht nachgemessen. Die untypisierte Wohnküche heilt kein Slice des Stapels.

Referenzabgleich OG1: T01–T07, T09 und T10 je genau eine Blocktür; T08 weiter als Durchgang
2518 mm (Balkontür → S4d); O01/O02 1198 mm, O03 1450 mm, O04 1198 mm, O05 948 mm.

### 8e. Blast Radius über alle Familien (V = `1e5e5ac` vor S5b · A = `67527da` · C = Korrektur)

Je Plan und Stand ein voller In-Memory-Parse (33 Läufe, Modulkopie per `git show`), kein
Output; von drei unabhängigen Prüfern nachgerechnet (0 Abweichungen in den Tabellen). C ist
auf dem Arbeitsbaum vor dem Commit gemessen, Produktionscode AST-gleich mit `94b7480`.
Durchgang = `quelle` beginnt mit `durchgang` (die frühere Zählung mit exaktem Vergleich
unterschlug auf Muthgasse die Durchgänge mit Text-Suffix: 119 → 48 statt 146 → 61).

| Plan | Durchgänge V/A/C | Türen V/A/C | Wohnungen V/A/C | Einraum V/A/C | Räume mit 0 Verbindungen V/A/C |
|---|---|---|---|---|---|
| Rennweg UG | 15/4/4 | 33/22/22 | 4/4/4 | 4/4/4 | 4/4/4 |
| Rennweg EG | 22/20/20 | 42/40/40 | 2/2/2 | 1/1/1 | 2/2/2 |
| Rennweg OG1 | 17/9/9 | 28/20/20 | 3/4/4 | 2/3/3 | 1/1/1 |
| Rennweg OG2 | 21/10/10 | 33/22/22 | 1/2/2 | 0/0/0 | 2/2/2 |
| Rennweg OG3 | 12/2/2 | 27/17/17 | 1/3/3 | 0/0/0 | 5/7/7 |
| Rennweg DG1 | 12/9/9 | 19/16/16 | 1/1/1 | 0/0/0 | 2/2/2 |
| Rennweg DG2 | 16/6/6 | 21/11/11 | 1/2/2 | 0/1/1 | 3/3/3 |
| Barawitzka EG | 61/24/27 | 99/62/65 | 6/14/13 | 4/9/8 | 7/13/11 |
| Mollgasse EG | 70/26/31 | 147/106/111 | 9/23/21 | 2/18/15 | 2/4/3 |
| Muthgasse E2 | 146/61/70 | 264/181/190 | 7/34/28 | 3/21/15 | 6/8/7 |
| **Summe 10 Prüfpläne** | **392/171/188** | **713/497/514** | **35/89/80** | **16/57/47** | **34/46/42** |
| Rennweg DD (getrennt) | 2/1/2 | 3/2/3 | 0/0/0 | 0/0/0 | 0/0/0 |

Es entfallen also **204 Durchgänge** (392 → 188). `final_exit` 14 → 16 → 16, `stair_exit`
17 → 14 → 14 (OG3 1 → 0, Muthgasse 4 → 2), Außenöffnungen 11 → 16 → 16 (Mollgasse 7 → 10,
Muthgasse 0 → 2: weniger Innen-Durchgänge bedienen die 600-mm-Regel, S5c unberührt).
Nutzungsklassen-Wechsel V → A: Mollgasse `raum_7` und `raum_55`, Muthgasse `raum_68`; A → C:
Mollgasse `raum_7` VORRAUM 8,17 zurück auf ALLGEMEIN_ERSCHLIESSUNG (K1-Durchgang zur
Außenanlage, 14,2 m „breit").

**Wird ein Raum unerreichbar?** Acht Räume hatten vor S5b mindestens eine Verbindung und
haben danach keine mehr. Alle 16 verlorenen Verbindungen waren synthetische Durchgänge:

| Plan | Raum | Verlauf V/A/C | Befund | Klasse | heilt |
|---|---|---|---|---|---|
| Rennweg OG3 | `rest_3` STIEGENHAUS 2,94 | 1/0/0 | 4 Blocktüren liegen 905–938 mm vor dem Polygon, alle mit `KEIN_RAUM`-Seite | Durchgang war Artefakt, echte Tür ohne Raumseite | S3b |
| Rennweg OG3 | `rest_6` (leer) 5,46 | 4/0/0 | Wohnungsflur als Restfläche, endet vor `tuer_8/9/10` | wie oben | S3b |
| Barawitzka EG | `raum_22` BAD 4,51 | 2/0/0 | Bogentür `tuer_19` (830) 125 mm am Bad, zugeordnet VORRAUM / `KEIN_RAUM` | wie oben | Seitenzuordnung am gestempelten Raum (S4b-Rest, kein benannter Slice) |
| Barawitzka EG | `raum_28` ABSTELLRAUM 1,98 | 2/0/0 | die 830er Bogenöffnung hat **keine eigene Tür**: sie steckt in `tuer_38` „doppelfluegel" 1660 (Fehlpaarung zweier Einzeltüren) | **echte Tür ohne Ersatz** | S4a-Rest (Doppelflügel-Paarung) |
| Barawitzka EG | `raum_36` (leer) 29,87 | 2/0/0 | Wandkörper lokal mit Lücken (Sonde 853 / 2658 mm), kein Türbogen ≤ 2,9 m; scheitert an der Kontaktgrenze mit globalem Abstand (§ 8f) | unklar | — |
| Barawitzka EG | `rest_2` (leer) 3,40 | 2/0/0 | Bogentüren `tuer_26` (900) und `tuer_12` (1003) 858 / 981 mm vor dem Polygon, `KEIN_RAUM`-Seite; hier hing die `brandschutztuer` | Durchgang war Artefakt, echte Tür ohne Raumseite | S3b (an Bogentüren) |
| Mollgasse EG | `raum_21` BAD 4,37 | 2/0/0 | Blocktür `tuer_43` (800) 24 mm am Bad, zugeordnet GANG / `KEIN_RAUM` | wie oben | Seitenzuordnung (S4b-Rest) |
| Muthgasse E2 | `raum_91` KÜCHE 2,55 | 1/0/0 | liegt zu 99,97 % in `raum_29` (verschachteltes Polygon) | Durchgang war Artefakt | Raumerkennung, kein Slice |

S5c heilt keinen der acht. Die Korrektur bindet vier Räume wieder an (Barawitzka `raum_1`
Treppenlauf und `raum_2` TERRASSE, Mollgasse `raum_4` GANG 19,46, Muthgasse `raum_81`) —
keiner davon ist ein Innenraum mit belegter Wandöffnung (§ 8c).

**Die Zählung „0 Verbindungen" unterschätzt den Effekt**, weil sie Türen mit `KEIN_RAUM`-
oder AUSSEN-Gegenseite mitzählt. Begehbare Räume ohne Tür zu einem anderen Raum: 12 → 38 →
34; zu den acht kommen 14 weitere, u. a. OG3 `rest_4` STIEGENHAUS 9,78, DG2 TERRASSE 9,93,
Mollgasse MUELLRAUM 35,08 und acht Muthgasse-Räume (darunter SCHLEUSE 13,04), deren
Text-/Blocktüren eine `KEIN_RAUM`-Seite haben. Zusammenhangskomponenten über die 10 Prüfpläne:
**30 → 72 → 61** (Barawitzka 3/13/10, Mollgasse 4/12/9, Muthgasse 8/27/22, OG3 3/7/7, DG2
1/2/2). Vorbehalt: die Konnektivität vor S5b war zum Teil falsch (Durchgänge durch
geschlossene Wände); V ist Vergleichsstand, nicht Wahrheit. Der Kern: die synthetischen
Durchgänge waren in diesen Familien die Stellvertreter echter Türen, deren Raumseite fehlt
(`seite_fehlt`: Barawitzka 30, Mollgasse 21, Muthgasse 79). Das Gate misst nur Rennweg —
**diese Fragmentierung sieht es nicht.**

### 8f. Offene Befunde aus Messung und Review (nicht gebaut)

1. **Kontaktgrenze rechnet mit dem globalen Paarabstand.** Rennweg DG2 TERRASSE 9,93 ↔
   VORRAUM 15,96: Wandkörper-Lücke 1371 mm (Sonde, am Rennweg kalibriert), globaler
   Raumabstand 400,000 mm, lokal 401,567 mm — der freie Teil liegt 150,959 mm von beiden
   Räumen bei Grenze 151,000 mm, `_grenz_breite` misst 45,7 mm → verworfen. Gleiches Muster
   Barawitzka STIEGENHAUS 30,02 ↔ (leer) 29,87 (global 0, lokal 270 mm). Betrifft § 8a;
   ein lokaler Abstand je freiem Teil wäre die Korrektur, mit eigenem Blast Radius.
   **Vom Entscheid zu § 8a (2026-09-20, Kontaktgrenze übernommen) ist dieser Befund nicht
   berührt und bleibt offen:** er betrifft nicht die Toleranz, sondern welchen Abstand sie
   anwendet. Ob am DG2 Fenstertür oder Festverglasung steht, ist nicht gemessen.
2. **Breitenmaß bei Raumabstand 0:** `_grenz_breite` zählt den Umfang eines kleinen Polygons
   in der Kerbe eines großen als Öffnungsbreite (DD 9472 mm bei 2920 mm gemeinsamer Kante).
3. **Phantom Rennweg OG3 ZIMMER 45,36 ↔ WC 1,51, 1794 mm:** 1667 der gezählten mm liegen
   1–3 mm neben dem Wandkörper (fester 1-mm-Wandpuffer; mit 2 mm blieben 278 mm). Schon in
   `67527da`, kein Rückschritt. Mit `min` statt `max` beider Raumseiten entfielen am Rennweg
   genau drei Durchgänge (dieser, DG2 STIEGENHAUS 0,87 ↔ VORRAUM 15,96, OG2 BAD 4,58 ↔
   WC 1,55) — eigener Slice, vorher Blast Radius.
4. **Regel (a) misst gegen den Schwerpunkt des freien Teils:** eine 800- oder 900-mm-Türlücke
   am Wandende bleibt bei Türen ohne Sehnenzone als Dublette stehen (30 von 84 Rennweg-Türen
   haben keine Sehnenzone). Als Decke getestet, an den 11 Plänen ohne Treffer.
5. **Überlappungstoleranz ist eine Fläche** und skaliert mit der Kantenlänge (4 m Kante:
   0,25 µm Überstand = 1 mm²). Gegen die Messwerte (≤ 0,197 mm² gegen 2,55 m²) reicht sie.
6. **Muthgasse-Türnummern:** von 20 Texten, die vor S5b an einem Durchgang hingen, hängen 9
   nur noch an Türen mit `KEIN_RAUM`-Seite und 3 an keiner Tür mehr (E2-VF-15b, T-E2-8-05-1,
   T-E2-9-07-2).
7. **Grenzen der Wandsonde:** an Barawitzka laufen Wandkörper durch die Türöffnungen (an 15
   erkannten Türen findet die Sonde nur bei 4 eine Lücke) — „Sonde 0" ist dort kein Beleg
   für „keine Öffnung".
