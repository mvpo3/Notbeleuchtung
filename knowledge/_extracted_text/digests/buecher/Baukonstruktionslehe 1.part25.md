# Baukonstruktionslehe 1 — Teil 25
> Quelle: Baukonstruktionslehe 1 (buecher) · Seiten 1001-1040.

Dieser Teil behandelt zwei grosse bauliche Schutzdomaenen: Schallschutz (Trittschall-Messkunde, Flankenübertragung, Anforderungsnormen) und baulichen Brandschutz (Baustoff- und Bauteilklassifizierung, Gebäudeklassen, konstruktive Schutzmaßnahmen für Stahl, Stahlbeton, Mauerwerk und Holz, Leitungsführung, Verglasungen). Am Ende beginnt das Kapitel über Gesundheitsschutz (gefährliche Stoffe, Radon).

## Inhalt

### 17.6 Schallschutz — Trittschall: Messkunde und Berechnungsverfahren

#### Deckenarten und ihre Eignung

- Stahlbetonplatten ab mindestens 160 mm Dicke mit schallbrückenfreiem schwimmendem Estrich bieten ausreichenden Luft- und Trittschallschutz.
- Stahlbeton-Rippendecken und Decken mit Füllkörpern oder Hohlräumen: Dämmwirkung nur sicher wenn die Ausführung genau nach DIN 4109 erfolgt.
- Unterdecken verbessern Trittschallschutz nur begrenzt; merkliche Wirkung nur bei dichter Ausführung. Unterdecken mit Verbundestrich können nahe an schwimmenden Estrich herankommen.
- Holzbalkendecken in herkömmlicher Form: kein ausreichender Schallschutz. Als zwei- oder mehrschalige Konstruktionen mit Beschwerung (aufgelegte Betonsteine, schwimmender Zementestrich) erreichbar; Details in Kap. 10.

#### Trittschallmessung mit Norm-Hammerwerk

- Norm-Hammerwerk simuliert Gehbelastung durch definierte Gewichte, die aus definierter Höhe auf den Bodenbelag fallen.
- Gemessen werden im Empfangsraum:
  - Schallpegel L₀ durch Norm-Hammerwerk-Anregung
  - Nachhallzeit T₂ des Empfangsraums (zur Berücksichtigung der Schallabsorption)
  - Störschallpegel B₂ ohne Hammerwerk-Immission (muss herausgerechnet werden wenn wesentlich)
- Mehrere Hammerwerk-Stellungen + mehrere Mikrofon-Positionen → Mittelwertbildung ergibt Trittschallpegel L₀.

#### Norm-Trittschallpegel L'n

Der normierte Trittschallpegel korrigiert den gemessenen Wert um die Schallabsorption des Empfangsraums:

**L'n = L₀ − 10 · lg(A/A₀)**

Dabei:
- L'n = Norm-Trittschallpegel
- L₀ = gemessener Trittschallpegel
- A = äquivalente Schallabsorptionsfläche des Empfangsraums; ermittelt aus Nachhallzeit: A = 0,163 · V/T
- A₀ = Bezugs-Absorptionsfläche = 10 m²
- V = Volumen des Empfangsraums
- T = Nachhallzeit

#### Bewerteter Norm-Trittschallpegel L'n,w nach DIN EN ISO 717-2

- 16 Messwerte bei 16 Frequenzen (100 bis 3150 Hz, Terzbänder) werden ermittelt.
- Bezugskurve (DIN EN ISO 717-2) wird vertikal in 1-dB-Schritten verschoben bis folgende Bedingung gilt: Summe der ungünstigen Differenzen (Messkurve liegt über Bezugskurve) maximal 32 dB.
- L'n,w = Bezugskurvenwert bei f = 500 Hz der verschobenen Bezugskurve.
- Berechnungsbeispiel: Verschiebung um 15 dB → ungünstige Abweichung 29 dB (zulässig); Verschiebung um 16 dB → 38 dB (überschritten); daher 15 dB gültig → L'n,w = 45 dB.
- Wichtig: Hohe L'n,w-Werte sind ungünstig (im Gegensatz zu Rw). Bezugskurve nach unten verschieben = Verbesserung = positives Trittschallschutzmaß TSM.
- DIN 4109 nennt Trittschallschutzmaß TSM in Klammern hinter den L'n,w-Werten.
- Unterschied zu Rw: Bei Rw zählen Differenzen wo Messkurve unter Bezugskurve; bei L'n,w zählen Differenzen wo Messkurve über Bezugskurve (ungünstig).

#### Bewertete Trittschallminderung ΔLw (Verbesserungsmaß)

- Messgröße für den Verbesserungseffekt von Deckenauflagen (schwimmende Böden, weichfedernde Gehbeläge).
- Definition nach DIN EN ISO 717-2:2021-05: Differenz der L'n,w-Werte ohne und mit Deckenauflage, bezogen auf eine Referenz-Rohdecke (~120 mm homogene Stahlbetondecke).
- Achtung: Das Verbesserungsmaß gilt nur für die Referenzdecke; auf anderen Rohdecken kann der tatsächliche Effekt abweichen.
- Berechnungsformel nach DIN 4109-2:2018-01 für Massivdecken mit schwimmendem Boden:

  **L'n,w = Ln,eq,0,w − ΔLw + K**

  Dabei ist Ln,eq,0,w der äquivalente bewertete Norm-Trittschallpegel der Massivdecke, ΔLw das Verbesserungsmaß der Auflage, K Korrekturwert für Flankenübertragung und Unterdecken.

- Für andere Übertragungssituationen (nicht direkt darunter liegender Raum):

  **L'n,w = Ln,eq,0,w − ΔLw − KT**

  KT-Wert: Empfangsraum neben oder schräg unter Senderaum = 5 dB; mit einem Zwischenraum = 10 dB.

- Holzbalkendecken: Keine separate Berücksichtigung von Verbesserungsmaßen für Auflagen. Stattdessen Ln,w der Gesamtkonstruktion aus Bauteilkatalog DIN 4109-33:2016-07 oder Prüfberichten. Flankenkorrekturwerte K₁ (Weg Df) und K₂ (Weg DFf) nach Tabellen 3 und 4 in DIN 4109-2:2018-01:

  **L'n,w = Ln,w + K₁ + K₂**

- Regel: Mehrere gleichzeitige Trittschallverbesserungsmaßnahmen sind NICHT addierbar. Maßgebend ist in der Regel das stärkste Einzelmaß; bei etwa gleich wirkenden Maßnahmen ggf. geringe Zusatzverbesserung messbar, aber DIN 4109 lässt rechnerische Berücksichtigung nicht zu.

### 17.6.2.3 Schallnebenwege (Flankenübertragung)

- Flankenübertragung = Schallübertragung vom Senderaum in den Empfangsraum über Nebenwege an Anschlüssen des Trennbauteils an andere Bauteile.
- Übertragungswege: Ff (Flanke → Flanke), Df (direkt → Flanke), Fd (Flanke → direkt).
- Besonders relevant: Skelettbau, leichte Trennwände (GK-Ständerwände), aber auch in Massivbauten über leichte Außenwände (Porenbeton) oder Dachdecke.
- Häufig in der Praxis: Flankenübertragung bei Planung ignoriert → tatsächlicher Schallschutz weit unter Anforderung.
- DIN 4109-1 und DIN 4109-2 (Version 2018-01) geben dem Thema deutlich höhere Aufmerksamkeit als früher.
- Berechnung resultierendes Schalldämm-Maß R'w unter Berücksichtigung aller Übertragungswege:

  R'w = −10 · lg[10^(−RDd,w/10) + Σ 10^(−RFf,w/10) + Σ 10^(−RDf,w/10) + Σ 10^(−RFd,w/10)]

  Bei üblicher Situation (1 Trennbauteil + 4 Flanken) → 13 Übertragungswege zu berücksichtigen.

