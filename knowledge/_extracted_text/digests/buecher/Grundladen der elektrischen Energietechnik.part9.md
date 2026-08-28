# Grundladen der elektrischen Energietechnik — Teil 9
> Quelle: Grundladen der elektrischen Energietechnik (buecher) · Seiten 361-400.

Dieser Teil behandelt zunächst den Abschluss von Kapitel 4 (Modellierung und Berechnung von Kurzschlussströmen in Drehstromnetzen) und leitet dann in Kapitel 5 (Niederspannungsnetze im Gebäude) über. Im Vordergrund stehen Kurzschlussstromkenngrößen, das vereinfachte Berechnungsverfahren nach EN 60909/DIN EN 60909 (VDE 0102), Maßnahmen zur Beeinflussung von Kurzschlussströmen, numerische Lösungsverfahren sowie der Personenschutz nach DIN VDE 0100 und die Niederspannungs-Schaltgeräte (NH-Sicherungen, Leitungsschutzschalter, FI-Schutzschalter).

## Inhalt

### 4.4 Abschluss: Erdfehler und Sternpunktbehandlung (Seite 361)

- **Erdfehlerfaktor δE** ist das Verhältnis von Leiter-Leiter-Spannung an der Fehlerstelle ohne Fehlerwirkung (Effektivwert betriebsfrequent) zur Spannung unter Betrieb. Maximalwert: δE = √3 ≈ 1,73 in isolierten oder gelöschten Netzen; unterhalb δE = 1,4 gilt wirksame Erdung (niederohmig geerdet); Minimalwert δE = √3/2 ≈ 0,87 bei verschwindender Nullimpedanz.
- **Automatische Wiedereinschaltung (AWE)** in Freileitungsnetzen mit Erdschlusskompensation oder niederohmiger Sternpunkterdung: Freileitung für ca. 500 ms abschalten → Luftstrecke entionisiert → bei Erfolg Ursache (z.B. Blitz, Ast) beseitigt. Zunächst einpolige Abschaltung, bei Misserfolg dreipolige Unterbrechung. Bei Kabeln sollte AWE nicht angewendet werden.
- **Vorteile starre Sternpunkterdung:**
  - Schutz spricht schnell und sicher an
  - Einfache Fehlerortung
  - Selektive Ausschaltung einpoliger Fehler möglich
  - Niedrigere Spannungsbeanspruchung gesunder Leiter und Transformatorsternpunkt als bei isolierten oder Resonanzerdungsnetzen → weniger Isolationsaufwand
  - Spartransformatoren einsetzbar
- **Nachteile starre Sternpunkterdung:**
  - Hohe Kurzschlussströme gefährden Mensch und Tier bis zur Abschaltung; Investitionen in Erdungsanlagen gegen gefährliche Schritt- und Berührungsspannungen erforderlich
  - Hohe Beanspruchung für Leistungsschalter und Betriebsmittel
  - Jeder Kurzschluss erfordert Schalthandlungen
  - EMV-Probleme möglich

### 4.5 Dreipolige Kurzschlussstromberechnung

#### 4.5 Einleitung: Auswirkungen von Kurzschlussströmen (Seiten 362–363)

- Starke mechanische Beanspruchung durch elektromagnetische Kräfte zwischen stromführenden Leitern.
- Explosive Druckerhöhung durch exzessive Lichtbogenerwärmung; thermische und mechanische Beschädigung oder Zerstörung von Anlagen und Personengefährdung möglich.
- Bis zur Fehlerstromabschaltung treten gefährliche Schritt- und Berührungsspannungen auf.
- Automations- und Nachrichtensysteme können elektromagnetisch beeinflusst werden.
- Kurzschlussstromberechnung dient der Auslegung und Auswahl von Betriebsmitteln. Grundlage: vereinfachtes Verfahren nach **IEC 60909 / DIN EN 60909** (früher VDE 0102), basierend auf der Methode der Ersatzspannung an der Kurzschlussstelle.
- Online-Berechnungsverfahren in der Netzführung:
  - **Überlagerungsverfahren:** Dreipoliger Kurzschluss an ausgewähltem Knoten simuliert, aktuelle Knotenspannungen aus State Estimation (SE) oder Dispatcher Power Flow (DPF); Berechnung aller Fehlerströme im Netz; genauer als Planungsbedingungen.
  - **Takahashi-Verfahren:** Dreipoliger Kurzschlussstrom an allen Netzknoten; sehr schneller Algorithmus, liefert nur Strom an der Fehlerstelle. Ermöglicht kontinuierliche/periodische Online-Überwachung des Kurzschlussstromniveaus; Meldung wenn Bemessungsausschaltvermögen eines Leistungsschalters überschritten.

#### 4.5.1 Berechnung vom Anfangs-Kurzschlusswechselstrom (Seiten 363–370)

**Kenngrößen**

- Ausgangspunkt: metallischer Kurzschluss ohne Übergangswiderstände; keine Netztopologieänderungen während Kurzschlussdauer.
- **Zeitverlauf des Kurzschlussstroms ik(t)** wird durch elektromagnetische Ausgleichsvorgänge in Synchrongeneratoren bestimmt.
- **Abklingende Gleichstromkomponente idc(t):** Größe hängt von Eintritts-Zeitpunkt des Kurzschlusses ab; wenn so groß, dass ik(t) keinen Nulldurchgang hat → kritisch, da Leistungsschalter u.U. nicht unterbrechen können.
- **Generatornaher Kurzschluss:** Wechselstromamplitude klingt ab; **Generatorferner Kurzschluss:** Wechselstromamplitude konstant.
- Zielsetzung EN 60909: nicht die Zeitfunktion ik(t), sondern die für Betriebsmittelauslegung relevanten Kurzschlussstromparameter.

