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

## 2026-10-02 — Codex-Review-Workflow festgelegt (Doku-only)

Verbindlicher, projektweiter Prozess „Claude implementiert → Codex prüft → Claude
verifiziert → Claude fixt" in `CLAUDE.md` (Sektion **Codex-Review-Workflow (BINDEND)**).
Kein Produktiv-/Verhaltens-Code, kein Contract-Touch. Aufrufroute = Shell
`codex review` (`--uncommitted` / `--commit <sha>` / `--base <branch>`), Modell pro
Aufruf `-c model="gpt-5.5"` (config.toml unberührt, ChatGPT-Auth → keine API-Kosten;
Fallback `codex-auto-review`). Codex ist beratend; die Regelquellen (CLAUDE.md, docs,
Norm-YAML/regelwerk, Contracts) schlagen Codex. Verlauf = diese Datei.

## 2026-10-02 — M3 Frontalsicht: Pfeiltyp nach Ankunfts-Frontalsicht (verhaltensändernd)

RW-006/007 (Mollgasse-PDF): das Rettungszeichen-Symbol (links/rechts/down) wird nach
der **Frontalsicht der ankommenden Person** gewählt, nicht mehr rein aus dem
quantisierten Fluchtvektor.

| Datei | Funktion/Inhalt | rule_id |
|---|---|---|
| `platzierung/bausteine.py` | **Neu** `frontalsicht_block(in_vec, out_vec, keys) → (key, rot, mirror, richtung)`: gerade Fortsetzung (Ankunft ≤45°) → down-Typ, Pfeil ENTGEGEN der Person (`rotation_piktogramm_in_raum`); echter Abzweig (>45°) → gerichteter Block. `ist_abzweig`/`ABZWEIG_COS` von `gang_strategy` hierher geteilt (EINE Quelle). | RW-006/007 |
| `platzierung/gang_strategy.py` | Inline-Regel (NB-R06/R07) auf `frontalsicht_block` umgestellt — **byte-identisch** (Referenz, Gang-Band unverändert). | RW-006/007 |
| `platzierung/stgh_strategy.py` | Podest-RZ auf `frontalsicht_block((0,0), flucht)` = **down-Frontal** (die Person läuft gerade auf die Stiege; kein seitlicher Anlauf). Ersetzt die laufrichtungs-quantisierte Richtungswahl, die den Owner-Plan nicht traf. | RW-006/007 |
| `tests/platzierung/test_frontalsicht.py` | **Neu** Baustein-Tests (5 Frontalsicht-Szenarien). | RW-006/007 |
| `tests/platzierung/test_stgh_strategy.py` | 2 Tests auf M3-Soll nachgezogen (Richtungs-RZ→down; UG↔OG-Unterscheidung lebt jetzt in der **Rotation**, nicht im Block-Typ). | RW-006/007 |
| `tests/platzierung/test_gang_strategy.py` | `_ist_abzweig`-Import auf `bausteine` umgezogen (geteilte Quelle). | — |

**Messung (`scripts/analyse/mollgasse_gt_vergleich.py`, alle 8 Geschosse):** Typ-Match
**14→19 / 33** (+5: 413A0/952E8/852E3/852B0/1C8CC/1CD8C von „directional" auf das
Owner-Soll „unten" geflippt). Gepaart 31→30 (−1, 1OG: zwei deckungsgleiche „unten"-RZ
546 mm auseinander → `sichtkette` dünnt eins aus; Stelle bleibt gedeckt). `communal`
(Soll=directional, eng=down — anderes Problem) und `anker` (0 der Mollgasse-Paar-Misses)
bewusst unberührt. Rest-Misses 41220/41593/1BCBB (Soll=directional) folgen der
Gebäude-Ausgangsachse, nicht der Stiegen-Laufrichtung → eigener Dijkstra-Hebel, hier
nicht geraten.

**Suite:** `pytest tests/platzierung tests/render tests/contract` 506 passed · `tests/naht
tests/e2e` 366 passed / **5 failed = Baseline** (s7_wohnungsklasse + soll_muthgasse,
Selman-Naht, 0 neu) / 13 xfailed · `ruff` clean · kein Contract-Touch. Visual-Golden
(`-m visual`) unverändert (4OG-Fake-Modell hat keine Stiegenhäuser → kein Render-Diff).
**Hausfeld-2DG-Wächter: nicht automatisiert lauffähig** (kein leerer Architektur-Input
im Repo) → Owner-Sicht-Check empfohlen; betroffen nur Stiegen-Podest-RZ-Typ, Gang/Tür/
Ausgang unberührt. **Codex-Review ausstehend** (Quota bis 2026-10-03 ~19:10).
