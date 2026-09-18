# Parallel-Abgleich PDF ↔ DXF — Mollgasse Notbeleuchtungserklärung, Geschoss EG

**Quellen:**
- PDF-Erklärtext Seiten 1–13 (`Notbeleuchtungen zeichnen`, Kapitel „1) Erdgeschoss-Notbeleuchtungsplanung")
- DXF: `knowledge/Pläne zeichnen Wissen/Mollgasse-Notbeleuchtungserklärung/WHA_MOL_EG_Notbeleuchtung_Erklärung.dxf`
  (AC1032, INSUNITS=4 → **mm**; alle Erklärungs-Entities im **Modelspace**, Layout1 = nur Plankopf/Texte, keine Symbole)

**Konventionen (in dieser DXF gemessen):**
- Notbeleuchtungs-Blöcke: `RIVO-SIBEL-ARR-down` (Pfeil lokal (0,−1), Basis 270°), `RIVO-SIBEL-ARR-left` (Basis 180°), `RIVO-RZ-ARR_right` (Basis 0°), `Antipanikleuchte-RIVO`, `Aufheller Notbeleuchtung`, `Spot Notbeleuchtung`, `Gruppenbatterie-Verteiler`. Welt-Pfeil = Basis + INSERT-Rotation.
- **Achtung Einfügepunkt ≠ sichtbare Lage:** Die Blockgeometrie hat große Basispunkt-Offsets; die INSERT-Einfügepunkte liegen z. T. > 1 km entfernt. Alle Positionen unten sind **bbox-Zentren der virtuellen Entities** (sichtbare Lage).
- Menschensymbol Block `750298750` (nested `9809550`): **bei rot=0 und xscale>0 blickt der Läufer nach LINKS (Welt 180°)**; xscale<0 spiegelt → Blick rechts (Welt 0°). Formel: Blick = 180°+rot (xs>0) bzw. rot (xs<0). Verifiziert an EG-05: obere (UG)-Reihe rot 0/xs + = Blick West = Stiegenpfeilrichtung; untere (1OG)-Reihe rot 0/xs − = Blick Ost = entgegen.
- Fluchtweg = hellgrüne LWPOLYLINEs (true_color 0x21DF37, ACI 102) + Pfeilblock `4444444`; Sichtlinien = ACI 4 (cyan); rot nachgezeichnete Stiegenhauspfeile = ACI-1-LWPOLYLINEs (Linie + separates Pfeilspitzen-Polygon); blaue Hatch+Linien (ACI 5, Handles < 0x20000) sind **Original-Plan-Annotationen** (Dämmungsschalter-Leader), keine Erklärungs-Markierung. Türkise Dreiecke/Schnittmarken (S5, S9, S12) = Architektur-Schnittführung, NICHT Sichtlinie.
- Erklärungs-Entities haben Handles ≥ ~0x20200; kleinere Handles = originaler Architekturplan.

**Leuchten-Labels im DXF (grüne MTEXTe):** (A) 15493/68191 · (B) 15593/66431 · (C) 22672/66512 · (D) 11623/66745 · (E) 47933/41603 · (F) 55811/41990 · (G) 55830/46007 · (H) 59539/45482 · (A) 53547/30372 · (B) 59626/35067 · (1) 57043/30462 · (A) 59350/48930. Dazu Personen-Labels (UG)/(1OG)/(KIWA)/(1).

---

## EG-01 — Haupteingang EG (PDF S. 1)

**PDF:** Haupteingang; RZ mit Pfeil nach unten bei der Tür, mittig zum Türflügel, so rotiert, dass es entgegen der Türrichtung „in den Raum hinein" zeigt. Grüne Fluchtlinie + rotierte Menschensymbole.

