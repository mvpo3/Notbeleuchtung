# Lehrbuch der Bauphysik — Teil 22
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 881-920.

Dieser Teil schließt das Kapitel Kunstlicht mit Berechnungsverfahren und lichttechnischen Messungen ab, behandelt Lichtregelungssysteme für tageslichtabhängige Beleuchtungssteuerung und leitet dann in den Themenkomplex Brandschutz über. Abgedeckt werden: Wirkungsgradverfahren für Beleuchtungsanlagen, Ulbrichtsche Kugel als Messinstrument, Lichtregelung mit Photometerköpfen, sowie Brandschutzordnungen, DIN 4102, europäische Baustoffklassifizierung (EN 13501), Eurocodes für Brandschutz und erste Grundlagen der Brandentstehung.

## Inhalt

### 28.5 Beleuchtungsberechnungen — Wirkungsgradverfahren

Das Wirkungsgradverfahren dient zur überschlägigen Berechnung der mittleren Beleuchtungsstärke auf einer horizontalen Nutzfläche bei vorgegebener Leuchtenanzahl oder umgekehrt zur Ermittlung der erforderlichen Leuchtenanzahl für einen Nennwert.

**Grundprinzip:** Der Lichtstrom der Leuchten trifft teils direkt, teils nach Reflexion an den Raumoberflächen auf die Nutzfläche. Das Verhältnis direkter zu indirektem Anteil wird durch den Raumwirkungsgrad ηR beschrieben, der von der Leuchtenbauart (Abstrahlcharakteristik), der Raumgeometrie, der Montagehöhe über der Nutzebene und den Reflexionsgraden der Oberflächen abhängt.

**Raumindex k (für überwiegend direkt strahlende Leuchten):**

k = (a × b) / (h × (a + b))

Dabei gilt:
- a = Raumlänge in m
- b = Raumbreite in m
- h = Montagehöhe der Leuchte über der Nutzebene in m

Für überwiegend indirekt strahlende Leuchten gilt ein modifizierter Wert: k' = k × 1,5

**Berechnung der mittleren Beleuchtungsstärke EN bei gegebener Leuchtenanzahl n (Formel 28.6):**

EN = (F × ηLB × ηR × V × n) / (a × b)

**Berechnung der erforderlichen Leuchtenanzahl n für vorgegebenes EN (Formel 28.7):**

n = (1/V) × (EN × a × b) / (F × ηLB × ηR)

**Größenerklärung:**
- F = Lichtstrom je Leuchte in lm
- ηLB = Leuchtenbetriebswirkungsgrad
- ηR = Raumwirkungsgrad (aus Herstellertabellen in Abhängigkeit von k und Reflexionsgraden)
- V = Verminderungsfaktor für Verschmutzung der Leuchten
- n = Leuchtenanzahl
- a, b = Raumdimensionen in m

**Verminderungsfaktor V (Tab. 28.4) nach Verschmutzungsgrad:**

| V | Verschmutzungsgrad |
|---|---|
| 0,8 | Normal |
| 0,7 | Erhöht |
| 0,6 | Stark |

Hinweis: In manchen Literaturquellen wird der Planungsfaktor P verwendet, der dem Kehrwert von V entspricht (P = 1/V). In der Praxis werden häufig Einzelminderungsfaktoren verwendet, die Reinigungs- und Wartungszyklen gesondert berücksichtigen.

**Raumwirkungsgrade ηR für tief-breit strahlende Leuchten (A60, DIN 5040) — Auszug Tab. 28.5:**

| ρDecke | ρWände | ρBoden | k=1,25 | k=1,50 | k=2,00 |
|--------|--------|--------|--------|--------|--------|
| 0,70 | 0,70 | 0,50 | 0,99 | 1,06 | 1,17 |
| 0,70 | 0,50 | 0,20 | 0,73 | 0,79 | 0,88 |
| 0,70 | 0,50 | 0,10 | 0,70 | 0,76 | 0,83 |
| 0,70 | 0,20 | 0,20 | 0,62 | 0,69 | 0,79 |
| 0,70 | 0,20 | 0,10 | 0,61 | 0,67 | 0,76 |
| 0,50 | 0,50 | 0,10 | 0,68 | 0,74 | 0,81 |
| 0,50 | 0,20 | 0,10 | 0,60 | 0,66 | 0,75 |
| 0,20 | 0,20 | 0,10 | 0,59 | 0,65 | 0,73 |
| 0,00 | 0,00 | 0,00 | 0,55 | 0,61 | 0,70 |

**Rechenbeispiel direkt strahlende Leuchten (tief-breit, A60):**
- Vorgabe: EN = 500 lx, Nutzebene bei 0,85 m Höhe
- Raum: a = 12 m, b = 7 m, Deckenhöhe 3 m → h = 3 m − 0,85 m = 2,15 m
- Reflexionsgrade: ρDecke = 0,70, ρWände = 0,70, ρBoden = 0,50
- Leuchtenstrom: 4600 lm, ηLB = 0,75, V = 0,8 (normale Verschmutzung)

Raumindex: k = (12 × 7) / ((3 − 0,85) × (12 + 7)) ≈ 2

Aus Tabelle mit k = 2 und den Reflexionsgraden: ηR = 1,17

