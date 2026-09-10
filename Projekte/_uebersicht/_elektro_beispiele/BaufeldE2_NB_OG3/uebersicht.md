# Übersicht — BaufeldE2_NB_OG3

DXF: `C:\Users\selma\AppData\Local\Temp\claude\D--KI-Projekt\8fc32369-9bee-42cd-9e07-20d9eeb9eff5\scratchpad\zips\Baufeld_E2_NB\Elektromontageplan_3OG.dxf` · Geschoss: `3OG` · Bild: 2133×2400 px · Laufzeit 819.4 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 98 |
| Sanitär (BAD/WC) | 66 |
| sonstige typisierte Räume | 21 |
| Außenflächen (BALKON/TERRASSE) | 33 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 59 |
| Stiegenhäuser | 11 |
| Schächte/Lifte | 0 |
| untypisierte Räume (nicht erkannt) | 11 |
| Innenhöfe (geschlossene Außenflächen) | 4 |
| Wohnungen | 21 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 13 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 275 |
| Räume > 90 % in anderem Raum | 2 |

Räume gesamt: **299**, davon typisiert 288.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 60 |
| BAD | 33 |
| BALKON | 33 |
| KÜCHE | 33 |
| VORRAUM | 33 |
| WC | 33 |
| GANG | 26 |
| ABSTELLRAUM | 18 |
| STIEGENHAUS | 11 |
| WOHNZIMMER | 5 |
| KINDERWAGENRAUM | 3 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 41 |
| top_10 | 2 |
| top_11 | 2 |
| top_12 | 4 |
| top_13 | 8 |
| top_14 | 3 |
| top_15 | 3 |
| top_16 | 12 |
| top_17 | 3 |
| top_18 | 9 |
| top_19 | 6 |
| top_2 | 10 |
| top_20 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_21 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_3 | 23 |
| top_4 | 2 |
| top_5 | 7 |
| top_6 | 10 |
| top_7 | 27 |
| top_8 | 4 |
| top_9 | 11 |

Räume ohne `wohnung_id`: 110

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_262 | GANG | raum_289 | GANG | 99.4 % |
| raum_289 | GANG | raum_262 | GANG | 96.7 % |

## NICHT erkannt

- **untypisierte Räume: 11** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Schächte/Lifte: **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
