# Grundladen der elektrischen Energietechnik — Teil 8
> Quelle: Grundladen der elektrischen Energietechnik (buecher) · Seiten 321-360.

Dieser Teil behandelt fortgeschrittene Modellierungs- und Berechnungsverfahren für elektrische Energienetze: Nullimpedanz-Messung, abstrakte Ersatzschaltbilder in symmetrischen Komponenten, Knotenspannungsgleichungssysteme, Leistungsflussberechnung (Einzel- und Mehrfachlast, Newton-Raphson-Verfahren) sowie die verschiedenen Varianten der Sternpunktbehandlung in Drehstromnetzen mit Fokus auf einpolige Erdfehler.

## Inhalt

### Messung der Nullimpedanz (Seite 321)

- Mit- und Gegenimpedanz sind einander gleich, unterscheiden sich aber von der Nullimpedanz: Z1 = Z2 ≠ Z0
- Zur Nullimpedanz-Messung wird am Betriebsmittel eine Wechselspannung U0 angelegt und der dreifache Nullstrom 3·I0 gemessen
- Für Kurzschluss- oder Leistungsflussrechnungen werden Schalter im Ersatzschaltbild geschlossen; bei Leerlaufvorgängen (z. B. Blindleistungsaufnahme eines Transformators) bleiben die Schalter offen

### Komplexe Scheinleistungen in symmetrischen Komponenten (Seite 321)

- Die Transformationsmatrix für symmetrische Komponenten ist leistungsvariant: Die Drehstromleistung SS in symmetrischen Komponenten weicht von der tatsächlichen Leistung SL im Leitersystem ab: SS = (1/3) · SL
- Eine leistungsinvariante Darstellung ist in DIN IEC 62428 "Elektrische Energietechnik — Modale Komponenten in Drehstromsystemen — Größen und Formelzeichen" beschrieben

### Abstrakte Ersatzschaltbilder und Netzgleichungssysteme (Abschnitt 4.2)

#### Zweipolige Ersatzschaltbilder (Abschnitt 4.2.1, Seiten 313-314)

- Aktive Querelemente (Generatoren, Motoren, Ersatznetze) und passive Querelemente (Paralleldrosseln, Kondensatoren) werden als Zweipole modelliert
- Freileitungen, Kabel, Zweiwicklungstransformatoren, Längsdrosseln und Reihenkondensatoren als Vierpoleschaltbilder
- Im Mitsystem ist eine Quellenspannung U1q vorhanden (symmetrischer Maschinenaufbau vorausgesetzt); Gegen- und Nullsystem haben keine Quelle

**Impedanzen Z1 und Quellenspannungen U1q im Mitsystem (Tab. 4.4):**

| Betriebsmittel | Zustand | Z1 | U1q |
|---|---|---|---|
| Synchrongenerator | subtransient | Ra + j·X''d | U''1 |
| Synchrongenerator | transient | Ra + j·X'd | U'1 |
| Synchrongenerator | stationär | Ra + j·Xd | Up(If) |
| Asynchronmotor | quasi-stationär | Rs + j·X's | U'1 |
| Asynchronmotor | stationär | Z1(s) | — |
| Ersatznetze | quasi-stationär / stationär | R1N + j·X1N | U1N = const. |

- Passive Zweipole (nichtmotorische Lasten, Paralleldrosseln, Kondensatoren) werden nur mit Admittanzen Y1, Y2, Y0 dargestellt — ohne Quellenspannung
- Spannungsabhängigkeit von Wirk- und Blindleistung passiver Lasten im Mitsystem: Potenzfunktionen mit reellen Exponenten; für Gegen- und Nullsystem kaum verfügbare Daten; in Kurzschlussberechnungen werden Lasten grundsätzlich vernachlässigt
- Kompakte Matrixdarstellung der Stromgleichungen aller Zweipole in symmetrischen Komponenten: IS = YS · US + ISk (Quellenströme nur im Mitsystem aktiver Betriebsmittel)

