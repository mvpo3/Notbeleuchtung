# Handoff — Leonis (Platzierung + Integration)

> Claude: Du bist die Session von **Leonis**. Owner-Package:
> `src/notbeleuchtung/platzierung/`. GitHub `@mvpo3`. Task: **Issue #2**.
> Du hast als Einziger elektro-planer-Zugriff → du stagst Port-Material für andere.

## STAND (2026-09-05, Session-Ende) — #115 GEMERGT: Blatt-Modus fixiert — HIER WEITER

**PR #115 GEMERGT** (main `a584bc6`, **738 grün** — Enis' Abend-PRs #109/#110/#113/#114
sind eingeflossen). Das Nacht-Paket, alles Owner-getrieben am 3-Geschoss-Wohnbau
(`scratchpad/spec_builder_v8.py` + `wohnbau_spec.json`, Output `output/wohnbau_v8_*`):

- **Blatt-Modus (Rivoplan-Vorlage) ist DER Ausgabeweg**: `Vorlagen-Legende/
  Notbeleuchtungspläne-Vorlage.dxf` jetzt VERSIONIERT; liegt sie im Repo, baut
  `_baue_blatt_layout` das Blatt im Modelspace (Paperspace-Viewports rendert ezdxf
  nicht maßstabstreu) — Grundriss ins Planfenster skaliert (Geschoss-Extents),
  Legenden-Symbolspalte bestückt, PLANINHALT=Geschoss.
- **Owner-Fixierung (aus `wohnbau_v7_dg_verbessert.dxf`)**: im Blatt-Modus KEINE
  Zusatz-Boxen — LB-Legende, Stückliste, Prüfbericht-Box, Belegungsliste, alter
  Plankopf, Vorlage-Anhang alle unterdrückt; das Blatt trägt alles. Prüfbericht/
  Belegung bleiben im Summary/API. Box-Pfad existiert nur noch als Fallback ohne
  Vorlage (Tests: Fixture `ohne_blatt` patcht `_blatt_vorlage_cache["doc"]=None`).
- **PROJEKT-Platzhaltertext raus** (lief über die Spalte; Owner trägt selbst ein).
- **Rivoplan-Logo**: Vorlage referenzierte das PNG absolut in Owner-Downloads →
  Repo-Kopie `Vorlagen-Legende/rivoplan_logo.png`, IMAGE wird beim Blatt-Bau
  skaliert mitkopiert. Zwei PDF-Backend-Fixes in `pdf_export`: AxesImage ohne
  extent (savefig-tight-Crash) + **ezdxf spiegelt IMAGEs vertikal** (Logo stand
  kopfüber; empirisch an der Vorlage verifiziert, AutoCAD war immer korrekt).
- **PDF-Ausschnitt hält jetzt wirklich** (`aspect adjustable='box'` statt datalim;
  matplotlib ignorierte set_xlim) — `dxf_zu_pdf(..., ausschnitt=blatt_bbox)`.
- **Naht-Notiz Enis**: sein neuer Regel-13-Sichtbarkeitstest (Prüfbericht muss
  gezeichnet sein) kollidierte mit der Blatt-Fixierung → Test läuft jetzt auf dem
  Fallback-Pfad; im Blatt-Modus lebt der Befund in Summary/API. Falls Enis
  Sichtbarkeit AM BLATT will → Owner-Entscheidung nötig (Blatt-Feld dafür?).

**Nächste Kandidaten:** Wohnbau-Demo als E2E-Fixture einfrieren? · Blatt-Feld für
Prüf-/Statusvermerk (Enis-Naht) · SPOT-Grafik · AP3-LDT · Enis-Follow-ups (EW
produktabhängig, Blendungs-I_max, Quellen-Naht).

## STAND (2026-09-05, Spätabend) — #112 GEMERGT: Vorlage + Legende + Anlage

**PR #112 GEMERGT** (main `6b1d49c`, **681 grün**), das Abend-Paket:
- **Stückliste = Profi-Legende mit Symbol-Spalte** (din-ACAD_TABLE-Vorbild; je
  Typ-Zeile das Katalog-Symbol klein voran; Fallback ohne typ_letter unverändert).
- **Gruppenbatterie-/SV-Anlagen-Symbol** (neuer Owner-Block): LB-explizit gezeichnet
  (`lb.system_typ` gesetzt) im Technik-/Batterieraum, Label + `batterie_standort`.
- **Owner-Plan-VORLAGE** (`Vorlage_Legende`, 415×550 units): JEDER generierte Plan
  bekommt den Legenden-Rahmen rechts (auto-skaliert auf Grundriss-Höhe). In-Band-
  Guard nimmt `category: vorlage` aus; Visual-Goldens bewusst regeneriert.
- Library-Update committet (inkl. mitgekommener Elektro-Blöcke aus E-Symbole).
- Wissens-Nachträge im `STROMKREISNUMMER_DWG.md`: Voll-Analyse (SIBEL-Farb-Layer,
  Symbol-Größen ~1 m, 18 Attribute dekodiert, Legende MIT Zubehör-Artikeln,
  System-GUID→Anlage) + **Symbol→Produkt-Zuordnung web-verifiziert: din nutzt die
  ANTIPANIKLEUCHTE AP3 als Universal-Leuchte** (Rolle ≠ Produkt; SPOT = SL-Rolle).
- `Vorlagen-Legende/Baulegende.*` auf main für Selman (EI-Klassen-Vokabular).
Offen: SPOT-Grafik (nice-to-have) · AP3-LDT in Photometrie-Katalog falls DIN-
Produktwahl · Enis-Follow-ups (EW produktabhängig, Blendungs-I_max, Quellen-Naht).

## STAND (2026-09-05, Abend) — Owner-Feedback-Session + #111 GEMERGT — HIER WEITER

