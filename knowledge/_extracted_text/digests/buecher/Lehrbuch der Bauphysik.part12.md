# Lehrbuch der Bauphysik — Teil 12
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 481-520.

Dieser Teil umfasst das Ende des Literaturverzeichnisses zu Kapitel 16 (Außenklima) sowie vollständig Kapitel 17 (Charakterisierung des Raumklimas) und den Beginn von Kapitel 18 (Raumklima bei quasifreier Klimatisierung). Behandelt werden thermische Behaglichkeit, Raumluftfeuchte, Taupunktberechnung, Raumklimaklassen sowie die Energiebilanz-Modellierung zur Ermittlung der Raumlufttemperatur.

## Inhalt

### Kapitel 17: Charakterisierung des Raumklimas (Seiten 482–498)

#### 17.0 Einführung und Klimaparameter

Für die hygrothermische Bemessung von Bauteilen sind neben dem Außenklima auch die raumseitigen Klimakomponenten zu quantifizieren. Das Raumklima dient einerseits der Eigensicherung des Gebäudes, andererseits der Funktionssicherung (Behaglichkeit in Wohn-/Bürobauten, Sonderklimate in Produktionshallen, Museen usw.).

Maßgebliche Raumklimaparameter:
- Lufttemperatur θi in °C
- Oberflächentemperatur der Raumumschließungsflächen θsi bzw. θoi in °C
- Empfindungstemperatur θE in °C
- Absolute Luftfeuchte x in kg Dampf/kg Luft; Partialdruck des Wasserdampfs pDi in Pa
- Relative Luftfeuchte fi in % oder dimensionslos
- Strömungsgeschwindigkeit der Raumluft vLi in m/s
- Luftwechselrate nL in 1/h oder Lüftungsvolumenstrom dVL/dt in m³/h bzw. m³/(h·Person)

#### 17.1 Raumtemperaturen

##### 17.1.1 Energieumsatz des Menschen

Thermische Behaglichkeit erfordert ein Gleichgewicht zwischen der im menschlichen Körper erzeugten Wärmeleistung Fe und dem abgegebenen Wärmestrom Fa, bei minimalem physiologischem Thermoregulationsaufwand.

Die abgegebene Wärmeleistung hängt ab von:
- Umgebungstemperatur (genauer: Empfindungstemperatur)
- Körperlicher Tätigkeit
- Wärmewiderstand der Bekleidung

In der Bekleidungshygiene wird der Wärmewiderstand in der Einheit **clo** angegeben:
- 1 clo = 0,15 m²K/W (Umrechnung)

**Aktivitätsstufen und Wärmeabgabe:**

| Aktivitätsstufe | Beschreibung | Wärmeleistung |
|---|---|---|
| Grundumsatz | Ruhender Zustand | 85 W |
| Aktivität 1 | Ruhiges Sitzen | 100 W (bei 20 °C) |
| Aktivität 2 | Leichte Tätigkeit | 100–150 W |
| Aktivität 3 | Mittelschwere Tätigkeit | 150–200 W |
| Aktivität 4 | Schwere Tätigkeit | 200–300 W |
| Aktivität 4 (max) | Sehr schwere Tätigkeit | bis 700 W |

Bei sehr hohen Umgebungstemperaturen oder schwerer körperlicher Arbeit erfolgt die Entwärmung ausschließlich über die feuchte Wärmeabgabe (Verdunstungskühlung bei Phasenumwandlung flüssig/gasförmig). Dieser Zustand wird nicht mehr als behaglich empfunden.

Der Grundumsatz von Warmblütern in Abhängigkeit von der Körpermasse folgt einer Geradengleichung im doppeltlogarithmischen Maßstab; für 80 kg Körpermasse ergibt sich dabei 100 W.

**Produktivitätsabfall mit steigender Empfindungstemperatur:**
- Bei θE > 20 °C sinkt die körperliche und geistige Arbeitsproduktivität spürbar
- Bei 26 °C beträgt sie nur noch etwa 2/3 des Ausgangswerts
- Grenzwert für die warme Jahreszeit: θE max = 26 °C
- Behaglichkeitsbereich: 18 °C bis 23 °C

##### 17.1.2 Raumlufttemperatur, Umschließungsflächentemperatur und Empfindungstemperatur

