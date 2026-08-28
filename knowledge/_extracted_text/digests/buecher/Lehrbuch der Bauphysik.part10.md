# Lehrbuch der Bauphysik — Teil 10
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 401-440.

Dieser Abschnitt behandelt Kapitel 16 „Komponenten des Außenklimas" mit Fokus auf die mathematische Beschreibung von Außenlufttemperatur (Jahresgang, Tagesgang, Summenhäufigkeit) sowie kurzwellige und langwellige Strahlungsbelastungen auf Bauteilflächen — einschließlich des Analytischen Referenzklimas (ARY) und praxistauglicher Tabellenwerte für die wärmetechnische Bauteilbemessung.

## Inhalt

### 16.1 Außenlufttemperatur — Jahres- und Tagesgänge

#### Klimatische Unterschiede Dresden vs. Essen
- Dresden zeigt ausgeprägteres Kontinentalklima, Essen eher Seeklima (Westseiten)
- Jahresmaximum: Dresden 19,8 °C, Essen 17,7 °C
- Jahresminimum: Dresden −1,4 °C, Essen +1,3 °C
- Zeitverschiebung für Maximum (Juli) und Minimum (Januar) in beiden Fällen circa 20 Tage

Essen-Parameterwerte (vereinfachte harmonische Formel 16.1b):
- Jahresmitteltemperatur: θemE = 9,5 °C
- Jahresamplitude: ΔθeE = 8,2 K
- Jahreslänge: Ta = 365 d
- Zeitverschiebung: ta = 20 d
- Aus Formel: θeE(15) = 1,33 °C, θeE(197,5) = 17,67 °C

#### 16.1.2 Analytisches Referenzklima (ARY)

Das ARY (Analytical Reference Year) beschreibt den tatsächlichen Temperaturverlauf durch Überlagerung mehrerer harmonischer Funktionen mit verschiedenen Periodendauern und Amplituden (Formel 16.2). Zusätzlich wird der Tagesgang durch eine Exponentialfunktion leicht verformt, um den Wärmespeichereffekt des Erdbodens zu erfassen.

ARY-Parameter für Mitteleuropa (Dresden 1997 als Referenz):
- Jahresmitteltemperatur: θem = 8,6 °C
- Jahresamplitude: Δθea = 11,0 K
- Witterungsamplitude: ΔθeP = 3,4 K
- Tagesamplitude: Δθed = 12,0 K
- Jahreslänge: Ta = 365 d
- Witterungsperiodenlänge: Tp = 10 d
- Tageslänge: Td = 1 d
- Jahreverschiebung: ta = 20 d
- Tagesverschiebung: td = 9/24 d

Validierung: Vergleich berechneter vs. gemessener Werte Dresden 1997 zeigt gute Übereinstimmung; lediglich erste Märzdekade 1997 (ungewöhnlich warm) wird nicht gut abgebildet. Spitzenwerte der Außenlufttemperatur im Sommer: +32 °C, im Winter: −8 °C.

Klimatisch wichtige Mitteltemperaturen (aus Tag-/Nachtmittelung):
- Höchste Sommertemperatur (Tage 202–204): +24 °C → Berechnungswert für vereinfachten sommerlichen Wärmeschutz in Mitteleuropa
- Tiefste Wintertemperatur (Tage 16–18): −5 °C → rechnerische Wintertemperatur für Wärme- und Feuchtetechnik

Für exakte hygrothermische Simulationen können Messstundenwerte oder Testreferenzjahre (TRY) verwendet werden.

#### Tab. 16.2 — Ausgewählte Temperaturwerte (Mitteleuropa/Dresden)

| Kennwert | Wert |
|---|---|
| Mittelwert 2 heißeste Julitage (Tage 202–204) | 23,8 °C |
| Mittelwert 2 kälteste Januartage (Tage 16–18) | −5,2 °C |
| Jahresmittelwert (365 Tage) | 9,1 °C |
| Heizperiodenmittel (190 Tage, Okt.–Mitte April) | +2,2 °C |

