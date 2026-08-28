# Grundladen der elektrischen Energietechnik — Teil 4
> Quelle: Grundladen der elektrischen Energietechnik (buecher) · Seiten 161-200.

Dieser Teil des Lehrbuchs behandelt den Abschluss von Kapitel 2 (Elektrische Maschinen) mit dem Schwerpunkt Drehstrom-Asynchronmaschinen (Abschnitt 2.2) und Drehstrom-Synchronmaschinen (Abschnitt 2.3), sowie den Beginn von Kapitel 3 (Elektrische Anlagen und Betriebsmittel) mit Grundlagen zu Netzbetreibern, Drehstrom- vs. Gleichstrom-Übertragung und den Grundzügen der Hochspannungs-Gleichstrom-Übertragung (HGÜ/HVDC).

## Inhalt

### 2.2 Drehstrom-Asynchronmaschinen (DAM) — Aufbau

#### Stator und Rotor — Grundstruktur
- Feststehender Teil: Ständer (Stator); drehender Teil: Läufer (Rotor)
- Blechpakete bei Ständer und Läufer aus Blechen mit 0,3 bis 0,5 mm Dicke, gegeneinander elektrisch isoliert → reduziert Wirbelstromverluste
- Als Anker bezeichnet man den Maschinenteil, in dem Spannungen induziert werden; bei der Asynchronmaschine ist das der Rotor

#### Läufer-Typen
Zwei grundlegende Läuferausführungen:

**Schleifringläufer:**
- Dreistrangige Kupferwicklung in den Nuten, Sternschaltung
- Strangenden K, L, M werden über Schleifringe zum Klemmenkasten geführt
- Ermöglicht Zuschalten von Anlasswiderständen oder Wechselrichtern in den Läuferkreis

**Kurzschlussläufer (Käfigläufer):**
- Kupfer- oder Leitbronzestäbe in den Nuten, an den Enden durch Kurzschlussringe verbunden
- Alternativ: Druckgusskäfige aus Aluminium in verschiedenen Formen, ebenfalls mit Kurzschlussringen auf beiden Seiten
- Kupfer hat bessere elektrische Leitfähigkeit als Aluminium → geringere Verluste, höherer Wirkungsgrad, aber höherer Preis und aufwendigere Fertigung (höhere Schmelztemperatur)
- Geometrie und Material des Käfigläufers beeinflussen Drehmomenten-Drehzahl-Verhalten und Anlaufmomente
- Schrägstellung der Längsnuten reduziert Oberschwingungseinflüsse auf das Drehmoment

**Käfigstab-Ausführungsformen:**
- Rundstab (Kupfer)
- Hochstab
- Keilstab
- Ausgespritzte Nut
- Doppelstäbe (niedriger Widerstand) / Einzelstäbe (hoher Widerstand)

#### Stator
- Dreiphasige Ständerwicklung aus Kupfer in Längsnuten des Ständerblechpakets
- Drei Stränge U, V, W — Spulenachsen räumlich um je 120° versetzt
- Anschlusspunkte U1, U2, V1, V2, W1, W2 am Klemmenkasten
- Verschaltbar zu Stern- oder Dreieckschaltung

### 2.2.2 Wirkungsweise und Betriebsverhalten

#### Drehfeld
- Nach Einschalten fließen in den drei Strängen phasenverschobene Wechselströme (120° Phasenversatz)
- Jeder Strangstrom erzeugt ein magnetisches Wechselfeld; die drei Wechselfelder überlagern sich bei räumlicher Verdrehung von ±120° zum gemeinsamen rotierenden Drehfeld
- Das Drehfeld dreht sich mit der Netzfrequenz; Drehsinn lässt sich durch Tausch zweier beliebiger Anschlüsse umkehren (Rechts-/Linkslauf)
- Bei Kleinmaschinen mit Wechselstrom: zwei Spulen mit 90°-Phasenversatz und 90° räumlicher Verdrehung erzeugen ebenfalls ein Drehfeld