#### Vierpolige Ersatzschaltbilder (Abschnitt 4.2.2, Seiten 315-317)

- Freileitungen und Kabel werden mit symmetrischen Eigenschaften modelliert (Verdrillen bei Freileitungen, Auskreuzen der Schirme bei Kabeln)
- Pi-Ersatzschaltbilder bevorzugt (kein innerer Knoten)
- Leitungsparameter im Mit- und Gegensystem sind identisch, unterscheiden sich von den Nullsystemwerten

**Typische Leitungsbeläge Mit-/Gegensystem (Tab. 4.5):**

| Leitungstyp | R'b [Ω/km] | X'b [Ω/km] | C'b [nF/km] |
|---|---|---|---|
| Freileitung | 0,03 … 0,4 | 0,25 … 0,4 | 9 … 13 |
| Kabel | 0,03 … 0,4 | 0,1 … 0,2 | 250 … 600 |

**Typische Leitungsbeläge Nullsystem (Tab. 4.6):**

| Leitungstyp | R'0 | X'0 | C'0 |
|---|---|---|---|
| Freileitung | (2 … 9) · R'b | (3 … 6) · X'b | (0,4 … 0,6) · C'b |
| Kabel | 0,4 … 2 Ω/km | 0,3 … 0,7 Ω/km | 200 … 300 nF/km |

- Admittanzen der Halbglieder: YiA = YiB = (Gi + jωCi)/2; Längsadmittanz YiC = 1/(Ri + jXi)
- Symmetrischer Aufbau entkoppelt die Vierpolgleichungen; Admittanzmatrix für Transformatoren nicht immer symmetrisch
- In Verteilnetzen werden Ableitungen und Betriebskapazitäten häufig vernachlässigt

#### Knotenspannungs-Gleichungssysteme (Abschnitt 4.2.3, Seiten 317-318)

- Knotenadmittanzdarstellung (neben Maschenimpedanz- und Knotenimpedanzdarstellung)
- Matrixgleichung: IK = YK · UK
  - UK: Vektor der Leiter-Erd-Knotenspannungen Uα
  - IK: Vektor der Knotenströme Iα (alle Ein- und Ausspeisungen von Generatoren, Netzeinspeisungen, Lasten, Kompensationsdrosseln)
- Knotenstrom Iα = Σ Yαj · Uj (Summe aller Ströme auf abgehende Leitungen/Transformatoren)

**Aufbauregeln der Knotenadmittanzmatrix YK:**
- Diagonalelement Yii = Summe aller am Knoten i angeschlossenen Admittanzen
- Nebendiagonalelement Yij = negativer Wert der Admittanzen zwischen Knoten i und j

**Eigenschaften von YK:**
- Quadratisch, Ordnung n (mit Mit-/Gegen-/Nullsystem: 3n)
- Symmetrisch (außer bei Transformatoren mit phasendrehenden Schaltgruppen)
- Singulär, wenn gleichzeitig: (1) alle Leitungs- und Transformatorquerglieder vernachlässigt und (2) kein Betriebsmittel mit geerdetem Sternpunkt vorhanden
- Schwach besetzt: bei l Leitungen maximal n + 2l Nicht-Null-Elemente; 100-Knoten-Strahlennetz nur ca. 3 % besetzt, Quadratnetz ca. 4,6 %

### Leistungen an den Netzknoten (Abschnitt 4.3, Seiten 319-351)

#### Begriffliche Einordnung (Seite 320)

- Bezeichnung "Leistungsflussberechnung" (engl. Load Flow Calculation, LFC): trotz begrifflicher Unschärfe stark verbreitet; "Lastflussrechnung" ist historisch, sollte nicht mehr verwendet werden
- Im stationären Zustand: Wirk-, Blind- und Scheinleistungen an Netzknoten sind konstant (fließen nicht); zeitliche Variation nur als Momentanleistung mit 100 Hz
- Anwendung: Planung und Betrieb von Drehstromnetzen; für Deutschland/Europa symmetrischer Betrieb annehmbar (einphasige Berechnung im Mitsystem ausreichend)
- Für nordamerikanische einphasig verteilte Netze: dreiphasige Leistungsflussberechnung erforderlich

