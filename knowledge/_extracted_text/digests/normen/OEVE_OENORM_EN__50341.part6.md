# OEVE_OENORM_EN__50341 — Teil 6
> Quelle: OEVE_OENORM_EN__50341 (normen) · Seiten 241-273.

EN 50341 ist die europäische Norm für **Freileitungen über AC 45 kV** (Konstruktion von Hochspannungs-Freileitungen, Stahlgittermaste, Stahlmaste, Gründungen, Leiter, Isolatoren, Armaturen). Dieser Teil 6 (Anhänge J–R, das Dokumentende) behandelt: Stabilitäts-/Knicknachweis von Gitterfachwerk-Stäben (Anhang J), Bemessung einstieliger Stahlmaste (Anhang K), Bemessungsanforderungen für Tragwerke + Gründungen (Anhang L), geotechnische Bodenkennwerte (Anhang M), Leiter/Erdseile (Anhang N), Isolatorprüfungen (Anhang P), Isolatoren (Anhang Q) und Freileitungsarmaturen (Anhang R). **Hinweis:** Dies ist reine Hochspannungs-Freileitungs-Statik/Mechanik — kein Wohnungs-/Gebäude-Elektroinstallationswissen (kein OVE E 8101-Stoff). Querverweise durchgehend auf ENV 1993-1-1 (Eurocode 3, Stahlbau).

## Inhalt

### Anhang J (normativ) — Knicknachweis Gitterfachwerk-Stäbe (Winkelprofile)

**J.6.3.3 Gekreuzte Diagonalen**
- Wenn beide Stäbe durchlaufen und mit ≥1 Schraube verbunden sind: Schnittpunkt = Festpunkt in der Diagonalebene. Knicklänge = 1,0·L1, Schlankheitsgrad λ1 = 1,0·L1/ivv.
- Behinderung der Verschiebung quer zur Diagonalebene hängt von Sd/Nd ab (Sd = Kraft im Stützstab Zug/Druck, Nd = Kraft im Druckstab). Zusätzliche Schlankheitsgrade λ2:
  - Sd Zugkraft und Sd/Nd ≥ 2/3: λ2 = λ1 = 1,0·L1/ivv (Schnittpunkt Festpunkt)
  - Sd Zugkraft und Sd/Nd < 2/3: λ2 = 1,0·(L/iyy)·√(1 − 1,5·Sd/Nd)
  - Sd Druckkraft und Sd ≤ Nd: λ2 = 1,0·(L/iyy)·√(1 + 2·Sd/Nd), mit λ2 ≤ L2/iyy

**J.6.3.4 Gekreuzte Diagonalen mit Aussteifungsstäben**
- Aussteifungsstäbe stabilisieren Eckstiele, vermindern Knicklänge um kleinste Trägheitsachse auf L1: λ1 = 1,0·L1/ivv.
- Knicken mit Länge L2 um rechtwinklige Achse quer zur Diagonalebene: λ2 = 1,0·L2/iyy; λ2 mit Beiwert (Sd/Nd) nach J.6.3.3(2) multiplizieren.
- Schlankheit der Gesamtdiagonallänge L3 um Querachse yy darf **350 nicht überschreiten**.

**J.6.3.5 Unterbrochene gekreuzte Diagonalen mit durchgehendem Horizontalstab am Schnittpunkt**
- Horizontalstab muss in Querrichtung steif genug sein, um Festpunkt zu sein, wenn Druckkraft eines Stabs die Zugkraft des anderen übersteigt oder beide druckbelastet.
- Kriterium erfüllt, wenn Horizontalstab (Knicken über Gesamtlänge um Achse yy) der algebraischen Summe der in waagrechte Richtung zerlegten Kräfte standhält.
- Größte Schlankheit des Horizontalstabs darf **250 nicht überschreiten**.

**J.6.3.6 Mehrfache Gitterdiagonalen**
- Winkeldiagonalstäbe, an allen Schnittpunkten verbunden: zusätzlich als Sekundärstäbe (nach J.10) mit Knicklänge Eckstiel-zu-Eckstiel und Trägheitsradius iyy bemessen.
- Stabilität Mastabschnitt: iyy/ivv sollte **> 1,25** sein; gesamter Schlankheitsgrad L/iyy **< 350**.
- Stab AB unter Last mit kritischer Knicklänge L0: λ = 1,0·L0/ivv.

