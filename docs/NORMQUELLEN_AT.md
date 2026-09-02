# Normquellen-Status (Enis) — was liegt vor, was ist belegt, was fehlt

**Stand:** 2026-08-30 · Bestandsaufnahme rein lesend aus `knowledge/`.
Zweck: Trennung **Primärquelle / Sekundärquelle** und **Verbindlichkeitsebene**,
bevor Normwerte in `normwissen/data/` bestätigt oder geändert werden.

Ebenen: **A** verbindliche Rechtsquelle · **B** Richtlinie (OIB) · **C** Norm ·
**D** Fachinformation / Auslegungshilfe. *Eine Fachinformation ersetzt nie eine Norm
oder Rechtsvorschrift.*

## 1. Vorhanden (Original-PDFs, `knowledge/`)

### C — Normen
| Dokument | Ausgabe | S. | Pfad | Hinweis |
|---|---|---|---|---|
| ÖNORM EN 1838 | **2019-11-15** (IDT EN 1838:2013-07, Ersatz für ÖNORM EN 1838:2013-09) | 22 | `knowledge/EN 1838 - Notbeleuchtung 2019 (1).pdf` | Lizenzexemplar; **die im Repo zitierte Ausgabe 2013-09 liegt NICHT vor** |
| OVE E 8101 | 2025-10-01 | 852 | `knowledge/OVE E8101_2025 (1).pdf` | Teil 5-56 „Einrichtungen für Sicherheitszwecke" enthalten |
| OVE E 8101 | 2019-01-01 | 758 | `knowledge/OVE E 8101_2019 (1).pdf` | ältere Ausgabe |
| OVE E 8015 / E 8350 / E 8351 / OVE E 8014 | 2022 / 2017 / 2016 / 2019 | | `knowledge/…` | Randbezug |

### B — OIB-Richtlinien (Ausgabe Mai 2023, komplett RL 1–7 + Sonderrichtlinien)
`knowledge/OIB-Richtlinien/` — notbeleuchtungsrelevant: **RL 2** (Punkt 5.4 +
Tabelle 6), **RL 2-Erläuterungen** (S.48 zu Punkt 5.4), **RL 2.1** (3.6.5),
**RL 2.2** (4.3, 5.5.3, Tab. 3 Zeile 8.2), **RL 2.3** (2.14),
**Begriffsbestimmungen**, **Zitierte Normen und sonstige technische Regelwerke**.
Details: [`OIB_RL2_TABELLE6.md`](OIB_RL2_TABELLE6.md).
Verbindlichkeit entsteht erst durch Übernahme ins Landesbaurecht — in keinem der
Dokumente belegt → offen.

### A — Rechtsquellen (RIS-Ausdrucke)
ETG 1992 · ETV 2002/2010/2020 · ESV 2012 · Nullungsverordnung · Standesregeln.
Keine davon regelt die Erforderlichkeit von Notbeleuchtung direkt.

### D — Fachinformationen
`knowledge/OVE-Fachinformation/` (E01–E13, H02): notbeleuchtungsrelevant **E06**
(Bussysteme), **E07** (Funktionserhalt Leitungsanlagen), **E08** (Arbeitsstätten —
Ausführung von Sicherheitsbeleuchtung und nachleuchtenden Orientierungshilfen,
Ausgabe 2021-04-01).
Weiters `knowledge/extracted/` (38 selbst erzeugte Digests, **Sekundär**) und
Hersteller-Handbücher (Handbuch 2026, GSYSTEMS, Kaufel, licht.wissen 10, ONL).

### Sonderfall — eigene Arbeitskopie, NICHT amtlich
`knowledge/Österreichische Rechtsquelle/RIVOPLAN_Oesterreichische_Rechtsquellen_Notbeleuchtung_AT.pdf`
(Autor RIVOPLAN, erstellt 2026-08-30, 10 S.). Enthält aufbereitete Texte zu
**AStV § 9**, **AStV § 13**, **ASchG §§ 20/21**, **KennV inkl. Anhang 1 Pkt. 1.4**
plus RIS-Gesetzesnummern (ASchG 10008910, AStV 10009098, KennV 10009067 /
BGBl. II Nr. 101/1997). **Sekundärquelle** — die amtlichen RIS-Volltexte fehlen.