- Abhilfemaßnahmen bei kritischen Flanken: höhere Masse der Flanke, Vorsatzschalen (z.B. abgehängte Decke vor leichter durchlaufender Dachkonstruktion), entkoppelnde Anschlüsse.

### 17.6.2.4 Schalldämmung zusammengesetzter Bauteile

- Schall gelangt auch über Einbauten (Türen, Fenster) in den Empfangsraum.
- Schallleistung (Einheit Watt) = Energie, proportional dem Quadrat des Schalldrucks × Fläche.
- Formel für resultierendes Schalldämm-Maß aus n Teilflächen (DIN 4109-2:2018-01):

  Rres = −10 · lg(S₁/Sges · 10^(−0,1·R₁) + S₂/Sges · 10^(−0,1·R₂) + ... + Sn/Sges · 10^(−0,1·Rn))

  Sges = Summe aller schallübertragenden Bauteilflächen in m².

- **Rechenbeispiel Wand mit Tür:**
  - Wand: S₁ = 20 m², Rw,1 = 50 dB
  - Tür: S₂ = 2 m², Rw,2 = 35 dB
  - Resultierendes Rw,ges = ca. 44 dB
  - Wand auf 60 dB verbessern → Rw,ges nur auf ca. 45,3 dB
  - Tür auf 45 dB verbessern → Rw,ges auf ca. 49,2 dB
  - Fazit: Schwachstelle (Tür/Fenster) ist entscheidend, nicht die Hauptfläche.

### 17.6.3 Schallschutzanforderungen und Normen

Relevante Regelwerke:
- DIN 4109 „Schallschutz im Hochbau" (Hauptnorm)
- DIN 18005 „Schallschutz im Städtebau"
- Flugplatz-Schallschutzmaßnahmenverordnung
- Bundesimmissionsschutzgesetz + TA Lärm

DIN 4109 enthält:
- Teil 1 (DIN 4109-1:2018-01): Mindestanforderungen für Luft- und Trittschallschutz, gebäudetechnische Anlagen, raumlufttechnische Anlagen, Trinkwasserinstallation
- Teil 2 (DIN 4109-2:2018-01): Berechnungsverfahren
- Teil 4 (DIN 4109-4:2016-07): Eignungsprüfungen, Messverfahren (DIN EN ISO 10140 im Prüfstand, DIN EN ISO 16283-1 in ausgeführten Bauten)
- Teil 5 (DIN 4109-5:2020-08): Erhöhte Anforderungen (entspricht weitgehend früherem Beiblatt 2)
- Bauteilkataloge: DIN 4109-31 bis DIN 4109-36 (nach Bauweisen und Bauteilen)

Praxishinweis: Norm DIN 4109 spiegelt nicht immer den Stand der Technik wider. Beispiel: 25 % der Bewohner empfinden ihr Haus noch als hellhörig bei R'w = 55 dB Wohnungstrenndecke, obwohl die Norm nur 54 dB fordert.

**VDI-Richtlinie 4100** — Ergänzung zur Norm für Wohnnutzung:
- 3 Schallschutzstufen (SSt I, II, III)
- SSt I ≈ DIN 4109-1 Mindestanforderungen
- SSt II ≈ DIN 4109-5 erhöhter Schallschutz
- SSt III = höchstes Ruhemaß für Bewohner
- Kostenunterschiede und Ausführungshinweise enthalten; noch nicht in Landesbauordnungen übernommen.

**Rechtliche Hinweise:** Positive Vermarktungsadjektive (komfortabel, luxuriös) können Rechtsanspruch auf erhöhtes Schallschutzniveau (DIN 4109-5, VDI 4100) begründen.

#### Tabelle Mindestanforderungen (Auswahl aus DIN 4109-1:2018-01) und erhöhte Anforderungen (DIN 4109-5:2020-08)

| Bauwerk / Bauteil | Luft erf. R'w [dB] (Min.) | Luft erf. R'w [dB] (Erhöht) | Tritt erf. L'n,w [dB] (Min.) | Tritt erf. L'n,w [dB] (Erhöht) |
|---|---|---|---|---|
| **Mehrfamilienhäuser, Bürogebäude, gemischt genutzte Gebäude** | | | | |
| Decken | 54 | 57 | 50 | 45 |
| Wände | 53 | 56 | – | – |
| Treppen | – | – | 53 | ≤47 |
| Türen (Hausflur/Flur) | 27 | 32 | – | – |
| **Einfamilien-Doppel- und -Reihenhäuser** | | | | |
| Decken | – | – | 41 | 36 |
| Haustrennwände | 62 | 67 | – | – |
| Treppen | – | – | 46 | 41 |
| **Hotels und Beherbergungsstätten** | | | | |
| Decken | 54 | 57 | 50 | 45 |
| Wände | 47 | 52 | – | – |
| Treppen | – | – | 58 | 48 |
| Türen | 32 | 37 | – | – |
| **Krankenhäuser, Sanatorien** | | | | |
| Decken | 54 | 57 | 53 | 46 |
| Wände zwischen Krankenräumen | 47 | 52 | – | – |
| Treppen | – | – | 58 | 48 |
| Türen zw. Fluren und Krankenräumen | 32 | 37 | – | – |
| **Schulen** | | | | |
| Decken | 55 | – | 53 | – |
| Wände zw. Unterrichtsräumen und Fluren | 47 | – | – | – |
| Wände zw. Unterrichtsräumen und Treppenhäusern | 52 | – | – | – |
| Türen zw. Unterrichtsräumen und Fluren | 32 | – | – | – |

#### 17.6.3.2 Schallschutz bei gebäudetechnischen Anlagen

- DIN 4109-1, Kapitel 9: maximal zulässige Schalldruckpegel in fremden schutzbedürftigen Räumen (abhängig von Schallquelle und Raumnutzung).
- Kapitel 11: Anforderungen an Armaturen und Geräte der Trinkwasser-Installation.
- Kapitel 8: gilt wenn LAF,max häufig > 75 dB oder häufigere/größere Körperschallanregungen als in Wohnungen → Anforderungen an R'w von Decken/Wänden sowie L'n,w zu schutzbedürftigen Räumen.
- Kapitel 10: Anforderungen an maximalen Schalldruckpegel durch raumlufttechnische Anlagen in der eigenen Wohnung.

#### 17.6.3.3 Schutz gegen Außenlärm

**Maßgeblicher Außenlärmpegel:**
- Wird für Tag (06:00–22:00 Uhr) und Nacht (22:00–06:00 Uhr) getrennt ermittelt.
- Beurteilungspegel + 3 dB = maßgeblicher Außenlärmpegel (Straßen-, Schienen-, Wasserverkehr, Industrie/Gewerbe).
- Nachts zusätzlich +10 dB Zuschlag. Jeweils maßgebend ist der höhere Pegel.
- Ausnahme: Nicht regelmäßig zum Schlafen genutzte Räume (z.B. privates Arbeitszimmer) → nur Tagpegel maßgebend.

**Ermittlung der Beurteilungspegel:**
- Straßen- und Wasserverkehr: Nomogrammverfahren nach DIN 18005-1:2002-07 zulässig; aufwändigere Berechnung nach RLS-19 ebenfalls möglich (notwendig bei Topographie-Einflüssen, Lärmschutzwände/-wälle).
- Schienenverkehr: Beurteilungspegel nach 16. BImSchV (detailliertere Berechnung).
- Fluglärm aus Fluglärmschutzbereichen nach FluLärmG: Anforderungen aus 2. FlugLSV (Flugplatz-Schallschutzmaßnahmenverordnung), basierend auf äquivalentem Dauerschallpegel LAeq.
- Bei mehreren Lärmquellen: energetische Summation; 3-dB-Zuschlag nur einmal auf Summenpegel.