Ergebnis: n = (1/0,8) × (500 × 12 × 7) / (4600 × 1,17 × 0,75) ≈ 13 Leuchten

Aus Symmetriegründen und zur Sicherheit werden 14 Leuchten montiert.

Das Verfahren geht von einheitlichen Leuchtentypen aus. Bei gemischten Typen werden Einzelberechnungen je Typ addiert.

### 28.5.2 Lokale Beleuchtungsstärken anhand von Lichtstärken/LVK

Für lokale Beleuchtungsstärken (z. B. Akzentbeleuchtung) erfolgt die Berechnung über Lichtstärken nach dem photometrischen Entfernungsgesetz (Formel 28.10):

E = I(ε) × cos(ε) / r²

Dabei ist I(ε) die richtungsabhängige Lichtstärke aus der Lichtstärkeverteilungskurve (LVK), ε der Einfallswinkel und r der Abstand zwischen Quelle und Messpunkt.

Bei mehreren Punktlichtquellen werden die Einzelanteile addiert.

Der Reflexlichtanteil Eind (durch Reflexionen an Raumoberflächen) ergibt sich analog zum Innenreflexionsanteil beim Tageslichtquotienten mittels geometrischer Reihe (Formel 28.11):

Eind = ΦLe × ρ / (Ages × (1 − ρ))

- ΦLe = Gesamtlichtstrom aller installierten Leuchten im Raum
- ρ = mittlerer Reflexionsgrad aller Raumoberflächen
- Ages = Summe aller Raumoberflächen

### Kapitel 29 — Lichttechnische Messungen

#### 29.1 Messprinzip

Grundgröße jeder lichttechnischen Messung ist der Photostrom einer Fotodiode, der verstärkt und per A/D-Wandler digitalisiert wird. Mit V(λ)-Filter (spektrale Empfindlichkeitskurve des Auges) erhält man nach Kalibrierung direkt Beleuchtungsstärkemesswerte (lx). Für relative Vergleiche bei der Lichtplanung ist die absolute Genauigkeit weniger kritisch, da das menschliche Auge über mindestens fünf Größenordnungen adaptiert.

Leuchtdichtemessgeräte besitzen eine integrierte Optik, die einen gerichteten Lichtstrahl auf den Messsensor lenkt. Durch simultane Messung von Beleuchtungsstärke E und Leuchtdichte L an einem diffus reflektierenden Material gilt: E × ρ = L × π → Reflexionsgrad bestimmbar.

#### 29.2 Ulbrichtsche Kugel

Die Ulbrichtsche Kugel ist das wichtigste photometrische Messinstrument. Aufbau: Hohlkugel (meist zweiteilig), Innenfläche ideal matt-weiß mit möglichst konstantem Reflexionsgrad über den gesamten Wellenlängenbereich, typischerweise durch Bariumsulfat-Beschichtung realisiert.

**Eigenschaft:** Licht, das in die Kugel gelangt, verteilt sich vollkommen gleichmäßig auf der Innenfläche. Der indirekte Beleuchtungsstärkeanteil Eind aus einem einfallenden Lichtstrom Φ0 ist an jeder Stelle der Kugelwand gleich groß (Formel 29.1):

Eind = Φ0 × ρ / (4π × r² × (1 − ρ))

Gesamtbeleuchtungsstärke: Eges = Edir + Eind

Für Messungen muss der Direktlichtanteil auf den Sensor durch einen sog. Schatter (selber Reflexionsgrad wie Kugelwand) unterbunden werden, sodass Edir = 0 gilt.

**Größere Kugeln** reduzieren den Einfluss von Schatten, Kabelhalterungen und der Lichtquelle selbst auf die Interreflexion — daher werden Kugeln mit mehreren Metern Durchmesser eingesetzt.

#### 29.2.1 Lichtstrommessung

Aus dem gemessenen Eind lässt sich der Lampenlichtstrom berechnen (Formel 29.3):

Φ0 = Eind × 4π × r² × (1 − ρ) / ρ

**Beispielrechnung:**
- Gemessen: Eind = 330 lx
- Kugelradius: r = 1,50 m
- Bariumsulfat-Reflexionsgrad: ρ = 0,97

Ergebnis: Φ0 ≈ 289 lm

Genauigkeit hängt maßgeblich von der korrekten Angabe des Reflexionsgrades ab.

#### 29.2.2 Reflexionsgradmessung von Proben

Zwei Messungen: einmal Direktstrahl auf die Kugelwand, einmal auf die Probe. Da sich Licht gleichmäßig verteilt, ergibt das Verhältnis beider Messwerte direkt den Reflexionsgrad der Probe (Formel 29.4):

EProbe / EWeiß = ρProbe

Transmissionsgrade τ (senkrecht und diffus) von Proben sind analog messbar.

### Kapitel 30 — Lichtregelung

#### 30.1 Steuerung vs. Regelung

Steuerung: Vorgaben nach festem Zeitplan ohne Messwert-Rückkopplung.
Regelung: Einstellung von Kunstlicht und Sonnenschutz über Messdaten eines Lichtsensors mit Vergleichselektronik, sodass ein Beleuchtungsstärke-Sollwert auf einer Referenzebene (Arbeitsebene, Wandebene in Museen) eingehalten wird.