#### Polpaarzahl
- Magnetischer Dipol hat Nord- und Südpol; Anzahl der magnetischen Dipole = Polpaarzahl p
- p = 1: zweipolige Maschine, genau ein Nord- und Südpol im Luftspalt; Drehfeld bei 50 Hz dreht mit 3000 min⁻¹
- p = 2: vierpolige Maschine durch sechs Ständerstränge (je zwei in Reihe geschaltet); Drehfeld macht je Wechselstromperiode nur eine halbe Umdrehung, dreht mit 1500 min⁻¹ bei 50 Hz

**Tabelle: Synchrone Drehfrequenz fs und Drehzahl ns in Abhängigkeit von Polpaarzahl p**

| p | fs bei f1=50 Hz [Hz] | ns bei f1=50 Hz [min⁻¹] | fs bei f1=60 Hz [Hz] | ns bei f1=60 Hz [min⁻¹] |
|---|---|---|---|---|
| 1 | 50 | 3000 | 60 | 3600 |
| 2 | 25 | 1500 | 30 | 1800 |
| 3 | 16,67 | 1000 | 20 | 1200 |
| 4 | 12,5 | 750 | 15 | 900 |

- Allgemeine Formel: fs = f1 / p
- Diese Drehzahlen entsprechen auch den Rotordrehzahlen von Drehstrom-Synchrongeneratoren

#### Schlupf und Kennlinie
- Im Stillstand (n = 0) wird im ruhenden Läufer eine Spannung induziert → Läuferströme → Lorentzkräfte auf Längsstäbe → Antriebsdrehmoment
- Im Synchronlauf (n = ns) keine Induktion, kein Drehmoment → Läufer muss stets langsamer als das Drehfeld drehen (asynchron) → daher Name Asynchronmotor / englisch: Induction Motor
- Schlupf s = (ns − n) / ns; Einheit: 1 = 100 %
  - s = 1 im Stillstand; s = 0 bei Synchronlauf
  - Im Normalbetrieb (Leerlauf bis Volllast): s ≈ 3 bis 5 %
- Drehmomenten-Drehzahl-Kennlinie (M-n-Kennlinie):
  - Anfahrmoment Ma beim Anlauf
  - Kippmoment Mk (Maximum der Kennlinie)
  - Stabiler Arbeitsbereich nur im abfallenden Teil der Kurve
  - Generatorbetrieb möglich (n > ns)

### 2.2.3 Anlaufmethoden

- Anlaufströme Ian können das 5- bis 7-fache des Bemessungsstroms Ir erreichen (Ian/Ir ≈ 5 … 7)
- Hohe Anlaufströme verursachen kurzzeitige Spannungsabsenkungen im öffentlichen Netz → Störungen/Ausfälle möglich
- Verteilnetzbetreiber fordern in den Technischen Anschlussbedingungen (TAB) Anlaufverfahren

**Direktes Einschalten** ist zulässig wenn:
- Motor-Scheinleistung unter 5,2 kVA, oder
- Anlaufstrom überschreitet 60 A nicht (auch bei höherer Scheinleistung)

**Stern-Dreieck-Anlauf:**
- Einfachste Alternative wenn direktes Einschalten nicht erlaubt
- Reduziert Anlaufstrom durch Stern-Anlauf, Umschaltung in Dreieck nach Hochlauf

**Sanftanlauf (Softstarter):**
- Begrenzt Einschaltströme per Phasenanschnitt der Wechselspannung
- Besteht aus Leistungselektronik-Thyristorschalter

**Frequenzumrichter:**
- Ermöglicht ebenfalls Sanftanlauf
- Hauptanwendung ist jedoch die Drehzahlstellung

