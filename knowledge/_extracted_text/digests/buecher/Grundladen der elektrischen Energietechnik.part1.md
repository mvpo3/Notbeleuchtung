# Grundladen der elektrischen Energietechnik — Teil 1
> Quelle: Grundladen der elektrischen Energietechnik (buecher) · Seiten 41-80.

Dieser Teil des Lehrbuches behandelt Grundlagen der Gleichstromtechnik (Schaltungen, Netzwerkmethoden, Quellen) sowie das magnetische Feld (Feldgrößen, Materie im Magnetfeld, elektromagnetische Induktion). Er bildet das physikalisch-mathematische Fundament für die spätere Behandlung von Wechselstrom, Transformatoren, Motoren und Generatoren in der elektrischen Energietechnik.

## Inhalt

### 1.2 Gleichstrom — Widerstandseffekte: Dehnung und Licht (S. 41)

- **Dehnungsmessstreifen (DMS):** Bei einem langen dünnen metallischen Leiter, der im elastischen Bereich gedehnt wird, ändert sich der Widerstand proportional zur relativen Längenänderung. Der Proportionalitätsfaktor heißt K-Faktor (dimensionslos). Formel: ΔR/R = k · Δl/l. Anwendung: Messung von Oberflächenspannungen, Drehmomenten oder Kräften (z.B. in Waagen), indem DMS mit Spezialkleber auf Oberflächen geklebt werden.
- **Fotowiderstand (LDR — Light Dependent Resistor):** Lichtabhängiger Widerstand aus amorpher Halbleiterschicht. Höhere Lichtintensität → niedrigerer elektrischer Widerstand (durch inneren fotoelektrischen Effekt). Einsatz in Belichtungsmessern von Kameras und Dämmerungsschaltern.
- **Fotodiode:** Halbleiterdiode, die Lichtenergie in elektrischen Strom umwandelt. Benötigt — anders als der Fotowiderstand — keine externe Spannungsquelle. Als großflächige Variante (Solarzelle) dient sie in Photovoltaikanlagen zur Energiegewinnung.

---

### 1.2.3 Schaltungen mit ohmschen Widerständen und Kirchhoffsche Regeln (S. 41–45)

#### Reihenschaltung

- Bei n in Reihe geschalteten Widerständen R1 bis Rn gilt:
  - Alle Teilströme sind identisch: I = I1 = I2 = … = In
  - Die Teilspannungen addieren sich zur Gesamtspannung: U = U1 + U2 + … + Un
  - Gesamtwiderstand ist die Summe aller Einzelwiderstände: R = R1 + R2 + … + Rn

#### Parallelschaltung

- Bei n parallel geschalteten Widerständen gilt:
  - Alle Teilspannungen sind gleich: U = U1 = U2 = … = Un
  - Die Teilströme addieren sich zum Gesamtstrom: I = I1 + I2 + … + In
  - Die Leitwerte addieren sich: G = G1 + G2 + … + Gn, wobei G = 1/R

#### Spannungs- und Stromteilerregeln für zwei Widerstände

- **Reihenschaltung zweier Widerstände:** Gesamtwiderstand R = R1 + R2. Spannungsteilung: U1/U = R1/(R1+R2); U1/U2 = R1/R2
- **Parallelschaltung zweier Widerstände:** Gesamtwiderstand R = (R1·R2)/(R1+R2). Stromteilung: I1/I2 = G1/G2 = R2/R1; I1/I = R2/(R1+R2)

#### Kirchhoffsche Regeln

