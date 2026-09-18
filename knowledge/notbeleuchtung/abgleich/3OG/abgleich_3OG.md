# Parallel-Abgleich PDF ↔ DXF — Mollgasse 3OG (PDF-Seiten 27–30)

Quellen:
- PDF-Text/Seiten 27–30 der Mollgasse-Notbeleuchtungserklärung (Seitenbilder `seite_27.png`–`seite_30.png`).
- DXF: `knowledge/Pläne zeichnen Wissen/Mollgasse-Notbeleuchtungserklärung/WHA_MOL_3OG_Notbeleuchtung_Erklärung.dxf` (AC1032, `$INSUNITS=4` → mm; Modelspace; Layouts nur Blattrahmen).

Konventionen (in dieser DXF verifiziert):
- **Welt-Pfeil der RZ-Leuchten = Basis + INSERT-Rotation** (Registry: ARR-down Basis 270°, ARR-left Basis 180°, RZ-ARR_right Basis 0°).
- **Fluchtwegpfeil-Block `4444444`: Spitze zeigt bei rot 0 nach LINKS (Welt 180°)** → Welt-Richtung = (180° + rot) mod 360. Belegt: die 3 Pfeile h=78EA0/78EA1/78EA2 (rot 179,9 → Welt 359,9° = rechts) liegen exakt auf der (A)-Fluchtlinie y≈16 060 und zeigen wie im PDF-Bild S. 27 nach rechts.
- **Menschensymbol `750298750`: Läufer blickt bei rot 0, xscale>0 nach LINKS (Welt 180°)** → Blick = (180° + rot) mod 360; bei **xscale<0 (gespiegelt): Blick = rot**. Belegt: Top-20-/Top-21-Person (rot 101,9, xs=−4,007 → Blick 101,9° ≈ Nord-Nordwest) blickt exakt zur Leuchte (B) im Norden (Sichtlinien h=79396/793BC); 4OG-Läufer h=78F78/78F9D (rot 342,4, xs=+4 → Blick 162,4° ≈ links) laufen entgegen dem roten Ost-Stiegenhauspfeil.
- Grüne Fluchtweg-Linien = LWPOLYLINE color 102, Sichtlinien = color 4 (türkis), rote Nachzeichnungen = color 1, Personen-/Leuchten-Labels = MTEXT color 3.

Die DXF enthält **drei** Notbeleuchtungs-Cluster:
- **A2** = Stiegenhaus 1 mit Aufzug (um x≈−1 785 000, y≈16 000) → Beispiel 3OG-01 (PDF S. 27–28)
- **A3** = Stiegenhaus 2 + Gang (um x≈−1 748 000, y≈−12 000) → Beispiel 3OG-02 (PDF S. 29–30) + ein NICHT erklärter West-Teil
- **A1** = frei schwebendes Fragment ohne Plan-Geometrie (x≈−1 811 000…−1 803 000, y≈15 000…16 800) → in keiner PDF-Seite 27–30 erklärt

---

## Beispiel 3OG-01 — Stiegenhaus im 3. OG, Wohnung Top 16+17 (PDF S. 27–28)

**PDF-Aussagen:** (1) Nur eine Wohnung „Top 16+17“; Person sieht beim Verlassen unmittelbar Notleuchte (A) mit Pfeil nach rechts (türkise Sichtlinie). (2) Leuchten bei Richtungswechsel auf den ersten Blick erkennbar. (3) „4OG“-Menschen sehen auf dem Weg zum 3. OG die Notleuchte (B) mit Pfeil nach links; danach (A) mit Pfeil nach rechts. (4) Flucht über die Stiege nach unten **entgegen** der Richtung des rot nachgezeichneten Stiegenhauspfeils.

**DXF-Fakten:**

| Objekt | Handle | Block | Zentrum (mm) | rot | Welt-Pfeil |
|---|---|---|---|---|---|
| Leuchte (A), Label h=7900B | **78D92** | RIVO-RZ-ARR_right | (−1 784 516, 16 068) | 359,9° | **359,9° = rechts** ✓ |
| Leuchte (B), Label h=7902E | **78DB5** | RIVO-SIBEL-ARR-left | (−1 781 086, 17 879) | 359,4° | **179,4° = links** ✓ |

