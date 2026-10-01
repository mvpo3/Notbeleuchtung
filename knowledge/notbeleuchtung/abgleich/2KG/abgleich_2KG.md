# Parallel-Abgleich PDF ↔ DXF — Mollgasse Notbeleuchtungserklärung, Geschoss 2KG

**Quellen:**
- PDF-Erklärtext Seiten 57–94 (`Notbeleuchtungen zeichnen`, Kapitel „2.KG Notbeleuchtung"; S. 95 leer)
- DXF: `knowledge/Pläne zeichnen Wissen/Mollgasse-Notbeleuchtungserklärung/WHA_MOL_2KG_Notbeleuchtung_Erklärung.dxf` (mm)
- Ground-Truth-Messdaten: `tests/fixtures/mollgasse_gt/2KG.json` (36 Leuchten: 16 down / 15 left / 4 Antipanik / 1 Verteiler; 6 beidseitig-Paare; 79 Personen; 113 Labels)
- Seitenbilder: `S57.png` … `S94.png` (dieser Ordner, pypdfium2 scale=2)

**Konventionen (Phase B, bindend):**
- „Pfeil nach unten/links/rechts" = **Block-Typ** (`RIVO-SIBEL-ARR-down` Basis 270°, `ARR-left` Basis 180°), nie Weltrichtung. Welt-Pfeil = Basis + rot; **xscale<0 spiegelt** (links↔rechts). Alle „Pfeil-nach-rechts"-Leuchten dieses Geschosses sind gespiegelte `ARR-left` (xscale −29,87).
- Positionen = **Bbox-Zentren** (INSERT-Einfügepunkte haben >1-km-Offsets, siehe `insert_xy_mm` im GT).
- Personen-Läufer: Blick = 180°+rot bei xscale>0, sonst rot (Regel #8).
- **Beidseitig** = Doppel-Block: zwei `ARR-left` Rücken an Rücken (Paarabstand 264 mm, Gruppe 4: 318 mm), gegensinnig gespiegelt, gleiche Welt-Pfeilrichtung.
- Erklärungs-Entities: Handles ≥ ~0x1C600; Originalplan kleiner. Farben: grün = Fluchtweg/Labels, cyan (ACI 4) = Sichtlinien (61 explizite Erklär-Linien), gelb (ACI 2) = Konstruktions-/Hilfslinien (7), rot (ACI 1) = Gebäude-Trennlinie `1C7F4` + Stiegenhauspfeile `1CEFD`/`1CF44` + Merktexte, **orange (ACI 30, 0xF26722) = Alternativ-Markierung** (`1D34D` Rechteck + `1D370` Text).
- **Zwei Gebäudehälften mit je eigenem Label-Alphabet:** Mollgasse (A)–(O) und Anastasius-Grün-Gasse (A)–(N) — dieselben Buchstaben kommen doppelt vor!

**Leuchten-Label-Tabelle (alle 36 Notbel-INSERTs + Verteiler):**

*Gebäudehälfte Mollgasse:*
| Label | Handle(s) | Block/Typ | bbox-Zentrum | Welt-Pfeil | Rolle |
|---|---|---|---|---|---|
| (A) | 1C695 | down | −2937, 6579 | 179,6° W | Ausgang ER-L-Gang |
| (B) | 1C707 | Antipanik | −5243, 1380 | — (liegend 746×225) | L-Gang-Schenkel |
| (C) | 1C706 | Antipanik | −3402, 11592 | — (stehend 225×746) | ER-Bereich Nord |
| (D) | 1C64B | down | 234, 7071 | 269,6° S | Durchgang STGH-GANG |
| (E) | 1C644 | down | 889, 5105 | 269,6° S | NIEDERSP.-Tür |
| (F) | 1C647 | down | 4602, 5098 | 269,6° S | Schleusen-Tür |
| (G) | 1C649 | down | 4848, 3098 | 269,6° S | Tür Garage→Schleuse |
| (H) | 1D06D+1D06F | beidseitig (Gr. 5) | ~4716, −301 | 90,4° N | Doppelparker-Gang |
| (I) | 1C7CB | down | 19467, 7618 | 89,6° N | Parkplatzbereich |
| (J) | 1C7CC+1C7CE | beidseitig (Gr. 2) | ~19553, 2475 | 180,4° W | Motorrad-/Pflichtstellplatz 22 |
| (K) | 1C7FB | Antipanik | 13351, −277 | — (liegend) | Doppelparker-Gang |
| (L) | 1C697 | down | 1932, 10499 | 89,6° N | letzte ER Mollgasse |
| (M) | 1C698 | left **gespiegelt** = rechts-Typ | 7263, 8605 | 268,7° S | nach (O), an Wand |
| (N) | 1C7FC | left **gespiegelt** = rechts-Typ | 6206, 7496 | 178,7° W | vor Stiege |
| (O) | 1C66E+1C66F | beidseitig (Gr. 1) | ~780, 9374 | 358,7° O | Richtung Stiege |
| Anlage | 1D10E | Gruppenbatterie-Verteiler | −280, 3467 | rot 88,7° (stehend) | NIEDERSP.-Raum |

*Gebäudehälfte Anastasius-Grün-Gasse:*
| Label | Handle(s) | Block/Typ | bbox-Zentrum | Welt-Pfeil | Rolle |
|---|---|---|---|---|---|
| (A) | 1C7D0 | down | 21275, −3408 | 89,6° N | Garage, neben Kabeltrasse |
| orange Alternative | 1D326+1D327 | beidseitig (Gr. 6) | ~21346, −6228 | 359,8° O | Richtungswechsel (A)→(C), NUR ALTERNATIV |
| (B) | 1C9BD | Antipanik | 21261, −13829 | — (liegend) | Rampenfuß |
| (C) | 1C83E | down | 29847, −6227 | 179,6° W | Garagengang |
| (D) | 1C885+1C886 | beidseitig (Gr. 3) | ~38106, −11196 | 179,8° W | Doppelparker, zeigt zu (E) |
| (E) | 1C861 | down | 34416, −11150 | 359,6° O | Tür→Schleuse |
| (F) | 1C9A0 | down | 38114, −17933 | 269,6° S | Pflichtstellplatz/Doppelparker |
| (G) | 1C97D | down | 39083, −23326 | 269,6° S | nächste Doppelparker |
| (H) | 1C8CC | down | 33368, −12292 | 89,6° N | Schleuse |
| (I) | 1C8A9 | down | 32019, −11163 | 179,6° W | Technikraum-Tür |
| (K) | 1C936+1C937 | beidseitig (Gr. 4) | ~32177, −14236 | 269,8° S | STGH-Gang, Richtung Stiege |
| (L) | 1C8EF | down | 28234, −14222 | 180,1° W | ER-Tür |
| (M) | 1C912 | down | 33397, −16604 | 269,6° S | vor Medienraum |
| (N) | 1C95A | left **gespiegelt** = rechts-Typ | 35033, −18958 | 179,8° W | vor Aufzug |

Achtung: Label „(A)" existiert doppelt in der Anastasius-Hälfte (`1D157` @ 15985/−3192 **ohne** Leuchte in der Nähe + `1D17A` @ 21602/−3335 an `1C7D0`) — siehe Offene Punkte.

---

## 2KG-01 — Einlagerungsräume + gespiegelter L-förmiger Gang, Antipanik (B) (PDF S. 57–58, 61)

**PDF:** Mehrere ER + zusammenhängender, **gespiegelt L-förmiger** Gang, nicht durch Tür getrennt → **keine zusätzlichen Richtungsleuchten** im Gangverlauf („benötigen wir innerhalb dieses Gangverlaufs nicht an jeder Stelle zusätzliche Notleuchten zur Richtungsangabe"). Die L-Form schattet einen Gangteil ab → **Antipanikleuchte (B) mittig** in diesem Gangbereich; **gelbe diagonale Linie** visualisiert die Mitte. „Die Antipanikleuchte wurde außerdem **vertikal ausgerichtet**." Aufgabe: kein Pfeil, sondern Dunkelstellen verhindern. S. 61 Vergleichsregel (hypothetisch): **wäre** dort eine Wand mit Tür, müsste ein Tür-RZ (Pfeil nach unten) + nach der Tür ein Folge-RZ (rechts oder links, je nach Verlauf) platziert werden — hier NICHT NOTWENDIG.

**DXF:** (B) = `1C707` Antipanikleuchte @ (−5243, 1380), rot 178,74°, **Bbox 746×225 mm = LIEGEND/horizontal**. Gelbe Diagonale `1D03D` (−7563, 2165)→(−2856, 591), Länge 4963 mm; (B)-Zentrum liegt **9 mm** neben der Linie (auf halber Strecke, t≈0,49 → „mittig" bestätigt). ER-Stempel `1B3ED` ER 04 / `1B216` ER 05 (Nordzeile) vs. `1B3D1`/`1B21C`/`1B3CB` ER 01–03 (Südzeile); der L-Gang verbindet beide Zeilen. Keine weitere Richtungsleuchte zwischen (B) und (A) ✓. Personen-Schwarm „(2KG)" (u. a. `1C63F`, `1CA3A`, `1CA3C` Blick 12,3° O) aus den ER.

**Status: Widerspruch (nur Orientierungs-Aussage)** — Mittigkeit + Diagonale + „keine Richtungsleuchten" bestätigt (mm-genau); aber PDF-Text „vertikal ausgerichtet" widerspricht DXF **und** PDF-Bild: (B) liegt horizontal (746×225). Vertikal steht stattdessen die Mollgasse-Antipanik **(C)** `1C706` (225×746) — vermutlich Verwechslung im Text.

Bilder: `S57.png`, `S58.png`, `S61.png`

## 2KG-02 — Weitere ER + Antipanikleuchte (C) (PDF S. 59–60)

**PDF:** Bei den nächsten ER wurde Antipanik (C) platziert. Modalität wörtlich: „Grundsätzlich **müssen** wir an dieser Stelle **nicht zwingend** eine zusätzliche Antipanikleuchte platzieren. Um jedoch die benötigte **Beleuchtungsstärke in Lux** besser zu erreichen und … möglichst keine Stelle … vollständig dunkel bleibt, ist es **sinnvoll**…" → SINNVOLL, kein MUSS. Position über **gelbe Diagonale** „von der Kante der Mauer bis zur Ecke des Ganges bei ER 12".

**DXF:** (C) = `1C706` @ (−3402, 11592), rot 268,74° → **stehend** (225×746). Gelbe Diagonale `1D045` (−2775, 9530)→(−4005, 13613), Länge 4264 mm; (C)-Zentrum **20 mm** neben der Linie bei t≈0,51 → mittige Diagonal-Konstruktion bestätigt. ER-12-Stempel `1B162` @ (−5247, 13315) = Nordwest-Ecke des Bereichs, passt zum Diagonalen-Endpunkt. Status: **bestätigt** (+ Maße; Modalität SINNVOLL sauber vom MUSS getrennt).

Bilder: `S59.png`, `S60.png`

## 2KG-03 — Ausgang des ER-Gangs, Notleuchte (A) Mollgasse (PDF S. 60–61)

**PDF:** Am Ausgang des Gangbereichs die Notleuchte (A) „mit Pfeil nach unten", so gedreht, dass „der **lange weiße Balken im unteren Bereich** der Notleuchte **in Richtung der Menschen** zeigt" → frontale Erkennbarkeit.

**DXF:** (A) = `1C695` ARR-down @ (−2937, 6579), rot 269,58° → **Welt-Pfeil 179,58° W**; Symbol stehend (Bbox 292×577), Frontseite nach Osten zum Gang = Richtung der von Norden/Osten ankommenden ER-Personen. 2 Sichtlinien (1155/2272 mm) enden an (A). Danach Tür → (D): Abstand (A)→(D) 3209 mm (2KG-09). Status: **bestätigt** — „Pfeil nach unten" = Blocktyp, Weltrichtung West; Balken-Frontal-Logik konsistent mit Personen-Blickrichtungen (`1CA40` u. a. Blick 12,3°).

Bild: `S60.png`

## 2KG-04 — Letzte ER der Mollgasse, nur eine Notleuchte (L) (PDF S. 62)

**PDF:** Kurzer Gang; **nur eine** Tür-Notleuchte (L). Alle „2KG"-Menschen haben beim Verlassen der ER **direkten Blick** auf (L) → „benötigen wir … **keine weitere zusätzliche Notleuchte** zur Orientierung."

**DXF:** (L) = `1C697` ARR-down @ (1932, 10499), rot 179,58° → Welt-Pfeil 89,58° N (in den Raum/zur Tür, entgegen der Fluchtrichtung Süd). GANG-Stempel `1B299` @ (4356, 11066); ER 15/16/17-Stempel flankieren. Sichtlinie 1397 mm an (L); keine weitere Leuchte im Gang ✓. Von (L) weiter: (L)→(O) nur 1707 mm (Anschluss an die STGH-Kette, 2KG-10). Status: **bestätigt**.

Bild: `S62.png`

## 2KG-05 — Parkplatzbereich Mollgasse, Notleuchte (I) + KABELTRASSEN-REGEL (PDF S. 63–64)

**PDF:** (I) mit Pfeil nach unten; Parker sehen (I) direkt (türkise Blickwinkel-Linien); weißer Balken Richtung Menschen; „Der **Pfeil** der Notleuchte (I) zeigt **entgegen der tatsächlichen Richtung des Fluchtwegs**." Dann die Kabeltrassen-Regel, wörtlich (S. 63–64):
> „Wichtig ist in diesem Beispiel zusätzlich, dass sich im Parkplatzbereich **Kabeltrassen** befinden. Diese sind im Plan als **blaue Balken** dargestellt und beispielsweise mit **KT300, KT400 oder KT500** beschriftet. … **Eine Notleuchte darf niemals direkt innerhalb beziehungsweise auf dem Bereich einer Kabeltrasse platziert werden.** Die Notleuchte muss **seitlich neben der Kabeltrasse** positioniert werden … **Als Platzierungsregel verwenden wir hier möglichst einen Abstand von mindestens 450 mm zur Kabeltrasse.**"
Platzierungslogik 5 Schritte: 1. Fluchtweg-Position bestimmen → 2. Kabeltrassen-Kollision prüfen → 3. seitlich versetzen → 4. „Dabei **soll möglichst** ein Abstand von **mindestens 450 mm** eingehalten werden" → 5. „Trotz der Verschiebung müssen **Sichtbarkeit, Pfeilrichtung und frontale Ausrichtung** … weiterhin korrekt bleiben." → Modalität: SOLL/„möglichst", Schritt 1+5 = MUSS-Rahmen.

**DXF:** (I) = `1C7CB` ARR-down @ (19467, 7618), rot 179,58° → Welt-Pfeil 89,58° N = entgegen der Fluchtrichtung Süd ✓ (Fluchtweg führt südwärts zu (J), Abstand (I)→(J) 5012 mm). Bild S. 63 zeigt 4 türkise Sichtlinien von den Parker-Personen zu (I). **Kabeltrassen-Befund:** Die 2KG-Trassen-Beschriftung lautet 7× „**KT UK=+2,11 FBOK**" (`10100`, `1012B`, `1012D`, `1012F`, `10131`, `10133`, `10135`) — die im PDF genannten KT300/KT400/KT500-Labels stehen so NICHT in dieser DXF (generische Beispiel-Nennung). Die Trassen-Grafik verteilt sich im Originalplan auf eine geroutete Trassen-Polyline `1B502` (Layer `07_SYM-G00-LKG-HLP`, 10 Vertices durch die Mollgasse-Garage, z. B. (−6074,2007)→(17648,2766)→(18339,1081)) + Kantenlinien auf `02-HID-G00-LKG-M0` (verdeckt = Deckenmontage; Band `1B528`/`1B1B4` im Garagengang, y≈1675–2183). **Wichtige Abgrenzung:** Die vertikalen blauen „Leiter"-Bänder mit Schraffur (Layer `02-ANS-G00-Lkg-Rigol`, 300 mm Kanten `1B905`/`1B907`) sind **Boden-Rigole (Entwässerungsrinnen)**, KEINE Kabeltrassen — (I) und (J) stehen mittig AUF so einer Rigole (Deckenleuchte über Bodenrinne = kein Konflikt). Antipanik (K) hält 2,4 m Abstand zum Deckentrassen-Band. Eine mm-genaue 450-Nachmessung an (I)/(J) scheitert an der mehrdeutigen Balken-Zuordnung → Offener Punkt 2.

**Status: präzisiert** — Regel + Modalität wörtlich gesichert; DXF-Beschriftung abweichend („KT UK=+2,11 FBOK"); Rigole ≠ Kabeltrasse als neue, geometrisch belegte Unterscheidung.

Bilder: `S63.png`, `S64.png`

## 2KG-06 — Beidseitige Notleuchte (J): Motorrad-Parkplätze + Pflichtstellplatz 22 (PDF S. 65–67)

**PDF:** (J) = **beidseitige** Notleuchte, „Pfeile … **nach links** … in Richtung der **Motorrad-Parkplätze**". Zwei Ankunftsströme: (a) Menschen direkt von den Doppelparkern (sehen (J) auf den ersten Blick), (b) Menschen, die vorher (I) gefolgt sind. WARUM beidseitig (S. 66): „weil Menschen aus **beiden Richtungen** auf diese Notleuchte zuflüchten können. Der Vorteil … ist, dass die Menschen die Notleuchte **von beiden Seiten frontal** sehen können. Auf **beiden Seiten** ist der **lange weiße Balken** … so ausgerichtet, dass er in Richtung der jeweiligen Personen zeigt." Zusätzlich Kabeltrassen-Beachtung.

**DXF:** (J) = Gruppe 2: `1C7CC` (rot 180,36°, xscale −29,87) + `1C7CE` (rot 0,36°, xscale +29,87), Zentren (19552, 2607)/(19554, 2343), Paarabstand 264 mm, **beide Welt-Pfeil 180,4° W** = Richtung Motorrad-Stellplätze (MOTORRAD-Stempel `1B5A7` @ 11610/2725 und `1B5AD` @ 14056/2731, westlich) ✓. Sichtlinie 4423 mm an beide Blockhälften (= Blick vom Pflichtstellplatz 22, Stempel `1B589` @ 24787/688 östlich). Kette: (I)→(J) 5012 mm. Das Paar steht neben/über der Rigole (siehe 2KG-05); das Decken-KT-Band verläuft südlich (Kantenlinien `1B528`/`1B1B4`). Status: **bestätigt** — PFLICHT-beidseitig-Fall (zwei Ströme, beide brauchen Frontsicht); „nach links" = Welt-West hier deckungsgleich mit Blocktyp.

Bilder: `S65.png`, `S66.png`, `S67.png`

## 2KG-07 — Doppelparker: Antipanik (K) + beidseitige Notleuchte (H) (PDF S. 67–68)

**PDF:** Zwei mögliche Fluchtwege (über Motorrad-Parkplätze ODER über den Bereich der Antipanik (K)). (K)-Position per **gelben Linien** bestimmt: „**in einer Linie mit der Notleuchte (H)** … und **mittig zur Wand** beziehungsweise zum dargestellten Bereich". Zweck: Lux + keine Dunkelbereiche. (H) = beidseitig, „**mittig im Bereich der Doppelparker**", Pfeile auf den nächsten Ausgang/weiteren Fluchtweg; Menschen von (J) laufen an (K) vorbei und sehen dann (H); von der anderen Seite (Doppelparker links) sehen Menschen (H) auf den ersten Blick.

**DXF:** (K) = `1C7FB` Antipanik @ (13351, −277), liegend, rot 0. Gelbe Linien: `1D099` (13350, −266)→(4990, −318) = die „in-einer-Linie"-Konstruktion zu (H): (K) sitzt exakt am Linienstart, (H)-Paar @ (~4716, −301) liegt **17–24 mm** neben der Verlängerung → „in einer Linie" mm-genau bestätigt. `1D097` (10503, 1601)→…→(13359, −2928) (4 Vertices, 13056 mm) = Mittigkeit-zur-Wand-Konstruktion. (H) = Gruppe 5: `1D06D`/`1D06F` (rot 90,36°/270,36°, xscale ∓), Zentren (4848, −300)/(4584, −302), **Welt-Pfeil 90,4° N** = zum Ausgang/zur Tür bei (G) (Δ zu (G): 132 mm Ost, 3399 mm Nord → praktisch exakt Nord) ✓. Kette: (J)→(K) 6839 mm, (K)→(H) 8504 mm. Status: **bestätigt** (+ Konstruktionslinien gemessen).

Bilder: `S67.png`, `S68.png`

## 2KG-08 — Fluchtweg DURCH die Motorrad-Parkplätze: (H)→(G)→(F), Doppelparkergrube (PDF S. 69–70)

**PDF:** Menschen von den Doppelparkern **durchqueren** die Motorrad-Parkplätze („Dieser Bereich ist offen und kann … einfach durchquert werden"), sehen dann (G) an der Tür. Kernunterscheidung (S. 66/69): „Bei **Doppelparkern und großen PKW-Parkbereichen** in Untergeschoßen ergibt sich **nur sehr selten** ein geeigneter Bereich, durch den ein Fluchtweg sinnvoll weitergeführt werden kann. Bei **Motorrad-Parkplätzen** ist das anders … ausreichend freier Platz". (G) an der Tür, Balken frontal, Pfeil entgegen Fluchtweg. Abfolge (H)→(G)→Tür; von (H) aus ist (G) bereits sichtbar. Nach der Tür: **Schleuse** mit (F) an der nächsten Tür, gleiche Regeln. Zusatz (S. 70): Menschen von der **Doppelparkergrube** sehen (G) auf den ersten Blick (türkise Blickwinkel-Linie) → dort ist **„nicht notwendig"** eine weitere zeigende Notleuchte.

**DXF (Geometrie-Beleg Durchquerbarkeit):** Die Personenreihe `1CBF6`(17286, 2403) → `1CBF8`(15308, 2444) → `1CBFA`(11608, 2363) → `1CBFC`(7606, 2305), alle Blick 176,1° W, läuft mit dem grünen Fluchtweg **exakt durch die MOTORRAD-Stempelzone** (`1B5A7` @ 11610/2725, `1B5AD` @ 14056/2731 — gleiche x-Spanne, 300–400 mm daneben). Die DOPPELPARKER-Zonen (Stempel `1B3A4` Pflichtstellplatz 30-31 @ 12652/4678, Gruben `1B2A7` @ 8905/4607, `1B2AD` @ −527/−1609) werden von **keiner** Fluchtweg-Polyline und keiner Personenreihe gequert — der zweite Strom läuft südlich um sie herum (y≈−300, Reihe `1CC00`/`1CC02`/`1CC04` Blick 176°). (G) = `1C649` @ (4848, 3098), Welt-Pfeil 269,6° S = entgegen Flucht N; 3 Sichtlinien (1822–4072 mm) enden an (G), die längste = Doppelparkergrube-Blick. (F) = `1C647` @ (4602, 5098) in der SCHLEUSE (`1B148` @ 4240/4476), Welt-Pfeil S; (G)→(F) 2015 mm. Status: **bestätigt** — Durchquerbarkeits-Unterscheidung geometrisch belegt.

Bilder: `S69.png`, `S70.png`

## 2KG-09 — Schleuse, Niederspannungsraum, AR: Notleuchten (D), (E) + Anlagensymbol (PDF S. 71–74)

**PDF:** Vier Personengruppen (Garage, Niederspannungsraum, ER, AR) → alle zum Stiegenhaus Richtung 1KG. (D) mit Pfeil nach unten am **offenen Durchgang zum Stiegenhaus (keine Tür!)**, **mittig im Durchgang** (gelbe Linien). WARUM Typ „unten" statt links/rechts/beidseitig (S. 73): rechts/links → manche sähen sie „**nur seitlich und nicht frontal**"; beidseitig „wäre jedoch ebenfalls ungünstiger" (der NS-Raum-Mensch sähe sie nicht so unmittelbar frontal) → ALTERNATIVE ERWOGEN UND VERWORFEN. **Niederspannungsraum**: Stromversorgung des Gebäudes + der Notbeleuchtung; „die Stromversorgung der Notbeleuchtung darf … **nicht an derselben Wand** beziehungsweise innerhalb des Bereichs der **blau dargestellten E-Verteiler** platziert werden." (E) mit Pfeil nach unten an der NS-Raum-Tür. **AR/Abstellraum: „muss … nicht unbedingt eine eigene Notleuchte"** (klein, ein Ausgang, wenig genutzt) — der Technikraum dagegen bekommt wegen der wichtigeren technischen Nutzung/Gefährdung eine Tür-Notleuchte. **Allgemeine Platzierungslogik (S. 74):** „Bei einem **Richtungswechsel** des Fluchtwegs, bei einem **weiteren Ausgang** oder an einer Stelle, an der der weitere Verlauf … erkannt werden muss, **soll** eine … Notleuchte sichtbar sein. Auch beim **Verlassen eines Raumes oder einer Wohnung** soll eine Person grundsätzlich eine Notleuchte sehen können…" Ausnahme: Obergeschoße mit nur einem Stiegenhaus + eindeutigem I-Gang → „meistens keine zusätzliche Richtungsleuchte"; Schwerpunkt EG + UGs.

**DXF:** (D) = `1C64B` @ (234, 7071), Welt-Pfeil 269,6° S. Gelbe Linie `1D110` (−387, 7208)→(863, 7202) = Durchgangsbreite 1250 mm; (D)-x = 234 vs. Linienmitte 238 → **mittig auf 4 mm** ✓. Kein Türsymbol im Durchgang (STGH-GANG-Stempel `1B1AE` @ 1259/6512) ✓ „keine Tür". Sichtbarkeit aus allen 4 Richtungen: (A)→(D) 3209 mm, (E)→(D) 2072 mm, (F)→(D) 4793 mm, AR-Stempel `1B1CA` @ (−214, 4428). (E) = `1C644` @ (889, 5105), Welt S, an der NIEDERSP.-Tür (`1B190` @ 2640/4484). **Anlagensymbol** `1D10E` Gruppenbatterie-Verteiler @ (−280, 3467), stehend (rot 88,7°) an der Westwand des NS-Raums, mit grünem Merktext `1D10F` „Notbeleuchtungs, Stromversorgung aller Notleuchten im Gebäude" @ (1478, 3501) — abgesetzt von den blauen E-Verteiler-Bändern der Süd-/Ostwand (Originalplan; Text `1C048` „KANALLEITUNGEN … IN NIEDERSP.R."). Status: **bestätigt** (+ Mittigkeit 4 mm; Anti-Beispiele als bewusst verworfene Alternativen protokolliert).

Bilder: `S71.png`, `S72.png`, `S73.png`, `S74.png`

## 2KG-10 — Kette (D)→(O)→(M)→(N)→Stiege→1KG (PDF S. 74–76)

**PDF:** Nach (D) sehen die Menschen (O) = **beidseitig**, Pfeile Richtung **Stiege**; beidseitig, weil Menschen sich „von **unterschiedlichen Seiten** nähern" — zusätzlich kommen die ER-Menschen von (L). Generalisierte Logik wörtlich (S. 75): „**Wenn Menschen aus zwei unterschiedlichen Richtungen auf eine gemeinsame Notleuchte zulaufen, kann eine beidseitige Notleuchte sinnvoll sein**, damit beide Personengruppen die Notleuchte frontal sehen können." Danach (M) „mit Pfeil nach rechts", **mittig an der Wand**, türkise Blickwinkel-Linie; dann (N) „mit Pfeil nach rechts"; ab (N) zur Stiege → 1KG. Personen „(2KG) Richtung 1KG". Fluchtweg-Zusammenfassung: Schleuse/NS-Raum/ER → (D) → (O) → (M) → (N) → Stiege → 1KG.

**DXF:** (O) = Gruppe 1 `1C66E`/`1C66F` @ (777, 9242)/(783, 9506), Welt-Pfeil 358,7° **O** = zur Stiege (Stiegenhauspfeil-Zone x 1419–5871). Zulauf-Distanzen: (D)→(O) 2238 mm, (L)→(O) 1707 mm ✓ zwei Ströme. (M) = `1C698` **ARR-left xscale −29,87 = „Pfeil nach rechts"-Typ** (PDF-Sprache = Blocktyp!), rot 268,74° → Welt-Pfeil 268,7° S; steht an der Wand beim PODEST (`1B293` @ 6370/8057); Sichtlinie 1821 mm. (N) = `1C7FC`, ebenfalls gespiegelter left = rechts-Typ, Welt-Pfeil 178,7° W Richtung Stiege; (M)→(N) 1533 mm. **Stiegenhauspfeil rot nachgezeichnet** `1CEFD` (5871, 7984)→Spitze (1419, 8020) = **Pfeil nach West**; Personen „richtung 1KG" (`1CAEE`/`1CAF0`, Blick 169,9° ≈ W) laufen **in Pfeilrichtung** hinauf ✓ (UG-Regel, rote Merktexte `1CEFC`/`1CF20` „Stiegenhauspfeilrichtung"). Label `1CAF1` „(2KG)richtung 1KG". Status: **bestätigt** (+ alle Kettenmaße).

Bilder: `S74.png`, `S75.png`, `S76.png`

## 2KG-11 — ZWEI GEBÄUDEHÄLFTEN: Mollgasse / Anastasius-Grün-Gasse, rote Trennlinie + EG-Referenz (PDF S. 76–78)

**PDF:** „Das Projekt besteht aus **zwei Gebäuden**, die sich einen gemeinsamen Bereich im Untergeschoß beziehungsweise in der Garage teilen." Rote Linie = Abgrenzung. Konstruktion wörtlich (S. 77): „Als Trennlinie verwenden wir die **Gebäudewand der Mollgasse**. Auf dieser Wand habe ich im Bild die rote Linie eingezeichnet und diese Linie **über das Projekt weitergeführt**." Erkennung der Zuordnung: „am einfachsten, **nicht nur das Untergeschoß selbst zu betrachten**, sondern zusätzlich den **Grundriss des Erdgeschoßes (EG)** heranzuziehen" (S. 77-Bild = EG-DXF-Tab mit grünen FREIHEIT- / rotem KEINE-FREIHEIT-Rahmen). Folgen: zwei Fluchtwegführungen; die Aufteilung beeinflusst „die **Richtung des Fluchtwegs**, die **Pfeilrichtung** der Notleuchten, die **Rotation** der Notleuchten und die Frage, welchem der beiden Gebäude ein Bereich zugeordnet wird." **Prozessregel (S. 78, bindend):** Wenn die Zuordnung/Richtung „**nicht eindeutig erkennbar ist … darf diese Zuordnung nicht eigenständig geraten werden**. In diesem Fall soll die Stelle als **offene Frage** behandelt und gemeinsam detaillierter geklärt werden."

**DXF:** Rote Trennlinie = `1C7F4` (ACI 1), (−22184, −3052)→(94106, −2648), **Länge 116,3 m** — quer über das gesamte Blatt, quasi-horizontal (Steigung 0,2°), auf der Mollgasse-Südwand. Roter Merktext `1C7F5` @ (79085, 603), wörtlich: „**Hier teilt sich der Fluchtweg weil wir zwei Gebäude habe / die einen Fluchtweg bieten, und deshalb teilen wir das in der mitte / Eine Gebäude Hälfte (Mollgasse in dem Fall) und andere Gebäudehälfte (Anastasius-Grüngasse)**". Alle Mollgasse-Leuchten liegen nördlich (y > −2900), alle Anastasius-Leuchten südlich; jede Hälfte hat ihr eigenes Label-Alphabet (siehe Tabelle). Die FREIHEIT/KEINE-FREIHEIT-Rahmen des S.77-Bilds liegen in der **EG**-Erklärungs-DXF (dort Handles `209DC`ff., vgl. EG-Abgleich Offene Frage 6), nicht in der 2KG-Datei. Status: **bestätigt** (Trennlinie + Merktext wörtlich; EG-Referenz als datei-übergreifende Verweistechnik präzisiert).

Bilder: `S76.png`, `S77.png`, `S78.png`

## 2KG-12 — Anastasius: Notleuchte (A), Kabeltrasse, Richtungswechsel + orange Alternative (PDF S. 79–81)

**PDF:** (A) mit Pfeil nach unten, „Pfeil **entgegen der tatsächlichen Richtung** des Fluchtwegs". Kabeltrasse: (A) „mit entsprechendem Abstand **neben der Kabeltrasse**"; NEU: „Zusätzlich muss darauf geachtet werden, dass die Notleuchte (A) **auf der Seite der Anastasius-Grün-Gasse bleibt** und durch die Verschiebung wegen der Kabeltrasse **nicht der anderen Gebäudehälfte zugeordnet wird**." Richtungswechsel: der Mensch von (A) geht geradeaus, dann setzt sich der Fluchtweg „**nach rechts** in Richtung der Notleuchte (C)" fort; ohne Zusatzleuchte würde er (C) beim Links-Rechts-Schauen ohnehin erkennen. **Alternative beidseitige Notleuchte orange markiert**: „eine **alternative beziehungsweise zusätzliche** Position. Sie ist **nicht zwingend erforderlich**, weil die Notleuchte (C) grundsätzlich sichtbar ist. **Ich würde sie hier jedoch trotzdem platzieren**, weil sie den **Richtungswechsel … eindeutiger macht**." Allgemeine Logik: „Bei einem Richtungswechsel des Fluchtwegs ist es **sinnvoll**, direkt an diesem Richtungswechsel eine Notleuchte zu platzieren." Beidseitig, weil sich Menschen dem Punkt „von zwei unterschiedlichen Seiten nähern".

**DXF:** (A) = `1C7D0` ARR-down @ (21275, −3408), rot 179,58° → Welt-Pfeil 89,6° N (Flucht führt südwärts die RAMPE hinab, Stempel `1B121` @ 21181/−4317) ✓. KT-Text `1012B` „KT UK=+2,11 FBOK" @ (21284, −2631) direkt nördlich. **Gebäudehälften-Beleg:** (A)-Zentrum liegt **507 mm südlich** der roten Trennlinie (Trennlinien-y bei x=21275: −2901) → knapp, aber eindeutig auf der Anastasius-Seite ✓. **Orange Alternative** = Gruppe 6: `1D326`/`1D327` @ (21346, −6360)/(21347, −6096), Welt-Pfeil 359,8° **O** = Richtung (C); eingerahmt vom **orangen Rechteck `1D34D`** (777×672 mm, ACI 30) + orangem Text `1D370` „**alternativ muss nicht sein, aber es schadet nicht**" @ (20777, −5703). Ketten: (A)→Alternative 2953 mm, Alternative→(C) 8502 mm; 2 Sichtlinien (1094/2069 mm) am Paar. Personenströme: `1D396` (21057, −2366) Blick 282° (südwärts von (A)) und `1D34B` (21395, −8571) Blick 102° (nordwärts von der Rampe) = die „zwei Seiten" ✓.
**Richtungs-Anmerkung:** Für den von (A) kommenden (südwärts laufenden) Menschen ist die Ost-Abzweigung zu (C) geometrisch eine **Links**-Drehung; „nach rechts" stimmt nur in Plan-Leserichtung bzw. für den von der Rampe (Süden) kommenden Strom → Formulierung personenbezogen nicht konsistent.

**Status: präzisiert** — Kabeltrassen-Ausweich + Hälften-Bindung + Alternative (SINNVOLL/EMPFOHLEN: „würde sie trotzdem platzieren") voll belegt; „nach rechts"-Formulierung vs. Geometrie als Vorsicht dokumentiert (Offener Punkt 3).

Bilder: `S79.png`, `S80.png`, `S81.png`

## 2KG-13 — Antipanik (B) Anastasius + beidseitige Alternative NUR OPTIONAL (PDF S. 82–83)

**PDF:** Erneut der Bereich der (jetzt Anastasius-) Antipanik (B); dieselbe orange beidseitige Notleuchte wird hier aus der Gegenrichtung erklärt. Modalität wörtlich: „Diese zusätzliche beidseitige Notleuchte ist hier jedoch **kein Muss**. Der Grund … ist, dass die Menschen, die aus dem Bereich der Antipanikleuchte (B) kommen, von dort aus **nur in eine mögliche Richtung weiterflüchten können**. … Die beidseitige Notleuchte ist in diesem Beispiel **lediglich dargestellt, um zu zeigen, warum und an welcher Position man sie zusätzlich platzieren könnte**, wenn man die Orientierung … noch eindeutiger machen möchte." (B)-Aufgabe: Bereich beleuchten (sehr dunkel ohne sie), Orientierung, Lux-Beitrag.

**DXF:** (B) = `1C9BD` Antipanik @ (21261, −13829), liegend (742×209), am Fuß der Garagenrampe (`1B155` RAMPE @ 21180/−14602, `1B329` GARAGENRAMPE @ 21120/−17296). Distanz (B)→orange Alternative = **7470 mm** die Rampe hinauf; es ist **dasselbe** orange Paar `1D326`/`1D327` wie in 2KG-12 (nur EIN oranges Rechteck `1D34D` in der ganzen DXF) — die S.80- und S.82/83-Erklärungen beschreiben dieselbe Position aus zwei Personenströmen. **Modalitäts-Kontrast sauber halten:** S. 80 = „nicht zwingend, ich würde sie trotzdem platzieren" (EMPFEHLUNG), S. 82/83 = „kein Muss … lediglich dargestellt" (reine ALTERNATIVE/Demo) — beidseitig-PFLICHT-Fälle wie (J)/(H)/(D)/(K)/(O) sind davon strikt zu unterscheiden. Status: **bestätigt** (Modalität + Identität des Paars geometrisch geklärt).

Bilder: `S82.png`, `S83.png`

## 2KG-14 — Anforderung Lichtberechnung + Hauptengine (PDF S. 83–84)

**PDF (wörtlich, Owner-Auftrag an die Engine):** „Für die weitere Entwicklung ist wichtig, dass **alle bisher bearbeiteten Stockwerke vollständig mit der Lichtberechnung überprüft werden**. Dabei sollen insbesondere **alle von uns platzierten Elemente** berücksichtigt werden: Rettungszeichen-/Notleuchten, Antipanikleuchten, Aufheller. Für jeden bearbeiteten Bereich soll die Lichtberechnung prüfen, ob die von uns gewählte Platzierung tatsächlich eine **ausreichende Beleuchtung beziehungsweise die erforderlichen Lux-Werte** erreicht. Diese Überprüfung soll **nicht nur für dieses Beispiel im 2KG** durchgeführt werden, sondern **für alle Stockwerke und alle bisher von uns beschriebenen Bereiche**." Zweck (4 Punkte): 1. ob manuelle Platzierungen lichttechnisch funktionieren, 2. ob zusätzliche Antipanik/Aufheller nötig, 3. ob einzelne Leuchten entfallen können, 4. „ob die vorhandene **Lichtberechnung der Software zuverlässig genug ist**, um solche Entscheidungen zukünftig **automatisch** zu treffen." Abschluss S. 84: „Die bisher erklärten Platzierungen bilden damit die **fachliche Platzierungslogik**. Die Lichtberechnung soll anschließend als **zusätzliche Prüfung** feststellen, ob die Beleuchtungsstärke … tatsächlich ausreichend ist."

**DXF:** Kein Geometrie-Gegenstück (reine Prozess-/Engine-Anforderung). Status: **bestätigt** (wörtlich protokolliert; maps auf Task G3 „Lux auf Experten-Placement" + `render/lux_nachweis_bericht`).

Bilder: `S83.png`, `S84.png`

## 2KG-15 — Anastasius-Kette (C)→(D)→(E)→(H) + Technikraum (I), Kabeltrassen-Wiederholung (PDF S. 84–86)

**PDF:** Nach (C) geradeaus → (D) = **beidseitig**, Pfeile Richtung (E); die Doppelparker-Flüchtenden sehen (D) auf den ersten Blick (türkise Blickwinkel-Linien). Kabeltrasse: „darf die Notleuchte **nicht auf beziehungsweise innerhalb einer Kabeltrasse** platziert werden. Die Position der Notleuchte (D) muss deshalb so gewählt werden, dass sie **nicht mit einer Kabeltrasse kollidiert**, die Menschen sie weiterhin **frontal** erkennen … und ihre Pfeile weiterhin **korrekt** den nächsten Abschnitt … anzeigen." Kette (C)→(D)→(E); (E) mit Pfeil nach unten **bei der Tür**; danach Schleuse mit (H) (Pfeil nach unten, bei einer Tür). **Technikraum** mit (I) mit Pfeil nach unten; der Mensch aus dem Technikraum gelangt ebenfalls in die Schleuse und sieht dort (H).

**DXF:** (C) = `1C83E` @ (29847, −6227), Welt-Pfeil 179,6° W; Sichtlinie 7250 mm (längste des Geschosses — Doppelparker-Blick). (D) = Gruppe 3 `1C885`/`1C886` @ (38106, −11064)/(38106, −11327), **Welt-Pfeil 179,8° W = exakt Richtung (E)** (`1C861` @ 34416/−11150, 3691 mm westlich) ✓; **5 Sichtlinien** (1445–5939 mm) enden am (D)-Paar = die türkisen Blickwinkel der Doppelparker-Personen (`1CC9C`/`1CC9E`/`1CCA0`, Blick 181,7°) ✓. Kabeltrassen-Kontext: KT-Text `1012F` @ (37421, −8011) mit vertikalem Rigol-/Bandzug `1B2A1`/`1B8F8` x≈37960–38260 nördlich; das (D)-Paar steht südlich davon frei. (E) Welt-Pfeil 359,6° O = entgegen der Fluchtrichtung W ✓, an der Tür zur Schleuse (`1B14E` SCHLEUSE @ 33218/−10796); (E)→(H) 1550 mm; (H) = `1C8CC` @ (33368, −12292), Welt-Pfeil 89,6° N (entgegen Flucht S) ✓. (I) = `1C8A9` @ (32019, −11163), Welt-Pfeil 179,6° W = ins Rauminnere des TECHNIKRAUM (`1B3BA` @ 30311/−9996), Sichtlinie 452 mm, (I)→(H) 1760 mm ✓. Status: **bestätigt** (+ alle Maße; KT-MUSS-Formulierung („darf nicht") vs. 450-mm-SOLL sauber getrennt).

Bilder: `S84.png`, `S85.png`, `S86.png`

## 2KG-16 — Nächste Doppelparker, Notleuchte (G) Anastasius (PDF S. 86–87)

**PDF:** (G) mit Pfeil nach unten bei den nächsten Doppelparkern; Rotationsregel: Pfeil entgegen dem tatsächlichen Fluchtweg, weißer Balken Richtung Menschen (frontal); wer (G) sieht, folgt dem Fluchtweg geradeaus weiter.

**DXF:** (G) = `1C97D` ARR-down @ (39083, −23326), rot 359,58° → Welt-Pfeil 269,6° S = entgegen der Fluchtrichtung N ✓. **3 Sichtlinien** (1428 / 5118 / 5762 mm) von den Doppelparker-Personen (`1CCA4`/`1CCA6`/`1CCA8`, Blick 166,6°; Stempel `1B31D`/`1B323` PFLICHTSTELLPLATZ 13–20 @ y≈−30463). Kette: (G)→(F) 5480 mm. Status: **bestätigt**.

Bilder: `S86.png`, `S87.png`

## 2KG-17 — Pflichtstellplatz + Doppelparker → (F), dann (F)→(D)→(E)→(H) (PDF S. 87–89)

**PDF:** Zwei Gruppen (vom Pflichtstellplatz links, von den Doppelparkern über (G)) sehen als Nächstes (F) mit Pfeil nach unten → geradeaus. Wieder Kabeltrassen-Regel („nicht auf beziehungsweise innerhalb… so positioniert …, dass die Kabeltrasse nicht beeinträchtigt wird und die Menschen die Notleuchte weiterhin gut erkennen"). Ab (F): „Genau aus diesem Grund wurde die Notleuchte (D) **beidseitig** ausgeführt: **Nicht nur** die Menschen, die von der Notleuchte (F) kommen … **Auch von der anderen Seite** kommen Menschen auf die Notleuchte (D) zu." Abfolge wörtlich: **(F) → (D) → (E) → Tür → Schleuse → (H) → nächste Tür.**

**DXF:** (F) = `1C9A0` ARR-down @ (38114, −17933), rot 359,58° → Welt-Pfeil 269,6° S = entgegen Flucht N ✓; 2 Sichtlinien (3564/4537 mm); KT-Text `10133` @ (38037, −16927) direkt nördlich — (F) steht seitlich der Trassenachse. Kette gemessen: (F)→(D) 6869 mm, (D)→(E) 3691, (E)→(H) 1550. Das (D)-Paar bedient damit **zwei Zuläufe** ((C)-Strom von W: 9572 mm Sichtkette; (F)-Strom von S) → PFLICHT-beidseitig ✓. Status: **bestätigt**.

Bilder: `S87.png`, `S88.png`, `S89.png`

## 2KG-18 — Einlagerungsräume (ER) Anastasius + Notleuchte (L), türkise Blickwinkel (PDF S. 90–91)

**PDF:** „In diesem Bereich wurde **nur eine Notleuchte (L)** mit Pfeil nach unten platziert. Der Grund … ist, dass die Menschen, die aus den einzelnen ER-Räumen flüchten, die Notleuchte (L) **bereits beim Verlassen ihrer Räume** erkennen können." Türkise Linien = Blickwinkel/direkte Sichtverbindungen; via (L) erkennen sie die **Tür** als weiteren Fluchtweg → „**keine weitere zusätzliche Richtungsleuchte** benötigt".

**DXF:** (L) = `1C8EF` ARR-down @ (28234, −14222), rot 270,09° → Welt-Pfeil 180,1° W = ins ER-GANG-Innere, an der Tür Richtung STGH-Bereich. Sichtlinien am Symbol: 3 erfasst (1848 / 3089 / 4801 mm) — das S.90-Bild zeigt 6 konvergierende Linien aus den ER 24–26/ASR (Stempel `1B42E` ER 26 @ 25406/−15656, `1B442` ER 25, `1B434` ER 22, GANG `1B474` @ 27520/−18496); die übrigen enden am Fangpunkt neben dem Symbol (>0,7 m, Zeichenpraxis). Personen `1CD0C`/`1CD31`/`1CD56` (Blick 3,5° O) + `1CD7F`/`1CD84`/`1CD86` (Blick 108,6°) ✓. Kette: (L)→(K) 3784 mm. Status: **bestätigt**.

Bilder: `S90.png`, `S91.png`

## 2KG-19 — Abschluss: Stiegenhaus, Medienraum, Aufzug — (K), (M), (N), Übergang 1KG (PDF S. 92–94)

**PDF:** ER-Menschen von (L) sehen (K) = **beidseitig**, Pfeile Richtung **Stiege**; auch die Garage-Menschen über die Schleuse bei (H) sehen (K) frontal → „beidseitige Ausführung … sinnvoll, weil Menschen aus unterschiedlichen Richtungen … zukommen." Position (K) wörtlich: „**mittig im Gang und gleichzeitig mittig zur Stiege** platziert. Die **gelben Linien** … zeigen, wie diese Position bestimmt wurde." UG-Regel wörtlich: „**Menschen, die aus einem Untergeschoß nach oben flüchten, bewegen sich über die Stiege in Richtung des Stiegenhauspfeils.**" **Medienraum:** „Grundsätzlich könnte auch bei der Tür des Medienraums eine eigene Notleuchte vorgesehen werden. In diesem Beispiel ist der Medienraum jedoch **nicht so groß, dass zwingend** eine eigene Notleuchte im Raum benötigt wird" + nur eine Tür; beim Verlassen sieht der Mensch (M) mit Pfeil nach unten (Pfeil entgegen Fluchtweg → geradeaus). **Aufzug:** Menschen sehen (N); „Hier wurde eine **Notleuchte mit Pfeil nach rechts** verwendet und so rotiert, dass der Pfeil **im dargestellten Plan nach links zeigt**". Abfolgen: Aufzug → (N) → (M) → (K) → Stiege → 1KG; ER/Garage → (K) → Stiege. „Ab der Notleuchte (K) flüchten die Menschen somit **gemeinsam** vom 2. Kellergeschoß in das 1. Kellergeschoß."

**DXF:** (K) = Gruppe 4 `1C936`/`1C937` @ (32018, −14236)/(32336, −14236) (einziges Paar mit 318 mm Abstand, horizontal nebeneinander), **Welt-Pfeil 269,8° S = Richtung Stiege** (STGH `1B19E` @ 33005/−15300; roter Stiegenhauspfeil `1CF44` (32022, −15123)→Spitze (32014, −19077) = Süd) ✓. **Gelbe Linien** `1D813` (28581, −14195)→(31875, −14240), 3295 mm = Gang-Flucht von (L) zu (K) („mittig im Gang") + `1D816` (32111, −15030)→(32112, −14530), 501 mm = Lot zur Stiege („mittig zur Stiege"); 4 Sichtlinien (956–1579 mm) am Paar. UG-Regel-Beleg: Personen `1CDD0` @ (32117, −15568) und `1CED6` @ (31967, −17868), beide Blick 286° ≈ Stiegenlaufrichtung Süd, mit Labels `1CDD1`/`1CED7` „**(2KG) geht hinauf richtung 1KG**" — sie bewegen sich in Stiegenhauspfeilrichtung ✓. (M) = `1C912` @ (33397, −16604), Welt-Pfeil 269,6° S, vor dem MEDIENRAUM (`1B3AC` @ 34467/−19796); im Medienraum selbst KEINE Leuchte ✓; 2 Sichtlinien (1492/2329 mm); (M)→(K) 2741 mm. (N) = `1C95A` **ARR-left mit xscale −29,87 = „Pfeil-nach-rechts"-Blocktyp**, rot 179,84° → **Welt-Pfeil 179,8° = im Plan nach LINKS** — der PDF-Satz „Pfeil nach rechts … so rotiert, dass der Pfeil im Plan nach links zeigt" ist damit die exakteste Typ-vs-Welt-Formulierung des ganzen Dokuments und stimmt 1:1 mit der DXF (Typ rechts + Spiegelung/Rotation → Welt links) ✓; vor dem AUFZUG (`1B11B` @ 34990/−16355), Person `1CE41` mit Label `1CE42` „(2KG)Aufzug"; (N)→(M) 2866 mm. Status: **bestätigt** (inkl. schönster Beleg der Typ/Welt-Trennung).

Bilder: `S92.png`, `S93.png`, `S94.png`

---

## Regel-Kandidaten (generalisierbar, mit Klassifikation + Beleg)

1. **Zusammenhängender, türloser Gang braucht keine Zwischen-Richtungsleuchten** — Menschen folgen dem Gangverlauf bis zum Ausgangs-RZ. *Fachpraxis.* (S. 58/61; DXF: keine RZ zwischen `1C707` und `1C695`)
2. **L-/Winkel-Schenkel ohne Leuchten-Sichtkontakt → Antipanikleuchte statt Richtungs-RZ**, mittig im abgeschatteten Bereich, Position über Diagonale konstruiert. *Fachpraxis.* (S. 58; `1C707` + Diagonale `1D03D`, 9 mm Treffer)
3. **Antipanik „sinnvoll" als Lux-/Dunkelstellen-Stütze auch ohne Pflicht** — Modalität SINNVOLL, nicht MUSS. *Optional/Empfehlung.* (S. 59; `1C706` + `1D045`)
4. **Wäre ein Gang durch Wand+Tür getrennt: Tür-RZ (down) + Folge-RZ nach der Tür** (rechts/links je nach Verlauf). *Fachpraxis, hypothetisch formuliert.* (S. 61; kein DXF-Gegenstück)
5. **Kurzer Gang + Direktsicht aller Raumtüren auf EIN Tür-RZ → keine weiteren Leuchten.** *Fachpraxis.* (S. 62 + S. 90–91; `1C697`, `1C8EF` mit 3–6 Sichtlinien)
6. **Weißer-Balken-Frontal-Regel:** Der lange weiße Balken (unten am Symbol) zeigt zur ankommenden Person; Pfeil zeigt ENTGEGEN der tatsächlichen Fluchtrichtung („geradeaus/hier durch"). *Fachpraxis, projektweit konsistent.* (S. 60, 63, 69, 70, 72, 85, 86; alle 16 down-Leuchten geometrisch konsistent)
7. **Kabeltrassen-Regel:** nie auf/in der Trasse; seitlich daneben; „möglichst … mindestens **450 mm**" (SOLL); Sichtbarkeit/Pfeilrichtung/Frontalität müssen erhalten bleiben (MUSS-Rahmen); 5-Schritt-Reihenfolge Fluchtweg-Position→Kollisionsprüfung→Versatz. *Fachpraxis (450 mm = projektübliche Praxisgröße, KEIN Normzitat!).* (S. 63–64, 79, 85, 88; KT-Texte `10100`–`10135`)
8. **Kabeltrassen-Versatz darf die Gebäudehälften-Zuordnung nicht kippen** (Leuchte bleibt auf ihrer Seite der Trennlinie). *Projektspezifisch.* (S. 79/81; `1C7D0` 507 mm neben `1C7F4`)
9. **Beidseitig-PFLICHT-Muster:** Wenn zwei Personenströme aus entgegengesetzten Richtungen dieselbe Leuchte brauchen, beidseitige Ausführung, damit beide frontal sehen (weißer Balken je Seite). *Fachpraxis.* (S. 66–68, 74–75, 89, 92–93; Gruppen 1, 2, 3, 4, 5)
10. **Beidseitig-ALTERNATIVE am Richtungswechsel:** Ist das nächste RZ ohnehin sichtbar, ist die Knick-Leuchte optional — S. 80: „nicht zwingend … würde sie trotzdem platzieren" (EMPFEHLUNG); S. 82/83: „kein Muss … lediglich dargestellt" (Demo). Orange = Alternativ-Farbcode. *Optional.* (Gruppe 6 `1D326`/`1D327`, Rechteck `1D34D`, Text `1D370`)
11. **Richtungswechsel-Grundsatz:** Bei Richtungswechsel, weiterem Ausgang oder Stelle mit Orientierungsbedarf SOLL eine Notleuchte sichtbar sein; ebenso beim Verlassen jedes Raums/jeder Wohnung. Ausnahme: OG mit einem Stiegenhaus + eindeutigem I-Gang (dort meist keine Richtungsleuchten; Schwerpunkt EG+UG). *Fachpraxis/Grundsatz.* (S. 74, 80)
12. **Motorrad-Stellplätze sind durchquerbar und dürfen Fluchtweg führen; Doppelparker/große PKW-Bereiche „nur sehr selten".** *Fachpraxis.* (S. 66, 69; Geometrie-Beleg: Personenreihe `1CBF6`–`1CBFC` durch MOTORRAD-Stempelzone, keine Fluchtwege durch DOPPELPARKER-Zonen)
13. **Nutzungs-Priorität kleiner Räume:** Technikraum/Niederspannungsraum bekommt Tür-Notleuchte (Gefährdung/wichtige Nutzung); Abstellraum (AR) und kleiner Medienraum mit nur einer Tür brauchen keine eigene. *Fachpraxis/projektspezifisch abwägend.* (S. 73, 85–86, 93; `1C644`, `1C8A9` vs. leerer AR/Medienraum)
14. **Notbeleuchtungs-Stromversorgung nicht an derselben Wand/im Bereich der (blauen) E-Verteiler.** *Fachpraxis (Anlagenplatzierung).* (S. 72; `1D10E`+`1D10F` an der Gegen-Wand des NIEDERSP.)
15. **Offener Durchgang (ohne Tür) am Knotenpunkt → down-Typ mittig im Durchgang**, wenn mehrere Räume aus verschiedenen Richtungen zulaufen; rechts/links/beidseitig wurden explizit erwogen und wegen Seitensicht verworfen. *Fachpraxis.* (S. 73–74; `1C64B` mittig auf 4 mm in 1250-mm-Durchgang, gelbe Linie `1D110`)
16. **Zwei-Gebäude-Projekte mit gemeinsamer Garage: Trennlinie = weitergeführte Gebäudewand; Fluchtwege/Pfeile/Rotationen je Hälfte getrennt planen.** *Projektspezifisch, aber Muster für Mehrgebäude-Projekte.* (S. 76–78; `1C7F4` 116 m, Merktext `1C7F5`)
17. **Prozessregel: Unklare Hälften-/Richtungs-Zuordnung NIEMALS raten → offene Frage an den Owner.** *Prozess/bindend für die Engine.* (S. 78 wörtlich)
18. **UG-Stiegenregel:** Menschen aus dem UG bewegen sich über die Stiege in Richtung des Stiegenhauspfeils (rot nachgezeichnet). *Fachpraxis, deckt EG-Regel 4.* (S. 93; `1CEFD` West + Personen Blick 169,9°, `1CF44` Süd + „geht hinauf richtung 1KG")
19. **Lichtberechnung = nachgelagerte Prüfschicht über der fachlichen Platzierungslogik, für ALLE Stockwerke und alle platzierten Elemente (RZ, Antipanik, Aufheller); Ziel: Zuverlässigkeit für künftige Automatik bewerten.** *Prozess/Engine-Anforderung (Owner, wörtlich S. 83–84).*
20. **Antipanik-Ausrichtung folgt der auszuleuchtenden Gang-Achse** (stehend vs. liegend, vgl. (C) stehend im N-S-Bereich, (K)/(B) liegend in O-W-Gängen) — aber Achtung Widerspruch bei (B) Mollgasse, siehe Offene Punkte 1. *Fachpraxis, teilbelegt.* (S. 58; `1C706` 225×746 vs. `1C707`/`1C7FB`/`1C9BD` 746×225)

## Offene Punkte

1. **(B) Mollgasse „vertikal ausgerichtet" (S. 58) widerspricht DXF UND PDF-Bild:** `1C707` liegt horizontal (746×225, rot 178,74°). Vertikal steht nur (C) `1C706`. Vermutlich Text-Verwechslung (B)↔(C) — Owner fragen, bevor eine „Antipanik-vertikal"-Regel gebaut wird.
2. **Kabeltrassen-Balken-Geometrie nicht eindeutig einem Layer zuordenbar:** KT-Texte lauten „KT UK=+2,11 FBOK" (nicht KT300/400/500); Kandidaten = Trassen-Route `1B502` (`07_SYM-G00-LKG-HLP`) + `02-HID`-Bänder; die vertikalen Schraffur-„Leitern" sind Rigole (Bodenrinnen), auf denen (I)/(J) zulässig stehen. Die 450-mm-Distanz ist dadurch im 2KG nicht sauber nachmessbar → Owner-Bestätigung nötig, welche Blau-Bänder KT sind (ggf. 1KG-DXF mit echten KT300/KT400-Labels prüfen).
3. **„nach rechts in Richtung der Notleuchte (C)" (S. 80):** Für den von (A) südwärts laufenden Menschen ist die Abzweigung nach (C) geometrisch links (Ost-Abzweig); „rechts" stimmt nur in Plan-Leserichtung bzw. für den Rampen-Gegenstrom. PDF-Richtungswörter hier NICHT als Personensicht übernehmen.
4. **Doppel-Label „(A)" Anastasius:** `1D157` @ (15985, −3192) hat keine Leuchte im Umkreis (nächste = `1C7D0`, 5,3 m) — vermutlich Zweitbeschriftung für einen Bildausschnitt oder Versehen. Bei Label-basierter GT-Extraktion filtern.
5. **Sichtlinien-Zählung:** GT nennt 230 „sichtlinien", als explizite ACI-4-Erklärlinien messbar sind 61; Differenz = Zählkriterium (Originalplan-Cyan/Blöcke?). Kriterium im GT-Extraktor dokumentieren.
6. **Gruppe 4 (K) Anastasius: Paarabstand 318 mm statt 264 mm** (einziger horizontaler Doppel-Block) — prüfen, ob für `RIVO_NL_ARR_bothsided`-Migration (M2) ein einheitlicher Soll-Abstand gilt.
7. **Sichtlinien-Fangpunkte:** Mehrere türkise Linien enden >0,7–1,5 m neben dem Symbol (z. B. (I) Mollgasse: 4 Linien im Bild, 0 im 1,5-m-Radius des Zentrums) — Endpunkt-Toleranz für automatische Sichtketten-Extraktion großzügig wählen.
8. **FREIHEIT/KEINE-FREIHEIT-Rahmen** (S. 77) liegen in der EG-Erklärungs-DXF, nicht in der 2KG-Datei — der Gebäudehälften-Kontext ist datei-übergreifend (EG-Abgleich Offene Frage 6 damit teilgeklärt: gehört zum 2KG-Kapitel S. 76–78).
