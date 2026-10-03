# REGELWERK Notbeleuchtung — RIVOPLAN-Zeichenregeln

Generiert aus `REGELWERK_Notbeleuchtung.json` (`scripts/baue_regelwerk.py`)
— nicht von Hand editieren. BASIS = Mollgasse; Ergänzungsregeln nachrangig.

**35 Basis-Regeln · 31 Ergänzungsregeln (nachrangig)**

## Basis-Regeln (Mollgasse, verbindlich)

### RW-001 (aus NB-R01) — tuer_rz
Raum bindet ueber eine Tuer an den Fluchtweg an und erhaelt ein Tuer-RZ → in der Tuerachse, raumseitig hinter der Schwelle
- **Rotation:** Welt-Pfeil in den Raum = entgegen Fluchtrichtung durch die Tuer = entgegen Tuer-Oeffnungsrichtung
- **Parameter:** `{"quer_zur_tuerachse_mm": {"gemessen": [3, 35], "toleranz": 50}, "raumseitiger_versatz_mm": {"gemessen": [735, 930], "hinweis": "Gang-Trenntuer 1OG: 258 gangseitig der Wandachse"}}`
- **Leuchtentyp:** notlicht_ks_stiege_unten
- **PDF:** Mollgasse S.1,2,3,4,14,20,43,51,60,61,69,70… · AmRain S.10,89,96 · Hausfeld S.10,13,16,19,24,40,45,81 · Tomaschek S.25,27,29,31,34,39,40,43,48,49,51,52…
- **DXF-Belege:** 20240 (WHA_MOL_EG, rot 89.99) · 20286 (WHA_MOL_EG, rot 359.99) · 202A9 (WHA_MOL_EG, rot 179.99) · 202A9 (WHA_MOL_EG, rot 179.99) … +141 weitere
- **Begründung:** PDF S.1-4, 12, 14, 20 — Tuer muss bei Netzausfall auffindbar bleiben, Pfeil zeigt in den Raum

### RW-002 (aus NB-R02) — allgemeinbereiche
Raum ist Allgemeinbereich (fuer alle Bewohner zugaenglich; meist EG/UG): MUELLRAUM, FAHRRADRAUM(ABSTELLRAUM communal), KINDERWAGENRAUM, KELLERABTEIL, TECHNIK, SPIELRAUM, GESCHAEFTSLOKAL, Innenhof-Anbindung → bei der Tuer nach NB-R01; EIN RZ genuegt bei freier Sicht aus dem ganzen Raum
- **Rotation:** nach NB-R01
- **Parameter:** `{"sichtlinie_max_gemessen_mm": 9143}`
- **Leuchtentyp:** notlicht_ks_stiege_unten
- **PDF:** Mollgasse S.2,3,4,11,12,45,62
- **DXF-Belege:** 20286 (WHA_MOL_EG, rot 359.99) · 202A9 (WHA_MOL_EG, rot 179.99) · 202A9 (WHA_MOL_EG, rot 179.99) · 206E7 (WHA_MOL_EG, rot 359.99) … +9 weitere
- **Begründung:** PDF S.2-4, 11-13 — Allgemeinbereichs-Regel

### RW-003 (aus NB-R03) — haupteingang
Haupteingangs-/Hauptausgangstuer des Gebaeudes → ueber/vor der Tuer, mittig zur Tuerachse, raumseitig
- **Rotation:** Welt-Pfeil ins Rauminnere
- **Parameter:** `{"quer_mm": 26, "raumseitig_mm": {"gemessen": [375, 840]}}`
- **Leuchtentyp:** notlicht_ks_stiege_unten
- **PDF:** Mollgasse S.1,6,8 · AmRain S.15,26,32,38,51 · Hausfeld S.35
- **DXF-Belege:** 20240 (WHA_MOL_EG, rot 89.99) · 2070A (WHA_MOL_EG, rot 269.99) · 181E19 (ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.dxf, rot None) · 181BD7 (ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.dxf, rot None) … +15 weitere
- **Begründung:** PDF S.1, 6, 8, 10 — Ziel der Sichtkette beider Personenstroeme

### RW-004 (aus NB-R04) — stiegenhauspfeil
Stiegenhaus mit Architekten-Stiegenpfeil (Aufwaertsrichtung JE LAUF) → RZ so, dass Ankommende es beim Erreichen des Geschosses (Blick links/rechts) sofort sehen; je Personenstrom ggf. eigenes RZ
- **Rotation:** UG-Stroeme laufen IN Pfeilrichtung hinauf, OG/DG-Stroeme ENTGEGEN hinunter
- **Parameter:** `{"delta_bewegung_vs_pfeil_grad": {"gemessen": [168, 180]}}`
- **Leuchtentyp:** -
- **PDF:** Mollgasse S.5,6,7,8,15,21,25,26,27,28,32,38… · AmRain S.24,49,82,86,92 · Tomaschek S.17,97,131,133,134,156,193,194
- **DXF-Belege:** 202EF (WHA_MOL_EG, rot 89.99) · 20263 (WHA_MOL_EG, rot 359.99) · 20312 (WHA_MOL_EG, rot 359.71) · 20240 (WHA_MOL_EG, rot 89.99) … +59 weitere
- **Begründung:** PDF S.5-8, 15, 19, 25-28, 41

### RW-005 (aus NB-R05) — vor_der_stiege
Richtungs-RZ fuehrt auf eine Stiege bzw. empfaengt Stiegen-Ankoemmlinge → 800-1122 mm vor der Antritts-/Austrittskante, auf der Laufachse; Wandmontage als Sichtbarkeits-Alternative
- **Rotation:** Welt-Pfeil exakt in Abstiegs-/Weiterrichtung des Laufs, NIE auf eine Wand
- **Parameter:** `{"abstand_vor_kante_mm": {"gemessen": [801, 1122]}, "quer_zur_laufachse_mm": {"gemessen": [20, 130]}, "pfeil_vs_laufrichtung_grad": {"toleranz": 1.0}}`
- **Leuchtentyp:** notlicht_ks_stiege_links|_rechts (nach NB-R07)
- **PDF:** Mollgasse S.16,23,25,27,29,30,32,34,39,40,41,43… · AmRain S.11,22,28,35,42,63,64,79,86,92,93 · Hausfeld S.27,49,52,56,59,61,62,82,83 · Tomaschek S.158
- **DXF-Belege:** 94FE7 (WHA_MOL_1OG, rot 0) · 94FE8 (WHA_MOL_1OG, rot 89.83) · 95019 (WHA_MOL_1OG, rot 269.55) · 95042 (WHA_MOL_1OG, rot 180.1) … +70 weitere
- **Begründung:** PDF S.16, 25, 30 ('vor der Stiege, sonst zeigt der Pfeil zur Wand'), 39-40

