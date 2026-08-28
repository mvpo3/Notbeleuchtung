# Planung von Elektroanlagen — Teil 9
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 361-400.

Dieser Teil behandelt den Abschluss des Kapitels über Schutz gegen elektrischen Schlag (Kap. 16) mit Berechnungsbeispielen für TN-, TT- und IT-Systeme, gefolgt von Kapitel 17 (zentraler Erdungspunkt und Sicherheitsregeln beim Arbeiten an Anlagen) sowie dem vollständigen Kapitel 18 über Mittelspannungsanlagen (Schaltanlagentypen, Schaltgeräte, Erdung, Netzplanung, Isolationskoordination, Überspannungsschutz und Dimensionierungsformeln).

## Inhalt

### Kap. 16 — TN-System: Abschaltbedingungen und Fehlerstromberechnung

Für das TN-System müssen Kennwerte der Schutzeinrichtungen und Schleifenimpedanz so gewählt werden, dass bei einem Fehler zwischen Außenleiter und Schutzleiter die automatische Abschaltung innerhalb festgelegter Zeiten erfolgt.

**Abschaltbedingung (Schleifenimpedanz):**
- Zs ≤ U0 / Ia — Formel (16.1)
- Zweite Bedingung: I''k1min = IF ≥ Ia — Formel (16.2)

**Fehlerstromberechnung (vereinfacht):**
- IF = 230 V / Zs = 230 V / (ZT + ZL + ZPE + ZPEN) — Formel (16.3)

**Maximale Abschaltzeiten TN-System (Endstromkreise ≤ 32 A; bei Verteilungsstromkreisen: 5 s erlaubt):**

| Bemessungsspannung der Anlage | Abschaltzeit (N nicht verteilt) | Abschaltzeit (N verteilt) |
|---|---|---|
| 230/400 V | 0,4 s | 0,8 s |
| 400/690 V | 0,2 s | 0,4 s |
| 580/1000 V | 0,1 s | 0,2 s |

*(Anmerkung im Quelltext als Tab. 16.2 bezeichnet, obwohl sie inhaltlich IT-System-Zeiten für den zweiten Fehler betrifft — Werte werden wie angegeben übernommen.)*

**Bedingung beim Erdschluss eines Leiters (Spannungsbegrenzung):**
- RB/RE ≤ UT / (U0 − UT) — Formel (16.4)
- Beispielrechnung: RE = 50 V / (230 V − 50 V) = 7,2 Ω — Formel (16.5)

**Symbolerläuterungen:**
- Zs — Schleifenimpedanz
- U0 — Leiter-Erde-Nennspannung
- Ia — Abschaltstrom der Überstromschutzeinrichtung (ÜSE)
- I''k1min — kleinster minimaler Kurzschlussstrom
- RE — Erdübergangswiderstand
- RB — Gesamterdungswiderstand aller Betriebserder
- UT — vereinbarte Grenze der dauernd zulässigen Berührungsspannung

**Rechenbeispiel — Abschaltung der Fehlerströme:**
- Gemessene Schleifenimpedanz an CEE-Steckdose 5-polig 16 A: 1,3 Ω
- Nennspannung: 230 V / 400 V, 50 Hz
- Vorgeschaltete ÜSE: C/16 A; Messtoleranz ±15 %
- Abschaltstrom der ÜSE: Ia = 10 × In = 10 × 16 A = 160 A
- Schleifenimpedanz mit Toleranz: Zs = 1,3 Ω + 15 % = 1,495 Ω
- Minimaler einpoliger Kurzschlussstrom: I''k1min = (0,9 × 400 V) / (√3 × 1,495 Ω) = 139 A
- Ergebnis: Abschaltstrom (160 A) > minimaler Kurzschlussstrom (139 A) → Leitungsschutzschalter löst NICHT aus
- Lösungsvorschläge: (a) Bemessungsstrom der ÜSE reduzieren, z. B. auf C10 A; (b) Leiterquerschnitt erhöhen; (c) ÜSE mit Charakteristik B16 A verwenden

---

### Kap. 16.3 — TT-System

Im TT-System ist der Erdübergangswiderstand RA der Erder praktisch kaum erreichbar klein. Die zulässige Berührungsspannung UT = 50 V kann überschritten werden. Fehlerstromschutzeinrichtungen (RCD) sind unbedingt zusammen mit Überstromschutzeinrichtungen einzusetzen.

**Abschaltbedingungen:**
- Bei Überstromschutzeinrichtung: Zs ≤ U0 / Ia — Formel (16.6)
- Bei RCD: RA ≤ UT / In — Formel (16.7)

**Symbolerläuterungen:**
- RA — Summe der Widerstände von Erder und Schutzleiter
- RB — Betriebswiderstand
- UT — Berührungsspannung
- Ia — Abschaltstrom der Schutzeinrichtung
- In — Bemessungsdifferenzstrom des RCD

**Maximale Abschaltzeiten für TT-System (Endstromkreise ≤ 32 A):**
- Verteilerstromkreise und Endstromkreise > 32 A: max. 1 s
- In Verteilungsstromkreisen mit RCDs zur Selektivität: Abschaltzeit ≤ 0,5 s erlaubt
- Abschaltung unverzögert oder mit kürzer werdenden Auslösezeiten bei steigendem Strom, max. 5 s

**Gleichzeitigkeitsfaktor g für RCDs (Tab. 16.3):**

| Anzahl RCDs | g |
|---|---|
| 2 bis 4 | 0,5 |
| 5 bis 10 | 0,35 |
| Mehr als 10 | 0,25 |

**Rechenbeispiel Erdungswiderstand TT-System:**
- Sicherungsnennstrom 16 A; Abschaltstrom bei 5 s = 72 A; U0 = 230 V
- Erforderlicher Erdausbreitungswiderstand: RA ≤ 230 V / 72 A = 3,19 Ω
- Bei RCD 30 mA: RA ≤ 50 V / 30 mA = 1.666 Ω (leichter erreichbar als 3,19 Ω)

**Berührungs- und Fehlerspannungsberechnung am Stromkreis 4 (Annahmen):**
- RB = 2 Ω, RA = 1,5 Ω, Standortwiderstand RST = 750 Ω, Körperwiderstand RK = 1 kΩ, Netzwiderstand Zi ≈ RN = 1 Ω, Fehlerwiderstand RF = 3,7 kΩ
- Berührungsspannung: UT = RK × U0 / RG = 1 kΩ × 230 V / 5,45 kΩ = 42,2 V < 50 V — Formel (16.8)
- Fehlerstrom: IF = RA × U0 / (RB + RA + RN) = 1,5 Ω × 230 V / (2 + 1,5 + 1) Ω = 76,66 A — Formeln (16.9)
- Fehlerspannung: UF = RA × IF = 1,5 Ω × 76,66 A = 115 V > 50 V

---

### Kap. 16.4 — IT-System

Das IT-System ist ungeerdet und wird eingesetzt, wo hohe Betriebssicherheit gefordert ist: Operationsräume, Hüttenwerke, chemische Industrie, Schiffe.

