# Baukonstruktionslehe 1 — Teil 23
> Quelle: Baukonstruktionslehe 1 (buecher) · Seiten 921-960.

Dieser Abschnitt behandelt vertieft den konstruktiven Wärmeschutz (Kapitel 17.5): Symbolsystematik für bauphysikalische Größen, Mindest-Wärmedurchlasswiderstände, sommerlichen Wärmeschutz mit Nachweisverfahren und Schutzmaßnahmen, Wärmedämmstoffe und deren Kennzeichnung, Wasserdampfdiffusion mit dem Glaser-Verfahren, Innendämmung sowie Wärmebrücken mit wärmebrückenfreiem Konstruieren.

## Inhalt

### Symbole und Indizes bauphysikalischer Größen (Tab. 17.14 und 17.15, DIN 4108-2)

Normwechsel der Formelzeichen: bisherige Symbole wurden durch neue, internationale Symbole ersetzt. Wesentliche Zuordnungen (Norm: DIN EN ISO 7345 sofern nicht anders angegeben):

| Physikalische Größe | Einheit | Neues Symbol | Norm |
|---|---|---|---|
| Schichtdicke | m | d | DIN EN ISO 6946 |
| Fläche | m² | A | DIN EN ISO 7345 |
| Volumen | m³ | V | DIN EN ISO 7345 |
| Eingeschlossenes Gebäudevolumen | m³ | Ve | – |
| Masse | kg | m | DIN EN ISO 7345 |
| Rohdichte | kg/m³ | ρ | DIN EN ISO 7345 |
| Celsius-Temperatur | °C | θ | DIN EN ISO 7345 |
| Absolute Temperatur | K | T | DIN EN ISO 7345 |
| Wärmemenge | J; Wh; kWh | Q | DIN EN ISO 7345 |
| Wärmestrom/-leistung | W | Φ | DIN EN ISO 7345 |
| Wärmestromdichte | W/m² | q | DIN EN ISO 7345 |
| Spez. Transmissionswärmeverlustkoeffizient | W/K | HT | DIN EN ISO 13789 Anh. B |
| Wärmeleitfähigkeit | W/(m·K) | λ | DIN EN ISO 7345 |
| Wärmedurchlasskoeffizient | W/(m²·K) | Λ | DIN EN ISO 7345 |
| Wärmedurchlasswiderstand | m²·K/W | R | DIN EN ISO 7345 |
| Flächenbezogener Wärmeübergangskoeffizient | W/(m²·K) | h | DIN EN ISO 7345 |
| Wärmeübergangswiderstand innen | m²·K/W | Rsi | DIN EN ISO 6946 |
| Wärmeübergangswiderstand außen | m²·K/W | Rse | DIN EN ISO 6946 |
| Wärmedurchgangskoeffizient | W/(m²·K) | U | DIN EN ISO 7345 |
| Wärmedurchgangswiderstand | m²·K/W | RT | DIN EN ISO 6946 |
| Wasserdampfteildruck | Pa | p | DIN EN ISO 9346 |
| Relative Luftfeuchte | % | φ | DIN EN ISO 9346 |
| Wasserdampf-Diffusionsstromdichte | kg/(m²·h) | g | DIN EN ISO 9346 |
| Wasserdampf-Diffusionsdurchlasswiderstand | m²·h·Pa/kg | G | DIN EN ISO 9346 |
| Wasserdampfleitfähigkeit/-koeffizient | kg/(m·h·Pa) | δ | DIN EN ISO 9346 |
| Wasserdampf-Diffusionswiderstandszahl | – | μ | DIN EN ISO 9346 |
| Diffusionsäquivalente Luftschichtdicke | m | sd | DIN EN ISO 9346 |
| Wärmebrückenverlustkoeffizient (linear) | W/(m·K) | ψ | DIN EN ISO 10211 |
| Wärmebrückenverlustkoeffizient (punktförmig) | W/K | χ | DIN EN ISO 10211 |
| Temperaturfaktor | – | fRsi | DIN EN ISO 10211 |
| Sonneneintragskennwert | – | S | DIN 4108-2 |
| Zuschlagswert zum Sonneneintragswert | – | ΔS | DIN 4108-2 |
| Abminderungsfaktor Sonnenschutzvorrichtung | – | FC | DIN EN 832 |
| Gesamtenergiedurchlassgrad | – | g | DIN EN 410 |
| Abdeckwinkel | ° | β | DIN 4108-2 |

Indizes (Auszug, Tab. 17.15):
- w = Fenster, f/F = Rahmen, g = Verglasung, S = Oberfläche
- e = außen, a = Umgebung, AW = Außenwand
- h = Heizung, V = Lüftung, W = Warmwasser, t = Anlagentechnik
- r = regenerativ/Umwelt, HF = Hauptfassade, i = innen, l = längenbezogen

---

### Erdberührte Bauteile und mittlere Wärmedurchgangskoeffizienten

Erdberührte Außenflächen (Bodenplatten) werden nach ISO 13370 bzw. DIN EN 52016 berechnet; der anrechenbare Erdreichwiderstand bis zur Außenluft fließt ein. Als grobe Näherung darf ein Reduktionsfaktor btr (in Mitteleuropa etwa 0,5) auf den konventionell ermittelten U-Wert der reinen Bauteilschichten angewendet werden.

**Mittlerer U-Wert einer Gebäudehülle:** Besteht die Hülle aus Bauteilen mit Flächen A₁...Aₙ und U-Werten U₁...Uₙ ergibt sich der gesamte spezifische Wärmeverlust:
- Htr = A₁·U₁ + A₂·U₂ + ... + Aₙ·Uₙ (in W/K)

