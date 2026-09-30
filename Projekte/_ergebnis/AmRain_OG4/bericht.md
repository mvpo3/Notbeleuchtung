# Prüfbericht AmRain_OG4

Raum-Polygon-Quelle: `kaskade L:0 H:0 F:21 R:6` — Rotation: keine dominante Kantenrichtung — 0° belassen.

## Räume

„m² roh“ = Polygon VOR der Raumbereinigung (§ 14.6.1), „m² bereinigt“ = `polygon_mm`/`flaeche_m2` des Contracts. „Abw. %“ bleibt der ERKENNUNGS-Wert (Roh-Polygon gegen Stempel) — die bereinigte Abweichung steht im Bereinigungs-Block.

| Quelle | Name | Typ | m² Stempel | m² roh | m² bereinigt | Abw. % (Erkennung, roh) | Flag |
|---|---|---|--:|--:|--:|--:|---|
| F | WOHNKÜCHE | KÜCHE | 24.98 | 31.17 | 31.12 | +24.8 | flutung_unsicher |
| — | GANG | GANG | 10.83 | — | — | — | kein_polygon |
| F | VR | VORRAUM | 9.25 | 30.78 | 30.78 | +232.8 | flutung_unsicher |
| F | WOHNRAUM | WOHNZIMMER | 19.86 | 21.12 | 21.12 | +6.3 | ok |
| — | VR | VORRAUM | 8.52 | — | — | — | kein_polygon |
| F | WOHNKÜCHE | KÜCHE | 27.42 | 16.76 | 16.76 | -38.9 | flutung_unsicher |
| F | GANG | GANG | 7.56 | 4.27 | 4.27 | -43.5 | flutung_unsicher |
| F | AR | ABSTELLRAUM | 5.48 | 5.16 | 5.16 | -5.9 | ok |
| F | BAD/WC | BAD | 5.21 | 5.85 | 5.85 | +12.2 | flutung_unsicher |
| F | BAD | BAD | 6.47 | 7.94 | 7.94 | +22.7 | flutung_unsicher |
| F | BAD/WC | BAD | 6.36 | 6.30 | 6.30 | -0.9 | ok |
| F | WC | WC | 2.73 | 3.09 | 3.09 | +13.3 | flutung_unsicher |
| F | BAD | BAD | 5.48 | 5.45 | 5.45 | -0.6 | ok |
| F | AR | ABSTELLRAUM | 2.74 | 2.74 | 2.74 | -0.0 | ok |
| F | BAD | BAD | 4.97 | 5.01 | 5.01 | +0.8 | ok |
| — | WC | WC | 1.88 | — | — | — | kein_polygon |
| F | AR | ABSTELLRAUM | 5.11 | 5.11 | 5.11 | -0.0 | ok |
| — | Balkon 3. OG | BALKON | 2.32 | — | — | — | kein_polygon |
| — | Balkon 3. OG | BALKON | 2.32 | — | — | — | kein_polygon |
| — | Balkon 3. OG | BALKON | 2.32 | — | — | — | kein_polygon |
| — | BALKON | BALKON | 2.32 | — | — | — | kein_polygon |
| — | LOGGIA | BALKON | 8.13 | — | — | — | kein_polygon |
| — | LOGGIA | BALKON | 5.38 | — | — | — | kein_polygon |
| — | LOGGIA | BALKON | 7.02 | — | — | — | kein_polygon |
| — | LOGGIA | BALKON | 7.02 | — | — | — | kein_polygon |
| — | GEM.TERRASSE | TERRASSE | 107.61 | — | — | — | kein_polygon |
| — | VR | VORRAUM | 6.87 | — | — | — | kein_polygon |
| F | WC | WC | 3.20 | 3.29 | 3.29 | +2.9 | ok |
| — | VR | VORRAUM | 2.66 | — | — | — | kein_polygon |
| F | VR | VORRAUM | 2.12 | 2.18 | 2.18 | +3.0 | ok |
| F | BAD | BAD | 6.62 | 6.71 | 6.71 | +1.4 | ok |
| F | WOHNRAUM | WOHNZIMMER | 20.08 | 29.93 | 29.91 | +49.1 | flutung_unsicher |
| — | STGH | STIEGENHAUS | 32.44 | — | — | — | kein_polygon |
| — | BALKON | BALKON | 5.36 | — | — | — | kein_polygon |
| — | LOGGIA | BALKON | 7.88 | — | — | — | kein_polygon |
| F | WOHNKÜCHE | KÜCHE | 37.89 | 52.11 | 52.06 | +37.5 | flutung_unsicher |
| — | TERRASSE | TERRASSE | 27.89 | — | — | — | kein_polygon |
| F | GANG | GANG | 8.24 | 14.98 | 14.95 | +81.8 | flutung_unsicher |
| — | TERRASSE | TERRASSE | 36.31 | — | — | — | kein_polygon |
| — | SERVICE-TERRASSE | TERRASSE | 15.20 | — | — | — | kein_polygon |
| F | WC | WC | 2.19 | 2.76 | 2.76 | +26.1 | flutung_unsicher |
| R | rest_1 | GANG | — | 3.56 | 3.56 | — | kein_stempel |
| R | rest_2 | — | — | 40.17 | 40.17 | — | kein_stempel |
| R | rest_3 | — | — | 3.87 | 3.87 | — | kein_stempel |
| R | rest_4 | NISCHE | — | 1.19 | 1.19 | — | kein_stempel |
| R | rest_5 | GANG | — | 4.38 | 4.38 | — | kein_stempel |
| R | rest_6 | — | — | 1.70 | 1.70 | — | kein_stempel |