**Wichtige Kenngrößen im Überblick:**

- **I''k (Anfangs-Kurzschlusswechselstrom):** Effektivwert der Wechselstromkomponente zum Zeitpunkt t = 0 des Kurzschlussbeginns. Fiktive Größe für stationäre Rechnung.
- **ip (Stoßkurzschlussstrom):** Größter Augenblickswert (Scheitelwert) unmittelbar nach Fehlereintritt; dient mechanischer Auslegung.
- **Ib (Ausschaltwechselstrom):** Effektivwert der Wechselstromkomponente zum Zeitpunkt der Kontakttrennung im Leistungsschalter; bei generatornahem Kurzschluss Ib < I''k.
- **Ith (thermisch gleichwertiger Kurzschlussstrom):** Fiktiver Effektivwert, der über definierten Zeitraum gleiche thermische Wirkung wie tatsächlicher Kurzschlussstrom hat.
- **Ik (Dauerkurzschlussstrom):** Effektivwert nach Abklingen aller Ausgleichsvorgänge; generatornah I''k > Ik; generatorfern I''k = Ik.

**Drei Zeitbereiche beim generatornahen Kurzschluss:**

- **Subtransient:** Reaktanz X''d zugeordnet
- **Transient:** Reaktanz X'd zugeordnet
- **Stationär:** Synchronreaktanz Xd

**Reaktanzen von Synchronmaschinen in % (Tab. 4.13):**

| Reaktanz | Turbogenerator | Schenkelpol mit Dämpferwicklung | Schenkelpol ohne Dämpferwicklung |
|---|---|---|---|
| Anfangsreaktanz x''d | 9 ... 22 | 12 ... 30 | 20 ... 40 |
| Übergangsreaktanz x'd | 14 ... 35 | 20 ... 45 | 20 ... 40 |
| Synchronreaktanz xd | 140 ... 300 | 80 ... 180 | 80 ... 180 |
| Gegenreaktanz x2 | 9 ... 22 | 10 ... 25 | 30 ... 50 |
| Nullreaktanz x0 | 3 ... 10 | 5 ... 20 | 5 ... 25 |

- **Anfangskurzschluss-Wechselstrom-Scheinleistung S''k** (auch Kurzschlussleistung genannt): S''k = √3 · Un · I''k (Gl. 4.102). Hinweis: für Betriebsmittelauswahl (Leistungsschalter) sind ausschließlich Kurzschlussströme maßgebend, nicht die Kurzschlussleistung.

**Richtwerte für Kurzschlussströme und -leistungen (Tab. 4.14):**

| Un / kV | I''k / kA | S''k / GVA |
|---|---|---|
| 10 | 29 | 0,5 |
| 110 | 42 | 8 |
| 220 | 63 | 24 |
| 380 | 80 | 53 |

**Verfahren nach EN 60909 — Methode der Ersatzspannungsquelle**

- Annahmen beim Fehlereintrittszeitpunkt: ungestörter und symmetrischer Betrieb, Netznominalspannung Un an allen Knoten, Netz im Leerlauf (keine Betriebsströme). Vorgeschaltete Leistungsflussrechnung entfällt.
- Vereinfachungen für Betriebsmittel-Ersatzschaltbilder:
  - Freileitungen/Kabel: keine Betriebskapazität Cb und keine Ableitung Gb (vereinfachtes Leitungsersatzbild ohne Querelemente).
  - Transformatoren: Eisenverlustwiderstand RFe und Hauptreaktanz Xh vernachlässigt; Phasendrehungen entfallen; Stufensteller in Mittelstellung.
  - Lasten: vollständig außer Acht gelassen.
- Berechnung über Satz von Thevenin: Spannungsquelle an Fehlerort F einsetzen (Rückwärtseinspeisung); Kurzschlussimpedanz Z''k zusammenfassen:

  I''k = c · Un / (√3 · Z''k)   und   Ik = c · Un / (√3 · Zk)   (Gl. 4.103)

- **Spannungsfaktor c** (dimensionslos): Sicherheitsaufschlag für Vereinfachungen.

**Spannungsfaktoren nach EN 60909 (Tab. 4.15):**

| Nennspannung | cmin | cmax |
|---|---|---|
| Un ≤ 1 kV, Toleranz 6 % | 0,95 | 1,05 |
| Un ≤ 1 kV, Toleranz 10 % | 0,90 | 1,10 |
| 1 kV < Un ≤ 380 kV | 1,00 | 1,10 |

- cmax: Dimensionierung von Schaltgeräten, Leitungen, Sammelschienen.
- cmin: Schutz- und Selektivitätsberechnungen.

**Formeln für verschiedene Fehlerarten — Anfangs-Kurzschlusswechselstrom I''k (Tab. 4.16):**

| Fehlerart | Formel |
|---|---|
| Dreipoliger Kurzschluss (mit/ohne Erdberührung) | I''k3 = c·Un / (√3 · |Z1|) |
| Zweipoliger Kurzschluss ohne Erdberührung | I''k2 = c·Un / |Z1 + Z2| |
| Zweipoliger Kurzschluss mit Erdberührung | I''k2E = √3·c·Un / |Z1 + Z0 + Z0·Z1/Z2| |
| Einpoliger Kurzschluss / Erdfehler | I''k1 = √3·c·Un / |Z1 + Z2 + Z0| |

