# CHANGELOG Platzierungslogik — Regelwerk-Einbau (Auftrag „Wissensaufbau", 2026-09-29)

Alle Änderungen des Schritt-5-Einbaus, je Eintrag: Datei, Funktion, rule_id.
Grundsatz: KEINE Verhaltensänderung bestehender Platzierungen (GT-Freezes,
Golden-Fixtures, Naht-Invarianten unangetastet); der Einbau ist Regeln-als-
Daten + Audit-Mapping + Tests. Verhaltensändernde Folge-Slices sind unten
gelistet und brauchen Owner-GO.

## Neu

| Datei | Funktion/Inhalt | rule_id |
|---|---|---|
| `src/notbeleuchtung/platzierung/regelwerk.py` | Loader (`alle()`, `regel()`, `basis_regeln()`, `quelle()` = `"Referenz-Praxis: RW-### — <thema>"`-Audit-String), `UMSETZUNG`-Mapping (23 Regeln → Code-Stellen), `NICHT_UMSETZBAR` (12 Regeln mit dokumentiertem Grund) | RW-001…RW-035 |
| `src/notbeleuchtung/platzierung/data/notbeleuchtung_regeln.json` | 66 Regeln (35 basis + 31 ergaenzung), generiert aus `knowledge/…/_Analyse_Regelwerk/REGELWERK_Notbeleuchtung.json` via `baue_regelwerk.py` (Build-Weg dokumentiert im Modul-Docstring) | alle |
| `tests/platzierung/test_regelwerk.py` | Loader-Tests: IDs eindeutig, frozen, nb_ref-Migration, **jede basis-Regel hat UMSETZUNG ODER NICHT_UMSETZBAR-Begründung**, quelle()-Präfix, Engine-JSON ⊆ knowledge-JSON | alle basis |
| `tests/platzierung/test_regelwerk_belege.py` | je Basis-Regel 1 parametrisierter Test: mindestens ein Beleg-Handle existiert real in der Quell-DXF (Asset-Skip-Konvention) | RW-001…RW-035 |
| `docs/ENGINE_IST.md` | Ist-Aufnahme vor dem Einbau (Regel→Code-Landkarte, Lücken, Kalibrier-Delta) | — |

## Geändert

| Datei | Änderung | rule_id |
|---|---|---|
| `.gitignore` | `_Analyse_Regelwerk/seiten/` (538 Seiten-PNG-Cache) lokal gehalten | — |
| `scripts/analyse/mollgasse_gt_vergleich.py` | (P6) Typ-/Rotations-Match je Paar + „erreichbar"-Messmodus — s. ENGINE_VALIDIERUNG.md | RW-006/007/016 |

## Bewusst NICHT geändert (Folge-Slices, Owner-GO nötig)

| Kandidat | Grund | rule_id |
|---|---|---|
| AP-Längsachsen-Rotation in `flaechen_strategy` | verändert rotation_deg bestehender Antipanik-Platzierungen → Golden-Shift | RW-028 |
| OG-I-Gang-Sichtketten-Ausnahme | verändert Mollgasse-OG-Bänder (GT-Freeze) | RW-033 |
| Knick-RZ im Stiegenlauf | braucht Lauf-Knick-Geometrie (Treppenlauf liefert nur Antritt/Austritt — Selman-Naht) | RW-101 |
| STGH-Vorbereich-Aufheller | Ergänzungsregel (Hausfeld); Trigger würde auch Mollgasse-UG treffen → Band-Shift | RW-102 |
| Schräg-Wand-Rotation (keine 90°-Quantisierung) | `rotation_zur_tuer` quantisiert bewusst; Schräg-Fall braucht Tür-Achsen-Winkel aus Erkennung | RW-113 |
| Schul-Muster (Klassenraum = Tür-RZ + Aufheller) | braucht Raumtyp KLASSENRAUM (Selman) | RW-104 |

## Suite-Stand nach Einbau

`pytest tests/platzierung tests/contract tests/naht`: **453 passed / 34 skipped /
3 xfailed** (identisch zur Vorher-Basis + 40 neue Regelwerk-Tests) · `ruff check
src tests scripts` + `_Analyse_Regelwerk/scripts`: clean · kein Contract-Touch.
