# 0001 — Raumerkennung: Sprache (Python bleibt) + ML-Strategie

**Status:** angenommen · **Datum:** 2026-08-30 · **Betrifft:** Selman
(`raumerkennung/`) + Enis (`normwissen/`, LB-Input) · **Kontext:** verifizierter
Voll-Durchstich auf echten Plänen (siehe unten).

## Frage
Kommt die Raumerkennung mit **C++ oder Rust** schneller voran? Und wie können wir
**ML** einsetzen?

## Entscheidung
1. **Kein Sprachwechsel. Python bleibt.** C++/Rust bringen die Raumerkennung nicht
   voran — der Engpass ist **Algorithmus-Korrektheit**, nicht Rechengeschwindigkeit.
2. **ML nur als Augmentation**, nie als Norm-Entscheider. Deterministische Geometrie +
   Norm bleiben die auditierbare Quelle; ML füllt Lücken + markiert Unsicherheit.

## Begründung — warum nicht C++/Rust

**Der Blocker ist nicht CPU-Last.** Verifikation am 2026-08-30 (echtes Trio
`build_default_bundle` auf realen DXF):

| Plan | „Räume" | typisiert | ≥5 m² | med. Fläche | Türen | Ausgänge | Zirk-Nodes |
|---|---|---|---|---|---|---|---|
| Mollgasse EG | 185 | 0 | 7 | 0.2 m² | 44 | 4 | 154 |
| Barawitzka EG | 2 | 1 | 2 | 5.8 m² | 116 | 0 | 0 |
| Herrenholz EG | 473 | 193 | 211 | 4.1 m² | 140 | 0 | 0 |

Kein Plan bekommt alle 4 nötigen Layer (echte Räume + Typ + Ausgänge + Zirkulation)
zusammen → 0 platzierte Symbole. Das sind **Heuristik-/Geometrie-Probleme**
(Gap-Healing über Doppellinien-Wände + Türlücken, Raum-Typisierung, Ausgangs-Erkennung,
je-CAD-Familie andere Layer-Konventionen) — **sprachunabhängig**. Ein Rewrite fixt
keinen einzigen dieser Fälle; die Fragmente entstünden in Rust identisch.

**Kosten eines Rewrites:**
- **Ökosystem weg:** Python hat `ezdxf` (kein ernstes Rust/C++-Äquivalent), `shapely`
  (GEOS), `scikit-image`, `networkx`. In Rust/C++ = DXF-Parser + Computational Geometry
  neu bauen oder eh gegen GEOS/CGAL binden.
- **Tempo weg:** das Team fährt schnell parallel in Python; Rewrite = Monate Stillstand
  für 0 neue Korrektheit.
- **Kein realer Python-Flaschenhals:** die schweren Teile (Raster-Flood-Fill via
  scikit-image, numpy) laufen bereits in C unter der Haube.

**Wann Rust/C++ doch sinnvoll wäre — aktuell NICHT der Fall:**
- Echte Performance-Wand bei Riesen-DXF (z.B. Baufeld E2 > 100 MB), falls `ezdxf`
  timeout/RAM sprengt.
- Ein einzelner heißer Geometrie-Kernel (robuste Polygon-Arrangement / Boolean-Ops
  at scale).
- **Selbst dann:** gezielte Native-Extension (PyO3/pybind11) für genau den Hot-Path —
  **kein** Full-Rewrite. Python bleibt Orchestrierung.

## Weg vorwärts in Python (ohne ML)
1. **`raumlayer.py` ausbauen** — Räume von dedizierten Layern lesen statt aus Wänden
   polygonisieren. Läuft schon: Fischamender 68, Herrenholz 473, Baufeld 220 echte
   typisierte Räume, „löst das Schlitz-Problem auditierbar".
2. **Gap-Healing** für Familien ohne Raum-Layer (Mollgasse) — shapely buffer/union-
   difference tunen (virtuelle Wände über Türlücken).
