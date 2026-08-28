# Gebäudetechnik und Technischer Ausbau von Gebäuden — Teil 5
> Quelle: Gebäudetechnik und Technischer Ausbau von Gebäuden (buecher) · Seiten 201-240.

Dieses Kapitel (Kapitel 4) behandelt Wärme- und Kälteversorgungsanlagen für Gebäude. Teil 5 umfasst die Heizlast- und Kühllastvarfahren (Abschluss), Wärmeerzeugungsanlagen (Übersicht, Energieträger), Gasversorgung und -leitungen im Detail sowie Heizöllagerung und Wärmeerzeuger mit Gas/Heizöl einschließlich NT-Kessel und Brennwerttechnik.

## Inhalt

### Transmissions- und Lüftungswärmeverluste (Norm-Heizlastberechnung nach DIN EN 12831)

Der Transmissionswärmetransferkoeffizient HT,ie eines beheizten Raums (i) nach außen (e) berechnet sich aus der Summe über alle Bauteile k:
- **Ak** = Bauteilfläche [m²]
- **Uk** = Wärmedurchgangskoeffizient des Bauteils [W/(m²·K)]
- **ΔU_TB** = pauschaler Wärmebrücken-Zuschlag [W/(m²·K)]; ΔU_TB = 0 bei detaillierter Betrachtung nach Anhang C
- **fU,k** = Korrekturfaktor für Bauteileigenschaften und meteorologische Einflüsse
- **fie,k** = Temperaturanpassungsfaktor

Der Norm-Lüftungswärmeverlust eines Raums beträgt:
- ΦV,i = HV,i · (θint,i − θe)
- HV,i = Norm-Lüftungswärmeverlust-Koeffizient
- HV,i = 0,34 · Vi (mit V in m³/h; aus Dichte Luft 1,2 kg/m³ und cp = 1 kJ/(kg·K))

Luftdichtigkeit nach GEG: Umfassungsfläche einschließlich Fugen dauerhaft luftundurchlässig. Prüfung per Druckprüfung → n50-Wert ermitteln.

**Tab. Luftdichtigkeit bei 50 Pa Druckdifferenz (DIN 4108-6):**

| Luftdichtheit | Mehrfamilienhaus n50 [h⁻¹] | Einfamilienhaus n50 [h⁻¹] |
|---|---|---|
| Sehr dicht | 0,5–2,0 | 1,0–3,0 |
| Mittel dicht | 2,0–4,0 | 3,0–8,0 |
| Wenig dicht | 4,0–10,0 | 8,0–20,0 |

**Tab. Norm-Außentemperaturen (Auszug, DIN EN 12831 Beiblatt 1) – Standort → Klimazone → θe [°C] → Jahresmittel [°C]:**

| Ort | Klimazone | θe [°C] | Jahresmittel |
|---|---|---|---|
| Norderney | 1 | −10 | 9,0 |
| Pinneberg | 1 | −12 | 9,0 |
| Hamburg | 3 | −12 | 8,5 |
| Berlin | 4 | −14 | 9,5 |
| Leipzig | 4 | −14 | 8,7 |
| Aachen | 5 | −12 | 8,1 |
| Köln | 5 | −10 | 8,1 |
| Clausthal-Zellerfeld | 6 | −14 | 6,8 |
| Saarbrücken | 6 | −12 | 6,8 |
| Görlitz | 9 | −16 | 7,9 |
| Feldberg/Schwarzwald | 11 | −18 | 3,0 |
| Hof/Saale | 11 | −18 | 3,0 |
| Frankfurt a. M. | 12 | −12 | 10,2 |
| München | 13 | −16 | 7,9 |
| Ebingen/Albstadt | 14 | −18 | 6,8 |
| Mittenwald | 15 | −16 | 6,8 |

Hinweis: Norm-Auslegungsaußentemperatur wird nach aktueller DIN/TS 12831-1 digital per Postleitzahl ermittelt; liegt zwischen −10 und −16 °C (Extremstandorte wie Oberstdorf −20 °C).

Maschinelle Lüftung (z. B. innen liegende Bäder, WCs) sowie RLT-Anlagen sind gesondert zu berücksichtigen; Infiltration durch Wind und Thermik entfällt auch bei RLT-Anlagen nicht.

**Tab. Empfohlene Norm-Innentemperaturen (DIN/TS 12831-1):**

| Raumart | θ_int [°C] |
|---|---|
| Wohn- und Schlafräume | +20 |
| Büros, Sitzungsräume, Ausstellungsräume, Treppenräume, Schalterhallen | +20 |
| Hotelzimmer | +20 |
| Verkaufsräume und Läden allgemein | +20 |
| Unterrichtsräume | +20 |
| Theater- und Konzerträume | +20 |
| Bade-, Duschräume, Umkleiden, Untersuchungszimmer (unbekleideter Bereich) | +24 |
| WC-Räume | +20 |
| Beheizte Nebenräume (Flure, Treppenhäuser) | +15 |
| Gewerbe schwere Tätigkeit | +15 |
| Gewerbe mittelschwere Tätigkeit | +17 |
| Gewerbe leichte Tätigkeit | +20 |

Notwendige Unterlagen zur Heizlastberechnung:
- Lageplan mit Himmelsrichtungen, Windzutritt, umgebender Bebauung und Topographie
- Grundrisse und Ansichten mind. M 1:100 mit Raumnutzung und Fenster-/Türöffnungen
- Vertikalschnitte mit Geschosshöhen (OK-Fußboden zu OK-Fußboden), Lichtraumhöhen, Fensterbankshöhen
- Baubeschreibung mit U-Werten nach DIN 4108-4 oder Schichtaufbau aller Bauteile
- Angaben zu Verglasung, Rahmen, Fugenkoeffizient/Fenstergüteklasse nach DIN 18055

**Berechnung Gesamt-Norm-Heizlast (DIN EN 12831):**
- Summierung Transmissionswärmeverluste aller beheizten Räume (ohne internen Wärmefluss)
- Summierung Lüftungswärmeverluste aller beheizten Räume
- Addition beider Verluste
- Hinzurechnung Aufheizleistung (Korrekturfaktor) → ΦHL = Σ ΦT,i + Σ ΦV,i + Σ ΦRH,i

Luftvolumenstrom ohne RLT-Anlagen: Σ Vi = max(0,5 · Σ Vinf,i ; Σ Vmin,i). Hygienisch erforderlicher Mindeststrom Vmin wird mit 0,5 h⁻¹ angenommen, auch wenn Druckprüfung einen niedrigeren Wert ergibt. Mit RLT-Anlagen: Berücksichtigung von Zuluftvolumenstrom, Wärmerückgewinnungsgrad ηv (ohne WRG: ηv = 0) und Überschuss-Abluftvolumenstrom.

Aufheizleistung kann bis zu 137 W/m² betragen (laut DIN EN 12831); Bedingungen mit Bauherr abstimmen.

**Gesamte Wärmeerzeugerleistung:**
ΦSU = ΦHL + ΦDHW + ΦAS
- ΦHL = Heizlast
- ΦDHW = Zusatzleistung für Warmwasserbereitung (nach DIN 4708-1 bis 3)
- ΦAS = Zusatzleistung für andere Systeme (RLT, Prozesswärme usw.)

Bei statischer Heizung mit natürlicher Lüftung wird nur ΦHL als Wärmeerzeuger-Auslegungsgrundlage verwendet.

---

### Grob überschlägliche Heizlastermittlung

Orientiert sich an GEG-Grenzwerten; Anhaltswerte aus ausgeführten Objekten.

**Tab. überschlägliche Heizlast ΦHL in Abhängigkeit von A/V-Verhältnis:**

