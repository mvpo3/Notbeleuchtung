# Lehrbuch der Bauphysik — Teil 7
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 281-320.

Dieser Teil schließt Kapitel 11 (Feuchtetransport) ab — mit den Themen kapillarer Wasseraufnahme, Flüssigkeitsleitkoeffizienten, Schlagregenbelastung und -schutz, Luftströmungen in Kanälen, Fugenspaltströmungen, gesättigter Porenwasserströmung, Elektrokinese und Baufeuchteabfuhr — und beginnt Kapitel 12 (Feuchteübergang) mit den Stoffübergangskoeffizienten an Bauteiloberflächen.

## Inhalt

### 11.2.2 Flüssigkeitsleitkoeffizienten κ — Extremwerte

Der Flüssigkeitsleitkoeffizient κ variiert exponentiell mit dem Wassergehalt zwischen einem Trockenwert κ₀ (bei Wassergehalt u = 0) und einem Sättigungswert κf (bei kapillarer Sättigung uf). Messungen nach der NMR-Methode (zerstörungsfreie Wassergehaltsbestimmung im Labor) zeigten, dass beim Umverteilen von Wasser die κ-Werte bei hohen Wassergehalten etwa zehnmal kleiner sind als beim Saugvorgang.

**Tabelle: Extremwerte κ₀ und κf des Flüssigkeitsleitkoeffizienten (nach Krus und Kießl)**

| Baustoff | κ(u=0) [m²/h] | κ(uf) [m²/h] | κf/κ₀ [−] |
|---|---|---|---|
| Porenbeton | 8·10⁻⁶ | 8·10⁻⁴ | 100 |
| Obernkirchner Sandstein | 1·10⁻⁵ | 1·10⁻³ | 100 |
| Baumberger Sandstein | 8·10⁻⁶ | 1·10⁻⁴ | 12 |
| Ziegel | 5·10⁻⁴ | 1·10⁻² | 20 |
| Kalksandstein | 4·10⁻⁶ | 1·10⁻⁴ | 25 |
| Zementputz | 8·10⁻⁹ | 4·10⁻⁶ | 500 |
| Kalkzementputz | 8·10⁻⁹ | 4·10⁻⁵ | 5000 |
| Kalkputz | 2·10⁻⁸ | 2·10⁻³ | 100000 |
| Beton B 25 (C 20/25) | 1·10⁻⁸ | 3·10⁻⁶ | 300 |
| Beton B 35 (C 30/37) | 1·10⁻⁸ | 2·10⁻⁶ | 200 |
| Beton B 45 (C 35/45) | 1·10⁻⁸ | 1·10⁻⁶ | 100 |

### 11.2.3 Wasseraufnahmekoeffizient Ww

Wenn saugfähige Baustoffe mit Wasser in Kontakt kommen, zieht der Kapillardruck das Wasser in die Poren. Mit wachsender Eindringtiefe steigt der viskose Fließwiderstand; die Eindringtiefe h wächst daher proportional zur Wurzel der Zeit (parabolisches Zeitgesetz):

- h = W'w · √t — wobei W'w als Wassereindringkoeffizient bezeichnet wird
- Die flächenbezogene Wasseraufnahme Δm = Ww · √t (Gl. 11.23)
- Messung nach DIN EN ISO 15148: Probe mit Messfläche nach unten in Wasserbad, regelmäßiges Wägen; Δm = (mt − mi) / A
- Standardwert: Ww = Δm nach 1 Stunde Saugzeit (Gl. 11.26)
- Bei Materialien mit gekrümmter Saugkurve (z.B. hydrophobierte Baustoffe): Ww aus 24 h-Wert, Ww = Δm₂₄/√24 (Gl. 11.27)
- Weitere produktspezifische Normen: DIN EN 772-11 (Ziegel, Betonwerkstein, Porenbeton, Naturstein), DIN EN 1015-18 (Putz, Sanierputz); Prüfbedingungen nicht untereinander vergleichbar; haben DIN 52617 abgelöst

**Tabelle: Wasseraufnahmekoeffizienten Ww [kg/(m²·h⁰·⁵)]**

| Baustoff | Ww [kg/(m²·h⁰·⁵)] |
|---|---|
| Klinker | 0,5 … 5 |
| Handschlagziegel | 5 … 25 |
| Hochlochziegel | 5 … 10 |
| Vormauerziegel | 5 … 10 |
| Kalksandstein | 2,5 … 10 |
| Schlaitdorfer Sandstein | 1,5 |
| Rüthener Sandstein | 6 … 15 |
| Obernkirchner Sandstein | 1,5 … 3,0 |
| Krenzheimer Muschelkalk | 1,5 |
| Zementbeton | 0,1 … 1,0 |
| Bimsbeton | 2 … 4 |
| Porenbeton | 2 … 8 |
| Gips, Gipsmörtel | 20 … 70 |
| Weißkalkputz | 7 … 15 |
| Kalkzementputz | 0,5 … 4,0 |
| Zementputz | 0,1 … 2,0 |
| Polymerdispersionbeschichtung | 0,05 … 0,2 |
| 2-Komponenten-Polymerbeschichtung | < 0,01 |
| Silikonimprägnierte mineralische Baustoffe | 0,01 … 0,1 |

**Klassifikation der kapillaren Saugfähigkeit (Tab. 11.6):**

