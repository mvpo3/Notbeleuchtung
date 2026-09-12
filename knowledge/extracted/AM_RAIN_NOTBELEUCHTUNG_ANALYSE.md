# AM_RAIN_NOTBELEUCHTUNG_ANALYSE

## 1. Quelle, Geltung, Analysestand

**Quelle:** 6 din-Referenz-DXF in `DIN-Notbeleuchtungspläne(Beispiele)/Am Rain Notbeleuchtungspläne/` (NUR LESEN, AutoCAD-Locks — `.dwl/.dwl2` liegen daneben):

- `ARAI5_FE_XEL_ZZ_MOP_UG_0010_V_02.dxf`
- `ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02.dxf`
- `ARAI5_FE_XEL_ZZ_MOP_OG1_0012_V_01.dxf`
- `ARAI5_FE_XEL_ZZ_MOP_OG2_0013_V_01.dxf`
- `ARAI5_FE_XEL_ZZ_MOP_OG3_0014_V_01.dxf`
- `ARAI5_FE_XEL_ZZ_MOP_OG4_0015_V_01.dxf`

Rohdaten-Extrakte: `scratchpad/am_rain/<GESCHOSS>.json` (INSERTs name/layer/x/y/rot, Block-Zählungen, Blockdef-Entity-Arten, Notlicht-Layer, rote Texte, Layouts; `insunits=4` = mm). Attribute/Layout-Texte stehen NICHT in den JSONs — wo zitiert, wurden sie read-only per ezdxf direkt aus den DXF verifiziert.

**Geltung:** Am Rain ist ein **din-Praxisplan → Tag Referenz-Praxis (Rang 3 der Entscheidungs-Hierarchie**, `platzierung_regeln.yaml:56-60`). **AT-Zuordnung ist BELEGT** (nicht mehr nur Indiz): OG1-Layout2-Plankopf „Wohnhausanlage / Am Rain 5 / 1220 WIEN“, Planer „RR Electro - Engineering GmbH, Simmeringer Hauptstraße 39, A-1110 Wien“, Bauherr Österreichisches Siedlungswerk (1080 Wien), „1:100“ — Tag anhebbar auf **„Referenz-Praxis AT (belegt)“**. Am Rain ist zudem **identisch mit dem V25-Referenzprojekt** (Dateinamen = XRef-Muster aus `DIN_PLANUNGSUNTERSTUETZUNG_V25_ANALYSE.md:9-10`, Symbolzählungen matchen komponentenweise). Norm-Aussagen werden nur gegen `src/notbeleuchtung/normwissen/data/*.yaml` zitiert; Praxis überschreibt nie OIB/EN-Hard-Stops.

**Analysestand:** 2026-09-12. 6 Geschoss-Analysen, adversarial verifiziert: **44 Findings gehalten** (mit dokumentierten Korrekturen), **12 Behauptungen verworfen** (Abschnitt 5). Owner-Regelwerk-Referenz: `knowledge/extracted/NOTBELEUCHTUNG_ZEICHNEN_LERNEN.md` (R-A..R-K).

## 2. Gebäude-/Geschossüberblick

Wohnhausanlage Am Rain 5, 1220 Wien: 6 Stiegen + Reihenhäuser H1–H8, UG mit Tiefgarage (Fahrgasse ~150 m, „BRANDABSCHNITT 2“ @(83302,39887) im UG-DXF), OG4 mit GEM.TERRASSE (107,61 m²) + DACHAUSSTIEG.

| Geschoss | Notlicht-INSERTs | Inhalt |
|---|---|---|
| UG | **213** | davon **106 din-STANDARD-Welt** (31 RZ_PU + 12 PLPR + 2 PL + 1 PR + 30 SL + 19 SPOT + 3 SPOT_SL + 5 SYSTEM + 3 \*U1814) — deckt die V25-UG-Zeile exakt (`DIN_PLANUNGSUNTERSTUETZUNG_V25_ANALYSE.md:29`) — **plus 102 SIMA_ET-Zweitwelt** (45 SIMA_ET_SIBEL_Sicherheitsleuchte, 5 „SiBel Zentrale“, ~50 anonyme \*U14xx/\*U15xx) + 5 \*U65-Typenschilder |
| EG | **37** | Stiegen-Eingänge, Laubengang-Sichtketten, 6 Außen-SL (Wandausleger) |
| OG1 | **9** | NUR Stiege 2 + Stiege 4 (die mit communal Gang); Stiegen 1/3/5/6 + H1–H8 = 0 |
| OG2 | **13** | 2 Gang-Achsen + STGH-Template, Rauchschutztür-RZ |
| OG3 | **12** | wie OG2, STGH-Flächenkontrast 31,50 vs. 12,74 m² |
| OG4 | **3** | Minimal-Bestückung: RZ_PL + RZ_PU + 1 SPOT_SL im STGH-Band |

**R-K-Lehre:** din liefert **immer ein Blatt je Geschoss** (alle 6 Dateien existieren, OG4 mit nur 3 Symbolen) — der „kein Plan nötig“-Ast von R-K wird als **Minimal-Bestückung**, nicht als Weglassen ausgeübt. Liefer-Konvention (Blatt je Geschoss) und Platzierungs-Minimalismus sind **zwei getrennte Entscheidungen**. Innerhalb des Geschosses fällt der Planumfang scharf: UG (Garage, mehrere Brandabschnitte, 5 Anlagen) = 106 din-Symbole; Wohn-OGs = 3–13, ausschließlich am Fluchtweg-Skelett.

## 3. Verifizierte Findings

Alle Findings adversarial geprüft (Belege koordinaten-/zeilengenau reproduziert); Verdict-Korrekturen sind eingearbeitet und als *Korrektur* markiert.

### 3.1 Block-/Layer-System & Import

**Importer-Warnung/-Härte: Header-Extents lügen, Symbolwelten als Koordinaten-Inseln (34,6-Mio-mm-Klasse) — Cluster statt EXTMIN/EXTMAX** *(selman_erkennung + leonis_engine, mittel)*
UG trägt zwei disjunkte Symbolwelten: lokale din-Welt x=1.166–162.514 mm (111 Inserts) vs. SIMA_ET-Insel x=34.584.218–34.742.329 mm (102 Inserts, ~34,5 km entfernt); die Header-Extents `[-9660,-146219,439322,58267]` (UG.json:4-9) decken die SIMA-Welt NICHT (Faktor ~79). OG3 umgekehrt: Extents bis x=34.746.632 (34,75 km) bei Symbolen im Band x=11.843–73.111. Header-Extents sind also in **beide** Richtungen unbrauchbar → Import braucht Symbol-/Entity-Dichte-Cluster, Inseln getrennt ausweisen statt BBox sprengen; unsere Caps (`_MAX_RASTER_PX`, Unterlage-Bounds-Filter `dxf_renderer.py:438-453`) kappen, clustern aber nicht — bei zwei Inseln gewinnt still die des größten Raums, ohne Warnung. *Korrektur:* Analogie zum Baufeld-4OG ist Klassen-, nicht Größengleichheit (34,7 km vs. 347 km); „georeferenziert“ für SIMA ist Indiz, nicht bewiesen. Fallback-Blocksignatur: `STANDARD_SPOT_SL {LINE:18}` (Strahlenkranz) vs. `STANDARD_RZ_*` (HATCH 3, LWPOLYLINE 5–10, LINE 0) — korpusweit eindeutig.
Beleg: UG.json extents vs. `SIMA_ET_SIBEL_Sicherheitsleuchte`(34589975.3,1203402.1) + `SiBel Zentrale`(34731850.3,1204857.1); OG3.json blockdefs.

