# Elektrotechnik für Architekten,Bauingenieure und Gebäudetechniker — Teil 8
> Quelle: Elektrotechnik für Architekten,Bauingenieure und Gebäudetechniker (buecher) · Seiten 321-360.

Dieser Teil behandelt zwei Schwerpunkte: Kapitel 24 beschreibt vollständig das Thema Blitzschutzanlagen — von der Planungskoordination über Blitzschutzklassen, Erdungsanlagen, Trennungsabstände und das EMV-Blitzschutzzonen-Konzept bis hin zu Überspannungsschutz, Prüfungsmaßnahmen und Dokumentation. Kapitel 25 leitet über zur Tages- und Kunstlichtplanung: lichttechnische Grundbegriffe, Beleuchtungskonzepte, Gütemerkmale, Beleuchtungsarten und Planungsberechnungen (Lichtstrommethode, Lichtstärkemethode) werden systematisch aufgearbeitet.

## Inhalt

---

### 24. Blitzschutzanlagen — Planung und Koordination

**Planung (Abschnitt 24.2):**
- Im Entwurfs- und Ausführungsstadium müssen Blitzschutz-Planer, Errichter, Auftraggeber, Architekt und Bauausführender regelmäßig zusammenarbeiten. Regelmäßige Abstimmungsgespräche führen zu einem wirksamen System bei minimalen Kosten.
- Laut aktueller Blitzschutznorm ist der Architekt für die Koordination der Schutzmaßnahme verantwortlich.
- Versicherer fordern Blitzschutz nach VdS-Richtlinie 2010.
- Eine vollständige Blitzschutzanlage umfasst drei Hauptbestandteile:

**1. Äußerer Blitzschutz:**
- Enthält alle Einrichtungen zum Auffangen und Ableiten des Blitzstroms in die Erdungsanlage.
- Fangeinrichtung = vorgesehener Einschlagpunkt; Maschenweite der Fangleitungen:
  - Normale Gebäude: max. 10 m × 20 m
  - Krankenhäuser: max. 10 m × 10 m
- Kein Punkt der Dachfläche darf mehr als 5 m von einer Fangleitung entfernt sein.
- Höhe der Fangstange: max. 2 m; Abstand zum Gebäude mindestens 2 m.
- Schutzwinkel der Fangstange: 45°. Gebäude gilt als geschützt bei diesem Winkel.
- Dachaufbauten aus elektrisch nichtleitendem Material: dürfen nicht höher sein als 0,3 m.
- Dachlüfter darf ohne Einbindung ins Blitzschutzkonzept nicht angeschlossen werden; Schutz über Fangstange erfordert Abstandsermittlung gemäß Bild 24.5.
- Fangeinrichtungen sind bevorzugt an Ecken und Kanten anzubringen.
- **Ableitungen:** verbinden Fangeinrichtung mit Erdungsanlage; je 20 m Gebäudeumfang (gemessen an Dachaußenkanten) eine Ableitung, ausgehend von den Ecken. Mindestens zwei Ableitungen sind verpflichtend.
- Ableitungen müssen so angeordnet sein, dass:
  - mehrere parallele Strompfade entstehen,
  - Stromleitungswege so kurz wie möglich bleiben,
  - Potentialausgleichsverbindungen hergestellt werden,
  - keine Beeinflussung von Sicherheitsbereichen stattfindet,
  - eine Verbindung untereinander nahe der Erdoberfläche möglich ist.
- Ableitungen erhalten Trennstellen für spätere Messungen.

**2. Innerer Blitzschutz:**
- Schutz elektrischer Installationen im Gebäudeinneren gegen Blitzstrom und elektromagnetische Felder.
- Hauptbestandteil ist der Potentialausgleich, an den alle metallischen Rohre, Starkstrom- und Informationstechnikanlagen angeschlossen werden.
- Für informationstechnische Einrichtungen bietet das Blitzschutzzonen-Konzept den besten Schutz.

**3. Überspannungsschutz:**
- Schutz elektrischer/elektronischer Geräte gegen Überspannungen aus atmosphärischen Entladungen (Nah-, Direkt-, Ferneinschläge in NS-Anlagen) und Schalthandlungen (Abschalten induktiver Lasten, Ein-/Ausschalten von Leuchtstofflampen, Erd- und Kurzschlüsse, Auslösen von Sicherungen).
- Hauptschutz-Potentialausgleich muss nach DIN VDE 0100 Teil 540 in jedem Gebäude installiert sein.
- An die Haupterdungsschiene sind anzuschließen: alle leitfähigen Teile, metallische Rohre, Energie- und Informationsanlagen, Gas-/Wasser-/Heizrohrleitungen, Metallteile der Gebäudekonstruktion, Erder, Blitzschutzanlagen.
- Blitzschutz-Potentialausgleich gilt als erfüllt, wenn alle eingeführten Systeme über Blitzstrom-Ableiter nahe der Eintrittsstelle angeschlossen sind (Ausführung nach DIN EN 62305-3 / VDE 0185-305-3 auf Basis DIN VDE 0100-410/-540).

---

### 24.3 Blitzschutzklassen

Vor Planung einer Blitzschutzanlage ist eine Risikoanalyse (mit geeigneter Software) durchzuführen und die Schutzklasse zu bestimmen.

**Tabelle: Charakteristik der Blitzschutzklassen**

| Blitzschutzklasse | Kugelradius (m) | Maschenweite (m) | Wirkungsgrad (%) |
|:-----------------:|:---------------:|:----------------:|:----------------:|
| I                 | 20              | 5 × 5            | 98               |
| II                | 30              | 10 × 10          | 95               |
| III               | 45              | 15 × 15          | 90               |
| IV                | 60              | 20 × 20          | 80               |

Für jede Schutzklasse lässt sich der Schutzwinkel eines Gebäudes abhängig von der Höhe der Fangeinrichtung über Erdboden ablesen.

**Methoden zur Festlegung der Fangeinrichtungslage:**
1. Schutzwinkel-Methode (α) — für einfache Gebäudeformen
2. Blitzkugel-Methode (Radius r) — für komplizierte Fälle
3. Maschen-Methode (w) — für ebene Flächen

