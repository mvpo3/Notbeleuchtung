# ANALYSE — Projekt 4 — Hausfeldstraße

Generiert aus `evidenz/Hausfeld/seitenprotokoll.jsonl` (83 Seiten-Records) — nicht von Hand editieren.

**Bilanz:** 59 bestätigt · 9 neu · 0 Widerspruch · 15 ohne Regelgehalt (Deckblatt/Legende/…)

## S.  1 — Notbeleuchtungen zeichnen – Hausfeldstraße (Deckblatt)
**Bereich:** Projekt 4 gesamt, UG·EG·1OG·1DG·2DG, Stiegen 1 und 2
**Bild:** Deckblatt mit einer dunklen Geschoss-Gesamtübersicht (Regelgeschoss mit grünen RIVO-Symbolen im Mittelgang). Mengenbilanz: 65 physische Leuchtenpositionen = 57 RZ + 3 Aufheller + 5 Antipanik-CAD-Zuordnungen, dazu 20 getrennt bilanzierte Legendenmuster. 58 räumlich erklärt, 7 mit lokaler Teilfrage, 0 unerklärbar.
> „Lern- und Prüfunterlage, keine behauptete Ausführungsfreigabe oder Anlagenabnahme.“
> „Alle grünen Wegfolgen sind lokal begründete Lehrinterpretationen; die dargestellten Menschen sind Beispiele, keine Belegungszahlen.“
**DXF-Abgleich:**  · Handles — · Deckblatt, kein Einzelnachweis; Mengen (65 Positionen) noch gegen die 5 RIVO-DXFs zu bilanzieren
**Bewertung:** kein_regelgehalt

## S.  2 — So finden Sie eine Leuchte
**Bereich:** Grundlagen / Lesekonvention
**Bild:** Reine Textseite: Erklärt Lehr-IDs (HF-…, verknüpft mit Quellhandle und RIVO-INSERT), Bildkennungen A/B/C, Personenkonvention P1a/P1b = dieselbe Person zu zwei Zeiten, P2 = andere Herkunft. Linienfarben: grün gestrichelt = geprüfte Lehrinterpretation, türkis gestrichelt = angenommener 2D-Blick, orange = begrenzter Nachweis.
> „Eine grüne Linie beschreibt den begehbaren Abschnitt, nicht die beleuchtete Fläche oder eine normgerechte Wegbreite.“
> „Linien durch Liftkabinen, Schächte oder Treppenaugen sind keine zulässige Fortsetzung.“
> „Leere Quellattribute wurden nicht mit erfundenen Stromkreisnummern gefüllt.“
**Linien:** grün gestrichelt / türkis gestrichelt / orange (Legende)
**DXF-Abgleich:**  · Handles — · Konventionsseite; deckt sich mit NB-R27 (Lift/Schacht nie Fortsetzung), aber selbst nur Legende
**Bewertung:** kein_regelgehalt

## S.  3 — Inhalt und Seiten
**Bereich:** Wegweiser / Inhaltsverzeichnis
**Bild:** Kapiteltabelle: UG ab S.6, EG ab S.33, 1OG ab S.46, 1DG ab S.53, 2DG ab S.60, geschossübergreifende Stiegenfolgen ab S.64, Quellen/Norm ab S.70, CAD-Prüfung ab S.78, Leuchtenindex ab S.80. Keine Planinhalte.
**DXF-Abgleich:**  · Handles — · 
**Bewertung:** kein_regelgehalt

## S.  4 — Wegweisung ist nicht Bodenbeleuchtung (Symbole und Konvention)
**Bereich:** Symbollegende RIVO_ARR_down/left/right, RIVO_Aufheller_Variante, RIVO_Antipanik
**Bild:** Legendenseite mit den 5 RIVO-Blöcken als Bildkacheln (grünes RZ mit Läufer/Pfeil, grüner Doppelkegel-Aufheller, weißes Antipanik-Rechteck). Kernaussage: der Down-Block wird als GANZER Block (Person, Pfeil, Rahmen, Balken) entgegen der örtlichen Gehbewegung gedreht, das Piktogramm wird nicht separat aufgerichtet; left/right erhalten KEINE pauschale Gegenrotation. RIVO_ARR_bothsided wurde geprüft, im Hausfeld-Bestand aber nicht benötigt.
> „Down – vollständiger Block dreht entgegen der örtlichen Gehbewegung. Weißer Balken zeigt zur Ankunft.“
> „Rechts – keine pauschale Gegenrotation wie beim Down-Zeichen.“
> „Der vollständige Down-Block wird einschließlich Person, Pfeil, Rahmen und Balken gedreht. Das Piktogramm wird danach nicht separat aufgerichtet.“
> „Der grüne Laufmensch stammt aus dem Original-Mollgasse-Block 750298750.“
**Leuchten im Bild:** RIVO_ARR_down down, RIVO_ARR_left left, RIVO_ARR_right right, RIVO_Aufheller_Variante aufheller, RIVO_Antipanik antipanik
**DXF-Abgleich:**  · Handles — · Blocknamen decken sich mit den in den *_RIVO.dxf verwendeten Blöcken (RIVO_ARR_right/down/left, RIVO_Aufheller_Variante); bothsided kommt im UG-Bestand nicht vor — konsistent
**Bewertung:** bestaetigt:NB-R06

## S.  5 — Eingaben, Planstände und Mengen
**Bereich:** Grundlagen / Datenquellen (5 Notbeleuchtungs-DXFs + 5 Vertrags-PDFs)
**Bild:** Textseite zu den Eingangsdaten: 5 Notbeleuchtungs-DXFs (DG-Datei dem 1DG zugeordnet; '5.Elektromontageplan 2DG_Index A.dxf' bytegleich zur 2DG-Datei, kein 6. Geschoss). Rohzählung 67 minus 2 Modell-Legenden außerhalb des Gebäudes = 65 physische Positionen; UG-RZ-Folge beginnt darum bei 002. Keine Xrefs; Header INSUNITS=6 wurde bewusst NICHT für eine Meter-Umrechnung verwendet, Türmaß-/Blockskalierungsvergleich belegt mm-Koordinaten.
> „Der Header INSUNITS=6 wurde nicht für eine automatische Meter-Umrechnung verwendet: Türmaß-/Blockskalierungsvergleich belegt mm-äquivalente Modellkoordinaten.“
> „Layout-/Dateinamen sind kein Beweis, dass nur eine Stiege enthalten ist: Die Pläne enthalten auch STGH2.“
> „Die anfängliche Rohzählung 67 enthielt zwei außerhalb des Gebäudes stehende UG-Modell-Legenden.“
**DXF-Abgleich:**  · Handles — · Bestätigt exakt die NB-R26-Datenfalle (INSUNITS kann lügen, über Türbreiten/Blockskala verifizieren); zusätzlich neue Falle: Legendenmuster im Modellraum außerhalb des Gebäudes verfälschen Rohzählungen
**Bewertung:** bestaetigt:NB-R26

## S.  6 · UG — UG – vorhandene Bereiche und Fälle
**Bereich:** UG-Geschossübersicht (Garage, Kellerflure FRR1/FRR2, Stgh 1, Stgh 2, Haustechnik)
**Bild:** Gesamtübersicht des UG-Plans (dunkle RIVO-Kopie mit Garagen-Stellplätzen, Kellerflur-Spangen und beiden Stiegenhäusern; grüne Symbole verstreut, nicht einzeln lesbar). Bilanz: 35 physische Positionen = 31 RZ + 1 Aufheller + 3 Antipanik. Szenenverzeichnis HF-UG-S01 bis HF-UG-S13 mit Seitenverweisen.
> „Menschen und Wege stehen in den nachfolgenden vergrößerten Szenen; die Übersicht ist kein lesbarer Einzelzeichennachweis.“
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles — · Evidenz-JSON zählt n_leuchten=37 im UG-DXF vs. 35 physische laut PDF — Differenz 2 = die beiden Modell-Legendenmuster (HF-UG-RZ-001/HF-UG-AP-001, S.5); konsistent
**Bewertung:** kein_regelgehalt

## S.  7 · UG — HF-UG-S01 · Westlicher Kellerflur: aus FRR 1.11 zur nördlichen Fortsetzung
**Bereich:** Westlicher Kellerflur, Kellerabteile FRR 1.05–1.12, Gang 39,36 m²
**Bild:** Szenenbild mit drei RZ (A unten an der SW-Ecke, B im westlichen Gang, C im mittleren Querflur) und Personen P1a (verlässt FRR 1.11), P1b (nach dem Nordknick) und P2 (kommt aus dem mittleren Querflur, türkiser Blickstrahl auf C). Grün gestrichelte Wegfolge läuft die untere Gangspange nach Westen und dann nach Norden; sie schneidet keinen Kellerraum. Detail A: RZ-004 als gedrehte Rechts-Variante an der Ecke, örtliche Richtungsinfo = nördliche Fortsetzung.
> „RZ-004 ist das erste Zeichen an der unteren westlichen Ecke. Es liegt neben der Stelle, an der die aus FRR 1.11 oder dem unteren Gang kommenden Personen von der Querbewegung in die Längsbewegung nach Norden wechseln.“
> „Die Lehrlinie endet nicht am Wandzeichen, sondern setzt sich auf der freien Gangfläche fort.“
> „Örtliche Grenze: Nicht schon aus dem Raum FRR 1.11 als sichtbar behauptet; davor liegt dessen Raumwand.“
**Leuchten im Bild:** (A) HF-UG-RZ-004 right, (B) HF-UG-RZ-002 right, (C) HF-UG-RZ-003 down
**Personen:** P1a/P1b: aus FRR 1.11, untere Gangspange nach Westen, dann Nord, P2: aus dem mittleren Querflur
**Linien:** grün gestrichelt + türkis gestrichelt
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6012E · 6012E = RIVO_ARR_right, welt_pfeil 90° (Nord) — passt zur beschriebenen nördlichen Fortsetzung; Lehr-Layer HF_LEHR_HF-UG-S01_* vorhanden (Kennungen 61413/61416/61419)
**Bewertung:** bestaetigt:NB-R07

## S.  8 · UG — HF-UG-S01 (Fortsetzung) · RZ-002 und RZ-003
**Bereich:** Westlicher Kellerflur + mittlerer Querflur
**Bild:** Gleiches Szenenbild wie S.7. Detail B: RZ-002 als Zwischen-RZ im langen Gang auf Höhe des mittleren Querarms, bestätigt die fortgesetzte Nordrichtung für P1b und den Anschluss für P2. Detail C: RZ-003 als Down-Typ, ganzer Block gedreht, Grundrisspfeil ostwärts = der westwärtigen Gehbewegung von P2 entgegen, langer Balken auf der Ankunftsseite = Frontansicht.
> „RZ-002 übernimmt den nächsten Orientierungsbezug im langen Gang.“
> „Der Down-Typ wird als ganzer Block so gedreht, dass sein Grundrisspfeil ostwärts und damit der Gehbewegung entgegen zeigt; der lange Balken liegt auf der Ankunftsseite.“
> „Das bedeutet die in der Vorlage erläuterte Frontansicht und keine reale Aufforderung zum Zurückgehen.“
**Leuchten im Bild:** (B) HF-UG-RZ-002 right, (C) HF-UG-RZ-003 down
**Personen:** P1b: im westlichen Gang nördlich der unteren Ecke, P2: aus dem mittleren Querflur westwärts
**Linien:** grün gestrichelt + türkis gestrichelt
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 600EE, 6010E · 600EE = RIVO_ARR_right welt 90° (Nord, Sichtketten-Zwischenglied); 6010E = RIVO_ARR_down welt 0° (Pfeil Ost = entgegen westwärtigem Strom) — beide decken die Textbeschreibung
**Bewertung:** bestaetigt:NB-R06

## S.  9 · UG — HF-UG-S02 · Westlicher Kellerflur: oberer Abzweig und Tür zum Stgh 1
**Bereich:** Oberer Querflur bei FRR 1.01–1.04, Wasserzählerbereich, DL100-Tür zum Stgh 1
**Bild:** Szenenbild: P1a/P1b kommen aus dem langen westlichen Gang, biegen bei A (RZ-005, Ecke) nach Osten, P1c läuft östlich an FRR 1.01 vorbei nach Norden zur DL100-Tür (grüner Pfeil oben). P2 kommt von Osten; B (RZ-006) liegt vor dieser Ankunft und zeigt als gedrehte Rechts-Variante die nördliche Fortsetzung. Zwei getrennte Einzel-RZ für zwei Ankunftsrichtungen statt eines beidseitigen Zeichens.
> „RZ-005 sitzt an der Ecke des langen Gangs. P1 sieht vor dem Richtungswechsel die für die Querbewegung nach Osten bestimmte Richtungsinformation.“
> „sie soll die Person nicht zum eigenen Montagepunkt an die Wand ziehen.“
> „Die Montage muss die für P2 zugeordnete Fläche tatsächlich lesbar machen; für P1 von Westen wird keine zweite bestätigte Schildseite erfunden.“
> „Örtliche Grenze: Beidseitige Lesbarkeit ist aus dem einseitig gezeichneten Symbol nicht belegt.“
**Leuchten im Bild:** (A) HF-UG-RZ-005 right, (B) HF-UG-RZ-006 right
**Personen:** P1a/P1b: aus dem langen westlichen Gang, P2: aus dem östlichen Querflur
**Linien:** grün gestrichelt + türkis gestrichelt
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6014E, 6016E · 6014E = RIVO_ARR_right welt 0° (Pfeil Ost = Querbewegung nach Osten); 6016E = RIVO_ARR_right welt 90° (Pfeil Nord = nördliche Fortsetzung) — beide wie beschrieben; kein bothsided-Block im Bestand
**Bewertung:** bestaetigt:NB-R07

## S. 10 · UG — HF-UG-S02 (Fortsetzung) · RZ-009 an der DL100-Tür
**Bereich:** DL100-Tür Kellerflur → Stgh 1-Vorbereich
**Bild:** Gleiches Szenenbild. Detail C: RZ-009 liegt direkt an der Türlinie der DL100-Tür. Down-Typ mit Vorderseite nach Süden (zur Lehrankunft P1c) und sichtbarem Grundrisspfeil entgegen der nördlichen Bewegung. Abgrenzung: RZ-009 bestätigt den konkreten Durchgang, RZ-006 den weiter entfernten Abzweig — zwei getrennte Aufgaben.
> „RZ-009 liegt direkt an der Türlinie.“
> „Der Down-Typ besitzt deshalb für diese Lehrankunft die Vorderseite nach Süden und den sichtbaren Grundrisspfeil entgegen der nördlichen Bewegung.“
> „Es bestätigt jetzt den konkreten Durchgang.“
**Leuchten im Bild:** (C) HF-UG-RZ-009 down
**Personen:** P1c: von Süden durch den schmalen Bereich östlich von FRR 1.01
**Linien:** grün gestrichelt
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 601CE · 601CE = RIVO_ARR_down welt 270° (Pfeil Süd = entgegen nördlicher Bewegung, Front zur Ankunft) — Tür-RZ in der Türachse wie NB-R01
**Bewertung:** bestaetigt:NB-R01

## S. 11 · UG — HF-UG-S03 · Stgh 1: E-Verteiler, Vorbereich und Aufheller beim Lift
**Bereich:** E-Verteilerraum (6,42 m²), Stgh 1-Vorbereich, Lift (Kabine 140x110), Stgh1 23,40 m²
**Bild:** Szenenbild: P1a verlässt den E-Verteilerraum durch die Nordtür unter A (RZ-007, Down-Typ an der Türlinie), P1b schwenkt im Vorbereich nach Westen (B, RZ-010 left). P2 kommt von der nördlichen Schleuse; C ist der runde Aufheller (Doppelkegel-Symbol) im Liftvorbereich. Die grüne Linie führt südlich um die Liftkabine herum — die Kabine wird nicht durchquert.
> „RZ-007 betreut konkret das Verlassen des E-Verteilerraums. Für P1 ist zunächst diese Tür und nicht das weiter entfernte Stiegenzeichen relevant.“
> „Das Down-Symbol wird zur südlichen Ankunft ausgerichtet; seine Pfeilgrafik steht gemäß Vorlagenkonvention gegen P1s nördlichen Durchgang.“
> „Die Kabine bleibt ein Hindernis in der Gehwegzeichnung und wird nicht durchquert.“
**Leuchten im Bild:** (A) HF-UG-RZ-007 down, (B) HF-UG-RZ-010 left, (C) HF-UG-SL-001 aufheller
**Personen:** P1a: aus dem E-Verteilerraum (Technikraum), P2: von der nördlichen Schleuse
**Linien:** grün gestrichelt
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6018E · 6018E = RIVO_ARR_down welt 270° (Front Süd, Pfeil gegen den nördlichen Durchgang) an der E-Verteiler-Nordtür — deckungsgleich mit der NB-R19-Technikraum-Türleuchte (Mollgasse: mittig, zugangsseitig)
**Bewertung:** bestaetigt:NB-R19

## S. 12 · UG — HF-UG-S03 (Fortsetzung) · RZ-010 und Aufheller SL-001 am Liftzugang
**Bereich:** Stgh 1-Vorbereich am Lift, Weg zum südwestlichen Stiegenfuß
**Bild:** Gleiches Szenenbild. Detail B: RZ-010 (left, Pfeil West) gibt im Vorbereich rechts vom Lift die westliche Weiterführung zum Stiegenfuß an — Richtungswechsel-Zeichen, nicht Türfunktion. Detail C: SL-001 = RIVO_Aufheller_Variante am Knoten aus nördlichem Schleusenanschluss, Liftvorbereich und Bewegung zum Stiegenfuß; Aufgabe ist Flächenaufhellung der benutzten Vorbereichsfläche, keine Richtungsaussage; ersetzt weder RZ-007 noch RZ-010. Sicht durch den Liftschacht wird nicht eingezeichnet.
> „RZ-010 liegt im Vorbereich rechts vom Lift und gibt die westliche Weiterführung in Richtung Stiegenfuß an.“
> „Die Leuchte soll die benutzte Vorbereichsfläche erkennbar machen; sie ersetzt weder RZ-007 an der Raumtür noch RZ-010 als Richtungsinformation.“
> „Örtliche Grenze: Photometrie und Montagehöhe fehlen; die Ausleuchtung des Stiegenlaufs ist durch diese Position allein nicht nachgewiesen.“
> „Örtliche Grenze: Für die nördliche Ankunft von P2 ist die tatsächliche Front-/Rückseitenmontage nicht nachgewiesen; deshalb kein bestätigter Blickstrahl von P2.“
**Leuchten im Bild:** (B) HF-UG-RZ-010 left, (C) HF-UG-SL-001 aufheller
**Personen:** P1b: nach Türdurchtritt im Vorbereich, P2: von der nördlichen Schleuse
**Linien:** grün gestrichelt
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 601EE, 6020E · 601EE = RIVO_ARR_left welt 180° (Pfeil West = Weiterführung zum Stiegenfuß); 6020E = RIVO_Aufheller_Variante im Vorbereich am Lift — beide wie beschrieben; Lift bleibt Hindernis (deckt NB-R27)
**Bewertung:** neu → Trifft in einem Stiegenhaus-Vorbereich der Zugang von Schleuse/Gang, der Liftzugang und der Weg zum Stiegenfuß zusammen, wird dort zusätzlich zu Tür-RZ und Richtungs-RZ EIN runder Aufheller (RIVO_Aufheller_Variante) zur Flächenaufhellung der Knotenfläche gesetzt — ohne Richtungsaussage, ersetzt kein RZ; Lux-/Stiegenlauf-Nachweis bleibt separat (lux_nachweis_erforderlich). Nachrangige Ergänzung zu NB-R09/NB-R14; kein Widerspruch zur Mollgasse-Basis.