Für inhomogene Bauteile (z.B. Holzständer mit Gefach) schreibt ISO 6946 ein Näherungsverfahren vor:
- Oberer Grenzwert R'tr: Parallelschaltung der einzelnen Bauteilbereiche über Flächenanteile
- Unterer Grenzwert R''tr: serielle Reihenschaltung über homogene Lagen, wobei jede inhomogene Lage als Parallelwiderstand berechnet wird
- Mittlerer Widerstand: Rtr = (R'tr + R''tr) / 2
- Wenn Differenz zwischen R'tr und R''tr über 20 % liegt, empfiehlt sich eine zweidimensionale Temperaturfeldbrechnung (ISO 10211-2) oder ein Wärmebrückenkatalog.

**Luftschichten und Gasschichten:** Der Wärmedurchlasswiderstand ruhender Luftschichten hängt von der Schichtdicke und der Richtung des Wärmestroms ab (Tab. 17.17, ISO 6946). Bei Schichten über 300 mm Dicke darf kein Wärmedurchlasswiderstand angesetzt werden — stattdessen Wärmebilanz nach ISO/DIS 13789.

Wärmedurchlasswiderstand (m²·K/W) ruhender Luftschichten nach Richtung des Wärmestroms:

| Dicke (mm) | Aufwärts | Horizontal | Abwärts |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 5 | 0,11 | 0,11 | 0,11 |
| 7 | 0,13 | 0,13 | 0,13 |
| 10 | 0,15 | 0,15 | 0,15 |
| 15 | 0,16 | 0,17 | 0,17 |
| 25 | 0,16 | 0,18 | 0,19 |
| 50 | 0,16 | 0,18 | 0,21 |
| 100 | 0,16 | 0,18 | 0,22 |
| 300 | 0,16 | 0,18 | 0,23 |

Schwach belüftete Luftschichten: niedrigere Werte als Tab. 17.17. Stark belüftete Luftschichten (z.B. Luftschichten in zweischaligem Mauerwerk nach DIN 1053): gelten als nicht wärmedämmend — weder Luftschicht noch Vormauerschale dürfen bei U-Wert-Berechnungen berücksichtigt werden.

---

### Mindestwerte für Wärmedurchlasswiderstände (Tab. 17.16, DIN 4108-2: 2001-03)

| Nr. | Bauteilkategorie | R [m²·K/W] |
|---|---|---|
| 1 | Außenwände; Wände gegen Bodenräume, Durchfahrten, Hausflure, Garagen, Erdreich | 1,2 |
| 2 | Wände zwischen fremd genutzten Räumen; Wohnungstrennwände | 0,07 |
| 3 | Treppenraumwände zu indirekt beheizten Treppenhäusern (Θi > 10 °C, frostfrei) | 0,25 |
| 4 | Treppenraumwände bei Θi > 10 °C (Verwaltung, Geschäft, Hotel, Wohngebäude) | 0,07 |
| 5 | Wohnungstrenndecken, Decken fremder Arbeitsräume; Decken unter gedämmten Dachschrägen/-abseitenwänden (allgemein) | 0,35 |
| 6 | Wohnungstrenndecken in zentralbeheizten Bürogebäuden | 0,17 |
| 7 | Unterer Abschluss nicht unterkellerter Aufenthaltsräume: unmittelbar an Erdreich bis 5 m Raumtiefe | – |
| 8 | Unterer Abschluss: über nicht belüfteten Hohlraum an Erdreich grenzend | 0,90 |
| 9 | Decken unter nicht ausgebauten Dachräumen; unter bekriechbaren Räumen; unter belüfteten Räumen zwischen Dachschrägen und Abseitenwänden; wärmegedämmte Dachschrägen | – |
| 10 | Kellerdecken; Decke gegen abgeschlossene unbeheizte Hausflure | – |
| 11.1 | Decken/Dächer Aufenthaltsraum gegen Außenluft — nach unten (Garagen, Durchfahrten, belüftete Kriechkeller) | 1,75 |
| 11.2 | Decken/Dächer gegen Außenluft — nach oben (Flachdächer, Terrassen; Umkehrdach: Korrektur ΔU nach ISO 6946 Tab. 4) | 1,2 |

Hinweis: erhöhter Wärmedurchlasswiderstand bei 11.1 wegen Fußkälte.

---

### Wärmespeicherung

Wärmekapazität C eines Bauteils beschreibt die gespeicherte Wärmemenge proportional zur Temperaturänderung. In Bauteilen relevante Zeitmaßstäbe: Minuten bis wenige Tage. Monatliche oder jährliche Speichereffekte in normalen Bauteilen vernachlässigbar (anders im Erdreich mit meterdicken Materialstärken).

Wirksame Wärmekapazität des Gebäudes:
- Cwirk = Σ(cᵢ · ρᵢ · dᵢ · Aᵢ)
  - cᵢ = spezifische Wärmekapazität (Wh/(kg·K))
  - ρᵢ = Rohdichte (kg/m³)
  - dᵢ = wirksame Schichtdicke (m), begrenzt auf 0,1 m (typische Tages-Eindringtiefe)
  - Aᵢ = Bauteilfläche (m²)
- Nur Materialschichten raumseitig von Dämmschichten (λ ≥ 0,1 W/(m·K)) dürfen angerechnet werden
- Normen fordern keine Mindestwärmekapazität; sie wirkt sich vor allem beim sommerlichen Wärmeschutz positiv aus

Negative Effekte hoher Wärmekapazität: bei nicht dauernd beheizten Gebäuden höherer Heizwärmebedarf, da Temperaturabfall nach Abschaltung langsamer, Verluste damit länger andauernd.

---

### 17.5.4 Sommerlicher Wärmeschutz

Im Sommer dominiert solare Einstrahlung durch Glasflächen (bis zu ~800 W/m² Solarstrahlungsleistung). Wände überschreiten auch im ungünstigsten Fall kaum 60 W/m². Ausgebaute Dachgeschosse mit großen Dachflächen besonders gefährdet (Außenoberflächentemperatur über 70 °C möglich). Mitteleuropa: periodische Nachtabkühlung ermöglicht Wärmeabfuhr — Ausnutzung wichtig.

Einflussfaktoren auf sommerliche Raumerwärmung (nach Bedeutung):
1. Flächenanteile transparenter Außenbauteile (Fensterflächenanteil f) incl. Rahmenanteil und Verschattung
2. Neigung und Orientierung der transparenten Flächen
3. Gesamtenergiedurchlassgrad g (g-Wert) der Verglasung
4. Innere Wärmequellen
5. Wirksame Wärmekapazität Cwirk der innen gelegenen raumnahen Bauteile
6. Lüftung (besonders nächtliche Lüftung, bevorzugt 2. Nachthälfte)
7. U-Werte und Absorptionsgrade der opaken Außenbauteile, insbesondere Dächer

Temperatur-Amplitudenverhältnis (TAV): Ab U < 0,3 W/(m²·K) praktisch bedeutungslos. Bei den empfohlenen modernen Standards (U < 0,14 W/(m²·K)) spielt TAV keine Rolle mehr. Für leichte Außenbauteile mit Flächenmasse m' < 100 kg/m² muss Mindestwärmedurchlasswiderstand R ≥ 1,75 m²·K/W eingehalten werden; bei Rahmen- und Skelettkonstruktionen gilt R ≥ 1,75 m²·K/W nur für den Gefachbereich, im Mittel über das Bauteil R ≥ 1,0 m²·K/W. Empfohlene Außenbauteile übertreffen diese Werte bei weitem (R ≥ 6,0 m²·K/W empfohlen).

#### 17.5.4.1 Normative Anforderungen (DIN 4108-2, Abschn. 8)

Nachweis über Sonneneintragskennwert Svorh, der den zulässigen Wert Szul nicht überschreiten darf:
- Svorh ≤ Szul

Berechnungsformel:
- Svorh = Σ(Aw,j · gtot,j) / AG
  - Aw,j = Fensterflächeninhalt des j-ten Fensters (m²)
  - gtot = Gesamtenergiedurchlassgrad Glas + Sonnenschutz = g · FC
    - g = Gesamtenergiedurchlassfaktor des Fensters (nach DIN EN 410)
    - FC = Abminderungsfaktor für fest eingebaute Sonnenschutzvorrichtungen (DIN 4108-2 Tab. 7)
    - FC ist eigentlich Durchlassfaktor (FC = 0,15 bedeutet: 15 % Strahlung durchgelassen)
  - AG = Nettogrundflächedes Raumes (m²)

Kein Nachweis erforderlich, wenn (Tab. 17.19):

| Neigung (gegen Horizontale) | Orientierung | Fensterflächenanteil fwg (%) |
|---|---|---|
| Über 60° bis 90° | NW über S bis NO | ≤ 10 |
| Über 60° bis 90° | alle anderen Nordorientierungen | ≤ 15 |
| 0° bis 60° | alle Orientierungen | ≤ 7 |

Orientierungstoleranz: ±22,5°. An Grenzen: kleinerer Fensterflächenanteil maßgebend.

Abminderungsfaktoren FC fest installierter Sonnenschutzvorrichtungen (Tab. 17.20):

| Art der Sonnenschutzvorrichtung | FC |
|---|---|
| Keine Sonnenschutzvorrichtung | 1,00 |
| Innenliegend/zwischen Scheiben, weiß/reflektierend, Transparenz < 10 % | 0,65 |
| Innenliegend/zwischen Scheiben, hell, Transparenz < 10 % | 0,75 |
| Innenliegend/zwischen Scheiben, dunkel, Transparenz < 30 % | 0,85 |
| Außenliegend: Jalousien, Raffstores, drehbare Lamellen 45° | 0,25 |
| Außenliegend: Jalousien, Raffstores, drehbare Lamellen 10° | 0,15 |
| Vordächer, Markisen, freistehende Lamellen | 0,50 |

Nur fest installierte Sonnenschutzvorrichtungen zählen; dekorative Vorhänge gelten nicht als Sonnenschutz.

Gesamtenergiedurchlassgrade gV von Verglasungen (Tab. 17.21):

| Verglasung | gV |
|---|---|
| Einfachverglasung (Klarglas) | 0,9 |
| Doppelverglasung (Klarglas) | 0,8 |
| Dreifachverglasung (Klarglas) | 0,7 |
| Glasbausteine | 0,6 |
| Sonnenschutzverglasung ohne Nachweis | 0,8 |

Beispiel Herstellerkennzeichnung: „49/34" = 49 % Tageslichtdurchlässigkeit, g-Wert 0,34. Falls nur Energiedurchgangsfaktor b nach VDI 2078 bekannt: g = 0,87 · b.

Der berechnete Svorh-Wert ist ein Anforderungswert nach GEG, kein bloßer Richtwert. Wenn Randbedingungen der Norm (z.B. maximale interne Lasten) nicht eingehalten werden können (z.B. Klassenräume mit PC-Nutzung), ist eine thermische Gebäudesimulation für den Genehmigungsnachweis erforderlich.

#### 17.5.4.2 Erweitertes Sommerfallverfahren (PHPP)

Analytisch gelöstes Einkapazitätenmodell, das monatliche Klimadaten nutzt und einzelne Monate in kürzere Hitzeperioden auflöst. Eingabegrößen:
- Fensterflächenanteile nach Himmelsrichtungen Aw,j
- Verglasungsqualitäten (U-Werte, g-Werte)
- Rahmenanteile und Verschattung durch Laibung, Überstände, Bebauung, Topografie
- Luftwechselraten n (mechanisch, Erdreichwärmetauscher)
- Innere Wärmequellen qi
- Wärmeschutz und Absorptionsgrad der Außenbauteile Uj und αj
- Wirksame innere Speichermasse Cwirk

Ziel: Übertemperaturstunden unter 5 % des Jahres ohne Klimaanlage. Bei unvermeidbarer aktiver Kühlung: Berechnung der Kennwerte des Kühlenergiebedarfs und der Kühllast über das PHPP-Kühlrechnenblatt.

#### 17.5.4.3 Empfehlungen für gutes sommerliches Raumklima

- Fensterflächenanteil begrenzen: f ≤ 18 % (Ost/West und Horizontalverglasungen besonders kritisch). Südfenster ab f > 30 % ohne Zusatzmaßnahmen problematisch.
- Außenliegende temporäre Verschattung: Jalousien, Raffstores, Rollläden — FC < 15 % möglich, windgesichert bis mind. 13 m/s. Universell einsetzbar (auch Ost/West/Horizontal).
- Zwischen-Scheiben-Verschattung (in Dreifachverglasung): Ähnliche Wirkung wie außen; FC minimal ca. 6 %; witterungs- und windgeschützt; FC-Normwerte jedoch deutlich schlechter als dieser Minimalwert.
- Innenliegende Verschattung: Reduziert nur direkten Energiedurchlass; indirekte Wärmeabgabe durch Absorption erhöht sich sogar. FC-Werte bei Dreifachverglasung:
  - heller Vorhang: FC ≈ 85 %
  - dichter weißer schwerer Vorhang: FC ≈ 70 %
  - speziell außen reflektierend beschichteter weißer Vorhang: FC ≈ 50 %
  - übliche innenliegende Jalousie: FC ≈ 75 %
  - optimierte rückreflektierende Jalousie: FC ≈ 60 %
  - dichter schwarzer Vorhang (Verdunklung): FC ≈ 90 %
  - metallbeschichtete Verdunklung: FC ≈ 40 % (Minimalwert innenliegender Vorrichtungen)
- Feststehende außenliegende Verschattungselemente (Südseite): Horizontale Überstände 50 cm → bereits wirksam. 1 m Überstandstiefe: > 50 % Sommerlast-Reduktion; 1,5 m: > 70 %. Auf Ost/West-Seiten wirkungslos (flacher Einfallswinkel).
- Verschattung durch Laubbäume: Sommerliche Transparenz für dahinter liegende Fassade z.B. 40 %, winterlich bis 68 %.
- Verringerung innerer Wärmelasten: Stromsparende Geräte, Flachbildschirme, effiziente IT, niedrige Standby-Verluste, automatische Regelungen des Kunstlichts. Faktor > 2 erreichbar, spart direkt Betriebskosten.
- Lüftung (wichtigste Maßnahme):
  - Kippfenster nachts gekippt: mehr als ein Kippfenster je ca. 12 m² Raumnutzfläche empfohlen. Kippwinkel im Sommer möglichst weit.
  - Hohe schmale Öffnungen besser als breite (Luftwechsel wächst mit h^(3/2)).
  - Querlüftung (gegenüberliegende Fassaden): hohe freie Luftwechsel.
  - Kaminwirkung durch Öffnungen auf verschiedenen Höhen; Dachentlüftungsöffnungen oder Entlüftungsturm steigern Wirkung. Zuluft idealerweise aus Untergeschoss oder durch erdverlegte Kaltluftkanäle.
  - Lüfter auf Fortluftseite platzieren (kein zusätzlicher Energieeintrag in Raum).
  - Glashäuser/Wintergärten: zwingend Fortluftöffnungen im obersten Bereich.
  - Berechnung natürlichen Luftwechsels: DIN EN 16798-7 (ehem. DIN EN 15242).
- Helle Außenoberflächenfarben: Verringern Außenoberflächentemperatur und Solarlastzufluss; erhöhen Albedo, senken Umgebungstemperatur. Heat-Island-Effekt: in dicht besiedelten Gebieten bis 2–4,5 K höhere Sommertemperaturen als ländliches Umfeld.
- Erhöhung wirksamer Wärmekapazität:
  - Speichernde Oberflächen nicht verdecken (keine abgehängten Decken, Holzverkleidungen, wärmedämmende Teppiche).
  - Hohe spez. Wärmekapazität: Vollziegel, Kalksandstein, Normalbeton, Zementsteine, Zementestrich, Lehmsteine, Lehmputze. Massivholz ebenfalls hoch, aber begrenzte Eindringtiefe (Nutzungszeit 10–14 h).
  - Gipskarton: geringer wirksam; doppelte Lage besser als einfache.
  - Massive Innenwände auch in Holzbauten bevorzugen; Geschossdecken mit Massivbaustoff statt Dämmstoff füllen.
- Vorsorgendes Kühlhalten: Im Frühsommer durch freie Lüftung niedrige Innentemperaturen halten; hohe Zeitkonstanten moderner gedämmter Gebäude ermöglichen dann kühles Innenklima auch in Hitzeperioden.

---

### 17.5.5 Wärmedämmstoffe

Wärmetransport erfolgt über drei Mechanismen: molekulare Wärmeleitung, Konvektion (Molekültransport), Wärmestrahlung. Messtechnisch wird die Wärmeleitfähigkeit λ als kombinierter Wert erfasst.

Gase leiten Wärme schlechter als Flüssigkeiten oder Feststoffe. Wärmedämmstoffe: λ < 0,1 W/(m·K); übliche luftbasierte Dämmstoffe: 0,03 bis 0,045 W/(m·K). Poren gefüllt mit Luft, CO₂ oder Pentan. Konvektionsunterdrückung und Strahlungsunterdrückung (Trübungsmittel) wichtig.

Nanoporöse Dämmstoffe: Porendurchmesser kleiner als freie Weglänge der Gasmoleküle; λ unter 0,027 W/(m·K) schon bei Normaldruck. Vakuum-Isolations-Paneele (VIP): 4–10-fach niedrigere λ als konventionelle Dämmstoffe. Stützmatrix: mikroporöse Kieselsäure, Mineralwollegewebe, Polystyrol- oder Polyurethanschäume. Bei 6 cm Dämmstärke U-Werte um 0,1 W/(m²·K) möglich. Preis ca. 50–100 €/m². Langzeitstabilität des Vakuums noch in Untersuchung. Schutz gegen Hüllenverletzung durch Einbau in vorgefertigte Bauteile empfohlen.

Feuchte Dämmstoffe leiten besser als trockene (Feuchtetransport mit Verdunstungs-/Kondensationsvorgängen). Wärmeleitfähigkeit nimmt mit Temperatur zu.

Porosierte Massivbaustoffe: Porenbeton, Porenziegelsteine, Leichtbetonsteine bis λ ≈ 0,07 W/(m·K) — für monolithische Konstruktionen mit U ≈ 0,14 W/(m²·K) geeignet.

**Dämmstoffarten nach europäischer Normung:**
- Mineralfaserdämmstoffe: EN 13162
- Expandierter Polystyrolschaum (EPS): EN 13163
- Extrudierter Polystyrolschaum (XPS): EN 13164
- Polyurethan-Hartschaum (PUR): EN 13165
- Phenolharzschaum (PF): EN 13166
- Schaumglas: EN 13167
- Holzwolledämmstoffe (WW): EN 13168
- Expandiertes Perlite (EPB): EN 13169
- Expandierter Kork (ICB): EN 13170
- Holzfaserdämmstoffe (WF): EN 13171

Wärmeleitfähigkeitsmessung an ebenen trockenen Platten nach EN 1946-2. Für Nachweise nur Bemessungswerte verwenden:
- Kategorie I: Nennwert × Sicherheitsfaktor 1,2
- Kategorie II: Bauaufsichtliche Zulassung, max. 5 % über Nennwert

Mindestanforderung Brandschutz: mindestens schwerentflammbar (Baustoffklasse B 1, DIN 4102-1: 1998-05).

Weitere relevante Eigenschaften: Festigkeitswerte, Brandverhalten (Feuerwiderstandsklassen), Formbeständigkeit.

**Anwendungskurzzeichen für Dämmbereiche (Tab. 17.22, Auszug):**

Dach/Decke: DAD (Außen unter Deckung), DAA (Außen unter Abdichtung), DUK (Umkehrdach), DZ (Zwischensparren), DI (Unterseite/abgehängt), DEO (unter Estrich ohne Schallschutz), DES (unter Estrich mit Schallschutz)

Wand: WAB (Außen hinter Bekleidung), WAA (Außen hinter Abdichtung), WAP (Außen unter Putz), WZ (zweischalig), WH (Holzrahmen-/Tafelbau), WI (Innen), WTH (Haustrennwand), WTR (Raumtrennwand)

Perimeter: PW (Wand gegen Erdreich außerhalb Abdichtung), PB (Bodenplatte gegen Erdreich außerhalb Abdichtung)

**Europäische Typkennzeichnung (Tab. 17.23):**

Druckbelastbarkeit: Dk (keine), Dg (gering, z.B. unter Estrich im Wohnbereich), Dm (mittel, nicht genutzte Dachflächen), Dh (hoch, genutzte Dachflächen), Ds (sehr hoch, Parkdeck/Industrieböden), Dx (extrem hoch)

Wasseraufnahme: Wk (keine, Innendämmung), Wf (durch flüssiges Wasser, Außenwand), Wd (durch flüssiges Wasser und/oder Diffusion, Perimeterdämmung/Umkehrdach)

Zugfestigkeit: Zk (keine, Hohlraumdämmung), Zg (gering, Außenwand hinter Bekleidung), Zh (hoch, Außenwand unter Putz)

Schalltechnische Eigenschaften: Sk (hohe Zusammendrückbarkeit, Trittschalldämmung — bei keinen Anforderungen), Sh/Sm/Sg (hohe/mittlere/geringe Zusammendrückbarkeit unter schwimmenden Estrich, Haustrennwand)

Verformung: Tk (keine, Innendämmung), Tf (Dimensionsstabilität unter Feuchte+Temperatur, Außenwand unter Putz), Tl (Dimensionsstabilität unter Last+Temperatur, Dach mit Abdichtung)

---

### Rechenwerte der Wärmeleitfähigkeit und Diffusionswiderstandszahlen (Tab. 17.22, DIN V 4108-4)

| Baustoff | Rohdichte (kg/m³) | λ (W/(m·K)) | μ (–) |
|---|---|---|---|
| Putzmörtel Kalk/Kalkzement/hydr. Kalk | 1800 | 0,87 | 15/35 |
| Zementmörtel, Zementestrich | 2000 | 1,4 | 15/35 |
| Leichtmörtel LM 21 | ≤700 | 0,21 | 15/35 |
| Wärmedämmputz (DIN 18550-3) | ≤200 | 0,060–0,100 | 5/20 |
| Normalbeton (DIN EN V 206) | 2400 | 2,1 | 70/150 |
| Bimsbeton (DIN 4232) | 800 | 0,24 | 5/15 |
| Porenbeton/Gasbeton (DIN 4223) | 600 | 0,19 | 5/15 |
| Wandbauplatten Gips (DIN 18163) | 900 | 0,41 | 5/10 |
| Wandbauplatten Porenbeton (DIN 4166) | 600 | 0,24 | 5/10 |
| Gipskartonplatten (DIN 18180) | 900 | 0,25 | 8 |
| Vollklinker, Hochlochklinker (DIN 105) | 2000 | 0,96 | 50/100 |
| Vollziegel, Hochlochziegel (DIN 105) | 1600 | 0,68 | 5/10 |
| Porenbeton-Plansteine PP (DIN 4165) | 350 | 0,14 | 5/10 |
| Kalksandsteine (DIN 106) | 1800 | 0,99 | 15/25 |
| Holzwolleleichtbauplatten (DIN 1101, d ≥ 25 mm) | 360–460 | 0,065–0,090 | 2/5 |
| Polystyrol-Partikelschaum EPS | ≥30 | 0,035–0,040 | 40/100 |
| Polystyrol-Extruderschaum XPS | ≥25 | 0,030–0,040 | 80/250 |
| Faserdämmstoffe (DIN 18165-1) | 8–500 | 0,035–0,050 | 1 |
| Schaumglas (DIN 18174) | 100–150 | 0,045–0,060 | prakt. dampfdicht |
| Fichte, Kiefer, Tanne | 600 | 0,13 | 40 |
| Sperrholz (DIN 68705-2 bis -4) | 800 | 0,15 | 50/400 |
| Span-Flachpressplatten (DIN 68761–63) | 700 | 0,13 | 50/100 |
| Poröse Holzfaserplatten (DIN EN 622-4) | ≤400 | 0,07 | 5 |
| Linoleum (DIN EN 548) | 1000 | 0,17 | – |
| Kunststoffbeläge/PVC | 1500 | 0,23 | – |
| Bitumendachbahnen (DIN 52128) | 1200 | 0,17 | 10000/80000 |
| Kunststoff-Dachbahnen PIB (DIN 16731) | – | – | 400000/1750000 |
| Polyethylen-Folien (d > 0,1 mm) | – | – | 100000 |
| Aluminiumfolien (d > 0,05 mm) | – | – | prakt. dampfdicht |
| Kunstharzputz | 1100 | 0,7 | 50/200 |
| Glas | 2500 | 0,8 | prakt. dampfdicht |
| Keramik und Glasmosaik | 2000 | 1,2 | 100/300 |
| Strohlehm | 2000 | 0,6 | 5/10 |
| Sedimentgesteine (Sandstein, Kalkstein, Schiefer) | 2600 | 2,3 | 40–1000 |

---

### 17.5.6 Wasserdampfdiffusion, Temperaturen an Bauteilen, Tauwasserbildung

**Grundbegriffe:**
- Wasserdampfpartialdruck pH₂O (in Pa): Anteil des Wasserdampfs am Gesamtluftdruck. Maximaler Partialdruck = Sättigungsdampfdruck ps; er hängt ausschließlich von der Temperatur ab.
- Bei 20 °C: bis 17,3 g/m³ Wasserdampf (ps = 2340 Pa)
- Bei 0 °C: nur 4,8 g/m³ (ps = 611 Pa)
- Relative Feuchte: φ = pH₂O / ps (in %)
- Tauwasser entsteht, wenn ungesättigter Wasserdampf auf die Taupunkttemperatur abgekühlt wird.

Sättigungsdampfdruck-Näherungsformel (DIN 4108-3):
- ps = a · ((b + θ) / 100)^n
  - für 0°C ≤ θ ≤ 30°C: a = 288,680 Pa, b = 1,098, n = 8,020
  - für -20°C ≤ θ ≤ 0°C: a = 4,689 Pa, b = 1,486, n = 12,300

Sättigungsdampfdruck-Tabelle (Tab. 17.24, DIN 4108-3) — Auswahl:

| θ (°C) | ps (Pa) | θ (°C) | ps (Pa) |
|---|---|---|---|
| +30 | 4244 | 0 | 611 |
| +25 | 3169 | -5 | 401 |
| +20 | 2340 | -10 | 260 |
| +15 | 1706 | -15 | 165 |
| +10 | 1228 | -20 | 103 |
| +5 | 872 | | |

**Tauwassergefährdung:**
- Schimmelpilzgefahr ab rel. Feuchte ≥ 80 % über 1–2 Wochen auf Bauteiloberfläche.
- Typische Entstehungsorte: schlecht gedämmte Bauteile und Wärmebrücken (Fensterstürze, auskragende Betonteile, Gebäudeaußenecken); unzureichend belüftete Räume, wenig beheizte Schlafzimmer, Bäder, Küchen bei hohen Feuchtelasten.
- Bester Schutz: gute Wärmedämmung — hohe Innenoberflächentemperaturen ausschlaggebend.
- Im Sommer: Kellerräume und Übergangszeiten ebenfalls gefährdet.

**Bemessungswerte der Wärmeübergangswiderstände (Tab. 17.18, DIN V 4108-4):**

| Bauteil | Rsi (m²·K/W) | Rse (m²·K/W) |
|---|---|---|
| Außenwand | 0,13 | 0,04 |
| Außenwand mit hinterlüfteter Außenhaut; Abseitenwand zu nicht gedämmtem Dachraum | 0,13 | 0,08 |
| Wohnungstrennwand, Wand zw. fremden Arbeitsräumen, Trennwand zu dauernd unbeheizten Räumen, Abseitenwand zu gedämmtem Dachraum | 0,13 | 0,13 |
| Wand an Erdreich | 0,13 | 0,00 |
| Decke/Dachschräge: Aufenthaltsraum nach oben gegen Außenluft | 0,13 | 0,04 |
| Decke unter nicht ausgebautem Dachraum, unter Spitzboden, unter belüftetem Raum | 0,13 | 0,08 |
| Wohnungstrenndecke, Wärmestrom von unten nach oben | 0,10 | 0,10 |
| Wohnungstrenndecke, Wärmestrom von oben nach unten | 0,17 | 0,17 |
| Kellerdecke | 0,17 | 0,17 |
| Decke: Aufenthaltsraum nach unten gegen Außenluft | 0,17 | 0,04 |
| Unterer Abschluss nicht unterkellerter Aufenthaltsraum an Erdreich | 0,17 | 0,00 |

Vereinfachung zulässig: Rsi = 0,13 m²·K/W in allen Fällen; Rse = 0,04 m²·K/W bei Außenwänden und Trennwänden. Für Tauwasserberechnungen nach Glaser-Verfahren gelten abweichende Werte (DIN 4108-3).

#### 17.5.6.1 Temperaturverhältnisse in und an Bauteilen

Rechengang nach DIN 4108 (vereinfacht mit konstanten Lufttemperaturen innen/außen):
- Innenoberflächentemperatur: θsi = θi − U·(θi − θe)·Rsi
- Grenzflächentemperaturen der Einzelschichten: θj = θj-1 − U·(θi − θe)·(dj/λj)
- Außenoberflächentemperatur: analog mit Rse

Für einfache Tauwasserberechnungen nach DIN 4108-3 (nicht-klimatisierte Wohn- und Bürogebäude):
- Innenluft: 20 °C
- Außenluft: -5 °C (aktuell: 90 Tage bei -5 °C); ältere Fassung 2001: -10 °C Außentemperatur

Für Tauwasserberechnungen festgelegte Wärmeübergangswiderstände (DIN 4108-3, A.2.3):
- Raumseitig: Rsi = 0,25 m²·K/W (ungünstige Verhältnisse abdeckend, kaum Konvektion)
- Außenseitig: Rse = 0,04 m²·K/W (an Außenluft); 0,08 m²·K/W (an belüftete Luftschichten); 0 m²·K/W (an Erdreich)
- Innere Bauteile beidseitig: Rsi

**Rechenbeispiel (Tab. 17.25):** Außenwand mit Kalkzementputz (15 mm) / Leichthochlochziegel-Mauerwerk (240 mm, λ = 0,21 W/(m·K)) / Kalkzementputz (20 mm):
- R = 0,844 m²·K/W; U = 0,986 W/(m²·K)
- Innen: θi = 20 °C, pi = 1521 Pa (φi = 65 %)
- Außen: θe = -10 °C, pe = 208 Pa (φe = 80 %)
- Innere Oberflächentemperatur: θsi = 16,1 °C
- Grenzfläche nach Putz 1: θ₁ = 15,5 °C
- Grenzfläche nach Mauerwerk: θ₂ = -8,1 °C → ps = 306 Pa
- Außenoberflächentemperatur: θse = -8,8 °C → ps = 289 Pa

#### 17.5.6.2 Das Glaser-Verfahren

Nicht der Temperaturverlauf, sondern der Sättigungsdampfdruckverlauf ps entlang des Querschnitts ist entscheidend für Tauwassergefahr. Diffusionsstrom und Wärmestrom folgen analogen Gesetzen.

**Diffusionswiderstandszahl μ:** μ = δLuft / δBaustoff — gibt an, wie viel schlechter ein Baustoff Wasserdampf leitet als gleich dicke ruhende Luftschicht. Kleine μ-Werte (nahe 1): diffusionsoffene poröse Dämmstoffe. Hohe μ-Werte: diffusionsdichte Schichten.

**Äquivalente Luftschichtdicke:** sd = μ · d (in m). Gibt die Dicke einer gleichwertigen Luftschicht an. Gesamt für mehrschichtiges Bauteil: sd = μ₁·d₁ + μ₂·d₂ + ... + μₙ·dₙ

Klassifizierung:
- sd ≤ 0,5 m: diffusionsoffen
- sd ≥ 1500 m: diffusionsdicht (echte Dampfsperre)
- Übliche PE-Folie 0,25 mm: sd = 200 m

**Glaser-Diagramm:** Dampfdruckverlauf über äquivalente Luftschichtdicken aufgetragen (Abszisse = Diffusionswiderstand). Verbindungsgerade von pi zu pe zeigt rechnerischen Druckverlauf. Wo diese Gerade die ps-Kurve berührt oder überschreitet: Kondensationszone.

Normwerte für Dampfdrücke Winter (DIN 4108-3):
- Innen: pi = ps(20°C) · 50 % = 2340 · 0,5 = 1170 Pa
- Außen: pe = ps(-5°C) · 80 % = (ca. 401) · 0,8 ≈ 321 Pa
(ältere Fassung 2001: pe = ps(-10°C) · 80 % = 260 · 0,8 = 208 Pa)

Tauwassermenge mW,T = (gi − ge) · tT (kg/m²)
- gi = Dampfstrom von innen bis Kondensationszone
- ge = Dampfstrom von Kondensationszone nach außen
- tT = Dauer der Tauwasserperiode (in Stunden)

Grenzwerte (DIN 4108-3):
- Tauwassermenge je Wintersaison: max. 1,0 kg/(m²·a) bei Dach- und Wandkonstruktionen
- An Grenzflächen mit kapillar nicht wasseraufnahmefähigen Schichten (Luftschicht, wasserdurchlässige Schicht): max. 0,5 kg/m²
- Keine schädigende Feuchteerhöhung in Holz/Holzbaustoffen (DIN 68800-2; 6.4; DIN 4108-3)
- Verdunstungsmenge im Sommer muss Tauwassermenge übertreffen

Verdunstungsperiode (DIN 4108-3, 2001): θi = θe = 12 °C, φi = φe = 70 % → pi = pe = 982 Pa; Dauer: 90 Tage (tV = 2160 h). Wandkonstruktion trocknet nach beiden Seiten aus.

Wenn sd < 0,1 m (nach ISO 12572): Wert sd = 0,1 m ansetzen.

**Regeln zur Tauwasserminderung:**
- Außendämmung: erhöht Bauteiltemperatur im kritischen Bereich, vermeidet Kondensat
- Innendämmung und äußere dampfbremsende Schichten (Klinker, Metallbleche, Kunststoffverkleidungen außen): erhöhen Tauwasserrisiko
- Allgemeine Regel: sd-Werte sollen zur Außenseite hin abnehmen, Wärmedurchlasswiderstände d/λ sollen zur Außenseite hin zunehmen
- Dampfsperren können Austrocknung behindern: bei Holzbau und belüftungslosen Dachkonstruktionen besonders sorgfältig prüfen; trockene Baumaterialien Pflicht

**Bauteile ohne Tauwassernachweis (DIN 4108-3: 2001-07, Abschn. 4.3):**
- Mauerwerk (DIN 1053-1), Normalbeton (DIN EN 206-1/1045-2), Leichtbeton (DIN 4219, DIN 4232) mit Innenputz und: Außenputz DIN 18550-1; Bekleidungen DIN 18515-1/-2 (Fugenanteil ≥ 5 %); hinterlüftete Bekleidungen DIN 18516-1; Außendämmung nach DIN 1102, DIN 18550-3 oder zugelassenem WDVS
- Außenwände mit Innendämmung (R ≤ 1,0 m²·K/W) und sd,i ≥ 0,5 m der Innenbekleidung incl. Dämmung
- Holzbauart-Wände mit innenseitiger Dampfbremse (sd,i ≥ 2,0 m)
- Holzfachwerkwände mit Luftdichtheitsbahn und diversen Dämm-Varianten
- Unbelüftete Dächer: wenn ≤ 20 % von R unterhalb diffusionshemmender Schicht liegt und bestimmte sd-Kombinationen eingehalten sind (z.B. sd,e ≥ 0,3 m und sd,i ≥ 6·sd,e; oder sd,i ≥ 100 m unterhalb Dämmschicht)
- Belüftete Dächer mit ausreichend sd,i und konstruktiv gesicherter Belüftung (Traufenöffnung ≥ 2‰ Dachfläche, ≥ 200 cm²/m Traufenlänge; Satteldach: Lüftungsöffnungen ≥ 0,5‰ und ≥ 50 cm²/m)

Fälle, bei denen Nachweis erforderlich: z.B. innengedämmte Wände mit sd,i < 0,5 m; Holzbau-Wände mit sd,i < 2 m; belüftete Flachdächer (Neigung < 5°) mit sd,i < 100 m.

**Feuchtekonvektion:** Viele Tauwasserschäden entstehen nicht durch Diffusion, sondern durch Konvektion feuchter Innenluft durch Undichtheiten. Tauwassermengen durch Konvektion weit über Diffusionswerte. Hohe Luftdichtheit daher aus bautenschutztechnischen und energietechnischen Gründen zwingend erforderlich.

**Sparrenvolldämmung:** Günstig für Feuchteverhalten, wenn ausreichend dampfdurchlässige Unterspannbahn vorhanden. Dampfdichte Unterdächer (z.B. bei Schieferdeckung) bei Vollsparrendämmung über Jahre problematisch.

**Schimmelpilzbildung:** Keine notwendige Bedingung Tauwasser auf Oberfläche. Bei porösen Materialien kann Kapillarkondensation bei rel. Feuchte ~80 % auf Bauteiloberfläche Schimmelpilzwachstum ermöglichen. Bei θi = 20 °C und φi = 50 % entspricht das bereits Oberflächentemperaturen unter 12,6 °C. Schimmelpilz benötigt zusätzlich organische Nahrung (Staub) und Zeit (> 1 Woche). Erste Schimmelbildung oft in Übergangszeiten, nicht im Winter.

---

#### 17.5.6.3 Innendämmung

Außendämmung ist generell unkritisch: verbessert Behaglichkeit, trocknet das Mauerwerk, reduziert Wärmebrückenproblematik. Innendämmung erfordert besondere Sorgfalt.

**Voraussetzungen für Innendämmung (Sanierungsfall):**
- (A) Aufsteigende Feuchte muss zuerst beseitigt werden (Horizontalsperren o.Ä.)
- (B) Bei Schlagregenbeanspruchungsgruppe III: wasserabweisende Fassade zwingend. Gruppen I und II: Außenputz/Fassade mindestens intakt (wasserhemmend). Erst wenn Schlagregenschutz gesichert und aufsteigende Feuchte beseitigt, ist Innendämmung sinnvoll.

**Planungsziele:**

(1) Luftdichtheit: Dämmkonstruktion raumseitig dauerhaft luftdicht (Hinterströmung mit Innenluft verhindert massive Auffeuchtung der alten Wandkonstruktion). Zielwert: q50 < 0,6 m³/m²/h — entspricht Passivhaus-Luftdichtheitsstandard. Vereinzelte Nägel/Schrauben bis 3 mm Durchmesser unkritisch; mehr als 8 Löcher je m² (7 mm² je Verletzung) wären erst schadensträchtig.

(2) Wärmebrückenreduktion: An allen Anschlusspunkten müssen Temperaturen bei -5 °C Außentemperatur auf mindestens 12,5 °C begrenzt bleiben. Kritische Punkte:
- Fensterlaibungen: Begleitdämmung bis Rahmen mit ≥ 20 mm zwingend
- Geschossdecken Beton: Oberseite Trittschalldämmung (~25 mm) ausreichend; Unterseite Dämmkeil erforderlich
- Einmündende Innenwände: Begleitdämmungen, Dämmkeile, Temperaturleitbleche als Lösung möglich

**Dampfdiffusionsschutz-Konzepte:**

Konzept DB (Dampfbremse):
- Raumseitige Dampfbremse behindert Diffusion zur kalten alten Wandkonstruktion. Mindestwert: sd,eff ≥ 10 m (effektiver Diffusionswiderstand des Gesamtaufbaus inkl. Nebenwege). „Echte Dampfsperre": sd,eff ≥ 100 m — erfordert spaltfrei durchgehende Bahn und Abklebung wie bei Passivhaus-Luftdichtheitsbahn.
- Voraussetzung: keine aufsteigende Feuchte, keine Schlagregenproblematik, keine Baufeuchte in der Wand.
- Feuchteadaptive Dampfbremsen erhöhen Toleranz gegenüber Belastungen etwas.
- Simulationsergebnisse: 1 mm breiter Spalt/m² in Dampfbremse (luftdicht überdeckt durch Gipskartonplatte) ist bei Mineralwolledämmung grenzwertig; bei EPS-Dämmung unkritisch.
- Parallelschaltung von Diffusionswiderständen: harmonisches Mittel anwenden, nicht flächengewichtetes arithmetisches Mittel.

Konzept KA (Kapillaraktive Dämmstoffe):
- Diffusionsoffener, aber luftdichter Aufbau mit kapillaraktivem Dämmstoff. Eindiffundierender Wasserdampf wird im Material sorbiert und durch Flüssigwassertransport in Richtung geringerer Materialfeuchte (d.h. nach innen) weitergeleitet — Rücktransport gegen den Dampfstrom. Erfordert verifizierte Materialeigenschaften (Feuchtespeicherfunktion, Flüssigwassertransport, μ-Wert, Wasserresistenz, λ). Hydrophobierende Zusätze können die Wirkung zerstören.
- Simulationsresultate über mehrere Jahre: bei wasserabweisenden Außenputzen (Gruppe III) bzw. wasserhemmenden (Gruppen I/II) gleichwertig zu Dampfbremsen-Lösung.
- Innenseitig diffusionsoffene Verkleidungen möglich: qualifizierte OSB-Platten (an Stößen abgeklebt), Gipswerkstoffplatten (an Stößen abgeklebt), Innenputze vollflächig aufgetragen und luftdicht angeschlossen.
- Schädlich bei beiden Konzepten: kaltseitig der Innendämmlage ganzflächig dampfbremsende Beschichtungen (Ölfarben, Alu-Tapeten, Metallbleche) — vor Dämmungsanbringung entfernen.

**Energiepotenziale Innendämmung:**
- Unkritische Dämmstoffstärken bei konventionellen Dämmstoffen: 4–10 cm
- Nominale U-Werte Außenwand bei guter Innendämmung: 0,25–0,35 W/(m²·K)
- Effektive Ueff-Werte (inkl. Wärmebrückenwirkung): 0,33–0,5 W/(m²·K) — deutlich höher als bei Außendämmung
- Wärmebrückenzuschlag UWB bei sonstiger guter Planung: 0,08–0,15 W/(m²·K)
- Altbau ohne Dämmung: ca. 240 kWh/(m²·a). Mit Innendämmung + Passivhauskomponenten: ca. 55 kWh/(m²·a) (Faktor ~4). Mit Außendämmung + Passivhauskomponenten: Faktor ~10 möglich.

---

### 17.5.7 Wärmebrücken

#### 17.5.7.1 Allgemeines

**Definition:** Wärmebrücken sind Bereiche in Bauteilen, in denen der Wärmestrom nicht eindimensional verläuft — Isothermen sind nicht mehr parallel. In der Regel schlechterer Wärmeschutz als Umgebung; manchmal auch reduzierter Verlust. Mögliche Folgen: Tauwasser, Rissbildung, Schimmelpilz.

**Typen:**
- Geometrische Wärmebrücken: Außenecken/-kanten in Massivbauten
- Materialbedingte Wärmebrücken: Material mit hoher λ in Bereich mit niedriger λ

Beschreibung durch:
- Längenbezogener Wärmebrückenverlustkoeffizient ψ (W/(m·K)): für linienhafte Wärmebrücken (Gebäudekanten, Bauteilanschlüsse, Fensterlaibungen)
- Punktbezogener Wärmedurchgangskoeffizient χ (W/K): für lokale Wärmebrücken (Dübel für Außenbauteile)

Berechnungsnormen: DIN EN ISO 10211-1+2.

Gesamter Wärmestrom durch Außenflächen:
- Q̇ = (ΣᵢAᵢ·Uᵢ + Σₖlₖ·ψₖ + Σⱼχⱼ) · Δθ
  - Ai: Außenflächen (m²)
  - Ui: U-Werte ebener Bauteile
  - lk: Längen linearer Wärmebrücken (Außenmaß)
  - ψk: lineare WBV-Koeffizienten
  - χj: punktförmige WBV-Koeffizienten

#### 17.5.7.2 Einfluss auf den Energiebedarf (GEG-Anforderungen)

Drei Methoden der Wärmebrückenberücksichtigung:
1. Genaue Berücksichtigung nach DIN EN ISO 10211-1/-2, DIN EN ISO 10077-1, DIN EN ISO 13370 aus Wärmebrückenkatalogen oder Rechenprogrammen; geometrische WB können negativ sein.
2. Normierte wärmebrückenverringerte Konstruktionen (DIN 4108 Bbl 2 2019): Pauschalzuschlag UWB = 0,03 bzw. 0,05 W/(m²·K) nach DIN V 18599.
3. Pauschalzuschlag UWB = 0,10 W/(m²·K) ohne Nachweis — benachteiligt wärmebrückenarme Konstruktionen stark.
4. Wärmebrückenfreies Konstruieren: UWB = 0,0 W/(m²·K) bei Nachweis der Einhaltung der Kriterien.

Bei zunehmender Dämmstärke: absoluter Wärmebrückenverlust kann konstant bleiben, prozentualer Anteil steigt; Berücksichtigung wird wichtiger.

#### 17.5.7.3 Wärmebrückenfreies Konstruieren

**Definition:** Gebäudehülle ist wärmebrückenfrei, wenn Transmissionswärmeverlust mit allen Wärmebrücken nicht höher als bei Berechnung nur mit regulären U-Werten über die Außenflächen.

Formales Kriterium:
- Σ(ψᵢ·lᵢ) + Σ(χⱼ) ≤ 0 → UWB ≤ 0

Vereinfachtes Kriterium: für alle linearen Störungen ψ ≤ 0,01 W/(m·K) und ΣXⱼ/AHülle ≤ 0,01 W/(m²·K).

Praktisches Werkzeug: Gesamte Außenhülle muss mit einem Stift der maßstäblichen Mindest-Dämmdicke (~200 mm beim Passivhaus) ohne Absetzen innerhalb der Dämmschichten umfahren werden können.

**Beispiel:** Mauerwerks-Fußpunkt auf wärmegedämmter Bodenplatte (Abb. 17.73): Wenn Fußpunktstein λ < 0,25 W/(m·K) (Porenbetonstein), dann ψ ≤ 0,01 W/(m·K) → wärmebrückenfrei. Mit normalen Steinen (λ > 0,8 W/(m·K)): erhebliche Wärmebrückenverluste. Geringe Zusatzkosten, immer lohnend bei Neubau.

#### 17.5.7.4 Einfluss auf Bauteiltemperaturen

Temperaturfaktor fRsi (DIN EN ISO 10211-1):
- fRsi = (θsi − θe) / (θi − θe)
- θsi = fRsi · (θi − θe) + θe

Bewertung:
- fRsi = 1: Innenoberflächentemperatur = Innenlufttemperatur (kein Verlust)
- fRsi = 0: Innenoberflächentemperatur = Außenlufttemperatur
- fRsi ≥ 0,70: Mindestanforderung zur Schimmelpilzverhinderung bei θe = -10 °C und normalen Innenklimabedingungen → entspricht θsi ≈ 12,6 °C
- fRsi > 0,9 für hohe thermische Behaglichkeit wünschenswert
- θsi < 13 °C (f < 0,76): Kapillarkondensationsgefahr und Schimmelpilzrisiko bei φi > 50 %

Typische Wärmebrücken mit kritischen Innenoberflächentemperaturen: Fensterrahmen, Fensterstürze, Fensterlaibungen, Außenecken/-kanten, breite Mauerwerksfugen.

Beispiel massive Gebäudeaußenecke: Bei θe = 0 °C, θi = 20 °C sinkt θsi auf 12,1 °C → Schimmelgefahr bei mäßig gedämmten Wänden.

#### 17.5.7.5 Beispiele beachtlicher Wärmebrücken

Zur Analyse werden zweidimensionale Temperaturfeld-Computerprogramme eingesetzt (Isothermen-Darstellungen, Wärmeflusslinien). Wärmebrückenkataloge geben ψ-Werte und fRsi-Werte für typische Details an.
