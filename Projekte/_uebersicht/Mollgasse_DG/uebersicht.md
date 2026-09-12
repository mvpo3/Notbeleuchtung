# Übersicht — Mollgasse_DG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Mollgasse\Dachgeschoß.dxf` · Geschoss: `EG` · Bild: 2400×2235 px · Laufzeit 57.0 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 11 |
| Sanitär (BAD/WC) | 9 |
| sonstige typisierte Räume | 4 |
| Außenflächen (BALKON/TERRASSE) | 1 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 5 |
| Stiegenhäuser | 1 |
| Schächte/Lifte | 3 |
| untypisierte Räume (nicht erkannt) | 1 |
| Innenhöfe (geschlossene Außenflächen) | 2 |
| Wohnungen | 5 |
| Ausgänge final_exit | 1 |
| Ausgänge stair_exit | 0 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 5 |
| Räume > 90 % in anderem Raum | 1 |

Räume gesamt: **35**, davon typisiert 34.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 9 |
| BAD | 6 |
| ABSTELLRAUM | 4 |
| VORRAUM | 3 |
| WC | 3 |
| GANG | 2 |
| KÜCHE | 2 |
| LIFT | 2 |
| SCHACHT | 1 |
| STIEGENHAUS | 1 |
| TERRASSE | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 10 |
| top_2 | 8 |
| top_3 | 5 |
| top_4 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_5 | 2 |

Räume ohne `wohnung_id`: 9

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| lift_2 | LIFT | raum_31 | — | 95.1 % |

## NICHT erkannt

- **untypisierte Räume: 1** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- `stair_exit`: **0** — kein Stiegenhaus-Ausgang erkannt.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
