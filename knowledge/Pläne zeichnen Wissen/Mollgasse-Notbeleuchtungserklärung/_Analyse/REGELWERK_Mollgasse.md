# REGELWERK Mollgasse — Basis-Zeichenregeln (aus PDF 95 S. + 8 Erklär-DXFs)

Generiert aus dem Gate-geprüften Gesamt-Regelwerk (REGELWERK_Notbeleuchtung.json) — nur Mollgasse-belegte BASIS-Regeln; Häufigkeit = Mollgasse-PDF-Seiten + vermessene DXF-Belege. Nicht von Hand editieren.

**35 Basis-Regeln.**

### RW-001 (NB-R01) — tuer_rz
Raum bindet ueber eine Tuer an den Fluchtweg an und erhaelt ein Tuer-RZ → in der Tuerachse, raumseitig hinter der Schwelle
- **Geometrie/Rotation:** Welt-Pfeil in den Raum = entgegen Fluchtrichtung durch die Tuer = entgegen Tuer-Oeffnungsrichtung
- **Leuchtentyp:** notlicht_ks_stiege_unten
- **PDF:** S.1,2,3,4,14,20,43,51,60,61,69,70,72,85
- **DXF-Belege (39):** 20240 (WHA_MOL_EG, rot 89.99) · 20286 (WHA_MOL_EG, rot 359.99) · 202A9 (WHA_MOL_EG, rot 179.99) · 202A9 (WHA_MOL_EG, rot 179.99) … +35
- **Häufigkeit:** 14 PDF-Seiten, 39 DXF-Belege
- **Grenzfälle/Parameter:** `{"quer_zur_tuerachse_mm": {"gemessen": [3, 35], "toleranz": 50}, "raumseitiger_versatz_mm": {"gemessen": [735, 930], "hinweis": "Gang-Trenntuer 1OG: 258 gangseitig der Wandachse"}}`
- **Begründung/Quelle:** PDF S.1-4, 12, 14, 20 — Tuer muss bei Netzausfall auffindbar bleiben, Pfeil zeigt in den Raum

### RW-002 (NB-R02) — allgemeinbereiche
Raum ist Allgemeinbereich (fuer alle Bewohner zugaenglich; meist EG/UG): MUELLRAUM, FAHRRADRAUM(ABSTELLRAUM communal), KINDERWAGENRAUM, KELLERABTEIL, TECHNIK, SPIELRAUM, GESCHAEFTSLOKAL, Innenhof-Anbindung → bei der Tuer nach NB-R01; EIN RZ genuegt bei freier Sicht aus dem ganzen Raum
- **Geometrie/Rotation:** nach NB-R01
- **Leuchtentyp:** notlicht_ks_stiege_unten
- **PDF:** S.2,3,4,11,12,45,62
- **DXF-Belege (13):** 20286 (WHA_MOL_EG, rot 359.99) · 202A9 (WHA_MOL_EG, rot 179.99) · 202A9 (WHA_MOL_EG, rot 179.99) · 206E7 (WHA_MOL_EG, rot 359.99) … +9
- **Häufigkeit:** 7 PDF-Seiten, 13 DXF-Belege
- **Grenzfälle/Parameter:** `{"sichtlinie_max_gemessen_mm": 9143}`
- **Begründung/Quelle:** PDF S.2-4, 11-13 — Allgemeinbereichs-Regel

### RW-003 (NB-R03) — haupteingang
Haupteingangs-/Hauptausgangstuer des Gebaeudes → ueber/vor der Tuer, mittig zur Tuerachse, raumseitig
- **Geometrie/Rotation:** Welt-Pfeil ins Rauminnere
- **Leuchtentyp:** notlicht_ks_stiege_unten
- **PDF:** S.1,6,8
- **DXF-Belege (8):** 20240 (WHA_MOL_EG, rot 89.99) · 2070A (WHA_MOL_EG, rot 269.99) · 20312 (WHA_MOL_EG) · 202EF (WHA_MOL_EG) … +4
- **Häufigkeit:** 3 PDF-Seiten, 8 DXF-Belege
- **Grenzfälle/Parameter:** `{"quer_mm": 26, "raumseitig_mm": {"gemessen": [375, 840]}}`
- **Begründung/Quelle:** PDF S.1, 6, 8, 10 — Ziel der Sichtkette beider Personenstroeme

