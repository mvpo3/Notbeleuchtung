# Lehrbuch der Bauphysik — Teil 15
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 601-640.

Dieser Teil behandelt ausschließlich das Kapitel 21 „Raumakustik" und deckt die Themen Schallabsorbertypen (poröse Absorber, Plattenresonatoren, Helmholtzresonatoren, mikroperforierte Absorber), Schallreflektoren und Diffusoren, Schallausbreitung im Raum, raumakustische Anforderungen nach DIN 18041:2016 sowie die Systematik der raumakustischen Planungspraxis ab.

## Inhalt

### 21.2.1 Poröse Schallabsorber

Poröse Schallabsorber aus Fasermaterialien oder offenzelligen Schaumstoffen bilden einen großen Anteil der am Bau eingesetzten Absorber. Typische Ausführungsformen sind Teppichböden, Vorhänge, Filze, Vliese auf abgehängten Decken, Stellwände und Wandabsorber. Schallwellen dringen in das Porengefüge ein und werden durch Reibung in Wärme umgewandelt (dissipative Absorption). Das Absorberskelett gilt als ortsfest; Skelettschwingungen bleiben bei dieser Betrachtung unberücksichtigt.

**Kenngrößen und Modellierung:**
- Maßgebliche Materialkenngröße ist der längenbezogene Strömungswiderstand Ξ [Ns/m⁴]
- Zur Berechnung der Wandimpedanz benötigt man die komplexe Ausbreitungskonstante Γ und den Wellenwiderstand Za des Absorbermaterials
- Empirische Modelle nach Delany/Bazley, erweitert durch Mechel/Grundmann, liefern Γ und Za in Abhängigkeit des dimensionslosen Parameters C = f/Ξ:
  - Für C < 60 (hochfrequenter Bereich): eigene Gleichungen für Γ und Za (Gl. 21.11 / 21.12)
  - Für C ≥ 60 (tieffrequenter Bereich): andere Gleichungssätze (Gl. 21.13 / 21.14)
- Wellenzahl k₀ = 2π/λ, Schallkennimpedanz der Luft Z₀ = ρc

**Wandimpedanz und Absorptionsgrad:**
- Poröser Absorber der Dicke d vor schallharter Wand: Z₁ = Za · coth(Γd) — Gl. 21.15
- Höhere Schallabsorptionsgrade erst bei hohen Frequenzen; Verschiebung zu mittleren Frequenzen durch größere Materialdicke d möglich
- Für tieffrequente Absorption sind sehr große und baulich unübliche Materialdicken notwendig
- Strömungswiderstand Ξ beeinflusst ebenfalls den Absorptionsgradsverlauf bei konstantem d

**Absorber mit Wandabstand:**
- Vor schallharter Wand nimmt die Schallschnelle den Wert null an → Material direkt an der Wand trägt wenig bei
- Lösung: poröse Schicht dünner ausführen + Luftspalt lw zwischen Absorber und Wand belassen
- Vorteile: geringerer Materialeinsatz, Belüftung verhindert Tauwasser an kalten Außenwänden
- Wandimpedanz mit Luftspalt (senkrechter Schalleinfall) nach Mechel: kombinierende Formel aus Absorber- und Luftspaltimpedanz (Gl. 21.16 / 21.17)
- Für 100 mm Gesamtaufbau: Verteilung zwischen Absorbermaterial und Luftspalt beeinflusst den Frequenzgang

**Stoffbespannung als Sonderfall:**
- Anstelle eines Absorbers mit Dicke d kann eine Stoffbespannung (Strömungswiderstand R des Materials, nicht Ξ) verwendet werden
- Wandimpedanz ergibt sich aus R, akustischer Masse m′ und Impedanz des Luftraums hinter der Bespannung (Gl. 21.18)

**Deckschichten bei porösen Absorbern:**
- Mineralwolle, offenzellige Schäume, Filze erfüllen ästhetische und mechanische Anforderungen oft nicht allein
- In der Praxis werden schützende Deckschichten verwendet: Stoffkaschierungen oder Lochbleche
- Deckschicht-Strömungswiderstand sollte möglichst gering sein, um den Schallabsorptionsgrad nicht zu beeinflussen
- Bei dünnen Lochblechen wird ab einem Lochflächenanteil von etwa 25 % eine ausreichende akustische Transparenz erzielt
- Dünne Folien als Rieselschutz für Mineralwolle müssen sehr dünn sein, da ansonsten ein Plattenresonator entsteht

### 21.2.2 Plattenresonatoren

Für die tieffrequente Schallabsorption, wo poröse Absorber ungeeignet sind, kommen Resonanzabsorber zum Einsatz, bei denen Masse-Feder-Systeme schwingen.

**Aufbau:**
- Leichte Platte (flächenbezogene Masse m′₁) als Vorschaltmasse
- Luft- oder Dämmstofffeder (dynamische Steifigkeit s′)
- Schwerere rückseitige Platte (Masse m′₂) oder schallharte Wand

**Resonanzfrequenz:**
- Allgemein: f₀ = (1/2π) · √[s′ · (1/m′₁ + 1/m′₂)] — Gl. 21.19
- Vereinfacht (wenn m′₂ >> m′₁): f₀ = (1/2π) · √(s′/m′₁) — Gl. 21.20
- Bei Luftfeder der Dicke lw: s′ = ρc²/lw — Gl. 21.21

**Wandimpedanz eines Plattenresonators** (biegeweiche Vorschaltmasse + Dämmstofffeder):
- Z₁ = jωm′₁ + Za · coth(Γd) — Gl. 21.22
- Ergebnis: selektiver Absorber mit ausgeprägtem Maximum bei der Resonanzfrequenz f₀

