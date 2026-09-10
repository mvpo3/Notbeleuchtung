# Übersicht — Fischamend_E_BT1_EG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\BVH Fischamenderstraße\fertige Elektromontagepläne\BT1\Elektromontageapläne_ERDGESCHOSS BT1.dxf` · Geschoss: `EG` · Bild: 1800×1027 px · Laufzeit 59.8 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 26 |
| Sanitär (BAD/WC) | 12 |
| sonstige typisierte Räume | 6 |
| Außenflächen (BALKON/TERRASSE) | 7 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 14 |
| Stiegenhäuser | 1 |
| Schächte/Lifte | 1 |
| untypisierte Räume (nicht erkannt) | 5 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 2 |
| Ausgänge final_exit | 3 |
| Ausgänge stair_exit | 1 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 87 |
| Räume > 90 % in anderem Raum | 11 |

Räume gesamt: **72**, davon typisiert 67.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 14 |
| KÜCHE | 12 |
| GANG | 8 |
| BAD | 6 |
| VORRAUM | 6 |
| WC | 6 |
| TERRASSE | 5 |
| ABSTELLRAUM | 4 |
| BALKON | 2 |
| GARAGE | 1 |
| KINDERWAGENRAUM | 1 |
| LIFT | 1 |
| STIEGENHAUS | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 32 |
| top_2 | 13 |

Räume ohne `wohnung_id`: 27

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_2 | ZIMMER | raum_68 | KÜCHE | 100.0 % |
| raum_18 | ZIMMER | raum_68 | KÜCHE | 100.0 % |
| raum_19 | ZIMMER | raum_68 | KÜCHE | 98.2 % |
| raum_20 | KÜCHE | raum_68 | KÜCHE | 100.0 % |
| raum_44 | KÜCHE | raum_69 | KÜCHE | 99.3 % |
| raum_47 | KÜCHE | raum_70 | KÜCHE | 100.0 % |
| raum_50 | GANG | raum_68 | KÜCHE | 100.0 % |
| raum_51 | VORRAUM | raum_68 | KÜCHE | 99.9 % |
| raum_52 | ABSTELLRAUM | raum_68 | KÜCHE | 96.7 % |
| raum_61 | — | raum_62 | STIEGENHAUS | 100.0 % |
| lift_1 | LIFT | raum_60 | GARAGE | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 5** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