Monatsmittelwerte (aus ARY-Formel 16.2):

| Monat | Mitteltemperatur |
|---|---|
| Januar | −2,0 °C |
| Februar | −0,9 °C |
| März | +2,9 °C |
| April | +8,4 °C |
| Mai | +14,3 °C |
| Juni | +18,5 °C |
| Juli | +20,1 °C |
| August | +18,5 °C |
| September | +14,4 °C |
| Oktober | +8,7 °C |
| November | +2,5 °C |
| Dezember | −0,1 °C |

#### Tab. 16.3 — Monatsmittelwerte im Vergleich (Temperaturen in °C)

| Monat | Zeitvektor tM (d) | ARY θm | Messung 1997 θM | Dresden-Klotzsche θK |
|---|---|---|---|---|
| Jan | 15,0 | −2,0 | −2,4 | −0,7 |
| Feb | 45,0 | −0,9 | 5,6 | 0,4 |
| März | 75,0 | 2,9 | 6,7 | 4,0 |
| April | 105,0 | 8,4 | 7,1 | 7,9 |
| Mai | 135,0 | 14,3 | 15,2 | 12,7 |
| Juni | 165,0 | 18,5 | 18,2 | 16,2 |
| Juli | 195,0 | 20,1 | 19,2 | 18,2 |
| Aug | 225,0 | 18,5 | 21,9 | 17,8 |
| Sept | 255,0 | 14,4 | 15,6 | 14,1 |
| Okt | 285,0 | 8,7 | 8,8 | 9,8 |
| Nov | 315,0 | 2,5 | 5,1 | 4,2 |
| Dez | 345,0 | −0,1 | 3,4 | 1,2 |

Dresden-Klotzsche = 100 m über Innenstadt, Mittelwerte 1981–1990.

#### 16.1.3 Tagesgang der Außenlufttemperatur

- Amplitude des Tagesgangs ist im Sommer größer als im Winter
- An wolkenlosen Tagen größer als an trüben Tagen
- Wärmespeichereffekt des Erdbodens deformiert harmonischen Verlauf leicht
- Aufheizung am Vormittag und Abkühlung am Nachmittag verlaufen jeweils exponentiell
- ARY-Ansatz (Formel 16.2) bildet diese Phänomene für typische Tagesgänge (heiterer Tag, Regentag, wolkenloser Frosttag, bewölkter Tauwettertag) gut ab

#### 16.1.4 Summenhäufigkeit der Außenlufttemperatur

Die Summenhäufigkeit gibt an, wie viele Tage im Jahr eine bestimmte Grenztemperatur unterschritten wird. Sie läuft von −25 °C bis +40 °C in 0,5-K-Schritten und kann durch das Gaußsche Fehlerintegral angenähert werden.

Jahresmitteltemperaturen für Fehlerintegral-Ansatz:
- Dresden 1997: θemD = 9,5 °C
- Cottbus 2014 (sehr warmes Jahr): θemC = 11,1 °C

Grobe Linearisierungen (Geraden):
- Dresden 1997: Z(θ) = 12 × θ + 70
- Cottbus 2014: Z(θ) = 14,5 × θ + 20

#### Tab. 16.4 — Bauklimatisch wichtige Außentemperaturen und Auftrittshäufigkeit

| Temperatur | Bedeutung | Häufigkeit z (Tage) |
|---|---|---|
| −5 °C | Wintertemperatur für Mindestwärme-/Feuchteschutz-Nachweis | z(−5) = 21 |
| 0 °C | Frost-Tauübergang | z(0) = 55 |
| 9,5 °C | Jahresmitteltemperatur | z(9) = 183 |
| 10 °C | Heizgrenztemperatur (Nachweis Heizwärmebedarf) | z(10) = 190 |
| 15 °C | Sommertemperatur für Trocknungsnachweis nach Kondensatbefall | z(15) = 255 |
| 24 °C | Sommertemperatur für sommerlichen Wärmeschutz | z(24) = 344 |