**SIMA_ET-Zweitsystem im UG ist NEU gegenüber V25 — der 11_system-Layer ist es NICHT** *(doku, hoch)*
`din_SIBEL_11_emergency_lighting_system` steht bereits in `DIN_PLANUNGSUNTERSTUETZUNG_V25_ANALYSE.md:23` („5x“); die UG-Zählung reproduziert die V25-UG-Zeile 106 spaltengenau — **Am Rain IST das V25-Projekt, jetzt mit lesbarer Architektur** (ODA-Blocker entfällt: UG-Modelspace enthält 489 Raum-Beschriftungs-Texte, Wand-/Tür-Layer). Wirklich neu: (1) SIMA_ET-Zweitwelt (45 SL + 5 „SiBel Zentrale-A0RC9Y\*“ auf `SIMA_ET_SiBel_Symbol` + anonyme \*U-Blöcke, per GEBEZ als „SIMA_ET_SIBEL_Rettungszeichenleuchte linksrechts/obenunten“ belegt; ATTRIBs nur GEBEZ/Z='1', keine Produktdaten = Alt-/Fremdsystem-Indiz), (2) Layer `din_SIBEL_34_color_sperr` (UG.json:22, in V25-Analyse unerwähnt, Inhalt ungeklärt), (3) 5× \*U65-Typenschild auf Legacy-Layer `E_Fluchtwegleuchten`, je <450 mm neben einem STANDARD_SYSTEM. *Korrektur:* anonyme \*U14xx/\*U15xx sind 50 (nicht ~55). Doku-Folge: V25-Analyse um AT-Zuordnung + Quellen-Merge ergänzen.
Beleg: V25-Analyse:23+:29; UG.json:19+22; DXF-ATTRIB-Probe.

**Owner-Frage UG-Doppelwelt: SIMA_ET Bestand/Fremdsystem oder gültiger Ausführungsstand?** *(owner_frage, mittel)*
Beide Welten decken denselben Inhalt (5 SIMA-Zentralen vs. 5 STANDARD_SYSTEM; parallele Fahrgassenreihen, SIMA-Deltas u.a. 10000/12000/12700 mm): SYSTEM-Paar (11791.8,3933.5)/(11791.8,3183.5) vs. SiBel-Paar (34594880.3,1166381.5)/(34594880.3,1166031.5). SIMA ohne Produktdaten vs. STANDARD mit vollem Datenmodell → Indiz Alt-System, aber Festlegung nur durch Owner.

**R-B NICHT PRÜFBAR — Blocknull-Konvention der STANDARD_RZ_\*-Blöcke fehlt (einmalige Owner-Sichtung löst es)** *(owner_frage, hoch)*
Rotation „Piktogramm ins Rauminnere“ ist über alle 6 Geschosse konsistent-widerspruchsfrei: PU-Rotation variiert türabhängig über alle 4 Orthogonalen (EG rot0 (9793.2,23965.9) / rot90 (14818.6,17633.4) / rot180 (95.1,39047.2); UG rot270 (61730.1,38770.4)), ausnahmslos xscale=1 (keine Spiegelung), identische Stack-Positionen OG1–OG4 tragen identische Rotationen. Aber blockdefs im JSON enthalten nur Entity-Zählungen (RZ_PU: ATTDEF 28, INSERT 1, HATCH 3, LWPOLYLINE 5, CIRCLE 1) — die Blickrichtung bei rot=0 ist maschinell nicht ableitbar. Eine AutoCAD-Sichtung eines RZ_PU fixiert die Konvention und macht R-B an allen din-Referenzplänen automatisch prüfbar. Regel: `NOTBELEUCHTUNG_ZEICHNEN_LERNEN.md:20-27`.

### 3.2 Platzierungsmuster

**R-F BESTÄTIGT+VERFEINERT: Sichtketten-Dichte skaliert mit Raumgeometrie — 30-m-Limit im EG ausgereizt, UG-Kellergang 6,7-m-Takt** *(leonis_engine, hoch)*
RZ als Sichtkette mit kontextabhängiger Dichte, kein Festraster: größte EG-Lücke RZ_PR(4825.3,39072.6)→RZ_PL(35206.6,39046.6) = **30.381 mm** am Norm-Default 30 m für hinterleuchtete RZ — Norm exakt: `en1838_grundwerte.yaml:52` `z_hinterleuchtet: 200.0`, `:56` `piktogramm_hoehe_default_m: 0.15`, `platzierung_regeln.yaml:243` `default_max_sichtachse_m: 30`. UG-Fahrgasse: 7 RZ auf dem Band (PLPR 29538.4/41077.0/97452.4, PU 77413.8, 3× \*U1814 y=30533.2); Kellergang dagegen dichte RZ_PU-Kette (61002.4/67732.1/74405.3, y=8227.5, Deltas 6729,7/6673,2 mm — Sichtabbruch durch Abteilstruktur). Engine-Verfeinerung: **Kette bis Erkennungsweite strecken, Dichte aus Sichtlinien, nicht aus Distanz.** *Korrekturen:* 30.381 mm liegt 1,3 % ÜBER 30 m (Insert-zu-Insert) — als Obergrenze mit Toleranzhinweis führen; die Fahrgassen-Kette enthält eine **52,7-m-Lücke** (97452.4→150193.3, vermutlich Sichtbruch/Brandabschnitt, offen); RZ-Spann der Fahrgasse = 138,2 m; \*U1814 ist ein anonymer Block („Typ N“ nur per ATTRIB).

**R-F/R1/R6 BESTÄTIGT (mm-genau): Bestandslinie + Spot-Lückenmitte ist exakt die din-Praxis** *(leonis_engine, hoch)*
OG1: Bestandsraster `E_Beleuchtungstyp` (\*U32) y=9276.4, x=59099.8..76599.8 (exakt 2500,0 mm); SPOT_SL (62876.5,9298.4) = **26,7 mm** neben Lückenmitte 62849.8, y-Versatz **22,0 mm**; zweiter SPOT (73111.2,9298.4) = 261,4 mm neben 72849.8. OG4: \*U43-Linie x=13226.3, Raster 2400,0 mm; SPOT_SL (13195.3,12641.2) = 31,0 mm neben Achse, 130,0 mm neben Lückenmitte 12771.2. Owner-Regeln R1/R6 (`NOTBELEUCHTUNG_ZEICHNEN_LERNEN.md:107`) sind Referenz-Praxis-validiert; keine Implementierungs-Änderung nötig. *Korrekturen:* „millimetergenau“ gilt streng für den Achs-Versatz (22–31 mm), Lückenmitte auf 27–261 mm; Datenbasis 3 distinkte Spot-Positionen, OG4-Spot ist koordinatenidentisch mit OG1 (Wiederholgeschoss) — nur der \*U43-Raster-Nachweis ist OG4-eigen; „Bestand“ = Interpretation des Layers `E_Beleuchtungstyp` (funktional egal).

**Neues Praxis-Band: Gang-SL-Achsabstand ~10,0–10,25 m — als Plausibilitäts-Band, NICHT als Raster** *(leonis_engine, mittel)*
Wohnbau-Gang mit „eco spot SL DA R“: 9.989 (EG) / 10.021 (OG3) / 10.235 mm (OG1/OG2, identisches Paar), y-Streuung ≤64 mm; UG-Fahrgasse Median ~10,1 m bei Streuung 5.678–14.367 mm; Keller deutlich dichter (*Korrektur:* ~4,3–7,9 m, nicht 6,7–7,1). Einordnung: das Band ist ein **Lichtberechnungs-Ergebnis** (R-J: OG1 nur 2 SPOTs auf 8 Achsen-Bestandsleuchten = 7 Lücken), taugt als Plausibilitäts-Band für den Lux-Nachweis (`en1838_grundwerte.yaml:74` `rettungsweg: 1.0` [BELEGT §4.2.1]; `:66-68` Wartungsfaktor innen `0.80` [PRAXIS]) — nichts hardcoden. *Korrektur:* OG2 hat im Mittelgang ein 17.357-mm-Gap — Band gilt für die zitierten Paare, nicht universell; SL-Rotation folgt der Gangachse (mod 180), konkrete Gradzahlen nicht blockübergreifend generalisierbar.

**R-J BESTÄTIGT + Praxis-Anker: Aufheller-Anzahl folgt der Lichtberechnung** *(leonis_engine, hoch)*
20-m-Gang mit 2500-mm-Bestandsraster (9 Leuchten) → nur 2 Not-Spots (Abstand 10.234,7 mm); großes STGH (31,50 m²) 1 SL, kleines (12,74 m²) keine (OG3: SL-Paar (24115.9,17649.1)→(34137.1,17585.2)=10.021,2 mm). Trennung „RZ=Platzierungsregel / SL=Lichtberechnungs-Ergebnis“ materiell belegt (`NOTBELEUCHTUNG_ZEICHNEN_LERNEN.md:81-86`).

