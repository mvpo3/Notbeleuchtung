# INDEX — Übersichtskarten der Raumerkennung

Erzeugt von `scripts/analyse/uebersicht_karte.py` (Sweep 2026-09-11, 63 Pläne, rund 133 min
Wanduhr, 2 parallel). Je Plan liegen `uebersicht.png` / `.json` / `.md` im Ordner darunter.

**Was die Zahlen sind:** genau das, was `ArchitekturRaumProvider.parse()` liefert — keine
fachliche Bewertung, kein Normurteil. Ausgänge sind nach `Ausgang.typ` (`final_exit` /
`stair_exit`) gezählt, nicht nach eigener Einschätzung. Was die Erkennung nicht liefert,
steht als `0` bzw. `—` und ist unter „Was die Karte NICHT zeigt“ begründet.

**Geschoss** ist die Bezeichnung aus dem Dateinamen, **nicht** das `floor`-Feld des
Modells — das steht auf den meisten Plänen auf `EG` (s. Auffälligkeit 8).

Spalten: **untyp.** = Räume ohne `raum_typ` (in der Karte magenta „nicht erkannt“) ·
**Schächte+Lifte** = `raum_typ` SCHACHT oder LIFT · **Innenhöfe** = geschlossene
Außenflächen aus der Wandkörper-Analyse · **FW-Segm.** = Fluchtweg-Zirkulationssegmente.

---

## A — Grundrisse (Architektur), 46 Pläne — 45 Karten + 1 nicht auswertbar

### Barawitzkagasse 8

| Plan | Geschoss | Karte | Räume | untyp. | Whg | Stiegenh. | Gänge | Innenhöfe | Schächte+Lifte | final_exit | stair_exit | FW-Segm. |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Barawitzka_1DG | 1DG | [png](./Barawitzka_1DG/uebersicht.png) | 40 | 9 | 6 | 3 | 2 | 3 | 7 | 0 | 1 | 4 |
| Barawitzka_1ST | 1ST | [png](./Barawitzka_1ST/uebersicht.png) | 58 | 11 | 11 | 8 | 2 | 6 | 6 | 5 | 5 | 11 |
| Barawitzka_2DG | 2DG | [png](./Barawitzka_2DG/uebersicht.png) | 25 | 4 | 5 | 2 | 1 | 1 | 6 | 0 | 0 | 2 |
| Barawitzka_2ST | 2ST | [png](./Barawitzka_2ST/uebersicht.png) | 53 | 11 | 11 | 4 | 4 | 7 | 7 | 5 | 1 | 5 |
| Barawitzka_3ST | 3ST | [png](./Barawitzka_3ST/uebersicht.png) | 36 | 11 | 9 | 3 | 1 | 3 | 6 | 7 | 1 | 7 |
| Barawitzka_EG | EG | [png](./Barawitzka_EG/uebersicht.png) | 50 | 6 | 7 | 2 | 5 | 2 | 5 | 1 | 0 | 12 |
| Barawitzka_FDM | FDM | [png](./Barawitzka_FDM/uebersicht.png) | 8 | 3 | 0 | 2 | 0 | 1 | 3 | 0 | 0 | 2 |
| Barawitzka_KG | KG | [png](./Barawitzka_KG/uebersicht.png) | 41 | 28 | 3 | 0 | 0 | 6 | 5 | 0 | 0 | 0 |
| **Σ Barawitzkagasse 8** | | **8 Karten** | **311** | **83** | **52** | **24** | **15** | **29** | **45** | **18** | **8** | **43** |

### BVH Fischamenderstrasse

