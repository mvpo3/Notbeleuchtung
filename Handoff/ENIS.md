# Handoff — Enis (Normwissen + LB)

> Claude: Du bist die Session von **Enis**. Owner-Package:
> `src/notbeleuchtung/normwissen/`. GitHub `@EnisAMG`.
> Lies zuerst `CLAUDE.md`, `docs/CONTRACTS.md`, `docs/ONBOARDING.md` (Abschnitt Enis).

## Stand (2026-09-05, Tagesende)

### Wiedereinstieg in 60 Sekunden
1. **`origin/main` = `5e4a46e`.** Alles von heute ist entweder drauf oder liegt
   als offener PR.
2. **Ein eigener PR ist gemergt:** **#103** (Sonderstellen-Quellen + Korrekturen)
   als `680676f` — ohne fremdes Review, 22 Minuten nach dem Öffnen.
3. **Zwei eigene PRs sind offen, beide mit @mvpo3 als Reviewer:**
   - **#109** `enis/sonderstellen-nachzug-0905` (`f4ffd84`) — §4.3.8 nur belegte
     Toiletten, RZ an Niveauänderung nur mit LB, Prüfregeln 12b/12c.
     **Enthält Änderungen in Leonis' Lane.**
   - **#110** `enis/wegbreite-randstreifen-0905` (`c964ca2`) — §4.2.1 Wegbreite/
     Mittelbereich + §4.3.1 Randstreifen quellengebunden. Reine eigene Lane.
   Beide CI grün, `mergeStateStatus: CLEAN`.
4. **Nur noch ein Blocker:** das Scope-Gate der Flächen-Schwellen (Blocker 2).
   Blocker 1 (Sonderstellen-Contract, #93) und Blocker 3 (40/10-Docstrings, #87)
   sind mit den Merges erledigt.
5. **Der wichtigste offene fachliche Befund** ist der Audit-Trail: die
   Sonderstellen-Leuchten tragen weiter die Fallback-Quelle (§4.1/§4.2.1/§4.3.1)
   statt der echten Fundstelle. Behebbar nur über die 3-Owner-Naht — ausgearbeitet
   in `docs/proposals/SONDERSTELLEN_QUELLEN_NAHT.md` (liegt auf dem #109-Branch).

### 🔴 MORGEN ZUERST

```
1. git fetch origin
2. git log --oneline -1 origin/main        # zuletzt: 5e4a46e
3. gh pr view 109 --json state,reviewDecision
4. gh pr view 110 --json state,reviewDecision
5. gh pr list --state open --limit 10
```

1. **Reviews zu #109 und #110 nachhalten.** Bei #109 ist die Auslegungsfrage
   BAD/DUSCHE/NASSRAUM/SANITÄR offen — bewusst nicht still entschieden.
2. **3-Owner-Vorschläge einbringen**, sobald #109/#110 durch sind:
   - `SONDERSTELLEN_QUELLEN_NAHT.md` (Bump **1.2.0 → 1.3.0**, Ports + zwei
     Contract-Typen) — löst den Audit-Trail-Befund.
   - `WEGBREITE_RANDSTREIFEN.md` (`FluchtwegSegment.breite_mm`, `raum_modell`
     **1.1.0 → 1.2.0**) — löst den fehlenden Eingabewert für §4.2.1.
3. **Blocker 2** weiterverfolgen: Gate je Schwelle (8 m² Nutzungsart-Scope auf
   Raum-Ebene, 60 m² Verkehrsbauwerk-Merkmal).
4. Ohne GO: restliche **§4.1.2-Punkte d), e), f), g), j), k)** am Volltext gegen
   die Decision-Matrix prüfen.

## Was heute auf `main` gelandet ist

**Eigen (#103, `680676f`):** Sonderstellen-Anforderungen mit echter Fundstelle,
`SonderstellenAnforderung` + `LuxAnforderung` (normwissen-eigene Typen),
`NormRegelwerk.quellen` um §4.1.2 c)/h)/i), §4.3.8, §4.4.1 erweitert (rein
additiv), vier Seitenangaben korrigiert, RZ-06 in der Matrix auf `lb_explizit`.

**Fremd, für meine Lane relevant:**

| PR | Inhalt | Folge |
|---|---|---|
| **#93** | `RaumModell` v1.1.0 — Sonderstellen Option A | Blocker 1 zu |
| **#87** | `NormRegelwerk` v1.2.0 + OIB-Naht, `FlaechenSchwellen.quelle` | Blocker 3 zu; Feld bereit, **bleibt leer** bis das Scope-Gate stimmt |
| **#96** | `PlatzierungsErgebnis` v1.2.0 — Symbol-Datenmodell | keine Berührung |
| **#105–#108** | Neuschnitte der gestrandeten Konsumptions-PRs (Symbol-Datenmodell, Sonderstellen, OIB-Gate, Verdichtung/Photometrie) | siehe Prüfung unten |

**Contract-Versionen auf `main`:** `norm_regelwerk` **1.2.0** · `raum_modell`
**1.1.0** · `platzierung_ergebnis` **1.2.0** · `oib_ergebnis` **1.1.0**.

## Prüfung von #106 gegen die eigenen Befunde (05.09., nachmittags)

Geprüfte Stände: #106 Head `2a216ee` / Merge `62ac276` · #107 `a368b41`/`bf42852`
· #108 `4c57667`/`5e4a46e`.

| Befund | Stand nach #106–#108 | wodurch |
|---|---|---|
| 5-lx-Nachweis unsichtbar | **behoben** — Prüfregel 12 kippt den Status auf `warnung` | #106 (`77214b3`) |
| §4.4.1-Nachweis unsichtbar | **behoben** — Prüfregel 12b | #106 |
| Audit-Trail falsche Fundstelle | **offen**, nur als Fallback gekennzeichnet (Docstring + `hinweise`) | — |
| §4.3.8 galt für jeden barrierefreien Raum | **auf `main` weiter offen** — Fix liegt in PR #109 (nicht gemergt) | eigener Nachzug |
| RZ an Niveauänderung als Norm-Default | **auf `main` weiter offen** — Fix liegt in PR #109 (nicht gemergt) | eigener Nachzug |
| 12b ohne Bezugsfläche · 2-m-Test art-blind | **auf `main` weiter offen** — Fix liegt in PR #109 (nicht gemergt) | eigener Nachzug |

**#107** berührt keinen dieser Punkte; `flaechen_schwellen` bleiben `None`.
**#108** stellt den Fluchtweg-Nachweis auf die **Mittellinie (§4.2.1, horizontal
am Boden)** um — es ermöglicht **keinen** vertikalen Nachweis. Die geprüfte
Bezugsfläche bleibt ausschließlich der Boden.