## S. 13 · UG — Stgh 1: aus KiWa und Vorbereich zum unteren Stiegenlauf
**Bereich:** KiWa-Raum + Stgh-1-Vorbereich, unterer Stiegenlauf westlich des Lifts
**Bild:** KiWa-Raum (12,11 m²) und Stgh-1-Vorbereich mit 18-STG-Lauf. P1a verlaesst KiWa durch die suedliche Tuer unter (A)=RZ-011, P2 kommt aus dem Foyer; beide gruene Linien vereinigen sich vor der unteren Stufenkante bei (B)=RZ-008. Orangenes '?' markiert eine oertliche Luecke noerdlich von B. Beide Zeichen sind Down-Bloecke, Pfeil entgegen der Gehbewegung.
> „Die Person aus KiWa benutzt die suedliche Tuer unter RZ-011.“
> „Fuer den hier dargestellten Eintritt in den annaehernd nordwaerts gerichteten Lauf zeigt der vollstaendige Down-Block mit seinem Grundrisspfeil nach Sueden.“
> „Die urspruengliche numerische Fremdblockrotation wird nicht blind uebernommen.“
**Leuchten im Bild:** (A) down, (B) down
**Personen:** KiWa (P1a/P1b), Foyer (P2)
**Linien:** gruen gestrichelt = Lehrinterpretation beider Stroeme, tuerkis = 2D-Blick auf A, orange ? = oertliche Luecke
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6012E, 6014E, 6018E, 60210, 60290, 602D0, 60310, 604D0, 60330, 60390, 60430, 604B0, 60490, 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470 · A=60210 RIVO_ARR_down welt_pfeil 90° (Pfeil nach Nord in den Raum, Bewegung sued — deckt Text); B=601AE RIVO_ARR_down welt_pfeil 266,95° (Pfeil nach Sued, Bewegung nord).
**Bewertung:** bestaetigt:NB-R01

## S. 14 · UG — Stgh 1: aus KiWa und Vorbereich zum unteren Stiegenlauf (Fortsetzung)
**Bereich:** Untere Stufenkante westlich des Lifts, Stgh 1
**Bild:** Gleiches Bild wie S.13. Fokus (B)=RZ-008 an der Naht vom ebenen Vorbereich zum unteren Stiegenlauf. Letzte oertliche Bewegung vor Laufeintritt annaehernd nach Norden; die Down-Front wird zur suedlichen Ankunft gedreht. Eine alte Fremdrotation von ca. 176,95° wird ausdruecklich als Unterschied dokumentiert und nicht uebernommen.
> „Dafuer wird die Front des Down-Typs zur suedlichen Ankunft gedreht.“
> „Die neue CAD-Darstellung folgt der bestaetigten Gegenrichtungsregel und dem dargestellten oertlichen Gehabschnitt, nicht einer pauschalen Drehung aller Zeichen.“
> „kein kuenstlicher Weg durch Planleerraum“
**Leuchten im Bild:** (B) down
**Personen:** KiWa + Foyer (vereinigt)
**Linien:** gruen gestrichelt vereinigte Fluchtlinien, orange ? als offene Zwischenpodest-Zuordnung zum EG
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470 · 601AE RIVO_ARR_down welt_pfeil 266,95° = Grundrisspfeil nach Sued, Front zum ankommenden Nord-Strom; dokumentierte Alt-Rotation 176,95° im DXF nicht mehr vorhanden — deckt Text.
**Bewertung:** bestaetigt:NB-R06

## S. 15 · UG — Haustechnik: Aufhellung des Raums und Austritt in die Schleuse
**Bereich:** Haustechnik (30,70 m²) mit oestlicher Tuer zur Schleuse, STGH1/1.2
**Bild:** P1a geht auf freier Raumflaeche der Haustechnik zur vorhandenen oestlichen Tuer; eine ausgemauerte Oeffnung daneben wird nicht als Passage benutzt. (A)=AP-002 ist eine rechteckige Bestands-Sicherheitsleuchte mitten im Raum, der das RIVO-Antipanik-Symbol zugeordnet wird — reine Beleuchtungsaufgabe ohne Richtungspfeil. (B)=RZ-014 bezeichnet den Tuerdurchgang in die Schleuse.
> „Die rechteckige Sicherheitsleuchte erhaelt das RIVO-Antipanik-Symbol nach der vereinbarten grafischen Zuordnung.“
> „ein Richtungspfeil gehoert nicht zu dieser Leuchte“
> „Rechnerischer Nachweis der tatsaechlich vorgesehenen Beleuchtungsfunktion fehlt; aus 30,70 m² folgt hier keine behauptete allgemeine Pflicht.“
**Leuchten im Bild:** (A) antipanik, (B) down
**Personen:** Haustechnik (P1a/P1b)
**Linien:** gruen gestrichelt Weg quer durch den Raum zur oestlichen Tuer, ausgemauerte Oeffnung ausgelassen
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6012E, 6014E, 6018E, 60210, 60290, 602D0, 60310, 604D0, 60330, 60390, 60430, 604B0, 60490, 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470 · A=60290 RIVO_Antipanik (typ antipanik, ohne welt_pfeil) auf der Bestandsleuchte; B=60270 RIVO_ARR_down welt_pfeil 176,95° — deckt Text.
**Bewertung:** neu → Rechteckige Bestands-Sicherheitsleuchte in UG-Nebenraum (Haustechnik) wird der Symbolfamilie RIVO_Antipanik zugeordnet: Beleuchtungsaufgabe (Raum-/Zugangserkennbarkeit) ohne Richtungspfeil; ob Antipanikfunktion oder Rettungswegbeleuchtung, entscheidet erst der Lux-Nachweis, nicht die Legende (erweitert NB-R10/NB-R19).

## S. 16 · UG — Haustechnik: Aufhellung des Raums und Austritt in die Schleuse (Fortsetzung)
**Bereich:** Oestliche Haustechnik-Tuer zur Schleuse
**Bild:** Gleiches Bild wie S.15. Fokus (B)=RZ-014 an der vorhandenen seitlichen Tuer: P1b bewegt sich annaehernd ostwaerts in die Schleuse, die Down-Front wird nach Westen zur Ankunft gelegt. Der ganze Block behaelt die leichte Schraeglage der oertlichen Passage. Nach der Tuer folgt kein sicherer Aussenbereich, sondern die naechste Entscheidung an der suedlichen Schleusentuer.
> „Die Front des Down-Blocks wird deshalb nach Westen zur Ankunft gelegt; der ganze Block behaelt die leichte Schraeglage der oertlichen Passage.“
> „Nach der Tuer folgt nicht unmittelbar ein sicherer Aussenbereich, sondern die naechste Entscheidung an der suedlichen Schleusentuer.“
**Leuchten im Bild:** (B) down
**Personen:** Haustechnik (P1b)
**Linien:** gruen gestrichelt bis zur Tuer, Fortsetzung in S06 referenziert
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470 · 60270 RIVO_ARR_down welt_pfeil 176,95° = Pfeil nach West (leicht schraeg, Passage-Schraeglage im DXF sichtbar), Front zum ankommenden Ost-Strom — deckt Text.
**Bewertung:** bestaetigt:NB-R01

## S. 17 · UG — Westliche Garage: am Rampenknick zur Schleuse des Stgh 1
**Bereich:** Westliche Garagengasse, Rampenknick, Schleuse Stgh 1
**Bild:** P1 laeuft in der freien Garagengasse nach Norden ((A)=RZ-016 haelt die Orientierungsfolge), bei (B)=RZ-015 uebernimmt ein Linkszeichen den westlichen Anschluss zur Schleuse; (C)=RZ-013 markiert den Eintritt in die Schleuse, (D)=RZ-012 die zweite, suedliche Schleusentuer. Die Linie fuehrt noerdlich am Stuetzenbereich vorbei; P1a bleibt links der Stellflaechen und muss nicht zum Leuchtensymbol neben der Fahrzeugdarstellung laufen.
> „Die beiden Zeichen gehoeren damit zu zwei verschiedenen Tuerflaechen; ein einziger Pfeil mitten in der Garage koennte diesen zweistufigen Anschluss nicht gleichwertig erklaeren.“
> „Die Down-Front wird zur suedlichen Gassenankunft gelegt.“
> „Ein eingezeichnetes Fahrzeug beweist weder eine freie reale Sicht unter der Leuchte noch deren Montagehoehe.“
**Leuchten im Bild:** (A) down, (B) left, (C) down, (D) down
**Personen:** westliche Garagengasse (P1a/P1b/P1c)
**Linien:** gruen gestrichelt lange Gassenlinie mit Westknick zur Schleuse, tuerkis 2D-Blick auf A
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6012E, 6014E, 6018E, 60210, 60290, 602D0, 60310, 604D0, 60330, 60390, 60430, 604B0, 60490, 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470, 6010E, 601CE, 6020E, 60250, 60510, 60370, 603D0, 603F0, 60450, 60230 · A=602D0 RIVO_ARR_down welt_pfeil 270° = Pfeil nach Sued, Front zur suedlichen Ankunft — deckt Text; Gassenfuehrung neben Stellflaechen deckt zusaetzlich NB-R17.
**Bewertung:** bestaetigt:NB-R06

## S. 18 · UG — Westliche Garage: am Rampenknick zur Schleuse des Stgh 1 (Fortsetzung)
**Bereich:** Rampenknick + garagenseitige Schleusentuer Stgh 1
**Bild:** Fokus (B)=RZ-015: Linkszeichen am Uebergang zum westlichen Schleusenanschluss; die Rampe liegt rechts, der Weg wird um den Stuetzenbereich gefuehrt. Aus dem Rampengefaelle wird ausdruecklich KEINE Fluchtrichtung und aus der Rampenfortsetzung kein bestaetigter sicherer Aussenort abgeleitet. (C)=RZ-013 sitzt an der garagenseitigen westlichen Tuer, Down-Front zur oestlichen Ankunft, Durchgang leicht schraeg.
> „Aus dem Rampengefaelle wird keine Fluchtrichtung und aus der Rampenfortsetzung kein bestaetigter sicherer Aussenort abgeleitet.“
> „Benutzbarkeit und vollstaendiges Fluchtwegkonzept der Rampe sind nicht bestaetigt.“
> „Der oertliche Durchgang ist annaehernd westwaerts und leicht schraeg. Die Down-Front zeigt daher zur oestlichen Ankunft.“
**Leuchten im Bild:** (B) left, (C) down
**Personen:** Garagengasse (P1b/P1c)
**Linien:** gruen gestrichelt um den Stuetzenbereich zur Tuer; Rampe ohne Fluchtlinie
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470, 6010E, 601CE, 6020E, 60250, 60510, 60370, 603D0, 603F0, 60450 · B=602B0 RIVO_ARR_left welt_pfeil 180° = Pfeil nach West (Fluchtrichtung aus Sicht, NB-R07 gedeckt); C=60250 RIVO_ARR_down welt_pfeil 356,95° = Pfeil nach Ost, Front zur oestlichen Ankunft — deckt Text.
**Bewertung:** neu → Garagenrampe ist NICHT automatisch Fluchtweg: aus Rampengefaelle keine Fluchtrichtung ableiten, Rampenfortsetzung nicht als sicherer Aussenort werten, solange Benutzbarkeit/Konzept unbestaetigt; Fluchtfuehrung stattdessen ueber den Schleusenanschluss (ergaenzt NB-R17 um die Rampen-Flaeche).

## S. 19 · UG — Westliche Garage: am Rampenknick zur Schleuse des Stgh 1 (Fortsetzung)
**Bereich:** Suedliche Schleusentuer in den Stgh 1-Vorbereich
**Bild:** Fokus (D)=RZ-012: zweite Tuer der Schleuse. Nach Eintritt ueber RZ-013 oder aus der Haustechnik fuehrt der Durchgang aus der Schleuse nach Sueden in den Stgh 1-Vorbereich; der Down-Block wird mit der Front zur noerdlichen Ankunft orientiert. Danach folgen Aufhellerbereich und Stiegenfuss (S03/S04). Jede der beiden Schleusentueren traegt ihr eigenes RZ.
> „Der gezeichnete Durchgang fuehrt aus der Schleuse nach Sueden in den Stgh 1-Vorbereich. Der Down-Block wird mit seiner Front zur noerdlichen Ankunft orientiert.“
**Leuchten im Bild:** (D) down
**Personen:** Schleuse (nach RZ-013 bzw. Haustechnik)
**Linien:** gruen gestrichelt Suedwendung innerhalb der Schleuse bis in den Vorbereich
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 60230 · D=60230 RIVO_ARR_down welt_pfeil 86,95° = Pfeil nach Nord, Front zum von Norden ankommenden Strom, Bewegung sued — deckt Text.
**Bewertung:** bestaetigt:NB-R01

## S. 20 · UG — Westliche Garagengasse: Orientierung zwischen den Stellflaechen
**Bereich:** Westliche Garagengasse, Stellplatzreihen PP 03-PP 07
**Bild:** Beispielperson bleibt in der freien Gasse zwischen den Fahrzeugreihen, kein Weg quer durch Stellplaetze. (A)=RZ-018 ist der erste Zeichenbezug fuer die nordwaerts gerichtete Bewegung von P1a, (B)=RZ-017 folgt weiter noerdlich an derselben langen Gasse. Die Wiederholung ist raeumlich begruendet, die Weiterfuehrung zeigt S06 am Rampenknick.
> „Hier sehen wir keinen Weg quer durch Stellplaetze. Die Beispielperson bleibt in der freien Gasse zwischen den Fahrzeugreihen.“
> „Der Down-Block wird so gedreht, dass seine Front zur suedlichen Ankunft weist; die Pfeilgrafik zeigt nach der vereinbarten CAD-Konvention entgegengesetzt.“
**Leuchten im Bild:** (A) down, (B) down
**Personen:** suedliche Garagengasse (P1a/P1b)
**Linien:** gruen gestrichelt gerade Nordlinie durch die Gasse, tuerkis 2D-Blicke auf A und B
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6012E, 6014E, 6018E, 60210, 60290, 602D0, 60310, 604D0, 60330, 60390, 60430, 604B0, 60490, 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470 · A=60310 RIVO_ARR_down welt_pfeil 270° = Pfeil nach Sued, Front zur suedlichen Ankunft — deckt Text; Gassenfuehrung deckt NB-R17.
**Bewertung:** bestaetigt:NB-R06

## S. 21 · UG — Westliche Garagengasse: Orientierung zwischen den Stellflaechen (Fortsetzung)
**Bereich:** Mittlerer Abschnitt der westlichen Garagengasse (Beschriftung Garage und Rampe)
**Bild:** Fokus (B)=RZ-017 als naechster Orientierungsbezug der langen Gasse: hier wird noch die gerade Fortsetzung erklaert, erst weiter noerdlich der Abzweig zur Schleuse (Linkszeichen RZ-015 in S06). P1b bleibt neben und nicht innerhalb der gezeichneten Stellflaechen. RZ-018 und RZ-017 bilden eine folgerichtige Kette entlang derselben Gasse.
> „Hier wird noch die gerade Fortsetzung erklaert, erst weiter noerdlich der Abzweig zur Schleuse.“
> „Erkennungsweite und moegliche Sichtbehinderungen durch abgestellte Fahrzeuge benoetigen reale Montage-/Nutzungsdaten.“
**Leuchten im Bild:** (B) down
**Personen:** Garagengasse (P1b)
**Linien:** gruen gestrichelt Fortsetzung der Gassenlinie nach Norden
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470 · B=602F0 RIVO_ARR_down welt_pfeil 270° = Pfeil nach Sued, Front zum ankommenden Strom; Folgezeichen in einer Kette RZ-018→RZ-017→RZ-015 — deckt Text.
**Bewertung:** bestaetigt:NB-R12

## S. 22 · UG — Oestliche Garage: von der Laengsgasse zum Zugang des Stgh 2
**Bereich:** Oestliche Garagen-Laengsgasse + noerdlicher Queranschluss zum Stgh 2
**Bild:** P1 folgt der oestlichen Laengsgasse nordwaerts: (A)=RZ-030 erklaert die gerade Fortsetzung (noch kein Tuerzeichen, Schleusenzugang liegt weiter noerdlich und seitlich versetzt), am noerdlichen Querbereich uebernimmt (B)=RZ-031 als Linkszeichen den Wechsel nach Westen oberhalb der Stellplaetze. P2 kommt aus der westlichen Querzone; fuer diese Ankunft zeigt (C)=RZ-032 die Nordwendung zur Schleusentuer.
> „Der Down-Typ hat fuer diese Ankunft die Front nach Sueden. Er ist noch kein Tuerzeichen: Der tatsaechliche Schleusenzugang liegt deutlich weiter noerdlich und seitlich versetzt.“
> „Danach folgt die Schleusentuer RZ-019; eine Linie quer durch die noerdlich davor gezeichneten Fahrzeuge waere keine gleichwertige Erklaerung.“
**Leuchten im Bild:** (A) down, (B) left, (C) left
**Personen:** oestliche Laengsgasse (P1a/P1b), westliche Querzone (P2)
**Linien:** gruen gestrichelt Laengsgasse mit Westknick oberhalb der Stellplaetze, zweite Linie von Westen
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6012E, 6014E, 6018E, 60210, 60290, 602D0, 60310, 604D0, 60330, 60390, 60430, 604B0, 60490, 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470, 6010E, 601CE, 6020E, 60250, 60510, 60370, 603D0, 603F0, 60450 · A=604D0 RIVO_ARR_down welt_pfeil 270° = Pfeil Sued, Front zur Sued-Ankunft (NB-R06); B=604F0 RIVO_ARR_left welt_pfeil 180° = Pfeil West = Fluchtrichtung aus Sicht (NB-R07) — deckt Text.
**Bewertung:** bestaetigt:NB-R06

## S. 23 · UG — Oestliche Garage: von der Laengsgasse zum Zugang des Stgh 2 (Fortsetzung)
**Bereich:** Querzone suedlich des Schleusenzugangs Stgh 2
**Bild:** Fokus (C)=RZ-032 fuer die zweite Herkunft: P2 kommt von Westen und schwenkt nach Norden zum Zugang ein; der gedrehte Links-Typ vermittelt die Nordrichtung. Ausdruecklich festgehalten: das ist NICHT dieselbe Frontansicht wie fuer P1s oestliche Ankunft; es wird keine unbelegte beidseitige Montage angenommen, die Lesbarkeit fuer die Gegenankunft bleibt gesondert zu pruefen.
> „Der gedrehte Links-Typ vermittelt dafuer die Nordrichtung. Das ist nicht dieselbe Frontansicht wie P1s oestliche Ankunft.“
> „Keine unbelegte beidseitige Montage angenommen; Blickbezug nur fuer die dargestellte westliche Ankunft.“
**Leuchten im Bild:** (C) left
**Personen:** westliche Querzone (P2)
**Linien:** gruen gestrichelt Westankunft mit Nordschwenk, tuerkis 2D-Blick auf C
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6010E, 601CE, 6020E, 60250, 60510, 60370, 603D0, 603F0, 60450 · C=60510 RIVO_ARR_left welt_pfeil 90° = Pfeil Nord (Fluchtrichtung aus Sicht der Westankunft); im DXF 0 beidseitig-Gruppen im UG — deckt die Zurueckhaltung des Texts.
**Bewertung:** bestaetigt:NB-R16

