# Lehrbuch der Bauphysik — Teil 26
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 1041-1080.

Dieser Teil schließt Kapitel 38 (Mathematische Brandmodelle, Abschnitte 38.3.5–38.4 mit Literaturverzeichnis) ab und enthält anschließend den vollständigen Anhang: das Symbolverzeichnis für alle sechs Fachbereiche (Wärme, Feuchte, Klima, Schall, Licht, Brand) sowie das Gesamtliteraturverzeichnis für Teil I (Wärme) des Lehrbuchs.

## Inhalt

### CFD-Brandsimulation: Ablaufschema und Durchführung (Abschnitt 38.3.5)

Für die Ausführung einer CFD-Brandsimulation empfiehlt [650, Blatt 2] ein dreistufiges Ablaufschema:

1. **Modellaufbau**
   - Festlegung des Simulationsbereichs
   - Erstellung eines Geometriemodells
   - Erzeugung eines Rechengitters
   - Auswahl der mathematischen Teilmodelle: Turbulenzmodell, Verbrennungsmodell, Strahlungsmodell u. a.

2. **Randbedingungen**
   - Festlegung von Simulationsdauer und Zeitschrittweite
   - Vorgabe von Anfangs- und Randbedingungen: Geschwindigkeiten, Drücke, Temperaturen, Konzentrationen, Turbulenzgrößen
   - Definition von Stoffwerten
   - Wahl der Diskretisierungsverfahren
   - Festlegung von Konvergenzkriterien

3. **Simulation und Auswertung**
   - Durchführung der Rechnung
   - Interpretation, Bewertung und Schlussfolgerungen
   - Dokumentation

Die Vielfalt der Möglichkeiten in jedem Schritt hängt stark von den eingesetzten Submodellen des jeweiligen Brandsimulationscodes ab. Eine Übersicht freier und kommerzieller Programme findet sich in [29].

---

### Berechnungsbeispiele (Abschnitt 38.3.6)

Alle nachfolgenden Beispiele wurden mit einem LES-Modell (Large Eddy Simulation) berechnet.

#### Beispiel: Einfluss der Randbedingungen bei der Entrauchung

Untersucht wurde ein dreigeschossiges Atrium mit 18 m Höhe. Die einzelnen Geschosse sind zum Deckendurchbruch hin mit rauchdichten Verglasungen abgetrennt. Die Rauchabführung erfolgt über natürliche Rauchabzugsöffnungen (RWA) in den Seitenflächen des Dachkranzes. Im Brandfall werden durch Winderkennungsgeräte nur die RWA auf der windabgewandten Seite geöffnet. Als Brandlast wurde im Erdgeschoss eine Wärmefreisetzungsrate von 0,1 MW angesetzt. Windeinflüsse blieben in der Simulation unberücksichtigt.

Drei Varianten wurden verglichen (Tab. 38.2):

| Variante | Außentemperatur [°C] | Temperatur im Atrium [°C] | Nachströmungsart |
|----------|----------------------|--------------------------|-----------------|
| 1        | 30                   | 20                       | natürlich       |
| 2        | 20                   | 20                       | natürlich       |
| 3        | 30                   | 20                       | maschinell      |

Ergebnisse nach 900 Sekunden:
- **Variante 1** (Außen wärmer als innen): Wärmere Außenluft strömt durch die RWA nach innen und verdünnt die Rauchgase im Atrium stark. Die Rauchabführung funktioniert nicht.
- **Variante 2** (gleiche Innen-/Außentemperatur): Wärmere Rauchgase können durch die RWA nach außen abströmen — natürliche Konvektion wirkt korrekt.
- **Variante 3** (Außen wärmer, maschinelle Zuluft): Maschinell zugeführte Luft verdrängt die Rauchgase und sichert die Abströmung trotz ungünstiger Temperaturverhältnisse.

Bei allen drei Varianten können die Schutzzielkriterien gemäß Tab. 37.1, Abschn. 37.5.2 (Erkennungsweite mindestens 10 m bis 20 m) für die Erdgeschossebene eingehalten werden. Das Beispiel verdeutlicht den erheblichen Einfluss von Außentemperatur und Zuluftart auf die Wirksamkeit der Entrauchung.

#### Beispiel: Berechnungen für Stand- und Personensicherheit (Hörsaal)

Analysiert wurde ein Hörsaal mit rund 1000 m² Grundfläche, ansteigenden Sitzreihen, Stahlriegelkonstruktion und vorgehängter Glasfassade. Ziel war die Dimensionierung für Personen- und Standsicherheit. Es wurden mehrere Szenarien untersucht:

- **Fall A** (Standard): Brand beginnt gleichzeitig auf allen Sitzreihen
- **Fall B** (Brandausbreitung): Berücksichtigung einer fortschreitenden Brandausbreitung
- **Fall C** (Fensterversagen): Zusätzliches Versagen der Fenster bei 300 °C
- **Fall C + Zuluft**: Wie Fall C, jedoch mit zusätzlicher Zuluft über Türöffnung

Auswertung: Temperaturverlauf entlang der Mittelachse der Sitzreihen (Abb. 38.17a) und Temperatur in Feldmitte unterhalb Riegel 2 (R_2) über die Branddauer bis 1800 s (Abb. 38.17b). Zwei Schnittebenen zum Zeitpunkt 300 s zeigen Temperaturen (20 °C bis maximal 85 °C) und Sichtweiten (0 m bis 30 m). Der Gradient der maximalen Einschränkung der Erkennungsweite liegt dabei unterhalb des maximalen Temperaturgradienten (Abb. 38.18a/b).

#### Beispiel: Einfluss der Gitterfeinheit bei LES-Simulationen

Untersucht wurde ein Poolbrand auf einer Fläche von 4 × 4 m² mit einer stationären Wärmefreisetzungsrate von 51,2 MW. Das Berechnungsvolumen betrug 10 m × 10 m × 30 m. Angenommen wurde eine freie Randbedingung ohne Windeinfluss, der Boden als geschlossen. Vier Gittergrößen wurden verglichen:

| Gittergröße (Kantenlänge) | Zellenanzahl |
|--------------------------|--------------|
| 100,0 cm                 | 3.000        |
| 50,0 cm                  | 24.000       |
| 25,0 cm                  | 192.000      |
| 12,5 cm                  | 1.536.000    |

Im Experiment wurden 815 °C in etwa 1 m Abstand über der Poolfläche gemessen. Die Temperaturprofile längs der Zentralachse zeigen: Bei groben Gittern (50 und 100 cm) weichen die berechneten Temperaturen stark vom Experiment ab. Bei den feineren Gittern (12,5 und 25 cm) nähern sich Peaktemperaturen und die Höhe des Temperaturmaximums den Messwerten gut an. Für 25 cm und 12,5 cm werden Spitzentemperaturen von rund 860–870 °C berechnet, was gut mit dem Experiment übereinstimmt. Die dreidimensionale Energieverteilung ist stark gitterabhängig.

---

### Evaluierung von Brandsimulationsmodellen (Abschnitt 38.4)

Eine Modellevaluierung ist notwendig, um die technische Grundlage und den Grad der Verlässlichkeit eines Modells abzusichern. Sie besteht aus zwei Teilen:

- **Verifikation**: Überprüfung, ob die Erhaltungsgleichungen korrekt gelöst werden (mathematische Richtigkeit des Codes)
- **Validierung**: Nachweis, dass die verwendeten Erhaltungsgleichungen die physikalischen Vorgänge angemessen beschreiben (physikalische Angemessenheit)

Fehlerquellen umfassen nach Beard (1997):
- Teilmodelle für Turbulenz, Verbrennung, Strahlung, Rußproduktion und Pyrolyse sind stets Näherungen der Realität
- Feldmodell-Ergebnisse werden maßgeblich durch numerische Techniken, Gitterauflösung und Gitterart sowie durch Randbedingungen des Berechnungsvolumens beeinflusst
- Zusätzliche Fehler entstehen durch Software (Compiler), Hardware und anwenderbedingte Effekte (user effects and errors)

**Einfluss numerischer Verfahrensordnung:** Der Ansatz bei der Diskretisierung der Differentialgleichungen in algebraische Gleichungen hat erkennbaren Einfluss auf den Detaillierungsgrad der Strömungslösung. Ein Beispiel ist die Simulation des Aufpralls eines Wassertropfens auf eine Wasseroberfläche: Ein Verfahren 1. Ordnung ergibt deutlich gröbere Strukturen als ein Verfahren 2. Ordnung.

