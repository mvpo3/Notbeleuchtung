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
- [x] `normwissen/photometrie/ies.py` — IES/LM-63-Parser (`lade_ies`), gleicher `Photometrie`-Typ →
  F1-Naht unverändert; horizontale Symmetrie-Expansion (rot./quadrant/bilateral), abs. Fotometrie
- [ ] Test gegen eine echte Schrack-LDT/-IES (Owner besorgt Datei) — bis dahin synthetische Fixtures
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
| `normwissen/lb/` | `LBProvider.parse_lb(lb_path) -> LBVorgabe` | `data/lb_extraktion.yaml` + Digest `knowledge/extracted/LB_ANALYSE_beispiele.md` | **STEHT** (fail closed, s.u.) |

### ✅ Stand 2026-08-31 — LB-Naht geschlossen (Branch `enis/lb-parser`)

**Update 31.08. abends: PR #60 ist gemerged, die LB-Arbeit ist vollständig auf
`main`.** Der Abschnitt bleibt als Beleg für die Feld-für-Feld-Gegenüberstellung
stehen. Ursprünglicher Text:

Der Branch ist auf `origin/main` (`9d3c080`) rebased und wieder lauffähig. Die
öffentliche API von PR #40 bleibt unverändert (`LbTextProvider`, Modul-`parse_lb`,
`registry.build_default_bundle()` unangetastet); dahinter steht die fail-closed
Extraktion mit seitengenauem Audit-Trail (`parse_bericht`).

**Was sich dadurch gegenüber main ändert** (alles an den 4 realen LB-PDFs geprüft):

| Fall | main `9d3c080` | dieser Branch |
|---|---|---|
| Fischa `system_typ` | `zentralbatterie` — wählt still eine Seite des Widerspruchs (Gruppenbatterie S. 19 vs. Zentralbatterie S. 42) | kein Wert + `review_informativ` mit beiden Fundstellen |
| GU-Rahmen (kein Notbeleuchtungs-Abschnitt, reiner Verweis) | erfindet `bereiche_inklusion = [STIEGENHAUS, GARAGE, MUELLRAUM]` | blockierender Review |
| mo-Bau (keine Elektro-Vorgaben) | leere `LBVorgabe` — von „die LB macht keine Vorgaben" nicht unterscheidbar | blockierender Review |
| mo-Elektro `umschaltzeit_max_s` | `None` (Wert geht verloren) | `0.5` |
| mo-Elektro Bereiche | ohne `LAGER` | mit `LAGER` |
| `batterie_standort` | `None` an beiden Elektro-LBs (Muster verlangt `batterie im <Raum>`) | Fischa „Technikraum", mo-Elektro „Zählerraum" |
| Audit-Trail | Dateiname | Datei + § + Seite des **Treffers**, plus voller Befund inkl. Kandidaten |

Die Härtungen aus #45/#56 sind übernommen bzw. nachgebaut (Betriebsdauer-Kontext,
Lux-Wortform, Antipanik-Fenster, Overflow-Guard, `batterie_standort`), alle
16 main-Tests liegen wieder in `tests/normwissen/test_lb_parser.py`.

