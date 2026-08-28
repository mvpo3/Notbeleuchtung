# Kaufel Planungshandbuch — „Planungsgrundlagen Sicherheitsbeleuchtung", ABB Kaufel, 6. Auflage (© 2016, Dok-Nr. 460.102.DE.06)
**Quelle:** knowledge/Kaufel Planungshandbuch.pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
**Einordnung:** Referenz-Praxis (Hersteller-Planungshandbuch, ABB Kaufel GmbH, Berlin — **Deutschland**; deutsche Rechts-/Normlage: MBO, MLAR, ArbStättV/ASR, DIN V VDE V 0108-100. AT-Übertragung nur, wo EN-Normen zitiert werden; DE-only-Spalte beachten)

## Relevanz für die Engine

Das Handbuch ist die beste bisher extrahierte Quelle für **Referenz-Praxis** in der
Entscheidungs-Hierarchie (LB-explizit → **Referenz-Praxis** → EN-1838/ÖNorm-Default → OVE-Verbote):

1. **Platzierungs-Checkliste** (S. 43–45, 78–79): vollständige, praxis-konsolidierte Liste
   aller Punkte, an denen Sicherheitsleuchten montiert werden MÜSSEN — inkl. der
   entscheidenden Faustformel **„nahe" = max. 2 m horizontale Entfernung** (deckt sich mit
   EN 1838, aber hier explizit als Planungsregel formuliert). Direkt umsetzbar in Leonis'
   Platzierungs-Strategien.
2. **Gebäudetyp-Tabelle** (S. 13, Tab. 02 nach DIN V VDE V 0108-100): Lux / Umschaltzeit /
   Betriebsdauer / Dauerschaltung je Nutzungsart — das ist genau die Struktur, die Enis'
   `NormRegelwerk` bzw. eine LB-Plausibilisierung braucht (DE-Werte, in AT über
   OVE/ÖNORM-Pendants bzw. TRVB gegenprüfen).
