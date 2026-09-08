---
name: plan-verify
description: >
  Notbeleuchtungsplan generieren UND das Ergebnis automatisch verifizieren
  (statt es hinterher von Hand in AutoCAD zu prüfen). Rendert einen Plan aus
  einem Architektur-DXF/DWG (+ optional LB) und fährt danach eine Prüf-Batterie:
  Eingabe-DXF-Gesundheit (Koordinaten-Versatz/Extents), PDF-Integrität (%%EOF),
  Raumerkennungs-Plausibilität, Symbol-Zahlen im erwarteten Band, Norm-Prüfstatus.
  Gibt ein GO/NO-GO mit konkreten Befunden aus.
when_to_use: >
  Bei "render + prüf", "plan verifizieren", "ist der Plan brauchbar/vollständig",
  "sind die Pläne besser", "check die DXF/PDF", "batch prüfen", "%%EOF prüfen", oder
  automatisch nach jedem `pipeline.run` / `scripts/projekt_batch_worker.py`. NICHT für
  reine Code-Änderungen ohne Render (dafür pytest/ruff).
---

# plan-verify — generieren + verifizieren in einem Schritt

## Warum
Nach jedem Render prüft der Owner das Ergebnis heute manuell: PDF öffnen ("ist der
vollständig?"), Symbole gegenzählen, und bei fremden Eingabe-Plänen erst mal raten,
ob die DXF überhaupt brauchbar ist. Diese Skill übernimmt genau diese Nachkontrolle
deterministisch — der Owner bekommt statt "hier ist die Datei" ein **GO/NO-GO mit
konkreten Befunden**.

## Wann triggern (Beispiele)
- "Render mal <Projekt>/<Geschoss>" → rendern **und** verifizieren, nicht nur rendern.
- "Sind die (Baufeld-)Pläne jetzt besser?" → Eingabe-DXF-Gesundheit je Geschoss.
- "Ist der Plan vollständig / brauchbar?" → Output-Verifikation.
- "Prüf die PDF / %%EOF" → Integritäts-Check vor Versand.
- "Batch über 1OG 2OG 3OG …" → je Geschoss rendern + verifizieren + Bilanz.
- Automatisch nach jedem `pipeline.run(...)` / `scripts/projekt_batch_worker.py`.
- NICHT triggern für reine Code-Änderungen ohne Render (dafür `pytest`/`ruff`).

## Ablauf

### Schritt 0 — Eingabe-Gesundheit (VOR dem teuren Render)
Fängt korrupte Quell-DXF ab, bevor 2+ Minuten Parse/OOM verbrannt werden
(4OG-Lektion 2026-09-08: 61 % der Entities bei y≈347.535 km → 2,5-TiB-Raster).
- `python scripts/dxf_healthcheck.py "<pfad.dxf>"` (siehe „Tools").
- Prüft: Anteil Entities mit |x|/|y| > 1000 km, Cluster-Verteilung, Bbox-Spanne.
- **NO-GO wenn** Ausreißer > 0 oder Bbox-Spanne > ~2 km → melde Layer/Cluster,
  render NICHT, empfiehl AutoCAD-MOVE/PURGE bzw. Selman-Extents-Clustering.

### Schritt 1 — Generieren
- Einzeln: `pipeline.run(build_default_bundle(), "<dxf>", "<floor>", out_path=…)` bzw.
  API `POST /plan`. Batch: `scripts/projekt_batch_worker.py <FLOOR...>` (sequenziell —
  parallel = MemoryError; Langläufer im Owner-Terminal via `!`, nicht als gekillter
  Hintergrund-Task).
- Merke die Rückgabe: `render_summary`, `pruefung`, Platzierungs-Liste.

### Schritt 2 — Verifikation (die eigentliche Skill-Leistung)
Alles automatisch, keine manuelle Sicht nötig:
1. **PDF-Integrität:** letzte Bytes enthalten `%%EOF` (Abbruch-Leiche = NO-GO;
    2026-09-06-Lektion: kaputtes PDF ging an den Owner raus).
2. **DXF liest zurück:** `ezdxf.readfile(out.dxf)` ohne Fehler; TEXT/INSERT-Zahlen > 0.
3. **Raumerkennung plausibel:** `raeume ≥ 1`, `ausgaenge ≥ 1`, nicht „quasi-leer"
    (Symbole ≥ Schwelle); Türen ≫ Räume ODER 0 Ausgänge → Erkennung fragwürdig
    (Regeln 8b/8c) → WARNUNG.
4. **Symbol-Zahlen im Band:** RZ/SL gegen das erwartete Band der CAD-Familie
    (Referenz `plan_verify_baender.yaml`, s. Tools) — außerhalb = WARNUNG mit Delta.
5. **Norm-Prüfstatus:** `render_summary["pruefung"]["status"]` (ok/warnung/fehler)
    + offene Regeln zitieren; `fehler` = NO-GO.
6. **Vermerk am Blatt:** Prüfvermerk/OIB-Stufe sichtbar (nicht abgeschnitten;
    Breiten-Budget) — reuse der L1/L3-Messmethode (`_vermerk_messer`).

### Schritt 3 — Report (statt "hier ist die Datei")
```
PLAN-VERIFY <projekt>/<floor>
  Eingabe:    ok (Spanne 78 m, 0 Ausreißer)
  Render:     13,6 MB DXF · 244 s
  PDF:        ok (%%EOF) · 4,2 MB
  Räume:      266 · Ausgänge 4 · Türen 120
  Symbole:    17 RZ / 31 SL   (Band 10–30 / 15–44 → im Band)
  Prüfstatus: warnung — Regel 15 (Photometrie-Ausrichtung offen)
  VERDIKT:    GO mit Hinweis   |   NO-GO: <konkreter Befund>
```
Regel: **niemals still abschneiden** — jede gedeckelte/übersprungene Prüfung wird
im Report benannt (sonst liest sich "geprüft" als "alles ok").

## Tools, die die Skill besser machen
Priorisiert; ① ist der größte Hebel (heute 3× ad-hoc nachgebaut).

1. **`scripts/dxf_healthcheck.py` (GEBAUT — 2026-09-08)** — Eingabe-DXF-Gesundheit:
   Ausreißer-Anteil (|x|/|y|>1e9 mm), y-Cluster-Histogramm, Bbox-Spanne, Top-Layer
   je Cluster; Exit≠0 + GO/NO-GO-Report bei Korruption. Kapselt genau die 4OG-Diagnose.
   Rein `ezdxf`, keine Engine-Importe. Aufruf:
   `python scripts/dxf_healthcheck.py "<plan.dxf>" [...]` · Funktion `pruefe(pfad) -> Befund`
   für Schritt 0 der Skill. Tests: `tests/hauptengine/test_dxf_healthcheck.py`.
2. **`plan_verify_baender.yaml` (NEU)** — erwartete RZ/SL-Bänder je CAD-Familie/Geschoss
   (Mollgasse, Baufeld, Wohnbau …), damit "Symbol im Band" nicht hartkodiert ist.
   Quelle sind die schon existierenden E2E-Bänder (`tests/e2e/…`).
3. **`scripts/plan_pruefen.py` (EXISTIERT)** — erzeugt Prüfbericht + PNG-Overlays
   (05_fluchtweg/06_platzierung). Die Skill ruft es für die visuelle Beilage.
4. **PDF→PNG-Thumbnail (pypdfium2, im `analyse`-Extra)** — ein Vorschaubild je Plan,
   damit der Owner ohne AutoCAD drüberschauen kann (SendUserFile).
5. **`ezdxf` (EXISTIERT)** — Read-back, TEXT/INSERT-Zählung, `_vermerk_messer`-Breiten.
6. **`hauptengine.validierung` / `pruefbericht` (EXISTIERT)** — liefert `status` +
   Regel-Befunde; die Skill zitiert nur, rechnet nicht selbst nach (Owner-Grenze).
7. **Optional MCP `claude_ai_Autodesk_Product_Help`** — Norm-/AutoCAD-Nachschlag,
   wenn ein Befund eine Vorschriften-Referenz braucht (statt aus dem Gedächtnis).

## Grenzen
- Verifiziert Ausgabe-Integrität + Plausibilität + Band-Konformität — **ersetzt keine
  fachliche Abnahme** (Norm-Korrektheit bleibt Prüfbericht/Enis-Lane).
- Kein Push/Merge/Versand ohne Owner-GO (irreversibel).
- Bänder sind Toleranzen, keine Goldens: kippt ein Band, ist das ein Signal
  („bewusste Änderung? dann Band + Begründung nachziehen"), kein stiller Fix.