**DXF:** Leuchte `20240` `RIVO-SIBEL-ARR-down` @ (11513, 66599), rot 90° → **Welt-Pfeil 0° = Ost = ins Rauminnere** (Ausgang liegt im Westen: grüne Linie `2031A` (11402,66569)→(6480,66571) führt nach Westen ins Freie Richtung MOLLGASSE). Nächste Türachse `1FD36` @ (10674, 66573): Δy = **26 mm** (praktisch mittig zur Tür), 840 mm raumseitig vor der Türachse. Label (D) `20F4E`. Status: **präzisiert** — „Pfeil nach unten" = Symboltyp; die Rotation 90° macht daraus Welt-Ost (in den Raum); „mittig" stimmt auf 26 mm.

Bild: `EG-01.png`

## EG-02 — Müllraum 27.61 m² (PDF S. 2)

**PDF:** Müllraum-Beispiel „zu 99 % fast immer gleich"; Notleuchte bei der Tür, Pfeil in den Raum; wäre der Müllraum L-förmig, zusätzlich Antipanikleuchte.

**DXF:** Raumstempel `1F275` MÜLLRAUM 27.61m2 @ (9351, 63611). Leuchte `20286` ARR-down @ (10284, 64443), rot 0 → **Welt-Pfeil 270° = Süd = in den Müllraum** (Raum liegt südlich der Tür). Türachse `1FD33` @ (10288, 65356): Δx = **4 mm** (exakt in der Türachse), 913 mm raumseitig. Keine Antipanik im Raum (rechteckiger Grundriss) ✓. Status: **bestätigt** (+ Maße).

Bild: `EG-02.png`

## EG-03 — Fahrradraum / KIWA 50.05 m² (PDF S. 3)

**PDF:** Auch im Fahrradraum gilt die Tür-Platzierungs-/Rotationsregel; Definition „Allgemeinbereiche".

**DXF:** Raumstempel `1FA86` „FAHRRADRAUM / KIWA" 50.05m2 @ (14798, 72624). Leuchte `202A9` ARR-down @ (15948, 70780), rot 180° → **Welt-Pfeil 90° = Nord = in den Raum** (Raum nördlich der Tür). Tür `200CC` TÜR-BLOCKZARGE-100_STUMPF @ (15957, 70045): Δx = **9 mm** (mittig), 735 mm raumseitig nördlich. Status: **bestätigt** (+ Maße). Hinweis: dieselbe Leuchte dient auch als Innenhof-Beispiel EG-04/EG-14 (eine Tür, drei PDF-Erklärungen).

Bild: `EG-03.png`

## EG-04 — Innenhof zwischen zwei Gebäuden (PDF S. 4)

**PDF:** Tür-Notleuchte, damit Menschen im Innenhof den Weg zum Hauptausgang erkennen; Pfeil „in den Innenhof".

**DXF:** Gleiche Leuchte `202A9` (Welt-Pfeil 90° Nord). Der Bereich nördlich der F15-Tür ist der Zugang Innenhof/Gehweg (GEHWEG-Stempel `1F9AA` @ 22709/73687; TERRASSE/EIGENGARTEN TOP 2 östlich). Person `20C29` @ (15834, 71500), Blick 270° (Süd, zur Tür); Person `20C28` @ (12137, 72095), Blick 0°. Grüne Linie `20364` (15879,70682)→(15878,68327) führt durch die Tür südwärts ins Gebäude. Status: **präzisiert** — „in den Innenhof" = Welt-Nord (90°); identisch mit der EG-03-Leuchte, PDF erklärt dieselbe Platzierung aus zwei Raum-Perspektiven (Fahrradraum-innen vs. Innenhof).

Bild: `EG-04.png`

## EG-05 — Stiegenhaus EG links + Stiegenhauspfeil (PDF S. 5–6)

**PDF:** Stiegenhauspfeil rot nachgezeichnet, zeigt „nach links"; UG-Menschen gehen in Pfeilrichtung hinauf, OG-Menschen entgegen hinunter. (A) „Pfeil nach links" vor den UG-Ankömmlingen; danach (B) „Pfeil nach links"; OG-Ankömmlinge sehen (C) „Pfeil nach links"; alle enden bei (D) „Pfeil nach unten" an der Haupteingangstür.

