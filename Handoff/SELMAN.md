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

### 2026-08-29 — FIX Ausgänge + Skala (nach Analyse ALLER 6 Projekte)
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