## S. 24 · UG — Stgh 2: aus der Garage durch zwei Schleusentueren
**Bereich:** Stgh-2-Schleuse (4,11 m²) + Stgh 2-Vorbereich, STGH2/2
**Bild:** Zweistufiger Anschluss aus der Garage: P1a geht durch die suedliche Tuer unter (A)=RZ-019 in die Schleuse, aendert dort die Richtung und benutzt die oestliche Tuer unter (B)=RZ-020; erst P1c steht im Stgh 2-Vorbereich, wo (C)=RZ-021 die noerdliche Weiterbewegung zum linken Stiegenpodest (18 STG) anzeigt. Die drei Personen sind aufeinanderfolgende Positionen derselben Beispielperson. Jede Schleusentuer traegt ihr eigenes RZ; RZ-020 wird nicht mit RZ-019 zu einer geraden Tuerfolge zusammengefasst.
> „Die Front des Down-Blocks liegt zur Garage hin; nach der Nutzerkonvention zeigt die gesamte Pfeilgrafik der Gehbewegung entgegen.“
> „Die Leuchte ist nicht mit RZ-019 zu einer vermeintlich geraden Tuerfolge zusammenzufassen.“
**Leuchten im Bild:** (A) down, (B) down, (C) left
**Personen:** Garage (P1a→P1b→P1c, dieselbe Person)
**Linien:** gruen gestrichelt zweistufiger Weg durch die Schleuse mit Richtungswechsel, tuerkis 2D-Blicke
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6012E, 6014E, 6018E, 60210, 60290, 602D0, 60310, 604D0, 60330, 60390, 60430, 604B0, 60490, 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470, 6010E, 601CE, 6020E, 60250, 60510, 60370, 603D0, 603F0, 60450 · A=60330 RIVO_ARR_down welt_pfeil 270° (Pfeil Sued zur Garage, Bewegung nord); B=60350 RIVO_ARR_down welt_pfeil 180° (Pfeil West, Bewegung ost); C=60370 RIVO_ARR_left welt_pfeil 90° (Pfeil Nord = Weiterrichtung) — alle decken den Text.
**Bewertung:** bestaetigt:NB-R01

## S. 25 · UG — Stgh 2: aus der Garage durch zwei Schleusentüren (FORTSETZUNG)
**Bereich:** Stgh 2-Vorbereich / Schleuse (4,1 m²) / Garagenanschluss
**Bild:** P1a kommt aus der Garage von Süden zur Tür-Leuchte (A), P1b durchquert die Schleuse zur zweiten Schleusentür (B), P1c steht hinter der Schleuse und wendet nach Norden zum linken Stiegenpodest (18 STG, 18/27). RZ-021 (C) ist eine gedrehte Links-Variante und vermittelt die Nordwendung. Die grüne Folge läuft links am Symbolstandort vorbei und endet nicht am Zeichenmittelpunkt.
> „RZ-021 gibt nach dem zweiten Türdurchgang die Nordwendung zum linken Stiegenpodest an.“
> „die gedrehte Links-Variante vermittelt die weiterführende Richtung“
> „Die Person geht auf dem Boden links am Symbolstandort vorbei und endet nicht am Zeichenmittelpunkt.“
**Leuchten im Bild:** (A) down, (B) down, (C) left
**Personen:** P1a aus der Garage (Süden), P1b in der Schleuse, P1c hinter der Schleuse
**Linien:** Grün gestrichelte Wegfolge Garage->Schleuse->Podest; türkise 2D-Blick-Linien von P1c zu C; keine Orange-Markierung auf dieser Seite
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6012E, 6014E, 6018E, 60210, 60290, 602D0, 60310, 604D0, 60330, 60390, 60430, 604B0, 60490, 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470, 6010E, 601CE, 6020E, 60250, 60510, 60370, 603D0, 603F0, 60450 · Szene-9-Kennungen A/B/C auf nächste Leuchten gemappt: A=60330 (RIVO_ARR_down, Welt-Pfeil 270), B=60350 (RIVO_ARR_down, Welt-Pfeil 180), C=60370 (RIVO_ARR_left, Welt-Pfeil 90 = Nordwendung wie beschrieben)
**Bewertung:** bestaetigt:NB-R07

## S. 26 · UG — Stgh 2: Vorbereich am Lift und Einstieg in den Stiegenlauf
**Bereich:** STGH 2 (31,01 m²) / Liftvorbereich / Treppenkopf
**Bild:** Freier Vorbereich südlich des Treppenkörpers: P1a/P1b läuft von der Liftseite um die sichtbare Stiege herum zum linken Podest, P2 kommt aus Richtung Schleuse. Die grüne Linie läuft weder durch die Liftkabine noch quer über das Treppenauge. RZ-022 (A, Linkszeichen) ordnet die westliche Weiterbewegung zu, RZ-023 (B, gedrehte Rechtsvariante südwärts) den Weg um den östlichen Treppenkörper; für beide bleibt die real gelesene Zeichenfläche mangels Montageangabe offen (orangenes X und ? am Treppenauge markieren die örtliche Lücke).
> „die Linie läuft weder durch die Kabine noch quer über das Treppenauge“
> „Es führt damit zur linken Podestentscheidung, nicht in die rechts liegende Kabine.“
> „lässt sich ohne Montage-/Schnittzuordnung nicht sicher festlegen [...] keine fiktive beidseitige Lesbarkeit“
**Leuchten im Bild:** (A) left, (B) right, (C) right
**Personen:** P1a aus dem Liftvorbereich (Osten), P1b (gleiche Person, 2/2), P2 aus Richtung Schleuse (Westen)
**Linien:** Grün gestrichelte Bögen um den Treppenkörper; grüner Pfeil bei C zum orangen X am 18-STG-Lauf; türkise 2D-Blick-Annahmen; orange = örtliche Lücke (Montage unbelegt)
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6012E, 6014E, 6018E, 60210, 60290, 602D0, 60310, 604D0, 60330, 60390, 60430, 604B0, 60490, 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470, 6010E, 601CE, 6020E, 60250, 60510, 60370, 603D0, 603F0, 60450 · Szene-10: A=60390 (RIVO_ARR_left, Welt-Pfeil 180 = westliche Weiterbewegung), B=603B0 (RIVO_ARR_right, Welt-Pfeil 270 = südwärts wie 'Rechtsvariante zeigt im Grundriss südwärts')
**Bewertung:** bestaetigt:NB-R27

## S. 27 · UG — Stgh 2: Vorbereich am Lift und Einstieg in den Stiegenlauf (FORTSETZUNG)
**Bereich:** STGH 2 / linkes Podest vor dem 18-Stufen-Lauf
**Bild:** Gleicher Bildausschnitt wie S.26. Behandelt wird RZ-024 (C): P2 erreicht das Zeichen aus dem südlichen Vorbereich, die Rechtsinformation gehört zur ostwärts gerichteten Fortsetzung auf den sichtbaren Stiegenlauf. Anders als RZ-021 hinter der Schleuse bestätigt RZ-024 den tatsächlichen Einstieg am Podest; die Folge endet auf dem belegbaren unteren Lauf, das EG-Bild übernimmt den Geschosswechsel.
> „Die Rechtsinformation gehört hier zur ostwärts gerichteten Fortsetzung auf den sichtbaren Stiegenlauf.“
> „bestätigt RZ-024 den tatsächlichen Einstieg am Podest“
> „HF-N03: § 4.1.2 a–c [...] Türen, Stufen und Niveauwechsel hervorheben“
**Leuchten im Bild:** (C) right
**Personen:** P2 aus dem südlichen Vorbereich
**Linien:** Grüner Pfeil von C ostwärts auf den Lauf, endet am orangen X (Geschosswechsel dort nicht weitergezeichnet); türkise Blick-Linie P2->C
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6010E, 601CE, 6020E, 60250, 60510, 60370, 603D0, 603F0, 60450 · Szene-10 C=603D0 (RIVO_ARR_right, Welt-Pfeil 0 = ostwärts in Aufstiegsrichtung des Laufs, passt zu NB-R05/NB-R13: UG-Strom flieht hinauf, Pfeil in Laufrichtung)
**Bewertung:** bestaetigt:NB-R05

## S. 28 · UG — Nördlicher Stgh 2-Anschluss: KiWa, E-Verteiler und Verbindungsflur
**Bereich:** KIWA (16,66 m²) / E-Verteilerraum (6,13 m²) / Verbindungsflur westlich der Wohnungstrennwand
**Bild:** Drei getrennte Herkünfte: P1 verlässt KiWa durch die östliche Tür (RZ-027, A), P2 den E-Verteilerraum durch einen eigenen südlicheren Durchgang (RZ-026, B), P3 kommt aus dem nördlichen FRR-Flur. Alle Linien bleiben im gemeinsamen Verbindungsflur; private Treppe und Hobbyräume werden nicht zum allgemeinen Fluchtweg erklärt. Die Down-Blöcke sind mit der Front zur Ankunft ausgerichtet (RZ-027 Front nach Westen).
> „RZ-027 ist für die aus KiWa kommende P1 der erste unmittelbare Türbezug [...] der Down-Block wird mit der Front nach Westen ausgerichtet.“
> „Diesen Zusammenhang darf ein Raumname allein nicht ersetzen: Der gezeichnete Türdurchgang ist hier der örtliche Beleg.“
> „P2 muss nicht erst nach Norden zu RZ-027 zurückgehen.“
**Leuchten im Bild:** (A) down, (B) down, (C) down
**Personen:** P1 aus KiWa (östliche Tür), P2 aus dem E-Verteilerraum, P3 aus dem nördlichen FRR-Flur
**Linien:** Grün gestrichelte Folgen aller drei Herkünfte, vereinigt im Verbindungsflur Richtung 18 STG; türkise 2D-Blick-Linien zu den Türleuchten
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6012E, 6014E, 6018E, 60210, 60290, 602D0, 60310, 604D0, 60330, 60390, 60430, 604B0, 60490, 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470, 6010E, 601CE, 6020E, 60250, 60510, 60370, 603D0, 603F0, 60450 · Szene-11: A=60430 (RIVO_ARR_down, Welt-Pfeil 180 = Front nach Westen zur KiWa-Ankunft), B=60410 (RIVO_ARR_down, Welt-Pfeil 180 an der E-Verteiler-Tür); Tür-RZ an KiWa (Allgemeinbereich, NB-R02) und E-Raum (NB-R19) belegt
**Bewertung:** bestaetigt:NB-R19

## S. 29 · UG — Nördlicher Stgh 2-Anschluss: KiWa, E-Verteiler und Verbindungsflur (FORTSETZUNG)
**Bereich:** Nord-Süd-Verbindungsflur auf Höhe des Wohnungszugangs
**Bild:** Gleicher Ausschnitt wie S.28, behandelt RZ-025 (C) im gemeinsamen Verbindungsflur: Die Down-Front wird zur nördlichen Herkunft gelegt (insbesondere P3s südliche Ankunft aus dem FRR-Bereich). Die Leuchte setzt die Orientierung zum Stgh 2-Podest fort; die direkt benachbarte Wohnungstür wird nicht als Fortsetzung der gemeinsamen Wegkette benutzt.
> „Die Down-Front wird zur nördlichen Herkunft gelegt.“
> „die direkt benachbarte Wohnungstür wird nicht als Fortsetzung der gemeinsamen Wegkette benutzt“
> „Örtliche Grenze: Benutzbarkeit der Wohnungstür für andere Personen wird nicht unterstellt.“
**Leuchten im Bild:** (C) down
**Personen:** P3 aus dem nördlichen FRR-Flur
**Linien:** Grün gestrichelte Nord-Süd-Folge durch den Flur bis 18 STG; türkise Blick-Linie P3->C
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6010E, 601CE, 6020E, 60250, 60510, 60370, 603D0, 603F0, 60450 · Szene-11 C=603F0 (RIVO_ARR_down, Welt-Pfeil 90 = Front nach Norden zur ankommenden P3, Fluchtrichtung Süd -> Pfeil entgegen Fluchtrichtung wie NB-R06)
**Bewertung:** bestaetigt:NB-R06

## S. 30 · UG — Westlicher FRR2-Flur: Raumankunft und gemeinsamer Südast
**Bereich:** FRR2-Flur West (FRR 2.08-2.11) / zentraler Südast
**Bild:** P1 kommt aus FRR 2.09 durch die südliche Raumtür und folgt dem westlichen Flurarm nach Osten (P1a/P1b als Zeitfolge). Die Antipanik-Leuchte AP-004 (A) beleuchtet den westlichen Flurarm ohne Pfeilbotschaft; RZ-029 (B) macht die südliche Weiterführung verständlich, RZ-028 (C) sitzt an der südlichen Tür. P3 steht im Südast vor der Tür; danach schließt der Verbindungsflur aus S11 an.
> „Das RIVO-Antipanik-Symbol ersetzt die rechteckige Sicherheitsleuchtengrafik, ohne eine Pfeilbotschaft zu erzeugen.“
> „Aus dem Bibliotheksnamen folgt hier keine bestätigte flächige Antipanikberechnung.“
> „HF-N01: §§ 3.2–3.5 [...] Zeichen- und Beleuchtungsaufgaben unterscheiden“
**Leuchten im Bild:** (A) antipanik, (B) right, (C) down
**Personen:** P1a aus FRR 2.09 (südliche Raumtür), P1b im westlichen Flurarm, P3 im Südast
**Linien:** Grün gestrichelte Folge FRR 2.09 -> Flurarm Ost -> Südast -> Tür; türkise 2D-Blick-Linien; orange FUK-Marker im Plan (Bestand, keine Lehr-Lücke)
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6012E, 6014E, 6018E, 60210, 60290, 602D0, 60310, 604D0, 60330, 60390, 60430, 604B0, 60490, 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470, 6010E, 601CE, 6020E, 60250, 60510, 60370, 603D0, 603F0, 60450 · Szene-12 A=604B0 (RIVO_Antipanik, typ=antipanik, kein Welt-Pfeil) im westlichen Flurarm; Gang mit Trenntür erhält Tür-RZ + Antipanik-Leuchten auf der Gangachse wie NB-R09
**Bewertung:** bestaetigt:NB-R09

## S. 31 · UG — Westlicher FRR2-Flur: Raumankunft und gemeinsamer Südast (FORTSETZUNG)
**Bereich:** Zusammenlauf der FRR2-Flurarme / südliche LET-/EI2-Tür
**Bild:** RZ-029 (B, gedrehte Rechts-Variante, zeigt im Grundriss südwärts) liegt vor dem zentralen Südast, auf den P1 und P2 aus entgegengesetzten Flurarmen zulaufen; eine beidseitige Frontansicht wird ausdrücklich nicht erfunden, die beidseitige Lesbarkeit bleibt als örtliche Grenze offen. RZ-028 (C, Down-Front zur nördlichen Ankunft) erklärt den konkreten südlichen Türdurchgang, nach dem RZ-025 in S11 übernimmt.
> „P1 und P2 kommen jedoch von gegenüberliegenden Seiten. Eine einzige gezeichnete Zeichenfläche beweist nicht automatisch die Lesbarkeit aus beiden Ankünften, weshalb hier keine beidseitige Frontansicht erfunden wird.“
> „Die Down-Front ist deshalb zur nördlichen Ankunft gerichtet.“
> „Örtliche Grenze: Reale Front-/Rückseite für beide Gegenankünfte nicht belegt“
**Leuchten im Bild:** (B) right, (C) down
**Personen:** P1 aus dem westlichen Flurarm, P2 aus dem östlichen Flurarm, P3 im zentralen Ast
**Linien:** Grün gestrichelte Folgen beider Gegenankünfte zum Südast; türkise 2D-Blick-Annahmen zu B; Grenze der beidseitigen Lesbarkeit textlich (orange Kategorie)
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 600EE, 6016E, 601EE, 601AE, 60270, 602B0, 602F0, 604F0, 60350, 603B0, 60410, 60470, 6010E, 601CE, 6020E, 60250, 60510, 60370, 603D0, 603F0, 60450 · Szene-12: B=60470 (RIVO_ARR_right, Welt-Pfeil 270 = südwärts), C=60450 (RIVO_ARR_down, Welt-Pfeil 90 = Front zur Nordankunft). Kein beidseitig-Block im Quellplan an diesem Knoten; die Unterlage dokumentiert das als offene Grenze, kein Widerspruch zu NB-R16, sondern Bestätigung der Begründung (eine Zeichenfläche deckt keine zwei Gegenströme)
**Bewertung:** bestaetigt:NB-R16

## S. 32 · UG — Östlicher FRR2-Flur: aus FRR 2.05 zum gemeinsamen Südast
**Bereich:** FRR2-Flur Ost (FRR 2.02-2.07) / Anschluss Südast
**Bild:** P2 kommt aus FRR 2.05 durch die tatsächlich gezeichnete südliche Raumtür und geht im östlichen Flurarm nach Westen (P2a/P2b). Die Linie bleibt zwischen den Raumreihen und läuft nicht durch die Türen der südlich angrenzenden Räume. AP-003 (A) übernimmt die Beleuchtungsaufgabe im längeren östlichen Flurarm ohne Richtungsbotschaft; die Bewegung endet am gemeinsamen Anschluss zum Südast, ab dort übernimmt S12 (RZ-029/RZ-028) ohne Doppelzählung.
> „Ihre Beleuchtungsaufgabe unterstützt die Erkennbarkeit der Gangfläche und der Raumtüranschlüsse; sie zeigt keine Richtung wie ein Rettungszeichen.“
> „Diese Leuchte ist nicht mit AP-004 austauschbar zu beschreiben: Sie liegt auf der anderen Seite des zentralen Asts und unterstützt eine entgegengesetzte Ankunft.“
> „Die tatsächliche Flächendeckung ist offen.“
**Leuchten im Bild:** (A) antipanik
**Personen:** P2a aus FRR 2.05 (südliche Raumtür), P2b im östlichen Flurarm
**Linien:** Grün gestrichelte West-Folge durch den östlichen Flurarm mit Pfeilende am Anschluss zum Südast; türkise Blick-Linie P2b->A
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles 6012E, 6014E, 6018E, 60210, 60290, 602D0, 60310, 604D0, 60330, 60390, 60430, 604B0, 60490 · Szene-13 A=60490 (RIVO_Antipanik im östlichen Flurarm); zweite Antipanik-Leuchte des FRR2-Flurs, je Flurarm eine, Tür-RZ am Trenn-Durchgang -> Muster NB-R09
**Bewertung:** bestaetigt:NB-R09

