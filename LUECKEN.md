# LÜCKEN — Bestandsaufnahme der Kette DXF → Raumerkennung → Ausgänge/Fluchtwege → Platzierung → Planausgabe

**Stand:** 2026-09-30 · Branch `luecken-2026-09-30` von `selman/integration-2026-09-30` @ `0434392`
(Code-Stand `ed292e1`, darüber nur Doku) · Owner-Auftrag 2026-09-30, Schritt 1 (Bestandsaufnahme, kein Code).

## Lesart

- **Priorität:** **P0** = Abbruch oder falsches Notlicht (Leuchte in einer Verbotszone, fehlender
  Geschossausgang, Prüfstrecke bricht ab). **P1** = falsches oder fehlendes Modell ohne belegten
  Notlicht-Fehler, stiller Datenverlust, Merge- oder Abnahme-Blocker. **P2** = Nachweis-, Test-, Doku- oder
  Ausweis-Lücke. „—" = kein offener Punkt bekannt.
- **Owner-Lane:** Selman (`raumerkennung/`, Lade-/Provider-Pfad, `scripts/plan_pruefen.py`), Leonis
  (`platzierung/`), Enis (`normwissen/`, Kanon, Board), gemeinsam (`hauptengine/`; Contract = 3 Owner).
  Einträge in fremden Lanes sind **nur gemeldet**, nicht bearbeitet.
- **Belegt durch:** Testname (`Datei::Funktion`) bzw. Gate-Bedingung aus `docs/GATE_TUERSTAPEL.md` § 3.
  „—" heißt: kein Test bindet den Baustein.
- **Quellen:** Code auf `0434392` (gelesen, `grep`), `tests/`, `docs/GATE_TUERSTAPEL.md`,
  `docs/INTEGRATION_2026-09-30.md`, `docs/SLICES_K1_K4.md`, `docs/OFFENE_FRAGEN.md`, `docs/COORDINATION.md`.
  **Basislauf** = eigener `ArchitekturRaumProvider().parse(dxf, "")` plus Default-Platzierung
  (`build_default_bundle().platzierer.place`) auf `0434392`, je Plan allein, über die 13 DXF der Prüfstrecke
  (Runner und JSON außerhalb des Repos; Zählweise der Leuchten je Klasse wie
  `plan_pruefen._leuchten_je_klasse`, `scripts/plan_pruefen.py:910-927`).
  Aussagen, die nur in `Projekte/_ergebnis/VERLAUF.md` stehen, heißen **„unbelegt (nur VERLAUF)"**.

## 0. Aufrufgraph (am Code geprüft)

```
pipeline.run (hauptengine/pipeline.py:165)
 └ _parse_raum (:153) → ArchitekturRaumProvider.parse (raumerkennung/provider.py:123)
    ├ lade_dxf (dxf_load.py:232)                      Stufe 1
    ├ raeume_aus_kaskade (kaskade.py:94)              Stufe 2: finde_stempel → raeume_aus_layer (L)
    │    → raeume_aus_hatch (H) → finde_wandkoerper → tuer_oeffnungen → ordne_zu → flute_stempel (F)
    │    → komponenten_ohne_stempel (R) → bereinige_kaskade
    ├ Bounds (provider.py:132-149) · typisiere_geometrisch (:155) · Türen (:156-211)
    ├ K3-Probe (:231-239) · _tueren_und_wohnungen (:60): ordne_tueren → liftschacht_reste
    │    → Durchgänge → andere_bogenrichtung → typisiere_tueren → bilde_wohnungen
    ├ leite_ausgaenge (:245) + footprint.hauptausgaenge (:175) → ohne_unzulaessige_final_exits (:259)
    ├ fluchtwege (:266) · finde_lifte / Stiegenhaus / Anker (:274-299)          Stufe 3
    └ RaumModell (:300) · kreuzcheck (:324)
 └ _run_mit_quelle (pipeline.py:190) → platzierer.place (Leonis)              Stufe 4
    → pruefbericht (validierung.py:692) → render_dxf (dxf_renderer.py:1327)    Stufe 5
    → schreibe_bericht (lux_nachweis_bericht.py:134); PDF über dxf_zu_pdf (pdf_export.py:57)

Prüfstrecke scripts/plan_pruefen.py: main (:1984) → plan_pruefen (:1538): lade_dxf (:1544)
 → eigene Kaskade _raum_kaskade (:1546) → bis zu 8 × _figur (:137) → _fachteil3 (:1254):
   bundle.raum.parse (:1265, lädt die DXF ein zweites Mal) + platzierer.place → bericht.md / raeume.json
 → _verlauf_schreiben (:1912) erst nach der Schleife über alle Pläne
```

Prüfstrecken-Ausgabe außerhalb des Contracts (Attribute am Provider): `wand_warnungen`, `tuer_warnungen`,
`wohnungsklasse_warnungen`, `ausgangs_warnungen`, `fluchtweg_warnungen`, `sanitaer_befund`,
`geschoss_befund`, `letzte_aussenbereiche`, `letzter_kreuzcheck`. `plan_pruefen` liest davon
`fluchtweg_warnungen` (:1268), `ausgangs_warnungen` (:1269), `wohnungsklasse_warnungen` (:1308),
`letzter_kreuzcheck` (:1267), `letzte_aussenbereiche` (:1300) — **nicht** `wand_warnungen`,
`tuer_warnungen`, `sanitaer_befund` (`grep` in `scripts/plan_pruefen.py`: 0 Treffer).

---

## 1. Stufe DXF-Laden

| Nr. | Baustein | gebaut (Datei:Funktion:Zeile) | belegt durch | fehlt / Lücke | Prio | Lane |
|---|---|---|---|---|---|---|
| D-01 | DXF öffnen | `dxf_load.py:lade_dxf:232` (`ezdxf.readfile` :234) | `test_dxf_load.py::test_synth_bounds`, `::test_mollgasse_leer_ist_meter_kalibriert`; `::test_mollgasse_fertig_ist_mm` **skipped** (WHA_MOL_EG.dxf nicht im Repo, `docs/INTEGRATION_2026-09-30.md:125-127`) | Kaputte oder Nicht-DXF: `readfile` ohne Fang, Ausnahme läuft durch (API: 422, `api/main.py:315-316`; Prüfstrecke: siehe O-06). Kein Test mit defekter Datei. **→ 2a erledigt (§ 12):** `DxfNichtLesbar` mit Pfad in der Meldung, Test `test_provider.py::test_nicht_lesbare_datei_definierter_fehler`. | P2 | Selman |
| D-02 | Architektur-Raum wählen (Direct/Wrapper) | `dxf_load.py:lade_dxf:237-243`, `_has_walls:184` | `test_wandkoerper.py::test_fischamender_bt1_eg_wandkoerper` | Wrapper-Wahl hängt an `WALL_PATTERN` (≥ 10 Treffer); ohne Treffer bleibt der Modelspace. Block-Raum „best-effort, ohne Transform" (Modul-Doc :9-10). | P2 | Selman |
| D-03 | Wand-Layer-Erkennung | `dxf_load.py:WALL_PATTERN:31-35`, `_wall_layers:52` | `test_provider.py::test_ohne_wandlayer_hatch_waende_raeume_statt_valueerror`, `::test_naht_am_rain_og4_parse_ohne_abbruch`; `test_wandkoerper.py::test_ohne_wandlayer_doppellinien_auf_wand_hinweis_layer` | ARAI5 `Wand <Material> <Tragwirkung>` trifft kein Muster (`docs/INTEGRATION_2026-09-30.md:145-147`). Seit `ed292e1` kein Abbruch, aber `plan.wall_layers` leer → D-04 fällt auf `$INSUNITS`, X-01 wirft. **Owner offen:** zählt `Wand brüstungshoch` als raumbildend? (heute ja, `wandkoerper._WAND_LAYER:41-42` trifft `\bwand\b`). | P1 | Selman (Owner-Frage) |
| D-04 | mm-Kalibrierung | `dxf_load.py:_calibrate_factor:163`, `_door_arc_factor:125`, `_raw_wall_span:107` | nur synthetisch + Mollgasse-Fixtures (`test_dxf_load.py::test_wand_im_block_kalibriert_nicht_ueber_insunits`, `::test_ausreisser_kippen_den_faktor_nicht`) | S-MST (`docs/OFFENE_FRAGEN.md`, § S-MST): Türprobe nur Tiebreak (:175-176); stiller Rückfall auf `$INSUNITS` (:180-181) — **ohne Wand-Linien immer** (`_raw_wall_span` liefert 0,0 → keine Kandidaten, :171-174). Gemessen (§ 7): **8 von 13** Prüfplänen laufen über `$INSUNITS` (Rennweg EG/OG3: Wand-Layer ohne Linien-Stützpunkte; Am Rain ×6: kein Wand-Layer), und auf 4 davon widerspricht die Türprobe (Rennweg EG, Am Rain OG4/OG3/EG: Faktor 10 statt 1); Faktor nirgends ausgewiesen (`plan_pruefen` nutzt `plan.factor` nur zum Zeichnen, :159/:203-210); kein Messfall gegen echte Pläne. `_door_arc_factor` sucht `DOOR` im Blocknamen (:140-141), die Türerkennung kennt `DOOR` nicht (F-01). Owner offen: Hard Stop oder Warnung. | P1 | Selman (Owner-Frage) |
| D-05 | Bounds | `dxf_load.py:bounds_mm:249` (raise X-01), Fallback `provider.py:132-149`, `wandkoerper.py:bounds_aus_wandkoerpern:292` | `test_dxf_load.py::test_synth_bounds`; `test_provider.py::test_ohne_wandlayer_hatch_waende_raeume_statt_valueerror` (Bounds ohne Fern-Körper) | `entity_points` nimmt für INSERT nur den Einfügepunkt (`dxf_load.py:227-228`) → Extents-Ausreißer (S3c: Rennweg UG 319,9 × 1 391,2 m bei Wandkörper-Bounds 19,1 × 27,0 m, `docs/OFFENE_FRAGEN.md` § S3c). Am Rain OG4: Bounds enden bei x 63,6 m, Wand-Linien bis 78,1 m — nicht untersucht (`docs/INTEGRATION_2026-09-30.md:198-199`). Leser außerhalb: `aussen_strategy.py:73`, `bestand_leuchten.py:62`, `dxf_renderer.py:78/228/291/860/1238`, `lux_nachweis_bericht.py:165` (nur `_geschoss_extents` :338 schützt das Blatt). | P1 | Selman; Leser gemeinsam/Leonis |
| D-06 | Wandkörper nach Erscheinungsbild | `wandkoerper.py:finde_wandkoerper:130`, `_NEGATIV_LAYER:45-49` | `test_wandkoerper.py` (Rennweg/Mollgasse/Barawitzka/BT1, 11 Tests); Gate M17 (18/18) | `_NEGATIV_LAYER` trifft `Moeblierung`/`Möblierung` nicht (Regex geprüft: `KFLD-04_Moeblierung-Bank` → kein Treffer) → Am Rain EG Freiraum-Hatches zählen als Wandkörper (`docs/INTEGRATION_2026-09-30.md:232-233`). Gartenmöbel als Wandkörper: 43 auf Muthgasse E7/E9 (K1, Owner-Frage 3, Branch `selman/fix-k1-moebel-keine-wand` `558dee3`). | P1 | Selman |
| D-07 | Fern-Körper-Filter | `wandkoerper.py:_ohne_fernkoerper:185` (nur ohne Wand-Layer, Median ± 500 m) | `test_wandkoerper.py::test_ohne_wandlayer_fernkoerper_fallen_weg` | Pläne **mit** Wand-Layer ungefiltert, Räume nirgends nach Planbereich gefiltert (`raumlayer.raeume_aus_layer:98` ohne Filter). S3c, Owner-Entscheid 2026-09-26 (Fremdcluster > 100 m ohne Wandkörper verwerfen, mit Warnung): Rennweg EG 11 Räume / 15 Durchgänge im Cluster 1 365,8 m entfernt, erwartete Wirkung Platzierung 21 → 17; Muthgasse E2 Cluster 400,5 m **mit** 56 Wandkörpern → melden. ponytail-Grenze: mehrere Geschosse in einem Modelspace (:192-193). | P1 | Selman (Slice S3c, nach dem Merge) |
| D-08 | Doppellinien-Fallback | `wandkoerper.py:_doppellinien:223` (nur bei < 5 Hatch-Körpern, :178-179) | `test_wandkoerper.py::test_doppellinien_fallback` | O(n²)-Paarvergleich ohne Spatial-Index (ponytail :226); Laufzeit auf großen Linienplänen nicht gemessen. | P2 | Selman |
| D-09 | OCS gespiegelter Blöcke | ohne OCS: `tueren.py:111/232/319` (`e.dxf.center`), `dxf_load._wand_punkte:66` | — | Mollgasse: 10 von 43 (EG) bzw. 32 von 63 (1OG) Kaskaden-Bögen landen gespiegelt außerhalb, alle aus Fenster-/Duschblöcken; reine OCS-Umrechnung kostet 5 Räume Notlicht. Owner-Frage offen (`docs/OFFENE_FRAGEN.md` § OCS). Gespiegelte Polylinien als Wandpunkte nicht gemessen. | P2 | Selman (Owner-Frage) |
| D-10 | Eingangsqualität | — | — | Am Rain UG ist als leerer Architekturplan abgelegt, trägt aber E-Planung (45 `SIMA_ET_SIBEL_Sicherheitsleuchte`, `docs/INTEGRATION_2026-09-30.md:234-235`). Die Pipeline zieht Bestands-Leuchten selbst aus der Unterlage (`pipeline.py:227-230`, `bestand_leuchten.extrahiere_fuer`) — Wirkung auf Am Rain UG nicht gemessen. | P2 | Owner / gemeinsam |
| D-11 | DWG-Eingang | `hauptengine/dwg_input.py:stelle_dxf_bereit` (raise `OdaKonverterFehlt` :93) | `tests/hauptengine/test_dwg_input.py` ×2 **skipped** (ODA File Converter fehlt) | DWG-Pfad lokal nie gelaufen. | P2 | gemeinsam |