| Bezeichnung | Ww [kg/(m²·h⁰·⁵)] |
|---|---|
| wassersaugend | > 2 |
| wasserhemmend | 0,5 < Ww ≤ 2 |
| wasserabweisend | 0,001 < Ww ≤ 0,5 |
| wasserdicht | ≤ 0,001 |

Aus Ww lässt sich der Flüssigkeitsleitkoeffizient κf näherungsweise bestimmen (Gl. 11.28): κf = (ρw · Ww²) / (4 · uf² · ln(κf/κ₀)). Der Logarithmus-Faktor hat geringen Einfluss und kann mit Schätzwert berücksichtigt werden.

### 11.3 Feuchtetransport durch strömende Luft

#### 11.3.1 Schlagregenbelastung von Fassaden

Luftströmungen entstehen durch Gesamtdruckunterschiede bis etwa 400 Pa. Mitgeführte Wassertropfen und Wasserdampf können Feuchtemassenstromdichten erzeugen, die Wasserdampfdiffusion um Zehnerpotenzen übersteigen.

**Windgeschwindigkeiten:** Bezugshöhe 10 m über Boden (v₁₀). Mittlere Werte Deutschland: Norddeutschland ca. 5 m/s, Süddeutschland ca. 1,5 m/s, Bundesmittel ca. 3,0 m/s. Vorherrschende Windrichtung: Südwest → Nord- und Ostfassaden seltener unter Staudruck/Schlagregen.

Die Windgeschwindigkeit folgt mit der Höhe einem Exponentialgesetz: v(h) = v₁₀ · (h/10 m)ⁿ, wobei n von der Rauigkeit der Erdoberfläche abhängt.

**Staudruck:** PST = ρL · v² / 2, mit Luftdichte ρL = 1,293 kg/m³

**Tabelle: Staudruck PST in Abhängigkeit von Windgeschwindigkeit v**

| v [m/s] | 1 | 3 | 5 | 10 | 15 | 20 | 25 |
|---|---|---|---|---|---|---|---|
| PST [Pa] | 0,64 | 5,74 | 16,0 | 63,8 | 143 | 255 | 399 |

An Gebäuden variiert der Winddruck nach Geometrie und Anblasrichtung. Berücksichtigung über dimensionslosen Formfaktor C: Pw = C · PST. Positive C = Überdruck, negative C = Unterdruck. Schlagregen tritt auf, wenn fallende Regentropfen durch Wind aus ihrer Bahn abgelenkt werden; an Gebäudekanten mit hoher Windgeschwindigkeit (enge Stromlinien) besonders hohe Schlagregenbelastung.

**Beanspruchungsgruppen nach DIN 4108-3 (Tab. 11.8):**

| Gruppe | Beschreibung |
|---|---|
| I — Gering | Gebiete mit Jahresniederschlag < 600 mm; windgeschützte Lagen |
| II — Mittel | Gebiete 600–800 mm Jahresniederschlag; windgeschützte Lagen in Gebieten mit mehr Niederschlag; Hochhäuser und exponierte Lagen in Gruppe-I-Gebieten |
| III — Stark | Gebiete > 800 mm Jahresniederschlag; windreiche Gebiete (Küste, Mittel-/Hochgebirge, Alpenvorland); Hochhäuser/exponierte Lagen in Gruppe-II-Gebieten |

#### 11.3.2 Maßnahmen gegen Schlagregen

Schlagregenschutz durch vier Wirkprinzipien (Abb. 11.19):
- **A — Kapillarspeicherung:** Wandbaustoff nimmt wenig Wasser auf oder ist bei großer Dicke ausreichend speicherfähig (z.B. Sichtbeton)
- **B — Hinterlüftete Schale:** Schindeln, Platten auf Traggerüst oder hinterlüftete Vormauerschale halten Regen ab; Schale muss frostbeständig, muss nicht absolut dicht sein
- **C — Innenliegende Sperrschicht:** Undurchlässige Schicht im Wandquerschnitt (geschlossene Mörtelschale, hydrophobe Kerndämmschicht, Bitumendichtungsbahn)
- **D — Oberflächenbehandlung:** Anstriche, Mineralputze, Kunstharzputze, Imprägniermittel — kein kapillares Saugen mehr; Risse dann problematischer; rissüberbrückende Beschichtungen oder bei Spaltweiten < 0,3 mm Hydrophobierung der Randzone erforderlich

**Einschaliges Sichtmauerwerk nach DIN 1053-1:**
- Mindestens zwei Steinreihen je Steinlage mit durchgehender, schichtweise versetzter, hohlraumfrei vermörtelter Längsfuge von 2 cm Dicke
- Gesamtquerschnitt vollfugig und kraftschlüssig mauern

**Zweischaliges Sichtmauerwerk nach DIN 1053-1:**
- Zwischen den Schalen Mörtelschale 2 cm ohne Unterbrechung, als Putz auf Hintermauerschale aufgebracht
- Vormauerschale vollfugig aus frostbeständigen Steinen
- Luftschichten / Kerndämmraum am Fußpunkt gegen rückstauendes Sickerwasser durch Dichtungsbahnstreifen schützen und nach außen entwässern

**Silikonimprägnierung:** Beliebt bei Sichtmauerwerk, verändert Erscheinungsbild nicht, preiswert, Schutzdauer > 20 Jahre erreichbar.

