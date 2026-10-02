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
| D-04 | mm-Kalibrierung | `dxf_load.py:_calibrate_factor:163`, `_door_arc_factor:125`, `_raw_wall_span:107` | nur synthetisch + Mollgasse-Fixtures (`test_dxf_load.py::test_wand_im_block_kalibriert_nicht_ueber_insunits`, `::test_ausreisser_kippen_den_faktor_nicht`) | S-MST (`docs/OFFENE_FRAGEN.md`, § S-MST): Türprobe nur Tiebreak (:175-176); stiller Rückfall auf `$INSUNITS` (:180-181) — **ohne Wand-Linien immer** (`_raw_wall_span` liefert 0,0 → keine Kandidaten, :171-174). Gemessen (§ 7): **8 von 13** Prüfplänen laufen über `$INSUNITS` (Rennweg EG/OG3: Wand-Layer ohne Linien-Stützpunkte; Am Rain ×6: kein Wand-Layer), und auf 4 davon widerspricht die Türprobe (Rennweg EG, Am Rain OG4/OG3/EG: Faktor 10 statt 1); Faktor nirgends ausgewiesen (`plan_pruefen` nutzt `plan.factor` nur zum Zeichnen, :159/:203-210); kein Messfall gegen echte Pläne. `_door_arc_factor` sucht `DOOR` im Blocknamen (:140-141), die Türerkennung kennt `DOOR` nicht (F-01). Owner offen: Hard Stop oder Warnung. **→ 2g (§ 20.3): Rückfall auf `$INSUNITS` steht mit Türprobe als `mm_faktor: …` unter „Warnungen"; Hard Stop offen.** | P1 | Selman (Owner-Frage) |
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
| R-04 | F-Stufe (Stempel-Flutung) | `stempel_flutung.py:flute_stempel:227`, Reißleine `:246-257` | `test_stempel_flutung.py` | Reißleine liefert `[]` mit `RuntimeWarning` — alle Flut-Räume weg, im Bericht nicht sichtbar. **→ 2g (§ 20.2): steht jetzt als `flutung: …` unter „Warnungen".** | P2 | Selman |
| R-05 | R-Stufe (stempellose Restflächen) | `rest_komponenten.py:komponenten_ohne_stempel:228`, `_typisiere:200` | `test_rest_komponenten.py` (22 Tests, u. a. K2 und S3b) | (a) **keine Raster-Reißleine** (`:248-255`, anders als R-04); ein `MemoryError` wird in `kaskade.py:177-181` gefangen → nur `print`, R-Stufe leer, stempellose Stiegenhauskerne/Gänge fehlen still. (b) Sucht nur in der **größten** Komponente der Außenkontur (`aussenkontur:278-289`, `d_mm=1000` :245; Modul-Doc :20-21) — freie Flächen außerhalb werden kein Raum (Pflicht-Eintrag „freie Flächen"). Ob ein Mehr-Trakt-Plan des Korpus (Barawitzka 2 Trakte) dadurch Räume verliert: nicht gemessen. **→ (a) 2f (§ 18) Raster-Obergrenze, 2g (§ 20.2) Fehler und Grenzen als Warnung im Bericht; (b) offen.** | P1 | Selman |
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
| R-17 | Freie Flächen (K1-Diagnose) | — (R-Stufe R-05 b); **2d:** `freiflaeche.py:fuelle_freie_flaechen`, Aufruf `provider.py` nach `_tueren_und_wohnungen` | `test_freiflaeche.py` (4), `tests/naht/test_freiflaeche_wohnung.py::test_dg1_sofa_feld_geht_ins_wohnzimmer` | Pflicht-Eintrag § 6.5. **→ 2d erledigt im Wohnungsumriss (§ 16):** 16 Flächen > 2 m² auf 24 Plänen, 4 → Raum, 12 → neuer Raum UNBEKANNT; Flächen außerhalb eines Wohnungsumrisses bleiben frei (R-05 b). | P1 | Selman (Owner-Frage) |

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
| F-10 | Durchleitung durch private Räume | `wohnungsklasse.py:durchleitung_raeume:921`, `fluchtweg.py:382-399` | `test_wohnungsklasse.py::test_durchleitung_zerreisst_den_weg_nicht`, `::test_durchleitung_wird_als_warnung_ausgewiesen`, `::test_durchleitung_fuehrt_nicht_durch_die_wand` | Pflicht-Eintrag § 6.6. **→ 2e (§ 17): entschieden B — kein Contract-Feld, Board-Antrag geschlossen.** | P2 | Contract (3 Owner) |
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
| O-04 | Warnungen im Prüfbericht | `plan_pruefen.py:_geschoss_md:1136`, `_kreuzcheck_md:1153` | — | `wand_warnungen` (`keine_wand_entities`), `tuer_warnungen` (`seite_fehlt`) und `sanitaer_befund` erscheinen **nicht** in `bericht.md` (0 Treffer). Die Owner-Regel P0 („es bleibt eine Warnung") ist in der Prüfstrecke unsichtbar. **→ 2a (§ 12): `wand_warnungen` stehen jetzt im Abschnitt „Warnungen"**; `tuer_warnungen` und `sanitaer_befund` weiter offen. **→ 2g (§ 20.1): beide jetzt ebenfalls unter „Warnungen".** | P1 | Selman |
| O-05 | Plan-Render der Prüfstrecke (RAM) | `plan_pruefen.py:_figur:137`, 8 Aufrufstellen (:419/:491/:667/:740/:854/:1556/:1565/:1589) | — | Pflicht-Eintrag § 6.7. | P0 | Selman |
| O-06 | Prüfstrecken-Schleife | `plan_pruefen.py:main:1984-2034` | — | Kein Fehler-Fang je Plan (:1990-1992): ein Fehler bricht alle folgenden Pläne ab, und `VERLAUF.md` wird nicht geschrieben (`_verlauf_schreiben` erst nach der Schleife, :2030-2032). | P1 | Selman |
| O-07 | Maßstab im Bericht | — | — | Faktor und Beleg nicht ausgewiesen (D-04). **→ 2g (§ 20.3): im `$INSUNITS`-Rückfall ausgewiesen (Warnung); ein Faktor aus der Spanne steht weiter nicht im Bericht.** | P2 | Selman |
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
  - `rest_komponenten` ohne Raster-Reißleine (R-05 a, P1). **→ 2f (§ 18):** gröbere Zelle über 1e8 Zellen,
    Reißleine über 200 mm, je mit `RuntimeWarning`.
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
- K4-Nachzug: netto **270** korrigierte Rollen kippen gegen `f682c77` (Muthgasse 260, Mollgasse 10)
  (`docs/SLICES_K1_K4.md:1345`, `:1358`; die 277 ist überholt) — nachgemessen alle `zimmertuer` → `wohnungseingang`,
  nicht in beide Richtungen. **→ 2c erledigt (§ 14):** Loch-Raum-Artefakt Option W, 277 fälschlich (dazu Barawitzka
  EG 3, Am Rain EG 2 / OG2 2), 0 zu Recht, behoben in `wohnungsraeume`; K4-Frage 2 als Lesart zur Owner-Bestätigung.
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
- **→ 2d erledigt (§ 16):** Owner-Regel „im Wohnungsumriss keine freie Fläche ohne Raum“; das Feld geht über die
  offene Grenze ins Wohnzimmer (73,95 → 90,89 m²), Test `test_freiflaeche_wohnung.py`.

### 6.6 Durchleitung

- `FluchtwegSegment` hat kein Feld `durchleitung` (`hauptengine/contracts/raum_modell.py:184-196`, gelesen);
  Board-Antrag (`provider.py:104-107`, `docs/GATE_TUERSTAPEL.md:903-904`).
- Erkennbar nur als GRAPH-Direktlinie Tür → Tür durch einen `WOHNUNG_PRIVAT`-Raum mit Flags 00, nie
  `start_raum`/`ziel_raum` (`fluchtweg.py:20-27`, `:382-399`); Text `durchleitung: seg_graph_<tür> …` in
  `wohnungsklasse_warnungen` → `bericht.md`.
- Gemessen 0 Durchleitungen (`docs/COORDINATION.md` Log 2026-09-30 Punkt 6); Basislauf: 0 `durchleitung:`-Zeilen
  auf allen 13 Plänen.
- Prio **P2** (0 Fälle) · Lane Contract (3 Owner).
- **→ 2e (§ 17): entschieden B** (kein Feld, Board-Antrag geschlossen). Die Aussage „nie `start_raum`/`ziel_raum`"
  oben gilt nicht (synthetisch `start_raum` = durchgeleiteter Raum, § 17), ebenso wenig „immer Direktlinie" (nicht
  konvex → Skelettpfad, `fluchtweg.py:391-404`).

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
- **→ 2f erledigt (§ 18):** gemessen je Phase; Treiber F-Stufe (Vollraster je Stempel und Stufe), Linientyp-Striche
  im Render, Figuren erst mit dem Zyklen-GC frei, EG-Parse je OG. Gemeinsamer Lauf aller 13 Pläne mit Render:
  Spitze 4,19 GB, 4 829 s. PDF-Export (O-03) bleibt offen.

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
fehlen), `:194-195` (Bereinigung). **→ 2g (§ 20.2): alle drei zusätzlich als `kaskade_fehler: …` im Bericht.** `stempel_flutung.py:246-257` warnt statt zu werfen (R-04). Die übrigen
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
| Laufzeiten und Peaks der Prüfstrecke (z. B. OG4 1 551,7 s / 13,28 GB, EG 856,5 s / 6,65 GB) | **unbelegt (nur VERLAUF)** | Basislauf misst Parse + Platzierung ohne Render (EG 476,6 s / 6,30 GB); **2f (§ 18):** OG4 mit Render nachgemessen 1 601 s / 13,19 GB |
| UG-Normallauf nach 394 s bei 14,3 GB an der RAM-Reißleine abgebrochen; Render OG4 5,6 GB und 107 s je Bild; Kaskade allein 0,45 GB | **unbelegt (nur VERLAUF)** | Mechanismus am Code bestätigt (§ 6.7), Zahlen nicht nachgemessen; **2f (§ 18):** Render OG4 nachgemessen 5,61 GB / 108 s je Bild, Kaskade 0,45 GB |
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
   **→ 2g (§ 20.4): gemessen, offen (Owner-Frage)**
2. O-05 / § 6.7 — Render-RAM der Prüfstrecke (8 Render-Aufrufe, doppelte Kaskade) **[2f]** · Selman **→ erledigt (§ 18)**
3. N-03 / § 6.8 — Leuchten in LIFT/SCHACHT · Leonis, **nur melden**

**P1 — eigene Lane (Selman), nach Hebel**

4. O-04 — `keine_wand_entities`, `seite_fehlt`, `sanitaer_befund` in `bericht.md` (erlaubte `plan_pruefen`-Änderung) **→ erledigt (2a, § 20.1)**
5. R-05 a — Raster-Reißleine der R-Stufe, Verlust als Warnung statt `print` **→ erledigt (2f, § 20.2)**
6. F-03 — Ausgänge an Türen `von_raum == nach_raum` (Barawitzka: einziger `final_exit`; `stair_exit` im Stiegenhaus) **→ diagnostiziert, offen: S4c-Gebiet (§ 20.5)**
7. D-04 — mm-Faktor und Quelle ausweisen (8 von 13 über `$INSUNITS`, Türprobe widerspricht 4×); Hard Stop = Owner-Frage;
   S-MST nach dem Merge **→ Ausweisen erledigt (§ 20.3), Hard Stop offen**
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

## 12. Punkt 2a — Warnung und Weiterlauf (teilweise erledigt; **Review 1: Abbruch bei defekter Koordinate offen, § 15**)

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
- **Review 1 (§ 15, R1-01):** eine `nan`/`inf`- oder Phantom-Koordinate auf einem Wand-Layer bricht `parse` weiter ab
  (`footprint.py:79`/`:80`) — 2a gilt für „defekte Entities" nicht. P0 · Selman.
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

---

## 14. Punkt 2c — Kippende Türrollen nach K4 (erledigt mit dem Commit dieses Eintrags)

**Auftrag (Owner 2026-09-30):** die nach K4 netto kippenden korrigierten Rollen je Tür aufschlüsseln, je Fall
„zu Recht" (S7c: Wohnungseingang an der Grenze privat|Erschließung, Zimmertür innerhalb einer Wohnung) oder
„fälschlich" (Tür zwischen zwei Räumen derselben Wohnung wird Wohnungseingang; Tür zu `KEIN_RAUM`/`AUSSEN`;
Loch-Raum-Artefakt Option W), nur die fälschlichen beheben; keine Notlicht-Verluste.

**Ausgangswert nachgemessen.** Quelle der 270: die erweiterten Läufe des K4-Berichts, vor K4 `f682c77` ↔ nach dem
K4-Nachzug `bdbbd00`, 23 Geschosse (Mollgasse 8, Muthgasse E2–E9, Rennweg 7), Tür für Tür ausgewertet:
**270 Türen, alle `zimmertuer` → `wohnungseingang`** — nur diese eine Richtung, nicht „in beide Richtungen"
(§ 6.4 berichtigt). Muthgasse 260 (E2 22, E3 43, E4 42, E5 43, E6 40, E7 25, E8 29, E9 16), Mollgasse 10 (DG 8,
3.OG 2) — wie `docs/SLICES_K1_K4.md:1358-1359`. Auf dem Kopf vor 2c (`2016268`, eigene Läufe je Plan allein)
dieselben 270 Türen (Plan, ID, Seiten, rohe Rolle gleich; nur die `top_n`-Nummern in Muthgasse E5/E6/E7 um
neu zugeordnete Türen verschoben). Dieselbe Wirkung außerhalb der 23 K4-Geschosse (K4 hat diese Pläne nicht
gemessen): Barawitzka EG 3, Am Rain EG 2, Am Rain OG2 2 — zusammen **277** auf 31 gemessenen Plänen.