**Einfluss der Gitterart:** Strukturierte und unstrukturierte Gitter können kombiniert werden — z. B. unstrukturiert in der Gasphase, strukturiert in der festen Phase. Beim Übergang zwischen beiden Gittertypen im Bereich benachbarter Objekte muss die Konsistenz gewährleistet sein.

#### Validierungsmethoden

Grundlegende Techniken zum Vergleich von Zeitreihen aus Versuch und Simulation (nach Peacock et al. [33]):

**Lokale Metrik — PEAK-Vergleich** (Gl. 38.34):

PEAK = (peakY_Simulation − peakY_Versuch) / peakY_Versuch

Ermöglicht einen schnellen Vergleich der Extremwerte; deckt grobe Abweichungen auf, macht jedoch keine Aussage über den zeitlichen Verlauf der Zeitreihen.

**Globale Metrik — Normierte Fehlerquadratsumme NED** (Gl. 38.35, sogenannte L²-Norm nach Peacock):

NED = Summe[(Y_Versuch,i − Y_Simulation,i)²] / Summe[Y_Versuch,i²]   (i = 1 bis n)

Die Quadratur der Einzelabweichungen verhindert gegenseitige Kompensation von positiven und negativen Fehlern. Der Bezug auf Versuchswerte erlaubt den direkten Vergleich verschiedener physikalischer Größen. Voraussetzung: Beide Zeitreihen müssen gleich viele Punkte zum gleichen Zeitpunkt aufweisen; unterschiedliche Zeitschritte erfordern ein Mittelungsverfahren.

**Kombinierte Darstellung:** PEAK und NED werden als X-Y-Plot gemeinsam dargestellt. Bewertungsgrenzkriterien (z. B. UCW = ±15 %) können dabei eingezeichnet werden (Abb. 38.24).

#### Bewertung der Prognosefähigkeit (US NRC Methodik)

Auf Grundlage von ASTM E1355 [35] wird ein Verfahren zur quantitativen Bewertung der Prognosefähigkeit beschrieben [38]. Kernidee: Die Simulationsunsicherheit UM wird der experimentellen Messunsicherheit UE gegenübergestellt.

Kombinierte und erweiterte Unsicherheit:
UC ≈ √(UM² + UE²) / 2   (vereinfachte Form)

Aus mehreren Tests wird eine gewichtete, kombinierte, erweiterte Unsicherheit UCW (Weighted Combined Expanded Uncertainty) abgeleitet, die als repräsentative Bewertungsgröße gilt.

**Tabelle 38.3: UCW-Werte aus der amerikanischen Referenzstudie [38]**

| Messgröße | Anzahl Versuche | UCW [%] |
|-----------|----------------|---------|
| Heißgasschicht Offset-Temperatur | 26 | 14 |
| Heißgasschicht Dicke | 26 | 13 |
| Ceiling Jet Temperatur | 18 | 16 |
| Plume-Temperatur | 6 | 14 |
| Gaskonzentration | 16 | 9 |
| Rauchkonzentration (Smoke) | 15 | 33 |
| Druck (ohne mechanische Belüftung) | 15 | 40 |
| Druck (mit mechanischer Belüftung) | 15 | 80 |
| Wärmestromdichte | 17 | 20 |
| Oberflächentemperatur | 17 | 14 |

**Modellanwendungen:** In der Studie [38] wurden Plumegleichungen (algebraische Handrechenmethoden), Zonenmodelle und CFD-Modelle verglichen. Plumegleichungen liegen auf der sicheren Seite: Die berechneten Temperaturanstiege der Heißgasschicht (HGL) überschätzen die Messwerte systematisch.

Für das international verbreitete CFD-Feldmodell FDS (Fire Dynamics Simulator) gibt es eine umfangreiche Validierungsdatenbank auf Basis von Extremwertvergleichen für verschiedene Referenzaufgaben [39].

#### PRISME-Projekt — Zeitreihenanalyse

Im Rahmen des internationalen Forschungsvorhabens PRISME [40, 41] wird eine zweiteilige Methodik für die Zeitreihenanalyse aus Versuchen und Simulationen entwickelt [42]:

- **Lokaler Vergleich (PEAK)**: Abweichung der Maxima/Minima
- **Globaler Vergleich (NED)**: Fehlerquadratsumme über den gesamten zeitlichen Verlauf

Nach Einführung von Grenzwerten (unter Berücksichtigung von Mess- und Berechnungsunsicherheiten) ist eine abschließende quantitative Bewertung der Simulationsergebnisse möglich. Die Methodik ist nicht auf Brandschutzprobleme beschränkt, sondern allgemein anwendbar.

---

### Literatur zu Kapitel 38

Vollständige Referenzliste (Auswahl der zitierten Werke):

- [1] Hosser/Riese: Brandkenngrößen-Datenbank, iBMB TU Braunschweig, 2008
- [2] Drysdale: An Introduction to Fire Dynamics, Wiley-Interscience, 1992
- [3] Zehfuß (Hrsg.): TB 04-01 Leitfaden Ingenieurmethoden des Brandschutzes, 4. Aufl. 2020
- [4] Zukoski et al.: Visible Structure of Buoyant Diffusion Flames, 20th Symposium on Combustion, 1985
- [5] McCaffrey: Momentum Implications for Buoyant Diffusion Flames, Combustion and Flame 52, 1983
- [6] Heskestad: Fire Plumes, Flame Height, and Air Entrainment, SFPE Handbook, 4. Aufl. 2008
- [7] ISO 16734 Draft: Fire safety engineering — algebraic equations for fire plumes, 2006
- [8] Thomas et al.: Flow of hot gases in roof venting, Fire Research Technical Paper No. 7, 1963
- [9] Brein: Plume-Formeln für Rauchausbreitung, Forschungsstelle Brandschutztechnik Karlsruhe, 2001
- [10] Alpert: Ceiling Jet Flows, SFPE Handbook, 4. Aufl. 2008
- [11] Evans: Calculating Sprinkler Actuation Time in Compartment, Fire Safety Journal Vol. 9, 1985
- [12] Mowrer: Enclosure Smoke Filling, SFPE Handbook, 4. Aufl. 2008
- [13] ISO 16735: Calculation methods for smoke layers, 2005
- [14] Karlsson/Quintiere: Enclosure Fire Dynamics, CRC Press, 2000
- [15] Schneider/Haksever: Wärmebilanzberechnungen für Brandräume, TU Braunschweig, 1978
- [16] Schneider: Grundlagen der Ingenieurmethoden im Brandschutz, Werner Verlag, 2002
- [17] Jansens: Heat Release in Fires, Elsevier, 1992
- [18] Schneider: Ingenieurmethoden im baulichen Brandschutz, 6. Aufl., Expert-Verlag, 2011
- [19] McGrattan/Miles: Modeling Enclosure Fires Using CFD, SFPE Handbook, 4. Aufl. 2008
- [20] Gerlinger: Numerische Verbrennungssimulation, Springer, 2005
- [21] Cox: Compartment Fire Modelling, Academic Press, 1995
- [22] Yeoh/Yuen (Hrsg.): CFD in Fire Engineering, Butterworth Heinemann, 2009
- [23] Ferziger/Peric: Computational Methods for Fluid Dynamics, 2. Aufl., Springer, 1999
- [24] Guerts: Elements of direct and large-eddy simulation, Edwards, 2004
- [25] Spalding: Mixing and Chemical Reaction in Turbulent Flames, 13th Int. Symp. Combustion, 1971
- [26] Magnussen/Hjertager: Mathematical Modeling of Turbulent Combustion, 16th Int. Symp. Combustion, 1976
- [27] Moss: Turbulent Diffusion Flames, Academic Press, 1995
- [28] Riese et al.: Evaluation of Fire Models for Nuclear Power Plants — Flame Spread in Cable Tray Fires, GRS Report 214, 2006
- [29] Olenik/Carpenter: International Survey of Computer Models for Fire and Smoke, J. Fire Protection Eng. 13, 2003
- [30] Riese: Ermittlung der Brandwirkungen mit Brandmodellen, Braunschweiger Brandschutztage, 2005
- [31] Forell: Nachweise der Personensicherheit, Braunschweiger Brandschutztage, 2005
- [32] Münch: Verifikation und Validierung bei der Softwareentwicklung, FDS-Usergroup 2008
- [33] Peacock et al.: Quantifying fire model evaluation using functional analysis, Fire Safety Journal 33, 1999
- [34] ISO/DIS 16730: Assessment, verification and validation of calculation methods, 2008
- [35] ASTM E1355-11: Standard Guide for Evaluating Predictive Capability of Deterministic Fire Models
- [36] Rigollet/Roewekamp: Fire code benchmark activities — PRISME, EUROSAFE 2009
- [37] Audouin et al.: Quantifying differences between CFD results and measurements, large-scale fire, Nuclear Engineering and Design 241, 2011
- [38] NUREG-1824/EPRI 1011999: Verification & Validation of Selected Fire Models for Nuclear Power Plants, Vol. 2: Experimental Uncertainty, 2007
- [39] McGrattan et al.: Fire Dynamics Simulator Technical Reference Guide, Vol. 3: Validation, NIST, 2016
- [40] Fire Code Reform Centre: Fire Engineering Guidelines, NSW Australia, 2000
- [41] Schneider/Könnecke: Simulation der Personenevakuierung, vfdb-Zeitschrift 3, 1996
- [42] Riese/Siemon: Untersuchung der Prognosefähigkeit von Brandsimulationsmodellen — PRISME DOOR, Bauphysik 36, 2014