| A/V [m⁻¹] | ΦHL [W] über Kubatur | ΦHL [W] über Fläche (2,75 m Gh) | ΦHL [W] über Fläche (3,25 m Gh) |
|---|---|---|---|
| ≤ 0,20 | 9,1 × V | 27 × F | 34,7 × F |
| 0,30 | 10,0 × V | 27,5 × F | 44,0 × F |
| 0,40 | 10,9 × V | 30,0 × F | 41,5 × F |
| 0,50 | 11,8 × V | 32,6 × F | 45,0 × F |
| 0,60 | 12,7 × V | 35,0 × F | 48,5 × F |
| 0,70 | 13,6 × V | 37,5 × F | 51,9 × F |
| 0,80 | 14,5 × V | 40,0 × F | 55,4 × F |
| 0,90 | 15,5 × V | 42,6 × F | 58,8 × F |
| 1,00 | 16,4 × V | 45,1 × F | 62,4 × F |
| ≥ 1,10 | 17,3 × V | 47,5 × F | 65,8 × F |

(A = wärmeübertragende Umfassungsfläche, V = beheiztes Bauwerksvolumen, F = beheizte Geschossfläche)

Abkühlungsflächen im Erdreich können mit Faktor 0,5 reduziert werden. Gemeinsame Wände mit anderen beheizten Gebäuden werden bei A nicht eingerechnet. Unbeheizte Keller und nicht ausgebaute Dachräume bleiben bei V unberücksichtigt.

Klimakorrekturfaktoren f (Beispiele, Tab. 4.5):
- Bonn, Köln, Essen, Lübeck: f = 1,00 (θe = −10 °C)
- Hamburg, Stuttgart, Bremen: f = 1,07 (θe = −12 °C)
- Berlin, Leipzig, Hannover: f = 1,13 (θe = −14 °C)
- Bamberg, Bayreuth, München: f = 1,20 (θe = −16 °C)
- Garmisch-Partenkirchen, Oberwiesenthal: f = 1,27 (θe = −18 °C)
- Oberstdorf: f = 1,33 (θe = −20 °C)

**Beispielrechnung 1** (eingeschossig, unterkellert, Flachdach, Berlin θe = −14 °C, f = 1,13):
- Gebäude 9 m × 17 m × 2,75 m
- Wandfläche: 2(9·2,75) + 2(17·2,75) = 143 m²
- Dachfläche: 153 m²; Bodenfläche: 153 m²
- A = 449 m²; V = 421 m³; A/V = 1,07 m⁻¹
- ΦHL = [23,4 + (24,7–23,4)·0,7] · 421 = 24,3 · 421 = 10.230 W
- Mit Klimafaktor: 10.230 · 1,13 = ca. 11.560 W ≈ 11,5 kW

**Beispielrechnung 2** (Gebäude mit beheiztem Dach- und Kellergeschoss, Düsseldorf θe = −10 °C, f = 1,00):
- Wandfläche gesamt: 553 m²; Bodenfläche (×0,5 wg. Erdreich): 75 m²; Dachfläche: 210 m²
- A = 838 m²; V = 2025 m³; A/V = 0,41 m⁻¹
- ΦHL = 15,7 · 2025 ≈ 32 kW
- Oberstdorf statt Düsseldorf: 32.000 · 1,33 ≈ 42 kW

---

### Kühllast (Abschnitt 4.1.2)

In Mitteleuropa nicht zwingend erforderlich, aber häufiger durch Komfortansprüche und innere Wärmelasten aus IT-Ausstattung. Hochgedämmte Gebäude mit großen Fensterflächen ohne Sonnenschutz sind überhitzungsgefährdet.

**Solarkonstante:** 1353 W/m² am äußeren Rand der Atmosphäre; an der Erdoberfläche max. ca. 1000 W/m². Strahlung teilt sich in direkte und diffuse Komponenten auf.

**Globalstrahlung für wolkenlosen Tag, Deutschland 50° Breite (Tab. 4.6 – mittlere und geringe Trübung):**

| Monat | TL (mittl.) | I_dir [W/m²] | I_dif [W/m²] | I_ges [W/m²] | TL (gering) | I_dir | I_dif | I_ges |
|---|---|---|---|---|---|---|---|---|
| Januar | 3,7 | 591 | 157 | 748 | 2,7 | 748 | 123 | 871 |
| Februar | 4,1 | 663 | 188 | 851 | 3,1 | 795 | 152 | 947 |
| März | 4,6 | 714 | 209 | 923 | 3,3 | 860 | 164 | 1024 |
| April | 5,1 | 725 | 216 | 941 | 3,5 | 883 | 164 | 1047 |
| Mai | 5,3 | 738 | 211 | 949 | 3,7 | 883 | 162 | 1045 |
| Juni | 6,1 | 682 | 223 | 905 | 4,3 | 830 | 176 | 1006 |
| Juli | 6,1 | 670 | 228 | 898 | 4,3 | 820 | 180 | 1000 |
| August | 5,9 | 649 | 233 | 882 | 4,1 | 810 | 183 | 993 |
| September | 5,4 | 629 | 228 | 857 | 3,9 | 779 | 183 | 962 |
| Oktober | 4,2 | 643 | 189 | 832 | 3,0 | 800 | 146 | 946 |
| November | 3,6 | 598 | 152 | 750 | 2,9 | 706 | 129 | 835 |
| Dezember | 3,5 | 538 | 137 | 675 | 2,7 | 671 | 113 | 784 |

**Kühllast-Komponenten:**
- Äußere Lasten: Transmission über Wände, Dächer, Fenster + Solarstrahlung durch Fenster + Infiltration warmer Außenluft
- Innere Lasten: Personen (latent + sensibel ΦP), Computer/Maschinen (ΦC), Beleuchtung (ΦB), Sonstige (ΦS)
- Gesamtkühllast: Φges = Φi + Φa

Äußere Lasten:
- Φw = U · A · θäq (Transmission opake Flächen, mit äquivalenter Temperatur)
- ΦT = Uw · Am · (θLR − θLO) (Fenster-Transmission)
- ΦS = AF · Imax · g (Solarstrahlung durch Fenster mit Gesamtenergiedurchlassgrad g = τE + qi)

**Gesamtenergiedurchlassgrad g = τE + qi** (direkter Anteil + Sekundärstrahlung). Tageslichtquotient T [%] beschreibt den sichtbaren Strahlungsanteil durch ein Fenster.

**Sonnenschutz-Abminderungsfaktoren Fc:**
- Ohne Sonnenschutz: Fc = 1,0
- Außenjalousie: Fc = 0,25
- Außenrollo / Markise: Fc = 0,4–0,5
- Rollo im Scheibenzwischenraum: Fc = 0,5
- Innenrollo / Innenjalousie: Fc = 0,7–0,9
- Klapp- und Schiebeladen: Fc = 0,3

Zielwert: Fc ≤ 0,5 anstreben.

**Tab. Sonnenschutz g-Gesamtwert (mit 2-fach Wärmeschutzverglasung g = 60 %):**

| Sonnenschutzvorrichtung | Farbe/Anordnung | g-Gesamtwert |
|---|---|---|
| Außenlamellenstore | Hell | 0,13–0,20 |
| Außenlamellenstore | Dunkel | 0,20–0,30 |
| Gitterstoffstore | Außen | 0,22–0,35 |
| Innenlamellenstore | Hell | 0,45–0,55 |
| Reflexionsgläser | – | 0,20–0,55 |

Außenliegender Sonnenschutz kann Einstrahlung um bis zu 80 % reduzieren.

**Tab. Glasparameter verschiedener Gläser (g: Energiedurchlassgrad, T: Tageslicht, U: Wärmedurchgang):**

| Bezeichnung | Typ | g [%] | T [%] | U [W/(m²·K)] |
|---|---|---|---|---|
| Planilux | Einfachglas 2 mm | 88 | 91 | 5,9 |
| Climalit | 2-fach Isolierglas | 76 | 81 | 2,7 |
| Climaplus ultimate | 2-fach | 53 | 75 | 0,8 |
| Climatop positiv | 3-fach | 60 | 77 | 0,4 |
| Climaplus xtreme 70/33 | 3-fach selektiv beschichtet | 31 | 64 | 0,5 |
| Planistar | 2-fach Argonfüllung | 38 | 71 | 1,0 |

**Wärmespeicherung:** Speicherwirksame Innenflächen dämpfen Temperaturanstieg erheblich. Faustformel: 2,5–3-fache wärmspeichernde Fläche je m² Fenster erlaubt passive Speicherung ohne Überhitzung (bei außenliegendem Sonnenschutz). Mit zunehmender Bauteildicke steigt Wärmekapazität (bis ca. 30–40 cm wirksam, danach abnehmend).

