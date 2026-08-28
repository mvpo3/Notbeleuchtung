# Elektrotechnik für Architekten,Bauingenieure und Gebäudetechniker — Teil 3
> Quelle: Elektrotechnik für Architekten,Bauingenieure und Gebäudetechniker (buecher) · Seiten 121-160.

Dieser Teil behandelt die elektromagnetischen Grundlagen veränderlicher Felder (Kapitel 11), die Wechselstromtechnik mit komplexer Rechnung (Kapitel 12) sowie den Einstieg in die Drehstromtechnik (Kapitel 13). Der Schwerpunkt liegt auf induzierten Spannungen, Selbst- und Gegeninduktion, Schaltungen mit R, L, C im Wechselstromkreis sowie Leistungsarten und deren Berechnung.

## Inhalt

### Kapitel 11: Veränderliche magnetische Felder

#### 11.1 Das Induktionsgesetz
- Fließt in einem Leiter ein zeitlich konstanter Strom und nähert sich eine geschlossene Leiterschleife diesem Leiter, entsteht während der Bewegung ein induzierter Strom in der Schleife.
- Grundprinzip: Eine Spannung wird entweder durch Veränderung des Magnetfelds oder durch Verschiebung von Ladungen erzeugt.
- An den Enden einer Spule tritt eine Spannung auf, wenn ein Magnet im Inneren bewegt wird, da sich der magnetische Fluss ändert.
- Durch die Bewegung eines Leiters im Magnetfeld der Flussdichte B entsteht ein elektrisches Feld: E_ind = v · B.
- Die in einer Leiterschleife induzierte Spannung entspricht der zeitlichen Änderungsrate des mit der Schleife verknüpften magnetischen Flusses.
- Formel: u_i = −N · dΦ/dt (Gleichung 11.1)

**Unterscheidung der Induktionserscheinungen nach Art der Flussänderung:**
- Ruheinduktion: Das Magnetfeld ändert Größe und/oder Richtung in Abhängigkeit der Zeit; Induktionsweg und Feld befinden sich relativ zueinander in Ruhe (Beispiel: Transformator).
- Bewegungsinduktion: Das Magnetfeld ändert seine Größe/Richtung zeitlich nicht; Induktionsweg und Magnetfeld bewegen sich relativ zueinander (Beispiel: Generator und Motor).

**Unterscheidung nach Ort von Ursache und Wirkung:**
- Selbstinduktion: Die induzierte Spannung entsteht in derselben Schleife, in der der stromverursachende Strom fließt.
- Gegeninduktion: Die induzierte Spannung entsteht in einer anderen Schleife als jener, in der der ursächliche Strom fließt.

#### 11.1.1 Rotatorische Induktion
- Eine Spule rotiert im Magnetfeld oder das Magnetfeld verändert sich in einer ruhenden Spule.
- Voraussetzung: B = konstant, A ändert sich, drehbare Leiterschleife im homogenen Magnetfeld.
- Die magnetisch wirksame Fläche ist winkelabhängig: Φ = B · Â · cos(ωt).
- Induzierte Spannung: u(t) = N · B · Â · ω · sin(ωt) = û · sin(ωt) (Gl. 11.4).

#### 11.1.2 Transformatorische Induktion
- In einer ruhenden Spule verändert sich der magnetische Fluss zeitlich (dΦ/dt).
- Voraussetzung: A = konstant, B ändert sich.
- Induzierte Spannung: u(t) = −N · Φ̂ · ω · cos(ωt) = −û · cos(ωt) (Gl. 11.5).
- Wechselspannungen und Wechselströme können mittels des Induktionsgesetzes transformiert werden.

#### 11.1.3 Lenzsche Regel
- Eine angelegte Spannung induziert einen Strom, der ein Magnetfeld aufbaut, welches dem auslösenden Magnetfeld entgegenwirkt.
- Flusszunahme (dΦ/dt > 0 → i > 0) führt zu einem Gegenfeld; Flussabnahme (dΦ/dt < 0 → i < 0) bewirkt gleichgerichtetes Feld.
- Grundaussage: Der induzierte Strom wirkt stets der Flussänderung entgegen, die ihn hervorruft.