**Schutz bei indirektem Berühren (nach DIN VDE 0100 Teil 410):**
- Meldung durch Isolationsüberwachung mit zusätzlichem Potentialausgleich, oder
- Abschaltung beim Doppelfehler

**Abschaltbedingung Erdungswiderstand:**
- RA ≤ UT / Id — Formel (16.10)

**Abschaltbedingungen zweiter Fehler:**
- Neutralleiter nicht mit verteilt: ZS ≤ U / (2 × Ia) — Formel (16.11)
- Neutralleiter mit verteilt: Z'S ≤ U0 / (2 × Ia) — Formel (16.12)

**Maximale Abschaltzeiten IT-System (zweiter Fehler, Tab. 16.4):**

| Bemessungsspannung | Abschaltzeit (N nicht verteilt) | Abschaltzeit (N verteilt) |
|---|---|---|
| 230/400 V | 0,4 s | 0,8 s |
| 400/690 V | 0,2 s | 0,4 s |
| 580/1000 V | 0,1 s | 0,2 s |

**Symbolerläuterungen:**
- RA — Erdungswiderstand
- UT — Berührungsspannung
- Id — Fehlerstrom beim ersten Fehler (vernachlässigbare Impedanz zwischen Außenleiter und Schutzleiter oder damit verbundenem Körper; berücksichtigt Ableitströme und Gesamtimpedanz der Anlage gegen Erde)
- ZS — Impedanz der Fehlerschleife (Außenleiter + Schutzleiter des Stromkreises)
- Z'S — Impedanz der Fehlerschleife (Neutralleiter + Schutzleiter des Stromkreises)
- U0 — Bemessungswechselspannung zwischen Außenleiter und Neutralleiter
- U — Bemessungswechselspannung zwischen Außenleitern

**Maximal zulässige Schleifenimpedanz Zs bei U0 = 230 V (Tab. 16.5), nach Leitungsschutzschalter-Charakteristik (B, C, K, Z) und Bemessungsstrom In [A]:**

| In (A) | B ta<0,4 s | B ta<5 s | C ta<0,4 s | C ta<5 s | K ta<0,4 s | K ta<5 s | Z ta<0,4 s | Z ta<5 s |
|---|---|---|---|---|---|---|---|---|
| 0,5 | — | — | 46 | 70,8 | 38,3 | 48,4 | 153 | 153 |
| 1 | — | — | 23 | 35,4 | 19,1 | 24,1 | 78,7 | 78,7 |
| 1,6 | — | — | 14,4 | 22,1 | 11,9 | 15,0 | 47,9 | 47,9 |
| 2 | — | — | 11,5 | 17,7 | 9,5 | 12,0 | 38,3 | 38,3 |
| 3 | — | — | 7,7 | 11,8 | 6,3 | 8,0 | 25,5 | 25,5 |
| 4 | — | — | 5,8 | 8,8 | 4,7 | 5,9 | 19,1 | 19,1 |
| 6 | 7,6 | 7,6 | 3,8 | 5,9 | 3,1 | 4,0 | 12,7 | 12,7 |
| 8 | — | — | 2,8 | 5,7 | 2,4 | 2,9 | 9,5 | 9,5 |
| 10 | 4,6 | 4,6 | 2,3 | 3,5 | 1,9 | 2,4 | 7,6 | 7,6 |
| 13 | 3,5 | 3,5 | 1,7 | 2,7 | — | — | — | — |
| 16 | 2,9 | 2,9 | 1,4 | 2,2 | 1,1 | 2,0 | 4,7 | 4,7 |
| 20 | 2,3 | 2,3 | 1,1 | 1,7 | 0,9 | 1,6 | 3,8 | 3,8 |
| 25 | 1,8 | 1,8 | 0,9 | 1,4 | 0,7 | 1,25 | 3,0 | 3,0 |
| 32 | 1,4 | 1,4 | 0,7 | 1,1 | 0,55 | 0,95 | 2,4 | 2,4 |
| 40 | 1,1 | 1,1 | 0,6 | 0,9 | 0,45 | 0,6 | 1,9 | 1,9 |
| 50 | 0,9 | 0,9 | 0,5 | 0,7 | 0,3 | 0,58 | 1,5 | 1,5 |
| 63 | 0,7 | 0,7 | 0,4 | 0,6 | 0,25 | 0,46 | 1,1 | 1,1 |

---

### Kap. 16 — Zusammenfassung und Normverweise

Nach DIN VDE 0100-200 und 0100-410 werden in der Niederspannung drei Netzformen (TN, TT, IT) und verschiedene aktive Leiter (L1, L2, L3, PEN, N; PE) unterschieden. Jede Schutzmaßnahme muss Basis- und Fehlerschutz umfassen. Die häufigste Schutzmaßnahme ist die automatische Abschaltung des Fehlerstroms. Endstromkreise sind durch RCD 30 mA zu schützen und die Abschaltzeiten einzuhalten. Der Schutzleiter muss sorgfältig verlegt, sein Querschnitt nach dem Kurzschlussstrom bemessen und seine Durchgängigkeit gemessen werden. Das TN-System ist bei jeder Planung elektrischer Anlagen zu bevorzugen.

**Normverweise Kap. 16:**
- DIN VDE 0100-410 (VDE 0100-410:2018-10) — Schutz gegen elektrischen Schlag
- DIN VDE 0100-540 (VDE 0100-540:2012-06) — Erdungsanlagen, Schutzleiter, Schutzpotentialausgleichsleiter
- DIN EN 50522 (VDE 50522:2011-11) — Starkstromanlagen mit Nennwechselspannungen über 1 kV

---

### Kap. 17 — Zentraler Erdungspunkt

Ströme über Schutzleiter und Schirmung von Daten-/Informationsleitungen können Störungen, Fehlfunktionen und Schäden verursachen. Die Art der Erdungsverhältnisse ist dafür ausschlaggebend.

- Im TN-S-Netz werden diese Störströme durch Trennung des Schutzleiters vom Neutralleiter vermieden.
- An einem einzigen Punkt der Anlage werden Anlagenerdung und Betriebserdung zusammengeführt.
- Der PEN-Leiter wird im gesamten Verlauf isoliert verlegt.
- PE und PEN dürfen niemals geschaltet werden.
- Im TT-System kommen Neutral- und Schutzleiter nicht zusammen; sie müssen stets getrennt bleiben.
- Für abgelegene Elektroanlagen, Häuser oder Landwirtschaft werden 990 V-Übertragungsleitungen eingesetzt; dafür kommen 990/400/230 V-Transformatoren mit amorphen Kernen zum Einsatz (Vorteil: ca. 1/3 der Eisenverluste gegenüber konventionellen Kernen).

---

### Kap. 17.1 — Arbeiten an elektrischen Anlagen: Fünf Sicherheitsregeln

An elektrischen Anlagen dürfen grundsätzlich nur Elektrofachkräfte tätig sein. Die Arbeit erfolgt ausschließlich im spannungsfreien Zustand. Nach Abschluss wird in umgekehrter Reihenfolge zur Spannungswiederherstellung vorgegangen. Schutzabstände zu spannungsführenden Teilen müssen eingehalten werden. Bei Elektrounfällen: Strom sofort unterbrechen, Verletzte in Ruhelage bringen, Erste Hilfe einleiten.