**Beispiele für Blitzschutzklassen (nach VdS 2010:2010-09):**
- SK I: Bio- und Nuklearanlagen, Gebäude mit Explosionsgefahr
- SK II: Krankenhäuser, Fernmeldetürme, Dome, Industrieanlagen, Kirchen, Museen
- SK III: Wohnhäuser, Höfe, Schulen, Theater, Banken, Bürogebäude, Heime, Kindergärten, Lager
- SK IV: Wetterschutzhütten, Fluchtunterstände

**Tabelle: Mindestquerschnitte von Fangleitungen und Ableitungen (nach DIN VDE 0185-3, Tab. 7)**

| Werkstoff               | Form       | Mindestquerschnitt (mm²) | Mindestmaß / Anmerkung                  |
|-------------------------|------------|--------------------------|------------------------------------------|
| Kupfer                  | Band       | 50                       | Dicke 2 mm                               |
| Kupfer                  | Rund       | 50                       | Ø 8 mm                                   |
| Kupfer                  | Seil       | 50                       | Einzeldraht Ø 1,7 mm                     |
| Kupfer                  | Rund (c,d) | 200                      | Ø 16 mm                                  |
| Kupfer verzinnt (a)     | Band       | 50                       | Dicke 2 mm                               |
| Kupfer verzinnt         | Rund       | 50                       | Ø 8 mm                                   |
| Kupfer verzinnt         | Seil       | 50                       | Einzeldraht Ø 1,7 mm                     |
| Aluminium               | Band       | 70                       | Dicke 2 mm                               |
| Aluminium               | Rund       | 50                       | Ø 8 mm                                   |
| Aluminium               | Seil       | 50                       | Einzeldraht Ø 1,7 mm                     |
| Aluminiumlegierung      | Band       | 50                       | Dicke 2,5 mm                             |
| Aluminiumlegierung      | Rund       | 50                       | Ø 8 mm                                   |
| Aluminiumlegierung      | Seil       | 50                       | Einzeldraht Ø 1,7 mm                     |
| Aluminiumlegierung      | Rund (d)   | 200                      | Ø 16 mm                                  |
| Stahl feuerverzinkt (b) | Band       | 50                       | Dicke 2 mm                               |
| Stahl feuerverzinkt     | Rund       | 50                       | Ø 8 mm                                   |
| Stahl feuerverzinkt     | Seil       | 50                       | Einzeldraht Ø 1,7 mm                     |
| Stahl feuerverzinkt     | Rund (c,d) | 200                      | Ø 16 mm                                  |
| Nichtrostender Stahl (e)| Band (f)   | 60                       | Dicke 2 mm                               |
| Nichtrostender Stahl    | Band       | 105                      | Dicke 3 mm                               |
| Nichtrostender Stahl    | Rund (f)   | 50                       | Ø 8 mm                                   |
| Nichtrostender Stahl    | Seil       | 70                       | Einzeldraht Ø 1,7 mm                     |
| Nichtrostender Stahl    | Rund (c)   | 200                      | Ø 16 mm                                  |
| Nichtrostender Stahl    | Rund (d)   | 78                       | Ø 16 mm                                  |

Anmerkungen:
- (a) feuerverzinnt oder galvanisch verzinnt, Mittelwert 2 µm
- (b) Zinnüberzug 50 µm
- (c) nur für Fangstangen
- (d) nur für Erdeinführungsstangen
- (e) Chrom ≥ 16 %, Nickel ≥ 8 %, Kohlenstoff max. 0,03 %
- (f) bei nichtrostendem Stahl im Beton: auf 78 mm² (Ø 10 mm) bzw. 75 mm² (3 mm Dicke) erhöhen

---

### 24.3.1 Erdungsanlage

- Gemeinsame, integrierte Erdungsanlage für verschiedene technische Einrichtungen (NS-Anlagen, Fernmeldeanlagen, Blitzschutz) ist zu planen.
- Erdungsanlage muss mit dem Potentialausgleich verbunden sein; Ableitungen daran anschließen.
- Erdungswiderstand: nach DIN VDE 0185 darf er 10 Ω nicht überschreiten.

**Typ A — Flacherder/Tiefenerder:**

1. **Oberflächenerder (Horizontalerder):**
   - Einbringtiefe: mindestens 0,5 m; Länge je Ableitung: 5 m
   - Kann aus Rund- oder Flachleitern bestehen; als Ring-, Strahlen-, Maschenerder oder Kombination

2. **Tiefenerder (Vertikalerder):**
   - Wenn kein Fundament- oder Ringerder verwendbar: je Ableitung ein Einzelerder
   - Variante 1: Oberflächenerder mit 20 m Länge
   - Variante 2: Tiefenerder mit 9 m Länge, 1 m Abstand vom Fundament, senkrecht eingebracht
   - Vorteil: in größeren Tiefen geringerer spezifischer Erdwiderstand; Frost hat keinen negativen Einfluss auf den Erdungswiderstand
   - Mindestabstand von Tiefenerdern untereinander: 1,5-fache der Erder-Länge
   - Tiefenerder nur zulässig, wenn miteinander verbunden

**Typ B — Ring- und Fundamenterder:**

3. **Ringerder:**
   - Oberflächenerder, als geschlossener Ring; Verlegetiefe mindestens 0,5 m; Abstand um das Außenfundament: 1 m
   - 80 % der Erderlänge muss Erdkontakt haben
   - Einsatz bei isolierten Bodenplatten

4. **Fundamenterder:**
   - Für optimale Funktion des Hauptschutzpotentialausgleichs sehr geeignet
   - Nach DIN 18014 als geschlossener Ring in Fundamenten der Außenwände
   - Bei größeren Gebäuden (Kantenlängen > 20 m): Querverbindungen zur Maschenbildung ca. 20 m × 20 m
   - Mindestmaterial: Bandstahl 30 mm × 3,5 mm oder Rundstahl Ø 10 mm
   - Kann als Erder für Blitzschutz-, Fernmelde- und Niederspannungsanlagen gemeinsam dienen

**Ausbreitungswiderstand:**
- Abhängig von: spezifischem Erdwiderstand, Masse der Anordnung, Länge des Erders — weniger vom Querschnitt
- Spezifischer Erdwiderstand (ρE) in Ωm definiert als Widerstand eines Erdwürfels 1 m³ (1 m Kantenlänge), gemessen zwischen zwei gegenüberliegenden Würfelflächen

