# Übersicht — Muthgasse_E4

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Pläne 19., Muthgasse 109B - 2026-05-07_13-12\Architekt\Ausführungsplan\M109B_-Plan - AR-AF-A-GR-E4 100 - GRUNDRISS E4.dxf` · Geschoss: `EG` · Bild: 2400×1879 px · Laufzeit 390.2 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 51 |
| Sanitär (BAD/WC) | 25 |
| sonstige typisierte Räume | 9 |
| Außenflächen (BALKON/TERRASSE) | 17 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 6 |
| Stiegenhäuser | 6 |
| Schächte/Lifte | 6 |
| untypisierte Räume (nicht erkannt) | 12 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 5 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 3 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 185 |
| Räume > 90 % in anderem Raum | 33 |

Räume gesamt: **132**, davon typisiert 120.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| KÜCHE | 28 |
| ZIMMER | 23 |
| BAD | 18 |
| BALKON | 17 |
| ABSTELLRAUM | 8 |
| WC | 7 |
| LIFT | 6 |
| STIEGENHAUS | 6 |
| GANG | 3 |
| VORRAUM | 3 |
| KINDERWAGENRAUM | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 43 |
| top_2 | 21 |
| top_3 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_4 | 19 |
| top_5 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 47

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_2 | KÜCHE | raum_115 | KÜCHE | 98.0 % |
| raum_6 | KÜCHE | raum_114 | KÜCHE | 98.2 % |
| raum_10 | KÜCHE | raum_113 | KÜCHE | 97.4 % |
| raum_25 | KÜCHE | raum_120 | KÜCHE | 98.8 % |
| raum_41 | KÜCHE | raum_118 | KÜCHE | 97.0 % |
| raum_43 | KÜCHE | raum_117 | KÜCHE | 98.0 % |
| raum_44 | ZIMMER | raum_117 | KÜCHE | 98.2 % |
| raum_47 | VORRAUM | raum_112 | KÜCHE | 90.8 % |
| raum_50 | VORRAUM | raum_120 | KÜCHE | 97.9 % |
| raum_51 | — | raum_120 | KÜCHE | 98.6 % |
| raum_67 | ZIMMER | raum_111 | KÜCHE | 98.7 % |
| raum_71 | — | lift_1 | LIFT | 100.0 % |
| raum_80 | — | raum_111 | KÜCHE | 95.2 % |
| raum_82 | KÜCHE | raum_111 | KÜCHE | 97.0 % |
| raum_101 | BAD | raum_118 | KÜCHE | 90.7 % |
| raum_104 | — | lift_2 | LIFT | 100.0 % |
| raum_105 | — | lift_3 | LIFT | 100.0 % |
| raum_110 | KÜCHE | raum_16 | KÜCHE | 94.4 % |
| raum_112 | KÜCHE | raum_47 | VORRAUM | 97.0 % |
| raum_113 | KÜCHE | raum_10 | KÜCHE | 98.0 % |
| raum_115 | KÜCHE | raum_2 | KÜCHE | 97.6 % |
| stiegenhaus_1 | STIEGENHAUS | stiegenhaus_2 | STIEGENHAUS | 100.0 % |
| stiegenhaus_2 | STIEGENHAUS | stiegenhaus_1 | STIEGENHAUS | 95.6 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 100.0 % |
| stiegenhaus_3 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 100.0 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 91.6 % |
| stiegenhaus_4 | STIEGENHAUS | stiegenhaus_5 | STIEGENHAUS | 100.0 % |
| stiegenhaus_5 | STIEGENHAUS | stiegenhaus_3 | STIEGENHAUS | 90.6 % |
| stiegenhaus_5 | STIEGENHAUS | stiegenhaus_4 | STIEGENHAUS | 98.9 % |
| stiegenhaus_6 | STIEGENHAUS | lift_5 | LIFT | 100.0 % |
| lift_1 | LIFT | raum_71 | — | 100.0 % |
| lift_2 | LIFT | raum_104 | — | 100.0 % |
| lift_3 | LIFT | raum_105 | — | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 12** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
