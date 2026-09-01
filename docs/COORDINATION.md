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
- 2026-09-01 **Leonis: Norm-Integration Platzierung (Track A, Branch `leonis/norm-integration-platzierung`, kein Contract, 437 grün).** Ziel: die schon in `normwissen/data` kodierten Norm-Werte konsequent durch die Platzierung fließen lassen statt hardcoden. (A1) `deckung.verdichte_fluchtweg` zieht `ziel_lux` aus `anf.min_lux` statt Konstante 1,0 (norm-belegt via `anf.quelle`). (A2) `flaechen_strategy` verdichtet **Antipanik bis zum 0,5-lx-Nachweis** (`_antipanik_punkte`) statt blind `mindest_anzahl` — der 0,5-lx-Wert war bis dato tot; kleine Räume unverändert (4er-Raster erfüllt 0,5 lx), große Halle verdichtet (Cap gegen Überproduktion). (A3) neue Validierungsregel **2-Leuchten-Redundanz je Fluchtweg-Abschnitt** (EN 50172 / §5.1.8), Warnung nicht Hard-Fail. (A4) `lux_raster`-Fallback-Höhe 2,5→2,0 m (EN-Mindesthöhe). **Mollgasse-EG-Durchstich unverändert:** 15 RZ + 21 SL, Prüfstatus **ok**, alle 103 Abschnitte ≥ 2 Leuchten (Redundanz greift, kein Rauschen). Schema unverändert (kein Contract). PR noch offen (User-GO). **Track B/C (Roadmap):** neue abfragbare Norm-Werte (Ud/Flächen-Trigger 60m²·8m²/Arbeitsplatz-Lux 15·5) = Contract-Erweiterung `NormRegelwerk` (3-Owner, Enis-Daten); Pflichtpunkte (Aufzug/Erste-Hilfe/Löschgerät) = Selman-RaumModell-POIs.
- 2026-09-01 **Hinweis an Enis:** PR #60 ist bereits **gemergt** (2026-08-31 20:18, `8eaa1f8`) — nichts mehr zu approven. Der „Track-A"-Punkt `LbReviewRequired→HTTP 500` ist ebenfalls erledigt: `pipeline.py:117-122` fängt `LbFehler` (→ `lb_review`-Flag, Plan läuft norm-getrieben weiter), `api/main.py:91-92` mappt jede Exception auf 422. Kein 500-Pfad mehr.
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