Interpretation:
- Wintertemperatur −5 °C wird an 21 Tagen unterschritten
- Etwa 2 Monate Frost (0 °C unterschritten: 55 Tage)
- Heizperiode (unter 10 °C): 190 Tage
- Trocknungsphase oberhalb 15 °C: rund 3 Monate (365 − 255 = 110 Tage)
- Sommerauslegungsperiode (über 24 °C): circa 3 Wochen (365 − 344 = 21 Tage)

---

### 16.2 Kurzwellige und langwellige Wärmestrahlungsbelastung

Auf Gebäude wirken folgende strahlungsbedingte Wärmestromdichten ein:
- Direkte kurzwellige Sonnenstrahlung: Gdir
- Diffuse kurzwellige Strahlung: Gdif
- Langwellige Abstrahlung und Himmelsgegenstrahlung: Glang oder Gre

Kurzwellige Strahlung ist elektromagnetische Strahlung emittiert von Flächen mit ca. 5785 K (Sonnenoberfläche). Langwellige Strahlung wird zwischen Flächen im 300-K-Bereich ausgetauscht.

Solarkonstante G0 an der Atmosphärengrenze (in 2000 km Höhe, normal zur Strahlungsrichtung): 1380 W/m²

Beim Atmosphäreneintritt wird ein Teil absorbiert, ein Teil diffus gestreut.

#### Atmosphärischer Trübungsfaktor Tr

Definition via Verhältnis der Strahlungsdämpfung (Formel 16.7):
- Gno = Strahlungsdichte bei sauberer, trockener Luft
- Gn = tatsächliche Strahlungsdichte

#### Tab. 16.5 — Trübungsfaktor und Strahlungsleistung auf der Erdoberfläche (Formel: Gn = G0 · e^(Tr · ln(0,87)))

| Trübungsstufe Tr | Beschreibung | Strahlungsleistung Gn (W/m²) |
|---|---|---|
| Tr = 1 | Saubere, trockene Luft | 1174,5 |
| Tr = 2 | Landluft Winter | 1021,8 |
| Tr = 3 | Stadtluft Winter | 889,0 |
| Tr = 4 | Landluft Sommer | 773,4 |
| Tr = 5 | Stadtluft Sommer | 672,9 |
| Tr = 6 | Industriegebiet, stark verschmutzt | 585,4 |

Bei Tr = 6 kommt nur noch die Hälfte der Strahlungsleistung aus sauberer Luft an (585 vs. 1175 W/m²).

#### 16.2.1 Kurzwellige Strahlung auf eine Horizontalfläche

Jahresgang der direkten Strahlung auf Horizontalfläche (ARY, Formel 16.9, Trübung ≈ 4):
- Gdirl = 379 W/m²
- Gdir2 = −62 W/m²
- ΔGdir = 242 W/m²
- Ta = 365 d, ta = 10 d, Td = 1 d, Tp = 10 d

Jahresgang der diffusen Strahlung auf Horizontalfläche (ARY, Formel 16.10):
- Gdif1 = 190 W/m²
- Gdif2 = 12 W/m²
- ΔGdif = 98 W/m²

Globalstrahlung (Gesamtstrahlungswärmestromdichte auf Horizontalfläche) als Summe aus Gdir + Gdif (Formel 16.11).

Mittelwerte der Globalstrahlung:
- Winterliche Heizperiode (190 Tage, Oktober bis April): 55 W/m²
- Schönwetterperiode (5 Tage im Juni, Tage 173–178): 276 W/m²

Vereinfachter harmonischer Jahresgang der Globalstrahlung (Formel 16.12):
- Ghm = 114 W/m² (Mittelwert)
- ΔGh = 110 W/m² (Amplitude)
- Maximum im Juni, Minimum im Dezember
- Heizperiodenmittel bestätigt: 55,1 W/m²

