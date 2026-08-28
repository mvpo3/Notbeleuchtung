# Lehrbuch der Bauphysik — Teil 8
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 321-360.

Dieser Teil behandelt bauphysikalische Feuchtemechanismen: Wasserverdunstung von Wasseroberflächen (Kap. 12, Abschluss), stationären Feuchtetransport in mehrschichtigen Bauteilen inklusive des Glaser-Verfahrens (Kap. 13, vollständig), und den Flüssigwassertransport bei einseitiger Wasserbelastung. Kernthema ist der Nachweis von Tauwasserausfall im Bauteilinneren sowie Maßnahmen zu seiner Vermeidung.

## Inhalt

### 12.3 Wasserverdunstung von Wasseroberflächen (Abschluss)

- Tauen (Kondensieren) ist die Umkehrung von Wasserverdunstung — alle Gesetzmäßigkeiten gelten für beide Richtungen.
- Für ruhende Freiwasser-Oberflächen im Freien (nach Sprenger): Massenstromdichte g proportional zu Luftgeschwindigkeit v und Dampfdruckdifferenz Δp. Zahlenwertgleichung (Gl. 12.11): g [kg/(m²·h)] = 16 · (12 + v [m/s]) · Δp [Pa] · 10⁻⁴. Bei der Wasseroberfläche gilt naturgemäß φ = 1.
- Hallenbäder (nicht genutzt) verdunsten deutlich weniger als Freibäder oder natürliche Gewässer.
- Biasin und Krumme unterscheiden nach Verhältnis von Lufttemperatur θL zu Wassertemperatur θW:
  - θL > θW: g = (0,055 + 1,0 · 10⁻⁴) · Δp [Pa]
  - θL < θW: g = (0,055 + 0,8 · 10⁻⁴) · Δp [Pa]
  - θL = θW: g = (0,055 + 0,7 · 10⁻⁴) · Δp [Pa]
  - Einheit jeweils kg/(m²·h) (Gl. 12.12).
- Im benutzten Hallenbad (nach Kappler) hängt die Verdunstung von Personendichte pX [m⁻²] und Luftgeschwindigkeit v [m/s] ab: g = (0,12 + 8,9 · 10⁻⁴ · pX) · v · Δp · 10⁻⁴ · [kg/(m²·h)] (Gl. 12.13).
  - Verdunstung setzt erst ein, wenn Δp einen Schwellwert überschreitet (Grenzschicht im Becken).
  - Bei kleiner werdender Lufttemperatur im Verhältnis zur Wassertemperatur steigt die Massenstromdichte durch zunehmende Konvektion.
  - Zulässige Besucherzahlen: 0,3 m⁻² als Maximum, 0,15 m⁻² als gute Belegung.
  - Gl. 12.13 gilt nur für Nutzungszeiten; in der übrigen Tageszeit Berechnung nach Gl. 12.12.
  - Voraussetzung: Lüftung bläst Wasseroberfläche nicht an.

---

### Kapitel 13: Stationärer Feuchtetransport in Bauteilen

#### 13.1 sd-Werte zusammengesetzter Schichten

**Reihenschaltung (Schichten hintereinander, senkrecht zum Diffusionsstrom):**
- Bei stationärer Diffusion ist die Massestromdichte in allen Einzelschichten identisch; andernfalls würde sich Wasser anreichern oder abreichern (Widerspruch zur Stationarität).
- Konsequenz (Gl. 13.1): Das Verhältnis Δpi/sdi ist in jeder Schicht gleich groß — im sd-verzerrten Querschnitt verläuft der Partialdruck linear als gerade Linie, nicht als Knickzug.
- Additionsregel (Gl. 13.2): sd,ges = Σ sdi — äquivalente Luftschichtdicken hintereinanderliegender Schichten addieren sich.
- Transportgesetz bei mehrschichtigen Bauteilen, stationär (Gl. 13.3): g = δ · Δp / Σdi mit δ = 1,5 · 10⁻⁶ [kg/(m·s·Pa)]⁻¹.
- Mit Stoffübergang (Luftgrenzschichten) an beiden Seiten (Gl. 13.4): Nenner erweitert um 1/βp,a und 1/βp,i — vollständig analog zum Wärmedurchgangswiderstand RT = 1/U.