---

### Anhang: Symbolverzeichnis

Der Anhang enthält das vollständige Symbolverzeichnis des Lehrbuchs, gegliedert nach sechs Fachbereichen.

#### I. Wärme — Lateinische Buchstaben

| Symbol | Bezeichnung | Einheit |
|--------|------------|---------|
| a | Temperaturleitfähigkeit | m²/s |
| A | Fläche | m² |
| A | Strahlungsabsorptionsgrad | – |
| AB | Bezugsfläche | m² |
| AGW | Arbeitsplatzgrenzwert | – |
| Al | lichte Öffnungsfläche des Fensters | m² |
| b | Energiegehalt | kWh/Einheit |
| B | Brennstoffeinsparung | l bzw. m³ bzw. kg |
| B | Breite | m |
| c | spezifische Wärmekapazität | Wh/(kg·K) |
| C | Wärmekapazität | Wh/K |
| C | Strahlungskonstante | W/(m²·K⁴) |
| Cs | Strahlungskonstante des schwarzen Körpers | W/(m²·K⁴) |
| d | Schichtdicke | m |
| eP | Anlagenaufwandszahl | – |
| E | Energiebedarf | W/K |
| f | Fensterflächenanteil | – |
| fa, fb, fq | Abschnittsanteile | – |
| fP | Primärenergiefaktor | – |
| f, fRsi | Temperaturfaktor | – |
| FC | Abminderungsfaktor für Sonnenschutz (Verschattung) | – |
| Ff | Abminderungsfaktor infolge Rahmenanteil | – |
| Fx | Temperaturkorrekturfaktor für Bauteil x | – |
| g | Erdbeschleunigung | m/s² |
| g | Gesamtenergiedurchlassgrad der Verglasung | – |
| gtotal | Gesamtenergiedurchlassgrad inkl. Sonnenschutz | – |
| Gr | Grashof-Zahl | – |
| Gt | Gradtagzahl | Kh/a |
| h | Wärmeübergangskoeffizient | W/(m²·K) |
| hK | konvektiver Wärmeübergangskoeffizient | W/(m²·K) |
| HS | Wärmeübergangskoeffizient für Strahlung | W/(m²·K) |
| H | Höhe | m |
| H | temperaturspezifischer Wärmeverlust | W/K |
| H | Wärmetransferkoeffizient (HT + HV) | W/K |
| HT | Transmissionswärmeverlust | W/K |
| HT' | spezifischer Transmissionswärmeverlustkoeffizient | W/(m²·K) |
| HV | Lüftungswärmeverlust | W/K |
| I | Strahlungsintensität | W/m² |
| k | spezifische Brennstoffkosten | €/Einheit |
| K | Kosten | € |
| ΔK | Energiekosteneinsparung | € |
| l | Länge, charakteristische Länge | m |
| lÜ | Überströmlänge | m |
| L | Länge | m |
| L2D | thermischer Leitwert | W/(m·K) |
| m | Masse | kg |
| mi | flächenbezogene Masse | kg/m² |
| n | Luftwechselrate | h⁻¹ |
| MFH | Mehrfamilienhaus | – |
| nv | volumenbezogener Feuchtegehalt | – |
| Nu | Nusselt-Zahl | – |
| P | elektrische Bewertungsleistung | W/m² |
| Pr | Prandtl-Zahl | – |
| q | Wärmestromdichte | W/m² |
| Q" | spezifische Energie | kWh/(m²·a) |
| Q | Wärmemenge | Wh oder kWh |
| Qc,f | Endenergie für Kühlsystem | kWh/a |
| Qc*,f | Endenergie für RLT-Kühlfunktion | kWh/a |
| Qf,j | Endenergie nach Energieträger j (Brennwertbasis) | kWh/a |
| Qh,f | Endenergie für Heizsystem | kWh/a |
| Qh*,f | Endenergie für RLT-Heizfunktion | kWh/a |
| Qi,M | mittlere monatliche Wärmegewinne aus internen Quellen | kWh/Monat |
| Qg,M | monatliche Wärmegewinne | kWh/Monat |
| Ql,f | Endenergie für Beleuchtung | kWh/a |
| Ql,M | monatliche Wärmeverluste | kWh/Monat |
| Qm*,f | Endenergie für Befeuchtung | kWh/a |
| Qp,HS | brennwertbezogene Primärenergie | kWh/a |
| Qr | Umweltwärme | kWh/a |
| Qs | solare Wärmegewinne | kWh/a |
| Qs,M | mittlere monatliche Solarstrahlungsgewinne | kWh/Monat |
| Qt | Verluste der Anlagentechnik | kWh/a |
| Qw,f | Endenergie für Trinkwarmwasser | kWh/a |
| R | Strahlungsreflexionsgrad | – |
| R | Wärmedurchlasswiderstand | (m²·K)/W |
| RT | Wärmedurchgangswiderstand | (m²·K)/W |
| Ra | Rayleigh-Zahl | – |
| Re | Reynolds-Zahl | – |
| Rse | Wärmeübergangswiderstand außen | (m²·K)/W |
| Rsi | Wärmeübergangswiderstand innen | (m²·K)/W |
| S | Sonneneintragskennwert | – |
| S, SF | Strahlungsgewinnkoeffizient | W/(m²·K) |
| SSG | Sonnenschutzglas | – |
| SX | anteiliger Sonneneintragskennwert | – |
| t | Zeit | h |
| Teff,Tag,TL | Effektive Betriebszeit im tageslichtversorgten Bereich tagsüber | h |
| Teff,Tag,KTL | Effektive Betriebszeit ohne Tageslicht tagsüber | h |
| Teff,Nacht,KTL | Effektive Betriebszeit ohne Tageslicht nachts | h |
| tm | Tage im Monat | d/Monat |
| T | Strahlungsemissionsgrad | – |
| T | thermodynamische Temperatur | K |
| Tm | absolute mittlere Temperatur im Hohlraum | K |
| TWD | Transparentes Wärmedämmsystem | – |
| u | Windgeschwindigkeit | m/s |
| U | Wärmedurchgangskoeffizient | W/(m²·K) |
| v | Geschwindigkeit | m/s |
| V | Verglasung | – |
| V | Volumen | m³ |
| V | Volumenstrom | m³/h |
| w | Strömungsgeschwindigkeit | m/h |
| W | Heiz-/Kühlleistung | W oder kW |
| Wf | Endenergiebedarf für Hilfsenergien | kWh/a |
| WDG | Wärmedämmglas | – |
| WDVS | Wärmedämmverbundsystem | – |
| WRG | Wärmerückgewinnung | – |
| x | Dicke | m |

#### I. Wärme — Griechische Buchstaben

| Symbol | Bezeichnung | Einheit |
|--------|------------|---------|
| α | Strahlungsabsorptionsgrad | – |
| β | Abdeckwinkel | – |
| β | thermischer Ausdehnungskoeffizient | 1/K |
| γ | Verhältnis Wärmequelle zu Wärmesenke | – |
| δ | Wärmeabgabegrad | – |
| Δ | Differenz (z. B. Δθ für Temperaturdifferenz) | – |
| ε | Emissionsgrad | – |
| η | dynamische Viskosität | kg/(m·s) |
| ηM | monatlicher Ausnutzungsgrad | – |
| θ | Temperatur | °C |
| Θ | Durchflussverhältnis | – |
| λ | Wärmeleitfähigkeit | W/(m·K) |
| ν | kinematische Viskosität | m²/s |
| σ | Stefan-Boltzmann-Konstante: σ = 5,67 × 10⁻⁸ W/(m²·K⁴) | W/(m²·K⁴) |
| ρ | Rohdichte | kg/m³ |
| ρ | Strahlungsreflexionsgrad | – |
| τ | Strahlungstransmissionsgrad | – |
| φ | relative Luftfeuchte | % |
| φi→j | Einstrahlzahl | – |
| Φ | Wärmestrom | W |
| ΦL | Lüftungswärmestrom | W |
| ΦT | Transmissionswärmeverluste | W |
| χ | punktförmiger Wärmedurchgangskoeffizient | W/K |
| Ψ | linienförmiger Wärmedurchgangskoeffizient | W/(m·K) |
| ΨG | linienförmiger Wärmedurchgangskoeffizient durch Abstandshalter der Verglasung | W/(m·K) |