**Eigenschaften:**
- Auch bei geringer Aufbaudicke sind hohe Schallabsorptionsgrade im tieffrequenten Bereich erreichbar
- Plattenresonatoren ergänzen poröse Absorber ideal: Letztere wirken bei mittleren und hohen Frequenzen, Plattenresonatoren bei tiefen
- Biegesteife Platten erzeugen zusätzliche Biegeeigenschwingungen neben der Resonanz f₀ und liefern geringere Schallabsorptionsgrade als biegeweiche Varianten → in der raumakustischen Planung möglichst biegeweiche Vorschaltmassen verwenden

### 21.2.3 Helmholtzresonatoren

Statt schwingender Platten können Luftmassen in Schlitzen oder Löchern gegen Luftvolumina schwingen und bei Resonanzfrequenz hohe Absorption liefern.

**Grundprinzip:**
- Steifigkeit der Luftfeder: s′ = ρc² · S²/V — Gl. 21.23 (S = Halsquerschnittsfläche, V = rückwärtiges Luftvolumen)
- Schwingende Luftmasse setzt sich zusammen aus Halsmasse mh und Mündungskorrekturen Δd an den Öffnungen innen und außen (Gl. 21.24)
- Resonanzfrequenz: f₀ = (c/2π) · √[S / (V · (d + Δdi + Δda))] — Gl. 21.25

**Mündungskorrekturen (Überschlagsformeln nach Fasold):**
- Runde Löcher mit Radius r: Δdi = Δda = 2r — Gl. 21.26
- Quadratische Löcher mit Kantenlänge a: Δdi = Δda = 2a/π — Gl. 21.27
- Bei Schlitzen sind die Mündungskorrekturen frequenzabhängig

**Anordnung und Wirkung:**
- Eckplatzierung im Raum ermöglicht Vervielfachung der äquivalenten Schallabsorptionsfläche A aufgrund des hohen Schalldrucks in Kanten und Ecken bei modalen Schallfeldern
- Flächenhafte Anordnung vieler Resonatoren (gelochte/geschlitzte Platten) bewirkt gegenseitige Verstimmung → breitbandigere Absorption
- Praktische Ausführungen: perforierte Holzpaneele, Gipskartonlochplatten
- Bei nicht kassettierten Hohlräumen hinter Lochplatten: hohe Absorption nur bei senkrechtem Schalleinfall
- Für hohe Absorption auch bei schrägem Einfall: Luftschicht in Einzelvolumen kassettieren (lokal wirksam)

### 21.2.4 Mikroperforierte Absorber

Sonderform der Helmholtzresonatoren mit sehr geringem Lochflächenanteil und Lochdurchmessern im Sub-Millimeterbereich.

**Physikalisches Prinzip:**
- Hydraulischer Lochdurchmesser so klein, dass laminare Strömung entsteht
- Absorption beruht wesentlich auf Reibung der Luftmoleküle untereinander
- Grenzschichtparameter k = (d/4) · √(ωρ/η) — Gl. 21.31 (η = 1,789 · 10⁻⁵ kg/(ms), dynamische Viskosität von Luft)
- Mikroperforation: Grenzschichtparameter k liegt zwischen 1 und 10

**Wandimpedanz einer mikroperforierten Platte:**
- Berechnet aus akustischem Reibungswiderstand r′ + Plattenimpedanz jωm′ + Luftspaltimpedanz jZ₀ cot(k₀lw) — Gl. 21.28
- Reibungswiderstand r′ nach Maa (Gl. 21.29) und akustisch wirksame Masse m′ nach Maa (Gl. 21.30) sind funktionen von Plattendicke t, Lochdurchmesser d, Lochflächenanteil σ und Grenzschichtparameter k

**Baupraktische Hinweise:**
- Erstmals im Plenarsaal des Deutschen Bundestages in Bonn eingesetzt (in transparente Acrylglasscheiben eingebracht → transparente Schallabsorber)
- Wegen hoher Herstellungskosten gebohrter Platten werden heute meist dünne Folien oder Holzplatten genadelt → günstigere Herstellung

### Nachhallzeitberechnung — Beispiel Seminarraum (Tab. 21.4, DIN 18041:2016)

Beispiel eines vollständig durchgerechneten Seminarraums:

| Raumgeometrie | Wert |
|---|---|
| Breite | 5,0 m |
| Länge | 8,0 m |
| Höhe | 3,2 m |
| Volumen (Netto) | 128 m³ (Objektvolumen 2,25 m³) |
| Nutzung | Unterricht/Kommunikation |
| Temperatur | 20 °C |
| Soll-Nachhallzeit Tsoll,A3 | 0,50 s |

**Schallabsorptionsgrade α der Bauteilflächen nach Oktavband (Hz):**

| Bauteil | 125 | 250 | 500 | 1k | 2k | 4k |
|---|---|---|---|---|---|---|
| Parkett auf Beton | 0,02 | 0,03 | 0,04 | 0,05 | 0,05 | 0,06 |
| Gipskartonwand | 0,15 | 0,12 | 0,10 | 0,08 | 0,07 | 0,06 |
| Glatter Beton | 0,01 | 0,01 | 0,01 | 0,02 | 0,02 | 0,03 |
| Rasterdecke Glasfaser, lw = 200 mm | 0,30 | 0,50 | 0,60 | 0,71 | 0,89 | 0,81 |
| Glasfassade | 0,12 | 0,08 | 0,05 | 0,04 | 0,03 | 0,02 |
| Türen aus Holz | 0,14 | 0,10 | 0,08 | 0,08 | 0,08 | 0,08 |

