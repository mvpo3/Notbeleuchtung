# Lehrbuch der Bauphysik — Teil 20
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 801-840.

Dieser Teil behandelt den Abschluss von Kapitel 26 (Lichtgrundlagen, Farbwiedergabeindex) sowie das vollständige Kapitel 27 (Tageslicht), das sich mit Tagesbeleuchtungsplanung, Tageslichtquotienten, Verglasungstechnik und Besonnungsuntersuchungen befasst. Der Autor ist Christian Kölzow (Institut für Tageslichttechnik Stuttgart).

## Inhalt

### Farbwiedergabeindex Ra — Klassifizierung (Kap. 26, Abschluss)

Leuchtmittel mit identischem Ra-Gesamtindex können bei einzelnen Farbtönen deutlich voneinander abweichen. Beispiel: Hochdruck-Metallhalogendampflampen (3000 K, Ra > 80) reproduzieren Grün- und Blautöne besser als Höchstdruck-Natriumdampflampen mit demselben Ra, die dafür im Rotbereich höhere Einzelwerte Ri aufweisen.

**Klassifizierungstabelle Farbwiedergabeindex Ra:**

| Bewertung | Stufe | Ra-Bereich |
|-----------|-------|------------|
| sehr gut | 1A | Ra ≥ 90 |
| sehr gut | 1B | 80 ≤ Ra < 90 |
| gut | 2A | 70 ≤ Ra < 80 |
| gut | 2B | 60 ≤ Ra < 70 |
| weniger gut | 3 | 40 ≤ Ra < 60 |
| weniger gut | 4 | 20 ≤ Ra < 40 |

Referenznormen für Farbmessung und -wiedergabe: DIN EN ISO 11664 (Farbmetrik), DIN 5033 (Farbmessung), DIN 6169 Teil 2 (Farbwiedergabe-Eigenschaften von Lichtquellen), DIN 5034 Teil 2 (Tageslicht in Innenräumen, Grundlagen, Februar 1985).

---

### Kapitel 27: Tageslicht — Einführung und Planungsgrundlagen

Tagesbeleuchtungsplanung umfasst zwei Schwerpunkte:
- Beleuchtungssituation bei vollständig bedecktem Himmel (normierte Planungsgrundlage, unabhängig von Tages- und Jahreszeit)
- Besonnungssituation (geometrisch-astronomische Analysen)

Der **Tageslichtquotient** (TLQ) ist das zentrale Planungskriterium für den bedeckten Himmel. Er charakterisiert jeden Raum tageslichttechnisch und erlaubt bereits in der Planungsphase Entscheidungen zu Raumgeometrie und Verglasung.

Besonnungsuntersuchungen sind zusätzlich notwendig für:
- Dimensionierung von Licht- und Sonnenschutzmaßnahmen
- Konfiguration von Sonnenschutzrastern (abgestimmt auf Neigung, Orientierung, geografische Lage)
- Energetische Betrachtungen (Photovoltaik, Solarthermie, Raumerwärmung, Kühllasten)

---

### 27.1 Projektionsverfahren — qualitative Abschätzung des Lichteinfalls

Der **Formfaktor Fd1-2** (projizierter, normierter Raumwinkel) gibt Auskunft über den Lichteintrag einer unendlich langen Lichtöffnung in einen Punkt. Er ist dimensionslos und dem Tageslichtquotienten analog:

```
Fd1-2 = (1/2) × (sin ε2 − sin ε1)
```

Der Faktor 1/2 ergibt sich, weil die Projektion des Viertelkreises auf die Grundlinie bereits 1 ergibt (sin 90° − sin 0°); das Ergebnis muss zur Normierung halbiert werden.

**Vergleiche und Erkenntnisse aus dem Projektionsverfahren:**

- **Hohes vs. niedriges Fenster (27.1.1):** Hochliegendes Fenster erzeugt auf Bodenebene nahezu doppelt so hohen Lichtempfang. Wirksamkeit steigt durch günstigeren Einfallswinkel auf Arbeitsebene, geringere Verbauungswirkung, und weil die Himmelsleuchtdichte vom Horizont zum Zenit um das Dreifache zunimmt. In Fensternähe fällt bei hohem Fenster der Wert allerdings schnell ab.

- **Seitenlicht vs. Oberlicht (27.1.2):** Oberlicht ist ca. dreimal effizienter als ein seitliches Fenster gleicher Fläche, weil der Einfallswinkel auf der Arbeitsebene kleiner ist (Cosinus nahe 1). Unter Berücksichtigung der Himmelsleuchtdichteverteilung (Zenit heller als Horizont) wäre der Vorteil noch größer.