**Tabelle: Spezifischer Widerstand verschiedener Bodenarten (nach EN 50522)**

| Bodenart               | ρE (Ωm, Mittelwert) |
|------------------------|---------------------|
| Moorboden              | 30                  |
| Lehm, Ton, Humus       | 100                 |
| Sand (feucht)          | 200                 |
| Sand (trocken)         | 1100                |
| Kies (feucht)          | 500                 |
| Kies (trocken)         | 3000                |
| Steiniger Boden        | 1000                |
| Granit                 | 2500                |
| Fels                   | > 10 000            |
| Reines Wasser (13 °C)  | 56                  |
| Reines Wasser (39 °C)  | 34                  |
| Regenwasser            | 30–300              |
| Meerwasser             | 0,22                |

---

### 24.3.2 Werkstoff, Form und Mindestmaße von Erdern

Allgemeine Hinweise:
- Überzug muss glatt, durchgehend und frei von Flussmittelresten sein; Mindestdicke: 50 µm (Rundmaterial), 70 µm (Flachmaterial)
- Gewinde müssen vor der Verzinkung geschnitten werden
- Verzinnen als Alternative möglich
- Kupfer soll mit Stahl unlösbar verbunden und vollständig in Beton eingebettet sein
- Erder im erdberührenden Fundamentteil nur erlaubt, wenn mindestens alle 5 m eine sichere Verbindung mit der Bewehrung besteht
- Legierungsanforderungen nichtrostender Stahl: Chrom 16 %, Nickel 5 %, Molybdän 2 %, Kohlenstoff 0,08 %

**Tabelle: Material, Form und Mindestabmessungen von Erdern (DIN VDE 0185-3, Tab. 8)**

| Material               | Form            | Staberder Ø/mm | Erdleiter mm² | Anmerkung                    |
|------------------------|-----------------|:--------------:|:-------------:|------------------------------|
| Kupfer                 | Seil            | —              | 50            | Mindestdraht Ø 1,7 mm        |
| Kupfer                 | Rund (a)        | —              | 50            | Ø 8 mm                       |
| Kupfer                 | Band            | —              | 50            | Mindestdicke 2 mm            |
| Kupfer                 | Rund            | 20             | —             |                              |
| Kupfer                 | Rohr            | 20             | —             | Mindestwandstärke 2 mm       |
| Stahl verzinkt (b,c)   | Rund verzinkt   | 20             | —             |                              |
| Stahl verzinkt         | Rohr verzinkt   | 25             | —             | Mindestwandstärke 2 mm       |
| Nichtrostender Stahl   | Rund            | 20 (10 mm)     | —             |                              |
| Nichtrostender Stahl   | Band (d)        | —              | 100           | Mindestdicke 3 mm            |

Anmerkungen:
- (a) kann auch verzinnt sein
- (b) Zinküberzug: glatt, durchgehend, frei von Flussmittelresten; Mittelwert 50 µm (rund), 70 µm (flach)
- (c) Material muss vor der Verzinkung in Form gebracht werden

**Tabelle: Mindestabmessungen von Leitern (DIN VDE 0185-3, Tab. 9)**

Verbindungsleitungen von Potentialausgleichsschienen (PAS) untereinander und zur Erdungsanlage:

| Blitzschutzklasse | Werkstoff  | Querschnitt (mm²) |
|:-----------------:|------------|:-----------------:|
| I bis IV          | Kupfer     | 16                |
| I bis IV          | Aluminium  | 25                |
| I bis IV          | Stahl      | 50                |

Verbindungsleitungen von inneren metallenen Installationen zur PAS (DIN VDE 0185-3, Tab. 10):

| Blitzschutzklasse | Werkstoff  | Querschnitt (mm²) |
|:-----------------:|------------|:-----------------:|
| I bis IV          | Kupfer     | 6                 |
| I bis IV          | Aluminium  | 10                |
| I bis IV          | Stahl      | 16                |

---

### 24.4 Trennungsabstand

**Definition Näherung:** Zu geringer Abstand zwischen Blitzschutzanlage und metallenen Installationen oder elektrischen Anlagen, bei dem Über- oder Durchschlagsgefahr besteht.

Näherungen sind zu beseitigen durch:
- Vergrößern des Abstands, oder
- Verbinden der Installationen mit der Blitzschutzanlage direkt oder über Trennfunkenstrecken

**Formel für den Sicherheitsabstand:**

```
s = ki · (kc / km) · l     mit d ≥ s
```

Variablenbedeutungen:
- s = Sicherheitsabstand in m
- d = Trennungs- oder Näherungsabstand in m
- kc = Stromaufteilungskoeffizient (abhängig von geometrischer Anordnung, Tab. 24.7)
- km = Materialkoeffizient in der Trennungsstrecke (Tab. 24.6)
- l = Länge der Blitzschutzleitung
- ki = Blitzschutzklassen-Koeffizient (Tab. 24.6)

**Tabelle: Koeffizientenwerte**

| Blitzschutzklasse | ki    | Material  | km  |
|:-----------------:|-------|-----------|-----|
| I                 | 0,1   | Luft      | 1   |
| II                | 0,075 | Feststoff | 0,5 |
| III–IV            | 0,05  | —         | —   |

**Tabelle: Koeffizient kc nach Typ der Fangeinrichtung**

| Typ der Fangeinrichtung   | Ableitungen auf Erdniveau nicht verbunden (c) | Ableitungen auf Erdniveau verbunden (c) |
|---------------------------|:---------------------------------------------:|:---------------------------------------:|
| Einzelne Fangstange       | 1                                             | 1                                       |
| Gespannte Drähte/Seile    | 1                                             | Bild C405-1                             |
| Vermaschte Leiter         | 1                                             | Bild C405-2                             |

Für die Ermittlung des Stromaufteilungskoeffizienten c stehen drei Varianten zur Verfügung.

---

### 24.5 EMV-Blitzschutzzonen-Konzept

