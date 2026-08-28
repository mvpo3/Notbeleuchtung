# Projektmanagement für Ingenieure — Teil 6
> Quelle: Projektmanagement für Ingenieure (buecher) · Seiten 241-280.

Dieser Abschnitt behandelt zwei Kernthemen des Projektmanagements: zunächst wird die Earned Value Analyse (Kapitel 9, Abschluss) mit Istwertermittlung, Kennzahlen und Projektprognose vertieft. Dann folgt Kapitel 10 (Qualitätsmanagement) vollständig — von Qualitätsdefinition über ISO-Normenfamilie, TQM, Lean Management und Reifegradmodelle bis hin zu QM-Prozessen in Projekten (Planung, Lenkung, Sicherung). Kapitel 11 (Projektsteuerung) beginnt am Ende mit einer Überblickseinführung.

## Inhalt

### 9.3.2 Earned Value Analyse — Ermittlung der Istwerte

Der tatsächlich entstandene Aufwand (Actual Cost, AC) ergibt sich bei funktionierender Zeiterfassung mit Buchung auf Arbeitspakete direkt aus den Stundenwerten multipliziert mit Stundensatz.

Die Bestimmung des Fertigstellungswerts (Earned Value, EV) ist anspruchsvoller. Vollständig abgeschlossene Pakete fließen mit 100 % ein. Laufende Pakete erfordern Schätzungen des Fertigstellungsgrads (FG).

**Methoden zur FG-Schätzung für laufende Arbeitspakete:**

- **0=100-Methode**: Angefangene Pakete zählen mit 0 %, fertige mit 100 %. Sehr konservativ.
- **0=50=100-Methode**: Angefangene Pakete pauschal mit 50 % bewertet. Realistischer, bei vielen Paketen gleichen sich Einzelfehler aus.
- **Detaillierte Stufenmethode (0/20/50/80/100)**: Fertigstellung laufender Pakete wird auf einen der Fixwerte 20, 50 oder 80 % geschätzt.
- **Restaufwandsschätzung**: Präziseste, aber aufwändigste Methode. FG = Istwert / (Istwert + Restaufwand). Normallfall: Restaufwand = Plan minus Ist. Bei Mehraufwand sinkt FG entsprechend.

**Rechenbeispiel (Tab. 9.3 & 9.4) — 4 laufende Arbeitspakete:**

| Paket | Plan (T) | Ist (T) | FG Ist/Plan | 0=100 EV | 0=50=100 EV | Restaufwand | FG Rest | EV Rest |
|-------|----------|---------|-------------|----------|-------------|-------------|---------|---------|
| AP1   | 15       | 5       | 33 %        | 0,0      | 7,5         | 10          | 33 %    | 5,0     |
| AP2   | 12       | 10      | 83 %        | 0,0      | 6,0         | 4           | 71 %    | 8,6     |
| AP3   | 20       | 12      | 60 %        | 0,0      | 10,0        | 15          | 44 %    | 8,9     |
| AP4   | 15       | 8       | 53 %        | 0,0      | 7,5         | 8           | 50 %    | 7,5     |
| Summe | 62       | 35      | 56 %        | 0,0      | 31,0        | 37          | 49 %    | 30,0    |

Ergebnis: Die Restaufwandsschätzung liefert einen Fertigstellungswert von 30 Tagen (49 %), während der Ist-Aufwand 35 Tage (56 %) suggeriert. Reine Ist-Fortschreibung überschätzt also den Fortschritt.

Fazit: Die 0=50=100-Methode liefert bei minimalem Aufwand brauchbare Ergebnisse, besonders bei vielen kleinen Arbeitspaketen. Restaufwandsschätzungen sind präziser und fördern eine bewusste Auseinandersetzung der Beteiligten mit dem Arbeitsfortschritt.

---

### 9.3.3 Analyse von Plan-, Ist- und Sollzahlen — EVA-Kennzahlen

Aus Planned Value (PV), Actual Cost (AC) und Earned Value (EV) werden vier Kernkennzahlen abgeleitet:

**Terminabweichung:**
- Schedule Variance (SV) = EV − PV
- Schedule Performance Index (SPI) = EV / PV
- SV = 0, SPI = 1 → plangemäß; SV < 0, SPI < 1 → hinter Plan; SV > 0, SPI > 1 → vor Plan

**Kostenabweichung:**
- Cost Variance (CV) = EV − AC
- Cost Performance Index (CPI) = EV / AC
- CV = 0, CPI = 1 → kostenkonform; CV < 0, CPI < 1 → Kosten übersteigen Wert; CV > 0, CPI > 1 → effizient