- **Horizontale vs. vertikale Empfangsebene in Raumtiefe (27.1.3):** Horizontaler Lichtempfang nimmt vom Fenster zur Raumtiefe stark ab (Faktor ca. 1/7), weil Raumwinkel kleiner und Einfallswinkel größer wird. Vertikale Empfangsebene zeigt weniger starken Abfall; in der Raumtiefe ist der vertikale Empfang mehr als fünfmal so hoch wie der horizontale.

- **Oberlicht: Raummitte vs. Rand (27.1.4):** Horizontaler Lichtempfang nimmt vom Zentrum unter dem Oberlicht zum Rand ab (Raumwinkelabnahme). Vertikale Empfangsflächen erhalten bei großer Lichtdecke oft nur geringen Lichtempfang wegen streifendem Einfall; zudem wirkt nur ein Teil der Lichtdecke auf die jeweilige vertikale Empfangsfläche.

---

### 27.2 Leuchtdichteverteilung des Himmels

Planungsgrundlage ist das **Moon-&-Spencer-Modell** des vollständig bedeckten Himmels. Die Leuchtdichte ist azimutinvariant, steigt aber vom Horizont zum Zenit um das Dreifache:

```
L(ε) = Lz × (1 + 2 × cos ε) / 3
```

Die **Zenitleuchtdichte Lz** [cd/m²] hängt von der Sonnenhöhe γs ab:

```
Lz = (9 / (7 × π)) × (300 + 2100 × sin γs)
```

Die zugehörige Außenbeleuchtungsstärke auf horizontaler unverbauter Fläche bei bedecktem Himmel:

```
Ea = 300 + 2100 × sin γs   [lx]
```

**Außenbeleuchtungsstärken bei bedecktem Himmel für verschiedene Sonnenhöhen:**

| Sonnenhöhe γS [°] | Beleuchtungsstärke Ea [lx] |
|-------------------|---------------------------|
| 0 | 300 |
| 10 | 3 947 |
| 20 | 7 482 |
| 30 | 10 800 |
| 40 | 13 799 |
| 50 | 16 387 |
| 60 | 18 487 |
| 65 | 19 332 |
| 70 | 20 034 |
| 80 | 20 981 |
| 90 | 21 300 |

Für klaren Himmel ist das Modell zusätzlich vom Azimutwinkel der Sonne abhängig. Die CIE stellt verschiedene Himmelsmodelle für Mischzustände zwischen klarem und bedecktem Himmel bereit.

---

### 27.3 Tageslichtquotient (TLQ)

**Definition:** Der Tageslichtquotient D (Daylight Factor) ist das Verhältnis der Beleuchtungsstärke Ei an einem Innen- oder Außenpunkt zur Beleuchtungsstärke Ea auf unverbauter horizontaler Fläche im Freien bei vollständig bedecktem Himmel. D ist dimensionslos, Angabe in Prozent:

```
D = Ei / Ea
```

D ist eine quasi-geometrische Größe, abhängig von Raumabmessungen, Reflexionsgraden der Oberflächen, Anzahl/Anordnung/Größe der Lichtöffnungen und Verglasungsart. Er ist vor Baubeginn berechenbar und korreliert gut mit dem subjektiv wahrgenommenen Helligkeitseindruck.

**Komponenten des TLQ:**

```
D = DH + DV + DR
```

- **DH** (Himmelslichtanteil): direkt am Untersuchungspunkt auftreffendes Himmelslicht
- **DV** (Außenreflexionsanteil): Reflexlicht von der Verbauung (alles, was beim Blick nach außen nicht Himmel ist)
- **DR** (Innenreflexionsanteil): im Innenraum interreflektiertes Himmelslicht

DH und DV bilden zusammen den **Direktlichtanteil Ddir**, ermittelt über den Raumwinkel.

**Superpositionsprinzip:** TLQ-Anteile verschiedener Lichtöffnungen können getrennt berechnet und addiert werden, da sie sich quantitativ nicht gegenseitig beeinflussen.

**Für lichtstreuende Verglasungen** (Milchüberfangglas, Glasgespinsteinlage) gilt: Diese Flächen werden als selbstleuchtend behandelt; TLQ auf dem Fenstermittelpunkt liefert die relative Abstrahldichte; der erzeugte Direktlichtanteil am Untersuchungspunkt heißt DA. Auch für Oberlichter wird der TLQ außen auf der Glasebene berechnet (kann wegen Neigung und Verbauung < 100 % sein):

```
D = DA + DR
```

**Minderungsfaktoren für Fensterkonstruktion:**

```
D = (DHr + DVr + DRr) × k1 × k2 × τ
  oder
D = (DAr + DRr) × k1 × k2 × τ
```

- k1: Versprossungsfaktor (Minderung durch opake Konstruktionsteile)
- k2: Verschmutzungsfaktor
- τ: Lichttransmissionsgrad der Verglasung (einfallswinkelabhängig)