**Effizienz Tageslicht vs. Kunstlicht:**
- Tageslicht hat im Mittel > 100 lm/W bei höchster Farbwiedergabe
- Wärmeschutzglas-Beispiel: Lichttransmissionsgrad 75 %, g-Wert 0,6 → Selektivität 1,25 (Verhältnis Lichttransmission zu g-Wert)
- Effiziente Nutzung von Tageslicht steigert die Lichtausbeute nochmals um mind. 25 % gegenüber dem solaren Wärmegewinn
- Nur moderne hochpreisige LED-Lichtleisten erreichen ähnliche Effizienz

#### 30.2 Optimierte Tageslichtnutzung durch Lichtregelung

**Ziele einer tageslichtabhängigen Regelung:**
- Vorrang des Tageslichts vor Kunstlicht
- Spürbarkeit der Tageslichtschwankungen auf moderatem Niveau halten
- Einhaltung eines Sollwertbereichs, sichere Vermeidung zu hoher Beleuchtungsstärken
- Entlastung des Nutzers vom manuellen Nachstellen
- Kunstlicht als Grundbeleuchtung nur bei zu wenig Tageslicht hinzudimmen
- Minimierung des Stromverbrauchs für Kunstlicht und Reduktion solarer Kühllast

**Systemstruktur (Abb. 30.2):**
- Erweiterte Bedienebene: stationärer PC, Notebook, Fernwartung; umfangreiche Parametereinstellungen
- Einfache Bedienebene: Touchpanels/Schalter vor Ort; Betriebsartenauswahl, Beleuchtungsszenen; keine Parameteränderung
- Regelungsebene: abgegrenztes, autonomes System; wertet Messdaten, Besonnungszeitdatenbanken und Nutzervorgaben aus; gibt Stell- und Dimmbefehle aus
- Schnittstellen zur GLT (Gebäudeleittechnik), HKL, Sicherheit, Brand

Die Lichtregelung sollte als separate Anlage mit definierten Bezügen zur GLT ausgeführt werden.

#### 30.2.1 Regelungsprinzip

Vergleich Heizungsregelung vs. Lichtregelung:
- Heizung: Außentemperatur −30 °C bis +40 °C auf Innentemperatur 15 °C bis 25 °C → weniger als eine Größenordnung → träge Regelung
- Licht: Außenbeleuchtungsstärke 0–100.000 lx auf Raumwert ca. 100–1.000 lx → von fünf auf eine Größenordnung → trotzdem träge Regelung notwendig (mechanische Gewerke können schnellen Schwankungen nicht folgen)

**Toleranzbereich und Toleranzzeit:**
- Kein fixer Sollwert realisierbar, sondern ein Toleranzband um den Sollwert
- Kurzfristige Überschreitungen werden für eine Toleranzzeit akzeptiert
- Prinzip: Je weiter die Beleuchtungsstärke vom Sollwert entfernt, desto kürzer die Toleranzzeit bis ein Gewerk (Rollo/Lamelle) reagiert

#### 30.2.2 Schutz vor direkter Besonnung

Zwei Kriterien:
1. Wann kann die Sonne prinzipiell einfallen? → Besonnungszeitdatenbank (wöchentliche Abstufung)
2. Scheint die Sonne gerade? → Lichtsensor im Außenbereich, fassadenorientiert

**Methoden zur Erstellung der Besonnungszeitdatenbank:**
- Horizontoscop-Aufnahme am Referenzpunkt (z. B. Brüstungsmitte) mit hinterlegtem Sonnenstandsdiagramm für die geographische Breite
- Stereographische Projektion der Eigen- und Fremdverbauung in Sonnenstandsdiagramm per Computerprogramm (Drahtgittermodell aller beteiligten Gebäudeteile)

**Zeitumrechnung:** Zeiten im Sonnenstandsdiagramm sind in Ortszeit angegeben → Umrechnung in MEZ oder MESZ erforderlich.

Rückkehr in den Nicht-Besonnungsmodus mit Verzögerung/Hysterese (verhindert ständiges Öffnen und Schließen).

#### 30.2.3 Abstufung der Schließzustände

Äquidistante Einteilung der Lamellen (z. B. 90° in 5°-Schritte) berücksichtigt die nichtlineare Lichtwahrnehmung nicht: In den ersten Schließschritten kaum wahrnehmbare Helligkeitsänderung, später störend zunehmend.

**Lösung:** Einteilung nach dem Weber-Fechnerschen Gesetz (Abschn. 26.9) — Schritte von der Öffnungsposition zunehmend kleiner werdend (logarithmische Stufung). Vorteil: System wird träger (weniger Schritte nötig).

#### 30.2.4 Einbindung Kunstlicht in Tageslichtregelung

Nur dimmbare Grundbeleuchtung einbinden — zwei Funktionen:
- Schnelles Einspringen bei schnellen Außenlichtschwankungen (mechanische Gewerke zu träge)
- Stetiges Hinzudimmen abends oder bei bedecktem Himmel

**Parametrierung:** Dimmen träge einstellen (kein Sprung beim Einschalten); Abschaltverzögerung vorsehen.