**Tab. Wärmekapazitäts-Kennwerte verschiedener Baustoffe (Dichte ρ, λ, c, b-Eindringgeschwindigkeit):**

| Baustoff | ρ [kg/m³] | λ [W/(mK)] | c [J/(mK)] | b [J/(m²Ks^½)] |
|---|---|---|---|---|
| Normalbeton | 2400 | 2,10 | 1000 | 2240 |
| Zementestrich | 2000 | 1,40 | 1000 | 1670 |
| Kalkputz | 1800 | 0,87 | 1000 | 1250 |
| Kalksandstein | 1400 | 0,70 | 1000 | 990 |
| Leichtbeton | 1400 | 0,62 | 1000 | 930 |
| Ziegel | 1400 | 0,58 | 1000 | 900 |
| Gipskartonplatten | 900 | 0,21 | 1000 | 850 |
| Leichthochlochziegel | 800 | 0,33 | 1000 | 510 |
| Holz | 600 | 0,13 | 2100 | 400 |
| Hohlblocksteine | 500 | 0,29 | 1000 | 380 |
| Gasbeton | 600 | 0,19 | 1000 | 340 |
| Kork | 300 | 0,05 | 1700 | 160 |
| PS-Hartschaum | 20 | 0,04 | 1500 | 35 |

**Konstruktionsvarianten Verwaltungsgebäude:**
- Variante A (außenliegender Sonnenschutz + Deckenabhängung): typische Ausführung
- Variante C (Doppelboden, Deckenabhängung, innenliegender Sonnenschutz): geringe Speichermasse, hoher Glasanteil, Überhitzungsneigung
- Variante D (hohe speichernde Innenflächen, geringer Glasanteil, außenliegender Sonnenschutz): günstigste Bedingungen gegen Überhitzung

**Erfahrungswerte Kühllast nach Nutzung (Tab. 4.10):**

| Nutzung | Nutzungstage [d] | Kühllast [W/m²] |
|---|---|---|
| Büro/Verwaltung | 250 | 10–40 |
| Einzelhandel | 300 | 10–100 |
| Restaurant | 300 | 20–150 |
| Dienstleistung | 250 | 0–80 |

---

### Wärmeerzeugungsanlagen — Übersicht (Abschnitt 4.2)

Wärmeträger in Gebäuden: überwiegend Wasser (seltener Luft); Dampf nur noch für Industrie. Primärenergieträger historisch Erdgas und Heizöl. Alternativen: Erdwärme + Wärmepumpe, Kraft-Wärme-Kopplung (KWK), Holz, saisonale Wärmespeicher mit Solarthermie.

**Energiestandards (Heizendenergie):**
- Bestandsgebäude unsaniert: bis über 200 kWh/(m²·a)
- GEG-Neubauten (Stand 2022): ca. 30–60 kWh/(m²·a)
- „3-Liter-Haus" (sehr guter Wärmeschutz): bis 30 kWh/(m²·a)
- Passivhaus: max. 15 kWh/(m²·a)

**U-Werte Niedrigstenergie- und Passivhäuser:**
- „3-Liter-Haus": opake Bauteile 0,18–0,22 W/(m²K), transparente Flächen < 1,2 W/(m²K); Heizlast ca. 25–40 W/m²
- Passivhaus: opake Bauteile ca. 0,10–0,16 W/(m²K), Fenster max. 0,67–0,8 W/(m²K); Heizlast ca. 10 W/m²

Unterscheidung: **Heizenergie** (inkl. Transport/Aufbereitungsverluste) → **Endenergie** (ab Hausanschluss) → **Primärenergie** (inkl. Stromerzeugungskette).

**Primärenergienutzungsgrad und CO₂-Emissionen (Tab. 4.11, Stand 2018):**

| Heizsystem | Primärenergienutzungsgrad [kWh/kWh] | CO₂ [kg/kWh] |
|---|---|---|
| Elektroheizung (Strommix) | 0,4 | 0,60–0,61 |
| Öl-/Gasheizung (Brennwert) | 0,80–0,85 | 0,20–0,30 |
| Elektrowärmepumpe | 1,4–1,8 | 0,18–0,23 |
| Gasmotor-Wärmepumpe | 1,5–1,8 | 0,15–0,20 |
| Holzpelletsheizung | 0,6–0,7 | 0,05–0,10 |
| BHKW | 1,5 | 0,05–(−0,3) |

**Heizungsmarkt Neubau 2020 (Tab. 4.18):**

| Energieträger/Heizsystem | Anteil |
|---|---|
| Erdgas (inkl. Biogas) | 33,2 % |
| Heizöl | 0,3 % |
| Wärmepumpen (Strom) | 35,5 % |
| Sonstige (Pellets u. a.) | 5,4 % |
| Fernwärme | 24,4 % |
| Stromheizung | 1,3 % |

Wärmepumpenanlage ist derzeit häufigste Wärmeerzeugungsanlage bei Neubauten.

**Wärmeerzeugungssysteme (Übersicht):**
- Warmwasserpumpenheizung (WWPH) mit Erdgas/Brennwert + solare Unterstützung
- Fern-/Nahwärmeanschluss (Vorlauftemperatur z. T. bis > 90 °C); geeignet für hohe VL-Temperaturen und Kälteerzeugung über Ab-/Adsorption
- Sole-/Wasser-Wärmepumpe mit Erdwärmesonden (monovalent): geringe Primärenergie, konstante Wärmequellentemperatur
- Luft-/Wasser-Wärmepumpe (Kaskaden): niedrige VL-Temperaturen erforderlich, ungünstige Außenlufttemperaturen im Winter
- KWK / BHKW: Auslegung auf min. 4000 h/a Laufzeit; Mikro-KWK ab 1 kW_el erhältlich; i. d. R. Backup-Wärmeerzeuger erforderlich
- Solarthermie mit Langzeitspeicher + Pelletskessel (Zusatzwärmequelle)
- Passivhaus: Restwärme über Abluftwärmepumpe, dezentrale Einzelheizung oder elektrische Widerstandsheizung zur Zuluft-Nacherwärmung

Regenerativer Stromanteil 2021: 40,9 % der Bruttostromerzeugung.

---

### Energieträger für Wärmeerzeuger (Abschnitt 4.2.2)

**Fossile Brennstoffe:** Hauptbestandteile Kohlenstoff C, Wasserstoff H, Schwefel S.
Verbrennungsprodukte:
- S + O₂ → SO₂ (Schwefeldioxid, unerwünscht)
- C + O₂ → CO₂ (Kohlendioxid, Atmosphärenerwärmung); bei unvollständiger Verbrennung: CO (giftig)
- 2H₂ + O₂ → 2H₂O (Wasserdampf)

**Heizöl EL** (extra leichtflüssig): ca. 21 % Wärmemarktanteil. Schwefelgehalt max. 50 mg/kg (schwefelarmes Heizöl). Bioheizöl EL A Bio: mind. 3 Vol.-% Bioöl.

**Biomasse:** Feste, flüssige und gasförmige Brennstoffe organischer Herkunft; gilt als CO₂-neutral (Aufnahme im Wachstum = Freisetzung bei Verbrennung). Verfahren:
- Thermo-chemisch: Verbrennung, Vergasung, Verflüssigung
- Biologisch: Biogas aus Dünger/Gülle

Biodiesel (aus Rapsöl-Methylester RME): biologisch voll abbaubar, in Dieselmotoren und Heizkesseln einsetzbar, beliebig mit konventionellem Diesel mischbar. Viskosität beachten. Bei Gebäudeheizanlagen i. d. R. keine Vorwärmung nötig.

**Brenngase für Gebäudeheizung:**
- 1. Gasfamilie: Kokereigas (Ferngas); H₂ + CH₄ + CO; Brennwert ca. 4,6–5,9 kWh/m³; heute wenig bedeutsam
- 2. Gasfamilie: Erdgas (H und L); Methangehalt > 80 %; Erdgas H (Brennwert ca. 10,5–13,1 kWh/m³), Erdgas L (ca. 8,4–10,5 kWh/m³); Preis an Rohölpreis gekoppelt
- Biogas: aus Faulgas, Klärgas, Deponiegas; Potenzial bis 30 % (2030)
- 3. Gasfamilie: Flüssiggas (Propan C₃H₈, Butan C₄H₁₀); komprimiert auf 1/260 Volumen bei ca. 25 bar; ca. 1,8-mal schwerer als Luft

