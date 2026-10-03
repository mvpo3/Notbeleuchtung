# Einbau-Fahrplan Platzierungslogik (2026-10-03)

Wie das aufgebaute Regelwerk-Wissen in die Hauptengine kommt. Priorisiert nach
**GT-Hebel × Lane-Freiheit × Regressionsrisiko**. Quellen: Review
`docs/REVIEW_Plaene_zeichnen_Wissen_2026-10-03.md`, Mollgasse-Analyse
(`_Analyse/GEGENPRUEFUNG_ENGINE.md`, `REVIEW.md`), Klassifikation in
`platzierung/regelwerk.py` (UMSETZUNG/NICHT_UMSETZBAR).

## Ausgangslage

- **26 von 66 Regeln live** (23 Basis + 3 Ergänzung) — handcodiert in den
  Strategien (`gang_/stgh_/anker_/communal_stgh_/flaechen_/aussen_strategy`,
  `deckung`, `fachpraxis`, `bausteine`, `sichtkette`). 40 offen.
- **Das Regelwerk als Daten steuert die Engine NICHT** — kein `src/`-Modul
  importiert `regelwerk`; `quelle()` ist ungenutzt. Es ist Spec/Audit, kein
  Ausführungscode.
- **„Gebaut" ≠ „reproduziert"**: Mollgasse-GT 33/97 gepaart (34 %), 13 Typ-Match.
  Laut `GEGENPRUEFUNG`: von den Paar-Misses sind **~31 = Zündkette reißt
  (Raumtyp/Tür/Zirkulation → Selman)**, nur **~5 = Pfeiltyp (M3 → Leonis)**.
  **Kernaussage: der größte Rest-Hebel liegt bei Selman (Erkennung), nicht bei
  der Platzierung.**

## Architektur-Entscheidung (Empfehlung)

**Strategien bleiben die Ausführungsschicht; das Regelwerk bleibt Spec/Audit —
KEIN Umbau auf eine daten-getriebene Regel-Engine.** Begründung: die Regeln sind
geometrisch/kontextuell (Frontalsicht, Diagonalen-Mitte, Sichtketten), nicht als
JSON-Prädikate ausdrückbar; ein Rewrite würde alle GT-/Golden-Freezes riskieren
für Null Verhaltensgewinn. Die „Wissen-nicht-verdrahtet"-Lücke schließt man
billig durch **Audit-Kopplung** statt Rewrite:

- **S-AUDIT (optional, klein):** jede praxisbegründete Platzierung trägt ihre
  `regelwerk.quelle("RW-xxx")` im `norm_quelle`-Präfix. ⚠️ Naht-Invariante
  `norm_quelle ∈ NormRegelwerk.quellen` (Leonis↔Enis, `tests/contract/`) — vorher
  mit Enis klären, ob „Referenz-Praxis: RW-xxx" als zulässige Quelle gilt, sonst
  bricht das Gate. Nutzen: Audit-Trail Platzierung→Regel ohne Verhaltens-Change.

## Blocker — Owner-Entscheidungen (Stand 2026-10-03)

| B | Frage | Owner-Antwort 2026-10-03 | Folge |
|---|---|---|---|
| B1 | Aufheller 500 mm je RZ drosseln? | **500 mm = MINDESTabstand; darüber unschädlich/nicht falsch → NICHT drosseln** | S-B nicht mehr „Überschuss-Drossel"; die 115 Überschüsse sind großteils RZ-only-DXF-Artefakt (M1-Phantom), kein Fehler |
| B2 | Tür-RZ-Versatz 0 mm (Wandlinie) oder 735–930 mm raumseitig? | **offen** — Herkunft erläutert: gemessener raumseitiger Versatz im Mollgasse-Erklär-DXF (`REGELWERK_Mollgasse.md:14`, RW-001; RW-003 375–840, UG 711–779). Steht gegen Ansage 18.09. „Wandlinie, 0 mm" | RW-001-Feinschliff wartet weiter auf Entscheid |
| B3 | beidseitig: 2 Einzel-RZ oder 1 Block? | **1 Block** (`RIVO_ARR_bothsided` in `CAD_Symbole/RIVO_NL_Symbole.dxf`) | ✅ Engine schon korrekt (`dxf_renderer.py:1183/1205`) — KEIN Umbau; GT-„2 Einzel" = nur Mess-Nuance |
| B4 | S-AUDIT (regelwerk.quelle → norm_quelle) bauen? | **ja** | ⚠️ Naht: `test_naht_norm_quelle_in_regelwerk` erzwingt norm_quelle ∈ `NormRegelwerk.quellen` → Enis muss „Referenz-Praxis: RW-xxx" registrieren (Präzedenz `fachpraxis.py:91`). **Leonis+Enis-Naht, nicht solo** |

## Phase 1 — Leonis-pur, Selman-unabhängig (sofort baubar)