**Praxisbeispiel Museumssaal mit Oberlicht:**
- Sollwert auf Wandebene: ca. 250 lx
- Außenbeleuchtungsstärke variabel; Rollos stufenweise gefahren
- Bei Tageslichtabnahme: Rollos öffnen schrittweise; bei kurzzeitiger Unterschreitung Kunstlicht-Sollwert → Kunstlicht stufenlos hinzudimmen
- Kunstlichtsteuerung (nahezu instantan) kompensiert schnelle Helligkeitsabnahmen bis träge Rollos reagieren (Beispiel: Zeitraum 14:00–16:00 Uhr)

#### 30.2.5 Position von Photometerköpfen (Lichtsensoren)

- Möglichst nahe der Referenz-/Bezugsebene anbringen
- Museen: auf oder nahe Bildebene (außerhalb der Haupthängeebene)
- Bibliotheken: unauffällig horizontal auf Tischlampen
- Zusätzlich Außenmessung erforderlich (Besonnungsdetektion, Vordosierung, Überprüfung der Regelungsfunktion durch Datenaufzeichnung)

#### 30.2.6 Graphische Datenaufzeichnung

Numerische Datenaufzeichnung unverzichtbar für Berechnungen, aber für Überblick ungeeignet. Tageweise graphische Darstellung zeigt:
- Außenbeleuchtungsstärke (Hochpegel-Kurve)
- Innenraumbeleuchtungsstärke am Referenzpunkt
- Rolloposition (stufenweise Änderungen)
- Dimmwert Kunstlicht (stufenlose Änderungen)

#### 30.2.7 Visualisierung

Benutzerfreundliche Bedienoberfläche (Visualisierung) ist entscheidend für Akzeptanz. Alle Eingabe- und Anzeigepunkte müssen mit den Datenpunkten in der SPS (Speicherprogrammierbare Steuerung) verknüpft werden. Typisch: Grundrissansicht → Klick auf Raum → Raumquerschnitt mit Übersicht aller relevanten Größen.

---

## Teil VI — Brand

### Kapitel 31 — Einführung Brandschutz

Brandschutzmaßnahmen gliedern sich in drei Hauptbereiche:
- Abwehrender Brandschutz (Feuerwehr)
- Vorbeugender und anlagentechnischer Brandschutz (Melde-, Warn- und Frühbekämpfungsanlagen)
- Vorbeugender baulicher Brandschutz (Planung, Ausbildung der Bauteile)

**Prinzip des baulichen Brandschutzes:** Das Bauwerk muss bei Brandereignis hinreichende Tragfähigkeit und Wärmeisolierung über die gesamte oder eine ausreichende Teildauer eines Schadfeuers gewährleisten. Nach Ablauf dieser vorgeschriebenen Dauer werden in Deutschland keine weiteren Anforderungen an das Bauwerk gestellt (mit wenigen Sonderfall-Ausnahmen).

**Entwicklungen der Rahmenbedingungen:**
- Einführung europäischer Normen für Baustoff- und Bauteilbewertung (ersetzen nationale Normen sukzessive)
- Etablierung leistungsorientierter Brandschutzmaßnahmen auf Basis moderner Ingenieurmethoden — ergänzendes Werkzeug besonders für Sonderbauten, die durch Normen nicht oder unzureichend abgedeckt werden

### Kapitel 32 — Ordnungen und Normen im Brandschutz

#### 32.1 Landesbauordnungen und Sonderverordnungen

In Deutschland regeln die Landesbauordnungen (LBO) den vorbeugenden baulichen Brandschutz (Länderzuständigkeit mit Bemühen um einheitliche Musterentwürfe).

**Generalklausel (sinngemäß, in allen LBO ähnlich formuliert):**
Bauliche Anlagen müssen unter Berücksichtigung der Brennbarkeit der Baustoffe, der Feuerwiderstandsdauer der Bauteile (ausgedrückt in Feuerwiderstandsklassen), der Dichtheit von Öffnungsverschlüssen und der Anordnung von Rettungswegen so gestaltet sein, dass Brandentstehung und -ausbreitung verhindert werden und im Brandfall Rettung von Menschen und Tieren sowie wirksame Löscharbeiten möglich sind.

**Ziel:** Sicherstellung der Rettungsmöglichkeit für betroffene Personen, Verhinderung der Brandausbreitung, Schutz von Sachwerten und Tieren.

**Anforderungsstufen für Bauteile:**
- feuerhemmend
- hochfeuerhemmend
- feuerbeständig

**Brandabschnitte:** Festlegung zulässiger Brandabschnittsgrößen und maximaler Abstände von Brandwänden; detaillierte Vorgaben zur Ausbildung von Brandwänden in den LBO.

**Sonderverordnungen** (ergänzend zu LBO, nicht in allen Bundesländern eingeführt): Versammlungsstätten, Geschäftshäuser, Garagen, Krankenhäuser, Hochhäuser.

#### 32.2 Richtlinien

Ergänzend zu Verordnungen: Industriebau- und Schulbau-Richtlinien sowie die Richtlinie für die Verwendung brennbarer Baustoffe im Hochbau. Richtlinien haben rechtlich anderen Stellenwert als Verordnungen.

#### 32.3 Normen

##### 32.3.1 DIN 4102 — Brandverhalten von Baustoffen und Bauteilen

Klassische Brandschutznorm, den Bauordnungen zugeordnet. Definiert Brennbarkeitsgrade von Baustoffen und Feuerwiderstandsfähigkeit von Bauteilen.