### RW-006 (aus NB-R06) — pfeil_unten_geradeaus
RZ im geraden Gangverlauf bedeutet 'geradeaus weiter' → mittig im Gang (Gangachse)
- **Rotation:** Welt-Pfeil ENTGEGEN der Fluchtrichtung (Vorderseite frontal zum ankommenden Strom)
- **Parameter:** `{"neben_gangachse_mm": {"gemessen": [6, 95]}, "delta_pfeil_vs_fluss_grad": {"gemessen": [178.6, 180.0]}}`
- **Leuchtentyp:** notlicht_ks_stiege_unten
- **PDF:** Mollgasse S.16,18,22,24,25,30,33,34,38,40,43,47… · AmRain S.74 · Hausfeld S.4,8,14,17,20,22,29,38,51,58,65 · Tomaschek S.117
- **DXF-Belege:** 94FE7 (WHA_MOL_1OG, rot 0) · 94FE8 (WHA_MOL_1OG, rot 89.83) · 95019 (WHA_MOL_1OG, rot 269.55) · 95042 (WHA_MOL_1OG, rot 180.1) … +122 weitere
- **Begründung:** PDF S.18, 33-34

### RW-007 (aus NB-R07) — frontalsicht_auswahl
Auswahl links/rechts/unten fuer ein Richtungs-RZ → Symbol-Laengsachse quer zum Betrachter-Korridor
- **Rotation:** Pfeil = Fluchtrichtung AUS SICHT der Person; Person muss die Vorderseite sehen
- **Parameter:** `{"erstleuchte_sichtwinkel_zur_normalen_grad": {"gemessen": [0.3, 45.5], "falschvariante": 89}, "folgeleuchte": "nur Sichtbarkeit noetig (bis ~47.5 Grad, Seitenansicht toleriert 86-90 Grad bei Tuer-RZ am Gangende)"}`
- **Leuchtentyp:** notlicht_ks_stiege_links|_rechts|_unten
- **PDF:** Mollgasse S.6,13,15,17,22,23,25,27,29,30,31,32… · AmRain S.43,53,72,78 · Hausfeld S.7,9,25,36,37,39,48,55,72,79 · Tomaschek S.5,16,19,35,42,53,54,62,63,65,95,98…
- **DXF-Belege:** 41249 (WHA_MOL_4OG, rot 269.42) · 4121F (WHA_MOL_4OG, rot 359.87) · 41220 (WHA_MOL_4OG, rot 359.42) · 413A0 (WHA_MOL_4OG, rot 179.71) … +152 weitere
- **Begründung:** PDF S.31-37 (Vergleichsbeispiele 'Pfeil unten statt links' = Seitenansicht = falsch)

### RW-008 (aus NB-R08) — erster_blick
Verlassen jeder Wohnung / jedes Raums → eine relevante Leuchte muss direkt sichtbar sein; bei zu grosser Entfernung ZUSATZ-Leuchte dazwischen; ein RZ darf mehrere Tueren bedienen
- **Rotation:** -
- **Parameter:** `{"sichtlinien": "eine je Wohnungstuer, Start <=136 mm neben der Tuer, Laenge 882-12028 mm, 0 Wandschnitte", "mehrfachbedienung": "bis 4 Wohnungstueren je RZ (1140-4275 mm)"}`
- **Leuchtentyp:** -
- **PDF:** Mollgasse S.9,13,14,15,17,18,20,21,22,23,24,25… · AmRain S.48,87 · Hausfeld S.34,42,47,54,63,71 · Tomaschek S.10,41
- **DXF-Belege:** 95042 (WHA_MOL_1OG, rot 180.1) · 95066 (WHA_MOL_1OG, rot 90) · 95067 (WHA_MOL_1OG, rot 90) · 952E9 (WHA_MOL_1OG, rot 359.55) … +89 weitere
- **Begründung:** PDF S.14, 17-18 (Zusatz-RZ wegen Distanz), 22, 27, 29-30, 39

### RW-009 (aus NB-R09) — gang_mit_ohne_stgh_tuer
Gang muendet ins Stiegenhaus → MIT Trenntuer: Tuer-RZ an der Trenntuer (NB-R01) + 2 antipanik_leuchte auf der Gangmittellinie. OHNE Trenntuer: KEIN Tuer-RZ an der Muendung; Richtungs-RZ am Knick bzw. vor der Stiege (NB-R05)
- **Rotation:** nach NB-R01/NB-R06/NB-R07
- **Parameter:** `{"ap_teilung_12m_gang_mm": [3090, 6297, 2579], "ap_neben_fluchtlinie_mm": 55, "alternativen_nur_text": "2 Aufheller | mittiges down-RZ | down-RZ + Aufheller (Wahl nach Situation, Lux-Nachweis entscheidet)"}`
- **Leuchtentyp:** siehe Faelle
- **PDF:** Mollgasse S.14,20,21,29 · Hausfeld S.30,32
- **DXF-Belege:** 95042 (WHA_MOL_1OG, rot 180.1) · 95066 (WHA_MOL_1OG, rot 90) · 95067 (WHA_MOL_1OG, rot 90) · 9568B (WHA_MOL_1OG, rot 89.99) … +48 weitere
- **Begründung:** PDF S.14, 19, 20-21, 29

### RW-010 (aus NB-R10) — antipanik_sichtblockade
Sicht der Person auf die Notleuchte ist blockiert (L-/U-Raumform, Wand dazwischen) ODER Lux-Nachweis im Gang scheitert → im abgeschatteten Bereich (gemessen 3211 mm vor der Person); rechteckige Raeume ohne Blockade: KEINE
- **Rotation:** -
- **Parameter:** `{"lux_nachweis": "separater Nachweis (Lichtberechnung) — hier nur Flag lux_nachweis_erforderlich"}`
- **Leuchtentyp:** antipanik_leuchte
- **PDF:** Mollgasse S.2,10,11,12,50,68,82 · AmRain S.115 · Hausfeld S.44,75 · Tomaschek S.28,38,110,111,124,170,183,186
- **DXF-Belege:** 2070C (WHA_MOL_EG, rot 269.99) · 20752 (WHA_MOL_EG, rot 359.99) · 20286 (WHA_MOL_EG, rot 359.99) · 21312 (WHA_MOL_EG, rot 269.99) … +36 weitere
- **Begründung:** PDF S.2 (L-Form Muellraum), 10-12

### RW-011 (aus NB-R11) — hindernis_versatz
Sollposition kollidiert mit Hindernis (z.B. Lichtkuppel, blau markiert) → quer versetzen bis frei (gemessen 142 mm Versatz, 292 mm Zentrum->Kuppelkante)
- **Rotation:** UNVERAENDERT beibehalten
- **Leuchtentyp:** -
- **PDF:** Mollgasse S.40
- **DXF-Belege:** 20864 (WHA_MOL_DG, rot 269.71) · 2083F (WHA_MOL_DG, rot 359.42) · 206DB (WHA_MOL_DG, rot None) · 20705 (WHA_MOL_DG, rot None) … +1 weitere
- **Begründung:** PDF S.40

### RW-012 (aus NB-R12) — sichtkette_abstaende
Folge von RZ entlang des Fluchtwegs → lueckenlose Kette bis zum Ausgang; Wand-RZ mit Kante an Wandkante (15-101 mm)
- **Rotation:** -
- **Parameter:** `{"folgeabstaende_mm": {"gemessen": [1975, 7749]}, "sichtlinien_ende": "an der Symbol-KANTE, nicht am Zentrum"}`
- **Leuchtentyp:** -
- **PDF:** Mollgasse S.5,6,7,8,9,13,16,22,25,28,32,36… · AmRain S.75,87,93,96 · Hausfeld S.21 · Tomaschek S.14,80,139,203,206
- **DXF-Belege:** 202EF (WHA_MOL_EG, rot 89.99) · 20263 (WHA_MOL_EG, rot 359.99) · 20312 (WHA_MOL_EG, rot 359.71) · 20240 (WHA_MOL_EG, rot 89.99) … +81 weitere
- **Begründung:** PDF S.5-9 (EG-Ketten)

