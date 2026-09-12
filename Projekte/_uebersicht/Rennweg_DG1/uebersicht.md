# Übersicht — Rennweg_DG1

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Rennweg\DG1 - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf` · Geschoss: `DG` · Bild: 1375×1800 px · Laufzeit 11.6 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 3 |
| Sanitär (BAD/WC) | 3 |
| sonstige typisierte Räume | 1 |
| Außenflächen (BALKON/TERRASSE) | 1 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 2 |
| Stiegenhäuser | 2 |
| Schächte/Lifte | 2 |
| untypisierte Räume (nicht erkannt) | 1 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 1 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 1 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 5 |
| Räume > 90 % in anderem Raum | 1 |

Räume gesamt: **15**, davon typisiert 14.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| BAD | 2 |
| STIEGENHAUS | 2 |
| ZIMMER | 2 |
| ABSTELLRAUM | 1 |
| BALKON | 1 |
| GANG | 1 |
| LIFT | 1 |
| SCHACHT | 1 |
| VORRAUM | 1 |
| WC | 1 |
| WOHNZIMMER | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 8 |

Räume ohne `wohnung_id`: 7

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_11 | ABSTELLRAUM | raum_1 | WOHNZIMMER | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 1** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
