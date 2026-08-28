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

## Slice 2 (Platzierung — Leonis)
| Neu | Herkunft (elektro-planer) | Commit | Divergenz |
|-----|---------------------------|--------|-----------|
| `platzierung/geometry.py` | `backend/engine/placement_geometry.py` | 3976fa6 | kuratiert: nur render-freie Primitive für Notbeleuchtung (Möbel-/Bad-Grid-/scale-Primitive weggelassen); `find_center_visual` ohne blind-except umgebaut (ruff) |
| `platzierung/communal_stgh_strategy.py` | `backend/diagnostics/inject_communal_stgh.py` | 85511b0 | **Render entkoppelt** (kein ezdxf/insert_symbol/render_pdf) — erzeugt Contract-B `Platzierung` statt zu zeichnen; **generativ statt faithful**: 1 RZ je Fluchtweg-Segment am Ausgangs-Endpunkt, Orientierung/Bauteil (AGV-A/B-F13) aus der Segment-Geometrie; GT-Sub-Grad-Rotationen bewusst nicht reproduziert |
| `symbols/schrack_symbol_mapping.yaml` | `backend/symbols/schrack_symbol_mapping.yaml` | 5dad907 | kuratierte Notlicht-Teilmenge (nicht 109 Blöcke); **`notlicht_ks_stiege_unten` neu** (im Original über GT-Subtype auf `notlicht_ks_stiege` gemappt) |

## Geplante Ports (noch offen)
| Ziel | Herkunft | Slice | Kopplung |
|------|----------|-------|----------|
| `normwissen/data/*.yaml` | `backend/rules/{emergency_lighting_en1838,rz_coverage_oenorm,clearance_rules,heights_fachpraxis,circuit_rules_ove_8015,circuit_label_policy}.yaml` | 1 | reine Daten (1/5) |
| `hauptengine/render/*` + Insert-Infra | `backend/engine/{dxf_writer,dxf_layers,layout_template}.py`, `backend/symbols/{schrack_inserter,schrack_library}.py` | 3 | `config.py`-Refactor (Pfade optional); ergänzt das in Slice 2 gestartete `symbols/` |
| `assets/E-Symbole.dxf` | `elektro-planer/CAD_Symbole/E-Symbole.dxf` | 3 | Binär, Version hier pinnen |
| `raumerkennung/_port/*` (~38 Module) | `backend/parsers/*`, `backend/engine/walls/*`, `backend/models/{room,component,project}.py` | 4 | größter Port; keller_geometry↔architecture_dxf Zirkular-Import trennen |