| Plan | Geschoss | Karte | Räume | untyp. | Whg | Stiegenh. | Gänge | Innenhöfe | Schächte+Lifte | final_exit | stair_exit | FW-Segm. |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Fischamend_BT1_DG | BT1 DG | [png](./Fischamend_BT1_DG/uebersicht.png) | 46 | 4 | 2 | 1 | 8 | 0 | 1 | 1 | 1 | 39 |
| Fischamend_BT1_EG | BT1 EG | [png](./Fischamend_BT1_EG/uebersicht.png) | 79 | 7 | 3 | 1 | 14 | 0 | 1 | 3 | 1 | 90 |
| Fischamend_BT1_OG1 | BT1 OG1 | [png](./Fischamend_BT1_OG1/uebersicht.png) | 67 | 1 | 1 | 1 | 14 | 0 | 1 | 0 | 1 | 68 |
| Fischamend_BT1_OG2 | BT1 OG2 | [png](./Fischamend_BT1_OG2/uebersicht.png) | 67 | 1 | 1 | 1 | 14 | 0 | 1 | 0 | 1 | 98 |
| Fischamend_BT1_UG | BT1 UG | [png](./Fischamend_BT1_UG/uebersicht.png) | 44 | 21 | 0 | 1 | 3 | 2 | 4 | 3 | 2 | 114 |
| Fischamend_BT2_DG | BT2 DG | [png](./Fischamend_BT2_DG/uebersicht.png) | 58 | 1 | 5 | 2 | 10 | 0 | 3 | 1 | 3 | 74 |
| Fischamend_BT2_EG | BT2 EG | [png](./Fischamend_BT2_EG/uebersicht.png) | 55 | 7 | 1 | 1 | 8 | 1 | 2 | 4 | 2 | 55 |
| Fischamend_BT2_OG1 | BT2 OG1 | [png](./Fischamend_BT2_OG1/uebersicht.png) | 68 | 1 | 4 | 2 | 13 | 0 | 2 | 1 | 2 | 88 |
| Fischamend_BT2_OG2 | BT2 OG2 | [png](./Fischamend_BT2_OG2/uebersicht.png) | 66 | 3 | 5 | 1 | 12 | 0 | 2 | 1 | 2 | 81 |
| **Σ BVH Fischamenderstrasse** | | **9 Karten** | **550** | **46** | **22** | **11** | **96** | **3** | **17** | **14** | **15** | **707** |

### Herrenholzgasse

| Plan | Geschoss | Karte | Räume | untyp. | Whg | Stiegenh. | Gänge | Innenhöfe | Schächte+Lifte | final_exit | stair_exit | FW-Segm. |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Herrenholz_EG | EG | [png](./Herrenholz_EG/uebersicht.png) | 498 | 244 | 49 | 0 | 46 | 0 | 1 | 15 | 0 | 0 |
| Herrenholz_OG1 | OG1 | [png](./Herrenholz_OG1/uebersicht.png) | 300 | 23 | 47 | 0 | 55 | 0 | 0 | 0 | 0 | 55 |
| Herrenholz_OG2 | OG2 | [png](./Herrenholz_OG2/uebersicht.png) | 155 | 38 | 23 | 0 | 14 | 0 | 0 | 0 | 0 | 14 |
| Herrenholz_UG | UG | [png](./Herrenholz_UG/uebersicht.png) | 155 | 38 | 23 | 0 | 14 | 0 | 0 | 0 | 0 | 14 |
| **Σ Herrenholzgasse** | | **4 Karten** | **1108** | **343** | **142** | **0** | **129** | **0** | **1** | **15** | **0** | **83** |

### Mollgasse

| Plan | Geschoss | Karte | Räume | untyp. | Whg | Stiegenh. | Gänge | Innenhöfe | Schächte+Lifte | final_exit | stair_exit | FW-Segm. |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Mollgasse_DG | DG | [png](./Mollgasse_DG/uebersicht.png) | 35 | 1 | 5 | 1 | 5 | 2 | 3 | 1 | 0 | 5 |
| Mollgasse_EG | EG | [png](./Mollgasse_EG/uebersicht.png) | 64 | 10 | 8 | 2 | 16 | 1 | 2 | 9 | 4 | 126 |
| Mollgasse_KG1 | KG1 | [png](./Mollgasse_KG1/uebersicht.png) | 31 | 24 | 0 | 2 | 2 | 0 | 2 | 2 | 0 | 4 |
| Mollgasse_KG2 | KG2 | [png](./Mollgasse_KG2/uebersicht.png) | 30 | 19 | 1 | 3 | 2 | 0 | 3 | 3 | 6 | 15 |
| Mollgasse_OG1 | OG1 | [png](./Mollgasse_OG1/uebersicht.png) | 92 | 7 | 20 | 2 | 16 | 5 | 2 | 0 | 1 | 26 |
| Mollgasse_OG2 | OG2 | [png](./Mollgasse_OG2/uebersicht.png) | 97 | 8 | 18 | 2 | 20 | 5 | 3 | 0 | 1 | 26 |
| Mollgasse_OG3 | OG3 | [png](./Mollgasse_OG3/uebersicht.png) | 64 | 10 | 13 | 1 | 12 | 4 | 2 | 1 | 0 | 9 |
| Mollgasse_OG4 | OG4 | [png](./Mollgasse_OG4/uebersicht.png) | 53 | 5 | 12 | 3 | 10 | 4 | 3 | 1 | 1 | 10 |
| **Σ Mollgasse** | | **8 Karten** | **466** | **84** | **77** | **16** | **83** | **21** | **20** | **17** | **13** | **221** |

