# Fachinformation_E-09_Schutzbereich_SPD_2022-03 — Teil 0
> Quelle: Fachinformation_E-09_Schutzbereich_SPD_2022-03 (normen) · Seiten 1-15.

OVE-Fachinformation E09 (Ausgabe 2022-03-01), zuständig OVE/TSK E05 „Elektrische Betriebsmittel“. Behandelt den **wirksamen Schutzbereich von SPD** (Surge Protective Devices / Überspannungs-Schutzeinrichtungen): wie weit eine SPD entlang der Leitung schützt, beeinflusst durch Schwingungen und Induktion, inkl. der „10 m-Regel“, Berechnungsformeln und beispielhaft berechneter Schutzbereiche. Dieser Teil deckt das gesamte Dokument ab (Abschnitte 1–3, Anhänge A–C, Literaturhinweise).

## Inhalt

### 1.1 Potentialausgleich (Voraussetzung)
- Schutzpotentialausgleich (Hauptpotentialausgleich) nach **OVE E 8101 Abschnitt 411.3.1.2** und, soweit erforderlich, der zusätzliche Schutzpotentialausgleich nach **OVE E 8101 Abschnitt 415.2** sind **Voraussetzung** für wirkungsvollen Schutz gegen transiente Überspannungen und Blitzeinwirkungen.
- Ergänzende Anforderungen für Blitzschutzpotentialausgleich: **ÖVE/ÖNORM EN 62305-3**.

### 1.2 Schirmung
- Grundsätzliche Maßnahmen gegen Störspannungen/elektromagnetische Störgrößen: **OVE E 8101 Teil 4-44**.
- Schirmung hält bei höheren Frequenzen auftretende elektrische/magnetische Felder fern bzw. schützt Umgebung; reduziert Felder und verhindert Induktion von Spannungen in Kabel/Leitungen.
- Erreicht durch:
  - **a)** Kabel/Leitungen mit metallenem Schirm, vorzugsweise **direkt beidseitig** aufgelegt. Ist das betriebstechnisch nicht möglich: eine Seite direkt, andere Seite über Überspannungs-Schutzeinrichtungen (indirekte Erdung) auflegen.
  - **b)** Schirmung der Kabel-/Leitungswege durch (vorzugsweise geschlossene) metallene, durchverbundene und geerdete Kabelkanäle/-trassen oder durchverbundene und geerdete metallene Installationsrohre.
  - **c)** Verlegung **blanker paralleler Erder** bei erdverlegten Kabeln: empfohlener Abstand etwa **30 cm mittig** über den Kabel-/Leitungssystemen. Bei breiteren Trassen **ab Breite 60 cm** zusätzliche parallele Erder (empfohlener Abstand der parallelen Erder etwa **60 cm**, Bild 1). Parallele Erder an beiden Enden mit der übrigen Erdungsanlage verbinden.
- Nähere Infos Schirmwirkung offener Kabel-/Leitungsführungssysteme: **OVE EN 50174-2:2018**. Mindestquerschnitt von Schirmen (Kabel-/Leitungsschirm oder Tragsystem): **ÖVE/ÖNORM EN 60305-3**.
- **Wichtig:** Nur **ferromagnetische Werkstoffe** sind bei Schirmungen auch gegen elektromagnetische Felder wirksam.

### 1.3 Indirekte/direkte Blitzeinwirkungen + Naheinschläge — Einflussparameter
- **a) Indirekte Blitzeinwirkungen** (leitungsgebundene Störungen) auf Schutzbereich von SPD:
  - Schwingungen mit zunehmender Leitungslänge und in Abhängigkeit der angeschlossenen Lasten (induktiv, kapazitiv).
- **b) Direkte Blitzeinwirkungen / Naheinschläge:**
  - Schwingungen (s.o.);
  - Induktionen mit zunehmender Leiterschleifengröße (Schleifenfläche zwischen aktiven Leitern und Schutzleiter/Potentialausgleich);
  - Induktionen mit zunehmender Schleifengröße zwischen unterschiedlichen Leitungssystemen (z.B. Energie- ↔ Datenkabel);
  - galvanisch eingekoppelte Teilblitzströme infolge direkten Einschlags in ein außen angebrachtes Betriebsmittel, in dessen Zuleitung ein SPD installiert ist.
