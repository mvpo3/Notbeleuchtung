# OEVE-L_1 — Teil 0
> Quelle: OEVE-L_1 (normen) · Seiten 1-40.

ÖVE-L 1/1981 ist die österreichische Bestimmung für die **Errichtung von Starkstromfreileitungen bis 1000 V** (Niederspannungsfreileitungen), herausgegeben vom Österreichischen Verband für Elektrotechnik (ÖVE), Fachausschuss L. Sie löst die ÖVE-L 1/1970 ab (in Kraft gesetzt mit 2. Durchführungsverordnung 1981 zum Elektrotechnikgesetz). Teil 0 deckt §1–§23 ab: Geltung, Begriffe, Ausführung/Bemessung der Leiter, Isolatoren und Armaturen, sowie Führung/Anordnung der Leitungen mit allen Mindestabständen (Spannfeld, Gelände, Bäume, Verkehrsflächen, Gebäude, Antennen, Sportanlagen, Gewässer, Seilbahnen, Fernmeldeleitungen).

> Hinweis: Dies betrifft Außen-Freileitungen, nicht Gebäude-Innenelektrik — Relevanz für den ElektroPlaner gering, aber als Norm-Wissensbasis vollständig destilliert.

## Inhalt

### Geltungsbereich (§1)
- Gilt für Starkstromfreileitungen bis 1000 V.
- Gilt auch für Fernmeldeleitungen, die auf Tragwerken von Starkstromfreileitungen bis 1000 V mitgeführt werden.
- Gilt **nicht** für: alle anderen Fernmeldeleitungen, Fahrleitungen aller Art, Starkstromfreileitungen der Eisenbahnen (am Fahrleitungsgestänge mitgeführt), bahneigene Beleuchtungseinrichtungen auf Bahngrund.
- §2–§4 bleiben frei.

### Referenzierte Normen (Einleitung)
- ÖVE-Bestimmungen: OVE-E 49 (Blitzschutzanlagen), OVE-EN 1 Teil 1 (Errichtung Starkstromanlagen ~1000 V/–1500 V: Begriffe + Schutzmaßnahmen), OVE-EN 1 Teil 3 §41 (Bemessung von Leitungen/Kabeln), OVE-K 41 (Energieleitungen mit PVC-Isolierung), OVE-L 14 (Starkstromfreileitungen über 1 kV), OVE-L 31 (Prüfung Isolatoren < 1000 V), OVE-L 40 (Prüfung Armaturen).
- ÖNORMEN: B 4205 (Stahlbetonmaste), B 4605 (Stahlbau-Maste), E 3600 (Vornorm, PE-isolierte Freileitungsleiter bis 1000 V), E 4000/E 4001 (Draht/Leiterseile Aluminium + E-AlMgSi), E 4004 (Aluminium-Stahl-Seile + E-AlMgSi-Stahl-Seile), E 4006 (verzinkte Stahldrähte), E 4007 (verzinkte Stahlseile), E 4030 (techn. Lieferbedingungen Drähte/Seile), E 4100 (Stützenisolatoren Reihe N bis 1000 V), E 4105 (Schäkelisolatoren Reihe S bis 1000 V), E 4106 (Abspannisolatoren Reihe A bis 1000 V), E 4107 (Abspannisolatoren Typ E 100 mit Bügel bis 1000 V), E 4200/E 4201/E 4202 (Holzmaste).
- International: Elektrotechnikgesetz BGBl. Nr. 57/1965 (23. Stück, 6. April 1965), DIN 48200 Teil 1 (Drähte Kupfer), DIN 48201 Teil 1 (Seile Kupfer), DIN 48202 Teil 2 (Drähte/Seile Kupfer und Bronze).
- Rechtsstatus: Rechtsbelehrungen, Einleitungen, Fußnoten, Hinweise, Anhänge gelten **nicht** als Bestandteil der Bestimmungen; Vorworte und Kleingedrucktes hingegen schon.

### Begriffe und Benennungen (§5)
- **Niederspannungsfreileitungen** = Starkstromfreileitungen mit Nennspannung bis 1000 V; umfasst alle Leiter, Tragwerke samt Fundierung/Befestigung, Erdungen, Isolatoren, Armaturen.
- Drei Ausführungsformen:
  - (1) **Blanke Freileitungen.**
  - (2) **Freileitungen mit isolierten Leitern** — isolierte Leiter, aber blanke Armaturen und blanke Verbindungsteile → **nichtvollisolierte** Anlagen.
  - (3) **Isolierte Freileitungen** — isolierte Leiter nach §10.2 + vollisolierte Armaturen → **vollisolierte** Anlagen.