### Muthgasse 109B

| Plan | Geschoss | Karte | Räume | untyp. | Whg | Stiegenh. | Gänge | Innenhöfe | Schächte+Lifte | final_exit | stair_exit | FW-Segm. |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Muthgasse_E2 | E2 | [png](./Muthgasse_E2/uebersicht.png) | 113 | 10 | 8 | 9 | 5 | 0 | 5 | 5 | 5 | 146 |
| Muthgasse_E3 | E3 | [png](./Muthgasse_E3/uebersicht.png) | 135 | 14 | 4 | 7 | 6 | 0 | 6 | 0 | 3 | 184 |
| Muthgasse_E4 | E4 | [png](./Muthgasse_E4/uebersicht.png) | 132 | 12 | 5 | 6 | 6 | 0 | 6 | 0 | 3 | 185 |
| Muthgasse_E5 | E5 | [png](./Muthgasse_E5/uebersicht.png) | 133 | 13 | 4 | 6 | 11 | 0 | 6 | 1 | 2 | 194 |
| Muthgasse_E6 | E6 | [png](./Muthgasse_E6/uebersicht.png) | 137 | 15 | 5 | 7 | 11 | 0 | 5 | 1 | 3 | 193 |
| Muthgasse_E7 | E7 | [png](./Muthgasse_E7/uebersicht.png) | 107 | 8 | 4 | 6 | 7 | 0 | 5 | 0 | 2 | 160 |
| Muthgasse_E8 | E8 | [png](./Muthgasse_E8/uebersicht.png) | 106 | 10 | 3 | 6 | 5 | 0 | 6 | 0 | 2 | 160 |
| Muthgasse_E9 | E9 | [png](./Muthgasse_E9/uebersicht.png) | 69 | 7 | 3 | 8 | 5 | 0 | 6 | 2 | 3 | 89 |
| **Σ Muthgasse 109B** | | **8 Karten** | **932** | **89** | **36** | **55** | **56** | **0** | **45** | **9** | **23** | **1311** |

### Rennweg 15

| Plan | Geschoss | Karte | Räume | untyp. | Whg | Stiegenh. | Gänge | Innenhöfe | Schächte+Lifte | final_exit | stair_exit | FW-Segm. |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Rennweg_DG1 | DG1 | [png](./Rennweg_DG1/uebersicht.png) | 15 | 1 | 1 | 2 | 2 | 0 | 2 | 0 | 1 | 5 |
| Rennweg_DG2 | DG2 | [png](./Rennweg_DG2/uebersicht.png) | 14 | 0 | 1 | 5 | 3 | 0 | 2 | 0 | 3 | 18 |
| Rennweg_EG | EG | [png](./Rennweg_EG/uebersicht.png) | 22 | 5 | 2 | 5 | 2 | 0 | 1 | 3 | 5 | 9 |
| Rennweg_OG1 | OG1 | [png](./Rennweg_OG1/uebersicht.png) | 18 | 1 | 3 | 3 | 4 | 0 | 1 | 0 | 3 | 6 |
| Rennweg_OG2 | OG2 | [png](./Rennweg_OG2/uebersicht.png) | 19 | 1 | 2 | 1 | 5 | 0 | 1 | 0 | 0 | 2 |
| Rennweg_OG3 | OG3 | [png](./Rennweg_OG3/uebersicht.png) | 15 | 1 | 2 | 1 | 1 | 0 | 3 | 0 | 1 | 5 |
| Rennweg_UG | UG | [png](./Rennweg_UG/uebersicht.png) | 23 | 10 | 4 | 3 | 3 | 0 | 1 | 0 | 2 | 6 |
| **Σ Rennweg 15** | | **7 Karten** | **126** | **19** | **15** | **20** | **20** | **0** | **11** | **3** | **15** | **51** |