**Parallelschaltung (Teilflächen nebeneinander, unterschiedliche sd-Werte):**
- Mittlere äquivalente Luftschichtdicke sd der Gesamtfläche A aus n Teilflächen Ai mit sdi:
  - sd = A / Σ(Ai/sdi) (Gl. 13.9).
  - Herleitung: Gesamtdiffusionsstrom = Summe Teilströme; derjenige sd-Wert, der denselben Strom erzeugt, ist der harmonische Flächenmittelwert.

**Profilierte Schichten:**
- Schichten mit profilierter (unebener) Oberfläche sind durchlässiger als planparallele mit gleicher mittlerer Dicke, weil Dünnstellen überproportional mehr Strom durchlassen.
- Beispiel Rechteckprofil mit ±50 % Dickenabweichung vom Mittelwert:
  - Dünnstelle: 200 % Stromdichte des ebenen Referenzwertes
  - Dickstelle: 67 % Stromdichte
  - Summe: 267 %, Mittelwert: 133 % → effektive Diffusionswiderstandszahl reduziert auf 75 % des Mittelwerts (Punkt A in Abb. 13.3).

---

#### 13.2 Das Glaser-Verfahren

##### 13.2.1 Beschreibung des Verfahrens

- Das Glaser-Verfahren ist ein halbgraphisches Berechnungsverfahren zur Beurteilung, ob in einem Bauteil infolge Wasserdampfdiffusion Tauwasser zu erwarten ist.
- Entwickelt von Glaser 1959, genormt 1981 in DIN 4108; weiterentwickelt in DIN 4108-3.
- Grundprinzip: Bei stationärer Diffusion verläuft der Wasserdampfpartialdruck im sd-verzerrten Querschnitt linear. Sattdampfdruckverlauf psat ergibt sich aus Temperaturprofil. Tauwasser fällt aus, wo Dampfdruck psat überschreiten würde.

**Schritt a — Vorbereitende tabellarische Berechnung (Tab. 13.1):**
- Schichten inkl. Luftgrenzschichten tabellarisch auflisten.
- Spalten: d [m], μ [–], sd [m], d/sd,T [–], λ [W/(m·K)], R/Rsi/Rse [m²·K/W], θ [°C], psat [Pa].
- Wärmeübergangswiderstände: innen Rsi = 0,25 m²·K/W; außen Rse = 0,04 m²·K/W.
- Temperaturdifferenz je Schicht: Δθ = q · R, mit q = (θi − θe)/RT [W/m²] (Gl. 13.10/13.11).
- Aus Temperatur an jeder Schichtgrenze → psat aus Sattdampfdrucktabelle (Tab. 10.2) ablesen.

**Klimarandbedingungen (Tab. 13.2):**

| Periode | Seite | θ [°C] | φ [%] | p [Pa] | Dauer |
|---------|-------|--------|-------|--------|-------|
| Tauperiode (Dez–Feb) | innen | 20 | 50 | 1168 | 90 d / 7776·10³ s |
| Tauperiode | außen | −5 | 80 | 321 | — |
| Verdunstungsperiode (Jun–Aug) | innen | — | — | 1200 | 90 d / 7776·10³ s |
| Verdunstungsperiode | außen | — | — | 1200 | — |

Sättigungsdruck an Tauwasserebene:
- Wände und Decken (gegen Außenluft): psat,c = 1700 Pa
- Dächer (gegen Außenluft): psat,c = 2000 Pa

**Schritt b — Glaser-Diagramm (Tauperiode):**
- Achsensystem: x-Achse = sd-Werte der Schichten, y-Achse = p und psat.
- Verlauf psat aus Tabelle in Diagramm übertragen; Schichtgrenzen linear verbinden (bei ΔT > 10 K auch Zwischenpunkte).
- Dampfdruckverlauf p: lineare Verbindung von pi zu pe (Oberflächenwerte).
  - Schneidet p-Linie den psat-Polygonzug nicht → kein Tauwasserausfall.
  - Schneidet sie ihn → Seilregel anwenden: pi und pe als Seilrollen, psat-Profil als untere Hindernisskante. Seil stramm ziehen → Verlauf des Dampfdrucks. Berührungspunkte = Tauwasserebenen.