**Anwendungsfelder der Leistungsflussberechnung:**
- Grundleistungsfluss für störungsfreien Betrieb (Spannungsbandprüfung, thermische Überlastprüfung)
- Schaltmaßnahmen-Simulation vor tatsächlicher Ausführung
- Ausfallanalyse (CA = Contingency Analysis, SA = Security Analysis) für das (n–1)-Prinzip
- Ausgangszustand für Kurzschlussstromberechnung nach Überlagerungsverfahren und Stabilitätsrechnungen
- Schulungssimulationen / Trainingssimulationen
- Optimierende Leistungsflussverfahren (OPF = Optimal Power Flow): Netzverlusminimierung, Spannungsband-Einhaltung

**Netzzustandsestimation (State Estimation, SE / NSD):**
- Online-Berechnung der Knotenspannungen aus redundantem Messwertsatz (Schalterstellungen, Strom-/Spannungsmessungen aus eigenem und benachbartem Netz)
- Für Übertragungsnetze etabliert; für Verteilnetze modifizierte Verfahren in Entwicklung

#### Einzelner Verbraucher an einer Leitung (Abschnitt 4.3.1, Seiten 323-325)

Vereinfachtes Ersatzschaltbild mit Rb und Xb:
- Spannungsbilanz: UQ = UB + ZL · I mit ZL = Rb + j·Xb
- Leistung der Quelle: SQ = 3 · UQ · I*
- Leistung Verbraucher: SB = 3 · UB · I*
- Leitungsverluste: SL = SQ − SB = 3·ZL·I²; Wirkleistung PL = 3·Rb·I², Blindleistung QL = 3·Xb·I²

**Drei Verbrauchercharakteristiken:**

1. **Konstante Impedanz** (z. B. Elektroheizungen): Spannung UB per Spannungsteiler berechenbar; Scheinleistung SB proportional zu UB² (quadratische Abhängigkeit)
2. **Konstanter Strom** (ungeregelte Antriebe): Spannung UB nur iterativ berechenbar (Betrag und Phasenlage des Stroms festgelegt); Scheinleistung proportional zu UB
3. **Konstante Leistung** (geregelte Antriebe): führt immer auf iterative Lösung; Startwert Un/√3 mit Winkel 0; Abbruchkriterium auf Leistungsgröße SB empfohlen (Leistungen reagieren empfindlicher auf Spannungsänderungen als Spannungen)

#### Mehrere Verbraucher an einer Leitung (Abschnitt 4.3.2, Seiten 325-328)

Unverzweigte, einseitig gespeiste Leitung mit n Verbrauchern:
- Alle Verbraucher ohmsch-induktiv; Nullphasenwinkel der Spannungen näherungsweise 0
- Nullphasenwinkel der Ströme φiα sind wegen Phasendifferenz negativ

**Gesamter Spannungsfall ΔUY bei konstantem Strom:**
- Stromwirkmoment MW = Σ Iα · cos(φiα) · Lα (positiv)
- Stromblindmoment MB = Σ Iα · sin(φiα) · Lα (negativ, da Ströme induktiv)
- Aufspaltung: ΔUlY = R'b · MW − X'b · MB (Längsspannungsfall, in Phase mit UQ)
- ΔUqY = X'b · MW + R'b · MB (Querspannungsfall, 90° zu UQ)
- Betrag: ΔUY = √(ΔUlY² + ΔUqY²)

**Gesamter Spannungsfall ΔUY bei konstanter Leistung:**
- Leistungswirkmoment M*W = Σ Pα · Lα (positiv)
- Leistungsblindmoment M*B = Σ Pα · tan(φiα) · Lα (negativ)
- ΔUY = (R'b + j·X'b)/(√3 · Un) · (M*W + j·M*B)
- Längs-/Quer-Aufspaltung analog zur Strommoment-Formel

