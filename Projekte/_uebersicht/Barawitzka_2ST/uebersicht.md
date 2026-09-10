# Übersicht — Barawitzka_2ST

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Barawitzkagasse\415_260415_PP_VA_1_5 2 St.dxf` · Geschoss: `EG` · Bild: 1800×782 px · Laufzeit 144.1 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 13 |
| Sanitär (BAD/WC) | 8 |
| sonstige typisierte Räume | 3 |
| Außenflächen (BALKON/TERRASSE) | 3 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 4 |
| Stiegenhäuser | 4 |
| Schächte/Lifte | 7 |
| untypisierte Räume (nicht erkannt) | 11 |
| Innenhöfe (geschlossene Außenflächen) | 7 |
| Wohnungen | 11 |
| Ausgänge final_exit | 5 |
| Ausgänge stair_exit | 1 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 5 |
| Räume > 90 % in anderem Raum | 0 |

Räume gesamt: **53**, davon typisiert 42.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 8 |
| KÜCHE | 5 |
| BAD | 4 |
| LIFT | 4 |
| STIEGENHAUS | 4 |
| VORRAUM | 4 |
| WC | 4 |
| ABSTELLRAUM | 3 |
| SCHACHT | 3 |
| BALKON | 2 |
| TERRASSE | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_10 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_11 | 4 |
| top_2 | 5 |
| top_3 | 4 |
| top_4 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_5 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_6 | 2 |
| top_7 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_8 | 2 |
| top_9 | 6 |

Räume ohne `wohnung_id`: 25

## NICHT erkannt

- **untypisierte Räume: 11** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
