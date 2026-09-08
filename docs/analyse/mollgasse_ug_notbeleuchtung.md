# Mollgasse UG — unabhängige Notbeleuchtungs-Referenz aus den GU-Plänen

**Slice 4.1 (MEGA-Prompt 2026-09-07).** Quelle: GU-Elektro-Grundrisse
`S-24-2103-GU, 1180 Wien Mollgasse 15\Elektro\` (extern, read-only):
`MOL_GR-1KG_01-1-50_Index_4.pdf` · `MOL_GR-2KG_00-1-50_Index_5.pdf`.
Die 9-seitige Beilage „02B … -2KG-DG" enthält byte-identische Kopien beider
Seiten (Vektorzählung identisch) und wurde ignoriert. Werkzeug:
`scripts/analyse/mollgasse_ug_nb.py` (Extra `analyse`, keine Runtime-Deps).

## Kalibrierungsprotokoll

- Plankopf beider Blätter: Maßstab **1:50**, Rahmen **„1730 x 743"** (mm Papier).
- Gegenprobe: PDF-CropBox = 4904,28 × 2105,16 pt × 25,4/72 = **1730,1 × 742,7 mm**
  → Abweichung **< 0,1 %**. Faktor: 1 pt = 25,4/72 mm Papier × 50 = **17,6389 mm Modell**.
- Fixture-Koordinaten: mm Modell, Ursprung = linke untere MediaBox-Ecke, y nach
  oben (Seite ist 270°-rotiert + gecroppt; pdfplumber-Raum, dokumentiert im Skript).
- Maßketten-Gegenprobe (2 %-Kriterium des Auftrags): über den gezeichneten
  Blattrahmen geführt statt über einzelne Maßketten-Texte — der Rahmen ist die
  längste bemaßte Strecke des Blatts und damit der schärfere Test.

## Symbol-Findung (Methode)

NB-Symbole zeichnen als Vektor-Cluster in RGB **(0, 0.722, 0)** — exklusiv:
Legende nutzt (0, 0.867, 0)/(0.345, 0.729, 0.282), Fluchtweg-Strichlinien und
alle anderen Gewerke andere Farben. Planfeld = x < 4300 pt. Clustern per
Union-Find (Gap 6 pt ≈ 106 mm). **Jeder Cluster wurde als 288-dpi-Crop gerastert
und einzeln angesehen** (`reports/mollgasse_ug/<floor>/*.png`, gitignored);
Typ/Pfeilrichtung/Montage stehen als `SICHT`-Tabelle im Skript. 0 Cluster
blieben unklassifiziert; 4 tragen Konfidenz „mittel" (abgewinkelte Pfeile).

## Legende (E-Notbeleuchtung, beide Blätter)

- Rettungszeichenleuchte Fluchtrichtung **rechts / links / unten**, Dauerschaltung
  (Legende zeigt schlichte grüne Kästchen; die Plan-Instanzen tragen Piktogramme).
- Rettungszeichenleuchte Fluchtrichtung **Beidseitig**, Dauerschaltung.
- **Sicherheitsleuchte, Bereitschaftsschaltung** (grünes X-Rechteck).
- **KEIN** „Aufheller"-Typ, **KEINE** Antipanikleuchte in der Legende.

## Zählung

| Geschoss | RZ | davon Doppel (Rücken an Rücken) | SL | Antipanik |
|---|---|---|---|---|
| 1KG | 11 | 2 Paare (c06, c07) | 0 | 0 |
| 2KG | 30 | 6 Paare | 2 | 0 |

Pfeilrichtungen (im Plan): 1KG rechts 3 · unten 4 · oben 4 · links 0;
2KG oben 10 · rechts 8 · unten 7 · links 5. Symbolgröße einheitlich
**480 × 233 mm Modell** (9,6 × 4,7 mm Papier).

## Muster (in Worten)

- **RZ sitzen an Türen und Durchgängen**: direkt an/über Türöffnungen (Türmaß-
  Texte 80/200, 90/200, 100/200; oft `EI₂30-C`-Brandschutztüren, FTS) oder an
  Gang-/Fluchtweg-Strichlinien (hellgrün gestrichelt).
- **Montage folgt der Wand**: horizontale UND vertikale Symbol-Lagen; vertikal
  montierte RZ stehen seitlich am Türstock, Pfeil läuft die Wandachse entlang.
- **Doppel-RZ**: zwei Symbole Rücken an Rücken an Durchgängen mitten im
  Fluchtweg (von beiden Seiten lesbar) — deckt sich mit dem beidseitigen
  RZ_PLPR-Muster des Barawitzka-Profiplans.
- Die „unten"-Piktogramm-Variante hängt bevorzugt **horizontal direkt über der
  Tür** („durch diese Tür").
- Die 2 SL (2KG) markieren **Deckensprünge** in der Garage — Sonderstellen, je
  ~7 m vom nächsten RZ, NICHT als RZ-Begleiter.

## Befunde für Slice 2.3 (Messungs-Entscheid)

- **Regel A („Tür-RZ-unten → Pfeil links")**: Von 41 RZ zeigen **5 links (12 %)**
  — rechts 11, oben 14, unten 11. Auch an Türen keine Links-Dominanz: die
  Richtung folgt der FLUCHTRICHTUNG, nicht einer festen Konvention. → **G3**.
- **Regel B (Aufheller 500 mm)**: Der GU-Plan kennt **keinen Aufheller-Typ**;
  die einzigen 2 SL stehen ~7000 mm vom nächsten RZ (Deckensprung-Sonderstellen).
  Abstands-Histogramm Aufheller↔RZ ist **leer** → keine B1/B2-Entscheidung aus
  diesen Daten möglich. → **G4**.

## Unsicherheiten / Negativbefunde (ehrlich)

- `naechste_tuer_mm` ist die Distanz zum nächsten **Türmaß-Text** (80/90/100/200),
  nicht zur Tür-Geometrie — Näherung, unterschätzt „an Tür" systematisch
  (Text steht oft neben der Tür): 1KG 2/11, 2KG 8/30 unter 1,5 m; die
  Sichtprüfung zeigt deutlich mehr Tür-Nähe.
- Richtung bei 4 Clustern „mittel" (abgewinkelte Pfeile 2kg_c10/c15/c20/c25).
- Raumzuordnung nur als nächster Text-Schnipsel (`raum_text`), keine
  Polygon-Zuordnung.
- Aufheller vs. Antipanik in diesem Planwerk **nicht unterscheidbar/nicht
  vorhanden** — die Referenz beantwortet die 500-mm-Frage nicht.
- Die drei Richtungs-Legendeneinträge sind grafisch identische Kästchen; die
  Richtungs-Semantik wurde aus den Plan-Piktogrammen gelesen, nicht der Legende.

## Deliverables

- `tests/fixtures/mollgasse_ug_referenz_1kg.json` (11 Symbole)
- `tests/fixtures/mollgasse_ug_referenz_2kg.json` (32 Symbole)
- Crops: `reports/mollgasse_ug/{1KG,2KG}/` (gitignored, reproduzierbar via Skript)