**R-E VERFEINERT/SPANNUNG: Antipanik als WANDAUSLEGER neben der Eingangstür (auch unter VORDACH), nicht deckenmittig** *(owner_frage, hoch)*
Alle Stiegen-Eingänge im EG (4 Eingangs-Situationen, 6 SL gesamt) bekommen eine `CONCEPT 2  AP 3 WA` als Wandausleger — #v1-dekodiert (base64+XOR 0xFF): `MountingMethod='Wandausleger'`, `AccessoriesAsText='9020000052;;;Concept-WA-PP-G Kunststoff;;;Wandausleger parallel zur Wand geschlossen;;;0'`. Distanzen SL→Tür-RZ: PU(95.1,39047.2)+SL(−1441.6,38545.4)=1,62 m (SL orthogonal ~1,44 m VOR der Fassadenlinie x≈0); PU(55677.4,34444.0)+SL(54645.6,34193.1)=1,06 m am „VORDACH“(53749.9,33451.8); PU(9793.2,23965.9)+SL(8930.5,24202.8)=0,90 m am „EINGANG“. **4 VORDACH-Texte im EG, je einer pro Eingang → R-E Fall 1 wäre überall einschlägig, die Abweichung (seitlich statt mittig) ist systematisch**; Fall 3 („keine Leuchte“) kommt nicht vor. Widerspricht R-E Fall 1 (`NOTBELEUCHTUNG_ZEICHNEN_LERNEN.md:40-49`) in der Ausführung — EN 1838 §4.1.2 schreibt keinen Montageort fest. Owner-Entscheid nötig (Frage 4, Abschnitt 7). *Korrekturen:* die VORDACH-SL gehört zu Stiege 5 (nicht 4); Distanz-Range korrekt 1,0–1,6 m (SL→Tür-RZ 1,06/1,39/1,49/1,62 m).

**R-K VERFEINERT: immer ein Blatt je Geschoss; OG1 liefert Kriterium-Kandidat „communal Gang vorhanden?“** *(owner_frage, hoch)*
(1) Blatt je Geschoss = Liefer-Konvention (s. Abschnitt 2). (2) Scharfes Kriterium in OG1: alle 9 Inserts in x=11843.8..13969.5 (Stiege 2) und x=54897.1..73111.2 (Stiege 4); STGH-Stempel Stiegen 1/3/5/6 @(7608,40654)/(34788,42991)/(67189,38835)/(146140,38585) und H1–H8 (x 87814..126400) ohne ein einziges STANDARD_\*-Insert. Flächen-Gegenprobe stärkt es: einziger großer GANG (31,06 m², Feinsteinzeug) liegt im Stiege-4-Cluster; alle anderen GANG-Labels 3–11 m² Parkett = wohnungsintern. *Korrektur:* „4_10“ ist eine WOHNUNG, der GANG-Text ist separat/unnummeriert → Kriterium formulieren als **„gemeinschaftlicher GANG-Raum (groß, mit Wohnungstüren) zwischen Wohnungen und STGH“**, nicht „nummerierter Gang“. Regel: `NOTBELEUCHTUNG_ZEICHNEN_LERNEN.md:88-93`.

**R-A BESTÄTIGT (Ergebnisbild): Symbolverteilung folgt in allen 6 Geschossen der Fluchtwegstruktur** *(doku, niedrig)*
Nächster-Stempel-Analyse pro Insert über alle 6 DXF: kein einziges Insert mit Wohnungs-/Privatraum-Kontext; OG3 „ZI 1“(36652,20231)/„WOHNKUECHE“(16256,20798) symbolfrei; OG4 „GEM.TERRASSE“/„107.61 m²“(18404,15217)/(18812,14843) und „DACHAUSSTIEG“(55643,9536) leer. Planungs-REIHENFOLGE (Prozess) aus fertigen DXF nicht beweisbar — Ergebnis vollständig R-A-konsistent, 0 Widerspruchsfälle. Randfrage Owner: Dachterrasse bewusst notlichtfrei?

**STGH-Template-Klone: identischer Offset +2125,7/−2372,0 in OG1/OG2/OG3, beide Cores — Determinismus-Anker (R-H)** *(leonis_engine, niedrig)*
RZ_PL(11843.8,22368.9,rot90)→RZ_PU(13969.5,19996.9,rot0) West = RZ_PL(54897.1,15003.6)→RZ_PU(57022.8,12631.7) Ost, Delta identisch bis 0,1 mm (Abstand 3,19 m), über 3 Geschosse bit-identisch (West-Template auch in OG4). Situative Ergänzungen ON TOP: nur Ost-Core trägt das PLPR am Verzweigungsknoten (56350.8,9484.0), nur das große West-STGH eine SL. Praxis-Bestätigung R-H + billiger Regressionstest (gleiche Stiegen-Geometrie ⇒ identische relative Anordnung). Blockiert durch Selman-Naht `Treppenlauf.richtung` (02-TWA). Beleg: `platzierung_regeln.yaml:256-266` (RZ-10 Wasserscheide), `NOTBELEUCHTUNG_ZEICHNEN_LERNEN.md:68-74`.

**Wohnungstüren-Abstinenz + WOHNUNG_PRIVAT-Skip durch alle 6 Geschosse — RZ-08 ist exakt die din-Praxis** *(doku, mittel)*
Keine Wohnungstür trägt ein RZ; Wohnungen, Maisonette-Oberebenen, private AR/VR, GEM.TERRASSE leer. Validiert RZ-08 (`platzierung_regeln.yaml:212-231`, „Diese Regel erzeugt NICHTS“), WOHNUNG_PRIVAT-Skip und OIB Zeile 1.1 „außerhalb von Wohnungen“ (`oib_rl2_tabelle6.yaml:145-146`) im Ergebnis. **Am Rain taugt als Golden-Referenz/Regressions-Anker:** ein Lauf, der Wohnungstüren bestückt oder Wohnungen füllt, weicht messbar ab. *Einschränkung:* Detail-Kontexte (OG2 „2_23“ d=596) stammen aus DXF-Radius-Queries, nicht aus den JSONs.

**Offene Detailfrage Kellergang-PU-Kette: türgebunden (R-G-konform) oder Verlaufs-RZ?** *(owner_frage, mittel)*
3 RZ_PU (61002.4/67732.1/74405.3, y=8227.5, rot=0, Deltas 6729,7/6673,2 mm) mit fast x-identischer paralleler SPOT-Zeile (61037.2/67766.5/74415.4). Einziger Fund mit regelmäßiger Verlaufs-Signatur, der R-G (`NOTBELEUCHTUNG_ZEICHNEN_LERNEN.md:61-66`) potenziell widerspricht; JSON trägt keinen Tür-Kontext. *Caveat:* zweite kollineare 3er-PU-Kette bei x=14832.9 (Deltas 4730/3984 mm, eher Tür-Signatur) bei der Owner-Sichtung mitprüfen. Keine Keller-Sonderregel vor Klärung.

### 3.3 Kennzeichnung (Typenschild/Attribute/QR)

