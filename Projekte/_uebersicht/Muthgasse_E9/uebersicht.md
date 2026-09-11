# Übersicht — Muthgasse_E9

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Pläne 19., Muthgasse 109B - 2026-05-07_13-12\Architekt\Ausführungsplan\M109B_-Plan - AR-AF-A-GR-E9 100 - GRUNDRISS E9.dxf` · Geschoss: `EG` · Bild: 2400×1777 px · Laufzeit 416.4 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 20 |
| Sanitär (BAD/WC) | 10 |
| sonstige typisierte Räume | 5 |
| Außenflächen (BALKON/TERRASSE) | 8 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 5 |
| Stiegenhäuser | 8 |
| Schächte/Lifte | 6 |
| untypisierte Räume (nicht erkannt) | 7 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 3 |
| Ausgänge final_exit | 2 |
| Ausgänge stair_exit | 3 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 89 |
| Räume > 90 % in anderem Raum | 27 |

Räume gesamt: **69**, davon typisiert 62.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| KÜCHE | 11 |
| BAD | 9 |
| ZIMMER | 9 |
| STIEGENHAUS | 8 |
| BALKON | 7 |
| LIFT | 6 |
| ABSTELLRAUM | 3 |
| VORRAUM | 3 |
| GANG | 2 |
| KINDERWAGENRAUM | 1 |
| TECHNIK | 1 |
| TERRASSE | 1 |
| WC | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 28 |
| top_2 | 4 |
| top_3 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 36

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_20 | KÜCHE | raum_50 | KÜCHE | 99.0 % |
| raum_21 | ZIMMER | raum_50 | KÜCHE | 98.3 % |
| raum_22 | ZIMMER | raum_50 | KÜCHE | 99.7 % |
| raum_23 | VORRAUM | raum_50 | KÜCHE | 99.2 % |
| raum_25 | BAD | raum_50 | KÜCHE | 94.1 % |
| raum_27 | KÜCHE | raum_51 | KÜCHE | 98.6 % |
| raum_34 | ABSTELLRAUM | raum_50 | KÜCHE | 98.9 % |
| raum_39 | BAD | lift_1 | LIFT | 100.0 % |
| raum_44 | — | lift_2 | LIFT | 100.0 % |
| raum_45 | — | lift_3 | LIFT | 100.0 % |
| raum_53 | BALKON | raum_14 | KÜCHE | 90.5 % |
| stiegenhaus_1 | STIEGENHAUS | stiegenhaus_2 | STIEGENHAUS | 100.0 % |
| stiegenhaus_2 | STIEGENHAUS | stiegenhaus_1 | STIEGENHAUS | 100.0 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 100.0 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 100.0 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 100.0 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 100.0 % |
| stiegenhaus_5 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 94.8 % |
| stiegenhaus_5 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 94.8 % |
| stiegenhaus_6 | STIEGENHAUS | stiegenhaus_1 | STIEGENHAUS | 100.0 % |
| stiegenhaus_6 | STIEGENHAUS | stiegenhaus_2 | STIEGENHAUS | 100.0 % |
| stiegenhaus_6 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 100.0 % |
| stiegenhaus_6 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 100.0 % |
| stiegenhaus_6 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 100.0 % |
| lift_1 | LIFT | raum_39 | BAD | 97.6 % |
| lift_2 | LIFT | raum_44 | — | 100.0 % |
| lift_3 | LIFT | raum_45 | — | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 7** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