### RW-004 (NB-R04) — stiegenhauspfeil
Stiegenhaus mit Architekten-Stiegenpfeil (Aufwaertsrichtung JE LAUF) → RZ so, dass Ankommende es beim Erreichen des Geschosses (Blick links/rechts) sofort sehen; je Personenstrom ggf. eigenes RZ
- **Geometrie/Rotation:** UG-Stroeme laufen IN Pfeilrichtung hinauf, OG/DG-Stroeme ENTGEGEN hinunter
- **Leuchtentyp:** -
- **PDF:** S.5,6,7,8,15,21,25,26,27,28,32,38,39,41…
- **DXF-Belege (46):** 202EF (WHA_MOL_EG, rot 89.99) · 20263 (WHA_MOL_EG, rot 359.99) · 20312 (WHA_MOL_EG, rot 359.71) · 20240 (WHA_MOL_EG, rot 89.99) … +42
- **Häufigkeit:** 16 PDF-Seiten, 46 DXF-Belege
- **Grenzfälle/Parameter:** `{"delta_bewegung_vs_pfeil_grad": {"gemessen": [168, 180]}}`
- **Begründung/Quelle:** PDF S.5-8, 15, 19, 25-28, 41

### RW-005 (NB-R05) — vor_der_stiege
Richtungs-RZ fuehrt auf eine Stiege bzw. empfaengt Stiegen-Ankoemmlinge → 800-1122 mm vor der Antritts-/Austrittskante, auf der Laufachse; Wandmontage als Sichtbarkeits-Alternative
- **Geometrie/Rotation:** Welt-Pfeil exakt in Abstiegs-/Weiterrichtung des Laufs, NIE auf eine Wand
- **Leuchtentyp:** notlicht_ks_stiege_links|_rechts (nach NB-R07)
- **PDF:** S.16,23,25,27,29,30,32,34,39,40,41,43,56
- **DXF-Belege (37):** 94FE7 (WHA_MOL_1OG, rot 0) · 94FE8 (WHA_MOL_1OG, rot 89.83) · 95019 (WHA_MOL_1OG, rot 269.55) · 95042 (WHA_MOL_1OG, rot 180.1) … +33
- **Häufigkeit:** 13 PDF-Seiten, 37 DXF-Belege
- **Grenzfälle/Parameter:** `{"abstand_vor_kante_mm": {"gemessen": [801, 1122]}, "quer_zur_laufachse_mm": {"gemessen": [20, 130]}, "pfeil_vs_laufrichtung_grad": {"toleranz": 1.0}}`
- **Begründung/Quelle:** PDF S.16, 25, 30 ('vor der Stiege, sonst zeigt der Pfeil zur Wand'), 39-40

### RW-006 (NB-R06) — pfeil_unten_geradeaus
RZ im geraden Gangverlauf bedeutet 'geradeaus weiter' → mittig im Gang (Gangachse)
- **Geometrie/Rotation:** Welt-Pfeil ENTGEGEN der Fluchtrichtung (Vorderseite frontal zum ankommenden Strom)
- **Leuchtentyp:** notlicht_ks_stiege_unten
- **PDF:** S.16,18,22,24,25,30,33,34,38,40,43,47,48,55…
- **DXF-Belege (62):** 94FE7 (WHA_MOL_1OG, rot 0) · 94FE8 (WHA_MOL_1OG, rot 89.83) · 95019 (WHA_MOL_1OG, rot 269.55) · 95042 (WHA_MOL_1OG, rot 180.1) … +58
- **Häufigkeit:** 23 PDF-Seiten, 62 DXF-Belege
- **Grenzfälle/Parameter:** `{"neben_gangachse_mm": {"gemessen": [6, 95]}, "delta_pfeil_vs_fluss_grad": {"gemessen": [178.6, 180.0]}}`
- **Begründung/Quelle:** PDF S.18, 33-34

### RW-007 (NB-R07) — frontalsicht_auswahl
Auswahl links/rechts/unten fuer ein Richtungs-RZ → Symbol-Laengsachse quer zum Betrachter-Korridor
- **Geometrie/Rotation:** Pfeil = Fluchtrichtung AUS SICHT der Person; Person muss die Vorderseite sehen
- **Leuchtentyp:** notlicht_ks_stiege_links|_rechts|_unten
- **PDF:** S.6,13,15,17,22,23,25,27,29,30,31,32,33,34…
- **DXF-Belege (62):** 41249 (WHA_MOL_4OG, rot 269.42) · 4121F (WHA_MOL_4OG, rot 359.87) · 41220 (WHA_MOL_4OG, rot 359.42) · 413A0 (WHA_MOL_4OG, rot 179.71) … +58
- **Häufigkeit:** 29 PDF-Seiten, 62 DXF-Belege
- **Grenzfälle/Parameter:** `{"erstleuchte_sichtwinkel_zur_normalen_grad": {"gemessen": [0.3, 45.5], "falschvariante": 89}, "folgeleuchte": "nur Sichtbarkeit noetig (bis ~47.5 Grad, Seitenansicht toleriert 86-`
- **Begründung/Quelle:** PDF S.31-37 (Vergleichsbeispiele 'Pfeil unten statt links' = Seitenansicht = falsch)