**Fünf Sicherheitsregeln (Tab. 17.1):**

| Schritt | Maßnahme | Erläuterung | Praxisbeispiel |
|---|---|---|---|
| 1 | Freischalten | Anlage vollständig von der Energieversorgung trennen | Schutzeinrichtungen allpolig abschalten, Sicherungen entfernen |
| 2 | Gegen Wiedereinschalten sichern | Unbefugtes Zuschalten verhindern | Verbotsschilder und Klebeband anbringen |
| 3 | Spannungsfreiheit feststellen | Spannungslosigkeit kontrolliert prüfen | Jeden Abgang mit Spannungsprüfer prüfen |
| 4 | Erden und kurzschließen | Anlagenteile zuerst erden, dann kurzschließen | Auf guten Erdkontakt achten |
| 5 | Benachbarte spannungsführende Teile abdecken/abschranken | Bis 1 kV: abdecken; über 1 kV: Absperrtafeln, Seile, Warntafeln | Körperschutz, Schutzkleidung, Schuhe, Schutzhelm, Gesichtsschutz |

**Normverweise Kap. 17:**
- DIN VDE 0100-100 (VDE 0100-100:2009-06)
- DIN VDE 0100-410 (VDE 0100-410:2018-10)
- DIN EN 50522 (VDE 50522:2011-11)
- DIN VDE 0100-540 (VDE 0100-540:2012-06)

---

### Kap. 18 — Mittelspannungsanlagen: Grundlagen

Mittelspannungsnetze werden aus dem Hochspannungsnetz (110 kV) gespeist.

**Spannungsdefinitionen nach Normen:**
- DIN IEC 38 / IEC 60038: MS = 1 bis 36 kV; in der Praxis werden 1 bis 60 kV als Mittelspannung bezeichnet
- Bis einschließlich 1 kV = Niederspannung; ab 1 kV = Hochspannung (IEC 60038)
- Typische Bemessungsspannungen MS-Schaltanlagen: 1 bis 52 kV; üblich 10 oder 20 kV

Energie wird über Netzstationen in Niederspannungsnetze verteilt. MS-Schaltanlagen kommen in Industrie, Hochhäusern und regionalen Verteilungsnetzen vor. Stationen können in Fertigbetonzellen, Containern oder Spezialräumen untergebracht sein.

Netzstationen enthalten häufig zwei Netztransformatoren (für hohe Verfügbarkeit) sowie die Niederspannungshauptverteilung (NSHV), welche Verbraucher in Strahlennetztopologie speist. Bemessungsleistung der Transformatoren: 100 bis 2500 kVA.

Übertragung erfolgt üblicherweise über Erdkabel in Ringstruktur mit Trennstellen, sodass einzelne Leitungsabschnitte bei Störung freigeschaltet werden können.

**Schaltanlagen-Bauformen:**
- Metallkapselung oder Isolierstoffkapselung
- Felder durch Schottungen in Bereiche unterteilt
- Aufstellung: Einspeise-, Schleifen-, Mess- und Abgangsfelder

**Netzbetriebs-Pflichten:**
- Netzbetreiber (NB): nach Energiewirtschaftsgesetz für sicheren, zuverlässigen, umweltverträglichen, wirtschaftlichen und preisgünstigen Betrieb verantwortlich
- Betreiber und Elektroplaner: verpflichtet, Anlagen nach DIN-VDE-Vorschriften und anerkannten Regeln der Technik zu planen, errichten und betreiben

**Charakteristiken der MS-Anlagen:**
- Verluste
- Wartungsanforderungen
- Investitionen
- Maximale Einspeiseleistung
- Anlagensicherheit
- Betriebsprobleme
- Umgebungseinflüsse

---

### Kap. 18.1 — Betriebsverfügbarkeit

Norm IEC 62271-200 (VDE 0671-200) definiert Kategorien für die Betriebsverfügbarkeit (LSC: loss of service continuity) von Schaltanlagen-Funktionseinheiten.

**Kategorien der Betriebsverfügbarkeit (Tab. 18.1):**

| Kategorie | Auswirkung beim Öffnen eines zugänglichen Schottraums | Konstruktive Ausführung |
|---|---|---|
| LSC 1 | Sammelschiene und gesamte Schaltanlage müssen freigeschaltet werden | Keine Schottwände innerhalb des Feldes, keine Feldtrennwände zu Nachbarfeldern |
| LSC 2A | Nur das einspeisende Kabel muss freigeschaltet werden; Sammelschiene und Nachbarfelder bleiben in Betrieb | Feldtrennwände und Trennstrecke mit Schottung zur Sammelschiene |
| LSC 2B | Einspeisekabel, Sammelschiene und Nachbarfelder können alle in Betrieb bleiben | Feldtrennwände und Trennstrecken mit Schottung zur Sammelschiene sowie zum Kabel |

---

### Kap. 18.1.1 — Arten von Schottungen

Nach IEC 62271-200 gibt es zwei Schottungsklassen. Die Schottungsklasse allein garantiert nicht den Personenschutz bei Störlichtbögen in benachbarten Schotträumen.

- **Klasse PM (Partitions metallic):** Offene Schotträume sind von geerdeten metallischen Zwischenwänden und/oder Shuttern umgeben. Im offenen Schottraum darf kein elektrisches Feld vorhanden sein. Verhindert Einflüsse auf spannungsführende Teile (Ausnahme: Shutter-Stellungsänderung).
- **Klasse PI (Partitions non-metallic, i = insulating material):** Metallgekapselte Schaltanlage mit einer oder mehr nicht-metallischen Zwischenwänden oder Shuttern zwischen zugänglichen Schotträumen und spannungsführenden Teilen.

---

### Kap. 18.1.2 — Störlichtbogenqualifikation

Bei Auswahl metallgekapselter Schaltanlagen nach IEC 62271-200 ist das Risiko von Störlichtbögen (IAC: internal arc classified) zu berücksichtigen. Risikobewertung nach ISO/IEC-Leitfaden 51 aus Auftrittswahrscheinlichkeit und Schadensausmaß:
- Vernachlässigbares Risiko: IAC-Qualifikation nicht erforderlich
- Erhebliches Risiko: Nur Schaltanlagen mit IAC verwenden

**Zugänglichkeitsgrade:**
- **Grad A:** nur befugtes Personal
- **Grad B:** uneingeschränkte Zugänglichkeit einschließlich Öffentlichkeit
- **Grad C:** eingeschränkt, außer Reichweite und oberhalb öffentlich zugänglicher Bereiche (für mastmontierte Schaltanlagen); der Mindestarbeitsabstand ist vom Hersteller anzugeben; Mindestinstallationshöhe = Mindestarbeitsabstand + 2 m

**Klassifizierte Seiten (für Grad A und B):**
- F = Vorderseite, L = Seitenfläche, R = Rückseite
- Vorderseite muss vom Hersteller eindeutig angegeben werden
- Klassifizierte Seiten gelten nicht für Anlagen mit Zugänglichkeitsart C

---

### Kap. 18.2 — Projektierung: Definitionen und Schottraumtypen