**Wärmewerte von Gasen:**
- **Brennwert (Ho,n):** Wärmemenge bei vollständiger Verbrennung von 1 m³ trockenem Gas (Normzustand 0 °C, 1,013 bar) bei Rückkühlung auf 25 °C; schließt Kondensationswärme des Wasserdampfes ein
- **Heizwert (Hu,n):** Wie Brennwert, jedoch ohne Kondensationswärme des Wasserdampfes
- **Betriebsheizwert (Hu,B):** Heizwert unter Betriebsbedingungen (Druck und Temperatur an der Verbrauchsstelle); etwas niedriger als Hu,n
- **Wobbe-Index:** Kennwert für Gaustauschbarkeit; gleicher Wobbe-Index → Gaswechsel ohne Brenner-/Düsenänderung möglich

**Holz als Brennstoff:**
- Zusammensetzung: Wasser, Asche, flüchtige Bestandteile, Holzkohle
- Feuchte: Erntefrisches Waldholz 40–50 %, lufttrockenes Holz 15–20 %
- Unterer Heizwert (trocken): 16–23 MJ/kg je nach Holzart; bei 50 % Feuchte: Heizwert halbiert
- Heizwert-Bandbreite: 1400–2100 kWh/m³ (je nach Holzsorte, trocken)
- Formen: Stückholz, Hackgut/Hackschnitzel, Pellets, Briketts

**Steinkohle:** Anthrazit/Gasflammkohle, ab ca. 10 kW automatisierte Kessel; relativ hoher Schadstoffausstoß.
**Braunkohle:** Überwiegend brikettiert für Einzelöfen; hoher Schadstoffausstoß.
**Koks:** Entgastes Steinkohleprodukt; nur für größere Kessel mit automatischer Beschickung.
**Elektrischer Strom:** Nahezu 100 % in Nutzenergie umsetzbar; sinnvoll über Wärmepumpe oder (bei Regenerativstromanteil) Power-to-X und Stromdirektheizung.

---

### Gasversorgung und Gasinstallation (Abschnitt 4.2.3.1)

**Regelwerk:** DVGW-TRGI (Technische Regeln für Gasinstallationen), Landesbauordnungen, Feuerungsverordnungen (FeuVO) der Länder. TRGI gilt ab Hauptabsperreinrichtung an der Gebäudeeinführung bis zur Abgasausmündung ins Freie.

**Vorteile von Brenngasen:**
- Gute Regelbarkeit
- Keine Brennstofflagerung erforderlich
- Verbrauchserfassung über Gaszähler
- Geringere Schadstoff- und CO₂-Emissionen als andere fossile Träger

**Gasinstallation:** Nur durch GVU-eingetragene Vertragsinstallationsunternehmen; Beginn muss GVU rechtzeitig gemeldet werden.

**Hausanschluss:**
- Hausanschlussleitung möglichst geradlinig, rechtwinklig auf das Gebäude
- Tiefbauarbeiten können vom Anschlussnehmer beauftragt werden (nach DIN 4124)
- Überdeckung: i. d. R. 0,60–1,00 m; Abweichungen: max. 5,00 m Tiefe / 2,00 m Überdeckung
- Sandbett: mind. 10 cm dick, allseitige Einbettung in Sand
- ca. 30 cm oberhalb der Gasleitung: gelbes Kunststoff-Trassenwarnband (Flatterband) einlegen
- Bei PE-HD-Rohren: zweites Warnband ca. 10 cm unter Oberflächenbefestigung
- Keine Überbauung zulässig, sofern Zugänglichkeit beeinträchtigt (Ausnahme: Pflasterungen, Gehwegplatten)
- Unter nicht unterkellerten Gebäudeteilen: Gasleitung in Mantelrohr verlegen
- Hausanschluss endet mit Hauptabsperrvorrichtung unmittelbar hinter Gebäudeeinführung
- Gebäudeeinführung elastisch mit Mantelrohr (lichter Durchmesser ca. 2 cm größer als Gasrohr), dauerelastisch verschlossen
- Erdverlegte Leitungen einmessen und in Bestandspläne eintragen (gem. TRGI)

**Gaszähler:**
- Aufstellungsort: trocken, nicht überhitzt, mechanisch geschützt, leicht erreichbar; Frostfreiheit nicht gefordert
- Bevorzugt im Hausanschlussraum; in Geschossen: belüftete Zählerschränke in Nischen, Mindest-Nischentiefe 14 cm
- Zählerwechsel alle 12 Jahre
- Unzulässige Aufstellorte:
  - Treppenräume notwendiger Treppen (Ausnahme: Wohngebäude geringer Höhe max. 2 Wohnungen)
  - Allgemein zugängliche Flure (wenn Hindernis)
  - Bereiche mit brandfördernden oder leicht entzündlichen Stoffen (Flammpunkt bis 55 °C)
  - Bereiche mit explosiven Gasen, Dämpfen, Nebeln, Stäuben
  - Bereiche mit explosionsgefährlichen Stoffen

**Gasleitungen innerhalb von Gebäuden:**
- Rohrmaterial: verzinktes Stahlrohr oder Kupferrohr; in seltenen Fällen Präzisionsstahlrohr
- Kellerräume: frei vor der Wand mit Abstandsschellen
- Übrige Räume: unter Putz in Wandschlitzen (ca. 6×6 cm, ausgemörtelt oder ausgeschäumt)
- Kupferrohre möglichst nicht unter Putz (Beschädigungsrisiko durch Nägel/Bohrgeräte)
- **Verboten:** Verlegung in Estrichen (schwimmend oder Verbund)
- Zulässig: unter schwimmendem Estrich in Dämmstoffschicht, wenn Rohr nicht belastet und Stahlrohre Korrosionsschutz erhalten
- Hohlräume mit Gasleitungen: mind. 1 Belüftungs- und 1 Entlüftungsöffnung je 10 cm² (wegen Odorierung frühzeitige Leckageerkennung)
- Alternativ: Hohlräume formbeständig und dicht mit geeigneten Baustoffen verfüllen; oder Gasleitungen in korrosionsbeständigen Mantelrohren verlegen
- Abgehängte Decken: Hohlraum belüften (Rundumschlitze an Umfassungswänden oder diagonal max. 5 m auseinander liegende Lüftungsöffnungen)
- **Verboten:** Führung durch Aufzugsschächte, Lüftungsleitungen, Kohlenschütten, Müllabwurf, Schornsteinwangen

**In Rettungswegen (Flure, Treppenräume notwendiger Treppen) gem. MLAR + TRGI zulässige Verlegung:**
- Frei verlegt
- Unter Putz hohlraumfrei mit mind. 15 mm Putzüberdeckung auf nicht brennbarem Putzträger
- In eigenem längsgelüftetem Installationskanal/-schacht (ohne Lüftungsverbund mit Flur) oder formbeständig dicht verfüllt
- Kanal/Schacht aus nichtbrennbaren Baustoffen, Feuerwiderstandsklasse I 90

**Korrosionsschutz:** Alle Stahlleitungen außer frei liegenden in trockenen Räumen erhalten Korrosionsschutzanstrich. Mantelrohre bei Decken-/Wanddurchführungen (Überstand ca. 5 cm über Decke). Stahlleitungen in Beton/Gips sowie Kupferleitungen in nitrit-/ammoniumhaltigen Baustoffen: Mantelrohr.

**Druckprüfung:**
- Vorprüfung (ohne druckempfindliche Armaturen): Prüfdruck 1 bar (ca. 50-facher Betriebsdruck)
- Hauptprüfung (mit Armaturen, ohne Gasgeräte): Prüfdruck 110 mbar; Druck darf 10 min nicht abfallen; Lecksuche mit schaumbildendem Spray
- Freiliegende Gasleitungen können gelb markiert werden (Unterscheidung von anderen Leitungen)
- Gasleitungen dürfen nicht als Erder von Elektroanlagen oder Blitzableitern dienen; Anschluss an Potentialausgleichsschiene erforderlich

