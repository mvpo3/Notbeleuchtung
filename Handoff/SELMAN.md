# Handoff — Selman (Raumerkennung)

> Claude: Du bist die Session von **Selman**. Owner-Package:
> `src/notbeleuchtung/raumerkennung/`. GitHub `@polatselman`. Task: **Issue #3**.
> Lies zuerst `CLAUDE.md`, `docs/CONTRACTS.md`, `docs/ONBOARDING.md` (Abschnitt Selman).

## 0. Setup — Claude, führe das ZUERST für den Nutzer aus

Du bist ein Agent — **führe diese Schritte selbst aus**, frag nicht lang nach.

1. **Prüfe den Arbeitsordner:** du musst im Repo-Root `Notbeleuchtung/` sein
   (`pyproject.toml` + `CLAUDE.md` liegen hier). Wenn nicht → sag dem Nutzer:
   „Öffne den Ordner `Notbeleuchtung` (Cursor: File → Open Folder → Notbeleuchtung)
   und starte mich dort neu." Erst weiter, wenn der Ordner stimmt.
2. **venv + Installation:**
   - Windows: `python -m venv .venv` → `.venv\Scripts\python.exe -m pip install -e ".[dev,api]"`
   - Mac/Linux: `python3 -m venv .venv` → `.venv/bin/python -m pip install -e ".[dev,api]"`
3. **Tests grün prüfen:** `.venv\Scripts\python.exe -m pytest -q` → muss zeigen
   **`13 passed, 1 skipped`**. Wenn nicht → stopp + melde dem Nutzer den Fehler.