- **Kapselung:** Teil einer metallgekapselten Schaltanlage, der festgelegten Schutzgrad gegen äußere Einwirkungen, gegen Annähern/Berühren spannungsführender Teile und gegen bewegliche Teile bietet
- **Hochspannungsschottraum:** Schottraum mit spannungsführenden Teilen, bis auf Öffnungen für elektrische Verbindungen, Steuerung und Belüftung vollständig gekapselt

**Vier Arten von Hochspannungsschotträumen:**
1. Verriegelungsgesteuert zugänglicher Schottraum
2. Verfahrensabhängig zugänglicher Schottraum
3. Werkzeugabhängig zugänglicher Schottraum
4. Nicht zugänglicher Schottraum

---

### Kap. 18.2 — Gasisolierte Verteilungsnetze (GIS)

GIS-Schaltanlagen bestehen aus auf Erdpotential liegenden, gasdichten, gekapselten Gasräumen; alle Felder dicht und voneinander getrennt. Isoliergas: Schwefelhexafluorid (SF6).

**SF6-Eigenschaften:** ungiftig, farb-, geruch- und geschmacklos, hohe Durchschlagfestigkeit, gutes Isoliervermögen, bei Raumtemperatur sehr beständig, 5-mal schwerer als Luft (sammelt sich am Boden).

**Vorteile GIS:**
1. Kleine, kompakte Abmessungen → geringe Gebäude-/Baukosten
2. Klimaunabhängig → keine Kosten für Reinigung, Heizung, Reparatur
3. Unempfindlich bei aggressiven Umgebungsbedingungen (Salz, Wasser)
4. Wartungsfrei → keine Kosten für Wartung und Stillstandzeiten
5. Höchste Zuverlässigkeit
6. Höchster Personenschutz

**Komponenten (Ringkabel- und Transformatorabzweig, Abb. 18.3):**
1. Bedienfeld; 2. Sammelschiene; 3. Dreistellungslasttrennschalter; 4. Druckentlastungseinrichtung; 5. Trennblech Kabelanschlussraum/Druckentlastungsraum; 6. Kabelkanal (abnehmbar); 7. Anlagenbehälter (gasgefüllt); 8. Antrieb Schaltgerät; 9. Durchführung für Kabelstecker mit Schraubkontakt; 10. Kabelraumabdeckung; 11. Erdsammelschiene mit Erdungsanschluss; 12. Schottung; 13. HH-Sicherungsanbau; 14. Durchführung für Kabelstecker mit Steckkontakt; 15. Vakuumleistungsschalter; 16. Antriebe Leistungsschalter und Dreistellungstrennschalter

**Leistungsschalterabzweig und Messfeld (Abb. 18.4):**
1. Buchsen für Spannungsprüfsystem; 2. Sammelschienenanschluss; 3. Sammelschienenbehälter (gasgefüllt); 4. Druckentlastungseinrichtung; 5. Stromwandler; 6. Spannungswandler; 7. Kabelkanal; 8. Nische für kundenseitige NS-Ausrüstung; 9. Durchführungen Wandlerschienen; 10. Abdeckung Wandlerraum; 11. Kabelanschluss; 12. Erdsammelschiene mit Erdungsanschluss

---

### Kap. 18.2 — Luftisolierte Verteilungsnetze (AIS)

AIS benötigen wegen des schlechten Isoliervermögens von Luft mehr Platz.

**Vorteile AIS:**
1. Niedrigerer Preis für die Schaltanlage
2. Reduktion bei Aufstellung über 1000 m Höhe
3. Keine Klimaunabhängigkeit (Nachteil)
4. Keine Unabhängigkeit von Umwelteinflüssen (Nachteil)
5. Wandler und Schalter austauschbar
6. Regelmäßige Wartung notwendig → Kosten, Risiko, Personenschutzaufwand

**Aufbau (Bereiche):**
- A: Schaltgeräteraum; B: Sammelschienenraum; C: Anschlussraum; D: Leistungsschaltereinschub; E: Niederspannungsschrank

**Bestandteile (Komponenten 1–23 der AIS-Anlage, Abb. 18.5):**
1. Tür zum NS-Schrank; 2. Schutzgerät; 3. Kapazitives Spannungsprüfsystem (Option); 4. Hochspannungstür; 5. Abschließvorrichtung; 6. Blindschaltbild; 7. EIN/AUS-Betätigungsöffnungen und Federspann-Öffnung; 8. Sichtfenster (Trenn-/Betriebsstellung, EIN/AUS-Anzeige, Federanzeige, Schaltspielzähler); 9. Betätigungsknopf Hochspannungstür; 10. Betätigungsöffnung Verfahren Schaltgerät; 11. Mechanischer Schaltstellungsanzeiger und Betätigungsöffnung einschaltfester Erdungsschalter; 12. Druckentlastungskanal; 13. Sammelschienen; 14. Durchführungsstützer; 15. Durchführungsstromwandler; 16. Spannungswandler; 17. Kabelanschluss (4 Kabel je Leiter); 18. Einschaltfester Erdungsschalter; 19. Niederspannungsverbindung (steckbar); 20. Antriebs- und Verriegelungseinheit Leistungsschalter; 21. Vakuumschaltröhren; 22. Kontaktsystem; 23. Antriebs- und Verriegelungseinheit (Verfahren des Schalters und Erden)

---

### Kap. 18.3 — Mittelspannungsschaltgeräte

**Leistungsschalter:**
- Bemessungsausschaltvermögen für Ein-/Ausschalten bei Betriebs- und Kurzschlussbedingungen
- Niedrige zulässige Schaltspielzahlen, lange Schalt- und Lichtbogenzeiten
- Kein mechanischer Verriegelungsabgriff

**SF6-Schalter:**
- Isolier- und Löschmittel: SF6 (farblos, geruchlos, 5-mal schwerer als Luft)
- SF6 bindet Elektronen → schwere negative Ionen → erhöhte Durchschlagfestigkeit
- Gute Wärmeleitfähigkeit kühlt und entionisiert den Lichtbogen im Bereich des Stromnulldurchgangs

**Vakuumschalter:**
- Sehr große Schaltspielzahlen
- Vorteile: rasche Wiederverfestigung, hohe Druckschlagfestigkeit, geringe Bogenspannung, niedriger Materialverschleiß, Wartungsfreiheit
- Aufbau: drei Vakuumschaltröhren, Schaltröhrenträger pro Pol, mechanischer Antrieb
- Weitere Vorteile: großes Bemessungsausschaltvermögen, große dielektrische Festigkeit, kleiner Abreißstrom, geringer Schaltstückabbrand, kleiner Kontaktwiderstand

**Vakuumschütze:**
- Elektromagnetischer Antrieb; für MS-Anlagen geeignet
- Begrenztes Kurzschlusseinschalt- und Ausschaltvermögen
- Schaltaufgaben: Drehstrommotoren (AC-3 und AC-4), Transformatoren, Drosselspulen, ohmsche Verbraucher, Kondensatoren
- Abreißströme der Schütze: ≤ 5 A
- Schaltüberspannungen möglich, wenn HS-Motoren mit Anlaufströmen ≥ 600 A während des Hochlaufens abgeschaltet werden → Überspannungsbegrenzer einsetzen

