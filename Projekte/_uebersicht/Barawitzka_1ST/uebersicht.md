# Übersicht — Barawitzka_1ST

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Barawitzkagasse\415_260415_PP_VA_1_4 1 St.dxf` · Geschoss: `EG` · Bild: 1800×731 px · Laufzeit 147.6 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 13 |
| Sanitär (BAD/WC) | 12 |
| sonstige typisierte Räume | 3 |
| Außenflächen (BALKON/TERRASSE) | 3 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 2 |
| Stiegenhäuser | 8 |
| Schächte/Lifte | 6 |
| untypisierte Räume (nicht erkannt) | 11 |
| Innenhöfe (geschlossene Außenflächen) | 6 |
| Wohnungen | 11 |
| Ausgänge final_exit | 5 |
| Ausgänge stair_exit | 5 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 11 |
| Räume > 90 % in anderem Raum | 3 |

Räume gesamt: **58**, davon typisiert 47.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 9 |
| STIEGENHAUS | 8 |
| WC | 8 |
| BAD | 4 |
| KÜCHE | 4 |
| LIFT | 4 |
| ABSTELLRAUM | 3 |
| BALKON | 3 |
| SCHACHT | 2 |
| VORRAUM | 2 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 2 |
| top_10 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_11 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_2 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_3 | 5 |
| top_4 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_5 | 2 |
| top_6 | 4 |
| top_7 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_8 | 11 |
| top_9 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 28

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| stiegenhaus_1 | STIEGENHAUS | stiegenhaus_2 | STIEGENHAUS | 99.8 % |
| stiegenhaus_2 | STIEGENHAUS | stiegenhaus_1 | STIEGENHAUS | 99.1 % |
| lift_2 | LIFT | raum_8 | WC | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 11** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