**Schaltungskomponenten (laut Abb. 2.46):**
- F1 = Absicherung (Kurzschluss- und Leitungsschutz)
- Q1 = Schalten (Leistungsschütz, Motorschütz)
- F2 = Motorschutz (thermische Überlast, Motorschutzrelais)
- Q2 = Softstarter
- T1 = Frequenzumrichter
- M1 = Drehstrom-Asynchronmotor

### 2.2.4 Drehzahlstellung

Aus der Schlupf-Beziehung folgt: n = (f1 / p) × (1 − s)

Drei Stellschrauben zur Drehzahlanpassung:
1. Netzfrequenz f1
2. Polpaarzahl p
3. Schlupf s (= indirekt Spannung)

#### Läuferwiderstände beim Schleifringläufer
- Widerstände Rv im Läuferkreis, stufenweise oder kontinuierlich zuschaltbar
- Ermöglicht Anlauf mit hohem Drehmoment aus dem Stillstand
- Nachteil: weichere Kennlinien, erhöhte Verluste in den Widerständen

#### Läuferspannungssteuerung mit Umrichter
- Verlustarme Umrichter im Läuferkreis; aufgenommene Drehfeldleistung sPδ wird nahezu vollständig ins Netz zurückgespeist
- Gegenspannung im Läuferkreis reduziert Läuferströme und damit Drehmoment
- Kennlinien behalten gleiche Form wie natürliche Kennlinie, werden parallel verschoben → kontinuierliche Arbeitspunktverstellung

#### Polumschaltung (historisch / Dahlander-Schaltung)
- Vor Leistungshalbleitern die einzige Möglichkeit für Käfigläufer
- Ständerwicklungen in Teilwicklungen aufgeteilt (Dahlander-Schaltungen)
- Durch Umschalten wird Polpaarzahl geändert → diskrete Drehzahlstufen
- Nur stufenweise Verstellung möglich
- Hoher Fertigungsaufwand, teure Motoren, schwierige Reparaturen → heute durch Umrichter ersetzt

#### U-f-Steuerung mit Wechselstromumrichter (VFD)
- Umrichter (AC/AC-Konverter, Variable Frequency Drive) zwischen Netz und Motor
- Kann Spannung U1 und Frequenz f1 unabhängig einstellen
- **Ankerstellbereich** (f1 ≤ 50 Hz): U1/f1 konstant halten — sonst bei sinkender Frequenz Stromanstieg auf I1 ≈ U1 / (√3 · 2πf1 · L)
  - Halbierung f1 auf 25 Hz bei konstanter Spannung verdoppelt den Strom → Überlastung
  - Spannungsfrequenzsteuerung: Spannung proportional zur Frequenz verringern
- **Feldstellbereich** (f1 ≥ 50 Hz): Spannung bleibt bei Bemessungswert; Frequenz steigt → Strom sinkt → abgegebenes Drehmoment sinkt; Kennlinienverschiebung schwieriger, irgendwann kein stabiler Betrieb mehr

**Aufbau des Wechselstromumrichters (drei Teile):**
1. Diodengleichrichter: richtet Netzspannung gleich, zieht impulsförmige (nicht sinusförmige) Netzströme → enthält Oberschwingungen
2. Zwischenkreis (Kondensator)
3. Pulswechselrichter: wandelt Gleichspannung ud in sinusbewertete pulsweitenmodulierte Rechteckimpulse um

- Motorinduktivitäten glätten den Strom → annähernd sinusförmig, verbleibende Welligkeit Δi kann mechanische Resonanzen und Störgeräusche erzeugen
- Entstörbeschaltungen: Netzfilter (LC, vorgeschaltet) und Motorfilter (LC, nachgeschaltet) → nahezu sinusförmige Strom-/Spannungsverläufe, minimale Motorgeräusche
- Bei Bedarf können Netzrückwirkungen durch vorgeschaltete LC-Filter gemildert werden

---

### 2.3 Drehstrom-Synchronmaschinen (DSM)