**J.6.3.7 Gekreuzte Diagonalen mit diagonalen Eckverbindungen**
- Fünf Stabilitätsprüfungen erforderlich:
  1. Stab unter größter Last, Länge L1, um kleinste Trägheitsachse vv.
  2. Stab unter größter Last, Länge L2, um Querachse yy.
  3. Beide gekreuzten Diagonalen, algebraische Summe, Länge L3, Achse yy.
  4. Zwei Stäbe (je benachbarte Wand), algebraische Summe der mit Eckstab verbundenen Lasten, Länge L4, Achse yy.
  5. Vier Stäbe (je gekreuzte Diagonale in zwei Nachbarwänden), algebraische Summe aller vier, Länge L5, Achse yy.
- Schlankheit von L5 um yy darf **350 nicht überschreiten**.

**J.6.3.8 K-Ausfachung**
- Kritische Knicklänge L1 um Achse kleinster Trägheit: λ1 = 1,0·L1/iyy.
- Ohne dritte Wand: Knicken Länge L2 → λ2 = 1,0·L2/iyy oder L2/izz.
- Mit dritter Wand + dreiecksförmiger Aussteifung: Länge L3 zwischen Aussteifungsstäben → λ3 = 1,0·L3/iyy oder L3/izz.

**J.6.4 Zusammengesetzte Stäbe**
- J.6.4.1: Gebildet aus zwei Rücken-an-Rücken-Winkelstählen (Bild J.7) oder zwei/drei/vier Winkelstählen mit kreuzförmigem Querschnitt (Bild J.8). Durchgehend verschweißt → als ein Stab. Fachwerkgitterstäbe: siehe ENV 1993-1-1 Abschnitt 5.9.2.
- J.6.4.2 Einzelheiten: Schlankheitsgrad eines Teilstabs **λ1 ≤ 50**. Bindebleche mindestens in Drittelpunkten der gesamten Knicklänge + an Stabenden. Bei Anschluss an gemeinsames Knotenblech keine zusätzlichen Bindebleche an Enden. Jedes Bindeblech an jeden Einzelstab mit Schrauben/gleichwertiger Schweißnaht; an Stabenden zusätzliches Verbindungselement je Verbindung. Über Eck gestellte Winkelstähle: **mind. 2 Schrauben je Stab je Bindeblech**.
- J.6.4.3 Bemessung: Mehrteilige Druckstäbe aus m Einzelstäben mit Stoffhauptachse y-y → quer dazu wie einteilige Druckstäbe. Quer zur stofffreien Achse z-z → ideelle Schlankheit λ = √(λz² + (m/2)·λ1²). m = Anzahl Profile; λz = Schlankheit Gesamtstab (J.6.2/J.6.3); λ1 = Schlankheit Einzelstab = c/ivv; c = Abstand zwischen Bindeblechen (Bilder J.7, J.8).

**J.7 Zusätzliche Empfehlungen für Ausfachungsformen**
- J.7.1 Waagrechte Randstäbe mit Querverbänden (Bild J.9): Querverband nötig wenn Schlankheit > J.6.3.5(3) / J.7.2(5) oder gegen Teilinstabilität. Praktische Bemessungsregel: waagrechter Querverband muss waagrechter Einzellast **F = 1,5·L [kN]** (L = Länge waagrechter Randstab in m), angreifend in Stabmitte, standhalten; Durchbiegung der waagrechten Diagonalen unter dieser Last begrenzt auf **L/1000**.
- J.7.2 Waagrechte Randstäbe ohne Querverband: wirksame Länge kL aus Bild J.10. **k = 0,085·R² − 0,316·R + 0,730**, mit R = |P2/P1| und 0 ≤ R ≤ 1 (P2 = Zuglast, P1 = Drucklast). Trägheitsradius iyy für Knicken quer zum Fachwerk (außer Einzelwinkelstäbe → ivv oder sekundäres Fachwerk). Stab an beiden Enden nicht durchlaufend annehmen. Gesamtschlankheit um Querachse **< 250**.
- J.7.3 Geknicktes K-Fachwerk (Bild J.11): Abknickung in Hauptdiagonalen bei großen Mastbreiten; ermäßigt Längen/Maße Sekundärstäbe, ruft höhere Spannungen am Knick hervor, erfordert Queraussteifung.
- J.7.4 Portalrahmen (Bild J.12): waagrechter Stab am Knickpunkt → Portalrahmen; Nachteil Fehlen Gelenk (anders als K-Fachwerk), empfindlich für Gründungssetzungen/-bewegungen. λ = kL/iyy; λ = kL/ivv für Winkel.