- ANMERKUNG: außen angebrachte Betriebsmittel = jede Art elektrischer/elektronischer/funktechnischer Betriebsmittel, z.B. Beleuchtung, Klimaanlagen, Sensoren (Temperatur, Druck), Antennen, Überwachungskameras (an baulichen Anlagen, Masten, Prozessbehältern).
- Diese Fachinformation beschränkt sich ausschließlich auf **Schwingungen und Induktionen**.

#### 1.3.1 Begrenzung des Schutzbereichs aufgrund von Schwingungen
- Eine SPD begrenzt beim Ansprechen die Überspannung an ihrem Einbauort. Zu lange Leitungen zwischen SPD und Betriebsmittel → Ausbreitung von Stoßwellen → Schwingungserscheinungen.
- An offenen Anschlussklemmen kann die Überspannung bis auf den **doppelten Begrenzungswert** der SPD ansteigen → Ausfall des Betriebsmittels, auch wenn der Schutzpegel der SPD nicht höher ist als die Stehstoßspannungsfestigkeit des Betriebsmittels.
- Wirksamer Schutzbereich = zulässige Leitungslänge zwischen SPD und Betriebsmittel mit noch ausreichender Schutzwirkung; hängt ab von SPD-Technologie, Ausführung der Anschluss-/Verbindungsleitungen, Lastimpedanzen.
- **Konventionell vereinbarter wirksamer Schutzbereich = 10 m**, wenn die SPD einen Schutzpegel entsprechend der geforderten Überspannungskategorie aufweist.
- Wirksamer Schutzbereich kann **vernachlässigt** werden, wenn der Schutzpegel der SPD **50 % der Stehstoßspannung** der geforderten Überspannungskategorie **nicht überschreitet** (auch unter Berücksichtigung des Schwingungsfaktors 2 / Reflexion, Abschnitt 1.6, keine Überlastung zu erwarten).
- Wenn Leitungslänge **> 10 m** UND Schutzpegel **> 50 %** der Stehstoßspannung: wirksamer Schutzbereich aufgrund Schwingungen (LPO) nach **Anhang A** abschätzen.

#### 1.3.2 Begrenzung des Schutzbereichs aufgrund von Induktion
- Blitzeinschläge in/neben die bauliche Anlage induzieren Überspannung in die Leiterschleife zwischen SPD und Betriebsmittel; diese addiert sich zum Schutzpegel der SPD und verringert deren Wirksamkeit.
- Induzierte Überspannungen ↑ mit Abmessungen der Leiterschleife (Leitungsführung, Länge des Stromkreises, Abstand zwischen PE und aktiven Leitern, Schleifenfläche); ↓ durch Abschwächung der magnetischen Feldstärke (ferromagnetische Schirmung oder Abstand).
- Begrenzung aufgrund Induktion (Lpi) nach **Anhang B** abschätzbar.
- **Bauliche Ausführung — beispielhafte Anwendungen:**
  - **a)** 230 V AC Betriebsmittel (mind. Überspannungskategorie II), nur über eine Anspeisung;
  - **b)** ungeschirmte Leitung;
  - **c)** Potentialausgleichs-Netzwerk vorhanden, z.B. gemäß **OVE-Richtlinie R 15**;
  - **d)** Vermeidung von Installationsschleifen durch mehradrige Leitung bzw. alle Leiter (inkl. Schutzleiter) in einem Installationsrohr/Kanal → **Schleifenfläche ≤ etwa 0,5 m²**;
  - **e)** Betriebsmittel mit mehreren Leitungen: Vermeidung größerer Schleifen durch parallele Verlegung/gleiche Leitungsführung → **Schleifenfläche ≤ etwa 10 m²**;
  - **f)** Betriebsmittel mit mehreren Leitungen: KEINE Vermeidung größerer Schleifen → **Schleifenfläche ≤ etwa 50 m²**;
  - ergibt eine Leitungslänge entsprechend **Tabelle C.1 (Anhang C)**.