- **Erstes Kirchhoffsches Gesetz (Knotenregel):** An einem elektrischen Knoten muss die Summe aller zufließenden Ströme gleich der Summe aller abfließenden Ströme sein. Ursache: Erhaltung elektrischer Ladung. Formale Schreibweise: Σ Ik = 0 (zuströmende Ströme positiv, abströmende negativ gewertet oder umgekehrt). Zahl unabhängiger Knotengleichungen in einem Netzwerk mit k Knoten: k−1.
- **Zweites Kirchhoffsches Gesetz (Maschenregel):** Die Summe aller Spannungen entlang eines geschlossenen Umlaufweges (Masche) ist null: Σ Uk = 0. Physikalische Begründung: Energieerhaltung — nach einem vollständigen Umlauf kehrt man zum Ausgangspotenzial zurück, die Bilanz der Potenzialunterschiede ist daher null. Analogie: Wie bei einer Bergwanderung, bei der die Summe der Höhendifferenzen nach Rückkehr zum Startpunkt null ergibt.
- Zahl unabhängiger Maschengleichungen in einem Netzwerk mit m Maschen: m.

#### Spannungsteiler

- Prinzip: Eine anliegende Gesamtspannung U wird aufgeteilt, um eine kleinere Lastspannung UB zu erzeugen. Der Gesamtwiderstand teilt sich in R1 und R2.
- **Unbelasteter Spannungsteiler** (kein Laststrom IB): UB = R2/(R1+R2) · U
- **Belasteter Spannungsteiler** (IB ≠ 0): UB = R2B/(R1+R2B) · U, wobei R2B der Parallelersatzwiderstand von R2 und dem Lastwiderstand RB ist: R2B = (R2·RB)/(R2+RB)
- Anwendungen: Einstellung von Arbeitspunkten in HiFi-Verstärkern; bei kleinen Leistungen auch Drehzahlregelung von Gleichstrommotoren.

#### Stern-Dreieck-Umwandlung

- Ohmsche Widerstände können in Stern- oder Dreieckschaltung angeordnet sein. Anwendungsbeispiel: Heizwendeln in Elektroherden und Durchlauferhitzern.
- Umrechnung Dreieck → Stern (Formeln für die Sternwiderstände R1, R2, R3 aus Dreieckwiderständen R12, R23, R31):
  - R1 = (R12 · R31) / (R12 + R23 + R31)
  - R2 = (R23 · R12) / (R12 + R23 + R31)
  - R3 = (R31 · R23) / (R12 + R23 + R31)
- Umrechnung Stern → Dreieck (Formeln für die Dreieckwiderstände):
  - R12 = R1 + R2 + (R1·R2)/R3
  - R23 = R2 + R3 + (R2·R3)/R1
  - R31 = R3 + R1 + (R3·R1)/R2

---

### 1.2.4 Berechnung von linearen Gleichstromnetzwerken (S. 37–42)

#### Direkte Anwendung der Kirchhoffschen Regeln

- Schaltungen mit linearen Widerständen und Gleichspannungsquellen bilden lineare Gleichstrom-Netzwerke.
- Vorgehensweise: Strombezugspfeile festlegen (dürfen nachher nicht geändert werden; negative Vorzeichen im Ergebnis zeigen entgegengesetzte Richtung an). Dann k−1 unabhängige Knotengleichungen und m unabhängige Maschengleichungen aufstellen.
- Ergebnis: Inhomogenes lineares Gleichungssystem für die gesuchten Zweigströme, lösbar z.B. mit dem Gaußschen Algorithmus.
- Einschränkung: Bei großen Netzwerken kaum in effiziente Algorithmen umsetzbar (Beispiel: Mittelspannungsnetz mit ca. 30.000 Leitungen erfordert Software).

#### Aktive Zweipole

- **Passive Zweipole** nehmen Leistung auf; **aktive Zweipole** stellen an ihren Klemmen selbst Spannung bereit und geben im Mittel Leistung ab.
- **Ideale Gleichspannungsquelle:** Klemmenspannung U = U0 unabhängig vom fließenden Strom. Reale Quellen weichen davon ab (Beispiel: Autobatterie bei Anlasserstart bricht Spannung bei mehreren hundert Ampere deutlich ein).
- **Technische (reale) Gleichspannungsquelle:** Modelliert durch Reihenschaltung einer idealen Spannungsquelle U0 mit einem Innenwiderstand Ri. Klemmenspannung: U = U0 − Ri·I. Bei konstantem Ri ist die Belastungskennlinie eine abfallende Gerade.
  - Leerlauf (I = 0 oder RV = ∞): Klemmenspannung = U0 (Leerlaufspannung, auch Urspannung).
  - Kurzschluss (U = 0 oder RV = 0): Strom = Ik = U0/Ri (Kurzschlussstrom).
