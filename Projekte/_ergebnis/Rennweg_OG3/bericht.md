# Prüfbericht Rennweg_OG3

Raum-Polygon-Quelle: `kaskade L:10 H:0 F:0 R:6` — Rotation: keine dominante Kantenrichtung — 0° belassen.

## Räume

„m² roh“ = Polygon VOR der Raumbereinigung (§ 14.6.1), „m² bereinigt“ = `polygon_mm`/`flaeche_m2` des Contracts. „Abw. %“ bleibt der ERKENNUNGS-Wert (Roh-Polygon gegen Stempel) — die bereinigte Abweichung steht im Bereinigungs-Block.

| Quelle | Name | Typ | m² Stempel | m² roh | m² bereinigt | Abw. % (Erkennung, roh) | Flag |
|---|---|---|--:|--:|--:|--:|---|
| L | Wohnküche | KÜCHE | 38.35 | 38.35 | 38.35 | +0.0 | ok |
| L | Hobbyraum/Fitness | ZIMMER | 45.36 | 45.36 | 45.36 | -0.0 | ok |
| L | Zimmer | ZIMMER | 20.25 | 20.25 | 20.25 | -0.0 | ok |
| L | Zimmer | ZIMMER | 23.27 | 23.27 | 23.27 | +0.0 | ok |
| L | Bad | BAD | 5.63 | 5.63 | 5.63 | -0.0 | ok |
| L | Bad | BAD | 6.01 | 6.01 | 6.01 | -0.1 | ok |
| L | AR | ABSTELLRAUM | 3.51 | 3.51 | 3.51 | +0.0 | ok |
| L | WC | WC | 1.51 | 1.51 | 1.51 | -0.2 | ok |
| L | Balkon | BALKON | 9.79 | 9.79 | 9.79 | +0.0 | ok |
| L | Gang | GANG | 9.38 | 9.38 | 9.38 | -0.1 | ok |
| R | rest_1 | SCHACHT | — | 1.16 | 1.16 | — | kein_stempel |
| R | rest_2 | SCHACHT | — | 1.15 | 1.15 | — | kein_stempel |
| R | rest_3 | STIEGENHAUS | — | 8.53 | 8.53 | — | kein_stempel |
| R | rest_4 | STIEGENHAUS | — | 12.22 | 12.22 | — | kein_stempel |
| R | rest_5 | GANG | — | 3.53 | 3.53 | — | kein_stempel |
| R | rest_6 | — | — | 6.56 | 6.56 | — | kein_stempel |

## Restflächen ohne Stempel (6)

- rest_1 [R] SCHACHT: 1.16 m², Zentrum (12555.53, 356216.66) m
- rest_2 [R] SCHACHT: 1.15 m², Zentrum (12552.06, 356216.42) m
- rest_3 [R] STIEGENHAUS: 8.53 m², Zentrum (12550.09, 356218.28) m
- rest_4 [R] STIEGENHAUS: 12.22 m², Zentrum (12548.89, 356219.63) m
- rest_5 [R] GANG: 3.53 m², Zentrum (12545.83, 356219.59) m
- rest_6 [R] —: 6.56 m², Zentrum (12543.79, 356220.70) m

## Warnungen (10)

- mm_faktor: 1 aus $INSUNITS=4 (keine Wand-Spanne 15–500 m messbar), Türprobe: keine
- seite_fehlt: tuer_3 Seite + bis 500 mm kein Raum und kein AUSSEN (nur Wandkörper oder gedeckte Freifläche)
- seite_fehlt: tuer_3 Seite - bis 500 mm kein Raum und kein AUSSEN (nur Wandkörper oder gedeckte Freifläche)
- sanitaer: rest_6: BAD aus Sanitärbeleg (DUSCHE 1, WASCHBECKEN 2, WC 1) im Umriss top_2 (Probe) — Nachbarn nur top_2: raum_2 ZIMMER top_2, raum_3 ZIMMER top_2, raum_5 BAD top_2, raum_8 WC top_2, rest_5 GANG top_2
- Polygon ohne Stempel: rest_1 (1.16 m²)
- Polygon ohne Stempel: rest_2 (1.15 m²)
- Polygon ohne Stempel: rest_3 (8.53 m²)
- Polygon ohne Stempel: rest_4 (12.22 m²)
- Polygon ohne Stempel: rest_5 (3.53 m²)
- Polygon ohne Stempel: rest_6 (6.56 m²)

## Raumbereinigung (ENIS_UEBERGABE_0908 § 14.6.1)

Überlapper >5 % 0 → 0 · doppelbelegt 0.004 → 0.000000 m² (0.00 mm²) · geändert 2 (Tabelle unten: 2 überlebende) · entfallen 0 · Zerfall 0.000 m² · Schlitzverlust 0.0 mm² · Restkörper entfallener Räume 0.000 m² · Stempelschutz 0

Einträge je Regel: {'SCHWERPUNKT': 2}