### LB-Material
`Leistungsbeschreibung BSP/` (4 PDFs, untracked): `mo-leistungsbeschreibung_Elektro_240718.pdf`
(Elektro-LV, direkter Kandidat), `250116_GU Leistungsbeschreibung.pdf`,
`20241209_E LV Fischa 46.pdf`, `mo-Bau-_und_Ausstattungsbeschreibung_…pdf`.

## 2. Prüfung der aktiven Werte gegen die vorhandene EN-1838-Ausgabe

Geprüft am 2026-08-29 gegen `knowledge/EN 1838 - Notbeleuchtung 2019 (1).pdf`
(PDF-Seite = Norm-Seite + 2).

| Wert in `normwissen/data/` | Fundstelle | Ergebnis |
|---|---|---|
| `z_hinterleuchtet: 200`, `z_beleuchtet: 100` | §5.5, Norm-S.13 | **bestätigt**, wörtlich („z ist eine Konstante: 100 für beleuchtete, 200 für hinterleuchtete Zeichen") |
| Formel `l = z·h`, h = „Höhe des Zeichens" | §5.5, Norm-S.13 | **bestätigt**; Maßeinheit von h und l muss gleich sein |
| `dauer_min: 60` | §4.2.5, §4.3.5, §5.4.5 | **bestätigt** („mindestens 1 h") |
| `lux.rettungsweg: 1.0` | §4.2.1, Norm-S.9 | bestätigt, **aber** gebunden an Wegbreite ≤ 2 m + 50-%-Mittelbereich + Anhang-B-Länderabweichungen — in der YAML nicht modelliert |
| `lux.antipanik: 0.5` | §4.3.1, Norm-S.11 | bestätigt („freie Bodenfläche **im Kernbereich**", Randbereiche 0,5 m ausgenommen — Randbereich fehlt in der YAML). Wortlaut „im Kernbereich" ist die **2019er** Fassung |
| `montagehoehe_min_mm: 2000` | §4.1.1, Norm-S.8 | bestätigt als Wert; Wortlaut ist ein **Erfüllungs-Kriterium**, kein absolutes Minimum — YAML-Kommentar „Hard Floor" ist strenger als die Norm |
| `norm: "ÖNORM EN 1838:2013"` | — | **nicht belegt** — diese Ausgabe liegt nicht vor; vorhanden ist 2019-11-15 |
| `piktogramm_hoehe_default_m: 0.15` | — | **nicht in EN 1838**; Praxiswert aus `_port_source/rz_coverage_oenorm.yaml` |
| `gleichmaessigkeit.rettungsweg: 40` | §4.2.2, Norm-S.10 | **bestätigt**, wörtlich („darf 1 : 40 entlang der Mittellinie des Rettungsweges nicht unterschreiten"). YAML führt max:min, die Norm min:max → Kehrwert |
| `gleichmaessigkeit.antipanik: 40` | §4.3.2, Norm-S.11 | **bestätigt**, wörtlich („darf 1 : 40 nicht unterschreiten") — **derselbe Wert wie der Rettungsweg**, nicht 1:10 (Abschnitt 2b) |
| `umschaltzeit.vollwert_s: 60` / `halbwert_s: 5` | §4.2.6, §4.3.6, §5.4.6 | **bestätigt** („50 % … innerhalb von 5 s und 100 % … innerhalb von 60 s"); die Norm ist zweistufig, das Contract-Feld ein Skalar → nur der Vollwert |
| `montagehoehe_mm: 2400` (raumtyp_regeln) | — | **unbelegt** — kein Notlicht-Eintrag in `heights_fachpraxis.yaml`; stammt aus der Slice-0-Fake-Fixture |
| `mindest_anzahl: 1` / `4` | — | **Engineering-/Fixture-Annahmen**, keine Normwerte |
| Zuordnung `STIEGENHAUS → sicherheitsleuchte`, Quelle „§4.1" | §4.1.2 b), Norm-S.8 | Art teilweise gestützt („nahe Treppen, um jede Treppenstufe direkt zu beleuchten"); die Regelform „eine Leuchte je Stiegenhaus-Raum" ist Auslegung, Quellenstring zu grob |

## 2a. Entscheidung zur Ausgabe-Bezeichnung (2026-08-30, Owner)

Der String `ÖNORM EN 1838:2013` **bleibt vorerst unverändert**, obwohl im Repo die
Ausgabe 2019-11-15 liegt. Grund: er ist keine reine `normwissen/`-Angelegenheit,
sondern **Naht-Invariante** (`Platzierung.norm_quelle ∈ NormRegelwerk.quellen`) und
hängt an sechs Stellen quer durch fremde Zuständigkeiten:

| Fundstelle | Eigentümer |
|---|---|
| `normwissen/data/en1838_grundwerte.yaml` (`norm:` + 3 `quellen`) | Enis |
| `tests/fixtures/norm_regelwerk_snapshot.json` | 3-Owner (CODEOWNERS) |
| `tests/fixtures/platzierung_4og.json` (5× `norm_quelle`) | 3-Owner (CODEOWNERS) |
| `tests/fakes.py` (`FakeNormProvider`) | Leonis' Test-Double |
| `tests/platzierung/test_flaechen_strategy.py` (harte Assertion) | Leonis |
| `hauptengine/contracts/norm_regelwerk.py` (Default + Docstring) | 3-Owner + `contract_version`-Bump + Schema-Regen |

⇒ Die Umstellung ist ein **eigener koordinierter Slice** (Fixture-Regen aus dem
echten Provider + Leonis-Abstimmung), kein Housekeeping. Bis dahin ist der
Beleg-Status direkt in `normwissen/data/*.yaml` als Kommentar markiert, damit kein
Leser den String für belegt hält. Inhaltlich ist die Deckungsgleichheit gegeben
(2019-11-15 ist IDT mit EN 1838:2013-07) — es geht rein um die **Bezeichnung**.

## 2b. Track-B-Werte (Contract `NormRegelwerk` v1.1.0) — Quellenprüfung 2026-09-01

PR #72 hat vier abfragbare Felder eingeführt, PR #80 konsumiert sie bereits. Geprüft
wurde jeder Wert am Volltext der im Repo liegenden Ausgabe
(`knowledge/_extracted_text/normen/EN 1838 - Notbeleuchtung 2019.txt`). Ergebnis: zwei
Felder sind belegt und gefüllt, zwei bleiben leer.

### Vier Korrekturen an den Annahmen aus PR #72

| Annahme (PR #72 · `platzierung/lux.py` · COORDINATION 01.09.) | Normtext | Konsequenz |
|---|---|---|
| Ud „40 Rettungsweg / **10 Antipanik**" | §4.2.2 **1:40** · §4.3.2 **1:40** (wortgleich) | Antipanik ist **40**, nicht 10 |
| die „10" gehöre zu Antipanik | §4.4.2: **Uo ≥ 0,1** für *Arbeitsplätze mit besonderer Gefährdung* | Uo (kleinste:mittlere, EN 12665) ist **nicht** Ud (kleinste:größte) — anderes Maß, falsches Feld |
| `flaechen_schwellen` = „EN 1838 §4.3 / OIB" (Contract-Docstring) | **60 m² und 8 m² kommen in EN 1838 nicht vor.** §4.3.8 nennt Toiletten für Menschen mit Behinderung **ohne** Flächenmaß | Fundstelle im Contract ist falsch zugeschrieben |
| `umschaltzeit_max_s` als ein Skalar | §4.2.6/§4.3.6/§5.4.6: **50 % in 5 s, 100 % in 60 s** | zweistufig; ein Skalar bildet nur den Vollwert ab |

Die Docstrings in `hauptengine/contracts/norm_regelwerk.py` und `platzierung/lux.py`
tragen die 40/10-Fehlangabe weiter. Beide liegen **nicht** in Enis' Lane (3-Owner-
Contract bzw. Leonis' Package) — der Befund ist gemeldet, nicht selbst korrigiert.

### Was gefüllt wurde

- `NormAnforderung.gleichmaessigkeit_max` = **40** für Rettungsweg (§4.2.2) und
  Antipanik (§4.3.2), über `gleichmaessigkeit_ref` in `raumtyp_regeln.yaml`.
- `NormAnforderung.umschaltzeit_max_s` = **60 s** (§4.2.6/§4.3.6/§5.4.6). Die
  5-s-Halbwertstufe steht als `umschaltzeit.halbwert_s` in der YAML, hat aber kein
  Contract-Feld → **offene Lücke**, an die 3 Owner gemeldet.
- Aufheller/Betonungsleuchten (§4.1): **kein** Ud-Wert — die Norm nennt für sie keine.

Beide Werte sind **inert**: 40 ergibt über `ud_min_aus_norm` exakt den bisherigen
Default 1/40, und `umschaltzeit_max_s` wirkt in `validierung.pruefe` nur gegen einen
LB-Wert. Mollgasse-EG-Durchstich vorher/nachher identisch (15 RZ + 21 SL, Status `ok`,
7 Befunde).

### Was bewusst leer bleibt — und warum

**`flaechen_schwellen` (60 m² / 8 m²).** Die Werte sind belegt, aber **nicht in
EN 1838** und **scope-gebunden**:

| Wert | Fundstelle | Scope im Original |
|---|---|---|
| 8 m² Sanitärbereiche | OVE E 8101:2019 `718.560.9.001.AT` 1) („in Sanitärbereichen ab 8 m2 Größe und in barrierefreien WC-Anlagen"); wortgleich ÖVE/ÖNORM E 8002-1 Punkt 1); OVE E 8101:2025 gleichlautend | nur „für Räume, Anlagen oder Gebäude, an die **erhöhte Anforderungen nach der Art der Nutzung** (OVE-Richtlinie R 12-2 bzw. OIB-Richtlinie 2) gestellt werden" |
| 60 m² | OVE E 8101:2019 / E 8002-1 Punkt 3): „Wartezonen, Abfertigungshallen, Geschäftsflächen über 60 m2 …" | nur **Flughäfen und Bahnhöfe** |
| 60 m² (allgemeiner) | ÖVE/ÖNORM E 8002-1 §3.2.2.1.2 | nur eine **ANMERKUNG** in einer Begriffsbestimmung (informativ), zusätzlich relativiert durch „oder bei kleineren Flächen, sofern … ein erhöhtes Risiko besteht" |

Das Contract-Feld ist dagegen **global**: `platzierung/flaechen_strategy.py`
`_ist_flaechen_antipanik` macht jeden Raum ≥ Schwelle antipanik-pflichtig, unabhängig
von der Gebäudenutzung. Ein Füllen würde die Schwelle über ihren Geltungsbereich hinaus
anwenden und im Audit-Trail unter `norm_quelle = "ÖNORM EN 1838:2013 §4.3.1"` führen,
obwohl der Auslöser aus OVE stammt.

**Vorschlag an die 3 Owner:** den Flächen-Trigger an den bereits vorhandenen
`OibRl2Provider` gaten — der bewertet genau die „erhöhten Anforderungen nach der Art
der Nutzung", auf die OVE E 8101 verweist. Bis zur Entscheidung bleiben beide Felder
`None` (inert, kein Fehlalarm).

**`arbeitsplatz_lux` (§4.4.1: 10 % der Nennbeleuchtungsstärke, mind. 15 lx).** Der Wert
ist belegt, aber das `RaumModell` kennt keinen Raumtyp „Arbeitsplatz mit besonderer
Gefährdung" — ohne Auslöser wäre der Wert toter Code. Track C (@polatselman); dieselbe
Lücke hält `sonderstellen.yaml` als `besondere_gefaehrdung` fest.

### Nebenbefund — Anhang B

Anhang B (A-Abweichungen) führt Frankreich, Italien, Deutschland und die Niederlande.
**Für Österreich gibt es keine Abweichung** — die EN-Werte oben gelten hier unverändert.
Relevant, weil Deutschland für §4.2.6/§4.3.6 abweichend 15 s festlegt; das gilt für
Österreich ausdrücklich nicht.

## 2c. Korrektur — §4.1.2 nennt sehr wohl ein Lux-Niveau (2026-09-01)

Der bis dahin **wichtigste offene fachliche Punkt** („Lux-Niveau an hervorgehobenen
Stellen — §4.1.2 belegt die Pflicht, nicht den Wert") ist geprüft. **Ergebnis: die
Annahme war falsch.** §4.1.2 nennt den Wert, in zwei seiner elf Punkte:

> **h)** nahe (siehe ANMERKUNG 1) jeder Erste-Hilfe-Stelle, **so dass 5 lx vertikale
> Beleuchtungsstärke am Erste-Hilfe-Kasten erreicht werden**;
>
> **i)** nahe (siehe ANMERKUNG 1) jeder Brandbekämpfungs- und Meldeeinrichtung, **so
> dass 5 lx vertikale Beleuchtungsstärke an den Melde-, den
> Brandbekämpfungseinrichtungen und der Anzeigen der Brandmeldeanlage erreicht
> werden**;

Fundstelle: `knowledge/_extracted_text/normen/EN 1838 - Notbeleuchtung 2019.txt`,
Norm-S.9 (PDF-Seite 11). ANMERKUNG 1 definiert „nahe" als „üblicherweise ein Abstand
von nicht mehr als 2 m in der Horizontalen".

### Was das ändert

| Typ | vorher | jetzt |
|---|---|---|
| `feuerloescher` | `norm_wert: null`, `MANUELL_PRUEFEN`, 5 lx nur als LB-Wert | **5 lx belegt** (§4.1.2 i), vertikal |
| `hydrant` | dito | **5 lx belegt** (§4.1.2 i), vertikal; nur die Zuordnung „Wandhydrant = Brandbekämpfungseinrichtung" bleibt AUSLEGUNG |
| `erste_hilfe` | `norm_wert: null`, `MANUELL_PRUEFEN` | **5 lx belegt** (§4.1.2 h), vertikal |
| `brandmelder` | dito | **5 lx belegt** (§4.1.2 i), vertikal |
| `niveauaenderung` | `norm_ref: MANUELL_PRUEFEN`, `beleg: LB` | **Auslöser belegt** (§4.1.2 c), **Lux weiterhin offen** |

Die reale Elektro-LB §5.1.23 nennt denselben Wert — sie **wiederholt** die Norm, sie
begründet sie nicht. Die Hierarchie bleibt unberührt: weicht eine LB ab, übersteuert
sie den Norm-Default.

### Was sich NICHT ändert — die Bezugsfläche

Der Wert ist **vertikal am Gerät**, nicht horizontal am Boden. Der Lux-Nachweis der
Engine (`platzierung/lux.py::lux_raster`) rechnet ausschließlich **horizontal**.
Ein vertikaler Norm-Wert dort als `min_lux` einzusetzen wäre derselbe Kategorienfehler
wie Ud gegen Uo (Abschnitt 2b). Deshalb:

- `SonderstellenKatalog.norm_lux_vertikal(typ)` → `5.0` für die vier Typen
- `SonderstellenKatalog.norm_lux_horizontal(typ)` → **immer** `None`
- `SonderstellenKatalog.norm_lux_bezugsflaeche(typ)` → `"vertikal"`
- in `platzierung_regeln.yaml` heißt der Schlüssel `min_lux_vertikal_norm`, nicht
  `min_lux` — er kann also nicht versehentlich in den Bodenraster laufen

Die alte Methode `norm_lux()` wurde **entfernt**, nicht umgewidmet: ein Name ohne
Achse war genau die Einladung zum Fehler.

### Warum es zuerst übersehen wurde

Die Prüfung am 31.08. stützte sich auf `_port_source/emergency_lighting_en1838.yaml`
(`en1838_antipanic_disabled_toilets` u.a.) statt auf den Volltext; die Extraktion
führt §4.1.2 verkürzt und ohne die Buchstaben h)/i). Lehre für die Quellenarbeit:
**die Extraktion ist ein Index, kein Beleg** — belegt wird am Volltext.

### Nebenbefund — §4.1.2 c)

§4.1.2 listet **b) Treppen** und **c) „jede andere Niveauänderung"** als getrennte
Punkte. Die frühere Notiz („unsere Extraktion nennt Treppen, die reale LB nennt
Niveauänderungen") ist damit ebenfalls erledigt: beide stehen in der Norm, die LB
deckt sich mit ihr. `RZ-06` und `SL-04` sind von `beleg: LB` / `decision_source:
lb_explizit` auf `BELEGT` / `norm_default` gezogen; ihr Lux-Wert bleibt offen.

## 3. Fehlt — kostenlos beschaffbar
1. **AStV, ASchG, KennV inkl. Anhang 1** als amtliche RIS-Ausdrucke (Gesetzesnummern s.o.).
2. Kommentierte AStV der Arbeitsinspektion (nur verlinkt).
3. **OVE-Richtlinie R 12-2** — von RL 2-Erl S.48 ausdrücklich als Anforderungsquelle zitiert; im Repo nur ein Bildausschnitt (`knowledge/extracted/bildlehren/beispiel_OVE_R12-2_Bild8-9.jpg`).
4. Landesbaurecht, das die OIB-Richtlinien verbindlich macht (Verbindlichkeitsanker).

## 4. Fehlt — kostenpflichtig
0. **ÖNORM B 1800:2013-08-01** „Ermittlung von Flächen und Rauminhalten von
   Bauwerken und zugehörigen Außenanlagen" — **blockiert aktiv den OIB-Resolver.**
   Die OIB-Begriffsbestimmungen definieren die Netto-Grundfläche nicht selbst,
   sondern verweisen auf diese Norm (Stichwort „Grundfläche", Norm-S. 7 /
   PDF-S. 9); die Ausgabe 2013-08-01 ist in „Zitierte Normen und sonstige
   technische Regelwerke" (Norm-S. 2 / PDF-S. 4) festgelegt. Ohne sie sind die
   Tabelle-6-Schwellen **3.200 m² (Zeile 2)** und **200 m² (Zeile 10)** nicht
   verifizierbar → beide Zeilen bleiben `review_required`. Von allen fehlenden
   Dokumenten das mit dem unmittelbarsten Effekt: eine Norm schaltet zwei
   Tabellenzeilen frei.
1. **ÖNORM EN 1838:2025-03-01** — Nachfolgeausgabe der Kernnorm; laut den
   Hersteller-Digests mit platzierungsrelevanten Änderungen.
2. **OVE/ÖVE EN 50172** (2024-11-01) — in EN 1838 §4.1.1 normativ verwiesen **und**
   in RL 2-Erl S.48 gemeinsam mit EN 1838 als Ausführungsanforderung genannt ⇒
   Pflicht-Baustein, nicht optional.
3. Nachrangig: TRVB E 102, TRVB B 108, ÖNORM EN ISO 7010.