- Raum: STGH 11,14 m² (01-SQM h=78104, Label 131 mm neben (A)), „3. STOCK“, AUFZUG 8 PERS., VR 5,09 m²; Stiege „9 HÖHEN, STG 16,9/28,0“ (06-TXT h=780F7). Plan lokal um −0,3° verdreht (rot≈359,7 überall).
- Wohnungstür Top 16+17: 00-top h=78789 bei (−1 785 157, 14 097); Türblatt TÜR-BLOCKZARGE-SCHACHT_125 h=78983 (−1 784 535, 13 453).
- **Sichtlinie** h=78FE8 (türkis): (−1 785 293, 14 101) → (−1 784 561, 15 909); **Länge 1 950 mm**, Richtung 68,0°; Startpunkt 136 mm neben der Türmitte, Endpunkt 165 mm vor dem (A)-Zentrum. Kreuzt **keine** Wand (Schnitte nur mit Achs-/Hidden-Layern 02-AXO/02-HID, keine 02-TWA/02-ZWA). Blickwinkel zur (A)-Vorderseite: Schild-Längsachse horizontal → Abweichung von frontal nur **22°** → Person sieht die Vorderseite.
- Tür→(A) Mitte-zu-Mitte: **2 073 mm** (Δ=641 östl., 1 971 nördl.) — (A) sitzt NICHT türmittig, sondern am **Richtungswechsel** im STGH (Knick des grünen Fluchtwegs h=78E2E: Tür → 592 mm Ost → 1 815 mm Nord zu (A)).
- **(A) „vor der Stiege“ in Zahlen:** Abwärts-Lauf = rote Nachzeichnung h=78F0E (Pfeilspitze West bei (−1 783 347, 15 947), Schaft bis (−1 779 897, 15 930)). (A) liegt 1 169 mm westlich des Laufbeginns, nur ~130 mm neben dessen Achse; (A)-Pfeil 359,9° = exakt die Gehrichtung der Abwärtsflucht (entgegen dem roten West-Pfeil, Δ=180,4°).
- **(B) für 4OG-Absteigende:** oberer Lauf = rote Nachzeichnung h=78F9F, Spitze OST bei (−1 781 195, 17 426) (Richtung ≈359,5°), Label „Stiegenhauspfeilrichtung“ h=78FC2/78F31 (rot). (B) sitzt 454 mm nördlich der Laufachse, 109 mm östlich der Pfeilspitze = am Antritt des oberen Laufs; (B)-Pfeil 179,4° = **entgegengesetzt** zum roten Pfeil (Δ=179,9°) und = Gehrichtung der 4OG-Menschen ✓.
- Personen (Block 750298750, Label MTEXT): (3OG) h=78E28 (−1 785 561, 14 069) Blick 78,3°; (3OG) h=78EE9 (−1 784 495, 14 699) Blick 78,3°; (3OG) h=79052 (−1 781 854, 15 957) Blick 11,5°; (4OG) h=78F0D (−1 782 722, 15 958) Blick 11,5°; (4OG) h=78FE6 (−1 784 416, 17 400) Blick 252,2°; (4OG) h=78F9D (−1 782 218, 17 382) Blick 162,4°; (4OG) h=78F78 (−1 780 652, 17 410) Blick 162,4°.
- Fluchtwegpfeile 4444444: h=78EC5 (Tür, Welt 0°=Ost), 78E7D (Welt 89,9°=Nord zu (A)), 78EA0/78EA1/78EA2 (Welt 359,9°=Ost ab (A)), 78E5A (Welt 269,9°=Süd zum (A)-Band), 78E58/78E59 (Welt 179,9°=West am oberen Lauf).

**Status: bestätigt + präzisiert.** Alle vier PDF-Aussagen stimmen; präzisiert um: Sichtlinie 1 950 mm/22° frontal, (A) 2 073 mm von der Türmitte am Knick, beide rot nachgezeichneten Stiegenhauspfeile (359,5° oben / 180,3° unten) jeweils exakt entgegen der lokalen grünen Fluchtrichtung.

Bild: `3OG-01.png` (links PDF S. 27, rechts DXF-Crop).

---

## Beispiel 3OG-02 — Gang im 3. OG ohne Abtrennung zum Stiegenhaus (PDF S. 29–30)