- **Leiter** (5.2): zwischen Tragwerken frei gespannte Seile/Drähte (ob unter Spannung oder nicht). Unterschieden: blanke Seile/Drähte; isolierte Leiter (kunststoffisolierte Leiterseile/Drähte). Isolierte Leiter weiter: selbsttragend (einadrig oder mehradrig verseilt) oder mit Tragorgan versehen.
- **Sollquerschnitt** (5.3): nach Konstruktionsdaten ermittelter Metallquerschnitt; ggf. leitender vs. nur tragender Querschnitt.
- **Nennquerschnitt** (5.4): zur Bezeichnung dienende Querschnittsangabe.
- **Mindestbruchlast** (5.5): das **0,95-fache** der rechnerischen Bruchlast.
- **Dauerzugspannung** (5.6): größte konstant gehaltene Zugspannung, die der Leiter **ein Jahr** lang aushält, ohne zu reißen.
- **Spannfeld** (5.7): Leitungsstrecke zwischen zwei aufeinanderfolgenden Tragwerken.
- **Spannweite** (5.8): waagrechte Entfernung zwischen zwei aufeinanderfolgenden Tragwerken.
- **Kreuzen** (5.9): Leiter kreuzt Objekt, wenn der Grundriss des windausgelenkten Leiters den Grundriss des Objekts schneidet.
- **Kreuzungsspannfeld** (5.10): Spannfeld, für das die Bedingung nach §5.9 zutrifft.
- **Leiterzug** (5.11): Produkt aus Sollquerschnitt des tragenden Leiters × Zugspannung in Tangentenrichtung der Durchhangskurve.
- **Durchhang** (5.12): lotrecht gemessener Abstand eines Punktes der Leiterachse von der Verbindungsgeraden der beiden Aufhängepunkte.
- **Ausgangszustand** (5.13): jener der beiden Zustände **–5 °C + Regelzusatzlast** oder **–20 °C ohne Zusatzlast**, bei dem im Scheitelpunkt der Durchhangskurve die höhere Zugspannung auftritt.
- **Ausgangszugspannung** (5.14): waagrechte Komponente der Zugspannung im Leiter beim Ausgangszustand.
- **Höchstzugspannung** (5.15): im oberen Aufhängepunkt beim Ausgangszustand auftretende Zugspannung.
- **Regelzusatzlast** (5.16): lotrecht wirkende, längs gleichmäßig verteilte Last, die alljährlich wiederkehrt.
- **Ausnahmszusatzlast** (5.17): lotrecht wirkende, längs gleichmäßig verteilte Last, die nur ausnahmsweise vorkommt.
- **Armaturen** (5.18): Bauelemente, die an Leitern, Isolatoren und zwischen Leitern/Isolatoren und Tragwerk eingebaut werden.
- §6–§9 bleiben frei.

### Ausführung der Leiter (§10)
- Nur **mehrdrähtige, verseilte Leiter**. Ausgenommen: Stahl-/Stalumdrähte bis **6 mm** Durchmesser als Tragorgane (Spanndrähte).
- Auf Beständigkeit gegen chemische Einflüsse und Korrosion achten. Leiter blank oder isoliert.

**10.1.2 Mindestquerschnitte für blanke Leiter:**
- Aluminium-Stahl-Seile und E-AlMgSi-Stahl-Seile: **35/6 mm²**
- Leiterseile aus Aluminium: **25 mm²**
- Leiterseile aus E-AlMgSi: **25 mm²**
- Leiterseile aus Kupfer: **16 mm²**
- Verzinkte Stahl-Seile: **16 mm²**
- Leiter ohne gesonderte Bestimmungen und Spanndrähte: rechnerische Bruchlast mind. **400 daN**, Querschnitt darf **16 mm²** nicht unterschreiten.
- Für Leiter, die in Tab. 10-1 nicht angeführt sind: zulässige Ausgangsspannung = **45 %** der Dauerzugspannung.