**DXF:**
- Stiegenhauspfeil rot: `20684` Linie (17013,68301)→(19813,68286) + Pfeilspitze `20685` mit Spitze bei x=17013 → **Richtung 180° (West)** ✓ „links".
- Rote OG-Gegenrichtungs-Visualisierung: `20DE8`/`20DE9` (17057,67843)→(21671,67826), Spitze Ost → 0°.
- (A) = `202EF` ARR-left @ (15868, 68105), rot 90° → **Welt-Pfeil 270° = Süd**. Das Schild hängt vertikal an der Westwand; die von der Stiege (Osten) nach Westen ankommenden UG-Personen sehen die Vorderseite frontal, der Pfeil zeigt aus ihrer Sicht **nach links = Welt-Süd**, Richtung (B). „Pfeil nach links" im PDF = Symboltyp ARR-left + Personensicht, NICHT Welt-links!
- (B) = `20263` ARR-left @ (15838, 66130), rot 0 → **Welt 180° (West)**, 1975 mm südlich von (A); zeigt nach Westen Richtung (D)/Ausgang (grüne Linie `2031D` (15590,66120)→(11675,66121)→nord).
- (C) = `20312` ARR-left @ (22318, 66418), rot ~0 (359.7°) → **Welt ~180° (West)**; hängt am Südost-Gang; OG-Ankömmlinge sehen sie und gehen nach Westen (grüne Linie `20320` (22097,66421)→(15874,66422) zu (B)). Abstand (C)→(B) 6486 mm.
- (D) = `20240` (EG-01), Welt-Pfeil Ost = in den Raum; von (B) 4350 mm.
- Personen: obere Reihe (UG) `20362`/`20363` rot 0, xs +3.32 → Blick 180° (West, in Stiegenpfeilrichtung); untere Reihe (1OG) `20E75`/`20EBC` rot 0, xs −3.32 → Blick 0° (Ost, entgegen). Rote Merktexte `20683`, `20DC5`, `20E0C` im DXF vorhanden.