**#106 nutzt die Prototyp-API nicht** (kein `fuer_sonderstelle`, kein `getattr`,
kein paketübergreifender Import) — die Quellen-Naht ist damit weiter der offene
Schritt.

## Die zwei offenen eigenen PRs

### #109 — Nachzug zu #103 (`f4ffd84`, CI grün)

Drei Platzierungs-/Berichtsfehler, unabhängig von der Quellen-Naht behebbar.
**Solange der PR offen ist, gilt auf `main` weiterhin der alte Stand** — die
Punkte unten beschreiben, was der PR ändert, nicht was schon wirkt:

* **§4.3.8 dreiwertig:** `eindeutig` (WC, TOILETTE) → Antipanik ·
  `mehrdeutig` (SANITAER, SANITÄR, BAD, DUSCHE, NASSRAUM) → **keine** Automatik,
  dafür **Prüfregel 12c** · `ausserhalb` (z.B. ZIMMER) → Regel greift nicht.
  Beide Auswertungen (normwissen + platzierung) bilden denselben Scope ab.
* **Kein automatisches Norm-RZ** an einer Niveauänderung: nur bei
  `LBVorgabe.rz_stellen` mit `niveauaenderung`, dann mit `lb_quelle` und leerer
  `norm_quelle` (Muster `lb_override`).
* **Regel 12b** nennt die Bezugsfläche **Arbeitsfläche**; **2-m-Test** prüft die
  zugeordnete Leuchtenart statt einer beliebigen Nachbarleuchte.

⚠️ **Enthält Dateien aus Leonis' Lane** (`platzierung/sonderstellen_strategy.py`,
`platzierer.py`) — im Modul-Docstring und im PR-Text als Review-Bitte markiert.
Offene Auslegungsfrage im Review: ob BAD/DUSCHE/NASSRAUM/SANITÄR künftig anders
behandelt werden sollen.

### #110 — Wegbreite und Randstreifen (`c964ca2`, CI grün)

Reine eigene Lane. `geometrie`-Abschnitt in `en1838_grundwerte.yaml` +
`weg_nachweis(breite_mm)` → `regime = mittellinie | breiter_weg | unbestimmbar`,
`antipanik_randstreifen_mm()`, `hat_at_abweichung()`. Kein geratener Default für
die Wegbreite, keine Vorwegnahme der Planer-Entscheidung bei > 2 m, keine doppelte
Zahlenpflege (Anteile rechnen auf `lux.rettungsweg`).

## 📐 §4.2.1 / §4.3.1 / Anhang B — am Original geprüft (05.09.)

| Größe | Wortlaut | Fundstelle |
|---|---|---|
| **Mittellinie** | „Bei Rettungswegen mit einer Breite **bis zu 2 m** … mindestens 1 lx" | §4.2.1 S. 1, Norm-S. 9 |
| **Mittelbereich** | „nicht weniger als der **Hälfte der Breite** … mindestens **50 % dieses Wertes**" | §4.2.1 S. 2, Norm-S. 9 |
| **Breitere Wege** | „**können** als mehrere 2 m breite Streifen … **oder** mit Antipanikbeleuchtung" | §4.2.1 S. 3, Norm-S. 9 |
| **Randstreifen** | „0,5 lx … im **Kernbereich** … Randbereiche mit einer Breite von **0,5 m** nicht berücksichtigt" | **§4.3.1**, Norm-S. 11 |

Drei Merksätze: die **2 m sind ein Geltungsbereich**, kein Planungsmaß · Satz 3
ist eine **KANN-Aussage mit zwei Wegen** (Planer-Entscheidung) · der
**Randstreifen gehört zu §4.3.1**, nicht zu §4.2.1.

**Anhang B** (Norm-S. 16–17): FR, IT, DE, NL — **für Österreich keine
A-Abweichung**; keine Abweichung berührt die 2-m-Grenze. Die französischen
Sonderregeln (≤ 15 m Leuchtenabstand, 5 lm/m²) gelten nur dort.

**Offen dazu** (in `WEGBREITE_RANDSTREIFEN.md`): die Engine prüft den
2-m-Geltungsbereich nicht, leitet die Breite aus der Bounding-Box ab und
schreibt `rand_mm` im Docstring §4.2.1 statt §4.3.1 zu. Der fehlende Eingabewert
ist eine **belegte Wegbreite je Fluchtweg-Abschnitt**.

## Veröffentlicht am 05.09.2026 — sieben Reviews

Alle auf dem jeweils geprüften Head-SHA, Head unmittelbar vor dem Posten
verglichen (keine Abweichung, nichts zurückgestellt).

| PR | Votum | Head-SHA | Kern |
|---|---|---|---|
| #93 | **APPROVED** → **gemerged** | `55b767f3` | Sonderstellen Option A, 1:1 nach Spec, additiv |
| #96 | **APPROVED** → **gemerged** | `ad96bd44` | Symbol-Datenmodell, formal sauber, fremde Lane |
| #95 | **CHANGES_REQUESTED** | `909a424f` | falsche Quellenzuordnung + unsichtbarer Nachweis |
| #87 | COMMENT (keine Freigabe) → **von @mvpo3 gemerged** | `72ee052c` | Contract-Text korrekt, aber Gate-Scope offen |
| #88 | COMMENT | `a6bc97fc` | nicht mergefähig; #88 nie ohne #92 mergen |
| #92 | COMMENT | `4f504e07` | nicht mergefähig; projektweite Gate-Öffnung offen |
| #98 | COMMENT | `c2a30a29` | nicht mergefähig (Renderer-Konflikt aus #102) |

**Warum #87 nur ein Kommentar war:** ein Approve gilt auf GitHub als Freigabe.
Der Contract-Text ist fachlich richtig, aber das Gate trifft den Geltungsbereich
der Schwellen nicht (s. Blocker 2). **#87 wurde trotzdem gemerged** — das ändert
nichts an der Sachlage: das Feld `FlaechenSchwellen.quelle` steht jetzt bereit,
gefüllt wird es erst, wenn das Scope-Gate stimmt.

## PR #103 — der Normwissen-Slice (**gemergt** als `680676f`)

**https://github.com/mvpo3/Notbeleuchtung/pull/103**, Branch
`enis/review-3owner-0905`, veröffentlicht auf Head **`a296e77`**:

| Commit | Inhalt |
|---|---|
| `0504030` | Sonderstellen tragen ihre eigene Norm-Fundstelle (Befund an #95) |
| `93ce6f5` | Korrektur-Slice: Geltungsbereich, Bezugsfläche, Belegtiefe |
| `a296e77` | Handoff-Zwischenstand + SPEC §8 |
| `9809079` | **lokal:** Merge von `origin/main` (`26742ed`) in den Branch — kein Rebase, kein Force-Push |

**Kein Contract berührt:** kein Feld, kein Schema, keine `CONTRACT_VERSION`.
Auf `main` steht `NormRegelwerk` seit dem Merge von #87 auf **1.2.0**; unser
Slice lässt sie unverändert. `scripts/gen_schema.py` erzeugt keine Änderung.

### Was der Slice liefert

- `data/sonderstellen.yaml`, Abschnitt `norm_anforderung`: je Auslöser
  Klassifikation, **echte** Fundstelle, Bezugsfläche und ein `symbol_wie`, das
  Katalog-Keys und Montagehöhe aus einer bestehenden Raumregel **leiht** —
  EN 1838 schreibt für eine hervorzuhebende Stelle weder Symbol noch Höhe vor.
- `SonderstellenAnforderung` + `LuxAnforderung` (normwissen-eigene Typen) und die
  Query-Methoden `fuer_sonderstelle`, `zur_pruefung`, `fuer_raum_attribut`.
- `NormRegelwerk.quellen` zusätzlich §4.1.2 c)/h)/i), §4.3.8, §4.4.1 — rein
  additiv, `quellen` ist ein `list[str]`: mehr Einträge sind **Daten**.

## 📌 GESICHERTES NORMWISSEN — geprüft, NICHT neu recherchieren

> Übernommen aus dem Tagesabschluss vom 02.09. (Commit `6b43ab2`, dort
> erarbeitet). Am 05.09. gegen das **Original-PDF** gegengeprüft — die
> Aussagen unten haben Bestand; die Seitenangaben und die h)/i)-Zuordnung
> stehen korrigiert im nächsten Abschnitt.

Volltext im Repo: `knowledge/_extracted_text/normen/EN 1838 - Notbeleuchtung 2019.txt`.
Volle Prüftabellen: `docs/NORMQUELLEN_AT.md` Abschnitte **2b** und **2c**.

### Gleichmäßigkeit

| Größe | Wert | Fundstelle | Status |
|---|---|---|---|
| **Ud Rettungsweg** | **1:40** („darf 1 : 40 entlang der Mittellinie des Rettungsweges nicht unterschreiten") | **§4.2.2**, Norm-S.10 | auf `main`, gefüllt als `gleichmaessigkeit_max = 40` (max:min) |
| **Ud Antipanik** | **1:40** („darf 1 : 40 nicht unterschreiten") — **derselbe Wert**, wortgleicher Satz | **§4.3.2**, Norm-S.11 | auf `main`, `gleichmaessigkeit_max = 40` |
| **Uo Arbeitsplätze mit besonderer Gefährdung** | **≥ 0,1** | **§4.4.2** | **bewusst NICHT gefüllt** |

> **Uo ist nicht Ud.** Ud = kleinste : größte, Uo = kleinste : mittlere (beide
> EN 12665). Die kursierende Angabe „40 Rettungsweg / **10** Antipanik" verwechselt
> beides: die 10 ist der Kehrwert von Uo ≥ 0,1 aus §4.4.2 und gehört zu einem
> **anderen Anwendungsfall** und einer **anderen Größe**. Sie darf nie als Ud = 10
> in `gleichmaessigkeit_max` landen. Zwei Tests nageln das fest
> (`test_antipanik_ud_ist_40_nicht_10`,
> `test_uo_aus_4_4_2_landet_nicht_in_gleichmaessigkeit_max`).

Für Aufheller/Betonungsleuchten (§4.1) nennt EN 1838 **keine** eigene Ud → kein
Wert, `None`, der Konsument bleibt bei seinem Default.

### Umschaltzeit — zweistufig

| Stufe | Wert | Fundstelle |
|---|---|---|
| **Halbwert** | 50 % der geforderten Beleuchtungsstärke **innerhalb 5 s** | §4.2.6 / §4.3.6 / §5.4.6 |
| **Vollwert** | 100 % **innerhalb 60 s** | §4.2.6 / §4.3.6 / §5.4.6 |
| Arbeitsplätze mit besonderer Gefährdung | dauernd vorhanden **oder innerhalb 0,5 s** | §4.4.6 |

Das Contract-Feld `NormAnforderung.umschaltzeit_max_s` ist ein **Skalar** und kann
deshalb nur den **60-s-Vollwert** abbilden — der steht auf `main`. Die 5-s-Stufe
lebt als `umschaltzeit.halbwert_s` in `en1838_grundwerte.yaml`, damit die
Norm-Aussage nicht verloren geht. **Ob die Halbwertstufe ein eigenes Contract-Feld
bekommt, ist eine 3-Owner-Frage — offen.**

### Flächen-Schwellen — bleiben `None`

`NormRegelwerk.flaechen_schwellen.antipanik_min_m2` und `.wc_sanitaer_min_m2` sind
**bewusst leer** (= inert). Die Werte existieren, stehen aber **nicht in EN 1838**
— die vorliegende Ausgabe kennt überhaupt keine flächenbezogene Auslöse-Schwelle
(§4.3.8 nennt Toiletten für Menschen mit Behinderung **ohne** Flächenmaß).

| Wert | Fundstelle | Geltungsbereich im Original |
|---|---|---|
| **8 m²** Sanitärbereiche | **OVE E 8101:2019 `718.560.9.001.AT` 1)** („in Sanitärbereichen ab 8 m2 Größe und in barrierefreien WC-Anlagen"); wortgleich ÖVE/ÖNORM E 8002-1 Punkt 1); OVE E 8101:2025 gleichlautend | nur „für Räume, Anlagen oder Gebäude, an die **erhöhte Anforderungen nach der Art der Nutzung** (OVE-Richtlinie R 12-2 bzw. **OIB-Richtlinie 2**) gestellt werden" |
| **60 m²** | OVE E 8101:2019 / ÖVE/ÖNORM E 8002-1 **Punkt 3)** | **nur Flughäfen und Bahnhöfe** (Wartezonen, Abfertigungshallen, Geschäftsflächen, Arbeitsräume) |
| **60 m²** (allgemeiner Satz) | ÖVE/ÖNORM E 8002-1 **§3.2.2.1.2** | nur eine **ANMERKUNG** in einer Begriffsbestimmung (informativ), zusätzlich relativiert durch „oder bei kleineren Flächen, sofern … ein erhöhtes Risiko besteht" |

> **Die 60 m² dürfen nicht global angewendet werden.** Normativ sind sie an den
> Nutzungsscope Flughafen/Bahnhof gebunden; der allgemeine Satz ist bloß eine
> ANMERKUNG. `platzierung/flaechen_strategy.py::_ist_flaechen_antipanik` wirkt
> dagegen **auf jeden Raum**. Ein Füllen würde die Norm über ihren
> Geltungsbereich hinaus anwenden und den Auslöser im Audit-Trail unter
> `norm_quelle = "ÖNORM EN 1838:2013 §4.3.1"` führen, obwohl er aus OVE stammt.

**Vorschlag (offen, s. Blocker 2):** den Trigger über den bereits vorhandenen
**`OibRl2Provider`** gaten — der bewertet genau die „erhöhten Anforderungen nach
der Art der Nutzung". Damit wären die **8 m² sauber freischaltbar**; die 60 m²
brauchen zusätzlich ein Nutzungsmerkmal (Verkehrsbauwerk) oder bleiben Auslegung.
Festgehalten in `test_flaechen_schwellen_bleiben_ohne_en_1838_beleg_leer`.

`arbeitsplatz_lux` (§4.4.1: 10 % der Nennbeleuchtungsstärke, mind. 15 lx) bleibt
ebenfalls leer — ohne Raumtyp „Arbeitsplatz mit besonderer Gefährdung" im
`RaumModell` wäre der Wert toter Code (Track C, @polatselman).

### §4.1.2 — die hervorzuhebenden Stellen

**5 lx sind ein EN-1838-Wert** — und zwar als **vertikale** Beleuchtungsstärke:

> **h)** nahe jeder Erste-Hilfe-Stelle, **so dass 5 lx vertikale
> Beleuchtungsstärke am Erste-Hilfe-Kasten erreicht werden**;
> **i)** nahe jeder Brandbekämpfungs- und Meldeeinrichtung, **so dass 5 lx
> vertikale Beleuchtungsstärke an den Melde-, den Brandbekämpfungseinrichtungen
> und der Anzeigen der Brandmeldeanlage erreicht werden**;