**Isolierte Leiter (10.2):** gesonderte technische Bestimmungen (OVE-K 41, ÖNORM E 3600); rechnerischer Nachweis zulässig. Für isolierte Mehraderleitungen: **Mindestquerschnitt 25 mm² Aluminium**. Bei abweichenden Ausführungen ist das spezifische Leitereigengewicht gesondert zu ermitteln.

### Mechanische und thermische Bemessung der Leiter (§11)
**Lastfälle (Tab. 11-1):**
- **Regellastfälle:** –5 °C mit Leitereigengewicht + Regelzusatzlast (zulässige Beanspruchung siehe §11.3); –20 °C mit Leitereigengewicht.
- **Ausnahmslastfall:** Leitereigengewicht + Ausnahmszusatzlast (siehe §11.4).
- Bei Mantelleitungen Bauart YMT (§10.2.3) und Bauarten mit gesondertem Spanndraht: Annahme, dass das Tragorgan allein die gesamte Last trägt.

**11.2 Höhe der Zusatzlasten (mindestens):**
- Regelzusatzlast: **(0,4 + 0,02·d) daN/m** (d = Leiterdurchmesser in mm; bei Leitungen nach §10.2 ist d die größte Abmessung der Gesamtanordnung nach Abb. 10-2).
- Ausnahmszusatzlast: **1,5 daN/m**.

**11.3 Ausgangszustand:**
- (1) Ausgangszugspannung darf den Wert nach Tab. 10-1 Spalte 6 (bzw. §10.1.3) nicht überschreiten.
- (2) Höchstzugspannung darf diesen Wert um höchstens **5 %** überschreiten.
- (11.4) Beim Ausnahmslastfall (Tab. 11-1, Zeile 5) darf die im oberen Aufhängepunkt auftretende Zugspannung die Dauerzugspannung nicht überschreiten.

**Tab. 11-2 — Zulässige Dauerstromstärken in A** (bei Luftausgangstemperatur 35 °C und Windgeschwindigkeit 0,6 m/s, bis zur zulässigen Erwärmungsgrenze):

| Nennquerschnitt mm² | Aluminium | E-AlMgSi | Stahl-IV | Kupfer | PE-isol. Freileitungsleiter E-A2Y RM |
|---|---|---|---|---|---|
| 16 | – | – | 30 | 125 | – |
| 25 | 145 | 135 | 40 | 160 | 80 |
| 35 | 180 | 170 | 50 | 200 | 100 |
| 50 | 225 | 210 | 60 | 250 | 125 |
| 70 | 270 | 255 | 70 | 310 | 160 |
| 95 | 340 | 320 | 00(?) | 380 | 185 |
| 120 | 390 | 365 | 95 | 440 | – |
| 150 | 455 | 425 | 110 | 510 | – |

Aluminium-Stahl / E-AlMgSi-Stahl (Verhältnis 6:1):

| Nennquerschnitt mm² | Alu-Stahl 6:1 | E-AlMgSi-Stahl 6:1 |
|---|---|---|
| 35/6 | 180 | 170 |
| 50/8 | 220 | 205 |
| 70/12 | 290 | 270 |
| 95/15 | 350 | 330 |
| 120/20 | 410 | 385 |
| 150/25 | 470 | 440 |

(Größere genormte Querschnitte: siehe OVE-L 11/1979 Tab. 11-2.)
- Thermische Bemessung isolierter Leiter nach §10.2.2/10.2.3: gesonderte technische Bestimmungen.

### Isolatoren (§12)
- Müssen Witterung und aggressiven Verunreinigungen widerstehen.
- Keramische Isolatoren müssen **braun glasiert** sein.
- Mechanische Nennlast ≥ **2,5-fache** der größten in den Regellastfällen (§11.1) auf den Leiter wirkenden Kraft.
- Bei gewährleistetem Mittelwert der Bruchlast nicht genormter Isolatoren: mechanische Nennlast = **80 %** des Mittelwerts der Bruchlast (wenn durch Stichprobenprüfung nachgewiesen).
- Prüfspannungen für Betriebsspannung über 500 V … 1000 V: Nenn-Steh-Kurzzeit-Wechselspannung (1 min, 50 Hz, unter Regen) mindestens; Nenn-Steh-Blitzstoßspannung mindestens (konkrete Zahlenwerte im Quelltext unleserlich/tabellarisch).