#### 11.2 Induktivität und Selbstinduktion
- Die Induktivität bezeichnet die Eigenschaft einer Spule, bei Stromänderungen eine Selbstinduktionsspannung zu erzeugen.
- Betrachtung einer widerstandslosen Leiterschleife mit eingeprägtem zeitlich veränderlichem Strom i(t):
  - u_i(t) = −N · dΦ/dt = N² · Λ · di(t)/dt (Gl. 11.6)
  - u_i(t) = −L · di(t)/dt (Gl. 11.7)
  - L = N² · Λ = N² · Φ/Θ (Gl. 11.8)
- L ist die Selbstinduktivität; sie hängt von der Spulengeometrie und dem magnetischen Material im Spulenquerschnitt ab.
- Die Induktivität L ist proportional zum Quadrat der Windungszahl N und dem magnetischen Leitwert Λ.
- L ist im Magnetfeld das Analogon zur Kapazität C im elektrischen Feld — beide sind integrale Größen ihrer jeweiligen Felder.

#### 11.3 Gegeninduktivität und Gegeninduktion
- Beschreibung am Beispiel eines Wechselstromtransformators mit N Windungen primär- und sekundärseitig.
- Die Stromänderung in Spule 1 bewirkt eine induzierte Spannung in Spule 2.
- Gleichungen für zwei magnetisch gekoppelte Spulen:
  - u1 = L1 · di1/dt + M · di2/dt (Gl. 11.9)
  - u2 = M · di1/dt + L2 · di2/dt (Gl. 11.10)
- Gegeninduktivität ist zwischen beliebigen Stromkreisen stets vorhanden.
- Feste Flussverkopplung ist bei Motoren und Transformatoren erwünscht; Streuung ist unerwünscht.
- Bei Signalleitungen ist Flusskopplung unerwünscht und störend.

**Selbst- und Gegeninduktion an zwei Spulen:**
- Fluss Φ1 = Φ11 + Φ12
- Eingangsspannung: u1 = N1 · dΦ1/dt (Gl. 11.16)
- Ausgangsspannung: u2 = N2 · dΦ12/dt (Gl. 11.17)
- Mit Selbstinduktivität L1 = N1 · dΦ1/di1 und Gegeninduktivität M21 = N2 · dΦ12/di1
- Induzierte Ausgangsspannung: u2 = M21 · di1/dt (Gl. 11.21)
- Bei Anschluss der Sekundärseite an u2, Primärseite offen:
  - u2 = L2 · di2/dt (Gl. 11.22)
  - u1 = M12 · di2/dt (Gl. 11.23)
  - M12 = N1 · dΦ21/di2 (Gl. 11.24)
- Es gilt: M12 = M21 = M (Symmetrie der Gegeninduktivität).
- M nimmt stets positive Werte an; das Vorzeichen von M · di/dt wird durch Prüfung der Ausrichtung oder durch Anwendung der Lenzschen Regel und der Rechte-Hand-Regel bestimmt.
- Beide Spulen werden physikalisch gewickelt und mit einem Punkt (Wicklungssinn) gekennzeichnet.
- Regel: Fließt ein Strom in den gepunkteten Anschluss einer Spule, ist die gegenseitige Spannung in der zweiten Spule positiv.
- Gesamtspulenspannungen im Zeitbereich:
  - u1 = i1 · R1 + L1 · di1/dt + M · di2/dt (Gl. 11.26)
  - u2 = i2 · R2 + L2 · di2/dt + M · di1/dt (Gl. 11.27)
- Im Frequenzbereich:
  - U1 = I1 · (R1 + jωL1) + jωM · I2 (Gl. 11.28)
  - U2 = I2 · (R2 + jωL2) + jωM · I1 (Gl. 11.29)

#### 11.4 Zusammenschaltung von Induktivitäten
- Voraussetzung: keine magnetischen Kopplungen, keine ohmschen Widerstände.

**11.4.1 Reihenschaltung:**
- u_AB = u1 + u2 + u3 + ... + un (Gl. 11.30)
- u_AB = (L1 + L2 + ... + Ln) · di/dt = L_G · di/dt (Gl. 11.32)
- Gesamtinduktivität: L_G = L1 + L2 + ... + Ln = Σ Li (Gl. 11.33)
- Der Gesamtwiderstand bei Reihenschaltung entspricht der Summe der Einzelinduktivitäten.

