# Übersicht — BaufeldE2_NB_OG2

DXF: `C:\Users\selma\AppData\Local\Temp\claude\D--KI-Projekt\8fc32369-9bee-42cd-9e07-20d9eeb9eff5\scratchpad\zips\Baufeld_E2_NB\Elektromontageplan_2OG.dxf` · Geschoss: `2OG` · Bild: 2133×2400 px · Laufzeit 697.9 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 98 |
| Sanitär (BAD/WC) | 66 |
| sonstige typisierte Räume | 20 |
| Außenflächen (BALKON/TERRASSE) | 33 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 60 |
| Stiegenhäuser | 9 |
| Schächte/Lifte | 2 |
| untypisierte Räume (nicht erkannt) | 13 |
| Innenhöfe (geschlossene Außenflächen) | 3 |
| Wohnungen | 23 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 12 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 277 |
| Räume > 90 % in anderem Raum | 3 |

Räume gesamt: **301**, davon typisiert 288.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 60 |
| BAD | 33 |
| BALKON | 33 |
| KÜCHE | 33 |
| VORRAUM | 33 |
| WC | 33 |
| GANG | 27 |
| ABSTELLRAUM | 17 |
| STIEGENHAUS | 9 |
| WOHNZIMMER | 5 |
| KINDERWAGENRAUM | 3 |
| SCHACHT | 2 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 22 |
| top_10 | 2 |
| top_11 | 7 |
| top_12 | 11 |
| top_13 | 3 |
| top_14 | 17 |
| top_15 | 4 |
| top_16 | 8 |
| top_17 | 2 |
| top_18 | 3 |
| top_19 | 3 |
| top_2 | 32 |
| top_20 | 6 |
| top_21 | 3 |
| top_22 | 4 |
| top_23 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_3 | 31 |
| top_4 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_5 | 2 |
| top_6 | 2 |
| top_7 | 10 |
| top_8 | 10 |
| top_9 | 2 |

Räume ohne `wohnung_id`: 115

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_278 | STIEGENHAUS | raum_291 | KINDERWAGENRAUM | 99.4 % |
| raum_279 | GANG | raum_290 | GANG | 99.4 % |
| raum_290 | GANG | raum_279 | GANG | 97.1 % |

## NICHT erkannt

- **untypisierte Räume: 13** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