#### I. Wärme — Indizes

| Zeichen | Bedeutung | Herleitung |
|---------|----------|-----------|
| a | außenmaßbezogen | – |
| bf | Fußboden Keller | – |
| bw | Wand Keller | – |
| AW | Außenwand | – |
| D | Dach | – |
| e | außen | external |
| eq | äquivalent | equivalent |
| f | feucht | – |
| f | Rahmen | frame |
| g | Verglasung | glazing |
| G | Grenzschicht | – |
| G | Nettogrundfläche des Raumes | – |
| G | unterer Gebäudeabschluss | – |
| HF | Hauptfassade | – |
| i | innen | internal |
| k | konvektiv | – |
| KTL | keine Tageslichtversorgung | – |
| l | längenbezogen | – |
| max | Höchstwert | maximum |
| mS | mit Strahlung | – |
| NA | Nachtabschaltung | – |
| nb | niedrig beheizte Räume | – |
| o | oben | – |
| oS | ohne Strahlung | – |
| P | opake Füllung | panel |
| R | Rechenwert | – |
| s | Strahlung / Oberfläche | surface |
| se | Oberfläche außen | surface external |
| si | Oberfläche innen | surface internal |
| t | trocken | – |
| T | Transmission | – |
| TL | tageslichtversorgt | – |
| u | unbeeinflusste Umgebung / unbeheizter Raum / unten | – |
| U | Abseitenwand | – |
| W | Fenster | window |
| WB | Wärmebrücke | – |

---

#### II. Feuchte — Symbole und Einheiten

| Symbol | Einheit | Bedeutung |
|--------|---------|----------|
| A | m² | Fläche |
| AW | kg/(m²·s⁰·⁵) | Wasseraufnahmekoeffizient |
| C | – | Formfaktor |
| D | m²/h | Diffusionskoeffizient |
| E | kg/(m·h·Pa) | Effusionskoeffizient |
| E | N/mm² | Elastizitätsmodul |
| F | N | Kraft |
| G | kg/h | Massenstrom |
| I | W/m² | Strahlungsintensität |
| K | kg/(m·h·V) | spezifische elektrokinetische Durchlässigkeit |
| K | Pa/V | spezifische elektrokinetische Steighöhe |
| L | m | Spaltlänge |
| M | kg | Masse |
| M | – | relative Molmasse |
| O | m²/g | Oberfläche |
| P | Pa | Gesamtdruck |
| PK | Pa | Kapillardruck |
| PSP | N/m | Spreitungsdruck |
| PST | Pa | Staudruck der Luft |
| RV | J/(kg·K) | Gaskonstante des Wasserdampfs |
| R | kJ/(kmol·K) | universelle Gaskonstante |
| R1,2 | m | Hauptkrümmungsradien |
| Re | – | Reynolds-Zahl |
| Rsi, Rse | m²·K/W | Wärmeübergangswiderstand innen/außen |
| RT | m²·K/W | Wärmedurchgangswiderstand |
| T | K | thermodynamische Temperatur |
| U | V | elektrische Spannung |
| U | W/(m²·K) | Wärmedurchgangskoeffizient |
| V | m³ | Volumen |
| V | m³/h | Volumenstrom |
| WD | kg/(m²·h⁰·⁵) | Wasserdampfaufnahmekoeffizient |
| WW | kg/(m²·h⁰·⁵) | Wasseraufnahmekoeffizient |
| Ww' | m·h⁰·⁵ | Wassereindringkoeffizient |
| a | m³/(m·h·Pa²/³) | Fugendurchlasskoeffizient |
| a | – | Absorptionskoeffizient |
| b | – | Approximationsfaktor |
| b | m | Breite |
| c | – | Wechselwirkungsparameter |
| d | m | Dicke / Durchmesser |
| deff | m | effektive Dicke |
| fRsi | – | Temperaturfaktor |
| g | kg/(m²·h) | Massenstromdichte |
| g | m/s² | Erdbeschleunigung |
| h | m | Höhe / Eindringtiefe |
| he | m | spezifische elektrokinetische Steighöhe |
| k | m/s | Durchlässigkeitswert |
| kD | kg/(m·h·Pa) | spezifische Durchlässigkeit nach Darcy |
| l | m | Länge |
| m | kg/m² | flächenbezogene Masse |
| n | h⁻¹ | Luftwechselrate |
| n | – | Exponent / Rauigkeit / Anzahl Wassermoleküllagen |
| p | Pa | Partialdruck des Wasserdampfs |
| q | W/m² | Wärme-/Energiestromdichte |
| r | m | Radius |
| r | kJ/kg | Verdunstungswärme |
| sd | m | wasserdampfdiffusionsäquivalente Luftschichtdicke |
| t | s, h, d, a | Zeit |
| u | –, % | massebezogener Wassergehalt |
| uV | –, % | volumenbezogener Wassergehalt |
| v | m/s | Geschwindigkeit |
| w | kg/m³ | Wassergehalt |
| x, y, z | m | Wegekoordinaten |
| α | – | Diffusionskoeffizienten-Verhältnis |
| βv | m/h, m/s | Wasserdampfübergangskoeffizient |
| βp | kg/(m²·h·Pa) | Wasserdampfübergangskoeffizient |
| σ | N/mm² | Spannung |
| εh | mm/m | hygrische Dehnung |
| εs | mm/m | Endschwindmaß |
| γ | – | Scherwinkel |
| θ | °C | Celsius-Temperatur / Randwinkel der Benetzung |
| δ | kg/(m·h·Pa) | Wasserdampf-Diffusionsleitkoeffizient |
| η | Pa·s | dynamischer Viskositätskoeffizient |
| λ | – | Reibungsbeiwert |
| λ | W/(m·K) | Wärmeleitfähigkeit |
| λ | m | mittlere freie Weglänge |
| ν | g/m³ | absolute Luftfeuchte / Wasserdampfkonzentration |
| ν | m²/s | kinematischer Viskositätskoeffizient |
| ϰ | m²/h | Flüssigkeitsleitkoeffizient |
| μ | – | Wasserdampf-Diffusionswiderstandszahl |
| ρ | kg/m³ | Dichte |
| σ | N/m | Oberflächenspannung |
| ϕ | –, % | relative Luftfeuchte |
| ψ | –, % | volumenbezogener Wassergehalt |
| ξ | – | Durchflussbeiwert |

**Feuchte — Indizes (Auswahl):**
A = Austritt / Luft; a = Umgebung; B = Baustoff; D = Diffusion / Wasserdampf; E = Eintritt; F = Flüssigwassertransport; f = frei/freiwillig; h = hygrisch; i = innen; j = Sonneneinstrahlung; K = Kapillar; k = Konvektion; L = Luft; O = Oberfläche; R = Raumluft; s = Sättigungszustand / Oberfläche / Strahlung / Schwinden / Taupunkt; T = Tauperiode; V = Verdunstungsperiode; W = Wasser flüssig / Wind; o = oben; u = unten; v = verdampfen; w = Wasser

---

#### III. Klima — Symbole und Einheiten