### Armaturen (§13)
- **13.1 Allgemeines:** Form/Konstruktion/Werkstoffe gegen atmosphärische Einflüsse, aggressive Verunreinigungen, elektrolytische Zerstörung widerstandsfähig. Armaturen aus nicht rostfreiem Stahl, Temper- und Stahlguss durch Feuerverzinkung o. gleichwertig gegen Rost schützen.
- **13.2 Elektrische Bemessung:** (1) Stromübergangs-Armaturen (Stromklemmen, Verbinder) dürfen beim zulässigen Dauerstrom keine höhere Temperatur als der Leiter annehmen, müssen Kurzschlussbeanspruchungen standhalten; Spannungsabfall kleiner als an gleich langem Leiterstück. (2) Armaturen in Erdschlussstrom-Ableitung für die jeweilige Stromstärke auslegen. (3) Armaturen für isolierte Freileitungen so, dass Berühren spannungführender Teile verhindert ist.
- **13.4 Grenzlasten:** (1) Bruchlast = Last beim Bruch / Unterbrechung der kraftschlüssigen Verbindung; (2) Höchstlast = Last, bei der trotz Verformung keine weitere Belastung aufgenommen wird; (3) Strecklast = Last, ab der bleibende Verformungen entstehen.
- **13.5 Sicherheiten:**
  - (1) Armaturen mit direktem Leiterkontakt unter Leiterzug (Endbund-/Abspannklemmen, zugfeste Verbinder): Bruch-/Höchstlast = **n-faches** des Leiterzuges im Ausgangszustand, mit **n = 2,0** (Aluminium), **n = 2,2** (Stahl), **n = 2,5** (E-AlMgSi, Alu-Stahl 6:1, E-AlMgSi-Stahl 6:1). Gilt für Querschnitte bis **150 mm²**. Zusätzliche Versagekriterien: Durchgleiten der Leiter, Brüche von Einzeldrähten.
  - (2) Armaturen unter indirektem Leiterzug (Bünde, Tragklemmen): müssen Leiterdifferenzzüge von mind. **5 %** des Leiterzuges aufnehmen, ohne dass der Leiter durchgleitet. Ausnahme: Rollenarmaturen als Tragklemmen für isolierte Freileitungen (wenn Durchhangsänderungen berücksichtigt).
  - (3) Armaturen mit Versagekriterium Bruch-/Höchstlast (Bügel für Abspannisolatoren, Abspannösenschrauben): Sicherheit bezogen auf Bruch-/Höchstlast ≥ **2,5**, dazu Sicherheit gegen Strecklast ≥ **1,5**.
  - (4) Armaturen, bei denen Verformung maßgebend (Isolatorenstützen, Bolzen, Abspanngelenke): Sicherheit bezogen auf Strecklast ≥ **1,5**.
  - (5) Zugentlastete Verbinder, Stromklemmen, schwingungsdämpfende Armaturen brauchen nicht nach (1)–(4) bemessen werden. Stromklemmen auf unter Zug stehenden blanken/abisolierten Leitern: dürfen Bruchlast (Mindestbruchlast) um höchstens **5 %** vermindern; bei isolationsdurchdringenden Kontaktstücken Verminderung von **20 %** zulässig.
- §14–§19 bleiben frei.

### Führung und Anordnung der Leitungen — Grundsätzliches (§20)
- §21-Abstände gelten als Erfüllung des Berührungsschutzes; §22 für Geländeabstände, §23 für Objektabstände.
- Spalte „blank" gilt für Leitungen nach §5.1(1); Spalte „isoliert" für §5.1(2) und §5.1(3). Im Bereich blanker Armaturen von §5.1(2)-Leitungen sind die „blank"-Abstände anzuwenden.
- **20.3:** Abstände für isolierte Leiter gelten auch für spannungsfreie blanke Leiter. **Neutral- und PEN-Leiter (Nullleiter) gelten NICHT als spannungsfreie Leiter.**
- **20.4:** In Kreuzungsfeldern (§23.9/.12/.15/.16/.19/.20) je Leiter höchstens **ein** unter Zug stehender Verbinder zulässig (Ausnahmen nur vorübergehend bei Störungsbehebung).
- Messregeln: Geländeabstände rechtwinkelig zur Geländeoberfläche; waagrechte Objektabstände zwischen Leitergrundriss und nächstgelegenem Objektteil bei Windauslenkung in ungünstige Richtung; lotrechte Objektabstände vom nicht ausgelenkten Leiter.