- ANMERKUNG: Berechnungsbasis und Werte aus **ÖVE/ÖNORM EN 62305-4:2008, Anhang D**; seit Ausgabe **EN 62305-4:2012** in diesem Detail nicht mehr Bestandteil der Norm.

### 1.4 Schutzpegel und in der Anlage wirksamer (effektiver) Schutzpegel
- Einrichtungen/Systeme gelten als ausreichend geschützt, wenn Schutzpegel **UP** der SPD **≤ 80 % der Bemessungs-Stehstoßspannung UW** der Überspannungskategorie II.
- Bei 230/400 V Versorgungssystem: 80 % von **UW = 2 500 V** → **2 000 V**.
- Die Herabsetzung um 20 % deckt den induktiven Spannungsabfall ΔU an Anschlussleitungen der SPD und an externen SPD-Abtrennvorrichtungen (z.B. Sicherung) ab; ΔU addiert sich zu UP.
- Für 230/400 V Versorgungssystem pauschal **ΔU = 500 V**.
- In der Anlage wirksamer (effektiver) Schutzpegel: **UP/F = UP + ΔU**.

### 1.5 One-Port SPD vs. Two-Port SPD

#### 1.5.1 One-Port SPD
- SPD, dem zu schützenden Stromkreis **parallel** geschaltet (Definition CLC/TS 61643-12:2009, Abschnitt 3.1.15). Kann getrennte Ein-/Ausgangsklemmen besitzen; **keine definierte Reihenimpedanz**.
- **Vorteile:** Nennstrom der Anlage beeinflusst die SPD nicht; Back-Up-Sicherung im SPD-Abzweig selbst möglich und unabhängig von der Hauptstromkreis-Sicherung bemessbar; Anlage bei Wartung/Austausch nicht zwingend freischalten; Anlage kann bei Versagen der SPD in Betrieb bleiben.
- **Nachteile:** Leitungslängen zu/von der SPD können den wirksamen Schutzpegel drastisch herabsetzen; parallele Verlegung von Zu-/Ableitung der SPD mit Anspeise-/Abgangsstromkreisen kann Einkopplungen in geschützte Abgangsstromkreise verursachen.

#### 1.5.2 Two-Port SPD
- SPD mit separaten Anschlussklemmen für Ein-/Ausgang, dazwischen eine **definierte Reihenimpedanz Z** (Definition CLC/TS 61643-12:2009, Abschnitt 3.1.16). Bauformen: 4-Anschlüsse und 3-Anschlüsse (Bild 3).
- **Vorteile:** Keine separaten „Anschlussleitungen“, gesamter Laststrom über die SPD → Schutzpegel UP entspricht grundsätzlich dem in der Anlage wirksamen Schutzpegel UP/F (siehe 1.4). Eingebaute Reihenimpedanz reduziert Spannungsanstieg (dU/dt) signifikant → Verschiebung des Frequenzspektrums in niederfrequenteren Bereich → minimiert Reflexionswahrscheinlichkeit.
- **Nachteile:** muss Nennstrom, Kurzschluss und Überlast der Anlage führen können; muss Einschaltspitzen standhalten (Erwärmung, Belastung); erzeugt Spannungsabfall im Lastkreis (max. Spannungsabfall beachten); Wartung/Überprüfung schwieriger als bei One-Port SPD.

