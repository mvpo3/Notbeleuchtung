# Übersicht — Mollgasse_OG3

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Mollgasse\3.Obergeschoß.dxf` · Geschoss: `EG` · Bild: 1800×1463 px · Laufzeit 84.6 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 15 |
| Sanitär (BAD/WC) | 15 |
| sonstige typisierte Räume | 7 |
| Außenflächen (BALKON/TERRASSE) | 2 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 12 |
| Stiegenhäuser | 1 |
| Schächte/Lifte | 2 |
| untypisierte Räume (nicht erkannt) | 10 |
| Innenhöfe (geschlossene Außenflächen) | 4 |
| Wohnungen | 13 |
| Ausgänge final_exit | 1 |
| Ausgänge stair_exit | 0 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 9 |
| Räume > 90 % in anderem Raum | 1 |

Räume gesamt: **64**, davon typisiert 54.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 11 |
| BAD | 8 |
| ABSTELLRAUM | 7 |
| WC | 7 |
| GANG | 6 |
| VORRAUM | 6 |
| KÜCHE | 3 |
| BALKON | 2 |
| LIFT | 2 |
| STIEGENHAUS | 1 |
| WOHNZIMMER | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 5 |
| top_10 | 5 |
| top_11 | 2 |
| top_12 | 2 |
| top_13 | 3 |
| top_2 | 4 |
| top_3 | 3 |
| top_4 | 4 |
| top_5 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_6 | 4 |
| top_7 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_8 | 6 |
| top_9 | 4 |

Räume ohne `wohnung_id`: 20

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| lift_2 | LIFT | raum_35 | — | 98.6 % |

## NICHT erkannt

- **untypisierte Räume: 10** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `stair_exit`: **0** — kein Stiegenhaus-Ausgang erkannt.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