### Abstand im Spannfeld und am Tragwerk (§21)
- Mindestabstand in Spannfeldmitte zwischen blanken, nicht ausgelenkten Leitern: **D = k·√f** (Formel). Mindestwerte:
  - Leiter übereinander angeordnet: **0,3 m**
  - Leiter nebeneinander oder schräg zueinander: **0,2 m**
  - (D = Leiterabstand in m, f = Durchhang in Spannfeldmitte in m, k = Faktor)
- **Faktor k bei Spannweiten bis 70 m** (alle Werkstoffe/Querschnitte): übereinander **0,7**; schräg (mind. 0,1 m waagrechte Versetzung) **0,5**; nebeneinander (höchstens 0,1 m lotrechte Versetzung) **0,4**. Über 70 m: Tab. 21-1 (abhängig vom Auslenkwinkel bei Wind nach §30.3).
- **21.2 Zwischen isolierten Leitern nach §10.2** auf gemeinsamen Tragwerken (Spannfeldmitte): bis 70 m alle Anordnungen **0,2 m**; über 70 m übereinander/schräg **0,3 m**, nebeneinander **0,2 m**.
- **21.3 Zwischen blanken und isolierten Leitern** auf gemeinsamen Tragwerken: bis 70 m übereinander/schräg **0,3 m**, nebeneinander **0,2 m**; über 70 m übereinander/schräg **0,5 m**, nebeneinander **0,3 m**.
- **21.4 Am Tragwerk:** Abstand blanker Leiter voneinander und von Tragwerksteilen ≥ **8 mm** (bei Betriebsspannung bis 500 V), ≥ **18 mm** (über 500 V). Bei isolierten Leitungen Abstände so wählen, dass mechanische Beschädigung der Isolation (z. B. Scheuern) vermieden wird.

### Abstand vom Gelände und von Bäumen/Sträuchern (§22)
**22.1 Geländeoberfläche** (rechtwinkelig gemessen; Angaben blank / isoliert in m):
- von normalem Gelände: **5 / 5**
- von Steilgelände (normalerweise nicht begangen): **3 / 3**
- von Felswänden: **0,3 / 0,3**
- von Geländeoberfläche bei nicht unterfahrbaren Hausanschlussleitungen: **4 / 4**

**22.2 Bäume und Sträucher** (allseitiger Abstand; blank / isoliert in m):
- in Waldbeständen: **1,5 / 0,5** (Werte aus Tab.; blank 1,5)
- in Hausgärten, Obstkulturen, Parkanlagen, einzelstehende Bäume/Sträucher: **1 / 0,5** (entspr. Tabelle)

### Leitungsführung im Bereich von Objekten (§23)
Werte jeweils **blank / isoliert** in m.

**23.1 Verkehrsflächen:**
- (1) Bundesstraßen S, Bundesstraßen B, Landes-/Gemeindestraßen, sonstige Fahrwege außerhalb Ortsgebiet: lotrechter Abstand von der Fahrbahn **5,5 / 5,5**; waagrechter Abstand vom Rand Fahrbahn/Bankette/Gehsteig **5,5 / 5,5** (bzw. 0,3 in Teilfällen); waagrechter Abstand Tragwerke an Erdeintrittsstelle vom Fahrbahnrand im Freiland.
- (2) Verkehrsflächen innerhalb Ortsgebieten/industriell/gewerblich/öffentliche Gartenanlagen: lotrechter Abstand **5,5 / 5,5**.

**23.2 Bundesstraßen A (Autobahnen):** **Überkreuzung unzulässig.** Waagrechter Abstand der Leiter vom Fahrbahnrand **4 / 4**; der Tragwerke **5 / 5**. Diese gelten, sofern Unterschreitung der **Bauverbotszone von 40 m** von der Bundesstraßenbehörde genehmigt wird.

**23.3 Brücken:**
- (1.1) lotrechter Abstand von Bauwerksteilen bei Führung auf eigenen Tragwerken: **1,5 / 0,1**
- (1.2) bei Befestigung der Leiter an der Brücke: **0,5 / 0,1**
- (1.3) oberhalb blanker Leiter, die in lotrechtem Abstand < 1,5 m Verkehrsflächen/Gehsteige/Standflächen kreuzen: **1,5 m auskragendes** und Leiter seitlich **1,5 m überragendes Schutzdach** anzubringen.