| Slice | Regel | Was | GT-Hebel | Risiko |
|---|---|---|---|---|
| **S-A** | RW-029 | Antipanik-Position auf **Diagonalen-Mitte-Rezept** (Mauerkante→Gangecke, Mitte Δ23–33 mm) statt `find_center_visual`-Näherung | Typ/Position Antipanik | Golden/GT-Band (AP-Positionen shiften) → Messlauf |
| **S-B** | RW-111 | Gang-Aufheller bedient mehrere Türvorbereiche (SL-Analogie NB-R08); EIN Aufheller für Türcluster (PDF 3OG „eine Leuchte bedient vier Türen") | Platzierungs-Treue (nicht Drossel — B1: 500 mm ist Mindestmaß) | GT-Band |
| **S-C** | RW-005 | Stiegen-RZ-Positionsband 800–1122 mm vor Antritt/Austritt, auf Laufachse schärfen | senkt 1–2 m Paarungsdistanzen | Golden stgh |
| **S-D** | #5 (validierung) | **Exit-RZ-Fallback**: RZ am `final_exit` auch wenn außerhalb Raumpolygon | schließt EG/1KG-WARNUNG (Diagnose 2026-10-03) | GT-Doppelzählung an schon gedeckten Ausgängen → eigener Messlauf; **Wurzel ist Selman (s. Phase 3)** |

## Phase 2 — Leonis-Logik, aber Selman-gated

Baubar als Platzierung, aber brauchen Erkennungs-/Zirkulations-Input, der heute
fehlt. Erst nach Selman-Paket (Phase 3) sinnvoll.

| Slice | Regel | Was | Abhängigkeit |
|---|---|---|---|
| **S-E** | M3-Teil-2 | Exit-Gradient: directional-Misses 41220/41593/1BCBB nach **Gebäude-Ausgangsachse** (Dijkstra) | `zirkulation.nodes/edges` auf Mollgasse LEER → Selman-Knotengraph nötig (Ansatz 02.10. darum verworfen) |
| **S-F** | RW-101 | Knick-RZ am Zwischenpodest im Stiegenlauf | Zwischenpodest/Lauf-Knick aus Selman |
| **S-G** | RW-102 | Aufheller am STGH-Vorbereich-Knoten (Schleuse/Lift/Stiegenfuß) | Knoten-Erkennung (Selman) |
| **S-H** | RW-110 | Mehrstufige Tür-Folgen (Raum→Raum→Gang), je Tür eigenes RZ | Türketten-Zirkulation (Selman) |
| **S-I** | RW-105/106 | Beidseitig-Reihe / Knoten-Kombi für seitliche Quer-Ankünfte | seitliche Raum-Ankunftserkennung (Selman); **braucht B3** |

## Phase 3 — Cross-Owner (nicht Leonis-solo)

**Selman-Paket (größter GT-Hebel überhaupt)** — hebt die gepaart-Quote, auf der
Phase 2 aufsetzt:
- Zirkulations-**Knotengraph** (`nodes`/`edges`, heute leer) → entsperrt S-E/F/G/H.
- **KG-/Garage-/Kellerabteil-Erkennung** (2KG strukturell schwächstes Geschoss,
  fehlt 20; KG-Riegel leer).
- **Ausgänge innerhalb Raumpolygon** zuordnen → **Wurzel-Fix der EG/1KG-#5-WARNUNG**
  (macht S-D überflüssig bzw. sauber).
- **beidseitig-Wasserscheide** (0/8 getroffen).
- Regeln: RW-015/017/023/024/025/035/115/116/118/124/128/129.

**Enis-Paket (Norm-/Nachweis-Lane):** RW-108 (BF-WC-AP), RW-109 (Sanitär-Schwellen),
RW-112 (Gefährdungs-SL), RW-114 (Stufen-SL-Nachweis), RW-125 (SL-Teilflächen-Lux),
RW-126 (Außenweg-Nachweis), RW-130 (Schul-Einstufung), RW-131 (Endausgang-Dreiklang).

**Contract (3-Owner, T2):** RW-104/107 Schule → **Bildungsraum-Nutzungsklasse**
(`contracts/raum_modell.py`). Ohne diesen Typ ist Tomascheks Hauptregel
(Unterrichtsraum = Innen-Notlicht, Saal-Antipanik flächenbezogen) nicht
ausdrückbar. Braucht Owner-GO + Selman (Erkennung) + Enis (Norm) + Contract-Freeze.

## Mess- & DoD-Strecke (jeder Slice)

- `scripts/analyse/mollgasse_gt_vergleich.py <Geschoss>` — typ_match/gepaart vor/nach.
- **Hausfeld-2DG-Wächter**: 2DG bleibt 3/3 `left` (kein Rückfall auf blanket-down).
- `pytest tests/{platzierung,naht,e2e,contract}` + `-m visual` Golden + `ruff`.
- Codex-Review je substanziellem Slice (CLAUDE.md), Regelquellen schlagen Codex.
- Owner-offene Fragen B1–B3 sind harte Vorbedingungen, nicht hardcoden.

## Empfohlene Reihenfolge (netto)

1. **Blocker:** B1 ✅ (kein Drossel), B3 ✅ (Engine korrekt), B4 ✅ (ja, aber Enis-Naht). **Nur B2 bleibt offen** (0 mm vs 735–930 mm).
2. **S-A + S-C** (Leonis-pur, Golden-Risiko beherrschbar, direkter Typ/Position-Gewinn).
3. **S-B** — Aufheller-Mehrfachbedienung (Platzierungs-Treue, kein Drossel).
4. **S-AUDIT** anstoßen = Leonis+Enis-Naht (Enis registriert „Referenz-Praxis: RW-xxx" in `quellen`).
5. **Selman-Paket anstoßen** (Knotengraph + KG + Ausgang-in-Raum) — entsperrt den
   eigentlichen gepaart-Hebel.
6. **Phase 2 (S-E…S-I)** sobald Selman liefert.
7. **Enis-/Contract-Pakete** parallel (eigene Lanes); RW-001-Feinschliff nach B2.

**Kurz:** Leonis kann den **Typ-Match** jetzt weiter heben (M3-Rest, S-A/C),
aber die **gepaart-Quote** (34 %) ist zu ~¾ Selman-gegated. Der Fahrplan baut
erst die Leonis-puren Gewinne, stößt dann das Selman-Paket an und schaltet Phase 2
nach.