**Alles auf main** (`97b8a1d`, **679 grün** inkl. Selmans neuem
`test_stempel_anker.py` — AIA-Kipp-Anleitung wird schon konsumiert!). Nach den
Rettungs-Merges #105/#106/#107/#108 kam die große **Owner-Feedback-Session am
H-Testgebäude** (synthetisches RaumModell, `scratchpad/demo_h_v*.py`) — der Owner
korrigierte DXF-Outputs in AutoCAD, wir lasen die Deltas aus und machten
Engine-Regeln daraus. **PR #111 GEMERGT** mit:
- **Tür-Rendering** (`_draw_tueren`: Schwelle+Blatt+Schwenkbogen, Notausgang
  doppelt; Wandrichtung = nächste Polygon-Kante).
- **Außenleuchte §4.1.2 b** (`aussen_strategy`: SL 1 m außerhalb jedes final_exit).
- **Pfeil-zur-Tür-Regel** (Owner-DXF-Korrektur): Ausgangs-RZ = unten-Block,
  rotiert zur Tür (Anlauf-Richtung wenn RZ auf Türposition).
- **Höhenkoten KOMPLETT raus** (Owner: projektabhängig) + **AGV-Stromkreis-Label
  je Symbol raus** (Owner: unnötig — Info lebt in Anlage/Kreis/Adresse-Zeile +
  Belegungsliste + XDATA).
- **Fluchtweg-Segmente in Notlicht-Grün** (true_color 30/180/80).
- **SL-Dubletten < 2 m mergen** (Owner-„falsch"-Marker: Sonderstellen-SL neben
  Verdichtungs-SL) — `abstand_nachpass._DUBLETTEN_ABSTAND_MM`.
- **Beschriftungs-Anti-Kollision gegen SYMBOLE** (Owner-Referenzbilder
  richtig/falsch-beschriftung-platziert.png): NODEID-Label Seitenwechsel +
  Stromkreis-Label-Kandidaten (war: Label lief durch Nachbar-Aufheller).
Offene Wissens-Gaps (Enis-Lane, in #111 protokolliert): produktabhängige
Erkennungsweite (z=100/200), Blendungs-I_max-Tabellen. Audit-Fehlalarm
dokumentiert: Kreuzungs-Pfeile waren korrekt (Dijkstra-Gefälle existiert).

## STAND (2026-09-05, Nachmittag) — Contract-Merges + Lost-Merge-Rettung

**Gemergt heute:** #101 · #102 · #104 (kleiner Aufheller) + durch Enis/Selman die
drei Contract-PRs **#93/#87/#96** (RaumModell v1.1.0 · NormRegelwerk v1.2.0 ·
PlatzierungsErgebnis v1.2.0). main `6a22b9a`+, 572 grün.

**⚠️ Lost-Merge-Vorfall:** die vier Konsum-PRs #88/#92/#95/#98 wurden in ihre
BASIS-Branches gemergt — Code erreichte main nie (COORDINATION-Log). Rettung als
saubere Neuschnitte, **4 offene PRs, Merge-Reihenfolge #105 → #106 → #107, #108
unabhängig**:
- **#105** = #98-Ersatz: Symbol-Datenmodell-Konsum (luminaire_id/schaltungsart/
  typ_letter + Typ-Letter-Stückliste), 580 grün.
- **#106** = #95-Ersatz + **Enis' Review komplett eingearbeitet** (Fallback-
  Kennzeichnung `_referenz` + hinweise; Prüfregeln 12/12b manuell-prüfen für
  §4.1.2-h/i-Stellen + besondere_gefaehrdung; ≤2-m-Nachpass-Test), 586 grün.
- **#107** = #88+#92-Ersatz: OIB-Gate (fail-closed + raum-genau) + ProjektKontext
  über HTTP; enthält #106-Commits (Diff schrumpft nach deren Merge), 613 grün.
- **#108** = Verdichtungs-Fix (Owner: „zu viele Aufheller"): Nachweis auf
  Mittellinie §4.2.1 + photometrischer Start-Abstand (`lux_punkte`/
  `max_leuchtenabstand_mm`) — **Mollgasse 28→18 SL**, alles ok, 572 grün.

**Weitere Kanonisierung heute:** Symbol-Library = `Notbeleuchtungssymbole.dxf`
(klein-Aufheller 342 mm; Blau-ACI→BYLAYER-Grün) · Produkt-Digest
`PRODUKTE_SCHRACK_DIN.md` (Schrack 21 Familien + DIN komplett; Cap 20 bestätigt,
EW 20m = S2-Scheibe, 8h≈halber Lichtstrom) · Muthgasse-Digest (AIA-Layer =
Crash-Ursache, FLW-L parsebar, Kipp-Anleitung an Selman) · Aushang-Digest mit
AT-Norm-Vergleich · Architektur-Diagramm `docs/architektur.png/svg` + Skript.

## STAND (2026-09-05, Vormittag) — #101 + #102 GEMERGT