**Anforderungen an Putze und Beschichtungen zum Schlagregenschutz (Tab. 11.10, DIN 4108-3):**
- Bezeichnung „wasserabweisend": Ww ≤ 0,5 kg/(m²·h⁰·⁵) UND sd ≤ 2 m UND Produkt Ww·sd ≤ 0,2 kg/(m·h⁰·⁵)

**Beispiele für Wandbauarten und Beanspruchungsgruppen (Tab. 11.9, DIN 4108-3 Kurzfassung):**

| Beanspruchungsgruppe I | Gruppe II | Gruppe III |
|---|---|---|
| Außenputz ohne besondere Anforderungen | wasserabweisender Außenputz nach DIN 4108-3 Tab. 6 | wasserabweisender Außenputz |
| Einschaliges Sichtmauerwerk 31 cm (mit Innenputz) | Einschaliges Sichtmauerwerk 37,5 cm (mit Innenputz) | Zweischaliges Verblendmauerwerk mit Luftschicht + Wärmedämmung oder Kerndämmung |
| Außenwände mit angemörtelten Fliesen/Platten | wie I + wasserabweisender Ansetzmörtel nach DIN 18515-1 | — |
| Außenwände mit gefügedichter Betonaußenschicht | — | — |
| Wände mit hinterlüfteten Außenwandbekleidungen | — | — |
| WDVS | — | — |
| Außenwände in Holzbauart mit Wetterschutz nach DIN 68800-2 | — | — |

**Fugen bei großformatigen Außenwandelementen (Tab. 11.11, DIN 4108-3):**

| Fugenart | Gruppe I | Gruppe II | Gruppe III |
|---|---|---|---|
| Vertikalfugen | konstruktive Ausbildung | konstruktive Ausbildung | Fugen nach DIN 18540 |
| Horizontalfugen offen | Schwellenhöhe h ≥ 60 mm | h ≥ 80 mm | h ≥ 100 mm |
| Horizontalfugen nach DIN 18540 | mit Schwelle h ≥ 50 mm | — | — |

**Fachwerkfassaden (Tab. 11.12):**

| Gruppe | Anforderungen |
|---|---|
| i(g) — geschützt | Keine Anforderungen, freie Materialwahl |
| I — gering | Gering wasserabweisende/wasserhemmende Putze; Außenanstriche sd ≤ 0,1 m; dampfdurchlässige Ausfachungsstoffe (μ < 10) |
| II/III — mittel/stark | Regenschutz durch Bekleidungen oder Putzsysteme mit Entkopplungsschicht zwischen Fachwerk und Oberputz |

**Fenster:** Schlagregendichtheit nach DIN 18055, Beanspruchungsgruppen A–D; im Normalfall nach Gebäudehöhe; Beanspruchungsgruppe im Leistungsverzeichnis anzugeben.

**Tropfkanten-Mindestmaße nach Klempnerhandwerk (Tab. 11.13):**

| Gebäudehöhe [m] | Tropfkantenabstand h3 [mm] | Ortgangaufkantung h1 [mm] | Abschluss h2 [mm] |
|---|---|---|---|
| < 8 | 40 … 60 | > 50 | 20 … 30 (Kupfer: 50 … 60) |
| 8 … 20 | 40 … 60 | > 80 | 30 … 40 (Kupfer: 50 … 60) |
| > 20 | 60 … 100 | > 100 | 40 … 50 (Kupfer: 50 … 60) |

Häufigste Beanstandungen: unzureichend ausgebildete oder fehlende Tropfkanten an Fensterbänken, Ortgängen, Mauerkronen und Attiken.

#### 11.3.3 Luftströmungen in Kanälen und Luftschichten

In vertikal vor Fassaden angeordneten Rohren treten gleichzeitig thermischer Auftrieb (bei Windstille: Strömung nach oben) und windbedingte Strömung (nach unten, steigend mit Windgeschwindigkeit) auf; bei ausreichend hoher Windgeschwindigkeit kehrt sich die Strömungsrichtung um.

**Druckdifferenz durch Wind (Gl. 11.32):** Differenz des Staudrucks zwischen oberer und unterer Öffnung in Abhängigkeit von Höhe, Windgeschwindigkeit, Rauigkeit n und Formfaktor C.

**Druckdifferenz durch thermischen Auftrieb (Gl. 11.33):** ΔPa = g · h · (ρLo − ρLu), wobei h die Höhenausdehnung der Luftsäule ist.

**Luftdichte ρL (Tab. 11.14) — sinkt mit Temperatur und relativer Feuchte:**

| θ [°C] | ρL (φ=0) [kg/m³] | ρL (φ=1) [kg/m³] | η [Pa·s] | ν [m²/s] |
|---|---|---|---|---|
| −20 | 1,394 | 1,393 | 16,2·10⁻⁶ | 11,6·10⁻⁶ |
| −10 | 1,341 | 1,340 | 16,7·10⁻⁶ | 12,4·10⁻⁶ |
| 0 | 1,292 | 1,290 | 17,1·10⁻⁶ | 13,2·10⁻⁶ |
| 10 | 1,246 | 1,241 | 17,6·10⁻⁶ | 14,1·10⁻⁶ |
| 20 | 1,204 | 1,193 | 18,1·10⁻⁶ | 15,0·10⁻⁶ |
| 30 | 1,164 | 1,146 | 18,6·10⁻⁶ | 16,0·10⁻⁶ |
| 40 | 1,127 | 1,096 | 19,1·10⁻⁶ | 16,9·10⁻⁶ |
| 50 | 1,092 | 1,042 | 19,5·10⁻⁶ | 17,9·10⁻⁶ |
| 60 | 1,060 | 0,981 | 20,0·10⁻⁶ | 18,9·10⁻⁶ |
| 70 | 1,028 | 0,909 | 20,5·10⁻⁶ | 19,9·10⁻⁶ |
| 80 | 0,999 | 0,823 | 20,9·10⁻⁶ | 20,9·10⁻⁶ |
| 90 | 0,972 | 0,718 | 21,4·10⁻⁶ | 21,9·10⁻⁶ |
| 100 | 0,946 | 0,588 | 21,8·10⁻⁶ | 23,0·10⁻⁶ |

