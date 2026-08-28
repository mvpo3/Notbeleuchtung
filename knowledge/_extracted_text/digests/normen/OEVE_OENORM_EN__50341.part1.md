# OEVE_OENORM_EN__50341 — Teil 1
> Quelle: OEVE_OENORM_EN__50341 (normen) · Seiten 41-80.

Dieses Dokument ist die österreichische Übernahme der **EN 50341-1:2001 + EN 50341-2:2001 + EN 50341-3-1:2001** (Freileitungen über AC 45 kV), kundgemacht im BGBl. II Nr. 33, ausgegeben am 30. Jänner 2006. Es behandelt die **bautechnische, bodenmechanische und mechanische Auslegung von Hochspannungs-Freileitungen** (Maste, Leiter, Isolatoren, Gründungen, Eislasten, Windlasten). Teil 1 deckt den Schluss des Symbolverzeichnisses, die normativen Verweisungen, Abschnitt 3 (Auslegungsgrundlagen, Grenzzustände, Teilsicherheitsbeiwerte) sowie Abschnitt 4 (Einwirkungen — allgemeine und empirische Vorgehensweise mit den österreichischen NNA/A-dev-Festlegungen) ab.

> Hinweis Domain-Relevanz: Diese Norm betrifft **Starkstrom-Freileitungen >45 kV** (Mast-/Tragwerksstatik, Wind/Eis), NICHT Wohnungs-Innenelektroinstallation (dafür OVE E 8101). Für den ElektroPlaner ist sie Randwissen; bewahrt für Vollständigkeit der Wissensbasis.

## Inhalt

### Markierungstypen der nationalen Festlegungen (NNA)
- **(A-dev)** = nationale Abweichung (deviation), bindend für Österreich.
- **(ncpt)** = national complement (nationale Ergänzung).
- **(snc)** = special national condition / spezielle nationale Bedingung.
- **NNA** = Nationale Normative Festlegungen; **NNA enthält Teilsicherheitsbeiwerte und nationale Anforderungen → werden bindend**.

### Symbolverzeichnis (Schluss, Wind/Last/Sicherheit)
- **VR** Bezugswindgeschwindigkeit (4.2.2.1.5); **VR(II)** Bezugswindgeschwindigkeit an Messstelle Geländeart II.
- **Vg** Böenwindgeschwindigkeit (4.2.2.1.1); **Vh** Bezugswindgeschwindigkeit in Höhe h über Grund (4.2.2.1.6); **Vmean** Mittelwert Windgeschwindigkeit.
- **XK / Xd** charakteristischer / Bemessungswert einer Werkstoffeigenschaft (3.7.2); **XnK / Xnd** für Werkstoffeigenschaft n (3.7.3).
- **z0** Bodenrauhigkeitslänge (4.2.2.1.4).
- **α** Exponent Windgeschwindigkeits-Höhenänderung (4.2.2.1.6) bzw. Abminderungsbeiwerte für Eislasten (4.2.10.2).
- **β** Abminderungsbeiwert für die Leiterzugkraft (4.2.7).
- **γ** Teilsicherheitsbeiwert: γA (Ausnahmeeinwirkung), γC (Leiterzugkräfte), γF (Einwirkungen), γG (ständige Einwirkung), γI (Eis), γM (Werkstoff), γP (Errichtung/Instandhaltung), γPt (Vorspannkräfte 7.6.4), γQ / γQn (veränderliche Einwirkung), γw (Wind).
- **ρ** Luftdichte (4.2.2.2); **ρE** spez. Erdwiderstand nahe Oberfläche (Ω·m) (6.2.4.3); **ρI** Eisdichte (4.2.4.2); **ρ'** Luftdichte bei T' und Bezugshöhe H.
- **φ** Windeinwirkungswinkel der maßgebenden Windrichtung (4.2.2.4.1) bzw. Winkel Windrichtung↔Längsachse Gitterquerträger (4.2.2.4.3).
- **χ** Völligkeit eines Mastschusses (4.2.2.4.3).
- **Ψ** Kombinationsbeiwert: ΨI (Eis), ΨQ / ΨQn (veränderliche Einwirkung), ΨW (Wind).

