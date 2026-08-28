# Lehrbuch der Bauphysik — Teil 17
> Quelle: Lehrbuch der Bauphysik (buecher) · Seiten 681-720.

Dieser Teil schließt Kapitel 22 (Bauakustik) mit den Themen Trittschallübertragung bei Holzbalkendecken und Treppen, Geräusche aus Gebäudetechnik sowie bauakustischen Anforderungen und Planungsregeln ab. Anschließend beginnt Kapitel 23 über Schall aus Anlagen der Gebäudetechnik, mit Schwerpunkt auf elastischer Maschinenlagerung und raumlufttechnischen Anlagen.

## Inhalt

### 22.3 Trittschallübertragung — Berechnungsformeln und Korrekturen

#### Berechnung des äquivalenten bewerteten Norm-Trittschallpegels
Der äquivalente bewertete Norm-Trittschallpegel Ln,eq,0,w hängt von der flächenbezogenen Masse der Rohdecke m′ ab (Bezugsmasse m′0 = 1 kg/m²). Formel (22.66):

```
Ln,eq,0,w = 164 − 35 · lg(m′/m′0)
```

#### Korrekturwert K für Flankenübertragung (Massivdecken ohne schalldämmende Unterdecken)
Formel (22.67) gilt für Massivdecken ohne schalldämmende Unterdecken:

```
K = 0,6 · lg(m′s / m′f,m) + 5,5   [dB]
```

- m′s = flächenbezogene Masse der Rohdecke
- m′f,m = mittlere flächenbezogene Masse der unverkleideten massiven flankierenden Bauteile
- Gültigkeitsbereich: 100 kg/m² ≤ m′s ≤ 900 kg/m², 100 kg/m² ≤ m′f,m ≤ 500 kg/m²
- Gilt nur für m′f,m ≤ m′s; bei m′f,m > m′s wird K = 0 dB angesetzt

Bei Massivdecken **mit** schalldämmenden Unterdecken (ΔRw ≥ 10 dB, m′f,m ≤ m′s), Formel (22.68):

```
K = 5,3 · lg(m′s / m′f,m) + 10,2   [dB]
```

Hintergrund: Schalldämmende Unterdecken reduzieren die Trittschallübertragung der Trenndecke merklich, haben jedoch keinen Einfluss auf die Schallübertragung auf flankierende Bauteile.

#### Trittschallminderung schwimmender Estriche (Formel 22.69)
Für Mörtelestriche aus Zement, Calciumsulfat, Magnesia oder Kunstharz:

```
ΔLw = 13 · lg(m′) + 14,2 · lg(s′) − 20,8
```

- Gültig für: 60 kg/m² ≤ m′ ≤ 160 kg/m² und 6 MN/m³ ≤ s′ ≤ 50 MN/m³
- m′ = flächenbezogene Masse der Estrichplatte
- s′ = dynamische Steifigkeit der Dämmschicht

Für schwimmende Gussasphaltestriche oder Fertigteilestrich, Formel (22.70):

```
ΔLw = 0,21 · m′ − 5,45 · s′ + 0,46 · m′ · lg(s′) − 23,8
```

- Gussasphalt: 58 kg/m² ≤ m′ ≤ 87 kg/m², 15 MN/m³ ≤ s′ ≤ 50 MN/m³
- Fertigteilestrich: 15 kg/m² ≤ m′ ≤ 40 kg/m², 15 MN/m³ ≤ s′ ≤ 40 MN/m³

#### Resultierende dynamische Steifigkeit bei übereinander liegenden Dämmschichten
Bei zwei durchgehend verlegten Trittschalldämmschichten ergibt sich die Gesamt-Steifigkeit s′tot aus den Einzelsteifigkeiten s1 und s2, Formel (22.71):

```
1/s′tot = 1/s1 + 1/s2
```

#### Weichfedernde Bodenbeläge (Tab. 22.21, DIN 4109-34:2016)
Bei Kombination Estrich + weichfedernder Bodenbelag gilt: Nur die höhere Trittschallminderung (Estrich oder Belag) wird berücksichtigt.

Bewertete Trittschallminderung ΔLw weichfedernder Bodenbeläge auf Massivdecken:

| Bodenbelag | ΔLw [dB] |
|---|---|
| Linoleum-Verbundbelag | 14 |
| PVC-Verbundbelag mit Schaumstoff-/Korkment-Träger | 16 |
| Nadelvlies 5 mm | 20 |
| Polteppich 4 mm, Unterseite geschäumt | 19 |
| Polteppich 4 mm, Unterseite ungeschäumt | 19 |
| Polteppich 6 mm, Unterseite geschäumt | 24 |
| Polteppich 6 mm, Unterseite ungeschäumt | 21 |
| Polteppich 8 mm, Unterseite geschäumt | 28 |
| Polteppich 8 mm, Unterseite ungeschäumt | 24 |

### 22.3.3 Trittschallübertragung von Holzbalkendecken

Alter oder einfach konstruierter Holzbalkendecken-Schallschutz ist deutlich schlechter als bei Massivdecken mit schwimmendem Estrich. Ursachen:
- Ungünstige Resonanzfrequenzen der beteiligten Masse-Feder-Systeme
- Bauakustisch ungünstige Schichtdicken (Koinzidenzgrenzfrequenzen)
- Schallübertragung über Balken und steife Befestigung der Deckenbekleidung

Rechnerische Prognose ist wegen vieler Einflussparameter kaum möglich → Messwerte erforderlich.

Schwimmend verlegte Deckenaufbauten verbessern Trittschallschutz von Holzbalkendecken, erreichen jedoch nicht die Trittschallminderung schwimmender Estriche auf Massivdecken. In erster Näherung ist bei Holzbalkendecken nur mit dem halben Wert der Trittschallminderung (ΔLw) zu rechnen.

#### Konstruktive Schichtenfolge für bauakustisch hochwertige Holzbalkendecken (von oben nach unten)

**Variante 1:**
- Estrich in verlorener Stahlblechschalung aus Schwalbenschwanzplatten, gelagert auf Elastomerstreifen
- Mit oder ohne obere Deckenbeplankung

**Variante 2:**
- Estrich
- Trittschalldämmung
- Biegeweiche Beschwerung (Schüttungen oder kleinformatige Betonplatten)
- Holzwerkstoffplatten als obere Deckenbeplankung

**Allgemein:**
- Bedämpfung der Gefache
- Keine festen Verbindungen zwischen Unterkonstruktion für Deckenbekleidung und Holzbalken (Federschienen oder Unterkonstruktion hängt mit ca. 1 mm Abstand zum Holzbalken in den Schrauben)
- Beplankung aus n × 12,5 mm Gipskartonplatten

