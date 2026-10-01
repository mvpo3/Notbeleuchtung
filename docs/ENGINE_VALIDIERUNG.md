# ENGINE_VALIDIERUNG — Engine vs. Referenz-DXFs (5 Projekte, 2026-09-29)

Auftrag „Wissensaufbau" Schritt 5.4. Werkzeuge:
`scripts/analyse/mollgasse_gt_vergleich.py` (erweitert: Typ-Match je Paar +
ERREICHBAR-Messmodus) und `knowledge/…/_Analyse_Regelwerk/scripts/
projekt_gt_vergleich.py` (Projekte 2–5, gleiche Metriken). Metriken:
- **gepaart** = GT-Leuchte hat Engine-Partner gleicher Klasse ≤ 3 m
  (reiner Paarungs-Radius, keine Pass-Toleranz; Distanzen metrisch berichtet).
- **Typ-Match** = Richtungs-Familie (down/left/right), beidseitig↔beidseitig
  bzw. Klassen-Match SL/AP.
- **ERREICHBAR** = Nenner nur GT-Leuchten, die in einem ERKANNTEN Raum-Polygon
  liegen oder ≤ 1,5 m an erkannter Zirkulation — misst die Platzierungslogik
  fair gegen Selman-Erkennungs-Lücken. (Kriterium ist großzügig: ein erkanntes
  Polygon ohne Zirkulation zählt erreichbar, obwohl der Platzierer dort ohne
  Fluchtweg nichts setzen kann — der echte Platzierungs-Anteil liegt also
  ZWISCHEN beiden Quoten.)

## Projekt 1 — Mollgasse (verbindlich)

| G | GT | gepaart | Typ-Match | erreichbar gepaart | fehlt | überflüssig | Median mm |
|---|---|---|---|---|---|---|---|
| EG | 17 | 5 | 3 | 4/15 | 12 | 48 | 1240 |
| 1OG | 11 | 4 | 2 | 4/10 | 7 | 8 | 1421 |
| 2OG | 11 | 4 | 1 | 4/10 | 7 | 10 | 1292 |
| 3OG | 4 | 1 | 1 | 1/2 | 3 | 8 | 1262 |
| 4OG | 7 | 5 | 1 | 4/5 | 2 | 9 | 959 |
| DG | 6 | 2 | 0 | 1/3 | 4 | 6 | 1851 |
| 1KG | 12 | 3 | 0 | 2/10 | 9 | 11 | 1621 |
| 2KG | 29 | 9 | 5 | 9/28 | 20 | 15 | 2024 |
| **Σ** | **97** | **33 (34 %)** | **13** | **29/83 (35 %)** | **64** | **115** | — |

**Das 95-%-Ziel ist NICHT erreicht — in keiner Metrik.** Ehrliche Attribution:

1. **Erkennungs-Lücken (Selman-Naht, bekannt seit GT-Bericht 2026-09-20):**
   14/97 GT-Leuchten liegen außerhalb jedes erkannten Polygons (Kellerabteil-
   Gänge, Garage). Zusätzlich: erkannte Polygone OHNE Zirkulation (Garage,
   KG-Gänge) zählen im erreichbar-Nenner mit, sind aber ohne Fluchtweg-Segment
   nicht bespielbar → Pakete **S-KG** (Kellerabteile/Garage/Gebäudehälften)
   und **S-W** bleiben der größte Hebel (an Selman übergeben, `8257ff9`).
2. **Positions-Konvention:** Median-Distanzen 1–2 m bei den Paaren = Engine
   platziert an Ankern/Segment-Enden, der Owner auf Bestandslinien-/Gangmitte-
   Konstruktionen (NB-R05-Parameter 800–1122 mm, Diagonale RW-029). Kandidat:
   Nachpass-Slice „Owner-Positions-Konventionen" (braucht Owner-GO, verschiebt
   Golden/GT-Freezes).
3. **beidseitig 0/8** (Wasserscheiden-Spots ohne durchgehende Zirkulation —
   NB-R16 ist gebaut, feuert aber ohne Graph-Pfad nicht).
4. **Überproduktion 115** (EG 48 = Aufheller-Lane; D1-Bremsen greifen, aber
   Owner-Soll ist nochmals dünner — Kalibrier-Slice S4 offen).

## Projekte 2–5 (KONFLIKTE-rückführbare Abweichungen zählen nicht als Fehler)

| Projekt | G | GT | gepaart | Typ | erreichbar | überfl. | Befund |
|---|---|---|---|---|---|---|---|
| Hausfeld | EG | 13 | 6 | 5 | 5/10 | 11 | läuft |
| Hausfeld | 1OG | 7 | 6 | 0 | 6/7 | 6 | beste Paar-Quote 86 % |
| Hausfeld | 1DG | 7 | 4 | 2 | 4/7 | 8 | läuft |
| Hausfeld | 2DG | 3 | 3 | 1 | 3/3 | 6 | **100 % gepaart** |
| Hausfeld | UG | — | — | — | — | — | Frame nicht auflösbar (keine gemeinsamen Architektur-INSERTs leer↔RIVO-GT) |
| Am Rain | alle 6 | — | — | — | — | — | **Erkennung: „Keine Wand-Entities gefunden"** — ARAI5-Dialekt fehlt im Parser (Selman-Naht; kein Platzierungs-Befund) |
| Tomaschek | EG | 52 | 4 | 2 | 4/21 | 20 | Schule: Klassenraum-Muster (RW-104) nicht gebaut → systematisch dünn |
| Tomaschek | OG | 47 | 5 | 2 | 3/17 | 19 | dito |
| Tomaschek | SG | 74 | 7 | 5 | 6/27 | 40 | dito; **kein Crash** (Schul-Klasse läuft erstmals durch die Engine) |
| Baufeld E2 | UG | 89 | **26** | 13 | 26/88 | 20 | bester Fremd-Lauf; Wohnbau-Muster trägt |

## Regelbezogene Einzel-Validierung

- `tests/platzierung/test_regelwerk_belege.py`: **35/35 Basis-Regeln** mit real
  existierendem DXF-Beleg-Handle (parametrisiert, grün).
- Baufeld E2 (nur DXF, Basis-Regel-Bewertung je Leuchte,
  `ANALYSE_BaufeldE2.md`): **87/89 Leuchten regelkonform** (B1 Front-zum-
  Menschen + B2 Blickkeil), 2 Prüffälle → KONFLIKTE.md P-01/P-02.
- Mollgasse-Regressions-Freezes (`tests/naht/test_mollgasse_gt.py`)
  unverändert grün — der Regelwerk-Einbau hat KEINE Platzierung verschoben
  (Kennzahlen identisch zum GT-Bericht 2026-09-20: 33/97/115).

## Nächste Hebel Richtung 95 % (Priorität)

1. Selman S-KG/S-W-Pakete (Zirkulation KG/Garage, Wohnungs-Stopp) → hebt
   erreichbar-Nenner UND beidseitig-Spots.
2. AmRain-Wand-Dialekt (ARAI5) in die Erkennung (Selman).
3. Owner-Positions-Konventions-Slice (Bestandslinie/Gangmitte/NB-R05-Band als
   Nachpass) — Owner-GO nötig, verschiebt Freezes.
4. Schul-Muster RW-104 (braucht Raumtyp KLASSENRAUM).
5. Aufheller-Kalibrierung S4 (Überproduktion EG).