**Rechenbeispiel 9.4 — Projekt nach 5 Monaten:**
- Gesamtbudget BAC = 420 Tsd. €, Gesamtlaufzeit TAC = 275 Tage
- AC = 140 Tsd. €, EV = 130 Tsd. €, PV = 115 Tsd. €
- CV = 130 − 140 = −10 Tsd. € → Kosten übersteigen Wert
- CPI = 130 / 140 = 0,928
- SV = 130 − 115 = +15 Tsd. € → Projekt liegt zeitlich vor Plan
- SPI = 130 / 115 = 1,130

Interpretation: Das Projekt macht schneller Fortschritt als geplant, verursacht aber gleichzeitig höhere Kosten als der erreichte Wert rechtfertigt.

**Vollständige Kennzahlen-Übersicht (Tab. 9.5):**

| Kennzahl | Abkürzung | Formel |
|----------|-----------|--------|
| Budget at Completion | BAC | Gesamtbudget (Planwert) |
| Time at Completion | TAC | Geplante Gesamtlaufzeit |
| Earned Value | EV | Fertigstellungswert |
| Planned Value | PV | Geplanter Wert zum Stichtag |
| Actual Cost | AC | Tatsächliche Kosten zum Stichtag |
| Cost Variance | CV | EV − AC |
| Cost Performance Index | CPI | EV / AC |
| Schedule Variance | SV | EV − PV |
| Schedule Performance Index | SPI | EV / PV |
| Estimate at Completion | EAC | BAC / CPI |
| Variance at Completion | VAC | EAC − BAC |
| Estimate to Complete | ETC | EAC − AC |
| Plan at Completion | PAC | TAC / SPI |
| Delay at Completion | DAC | PAC − TAC |

**Prognosekennzahlen** gehen davon aus, dass der bisherige Projektverlauf fortgeschrieben wird:
- EAC = voraussichtliche Gesamtkosten
- VAC = voraussichtliche Mehrkosten (positiv = Mehrkosten, negativ = Einsparung)
- ETC = verbleibende Restkosten
- PAC = voraussichtlicher Fertigstellungszeitpunkt
- DAC = Zeitverzug am Ende (positiv = Verzug, negativ = früher fertig)

**Rechenbeispiel 9.5 — Prognose aus Beispiel 9.4:**
- EAC = 420 / 0,928 = 452 Tsd. € → Mehrkosten erwartet
- VAC = 452 − 420 = +32 Tsd. € Mehrkosten
- ETC = 452 − 140 = 312 Tsd. € Restkosten
- PAC = 275 / 1,130 = 243 Tage → frühere Fertigstellung
- DAC = 243 − 275 = −32 Tage → 32 Tage früher

Hinweis: Diese Prognosen gelten nur bei Fortschreibung des bisherigen Verlaufs. Bei Projektproblemen werden steuernde Eingriffe nötig; diese werden im Rahmen der Projektsteuerung behandelt.

**Weiterführende Normen und Literatur (Kapitel 9):**
- ISO 21508:2018 — Earned Value Management im Projekt- und Programmmanagement
- Fleming/Koppelman: Earned Value Project Management, PMI, 4. Aufl. 2010

---

### 10.1 Qualität — Definition und Grundlagen

**Qualitätsbegriff:** Qualität bezeichnet den Grad, in dem ein Produkt die an es gestellten Anforderungen erfüllt. Kurz: Qualität ist Anforderungserfüllung. Diese Definition gilt für materielle Güter, Dienstleistungen und immaterielle Objekte gleichermaßen.

Produktmerkmale für die Anforderungen bestehen heißen Qualitätsmerkmale. Muss-Anforderungen definieren die Mindestqualität; ihre Nichterfüllung bedeutet fehlende Qualität. Soll-Anforderungen bestimmen den Grad der Qualität oberhalb des Minimums.

**Qualitätsbewertungs-Beispiel (10.1 — CAD-System):**
- Zielvariablen: Funktionsumfang (0–100 %), Handhabungsnote (5,0–1,0), Alt-Datei-Import (ja/nein), Linux-Eignung (ja/nein)
- Wertebereiche werden normiert (0 bis 1)
- Randbedingungen (Muss): Funktionsumfang ≥ 80 %, Handhabungsnote ≥ 3,0 (normiert > 0,5), Datei-Import muss möglich sein
- Gütekriterien mit Gewichtung: Funktionsumfang 50 %, Handhabung 40 %, Linux-Eignung 10 %
- Alle Randbedingungen erfüllt; Gesamtgüte = 0,725

**Drei Sichtweisen auf Qualität:**

1. **Objektive Sicht**: Kennt man alle Qualitätsmerkmale und ihre Werte, kennt man die Qualität. Messbar und überprüfbar.
2. **Subjektive Sicht**: Bei Massenprodukten ohne direkten Kundenkontakt weichen objektiv gemessene Qualität und subjektiv empfundene Kundenzufriedenheit ab. Unterschiedliche Nutzergruppen haben nicht deckungsgleiche Anforderungen.
3. **Kostenorientierte (relative) Sicht**: Qualität steht in Wechselwirkung mit Kosten. Höhere Qualität verursacht höhere Herstellkosten. Kunden bewerten das Preis-Leistungs-Verhältnis. Für Hersteller: Kosten der Qualitätssicherung vs. Kosten der Nichterfüllung.