#### 27.3.1 Berechnung des Direktlichtanteils

**Für Fensterflächen** (DH ohne Minderungsfaktoren, nach Rohbaumaßen):

Die Formel Gl. 27.9 arbeitet mit normierten kartesischen Koordinaten X = x/d und Y = y/d (d = Abstand Untersuchungspunkt-Fensterfläche) und enthält arctan-Terme. Die Leuchtdichteverteilung des bedeckten Himmels ist bereits in der Lösung enthalten.

**Für Oberlichtflächen** (Gl. 27.10): Analoge Formelstruktur, angepasst an die senkrechte Einstrahlgeometrie.

**Außenreflexionsanteil DV:** Berechnung mit denselben Formeln wie DH, wenn eine horizontale Trennlinie zwischen Himmel und Verbauung vorhanden ist (z.B. durchgehende First- oder Trauflinie). Das Ergebnis wird mit einem Minderungsfaktor multipliziert, i.d.R. 0,15 (üblicher Reflexionsgrad der Verbauung). Bei stark abweichendem Reflexionsgrad (z.B. helle Hauswand) ist der tatsächliche Reflexionsgrad anzusetzen.

#### 27.3.2 Berechnung des Innenreflexionsanteils

Das Verfahren basiert auf der Theorie der Lichtverteilung in der **Ulbrichtschen Kugel**: In einer Kugel mit ideal diffus reflektierender Innenoberfläche verteilt sich eintretender Lichtstrom vollständig gleichmäßig.

**Für Räume mit selbstleuchtenden Flächen:**

```
E_ind = F0 × ρ̄ / (A_ges × (1 − ρ̄))
```

Als TLQ-Anteil:

```
D_R,diff = D_Fr × A_Fr × ρ̄ / (A_ges × (1 − ρ̄))
```

Mittlerer Reflexionsgrad der Raumoberflächen:

```
ρ̄ = Σ(ρi × Ai) / Σ Ai
```

**Für Räume mit klarverglasten Fenstern:** Der Raum wird gedanklich auf Höhe des TLQ an der Fenstermitte horizontal in zwei Hälften geteilt. Der TLQ der Fensterfläche wird ebenfalls in obere (DFrO) und untere (DFrU) Hälften unterteilt. Für jede Raumhälfte werden separate mittlere Reflexionsgrade ρo und ρu bestimmt. Der untere Raumbereich empfängt überwiegend Licht aus dem oberen (Himmels-)Bereich (Multiplikation mit DFrO × ρu), der obere Bereich Licht aus dem unteren (Verbauungs-)Bereich (× DFrU × ρo):

```
D_R = (D_FrO × ρu + D_FrU × ρo) × A_Fr × ρ̄ / (A_ges × (1 − ρ̄))
```

Bei mehreren Lichtöffnungen: Innenreflexionsanteile getrennt berechnen. Gilt auch für Oberlichter.

#### 27.3.3 Minderungsfaktoren

**Versprossungsfaktor k1:**

```
k1 = lichte Öffnungsfläche / erfasste Öffnungsfläche
```

Sprossen, Kämpfer etc. haben reale Ausdehnung → soweit möglich direkt die effektive lichte Öffnung beim Direktlichtanteil ansetzen, um k1-Ungenauigkeit zu minimieren. Nenner ist nicht die Rohbauöffnungsfläche, sondern die erfasste Fläche. Tiefe Mauerleibungen dreidimensional berücksichtigen.

**Richtwerte k1 nach Fensterart:**

| Fenstertyp | k1 |
|------------|-----|
| Kunststofffenster, zwei- und mehrflüglig | ≤ 0,55 |
| Holzfenster zum Öffnen | 0,60 bis 0,65 |
| Sehr kleine Fenster oder enge Teilung | ≥ 0,35 |
| Holzfenster ohne Flügel | 0,75 bis 0,80 |
| Großflächenfenster | ≤ 0,85 |
| Metallfenster zum Öffnen | 0,70 bis 0,80 |
| Metallfenster zum Öffnen, kleine Fenster/enge Teilung | ≤ 0,65 |
| Metallfenster ohne Flügel | 0,80 bis 0,90 |
| Oberlichter mit Metallsprossen | 0,85 bis 0,90 |

**Verschmutzungsfaktor k2:**

