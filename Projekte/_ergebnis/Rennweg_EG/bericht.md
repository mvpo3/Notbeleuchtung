# Prüfbericht Rennweg_EG

Raum-Polygon-Quelle: `kaskade L:19 H:0 F:0 R:2` — Rotation: keine dominante Kantenrichtung — 0° belassen.

## Räume

„m² roh“ = Polygon VOR der Raumbereinigung (§ 14.6.1), „m² bereinigt“ = `polygon_mm`/`flaeche_m2` des Contracts. „Abw. %“ bleibt der ERKENNUNGS-Wert (Roh-Polygon gegen Stempel) — die bereinigte Abweichung steht im Bereinigungs-Block.

| Quelle | Name | Typ | m² Stempel | m² roh | m² bereinigt | Abw. % (Erkennung, roh) | Flag |
|---|---|---|--:|--:|--:|--:|---|
| L | Wohnküche | KÜCHE | — | 45.60 | 45.60 | — | ok |
| L | AR | ABSTELLRAUM | — | 5.09 | 5.09 | — | ok |
| L | Bad/WC | BAD | — | 5.10 | 5.10 | — | ok |
| L | Zimmer | ZIMMER | — | 11.07 | 11.07 | — | ok |
| L | Garage | GARAGE | — | 36.53 | 36.53 | — | ok |
| L | VR | VORRAUM | — | 21.03 | 21.03 | — | ok |
| L | Stiegenhaus | STIEGENHAUS | — | 6.72 | 6.72 | — | ok |
| L | Terrasse | TERRASSE | — | 17.06 | 17.06 | — | ok |
| L | Müllplatz | — | — | 3.98 | 3.98 | — | ok |
| L | Geschäftslokal 1 | — | 29.11 | 29.11 | 29.11 | +0.0 | ok |
| L | v.Küche | KÜCHE | 9.27 | 9.27 | 9.27 | -0.0 | ok |
| L | GESCHÄFTLOKAL | — | 111.03 | 111.03 | 111.03 | -0.0 | ok |
| L | MÜLLRAUM | MUELLRAUM | 12.92 | 12.92 | 12.92 | -0.0 | ok |
| L | TREPPENHAUS | STIEGENHAUS | 10.89 | 10.89 | 10.89 | -0.0 | ok |
| L | STGH. EG. | STIEGENHAUS | 12.13 | 12.13 | 12.13 | -0.0 | ok |
| L | GANG | GANG | 7.36 | 7.36 | 7.36 | +0.0 | ok |
| L | HOF/Terrasse | TERRASSE | 29.57 | 29.57 | 29.57 | +0.0 | ok |
| L | Zugangsweg | — | — | 5.50 | 5.50 | — | ok |
| L | Garageneinfahrt | — | — | 14.06 | 14.06 | — | ok |
| R | rest_1 | STIEGENHAUS | — | 9.90 | 9.90 | — | kein_stempel |
| R | rest_2 | STIEGENHAUS | — | 2.70 | 2.70 | — | kein_stempel |

## Restflächen ohne Stempel (2)

- rest_1 [R] STIEGENHAUS: 9.90 m², Zentrum (12548.30, 356219.55) m
- rest_2 [R] STIEGENHAUS: 2.70 m², Zentrum (12549.15, 356219.20) m

## Warnungen (2)

- Polygon ohne Stempel: rest_1 (9.90 m²)
- Polygon ohne Stempel: rest_2 (2.70 m²)

## Raumbereinigung (ENIS_UEBERGABE_0908 § 14.6.1)

Überlapper >5 % 0 → 0 · doppelbelegt 0.000 → 0.000000 m² (0.00 mm²) · geändert 1 (Tabelle unten: 1 überlebende) · entfallen 0 · Zerfall 0.000 m² · Schlitzverlust 0.0 mm² · Restkörper entfallener Räume 0.000 m² · Stempelschutz 0

Einträge je Regel: {'SCHWERPUNKT': 1}

Nicht destruktiv: `polygon_roh` hält den Ring vor der Bereinigung, jeder Abzug ist mit Regel und Gegenspieler gebucht. Invariante: Fläche(roh) − Fläche(bereinigt) == Σ der Buchungen.