**Beispiel 10.2 — Maschinenterminal — verschiedene Anforderungssteller:**
- Geschäftsleitung (Auftraggeber), Endkunden, Entwicklungsabteilung, Vertrieb
- Objektive Anforderungen: bestimmte Schnittstellen, IP-Schutzniveau, Preisobergrenze
- Subjektive Anforderung: „ergonomische" Benutzerschnittstelle — Ungeübte und Experten verstehen darunter Entgegengesetztes
- Konflikt: Entwicklung will Neuentwicklung mit neuen Bauteilen, Geschäftsleitung will Komponenten-Wiederverwendung für Kostenersparnis, Vertrieb fordert bessere Leistung bei niedrigerem Preis

---

### 10.1.3 Entwicklung des Fachgebiets Qualitätsmanagement

Chronologische Entwicklungsstufen (vgl. Abb. 10.2 — zeitliche Aufeinanderfolge, nicht Ablösung):

- **Vor 1920**: Handwerkliche Produktion — eine Person trägt Gesamtverantwortung für Qualität, implizit.
- **Ab ca. 1900/1920**: Arbeitsteilung führt zu Verlust direkter Qualitätsverantwortung → Qualitätsprüfung als eigenständige Abteilung entsteht. Fehlerhafte Produkte werden am Ende der Fertigung aussortiert oder nachgebessert.
- **Ab ca. 1940**: Massenproduktion macht lückenlose Prüfung unmöglich → Stichprobenprüfung mit statistischen Methoden. Statistische Prozesskontrolle rückt den Produktionsprozess in den Fokus.
- **Ab ca. 1960**: Verlagerung von Qualitätssicherung (Fehlererkennung) zu Qualitätsverbesserung (Fehlerreduzierung im Prozess). Qualitätssteuerung.
- **Ab ca. 1980**: ISO 9000-Normenreihe (erstmals 1986) definiert Anforderungen an Qualitätsmanagementsysteme (QMS). Alle Unternehmensprozesse (Entwicklung, Beschaffung, Führung, Kundenbeziehung) werden einbezogen. Begriff Qualitätsmanagement etabliert sich.
- **Ab ca. 2000**: Total Quality Management (TQM) — umfassende Ausweitung auf das gesamte Unternehmen.

---

### 10.1.4 Bedarf an Projekt-Qualitätsmanagement

Drei Gründe für ein dediziertes QM in Projekten:

1. **Fokussierung auf Anforderungserfüllung**: Projektmanagement verfolgt viele Ziele gleichzeitig (Ergebnis, Budget, Zeit). Einzelne Anforderungen können aus dem Blick geraten. Projekt-QM hält alle Anforderungen im Fokus und vermittelt bei Widersprüchen.
2. **Systematisierung der Methoden**: Qualitätsorientierte Maßnahmen in verschiedenen Projektphasen müssen aufeinander abgestimmt sein. Ein systematisches QM sorgt für ein konsistentes, reibungsarmes Gesamtsystem.
3. **Einbettung ins Unternehmens-QMS**: Projekte fallen in den Gültigkeitsbereich zertifizierter QMS und müssen auditiert werden. Projekt-QM muss mit dem übergeordneten Unternehmens-QM harmonieren.

Projekttypische Einschränkung: Da Projekte einmaligen Charakter haben, ist der aus der Serienproduktion bekannte schrittweise Verbesserungsansatz nicht direkt übertragbar. Trotzdem ist ein systemisches QM in Projekten möglich und notwendig.

---

### 10.2 Qualitätsmanagementsysteme — ISO 9000 ff.

**Normenfamilie ISO 9000 (wichtigste Normen, Tab. 10.1):**

| Norm | Inhalt |
|------|--------|
| ISO 9000:2015 | QMS — Grundlagen und Begriffe |
| ISO 9001:2015 | QMS — Anforderungen (verbindlich) |
| ISO 9004:2018 | QM — Anleitung zum nachhaltigen Erfolg (nicht verbindlich, Leitfaden) |
| ISO 10006:2017 | QM — Leitfaden für Qualitätsmanagement in Projekten |

Erstmals erschienen 1986. ISO 9001 enthält verpflichtende Anforderungen, deren Erfüllung nachweisbar sein muss. ISO 9004 ist freiwillig, aber hilfreich.

**Branchenspezifische QMS-Normen (Beispiele):**
- Automobilindustrie: VDA 6
- Medizintechnik: ISO 13485
- Telekommunikation: EN 9100 ff.

