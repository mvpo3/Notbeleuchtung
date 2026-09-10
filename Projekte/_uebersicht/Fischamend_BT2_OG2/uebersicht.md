# Übersicht — Fischamend_BT2_OG2

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\BVH Fischamenderstraße\BT2\260320_938-AR-PP-21020-A_2.OBERGESCHOSS BT2.dxf` · Geschoss: `EG` · Bild: 1081×1800 px · Laufzeit 46.1 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 24 |
| Sanitär (BAD/WC) | 14 |
| sonstige typisierte Räume | 4 |
| Außenflächen (BALKON/TERRASSE) | 6 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 12 |
| Stiegenhäuser | 1 |
| Schächte/Lifte | 2 |
| untypisierte Räume (nicht erkannt) | 3 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 5 |
| Ausgänge final_exit | 1 |
| Ausgänge stair_exit | 2 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 81 |
| Räume > 90 % in anderem Raum | 25 |

Räume gesamt: **66**, davon typisiert 63.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| KÜCHE | 13 |
| ZIMMER | 11 |
| BAD | 8 |
| VORRAUM | 8 |
| BALKON | 6 |
| WC | 6 |
| GANG | 4 |
| ABSTELLRAUM | 3 |
| LIFT | 2 |
| STIEGENHAUS | 1 |
| TECHNIK | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 36 |
| top_2 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_3 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_4 | 5 |
| top_5 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 22

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_1 | KÜCHE | raum_58 | KÜCHE | 99.0 % |
| raum_2 | KÜCHE | raum_61 | KÜCHE | 100.0 % |
| raum_3 | KÜCHE | raum_57 | KÜCHE | 99.9 % |
| raum_8 | KÜCHE | raum_60 | KÜCHE | 99.6 % |
| raum_11 | VORRAUM | raum_57 | KÜCHE | 99.7 % |
| raum_13 | BAD | raum_57 | KÜCHE | 99.1 % |
| raum_13 | BAD | lift_2 | LIFT | 100.0 % |
| raum_16 | VORRAUM | raum_58 | KÜCHE | 95.9 % |
| raum_20 | KÜCHE | raum_59 | KÜCHE | 99.2 % |
| raum_22 | VORRAUM | raum_59 | KÜCHE | 97.6 % |
| raum_24 | BAD | raum_59 | KÜCHE | 99.0 % |
| raum_25 | ZIMMER | raum_58 | KÜCHE | 99.9 % |
| raum_26 | VORRAUM | raum_61 | KÜCHE | 99.9 % |
| raum_31 | ZIMMER | raum_61 | KÜCHE | 100.0 % |
| raum_39 | VORRAUM | raum_60 | KÜCHE | 91.8 % |
| raum_42 | VORRAUM | raum_62 | KÜCHE | 94.3 % |
| raum_45 | — | raum_46 | STIEGENHAUS | 100.0 % |
| raum_50 | GANG | raum_57 | KÜCHE | 97.3 % |
| raum_51 | KÜCHE | raum_64 | KÜCHE | 99.4 % |
| raum_52 | VORRAUM | raum_64 | KÜCHE | 98.7 % |
| raum_54 | BAD | raum_64 | KÜCHE | 98.1 % |
| raum_56 | — | raum_64 | KÜCHE | 92.4 % |
| lift_1 | LIFT | raum_48 | — | 100.0 % |
| lift_2 | LIFT | raum_13 | BAD | 100.0 % |
| lift_2 | LIFT | raum_57 | KÜCHE | 99.1 % |

## NICHT erkannt

- **untypisierte Räume: 3** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
