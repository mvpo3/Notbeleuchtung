# Slices K1–K4 — Stapel ab `de31621`

Vier Slices aus Enis' Referenzen, Reihenfolge K1 → K2 → K3 → K4, je Slice ein
eigener Branch auf dem Stand des vorigen gebauten Slice. Diese Datei wächst
entlang des Stapels: je Slice ein Abschnitt mit Befund (gemessen), Regel
(wörtlich), Umsetzung, Test, Blast Radius, Gate, betroffenen fremden Lanes und
offenen Owner-Fragen.

**Basis des Stapels:** `de31621` (Code-Stand `60c671a` = Türstapel `aa05143` +
VOK-a + Darstellungsskripte). Basisläufe: alle 23 Prüfgeschosse (Rennweg 7,
Mollgasse 8, Muthgasse E2–E9) mit `ArchitekturRaumProvider().parse` auf `de31621`,
je Raum Typ, Polygon, Fläche, Nutzungsklasse, Wohnung, Notlicht-Flags, Kaskaden-
Quelle, dazu Türen, Ausgänge, Stempel-Zuordnungen und alle Wandkörper. Die
Messskripte liegen außerhalb des Repos (Scratch).

**K1 — Möbel sind keine Wände:** Prämisse falsch, nichts gebaut. Der Bericht
steht auf Branch `selman/fix-k1-moebel-keine-wand` (`558dee3`). K2 baut deshalb
direkt auf `de31621`.

---

## K2 — Schächte nur mit Beleg, und konsistent über Geschosse (Enis Referenz 15, Markierung 1; Diagnose „Schacht 1,4")

**Status: STOPP.** Regel a und b sind gebaut, alle K2-Tests grün, keine Wand
verloren, kein Notlicht-Wechsel — aber das Gate hat einen **neuen** Verstoß:
(3) Rennweg DG2 `M3` 4 → 5 Räume / 1,26 → 1,522 m² rote Schachtfläche, genau
die neue NISCHE (Owner-Frage 1). Die Commits bleiben stehen; K3 baut nicht auf
K2. Branch `selman/fix-k2-schacht-beleg` von `de31621`: `57168bd` Test (rot),
`6adc7b3` Fix, `fed0378` Kommentar-Korrektur, danach dieser Bericht.

### Owner-Befund (wörtlich)

> DG2 „Schacht 1,4" oben links ist die Fensternische mit rotem Keil,
> Falschtreffer, seit der Diagnose bekannt und immer noch da. OG2 hat 0
> Schächte, obwohl dieselben Schächte in OG1 und OG3 erkannt werden.

### Regel (wörtlich)

> Regel a: rote Kontur allein ist kein Beleg. SCHACHT braucht mindestens eines:
> Text DDB/BDB/DBA/Schacht/Durchbruch in 500 mm, U-förmige Schachtmauer,
> FEUERFESTER_STEIN-Keil, Schacht-Zone oder -Layer. Sonst NISCHE, magenta.
>
> Regel b: Schächte laufen senkrecht durchs Gebäude. Nach der Erkennung je
> Geschoss die Schachtpositionen über alle Geschosse desselben Projekts
> abgleichen (gleiche Lage in CAD-mm, Toleranz 300 mm). Ein Schacht, der in
> mindestens zwei Nachbargeschossen belegt ist, wird im dazwischenliegenden
> Geschoss an derselben Stelle gesucht; fehlt er, als Warnung „Schacht
> erwartet, nicht gefunden" mit Position melden, nicht erfinden.

**Lesarten** (jede einzeln gekennzeichnet, Owner-Bestätigung erbeten):

* **Planer-Lesart (verbindlich vorgegeben):** die S5c/F1-Evidenz „mehr als
  halbe Liftkabine im Polygon" (`lift_erkennung.liftschacht_reste`) zählt als
  Beleg — sonst bräche die Owner-Entscheidung F1 und Gate (11).
* **Planer-Lesart (verbindlich vorgegeben):** „dazwischenliegend" = ist eine
  Lage in Geschoss i und j (i < j) belegt, wird jedes Geschoss strikt
  dazwischen gesucht.