**Unterstützende Institutionen:**
- Deutschland: Deutsche Gesellschaft für Qualität (DGQ)
- Europa: European Organisation for Quality (EOQ), European Foundation for Quality Management (EFQM)
- USA: American Society for Quality (ASQ)

---

### 10.2.2 Grundsätze der ISO 9000

Acht Grundsätze für das Qualitätsmanagement (vier betreffen Akteure, zwei Systemsicht, zwei Problemlösung):

**Akteursbezogene Grundsätze:**
1. **Einbeziehung von Personen**: Produkte werden von Menschen für Menschen gemacht. Ein QMS muss die Beteiligten berücksichtigen und einbeziehen.
2. **Kundenorientierung**: Anforderungen der Kunden müssen vollständig erfasst, verstanden und erfüllt werden.
3. **Führung**: Führungspersonen setzen Ziele, schaffen Rahmenbedingungen und sind für Qualität verantwortlich. Glaubwürdigkeit entsteht durch das Vorleben eigener Vorgaben.
4. **Lieferantenbeziehung zum gegenseitigen Nutzen**: Lieferanten sind Teil der Wertschöpfungskette. Ihr Beitrag und ihre Anforderungen müssen im QMS berücksichtigt werden.

**Systemorientierte Grundsätze:**
5. **Prozessorientierter Ansatz**: Tätigkeiten sind als Prozesse zu betrachten, die Input in Output wandeln und Ressourcen sowie beteiligte Personen erfordern.
6. **Systemorientierter Managementansatz**: Prozesse stehen in wechselseitiger Abhängigkeit zueinander (Output eines Prozesses = Input des nächsten). Diese Vernetzung muss bei Planung und Steuerung berücksichtigt werden.

**Problemlösungsorientierte Grundsätze:**
7. **Sachbezogene Entscheidungsfindung**: Vor Entscheidungen steht die Erfassung und Auswertung sachlicher Informationen (Messungen, Analysen).
8. **Ständige Verbesserung**: Ein QMS ist kein einmaliger Aufbauakt. Organisationen befinden sich in ständigem Wandel — kontinuierliche Anpassung ist unvermeidlich.

---

### 10.2.3 Das QM-Prozessmodell

Das Modell der ISO 9001 definiert sieben Hauptprozesse in drei rückgekoppelten Wirkungskreisen:

**Innerer Wirkungskreis (4 Hauptprozesse):**
- **Betrieb**: Setzt Kundenanforderungen in Produkte um.
- **Bewertung der Leistung**: Erfasst Produktbeschaffenheit objektiv und Kundenzufriedenheit subjektiv.
- **Führung**: Leitet aus Bewertungsergebnissen Entscheidungen für Planung ab.
- **Planung**: Leitet aus Führungsentscheidungen Ressourcen-, Personal- und Infrastrukturbereitstellung ab. Unterstützende Aktivitäten sind im Hauptprozess „Unterstützung" gebündelt.

**Mittlerer Wirkungskreis:** Prozess „Verbesserung" — nutzt Erkenntnisse aus dem inneren Kreislauf zur stetigen Weiterentwicklung.

**Äußerer Wirkungskreis:** Prozess „Kontext der Organisation" — zielt auf die Weiterentwicklung der Gesamtorganisation.

**PDCA-Zyklus (Deming-Zyklus):** Grundprinzip auf allen Ebenen:
- Plan: Planung der Arbeiten
- Do: Ausführung
- Check: Überprüfung der Ergebnisse
- Act: Anpassung der Planungen bei Abweichungen

Der PDCA-Zyklus findet sich auf jeder Hierarchieebene — von der Gesamtorganisation bis zu einzelnen Arbeitsvorgängen.

**Beispiel 10.3 — Anforderungen für Entwicklungsplanung (ISO 9001 Abschnitt 8.3.2):**

Anforderungen an den Teilprozess Entwicklungsplanung:
- Entwicklungsprozess in Phasen gliedern
- Art, Dauer und Umfang der Entwicklungstätigkeiten festlegen
- Verantwortungen und Befugnisse der Beteiligten beschreiben
- Bewertung, Verifikation und Validierung der Ergebnisse festlegen

Diese Anforderungen bilden überprüfbare Kriterien für QMS-Auditierungen.

---

### 10.3 Qualitätsorientierte Managementkonzepte (QoM)

#### 10.3.1 Total Quality Management (TQM)

TQM geht über die reine QMS-Systematisierung hinaus und erweitert den Qualitätsbegriff auf das gesamte Unternehmen.

**Qualitätsbezogene Preise (fördern TQM freiwillig):**
- Deming Prize: seit 1951
- Malcolm Baldrige National Quality Award (USA): seit 1987
- EFQM Excellence Award (Europa): seit 1992

TQM gilt als „Kür" gegenüber der „Pflicht" eines QMS. Es ist kein neues Methodensystem, sondern eine erweiterte Zielsetzung.