- **Thévenin-Theorem (auch Helmholtz-Thévenin-Theorem / Helmholtz-Satz):** Jedes beliebige lineare Netzwerk aus Spannungsquellen, Stromquellen und Widerständen lässt sich auf eine einzige Spannungsquelle mit Innenwiderstand reduzieren.
- **Technische Gleichstromquelle (Stromquellenersatzschaltbild):** Äquivalent zur technischen Spannungsquelle. Besteht aus einer idealen Stromquelle mit Quellenstrom Ik (= Kurzschlussstrom) parallel zum Innenleitwert Gi. Umrechnung: U0 = Ik/Gi; Ik = U0/Ri; Ri = 1/Gi.

#### Knotenpotenzialverfahren

- Deutlich effizienter als direkte Anwendung der Kirchhoffschen Regeln, weil das Aufstellen der Leitwertmatrix in Software implementierbar ist.
- **Schritte:**
  1. Alle Spannungsquellen mit Innenwiderstand in äquivalente Stromquellen mit Innenleitwert umwandeln (bei Spannungsquellen ohne Zweigwiderstand ist anderes Vorgehen nötig).
  2. Netzwerk mit Stromquellen und Leitwerten neu zeichnen.
  3. Einen Bezugsknoten wählen (Index 0, Potenzial φ0 = 0 V), restliche k−1 Knoten nummerieren.
  4. **Knotenleitwertmatrix** direkt aufstellen:
     - Hauptdiagonalelement (i=j): Summe aller Leitwerte am Knoten i.
     - Nebendiagonalelement (i≠j): negativer Leitwert −Gij zwischen Knoten i und j.
  5. Rechte Seite des Gleichungssystems: eingeprägte Kurzschlussströme der Energiequellen (Vorzeichen: zufließend = positiv).
  6. Lösung des linearen Gleichungssystems liefert die Knotenspannungen Ui0.
  7. Zweigströme mit dem Ohmschen Gesetz berechnen.
- Im Gleichstromkreis ist die Leitwertmatrix symmetrisch.
- **Beispiel** (Netzwerk mit einer Spannungsquelle U0 und sechs Widerständen R1–R6, vier Knoten):
  - Spannungsquelle mit R1 wird zu Stromquelle Ik = U0/R1 mit G1 = 1/R1.
  - Die 3×3 Knotenleitwertmatrix hat auf der Hauptdiagonale z.B. (G1+G4+G6), auf Nebendiagonalen die negativen Leitwerte zwischen den Knoten.
  - Lösung ergibt U10, U20, U30, aus denen alle Zweigströme folgen:
    - I1 = Ik − G1·U10 (Strom der Quelle)
    - I2 = G2·U20; I3 = G3·U30 (Ströme zum Referenzknoten)
    - I4 = G4·(U10−U20); I5 = G5·(U20−U30); I6 = G6·(U10−U30) (Ströme zwischen Knoten)

---

### 1.3 Magnetisches Feld (S. 43 ff.)

#### Historische Einordnung und Grundphänomene

- Natürliche Magnete (Eisenerze) und die Erde als Magnet; Kompassnadeln richten sich nach magnetischem Nord-/Südpol aus. Name "Magnet" von der Stadt Magnesia in Kleinasien.
- Ab dem frühen 19. Jahrhundert wurde erkannt, dass bewegte elektrische Ladung mit einem Magnetfeld verbunden ist. Elektrizität und Magnetismus sind zwei Aspekte desselben Phänomens (Spezielle Relativitätstheorie).
- **Zwei praktische Auswirkungen des Magnetfeldes auf stromdurchflossene Leiter:**
  - **Motorprinzip:** Auf einen stromdurchflossenen Leiter im Magnetfeld wirkt die Lorentzkraft. Kräftepaare erzeugen ein Drehmoment → Antrieb von Arbeitsmaschinen.
  - **Generator-/Transformatorprinzip:** In stromlosen Leitern erzeugen Induktionsvorgänge messbare Spannungen; genutzt in Transformatoren und Generatoren.