### RW-008 (NB-R08) — erster_blick
Verlassen jeder Wohnung / jedes Raums → eine relevante Leuchte muss direkt sichtbar sein; bei zu grosser Entfernung ZUSATZ-Leuchte dazwischen; ein RZ darf mehrere Tueren bedienen
- **Geometrie/Rotation:** -
- **Leuchtentyp:** -
- **PDF:** S.9,13,14,15,17,18,20,21,22,23,24,25,27,29…
- **DXF-Belege (62):** 95042 (WHA_MOL_1OG, rot 180.1) · 95066 (WHA_MOL_1OG, rot 90) · 95067 (WHA_MOL_1OG, rot 90) · 952E9 (WHA_MOL_1OG, rot 359.55) … +58
- **Häufigkeit:** 30 PDF-Seiten, 62 DXF-Belege
- **Grenzfälle/Parameter:** `{"sichtlinien": "eine je Wohnungstuer, Start <=136 mm neben der Tuer, Laenge 882-12028 mm, 0 Wandschnitte", "mehrfachbedienung": "bis 4 Wohnungstueren je RZ (1140-4275 mm)"}`
- **Begründung/Quelle:** PDF S.14, 17-18 (Zusatz-RZ wegen Distanz), 22, 27, 29-30, 39

### RW-009 (NB-R09) — gang_mit_ohne_stgh_tuer
Gang muendet ins Stiegenhaus → MIT Trenntuer: Tuer-RZ an der Trenntuer (NB-R01) + 2 antipanik_leuchte auf der Gangmittellinie. OHNE Trenntuer: KEIN Tuer-RZ an der Muendung; Richtungs-RZ am Knick bzw. vor der Stiege (NB-R05)
- **Geometrie/Rotation:** nach NB-R01/NB-R06/NB-R07
- **Leuchtentyp:** siehe Faelle
- **PDF:** S.14,20,21,29
- **DXF-Belege (18):** 95042 (WHA_MOL_1OG, rot 180.1) · 95066 (WHA_MOL_1OG, rot 90) · 95067 (WHA_MOL_1OG, rot 90) · 9568B (WHA_MOL_1OG, rot 89.99) … +14
- **Häufigkeit:** 4 PDF-Seiten, 18 DXF-Belege
- **Grenzfälle/Parameter:** `{"ap_teilung_12m_gang_mm": [3090, 6297, 2579], "ap_neben_fluchtlinie_mm": 55, "alternativen_nur_text": "2 Aufheller | mittiges down-RZ | down-RZ + Aufheller (Wahl nach Situation, L`
- **Begründung/Quelle:** PDF S.14, 19, 20-21, 29

### RW-010 (NB-R10) — antipanik_sichtblockade
Sicht der Person auf die Notleuchte ist blockiert (L-/U-Raumform, Wand dazwischen) ODER Lux-Nachweis im Gang scheitert → im abgeschatteten Bereich (gemessen 3211 mm vor der Person); rechteckige Raeume ohne Blockade: KEINE
- **Geometrie/Rotation:** -
- **Leuchtentyp:** antipanik_leuchte
- **PDF:** S.2,10,11,12,50,68,82
- **DXF-Belege (20):** 2070C (WHA_MOL_EG, rot 269.99) · 20752 (WHA_MOL_EG, rot 359.99) · 20286 (WHA_MOL_EG, rot 359.99) · 21312 (WHA_MOL_EG, rot 269.99) … +16
- **Häufigkeit:** 7 PDF-Seiten, 20 DXF-Belege
- **Grenzfälle/Parameter:** `{"lux_nachweis": "separater Nachweis (Lichtberechnung) — hier nur Flag lux_nachweis_erforderlich"}`
- **Begründung/Quelle:** PDF S.2 (L-Form Muellraum), 10-12

