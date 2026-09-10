# Übersicht — Fischamend_E_BT1_DG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\BVH Fischamenderstraße\fertige Elektromontagepläne\BT1\Elektromontageapläne_DACHGESCHOSS BT1.dxf` · Geschoss: `EG` · Bild: 1800×909 px · Laufzeit 32.2 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 18 |
| Sanitär (BAD/WC) | 6 |
| sonstige typisierte Räume | 0 |
| Außenflächen (BALKON/TERRASSE) | 5 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 8 |
| Stiegenhäuser | 1 |
| Schächte/Lifte | 1 |
| untypisierte Räume (nicht erkannt) | 6 |
| Innenhöfe (geschlossene Außenflächen) | 0 |
| Wohnungen | 2 |
| Ausgänge final_exit | 1 |
| Ausgänge stair_exit | 1 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 39 |
| Räume > 90 % in anderem Raum | 7 |

Räume gesamt: **45**, davon typisiert 39.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| KÜCHE | 8 |
| BAD | 6 |
| VORRAUM | 6 |
| TERRASSE | 5 |
| WOHNZIMMER | 5 |
| ZIMMER | 5 |
| GANG | 2 |
| LIFT | 1 |
| STIEGENHAUS | 1 |

## Wohnungen

| Wohnung | Räume |
|---|---:|
| top_1 | 20 |
| top_2 | 5 |

Räume ohne `wohnung_id`: 20

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_2 | WOHNZIMMER | raum_39 | WOHNZIMMER | 99.7 % |
| raum_4 | KÜCHE | raum_40 | KÜCHE | 95.9 % |
| raum_6 | KÜCHE | raum_39 | WOHNZIMMER | 99.2 % |
| raum_19 | VORRAUM | raum_39 | WOHNZIMMER | 93.7 % |
| raum_28 | KÜCHE | raum_41 | KÜCHE | 98.3 % |
| raum_31 | VORRAUM | raum_41 | KÜCHE | 98.0 % |
| lift_1 | LIFT | raum_27 | — | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 6** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` ist leer (oder es gab keine Wandkörper-Analyse).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