**Äquivalente Schallabsorptionsflächen A [m²] der Bauteilflächen:**

| Bauteil (Fläche) | 125 | 250 | 500 | 1k | 2k | 4k |
|---|---|---|---|---|---|---|
| Parkett auf Beton (40,0 m²) | 0,80 | 1,20 | 1,60 | 2,00 | 2,00 | 2,40 |
| Gipskartonwand (52,6 m²) | 7,89 | 6,31 | 5,26 | 4,21 | 3,68 | 3,16 |
| Glatter Beton (15,0 m²) | 0,15 | 0,15 | 0,15 | 0,30 | 0,30 | 0,45 |
| Rasterdecke 200 mm Abhängehöhe (25,0 m²) | 7,50 | 12,50 | 15,00 | 17,75 | 22,25 | 20,25 |
| Glasfassade (25,6 m²) | 3,07 | 2,05 | 1,82 | 1,02 | 0,77 | 0,51 |
| Türen aus Holz (5 m²) | 0,70 | 0,40 | 0,40 | 0,40 | 0,40 | 0,40 |

**Sonstige äquivalente Absorptionsflächen:**

| Objekt | 125 | 250 | 500 | 1k | 2k | 4k |
|---|---|---|---|---|---|---|
| Einfache Polsterstühle, 30 Stück | 4,50 | 7,50 | 9,00 | 10,50 | 15,00 | 19,50 |
| Tische, 15 Stück, 0,15 m³ | 4,23 | 4,23 | 4,23 | 4,23 | 4,23 | 4,23 |
| Luftabsorption (20 °C, φ = 50 %) | 0,05 | 0,15 | 0,30 | 0,50 | 0,86 | 2,06 |

**Resultierender Nachhallzeitverlauf [s] nach DIN EN 12354-6:2004:**

| Frequenz | 125 | 250 | 500 | 1k | 2k | 4k |
|---|---|---|---|---|---|---|
| Toleranz oben | 0,73 | 0,60 | 0,60 | 0,60 | 0,60 | 0,60 |
| Toleranz unten | 0,33 | 0,40 | 0,40 | 0,40 | 0,40 | 0,33 |
| Berechnete Nachhallzeit | 0,70 | 0,59 | 0,54 | 0,50 | 0,41 | 0,38 |

### 21.2.5 Schallabsorptionsgradkenngrößen (Tab. 21.5)

Verschiedene Kenngrößen aus unterschiedlichen Regelwerken zur Beschreibung von Schallabsorbern:

| Kenngrößenform | Bedeutung | Ermittlung |
|---|---|---|
| α₀(f) nach DIN EN ISO 10534-1/-2:2001 | Frequenzabhängiger Absorptionsgrad für senkrechten Einfall, in Terzen oder schmalbandiger | Messung im Impedanzrohr |
| αs(f) nach DIN EN ISO 354:2003 | Frequenzabhängiger Absorptionsgrad für statistischen Einfall, in Terzen oder Oktaven | Hallraummessung |
| Praktischer Schallabsorptionsgrad αp nach DIN EN ISO 11654:1997 | Grundlage für αw | Mittelung der Terzwerte → gerundete Oktavwerte (Vielfaches von 0,05; αp ≤ 1,00) |
| Bewerteter Schallabsorptionsgrad αw nach DIN EN ISO 11654:1997 | Einzahlangabe für einfacheres Verständnis | Verschiebung Bezugskurve; Summe der Überschreitungen ≤ 0,15; αw = Bezugskurvenwert bei 500 Hz |
| NRC nach ASTM C423 | Einzahlangabe | Mittelwert der Terzwerte bei 250 / 500 / 1000 / 2000 Hz, gerundet auf Vielfaches von 0,05 |
| Schallabsorptionsgradklassen nach DIN EN ISO 11654:1997 | Klassenangabe für einfacheres Verständnis | A: 0,90 < αw ≤ 1,00 / B: 0,80 < αw ≤ 0,85 / C: 0,60 < αw ≤ 0,75 / D: 0,30 < αw ≤ 0,55 |
| Formindikatoren | Zusatzinformation zum Frequenzgang | L (tieffrequente), M (mittelfrequente), H (hochfrequente) Überschreitung der Bezugskurve um > 0,25 |

**Hinweis:** Für das Grundverständnis der Raumakustik sind die frequenzabhängigen Absorptionsgradverläufe αs(f) wesentlicher als die Einzahlkennwerte.

### 21.3 Schallreflektoren

#### 21.3.1 Geometrische Reflexion an Reflektoren

Geneigte Platten über Bühnen oder an Wänden lenken Schall in bestimmte Bereiche. Zwei Anforderungen:
1. Ausreichende Schallhärte bei den relevanten Frequenzen → Schall wird reflektiert und nicht absorbiert
2. Mindestgröße, damit keine Beugung um den Reflektor erfolgt

**Grenzfrequenz zwischen diffuser und geometrischer Reflexion** (nach Fasold):

f_g = c · √[(l² + s · e · 2cosθ) / (2 · l · s · e)] — Gl. 21.32

wobei l = kürzere Seite des Reflektors, s = Abstand Sender–Reflektor, e = Abstand Reflektor–Empfänger, θ = Schalleinfallswinkel