#### Leistungsflussrechnung für vermaschte Netze (Abschnitt 4.3.3, Seiten 328-337)

**Knotentypen (Tab. 4.7):**

| Knotentyp | Vorgabe | Gesucht |
|---|---|---|
| Slack-Knoten (Bilanz-/Swingknoten) | U und δ | P und Q |
| PV-Knoten (Generatorknoten) | P und U | Q und δ |
| PQ-Knoten (Lastknoten) | P(U) und Q(U) | U und δ |

- Mindestens ein Slack-Knoten nötig: (1) Ausgleich der Leistungsbilanz; (2) Ermöglichung einer Lösung wenn Knotenadmittanzmatrix singulär (Querelemente vernachlässigt)
- Slack-Knoten soll großes Kraftwerk oder Fremdnetzeinspeisung sein; Spannung festgelegt auf U = Un/√3 und δ = 0
- PV-Knoten: Kraftwerkseinspeisung mit geregelter Wirkleistung und Spannung; Blindleistung und Phasenlage werden berechnet; alternativ als negativer PQ-Knoten modellierbar
- PQ-Knoten: Spannungsabhängigkeit der Lasten im Bereich 80 % … 120 % der Nennspannung durch Potenzfunktionen: P = P0·(U/U0)^p und Q = Q0·(U/U0)^q
  - Exponenten p und q erfahrungsgemäß zwischen 1 und 2
  - Sonderfälle: p = q = 0 (konstante Leistung, geregelte Antriebe), p = q = 1 (konstanter Strom, ungeregelte Antriebe), p = q = 2 (konstante Impedanz, Elektroheizungen)
- Mischformen mit Gewichtungskoeffizienten g0, g1, g2 (Summe = 1, jeder ∈ [0,1]) möglich
- Knotentyp kann während eines Rechenlaufs geändert werden (z. B. PQ → PV bei Grenzwertverletzung)

**Standardlastprofile des BDEW (Tab. 4.8):**

| Kürzel | Beschreibung |
|---|---|
| H0 | Haushalt |
| G0 | Gewerbe allgemein (gewogener Mittelwert G1–G6) |
| G1 | Gewerbe werktags 8–18 Uhr (Büros, Arztpraxen, Werkstätten, Verwaltung) |
| G2 | Gewerbe mit starkem Abendverbrauch (z. B. Sportvereine) |
| G3 | Gewerbe durchlaufend (Kühlhäuser, Pumpen, Kläranlagen) |
| G4 | Laden/Friseur |
| G5 | Bäckerei mit Backstube |
| G6 | Wochenendbetrieb (z. B. Kinos) |
| G7 | Mobilfunksendestation (Bandlastprofil) |
| L0 | Landwirtschaft allgemein (gewogener Mittelwert L1, L2) |
| L1 | Landwirtschaft mit Milchwirtschaft/Nebenerwerbs-Tierzucht |
| L2 | Übrige Landwirtschaftsbetriebe |

- Profile differenzieren nach Werktag, Samstag, Sonntag sowie Sommer, Übergangszeit, Winter
- Anwendungsgrenze: Entnahmestellen unter 100.000 kWh/Jahr
- Für Online-Leistungsfluss in Netzleitanlagen werden SCADA-Messwerte genutzt; bei fehlenden Messungen: synthetische Lastprofile als Basis für Lastprognose
- Manche Unternehmen verwenden temperaturkorrigierte Eigenprofile