Wichtiger Hinweis: Konstruktionen mit zeitgemäßem Norm-Trittschallpegel weisen Direktschalldämm-Maße auf, die deutlich über den Anforderungen an den Luftschallschutz liegen. Daher muss bei der Planung von Holzhäusern zunächst dem Trittschallschutz Priorität eingeräumt werden. Bei ausreichend niedrigem Norm-Trittschallpegel kann in Holzhäusern mit leichtem Innenausbau (biegeweiche Schalen, geringe Flankenschallübertragung) sehr guter Schallschutz erzielt werden.

#### Vertikale Trittschallübertragung über Decken in Holzbauweise (DIN 4109-2:2018, Formel 22.72)

```
L′n,w = Ln,w + K1 + K2
```

- K1 = Korrekturwert für Flankenübertragung auf Weg Df (Decke → flankierende Wände im Empfangsraum)
- K2 = Korrekturwert für Flankenweg DFf (Estrichplatte → flankierende Wände Senderaum → flankierende Wände Empfangsraum); besonders relevant im Holz-/Leicht-/Trockenbau (berücksichtigt Randanschluss des schwimmenden Estrichs)
- Rechnerischer Trittschallschutznachweis ist bei Holzbauweise nicht möglich

#### Korrekturwert K1 bei Holzdecken (Tab. 22.23, DIN 4109-2:2016)

| Wandaufbau im Empfangsraum | 2× GK an Federschiene | 1× GK an Federschiene | GK direkt/Lattung, offene Holzbalkendecke etc. |
|---|---|---|---|
| GK (ρ ≥ 680 kg/m³) + HW (ρ ≥ 650 kg/m³) | K1 = 6 dB | K1 = 3 dB | K1 = 1 dB |
| Gipsfaserplatte GF (ρ ≥ 1100 kg/m³) | K1 = 7 dB | K1 = 4 dB | K1 = 1 dB |
| HW (ρ > 650 kg/m³) oder Holz-/Holzwerkstoffelement | K1 = 9 dB | K1 = 5 dB | K1 = 4 dB |

#### Korrekturwert K2 bei Holzdecken (Tab. 22.24, DIN 4109-2:2018)

Estrichaufbauten (Definitionen):
- **CT/WF:** Mineralisch gebundener Estrich auf Holzweichfaser-Trittschalldämmplatten, Randdämmstreifen > 5 mm (Mineralwolle oder PE-Schaum) oder Gussasphaltestrich auf Mehrschicht-Trittschalldämmplatte aus Blähperlit/Mineralwolle
- **CT/MW:** Mineralisch gebundener Estrich auf Mineralwolle- oder EPS-Trittschalldämmplatten, Randdämmstreifen > 5 mm, oder Gussasphaltestrich auf Blähperlit/Mineralwolle-Mehrschicht
- **TE:** Fertigteilestrich auf Mineralwolle-, EPS- oder Holzweichfaser-Trittschalldämmplatten, Randdämmstreifen > 5 mm

K2-Werte (Auszug) für Wandaufbau GK + HW oder GF:

| Estrich | Ln,DFf,w [dB] | K2 für Ln,w+K1 = 35...55 dB |
|---|---|---|
| CT/WF | 44 | 10...0 dB (fallend von 35 bis >55) |
| CT/MW | 40 | 6...0 dB |
| TE | 38 | 5...0 dB |

Für Wandaufbau HW oder Holz-/Holzwerkstoffelement:

| Estrich | Ln,DFf,w [dB] | K2 für Ln,w+K1 = 35...55 dB |
|---|---|---|
| CT/WF | 46 | 11...0 dB |
| CT/MW | 45 | 10...0 dB |
| TE | 42 | 8...0 dB |

#### Berechnungsbeispiel Trittschalldämmung nach DIN 4109-2:2018 — Massivdecke (Tab. 22.22)

Aufbau: 180 mm Stahlbetondecke (ρ = 2400 kg/m³) mit 45 mm Zementestrich auf Dämmung (s′ = 10 MN/m³); Flanken: Außenwand 175 mm Kalksandstein (ρ = 1700 kg/m³) verputzt + WDVS; Innenwände 115 mm KS (ρ = 1700 kg/m³) beidseitig verputzt; Wohnungstrennwand 240 mm KS verputzt; Empfangsraumvolumen 2,5 m³

| Kennwert | Wert |
|---|---|
| Flächenbezogene Masse Rohdecke m′s | 432 kg/m² |
| Äquivalenter Norm-Trittschallpegel Ln,eq,0,w | 71,8 dB |
| Flächenbezogene Masse Estrich m′ | 90 kg/m² |
| Dynamische Steifigkeit s′ | 10 MN/m³ |
| Trittschallminderung ΔLw | 32,0 dB |
| Mittlere flächenbezogene Masse flankierende Bauteile m′f,m | 292 kg/m² |
| Korrekturwert K | 1,5 dB |
| Norm-Trittschallpegel L′n,w | 41,3 dB |
| Standard-Trittschallpegel L′nT,w | 40,7 dB |
| Sicherheitsbeiwert uprog | 3 dB |
| Vergleichswert L′n,w + uprog | 44,3 dB |

#### Berechnungsbeispiel Trittschalldämmung — Holzbalkendecke (Tab. 22.26)

Aufbau: 60 mm Zementestrich CT (ρ = 2000 kg/m³) auf Mineralwolledämmung MW (s′ = 6 MN/m³), trockene Schüttung (m′ = 45 kg/m²) in Pappwaben, 22 mm OSB-Platte, 220 mm Holzbalken mit Hohlraumbedämpfung, 27 mm Federschiene, 12,5 mm Gipskartonplatte; Flanken: Holztafelwände (GK 9,5–12,5 mm ρ ≥ 680 kg/m³ + HW 13–22 mm ρ ≥ 650 kg/m³); Empfangsraumvolumen 46,9 m³

| Kennwert | Wert |
|---|---|
| Norm-Trittschallpegel Ln,w | 34 dB |
| Korrektur Weg Df (K1) | 3 dB |
| Korrektur Weg DFf (K2) | 5 dB |
| Norm-Trittschallpegel L′n,w | 42 dB |
| Standard-Trittschallpegel L′nT,w | 40,2 dB |
| Sicherheitsbeiwert uprog | 3 dB |
| Vergleichswert L′n,w + uprog | 45 dB |

#### Holzbalkendecken-Konstruktionen und bauakustische Kennwerte (Tab. 22.25, DIN 4109-33:2016)