3. **Stromkreis-Regeln** (S. 39): max. 20 Leuchten/Endstromkreis, 60-%-Belastungsregel,
   **Zwei-Stromkreis-Redundanz** („in Räumen/Rettungswegen mit mehr als einer Leuchte
   abwechselnd auf zwei Endstromkreise aufteilen") — relevant für den getrennten
   Sicherheitskreis in der Mission und spätere Stromkreis-Zuordnung im Plan.
4. **Projektierungs-Workflow** (Kap. 5, S. 76–89): der 9-Schritte-Ablauf
   (Nutzung → Brandabschnitte → Leuchten festlegen → Rettungswegbeleuchtung → RZ-Kennzeichnung
   → Unterstationen → Netzüberwachung → Batterie/Ladeteil → Schnittstellen) ist eine
   Blaupause für die Pipeline-Reihenfolge der Engine.
5. **Hersteller-Projektierungstabellen** (S. 78, Abb. 28): Leuchtenabstands-Werte sind
   leuchtenspezifisch (Lichtverteilungskurve!) — die Engine darf Abstände NICHT generisch
   hardcoden, sondern braucht pro `catalog_key` eine Abstandstabelle (h → Xa/Xb/Ya/Yb).

## Dokument-Landkarte

| Kap. | Seiten | Inhalt | Engine-Relevanz |
|------|--------|--------|-----------------|
| Vorwort | 4–5 | 6. Auflage, DE-Normenstand | Einordnung |
| 1 Grundlagen | 7–25 | Schutzziel, Definitionen, wann/wo Pflicht (Arbeitsschutz + Baurecht), Vorschriften-Übersicht, Anforderungs-Tabelle 02, Auszüge Musterverordnungen (Versammlungs-, Verkaufs-, Beherbergungsstätten, Schulen, Garagen, Hochhäuser, Krankenhäuser, Fliegende Bauten) | Hoch (Gebäudetyp-Anforderungen) |
| 2 Herangehensweise | 27–39 | CPS/LPS/Einzelbatterie-Wahl, SVHV/SVUV-Unterbringung (EltBauVO/MLAR), Batterieraum, Endstromkreise, Brandabschnitte, Gebäudeklassen MBO | Mittel (Stromkreise, Brandabschnitte) |
| 3 Sicherheitsbeleuchtung | 41–48 | Sicherheitszeichen (ISO 7010), Montageorte-Checkliste, Antipanik, EN-1838-Zusatzregeln, Erst-/wiederkehrende Prüfungen | Sehr hoch (Platzierung) |
| 4 Konzepte viaFlex | 51–72 | Produktkonzept (Strang/Einzel, zweite Einspeisung, Loop-Prinzip ohne E30) | Niedrig (produktspezifisch, überflogen) |
| 5 Praxis/Projektierung | 75–123 | 9-Schritte-Projektierung, virtuelle Brandabschnitte, Leuchten auszählen, US-Module, Netzüberwachung, Batterie-/Ladeteil-/Lüftungsberechnung, Projektierungstabellen 1 h/3 h/8 h × 4 Batterietypen (Tab. 09–20) | Hoch (Workflow + CPS-Auslegung) |
| 6 Batterien | 125–134 | Bauarten (OGiV/OPzS/OGi/NiCd), Temperatureinfluss, Lebensdauer, Wartung | Niedrig–mittel |
| 7 Prinzipdarstellung | 136–137 | viaFlex Systemschaltbild | Niedrig |

## Planungsregeln-Tabelle

| ID | Kapitel (Seite) | Regel/Faustformel | Werte | zitierte Norm | DE-only? |
|----|-----------------|-------------------|-------|---------------|----------|
| KAUFEL-R1 | 3.2 (S. 43–45, 78–79) | Definition „nahe" für alle Montageorte-Regeln der Sicherheitsleuchten | max. **2 m horizontale Entfernung** | DIN EN 1838 (Anm. des Handbuchs) | nein |
| KAUFEL-R2 | 3.2 (S. 43) | Sicherheitsleuchte außerhalb und nahe jedem letzten Ausgang; NEU: bis zum sicheren Bereich (Sammelplatz) | ≤ 2 m | DIN EN 1838 Pkt. 4.1 | nein |
| KAUFEL-R3 | 3.2 (S. 43) | Sicherheitsleuchte an vorgeschriebenen Notausgängen und Sicherheitszeichen | — | DIN EN 1838 Pkt. 4.2 | nein |
| KAUFEL-R4 | 3.2 (S. 43) | Sicherheitsleuchte nahe Treppen, jede Treppenstufe direkt beleuchten | ≤ 2 m | DIN EN 1838 | nein |
| KAUFEL-R5 | 3.2 (S. 44) | Sicherheitsleuchte nahe jeder Kreuzung, Fluchtrichtungsänderung, Niveauänderung | ≤ 2 m | DIN EN 1838 | nein |
| KAUFEL-R6 | 3.2 (S. 44, 78) | Erste-Hilfe-Stellen, Brandmelde-/Brandbekämpfungseinrichtungen beleuchten; NEU auch: Fluchtgeräte, Schutzbereiche und Toiletten-Alarmeinrichtungen für Menschen mit Behinderung | mind. **5 lx**, gemessen 2 cm über Boden; ≤ 2 m | DIN EN 1838 | nein |
| KAUFEL-R7 | 3.2 (S. 44, 77) | Rettungswege bis 2 m Breite: Mittelachse 1 lx, mittlere 50 % der Breite ≥ 0,5 lx; Messhöhe 2 cm | 1 lx / 0,5 lx / Messhöhe 2 cm | EN 1838, EN 50172 | nein |
| KAUFEL-R8 | 3.2 (S. 44) | Breitere Rettungswege (> 2 m): als mehrere 2-m-Streifen behandeln ODER als Antipanikfläche ausleuchten | Streifenbreite 2 m | DIN EN 1838 | nein |
| KAUFEL-R9 | 3.3 (S. 46) | Antipanikbeleuchtung: horizontale Beleuchtungsstärke ≥ 0,5 lx; Randstreifen 0,5 m ausgenommen | 0,5 lx; Rand 0,5 m | DIN EN 1838 | nein |
| KAUFEL-R10 | 3.4 (S. 46) | Gleichmäßigkeit auf Mittellinie des Rettungswegs: Verhältnis max:min Beleuchtungsstärke | ≤ **40:1** | DIN EN 1838 | nein |
| KAUFEL-R11 | 3.4 (S. 46) | Farbwiedergabe für Erkennung der Sicherheitsfarben | Ra ≥ 40 | DIN EN 1838 | nein |
| KAUFEL-R12 | 3.4 (S. 46) | Hochlaufzeit Sicherheitszeichen im Notbetrieb: 50 % der Mindestleuchtdichte in 5 s, 100 % (2 cd/m²) in 60 s; Abweichung Arbeitsstätten lt. ASR: 100 % Beleuchtungsstärke in 15 s | 2 cd/m² / 5 s / 60 s / 15 s | EN 1838 Pkt. 5.1, 5.3; ASR | ASR-Teil: ja |
| KAUFEL-R13 | 3.4 (S. 46) | Reflektiertes Licht darf bei Auslegung nicht angesetzt werden; Ausnahme: erste Reflexion indirekt strahlender Leuchten/Deckenfluter (mit Wartungswert der Fläche) | — | DIN EN 1838 | nein |
| KAUFEL-R14 | 3.1 (S. 42) | RZ-Montagehöhe: mind. 2 m über Boden, aber nicht höher als 20° über horizontaler Blickachse ab kürzester Betrachtungsentfernung beim Betreten des Rettungswegs | ≥ 2 m; ≤ 20° | EN 1838 | nein |
| KAUFEL-R15 | 3.1 (S. 42) | Piktogramme der Rettungszeichenleuchten nach ISO 7010; Leuchten nach EN 60598-2-22 (auch integrierte Allgemeinleuchten) | — | DIN EN ISO 7010; EN 60598-2-22; DIN 4844-1:2012 + DIN ISO 3864-1 | DIN 4844: ja |
| KAUFEL-R16 | 3.1 (S. 42), 1.7 | Schaltungsart-Grundregel: Rettungszeichenleuchten in **Dauerschaltung**, Sicherheitsleuchten in **Bereitschaftsschaltung**; im Bereitschaftsbetrieb Netzüberwachung jedes Endstromkreises der Allgemeinbeleuchtung | — | DIN VDE 0100-560 Pkt. 560.9.5; EN 50172 | Norm-Nr. DE, Prinzip EN |
| KAUFEL-R17 | 5.4 (S. 78) | Systemintegrität: Beleuchtung eines Bereichs durch **mindestens zwei Leuchten** an mindestens zwei unterschiedlichen Schutzeinrichtungen (Stromkreisen) | ≥ 2 Leuchten, ≥ 2 Stromkreise | DIN EN 1838 (Praxis-Konsolidierung) | nein |
| KAUFEL-R18 | 5.4 (S. 78) | Sicherheitsleuchten durchgängig mindestens 2 m über dem Boden montieren | ≥ 2 m | DIN EN 1838 | nein |
| KAUFEL-R19 | 2.6 (S. 39) | Max. Leuchten pro Endstromkreis (Dauer- und/oder Bereitschaftsbetrieb gemischt) | **20 Leuchten** | DIN V VDE V 0108-100 Pkt. 4.4.9 | ja (Vornorm; AT: OVE-Pendant prüfen) |
| KAUFEL-R20 | 2.6 (S. 39) | Belastung Endstromkreis ≤ 60 % des Nennstroms der Schutzeinrichtung; Tab. 06: 10 A→6 A/1.320 W · 8 A→4,8 A/1.056 W · 6 A→3,6 A/792 W · 5 A→3 A/660 W · 4 A→2,4 A/528 W · 3,15 A→1,89 A/415,8 W · 2 A→1,2 A/264 W | 60 %; Tab.-Werte | DIN VDE 0100-560 Pkt. 9.2 | Norm-Nr. DE |
| KAUFEL-R21 | 2.6 (S. 39), 5.5 (S. 79) | Redundanz: in Räumen und an Rettungswegen mit > 1 Leuchte diese **abwechselnd auf zwei Endstromkreise** aufteilen | 2 Kreise, alternierend | DIN V VDE V 0108-100 Pkt. 4.4.3 | ja (Vornorm) |
| KAUFEL-R22 | 2.7/5.2 (S. 38, 76–77) | Planung nach Brandabschnitten; MLAR erlaubt Brandabschnitte bis **1.600 m²** (Ausnahme NRW); größere Flächen in „virtuelle Brandabschnitte" < 1.600 m² aufteilen; Ausfall eines Brandabschnitts darf nicht weitere Brandabschnitte ausfallen lassen | 1.600 m² | MLAR 2005-11 Pkt. 5.2.2 | ja |
| KAUFEL-R23 | 2.6 (S. 35) | Verzicht auf Funktionserhalt der Leitungsanlage inkl. Verteiler zulässig, wenn Stromversorgung nur einen Brandabschnitt (< 1.600 m²) in einem Geschoss oder nur einen Treppenraum versorgt | < 1.600 m² | MLAR | ja |
| KAUFEL-R24 | 2.7 (S. 38) | Innere Brandwände unterteilen ausgedehnte Gebäude in Abständen von max. 40 m (F90) | 40 m | MBO | ja |
| KAUFEL-R25 | 1.6 (S. 13, Tab. 02) | Gebäudetyp-Anforderungen (Auszug): Versammlungsstätten/Theater/Kino, Fliegende Bauten, Ausstellungshallen, Verkaufsstätten, Restaurants, Flughäfen/Bahnhöfe: **1 lx / 1 s / 3 h**, RZ-Dauerschaltung · Beherbergungsstätten/Heime + Wohnhochhäuser: **1 lx / 1 s / 8 h** (3 h bei Leuchttaster+Zeitlicht) · Schulen + sonstige Hochhäuser: 1 lx / 1 s / 3 h · Parkhäuser/Tiefgaragen: **1 lx / 15 s / 1 h** · Rettungswege in Arbeitsstätten: 1 lx / 15 s / 1 h, Dauerschaltung nicht erforderlich · Arbeitsplätze bes. Gefährdung: **≥ 15 lx / 0,5 s** / Dauer der Gefährdung · Bühnen: **3 lx / 1 s / 3 h**; Umschaltzeit 1 s je nach Panikrisiko bis 15 s | s. links | DIN V VDE V 0108-100:2010-08 Anhang A (Tab. A.1) | ja (Struktur EN 50172-nah; AT-Pendant nutzen) |
| KAUFEL-R26 | 1.7.1 (S. 15) | Arbeitsstätten (ASR): mind. 1 lx nach längstens 15 s; bei erhöhter Unfallgefahr mind. 15 lx (besser 10 % der Allgemeinbeleuchtung) nach längstens 0,5 s; Gleichmäßigkeit < 40:1; Nennbetriebsdauer min. 1 h; RZ-Dauerschaltung nicht erforderlich | 1 lx/15 s; 15 lx/0,5 s; 1 h | ASR A2.3, A3.4/3 | ja |
| KAUFEL-R27 | 1.7.1 (S. 16) | Betriebsmäßig verdunkelte Versammlungsräume/Bühnen/Szenenflächen: Bereitschaftsschaltung; **keine automatische Rückschaltung nach Netzwiederkehr** (manuelle Quittierung); geschaltete Bereitschaftsschaltung für Sicherheitsleuchten unzulässig | — | DIN V VDE V 0108-100 | ja (Vornorm) |
| KAUFEL-R28 | 1.7.2 (S. 16–25) | Wo Sicherheitsbeleuchtung je Sonderbau vorhanden sein muss (Raumlisten je Musterverordnung), z. B. Versammlungsstätten: notwendige Treppenräume + Flure, alle Besucherräume (Foyer, Garderobe, WC), Bühnen, Räume für Mitwirkende/Beschäftigte ≥ 20 m² (außer Büros), elektrische Betriebsräume/Haustechnik, bis zu den öffentlichen Verkehrsflächen, Stufenbeleuchtung · Verkaufsstätten: Verkaufsräume > 50 m², Beschäftigtenräume > 20 m², WC > 50 m² · Schulen: Hallen mit Rettungswegen, notwendige Flure/Treppenräume, fensterlose Aufenthaltsräume (+ ggf. verdunkelte/Experimentierräume) · Großgaragen (≥ 1.000 m²): Fahrgassen, Gehwege neben Zu-/Abfahrten, Treppen, Wege zu Ausgängen · Hochhäuser (> 22 m): Rettungswege, Aufzugsvorräume; hohe Gebäude 13–22 m: nur innenliegende notwendige Treppenräume | Schwellwerte s. links | MVStättV 07/2014, MVkVO 07/2014, MBeVO 05/2014, MSchulbauR 04/2009, MGarVO 05/2008, MBO/MHHR | ja (DE-Musterverordnungen; AT: OIB/TRVB-Pendants) |
| KAUFEL-R29 | 1.7.2 (S. 18) | Schwimmbäder ab 1,35 m Wassertiefe: 15 lx auf der Wasseroberfläche, sonst 1 % der Allgemeinbeleuchtung, mind. 1 lx | 15 lx / 1 % / 1 lx | KOK-Richtlinien für Bäder (2013), DGUV Regel 107-001 | ja |
| KAUFEL-R30 | 1.7.2 (S. 24) | Medizinisch genutzte Bereiche: Umschaltzeit max. 15 s; Betriebsdauer **24 h** (3 h wenn Nutzung beendet + Evakuierung < 3 h); Gruppe-2-Räume (OP, Intensiv): 50 % aller Leuchten an SV | 15 s / 24 h / 50 % | DIN VDE 0100-710:2012-10 | Norm-Nr. DE (AT: OVE E 8101 Teil 710 prüfen) |
| KAUFEL-R31 | 3.2 (S. 45) | Blendungsbegrenzung horizontale Rettungswege (Lichtstärke im Bereich 60°–90° gegen Vertikale), je Montagehöhe h: 2,5 m→500 cd · 3,0 m→900 cd · 3,5 m→1.600 cd · 4,0 m→2.500 cd · 4,5 m→3.500 cd · >4,5 m→5.000 cd (Klammerwerte = Arbeitsplätze mit bes. Gefährdung: jeweils das Doppelte, 1.000–10.000 cd); bei Wegen mit vertikaler Komponente in keinem Winkel überschreiten | s. links | EN 1838 (Tab. Blendung) | nein |
| KAUFEL-R32 | 2.1 (S. 28) | Systemwahl: LPS begrenzt auf max. 500 W (3 h) bzw. 1.500 W (1 h); Einzelbatterie = kleine Objekte (Akkutausch ~ alle 4 Jahre); CPS = skalierbar, Batterielebensdauer ≥ 10 Jahre, Standard für größere Objekte | 500 W/1.500 W; 4 J.; 10 J. | EN 50171 | nein (EN) |
| KAUFEL-R33 | 2.4 (S. 31), 5.8 (S. 86) | Batterie-Auslegung: Kapazitätsreserve **25 %** über tatsächlichen Energiebedarf (Alterungskompensation); Lebensdauer-Ende bei 80 % Nennkapazität; Alterungsverlust ≤ 2 %/Jahr, Referenztemperatur 20 °C | 25 % / 80 % / 2 %/a / 20 °C | DIN EN 50171 Pkt. 6.7.2e, 6.12.4 | nein (EN) |
| KAUFEL-R34 | 2.4 (S. 32) | Batterieraum-Lüftung: Q = 0,05 × n × I_gas × C_N × 10⁻³ [m³/h]; natürliche Lüftung: Mindestquerschnitt A = 28 × Q [cm²]; Zu-/Abluft an gegenüberliegenden Wänden, sonst Trennabstand ≥ 2 m | Formeln s. links | DIN EN 50272-2 Pkt. 8.2/8.3 | nein (EN) |
| KAUFEL-R35 | 5.8 (S. 87) | Ladeteil: Wiederaufladung auf 80 % Kapazität in 12 h; Ladestrom I_L = 1/12 × C mit C = I_max × t_Ü (tatsächlich entnommene Kapazität); nächstgrößeres Ladeteil wählen | 80 % / 12 h | EN 50171:2001-11 | nein (EN) |
| KAUFEL-R36 | 5.8 (S. 89) | Netzanschlussleistung CPS: S_NA = S_LT (Eingangsleistung Ladeteil) + S_V (Verbraucherleistung) | Formel | Praxis Kaufel | nein |
| KAUFEL-R37 | 2.3/2.4 (S. 30–33) | Unterbringung SVHV/CPS/Batterie in eigenem elektrischem Betriebsraum: F30–F90-Bauteile je Gebäudeklasse, selbstschließende T30–T90-RS-Tür in Flur (nicht direkt in notwendigen Treppenraum), Anti-Panik-Tür nach außen öffnend, frostfrei/beheizbar, Bodenableitwiderstand 50 kΩ–10 MΩ, elektrolytfester Anstrich, freier Fluchtweg ≥ 600 mm | s. links | EltBauVO §4/§5/§6/§7; DIN EN 50272-2 Pkt. 10 | EltBauVO: ja |
| KAUFEL-R38 | 2.6 (S. 39) | Speisung: Sicherheitsbeleuchtung muss auch bei örtlichem Ausfall (einzelner AV-Endstromkreis) wirksam werden; bei vorhandenem Netz keine automatische Umschaltung auf Sicherheitsstromquelle | — | DIN EN 50172 Pkt. 4.1 | nein (EN) |
| KAUFEL-R39 | 5.7 (S. 84) | Netzüberwachung: **jeder einzelne Endstromkreis** der relevanten Allgemeinbeleuchtung muss auf Ausfall überwacht werden; Überwachung muss auf die Unterstation wirken, die die Sicherheitsbeleuchtung im betroffenen Bereich versorgt | — | EN 50172 | nein (EN) |
| KAUFEL-R40 | 3.5 (S. 47) | Erstprüfung: Messung der lichttechnischen Werte der Sicherheitsbeleuchtung | — | DIN V VDE V 0108-100 Pkt. 7.2; DIN 5035-6 | ja |
| KAUFEL-R41 | 3.6 (S. 47–48) | Prüfregime: täglich Sichtprüfung Anzeigen der Zentrale · wöchentlich Einschalten Sicherheitsstromquelle + Funktionsprüfung Leuchten · monatlich Umschalten jeder Leuchte auf Notbetrieb + Protokoll (lt. DIN V VDE V 0108-100 nur noch jährlich) · jährlich zusätzlich Bemessungsbetriebsdauertest über volle Überbrückungszeit (nicht automatisch auslösen) · mind. alle 3 Jahre Beleuchtungsstärkemessung nach EN 1838 · Prüfbuch (auch elektronisch) | s. links | DIN EN 50172 Pkt. 7.2.2–7.2.4, 6.3; DIN EN 50171 Pkt. 6.11; DIN V VDE V 0108-100 Pkt. 7.3.3/7.3.5 | teils (Vornorm-Abweichung) |
| KAUFEL-R42 | 3.6 (S. 48) | Entladene-Batterie-Risiko nach Prüfung managen, z. B. zwei parallele, zeitversetzt getestete Batterien oder manuelle Testauslösung nach Warnmeldung (12-Monats-Frist) | 12 Monate | DIN EN 50171 Pkt. 6.11 | nein (EN) |
| KAUFEL-R43 | 5.4 (S. 77–78) | Rettungsweg-Ausleuchtung: Mindestabstände der Leuchten aus **herstellerspezifischen Projektierungstabellen** (Lichtverteilungskurven) ableiten; Beispiel Serenga 75L (Optik D), 1,0 lx: h=2,0 m → Abstände Ya 3,0 m / Yb 7,7 m; h=3,0 m → 3,6/10,6 m; h=4,0 m → 1,4/10,8 m (Xa/Xb analog) | Beispielwerte | Hersteller-Daten (Kaufel) | nein (Prinzip universell) |
| KAUFEL-R44 | 5.5 (S. 79) | Rettungszeichen: für **jede Stelle des Gebäudes** muss der Rettungsweg per Rettungszeichen kenntlich sein; Erkennungsweite beachten → RZ-Leuchten in verschiedenen Erkennungsweiten wählen | — | EN 1838 | nein |
| KAUFEL-R45 | 5.6 (S. 80) | Unterstations-Dimensionierung (viaFlex, als Praxis-Größenordnung): 1 Unterstation pro Brandabschnitt; max. 1.500 W, max. 16 Stromkreise, max. 80 Leuchten pro Modul; Unterstation im Endbrandabschnitt → kein Verteiler in Funktionserhalt nötig; brandabschnittsübergreifende Leitungen immer in Funktionserhalt | 1.500 W / 16 / 80 | Hersteller Kaufel | nein (produktspezifisch) |
| KAUFEL-R46 | 5.11 (S. 100–123) | CPS-Projektierungstabellen: je Überbrückungszeit (1 h / 3 h / 8 h) und Batterietyp (Primus verschlossen, OGi, OPzS, NiCd SBLE) für Verbraucherleistung 0,5–15 kW → Batterienennkapazität, Ladeteil, Netzanschlussleistung, Lüftung, Maße/Massen. Beispiel 3 h/Primus: 5 kW → 111 Ah C10, Ladeteil 7,5 A, S_NA 7,2 kVA; 10 kW → 238 Ah, 15 A, 16,3 kVA | s. links | Kaufel-Tabellen (Basis EN 50171/50272-2) | nein (produktspezifisch) |
| KAUFEL-R47 | 6.2 (S. 129) | Batterie-Temperatur-Faustformel: +10 K über 20 °C ⇒ Brauchbarkeitsdauer verschlossener Bleibatterien halbiert (40 °C ⇒ nur 25 % Lebensdauer); NiCd −40…+50 °C einsetzbar | 10 K → −50 % | Herstellerpraxis | nein |
| KAUFEL-R48 | 1.7.2 (S. 25) | Fliegende Bauten: Sicherheitsbeleuchtung in Zelten > 200 m² bei Betrieb nach Einbruch der Dunkelheit; Anforderungen gemäß jeweiliger Nutzung; bei Dunkelheit während Betriebszeit Dauerschaltung | 200 m² | M-FlBauR 05/2007 | ja |
| KAUFEL-R49 | 1.7.2 (S. 16) | Bemessung Besucherzahl Versammlungsstätten: Sitzplätze an Tischen 1 Pers./m² · Sitzreihen + Stehplätze 2 Pers./m² · Stufenreihen 2 Pers./lfm · Ausstellungsräume 1 Pers./m²; Versammlungsstätte ab ≥ 200 Personen | s. links | MVStättV 07/2014 | ja |

## Zitierte Norm-Werte (Quelle-der-Quelle)

Normen, die (noch) nicht als eigener Digest im Repo liegen — Werte hier mit Handbuch-Seite:

- **DIN V VDE V 0108-100:2010-08** (DE-Vornorm, ersetzt Teile der alten VDE 0108) — S. 13:
  Anhang A Tabelle A.1 = Gebäudetyp-Matrix (KAUFEL-R25). Weitere §§: Pkt. 4.4.9
  (20 Leuchten/Kreis, S. 39), Pkt. 4.4.3 (Zwei-Kreis-Aufteilung, S. 39), Pkt. 7.2/7.3.3/7.3.5
  (Prüfungen, S. 47–48). **DE-only** (Vornorm; verbindlich nur bei Verweis in
  Brandschutznachweis/Vertrag, S. 12, 29–30). AT-Gegenstück: ÖVE/ÖNORM E 8002 bzw. heute
  OVE-Regelwerk — nicht 1:1 übernehmen.
- **DIN EN 50172 / VDE 0108-100:2005-01** (Errichternorm Sicherheitsbeleuchtungsanlagen) —
  S. 12, 39, 47, 77, 84: Pkt. 4.1 (Wirksamwerden auch bei Teil-Ausfall, keine automatische
  Umschaltung bei vorhandenem Netz), Pkt. 6.3 (Prüfbuch), Pkt. 7.2.2–7.2.4
  (wöchentlich/monatlich/jährlich), Netzüberwachung jedes AV-Endstromkreises. **EN — auch AT gültig.**
- **DIN EN 50171:2001-11** (CPS-Gerätenorm) — S. 28, 31, 86–87: LPS-Grenzen 500 W/3 h,
  1.500 W/1 h; 25 % Kapazitätsreserve (Pkt. 6.7.2e); Lebensdauer-Ende 0,8×C_N (Pkt. 6.12.4);
  Ladeteil 80 % in 12 h; Prüf-/Batterierisiko Pkt. 6.11. **EN.**
- **DIN EN 50272-2 / VDE 0510-2:2001-12** (Batteriesicherheit) — S. 32–33, 88: Lüftungsformel
  Q = 0,05·n·I_gas·C_N·10⁻³ m³/h (Pkt. 8.2); A = 28·Q cm² (Pkt. 8.3); 2-m-Trennabstand
  (Pkt. 8.4); Batterieraum-Regeln Pkt. 10 (Fluchtweg 600 mm, Bodenableitwiderstand
  50 kΩ–10 MΩ, Blei/NiCd-Trennung Pkt. 10.5); H₂-Explosionsgrenze 4 Vol.-% (S. 131). **EN.**
- **DIN VDE 0100-560:2013-10** — S. 39, 42, 61: Pkt. 9.2 (60-%-Belastungsregel),
  Pkt. 560.9.5 (Netzüberwachung bei Bereitschaftsschaltung), Pkt. 560.5.2/560.8.1
  (Feuerbeständigkeit der Betriebsmittel, Kabelanlagen im Brandfall). **DE-Ausgabe von
  HD 60364-5-56** → AT-Pendant in OVE E 8101 (im Repo, referenzieren statt duplizieren).
- **MLAR 2005-11** (Muster-Leitungsanlagen-Richtlinie) — S. 30, 34–35, 61, 76: Pkt. 5.1.1
  (Funktionserhalt-Grundsatz), Pkt. 5.2.2 (Verteiler-Unterbringung), 1.600-m²-Regel für
  Brandabschnitte/Funktionserhalt-Verzicht. **DE-only** (AT: TRVB E 102 / OIB-RL 2 sinngemäß).
- **EltBauVO (Muster 01/2009)** — S. 31–33: eigener elektrischer Betriebsraum für CPS/LPS
  + Batterien, Türen/Feuerwiderstand, Lüftung ins Freie, frostfrei (§4–§7). **DE-only.**
- **ASR A1.3 (2013), A2.3 (2007/2014), A3.4/3 (2009/2014)** — S. 10, 14–15: Pflichtkriterien
  (gefahrloses Verlassen nicht gewährleistet, erhöhte Gefährdung, Unfallgefahr bei
  Netzausfall); 1 lx/15 s; 15 lx bzw. 10 %/0,5 s; < 40:1; ≥ 1 h. **DE-only** (AT:
  ArbeitnehmerInnenschutz/AStV).
- **Muster-Sonderbauverordnungen** (MVStättV 07/2014, MVkVO 07/2014, MBeVO 05/2014,
  MSchulbauR 04/2009, MGarVO 05/2008, MHHR 04/2008, M-FlBauR 05/2007, MBO 09/2012) —
  S. 16–25, 37–38: Raumlisten + Schwellwerte je Nutzung (KAUFEL-R28), Gebäudeklassen 1–5,
  Feuerwiderstandsklassen F30–F180, Hochhausgrenze > 22 m / hohe Gebäude > 13 m. **DE-only.**
- **DIN VDE 0100-710:2012-10** (medizinische Bereiche) — S. 24: 15 s / 24 h / 50 % der
  Leuchten in Gruppe 2 (KAUFEL-R30). DE-Ausgabe; AT über OVE E 8101-710.
- **DIN EN 12193:2008-04** (Sportstättenbeleuchtung) — S. 18: sportartspezifisches
  Mindestbeleuchtungsniveau für definierte Zeit („geordnetes Beenden der Veranstaltung"). EN.
- **KOK-Richtlinien für Bäder (2013) + DGUV Regel 107-001 (2011-06)** — S. 18:
  Schwimmbad-Werte (KAUFEL-R29). **DE-only.**
- **DIN 5035-6** (Messung/Bewertung Beleuchtung) — S. 47: Messverfahren Erstprüfung. **DE-only.**
- **DIN 4844-1:2012-06 + DIN ISO 3864-1:2012-06** — S. 42: lichttechnische Anforderungen
  Rettungszeichen bei vorhandener Stromversorgung. **DE-only** (Piktogramme selbst: ISO 7010, international).
- **EN 60598-2-22** — S. 42: Leuchtennorm für alle Sicherheits- und Rettungszeichenleuchten. EN.

## Detail-Digest der Planungs-Kapitel

### Kap. 1 — Wann/wo Pflicht (S. 10–25)
Zwei Rechtsstränge (DE): **Arbeitsschutz** (ArbSchG-Gefährdungsbeurteilung → ArbStättV
Anhang 2.3 → ASR) und **Baurecht** (MBO/LBO → Sonderbau-Verordnungen → MLAR). Praxis-Trigger
für Sicherheitsbeleuchtung lt. ASR (S. 15): große Personenbelegung, hohe Geschosszahl,
unübersichtliche Fluchtwege, ortsunkundige Nutzer, große Räume (Hallen, Großraumbüros,
Verkauf), kein Tageslicht; erhöhte Unfallgefahr in Laboren, elektrischen Betriebsräumen,
Schaltwarten, an Baustellen. Tabelle 02 (S. 13) liefert die maschinennutzbare Matrix
Nutzungsart → (Lux, Umschaltzeit, Betriebsdauer, RZ-Dauerschaltung, zulässige
Stromquellen-Typen) — siehe KAUFEL-R25. Fußnoten: 8-h-Anforderung reduzierbar auf 3 h mit
Leuchttastern (von jedem Standort auch bei Dunkelheit erkennbar) + automatischer
Abschaltung; oberirdische Bahnhofsbereiche je Evakuierungskonzept 1 h; DB hat Eigenregelwerk 954.9103.

### Kap. 2 — Systemwahl + Infrastruktur (S. 28–39)
Planung „von außen nach innen": erst globale Festlegungen (Überbrückungszeit), dann Detail.
CPS vs. LPS vs. Einzelbatterie (KAUFEL-R32). SVHV/SVUV in eigenen Betriebsräumen
(EltBauVO/MLAR, KAUFEL-R37); Fernanzeige über potentialfreie Kontakte (betriebsbereit /
Batteriebetrieb / Störung) vorschreiben. Endstromkreis-Regeln KAUFEL-R19–R21.
Brandabschnitte/Gebäudeklassen KAUFEL-R22–R24.

### Kap. 3 — Platzierung + Lichttechnik (S. 42–48)
Kernkapitel für Leonis: Montageorte-Checkliste (KAUFEL-R2–R6), Rettungsweg-Ausleuchtung
(R7–R8), Antipanik (R9), Gleichmäßigkeit (R10), Farbwiedergabe (R11), Hochlaufzeiten (R12),
Reflexionsverbot (R13), RZ-Montagehöhe (R14), Blendungstabelle (R31). Prüfungen R40–R42.
Die Handbuch-Zusammenfassung S. 78–79 ergänzt gegenüber der reinen EN-1838-Liste:
Aufzugskabinen, „außerhalb bis zu den öffentlichen Verkehrsflächen" und die
Behinderten-Einrichtungen (aus EN 1838:2013 „NEU"-Punkten).

### Kap. 5 — Projektierungs-Workflow (S. 76–99)
Schrittfolge: (1) Gebäudemerkmale/Nutzung → (2) Brandabschnitte (inkl. virtueller,
KAUFEL-R22) → (3) Leuchten anhand Grundriss festlegen (EN 1838, EN 12464-1 für
Arbeitsstätten, EN 50172) → (4) Rettungsweg-/Sondereinrichtungs-Beleuchtung mit
Hersteller-Projektierungstabellen (KAUFEL-R43) → (5) RZ-Kennzeichnung lückenlos mit
Erkennungsweiten (KAUFEL-R44) → (6) Leuchten brandabschnittsweise auszählen, alternierend
auf 2 Stromkreise verteilen, Verbraucherleistung summieren; schon in Planungsphase
Stromkreis-/Leuchtennummer + Leuchtentext dokumentieren (Audit-Trail!) → (7)
Netzüberwachungskonzept (KAUFEL-R39; Leitungsüberwachung MLF: bei Ansprechen wird sicherer
Zustand = Licht EIN hergestellt) → (8) Batterie/Ladeteil/Lüftung (KAUFEL-R33–R36, R46) →
(9) Schnittstellen GLT (Meldungen Betrieb/Batteriebetrieb/Störung nach EN 50171,
Lichtsteuerkontakt zum Aufregeln gedimmter Leuchten; Dimm-Betriebsgeräte mit DC-Erkennung
sind für Systeme mit DC-Ausgang ungeeignet). Bus-Planung (LON): max. 64 Knoten/Kanal,
255 gesamt; Leitungslängen je Typ/Topologie (Tab. 08, S. 97), z. B. JY(St)Y 2×2×0,8:
Linie 900 m, freie Topologie 500 m gesamt/320 m Knotenabstand.

### Kap. 6 — Batterien (S. 126–134)
OPzS = Langzeitentladung 1 h bis > 10 h, > 18–20 J. Lebensdauer, Kaufel-Empfehlung
Preis/Leistung; OGi = Kurzzeitentladung ≤ 3 h, hochstromfähig, bis 15 J.; NiCd = −20…+50 °C
Betriebsbereich (kurzfristig −50…+60 °C), > 20 J., erste Wahl bei extremen Temperaturen,
teuer; verschlossene OGiV = 10–12 J., günstig, aber temperaturempfindlich (KAUFEL-R47),
Parallelschaltung vermeiden, Gehäusemaße nicht genormt (Ersatzbeschaffungsrisiko).
Lebensdauer-Ende = 80 % Nennkapazität. Belüftungspflicht gilt für ALLE Bauarten, auch
„verschlossene" (H₂ > 4 Vol.-% = Explosionsgefahr).

## Widersprüche zu bestehenden Digests

- **Kein inhaltlicher Widerspruch zu `EN_1838_notbeleuchtung.md` gefunden** — das Handbuch
  referenziert EN 1838:2013 und deckt sich in allen lichttechnischen Werten (1 lx / 0,5 lx /
  5 lx / 40:1 / Ra 40 / 2 m Montagehöhe / 2-m-„nahe"-Regel / Blendungstabelle).
  Das Handbuch **konkretisiert** darüber hinaus: Messhöhe 2 cm, Zwei-Leuchten-Prinzip
  pro Bereich (KAUFEL-R17) als Praxis-Verschärfung.
- **Achtung Normlagen-Drift (kein Widerspruch, aber Einordnung):** Gebäudetyp-Tabelle 02 und
  alle „1)"–Anforderungen stammen aus der **deutschen Vornorm DIN V VDE V 0108-100:2010-08**
  und den **deutschen Musterverordnungen** — sie sind in AT nicht normativ. Für die Engine:
  als Referenz-Praxis-Ebene nutzbar, aber unterhalb LB-explizit und neben (nicht über) den
  ÖNorm/OVE-Defaults einsortieren; OVE-Verbote aus `OVE_E_8101_niederspannungsanlagen.md`
  bleiben Hard Stop.
- **Prüfintervall-Diskrepanz innerhalb der DE-Quellenlage** (S. 47): EN 50172 fordert
  monatliche Umschaltprüfung jeder Leuchte; DIN V VDE V 0108-100 nur noch jährlich —
  Handbuch weist beide aus. Engine sollte konservativ die EN-50172-Lesart als Default nehmen.

## Offene Punkte / Extraktionslücken

- **Stand:** © 2016 (Copyright-Vermerk S. 140); im Vorwort nur „sechste Auflage" ohne
  Jahreszahl — Normstände der Zitate (EN 1838:2013, MVStättV 07/2014) passen zu 2015/2016.
  Neuere Normstände (DIN EN 50172:2025, EN 50171:2021, EN IEC 62485-2 als
  50272-2-Nachfolger, ArbStättV-Novellen) sind NICHT berücksichtigt.
- Abbildungen 09–20, 27–41 sind im Textextrakt nur als Bildunterschriften enthalten —
  grafische Details (z. B. genaue Geometrie der Blendungs-Winkelzonen, ISO-7010-Piktogramme)
  [Extraktionslücke, Werte aber im Text vorhanden].
- Projektierungstabelle Serenga (S. 78, Abb. 28): Bedeutung der Spalten Xa/Xb vs. Ya/Yb
  (Achsen quer/längs zum Rettungsweg, Abstand Wand vs. Leuchte–Leuchte) ist aus dem
  Textextrakt nicht eindeutig ableitbar [Extraktionslücke — vor Verwendung als
  Abstands-Referenz am PDF-Original klären].
- Tabellen 09–20 (S. 100–123) wurden strukturell + stichprobenartig extrahiert (1 h voll,
  3 h Primus voll, 8 h nur Kopf) — vollständige Zahlenübernahme aller 12 Tabellen bewusst
  ausgelassen (produktspezifische CPS-Auslegung, für Platzierungs-Engine nachrangig).
- Tabelle 02 (S. 13) ist im PDF-Extrakt spaltenverschoben (Fußnoten-Marker 0–3); die hier
  wiedergegebene Zuordnung folgt der bekannten Struktur der DIN V VDE V 0108-100 Tab. A.1 —
  bei Zweifel am PDF-Original gegenprüfen (insb. Bahnhöfe-Fußnote „1 h zulässig").
- MVStättV-Auszüge S. 16–18 mischen im Extrakt Sitzplatz-Bemessungsregeln über mehrere
  Seiten; Einzelwerte je Untertyp (Sportstätten vs. Gaststätten) ggf. am Original verifizieren.