## Restflächen ohne Stempel (6)

- rest_1 [R] GANG: 3.56 m², Zentrum (9.34, 3.99) m
- rest_2 [R] —: 40.17 m², Zentrum (12.82, 11.26) m
- rest_3 [R] —: 3.87 m², Zentrum (8.74, 9.96) m
- rest_4 [R] NISCHE: 1.19 m², Zentrum (14.01, 16.45) m
- rest_5 [R] GANG: 4.38 m², Zentrum (11.10, 18.87) m
- rest_6 [R] —: 1.70 m², Zentrum (8.62, 18.54) m

## Warnungen (37)

- Stempel ohne Polygon: „GANG“
- Stempel ohne Polygon: „VR“
- Stempel ohne Polygon: „WC“
- Stempel ohne Polygon: „Balkon 3. OG“
- Stempel ohne Polygon: „Balkon 3. OG“
- Stempel ohne Polygon: „Balkon 3. OG“
- Stempel ohne Polygon: „BALKON“
- Stempel ohne Polygon: „LOGGIA“
- Stempel ohne Polygon: „LOGGIA“
- Stempel ohne Polygon: „LOGGIA“
- Stempel ohne Polygon: „LOGGIA“
- Stempel ohne Polygon: „GEM.TERRASSE“
- Stempel ohne Polygon: „VR“
- Stempel ohne Polygon: „VR“
- Stempel ohne Polygon: „STGH“
- Stempel ohne Polygon: „BALKON“
- Stempel ohne Polygon: „LOGGIA“
- Stempel ohne Polygon: „TERRASSE“
- Stempel ohne Polygon: „TERRASSE“
- Stempel ohne Polygon: „SERVICE-TERRASSE“
- Polygon ohne Stempel: rest_1 (3.56 m²)
- Polygon ohne Stempel: rest_2 (40.17 m²)
- Polygon ohne Stempel: rest_3 (3.87 m²)
- Polygon ohne Stempel: rest_4 (1.19 m²)
- Polygon ohne Stempel: rest_5 (4.38 m²)
- Polygon ohne Stempel: rest_6 (1.70 m²)
- Abweichung > 10 % (Erkennung, roh): „WOHNKÜCHE“ (+24.8 %)
- Abweichung > 10 % (Erkennung, roh): „VR“ (+232.8 %)
- Abweichung > 10 % (Erkennung, roh): „WOHNKÜCHE“ (-38.9 %)
- Abweichung > 10 % (Erkennung, roh): „GANG“ (-43.5 %)
- Abweichung > 10 % (Erkennung, roh): „BAD/WC“ (+12.2 %)
- Abweichung > 10 % (Erkennung, roh): „BAD“ (+22.7 %)
- Abweichung > 10 % (Erkennung, roh): „WC“ (+13.3 %)
- Abweichung > 10 % (Erkennung, roh): „WOHNRAUM“ (+49.1 %)
- Abweichung > 10 % (Erkennung, roh): „WOHNKÜCHE“ (+37.5 %)
- Abweichung > 10 % (Erkennung, roh): „GANG“ (+81.8 %)
- Abweichung > 10 % (Erkennung, roh): „WC“ (+26.1 %)