| id | Name | Quelle | Flag | m² Stempel | m² roh | m² bereinigt | Abw. roh % | Abw. ber. % | Regeln (Gegenspieler) |
|---|---|---|---|--:|--:|--:|--:|--:|---|
| raum_6 | VR | L | ok | — | 21.03 | 21.03 | — | — | SCHWERPUNKT(raum_7) |

### Stempelschutz — nicht ausgestanzt (0)

- keine

### Abweichung bereinigt > 5 % vom Stempel (0)

**war schon > 5 % (0)**
- keine

**neu > 5 % (0)**
- keine

**Rest-Überlappung im RaumModell: 0 Überlapper / 0.000 m².** Die Bereinigung greift am Kaskaden-Ende; `typisiere_geometrisch` und `finde_lifte` legen danach im Provider eigene Räume an (`stiegenhaus_*`, `lift_*`), die sie nicht sieht. `raeume.json` und `RaumModell` sind nur für die Kaskaden-Räume deckungsgleich — der Überlappungs-Riegel misst auf `raeume.json`.

**`lift_*` und SCHACHT:** `lift_erkennung.finde_lifte` überspringt eine Stelle nur, wenn dort ein Raum mit `raum_typ` „LIFT“ liegt — „SCHACHT“ ist nicht abgedeckt. Ein Regel-1-Gewinner mit `raum_typ` „SCHACHT“ kann danach von einem `lift_*`-Raum überdeckt werden, den die Bereinigung nicht mehr sieht. Eigener Arbeitsschritt.

## Material (Bauteil-Hatches)

| Material | Anzahl | Fläche m² | mittl. Score |
|---|--:|--:|--:|
| GIPSKARTON_EI0 | 45 | 31.7 | 0.62 |
| STAHLBETON | 60 | 13.7 | 0.76 |
| WAERMEDAEMMUNG | 78 | 4.8 | 0.69 |
| SCHACHT | 16 | 0.4 | 0.72 |
| _nicht bewertet (Möbel/Plangrafik-SOLIDs)_ | 60 | 0.2 | — |

Abgrenzung: Muster-Hatches zählen immer als Bauteil; SOLIDs nur mit Material-Treffer, Layer-Hinweis oder Wand-Layer — übrige SOLIDs (Möbel/Treppen/Plangrafik) sind „nicht bewertet“ und gehen NICHT in die Legendenabdeckung ein.

**Legendenabdeckung: 100.0 %** (bekannte Materialfläche / Bauteil-Schraffurfläche)

## Markierungen

- Brandabschnittslinien: 0
- Fluchtweglinien: 0

## Türen (Fachteil 3)

24 / 41 Türen typisiert. Kürzel: Z=zimmertuer, WE=wohnungseingang, ST=stiegenhaustuer, HE=hauseingang, BT=balkontuer, GT=garagentor, BS=brandschutztuer; ? = untypisiert (keine Regel greift), /NA = Notausgang, * = ohne Türblatt.