4. **Cursor-Hinweis für den Nutzer:** Ordner `Notbeleuchtung` als Workspace öffnen
   und `.venv` als Python-Interpreter wählen (unten rechts / Command Palette
   „Python: Select Interpreter" → `.venv`).

Erst wenn Setup grün ist → weiter mit dem Auftrag unten.

## Wer du bist
Du machst den **1. Input**: leerer Architekturplan (DXF/DWG) → **RaumModell**
(Räume/Türen/Ausgänge/Fluchtweg-Zirkulation). Reine Geometrie/Topologie — KEIN
Norm-Urteil (das macht Enis/Leonis). Dein Contract: `RaumModell`
(`hauptengine/contracts/raum_modell.py`), dein Protocol: `RaumProvider`.

## Dein Auftrag — Slice 4 (größter Port, deshalb solide angehen)
Das Port-Material liegt schon im Repo (Leonis hat es gestaged, du hast keinen
elektro-planer-Zugriff): **`raumerkennung/_port/`** (~14,4k LOC — `parsers/`,
`engine_walls/`, `models/`). Es ist ROH und läuft noch nicht (alte Imports). Deine
Aufgabe (Details: `raumerkennung/_port/README.md`):

1. **Imports umbiegen** auf die neue Struktur (`engine.walls` → `._port.engine_walls`,
   `parsers.x` → `._port.parsers.x`).
2. **`config.py`-Kopplung brechen:** harte Mollgasse-Pfade (`CANONICAL_BLANK_DIR`,
   Referenz-DXF) optional/`.env`; nur `RULES_DIR`/`resolve_rule_path` behalten.
3. **Zirkular-Import** `keller_geometry` ↔ `architecture_dxf` sauber trennen.
4. **`ArchitekturRaumProvider.parse(dxf, floor)`** (`raumerkennung/provider.py`)
   erfüllt `RaumProvider` → liefert ein `RaumModell`, schema-gleich zu
   `tests/fixtures/raum_modell_4og.json`. Test-Pläne: `Projekte/`.
5. **Fake ersetzen:** `tests/fakes.py` `FakeRaumProvider` → echt; E2E mit echter
   4OG-DXF grün.

**Tipp:** nicht alles auf einmal. Erst `architecture_dxf` + `keller_geometry`
importierbar machen → Räume/Türen extrahieren → dann Fluchtweg-Zirkulation
(`segmente`) füllen. Zwischendrin `pytest -q` grün halten.

**DoD:** echtes RaumModell aus 4OG-DXF, schema-identisch zur Fixture;
`tests/contract/test_raum_modell_contract.py` grün.

## Regeln
Nur `raumerkennung/` + `hauptengine.contracts` importieren (der `_port`-Code darf
intern untereinander importieren). Contract ändern = version bump + gen_schema +
3-Owner-Approval. Branch `selman/…` → PR.

## STAND (append-only, neueste oben) — für nahtloses Weitermachen

### 2026-08-29 — Türen über ALLE Familien (F1-Naht: `richtung_durch_tuer`)
F1-Hinweis: `richtung_durch_tuer` greift automatisch, sobald echte `RaumModell.tueren`
an den realen Öffnungen stehen. → F2-Job: `tueren` pro Familie vollständig.
Vorher nur Mollgasse(44)+Fischamender(114); Barawitzka/Herrenholz/Baufeld = **0**.

`tueren.py` erweitert (3 Darstellungen):
1. Benannte Blöcke: `TÜR…` + jetzt auch `ÖFFNUNG` (Baufeld-Marker) + Außentür-Namen.
2. **ARC-Fallback** (ArchiCAD ohne Türblöcke): je Schwenkbogen (r 600–1300mm) eine Tür
   am Drehpunkt, Breite = Radius. Greift nur, wenn (1) leer.
3. Breite: cm-Konvention (`TÜR-80`→800) ODER mm direkt (`_0800x2000`→800).

**Ergebnis:** Mollgasse 44 · Fischamender 120 · Barawitzka **116** · Herrenholz **140** ·
Baufeld **191** — alle Familien liefern echte Tür-Positionen → F1 entblockt. Suite 95.
Caveat: ARC-Türen evtl. Doppelzählung (Doppeltür=2 ARCs); Baufeld-Öffnungen ggf. inkl.
Fenster; Positionen aber real.

### 2026-08-29 — Raum-Layer-Reader: echte Raum-Polygone (löst Schlitz-Problem)
Auf Basis des „Schritt-6"-Vorschlags (Face-Clustering), aber die auditierbarere/
billigere Variante: **3 von 4 Input-Familien haben fertige Raum-Polygone auf eigenen
Layern** → direkt lesen statt clustern. `raumlayer.py::raeume_aus_layer(plan)`:
- Raum-Poly-Layer per Muster (`81\d Raum` · `Raumbegrenzung` · `A_Raeume`, ohne Icon),
  geschlossene LWPOLYLINE → Polygon + Fläche.
- Name aus `ROOM_NAME`-ATTRIB (Herrenholz/Baufeld) ODER MTEXT im Polygon
  (Barawitzka/Fischamender) → `raumtyp_flags` (neuer Public-Helper in `raumtyp.py`).
- Provider: `raeume_aus_layer` bevorzugt, sonst Wand-Polygonize-Fallback (Mollgasse).

**Output-Wandel (echte Räume + Typen statt Schlitze):**
Fischamender **68** (45 typisiert: ZIMMER/GANG/BAD/WC/KÜCHE) · Herrenholz **473** ·
Baufeld **220** · Mollgasse Fallback 184 (kein Raum-Layer) · Barawitzka nur **2**
(Polygone liegen wohl auf Icon/LINE — Nacharbeit). Viz:
`output/RaumModell_Fischamender_EG_HQ.png` (Gänge sauber als Erschließung erkannt).
Suite **93**, ruff sauber.

Offen: Barawitzka-Raum-Polygone (Icon-Layer/LINE-Loops); Mollgasse-Räume brauchen
weiterhin Face-Clustering (Union-Find, nicht DBSCAN) da kein Raum-Layer.

### 2026-08-29 — Cross-Projekt-Fundament: Wand-Layer + Skala über alle 5 Familien
Ziel (Owner): Muster über alle Projekte, Haupteingänge in JEDEM Projekt erkennen.

**Generalisiert (getestet, Suite 91):**
- **Wand-Layer per Muster** statt fixem Prefix (`dxf_load.WALL_PATTERN`):
  `02-TWA/ZWA/WDA` (Mollgasse) · `A_Waende` (Fischamender) · `1[123]0 Wand` (ArchiCAD:
  Barawitzka/Herrenholz/Baufeld, auch mit `_Stift_Nr__N`). `DxfPlan.wall_entities()`.
- **Skala robust** (`_calibrate_factor`): Span-Gate 15–500 m (killt falsche Klein-Dekade),
  Tür-Schwenkbogen-Radius (~0.9 m) als Tiebreak. Ergebnis korrekt für ALLE:
  Mollgasse leer 54.6×48.4m (×1000) · fertig (×1) · Fischamender 53×95m · Barawitzka
  80×36m (vorher fälschlich 8m!) · Herrenholz 215×64m.
- Synth auf 20×12 m vergrößert (Span-Gate braucht ≥15 m); Tests angepasst.

**Hauptausgang-Status je Familie:**
- Mollgasse: **4** (Doppeltür am Rand) ✓.
- Barawitzka: 116 Tür-ARCs (800/900/1000mm ✓), 59 Doppeltür-Paare erkannt, aber alle
  INNEN → 0 am Rand. Braucht eigene Kalibrierung (Paar-Kriterium enger; andere
  Eingangs-Darstellung). Umriss OK (37% außen).
- Fischamender: nur 7 Tür-ARCs top-level — Rest **nested in `A_Tueren`-Blöcken** →
  `_schwenkboegen` muss in Tür-Blöcke absteigen (INSERT-Transform anwenden).
- Herrenholz/Baufeld: analog ArchiCAD, noch offen.

**Nächster Schritt:** (a) `_schwenkboegen` in Blöcke absteigen (Fischamender);
(b) Doppeltür-Paar-Kriterium schärfen (gleiche Wand, gegenläufige Flügel) gegen die 59
Barawitzka-Falschpaare; (c) je Familie an einem Geschoss validieren. Raum-Polygone aus
Raum-Layern (`_815`/`810`/`A_Raeume`) bleibt ebenfalls offen.

### 2026-08-29 — FIX-3 Hauptausgang = DOPPELTÜR am Rand (Fachmuster vom Owner)
Owner-Regel: **Gebäude-Haupteingang wird als Doppeltür gezeichnet** (2 Flügel), 1–2 je
Gebäude/Stiegenhaus; Muster über alle Projekte lernen. Perimeter-Tür allein war zu grob
(18 inkl. Fassaden-Wohnungstüren).

**Signatur Doppeltür (Mollgasse):** zwei Schwenkbögen (ARC, r≈600–1300mm = Tür-Blattbreite)
gleicher Größe, Drehpunkte 1.4–2.6m auseinander (= Öffnungsbreite). ARC-Paar **an der
Gebäude-Außenkante** (Raster-Umriss-Rand) = Hauptausgang. `türachse&qualität` (33×) =
vollständige Tür-Positionsquelle (nicht Noise!) — für spätere Verfeinerung.

`footprint.py::hauptausgaenge(plan, bounds)`: Raster-Umriss (mit Padding > Schließ-
Dilatation!) → Rand-Band → Doppeltür-ARC-Paare am Rand. Mollgasse EG (leer + fertig):
**4 Hauptausgänge** (1 links Hof + 3 rechts), deckt beide Stiegenhäuser/Blöcke. Provider:
`ausgaenge = hauptausgaenge(plan, bounds)`. Alte Perimeter-/Namensheuristik entfernt.
Suite **87**, ruff sauber. Viz: `output/hauptausgaenge_final_EG.png`.

Offen: Rechter Block 3 (evtl. 1 Loggia-Doppeltür zu viel) — Rim-Toleranz feinjustieren.
**Cross-Projekt:** Doppeltür-als-2-ARCs ist Mollgasse-Muster; Fischamender (`A_Tueren`
benannte Blöcke `…Wohnungstür…`) + ArchiCAD (keine Türblöcke, nur ARC-Schwenk) brauchen
je eigenes Doppeltür-Erkennungs-Profil. Muster-Lernen über Profile = nächster Schritt.

### 2026-08-29 — FIX-2 Hauptausgänge via Raster-Umriss (`footprint.py`)
User: „du erkennst die Hauptausgänge nicht" + 4 Beispielbilder (Mollgasse EG).
Definition bestätigt: **Hauptausgang = Tür in der Außenwand, die nach außen führt**
(Vorplatz/Hof), im fertigen Plan mit grünem RZ + Richtungspfeil.

Erprobt + verworfen (alle scheitern am lückigen, nicht-konvexen Wandwerk):
Wand-Polygonize→Schlitze · Wand-Buffer-Union→239m²-Fragment · konvexe Hülle→Türen
1.8–14m daneben · WET_AUSSEN-Namensheuristik→geraten · Fluchtrichtungspfeil-Block→im
Plan 0 (Pfeil steckt im RZ). RZ sitzen an `türachse&qualität`-Markern (jede Tür), nicht
nur an Hauptausgängen.

**Lösung `footprint.py` (nur scikit-image):** Wände rastern (200mm) → `disk(5)` dilatieren
(Türlücken schließen) → `label(~closed)`, Ecke=außen fluten → Gebäude-Innen/Außen.
**Hauptausgang = Perimeter-Tür** (Türzelle ∈ dilatierter Außen-Maske). Mollgasse EG:
**6 Perimeter-Türen, alle am Vorplatz/Hof — Owner bestätigt „im Wesentlichen richtig".**
Provider: `ausgaenge = ausgaenge_aus_umriss(plan, tueren, bounds)`. Suite **88**, ruff sauber.
Viz: `output/hauptausgaenge_perimeter_EG.png`.

Offen: rechter Gebäudeblock hat 0 Kandidaten (eigener Eingang? prüfen); ggf. 6→4
verschärfen (Türbreite). `footprint`-Umriss ist auch Basis für Raum-Extraktion (Innen-Blob).

### 2026-08-29 — FIX-1 Ausgänge + Skala (nach Analyse ALLER 6 Projekte)
User-Feedback: „Ausgänge falsch". Ursache: Heuristik „09-WEG-Endknoten nahe Bounding-Box"
→ 88 fragmentierte 2-Punkt-Segmente, deren Enden am **Planrahmen** liegen (die 09-WEG-
Annotation ist kein begehbarer Weg). Ergab 11 Müll-Ausgänge.

**Projekt-Analyse (4 Agenten, alle Ordner):**
- 3 Layer-Konventionen: Mollgasse (`02-TWA/09-WEG/TÜR-80`), Fischamender (`A_Waende/
  A_Tueren/A_Raeume/A_Fluchtweg`), ArchiCAD-numerisch (`110/120/130 Wand`, `810/815 Raum`
  + `ROOM_NAME`-ATTRIB) für Barawitzka/Herrenholz/Baufeld.
- **`$INSUNITS` lügt überall**: leere Pläne in METERN, fertige in mm, beide oft Code 4/6.
- **Kein Plan hat ein explizites Ausgang-Symbol.** Fertige Pläne: RZ/Sicherheitsleuchten
  auf `E_Sicherheitsbeleuchtung` (ATTRIB `ANLAGE='Eak'`) bzw. `dp_GE_SIBEL` = OUTPUT.
- **3 leere Inputs haben fertige Raum-Polygone** auf `_815`/`810 Raum`/`A_Raeume` → der
  Schlitz-Problem-Killer (nächster Slice: Raum aus Layer statt Wand-Polygonisierung).
- Ich hatte gegen die FALSCHE Datei getestet: `WHA_MOL_EG.dxf` = fertig (Output). Echter
  Input = `Projekte/Mollgasse/Erdgeschoß.dxf` (Meter).

**Gefixt (Owner-Wahl: Außentüren + Skala-Fix):**
- `dxf_load._calibrate_factor`: mm-Faktor per Dekaden-Snap aus Wand-Ausdehnung (Input
  Meter→×1000). `$INSUNITS` nur noch Fallback.
- `tueren.ausgaenge_aus_dxf`: Ausgang = Außen-/Eingangstür (`WET_AUSSEN`/`WET`/`SCHIEBETÜR`/
  `Fenstertür`), `typ=final_exit`; Außentüren tragen `ist_notausgang=True`.
- `zirkulation`: Ausgang-Erzeugung entfernt (nur noch Segmente+Graph), `reason` ohne Rand.
- Provider zieht Ausgänge aus Türen. Mollgasse: 11 Müll → **6 echte Außentüren**. Suite **86**.

**Nächster Schritt (empfohlen):** Raum-Polygone aus den Raum-Layern (`_815`/`810`/
`A_Raeume`) statt Wand-Polygonisierung — löst die 184-Schlitze für 3 Projekte. Danach
Parser-Profile (Mollgasse / A_* / ArchiCAD-numerisch) trennen.

### 2026-08-29 — S3–S6 fertig: parse() steht, Teil-READY (Owner-Weg B)
Owner-Entscheidung: **B** — erst die Teile bauen, die auf echten Plänen JETZT gehen.

**Fertig & echt grün auf Mollgasse-EG** (`ArchitekturRaumProvider.parse`):
- `tueren.py` (S4): 40 Türen, Nennbreite aus Blockname (cm→mm, erste Zahl 60–130),
  Achsmarker/Türöffner ausgeschlossen.
- `zirkulation.py` (S5): 09-WEG LINE/LWPOLYLINE → 103 `FluchtwegSegment` + networkx-Graph
  (gesnappte Knoten) + 11 `Ausgang` (grad-1 an Außenkante).
- `raumtyp.py` (S3): MTEXT-Stempel → `classify_room` → `raum_typ`+Flags per Point-in-Polygon
  (synth deterministisch; auf echt limitiert durch fehlende Raum-Polygone).
- `provider.py` (S6): verdrahtet alles, `RaumModell.model_validate`-Roundtrip grün.
  Volle Suite **80 passed**, ruff sauber.

**Weiter offen — das harte Teil:** echte **Raum-Polygone** (184 Wand-Schlitze statt
Räumen). Nächster Slice-Kandidat: Tür-Öffnungs-Virtualwände + Fragment-Bridge aus
`_port/parsers/architecture_dxf.py` (`_build_virtual_walls_from_doors`,
`_build_fragment_bridges`) selektiv portieren, ODER room-partition via Anker/`assign_room`.
Erst DANN E2E-Fake-Swap (mit kuratierter neuer 4OG-Golden + F1-Konsens).

Branch `selman/raumerkennung-dxf` — bereit für PR (User-GO nötig, nicht gepusht).

### 2026-08-29 — S1+S2 fertig, HARTES PROBLEM gefunden (Raum-Polygone)
**S1** `dxf_load.py`: ezdxf öffnen, `$INSUNITS`→mm (Mollgasse=mm, factor 1.0),
Direct-Mode (797 Wand-Ents direkt im msp; Wrapper-Fallback vorhanden), `bounds_mm`.
Tests grün gegen echte Mollgasse-EG.

**S2** `waende.py`: Wand-Segmente (LINE + LWPOLYLINE explodiert) → Port-Helfer
`extract_room_faces`. **Synth (Einzellinien-Wände) = exakt 2 Räume, 25+15 m² ✓.**
ABER echte Mollgasse: 1005 Segmente → 184 „Räume" mit median 0.2 m² = **Wand-Schlitze**
zwischen den Doppellinien (10er/20er-Wand), NICHT echte Räume. Zweiter Versuch
shapely-Buffer-Difference (Wände puffern → aus Grundfläche subtrahieren): 1 Riesen-Blob
2400 m² weil Türlücken alles verbunden lassen. → **Naive Geometrie reicht für echte
Pläne NICHT.** Das ist genau das Problem, für das die `_port`-Maschinerie (virtuelle
Wände an Tür-/Fensteröffnungen `_build_virtual_walls_from_doors`, `_build_fragment_bridges`,
room-partition via `assign_room`, room-hatch-ranking) existiert. FIL-Hatches (LILA/ORANGE)
sind Belag-Muster, KEINE Raum-Polygone.

**ENTSCHEIDUNG offen (User gefragt):** (A) Port-Maschinerie reanimieren, (B) erst
Türen/Fluchtweg/Bounds liefern (funktionieren auf echt) + Raum-Polygone nur clean-DXF,
(C) mittlere Heuristik. `waende.raeume_aus_waenden` bleibt als clean-DXF-Pfad + Fallback.


### 2026-08-29 — S0 fertig (Branch `selman/raumerkennung-dxf`)
**Ansatz (entschieden):** NICHT die 14.4k-LOC `_port/` reanimieren, sondern schlanker
Neubau in `raumerkennung/`, der die *sauberen* Port-Helfer wiederverwendet:
- `._port.parsers.room_faces.extract_room_faces` — Wand-Segmente → Raum-Polygone (pure).
- `._port.models.room.classify_room` + `GERMAN_ROOM_TYPE_MAP` — Stempel→RoomType (pure).
Plan-Datei: `.claude/plans/du-bist-fenster-delightful-wozniak.md`.

**Gebaut:** `provider.py` (`ArchitekturRaumProvider.parse` Stub, erfüllt Protocol),
`__init__.py` export, `tests/raumerkennung/{conftest,test_scaffold}.py`. Suite grün
(69 passed). Baseline-Info: volle Suite ist heute **69** (nicht mehr 13/1 aus Handoff).

**Datenlage (DXF-Inspektion):** Mollgasse `Projekte/Mollgasse Notbeleuchtung/WHA_MOL_*.dxf`
= mm ($INSUNITS=4, Koords ~65k). Layer: Wände `02-TWA*/02-ZWA*/02-WDA*`, Text
`01-/03-/05-TXT*` (MTEXT), Türen `TÜR-80_*` (INSERT auf `05-SYM*`), Fluchtweg `09-WEG*`.
Baufeld E2 = Meter + andere Taxonomie (110/120/130-Blöcke) → deferred.

**Nächster Schritt:** S1 `dxf_load.py` — ezdxf öffnen, Modelspace/Wrapper-INSERT,
$INSUNITS→mm-Faktor, Layer-Prefix-Filter, `bounds_mm`. Test gegen `WHA_MOL_EG.dxf` (skipif).

**Naht-Warnung:** E2E NICHT auf echten Provider umstellen — 4OG-Golden (neg. Koords,
7 Symbole) matcht keinen echten DXF. Fake-Swap erst mit kuratierter neuer Golden + F1.
