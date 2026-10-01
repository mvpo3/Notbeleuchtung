# Parallel-Abgleich PDF ↔ DXF — Mollgasse 4OG (Notbeleuchtungserklärung)

Quellen:
- PDF-Erklärtext Seiten 31–38 (`pdf_seiten/text.txt` + `seite_31.png` … `seite_38.png`)
- DXF: `knowledge/Pläne zeichnen Wissen/Mollgasse-Notbeleuchtungserklärung/WHA_MOL_4OG_Notbeleuchtung_Erklärung.dxf`
  (AC1032, $INSUNITS=4 = mm, alle Inhalte im Modelspace, Paperspace leer)

Konventionen (an diesem DXF verifiziert):
- Welt-Pfeil einer RZ-Leuchte = Basis-Orientierung + INSERT-Rotation
  (ARR-down Basis 270°, ARR-left Basis 180°, RZ-ARR_right Basis 0°).
- PDF-Bezeichnung „Pfeil nach links/rechts/unten" = **Produkttyp** (Pfeil im
  ungedrehten Symbol = Blockname), NICHT die Weltrichtung im Plan.
- Menschsymbol `750298750`: Blickrichtung = (180°+rot) bei xscale>0,
  (0°+rot) bei xscale<0 (gespiegelt). Verifiziert gegen Fluchtwegpfeile
  (z.B. h=414D2 rot=356.98 xs=+4.0 → Blick 176.98° West = Stiegen-Abstieg;
  h=41277 rot=11.86 xs=−4.0 → Blick 11.86° Ost = Gangfluss Ost).
- Fluchtwegpfeil `4444444`: Weltrichtung = (180°+rot).
- Türkis (ACI 4) = Sichtlinien Person→Leuchten-Kante; Grün (ACI 3) =
  Fluchtweg/Labels; Rot (ACI 1) = nachgezeichneter Stiegenhauspfeil inkl.
  MTEXT „Stiegenhauspfeilrichtung".

Es gibt im 4OG **zwei erklärte Bereiche**:
West-Stiegenhaus (Top 18/19, Seiten 31–32) und Ost-Stiegenhaus
(Top 23–26 + DG-Abstieg, Seiten 33–38).

---

## 4OG-01 — Top 18/19: Sichtbarkeit + Rotation der Notleuchte (A) [PDF S.31]

**PDF-Aussage:** Bewohner von Top 18 und Top 19 sehen beim Verlassen der
Wohnung unmittelbar die Notleuchte (A) „mit Pfeil nach links"; wäre sie anders
ausgerichtet, sähen sie nur die Seite statt der Vorderseite.

**DXF-Fakten:**
- (A) = `RIVO-SIBEL-ARR-left` **h=41249**, Zentrum (−75883, 30933), rot=269.42°,
  xs=36.10, Weltmaß 325×641 mm (Portrait, Längsachse N–S).
  Welt-Pfeil = 180+269.42 = **89.42° ≈ Nord (oben)**; „links" = Produkttyp ARR-left.
- Label `(A)` MTEXT h=4124A bei (−75667, 31272); Raum-Attribute TOP 18
  h=400AE (−77361, 30132), TOP 19 h=40049 (−78028, 30626).
- Westkante der Leuchte (−76045) liegt an der Wandkante x=−76030 → am
  Gang-Ende montiert, Vorderseite (Flächennormale O–W) nach **West** zu den
  Wohnungstüren.
- Sichtlinien (ACI 4):
  - h=41280 (−78462,30901)→(−76043,30934): **L=2419 mm**, Richtung 0.8°,
    Winkel zur Vorderseiten-Normalen ≈ **0.8° = frontal** (Person Top 19,
    h=41277, Blick 11.86° Ost).
  - h=41281 (−77641,29735)→(−76027,30939): **L=2014 mm**, Richtung 36.7°,
    Winkel zur Normalen ≈ **36.7°** = noch klar Vorderseite (Person Top 18,
    h=41222, Blick 101.86° ≈ Nord).
- Fluchtweg: Gang Ost-West y≈30635, Pfeile h=412AE/AF/B0 Welt 359.87° (Ost)
  → zur (A), dann Nord (h=412B2, Welt 89.87°).