| ID | raum_a | raum_b | Typ | Breite mm | Breiten-Quelle | Notausgang | Quelle | Grund |
|---|---|---|---|--:|---|---|---|---|
| tuer_1 | KEIN_RAUM | AUSSEN | — | 1110 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_2 | KEIN_RAUM | AUSSEN | — | 1110 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_3 | KEIN_RAUM | AUSSEN | — | 1110 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_4 | KEIN_RAUM | KEIN_RAUM | — | 1110 | GEOMETRIE_SCHWENKRADIUS | — | arc | tuer_ins_nichts |
| tuer_5 | KEIN_RAUM | KEIN_RAUM | — | 1110 | GEOMETRIE_SCHWENKRADIUS | — | arc | tuer_ins_nichts |
| tuer_6 | KEIN_RAUM | KEIN_RAUM | — | 1110 | GEOMETRIE_SCHWENKRADIUS | — | arc | tuer_ins_nichts |
| tuer_7 | KEIN_RAUM | raum_17 | — | 1180 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_8 | KEIN_RAUM | KEIN_RAUM | — | 1180 | GEOMETRIE_SCHWENKRADIUS | — | arc | tuer_ins_nichts |
| tuer_9 | raum_12 | raum_17 | — | 1180 | GEOMETRIE_SCHWENKRADIUS | — | arc | unbekannte_kombination |
| tuer_10 | KEIN_RAUM | KEIN_RAUM | hauseingang | 900 | GEOMETRIE_SCHWENKRADIUS | — | arc+text:TÜRSCHLIESSER |  |
| tuer_11 | AUSSEN | raum_14 | hauseingang | — | UNBEKANNT (nur Text-Beleg, keine Geometrie) | — | text:TÜRSCHLIESSER |  |
| durchgang_1 | raum_1 | raum_2 | zimmertuer | 3906 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_2 | raum_1 | raum_6 | wohnungseingang | 2649 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_3 | raum_1 | raum_8 | balkontuer | 5959 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_4 | raum_2 | raum_3 | zimmertuer | 3458 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_5 | raum_2 | raum_6 | wohnungseingang | 2100 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_6 | raum_3 | raum_4 | zimmertuer | 3490 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_7 | raum_3 | raum_6 | wohnungseingang | 2298 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_8 | raum_4 | raum_6 | wohnungseingang | 4189 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_9 | raum_4 | raum_7 | wohnungseingang | 3479 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_10 | raum_5 | raum_6 | garagentor | 2631 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_11 | raum_5 | raum_7 | garagentor | 3635 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_12 | raum_5 | raum_9 | — | 1223 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_13 | raum_5 | raum_19 | garagentor | 4799 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_14 | raum_6 | raum_7 | wohnungseingang | 2600 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_15 | raum_9 | raum_19 | — | 3426 | GEOMETRIE_OEFFNUNG | — | durchgang | beide_seiten_untypisiert |
| durchgang_16 | raum_10 | raum_11 | brandschutztuer | 860 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_17 | raum_11 | raum_13 | — | 3396 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_18 | raum_11 | raum_14 | wohnungseingang | 880 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_19 | raum_12 | raum_14 | — | 5493 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_20 | raum_12 | raum_14 | — | 1786 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_21 | raum_12 | raum_16 | — | 980 | GEOMETRIE_OEFFNUNG | — | durchgang+text:TÜRSCHLIESSER | unbekannte_kombination |
| durchgang_22 | raum_13 | raum_16 | — | 2137 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_23 | raum_14 | raum_15 | stiegenhaustuer | 2080 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_24 | raum_15 | raum_16 | stiegenhaustuer | 2100 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_25 | raum_15 | rest_1 | stiegenhaustuer | 1507 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_26 | raum_15 | rest_1 | stiegenhaustuer | 1496 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_27 | raum_15 | rest_2 | stiegenhaustuer | 2133 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_28 | rest_1 | rest_2 | stiegenhaustuer | 2187 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| aussenoeffnung_1 | raum_13 | AUSSEN | — | 1235 | GEOMETRIE_OEFFNUNG | — | oeffnung_aussenwand | unbekannte_kombination |
| aussenoeffnung_2 | raum_16 | AUSSEN | hauseingang | 1019 | GEOMETRIE_OEFFNUNG | ja | oeffnung_aussenwand+windfang |  |

## Ausgänge (8)

| ID | Typ | x m | y m |
|---|---|--:|--:|
| exit_tuer_10 | final_exit | 12553.32 | 356223.90 |
| exit_tuer_11 | final_exit | 12549.02 | 356210.06 |
| exit_durchgang_23 | stair_exit | 12550.47 | 356215.65 |
| exit_durchgang_24 | stair_exit | 12552.34 | 356220.24 |
| exit_durchgang_25 | stair_exit | 12549.38 | 356217.43 |
| exit_durchgang_26 | stair_exit | 12550.58 | 356220.24 |
| exit_durchgang_27 | stair_exit | 12549.97 | 356218.82 |
| exit_aussenoeffnung_2 | final_exit | 12555.26 | 356222.92 |

## Fluchtweg-Segmente (9)

Quellen: FALLBACK: 1, GRAPH: 8