## Bekannte Grenze: ausgebrochene Flutungen

Bei diesen Stempeln läuft die Flutung über eine offene Tür in Vorplatz/Korridor. Zwei Gegenversuche brachten keine Verbesserung ohne Regression und sind daher NICHT eingebaut: eine zusätzliche niedrigere Start-Versiegelungsstufe (300 bzw. 400 mm) senkte plan-weit die „ok“-Flutungen von 41 auf 38; eine Deckelung der Flutfläche auf 3× Stempelfläche trifft zwar genau diese Fälle, verletzt aber die Modul-Invariante „NIE verwerfen“ (`test_stempel_flutung.py::test_riesenbereich_unsicher`). Die Fälle bleiben darum als `flutung_unsicher` ehrlich geflaggt.

Ergänzung § 14.6.1: die Invariante „NIE verwerfen“ gilt der FLUTUNG. Die Raumbereinigung danach kann einen Raum auf einen Restkörper < 1 m² zusammenschneiden — der entfällt dann aus dem Modell und steht namentlich im Bereinigungs-Block sowie in `raeume.json` unter `entfallen`.

- „VR“: 9.25 m² Stempel → 30.78 m² geflutet (+233 %)

## Raumbereinigung (ENIS_UEBERGABE_0908 § 14.6.1)

Überlapper >5 % 0 → 0 · doppelbelegt 0.162 → 0.000001 m² (0.55 mm²) · geändert 7 (Tabelle unten: 7 überlebende) · entfallen 0 · Zerfall 0.000 m² · Schlitzverlust 0.0 mm² · Restkörper entfallener Räume 0.000 m² · Stempelschutz 0

Einträge je Regel: {'SCHWERPUNKT': 2, 'STEMPEL_NAEHE': 6, 'ZERFALL': 2}

Nicht destruktiv: `polygon_roh` hält den Ring vor der Bereinigung, jeder Abzug ist mit Regel und Gegenspieler gebucht. Invariante: Fläche(roh) − Fläche(bereinigt) == Σ der Buchungen.

| id | Name | Quelle | Flag | m² Stempel | m² roh | m² bereinigt | Abw. roh % | Abw. ber. % | Regeln (Gegenspieler) |
|---|---|---|---|--:|--:|--:|--:|--:|---|
| raum_1 | WOHNKÜCHE | F | flutung_unsicher | 24.98 | 31.17 | 31.12 | +24.8 | +24.6 | STEMPEL_NAEHE(raum_11) |
| raum_10 | WC | F | flutung_unsicher | 2.73 | 3.09 | 3.09 | +13.3 | +13.2 | STEMPEL_NAEHE(raum_11) |
| raum_18 | WOHNRAUM | F | flutung_unsicher | 20.08 | 29.93 | 29.91 | +49.1 | +49.0 | STEMPEL_NAEHE(raum_17) |
| raum_19 | WOHNKÜCHE | F | flutung_unsicher | 37.89 | 52.11 | 52.06 | +37.5 | +37.4 | STEMPEL_NAEHE(raum_6), ZERFALL |
| raum_20 | GANG | F | flutung_unsicher | 8.24 | 14.98 | 14.95 | +81.8 | +81.5 | STEMPEL_NAEHE(raum_8) |
| raum_5 | GANG | F | flutung_unsicher | 7.56 | 4.27 | 4.27 | -43.5 | -43.5 | STEMPEL_NAEHE(raum_16), ZERFALL |
| rest_2 | — | R | kein_stempel | — | 40.17 | 40.17 | — | — | SCHWERPUNKT(rest_5), SCHWERPUNKT(rest_4) |