Status: **präzisiert** — Kernbefund: PDF-Richtungsangaben („links") sind personen-/typbezogen; die Weltrichtung entsteht erst aus Basis+Rotation ((A): left+90° = Süd).

Bild: `EG-05.png`

## EG-06 — Stiegenhaus rechts, Stiegenhauspfeil nach rechts (PDF S. 7)

**PDF:** Gleiche Situation, Stiegenhauspfeil zeigt nach rechts; UG-Menschen gehen in Pfeilrichtung hinauf und sehen (F); 1OG-Menschen entgegen hinunter und sehen (E), danach (F).

**DXF:**
- Stiegenhauspfeil rot `20D09` (49834,40501)→(54314,40501), Pfeilspitze Ost → **0° (Ost/„rechts")** ✓.
- Rote Gegenrichtung `20F99`/`20F9B` (49886,39865)→(54301,39850), Spitze West → 180°.
- (E) = `206C0` RZ-ARR_right @ (48188, 41757), rot 0 → **Welt 0° (Ost)**; am Westende/PODEST (Raumstempel `1F501` PODEST @ 48354/41451). Label `210DB`.
- (F) = `206C3` RZ-ARR_right @ (55936, 41697), rot 0 → **Welt 0° (Ost)**; 7749 mm östlich von (E). Grüne Linie `20756` (48414,41750)→(55693,41748) verbindet.
- Personen: (UG) `207C6` @ (50521,41753) u. a., Blick 0° (Ost = Pfeilrichtung) ✓; (1OG) `20FBE`/`20FE1` @ y≈40080, Blick 180° (West = entgegen) ✓; `21091` (1OG) Blick 90° (biegt zum Gang hoch).

Status: **bestätigt** (+ Koordinaten/Winkel).

Bild: `EG-06.png`

## EG-07 — Weiterer Verlauf: (F) → (H) (PDF S. 8)

**PDF:** Ab (F) sehen UG- und 1OG-Menschen die Notleuchte (H); beide Gruppen flüchten ab hier in dieselbe Richtung.

**DXF:** (H) = `2070A` ARR-down @ (59671, 45739), rot 270° → **Welt-Pfeil 180° = West = ins Rauminnere**; die Hauptausgangstür liegt östlich (Türöffner `E901` @ (60036,45651), **375 mm** entfernt; MTEXT `209B8` „HAUPTAUSGANG" @ 62720/45929). Weg (F)→(H): grüne Linien `20759` (56167,41696)→(58899,41696)→(58899,45677) und `20758` (56129,45688)→(59541,45688); Distanz (F)→(H) 5503 mm Luftlinie. Personen (1OG)+(UG) nebeneinander: `2111F`/`21142` @ (57632/42128, 57594/42291), `21166`/`21167` @ (58133/42998), Blick 90° Nord (`2082F`), dann `2118B`/`2118C` @ (60859/46051) Blick 0° Ost Richtung Ausgang. Status: **bestätigt** (+ Maße; (H)-Weltrichtung präzisiert: West = entgegen der Fluchtrichtung Ost, Typregel „down = geradeaus/Ausgang hier").

Bild: `EG-07.png`

## EG-08 — KIWA 7.23 m² (PDF S. 9)

**PDF:** Menschen im KIWA sehen beim Verlassen direkt (G); beim Links-Rechts-Schauen (G) und (H); (H) bei der Hauptausgangstür.

**DXF:** Raumstempel `1F5FD` KIWA 7.23m2 @ (55054, 44051), Tür `1FBF0` TÜR-90 @ (56369, 44280). (G) = `206E7` RZ-ARR_right @ (55904, 45693), rot 0 → **Welt 0° (Ost)**, 1487 mm nördlich der KIWA-Tür am Gang; (H) = `2070A` 3767 mm östlich von (G). (KIWA)-Personen: `20852` @ (56344, 44588) Blick 0°, `2080C` @ (57895, 45672) Blick 0°. Sichtlinien von der Tür: (G) liegt 465 mm westlich / 1413 mm nördlich der KIWA-Türachse (Distanz 1487 mm), (H) 3610 mm nordöstlich — beide vom Türpunkt aus frei entlang des Gangs. Status: **bestätigt** (+ Maße).

Bild: `EG-08.png`

## EG-09 — KIWA-Person sieht „(D) Pfeil rechts" (PDF S. 10 oben)

**PDF:** „Person vom KIWA sieht Notleuchte **(D)** mit Pfeil nach rechts Richtung Hauptausgang; nahe dem Hauptausgang immer eine Notleuchte mit Pfeil nach unten über der Haupteingangstür + Notleuchte (E) siehe Bild."

**DXF:** Im Screenshot der Seite 10 heißen die Leuchten (D)/(E)/(C) — im aktuellen DXF stehen dort die Labels **(G)** `20D5C` und **(H)** `20DA2`; (C)/(D)/(E)-Texte existieren im rechten Stiegenhaus nicht. Geometrie identisch mit EG-08: (G)=`206E7` Welt-Pfeil Ost („rechts") ✓, (H)=`2070A` an der Hauptausgangstür. Status: **widerspruch (nur Beschriftung)** — PDF-S.10-Screenshot zeigt einen älteren Label-Stand ((D)/(E)); DXF-Wahrheit: (G)/(H). Geometrische Aussage selbst bestätigt.

Bild: `EG-09.png`

## EG-10 — U-förmiger Fahrradraum 73.03 m²: Antipanik (A), RZ (B) (PDF S. 10 unten + S. 11 oben)

**PDF:** Mensch (1) sieht (B) nicht (Mauer dazwischen); ohne Zusatz stünde er im Dunkeln → Antipanikleuchte (A); sobald (B) sichtbar wird, orientiert er sich daran.

**DXF:** Raumstempel `1F228` FAHRRADRAUM 73.03m2 @ (55454, 30551). (B) = `2070C` ARR-down @ (59722, 34557), rot 270° → **Welt 180° (West)**, am PODEST/Nordausgang des Raums (Raumstempel `1FE75` PODEST @ 58354/34191); Fluchtweg führt östlich hinaus (`20995` (59767,34571)→(63950,34571)). (A) = `20752` `Antipanikleuchte-RIVO` @ (53862, 30113) im Süd-Arm des U (630×178 mm Symbol). Mensch (1) = `21261` @ (57073, 30067), Blick 180° (West, Richtung (A)/Tür), Label `212CA`. Abstand Mensch(1)→(B) = Luftlinie 5213 mm, aber der Sichtstrahl quert den U-Innensteg (Wand zwischen Süd-Arm y≈30070 und Nord-Arm y≈34560) → Sicht blockiert ✓. Abstand (A)→(B) 7354 mm; (A)→Mensch(1) ≈ 3211 mm. Grüner U-Verlauf `2075A` (58973,30073)→(52039,30074)→(52039,34582)→(59557,34581). Status: **bestätigt** (+ Maße).

Bild: `EG-10.png`

## EG-11 — Geschäftslokal mit Sichtlinie (PDF S. 11 Mitte)

**PDF:** Geschäftslokal = Allgemeinbereich; eine Tür-Notleuchte genügt, weil die Person sie vom anderen Raumende sieht; türkise Linie = Sichtverbindung.

**DXF:** Tür-Leuchte = `20948` ARR-down @ (60934, 51510), rot 270° → **Welt 180° (West) = in den Raum**; Fluchtweg östlich hinaus (`20990` (60990,51436)→(62571,51436)). **Einzige Erklärungs-Sichtlinie der EG-DXF:** `212EE` (ACI 4) von (52194, 54687) zur Leuchte (60763, 51500): **Länge 9143 mm**, Richtung 339,6°; das Schild steht vertikal (Längsachse N-S), Front-Normale West → **Winkel zur Vorderseite 20,4° = nahezu frontal**, keine Wand im Strahl (offener Verkaufsraum). Türkiser MTEXT `21311` „Sichtwinkel zur Notleuchte, daher ist eine Antipanikleuchte nicht unbedingt notwendig…" @ (52794, 54428). Person `212ED` @ (52112, 54463), Blick 0° (Ost). Status: **bestätigt** (+ Sichtlinien-Metrik).

Bild: `EG-11.png`

## EG-12 — Zweiter Müllraum MÜLL 34.47 m² mit „(A)" (PDF S. 11 unten – S. 12 oben)

**PDF:** Erneut Müllraum; Tür-Notleuchte „Pfeil nach unten", Label (A); weder U- noch L-förmig, keine Sichtwand → keine Antipanik/kein Aufheller nötig (vorbehaltlich Lichtberechnung).

**DXF:** Raumstempel `1F17F` MÜLL 34.47m2 @ (56054, 49191). (A) = `21312` ARR-down @ (59789, 48584), rot 270° → **Welt 180° (West) = in den Müllraum** (Tür an der Ostwand). Türachse `1FD00` @ (60717, 48561): Δy = **22 mm** (mittig zur Tür), 929 mm raumseitig. Label (A) `21335` @ (59350, 48930). Keine weitere Leuchte im Raum ✓. Personen `21336` (53935,48615, Blick Ost), `208DE` (58260,48614, Blick Ost) — frontal auf die West-Vorderseite von (A). Fluchtweg hinaus: `2075C`/`2075D`/`20993` entlang y≈48600 nach Osten. Status: **bestätigt** (+ Maße). Hinweis: PDF nennt „Pfeil nach unten" — wieder Typbezeichnung; Weltrichtung West.

Bild: `EG-12.png`

## EG-13 — Innenhof mit nur einem Gehweg (PDF S. 12)

**PDF:** Nur ein möglicher Fluchtweg über den Gehweg zur Tür ins EG-Stiegenhaus; Tür-Notleuchte, Pfeil entgegen der Türflügel-Richtung (in den Hof).

**DXF:** Leuchte `21359` ARR-down @ (47774, 47342), rot 180° → **Welt 90° = Nord = in den Innenhof** (Gebäude südlich, Hof nördlich; F11-Tür, Türachse `1FD12` @ (48167, 47884), 670 mm entfernt). Grüner Weg: `20550` … (43413,49854)→(48066,49853)→(48066,47306) von Norden zur Tür, danach `20755` (47774,47134)→(47773,41755) südwärts ins Stiegenhaus zu (E). Personen `20573`/`205C4` (43583/54770, 43583/51520) Blick 270° (Süd), `205C5` (45248/49822) Blick 0°, `205C6` (47991/48880) Blick 270° — folgen dem Gehweg zur Tür ✓. Status: **bestätigt** (+ Vektoren).

Bild: `EG-13.png`

## EG-14 — Wieder Innenhof + Person vom Gehweg sieht (C) (PDF S. 13)

**PDF:** Bild 1: „wieder im Innenhof, dieselben Regeln." Bild 2: Person vom Gehweg gelangt in den Gang-/Stiegenhausbereich EG und sieht (C) mit Pfeil nach links → geht nach links.

**DXF:** Bild 1 = derselbe Türpunkt wie EG-03/04 (`202A9`, Welt-Pfeil Nord, TERRASSE/EIGENGARTEN TOP 2/3 östlich; Gehweg-Fluchtpfeile Richtung West zur Tür). Bild 2 = vertikaler Gang x≈22400: grüne Linie `2031E` (22403,72453)→(22418,66517) südwärts; Person `2137D` @ (22482, 70452), Blick 270° (Süd); am Gangende (C) = `20312` @ (22318, 66418), Welt-Pfeil ~180° (West) → Person erkennt Linksabbieg nach Westen ✓ (STGH 34.25m2-Stempel im Bild; die türkise horizontale Linie dort ist die S5-Schnittführung des Architekturplans, keine Sichtlinie). Status: **bestätigt**.

Bild: `EG-14.png`

---

## Abdeckung (alle 26 Notbeleuchtungs-INSERTs im Modelspace)

**Beispielen zugeordnet (15):**
| Handle | Block | bbox-Zentrum | Welt-Pfeil | Beispiel |
|---|---|---|---|---|
| 20240 | ARR-down (rot 90) | 11513, 66599 | 0° Ost | EG-01/05 „(D)" |
| 20286 | ARR-down (rot 0) | 10284, 64443 | 270° Süd | EG-02 |
| 202A9 | ARR-down (rot 180) | 15948, 70780 | 90° Nord | EG-03/04/14 |
| 202EF | ARR-left (rot 90) | 15868, 68105 | 270° Süd | EG-05 „(A)" |
| 20263 | ARR-left (rot 0) | 15838, 66130 | 180° West | EG-05 „(B)" |
| 20312 | ARR-left (rot 359.7) | 22318, 66418 | 179.7° West | EG-05/14 „(C)" |
| 206C0 | RZ-ARR_right (rot 0) | 48188, 41757 | 0° Ost | EG-06 „(E)" |
| 206C3 | RZ-ARR_right (rot 0) | 55936, 41697 | 0° Ost | EG-06 „(F)" |
| 206E7 | RZ-ARR_right (rot 0) | 55904, 45693 | 0° Ost | EG-08/09 „(G)" |
| 2070A | ARR-down (rot 270) | 59671, 45739 | 180° West | EG-07/08/09 „(H)" |
| 2070C | ARR-down (rot 270) | 59722, 34557 | 180° West | EG-10 „(B)" |
| 20752 | Antipanikleuchte-RIVO | 53862, 30113 | — | EG-10 „(A)" |
| 20948 | ARR-down (rot 270) | 60934, 51510 | 180° West | EG-11 |
| 21312 | ARR-down (rot 270) | 59789, 48584 | 180° West | EG-12 „(A)" |
| 21359 | ARR-down (rot 180) | 47774, 47342 | 90° Nord | EG-13 |

**Symbol-Legende am linken Blattrand (8, x≈1080–1140, y≈65275–68014; nicht Teil eines Beispiels):**
`20215` Aufheller @ (1080,67157) · `20216` Spot @ (1080,65275) · `20217` Gruppenbatterie-Verteiler @ (1125,65742) · `20218` RZ-ARR_right @ (1142,67451) · `20219` ARR-down @ (1142,68014) · `2021B` ARR-left @ (1133,66256) · `2021C` ARR-left gespiegelt (xs −25.2, rot 180 → wirkt als Rechts-Pfeil) @ (1133,66479) · `2021D` Antipanikleuchte @ (1098,66856). Dazu Legenden-Mensch `20359` @ (1679,67680) und Legenden-Fluchtpfeil `20332`.

**Unerklärt (3):**
- `202CC` ARR-down @ (22341, 61637), Welt 270° Süd — Südausgang linkes Stiegenhaus zum GEHWEG (Stempel `205EE` @ 21953/60301); liegt auf der grünen Linie `2031F`/`20550`, aber in keinem PDF-Seiten-1-13-Beispiel behandelt.
- `2137C` ARR-down @ (22285, 61595), Welt 270° Süd, xscale 41.2 — **Duplikat** 70 mm neben `202CC` (gleicher Türpunkt, zwei RZ übereinander; vermutlich Nachzeichnungs-Versehen).
- `2072F` Antipanikleuchte @ (50928, 37779), vertikal — Zwischenbereich Fahrradraum↔Stiegenhaus rechts; im PDF-EG-Text nicht erwähnt.

---

## Regel-Beobachtungen (geometrisch belegt, Rohstoff für Regelbasis)

1. **Tür-RZ sitzt in der Türachse, raumseitig versetzt:** Querabweichung zur Türachse 4–26 mm (EG-01: 26 mm, EG-02: 4 mm, EG-03: 9 mm, EG-12: 22 mm); Längsversatz ins Rauminnere 735–929 mm (840/913/735/929 mm). → Regel: RZ mittig zur Tür (Toleranz < 30 mm), ca. 0,7–0,95 m vor der Tür im Raum.
2. **Welt-Pfeilrichtung = Symbol-Basis + INSERT-Rotation; PDF-Sprache ist typ-/personenbezogen.** „Pfeil nach unten/links" bezeichnet den Blocktyp bzw. die Sicht der ankommenden Person, nie die Weltrichtung (EG-01: „unten"→Welt-Ost; EG-05 (A): „links"→Welt-Süd; EG-07 (H)/EG-12 (A): „unten"→Welt-West).
3. **Tür-RZ-Pfeil zeigt immer in den Raum hinein = entgegen der Fluchtrichtung durch die Tür** (EG-01 Ost vs. Flucht West; EG-02 Süd; EG-03/04 Nord; EG-07 West vs. Flucht Ost; EG-11 West; EG-12 West; EG-13 Nord). 7/7 Beispiele konsistent.
4. **Stiegenhauspfeil-Konvention:** Architekt-Pfeil (rot nachgezeichnet: `20684`→180°, `20D09`→0°) = Laufrichtung der Stiege nach oben; UG-Personen bewegen sich IN Pfeilrichtung (Blick 180° bei Pfeil 180°, Blick 0° bei Pfeil 0°), OG-Personen ENTGEGEN (Blick 0° bzw. 180°). Menschensymbol-Rotationen im DXF bestätigen das paarweise (EG-05/EG-06).
5. **Nach-Stiege-RZ steht am Austrittspunkt „vor der Stiege", nicht in Gangmitte:** (A) `202EF` hängt an der Wand 1975 mm vor (B); (E) `206C0` am Podest-Westende; Pfeil zeigt jeweils die Weiterlaufrichtung der gerade Angekommenen.
6. **Sichtkette lückenlos:** Abstände aufeinanderfolgender RZ im Fluchtweg 1975–7749 mm ((A)→(B) 1975, (B)→(D) 4350, (C)→(B) 6486, (E)→(F) 7749, (F)→(H) 5503, (G)→(H) 3767); jede Person sieht vom Erreichen einer Leuchte die nächste.
7. **Frontalitäts-Regel messbar:** Die einzige EG-Sichtlinie (`212EE`, 9143 mm) trifft die Schild-Vorderseite unter 20,4° zur Normalen → „von vorne erkennbar"; Schilder werden so rotiert (ggf. vertikal an die Wand), dass ankommende Personen die Breitseite sehen (EG-05 (A) vertikal für West-Ankömmlinge).
8. **Antipanik nur bei Sichtblockade:** U-Raum EG-10: Mensch(1)→(B) 5213 mm Luftlinie, aber wandgeblockt → Antipanik `20752` im abgeschatteten Arm (3211 mm vor der Person); rechteckige Räume (EG-02: 27,6 m², EG-12: 34,5 m²) bekommen bewusst KEINE Antipanik.
9. **Ein Tür-RZ kann mehrere Rollen erklären:** `202A9` bedient Fahrradraum-Regel (EG-03), Innenhof-Regel (EG-04) und Wiederholung (EG-14) — Platzierung identisch, nur die Erzählperspektive wechselt.
10. **Menschensymbol-Konvention:** Block `750298750`, Blick = 180°+rot (xscale>0) bzw. rot (xscale<0); der Autor rotiert jedes Symbol in die lokale Fluchtrichtung (52 Instanzen, stichprobenhaft alle konsistent mit den grünen Linien).
11. **Label-Drift möglich:** PDF-S.10-Screenshot nennt (D)/(E)/(C) im rechten Stiegenhaus; aktueller DXF-Stand labelt (G)/(H) — bei Regelextraktion aus PDF-Text die Buchstaben IMMER gegen die DXF-Labels verifizieren.

## Offene Fragen

1. `2072F` (Antipanikleuchte @ 50928/37779): Zweck unklar — Gang/Rampe zwischen Fahrradraum und rechtem Stiegenhaus? Im PDF-EG-Kapitel nicht erklärt.
2. `202CC`+`2137C`: Doppeltes RZ am Süd-Ausgang des linken Stiegenhauses (70 mm Versatz, unterschiedliche Skalierungen 25.2 vs. 41.2) — Absicht (Korrektur vergessen zu löschen?) oder bewusste Zweifach-Platzierung? Das zugehörige Tür-Beispiel fehlt im PDF.
3. PDF S. 10 oben nennt „(D)"/„(E)" im rechten Stiegenhaus (alter Label-Stand) — sollte der PDF-Text auf (G)/(H) korrigiert werden?
4. Die Symbol-Skalierungen variieren stark (xscale 25.2 / 36.1–36.9 / 41.2 / 52.5–54.4): Bedeutung (Darstellungsgröße vs. Symbolklasse) unklar; kein erkennbares System pro Symboltyp.
5. Warum trägt nur `20216` (Spot, Legende) den Layer `din_SIBEL_10_emergency_lighting`, alle anderen Notbel-Symbole Layer `0`?
6. „FREIHEIT"/„KEINE FREIHEIT"-Merktexte (`209DC`, `20A01`, `20A26`, `20A4B`) + rote Sperr-Rechtecke `20A00`/`20A25`/`20B53` markieren erlaubte/verbotene Fluchtziele bzw. die Gebäudeteilung (roter Merktext `20B76`: Fluchtweg teilt sich zwischen Mollgasse und Anastasius-Grüngasse) — im PDF S. 1-13 nicht erläutert, gehört vermutlich zu einem späteren Kapitel.
