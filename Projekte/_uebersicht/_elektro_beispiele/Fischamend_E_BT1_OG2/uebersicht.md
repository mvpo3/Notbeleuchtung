# Übersicht — Fischamend_E_BT1_OG2

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\BVH Fischamenderstraße\fertige Elektromontagepläne\BT1\Elektromontageapläne_2-OBERGESCHOSS BT1.dxf` · Geschoss: `EG` · Bild: 1800×1086 px · Laufzeit 50.4 s

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
| Wohnungen | 2 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 2 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 103 |
| Räume > 90 % in anderem Raum | 23 |

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
| top_1 | 13 |
| top_2 | 32 |

Räume ohne `wohnung_id`: 24

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_11 | BALKON | raum_63 | KÜCHE | 95.0 % |
| raum_13 | KÜCHE | raum_60 | KÜCHE | 100.0 % |
| raum_16 | KÜCHE | raum_61 | KÜCHE | 100.0 % |
| raum_21 | KÜCHE | raum_62 | KÜCHE | 99.4 % |
| raum_22 | GANG | raum_62 | KÜCHE | 92.1 % |
| raum_23 | VORRAUM | raum_62 | KÜCHE | 99.7 % |
| raum_24 | KÜCHE | raum_63 | KÜCHE | 99.9 % |
| raum_25 | GANG | raum_63 | KÜCHE | 95.9 % |
| raum_26 | VORRAUM | raum_63 | KÜCHE | 99.6 % |
| raum_35 | VORRAUM | raum_64 | KÜCHE | 100.0 % |
| raum_36 | GANG | raum_64 | KÜCHE | 95.5 % |
| raum_37 | KÜCHE | raum_64 | KÜCHE | 99.8 % |
| raum_41 | ZIMMER | raum_63 | KÜCHE | 98.6 % |
| raum_45 | ZIMMER | raum_62 | KÜCHE | 100.0 % |
| raum_50 | — | lift_2 | LIFT | 100.0 % |
| raum_51 | STIEGENHAUS | raum_65 | STIEGENHAUS | 98.3 % |
| raum_52 | GANG | raum_64 | KÜCHE | 100.0 % |
| raum_54 | VORRAUM | raum_66 | KÜCHE | 100.0 % |
| raum_55 | GANG | raum_66 | KÜCHE | 96.1 % |
| raum_56 | KÜCHE | raum_66 | KÜCHE | 99.9 % |
| raum_65 | STIEGENHAUS | raum_51 | STIEGENHAUS | 93.7 % |
| lift_1 | LIFT | raum_53 | — | 100.0 % |
| lift_2 | LIFT | raum_50 | — | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 2** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