### RW-013 (aus NB-R13) — ug_stiegenrichtung
Untergeschoss: Personen fluechten HINAUF ueber die Stiege → Leuchte vor/an der Stiege (NB-R05)
- **Rotation:** Welt-Pfeil = Aufwaertsrichtung des Laufs = IN Stiegenhauspfeilrichtung (OG: entgegen, NB-R04); Frontseite zum ankommenden UG-Strom
- **Leuchtentyp:** -
- **PDF:** Mollgasse S.41,43,54,55,56,71,75,92,93
- **DXF-Belege:** 1BEE4 (WHA_MOL_1KG, rot None) · 1BCBB (WHA_MOL_1KG, rot None) · 1BCBE (WHA_MOL_1KG, rot None) · 1BE99 (WHA_MOL_1KG, rot None) … +24 weitere
- **Begründung:** PDF S.43, 54-55 — UG-Gegenstueck zu NB-R04

### RW-014 (aus NB-R14) — montageort_wand_decke
Wahl Wand- vs. Deckenmontage → Stiegen-Leuchten = Wand; Gang-Leuchten = Decke, mittig
- **Rotation:** -
- **Leuchtentyp:** -
- **PDF:** Mollgasse S.16,32,56 · AmRain S.65,68,90,94
- **DXF-Belege:** BFE20 (ARAI5_FE_XEL_ZZ_MOP_OG1_0012_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) · BFE73 (ARAI5_FE_XEL_ZZ_MOP_OG1_0012_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) · 73D9D (ARAI5_FE_XEL_ZZ_MOP_OG3_0014_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) · 73E07 (ARAI5_FE_XEL_ZZ_MOP_OG3_0014_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) … +14 weitere
- **Begründung:** PDF S.56 woertlich: Notleuchten an Waenden hauptsaechlich bei Stiegen; alle 14 1KG-Platzierungen konsistent

### RW-015 (aus NB-R15) — kabeltrasse_hindernis
Sollposition liegt auf/nahe einer Kabeltrasse (blaue Balken, KT300/KT400/KT500) → NIE auf der Trasse; seitlich versetzen, moeglichst >= 450 mm Abstand
- **Rotation:** nach Versatz erhalten: Sichtbarkeit, Pfeilrichtung, Frontseite, Fluchtwegbezug, Gebaeudehaelfte
- **Parameter:** `{"abstand_mm": {"soll_min": 450, "modalitaet": "moeglichst (Fachpraxis-SOLL)"}, "versatz_gemessen_mm": [507]}`
- **Leuchtentyp:** -
- **PDF:** Mollgasse S.63,64,65,79,81,84,85,88
- **DXF-Belege:** 1C7CB (WHA_MOL_2KG, rot None) · 1C8A9 (WHA_MOL_2KG, rot None) · 1C7CC (WHA_MOL_2KG, rot None) · 1C695 (WHA_MOL_2KG, rot None) … +11 weitere
- **Begründung:** PDF S.63-64 woertlich; 2KG (A)-Ana 1C7D0 bleibt trotz Versatz auf der Anastasius-Seite. ACHTUNG: Rigole (Bodenrinnen-Schraffuren) sind KEINE Kabeltrassen

### RW-016 (aus NB-R16) — beidseitig
ZWEI Personenstroeme aus Gegenrichtungen nutzen denselben Fluchtweg-Knoten und brauchen beide die Frontseite → am gemeinsamen Knoten (GT: 2 gespiegelte Einzel-Bloecke, Abstand 264-318 mm; Engine: RIVO_NL_ARR_bothsided)
- **Rotation:** Achse = Fluchtweg-Achse beider Stroeme
- **Parameter:** `{"alternative": "beidseitig am Richtungswechsel OHNE Gegenstrom = NUR-ALTERNATIVE (orange, 'muss nicht sein') — NICHT automatisieren"}`
- **Leuchtentyp:** notlicht_ks_beidseitig
- **PDF:** Mollgasse S.52,65,66,67,68,69,70,71,72,73,74,75… · AmRain S.16,17,25,27,33,34,40,41,47,50,66,81… · Hausfeld S.23,31 · Tomaschek S.18,20,44,45,46,57,59,74,76,77,78,82…
- **DXF-Belege:** 181E37 (ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.dxf, rot None) · 181E55 (ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.dxf, rot None) · 181BB9 (ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.dxf, rot None) · 181BF5 (ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.dxf, rot None) … +95 weitere
- **Begründung:** PDF S.65-83; Pflicht-Paare 2KG Gr.1-5 + 1KG (I) + EG-Paar; Gr.6 = einzige Alternative

### RW-017 (aus NB-R17) — garage_durchquerbarkeit
Fluchtwegfuehrung durch Garagenbereiche → Motorrad-Stellflaechen sind durchquerbar; Doppelparker-/PKW-Flaechen und Gruben NICHT
- **Rotation:** -
- **Leuchtentyp:** -
- **PDF:** Mollgasse S.65,66,67,68,69,70,84,86,87 · AmRain S.101
- **DXF-Belege:** 32744 (ARAI5_FE_XEL_ZZ_MOP_OG4_0015_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) · 1C7CB (WHA_MOL_2KG, rot None) · 1C8A9 (WHA_MOL_2KG, rot None) · 1C7CC (WHA_MOL_2KG, rot None) … +14 weitere
- **Begründung:** PDF S.65-70; Personenreihe 1CBF6-1CBFC durch MOTORRAD-Stempel, 0 Fluchtwege durch DOPPELPARKER-Zonen. Durchquerbarkeit folgt aus freier Geometrie, nicht aus dem Raumlabel

### RW-018 (aus NB-R18) — gebaeudehaelften
Projekt besteht aus zwei zusammengebauten Gebaeuden → Trennung entlang der weitergefuehrten Gebaeudewand; Zuordnung am EG-Grundriss verifizieren; je Haelfte eigene Fluchtwege/Ausgaenge/Label-Alphabete
- **Rotation:** -
- **Parameter:** `{"prozessregel": "unklare Zuordnung NIEMALS raten -> offene Frage (PDF S.78, bindend)"}`
- **Leuchtentyp:** -
- **PDF:** Mollgasse S.76,77,78,79,80,81,82,83 · AmRain S.116
- **DXF-Belege:** 1291E8 (ARAI5_FE_XEL_ZZ_MOP_UG_0010_V_02_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) · 1C64B (WHA_MOL_2KG, rot None) · 1C885 (WHA_MOL_2KG, rot None) · 1C66F (WHA_MOL_2KG, rot None) … +8 weitere
- **Begründung:** PDF S.76-83; rote Trennlinie 1C7F4 (116 m) auf der Mollgasse-Gebaeudewand

