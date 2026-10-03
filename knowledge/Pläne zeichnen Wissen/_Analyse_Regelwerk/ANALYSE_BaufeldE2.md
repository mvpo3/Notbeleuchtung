# ANALYSE — Projekt 5: Baufeld E2 (nur DXF, UG)

Quelle: `Baufeld E2 Notbeleuchtung zeichnen\Notbeleuchtungspläne_UG_RIVO_mit_Lehrlayern.dxf` — Bewertung jeder Leuchte nach den
Mollgasse-BASIS-Regeln (mechanische Checks, `scripts/e2_auswertung.py`).
Die Datei ist die Owner-Referenz mit Lehrlayern: 118 grüne Personen
(`E2_MOL_LEHRPERSON_ZENTRIERT`), 269 türkise Blickkeile (SOLID auf
`E2_LEHR_WEG_B_INTERPRETATION`), Fluchtlinien (`681 Fluchtlinien`).

**Bilanz: 89 Leuchten — 87 ok · 2 Abweichung · 0 unprüfbar** (unprüfbar = keine ankommende Person im 12-m-Umkreis;
ehrlich ausgewiesen, nicht als ok gezählt).

Checks: **B1** Front/Balken zeigt zum ankommenden Menschen (NB-R06-Familie,
Toleranz 60°) · **B2** türkiser Blickkeil ≤ 4 m am RZ · **B3** bothsided nur
bei Ankunft aus Gegenrichtungen (Winkelspann ≥ 120°).