**Newton-Raphson-Verfahren:**
- Leistungsgleichungen: Knoten- und Netzleistungen müssen ausgeglichen sein: PK − PN = 0, QK − QN = 0
- Netzleistung in Matrixform: SN = 3 · UD · Y*KK · U*K
- Linearisierung durch Taylor-Entwicklung um Näherungswerte δν, Uν (Abbruch nach erstem Glied)
- Kompakte Darstellung mit Jacobi-Matrix Jν: Jν · Δxν+1 = −Δyν
- Startwerte ("flat start"): Ui = Un bzw. 1, δi = 0 für alle Knoten
- Hauptaufwand: in jedem Iterationsschritt Jacobimatrix neu aufstellen und Leistungsdifferenzen neu berechnen; spärlich besetzte Matrizen → spezielle Lösungsverfahren erforderlich
- Konvergenzvarianten: kartesische Koordinaten (Ui = Ei + j·Fi) oder Polarkoordinaten (Ui = Ui·e^(j·δi))

**Koordinatendarstellungen (Tab. 4.9):**

| Darstellung | Knotenspannung Ui | Zustandsvektor x | Admittanz Yij |
|---|---|---|---|
| Kartesisch | Ei + j·Fi | [E1…En F1…Fn]^T | Gij + j·Bij |
| Polar | Ui·e^(j·δi) | [δ1…δn U1…Un]^T | Yij·e^(j·αij) |

- Konvergenzprobleme entstehen durch Eingabefehler (falsche Impedanzen, Leistungen) oder durch Überschreitung der maximalen Übertragungsfähigkeit bei schweren Störungen → entspricht in der Realität einer Spannungsinstabilität bis zum (Teil-)Netzzusammenbruch

### Sternpunktbehandlung und einpolige Erdfehler (Abschnitt 4.4, Seiten 337-351)

#### Grundlagen (Seite 337)

- Im symmetrischen Betrieb: kein Strom außerhalb der isolierten Leiter L1, L2, L3; Neutralleiter N in NS-Ebene stromlos; Sternpunkte auf 0-V-Erdpotenzial
- Bei einpoligen Erdfehlern: Fehlerströme in Kabelmänteln, Erdseilen von Freileitungen oder im Erdreich; getrieben durch Synchrongeneratoren, Transformatoren oder Sternpunktbildner im MS-Netz
- Statorwicklungen von Synchrongeneratoren grundsätzlich mit isoliertem Sternpunkt (Ausnahme: mobile Notstromaggregate, USV-Anlagen)

**Varianten der Sternpunktbehandlung (Tab. 4.10):**

| Variante | Kürzel | Fehlerort-Strom | Spannungsanhebung gesunder Leiter | Fehlerdauer | Lichtbogen | Doppelerdschluss-Gefahr |
|---|---|---|---|---|---|---|
| Ohne Sternpunkterdung | OSPE | Kapazitiver Erdschlussstrom ICE | ja | 10 min … 120 min | selbst löschend (bis einige A) | ja |
| Resonanz-Sternpunkterdung | RESPE | Ohmsch-kapazitiver Reststrom IRES | ja | < 1 s nach KNOSPE | selbst löschend oder stehend | ja |
| Strombegr. niederohmige Erdung | NOSPE | Erdkurzschlussstrom I''k1 | nein | — | meist stehend | gering |
| Direkte Erdung | NOSPE | Erdkurzschlussstrom I''k1 | nein | — | stehend | nein |

**Anwendungsbereiche (aus Tab. 4.10):**
- OSPE isoliert: kleine MS-Netze oder Kraftwerkseigenbedarf
- RESPE gelöscht: 10 kV … 123 kV-Netze mit hohem Freileitungsanteil
- NOSPE strombegr.: 10 kV … 123 kV-Netze mit hohem Kabelanteil
- NOSPE direkt: Hoch-/Höchstspannungsnetze 123 kV … 400 kV

**Netzlängen in Deutschland 2009 nach FNN (Tab. 4.11) [km]:**

| Variante | 10 kV | 20 kV | 110 kV | 220/380 kV |
|---|---|---|---|---|
| OSPE isoliert | 9.465 | 152 | 0 | 0 |
| RESPE gelöscht | 53.104 | 230.779 | 50.090 | 0 |
| NOSPE | 34.968 | 11.083 | 13.688 | 35.783 |