Mittlere Strömungsgeschwindigkeit in Kanälen nach Bernoulli (Gl. 11.34): abhängig von Winddruck- und Auftriebsdruckdifferenz, Reibungsbeiwerten λ und lokalen Widerständen. Für baupraktische Berechnungen gilt vereinfachend λ = 0,04. Strömungsgeschwindigkeiten liegen typisch bei 0,1 bis 2 m/s; Reynolds-Zahl oft im Übergangsbereich laminar/turbulent.

**Feuchteabfuhr in Luftschichten (Gl. 11.36–11.37):** Die vom Diffusionsstrom aus der Wand zugeführte Feuchte gD wird von der aufsteigenden Luft abtransportiert; die relative Feuchte steigt entlang der Strömungsrichtung an. Bei Eintritt der Außenluft sinkt zunächst die relative Feuchte durch Erwärmung, dann steigt sie durch Wasserdampfaufnahme; bei zu langem Strömungsweg → Sättigung → Tauwasser. Empfehlung: Hinterlüftete Bauteile dürfen nicht zu lange Strömungswege haben; Durchströmung weder zu stark (Wärmeverlust) noch zu schwach (keine Entfeuchtung).

#### 11.3.4 Fugenspaltströmungen und Raumdurchlüftung

Fugenspaltströmungen unter atmosphärischen Druckunterschieden verursachen natürliche Raumdurchlüftung und können feuchtewarme Raumluft in Baukonstruktionen einbringen → Kondensation an unerwünschten Stellen → Durchfeuchtungsschäden besonders im Winterhalbjahr. Außenbauteile müssen daher **luftdicht** sein: Energieverluste vermeiden und Gebäudehülle vor Feuchteschäden schützen.

**Luftundichtigkeiten entstehen vor allem an:**
- Überlappungen, Anschlüssen und Durchdringungen von Luftdichtheitsbahnen
- Stößen und Anschlüssen von Plattenmaterialien
- Fensteranschlüssen
- Unverputztem Mauerwerk (→ stets Putzlage erforderlich)

**Luftvolumenstrom durch eine einzelne Fuge (Gl. 11.39):** V = a · l · Δp^(2/3) — Exponent 2/3 durch turbulente Strömung bedingt; l = Fugenlänge (Flügelumfang des Fensters).

**Fugendurchlässigkeit nach DIN 4701-2 (Tab. 11.15):**

| Bauteil | Gütemerkmal | a [m³/(m·h·Pa²/³)] |
|---|---|---|
| Fenster zu öffnen, Gruppe B/C/D | — | 0,3 |
| Fenster zu öffnen, Gruppe A | — | 0,6 |
| Fenster nicht zu öffnen, normal | — | 0,1 |
| Außentür Dreh-/Schiebetür sehr dicht | mit uml. Anschlag | 1 |
| Außentür Dreh-/Schiebetür normal | mit Schwelle/Dichtleiste | 2 |
| Pendeltür normal | — | 20 |
| Karusselltür normal | — | 30 |
| Innentür dicht | mit Schwelle | 3 |
| Innentür normal | ohne Schwelle | 9 |
| Außenwand Fertigteilelement sehr dicht | garantierte Dichtheit | 0,1 |
| Außenwand Fertigteilelement ohne Garantie | — | 1 |
| Rollläden/Jalousien von außen | normal | a·l = 0,2 m³/(h·Pa²/³) |
| Rollläden/Jalousien von innen | normal | a·l = 4 m³/(h·Pa²/³) |

**Anforderungen Energieeinsparverordnung:**
- Gebäude bis 2 Vollgeschosse: Fugendurchlässigkeitsklasse 2 → a ≤ 0,3 m³/(m·h·Pa²/³)
- Gebäude > 2 Vollgeschosse: Klasse 3 → a ≤ 0,1 m³/(m·h·Pa²/³)
- Gesamtdichtheitsprüfung: Über-/Unterdruck 50 Pa anlegen; Luftwechselrate n muss unterhalb definierter Grenze liegen

#### 11.3.5 Tauwasserschutz für Luftschichten und Luftkanäle

Luftschichten und -kanäle in Bauteilen dienen zur Schlagregenabwehr, Wasserdampfabfuhr, Tauwasserableitung und zur Erzeugung trockener, warmer Wandoberflächen; auch für sommerlichen Wärmeschutz nützlich.

**Allgemeine Anforderungen:**
- Mindestspaltweite **20 mm** (Toleranzen der Bauausführung berücksichtigt; < 20 mm riskiert Kapillarübertragung von Wand zu Wand)
- Be- und Entlüftungsöffnungen möglichst groß; am Fußpunkt schadloses Abfließen von Tauwasser sicherstellen