**Mechanismus (am Code):** ein Loch-Raum (`loch_raeume`, `wohnungsklasse.py:468`: GANG/VORRAUM, vom Stiegenhaus
über keine Tür erreichbar — Owner 2026-09-21 „Tür- oder Raumerkennungsloch") ist nach rohen Türen Mitglied einer
Wohnung (E3/G1.2 2026-09-22: über eine rohe Zimmertür gebunden; R1 2026-09-22: der Loch-GANG bildet mit den
Einzelräumen hinter seinen rohen Wohnungseingängen eine Wohnung). Vor K4: Klasse offen → `wohnungsraeume` zählt
ihn privat (Loch-Regel) → seine Innentüren sind korrigiert `zimmertuer`. K4 macht ihn `WOHNUNG_PRIVAT`; die
Ankerregel bestätigt ihn nicht („über keine Tür erreichbar") → `unbestaetigt_privat` → Option W zählt ihn als
Erschließung → **jede Tür zu einem eigenen Zimmer wird korrigiert `wohnungseingang`** (`korrigierte_rollen`,
Zweig `a != b`).

**Befund je Tür (alle 277 gemessen):** Loch-Seite GANG/VORRAUM, Klasse `WOHNUNG_PRIVAT` (K4), Flags 11, nicht
`bestaetigt_privat`; Nachbarseite KÜCHE 81, BAD 77, ZIMMER 47, ABSTELLRAUM 39, WC 33 — alle `WOHNUNG_PRIVAT`,
Flags 00, **dieselbe `wohnung_id` wie der Loch-Raum**. Rohe Rolle `zimmertuer` 272, `wohnungseingang` 5 (R1-Loch-GANG
Mollgasse DG `raum_13` 3, 3.OG `raum_48` 2); 251 blattlose Durchgänge, 26 mit Blatt. Tür zu `KEIN_RAUM`/`AUSSEN`: 0.
Keine dieser Türen startet ein Fluchtweg-Segment (0 `seg_graph_<tür>` vor und nach 2c).

**Urteil: 277 fälschlich, 0 zu Recht.** Regelbezug: S7c (Owner 2026-09-26, `korrigierte_rollen`-Docstring
`wohnungsklasse.py:704-739`): „Eine Zimmertür oder ein Wohnungseingang zwischen zwei Räumen der Wohnungsmenge ist
eine Zimmertür", Wohnungseingang ausschließlich an der Grenze privat|Erschließung; Grundsatz (b): beide Seiten liegen
nach rohen Türen in derselben Wohnung. Die Tür ist also innen, der Wohnungseingang fälschlich — Loch-Raum-Artefakt
Option W: Option W (Runde 5, „wer Notlicht behält, behält seine Zirkulation") meint den Raum mit Zirkulation vom
Stiegenhaus (Rennweg DG1 `raum_8`, `test_unbestaetigt_privater_flur_behaelt_eingang_und_weg`); ein Loch-Raum hat
keine. Bei den 5 R1-Türen ist `wohnungseingang` zugleich die rohe Rolle — R1 hat Gang und Einzelräume aber zu
einer Wohnung gebunden, S7c macht die Tür darum zur Zimmertür (wie vor K4).

**Fix** (`wohnungsklasse.py:wohnungsraeume`, `:481-509`): der Loch-Raum zählt für die korrigierten Rollen privat,
ob unbestimmt oder von K4 unbestätigt privat — `loch = ((unbestimmt | weich) - kand) & loch_raeume(…)` (`:505`),
Erschließung = allgemein ∪ ((unbestimmt ∪ unbestätigt privat) − Loch). Sonst unverändert: Klasse (K4 bleibt
privat), Flags, `bestaetigt_privat`, `wohnung_id`, Option W für Nicht-Loch-Räume (Rennweg DG1 `raum_4`, DG2
`raum_1` — blattlos getrennt, kein Loch —, Schritt-2-Flure), S4c (Barawitzka `tuer_17`/`_23`/`_27` unverändert
`wohnungseingang`, § 6.1). Einbahn unverändert: liest Klasse, rohe Rollen, Ankerregel; `bilde_wohnungen` liest
keine korrigierte Rolle. Unbestimmte Loch-Räume ohne Bindung gibt es hier nicht (`wohnungen.py:205` setzt sie
`ALLGEMEIN_ERSCHLIESSUNG`, K4 sieht sie nicht). **Lesart zur Owner-Bestätigung:** beantwortet K4-Frage 2
(`docs/SLICES_K1_K4.md:1184-1191`) mit „der K4-private Loch-Raum zählt für `wohnungsraeume` weiter als privat,
wie vor K4".

**Tests:** `tests/raumerkennung/test_k4_klasse_umriss.py::test_k4_privater_loch_raum_innentueren_bleiben_zimmertuer`
`[loch-vorraum|r1-loch-gang]` (synthetisch: Loch-VORRAUM mit rohen Zimmertüren; Loch-GANG nach R1 mit rohen
Wohnungseingängen; je Vorbedingung K4 privat, nicht bestätigt, Flags 11, eine Wohnung) und
`tests/naht/test_k4_klasse_gang_vorraum.py::test_k4_loch_raum_innentuer_bleibt_zimmertuer` (echte Parse-Läufe,
Tür über ihre Lage): Mollgasse DG `tuer_12` (`raum_9` VORRAUM ↔ ZIMMER, roh `zimmertuer`), DG `tuer_6`
(`raum_13` R1-GANG ↔ ZIMMER, roh `wohnungseingang`), 3.OG `tuer_43` (`raum_48` R1-GANG ↔ ZIMMER, roh
`wohnungseingang`). `tests/plaene.py`: `MOLLGASSE_DG` (getrackt).

**Rot vor dem Fix** (`pytest tests/raumerkennung/test_k4_klasse_umriss.py tests/naht/test_k4_klasse_gang_vorraum.py
-k innentuer --tb=line`, Kopf `2016268` + Tests, Kurzform — alle Vorbedingungen grün, rot nur die Rolle):

```
test_k4_klasse_umriss.py:226: AssertionError: {'tz': 'wohnungseingang', 'tb': 'wohnungseingang'}   [loch-vorraum]
test_k4_klasse_umriss.py:226: AssertionError: {'tz': 'wohnungseingang', 'tb': 'wohnungseingang'}   [r1-loch-gang]
test_k4_klasse_gang_vorraum.py:117: AssertionError: tuer_12   (assert 'wohnungseingang' == 'zimmertuer')
test_k4_klasse_gang_vorraum.py:117: AssertionError: tuer_6
test_k4_klasse_gang_vorraum.py:117: AssertionError: tuer_43
5 failed, 26 deselected in 78.51s
```

**Grün nach dem Fix:** `test_k4_klasse_umriss.py`, `test_wohnungsklasse.py`, `test_k4_klasse_gang_vorraum.py`
307 passed (87,8 s).

**Nachher** (Runner je Plan allein; Vorher = Nachher 2b bzw. eigene Läufe auf `2016268`, Nachher = Arbeitsbaum
dieses Commits; 31 Pläne: die 17 aus § 13, Mollgasse 2.OG/3.OG/4.OG/DG, Muthgasse E3–E9, Am Rain OG1–OG3):

| | vorher (`2016268`) | nachher (2c) |
|---|--:|--:|
| gekippte Rollen, Urteil **fälschlich** (23 K4-Geschosse / andere Pläne) | **277** (270 / 7) | **0** |
| gekippte Rollen, Urteil **zu Recht** | 0 | 0 |
| korrigierte Rollen ≠ vor K4 (`f682c77`) auf den 23 K4-Geschossen | 278 | 8 (nicht aus K4, s. u.) |

Je Plan geändert (nur `wohnungseingang` → `zimmertuer`): Muthgasse E2 22, E3 43, E4 42, E5 43, E6 40, E7 25, E8 29,
E9 16; Mollgasse DG 8, 3.OG 2; Barawitzka EG 3; Am Rain EG 2, OG2 2. Die übrigen 18 Pläne: keine Rolle geändert.

**Δ auf 31 Plänen** (Vergleich des Runner-JSON): Fluchtweg-Segmente neu/weg/geändert 0/0/0; Anker 0/0/0;
Notlicht-Flags 0 Wechsel; Nutzungsklassen 0; `bestaetigt_privat` +0/−0; Räume, Türen (roh), Ausgänge, Stiegenhäuser,
Bounds unverändert; **Leuchten** (Default-Platzierung, Art und Lage je Leuchte) auf 31/31 gleich.
**Fluchtweg-Warnungen −4, +0:** Barawitzka EG „kein final_exit erreichbar von Tür `durchgang_11` (Endraum
`raum_25`)", `tuer_19` (`raum_17`), `tuer_29` (`raum_10`); Am Rain EG `durchgang_62` (`raum_102`) — je „Türgraph endet
vor dem Ausgang", je an einer Innentür eines Loch-VORRAUMS (`raum_9` bzw. `raum_98`), die nur als falscher
Wohnungseingang Startpunkt war. Der Loch-Raum selbst bleibt als `loch:`-Zeile im Bericht (Wohnungsklasse-Warnungen
unverändert). Keine Notlicht-Verluste: Flags und `bestaetigt_privat` unverändert → kein STOPP.
**Prüfstrecke:** `plan_pruefen._fachteil3` listet in der Fluchtweg-Auskunft jede korrigierte `wohnungseingang`-Tür
(`scripts/plan_pruefen.py:1281-1292`); auf den Prüfplänen entfallen dort Muthgasse E2 22, Barawitzka 3, Am Rain
EG 2 und OG2 2 Zeilen (Luftlinie ohne Weg). `Projekte/_ergebnis/` nicht neu erzeugt (wie 2a/2b).

**Die 8 Rollen-Unterschiede gegen `f682c77`, die nicht aus K4 kommen** (unverändert gelassen): Muthgasse E5 `tuer_30`,
`tuer_46`, E6 `tuer_31`, E7 `tuer_36` (vor K4 Seite `KEIN_RAUM` ohne Rolle, heute Zimmertür zwischen zwei Räumen
derselben Wohnung), Rennweg OG3 `tuer_2` (heute `balkontuer` BALKON ↔ ZIMMER), Rennweg DG2 `durchgang_2`, `_3`, `_6`
(Türseiten/rohe Rollen seit `f682c77` anders zugeordnet) — Folgen späterer Slices an Türseite und roher Rolle.

**Einzelliste** — die 277 Türen je Loch-Raum (Plan, Loch-Raum, jede Innentür mit Nachbarraum und roher Rolle,
korrigierte Rolle vor K4 → `2016268` → 2c; `zt` = `zimmertuer`, `we` = `wohnungseingang`, `n. g.` = vor K4 nicht
gemessen). Loch-Seite überall GANG/VORRAUM, Klasse `WOHNUNG_PRIVAT` (K4), Flags 11, nicht bestätigt; Nachbar überall
`WOHNUNG_PRIVAT`, Flags 00, dieselbe Wohnung (Stand `2016268`, `top_n` dieses Stands):

| Plan | Loch-Raum (Typ, m², Wohnung; Klasse K4 privat, Flags 11) | Innentür → Nachbar (Typ; rohe Rolle `zimmertuer`, sonst genannt) | korrigiert: vor K4 → 2016268 → 2c | Urteil |
|---|---|---|---|---|
| Muthgasse E2 | `raum_48` VORRAUM 11,91, top_17 | `durchgang_6` ZIMMER, `durchgang_8` KÜCHE, `durchgang_9` ABSTELLRAUM | 3× zt → we → zt | fälschlich |
| Muthgasse E2 | `raum_51` VORRAUM 9,07, top_16 | `durchgang_52` KÜCHE, `durchgang_54` WC, `durchgang_55` BAD | 3× zt → we → zt | fälschlich |
| Muthgasse E2 | `raum_54` VORRAUM 11,56, top_14 | `durchgang_41` ABSTELLRAUM, `durchgang_42` WC, `durchgang_43` BAD, `durchgang_45` KÜCHE, `durchgang_57` ZIMMER, `tuer_32` BAD, `tuer_89` WC | 7× zt → we → zt | fälschlich |
| Muthgasse E2 | `raum_57` VORRAUM 13,10, top_13 | `durchgang_38` WC, `durchgang_40` BAD, `durchgang_58` ZIMMER, `durchgang_59` ZIMMER, `durchgang_61` KÜCHE | 5× zt → we → zt | fälschlich |
| Muthgasse E2 | `raum_59` VORRAUM 10,92, top_4 | `durchgang_10` ZIMMER, `durchgang_62` KÜCHE, `durchgang_63` BAD | 3× zt → we → zt | fälschlich |
| Muthgasse E2 | `raum_80` VORRAUM 4,73, top_15 | `durchgang_47` KÜCHE | 1× zt → we → zt | fälschlich |
| Muthgasse E3 | `raum_22` VORRAUM 5,06, top_11 | `durchgang_25` KÜCHE, `durchgang_27` BAD, `durchgang_28` ABSTELLRAUM | 3× zt → we → zt | fälschlich |
| Muthgasse E3 | `raum_64` VORRAUM 4,18, top_6 | `durchgang_19` KÜCHE, `durchgang_21` BAD, `durchgang_71` ABSTELLRAUM | 3× zt → we → zt | fälschlich |
| Muthgasse E3 | `raum_67` VORRAUM 9,07, top_5 | `durchgang_43` ZIMMER, `durchgang_45` KÜCHE, `durchgang_73` WC, `durchgang_74` BAD | 4× zt → we → zt | fälschlich |
| Muthgasse E3 | `raum_76` VORRAUM 13,10, top_18 | `durchgang_53` KÜCHE, `durchgang_78` BAD, `durchgang_79` ZIMMER, `durchgang_80` ZIMMER, `durchgang_81` WC, `tuer_39` ZIMMER | 6× zt → we → zt | fälschlich |
| Muthgasse E3 | `raum_80` VORRAUM 15,23, top_22 | `durchgang_82` BAD, `durchgang_83` WC, `durchgang_84` ZIMMER, `durchgang_85` KÜCHE, `durchgang_87` ABSTELLRAUM | 5× zt → we → zt | fälschlich |
| Muthgasse E3 | `raum_84` VORRAUM 13,10, top_2 | `durchgang_89` ZIMMER, `durchgang_91` ZIMMER, `durchgang_92` WC, `durchgang_93` KÜCHE, `tuer_26` ZIMMER | 5× zt → we → zt | fälschlich |
| Muthgasse E3 | `raum_86` VORRAUM 4,73, top_4 | `durchgang_46` KÜCHE, `durchgang_48` BAD | 2× zt → we → zt | fälschlich |
| Muthgasse E3 | `raum_87` VORRAUM 3,62, top_16 | `durchgang_40` BAD, `durchgang_62` KÜCHE | 2× zt → we → zt | fälschlich |
| Muthgasse E3 | `raum_92` VORRAUM 7,06, top_14 | `durchgang_35` ZIMMER, `durchgang_68` BAD, `durchgang_69` KÜCHE, `durchgang_95` ABSTELLRAUM | 4× zt → we → zt | fälschlich |
| Muthgasse E3 | `raum_99` VORRAUM 3,60, top_13 | `durchgang_30` KÜCHE, `durchgang_66` BAD, `durchgang_67` ZIMMER | 3× zt → we → zt | fälschlich |
| Muthgasse E3 | `raum_102` VORRAUM 11,55, top_3 | `durchgang_55` KÜCHE, `durchgang_56` WC, `durchgang_76` BAD, `durchgang_77` ZIMMER, `durchgang_98` ABSTELLRAUM, `tuer_40` BAD | 6× zt → we → zt | fälschlich |
| Muthgasse E4 | `raum_47` VORRAUM 4,18, top_7 | `durchgang_15` KÜCHE, `durchgang_16` BAD, `durchgang_52` ABSTELLRAUM | 3× zt → we → zt | fälschlich |
| Muthgasse E4 | `raum_50` VORRAUM 9,07, top_5 | `durchgang_29` ZIMMER, `durchgang_31` KÜCHE, `durchgang_54` WC, `durchgang_55` BAD | 4× zt → we → zt | fälschlich |
| Muthgasse E4 | `raum_58` VORRAUM 12,90, top_12 | `durchgang_40` KÜCHE, `durchgang_58` BAD, `durchgang_59` ZIMMER, `durchgang_60` ZIMMER, `durchgang_61` WC | 5× zt → we → zt | fälschlich |
| Muthgasse E4 | `raum_60` VORRAUM 4,73, top_4 | `durchgang_32` KÜCHE, `durchgang_34` BAD | 2× zt → we → zt | fälschlich |
| Muthgasse E4 | `raum_64` VORRAUM 5,06, top_8 | `durchgang_18` KÜCHE, `durchgang_62` BAD, `durchgang_63` ABSTELLRAUM | 3× zt → we → zt | fälschlich |
| Muthgasse E4 | `raum_76` VORRAUM 15,23, top_18 | `durchgang_68` BAD, `durchgang_69` WC, `durchgang_70` ZIMMER, `durchgang_71` KÜCHE, `durchgang_72` ZIMMER, `durchgang_73` ABSTELLRAUM | 6× zt → we → zt | fälschlich |
| Muthgasse E4 | `raum_80` VORRAUM 13,10, top_19 | `durchgang_75` ZIMMER, `durchgang_76` BAD, `durchgang_77` KÜCHE, `durchgang_78` ZIMMER, `durchgang_79` WC | 5× zt → we → zt | fälschlich |
| Muthgasse E4 | `raum_98` VORRAUM 7,06, top_21 | `durchgang_87` BAD, `durchgang_88` KÜCHE, `durchgang_90` ABSTELLRAUM | 3× zt → we → zt | fälschlich |
| Muthgasse E4 | `raum_99` VORRAUM 3,60, top_6 | `durchgang_83` KÜCHE, `durchgang_84` BAD, `durchgang_85` ZIMMER | 3× zt → we → zt | fälschlich |
| Muthgasse E4 | `raum_101` VORRAUM 3,62, top_2 | `durchgang_26` BAD, `durchgang_46` KÜCHE | 2× zt → we → zt | fälschlich |
| Muthgasse E4 | `raum_102` VORRAUM 11,55, top_3 | `durchgang_42` KÜCHE, `durchgang_43` WC, `durchgang_57` BAD, `durchgang_91` ABSTELLRAUM, `durchgang_92` ZIMMER, `tuer_44` BAD | 6× zt → we → zt | fälschlich |
| Muthgasse E5 | `raum_6` VORRAUM 3,68, top_15 | `durchgang_6` BAD, `durchgang_7` KÜCHE | 2× zt → we → zt | fälschlich |
| Muthgasse E5 | `raum_45` VORRAUM 5,65, top_10 | `durchgang_47` KÜCHE, `durchgang_48` BAD, `durchgang_49` ABSTELLRAUM | 3× zt → we → zt | fälschlich |
| Muthgasse E5 | `raum_54` VORRAUM 5,65, top_16 | `durchgang_55` KÜCHE, `durchgang_57` BAD, `durchgang_58` ABSTELLRAUM | 3× zt → we → zt | fälschlich |
| Muthgasse E5 | `raum_58` VORRAUM 3,80, top_14 | `durchgang_59` WC, `durchgang_60` KÜCHE, `tuer_34` ZIMMER | 3× zt → we → zt | fälschlich |
| Muthgasse E5 | `raum_61` VORRAUM 3,98, top_14 | `durchgang_53` BAD, `durchgang_61` KÜCHE | 2× zt → we → zt | fälschlich |
| Muthgasse E5 | `raum_65` VORRAUM 4,36, top_1 | `durchgang_2` KÜCHE, `durchgang_50` BAD, `durchgang_67` ABSTELLRAUM | 3× zt → we → zt | fälschlich |
| Muthgasse E5 | `raum_72` VORRAUM 11,28, top_12 | `durchgang_35` ZIMMER, `durchgang_73` KÜCHE, `durchgang_74` BAD, `durchgang_75` WC, `durchgang_76` ABSTELLRAUM | 5× zt → we → zt | fälschlich |
| Muthgasse E5 | `raum_79` VORRAUM 8,41, top_6 | `durchgang_21` KÜCHE, `durchgang_77` ZIMMER, `durchgang_79` ZIMMER, `durchgang_80` BAD, `durchgang_81` ABSTELLRAUM, `durchgang_82` ABSTELLRAUM, `durchgang_83` KÜCHE | 7× zt → we → zt | fälschlich |
| Muthgasse E5 | `raum_89` VORRAUM 7,00, top_2 | `durchgang_13` ZIMMER, `durchgang_46` BAD, `durchgang_87` ABSTELLRAUM, `durchgang_88` KÜCHE | 4× zt → we → zt | fälschlich |
| Muthgasse E5 | `raum_91` VORRAUM 3,65, top_5 | `durchgang_11` KÜCHE, `durchgang_43` BAD, `durchgang_44` ZIMMER | 3× zt → we → zt | fälschlich |
| Muthgasse E5 | `raum_95` VORRAUM 3,56, top_9 | `durchgang_16` KÜCHE, `durchgang_37` BAD | 2× zt → we → zt | fälschlich |
| Muthgasse E5 | `raum_99` VORRAUM 5,63, top_3 | `durchgang_66` KÜCHE, `durchgang_92` ABSTELLRAUM, `durchgang_93` BAD, `durchgang_94` BAD | 4× zt → we → zt | fälschlich |
| Muthgasse E5 | `raum_108` VORRAUM 4,47, top_4 | `durchgang_23` KÜCHE, `durchgang_25` BAD | 2× zt → we → zt | fälschlich |
| Muthgasse E6 | `raum_42` VORRAUM 5,65, top_10 | `durchgang_41` KÜCHE, `durchgang_42` ABSTELLRAUM, `durchgang_43` BAD | 3× zt → we → zt | fälschlich |
| Muthgasse E6 | `raum_53` VORRAUM 4,36, top_1 | `durchgang_2` KÜCHE, `durchgang_44` BAD, `durchgang_55` ABSTELLRAUM | 3× zt → we → zt | fälschlich |
| Muthgasse E6 | `raum_60` VORRAUM 11,28, top_13 | `durchgang_34` ZIMMER, `durchgang_61` KÜCHE, `durchgang_62` BAD, `durchgang_63` WC | 4× zt → we → zt | fälschlich |
| Muthgasse E6 | `raum_67` VORRAUM 8,41, top_8 | `durchgang_21` KÜCHE, `durchgang_65` BAD, `durchgang_66` ABSTELLRAUM, `durchgang_67` WC | 4× zt → we → zt | fälschlich |
| Muthgasse E6 | `raum_77` VORRAUM 3,98, top_15 | `durchgang_70` BAD, `durchgang_71` KÜCHE | 2× zt → we → zt | fälschlich |
| Muthgasse E6 | `raum_78` VORRAUM 3,80, top_15 | `durchgang_47` WC, `durchgang_72` KÜCHE, `tuer_28` ZIMMER | 3× zt → we → zt | fälschlich |
| Muthgasse E6 | `raum_83` VORRAUM 5,63, top_16 | `durchgang_53` KÜCHE, `durchgang_75` BAD, `durchgang_76` BAD, `durchgang_77` ABSTELLRAUM | 4× zt → we → zt | fälschlich |
| Muthgasse E6 | `raum_86` VORRAUM 3,68, top_9 | `durchgang_8` KÜCHE, `durchgang_78` WC, `durchgang_79` BAD | 3× zt → we → zt | fälschlich |
| Muthgasse E6 | `raum_95` VORRAUM 3,65, top_5 | `durchgang_12` KÜCHE, `durchgang_82` ZIMMER, `durchgang_84` BAD | 3× zt → we → zt | fälschlich |
| Muthgasse E6 | `raum_101` VORRAUM 7,00, top_2 | `durchgang_86` ZIMMER, `durchgang_87` KÜCHE, `durchgang_88` BAD, `durchgang_89` ABSTELLRAUM | 4× zt → we → zt | fälschlich |
| Muthgasse E6 | `raum_108` VORRAUM 3,56, top_3 | `durchgang_17` KÜCHE, `durchgang_69` BAD | 2× zt → we → zt | fälschlich |
| Muthgasse E6 | `raum_109` VORRAUM 4,47, top_4 | `durchgang_23` BAD, `durchgang_26` KÜCHE | 2× zt → we → zt | fälschlich |
| Muthgasse E6 | `raum_110` VORRAUM 5,65, top_6 | `durchgang_49` KÜCHE, `durchgang_51` BAD, `durchgang_52` ABSTELLRAUM | 3× zt → we → zt | fälschlich |
| Muthgasse E7 | `raum_23` VORRAUM 4,47, top_1 | `durchgang_13` KÜCHE | 1× zt → we → zt | fälschlich |
| Muthgasse E7 | `raum_33` VORRAUM 5,65, top_9 | `durchgang_33` KÜCHE, `durchgang_35` BAD, `durchgang_36` ABSTELLRAUM | 3× zt → we → zt | fälschlich |
| Muthgasse E7 | `raum_37` VORRAUM 3,98, top_8 | `durchgang_37` BAD, `durchgang_38` KÜCHE | 2× zt → we → zt | fälschlich |
| Muthgasse E7 | `raum_44` VORRAUM 11,28, top_5 | `durchgang_21` ZIMMER, `durchgang_43` KÜCHE, `durchgang_44` BAD, `durchgang_45` WC, `durchgang_46` ABSTELLRAUM | 5× zt → we → zt | fälschlich |
| Muthgasse E7 | `raum_51` VORRAUM 8,41, top_14 | `durchgang_9` KÜCHE, `durchgang_47` BAD, `durchgang_48` WC, `durchgang_49` ABSTELLRAUM | 4× zt → we → zt | fälschlich |
| Muthgasse E7 | `raum_66` VORRAUM 3,80, top_8 | `durchgang_31` WC, `durchgang_39` KÜCHE, `tuer_22` ZIMMER | 3× zt → we → zt | fälschlich |
| Muthgasse E7 | `raum_75` VORRAUM 5,63, top_17 | `durchgang_52` KÜCHE, `durchgang_55` BAD, `durchgang_56` BAD, `durchgang_57` ABSTELLRAUM | 4× zt → we → zt | fälschlich |
| Muthgasse E7 | `raum_82` VORRAUM 3,68, top_18 | `durchgang_60` KÜCHE, `durchgang_62` WC, `durchgang_63` BAD | 3× zt → we → zt | fälschlich |
| Muthgasse E8 | `raum_27` VORRAUM 4,47, top_2 | `durchgang_12` BAD, `durchgang_15` KÜCHE, `tuer_5` WC | 3× zt → we → zt | fälschlich |
| Muthgasse E8 | `raum_37` VORRAUM 5,65, top_6 | `durchgang_36` KÜCHE, `durchgang_38` BAD, `durchgang_39` ABSTELLRAUM | 3× zt → we → zt | fälschlich |
| Muthgasse E8 | `raum_41` VORRAUM 3,98, top_5 | `durchgang_40` BAD, `durchgang_41` KÜCHE | 2× zt → we → zt | fälschlich |
| Muthgasse E8 | `raum_44` VORRAUM 3,80, top_5 | `durchgang_34` WC, `durchgang_42` KÜCHE, `tuer_22` ZIMMER | 3× zt → we → zt | fälschlich |
| Muthgasse E8 | `raum_50` VORRAUM 11,28, top_2 | `durchgang_23` ZIMMER, `durchgang_47` KÜCHE, `durchgang_48` BAD, `durchgang_49` WC, `durchgang_50` ABSTELLRAUM, `tuer_8` WC | 6× zt → we → zt | fälschlich |
| Muthgasse E8 | `raum_57` VORRAUM 8,41, top_2 | `durchgang_11` KÜCHE, `durchgang_51` BAD, `durchgang_52` WC, `durchgang_53` BAD, `tuer_9` WC | 5× zt → we → zt | fälschlich |
| Muthgasse E8 | `raum_76` VORRAUM 5,63, top_11 | `durchgang_8` KÜCHE, `durchgang_66` BAD, `durchgang_67` BAD, `durchgang_68` ABSTELLRAUM | 4× zt → we → zt | fälschlich |
| Muthgasse E8 | `raum_83` VORRAUM 3,88, top_13 | `durchgang_71` KÜCHE, `durchgang_73` ABSTELLRAUM, `durchgang_74` BAD | 3× zt → we → zt | fälschlich |
| Muthgasse E9 | `raum_13` VORRAUM 11,28, top_1 | `durchgang_13` BAD, `durchgang_14` KÜCHE, `durchgang_16` BAD, `durchgang_17` ZIMMER, `durchgang_18` ABSTELLRAUM | 5× zt → we → zt | fälschlich |
| Muthgasse E9 | `raum_18` VORRAUM 4,47, top_3 | `durchgang_21` BAD, `durchgang_22` KÜCHE | 2× zt → we → zt | fälschlich |
| Muthgasse E9 | `raum_23` VORRAUM 8,41, top_5 | `durchgang_23` KÜCHE, `durchgang_25` ZIMMER, `durchgang_27` ZIMMER, `durchgang_29` WC, `durchgang_30` BAD, `durchgang_31` ABSTELLRAUM, `durchgang_32` KÜCHE | 7× zt → we → zt | fälschlich |
| Muthgasse E9 | `raum_38` VORRAUM 3,72, top_7 | `durchgang_37` ABSTELLRAUM, `durchgang_38` KÜCHE | 2× zt → we → zt | fälschlich |
| Mollgasse DG | `raum_9` VORRAUM 9,10, top_7 | `tuer_12` ZIMMER, `tuer_14` WC, `tuer_15` ABSTELLRAUM, `tuer_16` ZIMMER, `tuer_34` KÜCHE | 5× zt → we → zt | fälschlich |
| Mollgasse DG | `raum_13` GANG 3,44, top_4 | `tuer_6` ZIMMER (roh `wohnungseingang`), `tuer_7` ZIMMER (roh `wohnungseingang`), `tuer_27` ABSTELLRAUM (roh `wohnungseingang`) | 3× zt → we → zt | fälschlich |
| Mollgasse 3.OG | `raum_48` GANG 4,58, top_21 | `tuer_43` ZIMMER (roh `wohnungseingang`), `tuer_45` BAD (roh `wohnungseingang`) | 2× zt → we → zt | fälschlich |
| Barawitzka EG | `raum_9` VORRAUM 5,59, top_1 | `durchgang_11` KÜCHE, `tuer_19` WC, `tuer_29` BAD | 3× n. g. → we → zt | fälschlich |
| Am Rain EG | `raum_81` VORRAUM 8,79, top_39 | `durchgang_61` KÜCHE | 1× n. g. → we → zt | fälschlich |
| Am Rain EG | `raum_98` VORRAUM 18,86, top_1 | `durchgang_62` KÜCHE | 1× n. g. → we → zt | fälschlich |
| Am Rain OG2 | `raum_49` VORRAUM 2,97, top_22 | `durchgang_29` KÜCHE, `tuer_202` BAD | 2× n. g. → we → zt | fälschlich |

**Volle Suite:** (allein, 30 min 15 s): `6 failed, 2237 passed, 11 skipped, 6 deselected, 15 xfailed` — dieselben 6
roten wie nach 2b (3 × `test_keine_leuchten_in_wohnung_privat` OG1/OG2/DG1 = Board 1 Leonis,
`test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell`, die 2 S4c-Pins), 2237 = 2232 + 5 neue,
15 xfailed wie nach 2b, 0 xpassed. Kein Test umgestellt, keine Schwelle, kein Soll, kein xfail-Marker angefasst.

**Gate:** `pytest -m gate tests/gate` 3 passed, 1 xfailed (wie vorher). `gate_messung` auf dem Arbeitsbaum dieses
Commits (vor dem Commit, `_arbeit/gate/messung_2016268-dirty-2c.json`, 60,5 s), `pruefe_gate` gegen
`nullmessung_f15d03f.json`: (0) unsauberer Arbeitsbaum (erwartet, vor dem Commit gemessen) und **(3) `M4.einraum`
DG2 0 → 1** (Enis Board 3, unverändert); M17 18/18 BESTANDEN; OG3 0 Anker in `WOHNUNG_PRIVAT`; DG1 2 Ausgänge,
0 durch den Liftschacht; Barawitzka ABSTELLRAUM 1 Verbindung. Alle Messfelder außer `meta` gleich der 2b-Messung.

**Offen nach 2c:**
- **Owner-Bestätigung der Lesart** (K4-Frage 2): der K4-private Loch-Raum zählt für die korrigierten Rollen privat
  wie vor K4; Option W bleibt für Räume mit Zirkulation vom Stiegenhaus. P1 · Selman (Owner).
- **Die Loch-Räume selbst** bleiben Tür- oder Raumerkennungslöcher (Wohnungseingang fehlt im Modell): 81 Loch-Räume
  in der Einzelliste (Muthgasse 74, Mollgasse DG 2 / 3.OG 1, Barawitzka EG 1, Am Rain EG 2 / OG2 1);
  ihr Notlicht bleibt (Flags 11). Ursache Türerkennung, Messfall S4c/S3b. P1 · Selman.
- Die 8 Rollen-Unterschiede gegen `f682c77`, die nicht aus K4 kommen (oben), sind nicht bewertet. P2 · Selman.
- S4c unverändert (§ 6.1): Barawitzka `tuer_17`/`_23`/`_27` bleiben planwidrig `wohnungseingang`, die 2 Pins rot.
- Naht: die Platzierung liest weiter die rohe Rolle (§ 6.4, N-04). P1 · Contract / Leonis.

---

## 15. Review 1 — Punkte 2a–2c (adversarial, Kopf `27de6a0`)

Geprüft mit eigenem Code: eigener Runner (`provider.parse(dxf, "")`, je Plan allein), 17 eigene Defekt-DXF,
Plan-Ausschnitte, Vergleich gegen die Basisläufe `0434392` (§ 7). Runner, DXF, JSON und Bilder liegen im
Session-Scratch, nicht im Repo.

**(1) Diff `0434392..27de6a0`:** `src/notbeleuchtung/raumerkennung/` (`ausgaenge`, `dxf_load`, `fluchtweg`,
`provider`, `wohnungsklasse`), `scripts/plan_pruefen.py` (nur Warnungen in bericht.md), Tests, `tests/plaene.py`
(+ `MOLLGASSE_DG`), `LUECKEN.md`. Kein Contract, kein fremdes Paket, kein Owner-Import, keine lokalen Pfade. Tests nur
ergänzt (einzige geänderte Zeile: Import in `test_k4_klasse_gang_vorraum.py`); keine Schwelle, kein Soll, kein Marker
gelockert; neu genau ein strict-xfail (S4g a, § 13). Je Punkt ein Commit (`b849dd0`, `2016268`, `27de6a0`) mit
Rot-Nachweis im Eintrag; die zitierten Zeilennummern stimmen mit den Testdateien überein.

**(2) 2a — eigene Defekt-DXF** (`parse(…, "EG")` je Plan in einem eigenen Prozess):

| Fall | Ergebnis |
|---|---|
| leer; nur TEXT/MTEXT | 0 Räume, `keine_geometrie` + `keine_raeume` |
| nur Linien auf Layer `0` | 0 Räume, `keine_wand_entities` + `keine_raeume` |
| nur offene Wandlinien (`A-WALL`, 12 Stück) | 0 Räume, `keine_raeume` |
| nur kaputte Polylinien (LWPOLYLINE mit 0/1 Punkt, geschlossen-degeneriert, POLYLINE ohne VERTEX) | 0 Räume, `keine_raeume` |
| gültiger Raum + LWPOLYLINE 0/1 Punkt, POLYLINE ohne VERTEX, LWPOLYLINE-Zählerfehler (90 = 5, 2 Punkte), selbstschneidende Polylinie mit HATCH, degenerierter HATCH-Rand, ARC Radius 0 / Winkel 0, INSERT auf gelöschten Block | RaumModell mit Räumen, kein Abbruch, **keine Warnung** |
| abgeschnittene Datei; Binärdaten | `DxfNichtLesbar` (gewollter Abbruch) |
| **gültiger Raum + LWPOLYLINE mit `nan`/`inf`-Koordinate auf `A-WALL`** | **Abbruch** `OverflowError` `footprint.py:79` |
| **gültiger Raum + LWPOLYLINE mit Phantom-Punkt (1e15, 1e15) auf `A-WALL`** | **Abbruch** `ValueError` `footprint.py:80` |

Beleg (pytest-Lauf eines Scratch-Tests über die 11 Entity-Fälle, `--tb=line`, Kurzform):

```
footprint.py:79: OverflowError: cannot convert float infinity to integer                  [d14_raum_lwpoly_nan]
footprint.py:80: ValueError: array is too big; `arr.size * arr.dtype.itemsize` is larger
                 than the maximum possible size.                                          [d11_raum_riesenkoordinate]
2 failed, 9 passed in 1.42s
```

Ursache: `bounds_mm` (`dxf_load.py:258-268`) nimmt min/max über alle Wand-Stützpunkte ohne Endlichkeits- oder
Fern-Prüfung (der 500-m-Fern-Filter sitzt nur in `wandkoerper._ohne_fernkoerper`); `footprint.gebaeude_umriss`
rastert diese Bounds mit 200 mm (`footprint.py:78-80`). Die Stelle ist älter als 2a. `plan_pruefen.plan_pruefen`
auf vier der Pläne (leer, nur Linien Layer `0`, offene Wandlinien, nur kaputte Polylinien; Ausgabe über
`PLAN_PRUEFEN_ERGEBNIS` in den Scratch): Lauf ohne Abbruch, bericht.md „## Warnungen" mit `keine_geometrie` bzw.
`keine_wand_entities` und `keine_raeume` wie in § 12 behauptet.

**Urteil 2a: teilweise widerlegt.** Leer, nur Text, nur Linien und degenerierte Polylinien laufen durch; eine
nicht-endliche oder ferne Koordinate bricht weiter ab. Nicht behoben: die Abhilfe ist ein Entscheid (Entity mit
nicht-endlicher Koordinate beim Laden verwerfen, oder Bounds/Raster mit Fern-Filter bzw. Raster-Reißleine); eine
Bounds-Änderung verschiebt `footprint.hauptausgaenge` auch auf echten Plänen (Muthgasse E2 Bounds 503,8 × 275,9 m,
§ 7). → R1-01.

**(3) 2b:** Basis `0434392` gegen `27de6a0`, eigene Läufe auf 13 Plänen (12 Prüfpläne + Rennweg OG3 aus
`_eingang`): **0 Ausgänge entfallen, 0 neu** (ID, Typ, Lage); kein Geschoss hat seinen Ausgang verloren.
Mollgasse EG: `exit_tuer_67` `final_exit` (`AUSSEN`\|`raum_61` TERRASSE, `ist_notausgang`), `exit_tuer_68`
`stair_exit`; `exit_1` … `exit_4` unverändert und an der Lage aus § 13 (`exit_2` 8 mm neben `raum_30` MÜLLRAUM,
`exit_3` in `raum_51`, `exit_4` in `raum_41`). `markiere_windfang` setzt `ist_notausgang` ohne Blick auf die Rolle
(`tuer_typisierung.py:276`) — die Begründung für b stimmt. Gate (11) DG1 grün (s. (5)). **Urteil 2b: bestätigt**
(b und c erledigt, a offen wie § 13).

**(4) 2c:** korrigierte Rollen Basis gegen `27de6a0` auf den 13 Plänen: 25 gekippt (Muthgasse E2 22, Barawitzka
EG 3), alle `wohnungseingang` → `zimmertuer`. Alle 25 selbst beurteilt — die ganze Menge statt einer Stichprobe; einen
„zu Recht"-Fall gibt es auf diesen Plänen nicht, zehn davon zu ziehen war darum nicht möglich:

- beide Seiten dieselbe `wohnung_id`; Nachbar ZIMMER/KÜCHE/BAD/WC/ABSTELLRAUM mit Flags 00, Loch-Seite VORRAUM mit
  Flags 11;
- Muthgasse E2 `raum_48`, `raum_51`, `raum_57`, `raum_59` haben einen rohen Wohnungseingang zum
  `ALLGEMEIN_ERSCHLIESSUNG`-GANG (`tuer_13`, `tuer_7`, `tuer_3`, `tuer_12` → `raum_46`/`raum_96`), der
  `wohnungseingang` bleibt — die gekippten Türen liegen dahinter;
- Plan angesehen: Muthgasse E2 `raum_54` trägt den Stempel „E2-5-01 Vorraum 11,56 m²"; seine sieben gekippten Türen
  führen zu Räumen mit Stempeln „E2-5-…" (Bad, WC, AR, Zimmer, Wohnküche); der Zugang von außen ist `tuer_9` (Seite
  `KEIN_RAUM`, Türtext „T-E2-5-07-1" daneben). Barawitzka `raum_9` trägt „02 VR 5,59 m²" (Text „TOP 02" bei der
  Wohnküche `raum_25`), seine drei gekippten Türen führen zu Bad `raum_10`, WC `raum_17`, Wohnküche `raum_25`.

→ **25 fälschlich, 0 zu Recht** — deckt sich mit § 14. Flags, `bestaetigt_privat`, Nutzungsklassen, `wohnung_id`,
Polygone, Türen (roh), Ausgänge, Segmente, Anker: 13 von 13 Plänen gleich der Basis; Fluchtweg-Warnungen nur
Barawitzka −3 (wie § 14). **Urteil 2c: bestätigt.**

**(5) Gate** auf dem sauberen Kopf (`_arbeit/gate/messung_27de6a0.json`, 104,6 s), `pruefe_gate` gegen
`nullmessung_f15d03f.json`: **nur (3) `M4.einraum` DG2 0 → 1**; M17 18/18 BESTANDEN; DG1 2 Ausgänge, 0 durch den
Liftschacht; alle Messfelder außer `meta` gleich der 2c-Messung. `pytest -m gate tests/gate`: 3 passed, 1 xfailed.
`test_provider.py`, `test_s4g_ausgang_tuerbezug.py`, `test_k4_klasse_umriss.py`, `test_k4_klasse_gang_vorraum.py`,
`test_soll_mollgasse.py`: 53 passed, 1 skipped, 4 xfailed.

**Offen aus Review 1:**
- **R1-01 (P0: Abbruch; auf den 13 Plänen der Prüfstrecke nicht aufgetreten) · Selman:** eine `nan`/`inf`-Koordinate
  auf einem Wand-Layer → `OverflowError` `footprint.py:79`; eine Phantom-Koordinate (1e15) → `ValueError`
  `footprint.py:80` (Raster aus ungefilterten `bounds_mm`). 2a ist für „defekte Entities" damit nicht erfüllt.
  Entscheid offen: Entity mit nicht-endlicher Koordinate beim Laden verwerfen (mit Warnung) und/oder Bounds und Raster
  mit Fern-Filter bzw. Raster-Reißleine (vgl. `rest_komponenten`, § 6.7).
- **R1-02 (P2) · Selman:** degenerierte Entities (Polylinie mit 0/1 Punkt, POLYLINE ohne VERTEX, degenerierter
  HATCH-Rand, ARC Radius 0, INSERT auf fehlenden Block, LWPOLYLINE-Zählerfehler) laufen still durch — kein Abbruch,
  aber auch keine Warnung im Bericht.

---

## 16. Punkt 2d — Freie Flächen in Wohnungen (erledigt mit dem Commit dieses Eintrags)

**Auftrag (Owner 2026-09-30):** „Innerhalb eines Wohnungsumrisses gibt es keine freie Fläche ohne Raum." Jede freie
Fläche > 2 m² im Wohnungsumriss: Öffnung zum Nachbarraum ohne Türblatt = kein Trenner → die Fläche geht in diesen Raum
(mehrere: die breiteste entscheidet; nicht eindeutig → eigener Raum UNBEKANNT mit Grund); Tür mit Blatt = Trenner →
eigener Raum UNBEKANNT. Grundsatz (b): die Fläche erbt die Wohnung nur über den aufnehmenden Raum, ein neuer Raum
bekommt keine `wohnung_id`.

**Definition (festgelegt):**

- **Freie Fläche** = gedeckte Kontur − alle Räume − Wandkörper, je Zusammenhangskomponente > 2 m²
  (`freiflaeche.py:freie_flaechen`). Gedeckte Kontur = `kontur` im Provider (`aussen.gedeckt()`, sonst
  `aussenkontur`) — dieselbe Fläche, die die Türzuordnung als „nicht AUSSEN" liest. Wandkörper = `wand_union`.
  Vorher morphologisch geöffnet um ±150 mm (Streifen < 300 mm sind Raster-Splitter zwischen Raum und Wand; F-/R-Räume
  liegen auf 50 mm, die R-Stufe frisst 100 mm), danach die Zähne der Rasterränder bis 100 mm wieder angefügt.
  Begründung: die **Deckenplatte** gibt es nur in der Rennweg-Familie (`New_035 Decken`, Block `Slab_1`); auf DG1
  237,0 m² gegen 234,1 m² gedeckte Kontur, beide decken das Feld zu 100 %, das Feld nach beiden Bezügen 16,91 bzw.
  16,94 m² (symmetrische Differenz 0,05 m²). Der **±250-mm-Wohnungsumriss** allein deckt das Feld zu 0 % (Kerbe am
  Rand von `top_1`, unten Fassade mit Fensterlücken), `aussenkontur(d=1000)` zu 3,7 %.
- **Im Wohnungsumriss** (`_wohnung`): `umschliessende_wohnung` (alle Nachbarräume bis 500 mm in einer Wohnung;
  Schacht/Lift/Freiflächen zählen nicht — gebaut für genau diese Fassadenkerben, `wohnungsumriss.py` Modul-Doc) oder
  ≥ 98 % (`VOLL`) im ±250-mm-Umriss genau einer Wohnung. Alles andere bleibt frei.
- **Öffnung** (`_grenzen`): Rand der Fläche bis 100 mm am Nachbarraum minus Wandkörper (±1 mm), Länge
  ≥ 0,797 m = `_DURCHGANG_MIN_MM` (800) − 3 mm — dieselbe Mindestbreite und Toleranz wie der Durchgang ohne
  Türblatt (`tuer_zuordnung.durchgaenge_ohne_tuerblatt`). Die Länge zählt an einem offenen Ende bis 0,1 m mit.
- **Tür mit Blatt** an der Grenze zu einem Raum (Türpunkt bis halbe Türbreite + 300 mm an der Grenze; ohne Breite
  1 m) macht die **ganze** Grenze zu diesem Raum zum Trenner. Eigener Entscheid, gemessen: auf Am Rain liegen neben
  Türen Wandlücken (nicht erkannte Wand) — ohne diese Regel ginge Am Rain EG „VR 12,78" über die wandlose Grenze zum
  WC `raum_85` (3,06 m, `tuer_242` darin) in das WC (1,77 → 18,33 m²), OG1 über 5,70 m (`tuer_22`/`tuer_23` darin)
  in den Gang `raum_4`. Im Zweifel eigener Raum statt Zuschlag.
- **Nicht eindeutig**: die zwei breitesten Öffnungen zu verschiedenen Räumen liegen < 100 mm auseinander (je Ende
  eine 50-mm-Rasterzelle). **Breiteste Öffnung zu einem Raum außerhalb der Wohnung** (Balkon, Schacht,
  Erschließung) → eigener Raum.
- **Zuschlag**: Raum ∪ Fläche (um 1 mm geschlossen, sonst bleibt die Gleitkomma-Fuge), Löcher als 1-mm-Schlitz
  (`bereinigung._schlitz`); `polygon_roh` wird mitgeführt, die Bilanz roh − mm bleibt (DG1 `raum_1`: 100,87 − 90,89 =
  9,98 = Abzug AR). **Neuer Raum** `frei_<n>`: `raum_typ` leer (UNBEKANNT — magenta in `gesamtdarstellung` und
  `raumerkennung_darstellung`), Klasse `None`, ohne Wohnung, Flags 00. Türen bleiben unverändert.
- **Einbau** (`provider.py:252-260`): nach `_tueren_und_wohnungen` (der Umriss liest `wohnung_id` aus rohen Türen),
  vor Ausgängen und Fluchtwegen; im Fehlerschutz. Befund je Fläche in `freiflaeche_befund` → `bericht.md`
  „Warnungen" (`scripts/plan_pruefen.py:1333-1334`).

**Rennweg DG1 am Plan geprüft** (Bild und Koordinaten im Session-Scratch): Grenze Feld | Wohnzimmer von
(12 544 517 / 356 218 318) bis (12 542 250 / 356 213 068) mm, 5,92 m (Rand bis 100 mm am Wohnzimmer); Wandkörper darauf
0,20 m = 3,4 % (±1 mm) bzw. 5,1 % (±50 mm) — K1: 5,79 m, 3 %. Keine Tür an der Grenze; die nächste Tür mit Blatt ist
`tuer_3` (WC → Gang) 0,62 m vom Feld. Im Feld Sofas, TV, Schrank (`New_065 Möbel Einrichtung`), kein Stempel.
**Entscheidung: Öffnung ohne Türblatt 5,72 m → Wohnzimmer `raum_1` 73,95 → 90,89 m².** Prüfstrecke
(`plan_pruefen` DG1 in den Scratch): `bericht.md` Warnungen „freiflaeche: 16.94 m² … → raum_1 WOHNZIMMER 73.95 →
90.89 m² …", `06_platzierung.png` zeigt das Feld grau (privat) im Wohnzimmer.

**Tests:** `tests/naht/test_freiflaeche_wohnung.py::test_dg1_sofa_feld_geht_ins_wohnzimmer` (echter Parse: TV-Punkt im
Wohnzimmer, 90,85 ± 0,25 m² — 90,85 = 73,95 + 16,90 aus K1; Toleranz = 14 mm Randversatz auf dem Feldumfang 18,1 m,
gemessen +0,04; Wohnung `top_1`, `WOHNUNG_PRIVAT`, Flags 00, kein `frei_*`, Befund-Zeile) und
`tests/raumerkennung/test_freiflaeche.py` (synthetisch: Öffnung → Zuschlag; Tür mit Blatt → `frei_1` ohne Wohnung,
Klasse, Flags; zwei gleich breite Öffnungen → nicht eindeutig; Nachbar Erschließung → nicht im Umriss, nichts geändert).

**Rot vor dem Fix** (`pytest tests/raumerkennung/test_freiflaeche.py tests/naht/test_freiflaeche_wohnung.py
--tb=line`, Kopf `5f2f024` + Tests, Quelle als Kopie des Kopfs, Kurzform):

```
test_freiflaeche_wohnung.py:33 → :22: AssertionError: []   (TV-Punkt im Sofa-Feld liegt in keinem Raum)
test_freiflaeche.py: ModuleNotFoundError: No module named 'notbeleuchtung.raumerkennung.freiflaeche'
1 failed, 1 error in 3.32s
```

**Grün nach dem Fix:** dieselben 5 Tests passed (3,3 s).

**Messung** (eigener Runner je Plan allein; Vorher = Nachher 2c, Nachher = Arbeitsbaum dieses Commits; 24 Pläne:
Rennweg UG/EG/OG1/OG2/OG3/DG1/DG2/DD, Barawitzka EG, Mollgasse 1KG/2KG/EG/1.OG/2.OG/3.OG/4.OG/DG, Muthgasse E2, Am Rain
UG/EG/OG1/OG2/OG3/OG4; Am Rain und Muthgasse allein). Freie Flächen > 2 m² gesamt **125**, davon **16 im
Wohnungsumriss**, 109 außerhalb (Erschließung, Höfe, Außenflächen in der gedeckten Kontur, unerkannte Bereiche —
bleiben frei). Je Plan gesamt / im Umriss: Rennweg DG1 1/1, übrige Rennweg 0/0; Barawitzka EG 4/0; Mollgasse 1KG 0,
2KG 0, EG 5/0, 1.OG 5/1, 2.OG 5/1, 3.OG 2/0, 4.OG 5/1, DG 0; Muthgasse E2 5/0; Am Rain UG 4/0, EG 31/4, OG1 27/5,
OG2 21/1, OG3 7/1, OG4 3/1.

**Entscheidungen: 4 → Raum, 12 → neuer Raum UNBEKANNT, 0 nicht eindeutig, 0 ohne Entscheidung.** Jede Fläche einzeln
(Lage = `representative_point` in m, Planeinheiten; „Stempel" = Raumstempel, der IN der Fläche liegt):

| Plan | Geschoss | Fläche m² | Lage (x, y) | Wohnung (Beleg) | Entscheidung | Grund | Stempel in der Fläche |
|---|---|--:|---|---|---|---|---|
| Rennweg DG1 | DG | 16,94 | 12 542,2 / 356 216,6 | `top_1` (Nachbarn) | → `raum_1` WOHNZIMMER 73,95 → 90,89 | Öffnung 5,72 m, keine Tür | — (Sofas, TV) |
| Mollgasse 1.OG | 1OG | 6,45 | 2 841,2 / 1 687,1 | `top_1` (Nachbarn) | → `raum_31` ZIMMER 6,02 → 12,47 | Öffnung 6,41 m, keine Tür | ZIMMER 12,26 |
| Mollgasse 2.OG | 2OG | 5,93 | 2 730,6 / 1 554,0 | `top_4` (Nachbarn) | → `raum_35` ZIMMER 7,13 → 13,07 | Öffnung 6,01 m, keine Tür | ZIMMER 12,68 |
| Mollgasse 4.OG | 4OG | 7,34 | 2 828,3 / 1 745,6 | `top_3` (Nachbarn) | → `raum_2` ZIMMER 6,01 → 13,35 | Öffnung 6,95 m, keine Tür | ZIMMER 12,98 |
| Am Rain EG | EG | 16,57 | 37,0 / 21,7 | `top_42` (Nachbarn) | neuer Raum `frei_1` UNBEKANNT | Tür mit Blatt `tuer_172`, `tuer_201`, `tuer_242` (zum WC `raum_85`), keine Öffnung | VR 12,78 |
| Am Rain EG | EG | 3,92 | 33,4 / 19,9 | `top_42` (Nachbarn) | neuer Raum `frei_2` UNBEKANNT | Tür mit Blatt `tuer_151`, keine Öffnung | AR 3,37 |
| Am Rain EG | EG | 2,36 | 23,4 / 13,1 | `top_34` (Nachbarn) | neuer Raum `frei_3` UNBEKANNT | Tür mit Blatt `tuer_157` (zum VORRAUM `raum_91`), `tuer_214`/`tuer_249` (zum Wohnzimmer `raum_74`) | — |
| Am Rain EG | EG | 9,76 | 21,8 / 10,6 | `top_34` (Nachbarn) | neuer Raum `frei_4` UNBEKANNT | Tür mit Blatt `tuer_214`, `tuer_216`, `tuer_249`, keine Öffnung | — |
| Am Rain OG1 | 1OG | 11,17 | 149,3 / 49,3 | `top_12` (Nachbarn) | neuer Raum `frei_1` UNBEKANNT | Tür mit Blatt `tuer_51` an der Grenze zu BALKON `raum_30` und KÜCHE `raum_40` | BALKON 3,88 |
| Am Rain OG1 | 1OG | 6,75 | 95,8 / 44,9 | `top_10` (Nachbarn) | neuer Raum `frei_2` UNBEKANNT | 4 Türen mit Blatt an der Grenze zum Gang `raum_4` (Grenze ohne Wandkörper 5,70 m) | — |
| Am Rain OG1 | 1OG | 3,99 | 54,0 / 9,0 | `top_50` (Nachbarn) | neuer Raum `frei_3` UNBEKANNT | breiteste Öffnung 2,27 m zu `rest_10` SCHACHT (KEIN_RAUM) | — |
| Am Rain OG1 | 1OG | 2,39 | 51,5 / −1,1 | `top_42` (Nachbarn) | neuer Raum `frei_4` UNBEKANNT | keine Öffnung ≥ 0,80 m, keine Tür | LOGGIA 7,67 |
| Am Rain OG1 | 1OG | 18,19 | 12,7 / 44,7 | `top_26` (Nachbarn) | neuer Raum `frei_5` UNBEKANNT | Tür mit Blatt `tuer_95` (zum WC `raum_36`), `tuer_96`, `tuer_103` | BAD 5,35 · GANG 7,68 |
| Am Rain OG2 | 2OG | 3,99 | 54,0 / 9,0 | `top_24` (Nachbarn) | neuer Raum `frei_1` UNBEKANNT | breiteste Öffnung 2,27 m zu `rest_9` SCHACHT (KEIN_RAUM) | — |
| Am Rain OG3 | 3OG | 2,73 | 61,1 / 11,6 | `top_14` (±250-mm-Umriss) | neuer Raum `frei_1` UNBEKANNT | Tür mit Blatt `tuer_84`, `tuer_86`, `tuer_98` an der Grenze zum Wohnzimmer `raum_30` (Grenze ohne Wandkörper 4,23 m) | VR 5,13 |
| Am Rain OG4 | 4OG | 5,41 | 56,9 / 8,7 | `top_5` (Nachbarn: nur ABSTELLRAUM `raum_14`) | neuer Raum `frei_1` UNBEKANNT | Tür mit Blatt `tuer_45` (KEIN_RAUM\|AUSSEN), kein Nachbarraum an der Fläche | — |

Plan angesehen (Bilder je Fläche im Scratch): die drei Mollgasse-Zimmer sind je ein Raum zwischen vier Wänden (Fenster
links), dessen Polygon nur die rechte Hälfte deckte (runde Aussparung); der Stempel liegt in der freien Hälfte, nach dem
Zuschlag +1,7 / +3,1 / +2,8 % gegen den Stempel. Am Rain: in 6 der 12 neuen Räume liegt ein Stempel (VR, AR, BALKON,
LOGGIA, BAD + GANG) — dort ist ein echter Raum, dessen Stempel kein Polygon bekam; nach der Regel UNBEKANNT ohne Typ
(Typ aus dem Stempel wäre ein neuer Entscheid, s. offen).

**Blast Radius** (Runner-JSON 2c gegen 2d, 24 Pläne): **0 Verstöße.** Räume weg 0; Typ-, Klassen-, Wohnungs- oder
Flag-Wechsel 0; Fläche geändert nur an den 4 aufnehmenden Räumen (die alte Fläche bleibt enthalten bis auf
0,0002 m² an DG1 `raum_1` — 1-mm-Schließung an spitzen Ecken); 12 neue Räume `frei_*` (Typ leer, Klasse `None`, ohne
Wohnung, Flags 00); Zuwachs über Wandkörpern höchstens 0,0001 m² (Gleitkomma-Kontakt, keine Wand geschluckt); Türen,
Ausgänge, Segmente, Anker, korrigierte Rollen, `bestaetigt_privat`, Stiegenhäuser, Bounds und alle übrigen Warnungen
24/24 gleich (Wohnungen und Einraum damit unverändert). **Leuchten** (Default-Platzierung) 23/24 gleich; Am Rain OG1:
eine Sicherheitsleuchte neu in `frei_2`, eine RZ liegt statt in „kein Raum" jetzt in `frei_2` (unbestimmt) — kein
Notlicht-Verlust. Parse-Laufzeit und Spitze unverändert (Muthgasse E2 645,6 s / 11,29 GB, Am Rain EG 481,7 s /
6,30 GB). Ein Überlappungsschutz in `freie_flaechen` (zwei Flächen an einem Hals < 0,2 m, gefunden auf Am Rain OG1
außerhalb jedes Umrisses, 0,02 m²) kam nach den Läufen dazu; auf allen 24 gesicherten Ständen ergebnisgleich
(Befund-Zeilen und Flächen) nachgerechnet.

**Volle Suite** (allein, 29 min 41 s, vor dem Überlappungsschutz): `6 failed, 2242 passed, 11 skipped, 6 deselected,
15 xfailed` — dieselben 6 roten wie nach 2c (3 × `test_keine_leuchten_in_wohnung_privat` OG1/OG2/DG1 = Board 1
Leonis, `test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell`, die 2 S4c-Pins), 2242 = 2237 + 5 neue. Nach
dem Schutz: `test_freiflaeche.py`, `test_freiflaeche_wohnung.py`, `test_wohnungsumriss.py`, `test_provider.py`,
`test_rest_komponenten.py` 48 passed, 1 skipped. Kein Test umgestellt, keine Schwelle, kein Soll, kein Marker angefasst.

**Gate:** `pytest -m gate tests/gate` 3 passed, 1 xfailed. `gate_messung` auf dem Arbeitsbaum dieses Commits (vor dem
Commit, `_arbeit/gate/messung_5f2f024-dirty-2d.json`, 102,2 s), `pruefe_gate` gegen `nullmessung_f15d03f.json`:
(0) unsauberer Arbeitsbaum (erwartet) und **(3) `M4.einraum` DG2 0 → 1** (Enis Board 3, unverändert); M17 18/18
BESTANDEN; alle Messfelder außer `meta` gleich der Review-1-Messung `messung_27de6a0.json`.

**Offen nach 2d:**
- **Owner-Bestätigung** der Definition (gedeckte Kontur statt Deckenplatte; Umriss = Nachbarn oder ±250 mm), der
  Mindestbreite 0,80 m und der Regel „Tür mit Blatt an der Grenze → ganze Grenze Trenner" (Am Rain EG `frei_1`, OG1
  `frei_2`, OG3 `frei_1` hängen daran). P1 · Selman (Owner).
- **Stempel in neuen UNBEKANNT-Räumen** (Am Rain EG VR 12,78 / AR 3,37, OG1 BALKON 3,88 / LOGGIA 7,67 / BAD 5,35 +
  GANG 7,68, OG3 VR 5,13): echte Räume, deren Stempel kein Polygon bekam (F-Stufe/Zuordnung auf Am Rain). Typ aus dem
  Stempel übernehmen wäre ein neuer Entscheid (BALKON/LOGGIA → AUSSEN). P1 · Selman. **Erledigt mit Abschnitt 2
  (Owner-Entscheid 2, § 24): 7 der 12 typisiert, OG1 `frei_5` bleibt UNBESTIMMT mit Grund.**
- **Türseiten an neuen Räumen** bleiben `KEIN_RAUM` (z. B. Am Rain EG `tuer_242` KEIN_RAUM\|`raum_85` an `frei_1`):
  die Türzuordnung läuft vor 2d; neu zuordnen hieße Wohnungen und Fluchtwege nachziehen. P2 · Selman.
- **Darstellung:** `plan_pruefen._raumflaeche_stil` (`06_platzierung.png`) zeichnet einen Raum ohne Typ weiß, magenta
  nur GANG/VORRAUM ohne Klasse; `gesamtdarstellung`/`raumerkennung_darstellung` zeigen ihn magenta („UNBEKANNT").
  Änderung außerhalb der Grenze dieses Auftrags. P2 · Selman.
- **Am Rain OG4 `frei_1`** liegt am Treppen-/Liftkern ohne Stiegenhaus (R-09); „im Umriss `top_5`" stützt sich auf einen
  Nachbarn (ABSTELLRAUM `raum_14`). P1 · Selman (mit R-09).
- **Freie Flächen außerhalb jedes Wohnungsumrisses** (109 auf 24 Plänen) bleiben frei — nicht Teil der Owner-Regel;
  R-05 b gilt für sie weiter.

## 17. Punkt 2e — Kennzeichen `durchleitung` (entschieden: **B**, nichts gebaut, Board-Antrag geschlossen)

**Klärung 1 — wer, wann, wofür.** Beantragt hat das Feld **Selman selbst**, mit dem Owner-Entscheid vom 2026-09-20
(Commit `5ac3e0f`, „Stapel mit S4c, Verfahren für S7a+S7b"). In der Fassung dieses Commits steht in
`docs/GATE_TUERSTAPEL.md:602`: „**Board-Antrag (offen, blockiert den Slice nicht):** der Owner will durchgeleitete
Segmente mit `durchleitung=True` markiert sehen". Heute steht es in `docs/GATE_TUERSTAPEL.md:903-907` („Board-Antrag
weiter offen … durchgeleitete Segmente sollen `durchleitung=True` tragen … Der Slice baut die **Wirkung** und weist
die Durchleitung als Prüfstrecken-Warnung aus") und `:620-623`. Im Code verweisen `provider.py:105-108` und
`fluchtweg.py:238-239` darauf. Der Zweck war ein **Ausweis**: `FluchtwegSegment.quelle` kennt nur
LINIE/GRAPH/FALLBACK (`hauptengine/contracts/raum_modell.py:192`), daher sollten durchgeleitete Segmente erkennbar sein.
Beantragt war ein **Segment**-Feld. Eine Anforderung von Leonis findet sich nicht: Alle Commits aller Refs mit
„durchleit" in der Nachricht sind von Selman (`git log --all -i --grep`), und `Handoff/` hat 0 Treffer. Als eigener
Antrag stand es nie im Board:
`docs/COORDINATION.md` erwähnt die Durchleitung nur in der Naht-Aussage (Log 2026-09-30, Punkt 6) und im Hinweis zu
Option B vom 2026-09-26. In `docs/OFFENE_FRAGEN.md` gibt es 0 Treffer für „durchleit".

**Klärung 2 — was Leonis' Code liest** (gelesen, in `platzierung/` nichts geändert). Er liest keine Durchleitung:
Für `durchleit`, `start_raum`, `ziel_raum` und `.quelle` an Segmenten gibt es in `src/notbeleuchtung/platzierung/`
**0 Treffer**. Die Segment-Leser:

- `deckung.py:124-151` `garantiere_redundanz`: je Segment-Polylinie mindestens 2 Leuchten im Radius l = z·h.
  Fehlt eine, setzt die Funktion Zusatz-SL bogenverteilt **auf die Polylinie**, ohne Raum- und Klassenprüfung.
- `deckungs_zuordnung.py:85-99`: füllt nur `covers_segment`, setzt nichts.
- `sichtkette.py:145-157`: macht Segmentpunkte in Korridor-Polygonen zu Einzugspunkten. Die Korridore wählt sie nach
  `raum_typ` (`:92-95`).
- `communal_stgh_strategy.py:62-81`: setzt 1 RZ am Segment-Endpunkt `polyline[-1]`, nur wenn es keinen
  Kreuzungsanker gibt (`platzierer.py:239-243`).
- Graph und Anker: `graph.py:30-36`, `anker_strategy.py:50` und `sichtkette.py:119` lesen `zirkulation.nodes/edges`.
  Die füllt nur 09-WEG (`raumerkennung/zirkulation.py:61-96`). GRAPH-Segmente stehen nur in `segmente`
  (`provider.py:284-287`). Eine Durchleitung erzeugt also keinen Anker.
- Klasse und Flags liest nur `flaechen_strategy.py:162-166`: `WOHNUNG_PRIVAT` ohne Flags bekommt kein Flächenlicht.
  Nach dem Typ ohne Klasse arbeiten `deckung.verdichte_fluchtweg` (`deckung.py:234-236`) und
  `platzierer._sichtlinien_garantie` (`platzierer.py:200-204`). Das ist Board 1, § 6.8/6.9.

**Synthetischer Fall** (die Prüfstrecke hat 0 Durchleitungen). Topologie wie
`tests/raumerkennung/test_wohnungsklasse.py::_durchleitung_plan` bzw. `::_durchleitung_l_form`: KELLER → GANG `g1` →
privater Raum `v` (Wohnungseingang `tw` zum Stiegenhaus, ZIMMER dahinter) → GANG `g2` → Hauseingang. Die echte Kette
läuft so: `bilde_wohnungen`, dann `fluchtwege(…, durchleitung=notiz)`, dann der echte `NotlichtPlatzierer` aus
`build_default_bundle()`. Jeder Fall wird zweimal platziert: **mit** den GRAPH-Segmenten durch `v` und **ohne** sie
(Klassen und Flags unverändert). Runner `_durchleitung_platzierung.py` liegt im Session-Scratch. In allen Fällen ist
`v` `WOHNUNG_PRIVAT`, Flags 00, `top_1`.

| Fall | Segmente durch `v` (Provider-Notiz) | Leuchten gesamt mit/ohne | in `v` mit/ohne | alle Platzierungen gleich | Herkunft der Leuchten in `v` |
|---|---|--:|--:|---|---|
| GANG 5 × 4 m | `seg_graph_tk`, `_ta`, `_tw` | 5 / 5 | 1 / 1 | ja | SL (11 800, 2 000) aus `verdichte_fluchtweg` |
| VORRAUM 5 × 4 m | dieselben | 4 / 4 | 0 / 0 | ja | — |
| GANG L-Form (nicht konvex, Skelettpfad) | `seg_graph_tk`, `_tb`, `_tw` | 6 / 6 | 2 / 2 | ja | RZ (1 800, 8 000) aus `_sichtlinien_garantie`, Aufheller 500 mm |
| VORRAUM 40 × 4 m | `seg_graph_tk`, `_ta`, `_tw` | 4 / 4 | 0 / 0 | ja | — (`garantiere_redundanz` setzt keine SL in `v`) |
| GANG 40 × 4 m | dieselben | 8 / 8 | 5 / 5 | ja | 2 RZ, 2 SL (§ 4.2.1, ohne `covers_segment`), 1 Aufheller 500 mm |

Zuordnung der Herkunft einzeln aufgerufen: `plan_sicherheitsleuchten` setzt in `v` 0 Leuchten,
`verdichte_fluchtweg` (GANG 5 m) 1 SL, `_plan_rettungszeichen` (L-Form) 1 RZ. **Ergebnis:** Die Platzierung
reagiert nicht auf die Durchleitung. Mit und ohne durchgeleitetes Segment liegen dieselben Leuchten an denselben
Stellen. Nur `covers_segment` ändert sich (GANG 40 m: das RZ bei 11 800 deckt `seg_graph_tk`/`_ta`). Leuchten in
einem privaten GANG kommen aus den typbasierten Strategien (Board 1), und das gilt auch ohne Weg hindurch. Ein
privater VORRAUM bekommt 0 Leuchten.

**Korrektur der Naht-Aussage** (`docs/INTEGRATION_2026-09-30.md` „Naht für Leonis", `docs/COORDINATION.md` Log
2026-09-30, Punkt 6, § 6.6 hier):

- „der durchgeleitete Raum ist nie `start_raum`/`ziel_raum`" **gilt nicht.** Synthetisch tragen `seg_graph_tw` und
  `seg_graph_tb` als `start_raum` den privaten Raum `v`. Grund: Sind beide Türseiten Graph-Knoten, fällt
  `start_raum` auf `von_raum` zurück (`fluchtweg.py:409-410`). `seg_graph_tw` läuft dabei durch `v`.
- „Direktlinie Tür → Tür, ohne Stützpunkt" gilt nur, wenn das Raumpolygon die Strecke deckt. Sonst wird es ein
  Skelettpfad mit Stützpunkten (`fluchtweg.py:391-404`, L-Form oben).

**Ableitung aus bestehenden Feldern** (so liest Leonis die Durchleitung, falls er sie braucht):

- (a) **Knoten-Menge** = `wohnungsklasse.durchleitung_raeume`: `raum_typ` ∈ {GANG, VORRAUM} ∧
  `nutzungsklasse == "WOHNUNG_PRIVAT"` ∧ `not ist_fluchtweg` ∧ `not ist_communal` ∧ eine Tür (`von_raum`/`nach_raum`)
  zu einem STIEGENHAUS. Beleg im Code: `wohnungsklasse.py:124-135` (`kandidaten`), `:927-931`, und `:951`
  (Flags 00 genau für bestätigt private GANG/VORRAUM). Gemessen auf den 24 Mess-Dumps „Nachher 2d“ (Session-Scratch
  `lk/2d`): Feld-Regel und `kandidaten ∩ bestaetigt_privat` stimmen **24/24** überein, zusammen 13 Räume
  (Mollgasse 1.OG 4, 2.OG 3, 3.OG 1, 4.OG 3, Am Rain OG3 1, Rennweg OG2 1).
- (b) **tatsächlich durchgeleitet** = ein Raum aus (a), dessen Polygon, um 100 mm nach innen versetzt, eine Polylinie
  mit `quelle == "GRAPH"` schneidet. Synthetisch stimmen die Paare (Segment, Raum) in 5/5 Fällen genau mit der
  Provider-Notiz überein. Auf den 12 Prüfplänen (`tests/plaene.py`, echter `provider.parse` auf `22cd85e`, je Plan
  allein, Muthgasse 633 s) ergibt die Regel **0** Paare bei 0 Notizzeilen. Gezählt wurden 52 GRAPH-Segmente,
  232 Räume `WOHNUNG_PRIVAT`/00 und 5 Knoten-Räume (Rennweg OG2 1, Mollgasse 1OG 4).
- **Warum (a) und der Innenpuffer nötig sind:** Prüft man nur Klasse und Flags ohne Versatz, schneiden 26
  Polylinien einen privaten Raum (0,5 bis 847,5 mm). 24 davon sind der Startraum an der Starttür, 2 sind
  Knoten-Räume (Mollgasse 1OG `raum_2` 43,7 mm, `raum_4` 13,4 mm, keine Notiz). Mit 100 mm Versatz bleibt 1 Treffer:
  Mollgasse EG `seg_graph_tuer_50` läuft 847,5 mm durch das ZIMMER `raum_38`, seinen Startraum. Den nimmt (a)
  heraus.

**Entscheidung B (Owner-Entscheid Selman 2026-09-30):**

- Leonis' Code braucht die Information nicht. Er liest sie nirgends, seine Platzierung ist mit und ohne Durchleitung
  gleich, und für das Notlicht genügt Klasse plus Flags: jeder Raum aus (a) fällt unter `flaechen_strategy.py:162-166`.
- Die Information ist aus bestehenden Feldern eindeutig ableitbar, siehe (a) und (b).
- Der Ausweis, für den das Feld beantragt war, existiert bereits als Prüfstrecken-Zeile
  (`scripts/plan_pruefen.py:1203-1206`, Abschnitt „Durchleitung durch private Räume" in `bericht.md`).

Darum gibt es kein Contract-Feld, keinen `contract_version`-Bump und keine Schema-Regenerierung. `hauptengine/contracts/**`
und `platzierung/` sind unverändert. Den Board-Antrag schließt `docs/COORDINATION.md` (Log 2026-09-30, 2e), die
Naht-Aussage korrigiert `docs/INTEGRATION_2026-09-30.md`. Dieser Commit ist reine Doku und hat keinen Test, also gibt
es keinen roten Zustand zu belegen. Weder Suite noch Gate wurden neu gefahren, denn `src/`, `tests/` und `scripts/`
sind unverändert gegenüber `22cd85e`.

**Offen nach 2e:**
- `fluchtweg.py:24-26` (Modul-Doc) sagt weiter „Direktlinie Tür→Tür … und er ist nie Start- oder Zielraum eines
  Segments", `provider.py:105-108` und `docs/GATE_TUERSTAPEL.md:903-907` nennen den Antrag noch offen. Nicht geändert,
  weil B „nichts bauen" heißt. Nachziehen beim nächsten Code-Commit in `raumerkennung/`. P2 · Selman.
- Die Ableitungsregel (a)+(b) bindet kein Test. Ein Naht-Test, der sie synthetisch gegen `durchleitung_raeume` und die
  Provider-Notiz prüft, würde die Zusage an Leonis absichern. Nicht gebaut (B). P2 · Selman.
- Mollgasse EG `seg_graph_tuer_50` läuft 847,5 mm durch das private ZIMMER `raum_38` (Startraum). Die Ursache
  (Türpunkt im Raum oder Polygon-Überlappung mit dem Erschließungsraum) ist nicht untersucht. P2 · Selman.
- Leuchten in privaten GANG-Räumen (synthetisch 1 bis 5 je Fall) bleiben Board 1 (§ 6.8/6.9). Die Durchleitung
  ändert daran nichts. Leonis, nur gemeldet.

## 18. Punkt 2f — RAM der Prüfstrecke (erledigt mit dem Commit dieses Eintrags: **Ziel erreicht**)

**Auftrag (Owner 2026-09-30):** RAM-Spitze je Prüfplan messen und senken, bis Am Rain OG4 und die großen Pläne
(Am Rain EG 74,5 MB, UG 46,6 MB, OG1 50,8 MB) mit den anderen in **einem** Prüfstrecken-Lauf (`scripts/plan_pruefen.py`
ohne Argument, 13 Pläne nacheinander in einem Prozess) durchlaufen: Spitze je Plan ≤ 8 GB Working Set, keine
Reißleine, kein `MemoryError`, mit Plan-Render. Ergebnisse auf den 12 Prüfplänen feldgleich, Gate unverändert.

**Messung.** Je Plan ein eigener Prozess, allein auf dem Rechner, Wrapper um `plan_pruefen.plan_pruefen(dxf)` (Runner
`_ram.py` im Session-Scratch). Er umhüllt die Phasen: Laden (`lade_dxf`), Kaskade (`_raum_kaskade` bzw.
`raeume_aus_kaskade`, Wandkörper), F-Stufe (`flute_stempel`), R-Stufe (`komponenten_ohne_stempel`), Provider-Parse
(Außenbereich, Freifläche, Fluchtweg), Platzierung, Render (`_figur` bis `_speichern`, je Bildfunktion) und den
EG-Parse in `_restweg_im_eg`. Ein Sampler liest den Working Set alle 10 ms (`GetProcessMemoryInfo`), an jeder
Phasengrenze zusätzlich den monotonen `PeakWorkingSetSize` — ein neuer Prozess-Peak gehört so genau der Phase, in der
er entstand. Guard 14 GB (rund 16,7 GB frei). **Vorher** = Kopf `d63bc4c` (`git archive` von `scripts/`, `src/`,
`CAD_Symbole/` und der Barawitzka-Referenz-DXF in den Scratch, gestartet im Worktree wegen `Projekte/_eingang`),
**Nachher** = Arbeitsbaum dieses Commits. Ausgabe per `PLAN_PRUEFEN_ERGEBNIS` in den Scratch; die getrackten
`Projekte/_ergebnis/` sind unverändert.

**Ursachen (gemessen, nach Gewicht):**

1. **Plan-Render — Linientypen in Einzelstriche zerlegt.** Das ezdxf-Frontend zeichnet jeden Strich eines
   gestrichelten oder gepunkteten Linientyps als eigenes Segment. Am Rain OG4, ein `_figur` allein: **16,9 Mio.
   Segmente** (Layer `Achsen` 3,99 Mio., `Elektro` 3,56 Mio.); eine 84-m-Achse (`LINE` 302D4, Linientyp `PUNKT2_S9`)
   allein 372 677 Striche → **5,61 GB und 108 s je Bild**, Speichern 44 s. HATCH-Muster sind es nicht (7 Muster-Hatches,
   24 Linien). Vorher reißen Am Rain UG, OG1, OG2 und EG den Guard schon im **ersten** Bild, OG3 im zweiten.
2. **Geschlossene Figuren leben bis zum Zyklen-GC** (Referenzzyklen in matplotlib): OG4 nach `plt.close` 5,65 GB, nach
   `gc.collect()` 0,95 GB. Die vorige Figur lebte so neben der neuen — OG4 ab dem ersten Bild auf einem Plateau von
   11 GB, Spitze 13,19 GB im fünften Bild.
3. **F-Stufe — ein Vollraster je Stempel und Versiegelungsstufe** (`stempel_flutung._Flutwerk.masken`, Cache über
   5 Stufen; dazu das Distanzfeld der EDT, gerechnet nur für die Indizes). Muthgasse E2: Flutung der
   Prüfstrecken-Kaskade **11,31 GB / 597 s**, die zweite Flutung im Provider-Parse lief in den Guard (**14,03 GB** nach
   1 684 s). Am Rain, Flutung der Prüfstrecken-Kaskade vorher: EG 6,33 GB / 304 s, OG1 5,33, OG2 4,56, UG 3,94,
   OG3 2,14 GB. Mollgasse 1KG/2KG/EG: Spitze jeweils in der Flutung. Runner (Parse + Platzierung, allein): Muthgasse
   **631,6 s / 11,29 GB**.
4. **Restweg im EG — je Obergeschoss ein voller EG-Parse** (`_restweg_im_eg`, Aufruf aus `_fachteil3`) neben dem OG im
   Speicher: OG4 582 s, EG-Flutung dort 12,64 GB auf dem Render-Plateau. Im Lauf über alle Pläne viermal (Am Rain
   OG1–OG4).
5. **Keine Treiber (gemessen):** Laden der DXF (OG4 0,21 GB, Am Rain EG 0,58 GB Prozess nach dem ersten Laden); das
   zweite Laden im Provider-Parse hebt die Spitze nicht über das Plateau (EG nachher 2,52 → 2,60 GB). Die R-Stufe
   (Muthgasse vorher 0,82 GB Prozess, Am Rain EG 1,95 GB). Ein 50-mm-Raster über 34 km entsteht auf dem Kopf
   nicht mehr — der Fern-Filter aus `ed292e1` hält es klein (OG4-Kaskade 0,45 GB).

**Änderungen** (je danach Runner feldgleich):

- `scripts/plan_pruefen.py` (Render, erlaubt für 2f): `_figur` zeichnet mit `Configuration(min_dash_length=50 mm)` —
  Strich und Lücke mindestens 50 mm, auf 1 200 px höchstens 2 px (OG4: 16,9 Mio. → 45 264 Segmente, 5,61 → 0,41 GB,
  108 → 12 s je Bild, Speichern 44 → 2,5 s) — und ruft `gc.collect()` vor jeder Figur; `main` ruft es nach jedem Plan.
  `_restweg_im_eg` rechnet die Restweg-Zeile je EG-Plan einmal je Prozess (`_RESTWEG_EG`); der EG-Lauf legt seine Zeile
  nach dem eigenen Parse ab, nur bei Geschoss „EG" — derselbe Aufruf `parse(…, "EG")`. Ohne Argument läuft der EG vor
  seinen OG (Sortierung), dann parst kein OG mehr den EG.
- `stempel_flutung.py`: Flutregionen als **Ausschnitt** um ihre Box plus eine Zelle (`_Maske`, `_rahmen`) statt als
  Vollraster. Relief, Watershed, Rückdehnung, Lochfüllung und Konturen laufen auf dem Ausschnitt; er ist nur um ganze
  Zellen verschoben, also zellgleich (`_vektorisiere(…, versatz)` verschiebt die Konturen vor der Flächenwahl). Die EDT
  liefert nur noch die Indizes (`return_distances=False`).
- `rest_komponenten.py`: Labeln, Watershed und Vektorisieren im Rechteck der Außenkontur plus eine Zelle, je Label nur
  seine Box (`ndimage.find_objects`) statt `labels == lbl` über das Vollraster. **Raster-Obergrenze (R-05 a):** über
  `_MAX_ZELLEN` = 1e8 Zellen wird die Zelle ein Vielfaches von 50 mm (wie `fluchtweg._skelett_pfad`); bräuchte das mehr
  als `_MAX_RASTER_MM` = 200 mm, fällt die R-Stufe weg (Reißleine wie `stempel_flutung._MAX_RASTER_ZELLEN`) — beides mit
  `RuntimeWarning` statt `MemoryError`. Auf den 13 Plänen der Prüfstrecke und den 12 Prüfplänen greift keine der beiden
  Grenzen (keine Warnung im gemeinsamen Lauf und in der Runner-stderr).
- Nicht geändert: HATCH-Darstellung, DPI, Bildausschnitt (OG4 zeigt weiter 38 km Weltausdehnung, D-05 — kein
  RAM-Thema) und das doppelte Laden mit doppelter Kaskade (kein Treiber).

**Tabelle je Plan** (Einzellauf = je Plan eigener Prozess, allein; Spitze = Working Set; „Grundlast" = keine Phase
hebt sich ab; Guard = Abbruch bei 14 GB, die Spitze ist dann ≥):

| Plan | DXF MB | vorher: Spitze GB · Phase · Laufzeit | nachher Einzellauf: Spitze GB · Phase · Laufzeit | gemeinsamer Lauf: Spitze GB · Laufzeit | wirksame Änderung |
|---|--:|---|---|---|---|
| Rennweg_EG | 4,0 | 0,48 · Grundlast · 59 s | 0,47 · Grundlast · 54 s | 1,38 · 50 s | — |
| Rennweg_OG3 | 3,8 | 0,50 · Grundlast · 52 s | 0,48 · Grundlast · 53 s | 1,25 · 48 s | — |
| Barawitzka_EG | 12,9 | 1,32 · Render (Kacheln) · 266 s | 1,13 · Grundlast · 266 s | 1,43 · 255 s | Render, GC |
| Mollgasse_1KG | 4,1 | 0,89 · F-Stufe (Provider) · 120 s | 0,62 · F-Stufe (Provider) · 105 s | 1,27 · 99 s | F-Stufe |
| Mollgasse_2KG | 7,8 | 1,27 · F-Stufe (Provider) · 207 s | 0,88 · F-Stufe (Provider) · 180 s | 1,32 · 168 s | F-Stufe |
| Mollgasse_EG | 10,3 | 1,56 · F-Stufe (Provider) · 307 s | 1,07 · Grundlast · 264 s | 1,37 · 250 s | F-Stufe |
| Muthgasse_E2 | 23,2 | **≥ 14,03 Guard** · F-Stufe (Provider; in der Prüfstrecken-Kaskade 11,31) · Abbruch nach 1 684 s | 3,48 · F-Stufe (Provider) · 929 s | 3,57 · 908 s | F-Stufe |
| AmRain_OG4 | 12,9 | **13,19** · Render (Bild 05, Plateau 11 GB) · 1 601 s | 3,02 · EG-Parse (Außenbereich) · 444 s | 1,28 · 126 s | Render, GC, EG-Parse |
| AmRain_OG3 | 28,1 | **≥ 14,00 Guard** · Render (Bild 02, nach 01 Plateau 12,41) · Abbruch nach 474 s | 3,51 · EG-Parse · 685 s | 1,61 · 361 s | Render, GC, EG-Parse |
| AmRain_UG | 46,6 | **≥ 14,01 Guard** · Render (Bild 01) · Abbruch nach 383 s | 1,84 · Grundlast · 418 s | 1,92 · 401 s | Render, F-Stufe |
| AmRain_OG2 | 38,5 | **≥ 14,00 Guard** · Render (Bild 01) · Abbruch nach 484 s | 3,57 · EG-Parse · 818 s | 1,83 · 492 s | Render, F-Stufe, EG-Parse |
| AmRain_OG1 | 50,8 | **≥ 14,00 Guard** · Render (Bild 01) · Abbruch nach 516 s | 3,70 · EG-Parse · 901 s | 1,82 · 570 s | Render, F-Stufe, EG-Parse |
| AmRain_EG | 74,5 | **≥ 14,00 Guard** · Render (Bild 01) · Abbruch nach 669 s | 4,19 · Außenbereich (Provider) · 1 057 s | **4,19** · 1 034 s | Render, F-Stufe |

Vorher Muthgasse aus dem ersten Messlauf (Kopie ohne `CAD_Symbole/`; der Guard griff vor der Platzierung, die fehlende
Photometrie wirkt dort nicht), alle anderen aus dem Lauf mit vollständiger Kopie. Die höhere Spitze kleiner Pläne im
gemeinsamen Lauf ist die Grundlast des Prozesses aus den Plänen davor (Python-Heap).

**Gemeinsamer Prüfstrecken-Lauf** (`scripts/plan_pruefen.py` ohne Argument, unverändert gestartet; 13 Pläne in einem
Prozess, allein auf dem Rechner; Überwachung von außen alle 20 ms, Guard 26 GB; Runner `_gemeinsam.py` im Scratch):
**Exit 0, kein Guard, 0 × `MemoryError`, 0 Warnungen** (Reißleine, gröberes Raster, „fehlgeschlagen"), Plan-Render
für alle 13 Pläne, **4 829 s**, Prozess-Spitze **4,19 GB** (in Am Rain EG). **Ziel erreicht:** Spitze je Plan ≤ 4,19 GB
gegen das Ziel ≤ 8 GB. Die Ausgaben des gemeinsamen Laufs (`raeume.json`, `bericht.md` ohne die Zeile „Laufzeit",
`unbekannte_muster/*.json`) sind 13/13 gleich denen der Einzelläufe — auch die Restweg-Zeilen der vier Am-Rain-OG
(aus dem EG-Lauf statt aus einem eigenen EG-Parse).

**Feldgleich:**

- **Runner, 12 Prüfpläne** (`tests/plaene.py`; `provider.parse` + Default-Platzierung; je Raum id, Typ, Polygon,
  Fläche, Klasse, Wohnung, Flags; Türen, Ausgänge, Segmente, Anker, korrigierte Rollen, Warnungen, Leuchten): Kopf
  `d63bc4c` gegen den Arbeitsbaum **12/12 gleich in allen 18 Feldern**. Muthgasse E2 Parse + Platzierung 631,6 s /
  11,29 GB → 271,8 s / 1,79 GB.
- **Runner, Am Rain alle 6 Geschosse** (zusätzlich, je Plan allein): **6/6 gleich in allen 18 Feldern**. Parse + Platzierung
  EG 478,9 s / 6,30 GB → 307,5 s / 2,71 GB, OG1 254,6 / 5,31 → 102,8 / 0,67, OG2 219,2 / 4,54 → 88,5 / 0,63, UG 113,2 / 3,91 →
  50,8 / 0,65, OG3 99,3 / 2,12 → 46,1 / 0,45, OG4 21,9 / 0,43 → 16,1 / 0,23.
- **Prüfstrecke** (Einzellauf vorher gegen nachher, `raeume.json`, `bericht.md` ohne „Laufzeit", Muster-JSON):
  **7/7 gleich**, wo der Vorher-Lauf durchkam (Rennweg EG/OG3, Barawitzka EG, Mollgasse 1KG/2KG/EG, Am Rain OG4).
  Muthgasse und Am Rain EG/UG/OG1–OG3 haben vorher keine Ausgabe (Guard).
- Plan-Bilder angesehen (Mollgasse EG `01_render.png` vorher/nachher, Am Rain EG `02_raeume.png`): gleich bis auf eine
  gröbere Strichelung feiner Linientypen.

**Tests** — rot vor dem Fix (`pytest tests/raumerkennung/test_stempel_flutung.py
tests/raumerkennung/test_rest_komponenten.py -k 2f --tb=line`, Quelle als Kopie des Kopfs `d63bc4c` + Tests,
Kurzform):

```
test_stempel_flutung.py:195: AssertionError: assert (435625 * 10) < 435625
test_rest_komponenten.py:379: Failed: DID NOT WARN. No warnings of type (<class 'RuntimeWarning'>,) were emitted.
test_rest_komponenten.py:392: Failed: DID NOT WARN. No warnings of type (<class 'RuntimeWarning'>,) were emitted.
3 failed, 31 deselected in 2.08s
```

Grün: `test_stempel_flutung.py` + `test_rest_komponenten.py` 34 passed. Neu sind
`test_stempel_flutung.py::test_2f_flutmasken_sind_ausschnitte` (Wandkörper 100 m daneben: Ergebnis gleich, jede Maske
< 1/10 des Rasters), `test_rest_komponenten.py::test_2f_zu_grosses_raster_rechnet_mit_groeberer_zelle` und
`::test_2f_reissleine_ueberspringt_die_rest_stufe` (Grenzen per `monkeypatch` auf die 8×4-m-Box herabgesetzt). Render
und Restweg-Zeile bindet kein Test; Beleg sind Messung und Ausgabevergleich oben.

**Volle Suite** (allein, nach den Messläufen, 17 min 32 s): `6 failed, 2245 passed, 11 skipped, 6 deselected,
15 xfailed` — dieselben 6 roten wie nach 2d (3 × `test_keine_leuchten_in_wohnung_privat` OG1/OG2/DG1 = Board 1 Leonis,
`test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell`, die 2 S4c-Pins), 2245 = 2242 + 3 neue. Kein Test
umgestellt, keine Schwelle, kein Soll, kein Marker angefasst.

**Gate:** `pytest -m gate tests/gate` 3 passed, 1 xfailed. `gate_messung` auf dem Arbeitsbaum dieses Commits
(`_arbeit/gate/messung_d63bc4c-dirty-2f.json`, 62,9 s), `pruefe_gate` gegen `nullmessung_f15d03f.json`: (0) unsauberer
Arbeitsbaum (erwartet) und **(3) `M4.einraum` DG2 0 → 1** (Enis Board 3, unverändert); M17 18/18 BESTANDEN; alle
Messfelder außer `meta` gleich `messung_5f2f024-dirty-2d.json`.

**Offen nach 2f:**

- **PDF-Export** (`hauptengine/render/pdf_export.py:116`, O-03) zeichnet mit demselben Frontend ohne
  `min_dash_length`; auf Am Rain ist dieselbe Strich-Zerlegung zu erwarten (300 dpi, A0). Nicht gemessen, nicht
  geändert (gemeinsame Lane). P1 · gemeinsam.
- Ein Einzellauf eines OG (`plan_pruefen.py AmRain_OG1.dxf`) parst den EG weiter selbst (Cache leer): nachher 3,70 GB,
  +318 s. Unter dem Ziel; nur der Lauf ohne Argument spart den EG-Parse. P2 · Selman.
- Nach der Prüfstrecken-Kaskade bleibt ein Plateau (Muthgasse rund 1,9 GB, Am Rain EG rund 2,5 GB), auf dem
  Provider-Parse und Bilder aufsetzen. Ursache (Allokator oder gehaltene Objekte) nicht untersucht, unter dem Ziel.
  P2 · Selman.
- `Projekte/_ergebnis/` (getrackt) ist nicht neu geschrieben; der gemeinsame Lauf liegt im Scratch. Ein Lauf in das
  getrackte Verzeichnis geht jetzt (rund 80 min, ≤ 4,2 GB) — als eigener Commit nach Owner-Entscheid. P2 · Selman.
- Am Rain OG4 `01_render.png` zeigt weiter die 38-km-Weltausdehnung (D-05). P2 · Selman.

## 19. Review 2 — Punkte 2d–2f (adversarial, Kopf `27478ca`)

Geprüft mit eigenem Code: eigener Runner (`provider.parse(dxf, "")` + Default-Platzierung, je Plan ein Prozess). Der
Dump enthält das ganze `RaumModell` und `PlatzierungsErgebnis` (`model_dump`), korrigierte Rollen,
`bestaetigt_privat`, alle Provider-Warnungen und Befunde und die Zahl der Wandkörper der Kaskade. Verglichen wird
exakt, ohne Rundung. Stände: `5f2f024` (vor 2d), `d63bc4c` (vor 2f, Code = `22cd85e`), `27478ca`. Runner, Dumps und
Ausgaben liegen im Session-Scratch.

**(1) Diff `5f2f024..27478ca`:** geändert sind `src/notbeleuchtung/raumerkennung/` (`freiflaeche` neu, `provider`,
`rest_komponenten`, `stempel_flutung`), `scripts/plan_pruefen.py` (2d: Befund-Zeilen unter „Warnungen"; 2f:
Mindest-Strichlänge im Render, `gc.collect`, Restweg-Zeile je EG einmal je Prozess), Tests und Doku. Tests sind nur
ergänzt (2 neue Dateien, 3 angehängte Tests, keine Zeile entfernt); keine Schwelle, kein Soll, kein Marker gelockert.
Kein Contract (2e = B: kein Feld, kein Bump, Schema unberührt), kein fremdes Paket, keine lokalen Pfade. Je Punkt ein
Commit. Rot-Nachweise: 2d § 16 — im eigenen Lauf auf `5f2f024` liegt der TV-Punkt des Sofa-Felds in keinem Raum, auf
`27478ca` in `raum_1`; 2f § 18 — selbst nachgefahren, die drei `-k 2f`-Tests auf der Quelle `d63bc4c`:
`3 failed` (`test_stempel_flutung.py:195` Größen-Assert, `test_rest_komponenten.py:379`/`:392` `DID NOT WARN`), auf
`27478ca` grün. 2e ist reine Doku ohne Test. Umfang: der 2f-Commit trägt zusätzlich R-05 a (Raster-Obergrenze und
Reißleine der R-Stufe, § 11 Punkt 5) und in `plan_pruefen` den Restweg-Cache (RAM, nicht Render); beides ist
ergebnisgleich (s. (4)), die Reißleine greift auf keinem gemessenen Plan.

**(2) 2d:**

- 12 Prüfpläne `5f2f024` gegen `27478ca`: **10/12 in allen Feldern gleich** (Leuchten eingeschlossen). Rennweg DG1
  und Mollgasse 1OG unterscheiden sich nur im aufnehmenden Raum (`raum_1` bzw. `raum_31`: Polygon, Fläche, bei DG1
  auch `polygon_roh`) und im Befund. Wandkörper je Plan gleich, **12/12** (z. B. DG1 194, Barawitzka 1 243,
  Muthgasse 737).
- **Rennweg DG1:** Wohnzimmer `raum_1` 73,95 → **90,89 m²**, weiter WOHNZIMMER, `top_1`, `WOHNUNG_PRIVAT`, Flags 00;
  die alte Fläche ist ganz enthalten, Zuwachs über Wandkörpern 0,0000 m². Die 14 anderen Räume sind in Typ, Klasse,
  Wohnung, Flags und Polygon unverändert; Leuchten 6/6 gleich. Grenze Feld | Wohnzimmer selbst gemessen 5,92 m, davon
  5,72 m ohne Wandkörper.
- **Stichprobe freie Flächen**, selbst nachgemessen (Kontur − Räume − Wandkörper aus den Eingaben der Stufe; Nachbarn,
  Grenzlängen ohne Wand und Türen mit eigenem Code):
  - Mollgasse 1.OG, 6,40 m²: einziger Nachbar `raum_31` ZIMMER `top_1`, Grenze 5,79 m, davon 5,66 m ohne Wand, keine
    Tür → Zuschlag 6,02 → 12,47 m². Stimmt.
  - Mollgasse 4.OG, 7,36 m²: einziger Nachbar `raum_2` ZIMMER `top_3`, Grenze 6,28 m, davon 6,13 m ohne Wand →
    Zuschlag 6,01 → 13,35 m². Stimmt (zusätzlich Mollgasse 2.OG 5,89 m² → `raum_35` 7,13 → 13,07 m², stimmt).
  - Am Rain OG3, 2,73 m²: Nachbarn `raum_27` BAD und `raum_30` WOHNZIMMER (`top_14`) und GANG `raum_35`
    (Erschließung) → im Umriss nur über ±250 mm; Türen mit Blatt an der Grenze → `frei_1`. Stimmt nach der Regel, s.
    R2-01.
  - Am Rain OG4, 5,41 m²: kein Raum bis 100 mm, bis 500 mm nur Räume von `top_5`; `tuer_45` (KEIN_RAUM|AUSSEN) →
    `frei_1`. Stimmt nach der Regel.
  - Muthgasse E2, 13,73 m² (Nachbarn bis 500 mm in `top_13` … `top_16` und GANG ohne Wohnung) und 5,06 m² (`top_12`,
    `top_16`, `top_21`, SCHLEUSE/GANG ohne Wohnung): nicht im Umriss, bleiben frei. Stimmt; keine der 5
    Muthgasse-Flächen liegt im Umriss.
- **Am Rain OG1** `5f2f024` gegen `27478ca`: 5 neue `frei_*` (Typ leer, Klasse und Wohnung `None`, Flags 00, kein
  Wandkörper darin, keine Überlappung > 0,01 m² mit einem anderen Raum). Leuchten 68 → 69: alle 68 an derselben
  Stelle (14 nur mit neuer `luminaire_id`), neu 1 Sicherheitsleuchte in `frei_2` — kein Notlicht-Verlust.

**Urteil 2d: bestätigt.**

**(3) 2e:** In `platzierung/` gibt es 0 Treffer für `durchleit`, `start_raum`, `ziel_raum`; alle `.quelle`-Treffer
sind `anf.quelle`, `schwellen.quelle`, `eff.quelle` (Norm), keiner liest ein Segment. `flaechen_strategy.py:162-166`,
`deckung.py:234-236`, `platzierer.py:200-204` und `fluchtweg.py:409-410` sagen, was § 17 zitiert. Der Antrag steht in
`5ac3e0f` (Selman, 2026-09-20), damals `docs/GATE_TUERSTAPEL.md:602`; alle Commits mit „durchleit" sind von Selman.
Regel (a) gegen `kandidaten ∩ bestaetigt_privat` auf 14 eigenen Dumps (12 Prüfpläne + Mollgasse 2.OG/4.OG): 14/14
gleich (Knoten Mollgasse 1.OG 4, 2.OG 3, 4.OG 3, Rennweg OG2 1). Regel (b) auf denselben Dumps: 0 Paare bei 0
Notizzeilen, 52 GRAPH-Segmente auf den 12 Prüfplänen. Board-Antrag in `docs/COORDINATION.md` geschlossen,
Naht-Aussage in `docs/INTEGRATION_2026-09-30.md` korrigiert. **Urteil 2e: bestätigt.** Die Restaussagen in
`fluchtweg.py:24-26`, `provider.py:105-108` und `docs/GATE_TUERSTAPEL.md:903` bleiben offen wie in § 17.

**(4) 2f:** 12 Prüfpläne `d63bc4c` gegen `27478ca`: **12/12 in allen Feldern gleich** (RaumModell, Leuchten, Rollen,
Warnungen, Wandkörper); Muthgasse E2 im Runner 615,7 s / 11,29 GB → 256,1 s / 1,79 GB. Prüfstrecke
`scripts/plan_pruefen.py <dxf>` einzeln und allein, Spitze = `PeakWorkingSetSize` des Prozesses: **Am Rain OG4**
Exit 0, 431 s, **3,04 GB** (§ 18: 3,02 GB / 444 s); **Am Rain EG** Exit 0, 1 025 s, **4,19 GB** (§ 18: 4,19 GB /
1 057 s). Je 6 Bilder, 0 RuntimeWarnings; der OG4-Bericht hat die Restweg-Zeile und die Freiflächen-Zeile.
**Urteil 2f: bestätigt.**

**(5) Gate und Suite:** `gate_messung` auf dem sauberen Kopf (`_arbeit/gate/messung_27478ca_review2.json`, 56,7 s),
`pruefe_gate` gegen `nullmessung_f15d03f.json`: **nur (3) `M4.einraum` DG2 0 → 1**, M17 18/18 BESTANDEN; alle
Messfelder außer `meta` gleich `messung_d63bc4c-dirty-2f.json`. `pytest -m gate tests/gate`: 3 passed, 1 xfailed.
`pytest tests/raumerkennung tests/contract tests/gate`: **965 passed, 6 skipped, 2 xfailed, 0 failed**.
`tests/naht/test_s7_wohnungsklasse.py`, `test_soll_muthgasse.py`, `test_freiflaeche_wohnung.py`: 6 failed = genau die
6 bekannten (3 × `test_keine_leuchten_in_wohnung_privat` OG1/OG2/DG1, `test_soll_plan_tuerbloecke_im_modell`, die 2
S4c-Pins), 239 passed, 4 xfailed.

**Offen aus Review 2** (Beobachtungen, keine Widerlegung):

- **R2-01 (P1, gehört zur Owner-Bestätigung in § 16) · Selman:** „Tür mit Blatt an der Grenze" ist ein
  Abstandskriterium (Türpunkt bis halbe Türbreite + 300 mm an der Grenze), kein Türbezug. Am Rain OG3 `frei_1`: die
  auslösenden Türen `tuer_84` (`raum_27`|`raum_30`) und `tuer_86` (`raum_30`|`raum_35`) verbinden laut Modell andere
  Räume; die Grenze zum Wohnzimmer `raum_30` ist auf 4,3 m wandlos (eigene Messung ±1 mm). Das Ergebnis geht in die
  fail-safe Richtung (eigener Raum mit Notlicht statt Zuschlag in einen privaten Raum).
- **R2-02 (P2) · Selman:** Mollgasse 4.OG, freie Fläche 7,62 m² bei (2 826,7 / 1 751,5) m, 508 mm vom ZIMMER `raum_2`
  (`top_3`) — knapp über `NACHBAR_MM` = 500 und 0 % im ±250-mm-Umriss, bleibt darum frei („kein Nachbarraum bis
  500 mm"). Rand zu 59 % Wandkörper, kein TEXT/MTEXT im Modellbereich darin. Grenzfall der Definition, steckt in den
  109 Flächen außerhalb (§ 16).
- **R2-03 (P2) · Selman:** DG1 nach 2d 90,89 m² gegen den Stempel „Wohnzimmer 83,93" (= 73,95 + 9,98 AR, § 6.5).
  Anders als bei den drei Mollgasse-Zimmern bestätigt der Stempel den Zuschlag hier nicht; die Entscheidung trägt
  allein die Owner-Regel.
- **R2-04 (P2) · Selman:** Die Raster-Obergrenze und die Reißleine der R-Stufe (2f, R-05 a) melden sich nur als
  `RuntimeWarning` auf stderr, nicht in `bericht.md` und nicht in den Provider-Warnungen. Der Verlust stempelloser
  Restflächen wäre im Bericht nicht sichtbar.

---

## 20. Punkt 2g — übrige P0/P1 aus der Bestandsaufnahme, danach P2

**Auftrag (Owner 2026-09-30):** die Liste „Reihenfolge für Schritt 2g" (§ 11) in der Reihenfolge P0 → P1 → P2
abarbeiten, höchstens 6 Punkte; je Punkt nur innerhalb der Änderungsgrenze (Test zuerst rot, Fix, 12 Prüfpläne
über den Runner, Gate, Eintrag hier, ein Commit), fremde Lane nur melden; S4c bleibt unangetastet; keine Änderung,
die einen Prüfplan schlechter macht. Kopf zu Beginn `21e78b6` (Code = `27478ca`).

**Vorher** für alle Punkte = die Runner-Läufe nach 2f (Arbeitsbaum des 2f-Commits, 12 Prüfpläne aus
`tests/plaene.py`); Review 2 (§ 19) hat sie auf `27478ca` feldgleich bestätigt, `21e78b6` ändert nur Doku. Runner
wie § 12 (`provider.parse(dxf, "")` + Default-Platzierung, je Plan ein Prozess, allein), Vergleich des kompletten
JSON ohne Lauf-Metadaten (18 Felder). Runner, JSON und Logs liegen im Session-Scratch, nicht im Repo.

### 20.1 O-04 — `seite_fehlt` und Sanitärbefund im Bericht (erledigt mit dem Commit dieses Eintrags)

**Lücke:** `provider.tuer_warnungen` (`seite_fehlt`) und `provider.sanitaer_befund` (K3) standen nur am Provider,
`bericht.md` zeigte sie nicht (§ 5 O-04; `wand_warnungen` seit 2a).

**Rot vor dem Fix** (`pytest tests/raumerkennung/test_provider.py -k tuer_und_sanitaer --tb=line`, Kopf `21e78b6`,
Kurzform):

```
tests/raumerkennung/test_provider.py:257: AssertionError:  (3)
1 failed, 12 deselected in 2.96s
```

(Abschnitt „Warnungen (3)" enthielt nur `keine_wand_entities` und zwei „Polygon ohne Stempel".)

**Fix** (`scripts/plan_pruefen.py`, nur Berichtsausgabe): `_fachteil3` reicht zusätzlich `tuer_warnungen`
unverändert und `sanitaer_befund` mit Vorsatz `sanitaer: ` an „## Warnungen" (dieselbe Liste wie 2a/2d).

**Test:** `test_provider.py::test_plan_pruefen_schreibt_tuer_und_sanitaer_warnungen_in_bericht` (Prüfstrecke
end-to-end auf dem Hatch-Plan; der Parse setzt beide Listen fest, der Test bindet die Berichtsausgabe). Grün:
`test_provider.py` 12 passed, 1 skipped (`test_mollgasse_parse_valid`, wie vorher).

**Einmal-Lauf** `scripts/plan_pruefen.py` auf Rennweg OG3 (Ausgabe per `PLAN_PRUEFEN_ERGEBNIS` in den Scratch):
„## Warnungen (9)" mit `seite_fehlt: tuer_3 Seite +` und `Seite -` und `sanitaer: rest_6: BAD aus Sanitärbeleg
(DUSCHE 1, WASCHBECKEN 2, WC 1) im Umriss top_2 (Probe) …` — dieselben 2 + 1 Einträge, die der Runner am Provider
liest. Auf Am Rain kommen damit 23 (OG4) bis 186 (EG) `seite_fehlt`-Zeilen in den Bericht.

**Blast:** 12 Prüfpläne **12/12 feldgleich** zum Vorher (erwartet: der Runner liest den Provider, geändert ist nur
die Prüfstrecke). **Gate:** `gate_messung` auf dem Arbeitsbaum (`_arbeit/gate/messung_21e78b6-dirty-2gA.json`),
`pruefe_gate` gegen `nullmessung_f15d03f.json`: (0) unsauberer Arbeitsbaum (erwartet) und **(3) `M4.einraum` DG2
0 → 1** (Enis Board 3, unverändert); M17 18/18; alle Messfelder außer `meta` gleich `messung_27478ca_review2.json`.
`pytest -m gate tests/gate`: 3 passed, 1 xfailed.

`Projekte/_ergebnis/` nicht neu geschrieben (wie 2a–2f).

### 20.2 R-05 a — Verluste der Kaskade als Warnung statt nur `print` (erledigt mit dem Commit dieses Eintrags)

**Lücke:** die Raster-Obergrenze der R-Stufe ist seit 2f gebaut (§ 18), aber ein Fehler der R-Stufe (z. B.
`MemoryError`) wurde in `kaskade.py` gefangen und nur per `print` gemeldet; die R-Stufe war dann leer, stempellose
Stiegenhauskerne und Gänge fehlten still. Ebenso still: Fehler der Kürzel-Auflösung und der Bereinigung (§ 8
„Geschluckte Fehler"), die Raster-Grenzen der R-Stufe und die Reißleine der F-Stufe (nur `RuntimeWarning` auf
stderr; R2-04, R-04).

**Rot vor dem Fix** (`pytest tests/raumerkennung/test_provider.py tests/raumerkennung/test_stempel_flutung.py -k
"kaskade_fehler or rastergrenze or 2g_reissleine" --tb=line`, Kopf `755e06c`, Kurzform):

```
test_provider.py:277: AssertionError: ['keine_wand_entities: …']                      [loese_kuerzel]
test_provider.py:277: AssertionError: ['keine_wand_entities: …', 'keine_raeume: …']   [komponenten_ohne_stempel]
test_provider.py:277: AssertionError: ['keine_wand_entities: …']                      [bereinige_kaskade]
test_provider.py:295: AssertionError: ['keine_wand_entities: …', 'keine_raeume: …']   [reissleine]
test_provider.py:295: AssertionError: ['keine_wand_entities: …']                      [groeber]
test_stempel_flutung.py:204: Failed: DID NOT WARN (TypeError: flute_stempel() got an unexpected keyword argument 'warnungen')
6 failed, 23 deselected in 1.32s
```

Der Fall `komponenten_ohne_stempel` zeigt die Lücke direkt: der Plan verliert alle Räume, im Bericht stünde nur
`keine_raeume`, nicht warum.

**Fix** (`raumerkennung/`): `KaskadeErgebnis.warnungen` (neu, kein Contract-Feld). Die drei Fehlerschutz-Zweige in
`raeume_aus_kaskade` schreiben zusätzlich zum `print` `kaskade_fehler: <Stufe> <Ausnahme>: <Text> — <Folge>`;
`komponenten_ohne_stempel` und `flute_stempel` nehmen optional `warnungen` und hängen ihre Raster-Meldung als
`rest_stufe: …` bzw. `flutung: …` an (die `RuntimeWarning` bleibt). `provider.parse` hängt `k.warnungen` an
`wand_warnungen` — damit stehen sie über 2a/20.1 in bericht.md „## Warnungen".

**Tests:** `test_provider.py::test_kaskade_fehler_steht_in_den_warnungen[loese_kuerzel|komponenten_ohne_stempel|
bereinige_kaskade]` (Stufe per `monkeypatch` mit `MemoryError`, Parse läuft durch, Contract-Roundtrip),
`::test_rest_stufe_rastergrenze_steht_in_den_warnungen[reissleine|groeber]` (Grenzen wie 2f per `monkeypatch`),
`test_stempel_flutung.py::test_2g_reissleine_steht_in_der_warnungsliste`. Grün: `test_provider.py`,
`test_stempel_flutung.py`, `test_rest_komponenten.py`, `test_kaskade.py` 55 passed, 1 skipped.

**Blast:** 12 Prüfpläne **12/12 feldgleich** zu 20.1 (auch `warnungen`: keine Grenze und kein Fehler greift, wie in
2f gemessen). **Gate:** `_arbeit/gate/messung_755e06c-dirty-2gB.json`, `pruefe_gate` gegen
`nullmessung_f15d03f.json`: (0) unsauberer Arbeitsbaum (erwartet) und **(3) `M4.einraum` DG2 0 → 1**; M17 18/18;
alle Messfelder außer `meta` gleich `messung_27478ca_review2.json`. `pytest -m gate tests/gate`: 3 passed, 1 xfailed.

**Bleibt offen:** die F-Stufe selbst (`flute_stempel`) steht nicht im Fehlerschutz — ein Fehler dort bricht den
Parse weiter ab (am Code gelesen, `kaskade.py` Aufruf vor dem ersten `try`); auf den Prüfplänen nicht aufgetreten.
P2 · Selman.

### 20.3 D-04 — mm-Faktor aus `$INSUNITS` wird ausgewiesen (erledigt mit dem Commit dieses Eintrags; Hard Stop offen)

**Lücke:** ohne messbare Wand-Spanne fällt `_calibrate_factor` still auf `$INSUNITS` zurück (§ 7: 8 von 13 Plänen
der Prüfstrecke), die Türprobe wird dann nicht einmal gerechnet, und weder Faktor noch Quelle erscheinen irgendwo.
Owner-Frage (S-MST): Hard Stop oder nur Warnung. Gebaut ist nur der gemeinsame Teil beider Antworten — das
Ausweisen; der Faktor und die Kalibrierregel sind unverändert.

**Rot vor dem Fix** (`pytest tests/raumerkennung/test_provider.py -k mm_faktor --tb=line`, Kopf `5779ef6`, Kurzform):

```
test_provider.py:339: AssertionError: ['keine_wand_entities: …']    [insunits]
test_provider.py:339: AssertionError: ['keine_wand_entities: …']    [insunits_tuerprobe_10]
2 failed, 1 passed, 18 deselected in 1.25s
```

(`[wand_spanne]` grün = Gegenprobe: mit messbarer Spanne keine Meldung, vorher wie nachher.)

**Fix** (`raumerkennung/`): `_calibrate_factor` liefert `(Faktor, Quelle)`; `DxfPlan.faktor_quelle` (neu, Default
`""`) = `spanne`, `spanne+tuerbogen` oder `$INSUNITS=<Code> (keine Wand-Spanne 15–500 m messbar), Türprobe: <keine |
Faktor [— widerspricht]>`. Die Türprobe (`_door_arc_factor`) läuft im Rückfall nur noch zum Ausweisen mit, sie
entscheidet nichts. `provider.parse` schreibt im Rückfall `mm_faktor: <Faktor> aus <Quelle>` in `wand_warnungen` →
bericht.md „## Warnungen" (2a/20.1).

**Test:** `test_provider.py::test_mm_faktor_aus_insunits_steht_in_den_warnungen[insunits|insunits_tuerprobe_10|
wand_spanne]` (Hatch-Plan ohne Wand-Linien, derselbe mit drei Bögen r = 90 → Türprobe 10, Raum aus `A-WALL`-Linien
20 × 12 m). Grün: `test_provider.py` + `test_dxf_load.py` 24 passed, 2 skipped (wie vorher die zwei fehlenden
Fixtures).

**Gemessen** (`lade_dxf`, je Plan allein): Rennweg EG, Am Rain OG4, OG3, EG `Türprobe: 10 — widerspricht`; Am Rain
UG, OG1, OG2 `Türprobe: 1`; Rennweg OG3 `Türprobe: keine` — deckt sich mit § 7. Kosten der Türprobe je Plan < 0,1 s
(Am Rain EG: Laden 24,5 s).

**Blast:** 12 Prüfpläne gegen 20.2: **4/12 feldgleich** (Barawitzka EG, Mollgasse EG/1OG, Muthgasse E2 — Faktor aus
der Spanne), **8/12 nur in `warnungen` verschieden**, und dort genau um eine neue Zeile `mm_faktor: …` (alle 8
Rennweg-Geschosse; EG `Türprobe: 10 — widerspricht`, die übrigen 7 `Türprobe: keine`). Räume, Türen, Ausgänge,
Segmente, Anker, Leuchten: alle 12 gleich. **Gate:** `_arbeit/gate/messung_5779ef6-dirty-2gD.json`, `pruefe_gate`
gegen `nullmessung_f15d03f.json`: (0) unsauberer Arbeitsbaum (erwartet) und **(3) `M4.einraum` DG2 0 → 1**; M17
18/18; alle Messfelder außer `meta` gleich `messung_27478ca_review2.json`. `pytest -m gate tests/gate`: 3 passed,
1 xfailed.

**Offen (Owner):** Hard Stop oder Warnung bei `$INSUNITS`-Rückfall, und ob die Türprobe im Rückfall entscheiden
soll (4 × Widerspruch); S-MST nach dem Merge. P1 · Selman (Owner-Frage).

### 20.4 P0 R-09/F-07 — Am Rain OG4 ohne Stiegenhaus und Ausgang (nicht gebaut: Owner-Frage; Messung als Grundlage)

Owner-Frage aus § 11: welcher Beleg genügt für das Stiegenhaus, der Layer `Treppe` oder der Text „STGH"? Ohne
Entscheid keine Regel. Gemessen (OG4 allein, Kopf `6fe0bb8`; Skripte im Scratch):

- Text „STGH" (Layer `Raum-Beschriftung`) bei (12 320 / 12 909) mm liegt in `rest_2` — R-Stufe, ohne Typ, 40,17 m²,
  10 Türen. `raumtyp_flags("STGH")` = `STIEGENHAUS` (das Kürzel ist im Vokabular; auf Muthgasse typt ein
  „STGH"-Stempel so). Auf OG4 steht keine Flächenzeile daneben, darum ist der Text kein Stempel.
- Layer `Aufzug`: 325 Stützpunkte in einer Box 1,80 × 1,65 m, davon 311 in `rest_2`.
- Layer `Treppe`: 301 Stützpunkte über eine Box 46,0 × 20,8 m; **0 in `rest_2`**, 61 in `raum_19` (KÜCHE, `top_7`,
  `WOHNUNG_PRIVAT`), 240 in keinem Raum. Als Raumbeleg trifft der Layer auf OG4 den Kern nicht.
- Heute: 0 Ausgänge, 0 Stiegenhäuser, Segmente nur FALLBACK (4), Ausgangs-Warnung „kein Geschossausgang ableitbar",
  13 Leuchten, **davon 0 in `rest_2`** (der Kern mit „STGH" und Aufzug bekommt kein Notlicht).
- Gegenprobe in-memory (nicht gebaut, nicht committet: untypisierter Raum mit Text „STGH" → `STIEGENHAUS`):
  2 `stair_exit` (`exit_tuer_27`, `exit_tuer_28`), 1 Stiegenhaus, Segmente GRAPH 5 + FALLBACK 3, keine
  Ausgangs-Warnung, 20 Leuchten, davon 5 in `rest_2`.

**Offen:** Owner-Entscheid „Raumkürzel ohne Fläche als Typbeleg" (Option Text). Die Option Layer `Treppe` ist auf OG4
gemessen ohne Treffer im Kern. **P0** · Selman (Owner-Frage).

**Nachtrag 2026-10-02:** Owner-Entscheid 1 (2026-10-01, Option Text) → gebaut in § 23: `rest_2` STIEGENHAUS, 2
`stair_exit`, 1 Stiegenhaus, 20 Leuchten (= Gegenprobe). Korrektur zur Messung oben: neben „STGH" steht die
Flächenzeile „32.44 m²" (0,4 m darunter); der Stempel existiert, fand nur kein Polygon (`kein_polygon`), § 23.2.

### 20.5 P1 F-03 — Ausgang an einer Tür mit `von_raum == nach_raum` (nicht gebaut: S4c-Gebiet)

Barawitzka EG `tuer_31` (`arc+text:Eingang`, 950 mm, Rolle `hauseingang`) trägt den einzigen `final_exit`
`exit_tuer_31`; alle 7 GRAPH-Wege enden dort. Diagnose (Parse allein, Spion auf `ordne_tueren`):

- Bogen-Startwinkel 90° → Sehne senkrecht, Normale waagrecht. Seite +: bis 1 200 mm in der gedeckten Kontur, kein
  Raum. Seite −: 100–500 mm Wandkörper, bei 800/1 200 mm gedeckt, kein Raum. Ergebnis `KEIN_RAUM`|`KEIN_RAUM`. Nächster
  Raum `raum_35` STIEGENHAUS in 180 mm.
- Sehne aus dem Endwinkel (`blatt_enden[1]`): `raum_35`|`KEIN_RAUM` — die Außenseite bleibt gedeckte Fläche ohne Raum,
  nicht `AUSSEN`.

Nicht gebaut: (i) „Ausgang braucht eine Raumseite" nähme Barawitzka den einzigen Ausgang (STOPP, § 13); (ii) die
Sehnen-Korrektur für Türen mit **beiden** Seiten `KEIN_RAUM` ist die dokumentierte Grenze von S4c Fassung A
(`tuer_zuordnung.andere_bogenrichtung`, Docstring „Türen mit beiden Seiten KEIN_RAUM … bleiben", Ausbaupfad „Sehne aus
dem geschlossenen Blatt") — S4c bleibt unangetastet (Owner 2026-09-30). Die drei `stair_exit` im selben STIEGENHAUS
(Mollgasse EG `exit_tuer_68` in `raum_51`, F-13/S4g a; Am Rain UG `exit_tuer_186`, OG3 `exit_tuer_29`) sind nicht
diagnostiziert. **P1** · Selman, nach dem S4c-Entscheid.

### 20.6 P2 — VERLAUF-Befund „5 Restflächen / 9,47 m² entfallen" (geprüft, Messung ohne Code)

`docs/ZERFALL_SCHLITZ_PRUEFUNG.md` gelesen: § 4.1 führt 5 Stücke der Klasse (c) „echte Nutzfläche, darf nicht
entfallen", zusammen 9,471117 m², Stand `3d91a2c`. Die DXF dort sind dieselben wie in den heutigen Prüfplänen
(SHA-256 Barawitzka `76ed8b45…`, Mollgasse EG `4a0b6608…`, Muthgasse E2 `d840674b…`, gleich im Runner).
Probe: je Stück der Punkt aus dem Dokument (Schwerpunkt, bei `raum_90` der dort genannte „Punkt IM Stück") gegen
alle Modell-Räume des Runners nach 20.3:

| Stück (Dokument) | m² | heute |
|---|--:|---|
| Barawitzka `raum_43` „Terrasse" ZERFALL | 2,995052 | in `lift_3` (LIFT, `KEIN_RAUM`, 4,03 m², aus `finde_lifte`, 2,0 × 2,0 m) |
| Mollgasse EG `raum_25` ZIMMER ZERFALL | 1,938377 | in keinem Raum (nächster `raum_9` GANG 623 mm) |
| Muthgasse E2 `raum_88` „STGH" ZERFALL | 1,895620 | in keinem Raum (nächster `raum_67` 126 mm) |
| Muthgasse E2 `raum_90` Zimmer ZERFALL | 1,507416 | in keinem Raum (nächster `raum_54` VORRAUM 202 mm) |
| Mollgasse EG `raum_18` ZIMMER ZERFALL | 1,134652 | in keinem Raum (nächster `raum_56` GANG 423 mm) |

**Befund:** 4 von 5 Stücken (6,476 m²) liegen weiter in keinem Raum — für sie gilt der VERLAUF-Befund auch heute.
Das Barawitzka-Stück liegt heute in einem Liftpolygon; ob die Klasse (c) dort stimmt, ist offen (ein Liftschacht ist
keine Nutzfläche). Grenze der Probe: ein Punkt je Stück, keine Flächenbilanz (die Stück-Polygone liegen nicht im
Repo). **Offen:** der Zuschlag der (c)-Flächen wäre eine Änderung an den Bereinigungsregeln (§ 14.6.1,
`docs/ENIS_UEBERGABE_0908.md`) — nicht gebaut. P2 · Selman (Owner-Regel).

### 20.7 Übrige Listenpunkte ohne Bau

- **P0 [2f] Render-RAM:** erledigt in § 18 und von Review 2 bestätigt (§ 19 (4)); die VERLAUF-Zahlen sind dort
  nachgemessen (Render OG4 5,61 GB / 108 s je Bild, Spitze vorher 13,19 GB, nachher 3,02 GB).
- **P0 fremd, LIFT/SCHACHT-Leuchten (N-03, Leonis):** weiter nur gemeldet. Neu gesehen auf den 12 Prüfplänen (Runner,
  Zählweise `plan_pruefen._leuchten_je_klasse`, seit dem Basislauf unverändert): **Rennweg DG1 1 Rettungszeichen-
  leuchte (`rz`) in `rest_3` SCHACHT (2,30 m²)**, dazu Muthgasse E2 1 in LIFT (bekannt, § 6.8). Kein Code in
  `platzierung/`.
- **P1 S4g a–c, S4f, S3c, S-KG:** nach dem Merge des Türstapels (PR #160 offen) — nicht angefasst.
- **P1 S4c-Pins:** rot, nicht angefasst (§ 6.1).
- **Abgrenzung 2a–2d:** 2a–2f sind in § 12–19 geführt. Von den 2e-Kandidaten ist F-10 (Durchleitung) mit B entschieden
  (§ 17); F-06 (korrigierte Rolle an der Naht) bleibt Contract-Frage (§ 6.4).
- **P2 `docs/ZERFALL_SCHLITZ_PRUEFUNG.md`:** gelesen und geprüft (§ 20.6).

### 20.8 Stand nach 2g und Offenes nach Priorität

Gebaut: 3 Punkte (20.1 O-04, 20.2 R-05 a, 20.3 D-04), je ein Commit (`755e06c`, `5779ef6`, `6fe0bb8`). Gemessen ohne
Code: 3 Punkte (20.4 OG4, 20.5 F-03, 20.6 ZERFALL). Kein Prüfplan verliert Raum, Tür, Ausgang oder Leuchte (Blast je
Punkt, 12/12 gleich bis auf die neuen Warnungszeilen in 20.3).

**Volle Suite** (allein, Kopf `6fe0bb8`, 17 min 45 s): `6 failed, 2255 passed, 11 skipped, 6 deselected,
15 xfailed` — dieselben 6 roten wie nach 2f (3 × `test_keine_leuchten_in_wohnung_privat` OG1/OG2/DG1 = Board 1
Leonis, `test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell`, die 2 S4c-Pins), 2255 = 2245 + 10 neue
(20.1: 1, 20.2: 6, 20.3: 3), 0 xpassed; kein Test umgestellt, keine Schwelle, kein Soll, kein Marker angefasst.
**Gate auf dem sauberen Kopf** `6fe0bb8` (`_arbeit/gate/messung_6fe0bb8.json`, 105,8 s), `pruefe_gate` gegen
`nullmessung_f15d03f.json`: **nur (3) `M4.einraum` DG2 0 → 1** (Enis Board 3); M17 18/18; alle Messfelder außer
`meta` gleich `messung_27478ca_review2.json`.

**Offen, nach Priorität** (Zeilen-Nr. aus § 1–5 und § 11; eigene Lane, sofern nicht anders genannt):

- **P0:** R-09/F-07 Am Rain OG4 (Owner-Frage, § 20.4). R1-01 Abbruch bei `nan`/`inf`- oder Phantom-Koordinate auf
  einem Wand-Layer (`footprint.py:79/80`, Entscheid offen, § 15; nicht in der 2g-Liste). N-03 LIFT/SCHACHT-Leuchten
  (Leonis, gemeldet; neu Rennweg DG1 SCHACHT, § 20.7).
- **P1:** F-03 Ausgang an `tuer_31` (S4c-Gebiet, § 20.5). D-04 Hard Stop bei `$INSUNITS`-Rückfall (Owner, § 20.3).
  S4g a–c, S4f, S3c, S-KG (nach dem Merge). S4c-Pins (nicht anfassen). Aus § 11 unverändert offen: 8 N-07, 9 F-09,
  10 F-04/F-05, 13 D-05/D-07/R-02 (S3c), 14 R-05 b, 15 D-06/D-03, 16 F-13, 17 F-07 DD/UG, 18 R-10, 19 O-06 (außerhalb
  der Änderungsgrenze), 21 R-16, 23 F-06; fremd 24–29. `wand_warnungen` erreichen `pipeline.run`/API nicht (§ 12,
  gemeinsam).
- **P2:** F-Stufe ohne Fehlerschutz (§ 20.2). Zuschlag der ZERFALL-(c)-Flächen (§ 20.6). Faktor aus der Spanne steht
  nicht im Bericht (O-07, § 20.3). `Projekte/_ergebnis/` nicht neu geschrieben (wie 2a–2f). Übrige P2 aus § 11.

---

## 21. Abschluss (Kopf `e0c820d`, Prüfstrecke `8080655`)

**Auftrag (Owner 2026-09-30, Abschluss):** volle Suite, Gate, Schema-Check und ruff auf dem sauberen Kopf; die
Prüfstrecke über alle 13 Pläne (5 Prüfpläne, Mollgasse 1KG/2KG, Am Rain alle 6) in **einem** Lauf; Sammeleintrag in
`Projekte/_ergebnis/VERLAUF.md` und Abschnitt „Lückenstand 2026-09-30" in
`Projekte/_ergebnis_raumerkennung/VERSIONEN.md`; danach Sync mit `origin/main`, Push und PR (kein Merge).

### 21.1 Prüfung auf dem sauberen Kopf `e0c820d`

- **Volle Suite** (`pytest -q -p no:cacheprovider -rxXs`, allein, 17 min 48 s): `6 failed, 2255 passed, 11 skipped,
  6 deselected, 15 xfailed`, 0 xpassed — gleich § 20.8. Die 6 roten, alle erwartet:
  - `tests/naht/test_s7_wohnungsklasse.py::test_keine_leuchten_in_wohnung_privat[pfad0-OG1]`, `[pfad1-OG2]`,
    `[pfad3-DG1]` (`:1096`) — Board 1, Leonis;
  - `tests/naht/test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell` (`:423`, 30 von 72 gegen Band ≥ 40);
  - die S4c-Pins `tests/naht/test_s7_wohnungsklasse.py::test_bara_raum_19_behaelt_klasse_und_zirkulation` (`:937`) und
    `::test_bara_raum_30_wird_nicht_von_der_auswertungsreihenfolge_entschieden` (`:1055`) — S4c nicht angefasst (§ 6.1).

  Kein anderer roter Test, nichts zu untersuchen. 15 xfailed = die 14 aus § 10 und
  `test_s4g_ausgang_tuerbezug.py::test_soll_mollgasse_eg_kein_ausgang_ohne_tuerbezug` (S4g a, § 13). 11 skipped wie
  § 10 (Baufeld nicht entpackt, pyarrow fehlt, ODA-Konverter fehlt, `WHA_MOL_EG.dxf` fehlt, Herrenholz).
- **Gate:** `pytest -m gate tests/gate` 3 passed, 1 xfailed (`test_gate_tuerstapel_erfuellt`). `gate_messung` →
  `_arbeit/gate/messung_e0c820d.json` (59,6 s, Arbeitsbaum sauber), `pruefe_gate` gegen `nullmessung_f15d03f.json`:
  **nur (3) `M4.einraum` DG2 0 → 1** (Enis Board 3); M17 18/18 BESTANDEN; alle Messfelder außer `meta` gleich
  `messung_6fe0bb8.json`.
- **Schema:** `scripts/gen_schema.py --check` → „schema in sync" (kein Contract geändert). **ruff:** `ruff check .` →
  „All checks passed!".

### 21.2 Prüfstrecke: 13 Pläne in einem Lauf mit Plan-Render

`scripts/plan_pruefen.py` ohne Argument (13 DXF aus `Projekte/_eingang/` nach `Projekte/_ergebnis/`), ein Prozess,
allein auf dem Rechner, von außen alle 20 ms überwacht (Guard 26 GB, Runner im Session-Scratch wie § 18): **Exit 0,
kein Guard, 0 Traceback, 0 `MemoryError`, 0 `RuntimeWarning`**, 4 808,2 s, Prozess-Spitze **4,18 GB** (in Am Rain EG).
Im Log nur ezdxf-Kopierhinweise und 6 matplotlib-Hinweise „Ignoring fixed x/y limits". Alle 13 Pläne mit Bildern;
Am Rain UG, EG und OG1–OG3 erstmals (vorher nur `bericht.md` und `raeume.json`). **Das RAM-Ziel aus 2f ist erreicht**
(Spitze je Plan ≤ 8 GB, ein Lauf mit Render); der gemeinsame Lauf in § 18 hatte 4 829 s / 4,19 GB.

Kennzahlen je Plan (Räume = Kaskade gesamt; ohne Typ = Raum mit Polygon ohne `raum_typ`; Warnungen = Abschnitt
„Warnungen" in `bericht.md` = Provider-Warnungen (`keine_wand_entities`, `mm_faktor`, `seite_fehlt`, `sanitaer`,
`freiflaeche`) + Stempel/Polygon; RAM = höchster Working Set während des Plans, kleine Pläne tragen die Grundlast der
Pläne davor):

| Plan | Räume (ohne Typ) | Wohnungen | Türen typ./ges. | Ausgänge | Segmente | Leuchten | Warnungen gesamt = Provider + Stempel/Polygon | davon Wand/Lade (`keine_wand_entities`, `mm_faktor`) | Fluchtweg-Warn. | Laufzeit s | RAM GB |
|---|---|--:|---|---|---|---|---|---|--:|--:|--:|
| Barawitzka_EG | 46 (7) | 7 | 33/71 | final_exit 1 | GRAPH 7 FALLBACK 1 | rz 6 sicherheitsleuchte 5 | 37 = 24 + 13 | — | 8 | 254,6 | 1,44 |
| Mollgasse_EG | 62 (19) | 21 | 44/102 | final_exit 8 stair_exit 1 | LINIE 103 GRAPH 14 FALLBACK 3 | sicherheitsleuchte 27 rz 24 (2 in WOHNUNG_PRIVAT) | 60 = 21 + 39 | — | 8 | 245,5 | 1,37 |
| Muthgasse_E2 | 100 (6) | 22 | 113/193 | stair_exit 1 | LINIE 139 FALLBACK 3 | rz 86 sicherheitsleuchte 53 (62 in WOHNUNG_PRIVAT, 1 in LIFT) | 115 = 78 + 37 | — | 0 | 887,0 | 3,59 |
| Rennweg_EG | 23 (7) | 2 | 20/40 | stair_exit 3 final_exit 2 | GRAPH 5 FALLBACK 2 | rz 9 sicherheitsleuchte 8 | 16 = 12 + 4 | mm_faktor 1 | 8 | 49,2 | 1,38 |
| Rennweg_OG3 | 16 (1) | 2 | 17/18 | stair_exit 3 | GRAPH 5 FALLBACK 1 | rz 5 sicherheitsleuchte 2 | 10 = 4 + 6 | mm_faktor 1 | 0 | 47,4 | 1,27 |
| Mollgasse_1KG | 29 (24) | 0 | 0/28 | final_exit 1 | FALLBACK 4 | rz 7 sicherheitsleuchte 7 | 51 = 4 + 47 | — | 0 | 98,1 | 1,28 |
| Mollgasse_2KG | 28 (19) | 1 | 2/46 | stair_exit 1 | FALLBACK 2 GRAPH 1 | rz 8 sicherheitsleuchte 4 antipanik 1 (1 in LIFT) | 77 = 9 + 68 | — | 2 | 168,3 | 1,32 |
| AmRain_OG4 | 27 (3) | 11 | 22/58 | 0 | FALLBACK 4 | rz 8 sicherheitsleuchte 5 | 63 = 26 + 37 | keine_wand_entities 1, mm_faktor 1 | 0 | 126,0 | 1,26 |
| AmRain_UG | 82 (31) | 7 | 13/295 | stair_exit 4 final_exit 2 | FALLBACK 24 | rz 59 sicherheitsleuchte 32 (2 in WOHNUNG_PRIVAT) | 346 = 161 + 185 | keine_wand_entities 1, mm_faktor 1 | 10 | 401,0 | 1,93 |
| AmRain_EG | 135 (24) | 50 | 78/317 | final_exit 2 stair_exit 1 | FALLBACK 6 GRAPH 1 | rz 27 sicherheitsleuchte 13 (3 in WOHNUNG_PRIVAT) | 382 = 192 + 190 | keine_wand_entities 1, mm_faktor 1 | 12 | 1 038,5 | 4,16 |
| AmRain_OG1 | 134 (21) | 57 | 103/300 | stair_exit 4 | FALLBACK 17 GRAPH 6 | rz 47 sicherheitsleuchte 22 (2 in WOHNUNG_PRIVAT, 1 in SCHACHT) | 351 = 184 + 167 | keine_wand_entities 1, mm_faktor 1 | 0 | 570,3 | 1,83 |
| AmRain_OG2 | 102 (12) | 43 | 117/264 | stair_exit 2 | FALLBACK 15 GRAPH 9 | rz 52 sicherheitsleuchte 23 (3 in WOHNUNG_PRIVAT) | 279 = 122 + 157 | keine_wand_entities 1, mm_faktor 1 | 0 | 493,9 | 1,83 |
| AmRain_OG3 | 53 (8) | 23 | 61/129 | stair_exit 3 | GRAPH 10 FALLBACK 2 | sicherheitsleuchte 11 rz 9 (3 in WOHNUNG_PRIVAT) | 132 = 55 + 77 | keine_wand_entities 1, mm_faktor 1 | 0 | 360,2 | 1,60 |

**Gegen den Integrationsstand `bc2ccf0`** (`Projekte/_ergebnis/VERLAUF.md`, Eintrag „Integration"): Räume, ohne Typ,
Wohnungen, Türen typisiert, Ausgänge und Segmente 13/13 gleich; `raeume.json` 13/13 und `docs/MATERIAL_REPORT.md`
unverändert. Leuchten-Zahl je Art 12/13 gleich, Am Rain OG1 Sicherheitsleuchten 21 → 22 (`frei_2`, 2d, § 19 (2)). Neu
im Bericht die Provider-Warnungen (2a, 2d, 2g); Fluchtweg-Warnungen Barawitzka 11 → 8, Am Rain EG 13 → 12 und
Luftlinien-Zeilen der Weglängen-Tabelle Muthgasse −22, Barawitzka −3, Am Rain EG −2, OG2 −2 (2c, § 14). Jede
`bericht.md`-Änderung gegen `bc2ccf0` ist damit einem Punkt zugeordnet; die übrigen Zeilen sind die Laufzeit.

### 21.3 Gesamtstand — gebaut

| Punkt | Commit | vorher → nachher (Beleg) | Stand |
|---|---|---|---|
| 2a | `b849dd0` | leerer/defekter Plan: `ValueError` „DXF ohne Geometrie" bzw. `DXFTableEntryError` → RaumModell + Warnung (`keine_geometrie`, `keine_wand_entities`, `keine_raeume`); nicht lesbare Datei → `DxfNichtLesbar` (§ 12, 6 Tests rot → grün) | teilweise: R1-01 offen (§ 15) |
| 2b | `2016268` | Balkontür nie `final_exit` (0 Fälle auf 17 Plänen), Messfall Südgarten `exit_tuer_67`/`68` gepinnt; 17/17 feldgleich (§ 13) | b/c erledigt, **a offen** (STOPP: −10 von 14 GRAPH-Wegen, Leuchten 51 → 47) |
| 2c | `27de6a0` | fälschlich gekippte korrigierte Rollen 277 → 0 auf 31 Plänen, Leuchten 31/31 gleich, Fluchtweg-Warnungen −4 (§ 14) | erledigt |
| 2d | `22cd85e` | freie Flächen > 2 m² im Wohnungsumriss 16: 4 Zuschläge (Rennweg DG1 Wohnzimmer 73,95 → 90,89 m²), 12 neue Räume UNBEKANNT; 0 Verstöße im Blast (§ 16) | erledigt, Owner-Bestätigung der Definition offen (R2-01) |
| 2e | `d63bc4c` | Entscheidung B: kein Feld `durchleitung`, Board-Antrag geschlossen; Leonis liest keine Durchleitung, Platzierung synthetisch 5/5 gleich, ableitbar aus Klasse/Flags/GRAPH (§ 17) | entschieden, nichts gebaut |
| 2f | `27478ca` | Am Rain OG4 13,19 → 3,02 GB; Am Rain UG/EG/OG1–OG3 und Muthgasse vorher Guard ≥ 14 GB → ≤ 4,19 GB; 12 Prüfpläne feldgleich (§ 18, § 19) | erledigt, hier bestätigt (4,18 GB) |
| 2g | `755e06c`, `5779ef6`, `6fe0bb8`, `e0c820d` | O-04, R-05 a, D-04 als Warnung im Bericht (je rot → grün); Am Rain OG4, F-03, ZERFALL gemessen (§ 20) | 3 gebaut, 3 offen |
| Prüfstrecke | `8080655` | 13 Pläne in einem Lauf mit Render, Ergebnisse getrackt (21.2) | erledigt |

### 21.4 Gesamtstand — offen, nach Priorität

- **P0:** R-09/F-07 Am Rain OG4 ohne Stiegenhaus und Ausgang (Owner-Frage „STGH" als Typbeleg, § 20.4). R1-01 Abbruch
  bei `nan`/`inf`- oder Phantom-Koordinate auf einem Wand-Layer (§ 15). N-03 Leuchten in LIFT/SCHACHT (Leonis,
  gemeldet; Prüfstrecke: Muthgasse E2 1 LIFT, Mollgasse 2KG 1 LIFT, Am Rain OG1 1 SCHACHT).
- **P1:** S4c — 2 Pins rot, Owner-Entscheid (§ 6.1). S4g a — `footprint.hauptausgaenge` Mollgasse EG `exit_1` …
  `exit_4` ohne Tür (§ 13). F-03 Barawitzka `tuer_31` (§ 20.5). D-04 Hard Stop bei `$INSUNITS`-Rückfall (§ 20.3;
  8 von 13 Plänen der Prüfstrecke, 4 × „widerspricht"). Owner-Bestätigung 2d (R2-01) und Stempel in neuen
  UNBEKANNT-Räumen (§ 16). S4f, S3c, S-KG nach dem Merge. Gate (3) DG2 — Enis Board 3. Board 1 — Leuchten in
  `WOHNUNG_PRIVAT` (Leonis; Prüfstrecke: Muthgasse 62, Am Rain EG/OG2/OG3 je 3, Mollgasse EG, Am Rain UG/OG1 je 2).
  `wand_warnungen` erreichen `pipeline.run`/API nicht (§ 12, gemeinsam). PDF-Export ohne Mindeststrich (§ 18, O-03,
  gemeinsam). Aus § 11 unverändert: 8 N-07, 9 F-09, 10 F-04/F-05, 13 D-05/D-07/R-02, 14 R-05 b, 15 D-06/D-03, 16 F-13,
  17 F-07 DD/UG, 18 R-10, 19 O-06, 21 R-16, 23 F-06; fremd 24–29.
- **P2:** F-Stufe ohne Fehlerschutz (§ 20.2). Zuschlag der ZERFALL-(c)-Flächen (§ 20.6). O-07 Faktor aus der Spanne
  nicht im Bericht (§ 20.3). Restaussagen zur Durchleitung in `fluchtweg.py:24-26`, `provider.py:105-108`,
  `docs/GATE_TUERSTAPEL.md:903-907` (§ 17). R1-02, R2-02, R2-03 (§ 15, § 19). Am Rain OG4 `01_render.png` mit
  38-km-Weltausdehnung (D-05). Einzellauf eines OG parst den EG weiter selbst (§ 18). Erledigt aus § 20.8:
  „`Projekte/_ergebnis/` nicht neu geschrieben" (21.2).

## 22. Abschnitt 0 — die 12 UNBEKANNT-Räume (Typ vorher)

**Auftrag (Owner 2026-10-01, `docs/AUFTRAG_2026-10-01.md` § 0, Freigabe „Option 3, erweitert“):** die 12 neuen
UNBEKANNT-Räume `frei_*` aus 2d (§ 16, alle Am Rain) zeigen — Tabelle mit Plan, Geschoss, Raum-ID, Fläche,
Stempel/Kürzel im Polygon, Nachbarräumen und Türen; je Raum ein Ausschnittbild (Raum magenta, Stempeltext lesbar)
unter `Projekte/_ergebnis/AmRain_<Geschoss>/unbekannt/`. **Typ vorher** = Stand dieses Kopfs (alle 12 ohne
`raum_typ`, Klasse `None`, ohne Wohnung); **Typ nachher** nach Abschnitt 1 (§ 23, Runner `nachher` auf dem Arbeitsbaum
des § 23-Commits, Am Rain UG/EG/OG1–OG4 je allein): **alle 12 unverändert UNBEKANNT** — die Kürzel-Regel läuft in der
Kaskade, die `frei_*` entstehen erst danach im Provider (§ 16 „Einbau"); **nach Abschnitt 2** (§ 24, Runner
`nachher2` auf dem Arbeitsbaum des § 24-Commits): **7 typisiert** (VORRAUM 4, BALKON 2, ABSTELLRAUM 1), OG1 `frei_5`
UNBESTIMMT mit Grund (Doppelstempel ohne dominanten Stempel), 4 ohne Beleg UNBEKANNT. **Kein Code geändert**
(Abschnitt 0; der Code von Abschnitt 2 steht in § 24).

**Datenquelle.** `Projekte/_ergebnis/AmRain_*/raeume.json` trägt nur die Kaskaden-Räume (`scripts/plan_pruefen.py`
schreibt sie aus `raeume_aus_kaskade`; die `frei_*` entstehen erst in `provider.parse` nach `_tueren_und_wohnungen`,
§ 16 „Einbau“) — dort stehen sie also nicht. Darum ein eigener Parse auf diesem Kopf (`provider.parse(dxf, "")` +
Default-Platzierung, Runner wie § 12/§ 20, Am Rain UG/EG/OG1–OG4, je Plan ein Prozess; der Runner wickelt `lade_dxf`
nur im eigenen Prozess, um TEXT/MTEXT und `finde_stempel` desselben `DxfPlan` mitzuschreiben — kein Repo-Code).
Kennzahlen gegen die Prüfstrecke § 21.2 **6/6 gleich** (Türen typisiert/gesamt UG 13/295, EG 78/317, OG1 103/300,
OG2 117/264, OG3 61/129, OG4 22/58; Ausgänge UG stair 4 + final 2, EG final 2 + stair 1, OG1 stair 4, OG2 stair 2,
OG3 stair 3, OG4 0; Leuchten rz/SL UG 59/32, EG 27/13, OG1 47/22, OG2 52/23, OG3 9/11, OG4 8/5); Räume ohne Typ im
RaumModell = § 21.2 „ohne Typ“ + Anzahl `frei_*` (EG 24 + 4, OG1 21 + 5, OG2 12 + 1, OG3 8 + 1, OG4 3 + 1, UG 31 + 0).
Die 12 `frei_*` mit Fläche und Lage sind dieselben wie in § 16. Laufzeit und RAM dieses Laufs sind nicht belastbar
(zwei Runner-Ketten liefen versehentlich überlappend) und werden hier nicht ausgewiesen; die Felder sind
deterministisch (Kennzahlen oben).

**Spalten.** Lage = `representative_point` in m (Planeinheiten = mm, `mm_faktor 1 aus $INSUNITS=4`, § 20.3).
Stempel/Kürzel = jeder TEXT/MTEXT auf dem Layer `Raum-Beschriftung` (Am-Rain-Konvention: Kürzel-Zeile + Flächenzeile
+ Belag auf `Bodenfläche`), dessen Einfügepunkt im Polygon liegt — Rohtext nach Whitespace-Normierung. Weitere
Texte = alle anderen TEXT/MTEXT im Polygon (Rohtext, Layer). Nachbar = Raum mit Polygon ≤ 500 mm am
`frei_*`-Polygon (Schwelle wie `wohnungsumriss.umschliessende_wohnung`, hier **ohne** Neutral-Filter — Schacht/Rest
stehen mit). Tür = Türpunkt ≤ Breite/2 + 300 mm an der Grenze (ohne Breite 800 mm) — dieselbe Schwelle wie die
Trenner-Regel in § 16; Rolle = `tuer_detail` (— = unbestimmt), von→nach = `von_raum`→`nach_raum` (KEIN_RAUM = None),
Blatt ja = nicht `ohne_tuerblatt`. Die Türlisten enthalten alle Trenner-Türen aus § 16; dazu stehen hier Türen
innerhalb der Schwelle, die § 16 nicht nannte (EG `frei_1` `tuer_151`; OG1 `frei_3` und OG2 `frei_1`, wo § 16 über
die Öffnung zum Schacht entschied), und `durchgang_*` ohne Blatt, wo einer an der Grenze liegt.

| Plan | Geschoss | Raum-ID | Fläche m² | Lage (x, y) m | Stempel/Kürzel im Polygon — Layer `Raum-Beschriftung` (Rohtext, Lage m) | weitere Texte im Polygon (Rohtext, Layer) | Nachbarräume (ID, Typ, Abstand) | Türen (ID, Rolle, von→nach, Blatt) | Typ vorher | Typ nachher |
|---|---|---|--:|---|---|---|---|---|---|---|
| AmRain_EG | EG | `frei_1` | 16.57 | 37.0 / 21.7 | „12.78 m²“ (35.8 / 22.4); „VR“ (36.1 / 22.8) | „P_05“ (Fenster-Tür_NR); „EI“ (Beschriftung Brandschutz); „2“ (Beschriftung Brandschutz); „30“ (Beschriftung Brandschutz); „STUK=2,175 ü.FOK“ (Text 1_50); „Absturzsicherung H=102“ (Text 1_50); „OK= DUK“ (Text 1_50); „110“ (Beschriftung Fenster-Tür); „252“ (Beschriftung Fenster-Tür); „Handlauf H=90“ (Text 1_50); „Handlauf H=90“ (Text 1_50); „17 Stg“ (Beschriftung Stiege); „18,65/24“ (Beschriftung Stiege); „80“ (Beschriftung Fenster-Tür); „Parkett“ (Bodenfläche) | `raum_85` WC 0 mm; `frei_2` — 466 mm | `tuer_151` — KEIN_RAUM→AUSSEN Blatt ja; `tuer_172` — KEIN_RAUM→AUSSEN Blatt ja; `tuer_201` — KEIN_RAUM→KEIN_RAUM Blatt ja; `tuer_242` — KEIN_RAUM→raum_85 Blatt ja | UNBEKANNT | **VORRAUM** (WOHNUNG_PRIVAT, Flags 11; Kürzel »VR«, Polygon +30 % gegen Stempel) — § 24 |
| AmRain_EG | EG | `frei_2` | 3.92 | 33.4 / 19.9 | „3.37 m²“ (32.8 / 19.5); „AR“ (33.0 / 19.8) | „210“ (Beschriftung Fenster-Tür); „80“ (Beschriftung Fenster-Tür); „ker.Belag“ (Bodenfläche); „H“ (Verteiler) | `raum_85` WC 100 mm; `frei_1` — 466 mm | `tuer_151` — KEIN_RAUM→AUSSEN Blatt ja | UNBEKANNT | **ABSTELLRAUM** (WOHNUNG_PRIVAT, Flags 00; Kürzel »AR«, Polygon +16 %) — § 24 |
| AmRain_EG | EG | `frei_3` | 2.36 | 23.4 / 13.1 | — | „210“ (Beschriftung Fenster-Tür); „80“ (Beschriftung Fenster-Tür); „80“ (Beschriftung Fenster-Tür) | `raum_74` WOHNZIMMER 0 mm; `raum_91` VORRAUM 0 mm; `raum_92` WC 0 mm; `frei_4` — 1 mm; `raum_86` BAD 324 mm | `durchgang_59` zimmertuer raum_74→raum_91 Blatt nein; `tuer_157` zimmertuer raum_92→raum_91 Blatt ja; `tuer_214` — KEIN_RAUM→raum_74 Blatt ja; `tuer_249` — KEIN_RAUM→KEIN_RAUM Blatt ja | UNBEKANNT | UNBEKANNT (kein Text; Vorraum-Stich, Erscheinungsbild/zweite Meinung) — § 24 |
| AmRain_EG | EG | `frei_4` | 9.76 | 21.9 / 10.6 | „10.25 m²“ (21.7 / 11.3); „ZI 2“ (21.9 / 11.7) | „210“ (Beschriftung Fenster-Tür); „80“ (Beschriftung Fenster-Tür); „Parkett“ (Bodenfläche) | `raum_74` WOHNZIMMER 0 mm; `frei_3` — 1 mm | `tuer_214` — KEIN_RAUM→raum_74 Blatt ja; `tuer_216` — KEIN_RAUM→AUSSEN Blatt ja; `tuer_249` — KEIN_RAUM→KEIN_RAUM Blatt ja | UNBEKANNT | UNBEKANNT (»ZI 2« ohne Wörterbuch-Treffer, § 23.5 Owner-Entscheid) — § 24 |
| AmRain_OG1 | 1OG | `frei_1` | 11.17 | 149.3 / 49.3 | „3.88 m²“ (148.4 / 49.8); „BALKON“ (148.4 / 50.2) | „221“ (Beschriftung Fenster-Tür); „223“ (Beschriftung Fenster-Tür); „Betonpl.“ (Bodenfläche); „TW raumhoch“ (Parapethöhe 1_100) | `raum_30` BALKON 0 mm; `raum_40` KÜCHE 0 mm | `tuer_51` — KEIN_RAUM→KEIN_RAUM Blatt ja | UNBEKANNT | **BALKON** (AUSSEN, Flags 00; Kürzel »BALKON«, Polygon +188 %, nimmt Nachbar-Loggien mit) — § 24 |
| AmRain_OG1 | 1OG | `frei_2` | 6.75 | 95.8 / 44.9 | — | „Handlauf H=90“ (Beschriftung Stiege); „Handlauf H=90“ (Beschriftung Stiege); „17 STG 17/29“ (Beschriftung Stiege); „17 STG 17/29“ (Beschriftung Stiege); „210“ (Beschriftung Fenster-Tür) | `raum_4` GANG 0 mm | `tuer_13` wohnungseingang raum_4→raum_12 Blatt ja; `tuer_22` — KEIN_RAUM→KEIN_RAUM Blatt ja; `tuer_23` — KEIN_RAUM→raum_4 Blatt ja; `tuer_39` — raum_4→AUSSEN Blatt ja | UNBEKANNT | UNBEKANNT (kein Text; wohnungsinterne Stiege) — § 24 |
| AmRain_OG1 | 1OG | `frei_3` | 3.99 | 54.0 / 9.0 | „VR“ (53.6 / 7.6) | „STUK=2,175 ü.FOK“ (Text 1_1000) | `raum_81` BAD 0 mm; `raum_86` GANG 0 mm; `rest_10` SCHACHT 0 mm | `durchgang_35` wohnungseingang raum_81→raum_86 Blatt nein; `tuer_170` — KEIN_RAUM→KEIN_RAUM Blatt ja; `tuer_205` — KEIN_RAUM→raum_86 Blatt ja | UNBEKANNT | **VORRAUM** (WOHNUNG_PRIVAT, Flags 11; Kürzel »VR« ohne Flächenzeile im Polygon) — § 24 |
| AmRain_OG1 | 1OG | `frei_4` | 2.39 | 51.5 / -1.1 | „7.67 m²“ (51.2 / -0.8); „LOGGIA“ (51.2 / -0.4) | „Betonpl.“ (Bodenfläche) | `raum_66` WOHNZIMMER 272 mm | — | UNBEKANNT | **BALKON** (AUSSEN, Flags 00; Kürzel »LOGGIA«, Polygon −69 %) — § 24 |
| AmRain_OG1 | 1OG | `frei_5` | 18.19 | 12.7 / 44.7 | „5.35 m²“ (11.8 / 43.7); „BAD“ (11.9 / 44.1); „7.68 m²“ (13.3 / 45.4); „GANG“ (13.4 / 45.7); „5.34 m²“ (11.6 / 46.3); „KOCHNISCHE“ (11.2 / 46.6) | „210“ (Beschriftung Fenster-Tür); „E-Verteiler“ (Verteiler); „WM“ (Sanitär); „KS“ (Sanitär); „GS“ (Sanitär); „ker. Belag“ (Bodenfläche); „210“ (Beschriftung Fenster-Tür); „80“ (Beschriftung Fenster-Tür); „Parkett“ (Bodenfläche); „Parkett“ (Bodenfläche) | `raum_36` WC 0 mm | `tuer_103` — AUSSEN→KEIN_RAUM Blatt ja; `tuer_95` balkontuer raum_36→AUSSEN Blatt ja; `tuer_96` — KEIN_RAUM→KEIN_RAUM Blatt ja | UNBEKANNT | UNBESTIMMT mit Grund (Notlicht): »BAD«, »GANG« nicht eindeutig, kein dominanter Stempel (BAD 5,35 = 29 %, GANG 7,68 = 42 % der 18,19 m²; KOCHNISCHE kein Wörterbuch-Treffer) — § 24.2 |
| AmRain_OG2 | 2OG | `frei_1` | 3.99 | 54.0 / 9.0 | „VR“ (53.6 / 7.6) | „STUK=2,175 ü.FOK“ (Text 1_1000) | `raum_51` BAD 0 mm; `raum_65` GANG 0 mm; `rest_9` SCHACHT 0 mm | `durchgang_30` wohnungseingang raum_51→raum_65 Blatt nein; `tuer_154` — KEIN_RAUM→KEIN_RAUM Blatt ja; `tuer_206` — KEIN_RAUM→raum_65 Blatt ja | UNBEKANNT | **VORRAUM** (WOHNUNG_PRIVAT, Flags 11; Kürzel »VR« ohne Flächenzeile im Polygon) — § 24 |
| AmRain_OG3 | 3OG | `frei_1` | 2.73 | 61.1 / 11.6 | „5.13 m²“ (60.9 / 11.8); „VR“ (61.1 / 12.2) | „E-Verteiler“ (Verteiler); „Parkett“ (Bodenfläche) | `raum_27` BAD 0 mm; `raum_30` WOHNZIMMER 0 mm; `raum_35` GANG 56 mm | `tuer_84` zimmertuer raum_27→raum_30 Blatt ja; `tuer_86` wohnungseingang raum_30→raum_35 Blatt ja; `tuer_98` — raum_30→KEIN_RAUM Blatt ja | UNBEKANNT | **VORRAUM** (WOHNUNG_PRIVAT, Flags 11; Kürzel »VR«, Polygon −47 %) — § 24 |
| AmRain_OG4 | 4OG | `frei_1` | 5.41 | 56.9 / 8.7 | — | „DDB 112/35“ (Deckendurchbruch_ Aussparung); „FDB 112/35“ (Fussbodendurchbruch); „S4-4“ (004-RAI_EN_GR_HKLS_EG_01_Grundriss HKLS EG$0$SIMA_HKLS_Schachtnummer); „Haltegriff“ (Text 1_50); „DACHAUSSTIEG“ (Beschriften); „über Leiter von OG3“ (Beschriften); „Luftraum“ (Beschriften); „Fuge mit“ (Beschriften); „eingespachtelten“ (Beschriften); „Fugenband schließen“ (Beschriften); „RA mind. 1m²“ (Beschriften); „Dachausstieg“ (Beschriften) | `raum_14` ABSTELLRAUM 265 mm | `tuer_45` — KEIN_RAUM→AUSSEN Blatt ja | UNBEKANNT | UNBEKANNT (kein Raumstempel; Dachausstieg/Luftraum) — § 24 |

**Bilder** (12, `Projekte/_ergebnis/AmRain_<Geschoss>/unbekannt/<raum_id>.png`, längste Seite 1 400 px, PNG mit
Palette ≤ 256 Farben, 58–96 kB; Plan-Render des ganzen Geschosses über das ezdxf-Zeichen-Addon wie `plan_pruefen._figur`,
Ausschnitt = Polygon-Box + max(2,5 m, 40 %), Raum magenta, Nachbarn hellblau mit ID/Typ, Türen der Tabelle rot
markiert, 1-m-Balken unten links, Titel mit Raum-ID, Fläche, Typ vorher und den `Raum-Beschriftung`-Texten im
Polygon). Alle 12 selbst angesehen; Stempeltext ist auf jedem Bild lesbar, auf dem einer liegt.

**Befund je Raum (am Bild, kein Entscheid):**

- **EG `frei_1`** (VR 12,78): Vorraum einer Maisonette-Wohnung (Stiege „17 Stg 18,65/24“ mit Handlauf im Polygon,
  Absturzsicherung) — das Polygon greift über das VR hinaus: Dreiecke nach Norden über die Fassade (Fenstertür
  `P_05`, Pfeil 2_06) und nach Süden bis zum Eingang 2_06. 16,57 m² gegen 12,78 m² Stempel.
- **EG `frei_2`** (AR 3,37): Abstellraum mit WC-Nachbar; ein Zipfel ragt durch die Wandlücke neben `tuer_151` in
  „ZI 1 9,32 m²“ (ZI 1 hat selbst kein Polygon). 3,92 gegen 3,37 m².
- **EG `frei_3`** (kein Stempel): Stich des Vorraums zwischen `raum_91` VORRAUM, WC `raum_92` und den Türen zu ZI 1 /
  ZI 2 (`tuer_214`, `tuer_249`) — ein Vorraum-Rest, kein eigener Raum im Plan.
- **EG `frei_4`** (ZI 2 10,25): vollständiges Zimmer (Bett, Schrank, Fenstertür `tuer_216` zur Terrasse). 9,76 gegen
  10,25 m². Der Stempel ist für `finde_stempel` **kein Stempel**, weil `raumtyp_flags("ZI 2")` = None („ZI“ fehlt im
  Wörterbuch); darum stand er in § 16 nicht.
- **OG1 `frei_1`** (BALKON 3,88): Balkon samt angrenzenden Loggia-Streifen entlang der Fassade — Außenfläche;
  11,17 gegen 3,88 m² (das Polygon nimmt die Nachbar-Loggien mit).
- **OG1 `frei_2`** (kein Stempel): **wohnungsinterne Stiege** („17 STG 17/29“ ×2, Handlauf, Absturzsicherung) neben
  dem Gang `raum_4`, mit `tuer_22`/`tuer_23` im Stiegenauge; kein Stiegenhaus (liegt in der Wohnung, R-09 nicht
  betroffen).
- **OG1 `frei_3`** (VR, Flächenzeile außerhalb): Teil des Vorraums „VR 9,62 m²“ an der Wohnungstür 4_05 vom STGH
  (`tuer_205`); der Einfügepunkt der Flächenzeile „9.62 m²“ liegt im 1,4-m²-Schachtpolygon `rest_10` SCHACHT
  (E-Verteiler, FDB/DDB 75/40) direkt unter dem Kürzel, der übrige VR-Teil hat kein Polygon. `raum_86` GANG
  (20,07 m², Wohnung `top_50`) grenzt von oben an.
- **OG1 `frei_4`** (LOGGIA 7,67): Loggia (Außenfläche), Polygon deckt 2,39 von 7,67 m²; `raumtyp_flags("LOGGIA")` =
  BALKON (im Wörterbuch, Kanon-Typ).
- **OG1 `frei_5`** (BAD 5,35 + GANG 7,68 + KOCHNISCHE 5,34): **drei Räume in einem Polygon** (Wände zwischen
  Kochnische, Bad und Gang nicht als Wandkörper erkannt), Summe 18,37 ≈ 18,19 m². Ein Typ aus dem Stempel ist hier
  nicht eindeutig; „KOCHNISCHE“ fehlt zudem im Wörterbuch (`raumtyp_flags` = None).
- **OG2 `frei_1`** (VR, Flächenzeile außerhalb): dieselbe Lage wie OG1 `frei_3` ein Geschoss höher, Wohnungstür
  4_11; Flächenzeile „9.86 m²“ wieder im Schachtpolygon `rest_9` SCHACHT (1,4 m²), Gang `raum_65` (20,07 m²,
  `top_24`) grenzt von oben an.
- **OG3 `frei_1`** (VR 5,13): Vorraum an der Wohnungstür 4_23 (`tuer_86` wohnungseingang), Polygon 2,73 von 5,13 m²;
  Nachbar `raum_30` WOHNZIMMER ist großflächig ausgelaufen (deckt ZI 1 und Kochnische mit).
- **OG4 `frei_1`** (kein Stempel): **Dachausstieg/Luftraum** („DACHAUSSTIEG über Leiter von OG3“, „Luftraum“,
  „Haltegriff“, „RA mind. 1m²“, Deckendurchbrüche) neben einer Lift-Überfahrt („LIFT-ÜBERFAHRT“ im Bild), Nachbar
  nur `raum_14` ABSTELLRAUM (265 mm), `tuer_45` KEIN_RAUM→AUSSEN. Kein begehbarer Raum des Geschosses. Zum
  STGH-Kern `rest_2` aus § 20.4 (Text „STGH“ bei 12,3 / 12,9 m) sind es 33,5 m — ein anderer Kern; die Lesart in
  § 16 („liegt am Treppen-/Liftkern“) meint diesen Lift, nicht das Stiegenhaus von R-09.

**Abgleich mit § 16.** Dort „Stempel in der Fläche“ in 6 der 12 Räume; nach dem Rohtext hier **9**: zusätzlich EG
`frei_4` („ZI 2 / 10.25 m²“ — kein Wörterbuch-Treffer, deshalb kein `Stempel`-Objekt), OG1 `frei_3` und OG2 `frei_1`
(„VR“ ohne Flächenzeile im Polygon). Ohne jeden `Raum-Beschriftung`-Text bleiben 3: EG `frei_3` (Vorraum-Stich), OG1
`frei_2` (Stiege in der Wohnung), OG4 `frei_1` (Dachausstieg). Davon hat OG1 `frei_5` drei Stempel, die anderen
8 genau einen.

**Für Abschnitt 1/2 (Hinweise, keine Entscheide):** (a) Kürzel ohne Wörterbuch-Treffer in den 12 Räumen: „ZI“ /
„ZI 2“ (Kanon ZIMMER — Wörterbuch-Eintrag, kein neuer Typ), „KOCHNISCHE“ (Kanon-Kandidat KÜCHE — Owner); (b) „VR“ als
Kürzel **ohne** Flächenzeile im Polygon (OG1 `frei_3`, OG2 `frei_1`) ist der Fall „Kürzel ist Beleg auch ohne
Flächenzeile“ aus § 1 des Auftrags; (c) ein Polygon mit mehreren Stempeln (OG1 `frei_5`) ist nicht eindeutig →
UNBESTIMMT mit Grund, bis die Fläche getrennt ist; (d) BALKON/LOGGIA typen zu BALKON (Kanon), eine AUSSEN-Frage stellt
sich nicht; (e) die drei Räume ohne Text sind nur über das Erscheinungsbild (Stiege, Dachausstieg, Vorraum-Rest) oder
die zweite Meinung (Abschnitt 3) zu typen.

**Offen nach Abschnitt 0:** Spalte „Typ nachher“ für Abschnitt 2 (nach Abschnitt 1 alle 12 UNBEKANNT, § 23) —
**gefüllt mit § 24**; die Polygonform der `frei_*` (Überlauf durch Wandlücken, drei Räume in einem Polygon) ist nicht
Teil dieses Auftrags.

## 23. Abschnitt 1 — Kürzel sind Beleg (Entscheid 1; erledigt mit dem Commit dieses Eintrags)

**Auftrag (Owner 2026-10-01, `docs/AUFTRAG_2026-10-01.md` § 1, Entscheid 1):** „Ein Raumkürzel gilt als Beleg für den
Typ, auch ohne Flächenzeile. Bedingung: Der Text liegt innerhalb des Raumpolygons, nicht in Legende, Plankopf oder an
Schnitt-/Achsmarken." Bestehende Tabelle erweitern, nicht neu erfinden; kein neuer RaumTyp; mehrdeutige Kürzel bleiben
UNBESTIMMT mit Notlicht; Erscheinungsbild schlägt Kürzel; Test zuerst rot an Am Rain OG4 (`rest_2` „STGH" →
STIEGENHAUS, Abnahme 1 Stiegenhaus, 2 `stair_exit`, 20 Leuchten = Gegenprobe § 20.4).

### 23.1 Inventur (Runner `vorher`, Code `e0c820d` = `dad7bbd`, 13 Pläne der Prüfstrecke)

Methode: je Plan `provider.parse` + Default-Platzierung im eigenen Prozess (Runner wie § 12/§ 20/§ 22, Scratch
außerhalb des Repos); alle TEXT/MTEXT des Modellraums, deren Einfügepunkt in einem Raumpolygon des RaumModells liegt
(kleinster deckender Raum), mit ≥ 2 Buchstaben, ohne m²-Muster, kein Belag, ≤ 40 Zeichen. Ergebnis: **5 106
Text-in-Raum-Treffer, 1 335 Normtexte** (Rohtext, Layer, Häufigkeit, Plan, Raumtyp des deckenden Raums). Die drei
Gruppen, die zählen:

**(a) Kürzel mit Kanon-Typ** (Kürzel-Form, Wörterbuch-Treffer — alles schon in `raumtyp.py`; **kein neuer Eintrag
nötig**, die Mindestmenge STGH/VR/AR/BAD stand bereits drin). Spalte „heute" = Typ des Raums, in dem der Text liegt
(„—" = untypisiert → Kandidat für diese Regel):

| Kürzel (Normtext) | Rohvarianten | → Kanon | n | Layer | Pläne (Treffer) | heute |
|---|---|---|--:|---|---|---|
| VR | VR | VORRAUM | 78 | Raum-Beschriftung, 0._EG PP_2_810 Raum | Am Rain EG 25, OG1 17, OG2 18, OG3 10, OG4 4, Barawitzka 4 | VORRAUM 28, KÜCHE 12, WOHNZIMMER 8, GANG 6, STIEGENHAUS 3, TERRASSE 2, — 19 |
| BAD | BAD, Bad | BAD | 66 | Raum-Beschriftung, PP_2_810, A-AREA-IDEN | Am Rain 49, Barawitzka 3, Muthgasse 14 | BAD 59, GANG 2, VORRAUM 2, MUELLRAUM 1, WOHNZIMMER 1, — 1 |
| WC | WC | WC | 61 | Raum-Beschriftung, PP_2_810, A-AREA-IDEN | Am Rain 55, Barawitzka 3, Muthgasse 3 | WC 46, — 10, je 1 KÜCHE/VORRAUM/STIEGENHAUS/BAD/SCHACHT |
| BAD/WC | BAD/WC, Bad/WC | BAD | 58 | Raum-Beschriftung, PP_2_810 | Am Rain 57, Barawitzka 1 | BAD 57, — 1 |
| LOGGIA | Loggia, LOGGIA | BALKON | 49 | Raum-Top-Beschriftung, Raum-Beschriftung, PP_2_810, A-AREA-IDEN | Am Rain 35, Barawitzka 2, Muthgasse 12 | BALKON 23, TERRASSE 10, KÜCHE 4, WOHNZIMMER 2, STIEGENHAUS 1, — 9 |
| GANG | GANG, Gang | GANG | 46 | Raum-Beschriftung, A-AREA-IDEN | Am Rain 43, Muthgasse 3 | GANG 26, KÜCHE 4, VORRAUM 2, WOHNZIMMER 2, ABSTELLRAUM 1, — 11 |
| WOHNKÜCHE | WOHNKÜCHE, Wohnküche | KÜCHE | 45 | Raum-Beschriftung, PP_2_810, A-AREA-IDEN | Am Rain 27, Barawitzka 4, Muthgasse 14 | KÜCHE 43, — 2 |
| WOHNRAUM | WOHNRAUM | WOHNZIMMER | 45 | Raum-Beschriftung | Am Rain 45 | WOHNZIMMER 32, GANG 3, je 1 BALKON/KÜCHE/TERRASSE, — 7 |
| AR | AR | ABSTELLRAUM | 45 | Raum-Beschriftung, PP_2_810, A-AREA-IDEN | Am Rain 37, Barawitzka 2, Muthgasse 6 | ABSTELLRAUM 37, WC 3, je 1 MUELLRAUM/WOHNZIMMER/VORRAUM, — 2 |
| TERRASSE | TERRASSE, tERRASSE, Terrasse | TERRASSE | 28 | Raum-Beschriftung, PP_2_810 | Am Rain 24, Barawitzka 4 | TERRASSE 19, BALKON 4, — 5 |
| BALKON | BALKON, Balkon | BALKON | 23 | Raum-Beschriftung, A-AREA-IDEN | Am Rain 22, Muthgasse 1 | BALKON 10, KÜCHE 3, WOHNZIMMER 2, GANG 2, — 6 |
| ZIMMER | Zimmer | ZIMMER | 21 | PP_2_810, A-AREA-IDEN | Barawitzka 6, Muthgasse 15 | ZIMMER 21 |
| STGH | STGH | STIEGENHAUS | 13 | Raum-Beschriftung | Am Rain EG 3, OG1 1, OG2 4, OG3 2, OG4 1, UG 2 | STIEGENHAUS 12, **— 1 (OG4 `rest_2`)** |
| KÜCHE | KÜCHE | KÜCHE | 12 | Raum-Beschriftung | Am Rain 12 | KÜCHE 10, — 2 |
| SCHLEUSE | Schleuse, SCHLEUSE | SCHLEUSE | 10 | Text 1_20, Raum-Beschriftung | Am Rain UG 10 | SCHLEUSE 8, — 2 |
| VORR. | Vorr. | VORRAUM | 9 | A-AREA-IDEN | Muthgasse 9 | VORRAUM 8, BAD 1 |
| RESTMÜLL | Restmüll, RESTMÜLL | MUELLRAUM | 8 | Muellgefaesse, 02-TXT, New_160 | Am Rain EG 1, Mollgasse EG 4, Rennweg EG 3 | MUELLRAUM 8 |
| FAHRRADRAUM · FLUR · KIWA | — | ABSTELLRAUM · GANG · KINDERWAGENRAUM | 7 · 7 · 7 | Raum-Beschriftung, A-AREA-IDEN | Am Rain UG/EG, Muthgasse | ABSTELLRAUM 7 · GANG 7 · KINDERWAGENRAUM 6, SCHLEUSE 1 |
| TREPPENHAUS, TREPPENHAUS 1/2 | — | STIEGENHAUS | 6 + 2 | Raum-Beschriftung, PP_2_810 | Am Rain UG 6, Barawitzka 2 | STIEGENHAUS 7, — 1 |
| MÜLLRAUM · WC/DU · GARAGE 1/2 · ASR · GARD. · GARDEROBE · TEEKÜCHE · TECHNIK · FW-AUFZUG · WASCHKÜCHE | — | je Wörterbuch | 4 · 4 · 2 · 1 · 1 · 1 · 1 · 1 · 1 · 1 | div. | div. | GARAGE 1/2 (Layer E_Bauangaben, Am Rain UG) und GARDEROBE (Rennweg EG, Beschriftungslayer) liegen in untypisierten Räumen |

**(b) Mehrdeutig / Kandidat** (typisieren nie, Grund in den Bericht): **SR** 4× (Barawitzka EG `raum_27` 4,51 m²
„SR 4,51 m2", Muthgasse E2 3× — 3 davon in untypisierten Räumen) = Schlafraum oder Schutzraum; **TR** 0× (Auftrag:
Trockenraum/Technikraum); **KA** als „KA 101"/„KA401" ~110× (Kellerabteil-Nummern Am Rain UG, oft im Gang-Polygon,
nicht im Abteil) und „Zul.KA" 3× (Zuluft Kellerabteil — Lüftung); **Schl.** 2× (Muthgasse, `kuerzel_entscheid`,
unverändert).

**(c) Wörterbuch-Treffer ohne Kürzel-Form — zählen bewusst NICHT** (59 Normtexte; ohne Form-Regel würden sie Räume
falsch typen): Stufen-Beschriftung „20 STG 19/29" (16×, **davon 8 in untypisierten Räumen** — wohnungsinterne
Stiegen in Am Rain EG/UG → wären STIEGENHAUS geworden), „17 STG 17/29", „1 Stg 20/24", „15 STG" usw. (Token `stg` steht
im Wörterbuch); Höhenkoten „STUK = 225 ü. FOK STGH = -0.70" (Mollgasse, 8×); Summenblock „Wohnfläche (inkl.Loggia)",
„Terrasse/Balkon/Garten" (Raum-Top-Beschriftung, 54×, davon 15 in untypisierten Räumen → wären BALKON/TERRASSE);
Fließtext „Luftraum Garage", „Gully Müll", „T KiWa", „Lüftung Schleuse", „KA STG1 (+1)", „RDUK Balkon = +1.58";
Fragment „Schacht-" (+ „entlüftung" + „seitlich", Am Rain OG2/OG4, 5×).

**(d) Kürzel-Form auf Raumlabel-Layern ohne Wörterbuch-Treffer** (bleiben untypisiert; Kandidaten für Wörterbuch
oder Kanon — **Owner/Enis, hier nicht entschieden**): KOCHNISCHE 35× (Kanon-Kandidat KÜCHE), **ZI 1/2/3** 43× (Kanon
ZIMMER — s. 23.5, gemessen und bewusst nicht aufgenommen), GARTEN 19× (kein Kanon-Typ; Abschnitt 5 nennt ihn als
Außen-Beleg), ELEKTRO 11× (TECHNIK?), MECH.ENTL. 10×, ARBEITSNISCHE 8×, TOP 01/02 13× (Wohnungsnummer), SPEIS 2×
(ABSTELLRAUM?), KELLERABTEILE 1/2 4× (KELLER? Kompositum ≠ `kellerabteil`), HAUSKELLER 1× (KELLER?), MAGAZIN n.m 7×
(LAGER?), PROVIDERRAUM, WASSERZÄHLER, RAMPE, EIGENGARTEN, KLEINKINDERSPIELPLATZ, HAUS1–5, STIEGE (Muthgasse, in
LIFT-Räumen), AUFZUG 1/2 und Schrankr./TV Raum/Geschäftslokal (Vokabular-Fälle Enis, unverändert).

### 23.2 Regel und Einbau (`raumerkennung/kuerzel_beleg.py`, Aufruf `kaskade.py` nach R-Stufe und Bereinigung)

- **Ausschlussregel (festgelegt):** (1) Der Einfügepunkt liegt in einem Raumpolygon — alles andere zählt nicht;
  Legende und Plankopf liegen im Papierbereich (nie gelesen) oder außerhalb der Gebäudekontur (die R-Stufe baut nur in
  der größten Wandkörper-Komponente); auf den 13 Plänen liegt **kein** Text mit `Legende|Plankopf|Schriftfeld` im
  Modellraum in einem Raumpolygon (gemessen); zusätzlich zählt kein Text auf einem Layer `LEGEND|PLANKOPF|SCHRIFTFELD|
  TITEL|TITLE`. (2) **Kürzel-Form:** ein Buchstabenwort (`.`, `/`, `-` erlaubt), optional eine ein- bis zweistellige
  Zählnummer („ZI 2", „TREPPENHAUS 1"), jedes Buchstaben-Token ≥ 2 Zeichen, kein Trennstrich am Ende; bei `/` müssen
  alle Teile im Wörterbuch stehen („BAD/WC" ja, „WC/DU", „Terrasse/Balkon/Garten" nein). Damit sind Achs-/Schnittmarken
  („A", „1", „A-A"), Stufen, Höhenkoten, Summenblöcke und Fließtext ausgeschlossen (23.1 c). (3) Typ nur aus dem
  bestehenden Wörterbuch (`raumtyp.raumtyp_flags`), kein neuer Typ. (4) **Mehrdeutig** (`kuerzel_entscheid.MEHRDEUTIG`
  = `sr`, `tr`, `ka`, neu) und Kandidaten-Kürzel (`schl`) typisieren nie, nur als eigenes Wort gezählt („Zul.KA" ist
  Lüftung) → Raum bleibt UNBESTIMMT mit Notlicht, Grund als `kuerzel:`-Warnung in bericht.md. (5) **Ein Raum mit
  zugeordnetem Stempel wird nie umtypisiert**, auch wenn der Stempel keinen Kanon-Typ trägt — Rennweg EG `raum_12`
  „GESCHÄFTLOKAL" 111 m² (Vokabular-Fall Enis) trägt die Möbelbeschriftung „Garderobe" (Wörterbuch: Vorraum); ohne
  diese Regel wurde er VORRAUM, `tuer_8` von `hauseingang` zu `wohnungseingang`, der `final_exit` wanderte von
  `exit_tuer_8` nach `exit_tuer_13` (gemessen, verworfen). (6) **Eindeutigkeit:** alle Kürzel im Polygon ergeben
  denselben Typ; sonst gilt der **dominante Stempel** — der polygonlose Stempel (`kein_polygon`) mit der größten
  Flächenzeile, wenn sie ≥ 50 % der Polygonfläche deckt (R-Stufe fasst Räume zusammen, deren Stempel kein Polygon
  bekamen); ohne dominanten Stempel → UNBESTIMMT mit Grund. (7) **Erscheinungsbild schlägt Kürzel:** ≥ 2 Sanitärobjekte
  (`sanitaer.sanitaerobjekte`) im Polygon → kein AR/ZIMMER/SCHLAFZIMMER/KINDERZIMMER/WOHNZIMMER per Kürzel, Warnung,
  Typ offen (K3 im Provider kann BAD/WC setzen). Auf den 13 Plänen **0 Fälle**.
- **Einbau:** `kaskade.raeume_aus_kaskade` nach `bereinige_kaskade` (alle Polygone endgültig) über `raeume + rest_r`
  (L/H/F ohne Stempel und R), im Fehlerschutz (`kaskade_fehler: Kürzel-Beleg …`). Kein Stempel-Objekt, keine
  Zuordnung, keine Flutung: ein loses Wort ohne Polygon hat keine Wirkung (`_stempel_aus_texten` unverändert — ein
  Kürzel ohne m² als Stempel hätte über `_ein_polygon_ein_stempel` → `kein_polygon` → Flutung neue Räume aus
  Legendenwörtern erzeugt). Typisierte Räume → `k.hinweise` (bericht.md „Hinweise Kürzel-Auflösung", mit Layer,
  dominantem Stempel bzw. Flächenabweichung > 10 % gegen einen polygonlosen Stempel gleichen Typs); offene Räume →
  `k.warnungen` (`kuerzel: …`, bericht.md „Warnungen", Runner `warnungen.wand`). `frei_*`-Räume entstehen erst im
  Provider nach den Wohnungen (§ 16) und werden hier **nicht** erreicht — das ist Abschnitt 2.
- **Am Rain OG4 am Plan:** § 20.4 sagte „keine Flächenzeile neben STGH" — gemessen steht „32.44 m²" 0,4 m unter
  „STGH" (12,18 / 12,54 m), `finde_stempel` kennt den Stempel „STGH 32.44" (STIEGENHAUS) also; er fand nur kein
  Polygon (Flutung < 1 m², `kein_polygon`), ebenso „VR 8.52" und „VR 6.87". Die R-Stufe baute über alle drei
  **ein** Polygon `rest_2` 40,2 m² (OG4 hat keine L/H-Polygone: Kette F 26, R 5). Ohne Dominanz-Regel ist `rest_2`
  „nicht eindeutig — STGH, VR, VR, Schacht- → SCHACHT, STIEGENHAUS, VORRAUM" (gemessen); mit ihr gewinnt „STGH 32.44"
  (81 % der Polygonfläche) → STIEGENHAUS.

**Tests:** `tests/naht/test_kuerzel_am_rain_og4.py` (OG4 aus `Projekte/Am Rain.zip`, byteidentisch zur
Prüfstrecken-Kopie: Raum am STGH-Punkt ist `rest_*` STIEGENHAUS mit Flags 11, 1 Stiegenhaus, genau 2 `stair_exit`, keine
Warnung „kein Geschossausgang"; 20 Leuchten, ≥ 1 im Kern) und `tests/raumerkennung/test_kuerzel_beleg.py` (Varianten
Groß/klein/Punkt/Bindestrich/Zählnummer; Ausschluss Achsmarken, Stufen, Höhenkoten, Summenblock, Fließtext, Fragment,
Legenden-Layer, Text außerhalb; mehrdeutig SR/TR/KA/Schl.; Stempelraum bleibt; zwei Typen → nicht eindeutig; gleicher
Typ zweimal → eindeutig; dominanter Stempel 75 % entscheidet, 33 % nicht; Sanitär schlägt AR, nicht BAD; ein Objekt
schlägt nicht).

**Rot vor dem Fix** (`pytest tests/raumerkennung/test_kuerzel_beleg.py tests/naht/test_kuerzel_am_rain_og4.py
--tb=line`, Kopf `dad7bbd` + Tests, Kurzform):

```
test_kuerzel_beleg.py: ModuleNotFoundError: No module named 'notbeleuchtung.raumerkennung.kuerzel_beleg'  (1 error in 1.66s)
test_kuerzel_am_rain_og4.py:42: AssertionError: assert ('', False, False) == ('STIEGENHAUS', True, True)
test_kuerzel_am_rain_og4.py:59: AssertionError: assert 13 == 20
2 failed in 17.37s
```

**Grün nach dem Fix:** beide Dateien `69 passed in 17.92s` (67 Einheits- + 2 Naht-Tests). `pytest tests/raumerkennung
tests/contract`: 954 passed, 6 skipped, 2 xfailed (Zwischenstand vor den letzten Testergänzungen). ruff: „All checks
passed!".

### 23.3 Am Rain OG4 vorher / nachher (Runner, je allein)

| | vorher (`dad7bbd`) | nachher (Arbeitsbaum dieses Commits) |
|---|---|---|
| Räume / Typwechsel | 28, `rest_2` 40,2 m² ohne Typ | 28; **`rest_2` → STIEGENHAUS** (Flags 11, ALLGEMEIN_ERSCHLIESSUNG); `rest_6` 1,7 m² → WC (WOHNUNG_PRIVAT, `top_4`) |
| Türen typisiert / gesamt | 22 / 58 | 30 / 59 (`tuer_27`, `tuer_28` → `stiegenhaustuer`; `tuer_3`, `tuer_42`, `durchgang_5`, `_11` → `wohnungseingang`; `durchgang_6`, `_9` → `zimmertuer`) |
| Ausgänge | 0, Warnung „kein Geschossausgang ableitbar" | **2 `stair_exit`** (`exit_tuer_27`, `exit_tuer_28`), keine Ausgangs-Warnung |
| Stiegenhäuser / Anker | 0 / 34 | **1** / 58 |
| Segmente | FALLBACK 4 | GRAPH 6 + FALLBACK 3 |
| Leuchten | 13 (rz 8, SL 5; 0 im Kern) | **20** (rz 12, SL 8; 5 im Kern `rest_2`) — Klassen: ALLGEMEIN_ERSCHLIESSUNG 9 → 13, unbestimmt 3 → 3, kein Raum 1 → 3, WOHNUNG_PRIVAT 0 → 1 (`rest_6` WC, Board 1 Leonis) |
| Wohnungsklasse-Warnungen | 8 | 5 |

= exakt die Werte der Speicher-Gegenprobe § 20.4 (2 `stair_exit` `exit_tuer_27`/`_28`, 1 Stiegenhaus, GRAPH 5–6 +
FALLBACK 3, 20 Leuchten, 5 im Kern). Einziger Raum mit weniger Leuchten: `rest_1` GANG 3,6 m² 2 → 1 (Platzierung
verschiebt entlang der neuen GRAPH-Wege; Leonis-Lane).

### 23.4 Blast 13 Pläne (Runner `vorher` → `nachher`, je Plan allein, Am Rain und Muthgasse allein)

Summe: **49 Typwechsel** (alle UNBEKANNT → Typ: WC 10, VORRAUM 10, GANG 9, BALKON 7, WOHNZIMMER 5, STIEGENHAUS 2,
SCHLEUSE 2, KÜCHE 2, GARAGE 1, ABSTELLRAUM 1; Klassen danach WOHNUNG_PRIVAT 27, ALLGEMEIN_ERSCHLIESSUNG 13, AUSSEN 7,
ALLGEMEIN_NEBENRAUM 1, offen 1), 48 `rest_*` auf Am Rain und ein L/H-Raum (Barawitzka `raum_41` „Loggia" 5,3 m² →
BALKON); Rennweg, Mollgasse, Muthgasse **feldgleich** in Räumen, Typen, Türen, Ausgängen, Segmenten und Leuchten
(Muthgasse/Barawitzka nur 1–2 neue `kuerzel:`-Warnungen). **3 davon über den dominanten Stempel:** OG4 `rest_2`
(„STGH 32.44" 81 % gegen VR 8,52 / VR 6,87), UG `rest_23` 48,0 m² („TREPPENHAUS 29.8" 62 % gegen Text „Garage 1"),
EG `rest_3` 7,2 m² („VR 7.27" 101 % gegen „BAD/WC 3.32"); alle übrigen 46 mit genau einem Kürzel-Typ im Polygon.
Räume weg 0, neu 0; Polygone gleich bis auf Am Rain EG `rest_3` 7,2 → 11,3 m² (als VORRAUM nun im Umriss `top_20`,
Zuwachs 4,14 m² = 2d-Zuschlag einer freien Fläche nach § 16, das alte Polygon liegt vollständig im neuen; der
Freiflächen-Befund selbst steht nicht im Runner-JSON). **Leuchten 560 → 596**,
`stair_exit` 23 → 39, `final_exit` 16 → 16; **kein Plan verliert Leuchten**, Räume mit weniger Leuchten nachher nur
durch die verschobene Platzierung entlang neuer GRAPH-Wege (Leonis-Lane): Am Rain UG `rest_12` GANG 1,7 m² 1 → 0,
`raum_38` GANG 24,7 m² 1 → 0, `rest_17` GANG 1,6 m² 2 → 1, `raum_29` STIEGENHAUS 3 → 2, `raum_13` SCHLEUSE 2 → 1; OG1
`rest_24` GANG 3,2 m² 1 → 0, `raum_59` VORRAUM 4 → 2; OG4 `rest_1` GANG 2 → 1. `kuerzel:`-Warnungen 7: mehrdeutig 3
(SR: Barawitzka `raum_27`, Muthgasse `raum_52`, `raum_71`), nicht eindeutig 4 (Am Rain EG `rest_11`, `rest_23`, `rest_29`
— Gartenflächen mit Terrasse/Loggia/Garten-Stempeln mehrerer Tops; OG1 `rest_14` KOCHNISCHE + VR + WOHNRAUM), Sanitär 0.
Fluchtweg-Warnungen „kein final_exit erreichbar … Türgraph endet vor dem Ausgang" steigen auf Am Rain UG 10 → 44 und
EG 12 → 21: mehr Türen tragen eine Rolle (`wohnungseingang` 13 → 46 bzw. 78 → 114 typisierte Türen), also mehr
GRAPH-Starts, die den `final_exit` nicht erreichen — Befund der Türzuordnung, kein Notlicht-Verlust (FALLBACK bleibt).

| Plan | Typwechsel (Raum, m²: vorher → nachher; Klasse) | Wohnungen v → n (echte Mitgliedswechsel) | Türen typ. v → n | Ausgänge v → n | Segmente v → n | Leuchten v → n (Art) | Leuchten je Klasse v → n | `kuerzel:`-Warnungen (Kurzform: Raum bleibt UNBESTIMMT mit Notlicht) |
|---|---|---|---|---|---|---|---|---|
| Barawitzka_EG | `raum_41` 5.3: UNBEKANNT → **BALKON** (AUSSEN) (1) | 7 → 7 (—) | 33/71 → 35/71 | final_exit 1 | FALLBACK 1 GRAPH 7 | 11 → 11 (rz 6 sicherheitsleuchte 5) | ALLGEMEIN_ERSCHLIESSUNG 4 ALLGEMEIN_NEBENRAUM 2 kein Raum 5 | `raum_27` mehrdeutig »SR« |
| Mollgasse_EG | — (0) | 21 → 21 (—) | 44/102 → 44/102 | final_exit 8 stair_exit 1 | FALLBACK 3 GRAPH 14 LINIE 103 | 51 → 51 (rz 24 sicherheitsleuchte 27) | ALLGEMEIN_ERSCHLIESSUNG 29 ALLGEMEIN_NEBENRAUM 7 WOHNUNG_PRIVAT 2 kein Raum 9 unbestimmt 4 | — |
| Muthgasse_E2 | — (0) | 22 → 22 (—) | 113/193 → 113/193 | stair_exit 1 | FALLBACK 3 LINIE 139 | 139 → 139 (rz 86 sicherheitsleuchte 53) | ALLGEMEIN_ERSCHLIESSUNG 14 ALLGEMEIN_NEBENRAUM 5 LIFT 1 WOHNUNG_PRIVAT 62 kein Raum 57 | `raum_52` mehrdeutig »SR«; `raum_71` mehrdeutig »SR« |
| Rennweg_EG | — (0) | 2 → 2 (—) | 20/40 → 20/40 | final_exit 2 stair_exit 3 | FALLBACK 2 GRAPH 5 | 17 → 17 (rz 9 sicherheitsleuchte 8) | ALLGEMEIN_ERSCHLIESSUNG 11 ALLGEMEIN_NEBENRAUM 3 kein Raum 3 | — |
| Rennweg_OG3 | — (0) | 2 → 2 (—) | 17/18 → 17/18 | stair_exit 3 | FALLBACK 1 GRAPH 5 | 7 → 7 (rz 5 sicherheitsleuchte 2) | ALLGEMEIN_ERSCHLIESSUNG 6 kein Raum 1 | — |
| Mollgasse_1KG | — (0) | 0 → 0 (—) | 0/28 → 0/28 | final_exit 1 | FALLBACK 4 | 14 → 14 (rz 7 sicherheitsleuchte 7) | ALLGEMEIN_ERSCHLIESSUNG 9 kein Raum 4 unbestimmt 1 | — |
| Mollgasse_2KG | — (0) | 1 → 1 (—) | 2/46 → 2/46 | stair_exit 1 | FALLBACK 2 GRAPH 1 | 13 → 13 (antipanik 1 rz 8 sicherheitsleuchte 4) | ALLGEMEIN_ERSCHLIESSUNG 9 ALLGEMEIN_NEBENRAUM 3 LIFT 1 | — |
| AmRain_OG4 | `rest_2` 40.2: UNBEKANNT → **STIEGENHAUS** (ALLGEMEIN_ERSCHLIESSUNG); `rest_6` 1.7: UNBEKANNT → **WC** (WOHNUNG_PRIVAT) (2) | 11 → 11 (top_4→top_4 +rest_6) | 22/58 → 30/59 | — → stair_exit 2 | FALLBACK 4 → FALLBACK 3 GRAPH 6 | 13 → 20 (rz 8 sicherheitsleuchte 5 → rz 12 sicherheitsleuchte 8) | ALLGEMEIN_ERSCHLIESSUNG 9 kein Raum 1 unbestimmt 3 → ALLGEMEIN_ERSCHLIESSUNG 13 WOHNUNG_PRIVAT 1 kein Raum 3 unbestimmt 3 | — |
| AmRain_UG | `rest_3` 45.8: UNBEKANNT → **GANG** (ALLGEMEIN_ERSCHLIESSUNG); `rest_5` 56.8: UNBEKANNT → **GANG** (WOHNUNG_PRIVAT); `rest_6` 87.5: UNBEKANNT → **SCHLEUSE** (ALLGEMEIN_ERSCHLIESSUNG); `rest_7` 8.7: UNBEKANNT → **GARAGE** (ALLGEMEIN_NEBENRAUM); `rest_8` 152.5: UNBEKANNT → **GANG** (WOHNUNG_PRIVAT); `rest_18` 55.9: UNBEKANNT → **SCHLEUSE** (ALLGEMEIN_ERSCHLIESSUNG); `rest_23` 48.0: UNBEKANNT → **STIEGENHAUS** (ALLGEMEIN_ERSCHLIESSUNG); `rest_32` 90.0: UNBEKANNT → **GANG** (ALLGEMEIN_ERSCHLIESSUNG) (8) | 7 → 7 (top_2→top_2 + −raum_22) | 13/295 → 46/295 | final_exit 2 stair_exit 4 → final_exit 2 stair_exit 15 | FALLBACK 24 → FALLBACK 26 GRAPH 2 | 91 → 110 (rz 59 sicherheitsleuchte 32 → rz 69 sicherheitsleuchte 41) | ALLGEMEIN_ERSCHLIESSUNG 66 ALLGEMEIN_NEBENRAUM 3 WOHNUNG_PRIVAT 2 kein Raum 13 unbestimmt 7 → ALLGEMEIN_ERSCHLIESSUNG 78 ALLGEMEIN_NEBENRAUM 4 WOHNUNG_PRIVAT 8 kein Raum 16 unbestimmt 4 | — |
| AmRain_EG (dazu `rest_3` 7,2 → 11,3 m²: UNBEKANNT → **VORRAUM** über dominanten Stempel, s. o.) | `rest_5` 9.3: UNBEKANNT → **KÜCHE** (WOHNUNG_PRIVAT); `rest_6` 9.3: UNBEKANNT → **KÜCHE** (WOHNUNG_PRIVAT); `rest_8` 1.6: UNBEKANNT → **WC** (WOHNUNG_PRIVAT); `rest_9` 1.7: UNBEKANNT → **WC** (WOHNUNG_PRIVAT); `rest_10` 1.9: UNBEKANNT → **WC** (WOHNUNG_PRIVAT); `rest_13` 1.2: UNBEKANNT → **GANG** (ALLGEMEIN_ERSCHLIESSUNG); `rest_14` 1.2: UNBEKANNT → **GANG** (ALLGEMEIN_ERSCHLIESSUNG); `rest_16` 5.1: UNBEKANNT → **GANG** (ALLGEMEIN_ERSCHLIESSUNG); `rest_17` 2.3: UNBEKANNT → **WC** (WOHNUNG_PRIVAT); `rest_18` 2.6: UNBEKANNT → **WC** (WOHNUNG_PRIVAT); `rest_20` 26.9: UNBEKANNT → **WOHNZIMMER** (WOHNUNG_PRIVAT); `rest_21` 26.9: UNBEKANNT → **WOHNZIMMER** (WOHNUNG_PRIVAT); `rest_22` 2.0: UNBEKANNT → **WC** (WOHNUNG_PRIVAT); `rest_24` 28.5: UNBEKANNT → **WOHNZIMMER** (WOHNUNG_PRIVAT); `rest_25` 28.0: UNBEKANNT → **WOHNZIMMER** (WOHNUNG_PRIVAT) (15) | 50 → 49 (top_3→top_3 +raum_41,rest_5,raum_23; top_6→top_6 +rest_22; top_7→top_7 +rest_6,raum_26,raum_29; top_8→top_8 +rest_21,rest_18; top_9→top_3 +raum_19,raum_12,rest_5; top_12→top_7 +raum_20,rest_6,raum_42; top_14→top_12 +rest_20,rest_17; top_16→top_14 +rest_25; top_17→top_15 +rest_24; top_20→top_18 +rest_9; top_22→top_20 +rest_3; top_30→top_28 +rest_8) | 78/317 → 114/317 | final_exit 2 stair_exit 1 | FALLBACK 6 GRAPH 1 → FALLBACK 9 GRAPH 1 | 40 → 46 (rz 27 sicherheitsleuchte 13 → rz 30 sicherheitsleuchte 16) | ALLGEMEIN_ERSCHLIESSUNG 12 ALLGEMEIN_NEBENRAUM 7 WOHNUNG_PRIVAT 3 kein Raum 9 unbestimmt 9 → ALLGEMEIN_ERSCHLIESSUNG 14 ALLGEMEIN_NEBENRAUM 7 WOHNUNG_PRIVAT 4 kein Raum 10 unbestimmt 11 | `rest_11` nicht eindeutig → BALKON, GANG, KÜCHE, TERRASSE, VORRAUM, WOHNZIMMER; `rest_23` nicht eindeutig → BALKON, TERRASSE; `rest_29` nicht eindeutig → BALKON, TERRASSE |
| AmRain_OG1 | `rest_2` 5.0: UNBEKANNT → **VORRAUM** (WOHNUNG_PRIVAT); `rest_3` 4.9: UNBEKANNT → **VORRAUM** (WOHNUNG_PRIVAT); `rest_4` 3.4: UNBEKANNT → **BALKON** (AUSSEN); `rest_6` 41.2: UNBEKANNT → **WOHNZIMMER** (WOHNUNG_PRIVAT); `rest_7` 20.7: UNBEKANNT → **BALKON** (AUSSEN); `rest_8` 18.5: UNBEKANNT → **BALKON** (AUSSEN); `rest_11` 9.0: UNBEKANNT → **VORRAUM** (WOHNUNG_PRIVAT); `rest_15` 2.1: UNBEKANNT → **VORRAUM** (ALLGEMEIN_ERSCHLIESSUNG); `rest_17` 2.8: UNBEKANNT → **ABSTELLRAUM** (WOHNUNG_PRIVAT); `rest_19` 14.5: UNBEKANNT → **GANG** (WOHNUNG_PRIVAT); `rest_22` 3.3: UNBEKANNT → **GANG** (ALLGEMEIN_ERSCHLIESSUNG); `rest_23` 2.0: UNBEKANNT → **VORRAUM** (ALLGEMEIN_ERSCHLIESSUNG) (12) | 57 → 54 (top_35→top_35 +rest_19,raum_73,raum_84; top_38→top_49 +rest_6 −raum_61; top_39→top_38 +rest_17; top_45→top_35 +rest_19,raum_57,raum_84; top_51→top_35 +rest_19,raum_57,raum_73; top_56→top_54 +rest_2; top_57→top_3 +rest_3,raum_100; top_3→top_3 +rest_3,raum_99) | 103/300 → 138/300 | stair_exit 4 → stair_exit 7 | FALLBACK 17 GRAPH 6 → FALLBACK 16 GRAPH 12 | 69 → 73 (rz 47 sicherheitsleuchte 22 → rz 49 sicherheitsleuchte 24) | ALLGEMEIN_ERSCHLIESSUNG 43 ALLGEMEIN_NEBENRAUM 1 SCHACHT 1 WOHNUNG_PRIVAT 2 kein Raum 6 unbestimmt 16 → ALLGEMEIN_ERSCHLIESSUNG 47 ALLGEMEIN_NEBENRAUM 1 SCHACHT 1 WOHNUNG_PRIVAT 5 kein Raum 6 unbestimmt 13 | `rest_14` nicht eindeutig → VORRAUM, WOHNZIMMER |
| AmRain_OG2 | `rest_6` 45.1: UNBEKANNT → **BALKON** (AUSSEN); `rest_11` 2.1: UNBEKANNT → **VORRAUM** (ALLGEMEIN_ERSCHLIESSUNG); `rest_16` 2.0: UNBEKANNT → **VORRAUM** (WOHNUNG_PRIVAT); `rest_22` 5.3: UNBEKANNT → **WC** (WOHNUNG_PRIVAT) (4) | 43 → 42 (top_14→top_14 +rest_16; top_15→top_15 +raum_73,rest_22; top_39→top_15 +raum_34,rest_22,raum_35) | 117/264 → 134/264 | stair_exit 2 | FALLBACK 15 GRAPH 9 | 75 → 75 (rz 52 sicherheitsleuchte 23) | ALLGEMEIN_ERSCHLIESSUNG 57 WOHNUNG_PRIVAT 3 kein Raum 12 unbestimmt 3 | — |
| AmRain_OG3 | `rest_2` 29.9: UNBEKANNT → **BALKON** (AUSSEN); `rest_4` 9.3: UNBEKANNT → **VORRAUM** (WOHNUNG_PRIVAT); `rest_5` 17.4: UNBEKANNT → **WC** (WOHNUNG_PRIVAT); `rest_8` 25.0: UNBEKANNT → **BALKON** (AUSSEN); `rest_10` 1.7: UNBEKANNT → **WC** (WOHNUNG_PRIVAT); `rest_11` 1.3: UNBEKANNT → **VORRAUM** (WOHNUNG_PRIVAT) (6) | 23 → 21 (top_1→top_1 +raum_38,rest_10; top_3→top_2 +rest_5,raum_10; top_2→top_2 +rest_5,raum_9,raum_11; top_5→top_4 +rest_11; top_19→top_1 +raum_37,rest_10,raum_1,raum_2,raum_3) | 61/129 → 84/129 | stair_exit 3 | FALLBACK 2 GRAPH 10 → FALLBACK 2 GRAPH 15 | 20 → 20 (rz 9 sicherheitsleuchte 11) | ALLGEMEIN_ERSCHLIESSUNG 16 WOHNUNG_PRIVAT 3 kein Raum 1 | — |

Jeder Typwechsel einzeln (Tabelle; EG `rest_3` steht dort wegen des geänderten Polygons nicht in der Spalte, sondern
oben): alle 49 sind untypisierte Kaskaden-Räume, in deren Polygon genau ein Kanon-Kürzel oder ein dominanter
polygonloser Stempel liegt. Auffällig und **im Bericht zu nennen** (Regel greift wie beschlossen, Polygon fasst mehr als den
Stempelraum — R-Stufe, R-05 b): Am Rain UG `rest_8` 152,5 m² → GANG (Texte „GANG", „HAUSKELLER", „KELLERABTEILE 1",
„ELEKTRO", Lüftung) und `rest_6` 87,5 m² → SCHLEUSE (Texte „Schleuse", „HAUS1"–„HAUS5", „KELLERABTEILE 1"), beide
Erschließung mit Notlicht; `rest_5` 56,8 m² GANG und `rest_8` kommen als **WOHNUNG_PRIVAT** heraus (K4/S7-Klasse —
Leuchten in WOHNUNG_PRIVAT UG 2 → 8, Board 1 Leonis); OG3 `rest_5` 17,4 m² → WC bei Stempel „WC 2.25 m²" (+673 %)
und OG2 `rest_22` 5,3 m² → WC verbinden je zwei Wohnungen zu einer (OG3 23 → 21, OG2 43 → 42, EG 50 → 49, OG1
57 → 54 Wohnungen; die echten Mitgliedswechsel stehen in der Tabelle) — die Wohnung folgt rohen Türen (Grundsatz (b)),
der neue Typ macht die Tür zur `zimmertuer`. Kein Notlicht-Verlust ohne Regel: WOHNUNG_PRIVAT-Räume (WC/KÜCHE/
VORRAUM/WOHNZIMMER in Wohnungen) hatten vorher als UNBESTIMMT Notlicht; die Summe je Plan sinkt nirgends, die
Einzelräume mit weniger Leuchten sind oben genannt (Platzierung).

### 23.5 Nicht gebaut, gemessen: „ZI" → ZIMMER im Wörterbuch

§ 22 (a) nennt „ZI 1/ZI 2" als Wörterbuch-Eintrag (Kanon ZIMMER, 43 Vorkommen, Am Rain). Gebaut, gemessen,
**zurückgenommen**: der Eintrag wirkt nicht nur hier, sondern in `stempel_anker._stempel_aus_texten` — alle 43 „ZI n"
tragen eine Flächenzeile, werden damit **Stempel** und die F-Stufe flutet sie. Am Rain OG4 allein: Räume 28 → 32
(neue F-Räume ZIMMER 12,0/22,5/13,5/13,9/17,1/18,9/14,6/19,6 m²), Türen 58 → 69, 11 Wohnungswechsel, **Leuchten
20 → 9** gegenüber der Gegenprobe, `stair_exit` 2 → 1 (`tuer_28` 12 915/8 175 wird `raum_5` VORRAUM (nun
WOHNUNG_PRIVAT) → `rest_2` = `wohnungseingang`, kein `stair_exit` mehr). Das ist eine Stempel-Vokabular-Änderung mit
eigenem Blast auf allen sechs Am-Rain-Geschossen und verfehlt die Owner-Abnahme (20 Leuchten) — darum nicht in diesem
Commit; **Owner-Entscheid** (zusammen mit KOCHNISCHE → KÜCHE und den Kandidaten aus 23.1 d), eigener Schritt mit
eigenem Vorher/Nachher.

### 23.6 Gate und Suite

**Volle Suite** (`pytest -q -p no:cacheprovider -rxXs`, allein, nach dem Blast, 17 min 58 s): `6 failed, 2324 passed,
11 skipped, 6 deselected, 15 xfailed, 3 warnings`, 0 xpassed — dieselben 6 roten wie § 21.1 (3 ×
`test_keine_leuchten_in_wohnung_privat` OG1/OG2/DG1 = Board 1 Leonis, `test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell`,
die 2 S4c-Pins), 2324 = 2255 + 69 neue; 15 xfailed und 11 skipped wie § 21.1; die 3 Warnungen sind die bekannten
Starlette-/httpx-Hinweise der API-Tests. Kein Test umgestellt, keine Schwelle, kein Soll, kein Marker angefasst.

**Gate:** `pytest -m gate tests/gate` 3 passed, 1 xfailed (`test_gate_tuerstapel_erfuellt`, wie vorher). `gate_messung` auf
dem Arbeitsbaum dieses Commits (vor dem Commit, `_arbeit/gate/messung_dad7bbd-dirty-23.json`, 59,3 s), `pruefe_gate`
gegen `nullmessung_f15d03f.json`: **(0)** unsauberer Arbeitsbaum (erwartet, vor dem Commit gemessen) und **(3)
`M4.einraum` DG2 0 → 1** (Enis Board 3, unverändert); M17 **18/18 BESTANDEN**; OG1 a==b 0, Einraum 1; OG3 5
GRAPH-Segmente, 0 Anker in WOHNUNG_PRIVAT; DG1 2 Ausgänge, 0 durch den Liftschacht; **alle Messfelder außer `meta`
gleich `messung_e0c820d.json`** (Barawitzka `raum_41` → BALKON berührt die gemessene Verbindung nicht; Rennweg EG
`raum_12` bleibt dank Regel (5)).

### 23.7 Offen nach Abschnitt 1

- **„ZI" → ZIMMER, KOCHNISCHE → KÜCHE, GARTEN, ELEKTRO, SPEIS, KELLERABTEILE, HAUSKELLER, MAGAZIN** (23.1 d, 23.5):
  Wörterbuch-/Kanon-Kandidaten, je mit F-Stufen-Blast — Owner/Enis. P1 · Selman (Owner).
- **Mehrdeutig SR/TR/KA** (`MEHRDEUTIG`): 3 Räume bleiben UNBESTIMMT mit Notlicht (Barawitzka `raum_27`, Muthgasse
  `raum_52`/`raum_71`); Entscheid über die zweite Meinung (Abschnitt 3, Phase B). P2.
- **Polygon fasst mehr als den Stempelraum** (23.4: UG `rest_8` 152,5 m², `rest_6` 87,5 m², OG3 `rest_5` +673 %):
  Ursache R-Stufe/Wandlücken auf Am Rain (R-05 b, § 16 „Polygonform"), nicht die Typregel; die Hinweise in bericht.md
  nennen die Abweichung. P1 · Selman.
- **GANG als WOHNUNG_PRIVAT** (UG `rest_5`, `rest_8`) und Leuchten in WOHNUNG_PRIVAT (UG 2 → 8, OG1 2 → 5, OG4 0 → 1):
  Board 1, Leonis (gemeldet).
- **Platzierung verschiebt** entlang neuer GRAPH-Wege (UG `raum_38` GANG 24,7 m² ohne Leuchte nachher): Leonis-Lane,
  gemeldet.
- `frei_*` (§ 22) bleiben alle 12 UNBEKANNT — Abschnitt 2 (Stempel/Kürzel vor UNBEKANNT in `freiflaeche`). **Erledigt, § 24.**
- `Projekte/_ergebnis/` nicht neu erzeugt (Verifikation über den Runner; Prüfstrecke am Abschluss).

## 24. Abschnitt 2 — Stempel vor UNBEKANNT (Entscheid 2; erledigt mit dem Commit dieses Eintrags)

**Auftrag (Owner 2026-10-01, `docs/AUFTRAG_2026-10-01.md` § 2, Entscheid 2):** „Bevor ein neuer Raum UNBEKANNT wird,
Stempel/Kürzel im Polygon suchen und nach Abschnitt 1 typisieren. Die 2d-Definition (Nachbarn, 0,80 m, Tür mit Blatt)
bleibt unverändert. Test zuerst rot: Die 6 der 12 Räume mit Stempel (VR, AR, BAD …) bekommen ihren Typ." Dazu aus
dem Ablauf: Klasse der neu typisierten Räume statisch nach Typ, `wohnung_id` weiter nur aus rohen Türen; Doppelstempel
→ Regel definieren und begründen. Stand vorher `8748e24` (Abschnitt 1).

### 24.1 Regel und Einbau (`freiflaeche.fuelle_freie_flaechen`, Provider unverändert in der Reihenfolge)

- **Wo:** in `fuelle_freie_flaechen` NACH dem Anlegen aller neuen Räume `frei_n` und VOR der Befund-Zeile — die
  2d-Entscheidung (Umriss, Öffnung ≥ 0,80 m, Tür mit Blatt = Trenner) ist unverändert; die Typisierung hängt nur an den
  neuen Räumen, nie am aufnehmenden Raum eines Zuschlags. Keine neue Stufe im Provider: `provider.parse` reicht
  `kuerzel_texte(plan)`, die polygonlosen Stempel (`k.zuordnungen` mit `raum is None`) und `sanitaerobjekte(plan)` als
  Schlüsselwort-Argumente durch (`texte`, `stempel`, `sanitaer_quelle`); ohne sie läuft 2d wie bisher (Tests von § 16
  unverändert grün).
- **Wie:** dieselbe Funktion wie in der Kaskade — `kuerzel_beleg.typisiere_kuerzel` über die Liste der neuen Räume
  (Kürzel-Form, Wörterbuch `raumtyp_flags`, Legenden-Layer ausgeschlossen, mehrdeutig SR/TR/KA/Schl. nie, ≥ 2
  Sanitärobjekte schlagen AR/Zimmer-Familie, Eindeutigkeit mit dominantem Stempel ≥ 50 %, § 23.2). **Keine zweite Regel,
  keine zweite Schwelle:** ein Kürzel wirkt in `frei_*` genau so wie in `rest_*`. Kleinster deckender Raum zählt nur
  unter den neuen Räumen (die Kaskaden-Räume sind längst typisiert oder gestempelt und stehen nicht zur Wahl).
- **Klasse:** typisierter Raum → `nutzungsklasse_fuer(raum_typ)` (statisch: VORRAUM/ABSTELLRAUM → WOHNUNG_PRIVAT,
  BALKON → AUSSEN). Die Verfeinerung aus `bilde_wohnungen` (K4/S7) läuft nicht noch einmal — sie liegt vor 2d, und die
  Räume liegen per Definition im Umriss genau einer Wohnung, der statische Default ist dort richtig. Flags aus dem
  Wörterbuch wie in der Kaskade (VORRAUM 11, ABSTELLRAUM/BALKON 00).
- **Wohnung:** `wohnung_id` bleibt `None` (Grundsatz (b): nur aus rohen Türen). Die Türen an allen 12 Räumen tragen
  KEIN_RAUM-Seiten (24.4, Spalte Türen) — **so belassen und gemeldet** (§ 16 „Türseiten an neuen Räumen", P2).
- **Ausgabe:** die Befund-Zeile `freiflaeche: … → neuer Raum frei_n <TYP>, <2d-Grund>; Kürzel »VR« im Polygon … ->
  VORRAUM (Entscheid 1, Owner 2026-10-01) (Entscheid 2: Stempel vor UNBEKANNT)` (bericht.md „Warnungen" wie bisher,
  `scripts/plan_pruefen.py` unverändert); ein offener Fall als eigene Zeile `kuerzel: frei_n bleibt UNBESTIMMT
  (Notlicht): nicht eindeutig — …; kein dominanter Stempel` (derselbe Wortlaut wie aus der Kaskade). Kein Contract-Feld.

### 24.2 Doppelstempel — Regel (festgelegt) und Begründung

**Regel:** Liegen in einem neuen Raum Kürzel verschiedener Typen, gilt die Eindeutigkeitsregel aus Abschnitt 1 (§ 23.2
Punkt 6): es entscheidet der **dominante polygonlose Stempel**, dessen Flächenzeile mindestens die Hälfte der
Polygonfläche deckt (`kuerzel_beleg._DOMINANT` = 0,5); gibt es keinen, bleibt der Raum **UNBESTIMMT mit Grund und
Notlicht** (`kuerzel:`-Warnung). Keine eigene Schwelle für `frei_*`.

**Begründung am Fall OG1 `frei_5`** (18,19 m², § 22: „BAD 5,35" + „GANG 7,68" + „KOCHNISCHE 5,34", Summe 18,37 m²):
das Polygon ist kein Raum, sondern **drei Räume ohne erkannte Zwischenwände**. Jeder Typ wäre für mehr als die Hälfte
der Fläche falsch (größter Anteil GANG 42 %). GANG würde Bad und Kochnische zur Erschließung machen (Flags 11,
`anker_fuer_gang`, Fluchtweg-Graph durch ein Bad); BAD würde dem Gang das Notlicht nehmen (Grundsatz (a) verletzt);
KOCHNISCHE hat keinen Wörterbuch-Treffer (§ 23.1 d, Owner-Entscheid). UNBESTIMMT behält das Notlicht und macht die
Stelle sichtbar — die Ursache ist die Polygonform (R-05 b, § 16 „Polygonform", offen), nicht die Typregel; auch die
zweite Meinung (Abschnitt 3) kann ein Drei-Raum-Polygon nicht zu einem Typ machen. Die 50-%-Schwelle ist dieselbe, mit
der Abschnitt 1 OG4 `rest_2` (81 %), UG `rest_23` (62 %) und EG `rest_3` (101 %) entschied — eine Regel für Kaskade
und Freiflächen. Synthetisch geprüft: ein polygonloser Stempel „GANG 15,0 m²" in einem 22,6-m²-Polygon (66 %) gegen
»BAD« entscheidet → GANG; ohne ihn → UNBESTIMMT.

### 24.3 Tests, rot vor dem Fix

`tests/raumerkennung/test_freiflaeche.py` (+5 synthetisch: Kürzel »VR« im neuen Raum → VORRAUM/WOHNUNG_PRIVAT ohne
Wohnung, Befund nennt das Kürzel; Kürzel im Nachbarraum zählt nicht; Doppelstempel BAD + GANG ohne dominanten Stempel →
UNBEKANNT + `kuerzel:`-Warnung „nicht eindeutig … kein dominanter Stempel"; dominanter Stempel entscheidet → GANG/
ALLGEMEIN_ERSCHLIESSUNG; »ZI 2« ohne Wörterbuch → UNBEKANNT) und `tests/naht/test_freiflaeche_kuerzel_am_rain.py`
(Am Rain aus `Projekte/Am Rain.zip`, byteidentisch: **OG3** genau ein `frei_*` 2,7 m² → VORRAUM, WOHNUNG_PRIVAT, ohne
Wohnung, Befund-Zeile; **OG1** fünf `frei_*` 2,4/4,0/6,7/11,2/18,2 m² → BALKON/AUSSEN, VORRAUM/WOHNUNG_PRIVAT (»VR«
ohne Flächenzeile), UNBEKANNT (Stiege), BALKON/AUSSEN (»LOGGIA«), UNBESTIMMT mit `kuerzel:`-Warnung (Doppelstempel);
keiner mit Wohnung). Räume werden über die Fläche (0,1 m²) angesprochen, nicht über die ID. EG (VR 12,78 / AR 3,37,
Parse 310 s) läuft nicht im Test, sondern über den Blast-Runner (24.4).

**Rot vor dem Fix** (Kurzform; Einheitstests `pytest tests/raumerkennung/test_freiflaeche.py --tb=line` auf dem
Arbeitsbaum vor dem Fix; Naht-Tests gegen den Code `8748e24` — `git archive`-Kopie der `src/` außerhalb des Repos als
`pythonpath`, Tests aus dem Arbeitsbaum):

```
test_freiflaeche.py:76: TypeError: fuelle_freie_flaechen() got an unexpected keyword argument 'texte'   (5 failed, 4 passed in 1.13s)
test_freiflaeche_kuerzel_am_rain.py:58: AssertionError: assert ('', None, None) == ('VORRAUM', 'WOHNUNG_PRIVAT', None)
test_freiflaeche_kuerzel_am_rain.py:68: AssertionError: assert ('', None) == ('BALKON', 'AUSSEN')
2 failed in 150.62s
```

(Der erste Naht-Lauf scheiterte an einem Rundungsschlüssel im Test selbst — OG1 `frei_2` 6,746 m² rundet auf 6,7, nicht
6,8; Testdatum korrigiert, danach der oben zitierte Lauf.) **Grün nach dem Fix:** `test_freiflaeche.py`,
`test_freiflaeche_kuerzel_am_rain.py`, `test_freiflaeche_wohnung.py` **12 passed in 153.74s**. ruff: „All checks
passed!".

### 24.4 Die 12 `frei_*` vorher → nachher (Runner `vorher2` = `8748e24`, `nachher2` = Arbeitsbaum dieses Commits)

Methode wie § 22/§ 23 (eigener Parse + Default-Platzierung je Plan allein, Am Rain und Muthgasse allein, Scratch außerhalb
des Repos). Die Vorher-Kopie der `src/` braucht `CAD_Symbole/photometrie` daneben — ohne den Katalog fällt
`build_default_bundle` still auf die isotrope Platzierung zurück (Mollgasse EG 51 → 60 Leuchten bei identischem
RaumModell, gemessen und verworfen; **Befund für die Prüfstrecke: der Rückfall ist nicht als Warnung sichtbar**,
Leonis/gemeinsam). Mit Katalog sind alle 13 Vorher-Läufe feldgleich mit § 23.4 nachher.

| Plan | Raum | m² | Stempel/Kürzel im Polygon | Typ vorher → nachher | Klasse | Flags | `wohnung_id` | Türen an der Grenze (Rolle, von→nach) | Beleg / Grund |
|---|---|--:|---|---|---|---|---|---|---|
| AmRain_EG | `frei_1` | 16.57 | „12.78 m²"; „VR" | UNBEKANNT → **VORRAUM** | WOHNUNG_PRIVAT | 11 | — | `tuer_151`/`tuer_172` KEIN_RAUM→AUSSEN; `tuer_201` KEIN_RAUM→KEIN_RAUM; `tuer_242` KEIN_RAUM→raum_85 | Kürzel »VR«; Polygon +30 % gegen „VR 12.78" (fasst mehr als den Stempelraum, § 22) |
| AmRain_EG | `frei_2` | 3.92 | „3.37 m²"; „AR" | UNBEKANNT → **ABSTELLRAUM** | WOHNUNG_PRIVAT | 00 | — | `tuer_151` KEIN_RAUM→AUSSEN | Kürzel »AR«; Polygon +16 %; < 2 Sanitärobjekte im Polygon (Regel 7 greift nicht) |
| AmRain_EG | `frei_3` | 2.36 | — | UNBEKANNT → UNBEKANNT | — | 00 | — | `tuer_157` zimmertuer raum_92→raum_91; `tuer_214` KEIN_RAUM→raum_74; `tuer_249` KEIN_RAUM→KEIN_RAUM; `durchgang_59` raum_74→raum_91 | kein Text im Polygon |
| AmRain_EG | `frei_4` | 9.76 | „10.25 m²"; „ZI 2" | UNBEKANNT → UNBEKANNT | — | 00 | — | `tuer_214` KEIN_RAUM→raum_74; `tuer_216` KEIN_RAUM→AUSSEN; `tuer_249` KEIN_RAUM→KEIN_RAUM | »ZI 2« ohne Wörterbuch-Treffer (§ 23.5, Owner) |
| AmRain_OG1 | `frei_1` | 11.17 | „3.88 m²"; „BALKON" | UNBEKANNT → **BALKON** | AUSSEN | 00 | — | `tuer_51` KEIN_RAUM→KEIN_RAUM | Kürzel »BALKON«; Polygon +188 % (nimmt die Nachbar-Loggien mit, § 22) |
| AmRain_OG1 | `frei_2` | 6.75 | — | UNBEKANNT → UNBEKANNT | — | 00 | — | `tuer_13` wohnungseingang raum_4→raum_12; `tuer_22` KEIN_RAUM→KEIN_RAUM; `tuer_23` KEIN_RAUM→raum_4; `tuer_39` raum_4→AUSSEN | kein Raumstempel (Stufen-Beschriftung ist kein Kürzel, § 23.1 c) |
| AmRain_OG1 | `frei_3` | 3.99 | „VR" | UNBEKANNT → **VORRAUM** | WOHNUNG_PRIVAT | 11 | — | `tuer_170` KEIN_RAUM→KEIN_RAUM; `tuer_205` KEIN_RAUM→raum_86; `durchgang_35` raum_81→raum_86 | Kürzel »VR« **ohne Flächenzeile** im Polygon (Flächenzeile im Schacht `rest_10`) — der Fall „Kürzel ist Beleg auch ohne Flächenzeile" |
| AmRain_OG1 | `frei_4` | 2.39 | „7.67 m²"; „LOGGIA" | UNBEKANNT → **BALKON** | AUSSEN | 00 | — | — | Kürzel »LOGGIA« (Wörterbuch → BALKON, Kanon); Polygon −69 % |
| AmRain_OG1 | `frei_5` | 18.19 | „5.35 m²"; „BAD"; „7.68 m²"; „GANG"; „5.34 m²"; „KOCHNISCHE" | UNBEKANNT → **UNBESTIMMT mit Grund** | — | 00 | — | `tuer_95` balkontuer raum_36→AUSSEN; `tuer_96` KEIN_RAUM→KEIN_RAUM; `tuer_103` AUSSEN→KEIN_RAUM | `kuerzel: frei_5 bleibt UNBESTIMMT (Notlicht): nicht eindeutig — »BAD«, »GANG« → BAD, GANG; kein dominanter Stempel` (24.2) |
| AmRain_OG2 | `frei_1` | 3.99 | „VR" | UNBEKANNT → **VORRAUM** | WOHNUNG_PRIVAT | 11 | — | `tuer_154` KEIN_RAUM→KEIN_RAUM; `tuer_206` KEIN_RAUM→raum_65; `durchgang_30` raum_51→raum_65 | Kürzel »VR« ohne Flächenzeile (wie OG1 `frei_3`, ein Geschoss höher) |
| AmRain_OG3 | `frei_1` | 2.73 | „5.13 m²"; „VR" | UNBEKANNT → **VORRAUM** | WOHNUNG_PRIVAT | 11 | — | `tuer_84` zimmertuer raum_27→raum_30; `tuer_86` wohnungseingang raum_30→raum_35; `tuer_98` raum_30→KEIN_RAUM | Kürzel »VR«; Polygon −47 % |
| AmRain_OG4 | `frei_1` | 5.41 | — | UNBEKANNT → UNBEKANNT | — | 00 | — | `tuer_45` KEIN_RAUM→AUSSEN | kein Raumstempel (Dachausstieg/Luftraum, § 22) |

**Ergebnis: 7 typisiert** (VORRAUM 4, BALKON 2, ABSTELLRAUM 1) — die 6 Räume mit Stempel aus dem Auftrag minus OG1
`frei_5` (Doppelstempel → UNBESTIMMT mit Grund, 24.2) plus die beiden »VR« ohne Flächenzeile (OG1 `frei_3`, OG2
`frei_1`, § 22 Hinweis b); **4 ohne Beleg UNBEKANNT** (EG `frei_3`, OG1 `frei_2`, OG4 `frei_1` ohne Text; EG `frei_4`
»ZI 2«). Kein `frei_*` bekommt eine Wohnung; Erscheinungsbild-Regel (Sanitär) 0 Fälle. Jede Tür an einem `frei_*`
trägt mindestens eine KEIN_RAUM-Seite oder gehört ganz den Nachbarräumen — keine Tür kennt den neuen Raum.

### 24.5 Blast 13 Pläne (`vorher2` → `nachher2`, je Plan allein)

**Nur die 7 Räume ändern sich** — Typ, Klasse und (VORRAUM) Flags; alles andere ist auf allen 13 Plänen feldgleich:
Räume weg 0, neu 0, Polygone gleich; Türen (Seiten, Rollen, Lage), Ausgänge, Segmente, Anker, Stiegenhäuser, Bounds,
korrigierte Rollen, `bestaetigt_privat` und alle Warnungszähler gleich (OG1 `warnungen.freiflaeche` 5 → 6 = die
`kuerzel:`-Zeile von `frei_5`). **Leuchten je Position 13/13 gleich** (Summe 596 → 596); in den 7 typisierten Räumen lag
vorher keine Leuchte und liegt nachher keine (OG1 `frei_2`, untypisiert, behält RZ + Sicherheitsleuchte aus § 16) — kein
Notlicht-Verlust, auch nicht in der Klasse: Leuchten je Klasse 13/13 gleich. Wohnungen 13/13 gleich (keine
Mitgliedswechsel; ein typisierter `frei_*` ohne Wohnung ändert keine Partition). Parse-Laufzeit und Spitze unverändert
(EG 309 → 306 s, 2,70 → 2,71 GB; Muthgasse 254 → 254 s, 1,79 GB).

| Plan | Typwechsel (Raum, m²: vorher → nachher; Klasse) | Wohnungen v → n | Türen typ. v → n | Ausgänge | Segmente | Leuchten v → n (Art) | Leuchten je Klasse | neue `kuerzel:`-Warnungen |
|---|---|---|---|---|---|---|---|---|
| Barawitzka_EG | — (0) | 7 → 7 | 35/71 → 35/71 | final_exit 1 | FALLBACK 1 GRAPH 7 | 11 → 11 (rz 6 SL 5) | ALLGEMEIN_ERSCHLIESSUNG 4 ALLGEMEIN_NEBENRAUM 2 kein Raum 5 | — |
| Mollgasse_EG | — (0) | 21 → 21 | 44/102 → 44/102 | final_exit 8 stair_exit 1 | FALLBACK 3 GRAPH 14 LINIE 103 | 51 → 51 (rz 24 SL 27) | ALLGEMEIN_ERSCHLIESSUNG 29 ALLGEMEIN_NEBENRAUM 7 WOHNUNG_PRIVAT 2 kein Raum 9 unbestimmt 4 | — |
| Muthgasse_E2 | — (0) | 22 → 22 | 113/193 → 113/193 | stair_exit 1 | FALLBACK 3 LINIE 139 | 139 → 139 (rz 86 SL 53) | ALLGEMEIN_ERSCHLIESSUNG 14 ALLGEMEIN_NEBENRAUM 5 LIFT 1 WOHNUNG_PRIVAT 62 kein Raum 57 | — |
| Rennweg_EG | — (0) | 2 → 2 | 20/40 → 20/40 | final_exit 2 stair_exit 3 | FALLBACK 2 GRAPH 5 | 17 → 17 (rz 9 SL 8) | ALLGEMEIN_ERSCHLIESSUNG 11 ALLGEMEIN_NEBENRAUM 3 kein Raum 3 | — |
| Rennweg_OG3 | — (0) | 2 → 2 | 17/18 → 17/18 | stair_exit 3 | FALLBACK 1 GRAPH 5 | 7 → 7 (rz 5 SL 2) | ALLGEMEIN_ERSCHLIESSUNG 6 kein Raum 1 | — |
| Mollgasse_1KG | — (0) | 0 → 0 | 0/28 → 0/28 | final_exit 1 | FALLBACK 4 | 14 → 14 (rz 7 SL 7) | ALLGEMEIN_ERSCHLIESSUNG 9 kein Raum 4 unbestimmt 1 | — |
| Mollgasse_2KG | — (0) | 1 → 1 | 2/46 → 2/46 | stair_exit 1 | FALLBACK 2 GRAPH 1 | 13 → 13 (antipanik 1 rz 8 SL 4) | ALLGEMEIN_ERSCHLIESSUNG 9 ALLGEMEIN_NEBENRAUM 3 LIFT 1 | — |
| AmRain_OG4 | — (0) | 11 → 11 | 30/59 → 30/59 | stair_exit 2 | FALLBACK 3 GRAPH 6 | 20 → 20 (rz 12 SL 8) | ALLGEMEIN_ERSCHLIESSUNG 13 WOHNUNG_PRIVAT 1 kein Raum 3 unbestimmt 3 | — |
| AmRain_UG | — (0) | 7 → 7 | 46/295 → 46/295 | final_exit 2 stair_exit 15 | FALLBACK 26 GRAPH 2 | 110 → 110 (rz 69 SL 41) | ALLGEMEIN_ERSCHLIESSUNG 78 ALLGEMEIN_NEBENRAUM 4 WOHNUNG_PRIVAT 8 kein Raum 16 unbestimmt 4 | — |
| AmRain_EG | `frei_1` 16.6: UNBEKANNT → **VORRAUM** (WOHNUNG_PRIVAT); `frei_2` 3.9: UNBEKANNT → **ABSTELLRAUM** (WOHNUNG_PRIVAT) (2) | 49 → 49 | 114/317 → 114/317 | final_exit 2 stair_exit 1 | FALLBACK 9 GRAPH 1 | 46 → 46 (rz 30 SL 16) | ALLGEMEIN_ERSCHLIESSUNG 14 ALLGEMEIN_NEBENRAUM 7 WOHNUNG_PRIVAT 4 kein Raum 10 unbestimmt 11 | — |
| AmRain_OG1 | `frei_1` 11.2: UNBEKANNT → **BALKON** (AUSSEN); `frei_3` 4.0: UNBEKANNT → **VORRAUM** (WOHNUNG_PRIVAT); `frei_4` 2.4: UNBEKANNT → **BALKON** (AUSSEN) (3) | 54 → 54 | 138/300 → 138/300 | stair_exit 7 | FALLBACK 16 GRAPH 12 | 73 → 73 (rz 49 SL 24) | ALLGEMEIN_ERSCHLIESSUNG 47 ALLGEMEIN_NEBENRAUM 1 SCHACHT 1 WOHNUNG_PRIVAT 5 kein Raum 6 unbestimmt 13 | `frei_5` nicht eindeutig »BAD«, »GANG« → BAD, GANG; kein dominanter Stempel |
| AmRain_OG2 | `frei_1` 4.0: UNBEKANNT → **VORRAUM** (WOHNUNG_PRIVAT) (1) | 42 → 42 | 134/264 → 134/264 | stair_exit 2 | FALLBACK 15 GRAPH 9 | 75 → 75 (rz 52 SL 23) | ALLGEMEIN_ERSCHLIESSUNG 57 WOHNUNG_PRIVAT 3 kein Raum 12 unbestimmt 3 | — |
| AmRain_OG3 | `frei_1` 2.7: UNBEKANNT → **VORRAUM** (WOHNUNG_PRIVAT) (1) | 21 → 21 | 84/129 → 84/129 | stair_exit 3 | FALLBACK 2 GRAPH 15 | 20 → 20 (rz 9 SL 11) | ALLGEMEIN_ERSCHLIESSUNG 16 WOHNUNG_PRIVAT 3 kein Raum 1 | — |

Fail-safe-Prüfung (Auftrag § 3 „ein Typ, durch den der Raum sein Notlicht verliert"): VORRAUM/ABSTELLRAUM
(WOHNUNG_PRIVAT) und BALKON (AUSSEN) sind Typen ohne Notlicht-Anspruch; die 7 Räume hatten als UNBEKANNT keine Leuchte
(Platzierung setzt in `frei_*` nur dort, wo ein Weg hindurchführt — OG1 `frei_2`), also verliert kein Raum eine
Leuchte. Der Typ ist durch Kürzel belegt (Entscheid 1), die Klasse privat/außen folgt dem Typ — dieselbe Lage wie die 27
WOHNUNG_PRIVAT-Wechsel in § 23.4.

### 24.6 Gate und Suite

**Gate:** `pytest -m gate tests/gate` 3 passed, 1 xfailed (`test_gate_tuerstapel_erfuellt`, wie vorher; 105 s).
`gate_messung` auf dem Arbeitsbaum dieses Commits (vor dem Commit, `_arbeit/gate/messung_8748e24-dirty-24.json`,
59,0 s), `pruefe_gate` gegen `nullmessung_f15d03f.json`: **(0)** unsauberer Arbeitsbaum (erwartet, vor dem Commit
gemessen) und **(3) `M4.einraum` DG2 0 → 1** (Enis Board 3, unverändert); M17 **18/18 BESTANDEN**; **alle Messfelder
außer `meta` gleich `messung_dad7bbd-dirty-23.json`** (Abschnitt 1) — die Gate-Pläne (Rennweg, Barawitzka) haben keine
`frei_*`.

**Volle Suite** (`pytest -q -p no:cacheprovider -rxXs`, allein, nach dem Blast): `6 failed, 2331 passed, 11 skipped, 6 deselected, 15 xfailed, 3 warnings in 1248.99s (20 min 49 s)`, 0 xpassed —
dieselben 6 roten wie § 21.1/§ 23.6 (3 × `test_keine_leuchten_in_wohnung_privat` OG1/OG2/DG1 = Board 1 Leonis,
`test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell`, die 2 S4c-Pins `test_bara_raum_19`/`raum_30`),
2331 = 2324 + 7 neue (5 Einheits- + 2 Naht-Tests); 15 xfailed, 11 skipped und die 3 Starlette-/httpx-Warnungen wie
§ 23.6. Kein Test umgestellt, keine Schwelle, kein Soll, kein Marker angefasst.

### 24.7 Offen nach Abschnitt 2

- **OG1 `frei_5`** (BAD + GANG + KOCHNISCHE in einem Polygon): UNBESTIMMT mit Notlicht, Ursache Polygonform/Wandlücken
  (R-05 b, § 16 „Polygonform"). Erst nach getrennten Polygonen typisierbar. P1 · Selman.
- **EG `frei_4` »ZI 2«**, KOCHNISCHE: Wörterbuch-/Kanon-Kandidaten mit F-Stufen-Blast (§ 23.5, § 23.7). Owner.
- **3 Räume ohne Text** (EG `frei_3` Vorraum-Stich, OG1 `frei_2` wohnungsinterne Stiege, OG4 `frei_1` Dachausstieg):
  nur über Erscheinungsbild oder zweite Meinung (Abschnitt 3, Phase B) zu typen — Kandidaten-Liste dort.
- **Türseiten an `frei_*` bleiben KEIN_RAUM** (alle 12, Tabelle 24.4): Türzuordnung läuft vor 2d; die typisierten Räume
  hängen deshalb nicht am Türgraph (keine Wohnung, keine Rolle an `tuer_242`, `tuer_205`, `tuer_206`, `tuer_98`). Neu
  zuordnen hieße Wohnungen und Fluchtwege nachziehen — nicht Teil von Abschnitt 2, gemeldet. P2 · Selman.
- **Platzierungs-Rückfall ohne `CAD_Symbole/photometrie` ist stumm** (24.4): `build_default_bundle` fällt ohne Katalog auf
  isotrop zurück, ohne Warnung in `bericht.md`. Leonis/gemeinsam (registry), gemeldet.
- `Projekte/_ergebnis/` nicht neu erzeugt (Verifikation über den Runner; Prüfstrecke am Abschluss).

## 25. Review 1 — Abschnitte 0–2 (adversarial, Kopf `5f15955`)

Geprüft mit eigenem Code (eigene Runner-Kopie `provider.parse(dxf, "")` + Default-Platzierung je Plan allein,
seriell, Am Rain und Muthgasse allein; Vorher = `git archive dad7bbd` von `src/` mit `CAD_Symbole/photometrie`
daneben, Nachher = Arbeitsbaum `5f15955`; eigener Vergleich je Raum/Tür/Ausgang/Segment/Leuchte, eigene
Kürzel-Stichprobe über alle TEXT/MTEXT des Modellraums, direkter ezdxf-Scan von Modell-, Papierbereich und
Blöcken). Runner, JSON und Skripte liegen im Session-Scratch, nicht im Repo.

**(1) Diff `cadb537..5f15955`:** `raumerkennung/` (`freiflaeche`, `kaskade`, `kuerzel_beleg` neu, `kuerzel_entscheid`,
`provider`), Tests (nur ergänzt: 0 gelöschte Zeilen unter `tests/`), `LUECKEN.md`, 12 PNG unter
`Projekte/_ergebnis/AmRain_*/unbekannt/`. Kein Contract, kein fremdes Paket, kein Owner-Import, keine lokalen Pfade
(Diff und Commit-Texte durchsucht). **Kein neuer RaumTyp:** `raumtyp.py` unverändert, jedes Label kommt aus
`raumtyp_flags` (alle 13 `RoomType` des Ports stehen in `_TYP_MAP`, der `text.upper()`-Rückfall kann nicht greifen);
`MEHRDEUTIG` und `_TROCKEN` nennen nur bestehende Kanon-Namen. Keine Schwelle, kein Soll, kein xfail/skip angefasst. Je
Punkt ein Commit (`dad7bbd` nur Doku/Bilder, `8748e24`, `5f15955`) mit zitiertem Rot-Lauf; letzte Zeile
`Co-Authored-By` wie gefordert. Zusätzlich nachgesehen: die vier neuen Testdateien **80 passed in 167.87s**, ruff
„All checks passed!".

**(2) Am Rain OG4 allein (Kopf `5f15955`, DXF sha256 `f3d31546…` = Zip-Kopie):** 28 Räume, `rest_2` 40,2 m²
**STIEGENHAUS** (Flags 11, ALLGEMEIN_ERSCHLIESSUNG; im Polygon die polygonlosen Stempel VR 8,52 / VR 6,87 /
STGH 32,44), **1 Stiegenhaus, 2 `stair_exit`** (`exit_tuer_27`, `exit_tuer_28`), **20 Leuchten** (rz 12, SL 8, 5 in
`rest_2`), GRAPH 6 + FALLBACK 3, Türen 30/59, keine Ausgangs-Warnung, `rest_6` 1,7 m² WC. Vorher (`dad7bbd`): 13
Leuchten, 0 Ausgänge, 0 Stiegenhäuser, FALLBACK 4. = § 23.3 und Gegenprobe § 20.4. Bestätigt.

**(3) Kürzel-Stichprobe** (Einfügepunkt gegen die Nachher-Polygone; 46 Normtexte mit Wörterbuch-Treffer, 1 222
Vorkommen auf 13 Plänen):

| Kürzel | Fundstelle | zählt? | Beleg |
|---|---|---|---|
| STGH | Am Rain OG4, `Raum-Beschriftung`, Handle `31ED7`, (12 320 / 12 909) | ja | in `rest_2` → STIEGENHAUS (oben) |
| VR, AR, BAD, WC | Am Rain OG4 je 4× `Raum-Beschriftung` | ja | alle 16 in Räumen (VORRAUM/ABSTELLRAUM/BAD/WC) |
| LOGGIA (Stempel) | Am Rain OG1 `frei_4`, OG1 `rest_4` | ja | → BALKON (Kanon, Wörterbuch `loggia`) |
| TREPPENHAUS | Am Rain UG `rest_23` (Stempel 29,8 m², dominant 62 %) | ja | → STIEGENHAUS gegen „Garage 2" |
| SCHLEUSE | Am Rain UG `rest_18` | ja | → SCHLEUSE |
| KIWA | Am Rain EG 3× in Räumen | ja | → KINDERWAGENRAUM (unverändert, Räume schon typisiert) |
| **Plankopf: „Erdgeschoss-STG4/5/6"** | Am Rain EG, **Papierbereich** `Layout2`, Layer `ET_LEGENDE - Wohnung$0$800_AL_ALLG_L` (Viewport-Titel) | **nein** | `kuerzel_typ` → STIEGENHAUS, aber nur der Modellraum wird geladen; zusätzlich trifft der Layer `_ZONEN_LAYER` (`LEGEND`). Papierbereiche aller 13 Pläne: nur diese 6 Treffer |
| **Legende: „AR", „VR", „Stiegenhaus"** | Rennweg EG, Archicad-Zonenstempel-Legende als INSERT-ATTRIB (Handles `1D2`, `22A`, `240`) bei (11 814 197 / 355 053 689), ≈ 0,7 km westlich / 1,2 km südlich der Plan-Bounds | **nein** | ATTRIB wird von `kuerzel_texte` nicht gelesen, Punkt in keinem Polygon; Rennweg EG/OG3 feldgleich |
| **Summenblöcke neben dem Gebäude** | Am Rain, `Raum-Top-Beschriftung`: „Loggia" 105×, „Terrasse/Balkon" 89× außerhalb jedes Polygons | **nein** | nur über das Polygon-Kriterium — **nicht** über die Form-Regel (25.6 b) |
| HT (Elektro) | Am Rain OG3/OG4, `E_Beschriftung`, 112× | nein | → TECHNIK, alle bei x ≈ 34 600 m (Elektro-Overlay in anderem Koordinatensystem), in keinem Polygon |

**(4) Blast 13 Pläne (`dad7bbd` → `5f15955`, je Plan allein):** **56 Typwechsel** (= 49 aus § 23.4 + 7 `frei_*` aus
§ 24.4; alle UNBEKANNT → Typ, kein typisierter Raum verliert seinen Typ), **Leuchten 560 → 596**, `stair_exit`
23 → 39, `final_exit` 16 = 16, Stiegenhäuser 42 → 44, Räume weg/neu 0; Rennweg EG/OG3, Mollgasse EG/1KG/2KG,
Muthgasse E2 feldgleich (nur die `kuerzel:`-SR-Warnungen Barawitzka `raum_27`, Muthgasse `raum_52`/`raum_71`);
Laufzeit/Spitze wie § 24.5 (EG 319 s / 2,71 GB, Muthgasse 251 s / 1,79 GB). Jeden Typwechsel mit den Kürzel-Texten und
polygonlosen Stempeln im Polygon selbst nachgesehen: 55 plausibel, **1 widerlegt (UG `rest_7` → GARAGE, 25.6 a)**.
Regelkonform, aber im Bericht zu nennen (Polygon fasst mehr, R-05 b): UG `rest_3` 45,8 / `rest_5` 56,8 / `rest_8`
152,5 / `rest_32` 90,0 m² GANG enthalten je den Stempel „ELEKTRO" (Kanon-Kandidat § 23.1 d) — die Elektroräume laufen
als GANG mit; UG `rest_6` 87,5 m² SCHLEUSE enthält HAUS1–5 und KELLERABTEILE 1; OG1 `rest_19` 14,5 m² GANG (Stempel
GANG 3,06 m² + KOCHNISCHE). Alle in fail-safe-Richtung (Erschließung mit Notlicht). **Leuchten-Verluste je Raum:** 8
Räume, keiner mit Typwechsel — Platzierung entlang neuer GRAPH-Wege (UG `raum_29` STIEGENHAUS 3 → 2, `rest_12` GANG
1 → 0, `rest_17` GANG 2 → 1, `raum_13` SCHLEUSE 2 → 1, `raum_38` GANG 24,7 m² 1 → 0; OG1 `raum_59` VORRAUM 4 → 2,
`rest_24` GANG 3,2 m² 1 → 0; OG4 `rest_1` GANG 2 → 1): von keiner Raumerkennungs-Regel gedeckt, sondern Leonis-Lane
(§ 23.7 gemeldet); drei Fluchtweg-Räume enden ohne Leuchte. **Zwei Klassen-/Wohnungswechsel ohne Typwechsel:** OG1
`raum_61` GANG 21,7 m² (top_38 → keine Wohnung, Klasse None → ALLGEMEIN_ERSCHLIESSUNG, Leuchten 1 → 2) und UG `raum_22`
GANG 16,5 m² (top_2 → keine, Leuchten 2 → 4) — Folge neuer Türrollen (`wohnungseingang`) an frisch typisierten
Nachbarn (OG1 `rest_6` WOHNZIMMER, UG `rest_5`/`rest_8`); in § 23.4 als Mitgliedswechsel geführt, fail-safe
(Notlicht-Gewinn), aber ein Wohnungs-Gang wird zur Erschließung → Board 1 Leonis. Fluchtweg-Warnungen UG 10 → 44, EG
12 → 21 wie § 23.4.

**(5) Die 6 Stempel-Räume und die 12 Bilder:** eigener Lauf bestätigt § 24.4 Zeile für Zeile (EG `frei_1` VORRAUM,
`frei_2` ABSTELLRAUM, OG1 `frei_1`/`frei_4` BALKON, OG1 `frei_5` UNBESTIMMT mit `kuerzel:`-Warnung „nicht eindeutig
— »BAD«, »GANG« … kein dominanter Stempel", OG3 `frei_1` VORRAUM; dazu OG1 `frei_3`, OG2 `frei_1` VORRAUM ohne
Flächenzeile; EG `frei_3`/`frei_4`, OG1 `frei_2`, OG4 `frei_1` UNBEKANNT; alle ohne Wohnung, Leuchten 0 → 0). Alle 12
PNG angesehen: Raum magenta, Stempeltext lesbar, wo einer liegt; Nachbarn/Türen wie in der Tabelle § 22. Am Bild OG1
`frei_5`: die Wände zwischen Kochnische, Bad und Gang sind gezeichnet (Wandlayer), nur nicht als Wandkörper erkannt —
Polygonform, nicht Typregel (§ 24.7).

**(6) Gate:** `pytest -m gate tests/gate` **3 passed, 1 xfailed** (105 s). `gate_messung` auf dem sauberen Kopf
(`messung_5f15955_review1.json`, `commit_head 5f15955`, `arbeitsbaum_src_scripts_sauber true`, 59,4 s), `pruefe_gate`
gegen `nullmessung_f15d03f.json`: **nur (3) `M4.einraum` DG2 0 → 1**; M17 **18/18 BESTANDEN**; alle Messfelder außer
`meta` gleich `messung_e0c820d`, `messung_dad7bbd-dirty-23` und `messung_8748e24-dirty-24`.

### 25.6 Befunde (Widerlegung und Offenes)

- **(a) Am Rain UG `rest_7` 8,7 m² → GARAGE ist falsch (widerlegt, offen).** Das Polygon ist der Elektroraum:
  Raum-Beschriftung „9.56 m²" liegt im Polygon, der Stempel „ELEKTRO" 0,1 m außerhalb, Nachbarn `raum_31` STIEGENHAUS
  42,3 m² und `raum_36` ABSTELLRAUM (Fahrradraum) 101,9 m², Türen `tuer_194`/`durchgang_28` zu `raum_36`. Im Polygon
  liegen sonst nur Elektro-Beschriftungen auf Layer `E_Bauangaben` (ZP-15 ×2, Trennkasten, Allgemein, Sibel 2, Sibel 5,
  **„Garage 1"** — Stromkreis-/Verteilerbeschriftung). Die Kürzel-Regel liest „Garage 1" als Raumkürzel →
  GARAGE (ALLGEMEIN_NEBENRAUM, Flags 01), 1 Sicherheitsleuchte neu (0 → 1). Kein Notlicht-Verlust, aber falscher Typ
  (LB-Regel `notlicht_kw_garage` adressiert GARAGE; der Elektroraum hat keinen Kanon-Typ und bliebe nach § 23.1 d
  UNBESTIMMT). § 23.4 führt den Wechsel unkommentiert; § 23.1 (a) nennt „GARAGE 1/2 (Layer E_Bauangaben)" in
  untypisierten Räumen ohne Folge. Ursache: der Owner-Ausschluss (Legende, Plankopf, Schnitt-/Achsmarken) deckt
  Elektro-/Verteilerbeschriftung nicht, `_ZONEN_LAYER` kennt keine Elektro-Layer. **Nicht korrigiert — Regelentscheid
  Owner:** Option A Layer-Ausschluss für Elektro-Beschriftung (`E_Bauangaben`, `E_Beschriftung`; Wirkung auf den 13
  Plänen: genau `rest_7` → UNBEKANNT, „HT" 112× liegt ohnehin außerhalb, „Garage 2" in `rest_23` unterliegt dem
  dominanten TREPPENHAUS), Option B Positivliste der Raumlabel-Layer je Plan-Dialekt. Die 13 getrackten Ergebnisse der
  Prüfstrecke (Phase A, Vergleichsbasis) tragen den Fehler mit, solange er offen ist. **P1 · Selman (Owner).**
- **(b) Summenblock-Zeilen passieren die Form-Regel — § 23.1 (c) ist in diesem Punkt falsch (offen).** „Loggia" (ein
  Wort) und „Terrasse/Balkon" (zwei Teile, beide im Wörterbuch) sind der Form nach Kürzel (`kuerzel_typ` → BALKON bzw.
  TERRASSE); ausgeschlossen sind nur „Wohnfläche (inkl.Loggia)" und „Terrasse/Balkon/Garten". Gemessen (13 Pläne):
  „Loggia" auf `Raum-Top-Beschriftung` 124×, davon **5 in untypisierten Räumen** (EG `rest_11` ×3, `rest_23`, `rest_29`
  — dort machen sie die Räume zusammen mit den „TERRASSE"-Stempeln „nicht eindeutig" → UNBESTIMMT statt TERRASSE; § 23.4
  nennt dafür „Terrasse/Loggia/Garten-Stempel mehrerer Tops", tatsächlich ist „Loggia" dort die Summenzeile), 10 in
  TERRASSE-, 3 in BALKON-, 1 in STIEGENHAUS-Räumen (alle gestempelt, keine Wirkung), 105 außerhalb; „Terrasse/Balkon"
  90×, 89 außerhalb, 1 in OG3 `raum_41` STIEGENHAUS (gestempelt). Auf den 13 Plänen also **kein falscher Typ**, aber ein
  Summenblock mit nur einer „Loggia"-Zeile in einem untypisierten Polygon würde BALKON (AUSSEN, ohne Notlicht) typen.
  Ebenso der Form nach Kürzel: „Zul.Müll" (Lüftung) → MUELLRAUM (1×, in keinem Raum). Owner (Form-Regel oder Layer).
  **P2 · Selman.**
- **(c) Statische Klasse der `frei_*` umgeht K4/S7 (Abschnitt 2, offen).** `frei_*` VORRAUM bekommen WOHNUNG_PRIVAT
  statisch (`nutzungsklasse_fuer`); Kaskaden-VORRAUMs in gleicher Lage (keine Türanbindung, kein Aufenthaltsraum in
  der Wohnung) bleiben nach K4 „Klasse offen, Notlicht bleibt" — EG `rest_3` VORRAUM (`top_20`, Klasse None, Warnung
  „k4: … G4: kein Aufenthaltsraum in top_20") und 6 weitere VORRAUM auf EG. Gemessen ohne Leuchten-Folge (596 = 596),
  aber Fluchtweg-Räume (Flags 11) mit KEIN_RAUM-Türen erhalten die private Klasse ohne die K4-Sicherung (G4).
  Owner-Frage: K4 auch für `frei_*`? **P2 · Selman.**
- **(d) ATTRIB-Kürzel ungelesen (gemerkt).** `kuerzel_texte` liest nur TEXT/MTEXT des Modellraums; Zonenstempel als
  INSERT-ATTRIB (Rennweg, Mollgasse `01-SQM`) kommen nur über `finde_stempel` (mit Flächenzeile). Ein ATTRIB-Kürzel
  ohne Flächenzeile bliebe unsichtbar — auf den 13 Plänen kein Fall (alle ATTRIB-Stempel tragen AREA). P3.
- **(e) Platzierung:** 3 Fluchtweg-Räume ohne Leuchte nachher (UG `rest_12` GANG 1,7 m², `raum_38` GANG 24,7 m², OG1
  `rest_24` GANG 3,2 m²) und 2 Wohnungs-Gänge, die Erschließung werden (OG1 `raum_61`, UG `raum_22`) — Leonis, Board 1
  (§ 23.7).

**Fazit Review 1:** Abschnitt 0 und Abschnitt 2 bestätigt; Abschnitt 1 bestätigt in Regel, Abnahme (OG4), Gate und
Blast-Zahlen, **widerlegt in einem Typwechsel** (UG `rest_7`, a) und in einer Doku-Aussage (Summenblock, b). Keine
Bänder gesenkt, Gate wie erwartet. Nichts am Code geändert (a–c sind Regelentscheide des Owners).

## 25a. Abschnitt 3 Teil A — KI-Zweitmeinung offline: Schnittstelle, Backends, Konfiguration, Cache (Entscheid 3; erledigt mit dem Commit dieses Eintrags)

**Auftrag (Owner 2026-10-01, `docs/AUFTRAG_2026-10-01.md` § 3, Freigabe „Option 3, erweitert“):** „Modul mit
Schnittstelle und beiden Backends, Konfiguration, Cache, … alle Tests mit synthetischen oder gespeicherten Antworten,
Backend-Test mit der Limit-Meldung als Fall ‚Warnung, kein Abbruch‘." Phase A: **keine Live-Aufrufe** (Kontingent bis
2026-10-03 19:10 erschöpft), kein Push. Teil A = das Modul ohne Verdrahtung in `provider.parse`; Herkunfts-Ausweis im
Bericht, die Entscheidungsregeln „Erscheinungsbild ist Wahrheit" und die drei synthetischen Entscheidungs-Tests
(Kürzel vs. KI, Notlicht-Verlust, die 6 Räume ohne Stempel) sind Teil B. Stand vorher `b61cb4d` (Review 1).

### 25a.1 Voraussetzung nachgeprüft (ohne Aufruf)

`codex exec --help` der installierten codex-cli 0.159.2 (Desktop-App-Bundle, nicht im PATH): Prompt `[PROMPT]` oder
`-` = **stdin** („If not provided as an argument (or if `-` is used), instructions are read from stdin"); Bilder
`-i, --image <FILE>...` (Mehrfachwert — deshalb je Bild `--image=<Datei>` als EIN Argument, sonst schluckt das Flag
das folgende `-`); Antwortform `--output-schema <FILE>`; letzte Nachricht `-o, --output-last-message <FILE>`;
`-s read-only`, `--ephemeral`, `--skip-git-repo-check`, `--json` (JSONL-Events), `-m <MODEL>`, `-c key=value`.
Kein Live-Aufruf; die Limit-Antwort vom 2026-10-01 liegt als Fixture `tests/fixtures/ki/codex_limit.jsonl`
(4 JSONL-Zeilen `thread.started` / `turn.started` / `error` / `turn.failed`, `thread_id` anonymisiert, PowerShell-
Rauschen entfernt).

### 25a.2 Modulaufbau (`raumerkennung/`, zwei Dateien, nichts Bestehendes geändert)

- **`ki_zweitmeinung.py`** (anbieterneutral): `KiKonfig` · `RaumAnfrage` / `GeschossAnfrage` (Plan-Datei, Geschoss,
  Quadrant, Bilder, Räume mit `engine_typ`, `beleg`, `merkmale`) · `RaumAntwort` (`raum_id`, `raum_typ` ∈ Kanon ∪
  {UNBESTIMMT}, `sicherheit` 0–1, `bestaetigt`, `begruendung`) · `KiFehler` (`art` ∈ timeout | limit | login | format
  | sonstig, `meldung`) · `Antwort` (Räume, `verworfen`, Fehler, `roh`, Modell, Quelle backend | cache | aus) ·
  Protocol `ZweitmeinungBackend.frage(anfrage, modell=None) → Antwort` (runtime-checkable) · `kanon_typen()` =
  `_TYP_MAP ∪ _EXTRA_DIRECT ∪ _EXTRA_OVERRIDE` aus `raumtyp.py` (dieselbe Maschinen-Quelle wie `docs/VOKABULAR.md` § 1
  und `tests/contract/test_vokabular_doku.py`; **kein neuer RaumTyp**, UNBESTIMMT ist keiner, nur die erlaubte
  Enthaltung) · `ANTWORT_SCHEMA` (JSON-Schema für `--output-schema`) · `parse_antwort(text, raum_ids)` (Code-Fence und
  nackte Liste toleriert; je Raum verworfen bei fehlendem/falsch typisiertem Feld, Typ außerhalb Kanon, unbekannter
  `raum_id`, `sicherheit` ∉ [0, 1], Dublette; kein JSON → `format`) · `baue_prompt(anfrage)` (Rolle, Geschoss/Quadrant,
  Kanon-Liste, Ausgangs-Definition aus Abschnitt 5 wörtlich, Räume als JSON, Antwortform; **keine lokalen Pfade**;
  `PROMPT_VERSION = "1"`) · `KiCache` · `Zweitmeinung` (Cache → Backend → Cache; Zähler `anfragen`, `treffer`;
  `warnungen` als `ki: <art> — <meldung> …; Engine-Ergebnis bleibt unverändert, Räume ohne Typ bleiben UNBESTIMMT mit
  Notlicht`; Backend-Ausnahme → `sonstig`; Fallback-Modell einmal bei `sonstig`/`format`/`timeout`, **nicht** bei
  `limit`/`login` — die gelten kontoweit).
- **`ki_backends.py`:** `CodexAboBackend` (`codex exec --json --ephemeral --skip-git-repo-check -s read-only -m
  <modell> -c model_reasoning_effort=<effort> --output-schema <tmp> -o <tmp> --image=<Bild>… -`; Prompt über stdin;
  `subprocess.run` mit **Argumentliste**, nie Shell-String; `cwd` = Temp-Ordner; Zeitlimit `zeitlimit_s` →
  `TimeoutExpired` = `timeout`; Kindprozess-Umgebung ohne `OPENAI_API_KEY`/`ANTHROPIC_API_KEY`; JSONL-Parser liest
  `error`/`turn.failed` → Fehlerart per Muster („usage limit|rate limit|quota|429" → limit, „logged in|login|auth|
  401|403" → login, sonst sonstig) und `item.completed`/`agent_message` → Text, Rückfall auf die `-o`-Datei; fehlendes
  Bild oder fehlendes Binary → `sonstig` ohne Aufruf) · `finde_codex(konfig_pfad)` = Konfiguration → `PATH` →
  `%LOCALAPPDATA%/OpenAI/Codex/bin/*/codex.exe` (jüngstes zuerst) · `OpenaiApiBackend` = Gerüst (Klasse,
  Konfiguration, liefert `KiFehler sonstig` „nicht freigeschaltet", kein Key im Repo, liest keinen) · Registry
  `BACKENDS = {codex_abo, openai_api}` + `backend_aus_konfig(konfig)`; ein späteres `claude_abo` ist genau ein
  weiterer Eintrag (Test hängt eine Dummy-Klasse ein, ohne Engine-Änderung).
- Modell/Stufe immer explizit: `-m` und `-c model_reasoning_effort=…` stehen in jedem Aufruf, auch beim Fallback;
  `KiKonfig` lehnt `effort` außerhalb low | medium | high ab (**nie xhigh für die Engine**).

### 25a.3 Konfiguration (`KiKonfig`, Dataclass im Repo + Umgebung; kein Key, keine Login-Daten)

| Schlüssel | Standard | Umgebung |
|---|---|---|
| `an` | **aus** (`False`) | `NOTBEL_KI=an` (auch `1`/`true`/`ja`; alles andere = aus) |
| `backend` | `codex_abo` | `NOTBEL_KI_BACKEND` |
| `modell` | `gpt-6-astra` | `NOTBEL_KI_MODELL` |
| `effort` | `high` | — (nie xhigh, `ValueError`) |
| `fallback_modell` | `gpt-5.6-sol` (`""` = keiner) | — |
| `zeitlimit_s` | 300 | — |
| `cache_pfad` | `knowledge/ki_cache/` (Repo-Wurzel) | — |
| `prompt_version` | `"1"` (= `PROMPT_VERSION`) | — |
| `codex_binary` | `None` → PATH → App-Bundle | `NOTBEL_KI_CODEX` |

**Ohne KI läuft alles wie bisher — 0 Verhaltensänderung, belegt durch den Diff:** `git diff --stat b61cb4d` leer
(keine bestehende Datei geändert; nur neue Dateien `ki_zweitmeinung.py`, `ki_backends.py`, Test, Fixture,
`knowledge/ki_cache/README.md`), `grep ki_zweitmeinung|ki_backends` in `src/` und `scripts/` außerhalb der beiden
Module **0 Treffer** — kein Pfad der Engine importiert das Modul, ein Blast kann hier nur identische Zahlen liefern.
Der Blast „KI aus" wird in Teil B gefahren, wenn `provider.parse` das Modul kennt (dann ist er ein Beleg).

### 25a.4 Cache (`knowledge/ki_cache/`, Ort begründet)

Die Engine liest den Cache zur **Laufzeit**, nicht nur die Tests — also weder `tests/fixtures/` (Testmaterial) noch
im Paket `src/` (getrackte JSON im Code). `knowledge/` ist der getrackte Ort für Wissensdaten außerhalb des Codes;
`scripts/wissen_index.py` indiziert dort nur `extracted/**/*.md`, der Cache stört `knowledge/INDEX.md` nicht.
Schlüssel = Pfad `<plan>_<sha16>/<geschoss>_<quadrant|ganz>_<backend>_<modell>_v<prompt_version>.json` (Plan-Datei
als SHA-256 des Inhalts, 16 Hex, je Lauf memoisiert über Größe + mtime; Namen über `[^A-Za-z0-9_.-]` → `_`
bereinigt, kein lokaler Pfad im Schlüssel, nur der Dateiname). Inhalt: `schluessel`, `gespeichert` (UTC), `raeume`,
`verworfen`, `roh`; beim Lesen wird `roh` neu durch `parse_antwort` geprüft (strengerer Kanon wirkt ohne Aufruf).
**Treffer → kein Aufruf**; **Fehler werden nie gecacht**. Zähler `anfragen` (echte Aufrufe) und `treffer` je
`Zweitmeinung`-Instanz = je Lauf, für „Anzahl Anfragen je Lauf" im Bericht (Teil B). Der Ordner trägt heute nur
`README.md` (Format, Ort, Regeln) — Einträge entstehen erst mit den ersten Aufrufen in Phase B.

### 25a.5 Tests (`tests/raumerkennung/test_ki_zweitmeinung.py`, 26 + 1 skip; nie live)

Kanon = `raumtyp`-Kanon ohne UNBESTIMMT/UNBEKANNT · Mock, codex_abo, openai_api erfüllen das Protocol ·
Parsing gültig / Code-Fence + Liste + Kleinschreibung / kein JSON und Objekt ohne `raeume` → `format` / 7 Verwerfungen
(außerhalb Kanon „BÜRO", unbekannte `raum_id`, `sicherheit` 1,5, `bestaetigt` „ja", leere Begründung, Felder fehlen,
kein Objekt) / Dublette zählt einmal · Konfig Standard aus, `xhigh` → `ValueError`, `aus_umgebung` an/aus/Backend/
Modell · Cache-Schlüssel mit allen Teilen, anderer Dateiinhalt → anderer SHA, andere Prompt-Version → anderer Pfad ·
**Cache-Treffer verhindert Aufruf** (Mock zählt: 1 Aufruf bei 3 Fragen über zwei Instanzen, 2. Quadrant → 2. Aufruf,
2 Dateien, kein `\`/`:` im Schlüssel) · Fehler nicht gecacht, kein Abbruch, Warnung „Engine-Ergebnis bleibt" ·
Fallback bei `sonstig`, keiner bei `limit` · Backend-Ausnahme → `sonstig` · KI aus → kein Aufruf, kein Cache-Ordner
· Registry: beide Backends, `claude_abo` als Dummy-Klasse eingehängt, unbekannt → `ValueError` · openai_api Gerüst
liest keinen Key (`OPENAI_API_KEY` gesetzt, Meldung ohne Key, Quelltext ohne `sk-`) · **codex_abo mit gemocktem
`subprocess.run`:** Argumentliste (`exec`, `--json`, `--ephemeral`, `--skip-git-repo-check`, `-s read-only`, `-m
gpt-6-astra`, `-c model_reasoning_effort=high`, `--output-schema`, `-o`, `--image=<Pfad mit Leerzeichen>` als ein
Element, `-` zuletzt), kein `shell`, Prompt in `input` ohne lokale Pfade, `timeout` = Konfig, `cwd` ≠ Plan-Ordner,
**`env` ohne `OPENAI_API_KEY`/`ANTHROPIC_API_KEY`** bei erhaltenem `PATH`, Schema-Datei mit `raeume` + 5
Pflichtfeldern, Fallback-Aufruf mit `-m gpt-5.6-sol` und Effort · **Limit-Fixture → `art=limit`, über `Zweitmeinung`
eine `ki:`-Warnung mit „UNBESTIMMT", kein Fallback, keine Ausnahme** · Login-fehlt (synthetisches JSONL — die echte
Meldung ohne Login ist nicht aufgezeichnet) → `login` · `TimeoutExpired` → `timeout`; Prosa statt JSON und leeres
stdout → `format` · `-o`-Datei als Rückfall ohne `agent_message` · ungültige Räume aus JSONL verworfen ·
Binary-Suche Konfig / PATH (gemocktes `shutil.which`) / App-Bundle-Glob (`LOCALAPPDATA` auf tmp) / nichts → `sonstig`
ohne Aufruf · fehlendes Bild → `sonstig` ohne Aufruf · Prompt trägt Kanon, Ausgangs-Definition („Innenhof", „ins
Freie"), Raum-IDs, Geschoss, Quadrant, Antwortfelder, keine Pfade · `test_codex_live_minimal` nur mit
`NOTBEL_KI_LIVE=1` (Standard **skip**).

**Rot vor dem Fix** (`pytest tests/raumerkennung/test_ki_zweitmeinung.py --tb=line`, Kopf `b61cb4d` + Test + Fixture):

```
test_ki_zweitmeinung.py:15: ImportError: cannot import name 'ki_backends' from 'notbeleuchtung.raumerkennung'
1 error in 1.40s
```

**Grün nach dem Fix:** `26 passed, 1 skipped in 1.26s` (skip = Live-Test). `pytest tests/raumerkennung
tests/contract`: **990 passed, 7 skipped, 2 xfailed in 147.51s** (davon 26 neu, 1 neuer skip). ruff: „All checks
passed!" (FURB167/ISC004/UP017/BLE001/RUF059 aus dem ersten Lauf behoben, `# noqa: BLE001` wie `pipeline.py:280`).

### 25a.6 Gate

`pytest -m gate tests/gate` **3 passed, 1 xfailed** (`test_gate_tuerstapel_erfuellt`, 109 s). `gate_messung` auf
dem Arbeitsbaum vor dem Commit (`_arbeit/gate/messung_b61cb4d-dirty-25a.json`, 59,3 s), `pruefe_gate` gegen
`nullmessung_f15d03f.json`: **(0)** unsauberer Arbeitsbaum (erwartet, vor dem Commit) und **(3) `M4.einraum` DG2
0 → 1** (Enis Board 3, unverändert); M17 **18/18 BESTANDEN**; **alle Messfelder außer `meta` gleich
`messung_8748e24-dirty-24.json`** (Abschnitt 2) — erwartet, kein Gate-Plan erreicht das Modul.

### 25a.7 Offen nach Teil A (Teil B / Phase B)

- **Teil B (Phase A, offline):** Verdrahtung in `provider.parse` nach Kürzel-Regel und bestehenden Regeln (ein
  Aufruf je Geschoss, Quadranten wie Vision-Audit, gerendertes Bild mit Raum-IDs, Merkmale je Raum: Texte, Fläche,
  Möbel-/Sanitärblöcke, Fenster, Türen, Treppen/Lift, Lage zur Wohnungstür, Nachbarn); Entscheidungsregeln
  (übereinstimmend → bestätigt; Widerspruch bei Stempel/Kürzel/Erscheinungsbild → Engine-Typ bleibt, strittig;
  unbelegt → KI-Typ ab 0,8 ohne Geometrie-Widerspruch; Notlicht-Verlust nur mit bestätigender Regel, sonst UNBESTIMMT
  mit Notlicht); Herkunft je Raum (Engine | KI | bestätigt | strittig) und `ki:`-Warnungen + Anzahl Anfragen in
  `bericht.md` (`scripts/plan_pruefen.py`, kein Contract-Feld); die drei synthetischen Entscheidungs-Tests und der
  Test der 6 Räume ohne Stempel mit gespeicherten Antworten; **Blast „KI aus" 13 Pläne feldgleich** als Beleg der
  0-Verhaltensänderung nach der Verdrahtung; Prüfstrecke KI aus als Vergleichsbasis.
- **Phase B (ab 2026-10-03 19:10, live):** Format-Annahme des Erfolgsfalls (`item.completed` mit `item.type =
  agent_message` und `text`) ist **nicht live geprüft** — dafür der `-o`-Rückfall; erster Aufruf mit
  `NOTBEL_KI_LIVE=1 pytest -k codex_live` prüft Binary, Login, Schema-Flag und Antwortform. Echte Login-fehlt-Meldung
  aufzeichnen und die synthetische Fixture ersetzen. Eichung (Stempel abgedeckt, Trefferquote je Typ ≥ 95 %, kein
  Fehler bei Notlicht-Verlust-Typen), Prüfer-Durchgang, Lern-Kandidaten, Cache-Einträge ins Repo.
- Fallback-Semantik (einmal `gpt-5.6-sol` bei `sonstig`/`format`/`timeout`, nie bei `limit`/`login`) ist hier
  festgelegt, nicht vom Owner — bei Bedarf ändern. **Modell dieses Agenten: claude-fable-5-1 (Stufe laut Auftrag xhigh;
  vom Agenten selbst nicht prüfbar).**

## 25b. Abschnitt 3 Teil B — KI-Zweitmeinung: Anfrage-Aufbau, Entscheidungsregeln, Herkunfts-Ausweis, Verdrahtung (Entscheid 3; erledigt mit dem Commit dieses Eintrags)

**Auftrag (Owner 2026-10-01, `docs/AUFTRAG_2026-10-01.md` § 3, Freigabe „Option 3, erweitert“):** zweite Meinung je
Geschoss nach Kürzel-Regel und bestehenden Regeln; die KI bekommt das gerenderte Geschoss mit Raum-IDs, je Raum Typ +
Beleg, Texte, Fläche, Möbel-/Sanitärblöcke, Fenster, Türen, Treppen/Lift, Lage zur Wohnungstür, Nachbarn, Kanon und
Ausgangs-Definition; „Erscheinungsbild ist Wahrheit, KI ist zweite Meinung“; Herkunft je Raum im Bericht; Fehler →
Warnung, kein Abbruch. Phase A: **keine Live-Aufrufe**, alle Tests mit synthetischen/gespeicherten Antworten. Stand
vorher `be9cc57` (Teil A, § 25a).

### 25b.1 Rot vor dem Fix

`pytest tests/raumerkennung/test_ki_entscheid.py --tb=line -q` auf `be9cc57` + neuer Test + Fixtures:

```
E   ModuleNotFoundError: No module named 'notbeleuchtung.raumerkennung.ki_anfrage'
1 error in 1.52s
```

### 25b.2 Anfrage-Aufbau (`raumerkennung/ki_anfrage.py`, neu)

- **Belege je Raum** (`belege_je_raum`): `stempel` = Raum mit zugeordnetem Kaskaden-Stempel (`k.zuordnungen`, auch
  ohne Kanon-Typ — Vokabular-Fälle wie „GESCHÄFTSLOKAL“) bzw. im Wandzyklen-Pfad ohne Wandkörper ein Wörterbuch-Text
  von `raumtyp.beschrifte_raeume` im Polygon; `kuerzel` = Entscheid 1 (`k.hinweise` „`<id>: Kürzel …`“) oder
  Entscheid 2 (`freiflaeche_befund` „neuer Raum `frei_n` … Entscheid 2“); `erscheinungsbild` = K3-Sanitärbeleg
  (`sanitaer_befund` „`<id>: BAD|WC aus Sanitärbeleg`“); `geometrie` = jeder andere Typ (Treppen-/Schacht-/Gang-Regeln,
  `typisiere_geometrisch`, `rest_komponenten`); leer = ohne Typ und ohne Stempel (UNBEKANNT/UNBESTIMMT, mehrdeutiges
  Kürzel). Nur aus Strings und Zuordnungen, kein Parse — läuft auch mit KI aus (Herkunfts-Ausweis).
- **Merkmale je Raum** (nur mit KI an): `flaeche_m2`; `texte` = TEXT/MTEXT **und** ATTRIB/Blocktexte der INSERTs im
  Polygon (Rennweg-Stempel sind Blöcke — ohne Blocktexte fehlte „Wohnküche 38,35 m²“; Stempel-artige Texte zuerst,
  gekappt auf 16); `objekte` = Möbel-/Sanitärblöcke nach Blockname (**`sanitaer.moebelklasse`/`moebelobjekte`,
  neu**: Owner-Liste Bett, Herd, Spüle, Sofa, Esstisch, Waschmaschine, Auto zusätzlich zur K3-Liste WC, Waschbecken,
  Dusche, Wanne, Bidet; Layer `M.BEL|EINBAU|SAN|FURN|MOB|EINRICHT|GENM|PKW|STELLPL|PARK`; Blocknamen der 13 Prüfpläne aus
  der Inventur 2026-10-02 im Test; Am Rain zeichnet Möbel als Linien → dort leer; **die K3-Regel liest weiter nur
  `objektklasse`/`sanitaerobjekte`, unverändert**); `fenster` = `fenster_signatur.finde_rahmenfenster(wandsegmente,
  Wand-Union des Providers)` bis 400 mm am Polygon; `stiegen` = Treppenläufe aus `objekt_stiege.finde_stiegen`, die das
  Polygon schneiden; `lift` = Lift-Text (`lift_erkennung._LIFT_TEXT`) oder Lift-Block im Polygon; `tueren` = Türen des
  Raums mit **korrigierter Rolle** (`wohnungsklasse.korrigierte_rollen`, E7), `blatt`, `zu` (Gegenraum, AUSSEN, null =
  KEIN_RAUM); `wohnung`, `wohnungseingang_am_raum`, `klasse`, `nachbarn` (Polygone ≤ `wohnungsumriss.NACHBAR_MM` =
  500 mm, mit Typ).
- **Quadranten wie beim Vision-Audit** (`audit_render` auf `selman/vision-audit`, nur als Vorbild gelesen): längste
  Seite der Raum-Hülle > `QUADRANT_AB_MM` = 40 m → vier Ausschnitte NW/NO/SW/SO mit 1 m Überlappung, sonst ein
  Ausschnitt `ganz`; ein Raum gehört zum Quadranten seines `representative_point`; Quadranten ohne Raum werden nicht
  gefragt. Ein Aufruf je Ausschnitt; der Cache-Schlüssel trägt den Quadranten (§ 25a.4).
- **Bild** (`rendere_bilder`): derselbe Weg wie `plan_pruefen._figur` (ezdxf-Zeichen-Addon → matplotlib, weißer
  Grund, `min_dash_length` 50 mm gegen Punkt-Linientypen, Standard-Font DejaVuSans), **einmal** gezeichnet, dann je
  Quadrant Ausschnitt + 1 m Rand, längste Seite 1 600 px, Räume halbtransparent (untypisiert magenta), Label = Raum-ID +
  Engine-Typ (`?` ohne Typ) am `representative_point`. matplotlib bleibt optionale Abhängigkeit (`render`/`dev`): Import
  erst im Rendern, ohne KI wird nichts gerendert. Bilder leben in einem Temp-Ordner nur während der Frage; **gerendert
  wird nur für Fragen ohne Cache-Treffer** (`Zweitmeinung.im_cache`, neu) — Suite und Gate mit Cache brauchen kein Bild.
- **Eichungs-Option `stempel_abdecken`** (`KiKonfig.stempel_abdecken`, Standard aus): ein `Frontend`-Nachfahre lässt
  TEXT/MTEXT/ATTRIB weg — auch in Blöcken; die `filter_func` des Addons sieht nur Top-Level-Entities — und `texte`
  fehlt in den Merkmalen. Der Test misst weniger Tinte im Bild bei stehenden Raum-Labels.
- **Probe ohne Aufruf** (Scratch-Backend zeichnet nur auf, nicht im Repo): Rennweg_OG3 9,3 s gesamt (Parse vorher
  2,4 s), 1 Frage `ganz`, 16 Räume, Prompt 13 384 Zeichen, Bild 1 300 × 1 600 px — Stempel, Möbel und Raum-IDs lesbar
  (angesehen); Am Rain OG4 41,5 s (vorher 16,8 s), 4 Quadranten mit 12/1/8/7 Räumen, Prompts 2,7–11,5 k Zeichen
  (Quadrant NW angesehen: Stempel „ZI 2 10.53 m²“, Sanitär, Raum-IDs, magenta `rest_3` lesbar); Mollgasse EG 52,6 s
  (vorher 15,2 s), 3 Quadranten (SW ohne Raum) mit 25/15/22 Räumen, Prompts 14–25 k Zeichen. Der Mehraufwand
  (Fenster-Signatur O(n²), Treppenläufe, Render) fällt nur mit KI an.

### 25b.3 Entscheidungsregeln (`ki_zweitmeinung.zweitmeinung_anwenden`, neu; anbieterneutral, ohne Plan)

| Fall | Regel (Auftrag § 3) | Umsetzung |
|---|---|---|
| Engine-Typ = KI-Typ | bestätigt | Herkunft **bestätigt**, Grund = KI-Begründung + Sicherheit (Typgleichheit zählt, nicht das Feld `bestaetigt`) |
| Engine-Typ belegt, KI widerspricht | Engine bleibt, strittig | Herkunft **strittig**, beide Begründungen (Beleg der Engine; KI-Typ, Sicherheit, Begründung); belegt = jeder gesetzte Typ (stempel, kuerzel, erscheinungsbild, geometrie) |
| Engine-Typ, KI UNBESTIMMT | — | Herkunft **Engine** „KI enthält sich“ |
| ohne Typ, KI-Typ | KI-Typ ab 0,8 ohne Geometrie-Widerspruch | nacheinander: Sicherheit < `SICHERHEIT_MIN` 0,8 → nein; `geometrie_widerspruch` (Fläche außerhalb `FLAECHE_PLAUSIBEL_M2`: WC 0,8–8, BAD 1,5–25, ABSTELLRAUM 0,5–30, VORRAUM 1–40, KÜCHE 2–40, LIFT 0,8–12, SCHACHT 0,05–8, STIEGENHAUS 4–200, GANG 1,5–500, GARAGE ≥ 10, BALKON 0,5–80, TERRASSE 1–500 m²; andere Typen frei — **hier festgelegt, Owner änderbar**) → nein; LIFT/SCHACHT (`KEIN_RAUM_TYPEN`) nur mit Lift-/Schacht-Evidenz im Polygon (Lift-Text/-Block, Schacht-Text SCHACHT/DDB/BDB aus `rest_komponenten`) → sonst nein; Typ nicht in der **Freigabeliste** (`FREIGABE`/`KiKonfig.freigabe`, **heute leer**) → nein, Herkunft Engine „KI-Vorschlag …, nicht freigegeben (Eichungs-Freigabeliste, Phase B)“; sonst übernommen → Herkunft **KI** |
| Typ mit Notlicht-Verlust | nur mit bestätigender bestehender Regel, sonst UNBESTIMMT mit Notlicht | `verliert_notlicht(typ)` = Nutzungsklasse WOHNUNG_PRIVAT **und** Flags 00 aus `raumtyp.py` — genau die Bedingung in `platzierung/flaechen_strategy.py` (S2; nur gelesen): ZIMMER, SCHLAFZIMMER, KINDERZIMMER, WOHNZIMMER, KÜCHE, BAD, WC, ABSTELLRAUM; VORRAUM (Flags 11) nicht. Bestätigende Regel = `regel_bestaetigt(raum, typ)`, im Provider die K3-Sanitärregel (`sanitaer_typ` der Objekte im Polygon = KI-Typ); ohne Bestätigung bleibt `raum_typ` leer, Klasse None → Notlicht (Grundsatz (a)) |
| Stempel ohne Kanon-Typ (Vokabular, Enis) | — | nie umtypisiert, KI-Vorschlag nur Hinweis (wie `kuerzel_beleg`: „sein Stempel ist sein Name“) |
| Fehler/Timeout/Limit/verworfen | Engine unverändert, Warnung, kein Abbruch | Herkunft **Engine** mit Fehlerart bzw. Verwerfungsgrund; `ki:`-Warnung aus `Zweitmeinung` (§ 25a) |

Übernahme setzt `raum_typ`, `ist_fluchtweg`/`ist_communal` (Kanon-Flags) und die **statische** Nutzungsklasse
(`nutzungsklasse_fuer`) — wie Abschnitt 2 an den `frei_*`; `wohnung_id` nie (Grundsatz (b)). Kein neuer RaumTyp:
`kanon_typen()`/`kanon_flags()` lesen `raumtyp.py`; UNBESTIMMT ist keine Übernahme. Der Prompt nennt jetzt die
Merkmal-Legende und die Beleg-Werte; `PROMPT_VERSION` bleibt „1“ — Version 1 wurde nie live gesendet, es gibt keinen
Cache-Eintrag dazu.

### 25b.4 Herkunfts-Ausweis

- Provider-Attribut `ArchitekturRaumProvider.ki_ergebnis` (`ki_anfrage.KiErgebnis`: `an`, `backend`, `modell`,
  `herkunft` je Raum = `Herkunft(raum_id, herkunft, engine_typ, beleg, ki_typ, sicherheit, grund)`, `warnungen`
  (`ki: …`), `fragen`, `anfragen` = echte Aufrufe, `treffer` = Cache-Treffer) — **kein Contract-Feld**, kein
  Board-Antrag nötig.
- `bericht.md` (`scripts/plan_pruefen.py`, nur Berichtsausgabe): neuer Abschnitt **„Raumtyp-Herkunft (Abschnitt 3 …)“**
  mit KI an/aus + Backend/Modell, Fragen/Anfragen/Cache-Treffer, Zähler je Herkunft und Tabelle `Raum | Typ | Herkunft
  | Beleg | KI-Typ (Sicherheit) | Begründung` für jeden Raum; die `ki:`-Warnungen stehen zusätzlich unter „Warnungen“.
  Mit KI aus heißt jede Zeile „Engine“ mit Beleg — das ist die Vergleichsbasis für Phase B.

### 25b.5 Verdrahtung (`provider.parse`)

`ArchitekturRaumProvider(ki_konfig=None, ki_backend=None)` — None = `KiKonfig.aus_umgebung()` (Standard aus) und
Backend aus der Registry; `build_default_bundle()` ruft weiter `ArchitekturRaumProvider()`. Die zweite Meinung läuft
**nach** `fuelle_freie_flaechen` (Kürzel-Regel Entscheid 1/2, Sanitärregel, Wohnungen sind durch) und **vor**
`leite_ausgaenge`/`fluchtwege` — dieselbe Stelle wie Abschnitt 2: ein übernommener Typ wirkt auf Ausgänge, Fluchtwege
und Anker, nicht auf die rohen Türrollen und Wohnungen (die kommen aus rohen Türen, Grundsatz (b)). `zweite_meinung`
wirft nie (jede Ausnahme → `ki: sonstig`-Warnung). **Ohne KI:** nur Belege + Herkunft „Engine“ je Raum, kein Render,
keine Fenster-/Treppen-Suche, kein Cache-Ordner (Test). Räume, die erst nach dieser Stelle entstehen (LIFT aus
`finde_lifte`), tragen keine Herkunftszeile.

### 25b.6 Tests (`tests/raumerkennung/test_ki_entscheid.py`, 24, nie live; Fixtures `tests/fixtures/ki/`)

- **(i) die 6 Räume ohne Stempel aus § 22** (`amrain_6_ohne_stempel.json`: EG `frei_3`/`frei_4`, OG1 `frei_2`/
  `frei_3`, OG2 `frei_1`, OG4 `frei_1` mit Fläche, Texten, Nachbarn, Türen aus § 22 und **synthetischer** Antwort):
  Freigabeliste leer → **kein Raum verändert**; EG `frei_3` (KI VORRAUM 0,85) und EG `frei_4` (KI ZIMMER 0,92) Herkunft
  Engine „nicht freigegeben“, OG1 `frei_2` (KI STIEGENHAUS 0,70) Engine, OG1 `frei_3`/OG2 `frei_1` (Kürzel VR, KI
  VORRAUM) **bestätigt**, OG4 `frei_1` KI UNBESTIMMT („Dachausstieg“) Engine. Mit Freigabe {VORRAUM, ZIMMER,
  STIEGENHAUS}: EG `frei_3` → **VORRAUM** (Flags 11, kein Notlicht-Verlust, Klasse WOHNUNG_PRIVAT, ohne Wohnung); EG
  `frei_4` ZIMMER verliert Notlicht, keine Regel → bleibt UNBESTIMMT mit Notlicht; OG1 `frei_2` 0,70 < 0,80 → bleibt.
- **(ii)** Raum mit Kürzel AR, KI WC 0,95 (freigegeben) → ABSTELLRAUM bleibt, strittig, beide Begründungen; dasselbe für
  Stempel STIEGENHAUS vs GANG und Sanitärbeleg BAD vs ABSTELLRAUM.
- **(iii)** UNBESTIMMT-Raum, KI SCHLAFZIMMER 0,95 (freigegeben), keine Regel → bleibt ohne Typ, Klasse None (Notlicht);
  mit bestätigender Regel (BAD) → übernommen, `wohnung_id` bleibt None. `verliert_notlicht` für die 8 Typen ja, VORRAUM/
  GANG/STIEGENHAUS/BALKON/SCHACHT nein.
- weitere Regeln: Freigabeliste heute leer (`FREIGABE == frozenset()`, `SICHERHEIT_MIN == 0.8`); 0,79 → nein; 60-m²-WC
  → Geometrie-Widerspruch; SCHACHT nur mit Evidenz; Stempel ohne Kanon-Typ nie umtypisiert; Fehler/verworfen → alles
  unverändert.
- Anfrage-Aufbau: Belege aus Zuordnung/Hinweisen/Befunden; `moebelklasse` an 19 Blocknamen der Prüfpläne (inkl.
  Negativfälle Schreibtisch, Bewegungsfläche `2D_barrierefrei_WC`, Raumstempel-Block `Bad_WC__3`, Schrank); Merkmale
  je Raum auf einer synthetischen 3-Raum-DXF (Stempel STIEGENHAUS / ohne Text / Kürzel »AR«, 3 Sanitärblöcke in der
  Mitte → `objekte {DUSCHE 1, WASCHBECKEN 1, WC 1}`), `stempel_abdecken` ohne `texte`; Quadranten `ganz` bzw. 4 mit
  1 000 mm Überlappung; Bild: PNG ≥ 1 200 px, weniger Tinte ohne Stempeltexte, noch weniger ohne Raum-Labels.
- Verdrahtung: KI aus → Typen {STIEGENHAUS, —, ABSTELLRAUM} wie vorher, Herkunft Engine je Raum mit Belegen, kein
  Cache-Ordner; KI an mit Mock (Freigabe leer) → **Modell `model_dump` identisch** zum Lauf ohne KI, 1 Anfrage mit
  PNG, Herkunft bestätigt/Engine „nicht freigegeben“/strittig; zweiter Lauf → Cache-Treffer, kein Aufruf; Freigabe
  {BAD}: Mittelraum mit 3 Sanitärblöcken, den K3 nicht typt (kein Wohnungsumriss) → **BAD** aus KI + Sanitärregel;
  ohne Sanitärblöcke → bleibt ohne Typ (Notlicht).
- **(iv) Backend codex_abo mit gespeicherten Antworten** (`subprocess.run` gemockt): `codex_antwort_synth.jsonl`
  (synthetisches `agent_message`-JSONL für die 3-Raum-DXF) über den **Provider** → Argumentliste mit `--image=`,
  Kindprozess ohne `OPENAI_API_KEY`, Herkunft bestätigt/strittig/„nicht freigegeben“, Antwort gecacht;
  `codex_limit.jsonl` (echte Limit-Meldung vom 2026-10-01) → **Modell identisch** zum Lauf ohne KI, genau eine
  `ki: limit`-Warnung „Engine-Ergebnis bleibt unverändert“, ein Aufruf (kein Fallback), nichts gecacht, Herkunft Engine
  mit „limit“.
- Prüfstrecke: `plan_pruefen.plan_pruefen` auf der 3-Raum-DXF (Ausgabe nach tmp) schreibt „Raumtyp-Herkunft“ mit „KI
  aus“, „Anfragen 0“, „Cache-Treffer 0“ und die Zeilen `| STIEGENHAUS | Engine | stempel |`, `| ABSTELLRAUM | Engine |
  stempel |` (Wandzyklen-Pfad: jeder Wörterbuch-Text ist dort Stempel von `beschrifte_raeume`).

**Grün nach dem Fix:** `24 passed in 3.38s`; mit `test_ki_zweitmeinung`, `test_sanitaer`, `test_provider`,
`test_freiflaeche`, `test_kuerzel_beleg`: `183 passed, 2 skipped in 38.49s`; ruff „All checks passed!“.

### 25b.7 Blast „KI aus“ — 13 Pläne feldgleich (Beleg der 0-Verhaltensänderung nach der Verdrahtung)

Runner wie § 12/§ 20 (eigene Kopie außerhalb des Repos: `provider.parse(dxf, "")` + Default-Platzierung, JSON je Raum/
Tür/Ausgang/Segment/Anker/Leuchte, dazu Texte und Stempel des Plans), seriell über die 13 DXF der Prüfstrecke auf dem
Arbeitsbaum dieses Eintrags (`be9cc57-dirty`, Umgebung ohne `NOTBEL_KI*`), Am Rain und Muthgasse allein, kein pytest
parallel. Vergleich gegen den Stand von Abschnitt 2 (`8748e24-dirty-24` = Inhalt `5f15955`; `b61cb4d` und `be9cc57`
änderten keine bestehende Datei, § 25a.3): **13 gleich, 0 abweichend** über alle 22 Felder je Plan (Räume, Türen,
Ausgänge, Segmente, Anker, Stiegenhäuser, Bounds, korrigierte Rollen, bestätigt privat, alle Warnungen, Texte, Stempel,
Faktor, Leuchten je Kind/Klasse/Stück) — Rennweg EG R24 T40 A5 L17, OG3 R17 T18 A3 L7, Barawitzka EG R49 T71 A1 L11,
Mollgasse EG R64 T102 A9 L51, 1KG R31 T28 A1 L14, 2KG R30 T46 A1 L13, Am Rain OG4 R28 T59 A2 L20, OG3 R60 T129 A3 L20,
OG2 R103 T264 A2 L75, OG1 R139 T300 A7 L73, UG R82 T295 A17 L110, EG R140 T317 A3 L46, Muthgasse E2 R108 T193 A1 L139;
DXF-SHA je Plan gleich. Laufzeit/RAM wie Abschnitt 2 (Am Rain EG 312 s, 2,71 GB; Muthgasse 254 s, 1,79 GB), stderr
ohne Traceback. Die Prüfstrecke `scripts/plan_pruefen.py` über alle 13 Pläne (VERLAUF.md, `Projekte/_ergebnis/`) läuft
im Abschluss der Phase A mit KI aus — dann mit dem neuen Abschnitt „Raumtyp-Herkunft“ als Vergleichsbasis.

### 25b.8 Gate

`pytest -m gate tests/gate` **3 passed, 1 xfailed** (`test_gate_tuerstapel_erfuellt`, 108 s). `gate_messung` auf dem
Arbeitsbaum vor dem Commit (`_arbeit/gate/messung_be9cc57-dirty-25b.json`, 59,3 s), `pruefe_gate` gegen
`nullmessung_f15d03f.json`: **(0)** unsauberer Arbeitsbaum (erwartet, vor dem Commit) und **(3) `M4.einraum` DG2
0 → 1** (Enis Board 3, unverändert); M17 **18/18 BESTANDEN**; **alle Messfelder außer `meta` gleich
`messung_b61cb4d-dirty-25a.json`** (Teil A). Suite `pytest tests/raumerkennung tests/contract`: **1014 passed, 7 skipped,
2 xfailed in 150.66s** (990 + 24 neu). Bekannt rote Tests (4 + 2 S4c-Pins) unberührt, kein Band abgesenkt, kein
Contract-Feld, kein neuer RaumTyp, kein fremdes Paket geändert (`platzierung/flaechen_strategy.py` nur gelesen).

### 25b.9 Offen nach Teil B (Phase B ab 2026-10-03 19:10)

- **Freigabeliste füllen** aus der Eichung (Stempel abgedeckt: `KiKonfig(stempel_abdecken=True)`, Trefferquote je Typ
  ≥ 95 %, Notlicht-Verlust-Typen ohne einen Fehler) — bis dahin übernimmt die KI nichts; die 6 Räume ohne Stempel (§ 22)
  bleiben UNBEKANNT/UNBESTIMMT mit Herkunft „KI-Vorschlag, nicht freigegeben“.
- **Erfolgsformat live prüfen** (`item.completed`/`agent_message`, `--output-schema`, `--image=`), erste echte
  Antworten in `knowledge/ki_cache/`; Prüfstrecke mit KI an, Prüfer-Durchgang, Lern-Kandidaten.
- **Lage der zweiten Meinung** vor Ausgängen/Fluchtwegen, aber nach Türrollen/Wohnungen: ein übernommener Typ ändert
  heute keine rohe Türrolle und keine Wohnung. Soll er das (z. B. KI-VORRAUM → Wohnungseingang wandert), braucht es
  denselben Probelauf wie K3 (`_tueren_und_wohnungen` auf Kopien) — Owner-Entscheid, nicht hier gebaut.
- **Flächen-Plausibilität** (`FLAECHE_PLAUSIBEL_M2`) und **KEIN_RAUM-Evidenz** (Lift-Text/-Block, Schacht-Text) sind
  hier festgelegt; die Eichung kann sie belegen oder ändern. Am Rain liefert keine Möbelblöcke (Linien) — dort trägt
  die KI die Möbel nur aus dem Bild.
- `PROMPT_VERSION` bleibt „1“ (nie live gesendet, kein Cache-Eintrag); jede weitere Prompt-Änderung in Phase B wird „2“.
- **Modell dieses Agenten: claude-fable-5-1 (Stufe laut Auftrag xhigh; vom Agenten selbst nicht prüfbar).**