| Schichtenfolge (von oben) | Rw (C; Ctr) | Ln,w (Ci) |
|---|---|---|
| Holzwerkstoffplatte / Balken / Hohlraumbedämpfung / Lattung / GK 12,5 mm | 63 (−5; −11) dB | 54 (2) dB |
| Trockenestrich m′≥29 kg/m² / Dämmplatte s′≤30 MN/m³ / Schüttung m′≥45 kg/m² / HWP / Balken / Hohlraumbedämpfung / Federschiene / GK 12,5 mm | 69 (−4; −11) dB | 41 (2) dB |
| Estrich mineralisch m′≥120 kg/m² / Mineralwolledämmung s′≤6 MN/m³ / Betonplatten m′≥100 kg/m² / Brettstapeldecke | ≥ 70 dB | 45 (−1) dB |
| Estrich mineralisch m′≥120 kg/m² / Mineralwolledämmung s′≤6 MN/m³ / HWP / Balken / Hohlraumbedämpfung / Federschiene / GK 12,5 mm | 70 (−3; −9) dB | 46 (0) dB |
| Estrich mineralisch m′≥120 kg/m² / Mineralwolledämmung s′≤6 MN/m³ / Betonplatten m′≥100 kg/m² / HWP / Balken / Hohlraumbedämpfung / Federschiene / GK 12,5 mm | ≥ 70 dB | 30 (0) dB |
| Zementestrich in Trapezblech / Elastomerlager auf Balken / Balken / Hohlraumbedämpfung / Federschiene / Gipskarton 2×12,5 mm | 77 dB | 38 dB |

### 22.3.4 Trittschallübertragung von Treppen

Um Trittschall aus Treppenhäusern in Mehrfamilienwohnhäusern zu reduzieren, sind elastisch gelagerte Konstruktionen erforderlich. Mögliche Varianten:

1. Treppenpodeste mit schwimmenden Estrichen + Treppenläufe mit elastisch gelagerten Stufen oder trittschalldämmenden Belägen
2. Treppenpodeste mit schwimmenden Estrichen + seitlich entkoppelte Fertigteiltreppenläufe, elastisch auf Podesten gelagert
3. Elastisch gelagerte Treppenpodeste + seitlich entkoppelte Treppenläufe

#### Leichte Montagetreppen
Kommen insbesondere in Wohnungen, Reihen- und Doppelhäusern vor. Problem: Die geforderten bewerteten Norm-Trittschallpegel L′n,w werden zwar eingehalten, Nutzer klagen jedoch über subjektiv unzureichenden Schutz — insbesondere bei tiefen Frequenzen. Ursache der Diskrepanz zwischen gutem Messwert (nach DIN EN ISO 717-2:2021) und tatsächlicher Belästigung: Tiefe Frequenzen werden bei der Einzahlangabe L′n,w nicht berücksichtigt; das Norm-Trittschallhammerwerk bildet die tatsächliche Anregung beim Begehen nicht ausreichend nach.

Empfehlung aus bauakustischer Sicht: **Wangentreppen** bevorzugen (weniger Auflagerpunkte, keine Befestigung an der Trennwand zum Nachbarn). Bolzentreppen — bei denen jede Stufe an der Trennwand gelagert ist — stellen ein größeres trittschallspezifisches Problem dar.

Hinweis: Kein Nachweisverfahren nach DIN 4109-2:2018 für leichte Montagetreppen vorhanden.

#### Äquivalente bewertete Norm-Trittschallpegel für Treppenkonstruktionen in Massivbauweise (Tab. 22.27, DIN 4109-32:2016)

| Treppenkonstruktion | Ln,eq,0,w | L′n,w |
|---|---|---|
| Podest aus Stahlbeton, fest verbunden mit einschaliger biegesteifer Treppenraumwand (m′ ≥ 380 kg/m²) | 63 dB | 67 dB |
| Treppenlauf Stahlbeton, abgesetzt von einschaliger biegesteifer Treppenraumwand | 63 dB | 67 dB |
| Treppenlauf Stahlbeton, abgesetzt von einschaliger biegesteifer Treppenraumwand (Variante) | 60 dB | 64 dB |
| Podest Stahlbeton, fest verbunden mit Treppenraumwand, durchgehende Gebäudetrennfuge | ≤ 50 dB | ≤ 47 dB |
| Treppenlauf abgesetzt, durchgehende Gebäudetrennfuge | ≤ 43 dB | ≤ 40 dB |
| Treppenlauf abgesetzt, durchgehende Gebäudetrennfuge, elastisch auf Podest gelagert | 35 dB | 39 dB |

### 22.3.5 Gehschall im eigenen Raum

Gehschall bezeichnet die Lärmbelastung durch Gehen im eigenen Raum (im Gegensatz zu Trittschall, der Nachbarn betrifft). Besonders problematisch bei schwimmend verlegten Laminatböden, die großflächig Schall in den eigenen Raum abstrahlen. Bauordnungsrechtlich ohne Relevanz — man stört nur sich selbst.

### 22.4 Geräusche aus gebäudetechnischen Anlagen

Installationsgeräusche aus fremden Wohnungen und Geräusche aus Gebäudetechnik sind häufige Beanstandungsursachen. Maßnahmenhierarchie:

**Primär:** Geeignete Bauprodukte der technischen Gebäudeausrüstung wählen

**Sekundär (bauliche Maßnahmen):**
- Grundrissgestaltung, Kapselungen, Körperschall- und Luftschalldämmung verbessern, schallabsorbierende Bekleidungen

**Aufzugschächte:** Bei direktem Anschluss an Aufenthaltsräume → doppelschalige Ausführung prüfen

**Armaturen Armaturengruppe I:**
- Bei nicht unmittelbar angrenzenden schutzbedürftigen Räumen dürfen Armaturen und Wasserleitungen an Wänden mit m′ ≥ 220 kg/m² befestigt werden (entspricht Musterinstallationswand Massivbau nach DIN 4109-36:2016)

**Installationen im Leichtbau:**
- Befestigung an Wänden, die mindestens dem Standard der Leichtbau-Musterinstallationswand nach DIN 4109-36:2016 entsprechen (2 × 12,5 mm Gipsplatten an Wand und Vorwandinstallationswand; Vorwandinstallationswand mit 75 mm Hohlraumtiefe, Hohlraumbedämpfung)
- Schutzbedürftige Räume dürfen nicht unmittelbar angrenzen

**Alle anderen Situationen:** Besonderer Nachweis mit bauakustischen Messungen erforderlich

### 22.5 Bauakustische Anforderungen

#### Dreistufiges Anforderungssystem