---

### 1.3.1 Feldgrößen, Lorentzkraft und Durchflutungsgesetz (S. 44–52)

#### Statisches Magnetfeld: Grundeigenschaften

- Zwei Pole: Nordpol (N) und Südpol (S). Gleichnamige Pole stoßen sich ab, ungleichnamige ziehen sich an.
- Stabmagnet aufgeteilt → beide Hälften haben wieder N- und S-Pol. Magnetische Monopole sind nicht bekannt; es existieren nur magnetische Dipole.
- **Magnetische Flussdichte B** (nach DIN 1324): definiert die magnetische Feldwirkung. Einheit: [B] = Vs/m² = Tesla = T. Auch als "magnetische Induktion" bezeichnet. Historische Namensverwirrung: H trägt den Namen "magnetische Feldstärke", obwohl B physikalisch die Kraftgröße ist.
- **Magnetische Feldlinien:** geschlossene Kurven (kein Anfang, kein Ende → Magnetfeld ist Wirbelfeld, kein Quellenfeld). Außerhalb eines Dauermagneten verlaufen sie vom Nordpol zum Südpol. Feldliniendichte ist Maß für den Betrag von B; Richtung von B ist tangential zu den Feldlinien.
- **Unterschied elektrisches vs. magnetisches Feld:**
  - Elektrische Feldlinien: Anfang an positiver Ladung, Ende an negativer Ladung → Quellenfeld (3. Maxwellsche Gleichung / Gaußscher Satz für E-Feld).
  - Magnetische Feldlinien: stets geschlossen, keine Quellen oder Senken → Wirbelfeld (4. Maxwellsche Gleichung / Gaußscher Satz für B-Feld).
- **Rechtsschraubenregel (Korkenzieherregel / Rechtefaustregel):** Fließt Strom in Richtung des rechten Daumens, zeigen die Fingerspitzen die Richtung der magnetischen Feldlinien um den Leiter an. Feldlinien um einen langen dünnen Leiter: konzentrische Kreise, deren Dichte mit dem Abstand abnimmt.

#### Elektromagnetisches Feld

- Bei zeitlich veränderlichen Strömen oder beschleunigten Ladungen entsteht ein kombiniertes elektromagnetisches Feld.
- **Linear polarisiertes Licht:** E- und B-Felder schwingen senkrecht zueinander und zur Ausbreitungsrichtung. Ausbreitungsgeschwindigkeit im Vakuum: c0 = 299.792.458 m/s ≈ 300.000 km/s (exakt festgelegte Naturkonstante).
- Zusammenhang: c0 = 1/√(ε0·µ0). Magnetische Feldkonstante (Vakuumpermeabilität, Induktionskonstante): µ0 = 4π·10⁻⁷ Vs/(Am).
- In Materie: c = c0/√(εr·µr), wobei εr die relative Permittivität und µr die relative Permeabilität sind. Frequenz bleibt beim Medienwechsel konstant, Wellenlänge und Ausbreitungsgeschwindigkeit ändern sich.
- Wellenlängen-Frequenz-Relation: c = λ·f.
- **Elektromagnetisches Spektrum** (überblick):
  - 50 Hz Wechselstrom
  - Radiowellen, AM-Mittelwelle, FM-Radio
  - Mikrowellen (z.B. Radar)
  - Infrarot
  - Sichtbares Licht: f = 400–750 THz; λ0 = 400–750 nm
  - Ultraviolett
  - Röntgenstrahlen
  - Gammastrahlen (bis >10²⁰ Hz)

#### Lorentzkraft