**Flatterechos:**
- Entstehen zwischen parallelen schallharten Flächen; beeinträchtigen Nutzbarkeit erheblich
- Vermeidungsmaßnahmen:
  - Schallabsorber (sofern Nachhallzeitanforderungen dies erlauben), positioniert in jeder Raumachse
  - Schräge Flächen mit Neigungswinkel > 5° gegenüber der parallelen Ebene
  - Auffaltung schallharter Flächen (Strukturierung); Strukturgröße muss Kriterium aus Gl. 21.32 erfüllen

#### 21.3.2 Diffuse Reflexion — Schroeder-Diffusoren

Breitbandig diffuse Reflexion erfordert eine stochastische Verteilung der Wandimpedanzen, was in der Praxis kaum direkt realisierbar ist. Lösung: pseudostochastische λ/4-Resonatoren-Anordnungen nach Schroeder.

**Prinzip:**
- Ein Wandstreifen, dem ein zurückspringender Streifen benachbart ist, erzeugt bei einer Wellenlänge λ = viermal der Streifentiefe eine Phasendrehung um π
- Mehrere nebeneinander angeordnete Streifen unterschiedlicher Tiefe erzeugen ein Phasengitter → Ablenkung der reflektierten Schallwellen
- Phasengitter wirken nur in einem begrenzten Frequenzbereich (bei Phasenverschiebung 2π geht der Effekt verloren)

**Quadratic Residue Diffusoren (QRD):**
- Meistverbreitete Schroeder-Diffusor-Variante
- Zahlenfolge: Sn = n² mod P (n = ganze Zahl, P = Primzahl) — Gl. 21.33
- Designfrequenz (Frequenzbereich ±1 Oktave um fD mit maximaler Streuung):
  fD = c · Sn,max / (2 · ln,max) — Gl. 21.34 (Sn,max = höchster Wert der Zahlenfolge, ln,max = maximale Bautiefe)

**Beispiel QRD auf Basis Primzahl P = 7 (Tab. 21.6):**
- Designfrequenz fD = 500 Hz, Streifenbreite d = λ/P = 98 mm

| Index n | n² | Sn (n² mod 7) | Bautiefe ln [m] |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0,049 |
| 2 | 4 | 4 | 0,196 |
| 3 | 9 | 2 | 0,098 |
| 4 | 16 | 2 | 0,098 |
| 5 | 25 | 4 | 0,196 |
| 6 | 36 | 1 | 0,049 |
| 7 | 49 | 0 | 0 (Periode beginnt neu) |

**Einschränkung:** Große Bautiefe bei manchen Anwendungen problematisch; Lochplattenresonatoren bei geringerer Bautiefe als Alternative (nach Hunecke). Achtung: Wandstrukturen mit QRD können teils hohe Schallabsorptionsgrade aufweisen, was bei Reflektoren unerwünscht ist.

#### 21.3.3 Schallschirme in Räumen

Schallschirme reduzieren Pegel zwischen Sender und Empfänger durch Beugungsabschirmung.

**Einflussfaktoren auf erreichbare Pegelminderung:**
- Abstände Quelle–Schirm und Schirm–Empfänger
- Effektive Schirmhöhe
- Wellenlänge (größere Wellenlängen beugen stärker um die Schirmkante)

**Abschirmmaß im Freien** (nach Kurze/Nürnberger):
- Dz = 10 lg[(3 + 40z/λ)] — Gl. 21.35 (z = Umweg des Schalls gegenüber direktem Weg)

**Abschirmmaß im Raum** (reduziert wegen Mehrfachbeugung und Wandreflexionen):
- Dz,r = 10 lg[(1 + 20z/λ)] — Gl. 21.36
- Beide Formeln nur gültig, wenn Schallschirm innerhalb des Hallradius der Schallquelle liegt

### 21.4 Schallausbreitung in Räumen

#### 21.4.1 Raumimpulsantwort

Die Raumimpulsantwort beschreibt das zeitliche Verhalten der Schallausbreitung an einem bestimmten Empfangspunkt als Reaktion auf einen ausgesendeten Impuls. Sie enthält:
- Zeitliche Information (Eintreffen von Direktschall und Reflexionen)
- Frequenzinformation (via Fourier-Transformation ermittelbar)

Messung oder Berechnung durch raumakustische Simulationsprogramme. Starke Reflexionen und deren zeitliche Lage sind aus der Impulsantwort ablesbar.

**Wahrnehmungsschwelle:** Das menschliche Gehör kann Reflexionen innerhalb von ca. 50 ms nach Direktschalleintreffen nicht zeitlich auflösen → diese stärken die Deutlichkeit. Reflexionen nach > 50 ms werden als Einzelecho wahrgenommen und mindern die Deutlichkeit.

#### 21.4.2 Raumakustische Parameter

**Deutlichkeitsgrad D50** (nach DIN EN ISO 3382-1:2009):
- D50 = [∫₀⁵⁰ᵐˢ p²(t)dt] / [∫₀∞ p²(t)dt] × 100 % — Gl. 21.37
- Kriterium: Verhältnis der Schallenergie in den ersten 50 ms zur Gesamtenergie
- Angabe in Prozent; hohe Werte = hohe Sprachverständlichkeit
- Zielwert für Sprachdarbietungen: D50 > 50 %

**Sprachübertragungsindex STI** (nach DIN EN ISO 9921:2004 und DIN EN IEC 60268-16:2021):
- Bewertet Sprachverständlichkeit über akustische und elektroakustische Übertragungskanäle
- Wertebereich 0 bis 1
- Berechnung über Modulationsübertragungsfunktionen (Schwankung des Sprachsignals als Hauptmerkmal)
- Berücksichtigt Nachhall, Störgeräusche und elektroakustische Verzerrungen
- STI > 0,5: ausreichende Sprachverständlichkeit; STI > 0,7: hohe Sprachverständlichkeit