- Das EMV (Elektromagnetische Verträglichkeit)-Blitzschutzzonen-Konzept ist in die internationale Normung eingearbeitet.
- Besonders empfohlen für Gebäude mit umfangreichen elektronischen Einrichtungen.
- Grundprinzip: Raumschirmung — elektromagnetische Felder aus Blitzentladungen werden durch definierte Blitzschutzzonen stufenweise abgebaut.
- Jede Zone ist durch wesentliche Übergänge der Kennwerte der Anlage gekennzeichnet, die das Risiko beeinflussen.
- An den Schnittstellen zwischen Zonen: Einbeziehung in den Potentialausgleich + besondere Ableiter.

**Vier Hauptbereiche des EMV-Blitzschutzkonzepts:**
1. Äußerer Blitzschutz
2. Gebäudeschirmung
3. Raumschirmung
4. Geräteschirmung

**Tabelle: Definition der Blitzschutzzonen**

| Zone                   | Charakteristik                                                                                   |
|------------------------|--------------------------------------------------------------------------------------------------|
| Blitzschutzzone 0      | Direkte Blitzeinwirkung möglich; keine Abschirmung gegen elektromagnetische Felder              |
| Blitzschutzzone 0/E    | Durch Fangeinrichtung gegen direkte Blitzeinwirkung geschützt; keine EM-Feldabschirmung         |
| Blitzschutzzone 1      | Blitzteilströme verursachen energiereiche Transienten, die Schalthandlungen (SEMP) hervorrufen  |
| Blitzschutzzone 2      | Elektromagnetisches Feld weiter gedämpft; Schalthandlungen und elektrostatische Entladungen (ESD) entstehen |
| Blitzschutzzone 3      | Elektromagnetisches Feld auf ein Minimum reduziert                                               |

**Schutzmaßnahmen zur Verringerung der Schadenswahrscheinlichkeit:**

1. An bauliche Anlagen:
   - Blitzschutzsystem mit ausreichender Schutzklasse gegen physikalische Beschädigung und Lebensgefahr (Schäden C1, C2)
   - Überspannungsschutzgeräte am Einführungspunkt eingeführter Leitungen und an inneren Installationen gegen Versagen durch Überspannungen (Schadensursache C3)
   - Magnetische Abschirmungen an/in der baulichen Anlage und/oder Geräteschirmung für empfindliche elektronische Ausrüstungen (Schadensursache C3)

2. An Versorgungsleitungen:
   - Erdungsleitungen zur Verringerung der Wahrscheinlichkeit physikalischer Beschädigungen (Schadensursache C2)
   - Überspannungsschutzgeräte an Übergangspunkten entlang einer Versorgungsleitung und an Leitungsabschlüssen gegen Beschädigung durch Überspannungen (Schadensursache C3)

---

### 24.5.1 Planungsangaben zu Überspannungsableitern

Normgrundlagen für Planung und Projektierung:
- DIN VDE 0185 (neue Blitzschutznorm)
- DIN IEC 1312-1 (Überspannungsschutznorm)
- Leistungsbeschreibung nach VOB Teil C Blitzschutzanlagen oder DIN 18384
- Planung in Leistungsphasen nach HOAI

**Klasseneinteilung der Überspannungsableiter nach Einbauort:**
- **Typ 1 / Anforderungsklasse B / class I:** Blitzstromableiter für die Niederspannungshauptverteilung (NSHV); Kabelquerschnitt 16 mm² ausreichend
- **Typ 2 / Anforderungsklasse C / class II:** Überspannungsableiter für Unterverteilung und feste Installationen; Kabelquerschnitt 4 mm² ausreichend
- **Typ 3 / Anforderungsklasse D / class III:** Überspannungsableiter für Steckdosen und Endgeräte; Kabelquerschnitt 2,5 mm² ausreichend

Normen: DIN VDE 0675-6, IEC 61643-1:1998, EN 61643-11:2001

**Regelung nach TAB 2012:**
- TAB 2012, Abschnitt 12, Punkt 4: Überspannungsschutz nach DIN VDE 0100-443 mit Schutzeinrichtungen Typ 2 und Typ 3 (DIN VDE 0675-6) — Einbau im nicht plombierten Teil der Kundenanlage durch den Errichter.
- TAB 2012, Abschnitt 12, Punkt 5: Überspannungsschutz nach DIN VDE 0185-100 mit Schutzeinrichtungen Typ 1 (DIN VDE 0675-6) — Einbau im plombierten Teil der Kundenanlage zulässig.

---

### 24.6 Prüfungsmaßnahmen

- Prüfung muss von einer Blitzschutz-Fachkraft durchgeführt werden.
- Prüfung muss bestätigen, dass das System vollständig DIN VDE 0185 entspricht.

**Tabelle: Prüfintervalle in Jahren**

| Blitzschutzklasse | Vollständige Prüfung (Jahre) | Sichtprüfung (Jahre) |
|:-----------------:|:----------------------------:|:--------------------:|
| I                 | 2                            | 1                    |
| II                | 4                            | 2                    |
| III–IV            | 6                            | 3                    |

**Prüfumfang — Besichtigung:**
- Vollständigkeit und Normkonformität der technischen Dokumentation
- Übereinstimmung des Gesamtsystems mit den technischen Unterlagen
- Ordnungsgemäßer Zustand von äußerem und innerem Blitzschutz
- Lose Verbindungen und Unterbrechungen im Blitzschutzsystem
- Korrosionsschäden (besonders im Bereich der Erdoberfläche)
- Ordnungsgemäßheit aller Erdungsanschlüsse (soweit sichtbar)
- Ordnungsgemäße Befestigung aller Leitungen und Systembauteile; Funktionsfähigkeit mechanischer Schutzteile
- Änderungen am Gebäude, die zusätzliche Schutzmaßnahmen erfordern
- Richtiger Einbau der Überspannungsschutzgeräte in Energie- und Informationsnetzen
- Beschädigungen oder Auslösungen von Überspannungsschutzgeräten
- Unterbrechungen vorgeschalteter Sicherungen von Überspannungsschutzgeräten
- Lückenloser Blitzschutz-Potentialausgleich für neue Versorgungsanschlüsse oder Ergänzungen seit der letzten Prüfung
- Vorhandensein und Intaktheit von Potentialausgleichsverbindungen innerhalb des Gebäudes