### RW-011 (NB-R11) — hindernis_versatz
Sollposition kollidiert mit Hindernis (z.B. Lichtkuppel, blau markiert) → quer versetzen bis frei (gemessen 142 mm Versatz, 292 mm Zentrum->Kuppelkante)
- **Geometrie/Rotation:** UNVERAENDERT beibehalten
- **Leuchtentyp:** -
- **PDF:** S.40
- **DXF-Belege (5):** 20864 (WHA_MOL_DG, rot 269.71) · 2083F (WHA_MOL_DG, rot 359.42) · 206DB (WHA_MOL_DG) · 20705 (WHA_MOL_DG) … +1
- **Häufigkeit:** 1 PDF-Seiten, 5 DXF-Belege
- **Begründung/Quelle:** PDF S.40

### RW-012 (NB-R12) — sichtkette_abstaende
Folge von RZ entlang des Fluchtwegs → lueckenlose Kette bis zum Ausgang; Wand-RZ mit Kante an Wandkante (15-101 mm)
- **Geometrie/Rotation:** -
- **Leuchtentyp:** -
- **PDF:** S.5,6,7,8,9,13,16,22,25,28,32,36,38,48…
- **DXF-Belege (59):** 202EF (WHA_MOL_EG, rot 89.99) · 20263 (WHA_MOL_EG, rot 359.99) · 20312 (WHA_MOL_EG, rot 359.71) · 20240 (WHA_MOL_EG, rot 89.99) … +55
- **Häufigkeit:** 21 PDF-Seiten, 59 DXF-Belege
- **Grenzfälle/Parameter:** `{"folgeabstaende_mm": {"gemessen": [1975, 7749]}, "sichtlinien_ende": "an der Symbol-KANTE, nicht am Zentrum"}`
- **Begründung/Quelle:** PDF S.5-9 (EG-Ketten)

### RW-013 (NB-R13) — ug_stiegenrichtung
Untergeschoss: Personen fluechten HINAUF ueber die Stiege → Leuchte vor/an der Stiege (NB-R05)
- **Geometrie/Rotation:** Welt-Pfeil = Aufwaertsrichtung des Laufs = IN Stiegenhauspfeilrichtung (OG: entgegen, NB-R04); Frontseite zum ankommenden UG-Strom
- **Leuchtentyp:** -
- **PDF:** S.41,43,54,55,56,71,75,92,93
- **DXF-Belege (28):** 1BEE4 (WHA_MOL_1KG) · 1BCBB (WHA_MOL_1KG) · 1BCBE (WHA_MOL_1KG) · 1BE99 (WHA_MOL_1KG) … +24
- **Häufigkeit:** 9 PDF-Seiten, 28 DXF-Belege
- **Begründung/Quelle:** PDF S.43, 54-55 — UG-Gegenstueck zu NB-R04

### RW-014 (NB-R14) — montageort_wand_decke
Wahl Wand- vs. Deckenmontage → Stiegen-Leuchten = Wand; Gang-Leuchten = Decke, mittig
- **Geometrie/Rotation:** -
- **Leuchtentyp:** -
- **PDF:** S.16,32,56
- **DXF-Belege (14):** 94FE7 (WHA_MOL_1OG) · 9568B (WHA_MOL_1OG) · 94FE8 (WHA_MOL_1OG) · 956B0 (WHA_MOL_1OG) … +10
- **Häufigkeit:** 3 PDF-Seiten, 14 DXF-Belege
- **Begründung/Quelle:** PDF S.56 woertlich: Notleuchten an Waenden hauptsaechlich bei Stiegen; alle 14 1KG-Platzierungen konsistent

### RW-015 (NB-R15) — kabeltrasse_hindernis
Sollposition liegt auf/nahe einer Kabeltrasse (blaue Balken, KT300/KT400/KT500) → NIE auf der Trasse; seitlich versetzen, moeglichst >= 450 mm Abstand
- **Geometrie/Rotation:** nach Versatz erhalten: Sichtbarkeit, Pfeilrichtung, Frontseite, Fluchtwegbezug, Gebaeudehaelfte
- **Leuchtentyp:** -
- **PDF:** S.63,64,65,79,81,84,85,88
- **DXF-Belege (15):** 1C7CB (WHA_MOL_2KG) · 1C8A9 (WHA_MOL_2KG) · 1C7CC (WHA_MOL_2KG) · 1C695 (WHA_MOL_2KG) … +11
- **Häufigkeit:** 8 PDF-Seiten, 15 DXF-Belege
- **Grenzfälle/Parameter:** `{"abstand_mm": {"soll_min": 450, "modalitaet": "moeglichst (Fachpraxis-SOLL)"}, "versatz_gemessen_mm": [507]}`
- **Begründung/Quelle:** PDF S.63-64 woertlich; 2KG (A)-Ana 1C7D0 bleibt trotz Versatz auf der Anastasius-Seite. ACHTUNG: Rigole (Bodenrinnen-Schraffuren) sind KEINE Kabeltrassen