### RW-019 (aus NB-R19) — ug_nebenraum_tuerleuchte
UG-Nebenraum bindet an den Gang an → TECHNIK/NIEDERSPANNUNG/E-Raum: Tuer-Leuchte nach NB-R01 (mittig 3-26 mm, 711-779 mm zugangsseitig). Einzelne kleine ER/KELLERABTEIL/Medienraum: KEINE eigene Tuerleuchte, wenn nach Tuerdurchtritt sofort ein Gang-RZ sichtbar ist
- **Rotation:** nach NB-R01
- **Leuchtentyp:** notlicht_ks_stiege_unten
- **PDF:** Mollgasse S.45,47,51,52,53,71,72,73,85,90,91,93 · Hausfeld S.11,28,80 · Tomaschek S.32,36,37,60,174,176
- **DXF-Belege:** 6018E (Hausfeldstraße_UG, rot None) · 6012E (Hausfeldstraße_UG, rot None) · 6014E (Hausfeldstraße_UG, rot None) · 60210 (Hausfeldstraße_UG, rot None) … +69 weitere
- **Begründung:** PDF S.51-53, 71-73, 93; 1KG-09 (D) + Merktext 'Stromversorgung aller Notleuchten'

### RW-020 (aus NB-R20) — tuerlose_gaenge_durchgaenge
tuerloser Gang / offener Durchgang im Fluchtweg → tuerloser zusammenhaengender Gang: KEINE Zwischen-RZ solange Sichtkette steht; kurzer Gang mit Direktsicht aller Tueren: genau EIN Tuer-RZ; offener Durchgang als Knoten: down-Typ MITTIG im Durchgang (gemessen 4 mm Mittigkeit bei 1250 mm)
- **Rotation:** down-Typ frontal zum ankommenden Strom (rechts/links/beidseitig am Durchgang im PDF explizit VERWORFEN)
- **Leuchtentyp:** notlicht_ks_stiege_unten
- **PDF:** Mollgasse S.58,59,60,61,62,73,74,90,91 · AmRain S.18
- **DXF-Belege:** 181E73 (ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.dxf, rot None) · 1C695 (WHA_MOL_2KG, rot None) · 1C7D0 (WHA_MOL_2KG, rot None) · 1C707 (WHA_MOL_2KG, rot None) … +5 weitere
- **Begründung:** PDF S.58-62, 73-74, 90-91 — S.73-74 sind dokumentierte Negativ-Beispiele

### RW-021 (aus NB-R21) — sv_anlage
Projekt braucht Notbeleuchtungs-Stromversorgung → EIN System je Projekt ('meistens' auch bei zwei Gebaeudehaelften), Verteiler im Niederspannungsraum, NICHT an der E-Verteiler-Wand
- **Rotation:** -
- **Leuchtentyp:** gruppenbatterie_anlage
- **PDF:** Mollgasse S.51,71,72
- **DXF-Belege:** 1BE99 (WHA_MOL_1KG, rot None) · 1BCBE (WHA_MOL_1KG, rot None) · 1C695 (WHA_MOL_2KG, rot None) · 1C7D0 (WHA_MOL_2KG, rot None) … +15 weitere
- **Begründung:** PDF S.51, 71-72; 1KG 1CB68, 2KG 1D10E/1D10F

### RW-022 (aus NB-R22) — quellen_disziplin_fluchtplan
Quelle ist ein Flucht-/Rettungsplan (gruener Aushang), kein Notbeleuchtungsplan → belegt NUR Fluchtweg-Richtung/Tueren/Stiegenhaeuser/Ausgaenge; NICHT Leuchtenposition, Wand-/Deckenmontage, Frontseite, ein-/beidseitig, Typ, Hoehe, Lux, Anzahl
- **Rotation:** Blatt-Richtung != CAD-Richtung != Personen-Richtung; gedrehte Aushang-Blaetter
- **Parameter:** `{"standort_marke": "Aushang-Bezugspunkt, KEINE Leuchte", "mehrere_blaetter": "gleiches Geschoss aus mehreren Aushaengen = EINE Referenz", "raum_ohne_gruen": "bedeutet NICHT 'keine Notbeleuchtung noetig'"}`
- **Leuchtentyp:** -
- **PDF:** Mollgasse S.1,2,3,4,5,6,7,8,9,10 · Hausfeld S.74 · Tomaschek S.7,83,209
- **DXF-Belege:** 36C36 (SG_RIVO_Erklaerung.dxf, rot None) · 36C52 (SG_RIVO_Erklaerung.dxf, rot None)
- **Begründung:** TOMA S.1-10; Owner-Auftrag Quellen-Trennung A/B/C/D

### RW-023 (aus NB-R23) — schul_bildungscluster_fluchtweg
Schule, Cluster-/offene-Lernlandschaft-Typologie → offener 'Kommunikations- und Bewegungsbereich' traegt den Fluchtweg; Unterrichtsraeume oeffnen direkt darauf, OHNE 'Gang'-Label
- **Rotation:** -
- **Leuchtentyp:** -
- **PDF:** Tomaschek S.109,130,168,199
- **DXF-Belege:** 20796 (EG_RIVO_Erklaerung.dxf, rot None) · 49F16 (EG_RIVO_Erklaerung.dxf, rot None) · 1B6CF (OG_RIVO_Erklaerung.dxf, rot None)
- **Begründung:** TOMA OG-04: Unterrichtsraum 1-4 -> Kommunikations-/Bewegungsbereich -> TH 2. Generalisiert NB-R20 auf Cluster-Ebene

### RW-024 (aus NB-R24) — mehrere_stiegenhaeuser_gerichtet
Gebaeude mit mehreren Fluchtstiegenhaeusern (TOMA: TH 2/3/4) → Cluster/Gebaeudeteile GEZIELT verschiedenen THs zuordnen; NICHT alle zum naechstgelegenen TH / einem Hauptausgang; mehrere dargestellte Richtungen erhalten
- **Rotation:** -
- **Leuchtentyp:** -
- **PDF:** Tomaschek S.143
- **DXF-Belege:** 2082F (EG_RIVO_Erklaerung.dxf, rot None) · 2084D (EG_RIVO_Erklaerung.dxf, rot None)
- **Begründung:** TOMA SG/EG/OG; = Variante der Mollgasse-Gebaeudehaelften NB-R18 (unklar -> nicht raten)

### RW-025 (aus NB-R25) — egress_je_ebene_zieltypen
Sockel-/Untergeschoss und Ziel-Typ-Bestimmung → Sockel-/UG kann direkte Aussenausgaenge auf eigener Ebene haben (Flucht nicht zwingend ueber EG). Ziel-Typen NIE gleichsetzen: Fluchtstiegenhaus / Ausgang ins Freie / Balkon-Terrasse-Loggia / vorlaeufige Evakuierungsstelle / Sammelstelle
- **Rotation:** -
- **Leuchtentyp:** -
- **PDF:** AmRain S.58,69,84,85,91,98,100,102 · Hausfeld S.78 · Tomaschek S.22,79,205
- **DXF-Belege:** 73D2C (ARAI5_FE_XEL_ZZ_MOP_OG3_0014_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) · 73D4A (ARAI5_FE_XEL_ZZ_MOP_OG3_0014_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) · 73D68 (ARAI5_FE_XEL_ZZ_MOP_OG3_0014_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) · 73D7F (ARAI5_FE_XEL_ZZ_MOP_OG3_0014_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) … +15 weitere
- **Begründung:** TOMA SG: viele EN-Tueren ins Freie auf Sockel-Ebene. Ergaenzt NB-R13