**Prüfumfang — Messen:**
- Alle Verbindungen und Anschlüsse (Fangeinrichtungen, Ableitungen, Potentialausgleichsleitungen, Schirmungsmaßnahmen): niederohmiger Durchgang prüfen (Richtwert < 1 Ω)
- Erdungsanlage:
  - Übergangswiderstand an allen Messstellen zur Feststellung der Durchgängigkeit (Richtwert < 0,1 Ω)
  - Durchgang zu metallenen Installationen (Gas, Wasser, Heizung, Lüftung)
  - Gesamterdungswiderstand des Blitzschutzsystems
  - Erdungswiderstand von Einzelerdern und Teilringerdern

**Ablauf Prüfung Äußerer Blitzschutz:**
1. Alle Trennstellen öffnen
2. Potentialausgleichsschiene vom Erder trennen (TN-Systeme)
3. Zwischen allen Anschlussstellen messen (< 1 Ω)
4. Alle Ableiter-/Fangeinrichtungen messen
5. Alle Ableiter-/Fangeinrichtungen besichtigen
6. Erdungswiderstand messen
7. Trennstellen und Potentialausgleichsschiene wieder schließen
8. Potentialausgleich besichtigen
9. Alle Blitz- und Überspannungs-Ableiter prüfen

---

### 24.7 Montagebeispiel

- Für fachgerechte Planung ist die Gebäudebeschreibung entscheidend. DIN 48830 enthält näheres dazu.
- In der Vorplanungsphase: Blitzschutzklasse auf Basis der Vorschriften mit dem Auftraggeber abstimmen.
- Für Installation und Ausführung: Montageplan und Leistungsverzeichnis erstellen.

**Komponenten einer vollständigen Blitzschutzanlage (Bauteillegende):**

| Nr.   | Bauteil                  |
|-------|--------------------------|
| 1     | Dachleitungen            |
| 2, 3  | Dachleitungshalter       |
| 4     | Auffangspitze            |
| 5     | Dachrinnenklemmen        |
| 6     | Schneefanggitterklemmen  |
| 7     | Regenrohrschellen        |
| 8     | Falzklemme               |
| 9     | Funkenstrecke            |
| 10    | Fangstange               |
| 11, 12| Erdungsrohrschelle       |
| 13    | Universalverbinder       |
| 14    | Ableitungen aus Stahldraht |
| 15    | Leitungshalter           |
| 16    | Erdeinführungsstangen    |
| 16a   | Messstelle               |
| 17    | Regenrohrschellen        |
| 18    | Erdleitungsgraben        |
| 19    | Erdleitung aus Stahldraht |
| 20, 22| Parallelverbinder        |
| 23    | Potentialausgleichsschiene |

---

### 24.8 Dokumentation

- Nach DIN 18014 ist über die Erdungsanlage eine Dokumentation anzufertigen und die Prüfergebnisse einzutragen.

---

### 25. Tages- und Kunstlicht — Einführung und Normen

Relevante Normen und Regelwerke:
- **DIN EN 12464-1** (erschienen März 2003): ersetzt wesentliche Teile der DIN 5035; regelt Anforderungen an Innenraumbeleuchtung
- **DIN 5035-7:** Bildschirmarbeitsplätze
- **DIN 5034-1:** Tageslicht in Innenräumen
- **Arbeitsstättenrichtlinie ASR 7/3**

Hauptthemen des Kapitels:
1. Lichttechnische Größen
2. Beleuchtungskonzepte
3. Beleuchtungsarten
4. Lichttechnische Anforderungen
5. Beleuchtungsplanung

---

### 25.1 Begriffe und Definitionen

**Lichtstrom Φ:**
- Von einer Quelle ausgestrahlte oder von einer Fläche empfangene Lichtleistung; Bewertung der Strahlungsleistung mit der spektralen Empfindlichkeit des Auges
- Einheit: Lumen (lm)
- Beispiel: Eine 58-W-Leuchtstofflampe gibt 5400 lm ab.

**Lichtstärke I:**
- Maß für die räumliche Verteilung des Lichtstroms in eine Richtung, bezogen auf einen Raumwinkel
- Darstellung in Lichtstärkeverteilungskurven (LVK), bezogen auf 1000 lm für verschiedene Bezugsebenen (Polarkoordination der LVK)
- Einheit: Candela (cd) = 1 m/sr (sr = Steradiant)
- SI-Einheit: entspricht Strahlungsleistung von 1/683 W einer monochromatischen Strahlung der Frequenz 540 × 10¹² Hz

**Leuchtdichte L:**
- Beschreibt das von einer Lichtquelle ausgehende Licht; physikalisches Maß des Helligkeitsreizes; bestimmt bei großen Leuchtdichteunterschieden die Blendung
- Einheit: cd/m²

**Materialverhalten bei Lichtauftreffen:**
- Reflexionsgrad ρ: Anteil des zurückgeworfenen Lichts
- Absorptionsgrad α: Anteil des absorbierten Lichts
- Transmissionsgrad τ: Anteil des durchgelassenen Lichts

**Beleuchtungsstärke E:**
- Auf eine bestimmte Fläche auftreffender Lichtstrom; wichtigste Dimensionierungsgröße für Innenraumbeleuchtung
- Einheit: Lux (lx)

**Lichtausbeute η:**
- Maß für die Effektivität einer Lampe
- Einheit: lm/W
- Beispiele: Energiesparlampen 60 lm/W; stabförmige Leuchtstofflampen 90 lm/W

**Lampen — wichtigste Typen im Wohnbereich:**
1. **LEDs** (Light Emitting Diodes): erzeugen nach RGB-Muster nahezu alle Farben
2. **Halogenlampen:** angenehm weißes Licht, sehr gute Farbwiedergabe; mit Netz- oder Kleinspannung betreibbar; besonders effizient: Niedervolt-Halogenlampen mit Infrarotbeschichtung
3. **Energiesparlampen:** neue Generation von Leuchtstofflampen; teilweise dimmbar; sehr gute Farbwiedergabe; geeignet für indirekte, diffuse Raumbeleuchtung (Deckenfluter, größere Schirmleuchten, Stimmungslicht)

**Leuchten:**
- Elektrische Betriebsmittel, die Lampen und Zubehör enthalten und das ausgestrahlte Licht in die gewünschte Richtung lenken (über Reflektoren u. a.)