**Klarheitsmaß C80** (nach DIN EN ISO 3382-1:2009, für Musik):
- C80 = 10 lg{[∫₀⁸⁰ᵐˢ p²(t)dt] / [∫₈₀ᵐˢ∞ p²(t)dt]} [dB] — Gl. 21.38
- Verhältnis Schallenergie in ersten 80 ms zu danach eintreffender Energie
- Höhere Werte = höhere Klarheit in der Musikwahrnehmung

### 21.5 Raumformen

#### 21.5.1 Günstige Raumgeometrien

**Kleine Räume:**
- Laufwegdifferenzen bleiben unter 17 m (entspricht < 50 ms Zeitunterschied) → detaillierte Analyse von D50 und C80 i. d. R. entbehrlich
- Flatterechos durch keine parallel gegenüberstehenden schallharten Flächen vermeiden
- Sekundärstruktur (Absorber, Diffusoren) oder Neigung schallharter Flächen um mindestens 5° als Gegenmaßnahme
- Raumabmessungen (Länge, Breite, Höhe) sollten kein ganzzahliges Verhältnis zueinander haben → Eigenfrequenzen fallen sonst zusammen (modal)

**Große Räume:**
- Kein modales Schallfeld im relevanten Frequenzbereich → Eigenmoden kein Problem
- Wichtig: Verteilung der reflektierenden Flächen für gute Deutlichkeit/Klarheit an möglichst vielen Empfangsplätzen
- Für hohes Klarheitsmaß: ausreichend Reflexionen innerhalb der ersten 80 ms; entspricht maximalem Schallumweg von 27 m
- Aus dieser Bedingung ergibt sich indirekt ein maximales Raumvolumen je Nutzung → erklärt warum Konzertsäle meist unter 25.000 m³ bleiben
- Möglichst viele seitliche Schallreflexionen für gute Räumlichkeit (zeitlich und räumlich optimales Schallfeld)

**Volumenkennzahlen und maximale Volumina (Tab. 21.7) nach Fasold/Veres und DIN 18041:2016:**

| Nutzung | Volumenkennzahl K [m³/Sitzplatz] | Maximales Volumen V [m³] |
|---|---|---|
| Seminarräume | 3 bis 5 | 1.000 |
| Sprechtheater, Hörsäle | 4 bis 6 | 5.000 |
| Mehrzwecksäle (Sprache + Musik) | 4 bis 7 | 8.000 |
| Kammermusiksäle | 6 bis 10 | 10.000 |
| Konzertsäle für sinfonische Musik | 8 bis 12 | 25.000 |
| Sprache (DIN 18041:2016) | 4 bis 6 | — |
| Musik und Sprache (DIN 18041:2016) | 6 bis 8 | — |
| Musik (DIN 18041:2016) | 7 bis 12 | — |

**Raumakustische Kenndaten ausgewählter Konzertsäle (Tab. 21.8):**

| Konzertsaal | V [m³] | Sitzplätze | K [m³/Platz] | T [s] (besetzt, mittlere Freq.) | C80 [dB] (unbesetzt) |
|---|---|---|---|---|---|
| Concertgebouw Amsterdam | 18.780 | 2.037 | 9,2 | 2,0 | −3,3 |
| Philharmonie Berlin | 24.500 | 2.220 | 11,0 | 1,9 | −0,5 |
| Großer Saal Musikverein Wien | 15.000 | 1.680 | 8,9 | 2,0 | −3,7 |
| Großer Saal Tonhalle Zürich | 11.400 | 1.546 | 7,4 | 1,6 | −3,6 |
| Beethovensaal Liederhalle Stuttgart | 16.000 | 2.000 | 8,0 | 1,6 | −0,2 |

#### 21.5.2 Gekrümmte Flächen

- Konkave Kreisbögen: führen zu Schallbündelung und Brennpunktbildung → in Konzertsälen und ähnlichen Räumen grundsätzlich zu vermeiden
- Konvexe Flächen: fächern Schallstrahlen auf → können Schallversorgung in bestimmten Bereichen beeinträchtigen, erzeugen aber keine Brennpunkte
- Konkave Flächen können eingesetzt werden, wenn diffuse Reflexion gewünscht ist
- **Flüstergalerie:** Phänomen in runden Räumen bei streifendem Schalleinfall; Schall wird an der Wand entlanggeführt (St.-Pauls-Kathedrale London); auch sehr leise Schalle unmittelbar an der Wand können in großer Entfernung wiederum wandnah deutlich wahrgenommen werden

### 21.6 Raumakustische Anforderungen

#### 21.6.1 Soll-Nachhallzeiten nach DIN 18041:2016

Die DIN 18041:2016 unterscheidet Räume der **Gruppe A** (Hörsamkeit über große Entfernungen) und **Gruppe B** (Hörsamkeit über geringe Entfernungen).

**Gruppe A — Soll-Nachhallzeit Tsoll nach Nutzung und Volumen V [m³]:**

