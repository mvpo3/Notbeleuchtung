# Übersicht — Barawitzka_FDM

DXF: `D:\KI Projekt\Notbeleuchtung\Projekte\Barawitzkagasse\415_260415_PP_VA_1_1 -2 FDM.dxf` · Geschoss: `EG` · Bild: 2400×522 px · Laufzeit 22.9 s

## Erkannte Kategorien

| Kategorie | Anzahl |
|---|---:|
| Wohnräume (ZIMMER/KÜCHE/…) | 0 |
| Sanitär (BAD/WC) | 0 |
| sonstige typisierte Räume | 0 |
| Außenflächen (BALKON/TERRASSE) | 0 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ) | 0 |
| Stiegenhäuser | 2 |
| Schächte/Lifte | 3 |
| untypisierte Räume (nicht erkannt) | 3 |
| Innenhöfe (geschlossene Außenflächen) | 1 |
| Wohnungen | 0 |
| Ausgänge final_exit | 0 |
| Ausgänge stair_exit | 0 |
| Ausgänge door | 0 |
| Fluchtweg-Segmente | 2 |
| Räume > 90 % in anderem Raum | 0 |

Räume gesamt: **8**, davon typisiert 5.

## raum_typ im Detail

| raum_typ | Anzahl |
|---|---:|
| SCHACHT | 2 |
| STIEGENHAUS | 2 |
| LIFT | 1 |

## NICHT erkannt

- **untypisierte Räume: 3** — `raum_typ` leer, `nutzungsklasse` unbestimmt. In der Karte magenta schraffiert.
- Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ): **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- Außenflächen (BALKON/TERRASSE): **0** — nicht erkannt (kein Raum mit passendem `raum_typ`).
- `final_exit`: **0** — kein Ausgang ins Freie erkannt (in Obergeschossen erwartungsgemäß, s. provider.py).
- `stair_exit`: **0** — kein Stiegenhaus-Ausgang erkannt.
- `Ausgang.typ == "door"`: **0** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt.
- Wohnungen: **0** — keine `wohnung_id` vergeben.
- Zirkulationsgraph: 0 Knoten / 0 Kanten — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, nicht aus Plan-Layern `09-WEG*`.
- Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — dafür existiert kein automatischer Erzeuger.
- „Ausgang führt auf die Straße": wird NICHT geführt — das Modell kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.
