# RaumModell 1.5.0 — eindeutig zugeordneter Stand

**Für:** @EnisAMG · **Von:** Selman (`raumerkennung`) · **Erstellt:** 2026-09-12

Dieses Dokument ist zum **Nachrechnen** gedacht. Jede Zahl trägt ihre Quelle und
den Commit-SHA, auf dem sie erhoben wurde. Wo ich etwas **nicht** gemessen habe,
steht das als solches — nicht als Bestätigung.

**Ab hier gilt:** jede Kennzahl in der Doku wird mit dem Erhebungs-SHA
gekennzeichnet; ältere Angaben ohne Neumessung sind als veraltet zu behandeln.

---

## 1. Zuordnung: Branch, PR, Commit

| Angabe | Wert |
|---|---|
| Branch | `selman/extents-ausreisser` |
| PR | **#155** (offen, kein Merge) |
| **Commit, der `CONTRACT_VERSION` auf `1.5.0` setzt** | **`6ebf676b116ae61dac57ec15022ead5e22970f5a`** |
| Datum dieses Commits | 2026-09-12 02:17:40 +0200 |
| Titel | „raumerkennung — Raumueberlappungen nicht destruktiv bereinigen (Contract raum_modell 1.5.0)" |
| Messstand dieses Dokuments | **`91ad7ccfa0a1638490c9605f929f8d8b145b016a`** |

Der Sprung 1.4.0 → 1.5.0 ist additiv: `Raum.polygon_roh` (Ring **vor** der
Bereinigung), `Raum.bereinigung[]` (jeder Abzug mit Regel und Gegenspieler),
Literal `BereinigungsRegel`. `polygon_mm` trägt seither den **bereinigten**
Stand — wer eine Kennzahl auf Raumpolygonen gemessen hat, muss sagen, auf
welchem.

Nachgeprüft, nicht angenommen: `git log -S'CONTRACT_VERSION = "1.5.0"'` liefert
genau diesen einen Commit.

> **Hinweis zur Ehrlichkeit:** die Messungen unten laufen auf dem Arbeitsbaum
> über `91ad7cc`. Dieser Baum trägt die noch nicht committeten Änderungen der
> Runde vom 2026-09-12 (Balkontüren-Regel, Belegkorrekturen). Am Contract ändert
> davon **nichts** — `CONTRACT_VERSION` steht unverändert auf `1.5.0`.

## 2. Die 62 Überlappungen: welche Projekte, welche Geschosse

| Plan | Projekt | Geschoss |
|---|---|---|
| `Barawitzka_EG` | Barawitzkagasse | Erdgeschoss |
| `Mollgasse_EG` | Mollgasse | Erdgeschoss |
| `Muthgasse_E2` | Muthgasse 109B | Geschoss **E2 = 2. Obergeschoss** |
| `Rennweg_EG` | Rennweg | Erdgeschoss |
| `Rennweg_OG3` | Rennweg | 3. Obergeschoss |

