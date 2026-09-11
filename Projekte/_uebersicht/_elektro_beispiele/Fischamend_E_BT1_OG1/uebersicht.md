# Übersicht — Fischamend_E_BT1_OG1

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\BVH Fischamenderstraße\fertige Elektromontagepläne\BT1\Elektromontageapläne_1-OBERGESCHOSS BT1.dxf` · Geschoss: `EG` · Bild: 1800×1086 px · Laufzeit 42.5 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 26 |
| Sanitär (BAD/WC) | 12 |
| sonstige typisierte Räume | 4 |
| Außenflächen (BALKON/TERRASSE) | 7 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 14 |
| Stiegenhäuser | 2 |
| Schächte/Lifte | 2 |
| untypisierte Räume (nicht erkannt) | 2 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 1 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 2 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 60 |
| Räume > 90 % in anderem Raum | 25 |

Räume gesamt: **69**, davon typisiert 67.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 14 |
| KÜCHE | 12 |
| GANG | 8 |
| BALKON | 7 |
| BAD | 6 |
| VORRAUM | 6 |
| WC | 6 |
| ABSTELLRAUM | 4 |
| LIFT | 2 |
| STIEGENHAUS | 2 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 47 |

Räume ohne `wohnung_id`: 22

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_1 | KÜCHE | raum_60 | KÜCHE | 100.0 % |
| raum_18 | KÜCHE | raum_64 | KÜCHE | 100.0 % |
| raum_21 | — | lift_2 | LIFT | 100.0 % |
| raum_22 | STIEGENHAUS | raum_61 | STIEGENHAUS | 98.3 % |
| raum_27 | ZIMMER | raum_64 | KÜCHE | 100.0 % |
| raum_28 | ZIMMER | raum_64 | KÜCHE | 98.8 % |
| raum_31 | VORRAUM | raum_64 | KÜCHE | 99.2 % |
| raum_32 | KÜCHE | raum_62 | KÜCHE | 100.0 % |
| raum_34 | ZIMMER | raum_65 | KÜCHE | 100.0 % |
| raum_35 | ZIMMER | raum_65 | KÜCHE | 99.5 % |
| raum_36 | ABSTELLRAUM | raum_65 | KÜCHE | 95.3 % |
| raum_39 | GANG | raum_65 | KÜCHE | 99.8 % |
| raum_40 | KÜCHE | raum_65 | KÜCHE | 100.0 % |
| raum_41 | VORRAUM | raum_65 | KÜCHE | 99.4 % |
| raum_42 | ZIMMER | raum_63 | KÜCHE | 99.0 % |
| raum_43 | ZIMMER | raum_63 | KÜCHE | 100.0 % |
| raum_45 | GANG | raum_63 | KÜCHE | 92.2 % |
| raum_48 | VORRAUM | raum_63 | KÜCHE | 99.6 % |
| raum_49 | KÜCHE | raum_63 | KÜCHE | 99.4 % |
| raum_51 | GANG | raum_66 | KÜCHE | 96.1 % |
| raum_52 | KÜCHE | raum_66 | KÜCHE | 99.9 % |
| raum_58 | VORRAUM | raum_66 | KÜCHE | 100.0 % |
| raum_61 | STIEGENHAUS | raum_22 | STIEGENHAUS | 94.3 % |
| lift_1 | LIFT | raum_23 | — | 100.0 % |
| lift_2 | LIFT | raum_21 | — | 99.9 % |

## NICHT erkannt

- **untypisierte Räume: 2** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