**Erweiterte Qualitätsperspektive in TQM (Abb. 10.4):**
- Qualität der Produkte
- Qualität der Prozesse
- Qualität der Arbeit
- Qualität des Unternehmens als Ganzes
- Einbeziehung: Kunden, Mitarbeiter, Lieferanten
- Merkmale: Teamfähigkeit, Lernfähigkeit, Verantwortlichkeit

Ziel ist nicht nur Kundenzufriedenheit, sondern auch Zufriedenheit von Personal, Lieferanten, Unternehmenseignern und Gesellschaft. Damit ist TQM faktisch ein umfassendes Unternehmensmanagement-Konzept (wird deshalb nicht mehr im Begriff ISO 9000 geführt).

**Fünf TQM-Prinzipien für Projekte:**

1. Qualität ist das oberste Ziel — alle anderen Ziele (Kosten, Produktivität, Marktanteil) sind Folgen hoher Qualität (Demings Reaktionskette).
2. Qualität ist die Erfüllung der Anforderungen aller Betroffenen — nicht nur der Käufer, sondern auch Belegschaft, Führung, Lieferanten, gesellschaftliches Umfeld.
3. Qualität erfordert, dass alle Beteiligten ihre Verantwortung tragen — Ziele werden gemeinsam mit allen Betroffenen definiert, nicht nur vorgegeben.
4. Qualität erfordert prozessorientierte Sichtweise — jeder Beteiligte ist gleichzeitig Kunde des vorgelagerten und Lieferant des nachgelagerten Prozesses (internes Kunden-Lieferanten-Verhältnis).
5. Zur Erreichung von Qualität sind stetige Verbesserungen notwendig — Null-Fehler als Idealziel; kontinuierliche Verbesserung ist Wesensmerkmal von TQM. Japanisch: Kaizen, deutsch: Kontinuierlicher Verbesserungsprozess (KVP).

---

#### 10.3.2 Lean Management

Basiert auf denselben QM-Werkzeugen wie TQM, strukturiert durch fünf Grundprinzipien:

1. **Kundennutzen**: Dem Kundenwert wird höchste Priorität eingeräumt; alle Entscheidungen daran ausrichten.
2. **Wertschöpfungsprozesse**: Alle beteiligten Prozesse — Herstellung, Entwicklung, Beschaffung, unterstützende Funktionen — müssen zur Wertschöpfung beitragen.
3. **Prozessfluss**: Kontinuierlicher Output aller Prozesse, damit nachfolgende Prozesse stetig arbeiten können. Unnötiges Puffern, Liegezeiten und Transportwege sind zu vermeiden.
4. **Pull-Prinzip**: Aufträge werden nicht in die Produktion gedrückt (klassische Planung), sondern durch die Prozesskette gezogen. Jeder Prozess reagiert auf Anforderungen des Nachfolgeprozesses. Bekannteste Umsetzung: **Kanban** — Teileentnahme löst automatisch Produktionsauftrag für vorgelagerten Prozess aus. Ergebnis: nur benötigte Mengen vorrätig, keine Überproduktion.
5. **Kontinuierliche Verbesserung**: Daueraufgabe; Verbesserungsmöglichkeiten aktiv suchen und systematisch umsetzen.

**Lean-Methoden (Beispiele):** Just-in-Time, Kanban, One-Piece-Flow, Wertstromdesign.

**Unterschied Innovation vs. Progression:**
- Innovation: sprunghafte Fortschritte durch Erfindungen, neue Technologien (hohe Aufmerksamkeit).
- Kontinuierliche Verbesserung (KVP/CIP/Kaizen): schrittweise Fortschritte, weniger öffentlich wahrgenommen, aber nachhaltig wirksam.

---

#### 10.3.3 Kontinuierliche Verbesserung (KVP)

Jede KVP-Iteration ist ein vollständiger Problemlösungszyklus mit speziellen Erweiterungsschritten:

**Qualitätszirkel:** Feste Gruppe von 5–12 Personen, die freiwillig und selbstständig Verbesserungsvorschläge bearbeiten. Trifft sich regelmäßig.

**Ablauf:**
- **Study-Phase**: Ist-Zustand analysieren, Zielzustand formulieren, Wechselwirkungen und Ursachen untersuchen.
- **Plan-Phase**: Lösungsideen entwickeln und bewerten, Maßnahmen und Aufwand/Nutzen bestimmen.
- **Entscheidungsgremium**: Bewertet Vorschläge verschiedener Qualitätszirkel, wählt wichtigste aus, vereinbart Ressourcen.
- **Operate/Do-Phase**: Zunächst Testlauf an einem Arbeitsplatz; bei Erfolg Standardisierung und Ausweitung.
- **Check**: Erfolgsprüfung.
- **Act**: Dauereinsatz, falls erfolgreich.