---

## 2. Stufe Raumerkennung

| Nr. | Baustein | gebaut (Datei:Funktion:Zeile) | belegt durch | fehlt / Lücke | Prio | Lane |
|---|---|---|---|---|---|---|
| R-01 | Stempel finden und zuordnen | `stempel_anker.py:finde_stempel:242`, `ordne_zu:274`; `kaskade.py:_ein_polygon_ein_stempel:72` | `test_stempel_anker.py`; `test_kaskade.py` (Rennweg/Barawitzka/Mollgasse) | Stempel ohne Polygon bleiben ohne Raum: Mollgasse 1KG 22, 2KG 48 — **unbelegt (nur VERLAUF)**, im Basislauf nicht gezählt (Stempel-Zuordnung liegt nicht im Modell). Nicht zugeordneter Stempel „BAD 4,71 m²" Mollgasse 2.OG/3.OG, Raum erst aus der R-Stufe (`docs/SLICES_K1_K4.md` K3 Frage 3). Namenswahl „oberster statt nächster Text" (`stempel_anker.py:218/:230-231`, `docs/COORDINATION.md` Log 2026-09-29). | P1 | Selman (S-KG) |
| R-02 | L-Stufe (Raum-Layer) | `raumlayer.py:raeume_aus_layer:98` | `test_raumlayer.py` | kein Planbereichs-Filter → Fremdcluster (D-07). | P1 | Selman (S3c) |
| R-03 | H-Stufe (Raum-Hatches) | `raumlayer.py:raeume_aus_hatch:206`, IoU-Dedup `kaskade.py:104-109` | `test_raumlayer_hatch.py` | — | — | Selman |
| R-04 | F-Stufe (Stempel-Flutung) | `stempel_flutung.py:flute_stempel:227`, Reißleine `:246-257` | `test_stempel_flutung.py` | Reißleine liefert `[]` mit `RuntimeWarning` — alle Flut-Räume weg, im Bericht nicht sichtbar. | P2 | Selman |
| R-05 | R-Stufe (stempellose Restflächen) | `rest_komponenten.py:komponenten_ohne_stempel:228`, `_typisiere:200` | `test_rest_komponenten.py` (22 Tests, u. a. K2 und S3b) | (a) **keine Raster-Reißleine** (`:248-255`, anders als R-04); ein `MemoryError` wird in `kaskade.py:177-181` gefangen → nur `print`, R-Stufe leer, stempellose Stiegenhauskerne/Gänge fehlen still. (b) Sucht nur in der **größten** Komponente der Außenkontur (`aussenkontur:278-289`, `d_mm=1000` :245; Modul-Doc :20-21) — freie Flächen außerhalb werden kein Raum (Pflicht-Eintrag „freie Flächen"). Ob ein Mehr-Trakt-Plan des Korpus (Barawitzka 2 Trakte) dadurch Räume verliert: nicht gemessen. | P1 | Selman |
| R-06 | Bereinigung (Überlappung) | `bereinigung.py:bereinige_kaskade:505`; im Fehlerschutz `kaskade.py:191-195` | `test_bereinigung.py` | Provider-eigene Räume nach der Kaskade (`typisiere_geometrisch`, `finde_lifte`, Liftschacht-Reste) sieht die Bereinigung nicht (`plan_pruefen.py:1314-1319`) → Rest-Überlappung im Modell, Zahlen siehe Basislauf § 7. Fehler der Bereinigung nur `print`. | P2 | Selman |
| R-07 | Kürzel-Auflösung | `kuerzel_entscheid.py:loese_kuerzel`, Aufruf `kaskade.py:168-175` (Fehler nur `print`) | `test_kuerzel_entscheid.py` | Vokabular `Schl.`, `SR`, `Aufzug`, `Schrankr.`, Geschäftslokal, Wohnkche, Wohnbereich, TV Raum, Personalräume liegt bei Enis — **nicht anfassen** (Owner-Regel). | P2 | Enis |
| R-08 | Raumtyp aus Stempel/Layer | `raumtyp.py:raumtyp_flags:162`, `_port/models/room.py:classify_room` | `test_raumtyp.py`; `tests/contract/test_lb_raumtyp_naht.py`, `test_vokabular_doku.py` | Typlose Räume behalten Notlicht (fail-safe), aber die Leuchten-Art ist nicht ableitbar (`pipeline.py:77-85` warnt). WOHNKÜCHE, KELLERABTEIL, „Dachterrasse" nicht im Kanon (`docs/OFFENE_FRAGEN.md` § WOHNKÜCHE, § S-KG, § Rennweg DD). Zahlen je Plan: Basislauf § 7. | P1 | Enis (Kanon), Selman (Tokens) |
| R-09 | Geometrische Typisierung (Stiegenhaus, Gang) | `geometrie_typ.py:typisiere_geometrisch:206`, `stiege_rechtecke:54`; R-Stufe `_STIEGE_RX` `rest_komponenten.py:59` | `test_geometrie_typ.py`; `test_soll_mollgasse.py::test_zwei_stiegenhaus_raeume` | Am Rain OG4: 0 Stiegenhäuser, obwohl der Plan die Layer `Treppe` und `Aufzug` trägt (`docs/INTEGRATION_2026-09-30.md:197`; Basislauf bestätigt 0). Gemessen: Treppe und Lift sind lose Geometrie (`Treppe` 142 LINE, 2 LWPOLYLINE, 3 CIRCLE, 4 MTEXT; `Aufzug` 159 LINE, 3 ARC, 4 MTEXT), kein INSERT mit Treppen-/Liftnamen, ein Text „STGH". Beide Stiegenhaus-Quellen lesen nur **Blocknamen** (`geometrie_typ._STAIR_BLOCK:31`, `rest_komponenten._STIEGE_RX:59`) → wahrscheinliche Ursache, keine Regel gebaut. Folge F-07 (0 Ausgänge). | P0 | Selman |
| R-10 | Lift und Liftschacht | `lift_erkennung.py:finde_lifte:168`, `liftschacht_reste:236`; Anker-Filter `provider.py:295-299` | `test_lift_erkennung.py`; Gate (11) (`tests/gate/gate_dg1.py`) | Rennweg OG2/OG3: Schacht mit der Stiegenhaus-Restfläche verschmolzen (Kabinenanteil 0,082/0,204), nur Warnung (K2 Frage 6). Muthgasse E8/E9 `lift_1` deckt eine Nasszelle (K3 Frage 6). | P1 | Selman |
| R-11 | Schacht nur mit Beleg, sonst NISCHE (K2) | `rest_komponenten.py:_typisiere:200-225`, `_hat_beleg:192` | `test_rest_komponenten.py::test_k2_*` (7), `tests/naht/test_k2_schacht_beleg.py`, `tests/gate/test_gate_m3_nische.py` | U-förmige Schachtmauer nicht gebaut (ponytail :82-84); STO-Lesart; Nische ↔ Nachbarraum (F5) offen (`docs/SLICES_K1_K4.md` K2 Fragen 3, 4, 7). | P2 | Selman (Owner-Fragen) |
| R-12 | Sanitär → BAD/WC (K3) | `sanitaer.py:kandidaten:108`, `typisiere_sanitaer:124`; Probe `provider.py:231-239` | `test_sanitaer.py`; `tests/naht/test_k3_sanitaer_bad.py` | Probe ist eine einmalige Rückkante gegen Board 7 (Frage 9, offen); Barawitzka-Erscheinungsbild nicht gebaut; verschachtelte Blöcke nicht gelesen (K3 Fragen 2, 8). `sanitaer_befund` nicht im Bericht (O-04). | P2 | Selman (Owner-Fragen) |
| R-13 | Geschoss mehrstufig | `geschoss.py:geschoss_befund:252`, `_NICHT_PLAN_RE:199` | `test_geschoss_befund.py` (29 Tests, u. a. `::test_dachdraufsicht_ist_kein_geschoss`, `::test_fail_closed_*`) | — (DD bleibt UNBEKANNT, gewollt) | — | Selman |
| R-14 | Außenanalyse, Innen-Zonen | `aussenbereich.py:erkenne_aussenbereiche:340`, `waehle_innen_zonen:307` | `test_aussenbereich.py`; `test_soll_mollgasse.py::test_soll_hofausgaenge_cluster_a_und_b` | Laubengänge ohne lichtes Polygon (bewusste Grenze, `docs/OFFENE_FRAGEN.md` § Laubengänge); Mollgasse EG `raum_51`/`raum_55` siehe F-13. | P2 | Selman |
| R-15 | Wohnungen (`wohnung_id` nur aus rohen Türen) | `wohnungen.py:bilde_wohnungen:153` | `test_wohnungen.py`; Gate (3) M4, (5) | **Gate (3):** `M4.einraum` DG2 0 → 1 (`raum_5` bildet Einraum `top_2`), hängt an Board 3 (Blatt-Semantik, Enis) — einziger Gate-Verstoß, Merge-Blocker (`docs/INTEGRATION_2026-09-30.md:92-95`). | P1 | Enis (Board 3), Selman |
| R-16 | Nutzungsklasse, Klassifikation, Flags | `wohnungsklasse.py:klassifiziere:384`, `bestaetigt_privat:406`, `klasse_aus_umriss:818` (K4), `setze_wohnungsflags:928`; `nutzungsklasse.py:nutzungsklasse_fuer:59` | `test_wohnungsklasse.py`, `test_k4_klasse_umriss.py`, `tests/naht/test_k4_klasse_gang_vorraum.py`, `tests/naht/test_s7_wohnungsklasse.py`; Gate (5), (6), (9) | **S4c-Pins rot** (Pflicht-Eintrag § 6.1). 11 unbestimmte GANG/VORRAUM offen mit Grund, Flags 11 (1 R1-Flur, 6 G4, 4 G3; `docs/SLICES_K1_K4.md:1370-1377`). K4-Fragen 2–6 offen (`:1405-1407`). Gate (9) nicht verdrahtet: Skript `mollgasse_gt_vergleich.py`, Fixtures `tests/fixtures/mollgasse_gt/` und `knowledge/notbeleuchtung/` fehlen im Baum (`tests/gate/gate_regel.py:64`, `ls` geprüft). | P1 | Selman |
| R-17 | Freie Flächen (K1-Diagnose) | — (R-Stufe R-05 b) | — | Pflicht-Eintrag § 6.5. | P1 | Selman (Owner-Frage) |

---

## 3. Stufe Ausgänge und Fluchtwege

| Nr. | Baustein | gebaut (Datei:Funktion:Zeile) | belegt durch | fehlt / Lücke | Prio | Lane |
|---|---|---|---|---|---|---|
| F-01 | Türblöcke | `tueren.py:tueren_aus_dxf:117`, `_ist_tuer_block:50`, `_DOOR_HINT:35` | `test_tueren.py`; `tests/naht/test_soll_rennweg_og1_tueren.py`; **rot** `test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell` (30 von 72 gegen Band ≥ 40); xfail `::test_soll_jeder_plan_tuerblock_ist_tuer` | S4f: nur deutsche Wortstämme, `DOOR`/`OPENING` fehlen → ArchiCAD `Rectangular Door Opening` (Rennweg OG1, Kandidat Balkontür T08) weder Tür noch verworfen (`docs/OFFENE_FRAGEN.md` § S4f). Muthgasse-Türblöcke = S5b-Rest. | P1 | Selman |
| F-02 | Türöffnungen (Bögen, Blockgeometrie) | `tueren.py:tuer_oeffnungen:266`, `im_planbereich:540` | `test_wandkoerper.py::test_*_tueroeffnungen`; `test_tueren.py` | OCS siehe D-09. | P2 | Selman |
| F-03 | Zusatz-Türquellen | `tueren.py:aussentor_tueren:342`, `verschmelze_doppelfluegel:416`, `text_tueren:510` | `test_tuerquellen.py`; `test_provider.py::test_doppelfluegel_verschmilzt_aussentor_tueren` | Türen mit `von_raum == nach_raum` auf 11 von 13 Plänen (§ 7; Am Rain OG1 40, EG 35); Gate (4) prüft nur Rennweg OG1. **Ausgänge an solchen Türen:** Barawitzka EG — der **einzige** `final_exit` `exit_tuer_31` hängt an `tuer_31` `KEIN_RAUM`\|`KEIN_RAUM` (`hauseingang` über Text „Eingang"); `stair_exit` an einer Tür innerhalb desselben STIEGENHAUS: Mollgasse EG `exit_tuer_68` (`raum_51`, vgl. `docs/COORDINATION.md` Log 2026-09-30 Punkt 5), Am Rain UG `exit_tuer_186` (`raum_6`), OG3 `exit_tuer_29` (`raum_41`). | P1 | Selman |
| F-04 | Türzuordnung, Durchgänge | `tuer_zuordnung.py:ordne_tueren:183`, `andere_bogenrichtung:214` (S4c A), `durchgaenge_ohne_tuerblatt:343`, `aussen_durchgaenge:456` | `test_tuer_zuordnung.py`; Gate (4), (7), (8), (10) | `seite_fehlt` (Seite `KEIN_RAUM`) je Plan: Basislauf § 7 — Warnung nur am Provider, nicht im Bericht (O-04). Barawitzka `tuer_5`/`tuer_33` `KEIN_RAUM`\|`KEIN_RAUM`, `tuer_22`/`tuer_25` falsches Raumpaar (`docs/GATE_TUERSTAPEL.md` § 10g). Durchgänge ohne Türblatt übererkennen auf lückigen Wandkörpern (§ Fachteil 1). | P1 | Selman |
| F-05 | Rohe Türrollen | `tuer_typisierung.py:typisiere_tueren:104` | `test_tuer_typisierung.py`; xfail `::test_soll_90_prozent_tueren_typisiert` (Barawitzka, Mollgasse, Muthgasse, Rennweg EG) | Quote je Plan: Basislauf § 7. Türen ohne Rolle erzeugen weder Ausgang noch Fluchtweg-Start. | P1 | Selman |
| F-06 | Korrigierte Türrollen (Einbahn Board 7) | `wohnungsklasse.py:korrigierte_rollen:698`; Leser nur `fluchtweg.py:329`, `plan_pruefen.py:1281` | `test_wohnungsklasse.py::test_e7_*` (5); `tests/naht/test_s7_wohnungsklasse.py::test_korrigierte_rollen_sind_eine_funktion_von_klasse_und_roher_rolle` | Pflicht-Eintrag § 6.4. | P1 | Selman; Naht Leonis/Contract |
| F-07 | Geschossausgänge aus Türen | `ausgaenge.py:leite_ausgaenge:62`, S5c F2 `:50-59`/`:91-92`, `ohne_unzulaessige_final_exits:116` | `test_ausgaenge.py` (5); `test_geschoss_befund.py::test_fail_closed_*`; Gate (11) | **Am Rain OG4: 0 Ausgänge** (Pflicht-Eintrag § 6.2). Rennweg DD: 0 Ausgänge (Owner-Frage: Dachdraufsicht aus der Bewertung nehmen oder Regel „Freifläche am Stiegenhaus im OG", `docs/OFFENE_FRAGEN.md` § Rennweg DD). Rennweg UG: kein `final_exit`, nur 2 `stair_exit` (`docs/COORDINATION.md` Log 2026-09-30 Punkt 5). Veraltete Zeilenangabe `provider.py:102` in `ausgaenge.py:122` und `tuer_typisierung.py:154` (heute `:175`). | P0 (OG4) · P1 (DD, UG) · P2 (Doku) | Selman |
| F-08 | `final_exit` aus dem Footprint | `footprint.py:hauptausgaenge:123-135`, Aufruf `provider.py:175`, Zusammenlegung `:247-253` | `test_footprint.py::test_mollgasse_leer_hauptausgaenge` (sichert 1–6 `final_exit` aus dem Footprint); `test_soll_mollgasse.py::test_soll_hofausgaenge_cluster_a_und_b` | Pflicht-Eintrag § 6.3 (S4g). **→ 2b (§ 13): offen, STOPP** — ohne die Footprint-Ausgänge fallen auf Mollgasse EG 10 von 14 GRAPH-Wegen weg und Cluster A wird rot; Naht als strict-xfail `test_s4g_ausgang_tuerbezug.py::test_soll_mollgasse_eg_kein_ausgang_ohne_tuerbezug`. | P1 | Selman |
| F-09 | Fluchtweg-Segmente | `fluchtweg.py:fluchtwege:215` (GRAPH), `explizite_linien:88`/`linien_segmente:110` (LINIE), FALLBACK; `zirkulation.py:zirkulation_aus_dxf:61` | `test_fluchtweg.py`; `test_zirkulation.py::test_synth_fluchtweg` (`::test_mollgasse_fluchtweg` skipped); Gate (6) | Pläne nur mit FALLBACK-Segmenten (`richtung_unbekannt`), „kein final_exit erreichbar"-Warnungen: Zahlen Basislauf § 7. | P1 | Selman |
| F-10 | Durchleitung durch private Räume | `wohnungsklasse.py:durchleitung_raeume:921`, `fluchtweg.py:382-399` | `test_wohnungsklasse.py::test_durchleitung_zerreisst_den_weg_nicht`, `::test_durchleitung_wird_als_warnung_ausgewiesen`, `::test_durchleitung_fuehrt_nicht_durch_die_wand` | Pflicht-Eintrag § 6.6. | P2 | Contract (3 Owner) |
| F-11 | Kreuzcheck Linien ↔ `final_exit` | `kreuzcheck.py:kreuzcheck:57`, Aufruf `provider.py:321-324` | `test_kreuzcheck.py`; `test_soll_mollgasse.py::test_kreuzcheck_findet_endpunkte_an_der_aussenkante`; xfail `::test_soll_jeder_endpunkt_an_der_kante_hat_final_exit`, `::test_soll_final_exit_anzahl_gleich_endpunkte_an_der_kante` | Soll (jeder Kanten-Endpunkt hat einen `final_exit`) nicht erreicht. | P2 | Selman |
| F-12 | Stiegenhaus-Modell, Anker | `stiegenhaus.py:baue_stiegenhaus_modell:263`, `gang_anker.py:anker_fuer_gang:102`, `wohnungsklasse.py:anker_aus_privat_ziehen:958` | `test_stiegenhaus.py`, `test_gang_anker.py`; Gate (6); `test_soll_mollgasse.py::test_keine_anker_in_liftpolygonen` | Laufrichtung ohne Nummern/Gehlinie bleibt `unbekannt`; AUFZUGSVORPLATZ nicht automatisch (§ Fachteil 2). 18 Anker in `WOHNUNG_PRIVAT` sind eigene Anker K4-privater Gänge, nach Grundsatz (a) gewollt (`docs/SLICES_K1_K4.md:1362-1366`). | P2 | Selman |
| F-13 | Außenöffnungen Mollgasse EG | `tuer_zuordnung.py:aussen_durchgaenge:456` | — | `raum_55`: Hauseingang `aussenoeffnung_8` ist ein Streifen zwischen zwei Wandkörpern; `raum_51` (Außenanlage 122,43 m²) braucht ggf. eigenen Filter (`docs/OFFENE_FRAGEN.md` § Außenöffnungen). **Befund 2b (§ 13):** `raum_51` fasst Stiegenhaus und Hof, die Hof-Türen `tuer_52`/`tuer_68` bekommen keine `AUSSEN`-Seite — blockiert S4g a (Cluster A). | P1 | Selman |
| F-14 | Balkontür kein Ausgang (Leonis' S4d) | `tuer_typisierung.py:179-189`, Text dreht nicht zurück `:221-227` | `test_tuer_typisierung.py`, `test_ausgang_freiflaeche.py`; xfail `::test_soll_sentinel_aussen_ist_entscheidbar` | EG-Fenstertür AUSSEN × WOHNUNG_PRIVAT immer `balkontuer` (Norm-Frage an Enis, § Fachteil 1). **→ 2b (§ 13):** `leite_ausgaenge` macht keine `balkontuer` mehr zum `final_exit`, auch mit gesetztem `ist_notausgang` (`ausgaenge.py:83-89`). | P2 | Enis (Norm) |

---

## 4. Stufe Notleuchten-Platzierung (Leonis-Lane — nur gemeldet, nichts geändert)

| Nr. | Baustein | gebaut (Datei:Funktion:Zeile) | belegt durch | fehlt / Lücke | Prio | Lane |
|---|---|---|---|---|---|---|
| N-01 | Platzierer über die Registry | `platzierung/platzierer.py:place:261`; `hauptengine/registry.py` | `tests/platzierung/` (30 Dateien), `tests/e2e/` | — | — | Leonis |
| N-02 | Kein Flächenlicht in `WOHNUNG_PRIVAT` ohne Flags | `platzierung/flaechen_strategy.py:162-166` | `tests/platzierung/test_flaechen_strategy.py` | `deckung.verdichte_fluchtweg` wählt Korridore nur über `raum_typ` (`deckung.py:235`), liest weder Klasse noch Flags (Board 1) → Leuchten in `WOHNUNG_PRIVAT` (Pflicht-Eintrag § 6.8, Board-1-Tests § 6.9). | P1 | Leonis (Board 1) |
| N-03 | Leuchten in `KEIN_RAUM` (LIFT, SCHACHT) | `platzierung/` liest `KEIN_RAUM` nirgends (`grep` 0 Treffer); LIFT/SCHACHT nur in `fachpraxis._TUERLEUCHTE_KEIN_COMMUNAL:73-76`; `verbotszonen_nachpass.entferne_aus_verbotszonen:43` | `test_soll_mollgasse.py::test_soll_keine_leuchten_in_liftpolygonen` (nur Mollgasse EG) | Pflicht-Eintrag § 6.8. | P0 | Leonis |
| N-04 | Türrolle an der Naht | `fachpraxis.py:400/461/524` lesen `tuer_detail` (rohe Rolle) | — | Die korrigierte Rolle ist nicht im Modell (F-06). | P1 | Leonis / Contract |
| N-05 | Aufheller durch die Wand | `fachpraxis.aufheller_je_rz` | — | Rennweg DG1 `raum_3`: SL springt durch die Wand; Board-1-Erweiterung vorbereitet, nicht gestellt (`docs/GATE_TUERSTAPEL.md:2307-2312`, `:2372`). | P1 | Leonis |
| N-06 | Bounds-Leser | `aussen_strategy.py:73` | — | Extents-Ausreißer (D-05). | P2 | Leonis |
| N-07 | Leuchten außerhalb jedes Raumpolygons | — | — | Basislauf (§ 7): Muthgasse E2 **57 von 139** Leuchten in keinem Raumpolygon, Am Rain UG 13, OG2 12. Früher als „erwartbar" eingeordnet (Außenleuchten an `final_exit`, `docs/OFFENE_FRAGEN.md` § Fachteil 3); ob das bei 57 noch gilt, ist nicht untersucht — Kandidaten sind Lücken zwischen Raumpolygonen (Raumerkennung) oder Platzierung außerhalb (Leonis). | P1 | Selman / Leonis |

---

## 5. Stufe Planausgabe

| Nr. | Baustein | gebaut (Datei:Funktion:Zeile) | belegt durch | fehlt / Lücke | Prio | Lane |
|---|---|---|---|---|---|---|
| O-01 | Render DXF-Blatt | `hauptengine/render/dxf_renderer.py:render_dxf:1327`, Maßstab-Fallback `pipeline.py:259-267` | `tests/render/test_render_dxf.py`, `test_layout_vorlage.py`; `tests/e2e/` | `VorlageEinheitenFehler` (`dxf_renderer.py:1367`) fängt die Pipeline nicht → Abbruch bei falscher Vorlage (API 422); kein Test (`grep`: 0). | P2 | gemeinsam |
| O-02 | Blatt-Extents | `dxf_renderer.py:_geschoss_extents:338` | kein direkter Test (`grep` in `tests/`: 0) | schützt nur das Blatt, nicht die übrigen `bounds_mm`-Leser (D-05). | P2 | gemeinsam |
| O-03 | PDF A0 1:50 | `pdf_export.py:dxf_zu_pdf:57` (ezdxf-Frontend + matplotlib, 300 dpi) | `tests/render/test_pdf_export.py` | RAM auf Am Rain nicht gemessen — derselbe Frontend-Weg wie `_figur` (O-05). | P1 | gemeinsam |
| O-04 | Warnungen im Prüfbericht | `plan_pruefen.py:_geschoss_md:1136`, `_kreuzcheck_md:1153` | — | `wand_warnungen` (`keine_wand_entities`), `tuer_warnungen` (`seite_fehlt`) und `sanitaer_befund` erscheinen **nicht** in `bericht.md` (0 Treffer). Die Owner-Regel P0 („es bleibt eine Warnung") ist in der Prüfstrecke unsichtbar. **→ 2a (§ 12): `wand_warnungen` stehen jetzt im Abschnitt „Warnungen"**; `tuer_warnungen` und `sanitaer_befund` weiter offen. | P1 | Selman |
| O-05 | Plan-Render der Prüfstrecke (RAM) | `plan_pruefen.py:_figur:137`, 8 Aufrufstellen (:419/:491/:667/:740/:854/:1556/:1565/:1589) | — | Pflicht-Eintrag § 6.7. | P0 | Selman |
| O-06 | Prüfstrecken-Schleife | `plan_pruefen.py:main:1984-2034` | — | Kein Fehler-Fang je Plan (:1990-1992): ein Fehler bricht alle folgenden Pläne ab, und `VERLAUF.md` wird nicht geschrieben (`_verlauf_schreiben` erst nach der Schleife, :2030-2032). | P1 | Selman |
| O-07 | Maßstab im Bericht | — | — | Faktor und Beleg nicht ausgewiesen (D-04). | P2 | Selman |
| O-08 | Lux-Nachweis | `render/lux_nachweis_bericht.py:schreibe_bericht:134` (additiv, Fehler gefangen `pipeline.py:268-281`) | `tests/hauptengine/test_fix_wissensabgleich.py`, `tests/e2e/test_wohnbau_durchstich.py` | Bounds-Leser `:165` (D-05). | P2 | gemeinsam |

---

## 6. Pflicht-Einträge

### 6.1 S4c — offen (Owner 2026-09-30), zwei rote Pins

- **Stand:** S4c Fassung A (`xsehne3`) gebaut (`209755c`), Gate (10) grün (`docs/GATE_TUERSTAPEL.md` § 10g).
- **Rot, bleiben rot:** `tests/naht/test_s7_wohnungsklasse.py::test_bara_raum_19_behaelt_klasse_und_zirkulation`
  (`:924`, Wohnung von `raum_19` hat zusätzlich `raum_29` WC) und
  `::test_bara_raum_30_wird_nicht_von_der_auswertungsreihenfolge_entschieden` (`:1034`, zusätzliches Segment
  `seg_graph_tuer_27` ab WC `raum_29`). Beide scheitern auf `e979957` allein mit derselben Ausgabe — kein
  Merge-Fehler (`docs/INTEGRATION_2026-09-30.md:84-86`).
- **Ursache:** Fassung A korrigiert `tuer_17`/`_23`/`_27` planwidrig auf `wohnungseingang` (Vorraum-Fehlklasse
  `raum_12`/`30`/`31`, sichere Richtung, kein Notlicht-Verlust).
- **Offen (Owner):** Pins auf Fassung A nachziehen oder erst mit dem Slice, der die Vorraum-Fehlklasse behebt;
  § 10f Fragen 2–4. **Owner-Anweisung 2026-09-30: S4c nicht anfassen, Pins bleiben rot, Abweichung hier offen
  geführt.** Prio P1 · Lane Selman.

### 6.2 Am Rain

- **P0 behoben (`ed292e1`):** kein `ValueError` mehr bei fehlenden Wand-Entities; Warnung
  `keine_wand_entities` in `provider.wand_warnungen` (`provider.py:130`, `:145-149`), kein Contract-Feld;
  Fern-Filter 500 m (`wandkoerper._ohne_fernkoerper:185`); Tests `test_provider.py::test_ohne_wandlayer_*`,
  `::test_naht_am_rain_og4_parse_ohne_abbruch`, `test_wandkoerper.py::test_ohne_wandlayer_*`.
- **Offen:**
  - **OG4 0 Ausgänge, 0 Stiegenhäuser** (R-09/F-07) — ein Geschoss ohne Ausgang ist für die Notbeleuchtung
    nicht verwertbar (Owner-Satz zu Rennweg DD, `docs/OFFENE_FRAGEN.md` § Rennweg DD). **P0**. Wahrscheinliche
    Ursache gemessen: Treppe/Lift nur als lose Linien, Stiegenhaus-Erkennung liest nur Blocknamen (R-09).
  - Warnung nicht im Bericht (O-04, P1); im Basislauf auf allen 6 Geschossen gesetzt. Kalibrierung ohne
    Wand-Layer über `$INSUNITS` = 4 → Faktor 1; die Türprobe sagt auf OG4/OG3/EG 10 (D-04, P1).
  - `rest_komponenten` ohne Raster-Reißleine (R-05 a, P1).
  - **RAM/Render** (§ 6.7, P0) und Parse-Last: EG 6,30 GB / 485,8 s (`docs/INTEGRATION_2026-09-30.md:190`),
    Basislauf EG 6,30 GB / 476,6 s.
  - **OG1–OG3 nur teilweise gemessen:** `docs/INTEGRATION_2026-09-30.md:201` („nicht gemessen"); Prüfstrecke
    danach nur ohne Plan-Render. Der Basislauf § 7 misst jetzt Parse und Platzierung (OG1 5,31 GB / 257 s,
    OG2 4,54 GB / 220 s, OG3 2,12 GB / 100 s; Ausgänge 4 / 2 / 3 `stair_exit`), **nicht** den Render und
    nicht gegen eine Referenz — fachlich abgenommen ist keines der sechs Geschosse. UG: nur FALLBACK-Segmente
    (24), 13 von 295 Türen mit Rolle.
  - Owner-Fragen: `Wand brüstungshoch` (D-03), `_NEGATIV_LAYER` ohne „Moeblierung" (D-06), UG mit E-Planung
    (D-10). OG4-Bounds enden bei x 63,6 m (D-05).

### 6.3 S4g — Restlöcher der Balkontür-/Ausgangsregel (`docs/OFFENE_FRAGEN.md` § S4g)

- **a)** `footprint.hauptausgaenge` (`footprint.py:123-135`, Aufruf `provider.py:175`) erzeugt `final_exit` ohne
  Tür-, Raum- und Typbezug; Owner 2026-09-23: „Ein Ausgang ohne Türbezug ist kein Ausgang." Mollgasse EG
  `exit_1` … `exit_4` = 4 von 8 `final_exit` (`docs/INTEGRATION_2026-09-30.md:295`; Basislauf § 7). Zusätzlich
  am Code: das Zusammenlegen `provider.py:247-253` behält den Footprint-Ausgang und **verwirft** einen
  türgebundenen Ausgang gleichen Typs im Umkreis 1 500 mm — beim Entfernen der Footprint-Ausgänge sind diese
  Türen mitzuprüfen. `test_footprint.py::test_mollgasse_leer_hauptausgaenge` sichert heute 1–6
  Footprint-Ausgänge.
- **b)** `ausgaenge.py:83-86` (`hauseingang`, `ist_notausgang` ins Freie, Tor mit Fluchtweg-Ende); ein Türtext
  dreht `balkontuer`/`garagentor` nicht zurück (`tuer_typisierung.py:221-227`, gelesen). Kette in S4g mitprüfen.
- **c)** EG-Ausnahme **bleibt**: Freiflächen-Regel nur `not eg` (`tuer_typisierung.py:179`). Messfall
  Mollgasse EG `exit_tuer_67` (Südgarten-Tür, früher `tuer_68`; rohe Rolle `None`, `final_exit` über
  `ist_notausgang`). Der bestehende Test `test_soll_mollgasse.py::test_soll_hofausgaenge_cluster_a_und_b`
  prüft nur „irgendein `final_exit` ≤ 1 500 mm an Cluster B"; im Basislauf erfüllt ihn `exit_tuer_67` (3 mm),
  die Footprint-Ausgänge `exit_1`…`exit_4` liegen 12,9–34,7 m entfernt.
  Vor dem Bau ist ein eigener Messfall auf die Tür anzulegen (Owner 2026-09-23).
- Prio **P1** (Owner-Satz, Notlicht-Wirkung nicht gemessen) · Lane Selman · Reihenfolge: nach dem Merge des
  Türstapels (Owner-Vermerk).
- **→ 2b (§ 13):** b und c erledigt, a offen (STOPP; Messung und Einzelbefund `exit_1` … `exit_4` dort).

### 6.4 Türrollen (roh vs. korrigiert)

- Das Modell trägt die **rohe** Rolle (`tuer_detail`, `wohnungsklasse.py:21`, `:698-705`). Korrigierte Rollen
  leben nur in `korrigierte_rollen`, gelesen von `fluchtweg.py:329` und `plan_pruefen.py:1281`.
- Leonis liest die rohe Rolle (`platzierung/fachpraxis.py:400`, `:461`, `:524`).
- K4-Nachzug: netto **270** korrigierte Rollen kippen gegen `f682c77` (Muthgasse 260, Mollgasse 10), in beide
  Richtungen (`docs/SLICES_K1_K4.md:1345`, `:1358`; die 277 ist überholt). K4-Frage 2 (Option W für K4-private
  Loch-Räume) offen.
- Planwidrige korrigierte Rolle nach S4c A: Barawitzka `tuer_17`/`_23`/`_27` → `wohnungseingang` (§ 6.1).
- K3-Probe als einmalige Rückkante gegen Board 7 (K3-Frage 9).
- Basislauf, Türen mit roh ≠ korrigiert: Muthgasse E2 22, Barawitzka 15, Am Rain OG1 11, OG3 6,
  EG 5, OG2 5, UG 3, OG4 1, Rennweg EG 4, OG3 4, Mollgasse EG 3, 1KG 0, 2KG 0.
- **Lücke:** braucht die Platzierung die korrigierte Rolle, ist das ein Contract-Antrag (3 Owner). Prio **P1** ·
  Lane Selman / Contract / Leonis.

### 6.5 Freie Flächen (K1-Diagnose)

- Rennweg DG1: stempelloses Feld **16,90 m²** links neben Bad 8,6 / WC 1,7 (Sofas, TV, Layer `New_065 Möbel
  Einrichtung`), Grenze zum Wohnzimmer 5,79 m nur zu 3 % wandbelegt, in keiner Zone.
- Die R-Stufe findet es nicht: `aussenkontur(…, d_mm=1000)` (`rest_komponenten.py:245`) deckt nur 73,5 von
  211,1 m² Deckenplatte `Slab_1`; gesucht wird nur in der größten Komponente (`wandkoerper.py:284-289`).
- Wohnzimmer 73,95 m² (Stempel 83,93); die 9,98 m² AR-Zone sind ein echter Raum hinter Wand + Tür `tuer_7`.
- Quelle: Bericht K1 auf Branch `selman/fix-k1-moebel-keine-wand` `558dee3` (`docs/SLICES_K1_K4.md` dort, Owner-
  Fragen 1–2), nicht auf diesem Branch. Kein Test.
- Prio **P1** (Owner-Frage; im Beispiel private Wohnfläche, kein Notlicht-Fehler belegt) · Lane Selman.

### 6.6 Durchleitung

- `FluchtwegSegment` hat kein Feld `durchleitung` (`hauptengine/contracts/raum_modell.py:184-196`, gelesen);
  Board-Antrag (`provider.py:104-107`, `docs/GATE_TUERSTAPEL.md:903-904`).
- Erkennbar nur als GRAPH-Direktlinie Tür → Tür durch einen `WOHNUNG_PRIVAT`-Raum mit Flags 00, nie
  `start_raum`/`ziel_raum` (`fluchtweg.py:20-27`, `:382-399`); Text `durchleitung: seg_graph_<tür> …` in
  `wohnungsklasse_warnungen` → `bericht.md`.
- Gemessen 0 Durchleitungen (`docs/COORDINATION.md` Log 2026-09-30 Punkt 6); Basislauf: 0 `durchleitung:`-Zeilen
  auf allen 13 Plänen.
- Prio **P2** (0 Fälle) · Lane Contract (3 Owner).

### 6.7 RAM

- **Parse:** Am Rain EG 6,30 GB / 485,8 s, UG 3,91 GB / 110,0 s, OG4 0,43 GB / 21,8 s
  (`docs/INTEGRATION_2026-09-30.md:186-190`); Basislauf gleich (EG 6,30 GB / 476,6 s, UG 3,91 / 120,7 s,
  OG4 0,43 / 22,1 s). **Neu gemessen: Muthgasse E2 Parse 644,4 s, Peak Working Set 11,29 GB** — die
  Arbeitsregel „Muthgasse höchstens 2 parallel (~5 GB)" trägt damit nicht; zwei parallele Muthgasse-Läufe
  bräuchten rund 22,6 GB.
- **Render Prüfstrecke:** `_figur` (`plan_pruefen.py:137`) rendert den ganzen Architektur-Raum über das
  ezdxf-Frontend, 8 Aufrufstellen je Plan, **kein Schalter** zum Abschalten (`grep environ/argv`: nur
  `PLAN_PRUEFEN_ERGEBNIS` :71 und die Dateiliste :1985). Dazu lädt die Prüfstrecke die DXF zweimal und rechnet
  die Kaskade zweimal (`:1544-1546` und `_fachteil3` → `bundle.raum.parse` `:1265`).
- Zahlen zum Render — OG4 Spitze 13,28 GB, UG Abbruch bei 14,3 GB Working Set, OG4 5,6 GB und 107 s je Bild —
  **unbelegt (nur VERLAUF)**; der Auftrag nennt OG4 13,3 GB. UG/EG/OG1–OG3 liefen nur ohne Render.
- PDF-Export der Pipeline nutzt denselben Frontend-Weg (O-03), auf Am Rain nicht gemessen.
- Prio **P0** (Prüfstrecke bricht an der RAM-Grenze ab) · Lane Selman (`plan_pruefen`), PDF gemeinsam.

### 6.8 Leuchten in `KEIN_RAUM` / `WOHNUNG_PRIVAT` (Leonis-Lane — gemeldet)

- Am Code: `platzierung/` liest `KEIN_RAUM` nicht (`grep` 0 Treffer). LIFT und SCHACHT sind `KEIN_RAUM`
  (`nutzungsklasse.py:45-46`, `lift_erkennung.py:187-222`). Ausgelassen wird nur `WOHNUNG_PRIVAT` ohne Flags im
  Flächenlicht (`flaechen_strategy.py:162-166`); `deckung.verdichte_fluchtweg` liest nur `raum_typ`.
- Basislauf (§ 7), Zählweise `plan_pruefen._leuchten_je_klasse`: **LIFT** Muthgasse E2 1, Mollgasse 2KG 1;
  **SCHACHT** Am Rain OG1 1; **`WOHNUNG_PRIVAT`** Muthgasse E2 62, Am Rain EG 3, OG2 3, OG3 3, UG 2, OG1 2,
  Mollgasse EG 2 — deckt sich mit VERLAUF. Einzige Abnahme dazu im Baum:
  `test_soll_mollgasse.py::test_soll_keine_leuchten_in_liftpolygonen` (nur Mollgasse EG).
- Prio: LIFT/SCHACHT **P0** (Verbotszone), `WOHNUNG_PRIVAT` **P1** (Grundsatz (a) „im Zweifel behalten"
  konkurriert: DG1 `raum_4` ist `WOHNUNG_PRIVAT` **mit** Flags 11). Nur melden, nichts in `platzierung/` ändern.

### 6.9 Board-1-Tests

- `tests/naht/test_s7_wohnungsklasse.py::test_keine_leuchten_in_wohnung_privat` (`:1073`), rot für OG1, OG2,
  DG1 (OG3 grün); gemessen auf `bdbbd00`: OG1 2, OG2 2, DG1 2 (`raum_4:rz`, `raum_3`)
  (`docs/SLICES_K1_K4.md:1401-1404`, K4-Nachzug).
- Ursache: `platzierung/deckung.py::verdichte_fluchtweg` wählt Korridore über `raum_typ`, ohne Klasse und Flags
  (Docstring des Tests `:1079-1085`). Datei gehört Leonis; nicht grün gebogen, nicht als xfail versteckt.
- Prio **P1** · Lane Leonis (Board 1).

### 6.10 Mollgasse-KG (S-KG)

- Folgeauftrag nach dem Stapel-Merge (`docs/GATE_TUERSTAPEL.md` § 5a, `docs/OFFENE_FRAGEN.md` § S-KG): KELLERABTEIL
  (Stempel „ER") nicht im Kanon (`raumtyp.py` bildet „kellerabteil" auf `KELLER` ab), Garage-Zirkulation (NB-R17),
  Gebäudehälften über Graph-Komponenten (kein Contract-Feld), Treppenläufe 1KG 2×4, 2KG 4/0/3.
- Abnahme `mollgasse_gt_vergleich.py 1KG 2KG` nicht ausführbar: Skript, `tests/fixtures/mollgasse_gt/` und
  `knowledge/notbeleuchtung/` fehlen im Baum (`ls` geprüft; liegen auf `leonis/demo-l-gebaeude` `8257ff9`).
  Im Baum liegen `tests/fixtures/mollgasse_ug_referenz_1kg.json`/`_2kg.json` (NB-Referenz aus den GU-Plänen,
  `scripts/analyse/mollgasse_ug_nb.py`), von keinem Test gelesen.
- Basislauf 1KG / 2KG: 31 / 30 Räume, davon 24 / 19 ohne Typ; 0 / 1 Wohnung; 0/28 bzw. 2/46 Türen mit Rolle;
  1 `final_exit` bzw. 1 `stair_exit`; Segmente nur FALLBACK 4 bzw. FALLBACK 2 + GRAPH 1; 2KG 1 Leuchte im LIFT.
  VERLAUF-Zahlen „22/48 Stempel ohne Polygon" **unbelegt (nur VERLAUF)** — die Stempel-Zuordnung liegt nicht
  im Modell.
- Prio **P1** · Lane Selman (Enis für den Kanon, Leonis für das Material).

---

## 7. Basislauf `0434392` (13 Pläne der Prüfstrecke)

Je Plan allein, nacheinander, `0434392` (Arbeitsbaum `src/`, `scripts/`, `tests/` sauber; „dirty" im Runner-Kopf
nur wegen der unversionierten `LUECKEN.md`). Aufruf `ArchitekturRaumProvider().parse(dxf, "")`, dann
`build_default_bundle().platzierer.place(modell, norm, None)`; Peak = Peak Working Set des Prozesses (Parse +
Platzierung). „Räume" = Modell-Räume (inkl. der vom Provider nach der Kaskade angelegten), nicht die
Kaskaden-Zahl der Prüfstrecke. Faktor-Quelle aus einem eigenen `lade_dxf`-Lauf (`_calibrate_factor`-Zweig).
Runner, JSON und Auswertung liegen im Session-Scratch (`lk/_lauf.py`, `lk/base/*.json`, `lk/_auswertung.py`,
`lk/_faktor.py`), nicht im Repo.

| Plan | Geschoss | Räume | ohne Typ | Wohnungen | Türen mit Rolle / gesamt | Türen von = nach (davon `KEIN_RAUM`) | Ausgänge | Segmente | `seite_fehlt` | Fluchtweg-Warnungen | Leuchten rz / SL / AP | davon `WOHNUNG_PRIVAT` · LIFT · SCHACHT · kein Raum | Modell-Überlappung | Faktor (Quelle) | Parse s | Peak GB |
|---|---|--:|--:|--:|--:|--:|---|---|--:|--:|---|---|---|---|--:|--:|
| Barawitzka_EG | EG | 49 | 7 | 7 | 33 / 71 | 8 (8) | 1 final_exit | FALLBACK 1 GRAPH 7 | 24 | 11 | 6 / 5 / 0 | 0 · 0 · 0 · 5 | 4 / 7,13 m² | 1000 (spanne) | 10,8 | 0,24 |
| Mollgasse_EG | EG | 64 | 11 | 21 | 44 / 102 | 1 (0) | 8 final_exit + 1 stair_exit | FALLBACK 3 GRAPH 14 LINIE 103 | 21 | 8 | 24 / 27 / 0 | 2 · 0 · 0 · 9 | 0 / 0,00 m² | 1000 (spanne) | 30,4 | 0,73 |
| Mollgasse_1KG | KG | 31 | 24 | 0 | 0 / 28 | 0 (0) | 1 final_exit | FALLBACK 4 | 4 | 0 | 7 / 7 / 0 | 0 · 0 · 0 · 4 | 0 / 0,00 m² | 1000 (spanne) | 17,8 | 0,46 |
| Mollgasse_2KG | KG | 30 | 19 | 1 | 2 / 46 | 0 (0) | 1 stair_exit | FALLBACK 2 GRAPH 1 | 9 | 2 | 8 / 4 / 1 | 0 · 1 · 0 · 0 | 2 / 2,95 m² | 1000 (spanne) | 25,6 | 0,67 |
| Muthgasse_E2 | 2OG | 108 | 6 | 22 | 113 / 193 | 2 (2) | 1 stair_exit | FALLBACK 3 LINIE 139 | 78 | 0 | 86 / 53 / 0 | 62 · 1 · 0 · 57 | 10 / 15,43 m² | 10 (spanne+tuerbogen) | 644,4 | 11,29 |
| Rennweg_EG | EG | 24 | 7 | 2 | 20 / 40 | 4 (4) | 2 final_exit + 3 stair_exit | FALLBACK 2 GRAPH 5 | 11 | 8 | 9 / 8 / 0 | 0 · 0 · 0 · 3 | 2 / 1,74 m² | 1 (INSUNITS) | 2,1 | 0,15 |
| Rennweg_OG3 | 3OG | 17 | 0 | 2 | 17 / 18 | 1 (1) | 3 stair_exit | FALLBACK 1 GRAPH 5 | 2 | 0 | 5 / 2 / 0 | 0 · 0 · 0 · 1 | 0 / 0,00 m² | 1 (INSUNITS) | 2,1 | 0,15 |
| AmRain_UG | UG | 82 | 31 | 7 | 13 / 295 | 10 (7) | 2 final_exit + 4 stair_exit | FALLBACK 24 | 159 | 10 | 59 / 32 / 0 | 2 · 0 · 0 · 13 | 0 / 0,00 m² | 1 (INSUNITS) | 120,7 | 3,91 |
| AmRain_EG | EG | 136 | 24 | 50 | 78 / 317 | 35 (32) | 2 final_exit + 1 stair_exit | FALLBACK 6 GRAPH 1 | 186 | 13 | 27 / 13 / 0 | 3 · 0 · 0 · 9 | 0 / 0,00 m² | 1 (INSUNITS) | 476,6 | 6,30 |
| AmRain_OG1 | 1OG | 134 | 21 | 57 | 103 / 300 | 40 (38) | 4 stair_exit | FALLBACK 17 GRAPH 6 | 177 | 0 | 47 / 21 / 0 | 2 · 0 · 1 · 7 | 0 / 0,00 m² | 1 (INSUNITS) | 257,2 | 5,31 |
| AmRain_OG2 | 2OG | 102 | 12 | 43 | 117 / 264 | 11 (8) | 2 stair_exit | FALLBACK 15 GRAPH 9 | 119 | 0 | 52 / 23 / 0 | 3 · 0 · 0 · 12 | 0 / 0,00 m² | 1 (INSUNITS) | 220,3 | 4,54 |
| AmRain_OG3 | 3OG | 59 | 8 | 23 | 61 / 129 | 6 (3) | 3 stair_exit | FALLBACK 2 GRAPH 10 | 52 | 0 | 9 / 11 / 0 | 3 · 0 · 0 · 1 | 0 / 0,00 m² | 1 (INSUNITS) | 99,7 | 2,12 |
| AmRain_OG4 | 4OG | 27 | 3 | 11 | 22 / 58 | 4 (2) | **0** | FALLBACK 4 | 23 | 0 | 8 / 5 / 0 | 0 · 0 · 0 · 1 | 0 / 0,00 m² | 1 (INSUNITS) | 22,1 | 0,43 |

Befunde aus dem Basislauf (je mit Eintrag oben):

- `final_exit` ohne Tür: nur Mollgasse EG `exit_1` … `exit_4` (4 von 8) — § 6.3.
- Ausgänge an Türen `von_raum == nach_raum`: Barawitzka EG `exit_tuer_31` (einziger `final_exit`, `KEIN_RAUM`\|`KEIN_RAUM`),
  Mollgasse EG `exit_tuer_68`, Am Rain UG `exit_tuer_186`, OG3 `exit_tuer_29` (je `stair_exit` im selben STIEGENHAUS) — F-03.
- Am Rain OG4: 0 Ausgänge, 0 Stiegenhäuser, Ausgangs-Warnung „kein Geschossausgang ableitbar", Bounds bis x 63,6 m — R-09, F-07, D-05.
- Nur FALLBACK-Segmente (kein GRAPH, keine LINIE): Am Rain UG (24), OG4 (4), Mollgasse 1KG (4) — F-09.
- Faktor über `$INSUNITS`: 8 von 13; Türprobe widerspricht auf Rennweg EG, Am Rain OG4/OG3/EG — D-04.
- Bounds Muthgasse E2 503,8 × 275,9 m (Fremdcluster, S3c) — D-05, D-07.
- `keine_wand_entities`: auf allen 6 Am-Rain-Geschossen gesetzt, sonst 0; im Bericht nie sichtbar — O-04.
- Durchleitung: 0 auf 13 Plänen — § 6.6.
- Leuchten in LIFT/SCHACHT/`WOHNUNG_PRIVAT` — § 6.8; Leuchten in keinem Raumpolygon (Muthgasse 57) — N-07.
- Modell-Überlappung (Provider-Räume nach der Bereinigung): Muthgasse 10 / 15,43 m², Barawitzka 4 / 7,13 m²,
  Mollgasse 2KG 2 / 2,95 m², Rennweg EG 2 / 1,74 m² — R-06.
- RAM: Muthgasse E2 11,29 GB — § 6.7.

---

## 8. raise-Stellen im Lade-/Provider-Pfad

`grep -n "raise\b"` über alle 39 Module `src/notbeleuchtung/raumerkennung/*.py` (ohne `_port/`; die
benutzten Port-Helfer `_port/parsers/room_faces.py`, `_port/models/room.py` haben 0 Treffer): **3 Stellen**.
Kein `raise` in `kaskade.py`, `waende.py`, `raumlayer.py`, `stempel_anker.py`, `stempel_flutung.py`,
`rest_komponenten.py`, `tueren.py`, `tuer_zuordnung.py`, `tuer_typisierung.py`, `ausgaenge.py`,
`fluchtweg.py`, `geschoss.py`, `footprint.py` und den übrigen Modulen; kein `assert`.

| Nr. | Stelle | Bedingung | Aufrufer und Fang | Test | Befund | Prio |
|---|---|---|---|---|---|---|
| X-01 | `dxf_load.py:258` `bounds_mm` | keine Stützpunkte auf den erkannten Wand-Layern (`plan.wall_entities()` ohne LINE/LWPOLYLINE/POLYLINE/INSERT) | einziger Aufrufer `provider.py:133`, gefangen `except ValueError` `:134` → Bounds aus Wandkörpern bzw. allen Entities + Warnung `keine_wand_entities` | indirekt `test_provider.py::test_ohne_wandlayer_hatch_waende_raeume_statt_valueerror`, `::test_naht_am_rain_og4_parse_ohne_abbruch`; kein direkter Test | bricht nicht mehr ab | — |
| X-02 | `provider.py:141` `parse` | X-01 warf **und** keine Wandkörper **und** kein Stützpunkt (`entity_points` kennt nur LINE, LWPOLYLINE, POLYLINE, INSERT) | nicht gefangen → Abbruch (Pipeline/API 422) | — | gewollter Abbruch „DXF ohne Geometrie". Randfall: ein Plan nur aus ARC/CIRCLE/SPLINE/TEXT ohne Wandkörper bricht ebenfalls ab. Kein Test. **→ 2a erledigt (§ 12): kein `raise` mehr, Warnung `keine_geometrie`.** | P2 |
| X-03 | `wandkoerper.py:296` `bounds_aus_wandkoerpern` | leere Wandkörper-Liste | alle 5 Aufrufer prüfen vorher: `kaskade.py:111`, `provider.py:136-137`, `:172-174`, `rest_komponenten.py:240-241`, `stempel_flutung.py:239-240` | `test_wandkoerper.py::test_bounds_aus_wandkoerpern_leer` | im Parse nicht erreichbar | — |

**Abbruch ohne `raise`-Anweisung:** `dxf_load.py:234` `ezdxf.readfile` (Datei fehlt, defekt) — ungefangen (D-01).
**→ 2a (§ 12):** `readfile` gefangen → `DxfNichtLesbar`; dazu gefunden und behoben: `fluchtweg.py:84`
`doc.layers.get` warf `DXFTableEntryError` bei einem Layer ohne Tabelleneintrag.
**Geschluckte Fehler (nur `print`, kein Bericht):** `kaskade.py:174-175` (Kürzel), `:179-181` (R-Stufe → Räume
fehlen), `:194-195` (Bereinigung). `stempel_flutung.py:246-257` warnt statt zu werfen (R-04). Die übrigen
`except Exception` (21 Stellen) überspringen einzelne kaputte Blöcke/Hatches/Texte. Nicht vollständig geprüft:
implizite Ausnahmen (KeyError, StopIteration, GEOS) ohne `raise`-Anweisung.

**Außerhalb des Pfads (nur gelistet):** `hauptengine/dwg_input.py:93` `OdaKonverterFehlt`;
`hauptengine/registry.py:146`; `hauptengine/render/dxf_renderer.py:1290/1294/1299` `MassstabPasstNichtFehler`
(gefangen `pipeline.py:259`), `:1367` `VorlageEinheitenFehler` (nicht gefangen, O-01).

---

## 9. Aus `Projekte/_ergebnis/VERLAUF.md` — geprüft oder unbelegt

Geprüft wurde jede Aussage aus `VERLAUF.md`, die hier verwendet wird. „geprüft (Basislauf)" = gleiche Zahl im
eigenen Lauf § 7; „geprüft (Code)" = am Code nachgelesen; sonst **unbelegt**.

| Aussage (Lauf, Datum) | Status | Beleg / Abweichung |
|---|---|---|
| Am Rain: alle 6 Geschosse laufen ohne `ValueError` durch (Integration 2026-09-30) | geprüft (Basislauf) | 6 × `status ok`, je 1 `keine_wand_entities` |
| `plan_pruefen` zeigt `wand_warnungen` nicht im Bericht | geprüft (Code) | `grep wand_warnungen scripts/plan_pruefen.py`: 0 Treffer; ebenso `tuer_warnungen`, `sanitaer_befund` |
| Leuchten in `WOHNUNG_PRIVAT`: Mollgasse EG 2, Muthgasse E2 62, Am Rain UG 2 / EG 3 / OG1 2 / OG2 3 / OG3 3 | geprüft (Basislauf) | gleich |
| Leuchten in LIFT: Muthgasse E2 1, Mollgasse 2KG 1; in SCHACHT: Am Rain OG1 1 | geprüft (Basislauf) | gleich |
| Ausgänge je Plan (13 Pläne), Wohnungen, Türen typisiert/gesamt, Segmente je Quelle, Leuchten rz/SL/AP | geprüft (Basislauf) | gleich für alle 13 Pläne |
| Modell-Restüberlappung Barawitzka 4 / 7,131 m², Muthgasse 10 / 15,426 m², 2KG 2 / 2,946 m², Rennweg EG 2 / 1,740 m² | geprüft (Basislauf) | gleich (Muthgasse 15,425 m², Rundung) |
| Räume je Plan („Räume gesamt", „ohne Typ") | **nicht vergleichbar** | VERLAUF zählt die Kaskade, der Basislauf das Modell (z. B. Mollgasse 1KG 29 gegen 31, Am Rain UG 82 = 82) |
| Mollgasse 1KG 22, 2KG 48 Stempel ohne Polygon | **unbelegt (nur VERLAUF)** | Stempel-Zuordnung nicht im Modell, nicht nachgezählt |
| Laufzeiten und Peaks der Prüfstrecke (z. B. OG4 1 551,7 s / 13,28 GB, EG 856,5 s / 6,65 GB) | **unbelegt (nur VERLAUF)** | Basislauf misst Parse + Platzierung ohne Render (EG 476,6 s / 6,30 GB) |
| UG-Normallauf nach 394 s bei 14,3 GB an der RAM-Reißleine abgebrochen; Render OG4 5,6 GB und 107 s je Bild; Kaskade allein 0,45 GB | **unbelegt (nur VERLAUF)** | Mechanismus am Code bestätigt (§ 6.7), Zahlen nicht nachgemessen |
| Gegenprobe OG4 ohne Render: `raeume.json` byte-gleich | **unbelegt (nur VERLAUF)** | nicht wiederholt |
| Suite `6 failed, 1216 passed …` und Gate 1 Verstoß (Integration) | nicht in diesem Schritt nachgemessen | Quelle für diesen Stand ist `docs/INTEGRATION_2026-09-30.md` (Gegenprüfung auf `9f38f58`: 6 failed / 2223 passed; Gate 1 Verstoß) |
| 2026-09-12 Einwand 5: Freiflächen-Regel nur außerhalb des EG, Südgarten-Tür bleibt `final_exit` | geprüft (Code, Test) | `tuer_typisierung.py:157-179` (`not eg`), `test_soll_mollgasse.py::test_soll_hofausgaenge_cluster_a_und_b`; Tür heißt heute `tuer_67` |
| 2026-09-13 BT1-EG: 3 Selbstverbindungen aus Türtexten, 38 Türpaare < 50 mm, `gang_1` ↔ `raum_64` 20,25 m² Überlappung | **unbelegt (nur VERLAUF)** | Code-Stand `3d91a2c`, Plan nicht in der Prüfstrecke; Selbstverbindungen allgemein siehe F-03 |
| 2026-09-13 Zerfall/Schlitz: 5 Restflächen / 9,47 m² echte Nutzfläche entfallen (Klasse c) | **unbelegt (nur VERLAUF)** | Code-Stand `3d91a2c`; `docs/ZERFALL_SCHLITZ_PRUEFUNG.md` in diesem Schritt nicht gelesen; heutiger Stand offen |

---

## 10. Soll-Lücken als strict-xfail (14, Stand `docs/INTEGRATION_2026-09-30.md:103-118`)

`test_soll_barawitzka.py` (explizite Linien, 90 % Türen typisiert, 16 Endpunkte an der Außenkante) ·
`test_soll_mollgasse.py` (Endpunkt an der Kante hat `final_exit`, 90 % typisiert, `final_exit`-Anzahl) ·
`test_soll_muthgasse.py` (jeder Plan-Türblock ist Tür, `stair_exits`, `stair_exit` aus echter Blocktür, 90 %
typisiert) · `test_soll_referenzvergleich.py::test_soll_referenz_trefferquote` ·
`test_soll_rennweg.py::test_soll_eg_90_prozent_tueren_typisiert` ·
`test_ausgang_freiflaeche.py::test_soll_sentinel_aussen_ist_entscheidbar` ·
`test_belichtung_grundlage.py::test_soll_natuerlich_belichtet_bleibt_none_ohne_grundlage`; dazu im Gate-Lauf
`tests/gate/test_gate_tuerstapel.py::test_gate_tuerstapel_erfuellt` (Gate (3) offen). Übersprungen (11): u. a.
`test_soll_baufeld.py` (Baufeld nicht entpackt), `test_layer_korpus.py` (pyarrow fehlt), 5 Tests ohne
`WHA_MOL_EG.dxf`. Keine Schwelle, kein Soll, kein Marker wird gelockert (Owner-Regel).

---

## 11. Reihenfolge für Schritt 2g

**Zählung** (Tabellenzeilen § 1–5 und § 8, je Hauptpriorität; F-07 zählt als P0, seine Teile DD/UG sind P1, die
Doku-Zeile P2):

| Stufe | Zeilen | P0 | P1 | P2 | — |
|---|--:|--:|--:|--:|--:|
| 1 DXF-Laden (D) | 11 | 0 | 5 | 6 | 0 |
| 2 Raumerkennung (R) | 17 | 1 | 8 | 6 | 2 |
| 3 Ausgänge/Fluchtwege (F) | 14 | 1 | 8 | 5 | 0 |
| 4 Platzierung (N, Leonis) | 7 | 1 | 4 | 1 | 1 |
| 5 Planausgabe (O) | 8 | 1 | 3 | 4 | 0 |
| raise-Stellen (X) | 3 | 0 | 0 | 1 | 2 |
| **Summe** | **60** | **4** | **28** | **23** | **5** |

**Abgrenzung zu 2a–2f:** Auftrag 0+1 benennt 2a–2d nicht. Nach seinem Wortlaut ist **2e** der einzige erlaubte
Contract-Punkt (additiv, Owner-Entscheid Selman) und **2f** der RAM-Punkt der Prüfstrecke (Render). Die Liste führt
deshalb **alle** P0/P1; was nach Wortlaut zu 2e/2f passt, ist markiert. Welche Einträge 2a–2d abdecken, streicht der
Planer. „Nach dem Merge" = Owner-Vermerk „kein Code vor dem Merge des Türstapels" (PR #160 offen).

**P0**

1. R-09 + F-07 — Am Rain OG4 ohne Stiegenhaus und ohne Ausgang (Treppe/Lift nur als lose Linien, Erkennung liest nur
   Blocknamen). Owner-Frage vor dem Bau: welcher Beleg genügt (Layer `Treppe`, Text „STGH")? · Selman
2. O-05 / § 6.7 — Render-RAM der Prüfstrecke (8 Render-Aufrufe, doppelte Kaskade) **[2f]** · Selman
3. N-03 / § 6.8 — Leuchten in LIFT/SCHACHT · Leonis, **nur melden**

**P1 — eigene Lane (Selman), nach Hebel**

4. O-04 — `keine_wand_entities`, `seite_fehlt`, `sanitaer_befund` in `bericht.md` (erlaubte `plan_pruefen`-Änderung)
5. R-05 a — Raster-Reißleine der R-Stufe, Verlust als Warnung statt `print`
6. F-03 — Ausgänge an Türen `von_raum == nach_raum` (Barawitzka: einziger `final_exit`; `stair_exit` im Stiegenhaus)
7. D-04 — mm-Faktor und Quelle ausweisen (8 von 13 über `$INSUNITS`, Türprobe widerspricht 4×); Hard Stop = Owner-Frage;
   S-MST nach dem Merge
8. N-07 — Leuchten in keinem Raumpolygon (Muthgasse 57): Ursache messen, Raumerkennung oder Platzierung
9. F-09 — nur FALLBACK-Segmente (Am Rain UG, OG4, Mollgasse 1KG), „kein final_exit erreichbar"
10. F-04 / F-05 — `seite_fehlt` (Am Rain EG 186, OG1 177, UG 159) und Türrollen-Quote (Am Rain UG 13/295)
11. F-08 / § 6.3 — S4g a–c, Messfall `exit_tuer_67` zuerst · nach dem Merge
12. F-01 — S4f `Rectangular Door Opening`; Muthgasse-Türblöcke (roter Test) · S4f nach dem Merge
13. D-05 + D-07 + R-02 — S3c Fremdcluster und Bounds-Ausreißer (Muthgasse 503,8 × 275,9 m) · nach dem Merge
14. R-05 b / R-17 / § 6.5 — freie Flächen außerhalb der größten Konturkomponente · Owner-Frage
15. D-06 — `_NEGATIV_LAYER` ohne „Moeblierung"/„Möblierung"; D-03 — `Wand brüstungshoch` · Owner-Frage
16. F-13 — Mollgasse EG `raum_51`/`raum_55`
17. F-07 (P1-Teil) — Rennweg DD (Owner-Frage), Rennweg UG ohne `final_exit`
18. R-10 — Liftschacht mit Stiegenhaus-Rest verschmolzen, `lift_1` über Nasszelle
19. O-06 — Fehler-Fang je Plan in der Prüfstrecke. **Außerhalb der Änderungsgrenze** dieses Auftrags
    (`plan_pruefen` nur für Warnungs-Ausgabe und 2f) → Owner-Freigabe nötig
20. R-01 / § 6.10 — S-KG (Material fehlt im Baum) · nach dem Merge
21. R-16 — 11 unbestimmte GANG/VORRAUM, Gate (9) nicht verdrahtet (Material fehlt)
22. § 6.1 — S4c-Pins: **nicht anfassen** (Owner 2026-09-30), bleibt offen geführt
23. F-06 / § 6.4 — korrigierte Rolle an der Naht; nur über den Contract lösbar **[2e-Kandidat]**

**P1 — fremde Lanes (nur melden, kein Code)**

24. R-15 — Gate (3) DG2 `M4.einraum` 0 → 1 · Enis, Board 3
25. R-08 — Kanon WOHNKÜCHE, KELLERABTEIL, „Dachterrasse" · Enis
26. N-02 / § 6.8 / § 6.9 — Leuchten in `WOHNUNG_PRIVAT`, Board-1-Tests · Leonis
27. N-04 — rohe Türrolle an der Naht · Leonis / Contract
28. N-05 — Aufheller durch die Wand (DG1 `raum_3`) · Leonis
29. O-03 — PDF-Export-RAM auf Am Rain ungemessen · gemeinsam

**P2 (danach)**

D-01, D-02, D-08, D-09, D-10, D-11 · R-04, R-06, R-07 (Enis), R-11, R-12, R-14 · F-02, F-07 (veraltete Zeilenangabe
`provider.py:102`), F-10 / § 6.6 Durchleitung (additives Segment-Feld, **[2e-Kandidat]**), F-11, F-12, F-14 (Enis) ·
N-06 (Leonis) · O-01, O-02, O-08 (gemeinsam), O-07 · X-02.

---

## 12. Punkt 2a — Warnung und Weiterlauf (erledigt mit dem Commit dieses Eintrags)

**Regel (Owner-Auftrag 2026-09-30):** ein leerer oder defekter Plan (keine Geometrie, keine Wand-Entities, kein
Modelspace, defekte Entities, kein Raum) liefert ein `RaumModell` (ggf. ohne Räume) und eine Warnung im Bericht,
keinen Abbruch. Einzige Ausnahme: Datei nicht lesbar oder kein DXF.

**Vorher gelistet** (Kopf `829e01a`, Code = `0434392`): `grep -n "raise\b"` über
`src/notbeleuchtung/raumerkennung/*.py` ohne `_port/` → 3 Treffer (= § 8); `_port/parsers/room_faces.py` und
`_port/models/room.py` → 0; kein `assert`. Dazu die zwei Abbrüche ohne `raise`-Anweisung, die die neuen Testfälle
auslösen (X-04, X-05).

| Nr. | Stelle (vorher → nachher) | Bedingung | Aufrufer / Fang vorher | Verhalten vorher | Verhalten nachher |
|---|---|---|---|---|---|
| X-01 | `dxf_load.py:258` → `:267` `bounds_mm` | keine Stützpunkte auf den erkannten Wand-Layern | einziger Aufrufer `provider.py:133` → `:137`, gefangen `except ValueError` `:134` → `:138` | Fallback-Bounds + `keine_wand_entities` | unverändert; die Warnung entfällt nur, wenn gar keine Geometrie da ist (dann `keine_geometrie`) |
| X-02 | `provider.py:141` `parse` | X-01 warf, keine Wandkörper, kein Stützpunkt (LINE, LWPOLYLINE, POLYLINE, INSERT) | nicht gefangen | `ValueError` „DXF ohne Geometrie" → Pipeline/API 422, Prüfstrecke bricht ab (`plan_pruefen.py:1632` → alle folgenden Pläne, O-06) | **kein `raise` mehr:** Bounds (0, 0)–(0, 0) (`provider.py:148`), Warnung `keine_geometrie` (`:149-151`); `parse` läuft auf dem leeren Plan zu Ende |
| X-03 | `wandkoerper.py:296` `bounds_aus_wandkoerpern` | leere Wandkörper-Liste | alle 5 Aufrufer prüfen vorher (§ 8) | im Parse nicht erreichbar | unverändert |
| X-04 | `dxf_load.py:234` → `:241` `ezdxf.readfile` (ohne `raise`) | Datei fehlt (`FileNotFoundError`), kein DXF (`OSError` „… is not a DXF file."), Struktur defekt (`DXFStructureError`, z. B. „missing ENDSEC tag.") | ungefangen | rohe ezdxf-/OS-Ausnahme | **gewollter Abbruch** `DxfNichtLesbar(ValueError)` „DXF nicht lesbar: <Pfad> — <ezdxf-Grund>" (`dxf_load.py:232-243`) |
| X-05 | `fluchtweg.py:84` `_effektive_farbe` (ohne `raise`) | Linie mit BYLAYER-Farbe auf einem Layer ohne Tabelleneintrag (Minimal-DXF ohne TABLES) | `explizite_linien` ← `provider.parse` | `DXFTableEntryError`, Abbruch | Layer ohne Eintrag → Farbe 0 (der vorhandene `None`-Zweig war dafür gedacht), kein Abbruch (`fluchtweg.py:84-88`) |

Neu am Ende von `parse`: Warnung `keine_raeume`, wenn das Modell keinen Raum hat (`provider.py:333-336`).

**Begründung der Ausnahme (X-04):** ohne gelesenes Dokument gibt es keinen Plan, an dem ein Modell oder eine
Warnung hängen könnte. `DxfNichtLesbar` erbt von `ValueError` (derselbe Typ wie der alte Abbruch X-02) und nennt
Pfad und ezdxf-Grund; die API gibt die Meldung als 422 weiter (`api/main.py:315-316` fängt `Exception`).
„Kein Modelspace" ist kein eigener Fall: ezdxf legt den Modelspace auch für eine DXF nur aus einer
ENTITIES-Sektion an (Testfall `ohne_tabellen`), eine DXF ohne Entities ist der Fall `ohne_geometrie`.

**Warnungen gebündelt** in `provider.wand_warnungen` (Muster `tuer_warnungen`, kein Contract-Feld):
`keine_wand_entities` (Text unverändert), `keine_geometrie`, `keine_raeume`. `scripts/plan_pruefen.py`, nur
Berichtsausgabe: `_fachteil3` gibt sie zurück (`:1332`), `plan_pruefen` reicht sie an `_bericht` (`:1650`),
`_bericht` stellt sie an den Anfang von „## Warnungen" (`:1814`, `:1845`).

**Tests** (`tests/raumerkennung/test_provider.py`):
`test_leerer_oder_defekter_plan_warnt_statt_abbruch[ohne_geometrie|nur_text|waende_ohne_raum|ohne_tabellen]`
(RaumModell ohne Räume, Warnungen je Fall, Contract-Roundtrip), `test_nicht_lesbare_datei_definierter_fehler`
(Nicht-DXF und fehlende Datei), `test_plan_pruefen_schreibt_wand_warnung_in_bericht` (Prüfstrecke end-to-end auf dem
Hatch-Plan ohne Wand-Layer, `ERGEBNIS` nach `tmp_path`).

**Rot vor dem Fix** (`pytest tests/raumerkennung/test_provider.py -k "leerer or nicht_lesbare or
plan_pruefen_schreibt" --tb=line`, Kopf `829e01a`, Kurzform):

```
[ohne_geometrie]    src/.../raumerkennung/provider.py:141: ValueError: DXF ohne Geometrie — nichts zu erkennen.
[nur_text]          src/.../raumerkennung/provider.py:141: ValueError: DXF ohne Geometrie — nichts zu erkennen.
[waende_ohne_raum]  tests/raumerkennung/test_provider.py:201: AssertionError: []
[ohne_tabellen]     ezdxf/sections/table.py:145: ezdxf.lldxf.const.DXFTableEntryError: A-WALL
test_nicht_lesbare_datei_definierter_fehler         test_provider.py:206: ImportError: cannot import name 'DxfNichtLesbar'
test_plan_pruefen_schreibt_wand_warnung_in_bericht  test_provider.py:229: AssertionError:  (2)
6 failed, 6 deselected in 2.65s
```

**Grün nach dem Fix:** dieselbe Auswahl 6 passed; `test_provider.py` gesamt 11 passed, 1 skipped
(`test_mollgasse_parse_valid`, WHA_MOL_EG.dxf nicht im Repo, wie vorher).

**Blast** (Runner `ArchitekturRaumProvider().parse(dxf, "")` + Default-Platzierung, je Plan allein; Vergleich des
kompletten JSON ohne Lauf-Metadaten: Räume mit Polygon/Fläche/Klasse/Wohnung/Flags, Türen, Ausgänge, Segmente,
Anker, Stiegenhäuser, Bounds, korrigierte Rollen, bestätigt-privat, alle Provider-Warnungen, Leuchten je Lage und
Klasse): **13 von 13 feldgleich zur Basis `0434392`** — Rennweg UG/EG/OG1/OG2/OG3/DG1/DG2/DD, Barawitzka EG,
Mollgasse EG/1OG, Muthgasse E2, Am Rain OG4 (allein). Erwartet: alle geänderten Zweige greifen nur ohne jede
Geometrie, ohne Raum, bei nicht lesbarer Datei oder bei Layern ohne Tabelleneintrag.

**Volle Suite** (allein, 27 min 36 s): `6 failed, 2229 passed, 11 skipped, 6 deselected, 14 xfailed` — dieselben 6
roten wie vorher (3 × `test_keine_leuchten_in_wohnung_privat` OG1/OG2/DG1 = Board 1 Leonis,
`test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell`, die 2 S4c-Pins), 2229 = 2223 + 6 neue, 0 xpassed.

**Gate:** `pytest -m gate tests/gate` 3 passed, 1 xfailed (wie vorher). `gate_messung` auf dem Arbeitsbaum dieses
Commits (vor dem Commit, `_arbeit/gate/messung_829e01a-dirty-2a.json`), `pruefe_gate` gegen
`nullmessung_f15d03f.json`: (0) unsauberer Arbeitsbaum (erwartet, vor dem Commit gemessen) und **(3) `M4.einraum`
DG2 0 → 1** (Enis Board 3, unverändert); M17 18/18; Barawitzka ABSTELLRAUM 1 Verbindung, OG3 0 Anker in
`WOHNUNG_PRIVAT`, DG1 2 Ausgänge / 0 durch den Liftschacht.

**Einmal-Läufe (kein Test):** alle vier synthetischen Pläne laufen durch `plan_pruefen.plan_pruefen` (bericht.md
„## Warnungen" mit `keine_geometrie`/`keine_raeume`); `ohne_geometrie` und `waende_ohne_raum` laufen durch
`pipeline.run` mit Default-Bundle (0 Räume, Ausgabe-DXF geschrieben).

**Offen nach 2a:**
- O-04 Rest: `tuer_warnungen` (`seite_fehlt`) und `sanitaer_befund` stehen weiter nicht in `bericht.md`. P1 · Selman.
- `wand_warnungen` erreichen weder `pipeline.run` noch die API: `_summary` warnt nur `if raum.raeume`
  (`hauptengine/pipeline.py:77`, `:86`), im Render-Pfad fehlt der Schlüssel `warnungen` ganz (Einmal-Lauf:
  `render_summary.get("warnungen")` = `None`). Ein leerer Plan kommt dort als Blatt ohne Leuchten und ohne Hinweis
  zurück. Änderung läge in `hauptengine/` (gemeinsam) → nur gemeldet. P1 · gemeinsam.
- Defekte Entities nur für „Layer ohne Tabelleneintrag" getestet; implizite Ausnahmen anderer defekter Entities
  (KeyError, GEOS, kaputte HATCH-/INSERT-Referenzen) weiter nicht systematisch geprüft (§ 8). P2 · Selman.
- `Projekte/_ergebnis/*/bericht.md` nicht neu erzeugt (Prüfstrecke mit Render nur nach 2f, RAM); die Am-Rain-
  Berichte zeigen `keine_wand_entities` erst nach dem nächsten Lauf.

---

## 13. Punkt 2b — S4g: Balkonkonturen sind kein Ausgang (b und c erledigt, **a offen: STOPP**)

**Regel (Owner-Auftrag 2026-09-30):** ein `final_exit` braucht einen Türbezug (Tür/Öffnung mit Raumseite, Rolle ≠
`balkontuer`) und einen Geschossbezug (EG oder belegter Ausgang ins Freie); eine Balkon-/Terrassen-/Loggia-Kontur
ist nie Ausgang. Die EG-Ausnahme Mollgasse `exit_tuer_67` (Südgarten) bleibt erhalten.

**Vorher** (Code `b849dd0`). Quelle: 12 Prüfpläne + Am Rain OG4 = Nachher 2a; Mollgasse 1KG/2KG und Am Rain UG/EG
neu gerechnet auf `b849dd0` (je allein), Raumerkennung feldgleich zur Basis `0434392`. Türbezug = ID-Konvention
`exit_<tuer_id>` zeigt auf eine Tür des Modells; Raumseite = mindestens eine Seite ist ein Raum des Modells (nicht
`AUSSEN`/`KEIN_RAUM`).

| Plan | Geschoss | final_exit | stair_exit | ohne Tür | Tür ohne Raumseite / Balkontür |
|---|---|---|---|---|---|
| Rennweg_UG | UG | 0: — | 2: `exit_tuer_7`, `exit_durchgang_2` | — | — |
| Rennweg_EG | EG | 2: `exit_tuer_8`, `exit_tuer_18` | 3: `exit_durchgang_18`, `exit_durchgang_19`, `exit_durchgang_20` | — | — |
| Rennweg_OG1 | 1OG | 0: — | 2: `exit_durchgang_6`, `exit_durchgang_7` | — | — |
| Rennweg_OG2 | 2OG | 0: — | 1: `exit_tuer_1` | — | — |
| Rennweg_OG3 | 3OG | 0: — | 3: `exit_tuer_5`, `exit_tuer_6`, `exit_tuer_12` | — | — |
| Rennweg_DG1 | DG | 0: — | 2: `exit_durchgang_6`, `exit_durchgang_7` | — | — |
| Rennweg_DG2 | DG | 0: — | 3: `exit_durchgang_4`, `exit_durchgang_5`, `exit_durchgang_6` | — | — |
| Rennweg_DD | — | 0: — | 0: — | — | — |
| Barawitzka_EG | EG | 1: `exit_tuer_31` | 0: — | — | `exit_tuer_31` |
| Mollgasse_EG | EG | 8: `exit_1`, `exit_2`, `exit_3`, `exit_4`, `exit_tuer_16`, `exit_tuer_60`, `exit_tuer_67`, `exit_aussenoeffnung_1` | 1: `exit_tuer_68` | `exit_1`, `exit_2`, `exit_3`, `exit_4` | — |
| Mollgasse_1OG | 1OG | 0: — | 1: `exit_durchgang_10` | — | — |
| Muthgasse_E2 | 2OG | 0: — | 1: `exit_durchgang_74` | — | — |
| Mollgasse_1KG | KG | 1: `exit_aussenoeffnung_1` | 0: — | — | — |
| Mollgasse_2KG | KG | 0: — | 1: `exit_durchgang_8` | — | — |
| AmRain_UG | UG | 2: `exit_tuer_113`, `exit_tuer_150` | 4: `exit_tuer_160`, `exit_tuer_186`, `exit_durchgang_4`, `exit_durchgang_22` | — | — |
| AmRain_EG | EG | 2: `exit_tuer_68`, `exit_tuer_231` | 1: `exit_tuer_155` | — | — |
| AmRain_OG4 | 4OG | 0: — | 0: — | — | — |

Summe: 16 `final_exit`, 25 `stair_exit` auf 17 Plänen. **Ohne Tür:** nur Mollgasse EG `exit_1` … `exit_4`
(`footprint.hauptausgaenge`, `footprint.py:123-135`, Aufruf `provider.py:183`). Alle 25 `stair_exit` hängen an einer
Tür. **Tür ohne Raumseite:** nur Barawitzka EG `exit_tuer_31` (`tuer_31` `KEIN_RAUM`\|`KEIN_RAUM`, `hauseingang` über
Text „Eingang"). **Balkontür als Ausgang:** 0. Das Zusammenlegen (`provider.py:255-261`) hat auf keinem der 17 Pläne
einen türgebundenen Ausgang verdrängt (Mollgasse EG: alle 5 aus `leite_ausgaenge` im Modell).

**Mollgasse EG `exit_1` … `exit_4` einzeln** (Plan angesehen: Bogenpaar, Nachbarraum, Komponentenkante; Diagnose-Lauf
und Ausschnitte im Session-Scratch, nicht im Repo):

| Ausgang | Lage | Bogenpaar (Layer, Radius, Drehpunkt-Abstand) | Befund | GRAPH-Wege mit Ziel |
|---|---|---|---|---|
| `exit_1` | Ostwand von `raum_51` (STIEGENHAUS 122,4 m²), öffnet nach Osten auf eine Fläche mit Text „GEFÄLLE 2%", Komponentenkante 1 920 mm | 2 × `05-SYM-G00-LEG-M0`, r 1 000 / 1 000, 2 000 mm, spiegelbildlich (270–360° / 0–90°), Text „EI2 30-C - FTS" | **echte Doppeltür**, aber keine Tür im Modell (nächste `tuer_35` 3,8 m): Loch der Türerkennung | 0 |
| `exit_2` | 8 mm neben `raum_30` (MÜLLRAUM), keine Tür ≤ 4 m | oberer Flügel von `exit_1` (r 1 000) + Einzeltür Müllraum (r 900), 2 576 mm | **kein Ausgang** — zwei fremde Bögen gepaart | 0 |
| `exit_3` | Hof-Teil von `raum_51` (Texte „ZAUN, H = 1.00 m", „GEFÄLLE 2%"), Komponentenkante 930 mm | `tuer_52` (`05-SYM`, r 1 000, Nordwand Stiegenhaus → Hof, „EI2 30-C - FTS") + `tuer_68` (`02-ANS`, r 800, an der Zaunlinie „ZAUN, H = 1.00 m"), 2 334 mm | **kein Doppeltürpaar**, steht aber für den echten Hof-Ausgang: `tuer_52` `raum_51`\|`KEIN_RAUM`, `tuer_68` `raum_51`\|`raum_51` — `raum_51` fasst Stiegenhaus und Hof (F-13), darum wird keine der beiden Türen `final_exit`. Einziger `final_exit` an Cluster A (837 mm) | 1 (`seg_graph_tuer_35`) |
| `exit_4` | in `raum_41` (GANG 77,1 m²), Komponentenkante 978 mm | `tuer_55` (`05-SYM`, r 900) + Bogen auf dem Fluchtweg-Layer `09-WEG-G00-Leg-M0` (r 1 002, zugleich `tuer_64` `raum_41`\|`KEIN_RAUM`), 2 185 mm | **kein Doppeltürpaar**; der `09-WEG`-Bogen spricht für einen Fluchtweg-Ausgang aus `raum_41`, eine Tür dafür ist nicht belegt | 9 |

Die GRAPH-Wege erreichen `exit_3`/`exit_4` über die Nächste-Tür-Bindung für Ausgänge ohne Tür
(`fluchtweg.py:296-300`, ≤ 1 500 mm).

**Rot vor dem Fix** (`pytest tests/naht/test_s4g_ausgang_tuerbezug.py --tb=line`, Kopf `b849dd0`, Kurzform):

```
test_mollgasse_eg_kein_ausgang_ohne_tuerbezug  test_s4g_ausgang_tuerbezug.py:37: AssertionError: assert ['exit_1', 'e..._3', 'exit_4'] == []
test_balkontuer_ist_nie_final_exit             test_s4g_ausgang_tuerbezug.py:76: AssertionError: assert [('exit_t1', ...'final_exit')] == [('exit_t2', 'final_exit')]
2 failed, 2 passed in 33.16s
```

(Zeilennummern und Testname vor dem xfail-Marker; heute `test_soll_mollgasse_eg_kein_ausgang_ohne_tuerbezug`.)

Die zwei grünen sind die Messfälle, die schon vorher halten: `exit_tuer_67` `final_exit` / `exit_tuer_68` `stair_exit`
und Rennweg EG `exit_tuer_8` + `exit_tuer_18`.

**a — gebaut, gemessen, zurückgenommen (STOPP).** Fix: `provider.parse` ohne `footprint.hauptausgaenge`
(`vorhandene` startet leer; Harness in `test_s7_wohnungsklasse._eingabe` nachgezogen). Mollgasse EG, Runner allein:

| | vorher | nachher (Fix a) |
|---|---|---|
| Ausgänge | 8 `final_exit` + 1 `stair_exit` | 4 `final_exit` (`exit_tuer_16`, `_60`, `_67`, `exit_aussenoeffnung_1`) + 1 `stair_exit` (`exit_tuer_68`) |
| GRAPH-Wege | 14 (`exit_4` 9, `exit_tuer_16` 4, `exit_3` 1) | 4 (`exit_tuer_16`); die 10 übrigen fallen weg, je Warnung „kein final_exit erreichbar" (`tuer_5`, `_9`, `_11`, `_20`, `_21`, `_24`, `_25`, `_26`, `_35`, `_50`) |
| FALLBACK | 3 | 4 (`seg_fallback_raum_39`) |
| Leuchten rz / SL | 24 / 27 | 22 / 25 |

`pytest` (Mollgasse-, Ausgangs-, Provider-, GT- und e2e-Auswahl, 9 Dateien): `1 failed, 78 passed, 1 skipped, 4 xfailed`
— rot: `test_soll_mollgasse.py::test_soll_hofausgaenge_cluster_a_und_b` („kein final_exit an Cluster A (2689400.0,
1524600.0)"). Kein Geschoss verliert alle Ausgänge, aber ein scharfer Test wird rot und 10 von 14 Wegen samt 4 Leuchten
fallen weg (Grundsatz (a)). Fix a ist darum **nicht** committet; der Naht-Test steht als strict-xfail
`test_soll_mollgasse_eg_kein_ausgang_ohne_tuerbezug` (dreht, sobald a gebaut ist).

**b — erledigt.** Kette geprüft: `tuer_typisierung` setzt `balkontuer` mit `ist_notausgang=False` (`:179-181`,
`:187-189`), ein Türtext dreht das nicht zurück (`:225-227`); **aber** `markiere_windfang` setzt `ist_notausgang=True`
ohne Blick auf die Rolle (`:276`), und `leite_ausgaenge` las nur das Flag. Neu: `ausgaenge.py:83-89` — eine
`balkontuer` wird nie `final_exit`, auch mit gesetztem Flag (auf den 17 Plänen 0 Fälle, also ohne Wirkung auf die
Messung). Test `test_balkontuer_ist_nie_final_exit`.

**c — erledigt (Messfall).** `test_mollgasse_eg_messfall_suedgarten_und_hoftuer`: `exit_tuer_67` bleibt `final_exit`
(`tuer_67` `AUSSEN`\|`raum_61` TERRASSE, `ist_notausgang`, Rolle ≠ `balkontuer`), `exit_tuer_68` bleibt `stair_exit`;
dazu `test_rennweg_eg_behaelt_seine_zwei_final_exit`.

**Raumseite nicht gebaut:** die Bedingung träfe einzig Barawitzka EG `exit_tuer_31`, den einzigen Ausgang des
Geschosses → STOPP-Bedingung „kein Geschoss verliert alle Ausgänge". Die Ursache liegt in der Türzuordnung (F-03/F-04).

**Nachher** (Commit-Stand = nur b; Runner je Plan allein): **17 von 17 feldgleich** zum Vorher (Vergleich des
kompletten Runner-JSON ohne Lauf-Metadaten: Räume, Türen, Ausgänge, Segmente, Anker, Stiegenhäuser, Bounds,
korrigierte Rollen, alle Provider-Warnungen, Leuchten je Lage und Klasse) — 12 Prüfpläne + Am Rain OG4 gegen 2a,
Mollgasse 1KG/2KG und Am Rain UG/EG gegen die Basis `0434392`. final/stair je Plan vorher = nachher (Tabelle oben),
**kein Ausgang entfallen**, kein Geschoss ohne Ausgang, das nicht schon vorher keinen hatte (Rennweg DD, Am Rain OG4).
Laufzeit/Peak (Parse + Platzierung, je allein): Am Rain UG 114,2 s / 3,91 GB, EG 472,3 s / 6,30 GB, OG4 21,8 s / 0,43
GB; Muthgasse E2 634,9 s / 11,29 GB.

**Volle Suite:** (allein, 28 min 8 s): `6 failed, 2232 passed, 11 skipped, 6 deselected, 15 xfailed` — dieselben 6
roten wie nach 2a (3 × `test_keine_leuchten_in_wohnung_privat` OG1/OG2/DG1 = Board 1 Leonis,
`test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell`, die 2 S4c-Pins), 2232 = 2229 + 3 neue,
15 xfailed = 14 + der neue strict-xfail, 0 xpassed.

**Gate:** `pytest -m gate tests/gate` 3 passed, 1 xfailed (wie vorher). `gate_messung` auf dem Arbeitsbaum dieses
Commits (vor dem Commit, `_arbeit/gate/messung_b849dd0-dirty-2b.json`), `pruefe_gate` gegen
`nullmessung_f15d03f.json`: (0) unsauberer Arbeitsbaum (erwartet, vor dem Commit gemessen) und **(3) `M4.einraum` DG2
0 → 1** (Enis Board 3, unverändert); M17 18/18; **(11) DG1 grün:** 2 Ausgänge (`exit_durchgang_6`, `_7`), 0 durch den
Liftschacht. Alle Messfelder außer `meta` gleich der 2a-Messung.

**Offen nach 2b:**
- **S4g a (P1, Owner):** erst einen türgebundenen Ersatz, dann die footprint-Ausgänge entfernen — (i) Hof-Ausgang
  Cluster A: `raum_51` trennt Stiegenhaus und Hof nicht (F-13), `tuer_52`/`tuer_68` bekommen darum nie `AUSSEN`;
  (ii) `raum_41`: welche Tür ist der Ausgang, den `exit_4` vertritt (9 Wege)? (iii) `exit_1`: Doppeltür „EI2 30-C" ohne
  Tür-Objekt (Türerkennung). Nicht gebaute, nicht gemessene Owner-Option: `footprint`-Ausgang nur mit Tür ≤ 1 500 mm
  (dieselbe Bindung wie `fluchtweg.py:296-300`) — behielte `exit_3`/`exit_4`, verwürfe `exit_1`/`exit_2`.
- **Raumseite (P1):** Barawitzka `tuer_31` `KEIN_RAUM`\|`KEIN_RAUM` — erst die Türzuordnung, dann die Bedingung.
- `test_ausgang_freiflaeche.py::test_soll_sentinel_aussen_ist_entscheidbar` nennt im xfail-Grund noch „4 der 19 ohne
  Türbezug, `provider.py:102`" (Marker unverändert gelassen).
- `Projekte/_ergebnis/` nicht neu erzeugt (Verifikation über den Runner wie 2a).