**1. Bauordnungsrechtlicher Schallschutz** (zwischen Wohnungen und fremden Arbeitsbereichen):
- Grundlage: Landesbauordnungen und Technische Baubestimmungen (eingeführte Normenteile DIN 4109)
- Dienen dem Gesundheitsschutz der Bewohner

**2. Zivilrechtlich geschuldeter Schallschutz:**
- Über bauordnungsrechtliche Anforderungen hinaus müssen die allgemein anerkannten Regeln der Technik eingehalten werden
- Diese sind dynamisch und projektspezifisch durch Vertragsauslegung zu ermitteln
- Nutzerspezifische Anforderungen (Vertraulichkeit, Komfort, Lebensqualität) zu berücksichtigen
- Empfehlungen: VDI 4100:2012 (SSt I bis SSt III) oder DIN 4109-5:2020

**3. Schallschutz im eigenen Wohn-/Arbeitsbereich:**
- Nicht Bestandteil des Bauordnungsrechts → keine DIN 4109-Anforderungen
- Hinweise in VDI 4100:2012 (Schallschutzstufen SSt EB I und SSt EB II)

Empfehlung: Schallschutzanforderungen möglichst präzise im Bauvertrag definieren.

#### Berechnung des geforderten gesamten bewerteten Bau-Schalldämm-Maßes gegen Außenlärm (DIN 4109-1:2018, Formel 22.73)

```
R′w,ges = La − KRaumart
```

KRaumart-Werte:
- Bettenräume in Krankenanstalten und Sanatorien: 25 dB
- Aufenthaltsräume in Wohnungen, Unterrichtsräume, Übernachtungsräume in Beherbergungsstätten: 30 dB
- Büros: 35 dB

Mindestwerte unabhängig vom Außenlärmpegel:
- Bettenräume: R′w,ges ≥ 35 dB
- Aufenthaltsräume: R′w,ges ≥ 30 dB

Korrektur KAL für Fassadenfläche SS und Raumgrundfläche SG (Formel 22.74):

```
KAL = 10 · lg(0,8 · SS / SG)
```

#### Ermittlung der Standard-Schallpegeldifferenz nach Vertraulichkeitskriterien (VDI 4100:2012 Anhang A, Formel 22.75)

```
DnT,w = LWA − LGA − ΔL − 6 + 10·lg(TS/T0) − 10·lg(VS/1 m³) + (...)
```

Eingangsgrößen aus Tab. 22.31 (VDI 4100:2012):

| Kennwert | SSt I | SSt II | SSt III |
|---|---|---|---|
| A-bewerteter Schallleistungspegel LWA | 78 dB | 78 dB | 78 dB |
| Grundgeräuschpegel im Empfangsraum LGA | 20 dB | 20 dB | 18 dB |
| Schallpegeldifferenz ΔL | 4 dB | 7 dB | 10 dB |
| DnT,w (Beispiel: T = 0,5 s, VS = 50 m³) | 56 dB | 59 dB | 64 dB |

#### Lärmpegelbereiche und maßgeblicher Außenlärmpegel (Tab. 22.29, DIN 4109-1:2018)

| Lärmpegelbereich | Maßgeblicher Außenlärmpegel La |
|---|---|
| I | 55 dB |
| II | 60 dB |
| III | 65 dB |
| IV | 70 dB |
| V | 75 dB |
| VI | 80 dB |
| VII | > 80 dB |

#### Anforderungen für Bauteile zwischen besonders lauten Räumen und schutzbedürftigen Räumen (Tab. 22.30, DIN 4109-1:2018)

| Raumart | Anforderung |
|---|---|
| Betriebsräume Handwerk/Gewerbe, 75 ≤ LAF ≤ 80 dB(A) — Wände und Decken | R′w ≥ 57 dB |
| Betriebsräume Handwerk/Gewerbe, 81 ≤ LAF ≤ 85 dB(A) — Wände und Decken | R′w ≥ 62 dB |
| Betriebsräume Handwerk/Gewerbe — Fußböden | L′n,w ≤ 43 dB |
| Gasträume, nur bis 22:00 Uhr, 75 ≤ LAF ≤ 80 dB(A) — Wände und Decken | R′w ≥ 55 dB |
| Gasträume, nur bis 22:00 Uhr — Fußböden | L′n,w ≤ 43 dB |
| Gasträume, auch nach 22:00 Uhr, LAF ≤ 85 dB(A) — Wände und Decken | R′w ≥ 62 dB |
| Gasträume, auch nach 22:00 Uhr, LAF ≤ 85 dB(A) — Fußböden | L′n,w ≤ 33 dB |
| Gasträume, auch nach 22:00 Uhr, 85 ≤ LAF ≤ 95 dB(A) — Wände und Decken | R′w ≥ 72 dB |
| Gasträume, auch nach 22:00 Uhr, 85 ≤ LAF ≤ 95 dB(A) — Fußböden | L′n,w ≤ 28 dB |

#### Anforderungen und Empfehlungen für Wohngebäude und andere Nutzungen (Tab. 22.28, Auszug)

