# Übersicht — Fischamend_E_UG

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\BVH Fischamenderstraße\fertige Elektromontagepläne\UG\Elektromontageplan_Untergeschoß.dxf` · Geschoss: `EG` · Bild: 1800×1590 px · Laufzeit 40.3 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 0 |
| Sanitär (BAD/WC) | 0 |
| sonstige typisierte Räume | 6 |
| Außenflächen (BALKON/TERRASSE) | 0 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 3 |
| Stiegenhäuser | 1 |
| Schächte/Lifte | 3 |
| untypisierte Räume (nicht erkannt) | 30 |
| Innenhöfe (geschlossene Außenflächen) | 1 |
| Wohnungen | 0 |
| Ausgänge final_exit | 2 |
| Ausgänge stair_exit | 2 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 121 |
| Räume > 90 % in anderem Raum | 9 |

Räume gesamt: **43**, davon typisiert 13.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| GANG | 3 |
| GARAGE | 2 |
| KINDERWAGENRAUM | 2 |
| SCHACHT | 2 |
| TECHNIK | 2 |
| LIFT | 1 |
| STIEGENHAUS | 1 |

## Überlappungen (> 90 % der eigenen Fläche)

| Raum | Typ | liegt in | Typ | Anteil |
|---|---|---|---|---:|
| raum_1 | TECHNIK | raum_37 | TECHNIK | 99.1 % |
| raum_5 | — | raum_36 | KINDERWAGENRAUM | 99.8 % |
| raum_18 | — | raum_36 | KINDERWAGENRAUM | 95.8 % |
| raum_19 | — | raum_36 | KINDERWAGENRAUM | 93.3 % |
| raum_20 | — | raum_36 | KINDERWAGENRAUM | 98.0 % |
| raum_21 | — | raum_36 | KINDERWAGENRAUM | 97.7 % |
| raum_22 | — | raum_36 | KINDERWAGENRAUM | 98.0 % |
| raum_23 | — | raum_36 | KINDERWAGENRAUM | 99.8 % |
| lift_1 | LIFT | raum_29 | — | 100.0 % |

## NICHT erkannt

- **untypisierte Räume: 30** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Außenflächen (BALKON/TERRASSE): **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Wohnungen: **0** — keine `wohnung_id` vergeben.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
