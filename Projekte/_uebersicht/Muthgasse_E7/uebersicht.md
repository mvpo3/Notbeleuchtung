# Übersicht — Muthgasse_E7

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Pläne 19., Muthgasse 109B - 2026-05-07_13-12\Architekt\Ausführungsplan\M109B_-Plan - AR-AF-A-GR-E7 100 - GRUNDRISS E7.dxf` · Geschoss: `EG` · Bild: 2400×1515 px · Laufzeit 376.6 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 40 |
| Sanitär (BAD/WC) | 20 |
| sonstige typisierte Räume | 6 |
| Außenflächen (BALKON/TERRASSE) | 15 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 7 |
| Stiegenhäuser | 6 |
| Schächte/Lifte | 5 |
| untypisierte Räume (nicht erkannt) | 8 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 4 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 2 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 160 |
| Räume > 90 % in anderem Raum | 24 |

Räume gesamt: **107**, davon typisiert 99.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| KÜCHE | 23 |
| ZIMMER | 17 |
| BALKON | 14 |
| BAD | 13 |
| WC | 7 |
| STIEGENHAUS | 6 |
| ABSTELLRAUM | 5 |
| LIFT | 5 |
| VORRAUM | 5 |
| GANG | 2 |
| KINDERWAGENRAUM | 1 |
| TERRASSE | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 46 |
| top_2 | 18 |
| top_3 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_4 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 41

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_7 | KÜCHE | raum_96 | KÜCHE | 98.7 % |
| raum_15 | KÜCHE | raum_95 | KÜCHE | 98.4 % |
| raum_16 | KÜCHE | raum_94 | KÜCHE | 98.2 % |
| raum_17 | ZIMMER | raum_94 | KÜCHE | 90.6 % |
| raum_59 | KÜCHE | raum_91 | KÜCHE | 91.9 % |
| raum_61 | KÜCHE | raum_90 | KÜCHE | 98.4 % |
| raum_73 | WC | raum_92 | KÜCHE | 97.0 % |
| raum_80 | KÜCHE | raum_92 | KÜCHE | 99.1 % |
| raum_81 | WC | raum_92 | KÜCHE | 96.3 % |
| raum_86 | — | lift_1 | LIFT | 100.0 % |
| raum_87 | — | lift_2 | LIFT | 100.0 % |
| raum_91 | KÜCHE | raum_59 | KÜCHE | 98.1 % |
| raum_97 | KÜCHE | raum_46 | KÜCHE | 94.8 % |
| stiegenhaus_1 | STIEGENHAUS | stiegenhaus_2 | STIEGENHAUS | 100.0 % |
| stiegenhaus_2 | STIEGENHAUS | stiegenhaus_1 | STIEGENHAUS | 95.6 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 100.0 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 100.0 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 91.6 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 100.0 % |
| stiegenhaus_5 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 90.6 % |
| stiegenhaus_5 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 98.9 % |
| stiegenhaus_6 | STIEGENHAUS | lift_5 | LIFT | 100.0 % |
| lift_1 | LIFT | raum_86 | — | 100.0 % |
| lift_2 | LIFT | raum_87 | — | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 8** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