### Normative Verweisungen (Abschnitt 2.3)
Alle Verweisungen **undatiert** (neueste Ausgabe gilt); abgestimmt mit CEN/CENELEC/IEC-Katalogen 2001.
- **EN ISO 1461** Feuerverzinkung (Stückverzinken); **EN ISO 9001/9002/9003** Qualitätsmanagement; **EN ISO 14713** Korrosionsschutz Zink/Aluminium; **EN ISO 9001** für QS-Maßnahmen (3.2.9).
- **EN 10025** warmgewalzte unlegierte Baustähle; **EN 10149** Flachstäbe hoher Festigkeit; **EN 10204** Prüfbescheinigungen; **EN 22063** thermisches Spritzen Zn/Al.
- Holzmaste: **EN 12465** (Dauerfestigkeit), **EN 12479** (Größen), **EN 12509/12510/12511** (Prüfverfahren/Festigkeitsklassifikation/Kennwerte); **EN 12843** vorgefertigte Betonmaste.
- Leiter/Drähte: **EN 50182** verseilte Leiter konzentrische Lagen, **EN 50183** Al-Mg-Si-Drähte, **EN 50189** zinkummantelte Stahldrähte, **EN 50326** Fett für blanke Leiter, **EN 60889** hartgezogene Al-Drähte, **EN 61232** Al-ummantelte Stahldrähte.
- Telekom-Beeinflussung: **EN 50351** (Berechnung/Messung), **EN 50352** (Grenzwerte).
- Isolationskoordination: **EN 60071-1/-2**. Isolatoren: EN 60305, EN 60383-1/-2, EN 60433, EN 60437, EN 60507, EN 61325, EN 61466-1/-2, EN 61109, IEC 60720, IEC/TR2 61211, IEC/TR2 61467.
- LWL-Kabel: EN 60794-1-1/-1-2, IEC 60794-4-1, **EN 187200** (OCEPL Lichtwellenleiter-Starkstromleitungen).
- Kurzschluss: **EN 60865-1** (Wirkung), **IEC 60909** (Berechnung Drehstrom), **IEC 60724** (Kurzschluss-Temperaturgrenzen Kabel 1 kV Um=1,2 kV / 3 kV Um=3,6 kV).
- Armaturen/Seile: EN 61284, EN 61395 (Kriechen), EN 61854 (Feldabstandhalter), EN 61897 (Schwingungsdämpfer Typ Stockbridge), IEC/TR3 61597 (Berechnung verseilter blanker Leiter), IEC 62219.
- Tragwerksnormen: **ENV 1090-1** Stahltragwerke; **EUROCODE 1** (ENV 1991: Grundlagen/Einwirkungen, -2-1 Dichten/Eigen-/Nutzlasten, -2-4 Windlasten); **EUROCODE 2** (ENV 1992 Stahlbeton); **EUROCODE 3** (ENV 1993 Stahlbau, -1-3 kaltverformte dünnwandige Stäbe, -5 Pfahlgründungen); **EUROCODE 5** (ENV 1995 Holzbau); **EUROCODE 7** (ENV 1997 Grundbau); **EUROCODE 8** (ENV 1998 Erdbeben, -5 Gründungen).
- **HD 637** Starkstromanlagen Nennwechselspannung über 1 kV; **IEC 60038** standard voltages.
- IEC-Vokabular: IEC 60050-441/-466/-471/-601/-604. Belastung/Festigkeit: **IEC/TR 60826** (Loading and strength overhead lines — Basis probabilistischer Zuverlässigkeit). Meteorologische Klimalasten: **IEC/TR2 61774**.
- CISPR 16-1/16-2 (Funkstörmessung), CISPR 18-2/18-3 (Funkstörung Freileitungen).

