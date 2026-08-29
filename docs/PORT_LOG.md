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

## Slice 3 (Render — Leonis/Hauptengine)
| Neu | Herkunft (elektro-planer) | Commit | Divergenz |
|-----|---------------------------|--------|-----------|
| `symbols/library.py` | `backend/symbols/schrack_library.py` | 922d66c | Pfad-Resolution statt `config.py` (Arg → env `NOTBELEUCHTUNG_SYMBOL_LIB` → Aufwärts-Suche `CAD_Symbole/E-Symbole.dxf`); Mapping-Load delegiert an das Slice-2-`__init__` (ezdxf-frei für platzierung/) |
| `symbols/inserter.py` | `backend/symbols/schrack_inserter.py` | e0c01d6 | **generativ statt faithful** (273→~70 Z.): keine Catalog-Aliases, keine Notlicht-Variant-Heuristik (Leonis emittiert finale Keys), keine Verteiler-Farben, kein Marker-Fallback; Contract-B-Objekt direkt; effektive Spiegelung = Mapping-`mirror_x` XOR Contract-`mirror_x`; XDATA-appid `NOTBELEUCHTUNG`; behalten: `DE_GLOBAL_SCALE=185`, scale/scale_abs |
| `hauptengine/render/dxf_renderer.py` | `backend/engine/dxf_writer.py` (Subset) | ab53d8a | Contract-Objekte statt Placement-/Arch-JSON; Raum-Konturen aus `RaumModell.polygon_mm` + Fluchtweg-Segmente statt Wände; Stromkreis-Label-Port (Normale + Anti-Kollision, Konstanten verbatim) ohne Kürzel-Stapel; VPORT-Block vereinfacht; **kein Port:** `dxf_layers.py`/`layer_convention` (fixe Layer `E_Sicherheitsbeleuchtung`/`E_Stromkreis_Label`/`ARCH_*` statt kind→layer-Maschine für 1 Symbolfamilie), Höhenkoten, Media-Labels, Overlap-Spirale, Hatch-Stripping |
| `CAD_Symbole/E-Symbole.dxf` | `elektro-planer/CAD_Symbole/E-Symbole.dxf` | 6d5e865 | binär-identisch (schon vor Slice 3 gestaged) |

## Katalog-Erweiterung (Symbole — Leonis)
| Neu | Herkunft | Divergenz |
|-----|----------|-----------|
| `schrack_symbol_mapping.yaml` +2 Keys | **zweckgebaute Blocks** in `CAD_Symbole/E-Symbole.dxf` (Owner-gezeichnet) | **Sicherheitsleuchte** (`sicherheitsleuchte_aufheller` → „Sicherheitsleuchte Aufheller", CIRCLE+HATCH, 4.7×4.7 units) + **Antipanik** (`antipanik_leuchte` → „Notbeleuchtung- Antipanikleuchte", 44 LWPOLYLINE, 5.64×1.59). Kurations-Befund: „richtungspfeil nach rechts" korrupt (Extents 2606×2300 → „rechts" via mirror auf „nach links"); „SV_RETTUNGSZEICHEN" ist Legenden-Block (861×4945, 30 ATTDEF), nicht platzierbar. In-Band-Guard-Test (`< 50 units`) in `tests/render/test_symbols_library.py`. **Noch kein Platzierer emittiert die 2 Keys** — braucht Enis-Norm-`symbol_katalog_keys` + `plan_sicherheitsleuchten`/`plan_antipanik`-Strategie. |

## Geplante Ports (noch offen)
| Ziel | Herkunft | Slice | Kopplung |
|------|----------|-------|----------|
| `normwissen/data/*.yaml` | `backend/rules/{emergency_lighting_en1838,rz_coverage_oenorm,clearance_rules,heights_fachpraxis,circuit_rules_ove_8015,circuit_label_policy}.yaml` | 1 | reine Daten (1/5) |
| Layout-Template (Paperspace/Titelblock/PDF) | `backend/engine/layout_template.py` + `Vorlagen/{Vorlage_mit_Logo,rivoplan_logo_vector}.dxf` | 5+ | 681 Z. + Vorlagen-Assets; DoD Slice 3 braucht kein Titelblatt — deferred |
| `raumerkennung/_port/*` (~38 Module) | `backend/parsers/*`, `backend/engine/walls/*`, `backend/models/{room,component,project}.py` | 4 | größter Port; keller_geometry↔architecture_dxf Zirkular-Import trennen |