| Symbol | Einheit | Bedeutung |
|--------|---------|----------|
| A | m² | Fläche |
| a | 1 | Wärmeabsorptionskoeffizient |
| a | 1, ° | Azimutwinkel |
| B | 1 | Winkelhilfsfunktion |
| Cp | 1 | Regentagefunktion |
| C | Ws/K | Wärmekapazität |
| CF | kg/Pa | Feuchtekapazität |
| c | Ws/(kg·K) | spezifische Wärmekapazität |
| c | 1 | Widerstandsbeiwert |
| D | 1 | Tageslängenfunktion |
| DR | 1 | Abminderungsfaktor für Regenstromdichte |
| d | m | Abstand, Durchmesser |
| E | kg^(1/4)·m²/s^(1/2) | Gebäudeparameter für Schlagregen |
| F | N | Kraft |
| f | 1 | Rahmenfaktor, Glasanteil bei Fenstern |
| G | W/m² | Strahlungswärmestromdichte |
| g | kg/(m²·s) oder kg/(m²·h) | Regenmassenstromdichte |
| g | m/s² | Erdbeschleunigung |
| g | 1 | Glasdurchlasskoeffizient |
| H | m | Gebäudehöhe |
| h | W/(m²·K) | spezifischer Gesamtwärmeübergangskoeffizient |
| h | Ws/kg | spezifische Enthalpie |
| h | 1 | Sonnenhöhenwinkel |
| J | W | Wärmestrom innerer Quellen |
| K | – | Klimamatrix |
| k | W/(m²·K) | spezifischer Gesamtwärmedurchgangskoeffizient |
| k | W/K | Anstieg der Heizungskennlinie |
| L | W | Lüftungswärmestrom |
| LF | kg/h, kg/s | Lüftungsfeuchtestrom |
| L | m | Grenzschichtdicke |
| l | m | Gebäudelänge |
| m | kg | Masse |
| N | l/(m²·h) | Regenvolumenstromdichte |
| n | 1/h | Luftwechselrate |
| n | 1 | Bedeckungsgrad |
| PMV | 1 | Komfortparameter |
| P | Pa | Druck |
| Q | Ws | Wärmemenge |
| R | m²·K/W | Wärmeleitwiderstand |
| R | Ws/(kg·K) | Gaskonstante |
| r | m | Radius, Abstand |
| r | Ws/kg | spezifische Phasenumwandlungsenthalpie |
| S | W | Strahlungswärmestrom |
| s | 1 | Gesamtdurchlassgrad des Fensters |
| T' | W/K | temperaturbezogener Transmissionswärmestrom zwischen Wandoberflächen |
| TF | W/K | temperaturbezogener Transmissionswärmestrom durch Fenster |
| T | K | Temperatur |
| T | h, d, a | Periodendauer |
| Tr | 1 | Trübung |
| t | s, h, d, a | Zeit |
| U | W/(m²·K) | spezifischer Gesamtwärmedurchgangswert |
| U' | W/(m²·K) | spezifischer Wärmedurchgangswert ohne Wärmeübergänge |
| Ü | W/K | temperaturbezogener Wärmeübergangswert |
| V | m³ | Volumen |
| VG | 1 | Strahlungswärmestromverhältnis |
| v | m/s | Geschwindigkeit |
| w | 1, ° | Winkel der Windrichtung |
| wh | m³/m³ | hygroskopischer Feuchtegehalt im Material |
| x | m | Ortskoordinate |
| x | kg/kg | absoluter Feuchtegehalt der Luft |
| y | m | Ortskoordinate |
| z | 1 | Zahl der Tage / Personen / Verschattungsgrad |
| α | 1, ° | Winkel |
| β | 1, ° | Winkel |
| β | 1/s, 1/h | Zeitkonstante |
| δ | 1, ° | Deklinationswinkel |
| δL | s | Wasserdampfleitfähigkeit in Luft |
| ε | 1 | Emissionskoeffizient |
| Φ | 1 | Heaviside-Sprungfunktion |
| Φ | W | Wärmestrom |
| ϕ | 1, % | relative Luftfeuchtigkeit |
| χ | 1, ° | Breitengrad |
| λ | W/(m·K) | Wärmeleitfähigkeit |
| μ | 1 | Dampfdiffusionskoeffizient |
| ρ | kg/m³ | Dichte |
| σ | W/(m²·K⁴) | Stefan-Boltzmann-Konstante |
| τ | s, h | Einstellzeit |
| θ | °C | Temperatur |
| η | Pa·s | Zähigkeit |

**Klima — Indizes (Auswahl):**
a = Jahr / außen / abgegeben; B = Bauteil; c = konvektiv; D = Dampf / Dresden / Durchschnitt; dir = direkt; dif = diffus; E = Empfindung / Essen / Erde / Eigenverschattung / erzeugt; F = Fenster / Feuchte; G = Gesamt; H, h = Heizperiode; h, hor = horizontal; i = innen / Laufindex; j = Laufindex; K = Klotzsche / Kondensation; kin = kinetisch; L = Luft / Lüftung; l = lang / langwellig; M = Monat / Messung; m = Mittel / Laufindex; max, min = maximal / minimal; n = Laufindex / normal; o = Oberfläche; p = Druckableitung / isobar / Periode / Produktion; Qu = Quelle; R, r = resultierend / Reibung / Regen / Rahmen / radiativ; r = radiativ; ref = Referenz; S = Sonne / Sättigung; s = surface / Sättigung / Strahlung; Sp = Speicherung; T = Taupunkt / Translation; t = Zeitableitung; u = Umgebung; Ü = Übergang; v = vertikal / Volumenableitung; W = Wasser / Wand / Widerstand / Wind; z = zugeführt

---

#### IV. Schall — Symbole und Einheiten

| Symbol | Einheit | Bedeutung |
|--------|---------|----------|
| A | m² | äquivalente Schallabsorptionsfläche |
| A | dB | Oktavbanddämpfung |
| B' | kg·m²/s | Biegesteifigkeit |
| c | m/s | Schallgeschwindigkeit |
| cB | m/s | Biegewellengeschwindigkeit |
| C | – | Frequenzparameter |
| C | dB | Spektrum-Anpassungswert |
| C80 | dB | Klarheitsmaß |
| C1 | dB | Spektrum-Anpassungswert für Trittschall |
| Cmet | dB | meteorologische Korrektur |
| Ctr | dB | Spektrum-Anpassungswert für Verkehrsgeräusche |
| d | m | Dicke / Abstand / Durchmesser |
| D | – | Dämpfungsgrad |
| D2,s | dB | räumliche Abklingrate |
| D50 | – | Deutlichkeitsgrad |
| Dc | – | Richtwirkungskorrektur |
| Dn | dB | Norm-Schallpegeldifferenz |
| Dn,e,w | dB | bewertete Norm-Schallpegeldifferenz eines Fassadenelementes |
| Dn,f,w | dB | bewertete Norm-Flankenschallpegeldifferenz |
| Dn,w | dB | bewertete Norm-Schallpegeldifferenz |
| DnT | dB | Standard-Schallpegeldifferenz |
| DnT,w | dB | bewertete Standard-Schallpegeldifferenz |
| Dz | dB | Abschirmmaß |
| e | m | Abstand Schallreflektor zu -empfänger |
| Edyn | N/m² | dynamischer Elastizitätsmodul |
| f | Hz | Frequenz |
| f0 | Hz | Resonanzfrequenz |
| fc | Hz | Koinzidenzgrenzfrequenz |
| fD | Hz | Designfrequenz |
| fg | Hz | Grenzfrequenz |
| fsch | Hz | Schroeder-Grenzfrequenz |
| G | – | Bodenfaktor |
| h | m | Höhe |
| j | – | imaginäre Einheit √(−1) |
| k | – | Grenzschichtparameter |
| k0 | 1/m | Wellenzahl |
| K | m³/Platz | Volumenkennzahl |
| K | dB | Korrektursummand, Zuschläge |
| Kij | dB | Stoßstellendämm-Maß |
| Kmet | dB | Korrektur für meteorologische Effekte |
| l | m | Länge / Abstand |
| L | dB | Schallpegel (allgemein) |
| LA | dB(A) | A-bewerteter Schallpegel |
| Leq | dB | energieäquivalenter Dauerschallpegel |
| LAT (LT) | dB | A-bewerteter Langzeit-Mittelungspegel |
| LfT (DW) | dB | äquivalenter Oktavband-Dauerschalldruckpegel |
| LEX | dB(A) | Lärm-Expositionsschallpegel |
| Ln,eq,0,w | dB | äquivalenter bewerteter Norm-Trittschallpegel der Rohdecke |
| Ln' | dB | Norm-Trittschallpegel |
| Ln,w' | dB | bewerteter Norm-Trittschallpegel |
| Lp | dB | Schalldruckpegel |
| Lp,A,S,4m | dB | Schalldruckpegel der Sprache in 4 m Abstand |
| Lw | dB | Schallleistungspegel |
| Lr | dB | Beurteilungspegel |
| m' | kg/m² | flächenbezogene Masse |
| p | Pa | Schalldruck |
| Q | – | Richtwirkungsmaß |
| r | m | Radius |
| r' | – | akustischer Reibungswiderstand |
| rD | m | Ablenkungsabstand |
| rH | m | Hallradius |
| rp | m | Vertraulichkeitsabstand |
| R | J/(kg·K) oder Ns/m³ | spezifische Gaskonstante für Luft / Strömungswiderstand |
| R | dB | Schalldämm-Maß eines Bauteils |
| R' | dB | Schalldämm-Maß zwischen Räumen (inkl. Nebenwege) |
| R'e,w | dB | bewertetes Bau-Schalldämm-Maß der Fassade |
| R'w | dB | bewertetes Bau-Schalldämm-Maß zwischen Räumen |
| Rres | dB | resultierendes Schalldämm-Maß |
| R | – | komplexer Reflexionsfaktor |
| s' | MN/m³ | dynamische Steifigkeit |
| S | m² | Fläche |
| STI | – | Speech Transmission Index |
| T | m | Plattendicke |
| T | K | Temperatur |
| T | s, h | Beurteilungszeit |
| T | s | Nachhallzeit |
| Tsab | s | Nachhallzeit nach Sabine |
| Teyr | s | Nachhallzeit nach Eyring |
| Tsoll | s | Soll-Nachhallzeit |
| uprog | dB | Sicherheitsbeiwert |
| U | m | Umfang |
| Z | dB | Schirmwert |
| Z | – | normierte Wandimpedanz |
| Z | Ns/m³ | Impedanz |
| Za | Ns/m³ | Wellenwiderstand des Absorbers |
| ZT | Ns/m³ | Trennimpedanz |
| Z0 | kg/(m²·s) | Schallkennimpedanz der Luft |
| α | dB/km | Absorptionskoeffizient (Luft) |
| α | – | Schallabsorptionsgrad |
| α0 | – | Schallabsorptionsgrad für senkrechten Einfall |
| αk | – | Körperschallabsorptionsgrad |
| αp | – | praktischer Schallabsorptionsgrad |
| αs, αst | – | Schallabsorptionsgrad für statistischen Einfall |
| αw | – | bewerteter Schallabsorptionsgrad |
| Δ | – | Differenz |
| Γ | 1/m | komplexe Ausbreitungskonstante |
| η | – | Verlustfaktor |
| η | kg/(m·s) | dynamische Viskosität |
| ϑ | °C | Temperatur |
| ϑ | ° | Schalleinfallswinkel |
| κ | – | Adiabatenexponent |
| λ | m | Wellenlänge |
| λB | m | Biegewellenlänge |
| μ | – | Poissonsche Querkontraktionszahl |
| ρ | kg/m³ | Dichte |
| ρ | – | Schallreflexionsgrad |
| σ | – | Lochflächenanteil / Abstrahlgrad |
| τ | – | Transmissionsgrad |
| φ | – | Phasenwinkel |
| Ψ | – | Objektanteil |
| ω | Hz | Eigenkreisfrequenz |
| Ξ | Ns/m⁴ | längenbezogener Strömungswiderstand |