| Bauteil | DIN 4109-1:2018 Mindest | DIN 4109-5:2020 erhöht | VDI 4100:2012 SSt I/II/III | DIN 4109:1989 | DIN 4109 BB2:1989 |
|---|---|---|---|---|---|
| Wohnungstrennwände | R′w ≥ 53 dB | R′w ≥ 56 dB | DnT,w ≥ 56/59/64 dB | R′w = 53 dB | R′w ≥ 55 dB |
| Wohnungstrenndecken (Luft) | R′w ≥ 54 dB | R′w ≥ 57 dB | DnT,w ≥ 56/59/64 dB | R′w = 54 dB | R′w ≥ 55 dB |
| Wohnungstrenndecken (Tritt, Massiv) | L′n,w ≤ 50 dB | L′n,w ≤ 45 dB | L′nT,w ≤ 51/44/37 dB | L′n,w = 53 dB | L′n,w ≤ 46 dB |
| Wohnungstrenndecken (Tritt, Holz) | L′n,w ≤ 53 dB | L′n,w ≤ 45 dB | — | — | — |
| Treppenläufe und -podeste | L′n,w ≤ 53 dB | L′n,w ≤ 47 dB | L′nT,w ≤ 51/44/37 dB | L′n,w = 53 dB | L′n,w ≤ 46 dB |
| Türen in Flure von Wohnungen | Rw ≥ 27 dB | Rw ≥ 32 dB | DnT,w > 45/50/55 dB | Rw = 27 dB | Rw ≥ 37 dB |
| Türen in Wohnungsaufenthaltsräume | Rw ≥ 37 dB | Rw ≥ 42 dB | DnT,w ≥ 56/59/64 dB | Rw = 37 dB | — |
| Haustrennwände Reihenhäuser (nicht unterkellert) | R′w ≥ 59 dB | R′w ≥ 62 dB | DnT,w ≥ 65/69/73 dB | R′w = 57 dB | R′w ≥ 67 dB |
| Haustrennwände Reihenhäuser (mind. ein Geschoss darunter) | R′w ≥ 62 dB | R′w ≥ 64–67 dB | DnT,w ≥ 65/69/73 dB | R′w = 57 dB | R′w ≥ 67 dB |
| Decken in Einfamilien-Reihenhäusern (horizontal) | L′n,w ≤ 41 dB | L′n,w ≤ 36 dB | L′nT,w ≤ 46/39/32 dB | L′n,w = 48 dB | L′n,w ≤ 38 dB |
| Decken Einfamilien-Reihenhäuser (Bodenplatte auf Erdreich) | L′n,w ≤ 46 dB | L′n,w ≤ 41 dB | — | — | — |
| Treppenläufe/-podeste Einfamilien-Reihenhäuser | L′n,w ≤ 46 dB | L′n,w ≤ 41 dB | L′nT,w ≤ 46/39/32 dB | L′n,w = 53 dB | L′n,w ≤ 46 dB |
| Wände zw. Übernachtungsräumen Beherbergungsstätten | R′w ≥ 47 dB | R′w ≥ 52 dB | — | R′w = 47 dB | R′w ≥ 52 dB |
| Türen zwischen Fluren und Übernachtungsräumen | Rw ≥ 32 dB | Rw ≥ 37 dB | — | Rw = 32 dB | Rw ≥ 37 dB |
| Wände zw. Krankenräumen in Krankenhäusern | R′w ≥ 47 dB | R′w ≥ 52 dB | — | R′w = 47 dB | R′w ≥ 52 dB |
| Türen zwischen Fluren und Krankenräumen | Rw ≥ 32 dB | Rw ≥ 52 dB | — | Rw = 32 dB | Rw ≥ 37 dB |
| Türen zw. Untersuchungs- und Sprechzimmern | Rw ≥ 37 dB | Rw ≥ 52 dB | — | Rw = 37 dB | — |
| Wände zw. Unterrichtsräumen in Schulen | R′w ≥ 47 dB | — | — | R′w = 47 dB | — |
| Wände zw. Unterrichtsräumen und besonders lauten Räumen | R′w ≥ 55 dB | — | — | R′w = 55 dB | — |
| Decken zw. Unterrichtsräumen in Schulen | R′w ≥ 55 dB, L′n,w ≤ 53 dB | — | — | R′w = 55 dB, L′n,w = 53 dB | — |
| Türen zw. Unterrichtsräumen und Fluren | Rw ≥ 32 dB | — | — | Rw = 32 dB | — |
| Gebäudetechnik-Geräuschpegel in fremden Wohnräumen | LAF,max,n ≤ 30 dB(A) | LAF,max,n ≤ 27 dB(A) (MFH) | LAF,max,nT ≤ 30/27/24 dB(A) | — | — |

#### Schallschutzstufen im eigenen Wohn-/Arbeitsbereich (Tab. 22.32, VDI 4100:2012)

| Kennwert | SSt EB I | SSt EB II |
|---|---|---|
| Luftschallschutz (Wände ohne Türen, Decken) | DnT,w = 48 dB | DnT,w = 52 dB |
| Luftschallschutz offene Grundrisse (Wände mit Tür) | DnT,w = 26 dB | DnT,w = 31 dB |
| Trittschallschutz | L′nT,w = 53 dB | L′nT,w = 46 dB |
| Gebäudetechnik-Schalldruckpegel im eigenen Bereich | LAF,max,nT = 35 dB(A) | LAF,max,nT = 30 dB(A) |

#### Wahrnehmbarkeit von Geräuschen in Abhängigkeit von der Schallschutzstufe (Tab. 22.33, VDI 4100:2012)

Grundgeräuschpegel 20 dB(A) als Bezugspegel:

| Geräusch | SSt I | SSt II | SSt III |
|---|---|---|---|
| Laute Sprache | undeutlich verstehbar | kaum verstehbar | im Allgemeinen nicht verstehbar |
| Sprache angehobener Sprechweise | im Allgemeinen kaum verstehbar | im Allgemeinen nicht verstehbar | nicht verstehbar |
| Sprache normaler Sprechweise | im Allgemeinen nicht verstehbar | nicht verstehbar | nicht hörbar |
| Sehr laute Musikpartys | sehr deutlich hörbar | deutlich hörbar | noch hörbar |
| Musik in normaler Lautstärke | noch hörbar | kaum hörbar | nicht hörbar |
| Spielende Kinder | hörbar | noch hörbar | kaum hörbar |
| Gehgeräusche | im Allgemeinen kaum störend | im Allgemeinen nicht störend | nicht störend |
| Haushaltsgeräte | noch hörbar | kaum hörbar | im Allgemeinen nicht hörbar |

### 22.6 Bauakustische Planung

Bauakustische Planung erfolgt nach den Leistungsphasen der HOAI (aktuell 2021). Bauakustik zählt gemäß HOAI 2021 Anlage 1 zu den Beratungsleistungen.

#### Honorarzonen für bauakustische Planung

- **Honorarzone I (geringe Anforderungen):** Wohnhäuser, Heime, Schulen, Verwaltungsgebäude und Banken mit durchschnittlicher technischer Ausrüstung
- **Honorarzone II (durchschnittliche Anforderungen):** Heime, Schulen, Verwaltungsgebäude mit überdurchschnittlicher Ausstattung, Wohnhäuser mit versetzten Grundrissen, Wohnhäuser mit Außenlärmbelastung, Hotels (soweit nicht HZ III), Universitäten und Hochschulen, Krankenhäuser (soweit nicht HZ III), Erholungsgebäude, Versammlungsstätten (soweit nicht HZ III), Werkstätten mit schutzbedürftigen Räumen
- **Honorarzone III (hohe Anforderungen):** Hotels mit umfangreicher Gastronomie, gemischt genutzte Gebäude (Gewerbe + Wohnen), Krankenhäuser in bauakustisch ungünstigen Lagen, Theater-/Konzert-/Kongressgebäude, Tonstudios, akustische Messräume

#### Leistungsphasen der bauakustischen Planung