Der Körper gibt trockene Wärme konvektiv an die Raumluft (hc) und durch Strahlung an die Raumumschließungsflächen (hr) ab. Beispielwerte für die Koeffizienten:
- hc = 3,5 W/m²K (konvektiver Wärmeübergangskoeffizient)
- hr = 4,5 W/m²K (radiativer Wärmeübergangskoeffizient)

Körper-Beispielparameter:
- θsKörper = 26 °C (Hauttemperatur)
- θi = 20 °C (Raumluft)
- θsWand = 17 °C (Wandoberfläche)
- A = 1,8 m² (Körperoberfläche)
- Resulting Wärmeabgabe Φa = 110,7 W

Die **Empfindungstemperatur θE** ist definiert als gewichtetes Mittel aus Raumlufttemperatur und mittlerer Umschließungsflächentemperatur:

θE = (hc · θi + hr · θsWand) / (hc + hr)

Mit den Beispielwerten ergibt sich θE = 18,3 °C.

Konsequenzen:
- Kalte Wände lassen sich durch höhere Raumlufttemperatur kompensieren
- Umgekehrt kann die Raumlufttemperatur abgesenkt werden, wenn Raumflächen wärmer sind
- Die Temperatur der Raumumschließungsfläche darf aus hygienischen Gründen (Wärmeentzug durch Strahlung, Fußwärmeableitung) nicht unter 17 °C fallen (gilt nicht für Fenster)
- Aus bauphysikalischer Sicht darf sie nicht unter die Taupunkttemperatur bzw. unter die kritische Schimmeltemperatur (rel. Feuchte = 80 %) sinken

**Optimale Empfindungstemperatur** in Abhängigkeit von Bekleidungswärmewiderstand R und Wärmeproduktionsrate Φe (Formel 17.4, grafisch in Abb. 17.6).

**Richtwerte für optimale Empfindungstemperaturen:**
- Heizperiode: θi = 19 °C bis 20 °C
- Sommer: θi < 26 °C

**Bekleidungswärmewiderstand (Tabelle 17.1):**

| Wärmewiderstand [m²K/W] | clo-Wert | Typische Bekleidung |
|---|---|---|
| 0,000 | 0,000 | Unbekleidet |
| 0,020 | 0,133 | Tropische Bekleidung |
| 0,060 | 0,400 | Leichte Sommerbekleidung Mitteleuropa |
| 0,080 | 0,533 | Leichte Arbeitsbekleidung |
| 0,120 | 0,800 | Typische Winterbekleidung Wohnraum |
| 0,220 | 1,467 | Typische Winterbekleidung Büro |
| 0,300 | 2,000 | Typische Straßenbekleidung Frühjahr/Herbst |

(Zwischenwerte in Schritten von 0,020 m²K/W bzw. 0,133 clo vorhanden)

#### 17.2 Raumluftfeuchte

##### 17.2.1 Relative Luftfeuchtigkeit

Feuchte Luft ist ein Gemisch aus trockener Luft und Wasserdampf. Der Feuchtegehalt kann angegeben werden als:
- Partialdruck des Wasserdampfs pD in Pa
- Absolute Feuchte f = mD/VL in kg/m³ oder x = mD/mL in kg/kg
- Relative Luftfeuchtigkeit: ϕ = pD/pS (Verhältnis Dampfdruck zu Sättigungsdruck)

Der Feuchtegehalt der Raumluft ergibt sich aus:
- Raumlufttemperatur
- Ergiebigkeit der Feuchtequellen im Raum
- Temperatur und relativer Feuchte der Außenluft
- Luftvolumenstrom bzw. Luftwechselrate zwischen Außen- und Raumluft
- Feuchtespeichervermögen der Raumumschließungsflächen und Einrichtungsgegenstände

Außenluftströme dienen neben der Feuchteregulierung auch der Sauerstoffzufuhr und dem Abtransport von Luftverunreinigungen.

**Richtwerte Luftvolumenstrom (Tabelle 17.2-Beschreibung):**
- Spalte 0: personenbezogener Luftstrom in m³/(h·Person)
- Spalte 1: nutzflächenbezogener Luftstrom in m³/(m²·h)
- Spalte 2: Luftwechselrate in 1/h

