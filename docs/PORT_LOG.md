# PORT_LOG — Herkunft der aus `elektro-planer` portierten Module

Quelle: `github.com/mvpo3/MVP-Planer` (lokal `../elektro-planer`), Branch `mvp-main`.
elektro-planer ist für Notbeleuchtung **eingefroren** — keine Rück-Synchronisation.
Jede Zeile pinnt den Herkunfts-Commit + dokumentiert Divergenzen.

## Keimzelle (Contracts)
| Neu | Herkunft (elektro-planer) | Commit | Divergenz |
|-----|---------------------------|--------|-----------|
| `contracts/raum_modell.py` | `backend/engine/notlicht/contracts/fluchtweg_graph.schema.json` | 8281f5f (Slice 2.50.0) | JSON-Schema → Pydantic; um Vollräume/Türen/Ausgänge erweitert |
| `contracts/platzierung_ergebnis.py` | `.../notlicht_placement.schema.json` | 8281f5f | JSON-Schema → Pydantic; `richtung`/`norm_quelle` ergänzt |
| `contracts/norm_regelwerk.py` | — (NEU) | — | im Scaffold nicht vorhanden; hier als Query-API-Contract erstmals |
| Fixtures 4OG | `.../fixtures/*.json` (5 echte SV_RETTUNGSZEICHEN) | 8281f5f | an neue Contracts angepasst |

## Geplante Ports (noch offen)
| Ziel | Herkunft | Slice | Kopplung |
|------|----------|-------|----------|
| `normwissen/data/*.yaml` | `backend/rules/{emergency_lighting_en1838,rz_coverage_oenorm,clearance_rules,heights_fachpraxis,circuit_rules_ove_8015,circuit_label_policy}.yaml` | 1 | reine Daten (1/5) |
| `platzierung/communal_stgh_strategy.py` | `backend/diagnostics/inject_communal_stgh.py` | 2 | Import-Grenze hart: nur contracts+geometry+symbols, KEIN Render |
| `platzierung/geometry.py` | `backend/engine/placement_geometry.py` | 2 | — |
| `hauptengine/render/*` + `symbols/*` | `backend/engine/{dxf_writer,dxf_layers,layout_template}.py`, `backend/symbols/*` | 3 | `config.py`-Refactor (Pfade optional) |
| `assets/E-Symbole.dxf` | `elektro-planer/CAD_Symbole/E-Symbole.dxf` | 3 | Binär, Version hier pinnen |
| `raumerkennung/_port/*` (~38 Module) | `backend/parsers/*`, `backend/engine/walls/*`, `backend/models/{room,component,project}.py` | 4 | größter Port; keller_geometry↔architecture_dxf Zirkular-Import trennen |