**Erforderliches Schalldämmmaß R'w,ges:**
- Formel: R'w,ges = La − KRaumart
  - KRaumart = 25 dB für Bettenräume in Krankenanstalten/Sanatorien
  - KRaumart = 30 dB für Aufenthaltsräume in Wohnungen, Übernachtungsräume in Beherbergungsstätten, Unterrichtsräume
  - KRaumart = 35 dB für Büroräume
- Mindest-R'w,ges: 35 dB für Bettenräume; 30 dB für Wohnungen, Büros, Unterrichtsräume.
- Korrektur KAL für Verhältnis schallübertragende Außenfläche Ss zu Grundfläche SG nach DIN 4109-2.

**Abminderung bei abgewandten Gebäudeseiten:**
- Abgewandte Seite bei offener Bebauung: −5 dB
- Abgewandte Seite bei geschlossener Bebauung: −10 dB

**Berechnung R'w,ges der Außenbauteile:**
- Formel gemäß DIN 4109-2:2018-01:
  R'w,ges = −10 · lg(Σ 10^(−Re,i,w/10))
  Dabei Re,i,w = auf Fassadenfläche bezogenes Schalldämm-Maß jedes einzelnen Bauteils/Elements (Wand, Fenster, Dach, Rollladenkasten, Lüftungselement).

**Flankenübertragung bei Außenbauteilen:**
- Berücksichtigen wenn: biegesteife Fassadenbauteile (Beton/Mauerwerk) mit anderen biegesteifen Bauteilen verbunden, Schalldämm-Maß massives Außenbauteil ≥50 dB, erforderliches R'w,ges > 40 dB.
- Nicht berücksichtigen: wenn Bedingungen nicht erfüllt oder Holz-/Leicht-/Trockenbauweise oder Metall-Glas-Fassaden.

**Schwachstellen bei Außenbauteilen:** Fenster und Türen, Rolllädenkästen, Lüftungseinrichtungen (VDI 2719 beachten).

**Schallschutzfenster:**
- Angegebene Rw-Werte sind Labor-Dämmmaße.
- Einbau erfordert besondere Sorgfalt bei Dichtheit der Anschlussfugen.
- Lüftungsmöglichkeiten bei Erhaltung der Schallschutzwerte sicherstellen.
- Fensterdichtungen regelmäßig prüfen und bei Alterung ersetzen.