### Stempelschutz — nicht ausgestanzt (0)

- keine

### Abweichung bereinigt > 5 % vom Stempel (6)

**war schon > 5 % (6)**
- raum_1 „WOHNKÜCHE“: Stempel 24.98 m², roh +24.8 % → bereinigt +24.6 %
- raum_10 „WC“: Stempel 2.73 m², roh +13.3 % → bereinigt +13.2 %
- raum_18 „WOHNRAUM“: Stempel 20.08 m², roh +49.1 % → bereinigt +49.0 %
- raum_19 „WOHNKÜCHE“: Stempel 37.89 m², roh +37.5 % → bereinigt +37.4 %
- raum_20 „GANG“: Stempel 8.24 m², roh +81.8 % → bereinigt +81.5 %
- raum_5 „GANG“: Stempel 7.56 m², roh -43.5 % → bereinigt -43.5 %

**neu > 5 % (0)**
- keine

**Rest-Überlappung im RaumModell: 0 Überlapper / 0.000 m².** Die Bereinigung greift am Kaskaden-Ende; `typisiere_geometrisch` und `finde_lifte` legen danach im Provider eigene Räume an (`stiegenhaus_*`, `lift_*`), die sie nicht sieht. `raeume.json` und `RaumModell` sind nur für die Kaskaden-Räume deckungsgleich — der Überlappungs-Riegel misst auf `raeume.json`.

**`lift_*` und SCHACHT:** `lift_erkennung.finde_lifte` überspringt eine Stelle nur, wenn dort ein Raum mit `raum_typ` „LIFT“ liegt — „SCHACHT“ ist nicht abgedeckt. Ein Regel-1-Gewinner mit `raum_typ` „SCHACHT“ kann danach von einem `lift_*`-Raum überdeckt werden, den die Bereinigung nicht mehr sieht. Eigener Arbeitsschritt.

## Material (Bauteil-Hatches)

| Material | Anzahl | Fläche m² | mittl. Score |
|---|--:|--:|--:|
| STAHLBETON | 59 | 38.7 | via Layer |
| ZIEGELMAUERWERK | 27 | 0.4 | 0.75 |
| _nicht bewertet (Möbel/Plangrafik-SOLIDs)_ | 1186 | 80.7 | — |

Abgrenzung: Muster-Hatches zählen immer als Bauteil; SOLIDs nur mit Material-Treffer, Layer-Hinweis oder Wand-Layer — übrige SOLIDs (Möbel/Treppen/Plangrafik) sind „nicht bewertet“ und gehen NICHT in die Legendenabdeckung ein.

**Legendenabdeckung: 100.0 %** (bekannte Materialfläche / Bauteil-Schraffurfläche)

## Markierungen

- Brandabschnittslinien: 0
- Fluchtweglinien: 0

## Türen (Fachteil 3)

22 / 58 Türen typisiert. Kürzel: Z=zimmertuer, WE=wohnungseingang, ST=stiegenhaustuer, HE=hauseingang, BT=balkontuer, GT=garagentor, BS=brandschutztuer; ? = untypisiert (keine Regel greift), /NA = Notausgang, * = ohne Türblatt.