**PDF-Aussagen:** (1) Gang nicht durch Tür vom Stiegenhaus getrennt; Wohnungstüren Top 18+19, 20, 21, 22. (2) Notleuchte (B) mit Pfeil nach links → nach links zur Stiege, 3. OG → 2. OG. (3) Bei jeder Wohnungstür ein grünes „3OG“-Menschensymbol; türkise Sichtlinien; jede Person sieht (B) auf den ersten Blick. (4) (B) wurde **vor der Stiege und mittig im Gang** platziert; in Gangmitte würde der Links-Pfeil zur Wand zeigen.

**DXF-Fakten:**

| Objekt | Handle | Block | Zentrum (mm) | rot | Welt-Pfeil |
|---|---|---|---|---|---|
| Leuchte (B), Label h=79402 | **78DDA** | RIVO-SIBEL-ARR-left | (−1 743 996, −11 979) | 359,4° | **179,4° = links** ✓ |

- Räume: STGH 24,09 m² (h=77E3C), „3. STOCK“ (h=780A2), 17-Höhen-Stiege „16,9/28,0“ (06-TXT h=7803B) — **ein gerader Lauf**: rote Nachzeichnung h=792B8 von (−1 750 513, −12 022) bis Spitze (−1 746 033, −12 022) = 4 480 mm = exakt 16 Auftritte × 280 mm. Gang läuft Nord-Süd bei x≈−1 744 000; keine Tür zwischen Gang und STGH (grüne Linien h=79056/79055 laufen ohne Türblock durch) ✓.
- Türen (00-top): TOP 18+19 h=78A44 (−1 744 018, −9 842); TOP 20 h=77EA2 (−1 743 393, −13 172); TOP 21 h=77E8E (−1 744 018, −16 252); TOP 22 h=77E8A (−1 744 643, −14 837).
- **„Mittig im Gang“ in Zahlen:** Gang-Innenkanten bei y=−14 000: x=−1 744 643 (02-TWA h=77D21) und x=−1 743 393 (02-TWA h=77C90) → lichte Breite **1 250 mm**, Mittellinie x=−1 744 018. (B) bei x=−1 743 996 → **22 mm** neben der Gangmitte ✓.
- **„Vor der Stiege“ in Zahlen:** (B) y=−11 979 liegt 43 mm neben der Stiegenlauf-Achse (rot y=−12 022); (B) steht 2 037 mm östlich der roten Pfeilspitze, am T-Stoß Gang/Stiege. (B)-Pfeil 179,4° zeigt exakt in den Stiegenlauf; roter Stiegenhauspfeil 0,0° (Ost) → **entgegengesetzt (Δ=179,4°)** ✓; grüne Fluchtpfeile auf dem Lauf h=79271/79294/792B7 (Welt 179,9° = West) = entgegen rot ✓.
- **Sichtlinien zu (B)** (alle enden ≈150 mm südlich des (B)-Zentrums, keine kreuzt eine Wand — Schnitte nur mit 02-AXO/02-HID):

| von | Handle | Start → Ende | Länge | Abw. von frontal* |
|---|---|---|---|---|
| Top 18+19 | 79327 | (−1 743 691, −9 666) → (−1 744 041, −11 813) | **2 175 mm** | 9,3° |
| Top 20 | 79396 | (−1 743 443, −13 145) → (−1 743 977, −12 138) | **1 140 mm** | 27,9° |
| Top 21 | 793BC | (−1 744 265, −16 403) → (−1 743 977, −12 138) | **4 275 mm** | 3,9° |
| Top 22 | 79370 | (−1 744 458, −14 726) → (−1 744 002, −12 122) | **2 644 mm** | 9,9° |

*(B)-Schild-Längsachse horizontal (O-W) → frontal = Blick aus Süd/Nord; alle 4 Personen sehen die Vorderseite (≤28°).*
- Personen (alle Label „(3OG)“): Top 18+19 h=79325 (−1 743 958, −9 634) Blick 281,7°; Top 20 h=79394 (−1 743 176, −13 177) Blick 101,9°; Top 21 h=793BA (−1 743 998, −16 434) Blick 101,9°; Top 22 h=7936F (−1 744 725, −14 758) Blick 78,3° — jede blickt zu (B) ✓.
- Fluchtwegpfeile im Gang: 791C2/791E5/79208 (Welt 89,9° = Nord), 7922B (Top 22, Ost), 7924E (Top 20, West), 7917B/7919E (Welt 269,9° = Süd von Top 18+19 zu (B)).