**Ölarme Schalter:**
- Schaltflüssigkeit als Löschmittel
- Beim Schalten unter Öl: Lichtbogenhitze verdampft Öl → Dampf/Gasblase; große Ölmengen werden eingespritzt → Kühlung → Entionisierung → Lichtbogen erlischt

**Lastschalter:**
- Bemessungsausschaltvermögen für Ein-/Ausschalten im ungestörten Betrieb

**Erdungsschalter:**
- Für annähernd stromloses Schalten, Erden und Kurzschließen ausgeschalteter Anlagenteile

**Lasttrennschalter:**
- Stellen beim Ausschalten eine Trennstrecke dar
- Können maximal auftretenden Betriebsstrom ausschalten
- Geeignet für Einschalten auf Kurzschluss
- Teilweise undefinierte Kurzschlussfestigkeiten; Hilfsschalter ohne Zwangsteuerung mit ungenügender Meldegenauigkeit

**HH-Sicherungen (Hochspannungs-Hochleistungssicherungen):**
- Abgespannter Schmelzleiter mit geringem Querschnitt schmilzt beim Fehlerstromdurchfluss
- Übernehmen Kurzschlussschutz

**Is-Begrenzer:**
- Kombination: extrem schneller Schalter (hoher Bemessungsstrom, geringes Ausschaltvermögen) + parallel geschaltete Löscheinrichtung (hohes Ausschaltvermögen)
- Auftrennung des Stromkreises ca. 0,1 ms nach Auslösung; Strom kommutiert auf Löscheinrichtung, wird begrenzt und gelöscht

**Strom- und Spannungswandler:**
- Wandeln primäre elektrische Größen in proportionale, phasengetreue, für Geräte und Personal ungefährliche Größen um
- Stromwandler zwischen Leistungsschalter und Abgang anordnen

**Überspannungsableiter:**
- Schützen Isolation vor unzulässiger Beanspruchung durch transiente Überspannungen

**Lastschalter-Sicherungs-Kombination:**
- Lastschalter: schaltet Betriebsstrom
- Sicherung: zuständig für Kurzschlussschutz
- Zusammenarbeit im Überstrombereich geregelt durch IEC 420 (DIN VDE 0670 Teil 303)
- Bemessungsausschaltvermögen beider Geräte aufeinander abstimmen

---

### Kap. 18.4 — Aufstellung von Schaltanlagen

Alle Betriebsmittel in abgeschlossenen Betriebsstätten. Räume dienen ausschließlich dem elektrischen Betrieb und werden unter Verschluss gehalten. Zutritt nur für Elektrofachkräfte und elektrotechnisch unterwiesene Personen.

**Mindestanforderungen (Festlegungen):**
- Gänge: mindestens 1000 mm Breite
- Schaltfeldtüren müssen in Fluchtrichtung aufschlagen
- Ausgänge so anordnen, dass Rettungsweg innerhalb des Raums ≤ 40 m
- Mindestdurchgangshöhe unter Abdeckungen oder Umhüllungen: 2000 mm

**Schaltanlagen-Bauformen nach Norm:**
- Nach Mindestabständen gemäß DIN VDE 0101 (fabrikfertig)
- Mit kleineren Luftabständen nach DIN VDE 0670 Teile 6 und 7 (fabrikfertig und typgeprüft)

---

### Kap. 18.5 — Auswahlgrößen für MS-Anlagen

**1. Feste Vorgaben:**
- Normen, Bestimmungen, Vorschriften
- Bemessungsspannung
- Bemessungsfrequenz
- Sternpunktbehandlung
- Stoßkurzschlussstrom
- Umgebungsbedingungen

**2. Bedingte Auswahlgrößen:**
- Isolationspegel
- Kurzschlussdauer
- Netzaufbau

**3. Auswahl der Betriebsmittel:**
- Überstromschutzeinrichtungen
- Bauform der Schaltanlagen und des Sammelschienensystems
- Schutzmaßnahmen
- Bauformen der Schaltschränke

---

### Kap. 18.6 — Isolierung

In MS-Schaltanlagen kommen Luftisolierung, Feststoffisolierung und SF6-Gasisolierung zum Einsatz. Vorteile der SF6-Gasisolierung: kleine Abmessungen, höhere Betriebssicherheit, sicherer Berührungsschutz, lange Lebensdauer, geringer Wartungsaufwand.

---

### Kap. 18.7 — Raumplanung

Art der Raumplanung abhängig von: Einfach- oder Doppelsammelschienensystem, Anzahl der Felder, Festeinbau oder Einschubanlagen.

Aufstellungsarten: einreihig, Rücken-Rücken, Gegenüberaufstellung.

Für einzelne Stromkreise der Transformatorstation (Steckdosen, Beleuchtung, Ventilatoren, Heizgeräte): eigene Unterverteilung im NS-Raum vorsehen. Mess-, Schutz- und Stromkreisleitungen getrennt verlegen.

Belüftung: natürlich und unmittelbar. Für Be- und Entlüftung der Transformatoren hinter Abluftgittern Lüfter vorsehen, die über Temperaturschalter gesteuert werden.

---

### Kap. 18.8 — Transformatoren

Transformatoren müssen nach DIN 42524 gebaut sein, der Isolierstoffklasse E entsprechen und DIN VDE 0532 erfüllen.

**Bemessungsübersetzungen:** 20/0,4 kV, 10/0,4 kV, 5/0,4 kV
**Bemessungskurzschlussspannung:** 6 % oder 4 %

**Öltransformatoren:** zusätzlich mit Zweischwimmerbuchholzschutz und Kontaktthermometer ausrüsten → bei Ansprechen löst der MS-Schalter aus.

**Trockentransformatoren:** zwei Kaltleitersysteme zur Temperaturüberwachung (Warnung + Abschaltung) mit Auslösegeräten → bei Ansprechen Auslösung des MS-Schalters über Arbeitsstromauslöser.

Transformator-NS-Leistungsschalter mit Transformator-MS-Schalter verriegeln. NS-Leistungsschalter mit Arbeitsstromauslösung versehen (Rückspannungsschutz: trennt Transformator vom Netz). Leistungsschalter mit Auslöselampe ausstatten. Alle NH-Sicherungslasttrennschalter mit Einbaumöglichkeit für je drei Stromwandler installieren.

---

### Kap. 18.9 — Erdung von MS-Anlagen

MS/HS-Schutzerde und NS-Betriebserde nach EN 50522, EN DIN 50179 und Vorgaben des Netzbetreibers.

- **Schutzerde:** Erdung nicht betriebsstromführender Anlagenteile zum Schutz vor Berührungs- und Schrittspannung
- **Betriebserde:** Erdung des Sternpunktleiters für den NS-Netzbetrieb

**Anforderungen an Erdungswiderstand:** ≤ 2 Ω

**Potentialerdringleitung:** feuerverzinkter Bandstahl, Querschnitt 30 × 3,5 mm, ringsumlaufend, mit Stationssammelerde verbunden.