### Einzeldatei (Projekte/)

| Plan | Geschoss | Karte | Räume | untyp. | Whg | Stiegenh. | Gänge | Innenhöfe | Schächte+Lifte | final_exit | stair_exit | FW-Segm. |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| EG_Grundriss_DE_NEU | EG | [png](./EG_Grundriss_DE_NEU/uebersicht.png) | 14 | 2 | 4 | 1 | 4 | 0 | 1 | 1 | 1 | 6 |
| **Σ Einzeldatei (Projekte/)** | | **1 Karten** | **14** | **2** | **4** | **1** | **4** | **0** | **1** | **1** | **1** | **6** |

### Aichholzgasse

| Plan | Geschoss | Karte | Räume | untyp. | Whg | Stiegenh. | Gänge | Innenhöfe | Schächte+Lifte | final_exit | stair_exit | FW-Segm. |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **Aichholzgasse** | - | [md](./Aichholzgasse/uebersicht.md) | - | - | - | - | - | - | - | - | - | - |

Keine Karte — Grund s. „Pläne, die nicht auswertbar waren“.

### Σ Gruppe A (Architektur)

| Plan | Geschoss | Karte | Räume | untyp. | Whg | Stiegenh. | Gänge | Innenhöfe | Schächte+Lifte | final_exit | stair_exit | FW-Segm. |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **Σ A — alle Architekturpläne** | | **45 Karten** | **3507** | **666** | **348** | **127** | **403** | **53** | **140** | **77** | **75** | **2422** |

---

## B — fertige Elektro-/Notbeleuchtungspläne (ERGEBNISBEISPIELE)

> **Kennzeichnung:** Diese 17 Pläne sind **keine leeren Architekturpläne**. Sie enthalten
> bereits Leuchten/Symbole der fertigen Planung und gehören **nicht** in die Grundriss-
> Auswertung. Sie stehen hier, weil die Raumerkennung auch auf ihnen gelaufen ist.
> Ablage: `_uebersicht/_elektro_beispiele/<plan>/`.

### BVH Fischamenderstrasse - fertige Elektromontageplaene

| Plan | Geschoss | Karte | Räume | untyp. | Whg | Stiegenh. | Gänge | Innenhöfe | Schächte+Lifte | final_exit | stair_exit | FW-Segm. |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Fischamend_E_BT1_DG | BT1 DG | [png](./_elektro_beispiele/Fischamend_E_BT1_DG/uebersicht.png) | 45 | 6 | 2 | 1 | 8 | 0 | 1 | 1 | 1 | 39 |
| Fischamend_E_BT1_EG | BT1 EG | [png](./_elektro_beispiele/Fischamend_E_BT1_EG/uebersicht.png) | 72 | 5 | 2 | 1 | 14 | 0 | 1 | 3 | 1 | 87 |
| Fischamend_E_BT1_OG1 | BT1 OG1 | [png](./_elektro_beispiele/Fischamend_E_BT1_OG1/uebersicht.png) | 69 | 2 | 1 | 2 | 14 | 0 | 2 | 0 | 2 | 60 |
| Fischamend_E_BT1_OG2 | BT1 OG2 | [png](./_elektro_beispiele/Fischamend_E_BT1_OG2/uebersicht.png) | 69 | 2 | 2 | 2 | 14 | 0 | 2 | 0 | 2 | 103 |
| Fischamend_E_BT2_DG | BT2 DG | [png](./_elektro_beispiele/Fischamend_E_BT2_DG/uebersicht.png) | 58 | 1 | 3 | 2 | 10 | 0 | 3 | 1 | 2 | 58 |
| Fischamend_E_BT2_EG | BT2 EG | [png](./_elektro_beispiele/Fischamend_E_BT2_EG/uebersicht.png) | 51 | 6 | 2 | 1 | 8 | 0 | 2 | 6 | 2 | 53 |
| Fischamend_E_BT2_OG1 | BT2 OG1 | [png](./_elektro_beispiele/Fischamend_E_BT2_OG1/uebersicht.png) | 68 | 1 | 4 | 2 | 13 | 0 | 2 | 1 | 2 | 88 |
| Fischamend_E_BT2_OG2 | BT2 OG2 | [png](./_elektro_beispiele/Fischamend_E_BT2_OG2/uebersicht.png) | 66 | 3 | 6 | 1 | 12 | 0 | 2 | 1 | 1 | 81 |
| Fischamend_E_UG | UG | [png](./_elektro_beispiele/Fischamend_E_UG/uebersicht.png) | 43 | 30 | 0 | 1 | 3 | 1 | 3 | 2 | 2 | 121 |
| **Σ BVH Fischamenderstrasse - fertige Elektromontageplaene** | | **9 Karten** | **541** | **56** | **22** | **13** | **96** | **1** | **18** | **15** | **15** | **690** |