* **Executor-Lesart „FEUERFESTER_STEIN-Keil":** der Keil belegt den Schacht,
  den er markiert — den Kasten (geschlossene Polylinie ≤ 3 m², die den Keil
  enthält). Die Fläche muss zu mindestens der Hälfte in solchen Kästen liegen.
  Begründung unten („Messung DG2"): an der Fensternische liegt derselbe Keil
  wie an den echten Schächten; ohne Bezug auf den Kasten wäre sie belegt.
* **Executor-Lesart Text:** Wortschatz `DDB`, `BDB`, `FBDB`, `DBA`, `SCHACHT`
  als eigenes Wort, `DURCHBRUCH` auch im Kompositum; dieselbe Ausschlussliste
  wie S3a (`RAUM`, `TREPP`, `STIEG`, `AUFZUG`, `LIFT`). „500 mm" = Abstand
  Einfügepunkt → Polygon. Gemessen: die Ausschlussliste trifft an keinem der
  26 Schächte einen Text im Umkreis.
* **Schacht-Zone:** ein SCHACHT aus einem Stempel/einer Zone „Schacht"
  (`raumtyp._EXTRA_DIRECT["schacht"]`) ist durch seine Quelle belegt und läuft
  nicht durch die Prüfung. **Schacht-Layer:** Entity auf einem Layer mit
  `SCHACHT` im Namen, Stützpunkt-Mittel im Polygon (0 Treffer im Korpus).

### Messung: Inventur aller Schächte (Basis `de31621`, 23 Geschosse)

26 SCHACHT-Räume. Quelle = der Code-Pfad, der den Typ gesetzt hat; Beleg = was
im Plan steht (Text bis 500 mm, Keil-Kasten-Anteil der Fläche, Liftkabinen-
Anteil).

| Projekt | Geschoss | Raum | m² | Quelle | Beleg | nach K2 |
|---|---|---|--:|---|---|---|
| Rennweg | UG | `rest_3` | 2,69 | S5c `liftschacht_reste` (Rest war STIEGENHAUS) | Kabine 0,65 | SCHACHT |
| Rennweg | EG | `rest_2` | 2,70 | S5c | Kabine 0,64 | SCHACHT |
| Rennweg | OG1 | `rest_2` | 2,74 | S5c | Kabine 0,63 | SCHACHT |
| Rennweg | OG3 | `rest_1` | 1,16 | `rest_komponenten._typisiere` klein + türlos | Text „S5 DDB/BDB 40/105" 494 mm; Keil-Kasten 0,65 | SCHACHT |
| Rennweg | OG3 | `rest_2` | 1,15 | `_typisiere` Planzeichen im Polygon (S3a) | Text „DBA SCHACHT" 0 mm; Keil-Kasten 0,98 | SCHACHT |
| Rennweg | DG1 | `rest_1` | 1,25 | `_typisiere` S3a | Text „DBA SCHACHT" 0 mm; Keil-Kasten 0,97 | SCHACHT |
| Rennweg | DG1 | `rest_3` | 2,30 | S5c | Kabine 0,68 | SCHACHT |
| Rennweg | DG2 | `rest_2` | 1,16 | `_typisiere` S3a | Text „DBA SCHACHT" 0 mm; Keil-Kasten 0,99 | SCHACHT |
| Rennweg | DG2 | `rest_4` | 2,62 | S5c | Kabine 0,66 | SCHACHT |
| Rennweg | DG2 | **`rest_5`** | **1,42** | `_typisiere` klein + türlos | nächster Beleg-Text 2 592 mm; Keil-Kasten **0,18** | **NISCHE** |
| Mollgasse | 2.KG | `rest_2` | 2,36 | S5c | Kabine 0,99 | SCHACHT |
| Mollgasse | 2.OG | **`rest_2`** | **2,53** | `_typisiere` klein + türlos | nächster Beleg-Text 992 mm; kein Keil | **NISCHE** |
| Muthgasse | E2 | `stiegenhaus_1` / `_2` | 6,68 / 5,66 | S5c (STIEGENHAUS aus `geometrie_typ`) | Kabine 0,55 / 0,57; `_2`: Text „FDB/DDB HKLS" 0 mm | SCHACHT |
| Muthgasse | E3–E8 | `stiegenhaus_1` / `_3` je Geschoss | 6,46 / 5,77 | S5c | Kabine 0,54 / 0,58; `_3`: Text „FDB/DDB HKLS" 0 mm | SCHACHT (12) |

Summe: 26 SCHACHT → 24 SCHACHT + 2 NISCHE. 20 hängen an S5c (davon 7 zusätzlich
mit Text), 4 an Text und Keil-Kasten, 2 hatten keinen Beleg. Kein Schacht hing
an einem STO-Kästchen, einem Schacht-Layer oder einer Schacht-Zone.

### Messung DG2 „Schacht 1,4" (`rest_5`)

* Typ-Pfad: `rest_komponenten._typisiere` Zweig „< 3 m² und 0 Türen ≤ 600 mm"
  (vor K2 ohne jeden Beleg). Keine Tür, kein Treppenmarker ≤ 1 000 mm, kein
  STO-Kästchen.
* Im Plan an der Nische: ein roter Kasten auf `New_255 Plangrafiken_Pen_No__21`
  (0,387 m²), eine rote Kontur auf `New_HKLS1_Pen_No__21` und ein **HATCH
  `FEUERFESTER_STEIN`** auf `New_HKLS1_Pen_No__39` (0,0456 m²). Das ist
  **derselbe Keil** (gleiches Muster, gleicher Layer) wie an den drei
  beschrifteten DBA-/Installationsschächten (DG1 `rest_1` 0,107 m², DG2
  `rest_2` 0,131 m², OG3 `rest_2` 0,095 m²). Der „rote Keil" der Nische ist
  also ein FEUERFESTER_STEIN-Keil.
* Der Keil berührt `rest_5` (Abstand 0 mm, 0,0106 m² im Polygonring). Wörtlich
  genommen („mindestens eines: … FEUERFESTER_STEIN-Keil") wäre die Nische
  belegt und bliebe SCHACHT. Der Schwerpunkt des Keils liegt 19 mm außerhalb
  der Nische, bei den echten Schächten 30–73 mm innerhalb — das ist
  Rasterrauschen (50-mm-Raster), keine Regel.
* Was trennt: der Kasten, den der Keil markiert. Anteil der Fläche in
  Keil-Kästen: DBA-/Installationsschächte **0,65–0,99**, Nische **0,18**; alle
  gestempelten Räume mit Schachtsymbolen im Inneren ≤ 0,07. Der Kasten der
  Nische ist der „Schachtverzug über Dach" aus der Diagnose (Kasten außerhalb
  der Fassade, Beschriftung „Schachtverzug entweder im Zimmer oder über Dach
  blechverkleidet" in 1,8 m; das Wort „Schachtverzug" ist kein Schacht-Wort,
  Wortgrenze).
* Fensternische: `rest_5` grenzt an `raum_5` ZIMMER 19,60 m² (112 mm Fuge),
  in der Nordwand die Dachfenster `Roof_3`.

### Messung OG2 „0 Schächte"

* Die Rennweg-Geschosse liegen deckungsgleich (`lift_1` in allen 7 bei
  (12549102, 356219135)).
* OG1 und OG3 teilen **keine** Schachtlage: OG1 trägt nur den
  Liftschacht-Rest (`rest_2`), OG3 den DBA-Schacht (`rest_2`) und die
  L/S-Schachtreihe (`rest_1`). Der Befund stimmt in der Sache trotzdem: die
  Liftschacht-Lage ist in UG, EG, OG1, DG1, DG2 belegt und fehlt in **OG2 und
  OG3**.
* Ursache (in-memory gemessen): in OG2 und OG3 ist der Liftschacht keine eigene
  Restfläche, sondern Teil der Stiegenhaus-Restfläche — OG2 `rest_1`
  STIEGENHAUS 21,34 m² vor dem Ausstanzen, Kabinenanteil 0,082; OG3 `rest_3`
  8,53 m², Kabinenanteil 0,204. Unter 0,5 greift S5c/F1 nicht; `finde_lifte`
  stanzt nur die Kabine (1,82 / 1,75 m²) aus. Regel b meldet das jetzt als
  Warnung und erfindet nichts.

### Umsetzung

* `src/notbeleuchtung/raumerkennung/rest_komponenten.py`
  * `_schacht_belege(plan)` sammelt einmal je Plan die Beleg-Kandidaten:
    Text-Einfügepunkte (`_BELEG_TEXT_RX` minus `_SCHACHT_AUSSCHLUSS_RX`),
    Keil-Kästen (HATCH `FEUERFESTER_STEIN` → geschlossene LW/POLYLINE
    ≤ 3 m², die ihn mit 20 mm Toleranz deckt → Union), Schacht-Layer-Punkte.
  * `_hat_beleg(shp, belege)`: Text ≤ 500 mm **oder** Keil-Kasten-Anteil
    ≥ 0,5 **oder** Schacht-Layer-Punkt im Polygon.
  * `_typisiere`: der Zweig „klein (< 3 m²) und türlos" gibt SCHACHT nur mit
    Beleg, sonst **NISCHE** (Flags False/False). Die übrigen Zweige (S3a
    Planzeichen im Polygon, Treppenmarker, GANG) und alle anderen
    SCHACHT-Quellen (Stempel, S5c) sind unverändert. Der alte Zusatz „oder
    STO-Kästchen im Polygon" im letzten Zweig war toter Code (S3a fängt ihn
    vorher) und ist entfallen.
  * U-förmige Schachtmauer: **nicht umgesetzt** (Owner-Frage 3).