Belegt für `feuerloescher`, `hydrant`, `erste_hilfe`, `brandmelder`. Die reale
Elektro-LB §5.1.23 **wiederholt** den Wert nur; weicht eine LB ab, übersteuert sie
(LB-explizit > Norm-Default).

> **Vertikal und horizontal müssen getrennt bleiben.** Die 5 lx gelten **am
> Gerät** (vertikal); der Lux-Nachweis der Engine (`platzierung/lux.py::lux_raster`)
> rechnet **horizontal am Boden**. Ein Einsetzen als `min_lux` wäre derselbe
> Kategorienfehler wie Ud gegen Uo. Deshalb trägt die Query-API die Achse im
> Namen: `norm_lux_vertikal()` → 5.0 · `norm_lux_horizontal()` → **immer `None`**
> · `norm_lux_bezugsflaeche()` → `"vertikal"`. Die alte achslose `norm_lux()` ist
> **entfernt**, nicht umgewidmet. In `platzierung_regeln.yaml` heißt der Schlüssel
> `min_lux_vertikal_norm`.

**Niveauänderungen sind in §4.1.2 ausdrücklich genannt** — b) „nahe Treppen" und
c) „nahe jeder anderen Niveauänderung" sind **zwei getrennte Punkte**. Die frühere
Annahme („die Norm nennt nur Treppen, die Niveauänderung kommt aus der LB") ist
widerlegt. `RZ-06-NIVEAUAENDERUNG` und `SL-04-NIVEAUAENDERUNG` stehen jetzt auf
`beleg: BELEGT` / `decision_source: norm_default`; ihr **Lux-Wert bleibt offen**,
weil c) — anders als h)/i) — **kein** Beleuchtungsniveau nennt.

„nahe" = ANMERKUNG 1: „üblicherweise ein Abstand von nicht mehr als **2 m** in der
Horizontalen".

### Anhang B — keine österreichische Abweichung

Anhang B (A-Abweichungen) führt **Frankreich, Italien, Deutschland, Niederlande**.
**Für Österreich gibt es keine Abweichung** — alle EN-Werte oben gelten hier
unverändert. Relevant, weil Deutschland für §4.2.6/§4.3.6 abweichend **15 s**
festlegt; das gilt für Österreich **ausdrücklich nicht**.

### Arbeitsregel, die aus dem 01.09. folgt

**Die Extraktion ist ein Index, kein Beleg.** Der 5-lx-Irrtum entstand, weil die
Prüfung am 31.08. gegen `_port_source/emergency_lighting_en1838.yaml` lief statt
gegen den Volltext; die Extraktion führt §4.1.2 verkürzt und ohne die Buchstaben
h)/i). Ab jetzt: **immer am Volltext belegen.** Und: **Zahl und Größe zusammen
prüfen** — zwei Fehler desselben Typs an einem Tag (Ud gegen Uo, vertikal gegen
horizontal). Die richtige Zahl in der falschen Größe ist ein Fehler.

## 📌 Fachliche Korrekturen vom 05.09. — am ORIGINAL-PDF geprüft

Original: `knowledge/EN 1838 - Notbeleuchtung 2019 (1).pdf`, Kopfzeile
**„EN 1838:2013 (D)"**. Die Textextraktion ist **Suchhilfe, kein Beleg** — auch
die EN-1838-Datei nicht.

| Punkt | Befund | Norm-Seite |
|---|---|---|
| **h) vs. i)** | **h) = Erste-Hilfe-Stelle**, **i) = Brandbekämpfungs- UND Meldeeinrichtung**. Feuerlöscher, Wandhydrant und Brandmelder gehören zu **i)** | S. 9 |
| **§4.3.8** | „Antipanikbeleuchtung ist in **Toiletten** für Menschen mit Behinderung erforderlich" — raumtyp-gebunden, das Flag `ist_barrierefrei` allein genügt nicht | S. **11** (nicht 12) |
| **§4.4.1** | Wartungswert **auf der Arbeitsfläche**, 10 % der Aufgaben-Beleuchtungsstärke, mind. 15 lx — **nicht** pauschal horizontal, **nicht** der Boden | S. **12** (nicht 13) |
| **§4.1.2 c)** | belegt die **Sicherheitsleuchte**, nicht das Rettungszeichen. Die Einleitung von §4.1.2 verlangt an den aufgezählten Stellen Sicherheitsleuchten; d) verlangt nur, dass **vorhandene** Zeichen beleuchtet werden | S. 8 |
| **§4.2.1** | „Breitere Rettungswege können als mehrere 2 m breite Streifen betrachtet werden oder mit Antipanikbeleuchtung ausgerüstet werden" — Grundlage für den offenen Wegbreiten-Punkt | S. 9 |