- Asymmetrische Fehler: Ströme fließen im Mit-, Gegen- und Nullsystem; Kurzschlussimpedanz setzt sich aus Impedanzen aller beteiligten Systeme zusammen. Einpoliger Erdfehler: Mit-, Gegen- und Nullsystem in Reihe geschaltet → Zk1 = Z1 + Z2 + Z0.

**Kurzschlussimpedanzen der Betriebsmittel im Mitsystem (Tab. 4.17):**

| Betriebsmittel | Formeln |
|---|---|
| Netzeinspeisung | ZQ = c·Un/(√3·I''kQ); RQ = 0,1·XQ; XQ = 0,995·ZQ |
| Synchrongenerator (DSG) | RG = 0,05...0,15·XG; XG = x''d·U²rG/SrG; XG = xd·U²rG/SrG |
| Transformator | ZT = uk·U²rT/SrT; RT = uR·U²rT/SrT; XT = √(Z²T − R²T) |
| Drehstromleitung | Rb = R'b·l; Xb = X'b·l |

- Netzeinspeisung: I''kQ am Anschlusspunkt muss bekannt sein.
- Synchrongenerator: Unterscheidung direkte Netzeinspeisung oder über Blocktransformator; mit/ohne Stufenschalter; Asynchrongeneratoren je nach Ausführung mit Kurzschluss- oder Schleifringläufer.
- Transformator: relative Kurzschlussspannung uk und Wirkanteil uR erforderlich (Gl. 2.8).
- Leitungen NS/MS: Wirkwiderstand Rb oft nicht vernachlässigbar, da Rb und Xb in gleicher Größenordnung.
- Nullsystem bei isolierten oder kompensiert geerdeten Netzen: Erdkapazität CE stets berücksichtigen.

**Maßnahmen zur Beeinflussung der Kurzschlussströme**

- Einflussfaktoren: (1) Rotationsenergie in konventionellen Kraftwerken speist Kurzschlussströme (mit Rückgang → Kurzschlussströme sinken); (2) Impedanzen in der Fehlerstrombahn (X''d, Leitungs- und Transformatorimpedanzen).
- Anforderungen: Kurzschlussströme müssen hoch genug für sichere Schutzerkennung, dürfen aber Ausschaltvermögen der Leistungsschalter nicht überschreiten.
- Technische Maßnahmen zur Reduktion:
  - Einführung höherer Spannungsebene: X''d = x''d·U²rG/SrG steigt quadratisch mit Spannung, treibende Spannung nur linear → theoretisch wirksam, aber hohe Investitionskosten und lange Lieferzeiten für Großtransformatoren.
  - Synchrongeneratoren mit hochohmiger X''d: schlechtes Stabilitätsverhalten, kaum praxistauglich.
  - Transformatoren mit hoher relativer Kurzschlussspannung uk: höherer Blindleistungsbedarf und größerer Stufenstellerbereich als Nachteil.
  - Schaltanlagenkonfiguration für Teilnetzbildung im laufenden Betrieb: gängige Praxis.
  - **Kurzschlussstrom-Begrenzungsdrosseln** in der Strombahn (Schaltzeichen beschrieben).
  - HGÜ-Leitung zwischen entkoppelten Teilnetzen: überträgt nur Wirkleistung; Kurzschlussstrom im Übertragungsnetz ist wesentlich Blindstrom → wirkt sich nicht auf das andere Netz aus.

#### 4.5.2 Berechnung abgeleiteter Kurzschlussstromgrößen (Seiten 371–374)

**Dimensionslose Faktoren (Tab. 4.18):**

| Faktor | Bedeutung |
|---|---|
| κ | Stoßfaktor (für Stoßkurzschlussstrom ip) |
| µ | Abklingfaktor (für Ausschaltwechselstrom Ib) |
| λ | Faktor für Dauerkurzschlussstrom Ik |
| m | Faktor für Wärmeeffekt des Gleichstromanteils (für Ith) |
| n | Faktor für Wärmeeffekt des Wechselstromanteils (für Ith) |

**Stoßkurzschlussstrom ip (für mechanische Betriebsmittelauslegung):**

- Einfach gespeister Kurzschluss: ip = κ · √2 · I''k (Gl. 4.104)
- Stoßfaktor: κ = 1,02 + 0,98 · e^(−3·R/X); Bereich 1 < κ ≤ 2.
- Bei R/X = 0: κ = 2 (Maximum). Alternativ aus Diagramm ablesbar.

**Ausschaltwechselstrom Ib (für Dimensionierung der Leistungsschalter):**

- Generatornaher Kurzschluss (einfach gespeist): Ib = µ · I''kG (Gl. 4.106)
- Mindestschaltverzug tmin: kleinstmögliche Zeitspanne zwischen Kurzschlusseintritt und erster mechanischer Kontakttrennung.
- Abklingfaktoren µ in Abhängigkeit von tmin (Tab. 4.19):

| tmin | µ-Formel |
|---|---|
| 0,02 s | µ = 0,84 + 0,26 · e^(−0,26 · I''kG/IrG) |
| 0,05 s | µ = 0,71 + 0,51 · e^(−0,30 · I''kG/IrG) |
| 0,1 s | µ = 0,62 + 0,72 · e^(−0,32 · I''kG/IrG) |
| ≥ 0,25 s | µ = 0,56 + 0,94 · e^(−0,38 · I''kG/IrG) |