> **Befund zu Muthgasse_E2, der über dieses Dokument hinausgeht:**
> `geschoss_aus(None, "Muthgasse_E2.dxf")` liefert `""`, also gilt der Plan im
> Code als **Erdgeschoss**, obwohl er das 2. Obergeschoss ist. `plan_pruefen`
> macht daraus `or "EG"`. Betroffen sind **41 von 62** Korpusplänen. Folge:
> `ausgaenge.py` lässt dort `final_exit` zu, aktuell 5. Das ist eine
> Owner-Entscheidung (der Fix am Geschoss-Regex verschiebt die Ausgangszahlen
> vieler Pläne, und „E2" ist mehrdeutig: Etage oder Baufeld), deshalb **nicht**
> eigenmächtig geändert.

### Regel für Regel, je Plan

Gemessen mit `scripts/analyse/ueberlappung_regeln.py` (nur lesend) auf den
eingecheckten Ergebnissen, Stand `91ad7cc`. Kumulativ, „gelöst" = gegenüber
Stufe `{}`:

| Plan | `{}` | `{1}` | `{1,2}` | `{1,2,3}` | `{1,2,3,4}` | `{1..5}` | doppelt belegt am Ende |
|---|--:|--:|--:|--:|--:|--:|--:|
| Barawitzka_EG | 9 | 9 | 9 | 5 | **0** | 0 | 0,05 mm² |
| Mollgasse_EG | 16 | 16 | 16 | 12 | **0** | 0 | 0,14 mm² |
| Muthgasse_E2 | 37 | 36 | 36 | 31 | **2** | 2 | 2 552 357,00 mm² |
| Rennweg_EG | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 mm² |
| Rennweg_OG3 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 mm² |
| **Summe** | **62** | **61** | **61** | **48** | **2** | **2** | **2,552 m²** |

Doppelt belegte Fläche gesamt: **262,342 m² → 2,552 m²**.

Zwei Dinge, die man in dieser Tabelle sehen sollte:

- **Regel 2 (Restfläche) löst in keinem Plan einen einzigen Fall** — die Spalte
  `{1,2}` ist überall gleich `{1}`. Sie ist Vorsorge, im Bestand ohne Wirkung.
- **Regel 4 trägt die Hauptlast**: 53 × `QUELLE_RANG` und 29 × `STEMPEL_NAEHE`
  über alle Pläne. Regel 3 löst 14, Regel 1 genau eine (der verschluckte LIFT),
  Regel 5 nur Mikroflächen.

Buchungen im vollen Lauf: `QUELLE_RANG` 53 · `STEMPEL_NAEHE` 29 · `ZERFALL` 16 ·
`ENTHALTENSEIN` 6 · `SCHWERPUNKT` 5 · `ENTFALL` 5 · `LIFT_SCHACHT` 1 ·
`SCHLITZ` 1 · `RESTFLAECHE` **0**.

Die verbleibenden 2 Überlapper / 2,552 m² sind **ein** Paar, bewusst offen
gelassen: der Stempelschutz der Regel 3 lässt `raum_29` (quelle L, Stempel
16,52 m², Rang 1) nicht gegen `raum_91` (quelle F, Rang 3) ausstanzen, weil der
Raum dadurch um 15,4 % vom Stempelwert abwiche.

## 3. BT1-EG (Fischamenderstraße) — NEUE MESSUNG

Vor diesem Lauf lag für BT1-EG **kein Ergebnis auf 1.5.0** vor; der Plan ist
nicht in der Prüfstrecke. Das Verzeichnis `Projekte/_ergebnis_bt1_eg/` war leer
(ein früherer Versuch dieser Session war abgebrochen, bevor er schrieb).

**Das ist eine neue Messung, keine Rekonstruktion eines früheren Laufs.**
**Ausschließlich Raumerkennung** — keine Platzierung, keine Pipeline, deshalb
ausdrücklich **nicht** `scripts/plan_pruefen.py`, sondern der Provider direkt.

| Angabe | Wert |
|---|---|
| Eingabe | `Projekte/BVH Fischamenderstraße/fertige Elektromontagepläne/BT1/Elektromontageapläne_ERDGESCHOSS BT1.dxf` |
| **SHA-256 der Eingabe** | **`d1fc3b0b762609d1c445a29c6229c6b0f403eb7cd3d3d7ec83e44a3eba848107`** |
| Größe | 31 523 707 Bytes |
| **Commit-SHA** | `91ad7ccfa0a1638490c9605f929f8d8b145b016a` |
| **Exakter Aufruf** | `ArchitekturRaumProvider().parse('Projekte\BVH Fischamenderstraße\fertige Elektromontagepläne\BT1\Elektromontageapläne_ERDGESCHOSS BT1.dxf', 'EG')` |
| Laufzeit | 19,5 s |
| **Ablage** | `Projekte/_ergebnis_bt1_eg/raummodell.json` + `messung.md` |
| `contract_version` im Modell | **`1.5.0`** |

Zur Identifikation: es gibt zwei DXF mit „ERDGESCHOSS BT1" im Namen. Gewählt ist
der **Elektromontageplan** aus Enis' Diagnose; der zweite Kandidat
(`260320_938-AR-PP-11000-A_ERDGESCHOSS BT1.dxf`) ist der Architekturplan und
nicht gemeint.

### Kennzahlen des Laufs

| Kennzahl | Wert |
|---|--:|
| Räume | 72 |
| Türen | 225 |
| davon typisiert | 192 |
| Fluchtweg-Segmente | 87 |
| **Wandkörper** | **0** |
| Ausgänge | `stair_exit` 1 · `final_exit` 3 |

Raumtypen: ZIMMER 14 · KÜCHE 12 · GANG 8 · BAD 6 · WC 6 · VORRAUM 6 ·
TERRASSE 5 · ohne Typ 5 · ABSTELLRAUM 4 · BALKON 2 · GARAGE 1 · STIEGENHAUS 1 ·
KINDERWAGENRAUM 1 · LIFT 1.

Zwei Befunde, die ich nicht glätte:

- **0 Wandkörper.** Der Plan ist ein Wrapper-Plan (Block `65465465`, Faktor 1000
  bei `$INSUNITS` 6); die Wände stecken in Blockdefinitionen. Räume und Türen
  entstehen trotzdem, Wandkörper nicht.
- **Die 3 `final_exit` hängen NICHT an Freiflächen.** Der Plan trägt 7
  Freiflächen-Räume (5 TERRASSE, 2 BALKON) und 20 `balkontuer`, davon **0 mit
  AUSSEN-Seite**. Die neue Balkon-Regel greift hier also in null Fällen, und
  `exit_tuer_87`, `exit_tuer_97`, `exit_aussenoeffnung_1` bleiben unberührt —
  eine unabhängige Gegenprobe auf einem sechsten Plan.

## 4. Die fünf entfallenen Räume

Entfall-Kriterium: Restkörper unter 1 m² nach dem Ausstanzen (dasselbe wie
`kaskade.py:115`). **Nichts wird gelöscht** — Roh-Polygon, Stempel und
Regelkette stehen in `raeume.json` unter der Top-Level-Liste `entfallen`.

| Raum | Projekt / Geschoss | Stempel-Name (Typ) | Fläche roh | Stempelwert | Restkörper | Regeln |
|---|---|---|--:|--:|--:|---|
| `raum_44` | Barawitzkagasse EG | „Loggia" (BALKON) | 4,88 m² | 5,31 m² | 0,224 m² | `QUELLE_RANG` |
| `raum_82` | Muthgasse 109B E2 | „Wohnküche" (KÜCHE) | 19,88 m² | 51,32 m² | 0,361 m² | `QUELLE_RANG` |
| `raum_86` | Muthgasse 109B E2 | „Wohnküche" (KÜCHE) | 43,66 m² | 41,25 m² | 0,939 m² | `ENTHALTENSEIN`, `QUELLE_RANG` |
| `raum_92` | Muthgasse 109B E2 | „Wohnküche" (KÜCHE) | 20,73 m² | 84,72 m² | 0,141 m² | `QUELLE_RANG` |
| `raum_93` | Muthgasse 109B E2 | „Wohnküche" (KÜCHE) | 8,04 m² | 5,74 m² | 0,085 m² | `QUELLE_RANG` |

Summe Restkörper: Barawitzka 0,224 m², Muthgasse 1,525 m². Vier der fünf sind
als `KÜCHE` typisierte F-Räume (Stempel-Flutung), die ganze Wohnungen
verschluckt hatten — ihr Stempelwert liegt bei drei von ihnen weit über der
Roh-Fläche (51,32 gegen 19,88 · 84,72 gegen 20,73), das Flutungs-Artefakt ist
also auch am Stempel ablesbar.

### Zeigt eine Referenz auf eine entfallene Raum-ID? **Nein.**

Geprüft über alle fünf Pläne: alle Raum-IDs, die in `bericht.md` vorkommen,
gegen die lebenden IDs aus `raeume.json` und die Entfall-Liste.

Gefunden: **5 Erwähnungen** entfallener IDs — und jede einzelne ist
Dokumentation, keine funktionale Zuordnung:

| Fundstelle | Art |
|---|---|
| Barawitzka `bericht.md` Z113 | Abschnitt „Entfallen durch Bereinigung (1)" |
| Muthgasse `bericht.md` Z200–203 | Abschnitt „Entfallen durch Bereinigung (4)" |
| Muthgasse `bericht.md` Z191 | Raumbereinigungs-Tabelle: `raum_86` als **Gegenspieler** der Buchung `ENTHALTENSEIN` von `raum_88` |

**Null** Treffer in der Tür-, Ausgangs-, Fluchtwegsegment-, Leuchten- oder
Wohnungstabelle. Die Erwähnung als Gegenspieler ist genau die Buchungsspur, die
der Contract verlangt (`bereinigung[]` mit Regel und Gegenspieler). Es gibt
also keine hängende Referenz und nichts zu beheben.

## 5. Herkunft der drei Kennzahlen

### 5a. Fenstererkennung „24 Öffnungen" — **neu gemessen, bestätigt**

Erhoben ursprünglich in § 4.5 der Übergabe. Erzeuger:
`fenster_signatur.finde_fensteroeffnungen`, ohne Provider-Lauf und **ohne
Raumzuordnung** — die Zahl hängt damit **nicht** an Raumpolygonen und ist von
1.5.0 unberührt.

Neu gemessen auf `91ad7cc`:

| Plan | Wandsegmente | Fensteröffnungen | Laufzeit |
|---|--:|--:|--:|
| Barawitzka_EG | 1 689 | **24** | 5,2 s |
| Mollgasse_EG | 930 | 0 | 4,7 s |
| Muthgasse_E2 | 3 155 | 0 | 15,5 s |
| Rennweg_EG | **0** | 0 | 1,5 s |
| Rennweg_OG3 | **0** | 0 | 2,8 s |

Die 1689 → 24 sind exakt reproduziert, ebenso die 0 Falschtreffer auf den vier
Vergleichsplänen. Die beiden Rennweg-Pläne mit **0 Wandsegmenten** sind der
Echtdaten-Beleg für Punkt 6: dort heißt die leere Antwort „nicht gesucht".

### 5b. Türauszählung „612 mit `STANDARDWERT` 0-mal" — **neu gemessen, verschoben**

Die 612 ist die **Türsumme über die fünf Pläne**, erhoben am 2026-09-10 per
Provider-Parse (§ 6 der Übergabe: 27 + 41 + 106 + 147 + 291). Sie ist **vor**
der Bereinigung erhoben, also veraltet.

Neu gemessen auf `91ad7cc`, `breite_quelle` über alle fünf Pläne:

| `breite_quelle` | § 6 (2026-09-10) | neu (`91ad7cc`) | Delta |
|---|--:|--:|--:|
| `BLOCKNAME` | 58 | **58** | 0 |
| `GEOMETRIE_SCHWENKRADIUS` | 104 | **104** | 0 |
| `GEOMETRIE_SUMME` | 2 | **2** | 0 |
| `GEOMETRIE_OEFFNUNG` | 368 | **347** | **−21** |
| `UNBEKANNT` | 80 | **83** | +3 |
| **`STANDARDWERT`** | **0** | **0** | 0 |

Drei der fünf Quellen sind **unverändert**. Bewegt hat sich nur
`GEOMETRIE_OEFFNUNG` um −21 — das sind die weggefallenen
Kontaktzonen-Durchgänge, also synthetische Wandöffnungen, keine echten Türen.
Dazu +3 `UNBEKANNT`.

Drei Zählbasen, die ich ausdrücklich **nicht** gegeneinander verrechne:

| Basis | Wert |
|---|--:|
| Türsumme § 6 (2026-09-10, vor der Bereinigung) | 612 |
| Nenner „Türen n/m typisiert" im Lauf `91ad7cc` | **591** |
| Zeilen der Türtabelle (`tuer_` + `durchgang_` + `aussenoeffnung_`) | **709** |

Die 709 zerlegt sich in `tuer_*` **286**, `durchgang_*` **407**,
`aussenoeffnung_*` **16**. Wer 612 und 709 vergleicht, vergleicht verschiedene
Mengen.

**`STANDARDWERT` kommt weiterhin 0-mal vor** — in keinem der fünf Berichte.
Das bestätigt Auflage B: der Wert hat keinen Erzeuger im Modell; der
Zeichen-Default lebt außerhalb (`dxf_renderer.py`).

### 5c. Breitenverlauf „287/307" — **NICHT neu gemessen**

Erhoben in § 10.4 (209/307 → 287/307 = 93,5 %). Erzeuger:
`raumerkennung/breitenprofil.py`, und die Messung läuft über Fluchtwegsegmente
**gegen schneidende Raumpolygone**. Damit hängt genau diese Zahl an dem, was
1.5.0 verändert hat — sie ist die kritischste der drei.

**Ich bestätige sie nicht.** Der **Zähler** (287 messbare Segmente) steht in
keinem Bericht — die Segmenttabelle trägt Fluchtweg-Gründe wie `exit`,
`long_run`, `direction_change`, `corner`, aber kein `flaeche_fehlt`. Er ist nur
über `miss_breitenprofil` gegen ein frisch geparstes Modell zugänglich, weil die
Segment-Polylinien ausschließlich im Modell liegen und in keiner Datei abgelegt
sind. Ein erster Versuch, ihn aus den Berichten zu zählen, war falsch (falsche
Spalte) und ist verworfen.

**Der Nenner ist dagegen messbar — und er hat sich verschoben.** Je Plan, § 10.4
gegen die Berichte auf `91ad7cc`:

| Plan | Nenner § 10.4 | Nenner `91ad7cc` | Delta |
|---|--:|--:|--:|
| Barawitzka_EG | 12 | **12** | 0 |
| Mollgasse_EG | 126 | **126** | 0 |
| Muthgasse_E2 | **155** | **148** | **−7** |
| Rennweg_EG | 9 | **9** | 0 |
| Rennweg_OG3 | 5 | **5** | 0 |
| **Summe** | **307** | **300** | **−7** |

Vier von fünf Plänen sind unverändert; die −7 sitzen vollständig in Muthgasse
und haben dieselbe Ursache wie die −21 bei den Türen (§ 5b): weggefallene
Kontaktzonen-Durchgänge.

**Damit ist der Bruch als Ganzes veraltet** — nicht weil der Zähler falsch wäre,
sondern weil sich seine **Grundmenge** geändert hat. Eine Aussage „93,5 %" auf
`91ad7cc` ist unbelegt, solange der Zähler nicht gegen die 300 neu gemessen ist.

**Status: Nenner neu gemessen (300), Zähler ausstehend.** Die Neumessung des
Zählers braucht Provider-Parses über alle fünf Pläne (Summe ~42 min) — sie ist
beauftragt, aber noch nicht gelaufen.

## 6. Deine Regel zur Belichtung — festgehalten und per Test gesichert

> *Fehlende Fenstererkennung allein begründet kein `False` bei
> `natuerlich_belichtet`; bei unvollständiger Grundlage bleibt es `None`.*

**Messstand `91ad7cc`: das Feld existiert nicht.** Zur Laufzeit geprüft —
`Raum.model_fields` führt `bereinigung`, `besondere_gefaehrdung`, `flaeche_m2`,
`id`, `ist_barrierefrei`, `ist_communal`, `ist_fluchtweg`, `nutzungsklasse`,
`polygon_mm`, `polygon_roh`, `raum_typ`, `wohnung_id`. `natuerlich_belichtet`,
`belichtung_quelle` und `belichtung_vollstaendigkeit` sind **Vorschlag**
(§ 4.4), und es gibt keinen Belichtungs-Code am `Raum`.

Deine Regel ist damit keine Absicherung eines bestehenden Verhaltens, sondern
eine **Vorgabe an den ersten Erzeuger** — dieselbe Bauform wie deine Auflage A
zu `lichte_quelle`. Umgesetzt in
`tests/raumerkennung/test_belichtung_grundlage.py` (2 passed, 1 xfailed):

1. **Contract-Wächter:** wird rot, sobald ein Belichtungsfeld eingeführt wird.
   Rot heißt dort nicht „Fehler", sondern: jetzt ist der Erzeuger da, also muss
   deine Regel mit umgesetzt werden. Ohne den Wächter könnte das Feld
   stillschweigend mit `False`-Default erscheinen.
2. **Die Regel dort, wo sie heute messbar ist:** `finde_rahmenfenster([])`
   liefert dasselbe wie eine Segmentliste ohne Fenstersignatur — eine leere
   Liste. „Nicht gesucht" und „nichts gefunden" sind damit nicht
   unterscheidbar; die Unterscheidung hängt an `wandsegmente(plan)`, das auf
   Rennweg EG und OG3 **0 Segmente** liefert (§ 5a). Wer daraus ein `False`
   macht, erfindet eine Messung.
3. **Zielbild als strict-xfail:** sobald das Feld existiert, muss bei
   unvollständiger Grundlage `None` herauskommen, nicht `False`.

Fachliche Deckung im Normteil ist vorhanden und unverändert:
`normwissen/data/astv_arbeitsstaetten.yaml` führt
`z1_nicht_natuerlich_belichtet` mit `heute_im_modell: false`, `status:
ungeprueft` und der Abgrenzung, dass fehlende Belichtung allein einen Raum
nicht zum Arbeitsraum macht (AStV § 1 Abs. 4).

---

## Was in diesem Dokument offen bleibt

1. **287/307** (§ 5c) — veraltet, Neumessung braucht einen
   `breitenprofil`-Lauf gegen ein frisch geparstes Modell.
2. **Der Geschoss-Befund** (§ 2) — `geschoss_aus` liefert für 41 von 62
   Korpusplänen kein Geschoss, Muthgasse_E2 läuft als „EG". Owner-Entscheidung.
3. **`raum_67` / `E2-VF-11b`** bleibt untypisiert bis zu deiner Entscheidung;
   der Prüfbericht weist das je Lauf aus.
4. **Die Notbeleuchtungsanforderung der `SCHLEUSE`** ist weiter offen
   (`regel_deckung.yaml`, Owner Enis) — entschieden ist nur die
   Erschließungslage.