**Teile der DIN 4102:**
- Teil 1: Baustoffe — Begriffe, Anforderungen, Prüfungen
- Teil 2: Bauteile — Begriffe, Anforderungen, Prüfungen
- Teil 3: Brandwände und nichttragende Außenwände
- Teil 4: Katalog klassifizierter Baustoffe, Bauteile und Sonderbauteile
- Teil 5: Feuerschutzabschlüsse, Abschlüsse in Fahrschachtwänden
- Teil 6: Lüftungsleitungen
- Teil 7: Bedachungen
- Teil 8: Kleinprüfstand
- Teil 9: Kabelabschottungen
- Teil 11: Rohrummantelungen, Rohrabschottungen, Installationsschächte und -kanäle
- Teil 12: Funktionserhalt elektrischer Kabelanlagen
- Teil 13: Brandschutzverglasungen
- Teil 14: Bodenbeläge — Flammenausbreitung bei Wärmestrahler-Beanspruchung
- Teil 15: Brandschacht (Prüfgerät)
- Teil 16: Brandschachtprüfungen (Durchführung)
- Teil 17: Schmelzpunkt von Mineralfaserdämmstoffen
- Teil 18: Feuerschutzabschlüsse und Rauchschutztüren — Dauerfunktionstüchtigkeit
- Teil 19 (Entwurf): Wand- und Deckenbekleidung in Räumen — Versuchsraum
- Teil 20: Ergänzender Nachweis Außenwandbekleidungen — Wohnungsbrandszenario
- Teil 22: Anwendungsnorm auf Basis von Teilsicherheitsbeiwerten (zurückgezogen), Änderung A1
- Teil 24 (Entwurf): Ergänzender Nachweis Außenwandbekleidungen — Sockelbrandszenario

**Baustoffklassen nach DIN 4102-1:**

| Klasse | Bezeichnung | Beispiele |
|--------|-------------|-----------|
| A 1 | nichtbrennbar (klassisch) | Beton, Stahl, Ziegel, Kalksandstein |
| A 2 | nichtbrennbar (mit geringen brennbaren Anteilen, Prüfung bestanden) | Gipskartonplatten bestimmter Ausführung, Leichtbeton mit Polystyrolzuschlag |
| B 1 | schwerentflammbar | Holzwolle-Leichtbauplatte |
| B 2 | normalentflammbar | Holz |
| B 3 | leichtentflammbar | unbehandelte Polystyrol-Hartschaumplatten |

B3-Baustoffe dürfen nur eingesetzt werden, wenn sie werkmäßig mit anderen Baustoffen zu mindestens B2-Produkten verarbeitet wurden und diese Eigenschaft beim Einbau erhalten bleibt.

**Feuerwiderstandsklassen (FWK) F 30 bis F 180:**
Ein Bauteil wird in eine FWK eingestuft, wenn sein Prototyp (2 Prüfkörper) bei Normbrandbeanspruchung gemäß Einheitstemperaturzeitkurve über die jeweilige Prüfdauer die Normkriterien erfüllt.

**Raumabschluss-Kriterien (DIN 4102-2):**
- Feuerabgewandte Seite: mittlere Temperaturerhöhung maximal 140 K; Einzelmesswert maximal 180 K
- Keine Flammen oder heiße Gase an keiner Stelle des Bauteils (einschließlich Anschlüsse, Fugen, Stöße)
- Raumabschließende Wände müssen Pendelstoß von 20 Nm standhalten

**Tragfähigkeits-Kriterien:**
- Tragende Bauteile dürfen unter rechnerisch zulässiger Gebrauchslast nicht zusammenbrechen
- Nichttragende Bauteile dürfen unter Eigengewicht nicht versagen
- Durchbiegungsgeschwindigkeit bei statisch bestimmt gelagerten, biegebeanspruchten Bauteilen begrenzt (Grenzwert: Δf/Δt ≤ l² / (9000 × h), mit l = Stützweite in cm, h = statische Höhe in cm, Δf = Durchbiegungsintervall in cm je Minute)

**Brandwände (DIN 4102-3):**
Zusätzlich zu den F90-Anforderungen:
- Ausschließlich nichtbrennbare Baustoffe; günstige Wirkung von Putz oder Bekleidungen nicht anrechenbar
- Prüfung unter ausmittiger Vertikalbelastung
- Nach Brandbeanspruchung: Standhaltung gegen dreimaligen Pendelstoß von je 3000 Nm (Bleischrotsack)

**Nichttragende Außenwände:** Geringere Anforderungen als FWK-Wände — keine Begrenzung der Temperaturerhöhung auf feuerabgewandter Seite bei Innenbrandbeanspruchung; bei Außenbrandbeanspruchung abgeminderte Temperaturbeanspruchung.

**Ab 1. Juli 2012:** Eurocode-Nachweise (im genehmigten Anwendungsbereich) ersetzen tabellarische Bemessungen nach DIN 4102-4 und -22. DIN 4102-4 bleibt als Restnorm für nicht von Eurocodes erfasste Konstruktionen (raumabschließende Bauteile, Sonderbauteile) weiterhin unverzichtbar.