---

### Gasgeräte und Gasfeuerstätten

**Gasgerät-Klassifikation nach TRGI:**
- **Art A:** Gasgeräte ohne Abgasanlage (z. B. Gasherde, Einbaubacköfen, Laborbrenner); Verbrennungsluft aus Aufstellraum; Aufstellraum mind. 20 m³ (in manchen Bundesländern 15 m³) und zu öffnendes Fenster oder Außentür
- **Art B:** Raumluftabhängige Gasfeuerstätten; offene Verbrennungskammer; Anschluss an Abgasanlage erforderlich; Verbrennungsluft über Außenfugen, Öffnungen ins Freie oder Lüftungsverbund
- **Art C:** Raumluftunabhängige Gasfeuerstätten; geschlossene Verbrennungskammer; Verbrennungsluft über geschlossenes System von außen

Ergänzungsindizes bezeichnen konstruktive Gruppe (Index 1) und Einbauort (Index 2).

**Alle Gasgeräte müssen:** DVGW-Prüfzeichen und CE-Kennzeichnung tragen.

**Gas-Wasserheizer (Thermen):**
- Gas-Durchlaufwasserheizer: Warmwasserbereitung für Küche/Bad; max. Rohrleitungslänge für Spülen/WB ca. 5 m, für Bad/Dusche ca. 10 m; Durchsatzmenge ca. 2–8 l/min bei 60 °C
- Gas-Umlaufwasserheizer: Wärmeerzeuger für Warmwasserheizung; kein eigener Aufstellraum erforderlich; Wandmontage bevorzugt im Bad/Flur; Abmessungen ca. 50/38/85 cm; Leistungsbereich ca. 5–40 kW; bei 5 kW Heizung bis ca. 120 m² beheizter Fläche bei 40 W/m²
- Gas-Kombiwasserheizer: Heizung + Warmwasserbereitung kombiniert; Warmwasserbereitung ca. 18–24 kW; modulierende Brennerregelung
- Gas-Vorratswasserheizer: Warmwasservorrat ca. 120–380 l; geeignet für schwach dimensionierte Gasrohrnetze

**Gas-Raumheizer:** Wärmeabgabe direkt an Aufstellraum; überwiegend als Außenwandgeräte; kaum noch in Gebrauch.

**Gas-Etagenkessel:** Abmessungen entsprechen Küchenmöbel-Unterschränken (Höhe 90 cm, Tiefe 60 cm); erfordern Abgasanlage, Zuluftöffnungen und Elektroanschluss.

**Brenner-Typen:**
- Atmosphärische Brenner: ohne Gebläse, bei normalem Luftdruck; überwiegend in Kesseln < 50 kW
- Gasgebläsebrenner: mit Ventilator; für höhere Leistungsbereiche (Mehrfamilienhäuser, Gewerbe)

**Strömungssicherungen:** In allen Gasfeuerstätten mit atmosphärischem Brenner eingebaut; nehmen Einfluss auf Auftrieb, Stau und Rückstrom in der Abgasanlage; wirken auch als Nebenluftvorrichtung; verhindern CO-Bildung bei Rückstrom.

**Abgasklappe (Diermayerklappe):** Schließt bei Betriebsruhe; verhindert Wärmeverluste durch entweichende Raumluft; darf nicht absolut dicht schließen (Abtrocknung von Kondensat aus Strömungssicherung).

---

### Abgasanlagen für Gasgeräte

**Begriffe:**
- Schornstein: Rußbrandbeständig (1000 °C); für Festbrennstoff-Feuerstätten geeignet
- Abgasleitung: Alle übrigen Abgasanlagen; bauaufsichtlich genehmigungsfrei

Geeignete Abgasanlagen für Gasfeuerstätten:
- Feuchtigkeitsunempfindliche Schornsteine (für NT-Kessel und Standard)
- Feuchtigkeitsunempfindliche Abgasleitungen in feuerbeständigem/-hemmendem Schacht (besonders für Brennwertgeräte)
- Freistehende doppelwandige gedämmte Edelstahlschornsteine (Nachrüstungen)
- Luft-Abgas-Systeme (LAS) für raumluftunabhängigen Betrieb
- Koaxiale Abgasstutzen (LAS) im Dachbereich
- Dreischalige feuchtigkeitsempfindliche Schornsteine (nur im Bestand, mit Einschränkungen)
- Ableitung über Außenwand (Genehmigungsvorbehalt)

**Kombinationsregeln:**
- NT-Kessel/-Thermen: feuchtigkeitsunempfindliche Abgasanlagen
- Brennwertkessel/-Thermen: druckdichte und feuchtigkeitsunempfindliche Abgasanlagen
- Standardheizkessel: nicht mehr zugelassen

**Mehrfachanschluss:** Bis zu 4 Geräte gleicher Art an gemeinsame Abgasanlage (gem. DVGW G 637/I); Anschlüsse gegeneinander versetzen; max. Abstand zwischen unterstem und oberstem Anschluss 6,50 m; oberhalb des 5. Vollgeschosses keine raumluftabhängigen Geräte an gemeinsame Abgasanlage.

---

### Außenwandfeuerstätten

**Max. Nennwärmeleistungen:** Beheizung 7 oder 11 kW (je nach Geräteart); Warmwasserbereitung 28 kW.
Außenwandfeuerstätten sind vorrangig für Altbaumodernisierungen; im Neubau nur wenn Abgasführung unverhältnismäßig aufwändig wäre.

**Verbotene Mündungslagen (gem. TRGI):**
- Durchgänge und Durchfahrten
- Enge Traufgassen
- Lichtschächte und Luftschächte
- Loggien und Laubengänge
- Balkone (außer Raumheizer)
- Unter auskragenden Bauteilen
- Schutzzonen für brennbare/explosionsfähige Stoffe
- Ecklagen von Innenhöfen (außer ventilatorbetriebene Geräte C12/C13)
- Innenhöfe, wenn Gebäudehöhe die Hofbreite/-länge übertrifft

**Mindestabstände Außenwand-Mündungen:**
- Mind. 30 cm über Geländeoberkante
- Ventilatorbetriebene Geräte: Abgasöffnungen an begehbaren Flächen nicht unter 2 m; bis 2 m über Gelände Schutzgitter erforderlich
- Zu Lüftungsöffnungen für Raumlüftung: seitlicher Abstand ≥ 2,50 m; senkrecht nach oben ≥ 5,00 m
- Abstand Abgasöffnungen zu brennbaren Gebäudeteilen: 1,00 m gegenüberliegend; 0,50 m zur Seite und nach unten; 1,50 m nach oben (0,50 m wenn hinterlüftete nichtbrennbare Schutzschicht vorhanden)
- Für gebläseunterstützte Geräte (C32/C33) über Dach: 40 cm Dachabstand bei ≤ 50 kW; ab 50 kW: mind. 1,00 m Dachabstand oder First um 40 cm überragen
- Fenstermindestabstände ventilatorbetriebener Geräte (abhängig von Vorsprüngen etc.): bei d ≤ 25 cm → a mit 0,50 m; bei d ≥ 25 cm → b mit 1,00 m

---

### Verbrennungsluftversorgung für raumluftabhängige Gasfeuerstätten

**Bis 35 kW:**
- Aufstellraum mind. 4 m³/1 kW Gesamtwärmeleistung + zu öffnendes Fenster → Außenfugen reichen als Verbrennungsluftzufuhr
- Hygienischer Mindeststundenluftwechsel n = 0,5; Verbrennungsluftbedarf 1,6 m³/kW → rechnerischer Mindest-Rauminhalt 3,2 m³/kW (+ Reserven: Aufstellraum 4 m³/kW)
- Fensterlose Räume sind nicht anrechenbar

**Unmittelbarer Lüftungsverbund:** Aufstellraum mit direkt benachbarten Räumen verbunden; Durchlassöffnungen 150 cm² (in Türblatt oder über Türsturz, damit nicht zugestellt); Gesamtraumvolumen mind. 4 m³/kW