* `src/notbeleuchtung/raumerkennung/schacht_abgleich.py` (neu, reine Funktion)
  * `geschoss_rang(geschoss, name)`: `2KG` −2 < `UG`/`1KG` −1 < `EG` 0 <
    `nOG` n < `DG` 100 + n. `geschoss_befund` liefert DG1 und DG2 beide als
    `DG` (Kürzel-Muster ohne Ziffer); die Reihenfolge trägt nur der
    Dateiname, daher `DG<n>` aus dem Namen, sonst 101.
  * `gleiche_schaechte_ab([(Name, Räume), …])` (unten → oben): SCHACHT-Lage =
    Polygon-Schwerpunkt, erste Fundstelle ist der Anker, gleiche Lage bis
    300 mm; je Lücke zwischen zwei belegten Geschossen eine Warnung
    „Schacht erwartet, nicht gefunden: <Geschoss> bei (x, y) — belegt in …;
    an der Stelle: <Typ> <Raum>". Erzeugt und ändert keinen Raum; NISCHE und
    LIFT zählen nicht.
* `scripts/analyse/raumerkennung_darstellung.py`: `_schaechte_md` schreibt je
  Projektordner `SCHAECHTE.md` (Schachtzahl je Geschoss mit Raum-IDs, Lagen mit
  belegten Geschossen, Warnungen) aus den `_cache.pkl`; `index.html` und
  `README.md` verlinken sie. Die Spalte „Schächte" der Übersicht zählt wie
  bisher je Geschoss.