#### Österreichische Verweisungen (AT.1–AT.20)
- (ncpt) ÖNORM B 3304 (Betonzuschläge), B 3307 (Transportbeton), B 4100-2 (Holzbau).
- (A-dev) ÖNORM B 4200-4 (Stahlbeton Grundlagen), B 4200-7 (Stahleinlagen), B 4200-8/-9 (Stahlbeton Berechnung), B 4200-10 (Beton Herstellung/Überwachung). **Nat. Fußnote: B 4200-4/-8/-9 wurden durch ÖNORM B 4700 ersetzt.**
- (A-dev) ÖNORM B 4430-1 (zul. Belastung Baugrund, Flächengründungen), B 4430-2 (Pfahlgründungen), B 4605 (Stahlbau Maste).
- (ncpt) ÖNORM E 4000/E 4030/E 4006 (Freileitungsdrähte Al / Al-Stahl / verzinkte Stahldrähte), E 4200/E 4201/E 4202 (Holzmaste Behandlung/Berechnung/Tragfähigkeit).
- (A-dev) **ÖNORM S 1119** — niederfrequente elektr./magn. Felder, zulässige Expositionswerte zum Schutz von Personen im **Frequenzbereich 0 Hz bis 30 kHz**.
- (ncpt) DIN 48200 Teil 1 (Kupferdrähte).
- (A-dev) **ÖVE EN 50110-1** Betrieb elektrischer Anlagen; **ÖVE-L11** Errichtung von Starkstromfreileitungen über 1 kV.

### Abschnitt 3 — Grundlagen für Auslegung und Bemessung
- Gilt für Freileitungen mit Nennspannungen **über AC 45 kV**; im Zusammenhang mit EUROCODES 1, 2, 3, 5, 7, 8 lesen (Norm-Vorgaben treten an deren Stelle).
- Grundlage: **Grenzzustandskonzept** mit **Teilsicherheitsbeiwerten** (3.7).
- **(A-dev) AT.1 (3): In Österreich ist gemäß 4.3 „Einwirkungen, empirische Vorgehensweise" zu bemessen.** Eine Zuverlässigkeitsstufe muss daher NICHT festgelegt werden.
- (A-dev) AT.1: Nicht genormte Bauteile → Nachweis der geforderten Sicherheit erforderlich; rechnerischer Nachweis zulässig.

#### 3.2 Anforderungen
- Grundanforderungen: Übertragungsaufgabe mit angemessener Zuverlässigkeit; Schutz gegen kaskadenartige Schäden (Betriebssicherheit); keine Personenschäden bei Errichtung/Instandhaltung (Personensicherheit). Zusätzlich: öffentliche Sicherheit, Dauerhaftigkeit, Robustheit, Instandhaltbarkeit, Umweltverträglichkeit, Ästhetik.
- **3.2.7 Geplante Lebensdauer**: i. A. **50 Jahre** (sofern Projektspezifikation nichts anderes festlegt); Betriebsdauer üblich **30 bis 80 Jahre**.

##### Tabelle 3.1 — Zuverlässigkeitsstufen (Wiederkehrdauer T klimatischer Einwirkungen)
| Zuverlässigkeitsstufe | Wiederkehrdauer T (Jahre) |
|---|---|
| 1 | 50 |
| 2 | 150 |
| 3 | 500 |
- Gewählte Stufe muss mindestens Stufe 1 entsprechen (Ausnahme: zeitlich begrenzte Bauwerke/Komponenten). Jährliche Zuverlässigkeit ≈ zwischen **1 − 1/T** und **1 − 1/(2T)** (Minimalwert).

#### 3.3 Grenzzustände
- **Grenzlastzustände**: Zusammenbruch, übermäßige Verformung, Stabilitätsverlust, Umkippen, Riss, Knicken; betreffen Zuverlässigkeit/Betriebssicherheit von Stützpunkten, Gründungen, Leitern, Ausrüstung sowie Personensicherheit.
- **Grenzzustände der Gebrauchstauglichkeit**: mechanische Funktion + **elektrische Abstände**; Verformungen/Verschiebungen, Schwingungen, Risse.

#### 3.4 Einwirkungen
- Einwirkung F **direkt** (Last auf Tragwerk/Leiter) oder **indirekt** (aufgezwungene/verhinderte Verformung durch Temperatur, Grundwasser, Setzung).
- Zeitliche Einteilung: **G** ständige (Eigengewicht Tragwerke/Gründungen/Armaturen + Leitereigengewicht + Leiterzugkräfte bei Bezugstemperatur), **Q** veränderliche (Wind, Eis, äußere Lasten), **A** Ausnahmelasten (Schadensbegrenzung, Lawinen).
- 3.4.2: Veränderliche Einwirkung — oberer Wert mit jährlicher Wahrscheinlichkeit **0,02** nicht überschritten zu werden → **Wiederkehrdauer 50 Jahre**.