#### Einordnung und Bedeutung
- Als Motor: konstante Drehfrequenz, z.B. in Uhren, Phonogeräten; durch Frequenzumrichter auch als drehzahlregelbarer Antrieb (Servomotoren bis Großleistungen)
- Als Generator: seit über 100 Jahren dominante Rolle bei der Stromerzeugung; überwiegender Teil der elektrischen Energie wird mit Drehstrom-Synchrongeneratoren (DSG) erzeugt

**Typische Kenndaten großer DSG:**
- Zweipolige Generatoren bis ca. 1200 MVA Scheinleistung
- Vierpolige Generatoren bis ca. 1700 MVA
- Bemessungsspannungen bis 27 kV
- Bemessungsströme bis ca. 26 kA

**Beispiel — Typschild Braunkohlekraftwerk Niederaußem:**

| Kenngröße | Wert |
|---|---|
| Nennleistung | 1 223 000 kVA |
| Nennspannung | 27 000 V |
| Nennstrom | 26 152 A |
| Ständergewicht | 440 t |
| Läufergewicht | 102 t |
| Kühlsystem | H2O/H2-Kühlung |

#### Magnetfelderzeugung (Erregung)
- Kleine Maschinen: Permanentmagnete
- Große Kraftwerksgeneratoren: Erregerspulen mit Gleichströmen bis ca. 10 kA (Erregerströme)
- Erregerleistungen für zweipolige Turbogeneratoren: ca. 3 kW bei 100 kVA bis 4000 kW bei 1000-MVA-Generator

**Maschinentypen nach Pollage:**
- Innenpolmaschine: Erregerwicklung im rotierenden Läufer; dominanter Typ in Kraftwerken
- Außenpolmaschine: Gleichstromwicklung im feststehenden Gehäuse; Einsatz im Erregersystem von Kraftwerksgeneratoren

**Läufer-Konstruktionsformen:**
- Vollpolmaschine (Turboläufer): Massiver Stahlwalzenläufer mit gefrästen Nuten, konzentrisch aufgeteilte Erregerwicklung; Polpaarzahl p = 1 oder 2; schnell drehend; horizontal gelagert; angetrieben durch Gas- oder Dampfturbinen; Masse bis ca. 100 t
- Schenkelpolmaschine: Einzeln ausgeprägte, bewickelte Pole; höhere Polpaarzahl → langsamer drehend; Wasserkraftwerke bis zu 100 magnetischen Polen; vertikale Welle, Turbine unterhalb des Generators

### 2.3.1 Aufbau des DSG

#### Läufer (Induktor)
- Großmaschinen: kurzgeschlossene Dämpferwicklungen im Läufer, um mechanische Pendeldrehmomente und subsynchrone Schwingungen zu dämpfen
- Turbosätze: Dämpferwicklungen in den Nuten der Erregerwicklung
- Schenkelpolmaschinen: Dämpferwicklungen in gesonderten Dämpfernuten der Polschuhe

#### Stator (Ständer/Anker)
- Aufbau aus Segmenten geschichteter Eisenblechpakete mit schmaler Hysteresekurve → reduziert Eisenverluste; Massen bis ca. 440 t
- Bei hohen Ständerströmen: gegeneinander isolierte Teilleiter, längs der horizontalen Drehachse verdrillt → Roebelstäbe; sorgen für gleichmäßige Stromverteilung in den Nuten

**Verschaltung des Stators:**
- Fast ausschließlich Sternschaltung ohne Neutralleiter aus drei Gründen:
  1. Sternschaltung hat besseres Oberschwingungsverhalten (Dreieckschaltung hätte Kreisströme/Dauerkurzschlussströme)
  2. Sternpunkt bleibt isoliert — Neutralleiter würde gleichphasige Belastungsströme erzeugen, die nur Verluste, aber keinen Beitrag zum Drehfeld bringen
  3. Schutzmaßnahmen in Sternschaltung zweckmäßiger
- Im Rahmen des Ständererdschlussschutzes kann Sternpunkt über hochohmige Wandlerwicklung geerdet sein