| Fensterlage / Reinigungsintervall | k2 |
|-----------------------------------|-----|
| Wohnungsfenster | 1,00 bis 0,95 |
| Fenster sauberer Arbeitsräume (Schulen, Büros), regelmäßig gereinigt, normale Lage | 0,95 bis 0,90 |
| Bei Spritzwasser (dicht über Dächern, starren Sonnenblenden) | 0,85 bis 0,80 |
| Selten gereinigt (schlechter Zugang) | 0,80 bis 0,75 |
| Oberlichter, normal verschmutzt, Glasneigung 90° bis 75° | 0,80 |
| Oberlichter, normal verschmutzt, Glasneigung 70° bis 45° | 0,75 |
| Oberlichter, normal verschmutzt, Glasneigung 40° bis 10° | 0,70 |
| Starke Schmutzentwicklung: nur 0,85- bis 0,80-faches obiger Werte | — |

---

### 27.4 Richtwerte für Tageslichtquotienten

**Anforderungen an Fenster in Wohn- und Arbeitsräumen (nach [15]):**

Für Arbeitsräume (Raumhöhe bis 3,5 m, Raumtiefe bis 6 m, Grundfläche bis 50 m²):
- Glasoberkante Fenster: ≥ 2,20 m über OK Fertigfußboden (FFB)
- Glasunterkante Fenster: ≤ 0,95 m über OK FFB
- Lichte Glasbreite (bei mehreren Fenstern: Summe): ≥ 55 % der Breite der Fensterwand

**Anforderungen an Oberlichter in Arbeitsräumen:**
- Für Raumgrundflächen < 2000 m² sind zusätzlich Fenster (mit Sichtverbindung) notwendig
- Tageslichtquotienten für horizontale Empfangsflächen: Dmittel = 4 %, Dmin = 2 %
- Gleichmäßigkeit: Verhältnis Dmin : Dmittel ≥ 1:2
- Glasflächen einzeln: bei Raumtiefe < 5 m ≥ 1,25 m²; bei Raumtiefe ≥ 5 m ≥ 1,50 m²
- Gesamtfensterfläche: mindestens 10 % der Grundfläche; oder mindestens 30 % des Produkts aus Raumhöhe × Raumbreite

**Referenzpunkte bei seitlicher Befensterung:**
- Referenzpunkte liegen in halber Raumtiefe von der Fensterwand aus, in 1 m Abstand zu den Seitenwänden
- Einseitige Befensterung: Mittelwert ≥ 0,9 %, niedrigerer Wert D ≥ 0,75 %
- Befensterung zweier angrenzender Wände: D ≥ 1,0 % in beiden Punkten

**Referenz-Außenbeleuchtungsstärken bei bedecktem Himmel (Tab. 27.2):**

| Breitengrad | Dez. 10 u. 14 Uhr WOZ [lx] | Dez. 12 Uhr WOZ [lx] | März–Sep. 10–14 Uhr WOZ [lx] |
|-------------|-----------------------------|-----------------------|-------------------------------|
| 48° N | 6 800 | 9 150 | 18 100 |
| 49° N | 6 300 | 8 750 | 18 000 |
| 50° N | 5 900 | 8 250 | 17 800 |
| 51° N | 5 500 | 7 750 | 17 600 |
| 52° N | 5 100 | 7 250 | 17 300 |
| 53° N | 4 700 | 6 750 | 17 000 |

---

### 27.5 Verglasungen

#### Grundeigenschaften und Glastypen

**Floatglas** ist das am häufigsten verwendete Fensterglas (aus der Schmelze gegossen/gezogen). Der grünliche Farbstich entsteht durch Eisenoxid-Verunreinigungen. Da die Verunreinigung im Volumen liegt, ist der Grünstich und die Transmissionsminderung **dickenabhängig**.

**Weißglas** (eisenoxidarm): deutlich bessere Farbneutralität, teurer. Trotz des Namens ist Weißglas klar und transparent; es ist ebenfalls ein Floatglas. Sinnvoll nicht nur in Museen, sondern auch im Wohn- und Arbeitsbereich.

**Sicherheitsgläser:**
- **ESG** (Einscheibensicherheitsglas): zerbricht durch thermische Vorspannung in kleine Krümel
- **TVG** (teilvorgespanntes Glas): besseres Bruchverhalten als Floatglas
- **VSG** (Verbundsicherheitsglas): Scheiben mit Kunststofffolie (PVB) verklebt; auch als Mehrlagen-VSG für Intrusionsschutz

**UV-Verhalten von Glas:**
- Glas lässt UV-Strahlung bis ca. 320 nm (UVA-Bereich) durch
- Absorptionskante bei ca. 320 nm: Transmission fällt abrupt auf Null
- UVA-Strahlung bewirkt Ausbleichen lichtempfindlicher Materialien
- UV-Schutz in Museen: VSG mit ausreichender PVB-Foliendicke; PVB-Folien haben Absorptionskante bei ca. 390 nm

