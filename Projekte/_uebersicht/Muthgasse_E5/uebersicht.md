# Übersicht — Muthgasse_E5

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Pläne 19., Muthgasse 109B - 2026-05-07_13-12\Architekt\Ausführungsplan\M109B_-Plan - AR-AF-A-GR-E5 100 - GRUNDRISS E5.dxf` · Geschoss: `EG` · Bild: 2400×1772 px · Laufzeit 393.8 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 48 |
| Sanitär (BAD/WC) | 20 |
| sonstige typisierte Räume | 11 |
| Außenflächen (BALKON/TERRASSE) | 18 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 11 |
| Stiegenhäuser | 6 |
| Schächte/Lifte | 6 |
| untypisierte Räume (nicht erkannt) | 13 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 4 |
| Ausgänge final_exit | 1 |
| Ausgänge stair_exit | 2 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 194 |
| Räume > 90 % in anderem Raum | 35 |

Räume gesamt: **133**, davon typisiert 120.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| KÜCHE | 27 |
| ZIMMER | 21 |
| BAD | 18 |
| BALKON | 18 |
| ABSTELLRAUM | 10 |
| VORRAUM | 7 |
| LIFT | 6 |
| STIEGENHAUS | 6 |
| GANG | 4 |
| WC | 2 |
| KINDERWAGENRAUM | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 9 |
| top_2 | 22 |
| top_3 | 15 |
| top_4 | 33 |

Räume ohne `wohnung_id`: 54

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_13 | KÜCHE | raum_120 | KÜCHE | 98.6 % |
| raum_17 | KÜCHE | raum_115 | KÜCHE | 98.7 % |
| raum_18 | — | raum_113 | ZIMMER | 98.8 % |
| raum_22 | ZIMMER | raum_117 | KÜCHE | 98.9 % |
| raum_23 | BAD | raum_117 | KÜCHE | 90.2 % |
| raum_24 | KÜCHE | raum_117 | KÜCHE | 98.4 % |
| raum_35 | KÜCHE | raum_121 | KÜCHE | 97.6 % |
| raum_44 | ABSTELLRAUM | raum_115 | KÜCHE | 94.8 % |
| raum_78 | ZIMMER | raum_115 | KÜCHE | 99.1 % |
| raum_79 | VORRAUM | raum_115 | KÜCHE | 99.3 % |
| raum_80 | ZIMMER | raum_115 | KÜCHE | 99.7 % |
| raum_81 | BAD | raum_115 | KÜCHE | 93.0 % |
| raum_83 | ABSTELLRAUM | raum_115 | KÜCHE | 98.7 % |
| raum_89 | ABSTELLRAUM | raum_119 | KÜCHE | 99.1 % |
| raum_90 | ABSTELLRAUM | raum_119 | KÜCHE | 94.8 % |
| raum_92 | KÜCHE | raum_119 | KÜCHE | 99.5 % |
| raum_94 | KÜCHE | raum_114 | KÜCHE | 96.6 % |
| raum_95 | — | raum_120 | KÜCHE | 97.0 % |
| raum_105 | — | lift_1 | LIFT | 100.0 % |
| raum_108 | VORRAUM | raum_118 | KÜCHE | 96.8 % |
| raum_109 | — | lift_2 | LIFT | 100.0 % |
| raum_110 | — | lift_3 | LIFT | 100.0 % |
| raum_114 | KÜCHE | raum_94 | KÜCHE | 97.5 % |
| stiegenhaus_1 | STIEGENHAUS | stiegenhaus_2 | STIEGENHAUS | 100.0 % |
| stiegenhaus_2 | STIEGENHAUS | stiegenhaus_1 | STIEGENHAUS | 95.6 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 100.0 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 100.0 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 91.6 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 100.0 % |
| stiegenhaus_5 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 90.6 % |
| stiegenhaus_5 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 98.9 % |
| stiegenhaus_6 | STIEGENHAUS | lift_6 | LIFT | 100.0 % |
| lift_1 | LIFT | raum_105 | — | 100.0 % |
| lift_2 | LIFT | raum_109 | — | 100.0 % |
| lift_3 | LIFT | raum_110 | — | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 13** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
