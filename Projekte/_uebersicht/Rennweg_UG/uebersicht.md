# Übersicht — Rennweg_UG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Rennweg\UG - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf` · Geschoss: `UG` · Bild: 1800×1765 px · Laufzeit 11.4 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 0 |
| Sanitär (BAD/WC) | 3 |
| sonstige typisierte Räume | 3 |
| Außenflächen (BALKON/TERRASSE) | 0 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 3 |
| Stiegenhäuser | 3 |
| Schächte/Lifte | 1 |
| untypisierte Räume (nicht erkannt) | 10 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 4 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 2 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 6 |
| Räume > 90 % in anderem Raum | 0 |

Räume gesamt: **23**, davon typisiert 13.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| STIEGENHAUS | 3 |
| WC | 3 |
| GANG | 2 |
| ABSTELLRAUM | 1 |
| KINDERWAGENRAUM | 1 |
| LIFT | 1 |
| TECHNIK | 1 |
| VORRAUM | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_2 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_3 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_4 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 19

## NICHT erkannt

- **untypisierte Räume: 10** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Außenflächen (BALKON/TERRASSE): **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