**a) Hinterlüftete Außenwandbekleidungen (DIN 18516-1):**
- Mindestabstand Bekleidung zu Dämmstoff / Wandoberfläche: **20 mm**
- Abstand darf örtlich auf **5 mm** reduziert werden (durch Unterkonstruktion oder Wandunebenheiten)
- Bei vertikalen Trapez-/Wellprofiltafeln streifenförmig aufliegend: freier horizontaler Hinterlüftungsquerschnitt mindestens **200 cm²/m**
- Be- und Entlüftungsöffnungen mindestens am Gebäudefußpunkt und am Dachrand: Querschnitt **≥ 50 cm² je 1 m Wandlänge**
- Lüftungsöffnungen > 20 mm Breite im Sockelbereich: durch Lüftungsgitter sichern

**b) Belüftete Dächer:**
- Nach DIN 4108-3 ohne weiteren Nachweis unbedenklich, wenn Wärmeschutz nach DIN 4108-2 eingehalten
- Ein- und Austrittsöffnungen so platzieren, dass vollständige Durchlüftung sichergestellt ist; bei komplizierten Dachflächen prüfen, ob tatsächlich Winddruck + Windsog auf verschiedenen Seiten entstehen

**c) Hinterlüftete Vormauerschalen (DIN 1053-1):**
- Luftspalt: mindestens **40 mm** dick
- Beginn der Luftschicht: mindestens **100 mm** über Erdgleiche
- Lüftungsöffnungen: oben und unten, auch im Brüstungsbereich
- Größe der Lüftungsöffnungen: je **7500 mm²** Fläche pro **20 m²** Wandfläche
- Ergebnis: gebremste Hinterlüftung, ausreichend zur Tauwasserabfuhr im Jahreszyklus

**d) Durchlüftete Kanäle:**
- Rechnerischer Wirksamkeitsnachweis empfohlen (höherer Strömungswiderstand als bei Luftschichten)

**e) Spalten, Fugen und Risse:**
- Müssen luftundurchlässig ausgeführt / abgedichtet werden: Tauwasserbildung, Energieverluste, Schalldurchgang, Rauchdurchtritt verhindern
- Bei Neubauten und energetischen Instandsetzungen: Aufstellen eines Luftdichtheitskonzepts obligatorisch

### 11.4 Strömung von Wasser in gesättigten Poren und in Rissen

**Newton'sches Fließgesetz:** Scherspannung τ = η · (dv/dx), wobei η der dynamische Viskositätskoeffizient und dv/dx das Geschwindigkeitsgefälle ist. Gilt für viskoses Fließen von Flüssigkeiten und Gasen bei nicht zu großen Geschwindigkeitsgefällen.

**Eigenschaften von Wasser (Tab. 11.16):**

| θ [°C] | ρW [kg/m³] | η [Pa·s] | ν [m²/s] | σ [N/m] |
|---|---|---|---|---|
| 0 | 1000 | 1,787·10⁻⁶ | 1,787·10⁻⁶ | 0,0756 |
| 10 | 1000 | 1,307·10⁻⁶ | 1,307·10⁻⁶ | 0,0742 |
| 20 | 998 | 1,002·10⁻⁶ | 1,004·10⁻⁶ | 0,0727 |
| 30 | 996 | 0,798·10⁻⁶ | 0,801·10⁻⁶ | 0,0712 |
| 40 | 992 | 0,653·10⁻⁶ | 0,658·10⁻⁶ | 0,0696 |
| 50 | 988 | 0,547·10⁻⁶ | 0,554·10⁻⁶ | 0,0679 |
| 60 | 983 | 0,467·10⁻⁶ | 0,475·10⁻⁶ | 0,0662 |
| 70 | 978 | 0,404·10⁻⁶ | 0,413·10⁻⁶ | 0,0646 |
| 80 | 972 | 0,355·10⁻⁶ | 0,365·10⁻⁶ | 0,0626 |
| 90 | 965 | 0,315·10⁻⁶ | 0,326·10⁻⁶ | 0,0608 |
| 100 | 958 | 0,282·10⁻⁶ | 0,294·10⁻⁶ | 0,0589 |

**Hagen-Poiseuille-Gesetz für Rohrströmung (Gl. 11.45):** Massenstrom G durch zylindrisches Rohr mit Durchmesser d: G = (ρw · π · d⁴) / (128 · η) · (dp/dx)

**Spaltströmung (Gl. 11.46):** Massenstrom G durch Spalt der Weite d und Länge L: G = (ρw · d³ · L) / (12 · η) · (dp/dx)

**Darcy'sches Gesetz für gesättigte Porenwasserströmung in Böden (Gl. 11.47):** g = kD · (dp/dx), wobei kD die spezifische Durchlässigkeit nach Darcy ist. Gilt nur für vollständig wassergesättigte Porensysteme ohne Luftanteile.

**Tabelle: Darcy-Durchlässigkeiten für Bodenarten (Tab. 11.17):**