**Leuchtenwirkungsgrad ηLB:**
- Verhältnis des aus der Leuchte austretenden Lichtstroms zum gesamten abgegebenen Lichtstrom der Lampe

**Beleuchtungswirkungsgrad ηB:**
- Fasst Leuchtenwirkungsgrad und Raumwirkungsgrad in % zusammen

**Raumwirkungsgrad ηR:**
- Verhältnis des von der Bezugsfläche empfangenen Lichtstroms zur Summe aller Gesamtlichtströme der Leuchten der Anlage (in %)

**Vorschaltgerät:**
- Zwischen Versorgungsstromkreis und Entladungslampen geschaltet; dient zur Begrenzung des Lampenstroms

**Sonnenlicht:**
- Sichtbarer Anteil der direkten Sonnenstrahlung

**Tageslicht:**
- Sichtbarer Anteil der Globalstrahlung; verändert Sehaufgabe und Beleuchtungsstärke im Tagesverlauf; verursacht Blendung

**Tageslichtquotient:**
- Verhältnis der Beleuchtungsstärke an einem Punkt (durch direktes oder indirektes Himmelslicht) zur Horizontalbeleuchtungsstärke bei unverbauter Himmelshalbkugel; bei Berechnung sind Einflüsse der Verglasung, Verschmutzung und direktes Sonnenlicht zu berücksichtigen

---

### 25.2 Beleuchtungskonzepte

Planungsparameter bei der Planung von Beleuchtungsanlagen nach DIN EN 12464-1 und DIN 5035-7:
- **Beleuchtungsstärke:** Wartungswert und betreffende Fläche angeben
- **Leuchtdichte:** Wartungswert und betreffende Fläche angeben
- **Blendung:** Schwellenwerterhöhung oder UGR-Wert angeben
- **Farbe:** Farbwiedergabeindex angeben
- **Energie:** Anschlussleistung, Nutzungsdauer, Steuerung bekannt sein
- **Wartung:** Lichtplaner muss Wartungsfaktor festlegen und Wartungsplan erstellen
- **Licht-Messungen:** Messverfahren angeben

DIN EN 12464-1 macht keine Aussagen zur Größe des Bereichs der Sehaufgabe. DIN 5035-7 definiert drei Beleuchtungskonzepte:
1. **Raumbezogene Beleuchtung**
2. **Arbeitsbereichsbezogene Beleuchtung**
3. **Teilflächenbezogene Beleuchtung**

---

### 25.3 Lichttechnische Gütemerkmale

DIN EN 12464-1 beschreibt als Gütemerkmale:
- Wartungswert der Beleuchtungsstärke
- Bewertung der Blendung
- Farbwiedergabe der Lichtquellen
- Der unmittelbare Umgebungsbereich kann mit geringeren Beleuchtungsstärken als die Sehaufgabe beleuchtet werden.

---

### 25.4 Wartungswert der Beleuchtungsstärke

- DIN EN 12464-1 gibt Mindestwerte für Beleuchtungsstärken als Wartungswerte an. Nach Unterschreitung dieser Werte ist die Anlage zu warten, zu reinigen und Lampen zu ersetzen.
- Der Planer legt den Wartungsfaktor selbst fest und erstellt einen Wartungsplan mit: Intervallen für Lampenwechsel, Reinigung der Leuchten und des Raumes, Reinigungsmethoden.

**Empfohlene Wartungsfaktoren:**
- 0,80: sehr sauberer Raum (Reinraum)
- 0,67: sauberer Raum, dreijähriger Wartungszyklus
- 0,57: Außenbeleuchtungsanlagen, dreijähriger Wartungszyklus
- 0,50: Innen- oder Außenbeleuchtungsanlagen bei starker Verschmutzung

**Komponenten des Wartungsfaktors:**
- **LLWF (Lampenlichtstrom-Wartungsfaktor):** beschreibt Abnahme des Lampenlichtstroms über die Nutzungsdauer
- **LLF (Lampenlebensdauerfaktor):** beschreibt Lampenausfall über die Nutzungsdauer
- **LWF (Leuchtenwartungsfaktor):** beschreibt Einfluss der Verschmutzung des optischen Systems zwischen zwei Reinigungen
- **RWF (Raumwartungsfaktor):** beschreibt Verschlechterung der Reflexionsgrade der Raumflächen

Größerer Wartungsfaktor → geringerer Anlagenlichtstrom, weniger Lampen/Leuchten; kleiner Wartungsfaktor → höhere Anlagenlichtströme, mehr Lampen, höhere Investitionskosten.

---

### 25.5 Beleuchtungsstärken

- Blendung muss begrenzt werden, um Herabsetzung der Sehleistung zu vermeiden.
- **UGR-Verfahren** (Unified Glare Rating): zur Begrenzung der Direktblendung; entwickelt für Arbeitssituationen mit vornehmlich horizontaler Blickrichtung und regelm. Deckenleuchten.
- Beleuchtungsstärke und ihre Verteilung im Sehaufgabenbereich und im Umgebungsbereich haben großen Einfluss auf Sehleistung und Sehkomfort.
- **Gleichmäßigkeit der Beleuchtungsstärke:** definiert als Quotient Emin/E (minimale / mittlere Beleuchtungsstärke im Bereich der Sehaufgabe); Faktor von 1,5 vorgegeben.

---

### 25.6 Begrenzung der Direktblendung

- Blendung ist eine Störung durch zu hohe Leuchtdichten oder zu hohe Leuchtdichteunterschiede; kann zu Unfällen, Fehlern und Ermüdung führen.
- Beurteilung erfolgt nach der internationalen UGR-Methode: je größer der UGR-Wert, desto höher die Blendungswahrscheinlichkeit.

UGR-Wert wird beeinflusst von:
- Raumgröße
- Leuchtdichte der Blendquelle (gesehene leuchtende Fläche einer Leuchte)
- Vom Beobachter aus gesehene Größe der Blendquelle
- Lage der Blendquelle im Gesichtsfeld
- Umfeldleuchtdichte

---

### 25.7 Beleuchtungsarten

#### 25.7.1 Allgemeinbeleuchtung
- Raum wird gleichmäßig ausgeleuchtet
- Anordnung der Arbeitsplätze ist veränderbar; seitlicher Lichteinfall empfohlen
- Anwendungsbeispiele: Büros, Industrie