**Status: bestätigt + präzisiert.** Alle vier PDF-Aussagen geometrisch belegt; präzisiert um: 22 mm Mittigkeit bei 1 250 mm Gangbreite, 43 mm Fluchtachsen-Deckung zur Stiege, Sichtlinien 1 140–4 275 mm mit ≤28° Frontalabweichung. Die PDF-Begründung „in Gangmitte würde der Pfeil zur Wand zeigen“ stimmt geometrisch: auf Ganghöhe y≈−13 500 läge westlich direkt die Wand x=−1 744 643 (ASR/VR), die Stiege beginnt erst bei y≈−12 022.

Bild: `3OG-02.png` (links PDF S. 29, rechts DXF-Crop).

---

## Nicht in den PDF-Seiten 27–30 erklärte Notbeleuchtung

1. **Leuchte „(A)“ West-Teil Stiegenhaus 2** — Handle **78DFD**, Block RIVO-SIBEL-ARR-down, Zentrum (−1 750 373, −10 572), rot 269,7° → **Welt-Pfeil 179,7° = links/West**; Label „(A)“ MTEXT h=793DF (−1 750 215, −10 344). Zugehörig, aber ebenfalls unerwähnt: Türen TOP 16 h=77E86 (−1 752 273, −12 012) und TOP 17 h=77F10 (−1 752 273, −9 422), Personen h=79084 (Blick 78,3°) und h=792FF (Blick 281,7°), Doppel-Sichtlinie h=79301 (Top-16-Tür → 174 mm vor (A) → Top-17-Tür; Teillängen 2 215 mm und 1 984 mm). Liegt links außerhalb des PDF-Bildausschnitts von S. 29; im Text der Seiten 29–30 kommt nur (B) vor. **Auffällig:** Der (A)-Pfeil (West, 179,7°) zeigt entgegen den grünen Fluchtpfeilen h=79135/79158 (Welt 359,9° = Ost) auf derselben Route y≈−10 590 Richtung Gang/(B) → siehe offene Fragen.
2. **Fragment A1 (frei schwebend, keine Plan-Geometrie im Umkreis):**
   - RIVO-SIBEL-ARR-left h=**78D6A**, Zentrum (−1 803 433, 15 078), rot 359,4° → Pfeil links;
   - RIVO-RZ-ARR_right h=**78D6C**, Zentrum (−1 810 859, 15 083), rot 89,9° → Pfeil oben;
   - RIVO-SIBEL-ARR-down h=**78D6D**, Zentrum (−1 809 240, 16 506), rot 269,7° → Pfeil links; daneben Label „(B)“ h=78D6B und Person h=78D6E mit Label „(2OG)“ h=78D6F.
   Wirkt wie ein Kopier-Rest der 2OG-Erklärung (Labels (B)/(2OG)); in keiner 3OG-PDF-Seite referenziert.

**Abdeckung:** 7 Notleuchten-INSERTs gesamt (3× ARR-left, 2× RZ-ARR_right, 2× ARR-down) → 3 erklärt (78D92, 78DB5, 78DDA), 4 unerklärt (78DFD, 78D6A, 78D6C, 78D6D). Keine weiteren ungelabelten Notbeleuchtungs-INSERTs (Antipanik/Aufheller/Spot/Gruppenbatterie: 0 im 3OG-DXF). Personen: 14 (7 A2, 6 A3, 1 A1). Fluchtwegpfeile 4444444: 25 (8 A2, 17 A3). Sichtlinien: 6. Rote Nachzeichnungen: 3 (+3 rote MTEXT „Stiegenhauspfeilrichtung“ h=78F31/78FC2/792DB).

---

## Regel-Beobachtungen (Rohstoff Regelbasis)

