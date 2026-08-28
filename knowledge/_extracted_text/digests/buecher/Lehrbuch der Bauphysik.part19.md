# Lehrbuch der Bauphysik — Teil 19
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 761-800.

Dieser Teil behandelt die physikalischen Grundlagen der Lichttechnik (Kapitel 26): Strahlungsphysik, photometrische Grundgrößen, Rechenverfahren zur Lichtverteilung im Raum (Interreflexion, Formfaktoren), grafische und computergestützte Berechnungsmethoden sowie physiologische Wahrnehmungsphänomene (Adaptation, Blendung, Farbmetrik).

## Inhalt

### Wiensches Verschiebungsgesetz und Farbtemperatur (Kap. 26.2.2)

- Je höher die Temperatur eines Temperaturstrahlers, desto kurzwelliger (höherfrequent) liegt das Maximum seiner Spektralverteilung.
- Die Sonne hat eine Oberflächentemperatur von ca. 5900 K; ihr Abstrahlmaximum liegt bei ca. 500 nm (sichtbares Grün) — daher ist Tageslicht sehr effizient hinsichtlich des Verhältnisses Licht zu Gesamtstrahlung.
- Eine Glühlampe hat ihr Abstrahlmaximum bei ca. 2700 K, entsprechend ca. 1100 nm — außerhalb des sichtbaren Bereichs im infraroten Bereich. Folge: Glühlampen geben überwiegend Wärme ab, ihr Lichtwirkungsgrad ist gering.
- Kurzwelliges (hochfrequentes) Licht wird als kühl/bläulich empfunden, langwelliges (niederfrequentes) als warm/rötlich.
- Die Lage des Abstrahlmaximums des jeweiligen Temperaturstrahlers dient als Klassifizierungsmerkmal für den Farbton einer Lichtquelle: die sogenannte Farbtemperatur.

### Grundgrößen der Lichttechnik — Überblick (Kap. 26.3)

Strahlungsphysikalischen Größen stehen analoge lichttechnische Größen gegenüber:

| Strahlungsgröße | Einheit | Lichttechnische Größe | Einheit |
|---|---|---|---|
| Strahlungsleistung Φe | W | Lichtstrom Φv | Lumen lm = cd·sr |
| Strahlungsenergie Qe | W·s | Lichtmenge Qv | lm·s |
| Spezifische Ausstrahlung Me | W·m⁻² | Spez. Lichtabstrahlung Mv | lm·m⁻² |
| Strahlstärke Ie | W·sr⁻¹ | Lichtstärke Iv | Candela cd |
| Strahldichte Le | W·sr⁻¹·m⁻² | Leuchtdichte Lv | cd·m⁻² |
| Bestrahlungsstärke Ee | W·m⁻² | Beleuchtungsstärke Ev | Lux lx = lm·m⁻² |
| Bestrahlung He | W·m⁻²·s | Belichtung Hv | lm·m⁻²·s |
| Strahlungsausbeute ηe | % | Lichtausbeute ηv | lm·W⁻¹ |
| Transmissionsgrad τe, Reflexionsgrad ρe, Absorptionsgrad αe | % | τv, ρv, αv | % |

### Photometrisches Strahlungsäquivalent Km und V(λ)-Kurve (Kap. 26.3.1)

- Voraussetzung für Lichtwahrnehmung: elektromagnetische Strahlung muss auf der Netzhaut einen photoelektrischen Lichtreiz auslösen — nur für bestimmte Wellenlängen möglich.
- Das Auge besitzt die größte Helligkeitsempfindlichkeit bei 555 nm (540 THz); dieses Maximum dient als Referenzpunkt.
- Die frequenzabhängige relative Helligkeitsempfindung wurde experimentell an großen Probandengruppen ermittelt und in der Hellempfindlichkeitskurve V(λ) (dimensionslos, Maximum = 1) standardisiert.
- Es existieren zwei Kurven: V(λ) für photopisches Sehen (Tagsehen) und V'(λ) für skotopisches Sehen (Nachtsehen). In der Photometrie wird überwiegend V(λ) verwendet.
- Die Candela (cd) ist die einzige physikalische Grundgröße der Photometrie. Definition: Eine Strahlungsquelle, die monochromatisches Licht der Frequenz 540 THz aussendet und in einer bestimmten Richtung eine Strahlstärke von 1/683 W·sr⁻¹ aufweist, hat in dieser Richtung eine Lichtstärke von 1 cd.
- Daraus ergibt sich das photometrische Strahlungsäquivalent für Tagsehen: Km = 683 cd·sr·W⁻¹.
- Für das Nachtsehen berechnet sich analog: K'm = 1700 cd·sr·W⁻¹.
- Alle photometrischen Grundgrößen Xv berechnen sich aus den strahlungsphysikalischen Größen Xe über: Xv = Km · ∫₀^∞ Xe(λ) · V(λ) · dλ.

