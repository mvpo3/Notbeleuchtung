# Übersicht — Fischamend_E_BT2_DG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\BVH Fischamenderstraße\fertige Elektromontagepläne\BT2\Elektromontageplan_DACHGESCHOSS BT2.dxf` · Geschoss: `EG` · Bild: 1087×1800 px · Laufzeit 37.4 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 21 |
| Sanitär (BAD/WC) | 12 |
| sonstige typisierte Räume | 2 |
| Außenflächen (BALKON/TERRASSE) | 7 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 10 |
| Stiegenhäuser | 2 |
| Schächte/Lifte | 3 |
| untypisierte Räume (nicht erkannt) | 1 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 3 |
| Ausgänge final_exit | 1 |
| Ausgänge stair_exit | 2 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 58 |
| Räume > 90 % in anderem Raum | 23 |

Räume gesamt: **58**, davon typisiert 57.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| KÜCHE | 12 |
| ZIMMER | 9 |
| BAD | 7 |
| VORRAUM | 7 |
| WC | 5 |
| TERRASSE | 4 |
| BALKON | 3 |
| GANG | 3 |
| ABSTELLRAUM | 2 |
| LIFT | 2 |
| STIEGENHAUS | 2 |
| SCHACHT | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 28 |
| top_2 | 7 |
| top_3 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 22

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_6 | VORRAUM | raum_48 | KÜCHE | 100.0 % |
| raum_7 | KÜCHE | raum_49 | KÜCHE | 98.5 % |
| raum_9 | VORRAUM | raum_49 | KÜCHE | 98.2 % |
| raum_11 | BAD | raum_49 | KÜCHE | 96.9 % |
| raum_13 | KÜCHE | raum_50 | KÜCHE | 99.6 % |
| raum_15 | VORRAUM | raum_50 | KÜCHE | 94.3 % |
| raum_19 | VORRAUM | raum_51 | KÜCHE | 99.7 % |
| raum_20 | KÜCHE | raum_51 | KÜCHE | 100.0 % |
| raum_21 | BAD | raum_51 | KÜCHE | 99.1 % |
| raum_24 | VORRAUM | raum_52 | KÜCHE | 100.0 % |
| raum_25 | KÜCHE | raum_52 | KÜCHE | 99.6 % |
| raum_27 | VORRAUM | raum_54 | KÜCHE | 96.2 % |
| raum_28 | KÜCHE | raum_54 | KÜCHE | 99.9 % |
| raum_29 | GANG | raum_50 | KÜCHE | 94.8 % |
| raum_33 | BAD | raum_48 | KÜCHE | 99.1 % |
| raum_33 | BAD | lift_2 | LIFT | 100.0 % |
| raum_35 | GANG | raum_48 | KÜCHE | 96.9 % |
| raum_36 | KÜCHE | raum_48 | KÜCHE | 99.7 % |
| raum_37 | — | raum_38 | STIEGENHAUS | 100.0 % |
| raum_39 | ZIMMER | raum_52 | KÜCHE | 98.5 % |
| raum_42 | VORRAUM | raum_54 | KÜCHE | 91.9 % |
| lift_2 | LIFT | raum_33 | BAD | 100.0 % |
| lift_2 | LIFT | raum_48 | KÜCHE | 99.1 % |

## NICHT erkannt

- **untypisierte Räume: 1** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