**Empfehlungen für die Erdungsausführung:**
- Innen- und Außenerdungsanlage für gemeinsame Schutz- und Betriebserdung
- Außenerdungsanlage kann aus Tiefenerdern bestehen
- Innenerdungsanlage: Sammelleitung aus Flachkupfer, z. B. 30 × 5 mm, unter der Schaltanlage im Kabelkanal oder Doppelboden
- Verbindung zum zentralen Erdungspunkt: Kupferkabel, z. B. 150 mm²
- Schaltanlage an Anfang und Ende mit dem Querschnitt der Sammelleitung anschließen
- Gerüste jeder Zelle und der eingebauten Geräte jeweils einzeln an Sammelleitung anschließen
- NS-Gerüste sämtlich an die Sammelleitung anschließen
- PE-Schiene der NS-Schaltanlage mit Kupferkabel (z. B. 150 mm²) an zentralen Erdungspunkt
- N-Leiterschiene isoliert verlegen und durch Trennlasche mit Erdungspunkt verbinden
- Transformatorsternpunkt über Trennlasche an der PE-Schiene erden
- Erdungssammelleitung für Transformatorkammern, Hilfskonstruktionen, Transformatorkessel und Kondensatoren: Flachkupfer 30 × 5 mm
- Fahrschienen, Halteschienen, Schellen, sonstige Metallteile: nach DIN VDE 0100 und EN 50522
- Alle zum Erdungssystem gehörenden Schienen grün-gelb kennzeichnen

---

### Kap. 18.10 — Innenraumschaltfelder

Einteilung nach DIN VDE 0101:
- Offene Bauweise (Einfach- oder Doppelsammelschiene, nur teilweiser Berührungsschutz)
- Gekapselte Ausführung (vollständiger Schutz, Einfach- oder Doppelsammelschiene)
- Fest eingebaute Betriebsmittel

---

### Kap. 18.11 — Grundlagen der Netzplanung

Netzplanung berücksichtigt Verteilungsnetz und Verbraucheranforderungen. Aufbau nach dem (n−1)-Ausfallprinzip: Bei Ausfall eines Betriebsmittels darf weder das Netz überlastet noch die Versorgung anderer Anlagenteile beeinträchtigt werden.

Netzschutz: unterbrechungsfreie Versorgung gewährleisten; nur kurzschlussbetroffene Teile abtrennen. MS-Netz immer zusammen mit NS-Netz und Verbrauchern planen. Spannung möglichst konstant halten.

**Merkmale eines guten Netzes:**
- Gute Spannungshaltung
- Hohe Zuverlässigkeit der Versorgung
- Hohe Verfügbarkeit
- Sicherheit und geringe Störhäufigkeit
- Kostengünstiger Verbrauch

---

### Kap. 18.12 — Kriterien für die Anlagenauslegung

- **Spannungswahl:** 10- und 20-kV-Ebene in der öffentlichen Versorgung; bei SF6-Anlagen 110 kV → Zwischenspannungen entfallen; bei Industriemotoren: besondere Beachtung der Spannungsauswahl
- **Sternpunktbehandlung:** Verschiedene Arten im MS-Netz möglich; Freileitungsnetze: Erdschlusskompensation über Petersen-Spule; Kabelnetze: Sternpunkterdung mit Fehlererkennung und Fernsteuerung vorteilhaft
- **Kurzschlussleistung:**
  - UnQ = 10 kV → S''kQ = 250 bis 350 MVA
  - UnQ = 20 kV → S''kQ = 500 MVA
  - Berechnung: S''kQ = √3 × UnQ × I''k = c × U²nQ / ZkQ — Formel (18.1)
  - Symbole: S''kQ — Kurzschlussleistung; UnQ — Bemessungsspannung; ZkQ — wirksame Ersatzimpedanz; c — Spannungsfaktor nach DIN VDE 0102
- **Lastvorhersage:** Gesamtlast, zeitliche Lastentwicklung, Veränderung der Verbrauchergruppen
- **Netzgestaltung:** einfach, übersichtlich, bei Störungen beherrschbar; Schutz von Bedienungspersonal vor Störlichtbögen. Anforderung DIN VDE 0101 durch eine der Maßnahmen erfüllen:
  - Lasttrennschalter statt Trennschaltern
  - Bedienung aus sicherer Entfernung (z. B. Kraftantriebe)
  - Geeignete Schutzeinrichtungen (Trennwände, Lichtbogenfenster, druckfeste Türen)
  - Schaltfehlerschutz für Trenn- und Erdungsschalter
- **Technisch-wirtschaftliche Klärungen:** Kurzschlussfestigkeit der Betriebsmittel; Bemessungsausschaltvermögen der Schalter; Bemessungsstrom der Sammelschienen und Abzweige; Verfügbarkeit; Netzleittechnik-Anpassung

---

### Kap. 18.13–18.14 — Bauformen und Lasttrennschalteranlagen

**Bauformen nach DIN VDE 0670 Teile 6 und 7 sowie DIN VDE 0101:**
- Kombination von Leistungs- und Lasttrennschalteranlagen möglich

**Lasttrennschalteranlagen:**
- Typgeprüfte, fabrikfertige, metallgekapselte Innenraumschaltanlagen mit SF6-Gasisolierung
- Einsatz in Betriebsstätten und geschlossenen elektrischen Betriebsstätten nach DIN VDE 0101

**Spezifische Merkmale:**
- Kleinere Kurzschlussströme und Betriebsströme
- Sicheres Prüfen der Spannungsfreiheit an geschlossener Schaltfront
- Logische Verriegelungen
- Störlichtbogengeprüfter Edelstahlbehälter und Kabelanschlussraum
- Erhöhte Betriebs- und Wartungsfreiheit
- Umweltunabhängige Kabelanschlüsse (korrosions- und klimaunabhängig); einfache SF6-Entsorgung

**Bauweisen:**
- **Feldbauweise:** besonders in Industrienetzen; Abzweige als Lasttrennschalter-Sicherungskombination oder Leistungsschalter
- **Blockbauweise:** Einspeisung, Abzweige und Sammelschienen in gemeinsamer Kapselung; üblicherweise nur Lasttrennschalter; Einsatz in Netzstationen der Energieversorgung

---

### Kap. 18.15–18.16 — Leistungsschalteranlagen und Festeinbauanlagen

**Leistungsschalteranlagen:**
- Innenraumschaltanlagen nach DIN VDE 0670 Teil 6 und IEC 298; bis 36 kV, luftisoliert, teilgeschottet und metallgeschottet
- Merkmale: Sammelschienen-Schottung durch Schutzplatte möglich; Schutzplatte, Einschub und Tür in Gesamtverriegelung; vollständige Schottung Feld zu Feld; Schutzgrad Schutzplatte: IP 4X und IP 3XD

**Leistungsschalter-Festeinbauanlagen:**
- Merkmale: dreipolige Primärkapselung; Isoliergas SF6; Vakuumleistungsschalter; Dreistellungsschalter als Sammelschienentrennschalter und Abzweigerdungsschalter; hoher Lichtbogenschutz; Primärkapselung berührungssicher und hermetisch geschlossen; Schalterantrieb außerhalb des Anlagenbehälters
- Dreipolig metallgekapselte, metallgeschottete SF6-isolierte Schaltanlagen für Einfachsammelschienen
- Aufstellung in Innenräumen mit Längskupplungsfeld und Kabelanschluss
- Bemessungsspannung: bis 36 kV
- Bemessungskurzschlussausschaltstrom: 25 bis 31,5 kA
- Bemessungsbetriebsströme Sammelschienen und Abzweige: bis 2500 A