### Lichtstrom (Kap. 26.3.2)

- Der Lichtstrom Φ [Lumen, lm] ist die gesamte in den Raum abgegebene Lichtleistung (Lichtenergie pro Zeit), gewichtet mit der Hellempfindlichkeitskurve V(λ) und multipliziert mit Km.
- Er ist ein integraler Wert über den gesamten Umraum ohne Richtungsdifferenzierung.
- Anschaulich: Eine Punktlichtquelle in einer umschließenden Kugel — durch jede Kugelform fließt derselbe Gesamtlichtstrom, unabhängig vom Kugelradius. Die Flussdichte [lm/m²] nimmt mit 1/r² ab, da die Kugeloberfläche mit 4·π·r² zunimmt.

### Lichtmenge (Kap. 26.3.3)

- Die Lichtmenge Qv [lm·s] ist Lichtstrom mal Zeit; bei nicht-konstantem Lichtstrom das Zeitintegral.

### Raumwinkel (Kap. 26.3.3.1)

- Der Raumwinkel ω [Steradiant, sr] ist die zentrale Größe aller lichttechnischen Berechnungen.
- Definition: Wird auf der Oberfläche einer Kugel mit Radius r eine geschlossene Fläche A = r² mit dem Kugelmittelpunkt verbunden, so beträgt der entstehende Raumwinkel ω = 1 sr.
- Allgemeine Berechnung: ω = A/r² [sr = m²/m²].
- Die Form der Fläche A und der Kugelradius spielen keine Rolle; nur das Verhältnis A/r² ist maßgeblich.
- Der vollständige Raumwinkel der Kugel (Vollkugel) beträgt 4π ≈ 12,566 sr; der Halbraum (Hemisphäre) 2π ≈ 6,283 sr.
- Für beliebig orientierte Flächen zählt nur die Projektion der Fläche auf die Kugeloberfläche (der von einem Kugelmittelpunkt aus sichtbare Umriss).

### Lichtstärke (Kap. 26.3.4)

- Die Lichtstärke I [Candela, cd] beschreibt den Lichtstrom in eine bestimmte Richtung.
- Definition: I [cd] = Φ [lm] / ω [sr]; bei gegebenem Raumwinkel von 1 sr entspricht 50 cd einer Lichtabgabe von 50 lm.
- Differenziell: I = dΦ/dω; Φ ist die Stammfunktion von I.
- Die Lichtstärke beschreibt die richtungsabhängige Intensitätsverteilung einer Lichtquelle.

### Leuchtdichte (Kap. 26.3.5)

- Die Leuchtdichte L [cd/m² = lm/(sr·m²)] ist die Lichtstärke einer Fläche in eine bestimmte Richtung, bezogen auf die in diese Richtung projizierte Fläche.
- Formel: L(ε) = I(ε) / (A₀ · cos ε), wobei ε der Winkel zwischen Flächennormale und Abstrahlrichtung ist.
- Die projizierte Fläche A(ε) = A₀ · cos ε.
- Die Leuchtdichte gilt für selbst leuchtende und lichtreflektierende Flächen.
- Für Raumoberflächen werden bei lichttechnischen Berechnungen i.d.R. ideal lichtstreuende (matte) Eigenschaften angenommen.
- Die Leuchtdichte ist das Maß für die wahrgenommene Helligkeit von Flächen.

#### Lambertscher Strahler (Kap. 26.3.5.1)

- Ein ideal lichtstreuender (matter) Strahler sieht aus allen Richtungen gleich hell aus.
- Bedingung: Die Abstrahlcharakteristik folgt dem Cosinusgesetz: I(ε) = I₀ · cos ε (Lambertsches Gesetz).
- Eingesetzt in die Leuchtdichte-Formel: L(ε) = I₀·cos ε / (A₀·cos ε) = I₀/A₀ = L₀ — die Leuchtdichte ist also richtungsunabhängig und konstant.
- Begründung: Die mit zunehmendem Winkel ε abnehmende Lichtstärke wird exakt durch die gleichzeitig scheinbar kleiner werdende projizierte Fläche kompensiert.
- Vergleich realer Messungen mit dem Lambertschen Modell zeigt hohe Übereinstimmung, auch weil viele Reflexionsgänge die Lichtverteilung nivellieren.