### RW-016 (NB-R16) — beidseitig
ZWEI Personenstroeme aus Gegenrichtungen nutzen denselben Fluchtweg-Knoten und brauchen beide die Frontseite → am gemeinsamen Knoten (GT: 2 gespiegelte Einzel-Bloecke, Abstand 264-318 mm; Engine: RIVO_NL_ARR_bothsided)
- **Geometrie/Rotation:** Achse = Fluchtweg-Achse beider Stroeme
- **Leuchtentyp:** notlicht_ks_beidseitig
- **PDF:** S.52,65,66,67,68,69,70,71,72,73,74,75,76,77…
- **DXF-Belege (28):** 1C00E (WHA_MOL_1KG) · 1BFEA (WHA_MOL_1KG) · 1C7CB (WHA_MOL_2KG) · 1C8A9 (WHA_MOL_2KG) … +24
- **Häufigkeit:** 26 PDF-Seiten, 28 DXF-Belege
- **Grenzfälle/Parameter:** `{"alternative": "beidseitig am Richtungswechsel OHNE Gegenstrom = NUR-ALTERNATIVE (orange, 'muss nicht sein') — NICHT automatisieren"}`
- **Begründung/Quelle:** PDF S.65-83; Pflicht-Paare 2KG Gr.1-5 + 1KG (I) + EG-Paar; Gr.6 = einzige Alternative

### RW-017 (NB-R17) — garage_durchquerbarkeit
Fluchtwegfuehrung durch Garagenbereiche → Motorrad-Stellflaechen sind durchquerbar; Doppelparker-/PKW-Flaechen und Gruben NICHT
- **Geometrie/Rotation:** -
- **Leuchtentyp:** -
- **PDF:** S.65,66,67,68,69,70,84,86,87
- **DXF-Belege (17):** 1C7CB (WHA_MOL_2KG) · 1C8A9 (WHA_MOL_2KG) · 1C7CC (WHA_MOL_2KG) · 1C7FB (WHA_MOL_2KG) … +13
- **Häufigkeit:** 9 PDF-Seiten, 17 DXF-Belege
- **Begründung/Quelle:** PDF S.65-70; Personenreihe 1CBF6-1CBFC durch MOTORRAD-Stempel, 0 Fluchtwege durch DOPPELPARKER-Zonen. Durchquerbarkeit folgt aus freier Geometrie, nicht aus dem Raumlabel

### RW-018 (NB-R18) — gebaeudehaelften
Projekt besteht aus zwei zusammengebauten Gebaeuden → Trennung entlang der weitergefuehrten Gebaeudewand; Zuordnung am EG-Grundriss verifizieren; je Haelfte eigene Fluchtwege/Ausgaenge/Label-Alphabete
- **Geometrie/Rotation:** -
- **Leuchtentyp:** -
- **PDF:** S.76,77,78,79,80,81,82,83
- **DXF-Belege (11):** 1C64B (WHA_MOL_2KG) · 1C885 (WHA_MOL_2KG) · 1C66F (WHA_MOL_2KG) · 1C698 (WHA_MOL_2KG) … +7
- **Häufigkeit:** 8 PDF-Seiten, 11 DXF-Belege
- **Grenzfälle/Parameter:** `{"prozessregel": "unklare Zuordnung NIEMALS raten -> offene Frage (PDF S.78, bindend)"}`
- **Begründung/Quelle:** PDF S.76-83; rote Trennlinie 1C7F4 (116 m) auf der Mollgasse-Gebaeudewand

### RW-019 (NB-R19) — ug_nebenraum_tuerleuchte
UG-Nebenraum bindet an den Gang an → TECHNIK/NIEDERSPANNUNG/E-Raum: Tuer-Leuchte nach NB-R01 (mittig 3-26 mm, 711-779 mm zugangsseitig). Einzelne kleine ER/KELLERABTEIL/Medienraum: KEINE eigene Tuerleuchte, wenn nach Tuerdurchtritt sofort ein Gang-RZ sichtbar ist
- **Geometrie/Rotation:** nach NB-R01
- **Leuchtentyp:** notlicht_ks_stiege_unten
- **PDF:** S.45,47,51,52,53,71,72,73,85,90,91,93
- **DXF-Belege (31):** 1BEE4 (WHA_MOL_1KG) · 1BCBB (WHA_MOL_1KG) · 1BE99 (WHA_MOL_1KG) · 1BCBE (WHA_MOL_1KG) … +27
- **Häufigkeit:** 12 PDF-Seiten, 31 DXF-Belege
- **Begründung/Quelle:** PDF S.51-53, 71-73, 93; 1KG-09 (D) + Merktext 'Stromversorgung aller Notleuchten'