Nicht destruktiv: `polygon_roh` hält den Ring vor der Bereinigung, jeder Abzug ist mit Regel und Gegenspieler gebucht. Invariante: Fläche(roh) − Fläche(bereinigt) == Σ der Buchungen.

| id | Name | Quelle | Flag | m² Stempel | m² roh | m² bereinigt | Abw. roh % | Abw. ber. % | Regeln (Gegenspieler) |
|---|---|---|---|--:|--:|--:|--:|--:|---|
| rest_4 | — | R | kein_stempel | — | 12.22 | 12.22 | — | — | SCHWERPUNKT(rest_3) |
| rest_6 | — | R | kein_stempel | — | 6.56 | 6.56 | — | — | SCHWERPUNKT(rest_5) |

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

17 / 18 Türen typisiert. Kürzel: Z=zimmertuer, WE=wohnungseingang, ST=stiegenhaustuer, HE=hauseingang, BT=balkontuer, GT=garagentor, BS=brandschutztuer; ? = untypisiert (keine Regel greift), /NA = Notausgang, * = ohne Türblatt.

| ID | raum_a | raum_b | Typ | Breite mm | Breiten-Quelle | Notausgang | Quelle | Grund |
|---|---|---|---|--:|---|---|---|---|
| tuer_1 | raum_4 | AUSSEN | balkontuer | 790 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_2 | raum_9 | raum_3 | balkontuer | 980 | GEOMETRIE_SCHWENKRADIUS | — | arc |  |
| tuer_3 | KEIN_RAUM | KEIN_RAUM | — | 980 | GEOMETRIE_SCHWENKRADIUS | — | arc | tuer_ins_nichts |
| tuer_4 | raum_2 | rest_3 | wohnungseingang | 940 | GEOMETRIE_SCHWENKRADIUS | — | block |  |
| tuer_5 | rest_3 | raum_10 | stiegenhaustuer | 940 | GEOMETRIE_SCHWENKRADIUS | — | block |  |
| tuer_6 | rest_3 | rest_4 | stiegenhaustuer | 940 | GEOMETRIE_SCHWENKRADIUS | — | block |  |
| tuer_7 | raum_5 | raum_3 | zimmertuer | 840 | GEOMETRIE_SCHWENKRADIUS | — | block |  |
| tuer_8 | raum_8 | rest_5 | wohnungseingang | 840 | GEOMETRIE_SCHWENKRADIUS | — | block |  |
| tuer_9 | rest_6 | rest_5 | wohnungseingang | 840 | GEOMETRIE_SCHWENKRADIUS | — | block |  |
| tuer_10 | rest_5 | raum_3 | wohnungseingang | 840 | GEOMETRIE_SCHWENKRADIUS | — | block |  |
| tuer_11 | raum_10 | raum_4 | wohnungseingang | 840 | GEOMETRIE_SCHWENKRADIUS | — | block |  |
| tuer_12 | rest_4 | rest_3 | stiegenhaustuer | 940 | GEOMETRIE_SCHWENKRADIUS | — | block |  |
| tuer_13 | raum_10 | raum_6 | wohnungseingang | 840 | GEOMETRIE_SCHWENKRADIUS | — | block |  |
| tuer_14 | raum_7 | raum_10 | wohnungseingang | 840 | GEOMETRIE_SCHWENKRADIUS | — | block |  |
| durchgang_1 | raum_1 | raum_10 | wohnungseingang | 1196 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_2 | raum_2 | raum_8 | zimmertuer | 1794 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_3 | raum_2 | rest_5 | wohnungseingang | 1404 | GEOMETRIE_OEFFNUNG | — | durchgang |  |
| durchgang_4 | raum_8 | rest_6 | zimmertuer | 1292 | GEOMETRIE_OEFFNUNG | — | durchgang |  |

## Ausgänge (3)

| ID | Typ | x m | y m |
|---|---|--:|--:|
| exit_tuer_5 | stair_exit | 12551.98 | 356218.22 |
| exit_tuer_6 | stair_exit | 12551.19 | 356219.40 |
| exit_tuer_12 | stair_exit | 12549.40 | 356217.41 |

### Kein Endausgang wegen Freifläche (0 Türen ins Freie an BALKON/TERRASSE)

keine — auf diesem Plan führt keine Tür an einem typisierten BALKON/TERRASSE-Raum vorbei.

## Fluchtweg-Segmente (6)

Quellen: FALLBACK: 1, GRAPH: 5

| Segment | Quelle | Länge m | Grund | Ziel-Ausgang |
|---|---|--:|---|---|
| seg_graph_tuer_4 | GRAPH | 2.5 | exit | exit_tuer_12 |
| seg_graph_tuer_11 | GRAPH | 1.4 | exit | exit_tuer_5 |
| seg_graph_tuer_13 | GRAPH | 5.1 | exit | exit_tuer_5 |
| seg_graph_tuer_14 | GRAPH | 6.7 | exit | exit_tuer_5 |
| seg_graph_durchgang_1 | GRAPH | 6.4 | exit | exit_tuer_5 |
| seg_fallback_rest_4 | FALLBACK | 1.2 | direction_change | — |

