# Übersicht — Barawitzka_1DG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Barawitzkagasse\415_260415_PP_VA_1_7 1 DG.dxf` · Geschoss: `DG` · Bild: 1707×1800 px · Laufzeit 85.9 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 8 |
| Sanitär (BAD/WC) | 6 |
| sonstige typisierte Räume | 2 |
| Außenflächen (BALKON/TERRASSE) | 3 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 2 |
| Stiegenhäuser | 3 |
| Schächte/Lifte | 7 |
| untypisierte Räume (nicht erkannt) | 9 |
| Innenhöfe (geschlossene Außenflächen) | 3 |
| Wohnungen | 6 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 1 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 4 |
| Räume > 90 % in anderem Raum | 3 |

Räume gesamt: **40**, davon typisiert 31.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 6 |
| LIFT | 4 |
| WC | 4 |
| SCHACHT | 3 |
| STIEGENHAUS | 3 |
| ABSTELLRAUM | 2 |
| BAD | 2 |
| BALKON | 2 |
| KÜCHE | 2 |
| GANG | 1 |
| TERRASSE | 1 |
| VORRAUM | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_2 | 3 |
| top_3 | 4 |
| top_4 | 5 |
| top_5 | 2 |
| top_6 | 3 |

Räume ohne `wohnung_id`: 22

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_1 | BAD | raum_8 | STIEGENHAUS | 98.9 % |
| lift_3 | LIFT | raum_10 | WC | 94.4 % |
| lift_4 | LIFT | raum_9 | KÜCHE | 96.1 % |

## NICHT erkannt

- **untypisierte Räume: 9** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
