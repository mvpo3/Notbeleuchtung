# Merge-Gate des Türstapels S4a → S4b → S5b → S5c

Stand: 2026-09-18 · Owner: Selman (`src/notbeleuchtung/raumerkennung/`) · Branch
`selman/uebernahme-enis-m17` · Nullmessung auf Code-Stand `f15d03f` (Tranche 1)

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
| `distinct_rooms_connected_by_door` | Räume an A/B; Verbindungen = Türen zwischen beiden Räumen im clip, deren Abstand zur Sonde O ≤ halbe Türbreite ist | A/B verschieden und genau **eine** Verbindung **mit** Türblatt; genau eine **ohne** Türblatt → `NICHT_MESSBAR` (Frage an Enis, § 2) |

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

### Eingabe und Rechenstand

Alle Messungen gegen die getrackten DXF unter `Projekte/Rennweg/`; die Messung schreibt
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
| **M17-04-c** | **NICHT_MESSBAR** | einzige Verbindung WC ↔ Vorraum ist `durchgang_21`: Durchgang **ohne Türblatt**, 2506 mm breit, `tuer_detail` wohnungseingang, 534 mm von O — die Referenz erwartet eine „Türverbindung"; Frage an Enis in `docs/OFFENE_FRAGEN.md` |
| M17-05-a | BESTANDEN | W in Wandkörper 78 |
| M17-05-b | BESTANDEN | F (Möbel) in keinem Wandkörper |
| M17-05-c | BESTANDEN | F und R in `raum_1` |
| M17-06-a | BESTANDEN | W in Wandkörper 94 |
| M17-06-b | BESTANDEN | I genau in `raum_1` (ZIMMER, 16,11 m²) |
| M17-06-c | BESTANDEN | X liegt nicht im Zielraum `raum_1` (in keinem Raum) |

**Bilanz: 16 BESTANDEN · 1 NICHT_BESTANDEN · 1 NICHT_MESSBAR.** Die Erwartung aus Enis'
Fassung 2 (01-a/b/c und 02-a bestanden, 02-b mit drei Portalen nicht) ist getroffen; die
12 Erwartungen M17-03 bis M17-06 sind hier zum ersten Mal gemessen — 11 bestanden, eine
nicht messbar.

Gegenüber Enis' Fassung 2 ändert sich damit: M17-02-c von OFFEN auf BESTANDEN (durch die
Toleranzentscheidung § 4), die Gesamtbilanz des Pakets von 4 / 1 / 13 auf 16 / 1 / 1
(davon 1 nicht messbar wegen mehrdeutiger Referenz). Die Referenzlabels bleiben
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

---

## 3. Gate-Regel

Der Stapel **S4a → S4b → S5b → S5c wird nur gemeinsam gemergt**, und nur wenn
`pruefe_gate(nullmessung, messung)` **keinen** Verstoß liefert:

| Nr. | Bedingung | Umsetzung |
|---|---|---|
| (0) | Vergleichbarkeit | gleiche DXF (alle 7 SHA-256), gleiche Referenz-JSON, gleiche Toleranzen; Arbeitsbaum `src/`+`scripts/` sauber |
| (1) | keine der 18 Erwartungen fällt von BESTANDEN auf NICHT_BESTANDEN | Nenner 18, IDs und Reihenfolge wie die Referenz; ein Abrutschen von BESTANDEN auf NICHT_MESSBAR zählt ebenfalls als Verstoß (sichere Seite). NICHT_MESSBAR → NICHT_BESTANDEN ist kein Verstoß (heute M17-04-c, sobald Enis' Antwort vorliegt) |
| (2) | M17-02-b dreht auf BESTANDEN | die drei Durchgänge an der Wand verschwinden **und** M17-02-a bleibt BESTANDEN (die Wand bleibt erkannt) |
| (3) | M1 bis M4 steigen nirgends | je Plan und je Gate-Kennzahl (§ 1b) nachher ≤ vorher; Ganzzahlen exakt, `M3.rote_flaeche_m2` mit 0,001 m² Toleranz; fehlende oder ungültige Werte (NaN, bool, negativ) sind Verstöße |
| (4) | Türen mit `von_raum == nach_raum` null | OG1 |
| (5) | Einraum-Wohnungen auf OG1 sinken | nachher < 2 |

Zwischenstände der einzelnen Slices werden gemessen und berichtet (`python
tests/gate/gate_messung.py --out <datei.json>`, dann `pruefe_gate`), aber **nicht
gemergt** — auch nicht bei Verbesserung.

Heute liefert `pruefe_gate(nullmessung, nullmessung)` genau zwei Verstöße:
`(2) M17-02-b ist NICHT_BESTANDEN` und `(5) Einraum-Wohnungen sinken nicht: 2 → 2`.

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