### 1.6 Reflexion
- Ursache: Änderung des Ladungsflusses durch Änderung der Leiter-Impedanz (Bauelemente: Widerstände, Kapazitäten, Induktivitäten; offene hochohmige Leitungsenden; Querschnittsänderung).
- Bei **totaler Reflexion** kann die Ladung nicht abfließen → ganze Welle „auf sich selbst“ reflektiert → **Amplitude verdoppelt (Faktor 2)** (Bild 4).
- Jede sprunghafte Stromänderung/Stoßstrom erzeugt elektromagnetische Schwingung (Spektrum), breitet sich als Welle auf Leitungen aus (im Raum: Übersprechen).
- Reflexionen entstehen: an offenen Leitungsenden (hochohmig); bei Änderung des Leitungsquerschnitts; bei Änderung der Leitungsimpedanz; an Verbindungsstellen (Durchkontaktierungen, Steckverbindungen).
- Je höher die Anstiegssteilheit eines Stoßstromes / je höher das Frequenzspektrum, umso eher treten Reflexionen auf.

### 2 Zusammenhang Mindestableitstoßstrom ↔ Schutzpegel
- **OVE E 8101 Unterabschnitt 534.4.4** legt das Mindest-Stoßableitvermögen für SPD fest.
- **OVE E 8101 Unterabschnitt 534.4.4.2** beschreibt die Auswahl des Schutzpegels einer SPD bzw. SPD-Kombination in Abhängigkeit der Nennspannung der Anlage.
- Die meisten marktverfügbaren SPD haben einen Nennableitstoßstrom deutlich über den Mindestwerten aus **OVE E 8101 Unterabschnitt 534.4.4.4.1, Tabelle 534.3**. Der nach Produktnorm **ÖVE/ÖNORM EN 61643-11** vom Hersteller auszuweisende Schutzpegel UP bezieht sich immer auf diesen Nennableitstoßstrom.

### 3.1 Beispiel: Schutz gegen indirekte Blitzeinwirkungen (10 m-Regel)
- Anwendung: Wohnbau/Büro/(Klein-)Gewerbe, **3N 230/400 V AC TN-System**. Schutz gegen indirekte Blitzeinwirkungen nach **OVE E 8101 Unterabschnitt 534.4.4.4.1**.
- **Anschlussart 1**, geforderter Schutzpegel nach OVE E 8101 Unterabschnitt 534.4.4.2 und **Tabelle 534.1 = 2 500 V**.
- **Typ 2 SPD:** Nennableitstoßstrom **In = 40 kA**, Schutzpegel **UP = 1 500 V**.
- Zusätzliche Herstellerangaben (Schutzpegel bei verschiedenen Strömen):
  - 1 kA → **850 V**
  - 5 kA → **1 000 V**
  - 10 kA → **1 200 V**
  - 20 kA → **1 350 V**
- Geforderter Mindest-Nennableitstoßstrom nach **Tabelle 534.3**:
  - Schutzpfad **L–PE: 5 kA** → Schutzpegel lt. Hersteller **1 000 V**
  - Schutzpfad **N–PE: 5 kA** → Schutzpegel lt. Hersteller **1 000 V**
- Bewertung: Schutzpegelforderung nach Tabelle 534.1 und 80 %-Empfehlung (0,8 · 2 500 V = **2 000 V**) mit großer Sicherheitsreserve eingehalten.
- Da Schutzpegel **< 50 %** des nach Tabelle 534.1 geforderten Wertes (2 500 V): **zweiter Thesenstrich in OVE E 8101 Unterabschnitt 534.4.9** → **keine weiteren SPD erforderlich**, auch wenn Leitungslänge zwischen diesen SPD und Betriebsmitteln > 10 m beträgt.

### 3.2 Beispiel: Schutz gegen direkte und indirekte Blitzeinwirkungen

#### 3.2.1 Wohnbau/Büro/(Klein-)Gewerbe
- **3N 230/400 V AC TN-System**. Innerer Blitzschutz nach **ÖVE/ÖNORM EN 62305-4** und **OVE E 8101 Unterabschnitt 534.4.4.4.2**.
- **Anschlussart 1**, geforderter Schutzpegel nach Unterabschnitt 534.4.4.2 und Tabelle 534.1 = **2 500 V**.
- **Typ 1 SPD:** Blitzstoßstrom **Iimp = 12,5 kA**, Nennableitstoßstrom **In = 40 kA**, Schutzpegel **UP = 1 600 V**.
- Zusätzliche Herstellerangaben:
  - 1 kA → **800 V**
  - 5 kA → **900 V**
  - 10 kA → **1 000 V**
  - 20 kA → **1 200 V**