#### Erregersystem
- Zwei Typen vorgestellt:

**Statische Erregereinrichtung (Innenpol-Drehstrom-Erregergenerator mit Stromrichter):**
- Feststehende Hauptkomponenten (daher "statisch")
- Stromrichter aus netzgeführten Thyristoren oder selbstgeführten IGBTs
- Elektrische Leistung vom dreiphasigen Erregertransformator
- Erregerstromübertragung via Kohlebürsten und Schleifringe (Wartung im Betrieb möglich)
- Vorteil: hohe Regeldynamik für Spannungsregelung
- Nachteile: Wartungskosten, Risiko Bürstenfeuer → nicht im explosionsgeschützten Bereich einsetzbar

**Bürstenlose Erregereinrichtung (Außenpol-Drehstrom-Erregergenerator mit rotierenden Gleichrichter):**
- Erregerstrom kontaktlos über Wellengenerator auf die Welle gebracht
- Wellengenerator ist spezielle DSM mit Außenpol; auf der Welle rotieren drei in Stern verschaltete Drehstromwicklungen, deren Wechselströme mit Thyristoren gleichgerichtet werden
- Vorteil: kein Bürstenunterhalt, einsetzbar im explosionsgeschützten Bereich
- Nachteil: träge Spannungsregelung
- Einschränkung: nur für hohe Drehzahlen geeignet → in Wasserkraftwerken nicht verwendbar (dort nur statische Erregersysteme)

### 2.3.2 Stationärer Betrieb des DSG

#### Polradspannung und Leerlaufkennlinie
- Rotierendes Erregerfeld induziert in den sterngeschalteten Ständerwicklungen drei Wechselspannungen
- Polradspannung Up: Effektivwert der induzierten Spannung als Dreiecks-(Leiter-Leiter-)Größe, direkt an den Klemmen messbar (daher Name: Läufer = "Polrad")
- Sterngröße: synchrone Spannung E = Up / √3 (in der Literatur gebräuchlich, hier zur Vermeidung von Verwechslung mit Feldstärke-Betrag nicht weiterverwendet)

**Leerlaufkennlinie U0p(If):**
- Entspricht der Magnetisierungskennlinie der Maschine
- Beginnt wegen remanenten Magnetflusses meist nicht bei Null (Remanenzspannung UR = wenige Prozent der Bemessungsspannung)
- Bei kleinen Erregerströmen linearer Verlauf auf der Luftspaltgeraden
- Mit zunehmender Eisensättigung flacht die Kennlinie ab
- Auslegung: Bemessungsspannung liegt im Knie der Kennlinie

#### Ankerrückwirkung und stationäres Ersatzschaltbild
- Unter Belastung fließen phasenverschobene Wechselströme in den Statorwicklungen → erzeugen gemeinsames Drehfeld
- Nach dem Lenzschen Prinzip ist dieses Statordrehfeld dem Läuferdrehfeld entgegenwirkend → schwächt dieses → Klemmenspannung sinkt gegenüber Leerlaufspannung = Ankerrückwirkung
- Im stationären Ersatzschaltbild: interner Spannungsfall durch synchrone Reaktanz Xd modelliert, zusätzlich ohmscher Widerstand Ra der Statorwicklungen

  ΔU = (Ra + jXd) · I

- Für Vollpolmaschinen (zweipolig): einphasiges Ersatzschaltbild mit Ra und Xd vollständig gültig
- Für Schenkelpolmaschinen: zusätzlich synchrone Querreaktanz Xq erforderlich (nicht näher behandelt)

**Dimensionslose synchrone Reaktanz xd:**
- xd = Xd · Ir / (Ur / √3); Einheit: 1 = 100 %
- Typischer Bereich: 120 % ≤ xd ≤ 300 %
- Da xd > 1, ist im Kraftwerk eine Spannungs-Blindleistungs-Regelung mit dem Erregersystem unbedingt erforderlich