**11.4.2 Parallelschaltung:**
- 1/L_G = 1/L1 + 1/L2 + ... + 1/Ln (Gl. 11.35)
- Für zwei Induktivitäten: L_G = (L1 · L2) / (L1 + L2) (Gl. 11.36)
- Der Gesamtwiderstand bei Parallelschaltung ist der Kehrwert der Summe der Kehrwerte der Einzelinduktivitäten.

#### 11.5 Beispiel: Magnetische Felder — Reihen- und Parallelschaltung
- Berechnungsaufgabe: Gesamtinduktivität einer kombinierten Schaltung.
- Ergebnis: L_G = (L1 · L2)/(L1 + L2) + L3 = 0,511 H

#### 11.6 Wirbelstrom und Skineffekt

**11.6.1 Wirbelstrom:**
- Wenn ein zeitlich veränderlicher Fluss Φ(t) einen Leiter durchsetzt, entstehen aufgrund des elektrischen Wirbelfeldes Wirbelströme.
- Wirbelströme verursachen Verluste und bewirken Erwärmung des Metalls.

**11.6.2 Skineffekt:**
- Wirbelströme verringern die Stromdichte im Leiterinneren und erhöhen sie am Rand.
- Bei höherer Frequenz fließt der Strom durch Stromverdrängung nur noch in einer dünnen Randschicht des Leiters — dieser Effekt heißt Skineffekt.

#### 11.7 Auf- und Entladevorgänge bei Induktivität
- Wird eine Induktivität L in einen Stromkreis eingeschaltet, steigt der Strom nicht sofort an, sondern wächst exponentiell auf seinen Endwert an.
- Der Strom eilt der Spannung nach.
- Knotengleichung: u_q = u_R + u_L → 0 = i · R + L · di/dt − u_q (Gl. 11.37/11.38)
- Lösung beim Einschalten: i(t) = I · (1 − e^(−t/τ)) (Gl. 11.39)
- Zeitkonstante: τ = L/R
- Bei Unterbrechung des Stromkreises versucht der Strom weiterzufließen (Trägheitscharakter).
- Die induzierte Spannung stellt sich so ein, dass der Strom kontinuierlich abnimmt.
- Durch die dabei entstehende hohe Spannung kann ein Durchschlag über die Luftstrecke des offenen Schalters entstehen.
- Eine Schutzbeschaltung für mechanische und elektronische Schalter ist daher erforderlich.

#### 11.8 Magnetische Energie
- In der Spule wird magnetische Energie gespeichert — analog zur elektrischen Energie im Kondensator.
- Die gespeicherte magnetische Energie hängt nicht von der Zeit oder vom zeitlichen Stromverlauf ab, sondern nur vom Augenblickswert des Stroms.
- Formel: W_L = ½ · L · i²(t) (Gl. 11.40)

#### 11.9 Anwendungen von Spulen
Spulen finden Einsatz bei:
1. Erzeugung starker Magnetfelder
2. Medizinischen Anwendungen (Kernspintomografie)
3. Elektrischen Maschinen (Motoren, Transformatoren, Generatoren)
4. Elektromagnetischen Schutz- und Schalteinrichtungen
5. Lautsprechern

---

### Kapitel 12: Grundbegriffe der Wechselstromtechnik

#### Erzeugung von Wechselspannung
- Bei Gleichspannung und Gleichstrom sind Strom und Spannung konstant; bei Wechselgrößen sind beide zeitlich veränderliche, periodische Größen, die ständig die Richtung wechseln.
- Wechselspannung entsteht durch Induktion: An den Spulen eines Generators wechseln Nord- und Südpol des Läufers ab, wodurch Stärke und Richtung des Felds in jeder Spule fortlaufend wechseln.
- An den Klemmen der Ständerwicklung ist die Wechselspannung abgreifbar.
- Sinusförmige Wechselspannung lässt sich durch mechanische Rotationsbewegung und das Induktionsgesetz erzeugen.

#### 12.1 Kenngrößen von Wechselstrom
- Periodische sinusförmige Wechselgrößen werden durch Periodendauer, Frequenz und Effektivwerte beschrieben.
- Darstellung mittels Linien- und Zeigerdiagrammen.
- Zeitfunktion: u(t) = û · sin(ωt) (Gl. 12.1)
- Ströme und Spannungen erzeugen in Netzwerkelementen Wirkungen wie Widerstandserwärmung; dabei sind Mittelwerte von Energien und Leistungen maßgeblich.

