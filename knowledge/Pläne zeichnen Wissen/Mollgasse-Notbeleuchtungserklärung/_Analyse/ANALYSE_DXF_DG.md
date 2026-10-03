# ANALYSE DXF — Mollgasse DG

Quelle: `Mollgasse-Notbeleuchtungserklärung\WHA_MOL_DG_Notbeleuchtung_Erklärung.dxf` · 6 Leuchten (0 beidseitig-Gruppen) · 9 Personen · 20 Sichtlinien · 23 Fluchtweg-Elemente · 15 Kennungs-Texte · 0 gelbe Marker.

Messkonvention: Position = Bbox-Zentrum der sichtbaren Geometrie (virtual_entities, NB-R00); Welt-Pfeil = Blockbasis (down 270/left 180/right 0) + Rotation, xscale<0 spiegelt. Engine-heute-Spalte = Validierungslauf 2026-09-29 (leerer Input, pipeline.run, Paarungs-Radius 3 m).

## Leuchten

| Handle | Block | Kennung | xy (Bbox) | rot | xscale | Welt-Pfeil | beids. | PDF-Beleg | Tür-Bezug | Engine heute |
|---|---|---|---|---|---|---|---|---|---|---|
| 206D6 | RIVO-SIBEL-ARR-down | (D) | (-16047, 28414) | 269.71° | 35.6373 | 179.7° |  | — | — | FEHLT (Engine setzt hier nichts ≤3 m) |
| 206DB | RIVO-SIBEL-ARR-left | (B) | (-17184, 26892) | 359.42° | 36.0983 | 179.4° |  | — | — | FEHLT (Engine setzt hier nichts ≤3 m) |
| 206DC | RIVO-RZ-ARR_right | (A) | (667, 26391) | 359.87° | 1.3724 | 359.9° |  | S.39 (DG-01, praezisiert) | 1797 mm von Top-20-Tuer 1FC7A (1762,24966) entfernt - bewusst nicht… | gepaart (932 mm, Typ ≠) |
| 20705 | RIVO-SIBEL-ARR-left | (B) | (4697, 28336) | 359.42° | 36.0983 | 179.4° |  | S.39 (DG-01, praezisiert) | wandbuendig Nordwand (y=28497), 561 mm zur Ostwand | gepaart (2771 mm, Typ ≠) |
| 2083F | RIVO-SIBEL-ARR-left | (A) | (40303, -1717) | 359.42° | 36.0983 | 179.4° |  | S.40 (DG-02, praezisiert) | 458 mm noerdlich des Top-28-Labels (Versatz 'Richtung Top 28') | FEHLT (Engine setzt hier nichts ≤3 m) |
| 20864 | RIVO-SIBEL-ARR-down | (DG) | (36956, -59) | 269.71° | 35.6373 | 179.7° |  | S.40 (DG-02, praezisiert) | nicht tuergebunden | FEHLT (Engine setzt hier nichts ≤3 m) |

**6/6 Leuchten sind im PDF erklärt/vermessen; 0 ohne expliziten PDF-Beleg** — diese folgen den Basis-Regeln (Typ + Welt-Pfeil oben dokumentiert; Bewertung: Typ-Familie und Rotation liegen innerhalb der belegten Muster, kein Widerspruchsfall darunter).

## Personen (grüne Läufer, Block 750298750/9809550)

| Handle | xy | rot | xscale | Blick (Regel #8: 180°+rot bei xscale>0) |
|---|---|---|---|---|
| 206D8 | (634, 25540) | 92.75° | -4.0068 | 92.75° |
| 20780 | (2335, 26341) | 2.75° | -4.0068 | 2.75° |
| 207CB | (4129, 27812) | 356.98° | 4.0068 | 176.98° |
| 2083C | (40578, -2545) | 92.75° | -4.0068 | 92.75° |
| 208D8 | (39030, 841) | 272.75° | -4.0068 | 272.75° |
| 208FE | (39388, -1747) | 356.85° | 4.0068 | 176.85° |
| 20900 | (36364, -1704) | 356.85° | 4.0068 | 176.85° |
| 20902 | (38654, -50) | 2.89° | -4.0068 | 2.89° |
| 20904 | (35561, -42) | 2.89° | -4.0068 | 2.89° |

## Linien & Marker

- **Sichtlinien (türkis, ACI 4):** 20 — Start→Ende: 20265 (36254,1024)→(36254,1024); 20266 (36254,824)→(36305,1024); 20267 (-393,27705)→(-393,27705); 20268 (-193,27704)→(-392,27756); 20297 (39704,-6820)→(39704,-7020); 20298 (39704,-7020)→(39904,-6820); 20304 (1685,23414)→(1885,23413); 20305 (1684,23214)→(1885,23413); 20336 (1239,24117)→(1239,24117); 20337 (1339,24116)→(1339,24116); 20338 (1239,24117)→(1338,23916); 20339 (1339,24116)→(1437,23766)…
- **Fluchtweg (grün):** 23 Elemente (Polylines + Pfeilspitzen `Fluchtwegpfeil`/`4444444`)
- **Gelbe Marker:** 0

## PDF↔DXF-Abgleich

Erklärte Leuchten decken sich mit den PDF-Angaben (Phase-B-Vermessung `beispiele.json`, Spalten PDF-Beleg/Tür-Bezug oben). Abweichungsfälle aller Geschosse: siehe `ABWEICHUNGEN_PDF_DXF.md`.