### Baufeld E2 - Notbeleuchtungsplaene

| Plan | Geschoss | Karte | Räume | untyp. | Whg | Stiegenh. | Gänge | Innenhöfe | Schächte+Lifte | final_exit | stair_exit | FW-Segm. |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| BaufeldE2_NB_EG | EG | [png](./_elektro_beispiele/BaufeldE2_NB_EG/uebersicht.png) | 241 | 39 | 19 | 10 | 38 | 6 | 6 | 6 | 12 | 196 |
| BaufeldE2_NB_OG1 | OG1 | [png](./_elektro_beispiele/BaufeldE2_NB_OG1/uebersicht.png) | 299 | 11 | 20 | 11 | 59 | 4 | 0 | 0 | 13 | 277 |
| BaufeldE2_NB_OG2 | OG2 | [png](./_elektro_beispiele/BaufeldE2_NB_OG2/uebersicht.png) | 301 | 13 | 23 | 9 | 60 | 3 | 2 | 0 | 12 | 277 |
| BaufeldE2_NB_OG3 | OG3 | [png](./_elektro_beispiele/BaufeldE2_NB_OG3/uebersicht.png) | 299 | 11 | 21 | 11 | 59 | 4 | 0 | 0 | 13 | 275 |
| BaufeldE2_NB_OG4 | OG4 | [png](./_elektro_beispiele/BaufeldE2_NB_OG4/uebersicht.png) | 300 | 13 | 14 | 10 | 60 | 4 | 0 | 0 | 13 | 292 |
| BaufeldE2_NB_OG5 | OG5 | [png](./_elektro_beispiele/BaufeldE2_NB_OG5/uebersicht.png) | 219 | 14 | 16 | 11 | 40 | 5 | 0 | 0 | 15 | 197 |
| BaufeldE2_NB_OG6 | OG6 | [png](./_elektro_beispiele/BaufeldE2_NB_OG6/uebersicht.png) | 215 | 10 | 16 | 10 | 42 | 6 | 0 | 0 | 14 | 199 |
| BaufeldE2_NB_UG | UG | [png](./_elektro_beispiele/BaufeldE2_NB_UG/uebersicht.png) | 266 | 237 | 0 | 6 | 9 | 0 | 12 | 9 | 13 | 22 |
| **Σ Baufeld E2 - Notbeleuchtungsplaene** | | **8 Karten** | **2140** | **348** | **129** | **78** | **367** | **32** | **20** | **15** | **105** | **1735** |

### Σ Gruppe B (Elektro-Beispiele)

| Plan | Geschoss | Karte | Räume | untyp. | Whg | Stiegenh. | Gänge | Innenhöfe | Schächte+Lifte | final_exit | stair_exit | FW-Segm. |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **Σ B — alle Elektro-Beispiele** | | **17 Karten** | **2681** | **404** | **151** | **91** | **463** | **33** | **38** | **30** | **120** | **2425** |

---

## Σ über alles

| Plan | Geschoss | Karte | Räume | untyp. | Whg | Stiegenh. | Gänge | Innenhöfe | Schächte+Lifte | final_exit | stair_exit | FW-Segm. |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **Σ A (Architektur)** | | **45 Karten** | **3507** | **666** | **348** | **127** | **403** | **53** | **140** | **77** | **75** | **2422** |
| **Σ B (Elektro-Beispiele)** | | **17 Karten** | **2681** | **404** | **151** | **91** | **463** | **33** | **38** | **30** | **120** | **2425** |
| **Σ gesamt** | | **62 Karten** | **6188** | **1070** | **499** | **218** | **866** | **86** | **178** | **107** | **195** | **4847** |

---

## Was die Karte NICHT zeigt