- Betriebsmittel + bauliche Ausführung:
  - **a)** 230 V AC Betriebsmittel (mind. Überspannungskategorie II), nur eine Anspeisung;
  - **b)** ungeschirmte mehradrige Leitungen oder alle Leiter (inkl. Schutzleiter) in einem Installationsrohr/Kanal → Schleifenfläche **≤ 0,5 m²**;
  - **c)** Potentialausgleichs-Netzwerk vorhanden, z.B. gemäß OVE-Richtlinie R 15;
  - **d)** Vermeidung von Installationsschleifen → Schleifenfläche **≤ etwa 0,5 m²**.
- Geforderter Mindest-Blitzstoßstrom nach **OVE E 8101 Tabelle 534.4**:
  - Schutzpfad **L–PE: 12,5 kA** → Schutzpegel lt. Hersteller **ca. 1 050 V**
  - Schutzpfad **N–PE: 12,5 kA** → Schutzpegel lt. Hersteller **ca. 1 050 V**
- Bewertung: Schutzpegelforderung Tabelle 534.1 + 80 %-Empfehlung (2 000 V) mit großer Sicherheitsreserve eingehalten. Schutzpegel < 50 % von 2 500 V → zweiter Thesenstrich Unterabschnitt 534.4.9 → keine weiteren SPD nötig, auch bei Leitungslänge > 10 m.
- Da ermittelter Schutzpegel nur **ca. 40 %** des geforderten Wertes (2 500 V), ergibt sich nach **Tabelle C.1 (Anhang C)** (interpolierte Werte für **UP = 1 050 V**) ein wirksamer Schutzbereich:
  - Bei Einschlägen **nahe** einer baulichen Anlage **ohne räumliche Schirmung**: **> 1 250 m** → Leitungslänge vernachlässigbar;
  - Bei **direkten** Einschlägen in die bauliche Anlage **ohne gitterförmiges LPS**: **etwa 21 m**;
  - Bei direkten Einschlägen + **gitterförmiges LPS** (z.B. Baustahlarmierung): **etwa 79 m**.

#### 3.2.2 Einrichtungen für Sicherheitszwecke (OVE E 8101:2009 Abschnitt 35)
- Derartige Anlagen sind im Regelfall nicht nur mit Energieleitungen, sondern auch mit Datenleitungen (Busleitungen) verbunden → erhebliche Schleifenbildung (z.B. Melde-Loop; Schleife zwischen Energieversorgung und Rufweiterleitung bei Gefahrenmeldeanlagen).
- Beispiel: Sicherheitsbeleuchtungsanlage mit Netzzuleitung, Datenanbindung, Fernanzeigen, Verbindungen zu Unterstationen (Bild 5). Bauliche Ausführung gemäß Abschnitt 1.3.2 Unterpunkte a), b), c). Schleifenbildung gemäß Unterpunkte e) oder f).
- **Wirksamer Schutzbereich bei Einschlag nahe der baulichen Anlage ohne räumliche Schirmung**, angenommener SPD-Schutzpegel **1 100 V**:
  - nach **e)**: max. Leitungslänge **60 m**;
  - nach **f)**: max. Leitungslänge **12 m**.
- **Wirksamer Schutzbereich bei direktem Einschlag mit gitterförmigem LPS**, angenommener SPD-Schutzpegel **1 100 V**:
  - nach **e)**: max. Leitungslänge **3,7 m**;
  - nach **f)**: Leitungslänge **< 1 m**.
- **Typ 1 SPD** ist für **alle Leitungen erforderlich**, bei denen Risiko galvanischer Einkopplung eines (Teil-)Blitzstromes besteht; z.B. Fernanzeigen und/oder Stromkreise für im Freien installierte Betriebsmittel oder gebäudeüberschreitende Leitungsverbindungen zu Unterstationen.