**Schritt c — Berechnung Tauwassermasse Mc und Verdunstungsmasse Mev:**

*Fall b: Tauwasserausfall in einer Ebene (Gl. 13.12–13.15):*
- gc = δ · [(pi − p0c)/sdc,i + (p0c − pe)/(sd,T − sdc,i)] — Nettostromdichte zur Tauwasserebene.
- Mc = gc · tc
- Für Verdunstungsperiode (Abb. 13.7): gev analog mit psat,c = 1700 bzw. 2000 Pa, p außen/innen = 1200 Pa.
- Mev = gev · tev

*Fall c: Tauwasserausfall in zwei Ebenen (Gl. 13.16–13.33):*
- Zwei separate Tauwasserebenen c1 und c2.
- Für jede Ebene separater gc1/gc2 und Mc1/Mc2; Gesamtmasse Mc = Mc1 + Mc2 (Gl. 13.20).
- In der Verdunstungsperiode: gev1/gev2 für jede Ebene berechnen; Verdunstungszeiten tev1/tev2 ermitteln.
- Je nach Verhältnis tev1 zu tev2 unterschiedliche Rechenformeln (Gl. 13.25–13.33).

*Fall d: Tauwasserausfall in einem Bereich (Gl. 13.34–13.38):*
- Tauwasser fällt in einem ausgedehnten Bereich zwischen sd,c1 und sd,c2 aus.
- gc mit gemitteltem sd,c,m = 0,5·(sd,c1 + sd,c2) für die Verdunstungsrechnung.

**Alternative Normberechnung DIN EN ISO 13788:**
- Monatsweise Berechnung statt vereinfachter Tau-/Verdunstungsperiode.
- Akkumulierte Tauwassermasse am Ende der Kondensationsmonate mit Verdunstungsmenge in restlichen Monaten verglichen.

---

##### 13.2.2 Wahl der Randbedingungen

**Drei Situationen:**
- a) Bekannte und bewährte Bauweise: Kein rechnerischer Nachweis erforderlich, wenn keine Tauwasserbildung erfahrungsgemäß auftritt, Gebäude nicht klimatisiert, Wohn-/Büroklima (ca. 20 °C, 50 % r.L.), Lage in Deutschland. Praktische Bewährung hat Vorrang.
- b) Bauteil erfüllt Klimabedingungen, aber nicht in der Aufzählung von DIN 4108-3 enthalten und nicht erfahrungsgemäß unbedenklich → Glaser-Verfahren mit Normbedingungen anwenden.
- c) Tauperiode rechnen. Kein Tauwasser → unbedenklich. Tauwasser → noch unbedenklich, wenn alle folgenden Bedingungen erfüllt (DIN 4108-3, Nr. 4.2.1):
  1. In der Verdunstungsperiode trocknet das ausgefallene Wasser vollständig wieder aus.
  2. Baustoffe in Kontakt mit Tauwasser werden nicht geschädigt (Korrosion, Pilzbefall usw.).
  3. Grenzwerte für Tauwassermasse Mc:
     - Allgemein: Mc ≤ 1,0 kg/m²
     - An Grenzflächen nicht kapillar saugender Schichten (Metalle, Folien, Normalbeton, Schaumkunststoffe, Mineralwolle, Baustoffe mit Ww < 0,5 kg/(m²·h0,5)): Mc ≤ 0,5 kg/m²
     - Holz: massebezogener Feuchtegehalt u darf um max. 5 % zunehmen
     - Holzwerkstoffe (außer Holzwolleleichtbauplatten DIN EN 13168 und Mehrschichtleichtbauplatten): u-Zunahme max. 3 %
  4. Zusatz für Holzkonstruktionen (DIN 68800-2): Für allseitig geschlossene Bauteile rechnerische Trocknungsreserve von ≥ 250 g/m² nach DIN 4108-3 oder DIN EN 15026 nachzuweisen.