## S. 33 · EG — GESCHOSSÜBERSICHT: EG – vorhandene Bereiche und Fälle
**Bereich:** EG gesamt (Übersicht aus der vollständigen RIVO-Kopie)
**Bild:** Übersichtsblatt des EG mit 13 physischen Positionen: 9 Rettungszeichen, 2 Aufheller, 2 Antipanik-CAD-Zuordnungen. Verzeichnis der sechs EG-Szenen HF-EG-S01 bis HF-EG-S06 (Stiege 1, Stiege 2, Müllraum) mit Seitenverweisen S.34-45. Die Übersicht ist ausdrücklich kein lesbarer Einzelzeichennachweis.
> „13 physische Positionen: 9 Rettungszeichen · 2 Aufheller · 2 Antipanik-CAD-Zuordnungen.“
> „die Übersicht ist kein lesbarer Einzelzeichennachweis“
**Linien:** Gesamtgrundriss EG verkleinert; keine Lehr-Linien, nur Szenenverzeichnis
**DXF-Abgleich:** Hausfeldstraße_EG_Notbeleuchtung_RIVO.dxf · Handles — · GT-Inventar EG bestätigt n_leuchten=13 (exakt die genannten 13 physischen Positionen)
**Bewertung:** kein_regelgehalt

## S. 34 · EG — Stiege 1: aus Tür 01 zum westlichen Ausgang
**Bereich:** STGH1-Gang (81,39 m²) / Wohnungstür 01 / westliche Außentür
**Bild:** Zwei Stationen derselben Person: P1a kommt durch Wohnungstür 01 in den Gang der Stiege 1, das Linkszeichen RZ-002 (A) gibt dieser Ankunft die Fortsetzung nach Westen; P1b erreicht den Bereich vor der Außentür (RZ-001, B). Der echte RIVO-Linksblock übernimmt die Linksangabe des Quellblocks, sein weißer Balken liegt auf der Ankunftsseite. Die grüne Folge endet auf der unmittelbar gezeichneten Außenfläche (orangenes X), nicht an einem erfundenen sicheren Sammelpunkt.
> „Das Zeichen erklärt damit zuerst die Richtungswahl aus der Wohnung, während RZ-001 anschließend die westliche Ausgangsstelle betrifft.“
> „Eine bloße Verbindung zu RZ-002 an der Wand wäre keine Gehfolge: Gezeichnet ist der freie Gang davor.“
> „Übertragbar ist die Trennung von Türankunft und nächster Ausgangsentscheidung.“
**Leuchten im Bild:** (A) left, (B) down
**Personen:** P1a aus Wohnungstür 01 (südliche Türöffnung), P1b im Gang vor der Außentür
**Linien:** Grün gestrichelte Folge Tür 01 -> Gang -> westliche Außentür, endet am orangen X auf der Außenfläche; türkise 2D-Blick-Linien P1a->A und P1b->B
**DXF-Abgleich:** Hausfeldstraße_EG_Notbeleuchtung_RIVO.dxf · Handles 9ED84, 9EDA4, 9EDE4, 9EE48, 9EE68, 9EEA8, 9ED64, 9EDC4, 9EE08, 9EDE6, 9EE06, 9EE88 · Szene-1 A=9ED84 (RIVO_ARR_left, Welt-Pfeil 179 = Fortsetzung nach Westen); erste sichtbare Leuchte beim Verlassen der Wohnung, ein RZ bedient die Türankunft
**Bewertung:** bestaetigt:NB-R08

## S. 35 · EG — Stiege 1: aus Tür 01 zum westlichen Ausgang (FORTSETZUNG)
**Bereich:** STGH1 / westliche Außentür mit Gitterrost
**Bild:** RZ-001 (B) ist der westlichen Außentür zugeordnet; Türflügel, Öffnung und Gitterrost sind im Plan sichtbar. Der vollständige Down-Block wird so gedreht, dass sein CAD-Pfeil nach Osten und der weiße Balken zur ankommenden Person zeigt – die beauftragte Grundrisskonvention, keine reale Pfeilmontage gegen den Ausgang. Nach der Tür ist die Außenfortsetzung gesondert zu prüfen (örtliche Grenze: Anschluss an einen nachgewiesenen sicheren Bereich fehlt).
> „wird der vollständige Down-Block so gedreht, dass sein sichtbarer CAD-Pfeil nach Osten und der weiße Balken zur Person zeigt. Das ist die beauftragte Grundrisskonvention, keine reale Pfeilmontage gegen den Ausgang.“
> „HF-N05: § 4.1.2 g [...] letzter Ausgang und Außenfortsetzung“
> „Örtliche Grenze: Außenfläche vorhanden; Anschluss an einen nachgewiesenen sicheren Bereich fehlt.“
**Leuchten im Bild:** (B) down
**Personen:** P1b aus dem Gang (Osten)
**Linien:** Grün gestrichelte Folge durch die Türöffnung zum orangen X auf der Außenfläche; türkise Blick-Linie P1b->B
**DXF-Abgleich:** Hausfeldstraße_EG_Notbeleuchtung_RIVO.dxf · Handles 9ED64, 9EDC4, 9EE08, 9EDE6, 9EE06, 9EE88 · Szene-1 B=9ED64 (RIVO_ARR_down, Welt-Pfeil 0 = CAD-Pfeil nach Osten, ins Rauminnere/zur Person, Fluchtrichtung West) – deckungsgleich mit NB-R03-Rotation 'Welt-Pfeil ins Rauminnere' an der Gebäude-Ausgangstür
**Bewertung:** bestaetigt:NB-R03

## S. 36 · EG — Stiege 1: zwei Ankünfte treffen am Gangknick zusammen
**Bereich:** STGH1 (30,28 m²) / Tür 03 / Gang östlich des Lifts / Quergang
**Bild:** P2 benutzt den Gang östlich des Aufzugs und biegt südlich der Kabine nach Westen; P3 kommt durch Tür 02 in denselben Quergang. Der Aufzug wird nicht als Fluchtweg benutzt, eine grüne Linie durch das Treppenauge der 18-STG-Treppe wäre falsch. RZ-003 (A) steht bei Tür 03 am schmalen Gang neben dem Lift; der native Linksblock behält seine schräge Grundrissrotation (Pfeilgrafik nach Süden), die Down-Gegenrichtungsregel gilt hierfür nicht. Der RIVO-Weißbalken liegt ostseitig, die Türankunft erfolgt von Norden – die türkise Verbindung ist nur ein angenommener 2D-Blick, die reale Zeichenfläche benötigt einen Montagebeleg.
> „Der Aufzug selbst wird nicht als Fluchtweg benutzt. Die mit 18 STG bezeichnete Treppe ist ein eigener Anschluss; eine grüne Linie durch das Treppenauge wäre falsch.“
> „Der native Linksblock wird mit seiner vorhandenen schrägen Grundrissrotation übernommen [...] Die Down-Gegenrichtungsregel gilt hierfür nicht.“
> „Deshalb ist die türkise Verbindung nur ein angenommener 2D-Blick, kein behaupteter frontaler Lesbarkeitsnachweis.“
**Leuchten im Bild:** (A) left, (B) left
**Personen:** P2a aus dem Gang östlich des Aufzugs (Norden), P2b im Quergang, P3a aus Tür 02 (Südosten)
**Linien:** Grün gestrichelte Folgen beider Ankünfte, die am Gangknick zusammentreffen und nach Westen weiterlaufen; keine Linie durch Liftkabine oder Treppenauge; türkise 2D-Blick-Linien zu A und B
**DXF-Abgleich:** Hausfeldstraße_EG_Notbeleuchtung_RIVO.dxf · Handles 9ED84, 9EDA4, 9EDE4, 9EE48, 9EE68, 9EEA8, 9ED64, 9EDC4, 9EE08, 9EDE6, 9EE06, 9EE88 · Szene-2 A=9EDA4 (RIVO_ARR_left, Welt-Pfeil 269 = Pfeilgrafik nach Süden, native schräge Rotation rot_deg 89.16 bestätigt); Präzisierung: Gegenrichtungsregel NB-R06 gilt nur für den down-Typ, links/rechts-Blöcke tragen die Fluchtrichtung direkt (deckt sich mit NB-R07)
**Bewertung:** bestaetigt:NB-R07

## S. 37 · EG — Stiege 1: zwei Ankünfte treffen am Gangknick zusammen
**Bereich:** STGH1, Zusammenlauf südlich des Lifts
**Bild:** Fortsetzung HF-EG-S02: Am Übergang vom schmalen Liftseitengang in den langen West-Ost-Gang steht das Links-RZ (B) HF-EG-RZ-004. P2 kommt von Norden am Lift vorbei (P2a) und biegt am Gangende nach Westen ab (P2b); P3a kommt aus der südlichen Tür 02 hinzu. Oben an der Stiege ist (A) das Stiegen-RZ aus der Vorseite sichtbar; die Liftkabine (140x110) bleibt aus der Wegführung ausgeschlossen.
> „Sie unterscheidet sich von RZ-003 durch die hier mögliche Richtungswahl: P2 muss am Gangende abbiegen; P3 kommt dagegen aus der südlichen Tür 02 hinzu.“
> „Nach der Richtungswahl folgen RZ-002 und RZ-001, nicht der Aufzug.“
**Leuchten im Bild:** (A) down, (B) left
**Personen:** P2a/P2b: aus dem nördlichen Liftseitengang, P3a: aus südlicher Tür 02
**Linien:** grün gestrichelte Fluchtlinien beider Ströme treffen am Knick bei (B); türkise Sichtlinie P3a→(B); Lift ausgespart
**DXF-Abgleich:** Hausfeldstraße_EG_Notbeleuchtung_RIVO.dxf · Handles 9ED84, 9EDA4, 9EDE4, 9EE48, 9EE68, 9EEA8, 9ED64, 9EDC4, 9EE08, 9EDE6, 9EE06, 9EE88 · 
**Bewertung:** bestaetigt:NB-R07

## S. 38 · EG — Stiege 1: Aufheller und östliche Tür zum Verbindungsweg
**Bereich:** STGH1, langer Gang zum Verbindungsweg / östliche Außentür
**Bild:** Langer West-Ost-Gang mit Beschriftung FLUCHTWEG/Verbindungsweg. (A) Aufheller HF-EG-SL-001 (RIVO_Aufheller_Variante) liegt im Gangstück zwischen Liftbereich und östlicher Außentür, bewusst nicht mittig in die Gehlinie geschoben. (B) Down-RZ HF-EG-RZ-006 an der östlichen Außentür, Rotation 270 Grad: CAD-Pfeil nach Westen entgegen der Ostbewegung, weißer Balken zur ankommenden Person P1a/P1b. Orange ? jenseits der Tür (Außenfortsetzung offen).
> „Der Aufheller hat deshalb keine erfundene Pfeilbotschaft und keine Vorderseite wie ein Rettungszeichen.“
> „Nach Nutzerkonvention erhält der gesamte RIVO-Down-Block hier eine Rotation von 270 Grad: sichtbarer CAD-Pfeil nach Westen, weißer Balken auf der westlichen Ankunftsseite.“
**Leuchten im Bild:** (A) aufheller, (B) down
**Personen:** P1a/P1b: aus dem westlichen Gang (Liftbereich)
**Linien:** grüne Fluchtlinie West→Ost durch den Gang bis zur Tür; türkise Blicklinie auf (B); orange Lücke hinter der Tür
**DXF-Abgleich:** Hausfeldstraße_EG_Notbeleuchtung_RIVO.dxf · Handles 9ED84, 9EDA4, 9EDE4, 9EE48, 9EE68, 9EEA8, 9ED64, 9EDC4, 9EE08, 9EDE6, 9EE06, 9EE88 · 
**Bewertung:** bestaetigt:NB-R06

## S. 39 · EG — Stiege 2: Stiegenankunft und westlicher Türbereich
**Bereich:** STGH2, Gang südlich des Stiegenlaufs / westlich des Laufs
**Bild:** Freier Gang südlich des Stiegenlaufs (17 STG / 18 STG). (A) Links-RZ HF-EG-RZ-007 westlich des Stiegenlaufs nahe der Briefkastenanlage mit fast horizontaler Quellrotation, Weißbalken zur südlichen Blickseite; es trennt die vorgelagerte Richtungswahl vom eigentlichen Türzeichen (B) RZ-005 am westlichen Türbereich, daneben (C) AP-001. P1a kommt von der Stiege im Osten, P1b erreicht den westlichen Türbereich. Keine ungeprüfte Linie über den verdeckten Lauf oder durch das Treppenauge.
> „Nach dem Zeichen folgt der westliche Türbereich mit RZ-005. So wird die vorgelagerte Richtungswahl vom eigentlichen Türzeichen unterschieden.“
> „aus dieser Zeichnung wird dennoch keine ungeprüfte Linie über einen verdeckten Lauf oder durch das Treppenauge gezogen.“
**Leuchten im Bild:** (A) left, (B) down, (C) antipanik
**Personen:** P1a: von der Stiegenankunft im Osten, P1b: im Gang
**Linien:** grüne Fluchtlinie Ost→West südlich des Laufs; türkise Sichtlinien auf (A) und (B); orange X/? an der Außenfortsetzung links
**DXF-Abgleich:** Hausfeldstraße_EG_Notbeleuchtung_RIVO.dxf · Handles 9ED84, 9EDA4, 9EDE4, 9EE48, 9EE68, 9EEA8, 9ED64, 9EDC4, 9EE08, 9EDE6, 9EE06, 9EE88, 9EE28 · 
**Bewertung:** bestaetigt:NB-R07

## S. 40 · EG — Stiege 2: Stiegenankunft und westlicher Türbereich (Fortsetzung)
**Bereich:** STGH2, westliche Außentür
**Bild:** Gleicher Ausschnitt wie S.39. Fokus (B) HF-EG-RZ-005 innen am westlichen Durchgang: Auf ausdrückliche Nutzerkorrektur ersetzt der echte RIVO_ARR_down die zuvor dargestellte Linksvariante. Der ganze Block ist um 90 Grad gedreht, CAD-Pfeil nach Osten entgegen der lokalen Westbewegung, langer weißer Balken zur ankommenden Person P1b. RZ-007 erklärt davor die Richtungswahl, RZ-005 kennzeichnet die Türpassage; dahinter betrifft AP-001 die Außenfläche.
> „Auf ausdrückliche Nutzerkorrektur ersetzt hier der echte RIVO_ARR_down die zuvor dargestellte Linksvariante.“
> „Sein sichtbarer CAD-Pfeil zeigt nach Osten, entgegen der lokalen Westbewegung; der lange weiße Balken liegt zur ankommenden Person.“
**Leuchten im Bild:** (B) down, (A) left, (C) antipanik
**Personen:** P1b: von Osten aus dem Gang
**Linien:** grüne Fluchtlinie endet an der gezeichneten Türöffnung, nicht am Symbolmittelpunkt; türkise Blicklinie auf (B)
**DXF-Abgleich:** Hausfeldstraße_EG_Notbeleuchtung_RIVO.dxf · Handles 9ED64, 9EDC4, 9EE08, 9EDE6, 9EE06, 9EE88, 9ED84, 9EDA4, 9EDE4, 9EE48, 9EE68, 9EEA8, 9EE28 · 
**Bewertung:** bestaetigt:NB-R01

## S. 41 · EG — Stiege 2: Stiegenankunft und westlicher Türbereich (Fortsetzung)
**Bereich:** STGH2, unmittelbar außerhalb der westlichen Tür
**Bild:** Gleicher Ausschnitt wie S.39/40. Fokus (C) HF-EG-AP-001: rechteckiges Sicherheitsleuchtensymbol außen vor dem westlichen Türbereich neben dem Türflügel, per Nutzerzuordnung durch RIVO_Antipanik ersetzt. Aufgabe: Erkennbarkeit des Austritts und der angrenzenden Außenbodenfläche für P1b; keine Links-/Rechtsinformation, keine Zeichenfront. Umfang der Außenbeleuchtung bleibt zu berechnen.
> „Das rechteckige Sicherheitsleuchtensymbol liegt außen vor dem westlichen Türbereich, neben dem gezeichneten Türflügel.“
> „Im Unterschied zum inneren RZ-005 gibt diese Leuchte keine Links-/Rechtsinformation und besitzt keine betrachtete Zeichenfront.“
**Leuchten im Bild:** (C) antipanik, (B) down
**Personen:** P1b: von innen durch die westliche Tür
**Linien:** grüne Fluchtlinie durch die Türöffnung nach außen; orange X an der ungesicherten Außenfortsetzung
**DXF-Abgleich:** Hausfeldstraße_EG_Notbeleuchtung_RIVO.dxf · Handles 9EE28, 9ED64, 9EDC4, 9EE08, 9EDE6, 9EE06, 9EE88 · 
**Bewertung:** neu → Antipanik-/Sicherheitsleuchte unmittelbar AUSSEN vor dem letzten Ausgang (EN 1838 § 4.1.2 g Außenfortsetzung): reine Beleuchtungsaufgabe für Austritt + angrenzende Bodenfläche, ohne Richtungsinformation — ergänzt das innere Tür-RZ, kein Ersatz; Lux-Nachweis separat

## S. 42 · EG — Stiege 2: aus Tür 02 in den Gang am Stiegenfuß
**Bereich:** STGH2, Gang vor südlicher Wohnungstür 02
**Bild:** P2a tritt aus der Wohnungstür 02 (Top 02, 95,95 m2) nach Norden in den Gang und blickt auf die südlich markierte Weißseite des Links-RZ (A) HF-EG-RZ-008 unmittelbar vor der Tür; der native RIVO-Linksblock behält die fast horizontale Bestandsrotation. P2b folgt danach dem freien Bodenstreifen südlich der Treppe nach Westen; (B) Aufheller SL-002 im Gang ergänzt ohne Pfeilangabe. Die nördliche Tür 01 gilt als eigene Ankunft und wird nicht automatisch als mitabgedeckt erklärt.
> „RZ-008 bedient damit die unmittelbare Türankunft, während RZ-007 weiter westlich den Stiegen-/Gangzusammenhang erläutert.“
> „Die im selben Ausschnitt nördlich liegende Tür 01 ist eine eigene Ankunft und wird nicht allein wegen räumlicher Nähe als bereits durch dieselbe Schildseite abgedeckt erklärt.“
**Leuchten im Bild:** (A) left, (B) aufheller
**Personen:** P2a: aus südlicher Wohnungstür 02, P2b: im Gang am Stiegenfuß
**Linien:** grüne Fluchtlinie Tür 02 → Gang → West; türkise Sichtlinie P2a→(A); Liftkabine ausgespart
**DXF-Abgleich:** Hausfeldstraße_EG_Notbeleuchtung_RIVO.dxf · Handles 9ED84, 9EDA4, 9EDE4, 9EE48, 9EE68, 9EEA8, 9ED64, 9EDC4, 9EE08, 9EDE6, 9EE06, 9EE88 · 
**Bewertung:** bestaetigt:NB-R08