#### 3.7 Bemessungswerte und Nachweis
- Fd = γF · FK; G/Q/A: γG·GK, γQ·QK, γA·AK. Werkstoff: Xd = XK / γM.
- Grundgleichung: **Ed ≤ Rd** (Bemessungswert Auswirkung der Einwirkungen ≤ Tragwerksbeanspruchbarkeit).
- Kombinationen von Einwirkungen über Gleichungen (1)–(4): überwiegende Einwirkung γQ1·Q1K (üblicherweise Wind ODER Eis) + Kombinationswerte ΨQn·QnK; bei direkter Bestimmung dominante Einwirkung Q1 mit Wiederkehrdauer T1 (z. B. 150 Jahre) + ermäßigte Tn (z. B. 3 Jahre).

### Abschnitt 4 — Einwirkungen auf Freileitungen
- Zwei Versionen: **4.2 Allgemeine Vorgehensweise** und **4.3 Empirische Vorgehensweise**. **(A-dev) AT.1: In Österreich ist nach 4.3 (empirisch) zu bemessen.**

#### 4.2 Allgemeine Vorgehensweise — Windlasten
- 4.2.2.1.1: Höhenbegrenzung Tragwerk allgemein annehmbar **60 m**, falls NNA nichts vorgibt.
- **Vmean** = mittlere Windgeschwindigkeit (m/s), gemittelt über **10 min**, gemessen **10 m über Boden**, Geländeart II.
- **Vg** = Böenwindgeschwindigkeit, Mittelwert über **2 s**.
- Böenfaktor: **kg = 1 + 2,28 / ln(h/z0)**; Beziehung **Vg = kg · Vmean**.
- VR = Bezugswindgeschwindigkeit in 10 m Höhe. Umrechnung: **VR = VR(II) · kT · ln(10/z0)**.

##### Tabelle 4.2.1 — Geländebeiwert kT und Bodenrauhigkeitsparameter z0 (nach ENV 1991-2-4)
| Geländeart | Eigenschaften | kT | z0 |
|---|---|---|---|
| I | raue offene See, Binnenseen ≥5 km windseitig, flaches Gelände ohne Hindernisse | 0,17 | 0,01 |
| II | Ackerland mit Grenzhecken, verstreute kleine Häuser/Bäume | 0,19 | 0,05 |
| III | Vorstädte/Industriegebiete, ständige Wälder | 0,22 | 0,30 |
| IV | städtische Gebiete, ≥15 % Oberfläche mit Gebäuden ≥15 m Höhe | 0,24 | 1,0 |
| V | gebirgiges/komplexes Gelände | getrennt auszuwerten (ggf. Meteorologen) |
- Geländearten III und IV normalerweise nicht für Freileitungen anwendbar (nur zur Vollständigkeit).
- Höhenprofil: bis 10 m → Vh = VR; über 10 m → **Vh = VR(II) · kT · ln(h/z0)** (logarithmisches Gesetz); alternativ Potenzgesetz **Vh = VR · (h/10)^α**.

##### Tabelle 4.2.2 — Relative Änderung Vh/VR(II) = kT·ln(h/z0) je Geländeart und Höhe
| Geländeart | 10 m | 15 m | 20 m | 25 m | 30 m | 35 m | 40 m | 45 m | 50 m | 55 m | 60 m |
|---|---|---|---|---|---|---|---|---|---|---|---|
| I | 1,17 | 1,24 | 1,29 | 1,33 | 1,36 | 1,39 | 1,41 | 1,43 | 1,45 | 1,46 | 1,48 |
| II | 1,00 | 1,08 | 1,14 | 1,18 | 1,22 | 1,24 | 1,27 | 1,29 | 1,31 | 1,33 | 1,35 |
| III | 0,77 | 0,86 | 0,92 | 0,97 | 1,01 | 1,05 | 1,08 | 1,10 | 1,13 | 1,15 | 1,17 |
| IV | 0,55 | 0,65 | 0,72 | 0,77 | 0,82 | 0,85 | 0,89 | 0,91 | 0,94 | 0,96 | 0,98 |