### Anhang A — Schutzbereich aufgrund von Schwingungen (Formel)
- Bedingung: Leitungslänge > 10 m UND Schutzpegel der SPD > 50 % der Stehstoßspannung der geforderten Überspannungskategorie.
- **Formel:** `LPO = (UW − UP/F) / k` mit **k = 25 V/m**.
- Legende:
  - **LPO** = wirksamer Schutzbereich aufgrund von Schwingungen in m;
  - **UW** = Bemessungs-Stehstoßspannung des zu schützenden Betriebsmittels;
  - **UP/F** = in der Anlage wirksamer (effektiver) Schutzpegel;
  - **k** = erwartete Induktionsspannung je Meter Leitung in V/m.

### Anhang B — Schutzbereich aufgrund von Induktion (Formel)
- **Formel:** `Lpi = (UW − UP/F) / h`
  - **h = 300 · KS1 · KS2 · KS3** [V/m] bei Blitzeinschlägen **nahe** der baulichen Anlage, oder
  - **h = 30 000 · KS0 · KS2 · KS3** [V/m] bei Blitzeinschlägen **in** die bauliche Anlage.
- Legende:
  - **Lpi** = wirksamer Schutzbereich aufgrund von Induktion in m;
  - **UW** = Bemessungs-Stehstoßspannung des zu schützenden Betriebsmittels;
  - **UP/F** = in der Anlage wirksamer (effektiver) Schutzpegel;
  - **KS1** = räumliche Schirmung durch äußeres LPS o.a. Schirme an Grenze LPZ 0 auf 1;
  - **KS2** = räumliche Schirmung durch Schirme an Grenze LPZ 1 auf 2 oder höher;
  - **KS3** = Kennwerte der inneren Verkabelung;
  - **KS0** = Faktor für Schirmwirkung eines äußeren LPS an Grenze LPZ 0 auf 1:
    - **KS0 = 0,06 · w^0,5** für gitterförmiges äußeres LPS (Maschenweite w in m), oder
    - **KS0 = kc** für nicht gitterförmiges äußeres LPS (siehe ÖVE/ÖNORM EN 62305-3:2012, Anhang C).
- ANMERKUNG 1: KS1, KS2, KS3 näher beschrieben in **ÖVE/ÖNORM EN 62305-2:2012, Abschnitt B.5**; KS0 in **ÖVE/ÖNORM EN 62305-4:2008, Abschnitt D.2.4**.
- **Ungünstigster Fall:** KS1 = KS2 = KS3 = **1** (keine räumliche Schirmung an Grenze LPZ 0A/B→1, keine Schirmung an Grenze LPZ 1→2 oder höher, ungeschirmte Verkabelung).
- Bei vorhandenem **maschenförmigem Potentialausgleichs-Netzwerk** (z.B. OVE-Richtlinie R 15, ÖVE/ÖNORM EN 62305-4, OVE E 8101:2019 Unterabschnitte 444.5.3.4 und 444.5.4): KS1 und KS2 auf die **Hälfte reduzierbar**.
- ANMERKUNG 2 — Annahmen der Berechnungen für Tabelle C.1:
  - „ohne räumliche Schirmung durch maschenförmiges PA-Netzwerk nach c)“: zumindest sternförmiger Hauptpotentialausgleich → KS1 = KS2 = 1, mit Abschlagsfaktor 0,5 → **0,5**; sowie **KS0 = 0,3** (Annahme ≥ 4 äußere Ableitungen).
  - „mit räumlicher Schirmung durch maschenförmiges PA-Netzwerk nach c)“: Maschenweite **w = 5,0 m** → KS1 = KS2 = **0,3** (berechnet nach KS1 = KS2 = 0,12·w·0,5) und KS0 = 0,06 · w^0,5.
  - **KS3 = 0,01, 0,2 oder 1** je nach Schleifengröße.
  - Gebäudeschirmung mittels Metallblech: KS1 = KS2 = **10⁻⁴**.
  - Leitungsschirmung: KS3 = **10⁻⁴**.
  - Verlegung von Leiterschleifen nahe der räumlichen Schirmung (0,1·w bis 0,2·w) wurde nicht berücksichtigt.