## Wohnungen (2)

- top_1: 5 Räume (raum_1, raum_10, raum_4, raum_6, raum_7)
- top_2: 6 Räume (raum_2, raum_3, raum_5, raum_8, rest_5, rest_6)

## Weglänge je Wohnungseingang → nächster Ausgang

| Tür | Weglänge m | Quelle | Ausgang |
|---|--:|---|---|
| tuer_4 | 2.5 | GRAPH | exit_tuer_12 |
| tuer_11 | 1.4 | GRAPH | exit_tuer_5 |
| tuer_13 | 5.1 | GRAPH | exit_tuer_5 |
| tuer_14 | 6.7 | GRAPH | exit_tuer_5 |
| durchgang_1 | 6.4 | GRAPH | exit_tuer_5 |

## Leuchten je Nutzungsklasse

| Klasse | Leuchten |
|---|--:|
| ALLGEMEIN_ERSCHLIESSUNG | 6 |
| kein Raum | 1 |
| _davon auf Treppenlauf/Verbotszone_ | 0 |

## Rotationsprüfung RZ über Tür (Messung, ±2°)

- kein RZ näher als 1 m an einer Tür

## Anker je Stiegenhaus (2 Stiegenhäuser)

- **rest_3**: 3 Läufe, 1 Podeste, 4 Verbotszonen (größte 1.7 m², Summe 2.8 m²), 8 Anker
  - PODEST (12550.36, 356217.78) m, Winkel 59°, Fluchtrichtung 234°
  - AUSTRITT (12550.27, 356219.36) m, Fluchtrichtung 190°
  - ANTRITT (12548.52, 356220.35) m, Fluchtrichtung 188°
  - TUER (12549.97, 356216.20) m, Winkel 149°, Fluchtrichtung 234°
  - TUER (12551.98, 356218.22) m, Winkel 60°, Fluchtrichtung 190°
  - TUER (12551.19, 356219.40) m, Winkel 153°, Fluchtrichtung 190°
  - TUER (12549.40, 356217.41) m, Winkel 90°, Fluchtrichtung 234°
  - RICHTUNGSWECHSEL (12549.77, 356219.91) m, Fluchtrichtung 190°
- **rest_4**: 3 Läufe, 2 Podeste, 3 Verbotszonen (größte 2.2 m², Summe 2.7 m²), 10 Anker
  - PODEST (12551.13, 356219.93) m, Winkel 156°, Fluchtrichtung 188°
  - PODEST (12547.41, 356219.20) m, Winkel 67°, Fluchtrichtung 106°
  - ANTRITT (12550.56, 356220.36) m, Fluchtrichtung 188°
  - ANTRITT (12547.10, 356218.57) m, Fluchtrichtung 106°
  - AUSTRITT (12548.80, 356217.58) m, Fluchtrichtung 188°
  - ANTRITT (12549.34, 356220.88) m, Fluchtrichtung 106°
  - AUSTRITT (12549.45, 356220.51) m, Fluchtrichtung 106°
  - TUER (12551.19, 356219.40) m, Winkel 153°, Fluchtrichtung 188°
  - TUER (12549.40, 356217.41) m, Winkel 90°, Fluchtrichtung 188°
  - RICHTUNGSWECHSEL (12550.00, 356220.43) m, Fluchtrichtung 188°
- Gang-Anker (außerhalb Stiegenhäuser): 7

## Brandschutz-Hinweise im Plan (0)

- keine

## Außenbereich

- Gebäude-Komponenten: 1 (Flächen m²: 191.4; Summe 191.4)
- offene AUSSEN-Flächen: 8 (2.0 m²)
- geschlossene Höfe (AUSSEN_GESCHLOSSEN): 0 (0.0 m²)
- Überdachungen über offener Außenfläche: 0 (0.0 m²)

## Geschoss

- Geschoss: **3OG** (Quelle `dateiname`)
- Beleg: Dateiname 'Rennweg_OG3' → 'OG3'

## Kreuzcheck Fluchtweglinien ↔ Endausgänge

Restweg im EG (Rennweg_EG.dxf): 4.4–9.9 m (Stiegenhaustür → nächster final_exit)

0 Linien-Endpunkte an der Außenkante, davon 0 mit final_exit ≤ 1.5 m gedeckt.

### Unbestimmte Räume (§ 6g)

- ⚠ unbestimmt: raum_10 — R1: Wohnungsflur hinter Stiegenhaustür — gehört zur Wohnung, ist kein Beleg für eine eigene Wohnung; Notlicht bleibt, Owner 2026-09-27

### Untypisierte Türen — Gründe

| Grund | Anzahl |
|---|--:|
| tuer_ins_nichts | 1 |

Laufzeit: 47.4 s