**Feuchtebilanz (Gleichung 17.5):**
Die Gesamtbilanz des Wasserdampfstroms in einem Raum lautet:
Zugeführte Feuchte + Produzierte Feuchte = Abgeführte Feuchte + Gespeicherte Feuchte

Kenngrößen:
- RD = 462 Ws/(kgK) — Gaskonstante für Wasserdampf
- Die Luftwechselrate nL (1/h) und das Raumvolumen Vi (m³) bestimmen den Volumenstrom: dV/dt = nL · Vi

**Berechnungsformel für die relative Raumluftfeuchte (Gleichung 17.10):**
ϕi = f(nL, mptV, θe, θi)

wobei mptV die volumenbezogene Feuchteproduktionsrate in kg/(m³·h) ist.

**Typische Luftwechselraten bei Fensterlüftung:**
- Fenster geschlossen: 0 bis 0,5 /h
- Fenster gekippt: 0,8 bis 4,0 /h
- Fenster geöffnet (einseitig): 5,0 bis 15,0 /h
- Fenster geöffnet (Querlüftung): bis 40 /h

**Berechnungsbeispiel:**
- Außenklima: θe = −5 °C, ϕe = 0,8 (80 %)
  - pse(θe) = 610,5 Pa
- Raumklima: θi = 20 °C
  - psi(θi) = 2335,3 Pa
- Feuchteproduktionsrate mptV = 0,004 kg/(m³·h) (typisch: Bewohner, Zimmerpflanzen, Kochen)
- Luftwechselrate nL = 0,7 /h
- Ergebnis: ϕi ≈ 47 %

Ohne jede Feuchtequelle im Raum liefert trockene kalte Außenluft (−5 °C, 80 % r.F.) nach Erwärmung auf 20 °C nur noch etwa 13,7 % relative Feuchte im Raum.

Werte > 100 % in der Tabelle bedeuten: Tauwasserbildung in der Raumluft oder an kälteren Bauteiloberflächen (physikalisch nicht darstellbar).

**Relative Luftfeuchte als Funktion von nL und mptV (Tabelle 17.2, Auszug):**

| mptV [kg/m³h] | nL=0,2 | nL=0,4 | nL=0,6 | nL=0,8 | nL=1,0 | nL=2,0 | nL=4,0 |
|---|---|---|---|---|---|---|---|
| 0,000 | 13,7 | 13,7 | 13,1 | 13,7 | 13,7 | 13,7 | 13,7 |
| 0,001 | 42,7 | 28,2 | 23,4 | 21,0 | 19,5 | 16,6 | 15,2 |
| 0,002 | 71,7 | 42,7 | 33,1 | 28,2 | 25,3 | 19,5 | 16,6 |
| 0,003 | 100,7 | 57,2 | 42,7 | 35,5 | 31,1 | 22,4 | 18,1 |
| 0,004 | — | 71,7 | 52,4 | 42,7 | 36,9 | 25,3 | 19,5 |
| 0,005 | — | 86,2 | 62,0 | 50,0 | 42,7 | 28,2 | 21,0 |
| 0,006 | — | 100,7 | 71,7 | 57,2 | 48,5 | 31,1 | 22,4 |
| 0,008 | — | — | 91,0 | 71,7 | 60,1 | 37,5 | 25,3 |
| 0,010 | — | — | — | 86,2 | 71,7 | 45,9 | 28,2 |

(Alle Werte in %, Außenklima: −5 °C, 80 % r.F.)

**Jahresgang der Raumluftfeuchte:**
Unter Verwendung des ARY-Außenklimas (harmonische Funktionen für Temperatur, Sättigungsdruck, Feuchte) lässt sich die Raumluftfeuchte im Jahresverlauf berechnen. Dabei schwankt die Luftwechselrate:
- Winterminimum: nL = 1,2 /h
- Sommermaximum: nL = 2,2 /h
- Feuchteproduktionsrate: ca. 4,5 g/(m³·h) als Mittelwert

Der Jahresgang lässt sich näherungsweise als harmonische Funktion mit einer Zeitverschiebung von 20 Tagen darstellen:
- Minimum im Januar: ϕi ≈ 43 %
- Maximum im Juli: ϕi ≈ 62 %

Messwerte aus einem Testhaus Dresden-Talstraße (1997) zeigen ein ähnliches Verhalten, jedoch durch die Feuchtepufferung der Raumumschließungsfläche gedämpfte Schwankungen.

