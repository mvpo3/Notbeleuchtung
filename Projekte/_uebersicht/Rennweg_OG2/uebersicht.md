# Übersicht — Rennweg_OG2

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Rennweg\OG2 - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf` · Geschoss: `OG2` · Bild: 1800×1774 px · Laufzeit 14.6 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 5 |
| Sanitär (BAD/WC) | 4 |
| sonstige typisierte Räume | 0 |
| Außenflächen (BALKON/TERRASSE) | 2 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 5 |
| Stiegenhäuser | 1 |
| Schächte/Lifte | 1 |
| untypisierte Räume (nicht erkannt) | 1 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 2 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 0 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 2 |
| Räume > 90 % in anderem Raum | 2 |

Räume gesamt: **19**, davon typisiert 18.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 5 |
| VORRAUM | 4 |
| BAD | 3 |
| TERRASSE | 2 |
| GANG | 1 |
| LIFT | 1 |
| STIEGENHAUS | 1 |
| WC | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 11 |
| top_2 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 7

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_1 | ZIMMER | raum_17 | VORRAUM | 92.3 % |
| raum_11 | BAD | raum_17 | VORRAUM | 96.5 % |

## NICHT erkannt

- **untypisierte Räume: 1** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `stair_exit`: **0** — kein Stiegenhaus-Ausgang erkannt.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
