# Übersicht — Mollgasse_OG4

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Mollgasse\4.Obergeschoß.dxf` · Geschoss: `EG` · Bild: 1800×1469 px · Laufzeit 73.5 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 12 |
| Sanitär (BAD/WC) | 13 |
| sonstige typisierte Räume | 6 |
| Außenflächen (BALKON/TERRASSE) | 1 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 10 |
| Stiegenhäuser | 3 |
| Schächte/Lifte | 3 |
| untypisierte Räume (nicht erkannt) | 5 |
| Innenhöfe (geschlossene Außenflächen) | 4 |
| Wohnungen | 12 |
| Ausgänge final_exit | 1 |
| Ausgänge stair_exit | 1 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 10 |
| Räume > 90 % in anderem Raum | 1 |

Räume gesamt: **53**, davon typisiert 48.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 9 |
| BAD | 7 |
| ABSTELLRAUM | 6 |
| VORRAUM | 6 |
| WC | 6 |
| GANG | 4 |
| STIEGENHAUS | 3 |
| KÜCHE | 2 |
| LIFT | 2 |
| BALKON | 1 |
| SCHACHT | 1 |
| WOHNZIMMER | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 5 |
| top_10 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_11 | 2 |
| top_12 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_2 | 3 |
| top_3 | 2 |
| top_4 | 5 |
| top_5 | 6 |
| top_6 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_7 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_8 | 4 |
| top_9 | 4 |

Räume ohne `wohnung_id`: 18

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_43 | — | lift_2 | LIFT | 97.8 % |

## NICHT erkannt

- **untypisierte Räume: 5** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