##### 4.2.2.2 Staudruck
- **qh = ½ · ρ · Vh²** (N/m²). **ρ = 1,225 kg/m³ bei 15 °C und 1013 hPa.**

##### Tabelle 4.2.3 — Relative Luftdichte ρ (Funktion Höhe über NN und Temperatur)
| Temperatur °C | 0 m | 600 m | 1200 m | 1800 m |
|---|---|---|---|---|
| -30 | 1,18 | 1,10 | 1,02 | 0,95 |
| -20 | 1,13 | 1,05 | 0,97 | 0,91 |
| -5 | 1,08 | 1,00 | 0,93 | 0,87 |
| 5 | 1,04 | 0,96 | 0,90 | 0,84 |
| 15 | 1,00 | 0,93 | 0,86 | 0,80 |
| 30 | 0,96 | 0,89 | 0,83 | 0,77 |
- Ableitung: ρ'/ρ = e^(−1,2·10⁻⁴·H) · 288/T'.

##### 4.2.2.3 Windlast auf Komponenten
- **QWx = qh · Gq · Gx · Cx · A**. Gq = Böenfaktor (= **(kg)² = (1 + 2,28/ln(h/z0))²**; bei Option Böenwindgeschwindigkeit Gq = 1). Cx = Windwiderstandsbeiwert (Form), A = projizierte Fläche. Gesamtabminderung der Böenlasten typisch **5 % bis 15 %**.

##### Tabelle 4.2.4 — Böenfaktoren Gq je Geländeart und Höhe
| Geländeart | 10 m | 15 m | 20 m | 25 m | 30 m | 35 m | 40 m | 45 m | 50 m | 55 m | 60 m |
|---|---|---|---|---|---|---|---|---|---|---|---|
| I | 1,77 | 1,72 | 1,69 | 1,67 | 1,65 | 1,64 | 1,63 | 1,62 | 1,61 | 1,60 | 1,59 |
| II | 2,05 | 1,96 | 1,91 | 1,87 | 1,84 | 1,82 | 1,80 | 1,78 | 1,77 | 1,76 | 1,75 |
| III | 2,72 | 2,51 | 2,38 | 2,30 | 2,24 | 2,19 | 2,15 | 2,12 | 2,09 | 2,07 | 2,05 |
| IV | 3,96 | 3,39 | 3,10 | 2,92 | 2,79 | 2,69 | 2,62 | 2,56 | 2,51 | 2,46 | 2,42 |

##### 4.2.2.4 Windlasten auf Freileitungskomponenten
- **Leiter (4.2.2.4.1)**: QWc = qh · Gq · Gc · Cc · d · ½(L1+L2) · cos²φ. **Cc = 1,00 für verseilte Leiter aus Runddrähten bei üblichen Windgeschwindigkeiten.** L = Mittelwert der zwei benachbarten Spannfelder. Gesamtlast Leiterbündel = Summe Teilleiter (ohne Abschirmung leeseitig).
- **Isolatoren (4.2.2.4.2)**: QWins = qh · Gq · Gins · Cins · Ains. **Cins = 1,2** (Widerstandsbeiwert Isolatorketten). Gins = Gt oder Gpol.
- **Gittermasten (4.2.2.4.3)**: QWt-Formel mit Ct1/Ct2, At1/At2; Völligkeitsgrad **χ = At / (h·(b1+b2)/2)**. **Gt = 1,05 für Gittermasten unter 60 m** (über 60 m gesondert ermitteln). Anströmen über Eck zu berücksichtigen.
- **Einstielige Masten (4.2.2.4.4)**: QWpol = qh · Gq · Gpol · Cpol · Apol. **Cpol für Holzmaste ≈ 0,8**; **Gpol für selbsttragende einstielige Stahlmasten ≈ 1,15**.