## S. 43 · EG — Stiege 2: aus Tür 02 in den Gang am Stiegenfuß (Fortsetzung)
**Bereich:** STGH2, Bodenbereich südlich des Stiegenlaufs
**Bild:** Gleicher Ausschnitt wie S.42. Fokus (B) HF-EG-SL-002: runder Bestandskörper im Gang südlich des langen Treppenbereichs, ersetzt durch RIVO_Aufheller_Variante. Reine Beleuchtungsdarstellung ohne Pfeilfunktion: ergänzt RZ-008 und RZ-007, ersetzt deren Richtungsinformation nicht. Stufen-/Podestbezug plausibel, aber ein sichtbares Kreiszeichen ist kein Lichtkegel — direkter Stufen-/Bodennachweis nur per Lichtberechnung.
> „Der Ersatz RIVO_Aufheller_Variante ist deshalb eine Beleuchtungsdarstellung ohne Pfeilfunktion: Er ergänzt RZ-008 und RZ-007, statt deren Richtungsinformation zu ersetzen.“
> „Gerade bei einem langen Lauf ist ein sichtbares Kreiszeichen kein Lichtkegel.“
**Leuchten im Bild:** (B) aufheller, (A) left
**Personen:** P2b: im Gang südlich des Stiegenlaufs
**Linien:** grüne Fluchtlinie entlang des Gangs nach Westen; keine Linie über den Treppenlauf
**DXF-Abgleich:** Hausfeldstraße_EG_Notbeleuchtung_RIVO.dxf · Handles 9ED64, 9EDC4, 9EE08, 9EDE6, 9EE06, 9EE88, 9ED84, 9EDA4, 9EDE4, 9EE48, 9EE68, 9EEA8 · 
**Bewertung:** neu → Aufheller-Rollentrennung: Aufheller (RIVO_Aufheller_Variante) traegt NUR die Beleuchtungsaufgabe (Boden/Stufen/Laufanschluss), hat keine Pfeilbotschaft/Vorderseite und ersetzt nie die Richtungsinformation der RZ; Position nicht kosmetisch mittig in die Gehlinie schieben, Lux-Nachweis separat

## S. 44 · EG — Müllraum: freie Bewegungsfläche bis zur nördlichen Tür
**Bereich:** Müllraum (28,35 m2), zentrale freie Bodenfläche
**Bild:** Müllraum mit gezeichneten Behältergruppen (1.100 L Altpapier/Restmüll, 770 L Biomüll/Plastik). (A) HF-EG-AP-002 = RIVO_Antipanik-Block zentral im freien Mittelstreifen zwischen den Behältern; Beleuchtungsaufgabe für Raumfläche und Annäherung an den Ausgang, keine Schildvorderseite. P1a und P1b sind zwei Zeitpunkte derselben Bewegung im freien Mittelstreifen zur nördlichen Tür mit (B) RZ-009; die Linie kürzt nicht über Behälter oder den Schacht ab.
> „Im Gegensatz zu RZ-009 sagt die Leuchte nicht 'nach Norden' und hat keine Schildvorderseite.“
> „Die seitlichen Behälter begrenzen den begehbaren Bereich, ohne dass ihre eingezeichneten Flächen automatisch die normativ maßgebende Antipanik-Bezugsfläche definieren.“
**Leuchten im Bild:** (A) antipanik, (B) down
**Personen:** P1a: aus dem südlichen Raumteil, P1b: im Raum vor der Nordtür
**Linien:** grüne Fluchtlinie im freien Mittelstreifen Süd→Nord, nicht über Behälter/Schacht; orange ? jenseits der Nordtür
**DXF-Abgleich:** Hausfeldstraße_EG_Notbeleuchtung_RIVO.dxf · Handles 9ED84, 9EDA4, 9EDE4, 9EE48, 9EE68, 9EEA8, 9ED64, 9EDC4, 9EE08, 9EDE6, 9EE06, 9EE88 · 
**Bewertung:** bestaetigt:NB-R10

## S. 45 · EG — Müllraum: freie Bewegungsfläche bis zur nördlichen Tür (Fortsetzung)
**Bereich:** Müllraum, nördliche zweiflügelige Tür
**Bild:** Gleicher Ausschnitt wie S.44. Fokus (B) HF-EG-RZ-009 an der nördlichen zweiflügeligen Tür (DL180/DL200, zwei Türbögen, daneben ein Schacht — Passage darf nicht beliebig seitlich verschoben werden). Der vollständige RIVO-Down-Block ist auf die leicht schräge Nordbewegung abgestimmt: CAD-Pfeil zeigt entgegen der Bewegung nach Süden, weißer Balken zur ankommenden Person P1b. Jenseits der Tür (Rampe) endet die geprüfte lokale Folge, orange ?.
> „Der vollständige RIVO-Down-Block wird auf die leicht schräge Nordbewegung abgestimmt. Sein CAD-Pfeil zeigt entgegen dieser Bewegung nach Süden; der weiße Balken liegt zur ankommenden Person.“
> „Die Passage darf deshalb nicht beliebig seitlich verschoben werden.“
**Leuchten im Bild:** (B) down, (A) antipanik
**Personen:** P1b: aus dem Rauminneren
**Linien:** grüne Fluchtlinie durch die Türöffnung; orange X/? auf der Rampe (Außenfortsetzung nicht bestätigt)
**DXF-Abgleich:** Hausfeldstraße_EG_Notbeleuchtung_RIVO.dxf · Handles 9ED64, 9EDC4, 9EE08, 9EDE6, 9EE06, 9EE88, 9ED84, 9EDA4, 9EDE4, 9EE48, 9EE68, 9EEA8 · 
**Bewertung:** bestaetigt:NB-R01

## S. 46 · 1OG — 1OG — vorhandene Bereiche und Fälle
**Bereich:** Geschossübersicht 1OG (beide Bauteile)
**Bild:** Übersichtsseite aus der vollständigen RIVO-Kopie: 7 physische Positionen = 7 Rettungszeichen, 0 Aufheller, 0 Antipanik-CAD-Zuordnungen. Inhaltsverzeichnis der 1OG-Szenen: HF-1OG-S01 (Stiege 1, Zugänge 04/05 um den Liftkern, S.47-48), HF-1OG-S02 (Stiege 1, Ankünfte vor dem abknickenden Stiegenlauf, S.49-50), HF-1OG-S03 (Stiege 2, Türankünfte/unterer Gang/getrennte Laufenden, S.51-52). Kein lesbarer Einzelzeichennachweis.
> „7 physische Positionen: 7 Rettungszeichen · 0 Aufheller · 0 Antipanik-CAD-Zuordnungen.“
> „die Übersicht ist kein lesbarer Einzelzeichennachweis.“
**Linien:** keine Lehrlinien, nur Geschossübersicht
**DXF-Abgleich:** Hausfeldstraße_1OG_Notbeleuchtung_RIVO.dxf · Handles — · 
**Bewertung:** kein_regelgehalt

## S. 47 · 1OG — Stiege 1: von den Zugängen 04 und 05 um den Liftkern
**Bereich:** STGH 1, unterer Gang an den Zugängen 04/05
**Bild:** Unterer Gang von STGH 1: P1 kommt aus Zugang 04 (P1a→P1b), die Linie führt durch die gezeichnete Türöffnung; P2a kommt aus Zugang 05 von rechts. (A) HF-1OG-RZ-007 direkt am Zugang 04 zeigt in der Grundrissdarstellung nach rechts und ordnet den Türbereich dem seitlich fortgesetzten Gang unter dem Lift zu; (B) RZ-002 an der Gangecke übernimmt erst die Richtungsänderung. Die Liftkabine (140x110) bleibt ausgeschlossen; oben führt die Kette weiter Richtung STGH 1.
> „Die aus Zugang 04 kommende Person benötigt unmittelbar nach dem Türdurchgang eine Zuordnung zum seitlich fortgesetzten Gang.“
> „Seine Aufgabe wird deshalb als lokale Weiterleitung entlang der freien Fläche unter dem Lift erläutert, nicht als Aufforderung zum Betreten des Lifts.“
**Leuchten im Bild:** (A) right, (B) left?
**Personen:** P1a/P1b: aus Zugang 04 (87,99 m2), P2a: aus Zugang 05 (109,14 m2)
**Linien:** grüne Fluchtlinien beider Zugänge treffen sich im unteren Gang und laufen rechts am Liftkern hinauf zu STGH 1; türkise Sichtlinien auf (A) und (B)
**DXF-Abgleich:** Hausfeldstraße_1OG_Notbeleuchtung_RIVO.dxf · Handles 130B7, 13037, 13057, 13017, 12FF7, 13077 · 
**Bewertung:** bestaetigt:NB-R08

## S. 48 · 1OG — Stiege 1: von den Zugängen 04 und 05 um den Liftkern (Fortsetzung)
**Bereich:** STGH 1, untere rechte Gangecke neben Zugang 05
**Bild:** Gleicher Ausschnitt wie S.47. Fokus (B) HF-1OG-RZ-002 an der Zusammenführung: P1 wechselt aus dem unteren Gang nach oben im Bild, P2 kommt durch Tür 05 seitlich hinzu. Das Zeichen zeigt im Plan in den rechts am Lift vorbeiführenden Gang und unterscheidet sich damit vom Türzeichen 007 und vom weiter oben liegenden Stiegenzeichen 003. Die Lehrlinie macht den Knick nachvollziehbar, ohne den Weg durch den Schacht zu verkürzen.
> „002 steht an dieser Zusammenführung und zeigt im Plan in den rechts am Lift vorbeiführenden Gang.“
> „Die Lehrlinie macht den Knick nachvollziehbar, ohne einen Weg durch den Schacht zu verkürzen.“
**Leuchten im Bild:** (B) left?, (A) right
**Personen:** P1: aus dem unteren Gang (Zugang 04), P2: aus Tür 05
**Linien:** grüne Fluchtlinie knickt an der Ecke bei (B) nach Norden rechts am Liftkern vorbei; kein Weg durch den Schacht
**DXF-Abgleich:** Hausfeldstraße_1OG_Notbeleuchtung_RIVO.dxf · Handles 13017, 12FF7, 13077, 130B7, 13037, 13057 · 
**Bewertung:** bestaetigt:NB-R07

## S. 49 · 1OG — Stiege 1: mehrere Ankünfte vor dem abknickenden Stiegenlauf
**Bereich:** STGH 1, rechter Zugang zum querliegenden Stiegenlauf
**Bild:** Ausschnitt STGH 1 im 1OG mit zwei RZ: (A)=HF-1OG-RZ-003 am Übergang vom rechten Gang in den querliegenden Stiegenlauf, (B)=HF-1OG-RZ-001 am Knick des Laufes. Drei Personenströme (P1 Gang rechts vom Lift, P2 aus Zugang 06, P3 aus Zugang 07) treffen vor (A) zusammen; P1 wendet sich dort nach links in den Lauf (P1d = spätere Position). Grüner gestrichelter Lehrweg führt über den Lauf mit Vermerk 'weiter ins EG, Stiege 1 - S.36/37'; 17 STG, 17,65/27, beidseitige Handläufe belegen den realen Stiegenbezug.
> „Für P1 wird die im Grundriss nach links weisende Information dem Eintritt in den Lauf zugeordnet.“
> „Ob dieselbe reale Schildseite alle Ankünfte bedient, ist daraus nicht ableitbar.“
> „HF-N04: § 4.1.2 e–f … Richtungswechsel und Gangkreuzungen.“
**Leuchten im Bild:** (A) left, (B) left
**Personen:** Gang rechts vom Lift (P1/P1c/P1d), Zugang 06 (P2/P2a), Zugang 07 (P3/P3a)
**Linien:** grün gestrichelt = Lehrweg, türkis = angenommener Blick
**DXF-Abgleich:** Hausfeldstraße_1OG_Notbeleuchtung_RIVO.dxf · Handles 130B7, 13037, 13057, 13017, 12FF7, 13077 · RZ-003 = RIVO_ARR_left, welt_pfeil 176.3° (nach links/west) — deckt sich mit 'im Grundriss nach links weisende Information' am Stiegen-Eintritt
**Bewertung:** bestaetigt:NB-R05

## S. 50 · 1OG — Stiege 1: mehrere Ankünfte vor dem abknickenden Stiegenlauf (Fortsetzung)
**Bereich:** STGH 1, Knick zwischen querliegendem und linkem Stiegenabschnitt
**Bild:** Gleicher Ausschnitt wie S.49, Fokus (B)=HF-1OG-RZ-001: sitzt am Knick des Stiegenlaufs (Richtungswechsel INNERHALB der Stufenfolge), das gedrehte Quell-Linkszeichen zeigt im Grundriss nach unten entlang des linken Laufteils. P1d kommt von rechts über den querliegenden Lauf. (A)=003 erklärt den Eintritt in den Lauf, (B)=001 die weitere Umlenkung. Stufenbeleuchtung wird ausdrücklich als getrennte Aufgabe benannt.
> „001 befindet sich … am sichtbaren Richtungswechsel der mit Stufen gezeichneten Folge.“
> „Die Leuchte 003 erklärt den Eintritt in den Lauf, 001 die weitere Umlenkung.“
> „Stufenbeleuchtung ist eine zusätzliche Aufgabe und wird nicht durch dieses Rettungszeichen allein nachgewiesen.“
**Leuchten im Bild:** (A) left, (B) left
**Personen:** querliegender Laufteil (P1d)
**Linien:** grün gestrichelt = Lehrweg über den Knick, türkis = angenommener Blick
**DXF-Abgleich:** Hausfeldstraße_1OG_Notbeleuchtung_RIVO.dxf · Handles 130B7, 13037, 13057, 13017, 12FF7, 13077 · RZ-001 = RIVO_ARR_left gedreht, welt_pfeil 267.0° (nach unten/sued) — passt zur Umlenkung in den linken Laufteil
**Bewertung:** neu → Knick-RZ im Stiegenlauf: bei Richtungswechsel INNERHALB eines Stiegenlaufs (Zwischenpodest/abknickender Lauf) ein eigenes Richtungs-RZ am Knick zusätzlich zum Antritts-RZ (NB-R05); Pfeil = weitere Laufrichtung; Stufenbeleuchtung bleibt separater Nachweis

## S. 51 · 1OG — Stiege 2: Ankunft aus dem 1DG und weiterer Abstieg ins EG
**Bereich:** STGH 2, freier Gang südlich des geraden Stiegenlaufes
**Bild:** STGH 2 im 1OG mit geradem Stiegenlauf und Gang darunter. (C)=HF-1OG-RZ-006 liegt zentral auf der Gangachse; P1 tritt durch Zugang 06 und geht nach rechts (P1b später). Das native Down-Symbol ist per Nutzerkonvention gegen die geprüfte Gehbewegung rotiert (grafischer Pfeil nach links). (A)=004 am rechten Podest und (B)=005 am westlichen Laufende rahmen die Szene; P3 kommt aus dem 1DG herunter. Vermerke 'aus dem 1DG / jetzt im 1OG' und 'weiter ins EG, Stiege 2 - S.39-41'.
> „Das Down-Ziel wird dieser geprüften lokalen Gehbewegung gegenübergerichtet rotiert.“
> „Das ist eine Grundriss-Darstellungskonvention, keine Behauptung, ein links lesbares reales Schild bedeute allgemein rechts gehen.“
> „Die Quelle belegt ein Rettungszeichen, keine Antipanik- oder Flächenbeleuchtungsfunktion.“
**Leuchten im Bild:** (C) down, (A) left, (B) left
**Personen:** Zugang 06, südwestlicher Vorraum (P1/P1a/P1b), Tür 04 (P2/P2a), aus dem 1DG über Stiege 2 (P3/P3a)
**Linien:** grün gestrichelt = Lehrweg in der Gehfläche (besucht nicht jeden Montagepunkt), türkis = angenommener Blick
**DXF-Abgleich:** Hausfeldstraße_1OG_Notbeleuchtung_RIVO.dxf · Handles 13097, 130B7, 13037, 13057, 13017, 12FF7, 13077 · RZ-006 = RIVO_ARR_down, welt_pfeil 180.0° bei Gehbewegung [1,0] (0°) — Pfeil exakt ENTGEGEN der Fluchtrichtung, Frontseite zum ankommenden Strom
**Bewertung:** bestaetigt:NB-R06

## S. 52 · 1OG — Stiege 2: Ankunft aus dem 1DG und weiterer Abstieg ins EG (Fortsetzung)
**Bereich:** STGH 2, rechtes Podest und westliches Laufende
**Bild:** Gleicher Ausschnitt wie S.51. (A)=HF-1OG-RZ-004 liegt vor dem Eintritt in den quer zur Gangbewegung liegenden Stiegenlauf am rechten Podest (Linkswechsel für P1, Zusammentreffen mit P2 aus Tür 04); die rechts liegende Liftkabine wird ausdrücklich ausgenommen. (B)=HF-1OG-RZ-005 begleitet die Ankunft aus dem 1DG am westlichen Laufende, wo P3 in den Gang einbiegt; danach übernimmt 006 die Gangfolge und 004 den Abstieg ins EG.
> „004 liegt vor dem Eintritt in den quer zur Gangbewegung liegenden Stiegenlauf.“
> „Das Zeichen übernimmt damit die lokale Entscheidung am Antritt und nicht die Gangbegleitung von 006.“
> „Die unmittelbar rechts liegende Liftkabine ist keine Fortsetzung dieser Lehrfolge.“
**Leuchten im Bild:** (A) left, (B) left
**Personen:** unterer Gang (P1/P1b), Tür 04 (P2/P2a), aus dem 1DG (P3/P3a)
**Linien:** grün gestrichelt = Lehrweg, türkis = angenommener Blick
**DXF-Abgleich:** Hausfeldstraße_1OG_Notbeleuchtung_RIVO.dxf · Handles 130B7, 13037, 13057, 13017, 12FF7, 13077 · RZ-004 = RIVO_ARR_left welt_pfeil 180.1° (Linkswechsel am Antritt); RZ-005 = RIVO_ARR_left gedreht welt_pfeil 270.1° (Umlenkung in den Gang) — beide vor der Stiege bzw. am Laufende (Antritts-RZ nach NB-R05, Ankunfts-RZ nach NB-R04), Lift ohne Leuchte (NB-R27)
**Bewertung:** bestaetigt:NB-R05

## S. 53 · 1DG — Geschossübersicht 1DG – vorhandene Bereiche und Fälle
**Bereich:** gesamtes 1DG (beide Gebäudeteile)
**Bild:** Übersichtsblatt aus der vollständigen RIVO-Kopie mit beiden 1DG-Grundrissen. Kopfzeile: 7 physische Positionen = 7 Rettungszeichen, 0 Aufheller, 0 Antipanik-CAD-Zuordnungen. Verweisliste auf die drei Szenen HF-1DG-S01 (S.54/55), S02 (S.56/57), S03 (S.58/59). Ausdrücklich kein lesbarer Einzelzeichennachweis.
> „7 physische Positionen: 7 Rettungszeichen · 0 Aufheller · 0 Antipanik-CAD-Zuordnungen.“
> „die Übersicht ist kein lesbarer Einzelzeichennachweis.“
**Linien:** nur Übersichtsgrundrisse, keine Lehrwege
**DXF-Abgleich:** Hausfeldstraße_1DG_Notbeleuchtung_RIVO.dxf · Handles — · Evidenz-JSON 1DG: n_leuchten=7 (alle typ rz, 0 Aufheller/Antipanik) — Zählung deckungsgleich
**Bewertung:** kein_regelgehalt