- Ein Magnetfeld übt auf eine bewegte Ladung Q eine Kraft aus, wenn Geschwindigkeit v und magnetische Flussdichte B nicht parallel sind.
- **Lorentzkraft:** FL = Q·(v × B). Einheit über das Vektorprodukt: Richtung per Dreifingerregel (Rechtehandregel).
  - v ⊥ B: Betrag FL = Q·v·B; Richtung mit Dreifingerregel.
  - v parallel zu B (tangential zu Feldlinien): keine Lorentzkraft.
- **Elektrodynamische Gesamtkraft** (Coulomb + Lorentz): F = Q·(E + v×B) — eine der vier Grundkräfte der Physik (neben Gravitation, starker und schwacher Wechselwirkung).
- **Kraft auf stromdurchflossenen Leiter im Magnetfeld:** FL = I·(l × B). Anwendung: Gleichstrommotor — Lorentzkräfte auf Rotorleitungen erzeugen Drehmomenten-Paare.
- **Kräfte zwischen zwei parallelen Leitern** mit Abstand a, Strömen I1 und I2, Leiterlänge l: F1 = F2 = µ0·µr·(I1·I2·l)/(2π·a). Gleiche Stromrichtung → Anziehung; entgegengesetzte Stromrichtung → Abstoßung. Wichtig für Auslegung von Sammelschienen: müssen bei Kurzschlüssen mechanisch den Lorentzkräften standhalten.

#### Statisches Durchflutungsgesetz

- Gilt für Gleichströme (für Wechselströme gilt das erweiterte Durchflutungsgesetz / 1. Maxwellsche Gleichung).
- Aussage: Die Summe der durch eine Fläche A fließenden Gleichströme ist gleich dem Linienintegral von B₀/µ0 entlang eines geschlossenen Weges, der diese Fläche umschließt.
- Formel: Σj Ij = (1/µ0)·∮ B0·dr; die elektrische Durchflutung Θ = Σj Ij [A].
- **Vorzeichen:** Ströme in Richtung des rechten Daumens (wenn Finger in Integrationsrichtung) werden positiv gezählt.
- **Anwendungsbeispiel 1 — langer dünner Leiter (Kreisquerschnitt, Radius r1, Strom I):**
  - Außerhalb des Leiters (r ≥ r1): B0(r) = µ0·I/(2π·r) — nimmt mit zunehmendem Abstand ab.
  - Innerhalb des Leiters (r ≤ r1, gleichmäßige Stromverteilung): B0(r) = µ0·I·r/(2π·r1²) — linear ansteigend von null (Mitte) bis zum Maximum am Rand bei r = r1.
- **Anwendungsbeispiel 2 — lange Spule (Länge l, N Windungen, Gleichstrom I):**
  - Magnetische Flussdichte im Inneren: B0 = µ0·(N/l)·I — homogen (analog zur elektrischen Feldstärke im Plattenkondensator).

---

### 1.3.2 Materie im Magnetfeld (S. 54–60)

#### Magnetisches Dipolmoment

- Magnetische Dipolmomente sind mikroskopische Elementarmagnete (Kompassnadel-Analogie) mit eigenem Magnetfeld, die im äußeren Feld ein Drehmoment erfahren.
- Drehmoment auf Dipol: M = pm × B; magnetisches Dipolmoment pm [Am²].
- **Leiterschleife mit Strom I und umschlossener Fläche A:** pm = I·A.
- **Spule mit N Windungen:** pm = N·I·A.
- Richtung von pm: Rechtsschraubenregel — Strom in Richtung der Fingerspitzen, Daumen zeigt Richtung von pm.
- **Anwendung — Drehspulmesswerk:** Spule im Magnetfeld dreht sich proportional zum Messstrom; Rückstellfeder im Gleichgewicht → linearer Zeigerausschlag.
- **Atom/Molekül:** Elektronen auf Kreisbahnen bilden kreisförmige Gleichströme → magnetisches Moment; Elektronenspin liefert zusätzlichen Beitrag (quantenmechanischer Effekt).