Dies entspricht dem **PDCA-Zyklus (Deming-Zyklus)**: Plan → Do → Check → Act — als immer wiederkehrender Zyklus graphisch oft als Rad auf aufwärts strebender Kurve dargestellt.

---

#### 10.3.4 Reifegradmodelle

**Grundprinzip:** Reifegradmodelle messen das Kompetenzniveau einer Organisation in der Ausführung ihrer Prozesse. Für jeden Prozess werden Fähigkeitsstufen definiert. Die Gesamtheit ergibt den Reifegrad der Organisation.

Unterschied zu ISO 9001-Auditierung: ISO 9001 prüft Übereinstimmung von tatsächlichen und geplanten Abläufen. Reifegradmodelle messen, wie gut Prozesse beherrscht werden.

**CMMI (Capability Maturity Model Integration):**
- Sammelt bewährte Praktiken (Best Practices) und ordnet sie Arbeitsprozessen zu.
- Basiseinheit: **Prozessgebiet (Process Area, PA)** — fasst alle Anforderungen zu einem Thema zusammen.
- CMMI definiert insgesamt **22 Prozessgebiete**, darunter:
  - Anforderungsmanagement (REQM)
  - Projektplanung (PP)
  - Projektverfolgung und -steuerung (PMC)
- Jedes Prozessgebiet hat: Zweckbeschreibung, Hinweise, Beziehungen zu anderen PAs, spezifische Ziele (Specific Goals, SG) und spezifische Praktiken (Specific Practice, SP).
- **Spezifische Praktiken (SP)**: Konkrete, in der Praxis bewährte Handlungsmuster. Sie beschreiben was getan werden muss, nicht wie.
- Beispiel: Für das Ziel „Schätzungen etablieren" gibt es die Praktik „Schätzung für Aufwand und Kosten festlegen" mit Ergebnissen wie „Schätzgrundlagen", „Aufwandsschätzungen", „Kostenschätzungen" und Subpraktiken.
- CMMI lässt offen, wie der Bedarf der unterstützenden Infrastruktur kalkuliert wird — fordert aber, dass er in die Schätzung einbezogen wird.

---

### 10.4 Qualitätsmanagement in Projekten

#### 10.4.1 QM-Prozesse in Projekten

Drei QM-Prozesse im Projekt (Abb. 10.6):

1. **Qualitätsplanung**: Legt fest, welche Maßnahmen und Methoden zur Qualitätserreichung einzusetzen sind. Ergebnis: QM-Managementplan (Vorgehensweisen und Abläufe) + Qualitätsplan (konkrete Ableitung der Produktqualität aus Projektzielen).

2. **Qualitätslenkung**: Sorgt während der Durchführung für die Umsetzung der Planung. Fortschritte messen, realisierte Liefergegenstände erfassen, Soll-/Ist-Vergleich, notwendige Eingriffe und Änderungsanträge ableiten.

3. **Qualitätssicherung**: Überprüft Wirksamkeit von Planungs- und Lenkungsmaßnahmen. Dient zur kontinuierlichen Verbesserung des QM innerhalb von Projekten. Hauptsächlich nach Projektabschluss wirksam.

Projektspezifische Besonderheit: Im Unterschied zu Routineprozessen muss die geforderte Qualität nach einem einzigen Durchlauf am Projektende vollständig erreicht sein — schrittweise Verbesserung über Iterationen ist nur begrenzt möglich.

**ISO 10006** (Leitfaden für QM in Projekten): Gehört zur ISO-9000-Familie, strukturiert wie ISO 9001. Gibt Hilfestellungen für Herstellung und Sicherung der Projektqualität in PM-Teilprozessen. Hat Gemeinsamkeiten mit ISO 21500, ICB (IPMA), PMBOK (PMI) und PRINCE2, jedoch auch Details-Unterschiede.

---

#### 10.4.2 Qualitätsplanung

Qualitätsplanung begleitet den gesamten Weg von abstrakten Anforderungen bis zum realisierten Projektergebnis. Zwischenergebnisse müssen bereits während der Projektdurchführung überprüft werden.

**Quality Gates:** Definierte Kontrollpunkte, die nur passiert werden können, wenn Zwischenergebnisse die Anforderungen erfüllen. Bieten sich an Meilensteinen an, können aber auch zwischengeschaltet werden.

**Quality Function Deployment (QFD):**

Methode zur systematischen Verknüpfung von Kundenanforderungen mit Produktlösungsmerkmalen. Entwickelt in Japan durch Akao in den 1960ern, in den USA ab 1980ern, in Europa ab 1990ern verbreitet.

