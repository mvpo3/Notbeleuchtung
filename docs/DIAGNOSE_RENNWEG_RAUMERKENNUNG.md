# Diagnose Rennweg - Raumerkennung

| Feld | Wert |
|---|---|
| Stand | 2026-09-15 |
| Owner | Selman (raumerkennung) |
| Branch | `selman/diagnose-rennweg` |
| Basis | `origin/main` 2f610cc (Baum identisch mit f5d86a2) |
| Output-Commit | 511ad36. Alle Zahlen beziehen sich auf diesen Output, mit einer markierten Ausnahme: Tür- und Wohnungskennzahlen aus `Projekte/_ergebnis/**/kennzahlen.json` (Gesamtdarstellung, Commit 1e642ad, ohne `commit`-Feld). Sie sind als „Bestand 1e642ad“ gekennzeichnet. 1e642ad ist Vorfahr von 511ad36; `git diff --name-only 1e642ad 511ad36 -- src scripts` nennt nur `platzierung/{deckung,fachpraxis,platzierer,stgh_strategy}.py` und `scripts/analyse/raumerkennung_darstellung.py`, also keine Datei unter `raumerkennung/`. |
| Code-Stand | `src/` und `scripts/` seit 511ad36 unverändert (`git diff --stat 511ad36 HEAD -- src scripts` leer). Zeilennummern gelten auf HEAD und damit für den Output. |
| Status | **Analyse und Plan - kein Code geändert, kein Output neu erzeugt, nicht gepusht.** |

**Grundlage.** Architektpläne `Projekte/Rennweg/<PLAN> - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf` (PLAN = UG, EG, OG1, OG2, OG3, DG1, DG2; byte-identisch mit dem Eingang). Output `Projekte/_ergebnis_raumerkennung/Rennweg/<PLAN> .../` (`uebersicht.png`, `kennzahlen.json`, `_cache.pkl`), erzeugt von `scripts/analyse/raumerkennung_darstellung.py` (`_erkennen` Z.364-446). Feedback-Zitate stammen 1:1 aus Leonis' Rückmeldung; Leonis schreibt 1OG/2OG/1DG/2DG für die Dateien OG1/OG2/DG1/DG2.

**Methode.** Acht thematische Cluster (K1, K2a, K2b, K3, K4, K5, K6a, K6b) mit je zwei unabhängigen Gegenprüfungen (Linse „Code-Pfad + Plan-Beleg“ und Linse „Allgemeingültigkeit + Blast Radius + Fachfrage“) sowie vier Vorher-Messungen (M1-M4) mit je einer Nachrechnung auf anderem Weg.

- **Gelesen (HEAD):** `src/notbeleuchtung/raumerkennung/` (provider, kaskade, raumlayer, stempel_anker, stempel_flutung, rest_komponenten, wandkoerper, material_matching, legende_import, aussenbereich, geometrie_typ, lift_erkennung, stiegenhaus, gang_anker, tueren, tuer_zuordnung, tuer_typisierung, wohnungen, nutzungsklasse, raumtyp, kuerzel_entscheid, bereinigung, fenster_signatur, breitenprofil, layer_features, footprint, kreuzcheck, fluchtweg, ausgaenge, geschoss, dxf_load, `_port/models/room.py`, `_port/parsers/architecture_dxf.py`, `_port/parsers/door_blocks.py`, `_port/parsers/apartment_clustering.py`, Port-Profile), `src/notbeleuchtung/hauptengine/contracts/raum_modell.py` und `projekt_kontext.py`, `src/notbeleuchtung/platzierung/` (fachpraxis, flaechen_strategy, gang_strategy, bausteine, oib_gate), `src/notbeleuchtung/wissen/materialien.yaml`, `src/notbeleuchtung/normwissen/data/*.yaml`, `scripts/analyse/raumerkennung_darstellung.py`, `scripts/analyse/gesamtdarstellung.py`, `scripts/plan_pruefen.py`, `tests/raumerkennung/*`, `tests/naht/*`, `docs/OFFENE_FRAGEN.md`, `docs/COORDINATION.md`, `docs/ENIS_UEBERGABE_0908.md`, `docs/HANDOFF_SELMAN.md`, `Projekte/_ergebnis_raumerkennung/BERICHT.md`, eingecheckte Ergebnisse unter `Projekte/_ergebnis/` und `Projekte/_ergebnis_alle/`.
- **Werkzeuge (außerhalb des Repos):** Planausschnitt-Render in Originalfarben mit Overlay (Raumpolygone, offene Außenbereiche, Stempel), Entity-Inventar je Ausschnitt (rekursiv in Blöcken, mit Layer, Farbe, Text, Block-Bbox), Rohbyte-Suche in DXF (`grep -a`, `od -c`), `git log/show/blame/diff/status`.
- **In-memory aufgerufene Einzelfunktionen (je ein Python-Prozess, nur Rennweg-DXF):** `dxf_load.lade_dxf`; `wandkoerper.finde_wandkoerper`, `wand_union`, `aussenkontur`; `aussenbereich._wand_geschlossen`, `aussenkontur_komponenten`, `erkenne_aussenbereiche`, `grundstuecksgrenze`, `aussen_indizien`, `_strassenkante`; `raumlayer.raeume_aus_layer`; `kaskade.raeume_aus_kaskade`; `rest_komponenten.komponenten_ohne_stempel`, `_marker_punkte`, `_typisiere` (auch per Monkeypatch-Mitschnitt von `label`, `_vektorisiere`, `_typisiere`); `geometrie_typ.stiege_rechtecke`, `typisiere_stiegenhaus`, `typisiere_geometrisch`; `lift_erkennung.finde_lifte`; `stiegenhaus.baue_stiegenhaus_modell` (mit `tueren=[]`); `stempel_anker.finde_stempel`; `material_matching.bestimme_material`; `raumtyp.raumtyp_flags`, `_port.models.room.classify_room`; `nutzungsklasse.nutzungsklasse_fuer`; `tueren.tueren_aus_dxf`, `tuer_oeffnungen`, `im_planbereich`, `_ist_tuer_block`; `tuer_zuordnung.ordne_tueren`, `durchgaenge_ohne_tuerblatt`, `aussen_durchgaenge`; `tuer_typisierung.typisiere_tueren`; `wohnungen.bilde_wohnungen`; `bereinigung.bereinige` (synthetische bzw. simulierte Schacht-Ausstanzung); `wandkoerper.bounds_aus_wandkoerpern`; `objekt_stiege.finde_stiegen` (nur DG2). Zusätzlich synthetische Geometrien (Wandring mit Lücke, Diele mit Stiegenhaustür, Wand ohne Lücke). Befehl und Kernausgabe der Aufrufe, auf denen Ursachen und Slice-Erwartungen beruhen: **Anhang B**; Quelltexte der dafür verwendeten Diagnose-Skripte: **Anhang A.5-A.10**.
- **Nicht ausgeführt:** `ArchitekturRaumProvider.parse`, `hauptengine.pipeline.run`, `scripts/analyse/*.py`, `scripts/plan_pruefen.py`, `pytest`. Nichts unter `Projekte/` neu erzeugt; im Repo nur dieses Dokument angelegt.
- **Teilketten-Rekonstruktion:** Für die Tür- und Wohnungsbefunde (B.7, B.11, B.15) wurde die Teilkette `provider.parse` Z.64-149 aus den Einzelfunktionen nachgebaut. `parse` selbst wurde nicht aufgerufen, keine Datei geschrieben; der Abgleich `wohnung_id` mit dem Cache ist identisch. Vorbehalt zur Nutzungsklasse siehe U19.
- **Auslegung „kein Pipeline-Re-Run“:** von Selman am 2026-09-15 bestätigt. Einzelne Erkennungsfunktionen in-memory aufrufen und Zwischenzustände belegen ist erlaubt; kein `provider.parse`, keine Pipeline, kein neuer Output unter `Projekte/_ergebnis*`.
- **Abweichung von der Nur-Rennweg-Regel:** Eine Gegenprüfung (K2b, Linse 2) hat Schacht-Vokabular in `Barawitzka_EG`, `Mollgasse_EG` und `Muthgasse_E2` per Textzählung erfasst; weitere Gegenprüfungen haben eingecheckte `raeume.json` anderer Projekte gelesen. Diese Zahlen sind als Rohtext- bzw. Bestandsbelege gekennzeichnet, nicht als Package-Messung.

---

## 0. Kurzfassung - Ursachenkarte

Alle Messwerte: Output 511ad36, 7 Rennweg-Pläne. „korr.“ = von der Nachrechnung korrigierter Wert.

| ID | Ursache (ein Satz) | Feedback-Punkte | Datei:Zeile Funktion | Art | Sicherheit | Messwert vorher |
|---|---|---|---|---|---|---|
| U1 | Die achsparallele Bbox eines Treppenblocks wird als eigener STIEGENHAUS-Raum angehängt, wenn kein Raum ≥ 2 m² ihren Mittelpunkt deckt. | DG2-5, DG2-7 (`stiegenhaus_2`-Anteil), S-H1, S-H4 (DG2-Überdeckung) | `geometrie_typ.py:47-63` `stiege_rechtecke`; `geometrie_typ.py:73-96` `typisiere_stiegenhaus` | Code | hoch | M1: 1 achsparalleles STIEGENHAUS im gedrehten Plan, 15,86 m² (DG2 `stiegenhaus_2`) |
| U2 | Die Treppenmarker-Regel (Bbox-Zentrum ≤ 1000 mm) greift vor der SCHACHT-Regel; Liftschacht-Innenräume und der DBA-Schacht werden STIEGENHAUS, `finde_lifte` stanzt nur die Kabine und lässt einen Ring. | DG2-3, S-H1 | `rest_komponenten.py:57-86` `_marker_punkte`; `rest_komponenten.py:92-100` `_typisiere`; `lift_erkennung.py:177-210` `finde_lifte` | Code + Fachfrage F1 | hoch | M1: 6 STIEGENHAUS < 2 m² ohne Stempel (5 am Lift, 1 mit Text „DBA SCHACHT“) |
| U3 | Es gibt keinen Schacht-Detektor aus Planzeichen; die Architektenzone enthält die Schachtzellen, die R-Stufe sperrt Zonen und verwirft < 1 m², Bereinigung Regel 1 bekommt nie ein Paar. | EG-1, OG1-1, OG1-2, OG1-3 (Schächte H1/WP), DG1-1, DG1-2, DG2-4, DG2-6 (2. Satz), S-H3 | `raumlayer.py:67-78, 98-124`; `kaskade.py:173-175`; `rest_komponenten.py:42, 147-164`; `wandkoerper.py:36-37, 43-47, 136, 142-155`; `material_matching.py:272-276`; `stempel_anker.py:209-211` | Code + Fachfrage F3 | hoch | M3 korr.: 34 Nicht-Schacht-Räume mit roter Schachtfläche ≥ 0,02 m² (11,456 m²) |
| U4 | Die R-Stufe labelt mit 8er-Nachbarschaft und vektorisiert nur die größte Kontur; eine diagonal verbundene Schachtreihe geht still verloren. | DG2-4 (Teil), S-H3 | `rest_komponenten.py:156-164` `komponenten_ohne_stempel`; `stempel_flutung.py:204-207` `_vektorisiere` | Code | hoch | DG2: 1,843 m² verloren (Maske 5,838 m² → Polygon 3,995 m²) |
| U5 | SCHACHT wird ohne Planzeichen-Evidenz vergeben („< 3 m² und türlos“); Dach-Wandkörper erweitern die R-Kontur, eine Dachfenster-Nische wird SCHACHT. | DG2-6, S-H3 | `rest_komponenten.py:98-100` `_typisiere`; `rest_komponenten.py:119-137` | Code + Fachfrage F4 | hoch | M3: `fp_ohne_text` 1 (DG2 `rest_5`, 1,42 m²) |
| U6 | Fenster und Fenstertüren ohne Wandkörper bzw. dünn schraffierte Wände: das Closing mit d = 1200 mm versiegelt Lücken nur dickenabhängig (≥ 2,4 m nie); die Außenfläche fließt über den Hüllrand in Zimmer. | OG1-4 (Außenanteil), OG2-1, DG1-4 (Nordzimmer), DG2-1 und DG2-2 (Nischenanteil), DG2-7 (Terrassenseite), DG2-8, S-H2, S-C | `wandkoerper.py:164-173` `finde_wandkoerper`; `aussenbereich.py:51-56, 129-138` `_wand_geschlossen`; `aussenbereich.py:256-271` | Code + Fachfrage F8 | hoch | M2 nach Abzug von U7: DG1 4, OG1 3, OG2 2, OG3 2, DG2 1 (`raum_5`) = 12 Innenräume (B.1). Die S1-Akzeptanz (5.2) nennt 15 verbleibende Räume; die Differenz 3 sind DG2 `raum_2`/`raum_4` (Straßenseite, Ursache U9 + U8) und DG2 `stiegenhaus_2` (Randstreifen, U1). |
| U7 | Die Randprüfung arbeitet mit 250 mm Abstand statt Topologie; ein Loch der geschlossenen Wandunion 193 mm vor dem Hüllrand wird offen. | DG1-3, DG1-4, S-H2 (DG1/OG3-Teil) | `aussenbereich.py:58, 260-262, 268-271` `erkenne_aussenbereiche` | Code (+ F7) | hoch | offen DG1 143,83 → 40,07 m², OG3 114,03 → 35,66 m² ohne Löcher |
| U8 | Die Außenanalyse kennt keine Räume und Stempel: kein Innen-Veto nach Fachregel S-C, `gedeckt()` enthält die Zonen nicht. | S-C, OG1-4, OG2-1, DG1-3, DG1-4, DG2-1, DG2-2, DG2-7, S-H2 (DG2-Straßenfront) | `aussenbereich.py:227-271` `erkenne_aussenbereiche`; `aussenbereich.py:91-98` `gedeckt`; `provider.py:114-117` | Code + Fachfrage F6 | hoch | M2: 20 Innenräume ohne Freiflächen / 304,14 m² Schnitt; korr. inkl. Freiflächen 24 |
| U9 | Die Raumkontur ist die ArchiCAD-Zone 1:1; in DG2 reicht sie bis 1,27 m über die Dachschnitt-Innenkante, in OG1 endet sie vor einer ungeschraffierten 480-mm-Wandschicht. | DG2-1, DG2-2, DG2-7 (Straßenseite), DG2-8, OG1-4, S-H2 | `raumlayer.py:67-78, 98-124`; `kaskade.py:102-103` | Fachfrage F5 | hoch (Mechanismus) | DG2 Zone − geschlossene Wand, größte Komponente (B.13): Bad 24,00 → 16,20 m², Zimmer 59,28 → 40,49 m² |
| U10 | Die R-Stufe rechnet nur in `aussenkontur(d=1000)`; diese zerfällt in DG1, der zonenlose möblierte Wohnbereich wird nie Raum. | DG1-3, S-H2 (DG1-Wohnzimmer) | `rest_komponenten.py:119-137`; `wandkoerper.py:251-262` `aussenkontur` | Code + Fachfrage F9 | hoch | DG1 R-Kontur 73,5 m² gegen Gebäudekomponente 196,8 m² (B.13); freie Fläche 16,94 m² ohne Raum |
| U11 | Der Bildausschnitt wird nur aus Raumpolygonen (+ 6 %) gebildet. | DG1-3, S-H2 (Bildanteil) | `raumerkennung_darstellung.py:277-306` `_ausschnitte`; `raumerkennung_darstellung.py:397-402, 429` `_erkennen` | Code (nur Prüfbild) | hoch | DG1: 1,77 m² Wand und 0,49 m² freie Fläche außerhalb des Bildes |
| U12 | ArchiCAD-Türblöcke tragen einen gemeinsamen Welt-INSERT außerhalb des Hauses; Position und Winkel kommen daraus, `im_planbereich` verwirft alle echten Türen. | S-H4, OG1-3 | `tueren.py:169-181` `tuer_oeffnungen`; `tueren.py:36` `_DOOR_HINT`; `tueren.py:360-373` `im_planbereich`; `kaskade.py:110-115`; `provider.py:83-97` | Code | hoch | Öffnungen vor → nach Filter: OG1 11 → 2, OG3 14 → 3, DG1 7 → 2, DG2 5 → 1, EG 17 → 10 |
| U13 | `durchgaenge_ohne_tuerblatt` macht bei Wänden < 250 mm jede gemeinsame Wandkante ≥ 800 mm zum Durchgang (Breite = Wandlänge), dazu Nullflächen-Splitter und Überlappungen. | S-H4, OG1-3; S-C und S-H2 als Folge (U19, dasselbe Kriterium in `aussen_durchgaenge`) | `tuer_zuordnung.py:133-160` `durchgaenge_ohne_tuerblatt` | Code (+ F10) | hoch | OG1 Bad↔Gang 4830 mm, Zimmer↔Wohnküche 5711 mm; DG2 18 Türen mit Rolle `wohnungseingang`, alle `durchgang_*` ohne Türblatt (in-memory Türkette B.7; gleiche Zahl in `tuer_typen` Bestand 1e642ad); davon 10 in `eingangs_tuer_ids` von `top_1` |
| U14 | Ein Vorraum mit Tür ins Stiegenhaus wird Erschließung; seine Zimmertüren kippen zu Wohnungseingängen, Nebenräume werden eigene Wohnungen. | S-H4, OG1-1, OG1-2 (jeweils Einraum-Wohnung) | `wohnungen.py:32-55` `_verfeinere_gang_privat`; `wohnungen.py:71-80, 90-93` `bilde_wohnungen` | Code + Fachfrage F11 | hoch (Mechanismus), Fix strittig | M4: OG1 `top_2` AR, `top_3` WC; 8 VORRAUM ALLGEMEIN_ERSCHLIESSUNG ohne Wohnung |
| U15 | Stempel ohne Kanon-Treffer („Wohnkche“ ohne ü im Plan, „Wohnbereich“, „TV Raum“) bleiben untypisiert und können nie Teil einer Wohnung sein. | S-B1, S-H4, OG1-3 (Übergang zur Wohnküche) | `raumtyp.py:157-172` `raumtyp_flags`; `_port/models/room.py:73, 94-101` `classify_room`; `wohnungen.py:66, 90-93` | Code (+ F13) | hoch | M4: 3 Privaträume ohne Wohnung (73,06 / 59,53 / 15,91 m²) |
| U16 | Jede private Zusammenhangskomponente wird Wohnung, ohne Mindestkriterium; KÜCHE/WC/ABSTELLRAUM sind statisch WOHNUNG_PRIVAT. | S-H4, EG-1, OG1-1, OG1-2 (jeweils Einraum-Wohnung) | `nutzungsklasse.py:19-22` `_MAP`; `wohnungen.py:95-111` `bilde_wohnungen` | Fachfrage F12 + Code | mittel | M4: 8 Einraum-Wohnungen |
| U17 | „Geschäftslokal“ hat weder Kanon-Typ noch Nutzungsklasse. | S-B2 | `raumtyp.py:95-134`; `hauptengine/contracts/raum_modell.py:22-25` | Fachfrage F14 | hoch | EG `raum_12` 111,03 m² und `raum_10` 29,11 m² untypisiert |
| U18 | GANG und VORRAUM behalten `ist_fluchtweg`/`ist_communal` = True auch als WOHNUNG_PRIVAT; Gang-Anker, Gang-RZ und Flächenleuchte werden nicht gefiltert. | OG1-3 | `raumtyp.py:28-30`; `kaskade.py:150-159`; `wohnungen.py:53-55`; `provider.py:186-191`; `platzierung/flaechen_strategy.py:161-165` | Code + Fachfrage F16 | hoch (Code) | OG1 `raum_8` GANG und VORRAUM `raum_4`/`raum_5`/`raum_12`: Flags True |
| U19 | Folgeschaden: `kontur = gedeckt()` speist Türseiten; Stiegenhaus-Resträume erhalten AUSSEN-Öffnungen mit `ist_notausgang`. | S-C, S-H2 (Folge) | `tuer_zuordnung.py:106-115, 185-186`; `tuer_typisierung.py:128-132` | Code (Folge von U6/U7) | mittel | DG1 `aussenoeffnung` an `rest_2` 2590 mm, OG3 an `rest_3` 2473 mm, jeweils `ist_notausgang=True` (Näherung) |
| U20 | Die Wohnungsdarstellung zeichnet nur den Außenring ohne Füllung und setzt das Label über den höchsten Eckpunkt; das erzeugt Scheinbilder. | S-H4 (DG2, OG1-Label) | `raumerkennung_darstellung.py:709-731` `_zeichne_ausschnitt` | Code (nur Prüfbild) | hoch | DG2 `top_1` = 4 Räume, Umriss 115,23 m², kein Lift/Vorraum 15,2 im Umriss |

Pfade in der Tabelle: `src/notbeleuchtung/raumerkennung/` wird bei Package-Dateien weggelassen; `raumerkennung_darstellung.py` liegt unter `scripts/analyse/`. Die Spalte „Feedback-Punkte“ ist aus den Root-Cause-Zeilen in Abschnitt 2 (EG-1 bis DG2-8) und aus Abschnitt 3 (S-…) abgeleitet. Tabelle 5.1 übernimmt sie je Slice.

---

## 1. Pre-Read

Pfade relativ zu `src/notbeleuchtung/raumerkennung/`, wenn nicht anders angegeben. Zeilen auf HEAD 2f610cc.

### 1.1 Kontur-/Polygonbildung und Wandverfolgung

| Datei | Funktionen | Was macht der Code | Annahme hinter dem beobachteten Verhalten |
|---|---|---|---|
| `provider.py` | `ArchitekturRaumProvider.parse` Z.63-223 (Kaskade Z.69, `typisiere_geometrisch` Z.82, Türquelle Z.83-97, Außen Z.114-119, `ordne_tueren` Z.129, Durchgänge Z.135-138, `typisiere_tueren` Z.144-148, `bilde_wohnungen` Z.149, `finde_lifte` Z.180, Stiegenhaus-Modelle Z.183-189, Gang-Anker Z.190-191, Anker-Filter Z.193-197, `kreuzcheck` Z.219-222) | Verdrahtet Kaskade, Geometrie-Typisierung, Türen, Außenanalyse, Türzuordnung, Wohnungen, Ausgänge, Lifte, Stiegenhaus-Modelle. | Räume, die nach der Kaskade angehängt werden (`stiegenhaus_*`, `lift_*`), laufen nicht mehr durch die Bereinigung. Die Außenanalyse bekommt nur Wandkörper, obwohl Räume und Stempel vorliegen. Lifte entstehen nach der Wohnungsbildung. |
| `kaskade.py` | `raeume_aus_kaskade` Z.94-202 (L Z.102-103, H Z.104-109, `finde_wandkoerper` Z.110, Öffnungen + `im_planbereich` Z.110-115, Flutung Z.118-142, Typ-Rückschreiben Z.150-159, R-Stufe Z.173-180, `bereinige_kaskade` Z.188-192) | Kaskade L → H → F → R, danach Bereinigung. | Liegt ein Raum-Layer vor, sind die Zonen des Architekten die Raumpolygone. Nach der L-Stufe schneidet keine Stufe ein L-Polygon gegen Wand oder Marker. R läuft nur auf nicht belegter Fläche. |
| `raumlayer.py` | `_ROOM_LAYER` Z.32-35 (trifft „New_080 Raumdefinitionen“), `_MIN_FLAECHE_M2` Z.43-44, `_raum_polygone` Z.67-78, `raeume_aus_layer` Z.98-124 | Geschlossene LWPOLYLINE ≥ 1 m² auf Raum-Layern werden 1:1 Raumpolygone (nur Außenring). | Die Zone ist die begehbare Raumfläche. Schächte, Fensternischen, Dachschnitt-Bänder in der Zone bleiben Raum. |
| `wandkoerper.py` | `_BAUTEIL_MATERIAL` Z.36-37 (enthält SCHACHT), `_WAND_LAYER` Z.39-40, `_NEGATIV_LAYER` Z.43-47 (New_060, New_255), `finde_wandkoerper` Z.128-178 (`_hatch_pruefen` Z.134-162, `_walk` Z.164-173, Blöcke bis Tiefe < 3), `wand_union` Z.238-248, `aussenkontur` Z.251-262, `bounds_aus_wandkoerpern` Z.265-272 | Wandkörper nur aus HATCH (Material, Schmalheit oder Wand-Layer), auch aus Blöcken; Aussenkontur = größte Komponente nach Closing ±d. | Eine Wand ist durchgehend schraffiert. Fensterblöcke ohne HATCH und ungeschraffierte Wandschichten sind Lücken. FEUERFESTER_STEIN wird Wandmasse; auf New_255 fällt er ganz weg. Dachaufbau-Hatches aus `Roof_*` sind Wand. |
| `rest_komponenten.py` | `_MIN_M2` Z.42, `_SCHACHT_MAX_M2` Z.43, `_STIEGE_RX` Z.50, `_STO_LAYER_RX` Z.52, `_MARKER_NAEHE_MM` Z.54, `_marker_punkte` Z.57-86, `_typisiere` Z.89-102, `komponenten_ohne_stempel` Z.105-174 (Kontur `aussenkontur(d_mm=1000)` Z.120-124, Maske Z.132-137, Türsiegel Z.138-146, Belegt-Puffer 100 mm Z.147-152, `label` Z.156, Mindestfläche Z.158-164) | Rastert Kontur − Wand − Türen − belegte Räume, labelt freie Zellen, typisiert Komponenten ≥ 1 m². | Schächte sind stempellose Restflächen ≥ 1 m² zwischen Räumen. „Klein und türlos“ ist Schacht-Beleg. Nähe zum Treppen-Bbox-Zentrum schlägt jede andere Evidenz. d = 1000 überbrückt Öffnungen bis ~1,7 m (Kommentar; gemessen nicht bei 400-mm-Wand). |
| `stempel_flutung.py` | `_Raster` Z.63-80, `_fuelle` Z.83-111, `_Flutwerk._blockiert` Z.124-136, `label(frei)` Z.151, `_vektorisiere` Z.202-219 (nur größte Kontur Z.204-207), `flute_stempel` Z.227-302 | Rasterflutung für Stempel ohne Polygon; `_vektorisiere` wird auch von der R-Stufe genutzt. | Eine Label-Maske hat genau eine Außenkontur. Auf Rennweg ist F inaktiv (F:0). |
| `bereinigung.py` | `RAUSCH_MM2` Z.147, `LIFT_SCHACHT` Z.154, `STEMPEL_SCHUTZ` Z.160, `_rang` Z.202-207, `_entscheid` Z.266-297 (Regel 1 Z.266-269, Stempelschutz nur Regel 3 Z.280-297), `_abziehen` Z.317-330, `_schlitz` Z.332-366, `bereinige` Z.369-465, `bereinige_kaskade` Z.505-563 | Entzerrt Überlappungen; LIFT/SCHACHT gewinnt immer und wird als Loch mit 1-mm-Schlitz ausgestanzt; enthaltene Zonen werden ausgestanzt. | Ein SCHACHT-Raum überlappt den Wirtsraum bereits in der Eingabe. Zonen überlappen nicht absichtlich (DG1 AR-Zone liegt ganz in der Wohnzimmer-Zone, gleicher Rang → kein Schutz). |
| `waende.py` | `wand_segmente` Z.21-36, `raeume_aus_waenden` Z.49-62 | Wand-Layer-LINE/LWPOLYLINE werden Segmente; die Port-Polygonisierung `extract_room_faces` macht daraus untypisierte Räume. `provider.py:79` nutzt `raeume_aus_waenden` nur, wenn die Kaskade keinen Raum liefert; `wand_segmente` speist zusätzlich `verschmelze_doppelfluegel` (`provider.py:127`). | Geschlossene Wandlinien umranden Räume; laut Docstring Z.7-9 kein Gap-Healing an Türöffnungen. Auf Rennweg liefert die Kaskade Räume (Cache: 14-23 Räume je Plan; DG2 `L:7 R:5`), der Fallback läuft dort nicht und trägt zu keiner Ursache U1-U20 bei. |

### 1.2 Öffnungen (Fenster, Türen, Durchgänge)

| Datei | Funktionen | Was macht der Code | Annahme |
|---|---|---|---|
| `tueren.py` | `_DOOR_HINT` Z.36, `_AUSSENTUER` Z.43, `_ist_tuer_block` Z.50-58, `tueren_aus_dxf` Z.117, `tuer_oeffnungen` Z.160-197 (Block-Zweig Z.169-181), `aussentor_tueren` Z.209-244, `text_tueren` Z.336-353, `im_planbereich` Z.357-373 (Docstring Z.363-368) | Türöffnungen aus Tür-Blöcken und Schwenkbögen, auch in Blöcken; Filter auf Wandkörper-Bbox + 2 m. | Der INSERT-Punkt eines Türblocks liegt an der Tür, seine Rotation ist die Wandrichtung. Docstring: Inserts 300 m neben dem Haus seien ein zweiter Plan-Cluster (gemessen: die echten Türen). |
| `tuer_zuordnung.py` | `AUSSEN` Z.28, `_PROBE_MM` Z.31, `_DURCHGANG_MIN_MM`/`_KONTAKT_MM`/`_TUER_NAH_MM` Z.33-35, `_sehnen_richtung` Z.69-79, `_raum_an` Z.82-86, `ordne_tueren` Z.89-117, `durchgaenge_ohne_tuerblatt` Z.120-161, `aussen_durchgaenge` Z.169-224 | Türseiten über Probepunkte ±300 mm; synthetische Durchgänge aus Kontaktzonen; Außenöffnungen im Ring `kontur.buffer(2000) − kontur`. | Wand < 600 mm, Sehne aus Rotation. Jeder freie Teil der Kontaktzone ≥ 800 mm ist eine Öffnung. Alles nicht Gedeckte ist draußen. |
| `fenster_signatur.py` | `wandsegmente` Z.70-95, `finde_rahmenfenster` Z.113-160, `finde_fensteroeffnungen` Z.179-190 | Fenster über Rahmen-/Scheiben-Signatur in Modelspace-Wandlinien. | Nicht verdrahtet; laut Docstring Z.20-24 auf Rennweg (Wände in Blöcken) leer. |
| `_port/parsers/door_blocks.py` | `_block_base_point` Z.138-149, `_compose` Z.152-166, `_world_rotation_deg` Z.169-174, `_opening_from_block` Z.224-271, `detect_door_blocks` Z.274-329 | Port-Referenz: Tür-Lage aus in-place gezeichneter Geometrie für ArchiCAD-Weltkoordinaten-Blöcke (Docstring nennt Rennweg). | Außerhalb `_port` nirgends importiert. |

### 1.3 Schacht

| Datei | Funktionen | Was macht der Code | Annahme |
|---|---|---|---|
| `material_matching.py` | `_alias_score` Z.223-235, `_LAYER_HINWEISE` Z.238-245, `bestimme_material` Z.261-303 (nur hatch/solid Z.272-276, Alias-Boden Z.285-286), Docstring Z.14-15 | Ordnet HATCH-Signaturen Wörterbuch-Materialien zu; FEUERFESTER_STEIN → SCHACHT (Score 0,72). | Die „rahmen“-Signatur hat keinen Konsumenten; der Docstring verweist auf eine nicht existierende Marker-Spur. |
| `wissen/materialien.yaml` (unter `src/notbeleuchtung/`) | Eintrag SCHACHT Z.121-143, rahmen-Signatur Z.131-134 | SCHACHT mit Alias FEUERFESTER_STEIN und Signatur {rahmen, farbe 1, geschlossen, lineweight 13}, Quelle Rennweg; global geladen (`wissen/__init__.py` Z.42-64). | Wissen über den roten Schachtrahmen liegt vor, wird nie gelesen. |
| `legende_import.py` | Probe-Sammlung Z.120-126 | Erzeugt „rahmen“-Signaturen aus Legenden (rohe `e.dxf.color`, nicht effektive Farbe). | Import ohne Verbrauch. |
| `stempel_anker.py` | `_block_texte` Z.122-144, `_stempel_aus_insert` Z.147-195, `_stempel_aus_texten` Z.198-239 (m²-Anker Z.209-211, Wörterbuch Z.230-233), `finde_stempel` Z.242-257 | Stempel aus INSERT+ATTRIB (ROOM_NAME) und aus losen Texten mit m². | DDB/BDB/„DBA SCHACHT“ ohne m² sind kein Stempel und werden sonst nirgends gelesen. |
| `lift_erkennung.py` | `_rechteck` Z.43-68, `finde_lifte` Z.116-213 (Dedup nur gegen LIFT Z.170-173, Anlage Z.175, Ausstanzen nur aus STIEGENHAUS Z.177-210) | LIFT als gedrehtes Rechteck, ausgestanzt aus dem STIEGENHAUS, das sein Zentrum deckt; größter Rest bleibt STIEGENHAUS. | Der Lift liegt in einer größeren begehbaren Fläche; ein Rest aus reiner Schachtfuge wird nicht erkannt. |
| `_port/parsers/architecture_dxf.py` | `_SERVICE_MARKER_KIND_ALIASES` Z.2666-2671 | Port-Regex für Schacht-Texte (SCHACHT, DDB, BDB, FBDB, WDB, FDB, DBA, HKLS …). | Nicht importiert, im Lauf tot. |

### 1.4 Außenbereich

| Datei | Funktionen | Was macht der Code | Annahme |
|---|---|---|---|
| `aussenbereich.py` | Modul-Docstring Z.1-28, `_SCHLIESS_MM` Z.51-56, `_MIN_HOF_M2` Z.57, `_RAND_EPS_MM` Z.58, `_HALS_MM` Z.63, `AussenBereiche.gedeckt` Z.91-98, `aussen_indizien` Z.101-126, `_wand_geschlossen` Z.129-138, `aussenkontur_komponenten` Z.141-150, `_komponenten_aus` Z.153-157, `grundstuecksgrenze` Z.160-204, `_strassenkante` Z.207-224, `erkenne_aussenbereiche` Z.227-273 (Bezug Z.240-241, frei Z.245, Mindestfläche Z.257, Indiz Z.259, Rand Z.260-262, Hals Z.268-271) | Wandunion simplify(20), Closing ±1200 mm (quad_segs 2), Komponenten = gefüllte Außenringe; Bezug = Grundstücksgrenze, auf Rennweg None → konvexe Hülle; freie Teile mit Indiz oder Randabstand < 250 mm und Hals nahe Straßenkante sind offen. | Das Closing überbrückt Öffnungen ≤ 2·d (gilt nur für sehr dicke Wände). Ein Innenraum ist ein Loch > 250 mm vor dem Hüllrand. Kein Wissen über Räume, Stempel, Möbel. Rennweg: 0 Indizien, keine Grundstücksgrenze, kein Gehsteig-Layer. |
| `dxf_load.py` | `entity_points` Z.218-229 (DIMENSION → []), INSERT nur ein Punkt Z.227-228 | Punktlisten je Entity. | DIMENSION auf New_GRUNDSTÜCKSGRENZE liefert kein Indiz. |
| `nutzungsklasse.py` | `_MAP` Z.12-47 (BALKON/TERRASSE → AUSSEN Z.41-43, LIFT/SCHACHT → KEIN_RAUM Z.45-46), `nutzungsklasse_fuer` Z.59-61 | Statische Klasse je Typ, leerer Typ → None. | Freiflächen sind Nutzungsklasse AUSSEN (widerspricht dem Wortlaut von S-C). |
| `tuer_typisierung.py` | `_DOPPELFLUEGEL_MM` Z.56, `_FREIFLAECHE_TYPEN` Z.62-64, `_klasse` Z.90-96, `typisiere_tueren` Z.104-239 (Notausgang Z.128-132, Freiflächen-Regel Z.179-181, Hauseingang EG Z.182-186, balkontuer Z.187-189, STIEGENHAUS×PRIVAT Z.190-191, PRIVAT×PRIVAT Z.195-196, PRIVAT×ERSCHLIESSUNG Z.197-198, Text-Regel Z.205-222), Grund Z.295-305 | Tür-Rolle aus den Klassen beider Seiten, vor der Wohnungsbildung. | AUSSEN-Seite ist echter Außenraum; Sentinel AUSSEN und Nutzungsklasse AUSSEN werden gleich behandelt. |
| `ausgaenge.py`, `geschoss.py` | `leite_ausgaenge` Z.48-97, `ohne_unzulaessige_final_exits` Z.100-112; `ist_obergeschoss` Z.247-249 | final_exit nur außerhalb OG/DG. | Schützt OG/DG vor falschen final_exit; im EG würde derselbe Mechanismus Endausgänge erfinden. |
| `kreuzcheck.py`, `fluchtweg.py` | `kreuzcheck` Z.57-114, `_kandidat` Z.117-127; `_final_exit_fehlt_grund` Z.167-184 | Endpunkte an der Gebäudekante außerhalb der kontur brauchen final_exit. | Nicht gedeckt = draußen. |

### 1.5 Raumtyp

| Datei | Funktionen | Was macht der Code | Annahme |
|---|---|---|---|
| `raumtyp.py` | `_TYP_MAP` Z.27-41 (STAIRCASE/CORRIDOR/ENTRANCE_HALL → (…, True, True) Z.28-30), `_EXTRA_LABELS` Z.65-88, `loggia` → BALKON Z.81, `_EXTRA_DIRECT` Z.95-134 (`schacht` Z.113-115), `_EXTRA_OVERRIDE` Z.139-154, `raumtyp_flags` Z.157-172 | Stempeltext → (Typ, ist_fluchtweg, ist_communal); Override token-exakt, dann Port-Klassifizierer, dann Zusatzlisten. | Stempeltext ist orthografisch korrekt; Kompositum-Kopf muss exakt „küche“/„kueche“ sein. Nicht-Kanon-Begriffe bleiben bewusst None. |
| `_port/models/room.py` | `GERMAN_ROOM_TYPE_MAP` Z.42-68, `_SUFFIX_SAFE` Z.73, `classify_room` Z.78-101 | Label → RoomType über ganzes Label, Token, Kompositum-Kopf. | „wohnkche“ endet auf keinen Kopf → UNKNOWN (auch in der Substring-Version 221e866). |
| Plausibilität Fläche gegen Typ (kein Modul) | Suche in `raumerkennung/*.py` nach `raum_typ` zusammen mit Fläche/`area` und nach Vergleichen auf `flaeche_m2`: kein Treffer. Vorhandene Flächenschwellen: `raumlayer._MIN_FLAECHE_M2` Z.43 (Zone ≥ 1 m²), `raumlayer._HATCH_MAX_M2` Z.44 (nur layerlose Hatch-Räume mit Stempel, Z.238), `geometrie_typ._MIN_REALRAUM_M2` Z.34 (Deckung der Treppenmitte), `rest_komponenten._MIN_M2` Z.42 und `_SCHACHT_MAX_M2` Z.43 (Typregel), `stempel_anker._MAX_M2` Z.44 (m²-Textwert ≤ 10 000), `stempel_anker.Zuordnung.flag` Z.61-68 (Stempel gegen Polygon: `zu_gross`/`zu_klein`), `bereinigung._stempel_abweichung` Z.213, `tuer_typisierung._WINDFANG_M2` Z.59 (Rollenregel, Z.270). | Es gibt keine Prüfung, ob Fläche und Typ zusammenpassen; Typ (Stempel, Geometrie) und Fläche werden unabhängig übernommen. | Ein Typ gilt unabhängig von seiner Fläche. Fälle, die eine Warn-Kennzahl je Typ gezeigt hätte: STIEGENHAUS 0,73-1,16 m² (M1), SCHACHT 1,42 m² an der Fassade (U5), ABSTELLRAUM 9,98 m² vollständig in der Wohnzimmer-Zone (DG1-2); BAD 24,00 m² (DG2 `raum_4`) ist gestempelt und muss nicht falsch sein. Nur als Hinweis vorgeschlagen, nicht als Typisierung → F20. |
| `kuerzel_entscheid.py` | `loese_kuerzel` Z.192-219 (Stiegenkern-Beleg Z.205-207), `_BELEG_TOKEN` Z.89 | Mehrdeutige Kürzel mit Beleg; nutzt `stiege_rechtecke`. | Änderung am Treppen-Fußabdruck verschiebt Belege (Muthgasse `raum_65`). |
| `hauptengine/contracts/raum_modell.py` (unter `src/notbeleuchtung/`) | `Nutzungsklasse` Z.22-25, `BreiteQuelle` Z.35-43, `Raum.raum_typ` Z.114, `Raum.nutzungsklasse` Z.125 | Contract 1.5.0 mit fünf Nutzungsklassen. | Keine Klasse für Nichtwohn-Nutzungseinheiten; neue Klasse = 3-Owner-Änderung. |
| `platzierung/oib_gate.py` (unter `src/notbeleuchtung/`) | `verkehr_scope` Z.193-212 | Geschäftsflächen-Trigger nur für Verkehrsbauten. | Liefert nie „anwendbar“, weil Raumkategorie fehlt. |

### 1.6 Stiegenhaus

| Datei | Funktionen | Was macht der Code | Annahme |
|---|---|---|---|
| `geometrie_typ.py` | `_STAIR_BLOCK` Z.30, `_MIN_REALRAUM_M2` Z.34, `stiege_rechtecke` Z.47-63 (bbox.extents Z.54-62), `typisiere_stiegenhaus` Z.66-97 (covers(center) Z.75-80, nur untypisiert Z.82, Anhängen Z.86-96), `typisiere_geometrisch` Z.158-161 | Treppen-INSERTs als achsparallele Bbox; typisiert den Raum am Bbox-Mittelpunkt, sonst Anhängen von `stiegenhaus_i`. | Achs-Bbox = Fußabdruck; Mittelpunkt liegt im Stiegenhaus; keine Überlappungsprüfung; Zonenstempel-Blöcke („Stiegenhaus__16“, „TREPPENHAUS__14“) zählen als Treppe. |
| `stiegenhaus.py` | `_STAIR_BLOCK` Z.44, `_wcs_pts` Z.55-70, `baue_stiegenhaus_modell` Z.263-291 | Läufe, Podeste, Anker je STIEGENHAUS-Raum. | Jeder STIEGENHAUS-Raum ist ein echtes Stiegenhaus; auch Ringe, DBA-Schacht, Bbox-Rechteck bekommen Modelle und Anker. |
| `objekt_stiege.py` | Docstring Z.1-46, Konstanten Z.69-83 (`_MAX_STUFEN` Z.78, `_CONF_DECKEL` Z.82), `StiegenKandidat` Z.87, `finde_stiegen` Z.197-239 | Treppenlauf-Matcher aus parallelen Stufenlinien (Teilung 250-350 mm, mindestens 5 Stufen), ohne Raum und ohne Block-/Layernamen, über `layer_features._sammle`; nutzt `stiegenhaus._gruppiere_laeufe`/`_lauf_aus_gruppe`. Nicht in `provider.py` verdrahtet; Aufrufer nur `scripts/analyse/layer_merkmale.py:51, 158` und `tests/raumerkennung/test_objekt_stiege.py`. | Jeder Kandidat braucht menschliche Bestätigung (Confidence auf 0,84 gedeckelt; Docstring: Fahrradständer Mollgasse nicht unterscheidbar). Gemessen DG2 (B.9): 0 Kandidaten, obwohl `Stair_1`/`Stair_2` Stufenlinien tragen; Ursache nicht untersucht. Für U1 deshalb nicht als Quelle nutzbar (siehe U1-Fix). |
| `zirkulation.py` | `WEG_PREFIX` Z.27, `zirkulation_aus_dxf` Z.61-96 | Fluchtweg-Segmente und Graph nur aus Layern `09-WEG*` (`provider.py:99`); `provider.py:167-175` hängt explizite Linien und `fluchtwege(…)` an; die Segmente speisen `anker_fuer_gang` (`provider.py:191`). | Gezeichnete Fluchtweg-Linien liegen auf `09-WEG*`. Rennweg: Rohbyte-Suche „09-WEG“ in allen 7 DXF 0 Treffer (B.10), die Zirkulation kommt dort nur aus `fluchtwege`; für U1-U20 ohne eigenen Befund. |
| `gang_anker.py` | `anker_fuer_gang` Z.102-112 | Anker entlang der Gangachse. | Keine Prüfung von Nutzungsklasse oder Flags. |

### 1.7 Wohnungsbildung

| Datei | Funktionen | Was macht der Code | Annahme |
|---|---|---|---|
| `wohnungen.py` | `_klasse` Z.28-29, `_verfeinere_gang_privat` Z.32-55 (fremd Z.48-50, privat_ok Z.51-52, Zuweisung Z.53-55), `bilde_wohnungen` Z.58-112 (Default Z.61-63, privat Z.66, Rollen-Kippen Z.71-80, Union Z.90-93, top_n Z.95-111) | Wohnungen = Zusammenhangskomponenten privater Räume über zimmertuer/None-Kanten; GANG/VORRAUM vorher privat oder Erschließung. | Eine Tür ins Stiegenhaus macht einen Flur zur Erschließung. Untypisierte Räume verbinden nicht. Jede private Komponente ist eine Wohnung. Die Türkanten sind echte Türen. |
| `tests/raumerkennung/test_wohnungen.py` | `test_zwei_wohnungen_getrennt` Z.13-30, `test_wohnungs_flur_wird_privat` Z.33-47, `test_flur_mit_stiegenhaustuer_bleibt_erschliessung` Z.50-57 | Unit-Tests. | Z.50-57 schreibt die Regel fest, die OG1 zerlegt (eingeführt mit 9a5de6f, als Owner-Fallback in `docs/ENIS_STAND_1_5_0.md` Z.260-261 nur die private Richtung belegt). |
| `platzierung/flaechen_strategy.py`, `platzierung/gang_strategy.py`, `platzierung/fachpraxis.py` (unter `src/notbeleuchtung/`) | `flaechen_strategy` Z.157-167; `gang_strategy` Z.94-98; `fachpraxis._TUERLEUCHTE_KEIN_COMMUNAL` Z.73-76, `aussen_tuer_rz` Z.387-411 | Leuchten-Unterdrückung für WOHNUNG_PRIVAT nur ohne Fluchtweg-/communal-Flag; Gang-RZ ohne Klassenfilter; RZ an communal→AUSSEN ohne Geschossbezug. | Konsumieren Klassen und Flags der Erkennung ungeprüft. |

### 1.8 Output / Clipping

| Datei | Funktionen | Was macht der Code | Annahme |
|---|---|---|---|
| `scripts/analyse/raumerkennung_darstellung.py` | `_polygon` Z.218-222, `_ausschnitte` Z.277-306 (`_bounds` Z.288-293, Rand 6 %), `_breite_px` Z.309-315, `_hintergrund` Z.318-347, `_erkennen` Z.364-446 (polys Z.397-402, Aufruf Z.429, Cache Z.431-445), `_auswertung` Z.467-494, `_zeichne_ausschnitt` Z.605-783 (sichtbar Z.629-630, Wohnungsumriss Z.709-731), `_TYP_KAT` Z.123-136 | Bildausschnitt aus Raum-Bounds, Außenflächen und Räume als Overlay, Wohnungsumriss als Außenring der gepufferten Union. | Das Gebäude liegt vollständig in den Raumpolygonen; ein Außenring ohne Füllung ist eindeutig lesbar. |
| `scripts/analyse/gesamtdarstellung.py` | Kennzahlen Z.433 (tuer_typen), Z.443 (wohnungen), Umriss Z.311-319 | Kennzahlen aller Pläne. | Verhältnis Wohnungseingang/Wohnung misst die Wohnungsbildung, unabhängig von der Türquelle. |
| `scripts/plan_pruefen.py` | `_rotation` Z.87-133, `_bereinigung_felder` Z.1358-1377, Warnung Z.1797-1800 | Prüfstrecke trennt Fläche roh und bereinigt. | Rotation über `entity_points` (INSERT = 1 Punkt) sieht die Wall_N-Blöcke nicht („keine dominante Kantenrichtung“). |

---

## 2. Diagnose je Feedback-Punkt

Aufbau je Punkt: Zitat · Output · Architektplan · Root Cause · betroffen · Fix · Blast Radius · Code/Fachfrage · Prüfstatus. Mechanismus, Pseudocode und Blast Radius jeder Ursache stehen einmal in **2.6** (U1-U20); an den Punkten wird darauf verwiesen. Koordinaten in mm (Modelspace, Faktor 1,0).

### 2.1 EG

#### EG-1 - Küche 9,3 m²

> „EG: Küche 9.3m2 sind Schächte die nicht erkannt wurden, und nicht eingegrenzt worden sind.“

- **Output:** EG `raum_11` KÜCHE 9,27 m², Stempel „v.Küche“ 9,27 m², 4 Ecken, Quelle L; Polygon deckungsgleich mit der Zone auf „New_080 Raumdefinitionen“ (symmetrische Differenz 0,0000 m²). Bildet allein Wohnung `top_2`. Im EG gibt es keinen SCHACHT-Raum.
- **Architektplan:** „v.Küche“ ist ein echter Raum (Fliesen, Zargentür 80/2,00 zum TREPPENHAUS, Schiebetür 86/2,10 zu „Geschäftslokal 1“). Die Schächte liegen nur am Ostende in einem Dreieck hinter Schachtwänden: `Wall_90`/`Wall_91` (Layer „New_010 Aussenwände“, WAERMEDAEMMUNG 98-100 mm) und `Wall_64` (GIPSKARTON_EI0, 228 mm). Darin rote geschlossene LWPOLYLINE (ACI 1, Strichstärke 13) auf „New_255 Plangrafiken_Pen_No__21“ mit 0,336 und 0,125 m², kleine Rahmen auf „New_HKLS1_Pen_No__21“ (0,045/0,014 m²) und FEUERFESTER_STEIN-Keile. Beschriftung in der Küche: MTEXT „L3 DDB/BDB 65/103,9“ bei (12555047, 356213768) und „L5 DDB/BDB 25/50“ bei (12554804, 356213290), rote Hinweislinien enden in den Schachtzellen. Die Zone reicht bis an die Außenwandlinie und schließt die Zellen ein; die Nachbarzone MÜLLRAUM spart dieselben Schächte per Kerbe aus.
- **Messung:** Zone minus Wandunion = Hauptzelle 8,210 m² + Schachtzellen 0,400 und 0,259 m² (Zellen B.14); Wandkörper im Polygon 0,400 m² (davon FEUERFESTER_STEIN 0,059 m²). M3: rote Schachtfläche im Raum 0,458 m².
- **Root Cause:** **U3**: Zone 1:1 übernommen (`raumlayer.py:98-124` `raeume_aus_layer`), R-Stufe sperrt belegte Zonen und verwirft < 1 m² (`kaskade.py:173-175`; `rest_komponenten.py:42, 147-164` `komponenten_ohne_stempel`), kein Schacht-Detektor. Folge: Einraum-Wohnung aus **U16** (`nutzungsklasse.py:19-22` `_MAP`; `wohnungen.py:95-111` `bilde_wohnungen`).
- **Betroffen:** EG `raum_11`; mit gleicher Ursache EG `raum_12` (untypisiert, 9 Marker-Zellen, 1,296 m²) und ein 0,008-m²-Splitter in `raum_13`.
- **Fix / Blast Radius:** → 2.6 U3, U16.
- **Art:** Code (U3) + Fachfrage F3 (Umfang der Ausgrenzung). **Rückfrage an Leonis (F17a):** War die ganze Küche als Schacht gemeint? Geometrisch belegt sind nur die Randzellen.
- **Prüfstatus:** korrigiert. Die Schachtwand ist `Wall_90`/`Wall_91`/`Wall_64`, nicht `Wall_32` auf „New_015 Innenwände“ (Cluster-Angabe). Das Zitat „Küche sind Schächte“ ist am Plan nicht belegt.

### 2.2 1OG (Datei OG1)

#### OG1-1 - Abstellraum 4,5 m²

> „1OG: Abstellraum 4.5m2 die Schächte wurden nicht richtig vom Abstellraum abgegrenzt“

- **Output:** OG1 `raum_11` ABSTELLRAUM 4,520 m², Stempel „AR“ 4,52, 5 Ecken, deckungsgleich mit der Zone. Einraum-Wohnung `top_2`. Kein SCHACHT im OG1.
- **Architektplan:** Rote Rahmen auf „New_HKLS1_Pen_No__21“ (0,336 / 0,125 / 0,045 / 0,014 m²), FEUERFESTER_STEIN-Keile auf „New_HKLS1_Pen_No__39“, MTEXT „L3 DDB/BDB 65/103,9“ und „L5 DDB/BDB 25/50“ im AR (alle Modelspace, keine Blöcke). Schachtwände als Wall-Blöcke (`Wall_75`/`Wall_76` laut Cluster, nicht gegengeprüft).
- **Messung:** Hauptzelle 3,887 m², Schachtzellen 0,236 m² (Rahmen-Schnitt 0,236) und 0,152 m² (Rahmen-Schnitt 0,042), Wandkörper im Polygon 0,245 m². M3 rote Fläche 0,322 m². Fläche nach Ausgrenzen: 4,132 m² nur Zellen (−8,6 %), 3,887 m² ohne Zellen und Schachtwand (−14,0 %).
- **Root Cause:** **U3** (`raumlayer.py:98-124` `raeume_aus_layer`; `rest_komponenten.py:42, 147-164`). Die Einraum-Wohnung entsteht aus **U14** (Vorraum wird Erschließung, `wohnungen.py:32-55` `_verfeinere_gang_privat`, `:71-80` Rollen-Kippen) und **U16** (`wohnungen.py:95-111`).
- **Betroffen:** OG1 `raum_11`; gleiche Ursache in `raum_12` VORRAUM 10,943 m² (Zellen 0,419/0,065) und `raum_2`, `raum_9`, `raum_10` (OG1 gesamt 14 Marker-Zellen in 6 Räumen, 1,698 m², B.14).
- **Fix / Blast Radius:** → 2.6 U3, U14, U16.
- **Art:** Code + Fachfrage F3 (Hohlraum oder bis Schachtwand; Stempelbezug).
- **Prüfstatus:** bestätigt (beide Linsen; Wall-Nummern nicht verifiziert).

#### OG1-2 - WC 3,5 m²

> „1OG: WC 3.5 m2 hier wurden ebenfalls die Schächte nich richtig ausgegrenzt“

- **Output:** OG1 `raum_13` WC 3,502 m², Stempel 3,50, 7 Ecken, deckungsgleich mit der Zone. Einraum-Wohnung `top_3`.
- **Architektplan:** Zickzack-Schachtwände `Wall_78`/`Wall_89`/`Wall_90` („New_010 Aussenwände“, WAERMEDAEMMUNG 98-100 mm), rote Rahmen auf „New_HKLS1_Pen_No__21“ (0,280 / 0,062 / 0,041 / 0,012 m²), MTEXT „L1 DDB/BDB 25/25“ im WC, „L2 DDB/BDB 40/70“ und „S5 DDB/BDB 65/101.7“ im Vorraum.
- **Messung:** Hauptzelle 3,002 m² plus fünf Kleinzellen 0,104 / 0,063 / 0,038 / 0,032 / 0,027 m²; Wand im Polygon 0,235 m². Nur zwei Zellen haben Rahmen-Schnitt (0,0381 und 0,0272 = 0,065 m²), zwei berühren einen Rahmen nur (0,063/0,032), eine liegt 100 mm entfernt (0,104). Flächenstaffel: 3,437 m² (nur Zellen mit Rahmen, −1,9 %), 3,341 m² (mit berührenden, −4,6 %), 3,002 m² (nur Hauptzelle, −14,3 %). M3 rote Fläche 0,079 m².
- **Root Cause:** **U3** (`raumlayer.py:98-124`; `rest_komponenten.py:42, 147-164`); Einraum-Wohnung aus **U14** (`wohnungen.py:32-55, 71-80`) und **U16** (`wohnungen.py:95-111`).
- **Betroffen:** OG1 `raum_13`, dazu `raum_12` VORRAUM.
- **Fix / Blast Radius:** → 2.6 U3 (Beleg über Schnittfläche, nicht über Berührung), U14, U16.
- **Art:** Code + Fachfrage F3 (4): gelten berührende oder rahmenlose Kleinzellen als Schacht?
- **Prüfstatus:** korrigiert. Cluster nannte „vier Zellen mit Rahmen = 0,161 m²“; gemessen zwei mit 0,065 m² (Test „Schnitt > 0“ mit Fließkomma-Rauschen).

#### OG1-3 - Gang 6,5 m²

> „1OG: Gang 6.5“ (im Feedback ohne weitere Beschreibung)

- **Output:** OG1 `raum_8` GANG 6,48 m² = Stempel „Gang“ 6,48, Quelle L, 4 Ecken, 1200 × 5402 mm, WOHNUNG_PRIVAT, `top_1`, `ist_fluchtweg` und `ist_communal` = True, kein Außenschnitt. Verbindungen im Modell ausschließlich synthetische Durchgänge ohne Türblatt: `durchgang_4` zu Zimmer 10,6 (1200 mm), `durchgang_14` zu Bad 11,8 (4830 mm), `durchgang_16` zu Zimmer 17,0 (1009 mm), `durchgang_17` zur untypisierten Wohnküche (1450 mm, ohne Rolle).
- **Architektplan:** Zone „Gang 6,48 m²“, Parkett. Links Wand zu Bad 11,8 mit Zargentür 80/2,20 (`Zargentür_1_Fl 10[4]` in `Wall_11`), oben Öffnung 1,20/2,20 (`Rectangular Door Opening 27[12]`) zu Zimmer 10,59, unten wandlos offen zur Wohnküche, unten links Zargentür 80/2,20 zu Zimmer 17,0 (`Zargentür_1_Fl 10[3]`). Am unteren Ende an der Stiegenhauswand zwei rot umrandete Schächte „H1 DDB/BDB 25/90“ und „WP DDB/BDB 25/40“ (Einfügepunkte in der Wohnküchen-Zone, 554 bzw. 1313 mm vom Gang).
- **Root Cause:** Geometrie, Fläche und Typ entsprechen der Zone. Objektiv messbare Mängel: **U18** (Flags widersprechen WOHNUNG_PRIVAT; `raumtyp.py:28-30`, `kaskade.py:150-159`, Gang-Anker `provider.py:190-191`; Gang-Anker, Gang-RZ und Flächenleuchte werden nicht unterdrückt), **U12**/**U13** (echte Türen fehlen: `tueren.py:169-181` `tuer_oeffnungen`, `tueren.py:360-373` `im_planbereich`; Bad-Verbindung 4830 mm breit: `tuer_zuordnung.py:133-160` `durchgaenge_ohne_tuerblatt`), **U15** (Wohnküche ohne Wohnung teilt die Wohnung am offenen Übergang; `raumtyp.py:157-172` `raumtyp_flags`, `wohnungen.py:66, 90-93`), **U3** (Schächte am Gangende; `raumlayer.py:98-124`).
- **Betroffen:** OG1 `raum_8`; Flags-Widerspruch auch an VORRAUM `raum_4`, `raum_5`, `raum_12`.
- **Fix / Blast Radius:** → 2.6 U18, U12, U13, U15, U3.
- **Art:** Rückfrage an Leonis (F16): (A) Gang soll kein Fluchtweg sein, (B) Wohnungszugehörigkeit am Übergang, (C) Ausdehnung bzw. Schächte H1/WP ausgrenzen, (D) als korrekt gemeint. Normfrage an Enis (F16): Ist ein Wohnungsflur Fluchtweg?
- **Prüfstatus:** bestätigt als Rückfrage; Linse 2 hat den Flag-Anteil zu einem Code-Befund verschärft (U18).

#### OG1-4 - Zimmer 16,9 m²

> „1OG: Zimmer 16.9m2 man muss aufpassen und genau analysieren bis wo die Wände gehen, es wurde die Wand auf der Seite wo sich der Balkon befindet schon früher abgegrenzt, und deshalb wurde die Wand nicht richitg erkannt auf der Balkonseite, wahrscheinlich wegen den Fenster hier ist es dann Wichtig um die Fenster herum einzugrenzen und den Raum wirklich genau zu analysieren das jede Wand vom Raum erkannt wird.“

- **Output:** OG1 `raum_3` ZIMMER 16,86 m² = Stempel, 4 Ecken, Quelle L. 16,05 m² (95,2 %) liegen im offenen Außenteil `offen[0]` 64,13 m² (Randabstand 0), der auch `raum_1` ZIMMER 16,11 m² (Schnitt 14,41 m²), `raum_2` ZIMMER 10,59 m² (Schnitt 8,48 m²) und `raum_15` BALKON 7,50 m² überdeckt (achteckige Form = Closing mit `quad_segs=2`).
- **Architektplan:** Balkonseitige Wand `Wall_5` („New_010 Aussenwände“) mit Umrisslinien bei 0 / 480 / 680 mm. Schraffiert ist nur die äußere 200-mm-Schicht (6× HATCH DÄMMSTOFF__POLYSTYROL_EPS); die innere 480-mm-Schicht ist ungeschraffiert (Text „PH 85“). Fenster `2-Flügelfenster 1+1[8]`/`[9]` 1,30/1,70 m mit je 2 EPS-Hatches, Rahmen bei 369-459 mm. Balkontüren `2-Flügelfenster 1+1 25[10]`/`[11]` in `Wall_6`, 2,40/2,55 m, ohne HATCH, mit Flügelbogen. Die Zonenkante liegt an der inneren Linie (0-1 mm zur `Wall_5`-Umrisslinie).
- **Messung:** Wandunion an Kante 0: 0-450 mm über die ganze Kantenlänge frei; bei +550 mm zwei Lücken je 1300 mm. Die geschlossene Wand (`wand_zu`) ist an den Fenstern und Balkontüren frei (Brücke in der Mitte 0 mm). Balkontür `25[10]` liegt zu 5 % in der Wandunion. Längste Eintrittskreuzung 6283 mm, 916 mm neben Fenster `[9]`. Gegenprobe mit Fensterblock-Rechtecken als Barriere (Blöcke mit FENSTER/WINDOW in Name oder Layer als zusätzliche Wandkörper, plus Loch-Test; B.11): Zimmer-Schnitt OG1 38,94 → 0 m² (`raum_1`/`raum_2`/`raum_3`); `raum_15` BALKON 7,50 → 6,65 m².
- **Root Cause:** Außenfläche im Zimmer = **U6** (`wandkoerper.py:164-173` sammelt nur HATCH; `aussenbereich.py:129-138` `_wand_geschlossen` versiegelt dickenabhängig: dünne Schraffur 200 mm mit 1300-mm-Fenstern, Balkontüren ≥ 2,4 m nie versiegelt) plus **U8** (`aussenbereich.py:227-271` `erkenne_aussenbereiche` ohne Räume, Aufruf `provider.py:114`: kein Innen-Veto). Die Raumkante selbst ist Zonengeometrie (**U9**, `raumlayer.py:98-124`; Fachfrage Wandschicht/Fensternische); die Wandmaske verändert sie nicht.
- **Betroffen:** OG1 `raum_1`, `raum_2`, `raum_3`, `raum_15`.
- **Fix / Blast Radius:** → 2.6 U6, U8, U9. Flächen-Überschlag Option C (Nischen bis Rahmenlinie): 16,9 → ca. 17,8 m² (+5,7 %), bei voller Wanddicke 680 mm ca. 18,6 m².
- **Art:** Code (U6, U8) + Fachfragen F5 (Nische, Wandschicht) und F8 (Brücke). **Rückfrage an Leonis (F17b):** Meint „schon früher abgegrenzt“ die ungeschraffierte 480-mm-Schicht vor der Dämmung oder die blaue Außenfläche?
- **Prüfstatus:** korrigiert. Das Leck entsteht auch an schraffierten Fenstern (`[8]`/`[9]`), weil `Wall_5` nur 200 mm schraffiert ist; „Fenster ohne HATCH“ ist nicht die alleinige Ursache. S-H2-Teil „Wandmaske schneidet die Raumkante ab“ ist widerlegt (Zone L unverändert).

### 2.3 2OG (Datei OG2)

#### OG2-1 - Zimmer 14,5 und 10,7 m²

> „2OG: Zimmer 14.5m2 und Zimmer 10.7m2 wurden richtig erkannt, aber wurde teilweise als Außenbereich markiert hier muss man wirklich vorsichtig sein und das der Außenbereich um den Balkon/Terasse herum erkannt wird und nicht in dem Gebäude reinragt.“

- **Output:** Ein offener Teil 51,47 m² (Randabstand 0, maximale Tiefe 3572 mm) schneidet `raum_8` ZIMMER 14,51 m² mit 12,92 m² (89,0 %), `raum_7` ZIMMER 10,65 m² mit 8,47 m² (79,5 %), `raum_13` TERRASSE mit 15,17 m² und `raum_14` TERRASSE mit 7,50 m².
- **Architektplan:** Nordfassade `Wall_16` mit `2-Flügelfenster 1+1 25[9]`/`[10]` (Layer „New_Archicad Windows“, keine HATCH), beidseits Wandkörper STAHLBETON ~200 mm + WAERMEDAEMMUNG ~200 mm. In den Zimmern Doppelbett 01 25[37], Schrank variabel 25[39]/[40]; Raumstempel „Zimmer“, „Terrasse“.
- **Messung:** Eintrittskreuzung 187 mm neben `25[9]` (Brücke in der Mitte 0). Ohne Lückenzonen verbleiben 27,91 m², davon 21,7 m² Raum = nur die Terrassen. Gegenprobe Fensterbarriere (B.11): Zimmer-Schnitt 21,39 → 0 m², Terrassen bleiben (14,56 / 7,19 m²).
- **Root Cause:** **U6** (Fenster ohne Wandkörper, `wandkoerper.py:164-173`; Closing versiegelt nicht, `aussenbereich.py:129-138`) plus **U8** (kein Innen-Veto, `aussenbereich.py:227-271`, `provider.py:114`). Freiflächen unter blauer Schraffur sind die Begriffsfrage F6.
- **Betroffen:** OG2 `raum_7`, `raum_8`; Freiflächen `raum_13`, `raum_14`.
- **Fix / Blast Radius:** → 2.6 U6, U8.
- **Art:** Code + Fachfrage F6 (sind Terrasse/Balkon selbst Außenbereich, wo beginnt „um den Balkon herum“?).
- **Prüfstatus:** bestätigt. Präzisierung: Heute wird eine Freifläche nur blau, wenn sie in der konvexen Hülle der Wandkörper liegt (eingezogene Terrassen OG2/DG2 ja, auskragende Balkone DG1/OG3 `raum_9` mit 0,0 m² in der Hülle nie). Die im Cluster genannten Lückenmaße (3265/2742 mm) sind methodenabhängig.

### 2.4 1DG (Datei DG1)

#### DG1-1 - Wohnzimmer 73,9 m², Schächte

> „1DG: Hier wurden im Wohnzimmer 73.9m2 die Schächte übersehen und nicht ausgegrenzt“

- **Output:** DG1 `raum_1` WOHNZIMMER 73,95 m² ohne Löcher; Rohpolygon = Zone mit 5 Ecken und 83,93 m² (= Stempel), nach ENTHALTENSEIN gegen `raum_11` (9,98 m²) 73,95 m². Im DG1 gibt es nur `rest_1` SCHACHT 1,25 m² am DBA-Schacht; keine LIFT_SCHACHT-Buchung.
- **Architektplan:** In der Wohnzimmer-Zone rote geschlossene Konturen auf „New_HKLS1_Pen_No__21“ mit FEUERFESTER_STEIN auf „New_HKLS1_Pen_No__39“, beschriftet mit MTEXT auf „New_255 Plangrafiken_Pen_No__1“: „H1 DDB/BDB 25/90“ (Kontur 0,225 m²), „WP DDB/BDB 25/40“ (0,100 m²), „S3 BDB 20/20“ an der Fassade (0,040 m²), „L3 DDB/BDB 65/103,9“ (0,336 m², 62 % in der Zone), „L5 DDB/BDB 25/50“ (0,125 m², 69 % Wohnzimmer / 31 % AR). Alles Modelspace, 0 Treffer in Blöcken. Die Zonen auf New_080 haben keine Aussparungen (DG1: 11 geschlossene Polylinien, kleinste 1,725 m²).
- **Messung:** Raster der R-Stufe: H1 92 Zellen, 78 durch die Zone belegt, 0 frei; L3 34 freie Zellen als 0,118-m²-Komponente verworfen. 16 FEUERFESTER_STEIN-Hatches sind Wandkörper mit Material SCHACHT. M3 rote Fläche im Raum 0,653 m².
- **Root Cause:** **U3**: Zone ohne Aussparung übernommen (`raumlayer.py:98-124` `raeume_aus_layer`); Schachtzellen gesperrt bzw. < 1 m² verworfen (`rest_komponenten.py:42, 147-164`); FEUERFESTER_STEIN wird Wandkörper statt Schacht-Beleg (`wandkoerper.py:36-37, 142-155`).
- **Betroffen:** DG1 `raum_1`; gleiche Ursache `raum_11` AR (siehe DG1-2), `raum_10` BAD, `raum_4` GANG, `raum_2`/`raum_3` ZIMMER, `rest_2`.
- **Fix / Blast Radius:** → 2.6 U3.
- **Art:** Code + Fachfrage F3.
- **Prüfstatus:** bestätigt (beide Linsen).

#### DG1-2 - Abstellraum 10 m²

> „1DG: genauso im Abstellraum 10m2.“

- **Output:** DG1 `raum_11` ABSTELLRAUM 9,98 m², dreieckig, liegt vollständig in der Wohnzimmer-Zone.
- **Architektplan:** Schacht L5 (und Spitze L3) an der Dreieckspitze zwischen Wohnküche und AR; die Beschriftungen stehen in der Küche (`raum_1`).
- **Messung:** rote Fläche im AR 0,045 m² (Konturen 0,014 / 0,125 / 0,336 m² mit Schnitt 0,011 / 0,038 / 0,006 m²). Die textbasierte M3-Zählung übersieht den Raum, weil kein Einfügepunkt darin liegt; die Flächenzählung erfasst ihn.
- **Root Cause:** **U3** (wie DG1-1: `raumlayer.py:98-124`; `rest_komponenten.py:42, 147-164`).
- **Betroffen:** DG1 `raum_11`.
- **Fix / Blast Radius:** → 2.6 U3.
- **Art:** Code + Fachfrage F3.
- **Prüfstatus:** bestätigt; Messdefinition M3 korrigiert (Fläche statt Text).

#### DG1-3 - Wohnzimmer-Teil als Außenbereich, nicht erkannt, abgeschnitten

> „1DG: Ein Teil des Wohnzimmers wurd als Außenbereich markiert und wurde nicht erkannt, und wurde ein Teil des nicht erkannten Wohnzimmer wurde beim Output weggeschnitten.“

- **Output:** Offener Außenteil `offen[2]` 103,76 m² (Bbox 12540269/356208307 - 12555648/356219700), Schnitt mit `raum_1` WOHNZIMMER 70,83 m², `raum_7` „TV Raum“ (untypisiert) 12,85 m², `raum_8` VORRAUM 1,58 m². Links der Wohnzimmer-Zone eine freie Fläche ohne Raum: 16,94 m² (Gebäudekomponente − Wandunion − Räume, Bbox 12539939/356212945 - 12544610/356219188) bzw. 16,76 m² (Hülle − 300 mm − Wand − Räume); davon 16,09 bzw. 15,97 m² im offenen Teil. Wohnzimmer rote Zahl 73,95 gegen Stempel 83,93. `uebersicht.png` beginnt links bei x = 12540425, die Wandkörper bei x = 12539089.
- **Architektplan:** Offener Wohnbereich mit 2D_sofa_18585[1]/[56], 2D_sofa_38585[42], Flat Panel TV 27[61], Schrank variabel 25[53]/[60], 12× Chair 02, Texte „TV“, „WA9“, „S9 BDB 25/25“, „DDB 25/25“, „S2 DDB/BDB 25/90“ und „NACHBARGEBÄUDE RENNWEG 13“ an der Feuermauer. Keine Zone, kein Stempel. Zwischen TV-Bereich und Wohnzimmer keine Wand, nur die Zonenlinie (LWPOLYLINE „New_080 Raumdefinitionen“, true_color 16754856). Südfassade `Wall_28` (STAHLBETON 200 + WAERMEDAEMMUNG 200 mm) mit `2-Flügelfenster 1+1[4..8]` (Lücke 1320-1396 mm).
- **Messung:** Das offene Teil liegt vollständig in der Gebäudekomponente und in einem Loch der geschlossenen Wand (`ausserhalb_komponenten` 0,0 m²). Randabstand zum Bezug (konvexe Hülle, 238,6 m²) 193 mm; Hals zur Kante 173 mm (beide B.13); 0 Außen-Indizien; keine Grundstücksgrenze. Auf der kürzesten Verbindung Loch → Hüllrand am Fenster `[4]` enthält die rohe Wandunion 0 mm, die geschlossene Wand 11 mm. R-Kontur `aussenkontur(d=1000)` 73,5 m² (6 Teile, größtes ohne Loch) gegen Komponente d = 1200 mit 196,8 m²; TV-Punkt (12541300, 356215500) liegt in keiner Kontur, keiner Zone, keinem Raum. Außerhalb des Bildes: 1,77 m² Wand und 0,49 m² der freien Fläche.
- **Root Cause (drei getrennte Mechanismen):**
  1. Außen: **U7** (`aussenbereich.py:58, 260-262`: Loch 193 mm vor dem Hüllrand gilt über die 250-mm-Toleranz als offen) plus **U8** (`aussenbereich.py:227-271`, `provider.py:114`: kein Veto trotz Stempel und Möbeln).
  2. Nicht erkannt: keine Zone (Architektendaten) und **U10** (`rest_komponenten.py:122` mit `wandkoerper.py:251-262` `aussenkontur`: R-Stufe rechnet nur in der zerfallenen Kontur d = 1000).
  3. Weggeschnitten: **U11** (`raumerkennung_darstellung.py:277-306` `_ausschnitte`, `:402` Polygone nur aus Räumen). Die Wirkung ist klein; der Hauptteil ist im Bild sichtbar.
  - Die rote Zahl kommt aus Bereinigung Regel 3 ENTHALTENSEIN (`bereinigung.py:280-297`, gleicher Rang, kein Stempelschutz).
- **Betroffen:** DG1 `raum_1`, `raum_7`, `raum_8`, zonenloser TV-Bereich.
- **Fix / Blast Radius:** → 2.6 U7, U8, U10, U11.
- **Art:** Code (U7, U10, U11) + Fachfragen F7 (indizloser Lichthof) und F9 (zonenlose Fläche: eigener Raum, zuschlagen, Typ erben; AR in Wohnzimmer-Zone als Wiedervorlage des Stempelschutz-Entscheids).
- **Prüfstatus:** bestätigt, mit zwei Korrekturen: (a) Die 193 mm sind der Abstand zum Hüllrand, keine Brückendicke; das Teil ist nicht mit dem Freien verbunden. (b) Der Bildausschnitt schneidet nur 0,49 m² freie Fläche ab (Cluster-Gewichtung zu hoch).

#### DG1-4 - fast ganzes Geschoss als Außenbereich

> „1DG: Hier muss man ebenfalls aufpassen was als Außenbereich erkannt wird, weil teilweise der ganze Geschoß als Außenbereich markiert wurde. Außenbereich sind alle Sachen die sich außerhalb des bewohnten Bereiches befinden, also kann im Wohnzimmer, Schlafzimmer/Zimmer, Bad, WC, AR , VR, Stiegenhäußer , und Terasse/Balkon/loggia nicht zu Außenbereich zählen.“

- **Output:** Offen 143,83 m² in drei Teilen: 19,86 m² (`raum_2` ZIMMER 12,63, `raum_10` BAD 5,55), 20,21 m² (`raum_3` ZIMMER 15,05, `raum_6` BAD 4,05), 103,76 m² (siehe DG1-3). Innenraum-Schnitt 122,55 m² in 7 Räumen, alle > 1 m².
- **Architektplan:** Nordfassade mit `2-Flügelfenster 1+1 25[1]`/`[2]`/`[3]` in `Wall_6` ohne HATCH; `25[2]` ist eine Fenstertür (Flügelbogen im Block). Beidseits STAHLBETON ~200 + WAERMEDAEMMUNG ~200 mm. In den Räumen Doppelbett 01, Schrank variabel, Badewanne, Shower Kit, Waschbecken, WC-Symbol.
- **Messung:** Die Nordteile liegen vollständig außerhalb der Komponenten (Randabstand 0); Eintrittskreuzungen 332 mm neben `25[2]` und 335 mm neben `25[3]`. Gegenprobe ohne Lückenzonen: 1,17 m² bzw. kein Rest. Loch-Test allein: DG1 offen 143,83 → 40,07 m² (verbleiben nur die Nordzimmer; B.1).
- **Root Cause:** Nordzimmer **U6** (`wandkoerper.py:164-173`; `aussenbereich.py:129-138`); Wohnzimmer **U7** (`aussenbereich.py:58, 260-262`); Regelverletzung **U8** (Fachregel S-C gegen `aussenbereich.py:227-271`; Aufruf ohne Räume `provider.py:114`).
- **Betroffen:** DG1 `raum_1`, `raum_2`, `raum_3`, `raum_6`, `raum_7`, `raum_8`, `raum_10`.
- **Fix / Blast Radius:** → 2.6 U6, U7, U8.
- **Art:** Code + Fachfrage F6 (welche Zonen „innen“, Freiflächen).
- **Prüfstatus:** bestätigt. Präzisierung: Die Lückenmaße des Clusters (1795/5128/3387 mm) sind methodenabhängig (Gegenmessung entlang der Wandachse 1710/8221/5508 mm); qualitativ liegen alle über der Versiegelungsgrenze.

### 2.5 2DG (Datei DG2)

#### DG2-1 - Bad 24 m², Fensterseite

> „2DG: Bad 24m2 wurde die Wandseite wo sich die Fenster befinden nicht genau erkannt, hier ist es wichtig die Innenraumerkennung, von den Fenstern abzugrenzen, also muss entlang der Wand erkannt, werden und um die Fenster herum bis die Wand weitergeht.“

- **Output:** DG2 `raum_4` BAD 24,00 m² = Stempel, 8 Ecken, Quelle L. Offener Teil `offen[0]` 32,47 m² (Randabstand 0, Kontakt mit dem Hüllrand 4,84 m² in einem Stück, Bbox 12539297/356206392 - 12557441/356215143) schneidet das Bad mit 2,85 m² (davon 1,28 m² außerhalb einer 5-m-Gebäudemaske).
- **Architektplan:** Straßenseite ist Dachschräge `Roof_2` („New_045 Dachkonstruktionen“). Von der Zonenkante nach innen: Dachschnitt-HATCH bei −469 / −582 / −616 / −701 / −984 mm, LINE bei −1266 mm; die Dachfenster `Dachfenster_Kippflügel 10[7]`-`[10]` (im Roof-Block, ohne HATCH) liegen zu 100 % in der Zone. Nach außen: Modelspace-HATCH „New_255 Plangrafiken_Pen_No__1“, Muster DOUBLE_1_8, 32,35 m², von −462 bis +1358 mm (Schnitt mit der Bad-Zone 1,34 m²); graues SOLID-Band ab +1356 mm; Baulinie +1359 mm. New_255 ist per `_NEGATIV_LAYER` kein Wandkörper.
- **Messung:** Die Zone liegt 466 mm außerhalb der Außenkante und 1264-1266 mm außerhalb der Innenkante des Dachschnitt-Bands. Wandkörper nur zwischen −470 und −1000 mm mit 1343-mm-Dachfenster-Lücken; `wand_zu` ist bei −800 und −1000 mm lückenlos, bei −600 mm an den Fenstern 1180-1184 mm frei. Offen reicht von ca. −470 mm bis zur Hülle und dringt in die Nischen bis −600 bis −700 mm ein. Zone − Wandunion 21,80 m², Zone − geschlossene Wand 16,20 m² (größte Komponente; alle Teile 19,05 m²; B.13).
- **Root Cause:** Kein Fensterleck (Dachfenster sind ab −800 mm geschlossen). Das Band entsteht, weil die Zone über das Dachschnitt-Band hinaus in einen wandfreien Streifen reicht (**U9**, `raumlayer.py:98-124`, `kaskade.py:102-103`: Zone 1:1 als Raum) und die Außenanalyse Zonen nicht abzieht (**U8**, `aussenbereich.py:227-271`, `provider.py:114`); in die Fensternischen dringt die Fläche nur randlich ein (**U6**, `aussenbereich.py:129-138`).
- **Betroffen:** DG2 `raum_4`.
- **Fix / Blast Radius:** → 2.6 U6, U8, U9.
- **Art:** Fachfrage F5 (Raumfläche unter der Dachschräge, Fensternischen; Streifen zwischen Dachschnitt und Baulinie Außen oder Abseite) + Code U8.
- **Prüfstatus:** korrigiert. (a) Bbox-Obergrenze 356215143, nicht 356214085. (b) Der Streifen deckt sich mit der New_255-HATCH; „fachlich Außen“ ist unbelegt und wird Fachfrage. (c) Die Angabe „Lücke 8-10 m ohne Wandkörper“ (K4) ist methodenabhängig; entlang der Achse gemessen 1343 mm je Dachfenster. S-H2 „Flutung durch die Fenster“ ist für die Straßenfront widerlegt.

#### DG2-2 - Zimmer 59,3 m²

> „2DG: Genauso im Zimmer 59.3m2.“

- **Output:** DG2 `raum_2` ZIMMER 59,28 m² = Stempel, 8 Ecken. Schnitt mit `offen[0]` 6,73 m² (davon 4,65 m² außerhalb der Gebäudemaske).
- **Architektplan:** wie DG2-1; `Dachfenster_Kippflügel 10[3]`-`[6]` und `[11]`-`[14]` zu 100 % in der Zone; Schnitt Zone ∩ New_255-HATCH 3,29 m². Schächte L3/L5 im Zimmer siehe DG2-4.
- **Messung:** Zone − Wandunion 53,93 m² (5,36 m² Wand in der Zone), Zone − geschlossene Wand 40,49 m² (größte Komponente; alle Teile 47,22 m²; B.13). Profil Kante 3: bei −1000 mm nur am Kantenende 458 mm frei, bei −600 mm vier Lücken 1171-1177 mm.
- **Root Cause:** **U9** (`raumlayer.py:98-124`, `kaskade.py:102-103`) + **U8** (`aussenbereich.py:227-271`, `provider.py:114`) (+ Nischenanteil **U6**, `aussenbereich.py:129-138`).
- **Betroffen:** DG2 `raum_2`.
- **Fix / Blast Radius:** → 2.6 U6, U8, U9.
- **Art:** Fachfrage F5 + Code U8.
- **Prüfstatus:** korrigiert (wie DG2-1).

#### DG2-3 - „Stiegenhaus 1,2 m²“ am DBA-Schacht

> „2DG: Dann wurde ein Bereich als Stiegenhaus 1.2m2 markiert wo auch im Architektplan steht , dass dies ein DBA Schacht ist.“

- **Output:** DG2 `rest_2` STIEGENHAUS 1,159 m², 89 Ecken, Quelle R, ohne Stempel, Bbox 12551042/356215837 - 12553005/356217085. Stiegenhaus-Modell mit 1 Podest und einem PODEST-Anker bei (12551879, 356216461) im Schacht (Messung mit `tueren=[]`).
- **Architektplan:** MTEXT „DBA SCHACHT“ auf „New_255 Plangrafiken_Pen_No__1“ bei (12551856, 356216639), im Polygon. Geschlossene rote LWPOLYLINE 1,29 m² auf „New_255 Plangrafiken_Pen_No__21“ (IoU 0,88 mit `rest_2`), innere Kontur 0,13 m² auf „New_HKLS1_Pen_No__21“, HATCH FEUERFESTER_STEIN. Links und rechts Innenwände `Wall_44`/`Wall_52` (BETON_BEWEHRT_SN46). Keine Stufenlinien im Schacht (0,0 m). Daneben die Treppe `Stair_1` (Block-Bbox 12550947/356215866 - 12555358/356218331), deren Bbox den Schacht fast ganz überdeckt.
- **Messung:** Abstand `rest_2` → Stair_1-Bbox-Zentrum (12553153, 356217099) 726 mm. Die echte Funktion `_typisiere` liefert mit Markern STIEGENHAUS, mit leerer Markerliste SCHACHT (1,16 m² < 3 m², 0 Türen ≤ 600 mm, keine STO-Kästchen). Derselbe Schacht an derselben Lage ist in DG1 `rest_1` SCHACHT 1,25 m² (nächster Marker 3604 mm) und in OG3 `rest_2` SCHACHT 1,15 m² (Text 0 mm).
- **Root Cause:** **U2**: `rest_komponenten.py:57-86` `_marker_punkte` liefert das Bbox-Zentrum des Treppenblocks; in `_typisiere` greift die Markerregel `:92-93` vor der SCHACHT-Regel `:98-100`; Schacht-Text und Kontur liest kein Code. Der Typ stammt aus derselben Stair-Bbox wie in S-H1, das Polygon nicht.
- **Betroffen:** DG2 `rest_2`.
- **Fix / Blast Radius:** → 2.6 U2.
- **Art:** Code.
- **Prüfstatus:** bestätigt (K1 und K2b, alle vier Linsen). Fix: DG2-3 wird über **S3a** behoben (gedeckelte Text-Evidenz, Komponente < 3 m², unabhängig von F4; Wirkung B.3). Die Umordnung der türlosen SCHACHT-Regel vor die Markerregel (**S3b**) gilt nur bei F4 Option a und betrifft nur die Liftringe (siehe U2).

#### DG2-4 - Schächte in den Zimmern

> „2DG: Ebenfalls die Schächte in den Zimmern wurde nicht richtig erkannt und eingegrenzt.“

- **Output:** Keine SCHACHT-Stanzung in DG2-Räumen; alle L-Räume ohne Bereinigungsbuchung.
- **Architektplan:** `raum_5` ZIMMER 19,6: „S8 BDB 27/75“ (Kontur 0,202 m², in schwarzer Schachtwand) und „S8 DDB 27/75“ (0,202 m², teils gestrichelte rote Kanten in einem orangen Revisionskreis, rund 1,2 m daneben, Hinweis „Schachtverzug entweder im Zimmer oder über Dach“). `raum_2` ZIMMER 59,3: L3 (0,336 m²), L5 (0,125 m²). `raum_1` VORRAUM: S1, S2. `raum_7` VORRAUM: WP, BDB 27/75. Im Bad 24 keine rote Kontur. Schachtreihe „L1 DDB/BDB 25/25“, „L2 DDB/BDB 40/70“, „S5 DDB/BDB 40/105“ rechts der kleinen Treppe hinter einer Wand (Konturen L1 0,063, L2 0,28, S5 0,42 m²); die Einfügepunkte der Beschriftungen L1/L2 liegen aber in `rest_1`.
- **Messung:** M3 rote Fläche: `raum_1` 0,23, `raum_2` 0,461, `raum_5` 0,405, `raum_7` 0,165 m². Marker-Zellen (Zone − Wand, B.14): `raum_2` 0,403/0,214, `raum_5` 0,202 m². Schachtreihe L1/L2/S5: freie Rasterzellen hängen diagonal an der Treppen-Restfläche (8er-Label 5,838 m², 2 Konturen 3,991 + 1,844 m²), vektorisiert 3,995 m² = `rest_1`; mit 4er-Nachbarschaft eigene Komponente 1,845 m² → R-SCHACHT 1,849 m². „S7 DDB/BDB 60/95,5“ im VR/Büro: Komponente 0,3 m² bei `_MIN_M2` verworfen.
- **Root Cause:** Schächte in Zonen **U3** (`raumlayer.py:98-124`; `rest_komponenten.py:147-152`); Schachtreihe zwischen Räumen **U4** (`rest_komponenten.py:156` `label` ohne `connectivity`; `stempel_flutung.py:204-207` `_vektorisiere` nimmt nur die größte Kontur); kleine Schächte außerhalb von Zonen < 1 m² ebenfalls **U3** (Mindestfläche `rest_komponenten.py:42, 158-164`).
- **Betroffen:** DG2 `raum_1`, `raum_2`, `raum_5`, `raum_7`; Schachtreihe L1/L2/S5; S7.
- **Fix / Blast Radius:** → 2.6 U3, U4.
- **Art:** Code + Fachfrage F3 (DDB ohne BDB ausstanzen?).
- **Prüfstatus:** bestätigt. Präzisierung: Die Flächen im Cluster für L1/L2/S5 waren vertauscht zugeordnet; L1/L2-Beschriftungen liegen in `rest_1`.

#### DG2-5 - Stiegenhaus 15,9 m² und oranges Quadrat

> „2DG: Das Stiegenhaus 15.9m2 wurde erkannt, aber darüber wurde auch ein riesiges orangenes Quadrat eingezeichnet, was wenig sinn macht.“

- **Output:** DG2 `stiegenhaus_2` STIEGENHAUS 15,86 m², 12 Ecken, Bbox 12546309/356217795 - 12550379/356222125 = exakt die Extents von `Stair_2`. Überlappt `rest_3` STIEGENHAUS 6,41 m², `raum_7` VORRAUM 2,36 m², `raum_5` ZIMMER 2,26 m², `rest_4` 0,87 m², `raum_6` VORRAUM 0,30 m², `raum_3` TERRASSE 0,08 m². Stiegenhaus-Modell (mit `tueren=[]`): 3 Läufe, 4 Anker, davon ANTRITT (12546708, 356220076) in `raum_7` VORRAUM und AUSTRITT (12550566, 356219976) in `raum_6` VORRAUM.
- **Architektplan:** `Stair_2` (Layer „New_055 Treppen _ Lift“, 157 Segmente) ist mit dem Gebäude gedreht (Winkel des minimalen Rechtecks 66,6° mod 90), Insert-Punkt (12240439, 356160438) weit außerhalb. Konvexe Hülle 8,77 m², minimales gedrehtes Rechteck 11,02 m², Achs-Bbox 17,62 m². U-Treppe um den Liftschacht.
- **Messung:** Bbox-Mittelpunkt (12548344, 356219960) liegt im Wandkörper (`wand_union.covers` = True); nächster Raum `rest_3` 38 mm, `rest_4` 210 mm. `typisiere_geometrisch` hängt ein 17,62-m²-Rechteck an, `finde_lifte` stanzt den gedrehten Lift aus (17,62 → 15,86 m², 12 Ecken). In DG1 hat `Stair_1` dieselben Extents; dort deckt `rest_2` (9,09 m²) den Mittelpunkt, es wird nichts angehängt. M1: achsparallele Hülle im gedrehten Plan = 1.
- **Root Cause:** **U1**: `geometrie_typ.py:47-63` `stiege_rechtecke` nimmt die achsparallele Block-Bbox; der else-Zweig von `typisiere_stiegenhaus` (`geometrie_typ.py:86-96`) hängt sie ohne Deckungs- oder Überlappungsprüfung als `stiegenhaus_i` an.
- **Betroffen:** DG2 `stiegenhaus_2` und die überlappten Räume.
- **Fix / Blast Radius:** → 2.6 U1.
- **Art:** Code.
- **Prüfstatus:** korrigiert. (a) Nur der Anhängezweig darf geändert werden; eine Typisierung über den größten Hüllen-Schnitt würde UG `raum_17` „DBA Raum“ zu STIEGENHAUS machen. (b) Der Mittelpunkt liegt gemessen im Wandkörper, „Rasterzufall“ ist gestrichen.

#### DG2-6 - „Schacht 1,4 m²“ im Zimmer 19,6

> „2DG: Im Zimmer 19.6m2 wurde ein Bereich als Schacht 1.4m2 erkannt, was nicht stimmt weil dort eine Wand und ein Fenster ist sonst nichts. Die richtigen Schächten befinden sich im Zimmer, und diese wurde nicht eingegrenzt.“

- **Output:** DG2 `rest_5` SCHACHT 1,422 m², 164 Ecken, Bbox 12544287/356224587 - 12546465/356227737, KEIN_RAUM, 112 mm neben `raum_5` ZIMMER 19,6. In `uebersicht.png` rot gezeichnet (Darstellung „Schacht (mit Kreuz)“, `raumerkennung_darstellung.py:112, 132`).
- **Architektplan:** In der Nordwand des Zimmers Dachfenster `Roof_3` > `Dachfenster_Kippflügel 10[15]`/`[16]` (LWPOLYLINE/WIPEOUT auf „New_045 Dachkonstruktionen“, keine HATCH). Außerhalb der Fassade auf der Dachfläche vor der Attika ein roter Schachtkasten „New_255 Plangrafiken_Pen_No__21“ 0,387 m² mit innerer Kontur „New_HKLS1_Pen_No__21“ 0,046 m² und FEUERFESTER_STEIN in einem orangen Revisionskreis; MTEXT „Schachtverzug entweder im Zimmer oder über Dach blechverkleidet“ („New_160 Beschriftungen Ausführung“) in 1,8 m. Keine rote Kontur um das Fenster. Die echten Schächte im Zimmer sind S8 BDB/DDB 27/75.
- **Messung:** `_typisiere` für `rest_5`: 0 Türen ≤ 600 mm, Marker 5098/10215 mm, keine STO → SCHACHT allein über „< 3 m² und türlos“. 0,611 m² von `rest_5` liegen in den Hüllen der beiden Dachfensterblöcke, 0,262 m² im roten Kasten. R-Kontur (d = 1000) aus 183 Wandkörpern, davon 64 aus `Roof_*`-Blöcken: 162,6 m²; ohne Roof-Körper 52,08 m²; `rest_5` liegt zu 1,364 bzw. 0,121 m² darin (Zuordnung nur indikativ, größte Komponente wechselt). Fensterblöcke enthalten nur LWPOLYLINE/WIPEOUT/LINE/ARC.
- **Root Cause:** **U5**: SCHACHT ohne Evidenz allein über „< 3 m² und türlos“ (`rest_komponenten.py:98-100` `_typisiere`); Dach-Wandkörper erweitern die R-Kontur (`rest_komponenten.py:119-137`), die Dachfensteröffnung bleibt frei. „Die richtigen Schächte … nicht eingegrenzt“ = **U3** (`raumlayer.py:98-124`; `rest_komponenten.py:147-164`).
- **Betroffen:** DG2 `rest_5`; `raum_5` (S8).
- **Fix / Blast Radius:** → 2.6 U5, U3.
- **Art:** Code + Fachfrage F4. Planerfrage: `rest_5` überdeckt 0,26 m² eines gezeichneten Schachtkastens (Variante „über Dach“); die Aussage „sonst nichts“ trifft am Plan nicht ganz zu.
- **Prüfstatus:** bestätigt; S-H3-Teil „rote Fensterblock-Kontur wird als Schacht erfasst“ widerlegt (keine Farbregel im Code, 0 rote Konturen in Blöcken, rote Kontur im Bild ist das SCHACHT-Overlay). Fix korrigiert: Fensterzweig nicht über `fenster_signatur` (auf Rennweg leer), sondern Kriterium „allseitig ummauert“.

#### DG2-7 - Zimmer als Außenbereich

> „2DG: Auch hier wurden teilweise die Zimmer als Außenbereiche erkannt wo man aufpassen muss, die Außenbereich sind außerhalb der Fenster wo sich kein Balkon/Terasse oder Loggia befinden.“

- **Output:** DG2 offen 45,36 m² in zwei Teilen. Straßenseite 32,47 m² (siehe DG2-1/-2). Terrassenseite `offen[1]` 12,89 m² über `raum_3` TERRASSE 4,98 m², `raum_5` ZIMMER 19,6 mit 1,14 m² und `stiegenhaus_2` 0,23 m² (maximale Tiefe 1749 mm).
- **Architektplan:** `Wall_21` > `2-Flügelfenster 1+1 25[2]` (Terrassentür 2,30/2,18, Lücke 2423 mm, ohne HATCH), `Wall_19` > `1-Flügelfenster 25[1]`, `Wall_22` > `1-Flügelfenster 25[3]` (Lücke 1435 mm), alle ohne HATCH.
- **Messung:** `25[2]`: 1 % in Wandunion, 10 % in `wand_zu`, Brücke in der Mitte 0. M2 DG2: 4 Innenräume (ohne Terrasse), inkl. Terrasse 5; tiefer Schnitt (Raum um 300 mm verkleinert) nur 3 Innenräume, weil `stiegenhaus_2` ein 384 × 928-mm-Randstreifen des Treppen-Rechtecks ist.
- **Root Cause:** Terrassenseite **U6** (`aussenbereich.py:51-56, 129-138`: Terrassentür ≥ 2,4 m nie versiegelt); Straßenseite **U9** (`raumlayer.py:98-124`) + **U8** (`aussenbereich.py:227-271`, `provider.py:114`); `stiegenhaus_2`-Anteil **U1** (`geometrie_typ.py:86-96`).
- **Betroffen:** DG2 `raum_5`, `raum_2`, `raum_4`, `raum_3` (Freifläche), `stiegenhaus_2`.
- **Fix / Blast Radius:** → 2.6 U6, U8, U9, U1.
- **Art:** Code + Fachfrage F6 (Leonis' Definition „außerhalb der Fenster, wo kein Balkon/Terrasse/Loggia“ bezieht sich auf die geometrische Fläche) und F8 (Brücke bei Türen ≥ 2,4 m).
- **Prüfstatus:** bestätigt; Lückenmaße (2423/1435 mm) nicht unabhängig nachgemessen.

#### DG2-8 - größere Fenster nicht von der Wand unterschieden

> „2DG: Allgemein auf die Fenster aufpassen, da diese Fenster größer sind, und von der Wand nicht richtig differenziert wurden, sondern einfach mit erkannt wurden.“

- **Output:** Alle 12 Dachfenster der Straßenseite liegen zu 100 % in den Zonen `raum_2`/`raum_4`; `raum_5` enthält 29 % von `2-Flügelfenster 1+1 25[2]`, 24 % von `1-Flügelfenster 25[3]` und je 39 % von `Dachfenster_Kippflügel 10[15]`/`[16]`.
- **Architektplan:** Fensterblöcke ohne HATCH in `Wall_*` bzw. `Roof_*`; Rahmenlinien nur als LINE/LWPOLYLINE.
- **Root Cause:** Raumkontur = Zone, die die Fenster einschließt (**U9**, `raumlayer.py:98-124`, `kaskade.py:102-103`); Wandmaske kennt Fenster nicht als Wandfortsetzung (**U6**, `wandkoerper.py:164-173` nur HATCH).
- **Betroffen:** DG2 `raum_2`, `raum_4`, `raum_5`.
- **Fix / Blast Radius:** → 2.6 U6, U9.
- **Art:** Fachfrage F5 (Fensternischen zur Raumfläche?) + Code U6. **Rückfrage an Leonis (F17c):** Sind die Dachfenster der Straßenseite gemeint oder die Terrassentür 2,30?
- **Prüfstatus:** offen (Rückfrage); Mechanismus bestätigt.

### 2.6 Ursachen im Detail

Pseudocode ist Planungsnotation, kein Code. `# ponytail:` markiert bewusste Kalibrierknöpfe mit bekannter Grenze. „Test zuerst“ = der Test, der den Befund fängt und vor dem Fix rot sein muss (Handoff-Regel).

#### U1 - Treppen-Achs-Bbox als STIEGENHAUS-Raum

**Mechanismus.**
1. `geometrie_typ.py:54-62` (`stiege_rechtecke`) nimmt `bbox.extents` des Treppen-INSERTs, also die achsparallele Bbox; die Drehung der Blockgeometrie geht verloren. `_STAIR_BLOCK` (`geometrie_typ.py:30`) trifft auch Zonenstempel-Blöcke ohne Liniengeometrie (UG „Stiegenhaus__16“ 0,63 m², EG „Stiegenhaus__7“ 1,0 m², „TREPPENHAUS__14“ 0,79 m²; heute harmlos, weil `raum_16`/`raum_7`/`raum_14` die Zentren decken).
2. `typisiere_stiegenhaus` prüft nur, ob ein Raum ≥ 2 m² den Bbox-Mittelpunkt deckt (`geometrie_typ.py:75-80`, nur untypisierte Räume `:82`); sonst hängt der else-Zweig das Rechteck als `stiegenhaus_i` an (`:86-96`), ohne Deckungs- oder Überlappungsprüfung.
3. Der Aufruf liegt nach der Bereinigung (`provider.py:77-82` nach `kaskade.py:188-192`); Überlappungen bleiben.
4. `lift_erkennung.py:177-210` stanzt den gedrehten Lift aus (17,62 → 15,86 m²); `stiegenhaus.py:263-291` baut Läufe und Anker für das Rechteck.

**Belege (DG2, in-memory).** `Stair_2` Hülle 8,77 m², minimales Rechteck 11,02 m² (66,6° mod 90), Achs-Bbox 17,62 m²; Hülle zu 0,85 von Räumen und 0,83 von STIEGENHAUS gedeckt. Mittelpunkt (12548344, 356219960) in der Wandunion (Abstand 0), `rest_3` 38 mm, `rest_4` 210 mm. Alle Stair-Hüllen der 7 Pläne sind zu 0,85-0,99 von Räumen gedeckt; nur DG2 hängt an. Render: orange Achsrechteck über dem gedrehten Kern, Mittelpunkt auf der schwarzen Wand zwischen Lauf und Schacht.

**Fix (korrigiert: nur Anhängezweig).**
```text
# geometrie_typ.typisiere_stiegenhaus, else-Zweig (heute :86-96)
fuer (rect, center, flaeche) in stiege_rechtecke(plan):          # Funktion bleibt unverändert (kuerzel_entscheid.py:205-207)
    cover = Raum >= _MIN_REALRAUM_M2 mit covers(center)             # Typisierung wie heute
    if cover: wie heute; continue
    fp = konvexe_huelle(stiegenhaus._wcs_pts(v) fuer v in insert.virtual_entities())   # vorhandene Funktion, nur die Hülle ist neu
    if fp is None: continue                                          # Zonenstempel-Block ohne Linien ist keine Treppe
    if flaeche(fp ∩ union(raeume)) / flaeche(fp) >= ANTEIL_NEU:     # ponytail: Knopf; Rennweg 0,85-0,99; vor Einbau Muthgasse/Mollgasse/Barawitzka messen
        continue
    anhaengen('stiegenhaus_i', STIEGENHAUS, polygon = groesste_komponente(fp − union(raeume)))
```
Wiederverwendung vor Neubau geprüft: `objekt_stiege.finde_stiegen` liefert auf DG2 0 Kandidaten (B.9), ist nicht in `provider.py` verdrahtet, und jeder Kandidat ist auf Confidence 0,84 gedeckelt, braucht also Bestätigung. Als automatische Fußabdruck-Quelle für den Anhängezweig taugt es deshalb nicht. Die Hülle über das vorhandene `stiegenhaus._wcs_pts` (schon von `baue_stiegenhaus_modell` genutzt) ergibt für DG2 `Stair_2` 8,77 m² und `Stair_1` 6,57 m² (B.9); `stiege_rechtecke` und `kuerzel_entscheid` bleiben unberührt. Stufenlinien bzw. `objekt_stiege` werden erst wieder Thema, wenn F2 eine Treppenerkennung ohne Block verlangt.

Nicht übernehmen: „Raum mit größtem Hüllen-Schnitt wird STIEGENHAUS“. Gemessen: UG `Stair_1`-Hülle (13,16 m²) schneidet `raum_17` „DBA Raum“ (untypisiert, 6,11 m²) mit 5,65 m², `rest_4` STIEGENHAUS nur mit 3,44 m²; über dem DBA-Raum liegt eine gestrichelte Projektion des darüberliegenden Laufs (58,8 m Linien).

**Test zuerst.** Synthetisch: gedrehte Treppe (Linien) mit Hülle zu 90 % von Räumen gedeckt, Bbox-Mittelpunkt in einer Wand → kein neuer Raum. Bestehendes Fragment-Szenario (0,25 m² Raum, Hülle ungedeckt) hängt weiter an.

**Blast Radius.** Rennweg: nur DG2 (`stiegenhaus_2` entfällt, 5 → 4 STIEGENHAUS, 3 doppelte Läufe und 4 Anker weniger, davon 2 in Vorräumen). Tests: `tests/raumerkennung/test_geometrie_typ.py` (4 Unit-Tests mit Rechteck-Tupeln, `flaeche_m2 == 5.8` bei 5,76-m²-Rechteck, 2 Mollgasse-Tests), `test_kuerzel_entscheid.py` Z.107-126, `tests/naht/test_soll_mollgasse.py` Z.32-46, `tests/naht/test_soll_muthgasse.py` stair_exit-strict-xfails Z.475-509/576-644 (Kontaktzonen an `stiegenhaus_1/2`). Modell-Restüberlappungen Muthgasse 13 / 40,835 m², Barawitzka 4 / 7,131 m² (`Projekte/_ergebnis/VERLAUF.md` Z.172) verschieben sich. `scripts/analyse/layer_merkmale.py` Z.160 zählt `stiege_rechtecke`.

**Prüfstatus:** korrigiert (beide Linsen: Typisierungszweig unverändert lassen; „Rasterzufall“ gestrichen, Mittelpunkt liegt im Wandkörper).

#### U2 - Treppenmarker vor SCHACHT-Regel, Liftschachtring

**Mechanismus.**
1. `rest_komponenten.py:63-78` (`_marker_punkte`) liefert für Treppenblöcke das Bbox-Zentrum. Bei der U-Treppe um den Lift liegt es im Schacht.
2. `rest_komponenten.py:92-93` setzt STIEGENHAUS bei Abstand ≤ `_MARKER_NAEHE_MM` = 1000 (`:54`), bevor `:98-100` (SCHACHT bei < 3 m² und 0 Türen) greift. Schacht-Text und Schachtkontur liest kein Code.
3. `lift_erkennung.py:178-183` stanzt nur aus STIEGENHAUS, das das Liftzentrum deckt; `:196-210` behält den größten Rest als STIEGENHAUS. `provider.py:186-189` baut dafür Modelle; der Anker-Filter `:193-197` prüft nur das Kabinenrechteck.

**Belege.**

| Plan | Raum | vor `finde_lifte` | nach | Marker-Abstand | ohne Markerregel | außerhalb Lift + 400 mm |
|---|---|---|---|---|---|---|
| UG | `rest_3` | 2,69 m² | 0,95 m² | 0 mm | SCHACHT | 0,00 m² |
| EG | `rest_2` | 2,70 m² | 0,96 m² | 0 mm | SCHACHT | 0,00 m² |
| OG1 | `rest_2` | 2,74 m² | 1,00 m² | 0 mm | SCHACHT | 0,00 m² |
| DG1 | `rest_3` | 2,30 m² | 0,73 m² | 0 mm | SCHACHT | 0,00 m² |
| DG2 | `rest_4` | 2,62 m² | 0,87 m² | 210 mm | SCHACHT (echte Funktion) | 0,00 m² |
| DG2 | `rest_2` (DBA) | 1,16 m² | 1,16 m² | 726 mm | SCHACHT (echte Funktion) | - |

Echte Stiegenhäuser haben außerhalb Lift + 400 mm 13-19 m² (OG2 `rest_1` 16,79, OG3 `rest_3` 17,22, DG2 `stiegenhaus_2` 13,15). Stufenlinien in allen Ringen und im DBA-Schacht 0,0 m. OG2/OG3: Schacht mit Treppenraum verbunden, Lift mit Schlitz ausgestanzt; ob dort ein Schachtstreifen im STIEGENHAUS bleibt, ist nicht gemessen. „Lifttür nicht als Öffnung erkannt“ ist nur für DG2 belegt (0 Öffnungen ≤ 600 mm).

Spalte „ohne Markerregel“: für alle sechs Fälle mit der echten Funktion `_typisiere(shp, tueroeffnungen, [], sto)` auf den Kaskade-Polygonen vor `finde_lifte` gemessen (B.3; UG 2,691, EG 2,702, OG1 2,741, DG1 2,302, DG2 2,620 und 1,159 m²; jeweils 0 Türöffnungen ≤ 600 mm, 0 STO-Kästchen). Planzeichen-Evidenz: Schacht-Text (Wort SCHACHT oder DDB/BDB; ohne RAUM/TREPP/STIEG/AUFZUG/LIFT) im Polygon und in ≤ 500 mm nur bei DG2 `rest_2` („DBA SCHACHT“); rote Schachtfläche ≥ 0,02 m² (M3) nur bei DG2 `rest_2` (1,15 m²), bei keinem der fünf Ringe.

**DG2 `rest_1` (3,99 m²):** echte Treppe `Stair_1` (Stufennummern 1..7, 51,5 m Stufenlinien, im DG1 an dieser Lage `raum_7` „TV Raum“ ohne Treppe). Polygon aus R, Typ fachlich offen → Fachfrage F2.

**Fix (zwei Stufen wegen F4: S3a Evidenz behebt DG2-3; S3b Umordnung nur bei F4 a, nur Liftringe).** Der folgende Pseudocode ist Stufe **S3b** (türloser Kleinrest vor der Markerregel). Er gilt nur bei F4 Option a, weil er genau die Regel ohne Planzeichen-Beleg nach vorn zieht, die U5/F4 in Frage stellen. Stufe **S3a** (Evidenz, F4-unabhängig) steht darunter.
```text
# rest_komponenten._typisiere (:89-102)
tuer_n = Tueren <= 600 mm
if shp.area < _SCHACHT_MAX_M2 and (tuer_n == 0 or sto_treffer):
    return SCHACHT                                   # vor der Markerregel; kein neuer Knopf
if marker_abstand <= _MARKER_NAEHE_MM:
    return STIEGENHAUS
... GANG-Regel unverändert
```
Stufe S3a (in allen F4-Optionen gültig, weil ein Schacht mit Planzeichen in a, b und c SCHACHT ist):
```text
# rest_komponenten._typisiere (:89-102), vor der Markerregel
evidenz = schacht_text_im_polygon(shp) or any(shp.covers(p) fuer p in sto)
    # Wortgrenze; nie „DBA“ allein; nie Texte mit RAUM|TREPP|STIEG|AUFZUG|LIFT; Einfügepunkt im Polygon, kein Abstandsknopf
if shp.area < _SCHACHT_MAX_M2 and evidenz:
    return SCHACHT
# danach unverändert: Markerregel, GANG-Regel, SCHACHT-Regel „< 3 m² und tuer_n == 0“ (S3b zieht diese nur bei F4 a nach vorn)
```
Rennweg-Wirkung (echte Funktion, B.3): S3a macht nur DG2 `rest_2` (DBA-Schacht) zu SCHACHT. Die fünf Liftringe haben weder Schacht-Text noch rote Fläche und bleiben STIEGENHAUS. S3b macht zusätzlich die fünf Ringe zu SCHACHT (ohne Marker: UG `rest_3`, EG `rest_2`, OG1 `rest_2`, DG1 `rest_3`, DG2 `rest_4` → SCHACHT). Alle Läufe behalten in beiden Stufen ihren Typ. Abhängigkeit F4: Bei b („nur mit Evidenz“) entfällt S3b; die Ringe bleiben bis F1 STIEGENHAUS und werden in `finde_lifte` behandelt. Bei c („allseitig ummauert“) ersetzt das Umschlossen-Prädikat aus U5 in S3b die Bedingung `tuer_n == 0`; ob die Ringe umschlossen sind, ist nicht gemessen. `tuer_n` hängt in S3b an der Türquelle (U12), deshalb Nachmessung nach dem Türstapel als Pflicht-Gate (5.2). In den eingecheckten `raeume.json` von `Muthgasse_E2`, `Mollgasse_EG`, `Barawitzka_EG` gibt es keine R-STIEGENHAUS-Komponente < 3 m².

Nicht übernehmen:
- Stufenlinien-Kriterium (Cluster K1): Die Trennung „0 m gegen ≥ 35 m“ stammt aus einer Stichprobe nur mit rest-/STIEGENHAUS-Räumen; UG `raum_17` trägt 58,8 m gestrichelte Projektionslinien („Dashed Small“). Nur als späterer eigener Schritt mit Linientyp aus dem LTYPE-Muster (nicht aus dem Namen).
- Ungedeckelte Text-Evidenz „Wort SCHACHT → SCHACHT“ vor allem anderen: SCHACHT gewinnt in Regel 1 immer (`bereinigung.py:8-10`); „Schachtverzug entweder im Zimmer …“ steht im DG2-Plan; DDB/BDB-Beschriftungen stehen in Nachbarräumen. Text nur innerhalb der Deckelung (< 3 m²), mit Wortgrenze, nie „DBA“ allein, nie Texte mit TREPP|STIEG|AUFZUG|LIFT (Barawitzka „Aufzug 1 BD 1,98/2,02“, „Treppenlauf BD 4,745/1,26“).

`finde_lifte` (Ring → SCHACHT oder Teil des LIFT) erst nach Fachfrage F1 und zusammen mit dem offenen Bericht-Punkt „lift_* und SCHACHT“ (Barawitzka `rest_1`/`rest_3`).

**Test zuerst.** S3a: 1,2-m²-Komponente mit Text „DBA SCHACHT“ im Polygon, 700 mm vom Bbox-Zentrum eines Treppenblocks → SCHACHT; türlose 1-m²-Komponente ohne Text am Zentrum → STIEGENHAUS; Laufkomponente ≥ 3 m² mit Marker → STIEGENHAUS. S3b zusätzlich: türlose 1-m²-Komponente ohne Text 700 mm vom Zentrum → SCHACHT.

**Blast Radius.** S3a: nur Komponenten < 3 m² mit Schacht-Text oder STO-Kästchen im Polygon; Rennweg nur DG2 `rest_2` (B.3); andere Familien ungemessen. S3b: Grenze: ein Podest-Fragment < 3 m² ohne erkannte Tür wird SCHACHT und verliert das Fluchtweg-Flag (sicherheitsrelevant; `tuer_n` hängt an der Türquelle U12). Ring-SCHACHT überlappt dann LIFT 1,74 m² (Präzedenz Barawitzka `lift_2`/`rest_3`), beide KEIN_RAUM (`nutzungsklasse.py:45-46`); Bereinigung Regel 1 stanzt den Ring künftig aus Nachbarn (`tests/naht/test_ueberlappung_riegel.py` Z.68-69/87-88 nachmessen). `tuer_typisierung.py:190-194`, `wohnungen.py:48-50`, `ausgaenge.py:42-45` sehen den Ring nicht mehr als Stiegenhausseite. Stiegenhaus-Modelle und Anker entfallen (DG2 `rest_2`: 1 PODEST-Anker). `test_rest_komponenten.py` (plan=None) unberührt; `test_lift_erkennung.py::test_ausstanzen_aus_stiegenhaus` muss grün bleiben. Mollgasse LIFT-Blockmarker ungemessen.

**Prüfstatus:** Mechanismus bestätigt (K1 Befunde 2-3, K2b Befund 2; alle Linsen). Fix **strittig**: Cluster K1 und K1-Linse 1 bevorzugen Stufenlinien bzw. Text-Evidenz, K1-Linse 2 und K2b-Linse 2 die Umordnung. Aufteilung im Plan: DG2-3 wird über **S3a** behoben (gedeckelte Text-/STO-Evidenz im Polygon, Komponente < 3 m², unabhängig von F4; Wirkung B.3). Die Umordnung (**S3b**, türlose SCHACHT-Regel vor die Markerregel) gilt nur bei F4 Option a und betrifft nur die fünf Liftringe.

#### U3 - Schächte in Zonen werden nie erkannt und nie ausgestanzt

**Mechanismus.**
1. `raumlayer.py:67-78, 98-124` übernehmen die ArchiCAD-Zone als Raum (nur Außenring). Die Zone schließt die hohle Schachtzelle hinter der Schachtwand ein; auf „New_080“ gibt es keine Aussparungs-Polylinien (DG1 11, DG2 7 geschlossene Polylinien, keine < 1 m²).
2. `kaskade.py:173-175`: `belegte` = alle L/H/F-Polygone; `rest_komponenten.py:147-152` sperrt sie mit 100 mm Puffer, `:158-164` verwirft Komponenten < `_MIN_M2` = 1,0 m² (`:42`). OG1-Kontrafakt (L minus Schachtzellen): R liefert weiterhin nur `rest_1`/`rest_2`.
3. `bereinigung.py:266-269` (Regel 1) würde SCHACHT ausstanzen, bekommt aber kein Paar (R-Polygone schneiden L-Polygone gemessen mit 0 mm²).
4. Planzeichen werden nicht gelesen:
   - FEUERFESTER_STEIN wird per exaktem Alias Material SCHACHT (`material_matching.py:285-286`) und damit Wandkörper (`wandkoerper.py:36-37, 142-155`); auf „New_255 Plangrafiken_Pen_No__39“ verwirft `_NEGATIV_LAYER` (Muster `wandkoerper.py:43-47`, Filter in `_hatch_pruefen` `wandkoerper.py:136`) den Keil ganz (EG 7 von 16, OG1 2 von 17). Kein Code liest `Wandkoerper.material`.
   - Die rahmen-Signatur (`materialien.yaml:131-134`) filtert `material_matching.py:272-276` weg; `legende_import.py:120-126` erzeugt sie nur.
   - DDB/BDB/„DBA SCHACHT“ ohne m² werden kein Stempel (`stempel_anker.py:209-211, 230-233`); `raumtyp.py:113-115` kennt nur das Stempelwort „schacht“.
   - STO-Kästchen nur auf Layer `0\d-STO` (`rest_komponenten.py:52`); die Port-Regex (`_port/parsers/architecture_dxf.py:2666-2671`) ist nicht importiert.
5. Nach der Kaskade angehängte Polygone sehen Regel 1 nie (DG2 `stiegenhaus_2` enthält Marker-Zellen 0,741/0,15 m²).

**Belege.** Alle Schacht-Texte und roten Konturen liegen im Modelspace (Blockwalk bis Tiefe 3/4: 0 Treffer). Stabil über Geschosse: ACI 1, geschlossen, Strichstärke 13, FEUERFESTER_STEIN-Keil, MTEXT „Lx/Sx/H1/WP DDB/BDB b/h“ mit roter Hinweislinie. Rahmen-Layer wechseln (EG 19 Plangrafiken / 13 HKLS1 / 1 HKLS; OG3 25/5/2; DG2 20/7); dieselbe Kontur liegt bis zu dreimal gestapelt. Marker-Zellen (B.14: Zone − Wandunion, nicht größte Zelle, ≤ 3 m²; Beleg = rote geschlossene Rahmen-Kontur oder SCHACHT-Wandkörper in 10 mm): OG1 14 Zellen in 6 Räumen (1,698 m²; eine weitere Zelle 0,104 m² ohne Beleg), EG 12 Zellen in 3 Räumen (1,964 m²), DG2 `raum_2` 0,403/0,214, `raum_5` 0,202 m². Korrigiert: „7 Räume“ (OG1) ist nicht belegt; die Ausgabe nennt `raum_2`, `raum_9`, `raum_10`, `raum_11`, `raum_12`, `raum_13`. Alle Kleinzellen typisiert `_typisiere` als SCHACHT (0 Türen ≤ 600 mm, Stiegenmarker 4,5-9,6 m entfernt). M3: 34 Räume mit roter Fläche.

**Fix (Entwurf; Branch-Stapel S11a → S11b → S11c → S11d mit gemeinsamem Merge-Gate, siehe 5.2; S11b und S11c blockiert durch F3).** Die Markierung `[S11x]` ordnet jede Zeile ihrem Commit zu.
```text
# kaskade.raeume_aus_kaskade, nach R-Stufe, VOR bereinige_kaskade (ein Ort für Provider und plan_pruefen)
belege = schacht_belege(plan)                                # [S11a] Detektor; in S11a nur Hinweis + Kennzahl, keine Geometriewirkung
  # geschlossene rote Rahmen (effektive Farbe; Signatur familiengebunden laut F3(5)), gestapelte Duplikate zusammengefasst
  # FEUERFESTER_STEIN-HATCH mit eigenem Walk VOR dem Negativ-Layer-Filter
  # Material nur aus Signatur/Alias, nicht aus Layer-Hinweis (Barawitzka: 786 SOLID-HATCH auf Layern mit "Schacht")
  # kein Blockwalk, bis ein Plan Rahmen in Blöcken belegt (Rennweg 0)
wu = wand_union(wk)
fuer r in L/H/F-Raeume:                                      # [S11b] Ausstanzung in Zonen, blockiert durch F3(2)-(4)
    zellen = komponenten(Polygon(r) − wu)
    haupt = zelle mit Stempelpunkt, sonst groesste
    fuer z in zellen − haupt:
        if z.area <= _SCHACHT_MAX_M2 and flaeche(z ∩ belege) >= BELEG_MIN and keine Tuer <= 600 mm:
            # Schnittfläche statt Berührung (OG1 WC: 2 von 5 Zellen); ponytail: BELEG_MIN / Mindestgröße laut F3(3)
            schaechte += Raum('schacht_n', SCHACHT, z)      # eigene interne Quelle, nicht 'R' (kette/Rang)
zonenfreie Schächte: komponenten(Kontur − wu − belegte) ∩ belege, ohne _MIN_M2   # [S11c] blockiert durch F3(3)
Dedup gegen vorhandene SCHACHT und LIFT (IoU)                # [S11b], in S11c auf zonenfreie Schächte erweitert
bereinige_kaskade(raeume + schaechte, …)                    # [S11b] Regel 1 stanzt aus (polygon_roh, Buchung LIFT_SCHACHT)
Nachlauf nur LIFT/SCHACHT gegen spät angehängte stiegenhaus_*/lift_*  oder als bekannte Lücke dokumentieren   # [S11d]
Pflicht vorab (U13): durchgaenge_ohne_tuerblatt überspringt Paare mit KEIN_RAUM-Seite   # S5a, vor S11b
```
Designvariante (K2b): SCHACHT-Polygon = lichte rote Kontur statt Zelle. Text-Evidenz nur als Zusatz, nie als Ort: 14 der 49 Text-Räume (M3) haben die Kontur 41-150 mm hinter der Wand; DG2 „L1/L2“ stehen in `rest_1`, „S1/S2“ in `raum_1`, „S7“ in `raum_6`. Vokabular: WDB/WD (Wanddurchbruch, Mollgasse 46×, Muthgasse 52×) nicht aufnehmen; BD/DD (Barawitzka) nur ohne Lift-/Treppentext; „DBA“ allein nie.

**Test zuerst.** Synthetisch: L-Raum 5 × 5 m, innere Zelle aus 100-mm-Wänden mit roter geschlossener Kontur → SCHACHT-Raum existiert, Wirtsraum um die Zelle kleiner, Buchung LIFT_SCHACHT, kein Durchgang Schacht↔Wirtsraum. Negativ: rahmenlose Nische bleibt Raum.

**Blast Radius.**
- Alle Rennweg-Geschosse. Rote Rahmen zu > 50 % in einem Raumpolygon: UG 11, EG 14, OG1 16, OG2 19, OG3 22, DG1 16, DG2 17 (nur EG/OG1 nachgezählt; enthält Duplikate).
- Andere Familien: `materialien.yaml` wird global geladen (`wissen/__init__.py:42-64`) → ein Rahmen-Konsument wirkt sofort überall; Fischamender Schacht-Kästchen 0,08-0,2 m² auf `A_Raeume_` fallen heute per `raumlayer._MIN_FLAECHE_M2` weg; Mollgasse „SCHACHTTYP A/B“.
- Downstream: Stempelabweichung (Darstellung vergleicht bereinigte Fläche, `raumerkennung_darstellung.py:467-472`; Prüfstrecke trennt roh/bereinigt, `plan_pruefen.py:1358-1377, 1797-1800`), `nutzungsklasse.py:46`, `tuer_typisierung.py:295-296` (`tuer_in_schacht`), `platzierung/fachpraxis.py:73-76`, Schlitz-Kodierung (`bereinigung.py:332-366`; Konsumenten der Bbox-Mitte in `platzierung/geometry.py`), Bestandszahlen LIFT_SCHACHT (`docs/ENIS_UEBERGABE_0908.md` §20, `docs/COORDINATION.md:333`).
- Phantom-Durchgänge Schacht↔Wirtsraum ohne Guard (Simulation B.12: Marker-Zellen der Cache-Räume außer `stiegenhaus_*` als SCHACHT-Raum ausgestanzt, `durchgaenge_ohne_tuerblatt` ohne Türliste): EG 11 Durchgänge an 12 simulierten Schächten, OG1 6 an 14, DG2 6 an 6 (davon 1 Schacht↔Schacht); Breiten 824-1704 mm → `wohnungen.py:39-55, 75-80` kippen Vorräume. Korrigiert: Die frühere Angabe „DG2 9 von 10 (800-1490 mm)“ ist nicht reproduziert; von den 10 DG2-Nebenzellen (B.14) liegen 4 in `stiegenhaus_2`, das die Simulation ausschließt.
- Flächenwirkung: lichte Kontur −0,6 % (DG2 `raum_2`) bis −1,0 % (`raum_5`); Zellen −4,4 % bis −8,6 %; Zelle mit Schachtwand bis −14,3 % (OG1 WC).
- Tests: `test_bereinigung.py` (Regel 1, Flächenbuchhaltung), `test_rest_komponenten.py` unverändert, `test_kaskade.py::test_barawitzka_raeume` (≤ 53, Ist 50) und `::test_mollgasse_raeume_kuratiert` (≤ 70), `tests/naht/test_ueberlappung_riegel.py` (Band Rennweg_EG/OG3 = 0; bricht, wenn `_schlitz` fehlschlägt, `bereinigung.py:448-453`), `test_material_matching.py:137` bleibt grün; neuer Test.

**Prüfstatus:** Mechanismus bestätigt (K2a, K2b, alle Linsen). Fix korrigiert (Beleg über Schnittfläche, globaler Blast Radius, Guard, Vokabular, Negativ-Layer-Keile, Dedup). Polygon-Definition (Zelle, Kontur, mit Wand) **strittig** → F3(2). Umsetzung als Stapel S11a-S11d, damit die Korpusmessung der Beleg-Treffer (S11a) ohne Geometriewirkung vor der Ausstanzung steht.

#### U4 - R-Stufe verliert diagonal verbundene Flächen

**Mechanismus.** `rest_komponenten.py:156` ruft `label(~blockiert)` ohne `connectivity` (skimage 0.26.0: 8er-Nachbarschaft). `stempel_flutung.py:204-207` (`_vektorisiere`) nimmt nur die größte `find_contours`-Kontur. Zusätzlich verwirft `:160/163` alles < 1 m².

**Belege.** Synthetisch: zwei 6 × 6-Blöcke, Ecke an Ecke → 8er 1 Komponente, 4er 2; Maske 180 000 mm², Polygon 76 250 mm². DG2 (mitgeschnittene echte Maske): Label 5,838 m², 2 Konturen (3,991 + 1,844 m²), Polygon 3,995 m² = `rest_1`; die Zellen der Schachtreihe L2 (130/130 frei) und S5 (184/184) liegen darin. Mit 4er-Label: zusätzliche Komponente 1,845 m² → 1,849 m² SCHACHT. DG1 unverändert (L1/L2 0,845 m² → 4er 0,325/0,122 m², S5 0,488, S9 0,375, S7 0,248, S2 0,218 m² bleiben < 1 m²). DG2 S7 0,3 m² verworfen.

**Fix.**
```text
labels = label(~blockiert, connectivity=1)                          # rest_komponenten.py:156
# stempel_flutung._vektorisiere (:202-219), wirkt für R-Stufe und flute_stempel:
verlust = flaeche(maske) − poly.area
if verlust > TOL: warnung(id, verlust)                              # ponytail: TOL Knopf; stilles Verwerfen sichtbar machen
# label(frei) in flute_stempel (:151) erst nach Messung auf Flutungsplänen umstellen
```
**Test zuerst.** Zwei 2 × 2-m-Freiflächen, die sich nur an einer Rasterecke berühren → zwei R-Räume, Flächensumme erhalten.

**Blast Radius.** Alle Pläne mit R-Stufe; `rest_N`-IDs verschieben sich (DG2: neue Komponente wird `rest_1`, bisher `rest_1..5` → `rest_2..6`) → `raeume.json`, Bericht, ID-Vergleiche. Die gerettete Schachtreihe ist nur über „klein und türlos“ SCHACHT (gekoppelt an U5) und grenzt an `raum_2` (Guard aus U13 nötig). Falls Text-Evidenz eingeführt wird: OG3 `rest_1` hat Texte in 494-556 mm.

**Prüfstatus:** bestätigt (beide Linsen); Blast Radius korrigiert (Guard in `_vektorisiere`, ID-Verschiebung).

#### U5 - SCHACHT ohne Evidenz (DG2 `rest_5`)

**Mechanismus.** `rest_komponenten.py:98-100` vergibt SCHACHT allein über < 3 m² und `tuer_n == 0`; `tests/raumerkennung/test_rest_komponenten.py:31-37` schreibt das für eine ummauerte 1,4 × 1,3-m-Box fest. Die R-Kontur (`:119-137`, d = 1000) enthält 64 Wandkörper aus `Roof_*`-Blöcken (Dachaufbau WAERMEDAEMMUNG/STAHLBETON/GIPSKARTON), dadurch die Dachfläche vor der Fassade; die Dachfensterblöcke haben keine HATCH, die Öffnung bleibt frei. Eine Farbregel „rot = Schacht“ existiert nicht (Farbe nur in `fluchtweg.py:69`, `legende_import.py`, `material_matching.py`).

**Belege.** Siehe DG2-6. Bestand anderer SCHACHT: OG3 `rest_1` 1,157 m² (Texte S5/L1/L2 in 494-556 mm), OG3 `rest_2` 1,152 m² („DBA SCHACHT“ 0 mm), DG1 `rest_1` 1,25 m²; Barawitzka `rest_1` 2,304 m² (BD-Texte 0 mm), `rest_3` 2,534 m² (143 mm „Lifttuere 90/200“ = Lift). Heute latenter Durchgang `raum_5`↔`rest_5` 1531 mm (ohne Türliste).

**Fix (korrigiert: Option c, namensfrei).**
```text
umschlossen = (shp.buffer(RASTER) − wand_union) ∩ kontur_rand_band ist leer
if schacht_evidenz(shp) or (umschlossen and shp.area < _SCHACHT_MAX_M2 and tuer_n == 0):
    return SCHACHT
return ''                                            # Laibungen, Nischen, Dachreste am Konturrand
```
Nicht über `fenster_signatur` (auf Rennweg leer, Docstring Z.20-24) oder Blocknamen („Dachfenster_Kippflügel“).

**Test zuerst.** Box mit Fensterlücke am Konturrand → nicht SCHACHT; ummauerte Box aus Z.31-37 bleibt SCHACHT.

**Blast Radius.** Option c hält `test_rest_komponenten.py` grün, Option b bricht ihn. `test_bereinigung.py::test_regel1_vor_regel2_schacht_gewinnt` baut SCHACHT synthetisch (grün); Docstrings `bereinigung.py:34-40` veralten. Untypisierte Kleinflächen bekommen Klasse None (`wohnungen.py:28-29`); ≥ 2 m² kann `typisiere_stiegenhaus` sie zu STIEGENHAUS machen (Barawitzka `rest_3`, nicht gemessen). Der latente Durchgang `raum_5`↔`rest_5` entfällt. Roof-Körper in der Kontur betreffen auch Flutung und R (U10).

**Prüfstatus:** bestätigt; S-H3-Teil „rote Fensterblock-Kontur“ widerlegt; Fix korrigiert. Fachfrage F4.

#### U6 - Fensterlücken und dünne Wandschraffur lassen die Außenfläche in Zimmer fließen

**Mechanismus.**
1. `wandkoerper.py:164-173` sammelt nur HATCH. Fensterblöcke der 25-Familie und Dachfenster haben 0 HATCH (OG1 4, DG1 14 Mini-Körper aus schraffierten Fenstern, DG2 0); ungeschraffierte Wandschichten fehlen (OG1 `Wall_5` 480 mm). Fensterrechtecke liegen zu 1-6 % in der Wandunion.
2. `aussenbereich.py:136-138` (`_wand_geschlossen`): simplify(20), buffer ±1200 mit `quad_segs=2`. Die Kommentare `:51-55` und `:145-146` („überbrückt Öffnungen ≤ 2·d“, „Doppelflügel-Hauseingänge ~1,9 m müssen versiegelt werden“) stimmen nur für sehr dicke Wände; der Docstring `:132` nennt `join_style mitre`, `:138` setzt keinen.
3. Der Teil aus Raumloch und Freifläche berührt den Hüllrand (`:260`), der Hals erreicht die Kante (`:268-271`, Kante = ganzer Rand, weil kein Gehsteig-Layer). Ergebnis offen.
4. Balkon- und Fenstertüren mit 2,4 m (OG1/DG1 `Wall_6`, DG2 Terrassentür 2423 mm) sind nie versiegelbar; `:54-55` lässt Tore ≥ 2,4 m absichtlich offen (Mollgasse „Garagentor-Ostkante“ als Weg ins Freie).

**Belege (synthetisch mit `_wand_geschlossen`).**

| Wanddicke t | versiegelt (Restbrücke) | offen ab |
|---|---|---|
| 200 mm | g = 800 mm (51 mm) | g = 1000 mm |
| 400 mm | g = 1300 mm (44 mm), g = 1400 mm (3 mm) | g = 1600 mm |
| 600 mm | g = 1600 mm (120 mm) | g = 2000 mm |

g = 1900 mm ist bei t ≤ 400 mm offen (A.8.5); für t = 600 mm stammt „offen bei 1900 mm“ aus `_k4g_mess.py` (A.10.3), die Tabelle zeigt dort nur 1600 versiegelt / 2000 offen. Die Formel t > 2(d − √(d² − g²/4)) ist nur eine Obergrenze für runde Puffer. Gegenprobe mit Fensterblock-Rechtecken als Barriere (B.11: minimale Rechtecke verschachtelter Blöcke mit FENSTER/WINDOW in Name oder Layer als zusätzliche Wandkörper, zusammen mit dem Loch-Test; der Namensfilter dient nur der Gegenprobe, nicht als Fix): Zimmer-Schnitt OG1 38,94 → 0, OG2 21,39 → 0, DG1 Nord (nach Loch-Test) 37,28 → 0, OG3 (nach Loch-Test) 33,67 → 0 m²; in DG2 bleiben `raum_2` 1,80 und `raum_4` 0,34 m². Dieselbe naive Barriere verliert im EG den Haupteingang `tuer_11` (Texttür „TÜRSCHLIESSER“ in `Wall_2` > „Window 27[5]“ + „Fenster_Halbkreis_Fest[11]“): Abstand zum Komponentenrand 184 → 332 mm, mehr als die 300-mm-Probe (`tuer_zuordnung.py:31, 106-115`) → keine AUSSEN-Seite, kein hauseingang, kein final_exit.

**Fix (strittig).**
```text
def oeffnungs_bruecken(koerper):                             # nur in aussenbereich._wand_geschlossen verwenden,
    fuer (a, b) in stirn_paare(koerper):                      # nie in KaskadeErgebnis.wandkoerper (Durchgänge/R/Flutung)
        # familienneutral: zwei Wandkörper-Stirnen, kollinear, gleiche Dicke, Lücke g <= G_MAX;
        # Quelle ist nur die Wandkörper-Geometrie, kein Block, kein Layer, kein Name
        yield band_zwischen(a, b, dicke=min(a.t, b.t))        # ponytail: G_MAX, Winkel-/Dickentoleranz sind Knöpfe; g >= 2,4 m laut F8
    # Öffnungsgeometrie im Band (Fensterblock im Wall_*, Fenster-Layer, Rahmen-Signatur) nur als Beleg im Hinweis, nie Voraussetzung
wand_zu = _wand_geschlossen(koerper + bruecken, _SCHLIESS_MM)
Docstrings :51-55, :132, :145-146 mit gemessenen Schwellen korrigieren
```
- Sicht K4 (Cluster und beide Linsen): Brücke im Wandband für **alle** Öffnungen, ohne Ausnahme für Türblatt/Fenstertür; sonst bleiben die Balkontür-Lecks (OG1 `raum_1`/`raum_2`, DG1 `raum_2`/`raum_3`).
- Sicht K3 (Linse 2): Brücken zurückstellen, bis die Nachher-Messung nach U7 und U8 zeigt, dass sie nötig sind; Balkontür gegen Durchfahrt ≥ 2,4 m ist ungelöst (F8).

**Test zuerst.** Synthetischer 400-mm-Wandring mit 1320-mm-Fensterlücke und 2400-mm-Fenstertür, Raum dahinter → Raum nicht offen; eine Texttür in einer Fassadenlücke behält ihre AUSSEN-Seite.

**Blast Radius.** Grenze der Brückenquelle: Stirnpaare setzen voraus, dass die Wand beidseits der Öffnung als Wandkörper (HATCH) vorliegt. Das gilt unabhängig davon, ob Fenster als Block im `Wall_*` (ArchiCAD), im Modelspace oder auf eigenen Fenster-Layern liegen (Mollgasse „FENSTER“, Barawitzka „320 Fenster“/„325 Dachfenster“, Fischamend „^A_Fenster$“, siehe U9). Nicht abgedeckt sind ungeschraffierte Wandschichten (OG1 `Wall_5`, 480 mm) und Familien, deren Wandkörper aus dem Doppellinien-Fallback kommen (`wandkoerper.py:176-177`). Wirkung außerhalb Rennweg ungemessen; zusätzliches Risiko: auch echte Durchfahrten/Tore zwischen kollinearen Wandstücken werden gebrückt (F8). `kontur`/`gedeckt()` → `ordne_tueren`, `aussentor_tueren`, `aussen_durchgaenge`, `typisiere_tueren` (`kein_weg_ins_freie`), `leite_ausgaenge`/final_exit (EG/UG), `kreuzcheck`, U19. Pflichtmessung vor Merge: Rennweg EG `tuer_11`, Mollgasse EG `aussenoeffnung_1` Müllraum (`tests/e2e/test_mollgasse_eg_durchstich.py` Z.98-106, RZ-Band ≤ 34) und `tuer_68`, Barawitzka Hof 190,2/23,5 m² und `exit_tuer_27`. Tests: `tests/raumerkennung/test_aussenbereich.py` (6), `test_tuerquellen.py`, `test_tuer_zuordnung.py`, `tests/naht/test_soll_rennweg.py::test_soll_eg_final_exit_via_text` (Z.109-120) und `::test_soll_eg_wege_enden_am_final_exit` (Z.123-130), `test_soll_mollgasse.py::test_soll_hofausgaenge_cluster_a_und_b` (Z.66-79) und `::test_kreuzcheck_findet_endpunkte_an_der_aussenkante` (Z.93-98), `test_soll_barawitzka.py::test_soll_genau_ein_final_exit` (Z.41-52), Muthgasse-Laufzeit (`quad_segs=2` war Performance-Entscheid).

**Prüfstatus:** Mechanismus bestätigt; Fix **strittig** (Brücke ja/nein, Ausnahmen) → F8.

#### U7 - Randtoleranz statt Topologie

**Mechanismus.** Bezug = konvexe Hülle (`aussenbereich.py:240-241`), frei = Bezug − `wand_zu` (`:245`). `beruehrt_rand = t.distance(rand) < _RAND_EPS_MM` (250 mm, `:58`, `:260`) lässt ein Loch durch (`:261-262`); der Hals (`buffer(-400).buffer(420)`, `:268-270`) liegt ebenfalls < 250 mm an der Kante → offen. Jeder freie Teil ist entweder vollständig ein Loch der Komponenten oder vollständig außerhalb.

**Belege.** DG1: `wand_zu` hat zwei Löcher (103,76 und 5,42 m²); das große liegt 193 mm vor dem Hüllrand (Hals 173 mm), rohe Wand auf der Verbindungslinie 0 mm, geschlossen 11 mm (am Fenster `2-Flügelfenster 1+1[4]`); das AR-Loch hat 339 mm und bleibt innen. OG3: zwei Löcher 41,25 und 37,13 m², je 193 mm, Südfenster `2-Flügelfenster 1+1 25[1..7]` ohne HATCH, Lücke 1320 mm. Grenzfälle, die heute richtig innen bleiben: OG1 Wohnküchen-Loch 70,77 m² (364 mm), OG2 Wohnbereich 57,45 m² (325 mm). Eine Kontaktlänge mit Snap wirkt in DG1 nur bei Snap < 193 mm (0 mm bei 1/50/100, 4064 mm bei 200, 6182 mm bei 250).

**Fix.**
```text
komp_u = unary_union(komponenten)
ist_loch = t.within(komp_u.buffer(1.0))                     # binär, keine neue Schwelle
beruehrt_rand = (not ist_loch) and t.distance(rand) < _RAND_EPS_MM
if not (hat_indiz or beruehrt_rand): continue               # Loch nur mit Indiz AUSSEN
```
**Test zuerst.** Wandring mit 150-mm-Restbarriere zur Hülle, Innenraum ohne Indiz → nicht offen.

**Wirkung (in-memory gemessen).** DG1 offen 143,83 → 40,07 m², OG3 114,03 → 35,66 m²; UG, EG, OG1, OG2, DG2 unverändert. OG3-Außenringöffnungen (`raum_10` GANG 1598 mm, `rest_3` 2473/822 mm) entfallen.

**Blast Radius.** `test_aussenbereich.py` logisch grün (Zwei-Trakte ragt heraus, Hof mit Baum = Indiz, Hof ohne Indiz bleibt unklassifiziert, U-Hof ragt heraus; nicht ausgeführt). Ein indizloser Innenhof als Loch nahe der Hülle verliert „offen“ (F7). Mollgasse 910,1 m² offen stammt aus nicht schließenden Wänden (keine Löcher), bleibt (Bestandsangabe, nicht nachgemessen). Pläne mit Grundstücksgrenze: Barawitzka (616,8 m²) und Mollgasse (1510,2 m²) haben laut Docstring `aussenbereich.py:168` einen Grenzring; dort ist der Bezug der Ring statt der Hülle, und ein indizloses Loch nahe dem Ring würde ebenfalls kippen. Die Wirkung dort ist ungemessen. Rennweg-Basis (B.1): 3 Teile kippen von offen auf nicht offen (DG1 103,76 m², OG3 41,25 und 37,13 m²), alle ohne Indiz, alle Löcher mit 193 mm Randabstand. Sicherheitsrelevant, weil ein verlorenes „offen“ im EG Hauseingang und final_exit entzieht → Merge-Gate S1 (5.2).

**Prüfstatus:** bestätigt (K4 und K3/K6b, alle Linsen); Vereinfachung `within` statt 1-m²-Schwelle.

#### U8 - Außenanalyse ohne Innen-Veto (Fachregel S-C)

**Mechanismus.** `erkenne_aussenbereiche(plan, koerper)` (`aussenbereich.py:227-228`) erhält nur Wandkörper; die Klassifikation `:256-271` prüft Fläche, Indiz (Layer-Regex `:46-47`, Baumblock `:49`), Randabstand und Hals. `provider.py:114` ruft sie auf, obwohl Räume und Stempel seit `:77-82` vorliegen. `gedeckt()` (`:91-98`) = Komponenten ∪ geschlossen − offen; Zonen außerhalb der Komponenten bleiben ungedeckt, selbst wenn man sie aus `frei` abzieht (Simulation: nur DG1 `raum_1`/`raum_7`/`raum_8` würden gedeckt; OG1 `raum_1/2/3/15`, DG1 `raum_2/3/6/9/10`, DG2 `raum_2/3/4/5` nicht).

**Belege.** Stempel in offenen Teilen: DG1 7 (Zimmer 14,51, Bad 8,58, Zimmer 15,71, Bad 4,8, Wohnzimmer 83,93, TV Raum 15,91, VR 8,94), OG1 4 (3× Zimmer, Balkon), OG2 4 (2× Zimmer, 2× Terrasse), OG3 4 (Zimmer 20,25, Zimmer 23,27, Wohnküche 38,35, Hobbyraum/Fitness 45,36), DG2 1 (Terrasse). Möbel/Sanitär darin (Einfügepunkt): DG1 12× Chair 02, Doppelbett 01, Schrank variabel, Waschbecken, Shower Kit; OG1 Bett Gruppe, Schrank; OG2 Doppelbett 01, Schrank. `dxf_load.py:218-229`: DIMENSION auf „New_GRUNDSTÜCKSGRENZE“ liefert keine Punkte → 0 Indizien. Frühere Veto-Varianten (`docs/OFFENE_FRAGEN.md` Z.238-242): „Nutzungsklasse ≠ AUSSEN“ und „nur positiv typisierte Räume“ verloren den Barawitzka-Hof (23,5 → 0 m², „fälschlich offen“); TERRASSE war dort nicht im Veto; Ursache nicht rekonstruiert (vermutlich Neubewertung zerschnittener Teilstücke). DG2: Ein Veto aus rohen Raumpolygonen würde 4,65 m² (`raum_2`) und 1,28 m² (`raum_4`) außerhalb einer 5-m-Gebäudemaske als gedeckt erklären (Dachstreifen). Freiflächen: `nutzungsklasse.py:41-43` BALKON/TERRASSE → AUSSEN; S-C nennt sie „nie Außenbereich“; Mollgasse `raum_61` TERRASSE TOP 1 (19,48 m²) liegt 10 mm, EIGENGARTEN TOP 1 1,74 m vom Soll-Punkt der Hoftür Cluster B.

**Fix (korrigiert).**
```text
def erkenne_aussenbereiche(plan, koerper, innen_zonen=None):     # optional → test_aussenbereich.py mit 2 Argumenten grün
    innen = unary_union(poly(r) fuer r in innen_zonen or [])
    innen = innen ∩ gebaeude_maske                               # ponytail: Maske z. B. Closing der Wandkörper mit großem d; Knopf, vor Einbau über alle Pläne messen
    fuer t in teile:
        rest = t − innen                                          # Differenz; Reste erben den Status, gewinnen „offen“ nie neu
        …
    gedeckt = komponenten ∪ geschlossen ∪ innen − offen          # ohne diesen Teil bleibt die kontur für Türen unverändert
# provider.py:114
innen_zonen = Räume laut gewählter F6-Option
  # Default ohne Entscheid = F6 Option 1 ohne Freiflächen, gemessen in B.2:
  #   Typ in {WOHNZIMMER, ZIMMER, SCHLAFZIMMER, KINDERZIMMER, BAD, WC, ABSTELLRAUM, VORRAUM, STIEGENHAUS} (= M2 INNEN_TYPEN)
  # F6 Option 4: zusätzlich gestempelte Räume ohne Außen-Vokabular und Räume mit Sanitär-/Möbel-Beleg
  # nicht „jede gestempelte Zone“ (Option 3; Mollgasse EIGENGARTEN/VORPLATZ/TERRASSE)
```
**Test zuerst.** Synthetischer Ring mit Fensterlücke, dahinter gestempeltes ZIMMER → Zimmer nicht in `offen` und in `gedeckt()`; eine TERRASSE-Zone vor der Fassade bleibt offen.

**Wirkung (in-memory nachgerechnet, B.2).** Nach S1 wird die Veto-Fläche abgezogen: Räume mit Typ in {WOHNZIMMER, ZIMMER, SCHLAFZIMMER, KINDERZIMMER, BAD, WC, ABSTELLRAUM, VORRAUM, STIEGENHAUS}, also Leonis' Liste ohne Freiflächen und identisch mit M2 `INNEN_TYPEN`. Die Veto-Fläche ist auf die Gebäudemaske zugeschnitten (Komponenten von `_wand_geschlossen(koerper, 5000)`, wie K4-Gegenprobe). Zählung wie M2.

| Plan | offen heute m² | nach S1 | nach S1+S2 (Zuschnitt) | M2 `wert` heute → S1 → S1+S2 | verbleibende Innenräume nach S1+S2 | ohne Zuschnitt: offen m² / `wert` |
|---|---|---|---|---|---|---|
| UG | 23,19 | 23,19 | 23,19 | 0 → 0 → 0 | - | 23,19 / 0 |
| EG | 0 | 0 | 0 | 0 → 0 → 0 | - | 0 / 0 |
| OG1 | 64,13 | 64,13 | 25,19 | 3 → 3 → 0 | - | 25,19 / 0 |
| OG2 | 51,47 | 51,47 | 30,08 | 2 → 2 → 0 | - | 30,08 / 0 |
| OG3 | 114,03 | 35,66 | 1,99 | 4 → 2 → 0 | - | 1,99 / 0 |
| DG1 | 143,83 | 40,07 | 2,78 | 7 → 4 → 0 | - | 2,78 / 0 |
| DG2 | 45,36 | 45,36 | 40,40 | 4 → 4 → 2 | `raum_2` ZIMMER 4,65 m², `raum_4` BAD 1,28 m², beide Schnitte vollständig außerhalb der Maske (Dachstreifen, U9/F5) | 34,46 / 0 |
| **Summe** | **442,01** | **259,88** | **123,63** | **20 → 15 → 2** | | 117,69 / 0 |

Offen bleiben die Freiflächen OG1 `raum_15` BALKON 7,50 m², OG2 `raum_13`/`raum_14` TERRASSE 15,17/7,50 m² und DG2 `raum_3` TERRASSE 4,93 m² (F6). Die Reste in DG1 (2,78 m²) und OG3 (1,99 m²) schneiden keinen Raum über 0,05 m².

**Metrik gegen Fix.** M2 zählt einen Raum auch dann als innen, wenn er nur einen Stempel oder einen Möbel-/Sanitär-Block trägt. Das Veto nach Option 1 deckt solche Räume nicht: Typen außerhalb der Liste (KÜCHE, GANG, AUFZUGSVORPLATZ, SCHLEUSE, TECHNIK …) und untypisierte gestempelte Räume (DG1 „TV Raum“, OG1 „Wohnkche“). Auf Rennweg ändert das die Zahlen nicht. Die 15 nach S1 verbleibenden Räume (S1-Akzeptanz) haben alle einen Typ aus der Liste; OG3 `raum_1` KÜCHE und DG1 `raum_7` „TV Raum“ fallen schon mit S1 heraus (B.1, `S1_within`-Liste). Bei einem Fensterleck ohne Loch blieben sie unter Option 1 offen, und M2 würde sie weiter zählen. Für F6 Option 4 folgt ohne neue Messung nur: `wert` nach S1+S2 bleibt 2, weil die Veto-Fläche nur wächst und beide Reste vollständig außerhalb der Maske liegen. Die offene Fläche unter Option 4 ist nicht gemessen. Ohne Zuschnitt fiele `wert` auf 0, aber der Dachstreifen würde gedeckt (verworfen, 7.1). Die frühere Cluster-Gegenprobe (OG1 25,02, OG2 30,01, DG2 34,37, DG1/OG3 0 m²; andere Veto-Liste, kein Zuschnitt) ist damit ersetzt. Nicht nachgerechnet sind die Türfolgen. Die Cluster-Emulation meldete für OG3: 2 falsche Stiegenhaus-Außenöffnungen entfallen, 1 neue bei (12552000, 356220800) entsteht, weil der Ring der neuen gedeckten Fläche folgt.

**Blast Radius.** `ordne_tueren` prüft Räume vor der kontur (`tuer_zuordnung.py:109-111`) → Wirkung vor allem auf den Ring von `aussen_durchgaenge`, `aussentor_tueren`, `kreuzcheck`, Darstellung und Prüfkennzahl „Außen auf Räumen“. Tests: `test_aussenbereich.py` Z.57/68/78/146/150/170, `test_provider.py` Z.47-62, `test_tuerquellen.py`, `tests/naht/test_soll_mollgasse.py` (Hof, Cluster B, `test_soll_alle_graph_wege_enden_am_final_exit`), `test_soll_barawitzka.py`. Untypisierte R-Resträume ohne Stempel bleiben ohne Veto. Contract unberührt.

**Prüfstatus:** Mechanismus bestätigt (K3, K4, K6b); Fix korrigiert (gedeckt einschließen, Typliste statt „jede Zone“, Clip auf Gebäudemaske, Differenz statt Verwerfen). Freiflächen → F6.

#### U9 - Raumkontur ist die Zone, nicht die sichtbare Wand

**Mechanismus.** `kaskade.py:102-103` übernimmt `raeume_aus_layer` als Quelle L, bevor `finde_wandkoerper` läuft (`:110`); `raumlayer.py:67-78, 98-124` prüfen weder Wandflucht noch Fenster noch Dachschnitt. Die Bereinigung ist die einzige spätere Änderung. Die Stempelflächen sind die Zonenflächen (|Abweichung| ≤ 0,03 %).

**Belege.** OG1 `raum_3`: Zone an der inneren Linie einer über die ganze Kante ungeschraffierten 480-mm-Schicht (Strahl: −1 LWPOLYLINE, 0 Zone, +479 HATCH, +679 LWPOLYLINE), Fensterrahmen bei +369…+459. DG1 `raum_1` Kante 2: Zone an der Innenflucht der 400-mm-Wand (+0/+200/+400 HATCH, +402 Plangrafik, +405 Baulinie), Rahmen +140…+230. DG2 `raum_4`/`raum_2` Kante 3: siehe DG2-1; Wandkörper in Zone 2,20 bzw. 5,36 m²; Zone − Wandunion 21,80 m² (Bad) bzw. 53,93 m² (Zimmer), Zone − `wand_zu` 16,20 bzw. 40,49 m² (größte Komponente; alle Teile 19,05 bzw. 47,22 m²; B.13).

**Fachfrage F5 mit Flächenüberschlägen (Kantenlänge × gemessene Tiefe, ohne Eckkorrektur, nur Rennweg):**

| Option | DG2 Bad | DG2 Zimmer | OG1 Zimmer | DG1 Wohnzimmer | Contract |
|---|---|---|---|---|---|
| A Zone (heute) | 24,00 | 59,28 | 16,86 | 83,93 roh | unverändert |
| B lichte Innenfläche, Öffnungen gerade überbrückt | ca. 16,9 (−30 %) | ca. 43,1 (−27 %) | unverändert | unverändert | `polygon_mm` ändert sich |
| C wie B plus Nischen bis Rahmenlinie | ca. 20,3 | ca. 49,9 | ca. 17,8 (+5,7 %) | +1,1 m² (+1,3 %) | `polygon_mm` ändert sich |
| D A bleibt Contract-Polygon, B oder C als Zusatzkontur | 24,00 | 59,28 | 16,86 | 83,93 | unverändert |

**Pseudocode (nur nach Entscheid B/C/D).**
```text
def innenkontur(zone, wand_zu, stempelpunkt, nischen):
    innen = komponente_mit(zone − wand_zu, stempelpunkt)     # Dachschnitt-/Wandband raus
    if nischen:
        innen ∪= nische_bis(oeffnung, tiefe = lokale_wanddicke beidseits)   # familienfrei; sonst Fallback „keine Nische“
    return innen                                              # Option D: als Provider-Attribut wie letzte_aussenbereiche
```
**Blast Radius.** Jede Änderung an `polygon_mm` wirkt auf Stempelabweichung (±10 %, DG2 −27 bis −30 %), Bereinigung Regel 3/4, `tuer_zuordnung._raum_an`, Wohnungen und Leonis' Platzierung (`platzierung/geometry.py` `find_center_diagonal`/`find_center_visual` laut `bereinigung.py:114-119`; bei A liegt Platzierungsfläche im geschnittenen Dachaufbau). Tests: `test_raumlayer.py`, `test_raumlayer_hatch.py`, `test_kaskade.py`, `test_bereinigung.py`, `tests/naht/test_soll_*`. Zonenlage anderer L-Familien (Barawitzka `_815`, Fischamend `A_Raeume`, Herrenholz/Baufeld 810/811) ungemessen. Option D berührt den Contract nicht.

**Prüfstatus:** korrigiert. Rahmenlinie aus Fensterblöcken ist ArchiCAD-spezifisch (Fenster-Layer anderer Familien: Mollgasse „FENSTER“, Barawitzka „320 Fenster“/„325 Dachfenster“, Fischamend „^A_Fenster$“); der DG2-Streifen deckt sich mit der New_255-HATCH (Deutung Außen/Abseite offen).

#### U10 - R-Kontur zerfällt, zonenloser Bereich wird kein Raum

**Mechanismus.** `rest_komponenten.py:122` setzt `kontur = aussenkontur(wk, d_mm=1000)`; `wandkoerper.py:256-262` nimmt die größte Komponente als gefüllten Außenring; `rest_komponenten.py:132-134` blockiert alles außerhalb. Der Kommentar `:120-121` nennt genau diese Gefahr. Die Außenanalyse rechnet dieselbe Gebäudekontur zusätzlich mit d = 1200, simplify(20) und `quad_segs=2`; welcher Parameter den Unterschied macht, ist nicht isoliert.

**Belege.** DG1: Wandunion 31,23 m²; Closing 1000 → 6 größte Teile 73,50 / 1,07 / 0,63 / 0,59 / 0,58 / 0,45 m², größtes ohne Loch; Komponente d = 1200: 196,83 m² (B.13). Freie Fläche 16,94 m², nur 0,63 m² in der R-Kontur; `rest_1..3` schneiden sie mit 0,0 m²; keine New_080-Polylinie deckt den Punkt. R-Kontur (`aussenkontur(wk, d_mm=1000)` wie `rest_komponenten.py:122`, gefüllter Außenring) gegen Gebäudekomponenten (Union von `_komponenten_aus(_wand_geschlossen(wk, 1200))`), alle 7 Pläne in-memory nachgemessen (B.13): UG 253,2/253,5, EG 295,9/295,7, OG1 217,1/218,9, OG2 204,9/216,1, OG3 106,0/191,4, DG1 73,5/196,8, DG2 162,6/179,5 m². Die Aufbruchstelle in DG1 ist nicht lokalisiert (Kandidaten aus Differenz d1200 − d1000: 5,44 m² und 2,00 m²).

**Fix (korrigiert).**
```text
def komponenten_ohne_stempel(plan, wk, tueren, belegte, gebaeude=None):
    kontur = unary_union(gebaeude or aussenkontur_komponenten(wk))   # alle Trakte; einmal rechnen und an erkenne_aussenbereiche weiterreichen
    if aussenkontur(wk, 1000).area < 0.8 * kontur.area:                # ponytail: Diagnose-Knopf
        hinweis('R-Kontur zerfällt bei 1000 mm')
    fuer komp in Komponenten(kontur):
        if kein Stempel in komp and kein Raum-Layer-Polygon in komp:  # allgemein: Gebäudekomponente ohne Raumbeleg
            hinweis('Gebäudekomponente ohne Raumbeleg', komp)         # Stufe 1: nur Hinweis
            # Stufe 2 (erst nach Messung, siehe Blast Radius): komp nicht labeln
            # trifft auf Rennweg den zweiten EG-Grundriss (1,38 km entfernt)
```
Das verschiebt nur die Schwelle von 1000 auf 1200 mm; die robuste Ursache sind die Fensterlücken (U6).

**Test zuerst.** Wandring (400 mm) mit 1320-mm-Fenstern und zonenloser Innenfläche → R-Komponente entsteht.

**Blast Radius.** R-Stufe aller Pläne (neue oder größere `rest_n`), Bereinigung Regel 2, UNBEKANNT-Kennzahl, Wohnungen; gemessen stark OG3/DG1, mittel OG2/OG1/DG2. Die Komponentenregel „ohne Stempel und ohne Raum-Layer-Polygon“ trifft stempelarme Familien. Laut Kommentar `provider.py:80-81` gibt es Pläne ohne Text-Labels (z. B. Mollgasse); dort ist R heute die Raumquelle, und Stufe 2 würde ganze Trakte ohne Raum lassen. Pläne ohne Wand-Layer-Muster (Muthgasse-Familie, `provider.py:65`) sind nicht betroffen, weil die Kaskade dort gar nicht läuft. Deshalb zuerst nur Stufe 1 (Hinweis); Stufe 2 erst nach Messung, auf wie vielen Komponenten je Plan der Hinweis auf Mollgasse, Barawitzka und Fischamend feuert (ungemessen). Tests: `test_rest_komponenten.py` (geschlossene Box, voraussichtlich stabil), `test_bereinigung.py`, `test_kaskade.py`, `tests/naht/test_ueberlappung_riegel.py`, `tests/naht/test_soll_*` (Stiegenhaus-/Schacht-Zählungen); Laufzeit Muthgasse (836 Körper). `test_wandkoerper.py` Z.123 ist nicht betroffen (ruft `aussenkontur` direkt). Behandlung der dann entstehenden Fläche → F9.

**Prüfstatus:** bestätigt; Fix korrigiert.

#### U11 - Bildausschnitt nur aus Raumpolygonen

**Mechanismus.** `raumerkennung_darstellung.py:397-402` bildet `polys` nur aus `modell.raeume`; `:429` ruft `_ausschnitte(polys, f)`; `_bounds` (`:288-293`) = min/max + 6 % der längsten Seite; `_hintergrund` setzt diese Grenzen (`:329-330`). Der Cache (`:431-445`) enthält keine Gebäudekontur.

**Belege.** DG1 Raum-Bbox (12541771, 356206555) - (12557325, 356228980), Rand 1345 mm → Extent x 12540425-12558671, y 356205210-356230325 = Cache-Extent. Außerhalb: Wand 1,77 m² (x 12539089-12540425, y 356213420-356217325), freie Fläche 0,49 m² (von 16,94), offen 0,14 m². DG2 0,05 m² Wand (nicht nachgemessen), übrige Pläne 0.

**Fix.**
```text
_erkennen: cache['komponenten'] = [g.wkb fuer g in ab.komponenten] if ab else []
_ausschnitte(polys, f, zusatz=komponenten):
    Gruppierung über Räume wie heute
    je Gruppe: _bounds(gruppe + [k fuer k in zusatz if k schneidet huelle(gruppe)])   # EG: keine Briefmarke über 1,38 km
Stufe-2-Leser (Z.1196) liest den neuen Schlüssel per .get (alte Caches bleiben lesbar)
```
**Test zuerst.** Kein Package-Test; Prüfbild DG1 vorher/nachher (Westwand sichtbar).

**Blast Radius.** Nur Prüfbilder. `sichtbar()`-Zähler (`:656, 693-758`) und `kennzahlen.json` → `kontext.raeume_ohne_label` (`:492-494`) können sich leicht ändern; Kernkennzahlen nicht. Extent liegt im Cache → Stufe 1 muss neu laufen. `gesamtdarstellung.py`/`uebersicht_karte.py` nicht geprüft.

**Prüfstatus:** bestätigt; Gewichtung korrigiert (Hauptteil des DG1-Problems ist Erkennung, nicht Bild).

#### U12 - ArchiCAD-Türblöcke gehen verloren

**Mechanismus.** `tueren_aus_dxf` liefert auf OG1, DG2, EG und OG3 0 Türen; `provider.py:84-94` nimmt `k.tueroeffnungen`, `:95-97` filtert erneut. `tueren.py:171-181` (`tuer_oeffnungen`) setzt `xy_mm = plan._scale(e.dxf.insert)` und `winkel_grad = rotation`, ohne in den Türblock zu schauen. Alle Rennweg-Türblöcke sind Weltkoordinaten-Blöcke mit gemeinsamem INSERT (12240439, 356160438) und Rotation 0,0 (Haus ~23° gedreht); INSERT 308-318 m von der eigenen Geometrie, im 50-m-Umkreis keine Top-Level-Entity. `kaskade.py:110-115` (`im_planbereich`, Wandkörper-Bbox + 2 m) verwirft sie. `_ist_tuer_block` erkennt „Rectangular Door Opening 27“ nicht (`_DOOR_HINT` `tueren.py:36` ohne DOOR/OPENING). Der Docstring `tueren.py:366-368` (Commit e51d3ee: „11 Zargen-Inserts eines zweiten Plan-Clusters 300 m neben dem Haus“) beschreibt die 11 echten OG3-Türen. Dasselbe Weltkoordinaten-Muster umgeht `rest_komponenten.py:66-75` für `Stair_N` bereits; `_port/parsers/door_blocks.py` löst es für Türen (nicht importiert).

**Belege.**

| Plan | Öffnungen vor Filter | nach Filter | Türblöcke | INSERT in eigener Bbox |
|---|---|---|---|---|
| OG1 | 11 (9 Block, 2 Bogen) | 2 (Bogen) | 12 INSERT, 9 als Tür erkannt | 0 |
| OG3 | 14 (11 Block, 3 Bogen) | 3 (Bogen) | 11 Zargentür_1_Fl | 0 |
| DG1 | 7 (5 Block, 2 Bogen) | 2 (Bogen) | nicht einzeln geprüft | nicht geprüft |
| DG2 | 5 (4 Block, 1 Bogen) | 1 (Bogen) | 4 | 0 |
| EG | 17 (7 Block, 10 Bogen) | 10 (Bogen) | 7 | 0 |
| UG | 17 (15 Block, 2 Bogen) | 2 (Bogen) | nicht einzeln geprüft | nicht geprüft |
| OG2 | 12 (9 Block, 3 Bogen) | 3 (Bogen) | nicht einzeln geprüft | nicht geprüft |

Spalten „vor/nach Filter“ für alle 7 Pläne in-memory nachgezählt (B.6: `tuer_oeffnungen` → `im_planbereich` mit `bounds_aus_wandkoerpern`, wie `kaskade.py:110-115`). In keinem Plan übersteht eine Block-Öffnung den Filter.

OG1-Beispiele (Bbox-Zentren): `Zargentür_1_Fl 10[1]` (12552807, 356217435) in `Wall_9` = Wohnungseingangstür 90/2,20, 420 mm neben `durchgang_22`; `10[4]` (12545085, 356220378) = Bad/Gang 80/2,20; `Rectangular Door Opening 27[11]` (12552407, 356213813) 46 mm neben `durchgang_19`. Gegenproben der Seitenzuordnung (OG1 `tuer_3`, B.15, Varianten von `_gegenprobe.py`): Bbox-Zentrum + Rotation 0 (V1) → `raum_12|raum_12`; Winkel verworfen (V3) → `KEIN_RAUM|raum_12`; Blattlage aus dem Bogen (V5) → `raum_12|KEIN_RAUM` (Probe 300 mm; die Wanddicke 350 mm ist eine Cluster-Angabe ohne Beleg in den Ausgaben, offen); Bogen plus Probe 600 mm (V7) → `tuer_3` `VORRAUM|STIEGENHAUS` richtig, aber die WC-Tür (in V7 `tuer_10`) `STIEGENHAUS|WC` falsch. Die Bbox-Mitte liegt bis zu einer halben Blattbreite im Raum.

**Fix (korrigiert).**
```text
# tueren.tuer_oeffnungen: detect_door_blocks aus _port/parsers/door_blocks.py portieren
fuer ins in tuer_block_inserts(walk):
    if planbereich.contains(ins.insert): wie heute                  # Familien mit INSERT an der Tür unverändert
    elif planbereich.contains(zentrum(geometrie_bbox(ins))):
        s, e = scharnier_und_blattende(ins)                          # _opening_from_block, Kette (a)
        xy, sehne = (mitte(s, e), richtung(s, e)) if s else (zentroid(ins), None)
        breite = blattradius                                         # GEOMETRIE_SCHWENKRADIUS; Nennmass → F18
# _ist_tuer_block: DOOR/OPENING-Tokens nur nach Messung (Muthgasse strict-xfail)
# tuer_zuordnung.ordne_tueren: schrittweise Probe statt fester 300 mm
fuer sgn in (+1, −1):
    fuer d in schritte(50 mm .. lokale_wanddicke + 300 mm):
        p = xy + sgn·d·normale
        if raum_an(p): seite = raum; break
        if not wand_union.covers(p): seite = AUSSEN if not kontur.covers(p) else KEIN_RAUM; break
Docstring im_planbereich korrigieren
```
**Test zuerst.** Synthetischer Weltkoordinaten-Türblock (INSERT weit weg, Bogen in einer 350-mm-Wand zwischen zwei Räumen) → eine Tür mit beiden Raumseiten.

**Blast Radius.** Öffnungen speisen `stempel_flutung` und `komponenten_ohne_stempel` (Siegel `:138-146`, `tuer_n`) → R-Polygone und -Typen ändern sich (Gegenprobe DG2: `rest_4` STIEGENHAUS → SCHACHT, `rest_5` entfällt). Downstream `typisiere_tueren`, `leite_ausgaenge` (stair_exit), `fluchtweg.py:282-296` (Starts an Wohnungseingängen), Anker, `platzierung/bausteine.ist_echte_tuer` (Z.64-69, `TUER_MAX_BREITE_MM` 1300), `flaechen_strategy`. Tests: `test_wandkoerper.py::test_rennweg_tueroeffnungen` (Z.65-68: 11 Blöcke, Breiten {840, 940}), `test_tueren.py` Z.63-110, `test_tuerquellen.py`, `test_stempel_flutung.py` Z.138-145, `test_rest_komponenten.py`, `test_tuer_zuordnung.py` Z.22-43, `tests/naht/test_soll_rennweg.py` (`test_soll_tueren_mit_detail` ≥ 11 heute nur über Durchgänge grün, `test_soll_wohnungs_gruppe`, `test_keine_anker_in_wohnung_privat`, stair_exit, `test_soll_eg_final_exit_via_text`), `test_soll_muthgasse.py` strict-xfail Z.427-445 (XPASS-Gefahr), `test_soll_barawitzka.py` (Variantenfilter). Isoliert eingeführt verschlechtert der Fix OG1 → nur zusammen mit U13 mergen. EG: `bounds_aus_wandkoerpern` spannt beide Grundrisse, der Filter ist dort wirkungslos; welche der 7 verworfenen EG-Öffnungen Phantome sind, ist ungemessen. `Projekte/_eingang/Rennweg_OG3.dxf` (Testplan) ist nicht byte-gleich mit `Projekte/Rennweg/OG3 …` (md5 verschieden, 4 Byte).

**Prüfstatus:** bestätigt (K5 und K6b, alle Linsen); Fix korrigiert (Port-Code statt Neubau, Auslösekriterium „INSERT außerhalb, Geometrie innerhalb Planbereich“, Breite).

#### U13 - Synthetische Durchgänge an durchgehenden Wänden

**Mechanismus.** `tuer_zuordnung.py:133-160`: Paare mit Abstand ≤ 500 mm; `zone = pa.buffer(250) ∩ pb.buffer(250)` (`:137`), `frei = zone − wand_union` (`:138`), Breite = MRR-Langseite (`:143-148`), ≥ 800 mm → Tür (`:149`), unterdrückt nur ≤ 600 mm neben echten Türen (`:153`). Bei Wanddicke < 250 mm reicht die Zone in beide Räume; jeder Innenstreifen hat die Wandlänge als Langseite. Es fehlt jede Prüfung, dass der Teil die Wand quert, jede Mindestfläche und der Ausschluss von Überlappungen.

**Belege.** Synthetisch, Trennwand ohne Lücke: t = 100/200/240 mm → Durchgang 4490/4458/4438 mm; t = 260/300 mm → keiner. Mit bekannter 900-mm-Tür entsteht zusätzlich ein Durchgang 928 mm daneben. OG1 `raum_7` BAD | `raum_8` GANG: Abstand 100 mm, Zone 1,922 m², Wand 0,428 m², Teil 1,449 m² (400 × 4830 mm), davon 94 % in den Räumen; `raum_6` | `raum_7` (Bäder): drei einseitige Streifen (kurz 150 mm, Abstände 100/0). EG KÜCHE | MÜLLRAUM: 3396 × 2 mm, 0,0 m² (Wand ohne Öffnung im Plan). DG2 `raum_7` | `stiegenhaus_2`: Überlappung 2,36 m² → „Öffnung“ 4569 × 3625 mm, 5,43 m²; `raum_7` | `rest_4`: 1420 × 2 mm. Echte Verbindungen mit falscher Breite: OG1 `raum_1` | `raum_2` (Plan: Zargentür 80/2,20; Teil 3457 mm, Schlitz 881 mm), `raum_9` | `raum_10` (Tür 80/2,20; 5711 mm). Echte wandlose Übergänge: `raum_2` | `raum_8` 500 × 1200 mm (Plan 1,20), `raum_8` | `raum_10` 500 × 1450 mm. Durchgänge über Cache-Räume, davon mit Wand ≥ 50 mm dazwischen (Cluster): UG 29/28, EG 31/26, OG1 27/25, OG2 32/29, OG3 26/23, DG1 23/19, DG2 29/23.

**Fix (Kriterium strittig).**
```text
fuer (ra, pa), (rb, pb) mit d = pa.distance(pb) <= 2·_KONTAKT_MM:
    if nutzungsklasse_fuer(ra.raum_typ) == KEIN_RAUM or nutzungsklasse_fuer(rb.raum_typ) == KEIN_RAUM: continue
        # Guard für SCHACHT/LIFT (U3, U4); statische Map, weil Raum.nutzungsklasse hier noch None ist (U19)
    if flaeche(pa ∩ pb) > klein: warnung('Überlappung', ra, rb); nicht als Öffnung werten
    if d < eps:
        stuecke = linien(pa.boundary ∩ pb.buffer(eps)) − wand_union.buffer(eps); breite = laenge(stueck)
    else:
        stuecke = teile((pa.buffer(d+eps) ∩ pb.buffer(d+eps)) − pa − pb − wand_union)   # nur der Wandschlitz
        nur stuecke, die pa UND pb berühren (± eps); breite = Länge entlang der gemeinsamen Grenze
    Splitter (area < breite · 50 mm) verwerfen; Nähe zu echter Tür wie heute
aussen_durchgaenge (:169-224): dasselbe Querungskriterium
```
- Variante Asymmetrie (K5-Linse 1): echte Öffnung hat symmetrische Abstände zu beiden Räumen (100/100, 30/30, 50/50, 0/0), Streifen nicht (100/0, 0/124, 151/0) → `|d_a − d_b| > 0,5 · Raumabstand` verwerfen.
- Variante Schlitz (K5-Linse 2, K6b-Linse 2): siehe Pseudocode; Schwäche: der Schlitz fängt Wandkörper-Lücken (OG1 `raum_11` | `raum_12`: 1834 mm Schlitz bei 80er-Tür).
- Nicht übernehmen: absoluter eps-Filter „Teil berührt beide Räume“; er löscht den echten Eingang OG1 `durchgang_22` (Teil liegt je 100 mm von beiden Räumen; Gegenprobe V2 ergibt 5 Wohnungen).

**Test zuerst.** 100-mm-Wand ohne Lücke → keine Tür; Wand mit 900-mm-Lücke → genau eine Tür mit Breite ≈ 900 mm; `test_durchgang_ohne_tuerblatt` auf Breite ≈ 1200 mm (±100) verschärfen.

**Blast Radius.** Mollgasse +78 Durchgänge (`docs/OFFENE_FRAGEN.md` Z.76-79), Barawitzka `durchgang_63`, Muthgasse strict-xfails Z.474-511/574-590 („Kontaktzonen-Artefakte“), Fischamender BT1 EG 126 Durchgangstüren (`test_wandkoerper.py` Z.147-153), `test_tuer_zuordnung.py` Z.46-60, `tests/platzierung/test_fachpraxis.py` Z.363 (Durchgang 6064 mm), `bausteine.ist_echte_tuer`, Fluchtweg-Graph, stair_exit, Anker, `test_soll_rennweg.py::test_soll_tueren_mit_detail`. Allein ausgeliefert hohes Risiko (ohne echte Türen hätte OG1 nur 2 Verbindungen) → gemeinsam mit U12.

**Prüfstatus:** Mechanismus bestätigt und schärfer (keine Wandlücke nötig); Fix **strittig** (Asymmetrie gegen Schlitz). Planbeobachtung korrigiert: zwischen Zimmer 10,6 und 16,1 liegt eine Zargentür. Fachfrage F10.

#### U14 - Vorraum mit Stiegenhaustür wird Erschließung

**Mechanismus.** `typisiere_tueren` läuft vor der Wohnungsbildung mit statischer Klasse (VORRAUM → WOHNUNG_PRIVAT, `nutzungsklasse.py:23`), daher VR↔STIEGENHAUS „wohnungseingang“ (`tuer_typisierung.py:190-191`), VR↔WC/AR „zimmertuer“ (`:195-196`). `wohnungen.py:48-55`: eine Tür zu STIEGENHAUS, AUSSEN oder Nicht-Privat-Klasse macht GANG/VORRAUM zu ALLGEMEIN_ERSCHLIESSUNG. `:71-80` kippt dessen zimmertuer zu wohnungseingang; `:90-93` verbindet nur privat↔privat; `:95-111` jede Gruppe wird `top_n`. Eine WE-Kante zwischen zwei jetzt allgemeinen Räumen wird nicht zurückgestuft (OG1 `durchgang_22`).

**Belege.** Synthetische Diele (VR mit STGH-Tür, AR/WC/ZIMMER/BAD nur über VR): VR ALLGEMEIN_ERSCHLIESSUNG, alle 5 Türen „wohnungseingang“, 4 Einraum-Wohnungen. OG1 (Rekonstruktion = Cache): `top_1` 9 Räume ohne Eingang, `top_2` = `raum_11` (Eingang `durchgang_20`), `top_3` = `raum_13` (`durchgang_21`), `raum_12` VORRAUM ALLGEMEIN ohne Wohnung. Plan OG1: Zargentür 90/2,20 STGH.1.ST.→VR, 80/2,20 zu WC und AR, Öffnung 1,20/2,20 zur Wohnküche. DG2: `raum_7` VORRAUM 11 Kanten (6 zu `rest_1..4`), `raum_6` „VR/Büro“ zur TERRASSE (Klasse AUSSEN) → beide Erschließung; `durchgang_3/5/11/12` kippen zu WE; Plan: Podest mit Rollstuhl-Wendekreis offen zu VR und VR/Büro, die 4 Türblöcke (80/2,20) liegen an Zimmern/Bad. Keine Top-/Wohnungstexte (OG1 147, DG2 83 Texte). Die Regelrichtung „Stiegenhaustür → Erschließung“ stammt aus 9a5de6f; als Owner-Fallback belegt ist nur die private Richtung (`docs/ENIS_STAND_1_5_0.md` Z.260-261).

**Fix (strittig, blockiert durch F11).**
```text
fuer r in GANG/VORRAUM (iterativ bis Fixpunkt, Reihenfolge raum_id):
    fremd = Tueren(r) zu STIEGENHAUS/ALLGEMEIN_*        # bevorzugt mit Türblatt (U12)
    if len(fremd) == 1
       and kein privater Nachbar ist selbst GANG/VORRAUM mit eigener fremd-Tür
       and ein Nachbar hat Aufenthaltstyp
       and Beleg laut F11 (Stempel VR/Garderobe, TOP-Text, Türbreite):
        r privat; fremde Tür = wohnungseingang
    else:
        r ALLGEMEIN_ERSCHLIESSUNG
nach der Verfeinerung: wohnungseingang zwischen zwei ALLGEMEIN-Seiten → stiegenhaustuer (STGH-Seite) sonst None
```
- Verworfen: Cluster-Vorschlag „n_stgh ≤ 1 und n_privat ≥ 1 → privat“ (bricht `test_zwei_wohnungen_getrennt`; allgemeiner Vorraum vor zwei Wohnungen würde privat).
- Verworfen: K5-Linse-2-Vorschlag „genau eine private Gruppe ohne r“ – K6b-Linse 2 zeigt an der synthetischen Diele 4 Gruppen (ohne VR keine Kante), OG1 bliebe falsch. Topologie allein trennt Diele und Gang nicht.

**Test zuerst.** Synthetische Diele → eine Wohnung mit Eingang an der STGH-Tür; `test_zwei_wohnungen_getrennt` (Z.13-30) bleibt grün; `test_flur_mit_stiegenhaustuer_bleibt_erschliessung` (Z.50-57) wird bewusst neu gefasst.

**Blast Radius.** Falsch privat gewordener allgemeiner Vorraum verliert Notlicht (`flaechen_strategy.py:157-163`) – sicherheitsrelevant. Kandidaten, die kippen können: UG `raum_6/10/12`, EG `raum_6/16`, OG2 `raum_4/5`, OG3 `raum_10`, DG1 `raum_8`. Gang-Anker `provider.py:190-191` ohne Klassenfilter (→ U18). Tests: `test_wohnungen.py` Z.13-57, `tests/naht/test_soll_rennweg.py` Z.57-60, 63-84, 144-155; Wohnungszahlen Barawitzka/Mollgasse (11 bzw. 7 laut 9a5de6f); Kennzahl WE/Wohnung.

**Prüfstatus:** Mechanismus bestätigt (K5, K6b, alle Linsen); Fix **strittig**.

#### U15 - Stempel ohne Kanon-Treffer bleiben außerhalb jeder Wohnung

**Mechanismus.** `stempel_anker.py:149-155` übernimmt ATTRIB ROOM_NAME roh. `raumtyp.py:157-172` → `_port/models/room.py:87-101`: kein Map-Eintrag, kein Token, `endswith('zimmer'|'küche'|'kueche')` falsch → None. `kaskade.py:150-157` lässt den Typ leer; `nutzungsklasse.py:59-61` gibt None; `wohnungen.py:66` nimmt nur WOHNUNG_PRIVAT, `:92` verbindet nur privat↔privat. Türen am Raum werden „unbekannte_kombination“ (Bericht vom 8. Sep., `durchgang_17/18/19` an OG1 `raum_10`).

**Belege.** OG1 `raum_10` 73,06 m²: Rohbytes „W o h n k c h e“ in BLOCK_RECORD „Wohnkche__10“, ATTDEF und ATTRIB; `$ACADVER` AC1032, `$DWGCODEPAGE` ANSI_1252; dieselbe Datei trägt korrekte Umlaute („NACHBARGEBÄUDE“, „New_010 Aussenwände“ 423×, „DÄMMSTOFF__POLYSTYROL_EPS“ 28×). EG und OG3 tragen „Wohnküche“ als UTF-8 und sind KÜCHE (`raum_1` 45,60 bzw. 38,35 m², `top_1`). `raumtyp_flags`: „Wohnkche“ → None, „Wohnküche“/„Wohnkueche“/„v.Küche“ → („KÜCHE“, False, False). OG2 `raum_2` „Wohnbereich“ 59,53 m² (Map kennt „wohnraum“, `room.py:51`), DG1 `raum_7` „TV Raum“ 15,91 m². Korpus: „Wohnkche“ 1× in 298 Stempelnamen (63 `raeume.json`); in 76 DXF trifft `[A-Za-zÄÖÜäöüß]{3,}(kche|kuche|kueche)` nur „Wohnkche“.

**Fix (korrigiert: Normalisierung vor allen Stufen; zwei Commits: S6a Schreibvarianten, S6b Synonyme).**
```text
# [S6a] raumtyp.raumtyp_flags
text = unicodedata.normalize('NFC', text)
ergebnis = heutige Kette(text)                                   # exakter Durchlauf zuerst
if ergebnis is None:
    varianten(key) = {key, ü→ue, ü→u, ü→''} (analog ä, ö) für Schlüssel >= 4 Buchstaben
                     in _EXTRA_OVERRIDE, Kompositum-Köpfen, _EXTRA_DIRECT
    Override-Varianten zuerst ('Waschkche' → WASCHKÜCHE, nicht KÜCHE)
    Kopf-Toleranz nur als Kompositum mit Stamm >= 3 Buchstaben
    Hinweis 'Typ über Schreibvariante: <name> → <typ>'
# [S6b] Synonyme; Zieltyp WOHNZIMMER ist Default zur Bestätigung durch F15 (WOHNZIMMER oder ZIMMER)
_EXTRA_LABELS: 'wohnbereich' (token-exakt) → WOHNZIMMER; Tokenpaar {'tv','raum'} oder 'tvraum' → WOHNZIMMER
```
Nicht übernehmen: Toleranz nur in `classify_room` (der Override `raumtyp.py:159-162` prüft vorher exakt; „Waschkuche“ würde KÜCHE/WOHNUNG_PRIVAT statt communal).

**Test zuerst.** S6a: „Wohnkche“ → KÜCHE; „Waschkche“/„Waschkuche“ → WASCHKÜCHE; „Kche“/„Kuchen“ → None. S6b (Default bis F15): „Wohnbereich“, „TV Raum“, „TV-Raum“ → WOHNZIMMER; „Eingangsbereich“, „Außenbereich“, „TV“ → None.

**Blast Radius.** `_typ()` entscheidet auch, ob lose Texte neben einer m²-Zahl (`stempel_anker.py:230-231`) und Blockname-Stempel ohne m² (`:189-190`) Stempel werden → vor Einbau Textdump über alle Projekt-DXF auf Endungen „kche/kuche/kueche“ und die zwei Synonyme (gemessen sind nur Stempelnamen). OG1 `raum_10` → KÜCHE: schließt über `durchgang_17/18` an `top_1` an, `durchgang_19` wird Wohnungseingang (abgeleitet aus Türtabelle vom 8. Sep., nicht gemessen); `top_2`/`top_3` bleiben (U14). OG2 `raum_2`, DG1 `raum_7` → WOHNUNG_PRIVAT; heute 0 Leuchten in untypisierten Räumen, also keine Leuchtenänderung. Kein neuer Kanon-Typ → `test_vokabular_doku`, `test_lb_raumtyp_naht`, `test_regel_deckung`, `test_nutzungsklasse` unberührt; `test_raumtyp.py` Z.137-145 erweitern. Brücke für weiterhin untypisierte Räume → F13 (Risiko EG: „Geschäftslokal 1“ grenzt über Schiebetür an „v.Küche“).

**Prüfstatus:** bestätigt (K5, K6a, K6b); Fix korrigiert (Ort der Toleranz). S-B1-Regression widerlegt (Abschnitt 3). Zieltyp der Synonyme (S6b) nicht entschieden → F15.

#### U16 - Jede private Komponente wird Wohnung

**Mechanismus.** `nutzungsklasse.py:19-22`: KÜCHE, WC, ABSTELLRAUM (auch BAD) statisch WOHNUNG_PRIVAT, ohne Kontext. `wohnungen.py:95-111` vergibt `top_n` für jede Union-Find-Gruppe ohne Mindestkriterium.

**Belege.** EG `top_2` = `raum_11` KÜCHE 9,27 m² („v.Küche“): Türen `durchgang_16` 860 mm zu „Geschäftslokal 1“ (brandschutztuer), `durchgang_18` 880 mm zu TREPPENHAUS (wohnungseingang), Splitter `durchgang_17` 3396 × 2 mm zu MÜLLRAUM; in allen Tür-Gegenproben V1-V8 unverändert. UG `top_1..4`: WC 6,17 / 1,48 / 1,48 m², ABSTELLRAUM 1,06 m² (Personalbereich). OG1 `top_2` AR 4,52, `top_3` WC 3,50 (Ursache U14). OG2 `top_2` = ZIMMER 22,22 m² (nicht erklärt; ein Aufenthaltsraum-Kriterium fängt ihn nicht).

**Fix (blockiert durch F12).**
```text
nach Union-Find, je Gruppe:
    if alle Typen in {KÜCHE, BAD, WC, ABSTELLRAUM, VORRAUM}:
        keine wohnung_id; Hinweis 'privatklasse_ohne_wohnungskontext'
        nutzungsklasse gemäß F12 (None | ALLGEMEIN_NEBENRAUM | WOHNUNG_PRIVAT)
    elif Gruppe = ein einzelnes ZIMMER:
        Hinweis 'einraum_wohnung_verdaechtig'
```
**Test zuerst.** Synthetisch: WC mit Tür nur ins Stiegenhaus → keine Wohnung.

**Blast Radius.** `flaechen_strategy.py:161-165` filtert nach Nutzungsklasse, nicht nach `wohnung_id` → nur die ID zu entziehen ändert die Platzierung nicht; eine andere Klasse ändert Notlicht. Kennzahl „wohnungen“ (`gesamtdarstellung.py:443`), `test_soll_rennweg.py` Z.63-84, abhängig vom Geschäftslokal-Entscheid (F14).

**Prüfstatus:** bestätigt (Sicherheit mittel); Klassenfrage ergänzt (K5-Linse 2).

#### U17 - Geschäftslokal ohne Kanon

**Mechanismus.** `raumtyp_flags` liefert für „GESCHÄFTLOKAL“ (ohne Fugen-s), „Geschäftslokal 1“ und „GESCHÄFTSLOKAL“ None; VOKABULAR §1, `nutzungsklasse._MAP`, `lb_extraktion.yaml` (Z.318-322) und der Contract (`raum_modell.py:22-25`) kennen keine Nichtwohn-Nutzungseinheit. `oib_gate.verkehr_scope` (Z.193-212) liefert nie „anwendbar“. Offen seit 2026-09-08 (`docs/OFFENE_FRAGEN.md` Z.443-448, `docs/COORDINATION.md` Z.400: „blockiert“).

**Belege.** EG `raum_12` 111,03 m², `raum_10` 29,11 m², beide ohne Typ und Klasse, Polygone = Stempelfläche. Plan: dichte Tisch-/Stuhl-Möblierung, anschließend `raum_17` „HOF/Terrasse“ 29,57 m² mit runden Tischen, mehrere Türen in der Straßenfassade; „Geschäftslokal 1“ mit langem Tresen-/Tischrechteck und drei Straßentüren. Türen (Bericht 8. Sep.): `tuer_9` `raum_12`↔TERRASSE unbekannte_kombination, `durchgang_19/20` zu TREPPENHAUS unbekannte_kombination, `durchgang_21` zu GANG `raum_16` hauseingang über Text „TÜRSCHLIESSER“ (Text-Regel greift nur bei leerer Rolle, `tuer_typisierung.py:205-206`). Korpus: 4 Stempel auf 2 Plänen (Rennweg EG mit Polygon; Mollgasse EG 51,66/56,33 m², `kein_polygon`). Norm im Repo: OIB-RL2 Tabelle 6 Zeile 4 (Verkaufsstätten, erst > 200 m² Verkaufsfläche) bzw. 5.1 (Schank-/Speisewirtschaft, Verabreichungsplätze); AStV-Pfad; `projekt_kontext.py` Z.25-45 führt die Nutzungsart nur projektweit; R 12-2 Fußnote c (gemischte Nutzung).

**Fix.** Keine Code-Entscheidung vor F14. Nach Entscheid in einem PR: VOKABULAR §1, `raumtyp._EXTRA_DIRECT` (inklusive der belegten Schreibweise „geschäftlokal“ als explizite Variante), `nutzungsklasse._MAP`, `lb_extraktion.yaml`, `regel_deckung.yaml` (Status zunächst „offen“, Owner Enis), gegebenenfalls Contract-Literal mit Versionssprung; Tür-Regeln sind Teil der Fachfrage.

**Blast Radius.** Vier Guards (`tests/contract/test_vokabular_doku.py`, `test_lb_raumtyp_naht.py`, `tests/naht/test_regel_deckung.py`, `tests/raumerkennung/test_nutzungsklasse.py`). `tests/naht/test_soll_rennweg.py` läuft über `Projekte/_eingang/Rennweg_EG.dxf` (byte-identisch mit dem EG, sha256 7044ff3b…): `test_soll_eg_wege_enden_am_final_exit` gefährdet bei neuen Wohnungseingängen, strict-xfail `test_soll_eg_90_prozent_tueren_typisiert` (Ist 54 %) kann kippen. Eine neue Klassen-Regel an `raum_12` überschreibt die Text-Regel an `durchgang_21`; Option „ZIMMER“ macht `tuer_9` zur balkontuer ohne Notausgang.

**Prüfstatus:** bestätigt; Fachfrage ergänzt (Option E, Norm-Schwellen, Testbezug).

#### U18 - Wohnungsflure behalten Fluchtweg-/communal-Flags

**Mechanismus.** `raumtyp.py:28-30`: STAIRCASE, CORRIDOR, ENTRANCE_HALL → (Typ, True, True). `kaskade.py:150-159` schreibt die Flags aus dem Stempeltyp (OR-verknüpft). `wohnungen.py:53-55` setzt nur die Nutzungsklasse. `provider.py:186-191` erzeugt Gang-Anker für jeden GANG; `gang_anker.py:102-112` prüft keine Klasse. `flaechen_strategy.py:161-165` überspringt WOHNUNG_PRIVAT nur ohne `ist_fluchtweg`/`ist_communal` → Flächenleuchte im Wohnungsflur. `gang_strategy.py:94-98` setzt RZ in jeden Korridor ohne Klassenfilter (`docs/COORDINATION.md` Z.400 (5): offen in Leonis' Lane).

**Belege.** OG1 Kaskade in-memory: `raum_8` GANG 6,48 m² fluchtweg/communal True (später WOHNUNG_PRIVAT `top_1`); VORRAUM `raum_4` 3,4 m², `raum_5` 2,59 m², `raum_12` 10,94 m² fluchtweg True. Widerspruch zu `tests/naht/test_soll_rennweg.py::test_keine_anker_in_wohnung_privat` (Z.144-156) und `::test_soll_keine_leuchten_in_wohnung_privat` (Z.63-84), beide nur auf OG3. `normwissen/data/raumtyp_regeln.yaml` Z.68-72: GANG nur mit `ist_fluchtweg: true`. Ob `raum_8` heute tatsächlich Anker/RZ bekommt, ist nur aus dem Code abgeleitet (Platzierung nicht ausgeführt).

**Fix.**
```text
# wohnungen.bilde_wohnungen, nach _verfeinere_gang_privat
fuer r in GANG/VORRAUM:
    r.ist_communal = (r.nutzungsklasse != 'WOHNUNG_PRIVAT')
    r.ist_fluchtweg = gemäß F16 (A: = r.ist_communal; B: unverändert)
# provider.py:190-191
if r.raum_typ == 'GANG' and r.nutzungsklasse != 'WOHNUNG_PRIVAT': anker += anker_fuer_gang(…)
```
**Test zuerst.** Wohnung mit GANG → keine Gang-Anker, `ist_communal` False; allgemeiner GANG → Anker wie heute.

**Blast Radius.** Contract-Werte aller Wohnungsflure und -vorräume in allen Plänen; Norm-Lookup GANG (`raumtyp_regeln.yaml`); `test_gang_anker.py`; `test_keine_anker_in_wohnung_privat` sollte auf weitere Pläne ausgedehnt werden. `gang_strategy` gehört Leonis. Hängt an U14 (welche Flure privat sind).

**Prüfstatus:** korrigiert (Code-Anteil von K6b-Linse 2 ergänzt; Rückfrage OG1-3 bleibt).

#### U19 - Folgeschaden: falsche AUSSEN-Türen

**Mechanismus.** `provider.py:117`: `kontur = aussen.gedeckt()`. `tuer_zuordnung.py:106-115`: Probepunkt nicht in Raum und nicht in kontur → AUSSEN → ZIMMER×AUSSEN = balkontuer (`tuer_typisierung.py:187-189`). `aussen_durchgaenge` (`tuer_zuordnung.py:185-186`): Ring `kontur.buffer(2000) − kontur` auch im Gebäude, nur ALLGEMEIN-Räume (`:190-191`), 800 < Breite ≤ 2600 (`:211`) → `oeffnung_aussenwand`; > 1400 mm setzt `ist_notausgang` (`tuer_typisierung.py:128-132`). OG/DG sind vor final_exit geschützt (`ausgaenge.py:60-61, 100-112`, `geschoss.py:247-249`: 1OG/2OG/3OG/DG).

**Belege (Emulation mit Cache-Räumen; B.16).**

| Plan | Öffnung | Breite | Lage | Mechanismus |
|---|---|---|---|---|
| DG1 | `aussenoeffnung` an `rest_2` STIEGENHAUS (12549812, 356221732) | 2590 mm, `ist_notausgang` | 15 mm außerhalb der Komponenten | U6 (bleibt nach Loch-Test) |
| OG1 | an `rest_1` STIEGENHAUS (12550441, 356221471) | 1336 mm | in Komponenten, 162 mm vom Rand | U6 |
| OG3 | an `rest_3` | 2473 mm (`ist_notausgang`) und 822 mm | 5221/5252 mm vom Rand | U7 (entfällt mit Loch-Test) |
| DG2 | an `rest_3` | 1413 mm | in Komponenten, 286 mm | nur in der K4-Prüfung mit Cache-Nutzungsklasse, dort in beiden Kontur-Varianten; in der Türkette ohne Nutzungsklasse (`_aussen_folgen.py DG2`) keine Außenöffnung (korrigiert, vorher „in allen Varianten“) |

Balkontüren an Zimmern: DG1 `tuer_2` (`raum_3`), OG1 `tuer_2` (`raum_1`), OG2 `tuer_3` (`raum_8`), OG3 `tuer_1` (`raum_4`). Leser von `ist_notausgang`: `platzierung/gang_strategy.py:66`, `anker_strategy.py:166`, `communal_stgh_strategy.py:82-87`, `hauptengine/render/dxf_renderer.py:542`; `fachpraxis.aussen_tuer_rz` (Z.387-411) setzt RZ an communal→AUSSEN ohne Geschossbezug; Rest-STIEGENHAUS trägt `ist_communal` = True (`rest_komponenten.py:92-93`). Wirkung auf Platzierung ungemessen.

**Vorbehalt.** Die Cluster-Simulation (K4) nutzte Räume mit fertiger Nutzungsklasse. Im echten Lauf sehen `aussen_durchgaenge` und `typisiere_tueren` den statischen Default (Nutzungsklasse wird erst in `wohnungen.py:54, 63` bzw. `lift_erkennung.py:176` gesetzt). Emulations-Kandidaten wie DG1 `raum_8` VORRAUM (2095/2357 mm) können im echten Lauf nicht entstehen; die Aussage „Wohnungen durch Außen unverändert“ ist daher nicht belastbar.

**Fix.** Ursache über U6, U7, U8. Der defensive Ring-Fix `ring − komponenten.buffer(−400)` wird verworfen: gemessen identisch zum Loch-Test und wirkungslos für DG1 `rest_2` und OG1 `rest_1`.

**Test zuerst.** Nach S1/S2 Tür-Kette in-memory mit `nutzungsklasse = None` wiederholen (Zustand vor `bilde_wohnungen`).

**Prüfstatus:** korrigiert (Mechanismus je Fall getrennt; Simulationsvorbehalt).

#### U20 - Scheinbilder in der Wohnungsdarstellung

**Mechanismus.** `raumerkennung_darstellung.py:715`: `unary_union(ps).buffer(200).buffer(-200)`; `:719-722` zeichnet nur Außenringe ohne Füllung; `:723-725` setzt das Label über den höchsten Eckpunkt.

**Belege.** DG2 `top_1` = `raum_1` VORRAUM 10,84, `raum_2` ZIMMER 59,28, `raum_4` BAD 24,00, `raum_5` ZIMMER 19,60 (Summe 113,72 m²); Umriss 1 Teil, 0 Löcher, 115,23 m²; keine fremde Raummitte im Umriss; `stiegenhaus_2` liegt mit 2,27 m² (14 %) darin – das kommt aus der Polygon-Überlappung `raum_5` ∩ `stiegenhaus_2` = 2,26 m² (U1), der Puffer trägt ca. 0,01 m² bei. OG1 `top_2`-Label steht im VR (400 mm über der AR-Oberkante); gleiches Muster OG2 `top_2` (über `raum_5` VORRAUM) und UG `top_4` (über `raum_6`). EG `top_1` hat ein nicht gezeichnetes, leeres Loch.

**Fix.**
```text
je Wohnung: u = union.buffer(200).buffer(−200)
    Fläche leicht tönen (alpha), Außen- und Innenringe zeichnen
    label_xy = u.representative_point()        # wie gesamtdarstellung.py Z.312-319
```
**Blast Radius.** Nur Prüfbilder (`--nur-zeichnen` genügt); `gesamtdarstellung.py` zeichnet ebenfalls nur Außenringe.

**Prüfstatus:** bestätigt; S-H4-Teilaussage „DG2 ganzes Geschoss inkl. Stiegenhaus und Lift als top_1“ widerlegt.

---

## 3. Selmans Ergänzungen

### A1 - S-H1 Treppen-Block-Extents als Stiegenhaus-Polygon: **teilweise**

| Fall | Polygon aus Treppen-Bbox? | Typ aus Treppen-Bbox? | Ursache |
|---|---|---|---|
| DG2 `stiegenhaus_2` 15,86 m² („oranges Quadrat“) | ja (Achs-Bbox `Stair_2`, IoU 1,0) | ja | U1 - bestätigt |
| EG `rest_2` 0,96 m², OG1 `rest_2` 1,00 m² („Stiegenhaus 1,0“), UG `rest_3`, DG1 `rest_3`, DG2 `rest_4` | nein (Raster, 60-74 Ecken, Treppen-Randanteil ≤ 0,022) | ja (Bbox-Zentrum der U-Treppe im Liftschacht, Abstand 0-210 mm) | U2 |
| DG2 `rest_2` 1,16 m² („Stiegenhaus 1,2“, DBA-Schacht) | nein (Raster, 89 Ecken) | ja (`Stair_1`-Zentrum 726 mm) | U2 |
| DG2 `rest_1` 3,99 m² („Stiegenhaus 4,0“) | nein (Raster, 95 Ecken) | Marker 0 mm, aber echte Treppe (51,5 m Stufenlinien) | Polygon-Hypothese widerlegt; Typ Fachfrage F2 |

Zusätzlich latent: `stiege_rechtecke` nimmt Zonenstempel-Blöcke (UG „Stiegenhaus__16“, EG „Stiegenhaus__7“, „TREPPENHAUS__14“) als Treppen-Rechtecke (heute ohne Wirkung). Belege: M1, U1, U2.

### A2 - S-H2 Außenbereich flutet durch Fenster: **teilweise**

- **Bestätigt:** Die Außenfläche tritt an Fensterwänden ein: OG1 (Dreieck vom Balkon über Zimmer 16,9/10,6/16,1), OG2 Nordzimmer, DG1 Nordzimmer, OG3 Nordzimmer, DG2 Terrassenseite → U6. Präzisiert: Die Wandmaske liest die Fensterblöcke durchaus, bekommt aus ihnen aber mangels HATCH keinen Körper; zusätzlich lecken dünn schraffierte Wände auch an schraffierten Fenstern (OG1 `Wall_5`), und Fenstertüren ≥ 2,4 m werden vom Closing (d = 1200 mm) nie versiegelt.
- **Anderer Mechanismus:** DG1 Wohnzimmer sowie OG3 Wohnküche und Hobbyraum sind knapp versiegelte Löcher 193 mm vor dem Hüllrand → U7.
- **Widerlegt für DG2 Straßenfront:** Die Dachfenster sind in der geschlossenen Wand ab −800 mm dicht; das Band entsteht, weil die Zone über das Dachschnitt-Band hinaus reicht (U9) und die Außenanalyse Zonen nicht abzieht (U8).
- **Widerlegt „erklärt die abgeschnittenen Räume an Fensterseiten“:** Die Raumpolygone (Quelle L) entstehen vor der Außenanalyse und werden von ihr nicht verändert. Zimmer 16,9, Bad 24, Zimmer 59,3 enden an der Zonenlinie (U9, Fachfrage); das DG1-Wohnzimmer fehlt, weil die TV-Ecke keine Zone hat und die R-Stufe sie nicht sieht (U10), plus Bildausschnitt (U11).

### A3 - S-H3 Schacht-Regel greift falsch und nicht richtig: **teilweise**

| Teilhypothese | Urteil | Beleg | Ursache |
|---|---|---|---|
| „Schacht 1,4 m²“ DG2 ist eine rote Fensterblock-Kontur | widerlegt | Keine Farbregel im Code; 0 rote geschlossene Konturen in Blöcken; SCHACHT allein über „< 3 m² und türlos“; die rote unregelmäßige Kontur im Bild ist das SCHACHT-Overlay (`raumerkennung_darstellung.py:112, 132`) | U5 |
| Echte Schächte innen (rot, DDB/BDB, FEUERFESTER_STEIN) werden nicht ausgestanzt | bestätigt | M3: 34 Räume mit roter Schachtfläche; 0 LIFT_SCHACHT-Buchungen in DG1/DG2/OG1 | U3, U4 |
| Rote Entities und Texte in verschachtelten Blöcken werden nicht aufgelöst | widerlegt | Alle Schacht-Texte (außer Zonenstempel „DBA Raum“) und alle 216 roten Konturen < 3 m² liegen im Modelspace | - |
| Erkannter Schacht wird ausgestanzt oder liegt daneben | Code stanzt aus (Regel 1, `bereinigung.py:266-269`, Schlitz-Kodierung), aber es entsteht nie ein Schacht-Polygon in einer Zone; R-Schächte liegen per Konstruktion daneben; nach der Kaskade angehängte Polygone sehen Regel 1 nie | R ∩ L = 0 mm² in DG1/DG2; DG2 `stiegenhaus_2` enthält Marker-Zellen | U3 |

### A4 - S-H4 Wohnungsbildung kaputt: **bestätigt, eine Teilaussage widerlegt**

- **OG1** (`top_3` nur WC, `top_2` nur AR, Wohnküche 73,1 m² in keiner Wohnung): U12 (echte Türen verworfen) → U13 (Scheinkanten) → U14 (Vorraum mit Wohnungseingangstür wird Erschließung) → U15 („Wohnkche“ untypisiert). „`top_2` Vorraum + Abstellraum“: Daten = nur AR; das Label steht über dem VR (U20).
- **EG** (`top_2` nur Küche 9,3): U16 (statische Privatklasse, jede Komponente = Wohnung).
- **DG2** („ganzes Geschoss inkl. Stiegenhaus und Lift als top_1“): **widerlegt**. Daten 4 Räume (113,72 m²), Umriss 115,23 m²; einzige Überdeckung eines Erschließungsraums 2,27 m² von `stiegenhaus_2`, verursacht durch die Polygon-Überlappung aus U1; kein Lift, kein VR 15,2 im Umriss (U20). Die 10 Wohnungseingänge von `top_1` stammen aus U13 und U14.
- **Unterschied 18 zu 10 Eingängen (DG2):** `tuer_typen.wohnungseingang` zählt alle Türen mit dieser Rolle. `Wohnung.eingangs_tuer_ids` (`wohnungen.py:104-106`) nimmt nur die Türen, die an einen Raum der Wohnung grenzen. In der in-memory Türkette (B.7, Abgleich `wohnung_id` mit dem Cache identisch) haben 18 Türen die Rolle; 10 grenzen an `top_1` (`durchgang_3/5/6/7/11/12/13/14/15/17`). Die übrigen 8 (`durchgang_19` bis `_26`) liegen zwischen zwei ALLGEMEIN_ERSCHLIESSUNG-Räumen (`raum_6`/`raum_7` VORRAUM gegen `rest_1..4` STIEGENHAUS), gehören also zu keiner Wohnung. Sie entstehen, wenn der Vorraum nach der Rollenvergabe zur Erschließung kippt (U14) und die Rolle nicht zurückgestuft wird.
- **„30 von 75 Plänen mit Wohnungseingang-Missverhältnis“:** nachgezählt in M5 (Abschnitt 4), Bestand 1e642ad. 30 und 75 sind reproduziert: 75 = 83 Dateien − 8 Fehler-Stubs ohne `tuer_typen` (`docs/HANDOFF_SELMAN.md` Z.71: „75 ausgewertet, 8 nicht auswertbar“). Das Verhältnis ist nur auf 52 Dateien berechenbar; 23 der 75 haben kein Feld `wohnungseingang` (B.8). Rennweg ist selbst betroffen (Bestand 1e642ad, `Projekte/_ergebnis/<PLAN> - Rennweg …/kennzahlen.json`, `tuer_typen.wohnungseingang` / `wohnungen`): DG2 18/1, DG1 4/1, EG 7/2; unter der Schwelle OG1 3/3, OG2 5/2, OG3 5/2, UG 4/4. Für DG2, OG1 und EG ist die Wurzel U12-U14 per Türkette belegt (B.7), für DG1/OG2/OG3/UG nicht rekonstruiert. Fischamend (21000 EG BT2: 42/1; 11020 2.OG BT1: 82/2) ist nur als Kennzahl gezählt, die Ursache ist dort nicht untersucht.

### B1 - Wohnküche (OG1): **keine Regression**

- Der ArchiCAD-Zonenname lautet in der DXF wörtlich „Wohnkche“ (Rohbytes `W o h n k c h e _ _ 1 0`; BLOCK_RECORD, ATTDEF ROOM_NAME, ATTRIB). AC1032 (UTF-8-DXF), `$DWGCODEPAGE` ANSI_1252; dieselbe Datei trägt korrekte Umlaute. EG und OG3 tragen „Wohnküche“ und sind KÜCHE.
- `git log --all -S 'Wohnkche'` trifft nur f97d1e1 (Ergebnis) und 0204ee9 (Assets); `git log -S 'Wohnk' -- src/notbeleuchtung/raumerkennung/` ist leer; die OG1-DXF existiert nur in 0204ee9.
- Die Substring-Version des Klassifizierers vor 54b3ddc (221e866) hätte „wohnkche“ ebenfalls nicht getroffen („küche“ ist kein Teilstring).
- Bericht vom 8. Sep. (`Projekte/_ergebnis_alle/OG1 …/bericht.md` Z.18): „Wohnkche | —“; `kennzahlen.json` in f97d1e1 (Lauf 538d8d8): UNBEKANNT 1, 3 Wohnungen. `BERICHT.md` Z.69 vermerkt den Schreibfehler.
- Fläche: MTEXT „73,06 m²“, Cache 73,0645, Bild 73,1; die genannten 75,1 m² sind nicht reproduzierbar.
- Folgerung: Code-Lücke (keine Toleranz für fehlende Umlaute in Kompositum-Köpfen) → U15, Owner Selman.

### B2 - Geschäftslokal (EG 111,0 und 29,1 m²): **Fachfrage F14** (U17)

Nicht entschieden. Offen seit 2026-09-08, Adressaten Enis und Leonis.

### C - Fachregel „Außenbereich ist nur, was außerhalb des bewohnten Bereichs liegt“ gegen die heutige Bestimmung

| Regel-Element | Heutige Bestimmung | Datei:Zeile | Verletzt in (Output 511ad36) |
|---|---|---|---|
| Wohnzimmer, Zimmer, Bad, WC, AR, VR, Stiegenhaus nie Außen | Außenanalyse ohne Raum-/Stempel-/Möbelwissen; frei = Hülle − geschlossene Wand; offen bei Randabstand < 250 mm und Hals an der Kante | `aussenbereich.py:227-271`; `provider.py:114` | M2: 20 Innenräume, 304,14 m² Schnitt (DG1 7, OG3 4, OG1 3, DG2 4, OG2 2) |
| Raum mit Stempel ist innen | Stempel werden nicht übergeben | `provider.py:114` | 19 der 20 betroffenen Räume tragen einen Stempel (Ausnahme DG2 `stiegenhaus_2`, Randstreifen aus U1) |
| Raum mit Möbeln/Sanitär ist innen | kein Innen-Indiz; die Layer „New_065 Möbel Einrichtung“ und „New_060 Möbel Einbau“ kennt der Code nur als Nicht-Wand (`_NEGATIV_LAYER`, `wandkoerper.py:43-47`) | `aussenbereich.py:101-126` (nur Außen-Indizien) | 12 betroffene Räume mit Möbel/Sanitär per Einfügepunkt, 15 per Block-Mitte |
| Terrasse, Balkon, Loggia nie Außen | Nutzungsklasse AUSSEN; geometrisch offen, wenn in der konvexen Hülle | `nutzungsklasse.py:41-43`; `raumtyp.py:81` (Loggia → BALKON); `aussenbereich.py:240-245` | OG1 `raum_15`, OG2 `raum_13`/`raum_14`, DG2 `raum_3` (35,15 m²); auskragende Balkone DG1/OG3 `raum_9` nie (0,0 m² in der Hülle) - inkonsistent |
| Außen = außerhalb der Fenster, wo kein Balkon/Terrasse/Loggia | Fensterlücken ohne Wandkörper, dickenabhängiges Closing | `wandkoerper.py:164-173`; `aussenbereich.py:129-138` | U6 (OG1, OG2, DG1, OG3, DG2) |
| Innenraum ohne Zone/Stempel (DG1 TV-Ecke) | nicht erfasst | - | DG1: 16,09 m² der freien Fläche liegen in offen |

„AUSSEN“ hat im Code drei Bedeutungen: geometrischer Außenbereich (`aussenbereich.offen/geschlossen`), Nutzungsklasse (Contract-Literal, `raum_modell.py:22-25`) und Tür-Seiten-Sentinel (`tuer_zuordnung.py:28`); `tuer_typisierung._klasse` (Z.90-96) behandelt Nutzungsklasse und Sentinel gleich. Widerspruch im Code: Kommentar `tuer_typisierung.py:149-152` („fail closed, fällt auch im EG heraus“) gegen `:157, 179` (`not eg`: EG-Terrassentür ohne Beleg als hauseingang/final_exit). → Fachfrage F6.

---

## 4. Vorher-Messung (D)

> **Geltungsbereich (Entscheid Selman, 2026-09-15):** Die Vorher-Zahlen zu D (M1-M4) gelten **ausschließlich für die 7 Rennweg-Pläne**, die einzigen Pläne mit Cache in `Projekte/_ergebnis_raumerkennung/` (Output 511ad36). Die übrigen Pläne werden nach der Freigabe der Fixes mit dem regulären Lauf gemessen, dann gleich als Vorher/Nachher. M5 ist keine D-Vorher-Zahl, sondern eine Bestandszählung (1e642ad) zum Befund HANDOFF 4.1.

**Umfang (S-D).** Selman verlangt eine Vorher-Messung über alle Pläne. Es gibt zwei Bestände:
1. Caches mit Raumpolygonen, Stempeln und Außenflächen liegen nur unter `Projekte/_ergebnis_raumerkennung/`, und nur für die 7 Rennweg-Pläne (Output 511ad36). M1-M4 brauchen diese Caches. Für andere Familien sind M1-M3 **ohne Cache nicht messbar**. Caches zu erzeugen hieße, Stufe 1 laufen zu lassen, und das ist in dieser Analyse ausgeschlossen.
2. `kennzahlen.json` der Gesamtdarstellung gibt es für 83 Pläne (Bestand 1e642ad). Sie enthalten Tür- und Wohnungszahlen, aber keine Geometrie. Daraus lässt sich ohne Pipeline nur das Verhältnis Wohnungseingang je Wohnung zählen (M5).

Entschieden (F19, Selman 2026-09-15): vor den Slices keine weiteren Caches; andere Pläne nach Fix-Freigabe im regulären Lauf als Vorher/Nachher.

Grundmenge: alle `Projekte/_ergebnis_raumerkennung/**/_cache.pkl` (heute 7 Rennweg-Pläne, alle `kennzahlen.json` mit commit 511ad36, DXF-sha256 in allen Plänen gleich `kennzahlen.json`). Die Skripte lesen nur Cache, `kennzahlen.json` und DXF (in-memory `lade_dxf`, M2 zusätzlich `finde_wandkoerper`); Quelltext und Aufruf in Anhang A. **Nachher-Messung:** nach jedem Slice die Caches mit `scripts/analyse/raumerkennung_darstellung.py` neu erzeugen (Stufe 1), dann dieselben Skripte unverändert mit neuer Ausgabedatei aufrufen. Jede Messung wurde von einem zweiten Agenten auf anderem Weg nachgerechnet.

### M1 - Achsparallele STIEGENHAUS-Polygone in gedrehten Plänen (nur 7 Rennweg-Pläne)

**Definition.** Rotation je Plan und je Raum-Cluster aus Raumkanten (Winkel mod 90, 0,5°-Bins, Modus; „gedreht“ bei > 3° Abstand zu 0/90). Hauptwert: STIEGENHAUS mit achsparalleler konvexer Hülle (Kantenanteil ≥ 0,90 innerhalb ±1°) im gedrehten Plan. Vorgabe-Zahl: Kantenanteil des Polygons selbst ≥ 0,90. `aus_treppen_bbox`: Randanteil ≥ 0,5 an einem `stiege_rechtecke`-Rechteck. Zusatz „klein ohne Stempel“: STIEGENHAUS < 2 m² ohne Stempel; Lift ≤ 300 mm; Schacht-Text ≤ 500 mm (Regex nach Port-Liste).

| Plan | Rotation (Raumkanten) | STIEGENHAUS n / m² | achsparallel (Vorgabe) | Hauptwert: Hülle achsparallel im gedrehten Plan | aus Treppen-Bbox | klein ohne Stempel (am Lift / mit Schacht-Text) |
|---|---|---|---|---|---|---|
| UG | 66,5° | 3 / 15,69 | 0 | 0 | 0 | 1 (1 / 0) |
| EG | 66,5° (2 Cluster) | 5 / 40,60 | 0 | 0 | 0 | 1 (1 / 0) |
| OG1 | 66,5° | 3 / 22,11 | 0 | 0 | 0 | 1 (1 / 0) |
| OG2 | 66,5° | 1 / 19,53 | 0 | 0 | 0 | 0 |
| OG3 | 66,5° | 1 / 19,96 | 0 | 0 | 0 | 0 |
| DG1 | 66,5° | 2 / 9,82 | 0 | 0 | 0 | 1 (1 / 0) |
| DG2 | 66,5° | 5 / 28,50 | 0 | **1 / 15,86** | 1 / 15,86 | 2 (1 / 1) |
| **Summe** | 7 von 7 gedreht | **20 / 156,21** | 0 | **1 / 15,86** | 1 / 15,86 | **6 (5 / 1)** |

Betroffene: DG2 `stiegenhaus_2` (Hülle 1,0, Kantenanteil 0,772 wegen ausgestanztem Lift); klein: UG `rest_3` 0,95, EG `rest_2` 0,96, OG1 `rest_2` 1,00, DG1 `rest_3` 0,73, DG2 `rest_4` 0,87 (alle am Lift, 0 mm), DG2 `rest_2` 1,16 („DBA SCHACHT“ 0 mm).

**Prüfstatus: korrigiert.** Alle Zahlen bestätigt (Nachrechnung mit dem Winkel des minimalen gedrehten Rechtecks: `stiegenhaus_2` 0,00°, übrige 19 STIEGENHAUS 22,3-23,9°; Kreismittel 66,9-69,4° statt Modus 66,5°, Urteil gleich). Korrigiert ist die Deutung: Der STIEGENHAUS-Typ der kleinen Reste kommt aus dem Treppen-Bbox-Zentrum (U2).

**Grenzen.**
- Die Vorgabe-Zahl verfehlt den Zielfall (0,772 < 0,90); Hauptwert ist die Hülle. Ein gedrehter Schnitt an einer Rechteckecke könnte die Hülle schräg machen; robuster wäre der Winkel des minimalen Rechtecks.
- `aus_treppen_bbox` nutzt `stiege_rechtecke`; ändert U1-Fix die Funktion, ist der Wert zwischen Vorher und Nachher nicht vergleichbar.
- Schacht-Text-Schwelle 500 mm ist empfindlich (DG1 `rest_3` „WP DDB 25/60“ in 799 mm, DG2 `rest_4` in 1030 mm).
- „klein < 2 m²“ kippt, wenn die Liftstanze geändert wird (Ringe vorher 2,30-2,74 m²). Für die Nachher-Messung zusätzlich „STIEGENHAUS mit Liftkontakt ohne Stempel“ flächenunabhängig zählen.
- Regex-Falsch-Positive: „DBA Raum“ (Zonenstempel), „Schachtverzug …“ (Hinweistext).
- Nebenbefund: `plan_pruefen._rotation` meldet für DG2 „keine dominante Kantenrichtung“, weil `entity_points` für INSERT nur einen Punkt liefert (`dxf_load.py:227-228`).

### M2 - Innenräume mit offenem Außenbereich (nur 7 Rennweg-Pläne)

**Definition.** AUSSEN = Union `aussen_offen` aus dem Cache (`aussen_geschlossen` ist in allen Plänen 0 m²). Ein Raum ist innen bei Typ in {WOHNZIMMER, ZIMMER, SCHLAFZIMMER, KINDERZIMMER, BAD, WC, ABSTELLRAUM, VORRAUM, STIEGENHAUS} oder Freifläche {TERRASSE, BALKON, LOGGIA}, oder mit zugeordnetem Stempel, oder mit Möbel-/Sanitär-Block (Einfügepunkt im Raum, Zonenstempel-Blöcke `__\d+$` ausgeschlossen). „berührt“ = Schnitt > 0,05 m². `wert` = innen ohne Freiflächen. Hüllen: H1 = Raum-Union mit Closing 400 mm; H2 = Wandkörper-Union mit Closing 3000 mm.

| Plan | offen m² | wert (ohne Freiflächen) | inkl. Freiflächen (korr. Kopfzahl) | tief: Raum −300 mm (ohne / inkl. Freifl.) | Innen-Schnitt (Union) m² | Freiflächen berührt | H1 ohne Freiflächen: offen darin m² |
|---|---|---|---|---|---|---|---|
| DG1 | 143,83 | 7 | 7 | 7 / 7 | 122,55 | 0 | 124,12 |
| DG2 | 45,36 | 4 | 5 | 3 / 4 | 10,90 | 1 (4,98 m²) | 11,13 |
| EG | 0 | 0 | 0 | 0 / 0 | 0 | 0 | - |
| OG1 | 64,13 | 3 | 4 | 3 / 4 | 38,94 | 1 (7,50 m²) | 39,11 |
| OG2 | 51,47 | 2 | 4 | 2 / 4 | 21,39 | 2 (22,67 m²) | 21,47 |
| OG3 | 114,03 | 4 | 4 | 4 / 4 | 110,36 | 0 | 110,44 |
| UG | 23,19 | 0 | 0 | 0 / 0 | 0 | 0 | 0,00 |
| **Summe** | **442,01** | **20** (19 > 1 m²) | **24** | **19 / 23** | **304,14** | 4 (35,15 m²) | 306,27 (69,3 %) |

Nicht innen berührt: 1 (DG2 `rest_5` SCHACHT, 0,08 m², Randsplitter). H2 (Closing 3000 mm): 340,58 m² (Nachrechnung 340,00 m²). Betroffene Räume je Plan: siehe 2.1-2.5 und U6-U8.

**Prüfstatus: korrigiert.** Zahlen exakt reproduziert. Korrigiert: (1) Nach Selmans Wortlaut zählen Freiflächen zu „nie Außen“ → Kopfzahl inkl. Freiflächen 24. (2) „Jeder betroffene Raum hat einen Stempel“ → 19 von 20. (3) „13 von 20 mit Möbeln/Sanitär“ → 12 (Einfügepunkt) bzw. 15 (Block-Mitte). (4) „Einfügepunkt unkritisch“ → falsch: ArchiCAD-Einfügepunkte liegen 391-836 mm von der Block-Mitte (27 Räume mit abweichender Zuordnung; `wert` unberührt). (5) „79 % des Außenbereichs in der Hülle“ → ohne Freiflächen 69,3 %.

**Grenzen.** Zählt nur existierende Raumpolygone (DG1 TV-Ecke fehlt; Hüllenwerte mitlesen). DG2 `stiegenhaus_2` ist ein 384 × 928-mm-Randstreifen (tiefer Schnitt 0) und vermischt U1 mit Außen → für die Nachher-Messung `wert_tief` ausweisen. EG ohne offenen Außenbereich, keine Aussage. Block-Regex aus einer Familie. Empfehlung Nachher: Kopfzahl inkl. Freiflächen, `wert_tief`, Block-Zuordnung über Block-Mitte, Hüllenanteil ohne Freiflächen.

### M3 - Schachtflächen ohne Ausstanzung (nur 7 Rennweg-Pläne)

**Definition.** Hauptwert (korrigiert): Anzahl Nicht-SCHACHT/LIFT-Räume mit Fläche(Raum ∩ Union roter geschlossener Konturen) ≥ 0,02 m²; rot = ACI 1 oder RGB mit R ≥ 200 und G, B ≤ 60; Kontur = geschlossene LWPOLYLINE/2D-POLYLINE < 3 m². Das Skript gibt diesen Wert als `rot_flaeche_in_raeumen.raeume_n` aus. Nebenwert (ursprünglicher `wert`): Räume mit Schacht-Text-Einfügepunkt (Regex DDB/BDB/FBDB/WDB/FDB/DBA/SCHACHT als Wort, ohne „Raum“) ohne SCHACHT/LIFT in ≤ 500 mm.

| Plan | **Hauptwert: Räume mit roter Schachtfläche** | rote Fläche (Union rote Konturen ∩ Raum-Union) m² | Nebenwert: Text-Räume | beides | Marker gesamt / im Raum / am Schacht / außerhalb | rote Konturen | SCHACHT ohne Text in 500 mm |
|---|---|---|---|---|---|---|---|
| DG1 | 7 | 1,415 | 7 | 5 | 17 / 13 / 1 / 3 | 36 | 0 |
| DG2 | 6 | 2,470 | 8 | 6 | 13 / 12 / 0 / 1 | 28 | 1 (`rest_5`) |
| EG | 3 | 1,807 | 4 | 3 | 21 / 19 / 0 / 2 | 34 | 0 |
| OG1 | 6 | 1,544 | 9 | 6 | 16 / 13 / 0 / 3 | 37 | 0 |
| OG2 | 5 | 1,574 | 8 | 5 | 16 / 14 / 0 / 2 | 33 | 0 |
| OG3 | 3 | 1,442 | 7 | 3 | 16 / 14 / 2 / 0 | 32 | 0 |
| UG | 4 | 1,204 | 6 | 4 | 14 / 8 / 0 / 6 | 16 | 0 |
| **Summe** | **34** | **11,456** | 49 | 32 | 113 / 93 / 3 / 17 | 216 | 1 |

Die Flächenspalte ist ein Union-Wert, keine Summe je Raum: DG2 2,470 m² gegen 2,759 m² als Summe der Raumwerte unten, weil `stiegenhaus_2` `raum_5`/`raum_7` überlappt (U1); EG 1,807 gegen 1,801 m² und UG 1,204 gegen 1,186 m² enthalten zusätzlich Räume unter der Schwelle 0,02 m².

Räume im Hauptwert:
- DG1: `raum_1` WOHNZIMMER 0,653, `raum_2` ZIMMER 0,387, `raum_3` ZIMMER 0,038, `raum_4` GANG 0,116, `raum_10` BAD 0,027, `raum_11` ABSTELLRAUM 0,045, `rest_2` STIEGENHAUS 0,149 m²
- DG2: `raum_1` VORRAUM 0,23, `raum_2` ZIMMER 0,461, `raum_5` ZIMMER 0,405, `raum_7` VORRAUM 0,165, `rest_2` STIEGENHAUS 1,15 (DBA-Schacht), `stiegenhaus_2` 0,348 m²
- EG: `raum_11` KÜCHE 0,458, `raum_12` untypisiert 1,321, `raum_13` MÜLLRAUM 0,022 m²
- OG1: `raum_2` ZIMMER 0,178, `raum_9` ZIMMER 0,287, `raum_10` untypisiert 0,159, `raum_11` ABSTELLRAUM 0,322, `raum_12` VORRAUM 0,519, `raum_13` WC 0,079 m²
- OG2: `raum_1` ZIMMER 0,35, `raum_2` untypisiert 0,405, `raum_5` VORRAUM 0,255, `raum_7` ZIMMER 0,178, `raum_8` ZIMMER 0,387 m²
- OG3: `raum_1` KÜCHE 0,040, `raum_2` ZIMMER 0,837, `raum_3` ZIMMER 0,565 m²
- UG: `raum_1` TECHNIK 0,527, `raum_6` VORRAUM 0,176, `raum_13` untypisiert 0,063, `rest_2` untypisiert 0,42 m²

**Prüfstatus: korrigiert.** Alle Zahlen des Skripts unabhängig exakt reproduziert. Die ursprüngliche Hauptzahl 49 bucht den Raum, in dem die Beschriftung steht: 14 dieser Räume haben die Kontur 41-150 mm hinter der Wand (Schnitt 0), EG `raum_17` TERRASSE („BDB 25/25“) und UG `raum_11` („S9 DDB 25/25“) zeigen LINE+CIRCLE-Ablauf-/Rohrsymbole ohne Kontur, UG `raum_10` ist mit 0,018 m² ein Grenzfall; DG1 `raum_11` (Feedback DG1-2) und `raum_3` fehlen darin. Die Flächenzählung enthält alle Feedback-Räume (EG-1, OG1-1, OG1-2, DG1-1, DG1-2, DG2-3, DG2-4). Alle 34 Flächenräume haben einen Schacht-Marker in ≤ 1030 mm.

**Grenzen.** Kleine Schnitte nicht per Render geprüft (DG1 `raum_10` 0,027, EG `raum_13` 0,022, OG3 `raum_1` 0,040, DG1 `raum_3` 0,038 m²). Typ- und Stanzfehler landen in derselben Zahl (DG2 `rest_2`, `stiegenhaus_2`). Rot-Schwelle und Konturtyp aus einer Familie; 103 FEUERFESTER_STEIN-Hatches liegen alle innerhalb roter Konturen (kein Zusatzsignal). Die Zahl sinkt nur, wenn ein SCHACHT-Polygon die Kontur deckt oder der Raum an der Schachtwand endet. Textwert hängt am Textanker (Block-Mitte statt Einfügepunkt: OG3 6 statt 7).

### M4 - Wohnungsbildung (nur 7 Rennweg-Pläne)

**Definition.** Wohnung = verschiedene `wohnung_id`; Einraum = 1 Raum; Datenbefund = Wohnung enthält STIEGENHAUS/TREPPENHAUS/LIFT/AUFZUG oder Klasse ALLGEMEIN_*; Darstellungsbefund = Nachbau des Umrisses (`raumerkennung_darstellung.py:709-731`) überdeckt einen solchen Raum > 0,5 m²; Privatraum ohne Wohnung = Typ in {ZIMMER, WOHNZIMMER, BAD, WC, KÜCHE, ABSTELLRAUM, VORRAUM} oder untypisiert mit Wohn-Stempel (`wohn|tv raum|k(ü|ue)?che`). Nur Cache.

| Plan | Wohnungen | Einraum | Datenbefund | Darstellungsbefund | auffällig | Privatraum ohne Wohnung | davon nicht ALLGEMEIN |
|---|---|---|---|---|---|---|---|
| DG1 | 1 | 0 | 0 | 0 | 0 | 2 | 1 (`raum_7` „TV Raum“ 15,91) |
| DG2 | 1 | 0 | 0 | 1 (`stiegenhaus_2` 2,27 m²) | 1 | 2 (VR 15,96 / 15,2) | 0 |
| EG | 2 | 1 (`raum_11` KÜCHE 9,27) | 0 | 0 | 1 | 1 (VR 21,03) | 0 |
| OG1 | 3 | 2 (`raum_11` AR 4,52; `raum_13` WC 3,5) | 0 | 0 | 2 | 2 | 1 (`raum_10` „Wohnkche“ 73,06) |
| OG2 | 2 | 1 (`raum_3` ZIMMER 22,22) | 0 | 0 | 1 | 3 | 1 (`raum_2` „Wohnbereich“ 59,53) |
| OG3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| UG | 4 | 4 (WC 6,17 / 1,48 / 1,48; AR 1,06) | 0 | 0 | 4 | 1 (VR Personal 4,77) | 0 |
| **Summe** | **15** | **8** | **0** | **1** | **9** | **11** | **3** |

**Prüfstatus: bestätigt.** Alle Zahlen unabhängig (Punktraster statt Shapely-Schnitt) reproduziert; Wohnungszahlen stimmen mit `kennzahlen.json` überein. Ergänzungen: Der Darstellungsbefund DG2 entsteht aus der Polygon-Überlappung `raum_5` ∩ `stiegenhaus_2` (2,26 m², U1), nicht aus dem Umriss; der fehlende ü-Umlaut steht bereits in der DXF.

**Grenzen.** Keine Türen im Cache, Ursachen nicht messbar; „30 von 75“ aus dem Cache nicht prüfbar (Bestandszählung siehe M5). Falsch-Negativ: OG3 `rest_4` (10,09 m², untypisiert, ohne Stempel, 39 % bzw. 26 % des Umfangs an `top_1`/`top_2`, Türen 80/2,20 zu Bad und WC) wird nicht erfasst. SCHLEUSE fehlt in den Erschließungstypen, SCHLAFZIMMER/KINDERZIMMER/WOHNKÜCHE in den Privattypen (heute ohne Wirkung). Empfehlung Nachher: Darstellungsbefund zweiteilig (schon im Raumpolygon vs. nur durch Puffer), NFC-Normalisierung der Stempel, Zusatzzähler für stempellose Resträume an Wohnungen.

### M5 - Wohnungseingänge je Wohnung über alle Pläne (Bestand 1e642ad, keine D-Vorher-Zahl)

**Definition.** Grundmenge: `Projekte/_ergebnis/*/kennzahlen.json` (83 Dateien, alle zuletzt in 1e642ad geändert, ohne `commit`-Feld; raumerkennung-Code zwischen 1e642ad und 511ad36 unverändert, siehe Kopf). Gezählt werden Dateien mit `tuer_typen.wohnungseingang` und `wohnungen`. Schwelle wie `docs/HANDOFF_SELMAN.md` Z.180-193: Verhältnis ≥ 3 bei mindestens einer Wohnung. Nur JSON gelesen, kein Package-Aufruf (B.8).

| Größe | Wert |
|---|---|
| Dateien | 83 |
| ohne Schlüssel `tuer_typen` | 8 (Fehler-Stubs mit den Schlüsseln `dxf`, `fehler`, `plan`; letzte Fehlerzeile jeweils `ValueError: Keine Wand-Entities gefunden …`) |
| ausgewertet (mit `tuer_typen`) = Grundmenge laut HANDOFF | 75 |
| `tuer_typen` ohne Schlüssel `wohnungseingang` | 23 |
| mit beiden Feldern | 52 (alle mit ≥ 1 Wohnung) |
| davon Verhältnis ≥ 3 | **30** (28 verschiedene DXF-sha256; doppelt: `EG - Rennweg …` = `Rennweg_EG`, `Erdgeschoß` = `Mollgasse_EG`) |
| Summe Wohnungseingänge / Wohnungen (52 Dateien) | 1625 / 354 |

Höchste Verhältnisse: `260320_938-AR-PP-21000-A_ERDGESCHOSS BT2` 42/1, `260320_938-AR-PP-11020-A_2.OBERGESCHOSS BT1` 82/2, `Elektromontageapläne_2-OBERGESCHOSS BT1` 90/3, `260320_938-AR-PP-11010-A_1.OBERGESCHOSS BT1` 53/2, `260320_938-AR-PP-11000-A_ERDGESCHOSS BT1` 79/3. Rennweg: DG2 18/1, DG1 4/1, EG 7/2 (≥ 3); OG1 3/3, OG2 5/2, OG3 5/2, UG 4/4 (< 3); DD ohne `wohnungseingang`.

**Prüfstatus: bestätigt, präzisiert.** 30 und 75 aus `docs/HANDOFF_SELMAN.md` (Z.71, Z.177, Z.180-193) sind reproduziert. Im Commit liegen 83 Dateien (`git ls-tree -r 1e642ad`); 8 davon sind Fehler-Stubs ohne `tuer_typen` („8 nicht auswertbar“), 75 sind ausgewertet. Präzisierung: Das Verhältnis ist nur auf 52 Dateien berechenbar, weil 23 der 75 kein Feld `wohnungseingang` haben (B.8).

**Grenzen.** Nur Kennzahl, keine Ursache. Außerhalb Rennweg ist nicht belegt, dass U12-U14 die Wurzel ist. Das Verhältnis zählt Türen mit der Rolle, nicht `eingangs_tuer_ids` (DG2: 18 gegen 10, Abschnitt 3 A4). Zwei Paare sind byte-gleiche Pläne. Nachher: dieselbe Zählung auf neu erzeugten `kennzahlen.json`, getrennt nach Rennweg und übrigen Familien, zusätzlich „Türen mit Rolle `wohnungseingang` ohne private Seite“.

---

## 5. Fix-Reihenfolge

**Branch-Regel.** Je Slice ein eigener Branch von aktuellem `origin/main` (`selman/<slice>`), nie auf `main`. Ein Concern = ein Commit; Test zuerst (rot), dann Fix (grün). Kein Push ohne GO. Keine destruktiven Git-Operationen; Synchronisieren per `git merge origin/main`, nicht per Rebase. Nach jedem Slice: Caches neu (Stufe 1 `raumerkennung_darstellung.py`), Messskripte M1-M4 (Anhang A), Sichtprüfung der betroffenen `uebersicht.png`. `pytest` nie parallel zu großen DXF-Läufen. **Stapel statt Sammel-Slice:** Wo Slices nur gemeinsam gemergt werden dürfen, bleiben sie getrennte Branches mit je einem Commit in fester Reihenfolge (Branch-Stapel: jeder Branch zweigt vom vorigen ab). Gemergt wird der Stapel erst nach seinem gemeinsamen Merge-Gate.

### 5.1 Übersicht

| Nr. | Slice (Branch) | Ursachen | Feedback-Punkte | Blockiert durch | Abhängig von / Gate |
|---|---|---|---|---|---|
| S1 | `aussen-loch-topologie` | U7 | DG1-3, DG1-4, S-H2 | setzt F7 Option A voraus: Bestätigung vor Merge. **Merge-Gate:** Messung kippender Loch-Teile auf Plänen mit Wandkörpern und Grenzring (nur In-Memory-Einzelfunktionen wie B.1, kein Cache nötig) | - |
| S2 | `aussen-innenzonen` | U8 (U19 Folge) | S-C, OG1-4, OG2-1, DG1-3, DG1-4, DG2-1, DG2-2, DG2-7, S-H2 | F6 (Typliste, Freiflächen) | S1; Pflichtmessung Höfe vor Merge |
| S3a | `rest-schacht-evidenz-vor-treppenmarker` | U2 (Typisierung, Evidenz) | DG2-3, S-H1 | - | S5a; Pflicht-Gate Nachmessung nach Türstapel |
| S3b | `rest-schacht-tuerlos-vor-treppenmarker` | U2 (Typisierung, Liftringe) | S-H1 (Liftringe) | F4 (nur bei Option a), F1; bei F4 c indirekt F3 (über S12) | S3a, Türstapel; bei F4 c nach S12 |
| S4a | `tueren-archicad-weltblock` | U12 (Lage) | S-H4, OG1-3 | F18 (nicht blockierend) | Türstapel S4a → S4b → S5b → S5c, ein Merge-Gate |
| S4b | `tuer-seitenprobe-schrittweise` | U12 (Seiten) | S-H4, OG1-3 | - | S4a (Stapel) |
| S5a | `durchgang-guard-kein-raum` | U13 (Guard) | S-H4 (Vorbedingung für S3a, S10a, S11b, S11c) | - | eigenständig; Nachmessung Türkette vor Merge |
| S5b | `durchgang-querung` | U13 (Kriterium) | S-H4, OG1-3 | F10 (nicht blockierend) | S4b (Stapel) |
| S5c | `aussen-durchgang-querung` | U13 (`aussen_durchgaenge`) | S-C, S-H2 (Folge U19) | - | S5b (Stapel) |
| S6a | `raumtyp-schreibvarianten` | U15 (Normalisierung, Schreibvarianten) | S-B1, S-H4, OG1-3 | - | - |
| S6b | `raumtyp-synonyme` | U15 (Synonyme „Wohnbereich“, „TV Raum“) | S-H4 | F15 (Zieltyp; Default WOHNZIMMER zur Bestätigung, nicht blockierend) | S6a |
| S7a | `wohnung-vorraum-beleg` | U14 (Vorraum-Regel) | S-H4, OG1-1, OG1-2 | F11 | Türstapel, S6a |
| S7b | `wohnung-mindestkriterium` | U16 | S-H4, EG-1, OG1-1, OG1-2 | F12 | Türstapel, S6a, S6b |
| S7c | `wohnungseingang-allgemein-zurueckstufen` | U14 (Rolle nach Verfeinerung) | S-H4 | F11 Zusatz (Zielrolle) | Türstapel |
| S8 | `wohnungsflur-flags` | U18 | OG1-3 | F16 (für `ist_fluchtweg`) | S7a |
| S9 | `treppe-anhaengen-huelle` | U1 | DG2-5, DG2-7, S-H1, S-H4 | - | - |
| S10a | `rest-label-4er` | U4 (4er-Nachbarschaft in `komponenten_ohne_stempel`) | DG2-4, S-H3 | - | S5a; Stapel S10a → S10b |
| S10b | `vektorisiere-verlustwarnung` | U4 (Verlustwarnung in `stempel_flutung._vektorisiere`, wirkt auch auf `flute_stempel`) | DG2-4, S-H3 | - | S10a (Stapel) |
| S11a | `schacht-belege-hinweis` | U3 (Beleg-Detektor nur als Hinweis und Kennzahl) | S-H3 (Voraussetzung für EG-1, OG1-1, OG1-2, OG1-3, DG1-1, DG1-2, DG2-4, DG2-6 2. Satz) | - (liefert die Korpusmessung für F3(5)) | S3a; Schachtstapel S11a → S11b → S11c → S11d, ein Merge-Gate |
| S11b | `schacht-ausstanzen-zonen` | U3 (Belegzellen in L/H/F-Zonen ausstanzen) | EG-1, OG1-1, OG1-2, OG1-3, DG1-1, DG1-2, DG2-4, DG2-6 (2. Satz), S-H3 | F3(2)-(4) | S11a (Stapel), S5a |
| S11c | `schacht-zonenfrei-klein` | U3 (zonenfreie Schächte ohne `_MIN_M2`) | DG2-4 (kleine Schächte außerhalb von Zonen), S-H3 | F3(3) | S11b (Stapel) |
| S11d | `schacht-nachlauf-angehaengt` | U3 (Nachlauf gegen später angehängte `stiegenhaus_*`/`lift_*`) | S-H3 (DG2 `stiegenhaus_2` enthält Marker-Zellen) | - | S11c (Stapel); nach S9 nachmessen |
| S12 | `schacht-nur-mit-evidenz` | U5 | DG2-6, S-H3 | F4; indirekt F3 (S11a nur mit dem Schachtstapel mergebar, S11b/S11c an F3) | S10a, S11a (Evidenzfunktion); ersetzt S3b bei F4 b |
| S13 | `rest-kontur-komponenten` | U10 | DG1-3, S-H2 | F9 (Behandlung der neuen Fläche) | S1 |
| S14 | `aussen-oeffnungsbruecke` | U6 | OG1-4, OG2-1, DG1-4, DG2-1, DG2-2, DG2-7, DG2-8, S-H2, S-C | F8; nur wenn Nachher-Messung nach S1/S2 Reste zeigt | S1, S2 |
| S15a | `darstellung-ausschnitt` | U11 | DG1-3 (Bild), S-H2 (Bildanteil) | - | jederzeit vorziehbar |
| S15b | `darstellung-wohnungsumriss` | U20 | S-H4 (Bild) | - | jederzeit vorziehbar |
| - | nicht geplant bis Antwort | U9 (F5), U17 (F14), Brücke untypisierter Räume (F13), Liftring in `finde_lifte` (F1), DG2 `rest_1` (F2) | DG2-1, DG2-2, DG2-7, DG2-8, OG1-4, S-H2, S-B2 | siehe Spalte | - |

### 5.2 Slices im Einzelnen

**S1 - Loch-Topologie im Außenbereich (U7).**
- Concern: `aussenbereich.erkenne_aussenbereiche`: Loch der Komponenten ohne Indiz berührt den Rand nie.
- Test zuerst: Wandring mit 150-mm-Restbarriere zur Hülle, Innenraum ohne Indiz → nicht offen.
- Erwartete Wirkung (in-memory gemessen, B.1): offen DG1 143,83 → 40,07 m², OG3 114,03 → 35,66 m²; UG/EG/OG1/OG2/DG2 unverändert. M2 `wert` DG1 7 → 4, OG3 4 → 2, Summe **20 → 15**. Falsche Außenöffnungen an OG3 `rest_3` (2473 mm mit `ist_notausgang`, 822 mm) entfallen (Cluster-Emulation, nicht nachgerechnet).
- Akzeptanzkriterium M2 (namentlich, B.1): Es entfallen DG1 `raum_1`, `raum_7`, `raum_8` und OG3 `raum_1`, `raum_2`. Es verbleiben genau 15: DG1 `raum_2`, `raum_3`, `raum_6`, `raum_10`; OG3 `raum_3`, `raum_4`; OG1 `raum_1`, `raum_2`, `raum_3`; OG2 `raum_7`, `raum_8`; DG2 `raum_2`, `raum_4`, `raum_5`, `stiegenhaus_2`.
- Risiko: **sicherheitsrelevant**. Ein indizloser Innen- oder Lichthof, der als Loch nahe der Hülle oder dem Grenzring liegt, verliert „offen“; im EG verlieren seine Türen damit Hauseingang und final_exit. Rennweg-Basis (B.1): 3 kippende Teile (DG1 103,76 m², OG3 41,25 und 37,13 m²), alle ohne Indiz, alle mit 193 mm Randabstand; EG/UG unverändert. `test_aussenbereich.py` logisch grün, ausführen.
- **Merge-Gate (Pflicht):** Mit der Kopie aus B.1 auf allen Plänen mit Wandkörpern die Teile zählen, die von offen auf nicht offen kippen (Fläche, Indiz, Randabstand, Grenzring ja/nein, Türen am Teil). Mindestens: Barawitzka EG (Hof 190,2/23,5 m², `exit_tuer_27`, Grenzring 616,8 m²), Mollgasse EG (Hoftüren Cluster A/B, Grenzring 1510,2 m²), Muthgasse E2, Rennweg EG (`test_soll_rennweg.py::test_soll_eg_final_exit_via_text`, `::test_soll_eg_wege_enden_am_final_exit`) sowie `test_soll_mollgasse.py::test_soll_hofausgaenge_cluster_a_und_b` und `test_soll_barawitzka.py::test_soll_genau_ein_final_exit`. Merge nur, wenn kein Teil mit Tür ins Freie kippt oder F7 für genau diesen Fall mit A beantwortet ist. S1 setzt F7 Option A um; diese Bestätigung ist vor dem Merge einzuholen, auch wenn kein gemessener Hof kippt. Das Gate braucht keine Caches: Der Loch-Test in B.1 (`teile_status`, Anhang A.5) ruft nur Einzelfunktionen auf (`lade_dxf`, `finde_wandkoerper`, `_wand_geschlossen`, `_komponenten_aus`, `grundstuecksgrenze`, `aussen_indizien`, `_strassenkante`); Türen am Teil kommen aus `tuer_oeffnungen`/`tueren_aus_dxf`. Nur die M2-Zählung und der Cache-Abgleich in B.1 lesen Cache-Räume; beide entfallen für das Gate. Nach Selmans Entscheid (F19, 2026-09-15) läuft diese Messung auf Barawitzka/Mollgasse/Muthgasse erst nach Freigabe der Fixes, mit dem regulären Lauf als Vorher/Nachher.

**S2 - Innenraum-Zonen aus dem Außenbereich (U8).**
- Concern: `erkenne_aussenbereiche(…, innen_zonen=None)` zieht Innenzonen (auf Gebäudemaske geclippt) als Differenz ab und nimmt sie in `gedeckt()` auf; `provider.py:114` übergibt sie.
- Test zuerst: gestempeltes ZIMMER hinter Fensterlücke → nicht offen, in `gedeckt()`; TERRASSE vor der Fassade bleibt offen.
- Erwartete Wirkung (in-memory nachgerechnet auf Stand S1, B.2; Veto-Liste = F6 Option 1 ohne Freiflächen = M2 `INNEN_TYPEN` {WOHNZIMMER, ZIMMER, SCHLAFZIMMER, KINDERZIMMER, BAD, WC, ABSTELLRAUM, VORRAUM, STIEGENHAUS}; Zuschnitt = Komponenten von `_wand_geschlossen(koerper, 5000)`): M2 `wert` **15 → 2**. Es verbleiben DG2 `raum_2` ZIMMER 4,65 m² und `raum_4` BAD 1,28 m²; beide Schnitte liegen vollständig außerhalb der Maske (Dachstreifen, U9/F5). Offen gesamt 259,88 → 123,63 m². Offen bleiben die Freiflächen OG1 `raum_15` 7,50 m², OG2 `raum_13`/`raum_14` 15,17/7,50 m², DG2 `raum_3` 4,93 m². Ohne Zuschnitt wäre `wert` 0, der Dachstreifen würde aber gedeckt (DG2 offen 34,46 m²). Balkontür-Rollen an Zimmern: nicht nachgerechnet.
- Akzeptanzkriterium (gebunden an die F6-Antwort): Gemessen ist F6 Option 1 ohne Freiflächen (B.2). Dafür gilt M2 `wert` = 2 mit genau DG2 `raum_2` und `raum_4`, bis F5 entschieden ist, und die neue Kennzahl `wert_maske` (wie `wert`, Schnitt nur Raum ∩ offen ∩ Maske) = **0** (heute 20, nach S1 15). Option 1 mit Freiflächen, Option 2 und Option 4 sind Obermengen dieser Liste: `wert` = 2 und `wert_maske` = 0 gelten weiter (die Veto-Fläche wächst nur, beide Reste liegen außerhalb der Maske), die offene Fläche ist neu zu messen. Option 3 ist keine Obermenge (ungestempeltes DG2 `stiegenhaus_2`); dann ist das Kriterium vor dem Merge neu zu messen.
- Risiko: mittel (Barawitzka-Hof 190,2/23,5 m² und `exit_tuer_27`, Mollgasse Cluster B/`tuer_68`; der DG2-Dachstreifen darf nicht gedeckt werden). Pflichtmessung dieser Fälle vor Merge; Maskenknopf 5000 mm vor Einbau über alle Pläne messen.
- Blockiert: Typliste und Freiflächen (F6). Vorschlag zur Bestätigung: F6 Option 1 ohne Freiflächen (= gemessene Liste); Option 4 als Erweiterung, falls das Stempel-/Möbel-Indiz aus S-C gewollt ist.

**S3a - Evidenz-Schacht vor Treppenmarker (U2, Typisierungsteil).**
- Concern: In `rest_komponenten._typisiere` wird eine Komponente < 3 m² mit Schacht-Text im Polygon (Wortgrenze, nie „DBA“ allein, nie RAUM/TREPP/STIEG/AUFZUG/LIFT) oder mit STO-Kästchen vor der Markerregel SCHACHT.
- Warum unabhängig von F4: Ein Schacht mit Planzeichen ist in allen F4-Optionen (a, b, c) SCHACHT; S3a nimmt keine Antwort vorweg. Rote Konturen bleiben draußen, bis F3(5) klärt, ob die Farbsignatur familienübergreifend gilt.
- Test zuerst: 1,2-m²-Komponente mit „DBA SCHACHT“ 700 mm neben Treppen-Bbox-Zentrum → SCHACHT; türlose 1-m²-Komponente ohne Text am Zentrum → STIEGENHAUS; ≥ 3 m² mit Marker → STIEGENHAUS.
- Erwartete Wirkung (echte Funktion, B.3): nur DG2 `rest_2` → SCHACHT (DG2-3); die fünf Liftringe bleiben STIEGENHAUS. M1 „klein ohne Stempel“ 6 → 5; M3 Hauptwert DG2 6 → 5; DG2 PODEST-Anker im DBA-Schacht entfällt.
- Reihenfolge: nach S5a, weil `rest_2` heute Durchgänge zu `raum_2` und `raum_7` hat (`durchgang_7`, `durchgang_22`, B.7), die ohne Guard als Durchgänge zu einem KEIN_RAUM bestehen blieben.
- **Pflicht-Gate:** Nach dem Türstapel (S4a-S5c) M1, M3 und die R-Typen aller Pläne neu messen. `tuer_n` hängt an der Türquelle: In der DG2-Gegenprobe mit echten Türen wurde `rest_4` STIEGENHAUS → SCHACHT, und `rest_5` entfiel (U12 Blast Radius).
- Risiko: niedrig (nur Evidenz-Fälle < 3 m²); Schacht-Wortschatz anderer Familien ungemessen.

**S3b - Türloser Kleinrest vor Treppenmarker (U2, Liftringe).**
- Nur bei F4 Option a. Concern: Die bestehende SCHACHT-Regel „< 3 m² und `tuer_n == 0`“ rückt vor die Markerregel.
- Test zuerst: türlose 1-m²-Komponente ohne Text 700 mm neben Treppen-Bbox-Zentrum → SCHACHT.
- Erwartete Wirkung (echte Funktion ohne Marker, B.3): zusätzlich UG `rest_3`, EG `rest_2`, OG1 `rest_2`, DG1 `rest_3`, DG2 `rest_4` → SCHACHT; M1 „klein ohne Stempel“ 5 → 0.
- Warum S3 vor S12 und S3b abhängig von F4: S3a ist F4-unabhängig und behebt DG2-3 früh. S3b zieht genau die Regel ohne Planzeichen-Beleg nach vorn, die U5/F4/S12 in Frage stellen. Bei F4 b entfällt S3b; die Ringe bleiben bis F1 STIEGENHAUS und werden in `finde_lifte` behandelt. Bei F4 c ersetzt das Umschlossen-Prädikat aus S12 die Bedingung `tuer_n == 0`, dann kommt S3b erst nach S12. Ob die Ringe umschlossen sind, ist nicht gemessen.
- Risiko: Ein Podest-Fragment < 3 m² ohne erkannte Tür verliert das Fluchtweg-Flag (Rennweg und eingecheckte Ergebnisse von Muthgasse_E2/Mollgasse_EG/Barawitzka_EG: kein Fall). Ring-SCHACHT überlappt LIFT (Präzedenz Barawitzka). Pflicht-Gate wie S3a.

**Türstapel S4a → S4b → S5b → S5c (U12, U13): getrennte Commits, ein Merge-Gate.** Jeder Teil allein verschlechtert OG1: Ohne echte Türen hat OG1 nur 2 Verbindungen, und echte Türen mit fester 300-mm-Probe liegen auf falschen Seiten. Risiko hoch, wenn einzeln ausgeliefert. Merge-Gate für den ganzen Stapel: Türkette in-memory (B.7) auf OG1, OG3, DG2, EG; M4 und M5 (Rennweg) neu; `test_wandkoerper.py::test_rennweg_tueroeffnungen`, `test_soll_rennweg.py`, `test_soll_muthgasse.py` strict-xfails, `test_tuer_zuordnung.py`. R-Polygone können sich über Türsiegel ändern (danach Pflicht-Gate S3a).

**S4a - ArchiCAD-Weltkoordinaten-Türblöcke (U12, Lage).**
- Concern: Port von `door_blocks.detect_door_blocks` in `tuer_oeffnungen`, nur wenn der INSERT außerhalb und die Blockgeometrie innerhalb des Planbereichs liegt; Docstring `im_planbereich` korrigieren.
- Test zuerst: Weltkoordinaten-Türblock (INSERT weit weg, Bogen in einer 350-mm-Wand) → eine Öffnung an der Wand, nicht von `im_planbereich` verworfen.
- Erwartete Wirkung: Block-Öffnungen nach Filter heute 0 in allen Plänen (B.6); danach OG1 9, OG3 11, DG2 4, EG 7 (Türblöcke laut U12; nicht simuliert). UG/OG2/DG1 haben 15/9/5 Block-Öffnungen vor dem Filter; ob das echte Türen sind, ist nicht geprüft.

**S4b - Schrittweise Seitenprobe (U12, Seiten).**
- Concern: `tuer_zuordnung.ordne_tueren` probt schrittweise bis lokale Wanddicke + 300 mm statt fest ±300 mm.
- Test zuerst: Tür in 350-mm-Wand zwischen zwei Räumen → beide Raumseiten. Außerdem eine WC-Tür, bei der eine feste 600-mm-Probe ins Stiegenhaus reicht (Muster OG1 `tuer_10`) → WC und Vorraum.
- Erwartete Wirkung: OG1 `tuer_3` bekommt beide Seiten (Gegenprobe U12); nicht über alle Türen simuliert.

**S5a - Guard für KEIN_RAUM-Paare (U13).**
- Concern: `durchgaenge_ohne_tuerblatt` überspringt Paare mit einer Seite der Klasse KEIN_RAUM, bestimmt über `nutzungsklasse_fuer(raum_typ)`, weil `Raum.nutzungsklasse` an dieser Stelle noch None ist. Vor den Durchgängen trifft der Guard nur SCHACHT und gestempelte LIFT-Räume; `lift_*` entstehen erst mit `finde_lifte` (`provider.py:180`).
- Test zuerst: SCHACHT-Raum an Zimmer ohne Tür → kein Durchgang.
- Erwartete Wirkung: latenter Durchgang DG2 `raum_5`↔`rest_5` 1531 mm entfällt. Vorbedingung für S3a, S10a, S11b und S11c (Phantom-Durchgänge Schacht↔Wirtsraum simuliert, B.12: EG 11 Durchgänge an 12 simulierten Schächten, OG1 6 an 14, DG2 6 an 6). Eigenständig mergebar; vor Merge Türkette OG1/DG2/EG nachmessen (Wohnungszahl unverändert erwartet, nicht gemessen).

**S5b - Querungskriterium (U13).**
- Concern: In `durchgaenge_ohne_tuerblatt` zählt nur ein freier Teil, der die Wand zwischen beiden Räumen quert. Die Breite wird entlang der gemeinsamen Grenze gemessen. Splitter (Fläche < Breite · 50 mm) und Überlappungen queren nicht. Das ist ein Prädikat und ein Commit. Die Varianten Asymmetrie und Schlitz vor dem Commit auf OG1/DG2/EG in-memory vergleichen.
- Test zuerst: 100-mm-Wand ohne Lücke → keine Tür (heute 4490 mm, B.5); 900-mm-Lücke → eine Tür ≈ 900 mm; `test_durchgang_ohne_tuerblatt` auf Breite ≈ 1200 mm (±100) verschärfen.
- Erwartete Wirkung: Scheinkanten wie OG1 Bad↔Gang 4830 mm entfallen; DG2 heute 18 Türen mit Rolle `wohnungseingang`, alle `durchgang_*` ohne Türblatt (B.7). Nicht simuliert.

**S5c - Querungskriterium in `aussen_durchgaenge` (U13).**
- Concern: dasselbe Prädikat in `aussen_durchgaenge` (`tuer_zuordnung.py:169-224`).
- Test zuerst: Außenwand ohne Lücke neben ALLGEMEIN-Raum → keine `oeffnung_aussenwand`.
- Erwartete Wirkung: nicht simuliert. Betrifft die Außenöffnungen aus U19 (DG1 `rest_2` 2590 mm, OG1 `rest_1` 1336 mm), soweit sie keine Wand queren. DG2 `rest_3` 1413 mm entsteht laut U19-Vorbehalt nur in der K4-Prüfung mit Cache-Nutzungsklasse, nicht in der echten Türkette.

**S6a - Raumtyp-Schreibvarianten (U15, Normalisierung).**
- Concern: NFC-Normalisierung und Umlaut-Varianten in `raumtyp_flags` vor allen Stufen (Override-Varianten zuerst, Kopf-Toleranz nur als Kompositum). Keine Synonyme.
- Test zuerst: S6a-Zeilen aus U15 („Wohnkche“ → KÜCHE; „Waschkche“/„Waschkuche“ → WASCHKÜCHE; „Kche“/„Kuchen“ → None).
- Vorbedingung: Textdump über alle Projekt-DXF auf Endungen „kche/kuche/kueche“ (Fehltreffer).
- Erwartete Wirkung: M4 untypisierte Räume mit Wohn-Stempel 3 → 2 (OG1 `raum_10` → KÜCHE); ob der Raum einer Wohnung beitritt, hängt am Türstapel (S4a-S5c) und an S7a (nicht simuliert). Leuchten unverändert.
- Risiko: niedrig.

**S6b - Raumtyp-Synonyme (U15, Vokabular).**
- Concern: `_EXTRA_LABELS` um „wohnbereich“ (token-exakt) und das Tokenpaar „tv“ + „raum“ erweitern. Der Zieltyp WOHNZIMMER ist ein Default zur Bestätigung durch F15 (WOHNZIMMER oder ZIMMER, downstream gleichwertig); S6b nimmt die Antwort nicht vorweg, sondern trägt sie als einzigen Wert.
- Test zuerst: S6b-Zeilen aus U15 („Wohnbereich“, „TV Raum“, „TV-Raum“ → Zieltyp; „Eingangsbereich“, „Außenbereich“, „TV“ → None).
- Vorbedingung: Textdump über alle Projekt-DXF auf beide Synonyme (Fehltreffer).
- Erwartete Wirkung: zusammen mit S6a M4 3 → 0 (OG2 `raum_2`, DG1 `raum_7` → Zieltyp); nicht simuliert.
- Risiko: niedrig; ein anderer F15-Zieltyp ändert nur den eingetragenen Typ.

**S7a - Vorraum-Regel mit Beleg (U14).**
- Concern: `_verfeinere_gang_privat` nach F11 (Beleg: Stempel, Türmerkmal oder TOP-Text).
- Test zuerst: synthetische Diele → eine Wohnung (heute 4 Einraum-Wohnungen, B.5); `test_zwei_wohnungen_getrennt` grün; `test_flur_mit_stiegenhaustuer_bleibt_erschliessung` bewusst neu gefasst.
- Erwartete Wirkung: M4 Einraum OG1 2 → Ziel 0; nicht simuliert.
- Risiko: hoch (ein falsch privat gewordener allgemeiner Vorraum verliert Notlicht). Nur auf dem Türstapel.

**S7b - Mindestkriterium Wohnung (U16).**
- Concern: Eine Gruppe ohne Aufenthaltsraum bekommt laut F12 keine `wohnung_id`; ihre Klasse laut F12 (2).
- Test zuerst: WC mit Tür nur ins Stiegenhaus → keine Wohnung.
- Erwartete Wirkung: M4 Einraum EG 1 (`raum_11`) und UG 4 → Ziel 0; OG2 `raum_3` ZIMMER fängt das Kriterium nicht (U16). Nicht simuliert.
- Risiko: mittel bis hoch (eine andere Klasse ändert Notlicht).

**S7c - Wohnungseingang ohne private Seite zurückstufen (U14, Rolle).**
- Concern: Nach `_verfeinere_gang_privat` bekommt eine Tür `wohnungseingang` ohne private Seite die Rolle laut F11-Zusatz.
- Test zuerst: Tür VORRAUM (ALLGEMEIN_ERSCHLIESSUNG) ↔ STIEGENHAUS mit Rolle `wohnungseingang` → andere Rolle.
- Erwartete Wirkung (aus der Türkette abgeleitet, B.7): DG2 `tuer_typen.wohnungseingang` 18 → 10 (`durchgang_19` bis `_26`), `eingangs_tuer_ids` von `top_1` unverändert; M5-Verhältnis DG2 18 → 10.
- Risiko: mittel. `fluchtweg.py:282-296` startet Fluchtwege an `wohnungseingang`-Türen und an Türen von ALLGEMEIN-Räumen; ob sich die Startmenge ändert, ist nicht gemessen.

**S8 - Flags von Wohnungsfluren (U18).**
- Concern: `ist_communal`/`ist_fluchtweg` nach Wohnungsbildung; Gang-Anker nur für nicht-private Gänge.
- Test zuerst: GANG in Wohnung → keine Gang-Anker.
- Erwartete Wirkung: OG1 `raum_8` ohne Gang-Anker (nicht gemessen); `test_keine_anker_in_wohnung_privat` auf weitere Pläne ausdehnen.
- Risiko: mittel (Contract-Werte aller Wohnungsflure; Norm-Lookup GANG).

**S9 - Treppen-Anhängezweig (U1).**
- Concern: Deckungsprüfung mit gedrehter Hülle im else-Zweig von `typisiere_stiegenhaus`; `stiege_rechtecke` unverändert.
- Test zuerst: gedrehte Treppe, Hülle zu 90 % gedeckt, Mittelpunkt in Wand → kein Anhang.
- Erwartete Wirkung: M1 Hauptwert 1 → 0; DG2 3 Läufe und 4 Anker weniger; M2 DG2 `stiegenhaus_2`-Randstreifen und M3 `stiegenhaus_2` 0,348 m² entfallen.
- Risiko: `ANTEIL_NEU` vor Merge auf Muthgasse/Mollgasse/Barawitzka messen (stair_exit-xfails, Mollgasse-Stiegenhäuser).

**R-Stapel S10a → S10b (U4): zwei Commits im selben Branch-Stapel.**

**S10a - 4er-Nachbarschaft in der R-Stufe (U4).**
- Concern: `rest_komponenten.komponenten_ohne_stempel` labelt mit `connectivity=1` (`rest_komponenten.py:156`).
- Test zuerst: Eckberührung zweier Freiflächen → zwei R-Räume, Flächensumme erhalten.
- Erwartete Wirkung (B.4): DG2 zusätzliche R-Komponente 1,849 m² (SCHACHT, Schachtreihe L1/L2/S5); `rest_N`-IDs verschieben sich.
- Risiko: niedrig bis mittel (IDs in Berichten, mehr kleine R-Räume).

**S10b - Verlustwarnung in `_vektorisiere` (U4).**
- Concern: `stempel_flutung._vektorisiere` (`stempel_flutung.py:202-219`) meldet den Flächenverlust Maske → Polygon über einer Toleranz (Knopf). Das wirkt für die R-Stufe und für `flute_stempel`; `label(frei)` in `flute_stempel` (`:151`) bleibt unverändert.
- Test zuerst: Maske aus zwei getrennten Konturen → Warnung mit Verlustfläche; Maske mit einer Kontur → keine Warnung.
- Erwartete Wirkung: heute DG2 ein Fall mit Verlust (Maske 5,838 m² → Polygon 3,995 m², B.4 Aufruf 1). Wirkung nach S10a und auf Plänen mit aktiver Flutung (F) nicht gemessen.
- Risiko: niedrig (nur Hinweis, keine Geometriewirkung).

**Schachtstapel S11a → S11b → S11c → S11d (U3): getrennte Commits, ein Merge-Gate.** Merge-Gate für den ganzen Stapel: Korpusmessung der Beleg-Treffer aus S11a auf allen Plänen mit Wandkörpern (Treffer je Plan, Fehltreffer anderer Familien, Layer, Farbe, Strichstärke), M2-M4 Rennweg neu, `test_bereinigung.py`, `test_kaskade.py::test_barawitzka_raeume` und `::test_mollgasse_raeume_kuratiert`, `tests/naht/test_ueberlappung_riegel.py`. Vor S11b muss S5a gemergt sein. Zuordnung der Pseudocode-Zeilen: U3 Fix, Markierung `[S11x]`.

**S11a - Schacht-Belege nur als Hinweis (U3, Detektor).**
- Concern: `schacht_belege(plan)` (rote geschlossene Rahmen mit effektiver Farbe, FEUERFESTER_STEIN-HATCH mit eigenem Walk vor dem Negativ-Layer-Filter, gestapelte Duplikate zusammengefasst) liefert Hinweise und eine Kennzahl je Raum, ohne Geometrie- und Typwirkung.
- Test zuerst: synthetischer Plan mit roter geschlossener Kontur in einer Zone → ein Beleg-Hinweis am Raum, Raumpolygon unverändert; gleiche Kontur in Schwarz → kein Beleg.
- Erwartete Wirkung: Räume, Typen und M1-M4 unverändert. Die Hinweis-Kennzahl ist mit M3 vergleichbar (34 Räume; M3 nutzt nur die Farbregel ohne Keil-Walk), nicht simuliert.
- Risiko: niedrig (nur Hinweis). Liefert die Korpusmessung für F3(5).

**S11b - Belegzellen in Zonen ausstanzen (U3).**
- Concern: Nebenzellen einer L/H/F-Zone (Zone − Wandunion) mit Beleg-Schnittfläche werden eigene SCHACHT-Räume mit interner Quelle; Dedup gegen SCHACHT/LIFT; Bereinigung Regel 1 stanzt aus.
- Blockiert durch F3(2)-(4) (Polygon, Objekt, Beleg).
- Test zuerst: synthetische Zelle mit roter Kontur in einer Zone → SCHACHT-Raum, Wirtsraum verkleinert, Buchung LIFT_SCHACHT, kein Durchgang; rahmenlose Nische bleibt Raum.
- Erwartete Wirkung: M3 Hauptwert 34 → Ziel 0 (bzw. Rest je F3); Raumflächen −0,6 % bis −14 % je nach Polygon-Definition. Außer den Durchgängen (B.12) nicht simuliert.
- Risiko: hoch (Wörterbuch global; Stempelabweichungen; Schlitz-Konsumenten; Phantom-Durchgänge ohne S5a).

**S11c - Zonenfreie kleine Schächte (U3).**
- Concern: Komponenten aus Kontur − Wandunion − belegte Räume mit Beleg werden SCHACHT, auch unter `_MIN_M2` = 1 m².
- Blockiert durch F3(3) (Mindestgröße, Splitter).
- Test zuerst: 0,3-m²-Freifläche mit roter Kontur zwischen zwei Räumen → SCHACHT; 0,3-m²-Freifläche ohne Beleg → kein Raum.
- Erwartete Wirkung: Kandidat DG2 „S7 DDB/BDB 60/95,5“ (0,3-m²-Komponente, Text in 799 mm, B.4). Ob sie einen Beleg schneidet, ist nicht gemessen; weitere Kandidaten nicht gezählt.
- Risiko: mittel (mehr KEIN_RAUM-Kleinräume, Splitter).

**S11d - Nachlauf gegen später angehängte Räume (U3).**
- Concern: Nach der Kaskade angehängte `stiegenhaus_*`/`lift_*` werden gegen vorhandene SCHACHT-Räume bereinigt, sonst wird die Lücke als Hinweis dokumentiert.
- Test zuerst: angehängtes STIEGENHAUS-Rechteck über einem SCHACHT-Raum → Überlappung ausgestanzt bzw. Hinweis.
- Erwartete Wirkung: auf Rennweg nur DG2 `stiegenhaus_2` (enthält Marker-Zellen 0,741 und 0,15 m², B.14); entfällt, wenn S9 `stiegenhaus_2` beseitigt. Nicht simuliert.
- Risiko: niedrig bis mittel (Reihenfolge im Provider).

**S12 - SCHACHT nur mit Evidenz (U5).**
- Bezug zu S3b: Bei F4 b entfällt S3b; bei F4 c liefert S12 das Umschlossen-Prädikat, auf dem S3b dann aufsetzt.
- Abhängig von S10a (R-Komponenten) und S11a (Evidenzfunktion `schacht_belege`).
- Test zuerst: Box mit Fensterlücke am Konturrand → nicht SCHACHT; ummauerte Box bleibt SCHACHT.
- Erwartete Wirkung: M3 `fp_ohne_text` 1 → 0 (DG2 `rest_5`).
- Risiko: mittel (Bestand SCHACHT anderer Familien, Barawitzka `rest_3` = Lift).

**S13 - R-Kontur aus Gebäudekomponenten (U10).**
- Test zuerst: 400-mm-Ring mit 1320-mm-Fenstern und zonenloser Fläche → R-Komponente.
- Erwartete Wirkung: DG1 TV-Bereich wird R-Raum (nicht simuliert); R-Konturen OG3/DG1 deutlich größer.
- Risiko: mittel (R aller Pläne, Laufzeit; Komponenten nur einmal rechnen).

**S14 - Öffnungsbrücken (U6).**
- Nur wenn die Nachher-Messung nach S1/S2 noch Innenräume unter offen oder falsche AUSSEN-Türen zeigt (DG1 `rest_2` 2590 mm und OG1 `rest_1` 1336 mm hängen an U6, nicht an U7).
- Test zuerst: 400-mm-Ring mit 1320-mm-Fenster und 2400-mm-Fenstertür → nicht offen; Texttür in Fassadenlücke behält AUSSEN-Seite.
- Risiko: hoch (EG `tuer_11` final_exit; Durchfahrten/Höfe). Pflichtmessung EG/Mollgasse/Barawitzka.

**S15a - Bildausschnitt mit Gebäudekomponenten (U11).** Nur Prüfbilder; Cache-Format erweitert → Stufe 1 neu. Jederzeit vorziehbar; erleichtert die Sichtprüfung von S1, S2 und S13.

**S15b - Wohnungsumriss mit Füllung, Label im Umriss (U20).** Nur Prüfbilder (`--nur-zeichnen` genügt). Jederzeit vorziehbar; erleichtert die Sichtprüfung von S7a-S7c.

### 5.3 Begründung der Reihenfolge

1. **Sicherheitsrelevanz zuerst.** Der Außenbereich speist Türseiten, `ist_notausgang` im Contract, `aussen_tuer_rz` und im EG final_exit. S1 ist rein topologisch, ändert auf Rennweg EG/UG nicht und entfernt gemessen 103,76 + 78,38 m² falsche Außenfläche (M2 20 → 15). Weil ein verlorenes „offen“ auf Plänen mit Höfen den final_exit entziehen kann, trägt S1 ein Merge-Gate (Messung auf Barawitzka/Mollgasse/Muthgasse, F7). S2 setzt die Fachregel S-C direkt um (M2 15 → 2, `wert_maske` → 0), braucht aber die Typliste (F6) und die Pflichtmessungen an Höfen.
2. **Kleine gemessene Korrektur ohne Knopf:** S5a (Guard) zuerst, weil S3a, S10a, S11b und S11c neue KEIN_RAUM-Räume erzeugen. S3a behebt DG2-3 mit Planzeichen-Beleg und nimmt F4 nicht vorweg. S3b (Liftringe) wartet auf F4/F1 und steht nur bei F4 a vor S12.
3. **Türgraph vor Wohnungen:** Wohnungsbildung, Wohnungseingänge, Fluchtweg-Starts und stair_exit hängen am Türgraphen. S4a, S4b, S5b und S5c bleiben getrennte Commits, werden aber als Branch-Stapel nur gemeinsam gemergt, weil jeder allein OG1 verschlechtert; danach Pflicht-Gate für S3a (`tuer_n`). S6a ist unabhängig und risikoarm und liefert S7a die fehlende KÜCHE (OG1). S6b folgt mit einem Default-Zieltyp zur Bestätigung durch F15 und liefert S7b die übrigen Typen. S7c hängt nur an der Zielrolle (F11-Zusatz); S7a, S7b und S8 folgen, sobald F11/F12/F16 beantwortet sind.
4. **Stiegenhaus-Rechteck:** S9 hat auf Rennweg nur DG2-Wirkung, braucht aber Fremdmessungen (Muthgasse stair_exit).
5. **Schacht zuletzt unter den Code-Slices:** Der Schachtstapel S11a-S11d hat den größten Blast Radius (globales Wörterbuch, Flächen, neue KEIN_RAUM-Räume). S11a kommt ohne Geometriewirkung zuerst, damit die Korpusmessung der Beleg-Treffer vor jeder Ausstanzung vorliegt. S11b und S11c warten auf F3; der Guard S5a muss vor S11b stehen. S12 hängt über S11a am Stapel-Gate und damit indirekt an F3; S10a hängt nur an S5a, S10b an S10a. S12 ersetzt S3b bei F4 b.
6. **R-Kontur und Brücken:** S13 nach S1 (gemeinsame Komponenten), S14 nur bei Restbedarf, weil es das höchste EG-Risiko trägt.
7. **Darstellung** (S15a, S15b) unabhängig; Priorität nach Bedarf der Sichtprüfung.

---

## 6. Offene Fachfragen

| Nr. | Adressat | Frage | Optionen und Trade-offs | Blockiert bis zur Antwort |
|---|---|---|---|---|
| F1 | Selman, Leonis; Vokabular alle 3 Owner | Wie steht der lichte Liftschacht im RaumModell? Heute LIFT = Kabinen-/Symbolrechteck 1,74 m², Ring 0,73-1,00 m² (gesamt 2,30-2,74 m²) STIEGENHAUS. | **A** LIFT = Schachtinnenkontur: Verbotszone vollständig, aber `LIFT.flaeche_m2` größer als das Symbol, Rasterpolygon (60-74 Ecken). **B** LIFT Rechteck, Ring SCHACHT: kleinste Änderung, heute schon Ist-Zustand in Barawitzka; zwei KEIN_RAUM-Polygone im selben Schacht. **C** Ring verwerfen: sauberes Bild; Flächenbilanz und Verbotszone ohne Ring, nicht als LIFT_SCHACHT am Lift buchbar (`raum_modell.py:99-109`). Für Leonis sind LIFT und SCHACHT gleichwertig (`fachpraxis.py:73-76`). | Ringbehandlung in `finde_lifte` (U2), S3b |
| F2 | Enis (Fluchtweg/Norm), Leonis (Anker); Vokabular alle 3 | DG2 `rest_1` ist eine Treppe (`Stair_1`) in einer Fläche ohne Wohnung, im DG1 darunter keine Treppe. Wie typisieren? | **A** STIEGENHAUS bleibt: Anker, Stiegenhaus-Rollen angrenzender Türen. **B** private Innentreppe (neues Label, WOHNUNG_PRIVAT): keine Anker, Vokabular-Änderung. **C** untypisierter Raum der Wohnung: minimal, Treppeninfo verloren. **D** Treppe zu Dach/Dachterrasse/Technik: weder Wohnungs- noch allgemeines Stiegenhaus, Beleuchtungsregel offen. Vorher Ziel im Plan „DD - Rennweg …“ an x 12551378-12555280, y 356215871-356218037 prüfen (nicht geprüft). | Typ DG2 `rest_1` |
| F3 | Leonis (Konsum), Enis (Norm), Owner (Contract/Wörterbuch) | Wie sollen Schächte aus Räumen ausgegrenzt werden? | **(1) Flächenbezug im Prüfbild:** A bereinigt wie heute mit Vermerk „erklärt durch LIFT_SCHACHT“; B roh wie in `plan_pruefen`. **(1b) Stempelschutz (10 %, Regel 3) auch für Regel 1?** ja: stempeltreue Zonen, Schacht bleibt überlappend, Leuchten im Schacht möglich; nein (§14.6.1 (c) „immer“): saubere Verbotszone, AR −8,6 % bzw. −14 %. **(2) Polygon:** A lichte rote Kontur (−0,6 bis −1,0 %); B hohle Zelle zwischen Schachtwänden (OG1 AR 4,13 m²); C Zelle mit Schachtwand (AR 3,89 m², Raum endet an der sichtbaren Wand). **(3) Objekt:** eigener SCHACHT-Raum (Verbotszone als Objekt, braucht Durchgangs-Guard und Mindestgröße, Splitter 0,008 m²) oder Kerbe mit Buchung `gegenspieler=None` (kein Contract-Change, aber kein Objekt für Leonis). **(4) Beleg:** nur Zellen mit Kontur-Schnittfläche (OG1 WC 3,437 m²) / auch berührende Zellen (3,341) / auch rahmenlose Zellen zwischen Schachtwänden (3,238); DDB ohne BDB ausstanzen (DG2 S8 DDB im Revisionskreis)?; kleine Durchbrüche 25/25 als LINE+CIRCLE-Symbol (EG Terrasse, UG S9)? **(5)** Gelten Legenden-Signaturen (Rahmen Farbe 1, Strichstärke 13, Quelle Rennweg) global oder nur für Pläne mit passender Legende/Familie? **(6)** Bedeutet „DBA“ Druckbelüftungsanlage (Mollgasse „DBA - AUSSEN LUFTANSAUGUNG 15.000m3/h“, „BLITZLICHT DBA \| FEUERWEHRTABLEAU“)? | S11b (F3(2)-(4)), S11c (F3(3)), S12; S11a nicht blockiert, liefert die Korpusmessung für (5) |
| F4 | Leonis, Owner | Soll eine kleine türlose Restfläche ohne Planzeichen weiter SCHACHT (KEIN_RAUM) sein? | **a** ja (heute): Nischen/Laibungen/Dachreste werden KEIN_RAUM (DG2 `rest_5`). **b** nur mit Evidenz: Fehltreffer weg, unbeschriftete Schächte verlieren KEIN_RAUM, `test_rest_komponenten` bricht. **c** nur allseitig ummauert: Randflächen untypisiert, ummauerte Abstellnischen ohne Tür werden KEIN_RAUM. Zusatz: Ist ein „über Dach“ außerhalb der Fassade gezeichneter Schachtverzug Schacht des Geschosses oder Außenbereich? Planerfrage: `rest_5` überdeckt 0,26 m² eines gezeichneten Schachtkastens - trifft „sonst nichts“ (DG2-6) zu? | S12 (U5); S3b (nur bei a) |
| F5 | Leonis, Enis | Welche Geometrie ist die Raumfläche an Fenster- und Dachschrägenseiten? | Optionen A-D siehe U9 (Zone / lichte Innenfläche / mit Nischen / Zone plus Zusatzkontur). Teilfragen: (1) Zählt die Fläche unter der Dachschräge (Dachschnitt-Band, Dachfenster) zur Raumfläche? (2) Gehören Fensternischen dazu, bis Rahmenlinie oder Außenflucht? (3) Ist der Streifen zwischen Dachschnitt-Außenkante (−462 mm) und Roof-Umriss/Baulinie (+1358/+1359 mm), im Plan als New_255-HATCH DOUBLE_1_8 (32,35 m²) gezeichnet, Außenbereich oder niedrige Innenfläche? B/C ändern Stempelabweichungen (DG2 −27 bis −30 %); D berührt den Contract nicht. | U9; DG2-1, DG2-2, DG2-8, Raumkanten-Teil OG1-4 |
| F6 | Enis (Norm, final_exit), Leonis, Owner | Welche Zonen sind „innen“ und dürfen nie im Außenbereich liegen? | **Option 1** Leonis' Liste inklusive Balkon/Terrasse/Loggia: entspricht dem Feedback; Mollgasse TERRASSE TOP 1 liegt 10 mm an der Hoftür Cluster B → final_exit-Risiko. **Option 2** nur Zonen mit Nutzungsklasse ≠ AUSSEN: konsistent mit `nutzungsklasse.py`, widerspricht S-C bei Freiflächen. **Option 3** alle gestempelten Zonen: EIGENGARTEN/VORPLATZ würden innen, widerspricht Leonis; keine Obermenge von Option 1 (ungestempeltes DG2 `stiegenhaus_2` fiele heraus). **Option 4** Typliste aus Option 1 ohne Freiflächen ∪ gestempelte Räume ohne Außen-Vokabular ∪ Räume mit Sanitär-/Möbel-Beleg: setzt S-C wörtlich um („Raum mit Stempel oder mit Möbeln/Sanitär ist innen“), deckt bei einem Fensterleck ohne Loch auch KÜCHE, GANG, TECHNIK und untypisierte gestempelte Räume („Wohnkche“, „TV Raum“) und entspricht der Innen-Definition von M2. Trade-offs: Die Möbel-/Sanitär-Regex ist familienabhängig (M2-Regex aus ArchiCAD-Blocknamen einer Familie; Einfügepunkte liegen 391-836 mm neben der Block-Mitte). Das Außen-Vokabular (M2 `AUSSEN_STEMPEL`: HOF, ZUGANG, EINFAHRT, MÜLLPLATZ, GARTEN, VORPLATZ) ist nur aus Rennweg abgeleitet; Mollgasse EIGENGARTEN/VORPLATZ/TERRASSE hängen genau an dieser Liste. Möbel auf Freiflächen (EG `raum_17` „HOF/Terrasse“ mit runden Tischen) würden eine Freifläche innen machen. Messbezug für S2: B.2 misst Option 1 ohne Freiflächen; Option 1 mit Freiflächen, 2 und 4 sind Obermengen (`wert` bleibt 2, offene Fläche neu messen), Option 3 ist neu zu messen. Zusatz: Bleibt die Nutzungsklasse AUSSEN für BALKON/TERRASSE/LOGGIA (A nur geometrisch ausschneiden / B neue Klasse FREIFLAECHE mit Contract-Bump und Umbau `tuer_typisierung`, `wohnungen`, Platzierung / C nur Darstellung)? Loggia wie Balkon? Auskragende Freiflächen außerhalb der Hülle eigen darstellen? Braucht eine EG-Terrassentür mit Geländeausgang einen Beleg vor final_exit (heute nein, Kommentar widerspricht)? | Freiflächen- und Typlisten-Teil von S2; das S2-Akzeptanzkriterium gilt für die gewählte Option (5.2 S2) |
| F7 | Enis, Leonis | Darf eine vollständig von Wänden umschlossene Freifläche ohne Außen-Indiz (Lichthof ohne Grün/Belag) AUSSEN sein? | **A** nie ohne Indiz: robust gegen dünne Fassaden, verliert indizlose Lichthöfe. **B** nur ohne Raumstempel und ohne Möbel/Sanitär: S-C wörtlich, braucht familienabhängiges Möbel-Indiz. **C** heute (Randnähe): Wohnzimmer wird Außen. | **Merge-Gate S1:** S1 setzt A um; die Bestätigung von A ist vor dem Merge einzuholen (5.1). Vor dem Merge die kippenden Loch-Teile messen (5.2 S1; nur In-Memory-Einzelfunktionen, kein Cache); jeder gemessene Hof mit Tür ins Freie braucht die Bestätigung A oder blockiert |
| F8 | Enis, Owner | Soll jede Wandöffnung für die Innen/Außen-Frage geschlossen werden? | Im OG/DG jede Öffnung brücken, im EG alles außer Toren/Durchfahrten ≥ 2,4 m? Trade-off: Balkon- und Terrassentür-Lecks verschwinden gegen Höfe, die ihren Weg ins Freie verlieren; Balkontür und Durchfahrt sind allgemein (ohne Namen) nicht unterscheidbar. | S14 |
| F9 | Leonis, Owner | Wie wird eine zonen- und stempellose Fläche behandelt, die ohne Wand und Tür an genau eine Zone grenzt (DG1: 16,76 m², offene Grenze 5,7-5,8 m zum Wohnzimmer)? | **A** eigener untypisierter Raum: Architektendaten unverändert, UNBEKANNT-Raum in der Wohnung. **B** der Zone zuschlagen: entspricht „Teil des Wohnzimmers“, Wohnzimmer 73,95 + 16,76 = 90,7 m² gegen Stempel 83,93 (+8 %), Konflikt mit Stempelschutz. **C** eigener Raum mit Typ und Wohnung des Nachbarn: Typ ohne Stempel übertragen. Zusatz (Wiedervorlage Owner-Nachentscheid `bereinigung.py:52-67`): AR-Zone liegt vollständig in der Wohnzimmer-Zone - Stempel als „inkl. AR“ lesen (Warnung statt rote Zahl)? | Nachbehandlung in S13 |
| F10 | Leonis, Enis | Ist ein offener Durchgang ohne Türblatt zwischen Wohnraum und Stiegenhaus ein Wohnungseingang? (DG2: Treppe und Lift münden ohne Tür in VR 15,2 und VR/Büro 16,0.) | **a** ja (heute): viele Eingänge je Wohnung. **b** nur mit Türblatt; offene Verbindung als gemeldeter Fall ohne Fluchtweg-Startseite: echte offene Erschließungen verlieren den Start. **c** nur, wenn keine Tür mit Blatt zum selben Stiegenhaus existiert. **d** Durchgang nur bei Wandschlitz oder Berührung: Scheinkanten an Wandkörper-Lücken bleiben. | Rollenregel nach S5b |
| F11 | Leonis, Enis, Owner | Woran unterscheidet die Engine einen Wohnungsvorraum von einem allgemeinen Vorraum/Gang, wenn beide eine Tür ins Stiegenhaus haben? | **A** Topologie allein: nachweislich unzureichend (synthetische Diele ergibt 4 Gruppen). **B** Stempeltext (VR/Garderobe/Diele privat, Gang/Flur communal): einfach, aber OG1 hat „Gang“ innerhalb der Wohnung. **C** Türmerkmal (Eingangstür 90 gegen Zimmertüren 80, T30/EI30-Text): selten im Plan. **D** TOP-/Wohnungsnummer-Text (Mollgasse-Präzedenz „00-top“; Rennweg: keine gefunden). Offenlegung: Die Regel „Stiegenhaustür → Erschließung“ stammt aus 9a5de6f; belegt ist nur die private Richtung. Risiko jeder Option: falsch privater allgemeiner Vorraum ohne Notlicht. Zusatz DG2: eine Wohnung (Maisonette mit DG1?) mit privaten Vorräumen, Vorräume als Erschließung, oder „unklar“ ohne Wohnung? Zusatz Rolle (S7c): Welche Rolle trägt eine Tür zwischen zwei allgemeinen Räumen, die heute `wohnungseingang` ist (DG2: 8 von 18, VORRAUM↔STIEGENHAUS)? **a** `stiegenhaustuer`, wenn eine Seite STIEGENHAUS ist: gleiche Rolle wie andere Stiegenhaustüren. **b** None: Die Tür zählt in keiner Rollen-Kennzahl, Wirkung auf Fluchtweg-Starts ungemessen. **c** unverändert: Kennzahl WE/Wohnung bleibt verzerrt. | S7a (U14); Zusatz: S7c |
| F12 | Leonis, Enis | (1) Ist eine Gruppe ohne Aufenthaltsraum (nur KÜCHE/WC/AR/BAD) eine Wohnung? (2) Welche Klasse haben solche Räume ohne Wohnungskontext (UG Personal-WC, EG „v.Küche“ am Geschäftslokal)? | (1) **a** nein, keine `wohnung_id`; **b** ja (heute); **c** nur mit Eingangstür mit Türblatt. (2) **a** None: Leonis fällt auf Default; **b** ALLGEMEIN_NEBENRAUM: Notlicht, überplant echte Privaträume; **c** WOHNUNG_PRIVAT (heute): kein Notlicht in allgemeinen WC. Zusatz: Darf das UG Wohnungen haben? | S7b (U16) |
| F13 | Selman, Leonis | Darf ein untypisierter Raum mit Stempel, der nur an Räume einer Wohnung grenzt, deren `wohnung_id` erhalten? | **a** generell: EG „Geschäftslokal 1“ an „v.Küche“ würde Wohnung. **b** nur bei Wohn-Vokabular im Stempel: Tippfehler brauchen Unschärfe, die auch „Waschküche“/„Teeküche“ trifft. **c** nein, erst Typisierung (S6a/S6b). Hinweis: Die Wohnungszugehörigkeit ändert Leuchten nicht (`flaechen_strategy.py:161-165` filtert nach Klasse). | Brücke nach S6a/S6b |
| F14 | Enis (Norm), Leonis (Konsum), Selman | Wie wird ein gestempeltes „Geschäftslokal“ geführt? | **A** neuer Typ + neue Nutzungsklasse (Nichtwohn-Nutzungseinheit): sauber, Contract-Bump mit 3 Owner, neue Tür-Regeln. **B** neuer Typ + ALLGEMEIN_NEBENRAUM: kein Contract, semantisch falsch, praktisch ohne Wirkung (keine Tür-Regel). **C** vorhandener Typ (ZIMMER/LAGER/TECHNIK): nicht empfehlenswert (Scheinwohnung bzw. LB-Regel SL-13). **D** Status quo + Hinweis im Prüfbericht (fail closed): keine Tür-Rollen, Ausgänge, Leuchten. **E** Typ neutral + Nutzungsart je Raum/Nutzungseinheit mit dem vorhandenen Literal aus `projekt_kontext.py` (Z.25-45): koppelt an OIB-RL2 Tab. 6 Z.4/5.1 und R 12-2 Fußnote c, Contract-Touch. Zusatz: Verkaufsstätte (Z.4 erst > 200 m² Verkaufsfläche) oder Schank-/Speisewirtschaft (Z.5.1, Verabreichungsplätze; `raum_12` wie Gastronomie möbliert)? AStV-Arbeitsstätte? Ist „v.Küche“ Betriebsküche des Lokals? | U17 |
| F15 | Enis, Leonis; Selman für Synonyme | Übrige UNBEKANNT-Stempel (UG „WR-H“, „WR-D“, „WR-H /Umkleide“, „Dusche-H“, „Umkleide-D“, „DBA Raum“; EG „Müllplatz“, „Zugangsweg“, „Garageneinfahrt“). | Sanitär: **a** Kürzel WR bleibt verworfen, Auflösung über `kuerzel_entscheid` mit Beleg; **b** neuer Typ SANITAER (communal): aktiviert sofort Leonis' WC-Typen und die R-12-2-Sanitärregel ab 8 m² (größter WR-H 5,78 m²), VOKABULAR „Defensiv-Synonyme“ anpassen; **c** auf WC/BAD: statisch privat, Scheinwohnung. Umkleide: eigener Typ oder untypisiert; Schwelle 8 m² (INOTEC-Bildlehre, Sekundärquelle) oder 60 m² (ONL). DBA Raum: TECHNIK (SL-13) oder eigener Typ. Außenflächen: Vorentscheid „korrekt untypisiert“ (`OFFENE_FRAGEN.md` Z.417-418) bestätigen oder AUSSEN-Typ; vorgelagert: soll die zweite EG-Zeichnung (1,38 km entfernt) ausgewertet werden? Synonyme: „Wohnbereich“/„TV Raum“ → WOHNZIMMER oder ZIMMER (downstream gleichwertig). | Vokabular-Erweiterungen; Zieltyp in S6b (Default WOHNZIMMER, nicht blockierend) |
| F16 | Enis (Norm), Leonis (Gang-RZ) | Ist ein Wohnungsflur/-vorraum Fluchtweg (`ist_fluchtweg`)? Rückfrage OG1-3: Was ist an „Gang 6,5“ falsch? | **A** nein für WOHNUNG_PRIVAT: Norm-Lookup GANG fällt auf Default, keine Flächenleuchte, keine Gang-Anker. **B** ja: Wohnungsflur bekommt weiter Flächenleuchte/RZ/Anker, Widerspruch zu `test_soll_keine_leuchten_in_wohnung_privat`. Rückfrage Leonis: (A) kein Fluchtweg, (B) Wohnungszugehörigkeit am Übergang zur Wohnküche, (C) Ausdehnung bzw. Schächte H1/WP ausgrenzen, (D) als korrekt gemeint. | `ist_fluchtweg`-Teil von S8 |
| F17 | Leonis | Rückfragen zum Wortlaut | (a) EG-1: War die ganze „v.Küche“ als Schacht gemeint oder nur das Schachtdreieck am Ostende? (b) OG1-4: Meint „schon früher abgegrenzt“ die ungeschraffierte 480-mm-Wandschicht oder die blaue Außenfläche? (c) DG2-8: Dachfenster der Straßenseite oder Terrassentür 2,30? (d) DG2-6: roter Schachtkasten „über Dach“ (siehe F4). | Zuordnung der Punkte |
| F18 | Leonis, Owner | Welche Türbreite führt das Modell für ArchiCAD-Türblöcke? | **a** Nennmaß aus Marker-ATTRIB (80/90 cm): planentsprechend, braucht Erzeuger für `BreiteQuelle` „ATTRIBUT“ (reserviert), bricht `test_wandkoerper.py` Z.68. **b** Blattradius (840/940 mm, heute GEOMETRIE_SCHWENKRADIUS): 40 mm über Nennmaß. | nicht blockierend für S4a |
| F19 | Selman | **Entschieden 2026-09-15: Option a.** Vorher-Zahlen nur Rennweg; übrige Pläne nach Fix-Freigabe im regulären Lauf als Vorher/Nachher. Ursprüngliche Frage: Umfang der Vorher-Messung (S-D): Sollen vor den Slices Caches für weitere Familien erzeugt werden, damit M1-M3 und die Türfolgen über Rennweg hinaus messbar sind? | **a** Nur Rennweg-Caches (heute) plus M5 über 83 `kennzahlen.json`: sofort verfügbar, aber M1-M3 und die Türfolgen sagen nichts über andere Familien. Das S1-Gate ist nicht betroffen (Loch-Test nur mit Einzelfunktionen, kein Cache, 5.2 S1). Die Gate-Messungen für S2/S9/S11a/S14 liefen auf Rennweg mit Cache-Räumen bzw. Cluster-Skripten; ob sie ohne Cache in-memory (`raeume_aus_kaskade`) messbar sind, ist nicht erprobt. **b** Stufe 1 zusätzlich für je einen Plan je Familie (Barawitzka EG, Mollgasse EG, Muthgasse E2, je ein Fischamend-BT1/BT2-Plan): deckt die Merge-Gates ab; Laufzeit mittel; `pytest` nie parallel zu großen DXF-Läufen. **c** Stufe 1 für alle 83 Pläne: vollständige Basis, Laufzeit und Speicher am höchsten, Duplikate (2 Paare byte-gleich) mitgezählt. | nichts (entschieden) |
| F20 | Enis (Grenzen), Leonis (Konsum), Selman | Soll die Erkennung eine Warn-Kennzahl „Fläche ungewöhnlich für den Typ“ führen (nur Hinweis, keine Typänderung)? Heute gibt es keine solche Prüfung (1.5). | **a** Nein (heute): keine Fehlwarnungen, aber Fälle wie STIEGENHAUS 0,73 m² bleiben still. **b** Mindest- und Höchstfläche je Typ als Warnung, Grenzen von Enis: fängt die M1- und U5-Fälle; die Grenzen sind nutzungs- und familienabhängig (DG2 BAD 24,00 m² ist gestempelt). **c** Nur für geometrisch typisierte Räume (R-Stufe, Treppen-Bbox, Lift), nicht für gestempelte Zonen: trifft genau die Fälle ohne Architektenbeleg, weniger Fehlwarnungen. | nichts; optionaler Zusatz zu M1/M3 |

---

## 7. Verworfene Erklärungen, Grenzen, nicht Getanes

### 7.1 Verworfene Erklärungen

| Erklärung | Herkunft | Warum verworfen |
|---|---|---|
| „Stiegenhaus 1,0/1,2/4,0 m²“ sind Treppenblock-Extents als Polygon | S-H1 | Rasterpolygone (60-95 Ecken, Hülle nicht achsparallel, Treppen-Randanteil ≤ 0,022); nur der Typ stammt aus dem Bbox-Zentrum (U2) |
| Wandmaske mit Fensterlücken schneidet Zimmer 16,9 / Bad 24 / Zimmer 59,3 / Wohnzimmer 73,9 ab | S-H2 | Raumpolygone sind unveränderte Zonen (Quelle L), identisch mit `raeume_aus_layer`; Außenanalyse ändert sie nicht |
| DG2-Straßenband entsteht durch die Fenster | S-H2 | Dachfenster ab −800 mm geschlossen; Band = Zone über dem Dachschnitt (U9) ohne Zonenabzug (U8) |
| DG1 Wohnzimmer flutet über ein offenes Fensterleck | Cluster K3 („193-mm-Restbrücke“) | Teil ist ein geschlossenes Loch; 193 mm = Abstand zum Hüllrand, offen nur über die 250-mm-Toleranz (U7) |
| „Schacht 1,4 m²“ ist eine rote Fensterblock-Kontur | S-H3 | Keine Farbregel, keine roten Konturen in Blöcken; SCHACHT über „< 3 m², türlos“ (U5) |
| Schacht-Texte/rote Entities stecken in verschachtelten Blöcken | S-H3 | Alle im Modelspace (0 Treffer in Blöcken) |
| DG2 `top_1` umfasst das ganze Geschoss inkl. Stiegenhaus und Lift | S-H4 | Daten 4 Räume; Umriss-Scheinbild (U20); 2,26 m² Überdeckung aus U1 |
| „Wohnküche war früher KÜCHE“ (Regression) | S-B1 | Plantext ohne ü seit dem Asset-Commit; kein Code-Commit; älterer Output ebenfalls UNBEKANNT |
| Tür-Inserts 300 m neben dem Haus sind ein zweiter Plan-Cluster | Docstring `tueren.py:366-368`, Commit e51d3ee | Es sind die echten Türen (INSERT-Punkt eines Weltkoordinaten-Blocks, Geometrie im Haus; OG3 = T1..T11 des Soll-Tests) |
| „Rasterzufall“ entscheidet über das Anhängen von `stiegenhaus_2` | Cluster K1 | DG2-Mittelpunkt liegt gemessen im Wandkörper |
| Typisierung über den größten Hüllen-Schnitt ändert nur DG2 | Cluster K1 | UG `raum_17` „DBA Raum“ würde STIEGENHAUS |
| Stufenlinien trennen Läufe (≥ 35 m) von Schächten (0 m) allgemein | Cluster K1 | Stichprobe verzerrt; UG `raum_17` trägt 58,8 m gestrichelte Projektionslinien |
| Schachtwand der EG-Küche ist `Wall_32` („New_015 Innenwände“) | Cluster K2a | Gemessen `Wall_90`/`Wall_91` („New_010 Aussenwände“) und `Wall_64` |
| OG1 WC: vier Kleinzellen mit Rahmen (0,161 m²) | Cluster K2a | Zwei mit Schnittfläche (0,065 m²), zwei nur berührend |
| Zwischen OG1 Zimmer 16,1 und 10,6 liegt eine Wand ohne Tür | Cluster K5 | Plan zeigt Zargentür 80/2,20; Verbindung richtig, Breite falsch |
| Dachfenster-Lücken ohne Wandkörper 8-10 m | Cluster K4 | Messmethodenabhängig; entlang der Achse 1343 mm je Dachfenster |
| Veto aus rohen Raumpolygonen ist risikoarm | Cluster K3/K4 | Ohne Aufnahme in `gedeckt()` wirkungslos; ohne Clip verschluckt es den DG2-Dachstreifen |
| Defensiver Ring-Fix in `aussen_durchgaenge` beseitigt die Stiegenhaus-Außenöffnungen | Cluster K4 | Gemessen identisch zum Loch-Test; wirkungslos für DG1 `rest_2` und OG1 `rest_1` |
| Außenbereich verändert die Wohnungsbildung nicht | Cluster K4 | Simulation mit fertiger Nutzungsklasse; im echten Lauf nicht belastbar (U19) |
| Vorraum privat bei „n_stgh ≤ 1 und n_privat ≥ 1“ bzw. „genau eine private Gruppe ohne r“ | Cluster K5, K5-Linse 2 | bricht `test_zwei_wohnungen_getrennt` bzw. scheitert an der synthetischen Diele |
| Absoluter Filter „Durchgang muss beide Räume berühren“ | Cluster K5 | löscht den echten Wohnungseingang OG1 `durchgang_22` |
| M3-Hauptzahl 49 (Text-Räume), M2 „79 % in der Gebäudehülle“ | Messagenten | 16 Falsch-Positive bzw. Freiflächen in der Hülle; korrigiert auf 34 bzw. 69,3 % |

### 7.2 Grenzen

- Nur Rennweg per Package-Funktion gemessen. Wirkung der Fixes auf Barawitzka, Mollgasse, Muthgasse, Fischamend, Baufeld/Herrenholz nicht gemessen; vorhandene Aussagen dazu stammen aus eingecheckten Ergebnissen, Code-Lektüre oder Textzählung.
- Keine Fix-Wirkung simuliert, außer: Loch-Test S1 und Loch-Test mit Veto und Zuschnitt S2 (in-memory, alle 7 Pläne, B.1/B.2), `_typisiere` ohne Marker und mit Schacht-Text (B.3), 4er-Label (DG2, B.4), Schacht-Ausstanzung nur als Durchgangs-Simulation (B.12), Brücken-/Barriere-Gegenproben (Cluster K4, Ausgabe B.11; nicht unabhängig nachgerechnet). Türfolgen von S1/S2 sind nicht nachgerechnet.
- Türen sind nicht im Cache; Tür- und Wohnungsaussagen stammen aus in-memory-Rekonstruktionen mit Cache-Räumen (Abgleich `wohnung_id` identisch) oder aus dem Bericht vom 8. Sep. Stiegenhaus-Modelle und Anker wurden mit `tueren=[]` gebaut.
- Platzierung (Leuchten, RZ, Anker) nicht ausgeführt; alle Aussagen zu Leonis' Strategien sind Code-Pfade.
- `Projekte/_eingang/Rennweg_OG3.dxf` (Soll-Tests) ist nicht byte-gleich mit `Projekte/Rennweg/OG3 …` (4 Byte); die 11 Phantom-Zargentüren sind nur für die Projekte-Version gemessen.
- EG: zweiter Grundriss (1,38 km) nicht untersucht (`top_1` mit 5 Eingängen, Müllplatz/Zugangsweg/Garageneinfahrt); `im_planbereich` ist dort wirkungslos.
- Nicht erklärt: UG `rest_1` 27,79 / `rest_2` 20,08 / `rest_5` 15,23 m² und OG3 `rest_4` 10,09 m² (stempellose Resträume); OG2 `top_2` Einraum-ZIMMER 22,22 m²; Schachtstreifen in OG2/OG3-Stiegenhäusern; Warum dieselbe Treppen-Bbox-Mitte (DG1 `Stair_1`, DG2 `Stair_2`, gleiche Extents) in DG1 in `rest_2` liegt, in DG2 im Wandkörper; Lage des Aufbruchs der DG1-R-Kontur; Materialbedeutung der ungeschraffierten 480-mm-Schicht in OG1 `Wall_5`; Ursache des früheren Barawitzka-Hofverlusts bei Veto-Varianten.
- Ungeprüft: Anker im Liftring mit echten Türen; kreuzcheck auf Rennweg; Darstellung schlitzkodierter Löcher; Linientyp-Unterscheidung (durchgezogen/gestrichelt) über Familien; Wirkung der Tokens DOOR/OPENING auf andere Familien; Texte „20R x 15“/„19G x 175“ an `Stair_1` nur vom Cluster gelesen.
- „30 von 75“ (HANDOFF 4.1) nachgezählt (M5, Bestand 1e642ad): 30 und 75 reproduziert (75 = 83 − 8 Fehler-Stubs ohne `tuer_typen`); das Verhältnis ist nur auf 52 Dateien berechenbar, 23 haben kein Feld `wohnungseingang`. Ursache außerhalb Rennweg nicht untersucht. M1-M3 für andere Familien ohne Cache nicht messbar; laut Entscheid F19 (2026-09-15) nach Fix-Freigabe im regulären Lauf.
- `pytest` nicht ausgeführt; Aussagen „bleibt grün“ sind logische Prüfungen.

### 7.3 Nicht getan

- Kein Code geändert, kein Output unter `Projekte/` erzeugt. Einzige Repo-Änderung: dieses Dokument als eigener Commit auf `selman/diagnose-rennweg`; kein Push.
- `ArchitekturRaumProvider.parse`, `hauptengine.pipeline.run`, `scripts/analyse/*.py`, `scripts/plan_pruefen.py`, `pytest` nicht ausgeführt.
- Keine Fachfrage entschieden; Default-Vorschläge in 5.2 sind zur Bestätigung markiert.

---

## Anhang A: Messskripte

Die Skripte liegen außerhalb des Repos (Scratchpad dieser Analyse); der Quelltext ist hier vollständig wiedergegeben, damit die Nachher-Messung identisch läuft. A.1-A.4 sind die Vorher-Messungen M1-M4; A.5-A.10 sind die Diagnose-Skripte hinter Anhang B und den Ursachen (Akzeptanzkriterien S1/S2: A.5, S3a: A.6, S7c: A.7). Ablage im Repo nach Owner-Entscheid. Voraussetzung: Caches unter `Projekte/_ergebnis_raumerkennung/` mit dem zu messenden Code neu erzeugt (Stufe 1 `scripts/analyse/raumerkennung_darstellung.py`). `PY` = `D:/KI Projekt/Notbeleuchtung/.venv/Scripts/python.exe`. Nur lesen; ein Python-Prozess zur Zeit.

### A.1 M1-stiegenhaus-achsparallel

Aufruf (PowerShell):

```powershell
& "$PY" "./M1-stiegenhaus-achsparallel/_messen.py" nachher_<commit>.json
```

Vorher-Datei (Output 511ad36): `ergebnis.json`

```python
"""M1-stiegenhaus-achsparallel — achsparallele STIEGENHAUS-Polygone in gedrehten Plaenen.

Nur lesen. Grundmenge: alle _cache.pkl unter Projekte/_ergebnis_raumerkennung (rglob).
Aufruf:  PY _messen.py [out.json]      (Default: ergebnis.json neben diesem Skript)
Repo:    Umgebungsvariable NOTBEL_REPO, sonst D:/KI Projekt/Notbeleuchtung

Definitionen (unveraendert fuer Vorher/Nachher):
  Kantenwinkel     a = atan2(dy, dx) in Grad mod 90; Kanten < 1 mm ignoriert; Gewicht = Laenge.
  Rotation         Bin = round(a*2)/2 mod 90 (0,5-Grad-Bins); dominanter Bin = argmax Gewicht.
                   Abstand = min(w, 90-w); "gedreht" <=> Abstand > 3 Grad.
    - plan:        ueber alle Raumpolygon-Kanten des Plans (Vorgabe).
    - cluster:     Raumpolygone je Zusammenhangskomponente von union(buffer 1000 mm) —
                   trennt mehrere Grundrisse in einem Modelspace. Kantensumme < 20 m -> Plan-Wert.
                   MASSGEBLICH fuer "im gedrehten Plan".
    - wand_dxf:    Gegenprobe: Kanten der Wand-Layer-Entities (lade_dxf.wall_entities), INSERTs
                   eine Ebene aufgeloest (LINE/LWPOLYLINE/POLYLINE), verschachtelte INSERTs nicht.
  achsparallel     (Vorgabe) Anteil der Kantenlaenge mit min(a, 90-a) <= 1 Grad; achsparallel <=> >= 0,90.
  achsparallel_huelle  dieselbe Regel auf der konvexen Huelle (robust gegen gedreht ausgestanzte
                   Lifte/Schaechte in einem achsparallelen Rechteck).
  planparallel     Anteil der Kantenlaenge innerhalb +-1 Grad der massgeblichen Rotation (mod 90) — Info.
  Praefix          re.match(r"^([A-Za-z]+)_", id) -> Gruppe 1, sonst "(ohne)".
  Treppen-BBox     geometrie_typ.stiege_rechtecke(plan). treppen_rand_anteil = max ueber Rechtecke von
                   Laenge(Rand(Polygon) geschnitten mit Rand(Rechteck).buffer(10 mm)) / Laenge(Rand(Polygon));
                   "aus_treppen_bbox" <=> treppen_rand_anteil >= 0,5. treppen_bbox_iou = IoU(envelope, Rechteck) nur Info.
  Zusatz klein     STIEGENHAUS, flaeche_m2 < 2,0 und kein Cache-Stempel mit raum_id == id.
                   beruehrt_lift <=> shapely-Abstand zu irgendeinem LIFT-Polygon <= 300 mm.
                   schacht_text  <=> Text (TEXT/MTEXT/ATTRIB, rekursiv in INSERTs bis Tiefe 6,
                   Einfuegepunkt) mit Abstand zum Polygon <= 500 mm und Treffer SCHACHT_TEXT.
"""
from __future__ import annotations

import json
import math
import os
import pickle
import re
import sys
import time
from collections import Counter
from pathlib import Path

from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

REPO = Path(os.environ.get("NOTBEL_REPO", r"D:\KI Projekt\Notbeleuchtung"))
ERGEBNIS = REPO / "Projekte" / "_ergebnis_raumerkennung"

GEDREHT_GRAD = 3.0
ACHS_TOL_GRAD = 1.0
ACHS_ANTEIL = 0.90
CLUSTER_PUFFER_MM = 1000.0
CLUSTER_MIN_KANTEN_MM = 20_000.0
TREPPEN_RAND_MM = 10.0
TREPPEN_RAND_ANTEIL = 0.5
KLEIN_M2 = 2.0
LIFT_ABSTAND_MM = 300.0
ZAEHL = ("achsparallel", "achsparallel_im_gedrehten", "achsparallel_huelle",
         "achsparallel_huelle_im_gedrehten", "aus_treppen_bbox")
TEXT_ABSTAND_MM = 500.0
TEXT_TIEFE = 6
# Schacht-Kuerzel nach der Service-Marker-Liste im Port
# (_port/parsers/architecture_dxf.py _SERVICE_MARKER_KIND_ALIASES, Z. 2667-2671).
SCHACHT_TEXT = re.compile(
    r"SCHACHT|INSTALLATION|(?<![A-Z])(?:DDB|BDB|FBDB|WDB|FDB|DBA|HKLS)(?![A-Z])"
    r"|\b(?:DD|BD|FBD|WDD|WODD)\s*(?:[-/]\s*)?(?:HT|ET)?\s*\d",
    re.IGNORECASE)


def kanten(pts, geschlossen=True):
    n = len(pts)
    for i in range(n if geschlossen else n - 1):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        l = math.hypot(x2 - x1, y2 - y1)
        if l >= 1.0:
            yield math.degrees(math.atan2(y2 - y1, x2 - x1)) % 90.0, l


def rotation(kantenlisten) -> dict:
    bins: Counter = Counter()
    tot = 0.0
    for ks in kantenlisten:
        for a, l in ks:
            bins[(round(a * 2) / 2) % 90.0] += l
            tot += l
    if tot <= 0:
        return {"winkel_mod90": None, "anteil": 0.0, "abstand_0_90": None, "gedreht": None,
                "kanten_m": 0.0}
    w, g = bins.most_common(1)[0]
    ab = min(w, 90.0 - w)
    return {"winkel_mod90": w, "anteil": round(g / tot, 3), "abstand_0_90": ab,
            "gedreht": ab > GEDREHT_GRAD, "kanten_m": round(tot / 1000, 1)}


def diff90(a, b):
    d = abs(a - b) % 90.0
    return min(d, 90.0 - d)


def poly(pts):
    if len(pts) < 3:
        return None
    p = Polygon(pts)
    return p if p.is_valid else p.buffer(0)


def wand_rotation(plan) -> dict:
    def ks():
        for e in plan.wall_entities():
            ents = [e]
            if e.dxftype() == "INSERT":
                try:
                    ents = [v for v in e.virtual_entities()
                            if v.dxftype() in ("LINE", "LWPOLYLINE", "POLYLINE")]
                except Exception:  # noqa: BLE001
                    continue
            for v in ents:
                pts = plan.entity_points(v)
                if len(pts) >= 2:
                    yield list(kanten(pts, geschlossen=False))
    return rotation(ks())


def schacht_texte(plan) -> list[dict]:
    f = plan.factor
    out: list[dict] = []

    def add(txt, ins, layer, pfad):
        if txt and SCHACHT_TEXT.search(txt):
            out.append({"text": txt.strip()[:80], "xy_mm": [round(ins[0] * f), round(ins[1] * f)],
                        "layer": layer, "pfad": pfad})

    def walk(ents, pfad, tiefe):
        for e in ents:
            t = e.dxftype()
            try:
                if t == "INSERT":
                    for at in e.attribs:
                        add(at.dxf.text, at.dxf.insert, at.dxf.layer, pfad + [e.dxf.name])
                    if tiefe < TEXT_TIEFE:
                        walk(list(e.virtual_entities()), pfad + [e.dxf.name], tiefe + 1)
                elif t in ("TEXT", "ATTRIB"):
                    add(e.dxf.text, e.dxf.insert, e.dxf.layer, pfad)
                elif t == "MTEXT":
                    add(e.plain_text(), e.dxf.insert, e.dxf.layer, pfad)
            except Exception:  # noqa: BLE001
                continue
    walk(list(plan.space), [], 0)
    return out


def dxf_pfad(ordner: Path, kz: dict) -> Path | None:
    kand = [REPO / "Projekte" / ordner.parent.name / f"{ordner.name}.dxf"]
    if kz.get("dxf"):
        kand.append(REPO / kz["dxf"])
    return next((p for p in kand if p.exists()), None)


def messe_plan(cache_pfad: Path) -> dict:
    t0 = time.time()
    ordner = cache_pfad.parent
    kzp = ordner / "kennzahlen.json"
    kz = json.loads(kzp.read_text(encoding="utf-8-sig")) if kzp.exists() else {}
    c = pickle.loads(cache_pfad.read_bytes())
    raeume = c["raeume"]
    geo = {r["id"]: g for r in raeume if (g := poly(r["polygon_mm"])) is not None and not g.is_empty}
    stempel_je = Counter(s["raum_id"] for s in c["stempel"] if s.get("raum_id"))

    rot_plan = rotation(list(kanten(r["polygon_mm"])) for r in raeume)

    # Cluster (mehrere Grundrisse je Modelspace)
    u = unary_union([g.buffer(CLUSTER_PUFFER_MM) for g in geo.values()])
    komps = list(getattr(u, "geoms", [u]))
    cluster_von = {rid: next((i for i, k in enumerate(komps) if k.covers(g.representative_point())), -1)
                   for rid, g in geo.items()}
    cluster_rot = {}
    for i in range(len(komps)):
        ids = [r for r in raeume if cluster_von.get(r["id"]) == i]
        cr = rotation(list(kanten(r["polygon_mm"])) for r in ids)
        cr["n_raeume"] = len(ids)
        cr["fallback_plan"] = cr["kanten_m"] * 1000 < CLUSTER_MIN_KANTEN_MM
        cluster_rot[i] = cr

    dxf = dxf_pfad(ordner, kz)
    plan = None
    fehler = []
    if dxf is not None:
        from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
        plan = lade_dxf(dxf)
    else:
        fehler.append("DXF nicht gefunden")
    rot_wand = wand_rotation(plan) if plan is not None else None
    treppen = []
    if plan is not None:
        try:
            from notbeleuchtung.raumerkennung.geometrie_typ import stiege_rechtecke
            treppen = [Polygon(rect) for rect, _c, _a in stiege_rechtecke(plan)]
        except Exception as e:  # noqa: BLE001
            fehler.append(f"stiege_rechtecke: {e!r}")

    lifte = [geo[r["id"]] for r in raeume if r["typ"] == "LIFT" and r["id"] in geo]
    stg = [r for r in raeume if r["typ"] == "STIEGENHAUS"]
    klein_kand = [r for r in stg if r["flaeche_m2"] < KLEIN_M2 and not stempel_je.get(r["id"])]
    texte = schacht_texte(plan) if (plan is not None and klein_kand) else []

    zeilen = []
    for r in stg:
        g = geo.get(r["id"])
        ks = list(kanten(r["polygon_mm"]))
        tot = sum(l for _a, l in ks) or 1.0
        achs = sum(l for a, l in ks if min(a, 90.0 - a) <= ACHS_TOL_GRAD) / tot
        ci = cluster_von.get(r["id"], -1)
        cr = cluster_rot.get(ci)
        mass = rot_plan if (cr is None or cr["fallback_plan"]) else cr
        plan_par = (sum(l for a, l in ks if diff90(a, mass["winkel_mod90"]) <= ACHS_TOL_GRAD) / tot
                    if mass["winkel_mod90"] is not None else None)
        m = re.match(r"^([A-Za-z]+)_", r["id"])
        z = {"id": r["id"], "praefix": m.group(1) if m else "(ohne)",
             "flaeche_m2": round(r["flaeche_m2"], 2), "n_ecken": len(r["polygon_mm"]),
             "bbox_mm": [round(v) for v in g.bounds] if g is not None else None,
             "achsparallel_anteil": round(achs, 3), "achsparallel": achs >= ACHS_ANTEIL,
             "planparallel_anteil": round(plan_par, 3) if plan_par is not None else None,
             "cluster": ci, "rotation_massgeblich": mass["winkel_mod90"],
             "im_gedrehten_plan": bool(mass["gedreht"]),
             "stempel_n": stempel_je.get(r["id"], 0), "wohnung_id": r.get("wohnung_id")}
        z["achsparallel_im_gedrehten"] = z["achsparallel"] and z["im_gedrehten_plan"]
        hks = list(kanten(list(g.convex_hull.exterior.coords)[:-1])) if g is not None else []
        htot = sum(l for _a, l in hks) or 1.0
        hachs = sum(l for a, l in hks if min(a, 90.0 - a) <= ACHS_TOL_GRAD) / htot
        z["achsparallel_huelle_anteil"] = round(hachs, 3)
        z["achsparallel_huelle"] = hachs >= ACHS_ANTEIL
        z["achsparallel_huelle_im_gedrehten"] = z["achsparallel_huelle"] and z["im_gedrehten_plan"]
        if g is not None and treppen:
            env, rand = g.envelope, g.boundary
            ious = [env.intersection(t).area / env.union(t).area for t in treppen]
            rant = [rand.intersection(t.exterior.buffer(TREPPEN_RAND_MM)).length / rand.length
                    for t in treppen]
            z["treppen_bbox_iou"] = round(max(ious), 3)
            z["treppen_rand_anteil"] = round(max(rant), 3)
            z["aus_treppen_bbox"] = max(rant) >= TREPPEN_RAND_ANTEIL
        else:
            z["treppen_bbox_iou"], z["treppen_rand_anteil"], z["aus_treppen_bbox"] = None, None, False
        if r in klein_kand and g is not None:
            dl = min((g.distance(lg) for lg in lifte), default=None)
            nah = [dict(t, abstand_mm=round(g.distance(Point(t["xy_mm"]))))
                   for t in texte if g.distance(Point(t["xy_mm"])) <= TEXT_ABSTAND_MM]
            z["klein_ohne_stempel"] = {
                "lift_abstand_mm": round(dl) if dl is not None else None,
                "beruehrt_lift": dl is not None and dl <= LIFT_ABSTAND_MM,
                "schacht_text": bool(nah), "schacht_texte": nah}
        zeilen.append(z)

    def summe(rows):
        return {"n": len(rows), "m2": round(sum(x["flaeche_m2"] for x in rows), 2)}

    je_praefix = {}
    for p in sorted({z["praefix"] for z in zeilen}):
        rows = [z for z in zeilen if z["praefix"] == p]
        je_praefix[p] = {"gesamt": summe(rows)} | {k: summe([z for z in rows if z[k]]) for k in ZAEHL}
    klein = [z for z in zeilen if "klein_ohne_stempel" in z]
    return {
        "plan": ordner.name, "projekt": ordner.parent.name, "commit_output": kz.get("commit"),
        "dxf": str(dxf) if dxf else None, "fehler": fehler,
        "rotation_plan_raumkanten": rot_plan, "rotation_wand_dxf": rot_wand,
        "cluster": {str(i): cr for i, cr in cluster_rot.items()},
        "treppen_rechtecke_n": len(treppen),
        "treppen_rechtecke_bbox_mm": [[round(v) for v in t.bounds] for t in treppen],
        "stiegenhaus": {"gesamt": summe(zeilen)}
                       | {k: summe([z for z in zeilen if z[k]]) for k in ZAEHL}
                       | {"je_praefix": je_praefix},
        "klein_ohne_stempel": {
            "n": len(klein),
            "beruehrt_lift": sum(z["klein_ohne_stempel"]["beruehrt_lift"] for z in klein),
            "schacht_text": sum(z["klein_ohne_stempel"]["schacht_text"] for z in klein)},
        "schacht_texte_im_plan_n": len(texte) if klein_kand else None,
        "polygone": zeilen, "dauer_s": round(time.time() - t0, 1),
    }


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("ergebnis.json")
    plaene = [messe_plan(p) for p in sorted(ERGEBNIS.rglob("_cache.pkl"))]
    tot = {k: {"n": sum(p["stiegenhaus"][k]["n"] for p in plaene),
               "m2": round(sum(p["stiegenhaus"][k]["m2"] for p in plaene), 2)}
           for k in ("gesamt", *ZAEHL)}
    tot["plaene"] = len(plaene)
    tot["plaene_gedreht"] = sum(bool(p["rotation_plan_raumkanten"]["gedreht"]) for p in plaene)
    tot["klein_ohne_stempel"] = {k: sum(p["klein_ohne_stempel"][k] for p in plaene)
                                 for k in ("n", "beruehrt_lift", "schacht_text")}
    res = {"metrik": "M1-stiegenhaus-achsparallel", "definition": __doc__, "summe": tot,
           "plaene": plaene}
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"summe": tot, "je_plan": [
        {"plan": p["plan"][:4], "rot_raum": p["rotation_plan_raumkanten"], "rot_wand": p["rotation_wand_dxf"],
         "cluster": {i: (c["winkel_mod90"], c["n_raeume"], c["fallback_plan"]) for i, c in p["cluster"].items()},
         "treppen": p["treppen_rechtecke_n"], "stg": p["stiegenhaus"], "klein": p["klein_ohne_stempel"],
         "texte": p["schacht_texte_im_plan_n"], "fehler": p["fehler"], "s": p["dauer_s"]}
        for p in plaene]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
```

### A.2 M2-aussen-auf-innenraum

Aufruf (PowerShell):

```powershell
& "$PY" "./M2-aussen-auf-innenraum/_messen.py" --out nachher_<commit>.json
```

Vorher-Datei (Output 511ad36): `vorher_511ad36.json`

```python
"""M2-aussen-auf-innenraum — Innenraeume (Fachregel S-C) mit Schnitt zum OFFENEN Aussenbereich.

Aufruf (Repo-venv, nur lesen):
  PY _messen.py [--out <datei.json>]      Default: messung.json neben dem Skript

Grundmenge: jede Projekte/_ergebnis_raumerkennung/**/_cache.pkl (rglob, nichts hart verdrahtet).
DXF: kennzahlen.json "dxf" (relativ zum Repo), sonst Projekte/<relativer Ergebnisordner>.dxf;
     sha256 wird gegen kennzahlen.json geprueft (dxf_sha_ok).
Kein Pipeline-Re-Run. In-memory nur: dxf_load.lade_dxf (Space + Faktor, fuer Bloecke),
wandkoerper.finde_wandkoerper (nur Huelle H2).

Definition:
  Raumpolygon     = Polygon(polygon_mm).buffer(0) wie raumerkennung_darstellung._polygon (leer -> ignoriert)
  AUSSEN          = unary_union(cache["aussen_offen"])   (aussen_geschlossen zaehlt NICHT)
  schnitt_m2      = Flaeche(Raum ∩ AUSSEN) / 1e6
  beruehrt        = schnitt_m2 > SCHNITT_MIN_M2 (0.05); gross = schnitt_m2 > SCHNITT_GROSS_M2 (1.0)
  innen, wenn mind. ein Grund:
    typ      raum_typ in INNEN_TYPEN oder FREI_TYPEN
    stempel  mind. ein cache["stempel"] mit raum_id == Raum-id
    sanitaer/moebel  Einfuegepunkt (WCS, OCS->WCS, * factor) eines INSERTs, rekursiv ueber
             virtual_entities bis Verschachtelungstiefe MAX_TIEFE, liegt im Raumpolygon (covers);
             Blockname passt SANITAER bzw. MOEBEL (Sanitaer hat Vorrang), Namen mit STEMPELBLOCK
             (ArchiCAD-Zonenstempel "Bad__4") sind ausgeschlossen.
  Freiflaeche     = raum_typ in FREI_TYPEN -> getrennt ausgewiesen, zaehlt nicht in "wert".
  wert je Plan    = Anzahl innen-Raeume ohne Freiflaechen mit schnitt_m2 > 0.05.
  Huelle H1       = Union aller Raumpolygone, closing H1_CLOSE_MM (buffer +r/-r, quad_segs 2), Loecher gefuellt.
  Huelle H2       = Union finde_wandkoerper (buffer(0), simplify 20), closing H2_CLOSE_MM, Loecher gefuellt,
                    Teile >= 1 m2.  anteil = Flaeche(AUSSEN ∩ H) / Flaeche(AUSSEN).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pickle
import re
import subprocess
from collections import Counter
from pathlib import Path

from shapely import wkb
from shapely.geometry import MultiPolygon, Point, Polygon
from shapely.ops import unary_union

REPO = Path(r"D:\KI Projekt\Notbeleuchtung")
ERG = REPO / "Projekte" / "_ergebnis_raumerkennung"

INNEN_TYPEN = frozenset({"WOHNZIMMER", "ZIMMER", "SCHLAFZIMMER", "KINDERZIMMER", "BAD", "WC",
                         "ABSTELLRAUM", "VORRAUM", "STIEGENHAUS"})
FREI_TYPEN = frozenset({"TERRASSE", "BALKON", "LOGGIA"})
SCHNITT_MIN_M2 = 0.05
SCHNITT_GROSS_M2 = 1.0
MAX_TIEFE = 4
H1_CLOSE_MM = 400.0
H2_CLOSE_MM = 3000.0
WEIT_MM = 2000.0          # Einfuegepunkt weiter als das vom Block-bbox-Mittelpunkt -> Plausibilitaetswarnung

STEMPELBLOCK = re.compile(r"__\d+$")
SANITAER = re.compile(
    r"(?<![a-z])WC(?![a-z])|WASCH(BECKEN|TISCH)|DUSCH|SHOWER|WANNE|BATHTUB|URINAL|SP(Ü|UE)LE"
    r"|(?<![a-z])SINK(?![a-z])|BIDET|TOILET", re.IGNORECASE)
MOEBEL = re.compile(
    r"CHAIR|ST(U|Ü|UE)HL|TISCH|TABLE|SOFA|COUCH|BETT|(?<![a-z])BED(?![a-z])|SCHRANK|WARDROBE"
    r"|REGAL|K(Ü|UE)CHE|KITCHEN|KOCHFELD|PANEL TV|HOME-TRAINER|HANTELBANK|LAUFBAND|R(Ü|UE)CKENTRAINER",
    re.IGNORECASE)
AUSSEN_STEMPEL = re.compile(r"HOF|ZUGANG|EINFAHRT|M(Ü|UE)LLPLATZ|GARTEN|VORPLATZ", re.IGNORECASE)


def _polygon(pts):
    if len(pts) < 3:
        return None
    g = Polygon(pts).buffer(0)
    return None if g.is_empty else g


def _fuellen(g, min_m2: float = 0.0):
    gs = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
    return unary_union([Polygon(p.exterior) for p in gs
                        if p.geom_type == "Polygon" and not p.is_empty and p.area >= min_m2 * 1e6])


def _closing(g, r):
    return g.buffer(r, quad_segs=2).buffer(-r, quad_segs=2)


def _norm(name: str) -> str:
    return re.sub(r"\d+", "#", name)


def _dxf(ordner: Path, kz: dict) -> Path | None:
    kand = [REPO / kz["dxf"]] if kz.get("dxf") else []
    kand.append(ERG.parent / ordner.relative_to(ERG).parent / f"{ordner.name}.dxf")
    return next((p for p in kand if p.exists()), None)


def _inserts(plan):
    """(name, xy_mm, entity) aller INSERTs, rekursiv ueber virtual_entities bis MAX_TIEFE."""
    f = plan.factor

    def walk(ents, tiefe):
        for e in ents:
            if e.dxftype() != "INSERT":
                continue
            try:
                p = e.ocs().to_wcs(e.dxf.insert)
            except Exception:  # noqa: BLE001
                p = e.dxf.insert
            yield str(e.dxf.name), (float(p[0]) * f, float(p[1]) * f), e
            if tiefe < MAX_TIEFE:
                try:
                    sub = list(e.virtual_entities())
                except Exception:  # noqa: BLE001
                    continue
                yield from walk(sub, tiefe + 1)

    yield from walk(list(plan.space), 0)


def messe_plan(cpath: Path, glob_treffer: dict, glob_rest: Counter) -> dict:
    from ezdxf import bbox

    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
    from notbeleuchtung.raumerkennung.wandkoerper import finde_wandkoerper

    ordner = cpath.parent
    cache = pickle.loads(cpath.read_bytes())
    kzp = ordner / "kennzahlen.json"
    kz = json.loads(kzp.read_text(encoding="utf-8")) if kzp.exists() else {}
    dxf = _dxf(ordner, kz)
    out = {"ordner": str(ordner.relative_to(ERG)), "output_commit": kz.get("commit"),
           "dxf": str(dxf.relative_to(REPO)) if dxf else None}
    if dxf is None:
        out["fehler"] = "DXF nicht gefunden"
        return out
    out["dxf_sha_ok"] = (hashlib.sha256(dxf.read_bytes()).hexdigest() == kz.get("sha256")
                         if kz.get("sha256") else None)

    aussen = [wkb.loads(g) for g in cache.get("aussen_offen", [])]
    au = unary_union(aussen) if aussen else None
    au_m2 = au.area / 1e6 if au is not None else 0.0
    out["aussen_offen_n"] = len(aussen)
    out["aussen_offen_m2"] = round(au_m2, 2)

    # ── Bloecke ────────────────────────────────────────────────────────────
    plan = lade_dxf(dxf)
    out["factor_cache_plan"] = [cache.get("factor"), plan.factor]
    treffer = []                    # (kat, name, xy)
    n_ins = n_stempelblock = n_weit = 0
    weit_bsp = []
    bb = bbox.Cache()
    for name, xy, e in _inserts(plan):
        n_ins += 1
        if STEMPELBLOCK.search(name):
            n_stempelblock += 1
            continue
        kat = "sanitaer" if SANITAER.search(name) else ("moebel" if MOEBEL.search(name) else None)
        if kat is None:
            glob_rest[_norm(name)] += 1
            continue
        treffer.append((kat, name, xy))
        glob_treffer[kat][_norm(name)] += 1
        try:
            ext = bbox.extents([e], cache=bb)
            if ext.has_data:
                c = ext.center
                d = Point(c.x * plan.factor, c.y * plan.factor).distance(Point(xy))
                if d > WEIT_MM:
                    n_weit += 1
                    if len(weit_bsp) < 5:
                        weit_bsp.append({"block": name, "abstand_mm": round(d)})
        except Exception:  # noqa: BLE001
            pass
    out["bloecke"] = {"inserts": n_ins, "zonenstempel_ausgeschlossen": n_stempelblock,
                      "sanitaer": sum(1 for t in treffer if t[0] == "sanitaer"),
                      "moebel": sum(1 for t in treffer if t[0] == "moebel"),
                      "einfuegepunkt_weit_von_bbox": n_weit, "weit_beispiele": weit_bsp}

    # ── Raeume ─────────────────────────────────────────────────────────────
    st_je: dict[str, list[str]] = {}
    for s in cache.get("stempel", []):
        if s.get("raum_id"):
            st_je.setdefault(s["raum_id"], []).append(s.get("name") or "")
    polys = {}
    innen_n = frei_n = 0
    innen_hit, frei_hit, sonst_hit = [], [], []
    for r in cache["raeume"]:
        g = _polygon(r["polygon_mm"])
        if g is None:
            continue
        polys[r["id"]] = g
        typ = r.get("typ") or ""
        gruende = []
        if typ in INNEN_TYPEN or typ in FREI_TYPEN:
            gruende.append("typ")
        st = st_je.get(r["id"], [])
        if st:
            gruende.append("stempel")
        san = sorted({n for k, n, xy in treffer if k == "sanitaer" and g.covers(Point(xy))})
        moe = sorted({n for k, n, xy in treffer if k == "moebel" and g.covers(Point(xy))})
        if san:
            gruende.append("sanitaer")
        if moe:
            gruende.append("moebel")
        innen = bool(gruende)
        frei = typ in FREI_TYPEN
        if innen and not frei:
            innen_n += 1
        if frei:
            frei_n += 1
        schnitt = g.intersection(au).area / 1e6 if au is not None else 0.0
        if schnitt <= SCHNITT_MIN_M2:
            continue
        row = {"id": r["id"], "typ": typ, "stempel": st, "m2": round(r["flaeche_m2"], 2),
               "schnitt_m2": round(schnitt, 2), "schnitt_anteil": round(schnitt / max(g.area / 1e6, 1e-9), 3),
               "gruende": gruende, "sanitaer": san, "moebel": moe}
        if st and any(AUSSEN_STEMPEL.search(n) for n in st):
            row["stempel_aussen_verdacht"] = True
        (frei_hit if frei else innen_hit if innen else sonst_hit).append(row)

    def _flaechen(rows):
        if not rows or au is None:
            return 0.0, 0.0
        summe = sum(x["schnitt_m2"] for x in rows)
        union = unary_union([polys[x["id"]] for x in rows]).intersection(au).area / 1e6
        return round(summe, 2), round(union, 2)

    for key, rows in (("innen", innen_hit), ("frei", frei_hit), ("nicht_innen", sonst_hit)):
        s, u = _flaechen(rows)
        rows.sort(key=lambda x: -x["schnitt_m2"])
        out[key] = {"beruehrt_n": len(rows),
                    "gross_n": sum(1 for x in rows if x["schnitt_m2"] > SCHNITT_GROSS_M2),
                    "schnitt_m2_summe": s, "schnitt_m2_union": u, "raeume": rows}
    out["raeume_n"] = len(polys)
    out["innen_raeume_n_ohne_frei"] = innen_n
    out["frei_raeume_n"] = frei_n
    out["wert"] = len(innen_hit)

    # ── Huellen ────────────────────────────────────────────────────────────
    def _anteil(h):
        a = au.intersection(h).area / 1e6 if au is not None and not h.is_empty else 0.0
        return {"huelle_m2": round(h.area / 1e6, 1), "aussen_in_huelle_m2": round(a, 2),
                "anteil": round(a / au_m2, 3) if au_m2 > 0 else None}

    h1 = _fuellen(_closing(unary_union(list(polys.values())), H1_CLOSE_MM)) if polys else Polygon()
    out["huelle_H1_raeume"] = _anteil(h1)
    wk = finde_wandkoerper(plan)
    if wk:
        wu = unary_union([Polygon(k.polygon_mm).buffer(0) for k in wk]).simplify(20.0)
        h2 = _fuellen(_closing(wu, H2_CLOSE_MM), min_m2=1.0)
        out["huelle_H2_wand"] = {**_anteil(h2), "wandkoerper_n": len(wk),
                                 "wandkoerper_union_m2": round(wu.area / 1e6, 1)}
    else:
        out["huelle_H2_wand"] = {"wandkoerper_n": 0}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).with_name("messung.json")))
    a = ap.parse_args()
    try:
        head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, check=False).stdout.strip()
    except OSError:
        head = None
    glob_treffer = {"sanitaer": Counter(), "moebel": Counter()}
    glob_rest: Counter = Counter()
    plaene = {}
    for cpath in sorted(ERG.rglob("_cache.pkl")):
        rel = cpath.parent.relative_to(ERG)
        key = f"{rel.parent.as_posix()}/{cpath.parent.name.split(' - ')[0]}"
        plaene[key] = messe_plan(cpath, glob_treffer, glob_rest)
        p = plaene[key]
        print(key, "wert", p.get("wert"), "innen_schnitt_union", p.get("innen", {}).get("schnitt_m2_union"),
              "frei", p.get("frei", {}).get("beruehrt_n"), flush=True)

    def sm(k1, k2):
        return round(sum(p.get(k1, {}).get(k2, 0) for p in plaene.values()), 2)

    res = {
        "metrik": "M2-aussen-auf-innenraum", "repo_head": head,
        "konstanten": {"INNEN_TYPEN": sorted(INNEN_TYPEN), "FREI_TYPEN": sorted(FREI_TYPEN),
                       "SCHNITT_MIN_M2": SCHNITT_MIN_M2, "SCHNITT_GROSS_M2": SCHNITT_GROSS_M2,
                       "MAX_TIEFE": MAX_TIEFE, "H1_CLOSE_MM": H1_CLOSE_MM, "H2_CLOSE_MM": H2_CLOSE_MM,
                       "WEIT_MM": WEIT_MM, "STEMPELBLOCK": STEMPELBLOCK.pattern,
                       "SANITAER": SANITAER.pattern, "MOEBEL": MOEBEL.pattern,
                       "AUSSEN_STEMPEL": AUSSEN_STEMPEL.pattern},
        "block_treffer_gesamt": {k: dict(v.most_common()) for k, v in glob_treffer.items()},
        "block_unklassifiziert_top40": dict(glob_rest.most_common(40)),
        "summe": {"plaene": len(plaene),
                  "wert_innen_beruehrt": sum(p.get("wert", 0) for p in plaene.values()),
                  "innen_gross_n": sum(p.get("innen", {}).get("gross_n", 0) for p in plaene.values()),
                  "innen_schnitt_m2_union": sm("innen", "schnitt_m2_union"),
                  "frei_beruehrt_n": sum(p.get("frei", {}).get("beruehrt_n", 0) for p in plaene.values()),
                  "frei_schnitt_m2_union": sm("frei", "schnitt_m2_union"),
                  "nicht_innen_beruehrt_n": sum(p.get("nicht_innen", {}).get("beruehrt_n", 0)
                                                for p in plaene.values()),
                  "aussen_offen_m2": round(sum(p.get("aussen_offen_m2", 0) for p in plaene.values()), 2),
                  "aussen_in_H1_m2": sm("huelle_H1_raeume", "aussen_in_huelle_m2"),
                  "aussen_in_H2_m2": sm("huelle_H2_wand", "aussen_in_huelle_m2")},
        "plaene": plaene,
    }
    Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print("->", a.out)


if __name__ == "__main__":
    main()
```

### A.3 M3-schacht-ohne-stanzung

Aufruf (PowerShell):

```powershell
& "$PY" "./M3-schacht-ohne-stanzung/_messen.py" --out nachher_<commit>.json
```

Vorher-Datei (Output 511ad36): `vorher_511ad36.json (Hauptwert: plaene.*.rot_flaeche_in_raeumen.raeume_n)`

```python
"""M3-schacht-ohne-stanzung — Schacht-Marker (Text) in Raeumen ohne ausgestanzten SCHACHT/LIFT.

Aufruf (Repo-venv, nur lesen):
  PY _messen.py [--out <datei.json>]      Default: messung.json neben dem Skript

Grundmenge: jede Projekte/_ergebnis_raumerkennung/**/_cache.pkl (rglob, nichts hart verdrahtet).
DXF: kennzahlen.json "dxf" (relativ zum Repo), sonst Projekte/<relativer Ergebnisordner>.dxf;
     sha256 gegen kennzahlen.json geprueft (dxf_sha_ok).
Kein Pipeline-Re-Run. In-memory nur dxf_load.lade_dxf (Architektur-Space + mm-Faktor).

Walk: alle Entities von plan.space, rekursiv ueber INSERT.virtual_entities() bis Verschachtelung
MAX_TIEFE (Top-Level = 0). Koordinaten WCS (TEXT/ATTRIB: get_placement -> OCS->WCS; MTEXT: insert)
* plan.factor. Layer "0" im Block erbt den Layer des INSERTs; Farbe: true_color > ACI;
ACI 0 (BYBLOCK) erbt die effektive INSERT-Farbe; ACI 256 (BYLAYER) = Layer-true_color bzw. |Layer-ACI|
des effektiven Layers. ATTDEF zaehlt nicht (ezdxf ueberspringt es), unsichtbare ATTRIBs zaehlen nicht.
DIMENSION wird nicht betreten (Masstexte bleiben draussen).

Schritt 1 Inventar: TEXT/MTEXT/ATTRIB (MTEXT plain_text, Zeilen mit " | " verbunden) gegen TOKENS
  (breit, je Token gezaehlt + Beispiele) + haeufigste normalisierte Texte (Ziffern -> #).
Schritt 2 rote Konturen: LWPOLYLINE/2D-POLYLINE, geschlossen (Flag oder Endpunkte <= SCHLUSS_TOL_MM),
  Pfad geglaettet (ezdxf.path, FLATTEN_MM), Polygon.buffer(0), 0 < Flaeche < ROT_MAX_M2, effektive
  Farbe ROT (ACI 1 oder RGB mit R >= ROT_R_MIN und G, B <= ROT_GB_MAX).
Schritt 3 Metrik: Marker = sichtbarer Text, der MARKER matcht und nicht AUSSCHLUSS.
  Raumpolygon = Polygon(polygon_mm).buffer(0) (wie raumerkennung_darstellung._polygon).
  STANZ = Raeume mit typ in STANZ_TYPEN (SCHACHT, LIFT).
  Kategorie je Marker-Punkt P (exklusiv, in dieser Reihenfolge):
    schacht_nah          min. Abstand P -> STANZ-Polygon <= NAH_MM (0 = enthalten)
    raum_ohne_stanzung   sonst: ein Nicht-STANZ-Raumpolygon covers(P)
    ausserhalb           sonst
  wert je Plan = Anzahl DISTINKTER Raeume mit >= 1 Marker der Kategorie raum_ohne_stanzung.
  Zusatz: schacht_nah_und_raum_deckt = schacht_nah UND ein Nicht-STANZ-Raum covers(P)
          (Schacht-Polygon liegt daneben, Raum wurde am Marker nicht ausgestanzt).
  Rote Konturen: gleiche Kategorien ueber representative_point().
  FP-Kandidaten: SCHACHT-Polygone (typ in FP_TYPEN) ohne Marker-Punkt in <= NAH_MM
    (fp_ohne_text) bzw. zusaetzlich ohne rote Kontur in <= NAH_MM (fp_ohne_text_und_rot).
  Duplikate: gleicher Text <= DEDUP_MM neben gleichem Text zaehlt einmal; AUSSCHLUSS-Treffer zaehlen nicht.
  Sensitivitaet: dieselbe Kategorisierung mit NAH_MM_ALT statt NAH_MM (sensitiv_nah_1000mm).
  Flaechensignal (textunabhaengig): U = Union der roten Konturen; je Nicht-STANZ-Raum Flaeche(Raum ∩ U)
    >= ROT_FLAECHE_MIN_M2 -> rot_flaeche_in_raeumen; wert_bestaetigt_rot = Anzahl wert-Raeume, die auch
    rote Flaeche enthalten; betroffen_ohne_rot_in_raum = wert-Raeume ohne rote Flaeche (Text evtl. im Nachbarraum).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pickle
import re
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path

from ezdxf import colors as ezcolors
from ezdxf import path as ezpath
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

REPO = Path(r"D:\KI Projekt\Notbeleuchtung")
ERG = REPO / "Projekte" / "_ergebnis_raumerkennung"

MAX_TIEFE = 4
NAH_MM = 500.0
ROT_MAX_M2 = 3.0
ROT_R_MIN = 200
ROT_GB_MAX = 60
SCHLUSS_TOL_MM = 5.0
FLATTEN_MM = 5.0
STANZ_TYPEN = frozenset({"SCHACHT", "LIFT"})
FP_TYPEN = frozenset({"SCHACHT"})
BSP_MAX = 6
TOP_TEXTE = 60

# Schritt 1 — breites Inventar (bewusst uebervollstaendig, case-insensitive).
TOKENS = {
    "DDB": r"DDB", "BDB": r"(?<!F)BDB", "FBDB": r"FBDB", "WDB": r"WDB", "FDB": r"FDB", "DBA": r"DBA",
    "DB_wort": r"(?<![A-Z0-9])DB(?![A-Z])",
    "SCHACHT": r"SCHACHT", "SCH_wort": r"(?<![A-Z])SCH(?![A-Z])",
    "INSTALL": r"INSTALL", "STEIG": r"STEIG", "KAMIN": r"KAMIN",
    "LUEFTUNG": r"L\S{0,2}FTUNG", "AB_ZU_FORTLUFT": r"ABLUFT|ZULUFT|FORTLUFT",
    "HKLS": r"HKLS", "STRANG": r"STRANG", "FALLROHR": r"FALLROHR", "DURCHBRUCH": r"DURCHBRUCH",
    "SCHLITZ": r"SCHLITZ", "REVISION": r"REVISION", "VORWAND": r"VORWAND", "ROHR": r"ROHR",
}
TOKEN_RX = {k: re.compile(v, re.IGNORECASE) for k, v in TOKENS.items()}

# Schritt 3 — Marker (abgeleitet aus dem Inventar):
#  Durchbruch-Kuerzel als eigenes Wort (Ziffern direkt dahinter erlaubt: "DDB43/90") oder SCHACHT als
#  eigenes Wort. Komposita ("Schachtverzug ...", Hinweistext) fallen raus.
#  AUSSCHLUSS: Texte mit dem Wort RAUM benennen einen Raum ("DBA Raum", ArchiCAD-Zonenstempel), keinen Schacht.
MARKER = re.compile(r"(?<![A-Z])(?:F?BDB|DDB|WDB|FDB|DBA)(?![A-Z])|(?<![A-ZÄÖÜ])SCHACHT(?![A-ZÄÖÜ])", re.IGNORECASE)
AUSSCHLUSS = re.compile(r"(?<![A-ZÄÖÜ])RAUM(?![A-ZÄÖÜ])", re.IGNORECASE)
DEDUP_MM = 10.0            # gleicher Text <= 10 mm neben gleichem Text = Doppelexport, zaehlt einmal
NAH_MM_ALT = 1000.0        # Sensitivitaet: Textpunkte liegen gemessen meist 0,25-1 m neben der roten Kontur
ROT_FLAECHE_MIN_M2 = 0.02  # Rand-Splitter ignorieren; kleinster Durchbruch im Inventar 20/20 cm = 0,04 m2


def _polygon(pts):
    if len(pts) < 3:
        return None
    g = Polygon(pts).buffer(0)
    return None if g.is_empty else g


def _dxf(ordner: Path, kz: dict) -> Path | None:
    kand = [REPO / kz["dxf"]] if kz.get("dxf") else []
    kand.append(ERG.parent / ordner.relative_to(ERG).parent / f"{ordner.name}.dxf")
    return next((p for p in kand if p.exists()), None)


def _ist_rot(farbe) -> bool:
    k, v = farbe
    if k == "aci":
        return v == 1
    r, g, b = v
    return r >= ROT_R_MIN and g <= ROT_GB_MAX and b <= ROT_GB_MAX


def _farb_key(farbe) -> str:
    k, v = farbe
    return f"aci:{v}" if k == "aci" else "rgb:#{:02X}{:02X}{:02X}".format(*v)


class _Walker:
    def __init__(self, plan):
        self.plan = plan
        self.doc = plan.doc
        self.f = plan.factor
        self._lay: dict[str, tuple] = {}
        self.texte: list[dict] = []
        self.konturen: list[dict] = []
        self.typen: Counter = Counter()
        self.fehler = 0

    def layer_props(self, name: str):
        if name not in self._lay:
            lay = self.doc.layers.get(name)
            if lay is None:
                self._lay[name] = (("aci", 7), True)
            else:
                tc = lay.dxf.get("true_color", None)
                farbe = ("rgb", tuple(ezcolors.int2rgb(tc))) if tc is not None else ("aci", abs(lay.dxf.color))
                self._lay[name] = (farbe, lay.is_on() and not lay.is_frozen())
        return self._lay[name]

    def farbe(self, e, layer: str, erbe):
        tc = e.dxf.get("true_color", None)
        if tc is not None:
            return ("rgb", tuple(ezcolors.int2rgb(tc)))
        aci = e.dxf.get("color", 256)
        if aci == 0:
            return erbe or ("aci", 7)
        if aci == 256:
            return self.layer_props(layer)[0]
        return ("aci", aci)

    def _text(self, e, layer, farbe, pfad, tiefe):
        t = e.dxftype()
        try:
            if t == "MTEXT":
                txt = " | ".join(s.strip() for s in e.plain_text().splitlines() if s.strip())
                p = e.dxf.insert
            else:
                if t == "ATTRIB" and e.is_invisible:
                    return
                txt = str(e.dxf.text or "").strip()
                try:
                    _, p = e.get_placement()
                except Exception:  # noqa: BLE001
                    p = e.dxf.insert
                p = e.ocs().to_wcs(p)
        except Exception:  # noqa: BLE001
            self.fehler += 1
            return
        if not txt:
            return
        self.texte.append({"text": txt, "typ": t, "layer": layer, "farbe": _farb_key(farbe),
                           "sichtbar": self.layer_props(layer)[1], "pfad": "/".join(pfad), "tiefe": tiefe,
                           "xy": (float(p[0]) * self.f, float(p[1]) * self.f)})

    def _kontur(self, e, layer, farbe, pfad):
        t = e.dxftype()
        if t == "POLYLINE" and not e.is_2d_polyline:
            return
        try:
            pts = [(v.x * self.f, v.y * self.f) for v in ezpath.make_path(e).flattening(FLATTEN_MM / self.f)]
        except Exception:  # noqa: BLE001
            self.fehler += 1
            return
        if len(pts) < 3:
            return
        flag = e.closed if t == "LWPOLYLINE" else e.is_closed
        if not (flag or math.dist(pts[0], pts[-1]) <= SCHLUSS_TOL_MM):
            return
        g = _polygon(pts)
        if g is None or not (0 < g.area < ROT_MAX_M2 * 1e6):
            return
        self.konturen.append({"geo": g, "layer": layer, "farbe": farbe, "pfad": "/".join(pfad),
                              "sichtbar": self.layer_props(layer)[1]})

    def run(self):
        def walk(ents, tiefe, pfad, erbe_layer, erbe_farbe):
            for e in ents:
                t = e.dxftype()
                self.typen[t] += 1
                layer = e.dxf.get("layer", "0")
                if layer == "0" and erbe_layer:
                    layer = erbe_layer
                farbe = self.farbe(e, layer, erbe_farbe)
                if t == "INSERT":
                    for a in e.attribs:
                        al = a.dxf.get("layer", "0")
                        al = layer if al == "0" else al
                        self._text(a, al, self.farbe(a, al, farbe), pfad + (str(e.dxf.name),), tiefe + 1)
                    if tiefe < MAX_TIEFE:
                        try:
                            sub = list(e.virtual_entities())
                        except Exception:  # noqa: BLE001
                            self.fehler += 1
                            continue
                        walk(sub, tiefe + 1, pfad + (str(e.dxf.name),), layer, farbe)
                elif t in ("TEXT", "MTEXT", "ATTRIB"):
                    self._text(e, layer, farbe, pfad, tiefe)
                elif t in ("LWPOLYLINE", "POLYLINE"):
                    self._kontur(e, layer, farbe, pfad)

        walk(list(self.plan.space), 0, (), None, None)
        return self


def _bucket(d: float) -> str:
    if d == math.inf:
        return "keine"
    for grenze in (0, 250, 500, 1000, 2000):
        if d <= grenze:
            return f"<={grenze}"
    return ">2000"


def _norm(txt: str) -> str:
    return re.sub(r"\d+", "#", txt)[:50]


def messe_plan(cpath: Path, inv: dict) -> dict:
    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf

    ordner = cpath.parent
    cache = pickle.loads(cpath.read_bytes())
    kzp = ordner / "kennzahlen.json"
    kz = json.loads(kzp.read_text(encoding="utf-8")) if kzp.exists() else {}
    dxf = _dxf(ordner, kz)
    key = f"{ordner.relative_to(ERG).parent.as_posix()}/{ordner.name.split(' - ')[0]}"
    out = {"ordner": str(ordner.relative_to(ERG)), "output_commit": kz.get("commit"),
           "dxf": str(dxf.relative_to(REPO)) if dxf else None}
    if dxf is None:
        out["fehler"] = "DXF nicht gefunden"
        return out
    out["dxf_sha_ok"] = (hashlib.sha256(dxf.read_bytes()).hexdigest() == kz.get("sha256")
                         if kz.get("sha256") else None)
    t0 = time.time()
    plan = lade_dxf(dxf)
    w = _Walker(plan).run()
    out["walk"] = {"s": round(time.time() - t0, 1), "factor": plan.factor, "fehler": w.fehler,
                   "texte_n": len(w.texte), "texte_unsichtbar_n": sum(1 for t in w.texte if not t["sichtbar"]),
                   "geschlossene_konturen_unter_max_n": len(w.konturen)}
    inv["typen"].update(w.typen)

    # ── Schritt 1: Inventar ───────────────────────────────────────────────
    for t in w.texte:
        treffer = [k for k, rx in TOKEN_RX.items() if rx.search(t["text"])]
        for k in treffer:
            z = inv["tokens"][k]
            z["n"] += 1
            z["je_plan"][key] += 1
            z["layer"][t["layer"]] += 1
            z["tiefe"][t["tiefe"]] += 1
            z["texte"][t["text"]] += 1
            if len(z["beispiele"]) < BSP_MAX:
                z["beispiele"].append({"plan": key, "text": t["text"], "layer": t["layer"], "pfad": t["pfad"],
                                       "xy": [round(v) for v in t["xy"]], "sichtbar": t["sichtbar"]})
        inv["normtexte"][_norm(t["text"])] += 1
    for k in w.konturen:
        inv["kontur_farben"][_farb_key(k["farbe"])] += 1
        if _ist_rot(k["farbe"]):
            inv["rot_layer"][k["layer"]] += 1
            inv["rot_pfad_top"][k["pfad"].split("/")[0].rstrip("0123456789") if k["pfad"] else "<space>"] += 1

    # ── Raeume ────────────────────────────────────────────────────────────
    raeume = [(r, g) for r in cache["raeume"] if (g := _polygon(r["polygon_mm"])) is not None]
    stanz = [(r, g) for r, g in raeume if (r.get("typ") or "") in STANZ_TYPEN]
    andere = [(r, g) for r, g in raeume if (r.get("typ") or "") not in STANZ_TYPEN]

    def einordnen(p: Point):
        d, sid = math.inf, None
        for r, g in stanz:
            dd = g.distance(p)
            if dd < d:
                d, sid = dd, r["id"]
        cov = [r for r, g in andere if g.covers(p)]
        kat = "schacht_nah" if d <= NAH_MM else ("raum_ohne_stanzung" if cov else "ausserhalb")
        return kat, cov, d, sid

    rot = [k for k in w.konturen if k["sichtbar"] and _ist_rot(k["farbe"])]

    def naechste_rote(p: Point):
        best_d, best_k = math.inf, None
        for k in rot:
            dd = k["geo"].distance(p)
            if dd < best_d:
                best_d, best_k = dd, k
        return best_d, best_k

    # ── Schritt 3: Marker ─────────────────────────────────────────────────
    kand = [t for t in w.texte if MARKER.search(t["text"])]
    out["marker_kandidaten_roh"] = len(kand)
    out["marker_unsichtbar_ausgeschlossen"] = sum(1 for t in kand if not t["sichtbar"])
    out["marker_ausschluss_regex"] = [t["text"] for t in kand if t["sichtbar"] and AUSSCHLUSS.search(t["text"])]
    marker: list[dict] = []
    dubl = 0
    for t in kand:
        if not t["sichtbar"] or AUSSCHLUSS.search(t["text"]):
            continue
        if any(m["text"] == t["text"] and math.dist(m["xy"], t["xy"]) <= DEDUP_MM for m in marker):
            dubl += 1
            continue
        marker.append(t)
    out["marker_duplikate_entfernt"] = dubl

    kat_n, rot_abst = Counter(), Counter()
    betroffen: dict[str, dict] = {}
    betroffen_alt: dict[str, dict] = {}
    marker_rows = []
    nah_und_deckt = 0
    n_alt = 0
    ausserhalb_abst: list[int] = []
    alle_raeume = unary_union([g for _, g in raeume]) if raeume else None

    def buche(ziel, cov, text):
        for r in cov:
            b = ziel.setdefault(r["id"], {"id": r["id"], "typ": r.get("typ") or "",
                                          "m2": round(r["flaeche_m2"], 2), "texte": []})
            b["texte"].append(text)

    for t in marker:
        p = Point(t["xy"])
        kat, cov, d, sid = einordnen(p)
        kat_n[kat] += 1
        if kat == "schacht_nah" and cov:
            nah_und_deckt += 1
        d_rot, k_rot = naechste_rote(p)
        rot_abst[_bucket(d_rot)] += 1
        abst_raeume = None
        if kat == "ausserhalb" and alle_raeume is not None:
            abst_raeume = round(alle_raeume.distance(p))
            ausserhalb_abst.append(abst_raeume)
        marker_rows.append({"text": t["text"], "xy": [round(v) for v in t["xy"]], "layer": t["layer"],
                            "pfad": t["pfad"], "kat": kat, "in_raeume": [r["id"] for r in cov],
                            "naechster_stanz": sid, "abstand_stanz_mm": None if sid is None else round(d),
                            "abstand_rot_mm": None if k_rot is None else round(d_rot),
                            "rot_layer": None if k_rot is None else k_rot["layer"],
                            "abstand_zu_raeumen_mm": abst_raeume})
        if kat == "raum_ohne_stanzung":
            buche(betroffen, cov, t["text"])
        if cov and d > NAH_MM_ALT:
            n_alt += 1
            buche(betroffen_alt, cov, t["text"])
    out["marker"] = {"gesamt": len(marker), "raum_ohne_stanzung": kat_n["raum_ohne_stanzung"],
                     "schacht_nah": kat_n["schacht_nah"], "schacht_nah_und_raum_deckt": nah_und_deckt,
                     "ausserhalb": kat_n["ausserhalb"], "abstand_text_zu_roter_kontur": dict(rot_abst),
                     "ausserhalb_max_abstand_zu_raeumen_mm": max(ausserhalb_abst, default=None),
                     "liste": marker_rows}
    out["betroffene_raeume"] = sorted(betroffen.values(), key=lambda b: b["id"])
    out["wert"] = len(betroffen)
    out["sensitiv_nah_1000mm"] = {"marker_raum_ohne_stanzung": n_alt, "wert": len(betroffen_alt),
                                  "raeume": sorted(betroffen_alt)}

    # ── Schritt 2: rote Konturen ─────────────────────────────────────────
    rk = Counter()
    rot_raeume = Counter()
    for k in rot:
        kat, cov, _d, _s = einordnen(k["geo"].representative_point())
        k["kat"] = kat
        rk[kat] += 1
        if kat == "raum_ohne_stanzung":
            for r in cov:
                rot_raeume[r["id"]] += 1
    out["rote_konturen"] = {"gesamt": len(rot), "m2_summe": round(sum(k["geo"].area for k in rot) / 1e6, 3),
                            "raum_ohne_stanzung": rk["raum_ohne_stanzung"], "schacht_nah": rk["schacht_nah"],
                            "ausserhalb": rk["ausserhalb"], "je_layer": dict(Counter(k["layer"] for k in rot)),
                            "raeume_ohne_stanzung": dict(rot_raeume)}
    rot_u = unary_union([k["geo"] for k in rot]) if rot else None
    flaeche = []
    rot_in_raeumen = 0.0
    if rot_u is not None and andere:
        for r, g in andere:
            a = g.intersection(rot_u).area / 1e6
            if a >= ROT_FLAECHE_MIN_M2:
                flaeche.append({"id": r["id"], "typ": r.get("typ") or "", "m2": round(r["flaeche_m2"], 2),
                                "rot_m2": round(a, 3)})
        rot_in_raeumen = unary_union([g for _, g in andere]).intersection(rot_u).area / 1e6
    out["rot_flaeche_in_raeumen"] = {"union_rot_m2": round(rot_u.area / 1e6, 3) if rot_u is not None else 0.0,
                                     "in_raeumen_m2": round(rot_in_raeumen, 3), "raeume_n": len(flaeche),
                                     "raeume": flaeche}
    ids_rot = {x["id"] for x in flaeche}
    out["wert_bestaetigt_rot"] = len(ids_rot & set(betroffen))
    out["betroffen_ohne_rot_in_raum"] = sorted(set(betroffen) - ids_rot)

    # ── FP-Kandidaten ─────────────────────────────────────────────────────
    fp = []
    for r, g in raeume:
        if (r.get("typ") or "") not in FP_TYPEN:
            continue
        txt_nah = [{"text": t["text"], "abstand_mm": round(g.distance(Point(t["xy"])))}
                   for t in marker if g.distance(Point(t["xy"])) <= NAH_MM]
        rot_nah = [{"layer": k["layer"], "m2": round(k["geo"].area / 1e6, 3), "abstand_mm": round(g.distance(k["geo"]))}
                   for k in rot if g.distance(k["geo"]) <= NAH_MM]
        d_txt = min((g.distance(Point(t["xy"])) for t in marker), default=math.inf)
        fp.append({"id": r["id"], "typ": r["typ"], "m2": round(r["flaeche_m2"], 2), "n_ecken": len(r["polygon_mm"]),
                   "naechster_marker_mm": None if d_txt == math.inf else round(d_txt),
                   "marker_text_nah": txt_nah, "rote_kontur_nah": rot_nah,
                   "fp_ohne_text": not txt_nah, "fp_ohne_text_und_rot": not txt_nah and not rot_nah})
    out["schacht_polygone"] = fp
    out["fp_ohne_text_n"] = sum(1 for x in fp if x["fp_ohne_text"])
    out["fp_ohne_text_und_rot_n"] = sum(1 for x in fp if x["fp_ohne_text_und_rot"])
    out["raeume_n"] = len(raeume)
    out["stanz_polygone_n"] = len(stanz)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).with_name("messung.json")))
    a = ap.parse_args()
    try:
        head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, check=False).stdout.strip()
    except OSError:
        head = None
    inv = {"tokens": defaultdict(lambda: {"n": 0, "je_plan": Counter(), "layer": Counter(), "tiefe": Counter(),
                                          "texte": Counter(), "beispiele": []}),
           "normtexte": Counter(), "typen": Counter(), "kontur_farben": Counter(), "rot_layer": Counter(),
           "rot_pfad_top": Counter()}
    for k in TOKENS:            # Null-Treffer sichtbar machen
        inv["tokens"][k]
    plaene = {}
    for cpath in sorted(ERG.rglob("_cache.pkl")):
        rel = cpath.parent.relative_to(ERG)
        key = f"{rel.parent.as_posix()}/{cpath.parent.name.split(' - ')[0]}"
        p = plaene[key] = messe_plan(cpath, inv)
        print(key, "wert", p.get("wert"), "alt1000", p.get("sensitiv_nah_1000mm"),
              "bestaetigt_rot", p.get("wert_bestaetigt_rot"), "dubl", p.get("marker_duplikate_entfernt"),
              "ausschl", p.get("marker_ausschluss_regex"),
              "marker", {k: v for k, v in p.get("marker", {}).items() if k != "liste"},
              "rot", p.get("rote_konturen", {}).get("gesamt"), "fp", p.get("fp_ohne_text_n"),
              p.get("fp_ohne_text_und_rot_n"), "walk", p.get("walk"), flush=True)

    tokens = {k: {"n": z["n"], "je_plan": dict(z["je_plan"]), "layer": dict(z["layer"].most_common(8)),
                  "tiefe": dict(z["tiefe"]), "texte_top": dict(z["texte"].most_common(15)),
                  "beispiele": z["beispiele"]}
              for k, z in sorted(inv["tokens"].items(), key=lambda kv: -kv[1]["n"])}
    res = {
        "metrik": "M3-schacht-ohne-stanzung", "repo_head": head,
        "konstanten": {"MAX_TIEFE": MAX_TIEFE, "NAH_MM": NAH_MM, "ROT_MAX_M2": ROT_MAX_M2, "ROT_R_MIN": ROT_R_MIN,
                       "ROT_GB_MAX": ROT_GB_MAX, "SCHLUSS_TOL_MM": SCHLUSS_TOL_MM, "FLATTEN_MM": FLATTEN_MM,
                       "STANZ_TYPEN": sorted(STANZ_TYPEN), "FP_TYPEN": sorted(FP_TYPEN),
                       "MARKER": MARKER.pattern, "AUSSCHLUSS": AUSSCHLUSS.pattern, "DEDUP_MM": DEDUP_MM,
                       "NAH_MM_ALT": NAH_MM_ALT, "ROT_FLAECHE_MIN_M2": ROT_FLAECHE_MIN_M2, "TOKENS": TOKENS},
        "inventar": {"tokens": tokens, "texte_normalisiert_top": dict(inv["normtexte"].most_common(TOP_TEXTE)),
                     "entity_typen": dict(inv["typen"].most_common()),
                     "farben_geschlossene_konturen_unter_max": dict(inv["kontur_farben"].most_common(25)),
                     "rot_layer": dict(inv["rot_layer"].most_common()),
                     "rot_pfad_top": dict(inv["rot_pfad_top"].most_common())},
        "summe": {"plaene": len(plaene),
                  "wert_raeume_ohne_stanzung": sum(p.get("wert", 0) for p in plaene.values()),
                  "wert_sensitiv_nah_1000mm": sum(p.get("sensitiv_nah_1000mm", {}).get("wert", 0)
                                                  for p in plaene.values()),
                  "marker_raum_ohne_stanzung_sensitiv_1000mm": sum(
                      p.get("sensitiv_nah_1000mm", {}).get("marker_raum_ohne_stanzung", 0) for p in plaene.values()),
                  "wert_bestaetigt_rot": sum(p.get("wert_bestaetigt_rot", 0) for p in plaene.values()),
                  "rot_flaeche_raeume_n": sum(p.get("rot_flaeche_in_raeumen", {}).get("raeume_n", 0)
                                              for p in plaene.values()),
                  "rot_in_raeumen_m2": round(sum(p.get("rot_flaeche_in_raeumen", {}).get("in_raeumen_m2", 0)
                                                 for p in plaene.values()), 3),
                  "marker_duplikate_entfernt": sum(p.get("marker_duplikate_entfernt", 0) for p in plaene.values()),
                  "marker_ausschluss_regex": sum(len(p.get("marker_ausschluss_regex", [])) for p in plaene.values()),
                  "marker_abstand_text_zu_roter_kontur": dict(sum(
                      (Counter(p.get("marker", {}).get("abstand_text_zu_roter_kontur", {})) for p in plaene.values()),
                      Counter())),
                  "marker_ausserhalb_max_abstand_zu_raeumen_mm": max(
                      (p.get("marker", {}).get("ausserhalb_max_abstand_zu_raeumen_mm") or 0 for p in plaene.values()),
                      default=0),
                  **{f"marker_{k}": sum(p.get("marker", {}).get(k, 0) for p in plaene.values())
                     for k in ("gesamt", "raum_ohne_stanzung", "schacht_nah", "schacht_nah_und_raum_deckt",
                               "ausserhalb")},
                  **{f"rot_{k}": sum(p.get("rote_konturen", {}).get(k, 0) for p in plaene.values())
                     for k in ("gesamt", "raum_ohne_stanzung", "schacht_nah", "ausserhalb")},
                  "schacht_polygone": sum(len(p.get("schacht_polygone", [])) for p in plaene.values()),
                  "fp_ohne_text": sum(p.get("fp_ohne_text_n", 0) for p in plaene.values()),
                  "fp_ohne_text_und_rot": sum(p.get("fp_ohne_text_und_rot_n", 0) for p in plaene.values())},
        "plaene": plaene,
    }
    Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("->", a.out)


if __name__ == "__main__":
    main()
```

### A.4 M4-wohnungen

Aufruf (PowerShell):

```powershell
& "$PY" "./M4-wohnungen/_messen.py" nachher_<commit>.json
```

Vorher-Datei (Output 511ad36): `ergebnis.json`

```python
"""M4-wohnungen — Vorher/Nachher-Messung der Wohnungsbildung (S-H4).

Liest NUR die Output-Caches (_cache.pkl) unter Projekte/_ergebnis_raumerkennung,
keine Pipeline, kein DXF. Aufruf:
    python _messen.py [ausgabe.json]      (Default: ergebnis.json neben dem Skript)

Definitionen (fix, fuer Vorher und Nachher identisch):
  Wohnung          = jede verschiedene, nicht-leere raeume[].wohnung_id eines Plans.
  Einraum-Wohnung  = Wohnung mit genau 1 Raum in den Daten.
  Datenbefund      = Wohnung enthaelt einen Raum mit typ in ERSCHL_TYPEN oder
                     nutzungsklasse beginnend mit "ALLGEMEIN_".
  Darstellungsbefund = Nachbau von scripts/analyse/raumerkennung_darstellung.py
                     _zeichne_ausschnitt Z.709-731 (Umriss) + _polygon Z.218-222:
                     u = unary_union(Raumpolygone der Wohnung).buffer(200).buffer(-200)
                     (leer -> unary_union ohne Puffer); gezeichnet werden NUR die
                     Aussenringe -> "gezeichnete Flaeche" = Union der Polygon(exterior).
                     Befund, wenn ein Raum mit typ in ERSCHL_TYPEN davon > MIN_M2 m2
                     ueberdeckt wird (unabhaengig davon, ob er in den Daten dazugehoert).
  Privatraum ohne Wohnung = wohnung_id leer UND (typ.upper() in PRIVAT_TYPEN ODER
                     (typ leer = UNBEKANNT UND ein zugeordneter Stempel (stempel.raum_id)
                     matcht WOHN_STEMPEL_RX)).
"""
import json
import pickle
import re
import sys
from pathlib import Path

from shapely.geometry import Polygon
from shapely.ops import unary_union

REPO = Path(r"D:/KI Projekt/Notbeleuchtung")
AUSGABE = REPO / "Projekte" / "_ergebnis_raumerkennung"
MIN_M2 = 0.5
PUFFER_MM = 200.0                      # = raumerkennung_darstellung.py Z.715
ERSCHL_TYPEN = {"STIEGENHAUS", "TREPPENHAUS", "LIFT", "AUFZUG"}
PRIVAT_TYPEN = {"ZIMMER", "WOHNZIMMER", "BAD", "WC", "KUECHE", "KÜCHE", "ABSTELLRAUM", "VORRAUM"}
WOHN_STEMPEL_RX = re.compile(r"wohn|tv[\s._-]*raum|k(?:ü|ue)?che", re.IGNORECASE)


def _polygon(pts):                     # = raumerkennung_darstellung._polygon Z.218-222
    if len(pts) < 3:
        return None
    g = Polygon(pts).buffer(0)
    return None if g.is_empty else g


def _umriss(ps):                       # = _zeichne_ausschnitt Z.715-722
    u = unary_union(ps).buffer(PUFFER_MM).buffer(-PUFFER_MM)
    if u.is_empty:
        u = unary_union(ps)
    teile = list(getattr(u, "geoms", [u]))
    gezeichnet = unary_union([Polygon(g.exterior) for g in teile])
    return u, gezeichnet, teile


def _r(r):
    return {"id": r["id"], "typ": r["typ"] or "UNBEKANNT", "m2": round(r["flaeche_m2"], 2),
            "nutzungsklasse": r["nutzungsklasse"], "wohnung_id": r["wohnung_id"]}


def messe_plan(cache_pfad: Path) -> dict:
    c = pickle.loads(cache_pfad.read_bytes())
    kz_pfad = cache_pfad.parent / "kennzahlen.json"
    kz = json.loads(kz_pfad.read_text(encoding="utf-8")) if kz_pfad.exists() else {}
    raeume = c["raeume"]
    polys = {r["id"]: g for r in raeume if (g := _polygon(r["polygon_mm"])) is not None}
    stempel_je_raum = {}
    for s in c["stempel"]:
        if s.get("raum_id"):
            stempel_je_raum.setdefault(s["raum_id"], []).append(s["name"])

    # Einheitscheck: Polygonflaeche (mm2/1e6) gegen flaeche_m2
    abw = [abs(polys[r["id"]].area / 1e6 - r["flaeche_m2"]) / r["flaeche_m2"]
           for r in raeume if r["id"] in polys and r["flaeche_m2"] > 0]

    whg = {}
    for r in raeume:
        if r["wohnung_id"]:
            whg.setdefault(r["wohnung_id"], []).append(r)

    einraum = [{"wohnung": w, **_r(rs[0])} for w, rs in sorted(whg.items()) if len(rs) == 1]

    daten = []
    for w, rs in sorted(whg.items()):
        treffer = [_r(r) for r in rs
                   if (r["typ"] or "").upper() in ERSCHL_TYPEN
                   or (r["nutzungsklasse"] or "").startswith("ALLGEMEIN_")]
        if treffer:
            daten.append({"wohnung": w, "raeume": treffer})

    darstellung, fremde, umrisse = [], [], []
    for w, rs in sorted(whg.items()):
        ps = [polys[r["id"]] for r in rs if r["id"] in polys]
        if not ps:
            continue
        ids = {r["id"] for r in rs}
        u, gez, teile = _umriss(ps)
        umrisse.append({"wohnung": w, "raeume_daten": len(rs),
                        "raeume_m2_daten": round(sum(r["flaeche_m2"] for r in rs), 2),
                        "umriss_teile": len(teile),
                        "loecher_nicht_gezeichnet": sum(len(t.interiors) for t in teile),
                        "gezeichnete_flaeche_m2": round(gez.area / 1e6, 2)})
        for r in raeume:
            p = polys.get(r["id"])
            if p is None:
                continue
            a = gez.intersection(p).area / 1e6
            if a <= MIN_M2:
                continue
            eintrag = {"wohnung": w, **_r(r), "ueberdeckt_m2": round(a, 2),
                       "ueberdeckt_m2_mit_loechern": round(u.intersection(p).area / 1e6, 2),
                       "in_daten": r["id"] in ids}
            if (r["typ"] or "").upper() in ERSCHL_TYPEN:
                darstellung.append(eintrag)
            if r["id"] not in ids:
                fremde.append(eintrag)

    privat, unbek_kontext = [], []
    for r in raeume:
        if r["wohnung_id"]:
            continue
        typ = (r["typ"] or "").upper()
        namen = stempel_je_raum.get(r["id"], [])
        if typ in PRIVAT_TYPEN:
            privat.append({**_r(r), "grund": "typ", "stempel": namen})
        elif not typ:
            wohn = [n for n in namen if WOHN_STEMPEL_RX.search(n)]
            e = {**_r(r), "stempel": namen, "stempel_ascii": [ascii(n) for n in namen]}
            if wohn:
                privat.append({**e, "grund": "UNBEKANNT+Wohn-Stempel"})
            else:
                unbek_kontext.append(e)

    return {
        "projekt": cache_pfad.parent.parent.name,
        "plan_ordner": cache_pfad.parent.name,
        "plan": cache_pfad.parent.name.split(" - ")[0],
        "commit_output": kz.get("commit"),
        "kennzahlen_wohnungen": kz.get("wohnungen"),
        "raeume_gesamt": len(raeume),
        "einheit_max_rel_abw_polygon_vs_m2": round(max(abw), 4) if abw else None,
        "wohnungen": len(whg),
        "raeume_je_wohnung": {w: len(rs) for w, rs in sorted(whg.items())},
        "einraum_wohnungen": einraum,
        "daten_erschliessung_in_wohnung": daten,
        "darstellung_erschliessung_im_umriss": darstellung,
        "kontext_fremde_raeume_im_umriss": fremde,
        "kontext_umrisse": umrisse,
        "privat_ohne_wohnung": privat,
        "kontext_unbekannt_ohne_wohnung_ohne_wohnstempel": unbek_kontext,
        "zahlen": {
            "wohnungen": len(whg),
            "einraum": len(einraum),
            "wohnungen_daten_erschliessung": len(daten),
            "wohnungen_darstellung_erschliessung": len({d["wohnung"] for d in darstellung}),
            "wohnungen_auffaellig": len({e["wohnung"] for e in einraum + daten + darstellung}),
            "privat_ohne_wohnung": len(privat),
            "privat_ohne_wohnung_nicht_allgemein": sum(
                1 for p in privat if not (p["nutzungsklasse"] or "").startswith("ALLGEMEIN_")),
        },
    }


def main() -> int:
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("ergebnis.json")
    plaene = [messe_plan(p) for p in sorted(AUSGABE.rglob("_cache.pkl"))]
    summe = {k: sum(p["zahlen"][k] for p in plaene) for k in plaene[0]["zahlen"]} if plaene else {}
    summe["plaene"] = len(plaene)
    summe["plaene_mit_befund"] = sum(
        1 for p in plaene if p["zahlen"]["einraum"] or p["zahlen"]["wohnungen_daten_erschliessung"]
        or p["zahlen"]["wohnungen_darstellung_erschliessung"])
    ergebnis = {"metrik": "M4-wohnungen", "min_m2": MIN_M2, "puffer_mm": PUFFER_MM,
                "erschl_typen": sorted(ERSCHL_TYPEN), "privat_typen": sorted(PRIVAT_TYPEN),
                "wohn_stempel_rx": WOHN_STEMPEL_RX.pattern, "summe": summe, "plaene": plaene}
    ziel.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=1), encoding="utf-8")
    for p in plaene:
        print(p["plan"], p["commit_output"], json.dumps(p["zahlen"]))
    print("SUMME", json.dumps(summe))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

### A.5 Loch-Test S1, Veto S2, Öffnungsfilter (`NB1-nachbesserung/_s12_nachrechnung.py`; B.1, B.2, B.6)

Aufruf: `& $PY _s12_nachrechnung.py UG EG OG1 OG2 OG3 DG1 DG2` im Arbeitsordner; importiert `_messen.py` aus A.2 (Pfad `../messung/M2-aussen-auf-innenraum`). Der Loch-Test (`teile_status`) liest keinen Cache.

```python
"""Nachbesserung R1 - S1/S2-Wirkung, Oeffnungsfilter, F7-Basis je Rennweg-Plan (nur lesen, in-memory).

Aufruf: PY _s12_nachrechnung.py UG EG OG1 OG2 OG3 DG1 DG2   -> s12_<PLAN>.json neben dem Skript + stdout
In-memory nur Einzelfunktionen: dxf_load.lade_dxf, wandkoerper.finde_wandkoerper / bounds_aus_wandkoerpern,
aussenbereich._wand_geschlossen / _komponenten_aus / grundstuecksgrenze / aussen_indizien / _strassenkante,
aussenbereich.erkenne_aussenbereiche (nur Abgleich), tueren.tuer_oeffnungen / im_planbereich.
Raeume, Stempel, aussen_offen aus Projekte/_ergebnis_raumerkennung/Rennweg/<PLAN>/_cache.pkl (Output 511ad36).
Innen-Kriterium und Zaehlregel wie M2 (_messen.py wird importiert, nicht kopiert).
"""
from __future__ import annotations

import gc
import json
import pickle
import sys
from collections import Counter
from pathlib import Path

from shapely import wkb
from shapely.geometry import Point
from shapely.ops import unary_union

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent / "messung" / "M2-aussen-auf-innenraum"))
import _messen as M2  # noqa: E402

from notbeleuchtung.raumerkennung import aussenbereich as ab  # noqa: E402
from notbeleuchtung.raumerkennung.dxf_load import lade_dxf  # noqa: E402
from notbeleuchtung.raumerkennung.tueren import im_planbereich, tuer_oeffnungen  # noqa: E402
from notbeleuchtung.raumerkennung.wandkoerper import bounds_aus_wandkoerpern, finde_wandkoerper  # noqa: E402

REPO = Path(r"D:\KI Projekt\Notbeleuchtung")
NAME = "{} - Rennweg 15_1030 Wien_Ausfürung-2026-06-12"
MASKE_MM = 5000.0      # Gebaeudemaske fuer den Zuschnitt (wie K4-Gegenprobe _k4g_mess.py); Knopf


def _teile(g):
    if g is None or g.is_empty:
        return []
    return [x for x in getattr(g, "geoms", [g]) if x.geom_type == "Polygon" and not x.is_empty]


def _union(gs):
    gs = [g for g in gs if g is not None and not g.is_empty]
    return unary_union(gs) if gs else None


def _m2(g):
    return round(g.area / 1e6, 2) if g is not None and not g.is_empty else 0.0


def teile_status(plan, koerper):
    """Kopie erkenne_aussenbereiche Z.234-271; je freiem Teil alle Praedikate getrennt."""
    wand_zu = ab._wand_geschlossen(koerper, ab._SCHLIESS_MM)
    komp = ab._komponenten_aus(wand_zu)
    grund = ab.grundstuecksgrenze(plan, wand_zu)
    bezug = grund if grund is not None else unary_union(komp).convex_hull
    frei = bezug.difference(wand_zu)
    indizien = ab.aussen_indizien(plan)
    rand = bezug.exterior
    kante = ab._strassenkante(plan, rand)
    if kante is None:
        kante = rand
    komp_u = unary_union(komp)
    komp_b = komp_u.buffer(1.0)
    rows = []
    for t in _teile(frei):
        if t.area < ab._MIN_HOF_M2 * 1e6:
            continue
        hals = t.buffer(-ab._HALS_MM).buffer(ab._HALS_MM + 20.0)
        rows.append({
            "t": t,
            "indiz": any(t.covers(Point(p)) for p in indizien),
            "rand": t.distance(rand) < ab._RAND_EPS_MM,
            "loch_within": t.within(komp_b),
            "loch_diff": t.difference(komp_u).area <= 1e6,
            "weg": (not hals.is_empty and not kante.is_empty
                    and hals.distance(kante) < ab._RAND_EPS_MM),
            "d_rand_mm": round(t.distance(rand)),
        })
    return rows, grund is not None, len(indizien)


def offen_ist(r):
    return (r["indiz"] or r["rand"]) and r["weg"]


def offen_s1_within(r):      # Entwurf-Pseudocode U7: Loch nur mit Indiz
    return (r["indiz"] or ((not r["loch_within"]) and r["rand"])) and r["weg"]


def offen_s1_diff(r):        # K4-Gegenprobe _aussen_folgen._klassifiziere(loch_test=True)
    return (r["indiz"] or (not r["loch_diff"])) and r["weg"]


def m2_zaehlung(raeume, st_je, treffer, offen_u, maske):
    innen, frei = [], []
    for r in raeume:
        g = M2._polygon(r["polygon_mm"])
        if g is None or offen_u is None:
            continue
        typ = r.get("typ") or ""
        ist_innen = (typ in M2.INNEN_TYPEN or typ in M2.FREI_TYPEN or bool(st_je.get(r["id"]))
                     or any(g.covers(Point(xy)) for _k, _n, xy in treffer))
        if not ist_innen:
            continue
        s = g.intersection(offen_u)
        if s.area / 1e6 <= M2.SCHNITT_MIN_M2:
            continue
        aus = s.difference(maske).area / 1e6 if maske is not None else None
        row = [r["id"], typ, round(s.area / 1e6, 2), None if aus is None else round(aus, 2)]
        (frei if typ in M2.FREI_TYPEN else innen).append(row)
    innen.sort(key=lambda x: -x[2])
    frei.sort(key=lambda x: -x[2])
    return {"wert": len(innen), "innen_[id,typ,schnitt_m2,davon_ausserhalb_maske_m2]": innen,
            "frei": frei}


def plan_mess(pid: str) -> dict:
    n = NAME.format(pid)
    cache = pickle.loads((REPO / "Projekte" / "_ergebnis_raumerkennung" / "Rennweg" / n
                          / "_cache.pkl").read_bytes())
    plan = lade_dxf(str(REPO / "Projekte" / "Rennweg" / f"{n}.dxf"))
    koerper = finde_wandkoerper(plan)
    res: dict = {"plan": pid, "n_koerper": len(koerper), "maske_mm": MASKE_MM}

    # Oeffnungsfilter wie kaskade.py:110-115
    oeff = tuer_oeffnungen(plan)
    nach = im_planbereich(oeff, bounds_aus_wandkoerpern(koerper)) if koerper else oeff
    res["oeffnungen"] = {"vor_n": len(oeff), "vor_quellen": dict(Counter(o.quelle for o in oeff)),
                         "nach_n": len(nach), "nach_quellen": dict(Counter(o.quelle for o in nach))}

    rows, grenze, n_ind = teile_status(plan, koerper)
    res["grundstuecksgrenze"] = grenze
    res["n_indizien"] = n_ind
    real = ab.erkenne_aussenbereiche(plan, koerper)
    cache_offen = _union([wkb.loads(g) for g in cache.get("aussen_offen", [])])
    ist = _union([r["t"] for r in rows if offen_ist(r)])
    res["abgleich_ist"] = {
        "offen_real_m2": _m2(_union(real.offen)), "offen_kopie_m2": _m2(ist),
        "offen_cache_m2": _m2(cache_offen),
        "symdiff_kopie_cache_m2": _m2(ist.symmetric_difference(cache_offen))
        if ist is not None and cache_offen is not None else None}

    s1w = _union([r["t"] for r in rows if offen_s1_within(r)])
    s1d = _union([r["t"] for r in rows if offen_s1_diff(r)])
    maske = _union(ab._komponenten_aus(ab._wand_geschlossen(koerper, MASKE_MM)))
    zonen = _union([M2._polygon(r["polygon_mm"]) for r in cache["raeume"]
                    if (r.get("typ") or "") in M2.INNEN_TYPEN])
    zonen_clip = zonen.intersection(maske) if zonen is not None and maske is not None else None

    def minus(a, b):
        return a if a is None or b is None else a.difference(b)

    varianten = {"IST": ist, "S1_within": s1w, "S1_diff": s1d,
                 "S1_S2_zuschnitt": minus(s1w, zonen_clip), "S1_S2_ohne_zuschnitt": minus(s1w, zonen)}

    st_je: dict[str, list[str]] = {}
    for s in cache.get("stempel", []):
        if s.get("raum_id"):
            st_je.setdefault(s["raum_id"], []).append(s.get("name") or "")
    treffer = []
    for name, xy, _e in M2._inserts(plan):
        if M2.STEMPELBLOCK.search(name):
            continue
        kat = "sanitaer" if M2.SANITAER.search(name) else ("moebel" if M2.MOEBEL.search(name) else None)
        if kat:
            treffer.append((kat, name, xy))
    res["varianten"] = {k: {"offen_m2": _m2(v), **m2_zaehlung(cache["raeume"], st_je, treffer, v, maske)}
                        for k, v in varianten.items()}
    res["f7_teile_offen_ist_nicht_offen_s1"] = [
        {"m2": _m2(r["t"]), "indiz": r["indiz"], "d_rand_mm": r["d_rand_mm"],
         "loch_within": r["loch_within"], "loch_diff": r["loch_diff"]}
        for r in rows if offen_ist(r) and not offen_s1_within(r)]
    res["teile_n"] = len(rows)
    del plan, koerper, real
    gc.collect()
    return res


def main() -> None:
    for pid in sys.argv[1:]:
        res = plan_mess(pid)
        (HIER / f"s12_{pid}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                              encoding="utf-8")
        kurz = {k: (v["offen_m2"], v["wert"]) for k, v in res["varianten"].items()}
        print(pid, "oeffnungen", res["oeffnungen"]["vor_n"], "->", res["oeffnungen"]["nach_n"],
              "abgleich", res["abgleich_ist"], "varianten(offen_m2,wert)", kurz,
              "f7", res["f7_teile_offen_ist_nicht_offen_s1"], flush=True)


if __name__ == "__main__":
    main()
```

### A.6 R-Typisierung der Liftringe, Schacht-Text, Stair-Hüllen (`NB1-nachbesserung/_ringe_typ.py`; B.3, B.9)

Aufruf: `& $PY _ringe_typ.py UG EG OG1 DG1 DG2` im Arbeitsordner.

```python
"""Nachbesserung R1 - R-Typisierung der Liftringe mit/ohne Treppenmarker und Schacht-Text-Evidenz;
DG2 zusaetzlich objekt_stiege.finde_stiegen gegen die Stair-Huellen (nur lesen, in-memory).

Aufruf: PY _ringe_typ.py UG EG OG1 DG1 DG2   -> stdout
In-memory nur: dxf_load.lade_dxf, kaskade.raeume_aus_kaskade, rest_komponenten._marker_punkte/_typisiere,
stiegenhaus._wcs_pts, objekt_stiege.finde_stiegen (nur DG2).
"""
from __future__ import annotations

import gc
import json
import re
import sys
from pathlib import Path

from shapely.geometry import MultiPoint, Point, Polygon
from shapely.ops import unary_union

from notbeleuchtung.raumerkennung import rest_komponenten as RK
from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.geometrie_typ import _STAIR_BLOCK
from notbeleuchtung.raumerkennung.kaskade import raeume_aus_kaskade
from notbeleuchtung.raumerkennung.stiegenhaus import _wcs_pts

REPO = Path(r"D:\KI Projekt\Notbeleuchtung")
NAME = "{} - Rennweg 15_1030 Wien_Ausfürung-2026-06-12"
# Schacht-Evidenz laut Entwurf U2: Wortgrenze, nie DBA allein, nie Raum-/Treppen-/Lifttexte
SCHACHT_RX = re.compile(r"(?<![A-ZÄÖÜ])SCHACHT(?![A-ZÄÖÜ])|(?<![A-Z])(?:F?BDB|DDB)(?![A-Z])")
AUSSCHLUSS_RX = re.compile(r"(?<![A-ZÄÖÜ])RAUM(?![A-ZÄÖÜ])|TREPP|STIEG|AUFZUG|LIFT")


def texte(plan):
    f = plan.factor
    for e in plan.space:
        t = e.dxftype()
        if t == "MTEXT":
            s = e.plain_text()
        elif t == "TEXT":
            s = e.dxf.text
        else:
            continue
        s = " ".join(str(s).upper().split())
        if SCHACHT_RX.search(s) and not AUSSCHLUSS_RX.search(s):
            p = e.dxf.insert
            yield s, (p[0] * f, p[1] * f)


def main() -> None:
    for pid in sys.argv[1:]:
        plan = lade_dxf(str(REPO / "Projekte" / "Rennweg" / f"{NAME.format(pid)}.dxf"))
        k = raeume_aus_kaskade(plan)
        stiegen, sto = RK._marker_punkte(plan)
        tx = list(texte(plan))
        print(f"===== {pid} rest_raeume {len(k.rest_raeume)} schachttexte {len(tx)}", flush=True)
        for r in k.rest_raeume:
            shp = Polygon(r.polygon_mm).buffer(0)
            if shp.area >= RK._SCHACHT_MAX_M2 * 1e6:
                continue
            tuer_n = sum(1 for t in k.tueroeffnungen if shp.distance(Point(t.xy_mm)) <= RK._TUER_RAND_MM)
            innen = [s for s, xy in tx if shp.covers(Point(xy))]
            nah500 = [(s, round(shp.distance(Point(xy)))) for s, xy in tx if shp.distance(Point(xy)) <= 500]
            print(json.dumps({
                "raum": r.id, "typ_kaskade": r.raum_typ, "m2": round(shp.area / 1e6, 3),
                "typisiere_mit_marker": RK._typisiere(shp, k.tueroeffnungen, stiegen, sto)[0],
                "typisiere_ohne_marker": RK._typisiere(shp, k.tueroeffnungen, [], sto)[0],
                "marker_abstand_mm": sorted(round(shp.distance(Point(p))) for p in stiegen)[:2],
                "tuer_n_600": tuer_n, "sto_in": sum(1 for p in sto if shp.covers(Point(p))),
                "schachttext_im_polygon": innen, "schachttext_500mm": nah500}, ensure_ascii=False),
                flush=True)
        if pid == "DG2":
            from notbeleuchtung.raumerkennung.objekt_stiege import finde_stiegen
            huellen = {}
            for e in plan.space:
                if e.dxftype() == "INSERT" and _STAIR_BLOCK.search(e.dxf.name or ""):
                    pts = [p for v in e.virtual_entities() for p in _wcs_pts(v, plan.factor)]
                    if len(pts) >= 3:
                        huellen[e.dxf.name] = MultiPoint(pts).convex_hull
            ks = finde_stiegen(plan)
            polys = [Polygon(c.polygon_mm).buffer(0) for c in ks if len(c.polygon_mm) >= 3]
            u = unary_union(polys) if polys else None
            print("OBJEKT_STIEGE n", len(ks), json.dumps([
                {"layer": c.layer_name, "n_stufen": c.n_stufen, "m2": round(c.flaeche_m2, 2),
                 "conf": c.confidence, "winkel": c.winkel_grad, "quelle": c.quelle} for c in ks],
                ensure_ascii=False), flush=True)
            for name, h in huellen.items():
                s = h.intersection(u).area if u is not None else 0.0
                print("HUELLE", name, "m2", round(h.area / 1e6, 2), "kandidaten_in_huelle_m2", round(s / 1e6, 2),
                      "anteil_huelle", round(s / h.area, 3) if h.area else None,
                      "kandidaten_ausserhalb_m2", round((u.difference(h).area if u is not None else 0) / 1e6, 2),
                      flush=True)
        del plan, k
        gc.collect()


if __name__ == "__main__":
    main()
```

### A.7 Türkette und Tür-Gegenproben (`K5-wohnungen/_tuerkette.py`, `K5-wohnungen/_gegenprobe.py`; B.7, B.15)

Aufruf: `& $PY _tuerkette.py <PLAN>` bzw. `& $PY _gegenprobe.py <PLAN> <V1..V8>` im Arbeitsordner K5-wohnungen. `_gegenprobe.py` importiert `_tuerkette.py` aus demselben Ordner.

```python
"""K5-wohnungen: Tuerkette wie provider.parse Z.64-149 mit EINZELFUNKTIONEN
rekonstruieren (kein provider.parse), Zwischenzustaende loggen, bilde_wohnungen
instrumentiert laufen lassen, gegen den Output-Cache pruefen, Gegenproben.
Aufruf: python _tuerkette.py <PLAN>   (PLAN = EG | OG1 | DG2 ...)
Schreibt NUR nach scratchpad/K5-wohnungen/_out_<PLAN>.json.
"""
from __future__ import annotations

import copy
import json
import math
import pickle
import sys
import time
from collections import Counter
from pathlib import Path

from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

REPO = Path(r"D:\KI Projekt\Notbeleuchtung")
NAME = "{} - Rennweg 15_1030 Wien_Ausfürung-2026-06-12"
OUT = Path(__file__).parent

from notbeleuchtung.hauptengine.contracts.raum_modell import Tuer  # noqa: E402
from notbeleuchtung.raumerkennung.aussenbereich import erkenne_aussenbereiche  # noqa: E402
from notbeleuchtung.raumerkennung.dxf_load import bounds_mm, lade_dxf  # noqa: E402
from notbeleuchtung.raumerkennung.geometrie_typ import typisiere_geometrisch  # noqa: E402
from notbeleuchtung.raumerkennung.geschoss import geschoss_befund  # noqa: E402
from notbeleuchtung.raumerkennung.kaskade import raeume_aus_kaskade  # noqa: E402
from notbeleuchtung.raumerkennung.nutzungsklasse import nutzungsklasse_fuer  # noqa: E402
from notbeleuchtung.raumerkennung.tuer_typisierung import (  # noqa: E402
    brandschutz_hinweise_aus_dxf, typisiere_tueren)
from notbeleuchtung.raumerkennung.tuer_zuordnung import (  # noqa: E402
    AUSSEN, aussen_durchgaenge, durchgaenge_ohne_tuerblatt, ordne_tueren)
from notbeleuchtung.raumerkennung.tueren import (  # noqa: E402
    aussentor_tueren, im_planbereich, text_tueren, tuer_texte, tueren_aus_dxf,
    verschmelze_doppelfluegel)
from notbeleuchtung.raumerkennung.waende import wand_segmente  # noqa: E402
from notbeleuchtung.raumerkennung.wandkoerper import (  # noqa: E402
    aussenkontur, bounds_aus_wandkoerpern, wand_union)
from notbeleuchtung.raumerkennung.wohnungen import bilde_wohnungen  # noqa: E402
from notbeleuchtung.raumerkennung.zirkulation import zirkulation_aus_dxf  # noqa: E402


def xy(p):
    return [round(p[0]), round(p[1])]


def tuer_row(t, by_id):
    def seite(s):
        r = by_id.get(s or "")
        if r is None:
            return s
        return f"{s}:{r.raum_typ or '?'}:{r.nutzungsklasse or nutzungsklasse_fuer(r.raum_typ)}"
    return {"id": t.id, "xy": xy(t.xy_mm), "quelle": t.quelle, "breite": t.breite_mm,
            "ohne_blatt": t.ohne_tuerblatt, "von": seite(t.von_raum),
            "nach": seite(t.nach_raum), "detail": t.tuer_detail}


def main(plan_name: str) -> None:
    t0 = time.time()
    dxf = REPO / "Projekte" / "Rennweg" / f"{NAME.format(plan_name)}.dxf"
    cache = pickle.loads((REPO / "Projekte" / "_ergebnis_raumerkennung" / "Rennweg"
                          / NAME.format(plan_name) / "_cache.pkl").read_bytes())
    log: dict = {"plan": plan_name}
    plan = lade_dxf(str(dxf))
    k = raeume_aus_kaskade(plan)
    try:
        bounds = bounds_mm(plan)
    except ValueError:
        bounds = bounds_aus_wandkoerpern(k.wandkoerper)
    raeume = k.alle_raeume
    raeume = typisiere_geometrisch(plan, raeume)
    tueren = tueren_aus_dxf(plan)
    log["n_tueren_aus_dxf"] = len(tueren)
    if not tueren:
        tueren = [Tuer(id=f"tuer_{i}", xy_mm=o.xy_mm, breite_mm=o.breite_mm,
                       breite_quelle=o.breite_quelle, ist_notausgang=False, quelle=o.quelle)
                  for i, o in enumerate(k.tueroeffnungen, start=1)]
    log["n_tueroeffnungen_kaskade"] = len(k.tueroeffnungen)
    log["oeffnung_quellen"] = dict(Counter(o.quelle for o in k.tueroeffnungen))
    if k.wandkoerper:
        tueren = im_planbereich(tueren, bounds_aus_wandkoerpern(k.wandkoerper))
    log["n_nach_im_planbereich"] = len(tueren)
    zirkulation = zirkulation_aus_dxf(plan)
    befund = geschoss_befund("", str(dxf), plan)
    geschoss = befund.geschoss
    log["geschoss"] = [geschoss, getattr(befund, "quelle", None)]
    aussen = erkenne_aussenbereiche(plan, k.wandkoerper) if k.wandkoerper else None
    if aussen is not None and aussen.komponenten:
        kontur = aussen.gedeckt()
    else:
        kontur = aussenkontur(k.wandkoerper) if k.wandkoerper else None
    n0 = len(tueren)
    tueren += aussentor_tueren(k.tueroeffnungen, tueren, kontur)
    log["n_aussentor"] = len(tueren) - n0
    n0 = len(tueren)
    tueren = verschmelze_doppelfluegel(tueren, wand_segmente(plan))
    log["doppelfluegel_delta"] = len(tueren) - n0
    neu_text = text_tueren(plan, tueren)
    log["text_tueren"] = [(t.quelle, xy(t.xy_mm)) for t in neu_text]
    tueren += neu_text
    ordne_tueren(tueren, k.tueroeffnungen, raeume, kontur)
    n0 = len(tueren)
    tueren = [t for t in tueren if not (t.von_raum == t.nach_raum == AUSSEN)]
    log["n_beidseits_aussen_verworfen"] = n0 - len(tueren)
    for i, t in enumerate(tueren, start=1):
        t.id = f"tuer_{i}"
    if k.wandkoerper:
        wu = wand_union(k.wandkoerper)
        dg = durchgaenge_ohne_tuerblatt(raeume, tueren, wu)
        tueren = tueren + dg
        ag = aussen_durchgaenge(raeume, tueren, wu, kontur)
        tueren = tueren + ag
        log["n_durchgaenge"] = len(dg)
        log["n_aussenoeffnungen"] = len(ag)
    for s in zirkulation.segmente:
        s.quelle = "LINIE"
    flw_enden = [p for s in zirkulation.segmente
                 for p in (s.polyline_mm[0], s.polyline_mm[-1]) if s.polyline_mm]
    typisiere_tueren(tueren, raeume, geschoss, brandschutz_hinweise_aus_dxf(plan),
                     flw_enden, tuer_texte(plan),
                     unary_union(aussen.geschlossen)
                     if aussen is not None and aussen.geschlossen else None)
    by_id = {r.id: r for r in raeume}
    # Zustand VOR bilde_wohnungen (Klassen = statischer Default, da noch None)
    log["raeume_vor"] = [{"id": r.id, "typ": r.raum_typ, "m2": round(r.flaeche_m2, 2),
                          "klasse_attr": r.nutzungsklasse,
                          "klasse_statisch": nutzungsklasse_fuer(r.raum_typ)}
                         for r in raeume]
    log["tueren_nach_typisierung"] = [tuer_row(t, by_id) for t in tueren]
    detail_vor = {t.id: t.tuer_detail for t in tueren}
    klasse_vor = {r.id: r.nutzungsklasse for r in raeume}
    raeume_kopie = copy.deepcopy(raeume)
    tueren_kopie = copy.deepcopy(tueren)

    wohnungen = bilde_wohnungen(raeume, tueren)
    log["klasse_geaendert"] = {r.id: [klasse_vor[r.id], r.nutzungsklasse] for r in raeume
                               if klasse_vor[r.id] != r.nutzungsklasse}
    log["detail_geaendert"] = {t.id: [detail_vor[t.id], t.tuer_detail] for t in tueren
                               if detail_vor[t.id] != t.tuer_detail}
    log["wohnungen"] = [{"id": w.id, "raeume": w.raum_ids, "eingaenge": w.eingangs_tuer_ids}
                        for w in wohnungen]
    log["tueren_final"] = [tuer_row(t, by_id) for t in tueren]
    log["zaehl_detail_final"] = dict(Counter(t.tuer_detail for t in tueren))
    # Tueren je Raum (final)
    je = {}
    for t in tueren:
        for s in (t.von_raum, t.nach_raum):
            je.setdefault(s, []).append(t.id)
    log["tueren_je_raum"] = je
    # Abgleich mit Output-Cache
    c_w = {r["id"]: (r["wohnung_id"], r["nutzungsklasse"], r["typ"]) for r in cache["raeume"]}
    log["abgleich_cache"] = {r.id: {"rekon": [r.wohnung_id, r.nutzungsklasse, r.raum_typ],
                                    "cache": list(c_w.get(r.id, (None, None, None)))}
                             for r in raeume
                             if c_w.get(r.id, (None, None, None))[:2]
                             != (r.wohnung_id, r.nutzungsklasse)}
    log["abgleich_ids_nur_cache"] = sorted(set(c_w) - set(by_id))

    # Gegenprobe A: Wohnungs-Vorraum mit Tuer ins STIEGENHAUS bleibt privat,
    # wenn seine uebrigen Nachbarn privat oder untypisiert sind.
    ra, ta = copy.deepcopy(raeume_kopie), copy.deepcopy(tueren_kopie)
    import notbeleuchtung.raumerkennung.wohnungen as wm
    orig = wm._verfeinere_gang_privat

    def verf_a(rr, tt):
        bid = {r.id: r for r in rr}
        for r in rr:
            if r.raum_typ not in ("GANG", "VORRAUM"):
                continue
            nachbarn, stgh, aussen_n, fremd_n = [], 0, 0, 0
            for t in tt:
                if r.id not in (t.von_raum, t.nach_raum):
                    continue
                a = t.nach_raum if t.von_raum == r.id else t.von_raum
                nachbarn.append(a)
                if a == AUSSEN:
                    aussen_n += 1
                elif a in bid and bid[a].raum_typ == "STIEGENHAUS":
                    stgh += 1
                elif a in bid and wm._klasse(bid[a]) not in ("WOHNUNG_PRIVAT", None):
                    fremd_n += 1
            if nachbarn:
                privat_nachbarn = sum(1 for a in nachbarn if a in bid
                                      and wm._klasse(bid[a]) == "WOHNUNG_PRIVAT")
                ok = aussen_n == 0 and fremd_n == 0 and stgh <= 1 and (
                    r.raum_typ == "VORRAUM" or stgh == 0) and privat_nachbarn >= 1
                r.nutzungsklasse = "WOHNUNG_PRIVAT" if ok else "ALLGEMEIN_ERSCHLIESSUNG"
    wm._verfeinere_gang_privat = verf_a
    try:
        wa = wm.bilde_wohnungen(ra, ta)
    finally:
        wm._verfeinere_gang_privat = orig
    log["gegenprobe_A_vorraum_mit_1_stgh_tuer_privat"] = [
        {"id": w.id, "raeume": w.raum_ids, "eingaenge": w.eingangs_tuer_ids} for w in wa]

    # Gegenprobe B: zusaetzlich UNBEKANNT-Raeume mit Wohn-Stempel (Wohnk*, Wohn*) -> WOHNUNG_PRIVAT
    rb, tb = copy.deepcopy(raeume_kopie), copy.deepcopy(tueren_kopie)
    stempel_je = {}
    for z in k.zuordnungen:
        if z.raum is not None:
            stempel_je.setdefault(z.raum.id, []).append(z.stempel.name or "")
    log["stempel_je_raum"] = stempel_je
    for r in rb:
        if not r.raum_typ and any("wohn" in s.lower() for s in stempel_je.get(r.id, [])):
            r.nutzungsklasse = "WOHNUNG_PRIVAT"
    wm._verfeinere_gang_privat = verf_a
    try:
        wb = wm.bilde_wohnungen(rb, tb)
    finally:
        wm._verfeinere_gang_privat = orig
    log["gegenprobe_B_A_plus_wohnstempel_privat"] = [
        {"id": w.id, "raeume": w.raum_ids, "eingaenge": w.eingangs_tuer_ids} for w in wb]

    # Darstellung: Wohnungs-Umriss wie raumerkennung_darstellung Z.710-722
    polys = {r["id"]: Polygon(r["polygon_mm"]).buffer(0) for r in cache["raeume"]
             if len(r["polygon_mm"]) >= 3}
    je_w = {}
    for r in cache["raeume"]:
        if r["wohnung_id"] and r["id"] in polys:
            je_w.setdefault(r["wohnung_id"], []).append(polys[r["id"]])
    darst = {}
    for wid, ps in je_w.items():
        u = unary_union(ps).buffer(200).buffer(-200)
        teile = list(getattr(u, "geoms", [u]))
        huelle = unary_union([Polygon(g.exterior) for g in teile])
        drin = {}
        for rid, g in polys.items():
            rp = g.representative_point()
            if huelle.covers(rp):
                drin[rid] = {"in_union": u.covers(rp),
                             "anteil_in_huelle": round(g.intersection(huelle).area / g.area, 3)}
        darst[wid] = {"n_teile": len(teile), "n_loecher": sum(len(g.interiors) for g in teile),
                      "flaeche_union_m2": round(u.area / 1e6, 2),
                      "flaeche_aussenring_m2": round(huelle.area / 1e6, 2),
                      "raeume_repr_punkt_im_aussenring": drin}
    log["darstellung_umriss"] = darst
    log["laufzeit_s"] = round(time.time() - t0, 1)
    (OUT / f"_out_{plan_name}.json").write_text(json.dumps(log, ensure_ascii=False, indent=1),
                                                encoding="utf-8")
    print(json.dumps({"plan": plan_name, "wohnungen": log["wohnungen"],
                      "abgleich_cache": log["abgleich_cache"],
                      "abgleich_ids_nur_cache": log["abgleich_ids_nur_cache"],
                      "laufzeit_s": log["laufzeit_s"]}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
```

```python
"""K5-wohnungen Gegenproben (nur in-memory, nichts im Repo):
V1 'bloecke'  : tueren.tuer_oeffnungen liefert Tuer-Bloecke am BBox-Zentrum statt am
                INSERT-Punkt (ArchiCAD-Weltkoordinaten-Bloecke) -> kaskade sieht echte Tueren.
V2 'streifen' : V1 + durchgaenge_ohne_tuerblatt nur, wenn die freie Zone BEIDE Raeume
                beruehrt (Luecke QUER durch die Wand statt Streifen entlang einer Wandseite).
Aufruf: python _gegenprobe.py <PLAN> <V1|V2>   -> _out_<PLAN>.json in Unterordner gp_<V>
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import ezdxf.bbox

sys.path.insert(0, str(Path(__file__).parent))
import _tuerkette as tk  # noqa: E402

import notbeleuchtung.raumerkennung.kaskade as km  # noqa: E402
import notbeleuchtung.raumerkennung.tueren as tm  # noqa: E402
from notbeleuchtung.hauptengine.contracts.raum_modell import Tuer  # noqa: E402
from notbeleuchtung.raumerkennung.tuer_zuordnung import (  # noqa: E402
    _DURCHGANG_MIN_MM, _KONTAKT_MM, _TUER_NAH_MM, _raum_polys)

_BERUEHRT_MM = 60.0


def tuer_oeffnungen_bbox(plan):
    out = []

    def _walk(entities, tiefe=0):
        for e in entities:
            t = e.dxftype()
            if t == "INSERT":
                name = str(e.dxf.name)
                if tm._ist_tuer_block(name):
                    breite = tm._breite_mm(name)
                    bq = "BLOCKNAME"
                    if breite is None:
                        breite = tm._blattbreite_aus_block(e, plan.factor)
                        bq = "GEOMETRIE_SCHWENKRADIUS" if breite is not None else "UNBEKANNT"
                    b = ezdxf.bbox.extents([e])
                    xy = (plan._scale((b.center.x, b.center.y)) if b.has_data
                          else plan._scale(e.dxf.insert))
                    winkel = float(e.dxf.get("rotation", 0.0))
                    if WINKEL_VERWERFEN and b.has_data:
                        ix, iy = e.dxf.insert[0], e.dxf.insert[1]
                        aussen = not (b.extmin.x - 100 <= ix <= b.extmax.x + 100
                                      and b.extmin.y - 100 <= iy <= b.extmax.y + 100)
                        if aussen:   # Weltkoordinaten-Block: Rotation sagt nichts
                            winkel = None
                    out.append(tm.TuerOeffnung(xy_mm=xy, breite_mm=breite,
                                               winkel_grad=winkel,
                                               quelle="block", breite_quelle=bq))
                elif tiefe < 3:
                    try:
                        _walk(e.virtual_entities(), tiefe + 1)
                    except Exception:  # noqa: BLE001
                        pass
            elif t == "ARC":
                r = float(e.dxf.radius) * plan.factor
                sweep = (float(e.dxf.end_angle) - float(e.dxf.start_angle)) % 360.0
                if tm._ARC_MIN_MM < r < tm._ARC_MAX_MM and tm._SWEEP_MIN <= sweep <= tm._SWEEP_MAX:
                    out.append(tm.TuerOeffnung(xy_mm=plan._scale(e.dxf.center),
                                               breite_mm=float(round(r)),
                                               winkel_grad=float(e.dxf.start_angle),
                                               quelle="arc",
                                               breite_quelle="GEOMETRIE_SCHWENKRADIUS"))
    _walk(plan.space)
    return out


def durchgaenge_quer(raeume, tueren, wand_union_geom):
    if wand_union_geom is None or wand_union_geom.is_empty:
        return []
    polys = _raum_polys(raeume)
    tuer_punkte = [t.xy_mm for t in tueren]
    out = []
    for i, (ra, pa, _) in enumerate(polys):
        for rb, pb, _ in polys[i + 1:]:
            if pa.distance(pb) > 2 * _KONTAKT_MM:
                continue
            frei = pa.buffer(_KONTAKT_MM).intersection(pb.buffer(_KONTAKT_MM)).difference(
                wand_union_geom)
            if frei.is_empty:
                continue
            for g in (list(frei.geoms) if hasattr(frei, "geoms") else [frei]):
                if g.distance(pa) > _BERUEHRT_MM or g.distance(pb) > _BERUEHRT_MM:
                    continue   # Streifen nur an EINER Wandseite -> keine Oeffnung
                # Oeffnungsbreite = Ausdehnung der Zone entlang der Wand:
                # Schnittlaenge mit dem gepufferten Rand von A
                mrr = g.minimum_rotated_rectangle
                co = list(getattr(mrr, "exterior", g).coords)[:4]
                if len(co) < 3:
                    continue
                breite = max(math.dist(co[0], co[1]), math.dist(co[1], co[2]))
                if breite < _DURCHGANG_MIN_MM:
                    continue
                c = g.centroid
                xy = (float(c.x), float(c.y))
                if any(math.dist(xy, p) < _TUER_NAH_MM for p in tuer_punkte):
                    continue
                out.append(Tuer(id=f"durchgang_{len(out) + 1}", xy_mm=xy,
                                breite_mm=float(round(breite)),
                                breite_quelle="GEOMETRIE_OEFFNUNG", von_raum=ra.id,
                                nach_raum=rb.id, ohne_tuerblatt=True, quelle="durchgang"))
                tuer_punkte.append(xy)
    return out


def _bogen_in(e, tiefe=0):
    try:
        for v in e.virtual_entities():
            if v.dxftype() == "ARC":
                return v
            if v.dxftype() == "INSERT" and tiefe < 2:
                a = _bogen_in(v, tiefe + 1)
                if a is not None:
                    return a
    except Exception:  # noqa: BLE001
        pass
    return None


def tuer_oeffnungen_bogen(plan):
    """Tuer-Bloecke: Oeffnung = Mitte der GESCHLOSSENEN Blattlage aus dem Schwenkbogen
    im Block (Drehpunkt + Bogenende, das naeher an der Wandunion liegt); Sehne =
    Richtung Drehpunkt->geschlossenes Bogenende. Ohne Bogen: BBox-Zentrum, Winkel None."""
    from shapely.geometry import Point as _P

    from notbeleuchtung.raumerkennung.wandkoerper import finde_wandkoerper, wand_union
    wu = wand_union(finde_wandkoerper(plan))
    basis = tuer_oeffnungen_bbox(plan)            # liefert ARC-Oeffnungen unveraendert
    arcs = [o for o in basis if o.quelle == "arc"]
    out = list(arcs)
    f = plan.factor

    def _walk(entities, tiefe=0):
        for e in entities:
            if e.dxftype() != "INSERT":
                continue
            name = str(e.dxf.name)
            if tm._ist_tuer_block(name):
                a = _bogen_in(e)
                if a is not None:
                    c = (a.dxf.center[0] * f, a.dxf.center[1] * f)
                    r = float(a.dxf.radius) * f
                    ends = [(c[0] + r * math.cos(math.radians(w)),
                             c[1] + r * math.sin(math.radians(w)))
                            for w in (a.dxf.start_angle, a.dxf.end_angle)]
                    mitten = [((c[0] + p[0]) / 2, (c[1] + p[1]) / 2) for p in ends]
                    i = min((0, 1), key=lambda k: wu.distance(_P(mitten[k])))
                    xy = mitten[i]
                    winkel = math.degrees(math.atan2(ends[i][1] - c[1], ends[i][0] - c[0]))
                    breite = float(round(r))
                else:
                    b = ezdxf.bbox.extents([e])
                    xy = plan._scale((b.center.x, b.center.y))
                    winkel, breite = None, None
                out.append(tm.TuerOeffnung(xy_mm=xy, breite_mm=breite, winkel_grad=winkel,
                                           quelle="block",
                                           breite_quelle="GEOMETRIE_SCHWENKRADIUS"
                                           if breite else "UNBEKANNT"))
            elif tiefe < 3:
                try:
                    _walk(e.virtual_entities(), tiefe + 1)
                except Exception:  # noqa: BLE001
                    pass
    _walk(plan.space)
    return out


def main(pn: str, variante: str) -> None:
    global WINKEL_VERWERFEN
    WINKEL_VERWERFEN = variante in ("V3", "V4")
    km.tuer_oeffnungen = (tuer_oeffnungen_bogen if variante in ("V5", "V6", "V7", "V8")
                          else tuer_oeffnungen_bbox)
    if variante in ("V7", "V8"):
        import notbeleuchtung.raumerkennung.tuer_zuordnung as tz
        tz._PROBE_MM = 600.0     # Tuerpunkt an EINER Wandflaeche: Probe muss dicke Wand ueberspringen
    if variante in ("V2", "V4", "V6", "V8"):
        tk.durchgaenge_ohne_tuerblatt = durchgaenge_quer
    ziel = Path(__file__).parent / f"gp_{variante}"
    ziel.mkdir(exist_ok=True)
    tk.OUT = ziel
    tk.main(pn)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
```

### A.8 Gegenprüf-Skripte der Cluster (B.4, B.5, B.11, B.12, B.14, B.16)

Aufruf jeweils im eigenen Arbeitsordner. `_plan_werkzeug._plan(P)` (in A.8.1-A.8.3) ist das Scratchpad-Werkzeug aus dem Kopf („Werkzeuge“) und tut nur `lade_dxf(Projekte/Rennweg/<P> - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf)`. Nicht im Anhang, weil ihre Zahlen allein kein Akzeptanzkriterium tragen oder durch B.13 ersetzt sind: `_k4g_mess.py` (B.5, zweite Versiegelungsmessung), `_regel_messung.py` und K1-`_pruef2` (B.3, frühere Messungen), `_tuerbloecke.py` (B.6, Einzelblöcke OG1), `_k3_messung2.py`, `_pk3.py`, `_pk3c.py` (B.13, frühere Messungen).

#### A.8.1 `K2b-schacht-dg1-dg2-pruefung-code/_pruef.py` (B.4 Aufruf 1)

```python
"""Gegenpruefung K2b (nur lesen): Kaskade in-memory, R-Stufe per Monkeypatch mitgeschnitten.

Aufruf: python _pruef.py <PLAN>  -> schreibt pruef_<PLAN>.json neben das Skript
"""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent))
import _plan_werkzeug as W  # noqa: E402
import skimage  # noqa: E402
from skimage.measure import find_contours  # noqa: E402
from skimage.measure import label as sk_label  # noqa: E402

import notbeleuchtung.raumerkennung.rest_komponenten as RK  # noqa: E402
from notbeleuchtung.raumerkennung import kaskade as KA  # noqa: E402
from notbeleuchtung.raumerkennung.geometrie_typ import stiege_rechtecke  # noqa: E402
from notbeleuchtung.raumerkennung.stempel_flutung import _fuelle, _Raster  # noqa: E402
from notbeleuchtung.raumerkennung.wandkoerper import aussenkontur  # noqa: E402

P = sys.argv[1]
cap = {"label_in": None, "vek": [], "typ": [], "raster": None}

_orig_label = RK.label


def _lab(img, *a, **k):
    cap["label_in"] = np.array(img, copy=True)
    return _orig_label(img, *a, **k)


_orig_vek = RK._vektorisiere


def _vek(mask, raster, grenze):
    shp = _orig_vek(mask, raster, grenze)
    cap["raster"] = raster
    cap["vek"].append({"mask_m2": round(float(mask.sum()) * raster.res ** 2 / 1e6, 3),
                       "n_konturen": len(find_contours(mask.astype(np.uint8), 0.5)),
                       "vektor_m2": round(shp.area / 1e6, 3) if not shp.is_empty else 0.0})
    return shp


_orig_typ = RK._typisiere


def _typ(shp, tueren, stiegen, sto):
    r = _orig_typ(shp, tueren, stiegen, sto)
    cap["typ"].append({"m2": round(shp.area / 1e6, 3), "bounds": [round(v) for v in shp.bounds],
                       "ergebnis": r[0],
                       "tuer_n_600": sum(1 for t in tueren if shp.distance(Point(t.xy_mm)) <= RK._TUER_RAND_MM),
                       "marker_dist_mm": sorted(round(shp.distance(Point(p))) for p in stiegen)[:3],
                       "sto_n": len(sto)})
    return r


RK.label = _lab
RK._vektorisiere = _vek
RK._typisiere = _typ

# ── synthetische Mechanik-Probe (8er-Label + groesste Kontur) ──
m = np.zeros((20, 20), bool)
m[2:8, 2:8] = True
m[8:14, 8:14] = True
syn_r = _Raster(x0=0.0, y0=0.0, res=50.0, pad=0, shape=(20, 20))
syn = {"skimage": skimage.__version__, "label8_n": int(sk_label(m).max()),
       "label4_n": int(sk_label(m, connectivity=1).max()),
       "find_contours_n": len(find_contours(m.astype(np.uint8), 0.5)),
       "maske_mm2": float(m.sum()) * 2500, "vektor_mm2": round(_orig_vek(m, syn_r, None).area)}

plan = W._plan(P)
doc = plan.doc
erg = KA.raeume_aus_kaskade(plan)

TXT = re.compile(r"DDB|BDB|DBA|SCHACHT", re.IGNORECASE)


def eff_farbe(e):
    c = e.dxf.get("color", 256)
    if c in (0, 256):
        lay = doc.layers.get(e.dxf.get("layer", "0"))
        return lay.color if lay is not None else c
    return c


texte, nested = [], Counter()
rot = []


def walk(ents, tiefe, pfad):
    for e in ents:
        t = e.dxftype()
        if t == "INSERT":
            if tiefe < 3:
                try:
                    walk(e.virtual_entities(), tiefe + 1, pfad + [str(e.dxf.name)])
                except Exception:  # noqa: BLE001
                    pass
            continue
        if t in ("MTEXT", "TEXT"):
            s = e.plain_text() if t == "MTEXT" else e.dxf.text
            if s and TXT.search(s):
                if tiefe == 0:
                    texte.append({"text": s.replace("\n", " | "), "layer": e.dxf.layer,
                                  "xy": [round(v) for v in plan._scale(e.dxf.insert)]})
                else:
                    nested["text"] += 1
        elif t in ("LWPOLYLINE", "POLYLINE"):
            pts = plan.entity_points(e)
            zu = getattr(e, "closed", False) or (len(pts) > 2 and math.dist(pts[0], pts[-1]) < 5)
            if len(pts) >= 3 and zu and eff_farbe(e) == 1:
                if tiefe == 0:
                    rot.append((e.dxf.layer, pts))
                else:
                    nested["rot_geschlossen:" + pfad[0].split("_")[0]] += 1


walk(plan.space, 0, [])

roh_lhf = [Polygon(r.polygon_roh or r.polygon_mm).buffer(0) for r in erg.raeume if len(r.polygon_roh or r.polygon_mm) >= 3]
lhf_union = unary_union(roh_lhf)
final = [(r, Polygon(r.polygon_mm).buffer(0)) for r in erg.alle_raeume if len(r.polygon_mm) >= 3]

raster = cap["raster"]
frei = cap["label_in"]
lab8 = sk_label(frei) if frei is not None else None
lab4 = sk_label(frei, connectivity=1) if frei is not None else None
n8 = np.bincount(lab8.ravel()) if lab8 is not None else None
n4 = np.bincount(lab4.ravel()) if lab4 is not None else None


def naechst_text(g):
    if not texte:
        return None
    d, t = min(((g.distance(Point(t["xy"])), t["text"]) for t in texte), key=lambda x: x[0])
    return [round(d), t]


konturen = []
for layer, pts in rot:
    g = Polygon(pts).buffer(0)
    if g.is_empty or not (0.02e6 <= g.area <= 3e6):
        continue
    tx = naechst_text(g)
    if tx is None or tx[0] > 1500:
        continue
    zell = np.zeros(frei.shape, bool)
    _fuelle(zell, g, raster)
    fz = zell & frei
    konturen.append({
        "layer": layer, "m2": round(g.area / 1e6, 3), "c": [round(g.centroid.x), round(g.centroid.y)],
        "text": tx, "anteil_in_LHF_roh": round(g.intersection(lhf_union).area / g.area, 3),
        "final_raeume": [(r.id, r.raum_typ, round(p.intersection(g).area / g.area, 2)) for r, p in final
                         if p.intersection(g).area / g.area > 0.05],
        "zellen": int(zell.sum()), "frei_R": int(fz.sum()),
        "label8_m2": sorted({round(n8[k] * 2500 / 1e6, 3) for k in lab8[fz] if k}),
        "label4_m2": sorted({round(n4[k] * 2500 / 1e6, 3) for k in lab4[fz] if k}),
    })

# Rest-Raeume mit Texten im Polygon
rest = []
for r in erg.rest_raeume:
    p = Polygon(r.polygon_roh or r.polygon_mm).buffer(0)
    rest.append({"id": r.id, "typ": r.raum_typ, "m2": round(p.area / 1e6, 3), "bounds": [round(v) for v in p.bounds],
                 "texte_im_polygon": [t["text"] for t in texte if p.buffer(50).covers(Point(t["xy"]))],
                 "bereinigung": [(b.regel, b.gegenspieler, round(b.flaeche_m2, 3)) for b in r.bereinigung]})

stiegen, sto = RK._marker_punkte(plan)
namen = [str(e.dxf.name) for e in plan.space if e.dxftype() == "INSERT" and RK._STIEGE_RX.search(str(e.dxf.name))]

wk = erg.wandkoerper
roof = [k for k in wk if k.quelle.startswith("block:Roof")]
k_voll = aussenkontur(wk, d_mm=1000.0)
k_ohne = aussenkontur([k for k in wk if not k.quelle.startswith("block:Roof")], d_mm=1000.0)

# Fenster-Bloecke: Entity-Typen
fen = Counter()


def walk_f(ents, tiefe, im_fenster):
    for e in ents:
        t = e.dxftype()
        if t == "INSERT" and tiefe < 4:
            n = str(e.dxf.name).lower()
            try:
                walk_f(e.virtual_entities(), tiefe + 1, im_fenster or "fenster" in n or n.startswith("window"))
            except Exception:  # noqa: BLE001
                pass
        elif im_fenster:
            fen[t] += 1


walk_f(plan.space, 0, False)

out = {
    "plan": P, "kette": erg.kette, "synthetik": syn,
    "raeume": [(r.id, r.raum_typ, erg.quelle.get(r.id), round(r.flaeche_m2, 3), len(r.polygon_roh or r.polygon_mm),
                [(b.regel, b.gegenspieler, round(b.flaeche_m2, 3)) for b in r.bereinigung]) for r in erg.alle_raeume],
    "stempel_mit_schachttoken": [z.stempel.name for z in erg.zuordnungen if TXT.search(z.stempel.name or "")],
    "texte_top": texte, "nested": dict(nested),
    "rote_konturen_mit_text": konturen,
    "rest": rest,
    "typisiere_aufrufe": cap["typ"],
    "vektorisierung": cap["vek"],
    "labels_unter_1m2_naehe_text": [],
    "stiegen_marker": list(zip(namen, [[round(v) for v in s] for s in stiegen])),
    "stiege_rechtecke": [[round(v) for v in (min(x for x, _ in r[0]), min(y for _, y in r[0]),
                                             max(x for x, _ in r[0]), max(y for _, y in r[0]))] for r in stiege_rechtecke(plan)],
    "wk_n": len(wk), "wk_roof_n": len(roof), "wk_material_schacht": Counter(k.layer for k in wk if "SCHACHT" in k.material),
    "kontur_voll_m2": round(k_voll.area / 1e6, 2), "kontur_ohne_roof_m2": round(k_ohne.area / 1e6, 2),
    "rest_in_kontur": {r.id: [round(Polygon(r.polygon_roh or r.polygon_mm).buffer(0).intersection(k_voll).area / 1e6, 3),
                              round(Polygon(r.polygon_roh or r.polygon_mm).buffer(0).intersection(k_ohne).area / 1e6, 3)]
                       for r in erg.rest_raeume},
    "fenster_entity_typen": dict(fen),
}
for k in range(1, int(lab8.max()) + 1):
    a = n8[k] * 2500 / 1e6
    if 0.1 <= a < 1.0:
        rr, cc = np.nonzero(lab8 == k)
        xy = raster.mm(float(rr.mean()), float(cc.mean()))
        tx = naechst_text(Point(xy))
        if tx and tx[0] <= 1000:
            out["labels_unter_1m2_naehe_text"].append([round(a, 3), [round(v) for v in xy], tx])
(HIER / f"pruef_{P}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print("ok", P, erg.kette)
```

#### A.8.2 `K2b-schacht-dg1-dg2-pruefung-code/_pruef2.py` (B.4 Aufruf 2)

```python
"""Gegenpruefung K2b Teil 2 (nur lesen): Raumdef-Polylinien, 4er- vs 8er-Label, R/L-Ueberlappung.

Aufruf: python _pruef2.py <PLAN> -> pruef2_<PLAN>.json
"""
import json
import sys
from pathlib import Path

import numpy as np
from shapely.geometry import Polygon

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent))
import _plan_werkzeug as W  # noqa: E402
from skimage.measure import label as sk_label  # noqa: E402

import notbeleuchtung.raumerkennung.rest_komponenten as RK  # noqa: E402
from notbeleuchtung.raumerkennung import kaskade as KA  # noqa: E402
from notbeleuchtung.raumerkennung.raumlayer import _flaeche_m2, _ist_raum_layer  # noqa: E402

P = sys.argv[1]
cap = {}
_ol, _ov = RK.label, RK._vektorisiere


def _lab(img, *a, **k):
    cap["frei"] = np.array(img, copy=True)
    return _ol(img, *a, **k)


def _vek(mask, raster, grenze):
    cap["raster"], cap["grenze"] = raster, grenze
    return _ov(mask, raster, grenze)


RK.label, RK._vektorisiere = _lab, _vek
plan = W._plan(P)

# Raumdef-Polylinien ohne Flaechenfilter
rd = []
for e in plan.space:
    if not _ist_raum_layer(str(e.dxf.layer)) or e.dxftype() not in ("LWPOLYLINE", "POLYLINE"):
        continue
    pts = plan.entity_points(e)
    rd.append({"layer": e.dxf.layer, "closed": bool(getattr(e, "closed", False)), "n": len(pts),
               "m2": round(_flaeche_m2(pts), 3) if len(pts) >= 3 else 0})

erg = KA.raeume_aus_kaskade(plan)
frei, raster, grenze = cap["frei"], cap["raster"], cap["grenze"]
stiegen, sto = RK._marker_punkte(plan)


def komps(conn):
    lab = sk_label(frei, connectivity=conn)
    n = np.bincount(lab.ravel())
    out = []
    for k in range(1, int(lab.max()) + 1):
        if n[k] * 2500 < 1e6:
            continue
        shp = _ov(lab == k, raster, grenze)
        if shp.is_empty or shp.area < 1e6:
            continue
        typ = RK._typisiere(shp, erg.tueroeffnungen, stiegen, sto)[0]
        out.append({"mask_m2": round(n[k] * 2500 / 1e6, 3), "vektor_m2": round(shp.area / 1e6, 3), "typ": typ,
                    "c": [round(shp.centroid.x), round(shp.centroid.y)]})
    return out


L = [(r.id, Polygon(r.polygon_roh or r.polygon_mm).buffer(0)) for r in erg.raeume]
ueber = []
for r in erg.rest_raeume:
    p = Polygon(r.polygon_roh or r.polygon_mm).buffer(0)
    for i, q in L:
        a = p.intersection(q).area
        if a > 0:
            ueber.append([r.id, i, round(a, 1)])

out = {"plan": P, "kette": erg.kette,
       "raumdef": sorted(rd, key=lambda d: d["m2"]),
       "komponenten_8er": komps(2), "komponenten_4er": komps(1),
       "rest_L_schnitt_mm2": ueber}
(HIER / f"pruef2_{P}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", P, erg.kette)
```

#### A.8.3 `K2b-schacht-dg1-dg2/_label16.py` (B.4 Aufruf 3)

```python
"""DG2: Label der Schachtreihe L1/L2/S5 -> Konturen/Vektorisierung (nur lesen)."""
import json
import sys
from pathlib import Path

import numpy as np
from shapely.geometry import Point, Polygon
from skimage.measure import find_contours, label
from skimage.morphology import disk

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _plan_werkzeug as W  # noqa: E402
from notbeleuchtung.raumerkennung import rest_komponenten as RK  # noqa: E402
from notbeleuchtung.raumerkennung.kaskade import raeume_aus_kaskade  # noqa: E402
from notbeleuchtung.raumerkennung.stempel_flutung import _fuelle, _Raster, _vektorisiere  # noqa: E402
from notbeleuchtung.raumerkennung.wandkoerper import aussenkontur, bounds_aus_wandkoerpern, wand_union  # noqa: E402

plan = W._plan("DG2")
erg = raeume_aus_kaskade(plan)
wk = erg.wandkoerper
belegte = [r.polygon_roh or r.polygon_mm for r in erg.raeume] + [r.polygon_roh or r.polygon_mm for r, _ in erg.entfallen]
union = wand_union(wk)
kontur = aussenkontur(wk, d_mm=1000.0)
b = bounds_aus_wandkoerpern(wk)
res, pad = 50.0, 4
h = int(np.ceil((b.max_xy[1] - b.min_xy[1]) / res)) + 2 * pad + 1
w = int(np.ceil((b.max_xy[0] - b.min_xy[0]) / res)) + 2 * pad + 1
raster = _Raster(x0=b.min_xy[0], y0=b.min_xy[1], res=res, pad=pad, shape=(h, w))
innen = np.zeros((h, w), bool)
_fuelle(innen, kontur, raster)
blockiert = ~innen
wand = np.zeros((h, w), bool)
_fuelle(wand, union, raster)
blockiert |= wand
for t in erg.tueroeffnungen:
    r_px = max(1, round(max(RK._TUER_RAND_MM, t.breite_mm or 0.0) / res))
    rr, cc = raster.px(t.xy_mm)
    d = disk(r_px, dtype=bool)
    r0, c0 = rr - r_px, cc - r_px
    rs = slice(max(r0, 0), min(r0 + d.shape[0], h))
    cs = slice(max(c0, 0), min(c0 + d.shape[1], w))
    blockiert[rs, cs] |= d[rs.start - r0:rs.stop - r0, cs.start - c0:cs.stop - c0]
for pl in belegte:
    shp = Polygon(pl).buffer(RK._BELEGT_PUFFER_MM)
    if not shp.is_empty:
        _fuelle(blockiert, shp, raster)
labels = label(~blockiert)
labels4 = label(~blockiert, connectivity=1)
punkte = {"L2": (12555467, 356216889), "S5": (12555601, 356216024), "rest1_centroid": (12553505, 356217048)}
out = {}
for name, xy in punkte.items():
    r, c = raster.px(xy)
    out[name] = {"label8": int(labels[r, c]), "label4": int(labels4[r, c])}
k = out["L2"]["label8"]
m = labels == k
konts = find_contours(m.astype(np.uint8), 0.5)


def sh(kk):
    return 0.5 * abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(kk, list(kk[1:]) + [kk[0]])))


poly = _vektorisiere(m, raster, union.boundary)
rest1 = next(r for r in erg.rest_raeume if r.id == "rest_1")
out["label8_m2"] = round(m.sum() * res * res / 1e6, 3)
out["n_konturen"] = len(konts)
out["kontur_flaechen_m2"] = sorted([round(sh(kk) * res * res / 1e6, 3) for kk in konts], reverse=True)[:6]
out["vektor_m2"] = round(poly.area / 1e6, 3)
out["vektor_deckt"] = {n: poly.buffer(1).covers(Point(xy)) for n, xy in punkte.items()}
out["rest1_m2"] = round(rest1.flaeche_m2, 3)
out["label4_groessen_m2"] = {n: round((labels4 == out[n]["label4"]).sum() * res * res / 1e6, 3)
                             for n in punkte if out[n]["label4"]}
print(json.dumps(out, ensure_ascii=False, indent=1))
```

#### A.8.4 `K6b-output-gang-pruefung/_synth.py` (B.5 Durchgänge und Diele)

```python
"""Synthetische Gegenprobe: durchgaenge_ohne_tuerblatt (duenne Wand) und bilde_wohnungen (Diele)."""
from shapely.geometry import box, MultiPolygon
from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.tuer_zuordnung import durchgaenge_ohne_tuerblatt
from notbeleuchtung.raumerkennung.tuer_typisierung import typisiere_tueren
from notbeleuchtung.raumerkennung.wohnungen import bilde_wohnungen


def raum(i, typ, x0, y0, x1, y1):
    b = box(x0, y0, x1, y1)
    return Raum(id=i, raum_typ=typ, polygon_mm=list(b.exterior.coords)[:-1], flaeche_m2=b.area / 1e6)


print("== Durchgang: Wandstaerke t, keine Luecke, keine Tuer ==")
for t in (100, 200, 240, 260, 300):
    a, b = raum("a", "ZIMMER", 0, 0, 5000, 4000), raum("b", "BAD", 5000 + t, 0, 10000, 4000)
    d = durchgaenge_ohne_tuerblatt([a, b], [], MultiPolygon([box(5000, 0, 5000 + t, 4000)]))
    print(f"t={t}", [(x.id, x.breite_mm, tuple(round(v) for v in x.xy_mm)) for x in d])

print("== Durchgang: t=100, echte Tuer 900 mm bei y 500..1400 (Tuer bekannt) ==")
a, b = raum("a", "ZIMMER", 0, 0, 5000, 4000), raum("b", "BAD", 5100, 0, 10000, 4000)
wand = box(5000, 1400, 5100, 4000)
tuer = Tuer(id="t1", xy_mm=(5050.0, 950.0), breite_mm=900)
d = durchgaenge_ohne_tuerblatt([a, b], [tuer], MultiPolygon([wand]))
print([(x.id, x.breite_mm, tuple(round(v) for v in x.xy_mm)) for x in d])

print("== Wohnung: Diele VR mit Eingangstuer ins STIEGENHAUS, AR/WC/ZI/BAD nur ueber VR ==")
rs = [raum("stgh", "STIEGENHAUS", 0, 0, 3000, 3000), raum("vr", "VORRAUM", 3100, 0, 6000, 1500),
      raum("ar", "ABSTELLRAUM", 3100, 1600, 4000, 3000), raum("wc", "WC", 4100, 1600, 5000, 3000),
      raum("zi", "ZIMMER", 6100, 0, 10000, 3000), raum("bad", "BAD", 3100, -2600, 6000, -100)]
ts = [Tuer(id=f"t_{n}", xy_mm=(0.0, 0.0), breite_mm=900, von_raum="vr", nach_raum=n)
      for n in ("stgh", "ar", "wc", "zi", "bad")]
typisiere_tueren(ts, rs, "OG1")
print("vor bilde:", [(t.id, t.tuer_detail) for t in ts])
ws = bilde_wohnungen(rs, ts)
print("nach bilde:", [(t.id, t.tuer_detail) for t in ts])
print("vr klasse:", next(r for r in rs if r.id == "vr").nutzungsklasse)
print("wohnungen:", [(w.id, w.raum_ids, w.eingangs_tuer_ids) for w in ws])
# Cluster-Kriterium: private Nachbarn des VR, Komponenten ueber zimmertueren OHNE vr
privat_nachbarn = {"ar", "wc", "zi", "bad"}
kanten = [(t.von_raum, t.nach_raum) for t in ts if "vr" not in (t.von_raum, t.nach_raum)]
print("zimmertuer-Kanten ohne vr:", kanten, "-> gruppen:", len(privat_nachbarn))
```

#### A.8.5 `K4-aussen-pruefung-code/_pruef.py` (B.5 Versiegelung, B.16)

```python
"""Gegenpruefung K4-aussen (nur lesen). Aufruf: PY _pruef.py synth | <PLAN> [...]"""
from __future__ import annotations

import json
import math
import pickle
import re
import sys
from pathlib import Path

from shapely import wkb
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import nearest_points, unary_union

from notbeleuchtung.raumerkennung import aussenbereich as ab
from notbeleuchtung.raumerkennung.wandkoerper import Wandkoerper

REPO = Path(r"D:\KI Projekt\Notbeleuchtung")
NAME = "{} - Rennweg 15_1030 Wien_Ausfürung-2026-06-12"
HIER = Path(__file__).parent
OEFF_RX = re.compile(r"FENSTER|WINDOW|T.R|TUER|DOOR|SCHIEBE", re.IGNORECASE)


def _wk(poly):
    return Wandkoerper(polygon_mm=list(poly.exterior.coords), material="X", layer="",
                       quelle="msp", breite_mm=0.0)


def synth():
    out = []
    L = 6000.0
    for t in (200.0, 400.0, 600.0):
        for g in (800.0, 1000.0, 1300.0, 1400.0, 1600.0, 2000.0):
            # quadratischer Raum innen 0..L, Wandring Dicke t, Luecke g mittig in der Suedwand
            walls = [box(-t, -t, L / 2 - g / 2, 0), box(L / 2 + g / 2, -t, L + t, 0),
                     box(-t, L, L + t, L + t), box(-t, 0, 0, L), box(L, 0, L + t, L)]
            wz = ab._wand_geschlossen([_wk(w) for w in walls], ab._SCHLIESS_MM)
            polys = list(getattr(wz, "geoms", [wz]))
            loecher = [Polygon(i) for p in polys for i in p.interiors]
            rest = None
            if loecher:
                h = max(loecher, key=lambda p: p.area)
                rest = round(h.distance(Polygon(max(polys, key=lambda p: p.area).exterior).exterior))
            out.append({"t": t, "g": g, "versiegelt": bool(loecher), "restbarriere_mm": rest})
    print(json.dumps(out))


def main(pid: str) -> dict:
    from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
    from notbeleuchtung.raumerkennung.tuer_zuordnung import aussen_durchgaenge
    from notbeleuchtung.raumerkennung.tueren import im_planbereich, tuer_oeffnungen
    from notbeleuchtung.raumerkennung.wandkoerper import (bounds_aus_wandkoerpern,
                                                          finde_wandkoerper, wand_union)

    n = NAME.format(pid)
    plan = lade_dxf(str(REPO / "Projekte" / "Rennweg" / f"{n}.dxf"))
    c = pickle.loads((REPO / "Projekte" / "_ergebnis_raumerkennung" / "Rennweg" / n
                      / "_cache.pkl").read_bytes())
    koerper = finde_wandkoerper(plan)
    erg = ab.erkenne_aussenbereiche(plan, koerper)          # echte Funktion
    offen_u = unary_union(erg.offen) if erg.offen else Polygon()
    c_off = unary_union([wkb.loads(g) for g in c["aussen_offen"]]) if c["aussen_offen"] else Polygon()
    wand_zu = ab._wand_geschlossen(koerper, ab._SCHLIESS_MM)
    komp_u = unary_union(erg.komponenten)
    rand = komp_u.convex_hull.exterior
    wu = wand_union(koerper)
    res = {"plan": pid, "n_koerper": len(koerper), "symdiff_cache_m2": round(offen_u.symmetric_difference(c_off).area / 1e6, 3),
           "komponenten_m2": [round(k.area / 1e6, 2) for k in erg.komponenten],
           "wand_zu_m2": round(wand_zu.area / 1e6, 2),
           "wand_zu_loecher_m2": sorted([round(Polygon(i).area / 1e6, 2) for p in getattr(wand_zu, "geoms", [wand_zu]) for i in p.interiors], reverse=True)[:8],
           "geschlossen_m2": [round(g.area / 1e6, 2) for g in erg.geschlossen], "teile": []}
    raeume = []
    for r in c["raeume"]:
        if len(r["polygon_mm"]) >= 3:
            p = Polygon(r["polygon_mm"]).buffer(0)
            raeume.append((r, p))
    room_u = unary_union([p for _, p in raeume])
    for t in erg.offen:
        pt, pr = nearest_points(t, rand)
        seg = LineString([pt, pr])
        e = {"m2": round(t.area / 1e6, 2), "d_rand_mm": round(t.distance(rand)),
             "ausserhalb_komponenten_m2": round(t.difference(komp_u).area / 1e6, 2),
             "nahpunkt": [round(pt.x), round(pt.y)],
             "nahlinie_len": round(seg.length), "nahlinie_in_rohwand_mm": round(seg.intersection(wu).length),
             "raeume": [(r["id"], r["typ"], round(p.intersection(t).area / 1e6, 2),
                         round(p.intersection(t).intersection(komp_u).area / 1e6, 2))
                        for r, p in raeume if p.intersection(t).area > 2e5],
             "stempel": [(s["name"], s["flaeche_m2"]) for s in c["stempel"] if t.covers(Point(s["xy"]))]}
        res["teile"].append(e)
    res["schnitt_offen_raeume_m2"] = round(offen_u.intersection(room_u).area / 1e6, 2)
    res["grund_none"] = ab.grundstuecksgrenze(plan, wand_zu) is None
    res["n_indizien"] = len(ab.aussen_indizien(plan))
    res["kante_none"] = ab._strassenkante(plan, rand) is None
    hull = komp_u.convex_hull
    res["freiflaechen"] = [(r["id"], r["typ"], round(p.area / 1e6, 2), round(p.intersection(hull).area / 1e6, 2),
                            round(p.intersection(offen_u).area / 1e6, 2), round(p.intersection(komp_u).area / 1e6, 2))
                           for r, p in raeume if r["typ"] in ("BALKON", "TERRASSE")]
    # Loch-Test-Gegenprobe: Teile, die nicht aus den Komponenten herausragen
    res["offen_ohne_loecher_m2"] = round(sum(t.area for t in erg.offen if t.difference(komp_u).area > 1e6) / 1e6, 2)

    # Oeffnungsbloecke neben der gefluteten Raumflaeche
    flut = offen_u.intersection(room_u).buffer(1000) if not offen_u.is_empty else Polygon()
    from ezdxf import bbox as ebbox
    bloecke = []

    def n_hatch(ins, tiefe=0):
        k = 0
        try:
            for v in ins.virtual_entities():
                if v.dxftype() == "HATCH":
                    k += 1
                elif v.dxftype() == "INSERT" and tiefe < 3:
                    k += n_hatch(v, tiefe + 1)
        except Exception:  # noqa: BLE001
            pass
        return k

    def walk(ents, pfad, tiefe):
        for en in ents:
            if en.dxftype() != "INSERT":
                continue
            name = str(en.dxf.name)
            if OEFF_RX.search(name) and not flut.is_empty:
                b = ebbox.extents([en])
                if b.has_data:
                    f = plan.factor
                    bb = box(b.extmin.x * f, b.extmin.y * f, b.extmax.x * f, b.extmax.y * f)
                    if bb.intersects(flut):
                        cx, cy = bb.centroid.x, bb.centroid.y
                        # Lueckenlaenge in der rohen Wand-Union entlang der Wandrichtung (nahester Koerper)
                        nk = min(koerper, key=lambda k: Polygon(k.polygon_mm).distance(Point(cx, cy)))
                        mrr = list(Polygon(nk.polygon_mm).minimum_rotated_rectangle.exterior.coords)
                        a, b2, c2 = mrr[0], mrr[1], mrr[2]
                        v = (b2[0] - a[0], b2[1] - a[1]) if math.dist(a, b2) >= math.dist(b2, c2) else (c2[0] - b2[0], c2[1] - b2[1])
                        ln = math.hypot(*v)
                        ux, uy = v[0] / ln, v[1] / ln
                        luecke = None
                        for off in (0.0,):
                            line = LineString([(cx - 8000 * ux, cy - 8000 * uy), (cx + 8000 * ux, cy + 8000 * uy)])
                            frei = line.difference(wu)
                            fs = [g for g in getattr(frei, "geoms", [frei]) if g.distance(Point(cx, cy)) < 50]
                            luecke = round(max(g.length for g in fs)) if fs else 0
                        bloecke.append({"pfad": "/".join(pfad + [name]), "layer": str(en.dxf.layer),
                                        "n_hatch": n_hatch(en), "bbox_wh": [round(bb.bounds[2] - bb.bounds[0]), round(bb.bounds[3] - bb.bounds[1])],
                                        "mitte": [round(cx), round(cy)], "freie_luecke_rohwand_mm": luecke,
                                        "in_offen": bb.intersects(offen_u)})
            if tiefe < 3 and not OEFF_RX.search(name):
                try:
                    walk(list(en.virtual_entities()), pfad + [name], tiefe + 1)
                except Exception:  # noqa: BLE001
                    pass

    walk(list(plan.space), [], 0)
    res["oeffnungsbloecke_an_flut"] = bloecke
    # Eintrittsstellen: Kreuzungen der offenen Teile mit dem Rand einer grob geschlossenen Gebaeudemaske
    maske = unary_union(ab._komponenten_aus(ab._wand_geschlossen(koerper, 5000.0)))
    for i, t in enumerate(erg.offen):
        kr = t.intersection(maske.boundary)
        segs = [g for g in getattr(kr, "geoms", [kr]) if g.length > 200]
        tt = res["teile"][i]
        tt["in_maske5000_m2"] = round(t.intersection(maske).area / 1e6, 2)
        tt["raeume_in_maske5000"] = [(r["id"], round(p.intersection(t).intersection(maske).area / 1e6, 2))
                                     for r, p in raeume if p.intersection(t).area > 2e5]
        tt["kreuzungen"] = []
        for g in sorted(segs, key=lambda g: -g.length)[:8]:
            m = g.centroid
            nb = sorted(bloecke, key=lambda b: Point(b["mitte"]).distance(m))[:2]
            tt["kreuzungen"].append({"len": round(g.length), "mitte": [round(m.x), round(m.y)],
                                     "naechste_bloecke": [(b["pfad"], b["n_hatch"], round(Point(b["mitte"]).distance(m))) for b in nb]})

    # Downstream: aussen_durchgaenge mit Tuer-Punkten aus tuer_oeffnungen, IST-kontur vs. kontur ohne offen
    oeff = im_planbereich(tuer_oeffnungen(plan), bounds_aus_wandkoerpern(koerper))
    tueren = [Tuer(id=f"o{i}", xy_mm=o.xy_mm) for i, o in enumerate(oeff)]
    rr = [Raum(id=r["id"], raum_typ=r["typ"], polygon_mm=r["polygon_mm"],
               nutzungsklasse=r["nutzungsklasse"]) for r, _ in raeume]
    for name, kontur in (("IST_gedeckt", erg.gedeckt()), ("nur_komponenten", unary_union([*erg.komponenten, *erg.geschlossen]))):
        ad = aussen_durchgaenge(rr, tueren, wu, kontur)
        res[f"aussen_durchgaenge_{name}"] = [
            {"raum": t.von_raum, "typ": next(r["typ"] for r, _ in raeume if r["id"] == t.von_raum),
             "xy": [round(t.xy_mm[0]), round(t.xy_mm[1])], "breite": t.breite_mm,
             "d_offen_mm": round(offen_u.distance(Point(t.xy_mm))) if not offen_u.is_empty else None,
             "in_komponenten": komp_u.covers(Point(t.xy_mm)),
             "d_komp_rand_mm": round(komp_u.boundary.distance(Point(t.xy_mm)))} for t in ad]
    (HIER / f"_pruef_{pid}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return res


if __name__ == "__main__":
    if sys.argv[1] == "synth":
        synth()
    else:
        for pid in sys.argv[1:]:
            r = main(pid)
            kurz = {k: v for k, v in r.items() if k not in ("oeffnungsbloecke_an_flut",)}
            print(json.dumps(kurz, ensure_ascii=False))
            print("BLOECKE", json.dumps(r["oeffnungsbloecke_an_flut"], ensure_ascii=False))
```

#### A.8.6 `K4-aussen/_aussen_folgen.py` (B.11, B.16)

```python
"""Diagnose K4-aussen (nur lesen): Oeffnungsbreiten, Gegenproben, Tuer-/Wohnungs-Blast-Radius.

Aufruf: PY _aussen_folgen.py <PLAN> -> _folgen_<PLAN>.json im Skriptordner

1) verschachtelte Fenster-/Tuer-INSERTs (Name ~ FENSTER|WINDOW|TUER|DOOR|OPENING), die eine
   offene Flaeche schneiden: MRR (Breite/Tiefe), Hatch-Anzahl, freie Luecke in wand_union
2) CF_A  Loch-Test: 'beruehrt_rand' := Teil ragt aus den gefuellten Komponenten heraus (> 1 m2)
   CF_B  Oeffnungsbloecke (MRR) als zusaetzliche Wandkoerper, sonst Code unveraendert
   CF_AB beides
3) Tuerkette in provider-Reihenfolge (Z.83-149) mit Einzelfunktionen, Raeume aus dem Cache
   (Endmodell, ohne Nutzungsklasse/Wohnung), Fluchtweg-Enden leer: IST vs CF_AB,
   plus Abgleich der IST-Simulation mit Nutzungsklasse/wohnung_id des Output-Caches.
"""
from __future__ import annotations

import copy
import json
import math
import pickle
import re
import sys
from pathlib import Path

import ezdxf.path
from shapely.geometry import LineString, MultiPoint, Point, Polygon
from shapely.ops import unary_union

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung import aussenbereich as ab
from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.tuer_typisierung import (
    brandschutz_hinweise_aus_dxf,
    typisiere_tueren,
)
from notbeleuchtung.raumerkennung.tuer_zuordnung import (
    AUSSEN,
    aussen_durchgaenge,
    durchgaenge_ohne_tuerblatt,
    ordne_tueren,
)
from notbeleuchtung.raumerkennung.tueren import (
    aussentor_tueren,
    im_planbereich,
    text_tueren,
    tuer_oeffnungen,
    tuer_texte,
    tueren_aus_dxf,
    verschmelze_doppelfluegel,
)
from notbeleuchtung.raumerkennung.waende import wand_segmente
from notbeleuchtung.raumerkennung.wandkoerper import (
    Wandkoerper,
    bounds_aus_wandkoerpern,
    finde_wandkoerper,
    wand_union,
)
from notbeleuchtung.raumerkennung.wohnungen import bilde_wohnungen

REPO = Path(r"D:\KI Projekt\Notbeleuchtung")
NAME = "{} - Rennweg 15_1030 Wien_Ausfürung-2026-06-12"
HIER = Path(__file__).parent
OEFF_RX = re.compile(r"FENSTER|WINDOW|T(?:Ü|UE)R|DOOR|OPENING", re.IGNORECASE)


def _poly(pts):
    if len(pts) < 3:
        return None
    p = Polygon(pts)
    return p if p.is_valid else p.buffer(0)


def _teile(g):
    if g.is_empty:
        return []
    return [x for x in getattr(g, "geoms", [g]) if x.geom_type == "Polygon"]


def _klassifiziere(plan, koerper, loch_test: bool):
    """Kopie von erkenne_aussenbereiche Z.234-271, nur der Rand-Test umschaltbar."""
    wand_zu = ab._wand_geschlossen(koerper, ab._SCHLIESS_MM)
    komp = ab._komponenten_aus(wand_zu)
    if not komp:
        return ab.AussenBereiche()
    grund = ab.grundstuecksgrenze(plan, wand_zu)
    bezug = grund if grund is not None else unary_union(komp).convex_hull
    frei = bezug.difference(wand_zu)
    indizien = ab.aussen_indizien(plan)
    rand = bezug.exterior
    kante = ab._strassenkante(plan, rand)
    if kante is None:
        kante = rand
    komp_u = unary_union(komp)
    offen, geschl = [], []
    for t in _teile(frei):
        if t.area < ab._MIN_HOF_M2 * 1e6:
            continue
        hat_indiz = any(t.covers(Point(p)) for p in indizien)
        if loch_test:
            beruehrt = t.difference(komp_u).area > 1e6
        else:
            beruehrt = t.distance(rand) < ab._RAND_EPS_MM
        if not (hat_indiz or beruehrt):
            continue
        hals = t.buffer(-ab._HALS_MM).buffer(ab._HALS_MM + 20.0)
        weg = (not hals.is_empty and not kante.is_empty
               and hals.distance(kante) < ab._RAND_EPS_MM)
        (offen if weg else geschl).append(t)
    return ab.AussenBereiche(komponenten=komp, offen=offen, geschlossen=geschl)


def _oeffnungs_bloecke(plan):
    out = []

    def walk(ents, tiefe):
        for e in ents:
            if e.dxftype() != "INSERT":
                continue
            name = str(e.dxf.name)
            if tiefe > 0 and OEFF_RX.search(name):
                pts = []
                n_hatch = 0
                try:
                    for x in e.virtual_entities():
                        if x.dxftype() == "HATCH":
                            n_hatch += 1
                            continue
                        try:
                            pts += [(v.x * plan.factor, v.y * plan.factor)
                                    for v in ezdxf.path.make_path(x).flattening(50)]
                        except Exception:  # noqa: BLE001
                            pass
                except Exception:  # noqa: BLE001
                    pass
                if len(pts) >= 3:
                    mrr = MultiPoint(pts).minimum_rotated_rectangle
                    if mrr.geom_type == "Polygon":
                        out.append({"name": name, "layer": str(e.dxf.layer), "n_hatch": n_hatch,
                                    "mrr": mrr})
                continue
            if tiefe < 3:
                try:
                    walk(e.virtual_entities(), tiefe + 1)
                except Exception:  # noqa: BLE001
                    pass

    walk(plan.space, 0)
    return out


def _seiten(mrr):
    c = list(mrr.exterior.coords)
    a, b = math.dist(c[0], c[1]), math.dist(c[1], c[2])
    if a >= b:
        return a, b, (c[0], c[1])
    return b, a, (c[1], c[2])


def _freie_luecke(mrr, wu):
    lang, _, (p, q) = _seiten(mrr)
    ux, uy = (q[0] - p[0]) / lang, (q[1] - p[1]) / lang
    cx, cy = mrr.centroid.x, mrr.centroid.y
    linie = LineString([(cx - 5000 * ux, cy - 5000 * uy), (cx + 5000 * ux, cy + 5000 * uy)])
    frei = linie.difference(wu)
    for g in getattr(frei, "geoms", [frei]):
        if g.distance(Point(cx, cy)) < 1.0:
            return round(g.length)
    return 0


def _flaechen(erg, rpolys):
    u = unary_union(erg.offen) if erg.offen else Polygon()
    je = {i: round(p.intersection(u).area / 1e6, 2) for i, _, p in rpolys
          if not u.is_empty and p.intersection(u).area > 2e5}
    return {"offen_m2": round(u.area / 1e6, 2), "n_offen": len(erg.offen),
            "geschlossen_m2": round(sum(g.area for g in erg.geschlossen) / 1e6, 2),
            "schnitt_raeume_m2": round(sum(je.values()), 2), "je_raum": je}


def _tueren_lauf(plan, koerper, raeume, aussen, geschoss):
    """provider.py Z.83-149 mit Einzelfunktionen (ohne Zirkulation: Fluchtweg-Enden leer)."""
    kontur = aussen.gedeckt() if aussen.komponenten else None
    bounds = bounds_aus_wandkoerpern(koerper)
    oeff = im_planbereich(tuer_oeffnungen(plan), bounds)
    tueren = tueren_aus_dxf(plan)
    quelle = "tueren_aus_dxf"
    if not tueren:
        quelle = "tuer_oeffnungen"
        tueren = [Tuer(id=f"tuer_{i}", xy_mm=o.xy_mm, breite_mm=o.breite_mm,
                       breite_quelle=o.breite_quelle,
                       breite_grund=(None if o.breite_mm is not None
                                     else "Tueroeffnung ohne messbare Breite"),
                       ist_notausgang=False, quelle=o.quelle)
                  for i, o in enumerate(oeff, start=1)]
    tueren = im_planbereich(tueren, bounds)
    tueren += aussentor_tueren(oeff, tueren, kontur)
    tueren = verschmelze_doppelfluegel(tueren, wand_segmente(plan))
    tueren += text_tueren(plan, tueren)
    ordne_tueren(tueren, oeff, raeume, kontur)
    tueren = [t for t in tueren if not (t.von_raum == t.nach_raum == AUSSEN)]
    for i, t in enumerate(tueren, start=1):
        t.id = f"tuer_{i}"
    wu = wand_union(koerper)
    tueren = tueren + durchgaenge_ohne_tuerblatt(raeume, tueren, wu)
    tueren = tueren + aussen_durchgaenge(raeume, tueren, wu, kontur)
    kein_weg = unary_union(aussen.geschlossen) if aussen.geschlossen else None
    typisiere_tueren(tueren, raeume, geschoss, brandschutz_hinweise_aus_dxf(plan), [],
                     tuer_texte(plan), kein_weg)
    wohnungen = bilde_wohnungen(raeume, tueren)
    by = {r.id: r.raum_typ for r in raeume}
    aus = [{"id": t.id, "xy": [round(t.xy_mm[0]), round(t.xy_mm[1])], "quelle": t.quelle,
            "typen": [by.get(t.von_raum, t.von_raum), by.get(t.nach_raum, t.nach_raum)],
            "seiten": [t.von_raum, t.nach_raum], "detail": t.tuer_detail,
            "notausgang": t.ist_notausgang, "breite": t.breite_mm}
           for t in tueren if AUSSEN in (t.von_raum, t.nach_raum)]
    return {"tuer_quelle": quelle, "n_tueren": len(tueren), "n_aussen": len(aus),
            "n_aussenoeffnung": sum(1 for t in tueren if t.quelle == "oeffnung_aussenwand"),
            "aussen_tueren": aus,
            "klassen_erschliessung": {r.id: f"{r.raum_typ}:{r.nutzungsklasse}" for r in raeume
                                      if r.raum_typ in ("GANG", "VORRAUM", "STIEGENHAUS")},
            "wohnungen": {w.id: w.raum_ids for w in wohnungen}}


def main(plan_id: str) -> None:
    n = NAME.format(plan_id)
    cache = pickle.loads((REPO / "Projekte" / "_ergebnis_raumerkennung" / "Rennweg" / n
                          / "_cache.pkl").read_bytes())
    plan = lade_dxf(str(REPO / "Projekte" / "Rennweg" / f"{n}.dxf"))
    koerper = finde_wandkoerper(plan)
    wu = wand_union(koerper)
    rpolys = [(r["id"], r["typ"], _poly(r["polygon_mm"])) for r in cache["raeume"]]
    rpolys = [(i, t, p) for i, t, p in rpolys if p is not None and not p.is_empty]

    ist = ab.erkenne_aussenbereiche(plan, koerper)
    offen_u = unary_union(ist.offen) if ist.offen else Polygon()
    bl = _oeffnungs_bloecke(plan)
    res = {"plan": plan_id, "geschoss": cache["geschoss"], "n_oeffnungsbloecke": len(bl),
           "bloecke_an_offen": []}
    for b in bl:
        if offen_u.is_empty or not b["mrr"].intersects(offen_u):
            continue
        lang, tief, _ = _seiten(b["mrr"])
        res["bloecke_an_offen"].append({
            "name": b["name"], "layer": b["layer"], "n_hatch": b["n_hatch"],
            "mrr_lang_mm": round(lang), "mrr_tief_mm": round(tief),
            "mitte": [round(b["mrr"].centroid.x), round(b["mrr"].centroid.y)],
            "freie_luecke_wand_union_mm": _freie_luecke(b["mrr"], wu)})

    extra = [Wandkoerper(polygon_mm=list(b["mrr"].exterior.coords), material="OEFFNUNG",
                         layer=b["layer"], quelle="cf:" + b["name"], breite_mm=_seiten(b["mrr"])[1])
             for b in bl]
    cf_a = _klassifiziere(plan, koerper, loch_test=True)
    cf_b = ab.erkenne_aussenbereiche(plan, koerper + extra)
    cf_ab = _klassifiziere(plan, koerper + extra, loch_test=True)
    res["IST"] = _flaechen(ist, rpolys)
    res["CF_A_lochtest"] = _flaechen(cf_a, rpolys)
    res["CF_B_oeffnungsbarriere"] = _flaechen(cf_b, rpolys)
    res["CF_AB"] = _flaechen(cf_ab, rpolys)

    def raeume_neu():
        return [Raum(id=r["id"], raum_typ=r["typ"],
                     polygon_mm=[tuple(p) for p in r["polygon_mm"]], flaeche_m2=r["flaeche_m2"])
                for r in cache["raeume"] if len(r["polygon_mm"]) >= 3]

    sim_ist_raeume = raeume_neu()
    res["tueren_IST"] = _tueren_lauf(plan, koerper, sim_ist_raeume, ist, cache["geschoss"])
    by_sim = {r.id: r for r in sim_ist_raeume}
    abw = []
    for r in cache["raeume"]:
        s = by_sim.get(r["id"])
        if s is None:
            continue
        if (s.nutzungsklasse, s.wohnung_id) != (r["nutzungsklasse"], r["wohnung_id"]):
            abw.append({"id": r["id"], "typ": r["typ"],
                        "cache": [r["nutzungsklasse"], r["wohnung_id"]],
                        "sim": [s.nutzungsklasse, s.wohnung_id]})
    res["abgleich_sim_ist_vs_cache"] = {"n_abweichungen": len(abw), "abweichungen": abw}
    res["tueren_CF_AB"] = _tueren_lauf(plan, koerper, raeume_neu(), cf_ab, cache["geschoss"])

    # CF_WA: NUR Fensterbloecke (Name/Layer ~ FENSTER|WINDOW) als Barriere + Loch-Test
    fenster_rx = re.compile(r"FENSTER|WINDOW", re.IGNORECASE)
    extra_w = [x for x, b in zip(extra, bl) if fenster_rx.search(b["name"] + " " + b["layer"])]
    res["n_fensterbloecke"] = len(extra_w)
    cf_wa = _klassifiziere(plan, koerper + extra_w, loch_test=True)
    res["CF_WA_fenster_plus_loch"] = _flaechen(cf_wa, rpolys)
    res["tueren_CF_WA"] = _tueren_lauf(plan, koerper, raeume_neu(), cf_wa, cache["geschoss"])

    def _schluessel(d):
        return {(round(t["xy"][0] / 50), round(t["xy"][1] / 50), t["detail"], tuple(t["typen"]))
                for t in d["aussen_tueren"]}

    ist_k = _schluessel(res["tueren_IST"])
    for name in ("tueren_CF_AB", "tueren_CF_WA"):
        k = _schluessel(res[name])
        res[f"diff_{name}"] = {"nur_IST": sorted(map(str, ist_k - k)),
                               "nur_CF": sorted(map(str, k - ist_k))}
    komp_ist = unary_union(ist.komponenten) if ist.komponenten else Polygon()
    komp_ab = unary_union(cf_ab.komponenten) if cf_ab.komponenten else Polygon()
    komp_wa = unary_union(cf_wa.komponenten) if cf_wa.komponenten else Polygon()
    res["komponenten_m2"] = {"IST": round(komp_ist.area / 1e6, 2),
                             "CF_AB": round(komp_ab.area / 1e6, 2),
                             "CF_WA": round(komp_wa.area / 1e6, 2)}
    for t in res["tueren_IST"]["aussen_tueren"]:
        p = Point(t["xy"])
        t["in_komp"] = {"IST": komp_ist.covers(p), "CF_AB": komp_ab.covers(p),
                        "CF_WA": komp_wa.covers(p),
                        "d_rand_IST": round(komp_ist.boundary.distance(p)),
                        "d_rand_CF_AB": round(komp_ab.boundary.distance(p)),
                        "d_rand_CF_WA": round(komp_wa.boundary.distance(p))}

    # CF_C: Fachregel-Veto (S-C) - Raeume mit zugeordnetem Stempel ODER typisiert, ausser
    # BALKON/TERRASSE, sind nie AUSSEN: aus offen ausschneiden und zur gedeckten Flaeche nehmen.
    # Vereinfachung: Resteile >= 5 m2 behalten ihren offen-Status (kein neuer Hals-Test).
    stempel_raeume = {s["raum_id"] for s in cache["stempel"] if s["raum_id"]}
    veto_polys = [p for i, t, p in rpolys
                  if t not in ("BALKON", "TERRASSE") and (t or i in stempel_raeume)]
    veto = unary_union(veto_polys) if veto_polys else Polygon()

    def _veto(erg):
        neu = []
        for t in erg.offen:
            neu += [g for g in _teile(t.difference(veto)) if g.area >= ab._MIN_HOF_M2 * 1e6]
        return ab.AussenBereiche(komponenten=list(erg.komponenten) + _teile(veto),
                                 offen=neu, geschlossen=list(erg.geschlossen))

    cf_c = _veto(ist)
    cf_ac = _veto(cf_a)
    res["n_veto_raeume"] = len(veto_polys)
    res["CF_C_veto"] = _flaechen(cf_c, rpolys)
    res["CF_AC_loch_plus_veto"] = _flaechen(cf_ac, rpolys)
    res["tueren_CF_C"] = _tueren_lauf(plan, koerper, raeume_neu(), cf_c, cache["geschoss"])
    res["tueren_CF_AC"] = _tueren_lauf(plan, koerper, raeume_neu(), cf_ac, cache["geschoss"])
    for name in ("tueren_CF_C", "tueren_CF_AC"):
        k = _schluessel(res[name])
        res[f"diff_{name}"] = {"nur_IST": sorted(map(str, ist_k - k)),
                               "nur_CF": sorted(map(str, k - ist_k))}
    out = json.dumps(res, ensure_ascii=False, indent=1)
    (HIER / f"_folgen_{plan_id}.json").write_text(out, encoding="utf-8")
    out = json.dumps(res, ensure_ascii=False, indent=1)
    (HIER / f"_folgen_{plan_id}.json").write_text(out, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
```

#### A.8.7 `K2a-pruefung-allg/_k2a_durchgang.py` (B.12)

```python
"""Gegenpruefung K2a (nur lesen, in-memory Simulation): wuerde ein ausgestanzter Schacht
(Nebenzelle mit Marker) in durchgaenge_ohne_tuerblatt einen Phantom-Durchgang erzeugen,
und liegen Marker-Zellen unter spaeter angehaengten stiegenhaus_*-Rechtecken?
Aufruf: python _k2a_durchgang.py <PLAN>"""
from __future__ import annotations

import pickle
import sys
from pathlib import Path

from shapely.geometry import Polygon
from shapely.ops import unary_union

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum
from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.tuer_zuordnung import durchgaenge_ohne_tuerblatt
from notbeleuchtung.raumerkennung.wandkoerper import finde_wandkoerper, wand_union

REPO = Path(r"D:\KI Projekt\Notbeleuchtung")
NAME = "{} - Rennweg 15_1030 Wien_Ausfürung-2026-06-12"
plan_id = sys.argv[1]
n = NAME.format(plan_id)
cache = pickle.loads((REPO / "Projekte/_ergebnis_raumerkennung/Rennweg" / n / "_cache.pkl").read_bytes())
plan = lade_dxf(REPO / "Projekte/Rennweg" / f"{n}.dxf")
f, doc = plan.factor, plan.doc


def eff(e, attr):
    v = e.dxf.get(attr, None)
    if v is None or v in (256, -1):
        lay = doc.layers.get(e.dxf.layer)
        return getattr(lay.dxf, attr, None) if lay is not None else None
    return v


def pg(pts):
    p = Polygon(pts)
    return p if p.is_valid else p.buffer(0)


rahmen = []
for e in plan.space:
    if e.dxftype() == "LWPOLYLINE" and e.closed and eff(e, "color") == 1 and eff(e, "lineweight") == 13:
        p = pg([(x * f, y * f) for x, y in e.get_points("xy")])
        if 0 < p.area <= 3e6:
            rahmen.append(p)
wk = finde_wandkoerper(plan)
wu = wand_union(wk)
M = unary_union(rahmen + [Polygon(k.polygon_mm).buffer(0) for k in wk if k.material == "SCHACHT"])

stiegen = [pg(r["polygon_mm"]) for r in cache["raeume"] if r["id"].startswith("stiegenhaus_")]
raeume_sim: list[Raum] = []
n_schacht = 0
unter_stiege = 0.0
for r in cache["raeume"]:
    if (r["typ"] or "") in ("SCHACHT", "LIFT") or len(r["polygon_mm"]) < 3 or r["id"].startswith("stiegenhaus_"):
        continue
    P = pg(r["polygon_mm"])
    frei = P.difference(wu)
    teile = sorted([g for g in getattr(frei, "geoms", [frei]) if g.area > 1e3], key=lambda g: -g.area)
    rest = P
    for g in teile[1:]:
        if g.area <= 3e6 and g.buffer(10).intersects(M):
            n_schacht += 1
            rest = rest.difference(g)
            unter_stiege += sum(g.intersection(s).area for s in stiegen)
            raeume_sim.append(Raum(id=f"schacht_{n_schacht}", raum_typ="SCHACHT",
                                   polygon_mm=[(float(x), float(y)) for x, y in g.exterior.coords[:-1]],
                                   flaeche_m2=g.area / 1e6))
    if rest.geom_type != "Polygon":
        rest = max(rest.geoms, key=lambda g: g.area)
    raeume_sim.append(Raum(id=r["id"], raum_typ=r["typ"] or "",
                           polygon_mm=[(float(x), float(y)) for x, y in rest.exterior.coords[:-1]],
                           flaeche_m2=rest.area / 1e6))
tp = [tuple(t["xy"]) for t in cache.get("tueren", []) if "xy" in t] if isinstance(cache.get("tueren"), list) else []
from notbeleuchtung.hauptengine.contracts.raum_modell import Tuer  # noqa: E402
tueren = [Tuer(id=f"t{i}", xy_mm=xy) for i, xy in enumerate(tp)]
dg = durchgaenge_ohne_tuerblatt(raeume_sim, tueren, wu)
mit_schacht = [(d.von_raum, d.nach_raum, d.breite_mm) for d in dg
               if d.von_raum.startswith("schacht_") or d.nach_raum.startswith("schacht_")]
print(f"[{plan_id}] simulierte Schaechte {n_schacht}; Tueren aus Cache {len(tueren)}; "
      f"Durchgaenge gesamt {len(dg)}; davon mit Schacht-Seite {len(mit_schacht)}: {mit_schacht}")
print(f"   Schnitt simulierter Schaechte mit spaeter angehaengten stiegenhaus_*-Rechtecken: {unter_stiege/1e6:.3f} m2")
print("   cache keys:", sorted(cache.keys()))
```

#### A.8.8 `K2a-pruefung-allg/_k2a_pruef.py` (B.14)

```python
"""Gegenpruefung K2a (nur lesen): Zonen minus Wand-Union -> Nebenzellen, Marker-Treffer,
rote Rahmen oben vs. in Bloecken, L-Identitaet. Aufruf: python _k2a_pruef.py <PLAN> [raum_id,...]"""
from __future__ import annotations

import pickle
import sys
from collections import Counter
from pathlib import Path

from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.raumlayer import raeume_aus_layer
from notbeleuchtung.raumerkennung.tueren import im_planbereich, tuer_oeffnungen
from notbeleuchtung.raumerkennung.wandkoerper import bounds_aus_wandkoerpern, finde_wandkoerper, wand_union

REPO = Path(r"D:\KI Projekt\Notbeleuchtung")
NAME = "{} - Rennweg 15_1030 Wien_Ausfürung-2026-06-12"
plan_id = sys.argv[1]
ziel = sys.argv[2].split(",") if len(sys.argv) > 2 else []
n = NAME.format(plan_id)
cache = pickle.loads((REPO / "Projekte/_ergebnis_raumerkennung/Rennweg" / n / "_cache.pkl").read_bytes())
plan = lade_dxf(REPO / "Projekte/Rennweg" / f"{n}.dxf")
f, doc = plan.factor, plan.doc


def eff(e, attr, layer_attr):
    v = e.dxf.get(attr, None)
    if v is None or v in (256, -1):
        lay = doc.layers.get(e.dxf.layer)
        return getattr(lay.dxf, layer_attr, None) if lay is not None else None
    return v


def pg(pts):
    p = Polygon(pts)
    return p if p.is_valid else p.buffer(0)


rahmen = []   # (poly, pfad, layer)


def walk(ents, pfad, tiefe):
    for e in ents:
        t = e.dxftype()
        if t == "LWPOLYLINE" and e.closed:
            if eff(e, "color", "color") == 1 and eff(e, "lineweight", "lineweight") == 13:
                p = pg([(x * f, y * f) for x, y in e.get_points("xy")])
                if 0 < p.area <= 3e6:
                    rahmen.append((p, pfad, str(e.dxf.layer)))
        elif t == "INSERT" and tiefe < 3:
            try:
                walk(e.virtual_entities(), pfad + [str(e.dxf.name)], tiefe + 1)
            except Exception:  # noqa: BLE001
                pass


walk(plan.space, [], 0)
print(f"[{plan_id}] rote geschl. LWPOLYLINE aci1 lw13 <=3m2: gesamt {len(rahmen)}; "
      f"top-level {sum(1 for _, p, _ in rahmen if not p)}; in Bloecken {sum(1 for _, p, _ in rahmen if p)}")
print("   Bloecke:", Counter(p[0].split('_')[0] if p else '-' for _, p, _ in rahmen))
print("   Layer:", Counter(l for _, _, l in rahmen))

wk = finde_wandkoerper(plan)
wu = wand_union(wk)
wk_s = [k for k in wk if k.material == "SCHACHT"]
print(f"   Wandkoerper {len(wk)}; material SCHACHT {len(wk_s)} Layer {Counter(k.layer for k in wk_s)}")
M_rahmen = unary_union([p for p, _, _ in rahmen])
M_rahmen_top = unary_union([p for p, pf, _ in rahmen if not pf])
M_keil = unary_union([Polygon(k.polygon_mm).buffer(0) for k in wk_s])
oeff = im_planbereich(tuer_oeffnungen(plan), bounds_aus_wandkoerpern(wk))

L = raeume_aus_layer(plan)
Lp = [Polygon(r.polygon_mm).buffer(0) for r in L]
print(f"   raeume_aus_layer: {len(L)}")
for rid in ziel:
    r = next(x for x in cache["raeume"] if x["id"] == rid)
    P = pg(r["polygon_mm"])
    sd = min(P.symmetric_difference(q).area for q in Lp) / 1e6
    print(f"   {rid} {r['typ']} {P.area/1e6:.3f} m2 | min. symm. Differenz zu L-Polygon {sd:.4f} m2")

for r in cache["raeume"]:
    if (r["typ"] or "") == "SCHACHT":
        P = pg(r["polygon_mm"])
        blk = [(pf[0], l, round(p.intersection(P).area / 1e6, 3)) for p, pf, l in rahmen if pf and p.intersects(P)]
        print(f"   SCHACHT-Raum {r['id']} {P.area/1e6:.3f} m2 bbox {[int(v) for v in P.bounds]} | Schnitt Rahmen top "
              f"{P.intersection(M_rahmen_top).area/1e6:.3f} / Rahmen in Bloecken {blk} / Keil {P.intersection(M_keil).area/1e6:.3f}")

stat = Counter()
zeilen = []
for r in cache["raeume"]:
    if (r["typ"] or "") in ("SCHACHT", "LIFT") or len(r["polygon_mm"]) < 3:
        continue
    P = pg(r["polygon_mm"])
    frei = P.difference(wu)
    teile = sorted([g for g in getattr(frei, "geoms", [frei]) if g.area > 1e3], key=lambda g: -g.area)
    for g in teile[1:]:
        if g.area > 3e6:
            continue
        bu = g.buffer(10)
        hr = bu.intersects(M_rahmen)
        hrt = bu.intersects(M_rahmen_top)
        hk = bu.intersects(M_keil)
        tn = sum(1 for t in oeff if g.distance(Point(t.xy_mm)) <= 600)
        stat["nebenzellen"] += 1
        stat["m2_nebenzellen"] += g.area / 1e6
        key = "marker" if (hr or hk) else "ohne_marker"
        stat[key] += 1
        stat["m2_" + key] += g.area / 1e6
        if hr and not hrt:
            stat["nur_block_rahmen"] += 1
        if hk and not hr:
            stat["nur_keil"] += 1
        if (hr or hk) and tn:
            stat["marker_aber_tuer<=600"] += 1
        zeilen.append((r["id"], r["typ"], round(g.area / 1e6, 3), int(g.centroid.x), int(g.centroid.y),
                       "R" if hr else "", "Rtop" if hrt else "", "K" if hk else "", tn))
print("   Nebenzellen (Zone minus Wand-Union, nicht groesste, <=3 m2, >0.001 m2):",
      {k: round(v, 3) if isinstance(v, float) else v for k, v in stat.items()})
for z in zeilen:
    print("     ", z)
```

### A.9 Nachbesserung R2 (`NB2-nachbesserung/_belege_r2.py`, `NB2-nachbesserung/_m5_zaehlung.py`; B.13, B.8)

Aufruf: `& $PY _belege_r2.py UG EG OG1 OG2 OG3 DG1 DG2` im Arbeitsordner; `& $PY <scratchpad>/NB2-nachbesserung/_m5_zaehlung.py` im Repo-Wurzelordner.

```python
"""Nachbesserung R2 - Belege U10 (R-Kontur gegen Gebaeudekomponente), U9 (Zone minus Wand),
DG1-3/U7 (Randabstand und Hals der offenen Teile). Nur lesen, in-memory.

Aufruf: PY _belege_r2.py UG EG OG1 OG2 OG3 DG1 DG2   -> stdout
In-memory nur: dxf_load.lade_dxf, wandkoerper.finde_wandkoerper / wand_union / aussenkontur,
aussenbereich._wand_geschlossen / _komponenten_aus / grundstuecksgrenze / aussen_indizien /
_strassenkante / erkenne_aussenbereiche (nur Abgleich).
Raumpolygone aus Projekte/_ergebnis_raumerkennung/Rennweg/<PLAN>/_cache.pkl (Output 511ad36).
"""
from __future__ import annotations

import gc
import json
import pickle
import sys
from pathlib import Path

from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

from notbeleuchtung.raumerkennung import aussenbereich as ab
from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.wandkoerper import aussenkontur, finde_wandkoerper, wand_union

REPO = Path(r"D:\KI Projekt\Notbeleuchtung")
NAME = "{} - Rennweg 15_1030 Wien_Ausfürung-2026-06-12"
ZONEN = {"DG2": ["raum_2", "raum_4", "raum_5"], "OG1": ["raum_3"], "DG1": ["raum_1"]}


def m2(g):
    return round(g.area / 1e6, 2)


def teile(g):
    if g is None or g.is_empty:
        return []
    return [x for x in getattr(g, "geoms", [g]) if x.geom_type == "Polygon" and not x.is_empty]


def main() -> None:
    for pid in sys.argv[1:]:
        n = NAME.format(pid)
        cache = pickle.loads((REPO / "Projekte" / "_ergebnis_raumerkennung" / "Rennweg" / n
                              / "_cache.pkl").read_bytes())
        plan = lade_dxf(str(REPO / "Projekte" / "Rennweg" / f"{n}.dxf"))
        wk = finde_wandkoerper(plan)
        wu = wand_union(wk)
        wz = ab._wand_geschlossen(wk, ab._SCHLIESS_MM)
        komp_u = unary_union(ab._komponenten_aus(wz))

        # U10: R-Kontur wie rest_komponenten.py:122 gegen Gebaeudekomponente der Aussenanalyse
        r_kontur = aussenkontur(wk, d_mm=1000.0)
        roh = unary_union([Polygon(k.polygon_mm) for k in wk])
        closing1000 = roh.buffer(1000.0).buffer(-1000.0)
        print("U10", json.dumps({
            "plan": pid, "wk_n": len(wk), "wand_union_m2": m2(wu),
            "r_kontur_d1000_m2": m2(r_kontur),
            "closing_d1000_teile_m2": sorted((m2(g) for g in teile(closing1000)), reverse=True)[:6],
            "komponenten_d1200_m2": m2(komp_u)}, ensure_ascii=False), flush=True)

        # U9: Zone (Cache-Polygon, Quelle L) minus rohe Wandunion bzw. minus geschlossene Wand
        by = {r["id"]: r for r in cache["raeume"]}
        for rid in ZONEN.get(pid, []):
            r = by[rid]
            z = Polygon(r["polygon_mm"]).buffer(0)
            minus_wz = teile(z.difference(wz))
            print("U9", json.dumps({
                "plan": pid, "raum": rid, "typ": r["typ"], "zone_m2": m2(z),
                "wand_in_zone_m2": m2(z.intersection(wu)),
                "zone_minus_wand_union_m2": m2(z.difference(wu)),
                "zone_minus_wand_zu_m2": m2(z.difference(wz)),
                "zone_minus_wand_zu_hauptteil_m2": m2(max(minus_wz, key=lambda g: g.area))
                if minus_wz else 0.0}, ensure_ascii=False), flush=True)

        # U7 / DG1-3: Kopie erkenne_aussenbereiche Z.240-271, je Kandidat Randabstand und Hals
        grund = ab.grundstuecksgrenze(plan, wz)
        bezug = grund if grund is not None else komp_u.convex_hull
        rand = bezug.exterior
        kante = ab._strassenkante(plan, rand)
        if kante is None:
            kante = rand
        indizien = ab.aussen_indizien(plan)
        zeilen = []
        for t in teile(bezug.difference(wz)):
            if t.area < ab._MIN_HOF_M2 * 1e6:
                continue
            indiz = any(t.covers(Point(p)) for p in indizien)
            d_rand = t.distance(rand)
            if not (indiz or d_rand < ab._RAND_EPS_MM):
                continue
            hals = t.buffer(-ab._HALS_MM).buffer(ab._HALS_MM + 20.0)
            d_hals = None if hals.is_empty or kante.is_empty else hals.distance(kante)
            zeilen.append({"m2": m2(t), "indiz": indiz, "d_rand_mm": round(d_rand),
                           "hals_d_kante_mm": None if d_hals is None else round(d_hals),
                           "offen": d_hals is not None and d_hals < ab._RAND_EPS_MM,
                           "loch_within": t.within(komp_u.buffer(1.0))})
        real = ab.erkenne_aussenbereiche(plan, wk)
        print("U7", json.dumps({
            "plan": pid, "grundstuecksgrenze": grund is not None, "n_indizien": len(indizien),
            "kandidaten": sorted(zeilen, key=lambda z: -z["m2"]),
            "offen_kopie_m2": sorted((z["m2"] for z in zeilen if z["offen"]), reverse=True),
            "offen_real_m2": sorted((m2(g) for g in real.offen), reverse=True)},
            ensure_ascii=False), flush=True)
        del plan, wk, wu, wz, real
        gc.collect()


if __name__ == "__main__":
    main()
```

```python
"""M5 - Wohnungseingaenge je Wohnung ueber alle Projekte/_ergebnis/*/kennzahlen.json (nur JSON lesen).

Aufruf (im Repo-Wurzelordner): PY <scratchpad>/NB2-nachbesserung/_m5_zaehlung.py   -> stdout
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

dateien = sorted(Path("Projekte/_ergebnis").glob("*/kennzahlen.json"))
ohne_tt, ohne_we, beide = [], [], []
for f in dateien:
    k = json.loads(f.read_text(encoding="utf-8"))
    if "tuer_typen" not in k:
        ohne_tt.append((f.parent.name, sorted(k), str(k.get("fehler", ""))[:60]))
    elif "wohnungseingang" not in k["tuer_typen"]:
        ohne_we.append(f.parent.name)
    else:
        beide.append((f.parent.name, k["tuer_typen"]["wohnungseingang"], k.get("wohnungen"), k.get("sha256")))

print("dateien", len(dateien), "ohne tuer_typen", len(ohne_tt), "tuer_typen ohne wohnungseingang", len(ohne_we),
      "mit beiden", len(beide), "ausgewertet (mit tuer_typen)", len(dateien) - len(ohne_tt))
for name, keys, fehler in ohne_tt:
    print("  STUB", name, keys, fehler)
print("wohnungen >= 1 in allen mit beiden:", all((w or 0) >= 1 for _, _, w, _ in beide))
treffer = [(n, we, w, s) for n, we, w, s in beide if w and we / w >= 3]
print("schwelle >= 3:", len(treffer), "distinct sha256:", len({s for *_, s in treffer}))
je_sha = defaultdict(list)
for n, _, _, s in treffer:
    je_sha[s].append(n)
for s, ns in je_sha.items():
    if len(ns) > 1:
        print("  dup", s[:10], ns)
print("summe WE", sum(we for _, we, _, _ in beide), "W", sum(w for _, _, w, _ in beide))
print("top5", sorted(((round(we / w, 1), n, we, w) for n, we, w, _ in treffer), reverse=True)[:5])
print("fehler-texte", Counter(f for *_, f in ohne_tt))
```

### A.10 Weitere Diagnose-Skripte (Nachtrag zur Vollständigkeitskritik)

#### A.10.1 `K1-stiegenhaus/_regel_messung.py` (U1 Hüllen-Deckung 0,85-0,99, U2 Spalte „außerhalb Lift + 400 mm“, echte Stiegenhäuser 13-19 m²)

```python
"""K1: Belastbarkeit allgemeiner Fix-Regeln ueber alle Plaene messen (nur in-memory, nur stdout).
Aufruf: PY _regel_messung.py UG EG OG1 OG2 OG3 DG1 DG2
"""
import gc
import json
import sys
from pathlib import Path

from shapely.geometry import LineString, MultiPoint, Point, Polygon
from shapely.ops import unary_union

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.geometrie_typ import _STAIR_BLOCK, typisiere_geometrisch
from notbeleuchtung.raumerkennung.kaskade import raeume_aus_kaskade
from notbeleuchtung.raumerkennung.lift_erkennung import finde_lifte
from notbeleuchtung.raumerkennung.stiegenhaus import _wcs_pts

REPO = Path(r"D:\KI Projekt\Notbeleuchtung")


def pg(r):
    return Polygon(r.polygon_mm).buffer(0)


for name in sys.argv[1:]:
    dxf = REPO / "Projekte" / "Rennweg" / f"{name} - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf"
    plan = lade_dxf(str(dxf))
    f = plan.factor
    print(f"===== {name}")
    stairs = []
    for e in plan.space:
        if e.dxftype() != "INSERT" or not _STAIR_BLOCK.search(e.dxf.name or ""):
            continue
        segs, pts = [], []
        for v in e.virtual_entities():
            p = _wcs_pts(v, f)
            if len(p) >= 2:
                pts += p
                segs += [LineString([a, b]) for a, b in zip(p, p[1:]) if a != b]
        attribs = len(getattr(e, "attribs", []))
        stairs.append((e.dxf.name, e.dxf.layer, attribs, segs, MultiPoint(pts).convex_hull if len(pts) >= 3 else None))
    k = raeume_aus_kaskade(plan)
    rooms = [r for r in k.alle_raeume if len(r.polygon_mm) >= 3]
    u_all = unary_union([pg(r) for r in rooms if pg(r).area >= 1e6])
    u_stgh = unary_union([pg(r) for r in rooms if r.raum_typ == "STIEGENHAUS"]) if any(r.raum_typ == "STIEGENHAUS" for r in rooms) else None
    for nm, layer, att, segs, hull in stairs:
        d = {"block": nm, "layer": layer, "attribs": att, "n_segs": len(segs)}
        if hull is not None and hull.area > 0:
            d["hull_m2"] = round(hull.area / 1e6, 2)
            d["hull_von_raeumen_gedeckt"] = round(hull.intersection(u_all).area / hull.area, 2)
            d["hull_von_STIEGENHAUS_gedeckt"] = round(hull.intersection(u_stgh).area / hull.area, 2) if u_stgh is not None else 0
        print("STAIR", json.dumps(d, ensure_ascii=False))
    # Stufenlinien je Raum (nur echte Treppenbloecke mit Segmenten)
    alle_segs = [s for nm, layer, att, segs, hull in stairs for s in segs]
    for r in rooms:
        if not (r.id.startswith("rest_") or r.raum_typ == "STIEGENHAUS"):
            continue
        innen = pg(r).buffer(-50)
        laenge = sum(s.intersection(innen).length for s in alle_segs) / 1000 if not innen.is_empty else 0.0
        print("STUFEN", r.id, r.raum_typ, round(pg(r).area / 1e6, 2), "stair_linien_m_im_raum", round(laenge, 1))
    vor = {r.id for r in rooms}
    raeume = typisiere_geometrisch(plan, list(k.alle_raeume))
    roh = {r.id: pg(r) for r in raeume if len(r.polygon_mm) >= 3}
    lifte = finde_lifte(plan, raeume)
    for r in raeume:
        if not any(b.regel == "LIFT_SCHACHT" for b in r.bereinigung):
            continue
        before = roh[r.id]
        for lf in lifte:
            lp = Polygon(lf.polygon_mm)
            if not before.intersects(lp):
                continue
            d = {"raum": r.id, "vorher_m2": round(before.area / 1e6, 2), "lift_m2": round(lp.area / 1e6, 2),
                 "anteil_lift": round(lp.area / before.area, 2)}
            for dd in (200, 400, 600):
                d[f"rest_ausserhalb_lift_buffer_{dd}_m2"] = round(before.difference(lp.buffer(dd, join_style=2)).area / 1e6, 2)
            print("LIFTRING", json.dumps(d))
    neu = [r for r in raeume if r.id not in vor and r.raum_typ == "STIEGENHAUS"]
    for r in neu:
        ov = [(o.id, o.raum_typ, round(pg(r).intersection(pg(o)).area / 1e6, 2)) for o in raeume
              if o is not r and len(o.polygon_mm) >= 3 and pg(r).intersection(pg(o)).area > 1e4]
        print("NEU_STIEGENHAUS", r.id, round(r.flaeche_m2, 2), "ueberlappt", ov)
    if name == "DG2":
        r2 = next(r for r in raeume if r.id == "rest_2")
        p2 = pg(r2)
        for e in plan.space:
            if e.dxftype() == "MTEXT" and "DBA" in e.plain_text().upper():
                xy = (e.dxf.insert[0] * f, e.dxf.insert[1] * f)
                print("DBA_TEXT", repr(e.plain_text()), [round(v) for v in xy], "in rest_2:", p2.covers(Point(xy)),
                      "abstand_mm", round(p2.distance(Point(xy))))
            if e.dxftype() == "LWPOLYLINE":
                col = e.dxf.get("color", 256)
                lay = plan.doc.layers.get(e.dxf.layer)
                aci = lay.color if col == 256 and lay is not None else col
                if aci != 1:
                    continue
                pts = plan.entity_points(e)
                if len(pts) < 3:
                    continue
                q = Polygon(pts).buffer(0)
                if q.is_empty or not q.intersects(p2):
                    continue
                iou = q.intersection(p2).area / q.union(p2).area
                print("ROTE_KONTUR", e.dxf.layer, "closed", e.closed, "m2", round(q.area / 1e6, 2), "IoU_rest_2", round(iou, 2))
    del plan, k, raeume, lifte, rooms
    gc.collect()
```

#### A.10.2 `K5-wohnungen/_tuerbloecke.py` (U12 Spalten „Türblöcke“ und „INSERT in eigener Bbox“)

```python
"""K5-wohnungen: (1) Wo gehen die ArchiCAD-Zargentuer-Bloecke verloren?
(2) Sind die breiten durchgang_*-Kanten Streifen entlang duenner Waende?
Nur lesen; Aufruf: python _tuerbloecke.py <PLAN>. Ausgabe: stdout + _tb_<PLAN>.json
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

import ezdxf.bbox
from shapely.geometry import Point, box

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.geometrie_typ import typisiere_geometrisch
from notbeleuchtung.raumerkennung.kaskade import raeume_aus_kaskade
from notbeleuchtung.raumerkennung.tuer_zuordnung import (
    _DURCHGANG_MIN_MM, _KONTAKT_MM, _raum_polys)
from notbeleuchtung.raumerkennung.tueren import (
    _ist_tuer_block, im_planbereich, tuer_oeffnungen)
from notbeleuchtung.raumerkennung.wandkoerper import (
    bounds_aus_wandkoerpern, wand_union)

REPO = Path(r"D:\KI Projekt\Notbeleuchtung")
NAME = "{} - Rennweg 15_1030 Wien_Ausfürung-2026-06-12"
OUT = Path(__file__).parent


def main(pn: str) -> None:
    dxf = REPO / "Projekte" / "Rennweg" / f"{NAME.format(pn)}.dxf"
    plan = lade_dxf(str(dxf))
    f = plan.factor
    res: dict = {"plan": pn}

    # (1) Tuer-Bloecke rekursiv, gleiche Tiefe wie tueren.tuer_oeffnungen._walk
    bl = []

    def walk(ents, tiefe, pfad):
        for e in ents:
            if e.dxftype() != "INSERT":
                continue
            name = str(e.dxf.name)
            if _ist_tuer_block(name):
                ins = plan._scale(e.dxf.insert)
                b = ezdxf.bbox.extents([e])
                bb = ([b.extmin.x * f, b.extmin.y * f, b.extmax.x * f, b.extmax.y * f]
                      if b.has_data else None)
                marker = None
                try:
                    for v in e.virtual_entities():
                        if v.dxftype() == "INSERT" and list(getattr(v, "attribs", [])):
                            marker = [a.dxf.text for a in v.attribs]
                            break
                except Exception:  # noqa: BLE001
                    pass
                bl.append({"name": name, "pfad": pfad, "tiefe": tiefe,
                           "insert": [round(ins[0]), round(ins[1])],
                           "bbox": [round(v) for v in bb] if bb else None,
                           "marker": marker})
            elif tiefe < 3:
                try:
                    walk(list(e.virtual_entities()), tiefe + 1, pfad + [name])
                except Exception:  # noqa: BLE001
                    pass

    walk(plan.space, 0, [])
    oeff_all = tuer_oeffnungen(plan)
    k = raeume_aus_kaskade(plan)
    wk = k.wandkoerper
    bounds = bounds_aus_wandkoerpern(wk)
    (x0, y0), (x1, y1) = bounds.min_xy, bounds.max_xy
    rand = 2000.0

    def drin(p):
        return x0 - rand <= p[0] <= x1 + rand and y0 - rand <= p[1] <= y1 + rand

    oeff_in = im_planbereich(oeff_all, bounds)
    res["bounds_wandkoerper"] = [round(x0), round(y0), round(x1), round(y1)]
    res["tuer_oeffnungen_alle"] = dict(Counter(o.quelle for o in oeff_all))
    res["tuer_oeffnungen_im_planbereich"] = dict(Counter(o.quelle for o in oeff_in))
    res["block_oeffnungen_xy_beispiele"] = [
        [round(o.xy_mm[0]), round(o.xy_mm[1])] for o in oeff_all if o.quelle == "block"][:5]
    res["n_tuerbloecke_walk"] = len(bl)
    res["tuerbloecke_insert_im_planbereich"] = sum(drin(b["insert"]) for b in bl)
    res["tuerbloecke_bbox_im_planbereich"] = sum(
        1 for b in bl if b["bbox"] and drin(((b["bbox"][0] + b["bbox"][2]) / 2,
                                             (b["bbox"][1] + b["bbox"][3]) / 2)))
    res["tuerblock_namen"] = dict(Counter(b["name"].split("[")[0].strip() for b in bl))
    res["tuerbloecke_beispiele"] = bl[:6]

    # (2) Durchgaenge wie tuer_zuordnung.durchgaenge_ohne_tuerblatt Z.133-160, instrumentiert
    raeume = typisiere_geometrisch(plan, k.alle_raeume)
    polys = _raum_polys(raeume)
    wu = wand_union(wk)
    tb_boxen = [box(*b["bbox"]) for b in bl if b["bbox"] and drin(
        ((b["bbox"][0] + b["bbox"][2]) / 2, (b["bbox"][1] + b["bbox"][3]) / 2))]
    zeilen = []
    for i, (ra, pa, _) in enumerate(polys):
        for rb, pb, _ in polys[i + 1:]:
            if pa.distance(pb) > 2 * _KONTAKT_MM:
                continue
            zone = pa.buffer(_KONTAKT_MM).intersection(pb.buffer(_KONTAKT_MM))
            frei = zone.difference(wu)
            if frei.is_empty:
                continue
            for g in (list(frei.geoms) if hasattr(frei, "geoms") else [frei]):
                mrr = g.minimum_rotated_rectangle
                co = list(getattr(mrr, "exterior", g).coords)[:4]
                if len(co) < 3:
                    continue
                s1, s2 = math.dist(co[0], co[1]), math.dist(co[1], co[2])
                lang, kurz = max(s1, s2), min(s1, s2)
                if lang < _DURCHGANG_MIN_MM:
                    continue
                c = g.centroid
                d_tb = min((bx.distance(Point(c.x, c.y)) for bx in tb_boxen), default=None)
                zeilen.append({"a": f"{ra.id}:{ra.raum_typ}", "b": f"{rb.id}:{rb.raum_typ}",
                               "xy": [round(c.x), round(c.y)], "lang": round(lang),
                               "kurz": round(kurz), "flaeche_m2": round(g.area / 1e6, 3),
                               "raumabstand": round(pa.distance(pb)),
                               "dist_tuerblock_bbox": None if d_tb is None else round(d_tb)})
    res["durchgang_teile_ge_800"] = zeilen
    res["n_teile"] = len(zeilen)
    res["n_teile_kurz_le_150"] = sum(1 for z in zeilen if z["kurz"] <= 150)
    res["n_teile_ohne_tuerblock_1000"] = sum(
        1 for z in zeilen if z["dist_tuerblock_bbox"] is None or z["dist_tuerblock_bbox"] > 1000)
    (OUT / f"_tb_{pn}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    kurz = {k2: v for k2, v in res.items() if k2 not in ("durchgang_teile_ge_800",)}
    print(json.dumps(kurz, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
```

#### A.10.3 `K4-aussen-gegen/_k4g_mess.py` (U6 Versiegelungstabelle, g = 1900 mm)

```python
"""K4-aussen Gegenpruefung - eigene in-memory Messung (nur lesen).

Aufruf: PY _k4g_mess.py synth DG1 OG1 DG2 OG3  -> _k4g_<arg>.json im Skriptordner
"""
import json
import math
import pickle
import sys
from pathlib import Path

from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum
from notbeleuchtung.raumerkennung import aussenbereich as ab
from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.tuer_zuordnung import aussen_durchgaenge
from notbeleuchtung.raumerkennung.wandkoerper import Wandkoerper, finde_wandkoerper, wand_union

REPO = Path(r"D:\KI Projekt\Notbeleuchtung")
NAME = "{} - Rennweg 15_1030 Wien_Ausfürung-2026-06-12"
HIER = Path(__file__).parent


def _wk(x0, y0, x1, y1):
    return Wandkoerper(polygon_mm=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                       material="STAHLBETON", layer="w", quelle="msp", breite_mm=float(y1 - y0))


def synth():
    out = []
    for t in (200, 400, 600):
        for g in (800, 1000, 1300, 1600, 1900, 2400):
            k = [_wk(-8000, 0, -g / 2, t), _wk(g / 2, 0, 8000, t)]
            zu = ab._wand_geschlossen(k, ab._SCHLIESS_MM)
            rest = zu.intersection(LineString([(0, -3000), (0, t + 3000)])).length
            grenze = 2 * (1200 - math.sqrt(max(1200 ** 2 - (g / 2) ** 2, 0)))
            out.append({"t": t, "g": g, "rest_mm": round(rest),
                        "versiegelt": rest > 0, "formel_t_min": round(grenze)})
    return out


def _teile(g):
    if g is None or g.is_empty:
        return []
    return [x for x in getattr(g, "geoms", [g]) if x.geom_type == "Polygon"]


def _ring_oeffnungen(raeume, wu, ring):
    """Emulation aussen_durchgaenge Z.189-223 OHNE Tuer-Naehe-Filter."""
    out = []
    for rid, typ, kl, p in raeume:
        if not (kl or "").startswith("ALLGEMEIN"):
            continue
        frei = p.buffer(400).intersection(ring).difference(wu)
        for g in _teile(frei):
            c = list(g.minimum_rotated_rectangle.exterior.coords)[:4]
            b = max(math.dist(c[0], c[1]), math.dist(c[1], c[2]))
            if 800 < b <= 2600:
                out.append({"raum": rid, "typ": typ, "breite": round(b),
                            "xy": [round(g.centroid.x), round(g.centroid.y)]})
    return out


def plan_mess(pid):
    n = NAME.format(pid)
    cache = pickle.loads((REPO / "Projekte" / "_ergebnis_raumerkennung" / "Rennweg" / n
                          / "_cache.pkl").read_bytes())
    plan = lade_dxf(str(REPO / "Projekte" / "Rennweg" / f"{n}.dxf"))
    koerper = finde_wandkoerper(plan)
    aus = ab.erkenne_aussenbereiche(plan, koerper)
    wand_zu = ab._wand_geschlossen(koerper, ab._SCHLIESS_MM)
    grund = ab.grundstuecksgrenze(plan, wand_zu)
    komp_u = unary_union(aus.komponenten)
    bezug = grund if grund is not None else komp_u.convex_hull
    rand = bezug.exterior
    maske = unary_union(ab._komponenten_aus(ab._wand_geschlossen(koerper, 5000.0)))
    wu = wand_union(koerper)
    raeume = []
    for r in cache["raeume"]:
        if len(r["polygon_mm"]) >= 3:
            p = Polygon(r["polygon_mm"]).buffer(0)
            if not p.is_empty:
                raeume.append((r["id"], r["typ"], r["nutzungsklasse"], p))
    res = {"plan": pid, "grenze": grund is not None, "n_koerper": len(koerper),
           "offen_m2": round(sum(t.area for t in aus.offen) / 1e6, 2), "teile": []}
    # alle freien Teile >= 5 m2 mit Status
    for t in _teile(bezug.difference(wand_zu)):
        if t.area < 5e6:
            continue
        status = ("offen" if any(t.equals_exact(o, 1.0) or t.equals(o) for o in aus.offen)
                  else "geschlossen" if any(t.equals(o) for o in aus.geschlossen) else "innen")
        e = {"status": status, "m2": round(t.area / 1e6, 2), "d_rand": round(t.distance(rand)),
             "ausserhalb_komp_m2": round(t.difference(komp_u).area / 1e6, 2),
             "ausserhalb_maske5000_m2": round(t.difference(maske).area / 1e6, 2), "raeume": {}}
        for rid, typ, kl, p in raeume:
            s = p.intersection(t)
            if s.area > 0.3e6:
                e["raeume"][rid] = [typ, round(s.area / 1e6, 2),
                                    round(s.difference(maske).area / 1e6, 2)]
        if status != "innen" or any(v[0] in ("BALKON", "TERRASSE") for v in e["raeume"].values()):
            res["teile"].append(e)
    # Veto-Ueberstand: Raumflaeche (ausser BALKON/TERRASSE) in offen, die AUSSERHALB der 5000er-Maske liegt
    offen_u = unary_union(aus.offen) if aus.offen else Polygon()
    res["veto_ausserhalb_maske_m2"] = {
        rid: [typ, round(p.intersection(offen_u).difference(maske).area / 1e6, 2)]
        for rid, typ, kl, p in raeume
        if typ not in ("BALKON", "TERRASSE") and p.intersection(offen_u).difference(maske).area > 0.3e6}
    # Aussenring-Varianten (Befund 5)
    kontur = aus.gedeckt()
    ring = kontur.buffer(2000.0).difference(kontur).buffer(400.0)
    ring_def = ring.difference(komp_u.buffer(-400.0))
    offen_loch = [t for t in aus.offen if t.difference(komp_u).area > 1e6]
    kontur_loch = unary_union([*aus.komponenten, *aus.geschlossen])
    if offen_loch:
        kontur_loch = kontur_loch.difference(unary_union(offen_loch))
    ring_loch = kontur_loch.buffer(2000.0).difference(kontur_loch).buffer(400.0)
    res["ring_IST_emul"] = _ring_oeffnungen(raeume, wu, ring)
    res["ring_defensiv_emul"] = _ring_oeffnungen(raeume, wu, ring_def)
    res["ring_lochtest_emul"] = _ring_oeffnungen(raeume, wu, ring_loch)
    rm = [Raum(id=rid, raum_typ=typ, polygon_mm=list(p.exterior.coords)[:-1], nutzungsklasse=kl)
          for rid, typ, kl, p in raeume]
    res["aussen_durchgaenge_real_IST_ohne_tueren"] = [
        {"raum": t.von_raum, "breite": t.breite_mm, "xy": [round(t.xy_mm[0]), round(t.xy_mm[1])]}
        for t in aussen_durchgaenge(rm, [], wu, kontur)]
    return res


def main():
    for arg in sys.argv[1:]:
        res = synth() if arg == "synth" else plan_mess(arg)
        (HIER / f"_k4g_{arg}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                               encoding="utf-8")
        print(arg, json.dumps(res, ensure_ascii=False)[:3000])


if __name__ == "__main__":
    main()
```

## Anhang B: Diagnoseaufrufe

Rahmen für alle Aufrufe: `PY` = `D:/KI Projekt/Notbeleuchtung/.venv/Scripts/python.exe`. Die Hilfsskripte liegen außerhalb des Repos, jeweils im eigenen Arbeitsordner, und werden aus diesem Ordner gestartet (`& $PY <skript> <argumente>`). Eingaben sind nur `Projekte/Rennweg/<PLAN> - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf` und `Projekte/_ergebnis_raumerkennung/Rennweg/<PLAN> - …/_cache.pkl` (Output 511ad36). Code-Stand: HEAD 2f610cc (src identisch mit 511ad36). Es läuft ein Python-Prozess zur Zeit, keine Datei im Repo wird geschrieben. Kernausgaben sind wörtlich gekürzt (Zahlen unverändert).

### B.1 Loch-Test S1 und F7-Basis (`_s12_nachrechnung.py`, Nachbesserung R1)

- Funktionen: `dxf_load.lade_dxf`, `wandkoerper.finde_wandkoerper`, `aussenbereich._wand_geschlossen(koerper, 1200)`, `_komponenten_aus`, `grundstuecksgrenze`, `aussen_indizien`, `_strassenkante`; zum Abgleich `erkenne_aussenbereiche`.
- Logik: Kopie von `erkenne_aussenbereiche` Z.234-271, aber je freiem Teil drei Rand-Prädikate. **heute:** `t.distance(rand) < 250`. **S1** (Pseudocode U7): `not t.within(komp_u.buffer(1.0)) and t.distance(rand) < 250`. **K4-Variante:** `t.difference(komp_u).area > 1e6`. Offen, wenn (Indiz oder Prädikat) und Hals an der Kante. Zählung M2 mit importiertem M2-`_messen.py` (`INNEN_TYPEN`, Stempel aus Cache, Möbel/Sanitär per Einfügepunkt, Schnitt > 0,05 m²).
- Abgleich: Kopie „heute“ = `erkenne_aussenbereiche` = Cache in allen Plänen (symmetrische Differenz 0,0 m²; EG ohne offen).
- Befehl: `& $PY _s12_nachrechnung.py UG EG OG1 OG2 OG3 DG1 DG2` (Quelltext: Anhang A.5; importiert M2-`_messen.py` aus Anhang A.2)
- Kernausgabe (offen m², M2 `wert`):
```text
UG  IST (23.19, 0)   S1_within (23.19, 0)  S1_diff (23.19, 0)  f7 []
EG  IST (0.0, 0)     S1_within (0.0, 0)    S1_diff (0.0, 0)    f7 []
OG1 IST (64.13, 3)   S1_within (64.13, 3)  S1_diff (64.13, 3)  f7 []
OG2 IST (51.47, 2)   S1_within (51.47, 2)  S1_diff (51.47, 2)  f7 []
OG3 IST (114.03, 4)  S1_within (35.66, 2)  S1_diff (35.66, 2)
    f7 [{m2 37.13, indiz False, d_rand_mm 193, loch_within True}, {m2 41.25, indiz False, d_rand_mm 193, loch_within True}]
DG1 IST (143.83, 7)  S1_within (40.07, 4)  S1_diff (40.07, 4)
    f7 [{m2 103.76, indiz False, d_rand_mm 193, loch_within True}]
DG2 IST (45.36, 4)   S1_within (45.36, 4)  S1_diff (45.36, 4)  f7 []
S1_within innen: DG1 raum_3 15.05, raum_2 12.63, raum_10 5.55, raum_6 4.05 | OG3 raum_4 18.12, raum_3 15.55
alle 7 Pläne: grundstuecksgrenze False, n_indizien 0
```
- Frühere Messung derselben Größe: Cluster K4 `_aussen_folgen.py <PLAN>` (`_klassifiziere(plan, koerper, loch_test=True)`) → `offen_m2` DG1 40.07, OG3 35.66; Gegenprüfung `_pruef.py <PLAN>` → `offen_ohne_loecher_m2` 40.07 / 35.66.

### B.2 S2 Veto mit Zuschnitt (gleicher Aufruf wie B.1)

- Logik: `zonen` = Union der Cache-Räume mit Typ in M2 `INNEN_TYPEN`; `maske` = Union `_komponenten_aus(_wand_geschlossen(koerper, 5000))`; offen_S2 = offen_S1 − (zonen ∩ maske); Variante ohne Zuschnitt: offen_S1 − zonen.
- Kernausgabe (offen m², `wert`; innen = [id, typ, Schnitt m², davon außerhalb Maske m²]):
```text
UG  S1_S2_zuschnitt (23.19, 0)  S1_S2_ohne_zuschnitt (23.19, 0)
EG  S1_S2_zuschnitt (0.0, 0)    S1_S2_ohne_zuschnitt (0.0, 0)
OG1 S1_S2_zuschnitt (25.19, 0)  S1_S2_ohne_zuschnitt (25.19, 0)  frei [raum_15 BALKON 7.5]
OG2 S1_S2_zuschnitt (30.08, 0)  S1_S2_ohne_zuschnitt (30.08, 0)  frei [raum_13 TERRASSE 15.17, raum_14 TERRASSE 7.5]
OG3 S1_S2_zuschnitt (1.99, 0)   S1_S2_ohne_zuschnitt (1.99, 0)
DG1 S1_S2_zuschnitt (2.78, 0)   S1_S2_ohne_zuschnitt (2.78, 0)
DG2 S1_S2_zuschnitt (40.4, 2)   innen [raum_2 ZIMMER 4.65/4.65, raum_4 BAD 1.28/1.28]  frei [raum_3 TERRASSE 4.93]
DG2 S1_S2_ohne_zuschnitt (34.46, 0)
DG2 IST innen [raum_2 6.73/4.65, raum_4 2.85/1.28, raum_5 1.14/0.01, stiegenhaus_2 0.23/0.0]
```

### B.3 R-Typisierung mit/ohne Treppenmarker, Schacht-Text (`_ringe_typ.py`, Nachbesserung R1)

- Funktionen: `lade_dxf`, `kaskade.raeume_aus_kaskade`, `rest_komponenten._marker_punkte`, `rest_komponenten._typisiere(shp, k.tueroeffnungen, stiegen | [], sto)`; Polygone = `k.rest_raeume` < 3 m² (vor `finde_lifte`). Schacht-Text: TEXT/MTEXT im Modelspace, Regex `SCHACHT` als Wort oder `F?BDB|DDB` als Wort, ohne `RAUM|TREPP|STIEG|AUFZUG|LIFT`.
- Befehl: `& $PY _ringe_typ.py UG EG OG1 DG1 DG2` (Quelltext: Anhang A.6)
- Kernausgabe:
```text
UG  rest_3 2.691 mit_marker STIEGENHAUS ohne_marker SCHACHT marker [0, 1366]  tuer_n_600 0 sto 0 text_im_polygon [] text_500mm []
EG  rest_2 2.702 mit_marker STIEGENHAUS ohne_marker SCHACHT marker [0, 0]     tuer_n_600 0 sto 0 text_im_polygon [] text_500mm []
OG1 rest_2 2.741 mit_marker STIEGENHAUS ohne_marker SCHACHT marker [0, 0]     tuer_n_600 0 sto 0 text_im_polygon [] text_500mm []
DG1 rest_1 1.251 mit_marker SCHACHT     ohne_marker SCHACHT marker [3604, 3604] tuer_n_600 0 text_im_polygon ["DBA SCHACHT"]
DG1 rest_3 2.302 mit_marker STIEGENHAUS ohne_marker SCHACHT marker [0, 0]     tuer_n_600 0 sto 0 text_im_polygon [] text_500mm []
DG2 rest_2 1.159 mit_marker STIEGENHAUS ohne_marker SCHACHT marker [726, 4125] tuer_n_600 0 text_im_polygon ["DBA SCHACHT"] text_500mm [["DBA SCHACHT", 0]]
DG2 rest_4 2.62  mit_marker STIEGENHAUS ohne_marker SCHACHT marker [210, 3697] tuer_n_600 0 sto 0 text_im_polygon [] text_500mm []
DG2 rest_5 1.427 mit_marker SCHACHT     ohne_marker SCHACHT marker [5098, 10215] tuer_n_600 0 text_im_polygon []
```
- Frühere Messung DG2: Cluster K1-Gegenprüfung `_pruef2` (stdout) `DG2 REST rest_2 … typisiere_heute STIEGENHAUS typisiere_ohne_treppenmarker SCHACHT marker_abst [726, 4125] tueren_600 0 stair_linien_m 0.0`; `rest_1 … ohne_treppenmarker '' … stair_linien_m 51.5`; `rest_4 … ohne SCHACHT marker_abst [3697, 210]`.
- Treppenhüllen-Deckung und Liftringe (U1/U2): Cluster K1 `_regel_messung.py UG EG OG1 OG2 OG3 DG1 DG2` → `STAIR … hull_von_raeumen_gedeckt` UG 0.88, EG 0.91/0.88, OG1 0.89/0.89, OG2 0.98/0.98, OG3 0.99/0.99, DG1 0.91/0.87/0.87, DG2 0.88/0.85; `LIFTRING vorher_m2` UG 2.69, EG 2.7, OG1 2.74, DG1 2.3, DG2 2.62, `rest_ausserhalb_lift_buffer_400_m2` 0.0; `NEU_STIEGENHAUS stiegenhaus_2 15.86 ueberlappt [raum_3 0.08, raum_5 2.26, raum_6 0.3, raum_7 2.36, rest_3 6.41, rest_4 0.87]`.

### B.4 R-Stufe per Monkeypatch mitgeschnitten, 4er-Label (DG2)

- Quelltexte: Anhang A.8.1 (`_pruef.py`), A.8.2 (`_pruef2.py`), A.8.3 (`_label16.py`).
- Aufruf 1 (Cluster K2b-Gegenprüfung): `& $PY _pruef.py DG2`. `rest_komponenten.label`, `rest_komponenten._vektorisiere` und `rest_komponenten._typisiere` werden durch Hüllen ersetzt, die Ein- und Ausgaben protokollieren und die Originale aufrufen. Dann läuft `kaskade.raeume_aus_kaskade(plan)`. Vorab eine synthetische Probe: zwei 6 × 6-Zellblöcke Ecke an Ecke.
```text
kette "kaskade L:7 H:0 F:0 R:5"
synthetik {skimage 0.26.0, label8_n 1, label4_n 2, find_contours_n 2, maske_mm2 180000.0, vektor_mm2 76250}
vektorisierung [{mask 5.838, n_konturen 2, vektor 3.995}, {1.19, 1, 1.159}, {6.605, 1, 6.617}, {2.618, 1, 2.62}, {1.415, 14, 1.422}]
typisiere rest_5: ergebnis SCHACHT, tuer_n_600 0, marker_dist_mm [5098, 10215], sto_n 0
labels_unter_1m2_naehe_text [[0.3, [12555145, 356219655], [799, "S7 | DDB/BDB | 60/95,5"]]]
wk_n 183, wk_roof_n 64, kontur_voll_m2 162.6
```
- Aufruf 2 (Cluster K2b-Gegenprüfung): `& $PY _pruef2.py DG2`. Die Freiflächenmaske der R-Stufe wird wie in Aufruf 1 mitgeschnitten, dann `skimage.measure.label(frei, connectivity=2|1)`; jede Komponente ≥ 1 m² läuft durch das originale `_vektorisiere` und `_typisiere`.
```text
komponenten_4er [{mask 1.845, vektor 1.849, typ SCHACHT, c [12555367, 356216374]}, {mask 1.19, vektor 1.159, typ STIEGENHAUS}, {mask 3.992, vektor 3.995, typ STIEGENHAUS}, …]
```
- Aufruf 3 (Cluster K2b): `& $PY _label16.py` (DG2; Raster und Blockiert-Maske nachgebaut wie `komponenten_ohne_stempel` Z.120-152):
```text
L2/S5 label8 16, label4 30; label8_m2 5.838; n_konturen 2; kontur_flaechen_m2 [3.991, 1.844]; vektor_m2 3.995 (= rest_1); label4_groessen_m2 L2 1.845, S5 1.845, rest1_centroid 3.992
```

### B.5 Synthetische Geometrien

- Quelltexte: Anhang A.8.5 (`_pruef.py`, Funktion `synth`) und A.8.4 (`_synth.py`). Die zweite Messung `_k4g_mess.py synth` steht in A.10.3 und trägt keine Aussage allein (g = 1900 mm ergänzt nur die Tabelle in U6).
- Versiegelung `_wand_geschlossen` (Cluster K4-Gegenprüfung): `& $PY _pruef.py synth`. Quadratischer 6 × 6-m-Raum, Wandring der Dicke t, Lücke g mittig in einer Wand, `_wand_geschlossen(…, 1200)`. Versiegelt = Loch vorhanden; Restbarriere = Abstand des Lochs zum Außenring.
```text
t=200: g=800 versiegelt 51 | g=1000, 1300, 1400, 1600, 2000 offen
t=400: g=800 251 | g=1000 168 | g=1300 44 | g=1400 3 | g=1600, 2000 offen
t=600: g=800 451 | g=1000 368 | g=1300 244 | g=1400 203 | g=1600 120 | g=2000 offen
```
  Zweite Messung mit kollinearer Querlinie (Cluster K4-Gegenprobe `_k4g_mess.py synth`): zusätzlich g=1900 bei t=200/400/600 offen (`rest_mm` 0).
- Durchgänge und Diele (Cluster K6b-Gegenprüfung): `& $PY _synth.py`. Funktionen `tuer_zuordnung.durchgaenge_ohne_tuerblatt`, `tuer_typisierung.typisiere_tueren(ts, rs, "OG1")`, `wohnungen.bilde_wohnungen`.
```text
Durchgang ohne Lücke: t=100 [durchgang_1 4490.0 (5050, 2000)] | t=200 [4458.0] | t=240 [4438.0] | t=260 [] | t=300 []
t=100 mit bekannter 900-mm-Tür bei (5050, 950): [durchgang_1 4490.0 (5050, 1878)]   (Mittelpunkt 928 mm neben der Tür)
Diele vor bilde: t_stgh wohnungseingang, t_ar/t_wc/t_zi/t_bad zimmertuer
Diele nach bilde: alle 5 wohnungseingang; vr klasse ALLGEMEIN_ERSCHLIESSUNG
wohnungen: top_1 [ar], top_2 [bad], top_3 [wc], top_4 [zi]
```

### B.6 Türöffnungen vor/nach `im_planbereich` (gleicher Aufruf wie B.1)

- Logik wie `kaskade.py:110-115`: `oeff = tuer_oeffnungen(plan)`; `im_planbereich(oeff, bounds_aus_wandkoerpern(finde_wandkoerper(plan)))`; gezählt nach `quelle`.
```text
UG  17 {block 15, arc 2}  -> 2 {arc 2}
EG  17 {block 7, arc 10}  -> 10 {arc 10}
OG1 11 {block 9, arc 2}   -> 2 {arc 2}
OG2 12 {block 9, arc 3}   -> 3 {arc 3}
OG3 14 {block 11, arc 3}  -> 3 {arc 3}
DG1 7 {block 5, arc 2}    -> 2 {arc 2}
DG2 5 {block 4, arc 1}    -> 1 {arc 1}
```
- Einzelblöcke OG1 (Cluster K5): `& $PY _tuerbloecke.py OG1` → `tuer_oeffnungen_alle {arc 2, block 9}`, `tuer_oeffnungen_im_planbereich {arc 2}`, INSERT aller Blöcke (12240439, 356160438), `tuerbloecke_insert_im_planbereich 0`, `tuerbloecke_bbox_im_planbereich 9`, Namen `Zargentür_1_Fl 10` 7×, `Schiebetür_Typ1_1_Fl` 2×.

### B.7 Türkette und Wohnungen (Cluster K5, `_tuerkette.py <PLAN>` für EG, OG1, DG2)

- Logik: `provider.parse` Z.64-149 mit Einzelfunktionen nachgebaut (`raeume_aus_kaskade`, `typisiere_geometrisch`, `tueren_aus_dxf`, Öffnungen der Kaskade, `im_planbereich`, `erkenne_aussenbereiche`, `aussentor_tueren`, `verschmelze_doppelfluegel`, `text_tueren`, `ordne_tueren`, `durchgaenge_ohne_tuerblatt`, `aussen_durchgaenge`, `typisiere_tueren`, `bilde_wohnungen`). Abgleich je Raum (`wohnung_id`, `nutzungsklasse`) mit dem Cache.
- Befehl: `& $PY _tuerkette.py DG2` (Quelltext: Anhang A.7)
```text
n_tueren_aus_dxf 0; n_tueroeffnungen_kaskade 1 {arc 1}; n_nach_im_planbereich 1; n_durchgaenge 29
zaehl_detail_final {zimmertuer 4, wohnungseingang 18, balkontuer 3, null 1, stiegenhaustuer 3}
wohnungen top_1 raeume [raum_1, raum_2, raum_4, raum_5] eingaenge [durchgang_3, _5, _6, _7, _11, _12, _13, _14, _15, _17]
wohnungseingang ohne private Seite: durchgang_19 raum_6|rest_1, _20 raum_6|rest_3, _21 raum_7|rest_1, _22 raum_7|rest_2, _23/_24 raum_7|rest_3, _25/_26 raum_7|rest_4
abgleich_cache {} (keine Abweichung); abgleich_ids_nur_cache [lift_1] (finde_lifte nicht nachgebaut)
```

### B.8 M5 Kennzahlen-Zählung (nur JSON; `_m5_zaehlung.py`, Nachbesserung R2)

- Befehl (im Repo-Wurzelordner, nur lesen): `& $PY <scratchpad>/NB2-nachbesserung/_m5_zaehlung.py`. Quelltext: Anhang A.9. Das Skript liest `Projekte/_ergebnis/*/kennzahlen.json` und trennt Dateien ohne `tuer_typen` (Fehler-Stubs), Dateien ohne `tuer_typen.wohnungseingang` und Dateien mit beiden Feldern. Es zählt Verhältnis ≥ 3 bei `wohnungen` ≥ 1 und gruppiert nach `sha256`. Die frühere Zählung (Entwurf R1) lief als `-c`-Einzeiler, dessen Text nicht erhalten ist; sie ist durch diesen Lauf ersetzt.
- Kernausgabe (Umlaute der Konsolenausgabe korrigiert, Fehlertext gekürzt):
```text
dateien 83 ohne tuer_typen 8 tuer_typen ohne wohnungseingang 23 mit beiden 52 ausgewertet (mit tuer_typen) 75
  STUB Baulegende ['dxf', 'fehler', 'plan'] Traceback (most recent call last): …
  STUB Baulegende (Legende) ['dxf', 'fehler', 'plan'] Traceback (most recent call last): …
  STUB din Planungsunterstützung_Stromkreisnummer ['dxf', 'fehler', 'plan'] …
  STUB din_support_ReMi_Barawitzkagasse_28.04.2026 ['dxf', 'fehler', 'plan'] …
  STUB E-Symbole ['dxf', 'fehler', 'plan'] …
  STUB E-Symbole-clean ['dxf', 'fehler', 'plan'] …
  STUB Notbeleuchtungspläne-Vorlage ['dxf', 'fehler', 'plan'] …
  STUB Notbeleuchtungssymbole ['dxf', 'fehler', 'plan'] …
wohnungen >= 1 in allen mit beiden: True
schwelle >= 3: 30 distinct sha256: 28
  dup 7044ff3bed ['EG - Rennweg 15_1030 Wien_Ausfürung-2026-06-12', 'Rennweg_EG']
  dup 4a0b66084d ['Erdgeschoß', 'Mollgasse_EG']
summe WE 1625 W 354
```
- Zusatzaufruf 1, letzte Fehlerzeile der Stubs (`& $PY -c "<Text>"` im Repo-Wurzelordner), Text:
```python
import json
from pathlib import Path
for f in sorted(Path('Projekte/_ergebnis').glob('*/kennzahlen.json')):
    k=json.loads(f.read_text(encoding='utf-8'))
    if 'tuer_typen' not in k:
        z=[l for l in str(k.get('fehler','')).strip().splitlines() if l.strip()]
        print(repr(f.parent.name), '|', z[-1] if z else None)
```
```text
8 Zeilen, jeweils: <Planname> | ValueError: Keine Wand-Entities gefunden … Layer-Muster prüfen.
```
- Zusatzaufruf 2, Verhältnisse ≥ 20 (gleicher Rahmen), Text:
```python
import json
from pathlib import Path
for f in sorted(Path('Projekte/_ergebnis').glob('*/kennzahlen.json')):
    k=json.loads(f.read_text(encoding='utf-8'))
    tt=k.get('tuer_typen') or {}
    we,w=tt.get('wohnungseingang'),k.get('wohnungen')
    if we is not None and w and we/w>=20: print(round(we/w,2), we, w, f.parent.name.encode('ascii','replace').decode())
```
```text
26.33 79 3 260320_938-AR-PP-11000-A_ERDGESCHOSS BT1
26.5 53 2 260320_938-AR-PP-11010-A_1.OBERGESCHOSS BT1
41.0 82 2 260320_938-AR-PP-11020-A_2.OBERGESCHOSS BT1
42.0 42 1 260320_938-AR-PP-21000-A_ERDGESCHOSS BT2
21.5 43 2 Elektromontageapl?ne_1-OBERGESCHOSS BT1
30.0 90 3 Elektromontageapl?ne_2-OBERGESCHOSS BT1
26.33 79 3 Elektromontageapl?ne_ERDGESCHOSS BT1
20.5 41 2 Elektromontageplan_ERDGESCHOSS BT2
```
  Die fünf höchsten Verhältnisse in M5 sind damit belegt; 79/3 kommt zweimal vor (`260320_938-AR-PP-11000-A_ERDGESCHOSS BT1` und `Elektromontageapläne_ERDGESCHOSS BT1`).
- Stand: `git log -1 -- "Projekte/_ergebnis/DG2 - Rennweg 15_1030 Wien_Ausfürung-2026-06-12/kennzahlen.json"` → 1e642ad (2026-09-13); `git ls-tree -r 1e642ad -- Projekte/_ergebnis | grep -c kennzahlen.json` → 83; `git merge-base --is-ancestor 1e642ad 511ad36` → wahr; `git diff --name-only 1e642ad 511ad36 -- src scripts` → nur `platzierung/{deckung,fachpraxis,platzierer,stgh_strategy}.py`, `scripts/analyse/raumerkennung_darstellung.py`.

### B.9 Treppen-Objektmatcher und Stair-Hüllen (DG2, `_ringe_typ.py`)

- Funktionen: `objekt_stiege.finde_stiegen(plan)`; Hülle je `Stair_*`-INSERT aus `stiegenhaus._wcs_pts` über `virtual_entities()`. Quelltext: Anhang A.6 (DG2-Zweig).
```text
OBJEKT_STIEGE n 0 []
HUELLE Stair_1 m2 6.57 kandidaten_in_huelle_m2 0.0
HUELLE Stair_2 m2 8.77 kandidaten_in_huelle_m2 0.0
```

### B.10 Rohbyte-Suche Fluchtweg-Layer

- Befehl (Git Bash, im Repo): `grep -a -c "09-WEG" "Projekte/Rennweg/<PLAN> - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf"` für alle 7 Pläne → jeweils `0`.

### B.11 Gegenprobe Fensterblock-Barriere, Loch-Test und Veto je Variante (Cluster K4, `_aussen_folgen.py <PLAN>`)

- Funktionen: `lade_dxf`, `finde_wandkoerper`, `wand_union`, `aussenbereich.erkenne_aussenbereiche`, `_wand_geschlossen`, `_komponenten_aus`, `grundstuecksgrenze`, `aussen_indizien`, `_strassenkante`; Türkette wie `provider.py` Z.83-149 mit `tuer_oeffnungen`, `im_planbereich`, `tueren_aus_dxf`, `aussentor_tueren`, `verschmelze_doppelfluegel`, `text_tueren`, `ordne_tueren`, `durchgaenge_ohne_tuerblatt`, `aussen_durchgaenge`, `typisiere_tueren`, `bilde_wohnungen`. Räume aus dem Cache, ohne Nutzungsklasse. Quelltext: Anhang A.8.6.
- Varianten: `IST` = echte Funktion. `CF_A` = Loch-Test (Teil ragt > 1 m² aus den Komponenten). `CF_B` = Öffnungsblöcke (minimales gedrehtes Rechteck verschachtelter INSERTs mit FENSTER, WINDOW, TÜR, DOOR oder OPENING im Namen) als zusätzliche Wandkörper. `CF_AB` = beides. `CF_WA` = nur Blöcke mit FENSTER oder WINDOW in Name oder Layer, plus Loch-Test. `CF_C` = Veto aus gestempelten oder typisierten Räumen außer BALKON/TERRASSE. `CF_AC` = Loch-Test plus Veto. Raumschnitte werden nur über 0,2 m² gelistet. Die Namensfilter dienen nur der Gegenprobe.
- Befehl: `& $PY _aussen_folgen.py <PLAN>` je Plan (UG, EG, OG1, OG2, OG3, DG1, DG2) → `_folgen_<PLAN>.json` im Arbeitsordner K4-aussen; die Kernausgabe wurde in der Nachbesserung R2 aus diesen Dateien ausgelesen.
- Kernausgabe (offen m² {Schnitt je Raum m²}):
```text
UG  alle Varianten 23.19 {}          EG  alle Varianten 0.0 {}
OG1 IST 64.13 {raum_1 14.41, raum_2 8.48, raum_3 16.05, raum_15 7.5} | CF_A = IST | CF_B = CF_AB = CF_WA 18.98 {raum_15 6.65} | CF_C = CF_AC 25.02 {raum_15 7.5}
OG2 IST 51.47 {raum_7 8.47, raum_8 12.92, raum_13 15.17, raum_14 7.5} | CF_A = IST | CF_WA 26.81 {raum_13 14.56, raum_14 7.19} | CF_AC 30.01 {raum_13 15.17, raum_14 7.5}
OG3 IST 114.03 {raum_1 36.24, raum_2 40.45, raum_3 15.55, raum_4 18.12} | CF_A 35.66 {raum_3 15.55, raum_4 18.12} | CF_WA 0.0 {} | CF_C = CF_AC 0.0 {}
DG1 IST 143.83 {raum_1 70.83, raum_2 12.63, raum_3 15.05, raum_6 4.05, raum_7 12.85, raum_8 1.58, raum_10 5.55} | CF_A 40.07 {raum_2 12.63, raum_3 15.05, raum_6 4.05, raum_10 5.55} | CF_WA 0.0 {} | CF_C 16.14 {} | CF_AC 0.0 {}
DG2 IST 45.36 {raum_2 6.73, raum_3 4.98, raum_4 2.85, raum_5 1.14, stiegenhaus_2 0.23} | CF_A = IST | CF_WA 32.53 {raum_2 1.8, raum_3 3.65, raum_4 0.34} | CF_AC 34.37 {raum_3 4.93}
komponenten_m2 IST: UG 253.45, EG 295.66, OG1 218.86, OG2 216.06, OG3 191.39, DG1 196.83, DG2 179.51
EG tuer_11 text:TÜRSCHLIESSER AUSSEN|STIEGENHAUS hauseingang; Abstand Komponentenrand IST 184, CF_AB 331, CF_WA 332 mm
EG diff_tueren_CF_WA nur_IST: (…, 'hauseingang', ('AUSSEN', 'STIEGENHAUS'))
OG3 diff_tueren_CF_C nur_IST: 2 × ('STIEGENHAUS', 'AUSSEN'); nur_CF: (251040, 7124416, None, ('STIEGENHAUS', 'AUSSEN'))   Rasterschlüssel × 50 mm = (12552000, 356220800)
```

### B.12 Phantom-Durchgänge Schacht↔Wirtsraum (Cluster K2a-Gegenprüfung, `_k2a_durchgang.py <PLAN>`; in der Nachbesserung R2 neu ausgeführt)

- Funktionen: `lade_dxf`, `finde_wandkoerper`, `wand_union`, `tuer_zuordnung.durchgaenge_ohne_tuerblatt`; Contract-Klassen `Raum`, `Tuer`. Räume aus dem Cache ohne SCHACHT, LIFT und `stiegenhaus_*`. Je Raum werden die Teile von Zone − Wandunion außer dem größten, wenn ≤ 3 m² und mit Beleg in 10 mm (rote geschlossene LWPOLYLINE im Modelspace mit effektiver Farbe 1, Strichstärke 13, ≤ 3 m², oder Wandkörper mit Material SCHACHT), als SCHACHT-Raum ausgestanzt. Der Wirtsraum behält den größten Rest. Die Türliste ist leer (der Cache enthält keine Türen). Quelltext: Anhang A.8.7.
- Befehl: `& $PY _k2a_durchgang.py EG`, danach `OG1` und `DG2` (nacheinander, Arbeitsordner K2a-pruefung-allg).
- Kernausgabe:
```text
[EG] simulierte Schaechte 12; Tueren aus Cache 0; Durchgaenge gesamt 41; davon mit Schacht-Seite 11: [('schacht_1', 'raum_11', 868.0), ('schacht_2', 'raum_11', 1317.0), ('schacht_3', 'raum_12', 1208.0), ('schacht_4', 'raum_12', 1339.0), ('schacht_5', 'raum_12', 1267.0), ('schacht_6', 'raum_12', 1704.0), ('schacht_7', 'raum_12', 1000.0), ('schacht_8', 'raum_12', 1461.0), ('schacht_9', 'raum_12', 931.0), ('schacht_11', 'raum_12', 884.0), ('schacht_12', 'raum_13', 961.0)]
   Schnitt simulierter Schaechte mit spaeter angehaengten stiegenhaus_*-Rechtecken: 0.000 m2
[OG1] simulierte Schaechte 14; Tueren aus Cache 0; Durchgaenge gesamt 32; davon mit Schacht-Seite 6: [('schacht_1', 'raum_2', 1234.0), ('schacht_2', 'raum_9', 1262.0), ('schacht_4', 'raum_9', 824.0), ('schacht_5', 'raum_10', 1000.0), ('schacht_7', 'raum_11', 1316.0), ('schacht_9', 'raum_12', 1598.0)]
   Schnitt simulierter Schaechte mit spaeter angehaengten stiegenhaus_*-Rechtecken: 0.000 m2
[DG2] simulierte Schaechte 6; Tueren aus Cache 0; Durchgaenge gesamt 29; davon mit Schacht-Seite 6: [('schacht_1', 'raum_1', 1176.0), ('schacht_2', 'raum_1', 1155.0), ('schacht_3', 'schacht_4', 844.0), ('schacht_3', 'raum_2', 1521.0), ('schacht_5', 'raum_5', 1250.0), ('schacht_6', 'raum_7', 935.0)]
   Schnitt simulierter Schaechte mit spaeter angehaengten stiegenhaus_*-Rechtecken: 0.090 m2
```
- Abweichung zu Entwurf R1: „DG2 9 von 10 (800-1490 mm)“ ist mit diesem Skript nicht reproduziert. Die 10 DG2-Nebenzellen aus B.14 enthalten 4 Zellen in `stiegenhaus_2`, die dieses Skript ausschließt.

### B.13 R-Kontur, Zone minus Wand, Randabstand und Hals (`_belege_r2.py`, Nachbesserung R2)

- Funktionen: `lade_dxf`, `finde_wandkoerper`, `wand_union`, `wandkoerper.aussenkontur(wk, d_mm=1000)` (wie `rest_komponenten.py:122`), `aussenbereich._wand_geschlossen(wk, 1200)`, `_komponenten_aus`, `grundstuecksgrenze`, `aussen_indizien`, `_strassenkante`, zum Abgleich `erkenne_aussenbereiche`. Zonen = Cache-Polygone. Quelltext: Anhang A.9.
- Befehl: `& $PY _belege_r2.py UG EG OG1 OG2 OG3 DG1 DG2`
- Kernausgabe (m²; `closing_d1000_teile` = Teilflächen mit Löchern, `r_kontur` = gefüllter Außenring des größten Teils):
```text
U10 UG  wk_n 187 wand_union 71.74 r_kontur_d1000 253.2  closing_d1000_teile [152.71]                             komponenten_d1200 253.45
U10 EG  wk_n 192 wand_union 49.36 r_kontur_d1000 295.86 closing_d1000_teile [98.34, 1.47, 0.22]                 komponenten_d1200 295.66
U10 OG1 wk_n 196 wand_union 45.92 r_kontur_d1000 217.07 closing_d1000_teile [105.82, 0.61, 0.35, 0.18]          komponenten_d1200 218.86
U10 OG2 wk_n 177 wand_union 35.74 r_kontur_d1000 204.93 closing_d1000_teile [99.04, 0.66]                       komponenten_d1200 216.06
U10 OG3 wk_n 204 wand_union 33.23 r_kontur_d1000 106.01 closing_d1000_teile [92.48, 0.63, 0.62, 0.59, 0.58, 0.0] komponenten_d1200 191.39
U10 DG1 wk_n 194 wand_union 31.23 r_kontur_d1000 73.5   closing_d1000_teile [73.5, 1.07, 0.63, 0.59, 0.58, 0.45] komponenten_d1200 196.83
U10 DG2 wk_n 183 wand_union 32.21 r_kontur_d1000 162.6  closing_d1000_teile [73.37, 0.03]                       komponenten_d1200 179.51
U9  OG1 raum_3 ZIMMER     zone 16.86 wand_in_zone 0.0  zone_minus_wand_union 16.86 zone_minus_wand_zu 16.05 hauptteil 16.05
U9  DG1 raum_1 WOHNZIMMER zone 73.95 wand_in_zone 1.11 zone_minus_wand_union 72.84 zone_minus_wand_zu 70.83 hauptteil 70.83
U9  DG2 raum_2 ZIMMER     zone 59.28 wand_in_zone 5.36 zone_minus_wand_union 53.93 zone_minus_wand_zu 47.22 hauptteil 40.49
U9  DG2 raum_4 BAD        zone 24.0  wand_in_zone 2.2  zone_minus_wand_union 21.8  zone_minus_wand_zu 19.05 hauptteil 16.2
U9  DG2 raum_5 ZIMMER     zone 19.6  wand_in_zone 0.35 zone_minus_wand_union 19.25 zone_minus_wand_zu 14.36 hauptteil 13.22
U7  UG  kandidaten [{m2 23.19, d_rand_mm 0, hals_d_kante_mm 0, offen true, loch_within false}]; offen_kopie = offen_real [23.19]
U7  EG  kandidaten []; offen_kopie = offen_real []
U7  OG1 kandidaten [{64.13, 0, 0, true, false}]; offen_kopie = offen_real [64.13]
U7  OG2 kandidaten [{51.47, 0, 0, true, false}]; offen_kopie = offen_real [51.47]
U7  OG3 kandidaten [{41.25, 193, 173, true, true}, {37.13, 193, 173, true, true}, {19.53, 0, 0, true, false}, {16.13, 0, 223, true, false}]; offen_kopie = offen_real
U7  DG1 kandidaten [{103.76, 193, 173, true, true}, {20.21, 0, 0, true, false}, {19.86, 0, 218, true, false}]; offen_kopie = offen_real
U7  DG2 kandidaten [{32.47, 0, 0, true, false}, {12.89, 0, 0, true, false}]; offen_kopie = offen_real
    alle 7 Pläne: grundstuecksgrenze false, n_indizien 0, indiz false
```
- Frühere Messungen derselben Größen: Cluster K3 `_k3_messung2.py` (`mess2.txt`: Kontur-R(1000) OG1 217.1, DG1 73.5, DG2 162.6; DG2 `raum_4` Zone-wand_union 21.80, Zone-wand_zu Hauptteil 16.20; `raum_2` 53.93 / 40.49). K3-Gegenprüfung `_pk3.py DG1` (`pk3_DG1.txt`: `aussenkontur(d=1000) m2 73.5 Komponenten d=1000: [73.5, 1.1, 0.6, 0.6, 0.6, 0.4] Huelle 238.6`) und `_pk3c.py` (`pk3c.txt`: `raum_4` Zone-wu Hauptteil 21.80, Zone-wz Hauptteil 16.20; `raum_2` Zone-wz Hauptteil 40.49). Die Quelltexte dieser drei Cluster-Skripte sind nicht im Anhang; die Werte sind durch diesen Lauf ersetzt.

### B.14 Marker-Zellen je Raum (Cluster K2a-Gegenprüfung, `_k2a_pruef.py <PLAN> [raum_ids]`)

- Funktionen: `lade_dxf`, `raumlayer.raeume_aus_layer`, `finde_wandkoerper`, `wand_union`, `tuer_oeffnungen`, `im_planbereich`, `bounds_aus_wandkoerpern`. Rote Rahmen: geschlossene LWPOLYLINE mit effektiver Farbe 1 und Strichstärke 13, ≤ 3 m², Walk bis Blocktiefe 3. Nebenzelle: Teil von Zone − Wandunion außer dem größten, 0,001-3 m². „marker“: Rahmen oder SCHACHT-Wandkörper in 10 mm. Quelltext: Anhang A.8.8.
- Befehle: `& $PY _k2a_pruef.py EG raum_11,raum_13`, `& $PY _k2a_pruef.py OG1 raum_11,raum_13,raum_12`, `& $PY _k2a_pruef.py DG2` → `eg.txt`, `og1.txt`, `dg2.txt` im Arbeitsordner K2a-pruefung-allg. Die Raum-Argumente sind aus den Ausgaben rekonstruiert.
- Kernausgabe (Zellen: Raum, Typ, m²; ohne Zusatz = mit Marker):
```text
[EG] rote geschl. LWPOLYLINE aci1 lw13 <=3m2: gesamt 33; top-level 33; in Bloecken 0 | Wandkoerper 192; material SCHACHT 9
   raum_11 KÜCHE 9.270 m2 | min. symm. Differenz zu L-Polygon 0.0000 m2
   Nebenzellen: {'nebenzellen': 12, 'm2_nebenzellen': 1.964, 'marker': 12, 'm2_marker': 1.964}
   raum_11 KÜCHE 0.4, 0.259 | raum_12 '' 0.312, 0.215, 0.18, 0.176, 0.124, 0.1, 0.095, 0.055, 0.039 | raum_13 MUELLRAUM 0.008
[OG1] gesamt 36; top-level 36; in Bloecken 0 | Wandkoerper 196; material SCHACHT 15
   raum_11 ABSTELLRAUM 4.520 m2 / raum_13 WC 3.502 m2 / raum_12 VORRAUM 10.943 m2 | min. symm. Differenz zu L-Polygon 0.0000 m2
   Nebenzellen: {'nebenzellen': 15, 'm2_nebenzellen': 1.802, 'marker': 14, 'm2_marker': 1.698, 'ohne_marker': 1, 'm2_ohne_marker': 0.104}
   raum_2 ZIMMER 0.169 | raum_9 ZIMMER 0.201, 0.091, 0.055 | raum_10 '' 0.124, 0.025 | raum_11 ABSTELLRAUM 0.236, 0.152 | raum_12 VORRAUM 0.419, 0.065 | raum_13 WC 0.104 (ohne Marker), 0.063, 0.038, 0.032, 0.027
[DG2] gesamt 27; top-level 27; in Bloecken 0 | Wandkoerper 183; material SCHACHT 2
   SCHACHT-Raum rest_5 1.427 m2 bbox [12544287, 356224587, 12546465, 356227737] | Schnitt Rahmen top 0.262 / Rahmen in Bloecken [] / Keil 0.011
   Nebenzellen: {'nebenzellen': 10, 'm2_nebenzellen': 7.356, 'marker': 8, 'm2_marker': 2.223, 'ohne_marker': 2, 'm2_ohne_marker': 5.133}
   raum_1 VORRAUM 0.231, 0.192 | raum_2 ZIMMER 0.403, 0.214 | raum_5 ZIMMER 0.202 | raum_7 VORRAUM 0.09 | stiegenhaus_2 STIEGENHAUS 2.624 (ohne), 2.509 (ohne), 0.741, 0.15
```

### B.15 Seitenproben OG1 `tuer_3` (Cluster K5, `_gegenprobe.py OG1 <Variante>`)

- Logik: `_gegenprobe.py` ersetzt `kaskade.tuer_oeffnungen` und ruft die Türkette `_tuerkette.main` (B.7) auf. V1: Türblock-Öffnung am Bbox-Zentrum mit INSERT-Rotation. V3: wie V1, Winkel None, wenn der INSERT außerhalb der Block-Bbox liegt. V5: Öffnung = Mitte der geschlossenen Blattlage aus dem Schwenkbogen, Sehne aus dem Bogen. V7: wie V5, zusätzlich `tuer_zuordnung._PROBE_MM = 600`. Quelltext: Anhang A.7.
- Befehl: `& $PY _gegenprobe.py OG1 V1` (ebenso V3, V5, V7; Arbeitsordner K5-wohnungen) → `gp_<V>/_out_OG1.json`; die Kernausgabe wurde in der Nachbesserung R2 aus diesen Dateien ausgelesen.
- Kernausgabe (`tueren_final`, Seiten als Raum:Typ:Klasse):
```text
V1 tuer_3  block [12552807, 356217448] von raum_12:VORRAUM:WOHNUNG_PRIVAT nach raum_12:VORRAUM:WOHNUNG_PRIVAT zimmertuer
V3 tuer_3  block [12552807, 356217448] von KEIN_RAUM nach raum_12:VORRAUM:WOHNUNG_PRIVAT None
V5 tuer_3  block [12552566, 356217378] von raum_12:VORRAUM:WOHNUNG_PRIVAT nach KEIN_RAUM None
V7 tuer_3  block [12552566, 356217378] von raum_12:VORRAUM:ALLGEMEIN_ERSCHLIESSUNG nach raum_14:STIEGENHAUS:ALLGEMEIN_ERSCHLIESSUNG wohnungseingang
V7 tuer_10 block [12553230, 356218638] von raum_14:STIEGENHAUS:ALLGEMEIN_ERSCHLIESSUNG nach raum_13:WC:WOHNUNG_PRIVAT wohnungseingang
wohnungen (top_1 jeweils raum_1..raum_9): V1/V3 top_2 [raum_11], top_3 [raum_12, raum_13] | V5 top_2 [raum_11, raum_12, raum_13] | V7 top_2 [raum_11], top_3 [raum_13]
```
- Nicht belegt: die Wanddicke 350 mm an `tuer_3` (in keiner Ausgabe).

### B.16 Außenöffnungen an Stiegenhaus-Resträumen (U19; Cluster K4 `_aussen_folgen.py`, K4-Gegenprüfung `_pruef.py`)

- `_aussen_folgen.py <PLAN>` (B.11): Türkette ohne Nutzungsklasse, Feld `tueren_IST.aussen_tueren` mit Abstand zum Komponentenrand. Quelltext: Anhang A.8.6.
- `_pruef.py DG1 DG2 OG1 OG3` (Arbeitsordner K4-aussen-pruefung-code): Räume mit Cache-Nutzungsklasse; `aussen_durchgaenge` mit Türpunkten aus `tuer_oeffnungen` → `im_planbereich`, einmal mit `kontur = gedeckt()`, einmal mit Komponenten ∪ geschlossen; Ausgabe `_pruef_<PLAN>.json`. Quelltext: Anhang A.8.5.
- Kernausgabe (in der Nachbesserung R2 aus den JSON-Dateien ausgelesen):
```text
_aussen_folgen tueren_IST mit Außenseite:
DG1 aussenoeffnung_1 oeffnung_aussenwand rest_2 STIEGENHAUS|AUSSEN [12549812, 356221732] breite 2590 notausgang True, in_komp False, d_rand 15
DG1 tuer_2 arc raum_3 ZIMMER|AUSSEN balkontuer
OG1 aussenoeffnung_1 oeffnung_aussenwand rest_1 STIEGENHAUS|AUSSEN [12550441, 356221471] breite 1336 notausgang False, in_komp True, d_rand 162
OG1 tuer_2 arc raum_1 ZIMMER|AUSSEN balkontuer
OG2 tuer_1 arc raum_15 ZIMMER|AUSSEN balkontuer; tuer_3 arc raum_8 ZIMMER|AUSSEN balkontuer
OG3 aussenoeffnung_1 rest_3 STIEGENHAUS|AUSSEN breite 2473 notausgang True, d_rand 5222; aussenoeffnung_2 rest_3 breite 822, d_rand 5252
OG3 tuer_1 arc raum_4 ZIMMER|AUSSEN balkontuer
DG2 keine Tür mit Außenseite
_pruef aussen_durchgaenge_IST_gedeckt:
DG1 raum_8 VORRAUM 2095 (d_komp_rand 375), 2357 (1924); rest_2 STIEGENHAUS [12549812, 356221732] 2590 in_komponenten False d_komp_rand 15; rest_2 1403 (4620)
DG2 rest_3 STIEGENHAUS [12549417, 356221796] 1413 in_komponenten True d_komp_rand 286   (identisch in aussen_durchgaenge_nur_komponenten)
OG1 rest_1 STIEGENHAUS [12550441, 356221471] 1336 in_komponenten True d_komp_rand 162   (identisch in nur_komponenten)
OG3 raum_10 GANG 1598 (3768); rest_3 2473 (5221); rest_3 822 (5252)                     (nur_komponenten: keine)
```