**Varianten:**
1. Luftisolierte Leistungsschalteranlagen
2. Gasisolierte Leistungsschalteranlagen: Schalten im Vakuum, Isolieren mit SF6; Erden mit Leistungsschalter; kein Kabeltrennschalter erforderlich; berührungssichere Steckanschlüsse; kompakte Bauweise; Dreistellungsschalter zum Trennen und Erden

---

### Kap. 18.17 — Schaltanlagenkonstruktionen

**Festeinbautechnik:**
- Am häufigsten ausgeführte Technik
- Für hohe Leistungen in Umspannwerken, Verteiler-/Netzstationen, Industrieanlagen
- Preisgünstig, einfach im Auf- und Ausbau
- Bestandteile: 1 Sammelschiene, 2 Trenner, 3 Leistungsschalter, 4 Sicherung, 5 Stromwandler, 6 Spannungswandler, 7 Erdung, 8 Einspeisung, 9 Abgang

**Schaltwagentechnik:**
- Einsatz in Umspannwerken, Eigenerzeugungsanlagen von Kraftwerken, Industrieanlagen zur Energieerzeugung
- Ausschließlich mit Leistungsschaltern ausgerüstet
- Bestandteile: 1 Sammelschiene, 2 Trenner, 3 Leistungsschalter, 4 Stromwandler, 5 Erdung, 6 Sicherung, 7 Spannungswandler, 8 Abgang

---

### Kap. 18.18 — Isolationskoordination

Koordination zwischen betrieblichen Beanspruchungen, Isolationsvermögen der Betriebsmittel und Anlagen notwendig. Vorgehen nach DIN VDE 0111 Teil 1 und 3.

Maßgebend: der für ein Betriebsmittel gewählte Isolationspegel. Spannungsbeanspruchung und Eigenschaften der Überspannungsschutzeinrichtungen berücksichtigen.

**Maßnahmen der Isolationskoordination:**
- Umgebungsbedingungen berücksichtigen
- Betriebsmittel nach Spannungsklasse wählen (Beispiel: Un = 20 kV → höchste Spannung für Betriebsmittel Um = 24 kV)
- Dielektrische und atmosphärische Beanspruchungen einrechnen
- Überspannungsschutzeinrichtungen vorsehen

**Ursachen zeitweiliger Spannungserhöhungen:**
- Erdberührungsfehler → betriebsfrequente Spannungserhöhungen (abhängig von Sternpunktbehandlung)
- Lastabwurf → Spannungserhöhungen bis 10 % (abhängig von abgegebener Blindleistung, Streureaktanz des Transformators, Spannungsregelung)
- Resonanz und Ferroresonanz → bei Zusammenschaltung kapazitiver und induktiver Betriebsmittel unter Resonanzbedingungen

---

### Kap. 18.19 — Schaltüberspannungen

Jede Zustandsänderung im Netz erzeugt gedämpfte Ausgleichsvorgänge → kurzzeitige Überspannungen.

**Ursachen:**
- Schalten induktiver und kapazitiver Ströme → elektromagnetische Ausgleichsvorgänge mit steilen Überspannungen
- Ein-, Aus- und Wiedereinschalten von Leitungen → Herabsetzen von Überspannungen
- Erdberührungsfehler → Schaltüberspannungen proportional zum Erdfehlerfaktor ι
- Lastabwurf → besonders durch Schalthandlungen ausgelöst; Höhe abhängig von Schaltvorgang, Schaltzustand des Netzes und Betriebsmitteleigenschaften

---

### Kap. 18.20 — Begrenzung von Überspannungen

**Maßnahmen:**
- **Überspannungsableiter (MO-Ableiter):** begrenzen Überspannung über spannungsabhängige Widerstände durch niederohmige Verbindung zur Erde; Schutzpegel durch Betriebsspannung Uc und Bemessungsspannung Ur festgelegt
- **Schutzfunkenstrecken:** größere Ansprechverzögerung als Ableiter; in höheren Spannungsebenen geringere Schutzwirkung
- **Schutzkondensatoren:** auf Sekundärseite von Transformatoren mit großem Übersetzungsverhältnis, um unzulässige Über- und Verlagerungsspannungen zu vermeiden

---

### Kap. 18.21 — Erdfehlerfaktor

Der Erdfehlerfaktor ι kennzeichnet Spannungsverhältnisse bei der Wahl von Isolationspegeln und Löschspannungen von Überspannungsableitern. Er hängt vom Verhältnis Z1/Z0 ab.

**Formel:**
- ι = ULE / (Ub / √3) — Formel (18.2)
- Maximale Leiter-Erd-Spannung: ULEmax = ι × Ubmax / √3 ≈ ι × Um / √3 — Formel (18.3)

**Symbole:**
- ι — Erdfehlerfaktor
- ULE — betriebsfrequente Spannung gegen Erde
- Ubmax — maximale Betriebsspannung
- Um — höchste Spannung für Betriebsmittel
- Ub — Betriebsspannung

---

### Kap. 18.22 — Ableiterauswahl

Überspannungsableiter werden üblicherweise zwischen Leiter und Erde eingebaut. Bei Erdberührungsfehlern entstehen zeitweilige Spannungserhöhungen an den Ableitern.

**Auswahlkriterien für Ableiter:**
- Löschspannung (bei SiC-Ableitern)
- Bemessungsspannung und Dauerspannung (bei MO-Ableitern)
- Bemessungsanleitstoßstrom
- Langwellenableitstrom bzw. Energieaufnahmevermögen
- Kurzschlussstromfestigkeit
- Aufstellhöhe

**Netzart 1 — Netze mit direkter oder niederohmiger Erdung:**
- Maximale Leiter-Erd-Spannung: UYm = Um / √3 — Formel (18.4)
- Spannungserhöhung durch Erdfehlerfaktor: ULE = ι × UY — Formel (18.5)
- Erdfehlerfaktor (ohne Wirkwiderstände für HS-Netze): ι = (√3 / 2) × √(3 / ((X0/X1)² + X0/X1)² + 1) — Formel (18.6)
- SiC-Ableiter: U1 ≥ ι × Um / √3 — Formel (18.7)
- MO-Ableiter Bemessungsspannung: Ur ≥ ι × Um / √3 — Formel (18.8)
- MO-Ableiter Dauerspannung: Uc ≥ 1,05 × Um / √3 — Formel (18.9)

**Netzart 2 — Netze mit isoliertem Sternpunkt oder Erdschlusskompensation:**
- Maximale Leiter-Erd-Spannung gesunder Leiter: ULE = Um = √3 × UYm — Formel (18.10)
- Löschspannung SiC-Ableiter: Ul ≥ Um — Formel (18.11)
- Dauerspannung MO-Ableiter: Uc ≥ Um — Formel (18.12)

---

### Kap. 18.23 — Dimensionierung von MS-Anlagen