Folgen in der Matrix (`platzierung_regeln.yaml`): **RZ-06** von
`norm_default`/`BELEGT` auf **`lb_explizit`/`LB`** korrigiert (ohne LB keine
RZ-Pflicht an einer Niveauänderung), **SL-04** bleibt Norm-Default; SL-10/SL-11
mit korrigierten Seitenangaben. **`engine_status` überall unverändert
`input_fehlt`.**

## 🔌 Offene Schnittstelle — die neuen APIs sind PROTOTYPEN

> Zwei Prototypen, an **verschiedenen Orten** — das ist beim Lesen wichtig:
>
> | Prototyp | Methoden | wo er liegt |
> |---|---|---|
> | **Sonderstellen** | `fuer_sonderstelle`, `zur_pruefung`, `fuer_raum_attribut` + `SonderstellenAnforderung`/`LuxAnforderung` | **auf `main`** (mit #103 gemergt, `680676f`) |
> | **Geometrie** | `weg_nachweis`, `antipanik_randstreifen_mm`, `hat_at_abweichung` + `WegNachweis` | **nur in PR #110** (`c964ca2`), **nicht** auf `main` |
>
> **Beide sind trotzdem nicht angebunden:** keine der Methoden steht im
> `ports.NormProvider`-Protocol. Dass der Sonderstellen-Prototyp auf `main`
> liegt, heißt nur, dass er dort **existiert** — konsumiert wird er von niemandem
> (`platzierung` ruft ihn nicht auf, siehe Prüfung von #106).

Der Sonderstellen-Prototyp ist seit #103 auf `main`, der Geometrie-Prototyp liegt
in PR #110. Beide stehen **nicht** im `ports.NormProvider`-Protocol und sind nur
intern + in Tests zu verwenden.

**Keine Lösung sind:** ein `getattr(norm, "fuer_sonderstelle", …)` aus
`platzierung` (stille Kopplung an eine ungeprüfte Signatur — ein Methodenzugriff
ersetzt keine vereinbarte Schnittstelle) und ein Import von `normwissen` in ein
fremdes Paket (Owner-Grenze, CLAUDE.md).

Der ausformulierte 3-Owner-Vorschlag steht in
`docs/SPEC_SONDERSTELLEN_CONTRACT.md` **§8** (auf `main`): Contract-Typen
(`SonderstellenAnforderung`, `LuxAnforderung`), drei Methodensignaturen und die
vollständige Auswirkungsliste — Version-Bump **1.2.0 → 1.3.0** (eindeutig, seit
#87 gemergt ist), Schema-Regen, `tests/fakes.py::FakeNormProvider` um drei
Methoden, und der Nachzug von `tests/fixtures/norm_regelwerk_snapshot.json`
(3-Owner-Lane, führt weiter nur die drei alten `quellen`-Strings).

**Keiner der beiden Vorschläge ist umgesetzt.** Die zwei Dokumente
`docs/proposals/SONDERSTELLEN_QUELLEN_NAHT.md` (auf dem **#109**-Branch) und
`docs/proposals/WEGBREITE_RANDSTREIFEN.md` (auf dem **#110**-Branch) liegen beide
noch nicht auf `main`; die darin vorgeschlagenen Contract-Erweiterungen
(`norm_regelwerk` 1.2.0 → 1.3.0 bzw. `raum_modell` 1.1.0 → 1.2.0) sind weder
angewendet noch 3-Owner-freigegeben.

## 📋 Anschlussauftrag für Leonis (@mvpo3)

> **Stand Tagesende:** Punkte 2–4 und 6 sind in **PR #109 umgesetzt — der PR ist
> aber offen, auf `main` wirkt davon nichts** (teils in seiner Lane, deshalb die
> Review-Bitte). Offen bleibt darüber hinaus Punkt 1: die Umstellung auf die
> vereinbarte Schnittstelle.

1. **Nicht** duck-typed anbinden — erst der 3-Owner-PR nach SPEC §8, dann
   konsumieren.
2. Für eine Sonderstelle die Anforderung **des Auslösers** verwenden, nie die
   erste Raumregel der Leuchtenart (das war der Befund an #95).
3. `fuer_raum_attribut` immer **mit `raum_typ`** rufen. Eine leere Liste heißt
   „§4.3.8 greift hier nicht" — **nicht** „kein Licht": Raumtyp-Regel,
   Fluchtweg und Flächen-Trigger gelten unabhängig weiter.
4. Lux nur über die achs-gebundenen Zugriffe; **nur** `lux_horizontal_boden` darf
   in `lux_raster`.
5. `zur_pruefung()`-Kandidaten nur setzen, wenn eine LB sie deckt — dann mit
   `lb_quelle`, nie mit `norm_quelle`.
6. **Prüfregel für `nachweis_offen`** ergänzen (vier Gerätetypen, Niveauänderung,
   `besondere_gefaehrdung`). Der Text steht in `nachweis_offen_grund`.

**Die Quellen sind jetzt korrekt zugeordnet — der lichttechnische Nachweis ist
damit nicht erbracht.** Ohne Punkt 6 meldet ein unvollständiger Plan weiterhin
`ok`. Und: **die Quellen schalten nichts automatisch frei** — `engine_status`
bleibt `input_fehlt`. #93 **und** die Konsumption sind seit dem 05.09. auf `main`
(#95 wurde nicht gemergt, sondern als **#106** neu geschnitten — mit meinen
Review-Punkten teilweise eingearbeitet). Was noch fehlt, ist der Nachweis **je
Regel**, getrennt nach Platzierung und Lichttechnik. Erst dann wird
`engine_status` regelweise gezogen — nicht pauschal.

## 🧪 Testprotokoll 05.09.2026

| Lauf | Commit | passed | skipped | deselected |
|---|---|---|---|---|
| Baseline `origin/main` | `b954b60` | 565 | 7 | 2 |
| nach Slice 1 | `c0ca778` (vor Rebase) | 591 | 7 | 2 |
| nach Korrektur-Slice | `d77ac30` (vor Rebase) | 599 | 7 | 2 |
| gezielte Regression `tests/normwissen/ tests/contract/ tests/platzierung/test_platzierer.py` | `d77ac30` | 321 | 0 | 0 |
| gezielte Regression, PR-Stand | `93ce6f5` | 321 | 0 | 0 |
| volle Suite, PR-Stand (rebased auf `674b8bc`) | `93ce6f5` | 599 | 7 | 2 |
| Contract + Normwissen nach Merge von `26742ed` | `9809079` | 314 | 0 | 0 |
| volle Suite nach Merge von `26742ed` | `9809079` | 599 | 7 | 2 |
| volle Suite, PR #103 final | `ebdda73` | 599 | 7 | 2 |
| Baseline `origin/main` nach #104–#108 | `5e4a46e` | 648 | 7 | 2 |
| **PR #109** (Nachzug) | **`f4ffd84`** | **671** | **7** | **2** |
| **PR #110** (Wegbreite/Randstreifen) | **`c964ca2`** | **663** | **7** | **2** |

`scripts/gen_schema.py` erzeugt in allen Läufen keine Änderung (Schema in sync).

**`ruff check .` — ein Befund, nicht aus dieser Lane:** `scripts/render_architektur.py:86`
meldet `C408 Unnecessary dict() call`. Die Datei kam mit `674b8bc` (Leonis'
Architektur-Diagramm) auf `main`; `origin/main` ist damit aktuell **nicht**
ruff-clean. Unsere Dateien sind es:
`ruff check src/notbeleuchtung/normwissen/ tests/normwissen/` → All checks passed.
An @mvpo3 gemeldet gehört das noch.

**CI-Historie zum C408 (erledigt):** `Lint` läuft im Workflow **vor** der
Testsuite. Solange der C408-Befund auf `main` lag, brach der Job `test` ab, bevor
ein Test lief — auf `main` (Run `33962252577`) wie auf #103 (Run `33962392314`).
Das war **kein** rotes Testergebnis, sondern gar keines. Mit `87db889`
(`bbox=dict(...)` → Dict-Literal) ist es behoben; seither sind alle Läufe grün.

**CI-Stand am Tagesende — beide PRs grün, deckungsgleich mit lokal:**

| PR | Commit | contracts | test | CI-Zahl |
|---|---|---|---|---|
| #109 | `f4ffd84` | pass (57 s) | pass (2 m 32 s) | 671 / 7 / 2 |
| #110 | `c964ca2` | pass (1 m 2 s) | pass (2 m 43 s) | 663 / 7 / 2 |

**Die 7 Skips einzeln** (Umgebung, nicht Code): 2 × `tests/hauptengine/
test_dwg_input.py` (ODA File Converter auf diesem Mac nicht installiert) · 5 ×
`tests/raumerkennung/*` (`Projekte/Mollgasse Notbeleuchtung/WHA_MOL_EG.dxf` liegt
lokal nicht vor — der Ordner enthält nur einen PNG-Screenshot; die Mollgasse-E2E
laufen, sie nutzen `Projekte/Mollgasse/*.dxf`).
**Die 2 deselected:** `addopts = "-m 'not visual'"` aus `pyproject.toml`.

### PR-Prüfstände der sieben Reviews

| PR | Head-SHA | eigene Basis | Merge-Probe gegen `main` |
|---|---|---|---|
| #87 | `72ee052c` | 530 / 5 / 2 | **konfliktfrei** → 565 / 7 / 2 |
| #88 | `a6bc97fc` | 545 / 5 / 2 | Konflikt (via Stack) |
| #92 | `4f504e07` | 557 / 5 / 2 | **Konflikt**: `pipeline.py`, `api/main.py`, `COORDINATION.md` |
| #93 | `55b767f3` | 537 / 5 / 2 | **konfliktfrei** → 565 / 7 / 2 |
| #95 | `909a424f` | 574 / 5 / 2 | **Konflikt** (dieselben drei Dateien) |
| #96 | `ad96bd44` | 546 / 5 / 2 | **konfliktfrei** → 565 / 7 / 2 |
| #98 | `c2a30a29` | 591 / 5 / 2 | **Konflikt** + `render/dxf_renderer.py` |

(Format: passed / skipped / deselected. Auf den älteren PR-Basen sind es 5 Skips,
weil die beiden ODA-Tests dort noch nicht existieren.)

## ✔ Blocker 1 — Sonderstellen-Contract: ERLEDIGT

**#93 ist am 05.09. gemerged** (`4c66c20`). `RaumModell` v1.1.0 mit
`sonderstellen[]`, `ist_barrierefrei` und `besondere_gefaehrdung` liegt auf
`main`. Mein Approval stand auf `55b767f3`.

Nach dem Merge **nicht** automatisch freischalten: `engine_status` der acht
Regeln wird erst gezogen, wenn auch die Konsumption (#95) drin ist und der
Nachweis **je Regel einzeln** vorliegt — Platzierung und lichttechnischer
Nachweis getrennt bewertet.

## 🚧 Blocker 2 — Scope-Gate: OFFEN (einziger verbleibender Blocker)

Seit dem Merge von #87 existiert `FlaechenSchwellen.quelle` im Contract — das
ändert an der Sachlage nichts: **beide Flächen-Schwellen bleiben leer**, auch die
8 m². `flaechen_schwellen` und `engine_status` sind unverändert.

| Schwelle | Geltungsbereich im Original | vom Gate abgedeckt? |
|---|---|---|
| 8 m² Sanitär | „erhöhte Anforderungen nach der Art der Nutzung" (OVE R 12-2 / OIB-RL 2) | inhaltlich ja, **aber** die Raum-Ebene stimmt nicht (s.u.) |
| 60 m² | **nur Flughäfen/Bahnhöfe** (OVE E 8101:2019 Punkt 3); der allgemeine Satz in E 8002-1 §3.2.2.1.2 ist eine **ANMERKUNG** | **nein** |

Zwei getrennte Gründe, **nicht gekoppelt**:

1. **Raum-Ebene / gemischte Nutzung.** `oib_gate.freigegebene_raeume` (#92) gibt
   „alle Räume" zurück, sobald **einem** bestätigenden Gebäudeteil die
   `raum_referenzen` fehlen. OIB-RL 2 Punkt 5.4 wörtlich: „Bei Gebäuden bzw.
   Bauwerken mit jeweils gemischter Nutzung gelten die für die jeweilige Nutzung
   anzuwendenden Anforderungen." Also je Nutzung, nicht projektweit. **Sobald das
   sitzt, sind die 8 m² freischaltbar — unabhängig von der 60-m²-Frage.**
2. **Nutzungsmerkmal für die 60 m².** `ProjektKontext.Nutzungsart` kennt
   `VERKEHRSEINRICHTUNG`, `oib_rl2_tabelle6.yaml` führt sie unter
   `review_nutzungsarten` (Tabelle 6 hat keine Zeile dafür, Bundeszuständigkeit)
   → Stufe `review_required` → Gate **zu**. Das Gate ist für die 60 m² also nicht
   nur zu grob, sondern für den einzigen belegten Fall gesperrt. Vorschlag: ein
   zweites, nutzungsart-basiertes Signal (die Nutzungsart steht bereits in
   `OibErgebnis.eingangswerte["nutzungsart"]`, dort aber nur als Audit-Dict).

## ✔ Blocker 3 — 40/10-Docstrings: ERLEDIGT

`platzierung/lux.py` war bereits korrigiert; `hauptengine/contracts/
norm_regelwerk.py` ist es mit dem **Merge von #87** (`9fff6e1`). Die Angabe
„40 Rettungsweg / 10 Antipanik" steht damit an keiner Stelle mehr im Code.

## ERLEDIGT am 01.09.2026 — Track-B-Norm-Werte (PR #83, **gemerged** `cfcbbde`)

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
+ Scope-Tabelle der AT-Quellen), COORDINATION-Log 01.09.

## ERLEDIGT am 01.09.2026 — Korrektur: §4.1.2 nennt 5 lx (vertikal)

Der bis dahin wichtigste offene fachliche Punkt, geprüft — mit umgekehrtem
Ergebnis. **§4.1.2 h)** fordert „so dass 5 lx vertikale Beleuchtungsstärke am
Erste-Hilfe-Kasten erreicht werden", **§4.1.2 i)** dasselbe an Melde- und
Brandbekämpfungseinrichtungen und den Anzeigen der Brandmeldeanlage. Damit ist der
Wert für **feuerloescher · hydrant · erste_hilfe · brandmelder** normativ; die
Elektro-LB §5.1.23 wiederholt ihn nur.

**Was bleibt und was der eigentliche Punkt ist:** der Wert ist **vertikal am
Gerät**, `lux_raster` rechnet **horizontal am Boden**. Deshalb trägt die Query-API
die Achse im Namen — `norm_lux_vertikal()` = 5.0, `norm_lux_horizontal()` = `None`,
`norm_lux_bezugsflaeche()` = `"vertikal"`; die alte achslose `norm_lux()` ist
**entfernt**, nicht umgewidmet. In der Matrix heißt der Schlüssel
`min_lux_vertikal_norm`, damit er nicht in den Bodenraster laufen kann.

**Nebenbefund, ebenfalls erledigt:** §4.1.2 führt b) Treppen und c) „jede andere
Niveauänderung" getrennt auf → `RZ-06` und `SL-04` von `beleg: LB` /
`lb_explizit` auf `BELEGT` / `norm_default` gezogen, Lux dort weiter offen.

**Warum es am 31.08. übersehen wurde:** die Prüfung stützte sich auf
`_port_source/emergency_lighting_en1838.yaml` statt auf den Volltext; die
Extraktion führt §4.1.2 verkürzt und ohne die Buchstaben h)/i).
**Regel ab jetzt: die Extraktion ist ein Index, kein Beleg.**

Geändert: `sonderstellen.yaml` · `sonderstellen.py` · `platzierung_regeln.yaml`
(SL-04…SL-08, RZ-06) · 3 Tests umgedreht + 3 neue · `NORMQUELLEN_AT.md` **2c** ·
`SPEC_SONDERSTELLEN_CONTRACT.md` §3.

## Historie 02.09. — Blocker 1 (3-Owner-GO Sonderstellen)

> **Überholt:** #93 liegt vor und hat mein Approval, es fehlt @polatselman.
> Aktueller Stand oben. Der Text bleibt als Begründungs-Historie stehen.

Unverändert seit 31.08. PR #69 hat **0 Reviews, 0 Kommentare**; zweite
Entscheidungsbitte steht im COORDINATION-Log vom 01.09. — ebenfalls ohne Reaktion.

**Empfohlen: Option A** — generisches `RaumModell.sonderstellen[]` (Feuerlöscher ·
Wandhydrant · Erste-Hilfe-Stelle · Brandmelder · Niveauänderung) plus
`ist_barrierefrei` (§4.3.8) und `besondere_gefaehrdung` (§4.4.1) auf `Raum`. Rein
additiv, alle Felder mit Default, schaltet **exakt** die 8 blockierten
Placement-Regeln frei. Ohne sie bleibt jeder erzeugte Plan in diesem Punkt
unvollständig, **ohne dass man es der Ausgabe ansieht**.

**Durch die 5-lx-Korrektur ist der Vorschlag stärker geworden:** vier der fünf
Typen tragen jetzt einen **belegten Norm-Wert** (5 lx vertikal, §4.1.2 h/i) statt
eines Review-Flags. `besondere_gefaehrdung` ist zugleich die Voraussetzung dafür,
dass das seit v1.1.0 existierende Contract-Feld `arbeitsplatz_lux` überhaupt einen
Auslöser bekommt — die beiden Themen hängen zusammen.

Bis zum GO wird `hauptengine/contracts/**` von Track B nicht angefasst.

## Historie 02.09. — Blocker 2 (Scope-Gate Flächen-Schwellen)

> **Verschärft:** auch die 8 m² bleiben leer, und die beiden Schwellen sind
> nicht gekoppelt. Aktueller Stand oben.

Offen seit 01.09. `flaechen_schwellen` wirkt im Contract **global**, die belegten
Werte sind es nicht (Tabelle oben). Solange kein Gate entschieden ist, bleiben
beide Felder `None` und `_ist_flaechen_antipanik` ist inert — kein Fehlalarm, aber
auch kein Nutzen.

**Vorschlag liegt vor:** Gating über den vorhandenen `OibRl2Provider`. Erste
Ausbaustufe wären die **8 m²** (Scope deckt sich exakt), die **60 m²** erst mit
einem Nutzungsmerkmal „Verkehrsbauwerk".

## Historie 02.09. — Blocker 3 (40/10-Docstrings)

> **Halb erledigt:** `platzierung/lux.py` ist auf `main` korrigiert; der
> Contract-Docstring kommt mit #87. Aktueller Stand oben.

Die Angabe „EN 1838: 40 Rettungsweg / 10 Antipanik" steht weiterhin in:

| Fundstelle | Eigentümer |
|---|---|
| `hauptengine/contracts/norm_regelwerk.py`, Docstring `NormAnforderung.gleichmaessigkeit_max` | 3-Owner (CODEOWNERS) |
| `platzierung/lux.py`, Docstring `ud_min_aus_norm` + Modul-Docstring | Leonis |
| COORDINATION-Eintrag 01.09. (Leonis) und PR-Text #72/#81 | Leonis |

Beides **nicht** in Enis' Lane → gemeldet, nicht angefasst. Meldung liegt als
Kommentar an PR #81 (`#issuecomment-5500891064`) und im COORDINATION-Log.
**Folgepunkt: nachhalten, dass @mvpo3 es korrigiert.** Der Code ist korrekt — nur
die Doku lügt, und sie ist die Stelle, an der der nächste Leser den Fehler wieder
aufnimmt.

## ⚠️ Prozess — Approvals in der `normwissen`-Lane

`src/notbeleuchtung/normwissen/` ist per CODEOWNERS Enis' Lane. Ohne
Enis-Approval durchgegangen: **#14, #22, #23, #40**. Dazu:

- **#72** hob `hauptengine/contracts/norm_regelwerk.py` auf v1.1.0, war im eigenen
  PR-Text als „braucht 3-Owner-Approval" deklariert und trägt **ein** Approval
  (@polatselman), gemerged von @mvpo3. Genau dieser PR transportierte die vier
  Quellen-Fehler.
- **#83** (Enis' eigener PR) wurde **12 Minuten** nach Erstellung von @mvpo3
  gemerged — **0 Reviews, 0 Kommentare**. Inhaltlich in Ordnung (CI grün, Leonis
  hat den Regress separat verifiziert), aber die erbetene Durchsicht aus fremder
  Lane hat nicht stattgefunden.

Sachlicher Team-Punkt, keine technische Frage; im COORDINATION-Log vom 01.09.
festgehalten. **Bleibt offen.** Nichts davon wird zurückgedreht.

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

- ~~**Die 5 lx an Feuerlöscher/Wandhydrant sind KEIN pauschaler EN-1838-Normwert.**~~
  **Am 01.09. am Volltext widerlegt und korrigiert.** §4.1.2 **h)** und **i)**
  fordern ausdrücklich „so dass **5 lx vertikale Beleuchtungsstärke** … erreicht
  werden" — am Erste-Hilfe-Kasten bzw. an Melde- und Brandbekämpfungseinrichtungen.
  Der Wert ist für vier der fünf Typen **normativ**, die LB §5.1.23 wiederholt ihn
  nur. Die alte Entscheidung beruhte auf einer unvollständigen Extraktion.
  **Was bleibt:** der Wert ist **vertikal am Gerät**, der Lux-Nachweis der Engine
  rechnet **horizontal am Boden** — deshalb `norm_lux_vertikal()` = 5.0 und
  `norm_lux_horizontal()` = `None`, festgenagelt. Ohne Lux-Wert bleibt nur
  `niveauaenderung` (§4.1.2 c) nennt keinen). Details: `docs/NORMQUELLEN_AT.md` 2c.
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