**Wichtige Teile für Bemessung:**
- Teil 2 und 3: Anforderungen an Bauteile und Sonderbauteile (inkl. Prüfvorschriften)
- Teil 4: Klassifizierungskatalog (macht Brandprüfungen häufig entbehrlich)
- Teil 8: Kleinprüfstand — ermittelt Wärmefreisetzung, Wärmedurchgang durch Dämmplatten, Schwelfeuerverhalten von dämmschichtbildenden Brandschutzbeschichtungen, Alterungsbeständigkeit
- Teil 14: Flammenausbreitung und Rauchentwicklung von Bodenbelägen → Grundlage für B1-Einstufung
- Teil 17: Schmelzpunkt Mineralfaserdämmstoffe — muss mindestens 1000 °C betragen, wenn Bauteil-FWK von Wärmebeständigkeit der Dämmschicht abhängt

##### 32.3.2 DIN 18009 — Brandschutzingenieurwesen, Teil 1

Anforderungen an Ingenieurmethoden des Brandschutzes für Gebäude und unterirdische Verkehrsanlagen. Zweck: Bewertung von Brandgefahren und Bemessung von Brandschutzmaßnahmen zur Erfüllung vorgegebener Schutzziele. Teil 1 = Rahmennorm; Teil 2 (in Planung) = Räumungssimulation und Personensicherheit.

##### 32.3.3 DIN 18230 — Baulicher Brandschutz im Industriebau

Ziel: Ermittlung der Feuerbeanspruchung tragender und raumabschließender Bauteile in Industriebauten durch Abbrand der im Brandbekämpfungsabschnitt vorhandenen Stoffe.

**Einflussfaktoren (gewichtet durch Bewertungsfaktoren im Berechnungsverfahren):**
- Brandlast (Größe und Anordnung im Abschnitt)
- Ventilationsbedingungen und Wärmeabzugsmöglichkeiten
- Größe des Brandbekämpfungsabschnittes
- Gebäudehöhe und Geschossanzahl
- Möglichkeit der Brandbekämpfung einschließlich automatischer Löschanlagen

Ergebnis: Brandschutzklassen für Einzelbauteile, die Feuerwiderstandsklassen nach DIN 4102 zugeordnet werden — Rückführung auf bewährte Normwelt. Randbedingungen für Anwendbarkeit in der Industriebau-Richtlinie.

##### 32.3.4 Muster-Verwaltungsvorschrift Technische Baubestimmungen (MVV TB)

Mit der Novellierung der Musterbauordnung 2016 wurden technische Regeln für Planung, Bemessung und Ausführung sowie für Bauprodukte in einem Dokument zusammengefasst.

**Struktur MVV TB:**
- Teile A und B: Vorschriften für Planung, Bemessung, Ausführung von Bauwerken
- Teil C: Regelungen für Bauprodukte ohne CE-Kennzeichnung nach BauPVO (EU) Nr. 305/2011; Festlegungen zu Produkten mit allgemeinem bauaufsichtlichem Prüfzeugnis
- Teil D: Informationen zu Produkten ohne bauaufsichtlichen Verwendbarkeitsnachweis; freiwillige Herstellerangaben zu Wesentlichen Merkmalen harmonisierter Bauprodukte

Bauregellisten A, B und C (bis 2016 gepflegt) wurden mit Einführung der MVV TB aufgehoben. Aktuelle MVV TB: www.dibt.de

#### 32.4 Europäische Brandschutznormung

##### 32.4.1 Klassifizierung von Baustoffen (Euroklassen)

Grundlage: Durchführungsverordnung Nr. 1062/2013 (auf Basis der Bauprodukte-Verordnung BauPVO). Klassifizierungsnorm: DIN EN 13501-1.

**Euroklassen (für Wand- und Deckenbekleidungen): A1, A2, B, C, D, E, F**

Für Bodenbeläge: analoge Klassen mit Index „fl" (z. B. Cfl); für elektrische Kabel: Index „ca".

Grenzwerte Euroklasse Cfl entsprechen der Baustoffklasse B1 nach DIN 4102-14.

**Zusatzklassen bei Prüfung im SBI (DIN EN 13823) und Kleinbrennertest (DIN EN ISO 11925-2):**
- Rauchentwicklung: s1 (gering), s2 (begrenzt), s3 (ohne Anforderung)
- Brennendes Abtropfen/Abfallen: d0 (keins), d1, d2

Insgesamt entstehen bis zu 40 Kombinationsmöglichkeiten der Baustoffklassifizierung.

**Prüfverfahren für Euroklassen (Tab. 32.1):**

| Klasse | ISO-Ofen (DIN EN ISO 1182) | Heizwert (DIN EN ISO 1716) | SBI (DIN EN 13823) | Kleinbrennertest (DIN EN ISO 11925-2) |
|--------|---------------------------|---------------------------|--------------------|-----------------------------------------|
| A1 | ✓ | ✓ | — | — |
| A2 | ✓* | ✓* | ✓ | ✓ |
| B | — | — | ✓ | ✓ |
| C | — | — | ✓ | ✓ |
| D | — | — | ✓ | ✓ |
| E | — | — | — | ✓** |
| F | — | — | — | — |

*Bei A2 kann zwischen ISO-Ofen und Heizwert gewählt werden.
**Bei E wurde die Anforderung nicht erreicht.

