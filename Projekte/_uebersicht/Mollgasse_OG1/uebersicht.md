# Übersicht — Mollgasse_OG1

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Mollgasse\1.Obergeschoß.dxf` · Geschoss: `EG` · Bild: 2400×2078 px · Laufzeit 110.0 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 27 |
| Sanitär (BAD/WC) | 24 |
| sonstige typisierte Räume | 11 |
| Außenflächen (BALKON/TERRASSE) | 3 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 16 |
| Stiegenhäuser | 2 |
| Schächte/Lifte | 2 |
| untypisierte Räume (nicht erkannt) | 7 |
| Innenhöfe (geschlossene Außenflächen) | 5 |
| Wohnungen | 20 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 1 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 26 |
| Räume > 90 % in anderem Raum | 0 |

Räume gesamt: **92**, davon typisiert 85.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 20 |
| BAD | 13 |
| ABSTELLRAUM | 11 |
| VORRAUM | 11 |
| WC | 11 |
| KÜCHE | 6 |
| GANG | 5 |
| BALKON | 3 |
| LIFT | 2 |
| STIEGENHAUS | 2 |
| WOHNZIMMER | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 14 |
| top_10 | 4 |
| top_11 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_12 | 4 |
| top_13 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_14 | 4 |
| top_15 | 5 |
| top_16 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_17 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_18 | 4 |
| top_19 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_2 | 4 |
| top_20 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_3 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_4 | 4 |
| top_5 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_6 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_7 | 3 |
| top_8 | 8 |
| top_9 | 5 |

Räume ohne `wohnung_id`: 24

## NICHT erkannt

- **untypisierte Räume: 7** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