**23.4 Gebäude, Bauwerke, Bauwerksteile** (Auswahl, blank / isoliert in m):
- (1.1) lotrecht vom Dachfirst, nicht begehbaren Mauerkronen, Einfriedungen: **0,5 / 0,1**
- (1.2) von Balkonen/Terrassen/Bedienungsstegen/Standflächen, Flachdächern/Dachflächen < 20° Neigung, nach oben: **2,5 / 0,5** (Werte gemäß Tabelle; nach oben höhere Werte)
- (1.3) Flachdächer < 20°, nur bei Instandhaltung begangen, nach oben: geringer
- (1.4) nach unten: (1.4.1) außerhalb bis 0,3 m innerhalb gedachter Lotfläche **0,5 / 0,3**; (1.4.2) mehr als 0,3 m innerhalb: **0,3 / 0,1**
- (1.6) über Dachausstiegsluken + 0,3 m erweiterter Bereich
- (1.7/1.8/1.9) Schornsteine: von außen gereinigt nach oben **2,5 / 1,25**; nur von innen gereinigt; mit korrosionsbeständiger Abdeckung
- (1.10) Fensteröffnungen nach oben / nach unten
- (1.11) über Einfahrten bei Wandbefestigung
- (1.12) von Untersichtfläche Dachtraufen/Erker/vorspringenden Gebäudeteilen nach unten: **0,1**
- (2) rechtwinkliger Abstand zu Dachflächen > 20° Neigung
- (3) waagrechte Abstände: (3.1) von Balkonen/Terrassen/Standflächen/Flachdächern/vor Fensteröffnungen **1,5 / 1**; (3.2.1) unterhalb 0,5 m unter tiefstem Rauchaustritt **1 / 0,3**; (3.2.2) oberhalb **1 / 1**; (3.3) von Fensteröffnungen/Einfahrten nach der Seite **1,25 / 0,5**; (3.4) von Gebäuden/Bauwerken/Bauwerksteilen **0,1 / 0,1**.
- Hinweis Feuer-/Explosionsgefahr, Arbeitsraum von Verladeeinrichtungen/Kränen in industriellen/gewerblichen sowie land-/forstwirtschaftlichen Betrieben.

**23.5 Blitzschutzanlagen:** allseitiger Abstand **0,4 / 0,4 m**. Reduzierbar auf **0,1 m**, wenn die Leiter im Annäherungsbereich (bis 0,4 m) eine Isolierung für mind. **100 kV Durchschlagsspannung** aufweisen oder eine Verbindung mit der Blitzschutzanlage über Überspannungsableiter besteht.

**23.6 Außenantennenanlagen:**
- (1.1) lotrecht von Antennen, Bauteilen, nicht besteigbaren Tragwerken/Verankerungen: **1 / 0,3**
- (1.2) von besteigbaren Antennentragwerken: **1,5 / 0,3**
- (2.1) waagrecht von Antennen/Bauteilen/nicht besteigbaren Tragwerken: **1 / 0,3**
- (2.2) von besteigbaren Antennentragwerken: **1,5 / 0,5**
- Zuspannung einer isolierten NS-Freileitung an Antennentragwerken für Eigenversorgung der Antennenanlage zulässig.

**23.7 Sportanlagen:** Schießstätten nur außerhalb des Streubereichs (Blendöffnung) kreuzbar; Schisprunganlagen (Absprung→Aufsprung) und Flächen mit leitungsgefährdenden Sportgeräten (große/harte Bälle, Diskus, Speer, Hammer) **unzulässig** zu kreuzen.
- (1) bodengebundene Sportarten / Ballspiele mit kleinen, leichten, weichen Bällen (Laufen, Weitsprung, Eisstockschießen, Tennis): **6 / 6**
- (2) öffentliche Schwimmbadanlagen und Campingplätze: **6 / 6**

