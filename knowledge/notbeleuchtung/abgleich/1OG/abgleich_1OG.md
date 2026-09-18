# Parallel-Abgleich PDF ↔ DXF — Mollgasse 1OG (Seiten 14–19)

Quellen:
- PDF-Text/-Bilder: `Notbeleuchtungen zeichnen.pdf`, Seiten 14–19 (Abschnitt „1.Obergeschoß Notbeleuchtung").
- DXF: `knowledge/Pläne zeichnen Wissen/Mollgasse-Notbeleuchtungserklärung/WHA_MOL_1OG_Notbeleuchtung_Erklärung.dxf`
  (AC1032, INSUNITS=4 → **mm**; alles Relevante im Modelspace; Layout2 = nur Blatt/Bemaßung, keine Notleuchten).

Das Geschoss hat **zwei Beispielbereiche**:
- **Bereich A1** (Stiegenhaus „1. STOCK / STGH 17.24m2" + Gang 15.74m2, Top 4–9): x ≈ −356k…−333k, y ≈ 28k…37k. Seiten 14–16.
- **Bereich A2** (Stiegenhaus „1. STOCK / STGH 29.74m2", Top 2–8 des zweiten Stiegenkerns): x ≈ −323k…−309k, y ≈ −3k…12k. Seiten 17–19.

Wichtige Block-/Farb-Konventionen (in dieser DXF gemessen):
- Insert-Punkte der RIVO-Blöcke liegen **weit neben der sichtbaren Geometrie** (Blockbasispunkt versetzt, Skalierung 25–52) → alle Positionen unten sind **bbox-Zentren** der sichtbaren Symbole.
- Welt-Pfeilrichtung = Basisrichtung des Blocks (down=270°, left=180°, right=0°) + INSERT-Rotation (über volle Matrix inkl. Spiegelung gerechnet).
- Fluchtweg-Polylinien: **ACI 100** (grün). Sichtlinien: **ACI 4** (türkis). Stiegenhauspfeil-Nachzeichnung: **ACI 1** (rot, LWPOLYLINE mit Dreiecks-Spitze am Zielende). Leuchten-/Personen-Labels: grüne MTEXT **ACI 3**.
- Menschensymbol `750298750`: bei rot=0 blickt der Läufer nach **links** (lokal (−1,0)); gespiegelte Instanzen (xscale=−4.007) über Matrix korrekt ausgewertet.
- Fluchtwegpfeil `4444444`: die sichtbare Spitze zeigt bei rot=0 nach **links** (lokal (−1,0)); d. h. visuelle Richtung = Welt-Richtung von (−1,0). (Doppelt verifiziert an Personen-Laufrichtungen in beiden Bereichen.)

---

## 1OG-01 — Gang mit drei Wohnungstüren Top 9/8/7 (PDF Seite 14) — Bereich A1

**PDF-Aussagen:** (D) mit Pfeil nach unten bei der Tür zwischen Gang und Stiegenhaus; (D) rotiert, dass der Pfeil in den Gang hineinzeigt = entgegengesetzt zur Öffnungsrichtung der Tür; Antipanikleuchten (E) und (F) im Gang; von Top 9/8/7 je eine türkise Sichtlinie zu (D); keine weitere Notleuchte nötig.

**DXF-Fakten:**
- **(D)** = `RIVO-SIBEL-ARR-down` **h=95042**, Zentrum (−346703, 34488), rot=180.10°, Welt-Pfeil **90.1° = oben (in den Gang)**.
- **Tür Gang↔STGH:** Öffnung in der O-W-Wand (Wandachse y≈34230), Laibungen x=−347218 (h=93DAD) und x=−346258 (h=93DAE) → **Türbreite 960 mm, Türmitte x=−346738**. (D)-Zentrum weicht **35 mm** von der Türmitte ab → **mittig zur Tür** bestätigt. (D) sitzt 258 mm **gangseitig** (nördlich) der Wandachse.
- **Öffnungsrichtung:** Türblatt h=93D42 (x≈−346280, y 33290–34190) + Schwenk-ARC **h=93DAC** (Zentrum (−346318,34190), r=900, 180°–270°) → Tür öffnet nach **Süden ins Stiegenhaus**. Welt-Pfeil von (D) = oben/Norden → **exakt entgegengesetzt (180°)**. ✔
- **(E)** = `Antipanikleuchte-RIVO` **h=95066**, Zentrum (−343613, 35026), rot=90. **(F)** = **h=95067**, Zentrum (−337316, 35025), rot=90. Beide ~55 mm neben der grünen Fluchtweglinie (y≈34970) → **mittig im Gang**; Abstand (D)→(E) = 3136 mm, (E)→(F) = 6297 mm.
- **Sichtlinien (ACI 4):** h=95614 Top 7 → (D), L=3646 mm; h=95615 Top 8 → (D), L=10897 mm; h=95616 Top 9 → (D), L=12028 mm. Alle enden an der **Ost-Kante** des (D)-Symbols (x≈−346388) und schneiden keine Wand (Verlauf im Gangband y 34.4k–35.4k).
- **Personen:** h=955EE (Top 7, −342639/34154, Blick links), h=95613 (Top 8, −335389/34152, Blick links), h=955A8 (Top 9, −334350/35065, Blick links) + Gang-Läufer h=950E4/950E3 (Blick links). Labels `(1OG)` ACI 3.
- **Winkel zur Vorderseite:** (D)-Längsachse liegt O-W (Symbol 630×316). Sichtlinien verlaufen 179.6°–183.6°, d. h. **fast parallel zur Längsachse (86–90° von frontal)** → streng genommen Seitenansicht; die PDF spricht hier nur von „direkter Sichtverbindung/Blickwinkel", nicht von Vorderseite (→ offene Frage O1).

**Status: bestätigt + präzisiert** (Türmitte 35 mm, Öffnungsrichtung per ARC belegt, Pfeil exakt 180° gegen Öffnungsrichtung).

Bild: `1OG-01.png`

---

## 1OG-02 — Stiegenhaus im 1. OG, Top 4+5/6 (PDF Seiten 15–16, inkl. Alternative für (C)) — Bereich A1

**PDF-Aussagen:** roter Stiegenhauspfeil (nachgezeichnet); OG-Menschen bewegen sich entgegen der Pfeilrichtung; (A) Pfeil nach rechts, direkt beim Austritt aus Top 4+5 und Top 6 sichtbar; (C) Pfeil nach links, vor der Stiege an der Wand (alternativ mittig im Gang, „immernoch vor den Stiegen"); (B) Pfeil nach unten, an der Decke mittig im Gang, Pfeil entgegen der Weiterlaufrichtung; Reihenfolge 2OG: (C)→(B)→(A); Gang-Menschen: (D)→(B)→(A).

**DXF-Fakten:**
- **Stiegenhauspfeil (rot):** LWPOLYLINE **h=95137** ACI 1, Spitze bei (−352066,31512), Schaft bis (−347586,31499) → Richtung **180° (links/West)**. MTEXT „Stiegenhauspfeilrichtung" h=9515A ACI 1. Personen auf der Stiege: h=9553A (Blick 11.6°, Label (1OG)), h=950C0 (Blick 5.2°, Label (2OG)) → **Differenz ≈ 168–175° zum Pfeil = entgegen** ✔.
- **(A)** = `RIVO-RZ-ARR_right` **h=94FE7**, Zentrum (−353158, 31486), rot≈0, Welt-Pfeil **0° (rechts)**. STIEGE h=93B6B: bbox x −352348…−347536, y 30899…32113 → (A) steht **810 mm vor (westlich) der Stiegen-Westkante**, y-Versatz zur Stiegen-Mittellinie nur 20 mm; Pfeil zeigt **in die Stiege**. Sicht von Top 4+5 (Person h=94FF6, −352491/29660, Blick oben): 1945 mm, ca. 20° von frontal; von Top 6 (−353432/33316): ca. 8° von frontal → beidseitig „direkt beim Austritt sichtbar" plausibel (keine trennende Wand auf den Strecken).
- **(C)** = `RIVO-SIBEL-ARR-left` **h=95019**, Zentrum (−346579, 31546), rot=269.55°, Welt-Pfeil **89.5° (oben)** (= Schildtyp „Pfeil links", gedreht). Lage: **957 mm vor (östlich) der Stiegen-Ostkante**, y-Versatz zur Stiegen-Mittellinie 40 mm (= „mittig, aber noch vor der Stiege" — die Alternative von Seite 16); Ost-Wand (h=93BE5, x=−346083): Abstand Symbolkante→Wand **334 mm** (= „an der Wand"). Beide PDF-Formulierungen treffen auf dieselbe DXF-Instanz zu; es existiert **nur eine** (C).
- **(B)** = `RIVO-SIBEL-ARR-down` **h=94FE8**, Zentrum (−348525, 33015), rot=89.83°, Welt-Pfeil **359.8° (rechts/Ost)**. Grüne Fluchtweglinie des oberen STGH-Stegs y≈33055, Fluss **nach links/West (180°)** (Pfeile h=95133–95135, visuell links) → Pfeil **179.8° entgegen der Laufrichtung** ✔ „mittig im Gang": 40 mm neben der grünen Linie.
- **(D)** (wie 1OG-01, h=95042) hängt über der Gang-Tür; Fluss durch die Tür nach Süden (Pfeile h=9510F/95110 visuell unten) → Gang-Menschen (D)→(B)→(A) entlang grüner Linie, Person h=9553C (Blick unten) und h=952C1/9553E (Blick links, Labels (2OG)/(1OG)) belegen die Kette.
- 2OG-Ankunft Ost: Person h=950E5 (−346544, 32333, Blick oben, Label (2OG)) direkt unter (C) → sieht (C) beim Erreichen des 1. OG ✔.
- Keine türkisen Sichtlinien in diesem Bereich (die PDF behauptet hier auch keine).

**Status: bestätigt + präzisiert** (Pfeil-gegen-Laufrichtung 179.8° exakt; „an der Wand" und „mittig/vor der Stiege" sind in der DXF **dieselbe** Position: 957 mm vor Stiege, 334 mm vor Ostwand, mittig zur Stiegenbreite).

Bilder: `1OG-02.png` (Seite 15), `1OG-02b.png` (Seite 16 unten, Alternative (C))

---

## 1OG-03 — Gang im 1. OG mit Top 6/7/8 (PDF Seite 17) — Bereich A2 (N-S-Gang Süd)

**PDF-Aussagen:** Bewohner von Top 6, Top 7, Top 8 sehen beim Verlassen auf den ersten Blick (D) mit Pfeil nach links; türkise Linien = Blickwinkel; Pfeil nach links → Fluchtweg verläuft nach links weiter.

**DXF-Fakten:**
- **(D)** = `RIVO-SIBEL-ARR-left` **h=952E9**, Zentrum (−312728, 3649), rot=359.55°, Welt-Pfeil **179.5° (links/West)** — zeigt zur Stiege (STIEGE h=94204, bbox x −319223…−314412, y 2993…4203). (D) sitzt **am Knick** des Fluchtwegs: N-S-Gang (grüne Linien h=952EC/952EF, x≈−312.7k) trifft O-W-Stiegenzuweg (h=9537E, y≈3645). Versatz zur Gangmittellinie ~20–43 mm → mittig im Gang.
- **Sichtlinien (ACI 4):** h=9561C Top 8 (Person h=9561B, −313464/928, Blick oben) → (D), **L=2572 mm**, Winkel ~10.5° von frontal; h=9561D Top 6 (Person h=95314, −311793/2454, Blick links) → (D), **L=1495 mm**, ~30° von frontal; h=9561E Top 7 (Person h=95337, −312744/−1093, Blick oben) → (D), **L=4578 mm**, ~4° von frontal. (D)-Längsachse O-W → alle drei sehen die **Vorderseite** (Süd-Breitseite). Keine Wand auf den Linien.
- Wohnungstür-Anker: ATTRIB `TOP 8` (−312996,640), `TOP 7` (−312841,−404), `TOP 6` (−312250,2306).
- Gang-Fluss: südlicher Ast visuell **oben** (h=95481–95483: dir(1,0)=271° → Spitze 91°), nördlicher Ast visuell **unten** → beide konvergieren auf (D), danach Fluss **West** in die Stiege ✔ „Fluchtweg verläuft nach links".

**Status: bestätigt** (mit Zahlen präzisiert).

Bild: `1OG-03.png`

---

## 1OG-04 — Gang mit Top 4 und Top 5 (PDF Seite 18) — Bereich A2 (N-S-Gang Nord)

**PDF-Aussagen:** türkise Linie = Blickwinkel zu (C) mit Pfeil nach unten; (D) ist weiter entfernt, evtl. nicht ausreichend erkennbar → deshalb zusätzlich (C); (C) mittig im Gang; Pfeil-nach-unten-Leuchten mittig im Gang, wenn geradeaus zu folgen ist; (C) rotiert, dass Pfeil in die entgegengesetzte Richtung des Fluchtwegs zeigt.

**DXF-Fakten:**
- **(C)** = `RIVO-SIBEL-ARR-down` **h=952E8**, Zentrum (−312693, 7719), rot=179.83°, Welt-Pfeil **89.8° (oben/Nord)**. Fluchtweg dort läuft nach **Süden (270°)** (grüne Linie h=952EA x≈−312.7k, Pfeile h=953E7/9542D visuell unten) → Pfeil **179.8° entgegen** ✔.
- **Mittig im Gang:** Gangbreite an y=7719: Westwand x=−313509 (h=9418F), Ostwand x=−312067 (h=9422C) → Breite 1442 mm, Mitte x=−312788; (C) liegt **95 mm** daneben bzw. **6 mm** neben der grünen Fluchtweglinie.
- **Sichtlinien (ACI 4):** h=9561F Top 4 (Person h=953C4, −313744/9884, Blick unten) → (C), **L=2070 mm**, ~19° von frontal; h=95620 Top 5 (Person h=953A1, −312751/10918, Blick unten) → (C), **L=2987 mm**, ~5° von frontal. (PDF sagt „eine türkise Linie", DXF hat **zwei** — je Wohnungstür eine.)
- **Abstand zu (D):** (C)→(D) = 4071 mm; Top-5-Tür→(D) ≈ 6.4 m (plausibilisiert „(D) ist von diesen Wohnungstüren weiter entfernt").
- Wohnungstüren: `TOP 4` (−313015,9610), `TOP 5` (−312863,10026); Türen h=9477B/9477C (y≈9480).

**Status: bestätigt + präzisiert** (2 statt „eine" Sichtlinie; Gegenrichtungs-Rotation exakt 179.8°).

Bild: `1OG-04.png`

---

## 1OG-05 — Gänge ohne Abtrennung zum Stiegenhaus, Top 2+3 (PDF Seite 19) — Bereich A2

**PDF-Aussagen:** Gänge (1OG-03/04) sind NICHT durch Türen vom STGH getrennt; (A) so platziert, dass 2OG-Ankömmlinge UND Top-2+3-Bewohner sie direkt sehen; je eine türkise Linie von „2OG" und von „1OG bei Top 2+3" **zur Notleuchte (A)**; (A) Pfeil nach rechts zeigt weiteren Weg im Stiegenhaus; gemeinsame Kette (A)→(B)→(D); Stiegenhauspfeil grau (Original) + rot nachgezeichnet; OG-Menschen entgegen Pfeilrichtung.

**DXF-Fakten:**
- **Keine Tür** zwischen N-S-Gang und STGH-Bereich in A2 (keine TÜR-Inserts an den Gang-Mündungen; Tür-Inserts liegen nur an Wohnungs-/Nebenraumtüren) ✔.
- **(A)** = `RIVO-RZ-ARR_right` **h=9568B**, Zentrum (−320154, 3638), rot=89.99°, Welt-Pfeil **90° (oben)** = Richtung des grünen Wegs (nach (A) erst nach Norden, dann Ost: h=952ED (−320171,3621)→(−320174,5057)→(−318687,5064)). „Vor der Stiege": **931 mm westlich der Stiegen-Westkante** (x=−319223).
- **Sichtlinien (ACI 4):** h=957AC von Person „(2OG)" h=957AA (−318059, 3496, Blick links) → **(A)**, L=1887 mm, **0.5° von frontal** ((A)-Längsachse N-S). ✔
  **ABER:** h=95621 von Person „(1OG)" bei Top 2+3 h=95452 (−321240, 3623, Blick rechts) endet bei (−318678, 4994) = **an (B) (h=956B0, Abstand Endpunkt→(B)-Zentrum 197 mm), NICHT an (A)** ((A)-Zentrum wäre 1946 mm entfernt). → **Widerspruch zur PDF-Textaussage** „jeweils eine türkise Linie zur Notleuchte (A)"; das PDF-Bild selbst zeigt die Linie ebenfalls zu (B). Sichtbarkeit von (A) von Top 2+3 aus wäre zudem seitlich (Blick ~0° vs. (A)-Längsachse N-S → nahezu frontal, Linie okay) — die gezeichnete Linie führt aber zu (B).
- **(B)** = `RIVO-SIBEL-ARR-down` **h=956B0**, Zentrum (−318519, 5111), rot=269.83°, Welt-Pfeil **179.8° (links/West)**; Personenzug im Nordgang läuft **nach Ost (11.6°/1.2°)** (Personen h=957D0/956F7/957F5/9571C, Labels (2OG)/(1OG) paarweise „nebeneinander" ✔) → Pfeil ≈178.6° **entgegen der Laufrichtung** ✔; 0–40 mm neben der grünen Linie (mittig).
- **(D)** (h=952E9, s. 1OG-03) schließt die Kette: nach Ost-Lauf knickt der Weg nach Süden und (D) zeigt **links/West in die Stiege** ✔ („nach links weitergehen, über die Stiege ins EG").
- **Stiegenhauspfeil:** rote Nachzeichnung **h=954A7** ACI 1, Spitze bei (−314693, 3602) → Richtung **0.2° (rechts/Ost)**; MTEXT h=954CA „Stiegenhauspfeilrichtung" ACI 1. Personen auf der Stiege h=95861 (Label-MTEXT h=95862 „(2OG/ist im 1OG geht Richtung EG)") und h=9537D: Blick **168.4°** → **entgegen dem Pfeil (Δ≈168°)** ✔. Graue Stiegen-Grafik (Steigungslinien-Umrisse, Layer 06-SYM, h=945F2/945FC …) liegt direkt daneben — Spitzenrichtung des grauen Originals aus den Umriss-Polylinien nicht eindeutig extrahierbar (→ offene Frage O2).

**Status: präzisiert mit einem Teil-Widerspruch** (Sichtlinie der Top-2+3-Person endet an (B), nicht an (A) — PDF-Text sagt (A), PDF-Bild zeigt (B)).

Bild: `1OG-05.png`

---

## Abdeckung (alle Notbeleuchtungs-INSERTs der DXF)

Gesamt 17 Notbeleuchtungs-INSERTs im Modelspace:

| Handle | Block | Zentrum (mm) | Zuordnung |
|---|---|---|---|
| 94FE7 | RIVO-RZ-ARR_right | (−353158, 31486) | 1OG-02 (A) |
| 94FE8 | RIVO-SIBEL-ARR-down | (−348525, 33015) | 1OG-02 (B) |
| 95019 | RIVO-SIBEL-ARR-left | (−346579, 31546) | 1OG-02 (C) |
| 95042 | RIVO-SIBEL-ARR-down | (−346703, 34488) | 1OG-01/02 (D) |
| 95066 | Antipanikleuchte-RIVO | (−343613, 35026) | 1OG-01 (E) |
| 95067 | Antipanikleuchte-RIVO | (−337316, 35025) | 1OG-01 (F) |
| 9568B | RIVO-RZ-ARR_right | (−320154, 3638) | 1OG-05 (A) |
| 956B0 | RIVO-SIBEL-ARR-down | (−318519, 5111) | 1OG-05 (B) |
| 952E8 | RIVO-SIBEL-ARR-down | (−312693, 7719) | 1OG-04 (C) |
| 952E9 | RIVO-SIBEL-ARR-left | (−312728, 3649) | 1OG-03/05 (D) |
| 94FE4 | Aufheller Notbeleuchtung | (−370594, 25521) | unerklärt: Legendenblock |
| 94FE5 | Spot Notbeleuchtung | (−370594, 23637) | unerklärt: Legendenblock |
| 94FE6 | Gruppenbatterie-Verteiler | (−370550, 24104) | unerklärt: Legendenblock |
| 94FF3 | RIVO-SIBEL-ARR-left | (−370542, 24619) | unerklärt: Legendenblock |
| 94FF4 | RIVO-SIBEL-ARR-left | (−370542, 24842) | unerklärt: Legendenblock (gespiegelte Zweitinstanz) |
| 94FF5 | Antipanikleuchte-RIVO | (−370576, 25219) | unerklärt: Legendenblock |
| 9568D | RIVO-SIBEL-ARR-down | (−378643, 60794) | unerklärt: **isolierter Streuner** (im Radius 8 m keinerlei andere Entities) |

Zugeordnet: 10 (alle gelabelten (A)–(F) beider Bereiche). Ungelabelt/unerklärt: 7 (6 × Legendenspalte bei x≈−370.5k, 1 × Streuner h=9568D).

## Regel-Beobachtungen (geometrisch belegt)

1. **Tür-RZ mittig zur Türöffnung:** (D)-A1 Abweichung Symbolzentrum↔Türmitte = **35 mm** bei 960 mm Türbreite; Symbol hängt 258 mm gangseitig der Wandachse. [1OG-01]
2. **Tür-RZ-Pfeil = 180° gegen die Tür-Öffnungsrichtung:** Türblatt+ARC (h=93D42/93DAC) öffnen nach Süden ins STGH, Welt-Pfeil (D)-A1 = 90.1° Nord in den Gang. [1OG-01]
3. **Pfeil-nach-unten-RZ („geradeaus") wird so rotiert, dass der Welt-Pfeil der lokalen Laufrichtung entgegensteht:** (B)-A1 359.8° vs. Fluss 180° (Δ179.8°); (B)-A2 179.8° vs. Fluss ~1° (Δ178.6°); (C)-A2 89.8° vs. Fluss 270° (Δ179.8°). Drei unabhängige Instanzen, Abweichung ≤1.4°. [1OG-02/04/05]
4. **Pfeil-nach-unten-RZ stehen mittig im Gang:** 6–55 mm neben der grünen Fluchtweg-Mittellinie; bei (C)-A2 95 mm neben der geometrischen Gangmitte (Gangbreite 1442 mm). Auch Antipanikleuchten (E)/(F) mittig (55 mm). [1OG-01/02/04/05]
5. **Richtungs-RZ „vor der Stiege":** (A)-A1 810 mm vor der Stiegen-Westkante (mittig zur Stiegenbreite, Δ20 mm); (A)-A2 931 mm vor der Westkante; (C)-A1 957 mm vor der Ostkante. Pfeil-Weltrichtung zeigt jeweils in den nächsten Wegabschnitt (A-A1: 0° in die Stiege; A-A2: 90° in den Umlauf; C-A1: 89.5° in den Umlauf). [1OG-02/05]
6. **Stiegenhauspfeil vs. Personenbewegung:** rote Nachzeichnung ACI 1 mit Dreiecksspitze; A1-Pfeil 180°, Stiegen-Personen Blick 5–12° (Δ≈170–175°); A2-Pfeil 0.2°, Stiegen-Personen Blick 168.4° (Δ≈168°) → OG-Personen laufen **entgegen** dem Stiegenhauspfeil (beide Kerne). [1OG-02/05]
7. **Sichtlinien:** ACI-4-LWPOLYLINEs Person→Leuchte, Längen 1495–12028 mm, enden an der Symbolkante (nicht am Zentrum); pro Wohnungstür genau eine Linie zum maßgeblichen RZ. Winkel zur Vorderseite: an Quergängen 0.5–30° (frontal); am Gang-Ende (D)-A1 dagegen 86–90° (entlang der Symbol-Längsachse). [alle]
8. **Zwei Antipanikleuchten decken einen ~12-m-Gang:** (D)…(E) 3136 mm, (E)…(F) 6297 mm, (F)…Gang-Ende ~2900 mm. [1OG-01]
9. **Labels:** Leuchten-Labels „(A)…(F)" und Personen-Labels „(1OG)/(2OG)" als grüne MTEXT ACI 3, 300–600 mm neben dem Symbol; rote MTEXT „Stiegenhauspfeilrichtung" ACI 1 an beiden Stiegen. [alle]
10. **Ohne Tür kein Tür-RZ:** in A2 (Gänge nicht vom STGH getrennt) hängt kein RZ an den Gang-Mündungen; stattdessen Richtungs-RZ an Knick/Stiege ((D)-A2 am Knick, (A)-A2 vor der Stiege). [1OG-03/05]

## Offene Fragen

- **O1:** (D)-A1 (Tür-RZ am Gang-Ende) wird von Top 7/8/9 fast exakt **entlang seiner Längsachse** gesehen (86–90° von frontal). Die PDF nennt hier nur „direkte Sichtverbindung"; ab Seite 31 (4OG) wird das Vorderseiten-Kriterium streng formuliert. Gilt das Vorderseiten-Kriterium für Tür-RZ nicht bzw. schwächer? (Symbol-Längsachse folgt der Türwand, nicht der Blickrichtung.)
- **O2:** „Der ursprüngliche Stiegenhauspfeil ist grau" — die grauen Stiegen-Grafiken (Layer 06-SYM) sind als Umriss-Polylinien gezeichnet; eine eindeutige graue Pfeil-Spitze konnte nicht isoliert werden. Richtung nur über die rote Nachzeichnung belegt.
- **O3:** Sichtlinien-Anzahl: Seite 18 sagt „eine türkise Linie", die DXF hat zwei (Top 4 und Top 5 je eine). Konvention vermutlich „eine je Wohnungstür" — vom PDF-Text nicht exakt gedeckt.
- **O4:** Streuner h=9568D (RIVO-SIBEL-ARR-down bei (−378643, 60794), isoliert, ohne Kontext) — Zweck unklar, vermutlich vergessene Kopie.
- **O5:** 1OG-05: PDF-Text „jeweils eine türkise Linie zur Notleuchte (A)" vs. DXF/PDF-Bild: Linie der Top-2+3-Person endet an (B) (Endpunkt 197 mm vor (B), 1946 mm von (A)). Textfehler im PDF oder bewusste Änderung?
