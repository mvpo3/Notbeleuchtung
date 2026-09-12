# BT1-EG (Fischamenderstrasse) — Raumerkennung auf RaumModell 1.5.0

**NEUE MESSUNG vom 2026-09-12.** Das ist KEINE Rekonstruktion eines
frueheren Laufs: vor diesem Lauf lag fuer BT1-EG kein Ergebnis auf 1.5.0
vor (der Plan ist nicht in der Pruefstrecke).

**Ausschliesslich Raumerkennung** — keine Platzierung, keine Pipeline.
Deshalb NICHT `scripts/plan_pruefen.py`, sondern der Provider direkt.

| Angabe | Wert |
|---|---|
| Eingabe | `Projekte\BVH Fischamenderstraße\fertige Elektromontagepläne\BT1\Elektromontageapläne_ERDGESCHOSS BT1.dxf` |
| SHA-256 der Eingabe | `d1fc3b0b762609d1c445a29c6229c6b0f403eb7cd3d3d7ec83e44a3eba848107` |
| Groesse | 31523707 Bytes |
| Commit-SHA | `91ad7ccfa0a1638490c9605f929f8d8b145b016a` |
| Exakter Aufruf | `ArchitekturRaumProvider().parse('Projekte\\BVH Fischamenderstraße\\fertige Elektromontagepläne\\BT1\\Elektromontageapläne_ERDGESCHOSS BT1.dxf', 'EG')` |
| Laufzeit | 19.5 s |
| Ablage RaumModell | `Projekte/_ergebnis_bt1_eg/raummodell.json` |
| contract_version im Modell | `1.5.0` |

## Kennzahlen

| Kennzahl | Wert |
|---|--:|
| Raeume | 72 |
| Tueren | 225 |
| davon typisiert | 192 |
| Fluchtweg-Segmente | 87 |
| Wandkoerper | 0 |

Ausgaenge: `{"stair_exit": 1, "final_exit": 3}`

Raumtypen: `{"ZIMMER": 14, "GANG": 8, "(ohne)": 5, "TERRASSE": 5, "BALKON": 2, "BAD": 6, "WC": 6, "KÜCHE": 12, "VORRAUM": 6, "ABSTELLRAUM": 4, "GARAGE": 1, "STIEGENHAUS": 1, "KINDERWAGENRAUM": 1, "LIFT": 1}`