---

#### V. Licht — Symbole und Einheiten

| Symbol | Einheit | Bedeutung |
|--------|---------|----------|
| A | m² | Fläche |
| AM | – | Airmass |
| D | % | Tageslichtquotient |
| Ee | W/m² | Bestrahlungsstärke |
| Ei | – | Energieeffizienzindex |
| EPhoton | eV | Photonenenergie |
| Ev | lx | Beleuchtungsstärke |
| F | 1 | geometrischer Formfaktor |
| GMT | – | Greenwich Mean Time |
| He | (W/m²)·s | Bestrahlung |
| Hv | lx·s | Belichtung |
| I0 | W/m² | Solarkonstante |
| Ie | W/sr | Strahlstärke |
| Iv | cd | Lichtstärke |
| Km | cd·sr/W | photometrisches Strahlungsäquivalent |
| L0 | – | minimale Schichtdicke der Atmosphäre |
| Le | W/(m²·sr) | Strahldichte |
| Lv | cd/m² | Leuchtdichte |
| Me | W/m² | spezifische Ausstrahlung |
| Mv | lm/m² | spezifische Lichtabstrahlung |
| MEZ | – | Mitteleuropäische Zeit |
| MOZ | – | mittlere Ortszeit |
| P | W | Leistung |
| Qe | W·s | Strahlungsenergie |
| Qv | lm·s | Lichtenergie / Lichtmenge |
| Ra | 100 | allgemeiner Farbwiedergabeindex |
| Ri | 100 | spezieller Farbwiedergabeindex |
| T | – | Trübungsfaktor nach Linke |
| U | W/(m²·K) | Wärmedurchgangskoeffizient |
| V | – | Verminderungsfaktor durch Leuchtenverschmutzung |
| WOZ | – | wahre Ortszeit |
| ZGL | – | Zeitgleichung |
| g | % | Gesamtenergiedurchlassgrad |
| h | J·s | Plancksches Wirkungsquantum |
| h | ° | Sonnenhöhe |
| k | – | Raumindex |
| k1 | – | Lichtminderungsfaktor lichtundurchlässiger Fensterkonstruktionsteile |
| k2 | – | Lichtminderungsfaktor infolge Glasverschmutzung |
| k3 | – | Lichtminderungsfaktor bei von 0° abweichendem Lichteinfallswinkel |
| n | – | optische Brechzahl |
| t | s | Zeit |
| z | ° | Zenitwinkel |
| α | % | Absorptionsgrad |
| α | ° | Azimutwinkel |
| γ | ° | Höhenwinkel |
| ε | ° | Einfalls-/Abstrahlwinkel gegenüber Flächennormalen |
| ηe | % | Strahlungsausbeute |
| ηv | lm/W | Lichtausbeute |
| λ | ° | Längengrad |
| λ | nm | Wellenlänge |
| ν | – | Frequenz der Strahlung |
| ρ | % | Reflexionsgrad |
| τ | % | Transmissionsgrad |
| φ | ° | Breitengrad |
| χ | ° | Rotationswinkel einer Schnittebene des Lichtstärkeverteilungskörpers |
| ω | sr | Raumwinkel |
| ΔEi | – | Farbortverschiebung |
| Γ | ° | Längengrad des Zentralmeridians |
| Φe | W | Strahlungsleistung |
| Φv | lm | Lichtstrom |

**Licht — Indizes (Auswahl):**
e = energetic; v = visible; r = Rohbaumaß; A = Direktlichtanteil aus selbstleuchtenden Flächen; a = außen; diff = diffus; dir = Direktlichtanteil; Fr = Fenster; ges = Gesamt; H = Himmellichtanteil; i = innen; i, j = Laufvariablen; ind = Indirektlichtanteil; L = Testlichtquelle; LB = Leuchtenbetriebswirkungsgrad; o = obere Raumhälfte; R = Referenzlichtquelle / Innenreflexionsanteil; S = Sonne; u = untere Raumhälfte; V = Außenanteil / Verbauung; W = Wand; x = gewählte Verglasung; z = Zenit; dif = diffus/gestreut

---

#### VI. Brand — Symbole und Einheiten