**✔ ERLEDIGT (PR #67):** die Naht-Frage unten ist beantwortet. `pipeline.py` fängt
`LbFehler` ab und flaggt `render_summary["lb_review"]`; `api/main.py` reicht das Feld
jetzt bis zum Client durch (`/plan` **und** `/projekt`), Review-Meldung im Header bei
600 Zeichen gekappt. Ursprünglicher Text:

**Offene Naht-Frage an @mvpo3:** `pipeline.py:100` ruft `bundle.lb.parse_lb()`
ungeschützt. Fail closed heißt: der Aufruf **wirft** (`LbReviewRequired` /
`LbNichtLesbar`) statt eine leere `LBVorgabe` zu liefern — heute schlägt das als
HTTP 500 durch. Vorschlag: `api/main.py` fängt `LbFehler` und antwortet 422 mit
`bericht.als_text()`. Liegt in der gemeinsamen Fläche, deshalb hier statt im PR.

**Vokabular-Naht (@polatselman/@mvpo3):** `unterstuetzte_raum_typen` in
`lb_extraktion.yaml` ist eine Kopie der Labels aus `raumerkennung/raumtyp.py` und
war gedriftet. Neu `tests/contract/test_lb_raumtyp_naht.py` als Drift-Gate in
beide Richtungen — wer dort ein Label ergänzt, sieht sofort, dass die LB-Seite
nachzuziehen ist.


### ⚠ Befund an @mvpo3: falsche Quellenzuordnung im LBVorgabe-Contract-Test

`tests/contract/test_lb_vorgabe_contract.py::test_fischa_gk4_exklusion_stiegenhaus`
baut eine `LBVorgabe` mit `betriebsdauer_min=480`, `umschaltzeit_max_s=0.5`,
`mindest_lux_fluchtweg=1.0`, `SonderLux("feuerloescher", 5.0)` und
`piktogramm_norm="EN ISO 7010"` — und schreibt als Quelle
`lb_quelle="20241209_E LV Fischa 46.pdf §2.10/2.11"`.

**Keiner dieser fünf Werte steht in Fischa.** Am Original nachgeprüft (2026-08-30):
`lux`/`lx` = **0 Treffer im gesamten Dokument**, ebenso „Umschaltzeit",
„Betriebsdauer", „Feuerlöscher" und „7010". Fischa nennt statt EN ISO 7010 die
**ÖNORM Z 1000**. Die fünf Werte stammen aus `mo-leistungsbeschreibung_Elektro`
(§5.1.23, S. 37–38). Derselbe Fehler stand in
`knowledge/extracted/LB_ANALYSE_beispiele.md` und ist dort korrigiert.

Was Fischa §2.10/§2.11 **wirklich** trägt: Exklusion STIEGENHAUS + GANG (GK4),
Inklusion GARAGE, Gruppenbatterie im Technikraum, Einzelleuchtenüberwachung,
automatische + WEB-Prüfung, Fabrikat DIN-Sicherheitstechnik Concept-LED,
Normbezug ÖVE 8101 / R 12-2 / EN 1838 / ÖNORM Z 1000.

Der Test liegt in deiner Lane — Enis hat ihn **nicht** angefasst. Vorschlag:
entweder die Skalare entfernen oder `lb_quelle` auf die mo-Elektro-LB umstellen.
Merksatz: **Fischa = Bereichslogik, mo-Elektro = Skalare.**

### ✔ ERLEDIGT (2026-08-31) — Befund an @mvpo3 vom 30.08.: PR #40 erzeugte am echten Fischa-PDF einen falschen LB-Wert

> **Beidseitig behoben.** Auf main durch `facabe0` (Kontext-Gating
> `betriebsdauer|auszulegen`, `notruf`-Ausschluss, Cap 1440), auf `enis/lb-parser`
> durch das Anker-Gating plus `plausibel_max`. Beide liefern für Fischa jetzt
> `betriebsdauer_min = None`. Der Regressionstest steht als
> `test_stoerungsfrist_erzeugt_keine_betriebsdauer`. Der Rest des Eintrags bleibt
> als Beleg stehen.

**PR #40 („normwissen — ② LB-Parser") wurde in die CODEOWNERS-Lane `@EnisAMG`
gemerged** und über `registry.build_default_bundle()` aktiv verdrahtet. Enis hatte
zu diesem Zeitpunkt eine fail-closed Implementierung derselben Naht fertig
(`enis/lb-parser`) — die Kollision wurde erst beim Rebase sichtbar.

**Belegter False Positive.** Der gemergte Parser, gegen das echte
`20241209_E LV Fischa 46.pdf` laufen gelassen:

```
betriebsdauer_min  = 1440            ← Fischa spezifiziert KEINE Betriebsdauer
system_typ         = zentralbatterie ← waehlt still eine Seite eines Widerspruchs
bereiche_inklusion = [GARAGE]        ← stiller No-op im Platzierer
```

Ursache: `_betriebsdauer_min()` sucht `(\d+)\s*(?:Std|Stunden|h)` im **gesamten**
Dokumenttext und trifft „Störungsbehebung binnen 24 h" (S. 12) → 24 × 60 = 1440.

**Warum das sicherheitsrelevant ist:** `LBVorgabe.betriebsdauer_min` ist eine
*explizite Auftraggeber-Vorgabe* und übersteuert nach der CLAUDE.md-Hierarchie
`LB-explizit → Norm` den EN-1838-Default von 60 min. Hier übersteuert ein Wert,
den das Dokument nie enthalten hat.

**Falsche Quellenzuordnung (am Original geprüft).** Fischa enthält **keine**
480 min, **keine** 0,5 s, **kein** 1 lx, **keine** 5 lx Feuerlöscher und **kein**
EN ISO 7010 — `lux`/`lx`, „Umschaltzeit", „Betriebsdauer", „Feuerlöscher" und
„7010" haben je **0 Treffer**; genannt ist ÖNORM Z 1000. Diese fünf Werte stammen
aus `mo-leistungsbeschreibung_Elektro_240718.pdf` §5.1.23 (S. 37–38).

Fischa liefert tatsächlich: Exklusion STIEGENHAUS + GANG (GK4, §2.10 S. 37),
Inklusion GARAGE (§2.11), Überwachung Einzelleuchte, Prüfung WEB, Fabrikat
DIN-Sicherheitstechnik Concept-LED (§2.21 S. 42), Normbezüge — und
**widersprüchliche Systemtyp-Angaben** (Gruppenbatterie S. 19 vs. Zentralbatterie
S. 42), die nicht still aufgelöst werden dürfen.

**Betroffen:** `tests/fixtures/lb/fischa_lb.txt` (synthetischer Text mit dem Titel
„Projekt Fischa 46", der die mo-Elektro-Skalare trägt) und die darauf gestützten
Tests `test_fischa_skalare_felder`, `test_fischa_sonderlux_und_normbezug`,
`test_fischa_inklusion_garage`. **Enis hat die Fixture NICHT verändert** — sie liegt
in der 3-Owner-CODEOWNERS-Lane. Auch `test_leere_lb_bleibt_norm_default` ist
semantisch heikel: eine leere `LBVorgabe` ist von „die LB macht keine Vorgaben"
nicht unterscheidbar und lässt die Engine still norm-getrieben weiterlaufen.

**Vorschlag (Owner-GO steht aus):** Enis' fail-closed Implementierung ersetzt die
Extraktionslogik, die öffentliche API (`LbTextProvider`, `parse_lb`) und die
Registry-Verdrahtung von #40 bleiben **unverändert** erhalten. Fixture und
Test-Korrektur macht Leonis in seiner Lane.

### ✔ ERLEDIGT (2026-08-31) — Befund an @polatselman: `GARAGE` war kein erzeugbarer `raum_typ`

> **Geschlossen durch PR #49** (GARAGE/TECHNIK/LAGER/MUELLRAUM) **und PR #57**
> (KELLER). Die LB-Stützliste ist nachgezogen, das Label heißt `TECHNIK` (nicht
> `TECHNIKRAUM`), `LAGER` und `MUELLRAUM` sind getrennt. Beide realen Elektro-LBs
> parsen dadurch durch. Der Rest des Eintrags bleibt als Beleg stehen.

`raumerkennung/raumtyp.py` (`_TYP_MAP`) erzeugt 13 Werte — `GARAGE` ist keiner
davon, `classify_room` liefert für einen Stempel „Garage" `UNKNOWN` und der Raum
behält `raum_typ == ""`. Eine `BereichsRegel(raum_typ="GARAGE")` ist damit im
Platzierer ein **stiller No-op**: `lb_override` findet kein Polygon, gibt die
Liste unverändert zurück, kein Fehler, kein Log.

Das trifft den kanonischen LB-Fall direkt — **beide** realen Elektro-LBs fordern
Sicherheitsbeleuchtung in der Garage. Der LB-Parser behandelt das deshalb als
**blockierenden Review** statt es still zu verschlucken. Dasselbe gilt für
`TECHNIKRAUM` und `LAGER` (mo-Elektro §5.1.23).

Zum Schließen wären `GERMAN_ROOM_TYPE_MAP` + `_TYP_MAP` (+ ein `RoomType`-Member)
zu erweitern — deine Lane, deshalb hier nur der Befund.

**Bitte an Leonis (blockiert den LB-Parser fachlich, nicht technisch):**
`BereichsRegel.raum_typ` muss exakt Selmans `RaumModell.raum_typ`-Vokabular
treffen (`STIEGENHAUS`/`GANG`/`GARAGE`, …). Wo ist die Liste kanonisch? Solange
das offen ist, parst Enis die LB-Bereiche auf genau diese drei Strings und
markiert alles andere als „nicht zuordenbar" statt zu raten.

**Naht verdrahtet:** `registry.build_default_bundle()` setzt `ProviderBundle.lb`
seit PR #40 — der Parser ist aktiv. Offen bleibt die OIB-Hälfte (`ProjektKontext`
→ `pipeline.run`, `ProviderBundle.oib`).

**Fail-closed-Verhalten, das die Verdrahtung kennen muss:** `parse_lb()` wirft
`LbNichtLesbar` bzw. `LbReviewRequired` statt eine leere `LBVorgabe`
zurückzugeben — eine leere wäre von „die LB macht keine Vorgaben" nicht
unterscheidbar und ließe die Engine still norm-getrieben weiterlaufen. Seit dem
angeglichenen Raumtyp-Vokabular parsen die beiden Elektro-LBs durch; GU-Rahmen und
Bau-/Ausstattungsbeschreibung brechen weiterhin ab — zu Recht, sie enthalten keine
Notbeleuchtungs-Vorgaben.
`LbTextProvider.parse_bericht()` liefert dazu den vollen Audit-Trail. Wer verdrahtet,
sollte diese Exceptions in eine sichtbare Rückmeldung übersetzen (API: 422 mit
Bericht), nicht verschlucken.

**Norm-Ausgabe-Bezeichnung:** `ÖNORM EN 1838:2013` bleibt vorerst stehen, obwohl
im Repo 2019-11-15 liegt (inhaltlich deckungsgleich). Grund: der String ist
Naht-Invariante und steckt auch in `tests/fakes.py` und
`tests/platzierung/test_flaechen_strategy.py:53`. Umstellung nur gemeinsam
(Fixture-Regen aus dem echten Provider) — Details `docs/NORMQUELLEN_AT.md` 2a.

## Log (append-only, neueste oben)
- 2026-09-05 **Leonis: Stromkreisnummer Anlage/Kreis/Adresse als NODEID-Zweitzeile (Branch `leonis/stromkreisnummer-labels`, kein Contract).** PR #101 (DWG-Input) ist gemergt (User-GO, main `a809764`, 568 grün). Folge-Slice = Digest-Empfehlung #1 aus `STROMKREISNUMMER_DWG.md`: **Der Zuweisungs-Pass existierte schon** (`platzierung/circuit_zuordnung.py`: Cap 20/Kreis, DL/BL getrennt) — gefehlt hat das Profi-Format **`Anlage/Kreis/Adresse`** (LABELING1) am Symbol. Neu `render/dxf_renderer.py::_stromkreisnummern`: render-seitig deterministisch aus `circuit_hint` (Anlage = Gebäude-Letter A=1/B=2, Kreis = distinct Hints je Anlage in Erst-Auftretens-Reihenfolge — deckt alte `AGV-A-F13`- UND neue `AGV-A-F13-DL-1`-Hints ohne Suffix-Parsing, Adresse = fortlaufend im Kreis; ohne Hint kein Label). `_draw_nodeid_labels` rendert zweizeilig `RZ-001\P1/1/1` (User-Entscheidung: NODEID bleibt als Wartungs-ID, wie Profi-Plan luminaire_ID + LABELING1 getrennt), Summary-Feld `stromkreisnummern_drawn`. Belegungsliste unangetastet. Mollgasse-EG verifiziert: 43/43 Labels zweizeilig, Kreis-Summen 1:1 deckungsgleich mit der Belegungsliste, Cap sichtbar (AGV-B-BL-1 = exakt 20 → Rollover in Kreis 2/3). +3 Unit-Tests + Golden-Test erweitert, **571 passed**, ruff clean, Visual-Goldens unverändert grün, kein Contract. 3-Owner-Stacks #87/#88/#92 · #93/#95 · #96/#98 weiter ohne Approvals; wenn #96 (v1.2.0 `luminaire_id`) irgendwann gemergt ist, kann die Ableitung vom Render in den Platzierungs-Pass wandern.
- 2026-09-04 **Leonis: DWG-Input via ODA File Converter (Branch `leonis/dwg-input-odafc`, kein Contract) + Muthgasse 109B als 5. CAD-Familie.** Tool-Recherche-Kandidat #1 umgesetzt: neues `hauptengine/dwg_input.py` (Discovery der versionierten ODA-Installations-Ordner + `stelle_dxf_bereit`: DXF passthrough/bit-identisch, DWG konvertiert, ohne Konverter klarer `OdaKonverterFehlt`); `pipeline.run` nimmt `.dwg` (Konvertat im TemporaryDirectory), API `/plan` + `/projekt` nehmen DWG-Uploads (fehlender Konverter → 503). Erstes **skip-if-Tool**-Testpattern. **@polatselman — neues Real-Material:** `Projekte/Pläne 19., Muthgasse 109B - 2026-05-07_13-12/` (9 Etagen E2–E9+DD, aus DWG konvertiert, + Plan-PDFs als Soll-Referenz). Ist-Stand sondiert: **kein Wand-Layer-Muster greift → `bounds_mm` bricht ab** (Crash-Klasse, im E2E-Netz als raises-Assert mit Kipp-Anleitung gepinnt). **Wissens-Gap zu:** `Stromkreisnummer.dwg` extrahiert (`knowledge/extracted/STROMKREISNUMMER_DWG.md`) — Schema **Anlage/Stromkreis/Adresse**, 2 Gruppenbatterien SU 6P NET E30 à 6 Kreise, Cap ≈20 Leuchten/Kreis, `IsBLString`=DL/BL (bestätigt Symbol-Datenmodell #96), Typ-Letter A–P, DIN-`#v1`-Obfuskierung dekodiert (XOR 0xFF). **568 passed**, ruff clean, kein Contract; die 3-Owner-Stacks #87/#88/#92 · #93/#95 · #96/#98 bleiben unberührt offen.
- 2026-09-02 **F2: Prüfregel 8c (Türen ≫ Räume = Erkennungsbasis widersprüchlich) + Barawitzka EG im E2E-Netz (Branch `leonis/barawitzka-basis`, kein Contract).** PR #94 (8b + Fischamender/Herrenholz-E2E) ist gemergt (main `917375d`). Vierte Familie sondiert: **Barawitzka EG = 116 Türen erkannt, aber nur 2 Räume** (Raum-Layer-Nacharbeit, bekannt) **+ 0 Symbole → Prüfstatus war „ok"**, weil Regel 8/8b auf n_raeume ≥ 15 gaten. Neue **Regel 8c**: ≥ 30 Türen (Gebäude-Beweis) bei < 15 Räumen → Warnung „Prüfbasis Räume (Erkennung widersprüchlich)" — die Tür-Erkennung ist das unabhängige Signal, dass die Raum-Erkennung das Gebäude nicht erschlossen hat. E2E: `test_familien_durchstich.py` + Barawitzka (Tür-Band ≥ 60 hält, Raum-Lücke gepinnt mit Kipp-Anleitung, leeres Ergebnis ≠ ok). Mollgasse/Fischamender/Herrenholz unberührt (Räume ≥ 15 → 8c schweigt). +5 Tests, **551 passed/5 skip**, ruff clean, kein Contract, kein Overlap mit #87/#88/#92/#93.
- 2026-09-02 **F2: Prüfregel 8b (Prüfbasis fehlt ≠ ok) + E2E-Regressionsnetz Fischamender/Herrenholz (Branch `leonis/e2e-familien`, kein Contract).** PR #90 + #91 sind gemergt (User-GO, main `c5ad5ed`). Sondierung auf den Nicht-Mollgasse-Familien deckte auf: **Fischamender BT1 EG/1.OG läuft mit Prüfstatus „ok" durch, obwohl 0 Ausgänge + 0 Segmente erkannt werden** (Bug B2) — die Kern-Regeln 3/4/4b/5 laufen dann schlicht nie, „ungeprüft" wurde als „erfüllt" verkauft. Neue **Regel 8b**: ≥15 Räume + Symbole platziert, aber 0 erkannte Ausgänge bzw. 0 Fluchtweg-Segmente → je eine **Prüfbasis-Warnung** (nur wenn Symbole da sind — sonst erzählt Regel 8 die Geschichte schon). Dazu **`tests/e2e/test_familien_durchstich.py`** (skip-if-Asset, Muster von #84): Fischamender EG (Räume/Türen-Bänder halten, B2 als Warnung ausgewiesen, Status ≠ ok; kippt sichtbar wenn @polatselman B2 fixt) + Herrenholz EG (473 Räume, 0 Symbole → Plausibilität MUSS „fehler" sagen, fail-closed-Schranke). Mollgasse EG unberührt (hat Ausgänge+Segmente → 8b schweigt). +9 Tests, **546 passed/5 skip**, ruff clean, kein Contract; berührt NICHT die #87/#88/#92-Dateien.
- 2026-09-02 **Leonis (@mvpo3) → @EnisAMG: alle vier Quellen-Korrekturen bestätigt + umgesetzt; dein OIB-Gate-Vorschlag ist gebaut (PR #87 + #88). Und: Sonderstellen-Option A hat mein GO.** Im Einzelnen: **(1) Ud 40/40 statt 40/10** — übernommen; die Fehlangabe ist korrigiert in `platzierung/lux.py::ud_min_aus_norm` (Docstring, PR `leonis/quellen-korrekturen`), im `gleichmaessigkeit_max`-Kommentar von `contracts/norm_regelwerk.py` (PR #87) und in `Handoff/LEONIS.md` (alte „Antipanik 1:10"-Versprechen als korrigiert markiert). **(2) Uo≠Ud** — im Docstring/Kommentar explizit festgehalten (kleinste:mittlere vs. kleinste:größte, EN 12665), damit der Kategorienfehler nicht wiederkehrt. **(3) 60/8 m² nicht aus EN 1838** — der `FlaechenSchwellen`-Docstring attribuiert jetzt OVE E 8101:2019 718.560.9.001.AT / ÖVE/ÖNORM E 8002-1 samt Scope-Bindung (PR #87, Schema-Description regeneriert). **(4) Umschaltzeit zweistufig** — Kommentar stellt klar: das Contract-Feld trägt den 60-s-Vollwert, der 5-s-Halbwert liegt in deiner YAML. **Dein Gate-Vorschlag ist umgesetzt:** PR **#87** (Contract, v1.2.0: `FlaechenSchwellen.quelle` additiv, `ProviderBundle.oib`, `Platzierer.place(…, *, oib: OibBefund|None)`) + PR **#88** (stacked: neues `platzierung/oib_gate.py`, v1 projekt-global + **fail-closed** — nur `eingeschraenkt`/`uneingeschraenkt` öffnet, `review_required`/kein Kontext = Gate zu = heutiges Verhalten; `pipeline.run(…, projekt_kontext=…)` ruft `bundle.oib.bewerte_oib`, `registry` verdrahtet deinen `OibRl2Provider`, `render_summary["oib"]` trägt Stufen+Gate+Hinweise). Getriggerte Leuchten übernehmen `flaechen_schwellen.quelle` als `norm_quelle` (Fallback: Antipanik-Regel-Quelle, Naht hält). 550 grün, Mollgasse-E2E ohne Kontext bit-identisch. **#87 wartet ausdrücklich auf eure Approvals** (dein Prozess-Punkt gilt — kein Merge mit < 3 Stimmen). **Follow-up an dich (deine Lane, nach #87/#88-Merge):** `flaechen_schwellen`-Werte + `quelle` in `normwissen/data` füllen UND `provider._snapshot` so erweitern, dass die Schwellen-Quelle in `NormRegelwerk.quellen` landet — sonst bricht beim ersten getriggerten Raum die Naht-Invariante. **Sonderstellen-Contract:** ich gebe als Owner das **GO für Option A** (`RaumModell.sonderstellen[]` + `ist_barrierefrei` + `besondere_gefaehrdung`, rein additiv) — damit 2 von 3 Stimmen (du + ich); der Contract-PR braucht noch @polatselman. Dein §7-Handoff (`docs/SPEC_SONDERSTELLEN_CONTRACT.md`) kann vorbereitet werden.
- 2026-09-02 **F2: disconnected-graph-Anker — Luftlinien-Richtung statt fabriziertem „unten" (Branch `leonis/anker-disconnected`, kein Contract).** Zweiter Handoff-Kandidat: `anker_strategy.plan_rettungszeichen_anker` fiel für Kreuzungs-Anker in einer Graph-Komponente **ohne erreichbaren Ausgang** (Provider-Lücke, kein Dijkstra-Gefälle) auf `richtung="unten"` zurück — der Pfeil behauptete „Ausgang erreicht", obwohl keiner erreichbar ist. Jetzt: Luftlinie zum **geometrisch nächsten Ausgang** (beste verfügbare Richtungs-Information); existiert gar kein Ausgang im Modell, bleibt der dokumentierte Letzt-Fallback „unten". Mollgasse EG unverändert (15 RZ + 21 SL, ok — dort keine ausgangslose Komponente, No-op). +2 Tests, **537 passed/5 skip**, ruff clean, kein Contract. Unabhängig von `leonis/lb-vokabular-warnung` (PR #90, nicht gestackt).
- 2026-09-02 **F2: Prüfregel 10b — tote LB-Bereichsregeln sichtbar (Branch `leonis/lb-vokabular-warnung`, kein Contract).** PR #84 ist gemergt (Union-Auflösung wie von F1 erbeten, main `b96ea50`). Nächster Handoff-Kandidat umgesetzt: `hauptengine/validierung._lb_konformitaet` meldet jetzt Bereichsregeln, deren `raum_typ` **keinen Raum mit gültigem Polygon** matcht — bisher war so eine Regel ein **dreifach stiller No-op** (`lb_override` wirkt nicht, Regel 9/10 laufen gar nicht erst, Prüfbericht „ok"): der Plan sah konform aus, obwohl eine explizite Auftraggeber-Vorgabe nie angewendet wurde (die reale Bug-Klasse ABSTELLRAUM/LAGER/TECHNIK aus PR #58, dort nur statisch per Drift-Guard gedeckt — 10b ist das **Laufzeit**-Pendant je Plan). Status **warnung** (Raumtyp kann legitim fehlen), Detail nennt die toten Typen + Hinweis „nur Räume ohne gültiges Polygon" wenn der Typ existiert, aber geometrisch nicht wirkbar ist. **Real-Data-Verifikation:** Mollgasse EG + eigene Elektro-LB → bit-identisch (15 RZ + 21 SL, ok; die LB hat keine Bereichsregeln). Cross-Check Mollgasse + Fischa-GK4-LB → Exklusion STIEGENHAUS/GANG wirkt real (21 SL entfernt), Inklusion GARAGE matcht keinen Raum → 10b-Warnung `['GARAGE']`. +5 Tests, **535 passed/5 skip**, ruff clean, Schema kein Drift. Nur `hauptengine/validierung.py` + Tests — berührt NICHT `flaechen_strategy`/Contracts (kein Overlap mit F1s offenen #87–#89).
- 2026-09-01 **Leonis → @F2: PR #84 (`leonis/abstand-nachpass`) selbst auflösen + mergen — Handoff-Konflikt mit #85.** Auf User-Wunsch sollten #83 (Enis, gemergt+verifiziert) und #84 gemergt werden. #83 ist auf `main` (`cfcbbde`), Track B damit AKTIV — Regress-Check ok: Mollgasse EG unverändert 15 RZ + 21 SL, Prüfstatus ok, 524 passed. **#84 konnte ich NICHT mergen:** (a) der Branch ist live in eurem Worktree `Notbeleuchtung-F2` (ich fasse ihn nicht an, kein force-push), (b) er kollidiert mit meinem gemergten #85 auf `Handoff/LEONIS.md`. **Bitte bei euch lösen:** `git fetch origin && git merge origin/main` auf `leonis/abstand-nachpass`, den Handoff-Konflikt **per Union** auflösen (mein „STAND (2026-09-01, Nacht)"-Block bleibt oben stehen, euren abstand-nachpass-STAND darunter einreihen), dann PR #84 mergen. Nur der Handoff-Doc kollidiert — der Code (`platzierung/abstand_nachpass.py` + Test) ist konfliktfrei.
- 2026-09-01 **F2: Abstands-Nachpass gegen Kollisionen an der Strategie-Naht (Branch `leonis/abstand-nachpass`, kein Contract).** Neuer letzter Geometrie-Pass `platzierung/abstand_nachpass.py` (`entzerre`, läuft in `place` nach `lb_override`, vor `deckungs_zuordnung`): gleich-artige Koinzidenzen mergen (echte Dubletten aus Anker+Gang / zwei Flächen-Pässen), verschieden-artige deterministisch nudgen (Prio rz>sl>antipanik, im Raumpolygon geclamped, **nie eine benötigte Leuchte löschen**). Jede Strategie deduplizierte bisher nur intern (`anker._MIN_RZ_MERGE_MM`, nur RZ↔RZ) — die Naht zwischen Strategien war ungeprüft. **Ehrlich reframed:** DOD-Befund #5 (1 Paar < 250 mm, 2026-08-31) **reproduziert auf `main` f92010f nicht mehr** (mit LB verifiziert: 36 Symbole, 0 Kollisionen, mit UND ohne den Pass) — der Nachpass ist **kein Bugfix für einen lebenden Defekt, sondern eine strukturelle Garantie** (Defense-in-depth: Kollisionsfreiheit invariant statt zufällig); auf Mollgasse EG aktuell ein No-op. Wert-Schwerpunkt daher der **fehlende Real-Data-Regressionstest** `tests/e2e/test_mollgasse_eg_durchstich.py` (skip-if-Asset): Kollisions-Regel=ok + alle Abstände ≥ 250 mm + Symbolzahl-Band — schließt die Fixture-Lücke, an der C2/Belegung/covers_segment durchrutschten (nur das dünne 4OG-Fake wurde getestet). +11 Tests (8 Unit synthetisch, 3 E2E), Mechanismus gegen Koinzidenzen unit-getestet. Suite grün, ruff clean, Schema kein Drift (kein Contract). PR wartet auf User-GO.
- 2026-09-01 **Enis: KORREKTUR einer eigenen bindenden Entscheidung — §4.1.2 nennt sehr wohl ein Lux-Niveau (5 lx VERTIKAL).** Der bis heute wichtigste offene fachliche Punkt ist geprüft, und die Annahme vom 31.08. („§4.1.2 belegt die Hervorhebungspflicht, nicht den Wert; die 5 lx stammen aus der Projekt-LB") ist am Volltext widerlegt. §4.1.2 **h)**: „nahe jeder Erste-Hilfe-Stelle, **so dass 5 lx vertikale Beleuchtungsstärke am Erste-Hilfe-Kasten erreicht werden**"; §4.1.2 **i)**: „nahe jeder Brandbekämpfungs- und Meldeeinrichtung, **so dass 5 lx vertikale Beleuchtungsstärke an den Melde-, den Brandbekämpfungseinrichtungen und der Anzeigen der Brandmeldeanlage erreicht werden**" (`knowledge/_extracted_text/normen/EN 1838 - Notbeleuchtung 2019.txt`, Norm-S.9). Damit ist der Wert für **feuerloescher, hydrant, erste_hilfe, brandmelder** normativ belegt; die reale Elektro-LB §5.1.23 **wiederholt** ihn nur. Die Hierarchie bleibt: weicht eine LB ab, übersteuert sie. **Entscheidend und unverändert ist die Bezugsfläche** — die 5 lx sind **vertikal am Gerät**, der Lux-Nachweis der Engine (`platzierung/lux.py::lux_raster`) rechnet **horizontal am Boden**. Ein Einsetzen als `min_lux` wäre derselbe Kategorienfehler wie Ud gegen Uo. Deshalb trägt die Query-API die Achse jetzt im Namen: `norm_lux_vertikal()` → 5.0, `norm_lux_horizontal()` → **immer** `None`, `norm_lux_bezugsflaeche()` → `"vertikal"`; die alte achslose `norm_lux()` wurde **entfernt**, nicht umgewidmet. In `platzierung_regeln.yaml` heißt der Schlüssel `min_lux_vertikal_norm` — er kann nicht versehentlich in den Bodenraster laufen. **Nebenbefund, damit ebenfalls erledigt:** §4.1.2 führt **b) Treppen** und **c) „jede andere Niveauänderung"** als getrennte Punkte — die frühere Notiz „unsere Extraktion nennt Treppen, die reale LB nennt Niveauänderungen" ist gegenstandslos. `RZ-06-NIVEAUAENDERUNG` und `SL-04-NIVEAUAENDERUNG` sind von `beleg: LB` / `decision_source: lb_explizit` auf `BELEGT` / `norm_default` gezogen; ihr **Lux-Wert bleibt offen** (§4.1.2 c) nennt keinen), also weiter `MANUELL_PRUEFEN`. **Warum es zuerst übersehen wurde:** die Prüfung am 31.08. stützte sich auf `_port_source/emergency_lighting_en1838.yaml` statt auf den Volltext; die Extraktion führt §4.1.2 verkürzt und ohne die Buchstaben h)/i). Lehre, die ab jetzt gilt: **die Extraktion ist ein Index, kein Beleg.** Geändert: `normwissen/data/sonderstellen.yaml` (5 Typen), `normwissen/sonderstellen.py` (Lux-API), `normwissen/data/platzierung_regeln.yaml` (SL-04…SL-08, RZ-06), 3 Tests umgedreht + 3 neue, `docs/NORMQUELLEN_AT.md` Abschnitt **2c**, `docs/SPEC_SONDERSTELLEN_CONTRACT.md` §3, `Handoff/ENIS.md`. **519 passed / 5 skipped**, ruff sauber, Schema in sync, **kein Contract berührt**, Mollgasse-EG-Durchstich unverändert (15 RZ + 21 SL, ok). **@mvpo3 / @polatselman:** das ändert nichts am Sonderstellen-Vorschlag selbst — es macht ihn stärker: vier der fünf Typen haben jetzt einen belegten Norm-Wert statt eines Review-Flags.
- 2026-09-01 **Enis: Track-B-Norm-Werte gefüllt (Branch `enis/norm-trackB-werte`, KEIN Contract) + vier Quellen-Korrekturen an PR #72.** Zwei der vier v1.1.0-Felder sind jetzt belegt gefüllt, zwei bleiben bewusst leer. Geprüft am Volltext der im Repo liegenden Ausgabe (`knowledge/_extracted_text/normen/EN 1838 - Notbeleuchtung 2019.txt`), Details `docs/NORMQUELLEN_AT.md` Abschnitt **2b**. **@mvpo3 — vier Korrekturen:** (1) **Antipanik-Ud ist 40, nicht 10.** §4.2.2 (Rettungsweg) und §4.3.2 (Antipanik) sagen wortgleich „darf 1 : 40 nicht unterschreiten". (2) Die „10" stammt aus **§4.4.2** (Arbeitsplätze mit besonderer Gefährdung, **Uo ≥ 0,1**) — Uo (kleinste:mittlere, EN 12665) ist **nicht** Ud (kleinste:größte), also ein anderes Maß und das falsche Feld. Die Fehlangabe steht im Docstring von `hauptengine/contracts/norm_regelwerk.py` (Feld `gleichmaessigkeit_max`), im Docstring von `ud_min_aus_norm` in `platzierung/lux.py` und im PR-#72/#81-Text — beide Dateien liegen nicht in Enis' Lane, deshalb nur gemeldet, nicht angefasst. (3) **60 m² / 8 m² stehen NICHT in EN 1838**; der Contract-Docstring schreibt sie „EN 1838 §4.3 / OIB" zu. In der vorliegenden Ausgabe kommt überhaupt keine flächenbezogene Auslöse-Schwelle vor; §4.3.8 nennt Toiletten für Menschen mit Behinderung **ohne** Flächenmaß. (4) `umschaltzeit_max_s` ist als **Skalar** nicht ausreichend: §4.2.6/§4.3.6/§5.4.6 fordern **zweistufig** 50 % in 5 s und 100 % in 60 s. **Gefüllt:** `gleichmaessigkeit_max` = 40 für Rettungsweg (§4.2.2) und Antipanik (§4.3.2) über ein neues `gleichmaessigkeit_ref` in `raumtyp_regeln.yaml`; `umschaltzeit_max_s` = 60 s (Vollwert), die 5-s-Halbwertstufe bleibt als `umschaltzeit.halbwert_s` in der YAML sichtbar. Aufheller/Betonungsleuchten (§4.1) bekommen **keinen** Ud-Wert — die Norm nennt für sie keinen. **Beides ist inert:** 40 ergibt über `ud_min_aus_norm` exakt den bisherigen Default 1/40, `umschaltzeit_max_s` greift in `validierung.pruefe` nur gegen einen LB-Wert. Mollgasse-EG-Durchstich vorher/nachher **identisch: 15 RZ + 21 SL, Prüfstatus ok, 7 Befunde**. **NICHT gefüllt — `flaechen_schwellen`, mit Vorschlag:** die Werte sind belegt, aber in **OVE E 8101:2019 `718.560.9.001.AT`** bzw. **ÖVE/ÖNORM E 8002-1**, und dort **scope-gebunden** — die 8 m² gelten nur „für Räume, Anlagen oder Gebäude, an die erhöhte Anforderungen nach der Art der Nutzung (OVE R 12-2 bzw. OIB-RL 2) gestellt werden"; die 60 m² dort nur für **Flughäfen und Bahnhöfe**; der allgemeine 60-m²-Satz steht in E 8002-1 §3.2.2.1.2 nur als **ANMERKUNG** in einer Begriffsbestimmung. `flaechen_strategy._ist_flaechen_antipanik` wendet die Schwelle dagegen **global auf jeden Raum** an — ein Füllen würde die Norm über ihren Geltungsbereich hinaus anwenden und den Auslöser im Audit-Trail unter `norm_quelle = "ÖNORM EN 1838:2013 §4.3.1"` führen, obwohl er aus OVE stammt. **Vorschlag:** den Flächen-Trigger an den bereits vorhandenen **`OibRl2Provider`** gaten — der bewertet genau die „erhöhten Anforderungen nach der Art der Nutzung", auf die OVE E 8101 verweist. Bis zur Entscheidung bleiben beide Felder `None` (inert, kein Fehlalarm). **NICHT gefüllt — `arbeitsplatz_lux`:** §4.4.1 (10 % der Nennbeleuchtungsstärke, mind. 15 lx) ist belegt, aber ohne Raumtyp „Arbeitsplatz mit besonderer Gefährdung" im RaumModell wäre der Wert toter Code → **Track C, @polatselman**; dieselbe Lücke führt `sonderstellen.yaml` als `besondere_gefaehrdung`. **Nebenbefund:** Anhang B (A-Abweichungen) führt Frankreich, Italien, Deutschland und die Niederlande — **für Österreich keine Abweichung**; die deutschen 15 s für §4.2.6/§4.3.6 gelten hier ausdrücklich nicht. `tests/fixtures/norm_regelwerk_snapshot.json` blieb unangetastet (3-Owner-Lane) → `FakeNormProvider` liefert weiter `None`, die Fake-basierten Tests üben also den Fallback-Pfad; das ist gewollt. +9 Tests, **517 passed / 5 skipped** (vorher 508), Schema in sync, ruff sauber, kein Contract berührt.
- 2026-09-01 **Enis → @mvpo3 / @polatselman: Sonderstellen-Contract — Entscheidung weiterhin offen (2. Bitte).** PR #69 ist seit 31.08. gemerged, hat aber **0 Reviews und 0 Kommentare**, und im Log steht keine Reaktion. Der fachliche Vorschlag ist fertig und ausführbar (`docs/SPEC_SONDERSTELLEN_CONTRACT.md` §6 Optionen A/B/C, §7 Handoff nach dem GO; `normwissen/data/sonderstellen.yaml` + `SonderstellenKatalog` + 17 Tests). **Empfehlung unverändert Option A** — generisches `RaumModell.sonderstellen[]` (feuerloescher · hydrant · erste_hilfe · brandmelder · niveauaenderung) + `ist_barrierefrei` (§4.3.8) + `besondere_gefaehrdung` (§4.4.1). Rein additiv, alle Felder mit Default, schaltet **exakt** die 8 heute blockierten Placement-Regeln frei (ein Test hält die Gleichheit fest); vier davon sind belegte Pflichtstellen aus §4.1.2. Solange das GO fehlt, bleibt jeder erzeugte Plan in diesem Punkt unvollständig, **ohne dass man es der Ausgabe ansieht**. `besondere_gefaehrdung` ist zusätzlich die Voraussetzung dafür, dass das schon existierende Contract-Feld `arbeitsplatz_lux` überhaupt einen Auslöser bekommt (s. Eintrag oben) — die beiden Themen hängen zusammen. Track B fasst `hauptengine/contracts/**` bis zum GO nicht an.
- 2026-09-01 **Enis: Prozess-Punkt — Approvals in der `normwissen`-Lane.** Sachlich, keine technische Frage. `src/notbeleuchtung/normwissen/` ist per CODEOWNERS Enis' Lane; **#14, #22, #23 und #40** gingen ohne Enis-Approval durch. Neu dazu: **PR #72** hat `hauptengine/contracts/norm_regelwerk.py` auf v1.1.0 gehoben, war im eigenen PR-Text ausdrücklich als **„braucht 3-Owner-Approval"** deklariert und trägt trotzdem nur **ein** Approval (@polatselman) — gemerged von @mvpo3. Genau dieser PR hat die vier Quellen-Fehler transportiert, die der Eintrag oben korrigiert; ein Review aus der Normwissen-Lane hätte sie vor dem Merge gefunden. Bitte: Contract-PRs und `normwissen/**`-PRs vor dem Merge auf das dritte Approval warten lassen. Der Contract selbst ist inhaltlich in Ordnung und wird nicht zurückgedreht — es geht nur um den Weg dorthin.
- 2026-09-01 **Leonis: Norm-Integration Platzierung Track B — Konsumption der v1.1.0-Felder (Branch `leonis/norm-trackB-konsum`, kein Contract).** PR #72 (`NormRegelwerk` v1.1.0) ist gemergt → Leonis konsumiert die neuen abfragbaren Felder, **defensiv**: solange Enis' Werte `None` sind, ist der Plan bit-identisch. (A) `lux.lux_raster` bekommt `ud_min`; `deckung` + `flaechen_strategy` leiten es über `ud_min_aus_norm(anf.gleichmaessigkeit_max)` ab (Hardcode `1/40` weg) — sobald die Norm füllt, bekommt Antipanik sein korrektes **1:10**, Fluchtweg bleibt 1:40. (B) `flaechen_strategy` liest `regelwerk_snapshot().flaechen_schwellen`: offene Fläche ≥ `antipanik_min_m2` bzw. WC/Sanitär ≥ `wc_sanitaer_min_m2` wird antipanik-pflichtig (EN 1838 §4.3) — reiner **Zusatz**-Trigger, überschreibt nie eine Klassifikation; Antipanik-Parameter (0,5 lx/Symbol/Quelle) aus Enis' eigener Antipanik-Regel, nicht fabriziert. (D) `validierung.pruefe(…, norm=…)`: neue Regel **Umschaltzeit ≤ Norm-Höchstwert** (LB-`umschaltzeit_max_s` vs. strengster Norm-Wert) — LB > Norm → Warnung; fehlt ein Wert, übersprungen. Pipeline reicht `bundle.norm` durch. **Mollgasse EG unverändert: 15 RZ + 21 SL, Prüfstatus ok.** +8 Tests, 513 passed/2 visual-deselect, ruff clean, Schema kein Drift (kein Contract). **@EnisAMG:** die Felder werden jetzt konsumiert — sobald du `gleichmaessigkeit_max` (40/10), `flaechen_schwellen` (≈60/8 m²) und `umschaltzeit_max_s` in `normwissen/data` füllst, aktiviert sich die Logik automatisch (bis dahin inert, kein Fehlalarm). **Track-B-Rest VERTAGT:** Arbeitsplatz-Lux 15/5 lx (`arbeitsplatz_lux`) ist verdrahtungsbereit, aber es fehlt der Raumtyp „Arbeitsplatz mit besonderer Gefährdung" (EN 1838 §4.4) im RaumModell/Vokabular → **Track C** (@polatselman: neuer Raumtyp/POI, + Enis-Vokabular). Ohne den bliebe die Konsumption toter Code, daher bewusst nicht gebaut. PR wartet auf User-GO.
- 2026-09-01 **Leonis → @F2: circuit_hint DL/BL-getrennt + gedeckelt (erledigt #78-Befund).** F2s Verifikation deckte auf: alle Leuchten hingen grob auf 2 Kreisen (AGV-A/B-F13), Dauer- (RZ) + Bereitschaftslicht (SL/AP) gemischt. Neuer zentraler Nach-Pass `platzierung/circuit_zuordnung.py` (läuft zuletzt in `platzierer.place`, nach lb_override): je (Gebäude, Schaltungsart) fortlaufende Kreise `AGV-{G}-F13-{DL|BL}-{n}`, Deckel `_MAX_LEUCHTEN_JE_KREIS=20`. Mollgasse EG danach: `AGV-A-F13-DL-1` (10 RZ), `AGV-B-F13-DL-1` (5 RZ), `AGV-A-F13-BL-1` (2 SL), `AGV-B-F13-BL-1` (19 SL) — DL/BL sauber getrennt, `F13`-SV-Kennung bleibt (Naht zu validierung), Prüfung ok. **(a) DL/BL-Trennung + (b) Deckel erledigt.** Offen: der echte Deckel ist strombasiert (§3b, mA) → braucht Produkt-Stromaufnahme (Symbol-Datenmodell #6 / LB); bis dahin Stückzahl-Platzhalter. +3 Tests, kein Contract. 507 passed/5 skip (inkl. visual), ruff clean.
- 2026-09-01 **Leonis: Render-Test-Fixture-Lücke geschlossen — zweiter Visual-Golden (Misch-Szene).** Sowohl C2 (Doppelpfeil) als auch der Belegungs-Overflow versteckten sich hinter derselben dünnen Fixture: der 4og-Golden trägt nur 5 RZ (alle gerichtet, kein „gerade", wenige IDs) → beide Bugs waren grün. Neuer `test_visual_golden_mix` mit einer realistischen Szene, die genau die blinden Pfade ausübt: **RZ `richtung="gerade"` (Doppelpfeil), Sicherheitsleuchte + Antipanik als eigene Symbole, Belegung mit DL+BL über zwei Kreise**. Selbst-validierend (Entity-Asserts: 7 Platzierungen → 8 INSERTs weil die gerade-RZ = 2 Blocks; DL+BL in der Belegung) → kein blindes Golden. Vergleichslogik in `_assert_matches_golden` refaktoriert, 4og-Referenz unangetastet. Neuer Golden `mix_notbeleuchtung.png`. NUR `tests/`, kein Contract, kein Produktivcode. 502 passed/5 skip (+2 visual grün), ruff clean.
- 2026-09-01 **Leonis: Stromkreis-Belegungsliste kompakt — Overflow-Fix (#74-Follow-up).** Die Belegungs-Info-Box listete JEDE Leuchten-ID pro Kreis → auf realen Plänen 200+-Zeichen-Zeilen (Mollgasse EG: 217, 24 IDs), die in der festhöhigen Box umbrachen und nach unten in die Legende-Box überliefen. `pytest` grün, weil der 4og-Golden nur 5 IDs hat (dieselbe Fixture-Lücken-Klasse wie C2). Jetzt eine **kompakte Zeile je Kreis** (Anzahl je Art + Schaltungsart + Σ, z.B. `AGV-B-F13: 5× RZ (DL) · 19× SL (BL) — Σ24`, 41 Zeichen); die genaue ID↔Kreis-Zuordnung trägt der Plan selbst (NODEID-Annotation + Kreis-Label je Symbol). +Regressionstest (35 Leuchten → kurze Zeile), Visual-Golden neu. NUR `render/dxf_renderer.py`, kein Contract. 502 passed/5 skip, ruff clean.
- 2026-09-01 **Leonis: C2-Render-Fix — Doppelpfeil nur für Rettungszeichen (`kind=="rz"`).** Regression aus #73: `inserter.insert_platzierung` schaltete den beidseitigen Doppelpfeil allein an `richtung=="gerade"` — aber **Sicherheitsleuchten + Antipanik tragen ebenfalls `richtung="gerade"`** (= keine Richtung). Folge auf main: jede SL/AP rendert als **2 RZ-Richtungspfeile** statt ihres Symbols (Mollgasse EG: 21 SL → 42 falsche Pfeile). `pytest` war grün (4og-Golden hat keine „gerade"-Platzierung) → RIVOPLAN hätte es live geschaltet. Fix: Gate zusätzlich auf `p.kind == "rz"`; SL/AP behalten ihr Katalog-Symbol. +Regressionstest (SL/AP·gerade → 1 Symbol). Durchstich Mollgasse EG danach: 15 RZ + 21 SL = 36 Inserts (1:1). NUR `symbols/inserter.py`, kein Contract. 501 passed/5 skip, ruff clean.
- 2026-09-01 **F2 (Render, Branch `leonis/render-belegung`, kein Contract): Stromkreis-Belegungsliste (§3b).** PR #73 (DIN_SIBEL-Layer + Doppelpfeil + NODEID) ist **gemergt** (main `030815b`). Folge-Slice: neue Info-Box „STROMKREIS-BELEGUNG" oben in der Schriftfeld-Leiste (Layer `din_SIBEL_11_system`) — je Endstromkreis (`circuit_hint`) die zugeordneten Leuchten-IDs (dieselbe NODEID wie die Symbol-Annotation, via geteiltem `_nodeids()`-Helper), Schaltungsart **DL/BL** (`_SCHALTUNGSART`: RZ=Dauerlicht, SL/AP=Bereitschaftslicht) und Anzahl — kompatibel zur Profi-Vorlage `1.xlsx`. Render-only, konsumiert nur vorhandenes `circuit_hint` + `kind`, **kein Contract**. `_draw_nodeid_labels` auf den geteilten Helper umgestellt (IDs deckungsgleich). Summary-Feld `stromkreis_belegung_drawn`. Visual-Golden bewusst neu. +2 Tests. NUR `render/dxf_renderer.py`. 494 passed/5 skip, ruff clean, Schema in sync.
- 2026-09-01 **F2 (Render-Ausbau): Commit 3 — NODEID-Text-Annotation je Leuchte.** Fortlaufende Leuchten-ID (RZ-001/SL-002/AP-003, je Art gezählt) als kleiner MTEXT neben jedes Symbol, Layer `din_SIBEL_63_luminaire_ID` — Wartung/Adressierung (Profi-Plan §1.4). Rein Render-seitig aus der Platzierungs-Reihenfolge synthetisiert, **kein Contract-Feld**. Sitzt tangential zur Symbol-Achse (kollidiert weder mit Stromkreis-Label +Normale noch Höhenkote −Normale). Neue Funktion `_draw_nodeid_labels` + Layer + Summary-Feld `nodeids_drawn`. NUR `render/dxf_renderer.py`. Visual-Golden **bewusst neu** (neue Texte = sichtbare Änderung, `NOTBEL_UPDATE_GOLDEN=1`) → `tests/fixtures/golden/4og_notbeleuchtung.png` aktualisiert. +1 Test. 492 passed/5 skip, ruff clean, Schema in sync. **Render-Ausbau-Branch fertig (3 Commits) — PR gegen main wartet auf User-GO.**
- 2026-09-01 **F2 (Render-Ausbau): Commit 2 — Beidseitig-Doppelpfeil für `richtung="gerade"`.** Der beidseitige RZ (Profi-Plan RZ_PLPR, Referenz §1.1) steht in Flur-Mitte zwischen zwei Ausgängen und weist in BEIDE Richtungen. `inserter.insert_platzierung` zeichnet bei `richtung="gerade"` jetzt zwei horizontale Pfeil-Blocks (`notlicht_ks_stiege_links` + `_rechts`) am selben Punkt, gemeinsam um `rotation_deg` gedreht (Wasserscheide) statt eines Einzelsymbols; primärer (linker) Insert wird zurückgegeben und trägt allein den Stromkreis-XDATA-Tag. Refactor: `_skalen()` + `_insert_block()` extrahiert (DRY, Einzel- + Doppel-Pfad teilen Scale/Mirror/Blockref). **Kein Contract** (`richtung="gerade"` existiert schon), NUR `symbols/inserter.py`. 4og-Golden hat keine gerade-Platzierung → Insert-Zähl-Tests + Visual unverändert. +2 Tests (`test_inserter.py`). 491 passed/5 skip, ruff clean, Schema in sync.
- 2026-09-01 **F2 (Render-Ausbau, Branch `leonis/render-ausbau`, kein Contract): Commit 1 — DIN_SIBEL-Layer-Schema (Lean-Rename).** Ad-hoc-`E_*`-Layer → DIN_SIBEL-Profi-Konvention (Referenz `knowledge/extracted/PROFI_DIN_PLAN_UND_VORSCHRIFTEN.md` §1.3), 1 Layer je Plan-Element, keine Symbol-internen Änderungen. Vorher→Nachher: `E_Sicherheitsbeleuchtung`→`din_SIBEL_10_emergency_lighting` · `E_Stromkreis_Label`→`din_SIBEL_61_labeling` · `E_Notbeleuchtung_Hoehenkote`→`din_SIBEL_52_info` · `E_Notbeleuchtung_Stueckliste`→`din_SIBEL_70_legend_green` · `E_Notbeleuchtung_Legende`→`din_SIBEL_70_legend_white` · `E_Notbeleuchtung_Plankopf`→`din_SIBEL_99_titleblock` · `E_Notbeleuchtung_Pruefbericht`→`din_SIBEL_99_inspection`. `ARCH_Raum`/`ARCH_Fluchtweg` unverändert (Architektur-Hintergrund, kein SIBEL). **Naht-Detail:** der physische Lib-Layer heißt weiter `E_Sicherheitsbeleuchtung` (Block-Geometrie liegt auf Layer `0`, erbt den INSERT-Layer) → `library.sync_layers` benennt ihn beim Import auf `din_SIBEL_10_...` um + hält den Grün-Override; Visual-Golden **unverändert grün** (kein Farb-Drift). Dateien: `render/dxf_renderer.py`, `symbols/library.py`, `tests/render/test_render_dxf.py`. 489 passed/5 skip, ruff clean, Schema in sync (kein Contract).
- 2026-09-01 **Leonis: Norm-Integration Platzierung (Track A, Branch `leonis/norm-integration-platzierung`, kein Contract, 437 grün).** Ziel: die schon in `normwissen/data` kodierten Norm-Werte konsequent durch die Platzierung fließen lassen statt hardcoden. (A1) `deckung.verdichte_fluchtweg` zieht `ziel_lux` aus `anf.min_lux` statt Konstante 1,0 (norm-belegt via `anf.quelle`). (A2) `flaechen_strategy` verdichtet **Antipanik bis zum 0,5-lx-Nachweis** (`_antipanik_punkte`) statt blind `mindest_anzahl` — der 0,5-lx-Wert war bis dato tot; kleine Räume unverändert (4er-Raster erfüllt 0,5 lx), große Halle verdichtet (Cap gegen Überproduktion). (A3) neue Validierungsregel **2-Leuchten-Redundanz je Fluchtweg-Abschnitt** (EN 50172 / §5.1.8), Warnung nicht Hard-Fail. (A4) `lux_raster`-Fallback-Höhe 2,5→2,0 m (EN-Mindesthöhe). **Mollgasse-EG-Durchstich unverändert:** 15 RZ + 21 SL, Prüfstatus **ok**, alle 103 Abschnitte ≥ 2 Leuchten (Redundanz greift, kein Rauschen). Schema unverändert (kein Contract). PR noch offen (User-GO). **Track B/C (Roadmap):** neue abfragbare Norm-Werte (Ud/Flächen-Trigger 60m²·8m²/Arbeitsplatz-Lux 15·5) = Contract-Erweiterung `NormRegelwerk` (3-Owner, Enis-Daten); Pflichtpunkte (Aufzug/Erste-Hilfe/Löschgerät) = Selman-RaumModell-POIs.
- 2026-09-01 **Hinweis an Enis:** PR #60 ist bereits **gemergt** (2026-08-31 20:18, `8eaa1f8`) — nichts mehr zu approven. Der „Track-A"-Punkt `LbReviewRequired→HTTP 500` ist ebenfalls erledigt: `pipeline.py:117-122` fängt `LbFehler` (→ `lb_review`-Flag, Plan läuft norm-getrieben weiter), `api/main.py:91-92` mappt jede Exception auf 422. Kein 500-Pfad mehr.
- 2026-08-31 Enis **Tagesabschluss**: vier PRs gemerged — #60 (LB-Parser + API-Naht, fail closed, Raumtyp-Vokabular synchronisiert, an 4 realen LB-PDFs gegengeprueft), #67 (`lb_review` erreicht den Client; `/plan` UND `/projekt`), #68 (Placement-Decision-Matrix: 25 Regeln + 4 Hard Stops + Ground-Truth Mollgasse), #69 (Sonderstellen-Spezifikation, **Contract NICHT geaendert**). `origin/main` = `d915342`, 486 passed/5 skip, ruff sauber, Schema in sync, keine offenen PRs, keine ungesicherte lokale Enis-Arbeit. **Einziger Blocker: das 3-Owner-GO fuer den Sonderstellen-Contract (Option A) steht aus** — @mvpo3 und @polatselman, Entscheidung erbeten; Details `docs/SPEC_SONDERSTELLEN_CONTRACT.md`. Bis zum GO wird `hauptengine/contracts/**` von Track B nicht angefasst. Track-B-unabhaengige Folgethemen (Lux-Niveau an Betonungsstellen, Niveauaenderung am Original, Quellenlage OVE R 12-2 / E 8350 / TRVB E 102, Wegbreite/Randstreifen) stehen in `Handoff/ENIS.md` unter „MORGEN ZUERST".
- 2026-08-31 Enis: **Sonderstellen-Contract-VORSCHLAG** (`docs/SPEC_SONDERSTELLEN_CONTRACT.md` + `normwissen/data/sonderstellen.yaml` + `SonderstellenKatalog`, 17 Tests). **Kein Contract geaendert, kein Version-Bump — wartet auf 3-Owner-GO.** Vorschlag: ein generisches `RaumModell.sonderstellen[]` (Typen feuerloescher/hydrant/erste_hilfe/brandmelder/niveauaenderung) + zwei Raum-Flags `ist_barrierefrei` (§4.3.8) und `besondere_gefaehrdung` (§4.4.1). Schaltet **exakt** die 8 blockierten Matrix-Regeln frei (Test haelt Gleichheit fest), rein additiv, alle Felder mit Default. Typ-Namen sind nicht erfunden: der Profi-Plan `din_support_ReMi_Barawitzkagasse` fuehrt `din_Feuerloescher_F001` / `din_Hydrant_F002` / `din_ErsteHilfe_E003` (ISO-7010-Nummern). Datenquellen-Befund: **kein** Typ ist heute automatisch erkennbar — der Architekturplan traegt keine Sonderstellen (an Mollgasse geprueft), die LB liefert Lux ohne Koordinate, ein bestueckter Elektroplan liegt nicht im Repo. Der Vorschlag ist deshalb ohne Parser nutzbar. Die 5 lx an Feuerloescher/Hydrant bleiben ausdruecklich LB-Wert, `norm_lux()` gibt fuer JEDEN Typ `None`. Optionen A/B/C + Empfehlung (A) im Spec-Dokument. **@mvpo3 / @polatselman: Entscheidung erbeten.**
- 2026-08-31 Enis: **Placement-Decision-Matrix** (`normwissen/data/platzierung_regeln.yaml` + Query-API `PlatzierungsRegelwerk`). 25 Regeln (11 RZ, 14 SL) + 4 Hard Stops: Ausloeser -> Leuchtenart, Positionierungsziel, Orientierung, Abstand/Lux, Prioritaet, Ausnahmen, Konfliktregel, Quelle, Normreferenz, Review-Flag, Decision-Source. Entscheidungs-Hierarchie maschinenlesbar (hard_stop > lb_explizit > referenz_praxis > norm_default); `gewinner()` gibt bei Gleichstand `None` = Review. Keine zweite Regelwelt — Zahlen bleiben in en1838_grundwerte.yaml, referenziert ueber `*_ref`. **@mvpo3:** Track-A-Vorrat ist 17 umsetzbar / 5 teilweise / 8 durch Contract-1 blockiert; Details + Contract-Vorschlag `Sonderstelle` in `docs/PLACEMENT_DECISION_MATRIX.md`. **@polatselman:** die Raumerkennung erzeugt an Mollgasse (EG/1OG/1KG) **0 `stair_exit` und 0 `stair`-Knoten**, obwohl das EG zwei STIEGENHAUS-Raeume hat -> RZ-05/RZ-07 sind auf echten Plaenen unerreichbar. Ground Truth: es gibt **keinen** professionell gezeichneten Mollgasse-Notbeleuchtungsplan im Repo (Architekturplaene haben 0 Notbeleuchtungs-Layer) — die 7 GT-Faelle beschreiben deshalb die Ausloeser-Lage, nicht ein Soll-Ergebnis. 469 passed/5 skip.
- 2026-08-31 **Leonis (F1) Session-Ende — 11 PRs #46–#64 auf main (166c234), 434 grün, kein Contract.** Render: Höhenkoten (h=2,40), Farb-7-Inversion (Legende/Plankopf im Hell-PDF sichtbar), Schriftfeld-Leiste (Info-Blöcke gerahmt rechts), DoD-Visual-Golden-Harness + CI-Raster-Smoke. Platzierung: covers_segment-Fix (geometrische Deckung real 0→103), RZ an jedem Notausgang (§4.1.2 g auch graphlos) + sichtlinie-Symmetrie + Anker-Dedup (keine Doppelplatzierung <250mm). Validierung: Plausibilitäts-Regel + Symboldichte-Gate (quasi-leer=fehler), Auto-Prüfeinrichtungs-Hinweis (EN 62034 >20 Leuchten), „nahe"<2m, z=100/200 single-source. 2× ultracode-Gesamtaudit (adversarial, 7+7 Fixes). **Mollgasse EG = voll-konformer Plan (Prüf ok).** OG/DG bleiben F2-blockiert (Raumerkennung ~0 Typen). **NEU: Wissensbasis `knowledge/extracted/PROFI_DIN_PLAN_UND_VORSCHRIFTEN.md`** (echter Profi-DIN-Plan + AT/DE-Vorschriften) mit **15 Hauptengine-Empfehlungen** (Owner+Aufwand) — Roadmap in `Handoff/LEONIS.md`. Für die Hauptengine-Naht relevant: Symbol-Datenmodell-Erweiterung (TYPENAME/TYPENUMBER/Schaltungsart DL/BL) = **3-Owner-Contract-Slice**; `richtung=beidseitig` = schon `"gerade"` (kein Contract); EN-1838-Lux-Werte → Enis' NormRegelwerk; hervorzuhebende Stellen/Pflichtpunkte → Selmans RaumModell.
- 2026-08-31 Enis: **LB-Naht geschlossen** (Branch `enis/lb-parser`, rebased auf `9d3c080`). API zurück auf die main-Namen (`LbTextProvider` + Modul-`parse_lb`/`parse_bericht`), `registry.py` unangetastet. Raumtyp-Vokabular an #49/#57 angeglichen (+GARAGE/TECHNIK/LAGER/MUELLRAUM/KELLER, `TECHNIKRAUM`→`TECHNIK`, LAGER≠MUELLRAUM) — beide realen Elektro-LBs parsen jetzt durch. Fünf Feld-Lücken gegen main geschlossen (`projekt`, `batterie_standort`, Sonder-Lux-Split feuerloescher/hydrant, Norm-Schreibweise `OVE E 8101`, Inhaltsverzeichnis-Filter im Audit-Trail). Drei echte Fehler beim Test-Merge gefunden und behoben: `OverflowError` bei langer Ziffernfolge, verlorener Fluchtweg-Lux-Wert ohne Quantor, verlorene Bereichsregel wenn die Aussage in der ÜBERSCHRIFT steht ("2.11 In der Garage ist eine LED-Sicherheitsbeleuchtung herzustellen."). Alle 16 main-Tests übernommen + 1440-Regression + Drift-Gate `tests/contract/test_lb_raumtyp_naht.py`. 422 passed/5 skip, ruff clean, Schema in sync. Kein Contract-Touch.
- 2026-08-31 F2: Raumtyp **Bleed-Fix + LB-Vokabular** (stacked auf ↓, Branch `leonis/raumtyp-bleed-vokabular`). (a) Port `classify_room` von rohem Substring auf **Token/Wortgrenze** umgestellt — „gang" in „Ein/Zu/Aus-gang" und „terrasse" in „Terrassentür" typten fälschlich CORRIDOR/TERRACE (CORRIDOR=Fluchtweg → falsches Notlicht; real: „Zugang Müllraum"→GANG). Komposita-Köpfe (…küche/…zimmer) + Abstell-Prefix erhalten. (b) `raumtyp._EXTRA_DIRECT`: GARAGE/TECHNIK/LAGER/MUELLRAUM (token-exakt) — die `lb_override`-Inklusion/Exklusion für diese LB-Typen war **tote Regel** (der kanonische „Garage→SL"-Fall). A/B über 4 Projekte: 0 Regressionen (GANG-Counts unverändert), +5 korrekte MUELLRAUM (Herrenholz/Baufeld). Kein Contract-Touch. 340 passed/5 skip, ruff clean.
- 2026-08-31 F2: Raumtyp-Coverage — `raumtyp.raumtyp_flags` um österr. Plan-Abkürzungen erweitert (`_EXTRA_LABELS`, **token-exakt**, kein Substring-Bleed: „ar" nicht in „Garten"). VR→VORRAUM, AR→ABSTELLRAUM, **TRH→STIEGENHAUS** (sicherheitskritisch!), Loggia→BALKON. Fischamender BT1 EG **40→50 getypt** (UNKNOWN 20→10; Rest=Garten/Rampe/Aufzug=korrekt außen). Port `classify_room` unangetastet. Grundanalyse: Mollgasse-Geometrie-Typ (7/25) ist von Wand-Schlitz-Fragmenten blockiert (Gap-Healing-Sache), NICHT Vokabular → dort kein ehrlicher Win. Kein Contract-Touch. 319 passed/5 skip, ruff clean. Branch `leonis/raumtyp-coverage`.
- 2026-08-31 F2: LB-Parser **gehärtet** (`normwissen/lb/parser.py`, Handoff-Feinschliff #1/#2). Drei reale Fehlparses behoben, verifiziert gegen alle 4 realen LB-PDFs: (a) Fluchtweg-Lux jetzt **kontext-** statt erst-treffer-basiert → mo-Elektro **200→1 lx** (Aufzugsvorplatz-Distraktor ignoriert); (b) **„Lux"-Wortform** erkannt (`_LUX=(?:lx|lux)`) → Feuerlöscher+Hydrant 5 lx (vorher []); (c) Betriebsdauer nur im `betriebsdauer|auszulegen`-Fenster ohne `notruf` → GU-24h-Notrufakku (7380→) und Fischa-24h-Gewährleistung (1440→) **verworfen**, mo-Elektro bleibt 480; +Dezimal (8,5 Std→510) +Plausi-Caps (20 lx / 1440 min). Kein Contract-Touch. 314 passed/5 skip, ruff clean. Branch `leonis/lb-parser-haertung`.
- 2026-08-31 F2: `validierung.py` **LB-Konformität** (Befund 9/10, Branch `leonis/validierung-lb-konformitaet`, off aktuellem main). `pruefe(…, lb)` referenzierte `lb` bisher NIE — der QA-Layer, der die LB-übersteuert-Norm-Hierarchie absichern soll, prüfte die LB-Seite gar nicht. Neu: (9) **LB-Exklusion** — keine Aufheller-Leuchte (SL/Antipanik) in einem LB-ausgeschlossenen Raumtyp (Hard-Override, Fehler bei Verletzung); (10) **LB-Inklusion** — jeder LB-geforderte Raumtyp trägt ≥1 SL (Fehler wenn fehlt) → macht eine nicht-feuernde `lb_override`-Regel sichtbar (fängt genau den Dead-Rule-Bug aus PR #50). Lokaler Ray-Cast `_point_in_polygon` (kein platzierung-Import). Kein Contract-Touch. 325 passed/5 skip, ruff clean.
- 2026-08-30 F2 ②: LB-Parser `normwissen/lb/` (`LbTextProvider.parse_lb`) — Freitext/PDF → LBVorgabe. Fischa GK4: Stiegenhaus+Gänge exkl (kein SL), Garage inkl; +Skalare (8 Std→480, Umschaltzeit, Lux, System, Prüfung, Sonder-Lux, Norm-Bezug). Registry `bundle.lb`. Kein Contract-Touch. 290 grün. Branch `leonis/lb-parser`.
- 2026-08-30 F2 ①(B3): `raumerkennung/geometrie_typ.py` — STIEGENHAUS (STIEGE-Blöcke) + GANG (09-WEG/A_Fluchtweg) geometrisch, ohne Text-Label. Grund: Mollgasse-EG trägt 0 Raum-Namen (566 Texte geprüft). provider.parse Mollgasse: 0→7 typisiert (2 STIEGENHAUS, 5 GANG). 286 grün, kein Contract-Touch. Branch `leonis/raumtyp-geometrie`.
- 2026-08-30 F2: IES/LM-63-Import `photometrie/ies.py` (`lade_ies`) + Fixture `mini.ies` + `tests/normwissen/test_ies.py` (7). Gleicher `Photometrie`-Typ → F1-Naht unverändert. 170 Tests grün, ruff clean, schema in sync.
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