**Beide PRs auf main** (`ee562e6`, **572 grün**, ruff clean, kein Contract):
- **#101 GEMERGT** (User-GO, DWG-Input via ODA + Muthgasse 5. Familie).
- **#102 GEMERGT** (User-GO): Stromkreisnummer-Labels **+ drei Owner-Feedback-
  Nachfixes in-Session**:
  1. Label-Position: NODEID-Offset **je Symbolart** (gemessene Halbbreite RZ 290/
     SL 435 + 280 Clearance) — erst mittig im Symbol, dann zu weit, jetzt knapp
     daneben; Höhenkote 150→90 (= Label-Größe).
  2. **SL rendert grün statt blau**: Library-Blöcke tragen explizite Blau-Farben
     (HATCH ACI 150), die den Layer-Grün-Override übergehen → `library.py` stellt
     blaue ACIs beim Import auf BYLAYER (+Regressionstest).
  3. **Kanonische Symbol-Library = `CAD_Symbole/Notbeleuchtungssymbole.dxf`**
     (Owner-Entscheidung: NUR noch diese Symbole; kuratierter 5-Block-Extrakt +
     Legende, gleiche Geometrie wie E-Symbole-Teilmenge). `_LIB_RELPATH`
     umgestellt, `sync_layers` legt den Grün-Layer immer an (neue Lib hat keinen
     Safety-Layer), Mapping: „unten"-Pfeil heißt neu `notbeleuchtung- richtungspfeil
     nach unten` (mit Bindestrich; `block_names()` normalisiert lowercase!).
     E-Symbole.dxf = nur noch Herkunfts-Referenz. `.gitignore`-Ausnahme.
- Lokaler Merge-Pull war von AutoCAD-File-Lock blockiert (User musste DXF
  schließen) + Stash-Roundtrip wegen identischer Working-Tree-Files.
- **Uncommitted lokal:** `E-Symbole.dxf`/`.bak` von AutoCAD modifiziert (Engine
  liest sie nicht mehr — Owner entscheidet committen/verwerfen); Muthgasse-ZIP.

Slice-Inhalt #102 (Kern):
- Digest-Empfehlung #1 (`STROMKREISNUMMER_DWG.md`): **Zuweisungs-Pass existierte
  schon** (`platzierung/circuit_zuordnung.py`, Cap 20 + DL/BL) — gefehlt hat nur
  das Profi-Format **Anlage/Kreis/Adresse** (LABELING1) am Symbol.
- Neu `dxf_renderer.py::_stromkreisnummern` (render-seitig deterministisch aus
  `circuit_hint`, robust für alte + neue Hint-Form) + zweizeiliges NODEID-Label
  `RZ-001` / `1/1/1` (User-Entscheidung: NODEID bleibt) +
  `stromkreisnummern_drawn`-Summary.
- Mollgasse-EG-Realdaten-Check: 43/43 Labels zweizeilig, Kreis-Summen 1:1 gleich
  Belegungsliste, Cap-Rollover sichtbar (BL-Kreis exakt 20 → Kreis 3).
- Wenn #96 (v1.2.0 `luminaire_id`) mal gemergt ist: Ableitung kann vom Render in
  den Platzierungs-Pass wandern (Follow-up, kein Blocker).

Danach: 3-Owner-Stacks warten weiter auf Enis+Selman (#87/#88/#92 · #93/#95 ·
#96/#98); unblockierter Leonis-Backlog sonst leer — Kandidat Tool-Recherche #2
Docling ist Enis' Lane.

## STAND (2026-09-04, Session-Ende) — DWG-Input-Slice (ODA)

**PR #101 offen** (`leonis/dwg-input-odafc`, gepusht mit User-GO, kein Contract,
**568 grün lokal**, ruff clean; CI beim Session-Ende: contracts ✅, test lief noch —
**morgen zuerst `gh pr checks 101` prüfen, dann Merge nur mit User-GO**).
Danach nächste Kandidaten: Tool-Recherche #2 Docling (Enis-Empfehlung) / warten
auf Approvals der 3-Owner-Stacks — unblockierter Leonis-Backlog ist sonst leer;
neue Idee aus dem Digest: Stromkreis-Zuweisungs-Pass (Anlage/Kreis/Adresse,
Cap ≈20, siehe `STROMKREISNUMMER_DWG.md`-Empfehlung #1).

Tool-Recherche-Kandidat #1 umgesetzt:
- **`hauptengine/dwg_input.py`** — ODA-File-Converter-Wrapper: Discovery der
  versionierten Installations-Ordner (`C:\Program Files\ODA\*\ODAFileConverter.exe`;
  odafc-Default kennt nur den unversionierten Pfad → `is_installed()` war False),
  `stelle_dxf_bereit` (DXF passthrough = bit-identisch, DWG konvertiert R2018),
  `OdaKonverterFehlt` mit Download-Hinweis. Lokal installiert: ODA 27.1.0.
- **Pipeline + API:** `run()` nimmt `.dwg` (Konvertat im TemporaryDirectory);
  `/plan` + `/projekt` nehmen DWG-Uploads, fehlender Konverter → **503**.
- **Tests:** erstes **skip-if-Tool**-Pattern (`tests/hauptengine/test_dwg_input.py`,
  8 neue inkl. Mini-DWG-Pipeline-Roundtrip gegen 4OG-Golden + API-503).
- **Muthgasse 109B = 5. CAD-Familie:** `Projekte/Pläne 19., Muthgasse 109B - …/`
  (9 Etagen E2–E9+DD, DWG→DXF ersetzt wie vom Owner gewünscht, PDFs als Soll;
  Original-ZIP lokal untracked). Sondiert: **Crash-Klasse — kein Wand-Layer-Muster
  greift, `bounds_mm` bricht ab**; im E2E-Netz als raises-Assert gepinnt
  (Kipp-Anleitung für Selman). `.gitignore`-Ausnahmen für den Ordner + knowledge-DXF.
- **Wissens-Gap zu:** `STROMKREISNUMMER_DWG.md` — Nummern-Schema
  **Anlage/Stromkreis/Adresse** (`LABELING1`), 2× Gruppenbatterie SU 6P NET E30 à
  6 Kreise, **Cap ≈20 Leuchten/Kreis**, `IsBLString`=DL/BL (bestätigt #96),
  Typ-Letter A–P, DIN-`#v1`-Obfuskierung = XOR 0xFF auf Base64. Engine-Follow-up
  darin: Stromkreis-Zuweisungs-Pass im Format Anlage/Kreis/Adresse (NODEID-Naht).
- Housekeeping: `WETTBEWERB_ENDRA_AI.md` + Referenzfoto Hotel-Fluchtwegplan committet.

## STAND (2026-09-03, F2-Abschluss)

**F2-Session komplett gemergt (main `c915a55`, 551 grün, ruff clean, kein Contract):**
- **#84** — Abstands-Nachpass + Mollgasse-Real-Data-E2E (Handoff-Auftrag, Union-Merge mit #85).
- **#90** — Prüfregel **10b**: LB-Bereichsregel ohne matchenden Raum = Warnung (vorher dreifach
  stiller No-op). Real bewiesen: Fischa-LB auf Mollgasse → `GARAGE`-Warnung.
- **#91** — disconnected-graph-Anker: Kreuzung ohne erreichbaren Ausgang zeigt Luftlinie zum
  nächsten Ausgang statt fabriziertem „unten" (relevant für B2-Klasse).