**23.8 Starkstromfreileitungen:**
- (1) Überkreuzen einer Starkstromfreileitung über 1 kV durch eine NS-Freileitung **unzulässig**.
- (2) Beim Unterkreuzen einer >1 kV-Leitung: diese nach gesonderten Bestimmungen ausführen, Kreuzung möglichst nahe einem Tragwerk, Abstände nach gesonderten Bestimmungen (OVE-L 11/1979).
- (4) waagrechter Abstand der Leiter von Tragwerken von >1 kV-Freileitungen: **1,5 / 1**
- (5) Kreuzung zweier NS-Freileitungen, lotrechte Abstände: (5.1.1) blanke Leiter auf beiden **1 / –**; (5.1.2) isolierte Leiter auf beiden oder einer Leitung **0,3 / 0,3**; (5.2) zwischen Leitern einer und Tragwerken der anderen **1,5 / 0,5**.
- (6) Parallelführung/Näherung auf getrenntem Gestänge, waagrechte Abstände: (6.1.1) blanke auf beiden **1,5 / –**; (6.1.2) isolierte auf beiden/einer **0,3 / 0,3**; (6.2) zwischen ausgelenkten Leitern und Tragwerken der anderen **1,5 / 0,5**.
- (7) allseitiger Abstand von ausgelenkten Leitern zu freistehenden Beleuchtungsanlagen: **1,5 / 0,5**.
- (8) Führung einer NS-Freileitung auf dem Gestänge einer >1 kV-Leitung nur bei Gruppe I zulässig: (8.1) bei Abschaltung der >1 kV-Leitung muss NS-Leitung zwangsläufig spannungslos werden; (8.2) NS-Leitung unterhalb anzuordnen; (8.3) >1 kV-Leitung mit erhöhter Sicherheit auszuführen; (8.4) auch bei isolierten Leitern gleiche Abstände wie für blanke.

**23.9 Oberirdische Fernmeldeleitungen** (blank / isoliert in m):
- (1.1.1) lotrecht von blanken FM-Leitern: **1 / 0,5**; (1.1.2) von isolierten FM-Leitern: **0,5 / 0,5**
- (1.2) von Stützpunkten der FM-Leitung: **1,5 / 0,75**
- (2.1) waagrecht von blanken FM-Leitern: **1 / 0,5**; (2.2) von isolierten FM-Leitern: **0,5 / 0,5**; (2.3) von Stützpunkten: **1,5 / 1**
- (3) waagrechter Abstand Tragwerke von FM-Leitern: **1 / 1**
- Unterkreuzen einer FM-Leitung nur zulässig, wenn im Kreuzungsspannfeld mind. eine der beiden Leitungen isoliert ist.

**23.10 Fernmeldekabel:** (1) Fundamente/Ausschachtung seitlich der Kabel **0,8 m**; (2) bei allseitigem mechanischem nichtmetallischem Schutz **0,3 m**. Bei Gefährdung durch Erder-/Blitzeinwirkung, Koaxialkabel, FM-Kabel gleicher Bedeutung, Spleißgruben → ggf. größere Abstände/Schutzmaßnahmen (Zustimmung Fernmeldebehörde).

**23.11 Gewässer** (ausgenommen Wasserstraßen §23.12; blank / isoliert in m):
- (1.1) lotrecht über Mittelwasser nicht schiffbarer Gewässer: **4 / 4**
- (1.2.1) über Mittelwasser schiffbarer Gewässer: **5 / 5**
- (1.2.2) über höchsten Bauteilen der Wasserfahrzeuge bei HSW: **5,5 / 5,5**
- (1.3) über Hochwasserschutzdämmen: **1,5 / 1,5**
- (2) waagrecht vom Ufergrat/Krone der HW-Schutzdämme: **3 / 3**
- (3) waagrecht Tragwerke seitlich vom Ufergrat/Fuß landseitiger Berme: (Unterschreitung an Zustimmung der Gewässeraufsichtsbehörde gebunden).

**23.12 Wasserstraßen** (blank / isoliert in m):
- (1.1) lotrecht über HSW: **19 / 19**
- (1.2) über Krone der HW-Schutzdämme: **5,5 / 5,5**
- (2) waagrecht vom Ufergrat/Krone: **4 / 4**
- (3) waagrecht Fundamente vom Ufergrat/Fuß landseitiger Berme: **3 / 3** (sofern nicht größerer Abstand von Wasserstraßenverwaltung vorgeschrieben).

**23.13 Ortsveränderliche Bodenseilzüge:** Unterkreuzen **unzulässig**. Beim unvermeidbaren Überkreuzen: Maßnahmen gegen Berühren spannungführender Leiter (Anordnung der Leiter gegen Abheben/Hochschnellen, Prellseil parallel unterhalb, Fangjoche/Führungs-/Niederhalterollen). Prellseil muss nicht geerdet sein; nicht geerdetes Prellseil zu Bodenverankerung → nach §40.5 ausführen.

