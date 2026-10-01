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
  Stempel übernehmen wäre ein neuer Entscheid (BALKON/LOGGIA → AUSSEN). P1 · Selman.
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
