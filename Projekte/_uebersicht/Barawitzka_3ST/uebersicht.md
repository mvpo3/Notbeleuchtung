# Übersicht — Barawitzka_3ST

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Barawitzkagasse\415_260415_PP_VA_1_6 3 St.dxf` · Geschoss: `EG` · Bild: 2400×723 px · Laufzeit 113.7 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 6 |
| Sanitär (BAD/WC) | 6 |
| sonstige typisierte Räume | 2 |
| Außenflächen (BALKON/TERRASSE) | 1 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 1 |
| Stiegenhäuser | 3 |
| Schächte/Lifte | 6 |
| untypisierte Räume (nicht erkannt) | 11 |
| Innenhöfe (geschlossene Außenflächen) | 3 |
| Wohnungen | 9 |
| Ausgänge final_exit | 7 |
| Ausgänge stair_exit | 1 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 7 |
| Räume > 90 % in anderem Raum | 1 |

Räume gesamt: **36**, davon typisiert 25.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 5 |
| WC | 4 |
| LIFT | 3 |
| SCHACHT | 3 |
| STIEGENHAUS | 3 |
| ABSTELLRAUM | 2 |
| BAD | 2 |
| BALKON | 1 |
| KÜCHE | 1 |
| VORRAUM | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_2 | 2 |
| top_3 | 2 |
| top_4 | 2 |
| top_5 | 2 |
| top_6 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_7 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_8 | 2 |
| top_9 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 22

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_1 | BAD | raum_4 | STIEGENHAUS | 98.7 % |

## NICHT erkannt

- **untypisierte Räume: 11** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