##### Tabelle 4.2.5 — Spannweitenbeiwerte Gc je Geländeart (L = Windspannweite in m)
| Geländeart | Formel | 100 m | 200 m | 300 m | 400 m | 600 m | 800 m |
|---|---|---|---|---|---|---|---|
| I | 1,30 − 0,073·ln(L) | 0,96 | 0,91 | 0,88 | 0,86 | 0,83 | 0,81 |
| II | 1,30 − 0,082·ln(L) | 0,92 | 0,87 | 0,83 | 0,81 | 0,78 | 0,75 |
| III | 1,30 − 0,098·ln(L) | 0,85 | 0,78 | 0,74 | 0,71 | 0,67 | 0,65 |
| IV | 1,30 − 0,110·ln(L) | 0,79 | 0,72 | 0,67 | 0,64 | 0,60 | 0,57 |

#### 4.2.3 Eislasten
- Zwei Hauptarten: Eisbildung aus Niederschlägen (nasser Schnee / Klareis) und in Nebel/wasserhaltiger Luft (weicher / harter Reif). Meteorologische Details: IEC 61774.
- Eislast Leiter: **QI = I · ½(Lw1 + Lw2)** (längenbezogene Eislast × Gewichtsspannweiten).

#### 4.2.4 Gleichzeitige Wind- und Eislasten
- (a) Extreme Eislast γI·QIK + mäßige Windlast ΨW·QWk (mäßige Windlast = **0,55–0,65×** der 50-Jahres-Windgeschwindigkeit je Eisart); **ΨW = 0,4**.
- (b) Hohe Windgeschwindigkeit + mäßige Eislast; hohe Windgeschwindigkeit = **0,7–0,85×** der extremen; **ΨI = 0,35**.

##### Tabelle 4.2.6 — Windwiderstandsbeiwerte CcI und Eisdichten ρI (kg/m³)
| Eisart | Nasser Schnee | Klareis | Weicher Reif | Harter Reif |
|---|---|---|---|---|
| CcI | 1,0 | 1,0 | 1,2 | 1,1 |
| ρI | 500 | 900 | 300 | 700 |
- Äquivalenter Durchmesser vereister Leiter: **D = √(d² + 4·I/(π·ρI·9,81))**; π = 3,1416.

#### 4.2.5 Temperatureinwirkungen
- Fünf Auslegungssituationen (a–e). **Bei Eisansatz für beide Hauptarten Temperatur 0 °C** annehmbar (sofern nicht anders festgelegt).

#### 4.2.6 Lasten aus Errichtung und Instandhaltung
- Charakteristische Errichtungs-/Instandhaltungslast auf Querträger **≥ 1,0 kN**.
- Begehbare Stäbe mit Neigung **< 30° zur Waagrechten**: charakteristische Last **1,0 kN lotrecht in Stabmitte** (ohne andere Lasten).
- Steigsprossen: konzentrierte charakteristische Last **1,0 kN lotrecht** an statisch ungünstiger Position.

#### 4.2.7 Lasten im Hinblick auf die Betriebssicherheit
- (a) Torsionslasten: statische Restlast aus Wegfall der Zugkraft eines Leiters/Teilleiters/Erdseils im angrenzenden Feld; Berechnung bei üblicher Umgebungstemperatur ohne Wind/Eis.
- (b) Längslasten: an allen Leiterbefestigungspunkten gleichzeitig.
- Alternativ: Betriebssicherheitslast = **AK = β · T0** (β = Abminderungsbeiwert Leiterzugkraft, T0 = Anfangshorizontalzugkraft). Begrenzung möglich durch Rutschklemmen.

#### 4.2.10 Lastfälle
- Ideelle Spannweite: **LR = √(ΣLn³ / ΣLn)**.

##### Tabelle 4.2.7 — Standardlastfälle
- **1a** extreme Windlast (4.2.2); **1b** Windlast bei niedrigster Temperatur.
- **2a** gleichförmige Eislast alle Felder; **2b** gleichförmig, Biegung quer; **2c** ungleichförmig, Biegung längs; **2d** ungleichförmig, Biegung + Torsion (4.2.3).
- **3** kombinierte Wind- und Eislast (4.2.4).
- **4** Errichtungs-/Instandhaltungslasten (4.2.6).
- **5a** Betriebssicherheit Biegung+Torsion; **5b** Betriebssicherheit Längslasten (4.2.7).
- **Empfohlene Abminderungsbeiwerte (NNA-Default):** α = 0,5; α1 = 0,3; α2 = 0,7; α3 = 0,3; α4 = 0,7.