### Anhang C — Tabelle C.1: Beispielhaft berechnete Schutzbereiche (230/400 V Versorgungssystem)
Wirksamer Schutzbereich [m Leitungslänge] in Abhängigkeit des wirksamen (effektiven) Schutzpegels UP/F. Listenpunkte beziehen sich auf Abschnitt 1.3.2.

**Achsen / Zuordnung Schutzpegel:**
- Schutzpegel SPD (Herstellerangabe) **UP [V]**: 1 500 / 1 600 / 1 700 / 1 800 / 1 900 / 2 000 / 2 100 / 2 200 / 2 300 / 2 400 / 2 500.
- Zugehöriger wirksamer (effektiver) Schutzpegel **UP/F [V]** (= UP + ΔU, ΔU pauschal 500 V — Fußnote a): 1 000 / 1 100 / 1 200 / 1 300 / 1 400 / 1 500 / 1 600 / 1 700 / 1 800 / 1 900 / 2 000.

**A) Schutz gegen Schwingungen** (wirksamer effektiver Schutzpegel > 50 % der geforderten Stehstoßspannung Überspannungskategorie II):
- Werte (für UP 1 500→2 500, soweit berechnet): **28 / 24 / 20 / 16 / 12 / 10ᵇ / 10ᵇ / 10ᵇ** (für die niedrigeren Schutzpegel keine Berechnung nötig, da UP < 50 % von 2 500 V).

**B) Schutz gegen indirekte Blitzeinwirkungen (KEIN Blitzschutz)** — ohne räumliche Schirmung durch maschenförmiges PA-Netzwerk (Listenpunkt c):
- **d) eine angeschlossene Leitung, Schleifenfläche ≤ 0,5 m²:** Werte u.a. **133 / 10ᵇ**; Leitungslänge aufgrund des errechneten Schutzbereichs von **3 704 m bis 370 m nicht relevant**.
- **e) mehrere Leitungen, Schleifenfläche ≤ 10 m²:** **66,7 / 60,0 / 53,3 / 46,7 / 40,0 / 33,3 / 26,7 / 20,0 / 13,3 / 6,7 / 0,0**.
- **f) mehrere Leitungen, Schleifenfläche ≤ 50 m²:** **13,3 / 12,0 / 10,7 / 9,3 / 8,0 / 6,7 / 5,3 / 4,0 / 2,7 / 1,3 / 0,0**.

**B') Mit räumlicher Schirmung durch maschenförmiges PA-Netzwerk (Listenpunkt c), durchschnittl. Maschenweite Zonengrenze LPZ 0/1 = 5 m:**
- **d) ≤ 0,5 m²:** **10ᵇ**; Leitungslänge aufgrund Schutzbereich von **1 333 m bis 267 m nicht relevant**.
- **e) ≤ 10 m²:** **185,2 / 166,7 / 148,1 / 129,6 / 111,1 / 92,6 / 74,1 / 55,6 / 37,0 / 18,5 / 0,0**.
- **f) ≤ 50 m²:** **37,0 / 33,3 / 29,6 / 25,9 / 22,2 / 18,5 / 14,8 / 11,1 / 7,4 / 3,7 / 0,0**.

**B'') Räumliche Schirmung Zonengrenze LPZ 0/1 mittels durchgängigem Metallblech** (z.B. Industriebau mit Metallfassade/Blechdach), unabhängig von d)–f): Leitungslänge bei vollständiger ferromagnetischer Metallblechschirmung **nicht relevant** (extrem großer Schutzbereich).

