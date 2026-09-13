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
| Nachgemessen in § 5c | **`5ccdc27634c6d4bbff7c731452c83c72a2344220`** |

Der Sprung 1.4.0 → 1.5.0 ist additiv: `Raum.polygon_roh` (Ring **vor** der
Bereinigung), `Raum.bereinigung[]` (jeder Abzug mit Regel und Gegenspieler),
Literal `BereinigungsRegel`. `polygon_mm` trägt seither den **bereinigten**
Stand — wer eine Kennzahl auf Raumpolygonen gemessen hat, muss sagen, auf
welchem.

Nachgeprüft, nicht angenommen: `git log -S'CONTRACT_VERSION = "1.5.0"'` liefert
genau diesen einen Commit.

> **Hinweis zur Ehrlichkeit:** die Messungen der Abschnitte 2 bis 5b liefen auf
> dem Arbeitsbaum über `91ad7cc`, also vor dem Commit der Runde vom 2026-09-12
> (Balkontüren-Regel, Belegkorrekturen). Dieser Stand ist inzwischen als
> `e5b742c`…`5ccdc27` committet; die Zahlen sind davon unberührt, weil jene
> Commits weder Räume noch Türen noch die Bereinigung verändern. Die
> Nachmessung in § 5c lief auf **`5ccdc27`** und ist dort so ausgewiesen. Am
> Contract ändert die ganze Runde **nichts** — `CONTRACT_VERSION` steht
> unverändert auf `1.5.0`, und `git diff 91ad7cc..5ccdc27 -- contracts/` ist
> leer.

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

> **KORREKTUR 2026-09-13: die Zuordnung oben ist falsch — gemessen wurde der
> falsche Plan.** Enis' Diagnose gehört zum **Architekturplan**
> `260320_938-AR-PP-11000-A_ERDGESCHOSS BT1.dxf`, nicht zum Elektromontageplan.
> Belegt über seine IDs im eingecheckten Ergebnis
> `Projekte/_ergebnis_alle/260320_938-AR-PP-11000-A_ERDGESCHOSS BT1/`:
> `tuer_111` 1×, `tuer_121` 3×, `exit_tuer_121` 2× und **3 Selbstverbindungen**
> von 361 Türzeilen — genau seine vier Befunde. Im hier gemessenen
> Elektromontageplan existiert keine dieser IDs (höchste ist `tuer_98`) und es
> gibt 0 Selbstverbindungen. Meine Begründung „aus Enis' Diagnose" war eine
> Annahme, die ich nie geprüft habe; es gab zwei Kandidaten und ich habe den
> falschen genommen. **Folge: alle Zahlen dieses Abschnitts gelten für den
> Elektromontageplan und sind KEINE Antwort auf Enis' Befunde.** Der Lauf am
> richtigen Plan steht aus.

### Kennzahlen des Laufs

| Kennzahl | Wert |
|---|--:|
| Räume | 72 |
| Türen | 225 |
| davon typisiert | 192 |
| Fluchtweg-Segmente | 87 |
| **Wandkörper** | **241** (Korrektur 2026-09-13, hier stand **0** — s. u.) |
| Ausgänge | `stair_exit` 1 · `final_exit` 3 |

Raumtypen: ZIMMER 14 · KÜCHE 12 · GANG 8 · BAD 6 · WC 6 · VORRAUM 6 ·
TERRASSE 5 · ohne Typ 5 · ABSTELLRAUM 4 · BALKON 2 · GARAGE 1 · STIEGENHAUS 1 ·
KINDERWAGENRAUM 1 · LIFT 1.

Zwei Befunde, die ich nicht glätte:

- **~~0 Wandkörper.~~ KORREKTUR 2026-09-13: es sind 241.** Die 0 war ein
  Messfehler von mir, keine Eigenschaft des Plans: mein Skript zählte
  `len(getattr(modell, "wandkoerper", []) or [])` auf einem `RaumModell` — und
  der Contract führt dieses Feld **nicht** (Felder: `contract`,
  `contract_version`, `floor`, `coordinate_system`, `bounds_mm`, `raeume`,
  `tueren`, `ausgaenge`, `zirkulation`, `sonderstellen`, `stiegenhaeuser`,
  `anker`). Der `getattr`-Default greift, also ist die Zahl für **jeden** Plan 0,
  auch für Muthgasse mit 737. Wandkörper leben nur im `KaskadeErgebnis`, das der
  Provider nicht herausgibt.
  **Ist-Wert, selbst gemessen auf `3d91a2c`: 241 Wandkörper**, davon 195 direkt
  im Wrapper und 46 aus Blöcken, 210 auf dem Layer `A_Waende`. Auch die
  Begründung oben war falsch: die Wände liegen **doppelt dargestellt**
  (HATCH + Linienzug) auf einem Layer, überwiegend direkt im Wrapper-Block, und
  `finde_wandkoerper` steigt selbst ab. Gegenbeweis aus den eigenen Daten: die
  126 `durchgang_*`-Türen dieses Laufs entstehen ausschließlich im Zweig
  `if k.wandkoerper:` (`provider.py:132-135`) — mit 0 Wandkörpern gäbe es keine
  einzige davon. Die Gegenprobe über alle Pläne zeigt **keinen** Plan mit
  Wandkörper-Mangel (WK/Raum: Mollgasse 2,76 · BT1-EG 3,44 · Muthgasse 7,60 ·
  Rennweg_EG 9,14 · Rennweg_OG3 14,57 · Barawitzka 27,02). Festgeschrieben in
  `tests/raumerkennung/test_wandkoerper.py`.
- **Die 3 `final_exit` hängen NICHT an Freiflächen.** Der Plan trägt 7
  Freiflächen-Räume (5 TERRASSE, 2 BALKON) und 20 `balkontuer`, davon **0 mit
  AUSSEN-Seite**. Die neue Balkon-Regel greift hier also in null Fällen, und
  `exit_tuer_87`, `exit_tuer_97`, `exit_aussenoeffnung_1` bleiben unberührt —
  eine unabhängige Gegenprobe auf einem sechsten Plan.

## 3b. BT1-EG am RICHTIGEN Plan — Enis' Plan, Nachlauf 2026-09-13

Abschnitt 3 misst den Elektromontageplan. Enis' Diagnose gehört zum
**Architekturplan** (Beleg: seine IDs, siehe Korrektur in § 3). Dieser Abschnitt
holt die Messung dort nach, auf `3d91a2c`.

| Angabe | Wert |
|---|---|
| Eingabe | `Projekte/BVH Fischamenderstraße/BT1/260320_938-AR-PP-11000-A_ERDGESCHOSS BT1.dxf` |
| **SHA-256** | **`dd2e6e7d9908085678a8a0cbc26475c6c9217fcbafc5bcff54234c45305ca407`** |
| Größe | 11 717 404 Bytes |
| Commit-SHA | `3d91a2ceebb5e1a034feb4fa4faf5b7a3edf81b4` |
| Aufruf | `ArchitekturRaumProvider().parse(<pfad>, 'EG')`, ausschließlich Raumerkennung |
| Laufzeit | Wandkörper 6,7 s · Provider 19,7 s |
| Ablage | `Projekte/_ergebnis_bt1_arch/` |

| Kennzahl | Architekturplan | Elektromontageplan (§ 3) |
|---|--:|--:|
| **Wandkörper** | **270** (218 msp / 52 block) | **241** (195 / 46) |
| Räume | 79 | 72 |
| Türen | 256 | 225 |
| Fluchtweg-Segmente | 88 | 87 |
| Ausgänge | `stair_exit` 1 · `final_exit` 3 | `stair_exit` 1 · `final_exit` 3 |

