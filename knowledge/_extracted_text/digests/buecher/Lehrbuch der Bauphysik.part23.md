# Lehrbuch der Bauphysik — Teil 23
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 921-960.

Dieser Teil behandelt die physikalischen und chemischen Grundlagen des Brandgeschehens (Pyrolyse, Verbrennung, Brandphasen, Normbrand, äquivalente Branddauer, Bemessungsbrand) sowie das mechanische und thermische Hochtemperaturverhalten der Baustoffe Stahl und Beton. Autor: Olaf Riese (iBMB, TU Braunschweig). Die Kapitel 33 und 34 bilden den Kern.

## Inhalt

### Kapitel 33 — Grundlagen des Brandes und Brandverlauf

#### 33.1 Pyrolyse und Verbrennung

Die relative Zersetzungsrate eines Brennstoffs in der festen Phase folgt dem Arrhenius-Gesetz (Gl. 33.1). Darin gehen ein:
- Universelle Gaskonstante R = 8,314 J/(mol·K)
- Oberflächentemperatur des Stoffes T in Kelvin
- Aktivierungsenergie E in J/mol
- Vor-exponentieller Faktor A in m/s
- Dichte des Stoffs ρ in kg/m³
- Massenanteile des beteiligten Sauerstoffs Y_O und des Brennstoffs Y_S
- Konstanten m und n (bei sauerstoffunabhängiger Zersetzung ist m = 0)

Viele Stoffe zeigen mehrere Zersetzungsstufen in verschiedenen Temperaturbändern — in solchen Fällen wird die Gleichung mehrfach und parallel angewendet, jeweils mit charakteristischen Aktivierungsenergien E und vor-exponentiellen Faktoren A. Methode zur Ableitung dieser Größen: Thermogravimetrische Analyse nach DIN 51006.

Die bei der Zersetzung freigesetzten Gase können mit Luftsauerstoff reagieren und oxidiert werden. Für Brennstoffe auf Kohlenstoff-Wasserstoff-Basis ergibt sich die Verbrennungsreaktionsgleichung (Gl. 33.2):

Reaktionspartner: C (Kohlenstoff), H (Wasserstoff), O₂ (Sauerstoff), N₂ (Stickstoff), ggf. Halogene Y (z. B. Chlor).
Produkte: CO₂ (Kohlendioxid), CO (Kohlenmonoxid), H₂O (Wasserdampf), N₂ (Stickstoff), HY (z. B. Salzsäure HCl).
Die molaren Anteile a (C), b (H), c (O), d (N), e (Halogene) je mol beschreiben die Brennstoffzusammensetzung.

Fehlen ausreichend Sauerstoff oder zu hohe Mindesttemperaturen, verbrennen die Pyrolysegase nicht vollständig — Energiefreisetzung entfällt anteilig.

Stöchiometrischer Luftbedarf (Gl. 33.3):
- Berechnet aus chemischer Zusammensetzung des Brennstoffs
- Parameter: Molmasse des Brennstoffs, Sauerstoffanteil in Zuluft X_O₂, molares Normvolumen V_m = 0,0224136 m³/mol, Luftdichte unter Normalbedingungen ρ₀ = 1,293 g/m³
- Ergebnis r: stöchiometrischer Luftbedarf in g_Luft/g_Brennstoff

Einflussfaktoren auf den Pyrolyseprozess (feste Phase) und den Verbrennungsprozess (Gasphase) — Abb. 33.1 — umfassen:
- Art des Stoffs: chemische Zusammensetzung, Reinheit
- Eigenschaften: Zündtemperatur, Pyrolyserate, Vergasungswärme, Verbrennungswärme, Wärmeleitfähigkeit, spezifische Wärme, Dichte
- Zustand: Aggregatzustand, spezifische Oberfläche, Feuchtigkeit, Temperatur, Druck
- Art der Verbrennung: Sauerstoffzufuhr, Durchmischung der Reaktionspartner
- Zündquelle: Art, Dauer, Intensität, Anwesenheit von Katalysatoren

#### 33.2 Brandverlauf und Einflüsse

Der zeitliche Verlauf eines Brandes wird maßgeblich bestimmt durch:
- Menge und Art der Brandlast (Gesamt-Wärmepotential)
- Konzentration und Lagerungsdichte der Brandlast
- Räumliche Verteilung der Brandlast im Raum
- Raumgeometrie
- Thermische Eigenschaften der raumumschließenden Bauteile (Wärmeleitfähigkeit, Wärmekapazität)
- Ventilationsbedingungen (Sauerstoffzufuhr)
- Löschmaßnahmen

Quantitative Wechselwirkungen zwischen diesen Parametern sind noch nicht vollständig erforscht, weil Messungen bislang fast ausschließlich in relativ kleinen Räumen möglich waren.