| Symbol | Einheit | Bedeutung |
|--------|---------|----------|
| A | m², cm² | Fläche |
| A | m² | Fläche der Fenster- und Türöffnungen |
| At | m² | Öffnungsfläche |
| Aw | m² | innere Oberfläche eines Brandraums |
| A1,i | m² | i-te Wandfläche der Kaltgasschicht |
| Ag,i | m² | i-te Wandfläche der Heißgasschicht |
| A | m/s | vor-exponentieller Faktor |
| Ä | 1 | Intervall / Differenz |
| C | – | Konstante für Erkennbarkeit |
| CD | – | Strömungskoeffizient (Einengungsfaktor für Öffnungen) |
| D | m | Durchmesser |
| D | – | substanzielle Ableitung |
| Dα | m²/s | Diffusionskoeffizient der Komponente α im Gasgemisch |
| E | N/mm² | Elastizitätsmodul |
| E | kJ | Gesamtenergie |
| E | J/mol | Aktivierungsenergie |
| E1 | kJ/kg | Energie gespeichert in der Kaltgasschicht |
| Eg | kJ/kg | Energie gespeichert in der Heißgasschicht |
| Fi | – | toxische Teildosis einer Komponente i |
| F | – | gesamte toxische Schadwirkung |
| FEDNIST | – | fraktionelle effektive Dosis (NIST-Definition) |
| FLDirr | – | fraktionelle tödliche toxische Dosis |
| Gk,i | kN; kN·m | charakteristischer Wert der ständigen Einwirkungen |
| H | kJ | Gesamtenthalpie |
| H | m | Differenz zwischen Deckenhöhe und Brandherdhöhe |
| Hn | m | Distanz von der Brüstung bis zur neutralen Ebene |
| Hd | m | Distanz von der Brüstung bis zur thermischen Grenzschicht |
| H0 | m | Höhe der Öffnung |
| H | kJ/kg | spezifische Gesamtenthalpie |
| H | kWh/kg | Heizwert |
| Hc,eff | kWh/kg | effektive Verbrennungswärme (Heizwert) |
| Hu | MJ/kg | unterer Heizwert |
| L | – | mittlere freie Weglänge des Gases |
| L | cd/m² | Leuchtdichte |
| L0 | cd/m² | Anfangsleuchtdichte |
| Lf | m | mittlere Flammenhöhe |
| M | kN·m | Moment |
| M | kg | Masse |
| Ma | – | Mach-Zahl |
| MBrennstoff | g·mol⁻¹ | Molmasse Brennstoff |
| N | kN | Normalkraft |
| Nk | – | Anzahl unterschiedlicher Komponenten |
| P | kN | Last |
| P | Pa | Druck |
| P | kN/m; kN/m² | Belastung je Längen-/Flächeneinheit |
| Q | kN | Last |
| Qk,i | kN; kN·m | charakteristischer Wert veränderlicher Einwirkungen |
| Q | J | Energieinhalt, Brandlast |
| Q | kW | Wärmefreisetzungsrate des realen Brandherdes |
| Qc | kW | konvektive Wärmefreisetzungsrate |
| Qr | kW | radiative Wärmefreisetzungsrate |
| Q1 | kW | netto Wärmeabgabe von Wänden zur Kaltgasschicht |
| Qg | kW | netto Wärmeabgabe von Wänden zur Heißgasschicht |
| QS | kW | Wärmefreisetzungsrate beim Übergang Schwel- zu Ausbreitungsbrand |
| Qmax,v | kW | maximale Wärmefreisetzungsrate (ventilationsgesteuert) |
| Qmax,f | kW | maximale Wärmefreisetzungsrate (brandlastgesteuert) |
| R | kg/s | Abbrandrate |
| R | – | universelle Gaskonstante |
| Re | – | Reynolds-Zahl |
| RMV | 1/min | Atemrate |
| RTI | m·s⁰·⁵ | Response Time Index — Ansprechempfindlichkeit eines Sprinklers |
| S | m | Erkennungsweite |
| T | K | Temperatur absolut |
| Ta | K; °C | Temperatur der Umgebungsluft |
| Tp | K | Plumetemperatur |
| Tf | K | Flammentemperatur |
| Tjet | °C | maximale Temperatur im Ceiling Jet |
| TD,akt | °C | Aktivierungstemperatur eines Sprinklers |
| Ts | °C | Temperatur der Rauchgasschicht |
| Tg | °C | Temperatur der Heißgasschicht / Gasphase |
| Tw | °C | Temperatur einer Oberfläche |
| U | m | Umfang |
| V | m³ | Volumen |
| V | cm; mm | Verformung |
| V | mm/min | Abbrandgeschwindigkeit |
| Vm0 | m³/mol | molares Normvolumen = 0,224136 m³/mol |
| VHyp | – | Verstärkungsfaktor für erhöhte Atemrate |
| W | m | Breite einer Öffnung |
| W | kg | mittleres Molekulargewicht eines Gasgemischs |
| XO2,0 | 1 | Sauerstoffanteil in der Zuluft |
| Y | g/g | Ausbeute |
| Yα | g/g | Massenanteil einer gasförmigen Komponente α |
| YO | g/g | Massenanteil des an der Zersetzung beteiligten Sauerstoffs |
| YS | g/g | Massenanteil des an der Zersetzung beteiligten Brennstoffs |
| Z | – | Mischungsbruch |
| a | W/(m²·K) | Wärmeübergangszahl |
| a | cm²/s | Temperaturleitzahl |
| a | m/s | Schallgeschwindigkeit des Mediums |
| b | cm; mm | Breite |
| c | min·m²/kWh | Umrechnungsfaktor |
| cp | J/(kg·K) | spezifische Wärmekapazität |
| ci | ppm; Vol.-% | lokale Konzentration einer Komponente i |
| d | cm; mm | Dicke / Durchmesser |
| dWand | m | Dicke einer Wand |
| e | %; ‰ | Dehnung / Stauchung |
| f | cm; mm | Durchbiegung |
| f | 1 | Formfaktor |
| fi | kN | externe spezifische Volumenkräfte |
| g | m/s² | Erdbeschleunigung/Gravitation (9,81 m/s²) |
| h | cm; mm | statische Höhe / Querschnittshöhe |
| h | m | mittlere Höhe der Fenster- und Türöffnungen |
| hw | m | Höhe der Öffnung |
| h | kJ/s | Energiestromdichte |
| h | kJ/kg | Enthalpie |
| ha | kJ/kg | Enthalpie einströmender Luft bei Temperatur Ta |
| h1 | kJ/kg | Enthalpie in der Kaltgasschicht bei Ta |
| hg | kJ/kg | Enthalpie in der Heißgasschicht bei Tg |
| hf | kJ/kg | Enthalpie der vom Brennstoff freigesetzten Gase bei Tf |
| hα | kJ/kg | spezifische Enthalpie der Komponente α |
| hWand | kW/(m²·K) | effektiver Wärmetransferkoeffizient für Wärmeverluste durch Umfassungsbauteile |
| hc | kW/(m²·K) | konvektiver Wärmetransferkoeffizient |
| jαi | – | Diffusionsmassenfluss |
| k | W/(m²·K) | Wärmeübergangszahl |
| k | kJ | kinetische Energie |
| kf | 1 | Beiwert für thermische Eigenschaften der brandraumumschließenden Bauteile |
| l | m | Stützweite |
| ls | mm | kleinstes charakteristisches Längenmaß der Strömung |
| m | % | Feuchtegehalt |
| m | 1 | Abbrandfaktor |
| m | kg/s | Massenstromdichte |
| m | – | Konstante für die Zersetzungsrateberechnung |
| ṁp | kg/s | Plume-Massenstrom |
| mf | g | Massenverlust |
| ṁa | kg/s | eintretende Luftmenge je Zeiteinheit |
| ṁe | kg/s | ausströmende Gasmenge je Zeiteinheit |
| ṁg | kg/s | Massenstrom aus der Heißgasschicht |
| ṁl | kg/s | Massenstrom in der Kaltgasschicht |
| ṁent | kg/s | Einmischungsrate von Luftmasse |
| mf | kg/s | Abbrandrate des Brennstoffs |
| mf'' | kg/(s·m²) | flächenspezifische Abbrandrate |
| mα | kg/s | chemischer Produktionsterm der Komponente α |
| n | 1 | Anzahl |
| n | – | Konstante für Zersetzungsrateberechnung |
| P | Pa | Druck |
| q | kN/m; kN/m² | Belastung je Längen-/Flächeneinheit |
| q | MJ/m²; kg/m² | Brandbelastung (Wärme je Fläche oder Holzgewicht je Fläche) |
| qr | kWh/m² | rechnerische Brandbelastung |
| q | kW | Wärmestromdichte |
| qi | kW | Wärmefluss in xi-Richtung |
| ql'' | kW/m² | flächenbezogener Wärmefluss |
| qc'' | kW/m² | flächenbezogener konvektiver Wärmetransfer |
| qt | MJ/m² | Wärmemenge aller brennbaren Stoffe bezogen auf innere Oberfläche des Brandraums |
| r | m; cm | Radius |
| r | m | Abstand eines Referenzpunktes von der Plume-Achse |
| r | 1 | stöchiometrischer Luftbedarf [g Luft / g Brennstoff] |
| s | m | Stablänge |
| t | min | Zeit |
| tD,akt | s | Zeit bis zur Aktivierung eines Sprinklers |
| tc | s | charakteristische Zeit für effektiven Wärmetransferkoeffizienten |
| tg | s | Brandentwicklungsgeschwindigkeit |
| u | cm; mm | Verformung / Achsabstand |
| u | m/s | Strömungsgeschwindigkeit |
| Vjet | m/s | maximale Geschwindigkeit im Ceiling Jet |
| w | 1 | Wärmeabzugsfaktor |
| 1/K | – | Wärmeausdehnungszahl |
| w | cm | Widerstandsmoment |
| w | J/(m³·s) | Wärmequelle oder -senke |
| zij | m | vertikaler Abstand von der Brandherdoberfläche zum Berechnungsort |
| z0 | m | Abstand vom virtuellen Brandursprung zum realen Brandherd |
| zs | m | Höhe der raucharmen Schicht |
| ß | N/mm² | Festigkeit |
| ß | 1 | Ausnutzungsgrad |
| γi | – | Teilsicherheitsbeiwert |
| δij | – | Kronecker-Delta |
| Δ | – | Intervall / Differenz |
| ε | 1 | Emission |
| ε | t/s | Dehngeschwindigkeit |
| η | – | Konstante für Temperaturerhöhung im Plumebereich |
| η | m | Kolmogorov-Länge für turbulente inerte Strömung |
| ϑ | °C; K | Temperatur |
| ϑ0 | K | Temperatur des Probekörpers bei Versuchsbeginn |
| λ | W/(m·K) | Wärmeleitzahl |
| μ | % | Bewehrungsgrad |
| μ | 1 | Querdehnungszahl |
| μ | kg/(m·s) | dynamische Viskosität |
| μv | kg/(m·s) | Volumenviskosität |
| υ | 1 | Sicherheit |
| ρ | kg/m³ | Dichte |
| ρa | kg/m³ | Dichte der Umgebungsluft |
| ρs | kg/m³ | Dichte des Rauchs / Dichte eines Stoffs |
| ρ0 | g/m³ | Dichte der Luft unter Normalbedingungen = 1293 g/m³ |
| σ | N/mm² | Spannung |
| τ | N/mm² | Spannung (Schubspannung) |
| τij | N/mm² | Spannungstensor |
| χ | 1 | Verbrennungseffektivität |
| χr | – | radiativer Anteil der Wärmefreisetzungsrate |
| ψi | 1 | Kombinationsbeiwert für Schutz brennbaren Materials |
| ψn,i | – | Kombinationsbeiwerte nach DIN EN 1990 bzw. nationalen Festlegungen |
| ∂ | – | partielles Differential (Ableitung) |