**Außenwand mit Wärmedämmung:**
- Zusätzliche Wärmedämmschicht (Innendämmung oder WDVS außen) kann Dämmwerte um 3 bis 6 dB verschlechtern (Resonanzerscheinungen der Putzschale auf Dämmschichten mit zu hoher dynamischer Steifigkeit s').
- Abhilfe: Mineralwolle oder elastifiziertes Polystyrol mit niedrigeren s'-Werten → Verschlechterung vermeidbar oder sogar Verbesserung erreichbar.

---

### 17.7 Baulicher Brandschutz

#### 17.7.1 Allgemeines

**Schutzziele der Muster-Bauordnung (MBO § 14):** Bauliche Anlagen so ausführen, dass Brandenstehung und Brandausbreitung (Feuer + Rauch) vorgebeugt wird, und bei Brand Rettung von Menschen/Tieren sowie wirksame Löscharbeiten möglich sind.

**Brandschutzarten:**
- Baulicher Brandschutz: Bauwerksplanung + konstruktive Ausbildung
- Anlagentechnischer Brandschutz: Brandmeldeanlage (BMA), Löschanlagen, Rauch- und Wärmeabzugsanlagen (RWA), Überdrucklüftung, Handfeuerlöscher, Wandhydranten
- Organisatorischer Brandschutz: Betriebsfeuerwehren, Unterweisungen, Brandschutz- und Alarmpläne, Prüfungen, Brandschutzordnungen
- Abwehrender Brandschutz: Öffentliche Feuerwehr, Löschwasserversorgung und -rückhaltung

**Einzelmaßnahmen baulicher Brandschutz:**
- Gebäudehöhe und Lage auf Grundstück / zur Nachbarbebauung
- Lage und Ausbildung der Rettungswege
- Anordnung, Lage und Größe von Brandabschnitten und Nutzungseinheiten
- Brandverhalten von Baustoffen + Feuerwiderstandsdauer von Bauteilen

**Zufahrten für Feuerwehr:** Aufstell- und Bewegungsflächen gemäß DIN 14090.

**Bebauungsarten (brandschutztechnisch):**
- Offene Bauweise: Gebäudeabstände (Abstandsflächen gem. § 6 MBO) verhindern Feuerübertritt.
- Geschlossene Bauweise: Brandübertritt an direkt angrenzenden Gebäuden durch Brandwände verhindert.

**Brandabschnitte:**
- Ab gewisser Gebäudeausdehnung erforderlich.
- Definition Nutzungseinheit: geschossweise abgegrenzte Nutzfläche einer Wohnung oder Büro-/Verwaltungsnutzung; jede Wohnung = eine Nutzungseinheit ohne weitere Abschnittsbildung. Serverräume, Technik- oder Brennstofflagerräume müssen abgeschottet werden.

**Sonderbauvorschriften** gelten für: Hochhäuser, Gast- und Beherbergungsstätten, Versammlungsräume, Verkaufsstätten, Schulen, Krankenhäuser, Industriebau (DIN 18230). Können sowohl schärfere Anforderungen als auch Erleichterungen (größere Brandabschnitte, längere Fluchtwege) ermöglichen.

#### 17.7.2 Begriffe und Klassifizierung

##### Baustoffklassen nach DIN 4102-1 (deutsches System)

- Klasse A: nicht brennbar (A1 und A2)
- Klasse B1: schwer entflammbar
- Klasse B2: normal entflammbar
- Klasse B3: leicht entflammbar — Verwendung nach § 26(1) MBO unzulässig, sofern nicht in Verbindung mit anderen Baustoffen nicht leichtentflammbar

Kennzeichnungspflicht für alle am Bau verwendeten Bauprodukte hinsichtlich Baustoffklasse.

##### Euroklassen nach DIN EN 13501-1 (europäisches System)

Ablösung des deutschen Systems durch EU-Klassifizierung (nach Koexistenzphase).

Sieben Euroklassen für Bauprodukte (A1–F), separat für Bodenbeläge (Afl–Ffl) und Rohrisolierungen (AL–FL).
Zusätzliche Klassifizierungen für Brandparallelerscheinungen:
- s (smoke): s1 (wenig Rauch), s2 (mittlere), s3 (starke Rauchentwicklung)
- d (droplets): d0 (kein brennendes Abtropfen), d1, d2

| Euroklasse | DIN 4102-1 Entsprechung | Bauaufsichtliche Bezeichnung |
|---|---|---|
| A1 | A | Nicht brennbar |
| A2 (mit s1,d0 bis s3,d2) | A | Nicht brennbar |
| B (mit s1,d0 bis s3,d2) | B1 | Schwer entflammbar |
| C (mit s1,d0 bis s3,d2) | B1 | Schwer entflammbar |
| D (mit s1,d0 bis s3,d2) | B2 | Normal entflammbar |
| E, E-d2 | B2 | Normal entflammbar |
| F | B3 | Leicht entflammbar |

Prüfungen gemäß DIN EN 1363 bis DIN EN 1366. Nicht geregelte Bauprodukte benötigen: Zulassung des DIBt, allgemeines bauaufsichtliches Prüfzeugnis oder Zustimmung im Einzelfall (ZiE). Europäische Produkte müssen CE-Kennzeichnung tragen.

##### Feuerwiderstandsklassen nach DIN 4102-2

Klassen F30, F60, F90, F120, F180 (Ziffer = Feuerwiderstandsdauer in Minuten).

Kombinierte Bezeichnung Feuerwiderstandsklasse + Baustoffklasse:
- F90-A = feuerbeständig + aus nicht brennbaren Baustoffen
- F90-AB = feuerbeständig + wesentliche Teile aus nicht brennbaren Baustoffen
- F90-B = feuerbeständig + aus brennbaren Baustoffen
- F90-BA = feuerbeständig + wesentliche Teile aus brennbaren Baustoffen, ummantelt mit nicht brennbaren

Wesentliche Teile = alle tragenden/aussteifenden Teile; bei raumabschließenden Bauteilen auch eine in Bauteilebene durchgehende Schicht (bei Decken: Mindestgesamtdicke 50 mm).

**Bauaufsichtliche Benennungen:**
- Feuerhemmend = F30
- Hochfeuerhemmend = F60
- Feuerbeständig = F90 (Bauteile mit wesentlichen Teilen aus B sind NICHT als feuerbeständig anzusehen)

##### Feuerwiderstandsklassen für Sonderbauteile (DIN 4102)

| Bauteil | Norm | Klassen (30–180 min) |
|---|---|---|
| Wände, Decken, Stützen | Teil 2 | F30–F180 |
| Brandwände | Teil 3 | – |
| Nichttragende Außenwände, Brüstungen | Teil 3 | W30–W180 |
| Feuerschutzabschlüsse (Türen, Tore, Klappen) | Teil 5 | T30–T180 |
| Brandschutzverglasungen strahlungsundurchlässig | Teil 13 | F30–F120 |
| Brandschutzverglasungen strahlungsdurchlässig | Teil 13 | G30–G120 |
| Rohre/Formstücke für Lüftungsleitungen | Teil 6 | L30–L120 |
| Absperrvorrichtungen Lüftungsleitungen | Teil 6 | K30–K90 |
| Kabelabschottungen | Teil 9 | S30–S180 |
| Installationsschächte und -kanäle | Teil 11 | I30–I120 |
| Rohrdurchführungen | Teil 11 | R30–R120 |
| Funktionserhalt elektrischer Leitungen | Teil 12 | E30–E90 |

##### Europäisches Klassifizierungssystem DIN EN 13501 (eingeführt ab Bauregelliste 2002/1)

Leistungskriterien:
- R = Tragfähigkeit (Résistance)
- E = Raumabschluss (Étanchéité)
- I = Wärmedämmung (Isolation)
- W = Begrenzung Strahlendurchtritt (Radiation)
- M = Stoßbeanspruchung (Mechanical)
- S = Rauchdichtheit (Smoke) — für Rauchschutztüren, Lüftungsanlagen inkl. Klappen
- C = Selbstabschließend (Closing) — für Rauchschutztüren, Feuerschutzabschlüsse, Förderanlagen
- K = Brandschutzfunktion — für Brandschutzbekleidungen
Minutenangaben: 10, 15, 20, 30, 45, 60, 90, 120, 180, 240, 360

**Entsprechungen DIN 4102 ↔ DIN EN 13501:**

| Bauaufsichtliche Bezeichnung | Tragende Bauteile ohne Raumabschluss | Mit Raumabschluss | Nichttragende Außenwände | Nichttragende Innenwände | Brandschutztüren | Rauchschutztüren |
|---|---|---|---|---|---|---|
| Feuerhemmend | R 30 (F30) | REI 30 (F30) | E 30 (W30) | EI 30 (F30) | EI2 30 (T30) | CS200 (T30 RS) |
| Hochfeuerhemmend | R 60 (F60) | REI 60 (F60) | E 60 (W60) | EI 60 (F60) | EI2 60 (T60) | CS200 (T60 RS) |
| Feuerbeständig | R 90 (F90) | REI 90 (F90) | E 90 (W90) | EI 90 (F90) | – | – |
| 120 min | R 120 (F120) | REI 120 (F120) | – | – | – | – |
| Brandwand | – | REI-M 90 | – | EI-M 90 | – | – |

Brandschutzverglasungen nach europäischem Recht: keine eigenständigen Bauteile, sondern Teil der Wand/Decke.

##### Gebäudeklassen gemäß Musterbauordnung (MBO)

| Gebäudeklasse | Definition |
|---|---|
| GK 1a | Freistehende Gebäude, Höhe ≤ 7 m, max. 2 Nutzungseinheiten, gesamt ≤ 400 m² BGF |
| GK 1b | Freistehende land- oder forstwirtschaftlich genutzte Gebäude |
| GK 2 | Gebäude, Höhe ≤ 7 m, max. 2 Nutzungseinheiten, gesamt ≤ 400 m² |
| GK 3 | Sonstige Gebäude, Höhe ≤ 7 m |
| GK 4 | Gebäude, Höhe ≤ 13 m, Nutzungseinheiten jeweils ≤ 400 m² |
| GK 5 | Sonstige Gebäude einschließlich unterirdischer Gebäude |
| Sonderbauten | Hochhäuser > 22 m, Anlagen > 30 m Höhe, Geschoss > 1600 m², Verkaufsflächen > 800 m², Büroräume ≥ 400 m², Räume für > 100 Personen, Versammlungsstätten > 200 Besucher, Gaststätten, Beherbergung > 12 Betten, Krankenhäuser, Pflegeheime, Kindergärten, Schulen, Hochschulen, Justizvollzugsanstalten |

Höhe im Sinne MBO = Fußbodenoberkante höchstgelegenes Geschoss mit Aufenthaltsraum über mittlerer Geländeoberfläche.

#### 17.7.3 Bauliche Brandschutzmaßnahmen

##### Anforderungen an tragende Bauteile nach MBO (Tab. 17.43)

| Bauteil | GK 1 | GK 2 | GK 3 | GK 4 | GK 5 |
|---|---|---|---|---|---|
| Wände und Stützen | F 0 | F 30 | F 30 | F 60 | F 90 |
| In Kellergeschossen | F 30 | F 30 | F 90 | F 90 | F 90 |
| Decken zwischen Geschossen | F 0 | F 30 | F 30 | F 60 | F 90 |
| In Kellergeschossen | F 30 | F 30 | F 90 | F 60 | F 90 |
| Brandwände | F 60 BA | F 60 BA | F 60 BA | F 60 BA + M | F 90 BA + M |
| Gebäudeabschlusswände (innen nach außen) | F 30 | F 30 | F 30 | – | – |
| Notwendige Treppen tragende Teile | Keine | Keine | F 30 oder A | A | F 30 A |
| Außentreppen tragende Teile | A | A | A | – | – |
| Wände notwendiger Treppenräume | Keine | Keine | F 30 | F 60 BA + M | F 90 A + M |
| Decken notwendiger Treppenräume | Wie Geschossdecken des Gebäudes (ohne Dachabschluss) | | | | |

Decken unter/über Räumen mit Explosions-/erhöhter Brandgefahr müssen feuerbeständig sein (Ausnahmen: Wohngebäude GK 1+2, zwischen Wohn- und Landwirtschaftsteil).

##### Brandabschnitte

- Unterteilung durch Massivdecken oder Wände F90-A (Brandwände).
- Horizontal ausgedehnte Gebäude: Unterteilung durch innere Brandwände in Abständen von max. 40 m, Teilflächen ≤ 1.600 m² (landwirtschaftliche Gebäude: ≤ 10.000 m³).

##### Brandwände

Brandwände sind feuerbeständige Wände aus nichtbrennbaren Baustoffen (F90-A), standsicher auch bei mechanischen Stoßbelastungen durch herabfallende Bauteile.

**Vorschriften MBO:**
- Als Gebäudeabschlusswand an Grundstücksgrenzen bei Grenzabständen < 2,50 m oder möglichen Gebäudeabständen < 5 m.
- Innerhalb ausgedehnter Gebäude in Abständen von max. 40 m (Ausnahmen möglich).
- Zwischen Wohngebäuden und landwirtschaftlichen Betriebsgebäuden; Unterteilung landwirtschaftlicher Gebäude in Brandabschnitte ≤ 10.000 m³.
- Bei Gebäudeecken mit Winkel < 120°: Abstand von innerer Ecke ≥ 5 m, oder mindestens eine Außenwand auf 5 m Länge als öffnungslose F90-A-Wand.

**Ausführung:**
- In der Regel ohne Versatz durch alle Geschosse hochzuführen. Geschossweiser Versatz zulässig wenn unterstützende Bauteile und Geschossdecken ohne Öffnungen in F90-A ausgeführt (Abb. 17.95).
- Mindestens 30 cm über Bedachung führen; alternativ beidseitig 50 cm auskragende feuerbeständige Platte in Höhe der Dachhaut.
- GK 1–3: Brandwände mindestens bis unter Dachhaut; verbleibende Hohlräume vollständig mit nichtbrennbaren Baustoffen füllen.
- Bauteile aus brennbaren Baustoffen (auch Dachlatten) dürfen Brandwände nicht überbrücken.
- Stahl-/Holzträger und -stützen, Schornsteine, Schlitze nur so tief eingreifen, dass der Restquerschnitt F90 erfüllt.
- Hinterlüftete Außenwandbekleidungen/Doppelfassaden dürfen ohne Abschottungen nicht über Brandwände geführt werden.
- Öffnungen in Brandwänden grundsätzlich unzulässig; Ausnahmen: dicht- und selbstschließende T90-Abschlüsse oder Brandschutzschleusen. Verglasungen in G90 möglich (z.B. Brandschutz-Verbundglas, Glas-Brandschutzsteine F90-A). Leitungsdurchführungen nur mit besonderen Vorkehrungen gegen Feuer- und Rauchübertragung (Brandschotts).
- Nichttragende Brandwände aus C-Profilen + mehrlagigen Brandschutzplatten mit Mineralwollkern möglich; mechanische Beanspruchbarkeit durch aufgenietete Stahlbleche.

**Komplextrennwände (besondere Versichereranforderungen):**
- Aus nichtbrennbaren Baustoffen, 180 min Tragfähigkeit und Raumabschluss auch unter mechanischer Beanspruchung.
- 50 cm über Dach zu führen.

**Trennwände** erforderlich:
- Zwischen Nutzungseinheiten sowie zwischen Nutzungseinheiten und anders genutzten Räumen (außer notwendigen Fluren)
- Abschluss von Räumen mit Explosions-/erhöhter Brandgefahr
- Zwischen Aufenthaltsräumen und anders genutzten Räumen im Kellergeschoss

##### Außenwände, Brüstungen und Schürzen

- Feuerüberschlagsweg (Deckenrand + Sturz + Brüstung) muss min. 1 m betragen.
- Nichttragende Außenwände: W30–W180 nach DIN 4102-3.
- Auskragende Decken oder Fluchtbalkone können Feuerüberschlag verhindern.

##### Dächer

- Dachhaut muss gegen Flugfeuer und strahlende Wärme widerstandsfähig sein ("harte Bedachung").
- Weiche Bedachungen bei GK 1–3 unter erhöhten Abstandsanforderungen zur Grundstücksgrenze und untereinander zulässig.
- Ausnahmen von Hartes-Dach-Anforderung: begrünte Bedachungen (kein Brandrisiko von außen), Gebäude ohne Aufenthaltsräume und ohne Feuerstätten ≤ 50 m³, lichtdurchlässige Bedachungen aus nichtbrennbaren Baustoffen, lichtdurchlässige Teilflächen aus brennbaren Baustoffen innerhalb harter Bedachungen, Lichtkuppeln und Oberlichter in Wohngebäuden, Eingangsüberdachungen.
- Dachüberstände, -gesimse, -aufbauten (PV, Glasdächer, Oberlichter): min. 1,25 m Abstand von Brandwänden.
- Traufseitig angebaute Gebäude: Dach für Brandbeanspruchung von innen nach außen feuerhemmend (F30); Öffnungen ≥ 2 m waagerecht von Brandwand entfernt.
- Dächer angrenzend an Außenwände mit Fenstern ohne Feuerwiderstand: im Abstand 5 m gleiche Feuerwiderstandsfähigkeit wie Decken des anschließenden Gebäudes.
- Flachdächer aus Trapezblechen: hohes Brandrisiko durch Hohlräume (rasche Hitzeausbreitung); Tragfähigkeitsverlust durch Hitze. Ausreichender Feuerwiderstand meist nur durch unterseitige Bekleidungen aus GKF- oder Brandschutzplatten erreichbar.

##### Rettungswege

- Jede Nutzungseinheit mit mindestens einem Aufenthaltsraum: mind. 2 voneinander unabhängige Rettungswege pro Geschoss.
- Beide Rettungswege dürfen innerhalb eines Geschosses über denselben notwendigen Flur führen.
- Oberhalb Erdgeschoss: Erster Rettungsweg = notwendige Treppe.
- Zweiter Rettungsweg: weitere notwendige Treppe ODER durch Feuerwehr erreichbare Stelle.
  - Feuerwehr-Leiter: Brüstungshöhe max. 8 m
  - Hubrettungsgeräte: Brüstungshöhe max. 23 m
- Bei vielen Personen (Versammlungsstätten) oder eingeschränkt beweglichen Personen (Altenheime): zweiter baulicher Rettungsweg regelmäßig gefordert.
- Sicherheitstreppenraum: zweiter Rettungsweg nicht erforderlich wenn Rettung über Sicherheitstreppenraum (feuer- und rauchfrei) möglich; bei Hochhäusern über loggienartige Zugänge.

##### Treppen

- Nicht ebenerdige Geschosse + benutzbarer Dachraum: mind. eine notwendige Treppe.
- Einschiebbare Treppen/Leitern: nur GK 1 und 2, nur Zugang zu Dachräumen ohne Aufenthaltsräume.
- Verbindungstreppen innerhalb derselben Nutzungseinheit bis 2 Geschosse und ≤ 200 m² gesamt möglich ohne durchgehenden Treppenraum (Maisonettwohnung), wenn in jedem Geschoss anderer Rettungsweg erreichbar.
- Lichte Laufbreite für Krankentragen: mind. 1,25 m; Podesttiefe mind. 1,50 m.

##### Treppenräume

- Jede notwendige Treppe in eigenem durchgehenden Treppenraum (notwendiger Treppenraum).
- Ohne eigenen Treppenraum zulässig in GK 1 und 2, Maisonettwohnungen, Außentreppen.
- Notwendiger Treppenraum muss i.d.R. an Außenwand liegen und unmittelbaren Ausgang ins Freie haben.
- Fenster: ≥ 0,5 m² freier Querschnitt pro Obergeschoss für Belüftung, Entrauchung, Belichtung. Alternativ: Öffnung zur Rauchableitung an oberster Stelle.
- Rauchableitung: mind. 1 m² freier Querschnitt; bedienbar vom Erdgeschoss und obersten Treppenabsatz. Schutzziel: Löscharbeiten der Feuerwehr nach Evakuierung unterstützen (nicht Rauchfreiheit des Treppenraums während Evakuierung).
- Erreichbarkeit: jede Stelle eines Aufenthaltsraums sowie Kellergeschoss in ≤ 35 m (Lauflinie).
- Übereinander liegende Kellergeschosse: mind. 2 Ausgänge in Treppenräume oder direkt ins Freie.
- Bekleidungen, Putze, Materialien: aus nichtbrennbaren Baustoffen. Bodenbeläge: mind. schwer entflammbar (B1 nach DIN 4102-1 bzw. Cfl-s1 nach DIN EN 13501-1).
- Hochhäuser ≤ 60 m: ein Sicherheitstreppenraum ausreichend; > 60 m: alle notwendigen Treppenräume als Sicherheitstreppenräume.
- Alle Obergeschosse in Hochhäusern: 2 unabhängige Treppenräume oder 1 Sicherheitstreppenraum.

##### Notwendige Flure

- Horizontaler Teil des Rettungswegs zwischen Aufenthaltsraum und Treppenraum (oder Ausgang ins Freie in ebenerdigen Geschossen).
- Erforderlich: innerhalb von Wohnungen und Nutzungseinheiten > 200 m² sowie Büro-/Verwaltungsnutzung > 400 m².
- Wandanforderungen: feuerhemmend; in Kellergeschossen (mit feuerbeständiger Tragkonstruktion) ebenfalls feuerbeständig; bis Rohdecke führen.
- Unterteilung durch rauchdichte und selbstschließende Abschlüsse in Rauchabschnitte ≤ 30 m Länge.
- Notwendige Flure mit nur einer Fluchtrichtung: max. 15 m lang.

#### 17.7.4 Brandschutzmaßnahmen für Bauteile

Brandverhalten hängt ab von: Brandbeanspruchung (Normfeuer), Querschnittserwärmung (Masse + Oberfläche), gleichzeitige mechanische Beanspruchung, statische Lasten, temperaturabhängige Baustoffkennwerte.

##### Stahlbauteile

- Stahl ist nicht brennbar, verformt sich aber erheblich bei Brandtemperaturen; verliert Tragfähigkeit, richtet durch Verdrehungen/Verbiegungen Schäden an Nachbarbauteilen an.
- Maßgebend für Bemessung: Formfaktor U/A (beflammter Umfang/Querschnittsfläche), statischer Ausnutzungsgrad α.
- Kritische Stahltemperatur: ca. 400°C (Fließgrenze je nach Stahlsorte und Spannung).
- Ungeschützte Stahlbauteile erfüllen kaum Brandschutzanforderungen (Ausnahme: sehr dicke Profile bei geringem Ausnutzungsgrad).

**Schutzmaßnahmen für Stahl:**
- Ummantelung mit Beton, Mauerwerk, Wandbauplatten, Putz (DIN 4102-4, Abschn. 7)
- Hohlprofile: ausbetonierbar
- Für F180-A: Feuerschutz-Ummantelungen aus bewehrten Putzen, GKF-Platten oder speziellen Brandschutzplatten ggf. mit Ausmauerungen.

**Berechnungsbeispiel Formfaktor:** Profil HEB 200 (IPBv 200): h = 200 mm, b = 206 mm, A = 131 cm² → U/A = (2×200 + 2×206)/131 = 65 m⁻¹

**Für F90-A (HEB 200) nach DIN 4102-4 Tab. 92:**
- 2 × 15 mm GKF-Platten (DIN 18180), oder
- 15 mm zementgebundene Feuerschutzplatten auf Basis Calciumsilikat (Promat).

**Für F90-A an Stützen (DIN 4102-4 Tab. 95):** 3 × 15 mm GKF-Platten.

**Putz-Bekleidung:** Putzträger (Rippenstreckmetall, Drahtgewebe) mit guter Haftung am Stahl erforderlich. Spezial-Brandschutzputze: Mineralfaser-Spritzputze (Rohdichte 300–400 kg/m³) oder Vermiculite-Spritzputze (450–850 kg/m³) → bis F180 erreichbar.

**Beschichtungen (Dämmschichtbildner):** F30–F90 möglich für offene und geschlossene Profile mit passendem U/A-Verhältnis. Systemaufbau: Korrosionsschutz + Brandschutzbeschichtung + Decklack. Im Außenbereich Decklack zwingend.

**Asbesthaltige Brandschutzbekleidungen:** Seit langem verboten. Vorhandene Beschichtungen schützen oder fachgerecht entsorgen (Lungengefährdung durch eingeatmete nicht gebundene Asbestfasern).

**Verbundträger/-stützen:** DIN 4102-4 Abschn. 7 für ausbetonierte Kammern/Seitenteile und betongefüllte Hohlprofile; Kammerbeton zugfest mit Stahlprofil verbinden (Bügel, Haken, Kopfbolzen). Bis F180 erreichbar.

**Unterdecken** zum flächigen Schutz horizontaler Stahlbauteile und Trapezbleche.

##### Massivbauteile aus Stahlbeton und Mauerwerk

- Stahlbetonbauteile gefährdet durch Abplatzen der Betondeckung bei hohen Temperaturen → Bewehrung freigelegt → Tragkraftsverlust.
- Feuerwiderstandsklassen abhängig von Bauteildicke und Betondeckung.
- Zusätzliche Putze oder Estriche können zur Querschnittsbemessung herangezogen werden.
- Ohne Zusatzschutz: F30–F180 möglich.
- Norma: DIN EN 1992-1-2 (Eurocode 2 Teil 1-2) für Regelfälle; DIN 4102-4 als Restnorm für Anschlüsse.
- **Mauerwerk:** Wände, Pfeiler, Stürze nach Materialart und Dicke klassifiziert (DIN 4102-4, Tab. 9.1 ff.). Halbstein-Wände aus Mauerziegeln oder Kalksandsteinen mit 11,5 cm Dicke: bereits F90-A möglich, auch bei mehrseitiger Brandbeanspruchung.

##### Bauteile aus Holz

- Holz: normalentflammbar B2 nach DIN 4102-2; europäisch D-s2 d0 (begrenzte Rauchentwicklung, kein brennendes Abtropfen).
- Brandverhalten von Holz besser als oft angenommen: Holzrohdichte, Feuchtigkeitsgehalt, Holzkohlebildung an der Oberfläche verzögern Zersetzung.
- Dämmschichtbildende Anstriche: B2-Hölzer zu B1 verbesserbar.
- DIN 4102-4 Abschn. 10: Tabellen für Holzbalkendecken, Wände/Decken in Holztafelbauart, Holzwolle-Leichtbauplatten, Dächer aus Holz und Holzwerkstoffen, Verbindungen.

**Feuerwiderstandsklassen für Holzbauteile:**
- Freiliegende Vollholzbalken/Brettschichtträger: F30-B oder F60-B je nach Querschnitt, Biegebeanspruchung, Knicklänge (DIN 4102-4).
- Bekleidete Balken/Stützen: unabhängig von Spannungsausnutzung und Holzart verbessert.
- F60-B: z.B. 2-lagige Bekleidung aus 2 × 12,5 mm GKF-Platten.

**MHolzBauRL (Muster-Richtlinie über brandschutztechnische Anforderungen an Holzbauteile, 2020):**
- Ermöglicht tragende/aussteifende Holzbauteile auch in GK 4 und 5.
- Hochfeuerhemmende Wände anstelle von Brandwänden und Treppenraumwände in Holzrahmen-/Holztafelbauweise mit Brandschutzbekleidung möglich.
- Massivholzbauweise in GK 4 und 5: Nutzungseinheiten max. 200 m² (Einheiten > 400 m² mit qualifizierten Trennwänden unterteilbar).
- Brandschutzbekleidung aus nichtbrennbaren Baustoffen erforderlich (z.B. 18 mm GKF-Platte) → verhindert Entzündung für mind. 30 min.
- Toleranz: je Raum entweder die Decke oder max. 25 % aller Wände (ausgenommen Wände mit Feuerwiderstandsanforderung) sichtig in Holz.
- Zweilagige raumseitige Bekleidung aus 2 × 18 mm GKF: typische Anforderung.
- Oberseitige Brandschutzbekleidung von hochfeuerhemmenden Decken entfällt, wenn Fußbodenaufbau die Anforderungen erfüllt (z.B. 20 mm nichtbrennbare Dämmschicht + mind. 30 mm Estrich).
- Besonders wichtig: rauchdichte Fugenausbildung (Stufenfalz, Feder, Fugenversatz); Planungsdetails in MHolzBauRL (Abb. 17.99–17.102).

**Holzfassaden (MHolzBauRL):**
- Außenwandbekleidungen aus Holz/Holzwerkstoffen auch in GK 4 und 5 möglich.
- Mindestens 15 mm dicke nichtbrennbare Trägerplatte erforderlich (wenn Außenwand nicht bereits nichtbrennbar oder mit durchgehender nichtbrennbarer Bekleidung).
- Dämmstoffe: grundsätzlich nichtbrennbar; Unterkonstruktionstiefe max. 50 mm.
- Geschossweise horizontale Brandsperren aus Stahlblech (kein Aluminium), Mindestdicke 1,5 mm (Auskragung ≤ 150 mm) bzw. 2,0 mm (Auskragung bis 150 mm).
- Mindestmaße der Auskragung (Maß X) abhängig vom Bekleidungstyp:

| Bekleidungstyp | Ausrichtung | Mindest-Auskragung X |
|---|---|---|
| Flächiger Holzwerkstoff (Rohdichte ≥ 350 kg/m³, geschlossen, Plattendicke ≥ 22 mm, Kantenlänge ≤ 625 mm) | horizontal/vertikal | ≥ 50 mm |
| Formschlüssige Schalung (≥ 22 mm Dicke, kernfrei ≤ 160 mm Breite, Deckleistenschalung, Nut+Feder) | horizontal | ≥ 50 mm |
| Formschlüssige Schalung | vertikal | ≥ 100 mm |
| Kraftschlüssige Schalung (Überfälzung, Stülpschalung, T-Leistenschalung) | horizontal | ≥ 100 mm |
| Kraftschlüssige Schalung | vertikal | ≥ 150 mm |
| Offene Schalung (Brettquerschnittsfläche ≥ 1.000 mm²) | horizontal | ≥ 200 mm |
| Offene Schalung | vertikal | ≥ 250 mm |

- Im Bereich von Brandwänden: brennbare Außenwandbekleidung mindestens 1,0 m unterbrechen und durch nichtbrennbare Baustoffe ersetzen; Hinterlüftungsspalt darf nicht über Brandwand geführt werden.
- Jede Gebäudeseite mit Holzbekleidung muss für Feuerwehr erreichbar sein.

##### Fugenausbildung

- Dehn- und Anschlussfugen: Ausdehnung/Verformung im Brandfall möglich lassen, gleichzeitig Feuerdurchtritt verhindern.
- Fugenverschluss: Baustoffe Klasse A (z.B. Steinwolle), ggf. Fugendichtungsmassen B2 und Stahlwinkel.
- DIN EN 13501-2 + Prüfverfahren DIN EN 1366-4: raumabschließende Bauteilfugen klassifiziert (E, EI) mit Zusatzklassifizierungen für Lage, Beweglichkeit, Anschlussausbildung, Fugenbreiten.

##### Wärmedämmstoffe

- Kunststoff-Dämmstoffe: ungünstiges Brandverhalten, starke Qualm-/Rauchentwicklung + giftige Gase, können über Kopf abtropfen.
- B3-Kunststoffe verboten (sofern nicht mit anderen Baustoffen nicht leichtentflammbar).
- Bei Fassadenverkleidungen, Garagenausbau, Versammlungsräumen: mind. B1 (schwerentflammbar).

#### 17.7.4 Brandschutzverglasungen (DIN 4102-13)

- G30/E30 bis G120/E120: wärmestrahlungsdurchlässige Einscheiben-Sicherheitsverglasungen (ESG — Borosilikat- oder Glaskeramikgläser, Drahtgläser mit besonderen Zulassungen). Verhindern nicht ausreichend Wärmestrahlung → nur wo durchtretende Wärmestrahlung unkritisch.
- F30/EI30 bis F180/EI180: wärmestrahlungsverhindernde Zwei- oder Dreischeiben-Sicherheitsverglasung mit transparenter Brandschutzschicht aus Natriumsilikat im Scheibenzwischenraum (SZR). Verhindern Flammen und entzündbare Gase auf brandabgewandter Seite.
- Sondergläser (mehrschichtiger Aufbau): wärmedämmende Brandschutzschichten schäumen auf → nicht transparente, wärmeabschirmende Masse (EI-Klassen).
- Anwendung F/EI-Verglasungen: Lichtöffnungen in Brandwänden, Treppenraumabschlüsse, Flucht- und Rettungswege, feuerhemmende/-beständige Bauteile.
- F/EI-Verglasungen werden wie die angrenzenden Decken-/Wandflächen behandelt.
- Mechanische Beanspruchbarkeit nur in Kombination mit geprüften Rahmenkonstruktionen.

**Fassaden- und Dachverglasungen:**
- Brüstungen als Brandschutz gegen vertikalen Brandüberschlag: G- oder F-Verglasungen.
- Innenecken bei Fassaden < 5 m: Feuerwiderstandsklasse der Glasfassaden im Eckbereich (z.B. F90 oder G30/F30) erforderlich; besser: Brandabschnitte außerhalb Inneneckbereich.
- Dachverglasungen: Schutz vor vertikaler Brandübertragung bis 5 m vor aufgehenden Fassadenflächen; F30, G30, F90 verfügbar.
- Bei Vollflächenfassaden/-überkopfverglasungen: häufig Abweichungen von LBO nötig; Kompensationsmaßnahmen (Brandmelde-/Sprinkleranlagen, Entrauchung) mit Behörden und Feuerwehr abstimmen.

#### Brandschutz bei haustechnischen Anlagen

- Leitungen (elektrisch + Rohrleitungen) durch raumabschließende Bauteile mit Brandschutzanforderungen nur wenn Brandausbreitung ausreichend lange nicht zu befürchten oder Vorkehrungen getroffen (MBO § 40).
- Ausnahme: Decken in GK 1 und 2; innerhalb Wohnungen und Nutzungseinheiten ≤ 400 m² in max. 2 Geschossen.

**Drei Möglichkeiten nach DIN 4102:**
1. Abschottungen: Kabelabschottungen S30–S180, Rohrleitungen R30–R180, Brandschutzklappen K30–K90, Lüftungsleitungen L30–L120
2. Feuerwiderstandsfähige Leitungen oder Einhausung/Ummantelung
3. Verlegung in feuerwiderstandsfähigen Schächten F30–F180 oder Installationskanälen I30–I180

**Elektroinstallationen:**
- PVC-Kabel: giftige Brandgase → vermeiden oder durch Rauchschutzmaßnahmen kontrollieren.
- Brandlasten aus Kabeln (i.d.R. B2): in Hohlräumen von Decken mit Unterdecken teilweise toleriert; im Bereich von Rettungswegen (Flure, Treppenräume) in eigenen Schächten/Kanälen abschotten oder Unterdecken brandschutztechnisch auslegen.
- Funktionserhalt elektrischer Anlagen im Brandfall (DIN 4102-12, M-LAR):
  - Mind. 90 min: Löschwasserversorgung, RWA-Anlagen, Feuerwehraufzüge
  - Mind. 30 min: Sicherheitsbeleuchtung, Brandmeldeanlagen, Alarmanlagen

**Kabelabschottungen (S-Klassen):**
- Nur von Fachbetrieben ausführbar.
- Abschottungen kennzeichnen.
- Einzelne Kabel mit geringen Querschnitten: ohne Kabelabschottung durch Wände/Decken möglich, wenn Resthohlräume vollständig mit nichtbrennbaren formbeständigen Baustoffen (Mörtel, Beton, Mineralfasern) oder aufschäumenden Schaumstoffen verschlossen.

**Durchdringungen:**
- Restquerschnitte mit Mörtel, Beton, aufschäumenden Baustoffen, Mineralfaser-Dämmstoffen oder Kombinationen verschließen → Feuerwiderstandsklasse der Wand/Decke erhalten.
- Nachrüstbarkeit berücksichtigen.

**Rohrleitungen:**
- Nicht brennbare Rohre: Außendurchmesser max. 160 mm, Abstand ≥ Außendurchmesser → keine Feuer-/Rauchübertragung zu erwarten; Restabstände mit Zement/Beton füllen.
- Aluminium- oder Glasrohre (für nichtbrennbare Flüssigkeiten): max. 32 mm, Abstand ≥ 5× Außendurchmesser; Resthohlräume mit Mineralfaser/Schaum verschließen.
- Rohrdurchführungen (R-Klassen) nach DIN 4102-11.

**Lüftungsleitungen (§ 41 MBO):**
- Lüftungsanlagen inkl. Dämmstoffe und Bekleidungen i.d.R. aus nichtbrennbaren Baustoffen.
- Ausnahmen nur für untergeordnete Bauteile ohne Brandbeitrag, jedoch außerhalb Rettungswege und oberhalb feuerwiderstandsfähiger Unterdecken.
- Abschottungen: selbsttätig schließende Brandschutzklappen (K-Klassen) an raumabschließenden Bauteilen und Schächten.
- Auslösung: temperatur- und/oder rauchgesteuert.
- Metallische Lüftungsleitungen: erhebliche Ausdehnungen bei Brandeinwirkung → Dehnungsbauteile erforderlich.
- Lüftung nach DIN 18017-3 (Bäder/WC ohne Außenfenster): einfachere Absperrvorrichtungen; luftführende Hauptleitungen vertikal über Dach.

**Unterdecken als Brandschutz:**
- Müssen feuerwiderstandsfähig gegen Brand von unten UND aus Deckenhohlraum sein.
- Anforderungen an Anordnung, Deckenbaustoffe, Abhängevorrichtungen in M-LAR festgelegt.
- Installationen oberhalb der Decke dürfen nicht herabfallen (→ Unterdeckenversagen).

**Doppelböden/Hohlraumböden:**
- Elektroinstallationen brandgeschützt in Estrichschichten, Hohlraumböden, Doppelbodensystemen verlegbar.
- Hohlraumhöhe < 20 cm: keine Brandbeanspruchung des Hohlraums anzunehmen.
- Regelung durch Muster-Systembödenrichtlinie (MSysBöR): B2 im Allgemeinen, A im Bereich Rettungswege; Abschottungen zu notwendigen Fluren/Treppenräumen.

**Installationsschächte/-kanäle:**
- I-Klassen nach DIN 4102-11; aus nichtbrennbaren Baustoffen.
- Gleiches Feuerwiderstandsdauer wie durchquerte raumabschließende Bauteile.
- Ausnahme: GK 1 und 2 (sofern keine Sonderbauten mit besonderen Risiken).
- Abgehängte Kanäle: brandschutzmäßig bemessende Aufhängekonstruktion erforderlich.
- Rohrabschottungen in Brandwänden: Rohrmanschetten oder Rohrstopfen.

---

### 17.8 Schutz vor gesundheitlichen Gefahren

#### 17.8.1 Gefährliche Stoffe

Physikalische und chemische Einflussgrößen auf menschliches Wohlbefinden (nach Wissenschaftsstand):
- Lufttemperatur, Raumluftqualität (Schadstoffe, Staub)
- Oberflächentemperatur raumumschließender Bauteile (Wärmestrahlungsanteil)
- Luftfeuchte (absolut, relativ), Luftbewegung (Zugerscheinungen)
- Frischluftanteil/Lüftungsrate, CO₂-Gehalt
- Luftdruck; Gehalt an natürlichen Gasen (CO, SO₂, NO₂)
- Anthropogene Luftbelastungen (Gase, Dämpfe, Stäube, Bakterien)
- Schallpegel; Frequenzverteilung (inkl. Infraschall und Ultraschall)
- Beleuchtungsstärke/Leuchtdichte (Tageslichteintrag, Blendung); spektrale Verteilung (IR, UV)
- Elektromagnetische Feldstärken (Gleich- und Wechselfelder)
- Ionenkonzentration; radioaktive Strahlung

Unbedingt zu meidende Stoffe beim Bau:
- Formaldehyd (HCHO) — in Leimen, Bindemitteln
- Polychlorierte Kohlenwasserstoffe (PCP) — in Holzschutzmitteln, Fugenmassen
- Isocyanate — in Farben, Lacken, Epoxidharzen, Polyurethanen
- Dioxine/Furane — aus Flammschutzmitteln
- Asbest — Krebsgefahr besonders bei Verarbeitung/Abbruch von Faserzementwerkstoffen

Lösungsmittel (Toluol, Xylol, Benzol in Farben, Beschichtungen, Polituren, Klebern, Reinigungsmitteln) gehen kurz nach Einbau in die Raumluft über. In den ersten Monaten nach Gebäudeherstellung kann die Innenluft ein Vielfaches an Schadstoffen gegenüber Stadtaußenluft enthalten. Allergische und toxische Reaktionen beobachtet. Mangels Deklarationspflicht für Inhaltsstoffe sind Gefahren für Anwender schwer erkennbar.

**Mineralwoll-Dämmstoffe:**
- 1993 von MAK-Kommission als (im Tierversuch) krebserzeugend eingestuft.
- Ab 1996: Mineralwolledämmstoffe mit verringertem Krebspotenzial (verbesserter Biolöslichkeit, KI < 40) auf Markt.
- Ab 2000: grundsätzliches Verbot des Einsatzes alter Mineralwolle; neue Mineralwolle darf nur nach Kriterien der Gefahrstoffverordnung (GefStoffV 2010/2021, Anhang II, Punkt 5 – Biopersistente Fasern) hergestellt werden.
- RAL-Gütezeichen Mineralwolle = Einhaltung GefStoffV; Faserlängen > 3 Mikrometer = nicht lungengängig.
- Vorsichtsmaßnahmen beim Einbau: Atemschutz, geschlossene Arbeitskleidung.
- Alte Mineralwolle: Arbeiten nur nach TRGS 521 (Technische Regeln für Gefahrstoffe, Stand 02/2008) mit besonderen Schutzmaßnahmen.
- Gefahrstoff-Informationssystem GISBAU der Berufsgenossenschaften Bauwirtschaft: Informationsquelle zu Inhaltsstoffen, Toxikologie, Berufskrankheiten, Schutzmaßnahmen, Ersatzstoffen.

#### 17.8.2 Radioaktivität, Radon

- Hauptbelastungsquelle: Radon (radioaktives Edelgas aus Uran-/Radiumzerfall). Zerfallsprodukte gelangen über Atemluft in den Körper.
- Radon entweicht vorwiegend aus Baugrund; geringere Mengen aus Baustoffen.
- Radonkonzentration hängt ab von: Ausführung des unteren Gebäudeabschlusses, Bodenbeschaffenheit (kristalline Böden/alte Tiefengesteine emittieren mehr als Sedimentböden), Lüftungsrate.
- Messgröße: Aktivität in Becquerel (Bq) pro m³.
- Durchschnittswert: ca. 50 Bq/m³; in ca. 50.000 deutschen Wohnungen: > 250 Bq/m³ messbar — dieser Wert sollte nicht überschritten werden.
- SSK-Empfehlungen (Strahlenschutzkommission): höhere Belüftung stärker gefährdeter Bauten; bessere Abdichtung unterer Gebäudeabschlüsse durch rissfreie Bodenplatten, Fugenversiegelungen, gasdichte Folien oder Beschichtungen.
- Radonbelastete Regionen in Deutschland: Hunsrück, Neuwieder Becken, Fichtelgebirge (u.a.).
