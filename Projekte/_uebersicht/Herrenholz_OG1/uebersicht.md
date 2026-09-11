# Übersicht — Herrenholz_OG1

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\DXF_Herrenholzgasse\20230228_po_1og_V.dxf` · Geschoss: `1OG` · Bild: 2400×1028 px · Laufzeit 205.7 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 107 |
| Sanitär (BAD/WC) | 92 |
| sonstige typisierte Räume | 23 |
| Außenflächen (BALKON/TERRASSE) | 0 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 55 |
| Stiegenhäuser | 0 |
| Schächte/Lifte | 0 |
| untypisierte Räume (nicht erkannt) | 23 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 47 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 0 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 55 |
| Räume > 90 % in anderem Raum | 0 |

Räume gesamt: **300**, davon typisiert 277.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| ZIMMER | 107 |
| GANG | 55 |
| BAD | 46 |
| WC | 46 |
| ABSTELLRAUM | 23 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 5 |
| top_10 | 5 |
| top_11 | 5 |
| top_12 | 7 |
| top_13 | 7 |
| top_14 | 7 |
| top_15 | 7 |
| top_16 | 7 |
| top_17 | 7 |
| top_18 | 7 |
| top_19 | 7 |
| top_2 | 3 |
| top_20 | 7 |
| top_21 | 4 |
| top_22 | 7 |
| top_23 | 7 |
| top_24 | 7 |
| top_25 | 7 |
| top_26 | 7 |
| top_27 | 7 |
| top_28 | 7 |
| top_29 | 7 |
| top_3 | 3 |
| top_30 | 7 |
| top_31 | 7 |
| top_32 | 7 |
| top_33 | 7 |
| top_34 | 5 |
| top_35 | 3 |
| top_36 | 5 |
| top_37 | 4 |
| top_38 | 4 |
| top_39 | 7 |
| top_4 | 5 |
| top_40 | 7 |
| top_41 | 5 |
| top_42 | 3 |
| top_43 | 1  ⚠ nur 1 Raum — Zusammenhang unsicher |
| top_44 | 3 |
| top_45 | 3 |
| top_46 | 3 |
| top_47 | 3 |
| top_5 | 3 |
| top_6 | 5 |
| top_7 | 5 |
| top_8 | 5 |
| top_9 | 5 |

Räume ohne `wohnung_id`: 44

## NICHT erkannt

- **untypisierte Räume: 23** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Stiegenhäuser: **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- Schächte/Lifte: **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- Außenflächen (BALKON/TERRASSE): **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `stair_exit`: **0** — kein Stiegenhaus-Ausgang erkannt.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