**Typenschild-System (Layer 50/51) = gebäudeweiter Typ-Letter + QRGuid je Leuchte** *(leonis_engine, hoch)*
Kennzeichnung ausschließlich über Block-ATTRIBs auf Sub-Layern: TYPE/TYPENAME → `din_SIBEL_50_type_name`, TYPENUMBER „Typ \<Letter\>“ → `din_SIBEL_51_typenumber`, QRGuid + #v1-Produktdaten (Artikelnummer, MountingMethod, Technology=PLC24) → `din_SIBEL_99_general` (*Korrektur:* nicht 62_QRCode — dort liegt der genestete QR-Grafik-Block). Buchstaben **gebäudeweit stabil**: kein Letter mappt geschossübergreifend auf verschiedene Produkte (Typ H = `BASIC 2 E-SIGN plus 115mA DA` Art. 9071090810 auf allen 6 Geschossen; Typ L = 9069099300 überall; Typ K UG+EG = 9069099100). Belege: STANDARD_SYSTEM(11791.8,3933.5)=Typ A `SU 6 NET 12Ah WA E30 1h`; RZ_PU(12195.6,41061.1)=Typ H; OG2 exakt 8 RZ Typ H + 5 SL Typ L; GUIDs `99991ccb-…`(OG2), `5f556f78-…`(OG4), instanz-eindeutig (UG 106/106). *Korrekturen:* UG-Spektrum = 13 Typen A,B,C,D,E,F,H,I,J,K,L,N,O (nicht nur A/F/H/K/N); EG zusätzlich Typ K; 1 von 3 \*U1814 ist „Typ O“ (gleicher Artikel, anderes Zubehör). Konsequenz: Typ-Letter-Stückliste (#7/#98) von geschossweise auf gebäudeweit; QRGuid/SelectedArticleNumber = Vorbild für `luminaire_id`/`catalog_key`. Artikelnummern 9071/9069/9080 Schrack-typisch (vgl. `aus_elektroplaner/Schrack_Katalog_NotSicherheitsbeleuchtung.md`) — AT-Produkt-Indiz.

**Beschriftungs-Modell: NULL Freitexte auf Notlicht-Layern in allen 6 Geschossen** *(leonis_engine, hoch)*
`texte_notlicht_layer=[]` wortwörtlich in UG.json:2223, EG.json:387, OG1.json:138, OG2.json:170, OG3.json:162, OG4.json:82; DXF-Gegenprobe: auch 0 MLEADER/LEADER/DIMENSION auf Notlicht-Layern (Extraktions-Artefakt ausgeschlossen — `extract.py:39` scannte nur TEXT/MTEXT). ATTDEFs: RZ_PU=28, SPOT_SL=21; ATTRIBs zu 100 % populiert (UG 103/103 din-INSERTs mit 2639 ATTRIBs). Sauberes Gegenmodell zu Leader/Solitärtext-Beschriftung (Falsch-Platzierungs-Klasse) → Render-Empfehlung: Labels als Attribute an den Block, Sub-Layer-schaltbar. *Randnote:* 20–28 ATTDEFs gilt für die din-Leuchtenfamilie; STANDARD_SYSTEM=18, UG-Altfamilie SIMA=6.

**„Rolle ≠ Produkt“ verschärft: Blockname STANDARD_\* ist KEIN Katalog-Key; AP3-Universalleuchte fährt als RZ** *(enis_norm, mittel)*
\*U1814 (TYPE=RZ, TYPENAME `Concept 2 AP3 PLC24`, Art. 9080095009) bei (12007.0,30533.2)/(59331.7,30533.2)/(150193.3,30533.2) rot=90 — dieselbe AP3-Universalleuchte, die bei uns als Antipanik geführt wird, hier in RZ-Rolle (Blockdef HATCH 72/LWPOLYLINE 201/CIRCLE 36 + nested INSERT `QRCode`). Stärkster Zusatzbeleg: UG-`STANDARD_RZ_PU` trägt **5 verschiedene Produkte** im TYPENAME, `STANDARD_RZ_PL` sogar ein SL-Produkt (`CONCEPT 2 SL 3 WA EW 20m`) — Rolle und Produkt sind orthogonal. Naht `schrack_symbol_mapping`: Rolle+Produkt getrennt führen; catalog_key nie auf din-Blocknamen stützen, nur auf ATTRIB-Artikelnummern. *Korrekturen:* dritte \*U1814-Instanz = „Typ O“; OG2-String exakt `BASIC 2  E-SIGN plus 115mA DA`.

**Symbol-Datenmodell-Vorbild (Konsequenzen gebündelt)** *(leonis_engine, mittel)*
(1) Typ-Letter-Stückliste gebäudeweit, (2) QRGuid/SelectedArticleNumber → luminaire_id/catalog_key (Klartext statt #v1 = Owner-Entscheid), (3) Label-Rendering als Blockattribut = din-Praxis (deckt ADR „Beschriftung ans Symbol“). *Korrekturen aus Verdicts:* Spektrum reicht bis Typ O; Rückrichtung nicht injektiv — `Concept 2 AP3 PLC24` trägt 7 Letters (B,C,E,F,G,N,O) — der Letter kodiert Produkt+Piktogramm-/Montagevariante, TYPENAME-genau; Engine-Granularität catalog_key→Letter ist richtig.

### 3.4 UG/Garage

**UG-Sonderfall (R-F/R-J): SL-Lichtband auf EINER Achse quer zur Fahrbahn, RZ nur an Entscheidungspunkten, PLPR in Bandlinie** *(leonis_engine, mittel)*
16 STANDARD_SL exakt y=30570.0, alle rot=270 (Blocklängsachse 653×330 mm quer zur x-laufenden Fahrgasse), x=17224.8..162514.1, Median 10.105 mm über 145,3 m; 0 Fremd-SL im Korridor y 28000–33500. 3 RZ_PLPR (29538.4/41077.0/97452.4) nur 19–37 mm neben der SL-Linie = Fahrgassen-Mitte in Bandlinie; RZ_PR (8275.8,38993.3) am STIEGE-1-Ende. „BRANDABSCHNITT 2“ (83301.6,39887.1) im DXF verifiziert. *Korrekturen:* „7 RZ auf 150 m“ zählweisenabhängig (5–9) — „sparsam“ hält in jeder Zählung; auch 1 RZ_PU sitzt mit auf der Bandlinie.

**System-/Anlagensymbolik ist ein reines UG-Thema: 5× SU 6 NET dezentral, nummerierte Anlagen mit Typenschild-Sibling** *(leonis_engine, mittel)*
Genau 5 STANDARD_SYSTEM auf `din_SIBEL_11_emergency_lighting_system` (11791.8,3933.5)/(11791.8,3183.5)/(53813.9,5339.6)/(54166.7,5356.6)/(148762.5,40193.7); in EG–OG4 existiert weder Layer noch INSERT. ATTRIBs: TYPENAME `SU 6 NET 12Ah WA E30 1h`, Typ A, **INFOTEXT durchnummeriert „Anlage 1“–„Anlage 5“** (*Korrektur:* nicht einheitlich „Anlage 4“ — das gilt nur für (11791.8,3933.5)). Je Anlage ein \*U65-Typenschild in 307–439 mm. *Korrekturen:* 5 Geräte an nur **3 Standorten** (2+2+1 bei Stiege 2/4/6 — nicht „Stiege 1“); „je Brandabschnitt“ ist Interpretation. Engine-Ableitung: Anlagen-Symbole nur im Geschoss der Anlagentechnik rendern; Owner-Tabelle Anlage→Brandabschnitt für circuit_hint anfragen.

**5× SU 6 NET = k-sibe-LPS-Prinzip in der Praxis; „Anlage n“ als circuit_hint-Vorbild** *(leonis_engine, mittel)*
Deckt `Schrack_Katalog_NotSicherheitsbeleuchtung.md:131` („Gruppenbatterie (LPS…) Pro Brandabschnitt eine Anlage -> macht E30-Verkabelung ueberfluessig“ — E30 hier im Gerätegehäuse, 1h = `en1838_grundwerte.yaml:48` `dauer_min: 60`) und `:101` (EN-62034-Autotest). Technology=PLC24 auf 98 Leuchten + QRGuid auf 106 → Praxis-Bestätigung der >20-SL-Schwelle (`astv_arbeitsstaetten.yaml:329-332` 560.9.001.AT; `:377-384` `_AUTO_PRUEF_SCHWELLE`-Konsument, Bezugseinheit bleibt offen wie dokumentiert). Ziel-Schema für Leonis: durchnummerierte „Anlage n“-Labels.

### 3.5 Norm-Abgleich & Regel-Lücken

**DE/AT-Einordnung GEKLÄRT: Am Rain = Wiener AT-Projekt mit din-Produktwelt, identisch mit V25** *(doku, mittel/hoch — 2 Findings konsolidiert)*
Plankopf-Volltreffer (OG1-Layout2): PROJEKT „Wohnhausanlage / Am Rain 5 / 1220 WIEN“, RR Electro A-1110 Wien, Bauherr ÖSW 1080 Wien, Architekt Kreiner+Partner 1020, GU Swietelsky 1130, „1:100“, www.rr-electro.at. AT-Vokabular im Modelspace: STGH 6×, VR 23×, AR 19×, „9 STG 17/28“ 41×, „Parapet notw.?“ (OG2), „KELLER STIEGE 3/6“ (UG). Jurisdiktions-Bedingung der OIB-Auswertung erfüllt (`oib_rl2_tabelle6.yaml:102-106` `jurisdiktion.erforderlich: "AT"`). *Korrekturen:* „TREPPENHAUS“ im UG ist 6× vorhanden (nicht einzeln), plausibel Vorlagen-Artefakt (Interpretation); Beleg NUR im DXF-Layout2, nicht in den JSONs — in Digests das DXF zitieren. Doku-Folge: V25-Analyse um „Am Rain 5, 1220 Wien“ + Merge ergänzen.

**Regel-Lücke: Brandabschnitts-/Rauchschutztür mitten im Gang bekommt bei din ein Tür-RZ — unser Regelwerk erzeugt dort NICHTS** *(enis_norm, hoch)*
OG2: RZ_PU (32604.5,17552.0) an der `EI2 30-S200`-Rauchschutztür nachweislich mitten im Gangband (GANG 48,90 m², nächstes STGH 20 m). Unsere Matrix kennt nur RZ-01/RZ-07/RZ-08 (`platzierung_regeln.yaml:212-231`, RZ-08: „Diese Regel erzeugt NICHTS“); `ausgaenge.py:62-65` promotet Brandschutztür nur mit STIEGENHAUS-Seite. Fachlich ist sie Sichtabbruch+Durchtritt — „jeder Ausgang und jede Tuere im Verlauf eines Fluchtweges“ (`astv_arbeitsstaetten.yaml:242`, E08 Abschn. 4, Ebene D). Vorschlag: neue Regel „RZ an Brandabschnitts-/Rauchschutztür am Fluchtweg“, decision_source `referenz_praxis`. *Korrekturen:* OG3-Beispiel (14935,17552) ist plausibel die STGH-Zugangstür (RZ-07-Territorium) — nur OG2 trägt „mitten im Gang“ sauber; Contract kennt `tuer_detail='brandschutztuer'` bereits (`raum_modell.py:29`, `tuer_typisierung.py:194`) — es fehlt EI-Klassen-Granularität + die Platzierungsregel, nicht das Merkmal (leichter umsetzbar als gedacht). Zusatz-Gap: Sichtkette behandelt solche Türen nicht als Barriere (`sichtkette.py:21-23` benennt den Gap selbst).

**Praxis LOCKERER als Norm-Default: din-STGH teils OHNE SL — SL-02 würde überall SL setzen** *(owner_frage, hoch)*
SL-02-TREPPE ist norm_default/BELEGT (`platzierung_regeln.yaml:314-330`, quelle „EN 1838 §4.1.2 b) — nahe Treppen, um jede Treppenstufe direkt zu beleuchten“, engine_status unterstuetzt). Am Rain: STGH 4_17 (12,74 m², OG3) NULL SL (nur PLPR+Tür-RZ), STGH 2_26 (31,50 m²) 1 SPOT_SL, OG4-STGH 1 SPOT_SL. Mögliche Auflösung: Stufenbeleuchtung per Lichtberechnung nachgewiesen (R-J, evtl. mit Beitrag beleuchteter RZ) — DXF belegt das nicht. Entscheidung: SL-02 Hard-Anker (Norm schlägt Praxis, §4.1.2 normativ) oder lichtberechnungsgesteuert. **Nicht still lockern.** *Korrektur:* „in der Bestandslücke“ (OG4) ist R1-Interpretation.