- **#94** — Prüfregel **8b**: ≥15 Räume + Symbole, aber 0 Ausgänge/0 Segmente erkannt →
  „UNGEPRÜFT ≠ erfüllt"-Warnung (Fischamender lief vorher als „ok" durch!). + E2E-Netz
  Fischamender EG + Herrenholz EG (`tests/e2e/test_familien_durchstich.py`).
- **#97** — Prüfregel **8c**: ≥30 Türen bei <15 Räumen = Erkennung widersprüchlich →
  Warnung (Barawitzka: 116 Türen/2 Räume/0 Symbole war „ok"). + Barawitzka im E2E-Netz.

**E2E-Regressionsnetz deckt jetzt alle 4 Familien** (Mollgasse · Fischamender · Herrenholz ·
Barawitzka) mit ehrlichen Ist-Stand-Bändern + Kipp-Anleitungen für Selmans Fixes.
Sondierungs-Fakten: Fischa EG 69 Räume(69 typed)/120 Türen/0 Ausgänge/0 Segmente/8RZ+14SL ·
Herrenholz EG 473/140/0/0/0 Symbole · Barawitzka EG 2/116/0/0/0.

**Unblockierter F2-Backlog = LEER.** Es warten nur noch die drei F1-3-Owner-Stacks
(#87→#88→#92 OIB · #93→#95 Sonderstellen · #96→#98 Symbol-Datenmodell) auf
**Approvals von Enis + Selman** — Owner-Entscheidung „nicht ohne Approvals mergen"
ist protokolliert (2026-09-03). N2 Weglänge-Deckung bleibt vertagt (2× protokolliert).

**Tool-Recherche (2026-09-03), Integrations-Kandidaten priorisiert:**
1. **ODA File Converter** via `ezdxf.addons.odafc` → DWG-Input (kleinster Slice, Hauptengine;
   Backlog-Punkt `Stromkreisnummer.dwg` löst sich mit). Konverter = externes Gratis-Programm.
2. **Docling** (IBM, open source) → echtes PDF-LB-Parsing als Vorstufe vor Enis' Regel-Parser
   (Tabellen/Struktur statt Rohtext). Empfehlung an @EnisAMG.
3. **ifcopenshell** → BIM-Pfad, Spike liegt in `spikes/ifc_raum_spike.py` (IfcSpace/IfcDoor →
   RaumModell-Contract). Fertigste Vorlage, Owner @polatselman.
4. **Radiance/honeybee** → nur als Golden-Referenz im Test zur Validierung von `lux_raster`
   (nicht Laufzeit). **luxpy = GPLv3** (nur Dev-Tool). **CubiCasa5k-ML = non-commercial-Lizenz
   + Raster→Vektor-Problem** (nur als Selman-Fallback-Spike denkbar).

## STAND (2026-09-02) — F1: Quellen-Korrekturen + OIB-Gate

**F1-Session: Quellen-Korrekturen + OIB-Gate.** main war `b96ea50` (#84 gemergt, 535 grün,
Mollgasse-Real-Data-E2E an Bord). Der im Nacht-STAND geforderte **Regress-Check nach #83 ist
erledigt** (COORDINATION-Eintrag: Mollgasse EG unverändert 15 RZ + 21 SL, ok) — Track B ist
aktiv, aber mit Ud=40 (s.u.) bit-identisch zum alten Default.

**Drei PRs dieser Session:**
- **PR #87** (`leonis/oib-gate-contract`, **3-Owner, WARTET auf Enis + Selman**):
  `NormRegelwerk` v1.2.0 — `FlaechenSchwellen.quelle` (additiv), Quellen-Doku-Korrektur
  (60/8 m² = OVE E 8101/E 8002-1, scope-gebunden, NICHT EN 1838), `ProviderBundle.oib`,
  `Platzierer.place(…, *, oib: OibBefund | None = None)`.
- **PR #88** (`leonis/oib-gate-konsum`, stacked auf #87): neues `platzierung/oib_gate.py`
  (v1 projekt-global, **fail-closed**: nur `eingeschraenkt`/`uneingeschraenkt` öffnet),
  Flächen-Trigger nur bei offenem Gate, `pipeline.run(…, projekt_kontext=…)` +
  `OibRl2Provider` in der Registry + `render_summary["oib"]`-Audit. Ohne ProjektKontext
  bit-identisch (Mollgasse-E2E unverändert grün). 550 passed.
- **Dieser PR** (`leonis/quellen-korrekturen`, Leonis-Lane): Ud-Doku-Fix in `lux.py`,
  Handoff-Korrekturen, COORDINATION-Antwort an Enis + **Sonderstellen-GO**.

**WICHTIGE fachliche Korrektur (Enis, von mir übernommen): Antipanik-Ud ist 40, nicht 10**
(§4.2.2/§4.3.2 wortgleich „1:40"; die „10" war Uo≥0,1 aus §4.4.2 = anderes Maß). Ältere
STAND-Blöcke unten, die „Antipanik 1:10" versprechen, sind in diesem Punkt überholt.

**Owner-Entscheidung protokolliert: Sonderstellen-Contract Option A hat das Leonis-GO**
(2 von 3 Stimmen mit Enis; wartet auf @polatselman). **Follow-up @EnisAMG:**
`flaechen_schwellen` (Werte + `quelle`) füllen + `provider._snapshot` so erweitern, dass
die Schwellen-Quelle in `quellen` landet — dann aktiviert sich der Flächen-Trigger, sobald
ein ProjektKontext mit bestätigter OIB-Erforderlichkeit mitgegeben wird.

## STAND (2026-09-01, Nacht)

**Alles Leonis-seitige ist auf `main` (`6bf7c6a`), keine offenen Leonis-PRs.** Seit dem
Abend-Stand dazugekommen und gemergt:
- **#82** — Integrations-Artefakte für Host-/Demo-Apps: `examples/demo_run.py` (ein Aufruf
  `build_default_bundle()` + `pipeline.run()` → RaumModell + Platzierung → DXF/PDF; verifiziert
  Mollgasse EG 192 Räume / 15 RZ + 21 SL / ok) + `docs/INTEGRATION.md` (Install, Einstiegspunkt,
  Output-Shape, PDF, Wissens-Inventar, HTTP-Alternative). Kein Produktivcode.
- **#81** — dieser Handoff (vorheriger STAND).

**Selman-Übergabe:** ZIP `Notbeleuchtung_Hauptengine.zip` (komplette Engine + `normwissen/data`
+ `knowledge/extracted` + `CAD_Symbole/E-Symbole.dxf` + Beispielplan + `PROMPT_SELMAN.md`) liegt
auf User-Desktop/Documents. **Wichtiger Bau-Lernpunkt:** der Render-Schritt braucht
`CAD_Symbole/E-Symbole.dxf` (Schrack-Library) im Baum — sonst `_resolve_library_path`-Fehler.
Verifiziert durch Frisch-Entpacken + Lauf. Für Updates zieht Selman einfach `main`.

**In-flight (Enis): PR #83 offen** — „Track-B-Norm-Werte gefüllt (Ud + Umschaltzeit) + vier
Quellen-Korrekturen". Füllt `normwissen/data` (en1838_grundwerte etc.) + provider.py = **die
Aktivierung meiner Track-B-Konsumption** (kein Contract/Schema berührt). **Leonis-Action nach
#83-Merge:** Regress-Check erneut fahren (`scratchpad/verify_mollgasse.py`) — der Mollgasse-Plan
ist dann NICHT mehr garantiert bit-identisch (Antipanik-Ud 1:40→1:10, evtl. Flächen-Trigger),
das ist gewollt; prüfen, dass er weiterhin plausibel/ok ist. Enis' PR selbst = sein Merge.

**Raumerkennung-Generalität (unverändert der zentrale Blocker, Selmans Package):** die Engine
läuft auf fast jedem DXF durch, ERKENNT aber primär Mollgasse-nahe CAD-Konventionen (Layer per
Regex hardcoded: `09-WEG`/`A_Fluchtweg`, `810 Raum`/`A_Raeume`, `0N-TXT`, Wandmuster). Fremde
Familien → degradiert (typlos → RZ-only/leer) oder Crash (0 Wand-Layer). Reifegrad: Mollgasse EG
~gut, OG/DG fast leer, Fischamender Räume gut aber Fluchtweg-Bug B2 (0 Ausgänge), Herrenholz/
Baufeld 100% getypt. = Selman-Arbeit, nicht F1.

## STAND (2026-09-01, spät) — Abstands-Nachpass (PR #84)

**PR #84 (`leonis/abstand-nachpass`, off `main` nach #81/#82 rebased, kein Contract).**
**519 grün**, ruff clean, Schema kein Drift.

Neuer letzter Geometrie-Pass `platzierung/abstand_nachpass.py` (`entzerre`, in `place` nach
`lb_override`, vor `deckungs_zuordnung`): löst Symbol-Kollisionen an der **Strategie-Naht**
auf — gleich-artige Dubletten mergen, verschieden-artige nudgen (Prio `rz>sl>antipanik`, im
Raumpolygon, **nie eine Leuchte löschen**). Jede Strategie deduplizierte bisher nur intern.

**Ehrlich einordnen (nicht überverkaufen):** DOD-Befund #5 (1 Paar < 250 mm) **reproduziert
auf aktuellem `main` nicht mehr** (mit LB verifiziert: 36 Symbole, 0 Kollisionen mit UND
ohne den Pass). Der Nachpass ist daher **Defense-in-depth** (Kollisionsfreiheit invariant
statt zufällig), auf Mollgasse EG aktuell ein **No-op**. Der eigentliche Wert liegt im
**neuen Real-Data-Regressionstest** `tests/e2e/test_mollgasse_eg_durchstich.py` (skip-if-
Asset) — schließt die Fixture-Lücke, an der bisher jeder Real-Plan-Bug durchrutschte (nur
das dünne 4OG-Fake wurde getestet). +11 Tests. **Housekeeping:** PR #78 (überholt von #79)
geschlossen.

**Nächste unblockierte Platzierungs-Kandidaten** (aus 2 Explore-Sweeps, kein Contract, keine
Fremd-Owner-Daten): LB-Vokabular-Mismatch-Warnung (deckt tote `lb_override`-Regeln auf),
disconnected-graph-Anker (`graph.py`/`anker_strategy`), Validierungs-Randfälle. Weglänge-
statt-Luftlinie-Deckung bleibt vertagt (braucht Selmans reicheren Graph im Contract).

## STAND (2026-09-01, Abend)

**Track B (Konsumption) ist auf `main`** (`f92010f`, PR #80 gemergt; PR #72 = `NormRegelwerk`
v1.1.0 davor gemergt `8d6fe23`). **513 grün**, ruff clean, Schema kein Drift = **kein Contract**.
Leonis liest jetzt die neuen abfragbaren Norm-Felder — **defensiv**: solange Enis' Werte `None`
sind, ist der Plan bit-identisch (Mollgasse EG unverändert **15 RZ + 21 SL, Prüfstatus ok**):
- **A** `lux.py` — `lux_raster` bekommt `ud_min`; `deckung.py` + `flaechen_strategy.py` leiten ihn
  über `ud_min_aus_norm(anf.gleichmaessigkeit_max)` ab (Hardcode `1/40` weg). ~~Aktiv → Antipanik
  1:10~~ **KORRIGIERT 2026-09-02: Antipanik-Ud ist ebenfalls 40 (§4.3.2), nicht 10.**
- **B** `flaechen_strategy.py` — liest `regelwerk_snapshot().flaechen_schwellen`: Fläche ≥
  `antipanik_min_m2` / WC ≥ `wc_sanitaer_min_m2` → antipanik-pflichtig (EN 1838 §4.3). Reiner
  **Zusatz**-Trigger; Antipanik-Parameter aus Enis' eigener Antipanik-Regel (`_antipanik_referenz`).
- **D** `hauptengine/validierung.py` — `pruefe(…, norm=…)` (keyword-only): Regel **Umschaltzeit ≤
  Norm-Höchstwert** (LB `umschaltzeit_max_s` vs. strengster Norm-Wert). Pipeline reicht `bundle.norm`.

### → Damit Enis & Selman weiterbauen können (NÄCHSTE Schritte)
- **@EnisAMG — Track B aktivieren:** die Konsum-Logik steht, sie ist nur inert weil die Werte fehlen.
  In `normwissen/data` füllen → aktiviert sich automatisch. **KORRIGIERT 2026-09-02 (Enis' Befund
  übernommen):** `gleichmaessigkeit_max` = **40 für Rettungsweg UND Antipanik** (§4.2.2/§4.3.2; die
  „10" war Uo aus §4.4.2 — von Enis in #83 bereits so gefüllt); `flaechen_schwellen` (≈60/8 m²)
  stammen aus **OVE E 8101/E 8002-1** (scope-gebunden, nicht EN 1838) → werden erst mit dem
  OIB-Gate (#87/#88) gefahrlos füllbar; `umschaltzeit_max_s` = 60-s-Vollwert (in #83 gefüllt).
- **@polatselman — Track C (braucht Contract):** (1) neuer Raumtyp „Arbeitsplatz mit besonderer
  Gefährdung" (EN 1838 §4.4) → schaltet die schon im Contract liegende `arbeitsplatz_lux` (15/5 lx)
  frei; heute bewusst NICHT verdrahtet (wäre toter Code ohne den Raumtyp). (2) Pflicht-POIs
  (Aufzug/Erste-Hilfe/Löschgerät/BMZ) → `anker_strategy` setzt Pflicht-RZ. Beides = 3-Owner.

**Doku/Naht:** COORDINATION.md trägt den vollen Befund (Log-Eintrag 2026-09-01, Hinweis an Enis +
Track-C-Blocker). Verifikations-Skript für den Regress-Check: `scratchpad/verify_mollgasse.py`
(build_default_bundle → Mollgasse EG → RZ/SL-Zähler + Prüfstatus).

## STAND (2026-09-01, früher) — Historie: Track A

**Norm-Integration Platzierung, Track A** (PR #71 **gemergt**). Der Platzierungscode achtet beim
Setzen auf die schon in `normwissen/data` kodierten Werte statt zu hardcoden:
- **A1** `deckung.py` — Fluchtweg-`ziel_lux` aus `anf.min_lux` (norm-belegt) statt Konstante 1,0.
- **A2** `flaechen_strategy.py` — **Antipanik verdichtet bis 0,5-lx-Nachweis** (`_antipanik_punkte`),
  der 0,5-lx-Norm-Wert war vorher tot. Kleine Räume unverändert, große Halle verdichtet (Cap).
- **A3** `hauptengine/validierung.py` — **2-Leuchten-Redundanz je Fluchtweg-Abschnitt** (EN 50172),
  Warnung (kein Hard-Fail). Mollgasse EG erfüllt sie (alle 103 Abschnitte ≥ 2).
- **A4** `lux.py` — Fallback-Höhe 2,5→2,0 m (EN-Mindesthöhe), produktive Aufrufer geben Norm-Höhe.

## STAND (2026-08-31 Session-Ende)

**Alles auf `main` (166c234), 434 Tests grün, ruff clean, Drift-Gate sauber, kein
Contract berührt.** Mollgasse EG ist ein **voll-konformer Plan** (Prüfbericht **ok**:
15 RZ + 21 SL, 4/4 Notausgänge, 0 Kollisionen, 103 Segmente gedeckt, LB-Inklusion).
OG/DG bleiben fast leer — **Wurzel = F2-Raumerkennung** liefert dort ~0 Typen/Fluchtwege
(Gap-Healing-Blocker, Owner-Entscheidung), **kein F1-Fehler**.

**Heute F1 gemergt (PRs #46–#64):** Höhenkoten (h=2,40) · DoD-Visual-Golden-Harness
(`pytest -m visual`) + CI-Raster-Smoke · **covers_segment-Fix** (geometrische Deckung,
real 0→103) · **Plausibilitäts-Regel + Symboldichte-Gate** (quasi-leer = fehler) ·
**Farb-7-Fix** (Legende/Plankopf im Hell-PDF sichtbar) · **RZ an jedem Notausgang**
(§4.1.2 g, auch graphlos) + sichtlinie-Symmetrie + **Anker-Dedup** (keine
Doppelplatzierung) · **Schriftfeld-Leiste** (Info-Blöcke in gerahmter rechter Spalte) ·
2× ultracode-**Gesamtaudit** (adversarial, 7+7 bestätigte Fixes) · **Auto-Prüfeinrichtungs-
Hinweis** (EN 62034 > 20 Leuchten) · Norm-Sofort-Wins („nahe" < 2 m; z=100/200 single-source).

**NEU: Wissensbasis für die Hauptengine** — `knowledge/extracted/
PROFI_DIN_PLAN_UND_VORSCHRIFTEN.md` (aus echtem Profi-DIN-Plan Barawitzkagasse +
AT/DE-Vorschriften extrahiert). Enthält **15 priorisierte Engine-Empfehlungen** mit
Owner + Aufwand — die Roadmap für den nächsten Hauptengine-Ausbau.

### → Hauptengine-Roadmap für das Team (aus dem Digest, gemeinsames Package)

Die Hauptengine (`src/notbeleuchtung/hauptengine/`) ist gemeinsam (alle 3 Owner). Nächste
Ausbaustufen, damit Enis/Selman + Leonis integriert weiterbauen:

- **Contract-Erweiterung (3-Owner-Konsens nötig, `hauptengine/contracts/`):**
  Symbol-Datenmodell reicher — `Platzierung` um `TYPENAME`/`TYPENUMBER`(Legenden-Letter)/
  `luminaire_ID`/`MountingMethod`/`Technology`/**`Schaltungsart`(DL/BL)** erweitern (Digest
  #6). Speist Stückliste-als-Typ-Letter-Legende (#7) + QR/NODEID (#9). `richtung=beidseitig`
  existiert bereits als `richtung="gerade"` → **kein Contract nötig**, nur Render-Symbol.
- **Enis (normwissen):** EN-1838-Lux-Grenzwerte als `NormRegelwerk`-Werte kodieren (Digest #3:
  1/0,5/15/5 lx + Gleichmäßigkeiten) · Anwendungsfall-Klassifikation GK/Nutzung/Fläche →
  OIB-Stufe + Betriebsdauer (1/3/8/24 h) + Stromquelle aus LB (#11) · z pro Symbol liefern (#4).
- **Selman (raumerkennung):** hervorzuhebende Stellen (BMZ/Erste-Hilfe/Löschgeräte) +
  Pflicht-Platzierungspunkte (Treppen/Niveau-/Richtungsänderung/Aufzugsflur) im RaumModell
  erkennen (#10) · flächenbasierte Trigger (Antipanik ≥ 60 m², WC > 8 m²) (#12) · **Mollgasse
  Gap-Healing** (echte Raum-Polygone) = der Gebäude-Blocker.
- **Render/Hauptengine (F1-nah):** DIN_SIBEL-Layer-Schema statt Ad-hoc-Layer (#2) ·
  Beidseitig-Pfeil-Symbol für `richtung="gerade"` · getrennter Sicherheitskreis modellieren
  (Geschoß/Brandabschnitt, NODEID, Stromkreis-Belegungsliste kompatibel zu `1.xlsx`) (#14).

**Offene F1-Follow-ups (F2-abhängig):** Deckungs-LOS echt (Weglänge im Zirkulationsgraph
statt Luftlinie — braucht Selmans Graph/Wände) · KELLER in LB-Naht adressierbar (Vokabular-
Symmetrie). Gaps in der Wissens-Extraktion: `Stromkreisnummer.dwg` (ODA-Konverter nötig).

---

## STAND (2026-08-29 Session-Ende) — Historie

**Platzier-Regeln aus dem Wissen kodiert** (Commit `e87a745`, `anker_strategy.py`):
1. **RZ-Dichte = `l = z·h`** — `plan_rettungszeichen_sichtlinie` zieht `max_abstand_mm`
   aus `norm.erkennungsweite_m` (z=200 hinterleuchtet/100 beleuchtet, h=Pikto-Höhe)
   statt geratener 12-m-Konstante. Keine Überproduktion.
2. **`richtung_durch_tuer(tuer_xy, ziel_xy)`** — RZ an Tür/Öffnung entlang der Schwelle,
   Pfeil DURCH die Öffnung in Reiserichtung; überschreibt das Distanz-Gefälle
   (Owner-Korrektur L-Knick). Tests +2, Suite 95 grün. Kein Contract berührt.

⚠️ **Git-Tangle:** dieser Commit + die früheren Platzier-Module (graph/richtungsfeld/
sichtlinie/mittellinie/lux/deckung) liegen auf Branch **`selman/raumerkennung-dxf`**
(nicht `leonis/*`). Integration war als PR #12 geplant. PR #11 stale/superseded.
Vor Weiterarbeit: entwirren — Platzier-Code gehört auf einen `leonis/*`-Branch.

**Echter End-to-End-Durchstich auf Fischamender BT1 1.OG** (F2-Provider → F1-Engine →
DXF in den echten Grundriss). Ergebnis ehrlich geprüft (Determinismus + Sanity):
- ✅ Provider läuft: **59 Raum-Polygone** (39 getypt, 20 Fragmente), **102 Tür-INSERTs**.
- ✅ Engine platziert 10 SL; RZ-Regeln laufen auf echter Geometrie.
- ✅ **DXF-Overlay** (`output/Fischamender_BT1_1OG_MIT_Notbeleuchtung.dxf`, untracked):
  Symbole IN den Original-Grundriss gezeichnet, Original-Einheiten (Meter → Pos+scale
  ÷ factor=1000, scale 0,185), neuer Layer `E_Sicherheitsbeleuchtung`, Original
  unangetastet. Per ezdxf-Preview verifiziert.
- ❌ **2 F2-Bugs gefunden** (in `docs/COORDINATION.md` als Tickets dokumentiert):
  (B1) Tür-**Doppelzählung** — 102 roh → ~60 dedup (jede Tür als 2 ARC-Schwenkbögen);
  (B2) **A_Fluchtweg + Ausgänge werden für die Fischamender-Familie nicht gelesen**
  (`zirkulation_aus_dxf` sucht Mollgasse `09-WEG`, footprint nur Mollgasse-kalibriert)
  → 0 Ausgänge, 0 Zirkulation → RZ-Routing musste stiegenhaus-verankert improvisiert
  werden (Stiegenhaus aus `S-STRS`-Layer lokalisiert, ×factor).

**Erkenntnis:** Platzier-Regeln (l=z·h, Wasserscheide, Pfeil-durch-Tür) sind solide;
der Engpass für vollautomatisch = **F2s Provider auf fremden CAD-Familien** (nicht die
Platzierung). Placement kann erst voll geroutet werden, wenn F2 Fluchtweg/Ausgänge
für die Fischamender-Konvention liefert.

**Nächste Leonis-Tasks:** (1) Git entwirren (Platzier-Code auf `leonis/*`, PR #12/#11
klären). (2) GANG-Raum→Graph-**Fallback** in `platzierung/` erwägen (RZ auch ohne
F2-Fluchtweg-Layer, aus erkannten GANG-Räumen — macht Engine auf mehr Plänen sofort
nutzbar). (3) SL-Symbolgröße justierbar + lux-Verifikation je realem Plan.
Demo-Skripte in `scratchpad`/`output/` (nicht im Repo).

## STAND (2026-08-28 Session-Ende) — Historie

**Slice 2 (PR #4) + Slice 3 (PR #5) = GEMERGT nach `main`.** `pytest -q` auf main →
**40 passed, 0 skipped**, `ruff check .` sauber, E2E `rendered: True`.
Branches `leonis/slice2-platzierung` + `leonis/slice3-render` noch da (nicht gelöscht).

**Wissensbasis auf main** (`knowledge/`): 20 Norm-/Praxis-PDFs + `extracted/` (18
Digests, Regel-Tabellen), `extracted/bildlehren/` (visuelle Analyse), Synthese
`extracted/PLATZIERUNGS_KONZEPTE.md`, `extracted/aus_elektroplaner/` (5 gefilterte
elektro-planer-Digests inkl. Schrack-Katalog + OVE E 8101:2025-Deltas) + kompletter
Rohimport `_extracted_text/`. Repo ist PRIVATE — lizenzpflichtige Norm-PDFs, NICHT
public stellen.

Slice 3 gebaut: `symbols/{library.py, inserter.py}`, `hauptengine/render/dxf_renderer.py`
(Contract B + RaumModell → DXF: 5 RZ auf `E_Sicherheitsbeleuchtung`, F13-Labels,
Raum-Konturen, VPORT), `pipeline.run(..., out_path=)`. KEIN Contract angefasst.
PORT_LOG Slice-3-Tabelle.

**Projekte auf main:** neues Projekt **Baufeld E2** als `Projekte/Baufeld_E2.zip`
(56 MB, 8 DXF-Etagenpläne). Roh war 756 MB, 4 DXF > 100 MB GitHub-Limit → DXF
komprimiert auf ~6%, daher Zip. Rohordner `Projekte/Baufeld E2/` ist gitignored
(bleibt lokal). Enis/Selman: einmal entpacken. E8101-2025-PDF liegt auch auf main.

**Entscheidungen dieser Session (nicht neu aufrollen):**
- **Kein Git-LFS.** Geprüft: 923 MB Binär ≈ ganzes Free-LFS-Limit (1 GB Speicher +
  1 GB/Mon Bandbreite); Migration = Historie-Umschreiben + Force-Push (alle neu
  klonen). Aufwand/Kosten > Nutzen → bleibt bei normalem Git. Falls Repo später
  stört: `_extracted_text` (53 MB) ist lokal verzichtbar (Wert in Digests), Roh-CAD
  projektweise zippen wie Baufeld E2.
- **NetworkX = gratis** (BSD-3). Andock-Analyse gemacht: `zirkulation.{nodes,edges}`
  ist aktuell UNGENUTZT (Platzierer nutzt nur `segmente`), Fixture-Graph zu dünn
  (2 stair-nodes). NetworkX lohnt erst mit Selmans echtem Graph (Slice 4) + Leonis'
  Schicht 1 (Kreuzungs-Anker via `degree>=3`) / Schicht 5 (Deckung/Distanz via
  `single_source_dijkstra`). Dann: neues Modul `platzierung/graph.py` + Dep in
  pyproject. **Jetzt noch nicht einbauen.**

**Nächste Leonis-Tasks:** (1) DoD-Sichtprüfung generierter DXF vs. 4OG-GU-PDF (offen),
(2) **Slice 5-Anteil** dünne FastAPI `api/main.py POST /plan` → E2E, oder Port-Staging
für Enis/Selman auf Zuruf. `layout_template` (Titelblock/PDF) deferred → PORT_LOG.
Neue Erkenntnisse fürs Normwissen (Enis): OVE E 8101:2025 neues Verbot RCD/AFDD in
Sicherheitskreisen (Hard-Stop), Schrack-Erkennungsweiten je Leuchtenfamilie.
Platzierer-Ausbau-Fahrplan (Anker→Linie→Fläche→Deckung): `extracted/PLATZIERUNGS_KONZEPTE.md`.

Offener Rest aus Slice 2 (kein Blocker, Enis' Slice 1): FakeNorm mappt
`fuer_fluchtweg_abschnitt` auf die GANG-Regel → alle 5 RZ nutzen `notlicht_ks_stiege`;
die `_unten`-Variantenwahl greift erst mit Enis' echtem STIEGENHAUS-NormProvider.

## Wer du bist
Du besitzt die **Platzierungs-Logik**: wie/wann/wo Notbeleuchtungs-Symbole gesetzt
werden. Contract: `PlatzierungsErgebnis`, Protocol: `Platzierer.place(raum, norm)`.
Du konsumierst Selmans `RaumModell` + Enis' `NormProvider`/`LBVorgabe` → produzierst
die Platzierungen. Dazu: Mit-Owner der `hauptengine/` (Contracts + Render + API).

## Dein Auftrag — Slice 2
1. Port `elektro-planer/backend/engine/placement_geometry.py` → `platzierung/geometry.py`.
2. Port `elektro-planer/backend/diagnostics/inject_communal_stgh.py` →
   `platzierung/communal_stgh_strategy.py`. **Import-Grenze hart:** nur `contracts`
   + `geometry` + `symbols`, KEIN Render — die Strategy produziert Contract B, sie
   zeichnet nicht selbst.
3. `NotlichtPlatzierer.place(raum, norm)` erfüllt `Platzierer`; reproduziert die 5
   echten 4OG-RZ (`tests/fixtures/platzierung_4og.json`).
4. Fake ersetzen (`FakePlatzierer`); Naht-Invarianten grün
   (`covers_segment ∈ RaumModell`, `norm_quelle ∈ NormRegelwerk`).

## Deine Sonderrolle — Port-Bridge + Integration
- **Staging für andere:** Enis/Selman haben keinen elektro-planer-Zugriff. Bereits
  gestaged: `normwissen/_port_source/` (Norm-YAMLs), `raumerkennung/_port/` (Parser).
  Weitere Port-Wünsche (LB-Parser für Enis, Symbol-Infra/Render für Slice 3) → du
  kopierst aus elektro-planer + committest.
- **Slice 3 (Render, Hauptengine):** `dxf_writer`/`dxf_layers`/`layout_template` +
  Schrack-Infra + `CAD_Symbole/E-Symbole.dxf` → echter Notbeleuchtungs-DXF aus
  Contract B.
- **Slice 5:** dünne FastAPI `api/main.py POST /plan` → E2E.

## Regeln
Contracts-Änderung = 3-Owner-Approval. Branch `leonis/…` → PR. Board pflegen:
`docs/PROGRAMM_NOTBELEUCHTUNG.md`.