**Status: praezisiert** — „Pfeil nach links" ist der Produkttyp; im Plan zeigt
der Welt-Pfeil 89.42° (Nord = weiterer Fluchtweg zu (B)). Vorderseiten-Aussage
geometrisch bestätigt (Sichtlinien 0.8°/36.7° zur Normalen; die Längsachse
steht senkrecht auf beiden Sichtlinien-Korridoren).

Bild: `4OG-01.png`

---

## 4OG-02 — West-Stiegenhaus: (A)→(B), (B) mittig+Pfeil auf Stiege, DG→(C) [PDF S.32]

**PDF-Aussagen:**
1. (A) zeigt mit „Pfeil nach links" den Weg zur nächsten Notleuchte (B).
2. (B) „mit Pfeil nach rechts", mittig im Gang, an einer Stelle, an der der
   Pfeil auf die Stiege zeigt; Menschen flüchten entgegen dem rot
   nachgezeichneten Stiegenhauspfeil nach unten.
3. DG-Menschen sehen beim Hinuntergehen ins 4. OG die Notleuchte (C) „mit
   Pfeil nach links"; Pfeil entgegen dem Stiegenhauspfeil; (C) an der Wand
   (Alternative: mittig zur Stiege).

**DXF-Fakten:**
- (A) h=41249 Welt-Pfeil 89.42° Nord → (B) liegt exakt nördlich:
  Abstand (A)-Zentrum→(B)-Zentrum = **1653 mm** (Δx nur 57 mm) im selben
  N–S-Gang. ✓
- (B) = `RIVO-RZ-ARR_right` **h=4121F**, Zentrum (−75940, 32585), rot=359.87°,
  xs=1.37, 637×320 mm (Landscape). Welt-Pfeil **359.87° ≈ Ost (rechts)**.
  Label `(B)` h=412DA (−76184,32936).
  - „Mittig im Gang": N–S-Gang-Innenkanten x=−76792 / −75065
    (Breite **1727 mm**), Mitte x=−75928 → (B)-Zentrum weicht **12 mm** ab. ✓
  - „Pfeil auf die Stiege": Abwärtslauf (8 HÖHEN, h=401CD bei (−73991,32515))
    beginnt ≈300 mm östlich von (B); grüner Fluss auf dem Lauf h=412B3/41305
    Welt 359.87° Ost. ✓
  - Sichtlinie h=4132E (−76225,33702)→(−75917,32744): **L=1006 mm**, Winkel
    zur (B)-Normalen (N–S) ≈ **17.8° = frontal** (DG-Person h=41329,
    Blick 257.5° Süd).
- Stiegenhauspfeil (rot nachgezeichnet, Original grau daneben):
  - oberer Lauf (9 HÖHEN, h=40042 (−74479,34018)): Polylinie h=412FC
    (−72716,34009)→(−74971,34020) mit Pfeilspitze h=412FD Apex (−72731,34009)
    → zeigt **0° Ost**; Label „Stiegenhauspfeilrichtung" h=4168B.
  - unterer Lauf (8 HÖHEN): h=412FE Apex (−74698,32519) → zeigt **180° West**;
    Label h=416AE. Pfeilkette = Aufwärtsrichtung 4OG→DG (unten O→W, oben W→O).
  - DG-Personen exakt entgegen: oberer Lauf h=41303 Blick 167.9° (West),
    Wende-Podest h=41329 Blick 257.5° (Süd), unterer Lauf h=4132D/41301
    Blick 11.9° (Ost). ✓ „entgegen der Richtung des Stiegenhauspfeils"
    geometrisch belegt (Δ ≈ 180°).
- (C) = `RIVO-SIBEL-ARR-left` **h=41220**, Zentrum (−72424, 34451), rot=359.42°,
  641×325 mm (Landscape). Welt-Pfeil **179.42° ≈ West (links)** =
  entgegengesetzt zum oberen Stiegenhauspfeil (0° Ost). ✓
  Label `(C)` h=41225 (−72061,34594).
  - „An der Wand": Zentrum 101 mm von der Wandkante y=34552 (Nordwand des
    DG-Ankunfts-/Podestbereichs). ✓ (C) sitzt am Ost-Ende des oberen Laufs =
    dort, wo DG-Menschen ankommen; Welt-Pfeil West = Abstiegsrichtung.
