# Übersicht — Fischamend_BT2_EG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\BVH Fischamenderstraße\BT2\260320_938-AR-PP-21000-A_ERDGESCHOSS BT2.dxf` · Geschoss: `EG` · Bild: 1800×1776 px · Laufzeit 45.8 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 14 |
| Sanitär (BAD/WC) | 9 |
| sonstige typisierte Räume | 8 |
| Außenflächen (BALKON/TERRASSE) | 6 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 8 |
| Stiegenhäuser | 1 |
| Schächte/Lifte | 2 |
| untypisierte Räume (nicht erkannt) | 7 |
| Innenhöfe (geschlossene Außenflächen) | 1 |
| Wohnungen | 1 |
| Ausgänge final_exit | 4 |
| Ausgänge stair_exit | 2 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 55 |
| Räume > 90 % in anderem Raum | 14 |

Räume gesamt: **55**, davon typisiert 48.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| KÜCHE | 8 |
| ZIMMER | 6 |
| WC | 5 |
| BAD | 4 |
| GANG | 4 |
| TERRASSE | 4 |
| VORRAUM | 4 |
| ABSTELLRAUM | 2 |
| BALKON | 2 |
| GARAGE | 2 |
| TECHNIK | 2 |
| KINDERWAGENRAUM | 1 |
| LIFT | 1 |
| MUELLRAUM | 1 |
| SCHACHT | 1 |
| STIEGENHAUS | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 27 |

Räume ohne `wohnung_id`: 28

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_1 | KÜCHE | raum_49 | KÜCHE | 100.0 % |
| raum_2 | KÜCHE | raum_48 | KÜCHE | 99.6 % |
| raum_7 | TERRASSE | raum_49 | KÜCHE | 100.0 % |
| raum_8 | KÜCHE | raum_49 | KÜCHE | 99.5 % |
| raum_12 | ZIMMER | raum_49 | KÜCHE | 100.0 % |
| raum_13 | ZIMMER | raum_49 | KÜCHE | 100.0 % |
| raum_14 | ZIMMER | raum_48 | KÜCHE | 100.0 % |
| raum_22 | ZIMMER | raum_49 | KÜCHE | 100.0 % |
| raum_26 | — | raum_50 | STIEGENHAUS | 100.0 % |
| raum_32 | KÜCHE | raum_51 | KÜCHE | 99.9 % |
| raum_36 | VORRAUM | raum_48 | KÜCHE | 99.9 % |
| raum_38 | ZIMMER | raum_51 | KÜCHE | 99.5 % |
| raum_42 | VORRAUM | raum_51 | KÜCHE | 99.1 % |
| lift_1 | LIFT | raum_29 | — | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 7** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