#### Betrieb am starren Netz

**Grundannahme:** Netzspannung UN am Anschlusspunkt konstant (starres Netz); Ra wird vernachlässigt; nur Xd im Ersatzschaltbild

**Lastwinkel (Polradwinkel) ϑ:**
- Phasendifferenz zwischen Polradspannung Up und Netzspannung UN
- Räumlich/mechanisch: Rotor dreht um ϑ/p gegenüber Lage bei P = 0

**Wirkleistung des Generators:**

  P = (Up · UN / Xd) · sin ϑ

**Bremsmoment des Generators:**

  MG = (Up · UN / (ωmech · Xd)) · sin ϑ

- Maximales Drehmoment bei ϑmax = 90° → Kippmoment Mk
- ϑmax = Stabilitätsgrenze: bei Überschreitung gerät Läufer außer Tritt → schwere Störung oder Totalschaden
- Im Betrieb immer sicherer Abstand unterhalb ϑmax

**Übersteuerter / Untersteuerter Betrieb:**
- Übererregter Betrieb (Up > UN): Generator gibt Wirkleistung und induktive Blindleistung ab → wirkt wie Leistungskondensator; Normalzustand bei Vollast
- Untererregter Betrieb: selten; tritt auf bei starker Windkrafteinspeisung in ländlichen Küstenregionen oder nachts bei schwach belasteten Kabelnetzen

**Blindleistung-Vorzeichenkonvention:**

| Betriebszustand | Erzeugerzählpfeilsystem (EZS) | Verbraucherzählpfeilsystem (VZS) | Beispiel |
|---|---|---|---|
| übererregt | Q > 0 | Q < 0 | Kondensator |
| untererregt | Q < 0 | Q > 0 | Spule |

**Blindleistung aus Zeigerdiagramm:**
- Up · UN / Xd · cos ϑ = UN² / Xd + √3 · UN · I · sin φ = QG + Q
- QG = UN² / Xd: Eigenbedarf des Generators (benötigt selbst induktive Blindleistung)
- Q = √3 · UN · I · sin φ: ans Netz gelieferte Blindleistung

**Leistungsdreieck (Schein-, Wirk-, Blindleistung netto):**
- S² = P² + Q² = (√3 · UN · I)²
- Aus quadratischer Addition von P und (QG + Q): (Up · UN / Xd)² = P² + (QG + Q)²

**Phasenschieberbetrieb:**
- Generator gibt keine Wirkleistung, nur Blindleistung ab
- Anwendung: Systemdienstleistung zur Spannungssteuerung an Kraftwerksstandorten (z.B. Pumpspeicherwerke, Druckluftspeicher)
- Praxisbeispiel: Nach Stilllegung Kernkraftwerk Biblis, Block A (1225 MW): Generator von Turbine getrennt, betrieb als Phasenschieber mit Blindleistung im Bereich −400 Mvar bis +900 Mvar

#### Leistungsdiagramm und Betriebsgrenzen

Begrenzungen durch mehrere Faktoren:
- **Dampfturbine:** Schwachlast PsT (Minimum) und Bemessungsleistung PrT (Maximum Wirkleistung)
- **Generator:** Maximal zulässiger Polradwinkel ϑzulG (Stabilitätsgrenze), Bemessungsscheinleistung SrG (Stromwärmeverluste Stator bei Bemessungsstrom IrG), maximal zulässiger Erregerstrom Imaxf (Stromwärmeverluste Erregersystem)

**Wirkleistungsregelung:**
- Wirkleistung P nur über antreibendes Turbinendrehmoment veränderbar
- Festdruckbetrieb: Ventil regelt Dampf, Dampfparameter konstant
- Gleitdruckbetrieb: Ventile bleiben offen, Leistungssteuerung über Massendurchsatz der Kohlemühlen; Frequenz-Wirkleistungs-Regelung arbeitet mit Kessellastgeber zusammen, dem ca. 150 Regelkreise untergeordnet sind
- Modifizierter Gleitdruckbetrieb: Kombination aus beiden