**B''') Ohne maschenförmiges PA-Netzwerk, aber Leitungsschirmung** (durchgehend geschirmte Kabel/Kabelkanäle), unabhängig von d)–f): Leitungslänge **nicht relevant** (Kabelschirme/metallische Schirmungen an **beiden Enden** in den Potentialausgleich einbeziehen).

**C) Schutz gegen direkte Einschläge in die bauliche Anlage (direkter Blitzschutz)** — Tabelle C.1 (2 von 2):
- **d) eine Leitung, ≤ 0,5 m²:**
  - äußeres LPS mit mehreren Ableitungenᵈ: **22,2 / 20,0 / 17,8 / 15,6 / 13,3 / 11,1 / 10ᵇ / 10ᵇ / 10ᵇ / 10ᵇ / 10ᵇ**.
  - gitterförmiges äußeres LPS (z.B. Baustahlarmierung einbezogen), Maschenweite LPZ 0/1 = 5 m: **82,8 / 74,5 / 66,3 / 57,9 / 49,7 / 41,4 / 33,1 / 24,8 / 16,6 / 10ᵇ / 10ᵇ**.
- **e) mehrere Leitungen, ≤ 10 m²:**
  - äußeres LPS mit mehreren Ableitungenᵈ: **1,1 / 1,0** (sehr kleiner Schutzbereich).
  - gitterförmiges äußeres LPS, Maschenweite 5 m: **4,1 / 3,7 / 3,3 / 2,9 / 2,5 / 2,1 / 1,7 / 1,2**.
- **f) mehrere Leitungen, ≤ 50 m²:** Überspannungsschutz **so nah wie möglich** an den zu schützenden Einrichtungen **immer erforderlich**, da berechneter Schutzbereich deutlich **< 1 m**.
- Mit räumlicher Schirmung LPZ 0/1 mittels durchgängigem Metallblech bzw. mit Leitungsschirmung: Leitungslänge nicht relevant (extrem großer Schutzbereich; Schirme beidseitig in Potentialausgleich).

**Fußnoten Tabelle C.1:**
- **a** wirksamer (effektiver) Schutzpegel UP/F = UP + ΔU, ΔU pauschal **500 V** (siehe Abschnitt 1.4).
- **b** Leitungslänge basiert nicht auf Berechnung, sondern auf Konsens: bis **10 m** Leitungslänge keine zusätzlichen Maßnahmen erforderlich.
- **c** Werte für Auflistung d) berechnet mit **KS3 = 0,01** nach ÖVE/ÖNORM EN 62305-2:2013, Tabelle B.5 (Änderung gegenüber Ausgabe 2008: dort KS3 = 0,02).
- **d** Blitzstromaufteilung **kc ≤ 0,3**.
- Lineare Interpolation des Schutzbereichs [m] in Abhängigkeit des wirksamen Schutzpegels ist zulässig.

### Literaturhinweise
- **OVE E 8101** — Elektrische Niederspannungsanlagen.
- **ÖVE/ÖNORM EN 62305 Reihe** — Blitzschutz.
- **OVE EN 50174-2** — Informationstechnik / Installation von Kommunikationsverkabelung, Teil 2: Installationsplanung und -praktiken in Gebäuden.
- **OVE-Richtlinie R 15** — EMV-, Potentialausgleichs-, Erdungs-, Blitzschutz- und Überspannungsschutz-Konzept in Gebäuden – Allgemeines.
- **CLC/TS 61643-12:2009** — Low-voltage surge protective devices, Part 12 (Selection and application principles).
- **ÖVE/ÖNORM EN 61643-11** — Überspannungsschutzgeräte für Niederspannung, Teil 11 (Anforderungen und Prüfungen).
- Bildquellen u.a.: OVE-Richtlinie R 6-3:2013 (Bild 1); CLC/TS 61643-12:2009 (Bild 2a, 3); DEHN AUSTRIA GmbH (Bild 2b, 5); VDE-Schriftenreihe 83 / Biegelmeier/Kiefer/Krefter (Bild 4).
- Medieninhaber/Hersteller: OVE Österreichischer Verband für Elektrotechnik, Eschenbachgasse 9, A-1010 Wien. Copyright © OVE 2022.