**IR-Verhalten von Glas (Treibhauseffekt):**
- Absorptionskante im IR-Bereich bei ca. 2800 nm; bei größeren Wellenlängen geht Transmission gegen Null
- Glas lässt kurzwellige Solarstrahlung hindurch, hält aber die nach Absorption in Langwellenstrahlung (Frequenzshift) umgewandelte Wärmestrahlung zurück → Treibhauseffekt
- Analogie zum globalen Treibhauseffekt durch Spurengase in der Stratosphäre

**U-Wert-Entwicklung durch Verglasungsinnovationen:**

| Verglasungstyp | U-Wert [W/m²K] |
|----------------|-----------------|
| Einfachscheibe | ca. 5–6 |
| Isolierverglasung ohne Beschichtung | ca. 2,5–3 |
| Isolierverglasung mit Wärmeschutzbeschichtung (Emissivität ~3 %) | ca. 1,5 |
| Zweifach-Isolierverglasung + Argonfüllung | ca. 1,1 |
| Dreifach-Isolierverglasung + 2 Beschichtungen | ca. 0,7 |

**Hintergrund:** Einfachglas hat Emissivität ca. 85 %, davon entfallen ca. 2/3 des Wärmeverlustes auf Strahlung, nur 1/3 auf Leitung und Konvektion. Dünne Metalloxidbeschichtung (zumindest einer Glasoberfläche, zum Scheibenzwischenraum hin) senkt Emissivität auf ca. 3 % → Strahlungsaustausch unterbrochen → U-Wert halbiert sich nochmals.

**Edelgasfüllungen im Scheibenzwischenraum (SZR):**
- Argon: häufigste Anwendung, U-Wert ca. 1,1 W/m²K
- Krypton: wirksamer als Argon
- Xenon: am wirksamsten, aber praktisch nicht eingesetzt (Kostengründe)

**Wärmeschutz- vs. Sonnenschutzbeschichtung:**
- Wärmeschutzbeschichtung: minimiert Wärmeverlust nach außen bei hohem Licht- und IR-Eintrag; Ziel: niedrige Emissivität, hohe Transparenz
- Sonnenschutzbeschichtung: minimiert solaren Energieeintrag; Ideal: im sichtbaren Bereich transparent, im restlichen Spektrum opak (Rechteckfilter). Halbleiterbeschichtungen nähern sich diesem Ideal, bringen aber spektrale Inhomogenität und Farbverfälschungen
- Güte einer Sonnenschutzbeschichtung: **Selektivität** = Lichttransmissionsgrad / g-Wert (möglichst groß)

#### 27.5.1 Glaskennwerte

- **Lichttransmissionsgrad τv** (oder τ): relativer Anteil des sichtbaren Lichts, der durchgelassen wird
- **UV-Transmissionsgrad**, **IR-Transmissionsgrad**: bei besonderer Fragestellung
- **g-Wert** (Gesamtstrahlungsdurchgang τe): gesamte eingehende solare Energie inkl. der nach Absorption wieder raumwärts abgegebenen Wärme; Maß für den solaren Energieeintrag
- **U-Wert** (früher k-Wert) [W/m²K]: Wärmedurchgangskoeffizient; multipliziert mit der Temperaturdifferenz ΔT ergibt sich der flächenspezifische Wärmeverlust [W/m²]
- Alle Transmissionsgrößen sind dimensionslos (0–1 bzw. 0–100 %)
- **Streuverhalten** und **Farbneutralität** lassen sich nicht vollständig numerisch klassifizieren; beste Bewertung durch vergleichende Bemusterung bei Tageslicht auf weißem Untergrund

**Übersicht Glaskennwerte klar durchsichtiger Verglasungen (Tab. 27.7):**

| Typ | SZR [mm] | Beschichtung Position | Ug [W/m²K] | τv [%] | ρv außen [%] | g-Wert [%] |
|-----|----------|-----------------------|------------|--------|--------------|------------|
| Einfach 8 mm Float | — | — | 5,7 | 88 | 8 | 80 |
| Einfach 8 mm Weißglas | — | — | 5,7 | 91 | 8 | 90 |
| IV 2-fach 2×4 mm Float / Wärmeschutz | 16 | 3 | 1,1 | 80 | 13 | 61 |
| IV 2-fach 6+4 mm Float / Sonnenschutz | 16 | 2 | 1,1 | 71 | 10 | 43 |
| IV 3-fach 3×4 mm Float / Wärmeschutz | 2×14 | 2+5 | 0,7 | 73 | 19 | 61 |
| IV 3-fach 3×4 mm Float / Sonnenschutz | 2×14 | 2+5 | 0,6 | 63 | 13 | 39 |

Alle Gasfüllungen: Argon. Beschichtungspositionen werden von außen nach innen nummeriert.