**R-K-Trigger-Kandidat bestätigt, aber OIB-Vorsicht: 0 Symbole ist KEIN sauberer Umkehrschluss** *(owner_frage, hoch)*
OG1-Kriterium (nur Stiege 2+4) maschinell greifbar — ABER `oib_rl2_tabelle6.yaml:12-14`: „KEIN UMKEHRSCHLUSS … -> review_required, nie nicht_erforderlich“; `:135-150` Zeile 1.1 fordert GK5 „außerhalb von Wohnungen“ die eingeschränkte Stufe, und die leeren STGH 1/3/5/6 SIND außerhalb von Wohnungen. Konsistent nur, wenn diese Stiegen nicht GK5 sind (unbelegte Hypothese) oder natürlich belichtet+niedrig. Empfehlung: Trigger als Referenz-Praxis-VORSCHLAG, der den OIB-Befund nie überschreibt (HS-03 fail-closed bleibt, `platzierung_regeln.yaml:597-610`), Owner-GO einholen. **Größter Einzelhebel auf die Symbolzahl im Wohnbau-OG** (unsere `anker_strategy.py:121-127` setzt heute an JEDEM Ausgang ein RZ → Überproduktion gegen die Referenz).

**KANN HEUTE (kein Gap): Sichtketten-Limit l=z·h + Bestandslinie/Lückenmitte sind implementiert und Am-Rain-validiert** *(doku, mittel)*
(1) `platzierer.py:71-77` (_arm_gap_mm = l=z·h via `norm.erkennungsweite_m(0.15, True)`) + `sichtkette.py:80` (kette_ausduennen) = exakt die EG-Praxis (~30,4 m Lücke, an/knapp über dem 30-m-Band; Engine wäre marginal konservativer: 1 Zwischen-RZ mehr, das ausduennen wieder entfernt). (2) `mittellinie_snap.py:57-83` (_bestand_mitte=R1 Median-Quer / _laengs_ausweichen=R6 Lückenmitte, `_BESTAND_MIN_LAENGS_MM=800`) = OG1/OG4-mm-Befund. Owner-Regeln vom 2026-09-11 unabhängig referenz-validiert.

### 3.6 Engine-Gaps & Owner-Fragen (Detail — speist Tabelle in Abschnitt 6)

**GAP (hoch): Bestands-Leuchten werden nirgends automatisch extrahiert — R1/R6 ist im Nordstern-Pfad tot** *(leonis_engine)*
`pipeline.py:189+211`: `bestand_leuchten_mm` nur Parameter der privaten `_run_mit_quelle`; die öffentliche `pipeline.run` (Z.152-163) exponiert das kwarg **gar nicht** → Upload-Pfad kann Bestand nie erhalten; einzige Befüller `scripts/demo/nachzeichnen_elektroplan.py:262` + Tests. Kein src-Modul liest `E_Beleucht*`-INSERTs; ohne Bestand fällt `mittellinie_snap` auf Bbox-Mitte. Kandidat: Layer-basierter Bestands-Extraktor in hauptengine (Blocknamen variieren: \*U32 OG1/EG, \*U43 OG4 — Layer ist der Schlüssel). Kein Contract nötig.

**GAP (hoch): Stiegenhaus-Template — Contract-Felder Treppenlauf/Podest liegen ungenutzt** *(leonis_engine)*
`raum_modell.py:174-200` (Treppenlauf.antritt/austritt/richtung, Podest.ist_hauptpodest) vs. grep `laeufe|podest` in platzierung = 0 Code-Treffer (nur `verbotszonen_nachpass.py:54`); `fachpraxis.py:569` R8-Nachpass ist explizit „Approximation (ohne Stiegenlauf-Geometrie)“. Am Rain klont das 2-RZ-Modul PL+PU mm-identisch (*Korrektur:* 2-RZ, nicht 3-RZ; drittes RZ nur OG2/OG3, nicht geklont). Kandidat: `platzierung/stgh_strategy.py` — je Lauf richtung='ab' ein Richtungs-RZ am (Haupt-)Podest + Pfeil-unten am Antritt (R-G umfasst den türlosen Stiegenantritt, OG4: PU 14,1 mm neben Laufachsen-LINE (13955.4,22060.2)→(13955.4,20100.3)).