| ID | raum_a | raum_b | Typ | Breite mm | Breiten-Quelle | Notausgang | Quelle | Grund |
|---|---|---|---|--:|---|---|---|---|
| tuer_1 | AUSSEN | rest_5 | — | 800 | GEOMETRIE_SCHWENKRADIUS | ja | arc+windfang | unbekannte_kombination |
| tuer_2 | KEIN_RAUM | raum_18 | — | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_3 | raum_9 | rest_2 | — | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc | unbekannte_kombination |
| tuer_4 | raum_6 | raum_19 | zimmertuer | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_5 | AUSSEN | rest_2 | — | 940 | GEOMETRIE_SCHWENKRADIUS | — | arc | beide_seiten_untypisiert |
| tuer_6 | raum_2 | KEIN_RAUM | — | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_7 | AUSSEN | raum_1 | balkontuer | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_8 | raum_1 | KEIN_RAUM | — | 980 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_9 | raum_2 | KEIN_RAUM | — | 980 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_10 | AUSSEN | raum_1 | balkontuer | 940 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_11 | raum_4 | KEIN_RAUM | — | 980 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_12 | raum_3 | KEIN_RAUM | — | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_13 | AUSSEN | raum_18 | balkontuer | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_14 | raum_14 | raum_7 | zimmertuer | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_15 | raum_20 | KEIN_RAUM | — | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_16 | KEIN_RAUM | raum_7 | — | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_17 | raum_20 | KEIN_RAUM | — | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_18 | KEIN_RAUM | KEIN_RAUM | — | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc | tuer_ins_nichts |
| tuer_19 | raum_5 | rest_5 | — | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc | unbekannte_kombination |
| tuer_20 | KEIN_RAUM | raum_5 | — | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_21 | raum_5 | KEIN_RAUM | — | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_22 | rest_1 | raum_10 | wohnungseingang | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_23 | raum_1 | raum_11 | zimmertuer | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_24 | rest_2 | KEIN_RAUM | — | 900 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_25 | rest_2 | KEIN_RAUM | — | 900 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_26 | raum_6 | raum_19 | zimmertuer | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_27 | rest_2 | rest_2 | — | 900 | GEOMETRIE_SCHWENKRADIUS | — | arc | beide_seiten_untypisiert |
| tuer_28 | rest_5 | rest_2 | — | 900 | GEOMETRIE_SCHWENKRADIUS | — | arc | unbekannte_kombination |
| tuer_29 | raum_19 | KEIN_RAUM | — | 980 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_30 | raum_19 | raum_19 | zimmertuer | 980 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_31 | raum_19 | AUSSEN | balkontuer | 980 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_32 | raum_19 | AUSSEN | balkontuer | 940 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_33 | KEIN_RAUM | raum_1 | — | 940 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_34 | AUSSEN | KEIN_RAUM | — | 940 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_35 | raum_2 | AUSSEN | balkontuer | 940 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_36 | raum_19 | AUSSEN | balkontuer | 940 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_37 | AUSSEN | raum_20 | — | 940 | GEOMETRIE_SCHWENKRADIUS | — | arc | unbekannte_kombination |
| tuer_38 | raum_20 | KEIN_RAUM | — | 940 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_39 | KEIN_RAUM | KEIN_RAUM | — | 940 | GEOMETRIE_SCHWENKRADIUS | — | arc | tuer_ins_nichts |
| tuer_40 | raum_18 | AUSSEN | balkontuer | 980 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_41 | raum_3 | KEIN_RAUM | — | 980 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| tuer_42 | rest_2 | raum_15 | — | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc | unbekannte_kombination |
| tuer_43 | raum_18 | raum_17 | zimmertuer | 800 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_44 | AUSSEN | raum_19 | balkontuer | 940 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_45 | KEIN_RAUM | AUSSEN | — | 940 | GEOMETRIE_SCHWENKRADIUS | — | arc | kein_nachbarraum |
| durchgang_1 | raum_1 | rest_1 | wohnungseingang | 1392 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_2 | raum_5 | rest_5 | — | 1672 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_3 | raum_6 | raum_21 | zimmertuer | 2326 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_4 | raum_8 | raum_20 | wohnungseingang | 2328 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_5 | raum_9 | rest_2 | — | 2338 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_6 | raum_13 | rest_6 | — | 1834 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_7 | raum_15 | raum_17 | zimmertuer | 2686 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_8 | raum_16 | rest_5 | wohnungseingang | 2217 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_9 | raum_16 | rest_6 | — | 1911 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_10 | raum_17 | raum_18 | zimmertuer | 1458 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_11 | raum_18 | rest_2 | — | 2631 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_12 | rest_2 | rest_4 | — | 1282 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| aussenoeffnung_1 | raum_5 | AUSSEN | — | 1378 | GEOMETRIE_OEFFNUNG | ja | oeffnung_aussenwand+windfang | unbekannte_kombination |

