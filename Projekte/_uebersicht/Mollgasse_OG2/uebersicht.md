# Übersicht — Mollgasse_OG2

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Mollgasse\2.Obergeschoß.dxf` · Geschoss: `EG` · Bild: 1800×1495 px · Laufzeit 111.5 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 24 |
| Sanitär (BAD/WC) | 25 |
| sonstige typisierte Räume | 12 |
| Außenflächen (BALKON/TERRASSE) | 3 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 20 |
| Stiegenhäuser | 2 |
| Schächte/Lifte | 3 |
| untypisierte Räume (nicht erkannt) | 8 |
| Innenhöfe (geschlossene Außenflächen) | 5 |
| Wohnungen | 18 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 1 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 26 |
| Räume > 90 % in anderem Raum | 0 |

Räume gesamt: **97**, davon typisiert 89.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 17 |
| VORRAUM | 13 |
| WC | 13 |
| ABSTELLRAUM | 12 |
| BAD | 12 |
| GANG | 7 |
| KÜCHE | 5 |
| BALKON | 3 |
| LIFT | 2 |
| STIEGENHAUS | 2 |
| WOHNZIMMER | 2 |
| SCHACHT | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 7 |
| top_10 | 5 |
| top_11 | 5 |
| top_12 | 4 |
| top_13 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_14 | 8 |
| top_15 | 5 |
| top_16 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_17 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_18 | 4 |
| top_2 | 7 |
| top_3 | 5 |
| top_4 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_5 | 4 |
| top_6 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_7 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_8 | 3 |
| top_9 | 6 |

Räume ohne `wohnung_id`: 28

## NICHT erkannt

- **untypisierte Räume: 8** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