**Effektivwert (quadratischer Mittelwert):**
- U = √(1/T · ∫ u²(t) dt) (Gl. 12.2)
- Vereinfacht: U = û / √2 (Gl. 12.3); I = î / √2 (Gl. 12.4)
- Leistung: P = U · I (Gl. 12.5)
- In der technischen Wechselstromlehre wird mit Effektivwerten und Phasenbeziehungen gerechnet.

**Nullphasenwinkel:**
- Die Zeit vom Nullpunkt bis zum ersten positiven Nulldurchgang heißt Nullzeitpunkt t0; der zugehörige Winkel ist der Nullphasenwinkel φ0.
- u(t) = û · sin(ωt + φ0) (Gl. 12.6)
- Kenngrößen: û = Scheitelwert/Amplitude in V; T = Periodendauer in s; f = Frequenz in Hz (= 1/T); φ0 = Nullphasenwinkel; ω = Kreisfrequenz in 1/s.

**Bedeutung harmonischer Schwingungen:**
- Die meisten Großgeneratoren liefern sinusförmige Spannungen und Ströme.
- In der Informationstechnik lassen sich Sinusgrößen mithilfe von Resonanzsystemen (Schwingkreisen) erzeugen und für Informationsübertragung nutzen.
- Mathematisch kann jeder periodische nichtharmonische Vorgang durch harmonische Funktionen nachgebildet werden (Fourier-Analyse).

#### 12.2 Einführung in das Rechnen mit komplexen Zahlen

**12.2.1 Begriffe und Rechenregeln:**
- Eine komplexe Zahl wird als Zeiger in der komplexen Ebene dargestellt.
- Normalform (algebraische Form): Z = a + jb; a = Realteil, b = Imaginärteil, j = imaginäre Einheit.
- Betrag: |Z| = √(a² + b²) (Gl. 12.8); a = Z · cos α (Gl. 12.9); b = Z · sin α (Gl. 12.10)
- Trigonometrische Form: Z = Z · (cos α + j sin α) (Gl. 12.11)
- Zeigerform: Z = Z · ∠arccos α (Gl. 12.12)
- Exponentialform (Euler): Z = Z · e^(jωt) (Gl. 12.13); dabei gilt α = ωt + φ.

**12.2.2 Rechenregeln für komplexe Zahlen:**
- Addition/Subtraktion erfordern die Komponentenform: z1 ± z2 = (a1 ± a2) + j(b1 ± b2) (Gl. 12.14)
- Multiplikation in Exponentialform: z1 · z2 = z1 · z2 · e^(j(φ1+φ2)) (Gl. 12.15)
- Division: z1/z2 = (z1/z2) · e^(j(φ1−φ2)) (Gl. 12.16)
- Spezielle Werte der imaginären Einheit: j⁰ = 1; j¹ = j; j² = −1; j³ = −j; j⁴ = 1.

#### 12.3 Komplexe Größen der Wechselstromtechnik
- Die komplexe Mathematik überträgt sich auf die Elektrotechnik; damit sind Ohmsches Gesetz und Kirchhoffsche Regeln direkt im Wechsel-/Drehstromkreis anwendbar, ohne Additionstheoreme.
- Zeiger: Z = û · (cos φ + j sin φ) = û · e^(jφ) (Gl. 12.17); Z steht für Zeiger, û für den Betrag (Scheitelwert).
- Betrachtung eines mit Winkelgeschwindigkeit ω umlaufenden Zeigers der Länge û.

**Vorteile der Zeigerdarstellung:**
1. Numerisch: Rechnung mit Real-/Imaginärteil oder Betrag und Phasenlage.
2. Grafisch: Darstellung als Zeigerdiagramm.
- Phasenverschiebung = Differenz der Nullphasenwinkel (eine Größe wird als Referenz festgelegt); der Phasenwinkel hängt von Schaltungsaufbau und Frequenz ab.
- Spannungs- und Stromzeiger: U = U · e^(jφu) (Gl. 12.18); I = I · e^(jφi) (Gl. 12.19).
- Erweitertes Ohmsches Gesetz für Wechselgrößen: Komplexe Impedanz Z = U/I = (U/I) · e^(j(φu−φi)) (Gl. 12.20).
- Zerlegung der Impedanz: Z = R + jX; R = Wirkwiderstand (Resistanz), X = Blindwiderstand (Reaktanz) (Gl. 12.21).
- Admittanz: Y = 1/Z = G + jB; G = Wirkleitwert (Konduktanz), B = Blindleitwert (Suszeptanz) (Gl. 12.22).