**Drei Brandphasen:**

1. **Schwelbrandphase (Entstehungsbrand):** Nach der Zündung breitet sich der Brandherd aus und erhitzt die Raumluft bis zum Feuerübersprung (Flashover). Diese Phase hängt hauptsächlich vom Raumvolumen und der Brandlast ab. Bei dichten Brandlasten kann sie lang dauern; bei Flüssigkeitsbränden tritt der Flashover sehr rasch nach Zündung ein.

2. **Erwärmungsphase des Vollbrandes:** Nach dem Flashover steigen die Raumtemperaturen stark an. Die erreichten Temperaturen und die Dauer dieser Phase hängen von Brandlast, Sauerstoffangebot (Raumgeometrie und Ventilation) sowie den thermischen Eigenschaften der Raumhülle ab. Hoch wärmedämmende Baustoffe (geringe Wärmeleitfähigkeit) führen zu höheren Brandraumtemperaturen. Diese Phase stellt den eigentlichen Brandangriff auf das Bauwerk dar.

3. **Abkühlphase:** Die Restenergie des abbrennenden Materials reicht nicht mehr zur Aufrechterhaltung der Brandraumtemperatur aus. Die aufgeheizten Bauteile geben Wärme zurück in den Brandraum — dieser Rückfluss bestimmt den Temperaturabfall in der Heißgasphase weitgehend mit.

#### 33.3 Normbrand (ETK)

Zur Schaffung einheitlicher Prüf- und Beurteilungsgrundlagen für das Brandverhalten von Bauteilen wurde auf internationaler Ebene die **Einheitstemperaturzeitkurve (ETK)** festgelegt. Ihr folgen die Bauteilprüfungen nach:
- DIN 4102-2, -3, -5, -6, -9, -11
- DIN EN 1363 bis DIN EN 1366
- DIN EN 13501

Die ETK folgt dem mathematischen Gesetz (Gl. 33.4):
`ϑ - ϑ₀ = 345 · lg(8t + 1)`

Darin bedeuten:
- ϑ = Brandraumtemperatur (K)
- ϑ₀ = Temperatur des Probekörpers bei Versuchsbeginn (K)
- t = Zeit (min)

Die ETK gibt einen realen Brand nur näherungsweise wieder: Sie bildet weder den unterschiedlich schnellen Temperaturanstieg der Erwärmungsphase noch den abfallenden Ast der Abkühlphase ab. Sie dient als einheitlicher Bewertungsmaßstab für alle Bauteile (bekleidete Stahlträger, Leichtbau-Trennwände, Stahlbeton-Kassettendecken, Stahl-Schiebetore usw.) in Bauwerken unterschiedlichster Nutzung. Der Nachweis zeigt, dass auf diesem Brandmodell basierende bauaufsichtliche Anforderungen ein ausreichendes Sicherheitsniveau erzeugen.

#### 33.4 Äquivalente Branddauer

Das Konzept der äquivalenten Normbranddauer dient dazu, natürliche Brände mit dem Normbrand vergleichbar zu machen. Die **äquivalente Normbranddauer t_ä** ist die Dauer eines Normbrandes, bei der in einem Bauteil näherungsweise dieselbe Schadenwirkung entsteht wie beim vollständigen Ablauf eines natürlichen Schadenfeuers. Als Schadenwirkung gilt meist die erreichte Temperatur an einem kritischen Bauteilpunkt (z. B. Bewehrung eines Stahlbetonbauteils auf Biegung).

**Näherungsformel für ummantelte Stahlbauteile (Gl. 33.5):**

`t_ä = 0,067 · (k_f · q_t / (A√h / A_t)) [min]`

Parameter:
- q_t: Brandbelastung je innere Oberfläche des Brandraums in MJ/m²
- k_f: Beiwert für unterschiedliche thermische Eigenschaften der raumumschließenden Bauteile
- A√h/A_t: Öffnungsfaktor zur Beschreibung der Ventilationsbedingungen in m^(1/2)
  - A: Fläche der Fenster- und Türöffnungen (m²)
  - h: mittlere Höhe der Fenster- und Türöffnungen (m)
  - A_t: innere Oberfläche des Brandraums — Boden, Decke, Wände einschließlich Öffnungen (m²)

Die Formel wird unter Vorbehalt auch für Bauteile aus anderen Werkstoffen verwendet.

**Erweiterte Formel nach DIN 18230 „Baulicher Brandschutz im Industriebau" (Gl. 33.6):**

`t_ä = q_R · c · w [min]`

Rechnerische Brandbelastung q_R:
`q_R = Σ(M_i · H_ui · m_i · ψ_i) / A`