##### Tabelle 4.2.8 — Teilsicherheits-/Kombinationsbeiwerte (Grenzlastzustände)
| Einwirkung | Symbol | Stufe 1 | Stufe 2 | Stufe 3 |
|---|---|---|---|---|
| Windlast | γW | 1,0 | 1,2 | 1,4 |
| Windlast | ΨW | 0,4 | 0,4 | 0,4 |
| Eislast | γI | 1,0 | 1,2 | 1,4 |
| Eislast | ΨI | 0,35 | 0,35 | 0,35 |
| Instandhaltungs-/Errichtungslasten | γP | 1,5 | — | — |
| Eigengewicht (ständig) | γG | 1,0 | — | — |
| Betriebssicherheit (Torsion γA1 / Längs γA2) | γA1, γA2 | 1,0 | — | — |

### 4.3 Einwirkungen — empirische Vorgehensweise (für Österreich maßgebend)
- (ncpt) AT.1: Tragwerke zu bemessen für: (1) Eigengewicht Tragwerk, (2) ständige Lasten, (3) Zusatzlasten, (4) Montagelasten, (5) Windlasten, (6) Leiterzüge.

#### 4.3.2 Windlasten (empirisch)
- QWx = qx · Cx · A (Maste/Querträger/Isolatoren); Leiter: QWc = qc · Gc · Cc · d · L · cos²φ.
- Staudruck **q = ½ · ρ · Vh²**; empfohlener Wert **ρ = 1,25 kg/m³ bei 10 °C**.
- Spannweitenbeiwert Gc: **= 1,0 für Spannweiten bis 200 m**; **= 0,6 + 80/L für Spannweiten über 200 m**.
- **(A-dev/ncpt) AT.3 — Winddruck Tabelle 4.3.2/AT.3** (Basis: Windgeschwindigkeit **120 km/h**, Staudruck **695 N/m²**):

| Bauteile | c | cx·q120 (N/m²) | Abminderungsfaktor |
|---|---|---|---|
| volle ebene Flächen | 1,6 | 1112 | 1 |
| aus Winkelprofilen | 1,4 | 973 | 1 |
| ebene Fachwerkwände aus Rohren | 1,1 | 765 | 1 |
| Holz-/Stahlrohr-/Stahlbetonmaste, kreisförmiger Querschnitt | 0,7 | 487 | 1 |
| Stahlrohr-/Stahlbetonmaste, sechs-/achteckiger Querschnitt | 1,0 | 695 | 1 |
| Doppelmaste Holz, in Stangenebene | 0,7 | 487 | 1 |
| Stahl/Stahlbeton rechtwinkelig zur Stangenebene (e < dm) | 0,8 | 556 | 1 |
| Drähte/Seile kreisförmig/elliptisch, d < 15,8 mm | 1,15 | 600 | 0,75 |
| Drähte/Seile, d > 15,8 mm | 1,0 | 521 | 0,75 |
| Warnkugeln/Radarmarker (Rotationskörper), d < 1,0 m | 0,4 | 278 | 1 |
(e = innerer Abstand Einzelstangen; dm = mittlerer Stangendurchmesser)

- (ncpt) AT.5: Ebene Flächen/Fachwerkwände in Windrichtung dürfen vernachlässigt werden.
- (ncpt) AT.6: Anströmen über Eck auf gleichseitig-dreieckige/quadratische Stahlgittermaste = **Zweifaches** der Windkraft bei senkrechter Anströmung einer Mastwand (Rückwände berücksichtigt).
- (ncpt) AT.7 — **Tabelle 4.3.2/AT.7, Windlast auf im Windschatten liegende Bauteile:**
  - Rückwand Fachwerkmaste/-ausleger: **80 %** der Windkraft auf vordere Fläche.
  - A-Maste (hintere Stange): **50 %** der Windkraft auf vordere Stange.
  - Bündelleiter, abgekehrte Einzelleiter: **80 %** der Windkraft auf vorderen Leiter.
  - Abhängig vom lichten Abstand x und Breite B: x < B → keine Windlast; x = B bis 20B → **50 %**; x > 20B → **100 %**.