#### 12.4 Einfache Sinusstromkreise

**12.4.1 Wechselspannung/-strom am Ohmschen Widerstand:**
- Bei einem rein ohmschen Widerstand sind Strom und Spannung in Phase (kein Phasenversatz).

**12.4.2 Wechselspannung/-strom an einer Induktivität:**
- Der Strom erzeugt in der Spule ein sich mit ihm änderndes Magnetfeld.
- Eine Induktivität bewirkt eine Phasenverschiebung von 90° zwischen Spannung und Strom.
- Der Strom eilt der Spannung um 90° nach; das Strommaximum folgt dem Spannungsmaximum um 90° verzögert.

**12.4.3 Wechselspannung/-strom am Kondensator:**
- Der Kondensator wird ständig auf- und entladen, da Spannung ihre Größe und Richtung kontinuierlich ändert.
- Ein Kondensator bewirkt eine Phasenverschiebung von 90° zwischen Spannung und Strom.
- Die Spannung eilt dem Strom um 90° nach; das Spannungsmaximum folgt dem Strommaximum um 90° verzögert (Strom eilt Spannung vor).

#### 12.5 Berechnung von Sinusstromnetzwerken
- Die Kirchhoffschen Gesetze gelten auch für Wechselstromnetze mit komplexen Größen U, I, Z, Y.

**12.5.1 Reihenschaltung:**

*RL-Reihenschaltung:*
- Komplexer Widerstand: Z = R + jX = R + jωL = Z · e^(jφ) (Gl. 12.23)
- Scheinwiderstand: Z = √(R² + (ωL)²) (Gl. 12.24)
- Phasenwinkel: φ = arctan(X/R) (Gl. 12.25)

*RC-Reihenschaltung:*
- Komplexer Widerstand: Z = R + 1/(jωC) (Gl. 12.26)
- Scheinwiderstand: Z = √(R² + (1/ωC)²) (Gl. 12.27)
- Phasenwinkel: φ = arctan(X_C/R) (Gl. 12.28)

*RLC-Reihenschaltung:*
- Komplexer Widerstand: Z = R + j(ωL − 1/(ωC)) (Gl. 12.29)
- Scheinwiderstand: Z = √(R² + (ωL − 1/(ωC))²) (Gl. 12.30)
- Phasenwinkel: φ = arctan((ωL − 1/(ωC)) / R) (Gl. 12.31)

**12.5.2 Parallelschaltung:**

*RL-Parallelschaltung:*
- Admittanz: Y = 1/R + 1/(jωL) = G + jB_L (Gl. 12.32)
- Betrag der Admittanz: Y = √((1/R)² + (1/(ωL))²) (Gl. 12.33)
- Gesamtstrom: I = U · √((1/R + 1/(jωL))) (Gl. 12.34)
- Scheinwiderstand: Z = 1 / √((1/R)² + (1/(ωL))²) (Gl. 12.35)
- Phasenwinkel: φ = arctan((1/(ωL)) / (1/R)) (Gl. 12.36)

*RC-Parallelschaltung:*
- Admittanz: Y = 1/R + jωC = G + jB_C (Gl. 12.37)
- Betrag der Admittanz: Y = √((1/R)² + (ωC)²) (Gl. 12.38)
- Gesamtstrom: I = U · √((1/R + jωC)) (Gl. 12.39)
- Scheinwiderstand: Z = 1 / √((1/R)² + (ωC)²) (Gl. 12.40)
- Phasenwinkel: φ = −arctan(R / X_C) (Gl. 12.41)

*RLC-Parallelschaltung:*
- Admittanz: Y = G + j(ωC − 1/(ωL)) (Gl. 12.42)
- Betrag der Admittanz: Y = √((1/R)² + (ωC − 1/(ωL))²) (Gl. 12.43)
- Gesamtstrom: I = I_R + I_C + I_L (Gl. 12.44); I = √(I_R² + (I_C − I_L)²) (Gl. 12.45)

