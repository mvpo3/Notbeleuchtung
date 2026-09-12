# Übersicht — Herrenholz_UG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\DXF_Herrenholzgasse\20230228_po_ug_V.dxf` · Geschoss: `UG` · Bild: 2400×943 px · Laufzeit 125.8 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 55 |
| Sanitär (BAD/WC) | 0 |
| sonstige typisierte Räume | 2 |
| Außenflächen (BALKON/TERRASSE) | 46 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 14 |
| Stiegenhäuser | 0 |
| Schächte/Lifte | 0 |
| untypisierte Räume (nicht erkannt) | 38 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 23 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 0 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 14 |
| Räume > 90 % in anderem Raum | 11 |

Räume gesamt: **155**, davon typisiert 117.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 55 |
| TERRASSE | 46 |
| GANG | 14 |
| MUELLRAUM | 2 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 3 |
| top_10 | 3 |
| top_11 | 3 |
| top_12 | 3 |
| top_13 | 3 |
| top_14 | 3 |
| top_15 | 3 |
| top_16 | 3 |
| top_17 | 3 |
| top_18 | 3 |
| top_19 | 3 |
| top_2 | 3 |
| top_20 | 3 |
| top_21 | 3 |
| top_22 | 3 |
| top_23 | 3 |
| top_3 | 3 |
| top_4 | 3 |
| top_5 | 3 |
| top_6 | 3 |
| top_7 | 3 |
| top_8 | 3 |
| top_9 | 3 |

Räume ohne `wohnung_id`: 86

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_19 | ZIMMER | raum_148 | MUELLRAUM | 98.7 % |
| raum_137 | — | raum_87 | — | 100.0 % |
| raum_138 | — | raum_18 | — | 100.0 % |
| raum_139 | — | raum_17 | — | 100.0 % |
| raum_140 | — | raum_16 | — | 100.0 % |
| raum_141 | — | raum_15 | — | 100.0 % |
| raum_142 | — | raum_74 | — | 100.0 % |
| raum_143 | — | raum_136 | — | 100.0 % |
| raum_144 | — | raum_76 | — | 100.0 % |
| raum_145 | — | raum_71 | — | 100.0 % |
| raum_146 | — | raum_79 | — | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 38** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Stiegenhäuser: **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- Schächte/Lifte: **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `stair_exit`: **0** — kein Stiegenhaus-Ausgang erkannt.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