**GAP (hoch, Selman-Naht): Treppenlauf/Podest auf echten Plänen füllen — R-H sonst unprüfbar** *(selman_erkennung)*
`StiegenhausModell.laeufe/podeste` default-leer (raum_modell.py:197-198); der Füllpfad in `raumerkennung/stiegenhaus.py` (Z.279/195/211) greift auf Am Rain nicht. Am Rain liefert erstmals lesbare Kalibrier-Referenz: Layer `Treppe` mit Laufrichtungs-LINEs + `Beschriftung Stiege` „8/9 STG 17/28“ (14130.8,20897.2).

**GAP (hoch): Beidseitiges RZ (PLPR) an Verzweigungsknoten — Wasserscheiden-Logik existiert, ist nicht verdrahtet** *(leonis_engine)*
`richtungsfeld.py:62-70` `wasserscheiden()` hat 0 Produktions-Aufrufer; `anker_strategy.py:136-151` vergibt an Kreuzungen immer EINE Richtung; `richtung='gerade'` produktiv nur bei LB-Vorgabe (sonderstellen RZ-06), Doppelpfeil-Render vorhanden (`inserter.py:107`). Am Rain: OG1–OG3 PLPR koordinatenidentisch (56350.8,9484.0,rot270) im STGH-Vorraum (Gang läuft weiter bis x=73111); EG 13× (3 Tripel + 2 Paare je Eingangsknoten); UG 12×. Kandidat: 'gerade' bei Wasserscheiden-Kante ODER „Zielraum verzweigt nach Durchtritt“ (Owner-Hypothese).

**GAP (mittel): Brandschutztür-Merkmal + Sichtbarriere** *(selman_erkennung, 3-Owner-Slice)* — siehe Regel-Lücke oben; auf `tuer_detail='brandschutztuer'` aufsetzen, EI-Klasse/Selbstschließer ergänzen (Am-Rain-Notation „EI2 30-S200“ matcht das heutige Regex `EI\s?30` nicht, Labels 3-fach gesplittet).

**GAP (mittel): Typ-Letter geschossweise statt gebäudeweit** *(leonis_engine)*
`circuit_zuordnung.py:65+80-81`: `letter_je_key` lauf-lokal, Reihenfolge des ersten Auftretens → gleiches Produkt kann OG1 'A' / UG 'C' heißen. Kandidat: persistente catalog_key→Letter-Map im Mehr-Geschoss-Runner; kein Contract-Bump (typ_letter existiert seit v1.2.0). Map je Projekt denken (Am Rain ist TYPENAME-genau, nicht artikelnummer-genau).

**GAP (mittel): Symbol-Beschriftung als Block-Attribute statt MTEXT+Leader** *(leonis_engine)*
`dxf_renderer.py:42+709-726` (LAYER_NODEID, freie MTEXT + Leader-Polyline) vs. din-Attributmodell (oben). Kandidat: ATTDEFs in die kanonische Library (`CAD_Symbole/Notbeleuchtungssymbole.dxf`) — luminaire_id→ID, typ_letter→TYPENUMBER, catalog_key/typ_name→TYPENAME auf 50/51/63-Sublayern (63 = unsere Konvention); MTEXT als Fallback. Löst die Label-Antikollisions-Klasse nebenbei. *Beleg-Korrektur aus Verdict:* GUID `99991ccb-…` gehört zu RZ_PU(13969.5,19996.9), nicht zur SPOT_SL(25152.9,17649.1) (dort `d5b87d08-…`).

**GAP (mittel): Tiefgaragen-Fahrgasse — kein SL-Band + keine sparsame RZ-Kette** *(leonis_engine)*
`bausteine.py:27` KORRIDOR_TYPEN={GANG,FLUR,KORRIDOR} ohne GARAGE; `deckung.py:16-17/187/282` feuert nur auf Korridoren; SL-12-GARAGE (`platzierung_regeln.yaml:523`) ist reine LB-Regel ohne Geometrie-Mechanismus. Kandidat: `fahrgassen_strategy` (Fahrgassen-Längsachse als Fluchtweg-Mittellinie → SL-Band quer + RZ nur an Stiegen-Zugängen/Brandabschnittsgrenzen; Achse aus Selman-Zirkulation, notfalls Bbox).

**GAP (mittel): Bestandslinien-Snap + Lux-Deckung enden am Korridor — STGH-SL fällt durch** *(leonis_engine)*
`mittellinie_snap.py:95-98` + `deckung.py` filtern beide auf KORRIDOR_TYPEN → STIEGENHAUS wird weder gesnappt noch lux-verdichtet. *Präzisierung aus Verdict:* es greifen §4.1.2a-Sonderstellen **plus** ein flacher 1-SL-Raum-Default (raumtyp_regeln, [ANNAHME]) — aber ohne Snap und ohne Lux-Nachweis, und der flache Default reproduziert den OG3-Flächenkontrast (31,50 → 1 SL / 12,74 → 0) gerade nicht. Kandidat: STIEGENHAUS in den Snap + STGH-SL lux-getrieben (OG3-Kontrast als Testfall).

**GAP (niedrig): Cluster-Extents + Multi-Insel-Warnung im Summary** *(leonis_engine)* — siehe 3.1; `_geschoss_extents` macht Single-Anker-Clustering, still ohne >1-Insel-Meldung.

**OWNER-FRAGEN-Findings** (R-K-Trigger, Gang-Tür-RZ in Lichtlinie einreihen, R-E-Wandausleger-Default, SIMA-Doppelwelt + Blocknull): kondensiert in Abschnitt 7. Zum Gang-Tür-RZ (OG2): beide RZ_PU auf y=17552.0 = Gangmitte (700/800 mm von beiden Wandfluchten, KEIN 150-mm-Wand-Offset; `_TUER_RZ_SNAP_FREI_MM=500` in `mittellinie_snap.py:87` nimmt Tür-RZ heute vom Snap aus); *Korrektur:* „exakt AUF der Leuchtenachse“ gilt nur RZ↔RZ (zur SL-Reihe 33/97 mm); Türebene nur 60–120 mm längs vom RZ.

## 4. Owner-Regel-Abgleich R-A..R-K (kondensiert, 6 Geschosse)

Legende: ✔=bestätigt, ✚=verfeinert, ∅=nicht prüfbar.