#### 12.6 Leistungen im Wechselstromkreis
- Elektrische Maschinen und Geräte werden mit Wechselspannung/Wechselstrom betrieben.
- Transformatoren, Elektromotoren und manche Beleuchtungsanlagen besitzen neben induktivem Blindwiderstand X_L auch einen nicht vernachlässigbaren Wirkwiderstand R (Wicklungsmaterial).
- Scheinwiderstände führen zu Phasenverschiebungen zwischen Strom und Spannung, was nachteilige Auswirkungen auf das Energieversorgungssystem hat.
- Bei Wechselstrom schwingt die Leistung ebenso wie Strom und Spannung zwischen Maximum und Minimum.

**Scheinleistung:**
- Geometrische Addition von Wirk- und Blindleistung; Bemessungsgröße für Betriebsmittel.
- Für Stern- und Dreieckschaltungen: S = U · I* → S = U · I = √(P² + Q²) (Gl. 12.46)
- Gesamtscheinleistung: S_Gesamt = 3 · S_Strang (Gl. 12.47)

**Wirkleistung:**
- Der Anteil der Scheinleistung, der beim Verbraucher Arbeit verrichtet und letztlich in Wärme übergeht.
- P_Strang = U_Strang · I_Strang · cos φ_Strang (Gl. 12.48)

**Blindleistung:**
- Pendelt zwischen Erzeuger und Verbraucher, belastet das Netz und beeinträchtigt die effektive Übertragung der Wirkleistung.
- Schwingt mit doppelter Frequenz 2ω um die Nulllinie.
- Zwischenzeitlich gespeichert im elektrischen Feld (Kondensator) oder magnetischen Feld (Induktivität) des Verbraucherzweipols.
- Im zeitlichen Mittel wird im Verbraucher durch Blindleistung keine Energie irreversibel umgesetzt.
- Die Pendelbewegung belastet Kabel und Leitungen thermisch (Verlustleistungen).
- Wird in der Einheit var angegeben.
- Eingeführte Begriffe: Blindspannung und Blindstrom (Komponenten parallel zur imaginären Achse im Zeigerdiagramm).
- Q_Strang = U_Strang · I_Strang · sin φ_Strang (Gl. 12.49)
- Maßnahme: Kompensation durch geeignete Schaltungen mit Kapazitäten und Induktivitäten.

**12.6.1 Blindstromkompensation:**
- Bei Zusammenschaltung beliebiger Bauelemente (R, L, C) entsteht eine resultierende Phasenverschiebung → neben Wirkleistung auch Blindleistung.
- Benötigte Kompensationsblindleistung: Q_C = P · tan φ (Gl. 12.50)
- Erforderliche Kondensatorkapazität für Wechselstrom: C = Q_C / (ω · U²) (Gl. 12.51)
- Erforderliche Kondensatorkapazität für Drehstrom: C = Q_C / (3 · ω · U²) (Gl. 12.52)

**12.6.2 Leistungsfaktor:**
- Die Wirkleistung ergibt sich als Summe der Einzelwirkleistungen der Stränge. Da die Summe der Phasenverschiebungen zwischen den Strängen Null ergibt, ist die Summenleistung konstant.
- Leistungsfaktor: Kennwert zur Beschreibung der Wirkleistungsaufnahme eines Wechselstromverbrauchers; bei rein sinusförmigen Größen bei 50 Hz ist er gleich dem Verschiebungsfaktor.
- Verschiebungsfaktor: wichtige Qualitätsgröße für Motoren und elektrische Antriebe.
- Praktischer Hintergrund: Jeder Motor besitzt neben Wirkleistungsaufnahme auch Blindleistungsanteile (R + L in der Wicklung). Bei großen Verbrauchern erreichen induktive Blindanteile hohe Werte → Blindstromzähler oder Kompensationsanlage beim Abnehmer.
- Leistungsfall und Verluste auf Zuleitungen: An der Zuleitung (z.B. für einen Motor) fällt Spannung und Leistung ab; bei Wechselstrom muss der Leistungsfaktor berücksichtigt werden.
- Auslegung von Zuleitungen: Der Leistungsfaktor beeinflusst direkt den Betriebsstrom → wirkt auf erforderlichen Leitungsquerschnitt.