### RW-026 (aus NB-R26) — ausfuehrungsplan_annotationen_anker
Architektur-Ausfuehrungsplan mit Brandschutz-/Flucht-Textannotation → EN 1125 (Panikstange) / EN 179 (Notausgangsbeschlag) = Ausgangstueren; FLn = Fluchtweg-Flaeche mit Soll-m2; EI 30/90/230-C + 'brandlastfreie Zone' + BA = Brandabschnitte; RWA = Rauchabzug; BMZ = Brandmeldezentrale
- **Rotation:** -
- **Parameter:** `{"daten_fallen": "INSUNITS kann luegen (TOMA=6 Meter, real mm -> ueber Tuerbreiten/Wandstaerken verifizieren); Riesen-Koordinaten-Offset moeglich (TOMA SG ~-1.7e9 -> Healthcheck/Nullung vor Engine-Lauf)", "messwerte_mm": {"toma_eg_fl": [72, 72, 33, 39], "toma_og_fl": [48]}}`
- **Leuchtentyp:** -
- **PDF:** Hausfeld S.5
- **Begründung:** TOMA SG/EG/OG: EN/FL/EI/RWA/BMZ als Textannotation mit Koordinaten (inventar_*.json)

### RW-027 (aus NB-R27) — aufzug_keine_fluchtverbindung
Aufzug im Gebaeude → Aufzug NIE als vertikale Flucht-Kante; Aufzugsvorbereich getrennt (kann Teil des Gangs sein)
- **Rotation:** -
- **Leuchtentyp:** -
- **PDF:** Hausfeld S.26 · Tomaschek S.96,204
- **DXF-Belege:** 6012E (Hausfeldstraße_UG, rot None) · 6014E (Hausfeldstraße_UG, rot None) · 6018E (Hausfeldstraße_UG, rot None) · 60210 (Hausfeldstraße_UG, rot None) … +36 weitere
- **Begründung:** TOMA Brandfall-Hinweis 'Aufzug nicht benutzen'; deckt sich mit fachpraxis.entferne_schacht_leuchten

### RW-028 — antipanik_laengsachse
Antipanikleuchte: Längsachse in Richtung des auszuleuchtenden (Gang-)Bereichs drehen; Position mittig im abgeschatteten Bereich.
- **Rotation:** Längsachse parallel zur Hauptachse des Zielbereichs
- **Leuchtentyp:** antipanik
- **PDF:** Mollgasse S.58
- **DXF-Belege:** 1C707 (WHA_MOL_2KG, rot None) · 1C9BD (WHA_MOL_2KG, rot None)

### RW-029 — antipanik_position_diagonale
Antipanik-Position konstruieren über die Bereichs-Diagonale (Mauerkante→Gangecke) bzw. fluchtend in EINER Achse mit der nächsten Richtungs-Notleuchte UND mittig zum Bereich (gelbe Hilfslinien).
- **Leuchtentyp:** antipanik
- **PDF:** Mollgasse S.59,67
- **DXF-Belege:** 1C706 (WHA_MOL_2KG, rot None) · 1C83E (WHA_MOL_2KG, rot None) · 1D06F (WHA_MOL_2KG, rot None) · 1C8CC (WHA_MOL_2KG, rot None) … +3 weitere

### RW-030 — antipanik_kann_fall
Optionale Antipanik zur Lux-Stützung: auch ohne Sichtblockade zulässig ('nicht zwingend, aber sinnvoll') — Kann-Fall zusätzlich zu NB-R10; Bestätigung durch Lichtberechnung.
- **Leuchtentyp:** antipanik
- **PDF:** Mollgasse S.59
- **DXF-Belege:** 1C706 (WHA_MOL_2KG, rot None) · 1C83E (WHA_MOL_2KG, rot None)

### RW-031 — geraete_wahl_geschoss
Geräte-Wahl nach Geschoss: Antipanikleuchten meist in Untergeschossen, runde Aufheller meist EG–OG; Antipanik auch im EG bei Allgemeinräumen (Technik/KIWA/Spielraum/Fahrradraum). Endgültige Wahl bestätigt die Lichtberechnung.
- **Leuchtentyp:** antipanik|aufheller
- **PDF:** Mollgasse S.49
- **DXF-Belege:** 1BE99 (WHA_MOL_1KG, rot None)

### RW-032 — stiegen_leuchte_decke_alternative
Deckenmontage mittig bei der Stiege ist zulässige Alternative zur Wandmontage (Regelfall NB-R14), solange die Frontal-Regel erfüllt bleibt; Alternativ-Position konstruierbar als Schnitt Mittellinie-Stiege × Mittellinie-Gang.
- **Leuchtentyp:** notlicht_ks_stiege_links|_rechts
- **PDF:** Mollgasse S.42,44
- **DXF-Belege:** 1BEE4 (WHA_MOL_1KG, rot None) · 1BCBB (WHA_MOL_1KG, rot None) · 1BE99 (WHA_MOL_1KG, rot None)

### RW-033 — og_sichtketten_ausnahme
OG-Ausnahme: In Obergeschoßen mit nur EINEM Stiegenhaus und einem eindeutig verlaufenden I-förmigen Gang wird meist keine zusätzliche Richtungsleuchte benötigt — Richtungs-RZ konzentrieren sich auf EG/UG.
- **Leuchtentyp:** -
- **PDF:** Mollgasse S.74
- **DXF-Belege:** 1C64B (WHA_MOL_2KG, rot None) · 1C885 (WHA_MOL_2KG, rot None) · 1C66F (WHA_MOL_2KG, rot None)

### RW-034 — lichtberechnung_qa_pflicht
QA-Prozess: JEDES bearbeitete Geschoss vollständig mit der Lichtberechnung nachprüfen, unter Einbezug ALLER platzierten Elemente (RZ, Notleuchten, Antipanik, Aufheller) — zweite Prüfstufe nach der Platzierungslogik.
- **Leuchtentyp:** -
- **PDF:** Mollgasse S.83
- **DXF-Belege:** 1C707 (WHA_MOL_2KG, rot None) · 1C9BD (WHA_MOL_2KG, rot None)

### RW-035 — stiegenpfeil_farbe_stiege
Erkennungs-Heuristik (Selman-Naht): Der Architekten-Stiegenhauspfeil ist in derselben Farbe/Darstellung wie die Stiege selbst gezeichnet (Mollgasse: grau); rote Pfeile in Erklärbildern sind nachträgliche Markierung, keine Plan-Semantik.
- **Leuchtentyp:** -
- **PDF:** Mollgasse S.5,19
- **DXF-Belege:** 94FE7 (WHA_MOL_1OG, rot None) · 9568B (WHA_MOL_1OG, rot None) · 94FE8 (WHA_MOL_1OG, rot None) · 956B0 (WHA_MOL_1OG, rot None) … +6 weitere

## Ergänzungsregeln (nachrangig — greifen nur, wenn keine Basis-Regel greift)

