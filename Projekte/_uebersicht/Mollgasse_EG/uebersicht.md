# Übersicht — Mollgasse_EG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Mollgasse\Erdgeschoß.dxf` · Geschoss: `EG` · Bild: 1800×1592 px · Laufzeit 87.3 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 11 |
| Sanitär (BAD/WC) | 11 |
| sonstige typisierte Räume | 11 |
| Außenflächen (BALKON/TERRASSE) | 1 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 16 |
| Stiegenhäuser | 2 |
| Schächte/Lifte | 2 |
| untypisierte Räume (nicht erkannt) | 10 |
| Innenhöfe (geschlossene Außenflächen) | 1 |
| Wohnungen | 8 |
| Ausgänge final_exit | 9 |
| Ausgänge stair_exit | 4 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 126 |
| Räume > 90 % in anderem Raum | 2 |

Räume gesamt: **64**, davon typisiert 54.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| GANG | 11 |
| ZIMMER | 10 |
| BAD | 6 |
| ABSTELLRAUM | 5 |
| VORRAUM | 5 |
| WC | 5 |
| KINDERWAGENRAUM | 2 |
| LIFT | 2 |
| MUELLRAUM | 2 |
| STIEGENHAUS | 2 |
| GARAGE | 1 |
| KÜCHE | 1 |
| TECHNIK | 1 |
| TERRASSE | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 3 |
| top_2 | 2 |
| top_3 | 14 |
| top_4 | 3 |
| top_5 | 8 |
| top_6 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_7 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_8 | 2 |

Räume ohne `wohnung_id`: 30

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_1 | — | raum_3 | GANG | 100.0 % |
| raum_53 | KINDERWAGENRAUM | raum_51 | STIEGENHAUS | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 10** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 154 Knoten / 119 Kanten.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