**Sonderfall c — abweichende Klimabedingungen:**
- Hochgebirgslage, Hallenbad, klimatisierte Gebäude → genormte Randbedingungen nicht anwendbar.
- Methode Jenisch: Vom Jahresmittel der Außenluft ausgehend Kondensations-Austrocknungsbilanz prüfen; Außentemperatur bestimmen, ab der Kondensat entsteht; aus Tabelle für 7 Städte (Braunschweig, Bremen, Clausthal, Hamburg, Karlsruhe, München, Münster) Tauperiodendauer und mittlere Temperatur ablesen → Glaserdiagramm für Tauperioden-Mitteltemperatur.
- Einfachere Alternative: Monatsweise Glaser-Berechnung mit tatsächlichen Monatsmittelwerten.

**Grenzen des Glaser-Verfahrens:**
- Nur stationäre Verhältnisse (exakt gegeben z.B. bei Trennwand zwischen Räumen konstanter, unterschiedlicher Klimata).
- Für veränderliches Außenklima: nur mit Normbedingungen und Bewertungskriterien DIN 4108-3 verwenden.
- Nicht berücksichtigt:
  - Erhöhter Feuchtetransport bei größerer Baustofffeuchte (kapillarer Transport)
  - Feuchtespeicherfähigkeit der Baustoffe
  - Realistische Jahresklimaverläufe (vereinfacht und verschärft)
- Konservative Seite: Bei Unbedenklichkeit nach Glaser ist Bauteil immer auch praktisch unbedenklich. Bei Bedenklichkeit nach Glaser kann es bedenklich sein, muss es aber nicht.
- Nicht anwendbar: begrünte Dachkonstruktionen, Berechnung natürlichen Austrocknungsverhaltens.

---

##### 13.2.3 Beispiele typischer Glaser-Diagramme

**Einfluss der Dämmstofflage (Abb. 13.8):**
- Wandaufbau A (homogen): psat-Verlauf gleichmäßig.
- Wandaufbau B (Dämmung innenseitig): psat bildet nach unten gerichtete Spitze → ungünstig; gefährlicher, je kleiner sd des Wandbildners innen und je größer Wärmedurchlasswiderstand der Dämmung.
- Wandaufbau C (Dämmung außenseitig): psat-Werte im Wandquerschnitt relativ hoch → günstig.
- Wandaufbau D (Kerndämmung): Intermediäre Situation.

**Einfluss von Dampfsperren (Abb. 13.9):**
- Im Glaserdiagramm wirkt eine Dampfsperre als unendlich breite Schicht (sd → ∞); dargestellt durch Herausschneiden aus dem Diagramm.
- Wandaufbau A (Dampfsperre raumseitig): pe pflanzt sich horizontal ins Bauteil fort; pi kann nicht wirken → tauwasserfrei.
- Wandaufbau B (Dampfsperre außenseitig): pe kann nicht ins Bauteil eindringen; pi trifft in spitzem Winkel auf psat an der Innenseite der Dampfsperre → Tauwasserausfall dort.
- Wandaufbau C (beidseitige Dampfsperren): Dampfdrücke beider Seiten ohne Einfluss; horizontaler Dampfdruckverlauf im Inneren, dessen Niveau vom Feuchtegehalt des eingeschlossenen Baustoffs vor dem Einbau bestimmt wird.

---

##### 13.2.4 Unbedenkliche Bauteile (kein rechnerischer Nachweis nötig)

Voraussetzungen: Mindestwärmeschutz, luftdichte Ausführung, Klimarandbedingungen nach 13.2.1.

