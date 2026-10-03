# SYMBOLE_UND_LAYER — Block-/Layer-Inventur der 5 Referenzprojekte

Stand: 2026-09-29 · Quelle: `scripts/inventur_dxf.py` → `evidenz/inventur.json`
(23 DXFs, alle lesbar, 0 Lesefehler). Version 1 — wird nach P1/P2 (visuelle
Verifikation) verfeinert.

## Alias-Tabelle Leuchten-Blöcke (datengetrieben)

| Kanonischer Typ | Mollgasse (P1, BASIS) | Tomaschek (P2) | Am Rain (P3) | Hausfeld (P4) | Baufeld E2 (P5) |
|---|---|---|---|---|---|
| RZ Pfeil unten | `RIVO-SIBEL-ARR-down` (46) | `RIVO_ARR_down` (34) + `RIVO_ARR_down0` (26) | `RIVO_ARR_down` (58) | `RIVO_ARR_down` (25) | `RIVO_ARR_down` (61) |
| RZ Pfeil links | `RIVO-SIBEL-ARR-left` (33) | `RIVO_ARR_left` (11+1) | `RIVO_ARR_left` (13) | `RIVO_ARR_left` (22) | `RIVO_ARR_left` (12) |
| RZ Pfeil rechts | `RIVO-RZ-ARR_right` (16) | `RIVO_ARR_right` (3+1) | `RIVO_ARR_right` (9) | `RIVO_ARR_right` (11) | `RIVO_ARR_right` (9) |
| RZ beidseitig | — (als 2er-Cluster gestapelter Einzel-RZ, s. GT-Extraktor) | `RIVO_ARR_bothsided` (13+8) | `RIVO_ARR_bothsided` (41) | — | `RIVO_ARR_bothsided` (7) |
| Antipanik | `Antipanikleuchte-RIVO` (10) | `RIVO_Antipanik` (3+15) | — | `RIVO_Antipanik` (6) | — |
| Aufheller | — | `RIVO_Aufheller` (3+1), `RIVO_Aufheller_Variante` (39+16) | — | `RIVO_Aufheller_Variante` (3) | — |
| Anlage/Verteiler | `Gruppenbatterie-Verteiler` (2) | `RIVO_Gruppenbatterie_Verteiler` (3+1) | `SiBel Zentrale-*` (5, Fremd) | — | — |

Anmerkungen:
- **Tomaschek `*0`-Suffix**: Duplikat-Blockdefinitionen (`RIVO_ARR_down0` etc.) —
  vermutlich Copy-Import-Artefakt; im Extraktor als Alias auf den Grundtyp mappen.
- **Am Rain Zweitwelt**: `SIMA_ET_SIBEL_Sicherheitsleuchte` (45) + Layer
  `SIMA_ET_SiBel_Symbol` = fremde SIMA-Welt → **IGNORIEREN** (bestätigt in
  `knowledge/extracted/AM_RAIN_NOTBELEUCHTUNG_ANALYSE.md` §8).
- **Mollgasse trägt ALT-Blocknamen** (`RIVO-SIBEL-ARR-*`, `RIVO-RZ-ARR_right`) —
  identisch zur GT-Extraktor-Behandlung (`scripts/analyse/mollgasse_gt_extract.py`);
  xscale<0 spiegelt left↔right!
- `Fluchtwegpfeil` (Mollgasse, 265×) = grüner Fluchtweg-Verlaufspfeil
  (Lehrelement, keine Leuchte).

## Lehr-/Markup-Elemente je Projekt