#### Magnetisierung und relative Permeabilität

- **Magnetisierung** ist die Dichte der magnetischen Dipolmomente dpm/dV [A/m]. Sie hat selbst ein Magnetfeld (magnetische Polarisation Bp = µ0·dpm/dV).
- Gesamte magnetische Flussdichte: B = Bf + Bp, wobei Bf der Anteil der frei beweglichen Ladungsträger (messbare makroskopische Ströme), Bp der Anteil der gebundenen Ladungsträger.
- **Magnetische Feldstärke H:** Definiert als H = Bf/µ0 [A/m]. H ist nicht messbar — reine Rechengröße / Zwischenergebnis.
- **Magnetische Suszeptibilität χm** (dimensionslos): Linearer Proportionalitätsfaktor zwischen Bp und Bf für lineare, isotrope Materialien: Bp = χm·Bf.
- **Relative Permeabilität µr** (dimensionslos): µr = 1 + χm; Zusammenhang: B = µr·Bf. Material verstärkt das Feld der freien Ströme um Faktor µr > 1.
- **Permeabilität µ:** µ = µ0·µr [Vs/(Am)]; µr wird daher auch relative Permeabilität genannt.
- Im Vakuum gilt χm = 0, µr = 1; für Luft in guter Näherung ebenfalls.

#### Klassifikation magnetischer Materialien

| Kategorie | χm | µr | Beispiele |
|-----------|-----|-----|-----------|
| Diamagnetika | < 0 | < 1 | H2, N2, H2O |
| Keine Magnetisierung | = 0 | = 1 | Vakuum, Luft |
| Paramagnetika | > 0 | > 1 | Sn, Pt, Al |
| Ferromagnetika | komplex (Hysterese) | >> 1 | Fe, Co, Ni |

- **Diamagnetismus:** Ohne äußeres Feld heben sich atomare Momente auf (Edelgaskonfiguration). Äußeres Feld → Bahndrehimpulse und Spins ändern sich → entgegengesetztes induziertes Feld (Lenzsche Regel) → Material verdrängt äußeres Feld. χm < 0, µr < 1. Effekt temperaturunabhängig, sehr schwach. Tritt in allen Stoffen auf.
- **Paramagnetismus:** Permanente magnetische Momente vorhanden, aber ohne äußeres Feld ungeordnet → kein Nettomoment. Äußeres Feld richtet Momente aus → Feldverstärkung. χm > 0, µr > 1. Nach Feldabschaltung wieder unmagnetisch. Stärker als Diamagnetismus.

#### Ferromagnetika und Hysterese

- Ferromagnetische Materialien (Fe, Co, Ni) haben unaufgefüllte innere Elektronenschalen; lineare Gleichungen χm und µr gelten für sie nicht.
- Bedeutung: Exzellente Magnetfeldleitung → Kernnaterial für Transformatoren, Generatoren, Motoren; auch als Dauermagnete.
- **Weißsche Bezirke:** Bereiche einheitlicher Magnetisierung im Eisenkristall, Größe ca. 10 µm bis 1 mm. Im entmagnetisierten Zustand ungeordnet.
- **Magnetisierungsvorgang (Neukurve):** Strom in Spule von 0 erhöhen → Weißsche Bezirke richten sich aus → Neukurve → Sättigungsbereich: alle Momente ausgerichtet, B wächst nur noch schwach linear (BS = Sättigungsflussdichte).
- **Hysterese:** Beim Reduzieren des Stroms wird eine andere Kurve durchlaufen (oberhalb der Neukurve). Bei I = 0 bleibt Restmagnetismus → **Remanenzflussdichte BR** → Material ist Dauermagnet.
- Stromumkehr nötig, um Magnetismus zu löschen; bei Strom −IC verschwindet B → **Koerzitivfeldstärke HC = N·IC/l** [A/m] (vektorielle Größe).
- Weitererhöhen des umgekehrten Stroms: Sättigung in negativer Richtung. Zurückdrehen: geschlossene Hystereseschleife.
- **Magnetisch harte vs. weiche Materialien:**
  - Weichmagnete: HC < 1 kA/m → schnelle Ummagnetisierung → Transformatoren- und Motorkerne.
  - Hartmagnete: HC > 450 kA/m → bleibender Magnetismus → Dauermagnete.
  - Dazwischen: magnetisch halb harte Materialien.