Parameter:
- M_i: Masse des einzelnen brennbaren Stoffs (kg)
- H_ui: Heizwert des einzelnen Stoffs (kWh/kg)
- A: Grundfläche des Brandraums bzw. Brandbekämpfungsabschnitts (m²)
- m_i: Abbrandfaktor des Stoffs, berücksichtigt Form, Verteilung, Lagerungsdichte, Feuchte
- ψ_i: Kombinationsbeiwert für Schutz des brennbaren Materials (z. B. Heizöl in Behältern)
- c: Umrechnungsfaktor für thermische Eigenschaften der raumumschließenden Bauteile (min·m²/kWh)
- w: Wärmeabzugsfaktor für Ventilationsbedingungen

Beide Gleichungen (33.5 und 33.6) basieren auf denselben Grundansätzen und liefern vergleichbare Ergebnisse, wenn in Gl. 33.6 die Beiwerte m_i und ψ_i gleich 1 gesetzt werden.

#### 33.5 Bemessungsbrand

Der **Bemessungsbrand (design fire)** ist ein theoretischer, aber grundsätzlich möglicher Brandverlauf, der eine Vielzahl denkbarer Brandentwicklungen auf der sicheren Seite abdeckt. Er muss nicht jeden möglichen Brandverlauf erfassen, aber alle resultierenden Gefahren hinreichend sicher beschreiben. Grundannahme in Brandschutzkonzepten: Brand beginnt an einer einzigen Stelle im Gebäude; Brandübertragungen auf weitere Objekte sind zu berücksichtigen.

Zentrale Größe: die **Wärmefreisetzungsrate HRR (Heat Release Rate)**. Aus ihr lassen sich Entstehungsraten weiterer Brandprodukte einschließlich Rauchpartikeln ableiten — auch als Quellterm bezeichnet.

**Möglichkeiten zur Ermittlung der Wärmefreisetzungsrate:**
- a) Experimente mit ähnlicher Brandlast unter ähnlichen Raum- und Ventilationsbedingungen
- b) Berechnungen — Pyrolysemodelle für prognostische Brandentwicklung sind wissenschaftlich noch nicht ausreichend gesichert; eingeschränkt möglich ist die Vorausrechnung bei Brandausbreitung durch Feuerüberschläge
- c) Vereinbarung auf Basis von Schadenauswertungen oder Literaturkurven für Sonderfälle (z. B. brennendes Sofa)
- d) Normative Vorgaben und technische Regelwerke (VDI-Richtlinien, Leitfaden Ingenieurmethoden)

Der Bemessungsbrand beschreibt typischerweise eine „ungestörte" Brandentwicklung bei ausreichender Sauerstoffzufuhr (brandlastgesteuerter Abbrand). Bei ventilationsgesteuertem Abbrand kann sich das Schadstoffpotential und die Rauchentwicklung verändern; Abweichungen vom ursprünglichen Verlauf sind zu dokumentieren.

##### 33.5.1 Standardisierte Bemessungsbrände

Schematisierter Brandverlauf für Berechnungen gliedert sich in drei Phasen:
- Brandausbreitungsphase (bis Zeitpunkt t₁)
- Vollbrandphase (t₁ bis t₂)
- Abklingender Brand (t₂ bis t₃)

Kenngrößen:
- Q_s: Wärmefreisetzungsrate zum Zeitpunkt t₀ (Übergang Schwelbrand → ausbreitender Brand), typisch Q_s = 25 kW
- Q₀ = 1000 kW (Referenzgröße)
- t_g: Brandentwicklungszeit in Sekunden bis zum Erreichen einer Brandstärke von 1 MW; typische Literaturwerte: 75 bis 600 Sekunden; quadratischer Ansatz für die Ausbreitungsphase
- Q_max,v: maximale Wärmefreisetzungsrate des ventilationsgesteuerten Brandes
- Q_max,f: maximale Wärmefreisetzungsrate des brandlastgesteuerten Brandes
- Q₁ bis Q₃: in den einzelnen Phasen umgesetzte Brandlasten (Integrale der Wärmefreisetzungskurve)

Gesamte Brandlast Q (Gl. 33.14):
`Q = Σ(m_i · H_u,i) [MJ]`
mit m_i = Masse des brennbaren Stoffs (kg) und H_u,i = unterer Heizwert (MJ/kg).

Effektive Brandlast unter Berücksichtigung des Verbrennungseffektivitätsfaktors χ_i (Gl. 33.15):
`Q_eff = Σ(m_i · H_c,eff,i) = Σ(m_i · χ_i · H_u,i)`

**Zwei Brandregime:**

a) **Brandlastgesteuerter Brand:** Selbst bei vollständiger Einbindung aller Brennstoffe wird die Brandleistung durch die verfügbare Brandlast begrenzt.