- Musik (A1), V = 30–1.000 m³: Tsoll,A1 = 0,45 · lg(V/m³) − 0,07 — Gl. 21.39
- Sprache/Vortrag (A2), V = 50–5.000 m³: Tsoll,A2 = 0,37 · lg(V/m³) − 0,14 — Gl. 21.40
- Unterricht/Kommunikation (A3), V ≤ 1.000 m³: Tsoll,A3 = 0,32 · lg(V/m³) − 0,17 — Gl. 21.41
- Sprache/Vortrag inklusiv (A4), V ≤ 5.000 m³: Tsoll,A4 = 0,32 · lg(V/m³) − 0,17 — Gl. 21.42
- Unterricht/Kommunikation inklusiv (A5), V = 30–500 m³: Tsoll,A5 = 0,26 · lg(V/m³) − 0,14 — Gl. 21.43
- Sport (A6), V = 200–10.000 m³: Tsoll,A6 = 0,75 · lg(V/m³) − 1,00 — Gl. 21.44
- Sport (A6), V > 10.000 m³: Tsoll,A6 = 2,0 s — Gl. 21.45

Toleranzbereiche: Nachhallzeitverhältnis (berechnete Nachhallzeit dividiert durch Tsoll) muss innerhalb vorgegebener frequenzabhängiger Grenzen liegen (Abb. 21.22 und 21.23 in der Quelle).

**Räume der Gruppe B — Raumbedämpfungsempfehlungen (A/V-Verhältnis):**

Kriterium: Verhältnis äquivalenter Schallabsorptionsfläche A zu Raumvolumen V in Abhängigkeit der Raumhöhe h.

| Nutzungsart | Raumbeispiele | Formel bei h ≤ 2,5 m | Formel bei h > 2,5 m |
|---|---|---|---|
| B1 | Eingangshallen, Treppenhäuser (keine Aufenthaltsqualität) | keine Anforderung | keine Anforderung |
| B2 | Schalterhallen, Verkehrsflächen mit Aufenthaltsqualität | A/V ≥ 0,15 | A/V ≥ (4,80 − 4,69 lg h) — Gl. 21.46 |
| B3 | Kantinen, Schulpausenräume, Verkehrsflächen | A/V ≥ 0,20 | A/V ≥ (3,13 − 4,69 lg h) — Gl. 21.47 |
| B4 | Ausgabebereiche Kantine, Bürgerbüro, Mehrpersonenbüro | A/V ≥ 0,25 | A/V ≥ (2,13 − 4,69 lg h) — Gl. 21.48 |
| B5 | Speiseräume in Schulen/Krankenhäusern, Großküchen, Leitstellen, Spielflure Kita | A/V ≥ 0,30 | A/V ≥ (1,47 − 4,69 lg h) — Gl. 21.49 |

#### 21.6.2 Mehrpersonenbüros — Raumakustik-Klassen nach VDI 2569:2019

Mehrpersonenbüros werden zunächst B4 zugeordnet, erfordern aber oft detailliertere Betrachtung. In großen Mehrpersonenbüros ist hauptsächlich Sprache anderer Personen störend; hier sollte Schallpegelabnahme mit der Entfernung groß sein.

Kenngrößen nach VDI 2569:2019 (Entwurf):
- Nachhallzeit T
- Störschalldruckpegel bauseitiger Geräusche LNA,Bau
- A-bewerteter Sprachschalldruckpegel in 4 m Abstand Lp,A,S,4m
- Räumliche Abklingrate von Sprache bei Abstandsverdopplung D2,S

**Raumakustik-Klassen für große Mehrpersonenbüros (Tab. 21.9):**

| Klasse | Charakterisierung | T (125 Hz) | T (250 Hz–4 kHz) | LNA,Bau | Schallausbreitungsstufe 1 (2/3 Pfade) Lp,A,S,4m / D2,S | Schallausbreitungsstufe 2 (rest. Pfade) Lp,A,S,4m / D2,S |
|---|---|---|---|---|---|---|
| A | hoher Aufwand, gut für Call Center + kommunikationsintensive Nutzung | 0,4–0,8 s | 0,4–0,6 s | ≤ 35 dB(A) | ≤ 47 dB / ≥ 8 dB | ≤ 49 dB / ≥ 6 dB |
| B | mittlerer Aufwand, für Call Center + Vertrieb/Konstruktion/Verwaltung | 0,4–0,9 s | 0,4–0,7 s | ≤ 40 dB(A) | ≤ 49 dB / ≥ 6 dB | ≤ 51 dB / ≥ 4 dB |
| C | geringer Aufwand, für Vertrieb/Konstruktion/Verwaltung | 0,4–1,1 s | 0,4–0,9 s | ≤ 40 dB(A) | ≤ 49 dB / ≥ 6 dB (1/3 der Pfade) | ≤ 51 dB / ≥ 4 dB (restl. Pfade) |

Zusätzliches Kriterium für Mehrpersonenbüros: STI ≤ 0,5 anstreben (ab diesem Wert deutliche Zunahme kognitiver Leistungsfähigkeit). DIN EN ISO 3382-3:2012 definiert Ablenkungsabstand rD (STI = 0,5) und Vertraulichkeitsabstand rP (STI = 0,2).

### 21.7 Raumakustische Planung

#### 21.7.1 HOAI-Rahmen

Raumakustik gehört gemäß HOAI 2021 (Anlage 1) zu den Beratungsleistungen. Honorarzoneneinteilung nach Schwierigkeitsgrad:

| Honorarzone | Beispielräume |
|---|---|
| I | Pausenhallen, Spielhallen, Liege- und Wandelhallen (sehr geringe Anforderungen) |
| II | Unterrichts-, Vortrags-, Sitzungsräume bis 500 m³; Filmtheater + Kirchen bis 1.000 m³; Großraumbüros (geringe Anforderungen) |
| III | Unterrichts-, Vortrags-, Sitzungsräume 500–1.500 m³; Filmtheater + Kirchen 1.000–3.000 m³; teilbare Turn- und Sporthallen bis 3.000 m³ (durchschnittlich) |
| IV | Mehrzweckhallen bis 3.000 m³; Filmtheater + Kirchen über 3.000 m³ (hohe Anforderungen) |
| V | Konzertsäle, Theater, Opernhäuser; Mehrzweckhallen > 3.000 m³; Tonaufnahmeräume; Räume mit veränderlichen akustischen Eigenschaften; akustische Messräume (sehr hohe Anforderungen) |

**Leistungsphasen der raumakustischen Planung:**
- LP 1: Grundlagenermittlung, raumakustische Anforderungen festlegen
- LP 2: Mitwirkung Vorplanung, Gesamtkonzept + Rechenmodelle
- LP 3: Mitwirkung Entwurfsplanung
- LP 4: Mitwirkung Genehmigungsplanung, raumakustischer Nachweis
- LP 5: Mitwirkung Ausführungsplanung, Koordination Fachplanungen
- LP 6: Mitwirkung Vorbereitung Vergabe, Beiträge zu Ausschreibungsunterlagen
- LP 7: Mitwirkung Vergabe, Angebotsprüfung

**Besondere Leistungen:**
- Fachübergreifender Bauteilkatalog
- Raumakustische Simulationsrechnungen
- Raumakustische Messungen
- Modelluntersuchungen
- Planung elektroakustischer Anlagen
- Mitwirkung bei Audits/Zertifizierungen

#### 21.7.2 Räume mit hohen Schallpegeln (Industriehallen, Werkstätten)

Planungsschritte:
1. Recherche/Bestimmung der Schallleistungspegel der Schallquellen
2. Belegung möglicher Flächen mit Schallabsorbern
3. Berechnung äquivalenter Schallabsorptionsfläche und zu erwartender Schalldruckpegel
4. Erarbeitung weiterer pegelsenkender Maßnahmen

Falls nach raumakustischen Maßnahmen die zulässigen Expositionsschallpegel nach LärmVibrationsArbSchV an Arbeitsplätzen nicht eingehalten werden: geeigneter Gehörschutz ist zu tragen.

**Musikübungsräume und Orchestergräben:**
- Widerstreitende Ziele: gute Nachhallzeit für Musik ↔ Lärmschutz der Musiker
- Große Abstände, kurze Nachhallzeiten und leise Spielweise würden Pegel senken, widersprechen aber musikalischen Anforderungen
- Instrumentenschallleistungspegel, die in großen Konzertsälen ausreichende Lautstärke sichern, führen in kleinen Proberäumen zwangsläufig zu sehr hohen Schalldruckpegeln
- Kompromiss: etwas kürzere Nachhallzeiten als musikalisch optimal + Schallschirme zwischen Musikern + bei Bedarf individueller Musikergehörschutz mit nahezu linearem Frequenzgang

#### 21.7.3 Räume für Musik

Planungsschritte:
1. Volumenkennzahlen und Toleranzbereich nach DIN 18041:2016 bzw. ISO/DIS 23591:2020 bestimmen
2. Sinnvolle Volumenkennzahl für die Kategorie ermitteln
3. Primärstruktur festlegen
4. Sekundärstruktur festlegen
5. Bei großen Räumen: strahlengeometrische Konstruktionen von Hand auf Plänen
6. Bei großen Räumen: raumakustische Computersimulationen oder Modellmessungen
7. Schallabsorbierende Flächen festlegen

Längere Soll-Nachhallzeit als für Sprache; geringer Anstieg der Nachhallzeit bei tiefen Frequenzen (Tiefenwärme) erwünscht; möglichst viele seitliche Reflexionen zu den Zuhörern.

**Tonstudios und Abhörräume:**
- Gehören nicht zu Musikräumen im Sinne DIN 18041:2016
- Eher kürzere Nachhallzeiten erforderlich; besondere Herausforderung bei tiefen Frequenzen
- DIN 15996:2020 bei besonderen Gleichmäßigkeitsanforderungen beachten; Einhaltung nur durch baubegleitende Messungen + Feinjustierung sicherstellbar

#### 21.7.4 Räume für Sprache (Besprechungsräume, Klassenräume, Hörsäle)

Planungsschritte:
1. Nutzung bestimmen, Soll-Nachhallzeit gemäß DIN 18041:2016 festlegen
2. Mögliche Konfliktbereiche identifizieren (z.B. thermisch sinnvolle unverkleidete Betondecke vs. Akustik)
3. Flächen mit geeigneten Schallabsorbern belegen (gleichmäßige Verteilung auf alle Raumachsen vorteilhaft) + frequenzabhängige Nachhallzeiten berechnen
4. Bei großen Räumen: geeignete Schallreflektoren für hohen Deutlichkeitsgrad

#### 21.7.5 Mehrpersonenbüros

Widerspruch: Zu niedrige Bedämpfung → hohe Sprachverständlichkeit über große Distanzen = stört. Zu starke Bedämpfung → zwar geringere Halligkeit, aber auch geringerer Grundgeräuschpegel → Verbesserung der Sprachverständlichkeit. Störgeräusche und Nachhallzeit sollten daher nicht zu gering sein.