---

### Gesamtliteraturverzeichnis Teil I (Wärme)

Vollständige Liste der im Wärmeteil zitierten Normen und Werke:

- [1] Baehr: Thermodynamik, Springer, 1984
- [2] Anderson et al.: Thermal properties of building materials — harmonised design values, EU DG XII, 1999
- [3] Cammerer: Tabellarium Wärme- und Kälteschutz, Mannheim, 1973
- [4] DIN 4108-4:2020-11 — Wärmeschutz im Hochbau, Wärme- und feuchteschutztechnische Kennwerte
- [5] DIN EN ISO 10456:2010-05 — Baustoffe: Wärme- und feuchteschutztechnische Eigenschaften, tabellierte Bemessungswerte
- [6] Glück/Recknagel/Sprenger/Schramek: Taschenbuch Heizung + Klimatechnik, Oldenbourg, 75. Aufl. 2011
- [7] VDI-Wärmeatlas, Springer, 10. Aufl. 2006
- [8] DIN EN ISO 6946:2018-03 — Wärmedurchlasswiderstand und U-Wert: Berechnungsverfahren
- [9] Hauser: Wärmebrücken bei Innendämmung, Baugewerbe 73 (1993)
- [10] Hauser/Stiegel/Haupt: Wärmebrückenkatalog auf CD-ROM, Ingenieurbüro Hauser, 1998
- [11] DIN EN ISO 10211:2018-04 — Wärmebrücken: Wärmeströme und Oberflächentemperaturen, detaillierte Berechnungen
- [12] DIN 4108-2:2013-02 — Wärmeschutz und Energieeinsparung, Mindestanforderungen
- [13] DIN EN ISO 13788:2013-05 — Oberflächentemperaturen zur Vermeidung kritischer Feuchte und Tauwasser im Bauteil
- [14] Hauser/Stiegel: Wärmebrückenatlas für Mauerwerksbau, Bauverlag, 2. Aufl. 1993
- [15] EnEV vom 16.11.2001 (Energieeinsparverordnung), BGBl. 2001 Teil I Nr. 59
- [16] DIN EN 12831:2003-08 — Heizungsanlagen: Verfahren zur Berechnung der Norm-Heizlast
- [17] Hauser: Wärmebrücken, Bauphysik-Kalender 2001, Ernst & Sohn
- [18] DIN EN ISO 10077-1:2020-10 — Wärmetechnisches Verhalten von Fenstern/Türen/Abschlüssen, Teil 1: Allgemeines
- [19] DIN EN ISO 10077-2:2018-01 — Teil 2: Numerisches Verfahren für Rahmen
- [20] DIN EN ISO 12567-1:2010-12 — U-Wert von Fenstern/Türen: Heizkastenverfahren
- [21] IFT Rosenheim: Forschungsvorhaben Warm Edge, Abschlussbericht, 1999
- [22] DIN 4108-4:2020-11 — Wärme- und feuchteschutztechnische Bemessungswerte
- [23] DIN-Fachbericht 4108-8:2010-09 — Vermeidung von Schimmelwachstum in Wohngebäuden
- [24] DIN 1946-6:2019-12 — Lüftung von Wohnungen, Allgemeine Anforderungen
- [25] GEG (Gebäudeenergiegesetz), BGBl. 2020 Teil I Nr. 37, 13.08.2020
- [26] DIN 4108-7:2011-01 — Luftdichtheit von Gebäuden: Anforderungen und Ausführungsempfehlungen
- [27] Maas: Luftwechsel bei Fensterlüftung, Dissertation Uni Kassel, 1995
- [28] Daler et al.: Bestandsaufnahme freier Lüftungseinrichtungen im Wohnungsbau, BMFT Forschungsbericht T 84-028, 1984
- [29] Schmidt/Hauser: Luftaustausch in Gebäuden, DFG-Forschungsvorhaben, Uni Kassel, 1998
- [30] RWE Bau-Handbuch mit EnEV 2009, EW Medien und Kongresse, 14. Ausgabe, 2010
- [31] Hall/Hauser: In-situ-Quantifizierung von Leckagen bei Holzbauten, AIF-Forschungsvorhaben 12611 N, 2003
- [32] Hall: Luftdichtheitsprobleme im Holzbau, 2. Sachverständigentag BDZ, 2001
- [33] DIN EN ISO 9972:2018-12 — Luftdurchlässigkeit von Gebäuden: Differenzdruckverfahren
- [34] Bansal/Hauser/Minke: Passive Building Design, Elsevier, 1994
- [35] Hauser: Passive Sonnenenergienutzung durch Fenster (keq-Werte), HLH 34 (1983)
- [36] Hens: Building Physics — Heat, Air and Moisture, Ernst & Sohn, 2007
- [37] DIN EN 673:2011-04 — Glas im Bauwesen: Bestimmung des U-Werts, Berechnungsverfahren
- [38] Hauser: Rechnerische Vorherbestimmung des Wärmeverhaltens großer Bauten, Dissertation Uni Stuttgart, 1977
- [39] Möhl/Hauser/Müller: Baulicher Wärmeschutz, Feuchteschutz und Energieverbrauch, Expert-Verlag, 1984
- [40] DIN V 4108-6:2003-06 — Jahres-Heizwärme- und Jahresheizenergiebedarfsberechnung
- [41] DIN V 4701-10:2006-12 — Energetische Bewertung heiz- und raumlufttechnischer Anlagen, mit Änderungsblatt A1
- [42] DIN 4108 Beiblatt 2:2019-06 — Wärmebrücken: Planungs- und Ausführungsbeispiele
- [43] DIN 4108-2:2013-02 — Mindestanforderungen an den Wärmeschutz
- [44] GEG 2020 (wie Nr. 25)
- [45] DIN V 4701-10 Bbl 1: Anlagenbeispiele für Heizung/Trinkwassererwärmung/Lüftung, 02/2007
- [46] DIN V 18599:2018-09 — Energetische Bewertung von Gebäuden: Nutz-, End- und Primärenergiebedarf
- [47] DIN 4108-7:2011-01 — Luftdichtheit (wie Nr. 26)
- [48] David et al.: Heizen, Kühlen, Belüften und Beleuchten — Bilanzierungsgrundlagen nach DIN V 18599, Fraunhofer IRB, 2006
- [49] Bansal/Hauser/Minke: Passive Building Design (wie Nr. 34)
- [50] DIN EN ISO 10456:2010-05 (wie Nr. 5)
- [51] VDI-Wärmeatlas (wie Nr. 7)
- [52] Cammerer: Tabellarium (wie Nr. 3)
- [53] Hauser: Der k-Wert im Kreuzfeuer — Wärmedurchgangskoeffizient als Maß für Transmissionswärmeverluste? Bauphysik 3 (1981)
- [54] DIN 4710:2003-01 — Meteorologische Daten für Energiebedarfsberechnungen heiz-/raumlufttechnischer Anlagen
- [55] Hauser/Otto: Erhöhter Wärmeschutz und sommerliche Behaglichkeit, Bauphysik 19 (1997)
- [56] Hauser: Einfluss von Glasflächen auf sommerliche Gebäudeerwärmung, VDI-Bericht 316, 1978
- [57] DIN EN ISO 52022-1:2018-01 — Sonnenschutz kombiniert mit Verglasung: Berechnung Solarstrahlung und Lichttransmissionsgrad, Teil 1: vereinfachtes Verfahren