Maximale Wärmefreisetzungsrate (Gl. 33.7):
`Q_max,f = m″ · H_u · χ · A_f [MW]`
- m″: flächenspezifische Abbrandrate (kg/(s·m²))
- H_u: unterer Heizwert (MJ/kg)
- χ: Verbrennungseffektivität — nach DIN EN 1991-1-2: feststoffartige Brandlasten χ = 0,8; flüssige χ = 0,9; gasförmige χ = 1,0
- A_f: Grundfläche des Brandraums (m²)

b) **Ventilationsgesteuerter Brand:** Mangel an Verbrennungsluft begrenzt die Gesamtbrandleistung, unabhängig von der vorhandenen Brennstoffmenge.

Maximale Wärmefreisetzungsrate (Gl. 33.8):
`Q_max,v = m_L · H_i / r · χ_O₂ [MW]`
- m_L: Zuluftmassenstrom (kg/s)
- H_i: Heizwert der brennbaren Stoffe (MJ/kg)
- χ_O₂: Sauerstoffausnutzungsgrad
- r: stöchiometrischer Luftbedarf (kg_Luft/kg_Brennstoff)

Empirischer linearer Zusammenhang zwischen stöchiometrischem Luftbedarf und Heizwert organischer Brandlasten (Gl. 33.9):
`r ≈ 0,33 · H_i [kg_Luft/kg_Brennstoff]`
Gilt sowohl für vollständige als auch unvollständige Verbrennung.

Zuluftmassenstrom bei natürlichen vertikalen Wandöffnungen nach Kawagoe (Gl. 33.10):
`m_L = 0,52 · A_W · √h_W [kg/s]`
- A_W: Fläche der Ventilationsöffnungen (m²)
- h_W: lichte Öffnungshöhe (m)

Daraus maximale ventilationsgesteuerte Wärmefreisetzungsrate (Gl. 33.11):
`Q_max,v = 1,57 · χ_O₂ · A_W · √h_W [MW]`

Bei Sauerstoffausnutzungsgrad χ_O₂ = 0,8 vereinfacht sich dies zu (Gl. 33.12):
`Q_max,v = 1,26 · A_W · √h_W [MW]`

Bei mehreren Wandöffnungen i wird die effektive Öffnungshöhe h_W berechnet als gewichtetes Mittel (Gl. 33.13):
`h_W = Σ(h_W,i · A_W,i) / A_W,ges`

Die maximale Wärmefreisetzungsrate insgesamt ist der kleinere der beiden Maximalwerte:
`Q_max = MIN{Q_max,v ; Q_max,f}`

In Brandsimulationsprogrammen wird die Sauerstoffkonzentration intern kontrolliert — daher ist der brandlastgesteuerte Ansatz praxistauglich, da das Programm den tatsächlichen Verlauf selbst aus den Randbedingungen berechnet. Flashover ist bei einfachen Raumgeometrien vorhersagbar; bei komplexen Geometrien eingeschränkt.

##### 33.5.2 Ausbreitung

Wenn eine Brandausbreitung nicht durch den standardisierten Ansatz abgedeckt werden kann (z. B. große oder mehrere einzelne Brandflächen; zeitliche Effekte entscheidend), muss sie möglichst realistisch beschrieben werden. Grundlage: brandgutbezogene Tabellenwerte aus Experimenten. Normative Werte: DIN 18230-1, DIN 18230-2, DIN EN 1991-1-2 Anhang E.

Richtwerte für Brandausbreitungsgeschwindigkeiten:
- Langsame Ausbreitung: ca. 0,15 m/min
- Schnelle Ausbreitung: ca. 3,0 m/min
- Grenzwert Flashover: Werte über 4–6 m/min gelten als Indikator

Übertragbarkeit auf Bemessungsbrände ist schwierig, da Ausbreitungsgeschwindigkeit stark von Randbedingungen (Luftwechsel, Stapelung des Brandguts) abhängt.

##### 33.5.3 Löschung

Löschmaßnahmen (z. B. Sprinklerung oder Feuerwehreinsatz) können vorab abgeschätzt und dem Bemessungsbrand zugrunde gelegt werden. In einem sprinklergeschützten Raum wird die Wärmefreisetzung eingeschränkt. Je nach Auslösezeitpunkt t_akt und Löscheffektivität entstehen unterschiedliche Verläufe:
- Brandbeherrschung (Reduktion der Wachstumsrate, aber kein Löschen)
- Brandunterdrückung (deutliche Abschwächung)
- Brandlöschung (vollständiges Erlöschen)

Berücksichtigung von Löschmaßnahmen muss mit der zuständigen Behörde abgestimmt werden.

---