### RW-101 — knick_rz_stiegenlauf
Bei Richtungswechsel INNERHALB eines Stiegenlaufs (Zwischenpodest/abknickender Lauf) ein eigenes Richtungs-RZ am Knick zusätzlich zum Antritts-RZ (NB-R05); Pfeil = weitere Laufrichtung.
- **Rotation:** Welt-Pfeil = Richtung des weiterführenden Laufs
- **Leuchtentyp:** notlicht_ks_stiege_links|_rechts
- **PDF:** Hausfeld S.50,57
- **DXF-Belege:** 130B7 (Hausfeldstraße_1OG, rot None) · 13037 (Hausfeldstraße_1OG, rot None) · 13057 (Hausfeldstraße_1OG, rot None) · 13017 (Hausfeldstraße_1OG, rot None) … +8 weitere

### RW-102 — aufheller_stgh_vorbereich_knoten
Treffen im Stiegenhaus-Vorbereich Schleusen-/Gangzugang, Liftzugang und Weg zum Stiegenfuß zusammen, wird dort zusätzlich zu Tür-/Richtungs-RZ EIN runder Aufheller gesetzt (Knoten-Beleuchtung).
- **Leuchtentyp:** aufheller
- **PDF:** Hausfeld S.12
- **DXF-Belege:** 601EE (Hausfeldstraße_UG, rot None) · 6020E (Hausfeldstraße_UG, rot None)

### RW-103 — aussen_leuchte_letzter_ausgang
Unmittelbar AUSSEN vor dem letzten Ausgang eine beleuchtende Position (Antipanik-/SL-Typ, KEINE RZ-Front, keine Richtungsinfo) für Austritt + angrenzende Bodenfläche (EN 1838 §4.1.2 g); getrennt von Fassadenleuchten.
- **Leuchtentyp:** antipanik|sicherheitsleuchte
- **PDF:** Hausfeld S.41 · Tomaschek S.47 · AmRain S.12,31
- **DXF-Belege:** 9EE28 (Hausfeldstraße_EG, rot None) · 9ED64 (Hausfeldstraße_EG, rot None) · 9EDC4 (Hausfeldstraße_EG, rot None) · 9EE08 (Hausfeldstraße_EG, rot None) … +7 weitere

### RW-104 — schulraum_muster
Schule: JEDER Unterrichts-/Bildungsraum erhält ein raumseitiges Tür-RZ (nach NB-R01, Front in den Raum) PLUS genau einen Aufheller/AP im Rauminneren; der Wohnbau-Skip (WOHNUNG_PRIVAT ohne Notlicht) gilt für Klassenräume NICHT. Aufheller wirkt nur im eigenen Raum.
- **Leuchtentyp:** rz + aufheller|antipanik
- **PDF:** Tomaschek S.87,90,101,114,146,159
- **DXF-Belege:** 20982 (EG_RIVO_Erklaerung.dxf, rot None) · 20596 (EG_RIVO_Erklaerung.dxf, rot None) · 20742 (EG_RIVO_Erklaerung.dxf, rot None) · 20578 (EG_RIVO_Erklaerung.dxf, rot None) … +6 weitere

### RW-105 — beidseitig_reihe_quer_ankuenfte
Eine REIHE beidseitiger RZ längs des Gangs bedient seitliche Raum-Ankünfte (Fronten quer zum Gang); lückenlose Frontalsicht für Längsläufer wird nicht gefordert — nuanciert NB-R07/NB-R16.
- **Leuchtentyp:** rz beidseitig
- **PDF:** Tomaschek S.75
- **DXF-Belege:** 34FD6 (SG_RIVO_Erklaerung.dxf, rot None) · 34FF4 (SG_RIVO_Erklaerung.dxf, rot None) · 35012 (SG_RIVO_Erklaerung.dxf, rot None) · 35030 (SG_RIVO_Erklaerung.dxf, rot None) … +1 weitere

### RW-106 — knoten_einseitig_plus_beidseitig
Knoten mit drei Ankunftsrichtungen: Kombination aus einseitigem RZ (frontal zur Längsankunft) und beidseitigem RZ (Fronten zu Querankünften) am SELBEN Knoten ist regulär — dicht benachbarte Zeichen funktional analysieren, nie als Dublette löschen.
- **Leuchtentyp:** rz
- **PDF:** Tomaschek S.115
- **DXF-Belege:** 207B0 (EG_RIVO_Erklaerung.dxf, rot None) · 209D4 (EG_RIVO_Erklaerung.dxf, rot None)

### RW-107 — antipanik_flaechenbezogen
Offene Cluster-/MFU-/Saal-Flächen: Antipanik FLÄCHENBEZOGEN bewerten (freie Boden-Kernfläche nach EN 1838 4.3, 0,5-m-Randstreifen ausgenommen), nicht nur Weg unter der Leuchte; Großraum/Saal erhält flächige AP unabhängig von Sichtblockade.
- **Leuchtentyp:** antipanik
- **PDF:** Tomaschek S.64,169
- **DXF-Belege:** 3552F (SG_RIVO_Erklaerung.dxf, rot None) · 3554A (SG_RIVO_Erklaerung.dxf, rot None) · 1B6CF (OG_RIVO_Erklaerung.dxf, rot None)

### RW-108 — barrierefrei_wc_antipanik
Barrierefreies WC benötigt Antipanikbeleuchtung nach EN 1838 4.3.8 — eigener Trigger unabhängig von Sichtblockade und Fläche (keine 8-m²-/60-m²-Pauschale); nur echte Behinderten-Toiletten.
- **Leuchtentyp:** antipanik
- **PDF:** Tomaschek S.58,120,182
- **DXF-Belege:** 34F6E (SG_RIVO_Erklaerung.dxf, rot None) · 34F50 (SG_RIVO_Erklaerung.dxf, rot None) · 34E01 (SG_RIVO_Erklaerung.dxf, rot None) · 34DE7 (SG_RIVO_Erklaerung.dxf, rot None) … +3 weitere

### RW-109 — sanitaer_schwellen
OVE E 8101 718.560.9.001.AT: Sanitärbereiche ≥8 m² nur bei ERHÖHTEN Anforderungen prüfen; die 60-m²-Ziffer gilt NUR für verkehrstechnische Einrichtungen — keine Schul-/Sanitär-Pauschale (Enis-Lane: Schwellenwerte in normwissen).
- **Leuchtentyp:** -
- **PDF:** Tomaschek S.103,123
- **DXF-Belege:** 49EFB (EG_RIVO_Erklaerung.dxf, rot None) · 49EFC (EG_RIVO_Erklaerung.dxf, rot None) · 49F00 (EG_RIVO_Erklaerung.dxf, rot None) · 49F01 (EG_RIVO_Erklaerung.dxf, rot None) … +1 weitere

### RW-110 — mehrstufige_tuerfolgen
Mehrstufige Raum-/Türfolge (Raum→Raum→Gang): jede Tür der Folge erhält ihr eigenes Tür-RZ mit eigener Front; ein Aufheller im Zwischenraum ersetzt kein Tür-RZ; EN 1838 4.3.9 macht den Zwischenweg zum beleuchteten Rettungsweg.
- **Leuchtentyp:** rz
- **PDF:** Tomaschek S.50,140
- **DXF-Belege:** 34E79 (SG_RIVO_Erklaerung.dxf, rot None) · 34E97 (SG_RIVO_Erklaerung.dxf, rot None) · 34E1F (SG_RIVO_Erklaerung.dxf, rot None) · 209B6 (EG_RIVO_Erklaerung.dxf, rot None) … +3 weitere