3. **Ausgang + Zirkulation pro CAD-Familie** (Layer-Muster wie `WALL_PATTERN`) — fehlt
   bei Herrenholz/Barawitzka.

## ML-Strategie

**Leitprinzip (bindend):** Das Produkt ist ein **norm-konformer, auditierbarer**
Notbeleuchtungsplan. Eine ML-Blackbox darf **keine** Norm-Entscheidung allein treffen.
ML = Assistenz mit **Confidence-Score + deterministischem Fallback + Audit-Trail**
(analog `norm_quelle`); bei niedriger Confidence → deterministischer Pfad / Human-in-
the-Loop. Das steht im Einklang mit dem bewussten „kein ML" von `raumlayer.py` (dort
sind die Daten schon sauber da — kein ML nötig).

**Datenlage:** nur ~6 reale Projekte (Mollgasse, Fischamender, Barawitzka, Herrenholz,
Baufeld E2 + DIN-Beispiele). Zu wenig für Deep Nets from scratch → **Low-Data-Methoden
und vortrainierte Modelle/LLMs bevorzugen**; die Projekte als Eval-/Golden-Set
hand-labeln, nicht als Trainings-Futter verheizen.

Nach ROI/Machbarkeit geordnet:

1. **LB-Parsing (Enis, 2. Input) — LLM-Struktur-Extraktion.** Freitext-Leistungs-
   beschreibung → strukturierte `LBVorgabe` (Produkte, Stückzahlen, Sonderwünsche).
   Klassischer LLM-Case (few-shot, kein Training), hoher Wert, direkt am Nordstern.
   **Bestes Erst-ML-Projekt.**
2. **Raum-Typ-Klassifikation (tabellarisch).** Wenn Räume polygonisiert sind: `raum_typ`
   aus Geometrie+Text-Features (Fläche, Seitenverhältnis, #Türen, Nachbarschaft, Text
   in der Nähe) via Gradient-Boosting. Ein paar hundert Räume über die Projekte reichen.
   Günstig, robust, erklärbar. Füllt Typen, wo Stempel/Label fehlen.
3. **Text → `raum_typ`-Mapping.** Raum-Namen sind chaotisch („Büro 3", „WC-D", „Stg.").
   Embedding-/Fuzzy-Match oder kleiner LLM-Call → Enum. Kein Training nötig.
4. **Layer-Konventions-Mapper (LLM few-shot).** Statt hartkodierter `WALL_PATTERN`:
   LLM bekommt die Layer-Namen eines neuen DXF und klassifiziert Wand/Raum/Tür/
   Fluchtweg → automatische Anpassung je CAD-Familie.
5. **CV-Grundriss-Segmentierung (U-Net / vortrainiert).** Grundriss rastern →
   semantische Segmentierung → Raum-Masken → vektorisieren. Adressiert genau das
   Fragment-/Gap-Healing-Problem, das reine Geometrie schwer löst. Größter Aufwand,
   braucht Daten → **Transfer-Learning / vortrainierte Floor-Plan-Modelle**
   (z.B. CubiCasa5k) statt from scratch. Später, als Fallback wo Layer-Reader versagt.

**Empfohlene Reihenfolge:** (1) LB-Parsing zuerst (eigenständig, hoher Wert, wenig
Daten) → (2)+(3) Raum-Typ/Text-Mapping (nutzt vorhandene Geometrie) → (4) Layer-Mapper
→ (5) CV-Segmentierung nur falls (1) Weg-vorwärts-in-Python die Fragmente nicht löst.

## Konsequenzen
- Selman: kein Rewrite; Fokus auf `raumlayer.py` + Gap-Healing + Familien-Ausgänge.
- Enis: LB-Parsing ist der natürliche ML-Einstieg (2. Input → `LBVorgabe`).
- Jede ML-Ausgabe trägt Confidence + Audit-Quelle; deterministischer Pfad bleibt
  autoritativ (Norm-Konformität).