### Kapitel 34 — Mechanische und thermische Hochtemperatureigenschaften der Baustoffe

Alle Kennwerte für mechanisches und thermisches Verhalten sind temperaturabhängig. Dies gilt besonders für mechanische Eigenschaften; thermische Änderungen müssen ebenfalls berücksichtigt werden.

**Versuchsarten zur Bestimmung mechanischer Hochtemperaturkennwerte (Tab. 34.1):**

| Versuchsart | Spannung | Dehnung | Temperatur | Auswertungsgröße |
|---|---|---|---|---|
| I a) ohne Vorlast | variabel | gemessen | konstant | σ-ε-Diagramm |
| I b) mit Vorlast | variabel | gemessen | konstant | σ-ε-Diagramm |
| II | konstant | gemessen | variabel | Hochtemperatur-Kriechen |
| III | gemessen | konstant | variabel | Hochtemperatur-Relaxation |

In den heißen Eurocodes werden Festigkeits- und Verformungseigenschaften als temperaturabhängige Spannungs-Dehnungsbeziehungen beschrieben, deren Zahlenwerte überwiegend aus Versuchen der Art II stammen. Das Ergebnis hängt von Prüftemperatur, Erwärmungsgeschwindigkeit sowie Vorlast während der Erwärmung ab.

#### 34.1 Stahl

##### 34.1.1 Festigkeit und Verformung

Zusammensetzung und Herstellungsverfahren beeinflussen das Hochtemperaturverhalten entscheidend.

Kaltverformte Beton- und Spannstähle besitzen erhöhte Raumtemperaturfestigkeit durch Verzerrungen und Versetzungen im Mikrogefüge. Bei Temperatureinwirkung heilen diese Gitterfehler aus (Erholung, Rekristallisation, Ausscheidungs- und Koagulationsvorgänge), die Festigkeit sinkt, die Verformungsfähigkeit steigt. Bei kaltverformten Betonstählen ist der Verfestigungseffekt nach Einwirkung von rund **400 °C** über längere Zeit vollständig aufgehoben.

Durch thermische Nachbehandlung entstandene Festigkeitssteigerungen (Ausscheidungs- und Aufspaltungsprozesse) werden abgebaut, sobald die Behandlungstemperatur wieder erreicht oder überschritten wird.

Für Stähle ohne ausgeprägte Streckgrenze bei Raumtemperatur gilt vereinbarungsgemäß die β₀,₂-Grenze: diejenige Spannung, die nach Entlasten eine bleibende Dehnung von 0,2 % erzeugt. Im Hochtemperaturbereich wird analog vorgegangen.

**Kriterium für Stahlversagen unter Hochtemperatur:** eine kritische Dehngeschwindigkeit von
`ε̇ = 10⁻⁴ /s`
Die Temperatur beim Erreichen dieses Wertes heißt **kritische Stahltemperatur**. Sie ist spannungsabhängig: höhere Stahlspannung → niedrigere kritische Stahltemperatur. Nach Erreichen der kritischen Dehngeschwindigkeit geht ε̇ sehr rasch gegen Unendlich (Riss).

Auf ein biegebeanspruchtes Bauteil übertragen bedeutet dies eine rapide Zunahme der Durchbiegung und der Durchbiegungsgeschwindigkeit bis zum Biege-(Zug-)Bruch.

Druckverhalten wird mangels systematischer Untersuchungen dem Zugverhalten gleichgesetzt.

##### 34.1.2 Elastizität

Der Elastizitätsmodul von Stahl nimmt mit steigender Temperatur ab. Nachbehandelte Stähle verlieren ihn schneller als naturharte. Der Unterschied ist gering; eine einheitliche Kurve kann näherungsweise für alle Stahlsorten angesetzt werden.

##### 34.1.3 Thermische Dehnung

Die thermische Dehnung von Bau- und Betonstählen kann für den brandrelevanten Bereich bis ca. 700 °C als annähernd linear angenommen werden mit:
`α_ϑ = const = 1,4 · 10⁻⁵ /K`

Bei kaltgezogenem Spannstahl bewirken die Mikrostrukturveränderungen auch Abweichungen in der thermischen Dehnung. Bei hohen Temperaturen treten Unstetigkeiten durch nicht eliminierbare Schrumpfeffekte auf.

##### 34.1.4 Wärmeleitfähigkeit

Die Wärmeleitfähigkeit λ von Stählen hängt stark von der Zusammensetzung ab. Übliche Baustähle zeigen einen mit steigender Temperatur abnehmenden Verlauf. Manche hochlegierten Stähle zeigen dagegen eine Zunahme der Wärmeleitfähigkeit mit der Temperatur.

##### 34.1.5 Spezifische Wärmekapazität