| Handle | Block | Welt-Pfeil | Status | Befund |
|---|---|---|---|---|
| 81C94 | RIVO_ARR_left | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 999EB (172 Grad, d=10930 mm, delta=8 Grad) · B2_blickkeil: ok: Keil 9A649 in 1091 mm |
| 81CB6 | RIVO_ARR_left | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 998B7 (159 Grad, d=5949 mm, delta=21 Grad) · B2_blickkeil: ok: Keil 998BB in 532 mm |
| 81CD8 | RIVO_ARR_left | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 998B9 (236 Grad, d=10700 mm, delta=56 Grad) · B2_blickkeil: ok: Keil 99845 in 912 mm |
| 81D1C | RIVO_ARR_left | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99A82 (178 Grad, d=11046 mm, delta=2 Grad) · B2_blickkeil: ok: Keil 99852 in 613 mm |
| 81D3E | RIVO_ARR_left | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99A7A (273 Grad, d=11300 mm, delta=3 Grad) · B2_blickkeil: ok: Keil 9A4E5 in 873 mm |
| 81D60 | RIVO_ARR_left | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 998C4 (268 Grad, d=9563 mm, delta=2 Grad) · B2_blickkeil: ok: Keil 9985B in 672 mm |
| 81DE8 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99D18 (267 Grad, d=1260 mm, delta=3 Grad) · B2_blickkeil: ok: Keil 9B052 in 404 mm |
| 81E0A | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99D3B (270 Grad, d=2785 mm, delta=0 Grad) · B2_blickkeil: ok: Keil 9B18D in 450 mm |
| 81E2C | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99D5E (270 Grad, d=2718 mm, delta=0 Grad) · B2_blickkeil: ok: Keil 9B2C8 in 793 mm |
| 81E4E | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99D81 (270 Grad, d=2927 mm, delta=0 Grad) · B2_blickkeil: ok: Keil 9B2EB in 814 mm |
| 81E70 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99DA4 (268 Grad, d=2912 mm, delta=2 Grad) · B2_blickkeil: ok: Keil 9B30E in 801 mm |
| 81E92 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99DC7 (270 Grad, d=2901 mm, delta=0 Grad) · B2_blickkeil: ok: Keil 9B331 in 570 mm |
| 81EB4 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 9BF7D (269 Grad, d=2617 mm, delta=1 Grad) · B2_blickkeil: ok: Keil 9B8CA in 630 mm |
| 81ED6 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99EE4 (263 Grad, d=2063 mm, delta=7 Grad) · B2_blickkeil: ok: Keil 9B8A7 in 652 mm |
| 81EF8 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99F07 (269 Grad, d=2279 mm, delta=1 Grad) · B2_blickkeil: ok: Keil 9B910 in 850 mm |
| 81F1A | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99F2A (266 Grad, d=2356 mm, delta=4 Grad) · B2_blickkeil: ok: Keil 9B956 in 897 mm |
| 81F3C | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 9A086 (266 Grad, d=2482 mm, delta=4 Grad) · B2_blickkeil: ok: Keil 9BA70 in 566 mm |
| 81F5E | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 9A292 (260 Grad, d=2954 mm, delta=10 Grad) · B2_blickkeil: ok: Keil 9BAB9 in 681 mm |
| 81F80 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 9A293 (265 Grad, d=3609 mm, delta=5 Grad) · B2_blickkeil: ok: Keil 9BAC3 in 401 mm |
| 81FA2 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 9A086 (294 Grad, d=5543 mm, delta=24 Grad) · B2_blickkeil: ok: Keil 9B9C1 in 471 mm |
| 81FE6 | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99C8C (162 Grad, d=1365 mm, delta=18 Grad) · B2_blickkeil: ok: Keil 9B00B in 561 mm |
| 82008 | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99E10 (183 Grad, d=2290 mm, delta=3 Grad) · B2_blickkeil: ok: Keil 9B561 in 532 mm |
| 8202A | RIVO_ARR_down | 0° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 0 Grad ~ Person 99F91 (1 Grad, d=11829 mm, delta=1 Grad) · B2_blickkeil: ok: Keil 9B3BD in 491 mm |
| 8204C | RIVO_ARR_down | 360° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 360 Grad ~ Person 99FD7 (11 Grad, d=1930 mm, delta=11 Grad) · B2_blickkeil: ok: Keil 9B81B in 1012 mm |
| 8206E | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99FFA (184 Grad, d=2168 mm, delta=4 Grad) · B2_blickkeil: ok: Keil 9B9BF in 519 mm |
| 820B2 | RIVO_ARR_down | 0° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 0 Grad ~ Person 99FD7 (359 Grad, d=11715 mm, delta=1 Grad) · B2_blickkeil: ok: Keil 9B74B in 579 mm |
| 820D4 | RIVO_ARR_down | 0° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 0 Grad ~ Person 9A295 (2 Grad, d=9089 mm, delta=2 Grad) · B2_blickkeil: ok: Keil 9BA07 in 406 mm |
| 820F6 | RIVO_ARR_down | 0° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 0 Grad ~ Person 9A294 (356 Grad, d=4360 mm, delta=4 Grad) · B2_blickkeil: ok: Keil 9BB32 in 582 mm |
| 82118 | RIVO_ARR_down | 90° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 90 Grad ~ Person 9A19C (98 Grad, d=764 mm, delta=8 Grad) · B2_blickkeil: ok: Keil 9BE11 in 330 mm |
| 8213A | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99D18 (274 Grad, d=3937 mm, delta=4 Grad) · B2_blickkeil: ok: Keil 9B0BB in 514 mm |
| 8215C | RIVO_ARR_down | 360° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 360 Grad ~ Person 9A228 (359 Grad, d=3983 mm, delta=1 Grad) · B2_blickkeil: ok: Keil 9BCF9 in 918 mm |
| 821C2 | RIVO_ARR_right | 0° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 0 Grad ~ Person 9A291 (1 Grad, d=8248 mm, delta=1 Grad) · B2_blickkeil: ok: Keil 9BFDD in 1450 mm |
| 82206 | RIVO_ARR_left | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 9A0CC (286 Grad, d=4582 mm, delta=16 Grad) · B2_blickkeil: ok: Keil 9BD62 in 537 mm |
| 82228 | RIVO_ARR_right | 90° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 90 Grad ~ Person 99B97 (104 Grad, d=10219 mm, delta=14 Grad) · B2_blickkeil: ok: Keil 9AE8A in 1036 mm |
| 8224A | RIVO_ARR_left | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99BDD (189 Grad, d=3576 mm, delta=9 Grad) · B2_blickkeil: ok: Keil 9AED0 in 495 mm |
| 8226C | RIVO_ARR_down | 0° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 0 Grad ~ Person 9BF0B (359 Grad, d=11922 mm, delta=1 Grad) · B2_blickkeil: ok: Keil 9B46C in 419 mm |
| 8228E | RIVO_ARR_down | 0° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 0 Grad ~ Person 99DEB (359 Grad, d=10897 mm, delta=1 Grad) · B2_blickkeil: ok: Keil 9B51B in 445 mm |
| 822D2 | RIVO_ARR_down | 90° | abweichung | B1_front_zum_menschen: abweichung: bestes delta=61 Grad (Person 99E34, Pfeil 90 vs Richtung 151) · B2_blickkeil: ok: Keil 9B5A7 in 430 mm |
| 822F4 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 9BF57 (311 Grad, d=764 mm, delta=41 Grad) · B2_blickkeil: ok: Keil 9B69C in 496 mm |
| 82338 | RIVO_ARR_right | 90° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 90 Grad ~ Person 99BDD (82 Grad, d=4627 mm, delta=8 Grad) · B2_blickkeil: ok: Keil 9B0DE in 631 mm |
| 82915 | RIVO_ARR_left | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 9BEB1 (276 Grad, d=9604 mm, delta=6 Grad) · B2_blickkeil: ok: Keil 99856 in 681 mm |
| 82937 | RIVO_ARR_left | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 998B9 (268 Grad, d=9003 mm, delta=2 Grad) · B2_blickkeil: ok: Keil 9985F in 440 mm |
| 84172 | RIVO_ARR_down | 90° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 90 Grad ~ Person 9A1BF (90 Grad, d=2360 mm, delta=0 Grad) · B2_blickkeil: ok: Keil 9BC90 in 871 mm |
| 841BC | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 9A292 (260 Grad, d=5217 mm, delta=10 Grad) · B2_blickkeil: ok: Keil 9BABF in 448 mm |
| 84206 | RIVO_ARR_down | 0° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 0 Grad ~ Person 9A228 (357 Grad, d=2300 mm, delta=3 Grad) · B2_blickkeil: ok: Keil 9BCD6 in 610 mm |
| 84250 | RIVO_ARR_down | 90° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 90 Grad ~ Person 99B97 (77 Grad, d=7620 mm, delta=13 Grad) · B2_blickkeil: ok: Keil 9ADB8 in 539 mm |
| 8429A | RIVO_ARR_down | 0° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 0 Grad ~ Person 998BF (358 Grad, d=11239 mm, delta=2 Grad) · B2_blickkeil: ok: Keil 9A2FB in 566 mm |
| 842E4 | RIVO_ARR_down | 0° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 0 Grad ~ Person 998C0 (358 Grad, d=10388 mm, delta=2 Grad) · B2_blickkeil: ok: Keil 9A387 in 446 mm |
| 8432E | RIVO_ARR_down | 90° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 90 Grad ~ Person 9990D (107 Grad, d=1199 mm, delta=17 Grad) · B2_blickkeil: ok: Keil 9A341 in 330 mm |
| 84378 | RIVO_ARR_down | 90° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 90 Grad ~ Person 99910 (108 Grad, d=1225 mm, delta=18 Grad) · B2_blickkeil: ok: Keil 9A364 in 551 mm |
| 843C2 | RIVO_ARR_down | 90° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 90 Grad ~ Person 999C5 (93 Grad, d=2011 mm, delta=3 Grad) · B2_blickkeil: ok: Keil 9A3CD in 792 mm |
| 84457 | RIVO_ARR_right | 0° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 0 Grad ~ Person 998C3 (337 Grad, d=11944 mm, delta=23 Grad) · B2_blickkeil: ok: Keil 9ACE6 in 631 mm |
| 844A1 | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 999E9 (177 Grad, d=3511 mm, delta=3 Grad) · B2_blickkeil: ok: Keil 9A47C in 820 mm |
| 844EB | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 999EB (177 Grad, d=3510 mm, delta=2 Grad) · B2_blickkeil: ok: Keil 9A784 in 659 mm |
| 84535 | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99A55 (171 Grad, d=1642 mm, delta=9 Grad) · B2_blickkeil: ok: Keil 9AC59 in 536 mm |
| 8457F | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99A68 (172 Grad, d=2169 mm, delta=8 Grad) · B2_blickkeil: ok: Keil 9AC57 in 547 mm |
| 845C9 | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99A69 (169 Grad, d=2110 mm, delta=11 Grad) · B2_blickkeil: ok: Keil 9AB1A in 528 mm |
| 84613 | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99A6A (167 Grad, d=2125 mm, delta=13 Grad) · B2_blickkeil: ok: Keil 9AA8D in 556 mm |
| 8465D | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99A6B (168 Grad, d=2089 mm, delta=12 Grad) · B2_blickkeil: ok: Keil 9AA00 in 556 mm |
| 846A7 | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99A6C (173 Grad, d=2064 mm, delta=7 Grad) · B2_blickkeil: ok: Keil 9A9D8 in 625 mm |
| 846F1 | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99A6D (175 Grad, d=2399 mm, delta=5 Grad) · B2_blickkeil: ok: Keil 9A879 in 961 mm |
| 8473B | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99A6D (178 Grad, d=4344 mm, delta=2 Grad) · B2_blickkeil: ok: Keil 9A89C in 337 mm |
| 84785 | RIVO_ARR_down | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99A6F (175 Grad, d=2891 mm, delta=5 Grad) · B2_blickkeil: ok: Keil 9A8E3 in 446 mm |
| 84818 | RIVO_ARR_down | 0° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 0 Grad ~ Person 9BEB1 (353 Grad, d=1822 mm, delta=7 Grad) · B2_blickkeil: ok: Keil 99867 in 367 mm |
| 84862 | RIVO_ARR_right | 90° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 90 Grad ~ Person 9990D (105 Grad, d=6338 mm, delta=15 Grad) · B2_blickkeil: ok: Keil 9986C in 665 mm |
| 848AC | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 998C5 (256 Grad, d=993 mm, delta=14 Grad) · B2_blickkeil: ok: Keil 9986E in 733 mm |
| 848F6 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 998E8 (257 Grad, d=1406 mm, delta=13 Grad) · B2_blickkeil: ok: Keil 9A2D8 in 613 mm |
| 84940 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99A7D (251 Grad, d=841 mm, delta=19 Grad) · B2_blickkeil: ok: Keil 9A626 in 398 mm |
| 8498A | RIVO_ARR_right | 90° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 90 Grad ~ Person 99910 (83 Grad, d=10636 mm, delta=7 Grad) · B2_blickkeil: ok: Keil 9A603 in 555 mm |
| 849D4 | RIVO_ARR_left | 90° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 90 Grad ~ Person 99A83 (82 Grad, d=8821 mm, delta=8 Grad) · B2_blickkeil: ok: Keil 9A73E in 914 mm |
| 84A1E | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99A78 (268 Grad, d=11374 mm, delta=2 Grad) · B2_blickkeil: ok: Keil 9AC55 in 880 mm |
| 84A68 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99A76 (269 Grad, d=10076 mm, delta=1 Grad) · B2_blickkeil: ok: Keil 9ABC9 in 286 mm |
| 84AB2 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99A74 (270 Grad, d=10051 mm, delta=0 Grad) · B2_blickkeil: ok: Keil 9AAB0 in 426 mm |
| 84AFC | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99A75 (268 Grad, d=9702 mm, delta=2 Grad) · B2_blickkeil: ok: Keil 9AB60 in 378 mm |
| 84B46 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99A72 (269 Grad, d=11185 mm, delta=1 Grad) · B2_blickkeil: ok: Keil 9AA23 in 479 mm |
| 84B90 | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99A71 (269 Grad, d=9076 mm, delta=1 Grad) · B2_blickkeil: ok: Keil 9A9DA in 553 mm |
| 84BDA | RIVO_ARR_down | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99A71 (253 Grad, d=1186 mm, delta=17 Grad) · B2_blickkeil: ok: Keil 9A94C in 592 mm |
| 9362D | RIVO_ARR_down | 90° | abweichung | B1_front_zum_menschen: abweichung: bestes delta=113 Grad (Person 998B5, Pfeil 90 vs Richtung 337) · B2_blickkeil: kein Keil im Umkreis (nächster 4634 mm) |
| 9981C | RIVO_ARR_left | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 9990D (167 Grad, d=9829 mm, delta=13 Grad) · B2_blickkeil: ok: Keil 9984E in 589 mm |
| 99939 | RIVO_ARR_right | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 99A7C (274 Grad, d=11818 mm, delta=4 Grad) · B2_blickkeil: ok: Keil 9A436 in 1071 mm |
| 99AAC | RIVO_ARR_bothsided | — | ok | B3_beidseitig: ok: Personen aus Gegenrichtungen (max Winkelspann 163 Grad) · B2_blickkeil: ok: Keil 9BA93 in 534 mm |
| 99AAD | RIVO_ARR_bothsided | — | ok | B3_beidseitig: ok: Personen aus Gegenrichtungen (max Winkelspann 174 Grad) · B2_blickkeil: ok: Keil 9BCD6 in 420 mm |
| 99AF2 | RIVO_ARR_bothsided | — | ok | B3_beidseitig: ok: Personen aus Gegenrichtungen (max Winkelspann 179 Grad) · B2_blickkeil: ok: Keil 9AFC5 in 373 mm |
| 99B43 | RIVO_ARR_bothsided | — | ok | B3_beidseitig: ok: Personen aus Gegenrichtungen (max Winkelspann 175 Grad) · B2_blickkeil: ok: Keil 9BC27 in 523 mm |
| 99B4D | RIVO_ARR_right | 270° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 270 Grad ~ Person 9A294 (269 Grad, d=11647 mm, delta=1 Grad) · B2_blickkeil: ok: Keil 9C025 in 903 mm |
| 9BEDB | RIVO_ARR_bothsided | — | ok | B3_beidseitig: ok: Personen aus Gegenrichtungen (max Winkelspann 179 Grad) · B2_blickkeil: ok: Keil 9A571 in 316 mm |
| 9BF34 | RIVO_ARR_right | 180° | ok | B1_front_zum_menschen: ok: Welt-Pfeil 180 Grad ~ Person 99E10 (120 Grad, d=7825 mm, delta=59 Grad) · B2_blickkeil: ok: Keil 9B633 in 640 mm |
| 9BFAF | RIVO_ARR_bothsided | — | ok | B3_beidseitig: ok: Personen aus Gegenrichtungen (max Winkelspann 180 Grad) · B2_blickkeil: ok: Keil 9BB55 in 1282 mm |
| 9C06F | RIVO_ARR_bothsided | — | ok | B3_beidseitig: ok: Personen aus Gegenrichtungen (max Winkelspann 178 Grad) · B2_blickkeil: ok: Keil 99729 in 322 mm |

Abweichungen sind KANDIDATEN für das Konfliktprotokoll bzw. für
Regel-Grenzfälle (Personen-Dichte im UG ist hoch — die nächste ankommende
Person ist nicht immer die regelgebende). Kein automatischer
KONFLIKTE-Eintrag ohne visuelle Gegenprüfung (crop_dxf.py).