| Regel | UG | EG | OG1 | OG2 | OG3 | OG4 | Kern-Erkenntnis |
|---|---|---|---|---|---|---|---|
| **R-A** Struktur vor Platzierung | ✔ | ∅ | ✔ | ✔ | ✔ | ✔ | Ergebnis 6/6 auf dem Fluchtweg-Skelett (Fahrgasse/Gang/STGH/Nebenraum-Fluchttüren), Wohnungen leer; Prozess-Reihenfolge aus DXF nicht beweisbar. |
| **R-B** Piktogramm ins Rauminnere | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | Rotationen nur 0/90/180/270, xscale=1, türabhängig, widerspruchsfrei — ohne Blocknull-Konvention nicht verifizierbar → einmalige Owner-Sichtung. |
| **R-C** Tür-RZ raumseitig, kleiner Offset | ✔ | ∅ | ✔ | ✚ | ✔ | ∅ | Offsets ~300–430 mm zur Türstation (Größenordnung Referenzmaße 176/420); OG2-Verfeinerung: Gang-Tür-RZ kollinear mit dem nächsten Gang-RZ (eigene RZ-Achse ~46–48 mm neben Bestands-/SL-Linie), nicht Wand-Offset. Türseite offen (Blocknull). |
| **R-D** communal-Nebenraum-Tür-RZ | ✔✚ | ∅ | ∅ | ∅ | ∅ | ✚ | UG: Fahrradräume mit Tür-RZ + Spots, große zusätzlich Richtungs-RZ im Raum (Spot-Zuordnung teils raumübergreifend, s. Verworfen #5/#11); OG4-Umkehrschluss: PRIVATE AR/VR bleiben strikt leer. |
| **R-E** Schlussausgang-Dreifall | ∅ | ✚ | ∅ | ∅ | ∅ | ∅ | EG: JEDER Eingang bekommt CONCEPT-2-AP3-**Wandausleger** 1,0–1,6 m neben der Tür (auch unter VORDACH), Fall 3 kommt nicht vor — Spannung zu Fall 1 „mittig in der Überdachung“. |
| **R-F** Sichtkette statt Raster | ✚ | ✔ | ✔ | ✔ | ✔ | ✔ | Dichte aus Sichtlinien: EG-Lücke 30,381 m ≈ 30-m-Default; Kellergang 6,7-m-Takt; PLPR mittig in langen geraden Achsen; Wohnungstüren ohne RZ (Sichtbarkeit ersetzt Zeichen). |
| **R-G** Typ folgt Position | ✔ | ✔ | ✚ | ✔ | ✔ | ✚ | PU an Tür/Durchtritt, PL/PR/PLPR im Verlauf; Erweiterungen: PU auch am türlosen Stiegenantritt (OG4), PLPR wenn Zielraum verzweigt (Ost-Core). Caveat: UG-Fahrgasse hat 4 freie PU (>2 m von jeder Tür) — in der Garage nicht „ausnahmslos“ (s. Verworfen #2). |
| **R-H** Platzierung folgt Stiegen-Geometrie | ∅ | ∅ | ✔ | ✚ | ∅ | ✔ | 2-RZ-Template (PL rot90 Podest + PU rot0 Lauf, 3,19 m) mm-identisch je Core/Geschoss; OG4: PU 14 mm an der Laufachsen-LINE. Laufrichtungs-Beweis braucht Selman-Naht `Treppenlauf.richtung`. |
| **R-I** Rotation ≠ Gehrichtung | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Identisches Produkt in rot 0/90/180(/270) je Wandlage; Prüf-/Diff-Läufe dürfen PU-Rotation nie als Fluchtrichtung bewerten (OG4 nur 1 PU = Einzelpunkt, Variation in 5/6 zeigbar). |
| **R-J** SL = Lichtberechnung | ✔ | ∅ | ✔ | ✚ | ✚ | ✔ | Anzahl < Lückenzahl (2 Spots auf 7 Bestandslücken), STGH 31,50 m² 1 SL vs. 12,74 m² 0 SL, ~10-m-Band mit fixem Gerät; Position folgt dann R1/R6. |
| **R-K** Plan nötig? | ∅ | ✚ | ✚ | ✚ | ✚ | ✚ | din liefert IMMER ein Blatt je Geschoss (auch OG4 mit 3 Symbolen); Sparsamkeit sitzt in der Bestückung. Innerhalb des Geschosses: communal-Gang-Kriterium (OG1). R-K bleibt Owner-Orientierung/Hard-Stop, kein Automatismus. |

## 5. Verworfene Behauptungen (Transparenz)

1. **„R-I 6/6 Geschosse, alle Typ H“** — Koordinaten/Rotationen exakt, aber UG-Paar ist Typ I (nicht H) und OG4 (1 PU) kann Variation nicht belegen; haltbar nur als „5/6, Paar-genau“.
2. **„R-G gilt ausnahmslos: PU nur an Türen“** — vom UG widerlegt: 4 Fahrgassen-PU >2 m von jeder Tür/Treppe (z.B. 77413.8,30471.5) = PU als Verlaufszeichen in der Garage; Verfeinerungen (Stiegenantritt, PLPR) halten separat.
3. **„R-C: Tür-RZ exakt AUF der Gang-Lichtlinie“** — RZ liegen 48,1/45,9 mm NEBEN der Bestandsachse mit wechselndem Vorzeichen; exakt ist nur die RZ↔RZ-Kollinearität (eigene RZ-Achse).
4. **„3-RZ-STGH-Template“** — geklont ist nur das 2-RZ-Paar PL+PU (0,0001-mm-identisch); das dritte RZ existiert nur OG2/OG3 West und ist nicht geklont.
5. **„9-SPOT-Antipanik-Feld im 199,91-m²-Fahrradraum“** — Spot-Bbox 215 m² > Raumfläche; mind. 4 der 9 SPOTs liegen in Treppenhaus/Gang/KA-Gängen; korrekt wären ~4 SPOTs + 2 RZ_PL im Raum.
6. **„Layer-Split grün/gelb 100 % über alle Inserts, unabhängige V25-Bestätigung“** — Am Rain IST V25 (n=1); Split gilt ausnahmefrei nur für STANDARD_\*-Blöcke, SIMA/\*U65 folgen ihm nicht.
7. **„30,38-m-Lücke mit hinterleuchtetem BASIC 2 E-SIGN plus“** — Produktname für die EG-Kette unbelegt (STANDARD-Familie); „hinterleuchtet“ (Prämisse für z=200) nur Inferenz.
8. **„Flächen-Antipanik-Schwellen-Datenpunkte 100 vs. 200 m²“** — Raum-Zuordnung falsch (s. #5); real gleiche Spot-Dichte, kein Schwellen-Sprung.
9. **„Kellergang-Kette = einziger R-G-kritischer Fund“** — zweite strukturgleiche PU-Kette bei x=14832.9 existiert; Prüfscope war zu eng (Kernfrage bleibt, s. Abschnitt 7).
10. **„R-I-Beleg Typ H + Deckenaufbau (UG-Paar)“** — ATTRIBs real Typ I + MountingMethod „Wandaufbau“; Kernempfehlung hält, Beleg wie formuliert nicht.
11. **„Owner-Frage Nebenraum-Kipppunkt mit 9-SPOT-Prämisse“** — Prämisse wie #5 falsch; Frage mit korrigierten Zahlen (~2–3 Spots im Raum) neu stellen.
12. **„Enis-Praxis-Anker mit OG2-Werten 10,22/10,23/9,91 + Produktrollen aus JSON“** — OG2-Paarabstände sind 10.235/12.964/17.357/21.988 mm (9,91 existiert nicht dort); Produktnamen stehen nicht in den JSONs; Keller-„SL-Band“ waren RZ-Abstände; mit korrigierten Belegen (EG 9,73/9,99 + OG 10,02–10,23 + UG 10,1) neu formulierbar.

## 6. Regel-Kandidaten für die Engine

| # | Kandidat | Lane | Prio | Beleg (Kurz) |
|---|---|---|---|---|
| 1 | Bestands-Leuchten-Extraktor (`E_Beleucht*`-Layer-INSERTs, Extents-gefiltert) → `bestand_leuchten_mm` in `pipeline.run` durchreichen | leonis_engine | hoch | `pipeline.py:189+211` (run exponiert kwarg nicht); OG1-Raster 2500 mm y=9276.4, SPOT Δy=22 mm |
| 2 | `stgh_strategy.py`: 2-RZ-Modul (Richtungs-RZ am Hauptpodest + PU am Antritt) aus `Treppenlauf/Podest` | leonis_engine | hoch | `raum_modell.py:174-200` ungenutzt (grep=0); `fachpraxis.py:569`; Klon-Delta +2125,7/−2372,0 (OG1–OG3, beide Cores) |
| 3 | Selman: `laeufe/podeste` auf echten Plänen füllen (Antritt/Austritt aus Treppen-LINE, Richtung aus STG-Text/Geschosslogik) | selman_erkennung | hoch | OG4 LINE(13955.4,22060.2)→(13955.4,20100.3), PU 14,1 mm daneben; „8 STG 17/28“(14130.8,20897.2) |
| 4 | `richtung='gerade'`/PLPR an Verzweigungsknoten: `wasserscheiden()` in `anker_strategy` verdrahten; Trigger „Zielraum verzweigt nach Durchtritt“ (Owner bestätigen) | leonis_engine | hoch | `richtungsfeld.py:62-70` (0 Prod-Aufrufer); `anker_strategy.py:136-151`; `inserter.py:107`; OG1-3 PLPR (56350.8,9484.0) |
| 5 | Sichtkette bis Erkennungsweite strecken, 30-m-Obergrenze mit Toleranzhinweis (Insert-zu-Insert 30,381 m in der Referenz) | leonis_engine | hoch | `platzierer.py:71-77`, `sichtkette.py:80`; `en1838_grundwerte.yaml:52/:56`, `platzierung_regeln.yaml:243` |
| 6 | RZ an Brandabschnitts-/Rauchschutztür am Fluchtweg (decision_source referenz_praxis) + Tür als Sichtbarriere; auf `tuer_detail='brandschutztuer'` aufsetzen, EI-Klasse/Selbstschließer ergänzen | enis_norm + selman + leonis (3-Owner) | hoch | RZ-08 `platzierung_regeln.yaml:212-231`; `astv_arbeitsstaetten.yaml:242`; OG2 RZ_PU(32604.5,17552.0) „EI2 30-S200“; `sichtkette.py:21-23` |
| 7 | R-K-Trigger „communal-GANG zwischen Wohnungstüren und STGH“ als Referenz-Praxis-VORSCHLAG unter OIB (HS-03 fail-closed, nie `nicht_erforderlich`) | owner_frage → leonis | hoch | OG1 (9 Inserts nur Stiege 2+4); `oib_rl2_tabelle6.yaml:12-14/:135-150`; `platzierung_regeln.yaml:597-610` |
| 8 | Typ-Letter gebäudeweit: persistente catalog_key→Letter-Map über Geschosse (kein Contract-Bump) | leonis_engine | mittel | `circuit_zuordnung.py:65+80-81`; Typ H=9071090810 / Typ L=9069099300 stabil über 6 Geschosse |
| 9 | Labels als Block-ATTRIBs auf Sub-Layern (50/51/63) statt MTEXT+Leader; MTEXT-Fallback behalten | leonis_engine | mittel | `dxf_renderer.py:42+709-726`; `texte_notlicht_layer=[]` 6/6; ATTRIB-Layer-Mapping 50/51/99 |
| 10 | `fahrgassen_strategy` für GARAGE: SL-Band quer zur Fahrgassen-Achse + RZ nur an Zugängen/Brandabschnittsgrenzen | leonis_engine | mittel | `bausteine.py:27`, `deckung.py:16-17`; UG 16 SL y=30570.0 rot=270, Median 10,1 m; 3 PLPR in Bandlinie |
| 11 | STIEGENHAUS in Bestandslinien-Snap aufnehmen + STGH-SL lux-getrieben statt flachem 1-SL-Default | leonis_engine | mittel | `mittellinie_snap.py:95-98`; OG3-Kontrast 31,50 m² (1 SL) vs. 12,74 m² (0 SL); OG4-Spot in \*U43-Lücke |
| 12 | Anlagen-Symbole nur im Geschoss der Anlagentechnik rendern; „Anlage n“-Schema für circuit_hint | leonis_engine | mittel | 5× STANDARD_SYSTEM nur UG (Layer 11 fehlt in EG–OG4); INFOTEXT „Anlage 1–5“ |
| 13 | Cluster-Extents statt Header-EXTMIN/EXTMAX im Unterlage-Import + Warnung bei >1 Koordinaten-Insel; catalog_key nie aus din-Blocknamen | leonis_engine / selman | niedrig | UG extents [-9660,-146219,439322,58267] vs. SIMA x≈34,6 Mio; OG3 extents 34,75 km bei Symbolen 11–73 m |

## 7. Offene Owner-Fragen (max. 8, dedupliziert)

1. **SIMA_ET-Zweitwelt im UG** (45 SL + ~50 anonyme \*U14xx/\*U15xx-RZ + 5 „SiBel Zentrale“, georeferenziert x≈34,6 Mio mm, ATTRIBs nur GEBEZ/Z=1): Bestand/Fremdsystem oder gültiger Ausführungsstand? Welche Welt ist Referenz-maßgeblich, und sollen die \*U-Blöcke als Import-Vokabular digestet werden?
2. **Blocknull-Konvention der STANDARD_RZ_\*-Blöcke:** Wohin schaut das Piktogramm bei rot=0 (und die Pfeilachse von RZ_PL)? Eine einmalige AutoCAD-Sichtung macht R-B (und die R-C-Türseiten-Frage) an allen din-Referenzplänen maschinell prüfbar.
3. **R-K maschinell:** Dürfen wir „gemeinschaftlicher GANG-Raum zwischen Wohnungstüren und STGH vorhanden?“ als Trigger bauen (OG1: nur Stiege 2+4 bestückt; sonst 0 Symbole) — als Referenz-Praxis-Vorschlag, der den OIB-Befund (kein Umkehrschluss, HS-03 fail-closed) nie überschreibt? Oder bleibt R-K reiner Owner-Entscheid? Zusatz: existieren für Stiegen 1/3/5/6 separate Pläne/LB-Vorgaben?
4. **R-E-Ausführung:** Wandausleger-Antipanik (CONCEPT 2 AP 3 WA, „parallel zur Wand geschlossen“) 1,0–1,6 m NEBEN jeder Eingangstür — auch unter VORDACH — übernehmen, oder bei „mittig in der Überdachungsfläche“ bleiben (din dann als Alternativ-Ausführung dokumentieren)? Bestätigt Am Rain „jeder Eingang bekommt eine Vorbereichs-SL“ als Default (Fall 3 kam nicht vor)? Und: GEM.TERRASSE (107,61 m²) bewusst notlichtfrei (Dach-Sackgasse ≠ Fluchtweg)?
5. **SL-02-TREPPE (EN 1838 §4.1.2 b, BELEGT):** Hard-Anker behalten (Engine setzt in jedem STGH SL — läge über der Referenz-Praxis: STGH 12,74 m² hat bei din NULL SL) oder lichtberechnungsgesteuert wie Aufheller? Nicht still lockern — §4.1.2 ist normativ. Gibt es zu Am Rain die Lichtberechnungs-Unterlage (Relux/DIALux) als R-J-Beleg für das ~10-m-Band?
6. **Kellergang-PU-Ketten im UG** (y=8227.5, 6,7-m-Takt; zweite Kette x=14832.9): sitzen die PU an Abteil-/Zwischentüren (R-G-konform) oder frei im Gang (PU als Verlaufs-RZ → Keller-/Garagen-Ausnahme nötig, vgl. auch die 4 freien Fahrgassen-PU)? Tür-Kontext-Sichtung im DXF/AutoCAD.
7. **Anlagen- und Typenschlüssel:** Zuordnungstabelle „Anlage 1–5“ → Brandabschnitt/Stiege (direkt für circuit_hint/Anlagen-Labels verwertbar)? Wo liegt die Typenlegende (Layout-Blatt?) zum gebäudeweiten Typ-Letter-Schema — 1:1 in unsere #7-Stückliste übernehmen, Artikel-Attribute im Klartext statt #v1?
8. **PLPR-Trigger & Gang-Tür-RZ:** (a) Bestätigt der Ost-Core-Befund den Trigger „nach Durchtritt zwei Fluchtrichtungen ⇒ beidseitiges PLPR statt einfachem Pfeil“ (R-G(D)-Präzisierung)? (b) Gilt für GANG-seitige Tür-RZ die Praxis-Variante „mit dem nächsten Gang-RZ kollinear einreihen (Längs-Position an der Tür halten)“ statt des 150-mm-Wand-Offsets, während Raum-seitige Tür-RZ (Pflichträume) beim Offset bleiben?

## 8. Owner-Antworten (2026-09-12, Sichtungsblatt)

- **Frage 2 GEKLÄRT — Blocknull-Konvention:** Owner-Sichtung des EG-RZ_PU (9793.2,
  23965.9, rot=0): „Die RZ schaut in den Raum rein" — der bediente Raum liegt SÜDLICH
  → **STANDARD_RZ_PU bei rot=0 blickt nach −Y**. Identisch mit der Engine-Konvention
  (`bausteine.rotation_piktogramm_in_raum`, S1-Kalibrierung Elektroplan DE). R-B ist
  damit an allen din-Referenzplänen maschinell prüfbar (Checker-Kandidat).
- **Frage 6 GEKLÄRT — Keller-Verlaufs-PU:** Owner: „Die sind am Gang in der Mitte vom
  Gang, zwischen den Kellerabteilen" → die UG-PU-Ketten (y=8227.5, 6,7-m-Takt) sind
  **freie Verlaufs-RZ in Gangmitte**, KEINE Tür-RZ. Präzisiert R-G: im Keller/UG wird
  der Pfeil-unten-Block auch im Verlauf gesetzt (din-Praxis; Kandidat „kellergang_rz"
  — Kette in Gangmitte mit ~6–7-m-Takt, deutlich enger als die 30-m-Sichtweite).
- Frage 1 (SIMA_ET-Doppelwelt): offen, Detail-Sichtung angefordert.