- Generatornaher Kurzschluss in vermaschten Netzen oder im Zweifelsfall: µ = 1 setzen.

**Dauerkurzschlussstrom Ik:**

- Wesentlich für Einstellungen des Netzschutzes; bei generatornahem Kurzschluss nur relativ ungenau bestimmbar (Sättigungseinflüsse, Schutzeinrichtungen kaum quantifizierbar).
- Für einzelne Synchronmaschine: obere und untere Grenze nach Gl. 4.107:
  - Ikmax = λmax · IrG
  - Ikmin = λmin · IrG
- λmax und λmin aus Kurvendiagrammen ablesen.

**Thermisch gleichwertiger Kurzschlussstrom Ith:**

- Hohe Kurzschlussströme belasten Betriebsmittel thermisch. Während Kurzschlussdauer Tk muss erzeugte Wärmemenge ΔQ unter zulässigen Werten bleiben.
- Vereinfachte Wärmeberechnung (adiabate Erwärmung): ΔQ = RB · ∫ik²(t)dt ≈ RB · I²th · Tk (Gl. 4.108/4.109).
- Wirbelstromeffekte erst bei Kabelquerschnitten oberhalb 600 mm² zu berücksichtigen.
- Berechnung: Ith = √(m + n) · I''k (Gl. 4.110)
- Faktor m: Wärmeeffekt aperiodischer Gleichstromanteil; abhängig von κ und Tk.
- Faktor n: Wärmeeffekt Wechselstromanteil; abhängig von I''k, Ik und Tk.
- Formeln für m und n aufwendig; alternativ aus Diagrammen.

#### 4.5.3 Numerische Lösung der Differenzialgleichungen (Seiten 374–377)

**Dreipoliger Klemmenkurzschluss am Synchrongenerator**

- Vollständige Spannungsgleichungen der Synchronmaschine basieren auf Parkschen Gleichungen (Park 1929/1933).
- Modell: dreisträngige symmetrisch aufgebaute Synchronmaschine, kurzgeschlossene Dämpferwicklungen durch zwei horizontale Wicklungen in Längs- und Querachse modelliert; konstante Permeabilität des Eisens (Sättigungseffekte vernachlässigt); keine Stromverdrängungseffekte und keine Eisenverluste.
- 6 Spannungsgleichungen in Matrizenschreibweise: [u(t)] = d/dt([L(t)]·[i(t)]) + [R]·[i(t)] (Gl. 4.112)
- Spannungsvektor: [uUY, uVY, uWY, uf, 0, 0]^T; Erregerspannung uf(t) = const während Fehlerdauer.
- Stromvektor: [iUY, iVY, iWY, if, iD, iQ]^T; iD und iQ sind Dämpferwicklungsströme.
- Lineares System von 6 gewöhnlichen Differenzialgleichungen; Teil der Elemente in Matrix [L(t)] periodisch zeitabhängig.
- Fehlerbedingungen dreipoliger Klemmenkurzschluss: iUY + iVY + iWY = 0 und uUV = uVW = uWU = 0.
- Nach 0αβ-Koordinatentransformation der Statorgrößen: fünf Gleichungen (Gl. 4.117).
- Induktivitätsmatrizen: [LLL] für Rotorinduktivitäten (Lff, LDD, LQQ, MfD), [L3P_SS(t)] mit winkelabhängigem Anteil ΔLs und [L3P_SL(t)] mit Stator-Rotor-Gegeninduktivitäten (Mdf, MdD, MqQ).
- Polradwinkel: pθ(t) = ωt + pθ0 = ωt + ϑ + α − π/2; Polpaarzahl p, Lastwinkel ϑ, Schaltwinkel α.
- Vereinfachende Annahme: ω und ϑ ändern sich in ersten Perioden nicht; sonst Bewegungsdifferenzialgleichung J·d²θ/dt² = M mit Massenträgheitsmoment J einbeziehen.
- Numerische Lösung: explizites/implizites Eulerverfahren, Trapezregel oder Runge-Kutta-Verfahren.

**Mehrmaschinenproblem**

- Mehrere Synchrongeneratoren: Modellbildung deutlich aufwendiger.
- Modifiziertes Trapezverfahren (Differenzenleitwertverfahren): im Programm **EMTP (Electromagnetic Transients Program)** von Hermann W. Dommel (1969) implementiert; auch in **NETOMAC (Network Torsion Machine Control)** von Bernd Kulicke (1975).
- EMTP löst Differenzialgleichungen von RLC-Elementen kombiniert mit Parkschen Gleichungen.
- Problematik: Kopplung von Netz und Synchronmaschinen sowie Verschmelzung von Netzmodell und Integrationsalgorithmus; alternative Verfahren konnten sich gegenüber etablierten Programmsystemen nicht durchsetzen.
- Programme zur Netzdynamikberechnung (Tab. 4.20): EMTP® (www.emtp.com), ATP-EMTP (www.emtp.org), PSS®NETOMAC (www.siemens.com).

### 5 Niederspannungsnetze im Gebäude

#### 5.0 Überblick (Seiten 382–383)

- NS-Netze außerhalb der Gebäude liegen in Verantwortung von Verteilnetzbetreibern und sind über Ortsnetzstationen mit dem Mittelspannungsnetz verbunden.
- Ab **Hausanschlusssicherungen im HAK (Hausanschlusskasten)** liegt das Netz in der Obhut des Anschlussnehmers; Zähler bleibt in Hand des Messstellenbetreibers. HAK und Zähler sind verplombt.
- Viele Industrieunternehmen oder große Liegenschaften direkt am MS-Netz angebunden; betreiben Transformatoren und NS-Netze eigenständig.
- Kapitelinhalt: NS-Verteilungen in der Gebäudetechnik **unterhalb des HAK**, Fokus auf Schutzmaßnahmen:
  - Schutz gegen gefährliche Körperströme (Personenschutz)
  - Schutz gegen thermische Einflüsse (Brandschutz)