**J.8 Berechnung der wirksamen Schlankheit λeff (belastungsgestützte Bemessung)**
- Knickbeanspruchbarkeit nach ENV 1993-1-1 Abschnitt 5.5.1.2, Imperfektionsbeiwert **0,34 (Kurve b)**.
- Dimensionslose Schlankheit λ̄ = (λ/π)·√(fy/E)·√(Aeff/A). λeff (Kurve b):
  - Fall 1: λeff = e^(1,747·λ̄ − 1,98) für 0,2 ≤ λ̄ ≤ 1,035; λeff = 1,091·λ̄ − 0,287 für λ̄ ≥ 1,035
  - Fall 2: λeff = e^(1,747·1,2λ̄ − 1,98) für 0,2 ≤ λ̄ ≤ 1,035; λeff = 1,091·1,2λ̄ − 0,287 für 1,2λ̄ ≥ 1,035 (= Fall 1 mit λ = 1,2·λ von Fall 1)
  - Fall 3: λeff = 0,02 + 0,88·λ̄
  - Fall 4: λeff = 0,30 + 0,68·λ̄
  - Fall 5: λeff = 0,52 + 0,68·λ̄
  - Fall 6: λeff = 0,16 + 0,94·λ̄
- Zutreffender Knickfall nach J.9 / Tabelle J.1.

**J.9 Wahl des Knickfalles für Winkelprofile**
- J.9.1 Einfachwinkel: Knickkurve b (ENV 1993-1-1). Eckstiele: Fall 1 = axial belasteter Stab durch mehrere Diagonalfelder ohne versetzte Abstützungen (Bild J.3 a/b/c); Fall 2 = gleicher Stab mit versetzten Abstützungen (Bild J.3 d). Diagonalen: einschenkliger Anschluss erzeugt Exzentrizitäten/Zwänge; Auswirkungen heben sich gegenseitig bei Schlankheitsparameter **λ̄ = √2** auf. Knicklängen = geometrische Längen (Abstand Mitten Systemschnittpunkte). Günstigerer Fall bei ausreichender Endsteifigkeit (min. 2 Schrauben oder Schweißung). Geschweißte Diagonale = als 2 Schrauben angeschlossen betrachtet. Diagonalstäbe an beiden Eckstielen = wie Eckstiele.
- Durchlaufbedingungen: 2 Enden (beidseitig durchlaufend), 1 Ende, 0 Enden (Einzelfeldstab).
- J.9.2 Mehrteilige/Gitterstäbe: Gesamtnachweis nach Fall 1; Einzelstab nach Tabelle J.1.

**Tabelle J.1 – Knickfälle (Auswahl):**
| Stab | Knickachse | λ̄-Bedingung | Lastexz./Durchlauf | Schrauben am nicht-durchl. Ende | Fall |
|---|---|---|---|---|---|
| Diagonal | vv | < √2 | 1 Ende | – | 3 |
| Diagonal | vv | < √2 | 2 Enden | – | 4 |
| Diagonal | vv | > √2 | 2 Enden | – | 1 |
| Diagonal | vv | > √2 | 1 Ende | 2 Schrauben | 4 |
| Diagonal | vv | > √2 | 1 Ende | 1 Schraube | 1 |
| Diagonal | vv | > √2 | 0 Enden | 2 Schrauben | 4 |
| Diagonal | vv | > √2 | 0 Enden | 1 Schraube | 1 |
| Diagonal | yy/zz | < √2 | 1 Ende | – | 4 |
| Diagonal | yy/zz | < √2 | 2 Enden | – | 5 |
| Diagonal | yy/zz | > √2 | 2 Enden | – | 1 |
| Diagonal | yy/zz | > √2 | 1 Ende | 2 Schrauben | 4 |
| Diagonal | yy/zz | > √2 | 1 Ende | 1 Schraube | 1 |
| Diagonal | yy/zz | > √2 | 0 Enden | 2 Schrauben | 5 |
| Diagonal | yy/zz | > √2 | 0 Enden | 1 Schraube | 6 |
| Eckstiel | vv | alle Fälle | Bild J.3 (a)(b) | | 1 |
| Eckstiel | vv | alle Fälle | Bild J.3 (c) | | 1 |
| Eckstiel | yy/zz | alle Fälle | Bild J.3 (d) versetzt | | 2 |