| Bodenart | kD [m/s] | kD [g·m/(h·m²·Pa)] |
|---|---|---|
| Feinkies | 10⁻⁴ bis 3·10⁻⁴ | 40 bis 120 |
| Grobsand | 0,5·10⁻⁴ bis 10⁻⁴ | 20 bis 40 |
| Mittelsand | 0,5·10⁻⁵ bis 10⁻⁵ | 2 bis 4 |
| Feinsand | 10⁻⁷ bis 10⁻⁶ | 0,04 bis 0,4 |
| Schluff, sandig | 10⁻⁶ bis 10⁻⁴ | 0,4 bis 40 |
| Schluff | 10⁻⁹ bis 10⁻⁶ | 0,0004 bis 0,4 |
| Löss | 10⁻⁸ bis 10⁻⁵ | 0,004 bis 4 |
| Lehm | 10⁻¹⁰ bis 10⁻⁶ | 0,00004 bis 0,4 |

Darcy-Gesetz praktisch angewendet für: Sickerwasserströmungen in Böden, Sickerschichten, Konsolidationsvorgänge in bindigen Böden. Für klassische Baustoffe kaum Messwerte, weil Bedingungen (vollständige Sättigung, Gesamtdruckgefälle) in Bauteilen selten gegeben.

**Durchströmung von Rissen in Beton (Gl. 11.48):** G = ξ · (ρw · d³ · L) / (12 · η) · (dp/dx), wobei ξ der Durchflussbeiwert ist (Berücksichtigung der Wandrauigkeit):
- Bei glatten Wandungen und weiten Rissen: ξ → 1
- Bei Spaltweiten ~0,05 mm: ξ → 0
- Riss in Beton mit Größtkorn 16 mm, Spaltweite 0,15 mm: ξ = 0,01
- Im Laufe der Zeit: ξ fällt um bis zu 90 % ab (Riss wirkt als Filter, setzt sich zu)
- Bei Rissweiten ≤ ~0,1 mm: lokaler Verschluss möglich → Risse können wasserdicht werden
- Voraussetzung: keine Aufweit- und Scherbewegungen; Wasser nicht betonaggressiv

### 11.5 Elektrokinese

Wasser in wassergesättigten, feinporigen Stoffen (Steine, Putze, bindige und sandige Böden, Baumstämme, organische Polymere) beginnt zu fließen, wenn es elektrisch geladene Teilchen (Ionen) enthält und einem elektrischen Spannungsgefälle ausgesetzt wird. Fließrichtung: zur Kathode hin. Das Phänomen wird als elektrokinetischer Wassertransport (= Elektro-Osmose) bezeichnet.

**Messprinzip:**
- **Fließversuch:** Probekörper in U-förmige Apparatur eingesetzt, Abfluss offen; Messung des Wasservolumenstroms g in Abhängigkeit vom elektrischen Spannungsgefälle dU/dx
- **Stauversuch:** Abfluss gesperrt, Steigrohr angebracht; nach Einpendeln misst man den Gesamtdruck, der dem elektrischen Antrieb das Gleichgewicht hält

**Berechnungsansatz (Gl. 11.49):** g = ke · (dU/dx), analog zum Darcy'schen Gesetz, wobei ke der elektrokinetische Durchlässigkeitskoeffizient ist.

**Spezifische elektrokinetische Steighöhe (Gl. 11.50):** he = ke / kD — Verhältnis der beiden Durchlässigkeiten.

**Anwendungen der Elektrokinese:**
- Messung von Wasserbewegungen in Bauteilen, Böden und Bäumen
- Bodenverbesserung durch Entwässerung und Eintrag stabilisierender Fremdionen
- Entwässerung von Baustoffen
- Verhinderung des kapillaren Aufsteigens von Bodenfeuchte in Wänden

### 11.6 Abführen der Baufeuchte

Baufeuchte bezeichnet den erhöhten Wassergehalt von Bauteilen unmittelbar nach Fertigstellung, verursacht durch Herstellung, Transport, Zwischenlagerung der Baustoffe und ungeschützten Rohbauzustand.

**Strategien zur Minimierung der Baufeuchteprobleme:**
- Baustoffwahl: Gussasphalt-Estrich statt Zementestrich; dampfdurchlässiger Teppich statt PVC-Belag; diffusionsoffene Unterspannbahnen; trocken einbaubare Gipskartonplatten statt Putz
- Sperrschichten gegen Feuchteumlagerungen (z.B. aus Betondecken in Estriche)
- Künstliches Trocknen vor Einbau feuchteempfindlicher Materialien
- Nutzern von Neubauten: kräftige Lüftung in der Anfangszeit

**Einflussfaktoren auf Austrocknungsgeschwindigkeit:**
- Ausgangswassergehalt
- Verhältnis von feuchtem Baustoffvolumen zu Verdunstungsoberfläche
- Konvektionsverhältnisse und Dampfdruckgefälle an der Verdunstungsoberfläche
- Verzögernde Oberflächenschichten

**Betonaustrocknung:** Beton enthält nach Herstellung durchschnittlich ~80 kg/m³ austrocknungsfähiges Wasser; trocknet wegen Porenstruktur des Zementsteins und großer Querschnitte langsam.

**Austrocknungszeiten für Betonplatten in trockener Luft (Tab. 11.18, DIN 4227):**

| Plattendicke [cm] | Beidseitig [a] | Einseitig [a] |
|---|---|---|
| 5 | 0,25 | 0,6 |
| 10 | 0,60 | 1,5 |
| 20 | 1,5 | 4 |
| 40 | 4 | 8 |
| 80 | 8 | 16 |
| 160 | 16 | 30 |