- Normgrundlage: **DIN VDE 0100 "Errichten von Niederspannungsanlagen"**.

**Gliederung DIN VDE 0100 (Überblick):**

| Gruppe | Inhalt |
|---|---|
| 100 | Anwendungsbereich, allgemeine Anforderungen, Begriffe |
| 200 | Begriffe (elektrische Anlagen von Gebäuden) |
| 300 | Allgemeine Angaben zur Planung elektrischer Anlagen (Leistungsbedarf, Gleichzeitigkeitsfaktor, Stromerzeugung, Netzformen, Stromkreisaufteilung, äußere Einflüsse, Verträglichkeit, Wartbarkeit) |
| 400 | Schutzmaßnahmen (Teil 410: Schutz gegen elektr. Schlag; Teil 420: Schutz gegen thermische Auswirkungen; Teil 430: Überstromschutz; Teil 442: Überspannungsschutz; Teil 450: Unterspannungsschutz; Teil 460: Trennen und Schalten; Teil 470/480: Anwendung/Auswahl Schutzmaßnahmen) |
| 500 | Auswahl und Errichtung elektrischer Betriebsmittel (Teil 510: allg. Bestimmungen; Teil 520: Kabel-/Leitungsanlagen; Teil 530: Schalt-/Steuergeräte; Teil 540: Erdungsanlagen, Schutzleiter, Potenzialausgleich; Teil 550: Steckvorrichtungen, Schalter, Installationsgeräte; Teil 560: Einrichtungen für Sicherheitszwecke) |
| 600 | Prüfungen / Erstprüfung (Besichtigen, Erproben/Messen, Schutzleiter/Potenzialausgleich, sichere Trennung, Isolationswiderstand, automatische Abschaltung, Spannungspolarität, Spannungsfestigkeit, Funktionsprüfungen) |
| 700 | Betriebsstätten besonderer Art (Teil 701: Räume mit Badewanne/Dusche; Teil 702: Schwimmbecken; Teil 703: Räume mit Saunaheizungen; Teil 715: Kleinspannungsbeleuchtungsanlagen; weitere ...) |

### 5.1 Schutz gegen elektrischen Schlag (Seiten 375–381)

- **Elektrischer Schlag:** physiologische Wirkung von elektrischem Strom durch Mensch oder Tier; pathophysiologische Effekte sollen möglichst nicht auftreten.
- **Körperschluss:** Isolationsfehler zwischen leitfähigem Gehäuse (Körper) und Leiter des Betriebsstromkreises → Fehlerstrom IF fließt. Größe abhängig von Schleifenimpedanz (Zusammenfassung aller Impedanzen in der Fehlerstrom-Strombahn).
- Berührungsspannung unterschieden:
  - **Prospektive/unbeeinflusste Berührungsspannung UPT:** Maximalwert ohne Körperkontakt.
  - **Berührungsspannung UT über den Körper:** Körperwiderstand parallel zu anderen → UT < UPT.

**Maximale dauerhaft zulässige Berührungsspannungen nach DIN IEC TS 60479-1 (Tab. 5.1):**

| Strom | Erwachsener | Kind oder Tier |
|---|---|---|
| DC | 120 V | 60 V |
| AC | 50 V | 25 V |

**Kategorien des Berührens:**

- **Direktes Berühren:** Kontakt mit aktiven Teilen (Leiter oder leitfähige Bereiche, die im üblichen Betrieb unter Spannung stehen; Neutralleiter eingeschlossen, nicht aber PEN, PEL, PEM). Schutzmaßnahmen → **Basisschutzvorkehrung** (= Basisschutz, Schutz gegen direktes Berühren, Schutz gegen elektr. Schlag unter normalen Bedingungen).
- **Indirektes Berühren:** Kontakt mit metallischen Körpern, die durch Fehler unter Spannung stehen. Schutzmaßnahmen → **Fehlerschutzvorkehrung** (= Fehlerschutz, Schutz bei indirektem Berühren, Schutz gegen elektr. Schlag unter Fehlerbedingungen).

#### 5.1.1 Basis- und Fehlerschutzvorkehrungen (Seiten 377–380)

**Basisschutz nach DIN VDE 0100-410:**

- Unterscheidung normale Bedingungen und besondere Bedingungen (letztere nur für Elektrofachkräfte oder elektrotechnisch unterwiesene Personen).
- **Basisisolierung:** verhindert Berühren von Leitern/leitfähigen Teilen, die im Betrieb unter Spannung stehen. Darf nur durch Zerstörung entfernt werden.
- **Umhüllungen und Abdeckungen** müssen bestimmte IP-Schutzarten erfüllen.
- Bei besonderen Bedingungen auch Hindernisse oder Anordnung außerhalb des Handbereichs ausreichend.
- **Hindernisse** schützen nur vor unbeabsichtigtem Berühren, nicht vor absichtlichem Kontakt.
- **Außerhalb des Handbereichs:** leitfähige Teile mit unterschiedlichem Potenzial müssen mindestens **2,5 m** voneinander angeordnet werden.

**Fehlerschutzvorkehrungen:**