### RW-020 (NB-R20) — tuerlose_gaenge_durchgaenge
tuerloser Gang / offener Durchgang im Fluchtweg → tuerloser zusammenhaengender Gang: KEINE Zwischen-RZ solange Sichtkette steht; kurzer Gang mit Direktsicht aller Tueren: genau EIN Tuer-RZ; offener Durchgang als Knoten: down-Typ MITTIG im Durchgang (gemessen 4 mm Mittigkeit bei 1250 mm)
- **Geometrie/Rotation:** down-Typ frontal zum ankommenden Strom (rechts/links/beidseitig am Durchgang im PDF explizit VERWORFEN)
- **Leuchtentyp:** notlicht_ks_stiege_unten
- **PDF:** S.58,59,60,61,62,73,74,90,91
- **DXF-Belege (8):** 1C695 (WHA_MOL_2KG) · 1C7D0 (WHA_MOL_2KG) · 1C707 (WHA_MOL_2KG) · 1C9BD (WHA_MOL_2KG) … +4
- **Häufigkeit:** 9 PDF-Seiten, 8 DXF-Belege
- **Begründung/Quelle:** PDF S.58-62, 73-74, 90-91 — S.73-74 sind dokumentierte Negativ-Beispiele

### RW-021 (NB-R21) — sv_anlage
Projekt braucht Notbeleuchtungs-Stromversorgung → EIN System je Projekt ('meistens' auch bei zwei Gebaeudehaelften), Verteiler im Niederspannungsraum, NICHT an der E-Verteiler-Wand
- **Geometrie/Rotation:** -
- **Leuchtentyp:** gruppenbatterie_anlage
- **PDF:** S.51,71,72
- **DXF-Belege (19):** 1BE99 (WHA_MOL_1KG) · 1BCBE (WHA_MOL_1KG) · 1C695 (WHA_MOL_2KG) · 1C7D0 (WHA_MOL_2KG) … +15
- **Häufigkeit:** 3 PDF-Seiten, 19 DXF-Belege
- **Begründung/Quelle:** PDF S.51, 71-72; 1KG 1CB68, 2KG 1D10E/1D10F

### RW-022 (NB-R22) — quellen_disziplin_fluchtplan
Quelle ist ein Flucht-/Rettungsplan (gruener Aushang), kein Notbeleuchtungsplan → belegt NUR Fluchtweg-Richtung/Tueren/Stiegenhaeuser/Ausgaenge; NICHT Leuchtenposition, Wand-/Deckenmontage, Frontseite, ein-/beidseitig, Typ, Hoehe, Lux, Anzahl
- **Geometrie/Rotation:** Blatt-Richtung != CAD-Richtung != Personen-Richtung; gedrehte Aushang-Blaetter
- **Leuchtentyp:** -
- **PDF:** S.1,2,3,4,5,6,7,8,9,10
- **Häufigkeit:** 10 PDF-Seiten, 0 DXF-Belege
- **Grenzfälle/Parameter:** `{"standort_marke": "Aushang-Bezugspunkt, KEINE Leuchte", "mehrere_blaetter": "gleiches Geschoss aus mehreren Aushaengen = EINE Referenz", "raum_ohne_gruen": "bedeutet NICHT 'keine `
- **Begründung/Quelle:** TOMA S.1-10; Owner-Auftrag Quellen-Trennung A/B/C/D

### RW-023 (NB-R23) — schul_bildungscluster_fluchtweg
Schule, Cluster-/offene-Lernlandschaft-Typologie → offener 'Kommunikations- und Bewegungsbereich' traegt den Fluchtweg; Unterrichtsraeume oeffnen direkt darauf, OHNE 'Gang'-Label
- **Geometrie/Rotation:** -
- **Leuchtentyp:** -
- **PDF:** —
- **Häufigkeit:** 0 PDF-Seiten, 0 DXF-Belege
- **Begründung/Quelle:** TOMA OG-04: Unterrichtsraum 1-4 -> Kommunikations-/Bewegungsbereich -> TH 2. Generalisiert NB-R20 auf Cluster-Ebene