Aus dem Inventar der 62 `uebersicht.md` (Abschnitt „nicht erkannt“). Die Zahl sagt, auf
wie vielen der 62 auswertbaren Pläne der Punkt zutrifft.

| Was das Modell heute nicht hergibt | betroffene Pläne |
|---|--:|
| untypisierte Räume (`raum_typ` leer) — Zahl je Plan s. Tabelle | 62 |
| `Ausgang.typ == "door"`: **0** | 62 |
| Zirkulationsgraph aus Plan-Layern `09-WEG*` leer oder ungenutzt | 62 |
| Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** | 62 |
| „Ausgang führt auf die Straße": wird NICHT geführt | 62 |
| Innenhöfe: **0** | 38 |
| `final_exit`: **0** | 29 |
| `stair_exit`: **0** | 12 |
| Außenflächen (BALKON/TERRASSE): **0** | 11 |
| Schächte/Lifte: **0** | 8 |
| Wohnungen: **0** | 5 |
| Stiegenhäuser: **0** | 5 |
| Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ): **0** | 2 |

**Vom Owner gewünschte Kategorien, die es im Modell überhaupt nicht gibt:**

- **„Ausgang führt auf die Straße“** — das `RaumModell` kennt nur `final_exit` /
  `stair_exit`, keine Straßen- oder Außenraum-Zuordnung. Wird nicht gezeichnet.
- **Sonderstellen (Feuerlöscher / Hydrant / Erste Hilfe)** — dafür existiert kein Erzeuger.
- **`Ausgang.typ == "door"`** — wird von `leite_ausgaenge` grundsätzlich nicht erzeugt;
  die Legende führt die Kategorie, der Wert ist auf **allen** Plänen 0.
- **Zirkulationsgraph aus Plan-Layern `09-WEG*`** — leer (0 Knoten / 0 Kanten) auf allen
  Plänen. Die gezeigten Fluchtweg-Segmente stammen aus dem Fluchtweg-Nachlauf.
- **Außenflächen (BALKON/TERRASSE)** und **Innenhöfe** nur dort, wo `raum_typ` bzw. die
  Wandkörper-Analyse sie liefert — sonst 0, ohne Ersatzwert.

### Pläne, die nicht auswertbar waren

| Plan | Datei | Grund |
|---|---|---|
| **Aichholzgasse** | `26_0507_AICH.dxf` (146 MB, 10 Grundrisse in einem Modelspace) | `ValueError('Keine Wand-Entities gefunden — Layer-Muster prüfen.')` in `dxf_load.py:258` (aus `provider.parse`). Abbruch nach 84,9 s vor dem Render. Die Layer-Benennung dieses Büros passt nicht auf die Wand-Muster der Erkennung. Voller Traceback: `Aichholzgasse/uebersicht.md`. |

**Bewusst nicht gerechnet (laut Auftrag):** 7 Schnitte + 1 Lageplan Barawitzka · 5
Dachdraufsichten (Barawitzka DD STG1, Fischamend BT1+BT2, Muthgasse DD, Herrenholz dd,
Rennweg DD) · Symbol-/Legendenbibliotheken (`Rennweg/Legende/Baulegende.dxf`,
`Vorlagen-Legende/`, `CAD_Symbole/`).

**Ungeprüft:** `Baufeld_E2.zip` — 8 Dateien mit denselben Namen wie
`Baufeld_E2_Notbeleuchtungsplaene.zip`, andere MD5, durchweg minimal kleiner. Gerechnet
wurde die Notbeleuchtungs-Variante; worin sich die zweite Fassung unterscheidet, ist
**nicht** geprüft.

---

## Auffälligkeiten

Sortiert, damit sichtbar wird, wo die Erkennung am schwächsten ist. Befund, keine Bewertung.

### 1. Höchster Anteil untypisierter Räume (≥ 25 %)

| Plan | Gruppe | Räume | untyp. | Anteil |
|---|---|--:|--:|--:|
| BaufeldE2_NB_UG | B | 266 | 237 | 89 % |
| Mollgasse_KG1 | A | 31 | 24 | 77 % |
| Fischamend_E_UG | B | 43 | 30 | 70 % |
| Barawitzka_KG | A | 41 | 28 | 68 % |
| Mollgasse_KG2 | A | 30 | 19 | 63 % |
| Herrenholz_EG | A | 498 | 244 | 49 % |
| Fischamend_BT1_UG | A | 44 | 21 | 48 % |
| Rennweg_UG | A | 23 | 10 | 43 % |
| Barawitzka_FDM | A | 8 | 3 | 38 % |
| Barawitzka_3ST | A | 36 | 11 | 31 % |

