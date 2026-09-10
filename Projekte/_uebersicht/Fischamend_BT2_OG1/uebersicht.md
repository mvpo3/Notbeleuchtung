# Übersicht — Fischamend_BT2_OG1

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\BVH Fischamenderstraße\BT2\260320_938-AR-PP-21010-A_1.OBERGESCHOSS BT2.dxf` · Geschoss: `EG` · Bild: 1091×1800 px · Laufzeit 43.8 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 25 |
| Sanitär (BAD/WC) | 15 |
| sonstige typisierte Räume | 3 |
| Außenflächen (BALKON/TERRASSE) | 7 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 13 |
| Stiegenhäuser | 2 |
| Schächte/Lifte | 2 |
| untypisierte Räume (nicht erkannt) | 1 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 4 |
| Ausgänge final_exit | 1 |
| Ausgänge stair_exit | 2 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 88 |
| Räume > 90 % in anderem Raum | 26 |

Räume gesamt: **68**, davon typisiert 67.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| KÜCHE | 14 |
| ZIMMER | 11 |
| BAD | 8 |
| VORRAUM | 8 |
| BALKON | 7 |
| WC | 7 |
| GANG | 5 |
| ABSTELLRAUM | 3 |
| LIFT | 2 |
| STIEGENHAUS | 2 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 43 |
| top_2 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_3 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_4 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 22

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_1 | KÜCHE | raum_63 | KÜCHE | 99.0 % |
| raum_2 | KÜCHE | raum_61 | KÜCHE | 100.0 % |
| raum_3 | KÜCHE | raum_64 | KÜCHE | 99.9 % |
| raum_8 | KÜCHE | raum_60 | KÜCHE | 100.0 % |
| raum_11 | VORRAUM | raum_64 | KÜCHE | 100.0 % |
| raum_12 | GANG | raum_64 | KÜCHE | 97.1 % |
| raum_14 | BAD | raum_64 | KÜCHE | 100.0 % |
| raum_14 | BAD | lift_2 | LIFT | 100.0 % |
| raum_18 | VORRAUM | raum_63 | KÜCHE | 95.1 % |
| raum_22 | KÜCHE | raum_62 | KÜCHE | 99.5 % |
| raum_24 | VORRAUM | raum_62 | KÜCHE | 96.9 % |
| raum_26 | BAD | raum_62 | KÜCHE | 99.0 % |
| raum_27 | ZIMMER | raum_63 | KÜCHE | 100.0 % |
| raum_28 | VORRAUM | raum_61 | KÜCHE | 99.8 % |
| raum_33 | ZIMMER | raum_61 | KÜCHE | 100.0 % |
| raum_34 | ZIMMER | raum_60 | KÜCHE | 99.4 % |
| raum_35 | ZIMMER | raum_60 | KÜCHE | 100.0 % |
| raum_36 | GANG | raum_60 | KÜCHE | 95.2 % |
| raum_44 | VORRAUM | raum_59 | KÜCHE | 94.1 % |
| raum_45 | KÜCHE | raum_59 | KÜCHE | 98.6 % |
| raum_49 | — | raum_50 | STIEGENHAUS | 100.0 % |
| raum_53 | KÜCHE | raum_65 | KÜCHE | 100.0 % |
| raum_54 | VORRAUM | raum_65 | KÜCHE | 95.0 % |
| raum_56 | BAD | raum_65 | KÜCHE | 96.3 % |
| lift_2 | LIFT | raum_14 | BAD | 100.0 % |
| lift_2 | LIFT | raum_64 | KÜCHE | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 1** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