* `docs/VOKABULAR.md`: NISCHE als geometrische Kategorie der Raumerkennung,
  **kein Kanon-Typ**. Die Naht-Guards `test_vokabular_doku.py` und
  `test_lb_raumtyp_naht.py` lesen nur `raumtyp._TYP_MAP`/`_EXTRA_DIRECT`/
  `_EXTRA_OVERRIDE`; NISCHE dort einzutragen hätte die LB-Stützliste
  (`normwissen/`) gezogen. Ein Tabelleneintrag in § 1 hätte
  `test_vokabular_doku` gebrochen (Doku ⊄ Kanon). Deshalb ein Absatz unter der
  Tabelle, beide Guards grün.

### Test

* `tests/raumerkennung/test_rest_komponenten.py`: sieben K2-Fälle (ohne Beleg
  NISCHE ohne Flags und ohne Klasse; Text 400 mm → SCHACHT, auch
  „Deckendurchbruch"; Text 700 mm → NISCHE; Keil im Kasten der Fläche →
  SCHACHT; Keil-Kasten streift nur 10 % → NISCHE; rote Kontur allein → NISCHE;
  Schacht-Layer → SCHACHT). **Geändert:** `test_rest_findet_rechten_raum_und_schacht`
  → `…_und_nische` (ohne Plan kein Beleg; Regeländerung, nicht grün gebogen).
* `tests/raumerkennung/test_schacht_abgleich.py`: Lücke im mittleren Geschoss →
  eine Warnung mit Position und dem Raum an der Stelle, Räume vorher = nachher;
  Suche nur zwischen belegten Geschossen; NISCHE und > 300 mm zählen nicht;
  mehrere Lücken; Rangfolge `2KG` … `DG2`.
* `tests/naht/test_k2_schacht_beleg.py` (Rennweg, 7 echte Parse-Läufe):
  DG2-Nische an (12545233, 356225851) ist NISCHE, 1,2–1,6 m², Klasse None;
  Liftschacht-Reste UG/EG/OG1/DG1/DG2 bleiben SCHACHT; DBA-Schacht OG3/DG1/DG2
  bleibt SCHACHT; Abgleich: Liftschacht-Lage belegt in UG, EG, OG1, DG1, DG2,
  Warnungen genau für OG2 und OG3, DBA-Lage OG3/DG1/DG2 ohne Warnung, Nische
  nimmt nicht teil, kein Raum erzeugt oder umtypisiert.