### RW-024 (NB-R24) — mehrere_stiegenhaeuser_gerichtet
Gebaeude mit mehreren Fluchtstiegenhaeusern (TOMA: TH 2/3/4) → Cluster/Gebaeudeteile GEZIELT verschiedenen THs zuordnen; NICHT alle zum naechstgelegenen TH / einem Hauptausgang; mehrere dargestellte Richtungen erhalten
- **Geometrie/Rotation:** -
- **Leuchtentyp:** -
- **PDF:** —
- **Häufigkeit:** 0 PDF-Seiten, 0 DXF-Belege
- **Begründung/Quelle:** TOMA SG/EG/OG; = Variante der Mollgasse-Gebaeudehaelften NB-R18 (unklar -> nicht raten)

### RW-025 (NB-R25) — egress_je_ebene_zieltypen
Sockel-/Untergeschoss und Ziel-Typ-Bestimmung → Sockel-/UG kann direkte Aussenausgaenge auf eigener Ebene haben (Flucht nicht zwingend ueber EG). Ziel-Typen NIE gleichsetzen: Fluchtstiegenhaus / Ausgang ins Freie / Balkon-Terrasse-Loggia / vorlaeufige Evakuierungsstelle / Sammelstelle
- **Geometrie/Rotation:** -
- **Leuchtentyp:** -
- **PDF:** —
- **Häufigkeit:** 0 PDF-Seiten, 0 DXF-Belege
- **Begründung/Quelle:** TOMA SG: viele EN-Tueren ins Freie auf Sockel-Ebene. Ergaenzt NB-R13

### RW-026 (NB-R26) — ausfuehrungsplan_annotationen_anker
Architektur-Ausfuehrungsplan mit Brandschutz-/Flucht-Textannotation → EN 1125 (Panikstange) / EN 179 (Notausgangsbeschlag) = Ausgangstueren; FLn = Fluchtweg-Flaeche mit Soll-m2; EI 30/90/230-C + 'brandlastfreie Zone' + BA = Brandabschnitte; RWA = Rauchabzug; BMZ = Brandmeldezentrale
- **Geometrie/Rotation:** -
- **Leuchtentyp:** -
- **PDF:** —
- **Beleg (alternativ):** Header-Beleg statt Handle: $INSUNITS=6 (Meter) bei mm-Koordinaten in TOMA-/Baufeld-E2-DXFs (inventur.json 'insunits'); Textanker-Fälle AmRain S.13/23 (EINGANG-Modelltext). Prozess-/Eingaberegel ohne eigenen INSERT.
- **Häufigkeit:** 0 PDF-Seiten, 0 DXF-Belege
- **Grenzfälle/Parameter:** `{"daten_fallen": "INSUNITS kann luegen (TOMA=6 Meter, real mm -> ueber Tuerbreiten/Wandstaerken verifizieren); Riesen-Koordinaten-Offset moeglich (TOMA SG ~-1.7e9 -> Healthcheck/Nu`
- **Begründung/Quelle:** TOMA SG/EG/OG: EN/FL/EI/RWA/BMZ als Textannotation mit Koordinaten (inventar_*.json)

### RW-027 (NB-R27) — aufzug_keine_fluchtverbindung
Aufzug im Gebaeude → Aufzug NIE als vertikale Flucht-Kante; Aufzugsvorbereich getrennt (kann Teil des Gangs sein)
- **Geometrie/Rotation:** -
- **Leuchtentyp:** -
- **PDF:** —
- **Häufigkeit:** 0 PDF-Seiten, 0 DXF-Belege
- **Begründung/Quelle:** TOMA Brandfall-Hinweis 'Aufzug nicht benutzen'; deckt sich mit fachpraxis.entferne_schacht_leuchten

### RW-028 — antipanik_laengsachse
Antipanikleuchte: Längsachse in Richtung des auszuleuchtenden (Gang-)Bereichs drehen; Position mittig im abgeschatteten Bereich.
- **Geometrie/Rotation:** Längsachse parallel zur Hauptachse des Zielbereichs
- **Leuchtentyp:** antipanik
- **PDF:** S.58
- **DXF-Belege (2):** 1C707 (WHA_MOL_2KG) · 1C9BD (WHA_MOL_2KG)
- **Häufigkeit:** 1 PDF-Seiten, 2 DXF-Belege
- **Grenzfälle/Parameter:** `"S.58: vertikal statt horizontal = bessere Ausleuchtung"`

