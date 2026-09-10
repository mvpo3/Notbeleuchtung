# Übersicht — Fischamend_BT1_UG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\BVH Fischamenderstraße\BT1\260320_938-AR-PP-11990-A_UNTERGESCHOSS BT1.dxf` · Geschoss: `EG` · Bild: 1800×1370 px · Laufzeit 28.1 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 0 |
| Sanitär (BAD/WC) | 0 |
| sonstige typisierte Räume | 15 |
| Außenflächen (BALKON/TERRASSE) | 0 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 3 |
| Stiegenhäuser | 1 |
| Schächte/Lifte | 4 |
| untypisierte Räume (nicht erkannt) | 21 |
| Innenhöfe (geschlossene Außenflächen) | 2 |
| Wohnungen | 0 |
| Ausgänge final_exit | 3 |
| Ausgänge stair_exit | 2 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 114 |
| Räume > 90 % in anderem Raum | 3 |

Räume gesamt: **44**, davon typisiert 23.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| TECHNIK | 12 |
| GANG | 3 |
| SCHACHT | 3 |
| GARAGE | 2 |
| KINDERWAGENRAUM | 1 |
| LIFT | 1 |
| STIEGENHAUS | 1 |

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_29 | TECHNIK | raum_34 | TECHNIK | 100.0 % |
| lift_1 | LIFT | raum_29 | TECHNIK | 100.0 % |
| lift_1 | LIFT | raum_34 | TECHNIK | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 21** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Außenflächen (BALKON/TERRASSE): **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Wohnungen: **0** — keine `wohnung_id` vergeben.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