**J.10 Sekundärstäbe (Null-Stäbe)**
- Hypothetische Kraft quer zum gestützten Hauptstab an jedem Knotenpunkt (addiert sich NICHT zu vorhandenen Kräften). Wert = K·N/100, mit **K = (λ + 60)/32** [Form aus Original], **1 ≤ K ≤ 2**, N = Axialkraft im Hauptstab.
- Winkel zwischen Sekundär- und Hauptstab **nicht weniger als 15°**.
- K-Fachwerk mit Knick (Bild J.11) und Diagonalwinkeln nahe 15°: Sekundäreffekte mitbetrachten (Gesamtinstabilität, Eckstielverkürzung, Schraubenschlupf).

**J.11 Schraubverbindungen (Tabelle J.2, Bild J.13):**
- Scherbeanspruchbarkeit je Scherfläche: gewindeloser Teil → Fv,Rd = 0,6·fub·A/γMb; Gewindeteil → Fv,Rd = 0,6·fub·As/γMb (Güten 4.6/5.6/6.6/8.8 und 4.8/5.8/6.8/10.9).
- Lochleibung je Schraube: Fb,Rd = α·fu·d·t/γM2; α = kleinster Wert aus 1,20·(e1/do); 1,85·(e1/do − 0,5); 0,96·(P1/do − 0,5); 2,3·(e2/do − 0,5).
- Zugbeanspruchbarkeit je Schraube: Ft,Rd = 0,9·fub·As/γMb.
- A = Querschnittsfläche Schraube; As = Schraubenfläche Gewindeteil (axialer Zug); d = Schraubendurchmesser; d0 = Bohrungsdurchmesser.

### Anhang K (normativ) — Einstielige Stahlmaste

Verweise in Klammern auf ENV 1993-1-1.
- **K.1 Symbole:** A Querschnittsfläche, Aeff wirksame Fläche, AS Zugquerschnitt Ankerschrauben, b Nennbreite, beff wirksame Breite, d Außendurchmesser (über Polygonecken), fbd Verbundspannung Stahl/Beton, fck char. Druckfestigkeit Beton, fctm durchschn. Zugfestigkeit Beton, fctk0,05 char. Zugfestigkeit Beton, fub Zugfestigkeit Ankerschrauben, fy Streckgrenze, Msd Biegemoment, Nsd Axialkraft, n Polygon-Seitenzahl, t Dicke, Weff/Wel wirksames/elastisches Widerstandsmoment, ∆M zusätzliches Moment, σcom,Ed größte Druckspannung, σx,Ed größte Längsspannung, γc Teilsicherheitsbeiwert Verbund, γM1 Beanspruchbarkeit, γMb Ankerschrauben, λ̄p Plattenschlankheit, ρ Reduktionsbeiwert, ψ Spannungsverhältnis.

**K.2 Querschnittsklassen (Abschnitt 5.3):** Klasse 3 wenn Dünnwandigkeit erlaubt, dass berechnete Spannungen in äußeren Druckzonen die Streckgrenze erreichen. Sonst Klasse 4 (explizite Beul-Vorkehrungen nötig).
**Tabelle K.1 – Klasse-4-Kriterien:**
- Rohr (kreisförmig): **d/t > 176·ε²**
- Polygon (n = 6 bis 18 Seiten): **b/t > 42·ε**
- mit ε = (235/fy)^0,5; fy = Nennwert Streckgrenze in N/mm².

**K.3 Wirksame Querschnittswerte Klasse 4 (Abschnitt 5.3.5):** Mit wirksamer Breite druckbeanspruchter Teile (Bild K.1). Effektive Breiten nach ENV 1993-1-1 Tabelle 5.3.2; Abminderungsfaktor ρ aus 5.3.5(3). Spannungsverhältnis ψ auf Bruttoquerschnittswerte beziehbar. Wirtschaftlicher: Plattenschlankheit λ̄p mit größter Druckspannung σcom,Ed statt fy (iterativ; ψ je Schritt neu, inkl. Zusatzmoment ∆M).