- Weiterer Verlauf ab (C): grüne Polylinie h=41285 (−72743,34454)→(−75874,34461)
  →(−75878,32744) (Gang „GANG 6.03m2" West, dann Süd zu (B)); Pfeile
  h=412B4/B5 Welt 179.87° West. ✓

**Status: praezisiert** — alle Aussagen geometrisch bestätigt; Pfeilnamen
sind Produkttypen ((B) „rechts" = Welt-Pfeil Ost, (C) „links" = Welt-Pfeil
West), Zahlen siehe oben.

Bild: `4OG-02.png`

---

## 4OG-03 — Gang Top 23/24: Notleuchte (A) „Pfeil nach unten" [PDF S.33–34]

**PDF-Aussagen:** (A) mit Pfeil nach unten, rotiert, sodass der Pfeil in die
entgegengesetzte Richtung des Fluchtwegs zeigt; Bewohner Top 23/24 sehen die
Vorderseite (eine links/rechts-Variante würde nur seitlich gesehen);
Bedeutung: „dem Fluchtweg geradeaus weiter folgen".

**DXF-Fakten:**
- (A) = `RIVO-SIBEL-ARR-down` **h=413A0**, Zentrum (−35385, 8592), rot=179.71°,
  xs=35.64, 631×318 mm (Landscape, Längsachse O–W). Welt-Pfeil = 270+179.71 =
  **89.71° ≈ Nord** — Fluchtweg fließt **269.87° Süd** (Pfeile h=41541/42/43)
  → exakt entgegengesetzt (Δ=179.8°). ✓
  Label `(A)` h=413A1 (−35052,8668).
- Gang: N–S, Innenkanten x=−35995 / −34475 (**Breite 1520 mm**), Mitte
  x=−35235; (A)-Zentrum 150 mm westlich der Gangachse (annähernd mittig).
- Räume: TOP 23 h=404BE (−35995,10719), TOP 24 h=404CE (−35325,10809).
- Sichtlinien (eine türkise Polylinie h=4145A mit 2 Schenkeln, Treffpunkt =
  (A)-Nordkante (−35384,8749)):
  - von Top-23-Person h=41433 (−36186,10555): **L=1958 mm**, Winkel zur
    Vorderseiten-Normalen (N–S) ≈ **15.2° = frontal**.
  - von Top-24-Person h=41458 (−35359,11437): **L=2789 mm**, Winkel ≈
    **6.5° = frontal**.
- Vorderseiten-Argument: Längsachse O–W ⇒ Normale N–S ⇒ von Norden kommende
  Personen sehen die Front. Eine ARR-left-Variante mit Welt-Pfeil Süd wäre
  Portrait (Längsachse N–S) ⇒ Sichtlinien ≈ parallel zur Längsachse =
  Seitenansicht. Geometrisch nachvollziehbar. ✓

**Status: bestaetigt** (mit Präzisierung: Welt-Pfeil 89.71° Nord, Fluss Süd,
Sichtwinkel 6.5°/15.2°).

Bild: `4OG-03.png`

---

## 4OG-04 — Gang Top 25/26: Notleuchte (B) „Pfeil nach links" [PDF S.34–35]

**PDF-Aussagen:** Bewohner Top 25/26 sehen unmittelbar (B) mit Pfeil nach
links; „links" gewählt, weil die Stiege links liegt und der Pfeil direkt auf
die Stiege zeigt; zwei Bedingungen: Vorderseite sichtbar + Pfeil Richtung
Stiege.

**DXF-Fakten:**
- (B) = `RIVO-SIBEL-ARR-left` **h=41593**, Zentrum (−35752, 4564), rot=359.42°,
  641×325 mm (Landscape). Welt-Pfeil **179.42° ≈ West (links)**. ✓
  Label `(B)` h=4156F (−35323,4629).
- Stiege liegt West: 17-HÖHEN-Lauf (h=4042B (−41305,4529)) Ostkante x=−37385,
  d.h. **1633 mm** westlich von (B); grüne Fortsetzung h=41461
  (−36020,4568)→(−41995,4568) exakt in Pfeilrichtung. ✓
- Räume: TOP 25 h=404D2 (−35045,3489), TOP 26 h=404C2 (−35750,2859).
- Fluchtweg-Zufluss von Süden: h=4145D (−35750,2677)→(−35732,4405) Nord,
  Pfeile h=41544/45 Welt 89.87° Nord.
- Sichtlinien (h=4140F, Treffpunkt = (B)-Südkante (−35703,4405)):
  - von Top-26-Person h=4140D (−35696,2846): **L=1551 mm**, Winkel zur
    Normalen ≈ **9.6° = frontal**.
  - von Top-25-Person h=4137B (−34563,3515): **L=1225 mm**, Winkel ≈
    **45.5°** = schräg, aber Vorderseite.
- Bedingung 1 (Vorderseite): Längsachse O–W, Personen von Süden → frontal ✓.
  Bedingung 2 (Pfeil zur Stiege): Welt-Pfeil West = Stiegenrichtung ✓.

**Status: bestaetigt** (Zahlen wie oben).

Bild: `4OG-04.png`

---

## 4OG-05 — Vergleich „Pfeil nach unten statt Pfeil nach links" (hypothetisch) [PDF S.35–36]

**PDF-Aussage:** Würde man statt (B) eine Pfeil-nach-unten-Leuchte verwenden
(rotiert, damit der Pfeil zur Stiege zeigt), sähen die Menschen sie seitlich;
Pfeilrichtung nicht erkennbar → falsch. Pfeil nach rechts wäre ebenfalls
nicht sinnvoll, wenn links möglich ist.

**DXF-Fakten:**
- Am Ort (−35752,4564) existiert **nur** die reale ARR-left h=41593; keine
  ARR-down-Variante im Bestand. Die PDF-Bilder S.35/36 sind
  AutoCAD-Momentaufnahmen (im Screenshot S.35 ist der Befehls-Prompt
  „Basispunkt angeben" sichtbar).
- Geometrische Logik der Aussage prüfbar: eine ARR-down mit Welt-Pfeil West
  (rot≈269.7°) wäre Portrait (318×631, Längsachse N–S) → Sichtlinien der
  Top-25/26-Personen (Richtungen 80.4°/135.5°) verliefen dann in ≈9.6°/45.5°
  zur **Längsachse** statt zur Normalen → Seitenansicht. ✓
- Bemerkenswert: außerhalb des Grundrisses steht eine **freie Kopie genau
  dieser Vergleichsvariante**: `RIVO-SIBEL-ARR-down` h=41221, Zentrum
  (−92576, 35298), rot=269.71°, Portrait, Welt-Pfeil 179.71° West, mit
  grünem Label `(A)` h=41224 (−92418,35526) — 16.6 m westlich von (B)-West,
  ohne Wände/Fluchtweg (siehe `4OG-08-unerklaert.png`).

**Status: bestaetigt** (konzeptionelles Vergleichsbeispiel; kein realer
DXF-Bestand am Ort — erwartungsgemäß).

Bild: `4OG-05.png`

---

## 4OG-06 — Blickrichtung + „falsch"-Beispiel bei (C) am Ost-Stiegenhaus [PDF S.36–37]

**PDF-Aussagen:** Zeigt die (C)-Position mit einer falschen Variante (rot
umrandet, „falsch", türkise Linie „schaut seitlich auf Notleuchte"): der
Mensch (DG) sähe die Leuchte von der Seite. Regel: Verläuft der Fluchtweg aus
Sicht des Menschen (DG) nach rechts, muss eine Notleuchte mit Pfeil nach
rechts verwendet werden; die Pfeilrichtung muss der tatsächlichen weiteren
Fluchtrichtung aus Sicht der Person entsprechen.

**DXF-Fakten:**
- Rote Umrandung, Text „falsch" und Text „schaut seitlich auf Notleuchte"
  existieren **nicht** im DXF (nur im PDF-Screenshot; temporäre Variante).
- Die reale (C) = `RIVO-RZ-ARR_right` **h=415B6**, Zentrum (−42975, 4646),
  rot=89.87°, xs=1.37, 320×637 mm (Portrait, Längsachse N–S).
  Welt-Pfeil **89.87° ≈ Nord**.
- Sichtlinie h=41645 (−42816,4806)→(−39474,4852): **L=3342 mm**, Richtung
  180.8°; zur realen (C) (Normale O–W): Winkel ≈ **0.8° = frontal**.
  Dieselbe Linie gegen die „falsche" Landscape-Variante (Längsachse O–W)
  ergäbe ≈ **89° = Seitenansicht** — exakt der im PDF gezeigte Unterschied. ✓
- Regelvalidierung: DG-Person h=414D4 (−39387,4581) Blick 176.98° West;
  Fluchtweg ab (C): grüne Polylinie h=415DA (−42969,4967)→(−42967,5987)→
  (−41750,5992) = Nord, dann Ost. Aus Sicht der nach West gehenden Person
  ist Nord = **rechts** → DXF verwendet den Produkttyp ARR_right. Die
  PDF-Regel von S.37 ist im DXF exakt umgesetzt. ✓

**Status: praezisiert** — „falsch"-Inszenierung nur im PDF; reale Geometrie
und S.37-Regel decken sich (Winkel 0.8° vs. ≈89°).

Bild: `4OG-06.png`

---

## 4OG-07 — DG-Abstieg Ost: Kette (C) → (D) → (B) [PDF S.38]

**PDF-Aussagen:** DG-Menschen kommen ins 4. OG und sehen „(C) mit Pfeil nach
links"; danach (D) mit Pfeil nach unten (geradeaus); anschließend (B) mit
Pfeil nach links; Flucht im Stiegenhaus entgegen dem rot nachgezeichneten
Stiegenhauspfeil.

**DXF-Fakten:**
- Stiegenhauspfeil rot nachgezeichnet: h=41462 (−41865,4529)→(−37385,4529),
  Pfeilspitze Apex (−37385,4529) → **0° Ost**; Label „Stiegenhauspfeilrichtung"
  h=416D1 (−41463,4457). Original grau: 17-HÖHEN-Lauf h=4042B.
- DG/4OG-Personen h=414D2 (−36506,4574), h=414D7 (−37946,4577), h=414D4
  (−39387,4581): Blick je **176.98° West** = entgegen (Δ=177°). ✓
- (C) h=415B6 (Details in 4OG-06): Welt-Pfeil **89.87° Nord**; steht
  **1110 mm** westlich des Laufendes (x=−41865), zwischen Wandkanten
  x=−43190/−42795 („an der Wand"). Sichtlinie 3342 mm frontal (0.8°).
  - **WIDERSPRUCH zur PDF-Formulierung:** S.38 nennt „(C) mit Pfeil nach
    links"; das DXF zeigt den Produkttyp `RIVO-RZ-ARR_right` (Pfeil nach
    RECHTS), Welt-Pfeil Nord. Aus Sicht der von Osten kommenden Person liegt
    der weitere Fluchtweg rechts (Nord) — die PDF-eigene Regel von S.37
    fordert hier ausdrücklich „Pfeil nach rechts". PDF-S.38-Text sagt X
    („links"), DXF zeigt Y (ARR_right / rechts) → vermutlich Schreibfehler
    im PDF.
- (D) = `RIVO-SIBEL-ARR-down` **h=413E8**, Zentrum (−39711, 6006), rot=269.71°,
  318×631 mm (Portrait). Welt-Pfeil = 270+269.71−360 = **179.71° ≈ West**;
  Gangfluss dort **359.87° Ost** (Pfeile h=414FB (−40222,6025), h=4151E
  (−37665,6021)) → Pfeil entgegen Fluchtrichtung, Bedeutung „geradeaus". ✓
  Label `(D)` h=415D9 (−39847,5661).
  - Gang O–W: Innenkanten y=5429 / 6699 (**Breite 1270 mm**), Mitte y=6064;
    (D)-Zentrum weicht **58 mm** ab → mittig im Gang.
  - Vorderseite: Längsachse N–S ⇒ Normale O–W ⇒ von West kommende Personen
    frontal. ✓
- (B) h=41593 (Details in 4OG-04): Welt-Pfeil 179.42° West = nächste
  Richtungsänderung zur Stiege. Zufluss von Nord: Gangfluss Süd
  (h=4154A Welt 89.87°? — konkret: Pfeile im STGH-Vorfeld h=41546
  (−35508,3485) Welt 179.87° West Richtung Lauf). ✓ „(B) mit Pfeil nach
  links" = Produkttyp ARR-left ✓.

**Status: widerspruch** (nur bei der (C)-Pfeilbezeichnung „links" vs.
DXF ARR_right/rechts; alle übrigen Aussagen der Seite geometrisch bestätigt).

Bild: `4OG-07.png`

---

## Abdeckung

Notbeleuchtungs-INSERTs im Modelspace: **8** (keine Antipanik-/Aufheller-/
Spot-/Gruppenbatterie-Symbole im 4OG-DXF; keine ungelabelten Leuchten —
alle 8 haben ein grünes MTEXT-Label):

| Handle | Block | Zentrum | Label | Beispiel |
|---|---|---|---|---|
| 41249 | RIVO-SIBEL-ARR-left | (−75883, 30933) | (A) West | 4OG-01/02 |
| 4121F | RIVO-RZ-ARR_right | (−75940, 32585) | (B) West | 4OG-02 |
| 41220 | RIVO-SIBEL-ARR-left | (−72424, 34451) | (C) West | 4OG-02 |
| 413A0 | RIVO-SIBEL-ARR-down | (−35385, 8592) | (A) Ost | 4OG-03 |
| 41593 | RIVO-SIBEL-ARR-left | (−35752, 4564) | (B) Ost | 4OG-04/05/07 |
| 413E8 | RIVO-SIBEL-ARR-down | (−39711, 6006) | (D) Ost | 4OG-07 |
| 415B6 | RIVO-RZ-ARR_right | (−42975, 4646) | (C) Ost | 4OG-06/07 |
| 41221 | RIVO-SIBEL-ARR-down | (−92576, 35298) | (A) frei | **unerklärt** |

Unerklärt: **h=41221** — freie Kopie außerhalb des Grundrisses (16.6 m
westlich von (B)-West, keine Wände/kein Fluchtweg), Portrait, Welt-Pfeil
179.71° West, mit Label (A) h=41224. Entspricht exakt der
„Pfeil-nach-unten-statt-links"-Vergleichsvariante der Seiten 35/36 →
vermutlich Arbeits-/Screenshotkopie. Siehe `4OG-08-unerklaert.png`.

---

## Regel-Beobachtungen (Rohstoff für Regelbasis)

1. **Pfeilbezeichnung = Produkttyp:** „Pfeil nach links/rechts/unten" im PDF
   benennt den Blocknamen (ARR-left/right/down im ungedrehten Zustand), nicht
   die Weltrichtung. Beleg: (A)-West „links" = ARR-left rot=269.42 →
   Welt-Pfeil 89.42° Nord [4OG-01]. Einzige Abweichung: S.38 „(C) links"
   vs. ARR_right [4OG-07].
2. **Welt-Pfeil von links/rechts-RZ = tatsächliche Weiterlaufrichtung:**
   (B)-West 359.87° Ost → Abwärtslauf beginnt ~300 mm östlich; (B)-Ost
   179.42° West → Laufkante 1633 mm westlich; (C)-West 179.42° West =
   Abstiegsrichtung [4OG-02, 4OG-04].
3. **ARR-down wird mit Welt-Pfeil ENTGEGEN der Fluchtrichtung rotiert**
   (Bedeutung „geradeaus"): (A)-Ost 89.71° vs. Fluss 269.87° (Δ179.8°);
   (D)-Ost 179.71° vs. Fluss 359.87° (Δ180°) [4OG-03, 4OG-07].
4. **Vorderseiten-Regel messbar:** Sichtlinienwinkel zur Flächennormalen
   (Normale ⊥ Symbol-Längsachse) bei allen realen Platzierungen 0.8°–45.5°
   (frontal/schräg-frontal); die bewusst falschen Varianten ergäben ≈89°
   (parallel zur Längsachse = Seitenansicht) [4OG-01: 0.8°/36.7°;
   4OG-03: 6.5°/15.2°; 4OG-04: 9.6°/45.5°; 4OG-06: 0.8° vs. 89°].
5. **Symbol-Orientierung folgt dem Betrachter-Korridor, nicht dem Gang:**
   Die Längsachse wird senkrecht zur erwarteten Blickrichtung gestellt
   (Portrait bei O–W-Blick, Landscape bei N–S-Blick), auch wenn dadurch der
   Welt-Pfeil aus der Gangachse dreht [alle Beispiele].
6. **„Mittig im Gang" wird präzise umgesetzt:** (B)-West 12 mm neben der
   Gangachse (Breite 1727 mm); (D)-Ost 58 mm (Breite 1270 mm); (A)-Ost
   150 mm (Breite 1520 mm) [4OG-02, 4OG-07, 4OG-03].
7. **„An der Wand" heißt Kante an Wandkante:** (C)-West Zentrum 101 mm von
   Wandkante y=34552; (A)-West Westkante 15 mm von Wandkante x=−76030;
   (C)-Ost zwischen Wandkanten x=−43190/−42795, 1110 mm vor dem
   Stiegenlauf-Ende [4OG-02, 4OG-01, 4OG-06].
8. **Stiegenhauspfeil = Aufwärtsrichtung; Abstieg exakt entgegen:**
   West-Stiege Apexe 0° (oberer Lauf) / 180° (unterer Lauf) = Aufwärtskette,
   DG-Personen Blick 167.9°/257.5°/11.9° (je Δ≈180° zum jeweiligen Lauf);
   Ost-Stiege Apex 0°, Personen Blick 176.98° (Δ=177°) [4OG-02, 4OG-07].
9. **RZ an der Stiegen-Ankunft wird dort platziert, wo der Ankommende
   hinschaut:** (C)-Ost 1110 mm hinter dem Laufende in Gehrichtung, frontale
   Sichtlinie 3342 mm über die ganze Stiege [4OG-06/07]; (C)-West am
   Ankunfts-Podest, Wandmontage statt „mittig zur Stiege" mit Begründung
   Sichtbarkeit beim Hinuntergehen [4OG-02].
10. **Sichtlinien enden an der nächstgelegenen Symbol-KANTE** (nicht am
    Zentrum): z.B. (A)-Ost-Nordkante y=8749, (B)-Ost-Südkante y=4405;
    Längen im 4OG 1006–3342 mm [4OG-02/03/04/06].
11. **Personen-Symbol-Konvention:** Blick = (180°+rot) bei xs>0, rot bei
    xs<0; Fluchtwegpfeil 4444444: Welt = (180°+rot). 17 Personen + 25
    Pfeile konsistent [alle].
12. **Einheitliche RZ-Weltgröße ≈ 640×320 mm** trotz verschiedener
    Block-Skalen (SIBEL xs≈35.6–36.1, RZ-ARR_right xs=1.37).

## Offene Fragen

- h=41221 (freie (A)-Kopie außerhalb des Grundrisses): Absicht unklar —
  vermutlich Arbeitskopie für die Vergleichs-Screenshots S.35/36; im PDF
  nirgends erklärt.
- S.38 „(C) mit Pfeil nach links": Schreibfehler im PDF? DXF-Produkttyp ist
  ARR_right und die S.37-Regel fordert hier „rechts". Owner-Bestätigung wäre
  gut.
- Wandschnitt-Prüfung der Sichtlinien nur visuell (Renders), nicht
  algorithmisch — keine Kreuzung erkennbar, aber ungeprüft.
- „Alternativ mittig zur Stiege" für (C) (S.32): keine DXF-Evidenz, reine
  Textalternative — als Regel-Option offen.
- Gang-Innenkanten für „mittig"-Messungen aus N–S-/O–W-Wandlinien im Umkreis
  abgeleitet; bei (B)-West existiert ein zweiter Kanten-Kandidat x=−75264
  (dann Mitte −76028, Abweichung 88 mm) — beide Lesarten bleiben „mittig".

## Side-by-Side-Bilder

- `4OG-01.png` … `4OG-07.png` (links PDF-Seite, rechts DXF-Crop, 140 dpi)
- `4OG-08-unerklaert.png` (freie (A)-Kopie h=41221)
