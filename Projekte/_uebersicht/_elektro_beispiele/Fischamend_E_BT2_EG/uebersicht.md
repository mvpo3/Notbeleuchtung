# Übersicht — Fischamend_E_BT2_EG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\BVH Fischamenderstraße\fertige Elektromontagepläne\BT2\Elektromontageplan_ERDGESCHOSS BT2.dxf` · Geschoss: `EG` · Bild: 1800×1781 px · Laufzeit 45.3 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 14 |
| Sanitär (BAD/WC) | 9 |
| sonstige typisierte Räume | 5 |
| Außenflächen (BALKON/TERRASSE) | 6 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 8 |
| Stiegenhäuser | 1 |
| Schächte/Lifte | 2 |
| untypisierte Räume (nicht erkannt) | 6 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 2 |
| Ausgänge final_exit | 6 |
| Ausgänge stair_exit | 2 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 53 |
| Räume > 90 % in anderem Raum | 11 |

Räume gesamt: **51**, davon typisiert 45.

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
| GARAGE | 1 |
| KINDERWAGENRAUM | 1 |
| LIFT | 1 |
| MUELLRAUM | 1 |
| SCHACHT | 1 |
| STIEGENHAUS | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 4 |
| top_2 | 23 |

Räume ohne `wohnung_id`: 24

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_2 | KÜCHE | raum_46 | KÜCHE | 99.0 % |
| raum_8 | KÜCHE | raum_47 | KÜCHE | 99.0 % |
| raum_11 | VORRAUM | raum_47 | KÜCHE | 95.8 % |
| raum_13 | ZIMMER | raum_47 | KÜCHE | 100.0 % |
| raum_14 | ZIMMER | raum_46 | KÜCHE | 100.0 % |
| raum_26 | — | raum_48 | STIEGENHAUS | 100.0 % |
| raum_32 | KÜCHE | raum_49 | KÜCHE | 100.0 % |
| raum_36 | VORRAUM | raum_46 | KÜCHE | 100.0 % |
| raum_39 | BAD | raum_49 | KÜCHE | 100.0 % |
| raum_42 | VORRAUM | raum_49 | KÜCHE | 96.2 % |
| lift_1 | LIFT | raum_29 | — | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 6** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
