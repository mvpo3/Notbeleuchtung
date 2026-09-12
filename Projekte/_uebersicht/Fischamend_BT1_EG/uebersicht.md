# Übersicht — Fischamend_BT1_EG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\BVH Fischamenderstraße\BT1\260320_938-AR-PP-11000-A_ERDGESCHOSS BT1.dxf` · Geschoss: `EG` · Bild: 1800×1377 px · Laufzeit 68.0 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 24 |
| Sanitär (BAD/WC) | 12 |
| sonstige typisierte Räume | 10 |
| Außenflächen (BALKON/TERRASSE) | 10 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 14 |
| Stiegenhäuser | 1 |
| Schächte/Lifte | 1 |
| untypisierte Räume (nicht erkannt) | 7 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 3 |
| Ausgänge final_exit | 3 |
| Ausgänge stair_exit | 1 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 90 |
| Räume > 90 % in anderem Raum | 17 |

Räume gesamt: **79**, davon typisiert 72.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 14 |
| KÜCHE | 10 |
| GANG | 8 |
| TERRASSE | 7 |
| BAD | 6 |
| VORRAUM | 6 |
| WC | 6 |
| ABSTELLRAUM | 4 |
| BALKON | 3 |
| TECHNIK | 3 |
| GARAGE | 2 |
| KINDERWAGENRAUM | 1 |
| LIFT | 1 |
| STIEGENHAUS | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 14 |
| top_2 | 16 |
| top_3 | 13 |

Räume ohne `wohnung_id`: 36

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_1 | ZIMMER | raum_74 | KÜCHE | 99.8 % |
| raum_2 | ZIMMER | raum_73 | KÜCHE | 100.0 % |
| raum_6 | — | raum_72 | BALKON | 94.0 % |
| raum_16 | ZIMMER | raum_74 | KÜCHE | 99.7 % |
| raum_19 | ZIMMER | raum_73 | KÜCHE | 100.0 % |
| raum_20 | ZIMMER | raum_73 | KÜCHE | 100.0 % |
| raum_21 | KÜCHE | raum_73 | KÜCHE | 99.9 % |
| raum_45 | KÜCHE | raum_74 | KÜCHE | 99.6 % |
| raum_48 | KÜCHE | raum_75 | KÜCHE | 100.0 % |
| raum_51 | GANG | raum_73 | KÜCHE | 99.9 % |
| raum_52 | VORRAUM | raum_73 | KÜCHE | 100.0 % |
| raum_53 | ABSTELLRAUM | raum_73 | KÜCHE | 100.0 % |
| raum_56 | KÜCHE | raum_72 | BALKON | 94.2 % |
| raum_57 | BALKON | raum_72 | BALKON | 91.5 % |
| raum_59 | TERRASSE | raum_69 | TERRASSE | 100.0 % |
| raum_62 | — | raum_63 | STIEGENHAUS | 100.0 % |
| lift_1 | LIFT | raum_61 | TECHNIK | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 7** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