* `tests/raumerkennung/test_raumerkennung_darstellung.py`: `SCHAECHTE.md` mit
  Schachtzahl je Geschoss (OG1 < OG2 < DG1 < DG2 über den Namen), Lage mit
  belegten Geschossen und IDs, Warnung für OG2.
* **Rot auf `de31621`** (neue Tests gegen den Basis-Code, Scratch-Runner
  importiert `src` und Darstellung aus dem Basis-Worktree): 6 failed
  (`test_rest_komponenten` 5, Darstellung 1: `_schaechte_md` fehlt),
  `test_schacht_abgleich` und `test_k2_schacht_beleg` ImportError
  (`schacht_abgleich` fehlt). **Grün auf `6adc7b3`:** 46 passed (20 s).

### Blast Radius (23 Geschosse, `de31621` → `6adc7b3`)

Vorher = Basisläufe `de31621`, nachher = 23 echte `ArchitekturRaumProvider().parse`
auf `6adc7b3` (alle `status ok`, Arbeitsbaum sauber). `fed0378` ändert danach nur
einen Kommentar (Gate-Messung auf `fed0378` ohne `meta` identisch mit der auf
`6adc7b3`). Räume per IoU ≥ 0,5 zugeordnet; Fläche = Änderung ≥ 0,5 m² oder
≥ 2 %; Notlicht-Flags = (`ist_fluchtweg`, `ist_communal`); Türen per Lage
≤ 150 mm, Ausgänge ≤ 500 mm; Wandkörper = Anzahl (Fläche mitverglichen).

| Projekt | Plan | Räume v→n | Typ | Klasse | Fläche | neu/weg | Wohnungen v→n | Einraum v→n | Notlicht-Flags | Türen v→n | Türrolle | Ausgänge v→n | SCHACHT v→n | NISCHE v→n | Wandkörper v→n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mollgasse | 1.KG | 31→31 | 0 | 0 | 0 | 0/0 | 0→0 | 0→0 | 0 | 23→23 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 116→116 |
| Mollgasse | 1.OG | 93→93 | 0 | 0 | 0 | 0/0 | 33→33 | 20→20 | 0 | 112→112 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 338→338 |
| Mollgasse | 2.KG | 30→30 | 0 | 0 | 0 | 0/0 | 1→1 | 1→1 | 0 | 40→40 (+0/−0) | 0 | 1→1 | 1→1 | 0→0 | 144→144 |
| Mollgasse | 2.OG | 98→98 | 1 | 1 | 0 | 0/0 | 33→33 | 18→18 | 0 | 121→121 (+0/−0) | 0 | 1→1 | 1→0 | 0→1 | 354→354 |
| Mollgasse | 3.OG | 65→65 | 0 | 0 | 0 | 0/0 | 26→26 | 15→15 | 0 | 93→93 (+0/−0) | 0 | 4→4 | 0→0 | 0→0 | 239→239 |
| Mollgasse | 4.OG | 53→53 | 0 | 0 | 0 | 0/0 | 15→15 | 7→7 | 0 | 59→59 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 211→211 |
| Mollgasse | DG | 35→35 | 0 | 0 | 0 | 0/0 | 10→10 | 3→3 | 0 | 38→38 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 177→177 |
| Mollgasse | EG | 64→64 | 0 | 0 | 0 | 0/0 | 21→21 | 15→15 | 0 | 102→102 (+0/−0) | 0 | 9→9 | 0→0 | 0→0 | 171→171 |
| Muthgasse | E2 | 108→108 | 0 | 0 | 0 | 0/0 | 22→22 | 8→8 | 0 | 193→193 (+0/−0) | 0 | 1→1 | 2→2 | 0→0 | 737→737 |
| Muthgasse | E3 | 124→124 | 0 | 0 | 0 | 0/0 | 23→23 | 6→6 | 0 | 141→141 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 839→839 |
| Muthgasse | E4 | 120→120 | 0 | 0 | 0 | 0/0 | 21→21 | 5→5 | 0 | 139→139 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 815→815 |
| Muthgasse | E5 | 123→123 | 0 | 0 | 0 | 0/0 | 21→21 | 4→4 | 0 | 144→144 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 1250→1250 |
| Muthgasse | E6 | 122→122 | 0 | 0 | 0 | 0/0 | 22→22 | 4→4 | 0 | 146→146 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 1249→1249 |
| Muthgasse | E7 | 96→96 | 0 | 0 | 0 | 0/0 | 19→19 | 4→4 | 0 | 100→100 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 1029→1029 |
| Muthgasse | E8 | 97→97 | 0 | 0 | 0 | 0/0 | 13→13 | 2→2 | 0 | 112→112 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 994→994 |
| Muthgasse | E9 | 61→61 | 0 | 0 | 0 | 0/0 | 9→9 | 2→2 | 0 | 58→58 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 701→701 |
| Rennweg | DG1 | 15→15 | 0 | 0 | 0 | 0/0 | 1→1 | 0→0 | 0 | 14→14 (+0/−0) | 0 | 2→2 | 2→2 | 0→0 | 194→194 |
| Rennweg | DG2 | 13→13 | 1 | 1 | 0 | 0/0 | 2→2 | 1→1 | 0 | 10→11 (+1/−0) | 0 | 3→3 | 3→2 | 0→1 | 183→183 |
| Rennweg | EG | 24→24 | 0 | 0 | 0 | 0/0 | 2→2 | 1→1 | 0 | 40→40 (+0/−0) | 0 | 5→5 | 1→1 | 0→0 | 192→192 |
| Rennweg | OG1 | 18→18 | 0 | 0 | 0 | 0/0 | 3→3 | 1→1 | 0 | 18→18 (+0/−0) | 0 | 2→2 | 1→1 | 0→0 | 196→196 |
| Rennweg | OG2 | 18→18 | 0 | 0 | 0 | 0/0 | 2→2 | 0→0 | 0 | 22→22 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 177→177 |
| Rennweg | OG3 | 17→17 | 0 | 0 | 0 | 0/0 | 2→2 | 0→0 | 0 | 18→18 (+0/−0) | 0 | 3→3 | 2→2 | 0→0 | 204→204 |
| Rennweg | UG | 24→24 | 0 | 0 | 0 | 0/0 | 4→4 | 3→3 | 0 | 21→21 (+0/−0) | 0 | 2→2 | 1→1 | 0→0 | 187→187 |

