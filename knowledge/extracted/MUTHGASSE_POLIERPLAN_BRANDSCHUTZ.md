# Wissens-Digest — Muthgasse 109B Polierpläne: Brandschutz-Gerüst + 6. CAD-Familie

Quellen: `Projekte/Pläne 19., Muthgasse 109B - 2026-05-07_13-12/Architekt/Ausführungsplan/`
— 9 DXF-Etagen (E2–E9 + DD, via ODA aus DWG) + 9 HNP-Plan-PDFs. Gesichtet 2026-09-05
(PDF E2 visuell + alle 9 DXF programmatisch via ezdxf).

**Wichtigster Befund vorweg:** Die PDFs sind **ROHBAU-POLIERPLÄNE** (HNP architects
ZT GmbH für GEWOG, Wohnbau 1190 Wien, Vorabzug 01.05.2026, 1:100) — sie enthalten
**KEINE Notbeleuchtungs-Symbole** (auch die DXF: 0 Notlicht-Layer). Der Wert liegt
woanders: der Architekt liefert das komplette **Brandschutz-Gerüst**, das die
Engine als Eingabe braucht — inklusive **vorgerechneter Fluchtweglängen**.

---

## 1. Die Pläne tragen vorgerechnete Fluchtweglängen (FLW-L) — parsebar!

MTEXT auf Layer `A-FLOR-HRAL-IDEN`, Format `FLW-L 24,1 m` (+ `TSL-36,1 m` für die
Trockensteigleitung). Gemessen über alle Etagen:

| Etage | FLW-L-Vermerke | Raumstempel | Tür-Texte (EI-klassifiziert) |
|---|---|---|---|
| E2 | 16,1 · 24,1 · 18,3 m | 457 | 349 (24) |
| E3 | 16,0 · 37,2 · 24,1 m | 533 | 432 (28) |
| E4 | 37,2 · 16,0 · 24,1 m | 533 | 432 (28) |
| E5 | 16,0 · 37,2 · 24,1 m | 540 | 446 (29) |
| E6 | 16,0 · 37,2 · 24,1 m | 540 | 446 (29) |
| E7 | 37,2 · 24,1 m | 433 | 360 (24) |
| E8 | 36,4 · 24,1 m | 435 | 354 (22) |
| E9 | 26,3 m | 295 | 207 (13) |
| DD | — (Dachdraufsicht, 9 Stempel) | 9 | 0 |

**Norm-Abgleich (Repo-Wissen):** AStV/OVE-Fachinfo E08 (E08-R11): Fluchtweg i.d.R.
**max. 40 m** bis zum gesicherten Fluchtbereich (+ E08-R10: ≤ 10 m von jedem Punkt
bis zum Fluchtweg). Alle Muthgasse-Werte 16,0–37,2 m = **konform, aber hart an der
Grenze geplant** (37,2 m in 4 Etagen). Der Architekt weist die Längen selbst aus →
genau die Prüfgröße, die unsere vertagte **N2 Weglänge-Deckung** (Weglänge statt
Luftlinie) rechnen soll.

## 2. Brandschutz-Inventar der Pläne (Legende + Bestätigungen)

- **Brandabschnitts-Linien** als eigenes Legenden-Element + EI90/EI30/EI0-Wandtypen
  (Gipskartonständerwände klassifiziert) → bestätigt Digest-#14 (getrennter
  Sicherheitskreis je Brandabschnitt) als planbare Größe.
- **Türen mit Brandschutzklasse im Tür-Text**: `EI₂30`, `EI₂30-S₂₀₀` (Rauchschutz),
  13–29 klassifizierte Türen je Etage → matcht ONL-R41 (Treppenhaus = gesicherter
  Fluchtbereich, Türen EI₂30-C).
- **Legenden-Abkürzungen mit Sonderstellen-Charakter**: `F+H` (Feuerlöscher- und
  Hydrantenkasten!), `BRE` (Brandrauchentlüftung), `BST` (Brandschutztor), `DBA`
  (Druckbelüftung), `FW` (Feuerwehrlift), `TSL+SPR` (Trockensteigleitung+Sprinkler,
  Sprinkler-Detailpläne LD-426/427) → die Positionen, die der Sonderstellen-
  Contract #93 (`feuerloescher`/`hydrant`) transportieren soll, stehen im
  Architektenplan.
- E-Türöffner an Zugängen vermerkt.

