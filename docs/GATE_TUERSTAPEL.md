# Merge-Gate des Türstapels S4a → S4b → S5b → S4c → S7a+S7b → S7c → S4e → S3b → S5c

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
| (11) | Rennweg DG1: das Geschoss behält nach dem Stapel einen echten Ausgang | Owner-Entscheid 2026-09-26 (VA-5, § 6g.11): „DG1 hat nach dem Stapel mindestens einen Ausgang, und keiner davon führt durch den Liftschacht." Messbar als `dg1.ausgaenge ≥ 1` **und** kein Ausgang, dessen Tür am Liftschacht liegt (Raumpaar mit dem Aufzugsring bzw. Türpunkt < 250 mm vom `lift_1`-Polygon). Heute ist `durchgang_9` (`rest_2` ↔ `rest_3`, 4 215 mm, Mittelpunkt im Lift) der **einzige** Ausgang von DG1 — S5c darf ihn nur entfernen, wenn ein echter Ausgang bleibt; sonst wäre das Geschoss ausgangslos. **Noch nicht in `gate_regel.py` verdrahtet** (Verdrahtung mit S5c; bis dahin Doku-Pflicht). Derselbe Messfall gilt für die Lifttür-Ausgänge OG1 `exit_durchgang_8`, EG `exit_durchgang_19`, UG `exit_durchgang_2` (Nebenbefund VA-5) |

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
- **Wer sie liest:** in der Pipeline nur `fluchtweg.py:329` (Segment-Starts). Durchleitung
  (`durchleitung_raeume`) und weiche Knoten (`volle_knoten`) lesen Klassen und rohe Rollen,
  nicht die korrigierten (Korrektur nach Review S7c, AST-belegt). Außerhalb der Pipeline
  liest `scripts/plan_pruefen.py` sie für die Fluchtweg-Auskunft im Prüfbericht.

**Durchleitung (Owner-Entscheid 2026-09-20, weiter gültig und jetzt gebaut).** Privat heißt
keine Notbeleuchtung und keine eigene Zirkulation — **kein Loch im Graph**: ein privat
gewordener Erschließungsraum bleibt Knoten für Wege zwischen zwei allgemeinen Räumen (nur
wenn das Raumpolygon die Strecke deckt), bekommt aber keine eigenen Stützpunkte, Anker oder
Leuchten. Ohne das zerreißen Wege — gemessen: Mollgasse 1OG STIEGENHAUS `raum_35` 10 → 2
Segmente, Rennweg UG KINDERWAGENRAUM verliert sein einziges, drei neue
`fluchtweg_warnungen` „kein final_exit erreichbar". Messfall (ii) (KINDERWAGENRAUM behält
seinen Weg) und (iii) (die drei Warnungen verschwinden) sind erfüllt und im Naht-Test
gebunden; Messfall (i) ist mit S7c entschieden — Owner 2026-09-26, Option A: Zielbild 9 statt 17
(§ 6g.10); Messfall (iv)
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
| **(6)** | Rennweg OG3 `segmente_graph = 0` — Fluchtweg-Graph, nicht Klassifikation. Der Anker-Teil derselben Bedingung ist erfüllt (0 Anker in `WOHNUNG_PRIVAT` auf OG3) | **S3b** (Restflächen enden vor den Blocktüren; auf OG3 ist das Stiegenhaus `rest_3`/`rest_4`, keine Tür erreicht es, § 6c). S7c heilt den GRAPH-Teil **nicht** — gemessen § 6g.10: OG3 hat keinen Ausgang, `segmente_graph` 0 vor wie nach |
| **(10)** | Barawitzka EG ABSTELLRAUM 1,98 m² ohne Verbindung, `raum_28` — Türerkennung | **S4c** |
| **(3)** | `M4.einraum` DG2 0 → 1: `raum_5` ZIMMER bildet die Einraum-Wohnung `top_2`, weil VORRAUM `raum_7` Erschließung ist und `raum_5` nur über `tuer_1` an ihm hängt; die Wohnungsgrenze (b) fällt damit auf `tuer_1` | **offen, NICHT S4e** (nachgemessen: 0 Regel-5-Türen auf DG2) — Kandidaten **Board 3 (Blatt-Semantik, @EnisAMG)** und **S5c**; keine S7-Regel heilt sie |

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

- **S7c** — **gebaut** (§ 6g.10, Stand `38b977f`), Wirkung auf den 12 Prüfplänen 0 Türen.
  Board-Frage 1 (Owner-Regel gegen die alte Abnahmezahl 17) ist **entschieden 2026-09-26:
  Option A** — die Abnahme aus Messfall (i) steht auf dem gemessenen Wert **9** (Mollgasse 1OG
  `raum_35` Start/Ziel; die 17 ist überholt, § 6g.10), `tests/naht` führt (2, 9) / 9 als
  Zielbild; Rennweg OG1 `rest_2` = 4 bleibt Abnahme und ist erfüllt (hängt an Option W von
  `raum_12`, Kanon-Punkt WOHNKÜCHE). S7c ist damit im Stapel merge-reif; Gate (3)(6)(10) wie
  vor S7c. Branch `selman/fix-s7c-rolle-aussen` gepusht (Owner-GO 2026-09-26), kein Merge.