## S. 54 · 1DG — Stiege 1 im 1DG: Zugänge 08/09 und der Gang um den Lift
**Bereich:** STGH 1, unterer Gang am Zugang 08
**Bild:** Unterer Bereich von STGH 1 im 1DG. (A)=HF-1DG-RZ-007 liegt am Zugang 08 vor der beschrifteten Loggia; das nach rechts dargestellte Quellzeichen wählt für P1 ausdrücklich die Innenfortsetzung unterhalb des Liftkerns, NICHT die Loggia. (B)=HF-1DG-RZ-002 sitzt an der Gangecke bei Zugang 09; P2 erreicht sie von der Seite. Grüner Lehrweg entlang des Gangs, Pfeil nach oben ins STGH 1; Rohbaukote +6,12 stützt nur den Geschossvergleich.
> „Für P1 wird ausdrücklich die Innenfortsetzung nach rechts gewählt: Sie verläuft unterhalb des Liftkerns und nicht auf die Loggia.“
> „aus der Ähnlichkeit des 1OG wird keine Türfreigabe für 08 abgeleitet.“
> „der benachbarte Außenbereich ist als Loggia/Terrasse beschriftet und wird nicht als Fortsetzung benutzt.“
**Leuchten im Bild:** (A) right, (B) right
**Personen:** Zugang 08 (P1/P1a/P1b), Zugang 09 (P2/P2a)
**Linien:** grün gestrichelt = Lehrinterpretation, türkis = angenommener 2D-Blick, orange = örtliche Lücke
**DXF-Abgleich:** Hausfeldstraße_1DG_Notbeleuchtung_RIVO.dxf · Handles 227F1, 22771, 22791, 22751, 22731, 227B1 · RZ-007 = RIVO_ARR_right, welt_pfeil 356.9° (nach rechts/ost) — deckt 'Innenfortsetzung nach rechts' am Zugang 08
**Bewertung:** bestaetigt:NB-R08

## S. 55 · 1DG — Stiege 1 im 1DG: Zugänge 08/09 und der Gang um den Lift (Fortsetzung)
**Bereich:** STGH 1, untere rechte Gangecke neben Zugang 09
**Bild:** Gleicher Ausschnitt wie S.54, Fokus (B)=HF-1DG-RZ-002 am rechten Ende des unteren Gangs nahe Zugang 09. Hier trifft die von 08 kommende P1 auf die seitlich aus 09 ankommende P2; die im Plan nach oben gerichtete Information wird dem freien Gang rechts am Lift zugeordnet (Richtungswechsel an der Ecke). Der daneben beschriftete Innenraum bleibt Herkunft, kein automatisch aus dem nächsten Raumtext erzeugtes Fluchtziel.
> „Die im Plan nach oben gerichtete Information wird dem freien Gang rechts am Lift zugeordnet.“
> „Anders als 007 begleitet diese Position den Richtungswechsel.“
> „Der daneben beschriftete Innenraum bleibt Herkunft, nicht ein automatisch aus dem nächstgelegenen Raumtext erzeugtes Fluchtziel.“
**Leuchten im Bild:** (A) right, (B) right
**Personen:** Zugang 08 (P1), Zugang 09 (P2/P2a)
**Linien:** grün gestrichelt = Lehrinterpretation, türkis = angenommener 2D-Blick
**DXF-Abgleich:** Hausfeldstraße_1DG_Notbeleuchtung_RIVO.dxf · Handles 227F1, 22771, 22791, 22751, 22731, 227B1 · RZ-002 = RIVO_ARR_right gedreht, welt_pfeil 86.9° (nach oben/nord) — passt zum Richtungswechsel in den Gang rechts am Lift
**Bewertung:** bestaetigt:NB-R07

## S. 56 · 1DG — Stiege 1 im 1DG: Vorräume 10/11 und die zwei Richtungswechsel
**Bereich:** STGH 1, rechter Zugang zum querliegenden Stiegenlauf
**Bild:** STGH 1 im 1DG. (A)=HF-1DG-RZ-003 sammelt die Ankünfte vom unteren Gang (P1) und aus den Vorräumen an Zugang 10 (P2) und 11 (P3) vor dem Stiegenantritt; der Grundrisspfeil weist nach links in den Stufenabschnitt. (B)=HF-1DG-RZ-001 übernimmt den anschließenden Knick. Tür 10 liegt seitlich hinter der Annäherung von P1, daher gilt dessen Blickbezug nicht automatisch als Sichtnachweis für P2. Vermerk 'weiter ins 1OG, Stiege 1 - S.49/50'; Lift bleibt rechts und wird nicht durchquert.
> „Der Grundrisspfeil weist hier nach links in den mit Stufen belegten Abschnitt.“
> „daher darf dessen angenommener Blickbezug nicht pauschal auch als Sichtnachweis für P2 gelten.“
> „Der Lift bleibt rechts davon und wird nicht durchquert.“
**Leuchten im Bild:** (A) left, (B) left
**Personen:** unterer rechter Gang (P1/P1c/P1d), Vorraum Zugang 10 (P2/P2a), Vorraum Zugang 11 (P3/P3a)
**Linien:** grün gestrichelt = Lehrweg, türkis = angenommener Blick
**DXF-Abgleich:** Hausfeldstraße_1DG_Notbeleuchtung_RIVO.dxf · Handles 227F1, 22771, 22791, 22751, 22731, 227B1 · RZ-003 = RIVO_ARR_left, welt_pfeil 176.3° (nach links/west) — deckt 'Grundrisspfeil weist nach links' vor dem Antritt
**Bewertung:** bestaetigt:NB-R05

## S. 57 · 1DG — Stiege 1 im 1DG: Vorräume 10/11 und die zwei Richtungswechsel (Fortsetzung)
**Bereich:** STGH 1, Knick zwischen querliegendem und linkem Stiegenabschnitt
**Bild:** Gleicher Ausschnitt wie S.56, Fokus (B)=HF-1DG-RZ-001 am Knick des querliegenden Laufteils in den linken Abschnitt neben dem Liftkern. P1d folgt den sichtbaren Stufen und dreht am Knick nach unten im Bild. Erklärt eine andere Entscheidung als 003: nicht Eintritt vom Gang, sondern Richtungsfortsetzung im Lauf; die benachbarte Loggia ist keine Ersatzroute. Kote +6,12 und Handlaufdetail stützen den Stiegenbezug.
> „001 liegt im 1DG am Knick des querliegenden Laufteils in den linken Abschnitt neben dem Liftkern.“
> „nicht der Eintritt vom Gang, sondern die Richtungsfortsetzung im Lauf.“
> „Die benachbarte Loggia ist keine Ersatzroute.“
**Leuchten im Bild:** (A) left, (B) left
**Personen:** querliegender Laufteil (P1d)
**Linien:** grün gestrichelt = Lehrweg über den Knick, türkis = angenommener Blick
**DXF-Abgleich:** Hausfeldstraße_1DG_Notbeleuchtung_RIVO.dxf · Handles 227F1, 22771, 22791, 22751, 22731, 227B1 · RZ-001 = RIVO_ARR_left gedreht, welt_pfeil 267.0° (nach unten/sued) — identisches Muster wie 1OG-RZ-001 (S.50)
**Bewertung:** neu → Knick-RZ im Stiegenlauf: bei Richtungswechsel INNERHALB eines Stiegenlaufs (Zwischenpodest/abknickender Lauf) ein eigenes Richtungs-RZ am Knick zusätzlich zum Antritts-RZ (NB-R05); Pfeil = weitere Laufrichtung; identisch belegt in 1OG (S.50) und 1DG

## S. 58 · 1DG — Stiege 2 im 1DG: Ankunft aus dem 2DG und Abstieg ins 1OG
**Bereich:** STGH 2, freier Gang südlich des geraden Stiegenlaufes
**Bild:** STGH 2 im 1DG. (C)=HF-1DG-RZ-006 liegt auf der Gangachse unter dem Stiegenlauf zwischen Zugang 09 und rechtem Podest; P1 geht nach rechts (Bewegung [1,0]), der echte Down-Block ist gegenläufig ausgerichtet. (A)=004 am rechten Podest bei Zugang 07, (B)=005 am westlichen Laufende; P3 kommt aus dem 2DG herunter. Dachschrägen sind eingetragen, werden aber nicht als freie Querung interpretiert. Ausdrücklich: das Zeichen ist keine Antipanikleuchte.
> „Für das dortige Down-Zeichen 006 ist die örtlich gewählte Bewegung [1,0] in den Quellachsen: Sein Pfeil wird nach Nutzerkonvention entgegengesetzt gedreht.“
> „Das Zeichen ist keine Antipanikleuchte: Die gezeichnete Richtungsinformation und eine erforderliche Flächenbeleuchtung bleiben verschiedene Aufgaben.“
> „Dachschrägen sind zusätzlich eingetragen; sie werden nicht als freie Querung in die Nachbarräume interpretiert.“
**Leuchten im Bild:** (C) down, (A) left, (B) left
**Personen:** Vorraum am Zugang 09 (P1/P1a/P1b), Zugang 07 (P2/P2a), aus dem 2DG über Stiege 2 (P3/P3a)
**Linien:** grün gestrichelt = Lehrweg in der Gehfläche, türkis = angenommener Blick
**DXF-Abgleich:** Hausfeldstraße_1DG_Notbeleuchtung_RIVO.dxf · Handles 227D1, 227F1, 22771, 22791, 22751, 22731, 227B1 · RZ-006 = RIVO_ARR_down, welt_pfeil 180.0° bei Gehbewegung [1,0] (0°) — Pfeil exakt ENTGEGEN der Fluchtrichtung, wie 1OG-Pendant
**Bewertung:** bestaetigt:NB-R06

## S. 59 · 1DG — Stiege 2 im 1DG: Ankunft aus dem 2DG und Abstieg ins 1OG (Fortsetzung)
**Bereich:** STGH 2, rechtes Podest und westliches Laufende
**Bild:** Gleicher Ausschnitt wie S.58. (A)=HF-1DG-RZ-004 beim Zugang 07 am rechten Ende des Stiegenlaufes: P2 aus dem Vorraum und P1 aus dem Gang brauchen den Bezug zum links beginnenden Lauf; die Liftkabine 140x110 rechts gehört nicht zur Folge. (B)=HF-1DG-RZ-005 begleitet die Ankunft aus dem 2DG am westlichen Laufende, P3 biegt in den südlichen Gang ein und folgt ihm über 006 bis 004, weiter ins 1OG. Dachschrägenangaben ersetzen keinen Montagebeleg.
> „Im Unterschied zu 006 beantwortet 004 den Knick am Antritt.“
> „die Dachschrägenangaben im Lauf ersetzen keinen Montagebeleg für die reale Schildseite.“
> „Die benachbarte Liftkabine 140x 110 liegt rechts, gehört aber nicht zur gezeichneten Folge.“
**Leuchten im Bild:** (A) left, (B) left
**Personen:** unterer Gang (P1/P1b), Vorraum Zugang 07 (P2/P2a), aus dem 2DG (P3/P3a)
**Linien:** grün gestrichelt = Lehrweg, türkis = angenommener Blick
**DXF-Abgleich:** Hausfeldstraße_1DG_Notbeleuchtung_RIVO.dxf · Handles 227F1, 22771, 22791, 22751, 22731, 227B1 · RZ-004 = RIVO_ARR_left welt_pfeil 180.1° (Antritt), RZ-005 = RIVO_ARR_left gedreht welt_pfeil 270.1° (Umlenkung in den Gang) — Antritts- und Ankunfts-RZ, Lift ohne Leuchte (NB-R27)
**Bewertung:** bestaetigt:NB-R05

## S. 60 · 2DG — Geschossübersicht 2DG – vorhandene Bereiche und Fälle
**Bereich:** gesamtes 2DG (beide Gebäudeteile)
**Bild:** Übersichtsblatt aus der vollständigen RIVO-Kopie mit beiden 2DG-Grundrissen. Kopfzeile: 3 physische Positionen = 3 Rettungszeichen, 0 Aufheller, 0 Antipanik-CAD-Zuordnungen. Verweisliste auf HF-2DG-S01 (Stiege 1, Zugänge 12/13, S.61/62) und HF-2DG-S02 (Stiege 2, zwei Türankünfte am schmalen Podest, S.63). Kein lesbarer Einzelzeichennachweis.
> „3 physische Positionen: 3 Rettungszeichen · 0 Aufheller · 0 Antipanik-CAD-Zuordnungen.“
> „die Übersicht ist kein lesbarer Einzelzeichennachweis.“
**Linien:** nur Übersichtsgrundrisse, keine Lehrwege
**DXF-Abgleich:** Hausfeldstraße_2DG_Notbeleuchtung_RIVO.dxf · Handles — · Evidenz-JSON 2DG: n_leuchten=3 (alle RIVO_ARR_left, typ rz) — Zählung deckungsgleich
**Bewertung:** kein_regelgehalt

## S. 61 · 2DG — Stiege 1 im 2DG: Zugänge 12/13 und der Weg auf die Stiege
**Bereich:** STGH 1, rechtes Podest am Lift, Stiegenantritt und L-Lauf
**Bild:** Oberster Abschluss von STGH 1 im 2DG. P1 kommt durch Zugang 12 von unten (P1a), P2 durch Zugang 13 aus dem nördlichen Vorraum (P2a); beide erreichen das rechte Podest neben dem Lift. (A) HF-2DG-RZ-001 sitzt an der oberen Entscheidung des Podeststreifens vor dem Stiegenantritt, Pfeil im Plan nach links; (B) HF-2DG-RZ-003 übernimmt am linken Knick die Fortsetzung nach unten. Die Angabe 'BRE/STGH Dachausstieg mind 1m²' wird ausdrücklich NICHT als Notausgang gelesen, die Liftkabine nicht durchquert.
> „001 liegt an der oberen Entscheidung des rechten Podeststreifens.“
> „Die im Plan nach links gerichtete Information wird hier dem Stiegenantritt zugeordnet.“
> „Dieses Zeichen ist nicht die Beleuchtung des markierten Dachausstiegs.“
> „Die tatsächliche Vorder-/Rückseite muss für beide Herkünfte gesondert geprüft werden; der Grundriss allein beweist keine Rundumsicht.“
> „Die Lehre zeigt keine Fortsetzung in die Kabine und auch keinen Weg durch den Dachausstieg.“
**Leuchten im Bild:** (A) left, (B) down
**Personen:** Zugang 12, von unten im Bild (Süden), P1 später am Podest (P1b), P1 auf dem querliegenden Laufabschnitt (P1c), Zugang 13, nördlicher Vorraum (P2a)
**Linien:** grüner Lehrweg gestrichelt von Zugang 12 und 13 über das rechte Podest, links in den querliegenden Lauf und am Knick nach unten; türkise Blicklinie P1c/P1b auf die Zeichenorte; Anschlusskasten 'weiter ins 1DG, Stiege 1 - S.56/57'
**DXF-Abgleich:** Hausfeldstraße_2DG_Notbeleuchtung_RIVO.dxf · Handles 35282, 352A2, 352C2 · Kennung A [-4277,13877] passt zu Leuchte 35282 RIVO_ARR_left [-4465,13222] welt_pfeil 176,7° (links) = Bildrichtung; Kennung B [-8157,13088] passt zu 352C2 RIVO_ARR_left rot 86,7° welt_pfeil 266,7° (down) = Bildrichtung. Personen/Kennungen P1a/P1b/P1c/P2a auf Layer HF_LEHR_HF-2DG-S01_* vorhanden.
**Bewertung:** bestaetigt:NB-R05

## S. 62 · 2DG — Stiege 1 im 2DG: Zugänge 12/13 und der Weg auf die Stiege (Fortsetzung)
**Bereich:** STGH 1, linker Knick des L-förmigen Stiegenlaufes
**Bild:** Gleicher Bildausschnitt wie S.61, jetzt Fall (B) HF-2DG-RZ-003: das Zeichen begleitet die zweite Richtungsentscheidung nach dem Eintritt bei 001. P1c kommt von rechts über den querliegenden Lauf und folgt dem linken Stufenabschnitt nach unten im Bild. Die Position wird dem Stiegenknick zugeordnet, NICHT der daneben gezeichneten Terrasse; die Terrasse wird nicht zur Abkürzung.
> „003 begleitet die zweite Richtungsentscheidung nach dem Eintritt bei 001.“
> „Die Position wird damit dem Stiegenknick, nicht der daneben gezeichneten Terrasse zugeordnet.“
> „Die Terrasse bleibt durch ihre eigene Konstruktion getrennt und wird nicht zur Abkürzung.“
> „HF-N04: § 4.1.2 e–f: Richtungswechsel und Gangkreuzungen.“
> „Handläufe, Montagehöhe und die wechselnde Augenhöhe auf der Stiege sind beim realen Sichtnachweis zu berücksichtigen.“
**Leuchten im Bild:** (A) left, (B) down
**Personen:** Zugang 12 (P1a), P1 am Podest (P1b), querliegender Lauf, von rechts (P1c), Zugang 13 (P2a)
**Linien:** grüner Lehrweg wie S.61; am L-Knick Wechsel nach unten; türkise Blicklinie von P1c auf (B); Anschluss 'weiter ins 1DG, Stiege 1 - S.56/57'
**DXF-Abgleich:** Hausfeldstraße_2DG_Notbeleuchtung_RIVO.dxf · Handles 35282, 352A2, 352C2 · RZ-003 = Leuchte 352C2 RIVO_ARR_left [-7878,12900], rot 86,7° → welt_pfeil 266,7° = Abstiegsrichtung des linken Laufs (down im Bild); Zuordnung zum Knick, nicht zur Terrasse, deckt sich mit Geometrie.
**Bewertung:** bestaetigt:NB-R05

## S. 63 · 2DG — Stiege 2 im 2DG: zwei Türankünfte am schmalen Podest
**Bereich:** STGH 2, rechtes/schmales Podest am Antritt des geraden Laufes
**Bild:** P1 kommt über Zugang 11 aus Süden (P1a), P2 über Zugang 10 aus Norden (P2a); die Wege treffen links der Liftkabine auf dem schmalen Podest zusammen. (A) HF-2DG-RZ-002 liegt an der Entscheidung, vom Podest nach links auf den geraden Lauf zu wechseln, und bedient BEIDE Türherkünfte. Der Text warnt: der Blockwinkel allein bestätigt keine reale Lesbarkeit für beide Personen; Dachausstieg und Lift sind keine freigegebenen Wege; die Person läuft nicht zum Symbolmittelpunkt, sondern in den benutzbaren Stiegenstreifen.
> „002 übernimmt für die beiden Türherkünfte 10 und 11 den Bezug zum links anschließenden Lauf.“
> „Das im Grundriss nach links zeigende Quellzeichen passt zu dieser örtlichen Richtungsänderung, aber sein Blockwinkel bestätigt noch keine reale Lesbarkeit für beide Personen.“
> „Die nebenan angegebene Dachausstiegsöffnung und der Lift sind keine zusätzlich freigegebenen Wege.“
> „die Person läuft nicht zum Symbolmittelpunkt, sondern in den benutzbaren Stiegenstreifen.“
> „Die links beschrifteten Sonderstufen und die Schräge benötigen eine eigene Detailprüfung ihrer Ausführung.“
**Leuchten im Bild:** (A) left
**Personen:** Zugang 11 aus Süden (P1a), P1 am Podest (P1b), Zugang 10 aus Norden (P2a)
**Linien:** grüne Lehrwege gestrichelt aus beiden Türöffnungen, Zusammentreffen links der Liftkabine, dann nach links auf den geraden Lauf; türkise Blicklinie P1b auf (A); Anschluss 'ins 1DG, S.58/59'
**DXF-Abgleich:** Hausfeldstraße_2DG_Notbeleuchtung_RIVO.dxf · Handles 35282, 352A2 · RZ-002 = Leuchte 352A2 RIVO_ARR_left [22015,10627], rot 0,33° → welt_pfeil 180,3° (links/West) = Bildrichtung; Kennung A [22202,11287] daneben. Ein RZ bedient beide Türherkünfte 10+11 — deckt sich mit NB-R08-Mehrfachbedienung.
**Bewertung:** bestaetigt:NB-R08