Konkretes Beispiel aus den Abbildungen: Wärmeschutzbeschichtung 6 mm auf Position 3 in 2-fach-IV → U-Wert 1,6 W/m²K, τv/g = 77/76; mit Beschichtungen auf Pos. 2 u. 4 → 1,4 W/m²K, τv/g = 77/70. Sonnenschutzverglasung auf Pos. 2 in 2-fach-IV → τv/g = 64/27, U-Wert 1,5 W/m²K.

#### 27.5.2 Lichttransmissionsgrad bei schrägem Lichteinfall

Hersteller geben τ i.d.R. für senkrechten Einfall (τ⊥ oder τ0) an. Für diffus aus dem Halbraum auftreffendes Licht gilt ein allgemeiner Minderungsfaktor von **0,875** gegenüber τ0. Bei Oberlichtern ohne nennenswerte Verbauung ist dieser Faktor anzuwenden. In anderen Fällen ist τ entsprechend der Haupteinfallsrichtung des hellsten Himmelslichts zu gewichten:

```
τ = τ0 × k3
```

k3 berücksichtigt die einfallswinkelabhängige Transmission.

#### 27.5.3 Glasaufbau

Einfachscheiben heute fast ausschließlich als Schutzverglasungen (Überdachungen, Fassaden, Innenbereich), meist als ESG, TVG und/oder VSG.

Zweifach-Isolierverglasung ist Standard; Dreifach-IV aus energetischen Gründen zunehmend verbreitet.

#### 27.5.4 Verglasungsarten

- **Klare (transparente) Gläser:** Standardeinsatz für Fenster und Fassaden; auch durchgefärbt (Graustufen) oder mit pyrolytischer Beschichtung (K-Glas) als Einzel-Sonnenschutzglas
- **Lichtstreuende Gläser:**
  - Strukturierte Gläser / Guss- / Ornamentgläser: Teildurchsicht erhalten, schwer zu IV/VSG verarbeitbar, verschmutzungsanfällig
  - Sandstrahlung: grob, schmutzanfällig → bei IV zum SZR orientieren
  - Ätzmattierung: fein, weniger schmutzanfällig, auch raumseitig möglich (Lichtdecken, verhindert Spiegelungen); Lichtminderung ca. 5 %; Hebt Grünstich hervor → Weißglas empfohlen
  - Milchüberfangglas: stärkste Streuung; Lichtdurchgang um über die Hälfte reduziert; keine Lebhaftigkeit des Tageslichts mehr spürbar; leicht zu reinigen
  - Bedruckung oder Mattfolieneinlage im VSG: stärkere Lichtminderung als Oberflächenbehandlungen; schlechtere Raumwirkung
  - Glasgespinsteinlage (Vlies oder Gewebe zwischen zwei Einfachscheiben, bekannt als Thermolux): keine Durchsicht, aber erhält Lebhaftigkeit des Tageslichts gut; Lichtdurchgang je nach Gespinstdicke um ca. die Hälfte gemindert; von Industriehallen in Museum-Dachverglasungen eingewandert
  - Profilit (U-förmige, aufrecht eingebaute Glasstreifen, außen strukturiert): ebenfalls inzwischen in der Architektur etabliert
- **Lichtlenkende Gläser:**
  - Kapillareinlagen: begrenzte Lenkwirkung, störende Brillanzeffekte bei direktem Sonnenlicht
  - Spiegelraster im SZR (astronomisch konfiguriert): wirksamer Sonnenschutz durch Reflexion des Direktsonnenlichts, lässt nur kühles Nordlicht durch; Transmissionsgrad sinkt mit Sonnenschutzwirkung
  - Prismatische Kunststoffeinsätze: Lichtlenkung mit Dispersion (Regenbogeneffekte) verbunden → nur als oberste Schicht mit darunter liegenden Streumaßnahmen einsetzbar
  - Holographische oder Polarisationsfolien: störende Dispersion verhindert Verbreitung

---

### 27.6 Besonnung

Normative Mindestanforderungen an Besonnungsdauer in Wohnräumen (nach [15]): Ein Wohnraum gilt als ausreichend besonnt bei einer Besonnungsdauer von mindestens **1 Stunde am 17. Januar**. Eine Wohnung ist ausreichend besonnt, wenn mindestens ein Wohnraum diese Bedingung erfüllt.

Planungsrelevante Gründe für Besonnungsuntersuchungen:
- Wertsteigernder Faktor Besonnung (unbestritten, obwohl normativ gering gefordert)
- Dimensionierung von Sonnenwärmeschutz und Blendschutz
- Konfiguration starrer Sonnenschutzblenden geometrisch-astronomisch auf Fensterneigung/-orientierung abgestimmt
- Nutzung von Sonnenenergie (Photovoltaik, Solarthermie, Raumerwärmung)
- Kühllasten-Ermittlung