### Spezifische Lichtabstrahlung (Kap. 26.3.6)

- Die spezifische Lichtabstrahlung Mv [lm/m²] gibt den in den Halbraum abgegebenen Lichtstrom pro Einheitsfläche an — analog zur Beleuchtungsstärke, jedoch für Lichtabgabe statt Lichtempfang.
- Für einen ideal diffus abstrahlenden Lambertischen Strahler mit Leuchtdichte L gilt: Mv_out = π · L.

### Beleuchtungsstärke (Kap. 26.3.7)

- Die Beleuchtungsstärke E [Lux, lx; 1 lx = 1 lm/m²] ist der empfangene Lichtstrom pro Fläche.
- Bei Neigung der Empfangsfläche um ε gegenüber der Einfallsrichtung: E(ε) = E₀ · cos ε.
- Bei Lichteinfall aus dem gesamten Halbraum: E = ∫_H L(ω) · cos ε · dω.
- Für konstante Leuchtdichte des Halbraums: E = π · L_in.
- Zusammenhang Leuchtdichte und Belichtung: Für eine ideal lichtstreuende Lichtdecke mit Transmissionsgrad τ gilt: L_out = τ · L_in, und Mv = E · τ.
- Aus Beleuchtungsstärke und bekanntem Reflexionsgrad ρ lässt sich die Leuchtdichte berechnen: E · ρ = π · L_out.
- Wichtig: Die Hemisphäre ist ein mathematisches Konstrukt, das am Messpunkt plan auf die Empfangsebene gelegt wird; die Polachse entspricht der Flächennormalen.

### Belichtung (Kap. 26.3.8)

- Die Belichtung Hv [lx·s] ist das Produkt aus Beleuchtungsstärke und Beleuchtungsdauer; bei nicht-konstanter Beleuchtungsstärke: Hv = ∫(t1 bis t2) E(t) · dt.

### Lichtausbeute und Leistungsausbeute (Kap. 26.3.9)

- Die Lichtausbeute ηv [lm/W] beschreibt die Lichtabgabe einer Lichtquelle pro eingesetzter Leistung.
- Abschätzung für Tageslicht: max. Außenbeleuchtungsstärke horizontal ca. 100.000 lx, max. Bestrahlungsstärke ca. 1000 W → Lichtausbeute Tageslicht ca. 100 lm/W.
- Die Leistungsausbeute ηPv = ηv / Km gibt den lichtwirksamen Anteil der Gesamtleistung an:
  - Tageslicht: 100 lm/W ÷ 683 lm/W ≈ 14 %
  - Hochdruck-Quecksilberdampflampe: 60 lm/W ÷ 683 lm/W ≈ 9 %
  - Glühlampe: 12 lm/W ÷ 683 lm/W ≈ 2 % (d.h. 98 % der elektrischen Leistung gehen direkt als Wärme verloren)

### Transmission, Reflexion, Absorption (Kap. 26.3.10)

- Die drei Wechselwirkungen zwischen Strahlung und Materie sind Transmission (τ), Reflexion (ρ) und Absorption (α).
- Grundgesetz: τ + ρ + α = 1 (bzw. ≤ 100 %, wenn in Prozent angegeben). Andere Wechselwirkungen gibt es nicht.
- Bei opaken Flächen: τ = 0.
- Beim idealen schwarzen Körper: τ = ρ = 0, damit α = 1.
- Reflexion kann zwischen spiegelnd und ideal streuend variieren; Transmission zwischen direktem und ideal gestreutem Durchgang.
- Bei Sondergläsern (Farb-, Sonnenschutzgläser) werden Transmissions- und Reflexionsspektren angegeben.

### Photometrisches Entfernungsgesetz (Kap. 26.4)

- Für kompakte Lichtquellen (Ausdehnung klein gegenüber dem Abstand) gilt das quadratische Entfernungsgesetz:
  E = I/r² · cos ε
- Fehler unter 1 %, solange das Verhältnis Ausdehnung zu Entfernung kleiner 1:10 bleibt.

