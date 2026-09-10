# Übersicht — Mollgasse_KG1

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Mollgasse\1.Kellergeschoß.dxf` · Geschoss: `EG` · Bild: 1206×1800 px · Laufzeit 43.2 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 0 |
| Sanitär (BAD/WC) | 0 |
| sonstige typisierte Räume | 1 |
| Außenflächen (BALKON/TERRASSE) | 0 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 2 |
| Stiegenhäuser | 2 |
| Schächte/Lifte | 2 |
| untypisierte Räume (nicht erkannt) | 24 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 0 |
| Ausgänge final_exit | 2 |
| Ausgänge stair_exit | 0 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 4 |
| Räume > 90 % in anderem Raum | 0 |

Räume gesamt: **31**, davon typisiert 7.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| GANG | 2 |
| LIFT | 2 |
| STIEGENHAUS | 2 |
| GARAGE | 1 |

## NICHT erkannt

- **untypisierte Räume: 24** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Außenflächen (BALKON/TERRASSE): **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `stair_exit`: **0** — kein Stiegenhaus-Ausgang erkannt.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Wohnungen: **0** — keine `wohnung_id` vergeben.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