Sonnenschutzmaßnahmen wirken am wirksamsten **außerhalb** der Isolierverglasung (oder bei Doppelfassaden außerhalb der IV). Für gesamtenergetische Betrachtungen und Solaranlagen sind meteorologische Daten der Wetterdienste heranzuziehen.

#### 27.6.1 Astronomische Gegebenheiten

**Erdbahn und Erdachse:**
- Erde bewegt sich auf leicht elliptischer Bahn um die Sonne (Exzentrizität 0,167, gering genug für Kreisbahnannahme bei Besonnungsberechnungen)
- Bahnebene = Ekliptik
- Erdrotation: 24 h
- Erdachsenneigung: 23° 26,5′ (≈ 23,5°) gegen die Ekliptiknormale
- Präzessionsperiode der Erdachse: ca. 24.000 Jahre → für Planungszwecke als konstant behandelt
- Folge der Achsenneigung: unterschiedliche Tageslängen, Sonnenhöhen und Einstrahlmengen im Tages- und Jahresverlauf, breitengradabhängig → Jahreszeiten

**Wichtige astronomische Lagen der Erde im Jahresverlauf:**
- Äquinoktien (Frühlingspunkt + Herbstpunkt, verbunden durch Äquinoktiallinie): Tag und Nacht gleich lang an allen Erdpunkten; Licht/Schatten-Grenzkreis verläuft durch beide Pole (= Meridian)
- Sommersonnenwende (ca. 21.6.) und Wintersonnenwende (ca. 21.12.) verbunden durch Solstitiallinie
- Nördlicher Wendekreis (Krebs): 23,45° N → Sonne steht am 21.6. um 12 Uhr im Zenit
- Südlicher Wendekreis (Steinbock): 23,45° S → Sonne steht am 21.12. um 12 Uhr im Zenit
- Sonne steht nur zwischen den beiden Wendekreisen (± 23,45°) im Zenit
- Nördlich des Polarkreises: Polarnacht (21.12.) bzw. Mitternachtssonne (21.6.)
- Nullmeridian: durch Greenwich (Grundlage GMT)

#### 27.6.2 Sonnenstandsdiagramme und Zeitumrechnung

**Darstellung:** Sonnenbahnen im Jahresverlauf werden in stereographischer Projektion auf den Horizont bzw. die Grundebene einer Einheits-Hemisphäre projiziert. Vorteil: Sonnenbahnen erscheinen als Kreissegmente. Äußerer Kreisrand = Horizont (h = 0°), Mittelpunkt = Zenit (h = 90°). Sonnenhöhe durch Zirkelschlag auf der Höhenskala ablesbar, Azimut auf der Randskala.

**Astronomische Grundgrößen:**

| Bezeichnung | Symbol |
|-------------|--------|
| Breitengrad | φ |
| Längengrad | λ |
| Sonnenhöhe | h |
| Zenitwinkel | z = 90° − h |
| Sonnenazimut | α |
| h_max am 21. Juni | h_max = 90° − φ + 23,45° |
| h_max am 21. Dezember | h_min = 90° − φ − 23,45° |

(Formeln gelten nur für Breitengrade zwischen Polar- und Wendekreisen)

**Azimutwinkel:** Beginnt bei 0° Nord, wird über Ost bis 360° (= 0° Nord) gezählt.

**Zeitumrechnungen:**

Wahre Ortszeit (WOZ, Sonnenzeit) → Mittlere Ortszeit (MOZ, Uhrenzeit):
```
MOZ = WOZ − ZGL(T)
```
ZGL(T) = Zeitgleichung (berücksichtigt Exzentrizität der Sonnenbahn und Schiefe der Ekliptik)

WOZ → Zonenzeit (z.B. MEZ mit Zentralmeridian Λ = 15° Ost):
```
Zonenzeit = WOZ + (Λ − λ) × 4 min/°
```

Zonenzeit → Sommerzeit:
```
Sommerzeit = Zonenzeit + 1 h
```

#### 27.6.3 Besonnungsuntersuchungsverfahren

**Verfahren 1: Stereographische Projektion**
Die Verbauung wird in richtiger Orientierung in das Sonnenstandsdiagramm des Standort-Breitengrades projiziert. Aus dem resultierenden Diagramm lassen sich auf einen Blick die Besonnungsintervalle über das ganze Jahr für einen räumlichen Untersuchungspunkt ablesen. Beispiel: Südorientiertes Fenster mit starrer Blende zeigt im Sonnenstandsdiagramm, dass direkter Sonnenlichteinfall von April bis August fast vollständig unterbunden ist (nur kurze Ausnahmen in den Früh- und Abendstunden).

