# Übersicht — Mollgasse_KG2

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Mollgasse\2.Kellergeschoß.dxf` · Geschoss: `EG` · Bild: 1800×1662 px · Laufzeit 69.8 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 0 |
| Sanitär (BAD/WC) | 0 |
| sonstige typisierte Räume | 3 |
| Außenflächen (BALKON/TERRASSE) | 0 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 2 |
| Stiegenhäuser | 3 |
| Schächte/Lifte | 3 |
| untypisierte Räume (nicht erkannt) | 19 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 1 |
| Ausgänge final_exit | 3 |
| Ausgänge stair_exit | 6 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 15 |
| Räume > 90 % in anderem Raum | 0 |

Räume gesamt: **30**, davon typisiert 11.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| STIEGENHAUS | 3 |
| GANG | 2 |
| LIFT | 2 |
| ABSTELLRAUM | 1 |
| GARAGE | 1 |
| SCHACHT | 1 |
| TECHNIK | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 29

## NICHT erkannt

- **untypisierte Räume: 19** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Außenflächen (BALKON/TERRASSE): **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