##### 17.2.2 Enthalpie und Wasserdampfgehalt — h-x-Diagramm

Grundlage bilden die Gasgleichungen für Wasserdampf und Luft:
- Gaskonstante Wasserdampf: RD = 462 Ws/(kgK)
- Gaskonstante Luft: RL = 287 Ws/(kgK)

Absolute Feuchte x in kg/kg:
- x = (RD/RL) · (pD/pL) ≈ 0,622 · pD/(p − pD)
- Alternativ: x = 0,622 · ϕ · ps(θ) / (p − ϕ · ps(θ))

Relative Luftfeuchte als Funktion von x und θ:
- ϕ(x,θ) = x / (x + 0,622) · p / ps(θ)

Feuchte Luft ist grundsätzlich leichter als trockene Luft (geringere Dichte).

Spezifische Enthalpie feuchter Luft (isobare Zustandsänderung):
- h = hL + x(θ) · hD
- hL = cpL · (θ − θ0); cpL = 1000 Ws/(kgK)
- hD = cpD · (θ − θ0) + r; cpD = 1860 Ws/(kgK)
- r = 2,5 · 10⁶ Ws/kg (spezifische Phasenumwandlungsenthalpie, flüssig → gasförmig)

**Berechnungsbeispiel (Abkühlung feuchter Luft):**
- 50 kg feuchte Luft (θ1 = 35 °C, ϕ1 = 50 %, p = 101,3 kPa)
- Abkühlung auf θ2 = 20 °C (dabei ϕ2 = 100 %, Tauwasserbildung)
- x1(35 °C) = 0,0177 kg/kg
- x2(20 °C) = 0,0147 kg/kg
- Kondensatmenge: mK = mL · (x1 − x2) = 50 · (0,0177 − 0,0147) = 0,152 kg = 152 g
- Frei werdende Energiemenge: ΔH = Δh · mL = 1165 · 10⁶ Ws = 324 kWh

##### 17.2.3 Taupunkttemperatur

Wird feuchte Luft mit Temperatur θ und relativer Feuchte ϕ abgekühlt, steigt ϕ an. Ab ϕ = 1 (Sättigung) bildet sich Tauwasser. Die **Taupunkttemperatur θT** ist jene Temperatur, bei der der vorhandene Partialdruck gerade zum Sättigungsdruck wird.

Berechnungsformel (Gleichung 17.21):
θT(θ, ϕ) = 0,1247 · (109,8 + θ · ϕ) / (109,8 − θ · ϕ)

(für Taupunkttemperaturen < 0 °C muss die Sublimationskurve statt der Sättigungsdruckkurve verwendet werden)

**Wichtige Stützwerte:**
- θ = 20 °C, ϕ = 60 % → θT = 12 °C
- θ = 5 °C, ϕ = 10 % → θT = −21,2 °C (Reifbildung)
- θ = 35 °C, ϕ = 90 % → θT = 33,1 °C (kritisch bei Raumkühlung)

**Taupunkttemperaturen (Tabelle 17.3, Gültigkeitsbereich):**
- Lufttemperatur θ: 5 °C bis 40 °C (Schritte 5 K)
- Relative Feuchte ϕ: 10 % bis 90 % (Schritte 10 %)
- Hervorgehobener Wert: θ = 20 °C, ϕ = 60 %, θT = 12 °C

Bauphysikalische Pflicht: An und in den Bauteilen ist Tauwasser zu vermeiden bzw. zu begrenzen. Dazu muss die Oberfläche stets wärmer als die Taupunkttemperatur bleiben.

#### 17.3 Raumklimaklassen

Auf Basis unterschiedlicher Feuchteproduktionsraten werden vier Raumklimaklassen definiert und daraus Jahresgänge (Monatsmittelwerte) der relativen Raumluftfeuchte ermittelt.

**Raumklimaklassen (Tabelle 17.4):**

| Klasse | Feuchteproduktionsrate | Feuchtebelastung |
|---|---|---|
| 1 | 0,002 kg/(m³·h) | Niedrig |
| 2 | 0,004 kg/(m³·h) | Normal |
| 3 | 0,006 kg/(m³·h) | Hoch |
| 4 | 0,008 kg/(m³·h) | Sehr hoch |