## Ausgänge (0)

| ID | Typ | x m | y m |
|---|---|--:|--:|

### Kein Endausgang wegen Freifläche (0 Türen ins Freie an BALKON/TERRASSE)

keine — auf diesem Plan führt keine Tür an einem typisierten BALKON/TERRASSE-Raum vorbei.

## Fluchtweg-Segmente (4)

Quellen: FALLBACK: 4

| Segment | Quelle | Länge m | Grund | Ziel-Ausgang |
|---|---|--:|---|---|
| seg_fallback_raum_5 | FALLBACK | 3.5 | direction_change | — |
| seg_fallback_raum_20 | FALLBACK | 3.8 | direction_change | — |
| seg_fallback_rest_1 | FALLBACK | 3.1 | direction_change | — |
| seg_fallback_rest_5 | FALLBACK | 3.4 | direction_change | — |

## Wohnungen (11)

- top_1: 2 Räume (raum_1, raum_11)
- top_10: 1 Räume (raum_4)
- top_11: 1 Räume (raum_9)
- top_2: 1 Räume (raum_10)
- top_3: 1 Räume (raum_12)
- top_4: 1 Räume (raum_13)
- top_5: 2 Räume (raum_14, raum_7)
- top_6: 3 Räume (raum_15, raum_17, raum_18)
- top_7: 3 Räume (raum_19, raum_21, raum_6)
- top_8: 2 Räume (raum_20, raum_8)
- top_9: 1 Räume (raum_3)

## Weglänge je Wohnungseingang → nächster Ausgang

| Tür | Weglänge m | Quelle | Ausgang |
|---|--:|---|---|
| tuer_22 | — | kein Ausgang | — |
| durchgang_1 | — | kein Ausgang | — |
| durchgang_8 | — | kein Ausgang | — |

## Leuchten je Nutzungsklasse

| Klasse | Leuchten |
|---|--:|
| ALLGEMEIN_ERSCHLIESSUNG | 9 |
| kein Raum | 1 |
| unbestimmt | 3 |
| _davon auf Treppenlauf/Verbotszone_ | 0 |

## Rotationsprüfung RZ über Tür (Messung, ±2°)

- kein RZ näher als 1 m an einer Tür

## Anker je Stiegenhaus (0 Stiegenhäuser)

- Gang-Anker (außerhalb Stiegenhäuser): 34

## Brandschutz-Hinweise im Plan (2)

- „EI 30“ bei (15.24, 11.55) m
- „EI 30“ bei (15.22, 14.85) m

## Außenbereich

- Gebäude-Komponenten: 7 (Flächen m²: 72.1, 1.3, 1.1, 1.3, 158.0, 2.5, 1.7; Summe 237.9)
- offene AUSSEN-Flächen: 17 (1033.4 m²)
- geschlossene Höfe (AUSSEN_GESCHLOSSEN): 0 (0.0 m²)
- Überdachungen über offener Außenfläche: 2 (14.7 m²)

## Geschoss

- Geschoss: **4OG** (Quelle `dateiname`)
- Beleg: Dateiname 'AmRain_OG4' → 'OG4'
- ⚠ kein Geschossausgang ableitbar
  - final_exit: keine hauseingang-/Notausgangstür ins Freie (EG)
  - stair_exit: keine stiegenhaustuer/wohnungseingang am STIEGENHAUS

## Kreuzcheck Fluchtweglinien ↔ Endausgänge

Restweg im EG: unbekannt (AmRain_EG.dxf: kein Segment Stiegenhaustür→final_exit)