Muster: **Keller-/Untergeschosse typisieren durchgehend schlecht** — der Raum-Typ-Wortschatz
greift im UG/KG nicht. Größter Absolutwert ist `Herrenholz_EG` mit 244 untypisierten Räumen,
gefolgt von `BaufeldE2_NB_UG` mit 237. **@EnisAMG: das ist die Vokabular-Frage** — welche
Bezeichnungen aus den UG-Plänen sollen in den Typ-Wortschatz? Die Erkennung kann die Typen
nicht selbst erfinden, deshalb steht dort `untypisiert` und nichts anderes.

### 2. Verschluckte Räume (> 90 % Fläche in einem anderen Raum), davon LIFT/SCHACHT

`Paare` = Überlappungs-Beziehungen, `verschluckte Räume` = wie viele **verschiedene** Räume
darin stecken (ein Raum kann in mehreren liegen — deshalb können die Paare die Raumzahl des
Plans übersteigen). `davon LIFT/SCHACHT` sind die gesuchten verschluckten Schacht-/Lift-Polygone.

| Plan | Gruppe | Räume ges. | Paare | verschluckte Räume | davon LIFT/SCHACHT |
|---|---|--:|--:|--:|--:|
| Herrenholz_EG | A | 498 | 257 | 127 | 0 |
| BaufeldE2_NB_UG | B | 266 | 201 | 201 | 0 |
| Barawitzka_KG | A | 41 | 54 | 28 | 1 |
| Muthgasse_E5 | A | 133 | 35 | 32 | 3 |
| Muthgasse_E4 | A | 132 | 33 | 30 | 3 |
| Muthgasse_E3 | A | 135 | 31 | 28 | 3 |
| Muthgasse_E6 | A | 137 | 29 | 26 | 2 |
| Muthgasse_E9 | A | 69 | 27 | 20 | 3 |
| Fischamend_BT2_OG1 | A | 68 | 26 | 24 | 1 |
| Fischamend_E_BT2_OG1 | B | 68 | 26 | 24 | 1 |
| Fischamend_BT1_OG1 | A | 67 | 25 | 25 | 1 |
| Fischamend_BT1_OG2 | A | 67 | 25 | 25 | 1 |
| Fischamend_BT2_OG2 | A | 66 | 25 | 23 | 2 |
| Fischamend_E_BT1_OG1 | B | 69 | 25 | 25 | 2 |
| Muthgasse_E2 | A | 113 | 24 | 21 | 3 |
| Muthgasse_E7 | A | 107 | 24 | 21 | 2 |
| Fischamend_BT2_DG | A | 58 | 23 | 21 | 1 |
| Muthgasse_E8 | A | 106 | 23 | 20 | 3 |
| Fischamend_E_BT1_OG2 | B | 69 | 23 | 23 | 2 |
| Fischamend_E_BT2_DG | B | 58 | 23 | 21 | 1 |

**Nur LIFT/SCHACHT, absteigend:** Muthgasse_E2 (3), Muthgasse_E3 (3), Muthgasse_E4 (3), Muthgasse_E5 (3), Muthgasse_E8 (3), Muthgasse_E9 (3), Barawitzka_1DG (2), Barawitzka_EG (2), Fischamend_BT2_OG2 (2), Muthgasse_E6 (2), Muthgasse_E7 (2), Fischamend_E_BT1_OG1 (2), Fischamend_E_BT1_OG2 (2), Fischamend_E_BT2_OG2 (2), Barawitzka_1ST (1), Barawitzka_2DG (1), Barawitzka_KG (1), Fischamend_BT1_DG (1), Fischamend_BT1_EG (1), Fischamend_BT1_OG1 (1), Fischamend_BT1_OG2 (1), Fischamend_BT1_UG (1), Fischamend_BT2_DG (1), Fischamend_BT2_EG (1), Fischamend_BT2_OG1 (1), Mollgasse_DG (1), Mollgasse_OG3 (1), Fischamend_E_BT1_DG (1), Fischamend_E_BT1_EG (1), Fischamend_E_BT2_DG (1), Fischamend_E_BT2_EG (1), Fischamend_E_BT2_OG1 (1), Fischamend_E_UG (1).

