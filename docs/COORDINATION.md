# COORDINATION — 2-Fenster-Parallelbetrieb

**Zweck:** Zwei Claude-Code-Sessions arbeiten parallel in getrennten Worktrees. Diese
Datei ist das gemeinsame Board — **beide Fenster lesen + pflegen sie**. Da Sessions
keinen Live-Speicher teilen, läuft die Kommunikation über **Git** + diese Datei.

## Aufteilung (kein Datei-Overlap)

| Fenster | Ordner | Branch | Bereich |
|---|---|---|---|
| **F1** | `Notbeleuchtung/` | `leonis/anker-platzierer` | `src/notbeleuchtung/platzierung/` + `hauptengine/` — Platzier-Pipeline (Anker/Linie/Fläche/Deckung) |
| **F2** | `Notbeleuchtung-F2/` | `leonis/ldt-photometrie` | `src/notbeleuchtung/normwissen/photometrie/` — (b) IES/LDT-Import → exakte Lux |

## Regeln (bindend)
- **Eigenes Package = frei** parallel bearbeiten.
- **`hauptengine/contracts/**` = Konsens** (Contract-Freeze-Regel, beide Fenster + Version-Bump). Wer einen Contract ändern will → hier eintragen + abwarten.
- **Kleine Commits**, eine Sache pro Commit. Nach jedem Schritt Status unten aktualisieren + committen.
- **Sync:** `git fetch` + `git show origin/<other-branch>:docs/COORDINATION.md` (oder Board unten lesen). Das andere Fenster sieht Änderungen erst nach Fetch/Pull.
- **Naht/Lux:** F2 liefert `photometrie`-API; F1 konsumiert sie später in `platzierung/lux.py`. Schnittstelle unten festhalten, bevor F1 sie einbaut.

## Schnittstelle F2 → F1 (Lux-Photometrie)
F2 baut: `normwissen/photometrie/ldt.py` mit
`lade_ldt(pfad) -> Photometrie` und `Photometrie.intensitaet(gamma_grad, c_grad) -> cd`.
F1 tauscht dann in `platzierung/lux.py` das konstante `i_cd` gegen `Photometrie.intensitaet`.
**Contract bleibt unberührt** (rein additives Modul). → wenn API steht, hier „READY" markieren.

**READY** (F2, 2026-08-30): `normwissen/photometrie/{ldt.py,__init__.py}` steht.
`lade_ldt(pfad) -> Photometrie` (EULUMDAT, alle Isym-Symmetrien) +
`Photometrie.intensitaet(gamma_grad, c_grad=0.0) -> cd` (bilinear γ×C, cd über
`lampen_lumen` skaliert). F1 kann `lux.py` umstellen. Noch offen: Test gegen echte
Schrack-LDT (Owner besorgt Datei) — bis dahin synthetische Fixture `tests/fixtures/photometrie/mini.ldt`.

## Status-Board (live — nach jedem Schritt updaten + committen)

### F1 (Platzierung)
- [x] (a) Anker-Platzierer (`anker_strategy`) — committed
- [x] (b-vorbereitet) `mittellinie` + `lux` — committed
- [x] (c) `place()` Durchstich Anker→Linie→Fläche→Deckung (`deckung.py`) — committed
- [x] `lux.py`/`deckung.py` auf F2-Photometrie umstellbar: neues `i_cd_fn(γ)`-Callable
  (Dependency-Injection, KEIN `normwissen`-Import → Import-Grenze gewahrt); Hauptengine
  baut es aus `Photometrie.intensitaet`. Fallback bleibt konstant `i_cd`. (Branch `leonis/lux-photometrie`)
- [ ] offen: PR für anker-platzierer-Branch; Hauptengine/pipeline: `i_cd_fn` real verdrahten

### F2 (Photometrie / LDT)
- [x] `normwissen/photometrie/ldt.py` — LDT/EULUMDAT-Parser (Kopf + Lampensatz + Isym-Expansion)
- [x] `Photometrie.intensitaet(gamma, c)` mit Winkel-Interpolation (bilinear γ×C, periodisch)
- [ ] Test gegen eine echte Schrack-LDT (Owner besorgt Datei) — bis dahin synthetische Fixture
- [x] API READY-Meldung hier → F1 baut sie in `lux.py` ein