Berechnungsrandbedingungen für Klasse 2:
- Luftwechselrate zwischen 0,7/h (Winter) und 1,3/h (Sommer) bei freier Fensterlüftung
- Raumlufttemperatur zwischen 19 °C (Winter) und 25 °C (Sommer)

**Monatsmittelwerte der relativen Raumluftfeuchte (Tabelle 17.5/17.6):**

| Monat | θi [°C] | ϕ (Klasse 1) | ϕ (Klasse 2) | ϕ (Klasse 3) | ϕ (Klasse 4) |
|---|---|---|---|---|---|
| Jan | 19,0 | 0,348 (35 %) | 0,511 (51 %) | 0,674 (67 %) | 0,811 (81 %) |
| Feb | 19,3 | 0,337 (34 %) | 0,494 (49 %) | 0,650 (65 %) | 0,777 (78 %) |
| März | 20,2 | 0,381 (38 %) | 0,515 (52 %) | 0,649 (65 %) | 0,757 (76 %) |
| April | 21,7 | 0,448 (45 %) | 0,556 (56 %) | 0,664 (66 %) | 0,744 (74 %) |
| Mai | 23,2 | 0,526 (53 %) | 0,615 (62 %) | 0,703 (70 %) | 0,764 (76 %) |
| Juni | 24,4 | 0,577 (58 %) | 0,654 (65 %) | 0,730 (73 %) | 0,775 (78 %) |
| Juli | 24,9 | 0,619 (62 %) | 0,690 (69 %) | 0,762 (76 %) | 0,800 (80 %) |
| Aug | 24,7 | 0,607 (61 %) | 0,681 (68 %) | 0,754 (75 %) | 0,796 (80 %) |
| Sept | 23,7 | 0,560 (56 %) | 0,643 (64 %) | 0,726 (73 %) | 0,779 (78 %) |
| Okt | 22,3 | 0,493 (49 %) | 0,593 (59 %) | 0,693 (69 %) | 0,766 (77 %) |
| Nov | 20,8 | 0,432 (43 %) | 0,556 (56 %) | 0,680 (68 %) | 0,780 (78 %) |
| Dez | 19,6 | 0,382 (38 %) | 0,532 (53 %) | 0,681 (68 %) | 0,806 (81 %) |

**Auswertung:**
- Niedrige Feuchteproduktionsrate (Klasse 1) führt vor allem im Winter zu sehr trockener Raumluft (ϕi ≈ 35 %)
- Klasse 4 mit ϕi bis 80 % begünstigt grundsätzlich Schimmelbildung an Außenbauteiloberflächen
- Im Sommer rücken alle Kurven zusammen (höhere absolute Feuchte der Außenluft)
- Klasse 2 gilt als Normverlauf für Wohngebäude in Mitteleuropa bei freier Klimatisierung; empfohlen als Bemessungsgrundlage, wenn keine genaueren Messwerte vorliegen

**Vereinfachte Eckwerte für relative Raumluftfeuchte im Wohnungsbau:**
- Wohnräume mit kontinuierlichem Heizbetrieb: ϕWinter < 50 %, ϕSommer = 60 %
- Wohnräume mit diskontinuierlichem Heizbetrieb: ϕWinter < 60 %, ϕSommer = 60 %

#### 17.4 Einfluss der Raumluftparameter auf die Behaglichkeit

Der physiologisch optimale Bereich und der Erträglichkeitsbereich für die Empfindungstemperatur werden von Tätigkeit, Luftfeuchte und Luftgeschwindigkeit bestimmt.

**Luftfeuchte:**
- Raumluft > 80 % r.F. wird ab ca. 23 °C als schwül empfunden (feuchte Körperentwärmung behindert)
- Raumluft < 20 % r.F. führt zur Reizung der Schleimhäute
- Im relevanten Behaglichkeitsbereich ist der Körper gegenüber der Luftfeuchte relativ tolerant

**Luftgeschwindigkeit (Zugempfindung):**
Maximale Luftgeschwindigkeit ohne Zugempfindung abhängig von der Raumlufttemperatur (Gleichung 17.19):
- vmax [m/s] ≤ (0,59 − 0,04 · (16 − θi)) · [m/s] für 16 °C ≤ θi ≤ 26 °C