Grundgedankenkette:
1. Anforderungen des Kunden vollständig erfassen und hierarchisch auflisten. Jeder Anforderung eine Prioritätszahl zuordnen (z. B. 1–5).
2. Lösungsmaßnahmen des Herstellers als gegliederte Liste zusammenstellen.
3. Anforderungen (Zeilen) und Maßnahmen (Spalten) in einer **Korrelationsmatrix** gegenüberstellen. Jede Matrixzelle gibt den Einfluss der Maßnahme auf die Anforderung an (Skala 0 = kein Einfluss bis 3 = starker Einfluss).
4. Bedeutung jeder Maßnahme: Summe der Produkte (Anforderungspriorität × Einflussgröße) über alle Anforderungen. Kann als relative Prozentzahl ausgedrückt werden.

**House of Quality (HoQ)** — erweiterte Gesamtdarstellung (Abb. 10.7):
- Fragestellungen: Was (Kundenanforderungen), Wie (Lösungsmerkmale), Warum (Wettbewerbsvergleich auf Anforderungsebene), Wieviel (Zielgrößen für Merkmale)
- Dach: Korrelationsmatrix der Lösungsmerkmale untereinander (zeigt gegenseitige Beeinflussung, positiv oder negativ)
- Unterhalb der Hauptmatrix: absolute und relative Bedeutung jedes Merkmals, Schwierigkeitsgrad der Realisierung (Punkteskala), Wettbewerbsvergleich auf Merkmalsebene
- Ziel: wichtige von unwichtigen Lösungsmaßnahmen unterscheiden — Maßnahmen mit höchstem Beitrag zur Anforderungserfüllung und maximaler Differenzierung vom Wettbewerb identifizieren

Devise des QFD-Erfinders Akao: „Copy the spirit, not the form" — Kerngedanken auf individuelle Problemstellungen übertragen, nicht an Formalitäten scheitern.

---

#### 10.4.3 Qualitätslenkung

Aufgabe während der Projektdurchführung: Überprüfen, ob das Projekt auf Kurs ist. Istwerte erfassen, mit Sollwerten vergleichen, Regelkreise für notwendige Eingriffe schließen.

**Zielvariablen:** Bei der Zielformulierung werden messbare Variablen definiert (stetige, diskrete oder binäre Größen). Frühzeitig messbare Variablen ermöglichen frühere Korrektureingriffe.

**Qualitätswerkzeuge (graphische Darstellungsmittel):**

- **Fehlersammelliste (Strichliste)**: Zählt aufgetretene Fehlerarten. Fehlerarten vorab benennen, Kategorie „Sonstige" vorsehen. Kann in Zeitintervalle (pro Tag, pro Schicht, pro Stunde) unterteilt werden.
- **Histogramm**: Balkendiagramm der Häufigkeit bestimmter Qualitätsmerkmale. Eine Achse: mögliche Merkmalswerte; andere Achse: Häufigkeiten.
- **Pareto-Diagramm**: Spezielle Histogrammform, bei der Merkmalswerte nach Häufigkeit sortiert sind (absteigende Balkenlänge). Grundlage der **Pareto-Analyse** (Suche nach wichtigsten Einflussfaktoren).
  - **80/20-Regel**: 20 % der Fehlerarten verursachen 80 % aller Fehler.
  - **ABC-Analyse**: Einteilung aller Merkmale in Kategorien A (wichtigste), B und C.
- **Korrelationsanalyse**: Untersucht Wechselwirkungen zwischen zwei beobachteten Größen x und y. Korrelationskoeffizient r normiert auf Bereich −1 bis +1.
  - r = 0: keine Abhängigkeit
  - r > 0: gleichläufige Wirkung
  - r < 0: gegenläufige Wirkung
  - r = ±1: vollständige Kopplung
  - Einschränkung: Korrelation ist kein Kausalitätsbeweis. Beide Größen könnten durch eine dritte gemeinsame Ursache getrieben sein.
- **5-Warum-Fragetechnik**: Durch mehrfaches Nachfragen von beobachteter Wirkung (Fehler) zu tieferliegenden Ursachen gelangen. Die Zahl 5 ist nicht wörtlich, signalisiert: nicht vorzeitig abbrechen.
- **Ursache-Wirkungs-Diagramm (Ishikawa)**: Stellt viele Einflussfaktoren auf eine Wirkung grafisch dar. Einflussfaktoren werden als Pfeile dargestellt, zu Gruppen zusammengefasst, die auf einen Hauptpfeil zur beeinflussten Größe führen.

**Qualitätserfassung im Projektverlauf:**
- Permanente Erfassung nicht sinnvoll (keine ständigen signifikanten Änderungen im Einzelprojekt).
- Erfassung integraler Bestandteil von Meilensteinen: Meilenstein gilt erst als erreicht, wenn Zwischenergebnisse die Anforderungen erfüllen.
- Zwischen Meilensteinen können weitere Quality Gates eingeplant werden.
- Entwurfsphase: qualitative Fortschritte schwer messbar, häufig Restaufwandsschätzungen.
- Realisierungsphase (z. B. Software): tägliche Code-Inspektion und regelmäßige Release-Tests möglich.
- Projektabschluss: Verifikation (alle Lieferungen und Leistungen in zugesagter Quantität und Qualität vorhanden?) → Validierung (werden damit die Auftraggeber-Anforderungen erfüllt?) → Abnahme durch Auftraggeber.