**Mittelbarer Lüftungsverbund:** Über Verbundräume bis zum erforderlichen Gesamtvolumen; Öffnungen ≥ 150 cm²; Aufstellraum mit Außenöffnung mind. 2 m³/kW

Wenn Aufstellraum-Volumen < 1 m³/kW: zwei Öffnungen von je 150 cm² zu Nebenraum, untere in Bodennähe, obere mind. 1,80 m über OK Fußboden.

Zuluftschacht (für zweigeschossige Gebäude beispielhaft): 300 cm² erforderlich vs. 140 cm² für Abluftschacht (wegen Reibungsverlusten)

**Außenwand-Durchlasselemente:** für Räume mit besonders dichten Fenstern (Schallschutz); Auslegung auf 0,8 m³/kW·h Luftvolumenstrom.

**35 bis 50 kW:**
- Öffnung ins Freie mind. 150 cm² freier Querschnitt; verschließbar wenn Verriegelung mit Brenner
- Bei Aufstellraum-Volumen < 1 m³/kW: 2 Öffnungen je 75 cm² ins Freie höhenversetzt (obere ≥ 1,80 m, untere in Fußbodenhöhe)
- Luftkanäle ins Freie nach TRGI Diagramm bemessen (Beispiel: 10 m gerade Leitung nach 150 cm² → 300 cm² Querschnitt)

**Verbrennungsluftbedarf:** 1,6 m³/kW gilt auch für flüssige und feste Brennstoffe. Kachelöfen: 1 kW je m² Oberfläche; offene Kamine: 340 kW je m² Feuerraumöffnung.

---

### Aufstellräume für Gasfeuerstätten

**Bis 50 kW – unzulässige Aufstellorte:**
- Treppenräume (Ausnahme: Wohngebäude geringer Höhe ≤ 7 m Fußbodenhöhe über Gelände, max. 2 Wohnungen)
- Allgemein zugängliche Flure als Rettungswege
- Räume mit leicht entzündlichen Stoffen in gefährlicher Menge
- Räume mit explosionsfähigen Stoffen (Ausnahme: Art-C-Geräte in Garagen)

**In Neubauten unzulässig:** Raumluftabhängige Art-B-Feuerstätten in Räumen mit Lüftungsanlagen, die Konkurrenz zwischen Entlüftung und Abgasableitung erzeugen können (innen liegende Bäder, WCs, Küchen mit Dunstabzug). Auch nicht in Räumen mit offenem Kamin ohne eigene Verbrennungsluftversorgung.

**Verriegelungseinrichtung:** Raumluftunabhängige Art-C-Geräte in schachtentlüfteten Räumen zulässig, wenn Verriegelung den Brenner bei Ventilator-Lüftungsbetrieb abschaltet. Kann entfallen, wenn Unterdruck im Aufstellraum max. 4 Pa.

**Über 50 kW:** Gasbefeuerte Heizkessel nicht mehr an besonderen Heizraum gebunden (gem. MFeuVO); Anforderungen an Aufstellraum nach Abschnitt 4.6.

**Abstände zu brennbaren Bauteilen:**
- An Oberflächen brennbarer Bauteile/Einbaumöbel darf nicht mehr als 85 °C auftreten
- Fehlen Herstellerangaben: mind. 40 cm Abstand (obwohl moderne Geräte 85 °C nicht erreichen)
- Abgasleitungen außerhalb von Schächten: mind. 20 cm Abstand zu brennbaren Bauteilen
- 5 cm ausreichend bei: ≥ 2 cm Ummantelung mit nichtbrennbaren Dämmstoffen ODER max. Abgastemperatur 160 °C
- Abgasleitungen durch brennbare Bauteile: mind. 20 cm Schutzrohr oder 20 cm Ummantelung mit nichtbrennbaren Baustoffen (5 cm wenn Strömungssicherung vorhanden UND max. 160 °C Abgastemperatur)
- Abgasrohre nicht durch andere Wohnungen, Treppenräume (Ausnahme kleine Wohngebäude), allg. zugängliche Flure, Räume mit entzündlichen/explosionsfähigen Stoffen

---

### Flüssiggas

**Eigenschaften:** Propan/Butan-Gemisch; ca. 1,8-mal schwerer als Luft; ungiftig; kondensiert ab ca. 25 bar; bei Atmosphärendruck gasförmig. Technische Regeln: TRF (Technische Regeln Flüssiggas).

**Druckflaschen:** 3–46 kg Inhalt (ca. 6–90 l); Aufstellraum-Fußboden darf nicht allseitig tiefer liegen als Geländeoberfläche; Außentüren nach außen schlagend ins Freie.

**Ortsfeste Großbehälter:**
- Ab 700 kg Füllgewicht (ca. 1775 l); oberirdisch oder unterirdisch
- Verkauf nach Gewicht: 1 kg ≈ 1,8–2 l Flüssigkeit ≈ 400–550 l Gas
- 1000 l Heizöl EL ≡ ca. 750 kg Flüssiggas (Heizwertäquivalent)
- Fundament unterirdischer Behälter: mind. 50 cm Erdüberdeckung
- Fundament oberirdischer Behälter: Betonplatte mind. 20 cm (C12/15, Baustahlgewebeeinlage) auf 25 cm Kies-/Schotterbett
- Anfahrschutz an Verkehrsflächen

**Explosionsgefährdete Bereiche:**
- Bereich A (ständig gefährdet): direkte Behälterumgebung
- Bereich B (temporär, beim Befüllvorgang gefährdet): größerer Bereich; keine unabschaltbaren Zündquellen, keine Kanalisationseinläufe ohne Geruchsverschluss

**Rohrleitungen:** Kupfer oder korrosionsgeschützter Stahl mind. 60 cm Tiefe; PE-HD im Erdreich zulässig; metallische Rohre mind. 10 cm allseitig in Sand; Kunststoffrohre: 15 cm Sand-Unterlage, 30 cm Sandüberdeckung; Abstand zu anderen Leitungen/Kabeln mind. 80 cm. Tankfahrzeuge (≥ 16 t) müssen bis ca. 25 m (Schlauchlänge) heranfahren können.

---

### Heizöl- und Biodiesel-Lagerung (Abschnitt 4.2.3.2)

Heizöl ist wassergefährdend; Lagerung genehmigungspflichtig. Biodiesel: Flammpunkt > 100 °C (kein Gefahrgut), Lagerung analog Heizöl.

**Jahresbedarf Berechnung:**
B = ΦHL · bvH / HU

Heizwert Heizöl EL = 10,0 kWh/l.

**Tab. Vollbenutzungsstunden für Überschlagsrechnung (bvH):**

| Gebäudeart | bvH [h/a] |
|---|---|
| Einfamilienhaus | 1500–2100 |
| Mehrfamilienhaus | 1800–2100 |
| Bürogebäude | 1500–1900 |
| Krankenhaus | 1900–2500 |
| Schule (einschichtiger Betrieb) | 1200–1400 |
| Schule (mehrschichtiger Betrieb) | 1300–1500 |

**Beispielrechnung** (Gebäude 32 kW Heizlast): B = 32 · 1800–2100 / 10,0 = 5760–6270 l/a; bei zentraler WW-Bereitung +10–20 %.

**Empfohlene Lagermenge nach Kesselleistung (AMEV):**
- Bis 0,1 MW: bis 1,0-facher Jahresbedarf
- 0,1–1,0 MW: ca. 0,7–0,5-facher Jahresbedarf
- Über 1,0 MW: ca. 0,5–0,15-facher Jahresbedarf

**Pellets-Lagerraum:**
- 1 kW Heizlast = 0,9 m³ Lagerraum (inkl. Leerraum)
- Mindestgrundfläche 2 m × 3 m
- Solides Lager: 1,2–1,3-facher Jahresbrennstoffbedarf (nutzbares Volumen = 2/3 Lagerraumvolumen)

**Erster Nutzungszyklus Massivbau:** Im 1. Jahr ca. 25 % Mehrverbrauch wegen Feuchtigkeitsüberschuss; Normal-Feuchtigkeitswerte ab 3.–4. Heizperiode.