Die Strömungsverhältnisse in Räumen lassen sich analytisch nur grob erfassen; für genaue Berechnungen ist CFD erforderlich.

**Fanger-Bewertungsmodell:**
P. O. Fanger entwickelte 1967 einen umfassenden Ansatz zur physiologischen Gesamtbewertung des Raumklimas. Die Europäische Norm (DIN EN ISO 77) basiert auf diesem Modell.

Die thermische Belastung pro Hautflächeneinheit und Stunde ergibt sich aus der Wärmeproduktion abzüglich der Verluste durch:
- Dampfdiffusion und Schwitzen
- Trockene und feuchte Atmungsverluste
- Wärmeleitung über Bekleidung
- Strahlung und Konvektion

Eingangsvariablen des Modells:
- Wasserdampfpartialdruck (Umgebung)
- Lufttemperatur
- Mittlere Strahlungstemperatur der Umgebungsflächen
- Luftgeschwindigkeit
- Wärmeproduktionsrate (Aktivität)
- Relative Luftgeschwindigkeit an der Körperoberfläche
- Bekleidungsparameter (Verhältnis bekleideter zu unbekleideter Fläche, Wärmewiderstand)
- Mittlere Hauttemperatur

**Bewertungsindex PMV (Predicted Mean Vote):**
- 7-Punkte-Skala: −3 (sehr kalt) bis +3 (sehr warm)
- Behaglichkeitsbereich: −1 (kühl) bis +1 (warm), Optimum bei 0
- Faktoren wie Geschlecht, Alter, Konstitution, Gewicht und Nationalität haben bei geringen Aktivitätsgraden keinen signifikanten Einfluss

**PPD-Index (Predicted Percentage of Dissatisfied):**
Gibt an, welcher Anteil einer Nutzergruppe das Raumklima mit |PMV| > 0,5 bewertet (d. h. unzufrieden ist).

Berechnungsformel (Gleichung 17.20):
PPD = 100 − 95 · exp(−0,03353 · PMV⁴ − 0,2179 · PMV²)

- Erreichbarer Minimalwert: PPD = 5 % (bei PMV = 0)
- Zusammenhang zwischen PMV und thermischer Belastung wurde aus Klimakammerstudien empirisch ermittelt

---

### Kapitel 18: Raumklima bei quasifreier Klimatisierung (Seiten 501–510)

#### 18.1 Vorbemerkung

**Freie (autogene) Klimatisierung:** Das Gebäude klimatisiert sich selbst ohne Zufuhr von Aufbereitungsenergie. Grundvoraussetzungen:
- Ausreichender Wärmewiderstand der Hüllkonstruktion
- Ausreichende Wärme- und Feuchtespeicherung des Baukörpers
- Klimaangepasstes Lüftungsregime

**Erzwungene (energogene) Klimatisierung:** Raumklima wird durch Heiz- oder Kühlenergie aktiv erzeugt. Raumlufttemperatur bleibt dabei annähernd konstant, weswegen das thermische Zeitverhalten des Baukörpers von geringerer Bedeutung ist. Relevante Baukörpereigenschaften beschränken sich im Wesentlichen auf:
- Wärmewiderstand der Hüllkonstruktion (dominant)
- Dämpfung instationärer Lastanteile (Strahlungs- und innere Wärmelasten)

In Mitteleuropa wird ein Gebäude im Regelfall nur beheizt. Daher muss:
- Die Hüllkonstruktion auf die Heizphase abgestimmt sein
- Das Gebäude gleichzeitig den Anforderungen der freien Klimatisierung im Sommer genügen

Bei beheiztem Gebäude: Raumlufttemperatur wird durch Heizenergie auf Sollwert gehalten, der Wasserdampfgehalt stellt sich frei ein. Nur bei speziellen Nutzungsanforderungen (z. B. Museen) wird auch der Feuchtegehalt durch Klimaanlagen geregelt.

Bei freier Klimatisierung folgt das Raumklima dem Außenklima. Änderungen werden vom Baukörper gedämpft — sowohl thermisch (Wärmeabsorptionsvermögen) als auch hygrisch (hygrisches Absorptionsvermögen).

**Bemessungsanforderung Sommer:** Unter extremen sommerlichen Bedingungen darf die zulässige Raumlufttemperatur (θE,max = 26 °C) nicht überschritten werden.

