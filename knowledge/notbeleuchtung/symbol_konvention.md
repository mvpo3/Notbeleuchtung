# Symbol-Konvention — PDF-Begriffe ↔ Symbol-Registry ↔ Rotationslogik

Quelle der Registry: `src/notbeleuchtung/symbols/schrack_symbol_mapping.yaml`
(catalog_key → Blockname + `scale_abs`) + `src/notbeleuchtung/symbols/orientation.py`
(`_BLOCK_BASE_DEG` = gemessene Basisorientierung). Migration: Phase A 2026-09-18,
`docs/SYMBOL_MIGRATION_2026-09-18.md`. PDF = „Notbeleuchtungen zeichnen"
(41 S., Owner, Mollgasse-Beispiele).

## PDF-Begriff ↔ Block ↔ lokaler Pfeilvektor

| PDF-Begriff | Block (Bibliothek Notbeleuchtungssymbole_neu+.dxf) | catalog_key | Pfeilvektor bei rot 0 | Basis |
|---|---|---|---|---|
| „RZ / Notleuchte mit Pfeil nach unten" | `RIVO-SIBEL-ARR-down` | notlicht_ks_stiege / _unten / notlicht_kw_garage | (0,−1) | 270° |
| „Notleuchte mit Pfeil nach links" | `RIVO-SIBEL-ARR-left` | notlicht_ks_stiege_links | (−1,0) | 180° |
| „Notleuchte mit Pfeil nach rechts" | `RIVO-RZ-ARR_right` | notlicht_ks_stiege_rechts | (+1,0) | 0° |
| „Antipanikleuchte" | `Antipanikleuchte-RIVO` | antipanik_leuchte | — (richtungslos) | — |
| „Aufheller" | `Aufheller Notbeleuchtung` (blauer Vollkreis) | sicherheitsleuchte_aufheller | — | — |
| „Spot-Aufheller" (Vorlagen-Legende) | `Spot Notbeleuchtung` | sicherheitsleuchte_spot | — | — |
| „Gruppenbatterie-Verteiler" | `Gruppenbatterie-Verteiler` | gruppenbatterie_anlage | — | — |
| Menschensymbol (grün, Erklärungspläne) | `750298750` (Füllung) über `9809550` (Kontur) | — (kein Engine-Symbol) | Blickrichtung aus INSERT-Rotation | — |
| Fluchtweg-Richtungspfeil (grün, Erklärungspläne) | `4444444` | — (kein Engine-Symbol) | Pfeilrichtung aus INSERT-Rotation | — |

Kein eigener Block existiert für: „Haupteingang/Ausgang" (= Pfeil-unten-Schild über
der Haupteingangstür, PDF S.1/S.6) und „RZ-beidseitig" (Vorlagen-Legende
komponiert 2× left, eine Instanz gespiegelt). Siehe `offene_fragen.md` #1/#2.

## Rotationslogik (der EINE Rahmen)

Welt-Pfeilrichtung eines gesetzten RZ = **Basis des Blocks + INSERT-Rotation**
(CCW, 0° = +x = „rechts"). `orientation.transformation(catalog_key, richtung)`
liefert `(ziel − basis) % 360`; Spiegelung ist nie nötig (alle drei Basen sind
eigene Blöcke). Ziel-Winkel: rechts 0°, oben 90°, links 180°, unten 270°.

Die Owner-Erklärungspläne bestätigen das Muster: das down-Schild kommt dort mit
Rotationen 0/90/180/270 vor (alle Richtungen aus EINEM Block gedreht), left/right
ergänzen, wo die Frontalsicht es verlangt (PDF S.31–37: die Person muss die
VORDERSEITE sehen — Auswahl links/rechts/unten folgt aus Fluchtrichtung UND
Blickwinkel, nicht aus der Richtung allein).

## Größen (Owner-kalibriert, `scale_abs`)

RZ-Schilder ≈ 636 mm Weltbreite · Antipanik ≈ 539 mm · Aufheller/Spot ≈ 97 mm Ø ·
SV-Anlage ≈ 430 mm — dominante INSERT-Skalen der Erklärungspläne (alle 6 Geschosse
gemessen); Zweitgrößen (446-mm-RZ, 296-mm-Antipanik) siehe `offene_fragen.md` #5/#6.

## Farb-Semantik der Erklärungspläne („Erscheinungsbild ist Wahrheit")

grüne Linie + grüne Pfeile (`4444444`) = Fluchtweg + Richtung · grüne Menschen
(`750298750`, rotiert) = Bewegungs-/Blickrichtung = Ground Truth des Fluchtwegs ·
türkis = Sichtlinie Person→Leuchte · rot = nachgezeichneter Stiegenhauspfeil
(Original grau, in Stiegenfarbe) · blau = Hindernis (z.B. Lichtkuppel, PDF S.40).