Bodenbeläge: SBI-Test ersetzt durch Radiant-Panel-Test (DIN EN ISO 9239-1, Proben horizontal). Zusätzlich Kleinbrennertest nach DIN EN ISO 11925-2 erforderlich.

**Zuordnung Euroklassen zu bauaufsichtlichen Anforderungen (Tab. 32.2, Auszug):**

| Bauaufsichtliche Anforderung | Bauprodukte allg. | Lineare Rohrdämmstoffe | Bodenbeläge |
|-----------------------------|-------------------|----------------------|-------------|
| nichtbrennbar | A2 – s1, d0 | A2L – s1, d0 | A2fl – s1, d0 |
| schwerentflammbar, nicht brennend abtropfend, geringe Rauch | C – s1, d0 | CL – s1, d0 | — |
| schwerentflammbar, nicht brennend abtropfend | C – s2, d0 | CL – s2, d0 | Cfl – s1 |
| schwerentflammbar, geringe Rauch | C – s1, d0 | CL – s1, d0 | Cfl – s1 |
| schwerentflammbar | C – s2, d2 | CL – s2, d2 | — |
| normalentflammbar, nicht brennend abtropfend | E – d2 | EL | — |
| normalentflammbar | E – d2 | EL – d2 | Efl |

Zusätzliche Anforderungen:
- Nichtbrennbar: Schmelzpunkt > 1000 °C soweit erforderlich
- Glimmverhalten: Prüfverfahren DIN EN 16733; Nachweis: kein kontinuierliches Schwelen

**Kurzzeichen-Erläuterung:**
- s (Smoke): Rauchentwicklung — s1 gering, s2 begrenzt
- d (Droplets): brennendes Abtropfen/Abfallen — d0 keines, d1/d2 vorhanden