### RW-111 — gang_aufheller_mehrfachbedienung
Ein gemeinsamer Gang-Aufheller darf mehrere benachbarte Türvorbereiche bedienen (SL-Analogie zu NB-R08); er deckt aber NIE Innenräume hinter Wänden/Kabinentrennungen und trägt keine Richtungsinformation.
- **Leuchtentyp:** aufheller
- **PDF:** Tomaschek S.126,185
- **DXF-Belege:** 49F0B (EG_RIVO_Erklaerung.dxf, rot None)

### RW-112 — gefaehrdung_nur_beurteilung
Werk-/Küchenbereiche: Sicherheitsbeleuchtung für besondere Gefährdung (EN 1838 4.4: ≥10 % Wartungswert, ≥15 lx, Uo≥0,1, 0,5 s) NUR über Gefährdungsbeurteilung auslösen — nie automatisch aus dem Raumnamen.
- **Leuchtentyp:** -
- **PDF:** Tomaschek S.30,128,190
- **DXF-Belege:** 34C50 (SG_RIVO_Erklaerung.dxf, rot None) · 34C6E (SG_RIVO_Erklaerung.dxf, rot None) · 49F14 (EG_RIVO_Erklaerung.dxf, rot None) · 49F15 (EG_RIVO_Erklaerung.dxf, rot None) … +1 weitere

### RW-113 — schraeg_rotation_exakt
Rotation an schrägen Wänden/Bestand exakt erhalten: krumme Winkel (96°, 269.007°, 7°/97°/187°/277°-Familie) NIE auf 90°-Raster runden — kleine Winkelabweichungen tragen realen Gebäudebezug.
- **Rotation:** exakter Wand-/Bestandswinkel, kein Quantisieren
- **Leuchtentyp:** rz
- **PDF:** Tomaschek S.99,200,220
- **DXF-Belege:** 43561 (EG_RIVO_Erklaerung.dxf, rot 269.01) · 1B563 (OG_RIVO_Erklaerung.dxf, rot 96.0) · 34FD6 (SG_RIVO_Erklaerung.dxf, rot 97.0)

### RW-114 — rz_ersetzt_keine_stufen_sl
Eine RZ-Kette an einer Stiege deckt NICHT die Beleuchtungsaufgabe der Stufen (EN 1838 4.1.2 b); fehlende Stiegen-SL ist als offener Beleuchtungsnachweis auszuweisen, nicht durch RZ-Anrechnung zu heilen.
- **Leuchtentyp:** -
- **PDF:** Tomaschek S.157
- **DXF-Belege:** 1B3FD (OG_RIVO_Erklaerung.dxf, rot None) · 1B41A (OG_RIVO_Erklaerung.dxf, rot None)

### RW-115 — absturzsicherung_wegbarriere
Absturzsicherungen/Brüstungskanten sind beim Fluchtweg-Routing Wegbarrieren (Weg nie über die Schutzkante führen) — erweitert den Hindernisbegriff über Symbol-Kollision hinaus (Selman-Naht).
- **Leuchtentyp:** -
- **PDF:** AmRain S.61
- **DXF-Belege:** BFDAF (ARAI5_FE_XEL_ZZ_MOP_OG1_0012_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None)

### RW-116 — rampe_kein_automatischer_fluchtweg
Garagen-/Fahrradrampe ist NICHT automatisch Fluchtweg oder sicherer Außenort: aus Rampengefälle keine Fluchtrichtung ableiten; erst nach belegter begehbarer Öffnung + Passage als Weg werten.
- **Leuchtentyp:** -
- **PDF:** Hausfeld S.18 · AmRain S.109
- **DXF-Belege:** 600EE (Hausfeldstraße_UG, rot None) · 6016E (Hausfeldstraße_UG, rot None) · 601EE (Hausfeldstraße_UG, rot None) · 601AE (Hausfeldstraße_UG, rot None) … +18 weitere

### RW-117 — rz_instanzen_kein_merge
Benachbarte RZ-Instanzen (z.B. am STGH-Knoten) sind eigenständige Geräte: kein Merge, kein Löschen, getrennte Handles/Belege je Instanz — der Engine-SL<2m-Merge betrifft NUR Sicherheitsleuchten.
- **Leuchtentyp:** rz
- **PDF:** AmRain S.67
- **DXF-Belege:** BFE55 (ARAI5_FE_XEL_ZZ_MOP_OG1_0012_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None)

### RW-118 — geschoss_individualitaet
Geschoss-Konfigurationen NIE kopieren: dieselbe Grundriss-Stelle kann je Geschoss anderen Zeichentyp brauchen; vertikale Stiegenkern-Zuordnung nur über Stiegenbezeichnung+Lauf-/Liftkonfiguration+Schnittmarken/Höhen, nie über Koordinaten-Ähnlichkeit.
- **Leuchtentyp:** -
- **PDF:** AmRain S.71 · Tomaschek S.153 · Hausfeld S.64
- **DXF-Belege:** 9C724 (ARAI5_FE_XEL_ZZ_MOP_OG2_0013_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) · 1B737 (OG_RIVO_Erklaerung.dxf, rot None) · 1B4AF (OG_RIVO_Erklaerung.dxf, rot None) · 1B491 (OG_RIVO_Erklaerung.dxf, rot None)

### RW-119 — leuchten_kennzeichnung_ove
Jede Sicherheitsleuchte trägt sichtbar Verteiler-, Stromkreis- und Leuchtennummer an/nahe der Leuchte (OVE E 8101:2025-10 560.9.15) — deckt die Engine-Praxis der circuit_hint-/NODEID-Labels.
- **Leuchtentyp:** -
- **PDF:** Hausfeld S.73

### RW-120 — bestandsform_symbol_zuordnung
AG-CAD-Formregel Bestandskonvertierung: runde/quadratische Bestandsleuchten mit Mittelkreis → Aufheller-Symbol; rechteckige → Antipanik-Symbol. Reine Zeichensprache OHNE Lichtnachweis; Produktfunktion bleibt Attribut (Rolle ≠ Produkt).
- **Leuchtentyp:** aufheller|antipanik
- **PDF:** Tomaschek S.6,21,84 · Hausfeld S.15
- **DXF-Belege:** 8C384 (SG_RIVO_Erklaerung.dxf, rot None) · 36C36 (SG_RIVO_Erklaerung.dxf, rot None) · 36C52 (SG_RIVO_Erklaerung.dxf, rot None) · 6012E (Hausfeldstraße_UG, rot None) … +24 weitere

### RW-121 — rotationserhalt_bestand
Beim Symboltausch Bestand→RIVO Position/Kennung/Rotation/Skalierung EXAKT übernehmen (auch 269.007° oder 0.482583); die alte Leuchtenachse ist Dokumentation, NIE Fluchtrichtungs- oder Photometrie-Aussage.
- **Rotation:** Zieldrehung = Bestandsdrehung, keine Normalisierung
- **Leuchtentyp:** -
- **PDF:** Tomaschek S.23,99,220 · AmRain S.60
- **DXF-Belege:** 8C399 (SG_RIVO_Erklaerung.dxf, rot None) · BFD91 (ARAI5_FE_XEL_ZZ_MOP_OG1_0012_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None)