**Behältertypen:**

- **Stahltank:** Korrosionsrisiko vor allem innen an der Behältersohle (Lochfraß durch Kondenswasser + Chloride + Schwefelverbindungen). Korrosionsschutzmittel (Inhibitoren) nur bedingt wirksam.
- **Kunststoffbehälter (PE, PA/Nylon, GFK):** Korrosionsbeständig; leicht transportierbar; bei PA/PE oft transparent → Füllstandsanzeige von außen möglich
- PA-Behälter: diffusions- und aromatendicht → kein Ölgeruch im Keller
- GFK-Behälter: gasdicht; benötigen keinen Auffangraum

**Tab. Batteriebehälter aus Stahl (DIN 6625 – Abmessungen):**

| Fassungsvermögen | Breite | Höhe | Länge |
|---|---|---|---|
| 1000 l | 0,72 m | 1,50 m | 1,10 m |
| 1500 l | 0,72 m | 1,50 m | 1,65 m |
| 2000 l | 0,72 m | 1,50 m | 2,15 m |

**Tab. Mindestabstände Batteriebehälter:**

| Behälter aus | Abstand Wand | Abstand Fußboden | Abstand untereinander | Auffangwanne |
|---|---|---|---|---|
| Stahl | 2×40 cm + 2×25 cm | 5 cm | 4 cm | erforderlich |
| PA/PE | 2×40 cm (2×5 cm) | – | – | erforderlich |
| GFK | 2×40 cm + 2×5 cm | – | 5 cm | nicht erforderlich |

**Oberirdische Lagerung in Gebäuden:**
- Bis 5000 l im Heizraum/Aufstellungsraum; Mindestabstand Behälter zur Feuerungsanlage: 1,0 m
- Bis 100.000 l in separatem Heizöllagerraum (feuerbeständige Wände/Decken, feuerhemmende Innentüren/Klappen, Belüftung, Beschäumung durch Feuerwehr vom Freien möglich)
- Batteriebehälter bis 2000 l durch normale Türöffnungen transportierbar; max. 5 Behälter je Gruppe
- PA/PE-Batteries: Gesamtlagermenge innerhalb einer Auffangwanne max. 10.000 l

**Standortgefertigte Behälter (Kastentanks, DIN 6625):** Bis 100 m³; aus vorgefertigten, vor Ort verschweißten Wandungen; bevorzugtes Rastermaß 25 cm.

Mindestabstände standortgefertigter Behälter:
- 40 cm an Zugangsseite und einer angrenzenden Seite
- 25 cm an übrigen Seiten
- 25 cm zur Decke; 10 cm zum Boden
- 50 cm zwischen Einsteigöffnung und Decke/Wand (bei mind. 60 cm Durchmesser); sonst 60 cm
- Ab 10.000 l: allseitig 40 cm

**Unterirdische Lagerung:**
- Doppelwandige zylindrische Stahltanks mit Kontrollwarngerät für Leckagen
- GFK-Behälter i. d. R. ohne Kontroll-Warneinrichtung zugelassen; alle 5 Jahre Dichtheits-Prüfung
- In Wasserschutzgebieten: stets doppelwandig mit Leckanzeige; alle 2 Jahre Prüfung durch Sachverständigen

**Tab. Zylindrische doppelwandige Heizölbehälter Stahl für Erdlagerung (DIN EN 12285-1, Auszug):**

| Inhalt [m³] | 1 | 3 | 5 | 7 | 10 | 16 | 20 | 25 | 30 | 40 | 50 | 60 | 80 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Länge [m] | 1,51 | 2,74 | 2,82 | 3,74 | 5,35 | 8,57 | 6,96 | 8,54 | 10,12 | 8,80 | 10,80 | 12,60 | 12,75 | 15,95 |
| Durchmesser [m] | 1,0 | 1,25 | – | – | 1,60 | – | 2,00 | – | – | 2,50 | – | – | 2,90 | – |
| Gewicht [kg] | 400 | 830 | 1100 | 1400 | 1900 | 2820 | 3420 | 4110 | 4930 | 6470 | 7800 | 9280 | 13.100 | 16.000 |

**Einbau Erdtanks:**
- Allseitige Überdeckung mit steinfreiem Material (Sand) mind. 20 cm
- Zylindrische Behälter: 1 % Sohlengefälle zum Domende
- Überdeckungstiefe: mind. 30 cm, max. 100 cm; unter Fahrbahnen ohne statischen Nachweis mind. 1,00 m
- Behälterabstand untereinander ≥ 40 cm; zu Grundstücksgrenzen/öffentlichen Versorgungsleitungen ≥ 100 cm
- Bei Auftriebsgefahr (Grundwasser/Überschwemmung): Behälter mit 1,3-facher Sicherheit belasten oder verankern
- Leitungsführung ab Behälter: Entnahme- und Rücklaufleitung; Stockpunkt bei paraffinbasischen Rohölen ca. 8 °C → Wärmedämmung oder Begleitheizung vorsehen
- Füllstutzen max. 30 m von Fahrwegen entfernt (Schlauchlänge); Entlüftungsleitungen mind. 50 cm über Füllstutzen und über Erdgleiche
- Grenzwertgeber (Befüllungsfühler) am Behälterscheitel

---

### Wärmeerzeuger mit Gas oder Heizöl (Abschnitt 4.2.3.3)

**Genehmigungslage ab 2026:** Konventionelle Kessel (Heizöl) nur noch als Hybridsysteme (GEG) mit regenerativer Energie. Neue Heizöl-Kessel ab 2026 nur noch als Verbrennungsmotor-Wärmepumpe oder BHKW.

**Möglichkeiten bei Erdgas:**
- Heizkessel Niedertemperaturtechnik
- Heizkessel Brennwerttechnik
- Gasmotorwärmepumpen
- Gasabsorptionswärmepumpen
- Gasadsorptionswärmepumpen
- Blockheizkraftwerke (Mikro-, Mini-, größere BHKWs)
- Brennstoffzellen

**Tab. BHKW-Klassifikation (Tab. 4.20):**

| Bezeichnung | Leistungsbereich [kW_el] | Anwendung |
|---|---|---|
| Nano-BHKW | 1,0–2,5 | Ein- und Zweifamilienhäuser |
| Mikro-BHKW | 2,5–20 | Mehrfamilienhäuser, Gewerbeimmobilien, Verwaltungsgebäude |
| Mini-BHKW | 20–50 | Größere Wohnimmobilien, Objektgebäude, Nahwärmenetze |
| Klein-BHKW | > 50 | Größere Gebäude, Nah-/Fernwärmenetze |
| Groß-BHKW | > 2000 | Quartier- oder Fernwärmeversorgung |

**Heizkessel (Guss oder Stahl):**
- Gusskessel: höhere Korrosionsbeständigkeit, dauerhafter; durch Glieder anpassbar in der Leistung
- Stahlkessel: für höhere Leistungen
- Naturzugkessel: auf Schornsteinzug angewiesen
- Hochleistungskessel (Überdruckkessel): Brennergebläse überwindet Kesselwiderstand; kleinere Bauform, höherer Wirkungsgrad; lauterer Betrieb
- Lieferung bis ca. 50–70 kW als anschlussfertige Units (inkl. Brenner, Armaturen, Verdrahtung)
- Wirkungsgrad NT-Kessel: ca. 89–94 %

**Abgasverluste (gem. 1. BImSchV – jährlich kontrolliert):**
- 4–25 kW: max. 11 % Abgasverlust
- 25–50 kW: max. 10 %
- Über 50 kW: max. 9 %
- Neue Kessel: selten > 7–9 % (bezogen auf Heizwert); gilt für Öl- und Gasheizungen
- Brennwertgeräte: keine Abgasverlust-Kontrolle (Bauart garantiert Grenzwerteinhaltung)

**Auskühlverluste moderner Kessel:** 1–2 %

**Gleitende Vorlauftemperatur:** Anpassung der Heizmitteltemperatur durch motorisch betriebene 3- oder 4-Wege-Mischer; witterungsgeführte Regelung.

---

### Niedertemperaturkessel (NT-Kessel)