- Resonanz-Sternpunkterdung auch in Österreich, Schweiz, Frankreich verbreitet; Großbritannien und USA bevorzugen NOSPE

#### Schritt- und Berührungsspannungen (Seite 339)

- Bei einpoligem Erdfehler mit leitend geerdetem Sternpunkt: Stromkreis schließt sich über Erder mit Erdungsimpedanz ZE
- Erdspannung UE (EPR = Earth Potential Rise): Potenzialunterschied zwischen Bezugserde und Erdungsanlage; auch Erderspannung, Erdungsspannung genannt
- Schrittspannung US: jene Spannung, die eine Person bei einem Schritt von 1 m Abstand (von Fuß zu Fuß) aufgreift
- Berührungsspannung UT: Spannung bei Kontakt mit einem galvanisch mit der Erdungsanlage verbundenen Bauteil
- Tiefenerder: Rohre oder Stäbe bis zu 40 m Tiefe
- Steuererder: Strahlen-, Ring- und Maschenerder um Haupterder — von innen nach außen mit zunehmend größerer Tiefe verlegt
- Potenzialsteuerung: alle Maßnahmen zur Unterschreitung zulässiger Schritt-/Berührungsspannungen (Erdungsmatten, leitfähige Bodenbeschichtungen, Schutzisolierungen, Potenzialausgleich)

#### Sternpunktverlagerung bei einpoligem Erdfehler (Seite 339-341)

- Bei metallischem einpoligem Erdfehler L1-Erde: Leiter-Leiter-Spannungen U12, U23, U31 bleiben unverändert
- Spannung fehlerhafte Leiter an Fehlerstelle: UF1E = 0
- Spannung gesunde Leiter an Fehlerstelle: erhöht sich um Faktor √3 (Spannungsdreieck bleibt erhalten, verschiebt sich)
- Nicht nur an der Fehlerstelle, sondern im gesamten Netz: Überspannung auf gesunden Leitern
- Zusätzlich zu betriebsfrequenter Spannungserhöhung: kurzzeitige Überspannungen durch Ausgleichsvorgänge bis zum 2,5-fachen der Netznominalspannung

**Detektion per Spannungswandler:**
- Einpolig isolierte induktive Spannungswandler mit Erdschlusswicklung (da-dn-Wicklung) auf Messkern
- Drei Wandler: Erdschlusswicklungen in Reihe = offenes Dreieck → misst geometrische Summe der Leiter-Erd-Spannungen
- Ungestört: U1E + U2E + U3E = 0
- Bei metallischem einpoligem Erdfehler: Summe ≠ 0, an Erdschlusswicklung liegt 100 V Nennspannung an
- Bei NOSPE wird dieses Verfahren nicht verwendet

**Darstellung mit symmetrischen Komponenten:**
- Aufgrund der Fehlerbedingungen (IF2E = IF3E = 0) sind Mit-, Gegen- und Nullsystemstrom an der Fehlerstelle gleich: I1L1 = I2L1 = I0L1 = IeF / 3
- Fehlerbedingung UF1E = 0 liefert: U1L1 + U2L1 + U0L1 = 0
- Folge: Ersatzschaltbilder von Mit-, Gegen- und Nullsystem werden in Reihe geschaltet
- Einpoliger Erdfehlerstrom bei metallischem Fehler: IeF = √3 · UbN / (Z1 + Z2 + Z0)
- Übergangswiderstand RF kann ergänzt werden

**Varianten des einpoligen Erdfehlerstroms (Tab. 4.12):**

| Kürzel | Bezeichnung |
|---|---|
| IeF | Einpoliger Erdfehlerstrom allgemein |
| ICE | Kapazitiver Erdschlussstrom (OSPE) |
| IRES | Ohmsch-kapazitiver Erdschluss-Reststrom (RESPE) |
| I''k1 | Einpoliger Anfangs-Kurzschlusswechselstrom (NOSPE) |

