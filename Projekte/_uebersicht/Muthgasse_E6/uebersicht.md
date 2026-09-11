# Übersicht — Muthgasse_E6

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Pläne 19., Muthgasse 109B - 2026-05-07_13-12\Architekt\Ausführungsplan\M109B_-Plan - AR-AF-A-GR-E6 100 - GRUNDRISS E6.dxf` · Geschoss: `EG` · Bild: 2400×1879 px · Laufzeit 398.0 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 51 |
| Sanitär (BAD/WC) | 22 |
| sonstige typisierte Räume | 8 |
| Außenflächen (BALKON/TERRASSE) | 18 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 11 |
| Stiegenhäuser | 7 |
| Schächte/Lifte | 5 |
| untypisierte Räume (nicht erkannt) | 15 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 5 |
| Ausgänge final_exit | 1 |
| Ausgänge stair_exit | 3 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 193 |
| Räume > 90 % in anderem Raum | 29 |

Räume gesamt: **137**, davon typisiert 122.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| KÜCHE | 30 |
| ZIMMER | 21 |
| BAD | 18 |
| BALKON | 18 |
| VORRAUM | 8 |
| ABSTELLRAUM | 7 |
| STIEGENHAUS | 7 |
| LIFT | 5 |
| WC | 4 |
| GANG | 3 |
| KINDERWAGENRAUM | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 9 |
| top_2 | 21 |
| top_3 | 34 |
| top_4 | 16 |
| top_5 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 56

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_7 | KÜCHE | raum_124 | KÜCHE | 99.2 % |
| raum_13 | KÜCHE | raum_116 | KÜCHE | 99.0 % |
| raum_26 | KÜCHE | raum_122 | KÜCHE | 98.0 % |
| raum_36 | KÜCHE | raum_115 | KÜCHE | 97.8 % |
| raum_38 | KÜCHE | raum_114 | KÜCHE | 95.9 % |
| raum_56 | KÜCHE | raum_120 | KÜCHE | 98.7 % |
| raum_80 | KÜCHE | raum_123 | KÜCHE | 95.8 % |
| raum_87 | WC | raum_124 | KÜCHE | 98.1 % |
| raum_88 | — | raum_124 | KÜCHE | 97.0 % |
| raum_108 | — | raum_116 | KÜCHE | 96.7 % |
| raum_111 | — | lift_1 | LIFT | 100.0 % |
| raum_112 | — | lift_2 | LIFT | 100.0 % |
| raum_117 | VORRAUM | raum_21 | KÜCHE | 98.0 % |
| raum_118 | KÜCHE | raum_62 | KÜCHE | 92.3 % |
| raum_119 | KÜCHE | raum_62 | KÜCHE | 96.9 % |
| raum_121 | KÜCHE | raum_18 | KÜCHE | 100.0 % |
| raum_123 | KÜCHE | raum_80 | KÜCHE | 97.6 % |
| raum_127 | BALKON | raum_59 | KÜCHE | 91.0 % |
| stiegenhaus_1 | STIEGENHAUS | stiegenhaus_2 | STIEGENHAUS | 100.0 % |
| stiegenhaus_2 | STIEGENHAUS | stiegenhaus_1 | STIEGENHAUS | 95.6 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 100.0 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 100.0 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 91.6 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 100.0 % |
| stiegenhaus_5 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 90.6 % |
| stiegenhaus_5 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 98.9 % |
| stiegenhaus_6 | STIEGENHAUS | lift_5 | LIFT | 100.0 % |
| lift_1 | LIFT | raum_111 | — | 100.0 % |
| lift_2 | LIFT | raum_112 | — | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 15** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