### Formfaktoren und Photometrisches Grundgesetz (Kap. 26.5)

- Für die Lichtverteilung im Raum ist der Lichtaustausch zwischen Oberflächen entscheidend.
- Der Lichtstrom, der von Flächenelement dA1 auf dA2 fließt: dΦ1→2 = L1 · cos ε1 · cos ε2 / r² · dA1 · dA2.
- Daraus folgen zwei wichtige Schlussfolgerungen:
  1. Die zwischen zwei Flächen ausgetauschten Lichtströme verhalten sich wie ihre Leuchtdichten.
  2. Bei gleichen Leuchtdichten sind die ausgetauschten Lichtströme gleich groß — photometrisches Grundgesetz.
- Der (geometrische) Formfaktor F1-2 ist der Anteil der von Fläche A1 abgegebenen Strahlung, der auf Fläche A2 fällt. Er entspricht dem auf 1 normierten projizierten Raumwinkel von A2 aus A1-Perspektive: F1-2 = (1/π) · ∫ cos ε · dω.
- Mit Formfaktor vereinfacht sich der Lichtstrom: Φ1-2 = F1-2 · Φges,1 = π · L1 · A1 · F1-2 = Mv1 · A1 · F1-2.

#### Reziprozitätsbeziehungen (Kap. 26.5.1)

- Zwischen Formfaktoren gelten folgende Reziprozitätsbeziehungen (vorausgesetzt: Lambertsche Abstrahlung):
  - dF1-2 · dA1 = dF2-1 · dA2 (zwei Flächenelemente)
  - F1-2 · A1 = F2-1 · A2 (zwei endliche Flächen)
- Die Formfaktoren zweier Flächen sind umgekehrt proportional zu deren Größen; bei gleich großen Flächen sind die Formfaktoren gleich.
- Diese Beziehungen vereinfachen lichttechnische Berechnungen erheblich.

#### Analytische Formfaktoren für Rechteckflächen (Kap. 26.5.2)

- Für ein Flächenelement dA1 parallel zu einer rechteckigen Fläche A2 (Flächennormale von dA1 zeigt auf eine Ecke von A2) gilt: Fd1-2 = (1/π) · [arctan(X/√(1+Y²)) + arctan(Y/√(1+X²))].
- Für senkrecht zueinander stehende Flächen (dA1 auf Flächennormale von A2, die von einem Eckpunkt ausgeht) gilt ein eigener Ausdruck mit Y- und X-bezogenen arctan-Termen.
- Liegt der Untersuchungspunkt nicht in der Eckverlängerung, kann durch additive/subtraktive Stückelung (Fd0-2 = Fd0-1234 − Fd0-13 − Fd0-34 + Fd0-3) der Formfaktor stets ermittelt werden, sofern das Flächenelement parallel oder senkrecht zur Fläche steht.
- Damit lassen sich alle Interreflexionsberechnungen in rechteckigen Räumen lösen; für komplexere Raumgeometrien sind andere Methoden notwendig.

### Berechnung der Lichtverteilung durch Interreflexion (Kap. 26.6)

- Das Interreflexionsverfahren (auch Radiosity-Verfahren) berechnet den Lichtaustausch aller Raumflächen untereinander.
- Ablauf: Zunächst Berechnung des Direktlichtempfangs jeder Fläche, dann sukzessive Reflexionsgänge.
- Die allgemeine Formel für Reflexionsgang k auf Fläche i: Dik = D0i + Σ(j=1 bis N) ρj · Dj,k-1 · Fdi-j.
  - D0i: Direktlichtanteil der Fläche i
  - ρj: Reflexionsgrad der strahlenden Fläche j
  - Fdi-j: Formfaktor von Fläche i auf Fläche j
  - N: Anzahl der Flächen; k: Reflexionsgangnummer
- Die Lichtverteilung konvergiert i.d.R. nach spätestens 10 Reflexionsgängen; in Beispielrechnungen bereits nach dem dritten Gang.

#### Berechnungsbeispiel Quader mit Lichtdecke (Kap. 26.6, Tab. 26.4–26.6)

- Modellraum: Quaderförmig, Lichtabgabe durch obere Fläche (diffuse Lichtdecke), kein Fenster.
- Voraussetzungen (Tab. 26.4):
  - Boden E1: ρ = 0,15
  - Wände E2–E5: ρ = 0,50 (je)
  - Lichtdecke E6: τ = 0,6; ρ = 0,1; primärer Lichtempfang D = 0,1 (= 10 %)
