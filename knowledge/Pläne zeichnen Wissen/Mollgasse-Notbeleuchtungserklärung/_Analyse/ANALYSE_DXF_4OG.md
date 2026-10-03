# ANALYSE DXF — Mollgasse 4OG

Quelle: `Mollgasse-Notbeleuchtungserklärung\WHA_MOL_4OG_Notbeleuchtung_Erklärung.dxf` · 7 Leuchten (0 beidseitig-Gruppen) · 17 Personen · 6 Sichtlinien · 39 Fluchtweg-Elemente · 24 Kennungs-Texte · 0 gelbe Marker.

Messkonvention: Position = Bbox-Zentrum der sichtbaren Geometrie (virtual_entities, NB-R00); Welt-Pfeil = Blockbasis (down 270/left 180/right 0) + Rotation, xscale<0 spiegelt. Engine-heute-Spalte = Validierungslauf 2026-09-29 (leerer Input, pipeline.run, Paarungs-Radius 3 m).

## Leuchten

| Handle | Block | Kennung | xy (Bbox) | rot | xscale | Welt-Pfeil | beids. | PDF-Beleg | Tür-Bezug | Engine heute |
|---|---|---|---|---|---|---|---|---|---|---|
| 4121F | RIVO-RZ-ARR_right | (B) | (-75940, 32585) | 359.87° | 1.3724 | 359.9° |  | S.32 (4OG-02, praezisiert) | — | gepaart (933 mm, Typ ≠) |
| 41220 | RIVO-SIBEL-ARR-left | (C) | (-72424, 34451) | 359.42° | 36.0983 | 179.4° |  | S.32 (4OG-02, praezisiert) | — | gepaart (1187 mm, Typ ≠) |
| 41249 | RIVO-SIBEL-ARR-left | (A) | (-75884, 30933) | 269.42° | 36.0983 | 89.4° |  | S.31 (4OG-01, praezisiert) | Front zu den Wohnungstueren Top 18/19 im Westen | FEHLT (Engine setzt hier nichts ≤3 m) |
| 413A0 | RIVO-SIBEL-ARR-down | (A) | (-35385, 8592) | 179.71° | 35.6373 | 89.7° |  | S.33 (4OG-03, bestaetigt) | — | gepaart (959 mm, Typ ≠) |
| 413E8 | RIVO-SIBEL-ARR-down | (DG) | (-39711, 6006) | 269.71° | 35.6373 | 179.7° |  | S.38 (4OG-07, widerspruch) | — | gepaart (1812 mm, Typ ok) |
| 41593 | RIVO-SIBEL-ARR-left | (B) | (-35752, 4564) | 359.42° | 36.0983 | 179.4° |  | S.38 (4OG-07, widerspruch) | — | FEHLT (Engine setzt hier nichts ≤3 m) |
| 415B6 | RIVO-RZ-ARR_right | (C) | (-42976, 4646) | 89.87° | 1.3724 | 89.9° |  | S.38 (4OG-07, widerspruch) | — | gepaart (934 mm, Typ ≠) |

**7/7 Leuchten sind im PDF erklärt/vermessen; 0 ohne expliziten PDF-Beleg** — diese folgen den Basis-Regeln (Typ + Welt-Pfeil oben dokumentiert; Bewertung: Typ-Familie und Rotation liegen innerhalb der belegten Muster, kein Widerspruchsfall darunter).

## Personen (grüne Läufer, Block 750298750/9809550)

| Handle | xy | rot | xscale | Blick (Regel #8: 180°+rot bei xscale>0) |
|---|---|---|---|---|
| 41222 | (-77372, 29702) | 101.86° | -4.0068 | 101.86° |
| 41277 | (-78494, 30632) | 11.86° | -4.0068 | 11.86° |
| 412FF | (-75938, 31795) | 101.86° | -4.0068 | 101.86° |
| 41301 | (-73668, 32586) | 11.86° | -4.0068 | 11.86° |
| 41303 | (-73882, 33992) | 347.88° | 4.0068 | 167.88° |
| 41329 | (-75949, 33726) | 77.54° | 4.0068 | 257.54° |
| 4132D | (-75182, 32571) | 11.86° | -4.0068 | 11.86° |
| 4137B | (-34559, 3514) | 101.86° | -4.0068 | 101.86° |
| 4140D | (-35693, 2844) | 101.86° | -4.0068 | 101.86° |
| 41433 | (-36191, 10554) | 304.09° | -4.0068 | 304.09° |
| 41458 | (-35363, 11437) | 304.09° | -4.0068 | 304.09° |
| 41486 | (-35418, 7188) | 304.09° | -4.0068 | 304.09° |
| 41488 | (-41537, 5848) | 2.75° | -4.0068 | 2.75° |
| 414AD | (-38375, 5961) | 2.75° | -4.0068 | 2.75° |
| 414D2 | (-36506, 4573) | 356.98° | 4.0068 | 176.98° |
| 414D4 | (-39386, 4580) | 356.98° | 4.0068 | 176.98° |
| 414D7 | (-37945, 4576) | 356.98° | 4.0068 | 176.98° |

## Linien & Marker

- **Sichtlinien (türkis, ACI 4):** 6 — Start→Ende: 41280 (-78462,30901)→(-76043,30934); 41281 (-77641,29735)→(-76027,30939); 4132E (-76225,33702)→(-75917,32744); 4140F (-35962,2876)→(-34829,3546); 4145A (-35898,10638)→(-35070,11520); 41645 (-42816,4806)→(-39474,4852)
- **Fluchtweg (grün):** 39 Elemente (Polylines + Pfeilspitzen `Fluchtwegpfeil`/`4444444`)
- **Gelbe Marker:** 0

## PDF↔DXF-Abgleich

Erklärte Leuchten decken sich mit den PDF-Angaben (Phase-B-Vermessung `beispiele.json`, Spalten PDF-Beleg/Tür-Bezug oben). Abweichungsfälle aller Geschosse: siehe `ABWEICHUNGEN_PDF_DXF.md`.