#### 25.7.2 Arbeitsplatzorientierte Allgemeinbeleuchtung
- Arbeitsplätze haben fest angeordnete Raumzonen
- Hohes Beleuchtungsniveau
- Anwendungsbeispiele: Fertigungsbetriebe, Büros

#### 25.7.3 Einzelplatzbeleuchtung
- Einzelne Arbeitsplätze mit höheren Ansprüchen werden intensiver beleuchtet
- Anwendungsbeispiele: Prüftische, Drehmaschinen

---

### 25.8 Lichttechnische Anforderungen

1. **Beleuchtungsniveau:**
   - Nennbeleuchtungsstärke bezieht sich auf mittleren Alterungs- und Verschmutzungszustand
   - Planungsfaktoren: bei normaler Verschmutzung 1,25; bei erhöhter Verschmutzung 1,43; bei starker Verschmutzung 1,67
   - Maßgebende Ebene: 0,85 m über dem Fußboden (horizontale Arbeitsfläche)
   - Verhältnis vertikale zu horizontaler Beleuchtungsstärke: Ev = 1/3 · Eh
   - Nutzebene in Sporthallen und Sportplätzen: 1,0 m über Boden
   - Nutzebene auf Verkehrswegen: 0,20 m über Boden

2. **Gleichmäßigkeit der Beleuchtung:**
   - Alle Arbeitsplätze müssen gleich beleuchtet sein
   - Reflexionsgrade sollen eingehalten werden
   - Gemäß DIN 5035: Emin/E = 1/1,5 muss eingehalten werden

3. **Blendungsbegrenzung:**
   - Weder direkte noch Reflexblendung durch Beleuchtungsanlagen zulässig
   - Für Direktblendung: Güteklassen nach DIN 5035 in Verbindung mit der geforderten Nennbeleuchtungsstärke maßgebend

4. **Lichtrichtung und Schattigkeit:**
   - Blickrichtung grundsätzlich parallel zur Leuchtenachse
   - Günstige Anordnung: Licht fällt von links oben ein
   - Ausreichende Schattigkeit muss gewährleistet sein

5. **Lichtfarbe und Farbwiedergabe:**
   - Strahlungsverteilung einer Lampe bestimmt die Lichtfarbe; gemessen als Farbtemperatur in Kelvin (K)
   - Einteilung der Lichtfarbe von Leuchtstofflampen:
     - Warmweiß (ww): Entspannung und Erholung, hoher Rotanteil; Farbtemperatur < 3300 K
     - Neutralweiß (nw): Handwerk und Industrie; Farbtemperatur 3300 K bis 5300 K
     - Tageslichtweiß (tw): bestimmte Arbeitsräume/-plätze; Farbtemperatur > 5300 K
   - Farbwiedergabeindex Ra beeinflusst das Aussehen beleuchteter Gegenstände
   - Nach DIN 5035: 6 Stufen der Farbwiedergabe; für Wohn- und Innenräume mindestens Stufe 3 (Ra = 80) gefordert
   - Halogenlampen: Ra = 100; Energiesparlampen: Ra ≥ 80; höchstmöglicher Index: 100

---

### 25.9 Auswahl und Errichtung der Betriebsmittel

Betriebsmittel müssen:
- Den geltenden Regeln der Technik entsprechen
- Für den vorgesehenen Verwendungszweck geeignet sein
- Ein Ursprungszeichen tragen
- Mit den Nenngrößen gekennzeichnet sein
- Wirksamkeit der Schutzmaßnahmen sichergestellt sein
- Keine Gefahren von elektrischen Anlagen ausgehen

**Hausinstallation:**
- Lichtstromkreise oder kombinierte Stromkreise mit Steckdosen: nur max. 16-A-LS-Schalter; nach TAB Schaltvermögen 6 kA, Selektivitätsklasse 3
- Alle anderen Räume: Lichtstromkreise max. 25 A oder kleiner
- Drehstromkreise müssen durch einen Schalter, der alle nicht geerdeten Leiter gleichzeitig schaltet, freigeschaltet werden können

**Auswahl von Leuchten — zu berücksichtigen:**
- Zulässige Gebrauchslage
- Brandverhalten der Montagefläche
- Thermische Wirkung auf die Umgebung
- Mindestabstände von Strahlerleuchten
- Aufhängevorrichtung: muss das 5-fache Eigengewicht tragen, mindestens 10 kg
- Wanddosen bei Unterputzinstallation
- Ausführung der Durchgangsverdrahtung mit wärmebeständigen Leitungen

---

### 25.10 Beleuchtungsplanung

Wirtschaftlichkeitsempfehlungen:
- **Hohe Lichtausbeute:** Dreibanden-Leuchtstofflampen haben bis zu 30 % höhere Lichtausbeute als Standard-Leuchtstofflampen
- **Geringe Verlustleistung der Vorschaltgeräte:** Elektronische Vorschaltgeräte bis zu 62 % geringere Verlustleistung; erhöhen nutzbare Lebensdauer der Leuchtstofflampen
- **Hohe Leuchtenwirkungsgrade:** Spiegelrasterleuchten mit Betriebswirkungsgraden bis 75 % energiewirtschaftlich günstiger als opale Wannenleuchten
- **Hohe Beleuchtungswirkungsgrade** durch:
  1. Zweckmäßige Leuchtensysteme und optimale Anordnung
  2. Zweckmäßige Raumgestaltung
  3. Auswahl wirtschaftlicher Leuchtmittel
  4. Computeroptimierte Planung

Notwendige Planungsgrundlagen:
- Grundrisspläne und Höhenschnitte der Räume mit Fenstern und Türen
- Beschaffenheit der Räume (Reflexionsgrade)
- Nutzung der Räume
- Angaben zur Raumtemperatur (Lichtstrom nimmt bei niedriger Temperatur ab)
- Betriebsstunden der Beleuchtungsanlage
- Auswahl der Leuchten

**Tabelle: Lichttechnische Grundgrößen**