Die spezifische Wärmekapazität c_p üblicher Bau-, Beton- und Spannstähle ist temperaturabhängig (Verlauf in Diagrammform, Abb. 34.8).

##### 34.1.6 Dichte

Für praktische Berechnungen wird die Stahldichte als temperaturunabhängige Konstante angesetzt:
`ρ = 7850 kg/m³`

##### 34.1.7 Temperaturleitfähigkeit

Die Temperaturleitfähigkeit `a = λ / (c_p · ρ)` ist von der Stahlzusammensetzung abhängig. Der Verlauf für übliche Baustähle gilt näherungsweise auch für Beton- und Spannstähle.

##### 34.1.8 Temperaturverteilung in bekleideten Stahlquerschnitten

Ungeschützte Stahlbauteile versagen im Brandfall sehr früh und erfüllen keine brandschutztechnischen Anforderungen. Für ummantelte Querschnitte gelten folgende vereinfachende Annahmen:

- Stahl setzt dem Wärmedurchgang keinen Widerstand entgegen → gleichförmige Temperatur im Stahlquerschnitt (bei Vollprofilen großer Abmessungen ungünstig, da Randtemperatur maßgebend)
- Wärmekapazität der Bekleidung wird vernachlässigt → linearer Temperaturgradient über die Bekleidungsdicke
- Bei „leichter" Ummantelung (Spezialputze, Brandschutzplatten) ausreichend genau; bei „schwerer" Ummantelung (Betonummantelung, Ummauerung) führt dies zu ungünstigen Ergebnissen
- Übergangswiderstand Bekleidung → Stahl wird vernachlässigt

Wärmeübergangswert k (vereinfacht):
`1/k = 1/α_c + 1/α_r + d_i/λ_i`

Da `1/α_c + 1/α_r ≪ d_i/λ_i` vereinfacht sich dies praktisch zu:
`k ≈ λ_i / d_i`

Dabei bedeuten:
- α_c: konvektiver Wärmeübergangskoeffizient Heißgas-Bekleidung (W/(m²K))
- α_r: radiativer Wärmeübergangskoeffizient Heißgas-Bekleidung (W/(m²K))
- d_i: Bekleidungsdicke (m)
- λ_i: temperaturabhängige Wärmeleitfähigkeit der Bekleidung (W/(mK)) — schließt Effekte wie Risse und Klüfte im Material näherungsweise ein

**Profilfaktor:** Die Erwärmung eines Stahlprofils hängt wesentlich vom Verhältnis U/A ab:
- U: dem Wärmefluss ausgesetzter (erwärmter) Umfang (m)
- A: Querschnittsfläche des Stahlprofils (m²)
- Bei profilfolgender Ummantelung: U = Stahlprofilabwicklung; bei kastenförmiger Bekleidung: U = innere Kastenabwicklung
- Im Eurocode 3 wird das inverse Verhältnis A/V als Profilfaktor verwendet

Temperaturerhöhung Δϑ_s eines mit leichter Ummantelung versehenen Stahlquerschnitts im Zeitintervall Δt (Gl. 34.4):
`Δϑ_s = (λ_i/d_i) · (U/A) · (ϑ_t - ϑ_s) · Δt / (c_s · ρ_s)`

Parameter:
- ϑ_t: mittlere Heißgastemperatur im Zeitintervall (°C)
- ϑ_s: mittlere Stahltemperatur im Zeitintervall (°C)
- Δt: Zeitintervall (s) — muss ausreichend klein gewählt werden für Konvergenz
- c_s: spezifische Wärmekapazität des Stahls (J/(kgK))
- ρ_s: Rohdichte des Stahls (kg/m³)

**Eurocode-3-Formel (DIN EN 1992-1-2, Abschn. 4.2.5.2, Gl. 34.5)** für wärmegedämmte Stahlquerschnitte berücksichtigt zusätzlich die Speicherfähigkeit der Bekleidung über den Term ϕ:
`Δϑ_s = (λ_p/d_p) · (A/V) · (ϑ_t - ϑ_s) · Δt / (c_p,s · ρ_s) · (1/(1 + ϕ/3))`
(gilt nur wenn ϑ_t - ϑ_s > 0; sonst kein Temperaturanstieg)

Dabei: ϕ = (c_p · ρ_p · d_p) / (c_s · ρ_s) (Verhältnis Wärmespeicherkapazität Bekleidung zu Stahl)
- λ_p: Wärmeleitfähigkeit des Brandschutzsystems (W/(mK))
- d_p: Dicke des Brandschutzmaterials
- ρ_p: Rohdichte des Brandschutzmaterials (kg/m³)
- c_p: temperaturabhängige spezifische Wärmekapazität des Stahls (J/(kgK))

