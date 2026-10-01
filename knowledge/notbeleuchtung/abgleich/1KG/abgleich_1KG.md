# Parallel-Abgleich PDF ↔ DXF — Mollgasse Notbeleuchtungserklärung, Geschoss 1KG

**Quellen:**
- PDF-Erklärtext Seiten 41–56 (`Notbeleuchtungen zeichnen`, Kapitel „1.KG Notbeleuchtung", beginnt S. 41 unten)
- DXF: `knowledge/Pläne zeichnen Wissen/Mollgasse-Notbeleuchtungserklärung/WHA_MOL_1KG_Notbeleuchtung_Erklärung.dxf`
  (INSUNITS mm; alle Positionen = **bbox-Zentren der virtuellen Entities** — die INSERT-Einfügepunkte liegen > 300 km entfernt)
- Ground-Truth-Messdaten: `tests/fixtures/mollgasse_gt/1KG.json` (14 Leuchten: 5 down / 3 left / 5 right + 1 Gruppenbatterie-Verteiler, 1 beidseitig-Paar; 44 Personen; 57 Labels)
- Seitenbilder: `S41.png` … `S56.png` in diesem Ordner (pypdfium2, scale=2)

**Konventionen (Phase B, in dieser DXF verifiziert):**
- „Pfeil nach unten/links/rechts" im PDF = **Block-TYP** (`RIVO-SIBEL-ARR-down` Basis 270°, `RIVO-SIBEL-ARR-left` Basis 180°, `RIVO-RZ-ARR_right` Basis 0°), nie Weltrichtung. Welt-Pfeil = Basis + rot; xscale<0 spiegelt.
- Personen-Läufer Block `750298750`: Blick = 180°+rot bei xscale>0, sonst rot (Regel #8).
- **Farb-Codierung dieser DXF weicht vom EG ab:** Fluchtweg = LWPOLYLINEs **ACI 100** (grün) + Pfeilspitzen-HATCHes ACI 100 (im EG: true_color 0x21DF37 → deshalb meldet das GT-JSON `n_fluchtweg_polylines: 0`). Sichtlinien = LWPOLYLINEs **ACI 4** (türkis), im Erklär-Handle-Bereich (> 0x1BC00) exakt **27 Stück** (`n_sichtlinien: 124` im GT zählt auch Architektur-Cyan). Stiegenhauspfeile = rot ACI 1 (Linie+Dreieck in einer LWPOLYLINE), 4 Stück + 4 rote MTEXTe „Stiegenhauspfeilrichtung". Gelb ACI 2 = Alternativ-/Falsch-Positionen (3 Kreise r=130 + Mittellinien + 4 MTEXTe). **Orange kommt in diesem Kapitel nicht vor** — Alternativen sind hier gelb.
- Erklär-Entities: Handles ≳ 0x1BCBB; die drei einzigen TÜR-INSERTs (`TÜR-BLOCKZARGE-90`: 1B153/1B154/1B156) sind Original-Architektur.
- Sichtlinien mit 3 Punkten (1CAC5, 1CAC9, 1CACD, 1CACE) = **zwei Sichtstrahlen zweier Personen mit gemeinsamem Scheitel an der Leuchte** (V-Form), nicht ein geknickter Strahl.

**Leuchten-Labels im DXF (grüne MTEXTe) — zwei Cluster, Buchstaben doppelt vergeben:**

| Label | Leuchte | Block | bbox-Zentrum | rot | xscale | Welt-Pfeil | Beispiel |
|---|---|---|---|---|---|---|---|
| (A) `1C9DF` | `1BCBB` | RZ-ARR_right | 143046, −11912 | 359.45° | 1.13 | ~0° Ost | 1KG-01/02/03 |
| (B) `1CA02` | `1BCBE` | RZ-ARR_right | 149859, −12602 | 269.45° | 1.13 | ~270° Süd | 1KG-04 |
| (C) `1CA25` | `1BE99` | RZ-ARR_right | 148370, −14394 | 179.45° | 1.37 | ~180° West | 1KG-05 |
| (A) `1C57E` | `1BEE4` | RZ-ARR_right | 169927, −36445 | 359.45° | 1.13 | ~0° Ost | 1KG-06 |
| (E) `1C60A` | `1BF97` | ARR-down | 179183, −31326 | 179.29° | 35.6 | ~90° Nord | 1KG-07 |
| (C) `1C5C4` | `1CB3E` | RZ-ARR_right | 179073, −36464 | 179.45° | 1.43 | ~180° West | 1KG-08 |
| (D) `1C5E7` | `1BFC3` | ARR-down | 180118, −36404 | 89.29° | 35.6 | ~0° Ost | 1KG-09 |
| (B) `1C5A1` | `1CD8C` | ARR-down | 175824, −36815 | 179.51° | 47.8 | ~90° Nord | 1KG-10 |
| (I) `1C696` | `1C00E`+`1C00F` | ARR-left ×2 | 181067/181462, −47229 | 269.45°/89.45° | +44.7/−44.7 | beide ~90° Nord | 1KG-11 |
| (H) `1C673` | `1BFEA` | ARR-down | 181352, −42035 | 359.29° | 47.8 | ~270° Süd | 1KG-12 |
| (F) `1C62D` | `1CAF5` | ARR-left | 175602, −42605 | 179.45° | +41.8 | ~0° Ost | 1KG-13 |
| (G) `1C650` | `1CD69` | ARR-down | 178727, −40782 | 88.94° | 47.8 | ~0° Ost | 1KG-14 |
| — | `1CB68` | Gruppenbatterie-Verteiler | 182187, −38513 | 89.45° | 27.6 | — | 1KG-09 |

Alle 14 GT-Leuchten sind PDF-Beispielen zugeordnet — **keine unerklärte Leuchte** (anders als im EG).
Personen-Labels: 33× (1KG), 5× (2KG), plus Lauftexte „(2KG) kommt von 2KG hinauf in den 1KG", „(1KG)/(2KG) geht hinauf in den EG", „(2KG) geht hinauf richtung 1KG".

---

## 1KG-01 — Stiegenhaus „random Raum": Notleuchte (A) an der Wand (PDF S. 41–42)

**PDF:** Beginn beim „random Raum" (Autor-Name, keine anderen nutzbaren Räume in dem Bereich). Der Mensch (1KG) sieht beim Verlassen/Fluchtweg-Beginn **zuerst** die Notleuchte (A) „mit Pfeil nach rechts". (A) **ist an der Wand platziert**; sie „**könnte alternativ** … mittig angeordnet werden" (→ 1KG-02). Blickwinkel als türkise Linie dargestellt.

**DXF:** (A) = `1BCBB` RZ-ARR_right @ (143046, −11912), rot 359.45° → **Welt-Pfeil ~0° = Ost**, an der Nordwand des oberen Stiegenlaufs. Person random Raum `1BE0B` @ (142615, −15156), Blick 11.3° (≈ Ost, Bau-Achse ~11° gedreht). Sichtlinie `1BE0D` (142651, −14886)→(143042, −12030): **2883 mm**, endet 118 mm an (A). Der Fluchtweg (grüne ACI-100-Polyline `1BCFA`, 12752 mm) startet bei (A) (143113, −12413), läuft Ost → Süd → West (U um die Stiege). Pfeil Ost = Laufrichtung des oberen Laufs ✓. Status: **bestätigt** (+ Maße). „Pfeil nach rechts" = Blocktyp + Personensicht (Welt-Ost).

Bild: `S41.png`

## 1KG-02 — Alternative Position für (A): Schnitt Stiegenmitte × Gangmitte (PDF S. 42)

**PDF:** Alternative Position = **gelber Kreis**; gelbe Linien zeigen die Konstruktion: „eine Linie durch die **Mitte der Stiege**" + „eine Linie durch die **Mitte des Ganges**" → Schnittpunkt. Wichtig: Pfeil muss Richtung Stiege/weiterer Fluchtweg zeigen. Modalität: **ALTERNATIV** („könnte … angeordnet werden") — hier gelb, nicht orange.

**DXF:** Gelbe Gangmitte-Linie `1CA67` (145043, −12535)→(142250, −12494) horizontal; gelbe Stiegenmitte-Konstruktion `1CA6E` mit Vertikalsegment (142845, −14582)→(142977, −12501); **Kreis `1CA6F` @ (142977, −12504), r=130** exakt am Schnittpunkt; MTEXT `1CA92` „(alternativ Position für Notleuchte (A))". Abstand Alternativ-Punkt → tatsächliches (A): Δx −70 / Δy −592 → **596 mm** (von der Wand in die Gangmitte). Status: **bestätigt** — die Konstruktion ist geometrisch exakt so gezeichnet wie beschrieben.

Bild: `S41.png` (Anmerkung links im Bild)

## 1KG-03 — Flucht 2KG→1KG hinauf: UG-Regel, Frontal-Balken, Blocktyp-Wahl (PDF S. 41 oben, 42–43)

**PDF:** OG-Menschen flüchten **entgegen**, UG-Menschen **immer in derselben Richtung wie die Stiegenhauspfeilrichtung** (rot nachgezeichnet). Der 2KG-Ankömmling sieht sofort (A). „Besonders wichtig": der **lange weiße Balken im unteren Bereich muss zur flüchtenden Person zeigen** — möglichst **frontal, nicht seitlich**. Pfeil-unten wäre hier falsch (nur bei Türen oder langen geraden Gängen), Pfeil-links ebenfalls (Balken würde zur Wand zeigen). **Regel: verläuft der weitere Fluchtweg aus Sicht der Person nach rechts → Pfeil-rechts-Leuchte** — „Diese Logik gilt entsprechend auch für andere Notleuchten und andere Richtungen."

**DXF:** Rote Stiegenhauspfeile: `1BD32` unterer Zug bei y≈−12.55k, Linie ab (145730, −12546), Dreieckspitze (148250, −12583) → **Ost**; `1BD31` Zug y≈−13.9k, Spitze (144030, −13896) → **West** (+ MTEXTe `1C836`/`1C813`). Personen-Paare belegen die UG-Regel: obere Reihe `1BCF8`/`1BD08`/`1C92E` Blick 11.3° (≈ Pfeilrichtung Ost, Labels (1KG)/(2KG)), untere Reihe `1BD7C`/`1BDC3` Blick 167.3° (≈ Pfeilrichtung West, Labels „geht hinauf in den EG"). 2KG-Ankömmling `1C909` @ (143771, −13897): Sichtlinie `1C9BC` → (A), **1735 mm**. (A) ist RZ-ARR_right mit rot ≈ 0 — der weiße Balken (Unterkante) zeigt nach Süd zu den ankommenden Personen ✓. Status: **bestätigt** (Personen-Rotationen + rote Pfeile decken die UG-Regel doppelt).

Bild: `S41.png`

## 1KG-04 — Notleuchte (B) + falsche Position (PDF S. 43)

**PDF:** Beide Menschen folgen (A) nach rechts und sehen dann **(B) mit Pfeil nach rechts**, frontal ausgerichtet. Gelber Kreis = **alternative Position, die „falsch beziehungsweise ungeeignet" wäre**: Menschen sähen die Leuchte **seitlich statt frontal**, und der Pfeil „würde in Richtung der Wand zeigen". Modalität: die gezeigte Position ist „**sinnvoller**".

**DXF:** (B) = `1BCBE` RZ-ARR_right @ (149859, −12602), rot 269.45° → **Welt-Pfeil ~270° = Süd** (am Ost-Ende des oberen Laufs; aus Sicht der Ost-Läufer „rechts" = Süd, Richtung Abwärtszug). Abstand (A)→(B) **6847 mm**. Sichtlinie `1BE9A` (146775, −12128)→(149775, −12489): **3021 mm**, frontal auf die Westseite des vertikal hängenden Schilds. **Falsche Position:** gelber Kreis `1CAC1` @ (149407, −11921) (MTEXT `1CAC2`), **817 mm** nordwestlich an der Nordwand — dort zeigte der Süd-Pfeil zur Wand und die Ost-Läufer sähen nur die Schmalseite ✓. Status: **bestätigt** (+ Maße; „Pfeil nach rechts" wieder Blocktyp, Welt-Süd).

Bild: `S41.png`

## 1KG-05 — Notleuchte (C) + zwei Alternativen (Wand / Decke) (PDF S. 43–44)

**PDF:** Nach (B) sehen beide **(C) mit Pfeil nach rechts**, „in der dargestellten Variante **an der Wand**". Zwei **alternative** Positionen: 1. an der Wand (gelber Kreis), 2. **an der Decke, mittig über beziehungsweise bei der Stiege**. Bei allen gilt: weißer Balken Richtung Menschen (frontal).

**DXF:** (C) = `1BE99` RZ-ARR_right @ (148370, −14394), rot 179.45° → **Welt-Pfeil ~180° = West** = Laufrichtung des unteren Stiegenzuges (aus Sicht der von (B) nach Süd Kommenden wieder „rechts"). (B)→(C) **2330 mm**. Sichtlinie `1BE9B` (149501, −13365)→(148371, −14235): **1425 mm**. Alternativen: Kreis `1CA9B` @ (149503, −14514) = Wand-Alternative, **1139 mm** östlich von (C); Kreis `1CAC3` @ (149517, −14025) = Decken-Alternative bei der Stiegenmitte, **1205 mm** von (C); je ein MTEXT `1CA9C`/`1CAC4` „(alternativ Position für Notleuchte (C))". Zusätzlich läuft eine türkise Linie `1CA9D` (1149 mm) vom Scheitelpunkt (149501, −13365) **zur Wand-Alternative** — der Autor hat sogar den Blickwinkel auf die Alternativposition visualisiert. Status: **bestätigt** (+ Maße). Alle drei Cluster-1-Leuchten sind derselbe Blocktyp RZ-ARR_right, nur rotiert (0°/270°/180°) — die PDF-Sprache „immer Pfeil nach rechts" ist konsequent personenbezogen.

Bild: `S41.png`

## 1KG-06 — Andere Stiege: Einlagerungsräume (ER) + türkise Blickwinkel auf (A) (PDF S. 45–46)

**PDF:** Andere Stiege des Projekts; Räume „ER" = **Einlagerungsraum = Kellerabteil**. Kernpunkt **Sichtbarkeit**: „Jede Person, die aus einem dieser ER-Räume flüchtet, sieht **bereits beim Verlassen des Raumes auf den ersten Blick** die Notleuchte (A)." Türkise Linien = Blickwinkel. Pfeil-rechts, weil die (1KG)-Menschen nach rechts weitergehen **müssen**; Balken frontal.

**DXF:** (A) = `1BEE4` RZ-ARR_right @ (169927, −36445), rot 359.45° → **Welt-Pfeil ~0° = Ost** (am Nordende des ER-Ganges ER 27–32, an der Wand zur Weiterführung Ost). **5 Sichtstrahlen für 5 Personen**: Einzellinien `1CAC6` (3066 mm, ab ER-28-Tür), `1CAC7` (4578 mm), `1CAC8` (4812 mm) + V-Polyline `1CAC5` mit Scheitel an (A) (Strahlen ~2300/1500 mm ab ER-31/27-Türen); alle enden ≤ 131 mm an der Leuchte. Fluchtweg: `1BEE6` Gang nordwärts (169651, −41133)→(169695, −36584) mit Stich-Ästen `1BEE7`–`1BEEA` von den ER-Türen, danach `1BFA0` (170188, −36448)→(175849, −36421) **5661 mm nach Ost** — exakt die Pfeilrichtung von (A) ✓. Personen `1BEBF`/`1C114`/`1C116` Blick 101.3° (Nord, im Gang), `1C118`/`1C11A` Blick 77.6°, `1C13F`/`1C213` Blick 11.3° (Ost, nach der Ecke). Status: **bestätigt** (+ Sichtstrahl-Metrik 1,5–4,8 m).

Bild: `S45.png`, `S46.png`

## 1KG-07 — ER-Gang: Notleuchte (E), Zusatzleuchte, Antipanik/Aufheller-Lehre (PDF S. 47, 49–50)

**PDF:** Nächste ER (36–39): **(E) mit Pfeil nach unten**, „so rotiert, dass der **Pfeil entgegen der Richtung des Fluchtwegs** zeigt", Balken frontal zu den Menschen; alle sehen (E) auf den ersten Blick (türkise Blickwinkel); Pfeil-unten = „**geradeaus weiter folgen**"; grüne Fluchtweglinie. S. 49: dieser Gang ist **länger** als der (A)-Bereich → „**sinnvoll**, zwischen den Bereichen eine zusätzliche Notleuchte zu platzieren" (Orientierung + Beitrag zur **Beleuchtungsstärke in Lux**). Ob Antipanik/Aufheller/weitere NL nötig sind, „hängt grundsätzlich von der **Lichtberechnung** ab". **Antipanikleuchten meistens in Untergeschoßen; runde Aufheller meistens EG bis OG**; Antipanik auch im EG bei Allgemeinräumen (Technikraum, KIWA, Spielraum, Fahrradraum, vergleichbare). S. 50: typischer Fall **U-förmiger Raum** — Antipanik in den unbeleuchteten Schenkel, gegen Stehen im Dunkeln/Panik.

**DXF:** (E) = `1BF97` ARR-down @ (179183, −31326), rot 179.29° → **Welt-Pfeil ~90° = Nord**; Fluchtweg läuft **Süd** (`1BF98` von Nord kommend zu (E), `1BF9D` (179181, −31483)→(179133, −36296) weiter 4813 mm süd zur GANG-Kreuzung) → Pfeil exakt **entgegen der Fluchtrichtung** ✓; Schild horizontal, Front nach Süd zu den Ankommenden. **5 Sichtstrahlen** auf (E): `1CACA` 3371, `1CACB` 2305, `1CACC` 3785 mm + V-Linie `1CAC9` (Strahlen 1276/855 mm); ER-Tür-Äste `1BF99`–`1BF9C`. Die Zusatz-Rolle belegt die Kette: (A2)-Bereich und (C2)-Kreuzung liegen **5909 bzw. 5139 mm** entfernt — (E) sitzt dazwischen im langen Gang. **Auffällig: im ganzen 1KG-DXF gibt es 0 Antipanikleuchten und 0 Aufheller** — die S.-49/50-Lehre bleibt hier theoretisch (Lichtberechnung nicht Teil der Erklärung); der U-Raum-Fall ist im EG belegt (EG-10). Status: **bestätigt** (Pfeil-entgegen-Regel gemessen); Antipanik-Teil: nur Text, kein 1KG-DXF-Beleg.

Bild: `S47.png`, `S49.png`, `S50.png`

## 1KG-08 — ER: Notleuchte (C) — „nach links" = Plan-links (PDF S. 48–49)

**PDF:** ER 33/34/40/41: beim Verlassen sehen die Menschen **(C)**, rotiert mit Balken frontal zu den (1KG)-Menschen. „Der Pfeil zeigt den Menschen, dass sie **nach links weiterflüchten müssen**." Wer von (E) geradeaus kommt, sieht nach dem Passieren (C) als nächste Orientierung.

**DXF:** (C) = `1CB3E` RZ-ARR_right @ (179073, −36464), rot 179.45° → **Welt-Pfeil ~180° = West**. Fluchtweg an der Kreuzung: `1BF9F` (178757, −36449)→(175849, −36421)→südlicher Stich — Fortsetzung **West** = Pfeilrichtung ✓. **4 Sichtstrahlen als 2 V-Polylines** mit Scheitel ≈ (179133, −36296) (≤ 180 mm an (C)): `1CACD` Strahlen 1707/1991 mm (ER 33/41), `1CACE` Strahlen 3875/3567 mm (ER 34/40). (E)→(C) **5139 mm**, (C)→(D) **1047 mm**, (C)→(B2) **3268 mm**. **Frame-Befund:** „nach links" ist hier **Plan-/Bild-links** (Welt-West), nicht Personensicht — die von Nord kommenden Läufer biegen körperbezogen nach **rechts** ab. Vgl. 1KG-13, wo das PDF ausdrücklich „im Plan nach rechts" sagt; S. 43 dagegen formuliert personenbezogen („aus Sicht der Person"). Status: **präzisiert** — Geometrie bestätigt, Richtungs-Vokabular wechselt zwischen Personen- und Plan-Frame; für Regelextraktion zählt nur der gemessene Welt-Pfeil.

Bild: `S48.png`, `S49.png`

## 1KG-09 — Niederspannungsraum / E-Raum / Technikraum: Tür-Leuchte (D) + Stromversorgung (PDF S. 51)

**PDF:** Niederspannungsraum (= E-Raum/Technikraum) enthält „**meistens** die Stromversorgung für das Projekt"; auch bei **zwei Gebäuden** ist „meistens **eine** Stromversorgung für alle Notleuchten ausreichend". Blau dargestellte **Elektroverteiler** für Untergeschoße + Allgemeinbereiche. Der Mensch (1KG) sieht **(D) mit Pfeil nach unten bei der Tür** → weiß, dass er durch diese Tür muss. Ausrichtungsregel (Balken frontal) + **Tür-Regel: Pfeil-unten-Leuchte wird bei einer Tür so rotiert, dass der Pfeil in die entgegengesetzte Richtung zur Öffnungsrichtung beziehungsweise zum Türflügel zeigt.**

**DXF:** (D) = `1BFC3` ARR-down @ (180118, −36404), rot 89.29° → **Welt-Pfeil ~0° = Ost = in den Raum** (Flucht führt West durch die Tür in den Gang). Türblock `1B154` TÜR-BLOCKZARGE-90 bbox-Zentrum (179407, −36429): **Δy = 25 mm zur Türachse (mittig), 711 mm raumseitig** vor der Tür. Sichtlinie `1CACF` von der Person `1C254`-Nähe (181138, −36638) zu (D): **893 mm**. **Stromversorgung:** Gruppenbatterie-Verteiler `1CB68` @ (182187, −38513) im NIEDERSP.R. (11.03 m²), daneben grüner Merktext `1CD1B` „**Notbeleuchtungs, Stromversorgung aller Notleuchten im Gebäude**" @ (183163, −38049); die blau/rot gekreuzten Verteiler-Rechtecke im Bild sind Original-Plan-Inhalt (DDB/FBDB-Markierungen), keine Erklär-Entities. Status: **bestätigt** (+ Maße; Tür-RZ-Muster identisch zum EG: mittig, ~0,7 m raumseitig, Pfeil entgegen Fluchtrichtung/Türflügel).

Bild: `S51.png`

## 1KG-10 — Nächste Tür: Notleuchte (B) (PDF S. 52 oben)

**PDF:** Nach dem Verlassen des Niederspannungsraums sieht der Mensch „die nächste **Notleuchte (B) mit Pfeil nach unten**, die ebenfalls bei einer Tür platziert wurde" → auch diese Tür benutzen.

**DXF:** (B) = `1CD8C` ARR-down @ (175824, −36815), rot 179.51° → **Welt-Pfeil ~90° = Nord**; Türblock `1B153` @ (175821, −37594): **Δx = 3 mm (exakt in der Türachse), 779 mm zugangsseitig (nördlich) vor der Tür**; die Flucht läuft Süd durch die Tür (`1C088` (175803, −37052)→(175753, −42218) Richtung Stiegenhaus) → Pfeil wieder **entgegen** der Durchgangsrichtung ✓. 2 Sichtstrahlen: `1CAD0` (2017 mm, von West/ER-GESAMT) und `1CAD1` (1749 mm, von Ost aus Richtung (C2)) — die Leuchte wird von beiden Anmarschrichtungen des Ganges gesehen. (D)→(B2) **4314 mm**, (A2)→(B2) **5909 mm**. Status: **bestätigt** (+ Maße).

Bild: `S52.png` (oben), `S51.png`

## 1KG-11 — Letzte ER: beidseitige Notleuchte (I) (PDF S. 52)

**PDF:** Bei den letzten ER wird **(I) als beidseitige Notleuchte** verwendet, weil der Mensch aus **ER 48** die Leuchte sonst „von seiner Position aus **nicht richtig sehen würde**"; ER 47–43 sehen die andere Seite. Vorgehen: „**Am einfachsten** … zunächst eine Notleuchte mit Pfeil nach rechts", Balken frontal zu ER 47–43, „**anschließend wird die Leuchte gespiegelt**, sodass daraus die beidseitige Notleuchte (I) entsteht."

**DXF:** (I) = ko-lokalisiertes Paar (`beidseitig_gruppe: 1`): `1C00E` ARR-left rot 269.45°, xscale **+44.7** @ (181067, −47227) + `1C00F` ARR-left rot 89.45°, xscale **−44.7** (gespiegelt!) @ (181462, −47231) — Versatz **395 mm in x, 4 mm in y** = zwei Rücken-an-Rücken-Gesichter quer zum O-W-Gang; **beide Welt-Pfeile ~90° = Nord** = Fluchtrichtung durch den Nordkorridor zu (H) (`1C016` (181247, −47073)→(181294, −42150)). Sichtstrahlen: Westseite `1CD1C` **1689 mm** von der ER-48-Person `1C6E3` (Blick 11.3° Ost); Ostseite `1CD1D`/`1CD1E`/`1CD1F` **2430/3527/5161 mm** von den ER-47/46/45/44-Läufern (Blick 191.3° ≈ West). Die Spiegelung ist im Datenmodell exakt ablesbar (xscale-Vorzeichen). Status: **bestätigt** (+ Konstruktions-Beleg). Hinweis Engine: seit M2 wird beidseitig als `RIVO_NL_ARR_bothsided` gerendert — der GT-Stand hier ist das historische Doppel-Block-Muster.

Bild: `S52.png`

## 1KG-12 — Tür-Leuchte (H) am Wasserzählerraum + „keine eigene Leuchte je ER-Tür" (PDF S. 53)

**PDF:** **(H) mit Pfeil nach unten bei der Tür**; wer den **Wasserzählerraum** verlässt oder in **ER 42** ist, sieht (H) und weiß, welche Tür zum Fluchtweg gehört. **Keine eigene Notleuchte bei jeder kleinen ER-Tür:** kleine Räume entlang eines UG-Ganges **benötigen keine zusätzliche eigene Pfeil-unten-Leuchte** an jeder Tür — Orientierung über die im Gang bzw. bei den relevanten Türen platzierten Notleuchten.

**DXF:** (H) = `1BFEA` ARR-down @ (181352, −42035), rot 359.29° → **Welt-Pfeil ~270° = Süd**; Türblock `1B156` @ (181326, −41267): **Δx = 26 mm (mittig), 768 mm zugangsseitig (südlich)** vor der Tür; Flucht Nord durch die Tür (`1C084` (181327, −41815)→(181336, −40874)→West zu (G)) → Pfeil entgegen ✓, Schild-Front nach Süd zu den Ankommenden. Sichtstrahlen: `1CD20` **1769 mm** (Wasserzähler-Person `1C6DF`), `1CD21` **3476 mm** (ER-42-Person `1C6E1`). Negativ-Beleg im Bestand: ER 42–48 und der Wasserzählerraum haben **keine** eigene Türleuchte — die 14 Leuchten des Geschosses sitzen ausschließlich an Fluchtweg-Knoten ✓. (I)→(H) **5195 mm**. Status: **bestätigt** (+ Maße). Modalität: „benötigen … keine" = NICHT NOTWENDIG (Referenz-Praxis, keine Norm-Zitation).

Bild: `S52.png`, `S53.png`

## 1KG-13 — Stiegenhaus: Flucht vom 2. KG herauf, Notleuchte (F) (PDF S. 54–56)

**PDF:** Stiegenhaus 1KG; Menschen „(2KG) geht hinauf Richtung 1KG" bewegen sich **in Richtung des Stiegenhauspfeils** (rot nachgezeichnet); OG umgekehrt (allgemeine Regel wiederholt). Beim Erreichen des 1KG sehen sie **(F)**: „Hier wurde eine **Notleuchte (F) mit Pfeil nach links** verwendet und **so rotiert, dass der Pfeil im Plan nach rechts zeigt**", Balken frontal → sie gehen Richtung Stiege/weiterer Fluchtweg. S. 56: (F) ist „so ausgerichtet, dass ihr **Pfeil in Richtung der Stiege zeigt**" → weiter über die Stiege Richtung EG; ab hier folgen 1KG- und 2KG-Menschen demselben Weg.

**DXF:** (F) = `1CAF5` **ARR-left** (Basis 180°) rot 179.45°, xscale **+41.8** (ungespiegelt) → **Welt-Pfeil ~0° = Ost = „im Plan nach rechts"** — die PDF-Formulierung beschreibt exakt Blocktyp + Rotation ✓✓. Position (175602, −42605) an der Südwand vor der Stiege; der rote Stiegenhauspfeil `1CD45` läuft (176397, −42280)→Spitze (180301, −42318) = **Ost** (MTEXT `1CD68`), der zweite `1C7F0` (174430, −37323)→Spitze (174393, −41228) = **Süd** (MTEXT `1CD44`) — die 2KG-Läufer `1C7EA`/`1C7EC`/`1C7EE` (Blick 14.9° ≈ Ost) laufen exakt in Pfeilrichtung des unteren Zuges ✓ UG-Regel. 3 Sichtstrahlen auf (F): `1CAF6` **1830 mm** (2KG-Läufer West-Zug), `1CAF7` **2516 mm**, `1CAF8` **2616 mm** (1KG-Läufer aus dem Gang). Status: **bestätigt** — stärkster Beleg des Kapitels für „Pfeilrichtungs-Sprache = Blocktyp, Weltrichtung = Rotation", weil das PDF beide Ebenen selbst benennt.

Bild: `S54.png`, `S55.png`, `S56.png`

## 1KG-14 — Notleuchte (G): Decke im Gang, Wand nur bei Stiegen; Alternative neben Aufzug (PDF S. 55–56)

**PDF:** Wer über (H) durch die Tür kommt, sieht **(G) mit Pfeil nach unten** → „**geradeaus weiter folgen**". Grund: ohne (G) hätten die Menschen nach der Tür **keine weitere sichtbare Notleuchte**. **Alternativ könnte man** an der **Wand rechts neben dem Aufzug** eine Pfeil-links-Leuchte platzieren — „**wäre hier jedoch ungünstiger**". S. 56, Platzierungslogik: „**Notleuchten an Wänden hauptsächlich im Bereich von Stiegen**. In normalen Gangbereichen werden die Notleuchten dagegen **grundsätzlich an der Decke** platziert." Deshalb die an der **Decke** platzierte (G). Danach sieht der Mensch (F).

**DXF:** (G) = `1CD69` ARR-down @ (178727, −40782), rot 88.94° → **Welt-Pfeil ~0° = Ost**; Flucht läuft **West** (`1C084`/`1C085` (181336, −40874)→(178943, −40852)→(175767, −40805)) → Pfeil entgegen, Schild vertikal mit Front nach Ost zu den aus der (H)-Tür Kommenden ✓. Lage: **Gangmitte** (nicht an einer Wandlinie) nordöstlich des AUFZUG-Schachts → „Decke" ist im 2D-DXF nur über diese Mittellage ablesbar — Wand- vs. Deckenmontage ist **keine explizite DXF-Eigenschaft**. (H)→(G) **2909 mm**, (G)→(F) **3617 mm**. (G) ist die einzige Erklär-Leuchte **ohne** türkisen Sichtstrahl (sie wird erst nach Tür-Durchtritt sichtbar, Personenkette `1C7A3`/`1C758`/`1C733` belegt den Lauf). Die Aufzug-Alternative ist **nur Text** — kein gelber Kreis/Marker im DXF (anders als 1KG-02/04/05). Status: **präzisiert** — Wand/Decke-Regel bestätigt sich in allen 14 Platzierungen (Wand-Positionen A1/B1/C1/A2/F nur an Stiegen; Gang-Leuchten E/G/I in Bandmitte; Tür-Leuchten D/B2/H an Türachsen), ist im DXF aber nur geometrisch indirekt belegt.

Bild: `S54.png`, `S55.png`, `S56.png`

---

## Abdeckung

Alle **14 GT-Leuchten** + Verteiler sind den Beispielen 1KG-01…14 zugeordnet (Tabelle oben) — keine Kopier-Reste, keine Duplikate (im Gegensatz zu EG `202CC`/`2137C`). Sichtketten-Abstände aufeinanderfolgender Leuchten: (A1)→(B1) 6847 · (B1)→(C1) 2330 · (A2)→(B2) 5909 · (E)→(C2) 5139 · (C2)→(D) 1047 · (C2)→(B2) 3268 · (D)→(B2) 4314 · (I)→(H) 5195 · (H)→(G) 2909 · (G)→(F) 3617 mm. Erklär-Sichtstrahlen: 27 türkise LWPOLYLINEs = 31 Strahlen (4 V-Formen), Längen **855–5161 mm**, Endpunkt-Toleranz zur Leuchte ≤ ~280 mm (Ausreißer nur die Alternativ-Position-Linie `1CA9D`).

**Kapitel-Themen ohne DXF-Beleg:** Kabeltrassen werden auf S. 41–56 **nicht erwähnt** (die 450-mm-Fachpraxis stammt aus anderem Material); Antipanik/Aufheller nur als Lehrtext (0 Instanzen im 1KG); Lichtberechnung nur als Verweis.

## Regel-Kandidaten

1. **Frontal-Balken-Regel** *(Fachpraxis, im PDF als „besonders wichtig"/„muss" formuliert)*: Der lange weiße Balken unten am RZ muss zur flüchtenden Person zeigen — frontal, nicht seitlich. Beleg: wörtlich S. 42/44/46/47/48/51/52/55; geometrisch in allen 13 RZ (Schild-Front jeweils zur Anmarschrichtung, z. B. (E) rot 179° Front Süd gegen Nord-Ankömmlinge).
2. **Blocktyp-Wahl nach Fluchtweg aus Personensicht** *(Fachpraxis)*: verläuft der weitere Weg aus Sicht der Person nach rechts → Pfeil-rechts-Block; sinngemäß für alle Richtungen; falsche Wahl erkennbar daran, dass der Balken zur Wand zeigt (S. 42–43). Beleg: Cluster 1 = 3× RZ-ARR_right mit rot 0/270/180.
3. **Pfeil-unten-Einsatzfälle** *(Fachpraxis)*: „meistens bei Türen oder bei längeren geraden Gängen (= geradeaus)" (S. 42–43, 47, 51–56). Beleg: alle 5 ARR-down des Geschosses sind Tür- (D/B2/H) oder Geradeaus-Leuchten (E/G).
4. **Tür-RZ-Metrik** *(Fachpraxis, deckungsgleich mit EG)*: mittig zur Türachse (Δ 3–26 mm), **~0,7–0,8 m vor der Tür auf der Zugangsseite** (711/779/768 mm), Pfeil entgegen Türflügel-/Durchgangsrichtung (S. 51 wörtlich; gemessen D/B2/H).
5. **UG-Stiegenregel** *(Fachpraxis/projektübergreifend)*: In Untergeschoßen flüchten Menschen **in** Stiegenhauspfeilrichtung (hinauf), in Obergeschoßen **entgegen** (S. 41/42/54–55). Beleg: 4 rote Nachzeichnungen + Personen-Blickwinkel beider Cluster.
6. **Wand nur bei Stiegen, Gang = Decke** *(Fachpraxis, S. 56 wörtlich „grundsätzlich")*: Wand-RZ ausschließlich an Stiegenbereichen (A1/B1/C1/A2/F), Gang-RZ in Deckenmitte (E/G/I). Wand/Decke ist im 2D-DXF nur über Wandabstand ablesbar → Engine-Kandidat: Wandlinien-Snap bei Stiegen, sonst Gangmittellinie.
7. **Alternativ-Konstruktion Gangmitte** *(optional/ALTERNATIV)*: mittige Position = Schnitt „Mittellinie Stiege × Mittellinie Gang" (S. 42; gelbe Linien + Kreis `1CA6F`, 596 mm von der Wandposition); Pfeil muss weiterhin Richtung Stiege/Fluchtweg zeigen.
8. **Sofort-Sichtbarkeits-Regel** *(Fachpraxis, normnah zu EN-1838-Erkennbarkeit, vom PDF aber nicht normativ zitiert)*: Jede Person sieht **beim Verlassen ihres Raums auf den ersten Blick** die nächste Leuchte; nach jedem Tür-Durchtritt muss sofort die nächste sichtbar sein (Begründung für (G), S. 55). Gemessene Sichtstrahlen 0,9–5,2 m; Kettenabstände 1,0–6,8 m.
9. **Kleine UG-Räume ohne eigene Türleuchte** *(Fachpraxis, NICHT NOTWENDIG)*: ER/Kellerabteile und kleine Nebenräume entlang eines UG-Ganges bekommen keine eigene Pfeil-unten-Leuchte je Tür; Orientierung über Gang-/Knoten-Leuchten (S. 53). Beleg: 8 ER + Wasserzähler teilen sich (I)+(H).
10. **Beidseitig-Kriterium + Konstruktion** *(Fachpraxis)*: Beidseitige NL, wenn mindestens eine Personengruppe sonst nur die Rückseite sähe (ER 48 vs. ER 43–47); Konstruktion = Einseitig-Block frontal zur Mehrheit, dann **spiegeln** (S. 52; xscale +44.7/−44.7, Versatz 395 mm).
11. **Zusatz-NL im langen Gang** *(SINNVOLL, lichtberechnungs-vorbehaltlich)*: längerer Gang → Zwischenleuchte für Orientierung + Lux-Beitrag; ob Antipanik/Aufheller/NL, entscheidet die Lichtberechnung (S. 49).
12. **Geschoss-Heuristik Antipanik/Aufheller** *(Fachpraxis)*: Antipanik meistens UG (bzw. EG-Allgemeinräume Technik/KIWA/Spiel/Fahrrad/vergleichbar, typisch U-förmige Räume), runde Aufheller meistens EG–OG (S. 49–50). Im 1KG selbst 0 Instanzen (nur Lehrtext).
13. **Eine Stromversorgung je Projekt** *(projektspezifisch/Referenz-Praxis, „meistens")*: auch bei zwei Gebäuden meist eine zentrale Versorgung im Niederspannungsraum; Verteiler für UG + Allgemeinbereiche dort (S. 51; Verteiler-Symbol `1CB68` + Merktext `1CD1B`).
14. **Richtungs-Vokabular ist frame-gemischt** *(Messkonvention, kein Platzierungs-Regel-Kandidat)*: „links/rechts" mal personenbezogen (S. 43 „aus Sicht der Person"), mal planbezogen (S. 48 „nach links" = Welt-West; S. 55 „im Plan nach rechts"). Regeln nie aus dem Wort, immer aus gemessenem Welt-Pfeil ableiten.

## Offene Punkte

1. **Blaue Erklär-Polylines `1C010`/`1C011`** (ACI 5, am (I)-Gang: 10-m-Horizontale + Kreuz am Leuchtenpunkt) — im PDF nirgends erklärt; vermutlich Gang-/ER-GESAMT-Hervorhebung des Autors. Nicht mit den „blauen Elektroverteilern" (S. 51, Original-Plan) verwechseln.
2. **(G)-Alternative „Wand rechts neben Aufzug"** existiert nur als Text — kein gelber Kreis im DXF (Bruch mit der sonstigen Visualisierungs-Konvention der Alternativen).
3. **Antipanik/Aufheller-Lehre ohne 1KG-Instanz**: ob der 1KG nach Lichtberechnung tatsächlich ohne Antipanik auskommt, ist weder im PDF noch im DXF belegt (Lux-Nachweis auf Experten-Placement = Task G3).
4. **GT-Zählung `n_sichtlinien: 124`** enthält Architektur-Cyan; Erklär-Sichtlinien sind 27 (Handle-Filter > 0x1BC00). Extraktor-Filter ggf. schärfen, wenn Sichtlinien je Leuchte als GT-Feature gebraucht werden.
5. **Label-Buchstaben doppelt**: (A)/(B)/(C) existieren in beiden Stiegen-Clustern des Geschosses — bei automatischer PDF↔DXF-Label-Zuordnung immer über Koordinaten matchen (gleiches Muster wie EG-Label-Drift, hier aber ohne Widerspruch).
6. **Fluchtweg-Farbe wechselt je Geschoss-DXF** (EG true_color 0x21DF37 vs. 1KG ACI 100): GT-Extraktor erkennt 1KG-Fluchtwege derzeit nicht (`n_fluchtweg_polylines: 0`) — für G1 nachziehen.