**K.4 Kreisförmige Querschnitte ohne Öffnungen mit überwiegendem Biegemoment:**
- Kriterium: σx,Ed ≤ ρ·fy/γM1.
- Klasse 3: ρ = 1,0.
- Klasse 4: ρ = 0,70 + 53/((d/t)·ε²) ≤ 1,0, mit ε = (235/fy)^0,5.
- Bild K.2 gibt ρ als Funktion d/t (Stahl S235 und S355; ρ-Skala 0,83–1, d/t 100–250).

**K.5 Polygonale Querschnitte ohne Öffnungen mit überwiegendem Biegemoment:**
- K.5.1 Klasse 3 (5.4.8.2): σx,Ed ≤ fy/γM1, d.h. Nsd/A + Msd/Wel ≤ fy/γM1 (A Bruttofläche, Wel elastisches Widerstandsmoment).
- K.5.2 Klasse 4 (5.4.8.3): σd ≤ fy/γM1, d.h. Nsd/Aeff + Msd/Weff ≤ fy/γM1 (Aeff wirksame Fläche unter gleichförmigem Druck, Weff wirksames Widerstandsmoment). Detailmethode in ENV 1993-1-1 5.3.5; Nomogramme Bilder K.3/K.4 für schnelle Aeff/Weff-Bestimmung (Polygone n = 6/8/12/16/18, fy = 235 und 355 N/mm², d/t bis 250).

**K.6 Bemessung von Ankerschrauben (Tabelle K.2):**
- Verankerungslänge: gerade Anker / Anker mit Haken / Anker mit Platte; Grundform Fa,Rd = π·φ·Lb·fbd.
- Verbundspannung fbd = 0,36·√fck/γc für glatte Stäbe; fbd = 2,25·fctk0,05/γc für gerippte Stäbe.
- fctk0,05 = 0,7·fctm; fctm = 0,3·fck^(2/3). γc (Verbund) = **1,50**.
- Beispiel Beton **C 20/25**: fck = 20 N/mm², fctm = 2,2 N/mm², fctk0,05 = 1,55 N/mm² → fbd = 1,1 N/mm² (glatt) bzw. 2,3 N/mm² (gerippt).
- Bedingungen: Fa,Rd = π·φ·Lb·fbd ≥ Ft,Sd (Bemessungszugkraft je Schraube im Grenzlastzustand); Ft,Sd ≤ Ft,Rd = 0,9·fub·As/γMb. fub Zugfestigkeit Ankerschraube; As Zugquerschnitt; **γMb = 1,25**.
- ANMERKUNG (ENV 1993-1-1 6.5.5(6)): Wert mit Faktor **0,85** vermindern, wenn Gewinde nicht durch Schraubenfachfirma geschnitten.

### Anhang L (informativ) — Bemessungsanforderungen Tragwerke + Gründungen

- **L.1** Erforderliche Unterlagen: aufgebrachte Lasten inkl. Teilsicherheitsbeiwerte (Quer- T, Vertikal- V, Längslasten L an Isolator-/Leiter-/Erdseil-Anschlusspunkten), Windlasten auf Stützpunkte, Lastkombinationen, Grenzlastzustand je Kombination, Gebrauchstauglichkeitsgrenzzustand (zulässige Durchbiegungen), bevorzugte Fehlerfolge, Lasten aus Instandhaltung/Errichtung.
- **L.2** Stützpunktarten + Verwendungszweck; Tabelle L.1 (Art/Verwendung/Leitungswinkel/Isolatortyp), Tabelle L.2 (Umfang Verlängerungen: kleinste/größte Höhe, Zunahme in Metern; einzelne vs. Schaft-/Fußverlängerungen, Höhendifferenzgrenzen).
- **Tabelle L.3 Leitungsauslegung:** Teilleiter-Anzahl/Art/Größe/Anordnung/Abstand (horiz.+vert.), Erdseile (Anzahl/Art/Größe), Regelspannweite bei Nennhöhe, Stützpunktnennhöhe, größter Erdseilschutzwinkel ohne Wind (Grad), größte Einzelfeldlänge, größte Summe benachbarter Feldlängen, größte/kleinste Gewichtsspannweiten (Normal- und ungleiche Lastbedingungen, Endstützpunkte).
- **Tabelle L.4 Isolatorketten:** kleinste/größte Längen (Tragketten, Stützisolatoren, Hilfstragkette, Abspannkette innen/außen, Hilfskette mit/ohne Anpassung), Anzahl Isolatorstränge je Leiter (Trag-/Abspann-/Hilfsketten), kleinster Abstand spannungsführender Metallteile zu Stahlkonstruktion/geerdeten Armaturen, angenommene größte Ausschwingung (Grad) für Trag-/Abspann-/Hilfsketten. ANMERKUNG: V-Ketten → Länge zwischen Befestigungen / eingeschlossener Winkel / Druckbelastbarkeit.
- **Tabelle L.5 Räumliche Abstände:** Leiteranordnung (lotrecht/waagrecht/Dreieck), Mindesthöhe der Leiter am Tragwerk je Stützpunkttyp, größter Ausschwingwinkel Erdseile (Grad), kleinster lotrechter / projizierter lotrechter Abstand benachbarter Leiter eines Stromkreises, kleinster lotrechter Abstand Leiter↔Erdseil.
- **L.3** Befestigung Leiter/Erdseile in Projektspezifikation. **L.4** Stahlkonstruktion in Gründung (Fußeckstiele, Knaggen, Ankerschrauben, einbetonierte Schüsse). **L.5** Einrichtungen für Errichtung/Instandhaltung (vgl. 7.12: Instandhaltungs-, Befestigungs-, Transport-, Markierungs-, Erdungseinrichtungen). **L.6** Einschränkungen Massen/Maße (Gesamtbreite an Erdoberkante, Mastabschnitte/-schüsse, Einzelstäbe, Vor-Ort-Schweißen, Errichtungsmethoden).

