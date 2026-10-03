# ANALYSE DXF — Mollgasse 3OG

Quelle: `Mollgasse-Notbeleuchtungserklärung\WHA_MOL_3OG_Notbeleuchtung_Erklärung.dxf` · 4 Leuchten (0 beidseitig-Gruppen) · 13 Personen · 6 Sichtlinien · 37 Fluchtweg-Elemente · 17 Kennungs-Texte · 0 gelbe Marker.

Messkonvention: Position = Bbox-Zentrum der sichtbaren Geometrie (virtual_entities, NB-R00); Welt-Pfeil = Blockbasis (down 270/left 180/right 0) + Rotation, xscale<0 spiegelt. Engine-heute-Spalte = Validierungslauf 2026-09-29 (leerer Input, pipeline.run, Paarungs-Radius 3 m).

## Leuchten

| Handle | Block | Kennung | xy (Bbox) | rot | xscale | Welt-Pfeil | beids. | PDF-Beleg | Tür-Bezug | Engine heute |
|---|---|---|---|---|---|---|---|---|---|---|
| 78D92 | RIVO-RZ-ARR_right | (A) | (-1784516, 16068) | 359.87° | 1.3724 | 359.9° |  | S.27 (3OG-01, bestaetigt+praezisiert) | 2073 mm von Tuermitte Top16+17 (00-top h=78789), am Fluchtweg-Knick… | FEHLT (Engine setzt hier nichts ≤3 m) |
| 78DB5 | RIVO-SIBEL-ARR-left | (B) | (-1781086, 17879) | 359.42° | 36.0983 | 179.4° |  | S.27 (3OG-01, bestaetigt+praezisiert) | — | FEHLT (Engine setzt hier nichts ≤3 m) |
| 78DDA | RIVO-SIBEL-ARR-left | (B) | (-1743996, -11979) | 359.42° | 36.0983 | 179.4° |  | S.29 (3OG-02, bestaetigt+praezisiert) | keine Einzeltuer: bedient 4 Wohnungstueren (naechste Top 18+19 in 2… | FEHLT (Engine setzt hier nichts ≤3 m) |
| 78DFD | RIVO-SIBEL-ARR-down | (A) | (-1750373, -10572) | 269.71° | 35.6373 | 179.7° |  | — | — | gepaart (1262 mm, Typ ok) |

**4/4 Leuchten sind im PDF erklärt/vermessen; 0 ohne expliziten PDF-Beleg** — diese folgen den Basis-Regeln (Typ + Welt-Pfeil oben dokumentiert; Bewertung: Typ-Familie und Rotation liegen innerhalb der belegten Muster, kein Widerspruchsfall darunter).

## Personen (grüne Läufer, Block 750298750/9809550)

| Handle | xy | rot | xscale | Blick (Regel #8: 180°+rot bei xscale>0) |
|---|---|---|---|---|
| 78E28 | (-1785563, 14067) | 258.27° | 4.0068 | 78.27° |
| 78EE9 | (-1784497, 14698) | 258.27° | 4.0068 | 78.27° |
| 78F0D | (-1782723, 15955) | 11.46° | -4.0068 | 11.46° |
| 78F78 | (-1780651, 17406) | 342.38° | 4.0068 | 162.38° |
| 78F9D | (-1782218, 17380) | 342.38° | 4.0068 | 162.38° |
| 78FE6 | (-1784415, 17400) | 72.22° | 4.0068 | 252.22° |
| 79052 | (-1781855, 15955) | 11.46° | -4.0068 | 11.46° |
| 79084 | (-1752529, -12045) | 258.27° | 4.0068 | 78.27° |
| 792FF | (-1752398, -9384) | 281.73° | -4.0068 | 281.73° |
| 79325 | (-1743960, -9633) | 281.73° | -4.0068 | 281.73° |
| 7936F | (-1744728, -14760) | 258.27° | 4.0068 | 78.27° |
| 79394 | (-1743174, -13178) | 101.86° | -4.0068 | 101.86° |
| 793BA | (-1743996, -16436) | 101.86° | -4.0068 | 101.86° |

## Linien & Marker

- **Sichtlinien (türkis, ACI 4):** 6 — Start→Ende: 78FE8 (-1785293,14101)→(-1784561,15909); 79301 (-1752253,-12013)→(-1752129,-9417); 79327 (-1743691,-9666)→(-1744041,-11813); 79370 (-1744458,-14726)→(-1744002,-12122); 79396 (-1743443,-13145)→(-1743977,-12138); 793BC (-1744265,-16403)→(-1743977,-12138)
- **Fluchtweg (grün):** 37 Elemente (Polylines + Pfeilspitzen `Fluchtwegpfeil`/`4444444`)
- **Gelbe Marker:** 0

## PDF↔DXF-Abgleich

Erklärte Leuchten decken sich mit den PDF-Angaben (Phase-B-Vermessung `beispiele.json`, Spalten PDF-Beleg/Tür-Bezug oben). Abweichungsfälle aller Geschosse: siehe `ABWEICHUNGEN_PDF_DXF.md`.