0 Linien-Endpunkte an der Außenkante, davon 0 mit final_exit ≤ 1.5 m gedeckt.

### Unbestimmte Räume (§ 6g)

- ⚠ unbestimmt: raum_20 — Ankerregel nicht auswertbar: vom Stiegenhaus über keine Tür erreichbar — Tür- oder Raumerkennungsloch, kein Klassifikationsproblem; hinter seinen rohen Wohnungseingängen liegen nur Einzelräume, er bildet mit ihnen eine Wohnung (R1) — die Wohnung folgt rohen Türen, die Klasse bleibt offen (Owner 2026-09-22)

### Tür- oder Raumerkennungslöcher (Messfall S4c/S3b)

- ⚠ loch: raum_16 — vom Stiegenhaus über keine Tür erreichbar — Tür- oder Raumerkennungsloch, kein Klassifikationsproblem (Messfall S4c/S3b); Klasse allgemein; weder über eine rohe Zimmertür an eine Wohnung gebunden noch ein Loch-GANG mit nur Einzelräumen hinter seinen rohen Wohnungseingängen (R1) → keine Wohnung, Erschließung (Wohnung folgt rohen Türen, Owner 2026-09-22), Notlicht bleibt
- ⚠ loch: raum_2 — vom Stiegenhaus über keine Tür erreichbar — Tür- oder Raumerkennungsloch, kein Klassifikationsproblem (Messfall S4c/S3b); Klasse allgemein; weder über eine rohe Zimmertür an eine Wohnung gebunden noch ein Loch-GANG mit nur Einzelräumen hinter seinen rohen Wohnungseingängen (R1) → keine Wohnung, Erschließung (Wohnung folgt rohen Türen, Owner 2026-09-22), Notlicht bleibt
- ⚠ loch: raum_20 — vom Stiegenhaus über keine Tür erreichbar — Tür- oder Raumerkennungsloch, kein Klassifikationsproblem (Messfall S4c/S3b); Klasse offen; hinter seinen rohen Wohnungseingängen liegen nur Einzelräume → er bildet mit ihnen eine Wohnung (R1) (Wohnung folgt rohen Türen, Owner 2026-09-22), Notlicht bleibt
- ⚠ loch: raum_5 — vom Stiegenhaus über keine Tür erreichbar — Tür- oder Raumerkennungsloch, kein Klassifikationsproblem (Messfall S4c/S3b); Klasse allgemein; weder über eine rohe Zimmertür an eine Wohnung gebunden noch ein Loch-GANG mit nur Einzelräumen hinter seinen rohen Wohnungseingängen (R1) → keine Wohnung, Erschließung (Wohnung folgt rohen Türen, Owner 2026-09-22), Notlicht bleibt
- ⚠ loch: rest_1 — vom Stiegenhaus über keine Tür erreichbar — Tür- oder Raumerkennungsloch, kein Klassifikationsproblem (Messfall S4c/S3b); Klasse allgemein; weder über eine rohe Zimmertür an eine Wohnung gebunden noch ein Loch-GANG mit nur Einzelräumen hinter seinen rohen Wohnungseingängen (R1) → keine Wohnung, Erschließung (Wohnung folgt rohen Türen, Owner 2026-09-22), Notlicht bleibt
- ⚠ loch: rest_5 — vom Stiegenhaus über keine Tür erreichbar — Tür- oder Raumerkennungsloch, kein Klassifikationsproblem (Messfall S4c/S3b); Klasse allgemein; weder über eine rohe Zimmertür an eine Wohnung gebunden noch ein Loch-GANG mit nur Einzelräumen hinter seinen rohen Wohnungseingängen (R1) → keine Wohnung, Erschließung (Wohnung folgt rohen Türen, Owner 2026-09-22), Notlicht bleibt

### Untypisierte Türen — Gründe

| Grund | Anzahl |
|---|--:|
| kein_nachbarraum | 19 |
| unbekannte_kombination | 13 |
| beide_seiten_untypisiert | 2 |
| tuer_ins_nichts | 2 |

Laufzeit: 1551.7 s