Tageslängenfunktion D(t): D(t) = 1 wenn Sonnenhöhenwinkel h > 0 (Tag), D(t) = 0 wenn h < 0 (Nacht) — modelliert via Heaviside-Sprungfunktion.

#### 16.2.2 Strahlungswärmestromdichte auf beliebig orientierte und geneigte Flächen

Berechnung der direkten Strahlung auf eine beliebige Bauteilfläche aus der Horizontalstrahlung mittels Winkelhilfsfunktion B(t,α,β) (Formel 16.13):
- h = Sonnenhöhenwinkel (Winkel zwischen Sonnenstrahl und horizontaler Projektion)
- a = Azimutwinkel der Sonne (Winkel zwischen Sonnenstrahl-Schatten und Nordrichtung)
- β = Winkel zwischen Flächennormale und Nordrichtung
- α = Neigungswinkel der Bauteilfläche
- Ghorizontal = direkte Sonnenstrahlung auf Horizontalfläche in W/m²

Sonnenhöhenwinkel h(t) wird aus geographischer Breite χ (Breitengrad) und Tageszeit berechnet (Formel 16.14). Für Mitteleuropa: χ = 52° Nord.

Deklinationswinkel δ(t) der Sonne (Formel 16.15): Schwankt zwischen +23,5° (Sommer) und −23,5° (Winter).

Azimutwinkel a(t) der Sonne: Stetig zunehmend über den Tagesverlauf; Vorzeichenwechsel (Signumfunktion) muss berücksichtigt werden (Formel 16.16).

Eigenverschattungsfunktion SE(t,α,β) hat Wert 1, solange die Sonne die Bauteilfläche tatsächlich bescheint, sonst 0. Daraus ergibt sich die allgemeine Winkelhilfsfunktion B(t,α,β) (Formel 16.19).

Hinweis: Winkelhilfsfunktion B strebt bei streifendem Strahlungseinfall gegen unendlich → für Berechnungen wird B < 5 begrenzt.

Gesamtstrahlung auf beliebige Bauteilfläche (Formel 16.20):
- Gdir,αβ(t,α,β) = Gdir(t) × B(t,α,β) [direkte Strahlung]
- Gdif,α(t,α) = Gdif(t) × (0,65 + 0,35 × cos(α/3)) [diffuse Strahlung, nur neigungsabhängig, empirischer Ansatz]
- Gges,αβ = Gdif,α + Gdir,αβ [Gesamtstrahlung]

Wichtige Beobachtung: Südwand im Sommer erhält geringere Maximalwerte als Ost- oder Westwand, da der Sonnenstand im Sommer sehr hoch ist (flacherer Auftreffwinkel auf Südwand).

#### Tab. 16.6 — Strahlungsbelastungen auf Wände und Dächer nach Himmelsrichtung (W/m²)

Mittelwerte über Heizperiode (190 Tage, Oktober bis April) und Hitzeperiode (5 Tage Ende Juni):

| Bauteilfläche | Heizperiode (W/m²) | Hitzeperiode (W/m²) |
|---|---|---|
| Nordwand (90°) | 22,4 | 90,4 |
| Norddach 45° | 26,8 | 178,2 |
| Nordostwand (90°) | 24,0 | 126,7 |
| Nordostdach 45° | 30,7 | 193,0 |
| Ostwand (90°) | 33,8 | 160,7 |
| Ostdach 45° | 43,9 | 229,9 |
| Südostwand (90°) | 52,1 | 150,0 |
| Südostdach 45° | 61,2 | 239,4 |
| Südwand (90°) | 62,2 | 123,7 |
| Süddach 45° | 69,1 | 233,8 |

#### Tab. 16.7 — Gerundete mittlere Strahlungsbelastungen auf Wände (90°) und Dächer (45°) in W/m²