**Verfahren 2: Schattenwurf (Raytracing)**
Zeigt die Schattenverteilung im gesamten Raum zu einem bestimmten Zeitpunkt. Klassisch für drei Stichtage berechnet: 21. Dezember, 21. März/September (Tagundnachtgleiche), 21. Juni, jeweils für 12:00 Uhr WOZ.
- 21. Dezember: Tiefe Sonneneinstrahlung weit in den Raum; Schatten nur im Sturzbereich
- Vergleichende Darstellungen verschiedener Jahres- und Tageszeiten ermöglichen Überblick über Besonnbarkeit

Heute werden Schattenwurf-Darstellungen per Computerprogramm mittels Raytracing erzeugt (früher aufwändige Handkonstruktion).

**Ergänzung: Kumulierte Besonnungszeiten für Teilflächen**
Mittels Backwards-Raytracing können kumulative Besonnungszeiten an Stichtagen (oder über frei wählbare Intervalle) für Teilflächen von Fassaden oder Fenstern berechnet werden → flächenanteilsbezogene Übersicht über die Besonnung.

#### 27.6.3.4 Orientierungsabhängige solare Bestrahlung

Die jährliche Gesamtbestrahlung geneigter und orientierter Flächen kann Nomogrammen entnommen oder berechnet werden. Ableseregelwerk: immer entlang der Parallelen zu den Hauptachsen der Isometrie.

Beispiel: Um 60° aufgestellte, nach Osten orientierte, unverbaute Fläche → max. ca. **800 kWh/m² pro Jahr** solare Strahlungsenergie bei mittlerem Himmel (beinhaltet statistische Sonnenscheinwahrscheinlichkeit und atmosphärische Trübungsminderung) für 53° N.

**Solare Tagessummen durch Verglasungen (für 49° N, klarer Himmel, 2-fach-IV mit Wärmeschutzbeschichtung τv = 80 %, g-Wert = 0,6, τe = 0,5):**
- Sommer (Sonne hoch): horizontale Verglasung empfängt erheblich mehr als senkrechte
- Tag-/Nachtgleiche: nach Süden orientierte senkrechte Verglasung übersteigt horizontale
- Winter (Sonne tief): senkrechte Verglasung mit Orientierungen O bis S bis W empfängt mehr als horizontale
- Nach Süden orientierte senkrechte Verglasung hat im Sommer geringsten solaren Eintrag aller Orientierungen (außer Norden)

Korrekturfaktor für abweichenden Gesamtenergiedurchlass:
```
ke = τe / 0,5
```

Voraussetzungen der Berechnungen: AM 1,5 (Airmass), Trübungsfaktor nach Linke T = 2,75 (gibt an, wie vielen ungetrübten Rayleigh-Atmosphären die angesetzte Trübung entspricht).

**Optimale Fensterwahl für passive Solarnutzung:** Senkrechte, nach Süden orientierte Verglasungen bieten beste Kombination aus solaren Wintergewinnen und geringer sommerlicher Überhitzung, besonders in Kombination mit starrer oder beweglicher Blende oberhalb des Fensters.

#### 27.6.4 Blend- und Sonnenschutzmaßnahmen

Sonnenschutz und Blendschutz überschneiden sich konzeptionell. Sonnenschutzmaßnahmen sollen vor Sonnenwärmeeintrag und extremem Lichteintrag bei direkter Besonnung schützen, dienen damit auch zur Blendungsvermeidung. Blendschutz ohne direkte Besonnung (z.B. durch Himmelslicht an Bildschirmarbeitsplätzen) erfordert separate Maßnahmen (z.B. Blendschutzrollos, Jalousetten). Wenn nur eine Maßnahme möglich ist, muss diese beide Funktionen erfüllen.

**Sonnenschutzrollos:**
- Vorzugsweise außerhalb der wärmeisolierenden Verglasung anordnen
- Lichttransmissionsgrad muss so niedrig sein, dass Höchstbeleuchtungsstärken im Raum selbst bei direkter Besonnung eingehalten werden
- **Screen (netzartig, mit Öffnungen):** Durchsicht erhalten; openess factor; Lichttransmissionsgrad bei strikt geforderten Höchstbeleuchtungsstärken im einstelligen Prozentbereich; Risiko lokal hoher Beleuchtungsstärken durch geringe Streuung; bei nicht voller Besonnung schnell zu dunkle Räume
- **Ideal lichtstreuender Behang (Lambertsche Abstrahlung):** Hoher Lichtstrom bei direkter Besonnung wird um den integralen Transmissionsgrad gemindert, aber gut im Raum verteilt; keine lokalen Spitzenwerte; deshalb kann der Transmissionsgrad bei gleicher Höchstbeleuchtungsstärkenanforderung deutlich höher sein als beim Screen
