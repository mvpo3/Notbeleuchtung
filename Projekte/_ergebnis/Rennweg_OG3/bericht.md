# Prüfbericht Rennweg_OG3

Raum-Polygon-Quelle: `kaskade L:10 H:0 F:0 R:4` — Rotation: keine dominante Kantenrichtung — 0° belassen.

## Räume

| Quelle | Name | Typ | m² Stempel | m² berechnet | Abw. % | Flag |
|---|---|---|--:|--:|--:|---|
| L | Wohnküche | KÜCHE | 38.35 | 38.35 | +0.0 | ok |
| L | Hobbyraum/Fitness | ZIMMER | 45.36 | 45.36 | -0.0 | ok |
| L | Zimmer | ZIMMER | 20.25 | 20.25 | -0.0 | ok |
| L | Zimmer | ZIMMER | 23.27 | 23.27 | +0.0 | ok |
| L | Bad | BAD | 5.63 | 5.63 | -0.0 | ok |
| L | Bad | BAD | 6.01 | 6.01 | -0.1 | ok |
| L | AR | ABSTELLRAUM | 3.51 | 3.51 | +0.0 | ok |
| L | WC | WC | 1.51 | 1.51 | -0.2 | ok |
| L | Balkon | BALKON | 9.79 | 9.79 | +0.0 | ok |
| L | Gang | GANG | 9.38 | 9.38 | -0.1 | ok |
| R | rest_1 | SCHACHT | — | 1.16 | — | kein_stempel |
| R | rest_2 | SCHACHT | — | 1.15 | — | kein_stempel |
| R | rest_3 | STIEGENHAUS | — | 21.77 | — | kein_stempel |
| R | rest_4 | — | — | 10.09 | — | kein_stempel |

## Restflächen ohne Stempel (4)

- rest_1 [R] SCHACHT: 1.16 m², Zentrum (12555.53, 356216.66) m
- rest_2 [R] SCHACHT: 1.15 m², Zentrum (12552.06, 356216.42) m
- rest_3 [R] STIEGENHAUS: 21.77 m², Zentrum (12549.36, 356219.08) m
- rest_4 [R] —: 10.09 m², Zentrum (12544.50, 356220.31) m

## Warnungen (4)

- Polygon ohne Stempel: rest_1 (1.16 m²)
- Polygon ohne Stempel: rest_2 (1.15 m²)
- Polygon ohne Stempel: rest_3 (21.77 m²)
- Polygon ohne Stempel: rest_4 (10.09 m²)

## Material (Bauteil-Hatches)

| Material | Anzahl | Fläche m² | mittl. Score |
|---|--:|--:|--:|
| WAERMEDAEMMUNG | 142 | 18.3 | 0.69 |
| STAHLBETON | 62 | 14.8 | 0.78 |
| GIPSKARTON_EI0 | 1 | 9.8 | 0.47 |
| SCHACHT | 16 | 0.6 | 0.72 |
| _nicht bewertet (Möbel/Plangrafik-SOLIDs)_ | 22 | 26.7 | — |

Abgrenzung: Muster-Hatches zählen immer als Bauteil; SOLIDs nur mit Material-Treffer, Layer-Hinweis oder Wand-Layer — übrige SOLIDs (Möbel/Treppen/Plangrafik) sind „nicht bewertet“ und gehen NICHT in die Legendenabdeckung ein.

**Legendenabdeckung: 100.0 %** (bekannte Materialfläche / Bauteil-Schraffurfläche)

## Markierungen

- Brandabschnittslinien: 0
- Fluchtweglinien: 0

## Türen (Fachteil 3)

15 / 27 Türen typisiert. Kürzel: Z=zimmertuer, WE=wohnungseingang, ST=stiegenhaustuer, HE=hauseingang, BT=balkontuer, GT=garagentor, BS=brandschutztuer; ? = untypisiert (keine Regel greift), /NA = Notausgang, * = ohne Türblatt.

| ID | raum_a | raum_b | Typ | Breite mm | Breiten-Quelle | Notausgang | Quelle | Grund |
|---|---|---|---|--:|---|---|---|---|
| tuer_1 | raum_4 | AUSSEN | balkontuer | 790 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_2 | raum_3 | raum_3 | zimmertuer | 980 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_3 | KEIN_RAUM | KEIN_RAUM | — | 980 | GEOMETRIE_SCHWENKRADIUS | — | arc | tuer_ins_nichts |
| durchgang_1 | raum_1 | raum_2 | zimmertuer | 3812 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_2 | raum_1 | raum_2 | zimmertuer | 821 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_3 | raum_1 | raum_6 | zimmertuer | 2198 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_4 | raum_1 | raum_7 | zimmertuer | 1749 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_5 | raum_1 | raum_10 | wohnungseingang | 1448 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_6 | raum_2 | raum_8 | zimmertuer | 1987 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_7 | raum_2 | rest_3 | wohnungseingang | 1438 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_8 | raum_2 | rest_4 | — | 1285 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_9 | raum_2 | rest_4 | — | 1460 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_10 | raum_3 | raum_4 | zimmertuer | 3207 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_11 | raum_3 | raum_5 | zimmertuer | 3511 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_12 | raum_3 | rest_4 | — | 1204 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_13 | raum_4 | raum_10 | wohnungseingang | 3104 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_14 | raum_5 | rest_4 | — | 1341 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_15 | raum_5 | rest_4 | — | 2922 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_16 | raum_6 | raum_10 | wohnungseingang | 3641 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_17 | raum_6 | rest_1 | — | 1221 | GEOMETRIE_OEFFNUNG | — | durchgang | tuer_in_schacht |
| durchgang_18 | raum_7 | raum_10 | wohnungseingang | 2114 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_19 | raum_7 | rest_2 | — | 1627 | GEOMETRIE_OEFFNUNG | — | durchgang | tuer_in_schacht |
| durchgang_20 | raum_8 | rest_4 | — | 1983 | GEOMETRIE_OEFFNUNG | — | durchgang | unbekannte_kombination |
| durchgang_21 | raum_10 | rest_2 | — | 1684 | GEOMETRIE_OEFFNUNG | — | durchgang | tuer_in_schacht |
| durchgang_22 | raum_10 | rest_3 | stiegenhaustuer | 1376 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| aussenoeffnung_1 | rest_3 | AUSSEN | — | 2473 | GEOMETRIE_OEFFNUNG | ja | oeffnung_aussenwand | unbekannte_kombination |
| aussenoeffnung_2 | rest_3 | AUSSEN | — | 822 | GEOMETRIE_OEFFNUNG | — | oeffnung_aussenwand | unbekannte_kombination |