| Zeitraum | Horiz. | N-90° | NO-90° | O-90° | SO-90° | S-90° | N-45° | NO-45° | O-45° | SO-45° | S-45° |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Heizperiode 190 Tage (Okt–Apr) | 55 | 22 | 24 | 34 | 52 | 62 | 27 | 31 | 44 | 61 | 69 |
| Hitzeperiode 5 Tage (Ende Juni) | 276 | 90 | 127 | 161 | 150 | 124 | 178 | 193 | 230 | 239 | 234 |

Verwendungszweck: Quantifizierung des Heizwärmebedarfs während der Heizperiode und Berechnung von Raumtemperaturen bei freier Klimatisierung außerhalb der Heizperiode.

Globalstrahlung lässt sich ohne Einzelmessung hinreichend genau in direkte und diffuse Anteile aufteilen (eigene Aufteilungsfunktion 16.22, Gs = 1380 W/m²):
- Gdif,B(j) = 0,75 × Gges,B(j) × (1 − Gges,B(j)/Gs)^(0,5) × [Sprungfunktion ≥ 0]

#### Zusammenhang Strahlung, Temperatur und Regen
- An wolkenlosen Strahlungstagen treten auch die größten Temperaturschwankungen auf
- Regenschauer unterbrechen die direkte Strahlung (wird per Sprungfunktion auf null gesetzt)
- Hohe Temperaturen korrelieren mit hohen Strahlungswerten; niedrige Strahlungswerte treten sowohl im Winter als auch im Sommer auf
- Zwischen Jahresgang der Temperatur und der Strahlung besteht eine Phasenverschiebung

---

### 16.2.3 Langwellige Abstrahlung

Langwelliger Strahlungsaustausch findet zwischen Flächen im 300-K-Bereich statt (im Gegensatz zu kurzwelliger Strahlung von 6000-K-Flächen).

Einfluss auf Gebäudeenergiebilanz: eher gering, jedoch können sich Außenoberflächen nachts durch langwellige Abstrahlung stark abkühlen. Folgen:
- Betauung der Bauteiloberflächen
- Langsameres Abtrocknen nach Schlagregenbelastung
- Erhöhte Gefahr der Veralgung

Strahlungswärmestromdichte vom Gebäude (Stefan-Boltzmann-Gesetz, Formel 16.22):
- Glang = εB × σ × TB⁴

Emissionskoeffizient εB:
- Alle Baustoffe im langwelligen Bereich: εB ≈ 0,95
- Polierte Metalle: εB ≈ 0,05

Himmelsgegenstrahlung: gleiche Gleichungsform, aber Emissionskoeffizient εH des Himmels ist variabel und hängt von Außenlufttemperatur, relativer Luftfeuchte und Bedeckungsgrad n ab.
- εH bei bedecktem Himmel: 0,95
- εH bei klarem Himmel: 0,55
- εH Cottbus 2014: Bereich 0,55 bis 0,92

Bedeckungsgrad n: Fehlt häufig in Klimadateien. Kann aus dem Verhältnis von diffuser zu Gesamtstrahlung abgeschätzt werden, weil der Direktanteil mit zunehmendem Bedeckungsgrad abnimmt. Berechnung über Mittagswerte (Formel 16.23–16.24), lineare Interpolation über Nacht und Zwischenstunden.

Bedeckungsgradfunktion (Formel 16.24): n(i,k) = V_jG(i,k) — direkt aus interpoliertem Strahlungsverhältnis diffus/gesamt abgeleitet.

Emissionskoeffizient des bewölkten Himmels (Formel 16.25, nach Brutsaert und Konzelmann):
- εH = f(T/100, φ, n) — abhängig von absoluter Temperatur T (K), relativer Luftfeuchte φ und Bedeckungsgrad n
- Exponent 4/0,5-Terme beschreiben physikalische Dämpfung durch Wolken und Wasserdampf

Klimadatei Cottbus 2014: In Tabelle 16.1b und Abbildungen 16.48–16.50 dokumentiert. Direkte und diffuse Strahlungsdaten bilden Grundlage für Bedeckungsgradberechnung.