- Automatische Abschaltung der Stromversorgung mit Potenzialausgleich
- Kleinspannungen (ELV)
- Schutzisolierung (zusätzliche, doppelte oder verstärkte Isolierung)
- Schutztrennung (sichere Trennung eines Stromkreises gegen andere Stromkreise oder Erde)
- Schutz durch nicht leitende Umgebung

**Potenzialausgleich:** Alle leitenden Teile, die nicht zum Betriebsstromkreis gehören, über Potenzialausgleichsschiene galvanisch verbunden. Früher als "Nullung" bezeichnet, Begriff aus Normen weitgehend entfernt. Verbindung zum PEN-Leiter im TN-Netz; Fundamenterder (Bandstahl) eingebunden.

**Kleinspannungen ELV (Extra Low Voltage):**

- Spannungsbereich nach IEC 60449: AC ≤ 50 V Leiter-Leiter, DC ≤ 120 V zwischen L+ und L−. Gilt für geerdete, isolierte und nicht wirksam geerdete Netze.
- **SELV (Safety Extra Low Voltage):** Sicherheitskleinspannung im nicht geerdeten System. Spannungsquellen: Batterien, Klingeltransformatoren, Modelleisenbahn-Trafos, Netzteile (Schutzklasse III: Steckernetzteile, Ladegeräte).
- **PELV (Protective Extra Low Voltage):** Funktionskleinspannung mit Erdung der aktiven Leiter oder Körper (wenn betrieblich erforderlich); Anwendungsbeispiel: explosionsgefährdete Räume mit Potenzialausgleich zur Funkenverhinderung.

#### 5.1.2 Schutzarten und Schutzklassen (Seiten 380–382)

**IP-Schutzart nach DIN VDE 0470-1, EN 60525, IEC 60529:**

- Schutz von Personen gegen direktes Berühren aktiver Teile (Berührungsschutz)
- Schutz gegen Eindringen fester Fremdkörper
- Schutz gegen schädliche Wassereinwirkung

**IP-Code Aufbau:** Kürzel "IP" + erste Kennziffer (Berühr-/Fremdkörperschutz) + zweite Kennziffer (Wasserschutz) + optionale Buchstaben.

**Erste und zweite Kennziffer (Tab. 5.2 nach EN 60529):**

| Ziffer | Berührungsschutz (Person) | Fremdkörperschutz | Wasserschutz |
|---|---|---|---|
| 0 | kein Schutz | kein Schutz | kein Schutz |
| 1 | mit Handrücken | ≥ 50 mm Ø | senkrecht tropfendes Wasser |
| 2 | mit Fingern | ≥ 12,5 mm Ø | schräg (15°) tropfendes Wasser |
| 3 | mit Werkzeugen | ≥ 2,5 mm Ø | Sprühwasser schräg bis 60° |
| 4 | mit einem Draht | ≥ 1,0 mm Ø | Spritzwasser aus allen Richtungen |
| 5 | mit einem Draht | staubgeschützt | Strahlwasser |
| 6 | mit einem Draht | staubdicht | starkes Strahlwasser |
| 7 | — | — | zeitweiliges Untertauchen |
| 8 | — | — | dauerndes Untertauchen (5 bar) |

- Wenn erste oder zweite Kennziffer nicht angegeben: durch Buchstabe X ersetzen.
- Optionale Zusatzbuchstaben A/B/C/D: Zugangsschutz mit Handrücken (A), Finger (B), Werkzeug (C), Draht (D).
- Ergänzende Buchstaben H/M/S/W: Hochspannungsgerät (H), Wasserprüfung im Betrieb (M), Wasserprüfung im Stillstand (S), Wetterbedingungen (W).

**Elektrische Schutzklassen nach DIN EN 61140 (Tab. 5.3 nach DIN EN 60601):**

| Klasse | Merkmal | Schutzprinzip |
|---|---|---|
| I | Schutzleiteranschluss | keine Berührungsspannung bei Versagen der Basisisolierung |
| II | Schutzisolierung | doppelte oder verstärkte Isolierung |
| III | Kleinspannung | Anwendung von ELV |

**Fünf Sicherheitsregeln bei Arbeiten im spannungsfreien Zustand (Tab. 5.4, Norm EN 50110-1 / DIN VDE 0105 Teil 1):**

1. **Freischalten** aller Einspeisungen: Hauptschalter betätigen, Schmelzeinsätze entfernen, LS-Schalter betätigen, Trennstrecke in Luft oder gleichwertige Isolation herstellen; Kondensatoren oder Kabel nach Freischalten entladen.
2. **Gegen Wiedereinschalten sichern:** Betätigungsmechanismus sperren, Steuersicherung entfernen, Schmelzeinsätze sicher verwahren, LS-Schalter z.B. mit Klebeband absichern, Hilfsenergie unwirksam machen.
3. **Spannungsfreiheit feststellen:** Allpolige Spannungsfreiheit an der Arbeitsstelle mit zweipoligem Spannungsprüfer oder Messgerät; Spannungssucher kurz vor Benutzung auf Funktion prüfen.
4. **Erden und kurzschließen:** Zuerst erden, dann kurzschließen; Erdung und Kurzschließung sichtbar vom Arbeitsplatz; bei aufgetrennten Leitungen an beiden Seiten erden und kurzschließen; bei Freileitungen unter 1000 V möglichst alle Leiter erden, in jedem Fall kurzschließen.
5. **Benachbarte unter Spannung stehende Teile abdecken oder abschranken:** Abdeckung mit Tüchern, Schläuche (< 1 kV); zusätzlich Abschranken mit Absperrtafeln, Seilen etc. (> 1 kV).
- Maßnahmen nach Arbeitsende in umgekehrter Reihenfolge zurücknehmen. Erfahrung: bei Stromunfällen wurde mindestens eine Regel verletzt.