1. Grundlagenermittlung, Schallschutzanforderungen festlegen
2. Mitwirkung Vorplanung, Gesamtkonzept + Rechenmodelle erstellen
3. Mitwirkung Entwurfsplanung, Bauteile bemessen
4. Mitwirkung Genehmigungsplanung, Schallschutznachweis aufstellen
5. Mitwirkung Ausführungsplanung, Durcharbeiten unter Berücksichtigung integrierter Fachplanungen
6. Mitwirkung Vorbereitung Vergabe, Beiträge zu Ausschreibungsunterlagen
7. Mitwirkung Vergabe, Angebote prüfen und bewerten

**Besondere Leistungen** (Auswahl):
- Fachübergreifender Bauteilkatalog erstellen
- Bauakustische Messungen
- Leistungen des Schallimmissionsschutzes
- Mitwirkung bei Audits in Zertifizierungsprozessen

### 22.6.1 Allgemeine Konstruktionshinweise

- Laute und schutzbedürftige Räume durch geeignete Grundrissgestaltung gruppieren
- **Massivbau, einschalig:** Wände mindestens 175 mm Dicke, möglichst schwer; Schallängsleitung über leichte flankierende Bauteile beachten
- **Massivbau, zweischalig:** Möglichst große Luft- oder Dämmstoffschichten zwischen Schalen; Schallbrücken unbedingt vermeiden
- **Skelettbau:** Möglichst große Luft- oder Dämmstoffschichten zwischen biegeweichen Schalen; Plattendicken max. 15 mm; insbesondere Flankenübertragung an leichten Fassaden beachten
- **Fenster:** Möglichst großer Abstand zwischen Glasscheiben; unterschiedliche Scheibendicken verwenden
- **Türen:** Umlaufende Dichtungsebenen; schweres, aber nicht biegesteifes Türblatt; Stahlzargen vermörteln; Mineralwolle hinter Holzzargen; Estrich und Bodenbelag unter Tür trennen

### 22.6.2 Wohngebäude

Planungsschritte für Wohngebäude mit mehreren Einheiten:
- Geschuldeten Schallschutz bestimmen; bauakustische Anforderungen aus Bauordnungsrecht und allgemein anerkannten Regeln der Technik festlegen
- Grundrissgestaltung beeinflussen (Anordnung von Bädern und Toiletten besonders wichtig)
- Bauweise beeinflussen
- Rechnerischer Nachweis für Luft- und Trittschallschutz zwischen Wohnungen, Luftschallschutz gegen Außenlärm, Installationsgeräusche

### 22.6.3 Verwaltungsgebäude

Besonders zu beachten:
- Geschuldeten Schallschutz zwischen Nutzungseinheiten und innerhalb eigener Arbeitsbereiche bestimmen
- Bauweise der Außenwände beeinflussen (wichtig bei leichten Vorhangfassaden wegen erhöhter Flankenübertragung)
- Bauweise in eigenen Arbeitsbereichen beeinflussen (Problematik: flexibler Ausbau versus getrennte Unterdecken und Hohlraumböden)
- Rechnerischer Nachweis für Luft- und Trittschallschutz, Außenlärm, Installationsgeräusche

### 22.6.4 Gebäude mit hohen bauakustischen Anforderungen (Tonstudios, Musikhochschulen, Kinos)

DIN 4109:2018 reicht für diese Gebäude nicht immer aus. Planungsschritte:
- Detaillierte Abstimmung des Schallschutzes mit Nutzern (ggf. frequenzabhängige Anforderungen)
- Grundrissgestaltung: Sensible Räume nicht neben- oder übereinander anordnen
- Bauweise: Massivbauweise erfordert Raum-in-Raum-Konstruktion oder biegeweiche Vorsatzschalen
- Rechnerischer Nachweis, soweit möglich; häufig bauakustische Messungen erforderlich

### 22.6.5 Unsicherheiten bei der bauakustischen Planung

Streuungen entstehen durch:
- Unterschiedliche Prüfstandsbedingungen (Bauteilankopplung)
- Schwankungen bei der Schallfeldabtastung
- Unterschiedliche Bauteilflächen (verschiedene Modenausbildung)
- Luftdruck, Messausrüstung, Messteams

**Sicherheitskonzept DIN 4109:2018:** Prognoseunsicherheit wird durch Sicherheitsbeiwert uprog berücksichtigt:
- Luftschallberechnungen: uprog = 2 dB (Ausnahme Türen: uprog = 5 dB)
- Trittschallberechnungen: uprog = 3 dB

Hinweis: Eingangsdaten nach DIN 4109-2:2018 enthalten im Unterschied zur Vorgängernorm keine Zu- oder Abschläge.

Für detaillierte Unsicherheitsermittlung: DIN EN ISO 12999-1:2021 und informativer Anhang C der DIN 4109-2:2018.

---

## Kapitel 23: Schall aus Anlagen der Gebäudetechnik

### 23.1 Maschinenlagerung

Beim Betrieb von Maschinen und Aggregaten im Gebäude werden Schwingungen in den Baukörper eingeleitet, die als Körperschall weitergeleitet werden und in anderen Gebäudeteilen zu störenden Vibrationen oder Luftschallemissionen führen. Besonders relevant ist bei rotierenden Anlagenteilen die Betriebsfrequenz f (direkt aus Drehzahl ableitbar). Daneben ist impulsartige Körperschallanregung mit breitem Frequenzspektrum möglich.

#### Elastische Maschinenlagerung

Zur Reduktion der Körperschalleinleitung (Quellenisolierung) oder zum Schutz empfindlicher Maschinen vor Fundamentschwingungen (Empfängerisolierung). Materialien:
- **Elastomerlager:** Geeignet für vollflächige Auflage (Gummi- oder Schaumstoffmatten aus Polyurethan)
- **Stahlfedern:** Bevorzugt für punkt- oder linienweise Lagerung

#### Resonanzfrequenz und überkritische Abstimmung

Das Masse-Feder-System aus Maschine und elastischem Lager hat eine charakteristische Resonanzfrequenz f0 (aus Federsteifigkeit s′ und schwingender Masse m, Gleichungen 22.13/22.14):
- Unterhalb f0: Amplitude ändert sich kaum gegenüber direkter Lagerung
- Oberhalb √2 · f0: Körperschalldämmung verbessert sich mit steigender Frequenz
- **Überkritische Abstimmung empfohlen:** Resonanzfrequenz f0 bei etwa 1/5 bis 1/3 der Betriebsfrequenz f der Maschine ansetzen

#### Federsteifigkeit und Dämpfung