#### Netze ohne Sternpunkterdung — OSPE (Abschnitt 4.4.2, Seiten 342-345)

- Älteste Betriebsweise; noch heute in MS-Netzen kleinerer Ausdehnung
- Bezeichnungen: Netz mit freiem Sternpunkt, sternpunktisoliertes Netz
- Weitere Anwendungen: IT-Systeme in Gebäuden, Bordnetze in Flugzeugen und Schiffen, Kraftwerks-Eigenbedarf
- Symmetrische Erdkapazitäten vorausgesetzt: C1E = C2E = C3E = CE

**Berechnung kapazitiver Erdschlussstrom:**
- Erdfehlerstrom primär durch Erdkapazität CE im Nullsystem bestimmt
- IeF ≈ √3 · UbN · ω · CE
- Planungsaufschlag: UbN ≈ 1,1 · UnN (10 % Sicherheitsaufschlag auf Netznominalspannung, analog zu EN 60909)
- In OSPE-Netzen: IeF = ICE (kapazitiver Erdschlussstrom), unabhängig vom Fehlerort auf der Leitung
- ICE wächst mit Netznominalspannung und Netzgröße (Erdkapazitäten proportional zur Leitungslänge)

**Vorteile OSPE:**
- Bei stehendem Erdschluss bleiben Leiter-Leiter-Spannungen erhalten; Ortsnetztransformator mit Dreieckschaltung auf OS-Seite kann NS-Netz weiter speisen — keine Versorgungsunterbrechung
- Lichtbogenfehler in Luft verlöschen bis zur Löschgrenze von selbst (Erdschlusswischer ohne große Auswirkungen)
- Geringe Anforderungen an Erdungsanlagen wegen kleiner Gefährdungsspannungen

**Nachteile OSPE:**
- Erhöhte Leiter-Erd-Spannungen gesunder Leiter → Risiko für Folgefehler (zweipoliger Erdschluss)
- Fehlerbehaftetes Betriebsmittel muss schnell lokalisiert und getrennt werden
- Fehlerortung bei kleinen Fehlerströmen schwierig
- Beschränkung auf kleine Netze im MS-Bereich: Kabelzubau erreicht schnell Löschgrenze
- Rückzündungsgefahr bei kapazitivem Erdschlussstrom (beim Stromnulldurchgang liegt maximale Spannung an) → intermittierende Erdschlüsse mit hohen Spannungsbeanspruchungen
- Erdschlussbetrieb wegen möglicher Personengefährdung zeitlich begrenzt

#### Netze mit Resonanz-Sternpunkterdung — RESPE (Abschnitt 4.4.3, Seiten 345-350)

- Anwendung: 110-kV-Freileitungsnetze, 10/20-kV-Netze
- Kernkomponente: Erdschlusslöschspule (auch: Erdschlussspule, Erdschlussdrossel, Petersen-Spule nach Erfinder Waldemar Petersen)
- Betrieb auch als "gelöschtes Netz", "erdschlusskompensiertes Netz" bezeichnet
- Mehrere Löschspulen möglich: eine regelbar (motorisch verstellbarer Tauchkern), andere fest eingestellt

**Berechnung Erdfehlerstrom mit Löschspule:**
- Parallelschwingkreis im Nullsystem: Blindwiderstand 3·XD der Löschspule parallel zu Erdkapazität CE
- Parallelkreis-Blindwiderstand: X0 = (1/ωCE · 3XD) / (−1/ωCE + 3XD)
- Erdfehlerstrom: IeF = √3 · UbN / (j·X0)
- Resonanzbedingung: 3·XD = 1/(ω·CE) → X0 → ∞ → IeF = 0 (vollständige Löschung)
- Erdkapazität CE unabhängig vom Fehlerort, ändert sich mit Leitungslänge, Netzgröße und Schaltzustand
- Bei perfekter Abstimmung: IeF = ID + ICE = 0; Spule führt Strom ID = ICE ≈ 1,1 · √3 · UnN · ω · CE