### Anhang M (informativ) — Geotechnische Parameter Böden + Fels

- **M.1** Typische Werte nur bei fehlender Baugrunderkundung; ersetzen diese nicht, im Zweifel ungünstigeren Wert wählen.
- **M.2 Bodeneinteilung nach Korngröße (mm):** d > 200 Felsblöcke; 200–20 Kieselsteine; 20–2 Kies; 2–0,2 Grobsand; 0,2–0,06 Feinsand; 0,06–0,002 Schluff; d < 0,002 Ton.
- **M.3 Einheiten:** γ spez. Gewicht [kN/m³], γ' mit Auftrieb [kN/m³], Φ' innerer Reibungswinkel [Grad], c' Kohäsion [kN/m²], cu nicht entwässerte Scherfestigkeit [kN/m²], Ct Steifemodul in 2 m Tiefe [MN/m³], Rc Quetschfestigkeit [MN/m²], Rt Zugfestigkeit [MN/m²], E E-Modul [MN/m²].
- **Tabelle M.1** beschreibt 8 Bodenarten (kiesige Seitenmoränen, ungeordnete glaziale Schichten, geordnete glaziale Geschiebe, glazialer Ton, alluvialer Boden, Felsen/Klippenfuß, überkonsolidierte Böden, weiche Gesteine) mit Eignung von "sehr guter Untergrund" bis "schlechter Untergrund" (glazialer Ton = schlecht).