### F2 → umgelenkt auf Raumerkennung (Selman-Package)
Branch `selman/raumerkennung-dxf`. Baut echten `ArchitekturRaumProvider.parse(dxf, floor)
-> RaumModell` (ersetzt `FakeRaumProvider` schrittweise). Schlanker Neubau in
`raumerkennung/`, wiederverwendet pure Port-Helfer (`room_faces`, `classify_room`).
Primärziel Mollgasse (mm). **Kein Contract-Touch** (rein additiv). E2E bleibt vorerst
auf Fake (4OG-Golden matcht keinen echten DXF) — Fake-Swap = späterer Slice mit F1-Konsens.
- [x] S0 Scaffold (`provider.py` Stub, `tests/raumerkennung/`) — Suite grün (69), committed
- [x] S1 `dxf_load` (öffnen + $INSUNITS→mm + `bounds_mm`) — Mollgasse-Test grün (71), committed
- [x] S2 `waende` (Segmente → `extract_room_faces` → Räume) — **synth grün (2 Räume)**, aber
  ⚠️ **echte Mollgasse = 184 Wand-Schlitze statt Räume** (Doppellinien-Wände + Türlücken).
  Naive Polygonisierung UND shapely-Buffer-Difference scheitern ohne Gap-Healing/virtuelle
  Wände (= die 14k-LOC-Port-Maschinerie). Offene Design-Frage an F1/Owner (siehe unten).
- [x] S4 `tueren` (TÜR-INSERTs → `Tuer`, Breite aus Blockname cm→mm) — **Mollgasse echt grün**
  (≥10 Türen, Achsmarker/Türöffner ausgeschlossen). Suite 75.
- [x] S5 `zirkulation` (09-WEG → `FluchtwegSegment` + networkx-Graph + Ausgänge) —
  **Mollgasse echt grün** (77 Weg-Polylinien → Segmente + Knoten/Kanten). Suite 77.
- [x] S3 `raumtyp` (Stempel → raum_typ + Flags, Point-in-Polygon) — synth grün.
- [x] S6 `provider.parse` full → valides `RaumModell`, Contract-Roundtrip grün. Suite **80**.
- Reihenfolge: Owner wählte **B** — erst Türen/Fluchtweg (echt-nutzbar), Raum-Polygone später.

**Raum-Layer-Reader (`raumlayer.py`) — echte Raum-Polygone:** 3 von 4 Familien haben
fertige Raum-Polygone auf Layern (`81\d Raum`/`Raumbegrenzung`/`A_Raeume`) + Name via
`ROOM_NAME`-ATTRIB oder MTEXT → `classify_room`. Löst das Schlitz-Problem auditierbar
(kein ML). Fischamender **68**, Herrenholz **473**, Baufeld **220** echte typisierte Räume;
Mollgasse Fallback Wand-Polygonize. Suite **93**. (Barawitzka 2 = Nacharbeit.)

**Cross-Projekt-Fundament (alle 5 Familien):** Wand-Layer per Muster (`WALL_PATTERN`:
`02-TWA/ZWA/WDA` · `A_Waende` · `1[123]0 Wand`) + Skala robust (Span-Gate 15–500 m +
Tür-ARC-Radius-Tiebreak). Korrekt für Mollgasse/Fischamender/Barawitzka(80m, war 8m!)/
Herrenholz. Hauptausgang-Doppeltür bisher nur Mollgasse kalibriert; Fischamender braucht
Block-Descent (Tür-ARCs nested), Barawitzka schärferes Paar-Kriterium. Suite **91**.