**Faktoren für Austrocknungszeit je nach Luftbedingungen:**
- Trockene Luft: Faktor 1,0
- Allgemein im Freien: Faktor 1,5
- Sehr feuchte Luft: Faktor 5,0

**Belegreife von Estrichflächen:** Messung des Wassergehalts mit Calciumcarbid-Methode; maximale Feuchtegehalte vor dem Verlegen (Tab. 11.19):

| Bodenbelag | Zementestrich max. u [%] | Calciumsulfatestrich max. u [%] |
|---|---|---|
| Elastische Beläge dampfdicht | 1,8 | 0,3 |
| Elastische Beläge dampfdurchlässig | 3,0 | 1,0 |
| Textile Beläge dampfdicht | 1,8 | 0,3 |
| Textile Beläge dampfdurchlässig | 3,0 | 1,0 |
| Parkett, Kork | 1,8 | 0,3 |
| Laminat | 1,8 | 0,3 |
| Keramik/Natur-/Betonwerkstein Dickbett | 3,0 | — |
| Keramik/Natur-/Betonwerkstein Dünnbett | 2,0 | 0,3 |

Magnesia-Estriche: nicht beschichten oder belegen.

**Heizestriche (DIN 18560-2):** Müssen nach ausreichender Erhärtungszeit zuerst vorsichtig vorgeheizt werden; dabei trocknet der Estrich aus und schwindet. Erst dann feuchteempfindliche oder Schwindung behindernde Beläge aufbringen.

**Einfluss der Wärmedämmschicht auf Austrocknung:**
- WDVS an Außenwänden: erhöht mittlere Temperatur → fördert Austrocknung, behindert aber Austrocknung nach außen
- Dämmschicht über erdberührender Betonplatte: sehr geringe Austrocknung nach oben
- Dämmschicht unter erdberührender Betonbodenplatte: Austrocknung nach oben gefördert

**Sanierputze:** Zementgebundene Leichtputze mit Porenanteil **≥ 40 %** für feuchtes und salzhaltiges Mauerwerk (Altbauten, Baudenkmäler, Kellerwände, Sockel):
- Kleiner Diffusionswiderstand, geringes kapillares Saugen
- Rasche Feuchteabgabe an die Luft bei trockener Oberfläche
- Im Kapillarwasser transportierte Salze werden schadlos im Porenvolumen der Sanierputze abgelagert
- Oberflächenbehandlung (Anstriche, Oberputze) möglich, sofern Wasserdampfdurchlässigkeit erhalten bleibt

---

## Kapitel 12: Feuchteübergang

### 12.1 Stoffübergangskoeffizienten βp und βv

Luftbespülten Bauteiloberflächen haftet eine wenige Millimeter dicke, weitgehend ruhende Grenzschicht an. Feuchtetransport durch diese Grenzschicht erfolgt ausschließlich per Wasserdampfdiffusion (μ = 1 für Luft). Berechnungsansatz (Gl. 12.1): g = βp · (pO − pL), wobei βp der Wasserdampfübergangskoeffizient [kg/(m²·h·Pa)] ist.

Alternativ mit Konzentrationsdifferenz Δν oder mit äquivalenter Luftschichtdicke sd der Grenzschicht (Gl. 12.2): g = δ_Luft · (pO − pL) / sd. Da μ_Luft = 1, ist sd direkt gleich der effektiven physikalischen Dicke der Grenzschicht.

**Übergangskoeffizienten als Funktion der Luftgeschwindigkeit (Tab. 12.1):**

| Situation | v [m/s] | βv [m/h] | βp [kg/(m²·h·Pa)] | sd [m] |
|---|---|---|---|---|
| In Räumen (h = 2,5 m) | 0,10 | 3,0 | 0,22·10⁻⁴ | 31 |
| In Räumen | 0,15 | 4,0 | 0,30·10⁻⁴ | 23 |
| In Räumen | 0,25 | 6,0 | 0,45·10⁻⁴ | 16 |
| In Räumen | 0,50 | 10 | 0,75·10⁻⁴ | 9,3 |
| In Räumen (Ecken) | 0,50 | 10 | 0,75·10⁻⁴ | 9,3 |
| In Räumen | 1,0 | 16 | 1,2·10⁻⁴ | 5,6 |
| In Räumen | 2,5 | 35 | 2,6·10⁻⁴ | 2,6 |
| Im Freien (l = 5 m) | 5,0 | 55 | 4,5·10⁻⁴ | 1,5 |
| Im Freien | 10 | 100 | 7,8·10⁻⁴ | 0,9 |
| Im Freien | 25 | 200 | 16·10⁻⁴ | 0,4 |

Umschlag von laminarer zu turbulenter Luftströmung: bei ~0,1 m/s. Für Räume wurde l = 2,5 m (Geschosshöhe, Strömung praktisch vertikal) angesetzt; im Freien l = 5,0 m (Strömungsweg von Fassadenmitte zu Gebäudekante bei kleineren/mittleren Gebäuden).

**Formeln für βv (nach Krischer und Kast):**
- Turbulente Strömung (Gl. 12.3): βv = 22 · (v^0,81 / l^0,19) [m/h]
- Laminare Strömung (Gl. 12.4): βv = 13 · (v^0,5 / l^0,5) [m/h]

### 12.2 Stoffübergang im konkreten Fall