**Blindleistungsregelung:**
- Bei Wirkleistungsänderung mit konstantem Q: Erregerstrom If muss synchron angepasst werden (da Up ~ If)

**Kraftwerksleittechnik:**
- Betrieb der Kraftwerksblöcke vollständig automatisiert
- Regelt Wirk- und Blindleistung am Anschlusspunkt
- Steuert An-/Abfahren inklusive Generatorsynchronisation
- Verarbeitet Meldungen/Alarme von Überstrom-/Überspannungsschutz und Kessel
- Ermöglicht Energiemanagementfunktionen zur Wirkungsgradsteigerung

---

### 3 Elektrische Anlagen und Betriebsmittel — Einführung

#### Liberalisierung und Netzbetreiberstruktur
- Liberalisierung der Elektrizitätswirtschaft trennte Erzeugung, Transport, Verteilung, Vertrieb und Handel
- Erzeugung, Handel, Vertrieb im Wettbewerb; Netz exklusiv bei Netzbetreibern unter Regulierungsbehörde
- Deutschland: Verbundnetz (HöS-Ebene) auf vier Übertragungsnetzbetreiber (ÜNB/TSO) aufgeteilt:
  - 50Hertz Transmission
  - Amprion
  - TenneT TSO
  - TransnetBW
- Unterlagerte HS-, MS-, NS-Netze: ca. 865 Verteilnetzbetreiber (VNB/DSO)

#### Versorgungszuverlässigkeit — internationaler Vergleich

Durchschnittliche Unterbrechungsdauer (Minuten pro Kunde und Jahr):

| Land | Jahr | Unterbrechungsdauer |
|---|---|---|
| Südkorea | 2018 | 5,4 min |
| Japan | 2018 | 6,0 min |
| Deutschland | 2020 | 10,2 min |
| Niederlande | 2016 | 20,9 min |
| Österreich | 2019 | 25,1 min |
| Italien | — | 37,1 min |
| Frankreich | 2016 | 48,7 min |
| Spanien | 2016 | 51,3 min |
| China | 2018 | 54,0 min |
| Portugal | 2016 | 64,1 min |
| USA | 2019 | 92,0 min |

Quelle: VDE FNN, CEER, e-Control, eia, World Bank

#### Relevante Vorschriften und Normen

| Normen | VDE | Inhalt |
|---|---|---|
| IEC EN 60364 | VDE 0100 | Errichten von Starkstromanlagen, Nennspannungen bis 1000 V |
| IEC EN 61936 | VDE 0101 | Errichten von Starkstromanlagen, Nennspannungen über 1 kV |

#### Historische Entwicklung der Drehstromübertragung
- Erste Drehstromübertragung 1891: Kraftwerk Lauffen am Neckar → Elektrotechnische Ausstellung Frankfurt am Main
- Strecke: 175 km; Spannung: 14 kV; Frequenz: 40 Hz; transportierte Wirkleistung: 140 kW

#### Vorteile von Wechselstrom gegenüber Gleichstrom

**Vorteile Wechselstrom allgemein:**
- Leistungstransformatoren ermöglichen Hochspannung → kleinere Betriebsströme → Stromwärmeverluste R·I² sinken quadratisch mit Strom → kleinere Leiterquerschnitte möglich → Materialkostensenkung
- Wechselstrom lässt sich im Stromnulldurchgang mit Lichtbogenlöschverfahren zuverlässig unterbrechen; hohe Spannungen leichter zu schalten als hohe Ströme; Gleichstromschalten technisch erheblich schwieriger

