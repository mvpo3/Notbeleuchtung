# Abschlussbericht — Mollgasse-Ground-Truth → Rivoplan-Hauptengine (2026-09-20)

Owner-Auftrag 2026-09-20 (PDF „Notbeleuchtungen zeichnen" + Rivoplan-Master-
Symbole/-Vorlage). Berichts-Schema A–L des Auftrags. **KEIN Push/PR/Merge
erfolgt — alles lokal, wartet auf GO.**

## A. Basis

- Repository `mvpo3/Notbeleuchtung`, Branch `leonis/demo-l-gebaeude`.
- Ausgangs-HEAD `fd09163` (= origin), origin/main `1d97548` (+1 Asset-Commit
  „Schul-Zips", nicht im Branch).
- Working Tree: die vorbestehenden 94 unversionierten Löschungen getrackter
  CAD-Rohdateien + modifizierte din_support-DWG (Owner-Aufräumen, unbestätigt)
  wurden NICHT angefasst, nicht committet, nicht restauriert.
- Session-Commits (lokal): `456057e` M1 Symbole · `24074c6` M2 beidseitig ·
  `63a2743` M3 Vorlage · `8b9f0d2` W Regelbasis-UG · `0603aec` G Harness ·
  `59e8f31` E4 UG-Fluchtrichtung · (+V-Commit Runner/Regression/Bericht).
- PDF vollständig analysiert: **ja** (95 Seiten physisch; S.95 leer → 94
  Inhaltsseiten, deckungsgleich mit der Auftrags-Angabe).
- Alle 8 Geschosse gefunden: **ja** (EG, 1–4OG, DG, 1KG, 2KG).
- Alle 8 Erklärungs-DXFs gefunden: **ja** (`knowledge/Pläne zeichnen Wissen/
  Mollgasse-Notbeleuchtungserklärung/`; EG/1KG/2KG = Owner-Fassung 20.09.).
- Alle 8 leeren Architektur-Inputs gefunden: **ja**
  (`Projekte_Leere Architektpläne (Input)/Mollgasse/`). Befund: die leeren
  Pläne sind in METERN gezeichnet (INSUNITS behauptet mm) — Selmans Erkennung
  skaliert korrekt auf mm (×1000, verifiziert).

## B. PDF-Analyse

- Kapitel: EG S.1–13 · 1OG 14–19 · 2OG 20–26 · 3OG 27–30 · 4OG 31–38 ·
  DG 39–41 · **1KG 41–56 · 2KG 57–94** (neu). Paginierung der Alt-Kapitel
  unverändert → Phase-B-Belege (Seiten-Refs) bleiben gültig.
- Fallinventar: **68 Beispiele** in `knowledge/notbeleuchtung/beispiele.json`
  (35 Phase B für EG–DG + 33 neu für 1KG/2KG). UG-Status: 28 bestätigt /
  4 präzisiert / **1 Widerspruch = PDF-TEXTfehler S.57 (B↔C vertauscht,
  → Owner, offene Frage 27)**.
- Planbilder: 54 Seiten-PNGs (S.41–S.94) visuell geprüft + in
  `knowledge/notbeleuchtung/abgleich/{1KG,2KG}/` abgelegt; jedes Beispiel in
  der Erklärungs-DXF lokalisiert und mm-genau nachgemessen (Handles zitiert).
- Nicht zuordenbar: 0 Beispiele. Kleinbefunde: 2KG Doppel-Label (A) `1D157`
  ohne Leuchte; 1KG blaue Erklär-Linien `1C010/1C011` unerläutert
  (offene Fragen 31/32).

## C. DXF-Ground-Truth je Geschoss

| G | Erklärungs-DXF | leerer Input | Fallmatrix | GT-Abgleich (Engine↔GT) |
|---|---|---|---|---|
| EG | ✓ (Owner-Update 20.09.: Kopier-Reste bereinigt, 18 Leuchten) | ✓ | Phase B + Delta | ✓ |
| 1OG | ✓ | ✓ | Phase B | ✓ |
| 2OG | ✓ | ✓ | Phase B | ✓ |
| 3OG | ✓ | ✓ | Phase B | ✓ |
| 4OG | ✓ | ✓ | Phase B | ✓ |
| DG | ✓ | ✓ | Phase B | ✓ |
| 1KG | ✓ (neu) | ✓ | ✓ 14 Beispiele | ✓ |
| 2KG | ✓ (neu) | ✓ | ✓ 19 Beispiele | ✓ |

GT-Messdaten eingefroren: `tests/fixtures/mollgasse_gt/<G>.json`
(Extraktor `scripts/analyse/mollgasse_gt_extract.py`; bbox-Zentren,
Welt-Pfeile, Personen-Blicke nach Regel #8, beidseitig-Paare).

## D. Regeln (Klassifikation)

`knowledge/notbeleuchtung/regeln.md` + `regeln.yaml`: **NB-R00–NB-R21**
(9 neu aus dem UG). Klassifikation je Regel dokumentiert:

- Fachpraxis/Expertenwissen (ausdrücklich KEIN Normzitat): NB-R14 Wand/Decke,
  **NB-R15 Kabeltrasse ≥450 mm („möglichst mindestens", wörtlich S.63–64)**,
  NB-R17 Garage-Durchquerbarkeit (Motorrad ja / Doppelparker nein).
- Regelhaft/hoch belegt: NB-R13 UG-Stiegenrichtung (hinauf MIT Pfeil),
  NB-R16 beidseitig (Pflicht bei zwei Gegenströmen; **Alternative bleibt
  Alternative** — orange, „muss nicht sein", wird NICHT automatisiert),
  NB-R19 UG-Türleuchte nach Nutzung, NB-R20 türlose Gänge/Durchgänge
  (inkl. der im PDF explizit VERWORFENEN Varianten S.73–74).
- Projektspezifisches Muster + bindende Prozessregel: NB-R18 Gebäudehälften
  („unklare Zuordnung niemals raten → offene Frage", S.78).
- Optional/Empfehlung: beidseitig-Alternative (2KG Gr.6), AP-als-Lux-Stütze.

## E. Engine (Implementierung)

**Runtime-Code (Production, KEINE Mollgasse-Hardcodes — Koordinaten leben nur
in Tests/Fixtures/Eval):**

1. `symbols/library.py` — Rivoplan_Notbeleuchtungs_Symbole.dxf = EINZIGE
   Symbolquelle (Pfad, Doku, Fehlermeldung).
2. `symbols/schrack_symbol_mapping.yaml` — Registry auf `RIVO_NL_ARR_*`
   (right jetzt klein-nativ ×50 statt ×1,905 — an der neuen Vorlagen-Legende
   re-kalibriert, Werte sonst identisch: RZ 883/AP 586/Aufheller+Spot 192/
   Anlage 852 mm) + neuer Key `notlicht_ks_beidseitig`; Alt-Key
   `vorlage_legende` gestrichen.
3. `symbols/orientation.py` — Basen an den NEUEN Blöcken gemessen
   (down 270°/left 180°/right 0°; right ohne Spiegel-OCS).
4. `symbols/inserter.py` — `richtung="gerade"`+RZ rendert EINEN echten
   `RIVO_NL_ARR_bothsided` (statt links+rechts-Komposition), XDATA am Block.
5. `render/dxf_renderer.py` — Rivoplan_Notbeleuchtungs_Vorlage.dxf = einzige
   Blatt-/Output-Vorlage (copy-on-load, Master unverändert); **Blatt-Anker
   werden GEMESSEN** (`_vorlage_anker`: Planfenster-Viewport, Rahmen,
   Legenden-Unterkante, Prüfvermerk-Bande) statt hartkodierter
   Vorlagen-Koordinaten; toter `_draw_vorlage`-Pfad entfernt (Fallback =
   Stücklisten-Box); floor_label kennt 1KG/2KG/UG.
6. `platzierung/bausteine.py` + `stgh_strategy.py` + `fachpraxis.py` —
   **NB-R13**: `fluchtvektor(hinauf)`; `ist_untergeschoss(floor)`
   (KG/UG/Keller-Labelfamilien); beide Stiegen-Call-Sites floor-aware.

**Nur Ground-Truth/Eval (bewusst NICHT Runtime):** GT-Extraktor,
GT-Vergleichs-Runner, GT-Fixtures, Regelbasis-Dokumente.

**Bewusst NICHT hardcodiert:** beidseitig-ALTERNATIVEN, 450-mm-KT als
Norm, Gebäudehälften-Trennlinie (rote Linie), TOP-Nummern, Koordinaten,
Motorrad/Doppelparker-Raumlabel-Heuristik.

## F. Symbolbibliothek

- Inventar Rivoplan_Notbeleuchtungs_Symbole.dxf (11 Blöcke): RIVO_NL_ARR_down/
  left/right (17,665 nativ, Pfeilbasen gemessen 270/180/0), **RIVO_NL_ARR_
  bothsided** (17,665×17,665, zwei gegenläufige Schilder — ERSTMALS echter
  Beidseitig-Block), Antipanikleuchte-RIVO (11,726), Aufheller Notbeleuchtung
  (1,849, blau 150), Sicherheitsleuchte Aufheller (4,699), Spot Notbeleuchtung
  (1,780), Gruppenbatterie-Verteiler (17,038×9,267), Kinder 9809550/595995.
- Mapping Funktion→Block: vollständig in `schrack_symbol_mapping.yaml`
  (Naht-Invariante grün); Photometrie-Mapping unverändert gültig.
- Fehlende Symbole: keine für die heutigen Engine-Funktionen.
- Legacy verhindert: Migrations-Guard verbietet `rivo-sibel`/`rivo-rz-arr`/
  Alt-Bibliothekspfade in src/tests/scripts; alte Bibliotheken sind
  de-trackt (`git rm`; physische Dateien noch Windows-gelockt — vermutlich
  AutoCAD offen — lokale Lösch-Nacharbeit nötig, im Repo sind sie weg).
- Single Source of Truth: **aktiv** (Prüfstrecke Mollgasse EG: 0 Alt-Blöcke
  im Output).

## G. Output-Vorlage

- Rivoplan_Notbeleuchtungs_Vorlage.dxf integriert: **ja** (Modus 1 Blatt +
  Modus 2 Layout1-Viewport 1:50; `tests/render/test_layout_vorlage.py` 6/6).
- PDF nutzt sie wirklich: **ja** (pdf_quelle-Weg rendert das aus der Vorlage
  gebaute Modelspace-Blatt; Vorlagen-Gate-Tests bestehen).
- Layout/Plankopf erhalten: ja (Layout1 behält exakt die 8 Owner-INSERTs;
  Plankopf/Legende/Logo werden gemessen übernommen; Geschoss-Feld wird
  ersetzt, PROJEKT bleibt Owner-Feld).
- Master bleibt unverändert: **ja** (nur gelesen; copy-on-load).
- Output-DXF funktioniert: ja (8/8 Geschosse).
- Einschränkung (ehrlich): bei den Mollgasse-Extents (>Planfenster in 1:50)
  greift die definierte Liefer-Policy **G6-Fallback auf das Modelspace-Blatt**
  (`layout_fallback` im Summary) — wie bisher, kein Migrationseffekt.

## H. Lichtberechnung (je Geschoss; MF/Photometrie aus dem Repo, nichts erfunden)

Engine-Placement (Lux-Nachweis-Seite je Plan, `<G>_lux.pdf`): **8/8 erzeugt.**
Experten-GT-Placement (`Mollgasse_GT/<G>/gt_lux_nachweis.png`):

| G | GT-Lux | Befund |
|---|---|---|
| EG | ✓ | Nachweis-Seite erzeugt (GT enthält SL/AP) |
| 1OG | ✓ | dito |
| 2OG | ✓ | dito |
| 3OG | — nicht prüfbar | GT trägt NUR Rettungszeichen (Signalisierung) — keine Beleuchtungs-Bewertungsgrundlage; KEIN Wert erfunden |
| 4OG | — nicht prüfbar | dito |
| DG | — nicht prüfbar | dito |
| 1KG | — nicht prüfbar | dito (0 Antipanik im GT — offene Frage 33: Lux-Bestätigung des AP-Verzichts steht aus) |
| 2KG | ✓ | Nachweis-Seite erzeugt (4 Antipanik im GT) |

Grenzen: Photometrie über den Repo-Katalog (`photometrie_mapping.yaml`);
für das echte Owner-Antipanik-Produkt (AP3) liegt weiterhin keine
Hersteller-LDT vor (bekannter Bestand) — Berechnung nutzt die hinterlegte
Rundlinsen-LDT, das ist als konservative Abschätzung im Prüfvermerk sichtbar.

## I. Tests (exakt ausgeführt)

- je Slice: `pytest tests/render -q` (95 passed) · `pytest tests/platzierung
  tests/contract tests/e2e tests/naht -q` (420 passed/35 skipped/3 xfailed,
  nach M2 erneut 62/35/3 für e2e+naht) · `pytest tests/render tests/contract
  -q` (151 passed) · `pytest tests/platzierung -q` (304 passed) ·
  `pytest tests/naht/test_mollgasse_gt.py -q` (**10 passed, neu**).
- `ruff check src tests scripts`: **clean** (die 73 Alt-Findings liegen in
  unversionierten WIP-Dateien außerhalb, unverändert wie im Handoff).
- Voller `pytest -q`: **1411 passed / 51 skipped / 5 xfailed / 1 failed**
  (11:06 min). Der eine Fail war der eigene Migrations-Guard, der die
  Alt-Blocknamen im frisch committeten Ground-Truth-BESTAND (GT-Fixtures/
  Extraktor — Eval-Daten, kein Render-Pfad) mit-verbot; mit begründeter
  Ausnahme gefixt, Nachlauf Guard+GT-Regression 14 passed.
- Die 35 Skips sind die bekannten Asset-Skips (Selman-Pfad-Umstellung
  ausstehend), 3 xfail = Selmans S4a-Stapel (strict-xfail, gewollt).

## J. Ground-Truth-Ergebnis (Engine auf LEEREM Plan vs. Experten-GT)

Paarung Nearest-Neighbor je Symbolklasse, Paarungs-Radius 3000 mm (nur fürs
Matching — alle Distanzen metrisch, KEINE Pass-Toleranz erfunden):

| G | GT-Einheiten | gepaart | fehlt | überflüssig | Median mm | beidseitig |
|---|---|---|---|---|---|---|
| EG | 17 | 5 | 12 | **48** | 1240 | 0/1 |
| 1OG | 11 | 4 | 7 | 8 | 1421 | — |
| 2OG | 11 | 4 | 7 | 10 | 1292 | — |
| 3OG | 4 | 1 | 3 | 8 | 1262 | — |
| 4OG | 7 | 5 | 2 | 9 | 959 | — |
| DG | 6 | 2 | 4 | 6 | 1851 | — |
| 1KG | 12 | 3 | 9 | 11 | 1621 | 0/1 |
| 2KG | 29 | 9 | 20 | 15 | 2024 | 0/6 |
| **Σ** | **97** | **33** | **64** | **115** | — | **0/8** |

Ursachen-Klassifikation (Details `Projekte/_ergebnis/Mollgasse_GT/<G>/`):
- **EG-Überproduktion (48)** ist dominiert von Aufhellern (27 SL) — die
  bekannte Aufheller-/S4-Kalibrier-Lane, deckt sich mit dem Fischamend-Befund.
- **KG-Fehlstände** sind primär ERKENNUNGS-getrieben (siehe K.1): ohne
  Kellerabteile/Garage-Zirkulation platziert die Engine dort nicht.
- **beidseitig 0/8**: der Mechanismus existiert (Wasserscheide → `gerade` →
  seit M2 echter bothsided-Block), aber an den GT-Spots entsteht mangels
  KG-Zirkulation gar kein RZ (Komplett-Miss, nicht Typ-Fehler).
- Positionsniveau der ECHTEN Paare: Median ~1–2 m (Engine mittellinien-/
  ankergetrieben vs. Experten-Tür-/Wandpositionen) — Kalibrier-, kein
  Konzeptabstand.

## K. Engine-Gap-Liste (nach vollständigem GT-Abgleich)

1. **KG-/Garage-Erkennung (Selman-Naht, größter Hebel):** leere KG-Pläne
   liefern 0 KELLERABTEILE, nur 4–5 Zirkulations-Segmente, keine
   Garage-Fahr-/Gehwege → 29 GT-Einheiten im 2KG stehen 24 Engine-Symbolen
   an anderen Orten gegenüber. Ohne Räume/Wege kann keine Platzierungslogik
   der Welt die Experten-Spots treffen.
2. **Beidseitig-Entscheidung (NB-R16/E1):** baubereit erst, wenn (1) die
   Ströme an den Knoten existieren; das Kriterium „zwei Gegenströme auf einen
   Knoten" braucht die Zirkulation beider Seiten.
3. **Kabeltrassen (NB-R15/E3):** die LEEREN Architektur-Inputs enthalten
   KEINE KT-Daten (0 KT-Texte im 2KG-Input) — Regel steht in der Regelbasis,
   Integration braucht einen Input-Kanal (Elektro-Fachplanung als Overlay
   oder LB-Angabe). Extraktions-/Nachpass-Muster liegen bereit
   (`bestand_leuchten.py`/`abstand_nachpass`).
4. **Gebäudehälften (NB-R18/E5):** Ansatz = Zirkulations-Graph-Komponenten
   (disconnected-graph-Anker existiert); ob das RaumModell die Trennung
   trägt, entscheidet Selmans Zirkulation. Prozessregel „nie raten" gilt.
5. **Garage-Stellplatz-Klassen (NB-R17/E6):** Stellplatz-/Doppelparker-/
   Motorrad-Geometrie ist nicht im Contract — 3-Owner-Thema.
6. **Front-/Rotations-Semantik (NB-R06/R07/E2):** wartet designgemäß auf die
   D3-Owner-Diff-Runde (Handoff-Beschluss; Call-Sites erst nach Owner-Review
   drehen).
7. **Aufheller-Überproduktion EG** (S4-Kalibrier-Lane, bekannt).
8. **Wand-/Deckenmontage (NB-R14)** ist im Datenmodell nicht repräsentiert
   (2D-Contract kennt nur `height_mm`).
9. **Tür-RZ-Versatz:** GT misst 711–930 mm zugangsseitig, Engine steht seit
   `e5ac91b` auf Wandlinie (Owner-Ansage 18.09.) — die beiden Owner-Signale
   sind noch nicht konsolidiert (Kalibrierfrage, s. regeln.md Integration).

## L. Offene Fragen (nur echte)

`knowledge/notbeleuchtung/offene_fragen.md` Punkte 27–34, insbesondere:
PDF-Textfehler S.57 B↔C (bitte fixen wie die 4 vom 18.09.) · KT-Label-
Konvention (KT300/400/500 vs. „KT UK=+2,11", Rigole≠KT bestätigen) ·
FREIHEIT/KEINE-FREIHEIT-Wortbedeutung (Rest von Frage 23) · RZ-Zweitgröße
446 mm (Alt-Frage 6) · Tür-RZ Wandlinie vs. 711–930 mm (K.9) ·
Skalen-Abnahme der 883er-Reihe (Probe-PDF vom 18.09., jetzt faktisch durch
die Rivoplan-Legende re-bestätigt — bitte formal abnehmen).