#### 18.23.1 Wirtschaftlichkeitsbetrachtungen — Transformatorverluste

Transformatorverluste: Leerlaufverluste (Eisen) + Kurzschlussverluste (Kupfer)

**Leistung bei maximalem Wirkungsgrad:**
- Sηmax = SrT × √(PFer / (PCur × τ)) — Formel (18.13)
- Symbole: SrT — Bemessungsleistung des Transformators; PFer — Leerlaufverluste des Eisens; PCur — Kurzschlussverluste des Kupfers; τ — Verlustfaktor

**Verlustfaktor τ** (abhängig von Belastungsgrad m, m = 0,7 typische NB-Last):
- τ = 0,17m + 0,83m² (nach VDEW) — Formel (18.14)

**Lüfterleistung:**
- PL = a × √3 × Ur × IL — Formel (18.15)
- Symbole: a — Anzahl der Lüfter; Ur — Bemessungsspannung; IL — Lüfterstrom

**Jahresverlustarbeit:**
- WG = WFe + WCu = PFe × TB + PCu × (Smax / SrT)² × TB × τ — Formel (18.16)
- Symbole: WG — Gesamtjahresverlustarbeit; WFe — Jahresleerlaufverluste; WCu — Jahreskurzschlussverluste; TB — Jahresbetriebszeit

**Wirtschaftlichkeitsberechnung — Barwertmethode:**

Barwert gibt an, welcher Betrag zum Bezugszeitpunkt angelegt werden muss, um alle Kosten im Betrachtungszeitraum zu decken.

- Abzinsungsfaktor: q = 1 + z / (100 % − θ / 100 %) — Formel (18.17)
- Barwertfaktor: ba = q⁻ᵃ — Formel (18.18)
- Barwert der Anlage: KA = ba × Ka — Formel (18.19)
- Verlustkosten-Barwertfaktor: bo = (q^ta − 1) / (q^ta × (q − 1)) — Formel (18.20)
- Barwert der Leerlaufkosten: K0 = n × TB × (PFer + TLü/TB × PLü) → K0 = bo × Ko — Formeln (18.21), (18.22)
- Steigerungsfaktor: s = (1 + g)² — Formel (18.23)
- Barwertfaktor steigende Verluste: bk = ((s/q)^(t/a) − 1) / (s − q) — Formel (18.24)
- Kurzschlussverlustkosten: Kk = TB × k × τ × PCur/n × (Smax(1) / SrT)² — Formel (18.25)
- Barwert steigende Kosten: KK = bk × Kk — Formel (18.26)
- Gesamtbarwert: K = KA + K0 + KK — Formel (18.27)

**Symbole der Barwertmethode:**
- ba — Barwertfaktor der Anlage; bk — Barwertfaktor jährlich steigender Verluste; bo — Barwertfaktor jährlich gleicher Verluste; g — jährlicher Steigerungsfaktor; K — Gesamtbarwert; Ka — Anlagekosten zum Zeitpunkt t=0; KK — Barwert der Kurzschlussverluste; Kk — Kurzschlussverlustkosten; k — Arbeitsverlustkosten; n — Anzahl der Transformatoren; PFe — Leerlaufverluste; Ko — Leerlaufverlustkosten; PCu — Kurzschlussverluste; PLü — Lüfterverluste; q — Abzinsungsfaktor; SrT — Bemessungsleistung; Smax(1) — Höchstleistung im ersten Jahr; s — Steigerungsfaktor; TB — jährliche Einschaltdauer; TLü — jährliche Einschaltdauer der Lüfter; t — Zeitraum; z — Zinssatz; θ — Teuerungsrate; τ — Verlustfaktor

---

#### 18.23.2 Bemessung des Einspeisekabels

Leiterquerschnitt der Einspeisung nach vier Kriteriengruppen festlegen:

**1. Betriebliche Anforderungen:** Leistung; Betriebsart; Leistungsfaktor

**2. Netzanforderungen:** Fehlerart; Abschaltzeit; Erdungsbedingungen; Betriebsspannung

**3. Umgebungsanforderungen:** Häufung; Temperatur; spezifischer Erdbodenwärmewiderstand

**4. Kabeleigenschaften:** Zulässige Kurzschlusstemperatur; Impedanzen des Kabels; Verluste des Kabels

Diese vier Kriteriengruppen bestimmen außerdem: Strombelastbarkeit; Kurzschlussfestigkeit; zulässigen Spannungsfall; Wirtschaftlichkeit.

---

#### 18.23.3 Wirtschaftlicher Kabelquerschnitt

Wirtschaftlicher Querschnitt bedeutet Optimierung von Anschaffungs-, Verlege- und Energieverlustkosten. Methoden gemäß DIN VDE 0298 Teil 100.

**Jahreskosten einer Kabelanlage:**
- K = Kd + Kv — Formel (18.28)
- Kd — Kapitaldienst (feste Kosten); Kv — Jahresverlustkosten

**Kapitaldienst:**
- Kd = Ka × (T + TR) / 100 — Formel (18.29)
- Ka — Anschaffungskosten (Kabel, Garnituren, Montage, Erdarbeiten)
- T — Tilgungssatz; TR — Zuschlag zum Tilgungssatz (Wartung und Reparatur)

**Tilgungssatz:**
- T = 100 × q^t × (q − 1) / (q^t − 1) — Formel (18.30)
- q = 1 + p/100 — Formel (18.31)

**Jahresverlustkosten:**
- Kv = γ × l × Ns × NK × [ka × (Tv × Pi + TB × Pd) + k1 × Pi] — Formel (18.32)
- Spannungsabhängige Verluste (für 6/10 kV und >35/60 kV): Pd = ω × C'b × (Ub / √3)² × tan δ — Formel (18.33)
- Stromwärmeverluste: Pi = I²Br × Rwr — Formel (18.34)
- Verluststundenzahl: Tv = τ × TB — Formel (18.35)

**Symbole der Kabelkostenrechnung:**
- ka — Strompreis, Arbeitskosten [Euro/kWh]; kl — Leitungsverlustkosten [Euro/kWh]; l — Länge der Kabelverbindung [km]; p — Jahreszinsfluss [%]; m — Belastungsgrad; t — Tilgungsdauer [a]; IB — Betriebsstrom [A]; C'b — Betriebskapazitätsbelag des Kabels [F/km]; K — Jahreskosten [Euro/a]; Ka — Anschaffungskosten [Euro]; Kd — Kapitaldienst [Euro/a]; Kv — Verlustkosten [Euro/a]; Ns — Anzahl der Systeme; NK — Anzahl der Kabel je System; S — Leiterquerschnitt [mm²]; Pi — Stromwärmeverluste [kW/km]; Pd — dielektrische Verluste [kW/km]; Rwr — Wirkwiderstandsbelag [Ω/km]; T — Tilgungssatz [%]; TR — Tilgungserhöhung durch Kosten [%]; γ — Lastangriffsfaktor; TB — jährliche Einschaltdauer; Tv — Verluststundenzahl [h/a]; t — Zeitraum; ω — Kreisfrequenz [s⁻¹]; tan δ — dielektrischer Verlustfaktor; τ — Verlustfaktor