Bei ϕ = 0 reduziert sich Gl. 34.5 auf Gl. 34.4.

**Berechnungsbeispiel — Stahlprofil HEB (IPB) 200 unter Normbrandbeanspruchung:**

Bekleidung: Spritzputz bzw. Platten auf Vermiculitebasis
- Bekleidungsdicke: d_i = 0,03 m
- Wärmeleitfähigkeit: λ_i = 0,15 W/(mK) (nach d_i = 0,2)
- Profilfolgend: U/A = 1,15/78,1·10⁻⁴ = 147 m⁻¹
- Kastenförmig: U/A = 4·0,20/78,1·10⁻⁴ = 103 m⁻¹
- Zeitintervall Δt = 30 s

Ergebnistabelle (Stahltemperaturen zu bestimmten Zeiten):

| Zeit t (min) | Brandraumtemperatur ϑ_t (°C) | Stahltemperatur profilfolg. (°C) | Stahltemperatur kastenförmig (°C) |
|---|---|---|---|
| 0 | 20 | 20 | 20 |
| 30 | 842 | 206 | 157 |
| 60 | 945 | 379 | 298 |
| 90 | 1006 | 514 | 417 |
| 120 | 1049 | 620 | 515 |

Der Einfluss des Profilfaktors U/A auf die Erwärmungsgeschwindigkeit ist deutlich erkennbar — größerer U/A-Wert → stärkere Erwärmung.

#### 34.2 Beton

Bei der Erwärmung von Beton laufen im Zementstein und Zuschlag gleichzeitig physikalische, chemische und mineralogische Umwandlungen ab, deren Wirkungen sich überlagern. Generell nimmt mit steigender Temperatur die Festigkeit ab, die Verformungsfähigkeit zu. Unterschiede bestehen zwischen verschiedenen Normalbetonen (PZ, HOZ, quarzitischer oder Kalkstein-Zuschlag) sowie zwischen Normalbeton und Konstruktionsleichtbeton mit geblähten Zuschlägen.

##### 34.2.1 Festigkeit

Druckfestigkeit (σ-ε-Diagramme) nimmt mit steigender Temperatur ab. Unterschiedliche Zuschläge (quarzhaltig vs. Blähton) und unterschiedliche Vorlasten beeinflussen die Hochtemperaturfestigkeit signifikant. Betonzugfestigkeit unter Hochtemperatur ist bislang nicht systematisch untersucht; biaxiales Druckverhalten unter erhöhter Temperatur befindet sich in frühem Forschungsstadium.

##### 34.2.2 Elastizität

Der Elastizitätsmodul nimmt mit steigender Temperatur ab. Sowohl Zuschlagart als auch mechanische Beanspruchung während der Erwärmung beeinflussen den Verlauf.

##### 34.2.3 Gesamtverformung

Bei konstanter Druckspannung unter instationärer Erwärmung (Versuchsart II) überlagern sich der thermischen Dehnung lastabhängige Stauchungsanteile. Die Gesamtverformung hängt neben dem Hauptparameter Belastungsgrad auch von Zementgehalt, Betongüte, Lagerung und Zuschlagart ab — die Zuschlagart hat dominierenden Einfluss. Quarzbeton und Blähtonbeton zeigen deutlich unterschiedliche Verformungsverläufe.

##### 34.2.4 Kritische Temperatur

Die **kritische Betontemperatur** ist diejenige Temperatur, bei der unter konstanter Belastung die Stauchgeschwindigkeit einen kritischen Grenzwert überschreitet — vergleichbar dem Konzept bei Stahl. Dieser Zustand entspricht dem Biege-(Druck-)Bruch des Bauteils. Aus Versuchsart-II-Messungen ableitbar. Streubereiche für Normal- und Leichtbetone sind in Diagrammform angegeben.

##### 34.2.5 Zwängung

Versuche der Art III (konstante Dehnung, variable Temperatur) liefern Zwängungskräfte in dehnbehinderten Betonproben. Die zeitliche Entwicklung der Zwangskräfte verläuft diskontinuierlich — beeinflusst vor allem durch Entwässerungs- und Dehydratationsvorgänge im Beton.

##### 34.2.6 Thermische Dehnung

Die thermische Dehnung von Beton weicht deutlicher als die von Stahl von der Linearität ab und ist stark von der Zuschlagart abhängig. Betonstahl zeigt im Vergleich eine annähernd lineare thermische Dehnung.

##### 34.2.7 Wärmeleitfähigkeit

Die Wärmeleitfähigkeit λ von Beton sinkt mit steigender Temperatur. Unterhalb von ca. 100 °C wird sie durch den Feuchtegehalt mitbestimmt. Die Zuschlagart hat wesentlichen Einfluss auf das absolute Niveau und den Temperaturverlauf.