Der Architekturplan ist **kein** Wrapper-Plan — `plan.space` ist der Modelspace,
Faktor 1000, ein Wand-Layer `A_Waende` (192 der 270 Körper; dazu `M-EQPM` 34,
`A-DETL-GENF_` 18, `A_2D` 8, `A-DETL-MBND` 7). Die Wandkörper-Erkennung hat also
auf **keinem** der beiden Pläne eine Lücke; die „0" war allein mein Messfehler.

### Enis' vier Befunde, an seinem Plan reproduziert

**1. Selbstverbindungen: 3 — bestätigt, und eine davon trägt einen Ausgang.**

| Tür | Räume | `tuer_detail` | Quelle |
|---|---|---|---|
| `tuer_121` | `raum_76` == `raum_76` | **`hauseingang`** | `text:EINGANG BT1` |
| `tuer_122` | `raum_70` == `raum_70` | — | `text:RWA Garage BT1 Abluft` |
| `tuer_124` | `rest_1` == `rest_1` | — | `text:RWA BT1 ER´s + KiWa` |

`tuer_121` wird zu **`exit_tuer_121`** (`final_exit`) verwertet. Gemeinsame
Ursache, gemessen: **alle drei entstehen aus Türtexten**, nicht aus Geometrie —
zwei davon aus `RWA`-Beschriftungen (Rauch- und Wärmeabzug), die keine Türen
sind. Im Elektromontageplan gibt es 0 Selbstverbindungen.

**2. Türdubletten: 38 Paare unter 50 mm, davon 36 bei genau 10,00 mm.** Auf
beiden Plänen identisch. Das Muster ist durchgehend dasselbe und **nicht**
„Block gegen Bogen": **beide Partner haben `quelle=block`**, einer mit
`BLOCKNAME`-Breite, der andere mit `UNBEKANNT`, gleiches `tuer_detail`, exakt
10 mm versetzt — etwa `tuer_2` (900 mm, BLOCKNAME) ↔ `tuer_73` (None,
UNBEKANNT), beide `wohnungseingang`. Das ist ein doppelt eingefügter Türblock.

**3. Überlappungen: 8 Paare über 0,01 m², Summe 25,01 m², davon 2 über 1 m².**
Enis' Zahl ist exakt, meine frühere Zuordnung war falsch:

| Fläche | Paar |
|--:|---|
| **20,25 m²** | `gang_1` (GANG, 30,57 m²) ↔ **`raum_64`** (GANG, 41,54 m²) |
| 1,91 m² | `lift_1` (LIFT) ↔ `raum_61` (TECHNIK, 2,82 m²) |
| 0,77 m² | `gang_1` ↔ `raum_63` (STIEGENHAUS, 20,22 m²) |
| 0,59 · 0,52 · 0,35 · 0,35 · 0,27 m² | `gang_1` ↔ `raum_30`/`raum_40`/`raum_39`/`raum_37`/`raum_35` |

Sechs der acht Paare hängen an **`gang_1`**, dem im Provider nachträglich
angelegten Gang (`geometrie_typ.py`) — er überlappt die Kaskaden-Räume, weil die
Bereinigung ihn nicht sieht. Das ist dieselbe zweite Messbasis, die schon bei
Muthgasse als Modell-Restüberlappung dokumentiert ist.

**4. Wohnungsflure: 14 GANG/VORRAUM, und die Einordnung widerspricht sich.**
**Alle 14** tragen `ist_communal=True` — auch die drei mit `WOHNUNG_PRIVAT` und
gesetzter `wohnung_id` (`raum_4`/top_3, `raum_46`/top_1, `raum_51`/top_2). Die
Türnachbarschaft spricht bei mehreren gegen `ALLGEMEIN_ERSCHLIESSUNG`:

| Raum | Fläche | Klasse | Türen | davon in private Räume | Details |
|---|--:|---|--:|--:|---|
| `raum_24` | 7,42 m² | ALLGEMEIN_ERSCHLIESSUNG | 16 | **15** | 16× `wohnungseingang` |
| `raum_43` | 6,25 m² | ALLGEMEIN_ERSCHLIESSUNG | 12 | **11** | 12× `wohnungseingang` |
| `raum_50` | 3,80 m² | ALLGEMEIN_ERSCHLIESSUNG | 12 | **11** | 12× `wohnungseingang` |
| `raum_64` | 41,54 m² | ALLGEMEIN_ERSCHLIESSUNG | 26 | 4 | 16× `wohnungseingang`, **2× `stiegenhaustuer`**, **1× `hauseingang`** |

Nur `raum_64` hat mit Stiegenhaus- und Hauseingangstür eine echte
gemeinschaftliche Anbindung. Der Owner-Fallback („ein Gang, der nur an private
Räume grenzt und keine Tür ins Stiegenhaus oder ins Freie hat, ist privat")
würde bei `raum_24`, `raum_43` und `raum_50` greifen.

**Zur Ausgangshypothese:** die vier Befunde haben tatsächlich einen gemeinsamen
Nenner, aber **nicht** die Wandkörper — Befund 1 kommt aus Türtexten, Befund 2
aus doppelt eingefügten Türblöcken, Befund 3 aus dem nachträglich angelegten
`gang_1`, Befund 4 aus der Wohnungsbildung. Behoben ist in diesem Auftrag
**nichts**: er war eine Prüfung.

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

### Nachtrag 2026-09-12, `5ccdc27`: der Zähler ist jetzt gemessen

Gelaufen über alle fünf Pläne mit Provider-Parse, je Segment
`begrenzende_flaechen` plus `miss_breitenprofil` (Laufzeit 10,4 / 31,0 / 580,6 /
2,6 / 1,8 s):

| Plan | neu | § 10.4 (2026-09-10) |
|---|--:|--:|
| Barawitzka_EG | **12/12** | 12/12 |
| Mollgasse_EG | **110/126** | 107/126 |
| Muthgasse_E2 | **145/148** | 154/155 |
| Rennweg_EG | **9/9** | 9/9 |
| Rennweg_OG3 | **5/5** | 5/5 |
| **Summe** | **281/300 = 93,7 %** | 287/307 = 93,5 % |

**Die Quote hält, die Mengen haben sich verschoben.** Im Einzelnen:

- **Mollgasse 107 → 110 messbare Segmente** bei gleichem Nenner 126. Drei
  Segmente sind durch die Bereinigung messbar geworden — die Raumpolygone sind
  dort enger geschnitten, also greift `begrenzende_flaechen` sauberer.
- **Muthgasse 154/155 → 145/148.** Der Nenner fällt um 7 (weggefallene
  Kontaktzonen-Durchgänge), der Zähler um 9. Netto verliert dieser Plan also
  zwei messbare Segmente mehr, als er Segmente verliert.
- Barawitzka und beide Rennweg-Pläne sind **unverändert**.

Gründe-Verteilung neu: `kein_abschnitt_ueber_mindestlaenge` 126 ·
`flaeche_fehlt` **13** · `nur_tuer_oder_eckpunkte` **6**. Gegen § 10.4
(`flaeche_fehlt` 12, alle Mollgasse; `nur_tuer_oder_eckpunkte` 8): die 12
Mollgasse-Fälle sind **unverändert** vorhanden, dazu **einer neu in Muthgasse**.
`kein_abschnitt_ueber_mindestlaenge` ist kein Messausfall — diese Segmente sind
`messbar=True`, nur ohne Abschnitt über der Mindestlänge.

**Damit ist die Zahl neu erhoben und der alte Bruch abgelöst:** gültig auf
`5ccdc27` ist **281/300 (93,7 %)**. Die 287/307 bleibt als Angabe ihres Standes
(2026-09-10, vor der Bereinigung) stehen und ist nicht mehr aktuell.

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