**Tabelle M.2 – Bodenmechanische Kennwerte (γ / γ' / Φ' / c' / cu in genannten Einheiten, Ct MN/m³):**
- Mergel kompakt: 20±2 / 11±2 / 25±5 / 30±5 / 60±20 / >200
- Mergel gealtert: 19±2 / 11±2 / 20±5 / 10±5 / 30±10 / 50±10
- Kies (unterschiedl. Korngrößen): 19±2 / 10±2 / 38±5 / – / – / 150±10
- Sand lose / mitteldicht / dicht: 18/19/20±2 · 10/11/12±2 · 30/32/35±5 · – · – · 60/80/100±10
- Sandiger Schluff: 18±2 / 10±2 / 25±5 / 10±5 / 30±10 / 60±10
- Toniger Schluff: 19±2 / 11±2 / 20±5 / 20±10 / 40±10 / 50±10
- Lehm/Schluff gemischt: 17±2 / 7±2 / 20±5 / – / 20±10 / 35±5
- Ton weich / halbsteif / steif: 17/19/20±2 · 7/9/10±2 · 12/15/20±5 · cu 25±5 / 30±5 / 40±5 (weicher Ton bis 60±20) · Ct 25–40±5
- Ton geschichtet: 20±2 / 10±2 / 30±5 / 12±7 / 400±350 / –
- Ton mit organ. Beimengungen: 15±2 / 5±2 / 15±5 / – / – / –
- Torf/Morast: 12±2 / 2±2 / – / – / – / –
- Verfüllmaterial/Dämme (mittl. Verdichtung): 19±2 / 10±2 / 25±5 / – / 15±5 / 20±5

**Tabelle M.3 – Gesteinskennwerte (Rc / Rt / E in MN/m²):**
- Granit/Gneis/Basalt: 100–200 / 4–10 / 20 000–70 000
- Schiefer/Ton: 15–100 / 0–10 / 7 000–50 000
- Kalkstein kompakt: 50–100 / 5–7 / 30 000–60 000
- Kalkstein weich: 10–20 / 1–3 / 4 000–20 000
- Mergel nicht gealtert: 10–20 / 1–2 / 200–1 000
- Sandstein: 10–100 / 1–6 / 10 000–40 000
- Molasse: 2–10 / 0,2–1 / 1 500–5 000
- Gips: 3–10 / 0,3–1 / 2 000–5 000
- ANMERKUNG: Querkontraktion µ i.d.R. 0,25–0,35; innerer Reibungswinkel Φ' i.d.R. 35°–45° (stark von Klüftung abhängig).

### Anhang N (informativ) — Leiter und Erdseile

- **N.1.2 Betriebliche Einflüsse:** Zuverlässigkeit/Wiederherstellungszeit, Stromtragfähigkeit (dauernd + kurzzeitig), elektrische Verluste (I²·R und Korona), innere/äußere Abstände, Leitungskennwerte (Längsreaktanz, Querblindleitwert), Lebensdauer.
- **N.1.3 Instandhaltung:** Zugang entlang Leiter zu Feld-Armaturen (Feldbündelabstandhalter, Sichtmarker).
- **N.1.4 Umweltparameter:** Wind/Eis (Festigkeit, Durchhang, Schwingung/Tanz), Verschmutzung (Korrosion), Blitze, Funkstörung, Geräuschpegel, Sichtmarker für Vögel/Flugzeuge, optische Wahrnehmbarkeit, E-/Magnetfelder, Leiterfett (Tropfpunkt/Chemie), Umgebungstemperaturen.
- **N.2 Leiterauswahl** — Leitermaterialien (Bezeichnungen): (a) Reinaluminium AL1; (b) Al/Al-Legierung AL1/ALx; (c) Al/Stahl AL1/STyz; (d) Al/Al-ummantelter Stahl AL1/ASyz; (e) Al-Legierung/Stahl ALx/STyz; (f) Al-Legierung/Al-umm. Stahl ALx/Syz; (g) Al-Legierung ALx; (h) Al-ummantelte Stahldrähte 20SA; (i) Kupfer/Kupferlegierung; (j) Stahl. Weitere Kriterien: Leiterart (Rund-/Segmentdrähte, verseilt), Bündelleiterart (Einzel/Zweier/Dreier/Vierer), Maße, Dauerstromtragfähigkeit, Fett, Oberflächenbehandlung, Leitfähigkeit, Spannungs-Dehnungsverhalten, Zugfestigkeit (Minderung mit Temp./Zeit), Kriechverhalten, LWL-Anforderungen, Korrosionsschutz, Schwingungskennwerte, höchste Betriebstemperatur (Dauer/Kurzzeit/Kurzschluss), zulässige Belastungen der Stützpunkte.
- **N.3/N.4:** Verpackung auf Spulen (vereinbarte Längen), Rücklieferung Leerspulen; beim Verlegen Oberflächenschäden klein halten, schleifenden Bodenkontakt vermeiden.

### Anhang P (informativ) — Prüfungen Freileitungsisolatoren/-ketten (Porzellan + Glas)

**Tabelle P.1** listet Prüfungen je Typ (Kettenisolatoren Langstäbe Typ A / Kappen Typ B, Isolatorketten, Stützenisolatoren):
- **Genormte Typprüfungen:** Maße, betriebsfrequente Stehspannung unter Regen, Steh-Blitzstoßspannung trocken, Steh-Schaltstoßspannung unter Regen, thermisch-mechanisches Verhalten, mechanische/elektromechanische Nennkraft.
- **Wahlfreie Typprüfungen:** Funkstörspannung, Fremdschicht, Lichtbogen, Stoßspannungsdurchschlag, Zinkkragen, Restfestigkeit.
- **Stichprobenprüfungen:** Maße, Nachweis Sicherungssystem/Abweichungen, Temperaturwechsel, mech./elektromech. Nennkraft, Wärmeschock (nur vorgespanntes Glas), Durchschlags-Stehspannung, Porosität (nur Porzellan), Verzinkung.
- **Wahlfreie Stichprobenprüfungen:** Funkstörspannung, Stoßspannungsdurchschlag, Zinkkragen.
- **Stückprüfungen:** Sichtprüfung, mechanische Prüfung, elektrische Prüfung; wahlfreie Stückprüfung: Ultraschall (Stützenisolatoren h > 300 mm).
- Fußnoten: a) an kurzem Standardstrang/Langstabisolator; b) Isolatorketten Us ≤ 245 kV; c) Us > 245 kV; d) Fremdschicht an Strängen ohne Armaturen; e) nur keramischer Werkstoff (siehe EN 60383-1).