- Direktlichtempfang D0 der Untersuchungspunkte (Flächenmittelpunkte):
  - Boden E1: D0 = 0,029
  - Wand E2: D0 = 0,018
  - Wand E3: D0 = 0,017
  - Wand E4: D0 = 0,018
  - Wand E5: D0 = 0,017
  - Decke E6: D0 = 0,000 (empfängt nur Reflexlicht)
- Endwerte nach 5 Reflexionsgängen (Tab. 26.5):
  - Boden: D5 = 0,036 (Reflexlichtanteil ca. 0,007)
  - Wände E2, E4: D5 = 0,025
  - Wände E3, E5: D5 = 0,024
  - Decke: D5 = 0,134
- Tageslichtquotienten im Beispiel: Bodenmitte 3,6 %, Längswände mittig 2,5 %, Querwände 2,4 %. Reflexlichtanteil jeweils ca. 0,7 %.
- Beleuchtungsstärken bei 20.000 lx Außenbeleuchtungsstärke (Tab. 26.6):
  - Boden: E5 ≈ 720 lx (Reflexlichtanteil 135 lx)
  - Wände E2, E4: E5 ≈ 497 lx (Reflexlichtanteil 136 lx)
  - Wände E3, E5: E5 ≈ 484 lx (Reflexlichtanteil 142 lx)
  - Decke: E5 ≈ 179 lx (ausschließlich Reflexlicht)

### Nicht-analytische Ermittlung von Formfaktoren (Kap. 26.7)

Bei verwinkelten Raumgeometrien mit Teilverdeckungen und Schrägflächen sind analytische Lösungen für Formfaktoren meistens nicht verfügbar. Stattdessen werden numerische Näherungsverfahren eingesetzt.

#### Graphische Methoden (Kap. 26.7.1)

