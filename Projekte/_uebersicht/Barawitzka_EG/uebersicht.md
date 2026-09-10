# Übersicht — Barawitzka_EG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Barawitzkagasse\415_260415_PP_VA_1_3 0 EG.dxf` · Geschoss: `EG` · Bild: 1153×1800 px · Laufzeit 54.9 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 10 |
| Sanitär (BAD/WC) | 8 |
| sonstige typisierte Räume | 5 |
| Außenflächen (BALKON/TERRASSE) | 9 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 5 |
| Stiegenhäuser | 2 |
| Schächte/Lifte | 5 |
| untypisierte Räume (nicht erkannt) | 6 |
| Innenhöfe (geschlossene Außenflächen) | 2 |
| Wohnungen | 7 |
| Ausgänge final_exit | 1 |
| Ausgänge stair_exit | 0 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 12 |
| Räume > 90 % in anderem Raum | 5 |

Räume gesamt: **50**, davon typisiert 44.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| TERRASSE | 6 |
| ZIMMER | 6 |
| VORRAUM | 5 |
| BAD | 4 |
| KÜCHE | 4 |
| WC | 4 |
| ABSTELLRAUM | 3 |
| BALKON | 3 |
| LIFT | 3 |
| SCHACHT | 2 |
| STIEGENHAUS | 2 |
| KINDERWAGENRAUM | 1 |
| WASCHKÜCHE | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 11 |
| top_2 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_3 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_4 | 7 |
| top_5 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_6 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_7 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 27

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_15 | TERRASSE | raum_43 | TERRASSE | 99.0 % |
| raum_34 | WASCHKÜCHE | lift_1 | LIFT | 100.0 % |
| raum_37 | STIEGENHAUS | raum_43 | TERRASSE | 99.0 % |
| rest_3 | SCHACHT | lift_2 | LIFT | 100.0 % |
| lift_1 | LIFT | raum_34 | WASCHKÜCHE | 92.8 % |

## NICHT erkannt

- **untypisierte Räume: 6** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `stair_exit`: **0** — kein Stiegenhaus-Ausgang erkannt.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