- **Reihenfolge ab 2026-09-26 (Owner):** nächster Stapel-Slice ist **S3b**; S4e, S4c und S5c
  folgen. **S3c** (Fremdcluster-Filter und Extents-Ausreißer, VA-6 § 6g.11, `OFFENE_FRAGEN.md`)
  kommt als eigener Slice **nach dem Merge**, nicht in den Stapel. Neue Gate-Bedingung **(11)**
  (§ 3, VA-5): DG1 behält nach dem Stapel einen echten Ausgang, keiner durch den Liftschacht.
- **S4e** (Owner R5) — Regel 5 der Türtypisierung einschränken: eine Tür GANG → privater
  Raum wird nur dann roh zum Wohnungseingang, wenn der Gang selbst allgemein erschlossen
  ist, also vom Stiegenhaus ohne Wohnungseingang erreichbar. Ausgangsmessung liegt vor:
  **70 Regel-5-Türen, davon 46 S4e-Kandidaten** über 12 Pläne — UG 2/0 · EG 0/0 · OG1 2/2 ·
  OG2 2/2 · OG3 4/4 · DG1 4/4 · DG2 0/0 · DD 0/0 · BARA 0/0 · MOLL_EG 27/13 ·
  MOLL_1OG 16/13 · MUTH_E2 13/8. Größte Nester: MUTH `raum_94` 6 · OG2 `raum_9` 6 ·
  MOLL_1OG `raum_42` 5. Blast Radius über alle 12 Pläne ist Teil von S4e.
  **S4e heilt Gate (3) auf DG2 NICHT** (Owner-Klarstellung 2026-09-26): dort zählt die
  Ausgangsmessung 0/0 Regel-5-Türen, die Rolle sitzt auf blattlosen Durchgängen. Diese
  Bedingung hängt an Board 3 (Blatt-Semantik) und S5c, nicht an S4e.
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

#### 6g.10 S7c gebaut — die Rolle wandert an die äußere Tür; die Owner-Abnahme (i) braucht einen Entscheid

**Owner-GO 2026-09-25/26, wörtlich:** „Wird ein Vorraum privat, wandert die Rolle Wohnungseingang
an die äußere Tür (Vorraum zu Stiegenhaus oder allgemeinem Gang). Die innere Tür wird zimmertuer.
Einbahn beachten: rohe Rolle → Klasse → korrigierte Rolle → Fluchtweg, nie zurück." Abnahme:
Mollgasse 1OG `raum_35` wieder 17 Start/Ziel-Segmente, Rennweg OG1 `raum_14` wieder 4 an `rest_2`,
die acht Wege über das Stiegenhaus zurück, jetzt mit der Stiegenhaustür als Start. Zusatz
2026-09-25: die zwei Innentüren am Gang mit roher Rolle `wohnungseingang` und der Flag-Verlust von
OG1 `raum_4`/`raum_5`/`raum_8` (Vision-Audit § 6).

**Gebaut** (Branch `selman/fix-s7c-rolle-aussen`, Stand `38b977f`, zwei Runden mit je drei
Review-Linsen; Runde 1 wurde vom Absturz der Session unterbrochen und in Runde 2 zu Ende
geprüft): in `wohnungsklasse.korrigierte_rollen` folgt der Wohnungseingang allein der Grenze
privat|Erschließung aus `wohnungsraeume` — die rohe Rolle der äußeren Tür entscheidet nicht mehr
mit. Vorher stand der Filter `rolle in ("zimmertuer", "wohnungseingang")` auch vor dem befördernden
Zweig; die äußere Tür eines privat gewordenen GANGES trägt roh `stiegenhaustuer` oder keine Rolle
und blieb liegen. Der herabstufende Zweig behält den Filter; eine `balkontuer` wird nie befördert.
Einbahn unverändert (§ 6g.6): entsteht nach der fertigen Klassifikation, steht nicht im Modell,
einziger Pipeline-Leser `fluchtweg.py:329`; belegt per AST und Verfälschungsexperiment auf 11
Plänen. `wohnungseingaenge` (b) bleibt unverändert; sein Docstring und
`test_e7_bilde_wohnungen_liest_keine_korrigierte_rolle` binden die gemessene Beziehung zu den
korrigierten Wohnungseingängen (66 Topologien, 12 Pläne): Tür für Tür gleich, außer „nur (b)"
an einem Wohnungsseiten-Raum, der für (a) nicht privat ist, und „nur korrigiert" an Türen mit
anderer roher Rolle, die S7c befördert — Gleichheit ginge nur durch Rückspeisen (a) → (b).