**Thermische Grenzen:**
- Erdschlusslöschspulen haben Dauerstromgrenzen
- Maximal 1 bis 2 Stunden Erdschlussbetrieb; danach Abschaltung erforderlich

**Kurzzeitige niederohmige Sternpunkterdung (KNOSPE):**
- Auch als Kurzerdung (KE) bezeichnet
- Aktivierung nach etwa 10 bis 15 s nach Erdschlusseintritt (wenn selbstheilender Charakter nicht mehr zu erwarten)
- Aktivierungszeit meist unterhalb Auslösezeit des MS-Netzschutzes → Schutz nur angeregt (dient Fehlerortung)
- Bei längerer KNOSPE-Aktivierungszeit: selektive Abschaltung

**Erdschluss-Reststrom IRES:**
- Vollständige Löschung gelingt in der Praxis nicht
- Ursachen: (1) Wirkwiderstände im Nullsystem nicht vernachlässigbar; (2) Oberschwingungsüberlagerungen; (3) Verstimmung der Löschspule
- Erfahrungswert: IRES ≈ 0,1 · ICE
- Lichtbogen-Löschgrenzen nach DIN VDE 0228-2: 10–20 kV-Freileitungsnetze: 60 A; 110-kV-Ebene: 130 A

**Vorteile RESPE:**
- Alle Vorteile von OSPE-Netzen (Weiterversorgung, Selbstheilung)
- Gelöschte Netze erheblich größer als isolierte Sternpunktnetze
- Erdschluss-Reststrom ohmsch-induktiv bei leichter Überkompensation → geringere Rückzündungsgefahr

**Nachteile RESPE:**
- Risiko eines zweiten Erdschlusses (Doppelerdschluss)
- Rückzündungsgefahr bei intermittierenden Erdschlüssen
- Fehlerortung schwierig
- Netzgröße durch Reststrom begrenzt → Netztrennung manchmal nötig
- Investitionskosten für Erdschlusslöschspulen
- In weiträumigen Verteilnetzen zunehmende Dauererdschlüsse → steigende Doppelerdschluss-Gefahr → Vorteile zunehmend in Frage gestellt

#### Netze mit niederohmiger Sternpunkterdung — NOSPE (Abschnitt 4.4.4, Seiten 350-351)

- Auch "wirksam geerdetes Netz" genannt
- In allen Spannungsebenen vorhanden:
  - NS-Ebene (TT- und TN-Systeme): Sternpunkte direkt geerdet
  - MS-Bereich: manche Netze
  - Über 125 kV bei hohem Kabelanteil: niederohmige Impedanz
  - Ab 220 kV Freileitungsnetze: immer direkt geerdet
- Ziel: Verringerung zeitweiliger Überspannungen bei Erdfehler
- Erdfehlerstrom: einpoliger Anfangs-Kurzschlusswechselstrom I''k1 (kann Größenordnung von I''k3 erreichen)
- In Freileitungsnetzen: Erdkurzschlussstrom bis 80 kA möglich → schnellstmögliche Abschaltung erforderlich

**Berechnung Erdfehlerstrom bei NOSPE:**
- Erdkapazitäten vernachlässigbar (Fehlerstromkreis schließt sich über niederohmig geerdete Sternpunkte der Transformatoren)
- Leitungs- und Transformatorreaktanzen bestimmen Fehlerstromgröße

**Erdfehlerfaktor δE:**
- Beschreibt Spannungsanhebung gesunder Leiter bei Erdfehler für Isolationskoordination
- δE = UFLE / (UbF / √3)
  - UFLE: Effektivwert der höchsten betriebsfrequenten Leiter-Erd-Spannung eines gesunden Leiters an der Fehlerstelle
- Falls X0 < X1: Spannungsabsenkung statt Anhebung möglich
- Betriebsspannung UbN wird mit 10 % Sicherheitsaufschlag auf UnN abgeschätzt (konsistent mit EN 60909)