**Orthogonale Projektion (Nusselt'sches Analogon):**
- Die Grundfläche der Hemisphäre wird in eine große Anzahl gleich großer Felder (häufig 1000 Felder) unterteilt und orthogonal auf die Hemisphäre projiziert.
- Dabei entstehen Raumwinkelelemente, die auf der Empfangsfläche alle denselben projizierten Raumwinkel (= gleiche Wirkung) besitzen.
- Eine zu untersuchende Fläche wird auf die Kugeloberfläche und von dort orthogonal auf die Grundebene projiziert. Das Zählen der von diesem projizierten Umriss eingeschlossenen Felder, geteilt durch die Gesamtanzahl der Felder, ergibt den Formfaktor (Beispiel: 352 von 1000 Kästchen → Formfaktor 0,352).
- Das Blatt mit den 1000 Kästchen heißt Zählblatt.

**Stereographische Projektion (Kap. 26.7.1.2):**
- Im Horizontbereich werden die Kästchen bei orthogonaler Projektion sehr klein und ungenau.
- Alternativ: Die Kugeloberflächen-Teilflächen werden mit dem Nadir (Gegenpol des Zenits) verbunden; die Durchdringungspunkte durch die Grundebene ergeben ein neues Muster mit gleichmäßigeren Feldgrößen auch im Horizontbereich.
- In die Zählblatt-Einteilung kann die Leuchtdichteverteilung des bedeckten Himmels nach Moon und Spencer für horizontale Empfangsflächen direkt integriert werden (bei geneigten Flächen nicht möglich).
- Sonnenstandsdiagramme basieren meistens auf stereographischer Projektion (Sonnenbahnen erscheinen als Kreissegmente, geometrisch konstruierbar).
- Ein vollständiges grafisches System für Tageslichttechnik (inkl. Konstruktionsblätter) wurde Mitte des 20. Jh. von Tonne entwickelt (angeregt durch G. Pleijel, 1908–1962, schwedischer Architekt).

#### Computergestützte Methode (Kap. 26.7.2)

- Strahlen werden vom Hemisphären-Zentrum durch die Mittelpunkte der Hemisphären-Teilflächen in den Raum ausgesendet.
- Jeder Strahl entspricht einem Formfaktor-Wert (analog einem Zählkästchen bei der grafischen Methode).
- Der Formfaktor einer Fläche ergibt sich als Summe der Formfaktorwerte aller Strahlen, die diese Fläche treffen.
- Verdeckungen: Für jeden Strahl wird geprüft, welche Fläche zuerst getroffen wird. Dazu wird für jede Raumfläche (als Ebene mit Ebenengleichung) der Durchdringungspunkt berechnet; die dem Ursprung nächste Fläche gilt als unverdeckt.
- Genauigkeit steigt mit Strahlanzahl; aus nicht analytisch lösbaren Integralen werden diskrete Summen — in der Literatur als "brute force integration" bezeichnet.
- Ablauf für Interreflexion: Raumflächen in kleine Patches unterteilen → Reflexionsgrade und Leuchtdichten bestimmen → Formfaktoren aller Patches berechnen → Interreflexion nach allgemeiner Formel durchführen.

### Computergrafik und lichttechnische Berechnungsverfahren (Kap. 26.8)

- Rendering: Berechnung zweidimensionaler perspektivischer Bilder aus 3D-Raumdaten, Berücksichtigung gegenseitiger Verdeckung.
- Optisches Abbildungsmodell: Betrachtungspunkt, Blickrichtung, Bildebene. Die Bildebene wird in Pixel unterteilt; für jeden Pixel wird ein Sehstrahl in den Raum ausgesendet.
- Ray Casting: Der erste Schnittpunkt eines Sehstrahls mit einer Raumfläche ist die vorderste sichtbare Fläche. Helligkeit wird aus Lichtquellenintensität, Oberflächenfarbe und Einfallswinkel (Cosinus) berechnet. Ergebnis: perspektivisches Bild mit Hell-Dunkel, ohne Schatten.
- Ray Tracing (weiterentwickelter Algorithmus, späte 1970er): Vom Auftreffpunkt werden drei zusätzliche Strahlentypen ausgesandt:
  - Reflection rays (bei spiegelnden Oberflächen)
  - Refraction rays (bei transparenten Materialien, Brechungsindex berücksichtigt)
  - Shadow rays (zu jeder Lichtquelle; verdeckt → Schatten, unverdeckt → beleuchtet)
- Man unterscheidet eye-based (Strahlen vom Auge) und light-based ray tracing (Strahlen von der Lichtquelle).
- Global Illumination: Verfahrensfamilie für physikalisch korrekte Lichtverteilung im Raum:
  - Radiosity: Korrekt für diffuse Flächen und ausgedehnte Lichtquellen (s. Kap. 26.6).
  - Photon Mapping: Im ersten Rechenschritt werden von Lichtquellen Strahlen in den Raum ausgesendet; Licht wird absorbiert, reflektiert oder gebrochen und an Auftreffpunkten gespeichert. Im zweiten Schritt wird eye-based ray tracing für das Bild durchgeführt.
  - Metropolis Light Transport (MLT): Stochastische Methode, bei der relevante Raumwinkel mit mehr Strahlen dichter abgetastet werden (z.B. Türspalt als einzige Lichtquelle in einem Raum). Reduziert Rechenaufwand bei hoher Bildqualität.
- Limitierungen aller Verfahren:
  - Begrenzte Strahlanzahl → physikalisch nicht immer exakt, v.a. bei kleinen Geometrien (Lamellen, Raster).
  - Darstellbarer Leuchtdichtekontrast von Monitor und Druck ist kleiner als das berechnete physikalische Spektrum → Tone Mapping nötig (mit Informationsverlust).

### Wahrnehmung von Licht (Kap. 26.9)

#### Helligkeitswahrnehmung und Adaptation (Kap. 26.9.1)

- Das Auge adaptiert sich über einen enormen Bereich: von unter 1 lx (Vollmond) bis über 100.000 lx (Sommersonne) ohne dauernde Blendung.
- Adaptation bezeichnet die zeitliche Helligkeitsanpassung; Akkommodation das Scharfstellen.
- Im Gesichtsfeld werden Flächen mit großen Leuchtdichteunterschieden durch aktive Schaltgruppenbildung hinter der Netzhaut auf eine mittlere Umgebungsleuchtdichte gemittelt.
- Große Leuchtdichteunterschiede (Extremfall: helles Weiß neben Schwarz) werden als Kontrastblendung empfunden — je größer die Flächen, desto störender.
- Anforderungen an Arbeitsplatzbeleuchtung hängen von der Arbeitsaufgabe ab: Diffizilere Arbeit erfordert höhere Beleuchtungsstärken.

#### Weber-Fechnersches Gesetz (Kap. 26.9.2)

- Sinneswahrnehmungen verlaufen im Hauptempfindungsbereich proportional zum Logarithmus der Reizintensität.
- Wahrnehmungsunterschiede hängen nicht von absoluten, sondern von relativen Intensitätsunterschieden ab: ΔΨ ∝ ΔI/I → Ψ ∝ log I.
- Beispiel: Erhöhung von 1 lx auf 2 lx ist deutlich spürbar; Erhöhung von 100 lx auf 101 lx nicht wahrnehmbar. Gleicher relativer Unterschied (Verdoppelung) wird stets als gleiche Helligkeitsänderung wahrgenommen.
- Für Schall gibt es die logarithmische Einheit dB(A); eine entsprechende Einheit für Licht ist nicht definiert.
- In der Praxis werden Beleuchtungsstärken und Tageslichtquotienten oft logarithmisch aufgetragen (z.B. Tageslichtschnitte, Lichtregel-Messkurven).
- Vorteil log. Darstellung: Multiplikation (z.B. durch Verglasungs-Transmissionsgrad) wird zur Verschiebung auf der Skala, ohne Änderung der Kurvenform. Tageslichtquotientenverläufe ermöglichen qualitative Bewertung unabhängig von der angenommenen Außenbeleuchtungsstärke.

#### Blendung (Kap. 26.9.3)

- Es werden drei Arten unterschieden (fließende Übergänge):
  1. Blendende Blendung (stärkste): Blick direkt in Sonne oder Hochleistungsquellen → kurzfristige bis dauerhafte Erblindung.
  2. Physiologische Blendung: messbare Sehbeeinträchtigung (z.B. voll verglastes Gangende).
  3. Psychologische Blendung: ständige Helligkeitswechsel (z.B. Arbeitsplatz direkt am Fenster) → Ermüdung durch fortlaufende Adaptation, ohne bewusste Sehbeeinträchtigung, aber Unwohlsein.
- Kontrastblendung: durch hohes Leuchtdichtegefälle (z.B. großes Fenster vor dunkler Wand oder Person vor Fensterhintergrund → Silhouettenwahrnehmung).
- Maßnahmen gegen Blendung: Vorhänge, Blendschutzrollos, Jalousetten, Gardinen; planerisch: kein Fenster hinter Vortragenden, Oberlichter statt Seitenfenster bei Sporthallen und Konferenzsälen. Oberlichter möglichst lichtstreuend verglast; Größe und Anordnung bei geschlossenem seitlichem Sonnenschutz bemessen.
- Bei Kunstlichtplanung: direkt sichtbare Lichtquellen vermeiden.

#### Farbmetrik und Farbwiedergabe (Kap. 26.9.4)

- Das menschliche Farbsehen beruht auf drei Zapfentypen (nur Tagsehen, nicht Nachtsehen):
  - L-Typ (Rot-Rezeptor, long-wavelength)
  - M-Typ (Grün-Rezeptor, middle-wavelength)
  - S-Typ (Blau-Rezeptor, short-wavelength)
- Aus den gemittelten Probandenmessungen wird ein sog. Normalbeobachter mit standardisierter Wahrnehmungscharakteristik definiert.
- Hohe Farbwiedergabequalität ist wichtig in Museen, Wohn- und Arbeitsräumen (auch wenn nicht direkt bewusst wahrgenommen).
- Der allgemeine Farbwiedergabe-Index Ra bewertet Lichtquellen und transmittierende Materialien.
- Messverfahren: 8 von 14 definierten Farbproben werden abwechselnd mit Testlichtquelle und Bezugslichtart beleuchtet; die Farbortverschiebungen ΔEi werden im CIE-Normfarbsystem (meistens CIE 1964 L*u*v*) berechnet.
- Spezieller Farbwiedergabe-Index für eine einzelne Referenzfarbe: Ri = 100 − 4,6 · ΔEi.
  Der Faktor 4,6 ist so gewählt, dass eine warmweiße Standard-Leuchtstofflampe ungefähr Ra = 50 ergibt.
- Allgemeiner Farbwiedergabe-Index Ra: Mittelwert der ersten 8 Einzelindizes: Ra = (1/8) · Σ(i=1 bis 8) Ri.
- Farbort: Punkt in der CIE-Normfarbtafel oder einem anderen Farbdarstellungssystem; ermöglicht betrachterunabhängige Farbdefinition (Anwendung: Reproduzierbarkeit von Lacken, Stoffen, Kalibrierung von Druckern und Monitoren).