**Wände aus Mauerwerk (DIN EN 1996-1-1), Normalbeton (DIN EN 206-1/DIN 1045-2), gefügedichtem Leichtbeton (DIN 1045-2, EN 206, EN 1992-1-1), haufwerksporigem Leichtbeton (DIN 4213, EN 992, EN 1520) — jeweils mit Innenputz und folgenden Außenschichten:**
- Wasserabweisender Außenputz (Tab. 16.22)
- Außendämmungen (DIN 4108-10) oder wasserabweisender Wärmedämmputz oder genormtes WDVS (DIN EN 13499/13500)
- Verblendmauerwerk (DIN EN 1996-1-1)
- Angemörtelte Außenwandbekleidungen (DIN 18515-1), Fugenanteil ≥ 5 %
- Hinterlüftete Außenwandbekleidungen (DIN 18516-1), mit und ohne Wärmedämmung
- Einseitig belüftete Außenwandbekleidungen mit Lüftungsöffnung ≥ 100 cm²/m
- Kleinformatige luftdurchlässige Außenwandbekleidungen, mit und ohne Belüftung

**Wände mit Innendämmung:**
- Wie oben, jedoch ohne Schlagregenbeanspruchung
- Innendämmung R ≤ 0,5 m²·K/W → kein Nachweis
- Falls 0,5 m²·K/W < R ≤ 1 m²·K/W: sd,i ≥ 0,5 m der Innendämmung einschließlich raumseitiger Bekleidung

**Wände in Holzbauart (DIN 68800-2):**
- Beidseitig bekleidete/beplankte Wände mit vorgehängten Außenwandbekleidungen, raumseitig sd,i ≥ 2 m, außenseitig sd,e ≤ 0,3 m oder Holzfaserdämmplatte (DIN EN 13171); gilt auch für nicht belüftete kleinformatige Außenbekleidungen mit zusätzlicher wasserableitender Schicht sd,e ≤ 0,3 m.
- Raumseitig bekleidete/beplankte Wände mit sd,i ≥ 2 m und WDVS aus mineralischem Faserdämmstoff (DIN EN 13162) oder Holzfaserdämmplatten (DIN EN 13171) und wasserabweisendem Putzsystem sd ≤ 0,7 m.
- Beidseitig bekleidet mit sd,i ≥ 2 m, äußere Beplankung sd ≤ 0,3 m, WDVS aus mineralischem Faserdämmstoff (DIN EN 13162) oder Holzfaserdämmplatten (DIN EN 13171), wasserabweisendes Putzsystem sd ≤ 0,7 m.
- Beidseitig bekleidet mit WDVS aus Polystyrol oder Mauerwerks-Vorsatzschalen (DIN 68800-2).
- Massivholzbauart mit vorgehängten Außenwandbekleidungen oder WDVS (DIN 68800-2).

**Holzfachwerkwände** (mit raumseitiger Luftdichtheitsschicht):
- Wärmedämmende Ausfachung (Sichtfachwerk) + Innenbekleidung: 1 m ≤ sd,i ≤ 2 m
- Innendämmung ohne Schlagregenbeanspruchung: R ≤ 0,5 m²·K/W; falls 0,5 < R ≤ 1 m²·K/W: 1 m ≤ sd,i ≤ 2 m
- Außendämmung als genormtes WDVS oder Wärmedämmputz, äußere Schichten sd,e ≤ 2 m, oder hinterlüftete Außenwandbekleidung

**Erdberührte Kelleraußenwände:** Einschalig wärmedämmendes Mauerwerk oder Mauerwerk/Beton mit Perimeterdämmung und Bauwerksabdichtung.

**Bodenplatten mit Perimeterdämmung und Bauwerksabdichtung:**
- Raumseitige Schichten dürfen max. 20 % des Gesamtwärmedurchlasswiderstandes der Bodenplatte betragen.

**Nicht belüftete Dächer:**
- Wärmedurchlasswiderstand der Schichten unterhalb raumseitiger diffusionshemmender/diffusionsdichter Schicht: max. 20 % des Gesamtwärmedurchlasswiderstandes.
- Aufbautypen (Abb. 13.10–13.14):
  - Zwischensparren- ± Aufsparrendämmung (Tab. 13.3)
  - Nur Aufsparrendämmung (Tab. 13.4)
  - Von außen eingelegte diffusionsbegrenzende Schicht mit variablem sd-Wert (bei Bestandskonstruktionen, Abb. 13.12): sd,feucht ≤ 0,5 m; 2,0 m ≤ sd,trocken ≤ 10,0 m
  - Diffusionsdichte Untersparrendämmung (ggf. + Zwischensparrendämmung), sd,i ≥ 10 m (Abb. 13.13); Luftschicht h ≥ 5 cm, sd,i ≥ 100 m
  - Dachabdichtung (Abb. 13.14): sd,i ≥ 100 m; zwischen sd,i und Dachabdichtung kein Holz