## Ausgänge (1)

| ID | Typ | x m | y m |
|---|---|--:|--:|
| exit_durchgang_22 | stair_exit | 12551.93 | 356218.26 |

## Fluchtweg-Segmente (5)

Quellen: GRAPH: 5

| Segment | Quelle | Länge m | Grund | Ziel-Ausgang |
|---|---|--:|---|---|
| seg_graph_durchgang_5 | GRAPH | 6.4 | exit | exit_durchgang_22 |
| seg_graph_durchgang_7 | GRAPH | 6.3 | exit | exit_durchgang_22 |
| seg_graph_durchgang_13 | GRAPH | 2.1 | exit | exit_durchgang_22 |
| seg_graph_durchgang_16 | GRAPH | 5.4 | exit | exit_durchgang_22 |
| seg_graph_durchgang_18 | GRAPH | 6.5 | exit | exit_durchgang_22 |

## Wohnungen (2)

- top_1: 5 Räume (raum_1, raum_2, raum_6, raum_7, raum_8)
- top_2: 3 Räume (raum_3, raum_4, raum_5)

## Weglänge je Wohnungseingang → nächster Ausgang

| Tür | Weglänge m | Quelle | Ausgang |
|---|--:|---|---|
| durchgang_5 | 6.4 | GRAPH | exit_durchgang_22 |
| durchgang_7 | 6.3 | GRAPH | exit_durchgang_22 |
| durchgang_13 | 2.1 | GRAPH | exit_durchgang_22 |
| durchgang_16 | 5.4 | GRAPH | exit_durchgang_22 |
| durchgang_18 | 6.5 | GRAPH | exit_durchgang_22 |

## Leuchten je Nutzungsklasse

| Klasse | Leuchten |
|---|--:|
| ALLGEMEIN_ERSCHLIESSUNG | 2 |
| kein Raum | 1 |
| _davon auf Treppenlauf/Verbotszone_ | 0 |

## Rotationsprüfung RZ über Tür (Messung, ±2°)

- kein RZ näher als 1 m an einer Tür

## Anker je Stiegenhaus (1 Stiegenhäuser)

- **rest_3**: 3 Läufe, 1 Podeste, 4 Verbotszonen (größte 2.2 m², Summe 4.4 m²), 9 Anker
  - PODEST (12550.82, 356218.81) m, Winkel 156°, Fluchtrichtung 188°
  - ANTRITT (12550.56, 356220.36) m, Fluchtrichtung 188°
  - ANTRITT (12547.10, 356218.57) m, Fluchtrichtung 106°
  - AUSTRITT (12548.80, 356217.58) m, Fluchtrichtung 188°
  - ANTRITT (12549.34, 356220.88) m, Fluchtrichtung 106°
  - AUSTRITT (12549.45, 356220.51) m, Fluchtrichtung 106°
  - TUER (12549.91, 356216.11) m, Winkel 149°, Fluchtrichtung 188°
  - TUER (12551.93, 356218.26) m, Winkel 60°, Fluchtrichtung 188°
  - RICHTUNGSWECHSEL (12550.00, 356220.43) m, Fluchtrichtung 188°
- Gang-Anker (außerhalb Stiegenhäuser): 8

## Brandschutz-Hinweise im Plan (0)

- keine

## Außenbereich

- Gebäude-Komponenten: 1 (Flächen m²: 191.4; Summe 191.4)
- offene AUSSEN-Flächen: 4 (114.0 m²)
- geschlossene Höfe (AUSSEN_GESCHLOSSEN): 0 (0.0 m²)
- Überdachungen über offener Außenfläche: 0 (0.0 m²)

## Kreuzcheck Fluchtweglinien ↔ Endausgänge

Restweg im EG (Rennweg_EG.dxf): 4.6–13.5 m (Stiegenhaustür → nächster final_exit)

0 Linien-Endpunkte an der Außenkante, davon 0 mit final_exit ≤ 1.5 m gedeckt.

### Untypisierte Türen — Gründe

| Grund | Anzahl |
|---|--:|
| unbekannte_kombination | 8 |
| tuer_in_schacht | 3 |
| tuer_ins_nichts | 1 |

Laufzeit: 50.5 s