**Programm CLIMT (Climate-Indoor-Moisture-Temperature):** Analytisches Berechnungsmodell und nutzerfreundliches Windows-Programm für Raumlufttemperatur und relative Raumluftfeuchte bei quasi-freier Klimatisierung. Validiert durch Vergleich mit TRNSYS-Rechenwerten und Messwerten in zwei Testgebäuden.

#### 18.2 Modellierung der Energiebilanzen zur Ermittlung der Raumlufttemperatur im Jahresverlauf

Das Modell basiert auf drei gekoppelten Wärmestrombilanzen:
1. Wärmestrombilanz für die Außenoberfläche der opaken Bauteile
2. Wärmestrombilanz für die Raumluft
3. Wärmestrombilanz für die innere Raumumschließungsfläche

Lösungsansatz: Alle thermischen Belastungen werden innerhalb jedes einstündigen Zeitintervalls als konstant angenommen, ändern sich danach sprungartig. Dadurch können sowohl harmonische (Außentemperatur) als auch sprungförmige (Lüftung, innere Quellen) Belastungen abgebildet werden. Das Ergebnis sind 8760 Stundenwerte (Jahresgang).

##### 18.2.1 Wärmestrombilanz für die äußere Oberfläche der opaken Bauteile

Bilanzgleichung (18.1): ΦSWe = ΦSPe + ΦTW + ΦUe

Einzelterme:
- **ΦSWe** (Gl. 18.2): Absorbierter kurzwelliger Strahlungswärmestrom an der Außenoberfläche; a = Absorptionskoeffizient der Außenoberfläche
- **ΦSPe** (Gl. 18.3): Wärmestrom in die außenseitige speicherwirksame Bauwerksmasse; Ce = ce·me = Wärmekapazität der äußeren speicherwirksamen Masse in Ws/K
- **ΦTW** (Gl. 18.4): Durch die Konstruktion von Außen- nach Innenoberfläche geleiteter Wärmestrom; U′ = spezifischer Wärmedurchgangswert der Wand ohne Wärmeübergangswiderstände in W/(m²K); T′W = U′ · AW = Wärmedurchgangswert der Wand in W/K; 1/T′W = Wärmedurchlasswiderstand in K/W
- **ΦUe** (Gl. 18.5): Von der Außenoberfläche an die Umgebung abgegebener Wärmestrom; he = äußerer konvektiver und radiativer Wärmeübergangskoeffizient; Üe = he · AWe = äußerer Übergangswert in W/K

##### 18.2.2 Wärmestrombilanz für den Raum (Raumluft)

Bilanzgleichung (18.6): ΦL + ΦTF + ΦUi + Φci = ΦSPi (= 0, da Luftwärmespeicherung vernachlässigt)

Einzelterme:
- **ΦL** (Gl. 18.7): Lüftungswärmestrom; L = ρL · cpL · nL · Vi = temperaturbezogener Lüftungswärmestrom in W/K
- **ΦTF** (Gl. 18.8): Transmissionswärmestrom durch Fenster; UF = Wärmedurchgangskoeffizient Fenster in W/(m²K); TF = UF · AF in W/K; 1/TF = Durchgangswiderstand Fenster in K/W
- **ΦUi** (Gl. 18.9): Konvektiver Wärmeübergang von der inneren Raumumschließungsfläche an die Raumluft; Üi = hci · AWi = innerer Übergangswert in W/K; 1/Üi = innerer Wärmeübergangswiderstand
- **Φci** (Gl. 18.10): Konvektiver Anteil der inneren Wärmequellen (J = Gesamtleistung in W); Φci = J/2
- **ΦSPL** (Gl. 18.11): Wärmestrom in die Raumluft (Speicherung); CL = Wärmekapazität der Luft; wegen geringer Dichte vernachlässigt

##### 18.2.3 Wärmestrombilanz für die innere Raumumschließungsfläche

Bilanzgleichung (18.12): ΦSF + ΦTW + ΦUi + Φri = ΦSPi