**Summen:** 2 Typwechsel, 2 Klassenwechsel, 0 Flächenänderungen, 0 neue / 0
entfallene Räume, Wohnungen und Einraum-Wohnungen in allen 23 Geschossen
unverändert, **0 Notlicht-Flag-Wechsel** (00 ↔ 11: keiner), 1 neue Tür,
0 Türrollen- und 0 Ausgangs-Änderungen, Wandkörper in allen 23 Geschossen
gleich (Anzahl und Fläche) — **keine Wand verloren**.

Einzelliste:

* Rennweg DG2 `rest_5` 1,42 m²: SCHACHT → **NISCHE**, Klasse KEIN_RAUM → None,
  Flags 00 → 00, `wohnung_id` None → None. Neu: `durchgang_2` blattlos
  `raum_5` ZIMMER ↔ `rest_5`, 1 413 mm, Rolle None (vorher sperrte der
  S5a-Guard die Öffnung, weil SCHACHT KEIN_RAUM ist). Die übrigen Durchgänge
  rücken eine Nummer weiter (`durchgang_2…5` → `_3…6`, gleiche Lage, gleiche
  Rolle; die Wohnungsklassen-Warnung zu `raum_1` nennt jetzt `durchgang_6`).
* Mollgasse 2.OG `rest_2` 2,53 m²: SCHACHT → **NISCHE**, Klasse KEIN_RAUM →
  None, Flags 00 → 00. Das ist die Küchenzeile (Spüle, Kochfeld) der
  WOHNKÜCHE 25,94 m² von Top 15 — kein Schacht; der nächste Schacht-Text
  „S2.7a FBDB 20/20 DDB 20/20" in 992 mm gehört zum Schacht am AR daneben.
  Keine neue Tür.

### Regel b: Schachtlagen über die Geschosse (Nachher-Läufe)

Rang über `geschoss_rang` (Rennweg DG1 101, DG2 102 über den Dateinamen).