## Offene Punkte (Stand 02.09., ergänzt 05.09.)

> Die Punkte zu Sonderstellen-Quellen, §4.1.2 c)/h)/i) und den
> Flächen-Schwellen sind oben aktualisiert; hier steht der ältere Stand.
- 🚧 **3-Owner-GO für den Sonderstellen-Contract** — siehe Blocker 1.
- 🚧 **Scope-Gate für `flaechen_schwellen`** — siehe Blocker 2.
- 🚧 **40/10-Docstrings** in `contracts/norm_regelwerk.py` und `platzierung/lux.py`
  — siehe Blocker 3. Gemeldet an @mvpo3, Korrektur nachhalten.
- **PR #84** (Leonis, `abstand-nachpass`) ist der nächste Integrationspunkt: er
  läuft als Nachpass in `platzierer.place` und ändert
  `tests/e2e/test_mollgasse_eg_durchstich.py`. **Wenn er die Referenz
  15 RZ + 21 SL / Prüfstatus `ok` / 7 Befunde verschiebt, hier nachziehen** — sie
  ist die Vergleichsbasis für die Inertheit der Track-B-Werte.
- ✔ **Track-B-PR #83** — am 01.09. gemerged (`cfcbbde`, Squash, @mvpo3),
  Track B ist auf `main` **aktiv**.