## 3. Sechste CAD-Familie: AIA-Layer-Standard (Ursache der Crash-Klasse)

Die Muthgasse-DXF nutzen den **US-AIA-Layer-Standard** (66 Layer): `A-WALL`,
`I-WALL`, `A-DOOR`(+`-IDEN`/`-OPNG`/`-FRAM`), `A-AREA`(+`-BNDY`/`-IDEN`),
`S-STRS` (Stiegen), `A-FLOR-HRAL-IDEN` (FLW-Texte), `A-GLAZ`, `M-EQPM`, `P-SANR` …
**Darum crasht der Provider** (`bounds_mm` bricht ab): kein einziges
Mollgasse-Wandmuster (`A_Raeume`/`810 Raum`/`09-WEG`) matcht.

**Kipp-Anleitung für @polatselman (konkreter als bisher):**
- Wände: `A-WALL` + `I-WALL` (+ `A-WALL-PATT`)
- Räume: `A-AREA-BNDY` (Polygone) + `A-AREA-IDEN` (Stempel)
- Türen: `A-DOOR` + `A-DOOR-IDEN` (Text `T-E2-6-07-1` = Tür-ID mit Raum-Code!)
- Stiegen: `S-STRS`
- Fluchtweg-Metadaten: `A-FLOR-HRAL-IDEN` (`FLW-L …`)
- **Raumstempel-Format** (A-AREA-IDEN): `m²` / Raumname / Code / Belag, Code-Schema
  `{Etage}-{Top}-{Raum}` (z.B. `E2-7-01`); **`VF` = Verkehrsfläche** (`Gang
  E2-VF-13b`) → direkter GANG-Marker; Typen-Vokabular: Wohnküche · Zimmer · Bad ·
  WC · AR (Abstellraum) · SR · Vorraum/Vorr. · Loggia · Gang · STGH (Stiegenhaus).

## 4. Engine-Konsequenzen (Vergleich mit dem bestehenden Wissen)

1. **N2 Weglänge-Deckung bekommt Golden-Werte:** engine-gerechnete Weglänge je
   Fluchtweg vs. FLW-L-Vermerk des Architekten = Validierungsregel mit externem
   Soll (neu — bisher hatten wir kein unabhängiges Soll für Weglängen).
2. **Wohnbau-Kontext fürs OIB-Gate:** GEWOG-Wohngebäude → Erforderlichkeits-Frage
   (OIB RL 2) läuft exakt über das gebaute, aber approvals-blockierte Gate
   #87/#88 (`projekt_kontext`).
3. **Sonderstellen-Quelle bestätigt:** F+H/BRE/BST-Positionen stehen in
   Architektenplänen — #93 hat eine reale Datenquelle (bisher Befund: „kein Typ
   automatisch erkennbar" — für die Mollgasse-Familie; Muthgasse widerlegt das
   für die AIA-Familie zumindest auf Legenden-/Symbol-Ebene).
4. **Erkennungsweiten-Naht:** Gang-Schenkel bis 37,2 m → hinterleuchtete RZ
   (z=200) brauchen bei l=z·h mit h=150 mm genau 30-m-Ketten; ONL-R70-Tabelle
   (40 m → 200 mm Piktogramm) wird auf solchen Fluren real bindend — die
   Sichtlinien-Verdichtung (`l = z·h`) ist hier kein Theorie-Fall.
5. **E2E-Netz:** der raises-Assert (Crash-Klasse) kann nach Selmans AIA-Mapping
   auf echte Bänder kippen: ~50–70 Räume/Etage erwartbar (457–540 Stempel ÷
   ~8 Zeilen je Raum), 3 Stiegenhäuser/Kerne (3 FLW-Vermerke E2–E6).

## 5. Grenzen dieser Sichtung

- PDF nur E2 visuell geprüft (E3–E8 = Regelgeschoss-Varianten desselben Systems,
  DXF-seitig programmatisch bestätigt; DD = Dachdraufsicht ohne Relevanz).
- Kürzel `BL`/`BFL`/`RAR`/`S1.2`/`SA` im Plan nicht sicher aufgelöst (nicht in
  der Legende) — nicht spekulativ verwerten.
- Es existiert (noch) kein Elektro-/Notbeleuchtungsplan im Paket — wenn der
  E-Planer-Stand kommt, wäre er das Soll für einen Muthgasse-Golden-Vergleich.
