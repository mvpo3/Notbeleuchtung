# Übersicht — EG_Grundriss_DE_NEU

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\EG_Grundriss_DE_NEU.dxf` · Geschoss: `EG` · Bild: 1800×1233 px · Laufzeit 8.0 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 4 |
| Sanitär (BAD/WC) | 1 |
| sonstige typisierte Räume | 1 |
| Außenflächen (BALKON/TERRASSE) | 0 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 4 |
| Stiegenhäuser | 1 |
| Schächte/Lifte | 1 |
| untypisierte Räume (nicht erkannt) | 2 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 4 |
| Ausgänge final_exit | 1 |
| Ausgänge stair_exit | 1 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 6 |
| Räume > 90 % in anderem Raum | 0 |

Räume gesamt: **14**, davon typisiert 12.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| GANG | 2 |
| KÜCHE | 2 |
| VORRAUM | 2 |
| ABSTELLRAUM | 1 |
| BAD | 1 |
| SCHACHT | 1 |
| STIEGENHAUS | 1 |
| WOHNZIMMER | 1 |
| ZIMMER | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 2 |
| top_2 | 4 |
| top_3 | 2 |
| top_4 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 5

## NICHT erkannt

- **untypisierte Räume: 2** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Außenflächen (BALKON/TERRASSE): **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