- **Stahlfedern:** Nahezu ideal-elastisches Verhalten; geringere Dämpfungsgrade als Elastomerlager; Dämpfung durch parallel geschaltete Bauteile erhöhbar
- **Elastomerfedern:** Steifigkeit nimmt mit zunehmender Belastung zu (nicht-lineares Verhalten); Steifigkeit muss unter realen Betriebslasten ermittelt werden

Dämpfungseigenschaft elastischer Lager wird angegeben durch:
- Dämpfungsgrad D, oder
- Verlustfaktor η = 2D

#### Übertragungsfunktion (Formel 23.1)

Verhältnis der auf das Fundament übertragenen Kraft F2 zur Erregerkraft F1 in Abhängigkeit von Frequenzverhältnis f/f0 und Dämpfungsgrad D:

```
F2/F1 = √[(1 + 4D²(f/f0)²) / ((1−(f/f0)²)² + 4D²(f/f0)²)]
```

Wichtige Konsequenzen:
- Bei D = 0 (keine Dämpfung) und Anregung mit f0: übertragene Kraft theoretisch unendlich groß
- Mit zunehmender Dämpfung: Resonanzspitze kleiner, aber auch geringere Körperschallisolierung oberhalb f0

#### Einfügungsdämmung

Gibt die Körperschallpegelreduktion durch elastische Lagerung gegenüber direkter Aufstellung an. In der Praxis geprägt durch Einbrüche im hohen Frequenzbereich (Eigenresonanzen der Federelemente).

**Materialwahl je nach Betriebsweise:**
- Maschinen, die häufig hoch- und herunterfahren (Resonanz oft durchlaufen) → hohe Dämpfung wählen
- Maschinen im Dauerbetrieb bei konstanter Drehzahl → geringe Dämpfung wählen (höhere Einfügungsdämmung bei Betriebsfrequenz)

#### Zwischenfundament zur Masseerhöhung

Maschinen werden häufig auf einem Zwischenfundament aus Stahlbeton oder Stahl aufgestellt, das elastisch auf dem eigentlichen Fundament gelagert ist. Vorteile:
- Erhöhung der ständigen Lasten → kleinere Resonanzfrequenz f0
- Verringerung des Anteils veränderlicher Lasten → leichtere Federauswahl

Bei großen Zwischenfundamenten oder hohen Resonanzfrequenzen: Ausbildung von Biegewellen auf dem Fundament möglich → dynamisch wirksame Masse ist dann kleiner als Gesamtmasse.

#### Weitere Konstruktionsregeln

- Bei punktweiser Lagerung: Gleichmäßige Belastung aller Federn durch Abstimmung der Federpositionierung auf den Schwerpunkt der schwingenden Masse
- Versorgungsleitungen (Rohre, Kabel) stets von der massiven Konstruktion entkoppeln → keine Schallbrücken
- Bei besonders hohen Anforderungen: Doppeltelastische Lagerung (zwei Masse-Feder-Systeme) → zwei Resonanzfrequenzen; Dämmwirkung oberhalb der höchsten Resonanzfrequenz steigt stärker als bei einfachelastischer Lagerung

### 23.2 Schall aus raumlufttechnischen Anlagen

Raumlufttechnische Anlagen (RLT) gewinnen wegen Energieeinsparung und gestiegener Komfortanforderungen an Bedeutung. Mechanische Lüftungsanlagen mit Wärmerückgewinnung sind im Verwaltungs- und Wohnungsbau verbreitet, stellen aber zusätzliche Lärmquellen dar.

#### Richtwerte für Schalldruckpegel aus RLT-Anlagen (Tab. 23.1, VDI 2081 Blatt 1:2019)

| Raumart | Schalldruckpegel Lp hohe Anforderung [dB(A)] | Niedrige Anforderung [dB(A)] |
|---|---|---|
| Einzelbüro | 30 | 35 |
| Großraumbüro | 35 | 45 |
| Werkstätten | 50 | — |
| Konzertsaal, Opernhaus | 25 | 30 |
| Theater, Kino | 30 | 35 |
| Konferenzraum | 35 | 40 |
| Hotelzimmer | 30 | 35 |
| Lesesaal | 30 | 35 |
| Klassenraum, Hörsaal | 30 | 35 |
| Bettenraum (Krankenhaus) | 25 | 35 |
| Operationssäle | 48 | 48 |
| Museum | 30 | 35 |
| Gaststätte | 35 | 50 |
| Verkaufsraum | 40 | 50 |
| Sporthallen, Schwimmbäder | 45 | 50 |
| Rundfunkstudio | 15 | 25 |
| Fernsehstudio | 25 | 30 |

Einzahlwerte dB(A) allein sind bei hohen Anforderungen nicht ausreichend — tonale Störsignale werden nicht erfasst. Stattdessen: Geräuschbewertungskurven verwenden.

#### Geräuschbewertungskurven

- **NR-Kurven (Noise-Rating):** in Oktavschritten, gemäß ISO 1996-1:2016 bzw. VDI 2081 Blatt 1:2019
- **GK-Kurven (Geräuschbewertungskurven):** in Terzschritten, gemäß DIN 15996:2020

Näherungsregel: A-bewerteter Schalldruckpegel aus RLT-Anlage liegt ca. 5 dB über dem Wert der zugehörigen Geräuschbewertungskurve.

Einschränkung: Vorgabe für maximale Schalldruckpegel ist nur sinnvoll, wenn andere Schallquellen (z.B. Nutzergeräte wie Computer) nicht höher sind als die angegebenen Richtwerte.

#### Geräuscherzeugung im Lüftungskanal

Hauptgeräuschquelle in RLT-Anlagen: Ventilator. Ursache der Lüftungsgeräusche: Turbulenzen beim Durchströmen des Laufrades (vorwiegend aerodynamisch, breitbandiges Rauschen, teils überlagert von Drehklang).

Schallleistungszunahme des Ventilatorgeräuschs: **12 bis 18 dB pro Verdopplung der Strömungsgeschwindigkeit** (bei steigender Fördermenge/Drehzahl).

Weitere Geräuschquellen:
- Einbauelemente (Abzweigungen, Umlenkungen, Filter, Luftdurchlässe)
- Luftdurchlässe mit zu kleinen Querschnittsflächen (Strömungsgeräusche bei hoher Strömungsgeschwindigkeit)

Empfehlung: Bei hohen Anforderungen an den Grundgeräuschpegel → große Kanalquerschnitte und Luftdurchlässe einplanen.

Besonderheit bei tiefen Frequenzen: Mündungsreflexion zu berücksichtigen — tieffrequente Schallanteile werden zu großem Teil reflektiert, wenn die Austrittsfläche klein gegenüber der Wellenlänge ist.

#### Schalldruckpegel im Empfangsraum (Formel 23.2)