**sd-Werte für Dachtypen (Tab. 13.3 — Zwischensparren-/Aufsparrendämmung):**

| sd,e außen | sd,i innen |
|-----------|-----------|
| ≤ 0,1 m | ≥ 1,0 m |
| 0,1 < sd,e ≤ 0,3 m | ≥ 2,0 m |
| 0,3 < sd,e ≤ 2,0 m | ≥ 6 · sd,e |

**sd-Werte für Dachtypen (Tab. 13.4 — nur Aufsparrendämmung):**

| sd,e außen | sd,i innen |
|-----------|-----------|
| ≤ 0,5 m | ≥ 10 m |
| > 0,5 m | ≥ 100 m |

Zwischen sd,i- und sd,e-Schicht kein Holz oder Holzwerkstoff.

**Belüftete Dächer:**
- Dachneigung < 5° (Abb. 13.15):
  - Schichten unterhalb diffusionsstrombegrenzender Schicht: R ≤ 20 % Gesamtwärmedurchlasswiderstand
  - Sparren-/Luftraumlänge ≤ 10 m
  - Lüftungsquerschnitt an mind. zwei gegenüberliegenden Dachrändern: Q ≥ 2 ‰ der zugehörigen geneigten Dachfläche, mindestens 200 cm²/m
  - Freier Lüftungsquerschnitt über Dämmschicht: ≥ 2 ‰ der geneigten Dachfläche, mindestens 5 cm Höhe; sd,i ≥ 100 m
- Dachneigung ≥ 5° (Abb. 13.16):
  - Lüftungsquerschnitt an Traufe: Q ≥ 2 ‰, mindestens 200 cm²/m
  - Lüftungsquerschnitt an First und Grat: Q ≥ 0,5 ‰, mindestens 50 cm²/m
  - sd,i ≥ 2 m; Belüftungsebene h ≥ 2 cm

---

##### 13.2.5 Berechnungsbeispiele Tauwassernachweis

**Beispiel a — Außenwand (Tab. 13.5 / Abb. 13.18–13.20):**

Schichtaufbau (von innen nach außen):

| Schicht | d [m] | μ [–] | sd [m] | λ [W/(m·K)] | R [m²·K/W] | θ [°C] | psat [Pa] |
|---------|-------|--------|--------|-------------|-------------|--------|----------|
| Raumluft | — | — | — | — | — | 20,0 | 2337 |
| Wärmeübergang innen | — | — | — | — | 0,250 | 18,6 | 2142 |
| Spanplatte V20 | 0,019 | 50 | 0,95 | 0,127 | 0,150 | 17,8 | 2037 |
| Diffusionshemmende Schicht | — | 5·10⁵ | 40000 | — | — | 17,8 | 2037 |
| Mineralwolle | 0,160 | 1 | 0,16 | 0,040 | 4,000 | −4,0 | 437 |
| Spanplatte V100 | 0,019 | 100 | 1,90 | 0,127 | 0,150 | −4,8 | 408 |
| Wärmeübergang außen | — | — | — | — | 0,040 | −5,0 | 401 |
| Summe | 0,1981 m | — | sd,T = 5,01 m | — | RT = 4,590 m²·K/W | — | — |

U = 1/4,590 = 0,218 W/(m²·K); Wärmestromdichte q = 0,218 · 25 = 5,447 W/m².

Tauwasserausfall im Glaserdiagramm zwischen Mineralwolle und äußerer Spanplatte (V100):
- gc = 3,48 · 10⁻⁸ kg/(m²·s)
- Mc = 3,48 · 10⁻⁸ · 7776 · 10³ = 0,27 kg/m²
- Mc ≤ Mc,max = 0,5 kg/m² ✓
- Feuchtegehaltszunahme Spanplatte V100: Δu = Mc / (ρ · d) = 0,27 / (700 · 0,019) = 0,02 % ≤ 3 % ✓