**FIX-2/3 Hauptausgänge = DOPPELTÜR am Rand (`footprint.py`):** Owner-Muster: Gebäude-
Haupteingang wird als **Doppeltür** gezeichnet, 1–2 je Gebäude/Stiegenhaus. Naive Geometrie
(Polygonize/Buffer/Hülle) scheitert am lückigen nicht-konvexen Wandwerk → **Raster-Flood-
Fill** für Gebäude-Umriss. Hauptausgang = Paar gleich großer Tür-Schwenkbögen (ARCs,
r≈600–1300mm, Drehpunkte 1.4–2.6m auseinander) **an der Außenkante**. Mollgasse EG:
**4 Hauptausgänge**, beide Blöcke/Stiegenhäuser. Suite **87**. Cross-Projekt-Profile offen.

**FIX-1 (Ausgänge + Skala, nach Projekt-Analyse aller 6 Ordner):**
- **Ausgänge neu = Außentüren** (`WET_AUSSEN`/`WET`/`SCHIEBETÜR`/`Fenstertür`, `final_exit`).
  Alte Heuristik (09-WEG-Endknoten nahe Bounding-Box) war Müll (11 Punkte am Planrahmen)
  → jetzt 6 echte Egress-Türen. Ground-Truth-Abgleich: sitzen an/nahe den RZ.
- **Skala aus Geometrie kalibriert** (Dekaden-Snap), `$INSUNITS` ignoriert — leerer
  Mollgasse-Input steht in METERN (×1000), fertiger in mm. Beide deklarieren fälschlich `4`.
- Analyse aller Projekte: 3 Konventionen (Mollgasse `02-*`, Fischamender `A_*`, ArchiCAD
  numerisch `1xx/8xx`), 3 leere Inputs haben **Raum-Polygone auf eigenen Layern**
  (`_815`/`810 Raum`/`A_Raeume`) → löst Schlitz-Problem (nächster Slice). Suite **86**.

**READY (Teil-Naht):** `ArchitekturRaumProvider.parse(dxf, floor) -> RaumModell` steht.
Echte Mollgasse-EG: **40 Türen, 11 Ausgänge, 103 Fluchtweg-Segmente, Bounds** — echt
nutzbar für Leonis/Render. ⚠️ **Raum-Polygone** (184 Wand-Schlitze) noch NICHT
produktiv — brauchen Gap-Healing (Folge-Slice). E2E-Fake-Swap erst mit neuer Golden
(F1-Konsens). Branch `selman/raumerkennung-dxf` bereit für PR (User-GO nötig).

**OFFENE FRAGE (Owner):** Echte Raum-*Polygone* brauchen dicke-Wand-Handling. Türen
(INSERT) + Fluchtweg (09-WEG) funktionieren dagegen JETZT auf echten Plänen. Optionen:
(A) Port-Maschinerie reanimieren (virtuelle Wände/room-partition, ~14k LOC), (B) erst
Türen+Fluchtweg+Bounds liefern, Raum-Polygone nur auf sauberen DXF, (C) mittlere
Heuristik (Tür-Öffnungs-Virtualwände selektiv portieren).

## Bugs an F2 (aus F1-Durchstich Fischamender BT1 1.OG, 2026-08-29)
F1 hat den echten End-to-End (Provider → Platzierung → DXF) auf **Fischamender BT1
1.OG** gefahren. Zwei reproduzierbare Provider-Bugs auf dieser CAD-Familie:

- **B1 — Tür-Doppelzählung.** `tueren_aus_dxf` liefert **102** INSERTs, davon **~42
  Quasi-Duplikate <20 cm** (jede Tür als 2 ARC-Schwenkbögen gezählt) → echte ~60.
  Fix: Dedup-Cluster (<300 mm) je Tür-Position, ODER nur einen ARC/INSERT je Türblatt.
- **B2 — A_Fluchtweg + Ausgänge werden nicht gelesen (Fischamender-Familie).**
  `zirkulation_aus_dxf` sucht Mollgasse `09-WEG`; Fischamender-Fluchtweg liegt auf
  **`A_Fluchtweg`** (23 Ent., HATCH-Pfeile + degenerierte Linien, Rohkoords Meter).
  `hauptausgaenge` (footprint) ist nur Mollgasse-kalibriert. Folge: **0 Ausgänge,
  0 Zirkulation** → RZ-Routing unmöglich, F1 musste das Stiegenhaus aus dem
  **`S-STRS`**-Layer (×`plan.factor`) improvisieren. Fix: Layer-Muster + Ausgangs-
  Erkennung pro Familie (wie Wand-Muster `WALL_PATTERN`). Ein Stiegenhaus-Cluster
  für BT1 bei mm (20928, 85023).
