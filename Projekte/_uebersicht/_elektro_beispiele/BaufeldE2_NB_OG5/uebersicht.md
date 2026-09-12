# Übersicht — BaufeldE2_NB_OG5

DXF: `C:\Users\selma\AppData\Local\Temp\claude\D--KI-Projekt\8fc32369-9bee-42cd-9e07-20d9eeb9eff5\scratchpad\zips\Baufeld_E2_NB\Elektromontageplan_5OG.dxf` · Geschoss: `5OG` · Bild: 2051×2400 px · Laufzeit 1080.9 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 66 |
| Sanitär (BAD/WC) | 47 |
| sonstige typisierte Räume | 18 |
| Außenflächen (BALKON/TERRASSE) | 23 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 40 |
| Stiegenhäuser | 11 |
| Schächte/Lifte | 0 |
| untypisierte Räume (nicht erkannt) | 14 |
| Innenhöfe (geschlossene Außenflächen) | 5 |
| Wohnungen | 16 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 15 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 197 |
| Räume > 90 % in anderem Raum | 9 |

Räume gesamt: **219**, davon typisiert 205.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 39 |
| WC | 25 |
| BALKON | 23 |
| KÜCHE | 23 |
| VORRAUM | 23 |
| BAD | 22 |
| GANG | 17 |
| ABSTELLRAUM | 15 |
| STIEGENHAUS | 11 |
| WOHNZIMMER | 4 |
| KINDERWAGENRAUM | 3 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 35 |
| top_10 | 3 |
| top_11 | 4 |
| top_12 | 2 |
| top_13 | 2 |
| top_14 | 6 |
| top_15 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_16 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_2 | 23 |
| top_3 | 11 |
| top_4 | 14 |
| top_5 | 4 |
| top_6 | 8 |
| top_7 | 3 |
| top_8 | 3 |
| top_9 | 12 |

Räume ohne `wohnung_id`: 87

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_92 | — | raum_91 | STIEGENHAUS | 100.0 % |
| raum_93 | — | raum_91 | STIEGENHAUS | 100.0 % |
| raum_94 | — | raum_91 | STIEGENHAUS | 100.0 % |
| raum_95 | — | raum_91 | STIEGENHAUS | 100.0 % |
| raum_183 | STIEGENHAUS | raum_211 | KINDERWAGENRAUM | 99.6 % |
| raum_192 | — | raum_191 | STIEGENHAUS | 100.0 % |
| raum_193 | — | raum_191 | STIEGENHAUS | 100.0 % |
| raum_209 | WC | raum_28 | WC | 98.0 % |
| raum_210 | WC | raum_28 | WC | 97.3 % |

## NICHT erkannt

- **untypisierte Räume: 14** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Schächte/Lifte: **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