Verdunstungsperiode:
- gev = 8,48 · 10⁻⁸ kg/(m²·s)
- Mev = 8,48 · 10⁻⁸ · 7776 · 10³ = 0,659 kg/m²
- Mc = 0,27 kg/m² < Mev = 0,659 kg/m² ✓ → Tauwasserbildung unschädlich.

**Beispiel b — Flachdach (Tab. 13.6 / Abb. 13.21–13.23):**

| Schicht | d [m] | μ [–] | sd [m] | λ [W/(m·K)] | R [m²·K/W] | θ [°C] | psat [Pa] |
|---------|-------|--------|--------|-------------|-------------|--------|----------|
| Raumluft | — | — | — | — | — | 20,0 | 2337 |
| Wärmeübergang innen | — | — | — | — | 0,250 | 18,4 | 2115 |
| Stahlbeton | 0,18 | 70 | 12,6 | 2,100 | 0,086 | 17,8 | 2037 |
| Diffusionshemmende Schicht | 0,002 | 10000 | 20 | — | — | 17,8 | 2037 |
| Polystyrol-Partikelschaum | 0,140 | 30 | 4,2 | 0,040 | 3,500 | −4,7 | 412 |
| Dachabdichtung | 0,006 | 100000 | 600 | — | — | −4,7 | 412 |
| Wärmeübergang außen | — | — | — | — | 0,040 | −5,0 | 401 |
| Summe | 0,328 m | — | sd,T = 636,8 m | — | RT = 3,876 m²·K/W | — | — |

U = 1/3,876 = 0,258 W/(m²·K); q = 0,258 · 25 = 6,45 W/m².

Tauwasserausfall zwischen Polystyrol und Dachabdichtung:
- gc = 4,078 · 10⁻⁹ kg/(m²·s)
- Mc = 4,078 · 10⁻⁹ · 7776 · 10³ = 0,032 kg/m² ≤ 0,5 kg/m² ✓

Verdunstungsperiode (psat,c = 2000 Pa für Dach):
- gev = 4,614 · 10⁻⁹ kg/(m²·s)
- Mev = 4,614 · 10⁻⁹ · 7776 · 10³ = 0,036 kg/m²
- Mc = 0,032 kg/m² < Mev = 0,036 kg/m² ✓ → Tauwasserbildung unschädlich.

---

#### 13.3 Maßnahmen gegen Tauwasserausfall im Bauteilinneren

Fünf Strategien:

**a) Schichtenfolge ändern:**
- sd-Werte von innen nach außen abnehmen lassen.
- Wärmedurchlasswiderstände von innen nach außen zunehmen lassen.
- Ziel: möglichst hoher Sattdampfdruckverlauf im Querschnitt (Abb. 13.24).

**b) Baustoffe austauschen:**
- Baustoffwahl beeinflusst μ und λ.
- Bei Innendämmung und Kerndämmung: diffusionsbremsende Dämmstoffe mit großem μ günstig (Tauwasser vermeiden), aber nicht so hoch, dass Austrocknen auch nach innen stark behindert wird.
- Feuchtetechnische Betrachtung innengedämmter Konstruktionen: sehr komplex, instationäre Analyse erforderlich.
- Bei außenliegender Wärmedämmung oder homogenem Aufbau: sd-Werte der Schichten weniger relevant.
- Flachdächer: feucht gewordene Dämmschicht kann ggf. durch dampfdurchlässige Kunststoffabdichtungsbahn statt Bitumenbahn zum Austrocknen gebracht werden.
- Allgemein: diffusionsoffene Bauweisen sind vorteilhaft (schnellere Feuchteabgabe).

**c) Dampfbremsen / Dampfsperren einbauen:**
- Dampfbremse: 10 m ≤ sd < 100 m
- Dampfsperre: sd ≥ 100 m
- Sperrschicht erniedrigt Dampfdruck im dahinter liegenden Bereich, erhöht ihn davor (Abb. 13.25).
- Positionierung: möglichst nah an der Bauteiloberfläche, die an das tauwasserliefernde Klima angrenzt (= raumseitig bei Winterfall).
- Zusätzlich: mechanischen Schutz der Abdichtungsschicht sicherstellen und ausreichende Kondensatpuffer berücksichtigen.