- **Hystereseverluste:** Ständige Umorientierung der Elementarmagnete erzeugt Wärme. Verlust proportional zur Fläche der Hysteresekurve und zur Frequenz der Wechselspannung.
- Konstante relative Permeabilität µr für einige Eisenwerkstoffe (Tabelle A.30) dient nur zur groben Orientierung.

---

### 1.3.3 Elektromagnetische Induktion (S. 60–70)

#### Magnetischer Fluss

- **Magnetischer Fluss Φ(t)** (auch Induktionsfluss): Φ(t) = ∫∫A B(t)·dA. Einheit: [Φ] = T·m² = Vs = Weber = Wb.
- Skalare Größe, analog zur elektrischen Stromstärke. Bei homogenem Feld: Φ = B·A.

#### Induktionsgesetz und Lenzsche Regel

- **Grundexperiment:** Metallstab rollt mit Geschwindigkeit v senkrecht zu einem homogenen Magnetfeld B entlang leitender Schienen im Abstand l. Lorentzkraft trennt Ladungsträger → elektrisches Feld baut sich auf (Coulombkraft der Gegenrichtung), bis Gleichgewicht. Induzierte Gleichspannung: U12 = v·B·l (ohne Vorzeichen im Verbraucherzählpfeilsystem).
- **Allgemeines Induktionsgesetz:** u(t) = dΦ(t)/dt. (Formulierung ohne Minuszeichen im Verbraucherzählpfeilsystem — das Minuszeichen erscheint im Erzeugerzählpfeilsystem.) Formulierung mit N Windungen: u(t) = N·dΦ(t)/dt.
- Bedeutung: In einem Leiter wird Spannung induziert, wenn sich der ihn durchsetzende magnetische Fluss zeitlich ändert. Äquivalent zur 2. Maxwellschen Gleichung.
- **Lenzsche Regel (Lenzsches Gesetz):** Die Wirkung der elektromagnetischen Induktion ist stets der Ursache entgegen gerichtet → Ausdruck des Energieerhaltungssatzes. Beispiel: Induzierter Strom erzeugt Lorentzkraft entgegen der Bewegungsrichtung des Stabes; zur Aufrechterhaltung konstanter Geschwindigkeit muss mechanische Arbeit geleistet werden, die in elektrische Energie umgewandelt wird.

#### Hall-Effekt

- Anwendung der elektromagnetischen Induktion in der Messtechnik.
- Fließt ein Steuerstrom I durch eine Hall-Sonde (Dicke d) im Magnetfeld B, werden Ladungsträger durch die Lorentzkraft seitlich abgelenkt → Ladungstrennung → Hall-Spannung UH.
- Formel: UH = RH·(B·I)/d; RH = Hall-Konstante [m³/C].
- Anwendungen: Messung magnetischer Flussdichte; Strommessung mit Stromzangen; Drehzahlsensoren in bürstenlosen EC-Motoren (z.B. Lüfter in Klimaanlagen).

#### Transformator- und Generatorprinzip

- Unterscheidung nach Ursache der Flussänderung:

| Prinzip | Änderung B(t) | Änderung A(t) | Bauform |
|---------|--------------|--------------|---------|
| Transformatorprinzip (Ruheinduktion) | dB/dt ≠ 0 | dA/dt = 0 | Transformator |
| Generatorprinzip (Bewegungsinduktion) | dB/dt = 0 | dA/dt ≠ 0 | bewegter Leiter, rotierende Spule |

