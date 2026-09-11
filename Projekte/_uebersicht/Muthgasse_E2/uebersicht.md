# Übersicht — Muthgasse_E2

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Pläne 19., Muthgasse 109B - 2026-05-07_13-12\Architekt\Ausführungsplan\M109B_-Plan - AR-AF-A-GR-E2 100 - GRUNDRISS E2.dxf` · Geschoss: `EG` · Bild: 2326×2400 px · Laufzeit 664.1 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 42 |
| Sanitär (BAD/WC) | 19 |
| sonstige typisierte Räume | 9 |
| Außenflächen (BALKON/TERRASSE) | 14 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 5 |
| Stiegenhäuser | 9 |
| Schächte/Lifte | 5 |
| untypisierte Räume (nicht erkannt) | 10 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 8 |
| Ausgänge final_exit | 5 |
| Ausgänge stair_exit | 5 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 146 |
| Räume > 90 % in anderem Raum | 24 |

Räume gesamt: **113**, davon typisiert 103.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| KÜCHE | 23 |
| ZIMMER | 19 |
| BAD | 16 |
| BALKON | 14 |
| STIEGENHAUS | 9 |
| ABSTELLRAUM | 7 |
| LIFT | 5 |
| GANG | 3 |
| WC | 3 |
| VORRAUM | 2 |
| KINDERWAGENRAUM | 1 |
| TECHNIK | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 38 |
| top_2 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_3 | 4 |
| top_4 | 20 |
| top_5 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_6 | 3 |
| top_7 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_8 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 44

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_17 | ZIMMER | raum_85 | KÜCHE | 97.6 % |
| raum_22 | KÜCHE | raum_85 | KÜCHE | 97.7 % |
| raum_25 | ZIMMER | raum_86 | KÜCHE | 98.7 % |
| raum_26 | KÜCHE | raum_86 | KÜCHE | 99.1 % |
| raum_35 | ABSTELLRAUM | raum_90 | ZIMMER | 98.3 % |
| raum_37 | BAD | raum_92 | KÜCHE | 94.7 % |
| raum_67 | — | raum_88 | STIEGENHAUS | 99.3 % |
| raum_76 | BAD | raum_86 | KÜCHE | 94.8 % |
| raum_77 | — | lift_1 | LIFT | 100.0 % |
| raum_78 | — | lift_2 | LIFT | 100.0 % |
| raum_79 | LIFT | raum_88 | STIEGENHAUS | 97.6 % |
| raum_91 | KÜCHE | raum_29 | KÜCHE | 100.0 % |
| raum_93 | KÜCHE | raum_38 | KÜCHE | 91.6 % |
| stiegenhaus_1 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 95.6 % |
| stiegenhaus_2 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 100.0 % |
| stiegenhaus_2 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 100.0 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_2 | STIEGENHAUS | 96.9 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 100.0 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_2 | STIEGENHAUS | 96.0 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 99.1 % |
| stiegenhaus_5 | STIEGENHAUS | stiegenhaus_1 | STIEGENHAUS | 100.0 % |
| stiegenhaus_8 | STIEGENHAUS | lift_5 | LIFT | 100.0 % |
| lift_1 | LIFT | raum_77 | — | 100.0 % |
| lift_2 | LIFT | raum_78 | — | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 10** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