| Segment | Quelle | Länge m | Grund | Ziel-Ausgang |
|---|---|--:|---|---|
| seg_graph_durchgang_18 | GRAPH | 6.7 | exit | exit_tuer_11 |
| seg_graph_durchgang_22 | GRAPH | 4.9 | exit | exit_aussenoeffnung_2 |
| seg_graph_durchgang_23 | GRAPH | 6.5 | exit | exit_tuer_11 |
| seg_graph_durchgang_24 | GRAPH | 4.6 | exit | exit_tuer_10 |
| seg_graph_durchgang_25 | GRAPH | 10.1 | exit | exit_tuer_11 |
| seg_graph_durchgang_26 | GRAPH | 8.0 | exit | exit_tuer_10 |
| seg_graph_durchgang_27 | GRAPH | 8.4 | exit | exit_tuer_10 |
| seg_graph_durchgang_28 | GRAPH | 13.5 | exit | exit_tuer_10 |
| seg_fallback_raum_7 | FALLBACK | 3.2 | direction_change | — |

## Wohnungen (2)

- top_1: 4 Räume (raum_1, raum_2, raum_3, raum_4)
- top_2: 1 Räume (raum_11)

## Weglänge je Wohnungseingang → nächster Ausgang

| Tür | Weglänge m | Quelle | Ausgang |
|---|--:|---|---|
| durchgang_2 | 1373.6 | Luftlinie | exit_tuer_11 |
| durchgang_5 | 1372.4 | Luftlinie | exit_tuer_11 |
| durchgang_7 | 1372.0 | Luftlinie | exit_tuer_11 |
| durchgang_8 | 1371.6 | Luftlinie | exit_tuer_11 |
| durchgang_9 | 1369.7 | Luftlinie | exit_tuer_11 |
| durchgang_14 | 1371.2 | Luftlinie | exit_tuer_11 |
| durchgang_18 | 6.7 | GRAPH | exit_tuer_11 |

## Leuchten je Nutzungsklasse

| Klasse | Leuchten |
|---|--:|
| ALLGEMEIN_ERSCHLIESSUNG | 7 |
| ALLGEMEIN_NEBENRAUM | 1 |
| AUSSEN | 1 |
| kein Raum | 6 |
| _davon auf Treppenlauf/Verbotszone_ | 0 |

## Rotationsprüfung RZ über Tür (Messung, ±2°)

- kein RZ näher als 1 m an einer Tür

## Anker je Stiegenhaus (5 Stiegenhäuser)

- **raum_7**: 0 Läufe, 1 Podeste, 0 Verbotszonen, 4 Anker
  - PODEST (11821.63, 355049.54) m, Winkel 67°
  - TUER (11820.61, 355050.07) m, Winkel 67°
  - TUER (11822.73, 355049.04) m, Winkel 67°
  - TUER (11820.99, 355048.08) m, Winkel 157°
- **raum_14**: 1 Läufe, 2 Podeste, 1 Verbotszonen (größte 0.6 m², Summe 0.6 m²), 6 Anker
  - PODEST (12548.64, 356211.31) m, Winkel 157°, Fluchtrichtung 140°
  - PODEST (12549.81, 356214.03) m, Winkel 67°, Fluchtrichtung 140°
  - AUSTRITT (12548.94, 356212.02) m, Fluchtrichtung 140°
  - TUER (12551.37, 356214.77) m, Winkel 67°, Fluchtrichtung 140°
  - TUER (12548.73, 356214.17) m, Winkel 67°, Fluchtrichtung 140°
  - TUER (12550.47, 356215.65) m, Winkel 157°, Fluchtrichtung 140°
- **raum_15**: 1 Läufe, 1 Podeste, 1 Verbotszonen (größte 0.7 m², Summe 0.7 m²), 7 Anker
  - PODEST (12551.19, 356218.31) m, Winkel 67°, Fluchtrichtung 143°
  - AUSTRITT (12550.51, 356215.64) m, Fluchtrichtung 143°
  - TUER (12550.47, 356215.65) m, Winkel 157°, Fluchtrichtung 143°
  - TUER (12552.34, 356220.24) m, Winkel 157°, Fluchtrichtung 143°
  - TUER (12549.38, 356217.43) m, Winkel 67°, Fluchtrichtung 143°
  - TUER (12550.58, 356220.24) m, Winkel 67°, Fluchtrichtung 143°
  - TUER (12549.97, 356218.82) m, Winkel 67°, Fluchtrichtung 143°