### Anhang Q (informativ) — Isolatoren

- **Q.1.2 Betriebliche Faktoren:** Zuverlässigkeit/Wiedereinschaltzeit, Lebensdauer je Komponente, Nennspannung, vorübergehende Überspannungen, Isolationskoordination/Schaltverfahren, elektrische Abstände.
- **Q.1.3 Instandhaltung:** Arbeit unter Spannung/spannungsfrei, Zugang über Isolatoren, Resttragfähigkeit beschädigter Isolatoren, Befestigung Instandhaltungseinrichtungen (Trag-+Abspannketten).
- **Q.1.4 Umweltparameter:** NN-Höhe, Verschmutzungsgrad/-art, Geräuschpegel/Funkstörspannung, Blitz (Einschlagdichte, keraunischer Pegel) + Netzschutz, Umgebungstemperaturen, Wahrnehmbarkeit (Farbe), Vandalismus.
- **Q.2 Auswahl:** keramisch/Glas (Kappen-/Langstab-/Stützenisolatoren), Verbundisolatoren, Maße (Strang-/Kettenlänge, Abstand, Durchmesser, Kriechweg, Schirmprofil, Armaturen), Stehspannungen, Korrosionsschutz (Verzinkung, Zinkkragen an Kappenisolatoren, Fetten), Gewicht.
- **Q.3/Q.4:** Verpackung/Lieferung (Schutzverschläge gegen Stoß-/Schirmschäden); Einbau sorgfältig, ggf. mechan. Hubeinrichtungen, Personensicherheit; bei langen Strängen Verschlag zur Vermeidung von Biege-/Torsionslasten; halbstarre Verbindungen (Gabeln/Laschen/Ösen) empfindlich gegen hohe Torsionslasten beim Seilzug.

### Anhang R (informativ) — Freileitungszubehör / Freileitungsarmaturen

- **R.1.2 Betriebliche Einflussfaktoren:** Zuverlässigkeit/Betriebs-/Personensicherheit/Wiedereinschaltzeit, Lebensdauer je Komponente, Betriebsspannungsbereich, Stromtragfähigkeit, Verhalten im Kurzschlussfall, elektrische Verluste, Beanspruchungsbeschränkung durch Klemmenausführung.
- **R.1.3 Instandhaltung:** Arbeit unter Spannung/spannungsfrei, Zugang zu Leitern über Isolatoren+Armaturen, Befestigung Instandhaltungseinrichtungen (Trag-+Abspannketten), Zugang zu Feld-Armaturen (Feldabstandhalter, Sichtmarker).
- **R.1.4 Umwelteinflüsse:** winderregte Schwingungen, Geräuschpegel/Funkstörspannung, Vandalismus, Sichtmarker Vögel/Flugzeuge, Umgebungstemperaturbereich, atmosphärische Verschmutzung (Korrosion), Wind-/Eisbelastungen.
- **R.2/R.3:** Verpackung für sichere Lieferung (handhabbare Größe/Gewicht, Entsorgungsanforderungen); Einbau sorgfältig, ggf. mechan. Hubhilfen, Sicherheitsbestimmungen Arbeitspersonal.

---
*Quelldokument: BGBl. II, ausgegeben am 30. Jänner 2006, Nr. 33 (www.ris.bka.gv.at). EN 50341-1:2001 + EN 50341-2:2001 + EN 50341-3-1:2001. Norm-Seiten 237–269 = Dokument-Seiten 241–273 (Anhänge J, K, L, M, N, P, Q, R — Dokumentende).*
