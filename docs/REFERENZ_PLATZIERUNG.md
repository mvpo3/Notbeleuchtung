# Referenz-Platzierung — Muster aus Fachplaner-Plan, Beispielbildern und Wissensquellen

**Zweck:** Die beobachteten Platzierungs-MUSTER der Referenz-Praxis, als Vorbild für
die Platzierungs-Strategien (Leonis) und den Referenzvergleich
(`scripts/plan_pruefen.py`, `07_referenzvergleich.png`). KEINE Normwerte — wo eine
Zahl steht, ist sie eine **Messung am Referenzmaterial**, keine Norm-Anforderung.
Normzitate nur mit Fundstelle (siehe Quellenliste unten).

Erhoben 2026-09-07 (selbst gemessen an der Referenz-DXF bzw. an den Bildern; Skript-
Messungen mit ezdxf, temporär, gelöscht).

---

## 1. Fachplaner-Referenzplan Barawitzkagasse

**Quelle:** `DIN-Notbeleuchtungspläne(Beispiele)/din_support_ReMi_Barawitzkagasse_28.04.2026.dxf`
(R2018, mm, DIN-Notlicht-Planungstool „din support"). 46 Leuchten + 1 Controller auf
Layer `din_SIBEL_10_emergency_lighting` (RZ, 33×), `…_yellow` (SL, 13×),
`…_system` (Controller, 1×); Legenden-Duplikate auf `din_SIBEL_70_legend_*`
nicht mitzählen. Unterlage = gescannte JPG (Xref fehlt im Repo), mehrere
Geschoss-Frames nebeneinander im Modelspace.

### Frame → unser PP_2-Plan (m)

`our = ref/1000 + Offset` (Frame-Kalibrierung gegen unsere Barawitzka-EG-Erkennung):

| Geschoss | Offset (m) | Restfehler |
|---|---|---|
| UG | (-77.85, -37.66) | Ø 0.33 m |
| EG | (-48.44, -39.04) | Ø 0.19 m |
| OG1 | (-18.34, -38.66) | Ø 0.04 m |

EG-Bestückung (11 Leuchten): 5× RZ Typ A, 3× RZ Typ B, 1× RZ Typ F, 1× SL Typ H,
1× SL Typ I.

### Symbolik des Fachplaners

Blöcke `STANDARDMASK_RZ_PL` / `_PR` / `_PU` / `_PLPR` (Rettungszeichen: Pfeil links /
rechts / unten / links+rechts beidseitig), `STANDARDMASK_SL` (Sicherheitsleuchte),
`STANDARDMASK_SYSTEM` (SV-Anlage/Controller). Typen A–I in Attribut `TYPENUMBER`
(Schrack/din-Produkte BASICsc / CONCEPTsc, CMR 1–8 h in `TYPENAME`).
**Rotation strikt im 90°-Raster** und immer = Wand-/Gangwinkel — kein freier Winkel
im ganzen Plan (33 RZ gemessen: nur 0/90/180/270).

### Beobachtete Muster (mit Beispielkoordinaten in unserem m-System)

1. **RZ_PU mittig über der Ausgangstür**, 0.25–1.0 m vor der Türsehne (Innenseite).
   Beispiel EG: RZ_PU Typ A ref (62766, 35912) → our **(14.33, -3.13)**.
2. **SL zusätzlich AUSSEN über jedem Endausgang**; Typ I sitzt 0.35 m vor dem
   RZ des Ausgangs. Beispiel EG: SL Typ I ref (62773, 36264) → our
   **(14.33, -2.78)** — 0.35 m über dem RZ_PU aus Muster 1.
3. **Stiegenhaus-Regelgeschoss-Kit** — identisch je Geschoss wiederholt:
   RZ_PL an der Stiegenhaus-Tür + SL 2.2 m daneben am Podest + RZ_PLPR diagonal im
   Gang. Beispiel OG1 (Stiege 1): RZ_PL ref (56589, 128956) → our (8.15, -9.70),
   SL Typ H ref (58805, 128966) → our (10.37, -9.69) [2.2 m daneben],
   RZ_PLPR ref (61564, 130914) → our (13.12, -7.75). Wiederholung OG2 wortgleich:
   RZ_PL (56272, 157590), SL (58442, 157603), RZ_PLPR (61133, 159517).
4. **Richtungs-RZ an der Wand entlang der Gangachse** (Wandabstand ≤ 0.3 m),
   an Richtungswechseln **paarweise gegenläufig** (PL gegen PR). Beispiel EG:
   RZ_PR rot=0 ref (56580, 32797) ↔ RZ_PR rot=180 ref (56894, 30254).
5. **RZ_PLPR (beidseitig) an Gangknoten und Gang-Enden**, quer zur Gangachse
   gedreht. Beispiel UG: RZ_PLPR rot=270 ref (80989, 11556) und (83929, 18141).
6. **SL-Kette im innenliegenden Kellergang** alle ~4–5 m (Typ G). Beispiel UG:
   SL (83871, 23151) → SL (83871, 27255) = 4.1 m Abstand auf derselben Achse.
7. **Controller/SV-Anlage im UG-Technikraum**, 1× je Objekt:
   STANDARDMASK_SYSTEM „Anlage A" ref (90443, 29407).
8. **Außen-Fluchtweg als Sichtverbindungskette** mit Typen der
   20-m-Erkennungsweite-Klasse (Fachplaner-Typenwahl, nicht Normwert).

### Zweite Sichtung des Fachplaner-Plans (2026-09-09) — bisher ungenutzte Teile

Erhoben 2026-09-09, alles mit `ezdxf` gemessen (temporäre Skripte, gelöscht). Referenz
= `DIN-Notbeleuchtungspläne(Beispiele)/din_support_ReMi_Barawitzkagasse_28.04.2026.dxf`.
Architektur = `Projekte/Barawitzkagasse/*.dxf`. Engine-Lauf = `build_default_bundle()`
(raum.parse + platzierer.place), Vergleich = `scripts/plan_pruefen.py:779` / `:803`.
**Keine Normwerte, keine abgeleiteten Platzierungsregeln — nur beobachtete Muster mit Messwert.**

#### 1a. Der Plan hat 7 Geschoss-Frames auf 2 Blättern, nicht 3

Die 2 `IMAGE`-Entities des Modelspace sind die beiden gescannten Unterlagen (damit ist
die oben erwähnte fehlende Xref benannt):

| Xref-Dateiname | IMAGE insert (mm) | Größe (mm) | Frames | Leuchten |
|---|---|---|---|---|
| `.\Xref\240319_UG-OG1 Elektro Toga 2_1.jpg` | (0, 0) | 119 123 × 84 268 | 3 | 32 + 1 Controller |
| `.\Xref\240319_OG2-DD Elektro Toga 2_1.jpg` | (0, 97 067.75) | 119 123 × 84 268 | 4 | 14 |

Gemessene Frame-Fenster (REF-mm) und Bestückung — die drei ersten sind die oben
dokumentierten, die vier letzten waren bisher nicht erfasst:

| Frame | Fenster x | Fenster y | Leuchten-Extents | n | Typen |
|---|---|---|---|---|---|
| OG1 (Blatt 1 links) | 15 000–45 000 | 5 000–45 000 | 22 438–30 074 / 17 364–32 515 | 5 | B, E, A, H(SL), A |
| EG (Blatt 1 mitte) | 45 000–70 000 | 5 000–45 000 | 53 943–63 659 / 16 941–36 264 | 11 | 5×A, 3×B, F, H(SL), I(SL) |
| UG (Blatt 1 rechts) | 70 000–100 000 | 5 000–45 000 | 77 846–91 497 / 11 556–36 728 | 16 + Controller | 5×A, 3×C, 2×D, 6×G(SL) |
| F4 (Blatt 2 rechts unten) | 70 000–100 000 | 105 000–140 000 | 80 898–86 314 / 113 690–130 692 | 5 | B, E, A, H(SL), A |
| F5 (Blatt 2 mitte unten) | 45 000–70 000 | 120 000–140 000 | 56 589–61 564 / 128 956–130 914 | 3 | A, H(SL), A |
| F6 (Blatt 2 mitte oben) | 45 000–70 000 | 150 000–170 000 | 56 272–61 133 / 157 590–159 517 | 3 | A, H(SL), A |
| F7 (Blatt 2 links oben) | 15 000–45 000 | 150 000–170 000 | 31 147–32 722 / 158 051–160 602 | 3 | H(SL), A, A |

Summe 47 Inserts = 46 Leuchten + 1 Controller ✓ (Legenden-Duplikate liegen bei
x = 155 755, y 54 480–66 291, außerhalb beider Bilder — der Filter „Layer
`din_SIBEL_70_*` ignorieren" reicht, ein Fenster-Filter fängt sie zusätzlich ab).

**Korrektur zu Muster 3 oben:** die dort als „OG1" zitierten Beispielkoordinaten
(56 589, 128 956) / (58 805, 128 966) / (61 564, 130 914) liegen auf **Blatt 2**
(Frame F5), nicht im dokumentierten OG1-Frame (Blatt 1, y 17 364–32 515). Mit dem
OG1-Offset (−18.34, −38.66) sind sie nicht verdrahtbar; die als „OG2" zitierte
Wiederholung (56 272, 157 590) ist Frame F6.

#### 1b. Neue Muster (Fortsetzung der Nummerierung aus Abschnitt 1)

**Muster 9 — Stiegenhaus-Kit ist mechanisch, nicht „ungefähr".**
Jede der 6 SL Typ H im ganzen Plan sitzt vom nächsten RZ aus in **+X-Richtung,
Δx = +2.135…+2.242 m, |Δy| ≤ 0.021 m, identische Rotation 180°**, Partner immer
ein **RZ Typ A** (5× `RZ_PL`, 1× `RZ_PR`). Beispiel EG: RZ_PR Typ A (56 894, 30 254)
rot 180 → SL Typ H (59 029, 30 262) rot 180, Δ = (+2.135, +0.008).
Einziger Ausreißer: Frame F7 (31 179, 158 057) → (32 722, 158 051), Δ = (+1.542, −0.006).
(Präzisiert Muster 3, das nur „SL 2.2 m daneben" sagt und Achsenrichtung und
Rotationsgleichheit offen lässt.)

**Muster 10 — SL Typ I ist ein Einzelfall, kein Muster für „jeden Endausgang".**
Typ I kommt im ganzen Plan **1×** vor: (62 773, 36 264), +0.352 m in +Y über dem
RZ_PU Typ A (62 766, 35 912) des Hauseingangs. Kein zweiter Endausgang im Plan trägt
eine Außen-SL. (Muster 2 formuliert „über jedem Endausgang" — belegt ist n = 1.)

**Muster 11 — der Typenbuchstabe hängt am Geschoss, nicht am Ort.**
Typ G (SL, `BASIC 2 E-LED RZ1/AP DA`) ausschließlich im UG-Frame (6/6). Typ C
(`…RZ1/AP WA`) ausschließlich UG (3/3, alle `RZ_PU`). Typ D (`…RZ2 DA`) ausschließlich
UG (2/2, beide `RZ_PLPR` rot 270). Typ H (SL) ausschließlich als Kit-Partner aus
Muster 9 (6/6). Typ B/E ausschließlich in EG + Obergeschoss-Frames. Typ A ist der
Allzweck-RZ (20×). Beispiel: UG-SL (83 871, 23 151) Typ G vs. EG-SL (59 029, 30 262) Typ H.

**Muster 12 — RZ hängen an der Wand, SL nicht.**
Wandabstand zum Polygon des enthaltenden Raums (unsere Raumerkennung):
alle RZ, die in einem erkannten Raum liegen, **0.02–0.82 m** (EG: 0.02 / 0.02 / 0.07 / 0.25 m;
UG: 0.13 / 0.19 / 0.19 / 0.21 / 0.27 / 0.31 / 0.82 m). Genau **zwei** Ausnahmen, beide
`RZ_PLPR` Typ D im UG: (6.08, −19.52) → 4.17 m und (3.14, −26.10) → 1.10 m frei in der Fläche.
Die SL Typ G stehen ebenfalls frei: (6.02, −14.51) → 5.17 m, (6.02, −10.40) → 2.84 m.

**Muster 13 — Korrektur zu Muster 6: die UG-SL-Kette liegt in der GARAGE.**
Mit dem UG-Offset landen SL Typ G (6.02, −14.51) und (6.02, −10.40)
beide in `raum_32` **GARAGE** (nicht in einem Kellergang), exakt auf derselben
x-Achse, Δ = 4.11 m, je 2.55 / 2.75 m zur nächsten Tür.

**Muster 14 — Korrektur zu Muster 7: der Controller steht in der Garage.**
`STANDARDMASK_SYSTEM` „Anlage A" (90 443, 29 407) → our (12.59, −8.25) liegt in
`raum_32` GARAGE, 2.18 m zur nächsten Tür, 2.03 m zur nächsten Wand — nicht in
einem als Technikraum erkannten Raum.

**Muster 15 — im EG bestückt der Fachplaner ausschließlich Erschließung + Außen.**
Alle 11 EG-Leuchten liegen in/an `raum_35` STIEGENHAUS (6), `raum_37` STIEGENHAUS (1),
`rest_1` SCHACHT-Rand (1), `raum_43` TERRASSE (1) sowie 2 an der Hauseingangs-Sehne.
**Null** Symbole in Wohnung, Kinderwagenraum, Waschküche, Abstellraum oder Lift.
Beispiel Gegenprobe: unsere Leuchte (13.19, −4.87) sitzt im KINDERWAGENRAUM —
nächste Referenzleuchte 2.08 m entfernt.

**Muster 16 — RZ-Übergewicht.** EG-Frame 9 RZ : 2 SL; Gesamtplan 33 RZ : 13 SL.
Unsere EG-Ausgabe ist umgekehrt: 3 RZ : 4 SL.

**Muster 17 — 90°-Raster gilt für alle 47 Inserts**, nicht nur die 33 RZ:
Rotationen 0° (18×), 90° (6×), 180° (17×), 270° (5×), 360° (1×, `RZ_PL` bei
31 147/160 602 — numerisch ≈ 0°).

**Befund Symbol-Mapping:** 46 von 47 Inserts heißen `STANDARDMASK_*`, **einer** heißt
`STANDARD_RZ_PLPR` (EG, Typ F, (61 511, 18 056), rot 270). Die Legende führt zusätzlich
`STANDARD_RZ_00`. Ein Mapping auf das Präfix `STANDARDMASK_` allein verliert dieses Symbol.

#### 1c. Die 9 fehlenden und 5 überzähligen EG-Leuchten, einzeln

Basis: `Projekte/_eingang/Barawitzka_EG.dxf` (md5 `01752aef…`, **byte-identisch** mit
`Projekte/Barawitzkagasse/415_260415_PP_VA_1_3 0 EG.dxf`), Modell: 50 Räume, 106 Türen,
28 Anker, 1 Ausgang; Engine setzt **7** Leuchten (3 rz / 4 sicherheitsleuchte).

**Fehlend (Fachplaner setzt, wir nicht)** — je Zeile: unsere m-Koordinate, Raum,
nächste Tür, nächster Anker, Abstand zur nächsten eigenen Leuchte:

| # | Symbol / Typ | our (m) | Raum (unser Modell) | d Tür | nächster Anker | d nächste eigene |
|---|---|---|---|---|---|---|
| 1 | `RZ_PR` B rot 90 | (5.50, −22.10) | raum_37 STIEGENHAUS, Wand 0.07 m | 0.76 m (tuer_5) | AUSTRITT @0.51 m | 6.01 m |
| 2 | `STANDARD_RZ_PLPR` F rot 270 | (13.07, −20.98) | rest_1 SCHACHT, Wand 0.25 m | 0.97 m (durchgang_8) | TUER @1.04 m | 1.68 m |
| 3 | `RZ_PR` B rot 0 | (7.60, −19.56) | raum_43 **TERRASSE** (AUSSEN, ist_fluchtweg=False) | 0.92 m (tuer_6) | ANTRITT @2.50 m | 5.16 m |
| 4 | `RZ_PU` B rot 0 | (14.38, −15.09) | kein Raum (0.25 m neben rest_2) | 0.75 m (tuer_12) | AUSTRITT @0.65 m | 7.69 m |
| 5 | `RZ_PL` A rot 270 | (15.19, −13.52) | 0.05 m außerhalb raum_35 | 1.23 m (tuer_12) | AUSTRITT @0.28 m | 7.02 m |
| 6 | `RZ_PR` A rot 180 | (8.45, −8.79) | 0.01 m außerhalb raum_35 | 0.61 m (durchgang_2) | ANTRITT @0.96 m | 4.11 m |
| 7 | `SL` H rot 180 | (10.59, −8.78) | raum_1 (unklassifiziert) | 0.71 m (durchgang_1) | ANTRITT @1.66 m | 2.31 m |
| 8 | `RZ_PL` A rot 270 | (15.22, −7.91) | 0.08 m außerhalb raum_35 | 1.00 m (durchgang_58) | TUER @1.00 m | 3.08 m |
| 9 | `RZ_PR` A rot 0 | (8.14, −6.24) | raum_35 STIEGENHAUS, Wand 0.02 m | 1.11 m (tuer_30) | AUSTRITT @0.24 m | 4.20 m |

**Überzählig (wir setzen, Fachplaner nicht):**

| # | unsere Leuchte | our (m) | Raum | Begründung im Contract (`norm_quelle`) | d nächste Referenz |
|---|---|---|---|---|---|
| 1 | SL `sicherheitsleuchte_aufheller` | (11.44, −23.01) | raum_37 STIEGENHAUS, AUSTRITT @0.25 m | EN 1838 §4.1 | 2.60 m |
| 2 | RZ `notlicht_ks_stiege_unten` rot 180 | (12.34, −22.50) | rest_1 SCHACHT-Rand | EN 1838 §4.2.1 | 1.68 m |
| 3 | SL `sicherheitsleuchte_aufheller` | (12.23, −7.16) | raum_35 STIEGENHAUS | EN 1838 §4.1 | 2.31 m |
| 4 | RZ `notlicht_ks_stiege_unten` rot 0 | (13.19, −4.87) | **raum_33 KINDERWAGENRAUM**, an tuer_24 (0.00 m) | „Referenz-Praxis: Technik-/Nebenraum-SL an der Tür" | 2.08 m |
| 5 | SL `sicherheitsleuchte_aufheller` | (10.80, −2.09) | **raum_33 KINDERWAGENRAUM** | dieselbe Fachpraxis-Regel | 3.60 m |

**Muster F1 — es ist kein Toleranzproblem, sondern ein Mengen-/Rollenproblem.**
Toleranz-Sweep mit denselben Funktionen (`_referenz_match`): 1.0 m → 2/11; 1.5 m → 2/11;
2.0 m → 2/11; 2.5 m → 3/11; 3.0 m → 3/11. Ohne Rotationsfilter: 3.0 m → 4/11.
Auch mit 3 m Fangradius bleiben 7 der 11 Referenzleuchten ohne Gegenstück, weil die
Engine im EG nur 7 statt 11 Leuchten setzt und 5 davon an anderen Stellen.

**Muster F2 — der Fachplaner besetzt Treppenlauf-Enden, wir nicht.**
6 der 9 Fehlenden liegen **≤ 1.05 m** an einem `ANTRITT`/`AUSTRITT`-Anker, den unser
RaumModell bereits liefert (#9 @0.24 m, #5 @0.28 m, #1 @0.51 m, #4 @0.65 m, #6 @0.96 m,
#8 TUER @1.00 m). Gesamtbild über alle 28 Anker: **14/28 Anker tragen eine
Referenzleuchte ≤ 1.5 m, aber nur 7/28 eine eigene.** Die Anker existieren also, die
Platzierung konsumiert sie nicht (Befund an `platzierung/` — nicht geändert).

**Muster F3 — der Fluchtweg über den Hof fehlt uns komplett.**
Fehlend #3 (7.60, −19.56) liegt in `raum_43` TERRASSE, `nutzungsklasse=AUSSEN`,
`ist_fluchtweg=False`; Fehlend #1 (5.50, −22.10) liegt im zweiten Stiegenhaus `raum_37`,
das im Modell **keinen** `ausgaenge`-Eintrag hat (einziger `final_exit` ist
`exit_tuer_27` bei (14.90, −2.93)). Der Fachplaner führt dort einen zweiten Fluchtweg;
unser Modell kennt ihn nicht.

**Muster F4 — unsere SL sitzen an der falschen Stelle des Kits.**
Überzählig #1 und #3 sind Aufheller am Treppen-`AUSTRITT` (0.25 m bzw. am Durchgang);
die Referenz kennt SL im Stiegenhaus nur als +2.1 m-Partner eines RZ (Muster 9).
Beleg: (12.23, −7.16) vs. Referenz-SL (10.59, −8.78) = 2.31 m daneben.

**Muster F5 — 2 der 5 Überzähligen kommen aus einer Fachpraxis-Regel, die die Referenz
nicht stützt.** Überzählig #4/#5 tragen `norm_quelle = "Referenz-Praxis: Technik-/
Nebenraum-SL an der Tür"` und liegen im KINDERWAGENRAUM; der Fachplaner bestückt im
gesamten EG keinen einzigen Nebenraum (Muster 15). Befund an `platzierung/fachpraxis.py`
— gemeldet, nicht geändert.

#### 1d. Verdrahtbarkeit der UG-/OG1-Offsets — gemessen

Die Architektur-DXF liegen vor, unter diesen Namen:

| Geschoss | Datei in `Projekte/Barawitzkagasse/` | Größe |
|---|---|---|
| UG (Keller) | `415_260415_PP_VA_1_2 -1 KG.dxf` | 14.6 MB |
| EG | `415_260415_PP_VA_1_3 0 EG.dxf` | 12.9 MB (= `_eingang/Barawitzka_EG.dxf`, md5-identisch) |
| OG1 | `415_260415_PP_VA_1_4 1 St.dxf` | 9.8 MB |
| Blatt-2-Frames (F4–F7) | `…_1_5 2 St`, `…_1_6 3 St`, `…_1_7 1 DG`, `…_1_8 2 DG`, `…_1_9 DD STG1` | — |

`Projekte/_eingang/` enthält heute nur `Barawitzka_EG.dxf` — UG/OG1 müssten aus
`Projekte/Barawitzkagasse/` gezogen werden (oder dorthin gespiegelt).

**UG — verdrahtbar, aber der Vergleich bringt fast nichts.** Mit Offset (−77.85, −37.66)
fallen **14 von 17** Referenzpunkten in einen erkannten Raum (Wandabstand 0.13–0.31 m
bei den wandnahen RZ), 13 liegen ≤ 2.8 m an einer erkannten Tür. Aber:
`raum.parse` liefert für das KG **0 Anker, 0 Ausgänge, 0 Stiegenhäuser**, die Engine
setzt **3** Leuchten für 16 Referenzleuchten → Trefferquote bei 1 m Toleranz **1/16**.
Parse-Zeit 197 s.

**OG1 — Offset trägt nur den Stiegenbereich.** Mit Offset (−18.34, −38.66) landen die
3 Kit-Leuchten sauber: RZ_PL Typ A (6.87, −8.07) an `ANTRITT` @0.25 m in `raum_5`
STIEGENHAUS, SL Typ H (9.12, −8.05) @0.17 m an einer Tür, RZ_PLPR Typ A (11.73, −6.15)
@0.50 m neben dem Raumrand. Die beiden anderen (RZ_PL Typ B (4.10, −21.30) und
RZ_PLPR Typ E (10.28, −21.06)) liegen **5.75 m bzw. 4.72 m außerhalb jedes erkannten
Raums**. Das „1 St"-DXF ist 186 m breit (EG: 80 m) — der Frame deckt offenbar nur einen
Teil davon. Engine setzt 13 Leuchten; 1/5 Referenzleuchten hat eine eigene ≤ 1 m.
Parse-Zeit 106 s.

**Fazit zur Verdrahtung von `_REFERENZ_FRAME` (`scripts/plan_pruefen.py:767`):**
technisch verdrahtbar sind heute **UG und OG1** (Fenster oben in 1a, Offsets aus der
Tabelle „Frame → unser PP_2-Plan"), und mit denselben Fenstern auch F4–F7, sobald deren
Offsets gemessen sind. Die Trefferquote würde dadurch **fallen, nicht steigen**
(EG 2/11, UG 1/16, OG1 1/5 → 4/32 ≈ 13 % statt 18 %). Der 80-%-Zieltest wird durch
mehr Frames nicht erreichbarer; er wird ehrlicher. Zusätzlich zu beachten:
3 Geschosse = ~350 s Parse-Zeit, der Zieltest braucht dafür eine session-weite
Fixture oder gecachte RaumModelle.

---

## 2. Muster aus den 6 Beispielbildern

Alle in `DIN-Notbeleuchtungspläne(Beispiele)/`, selbst gesichtet 2026-09-07.

### `OVE-Richtlinie-R-12-2_Bild-8.9.jpg` (OVE R 12-2:2019 Bild 8.9, Beispiel 3)

- Schema-Schnitt: **je Geschoss eine Kette von SL** entlang des Ganges, RZ (grüner
  Pfeil) am Gang-Ende **Richtung Treppenhaus**.
- **Treppenhaus als eigener Strang**: SL je Podest/Halbgeschoss, Pfeile abwärts.
- **CPS-Anlage im Keller** in „abgeschlossener elektrischer Betriebsstätte",
  Steigschacht-Verkabelung je Geschoss als eigener Brandabschnitt (Anmerkung im
  Bild: E30-Dosen, TRVB 110 B).

### `LST_Notlicht.jpg` (licht.de, Gebäudeschnitt-3D)

- **RZ über jeder Tür in Fluchtrichtung** (auch Zwischentüren im Gang), SL an der
  Decke der Raummitte — Funk-Überwachungssymbolik an jeder Leuchte.
- **Treppenhaus: RZ an der Tür jedes Geschosses** + SL über den Läufen.
- **Zentrale (Batterie + Controller) im EG/UG-Technikbereich**, beide Wandgeräte
  nebeneinander.

### `uds-fluchtweglenkung-simulation.jpg` (dynamische Fluchtweglenkung, 3D-Sim)

- **Adaptive RZ**: gesperrte Richtung = rotes X-Zeichen, freigegebene Richtung =
  grüner Pfeil — RZ an jedem **Gangknoten paarweise** (je Laufrichtung eines).
- **Bodennahe SL-Punkte in Kette** entlang der Gang-Mittellinie (regelmäßiger
  Abstand), sichtbar als Punktreihe im geführten (grün markierten) Weg.
- RZ „Pfeil unten" **direkt am Ausgangs-/Türsturz**, Pfeil in Durchgangsrichtung.

### `mobile_krankenhaus_erhoeht.jpg` (licht.wissen-Stil, Krankenhaus „erhöhte" Sibe)

- **Lux-Beschriftung je SL** (0,5 lx Allgemein, 1 lx Gang, 5 lx Sonderstellen,
  15 lx Behandlungsplatz) — die Sonderstellen (Treppe, Erste-Hilfe-Kasten =
  grünes Kreuz-Symbol, Feuerlöscher = rotes Symbol) bekommen **eigene SL davor**.
- **RZ an jeder Gang-Verzweigung und über jeder Fluchttür**, WC-Trakt mit eigenem
  RZ „Pfeil unten" je Kabinenzeile.
- **Außenbereich vor dem Endausgang** bekommt eine eigene Leuchte (0,5 lx-Feld
  außerhalb der Fassade).

### `mobile_schule_erhoeht_2021.jpg` (licht.wissen-Stil, Schule)

- **Gang als Rückgrat**: 1-lx-SL-Kette in regelmäßigem Raster über die volle
  Ganglänge, Klassenräume je 2–4 SL (0,5 lx) an den Raum-Diagonalen.
- **Beide Stiegenhäuser symmetrisch bestückt**: RZ+SL am Antritt, 1-lx-Leuchte
  auf den Läufen, 5-lx-Punkt an der untersten Stufe (Typ-Beschriftung „5 lx").
- **Erste-Hilfe-/Brandschutz-Sonderstellen** (grünes Kreuz im Chemiesaal-Vorraum,
  rote Melder an den Stiegen) mit eigener davor gesetzter Leuchte.

### `csm_16_lw10_47_INO_Visualisierung_94461653fe.jpg` (INOTEC/licht.de, Monitoring-Grundriss)

- **Sparsame RZ-Setzung im Flur-Rückgrat**: nur an Knoten und Richtungswechseln
  (4 RZ + 3 Antipanik-Punkte für einen ganzen Riegel) — Überwachungs-Software
  zeigt Status je Leuchte (rot = gestörte Leuchte).
- **RZ paarweise gegenläufig am selben Flurpunkt** (links/rechts-Kombination am
  mittleren Knoten), Pfeilrichtung folgt der jeweils kürzeren Richtung zum Ausgang.
- **Treppenhaus-Kern: RZ „Pfeil unten + Lauffigur" direkt am Treppenantritt**.

---

## 3. Quellenliste (`knowledge/`)

**`knowledge/INDEX.md` ist die vollständige, generierte Landkarte des Wissens-Korpus
(`python scripts/wissen_index.py`); diese Liste hier hebt daraus nur die für die
Platzierung relevanten Quellen hervor** — sie ersetzt den Index nicht und ist nicht
vollzählig gepflegt.

Kurzaussage = wofür die Quelle bei Platzierungsfragen taugt; Fundstelle = Datei
(+ Abschnitt). **Keine Normwerte aus dieser Tabelle ableiten** — Werte immer in der
Quelle selbst nachschlagen und mit Fundstelle zitieren.

| Pfad | Kurzaussage | Fundstelle |
|---|---|---|
| `knowledge/extracted/EN_1838_notbeleuchtung.md` | Basis-Norm: Lux-Werte, Erkennungsweite l=z·h, Pflicht-Betonungspunkte des Fluchtwegs | §4.1 (Fluchtweg), §4.1.2 (Betonungspunkte a–j), §5 (RZ) |
| `knowledge/extracted/Fachinfo_E08_Arbeitsstaetten.md` | Wann Sicherheitsbeleuchtung in AT-Arbeitsstätten Pflicht ist (subsidiär zu E 8101/R 12-2/OIB 2) | Kopf „Einordnung" (S. 1) |
| `knowledge/extracted/OVE_E_8101_niederspannungsanlagen.md` | Elektrische Ausführung Sicherheitszwecke (Speisung, Stromkreise) | Abschnitte 560 + 7-718 |
| `knowledge/OVE-Richtlinie R 12-2 AC 2019-07-01.pdf` | Anlagen-Ausführung Sicherheitsbeleuchtung AT; Ausführungs-Beispiele mit baulichen Maßnahmen | Bild 8.9 (Beispiel 3, siehe Abschnitt 2) |
| `knowledge/sonstiges Wissen Notbeleuchtung/vorschriftenkurzuebersicht-at.pdf` | AT-Vorschriften-Überblick (welche Regel wofür) auf einer Seite | Gesamtdokument |
| `knowledge/sonstiges Wissen Notbeleuchtung/vorschriftenkurzuebersicht_de.pdf` | DE-Pendant — nur zum Abgleich, nicht AT-bindend | Gesamtdokument |
| `knowledge/extracted/PLATZIERUNGS_KONZEPTE.md` | Das Planer-Denkmodell hinter den Strategien (Schicht-1-Anker, Tür-Regel) | „Schicht-1-Anker" |
| `knowledge/extracted/PROFI_DIN_PLAN_UND_VORSCHRIFTEN.md` | Erst-Digest des Barawitzka-Referenzplans + Vorschriften-Scans | §1 (Plan-Analyse) |
| `knowledge/extracted/PRODUKTE_SCHRACK_DIN.md` | Produktfamilien (BASICsc/CONCEPTsc, CMR) hinter den Typen A–I | BASIC-2/CONCEPT-2-Abschnitte |
| `knowledge/extracted/Handbuch_NotSicherheitsbeleuchtung_2026.md` | INOTEC-Planungs-Blaupause inkl. dynamischer Fluchtweglenkung | „Planungsregeln-Tabelle", „Zitierte Norm-Werte (Quelle-der-Quelle)" |
| `knowledge/extracted/GSYSTEMS_Planungshandbuch.md` | Hersteller-Planungshandbuch (Referenz-Praxis) | „Planungsregeln-Tabelle", „Zitierte Norm-Werte (Quelle-der-Quelle)" |
| `knowledge/extracted/Kaufel_Planungshandbuch.md` | DE-Planungshandbuch — nur EN-identische Teile für AT nutzen | „Relevanz für die Engine" (DE-only-Hinweis), „Planungsregeln-Tabelle" |
| `knowledge/extracted/LichtWissen_10_Notbeleuchtung.md` | DE-Branchenpublikation, Bildvorlagen (mobile_*-Bilder oben) | „Planungsregeln-Tabelle", „Zitierte Norm-Werte (Quelle-der-Quelle)" |
| `knowledge/extracted/ONL_Normen_AT.md` | Zumtobel-Zusammenfassung der AT-Norm-Lage (Sekundärquelle) | „Regel-Tabelle", „Zitierte Norm-Werte (Quelle-der-Quelle)" |
| `knowledge/extracted/ANALYSE_Baufeld_E2_Notbeleuchtung.md` | Referenz-Praxis eines realen Planers vs. EN 1838 (Baufeld E2) | §1 „Befund (extrahierte Platzierung)", §2 „Warum so platziert — Abgleich mit EN 1838" |
| `knowledge/extracted/FLUCHTWEG_AUSHANG_REFERENZ.md` | Zimmeraushang-Referenz (Darstellungs-Konventionen) | §1 „Aufbau des Aushangs", §3 „AT-Norm-Vergleich" |
| `knowledge/extracted/MUTHGASSE_POLIERPLAN_BRANDSCHUTZ.md` | Muthgasse-Polierpläne: Brandschutz-Gerüst, 6. CAD-Familie | §1 (vorgerechnete Fluchtweglängen FLW-L), §2 „Brandschutz-Inventar", §3 (AIA-Layer-Standard) |
| `knowledge/extracted/LB_ANALYSE_beispiele.md` | Was reale LBs vorschreiben (Input 2, übersteuert Norm-Defaults) | „Kernbefund — LB übersteuert Norm", „Extrahierte LB-explizite Felder" |
| `knowledge/extracted/STROMKREISNUMMER_DWG.md` | Stromkreis-Nummernschema des din-Planungstools | „Kernbefund: das Nummern-Schema", Voll-Analyse §3 „Attribut-Schema" |
| `knowledge/extracted/ESV_2012.md`, `ETG_1992.md`, `ETV_2002_2010_2020.md`, `Nullungsverordnung.md`, `RIS_Standesregeln_Elektrotechnik.md`, `Sicherheitsvorschriften_Elektro.md`, `OENORM_E_8014.md`, `OVE_E_8015.md`, `OVE_E_8350.md`, `OVE_E_8351.md` | Rechts-/Elektro-Rahmen (kein Platzierungs-Wissen) | jeweils Kopf „Relevanz für die Engine" |
| `knowledge/extracted/WETTBEWERB_ENDRA_AI.md` | Wettbewerber-Einordnung (kein Platzierungs-Wissen) | §4 „Vergleich mit unserer Engine" |
| `knowledge/extracted/README.md` | Wegweiser durch die Digests (Einstiegs-Reihenfolge, Bild-Lehren-Hinweis) | Kopf + Einstiegs-Kasten |

### 3a. Bild-Lehren (`knowledge/extracted/bildlehren/`) — 7 Digests + 3 JPG

Visuelle Sichtung derselben PDFs Seite für Seite; erfasst genau das, was im
Text-Digest nicht steht (Anordnungs-Schemata, Beispiel-Grundrisse, Tabellenbilder).
Die 3 Gold-Bilder `beispiel_krankenhaus_luxzonen.jpg`, `beispiel_schule_luxzonen.jpg`,
`beispiel_OVE_R12-2_Bild8-9.jpg` liegen im selben Ordner.

| Pfad | Kurzaussage | Fundstelle |
|---|---|---|
| `bildlehren/Bildlehren_EN1838_E08.md` | Die 4 Bilder + 1 Tabelle der EN 1838:2019 und die E-08-Bilder/Tabellen, bildweise beschrieben (Blendungs-Zonen, Erkennungsweiten-Geometrie) | „EN 1838 — Bild für Bild" (Bild 4 = Erkennungsweite), „E-08 — visuelle Konzepte" |
| `bildlehren/Bildlehren_ONL_Zumtobel.md` | AT-Broschüre bildweise: Normen-Rangordnung, Sichtbarkeits-Isometrie, Rettungsweg-Geometrie | „S.31 — Isometrie ‚Sichtbarkeit für Evakuierungsmaßnahmen'", „S.32 — Rettungsweg-Geometrie" |
| `bildlehren/Bildlehren_INOTEC.md` | Hersteller-Handbuch bildweise: RZ an/über der Tür, Treppenraum-Regel, hervorzuhebende Stellen der 2025er-Fassung | „S.44 — Notausgangstür", „S.46 — Treppen + Außenbereich", „S.48 — Treppenraum-Regel" |
| `bildlehren/Bildlehren_GSYSTEMS.md` | Hersteller-Handbuch bildweise: Fluchtweg als Flächen-Layer im Grundriss, Erkennungsweite + Blickwinkel, Montagehöhen-Bänder (DE-only-Teile markiert) | „S.89 — Grundriss ‚Flucht- und Rettungswege'", „S.165", „S.166" |
| `bildlehren/Bildlehren_Kaufel.md` | DE-Planungsgrundlagen bildweise: Anordnung an Ausgang/Notausgang/Treppe, Kreuzung, Blendungs-Geometrie | „S. 43 — Abb. 11/12/13", „S. 44 — Abb. 14/15/16", „S. 45 — Abb. 17/18" |
| `bildlehren/Bildlehren_LichtWissen10.md` | DE-Branchenheft bildweise: Piktogramm-Matrix der hervorzuhebenden Stellen, Flur-Kreuzung/Richtungsänderung, Erkennungsweiten-Diagramm | „S.10 — Hervorzuhebende Stellen nach DIN EN 1838 (Abb. 07)", „S.23 — Erkennungsweiten-Formel" |
| `bildlehren/Bildlehren_Beispielplaene_Web.md` | Auswertung der 3 Gold-Bilder: Lux-Zonierung je Raumtyp, Antipanik als Raster im Großraum, OVE-R-12-2-Topologie | „Schlüssel-Abbildungen" (je Bild ein Unterabschnitt) |

### 3b. Aus dem elektro-planer-Bestand (`knowledge/extracted/aus_elektroplaner/`)

| Pfad | Kurzaussage | Fundstelle |
|---|---|---|
| `aus_elektroplaner/README.md` | Was gefiltert übernommen wurde + Hierarchie-Einordnung der 5 Digests | „Die 5 gefilterten Digests" |
| `aus_elektroplaner/OENORM_E_8002_Menschenansammlungen.md` | AT-Antwort auf das „WANN" (Erforderlichkeit nach Nutzung/Schwelle); historisch, 2019 in OVE E 8101 überführt | „Regel-Tabelle (Notbeleuchtungs-relevant)", Detail-Digest T1 §4.3.1 |
| `aus_elektroplaner/OENORM_E_8007_medizinisch.md` | Medizinische Räume: Anwendungsgruppe AG 0/1/2 → Umschaltzeit + Betriebsdauer | „Regel-Tabelle (Sicherheitsbeleuchtung/-stromversorgung medizinisch)", „Raumtyp → Anforderung (medizinisch)" |
| `aus_elektroplaner/OVE_E_8101_2025_Deltas.md` | Deltas der Ausgabe 2025 gegen 2019 (u.a. Verbot 560.7.13, Versammlungs-Schwelle, Anhang 56.A jetzt normativ) | „Delta-Tabelle", „Betriebsdauern Anhang 56.A (2025)" |
| `aus_elektroplaner/OVE_Fachinfos_E05_E06_E07.md` | AT-Fachinfos: Funktionserhalt der Leitungsanlagen (E-07), Bussysteme (E-06), Garagen (E-05) | „E-07 — Funktionserhalt Leitungsanlagen", „Regel-Tabelle" |
| `aus_elektroplaner/Schrack_Katalog_NotSicherheitsbeleuchtung.md` | Produktrealität der gerenderten Marke: Erkennungsweiten je Familie, Leuchtenabstände, Konvention Wand=RZ / Decke=SI | „Platzierungs-/Auslegungs-relevante Kennwerte", „Verknüpfung mit unserem Symbol-Mapping" |

### 3c. Original-PDF-Bestände (nicht als Digest erfasst)

| Pfad | Kurzaussage | Fundstelle |
|---|---|---|
| `knowledge/OIB-Richtlinien/` (Ausgabe Mai 2023, RL 1–7 + Sonderrichtlinien, PDF) | Bau-rechtliche Erforderlichkeit der Sicherheitsbeleuchtung je Nutzung | `OIB-Richtlinie 2 Brandschutz/oib-rl_2_ausgabe_mai_2023.pdf` Punkt 5.4 + Tabelle 6; ausgewertet in `docs/OIB_RL2_TABELLE6.md` |
| `knowledge/Österreichische Rechtsquelle/RIVOPLAN_Oesterreichische_Rechtsquellen_Notbeleuchtung_AT.pdf` | Eigene Arbeitskopie (**nicht amtlich**) zu AStV § 9 / § 13, ASchG §§ 20/21, KennV Anhang 1 Pkt. 1.4 | Gesamtdokument (10 S.); Einordnung in `docs/NORMQUELLEN_AT.md`, Abschnitt „Sonderfall" |
| `knowledge/OVE-Fachinformation/` (E-01…E-13, H02, PDF) | AT-Auslegungshilfen zu OVE E 8101 / ÖVE E 8002; notbeleuchtungsrelevant E-06/E-07/E-08 | `Fachinfo_E-06_Bussystem_2020-12.pdf`, `Fachinfo_E-07_Sicherheitsbeleuchtung_2020-12.pdf`, `Fachinfo_E-08_Sicherheitsbeleuchtung_Arbeitsstaetten_2021-04.pdf` |

### 3d. CAD-Symbol- und Photometrie-Quellen (`CAD_Symbole/`)

Kein Norm-, sondern Produkt-/Asset-Wissen — hier gelistet, weil Platzierungsfragen
regelmäßig darauf zurückgreifen. Messwerte und Deckungs-Tabellen dazu in Abschnitt 5.

| Pfad | Kurzaussage | Fundstelle |
|---|---|---|
| `CAD_Symbole/Notbeleuchtungssymbole.dxf` | **Kanonische** Symbol-Library (die einzige, auf die `NOTBELEUCHTUNG_SYMBOL_LIB` zeigen darf) | ADR-0002 `docs/adr/0002-kanonische-symbol-library.md`; Messwerte in Abschnitt 4a |
| `CAD_Symbole/E-Symbole.dxf` (+ `-clean.dxf`, `.dwg`, `.bak`, `_recover.dwg`) | Herkunfts-Referenz des Elektro-Planungs-Katalogs — **kein** Platzierungs-Asset, keine der Dateien kann die Library ersetzen | ADR-0002; Deckungs-Messung in Abschnitt 5.1 |
| `CAD_Symbole/photometrie/*.ldt` | EULUMDAT-Notbetriebs-Photometrie für den EN-1838-Lux-Nachweis (`platzierung/lux.py` via `i_cd_fn`) | Kopfzeilen-Messung + Zuordnung in Abschnitt 5.2 |
| `CAD_Symbole/photometrie/QUELLEN.md` | Herkunft/Audit-Trail der 4 LDT (Download-URLs, Produktseiten, Stand 2026-09-03) | Gesamtdokument; Abschnitt „In echten Lichtberechnungen verwendet" |

### 3e. Abgleich gegen `knowledge/INDEX.md` (2026-09-09) — hier bisher fehlend

Abgeglichen wurde jeder Eintrag des generierten Index gegen die Tabellen 3–3d.
Alle Digests aus `knowledge/extracted/` (inkl. `bildlehren/` und
`aus_elektroplaner/`) sind oben erfasst — **bis auf die folgenden**. Relevanz-Spalte
= Nutzen für Platzierungsfragen, nicht Wichtigkeit der Quelle an sich.

| Pfad | Kurzaussage | Relevanz für die Platzierung |
|---|---|---|
| `knowledge/extracted/LICHTBERECHNUNG_REFERENZ.md` | Digest dreier echter Profi-Notlicht-Lichtberechnungen (Relux + 2× DIALux, u. a. eine geprüfte), mit den dort verwendeten Berechnungs-Parametern und Leuchtentypen | **hoch** — einzige Kalibrier-Referenz für `platzierung/lux.py` / `deckung.py` gegen echte Nachweise |
| `docs/analyse/mollgasse_ug_notbeleuchtung.md` | Aus GU-Elektroplänen extrahierte, vom Barawitzka-Plan unabhängige zweite Notbeleuchtungs-Referenz (Mollgasse UG) inkl. Kalibrierungsprotokoll | **hoch** — zweiter Referenzplan zum Gegenprüfen der hier dokumentierten Muster |
| `src/notbeleuchtung/normwissen/data/platzierung_regeln.yaml` | Placement-Decision-Matrix (Enis' Lane, autoritativ) | **hoch** — die verbindlichen Regeln; Muster dieses Dokuments sind nur Beobachtung, nie Ersatz dafür |
| `src/notbeleuchtung/normwissen/data/raumtyp_regeln.yaml` | Raumtyp × Fluchtweg → NormAnforderung (autoritativ) | **hoch** — bestimmt, welcher Raum überhaupt bestückt wird (vgl. Muster 15) |
| `src/notbeleuchtung/normwissen/data/sonderstellen.yaml` | Typ-Katalog der hervorzuhebenden Stellen (EN 1838 §4.1.2, autoritativ) | **hoch** — Gegenstück zu den Sonderstellen-Beobachtungen in Abschnitt 2 |
| `src/notbeleuchtung/normwissen/data/en1838_grundwerte.yaml` | Norm-Grundwerte der EN 1838 (autoritativ, Single Source of Truth der Werte) | **hoch** — Werte immer hier bzw. im Contract nachschlagen, nie aus diesem Dokument |
| `src/notbeleuchtung/normwissen/data/regel_deckung.yaml` | Deckungs-Matrix Kanon-Raumtyp → Regelwerk (autoritativ) | mittel — sagt, welches Regelwerk je Raumtyp greift |
| `src/notbeleuchtung/normwissen/data/oib_rl2_tabelle6.yaml` | OIB-RL 2 Punkt 5.4 + Tabelle 6 als YAML (autoritativ) | mittel — Erforderlichkeit („ob"), nicht Platzierung („wo") |
| `src/notbeleuchtung/normwissen/data/ove_e8101_zusatz.yaml` | Belegte Zusatz-Anforderungen aus OVE E 8101 (autoritativ) | mittel — Ausführungs-/Verbots-Seite, Hard Stops |
| `src/notbeleuchtung/normwissen/data/lb_extraktion.yaml` | Vokabular + Muster für das LB-Parsing (2. Input) | keine — Parsing-Hilfsdaten, kein Platzierungs-Wissen |
| `knowledge/_extracted_text/` (Rohimport aus `elektro-planer`, mit eigenem `NOTBELEUCHTUNG_INDEX.md`) | Kompletter Roh-Textbestand, aus dem die Digests in `extracted/aus_elektroplaner/` gefiltert wurden | mittel — Nachschlage-Reserve; die gefilterten Digests (3b) sind der Einstieg |

Die übrigen Index-Abschnitte (ADRs, `docs/`-Entscheidungen, Handoffs) sind
Projekt-Steuerung, keine Wissensquelle für Platzierungsmuster, und bleiben hier
bewusst außen vor — Einstieg dafür ist `knowledge/INDEX.md` selbst.

### 3f. Noch ohne Digest (im Korpus vorhanden, kein Textextrakt)

Diese Dateien liegen im Repo, haben aber **keinen** Digest in `knowledge/extracted/`
und keinen Eintrag im generierten Index. **Keine Aussage über ihren Inhalt** — sie
sind hier nur als offene Erfassungs-Lücke geführt.

- `knowledge/OVE-Fachinformation/` — alles außer E-05/E-06/E-07 (Digest in 3b) und
  E-08 (Digest in Abschnitt 3): `8001_2.pdf`, `E-01_E100_Licht-Steckdosenstromkreise…`,
  `E-02_e8001_Korrekturen…`, `E-03_EN_219_USV-Systeme…`, `E-04_Hoehere_Ableitstroeme…`,
  `Fachinformation_E-09_Schutzbereich_SPD…`, `Fachinformation-E-10_Spannungsabfall…`,
  `Fachinfo_E-11_zu_vorbereitenden_weitergehenden_Untersuchungen…`,
  `OVE-Fachinformation_E13_Verwendung_Kabel_Leitungen…`,
  `OVE-Fachinformation_H02_202404.pdf`, `fachmeinung04.pdf`, `klemmen.pdf`,
  `OVE-IM12.pdf`.
- `knowledge/OIB-Richtlinien/` — sämtliche PDFs außer der in `docs/OIB_RL2_TABELLE6.md`
  ausgewerteten Stelle (RL 2, Punkt 5.4 + Tabelle 6): RL 1, RL 2 Abweichungen,
  RL 2.1/2.2/2.3, RL 3, RL 4, RL 5, RL 6 (beide Ordner), RL 7 Grundlagendokument,
  Begriffsbestimmungen, „Zitierte Normen", dazu die `aenderungen_*`- und
  `erlaeuterungen_*`-PDFs aller Richtlinien und die Excel-Tools der RL 6.
- `knowledge/OVE-Richtlinie R 12-2 AC 2019-07-01.pdf` — in Abschnitt 3 gelistet, aber
  nur über Bild 8.9 (Abschnitt 2) ausgewertet; kein Volltext-Digest.
- `knowledge/Österreichische Rechtsquelle/RIVOPLAN_Oesterreichische_Rechtsquellen_Notbeleuchtung_AT.pdf`
  — Arbeitskopie, kein Digest (Einordnung nur in `docs/NORMQUELLEN_AT.md`).
- `knowledge/sonstiges Wissen Notbeleuchtung/` — `vorschriftenkurzuebersicht-at.pdf`,
  `vorschriftenkurzuebersicht_de.pdf` (in Abschnitt 3 gelistet, ohne Digest),
  `DIN4708_Bedarfskennzahl Eichholzgasse .pdf`, `1.xlsx`.

---

## 4. Symbolkonvention unserer Library (selbst verifiziert)

Quelle: `CAD_Symbole/Notbeleuchtungssymbole.dxf` + `src/notbeleuchtung/symbols/`
(Mapping `schrack_symbol_mapping.yaml`, Insert-Pfad `inserter.py`/`library.py`).
Verifiziert 2026-09-07 per ezdxf-Geometrie-Dump **und** Render der drei
Pfeil-Blöcke (temporäres Skript, gelöscht).

Wichtig: `library.import_block()` **zentriert** jeden Block beim Import auf sein
Extents-Zentrum (die Roh-Blöcke tragen Basispunkt (0,0,0), aber Geometrie bei
~(2603, 2306)) — **effektiver Basispunkt = Symbol-Mitte**. Rotation ist DXF-CCW
um diesen Punkt.

| catalog_key | Block | Basispunkt (effektiv) | Pfeilrichtung bei rot=0 | Nullrichtung (Azimut) |
|---|---|---|---|---|
| `notlicht_ks_stiege`, `notlicht_ks_stiege_unten`, `notlicht_kw_garage` | `notbeleuchtung- richtungspfeil nach unten` | Symbol-Mitte | **−Y (unten)** | 270° |
| `notlicht_ks_stiege_links` | `notbeleuchtung-richtungspfeil nach links` | Symbol-Mitte | **−X (links)** | 180° |
| `notlicht_ks_stiege_rechts` | `notbeleuchtung-richtungspfeil nach rechts` | Symbol-Mitte | **+X (rechts)** | 0° |
| `sicherheitsleuchte_aufheller` | `aufheller notbeleuchtung` | Symbol-Mitte | richtungslos (Kreis) | — (`rotation_deg` = Optik-Azimut, ADR-0006) |
| `sicherheitsleuchte_spot` | `spot notbeleuchtung` | Symbol-Mitte | richtungslos | — (ADR-0006) |
| `antipanik_leuchte` | `notbeleuchtung- antipanikleuchte` | Symbol-Mitte | richtungslos | — |
| `gruppenbatterie_anlage` | `gruppenbatterie` | Symbol-Mitte | richtungslos | — |

**Folgerung (Rotations-Konvention, bindend für Pfeil-Blöcke):** Soll der Pfeil des
`unten`-Blocks in Azimut A zeigen, ist `rotation_deg = (A + 90) % 360`:
oben→180, rechts→90, links→270, unten→0. Genau so rechnen die Tür-Formel
(`atan2 + 90°`) und die `_ROT`-Tabelle der Sichtlinien-Strategie; `richtung_und_
rotation` in `platzierung/bausteine.py` ist seit dem Rotationsfix
(tests/platzierung/test_rotation_konvention.py) darauf geeicht. Die dedizierten
links/rechts-Blöcke zeigen bei rot=0 bereits in ihre Richtung (`is_directional`,
rotation=0). `richtung="gerade"` rendert der Inserter als Doppelpfeil
(links+rechts, gemeinsame Achsen-Rotation).

### 4a. Nachmessung 2026-09-09 (ezdxf, `.venv`)

Nachprüfung der Tabelle oben mit `ezdxf.bbox.extents` + Roh-Geometrie-Dump je Block
(temporäre Skripte, gelöscht). **Abschnitt 4 ist bestätigt** — Basispunkt-Aussage,
Pfeilrichtungen und Rotationsformel stimmen. Hier die Messwerte dazu und das, was
bisher fehlte.

#### 4a.1 Basispunkt — gemessen

Alle Blöcke der Library tragen `base_point = (0,0,0)`, die Geometrie liegt aber weit
davon entfernt. `library.import_block()` verschiebt jede Block-Definition einmal je
Output-Dokument auf ihr Extents-Zentrum (`_normalize_block_origin_recursive`,
`src/notbeleuchtung/symbols/library.py:213`), Guard
`tests/render/test_symbols_library.py::test_import_block_idempotent_and_origin_normalized`.
Nach dem Import liegt das Extents-Zentrum jedes gemappten Blocks bei (0.0000, 0.0000)
— gemessen für alle 10 Mapping-Einträge.

| Block | Roh-Extents-Zentrum (= Versatz Basispunkt→Symbolmitte) | Größe (units) | Zentrum nach `import_block` |
|---|---|---|---|
| `notbeleuchtung- richtungspfeil nach unten` | (2604.446, 2307.114) | 3.134 × 1.567 | (0.0000, 0.0000) |
| `notbeleuchtung-richtungspfeil nach links` | (2604.533, 2302.930) | 3.134 × 1.567 | (0.0000, 0.0000) |
| `notbeleuchtung-richtungspfeil nach rechts` | (2604.533, 2302.930) | 3.134 × 1.567 | (0.0000, 0.0000) |
| `aufheller notbeleuchtung` | (1841.317, 1485.400) | 1.849 × 1.849 | (0.0000, 0.0000) |
| `spot notbeleuchtung` | (0.000, 0.000) | 1.954 × 1.780 | (0.0000, 0.0000) |
| `notbeleuchtung- antipanikleuchte` | (3207.858, 2748.553) | 5.645 × 1.588 | (0.0000, 0.0000) |
| `gruppenbatterie` | (1842.553, 1457.554) | 8.195 × 4.457 | (0.0000, 0.0000) |
| `vorlage_legende` | (3405.497, 2575.203) | 415.016 × 550.546 | (0.0000, 0.0000) |

`spot notbeleuchtung` ist der einzige Block, der bereits im Roh-DXF origin-zentriert
ist (Repo-Nachbau 2026-09-06, ADR-0002).

#### 4a.2 Nullrichtung / Pfeilrichtung — gemessen an der Pfeil-Polygon-Geometrie

Der Pfeil jedes Richtungsblocks ist ein 7-Eck-HATCH-Pfad (Schaft + zwei Widerhaken
+ Spitze). Koordinaten relativ zum Block-Extents-Zentrum (= effektiver Basispunkt):

| Block | Widerhaken | Spitze | Pfeil-Azimut bei `rotation=0` | `_BLOCK_BASE_DEG` |
|---|---|---|---|---|
| `…richtungspfeil nach unten` | (±0.3009, −0.1755) | (0.0000, **−0.5767**) | **270°** (−Y) | 270.0 ✔ |
| `…richtungspfeil nach links` | (−0.3322, ±0.3009) | (**−0.7334**, 0.0000) | **180°** (−X) | 180.0 ✔ |
| `…richtungspfeil nach rechts` | (+0.3322, ±0.3009) | (**+0.7334**, 0.0000) | **0°** (+X) | 0.0 ✔ |

⚠️ **OCS-Falle beim `rechts`-Block:** seine HATCH-Entity trägt
`extrusion = (0, 0, −1)` (echter X-Spiegel des `links`-Blocks in DXF-Notation).
Wer die Hatch-Stützpunkte **roh** ausliest, ohne OCS→WCS zu transformieren, sieht die
Spitze bei x ≈ −5209.8 relativ zum Blockzentrum und schließt fälschlich auf einen
korrupten, nach links zeigenden Block. `ezdxf.bbox`, der `ezdxf`-Importer und AutoCAD
transformieren korrekt; selbstgebaute DXF-Leser/Renderer/Prüfskripte müssen es
ebenfalls tun. Die vier Rahmen-LINEs des Blocks tragen **keine** Extrusion — die
Mischung aus WCS-LINEs und OCS-HATCH im selben Block ist der eigentliche Stolperstein.

#### 4a.3 Rotationssymmetrie der „richtungslosen" Symbole

„Richtungslos" in der Tabelle oben heißt **kein Pfeil** — nicht rotationsinvariant.
Gemessene Seitenverhältnisse:

| Block | Größe (units) | rotationsinvariant? |
|---|---|---|
| `aufheller notbeleuchtung` | 1.849 × 1.849 (Kreis) | ja |
| `spot notbeleuchtung` | 1.954 × 1.780 | nein (Diagonal-X + 2 Sektoren) |
| `notbeleuchtung- antipanikleuchte` | 5.645 × 1.588 (3.6 : 1) | nein |
| `gruppenbatterie` | 8.195 × 4.457 (1.8 : 1) | nein |

Die Strategien schreiben für diese Keys `rotation_deg = 0.0`
(`flaechen_strategy.py:199`, `sonderstellen_strategy.py:90`, `fachpraxis.py:334`),
außer bei Fluchtweg-SL, wo `rotation_deg` per ADR-0006 der Optik-Azimut ist
(`deckung.py:153`) — dort dreht sich der längliche Block also sichtbar mit.

#### 4a.4 Layer & Farben der Library-Blöcke

Alle Blockgeometrie liegt auf Layer `0` (erbt also den INSERT-Layer). Explizite
Entity-Farben: Pfeil-Blöcke ACI 102, `aufheller notbeleuchtung` ACI **150**
(fällt in `library._BLAUE_ACI` → wird beim Import auf BYLAYER gesetzt),
`spot`/`antipanikleuchte` ACI 3, `gruppenbatterie` ACI 3/7/256. Die kuratierte
Library führt **keinen** Layer `E_Sicherheitsbeleuchtung` mehr (nur noch
`din_SIBEL_10_emergency_lighting` u. a.) — `sync_layers()` legt den Ausgabe-Layer
deshalb immer selbst an.

### 4b. Prüfung: verwendet die Rotationslogik dieselbe Konvention? — **ja**

`_BLOCK_BASE_DEG` in `src/notbeleuchtung/symbols/orientation.py:26-30`
(unten 270 / links 180 / rechts 0) stimmt **exakt** mit der in 4a.2 gemessenen
DXF-Geometrie überein. **Keine Abweichung** — die Tabelle ist damit als Ursache für
falsche Tür-Rotationen ausgeschlossen.

Algebra-Nachweis der Formel-Gleichheit: `orientation.transformation()` rechnet
`rotation = (ziel − basis) mod 360`. Für den unten-Block (`basis = 270`) ist das
`(A − 270) mod 360 ≡ (A + 90) mod 360` — identisch zur Tür-Formel
`round((atan2(dy,dx)° + 90)/90)·90 mod 360`, die an vier Stellen steht:

| Fundstelle | Kontext |
|---|---|
| `platzierung/anker_strategy.py:193` | RZ am Ausgang, Pfeil zur/durch die Tür |
| `platzierung/gang_strategy.py:143` | RZ am Gang-Zielende |
| `platzierung/communal_stgh_strategy.py:107` | Stiegenhaus-RZ an der Tür |
| `platzierung/fachpraxis.py:303` | Tür-RZ des Pflichtraums |

Effektiver Weltwinkel = `(basis + rotation) mod 360 = (270 + A + 90) mod 360 = A`
— der Pfeil zeigt also entlang `(dx, dy)`, wie beabsichtigt. Ebenso konsistent:
`bausteine.richtung_und_rotation()` (`rechts 90 / oben 180 / links 270 / unten 0`,
`platzierung/bausteine.py:41-44`) und die `_ROT`-Tabelle der Sichtlinien-Strategie
(`anker_strategy.py:288`).

Drei Kopplungen, die dabei aufgefallen sind und **nicht** geändert wurden
(Fremdpakete `platzierung/`, `normwissen/`) — offene Fragen dazu in
`docs/OFFENE_FRAGEN.md`:

- `communal_stgh_strategy.py:106` und `fachpraxis.py:302` rufen
  `_select_key(anf.symbol_katalog_keys, "unten")` und wenden danach hart die
  unten-Block-Formel `(A + 90)` an. `bausteine.select_key` (`bausteine.py:56-64`)
  fällt aber auf `keys[0]` zurück, wenn kein Key auf `_unten` endet. Heute ist
  `keys[0]` in `normwissen/data/raumtyp_regeln.yaml:44` und `:77` =
  `notlicht_ks_stiege` → Block „nach unten" (basis 270), also korrekt. Steht dort
  jemals ein links/rechts-Key zuerst, ist der Pfeil um 90 bzw. 270 Grad falsch —
  ohne Test, der das fängt.
- Die Tür-RZ tragen `richtung="unten"` bei `rotation_deg != 0`
  (`anker_strategy.py:193-198`, `communal_stgh_strategy.py:105-126`,
  `gang_strategy.py:143-149`, `fachpraxis.py:303-308`). `richtung` beschreibt dort
  **nicht** mehr die Pfeilrichtung; verlässlich ist nur
  `fachpraxis._effektive_richtung_deg` (`fachpraxis.py:101-113`). Bewusst so,
  dokumentiert im Docstring von
  `tests/render/test_pfeilrichtung.py::test_4og_rz_geometrisch_konsistent`.
- `round((deg + 90)/90)*90` nutzt Pythons Bankers-Rounding: exakt diagonale
  Türrichtungen (atan2 = 45° → 1.5 → 2 → 180; atan2 = 135° → 2.5 → 2 → 180) werden
  beide auf 180 gerastert statt auf 180 bzw. 270. Betrifft nur exakt diagonale
  Fälle, ist aber an allen vier Fundstellen unmarkiert.

---

## 5. Weiteres Repo-Material zu Symbolen und Photometrie

Gesichtet 2026-09-09 (ezdxf bzw. Datei-Kopfzeilen, temporäre Skripte gelöscht).
Nichts davon ist ein Platzierungs-Muster — es beantwortet die Frage, welche Dateien
neben der kanonischen Library im Repo liegen und wofür sie taugen.

### 5.1 `CAD_Symbole/E-Symbole.dxf` und die Nebenvarianten

**Rolle:** reine **Herkunfts-Referenz**, kein Platzierungs-Asset
(ADR-0002 `docs/adr/0002-kanonische-symbol-library.md`; `library.py:57`).
Kanonisch ist ausschließlich `Notbeleuchtungssymbole.dxf`.

| Datei | Größe | Lesbar mit ezdxf | Inhalt (gemessen) |
|---|---|---|---|
| `E-Symbole.dxf` | 1 674 505 B | ja (AC1032, INSUNITS 4 = mm) | 262 benannte Blöcke (+4 anonym), 26 Layer, 563 Modelspace-Entities |
| `E-Symbole-clean.dxf` | 428 826 B | ja (AC1032, INSUNITS 4) | 108 benannte Blöcke (+3 anonym), 20 Layer, **0** Modelspace-Entities |
| `E-Symbole.dwg` | 347 895 B | nein (DWG) | — |
| `E-Symbole.bak` | 3 078 309 B | nein (DWG-Backup) | — |
| `E-Symbole_recover.dwg` | **1 760 B** | nein (DWG) | Stummel — für 262 Blöcke viel zu klein, faktisch leer |

**Was drin ist:** der volle Elektro-Planungs-Katalog des Herkunftsprojekts, nicht nur
Notbeleuchtung. Häufigste Namensgruppen in `E-Symbole.dxf`: `blockreferenz-*` (88,
AutoCAD-Auto-Namen), `mtext*` (15), `et_legende - wohnung$…` (13 Legenden-Blöcke),
`polylinie*` (12), `steckdose*` (12), `notbeleuchtung*` (5), dazu Schalter,
Bewegungsmelder, Blitzschutz, Kabeltrassen, EDV. Layer u. a.
`E_Sicherheitsbeleuchtung` (Herkunft von `library._LIB_SAFETY_LAYER`),
`ET_BELEUCHTUNG`, `E_BRANDMELDE`, `E_Steckdose+Schalter`, `E_KABELTASSE`.

**Basispunkt-Konvention identisch** zur kanonischen Library: die benannten
Symbolblöcke tragen `base_point = (0,0,0)` mit weit entfernter Geometrie; nur die
128 `blockreferenz-*`-Auto-Blöcke tragen echte Basispunkte ≠ (0,0,0).

**Deckung gegen `schrack_symbol_mapping.yaml` (8 distinkte `block_name`) — gemessen:**

| `block_name` | in `E-Symbole.dxf` | in `E-Symbole-clean.dxf` |
|---|---|---|
| `notbeleuchtung- richtungspfeil nach unten` | ja, 3.134 × 1.567 | ja, 3.134 × 1.567 |
| `notbeleuchtung-richtungspfeil nach links` | ja, 3.134 × 1.567 | ja, 3.134 × 1.567 |
| `notbeleuchtung-richtungspfeil nach rechts` | ja, 3.134 × 1.567 | **ja, aber 2606.183 × 2300.291 = der korrupte Alt-Block** |
| `notbeleuchtung- antipanikleuchte` | ja, 5.645 × 1.588 | **fehlt** |
| `aufheller notbeleuchtung` | **fehlt** | **fehlt** |
| `spot notbeleuchtung` | **fehlt** | **fehlt** |
| `gruppenbatterie` | **fehlt** | **fehlt** |
| `vorlage_legende` | ja, 415.016 × 550.546 | **fehlt** |

⇒ **Keine der beiden E-Symbole-Dateien kann die kanonische Library ersetzen.**
Wer `NOTBELEUCHTUNG_SYMBOL_LIB` darauf zeigen lässt, bekommt bei `E-Symbole.dxf`
einen fail-loud `ValueError` aus `library.load_mapping()` (3 fehlende Blöcke) und bei
`E-Symbole-clean.dxf` zusätzlich den korrupten `nach rechts`-Block (In-Band-Guard
`< 50 units`, `tests/render/test_symbols_library.py:71`).

Zusätzlich enthält `E-Symbole.dxf` einen **Namens-Zwilling** des unten-Pfeils:
`notbeleuchtung richtungspfeil nach unten` (ohne Bindestrich, 3.134 × 1.567,
gleiches Zentrum) neben `notbeleuchtung- richtungspfeil nach unten`. In der
kanonischen Library gibt es ihn nicht — Guard
`tests/render/test_pfeilrichtung.py::test_mapping_nutzt_nur_eine_unten_schreibweise`.

### 5.2 `CAD_Symbole/photometrie/` — welche LDT, welche Leuchte, welche Quelle

Vier EULUMDAT-Dateien, Notbetriebs-Photometrie für den EN-1838-Lux-Nachweis
(`platzierung/lux.py` via `i_cd_fn`, Auflösung in `symbols/photometrie_katalog.py`,
Zuordnung in `symbols/photometrie_mapping.yaml`). Herkunft/Audit-Trail:
`CAD_Symbole/photometrie/QUELLEN.md`. Kopfzeilen unten **aus den Dateien gelesen**,
nicht aus QUELLEN.md übernommen.

| Datei | Firma (Z1) | Leuchtenname (Z9/Z10) | Artikel laut QUELLEN.md | Datum (Z12) | Lichtstrom (Z29) | P (Z32) | Mc × Ng, Isym | max I (cd/klm) |
|---|---|---|---|---|---|---|---|---|
| `rz_nlpxw433_1h3h_picto.ldt` | Schrack Technik GmbH | `NLPXW.39../NLPXW.433.. 1h - pictrogram lens` | NLPXW433SC, Notleuchte PX Autotest 4×1W ERT-LED, Piktogramm-Linse 1h/3h | 02.07.2025 | 520 lm | 0 | 24 × 28, Isym 4 | 294.3 |
| `sl_nlkbu433_3h_corridor.ldt` | Schrack-TECHNIK | `NLKBU433.. 3h — corridor lens` | NLKBU433SC, Notleuchte KB Autotest LED Universalmontage, Corridor-Linse 3h | 13.04.2026 | 260 lm | 3,3 W | 24 × 28, Isym 4 | 991.6 |
| `sl_nlkbu433_3h_round.ldt` | Schrack-TECHNIK | `NLKBU433.. 3h — round lens` | NLKBU433SC, dieselbe Leuchte, Rundlinse 3h | 13.04.2026 | 260 lm | 3,3 W | 24 × 28, Isym 4 | 279.8 |
| `antipanik_nlildl423_round.ldt` | Schrack Technik | `NLIL.L423. with round lens` | NLILDL423S, Notleuchte IL Autotest 1×3W ERT-LED, Rundlinse | 15.07.2021 | 240 lm | 0 | 72 × 61, Isym 4 | 417.9 |

Download-URLs und Produktseiten stehen vollständig in
`CAD_Symbole/photometrie/QUELLEN.md` (Stand 2026-09-03, Schrack-CDN
`image.schrackcdn.com/ldt/…`).

**Zuordnung `catalog_key → LDT`** (`symbols/photometrie_mapping.yaml`):

| catalog_key | LDT | Optik |
|---|---|---|
| `notlicht_ks_stiege`, `…_unten`, `…_links`, `…_rechts` | `rz_nlpxw433_1h3h_picto.ldt` | Piktogramm-Linse |
| `notlicht_kw_garage` | `sl_nlkbu433_3h_round.ldt` | Rundlinse |
| `sicherheitsleuchte_aufheller` | `sl_nlkbu433_3h_round.ldt` | Rundlinse |
| `antipanik_leuchte` | `antipanik_nlildl423_round.ldt` | Rundlinse |
| `fluchtweg_default` (Deckungs-Verdichtung, `platzierung/deckung.py`) | `sl_nlkbu433_3h_corridor.ldt` | Corridor-Linse |
| `sicherheitsleuchte_spot`, `gruppenbatterie_anlage`, `vorlage_legende` | — keine LDT | → `i_cd_fn = None`, Engine fällt auf isotrope Annahme zurück |

**Alle vier LDT tragen `Isym = 4`** (Symmetrie zu C0–C180 *und* C90–C270). Für die
Optik-Ausrichtung nach ADR-0006 heißt das: die Verteilung ist links/rechts
spiegelsymmetrisch; nur die **Achse** (Längs- vs. Querrichtung) ist relevant, ein
180°-Fehler im Optik-Azimut bleibt photometrisch folgenlos. Nicht-öffentliche
din-Photometrie (Concept 2 AP3 PLC24) ist in QUELLEN.md als offener Punkt geführt.

---

## 6. Weiteres Referenzmaterial im Repo

Bestandsaufnahme 2026-09-09: was sonst noch im Repo liegt, was davon in die
Prüfstrecke eingegangen ist und was nicht. Alle Angaben in dieser Tabelle sind
**gemessen** (Dateiliste, Dateigrößen, ezdxf-Lesung aus `.venv\Scripts\python.exe`),
nicht aus Dateinamen abgeleitet. Keine Normwerte in diesem Abschnitt.

| Pfad | Was es ist (gemessen) | Ausgewertet? | Nächster sinnvoller Schritt |
|---|---|---|---|
| `Projekte/Pläne 19., Muthgasse 109B - 2026-05-07_13-12/Architekt/Ausführungsplan/` | 9 Architekten-Grundrisse als DXF **und** dieselben 9 als PDF. DXF: `…GRUNDRISS DD.dxf` (12,4 MB), `…E2` (23,2 MB), `E3` (24,3 MB), `E4` (24,5 MB), `E5` (26,6 MB), `E6` (26,2 MB), `E7` (22,2 MB), `E8` (22,0 MB), `E9` (21,6 MB). PDF-Zwillinge `M109B_HNP_AF-A-GR-<02..09,DD>-AB-D--GRUNDRISS *.pdf` (2,7–3,3 MB, DD 20,2 MB). | **Nur E2.** Belegt durch `Projekte/_eingang/Muthgasse_E2.dxf`, Soll-Nahttest `tests/naht/test_soll_muthgasse.py:20` (`PLAN = Projekte/_eingang/Muthgasse_E2.dxf`) und `tests/e2e/test_familien_durchstich.py:32` (`MUTHGASSE_E2` zeigt direkt auf die Ausführungsplan-DXF). **Nicht aufgenommen: DD, E3, E4, E5, E6, E7, E8, E9** — 8 Geschosse. | Ein zweites Geschoss derselben Familie (z. B. E3, gleiche AIA-Layerstruktur, gleiche Größenordnung wie E2) durch dieselbe Nahtstrecke schicken. Das prüft, ob die AIA-Familienerkennung geschoss-unabhängig ist, ohne eine neue CAD-Familie zu erschließen. DD ist der Sonderfall (Dachdraufsicht, halbe Dateigröße) und eignet sich schlecht als Zweitprobe. |
| `Vorlagen-Legende/Baulegende.dxf` (183.196 B) | ezdxf: DXF `AC1032` (R2018), `$INSUNITS = 4`, `$MEASUREMENT = 1`. Extents 30,60 × 25,67 Einheiten bei Texthöhen 0,5–1,0 — die Geometrie passt zu Metern, nicht zur `INSUNITS`-Angabe „mm". **Keine Blöcke, keine Inserts.** Modelspace: 115 Entities (59 MTEXT, 39 LINE, 11 HATCH, 4 ARC, 2 LWPOLYLINE). 6 Layer: `0`, `Defpoints`, `G-ANNO-TTLB` (trägt alle Texte), `New_255 Plangrafiken_Pen_No__21`, `New_255 Plangrafiken_Pen_No__39`, `New_HKLS1_Pen_No__21`. Paperspace `Layout1`: 210 × 297 mm, `plot_rotation = 1` (A4 quer), 2 Entities. Inhaltlich eine **Bau**-Legende, keine Elektrik: Schraffur-Legende (`ZIEGELMAUERWERK`, `STAHLBETON`, `BETON`, `GIPSKARTONSTÄNDERWAND EI90/EI30/EI0`, `WÄRMEDÄMMUNG`, `ALU-GLASKONSTRUKTIONEN`, `YTONG`, `BRANDABSCHNITT`, `TROCKENSTEIGLEITUNG`, `FLUCHTWEGSLÄNGE`, `LÄNGE TSL`) plus Abkürzungsliste (`ADUK`, `AR`, `BRE`, `BST`, `DBA`, `DDB`, `F+H`, `FDB`, `FOK`, `FSTZ.`, `FW`, `HT`, `NÜ`, `ROK`, `RR`, `RUK`, `STGH.`, `UZUK`, `VR`, `WDB`). | Nein. | Als Wörterbuch für die Raum-/Bauteil-Klassifikation auswerten: `STGH.` → Stiegenhaus, `VR` → Vorraum, `AR` → Abstellraum sind genau die Kürzel, die in Grundriss-Raumstempeln stehen. Abgleich gegen die vorhandene Raumtypen-Erkennung, ob diese Kürzel dort schon aufgelöst werden. Für die Symbolik der Notbeleuchtung ist die Datei **wertlos** — sie enthält kein einziges Elektro-Symbol und keinen einzigen Block. |
| `Vorlagen-Legende/Notbeleuchtungspläne-Vorlage.dxf` (388.573 B) | ezdxf: DXF `AC1032` (R2018), `$INSUNITS = 4`. **Modelspace leer (0 Entities)** — der gesamte Inhalt liegt im Paperspace. `Layout1`: 210 × 297 mm, `plot_rotation = 1` (A4 quer), 88 Entities: 37 TEXT, 23 LINE, 15 LWPOLYLINE, 9 INSERT, 3 VIEWPORT, 1 IMAGE. `Layout2`: gleiches Blattformat, 2 Entities. 6 Layer, darunter `E_Muster` (Symbol-Beschriftung), `ET_LEGENDE - Wohnung$0$800_AL_ALLG_L` (Plankopf), `din_SIBEL_10_emergency_lighting` (derselbe Layername wie im Fachplaner-Plan, Abschnitt 1), `PDF2_Bilder`. **9 Blöcke definiert, 7 davon im Blatt platziert:** `Notbeleuchtung- Richtungspfeil nach unten` (1×), `Notbeleuchtung-Richtungspfeil nach links` (3×), `Notbeleuchtung-Richtungspfeil nach rechts` (1×), `Notbeleuchtung- Antipanikleuchte` (1×, 44 LWPOLYLINE), `Aufheller Notbeleuchtung` (1×), `Spot Notbeleuchtung` (1×), `Gruppenbatterie-Verteiler` (1×); nur definiert, nicht platziert: `Sicherheitsleuchte Aufheller`, `Gruppenbatterie`. Legendentexte auf `E_Muster` (Höhe 5,813): `Notbeleuchtung-RZ- Pfeil nach unten`, `…nach links`, `…nach rechts`, `Notbeleuchtung-RZ-beidseitig`, `Notbeleuchtung-Aufheller`, `Notbeleuchtung-Antipanikleuchte`, `Notbeleuchtung-Spot-Aufheller`, `Notbeleuchtung-Gruppenbatterie-Verteiler`, dazu die Spaltenköpfe `Symbole` / `Beschriftung`. Plankopf-Texte: `Rivoplan`, `Notbeleuchtungsplan`, Plannummern-Kürzel `NP`, Index `A`, `MASSSTAB 1:50`, `Erdgeschoss`, `MVP-Projekt`, Felder `ÄNDERUNG / DATUM / GEZ. / PLANINHALT / PLANNUMMER`, `Bauherr:`, `Architekt:`, `Planverfasser:`, `Generelunternehmer:` (sic), `E-Mail: office@rivoplan.at`, `Homepage: www.rivoplan.com`. | Nein — die Blocknamen decken sich weitgehend mit `schrack_symbol_mapping.yaml` (Abschnitt 5.1), aber die Datei ist nirgends im Repo als Quelle referenziert. | Zwei getrennte Verwertungen. (1) **Blattvorlage:** Layout1 ist ein fertiger A4-quer-Plankopf mit 3 Viewports und Legendenblock — die konkreteste vorhandene Vorgabe für den Plot-Rahmen unserer Ausgabe; Maße und Feldnamen als Soll gegen `docs/STEMPEL_REPORT.md` prüfen. (2) **Blockgeometrie:** die 9 Blöcke gegen die kanonische Library messen (Basispunkt/Nullrichtung wie in 4a.1/4a.2), insbesondere ob `Gruppenbatterie` und `Gruppenbatterie-Verteiler` zwei Symbole oder ein Duplikat sind (beide 2 HATCH + 2 LWPOLYLINE). **Achtung:** `Aufheller Notbeleuchtung` besteht hier nur aus 1 INSERT auf `Sicherheitsleuchte Aufheller` — verschachtelt, also nicht 1:1 als flacher Block übernehmbar. |
| `Vorlagen-Legende/rivoplan_logo.png` (25.882 B), `Vorlagen-Legende/Baulegende.pdf` (168.970 B), `Vorlagen-Legende/Baulegende.bak` (179.014 B) | Logo-Bitmap; PDF-Zwilling der Baulegende; `.bak` = AutoCAD-Sicherungskopie der `Baulegende.dxf`, 4.182 B kleiner als das `.dxf`, also ein älterer Speicherstand. | Nein. | Logo: Kandidat für den Plankopf — das `IMAGE`-Entity in `Notbeleuchtungspläne-Vorlage.dxf` Layout1 ist vermutlich genau dieses Logo; die Bildreferenz selbst wurde nicht aufgelöst, also vor der Verwendung nachmessen. `.bak` und `.pdf`: liegen lassen, kein eigener Informationswert gegenüber der `.dxf`. |
| `DIN-Notbeleuchtungspläne(Beispiele)/din_support_ReMi_Barawitzkagasse_28.04.2026.dwg` (1.858.220 B ≈ 1,77 MB) | Binär-DWG, Header-Signatur `AC1032` (= AutoCAD R2018) — identische Formatversion wie der in Abschnitt 1 ausgewertete DXF-Zwilling `din_support_ReMi_Barawitzkagasse_28.04.2026.dxf` (11.049.215 B ≈ 10,54 MB, Faktor 5,9). Nicht mit ezdxf geöffnet — ezdxf liest kein DWG. | Nein, und **nicht nötig**: der DXF-Zwilling ist vollständig ausgewertet (Abschnitte 1, 1a–1d). | Nichts tun, als Rohformat-Beleg behalten. Erst anfassen, falls der Verdacht entsteht, die DXF-Konvertierung habe Entities verloren; dann per ODA File Converter neu nach DXF wandeln und die Entity-Zahlen gegenüberstellen. |
| `Projekte/BVH Fischamenderstraße/fertige Elektromontagepläne/` | **11 DXF** in 3 Unterordnern. `BT1/` (5): `Elektromontageapläne_ERDGESCHOSS BT1.dxf` (31,5 MB), `…_1-OBERGESCHOSS BT1` (22,9 MB), `…_2-OBERGESCHOSS BT1` (31,1 MB), `…_DACHGESCHOSS BT1` (15,6 MB), `…_DACHDRAUFSICHT BT1` (5,2 MB). `BT2/` (5): `Elektromontageplan_ERDGESCHOSS BT2`, `…_1.OBERGESCHOSS BT2`, `…_2.OBERGESCHOSS BT2`, `…_DACHGESCHOSS BT2`, `…_DACHDRAUFSICHT BT2`. `UG/` (1): `Elektromontageplan_Untergeschoß.dxf`. Geschosse laut Dateinamen: UG, EG, 1. OG, 2. OG, DG, Dachdraufsicht — je Bauteil BT1 und BT2, das UG nur einmal (gemeinsam). **Gemessen an `BT1/Elektromontageapläne_ERDGESCHOSS BT1.dxf`** (ezdxf): DXF `AC1032`, `$INSUNITS = 6`, Extents (−16.594,8 / −7.942,8) bis (38.223,5 / 32.500,0), 98 Layer, 1.345 benannte Blöcke, 3 Layouts (`Model`, `Layout1`, `Layout2`). Notbeleuchtungs-relevant: Layer **`E_Sicherheitsbeleuchtung`** (Farbe 100) mit **6 INSERTs im Modelspace** und Layer **`A_Fluchtweg`** (Farbe 240); Block **`ET_LEGENDE - Wohnung$0$ET_SV_RETTUNGSZEICHEN`** (3 HATCH, 12 LINE, **30 ATTDEF**). Die 6 Inserts zeigen auf die anonymen Blöcke `*U1173` (2×) und `*U1284` (4×), deren Inhalt exakt dieselbe Signatur trägt (3 HATCH / 12 LINE / 30 ATTDEF) — also anonymisierte Kopien des Rettungszeichen-Blocks. Weitere Elektro-Layer im Modelspace: `E_Steckdose+Schalter` (412 Entities), `ET_NACHRTECH` (39), `E_Beleuchtungstyp` (29), `E_Muster` (12), `E_ERDUNG` (8), `E_NACHRTECH` (6). | Nein. Kein Test und kein `Projekte/_eingang`-Eintrag referenziert Fischamenderstraße. | Der höchste Nutzen des ganzen Abschnitts: das ist ein **zweiter fertig geplanter Referenzplan** neben Barawitzkagasse (Abschnitt 1), aus anderer Planerhand und mit anderer Layerkonvention (`E_Sicherheitsbeleuchtung` statt `din_SIBEL_10_*`). Erster Schritt: die 30 ATTDEF-Tags des Rettungszeichen-Blocks auslesen — dort steht vermutlich Typ/Leuchtennummer, analog zu `TYPENUMBER` beim Fachplaner (Abschnitt 1) — und die 6 EG-Positionen in Plankoordinaten überführen. Dann dieselbe Musteranalyse wie in Abschnitt 1 fahren (Tür-/Ecken-Anker, Abstände) und prüfen, ob die dortigen Muster planerübergreifend halten. Vorsicht: nur 6 Leuchten im EG gegenüber 11 in Barawitzkagasse EG — die Ursache der geringeren Dichte vor jedem Vergleich klären, möglicherweise sind Notleuchten teilweise auf `E_Beleuchtungstyp` mitgeführt. |
| `Projekte/Aichholzgasse.zip` (35.601.809 B ≈ 33,9 MB) | ZIP-Archiv. Nicht entpackt, Inhalt hier nicht belegt. | Nein. | Nur bei konkretem Bedarf öffnen (z. B. fünfte CAD-Familie). Vorher das Inhaltsverzeichnis ohne Extraktion listen. |
| `Projekte/Baufeld_E2.zip` (50.358.161 B ≈ 48,0 MB) | ZIP-Archiv. Nicht entpackt, Inhalt hier nicht belegt. | Nein. | Die Namensverwandtschaft zu Muthgasse E2 ist auffällig, aber ungeprüft. Inhaltsverzeichnis listen und gegen die bereits ausgewertete `Muthgasse_E2` abgleichen, bevor irgendetwas entpackt wird — mögliche Dublette. |
| `Projekte/Baufeld_E2_Notbeleuchtungsplaene.zip` (50.542.521 B ≈ 48,2 MB) | ZIP-Archiv. Nicht entpackt. Nur 184.360 B größer als `Baufeld_E2.zip`. | Nein. | Potenziell der **Soll-Plan zu einem Geschoss, das wir bereits verarbeiten** — damit die direkteste verfügbare Vergleichsgrundlage „unsere Platzierung vs. Fachplaner" für die Muthgasse-Familie. Vor dem Entpacken Inhaltsverzeichnis listen; die geringe Größendifferenz zu `Baufeld_E2.zip` legt nahe, dass beide Archive überwiegend dieselben Grundrisse enthalten und nur die Notbeleuchtungs-Ebene hinzukommt. |
| `Hauptausgang 1.png` (69.327 B), `Hauptausgang 2.png` (15.276 B), `Hauptausgang 3.png` (23.813 B), `Hauptausgang4.png` (24.195 B), `Screenshot 2026-08-29 151406.png` (98.253 B) | Fünf PNG in der Repo-Wurzel. Hier nur benannt, Bildinhalt nicht ausgewertet. Nicht zu verwechseln mit den 6 in Abschnitt 2 ausgewerteten Beispielbildern — die liegen als JPG in `DIN-Notbeleuchtungspläne(Beispiele)/`. | Nein. | Ansehen und einordnen: entweder Referenzmaterial zum Hauptausgangs-Begriff — dann wie Abschnitt 2 als Bild-Lehre aufnehmen und nach `knowledge/` einsortieren — oder Arbeitsscreenshots, dann aus der Repo-Wurzel nach `docs/analyse/` bzw. `output/` räumen. Bis dahin: nichts löschen. |
