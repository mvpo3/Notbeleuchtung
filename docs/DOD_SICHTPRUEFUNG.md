# DoD-Sichtprüfung — Real-Plan Mollgasse EG

**Stand:** 2026-08-31 · **Prüfer:** Leonis (F1) · **Fall:** `Projekte/Mollgasse/Erdgeschoß.dxf`
+ reale LB `Leistungsbeschreibungen BSP/mo-leistungsbeschreibung_Elektro_240718.pdf`.

Reproduzieren: `output/dod/`-Artefakte via
`.venv/Scripts/python.exe scripts/…` bzw. `run(build_default_bundle(), dxf, "EG",
out_path=…, lb_path=…)` → `render.dxf_zu_pdf(...)`. Output-PDF/PNG bleiben gitignored.

## Ist-Ergebnis (Engine-Lauf)

- 192 Räume, **33 Symbole** (12 RZ + 21 SL), LB geparst+angewendet.
- Render: Höhenkoten (33), Stromkreis-Labels (33), LB-Legende, Stückliste, Plankopf,
  Prüfbericht — alle `drawn=True`.
- Prüfbericht-Status: **warnung**.

## Befunde / Fix-Liste

| # | Befund | Owner | Schwere | Detail |
|---|--------|-------|---------|--------|
| 1 | **`covers_segment` real leer → Fluchtweg-Deckung 103/103 „ungedeckt"** | **F1 (Leonis)** | **hoch** | Alle 12 RZ tragen `covers_segment == []` auf echten Daten; Validierungs-Regel #3 summiert nur `p.covers_segment` → meldet immer 100 % ungedeckt, obwohl RZ auf den Gängen liegen. `NotlichtPlatzierer` füllt das Feld offenbar nur im 4OG-Fixture-Pfad. Fix: reale RZ mit den gedeckten `segment_id`s verknüpfen (Naht Leonis↔Selman, `covers_segment ∈ RaumModell.segmente`). |
| 2 | **`mindest_lux_fluchtweg = 200 lx`** (Legende zeigt „Fluchtweg: min. 200 lx") | **F2 (Enis/LB)** | **hoch** | EN 1838 Fluchtweg = 1 lx (Antipanik 0,5 lx). 200 lx ist ein Fehlparse aus der LB (vermutlich Arbeits-/Raum-Lux erwischt). Legende druckt damit einen normwidrigen Wert auf den Plan. LB-Parser härten + Plausibilitäts-Cap. |
| 3 | **185/192 Räume ohne Raumtyp** (Coverage-Audit-Warnung) | F2 (Selman) | mittel | Nur 7 getypt → Leuchten-Arten evtl. unvollständig. Bekannt, siehe F2-Prompt Punkt 2. |
| 4 | **2/4 Notausgänge ohne RZ in Reichweite** (§4.1.2 g) | F1 + F2 | mittel | Entweder RZ-Platzierung an Ausgängen (F1) oder Ausgangs-Erkennung/-Koordinaten (F2). Erst prüfen, welche der 4 Ausgänge echt sind. |
| 5 | ~~**1 Symbol-Paar < 250 mm** (Kollision)~~ **erledigt** | F1 (Leonis) | niedrig | Dedup/Mindestabstand griff an einer Naht zweier Strategien nicht. **Reproduziert auf `main` f92010f nicht mehr** (mit LB: 36 Symbole, 0 Kollisionen — zwischenzeitliche Platzier-Arbeit hat es aufgelöst). Zusätzlich **strukturell abgesichert:** `platzierung/abstand_nachpass.py` entzerrt die Naht (Dubletten mergen, verschieden-artige nudgen) → Kollisionsfreiheit ist jetzt invariant statt zufällig. Neuer E2E-Regressionstest `tests/e2e/test_mollgasse_eg_durchstich.py` hält es fest. |
| 6 | **Legende/Stückliste/Plankopf/Prüfbericht im Liefer-PDF nicht sichtbar** | F1 (Leonis) | mittel | Entities sind da (`drawn=True`), erscheinen aber im Raster-PDF (`dxf_zu_pdf`, A3, bbox-tight) nicht — vermutlich außerhalb des sichtbaren Rasters platziert (Offset relativ zu `raum.bounds`, weit vom gefüllten Grundriss). Prüfen: Textblöcke in einen definierten Paperspace-/Layout-Rahmen statt frei neben den Grundriss. |
| 7 | **Höhenkoten am Plan-Maßstab sehr klein/dicht** | F1 (Leonis) | niedrig | Neu (dieser Slice). Je-Symbol-Kote `h=2,40` kann bei 33 Symbolen als Rauschen wirken. Option: nur Abweichungen zur Standardhöhe koten + eine Standard-Höhen-Notiz in der Legende. Nach Real-Feedback entscheiden. |

## Positiv verifiziert

- Grundriss (Wände) + Symbol-Blocks rendern lagerichtig entlang der Gänge.
- Montagehöhe ≥ 2000 mm, getrennter SV-Kreis, RZ-Pfeilrichtung: alle **ok**.
- LB real: `system_typ=gruppenbatterie`, **`betriebsdauer_min=480` (8 h) korrekt** —
  der Feinschliff-#1-Betriebsdauer-Bug tritt auf DIESER LB **nicht** auf (war ein
  anderer LB-/Text-Fall; F2 reproduziert mit dem betroffenen Dokument).

## Nächste F1-Schritte (aus dieser Prüfung)

1. Befund #1 (covers_segment real füllen) — höchster Hebel, macht Regel #3 aussagekräftig.
   **Erledigt** (`deckungs_zuordnung`), aber mit bewusster Grenze (siehe unten).
2. Befund #6 (Liefer-Layout der Textblöcke) — Paperspace-Layout-Template (bisher deferred).
3. Befund #5/#7 — Kleinigkeiten, gebündelt.

## Bekannte Grenzen / Follow-ups

- **Deckungs-Zuordnung ist Luftlinie, keine Sichtlinie:** `deckungs_zuordnung` misst den
  euklidischen Abstand RZ→Segment innerhalb der Erkennungsweite — **ohne** Wand-/Line-of-
  Sight-Prüfung. Ein RZ kann so ein Segment „decken", das in Reichweite, aber hinter einer
  Wand/um eine Ecke liegt → Regel #3 ist tendenziell zu optimistisch. Echter Fix braucht
  Wandgeometrie oder Kopplung an die **Weglänge im Zirkulationsgraph** (statt Luftlinie).
  Follow-up, sobald Selmans echter Graph/Wände im Contract sind.