### 3. Pläne mit **0 erkannten Ausgängen** (weder `final_exit` noch `stair_exit`)

**7 von 62** auswertbaren Plänen. **@mvpo3: diese Pläne bekommen keine sinnvolle
Platzierung** — ohne Ausgang fehlt der Bezugspunkt.

| Plan | Gruppe | Räume | Türen | FW-Segmente |
|---|---|--:|--:|--:|
| Barawitzka_2DG | A | 25 | 47 | 2 |
| Barawitzka_FDM | A | 8 | 0 | 2 |
| Barawitzka_KG | A | 41 | 102 | 0 |
| Herrenholz_OG1 | A | 300 | 640 | 55 |
| Herrenholz_OG2 | A | 155 | 239 | 14 |
| Herrenholz_UG | A | 155 | 239 | 14 |
| Rennweg_OG2 | A | 19 | 38 | 2 |

Zusätzlich **29 Pläne ohne jeden `final_exit`** (Ausgang ins Freie). In Obergeschossen
erwartungsgemäß; **kein einziger EG-Plan** ist darunter.

### 4. Pläne mit 0 Fluchtweg-Segmenten

**2 Pläne:** `Barawitzka_KG`, `Herrenholz_EG`. `Herrenholz_EG` hat 498 Räume und 15 `final_exit`, aber **0 Segmente**;
`Barawitzka_KG` hat 41 Räume, 102 Türen und weder Ausgang noch Segment.

### 5. Dublette

`Herrenholz_UG` und `Herrenholz_OG2` liefern **Zeile für Zeile identische Werte**.
Dateigrößen 28.284.638 vs. 28.284.639 Byte. Das ist die vom Owner vermerkte Dublette
`_ug_V` / `_2og_V` — hier hart bestätigt: derselbe Plan zweimal, nur einer davon ist ein
echtes Geschoss. **Welcher, entscheidet der Owner.**

### 6. Karten, die so nicht vorzeigbar sind

**Alle 8 Muthgasse-Karten.** Die Zahlen stimmen, das PNG nicht: der Modelspace enthält
mehrere abgesetzte Zeichnungen (Lageplan-Kasten, Plan-Fragmente), der Auto-Zoom umfasst
alles, der eigentliche Grundriss sitzt als briefmarkengroßer Fleck oben links, die Legende
liegt darüber. `plan_pruefen._varianten_bounds` kennt nur den Barawitzka-Stempel-Prefix —
für Muthgasse braucht es eine eigene Bounds-Heuristik.

**`Barawitzka_FDM`** ist ein Fundamentplan (Ebene −2): 8 Räume, 0 Türen, 0 Ausgänge. Als
Draufsicht mitgerechnet, inhaltlich wahrscheinlich kein Grundriss. Owner-Entscheidung.

**Sichtgeprüft** wurden nur `Rennweg_UG` (sauber), `Herrenholz_EG` (dicht, aber lesbar) und
`Muthgasse_E2` (s. o.). Die übrigen ~59 PNGs wurden **nicht** einzeln angesehen.

### 7. Renderlast

`BaufeldE2_NB_OG1` und `BaufeldE2_NB_OG3` sind im 2-parallel-Lauf mit `MemoryError` im
ezdxf/matplotlib-Render (`LineCollection.set_segments`) gescheitert und **seriell**
nachgezogen worden — beide dann ok (512,5 s / 819,4 s). Ein Prozess stand dabei bei 22,3 GB.
Das ist Leonis' bekannter Befund (der Render-Pfad wächst monoton), hier reproduziert.

### 8. Das `floor`-Feld des Modells ist unbrauchbar

**43 von 62** auswertbaren Plänen melden `floor == "EG"`, darunter jedes Fischamend-
Obergeschoss, alle acht Muthgasse-Ebenen und alle Mollgasse-Geschosse. Nur bei Rennweg,
Herrenholz und Baufeld E2 steht ein echtes Geschoss drin. Die Geschoss-Spalte oben kommt
deshalb aus dem Dateinamen, nicht aus dem Modell. Befund, nicht korrigiert — die Erkennung
soll nichts erfinden.

