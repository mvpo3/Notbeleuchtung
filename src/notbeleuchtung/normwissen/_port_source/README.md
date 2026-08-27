# _port_source — Roh-Norm-YAMLs aus elektro-planer (für Enis)

Rohkopie aus `elektro-planer/backend/rules/` (Enis + Selman haben KEINEN
elektro-planer-Zugriff → Leonis hat sie hierher gestaged). Herkunft:
`mvpo3/MVP-Planer`, Branch `mvp-main`, Stand 2026-08-27.

**Deine Aufgabe (Enis, Slice 1):** die relevanten Werte kuratieren + nach
`../data/` überführen (nicht 1:1 alles — nur was Notbeleuchtung braucht), dann
`En1838NormProvider` dagegen bauen. Details: `Handoff/ENIS.md`.

Kern für Notbeleuchtung: `emergency_lighting_en1838.yaml` (l=z×h, Lux, Höhe,
Dauer), `rz_coverage_oenorm.yaml`, `heights_fachpraxis.yaml` (Notlicht-Höhen),
`clearance_rules.yaml`. Stromkreis (`circuit_*`) für F13-Sicherheitskreis.
