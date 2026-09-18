# Parallel-Abgleich PDF ↔ DXF — Mollgasse 2OG (Seiten 20–26)

Quellen:
- PDF-Text/Bilder: Notbeleuchtungserklärung Seiten 20–26 (`pdf_seiten/seite_20..26.png`)
- DXF: `knowledge/Pläne zeichnen Wissen/Mollgasse-Notbeleuchtungserklärung/WHA_MOL_2OG_Notbeleuchtung_Erklärung.dxf`
  (AC1032, $INSUNITS=4=mm, alle relevanten Entities im Modelspace, Layer meist `0`)

Das Geschoss hat ZWEI erklärte Bereiche:
- **Stiege 1** (Cluster 1, x≈−137 000…−117 000, y≈−600…5 400): Gang Top 15/14/13 + Stiegenhaus mit Top 11+12/Top 10. Labels (A)–(F). Seiten 20–22.
- **Stiege 2** (Cluster 2, x≈−104 700…−94 900, y≈−31 400…−19 300): vertikaler Gang Top 11–15 + Stiegenhaus mit Top 9/Top 10. Labels (A)–(D) (zweiter, eigenständiger Label-Satz!). Seiten 23–26.

Welt-Pfeilrichtung = Basis-Orientierung des Blocks + INSERT-Rotation
(ARR-down Basis 270°, ARR-left Basis 180°, ARR_right Basis 0°; Fluchtwegpfeil-Block `4444444` Basis 180°, d. h. bei rot 0 zeigt er nach Westen — an 10+ Pfeilen gegen die PDF-Bilder verifiziert).

---

## 2OG-01 — Gang mit Abtrennung zum Stiegenhaus (Stiege 1), PDF S. 20–21

**PDF-Aussagen:** Gang mit Wohnungstüren Top 15/14/13, durch eine Tür vom STGH getrennt. Jede Person sieht beim Verlassen direkt die Notleuchte (D) mit Pfeil nach unten an der Tür zum STGH (türkise Blickwinkel-Linien). Zusätzlich zwei Antipanikleuchten (Alternativen: 2 Aufheller / mittige RZ-unten / RZ-unten+Aufheller — nicht gezeichnet).

