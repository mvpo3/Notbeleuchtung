# Übersicht — BaufeldE2_NB_OG6

DXF: `C:\Users\selma\AppData\Local\Temp\claude\D--KI-Projekt\8fc32369-9bee-42cd-9e07-20d9eeb9eff5\scratchpad\zips\Baufeld_E2_NB\Elektromontageplan_6OG.dxf` · Geschoss: `6OG` · Bild: 2035×2400 px · Laufzeit 486.5 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 69 |
| Sanitär (BAD/WC) | 46 |
| sonstige typisierte Räume | 15 |
| Außenflächen (BALKON/TERRASSE) | 23 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 42 |
| Stiegenhäuser | 10 |
| Schächte/Lifte | 0 |
| untypisierte Räume (nicht erkannt) | 10 |
| Innenhöfe (geschlossene Außenflächen) | 6 |
| Wohnungen | 16 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 14 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 199 |
| Räume > 90 % in anderem Raum | 0 |

Räume gesamt: **215**, davon typisiert 205.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 42 |
| BAD | 23 |
| BALKON | 23 |
| KÜCHE | 23 |
| VORRAUM | 23 |
| WC | 23 |
| GANG | 19 |
| ABSTELLRAUM | 13 |
| STIEGENHAUS | 10 |
| WOHNZIMMER | 4 |
| KINDERWAGENRAUM | 2 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 22 |
| top_10 | 2 |
| top_11 | 3 |
| top_12 | 3 |
| top_13 | 3 |
| top_14 | 4 |
| top_15 | 2 |
| top_16 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_2 | 33 |
| top_3 | 13 |
| top_4 | 11 |
| top_5 | 3 |
| top_6 | 17 |
| top_7 | 4 |
| top_8 | 8 |
| top_9 | 2 |

Räume ohne `wohnung_id`: 84

## NICHT erkannt

- **untypisierte Räume: 10** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Schächte/Lifte: **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
