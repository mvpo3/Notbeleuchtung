# Übersicht — Muthgasse_E3

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Pläne 19., Muthgasse 109B - 2026-05-07_13-12\Architekt\Ausführungsplan\M109B_-Plan - AR-AF-A-GR-E3 100 - GRUNDRISS E3.dxf` · Geschoss: `EG` · Bild: 2400×1795 px · Laufzeit 388.9 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 51 |
| Sanitär (BAD/WC) | 26 |
| sonstige typisierte Räume | 8 |
| Außenflächen (BALKON/TERRASSE) | 17 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 6 |
| Stiegenhäuser | 7 |
| Schächte/Lifte | 6 |
| untypisierte Räume (nicht erkannt) | 14 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 4 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 3 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 184 |
| Räume > 90 % in anderem Raum | 31 |

Räume gesamt: **135**, davon typisiert 121.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| KÜCHE | 28 |
| ZIMMER | 23 |
| BAD | 19 |
| BALKON | 17 |
| ABSTELLRAUM | 7 |
| STIEGENHAUS | 7 |
| WC | 7 |
| LIFT | 6 |
| GANG | 3 |
| VORRAUM | 3 |
| KINDERWAGENRAUM | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 46 |
| top_2 | 18 |
| top_3 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_4 | 21 |

Räume ohne `wohnung_id`: 49

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_2 | ZIMMER | raum_117 | KÜCHE | 99.0 % |
| raum_3 | KÜCHE | raum_118 | KÜCHE | 98.4 % |
| raum_7 | KÜCHE | raum_117 | KÜCHE | 98.8 % |
| raum_11 | KÜCHE | raum_116 | KÜCHE | 98.9 % |
| raum_13 | ZIMMER | raum_114 | KÜCHE | 98.5 % |
| raum_23 | ZIMMER | raum_112 | KÜCHE | 97.3 % |
| raum_52 | KÜCHE | raum_121 | KÜCHE | 97.4 % |
| raum_54 | KÜCHE | raum_120 | KÜCHE | 98.1 % |
| raum_55 | ZIMMER | raum_120 | KÜCHE | 98.0 % |
| raum_56 | KÜCHE | raum_119 | KÜCHE | 96.6 % |
| raum_64 | — | raum_115 | KÜCHE | 91.8 % |
| raum_65 | ZIMMER | raum_118 | KÜCHE | 98.4 % |
| raum_68 | — | raum_108 | ZIMMER | 98.9 % |
| raum_87 | — | raum_121 | KÜCHE | 90.7 % |
| raum_88 | BAD | lift_1 | LIFT | 100.0 % |
| raum_104 | — | lift_2 | LIFT | 100.0 % |
| raum_105 | — | lift_3 | LIFT | 100.0 % |
| raum_109 | STIEGENHAUS | raum_106 | LIFT | 96.3 % |
| raum_115 | KÜCHE | raum_64 | — | 95.6 % |
| stiegenhaus_1 | STIEGENHAUS | stiegenhaus_2 | STIEGENHAUS | 100.0 % |
| stiegenhaus_2 | STIEGENHAUS | stiegenhaus_1 | STIEGENHAUS | 95.6 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 100.0 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 100.0 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 97.3 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 100.0 % |
| stiegenhaus_5 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 96.4 % |
| stiegenhaus_5 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 99.1 % |
| stiegenhaus_6 | STIEGENHAUS | lift_6 | LIFT | 100.0 % |
| lift_1 | LIFT | raum_88 | BAD | 100.0 % |
| lift_2 | LIFT | raum_104 | — | 100.0 % |
| lift_3 | LIFT | raum_105 | — | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 14** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
