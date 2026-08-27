# _port — Roh-Parser aus elektro-planer (für Selman)

Rohkopie aus `elektro-planer/backend/` (Selman hat KEINEN elektro-planer-Zugriff
→ Leonis hat sie hierher gestaged). Herkunft: `mvpo3/MVP-Planer`, Branch
`mvp-main`, Stand 2026-08-27. ~14.4k LOC.

- `parsers/`      — Architektur-Parser (`architecture_dxf.py`, `keller_geometry.py`,
                    `door_*`, `scale_detector`, `layer_profiles`, `unit_faces`,
                    `apartment_*`, `room_*`, `building_units`, …).
- `engine_walls/` — Wandgeometrie (`door_opening.py` etc., war `engine/walls/`).
- `models/`       — `room.py`, `component.py`, `project.py`.

## WICHTIG — das ist ROH, läuft noch nicht

Die Module tragen ihre **alten Imports** (`from parsers.x import …`,
`from engine.walls.y import …`) — die lösen in der neuen Paket-Struktur NICHT auf.
Genau das ist deine Slice-4-Aufgabe (siehe `Handoff/SELMAN.md`):

1. Imports auf die neue Struktur umbiegen (`engine.walls` → `._port.engine_walls`).
2. `config.py`-Kopplung brechen: harte Mollgasse-Pfade (`CANONICAL_BLANK_DIR`,
   Referenz-DXF) optional/`.env`; nur `RULES_DIR`/`resolve_rule_path` behalten.
3. Zirkular-Import `keller_geometry` ↔ `architecture_dxf` sauber trennen.
4. `ArchitekturRaumProvider.parse(dxf, floor)` bauen, der ein `RaumModell`
   (Contract) liefert — schema-gleich zu `tests/fixtures/raum_modell_4og.json`.

Test-Pläne: `Projekte/`. Ziel-Contract: `docs/CONTRACTS.md`.
