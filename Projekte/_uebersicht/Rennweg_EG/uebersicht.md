# Übersicht — Rennweg_EG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Rennweg\EG - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf` · Geschoss: `EG` · Bild: 1307×2400 px · Laufzeit 13.2 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 3 |
| Sanitär (BAD/WC) | 1 |
| sonstige typisierte Räume | 3 |
| Außenflächen (BALKON/TERRASSE) | 2 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 2 |
| Stiegenhäuser | 5 |
| Schächte/Lifte | 1 |
| untypisierte Räume (nicht erkannt) | 5 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 2 |
| Ausgänge final_exit | 3 |
| Ausgänge stair_exit | 5 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 9 |
| Räume > 90 % in anderem Raum | 0 |

Räume gesamt: **22**, davon typisiert 17.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| STIEGENHAUS | 5 |
| KÜCHE | 2 |
| TERRASSE | 2 |
| ABSTELLRAUM | 1 |
| BAD | 1 |
| GANG | 1 |
| GARAGE | 1 |
| LIFT | 1 |
| MUELLRAUM | 1 |
| VORRAUM | 1 |
| ZIMMER | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 4 |
| top_2 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |

Räume ohne `wohnung_id`: 17

## NICHT erkannt

- **untypisierte Räume: 5** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