Einzelterme:
- **ΦSF** (Gl. 18.13): Durch Fenster eindringender Strahlungswärmestrom; fR = Rahmenfaktor (Glasflächenanteil); z = Verschattungsgrad; g = Glasdurchlasskoeffizient; G = spezifischer Strahlungswärmestrom in W/m²; SF = fR · z · g · G · AF
- **ΦTW** (Gl. 18.14): Von der Außen- zur Innenoberfläche durch die Wand geleiteter Wärmestrom (wie in 18.2.1)
- **ΦUi** (Gl. 18.15): Konvektiver Wärmeübergang zwischen Innenoberfläche und Raumluft (wie in 18.2.2)
- **Φri** (Gl. 18.16): Radiativer Anteil der inneren Wärmequellen; Φri = J/2
- **ΦSPi** (Gl. 18.17): In die speicherwirksame innere Bauwerksmasse gespeicherter Wärmestrom; Ci = ci · mi = Wärmekapazität der inneren speicherwirksamen Masse in Ws/K

**Vereinfachtes Differenzialgleichungssystem (Gleichungen 18.18–18.20):**

1. Bilanz Außenoberfläche: S · (θoe − θe) + Üe · (θoe − θe) + T′W · (θoe − θoi) + Ce · dθoe/dt = 0
2. Bilanz Raumluft: (L + TF) · (θe − θi) + Üi · (θoi − θi) + J/2 = 0
3. Bilanz Raumumschließungsfläche: Ci · dθoi/dt = SF + T′W · (θoe − θoi) + Üi · (θoi − θi) + J/2

Die Wärmespeicherung der Raumluft wird wegen der geringen Luftdichte vernachlässigt.

**Lösung — Exponentialfunktion für die Innenoberflächentemperatur (Gleichung 18.21):**
θoi,j+1 = θoiLIM,j + (θoi,j − θoiLIM,j) · exp(−βj · Δt)

Darin ist:
- θoi,j = Ausgangstemperatur zu Beginn des Zeitintervalls j
- θoiLIM,j = fiktive Endtemperatur nach unendlich langer Aufheiz-/Abkühlzeit mit den Belastungsgrößen im Intervall j

**Fiktive Endtemperatur θoiLIM,j (Gleichung 18.22):**
Hängt ab von Strahlungsbelastungen SF und SW, der inneren Belastung J sowie den Übertragungswiderständen 1/T′W, 1/(Lj+TF), 1/Üe, 1/Üi.
- Steigt mit Strahlungsbelastung und inneren Wärmequellen
- Sinkt mit der Luftwechselrate
- Wärmespeicherkapazitäten Ci und Ce fließen in die fiktive Endtemperatur nicht ein, aber in das Zeitverhalten

**Zeitkonstante und Einstellzeit (Gleichungen 18.23–18.26):**
- βj = Zeitkonstante (1/s), abhängig von Ce, Ci und allen Übertragungswerten
- τ = 3/Bj = Einstellzeit in Sekunden (Zeit bis ~95 % des Endwerts)
- Die Wärmekapazität der inneren Oberfläche Ci geht dominierend ein (wegen größerer Fläche)

**Speicherwirksame Bauwerksmasse (Gleichungen 18.27–18.31):**

Tiefeneindringung des thermischen Signals bei Witterungsschwingung mit Periode tsp:
xE = √(tsp · λ / (π · ρ · c))

Speicherwirksame Masse für einschichtige Konstruktion (innen):
mi = ρi · (xE/2) · AWi

Für mehrschichtige Konstruktionen werden alle Schichten von der Innen- (bzw. Außen-) Oberfläche aus berücksichtigt, bis die Eindringtiefe xE überschritten wird (Gleichungen 18.29a/b und 18.30a/b).

**Raumlufttemperatur (Kerngleichung des Modells, Gleichung 18.34):**

θi,j+1 = θoi,j+1 · [Üi / (L+TF+Üi)] + [SF,j/Üi + SW,j/T′W + θe,j · (L+TF)/Üi + J · (1/Üi + 1/2)] / [1/Üi + 1/(L+TF) + ...] − (θoi,j+1 − θi,j) · exp(−βj · Δt)

(vereinfacht: θi ergibt sich aus θoi über Bilanzgleichung 2, Gl. 18.32)

**Empfindungstemperatur** (Gleichung 18.33):
θE,j+1 ≈ (θi,j+1 + θoi,j+1) / 2

Alle Indices j laufen von 1 bis 8760 (Stunden eines Jahres).
