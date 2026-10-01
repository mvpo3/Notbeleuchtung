# Parallel-Abgleich PDF <-> DXF — Geschoss DG (Mollgasse)

Quellen:
- PDF-Erklaertext Seiten 39–41 (`pdf_seiten/text.txt`, Abschnitt „Dachgeschoß Notbeleuchtung").
- DXF: `knowledge/Pläne zeichnen Wissen/Mollgasse-Notbeleuchtungserklärung/WHA_MOL_DG_Notbeleuchtung_Erklärung.dxf`
  (AC1032, `$INSUNITS=4` → **alle Koordinaten in mm**; Paperspace „Layout1" leer, alles im Modelspace).

Konventionen (an diesem DXF gemessen):
- **Fluchtwegpfeil `4444444`**: Dreieck-Spitze zeigt bei rot 0 nach **180° (links/West)** → Welt-Azimut = 180° + INSERT-Rotation.
- **Menschensymbol `750298750`** (nested `9809550`, grün ACI 3): bei rot 0 und xscale > 0 schaut der Laeufer nach **links (180°)**.
  Alle Instanzen hier sind mit |xscale|=4.007 skaliert; **Blick-Azimut = Rotation (bei xscale < 0, gespiegelt) bzw. Rotation + 180° (bei xscale > 0)**.
  Gegenprobe: Personen 20902/20904 (rot 2.89, xs=−4.007) laufen exakt mit den Ost-Fluchtwegpfeilen (Azimut ≈ 2.9°) ✓.
- **RZ-Welt-Pfeil** = Basisrichtung (down 270° / left 180° / right 0°) + INSERT-Rotation.
- Erklaerungs-Overlay komplett auf Layer `0` mit expliziten Farben: grün ACI 3 (Labels, Menschen, Fluchtweg), rot ACI 1 (Stiegenhauspfeil-Nachzeichnung), cyan ACI 4 (Sichtlinien), blau ACI 5 (Lichtkuppel).
- West-Trakt des Plans ist global um ca. −0.3° gedreht (Rotationen 359.71/269.71 statt 0/270).

---

## DG-01 — „Dachgeschoß – Wohnung Top 20 und Stiegenhaus" (PDF S. 39–40 oben)

**PDF-Aussagen:** Kein zusätzlicher Gang, nur Stiegenhaus. Mensch „DG" verlässt Top 20 und sieht **direkt von vorne** Notleuchte **(A) mit Pfeil nach rechts**, die **vor der Stiege** platziert ist, Pfeil **direkt zur Stiege**. Türkise Linie = Sichtverbindung. Mensch „DG/Podest" im Podestbereich sieht Notleuchte **(B) mit Pfeil nach links, an der Wand**; folgt er (B), sieht er anschließend (A).

**DXF-Fakten:**

| Objekt | Handle | Block | Sichtbares Zentrum (bbox) | Rotation | Welt-Pfeil/Blick |
|---|---|---|---|---|---|
| (A) | `206DC` | RIVO-RZ-ARR_right | (667, 26391) | 359.87° | **359.87° ≈ Ost (rechts)** |
| (B) | `20705` | RIVO-SIBEL-ARR-left | (4697, 28335) | 359.42° | **179.42° ≈ West (links)** |
| Person „(DG)" Top 20 | `206D8` | 750298750 | (634, 25541) | 92.75 (xs=−4.007) | Blick **92.75° = Nord** (zu A) |
| Person „(DG)" auf Stiege | `20780` | 750298750 | (2336, 26342) | 2.75 (xs=−4.007) | Blick **2.75° = Ost** (Abstieg) |
| Person „(DG/Podest)" | `207CB` | 750298750 | (4128, 27813) | 356.98 (xs=+4.007) | Blick **176.98° = West** |
| Sichtlinie cyan | `207CA` | LWPOLYLINE ACI4 | (362,25630)→(609,26232) | — | L=650 mm, Azimut 67.7° |
| Stiegenhauspfeil rot (Süd-Lauf) | `20782` | LWPOLYLINE ACI1 | Spitze (1792, 26414) | — | zeigt **180° West** |
| Stiegenhauspfeil rot (Nord-Lauf) | `20783` | LWPOLYLINE ACI1 | Spitze (3773, 27904) | — | zeigt **0° Ost** |
| graue Originale | `1FDC9` / `1FDCC` | LWPOLYLINE Layer 06-SYM | Spitzen (1792,26414) / (3768,27904) | — | rote Pfeile decken sie exakt |
| Labels | `206D7` „(A)", `20704` „(B)", `206D9`/`20781` „(DG)", `207EE` „(DG/Podest)" | MTEXT ACI3 | — | — | — |

**Geometrische Prüfung:**
1. **„direkt von vorne … (A) mit Pfeil nach rechts"** — Person 206D8 → A: Vektor (33, 850), Distanz **851 mm**, Sicht-Azimut 87.8°. A ist landscape (Längsachse O-W, bbox 637×320); frontal = Sicht senkrecht zur Längsachse (90°): Abweichung nur **2.2° → exakt frontal** ✓. Welt-Pfeil 359.87° = rechts ✓.
2. **„vor der Stiege, Pfeil direkt zur Stiege"** — erste Setzstufe des Süd-Laufs bei x≈1789; A-Zentrum 667 → **1122 mm vor der Stiege**; quer zur Laufachse (grauer Stiegenpfeil y=26414) nur **23 mm** versetzt = **achsmittig zum Lauf**. Pfeil 0° = exakt Laufrichtung des Abstiegs ✓.
3. **Türkise Sichtlinie** vorhanden (`207CA`, 650 mm, skizziert vom Personenbereich Richtung A) ✓.
4. **„(B) … an der Wand"** — B-Nordkante y≈28497 liegt auf der Stiegenhaus-Nordwand (Wandlinie y≈28493–28514), **561 mm** westlich der Ostwand (x≈5258) → wandbündig ✓. Welt-Pfeil 179.42° = links ✓.
5. **Blickwinkel Podest-Person → B**: Vektor (569, 522), **772 mm**, Azimut 42.5° → **47.5° von der Frontalen** (halb-schräg von unten). PDF sagt nur „sieht" — Präzisierung: kein Frontal-Blick.
6. **Bewegung vs. Stiegenhauspfeil** (U-Stiege, zwei Läufe O-W): Süd-Lauf-Pfeil 180° (West) vs. grüne Bewegungs-Pfeile `20755/20756/20757` Azimut 359.87° (Ost) → **Differenz 179.87° = exakt entgegen** ✓. Nord-Lauf-Pfeil 0° (Ost) vs. Bewegungs-Pfeile `20758/20759/2075A` Azimut 179.87° (West) → entgegen ✓. Abknick-Pfeil `2075B` (805, 27435) Azimut 269.87° (Süd) verbindet Nord-Route mit der A-Achse.
7. **Fluchtweg-Verlauf**: Podest (Ost) → West entlang Nord-Lauf → Süd-Knick bei x≈805 → (A) → Ost in den Süd-Lauf (Abstieg Richtung 4. OG). Raum: kleines rechteckiges STGH (4.86 m², Stempel `1F8F5`), kein Gang ✓ („keinen zusätzlichen Gang").

**Status: bestätigt + präzisiert** (851 mm Frontalsicht 2.2°; A 1122 mm vor der Stiege, achsmittig 23 mm; B wandbündig; Podest-Blick auf B 47.5° schräg).

Bild: `DG-01.png` (links PDF S. 39, rechts DXF-Crop −1.9…6.6 m / 24.6…29.4 m).

---

## DG-02 — „Dachgeschoß – Top 27, Top 28 und Flachdach" (PDF S. 40–41)

**PDF-Aussagen:** Stiegenhaus DG mit Top 27, Top 28 und begehbarem Flachdach. Wer das Flachdach verlässt, sieht zuerst **(B) mit Pfeil nach unten** (geradeaus weiter), danach **(A) mit Pfeil nach links** (nach links zur Stiege, hinunter ins 4. OG). (A) grundsätzlich **vor der Stiege**, Pfeil **auf die Stiege**. Wegen der **blau markierten Lichtkuppel** muss (A) **etwas nach unten Richtung Top 28 versetzt** werden; die Ausrichtung bleibt gleich.

**DXF-Fakten:**

| Objekt | Handle | Block | Sichtbares Zentrum | Rotation | Welt-Pfeil/Blick |
|---|---|---|---|---|---|
| (B) | `20864` | RIVO-SIBEL-ARR-down | (36956, −59) | 269.71° | **179.71° ≈ West** (= entgegen der Ost-Bewegung; Schild portrait = quer zum Gang) |
| (A) | `2083F` | RIVO-SIBEL-ARR-left | (40303, −1717) | 359.42° | **179.42° ≈ West (links, zur Stiege)** |
| Lichtkuppel blau | `20906` (außen) / `20908` (innen) | LWPOLYLINE ACI5 | Box (39624…40930, −1425…−125) | — | 1306×1300 mm Doppelrahmen |
| Person „(DG)" Flachdach-Route | `20904` / `20902` | 750298750 | (35562, −41) / (38655, −49) | 2.89 (xs=−4.007) | Blick **2.89° = Ost** |
| Person „(DG)" Top 27 | `208D8` | 750298750 | (39031, 840) | 272.75 (xs=−4.007) | Blick **272.75° = Süd** |
| Person „(DG)" Top 28 | `2083C` | 750298750 | (40577, −2544) | 92.75 (xs=−4.007) | Blick **92.75° = Nord** (zu A) |
| Personen „(DG)" auf Stiege | `20900` / `208FE` | 750298750 | (36363, −1703) / (39387, −1746) | 356.85 (xs=+4.007) | Blick **176.85° = West** (Abstieg) |
| Sichtlinie Top 28 → A | `208B4` | LWPOLYLINE ACI4 | (40306,−2455)→(40302,−1618) | — | **837 mm**, Azimut 90.3° |
| Sichtlinie Top 27 → A-Bereich | `208DA` | LWPOLYLINE ACI4 | (39302,751)→(40305,−1299) | — | **2282 mm**, Azimut 296.1° |
| Stiegenhauspfeil rot | `20812` | LWPOLYLINE ACI1 | Spitze (39123, −1575) | — | zeigt **0° Ost** |
| graues Original | `1FAA5` | LWPOLYLINE Layer 06-SYM | (35755,−1575)→(39123,−1575) | — | rote Nachzeichnung deckungsgleich |
| Labels | `20865` „(B)", `20840` „(A)", `2083D/208D9/208FF/20901/20903/20905` „(DG)", `2092B` „Lichtkuppel" (ACI 5) | MTEXT | — | — | — |

**Geometrische Prüfung:**
1. **„sieht zunächst (B) mit Pfeil nach unten … geradeaus"** — Person 20904 → B: Vektor (1394, −18), **1394 mm**, Azimut −0.7°. B portrait (318×631, Längsachse N-S, quer zum O-W-Gang) → Sicht **0.7° von der Frontalen = frontal** ✓. Welt-Pfeil 179.71° = exakt **entgegen** der Bewegungsrichtung (grüne Pfeile `208AE/208AF/208B0`, Azimut 359.87° Ost) → Down-RZ-Regel „Pfeil entgegen dem Fluchtweg" vektoriell belegt (Δ=179.8°).
2. **„danach (A) mit Pfeil nach links … zur Stiege"** — A-Welt-Pfeil 179.42° (West); Ost-Kante des Stufenfelds x≈39435 → A-Zentrum **868 mm vor der Stiege**, Pfeil zeigt exakt auf sie ✓.
3. **Lichtkuppel-Versatz quantifiziert:** Kuppel-Südkante y=−1425. Stiegen-/Gang-Achse (roter Pfeil) y=−1575. A-Zentrum y=−1717 → **142 mm südlich der Stiegenachse** und **292 mm südlich der Kuppelkante**; Richtung Top 28 (Top-Label `1FA04` bei (40380, −2175), 458 mm südlich von A) ✓. Gegenprobe: säße A auf der Stiegenachse, läge seine Oberkante bei y≈−1413 → **12 mm Überlappung mit der Kuppel** — der Versatz ist geometrisch erzwungen. Ausrichtung blieb unverändert (Rotation 359.42° identisch mit allen anderen ARR-left im Plan) ✓.
4. **Sichtlinien:** `208B4` (Top 28 → A): 837 mm, 0.3° von der Frontalen → frontal ✓, schneidet keine Wand (freier Vorbereich Top 28). `208DA` (Top 27 → A-Bereich): 2282 mm, **kreuzt die Lichtkuppel-Box** (Eintritt bei ca. (39730, −125)) und endet 418 mm nördlich des A-Zentrums **innerhalb** der Kuppel-Box — vermutlich Blick auf die ursprünglich vorgesehene (unversetzte) A-Position; Winkel zur A-Frontalen 26.1°.
5. **Bewegung vs. Stiegenhauspfeil:** Pfeil 0° (Ost, rot `20812` über grauem `1FAA5`); Personen 20900/208FE Blick 176.85°, grüne Pfeile `208B1/208B2/208B3` Azimut 179.87° (West) → **entgegen (Δ≈180°)** ✓ (PDF S. 41).
6. **Route:** Flachdach-Ausstieg (x≈33.9–34.2 m, West) → Ost durch STGH 11.11 m² (Stempel `1FA24`) → (B) → weiter Ost → Süd-Knick (`2088B`, Azimut 269.87°, x=40174) → (A) → West in den Stiegenlauf (Stufen x 36035…39395, y −955…−2155) Richtung 4. OG. Raumform: rechteckiges Stiegenhaus mit Gang-Schenkel → L-artiger Verlauf um die Kuppel.

**Status: bestätigt + präzisiert** (Versatz 142/292 mm, Kollisionsnachweis 12 mm, Frontalitäten 0.3–0.7°, Stiegenhauspfeil-Vektoren).

Bild: `DG-02.png` (links PDF S. 40, rechts DXF-Crop 32.8…42.8 m / −4.2…2.2 m).

---

## Abdeckung (alle Notbeleuchtungs-INSERTs im Modelspace)

| Handle | Block | Zentrum | Zuordnung |
|---|---|---|---|
| `206DC` | RIVO-RZ-ARR_right | (667, 26391) | DG-01 (A) |
| `20705` | RIVO-SIBEL-ARR-left | (4697, 28335) | DG-01 (B) |
| `20864` | RIVO-SIBEL-ARR-down | (36956, −59) | DG-02 (B) |
| `2083F` | RIVO-SIBEL-ARR-left | (40303, −1717) | DG-02 (A) |
| `206D6` | RIVO-SIBEL-ARR-down | (−16047, 28414) | **unerklärt** — grünes Label „(D)" (`206DD`) daneben |
| `206DB` | RIVO-SIBEL-ARR-left | (−17184, 26892) | **unerklärt** — grünes Label „(B)" (`206DA`) daneben |

6 Leuchten gesamt, 4 den PDF-Beispielen zugeordnet, 2 unerklärt. Die zwei unerklärten bilden mit Fluchtwegpfeil `206DF` (Azimut 89.87°→Süd), grüner Polyline `206DE` und Sichtlinie `206E0` (3342 mm) eine abgesetzte Mini-Szene bei x≈−16…−19.3 m — **außerhalb der Westfassade** (Gebäudekante/Achsen bei x≈−12.9 m, MOLLGASSE-Schriftzug bei x=−13.1 m). Das Label „(D)" kommt im DG-PDF-Text gar nicht vor; wirkt wie ein Arbeits-/Kopierrest aus einem anderen Geschoss-Beispiel. Bild: `DG-West-unerklaert.png`.

Antipanikleuchte-RIVO, Aufheller, Spot, Gruppenbatterie-Verteiler: **0 Instanzen** im DG-DXF (das DG kommt in beiden Beispielen ohne Antipanik/Aufheller aus).

---

## Regel-Beobachtungen (Rohstoff Regelbasis)

1. **RZ vor der Stiege statt an der Tür** (DG-01, DG-02): A `206DC` sitzt 1122 mm vor der ersten Setzstufe, quer zur Laufachse nur 23 mm versetzt (achsmittig); A `2083F` 868 mm vor der Stiegen-Ostkante. Pfeil-Azimut jeweils = Abstiegsrichtung des Laufs (0° bzw. 179.4°).
2. **Down-RZ im geraden Verlauf: Pfeil entgegen der Fluchtrichtung, Schild quer zum Gang** (DG-02 B): Welt-Pfeil 179.71° vs. Bewegung 359.87° (Δ=179.8°); portrait-Stellung (Längsachse N-S) macht das Schild für den O-W-Gehenden frontal sichtbar.
3. **Frontalitäts-Regel messbar:** Sichtlinien Person→RZ nahezu senkrecht zur Schild-Längsachse — DG-01 A: 2.2°, DG-02 B: 0.7°, DG-02 A (von Top 28): 0.3° Abweichung von der Frontalen. Gegenbeispiel im selben Plan: Podest-Person→B (DG-01) 47.5° schräg — dort genügt dem Autor Sichtbarkeit, Frontal-Anspruch gilt v. a. für die jeweils „erste" Leuchte beim Verlassen eines Raums.
4. **Abstieg entgegen Stiegenhauspfeil, vektoriell belegt:** DG-02 Pfeil 0° vs. Personenbewegung 179.87° (Δ≈180°); DG-01 Süd-Lauf 180° vs. 359.87°, Nord-Lauf 0° vs. 179.87°. Rote Nachzeichnungen liegen exakt auf den grauen Originalen (`20782`↔`1FDC9`, `20783`↔`1FDCC`, `20812`↔`1FAA5`).
5. **Hindernis-Ausweichregel (Lichtkuppel):** Kuppel 1306×1300 mm; A um 142 mm aus der Stiegenachse nach Süd versetzt (292 mm Abstand Zentrum→Kuppelkante); auf der Achse hätte das Symbol (325 mm tief) die Kuppel um ca. 12 mm überlappt. **Nur die Position wird verschoben, die Rotation bleibt** (359.42° wie alle ARR-left des Plans).
6. **Wand-RZ am Podest** (DG-01 B): Oberkante liegt auf der Wandlinie (y≈28497 vs. Wand 28493–28514), 561 mm zur Raumecke; Pfeil = Weiterweg-Richtung des Ankommenden (179.4° West).
7. **Blockkonventionen:** Fluchtwegpfeil `4444444` Welt-Azimut = 180° + rot; Mensch `750298750` Blick-Azimut = rot (xscale<0) bzw. rot+180° (xscale>0); RZ-Welt-Pfeil = Basis (down 270/left 180/right 0) + rot. Alle 9 Menschen sind exakt in Bewegungs-/Blickrichtung der Route rotiert.
8. **Layer-Semantik:** komplettes Erklärungs-Overlay auf Layer `0` (Labels ACI 3, Stiegenhauspfeil ACI 1, Sichtlinien ACI 4, Hindernis ACI 5) — Erscheinungsbild, nicht Layername, trägt die Bedeutung.

## Offene Fragen

1. West-Cluster `206D6`/(D) + `206DB`/(B) bei x≈−16…−19.3 m liegt außerhalb der Gebäudekante (x≈−12.9 m) und wird im DG-PDF (S. 39–41) nicht erwähnt; „(D)" existiert im DG-Text nicht → Kopier-/Arbeitsrest oder verlorenes Mini-Beispiel? (Owner fragen.)
2. Höhenlage PODEST (DG-01): Kote „FOK PODEST = +12.09" vs. „FOK STGH = +13.45", aber grüner Fluss + Nordlauf-Stiegenpfeil (aufwärts Ost) implizieren, dass die „DG/Podest"-Person von oben (Dachausstieg-Podest?) nach West herabsteigt. Nicht aus dem DXF allein auflösbar.
3. Sichtlinie `208DA` endet 418 mm nördlich des A-Zentrums **in** der Lichtkuppel-Box — Blick auf die ursprüngliche (unversetzte) A-Position? Reine Vermutung.
4. Wand-Schnitt-Prüfung der Sichtlinien erfolgte nur gegen die Kuppel-Box und die Stiegenhaus-Umrisse; vollständige Wand-Topologie wurde nicht extrahiert.
