# Übersicht — Rennweg_DG2

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Rennweg\DG2 - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf` · Geschoss: `DG` · Bild: 1607×1800 px · Laufzeit 13.5 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 2 |
| Sanitär (BAD/WC) | 1 |
| sonstige typisierte Räume | 0 |
| Außenflächen (BALKON/TERRASSE) | 1 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 3 |
| Stiegenhäuser | 5 |
| Schächte/Lifte | 2 |
| untypisierte Räume (nicht erkannt) | 0 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 1 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 3 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 18 |
| Räume > 90 % in anderem Raum | 2 |

Räume gesamt: **14**, davon typisiert 14.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| STIEGENHAUS | 5 |
| VORRAUM | 3 |
| ZIMMER | 2 |
| BAD | 1 |
| LIFT | 1 |
| SCHACHT | 1 |
| TERRASSE | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 4 |

Räume ohne `wohnung_id`: 10

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| rest_3 | STIEGENHAUS | stiegenhaus_2 | STIEGENHAUS | 96.9 % |
| rest_4 | STIEGENHAUS | stiegenhaus_2 | STIEGENHAUS | 99.5 % |

## NICHT erkannt

- untypisierte Räume: 0 — jeder Raum trägt einen `raum_typ`.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