| Größe                    | Symbol     | Formel                      | Einheit                    |
|--------------------------|------------|-----------------------------|----------------------------|
| Lichtstrom               | Φ          | —                           | Lumen (lm)                 |
| Lichtstärke              | I          | I = Φ / Ω                  | Candela (cd)               |
| Lichtmenge               | Q          | Q = Φ · t                  | Lumenstunde (lm·h)         |
| Beleuchtungsstärke       | E          | E = Φ / A                  | Lux (lx)                   |
| Lichtausbeute            | η          | η = Φ / P                  | Lumen/Watt (lm/W)          |
| Betriebswirkungsgrad     | ηLB        | ηLB = ΦL / (P · Φ)         | —                          |
| Raumwirkungsgrad         | ηR         | ηR = ΦN / ΣΦL              | —                          |
| Beleuchtungswirkungsgrad | ηB         | ηB = ηR · ηLB              | —                          |

(Ω = Raumwinkel in Steradiant)

Beispiel Standardglühlampe: Leistung 100 W, Lichtstrom 1380 lm, Lichtausbeute 13,8 lm/W

---

#### 25.10.1 Berechnung mit der Lichtstärkemethode

- Erfordert die Kenntnis der Lichtstärkeverteilungskurve (LVK) für die vorgesehene Leuchte.
- Beleuchtungsstärke wird in vorgegebenen Berechnungspunkten auf der Ebene berechnet; aus diesen Punkten wird ein Mittelwert ermittelt.
- Anwendbar für linienförmige, flächenförmige und punktähnliche Lichtquellen.

---

#### 25.10.2 Lichtstrommethode (Wirkungsgradverfahren)

- Überschlägiges Wirkungsgradverfahren, in der Praxis bewährt für Dimensionierung von Beleuchtungsanlagen.
- Voraussetzung: gleichförmige Leuchtenverteilung eines Leuchtentyps.
- Bei Räumen mit Einrichtungen, die Lichtverhältnisse nachhaltig beeinflussen: detaillierte Berechnung mit Computerprogrammen notwendig.

**Erforderliche Eingangsdaten:**
- Raumabmessungen (Länge, Breite, Höhe)
- Reflexionsgrade von Decke, Wänden und Boden
- Art der Tätigkeit / Sehaufgabe
- Möblierung
- Auswahl der Lampen, Leuchten und deren Anordnung

**Berechnungsgang:**

Schritt 1 — Raumindex k ermitteln:

```
k = (a · b) / (h · (a + b))
mit h = H - lp - e
```

Bedeutungen:
- a = Raumlänge
- b = Raumbreite
- h = Lichtpunkthöhe in m
- H = Raumhöhe in m
- e = Höhe der Bewertungsebene über dem Boden
- lp = Pendellänge / Abhängung in m

Schritt 2 — Leuchtenanzahl berechnen:

```
n = (En · A · 100) / (z · Φ · ηB · M)
```

Schritt 3 — Mittlere horizontale Beleuchtungsstärke bestimmen:

```
E = (N · z · Φ · ηB · M · v) / (A · 100)
```

**Variablenbedeutungen:**
- En = Nennbeleuchtungsstärke in Lux (lx)
- A = Grundfläche des Raums in m²
- z = Anzahl der Lampen je Leuchte
- v = Verminderungsfaktor (berücksichtigt Verschmutzung und Alterung von Lampen, Leuchten und Raum)
- ηB = Beleuchtungswirkungsgrad (in %; abhängig von lichttechnischen Eigenschaften der Leuchte, Reflexionsgraden, Raumindex k)
- Φ = Lichtstrom einer Lampe (lm, gem. Datenblatt)
- E = mittlere Beleuchtungsstärke in Lux (lx)
- n = berechnete Leuchtenanzahl (Stück)
- N = gewählte oder gegebene Leuchtenanzahl (Stück)
- M = Multiplikator für ηB

**Beispiel-Raumdaten:**

| Parameter                           | Wert   | Einheit |
|-------------------------------------|--------|---------|
| Länge a                             | 45     | m       |
| Breite b                            | 16     | m       |
| Fläche A = a · b                    | 720    | m²      |
| Höhe H                              | 7      | m       |
| Abstand Bewertungsebene ü. Boden e  | 0,85   | m       |
| Pendellänge / Abhängung lp          | 1      | m       |
| Lichtpunkthöhe h = H - lp - e       | 5,15   | m       |
| Raumindex k                         | 2,3    | —       |
| Reflexionsgrade Decke/Wände/Boden   | 0,5/0,3/0,1 | —  |

**Richtwerte nach ASR 7/3 / DIN 5035 T2 (Beispiel Buchbinderarbeiten):**

| Parameter                       | Wert   | Einheit |
|---------------------------------|--------|---------|
| Nennbeleuchtungsstärke En       | 300    | lx      |
| Lichtfarbe                      | ww/nw  | —       |
| Stufe Farbwiedergabeeigenschaften | 2A   | —       |
| Güteklasse Blendungsbegrenzung  | 1      | —       |
| Verminderungsfaktor v           | 0,8    | —       |
| Gleichmäßigkeit g1 = Emin/E    | 1/1,5  | —       |

---

#### 25.10.3 Wirkungsgrade

Für die Beleuchtungsplanung nach dem Wirkungsgradverfahren ist der Beleuchtungswirkungsgrad ηB maßgebend. Er wird bestimmt durch:
- Lichttechnische Eigenschaften der Leuchten
- Abmessungen des Raums (ausgedrückt durch den Raumindex k)
- Reflexionsgrade von Decke, Wänden und Boden

---

#### 25.10.4 Richtwerte für die Beleuchtungsplanung

Für überschlägige Berechnung des Leistungsbedarfs und der Lampenanzahl:

**Tabelle: Leistungsbedarf bei Nennbeleuchtungsstärke En = 500 lx mit Leuchtstofflampen L 15 bis L 58/65**

| Raumgröße | Grundfläche (m²) | Leistungsbedarf (W/m²) |
|-----------|:----------------:|:---------------------:|
| Mittel    | 30               | 15                    |
| Groß      | 150              | 13                    |

---

### 25.11 Leuchten (Beginn)

Leuchten sind erforderlich für Befestigung und Schutz der Lampen und Zubehör. Sie lenken das Licht durch Reflektoren in die gewünschte Richtung. (Dieser Abschnitt beginnt am Ende des erfassten Textausschnitts.)