##### 34.2.8 Spezifische Wärmekapazität

Die spezifische Wärmekapazität c_p verschiedener Betone ist temperaturabhängig und unterscheidet sich je nach Zuschlagart.

##### 34.2.9 Dichte

Für praktische Berechnungen wird die Betondichte als konstant (Raumtemperaturwert) angesetzt. Der bei Erwärmung auftretende Wasserverlust ist jedoch zu berücksichtigen.

##### 34.2.10 Temperaturleitfähigkeit

Die Temperaturleitfähigkeit `a = λ / (c_p · ρ)` setzt sich aus den einzelnen temperaturabhängigen Komponenten zusammen. Beispiel: Für quarzhaltigen Beton ist der Verlauf in Diagrammform dargestellt.

##### 34.2.11 Temperaturverteilung

**Fourier'sche Differentialgleichung (Gl. 34.6):**
`c_p · ρ · ∂ϑ/∂t = div(λ · grad(ϑ)) + W`

Dabei:
- c_p: spezifische Wärmekapazität (J/(kgK))
- ρ: Dichte (kg/m³)
- ϑ: Temperatur (K)
- t: Zeit (s)
- λ: Wärmeleitfähigkeit (W/(mK))
- W: Wärmequelle oder -senke (J/(m³s))

Für Betonquerschnitte gilt diese Gleichung nur näherungsweise, da zusätzlich Feuchte- und Dampftransport stattfinden. In vereinfachter wirklichkeitsnaher Berechnung wird der Massentransport vernachlässigt; die Wärmesenken durch Dehydratation des Zementsteins und Verdampfung des Kapillarwassers werden durch eine modifizierte Wärmeleitfähigkeit erfasst.

Für ein ebenes Temperaturfeld (Koordinaten x, y) ergibt sich (Gl. 34.7):
`c_p · ρ · ∂ϑ/∂t = ∂/∂x(λ · ∂ϑ/∂x) + ∂/∂y(λ · ∂ϑ/∂y)`

Die Stoffwerte λ, c_p und Temperaturleitzahl a = λ/(c_p · ρ) sind als temperaturveränderlich einzusetzen.

**Randbedingung — Wärmefluss je Oberflächeneinheit (Gl. 34.8):**
`q = α · (ϑ_t - ϑ_ct)`

Mit:
- α = α_c + α_r: Gesamter Wärmeübergangskoeffizient (W/(m²K))
- α_c: konvektiv (W/(m²K))
- α_r: radiativ (W/(m²K))
- ϑ_t: Gastemperatur zur Zeit t (°C)
- ϑ_ct: Oberflächentemperatur des Querschnitts zur Zeit t (°C)

An der Querschnittsoberfläche gilt ferner (Gl. 34.9):
`q = -λ · grad(ϑ_ct)`

**Wärmeübergangskoeffizienten unter Normbrandbedingungen:**

Konvektiv α_c (näherungsweise als Konstante):
- Erwärmte Oberfläche: α_c ≈ 25 W/(m²K)
- Feuerabgekehrte Oberfläche: α ≈ 9 W/(m²K)

Radiativ α_r (temperaturabhängig, Gl. 34.10):
`α_r = ε_res · 5,67·10⁻⁸ · ((ϑ_t + 273)⁴ - (ϑ_ct + 273)⁴) / (ϑ_t - ϑ_ct) [W/(m²K)]`

5,67·10⁻⁸ = Stefan-Boltzmann-Konstante

Für Normbrandbedingungen darf näherungsweise die resultierende Emissivität `ε_res = 0,7` verwendet werden.

**Einflüsse auf Betonquerschnitt-Temperaturfelder:**
- Querschnittsform und -größe: Größere Masse → höhere Wärmekapazität; kleinere spezifische Oberfläche → geringere massebezogene Wärmeenergie → Einfluss auf Erwärmungsgeschwindigkeit
- Zuschlagart: entsprechend unterschiedlicher Wärmeleitfähigkeit ergeben sich unterschiedliche Erwärmungsgeschwindigkeiten
- Betonfeuchte: besonders deutlich im Bereich um 100 °C — einsetzende Verdampfung verbraucht Wärme und verzögert die Querschnittserwärmung vorübergehend; die Verzögerungsdauer hängt vom Feuchtegehalt ab und ist im Inneren des Querschnitts ausgeprägter als in den Randbereichen
- Bewehrungsstahl: Stahl hat deutlich höhere Wärmeleitfähigkeit als Beton; bei Stahlbetonquerschnitten weichen Temperaturfelder je nach Bewehrungsstahl und -lagenanzahl vom ungestörten Betonquerschnitt ab — dieser Effekt ist jedoch im Allgemeinen vernachlässigbar