Planungsschritte:
1. Mitwirkung beim Zonierungskonzept + Festlegung Raumakustik-Klasse nach VDI 2569:2019
2. Konfliktbereiche identifizieren (z.B. thermisch sinnvolle Betondecke)
3. Mitwirkung Einrichtungskonzept + Positionierung schallschirmender Maßnahmen; Schallabsorber oder schallabsorbierende Möbel
4. Mitwirkung bei Mitarbeiterbeteiligung
5. Geeignete Messpfade in Abhängigkeit von Bürogröße und Arbeitsplatzanzahl festlegen
6. Akustische Kenngrößen berechnen: Nachhallzeit, räumliche Abklingrate D2,S, Sprachschalldruckpegel Lp,A,S,4m in 4 m Abstand, Ablenkungsabstand rD
7. Entscheidung über Sound-Masking-Systeme unter Mitarbeiterbeteiligung

Sound-Masking-Systeme: senden informationsarme Schalle aus und senken Sprachverständlichkeit; in Deutschland wenig akzeptiert, möglichst zu vermeiden.

#### 21.7.6 Kirchen

- Widerstreitende Anforderungen: Sprachverständlichkeit für Predigt (kurze Nachhallzeit) und Orgelmusik/Chorgesang (lange Nachhallzeit)
- Kompromiss je nach Gemeindeprioritäten notwendig
- Evangelische Kirchen (Untersuchung Schweizer Kirchen): tendenziell etwas kürzere Nachhallzeiten als katholische Kirchen
- Umgestaltung historischer Kirchenräume: besonderes Augenmerk auf Beibehaltung oder bewusste Änderung der Raumakustik; Vorabstimmung mit allen Beteiligten

#### 21.7.7 Planungswerkzeuge

- **Einfache Räume** (Besprechungsraum, handelsübliche Absorber): Taschenrechner oder Tabellenkalkulationsprogramm ausreichend; Soll-Nachhallzeit und frequenzabhängige Nachhallzeiten berechenbar
- **Kleine Räume oder tieffrequente Anforderungen** (z.B. Tonstudio-Abhörraum): Eingeschränkte Berechnungsmöglichkeiten; Planung durch baubegleitende Messungen absichern; Justiermöglichkeiten früh einplanen
- **Große Räume:** Computersimulationsprogramme auf Basis geometrischer Raumakustik; Schallstrahlen-Methode (Ray-Tracing) berechnet Raumimpulsantworten für jeden Empfängerplatz → daraus raumakustische Parameter; Anwendung auch für Mehrpersonenbüros (Schalldruckpegelverteilung, STI-Verteilung)
- **Modellmesstechnik:** Maßstabsgetreuer verkleinerter Raum + frequenzangepasste Absorber; misst Raumimpulsantworten an Modellsitzplätzen; kann Welleneffekte berücksichtigen (Vorteil gegenüber Ray-Tracing); erheblicher Aufwand (Nachteil)

#### 21.7.8 Unsicherheiten bei der raumakustischen Planung

- Hallraummessungen liefern Absorptionsgrade bei diffusem Schallfeld → im realen Raum kaum vergleichbare Diffusität erreichbar
- Ray-Tracing in Computersimulationen vernachlässigt Wellencharakter (keine Beugung, keine Interferenz)
- Schallabsorptionsgrade aus Hallraummessungen (statistischer Einfall) als Eingabedaten für Winkel-abhängige Reflexionen in Simulationen sind nur grobe Näherung
- Empfehlung: Unsicherheiten kennen, verschiedene Verfahren kombinieren, baubegleitende Messungen durchführen und akustische Maßnahmen feinjustieren

### Normverweise und Regelwerke (vollständig aus diesem Teil)

| Norm | Inhalt |
|---|---|
| ASTM C423:2009 | Schallabsorptionsgrad-Messung im Hallraum |
| DIN 15996:2020-12 | Arbeitsplatz in Bild-/Tonbearbeitung, Film/Video/Rundfunk |
| DIN 18041:2016-03 | Hörsamkeit in Räumen — Anforderungen, Empfehlungen, Planung |
| DIN EN 12354-6:2004-04 | Schallabsorption in Räumen (Berechnung aus Bauteileigenschaften) |
| DIN EN IEC 60268-16:2021-10 | Sprachübertragungsindex STI — Objektive Bewertung |
| DIN EN ISO 354:2003-12 | Schallabsorptionsmessung im Hallraum |
| DIN EN ISO 3382-1:2009-10 | Raumakustikparameter — Aufführungsräume |
| DIN EN ISO 3382-2:2008-09 | Nachhallzeit in gewöhnlichen Räumen |
| DIN EN ISO 3382-3:2012-05 | Raumakustikparameter — Großraumbüros |
| DIN EN ISO 9921:2003 | Sprachkommunikation — Ergonomische Beurteilung |
| DIN EN ISO 10534-1:2001-10 | Schallabsorptionsgrad im Impedanzrohr — Stehwellenverhältnis |
| DIN EN ISO 10534-2:2001-10 | Schallabsorptionsgrad im Impedanzrohr — Übertragungsfunktion |
| DIN EN ISO 11654:1997-07 | Schallabsorber in Gebäuden — Bewertung |
| DIN ISO 20189:2020-12 | Stellwände und Objekte — Absorption und Dämmung |
| ISO/DIS 23591 (Entwurf 2020-04) | Raumakustische Qualitätskriterien für Musikproberäume |
| VDI 2569:2019-10 | Schallschutz und akustische Gestaltung in Büros |
| LärmVibrationsArbSchV 2007 | Schutz der Beschäftigten vor Lärm und Vibrationen |
| HOAI 2021, Anlage 1 | Einordnung Raumakustik als Beratungsleistung; Honorarzonen |