### 5.2 Niederspannungs-Schaltgeräte (Seiten 382–391)

#### 5.2.1 Überstrom-Schutzeinrichtungen (Seiten 382–388)

- Überstrom-Schutzeinrichtungen in der Strombahn eingebaut; unterbrechen:
  - **Kurzschlussströme** (sehr schnelle Abschaltung)
  - **Überlastströme** (Fluss über ausreichend lange Zeit)
- Zweck: unzulässige Erwärmung von Leitungen und Verbrauchern verhindern (Brandschutz); auch Stromkreise unter üblichen Bedingungen ein-/ausschalten.
- Grundeinteilung: **Sicherungen** und **Überstrom-Schutzschalter** (nach Auslösung wieder einschaltbar).
- Oberhalb 1 kV bis 36 kV: **HH-Sicherungen (Hochspannungs-Hochleistungs-Sicherungen)** verbreitet.

**Klassifikation Überstrom-Schutzeinrichtungen (Abb. 5.10):**

- Überstrom-Schutzschalter: Leitungsschutzschalter (LS-Schalter, DIN EN 60898 / VDE 0641), Geräteschutzschalter (DIN EN 60934 / VDE 0642), Elektromechanischer Schütz und Motorstarter (DIN EN 60647-4-1), Selektiver Haupt-Leitungsschutzschalter (SH-Schalter), SHA-Schalter (E DIN VDE 0643), SHU-Schalter (E DIN VDE 0645).
- Sicherungen: Niederspannungs-Hochleistungs-Sicherung (NH-Sicherung, DIN EN 60269 / IEC 60269 / VDE 0636), D-System (DIAZED), D0-Sicherung (NEOZED), Geräteschutzsicherung (G-Sicherung), Hochspannungs-Hochleistungs-Sicherung (DIN EN 60282), Teilbereichssicherung, Vollbereichssicherung.

**NH-Sicherungen:**

- Einsatzorte: Ortsnetzstationen, Kabelverteilschränke der Verteilnetzbetreiber, NS-Hauptverteilungen im Gebäude.
- Aufbau: Anzeiger, Steatit-Körper, Lotauftrag, Schmelzleiter, Grifflasche, Kontaktmesser.
- Sicherungen nach Bemessungsspannung ausgelegt.

**Genormte Bemessungsspannungen in V (Tab. 5.5, fette Werte nach IEC 60038):**

- AC: Reihe 1: 230, 500, 690; Reihe 2: 120, 208, 240, 277, 415, 480, 600
- DC: 110, 125, 220, 250, 440, 460, 500, 600, 750

**Genormte Bemessungsströme in A (Tab. 5.6):**

| Bauform | Bemessungsströme |
|---|---|
| D, D0 | 2, 4, 6, 8, 10, 13, 16, 20, 25, 32, 40, 50, 63, 80, 100 |
| NH 00 | 6, 8, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100 |
| NH 1 | 80, 100, 125, 160, 200, 250 |
| NH 2 | 125, 160, 200, 250, 315, 400 |
| NH 3 | 315, 400, 500, 630 |
| NH 4 | 500, 630, 800, 1000 |
| NH 4a | 500, 630, 800, 1000, 1250 |

- **Bemessungsstrom In:** dauerhaft tragbarer Strom ohne Beeinträchtigung der Funktionalität.
- Weitere Kenngrößen: Leistungsabgabe (Verlustleistung), Bemessungsausschaltvermögen (Ausschaltstrom).
- Strom-Zeit-Kennlinie: beschreibt Schmelzzeit/Ausschaltzeit als Funktion des unbeeinflussten Kurzschlussstroms Ik (prospektiver Kurzschlussstrom); Streubereich/Toleranzband ca. ±10 %.
- **Durchlassstrom iD:** höchster Augenblickswert beim Schaltvorgang; in Durchlass-Kennlinie iD(Ik) dargestellt.
- Zeitphasen beim Kurzschlussabschalten: Schmelzzeit ts, Lichtbogenzeit tL, Ausschaltzeit ta = ts + tL; Durchlassstrom iD < Stoßkurzschlussstrom ip.

**Betriebsklassen:**

- Erster Buchstabe = Funktionsklasse:
  - **g** (Ganzbereichssicherung / general purpose): unterbricht sicher zwischen kleinstem Schmelzstrom und Bemessungsausschaltstrom.
  - **a** (Teilbereichssicherung / accompanied fuse): schaltet oberhalb Vielfachem des Bemessungsstroms bis zum Bemessungsausschaltstrom aus.
- Zweiter Buchstabe = Schutzobjekt (Tab. 5.7):

| Buchstabe | Schutzobjekt |
|---|---|
| B | Bergbauanlagenschutz |
| G | Allgemeine Zwecke, hauptsächlich Kabel-/Leitungsschutz |
| L | Kabel-/Leitungsschutz (veraltet) |
| M | Motorstromkreise |
| PV | PV-Anlagen |
| R | Halbleiterbauelemente (Rectifier), flinker als S |
| S | Halbleiterbauelemente oder erhöhte Leitungsauslastung |
| Tr | Transformatorenschutz |

**Gebräuchliche Betriebsklassen (Tab. 5.8):**