- **`umschaltzeit_max_s` bildet nur eine Stufe ab** — die Norm ist zweistufig
  (50 % in 5 s, 100 % in 60 s). Die 5-s-Stufe hat kein Contract-Feld; ob sie eins
  bekommt, ist eine 3-Owner-Frage. Bis dahin steht sie nur in der YAML.
- ✔ **Lux-Niveau an hervorgehobenen Stellen** — am 01.09. erledigt: §4.1.2 h)/i)
  nennen 5 lx **vertikal**. Siehe `docs/NORMQUELLEN_AT.md` 2c.
- ✔ **Niveauänderung** — am 01.09. erledigt: §4.1.2 c) nennt sie ausdrücklich.
- **Restliche §4.1.2-Punkte** (d, e, f, j, k) am Volltext gegen die Matrix prüfen.
- **`stair_exit` fehlt** in der Raumerkennung → blockiert `RZ-05`/`RZ-07`
  (@polatselman).
- **Quellenlage** OVE R 12-2 / OVE E 8350 / TRVB E 102 (nur Nennung, kein Volltext)
  · `vorschriftenkurzuebersicht-at.pdf` ist AES-verschlüsselt, nicht auswertbar.
- **Wegbreite > 2 m / Randstreifen 0,5 m** (§4.2.1/§4.3.1, Anhang B) nicht
  modelliert — **wichtigster offener fachlicher Punkt**. `lux_raster` hat bereits
  `rand_mm=500`, aber ohne Norm-Ref.
- **`tests/fixtures/lb/fischa_lb.txt`** trägt weiterhin die falsche Quellenzuordnung
  (3-Owner-Lane, bewusst nicht angefasst) — mit Leonis zu klären.
- **ÖNORM B 1800:2013-08-01** beschaffen → schaltet Tabelle-6-Zeilen 2 und 10 frei.
- Weiter offen: AStV/ASchG/KennV als RIS-Volltext, EN 1838:2025-03,
  EN 50172:2024-11; 4 Norm-Werte für Wohnungs-Fluchtweg ratifizieren.
- **Prozess:** `normwissen/` ist per CODEOWNERS Enis' Lane; #14, #22, #23, #40,
  **#72** und **#83** gingen ohne fremdes Review durch — siehe Abschnitt
  „Prozess" oben. Bleibt offen.
- **Aufräumbar:** alle `enis/*`-Branches sind inhaltlich in `main`
  (`enis/norm-trackB-werte` per Squash, deshalb kein Ancestor — Inhalt am
  02.09. gegen `origin/main` verifiziert: Diff leer). Der lokale Ref
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