**Beispiel 10.4 — Qualitätsplanung Software-Projekt (Lieferantenverwaltung für Fahrzeughersteller):**
- Anforderungsbeschreibung als „User Stories" aus Anwendersicht
- Rapid Prototyp für jeden Anwendungsfall → Benutzer-Abnahme der Bildschirmmasken
- Entwurfsdokument im „Structured Walk Through" mit unabhängigem Entwickler besprochen
- Testfälle bereits in der Entwurfsphase definiert
- Nach Implementierung: Modul-Tests → schrittweise Integration → Integrationstest → Übergabe → Kunden-Abnahme im vereinbarten Umfang

**Änderungsmanagement** als Bestandteil der Qualitätslenkung: Anforderungen ändern sich häufig während der Projektlaufzeit. Jede Änderung zieht zusätzlichen Aufwand nach sich. Stillschweigende Übernahme von Änderungen führt zu Mehrkosten und Verzögerungen. Erfassung, Analyse und Plananpassung bei Anforderungsänderungen ist Pflichtaufgabe.

---

#### 10.4.4 Qualitätssicherung

Zweck: Sicherstellung der Funktionsfähigkeit und stetige Verbesserung des Projekt-QMS. Nutzt Erkenntnisse aus Planung, Lenkung und vor allem aus der **Projekt-Retrospektive** nach Abschluss.

**Methoden zur QMS-Weiterentwicklung:**
- Projektinternes Vorschlagswesen
- Kontinuierlicher Verbesserungsprozess (KVP) aus dem Unternehmens-QM
- Qualitätszirkel bei grundsätzlichen Problemen

**Reifegradmodelle zur QMS-Messung (Beispiele):**
- CMMI (bereits beschrieben)
- OPM3 (Organizational Project Management Maturity Model, PMI)
- P3M3 (Portfolio, Programme, and Project Management Maturity Model)

**Exzellenz-Modelle als Qualitätsanreiz:**
- Ludwig-Erhard-Preis
- Deming-Award
- EFQM Excellence Award
- GPM-Modell „Project Excellence" — Adaption des EFQM-Modells für Projekte

**GPM Project-Excellence-Modell (Abb. 10.8):**
- Zwei Bewertungsbereiche: Projektergebnis und Projektmanagement
- Untergliedert in 9 Hauptkriterien, diese in weitere Teilkriterien
- Bewertung durch unabhängige Kommission im Assessment mit offengelegten Punkteschemata
- Nutzbar auch zur Selbstbewertung und zur Identifikation von PM-Schwachstellen

**Weiterführende Literatur (Kapitel 10):**
- Jakoby, W.: Qualitätsmanagement für Ingenieure. Springer Vieweg, 3. Aufl. 2025
- Preißner, A.: Projekterfolg durch Qualitätsmanagement. Hanser-Verlag, 2006
- Bartsch-Beuerlein, S.: Qualitätsmanagement in IT-Projekten. Hanser-Verlag, 2000
- Schmitt, R., Pfeifer, T.: Qualitätsmanagement. Hanser-Verlag, 5. Aufl. 2015

---

### 11.1 Projektsteuerung — Einführung (Kapitel 11, Beginn)

Projektsteuerung umfasst den regelmäßigen Abgleich des tatsächlichen Projektverlaufs mit den Projektplänen. Selbst bei gewissenhafter Vorbereitung kommt es zu Abweichungen durch externe Einflüsse und Planungs- oder Ausführungsfehler.

**Vier Hauptprozesse der Projektsteuerung (Abb. 11.1):**
- Projektüberwachung: Fortschrittsdaten erfassen
- Fortschrittssteuerung: korrigierende Maßnahmen ableiten
- Änderungsmanagement: Änderungsanträge bearbeiten
- Projektabschluss: validierte Liefergegenstände übergeben

Eingaben: Projektpläne + Fortschrittsdaten. Ausgaben: Arbeitsleistungsinformation + Änderungsanträge + korrigierende Maßnahmen + validierte Liefergegenstände.

**Grundprinzip:** Terminierter Ablaufplan = Sollwert im Regelkreis. Tatsächlicher Fortschritt = Istwert. Bei Abweichungen: primär lenkende Eingriffe zur Korrektur; falls nicht möglich, Plan revidieren.

**Kernfragen der Projektsteuerung (ab Kapitel 11.1):**
- Woraus besteht der Projektfortschritt?
- Wie kann er gemessen werden?
- Wann muss er gemessen werden?