### RW-029 — antipanik_position_diagonale
Antipanik-Position konstruieren über die Bereichs-Diagonale (Mauerkante→Gangecke) bzw. fluchtend in EINER Achse mit der nächsten Richtungs-Notleuchte UND mittig zum Bereich (gelbe Hilfslinien).
- **Position:** Schnitt/Mitte der Bereichs-Diagonale; Achse durch die nächste Fluchtweg-Leuchte
- **Leuchtentyp:** antipanik
- **PDF:** S.59,67
- **DXF-Belege (7):** 1C706 (WHA_MOL_2KG) · 1C83E (WHA_MOL_2KG) · 1D06F (WHA_MOL_2KG) · 1C8CC (WHA_MOL_2KG) … +3
- **Häufigkeit:** 2 PDF-Seiten, 7 DXF-Belege

### RW-030 — antipanik_kann_fall
Optionale Antipanik zur Lux-Stützung: auch ohne Sichtblockade zulässig ('nicht zwingend, aber sinnvoll') — Kann-Fall zusätzlich zu NB-R10; Bestätigung durch Lichtberechnung.
- **Leuchtentyp:** antipanik
- **PDF:** S.59
- **DXF-Belege (2):** 1C706 (WHA_MOL_2KG) · 1C83E (WHA_MOL_2KG)
- **Häufigkeit:** 1 PDF-Seiten, 2 DXF-Belege

### RW-031 — geraete_wahl_geschoss
Geräte-Wahl nach Geschoss: Antipanikleuchten meist in Untergeschossen, runde Aufheller meist EG–OG; Antipanik auch im EG bei Allgemeinräumen (Technik/KIWA/Spielraum/Fahrradraum). Endgültige Wahl bestätigt die Lichtberechnung.
- **Leuchtentyp:** antipanik|aufheller
- **PDF:** S.49
- **DXF-Belege (1):** 1BE99 (WHA_MOL_1KG)
- **Häufigkeit:** 1 PDF-Seiten, 1 DXF-Belege

### RW-032 — stiegen_leuchte_decke_alternative
Deckenmontage mittig bei der Stiege ist zulässige Alternative zur Wandmontage (Regelfall NB-R14), solange die Frontal-Regel erfüllt bleibt; Alternativ-Position konstruierbar als Schnitt Mittellinie-Stiege × Mittellinie-Gang.
- **Position:** Schnittpunkt der Mittellinien Stiege × Gang
- **Leuchtentyp:** notlicht_ks_stiege_links|_rechts
- **PDF:** S.42,44
- **DXF-Belege (3):** 1BEE4 (WHA_MOL_1KG) · 1BCBB (WHA_MOL_1KG) · 1BE99 (WHA_MOL_1KG)
- **Häufigkeit:** 2 PDF-Seiten, 3 DXF-Belege

### RW-033 — og_sichtketten_ausnahme
OG-Ausnahme: In Obergeschoßen mit nur EINEM Stiegenhaus und einem eindeutig verlaufenden I-förmigen Gang wird meist keine zusätzliche Richtungsleuchte benötigt — Richtungs-RZ konzentrieren sich auf EG/UG.
- **Leuchtentyp:** -
- **PDF:** S.74
- **DXF-Belege (3):** 1C64B (WHA_MOL_2KG) · 1C885 (WHA_MOL_2KG) · 1C66F (WHA_MOL_2KG)
- **Häufigkeit:** 1 PDF-Seiten, 3 DXF-Belege

### RW-034 — lichtberechnung_qa_pflicht
QA-Prozess: JEDES bearbeitete Geschoss vollständig mit der Lichtberechnung nachprüfen, unter Einbezug ALLER platzierten Elemente (RZ, Notleuchten, Antipanik, Aufheller) — zweite Prüfstufe nach der Platzierungslogik.
- **Leuchtentyp:** -
- **PDF:** S.83
- **DXF-Belege (2):** 1C707 (WHA_MOL_2KG) · 1C9BD (WHA_MOL_2KG)
- **Häufigkeit:** 1 PDF-Seiten, 2 DXF-Belege

### RW-035 — stiegenpfeil_farbe_stiege
Erkennungs-Heuristik (Selman-Naht): Der Architekten-Stiegenhauspfeil ist in derselben Farbe/Darstellung wie die Stiege selbst gezeichnet (Mollgasse: grau); rote Pfeile in Erklärbildern sind nachträgliche Markierung, keine Plan-Semantik.
- **Leuchtentyp:** -
- **PDF:** S.5,19
- **DXF-Belege (10):** 94FE7 (WHA_MOL_1OG) · 9568B (WHA_MOL_1OG) · 94FE8 (WHA_MOL_1OG) · 956B0 (WHA_MOL_1OG) … +6
- **Häufigkeit:** 2 PDF-Seiten, 10 DXF-Belege
