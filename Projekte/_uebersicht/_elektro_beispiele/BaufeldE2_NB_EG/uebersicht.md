# Übersicht — BaufeldE2_NB_EG

DXF: `C:\Users\selma\AppData\Local\Temp\claude\D--KI-Projekt\8fc32369-9bee-42cd-9e07-20d9eeb9eff5\scratchpad\zips\Baufeld_E2_NB\Elektromontageplan_EG.dxf` · Geschoss: `EG` · Bild: 2270×2400 px · Laufzeit 544.8 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 61 |
| Sanitär (BAD/WC) | 39 |
| sonstige typisierte Räume | 24 |
| Außenflächen (BALKON/TERRASSE) | 24 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 38 |
| Stiegenhäuser | 10 |
| Schächte/Lifte | 6 |
| untypisierte Räume (nicht erkannt) | 39 |
| Innenhöfe (geschlossene Außenflächen) | 6 |
| Wohnungen | 19 |
| Ausgänge final_exit | 6 |
| Ausgänge stair_exit | 12 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 196 |
| Räume > 90 % in anderem Raum | 6 |

Räume gesamt: **241**, davon typisiert 202.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 35 |
| TERRASSE | 24 |
| KÜCHE | 22 |
| VORRAUM | 22 |
| BAD | 21 |
| WC | 18 |
| GANG | 16 |
| ABSTELLRAUM | 14 |
| STIEGENHAUS | 10 |
| SCHACHT | 6 |
| KINDERWAGENRAUM | 5 |
| MUELLRAUM | 4 |
| WOHNZIMMER | 4 |
| WASCHKÜCHE | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 21 |
| top_10 | 3 |
| top_11 | 2 |
| top_12 | 4 |
| top_13 | 9 |
| top_14 | 3 |
| top_15 | 4 |
| top_16 | 6 |
| top_17 | 9 |
| top_18 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_19 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_2 | 2 |
| top_3 | 8 |
| top_4 | 3 |
| top_5 | 20 |
| top_6 | 6 |
| top_7 | 3 |
| top_8 | 7 |
| top_9 | 4 |

Räume ohne `wohnung_id`: 125

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_104 | MUELLRAUM | raum_222 | MUELLRAUM | 98.8 % |
| raum_183 | — | raum_221 | TERRASSE | 100.0 % |
| raum_195 | STIEGENHAUS | raum_224 | KINDERWAGENRAUM | 95.8 % |
| raum_204 | MUELLRAUM | raum_223 | MUELLRAUM | 99.8 % |
| raum_208 | — | raum_207 | STIEGENHAUS | 100.0 % |
| raum_223 | MUELLRAUM | raum_204 | MUELLRAUM | 93.4 % |

## NICHT erkannt

- **untypisierte Räume: 39** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