**DXF-Fakten:**
- (D) = `RIVO-SIBEL-ARR-down` **H=852B6**, Zentrum (−129 816.6, 4 317.9), rot 180.1°, xs 35.637 → **Welt-Pfeil 90.1° (Nord)**. Liegt 482 mm südlich der Gang-Fluchtlinie (y≈4 800) am Abzweig zum STGH; **dx = 2.6 mm** zur Türachsen-x des Tür-Maßtexts `05-TXT` H=83FD3 (−129 814, 4 026, „90/200") → mittig zur STGH-Tür. Welt-Pfeil (90.1°) zeigt **entgegen** der Abzweigrichtung nach Süden (270°, Pfeile H=852D1/852D2).
- (E) = `Antipanikleuchte-RIVO` **H=852B7** (−126 726.5, 4 855.4), rot 90; (F) = **H=852B8** (−120 429.3, 4 854.4), rot 90 → beide 55 mm neben der Gang-Fluchtlinie, Teilung D→E 3 090 mm, E→F 6 297 mm, F→Top-15-Tür 2 579 mm. **Genau 2 Antipanikleuchten ✓**, keine Aufheller/zusätzliche RZ im DXF (nur als Text-Alternative).
- Sichtlinien (cyan, ACI 4): H=85320 Top-13-Person→D, L=3 646 mm; H=85321 Top-14-Person→D, L=10 897 mm; H=85322 Top-15-Person→D, L=12 028 mm. **Alle drei enden an der Ost-Schmalkante von (D)** — Winkel zur Vorderseiten-Normalen 86.5°–90.0° = **reine Seitenansicht** (Sichtlinie parallel zur Schild-Längsachse), keine Frontalsicht.
- Personen: H=852C7/852C8/8531B (Gang, „(2OG)"), H=8531C/8531F (an Top-13/14-Türen). Das Gang-Trio blickt 348.7° (Ost) — **entgegen** der Fluchtrichtung West (Pfeile H=852CA…852D0, Welt 180°).

**Status: praezisiert** — Kernaussagen bestätigt (3 Sichtverbindungen, D an/mittig zur STGH-Tür, 2 Antipanik); präzisiert: „sieht direkt" ist hier nur Sichtverbindung, geometrisch Seitenansicht (86.5–90° zur Frontalen).

Bild: `2OG-01.png`

## 2OG-02 — Stiegenhaus im 2. OG (Stiege 1), PDF S. 21–22

**PDF-Aussagen:** Wohnungstüren Top 11+12 und Top 10; Bewohner sehen sofort (A) mit Pfeil nach rechts (türkise Linien), folgen nach rechts zur Stiege → 1. OG. Menschen aus dem Gang (via D) sehen (B) mit Pfeil nach unten (geradeaus), dann (A). Menschen aus dem 3. OG sehen zuerst (C) mit Pfeil nach links, dann (B), dann (A). Stiegenhauspfeil rot nachgezeichnet; Flucht entgegen dessen Richtung.

**DXF-Fakten:**
- (A) = `RIVO-RZ-ARR_right` **H=852AF** (−136 271.7, 1 315.4), rot 360.0 → **Welt-Pfeil 0° (Ost) ✓ = „rechts"**. 801 mm vor der Stiegen-Westkante (STIEGE H=83DCC, Achse y=1 348), 33 mm auf der Stiegenachse.
- (B) = `RIVO-SIBEL-ARR-down` **H=852B0** (−131 638.8, 2 845.0), rot 89.8 → Welt-Pfeil 359.8° (Ost), **entgegen** dem Fluss der oberen STGH-Zeile (Pfeile H=852D3–D5, Welt 180°); Schild hochkant → Vorderseite frontal zu den von Ost Kommenden.
- (C) = `RIVO-SIBEL-ARR-left` **H=85344** (−129 364.0, 1 325.0), rot 269.5 → **Welt-Pfeil 89.6° (Nord) = Abbiegerichtung „links"** (aus Ost-Laufrichtung). 1 293 mm östlich der Stiegen-Ostkante, 23 mm auf der Stiegenachse.
- Sichtlinien: H=85396 Top-11+12→A (L=1 838 mm, 23.5° zur Frontalen), H=85397 Top-10→A (L=1 681 mm, 13.7°), H=85398 3OG-Person→C (L=3 937 mm, **0.75° = frontal**).
- Stiegenhauspfeil rot: LWPOLYLINE **H=852D7** (ACI 1), Pfeilspitze WEST bei (−135 179.7, 1 341.8), Linie bis (−130 699.7, 1 328.5) → Richtung **180°**; grüne Fluchtpfeile auf der Stiegenzeile H=852C4/852C5 Welt **0° (Ost)** → **Δ = 180° = entgegen ✓**. MTEXT „Stiegenhauspfeilrichtung" H=852D8 (ACI 1). Graues Original = Lauflinie im Block `STIEGE` (BYLAYER, mit Antritts-Kreis).
- Personen-Etappen: (2OG) H=85311/852B4 unten (Blick ~101.6° Nord Richtung A), obere Zeile (3OG) H=852E1 + (2OG) H=85317 (Blick 168.5° West), Stiegenzeile (2OG) H=85313 + (3OG) H=852C6 (Blick ~5–12° Ost Richtung C), Abzweig (3OG) H=852C9 (Blick 78.7° Nord), Eckläufer H=8530F (Blick 296.5° Süd).

**Status: bestaetigt** (mit Zahlen präzisiert; Route Top-Türen→A→Stiege sowie D→B→A und 3OG→C→B→A vollständig durch Pfeile/Personen/Sichtlinien belegt).

Bild: `2OG-02.png`

## 2OG-03 — Gang Stiege 2, Südteil (Top 13/14/15), PDF S. 23

**PDF-Aussagen:** Gang mit drei Wohnungstüren Top 13/14/15; Bewohner sehen auf den ersten Blick die Notleuchte (D), türkise Linien. „Die Notleuchte (D) mit **Pfeil nach rechts**, wurde mittig vom Gang und mittig von der Stiege platziert."

**DXF-Fakten:**
- (D) = `RIVO-SIBEL-ARR-left` **H=852E4** (−95 917.8, −26 588.3), rot 359.55 → **Welt-Pfeil 179.55° (West/links)**. Auch das PDF-Bild S. 23 und der Text S. 25 zeigen/sagen LINKS. **Der S.-23-Text „Pfeil nach rechts" widerspricht Block, Bild und S. 25.**
- „mittig" bestätigt: Gangmitte aus den Türachsen Top 13 (x −95 233) / Top 15 (x −96 483) = x −95 858 → Abweichung **60 mm**; Stiegenachse y −26 630 (STIEGE H=844B6) → Abweichung **42 mm**.
- Fluchtpfeile im Südgang H=85305/85306/85307 Welt 91.2° (Nord, zur Leuchte hin); Zubringer Top 15 H=85304 Welt 1.2° (Ost).
- Sichtlinien: H=85325 Top-13-Person (H=852ED)→D, L=1 495 mm, 30.2° zur Frontalen; H=85324 Top-15-Person (H=85323)→D, L=2 572 mm, 10.1°; H=85326 Top-14-Person (H=852EE)→D, L=4 578 mm, **3.4° = frontal**. Alle enden an der Süd-Vorderseite des Schilds.

**Status: widerspruch** — PDF-Text: „(D) mit Pfeil nach rechts"; DXF: `RIVO-SIBEL-ARR-left`, Welt-Pfeil 179.55° = links/West (PDF-Bild S. 23 und PDF-Text S. 25 bestätigen die DXF). Positionsaussage „mittig/mittig" hingegen bestätigt (60 mm / 42 mm).

Bild: `2OG-03.png`

## 2OG-04 — Gang Stiege 2, Nordteil (Top 11/12), PDF S. 24

**PDF-Aussagen:** Gegenüberliegende Gangseite mit Top 11/Top 12; Notleuchte (C) mit Pfeil nach unten, „so rotiert, dass sie in die **entgegengesetzte Richtung des Fluchtweges** zeigt"; Bewohner sehen (C) auf den ersten Blick (türkise Linie).

**DXF-Fakten:**
- (C) = `RIVO-SIBEL-ARR-down` **H=852E3** (−95 883.0, −22 517.9), rot 179.83 → **Welt-Pfeil 89.8° (Nord)**. Fluchtweg im Nordgang: Pfeile H=852F3/F5/F9/FA/85302 Welt **270° (Süd)** → **Δ = 180.2° = exakt entgegengesetzt ✓**.
- Position: 8 mm neben der Fluchtweg-Linie (x −95 875), 25 mm von der Gangmitte (x −95 858) → mittig im Gang.
- Sichtlinien: H=85327 Top-11-Person (H=852F2)→C, L=2 070 mm, 19.2° zur Frontalen; H=85328 Top-12-Person→C, L=2 987 mm, **5.0° = frontal**. Beide enden an der Nord-Vorderseite (Schild quer zum Gang, Längsachse O-W).
- Personen (2OG) H=852F6 (Blick 258.4° Süd), H=852F7 (Süd) laufen mit dem Fluss zur Kreuzung/(D).

**Status: bestaetigt** — „entgegengesetzt rotiert" ist mit 89.8° vs. 270° exakt belegt.

Bild: `2OG-04.png`

## 2OG-05 — Stiegenhaus im 2. OG (Stiege 2, Top 9/Top 10), PDF S. 25–26

**PDF-Aussagen:** (A) mit Pfeil nach rechts „mittig im Gang und vor der Stiege"; 3OG-Ankömmlinge sehen (A) unmittelbar. Top 9 sieht (A) UND (B); Top 10 sieht (B) mit Pfeil nach unten (geradeaus). Nach (B) sehen alle (D) mit Pfeil nach links → über die Stiege ins 1. OG. Flucht entgegen dem rot dargestellten Stiegenhauspfeil.

**DXF-Fakten:**
- (A) = `RIVO-RZ-ARR_right` **H=8532D** (−103 343.5, −26 599.0), rot 90.0 → Block „rechts", **Welt-Pfeil 90° (Nord)** = Abbiegerichtung von der Stiegen-Ausmündung zur oberen Gangzeile. **940 mm** vor der Stiegen-Westkante (x −102 403), **31 mm** auf der Stiegenachse (y −26 630) → „mittig im Gang und vor der Stiege" ✓; zusätzlich exakt auf der Türachse von Top 9 (Δy = **1.6 mm** zum `00-top`-Anker H=847A5).
- (B) = `RIVO-SIBEL-ARR-down` **H=85330** (−101 727.4, −25 172.8), rot 269.8 → Welt-Pfeil 179.8° (West), **entgegen** dem Fluss der oberen Zeile (Pfeile H=852FE/FF/85300, Welt 1.2° Ost); hochkant → frontal für die von West Kommenden... (Vorderseiten-Normale O-W).
- (D) = `RIVO-SIBEL-ARR-left` **H=852E4** (−95 917.8, −26 588.3) → Welt-Pfeil **179.55° (West) = „links" ✓** = auf die Stiege zu (Stiegenzeilen-Pfeile H=85301/85303 Welt 181.2°/180°).
- Sichtlinien: H=853C0 Top-9-Person (H=852F8)→A, L=882 mm, **0.4° frontal**; H=85329 Top-9-Person→B, L=2 754 mm, 24.3° (Top 9 sieht A UND B ✓ = zwei Sichtlinien vom selben Startpunkt); H=853BF Top-10-Person (H=853BC)→B, L=2 899 mm, 26.5°; H=8533B 3OG-Person (H=85339)→A, L=1 887 mm, **0.5° frontal** ✓ „unmittelbar beim Erreichen".
- Stiegenhauspfeil rot: LWPOLYLINE **H=85309**, Pfeilspitze OST bei (−97 882.2, −26 634.8), Linie bis (−102 362.2, −26 644.4) → Richtung **0° (Ost)**; Flucht auf der Stiegenzeile **180°/181.2° (West)** → **entgegen ✓** (spiegelbildlich zu Stiege 1). MTEXT „Stiegenhauspfeilrichtung" H=8530A.
- Etappen-Personen: obere Zeile (3OG) H=8533C?/85332/8533E/85334 (Blick 11.6° Ost), Stiegenzeile H=85339 „(3OG)", H=85342 „(3OG/ist im 2OG geht Richtung 1OG)" (MTEXT H=85343), H=852EF „(2OG)" (Blick 168.4° West Richtung Stiege).

**Status: praezisiert** — alle Aussagen geometrisch bestätigt; Präzisierung: „(A) Pfeil nach rechts" ist der Blocktyp; in Weltkoordinaten ist (A) um 90° gedreht (Pfeil 90° Nord = Weiterlaufrichtung).

Bild: `2OG-05.png`

---

## Abdeckung (alle Notbeleuchtungs-INSERTs im DXF)

11 Notbeleuchtungs-INSERTs gesamt (5× ARR-down, 2× ARR-left, 2× ARR_right, 2× Antipanik; keine Aufheller/Spots/Gruppenbatterie in dieser Datei):

| Handle | Block | Zentrum | Label | Beispiel |
|---|---|---|---|---|
| 852AF | RIVO-RZ-ARR_right | (−136 271.7, 1 315.4) | (A) St.1 | 2OG-02 |
| 852B0 | RIVO-SIBEL-ARR-down | (−131 638.8, 2 845.0) | (B) St.1 | 2OG-02 |
| 85344 | RIVO-SIBEL-ARR-left | (−129 364.0, 1 325.0) | (C) St.1 | 2OG-02 |
| 852B6 | RIVO-SIBEL-ARR-down | (−129 816.6, 4 317.9) | (D) St.1 | 2OG-01 |
| 852B7 | Antipanikleuchte-RIVO | (−126 726.5, 4 855.4) | (E) | 2OG-01 |
| 852B8 | Antipanikleuchte-RIVO | (−120 429.3, 4 854.4) | (F) | 2OG-01 |
| 8532D | RIVO-RZ-ARR_right | (−103 343.5, −26 599.0) | (A) St.2 | 2OG-05 |
| 85330 | RIVO-SIBEL-ARR-down | (−101 727.4, −25 172.8) | (B) St.2 | 2OG-05 |
| 852E3 | RIVO-SIBEL-ARR-down | (−95 883.0, −22 517.9) | (C) St.2 | 2OG-04 |
| 852E4 | RIVO-SIBEL-ARR-left | (−95 917.8, −26 588.3) | (D) St.2 | 2OG-03/05 |
| **8532F** | RIVO-SIBEL-ARR-down | (−72 431.2, 61 138.5), rot 89.8, Welt-Pfeil 0° | **kein Label** | **unerklaert** |

## Regel-Beobachtungen (Rohstoff Regelbasis, geometrisch belegt)

1. **RZ vor der Stiege, auf der Stiegenachse:** (A) sitzt 801 mm (St.1) bzw. 940 mm (St.2) vor der Stiegen-Antrittskante und 33 mm bzw. 31 mm auf der Stiegen-Mittelachse (Stiegenbreite 1 224/1 200 mm). [2OG-02, 2OG-05]
2. **Flucht entgegen dem Stiegenhauspfeil (OG):** rot nachgezeichnete Lauflinie 180° (St.1) bzw. 0° (St.2); grüne Fluchtrichtung auf der Stiegenzeile 0° bzw. 180.6° → Δ=180° in beiden Fällen. Graues Original = Lauflinie im `STIEGE`-Block (BYLAYER, Antritts-Kreis). [2OG-02, 2OG-05]
3. **Pfeil-unten-RZ (geradeaus) werden gegen den ankommenden Strom gedreht:** Welt-Pfeil entgegen Laufrichtung in 4/4 Fällen (St.1-B 359.8° vs 180°; St.1-D 90.1° vs 270°; St.2-B 179.8° vs 1.2°; St.2-C 89.8° vs 270°) → Vorderseite steht frontal zum Ankommenden. [2OG-01…05]
4. **Richtungs-RZ (links/rechts) zeigen in Weltkoordinaten die Abbiege-/Weiterrichtung:** St.1-A 0° (Ost auf die Stiege), St.1-C 89.6° (Nord), St.2-A 90° (Nord), St.2-D 179.6° (West auf die Stiege) — 4/4. „links/rechts" im PDF = Piktogramm-Typ, nicht Weltrichtung. [2OG-02, 2OG-03, 2OG-05]
5. **Sichtlinien enden an der Schild-VORDERSEITE; 9 von 12 nahezu frontal** (0.4°–30.2° zur Flächennormalen); Längen 882–12 028 mm. Ausnahme: die 3 Gang-Sichtlinien auf St.1-(D) treffen mit 86.5°–90° die Schmalkante (Seitenansicht über 3.6–12.0 m) — „sieht direkt" heißt dort nur freie Sichtverbindung. [alle]
6. **Tür-RZ mittig zur Tür:** St.1-(D) dx=2.6 mm zur Türachsen-x des Tür-Maßtexts; St.2-(A) Δy=1.6 mm zur Top-9-Türachse; St.2-(D) 60 mm zur Gangmitte / 42 mm zur Stiegenachse. [2OG-01, 2OG-03, 2OG-05]
7. **Antipanik als Gang-Grundbeleuchtung:** genau 2 Stück auf der Gangmittellinie (55 mm neben der Fluchtlinie), Teilung 3.1 m / 6.3 m / 2.6 m zwischen Tür-RZ und Gangende; Alternativen (2 Aufheller, mittige RZ-unten, RZ+Aufheller) nur im Text, nicht gezeichnet. [2OG-01]
8. **Personen-Symbol `750298750` Blickrichtung:** xs>0 → Blick=(180°+rot); xs<0 (gespiegelt) → Blick=rot. Verifiziert per Render (H=852EF 168.4° West, H=852E1 168.5° West, H=8533C 11.6° Ost). Ausnahme/Inkonsistenz: Gang-Trio St.1 H=852C7/852C8/8531B blickt 348.7° (Ost) entgegen der Fluchtrichtung West. [2OG-01]
9. **Etappen-Dokumentation:** 32 Personensymbole mit Herkunftslabels (2OG)/(3OG)/„3OG/ist im 2OG geht Richtung 1OG" markieren jede Richtungsänderung des Fluchtwegs; die Fluchtwegpfeile (`4444444`, 38 Stück) bilden lückenlose Ketten Tür→RZ→Stiege. [alle]

## Offene Fragen

- Kein Türblock an der St.1-Abzweigung Gang→STGH (nur Maßtext `05-TXT` H=83FD3 „90/200"); Türmitte nur über den Maßtext-Anker belegbar.
- Unerklärte Leuchte H=8532F bei (−72 431, 61 139): kein Label, keine Sichtlinien/Personen — Rest/Kopie außerhalb der PDF-Beispiele? (In S. 20–26 nicht referenziert.)
- S.-23-Text „Pfeil nach rechts" vs. Bild+DXF links: vermutlich Textfehler des Autors — für die Regelbasis DXF + S. 25 maßgeblich?
- Blaue schraffierte Markierung „ÜBERGABESTATION" (St.2) ist keine Lichtkuppel gemäß Registry — Haustechnik ohne Notbeleuchtungs-Bezug?
- Blicken die St.1-Gang-Läufer absichtlich gegen die Fluchtrichtung (aus den Türen tretend) oder Kopierfehler?

Side-by-Side-Bilder: `2OG-01.png` … `2OG-05.png` (links PDF-Seite, rechts DXF-Render).