**Zusätzliche Vorteile Drehstrom gegenüber Einphasen-Wechselstrom:**
- Im symmetrischen Betrieb ist die momentane Gesamtleistung p(t) auf der Drehstromleitung zeitlich konstant; bei Einphasen-Wechselstrom schwingt sie mit doppelter Frequenz → mechanische Belastung von Turbinen/Generatoren und Nachteile für Lasten
- Drehstrom braucht pro Phase nur einen Leiter; Einphasen-Wechselstrom benötigt Hin- und Rückleiter → erhebliche Materialeinsparung bei Stromkreislängen über 1 800 000 km
- Magnetische Drehfelder ermöglichen preisgünstige, robuste DAM mit hohem Wirkungsgrad und konstantem Drehmoment

#### Vorteile von Gleichstrom (DC) gegenüber Wechselstrom

- Auf DC-Leitungen nur Wirkleistungsübertragung → kein Blindleistungshaushalt erforderlich (Blindströme verursachen Stromwärmeverluste)
- DC-Leitungen haben weniger Wirbelstromverluste; Kompensation durch Stromrichter/Transformatoren in Stationen erforderlich
- Radialfeldkabel müssen nicht kompensiert werden
- Betrieb mit sehr hohen Spannungen ohne Stabilitätsprobleme möglich

#### Stromkreislängen in Deutschland (km)

| Spannungsebene | Spannung | 2006 | 2008 | 2022 |
|---|---|---|---|---|
| NS | 0,4 kV | 1 067 100 | 1 131 181 | 1 570 100 |
| MS | 6–60 kV | 493 000 | 506 771 | 530 200 |
| HS | 60–220 kV | 75 200 | 76 946 | 95 200 |
| HöS | ≥220 kV | 36 000 | 35 709 | 36 400 |
| Gesamt | — | 1 671 300 | 1 750 607 | 2 231 900 |

Quellen: VDN Jahresbericht 2006, BDEW Energiemarkt 2023

#### Hochspannungs-Gleichstrom-Übertragung (HGÜ / HVDC)

**Abkürzungen:**
- HGÜ = Hochspannungs-Gleichstrom-Übertragung
- HVDC = High Voltage Direct Current (international)
- UHVDC = Ultra High Voltage Direct Current (Gleichspannungen > 800 kV)

**Drei klassische Anwendungsfelder der HGÜ:**
1. Große Überlandstrecken: Gleichstromleitungen bei extremen Leistungen; keine Alternative zu Freileitungen bei manchen Leitungslängen über 3000 km; bei moderaten Leistungen auch Kabel möglich (witterungsunabhängig, aber teurer)
2. Seeverbindungen: Kabel zwingend erforderlich; HGÜ schon bei kürzeren Leitungslängen nötig, da Drehstromkabel mit hohen kapazitiven Ladeströmen belastet sind; Beispiele: Gleichstromkabel Belgien–Großbritannien (Nemo Link); Offshore-Windparks fast ausnahmslos über DC-Kabel angeschlossen
3. Netzkurzkupplung zwischen asynchronen Verbundnetzen: ermöglicht Wirkleistungsübergabe ohne gegenseitige Beeinflussung der Frequenz-Wirkleistungs-Regelungen

**Topologie:**
- Einzelne Gleichstromleitungen als Punkt-zu-Punkt-Verbindung innerhalb oder zwischen Drehstromnetzen
- Schaltung auf Drehstromseite mit konventionellen Wechselstrom-Leistungsschaltern

**VSC-HVDC-Technik (Voltage Source Converter):**
- Einsatz von IGBT (Insulated-Gate Bipolar Transistor) als Stromrichter
- Wirkleistung über DC-Leitung veränderbar
- An beiden Stationen (Anfang und Ende der DC-Leitung) Blindleistungen unabhängig voneinander einstellbar

**Pilot-Projekte und Zukunft:**
- Erste Pilot-Projekte für DC-Netze gestartet
- Konzept DC-Overlay-Netz: europäische Windparks über überlagerndes DC-Netz verbunden
- DC-Netze benötigen für selektive Abschaltung im Fehlerfall Gleichstrom-Leistungsschalter