**Wirkung auf den 12 Prüfplänen: 0 Türen.** An der Grenze privat|Erschließung liegt auf keinem Plan
eine Tür, deren rohe Rolle nicht schon `zimmertuer` oder `wohnungseingang` ist (Regel 3/5 der
Türtypisierung vergeben für „statisch privat × statisch allgemein" immer `wohnungseingang`); der
`balkontuer`-Riegel trifft 0 Türen. Ausgeliefertes RaumModell, Segmente, Zirkulation, Anker,
Ausgänge und Leuchten sind auf 12/12 Plänen feldgleich zu `bface2b` (34 Messschlüssel, volle
Pipeline auf 11 Plänen durch zwei Linsen unabhängig). Kein Rückfall: 9 Notlicht-Verlierer
(47,71 m²), Einraum-Liste, Anker in `WOHNUNG_PRIVAT` (DG1 2, MOLL_EG 1, sonst 0), keine neue
Wohnung ohne Eingang gegenüber HEAD. Der konstruierbare Fall (Nachbar-GANG privat gedreht, äußere
Tür roh `stiegenhaustuer`/rollenlos) ist als Unit-Zusicherung gebunden.

**Abnahme (i), gemessen:**

| Größe | HEAD `5ac3e0f` | `bface2b` | S7c | Soll alt (E4 2026-09-21, **überholt**) | **Soll neu (Owner 2026-09-26, A)** |
|---|---|---|---|---|---|
| MOLL_1OG `raum_35` Start/Ziel | 17 | 9 | **9** | 17 | **9** — erfüllt |
| MOLL_1OG `raum_35` Stütz / Zirk | 10 / 64 | 2 / 13 | **2 / 13** | 10 / – | **2** / – — erfüllt |
| MOLL_1OG `raum_34` Stütz / Zirk | 17 / 49 | 9 / 41 | **9 / 41** | 17 / – | **9** / – — erfüllt |
| die acht Wege `seg_graph_tuer_5/6/7/8/25/28/82/83` | da | weg | **weg (0/8)** | da | **weg** — erfüllt |
| OG1 `rest_2` Start/Ziel (`raum_14` Stütz / Zirk) | 4 (3 / 9) | 4 (3 / 9) | **4 (3 / 9)** | 4 | **4** — erfüllt |

**Warum 17 je Starttür unerreichbar ist:** ein GRAPH-Segment entsteht je Tür mit korrigierter Rolle
`wohnungseingang` (`fluchtweg.py:329ff`, ID `seg_graph_<tuer>`); auf MOLL_1OG enden alle am
einzigen `stair_exit` `exit_durchgang_10`, „`raum_35` Start/Ziel = 17" heißt also „17 Starttüren".
Die acht fehlenden Starttüren sind die acht **inneren** Türen der bestätigt privaten Vorräume
`raum_2`/`raum_4` (`tuer_5`/`6`/`7`/`8`, `tuer_25`/`28`/`82`/`83`, roh und korrigiert `zimmertuer`)
— genau die, die der Owner-Satz zur Zimmertür macht. Die äußeren Türen `tuer_3`/`tuer_4`
(STIEGENHAUS ↔ Vorraum) tragen roh **schon** `wohnungseingang` (Regel 3) und **sind schon Start**
(`seg_graph_tuer_3`/`tuer_4`): die Wanderung ist dort strukturell erledigt und kann keinen Weg
hinzufügen (trüge die Stiegenhaustür eine andere rohe Rolle, wäre der Vorraum ohne
Wohnungseingang erreichbar und nie ankerprivat — als Zusicherung gebunden). HEAD hatte 17, weil
die Vorräume dort Erschließung waren (U14) und die acht inneren Türen als Wohnungseingang mit
Stützpunkten im Vorraum starteten — der Zustand, den S7a beendet hat.

**Board-Frage 1 (Owner Selman) — entschieden 2026-09-26: Option A** (Wortlaut unten). Regel und
Abnahmezahl schließen sich je Starttür aus. Drei Wege, alle in-memory mit voller Pipeline gemessen
(Executor und zwei Linsen unabhängig), nichts davon gebaut:

| | **A gebaut:** Regel gilt, Zahl fällt | **B:** Regel erweitern | **C:** Duplikate |
|---|---|---|---|
| Mechanik | innere Tür zimmertuer, Start nur an `tuer_3`/`tuer_4` | bestätigt privater VORRAUM zählt für (a) als Erschließung (wie Option W) → innere Türen Start, Vorraum durchgeleitet | je innerer Tür ein Segment mit Start an der äußeren Tür (Start-Regel `fluchtweg.py`) |
| MOLL_1OG `raum_35` Start/Ziel / Stütz / Zirk | 9 / 2 / 13 | 17 / 10 / 64 | 17 / 10 / 64 |
| MOLL_1OG `raum_34` Stütz / Zirk | 9 / 41 | 17 / 49 | 17 / 49 |
| die acht Wege | 0 | 8 eigene, Start an den inneren Türen (`raum_3`, `7`, `8`, `1`, `30`, `12`, `90`, `36`) | 8 punktgleiche Kopien von `seg_graph_tuer_3`/`_4` (Hausdorff 0,000 mm), ID nennt eine Tür, an der der Weg nicht startet |
| Klassen, Flags, Verlierer, Anker, Ausgänge, Leuchten (14, Positionen) | – | identisch A | identisch A, keine Doppel-Leuchten |
| Zirkulationspunkte, Delta | – | `raum_3/7/8/30/90` je +1; **`raum_2` 1 → 16, `raum_4` 1 → 24** (7 der 8 Wege per Skelettpfad durch die bestätigt privaten Verlierer-Vorräume, Durchleitungs-Ausnahme „Direktlinie verlässt das Raumpolygon"); `raum_34` 41 → 49, `raum_35` 13 → 64 | `raum_2` 1 → 6, `raum_4` 1 → 4 (verdoppelter Startpunkt); `raum_34`/`raum_35` wie B — reine Mehrfachzählung derselben Geometrie |
| korrigierte Rollen anders | – | 13 Türen (`zimmertuer` → `wohnungseingang`) | 0 |
| Owner-Satz „die innere Tür wird zimmertuer" | erfüllt | **verletzt** | erfüllt (Rolle), aber acht Kopien |
| Owner-Grundsatz „privat heißt keine eigene Zirkulation" | erfüllt | verletzt (Stützpunkte in Räumen mit Flags 00 und ohne Leuchte) | erfüllt |
| OG1 | 4 an `rest_2` | 4 (B ändert nur Rollen `tuer_4/7/8`) | 4 („kein äußerer Weg", `top_1` ohne Eingang) |

**Planer-Empfehlung: A.** 9 ist die Zahl, die aus den Owner-Grundsätzen (Durchleitung, keine eigene
Zirkulation privater Räume, § 6g.6) folgt; HEAD 17 war Folge der falschen Vorraum-Klasse. Dann
werden (2, 9) / 9 in `tests/naht` vom Charakterisierungs- zum Zielbildwert, Messfall (i) ist kein
S7c-Fall mehr und Gate (6) OG3 bleibt allein bei S3b. Bei B oder C kippen die drei Zusicherungen
`MESSFALL_I_MOLL`, `raum_34`-Liste und `test_messfall_i_acht_wege_ueber_das_stiegenhaus` gemeinsam
(gewollt, kein Rückfall) — B braucht zudem die ausdrückliche Rücknahme des Satzes „die innere Tür
wird zimmertuer".

**Owner-Entscheid 2026-09-26 (Selman), wörtlich:** „Board-Frage 1: Option A. Begründung: ‚privat'
heißt keine eigene Zirkulation, das ist der Grundsatz aus der Durchleitungs-Entscheidung, und er
gilt unverändert. Die Zahl 17 stammt aus einem Stand, in dem die Vorräume Erschließung waren; sie
ist mit der Regel nicht erreichbar und wird daher angepasst, nicht die Regel. B scheidet aus:
private Vorräume für den Fluchtweg als Erschließung zu zählen, hebt genau das auf, was S7a/S7b
gebaut haben, und 7 der 8 Wege laufen per Skelettpfad durch Räume ohne Notlicht. C scheidet aus:
8 punktgleiche Duplikate (Hausdorff 0 mm) sind keine zusätzlichen Wege, nur doppelte Einträge."

Folgen: die Abnahme (i) steht auf dem gemessenen Wert (Tabelle oben, Spalte „Soll neu"); die 17
bleibt als überholte Vorgabe dokumentiert, nicht gelöscht. `tests/naht` führt `MESSFALL_I_MOLL =
(2, 9)`, die `raum_34`-Liste (9) und die Abwesenheit der acht Wege als **Zielbild**. Rennweg OG1
`rest_2` = 4 bleibt Abnahme und ist erfüllt. Leonis ist informiert (Board `docs/COORDINATION.md`,
2026-09-26): die 17 war seine Vorgabe; besteht er auf der Durchleitung mit eigenen Wegen aus den
privaten Vorräumen, ist das eine Regeländerung (Option B), keine Abnahme-Anpassung, und geht ins
Board.

**Rennweg OG1 — Owner-Zusatz 2026-09-25 und VA-4, gemessen (Executor + Linse Sicherheit):**

- Die zwei Innentüren am Gang mit roher Rolle `wohnungseingang` sind `durchgang_1` (ZIMMER `raum_2`
  ↔ GANG `raum_8`, blattlos 1 198 mm) und `tuer_6` (BAD `raum_7` ↔ GANG `raum_8`, Blatt 840 mm),
  beide aus **Regel 5** (`tuer_typisierung.py:197`, GANG statisch allgemein × privater Raum; zur
  Typisierungszeit ist `nutzungsklasse` leer) — die zwei S4e-Kandidaten auf OG1. Korrigiert
  `zimmertuer` (beide Seiten in `top_1`, `raum_8` bestätigt privat).
- `raum_4` VORRAUM 3,40 · `raum_5` VORRAUM 2,59 · `raum_8` GANG 6,48: `WOHNUNG_PRIVAT`, Flags 00,
  `top_1`, Ankerurteil privat („nur über die Wohnungseingangstür `tuer_3` (mit Türblatt)
  erreichbar", Pfad `raum_14` → `tuer_3` → `raum_12` → `durchgang_5` → `raum_10` → `durchgang_4` →
  `raum_8` → …), bestätigt, belegt durch `raum_1`/`2`/`3` ZIMMER, kein Riegel. Flags 00 seit Runde 4
  (HEAD 11; R9 kurz 11 per Tiebreak; ab R10 00), S7c Vorher = Nachher.
- **Antwort auf „verlieren dadurch ihre Notlicht-Flags": nein, nicht dadurch.** Gegenprobe
  (S4e-Vorschau, beide rohe Rollen in-memory auf `zimmertuer`, volle Pipeline): außer den zwei rohen
  Rollen ändert sich **nichts** — Klassen, Flags, Wohnungen, Segmente, Verlierer (3 / 12,47 m²),
  Anker 19, Leuchten 10 identisch. Ursache des Flag-Verlusts ist der Entzug nach E3/R3 (§ 6g.4):
  Klasse privat ∧ Ankerregel roh privat über `tuer_3` ∧ G4 belegt ∧ kein Riegel.
- `top_1` hat keinen Wohnungseingang (roh wie korrigiert): seine Randtüren sind `durchgang_4`
  (→ `raum_10`, ohne Rolle) und zwei Balkontüren; `raum_10` (73,06 m², Wohnküchen-Stempel) ist
  untypisiert → R2 nimmt ihn aus jeder Wohnung. Die tragende Tür `tuer_3` ist nach (b) der Eingang
  von `top_2` = {`raum_11` AR, `raum_12` VR, `raum_13` WC}.
- **VA-4** (`tuer_10`/`tuer_11` WC/AR korrigiert `wohnungseingang`): `raum_12` ist unbestätigt privat
  (Option W) — Schritt 1 privat, aber `top_2` ohne Aufenthaltsraum → G4 nicht belegt → Notlicht
  bleibt → für (a) Erschließung → Innentüren korrigiert Wohnungseingang → `seg_graph_tuer_10`/`_11`.
  Genau daran hängt die OG1-Abnahme „4 an `rest_2`". Gegenprobe (`raum_10` in-memory als KÜCHE,
  Stellvertreter für den Kanon-Punkt WOHNKÜCHE): OG1 wird **eine** Wohnung mit 13 Räumen und
  Eingang `tuer_3`, `raum_12` bestätigt privat und belegt, Flags 00, `tuer_10`/`_11` korrigiert
  `zimmertuer`, `rest_2` Start/Ziel **2**, `raum_14` Stütz 1 / Zirk 3, Verlierer 4 / 23,41 m².
  Wer den Kanon-Punkt WOHNKÜCHE entscheidet (@EnisAMG), entscheidet damit diesen Abnahmewert mit;
  `tests/naht` nennt das im Docstring, damit es dann nicht als S7c-Rückfall gelesen wird.
- VA-3 (privater Vorraum `raum_12` als `ALLGEMEIN_ERSCHLIESSUNG`) ist seit S7a+S7b für die Klasse
  gelöst; die übrigen Fälle des Vision-Befunds (a) (Barawitzka `raum_19`/`30`/`31`, MOLL_EG
  `raum_29`) erreicht die Stiegenhaus-Flut über blattlose Durchgänge — Blatt-Semantik, Board 3 /
  S5c, nicht S7c.

**Gate auf dem sauberen Baum `38b977f`:** 3 Verstöße, keiner neu — (3) DG2 `M4.einraum` 0 → 1 (Board 3 / S5c), (6) OG3 `segmente_graph = 0` (S3b), (10) Barawitzka `raum_28` (S4c); (0) entfällt (`arbeitsbaum_src_scripts_sauber = True`), gegen die Runde-2-Messung weichen nur die `meta`-Schlüssel ab. Messung `_arbeit/gate/messung_s7c_38b977f.json`.

Tests auf dem Stand: `ruff` grün, `gen_schema --check` in sync, `tests/raumerkennung` +
`tests/contract` 717 passed / 6 skipped / 2 xfailed, `tests/gate` 73 passed, `pytest -m gate` 3
passed / 1 xfailed (das Gate selbst), `tests/naht` komplett 4 failed / 295 passed / 2 skipped /
16 xfailed — die vier Roten wortgleich mit dem Ausgangsstand (2× Leuchten in `WOHNUNG_PRIVAT`
OG1/OG3 = Board 1 @mvpo3, Muthgasse Türblöcke = S5b-Rest, Rennweg-Soll dieselbe OG3-Leuchte).
Zwei vorbestehende Befunde am Fluchtweg, nicht S7c, für S3b/S5c vorgemerkt: das ausgelieferte
Modell ist kein Fixpunkt von `fluchtwege` (`lift_erkennung.py:208` stanzt nach dem Fluchtweg-Lauf
den Lift aus; Rennweg EG/OG3 nur FALLBACK-Segmente betroffen), und die FALLBACK-Menge hängt an der
Raum-/Türreihenfolge (`fluchtweg.py:420-452`; EG, OG3, MUTH_E2).

#### 6g.11 Messfälle aus dem Vision-Audit (Rennweg OG1, 2026-09-25, `selman/vision-audit`)

Übernommen aus `docs/VISION_AUDIT.md` § 6 (Owner: „als Messfall in docs/GATE_TUERSTAPEL.md"):

- **VA-1 Durchgang durch die Aufzugsschachtmauer.** f15d03f: `durchgang_26` (`stiegenhaustuer`,
  2 188 mm, ohne Türblatt) verbindet die Treppenläufe `rest_1` mit dem Aufzugsring `rest_2` durch
  die links geschlossene, U-förmige Schachtmauer (Aufzug nur rechts zum Stiegenhaus offen; Enis
  15-M01, 01-B03). e617fd1: unverändert (`durchgang_9`, 4 689 mm). Soll: keine Verbindung
  `rest_1` ↔ `rest_2`. Beleg: `Projekte/_audit/Rennweg_OG1_v2/audit.json` (blind B022/B026/B027,
  Betrieb B012), `…/Rennweg_OG1_e617fd1_s7pruefung/VERGLEICH.md`.
- **VA-2 Außenfläche in Innentüröffnungen.** f15d03f und e617fd1 identisch: Außenpolygon reicht in
  die Öffnungen `raum_1`/`raum_2` (0,1105 m²), `raum_3`/`raum_5` (0,0594 m²), `raum_2`/`raum_5`
  (0,0106 m²). Soll: 0 m² Außenfläche zwischen zwei Innenräumen. Beleg: wie VA-1.
- **VA-3 (gegen S7) Privater Vorraum als ALLGEMEIN_ERSCHLIESSUNG.** f15d03f: `raum_12`
  `ALLGEMEIN_ERSCHLIESSUNG`; e617fd1: `WOHNUNG_PRIVAT` (`top_2`), Flags True/True (G4). Gelöst für
  die Klasse.
- **VA-4 (gegen S7/S7c) AR- und WC-Tür als Wohnungseingang.** f15d03f: `durchgang_20`/`_21`
  `wohnungseingang`; e617fd1: roh `zimmertuer`, korrigiert `wohnungseingang` (`raum_12` unbestätigt
  privat). Nach S7c gemessen: **eigene Ursache** (Option W von `raum_12`, hängt am Kanon-Punkt
  WOHNKÜCHE), nicht S7c — § 6g.10.
- **VA-5 (Owner 2026-09-26) Liftkern-Durchgang — `DURCHGANG_DURCH_WAND` ist kein Einzelfall.**
  Vision-Audit EG (f15d03f): 6 Meldungen, 5 richtig, 1 strittig. Auf dem Stapel-Stand `8b07780`
  (src = `42e8e14`) sind **3 von 6 offen**: B013 EG `durchgang_28` heißt heute **`durchgang_20`**
  (gleiche Lage, `rest_1` ↔ `rest_2`, 4 671 mm statt 2 187 — S5b misst über `_grenz_breite`
  statt über die MRR), B009/B010 `aussenoeffnung_2`/`_1` (Außenöffnungen an der Feuermauer,
  150 × 1 019 / 1 235 mm, 91–98 % außerhalb der Gebäudekontur, 250 mm Wandkörper auf der Linie;
  B009 wird über den Windfang `hauseingang` → `final_exit`, `seg_graph_tuer_17` endet dort).
  B003/B005/B007 sind durch S4a/S4b (Dublette der Blocktür `tuer_9`) und S5b (Querung NEIN)
  erledigt. Derselbe Kern liegt auf **OG1** (`durchgang_9`, 4 689 mm, = VA-1) und **DG1**
  (`durchgang_9`, `rest_2` ↔ `rest_3`, 4 215 mm) — **auf DG1 ist der Phantom-Durchgang der
  einzige Ausgang des Geschosses** (ohne ihn 0 Ausgänge, GRAPH 4 → 0). Zensus 12 Pläne (213
  Durchgänge, 17 Außenöffnungen): das Liftkern-Muster nur Rennweg EG/OG1/DG1; der Proxy
  „Mittelpunkt im Wandkörper" trifft es nicht, seine 25 Treffer (OG3 1, Mollgasse 7, Muthgasse
  17) sind unverifizierte Kandidaten.
  **Mechanismus** (Executor + Widerleger, unabhängig gemessen): einzige Quelle ist
  `tuer_zuordnung.durchgaenge_ohne_tuerblatt` (`:334-380`). `rest_2` ist zur Durchgangs- und
  Fluchtwegzeit der **ganze Schachtinnenraum inkl. Kabine** (2,70 m²) als STIEGENHAUS —
  Treppenmarker-Regel `rest_komponenten.py:130-131` vor der SCHACHT-Regel `:136-138`;
  `finde_lifte` läuft erst `provider.py:210` und lässt den Aufzugsring 0,96 m² übrig. Die
  Schachtwand (Stahlbeton 150 mm, U-förmig, EG Wall_38/39/40) liegt als Wandkörper dazwischen,
  77 % des Bands zwischen den Polygonen ist Wand. Der freie Teil der Kontaktzone ist ein
  **U-Ring um den Schacht** (1,015 m², MRR 2 161 × 2 187 mm), der beide Räume nur an den **zwei
  Wandenden auf der Lifttürseite** berührt (0,055 / 0,052 m²): `pa.distance(g) = pb.distance(g)
  = 0` ist damit trivial erfüllt (`:345-349`, `_kontakt_grenze` `:234-245`), die Breite ist die
  ganze U-Grenze (`_grenz_breite` `:248-278`), der Schwerpunkt liegt in `lift_1`, die Linie vom
  Türpunkt zu `rest_1` läuft 150 mm im Wandkörper. **Am Ort gibt es keine Öffnung und keine
  Wandlücke** — die Verbindung schließt sich um die Wandenden, nicht durch die Wand.
  **Zuordnung: primär S5b** — das Querungsprädikat sagt fälschlich JA, § 8a („die Querung führt
  nicht durch Wandkörper") ist verletzt, § 8f kennt den Fall nicht → **neuer S5b-Befund**;
  **Mitursache Rest-Typisierung/Lift-Reihenfolge** (Schacht bis `provider.py:210` STIEGENHAUS,
  der S5a-Guard `:322-323` greift nur für `KEIN_RAUM`). Dieselbe Mitursache macht die
  **Lifttüren zu `stair_exit`** (`tuer_typisierung.py:192-194`, `ausgaenge.py:74-76`): OG1
  `exit_durchgang_8`, EG `exit_durchgang_19`, UG `exit_durchgang_2`. **Nicht S5c** im
  Diagnose-Sinn (S5c = `aussen_durchgaenge` ohne Querungsprädikat, `tuer_zuordnung.py:389-451`)
  — dorthin gehören B009/B010; Gate-§-7-S3b ist nicht beteiligt.
  **Wirkung, gemessen:** EG ohne `durchgang_20`: Ausgänge 7 gleich (Dedup zu
  `exit_durchgang_19`), GRAPH 7 → 6, FALLBACK 1 → 3 (`rest_1` verliert sein einziges Segment),
  `raum_15` Stütz 5 → 4, Klassen/Flags/Wohnungen/Anker/M1–M4 gleich. OG1 ohne `durchgang_9`:
  alles gleich, `rest_2` Start/Ziel bleibt 4. **Hinweis zur OG1-Abnahme „4 an `rest_2`"** (keine
  Bewertung): sie besteht aus 3 Wegen mit Ziel **Lifttür** `exit_durchgang_8` (`raum_14` ↔
  `rest_2`, 209 mm neben `lift_1`) plus 1 FALLBACK im Aufzugsring; ohne `exit_durchgang_8` enden
  die Wege an `exit_durchgang_6` und `rest_2` fällt auf 1. Sie hängt nicht am Phantom-Durchgang,
  aber am Lifttür-Ausgang — Messfall für die Lift-Reihenfolge. Belege:
  Session-Scratch `…/8d935db0-…/scratchpad/s7c/va_diag/` (Executor `bericht_va.md`, zwei
  `review_*_r1/urteil.md`).
  **Owner-Entscheid 2026-09-26:** Zuordnung primär S5b mit S5c-Rest übernommen — Heilung im
  Stapel-Slice S5c (blattlose Öffnungen), Ursache im S5b-Prädikat (§ 8f). **Gate-Bedingung (11)**
  (§ 3): „DG1 hat nach dem Stapel mindestens einen Ausgang, und keiner davon führt durch den
  Liftschacht" — ohne diese Bedingung könnte S5c den falschen Ausgang entfernen und das Geschoss
  ausgangslos zurücklassen. Der Nebenbefund gehört dazu: dieselbe Mitursache macht die Lifttüren
  zu `stair_exit` (OG1 `exit_durchgang_8`, EG `exit_durchgang_19`, UG `exit_durchgang_2`). Die
  OG1-Abnahme „4 an `rest_2`" besteht aus drei Wegen mit zwei Liftfahrten plus einem Fallback im
  Aufzugsgang: **nach S5c prüfen, ob sie auf 1 fällt, und dann die Abnahme nachziehen, nicht die
  Regel.**
- **VA-6 (Owner 2026-09-26) Zweiter Zeichnungscluster im EG-DXF.** Bestätigt: **11 Räume**
  (171,74 m²), **15 Türen**, **1 365,8 m** Polygonabstand (Zentrum 1 380,3 m), Lage
  27,3 × 20,3 m. Reiner ArchiCAD-Zonensatz: 28 Top-Level-Entities (11 LWPOLYLINE „New_080
  Raumdefinitionen", 11 Zonenstempel-INSERTs, 6 MTEXT), keine Wände, keine Türblöcke, 0
  Wandkörper. Räume: `raum_1` KÜCHE („Wohnküche") 45,6 · `raum_2` AR · `raum_3` BAD · `raum_4`
  ZIMMER → `WOHNUNG_PRIVAT` `top_1`, Flags 00; `raum_5` GARAGE; `raum_6` VR 21,03 und `raum_7`
  STIEGENHAUS 6,72 (Erschließung); `raum_8` TERRASSE; `raum_9`/`18`/`19` untypisiert
  (Müllplatz, Zugangsweg, Garageneinfahrt); Stempel ohne Flächenwert. Alle 15 Türen sind
  synthetische `durchgang_1..15` (948–5 710 mm): in einer Zone ohne Wand verbindet
  `durchgaenge_ohne_tuerblatt` jedes Raumpaar ≤ 500 mm.
  **Warum keine Ausreißer-Logik greift:** `dxf_load._raw_wall_span` (2–98-%-Perzentil,
  `:59-63/107-118`) kalibriert nur den Faktor und sieht auf Rennweg EG 0 Wandpunkte (Faktor aus
  `$INSUNITS`); `bounds_mm` und die Wandkörper-Bounds decken nur den Hauptkörper;
  `tueren.im_planbereich` (`:480-503`) filtert nur Türobjekte, die Cluster-Türen entstehen erst
  danach in `provider.py:160`; die L-Stufe `raumlayer.raeume_aus_layer` (`:98-124`) hat keinen
  Planbereichs-Filter; nur der Render-Wächter `_geschoss_extents` (`dxf_renderer.py:338-370`)
  fängt den Fall, und nur fürs Blatt. **Keine Stelle der Raumerkennung filtert Räume.**
  **Wirkung** (Cluster an der Quelle entfernt, voller Parse): Räume/Türen 22/40 → 11/25,
  Wohnungen 2 → 1, Anker 39 → 35, alle 8 EG-Fluchtweg-Warnungen weg, 1 FALLBACK weg, Platzierung
  21 → 17 (Hauptkörper-Positionen identisch), Gate M1–M3 gleich, M4 `wohnungen` 2 → 1,
  `privatraum_ohne_wohnung` 1 → 0. **ID-Verschiebung:** die Hauptkörper-Durchgänge
  `durchgang_16..25` würden `durchgang_1..10`, `exit_durchgang_16..19` → `exit_durchgang_1..4`
  — EG-Abnahmen über Raumpaar + Lage formulieren, nicht über IDs (VA-5 hieße dann `durchgang_5`).
  **Zensus 12 Pläne:** ferne Raum-Cluster (> 100 m) nur Rennweg EG und Muthgasse E2 (Randcluster
  8 Räume, 26,78 m², 400,5 m — § 8c nennt „rund 347 m", andere Bezugsgröße; dort eine echte
  Nebenzeichnung mit 56 Wandkörpern, 0 Segmente/Anker/Ausgänge). **Zwei Zusatzbefunde des
  Widerlegers:** (a) das EG-DXF hat eine **dritte Lage** — 12 „Level Dimension"-INSERTs (Layer
  105 Bemassungen Projekt), 1 368,9 m vom Hauptkörper, ohne Räume/Türen; (b) der echte
  **Extents-Ausreißer sitzt im UG**: `modell.bounds_mm` spannt 319,9 × 1 391,2 m, weil zwei
  Wand-Layer-INSERTs mit fernem Einfügepunkt (Wall_2 1 304 m, Opening_1 204 m) in die Hülle
  eingehen (`dxf_load.py:227-228` nimmt für INSERTs nur den Einfügepunkt); Leser von `bounds_mm`
  außerhalb der Raumerkennung (`platzierung/aussen_strategy.py:73`,
  `hauptengine/bestand_leuchten.py:62`, `render/dxf_renderer.py`, `render/lux_nachweis_bericht.py:165`)
  — Wirkung dort nicht gemessen.
  **Zuständigkeit, nur benannt:** Ursprung Raumerkennung (Selman: `raumlayer`, `provider`,
  `durchgaenge_ohne_tuerblatt`, `dxf_load`); Render-Wächter hauptengine; Leuchten als Folge
  Platzierung (@mvpo3). Die Owner-Frage aus dem Audit bleibt: **soll das Modell fremde Cluster
  führen?**
  **Owner-Entscheid 2026-09-26: Nein.** Ein Cluster ohne jeden Wandpunkt, über 1 km vom
  Hauptgebäude entfernt, gehört nicht ins RaumModell. Regel (wörtlich): Hauptcluster ist die zusammenhängende Menge mit den meisten Wandpunkten. Alles, was weiter als
  100 m davon entfernt liegt UND null Wandkörper enthält, wird verworfen — nicht stillschweigend,
  sondern als Warnung „Fremdcluster verworfen" mit Anzahl Räume, Türen, Entfernung und Koordinaten
  im Bericht. Ein entfernter Cluster MIT Wandkörpern wird nicht verworfen (könnte ein zweiter Bauteil
  sein), sondern gemeldet und zur Entscheidung vorgelegt. Der Filter greift zentral an einer Stelle,
  nicht in jeder Teilfunktion einzeln (Kandidat: direkt nach dem Laden, vor der Raumbildung; Stelle
  prüfen und im Bericht begründen). Erwartete Wirkung ausweisen: Rennweg EG Wohnungen 2 → 1, Anker
  39 → 35, 8 Fluchtweg-Warnungen weg, Platzierung 21 → 17, plus die Wirkung auf alle anderen Pläne.
  Wenn irgendwo ein echter Bauteil wegfällt, stoppen und melden.
  **Eigener Slice S3c, nach dem Merge, nicht im Stapel** (`docs/OFFENE_FRAGEN.md`). Zu S3c gehören
  auch die beiden Zusatzbefunde der Widerleger (dritte Lage im EG-DXF, Extents-Ausreißer im UG).

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

**Nachtrag 2026-09-26 — neuer S5b-Befund aus dem Vision-Audit, VA-5 (§ 6g.11):** am Liftkern
(Rennweg EG `durchgang_20`, OG1 `durchgang_9`, DG1 `durchgang_9`) sagt das Querungsprädikat JA,
obwohl am Ort keine Öffnung ist — der freie Teil der Kontaktzone ist ein U-Ring um die
Schachtwand, der beide Räume nur an den Wandenden zur Lifttürseite berührt; Mitursache ist der
Schacht als STIEGENHAUS bis `provider.py:210`. Details, Zahlen und Wirkung in § 6g.11.

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