### RW-122 — attribut_grafik_widerspruch
Attribut/Grafik-Widerspruch (Produkttext vs. Symbolgrafik): Grafik-Rolle beibehalten, Widerspruch sichtbar als offenen Prüfpunkt führen — kein automatischer Symboltausch.
- **Leuchtentyp:** -
- **PDF:** Tomaschek S.136
- **DXF-Belege:** 208A0 (EG_RIVO_Erklaerung.dxf, rot None) · 2064B (EG_RIVO_Erklaerung.dxf, rot None)

### RW-123 — rolle_nicht_produkt_sl
SL-Bestand: 'AP'/'SL' im Produktnamen belegt keine Funktion; SL-Symbol ohne Pfeil trägt KEINE Richtungsinformation und ersetzt kein RZ; Funktionszuordnung (Wegbeleuchtung/Antipanik/Aufheller) braucht je Stelle eigenen Nachweis (EN 1838 4.1.2/4.3.1).
- **Leuchtentyp:** -
- **PDF:** AmRain S.14,44,62 · Tomaschek S.78
- **DXF-Belege:** 181D69 (ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.dxf, rot None) · BFDCD (ARAI5_FE_XEL_ZZ_MOP_OG1_0012_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) · 35012 (SG_RIVO_Erklaerung.dxf, rot None)

### RW-124 — quellen_disziplin_plananker
Architektur-Text (EINGANG/Adresse/SCHLEUSE/Türmarken) ist Plananker, KEIN Funktionsbeleg: keine Notausgangs-, Tür- oder Wegzuordnung aus Textnähe; Verbindungen nie aus Symbolnähe ableiten — Wand-/Türfolge muss geometrisch bestätigt sein.
- **Leuchtentyp:** -
- **PDF:** AmRain S.13,21,106,108
- **DXF-Belege:** 181E19 (ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.dxf, rot None) · 181E37 (ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.dxf, rot None) · 181E55 (ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.dxf, rot None) · 181E73 (ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.dxf, rot None) … +3 weitere

### RW-125 — sl_lichtnachweis_teilflaeche
Eine SL belegt nur ihre eigene Teilfläche: keine Lux-Deckung zwischen zwei Spots unterstellen, Treppenhaus-Nachweis deckt kein fernes Gangende, SL nahe Treppe ist kein Stufen-Nachweis — je Abschnitt eigene Lichtberechnung (EN 1838 4.2.7).
- **Leuchtentyp:** -
- **PDF:** AmRain S.80,97,107
- **DXF-Belege:** 73E5A (ARAI5_FE_XEL_ZZ_MOP_OG3_0014_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) · 1287E8 (ARAI5_FE_XEL_ZZ_MOP_UG_0010_V_02_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) · 9C81D (ARAI5_FE_XEL_ZZ_MOP_OG2_0013_V_01_RIVO_Symbole_TEILSTAND_v2.dxf, rot None)

### RW-126 — aussenleuchten_kein_wegnachweis
Fassaden-/Außenleuchten entlang der Gebäudekontur belegen KEINEN begehbaren Außenfluchtweg (auch nicht um Ecken); der Außenweg vom letzten Ausgang bis zum sicheren Bereich ist gesondert festzulegen und nachzuweisen.
- **Leuchtentyp:** -
- **PDF:** Tomaschek S.66,69,85
- **DXF-Belege:** 36BA5 (SG_RIVO_Erklaerung.dxf, rot None) · 36BC2 (SG_RIVO_Erklaerung.dxf, rot None) · 36BDF (SG_RIVO_Erklaerung.dxf, rot None) · 36BFC (SG_RIVO_Erklaerung.dxf, rot None) … +5 weitere

### RW-127 — erfassungsrand_pruefrand
Erfassungsrand ≠ Prüfrand: das Ende der erfassten/ersetzten Leuchtenmenge beendet NICHT den nachzuweisenden Rettungsweg; angrenzende Bestandsflügel bleiben offene Prüfpflicht — im Bestand ohne belegte Zielobjektfolge keine Symbole erfinden.
- **Leuchtentyp:** -
- **PDF:** Tomaschek S.144,207
- **DXF-Belege:** 2082F (EG_RIVO_Erklaerung.dxf, rot None) · 2084D (EG_RIVO_Erklaerung.dxf, rot None)

### RW-128 — sichtkette_erst_nach_passage
Eine RZ-Sichtkette (NB-R12) darf erst behauptet werden, wenn Tür-/Rampen-Durchgängigkeit belegt ist; Niveauwechsel im bestätigten Weg löst die §4.1.2-Prüfung aus.
- **Leuchtentyp:** -
- **PDF:** AmRain S.110
- **DXF-Belege:** 128ACA (ARAI5_FE_XEL_ZZ_MOP_UG_0010_V_02_RIVO_Symbole_TEILSTAND_v2.dxf, rot None)

### RW-129 — keine_sonderregel_aus_raumlabel
Hochrisiko-/Sonderregel-Einstufung nie allein aus dem Raumnamen (HEIZZENTRALE/Technikraum): Nutzungs- und Lichtwirkungsprüfung erforderlich; anonyme *U-Blöcke und Fremdgewerk-Texte erst per Legende klären.
- **Leuchtentyp:** -
- **PDF:** AmRain S.111,113 · Tomaschek S.210
- **DXF-Belege:** 128D11 (ARAI5_FE_XEL_ZZ_MOP_UG_0010_V_02_RIVO_Symbole_TEILSTAND_v2.dxf, rot None) · A9F3B (ARAI5_FE_XEL_ZZ_MOP_UG_0010_V_02_RIVO_Symbole_TEILSTAND_v2.dxf, rot None)

### RW-130 — schul_einstufung_schwellen
Schul-Einstufung (Enis-Lane): 3.200-m²-NETTO-Grundflächen-Schwelle (OIB RL2/OVE R12-2) über die maßgebende GESAMTfläche inkl. Bestand; Betriebsdauer 3 h nur bei erhöhten Anforderungen (Fußnote c); ≤20 Leuchten je Endstromkreis; Normausgabe exakt zitieren (AC1:2020 ≠ 2025).
- **Leuchtentyp:** -
- **PDF:** Tomaschek S.9,12,26,208
- **DXF-Belege:** 34BFE (SG_RIVO_Erklaerung.dxf, rot None) · 34C1C (SG_RIVO_Erklaerung.dxf, rot None) · 34C36 (SG_RIVO_Erklaerung.dxf, rot None)

### RW-131 — endausgang_dreiklang
Endausgang-Dreiklang (EN 1838 4.1.2 g): RZ + tatsächliche Ausgangstür + beleuchteter Außenweg bis zum sicheren Bereich sind ZUSAMMEN nachzuweisen — eine Leuchte an der Tür allein belegt den Außenweg nicht.
- **Leuchtentyp:** -
- **PDF:** Tomaschek S.15,60
- **DXF-Belege:** 34B86 (SG_RIVO_Erklaerung.dxf, rot None) · 34BA4 (SG_RIVO_Erklaerung.dxf, rot None) · 34B68 (SG_RIVO_Erklaerung.dxf, rot None) · 34E01 (SG_RIVO_Erklaerung.dxf, rot None) … +1 weitere