- (snc) AT.8: Spannweitenbeiwert Gc = 1,0.
- (snc) AT.9 — Vh-Ermittlung: für Höhen **über 15 m bis 40 m** über Grund mindestens **33,33 m/s (120 km/h)**; für Höhen **unter 15 m** dürfen Cx·q120-Werte um **30 % vermindert** werden; für Höhen **über 40 m** je angefangene **50 m** zusätzlicher Höhe um **30 % vergrößern**.

#### 4.3.3 Eislasten (empirisch, A-dev)
- Unterscheidung „normale" und „erhöhte Eislast" (erhöhte gilt, wenn regelmäßig auftretend, kann Vielfaches der normalen sein).
- (A-dev) AT.2 Mindestannahmen Leiter (auch Erdseile/OPGW):
  - **Regelzusatzlast = (4 + 0,2·d) N/m** (d = Leiterdurchmesser in mm).
  - **Ausnahmszusatzlast (N/m): Gruppe II = 35; Gruppe III = 40; Gruppe IV = 50.**
- (snc) AT.3 — **Tabelle 4.3.3/AT.3, Zusatzlasten/Eislasten Tragwerke und Ausrüstungen:**

| Bauteil | Regelzusatzlast | Ausnahmszusatzlast |
|---|---|---|
| Isolatorketten aus Glas/Porzellan | ≥ 20 % des Eigengewichts | ≥ 40 % des Eigengewichts |
| Mastkörper | keine | keine |
| Ausleger aus Stahlprofilen | ≥ 40 % des Eigengewichts | ≥ 80 % des Eigengewichts |
| Ausleger aus anderem Material | ≥ 120 N/m² auf Gesamtoberfläche | ≥ 250 N/m² auf Gesamtoberfläche |
| Warnkugeln/Radarmarker | ≥ 120 N/m² auf Gesamtoberfläche | ≥ 250 N/m² auf Gesamtoberfläche |
(Für Verbundisolatorketten ggf. höhere Prozentsätze.)

#### 4.3.5 Temperatureinwirkungen (empirisch)
- **Mit Eiszuständen angenommene Temperatur = −5 °C** (Mittelwert des Temperaturbereiches, in dem Eis auftreten kann).

#### 4.3.6 Lasten aus Errichtung/Instandhaltung (empirisch)
- (ncpt) AT.1 Montagelast alternierend als Einzellast **≥ 1000 N lotrecht**:
  (1) bei Auslegern, die mehr als **1,2 m** auskragen, am Auslegerende;
  (2) bei Horizontalstäben der Auslegeruntergurtebene in freier Stabmitte (Auslegerobergurte nicht auf Montagelast bemessen);
  (3) Bereiche mit Steighilfen (Leitern/Steigsprossen) → keine Montagelast-Bemessung;
  (4) alle horizontalen Stäbe der Tragwerkskörper in freier Stabmitte.
  Bei (1)/(2) übrige Regellastfall-Belastungen gleichzeitig; bei (3)/(4) nicht. Holzmaste: Mastkörper ohne Montagelast.

#### 4.3.8 Kurzschlusslasten (empirisch)
- (ncpt) AT.1: **Kurzschlusslasten sind nicht zu berücksichtigen.**

#### 4.3.10 Lastfälle (empirisch)
- (A-dev) 4.3.7 AT.1: Betriebssicherheitslasten sind durch Ausnahmslastfälle nach 4.3.10 abgedeckt, keine zusätzliche Berücksichtigung.

##### Tabelle 4.3.1 — Lastfälle für die Leiterzugkräfte
| Lastfall | Temperatur °C | Last |
|---|---|---|
| normal | −5 | Leitereigengewicht + normale (bzw. erhöhte) Eislast |
| normal | −20 | Leitereigengewicht |
| normal | +15 | Leitereigengewicht + größte Windlast |
| normal | +40 | Leitereigengewicht |
- Anmerkung 2: Bei Freileitungen mit hohen Strömen auch im Sommer höhere Leitertemperatur berücksichtigen, **z. B. +60 °C**; max. Leitertemperatur in Projektspezifikation.