* **Rennweg** (Geschosse deckungsgleich, `lift_1` überall bei
  (12549102, 356219135)). Schachtzahl je Geschoss: UG 1, EG 1, OG1 1, **OG2 0**,
  OG3 2, DG1 2, DG2 2 (vorher 3).
  * Lage (12549154, 356219192), Liftschacht-Rest: belegt UG `rest_3`, EG
    `rest_2`, OG1 `rest_2`, DG1 `rest_3`, DG2 `rest_4` → **2 Warnungen**:
    „Schacht erwartet, nicht gefunden: OG2 bei (12549154, 356219192) — belegt
    in UG, EG, OG1, DG1, DG2; an der Stelle: LIFT lift_1", dieselbe für OG3.
  * Lage (12552056, 356216416), DBA-Schacht: OG3 `rest_2`, DG1 `rest_1`, DG2
    `rest_2` — lückenlos.
  * Lage (12555534, 356216660), L/S-Schachtreihe: nur OG3 `rest_1`.
* **Muthgasse** (deckungsgleich): E2–E8 je 2, E9 0. Die Lagen (335812, 104358)
  und (337129, 105327) sind je in E2 … E8 belegt, lückenlos, keine Warnung (E9
  liegt oberhalb, nicht dazwischen).
* **Mollgasse**: 2.KG 1 (`rest_2`, Liftschacht-Rest), alle anderen 0 (2.OG
  vorher 1). Die acht Geschosse liegen in CAD-mm **nicht deckungsgleich**: der
  nächste Lift eines anderen Geschosses liegt 28,3 m bis 346,7 m entfernt. Der
  Abgleich findet deshalb keine gemeinsame Lage und meldet nichts — richtig
  im Sinne von „nicht erfinden", aber blind (Owner-Frage 5).

### Gate

| | `de31621` (vorher) | `fed0378` (nachher) |
|---|---|---|
| `pruefe_gate(nullmessung_f15d03f, …)` | 2 Verstöße: (3) DG2 `M4.einraum` 0 → 1; (10) Barawitzka ABSTELLRAUM ohne Tür | **4 Verstöße: dieselben 2 + NEU (3) DG2 `M3.hauptwert` 4 → 5 und (3) DG2 `M3.rote_flaeche_m2` 1,26 → 1,522** |
| M17 | 18/18 BESTANDEN | 18/18 BESTANDEN |
| (11) DG1 | 2 Ausgänge, 0 durch den Liftschacht | 2 Ausgänge, 0 durch den Liftschacht (grün) |
| `pytest -m gate tests/gate` | 3 passed, 1 xfailed (K1) | 3 passed, 1 xfailed, 81 deselected (60 s) |

Messungen: `tests/gate/gate_messung.py --out _arbeit/gate/messung_<sha>.json`
(`de31621` im sauberen Basis-Worktree, ohne `meta` identisch mit der
K1-Messung; `6adc7b3` und `fed0378` hier, `arbeitsbaum_src_scripts_sauber =
true`).

**Der neue Verstoß ist genau die Nische.** M3 zählt Räume, die nicht
SCHACHT/LIFT sind und rote Schachtfläche ≥ 0,02 m² enthalten. Nachher ist der
fünfte Raum `rest_5` NISCHE mit 0,262 m² roter Fläche — der Teil des Kastens
„Schachtverzug über Dach", der in die Nische ragt (Diagnose DG2-6: 0,26 m²).
Vorher war `rest_5` SCHACHT und damit von M3 ausgenommen. M3 misst also die
Folge der Owner-Regel selbst: eine Nische mit roter Kontur ist jetzt
ausdrücklich kein Schacht. Heilen lässt sich das nur über eine
Owner-Entscheidung (Owner-Frage 1), nicht innerhalb des Auftrags.

### Fremde Lanes (gemessen, nichts geändert)

* `platzierung/` (Leonis): `pipeline.run(build_default_bundle(), …)` mit dem
  Code `de31621` und `6adc7b3` — Rennweg DG2: 7 Leuchten (4 RZ, 3 SL) vorher
  wie nachher, **Positionen identisch**, 0 Leuchten in der Nische (vorher 0
  im SCHACHT); Mollgasse 2.OG: 18 Leuchten (7 RZ, 11 SL), Positionen
  identisch, 0 in der Nische. NISCHE bekommt keine Leuchte, wo SCHACHT keine
  hatte; kein Raum verliert eine Leuchte.
* `normwissen/` (Enis): nicht berührt. Die LB-Stützliste bleibt gültig, weil
  NISCHE nicht im `raumtyp`-Kanon steht (`test_lb_raumtyp_naht` grün).