| Klasse | Bedeutung |
|---|---|
| aM | Teilbereichs-Kurzschlussschutz Motorstromkreise |
| aR | Teilbereichs-Kurzschlussschutz Halbleiterbauelemente |
| gB | Ganzbereichs-Bergbauanlagenschutz |
| gG | Ganzbereichsschutz allg. Zwecke, Kabel-/Leitungsschutz |
| gL | veraltet, ersetzt durch gG |
| gM | Ganzbereichs-Schaltgeräteschutz |
| gPV | Ganzbereichssicherung für PV-Anlagen |
| gR, gS | Ganzbereichs-Halbleiterschutz |
| gTr | Ganzbereichs-Transformatorenschutz |

- Selektivität: hintereinandergeschaltete NH-Sicherungen verhalten sich selektiv, wenn sich ihre Bemessungsströme um mindestens Faktor 1,6 unterscheiden → nächstgelegene Sicherung schaltet zuerst ab (Staffelung im Strahlennetz).

**Leitungsschutzschalter (LS-Schalter / MCB):**

- International: MCB (Miniature Circuit Breaker). Umgangssprachlich: Sicherungsautomat, Automat. D0-Sicherungen oder D-Systeme für einzelne Stromkreise kaum mehr eingesetzt.
- Normenreihe: **DIN EN 60898 (VDE 0641-11)**.
- Zwei Auslösemechanismen:
  - **Elektromagnetauslöser:** zeitlich nahezu unverzögert; schützt vor Kurzschluss; nur stromstärkenabhängig.
  - **Thermo-Bimetall-Auslöser:** schützt vor Überlast; reagiert auf Erwärmung durch Strom und Zeit.
- Gemeinsame Auslösekennlinie: Kombination beider Auslöser.

**Auslösecharakteristiken nach DIN EN 60898 (Tab. 5.9):**

| Charakteristik | Anwendung | I2/In (Überlast) | I5/In (Kurzschluss) |
|---|---|---|---|
| B | Standard | 1,13...1,45 (30°C, 1h) | 3 ... 5 |
| C | Höherer Einschaltstrom: Maschinen, Lampengruppen | 1,13...1,45 (30°C, 1h) | 5 ... 10 |
| D | Stark induktive/kapazitive Last: Transformatoren, Kondensatoren, Schaltnetzteile | 1,13...1,45 (30°C, 1h) | 10 ... 20 |
| E | Selektiver LS-Schalter (SLS-Schalter) | 1,05...1,2 (30°C, 2h) | 5 ... 6,25 |
| Z | Halbleiterschutz, hohe Netzimpedanz | 1,05...1,2 (30°C, 2h) | 2 ... 3 |
| K | Hoher Einschaltstrom, sensible Überlastauslösung | 1,05...1,3 (30°C, 1h) | 8 ... 14 |

- **I2:** Strom, bei dem LS-Schalter bei 30°C innerhalb 1 h (oder 2 h) über Thermo-Bimetall-Mechanismus sicher abschaltet (Überlastschutz).
- **I5:** Strom, bei dessen Überschreitung Elektromagnetauslöser in ca. 40 ms unterbricht (Kurzschlussschutz).
- Untere Grenzwerte: Automat löst noch nicht aus. Obere Grenzwerte: maximaler noch unterbrechbarer Strom.

#### 5.2.2 Fehlerstrom-Schutzeinrichtungen (Seiten 388–391)

- Bezeichnungen: Differenzstrom-Schutzeinrichtung, FI-Schutzeinrichtung; international **RCD (Residual Current protective Device)**. F = Fehler, I = elektrische Stromstärke.
- Dienen dem **Personenschutz**. Typischer Auslösefall: Körperschluss.
- RCD ist Oberbegriff für unterschiedliche Ausführungen:
  - **RCCB (Residual Current operated Circuit-Breaker without overcurrent protection):** FI-Schutzschalter ohne eingebaute Überstrom-Schutzeinrichtung.
  - **RCBO (Residual Current operated Circuit-Breaker with Overcurrent protection):** FI/LS-Schalter; bietet Schutz vor Fehlerströmen UND Überlast-/Kurzschlussströmen.
  - **CBR (Circuit-Breaker incorporating Residual current protection):** Leistungsschalter mit fest angebautem Fehlerstromschutz; für Bemessungsströme oberhalb 125 A.
  - **MRCD (Modular Residual Current protective Device) / RCM (Residual Current Monitor):** modulare Fehlerstrom-Schutzgeräte ohne integrierte Abschaltvorrichtung; auch "Differenzstrom-Überwachungsgeräte". Fehlerstromerfassung über Wandler, Auswertung und Auslösung über separaten Leistungsschalter.
- **Funktionsprinzip FI-Schutzschalter:** Summenstromwandler (Ringkernwandler) überwacht Stromsumme IΔ in vier Leitern L1, L2, L3 und N. Fehlerfreiheit: Magnetfelder heben sich auf. Bei Körperschluss: Fehlerstromkreis schließt sich außerhalb der vier Leiter über PE oder Erdreich → verbleibende Magnetfelder induzieren merkliche Spannung in Sekundärwicklung → Abschaltung.
- **Bemessungsdifferenzstrom IΔn** (= Bemessungsfehlerstrom): Abschaltung erfolgt spätestens bei Erreichen dieses Wertes.
- **Bemessungsnichtauslösefehlerstrom IΔno:** Unterhalb dieses Wertes darf keine Auslösung erfolgen; Angabe durch Hersteller.