Kontinuierlicher Betrieb mit Rücklauftemperaturen von 35–40 °C ohne Korrosionsschäden. Sockeltemperatur ständig ca. 35–40 °C. Max. VL-Temperatur ca. 55–75 °C. Früherer Standardheizkessel: bis 90 °C VL.

Taupunktgrenzen brennstoffabhängig:
- Erdgas: ca. 55 °C
- Heizöl: ca. 45 °C

Brennkammerwand durch Konstruktion (Rippung, mehrschichtig) vor Taupunkt-Kondensation geschützt. Zweistufige oder modulierende Brenner zur Leistungsanpassung; höchste Stufe nur an wenigen Wintertagen; geringere Brenner-Einschaltfrequenz → Energieeinsparung.

NT-Feuerstätten benötigen kondensatgeeignete Abgasanlagen.

---

### Brennwertkessel (Kondensationsheizkessel)

Latentwärme des Wasserdampfes im Abgas wird durch Kondensation zurückgewonnen.

**Physikalischer Hintergrund:**
- 1 kg Wasser verdampfen: 0,63 kWh erforderlich; Kondensation setzt gleiche Menge frei
- Brennwert liegt bei Erdgas ca. 11 % und Heizöl EL ca. 6 % höher als Heizwert (HU)
- Wirkungsgrade > 100 % bezogen auf HU erreichbar

**Funktionsprinzip:** Abgase werden in nachgeschalteten Edelstahl-Wärmetauschern durch Rücklaufwasser auf unter Taupunkt abgekühlt → Kondensatbildung + Latentwärmefreisetzung.

Taupunkt (Kondensation ab ca. 45–57 °C, abhängig von CO₂-Gehalt im Abgas):
- Hoher CO₂-Anteil im Abgas → höhere Taupunkttemperatur → günstiger für Kondensationsbetrieb
- Theoretisch erreichbarer CO₂-Wert bei Erdgas: 12 Vol.-%

**Energiegewinn:** ca. 7 % sensibler Wärme + ca. 11 % Latentwärme (Gasfeuerstätten) bzw. 6 % (Öl) vom Rücklauf nutzbar.

**Systemtemperaturen für Brennwertbetrieb:**
- Bei 70/50 °C Systemauslegung: ganzjährig Brennwertbetrieb möglich
- Bei 90/70 °C Systemauslegung: ca. 80 % der Jahresheizarbeit im Brennwertbetrieb (hauptsächlich Übergangszeit)
- Fußbodenheizung 40/30 °C: ideale Voraussetzung, ganzjährig Kondensationsbetrieb

Praktischer Wirkungsgradgewinn von Brennwert ggü. NT-Kessel (Gas): bis zu 10–11 %.

**Heizöl:** Schwefelgehalt macht Brennwert problematischer (Korrosion, Kondensat saurer); Taupunkt liegt tiefer → weniger Kondensationsbetrieb. Für schwefelarmes Heizöl: Normnutzungsgrad bis 104 % bezogen auf HU (bei 30 °C Rücklauf).

**Abgasanlage für Brennwertkessel:**
- Kein thermischer Auftrieb → Gebläse erforderlich
- Normale Hausschornsteine (mineralisch) nach alter DIN 18160 nicht zugelassen (statischer Druck im Schornstein muss kleiner als in Umgebungsräumen sein)
- Erforderlich: gasdichte, kondensatbeständige Innenrohre (Edelstahl, Glas, Schamotte, Kunststoff)
- Aufstellung bevorzugt im Dachraum/oberstem Geschoss (kurzer Abgasweg)
- Kondensatableitung zur Schmutzwasserfallleitung erforderlich

**Kondensatanfall:** Theoretisch max. 0,14 l/kWh bei Erdgasfeuerung; ca. 1,4 l/h bei 10 kW. Saures Kondensat muss zur Kanalisation abgeführt werden.

**Neutralisation nach DWA-A 251 (drei Gruppen):**
- Gasbetriebene Anlagen bis 25 kW in Wohngebäuden: keine Neutralisation (häusliches Abwasser reicht zur Verdünnung; Sicherheitsfaktor 100); gleich für Büros ab 10 Beschäftigten
- 25 bis 200 kW: abhängig von Kondensatmenge/Abwassermenge → Grenzwerte gem. Tab. 4.19

**Tab. Mindestzahl Wohnungen/Beschäftigte ohne Neutralisationsanlage (Kesselleistung 25–200 kW):**

| Kesselleistung [kW] | 25 | 50 | 100 | 150 | 200 |
|---|---|---|---|---|---|
| Wohnungen | ≥ 1 | ≥ 2 | ≥ 4 | ≥ 6 | ≥ 8 |
| Beschäftigte | ≥ 10 | ≥ 20 | ≥ 40 | ≥ 60 | ≥ 80 |

- Über 200 kW: Neutralisationsanlage obligatorisch
- Ölbetriebene Anlagen bis 200 kW (schwefelarmes Heizöl DIN 51603-1): keine Neutralisationsanlage; mit normalem Heizöl EL: grundsätzlich Neutralisationsanlage
- Neutralisation auch bei Ableitung in Kleinkläranlagen (DIN 4261) und bei bestimmten alten Gussleitungen (LNA-, GA-, SML-Gussrohr) obligatorisch
- Neutralisationsbehälter: relativ kleiner Durchflussbehälter mit kalkhaltigem Granulat

**Allgemeine Ausführungshinweise:**
- Wandgeräte (Wandheizkessel/Kesselthermen) überwiegend im Wohnungsbau
- Standgeräte ab ca. 8 kW; obere Leistungsgrenze ca. 600–700 kW
- Einbau bei Keller-Installation: Rückstauebene beachten; Pumpenförderung für Kondensat vorsehen (kondensatgeeignete Pumpen)

**Tab. Abgasanlagen-Übersicht (Tab. 4.21) – Feuerstätte und Abgasanlage müssen aufeinander abgestimmt sein:**

| Abgasanlage | Feuerstätten | Brennstoffe | Abgastemperatur | Druck | Kondensatverhalten |
|---|---|---|---|---|---|
| Dreischalige gedämmte Schornsteine | Kachelofen, Kaminofen, offener Kamin, NT-Kessel, Brennwertkessel | Öl, Gas, feste Brennstoffe (rußbrandbeständig) | Bis ca. 400 °C | Unterdruck | Feuchtigkeitsempfindlich |
| Feuchtigkeitsunempfindliche Schornsteine | Kachelofen, Kaminofen, offener Kamin, NT-Kessel, Brennwertkessel (bei richtiger Bemessung) | Öl, Gas, feste Brennstoffe | 80–200 °C (NT), ≤ 400 °C (Feststoff) | Unterdruck | Feuchtigkeitsunempfindlich; Kondensatableitung |
| Abgasleitungen für NT-Kessel | NT-Kessel wandhängend, raumluftunabhängige Gaswasserheizer mit Gebläse | Öl, Gas | 80–200 °C | Unterdruck | Feuchtigkeitsunempfindlich |
| Abgasleitungen für Brennwertkessel und Brennstoffzellen | Brennwertkessel wandhängend, Brennstoffzellen (stehend) | Gas (Öl) | ≤ 80 °C | Überdruck | Feuchtigkeitsunempfindlich; Kondensatableitung |
| LAS-Systeme (Luft-Abgas-Systeme) | NT-Kessel wandhängend | Gas | 80–200 °C | Überdruck | Feuchtigkeitsunempfindlich; Kondensatableitung |

---

### Gaswärmepumpen

**Gasmotorantrieb:** Erdgas treibt Verbrennungsmotor als Kompressorantrieb; Motorabwärme in Heizkreis eingebunden → hohe Effizienz. Leistungsbereich 1,5–1200 kW; Heizleistungszahl 1,5–1,8.

**Gasabsorptionswärmepumpe:** Thermischer Verdichter statt Kompressor; physikalisch-chemischer Prozess mit Lösungskreislauf (z. B. Wasser-Ammoniak); keine beweglichen Teile im Verdichter.

**Gasadsorptionswärmepumpe:** Adsorptionsverfahren (festes Adsorptionsmittel).