**d) Hinterlüften / Belüften:**
- Hinterlüftete Schichten werden diffusionstechnisch vom übrigen Bauteil entkoppelt.
- Besonders wichtig bei außen liegenden Schichten mit großem sd (z.B. Metallfassaden).
- Nachteil: häufig verringert sich Wärmeschutz.
- Wirksamkeitsbedingungen: siehe Abschn. 11.3.2.

**e) Luftdichtheit sicherstellen:**
- Luftströmung von innen nach außen kann im Winter rasch große Wassermengen in kalte Querschnittsbereiche transportieren → Tauwasserbelag.
- Außenbauteile müssen deshalb luftdicht ausgeführt werden.

---

#### 13.4 Feuchtetransport bei einseitiger Wasserbelastung

##### 13.4.1 Flüssigwassertransport

- Ungesättigter Flüssigwassertransport beschreibbar nach Krischer (Gl. 11.18) mit Flüssigkeitsleitkoeffizient κ(u), der mit steigendem Wassergehalt weit überproportional zunimmt.
- Kießl-Ansatz: κ(u) über Exponentialansatz (Gl. 11.21) approximiert.
- Stationäre Massestromdichte (Gl. 13.43): g = (κ0 · uf / xf) · ln(κf/κ0)
  - κ0 = Leitkoeffizient bei u = 0 (trockene Seite)
  - κf = Leitkoeffizient bei u = uf (wasserbelastete Seite)
  - xf = Schichtdicke
- Vereinfachung zulässig, wenn κ0/κf < 10⁻² und u∞/uf < 0,6 (Gültigkeitsbereich z.B. für gefügedichten Beton bis 95 % r.F. auf Luftseite).
- Wassergehaltsprofil (Gl. 13.46): u(x)/uf = 1 − ln(1 + x/xf · (κf/κ0 − 1)) / ln(κf/κ0)
  - Profile für Betonschichten der Dicke 0,1 m bis 0,4 m in Abb. 13.27 dargestellt.
  - Massestromdichte nimmt mit größerer Schichtdicke ab.

##### 13.4.2 Flüssigwassertransport und Diffusion in Serienschaltung

- In einseitig wasserbelasteten feinporigen Schichten entsteht auf der luftseitigen Seite eine trockene Zone geringer Dicke mit hygroskopischer Feuchte → Wasserdampfdiffusion.
- Wasserbelastete Zone: Flüssigwassertransport bestimmend (Abb. 13.28).
- Grenzkoordinate x∞ zwischen beiden Zonen: Wassergehalt dort = Gleichgewichtsfeuchte bei 95 % r.F. (obere Grenze hygroskopischer Bereich).
- Im stationären Zustand müssen Massestromdichten beider Zonen übereinstimmen:
  - Flüssigwassertransport-Zone (Gl. 13.47): gFL = (κ0 · uf / xf) · ln(κf/κ0) [mit xf als Dicke der Flüssigwasserzone]
  - Diffusionszone (Gl. 13.48): gD = δ · Δp / (d − x∞) [d = Gesamtdicke]
- Mit Übergangsbereich an Luftseite (Gl. 13.51): gD = Δp / (1/βp + (d − x∞)/δ)
- Verhältnis Diffusionszonenlänge zu Gesamtdicke (Gl. 13.50): x∞/d = gFL/(gFL + gD) → bei den meisten Baustoffen liegt x∞/d zwischen 0,9 und 1,0 (Diffusionszone sehr dünn).
- Bedingung für wasserundurchlässigen Baustoff (Gl. 13.53): κf · uf · ln(κf/κ0) / (βp · Δp · d) < 1
  - Wasserundurchlässigkeit erfordert: kleines uf, kleines κf, große Schichtdicke d, große Verdunstungsstromdichte βp · Δp.
  - Nur Beton erfüllt diese Bedingung sicher → wasserundurchlässiger Beton praxisbewährt.