| Element | Mollgasse | Tomaschek | Am Rain | Hausfeld | Baufeld E2 |
|---|---|---|---|---|---|
| Person (grün) | Block `750298750` (HATCH aci:3 grün + nested INSERT `9809550`); alles auf Layer `0` | **KEINE Personen-Blöcke im DXF** (Inventur+Grün-Scan leer — PDF klärt) | (offen) | Layer `HF_LEHR_<G>-S##_MENSCHEN` | Block `E2_MOL_LEHRPERSON_ZENTRIERT` (118) auf `E2_LEHR_MENSCH_NATIVE` |
| Blickwinkel/Sichtlinie (türkis) | ACI-4-LINEs auf Layer 0 (EG nur 1; KG-Geschosse 124/230 — UG-Kapitel!) | Layer `RIVO_ERK_SICHTLINIE` (LINE 80 + LWPOLYLINE 10 je Geschoss) | **0 gefunden** (TEILSTAND ohne Lehrlinien) | Layer `HF_LEHR_<G>-S##_SICHT` | Layer `E2_LEHR_WEG_B_INTERPRETATION` = 269 **SOLID**-Keile |
| Fluchtweg-Linie (grün) | Block `Fluchtwegpfeil` + Block `4444444` (= grüne Pfeilspitze, **Crop-verifiziert 2026-09-29**, kein Keil!) + grüne Polylines | Layer `RIVO_ERK_FLUCHTWEG` (LINE/LWPOLYLINE/TEXT) | **0 gefunden** (TEILSTAND) | Layer `HF_LEHR_<G>-S##_WEGE` | Layer `681 Fluchtlinien` |
| Kennungen/Buchstaben (A),(B)… | (offen — Texte auf Layer 0) | (offen) | (offen) | Layer `HF_LEHR_<G>-S##_KENNUNGEN` | `E2_LEHR_KENNUNG` |
| Hinweise/Notizen | (offen) | (offen) | (offen) | Layer `HF_LEHR_<G>-S##_HINWEISE` | — |

**Hausfeld-Goldader:** Lehr-Layer sind SZENEN-indiziert
(`HF_LEHR_HF-<Geschoss>-S<NN>_<Kategorie>`, S01–S13 je Geschoss) — die Szenen-
Nummern korrespondieren mutmaßlich 1:1 mit den PDF-Bildern → maschinelles
Bild↔DXF-Matching möglich (in P2 verifizieren).

## Produktions-Layer (Leuchten)

- Mollgasse: alle Symbole auf Layer `0` (Erklär-Dateien, eigene Blockdefs).
- Tomaschek/Am Rain: `din_SIBEL_10_emergency_lighting` (+ `_yellow`-Zwilling,
  `_11_…_system` für Anlage) — din-Konvention.
- Baufeld E2: `dp_GE_SIBEL` (81).
- Hausfeld: (offen — Symbole liegen vermutlich auf eigenem Layer, P1 klärt.)

## Offene Verifikationen (→ P1/P2)

1. Mollgasse `4444444` = Blickwinkel-Keil? (Crop-Verifikation; Zählung EG 63 ≈
   Personen 51 + x). `9809550` (aus beispiele.json bekannt) in welchen Geschossen?
2. Tomaschek/Am Rain Personen-Blöcke identifizieren (kein Name-Hint-Treffer).
3. Gelbe Diagonale/Kreise (Antipanik-Mitte, Alternativ-Positionen): Layer/Farbe
   je Projekt suchen (aci gelb=2/tc-Gelbtöne), Mollgasse vermutlich Layer 0.
4. Hausfeld Szenen-Nummern ↔ PDF-Seiten-Mapping.
5. Am Rain: Sichtlinien vorhanden? (TEILSTAND v1/v2 — evtl. ohne Lehrlinien.)

## Datei-Protokoll

- Alle 23 Muster-DXFs vorhanden und lesbar (0 Fehler).
- Am Rain EG doppelt (`EG_Erklaerung` + `RIVO_Symbole`, 72k Entities je) —
  beide inventarisiert; Erklär-Analyse nutzt `EG_Erklaerung`, Übrige `RIVO_Symbole`.
- Mollgasse DG: nur `.dxf` genutzt (`.dwg`-Zwilling ignoriert), `.bak` ignoriert.
- Am Rain: zusätzlich `…Alle_Geschosse_RIVO_Zusammenfuehrung_TEILSTAND_v2.dxf`
  (Sammel-Datei) — NICHT im Muster, bewusst ausgelassen (Dubletten-Gefahr).