- Beide Ursachen können auch gleichzeitig auftreten.
- **Idealer Transformator:** Zwei galvanisch getrennte Wicklungen (N1, N2) um gemeinsamen Eisenkern. Spannungsübersetzung: u1(t)/u2(t) = N1/N2. Stromübersetzung: i1(t)/i2(t) = N2/N1. Reale Transformatoren weichen ab (Stufenschalter bei Lastwechsel nötig).
- **Wechselstromgenerator (Modell):** Rechteckige Leiterschleife rotiert gleichförmig (f = const) in homogenem Magnetfeld. Fluss: Φ(t) = Φ̂·cos(ωt). Induzierte Spannung (Rechenbeispiel mit N = 100, f = 50 Hz, Φ̂ = 10 mVs): û = N·Φ̂·ω = 314 V = √2·222 V. Φ(t) und u(t) sind um π/2 phasenverschoben.

#### Selbst- und Gegeninduktion

- **Selbstinduktion:** Ein durch eine Leiterschleife (oder Spule) fließender Wechselstrom erzeugt ein zeitlich veränderliches Magnetfeld, das seinerseits eine Spannung in derselben Schleife induziert — der treibenden Spannung entgegen (Lenzsche Regel).
- **Selbstinduktivität L** (auch Induktivität oder Selbstinduktionskoeffizient): u(t) = L·di(t)/dt; Einheit [L] = Vs/A = Henry = H. Definition setzt konstantes µr voraus (Ferromagnetika streng genommen ausgeschlossen).
- L hängt von Geometrie und Materialstoffkonstante µr ab (verschiedene Formeln je nach Leiteranordnung, siehe Tab. A.25). Meistens experimentelle Bestimmung notwendig.
- **Zeitkonstante τ = L/R** beim Einschalten einer Spule an Gleichspannung U0: i(t) = (U0/R)·(1 − e^{−t/τ}). Stationärer Zustand I0 = U0/R (kein Induktionseffekt bei Gleichstrom).
- Maschengleichung mit Widerstand und Induktivität: U0 = R·i(t) + L·di/dt.
- **Gegeninduktion:** Wechselstrom in einer Leiterschleife induziert Spannung in einer benachbarten Schleife.
- **Gegeninduktivität M** (auch gegenseitige magnetische Induktivität): M21 = M12 = M [H].
- **Spannungsgleichungen zweier verkoppelter Schleifen** (je mit Widerstand R1, R2 und Selbstinduktivitäten L1, L2):
  - u1(t) = R1·i1(t) + L1·di1/dt + M·di2/dt
  - u2(t) = R2·i2(t) + M·di1/dt + L2·di2/dt
- Umformulierung ergibt das **T-Ersatzschaltbild** (Längsimpedanzen L1−M und L2−M, Querinduktivität M).
- Anwendungen der elektromagnetischen Induktion: Leistungstransformatoren, Drehstrommotoren, Drehstromgeneratoren.
- Unerwünschte Wirkungen: elektromagnetische Störfelder (EMV-Problematik), Wirbelströme, Skin-Effekt, Proximity-Effekt → zusätzliche Verluste bei Wechselstrom-Übertragung.

#### Energie im Magnetfeld

- Eine stromdurchflossene Spule speichert Energie in ihrem Magnetfeld.
- Gespeicherte Energie: W = L·I0²/2 (aus Integration der Einschaltleistung).
- **Magnetische Energiedichte** in homogenem, isotropem Material: w = B²/(2·µ0·µr) [J/m³].

#### Magnetischer Kreis (Ringkernspule)

- Ringkernspule: Kreisquerschnitt A, Durchmesser d der Querschnittsfläche, mittlerer Ringumfang l = 2π·r (r = mittlerer Radius), Windungszahl N, Gleichstrom I.
- Anwendung des Durchflutungsgesetzes auf den mittleren Ringumfang als Integrationsweg: Θ = N·I umschließt die Durchflutung vollständig.
- (Fortsetzung auf Folgeseiten über S. 80 hinaus)