Im Empfangsraum mit diffusem Schallfeld:

```
Lp = Lw + 10 · lg(Q/(4πr²) + 4/A)
```

- Lw = Schallleistungspegel der Zu-/Abluftdurchlässe
- Q = Richtwirkungs-Maß (aus Abb. 23.8 für 0° bzw. Abb. 23.9 für 45° Abstrahlwinkel, VDI 2081)
- A = äquivalente Schallabsorptionsfläche des Raumes
- r = Abstand zwischen Durchlass und Raumpunkt

#### Kanalnetzberechnung

Ziel: Minimierung des Ventilatorgeräuschs und Vermeidung pegelbestimmender Strömungsgeräusche entlang der Kanalstrecke. Berechnungsvorgaben in VDI 2081 Blatt 1:2019.

Grundprinzip: Schallausbreitung für den gesamten Lüftungsweg berechnen — jedes Bauteil als Einzelschallquelle mit schallminderndem (Dämpfung) und schallerzeugenden Einfluss (Strömungsrauschen). Alle Einbauelemente — Kanal, Abzweigungen, Umlenkungen, Luftdurchlässe, Filter, Ventilator — werden berücksichtigt.

#### Schalldämpfer — Typen und Eigenschaften

**Absorptionsschalldämpfer:**
- Als Kulissenschalldämpfer (für Rechteckkanäle) oder Rohrschalldämpfer (für Rundkanäle)
- Wirkprinzip: Poröse Absorption (wie in Kap. 21 beschrieben)
- Breitbandige Dämpfung, hohe Absorptionswerte im mittleren und hohen Frequenzbereich
- Schwäche im tiefen Frequenzbereich → oft in Kombination mit Resonanzschalldämpfern

Aufbau Schalldämpferkulisse:
- Stahlblechrahmen, gefüllt mit Faserdämmstoff (Glas- oder Mineralwolle)
- Mineralwolle mit Faservlies gegen Abrieb geschützt
- Lochblech oder Streckmetall-Abdeckung gegen mechanische Beschädigungen

Geometrie-Parameter:
- Kulissendicke d und Spaltbreite 2s bestimmen das wirksame Dämpfungsspektrum
- Größere Kulissendicke + schmalere Spaltbreite → breiteres Dämpfungsspektrum
- Aber: schmalere Spaltbreite erhöht Strömungsrauschen und Druckverlust

Ausstellungsverhältnis m für Schalldämpfer mit Mittelkulisse (Formel 23.3):
```
m = d/s
```

Kulissenanzahl n in Abhängigkeit Gehäusebreite B (Formel 23.4):
```
n = B/(d + s) − 2
```

**Rohrschalldämpfer:** Für runde Kanäle; schallabsorbierende Wandung und je nach Rohrdurchmesser und gewünschtem Dämpfungsspektrum schallabsorbierender Zentralkörper.

#### Berechnung der Einfügungsdämpfung von Absorptionsschalldämpfern (Formel 23.5, nach Piening)

```
D = 1,5 · α · Δx · U/S
```

- α = Schallabsorptionsgrad
- Δx = Schalldämpferlänge
- U = absorbierender Umfang der Kanalauskleidung
- S = freie Querschnittsfläche

Schlussfolgerung: Möglichst großes Verhältnis U/S anstreben.

Einfügungsdämpfungen werden üblicherweise messtechnisch im Schalldämpferprüfstand in Oktavbandbreite ermittelt.

#### Schallübertragung zwischen Räumen über das Lüftungssystem

Über das Lüftungskanalnetz als Nebenweg kann die erreichbare Luftschalldämmung zwischen Räumen begrenzt werden. Berechnungsverfahren für Schallübertragung über das Kanalnetz: VDI 2081 Blatt 1:2019.

---

### Normen und Regelwerke (vollständige Referenzliste aus Kapitel 22)

**DIN 4109 (Schallschutz im Hochbau):**
- DIN 4109:1989-11 — Grundlegende Anforderungen und Nachweise
- DIN 4109 BB 1:1989-11 — Ausführungsbeispiele und Rechenverfahren
- DIN 4109 BB 1/A1:2003-09 — Ergänzung
- DIN 4109 BB 2:1989-11 — Planung, erhöhter Schallschutz, Empfehlungen eigener Wohnbereich
- DIN 4109-1:2018-01 — Mindestanforderungen
- DIN 4109-2:2018-01 und A1:2020-05 — Rechnerische Nachweise
- DIN 4109-4:2016-07 — Bauteilkatalog: Bauakustische Prüfungen
- DIN 4109-5:2020-08 — Erhöhte Anforderungen
- DIN 4109-31:2016-07 — Bauteilkatalog: Rahmendokument
- DIN 4109-32:2016-07 — Bauteilkatalog: Massivbau
- DIN 4109-33:2016-07 — Bauteilkatalog: Holz-, Leicht- und Trockenbau
- DIN 4109-34:2016-07 — Bauteilkatalog: Vorsatzkonstruktionen vor massiven Bauteilen
- DIN 4109-35:2016-07 — Bauteilkatalog: Elemente, Fenster, Türen, Vorhangfassaden
- DIN 4109-36:2016-07 — Bauteilkatalog: Gebäudetechnische Anlagen

**DIN EN ISO (Bauakustik):**
- DIN EN ISO 12354-1:2017-11 — Luftschalldämmung zwischen Räumen
- DIN EN ISO 12354-2:2017-11 — Trittschalldämmung zwischen Räumen
- DIN EN ISO 12354-3:2017-11 — Luftschalldämmung gegen Außenlärm
- DIN EN ISO 717-1:2021-05 — Bewertung Luftschalldämmung
- DIN EN ISO 717-2:2021-05 — Bewertung Trittschalldämmung
- DIN EN ISO 12999-1:2021-04 — Messunsicherheiten Schalldämmung
- DIN EN ISO 12999-2:2020-11 — Messunsicherheiten Schalldämpfung

**VDI-Richtlinien:**
- VDI 2081 Blatt 1:2019 — Geräuscherzeugung und Lärmminderung in RLT-Anlagen
- VDI 2719:1987-08 — Schalldämmung von Fenstern
- VDI 3728:2012-03 — Schalldämmung beweglicher Raumabschlüsse (Türen und Mobilwände)
- VDI 4100:2012-10 — Schallschutz in Wohnungen, Beurteilung und Vorschläge für erhöhten Schallschutz

**Sonstige:**
- ISO 1996-1:2016 — NR-Kurven (Noise-Rating)
- DIN 15996:2020 — GK-Kurven (Geräuschbewertungskurven)