**Zusammenfassung der Leistungsformeln:**
- Wirkleistung in W: P = U · I · cos φ (Gl. 12.53)
- Scheinleistung in VA: S = U · I (Gl. 12.54)
- Blindleistung in var: Q = U · I · sin φ (Gl. 12.55)
- Leistungsfaktor: λ = P/S ≤ 1 (Gl. 12.56); bei 50 Hz gilt λ = cos φ.

**12.6.3 Beispiel: Leistungsberechnung und Blindstromkompensation**
- Gegebener Verbraucher: 4 kW Wechselstrom, U = 230 V, cos φ = 0,8.
- Ziel: Verbesserung des Leistungsfaktors auf cos φ = 0,95.

Vor der Kompensation:
- S1 = P / cos φ1 = 4 kW / 0,8 = 5 kVA
- Q1 = S1 · sin φ1 = 5 kVA · 0,6 = 3 kvar

Nach der Kompensation:
- S2 = P / cos φ2 = 4 kW / 0,95 = 4,2105 kVA
- Q2 = S2 · sin φ2 = 4,2105 kVA · 0,3123 ≈ 2,5263 kvar (sin φ2 für cos φ2 = 0,95 → sin φ2 ≈ 0,3123)

Kompensationsblindleistung und Kapazität:
- Q_C = Q1 − Q2 = 3 kvar − 2,5263 kvar = 0,4737 kvar
- C = Q_C / (ω · U²) = 0,4737 kvar / (ω · (230 V)²) = 28,5 nF

---

### Kapitel 13: Drehstromtechnik

#### Einleitung Drehstromtechnik
- Elektrische Energie entsteht in Kraftwerken durch Energieumwandlung aus mechanischer Energie (Turbinenrotor), Wärmeenergie (Dampferzeuger) oder chemischer Energie (Verbrennung).
- Übertragung und Verteilung über weite Strecken erfolgen mit dem symmetrischen Dreiphasensystem (Drehstromsystem).
- Zur Erzeugung werden drei räumlich um je 120° versetzte Spulen (Stränge) benötigt.
- In diesen Strängen werden drei gleich große Wechselspannungen induziert, die jeweils um 360°/3 = 120° gegeneinander phasenverschoben sind.
- Unterscheidung zwischen drei- und einphasigen Verbrauchern.
- Drehstromverbraucher: drei Einzelwiderstände oder Spulen (Stränge), meist in Stern- oder Dreieckschaltung.

#### 13.1 Arten der Drehstromsysteme, Bezeichnungen
- Sternschaltung (Y): Sternpunktknoten verbindet alle Spulenabgänge sowie den Neutralleiter.
- Dreieckschaltung: Jeweils ein Spulenausgang wird an den Anfang der benachbarten Spule angeschlossen; die Anschlussknoten führen zu den drei Außenleitern L1, L2 und L3.
- Strangspannung: messbare Spannung zwischen zwei Punkten eines Stranges; beträgt ca. 230 V; Bezeichnung mit Strangindex (z.B. V-Strangspannung).
- Verkettete Spannung (Außenleiterspannung): messbare Spannung zwischen zwei Strängen.
- Zur Übertragung vom Generator zum Verbraucher können die Leitungen der Wicklungsstränge unterschiedlich zusammengeschaltet werden.
- Bei großen Leistungen ist es vorteilhaft, mehrphasige Spannungs- und Stromsysteme zu erzeugen und mit Mehrfachleitungen zu übertragen anstelle einfacher Wechselspannung mit Doppelleitung.
- Das symmetrische Dreiphasensystem hat besondere technische Bedeutung.

#### 13.2 Schaltungen der Drehstromsysteme
- Dreiphasenwechselströme bestehen aus drei um jeweils 120° phasenverschobenen Wechselspannungsquellen.
- Mit drei Spannungsquellen werden theoretisch sechs Leitungen benötigt; in der Energietechnik werden jedoch nur drei oder vier Leitungen verwendet.
- Zwei Schaltungsvarianten für Quellen und Verbraucher.
- Darstellung eines Dreiphasensystems mit Sternpunktleiter sowie Zeigerdiagramme der Strangspannungen werden in den Schaltbildern gezeigt (Bilder 13.1–13.8 im Original).