**23.14 Materialseilbahnen ohne beschränkt öffentlichen Verkehr (gewerblich/industriell/land-/forstwirtschaftliche Seilwege)** (blank / isoliert in m):
- (1.1.1) Unterkreuzung mit offener Zugseilführung: Schutzgerüst mit Seilfangvorrichtung; Abstand des Schutzgerüstes vom obersten Leiter bei –20 °C: **1 / 0,3**
- (1.1.2) bei geschlossener Zugseilführung kein Schutzgerüst; Abstand der Leiter bei –20 °C zu Bauteilen in ungünstigster Betriebslage: **2 / 1**
- (2.1.1) Überkreuzung, lotrecht vom Seil, wenn Seilbahntragseile mit PEN-Leiter verbunden (nur bei Nullung): **1 / 1**
- (2.1.2) in allen anderen Fällen: **2 / 1**
- (2.2) lotrecht von anderen Bauteilen: **1,5 / 1,5**
- (3.1) waagrecht zum Seil/Fahrbetriebsmitteln (windausgelenkt): **1 / 0,5**
- (3.2) zu anderen Bauteilen: **1,5 / 1**
- (4) waagrecht Tragwerke vom ausgelenkten Seil/Fahrbetriebsmitteln/Bauteilen: **1,5 / 1,5**

**23.15 Standseilbahnen für Güterbeförderung** (Schrägaufzüge, Bremsberge, Haspelberge; blank / isoliert in m):
- (1) lotrecht vom Lichtraumprofil und Zugseil in höchstmöglicher Lage: **1,5 / 0,5**
- (2) waagrecht vom Lichtraumprofil: **1,5 / 0,3**
- (3) waagrecht Tragwerke vom Lichtraumprofil: **1,5 / 1,5**

**23.16 Seilliftanlagen zur öffentlichen Personenbeförderung (Schlepplifte, Sessellifte, Sesselbahnen):** Unterkreuzung **unzulässig**. (blank / isoliert in m):
- (1) lotrecht vom Seil/Bauteilen: **1,5 / 0,5**
- (2) waagrecht zwischen Leitern und Seil/Fahrbetriebsmittel (windausgelenkt): **2 / 1**
- (3.1) waagrecht Tragwerke von ausgelenkten Seilen/Fahrbetriebsmitteln (Bauverbotsbereich **12 m**, Genehmigung Eisenbahnaufsichtsbehörde): **3 / 3**
- (3.2) vom Rand der Fahrbahn bei Schleppliften: **3 / 3**

**23.17 Seilschwebebahnen und Materialseilbahnen mit beschränkt öffentlichem Verkehr:** Kreuzung **unzulässig**. (blank / isoliert in m):
- (1) waagrecht vom nächstgelegenen Bauteil (Seil/Fahrbetriebsmittel, windausgelenkt): **2 / 1**
- (2) waagrecht Tragwerke von Bauteilen (Bauverbotsbereich **12 m**): **5 / 5**

**23.18 Standseilbahnen zur Personenbeförderung:** Kreuzung **unzulässig**, ausgenommen im Bereich von Tunneln/festen Überbauungen. (blank / isoliert in m):
- (1) waagrecht vom Lichtraumprofil: **2 / 1**
- (2) waagrecht Tragwerke vom Lichtraumprofil (Bauverbotsbereich **12 m**): **5 / 5**

**23.19 Straßenbahnen, Obuslinien, Materialseilbahnen, elektrische Treidelanlagen** (blank / isoliert in m):
- (1.1) lotrecht von Fahrleitungen: **2 / 2**
- (1.2) von Tragwerken der Fahrleitungen: **1,5 / –**
- (1.3) vom Lichtraumprofil: **2 / 1**
- (1.4) von Schienenoberkante (wenn keine Fahr-/Speiseleitung auf Fahrleitungstragwerken): **5,5 / 5,5**
- (1.5) von Speiseleitungen: es gelten die Bestimmungen nach §23.8.

> Teil 0 endet auf Seite 40 mitten in §23.19; §23.20 ff. und die folgenden Paragraphen (Tragwerke §30 ff., Fundierung, Erdungen §60, Fernmeldeleitungen §70, Anhang/Sachverzeichnis) folgen in Teil 1.