- **rest_1**: 4 Läufe, 4 Podeste, 4 Verbotszonen (größte 0.5 m², Summe 0.6 m²), 13 Anker
  - PODEST (12546.95, 356219.06) m, Winkel 68°, Fluchtrichtung 67°
  - PODEST (12549.52, 356221.16) m, Winkel 157°, Fluchtrichtung 67°
  - PODEST (12547.81, 356218.46) m, Winkel 68°, Fluchtrichtung 67°
  - ANTRITT (12549.04, 356221.01) m, Fluchtrichtung 67°
  - AUSTRITT (12548.62, 356221.19) m, Fluchtrichtung 67°
  - ANTRITT (12547.73, 356221.54) m, Fluchtrichtung 67°
  - AUSTRITT (12546.47, 356218.63) m, Fluchtrichtung 67°
  - ANTRITT (12547.81, 356220.22) m, Fluchtrichtung 67°
  - AUSTRITT (12547.77, 356220.12) m, Fluchtrichtung 67°
  - TUER (12549.38, 356217.43) m, Winkel 90°, Fluchtrichtung 67°
  - TUER (12550.58, 356220.24) m, Winkel 59°, Fluchtrichtung 67°
  - RICHTUNGSWECHSEL (12548.62, 356221.77) m, Fluchtrichtung 67°
  - RICHTUNGSWECHSEL (12548.22, 356220.71) m, Fluchtrichtung 67°
- **rest_2**: 1 Läufe, 0 Podeste, 2 Verbotszonen (größte 1.7 m², Summe 2.2 m²), 1 Anker
  - TUER (12549.97, 356218.82) m, Winkel 90°, Fluchtrichtung 174°
- Gang-Anker (außerhalb Stiegenhäuser): 9

## Brandschutz-Hinweise im Plan (2)

- „ABGEHÄNGTE DECKE EI90“ bei (12549.25, 356213.25) m
- „ABGEHÄNGTE DECKE EI90“ bei (12552.91, 356213.71) m

## Außenbereich

- Gebäude-Komponenten: 1 (Flächen m²: 295.7; Summe 295.7)
- offene AUSSEN-Flächen: 0 (0.0 m²)
- geschlossene Höfe (AUSSEN_GESCHLOSSEN): 0 (0.0 m²)
- Überdachungen über offener Außenfläche: 0 (0.0 m²)

## Kreuzcheck Fluchtweglinien ↔ Endausgänge

0 Linien-Endpunkte an der Außenkante, davon 0 mit final_exit ≤ 1.5 m gedeckt.

### Fluchtweg-Warnungen

- ⚠ EG/UG: kein final_exit erreichbar von Tür durchgang_2 (Endraum raum_1) — Türgraph endet vor dem Ausgang
- ⚠ EG/UG: kein final_exit erreichbar von Tür durchgang_5 (Endraum raum_2) — Türgraph endet vor dem Ausgang
- ⚠ EG/UG: kein final_exit erreichbar von Tür durchgang_7 (Endraum raum_3) — Türgraph endet vor dem Ausgang
- ⚠ EG/UG: kein final_exit erreichbar von Tür durchgang_8 (Endraum raum_4) — Türgraph endet vor dem Ausgang
- ⚠ EG/UG: kein final_exit erreichbar von Tür durchgang_9 (Endraum raum_4) — Türgraph endet vor dem Ausgang
- ⚠ EG/UG: kein final_exit erreichbar von Tür durchgang_10 (Endraum raum_5) — Türgraph endet vor dem Ausgang
- ⚠ EG/UG: kein final_exit erreichbar von Tür durchgang_11 (Endraum raum_5) — Türgraph endet vor dem Ausgang
- ⚠ EG/UG: kein final_exit erreichbar von Tür durchgang_14 (Endraum raum_6) — Türgraph endet vor dem Ausgang

### Untypisierte Türen — Gründe

| Grund | Anzahl |
|---|--:|
| unbekannte_kombination | 8 |
| kein_nachbarraum | 4 |
| tuer_ins_nichts | 4 |
| beide_seiten_untypisiert | 1 |

Laufzeit: 57.0 s