1. **RZ vor der Stiege auf der Fluchtachse:** Beide erklärten Stiegen-RZ sitzen ≤130 mm bzw. 43 mm neben der Stiegenlauf-Achse und der Pfeil zeigt exakt (Δ≤0,6°) in die Abwärts-Gehrichtung des Laufs [3OG-01 (A) 78D92; 3OG-02 (B) 78DDA].
2. **Mittig im Gang = Gang-Mittellinie:** (B) 78DDA steht 22 mm neben der Mittellinie eines 1 250 mm breiten Gangs [3OG-02].
3. **Pfeil entgegen Stiegenhauspfeil:** Leuchtenpfeil vs. rot nachgezeichneter (Original-)Stiegenhauspfeil = 179,4°–180,4° Differenz in allen 3 belegten Fällen [(B) 78DB5 vs h=78F9F; (A) 78D92 vs h=78F0E; (B) 78DDA vs h=792B8]; ebenso grüne Fluchtpfeile auf dem Lauf (Δ=180°).
4. **Sichtlinie ab Türmitte, frontal:** Türkise Sichtlinien starten ≤136 mm neben der Wohnungstür-Position (00-top-Block) und treffen die Leuchte mit ≤28° Abweichung von der Frontalen (Schild-Längsachse ⟂ Sichtlinie); Längen 1 140–4 275 mm; keine kreuzt eine Wand (nur 02-AXO/02-HID-Schnitte) [3OG-01, 3OG-02].
5. **RZ am Richtungswechsel, nicht an der Tür:** (A) 78D92 ist 2 073 mm von der Türmitte entfernt am Knick des Fluchtwegs platziert (Tür→592 mm Ost→1 815 mm Nord); die PDF nennt als Kriterium „bei Richtungswechsel auf den ersten Blick erkennbar“ [3OG-01].
6. **Ein RZ kann mehrere Türen bedienen:** (B) 78DDA deckt 4 Wohnungstüren (Sichtlinien 1 140–4 275 mm) ohne Zwischen-RZ im 7-m-Gang ab; zusätzlicher Beleg: Doppel-Sichtlinie h=79301 bündelt Top 16 UND Top 17 auf eine Leuchte [3OG-02, unerklärter West-Teil].
7. **Symbol-Rotation statt Symbol-Wechsel:** „Pfeil links“ wird zweimal als ARR-left mit rot≈359,4 und einmal als ARR-down mit rot≈269,7 erzeugt (78DFD, Fragment 78D6D) → Welt-Pfeil zählt, nicht der Blockname; deckt sich mit der 2OG-Aussage „(C) … so rotiert, dass sie in die entgegengesetzte Richtung zeigt“ (S. 24).
8. **Plan-Verdrehung wandert in die Symbole:** Alle Leuchten/Pfeile tragen die lokale Planrotation (−0,3°: rot 359,4/359,9/269,7 statt 0/90/270) → Toleranz ±1° beim Richtungs-Mapping nötig [alle].
9. **Stiegen-Bemessung als Kontrolle:** Rote Nachzeichnung 792B8 = 4 480 mm = 16 Auftritte × 280 mm (06-TXT „17 HÖHEN, 16,9/28,0“) — die Stufengeometrie bestätigt Lage und Länge des Stiegenlaufs [3OG-02].

## Offene Fragen

1. **Widerspruch am unerklärten (A) 78DFD:** Pfeil Welt 179,7° (West, zu den Türen Top 16/17 bzw. zur Westwand), aber die grünen Fluchtpfeile h=79135/79158 auf derselben Route (y≈−10 590) zeigen 359,9° (Ost, zum Gang und weiter zu (B)/Stiege). Ist (A) falsch rotiert, wandmontiert mit anderer Bedeutung („hinunter“), oder für eine andere Personengruppe gedacht? PDF-Seiten 27–30 schweigen dazu.
2. **Fragment A1:** 3 Leuchten + Person „(2OG)“ ohne umgebende Plan-Geometrie — Kopier-Rest aus der 2OG-Erklärung oder bewusst geparkt? Sollte vor einer Regel-Extraktion aus Roh-Inventaren gefiltert werden (Kriterium: keine Wand-Layer im Umkreis).
3. **Tür-Öffnungsrichtung:** Die PDF-Seiten 27–30 machen keine Aussage „Pfeil entgegen der Öffnungsrichtung“; Türflügel-Geometrie wurde daher nicht je Tür ausgewertet.
4. **Zwei rote Pfeile in 3OG-01:** Ober- und Unterlauf tragen je eine eigene Nachzeichnung mit entgegengesetzter Richtung (359,5° vs 180,3°) — der „Stiegenhauspfeil“ ist offenbar je Lauf definiert (Auf-Richtung), nicht je Stiegenhaus.

## Bilder

- `3OG-01.png` — links PDF S. 27, rechts DXF-Crop Stiegenhaus 1 (x −1 787 600…−1 778 400, y 13 100…19 300)
- `3OG-02.png` — links PDF S. 29, rechts DXF-Crop Gang/Stiegenhaus 2 (x −1 749 200…−1 741 200, y −17 700…−8 500)
