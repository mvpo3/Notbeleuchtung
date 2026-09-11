# Übersicht — Barawitzka_2DG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Barawitzkagasse\415_260415_PP_VA_1_8 2 DG.dxf` · Geschoss: `DG` · Bild: 2400×869 px · Laufzeit 79.6 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 7 |
| Sanitär (BAD/WC) | 4 |
| sonstige typisierte Räume | 1 |
| Außenflächen (BALKON/TERRASSE) | 0 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 1 |
| Stiegenhäuser | 2 |
| Schächte/Lifte | 6 |
| untypisierte Räume (nicht erkannt) | 4 |
| Innenhöfe (geschlossene Außenflächen) | 1 |
| Wohnungen | 5 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 0 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 2 |
| Räume > 90 % in anderem Raum | 2 |

Räume gesamt: **25**, davon typisiert 21.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 6 |
| LIFT | 3 |
| SCHACHT | 3 |
| BAD | 2 |
| STIEGENHAUS | 2 |
| WC | 2 |
| ABSTELLRAUM | 1 |
| KÜCHE | 1 |
| VORRAUM | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 7 |
| top_2 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_3 | 2 |
| top_4 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_5 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 13

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_5 | STIEGENHAUS | lift_3 | LIFT | 90.9 % |
| rest_2 | SCHACHT | lift_3 | LIFT | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 4** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Außenflächen (BALKON/TERRASSE): **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `stair_exit`: **0** — kein Stiegenhaus-Ausgang erkannt.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