Wichtig: Bisherige nationale Prüfergebnisse nach DIN 4102-1 („historic data") können für europäische Klassifizierung nicht verwendet werden, da sich die Prüfeinrichtungen (insbesondere SBI) geändert haben. Montage und Befestigung bei der Prüfung müssen der vorgesehenen Endanwendung entsprechen.

##### 32.4.2 Klassifizierung von Bauteilen (Europäisch)

Grundlage: DIN EN 13501-2 (Klassifizierung von Feuerwiderstandsprüfungen). Reihe fortgeführt durch:
- Teil 3: Haustechnische Anlagen — feuerwiderstandsfähige Leitungen, Brandschutzklappen
- Teil 4: Anlagen zur Rauchfreihaltung
- Teil 5: Bedachungen bei Außenbrandbeanspruchung

Ausgangspunkt war die international anerkannte ISO 834 (Brandverhalten von Bauteilen), um die herum national modifizierte Prüfverfahren entstanden. Diese nationalspezifischen Klassenbezeichnungen erschwerten eine einfache Harmonisierung.

**Prüfnorm-Reihen:**
- DIN EN 1363: allgemeine Anforderungen (Beheizung, Beanspruchungen, Kriterien)
- DIN EN 1364: nichttragende Bauteile
- DIN EN 1365: tragende Bauteile (geringste Abweichungen gegenüber DIN 4102)
- DIN EN 1366: Installationen (vielschichtig)
- DIN V ENV 13381: Bekleidungen und Schutzmaßnahmen (als Vornorm entwickelt)

**Feuerwiderstandsklassen nach DIN EN 13501-2 und bauaufsichtliche Zuordnung (Tab. 32.3):**

| Bauaufsichtliche Anforderung | Tragende Bauteile ohne Raumabschluss | Tragende Bauteile mit Raumabschluss | Nichtragende Innenwände | Nichtragende Außenwände |
|-----------------------------|--------------------------------------|--------------------------------------|------------------------|------------------------|
| feuerhemmend | R 30 | REI 30 | EI 30 | E 30 (i→o) + EI 30-ef (i←o) |
| hochfeuerhemmend | R 60 | REI 60 | EI 60 | E 60 (i→o) + EI 60-ef (i←o) |
| feuerbeständig | R 90 | REI 90 | EI 90 | E 90 (i→o) + EI 90-ef (i←o) |
| FWF 120 min | R 120 | REI 120 | — | — |
| Brandwand | — | REI 90-M | EI 90-M | — |

**Klassifizierungskriterien und Kurzzeichen (Tab. 32.4):**

| Symbol | Herleitung | Bedeutung |
|--------|-----------|-----------|
| R | Résistance | Tragfähigkeit |
| E | Étanchéité | Raumabschluss |
| I | Isolation | Wärmedämmung unter Brandeinwirkung |
| W | Radiation | Begrenzung des Strahlungsdurchtritts |
| M | Mechanical | Mechanische Einwirkung auf Wände (Stoßbeanspruchung) |
| Sm | Smokemax, leakage rate | Begrenzung der Rauchdurchlässigkeit |
| C | Closing | Selbstschließende Eigenschaft (inkl. Dauerfunktion, ggf. Lastspielanzahl) |
| P | — | Aufrechterhaltung Energieversorgung und/oder Signalübermittlung |
| K1, K2 | — | Brandschutzvermögen |
| I1, I2 | — | Unterschiedliche Wärmedämmungskriterien |
| i→o, i←o, i↔o | — | Richtung klassifizierter Feuerwiderstandsfähigkeit (innen/außen) |
| a↔b | — | Richtung klassifizierter FWF (oben/unten) |
| ve, ho | — | vertikal/horizontal |
| U/U, C/U, U/C | — | Rohrendenzustand offen (uncapped) / geschlossen (capped) innerhalb/außerhalb Prüfofen |

**Verwendbarkeitsnachweise (auch nach Einführung europäischer Klassifizierung gültig):**
- Allgemeine bauaufsichtliche Zulassung
- Allgemeines bauaufsichtliches Prüfzeugnis
- Zustimmung im Einzelfall

**Europäische Nachweise ergänzend:**
- Europäische (harmonisierte) Produktnormen
- Europäisch technische Bewertung (ETA) nach BauPVO mit CE-Zeichen
- Tabellenwerte der Eurocodes

##### 32.4.3 Eurocodes für Brandschutz

Die BauPVO enthält Brandschutzanforderungen zu: Tragfähigkeit, Feuer- und Rauchbegrenzung, Bewohnerschutz und Sicherheit der Rettungsmannschaften.

**Eurocodes (EC) mit Brandschutzteilen:**
- EC 1 (EN 1991): Einwirkungen auf Tragwerke
- EC 2 (EN 1992): Stahlbeton- und Spannbetontragwerke → EN 1992-1-2
- EC 3 (EN 1993): Stahlbauten → EN 1993-1-2 (EC3-1-2)
- EC 4 (EN 1994): Verbundtragwerke Stahl/Beton
- EC 5 (EN 1995): Holzbauwerke
- EC 6 (EN 1996): Mauerwerksbauten
- EC 9 (EN 1999): Aluminiumkonstruktionen

**Verbindlich in Deutschland ab 1. Juli 2012** (Bayern: Übergangsfrist bis 31. Dezember 2013). Brandschutzteile sind als „Teil 1–2" den jeweiligen Eurocodes angegliedert.

**Einheitliche Gliederung der Brandschutzteile:**
- Kapitel 1: Einführung, Ziel, Definition, Symbole
- Kapitel 2: Grundprinzipien
- Kapitel 3: Materialeigenschaften
- Kapitel 4: Tragwerksbemessung für Brandfall
- Kapitel 5: Bauartenspezifische Detailangaben
- Normative und informative Anhänge

Nationale Anhänge (NDP — National festzulegende Parameter) regeln nationale Entscheidungen: Zahlenwerte und Klassen, landesspezifische Daten (z. B. Schneekarten), Verfahrenswahl, NCCI (Non Contradictory Complementary Information). Beispiele: EC2-1-2 hat 16 nationale Festlegungen, EC3-1-2 hat 5.

**Drei Nachweisebenen für Standsicherheit im Brandfall:**
1. Tabellarisches Bemessungsverfahren (wie bisher nach DIN 4102, für Einzelbauteile)
2. Vereinfachte Rechenverfahren (Näherungsmethoden, für Bauteile und Tragwerksausschnitte)
3. Allgemeines Rechenverfahren (computergestützt, Gesamt- und Teiltragswerke)

**Für Nachweise, die in Eurocode-Brandschutzteilen nicht geregelt sind:** Bemessung nach DIN 4102-4 weiterhin zulässig.

**Materialkennwerte in Eurocode-Brandschutzteilen:** Rechenfunktionen für thermisches und mechanisches Verhalten; auf hohen Detaillierungsgrad (Legierungszusammensetzung, Feuchtetransporte) zugunsten einfacher mathematischer Beschreibungen verzichtet.

**Nachweis-Hierarchie nach Nachweisgegenstand:**
- Gesamttragwerk: nur allgemeine Rechenverfahren geeignet (temperaturabhängige Steifigkeitsveränderungen, thermische Ausdehnungen)
- Tragwerksausschnitte: vereinfachte Rechenverfahren
- Einzelbauteile: tabellarisches oder vereinfachtes Verfahren

### Kapitel 33 — Grundlagen des Brandes und Verlauf (Beginn)

**Vier Voraussetzungen für Brandentstehung:**
1. Brennbarer Stoff vorhanden
2. Ausreichende Sauerstoffmenge
3. Ausreichend hohe Zündenergie bzw. Zündtemperatur
4. Ausreichendes Mischungsverhältnis

Sind alle vier Bedingungen erfüllt, kommt es zur Entzündung und der Übergang zum offenen Brand ist wahrscheinlich.

#### 33.1 Pyrolyse und Verbrennung

Vor dem offenen Brand laufen physikalisch-chemisch mehrere Prozesse ab:
- Pyrolyse-/Zersetzungsprozess: brennbare Gase werden aus dem Brennstoff freigesetzt
- Verbrennung: in der Gasphase erfolgt die eigentliche Verbrennungsreaktion

**Thermische Stabilität:** Beschreibbar durch Abhängigkeit der relativen Zersetzungsrate von der Temperatur T. Die Moleküle des Stoffes zerfallen in kleinere Moleküle.

**Unterschied fest vs. flüssig bei der Vergasung:**
- Flüssigkeiten: Phasenwechsel nicht notwendigerweise mit chemischer Veränderung verbunden
- Feste Stoffe: Pyrolyse = endothermer Prozess durch mehrere chemische Reaktionen