## S. 64 — Stiegenfolgen – Anschlüsse statt Linien durch Papier
**Bereich:** Grundlagen-Textseite: Stiege 1 über alle Geschosse (2DG-1DG-1OG-EG, UG aufwärts)
**Bild:** Textseite ohne Planbild. Erklärt die Verknüpfung der Einzelszenen zu den zwei Kernen STGH 1 (L-Lauf um den Lift) und STGH 2 (gerader Lauf, Lift rechts): Bauteilzuordnung über Stiegenbezeichnung, Raumstempel, Schnittmarken, Laufangaben (17/18 STG) und Höhen — gleiche Koordinaten oder ähnliche Zeichen allein begründen KEINEN Anschluss. Abwärtsfolge 2DG-1DG-1OG-EG; UG-Personen kommen gegenläufig aufwärts zum EG und werden nicht mit den OG-Strömen gleichgesetzt; Kabine wird nicht durchquert, Dachausstieg nicht als Notausgang gelesen; Kotenarten (FOK/RDOK/Rohbau) werden nicht vermischt.
> „Gleiche Koordinaten oder ähnliche Zeichen allein begründen keinen Anschluss.“
> „Für beide Stiegen lautet die normale Abwärtsfolge: 2DG - 1DG - 1OG - EG. Menschen aus dem UG kommen dagegen aufwärts zum EG.“
> „Die Ankunft vom Keller wird nicht mit der gegenläufigen Ankunft aus den Obergeschossen gleichgesetzt.“
> „RZ-008 gehört genau zu dieser Stufenkante; die Kabine wird nicht durchquert.“
> „Der benachbarte Dachausstieg wird nicht als Notausgang gelesen.“
> „Diese Werte und Kotenarten werden nicht zu einer scheinbar exakten Fertigpodestrechnung vermischt.“
**Linien:** keine (Textseite); referenziert RZ-001/002/003/004/005/007/008/024 und Anschlüsse HF-T1-2DG-1DG, HF-T1-1DG-1OG, HF-T1-1OG-EG, HF-T1-UG-EG
**DXF-Abgleich:**  · Handles — · kein Einzel-Geschoss-Abgleich (geschossübergreifende Textseite)
**Bewertung:** neu → geschoss_anschluss_verifikation: Vertikale Stiegenkern-Zuordnung NUR über Stiegenbezeichnung + Lauf-/Liftkonfiguration + Schnittmarken + Laufangaben/Höhen verifizieren, NIE über bloße Koordinaten-/Zeichenähnlichkeit; UG-Aufwärtsstrom (NB-R13) und OG-Abwärtsstrom am selben Kern als getrennte Herkünfte behandeln, keine vertikale Gehlinie zwischen Grundrissbildern erfinden

## S. 65 — Stiegenfolgen – Anschlüsse statt Linien durch Papier (Fortsetzung)
**Bereich:** Grundlagen-Textseite: Stiege 2 über alle Geschosse, Normrahmen
**Bild:** Textseite ohne Planbild zu STGH 2: Ankünfte 10/11 im 2DG bei RZ-002, 1DG-Ankunft bei RZ-005, Folge über den südlichen Gang bei 006 zu RZ-004 und weiter abwärts; RZ-005 begleitet jeweils die Ankunft vom oberen Geschoss, RZ-004 den nächsten Abstieg. An der EG-Westtür ist RZ-005 auf ausdrückliche Nutzerkorrektur als vollständiges Down-Zeichen mit Weißbalken zur Ankunft aus Osten dargestellt. Garagenpersonen kommen über die zweistufige Schleuse (RZ-024, ostwärts); private Wohnungstreppe, Liftkabine und Garagenrampe sind keine freigegebenen allgemeinen Fluchtwege. CAD-Zeichen allein belegen keine Ausleuchtung.
> „An der Westtür ist RZ-005 auf ausdrückliche Nutzerkorrektur als vollständiges Down-Zeichen dargestellt, mit dem Weißbalken zur Ankunft aus Osten.“
> „Die östliche private Wohnungstreppe, Liftkabine und Garagenrampe werden dadurch nicht zu freigegebenen allgemeinen Fluchtwegen.“
> „RZ-005 begleitet jeweils die Ankunft vom oberen Geschoss; RZ-004 den nächsten Abstieg.“
> „Die gegenläufige Down-Darstellung bei 006 bleibt unverändert.“
> „Die CAD-Zeichen allein belegen diese Ausleuchtung nicht.“
> „Der Anschluss an den äußeren Verbindungsweg wird benannt, nicht als sicherer Endbereich behauptet.“
**Linien:** keine (Textseite); referenziert RZ-002/004/005/006/024 und Anschlüsse HF-T2-1OG-EG, HF-T2-UG-EG
**DXF-Abgleich:**  · Handles — · kein Einzel-Geschoss-Abgleich (geschossübergreifende Textseite)
**Bewertung:** bestaetigt:NB-R06

## S. 66 — Stiege 1 – benachbarte Planstufen
**Bereich:** Gebäudezusammenhang: EG (HF-EG-S02) und 1OG (HF-1OG-S02) am Kern STGH 1
**Bild:** Zwei verkleinerte Vergleichsbilder desselben Stiegenkerns STGH 1: EG-Szene S02 (zwei Ankünfte treffen am Gangknick, Zeichen A/B, Personen P2a/P2b/P3a) und 1OG-Szene S02 (mehrere Ankünfte vor dem abknickenden Stiegenlauf, Zeichen A/B, Personen P1c/P1d/P2a/P3a, ein oranges ?-X am Lauf). Reine Anschlussvergleich-Seite: Details und Einzelzeichen stehen auf S.36/37 bzw. S.49/50; Ausschnitte in eigenen Quellkoordinaten, kein gemeinsamer gezeichneter Gehweg zwischen den Bildern.
> „Bauteilzuordnung durch Stiegenbezeichnung, Lauf-/Liftkonfiguration, Schnittmarken und Höhen; eine durchgängige vertikale Gehlinie wird daraus nicht erfunden.“
> „Die kleinen Bilder dienen nur dem Anschlussvergleich, die Menschen-/Wegdetails stehen in den vergrößerten Fällen.“
**Leuchten im Bild:** (A) ?, (B) ?
**Personen:** Vergleichsbilder EG/1OG (P2a/P2b/P3a bzw. P1c/P1d/P2a/P3a)
**Linien:** grüne Lehrwege in beiden Miniatur-Ausschnitten; kein verbindender Gehweg zwischen den Bildern
**DXF-Abgleich:**  · Handles — · kein neuer Abgleich; Szenen bereits über Detailseiten (EG-S02, 1OG-S02) erfasst
**Bewertung:** kein_regelgehalt

## S. 67 — Stiege 1 – benachbarte Planstufen
**Bereich:** Gebäudezusammenhang: 1DG (HF-1DG-S02) und 2DG (HF-2DG-S01) am Kern STGH 1
**Bild:** Zwei verkleinerte Vergleichsbilder: 1DG-Szene S02 (Vorräume 10/11, zwei Richtungswechsel, Zeichen A/B, oranges ?-X) und 2DG-Szene S01 (Zugänge 12/13, Zeichen A/B). Reine Anschlussvergleich-Seite; Details auf S.56/57 bzw. S.61/62; Ausschnitte in eigenen Quellkoordinaten, kein gemeinsamer gezeichneter Gehweg zwischen den Bildern.
> „Bauteilzuordnung durch Stiegenbezeichnung, Lauf-/Liftkonfiguration, Schnittmarken und Höhen; eine durchgängige vertikale Gehlinie wird daraus nicht erfunden.“
**Leuchten im Bild:** (A) ?, (B) ?
**Personen:** Vergleichsbilder 1DG/2DG (P1c/P1d/P2a/P3a bzw. P1a/P1b/P1c/P2a)
**Linien:** grüne Lehrwege in beiden Miniatur-Ausschnitten; kein verbindender Gehweg zwischen den Bildern
**DXF-Abgleich:**  · Handles — · kein neuer Abgleich; 2DG-Szene S01 bereits auf S.61/62 gegen Handles 35282/352C2 abgeglichen
**Bewertung:** kein_regelgehalt

## S. 68 — Stiege 2 – benachbarte Planstufen
**Bereich:** Gebäudezusammenhang: EG (HF-EG-S05) und 1OG (HF-1OG-S03) am Kern STGH 2
**Bild:** Zwei verkleinerte Vergleichsbilder des Kerns STGH 2: EG-Szene S05 (aus Tür 02 in den Gang am Stiegenfuß, Zeichen A und grünes Kreuz-Symbol B, Personen P2a/P2b) und 1OG-Szene S03 (Türankünfte, unterer Gang, getrennte Laufenden, Zeichen A/B/C, Personen P1a/P1b/P2a/P3a, zwei orange ?-X am Lauf). Reine Anschlussvergleich-Seite; Details auf S.42/43 bzw. S.51/52; kein gemeinsamer gezeichneter Gehweg.
> „Bauteilzuordnung durch Stiegenbezeichnung, Lauf-/Liftkonfiguration, Schnittmarken und Höhen; eine durchgängige vertikale Gehlinie wird daraus nicht erfunden.“
**Leuchten im Bild:** (A) ?, (B) ?, (C) ?
**Personen:** Vergleichsbilder EG/1OG (P2a/P2b bzw. P1a/P1b/P2a/P3a)
**Linien:** grüne Lehrwege in beiden Miniatur-Ausschnitten; kein verbindender Gehweg zwischen den Bildern
**DXF-Abgleich:**  · Handles — · kein neuer Abgleich; Szenen über Detailseiten erfasst
**Bewertung:** kein_regelgehalt

## S. 69 — Stiege 2 – benachbarte Planstufen
**Bereich:** Gebäudezusammenhang: 1DG (HF-1DG-S03) und 2DG (HF-2DG-S02) am Kern STGH 2
**Bild:** Zwei verkleinerte Vergleichsbilder: 1DG-Szene S03 (Vorraum 09, Gangzeichen C, Stiegenantritt 07, Zeichen A/B/C, Personen P1a/P1b/P2a/P3a, zwei orange ?-X) und 2DG-Szene S02 (zwei Türankünfte am schmalen Podest, Zeichen A, ein oranges ?-X). Reine Anschlussvergleich-Seite; Details auf S.58/59 bzw. S.63; kein gemeinsamer gezeichneter Gehweg zwischen den Bildern.
> „Bauteilzuordnung durch Stiegenbezeichnung, Lauf-/Liftkonfiguration, Schnittmarken und Höhen; eine durchgängige vertikale Gehlinie wird daraus nicht erfunden.“
**Leuchten im Bild:** (A) ?, (B) ?, (C) ?
**Personen:** Vergleichsbilder 1DG/2DG (P1a/P1b/P2a/P3a bzw. P1a/P1b/P2a)
**Linien:** grüne Lehrwege in beiden Miniatur-Ausschnitten; kein verbindender Gehweg zwischen den Bildern
**DXF-Abgleich:**  · Handles — · kein neuer Abgleich; 2DG-Szene S02 bereits auf S.63 gegen Handle 352A2 abgeglichen
**Bewertung:** kein_regelgehalt

## S. 70 — Quellen und Geltungsgrenzen
**Bereich:** Grundlagen: Normquellen-Metaseite (N1838_2019)
**Bild:** Textseite ohne Planbild. Deklariert die ÖNORM EN 1838:2019-11-15 (identisch EN 1838:2013-07) als lokale fachliche Vergleichsgrundlage — keine vertragliche/behördliche Geltungsentscheidung nachgewiesen. Nennt Leseumfang (Vorwort, Einleitung, Begriffe, 4.1-4.3, 5.1-5.5, Anhänge; Druckseite = PDF-Seite minus 2). Grundsatz: HF-N-Fundstellen verlangen keine bestimmte RIVO-Blockbezeichnung und keine exakte CAD-Koordinate; 'Aufheller' ist Arbeits-/Bibliotheksbegriff; Normforderung, grafischer Symboltausch und errechnete Istwerte sind drei verschiedene Dinge.
> „Normen sind hier lokale fachliche Vergleichsgrundlagen.“
> „'Neueste lokal gefunden' ist keine Geltungsentscheidung.“
> „Sie verlangen keine bestimmte RIVO-Blockbezeichnung und keine exakte CAD-Koordinate.“
> „Normforderung, grafischer Symboltausch und errechnete Istwerte sind drei verschiedene Dinge.“
**Linien:** keine (Textseite)
**DXF-Abgleich:**  · Handles — · nicht anwendbar (Quellen-Metaseite)
**Bewertung:** kein_regelgehalt

## S. 71 — Gelesene Fundstellen und Anwendungsgrenzen (HF-N01 bis HF-N05)
**Bereich:** Quellenregister EN 1838: Begriffe, Sichtbarkeit, Stufen, Richtungswechsel, letzter Ausgang
**Bild:** Registerseite mit fünf EN-1838-Fundstellen samt Grenzen: HF-N01 Begriffe (Sicherheits-/Rettungsweg-/Antipanikbeleuchtung; Aufheller ist keine EN-Kategorie); HF-N02 § 4.1.1 (Zeichen an Notausgängen; bei fehlender Direktsicht zusätzliche Richtungszeichen — nicht jede Zimmertür ist ein Notausgang); HF-N03 § 4.1.2 a-c (Ausgangstüren, Treppen, Niveauwechsel hervorheben, Stufen direkt beleuchten, Nähe üblicherweise max. 2 m horizontal — keine automatische Leuchte an jeder Stufe); HF-N04 § 4.1.2 e-f (Richtungsänderungen/Gangkreuzungen, beide Richtungen ausleuchten — keine zwingende Leuchte exakt im Kreuzungsmittelpunkt); HF-N05 § 3.2/4.1.2 g (Beleuchtung bis zum sicheren Bereich außen — Hof/Terrasse nicht automatisch sicherer Bereich).
> „Ist der Notausgang nicht direkt sichtbar, sind zusätzliche beleuchtete oder hinterleuchtete Richtungszeichen zur Orientierung erforderlich.“
> „Die im Notfall benutzten Ausgangstüren, Treppen und sonstige Niveauwechsel sind durch Beleuchtung hervorzuheben.“
> „Richtungsänderungen und Gangkreuzungen sind durch Beleuchtung hervorzuheben. Dabei sind gemäß Anmerkung 2 beide Richtungen auszuleuchten.“
> „Die Beleuchtung umfasst den letzten Ausgang und die Außenfortsetzung bis zu einem sicheren Bereich.“
> „Grenze: Nicht jede Zimmertür ist deshalb automatisch ein Notausgang.“
**Linien:** keine (Registerseite)
**DXF-Abgleich:**  · Handles — · nicht anwendbar (Quellenregister)
**Bewertung:** bestaetigt:NB-R08

## S. 72 — Gelesene Fundstellen und Anwendungsgrenzen (HF-N06 bis HF-N09)
**Bereich:** Quellenregister EN 1838: Rettungsweg-Lux, Antipanik, Erkennungsweite, Einrichtungen
**Bild:** Registerseite mit vier EN-1838-Fundstellen samt Grenzen: HF-N06 §§ 4.2.1/4.2.2/4.2.7 (Rettungswege bis 2 m Breite: min. 1 lx auf der Boden-Mittellinie, min. 0,5 lx im Mittelbereich halber Wegbreite, Gleichmäßigkeit max. 1:40; Nutzebene 0,20 m nicht mit Boden-Mittellinie gleichsetzen); HF-N07 §§ 3.5/4.3 (Antipanik min. 0,5 lx Kernfläche ohne 0,5-m-Rand, 1:40 — Grenze: keine AP-Pflicht allein aus L-Form oder nicht sichtbarem Türzeichen ableiten, Blockname beweist keine Funktion); HF-N08 §§ 5.1-5.5 (Erkennungsweite l=z*h, z=100 beleuchtet / z=200 hinterleuchtet, Lage max. 20 Grad über horizontaler Blickrichtung — CAD-Symbolhöhe ist nicht die reale Zeichenhöhe); HF-N09 § 4.1.2 h-i (5 lx vertikal an Erste-Hilfe-/Brandbekämpfungs-/Meldeeinrichtungen, nur wenn belegt).
> „mindestens 1 lx horizontal auf der Boden-Mittellinie und mindestens 0,5 lx im mittleren Bereich von wenigstens halber Wegbreite.“
> „ihr Mindestwert bei 0,5 lx horizontal auf der freien Bodenfläche im Kernbereich, ohne den 0,5 m breiten Rand; Minimum zu Maximum mindestens 1:40.“
> „Grenze: Keine AP-Pflicht allein aus L-Form oder nicht sichtbarem Türzeichen ableiten.“
> „Die maximal betrachtete Erkennungsweite wird als l=z*h mit z=100 für beleuchtete und z=200 für hinterleuchtete Zeichen bestimmt.“
> „empfiehlt die Ausgabe eine Lage höchstens 20 Grad über der horizontalen Blickrichtung.“
> „die angegebene Anforderung betrifft 5 lx vertikal an den genannten Einrichtungen, nicht 5 lx auf irgendeiner Bodenfläche.“
**Linien:** keine (Registerseite)
**DXF-Abgleich:**  · Handles — · nicht anwendbar (Quellenregister); Hinweis: HF-N07-Grenze präzisiert NB-R10 — AP nicht automatisch aus L-Form, Lux-Nachweis entscheidet (deckt sich mit NB-R10-Flag lux_nachweis_erforderlich, kein Widerspruch)
**Bewertung:** bestaetigt:NB-R07

## S. 73 — QUELLENREGISTER — Gelesene Fundstellen und Anwendungsgrenzen
**Bereich:** Normquellen HF-N10 bis HF-N13
**Bild:** Reine Textseite ohne Planszene. Vier Norm-Claims mit Fundstelle und expliziter Anwendungsgrenze: HF-N10 (OVE E 8101:2025 560.1/560.9 trennt Erforderlichkeit, Anlagenanforderungen EN 50172, Lichttechnik EN 1838), HF-N11 (560.9.15: Sicherheitsleuchten sichtbar/lesbar kennzeichnen, Verteiler/Stromkreis/Leuchtennummer an oder nahe der Leuchte), HF-N12 (OIB RL2 Tabelle 6: Garagen 250-1600 m2 nur Fluchtwege-Spalte, Wohngebaeude nach Gebaeudeklasse/Fluchtniveau), HF-N13 (OIB RL2.2 5.5.3: Garage >250 m2 verweist auf Tabelle 6). Jede Quelle mit 'Grenze:'-Absatz gegen Uebergeneralisierung.
> „HF-N11: 'Sicherheitsleuchten und zugehoerige Komponenten muessen sichtbar und lesbar gekennzeichnet sein. Angaben zu Verteiler, Stromkreis und Leuchtennummer sind an oder nahe der Leuchte anzubringen.'“
> „HF-N12: 'Garagen ueber 250 bis 1600 m2 werden in der auf Fluchtwege begrenzten Spalte gefuehrt'“
> „HF-N13: 'Fuer Garagen mit mehr als 250 m2 verweist 5.5.3 zur Sicherheitsbeleuchtung auf Tabelle 6 der OIB-Richtlinie 2.'“
**Linien:** keine (Textseite)
**DXF-Abgleich:**  · Handles — · kein Geometrie-Abgleich moeglich — Quellenregister ohne Planbezug
**Bewertung:** neu → leuchten_kennzeichnung + garagen_erforderlichkeit: (a) Jede Sicherheitsleuchte traegt sichtbar/lesbar Verteiler-, Stromkreis- und Leuchtennummer an oder nahe der Leuchte (OVE E 8101:2025-10 560.9.15) — deckt Engine-Praxis circuit_hint-Labels, bisher keine NB-Regel; (b) Erforderlichkeits-Trigger: Garage >250 bis 1600 m2 -> Sicherheitsbeleuchtung nur fuer Fluchtwege (OIB RL2 Tab.6 + RL2.2 5.5.3) — Enis-Lane (normwissen/OIB), kein Widerspruch zu NB-R01..R27