* `hauptengine/contracts/`: nicht berührt (`raum_typ` ist ein freier String).
* Board-Eintrag an @EnisAMG und @mvpo3 in `docs/COORDINATION.md` (Log,
  2026-09-30).

### Gezielte Tests (`fed0378`)

`pytest tests/raumerkennung tests/naht tests/contract`: **4 failed, 1 096 passed,
8 skipped, 14 xfailed** (19 min 29 s). Die 4 Fehlschläge sind genau die bekannt
roten, vorbestehenden: `test_s7_wohnungsklasse.py::test_keine_leuchten_in_wohnung_privat`
OG1/OG2/DG1 (Board 1, Leonis) und `test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell`.
`ruff check .` ohne Befund. Die volle Suite läuft erst im Output-Schritt.

### Offene Punkte / Owner-Fragen

1. **Gate (3) M3 DG2 (STOPP-Grund).** Die Nische `rest_5` enthält 0,262 m² des
   roten Kastens „Schachtverzug über Dach". Optionen: (a) Abnahme nachziehen —
   M3 steigt DG2 4 → 5 / 1,26 → 1,522 m² als gewollte Folge von Regel a; (b)
   den Kasten als eigenen SCHACHT aus der Nische stanzen (Schacht aus
   Planzeichen, Diagnose U3/S11, Frage F4-Zusatz „über Dach gezeichneter
   Schachtverzug: Schacht des Geschosses oder außen?") — eigener Slice; (c) M3
   nimmt NISCHE wie SCHACHT aus (Gate-Definition). Solange nichts entschieden
   ist, baut K3 nicht auf K2.
2. **FEUERFESTER_STEIN-Keil — Lesart bestätigen.** Umgesetzt: der Keil belegt
   nur eine Fläche, die zu ≥ 50 % in seinem Kasten liegt (gemessen 0,65–0,99
   gegen 0,18). Wörtlich („ein Keil genügt") bliebe die Nische SCHACHT, weil
   an ihr derselbe Keil liegt wie an den DBA-Schächten.
3. **U-förmige Schachtmauer** ist nicht umgesetzt. Gemessen als Anteil des
   150-mm-Rands an Wandkörpern (0,5 ≈ allseitig ummauert): DBA-/
   Installationsschächte 0,49–0,58, Liftschacht-Reste Rennweg 0,35–0,38,
   Mollgasse 2.KG 0,42, Muthgasse 0,07/0,23, Fensternische DG2 0,24,
   Küchenzeile Mollgasse 2.OG 0,33. Kein Schacht im Korpus hängt allein an der
   Mauer; ohne Positivbeispiel ist kein Schwellwert kalibrierbar, und die
   Küchenzeile zwischen zwei Wänden liegt nahe an „U-förmig". Soll das
   Kriterium gebaut werden, und woran ist eine Schachtmauer erkennbar
   (Material, Layer)?
4. **STO-Kästchen (Mollgasse `04-STO`/`05-STO`)** bleiben Beleg über die
   S3a-Regel „Planzeichen im Polygon". Sind sie „rote Kontur allein" (dann
   NISCHE) oder ein Durchbruch-Layer (dann Beleg)? Wirkung heute 0 (kein
   Schacht im Korpus hängt daran).
5. **Mollgasse nicht deckungsgleich.** Regel b braucht die Geschosse in
   gemeinsamen CAD-Koordinaten; Mollgasse liegt je Geschoss woanders (≥ 28 m).
   Ausrichten (z. B. über die Liftkabinen) wäre ein eigener Schritt.
6. **Liftschacht OG2/OG3 Rennweg.** Die Warnung ist richtig, die Ursache liegt
   eine Stufe früher: der Schacht ist dort mit der Stiegenhaus-Restfläche
   verschmolzen (Kabinenanteil 0,082 / 0,204 < 0,5). Gebaut ist nur die
   Warnung; eine Trennung wäre Rest-/Wandarbeit, nicht Teil von K2.
7. **Nische und Nachbarraum.** Die DG2-Nische hängt jetzt über einen
   blattlosen Durchgang (1 413 mm) am ZIMMER `raum_5`; nach F5
   („Fensternischen gehören zum Raumpolygon") wäre sie Teil des Zimmers.
   Zuschlagen ist nicht Teil von K2.
8. **Teständerung:** `test_rest_findet_rechten_raum_und_schacht` erwartete die
   alte Regel (türlos + klein = SCHACHT ohne Beleg) und heißt jetzt
   `…_und_nische`.