Berechnung der Feuchtestromdichte durch die Grenzschicht erfordert neben βp auch die Dampfdruckdifferenz. Diese ist schwer direkt anzugeben, weil Feuchte- und Wärmetransport gekoppelt sind.

**Energiebilanz an der Bauteil-/Wasseroberfläche (Gl. 12.5):**
qj + qi − qv − q(k+s) = 0

Komponenten:
- qj = a · I — Sonneneinstrahlung (Absorptionskoeffizient a × Strahlungsintensität I)
- qi = (θR − θO) / (Σ(di/λi) + Rsi) — Transmissionswärme aus dem Bauteil/Raum
- qv = r · βp · (psat,O · φO − psat,L · φL) — Verdunstungswärme; r ist die temperaturabhängige Verdunstungswärme
- q(k+s) = h · (θO − θL) — Wärmeabgabe durch Konvektion und Strahlung

**Verdunstungswärme r:** Beim Verdunsten von Eis/Schnee werden Schmelz- + Flüssigkeits- + Verdampfungswärme aufgewendet; zum Verdampfen aus 100 °C warmem Wasser nur noch die reine Verdampfungswärme.

**Erkenntnisse aus Parameterstudien:**
- Sommer: Verdunstung durch Luftbewegung und hohe Außenlufttemperaturen stark gefördert
- Winter: Wind hat praktisch keinen Einfluss auf Fassadentrocknung (erhöht βp, senkt aber gleichzeitig Oberflächentemperatur → kein Nettoeffekt)
- Sonneneinstrahlung: großer Einfluss; bei Vorliegen immer Bilanzbetrachtung erforderlich
- Im Sommer: trotz intensiver Sonnenstrahlung kann eine nasse Fläche durch kühlende Verdunstungswirkung nicht wärmer als **40 °C** werden

**Richtwerte für Energiestromdichten (Tab. 12.2):**

| Bezeichnung | Bedingungen | Größenordnung [W/m²] |
|---|---|---|
| Verdunstungswärme qv | Nasse Fassade Sommer windgeschützt | 30 |
| Verdunstungswärme qv | Nasse Fassade Sommer stark angeblasen | 300 |
| Verdunstungswärme qv | Tauen von Wasserdampf an 5 °C Raumoberfläche | 20 |
| Transmissionswärme qi | Gut gedämmte Außenwand | 10 |
| Transmissionswärme qi | Schlecht gedämmte Außenwand | 80 |
| Strahlungswärme qj | Südfassade Tagesmittel Sommer+Winter Kalksandstein hell | 150 |
| Strahlungswärme qj | Südfassade Tagesmittel Sommer+Winter Ziegel rot | 300 |
| Strahlungswärme qj | Nordfassade Tagesmittel Sommer+Winter Kalksandstein hell | 25 |
| Strahlungswärme qj | Nordfassade Tagesmittel Sommer+Winter Ziegel rot | 50 |

**Tauwasserabgabe an kalten Raumoberflächen:** Berechnet für θR = 20 °C und βp = 0,75·10⁻⁴ kg/(m²·h·Pa) (~0,5 m/s Luftgeschwindigkeit). Erfahrungsgemäß tritt Tauwasser in Räumen bevorzugt an Wärmebrücken (z.B. nach außen vorspringende Ecken) auf, weil dort die niedrigsten Temperaturen und damit die größte Dampfdruckdifferenz und Tauwasserstromdichte herrschen.

---

### Normverzeichnis (Kapitel 11–12)

- DIN EN ISO 12572 — Wasserdampfdurchlässigkeit von Baustoffen und Bauprodukten (2015-01)
- DIN EN ISO 15148 — Wasseraufnahmekoeffizient bei teilweisem Eintauchen (2003-03)
- DIN EN 772-11 — Kapillare Wasseraufnahme von Mauersteinen aus Beton, Porenbeton, Betonwerkstein, Naturstein (2011-07)
- DIN EN 1015-18 — Kapillare Wasseraufnahme von erhärtetem Mörtel (2003-03)
- DIN 52615 — Wasserdampfdurchlässigkeit von Bau- und Dämmstoffen (1987-11)
- DIN 52617 — Wasseraufnahmekoeffizient von Baustoffen (1987-05, abgelöst)
- DIN 1053-1 — Mauerwerk, Berechnung und Ausführung (1996-11)
- DIN 4108-3 — Klimabedingter Feuchteschutz; Anforderungen, Berechnungsverfahren und Hinweise (2018-10)
- DIN 4108-7 — Luftdichtheit von Gebäuden (2011-01)
- DIN 4108-2 — Mindestanforderungen an den Wärmeschutz (2013-02)
- DIN 4227-1 — Spannbeton Bauteile aus Normalbeton (1988)
- DIN 4701-2 — Regeln für die Heizlastberechnung, Tabellen (Entwurf 1995-08)
- DIN 18055 — Fenster; Fugendurchlässigkeit, Schlagregendichtheit (1981-10)
- DIN 18516-1 — Außenwandbekleidungen hinterlüftet, Anforderungen und Prüfgrundsätze (2010-06)
- DIN 18540 — Abdichten von Außenwandfugen mit Fugendichtstoffen (2014-09)
- DIN 18560-2 — Estriche und Heizestriche auf Dämmschichten (2009-09)
- DIN 68800-2 — Holzschutz, Wetterschutz (Holzbauart)