- Nebenbefund: **20 von 59 Raum-Polygonen** sind Fragmente/untypisiert (Median 6,6 m²,
  9 unter 2 m²) — bekannte Gap-Healing-Grenze, hier bestätigt.

## Enis-Lane (Normwissen) — Naht-Erwartungen

Enis arbeitet in einer eigenen Session auf `enis/…`-Branches. Zwei Provider aus
`normwissen/` fehlen noch; beide Contracts stehen bereits auf main:

| Zu bauen | Protocol (`ports.py`) | Datengrundlage | Status |
|---|---|---|---|
| `normwissen/oib/` | `OibProvider.bewerte_oib(projekt) -> OibBefund` | `normwissen/data/oib_rl2_tabelle6.yaml` (neu) | TODO |
| `normwissen/lb/` | `LBProvider.parse_lb(lb_path) -> LBVorgabe` | reale LBs, Digest `knowledge/extracted/LB_ANALYSE_beispiele.md` | TODO |

**Bitte an Leonis (blockiert den LB-Parser fachlich, nicht technisch):**
`BereichsRegel.raum_typ` muss exakt Selmans `RaumModell.raum_typ`-Vokabular
treffen (`STIEGENHAUS`/`GANG`/`GARAGE`, …). Wo ist die Liste kanonisch? Solange
das offen ist, parst Enis die LB-Bereiche auf genau diese drei Strings und
markiert alles andere als „nicht zuordenbar" statt zu raten.

**Naht ohne Abnehmer:** `pipeline.run()` nimmt weder `ProjektKontext` noch LB;
`ProviderBundle` hat weder `oib`- noch `lb`-Feld. PR #23 schließt die LB-Hälfte
(`ports.py` + `pipeline.py`, 3-Owner) — die OIB-Hälfte bleibt danach offen.

**Norm-Ausgabe-Bezeichnung:** `ÖNORM EN 1838:2013` bleibt vorerst stehen, obwohl
im Repo 2019-11-15 liegt (inhaltlich deckungsgleich). Grund: der String ist
Naht-Invariante und steckt auch in `tests/fakes.py` und
`tests/platzierung/test_flaechen_strategy.py:53`. Umstellung nur gemeinsam
(Fixture-Regen aus dem echten Provider) — Details `docs/NORMQUELLEN_AT.md` 2a.

## Log (append-only, neueste oben)
- 2026-08-30 Enis: OIB-/OVE-/Rechtsquellen-PDFs ins Repo (`knowledge/`), Beleg-Status
  je Wert in `normwissen/data/*.yaml`, Spec auf PR #14 nachgezogen. Kein Code-Delta
  (144 passed / 5 skipped wie main, schema in sync).
- 2026-08-30 F1-Naht: `lux.py`+`deckung.py` bekommen `i_cd_fn(γ)`-Callable (Photometrie-Injektion, grenz-sauber). 77 Tests grün. Verdrahtung in Hauptengine/pipeline noch offen.
- 2026-08-30 F2: `photometrie/ldt.py` + `__init__.py` + Fixture `mini.ldt` + `tests/normwissen/test_ldt.py`. 74 Tests grün, ruff clean. Schnittstelle READY (siehe oben).
- <2026-08-29> F1: Platzier-Regeln l=z·h + `richtung_durch_tuer` kodiert (Commit
  `e87a745`, Suite 95). Fischamender-Durchstich + DXF-Overlay in echten Grundriss.
  2 F2-Bugs oben dokumentiert. ⚠️ F1-Platzier-Code liegt versehentlich auf
  `selman/raumerkennung-dxf` (Git-Tangle) — Integration/Entwirrung offen.
- <S0> F2 umgelenkt → Raumerkennung. Branch `selman/raumerkennung-dxf`, Scaffold + Test grün (69 passed).
- <setup> F1 legt Worktree + dieses Board an. F2 startet mit (b) LDT.