## S. 74 — GRUNDLAGEN — Weitere Originalquellen, keine vermischten Ausgaben
**Bereich:** Quellen-Disziplin Normausgaben
**Bild:** Reine Textseite. Dokumentiert je Norm exakt die gelesenen Seiten (E 8101:2019 Anhang 56.A informativ vs. 2025 normativ; OIB RL2/2.2; EN 50172 Volltext lokal nicht vorhanden und nicht als gelesen ausgegeben; R12-2 nur als AC-Corrigendum vorhanden). Kernprinzip: keine vermischten Ausgaben, keine erfundenen Abschnittsnummern/Pruefintervalle, 1138 indexierte Dateien sind Bestandserfassung und keine Lektuere.
> „'EN 50172: kein eindeutig vorhandener eigenstaendiger Volltext gefunden. ... Keine daraus erfundenen Abschnittsnummern oder Pruefintervalle verwendet.'“
> „'Massgeblich ist der dokumentierte Leseumfang der tatsaechlich zitierten Quellen.'“
**Linien:** keine (Textseite)
**DXF-Abgleich:**  · Handles — · kein Geometrie-Abgleich moeglich — Quellenseite
**Bewertung:** bestaetigt:NB-R22

## S. 75 — GRUNDLAGEN — Die vorhandene Lichtberechnung richtig einordnen
**Bereich:** Lichtberechnung Hausfeld 116 (Relux-artig, 18 Leuchten, 3 Rechenraeume)
**Bild:** Reine Textseite. Ordnet die projektspezifische 'Lichtberechnung Hausfeld 116.pdf' ein: DG1 Stiege 1 mit 3x Schrack NLKSC009ML, Raum 2 mit 3x demselben Produkt, Raum 3 mit 5x NLKWID039E + 7x NLKWIC039E corridor lenses; Rechennutzebene 0,20 m; Widerspruch Raumhoehe 2,50 m vs. Montagehoehe 2,80 m ist vor Uebertragung zu klaeren. Kernaussagen: Symboltausch (RIVO-Block) aendert weder Produkt noch Photometrie; die Berechnung beweist nicht die gesamte 65er-DXF-Bilanz; Mollgasse ist Gestaltungs-/Erklaerungsreferenz, keine Normausgabe.
> „'Ein RIVO-CAD-Block tauscht ausserdem nicht das geplante Leuchtenprodukt oder dessen Photometrie aus.'“
> „'Eine Boden-Mittellinienanforderung darf nicht stillschweigend mit dem Ergebnis einer 0,20 m-Nutzebene gleichgesetzt werden.'“
> „'Die Mollgasse-Vorlage ist eine Gestaltungs-/Erklaerungsreferenz, keine Hausfeld-Geometrie oder Normausgabe.'“
**Linien:** keine (Textseite)
**DXF-Abgleich:**  · Handles — · kein Geometrie-Abgleich — Einordnungsseite; Produktliste stuetzt die Trennung Symbol-Rolle vs. Photometrie-Produkt
**Bewertung:** bestaetigt:NB-R10

## S. 76 — QUELLENPFADE — Die tatsaechlich verwendeten lokalen Originale
**Bereich:** Pfad-Register (EN 1838, E 8101 2019/2025, R12-2/AC, OIB 2/2.2, Lichtberechnung, Mollgasse, VTP-Plaene 1.DG/1.Stock/2.DG)
**Bild:** Reines Pfad- und Leseumfang-Register: 11 Quellen-Eintraege mit Repo-relativem Pfad, Seitenzahl und gelesenen PDF-Seiten (u.a. MOLLGASSE = Notbeleuchtungen zeichnen.pdf, 95 Seiten, 1-95 vollstaendig gelesen; Hausfeld-VTP-Einzelplaene je 1 Seite). Keine fachliche Regelableitung auf dieser Seite.
**Linien:** keine (Textseite)
**DXF-Abgleich:**  · Handles — · kein Abgleich — Registerseite
**Bewertung:** kein_regelgehalt

## S. 77 — QUELLENPFADE FORTSETZUNG — Die tatsaechlich verwendeten lokalen Originale
**Bereich:** Pfad-Register Rest (VTP EG + Keller)
**Bild:** Fortsetzung des Pfad-Registers mit nur zwei Eintraegen: HF_PLAN 20-011_22haus116_VTP_EG.pdf und _Keller.pdf, je 1 Seite, je vollstaendig gelesen. Restseite weitgehend leer.
**Linien:** keine (Textseite)
**DXF-Abgleich:**  · Handles — · kein Abgleich — Registerseite
**Bewertung:** kein_regelgehalt

## S. 78 — GRUNDLAGEN — Pruefstand und konkrete Grenzen
**Bereich:** Technischer Symboltausch, Skalierung, Layer, Nachweisgrenzen
**Bild:** Reine Textseite mit Pruefstand-Bilanz: 65 physische Positionen + 20 Legendendarstellungen = 84 ersetzte INSERT-Entities (ein 1DG-Kind-INSERT doppelt genutzt); Positionen ueber grafischen Bezugspunkt verglichen, Restfehler <0,00001 mm; RZ proportional skaliert, Antipanik-Block bei gleicher Breite ~31,55 % hoeher (anderes Seitenverhaeltnis, kein verzerrtes Piktogramm); eigener weisser RIVO-Antipanik-Layer wegen BYLAYER-Fuellung; Lehr-Szenen auf abschaltbaren HF_LEHR-Layern. Grenzen: tuerkise 2D-Linie ist kein 3D-Sichtnachweis; Aussentuer und Hof sind nicht automatisch genehmigter Endausgang und sicherer Bereich; technisch ersetzt heisst nicht fachlich freigegeben.
> „'Eine tuerkise 2D-Linie ist kein dreidimensionaler Sichtnachweis.'“
> „'Aussentuer und Hof sind nicht automatisch genehmigter Endausgang und sicherer Bereich.'“
> „'Technisch ersetzt bedeutet nicht automatisch fachlich freigegeben.'“
> „'Oertliche Erklaerung: 58 Positionen raeumlich erklaert, 7 mit konkreter Teilfrage, 0 noch nicht erklaerbar.'“
**Linien:** keine (Textseite); erwaehnt tuerkise Blicklinien und HF_LEHR-Szenenlayer in den CAD-Kopien
**DXF-Abgleich:**  · Handles — · Zahlenprobe gegen evidenz-JSONs: Index-Positionssumme 65 (UG 35 + EG 13 + 1OG 7 + 1DG 7 + 2DG 3) = PDF-Angabe 65; JSON n_leuchten-Summe 67 (UG 37) enthaelt 2 UG-Zusatzinstanzen, siehe S.80-Befund
**Bewertung:** bestaetigt:NB-R25

## S. 79 — KONKRETE RESTFRAGEN — Oertlich begrenzte Fragen, keine verdeckten Skips
**Bereich:** 7 Teilfragen: UG-RZ-010/022/023/029, EG-RZ-003, 1OG-RZ-005, 1DG-RZ-005
**Bild:** Reine Textseite: 7 namentlich gelistete offene Positionen, alle mit demselben Fragetyp — tatsaechliche Front-/Rueckseitenmontage bzw. zugewandte Schildseite fuer eine bestimmte Ankunft (P2/P3) ist aus dem Grundriss allein nicht nachweisbar; ausdruecklich 'keine fiktive beidseitige Lesbarkeit'. Unklare Faelle werden als offene Frage dokumentiert statt geraten.
> „HF-UG-RZ-023: 'Ankunfts- und Zeichenflaechenzuordnung am oestlichen Treppenkopf nicht eindeutig; keine fiktive beidseitige Lesbarkeit.'“
> „HF-1OG-RZ-005: 'Offen bleibt die tatsaechlich zugewandte Schildseite einschliesslich Montage- und Sichtnachweis.'“
**Leuchten im Bild:** HF-UG-RZ-010 ?, HF-UG-RZ-022 ?, HF-UG-RZ-023 ?, HF-UG-RZ-029 ?, HF-EG-RZ-003 ?, HF-1OG-RZ-005 ?, HF-1DG-RZ-005 ?
**Personen:** P2 noerdliche Ankunft (UG, Stgh 1-Vorbereich), P3 aus 1DG bzw. 2DG ueber STGH 2, westliches Laufende
**Linien:** keine gezeichneten Linien (Textseite)
**DXF-Abgleich:**  · Handles — · geschossuebergreifend (UG/EG/1OG/1DG); Front-/Rueckseite ist im 2D-DXF-Block nicht kodiert — deckt sich mit der Restfragen-Begruendung
**Bewertung:** bestaetigt:NB-R07

## S. 80 · UG — REGISTER — Jede physische Leuchte wiederfinden
**Bereich:** Leuchtenindex UG Teil 1 (20 Eintraege, S.7-22 der PDF)
**Bild:** Index-Textseite: 20 UG-Positionen mit ID, Ortsbeschreibung, Erklaer-Seite und Status (18x oertlich erklaert, RZ-010 Teilfrage). Ortslogik bestaetigt die Tuer-RZ-Praxis: RZ an E-Verteilerraum-Nordtuer, KiWa-Raum-Suedtuer, Haustechnik-Tuer zur Schleuse, garagenseitiger Schleusentuer und Schleusentuer in Stgh 1; AP-002 in der Haustechnik (30,70 m2); SL-001 im Stgh 1-Vorbereich; RZ-Kette entlang der westlichen Garagengasse (noerdlich/mittig/suedlich).
> „'Nur physische Positionen; 20 Legendenmuster zaehlen nicht mit. RZ=Rettungszeichen, SL=Aufheller-CAD-Zuordnung, AP=Antipanik-CAD-Zuordnung.'“
> „'Technischer Ersatz ist bei allen 65 Positionen erfolgt; die Erklaerungstiefe bleibt getrennt ausgewiesen.'“
**Leuchten im Bild:** HF-UG-RZ-004 ?, HF-UG-RZ-002 ?, HF-UG-RZ-003 ?, HF-UG-RZ-005 ?, HF-UG-RZ-006 ?, HF-UG-RZ-009 ?, HF-UG-RZ-007 ?, HF-UG-RZ-010 ?, HF-UG-SL-001 aufheller, HF-UG-RZ-011 ?, HF-UG-RZ-008 ?, HF-UG-AP-002 antipanik, HF-UG-RZ-014 ?, HF-UG-RZ-016 ?, HF-UG-RZ-015 ?, HF-UG-RZ-013 ?, HF-UG-RZ-012 ?, HF-UG-RZ-018 ?, HF-UG-RZ-017 ?, HF-UG-RZ-030 ?
**Linien:** keine (Indexseite)
**DXF-Abgleich:** Hausfeldstraße_UG_Notbeleuchtung_RIVO.dxf · Handles — · evidenz-JSON UG: n_leuchten=37 (32 RZ, 4 AP, 1 Aufheller); Index S.80+81 nennt nur 35 UG-Positionen — UG-RZ-001 und UG-AP-001 kommen im Index nicht vor, und das JSON enthaelt 2 raeumlich abgesetzte Instanzen bei x~70,7 m mit abweichenden Skalen (Handles 60572 down-RZ, 60592 Antipanik) = mutmassliche Zweit-/Detaildarstellung; Index-Gesamtsumme 65 stimmt mit PDF-Angabe '65 physische Positionen' ueberein
**Bewertung:** bestaetigt:NB-R19

## S. 81 — LEUCHTENINDEX FORTSETZUNG — Jede physische Leuchte wiederfinden
**Bereich:** Leuchtenindex UG Teil 2 (15 Eintraege) + EG Teil 1 (6 Eintraege)
**Bild:** Index-Textseite: restliche UG-Positionen (Garagengasse Ost, Schleusen-Tuerfolge Garage->Schleuse->Stgh 2-Vorbereich mit RZ-019/020/021, KiWa- und E-Verteilerraum-Tueren, Verbindungsflur, FRR2-Flurarme mit AP-003/004, LET-/EI2-Tuer) und erste EG-Positionen (STGH1: Gang vor Tuer 01, westliche Aussentuer, Tuer 03, Zusammenlauf suedlich des Lifts, SL im freien Gang, oestliche Aussentuer). Drei Teilfragen (RZ-022/023/029) auch hier ausgewiesen. Die lueckenlose Tuer-fuer-Tuer-Belegung der Schleusenfolge bestaetigt die Tuer-RZ-Kette.
> „Schleusenfolge Stgh 2: 'Garagenseitige suedliche Tuer der Stgh 2-Schleuse' -> 'Oestliche Tuer aus der Schleuse in den Stgh 2-Vorbereich' -> 'Stgh 2-Vorbereich unmittelbar hinter der Schleuse' (RZ-019/020/021, je eigene Position)“
**Leuchten im Bild:** HF-UG-RZ-031 ?, HF-UG-RZ-032 ?, HF-UG-RZ-019 ?, HF-UG-RZ-020 ?, HF-UG-RZ-021 ?, HF-UG-RZ-022 ?, HF-UG-RZ-023 ?, HF-UG-RZ-024 ?, HF-UG-RZ-027 ?, HF-UG-RZ-026 ?, HF-UG-RZ-025 ?, HF-UG-AP-004 antipanik, HF-UG-RZ-029 ?, HF-UG-RZ-028 ?, HF-UG-AP-003 antipanik, HF-EG-RZ-002 ?, HF-EG-RZ-001 ?, HF-EG-RZ-003 ?, HF-EG-RZ-004 ?, HF-EG-SL-001 aufheller, HF-EG-RZ-006 ?
**Linien:** keine (Indexseite)
**DXF-Abgleich:**  · Handles — · geschossgemischt UG+EG; EG-Anteil des Index (gesamt 13 ueber S.81+82) deckt sich exakt mit evidenz-JSON EG n_leuchten=13 (9 RZ, 2 AP, 2 Aufheller)
**Bewertung:** bestaetigt:NB-R01

## S. 82 — LEUCHTENINDEX FORTSETZUNG — Jede physische Leuchte wiederfinden
**Bereich:** Leuchtenindex EG Teil 2 (7 Eintraege) + 1OG (7) + 1DG (7)
**Bild:** Index-Textseite: EG-Rest (STGH2 mit RZ westlich des Stiegenlaufs, Aussentuer, AP unmittelbar ausserhalb der westlichen Tuer, SL suedlich des Stiegenlaufs; Muellraum mit AP auf zentraler freier Bodenflaeche + RZ an noerdlicher zweifluegeliger Tuer) sowie 1OG und 1DG. Auffaellig: 1OG- und 1DG-Eintraege sind positionsgleich benannt (gleiche 7 Orte an STGH 1/2: unterer Gang am Zugang, Gangecke, Zugang zum querliegenden Stiegenlauf, Knick, freier Gang, rechtes Podest, westliches Laufende) = identisches Regelgeschoss-Muster; je eine Teilfrage (RZ-005 westliches Laufende).
> „Muellraum-Paar: 'Muellraum, zentrale freie Bodenflaeche' (AP-002) + 'Muellraum, noerdliche zweifluegelige Tuer' (RZ-009)“
> „Stiegenbezug durchgaengig: 'rechtes Podest zwischen Zugang und Stiegenantritt', 'Knick zwischen querliegendem und linkem Stiegenabschnitt'“
**Leuchten im Bild:** HF-EG-RZ-007 ?, HF-EG-RZ-005 ?, HF-EG-AP-001 antipanik, HF-EG-RZ-008 ?, HF-EG-SL-002 aufheller, HF-EG-AP-002 antipanik, HF-EG-RZ-009 ?, HF-1OG-RZ-007 ?, HF-1OG-RZ-002 ?, HF-1OG-RZ-003 ?, HF-1OG-RZ-001 ?, HF-1OG-RZ-006 ?, HF-1OG-RZ-004 ?, HF-1OG-RZ-005 ?, HF-1DG-RZ-007 ?, HF-1DG-RZ-002 ?, HF-1DG-RZ-003 ?, HF-1DG-RZ-001 ?, HF-1DG-RZ-006 ?, HF-1DG-RZ-004 ?, HF-1DG-RZ-005 ?
**Linien:** keine (Indexseite)
**DXF-Abgleich:**  · Handles — · geschossgemischt EG/1OG/1DG; evidenz-JSONs decken exakt: 1OG n_leuchten=7 (Handles 12FF7..130B7) und 1DG n_leuchten=7 (22731..227F1), Blocktypen/Rotationen der beiden Geschosse paarweise nahezu identisch (left/right/down, gleiche welt_pfeil_deg-Muster) — stuetzt die Regelgeschoss-Wiederholung; PDF S.78 nennt genau hierzu den doppelt genutzten 1DG-Kind-INSERT
**Bewertung:** bestaetigt:NB-R05

## S. 83 · 2DG — LEUCHTENINDEX FORTSETZUNG — Jede physische Leuchte wiederfinden
**Bereich:** Leuchtenindex 2DG (3 Eintraege, Abschluss-Seite 83/83)
**Bild:** Letzte Index-Textseite mit den drei 2DG-Positionen, alle oertlich erklaert: RZ-001 STGH 1 Podest vor Zugang 13 und Stiegenantritt (S.61), RZ-003 STGH 1 linker Knick des L-foermigen Stiegenlaufes (S.62), RZ-002 STGH 2 rechtes Podest am Antritt des geraden Laufes (S.63). Oberstes Geschoss traegt nur noch stiegenbezogene RZ an Podest/Antritt/Knick — Abwaerts-Sichtkette in die Stiegenhaeuser.
> „'STGH 1 im 2DG, Podest vor Zugang 13 und Stiegenantritt'“
> „'STGH 2 im 2DG, rechtes Podest am Antritt des geraden Laufes'“
**Leuchten im Bild:** HF-2DG-RZ-001 left, HF-2DG-RZ-003 left, HF-2DG-RZ-002 left
**Linien:** keine (Indexseite)
**DXF-Abgleich:** Hausfeldstraße_2DG_Notbeleuchtung_RIVO.dxf · Handles 35282, 352A2, 352C2 · 3 Index-Eintraege = 3 JSON-Leuchten, Deckung exakt; alle drei RIVO_ARR_left auf Layer E_Sicherheitsbeleuchtung, welt_pfeil_deg 176,71 / 180,33 / 266,71 = Pfeile in die jeweilige Abstiegs-/Weiterrichtung, xscale 31,114
**Bewertung:** bestaetigt:NB-R05
