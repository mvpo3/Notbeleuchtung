# Projektmanagement für Ingenieure — Teil 7
> Quelle: Projektmanagement für Ingenieure (buecher) · Seiten 281-320.

Dieser Teil behandelt Kapitel 11 (Projektsteuerung) vollständig sowie den Beginn von Kapitel 12 (Der Mensch im Projekt). Themen: Projektdatenerfassung, Fertigstellungsgrad-Methoden, Meilenstein-Trendanalyse, Fortschrittssteuerung, Änderungsmanagement, Projektabschluss, Erkenntnissicherung sowie Grundlagen des Selbstmanagements und Stressbewältigung im Projektumfeld.

## Inhalt

### 11.1 Projektüberwachung

#### 11.1.1 Projektdatenerfassung

Fortschrittsinformationen stammen primär von den zuständigen Bearbeitern. Um diese Informationen strukturiert zu erfassen, muss ein systematisches Berichtswesen eingerichtet werden. Statusberichte und Änderungsberichte liefern die Grundlage.

**Anforderungen an Berichte:**
- Standardisierter Aufbau (kein freies Format), damit Angaben vergleichbar und vollständig sind
- Pflichtangaben: geplanter Arbeitsaufwand, tatsächlicher Aufwand, geschätzter Restaufwand
- Symbolische Zustandsangaben (z.B. Ampelsystem) bewährt
- Ausreichend Raum für individuelle Darstellungen nötig (fachliche Vielfalt)
- Berichte zu festen, vorher festgelegten Terminen verfassen
- Drei-R-Regel: Regelmäßigkeit, Rechtzeitigkeit, Richtigkeit
- Probleme dürfen nicht verschleiert werden; gleiche Inhalte in aufeinanderfolgenden Berichten sind Warnsignal

**Informelle Abfragen:** Schriftliche Berichte neigen zu Abstraktheit und Verschleierung. Persönliche Gespräche ermöglichen das Erkennen echter Fortschritte und Probleme besser — Projektleiter sollte regelmäßig einzeln mit Mitarbeitern sprechen.

**Beispiel 11.1 — Projektstatus-Schnappschuss (23.6., Projekt 10.6.–3.7.):**
- AP1: abgeschlossen, 2 Tage Verzug (Fertigstellung 19.6. statt 17.6.), +20 % Mehrkosten
- AP2: in Bearbeitung, 75 % Planzeit verstrichen, optimistisch termingerecht, Kosten im Budget
- AP3: sollte fertig sein, „kleinere Restprobleme", Mitarbeiter überzeugt von Lösung bis Wochende
- AP4: erst 22.6. begonnen (wegen AP1-Verzug), keine konkreten Aussagen möglich, kann Zeitverlust evtl. aufholen
- AP5: kann nicht starten solange AP3 unvollständig

Erkenntnis: Projektabschluss erst am Ende bewertbar (Funktionalität, Kosten, Termine); für laufende Steuerung zu spät — daher regelmäßige Fortschrittskontrolle nötig.

**Fortschrittsmessung auf Arbeitspaket-Ebene:**
- Kleine Pakete (wenige Tage): 0 % oder 100 %, keine Zwischenwerte
- Mittlere Pakete (5–10 Arbeitstage): dritter Status „in Arbeit" = pauschal 50 %
- Empfohlenes Messintervall: Wochenrhythmus; in kritischen Phasen kürzer
- Permanente Messung erzeugt Überwachungsgefühl → hemmt Kreativität; sinnvoller Kompromiss auf AP-Ebene

**Fertigstellungsgrad-Methoden (Tab. 11.1):**

| Methode | Anwendungsebene | Basisgröße | Formel / Merkmale |
|---------|----------------|------------|-------------------|
| Meilenstein-Methode | Projektphase | Menge | FGR durch erreichte Meilensteine; grob, wichtige Ergebnisse vorliegend |
| Statusschritte | Arbeitspaket | Menge | FGR = 0 % / 50 % / 100 %; leicht handhabbar |
| Zeitproportionalität | Arbeitspaket | Zeit | FGR = Istzeit / Planzeit; oft ungenau bei Mehraufwand |
| Restzeitschätzung | Arbeitspaket | Zeit | FGR = (Planzeit − Restzeit) / Planzeit; Aktualisierung z.B. wöchentlich |
| Mengenschätzung | Arbeitspaket | Menge | FGR = x %; subjektiv, kaum überprüfbar; nur als letzter Ausweg |
| Mengenmessung | Arbeitspaket | Menge | FGR = Istmenge / Planmenge; sehr gut wenn geeignetes Mengenmaß vorhanden |

**Kritische Hinweise zur Genauigkeit:**
- 33 % der Arbeitsstunden ≠ 33 % der erwarteten Leistung
- Bekanntes Phänomen: 95-%-Syndrom in Softwareprojekten — plangemäße Fortschrittsmeldungen bis kurz vor Ende, dann Verzögerungsspirale
- Verbesserung: Neben Ist-Stunden immer auch voraussichtlichen Restaufwand schätzen; wöchentlich und selbsttätig ohne Aufforderung melden
- Qualitätskontrolle bei kritischen Paketen zwingend durch zweite Person

**Testbarkeit durch Modularisierung:**
- Feiner modulierter Produktstrukturplan ermöglicht stufenweises Testen (Einzel → Teilkomponente → Gesamtsystem)
- Reduziert Überraschungen im Systemtest

**Agile Projekte (Scrum):**
- Aufwandsmessung in Story Points statt Personentagen
- Gesamtaufwand = Summe aller Story Points im Product Backlog
- Burndown Chart: geplanter vs. tatsächlich verbleibender Aufwand über Projektlaufzeit
- Steigung der Plangeraden = Workload pro Sprint (Zeiteinheit)
- Tatsächlicher Verlauf unter Plangerade → besser als geplant; darüber → langsamer

#### 11.1.2 Projektdatenauswertung

Berichte allein sind nicht ausreichend — sie müssen ausgewertet und in steuernde Maßnahmen umgesetzt werden.

**Informationsverdichtung mit dem Zieldreieck:**
- Alle Einzelinformationen zu drei Achsen komprimieren: Funktionalität, Kosten, Termine
- Verbindung der drei Punkte ergibt Dreieck, dessen Form den Projektzustand symbolisiert
- Idealfall (alle Istwerte = Planwerte): gleichseitiges Dreieck
- Beispiel a: Funktionalität + Kostenrahmen eingehalten, Terminüberschreitung → Dreieck verzerrt Richtung Termin-Achse
- Beispiel b: Termine gehalten, aber Mehrkosten und reduzierte Funktionalität

**Reaktionsmöglichkeiten auf Planabweichungen (Tab. 11.2):**

| Priorität | Realität ändern | Plan ändern |
|-----------|----------------|-------------|
| Funktions-Priorität | Kapazität erhöhen | Termine verschieben |
| Kosten-Priorität | Produktivität erhöhen, Funktionen vereinfachen | Termine verschieben |
| Termin-Priorität | Kapazität (Personaleinsatz) erhöhen, Funktionen vereinfachen | — |

**Konkrete Maßnahmenliste:**
- Kapazität erhöhen: Überstunden, zusätzliche Mitarbeiter, Leistungszukauf
- Produktivität erhöhen: Schulung, qualifiziertere Mitarbeiter, bessere Information/Kommunikation, Motivation verbessern, von unproduktiven Arbeiten befreien
- Funktionen vereinfachen: nicht zwingend benötigte Funktionen streichen, einfachere technische Alternativen, Qualitätsanforderungen einschränken, Änderungswünsche ablehnen

#### 11.1.3 Fortschrittsplanung

Je detaillierter die Planung, desto früher erkennbar Abweichungen. Für den Planfortschrittsvergleich wird ein Referenzverlauf benötigt.

**S-Kurven-Verlauf des Projektfortschritts:**
- Typischer Projektverlauf aus systemtheoretischer Sicht: S-förmig (Verzögerungssystem)
- Anfangsphase: geringe oder keine sichtbaren Fortschritte (Vorarbeiten, Einarbeitung)
- Mittlere Phase: gute Fortschritte
- Endphase: Verlangsamung durch Tests, Fehlersuche, unterschätzte Detailaufgaben

**Lineare Denkfehler in verschiedenen Projektphasen:**
- Frühe Phase (t1): lineare Projektion → pessimistische Einschätzung → hektischer Aktionismus statt Analyse
- Mittlere Phase (t2): überhöhter Optimismus, Restaufwand unterschätzt, unrealistische Endterminversprechen → Ernüchterung beim Abflachen der Kurve

**Leistungspakete statt Programmzeilen-Messung:**
- Programmzeilen als Fortschrittsmaß ungeeignet (Analyse/Entwurf erzeugen keine Zeilen; Optimierung verkürzt Code)
- Besser: überprüfbare Leistungspakete (P1, P2, P3, P4) mit zugehörigen Meilensteinterminen
- Paketgrößen für gleichmäßige Terminverteilung: frühe Pakete kleiner, mittlere größer, späte wieder kleiner

**Beispiel 11.2 — Leistungspakete Software-Projekt:**
- Meilenstein 1: Abschluss Anforderungsanalyse → Pflichtenheft (nach 15 Tagen)
- Meilenstein 2: Abschluss Grobkonzept (nach 25 Tagen)
- Meilenstein 3: Abschluss Feinkonzept (nach 50 Tagen)
- Meilenstein 4: Abschluss Codierung + Komponententest (nach 90 Tagen)
- Meilenstein 5: Abschluss Systemtest (nach 110 Tagen)
- Zeitraum Meilenstein 3→4: nur 40 Tage Laufzeit, aber 124 Tage Arbeitsaufwand (Parallelität) → erhöhtes Terminrisiko
- Zwischenmessung in diesem Abschnitt: wöchentliche LOC-Messung, Planfortschritt: Codierung 2500 Zeilen/Woche, Test 400 Zeilen/Woche

**Kostenverlauf — nichtlinear:**
- Initialkosten zu Projektbeginn (Werkzeuge, Schulung, Einarbeitung)
- Analyse/Planungsphase: langsamerer Kostenanstieg (wenig Personal)
- Realisierungsphase: schnellerer Anstieg (höherer Personaleinsatz, Zulieferer, Prototypenbau)
- Endphase: Abflachung (Test/Fehlersuche kostet Laufzeit, weniger Personalzeit)
- Empfehlung: unterschiedliche Kostenbudgets (K1–K4) pro Phase, in gleichmäßigen Zeitabständen freigeben

**Beispiel 11.3 — CAD-Projekt Steinbachwerke:**
Personalkostenkalkulation (Kosten pro Personentag = 450 €/PT):

| Kostenfaktor | Kosten (€) | Anteil (%) |
|-------------|------------|------------|
| Direktes Entgelt (Bruttogehalt) | 5.000 | 100 |
| Direkte Nebenkosten (z.B. Urlaub) | 1.100 | 22 |
| Indirekte Nebenkosten (Arbeitgeberanteil Sozialversicherung) | 1.100 | 22 |
| Nebenkosten für nicht produktive Arbeiten | 1.000 | 20 |
| Zusatzkosten (Arbeitsplatz, Rechner: Miete, Abschreibung, Zinsen) | 800 | 16 |
| **Gesamtkosten pro Personenmonat (= 20 PT)** | **9.000** | **180** |

Weitere Kosten: Grundsoftware 25.000 €, zusätzliche Lizenzen 8.000 €, externer Spezialist Pilotbetrieb 1.000 €/Tag.

Phasen-Kostenbudgets (alle Budgets von Geschäftsleitung zu Phasenbeginn freizugeben):

| Projektphase | Eigenes Personal (PT / €) | Zukauf (€) | Fremdpersonal (PT / €) | Budget gesamt (€) |
|-------------|--------------------------|-----------|----------------------|------------------|
| Anforderungsspezifikation | 60 PT / 27.000 | — | — | 27.000 |
| Produktauswahl | 40 PT / 18.000 | — | — | 18.000 |
| Pilotbetrieb | 80 PT / 36.000 | 25.000 | 20 PT / 20.000 | 81.000 |
| Produkteinführung | 120 PT / 54.000 | 8.000 | 10 PT / 10.000 | 72.000 |
| **Summe** | **300 PT / 135.000** | **33.000** | **30 PT / 30.000** | **198.000** |

#### 11.1.4 Meilenstein-Trendanalyse (MTA)

Einzeldaten aus Arbeitspaketen liefern noch keinen Gesamtblick. Meilensteine ermöglichen übergeordnete Aussagen.

**Vorgehen:**
- Initiale Meilensteintermine aus der Planung
- In regelmäßigen Abständen (z.B. alle 2–4 Wochen) anhand aktueller Restaufwandsschätzungen korrigieren
- Grafische Darstellung: Vertikale Achse = geplante Meilensteintermine, horizontale Achse = tatsächliche Projektlaufzeit
- Diagonale Linie = aktueller Ist-Zeitpunkt
- Horizontale Trendlinie = Meilenstein plangemäß; Anstieg nach oben = Verzug; Abflachung nach unten = Verbesserung

**Beispiel 11.4 — MTA für kleines Projekt (4 Vorgänge A–D):**
Meilensteine: t1 = Abschluss A, t2 = Beginn D, tZ = Projektende.
Restaufwand-Aktualisierung alle 5 Tage.

Aktualisierungstabelle (Ist-Aufwand / Geschätzter Restaufwand):

| Vorgang | t=0 | t=5 | t=10 | t=15 | t=20 | t=25 | t=30 | t=35 | t=40 |
|---------|-----|-----|------|------|------|------|------|------|------|
| A | 0/5 | 5/2 | 8/0 | — | — | — | — | — | — |
| B | 0/10 | 0/10 | 2/9 | 7/6 | 12/2 | 14/0 | — | — | — |
| C | 0/12 | 5/8 | 10/5 | 15/2 | 20/1 | 21/0 | — | — | — |
| D | 0/15 | 0/15 | 0/15 | 0/15 | 0/15 | 3/12 | 8/7 | 13/3 | 17/0 |

Ergebnis: Meilenstein tZ verschob sich von 30 auf 39. Ist-Aufwand gesamt: 8+14+21+17 = 60 Tage; Plan: 5+10+12+15 = 42 Tage.

**Charakteristische MTA-Muster:**
- **Normal (Abb. 11.10a):** Trendlinien schwanken leicht um Horizontale → realistische Schätzung, kritische Überprüfung läuft
- **Anfangsverzug + Aufholen (Abb. 11.10b):** Gleichmäßige Verschiebung kurz nach Start (z.B. Aufgabenanalyse schwieriger), wird im Verlauf aufgeholt
- **Gleichmäßiger Anstieg (Abb. 11.11c):** Zu optimistische Anfangsschätzung → erheblicher Gesamtverzug wahrscheinlich → neue realistische Schätzung angebracht
- **Extremer Anstieg einzelner/mehrerer Linien (Abb. 11.11d):** Alarmsignal — massives Problem, ggf. Projektabbruch prüfen
- **Annähernde Trendlinien:** Eine Schätzung fehlerhaft; waghalsige Versprechungen = letzter Versuch Fehler zu kaschieren
- **Starke Schwankungen (Abb. 11.12e):** Große Unsicherheit bei Schätzung oder Durchführung → Ursachen klären
- **Glatte Linien mit plötzlichem Sprung (Abb. 11.12f):** Fehlende Aktualisierung zwischendurch → regelmäßige Schätzaktualisierung einfordern

**Anwendung:** MTA wird nach Abschluss der Projektplanung erstmalig erstellt; während der Durchführung regelmäßig in Besprechungen fortgeschrieben (Meilenstein-Verantwortliche erläutern aktualisierte Planwerte). Für Terminaspekte vergleichbar wirksam wie Earned-Value-Analyse für Kostenaspekte.

### 11.2 Projektlenkung

#### 11.2.1 Fortschrittssteuerung

**Umgang mit Planabweichungen — Abstufung nach Ausmaß:**
- **Kleine Abweichungen (wenige Prozent):** Kein Kommunikationsbedarf nach außen; durch Planungspuffer auffangbar; ständiges Kommunizieren wirkt wie Pedanterie, stumpft ab
- **Mittlere Abweichungen (~10 %):** Projektleiter kommuniziert ans Projektteam; Team als selbstorganisierendes System begreift und löst intern
- **Größere Abweichungen (deutlich >10 %):** Ernsthafte Krise; erfordert Krisenmanagement, Kommunikation nach außen, ggf. Einbindung des Auftraggebers

**Charakteristische Krisenzeichen:**
- Immer wieder verschobene Meilenstein- und AP-Termine
- Ständige Änderungen und neue Anforderungen des Auftraggebers
- Spürbar zunehmende Mitarbeiterfluktuation

**Reaktionsmöglichkeiten bei Rückstand (Abb. 11.13):**
- Verlauf I: Rückstand festgestellt
- Verlauf II: Plan an Realität anpassen (gedehnter Projektablauf) — wenn systematischer Planungsfehler vorliegt
- Verlauf III: Plankurve verschieben bei Einzeleffekten; weiteres Anwachsen des Rückstands verhindern
- Verlauf IV: Verlorene Zeit wiedergewinnen durch bessere Leistung, Überstunden oder Personalaufstockung (Mehrkosten beachten)

**Sonderfall Zeitvorteil:** Bei besserem Ist als Plan — als Puffer nutzen; bei größerem Vorsprung Plan revidieren, zunächst nur intern kommunizieren bis Vorteil sich als dauerhaft erweist.

**Krisenintervention:** Möglichst einmalig; vorher sorgfältige Analyse (Ursachen, Auswirkungen, Maßnahmen); vollständige Offenlegung der Fakten besser als schrittweise Wahrheitsoffenbarung. Mögliche Maßnahmen: Liefertermin verschieben, Rückstand aufholen auf Kosten höheren Aufwands, Lieferumfang reduzieren.

#### 11.2.2 Änderungsmanagement

Planabweichungen sind unvermeidlich (Fehler, Verzögerungen, neue Erkenntnisse). Kleinere lokale Abweichungen durch steuernde Maßnahmen behebbar. Gravierendere Probleme erfordern einen formellen Änderungsprozess, da Änderungen in vernetzten Projekten weitreichende Auswirkungen haben.

**Änderungsprozess (Abb. 11.14):**
1. Änderungsbedarf erfassen
2. Änderungsantrag bearbeiten (Gremium analysiert, bewertet, entscheidet)
3. Maßnahmen planen (welche Arbeiten, wer, Aufwand, Betroffene)
4. Maßnahmen überwachen (separat oder in Projektüberwachung integriert)
5. Claim Management

**Änderungsantrag (Abb. 11.15):**
- Antragsteller dokumentiert: Ursache (Problem/Fehler/neue Erkenntnis), notwendige Maßnahme, Auswirkung auf Projektziele
- Einheitliches Formular mit Genehmigung oder Ablehnung + Begründung
- Zuständiges Gremium (Change Board): regelmäßig oder bei Bedarf; Abwägung von Schwere, Aufwand, Projektauswirkung
- Kleine Änderungen müssen nicht mit Planrevision beantwortet werden — separate Überwachung möglich

**Änderungsregister:** Alle Anträge (auch abgelehnte) tabellarisch mit wichtigsten Informationen; verweist auf zugehörige Formulare.

**Claim Management:**
- Mehraufwand durch Auftraggeber-Anforderungen ist durch Angebot nicht abgedeckt → Ansprüche des Auftragnehmers
- Auch Lieferanten: Vertragsverletzungen → Ansprüche
- Zweck: Rentabilität des Projekts schützen

### 11.3 Projektabschluss

#### 11.3.1 Wozu ein Projektabschluss?

Projekte enden nicht automatisch mit der Abnahme. Ohne bewussten Abschluss entstehen pathologische Verläufe: Versickern, lautloses Sterben, kein klares Ende.

**Menschliche Tendenzen:**
- „Kleben am Projekt": Mitarbeiter zögern Rückkehr zur Linienabteilung hinaus → immer neue Restarbeiten entstehen; guter Projektleiter erkennt dies und unterstützt den Wechsel
- „Verdrücken aus dem Projekt": Frühzeitiges Absetzen aus Misstrauensgründen; bei berechtigten Zweifeln schwer aufzuhalten; bei unberechtigten: offene Aussprache

**Drei Prozessgruppen des Projektabschlusses (Abb. 11.16):**
1. Übergabe & Abnahme → Übergabeprotokoll, Abnahmebericht
2. Erkenntnissicherung → Lessons Learned, Abschlussbericht
3. Auflösung des Projekts → Ressourcenrückgabe, Gremienauflösung

Alle Abschlussaktivitäten sollen bereits im Projektplan berücksichtigt und personell zugeordnet werden.

#### 11.3.2 Abnahme des Projektergebnisses

**Rechtliche und kaufmännische Grundlage:**
- Auftragnehmer übergibt alle vereinbarten Leistungen; Auftraggeber prüft Vollständigkeit, Qualität, Zielerreichung
- Abnahme = Erklärung des Kunden, dass vereinbarte Bedingungen erfüllt sind → Zahlungen fällig, Gewährleistungsfrist + Verjährungsfrist für Mängelansprüche starten
- Abnahme schriftlich protokollieren und unterzeichnen

**Dokumente:**
- Übergabeprotokoll: Liste aller übergebenen Dokumente und Sachen + Übergabemodalitäten
- Abnahmebericht: durchgeführte Tests, erreichte Ziele, Abnahmebestätigung

**Nicht-Abnahme:** Auftraggeber muss bei nicht erfüllten Wesentlichkeitsbedingungen nicht abnehmen → Nachbesserungen nötig; Zahlung verzögert sich; ggf. wirtschaftlicher Schaden trotz technisch erfolgreichem Projekt.

**Abnahmevereinbarung:** Bereits im Auftrag/Pflichtenheft festlegen — Umfang, Kriterien und Bedingungen der Abnahme; kann Teilergebnisse mit Abschlagzahlungen definieren.

**Interne Projekte:** Auch hier Abnahme + Bericht notwendig, weniger formal, aber Konsens zwischen Unternehmensleitung und Projektleitung erforderlich.

**Beispiel 11.5 — Abnahmeprotokoll-Vorlage (drei Leistungstypen):**
- Typ 1: Leistung vollständig erbracht und funktionsfähig
- Typ 2: Leistung in wesentlichen Teilen nutzbar, weist Mängel auf (Nachbesserung erforderlich)
- Typ 3: Leistung nicht nutzbar, Mängel mit wirtschaftlich vertretbarem Aufwand nicht behebbar → führt zu Nicht-Abnahme; Verhandlung über Teil-Abnahme oder vollständige Nicht-Abnahme nötig
- Abnahmeerklärung von allen Beteiligten unterzeichnet

Kopf des Protokolls: Projektsstammdaten + Beschreibung der Abnahmemodalitäten (Testbedingungen im Pflichtenheft referenzierbar). Danach: Aufzählung der abgenommenen Leistungen mit Bemerkungen und Leistungstyp.

#### 11.3.3 Der richtige Zeitpunkt für den Projektabschluss

Auch nach Abnahme können Anforderungen offen bleiben:
- Mängelbeseitigung
- Fehlende Akzeptanz beim Anwender (trotz Abnahme durch Auftraggeber)
- Einarbeitungsbedarf, Anfangsmängel im Einsatz

**Nachbetreuung:** Anwenderunterstützung nach Abnahme + Mängelbeseitigung vereinbaren; Gewährleistung, Service- und Wartungsleistungen, Hotline bereits im Auftrag regeln.

**Provisorischer Projektabschluss:** Bei länger dauernden Nachbetreuungsarbeiten:
- Wesentliche Abschlussmaßnahmen durchführen (vorläufiger Abschlussbericht, Umfeldbeziehungen auflösen, Team weitgehend auflösen)
- Restarbeiten mit deutlich reduziertem Personal (ggf. Teilzeit) = „Nach-Projekt"
- Endgültiger Abschluss nach Gewährleistungsablauf

**Beispiel 11.6 — Software-Projekt Abschlussphase:**
- Schulung Anwender → Abnahme → geplante Mängelbeseitigung (Richtwert aus Erfahrung vorangegangener Projekte)
- „Provisional Acceptance" nach Mängelbeseitigung → 95 % der Auftragssumme fällig
- Intern: Dokumentation vervollständigen, Ressourcen zurückgeben, Projektanalyse, Team auflösen
- Gewährleistung + Service durch Entwicklungsabteilung übernommen
- „Final Acceptance" nach vereinbarter Servicezeit → restliche 5 % fällig (falls alle Mängel beseitigt)

#### 11.3.4 Erkenntnissicherung

Am Projektende sind Erfahrungen noch frisch und Ergebnisse vollständig vorliegend → optimaler Zeitpunkt für Analyse.

**Methoden/Bezeichnungen:** Projekt-Retrospektive, Project Review, Post-Mortem-Analyse — alle beschreiben dasselbe Kernziel: Erfahrungen analysieren und sichern für künftige Projekte.

**Inhalte der Erkenntnissicherung:**
- Funktions-, Kosten- und Zieltermine auf Einhaltung prüfen; Abweichungen und deren Ursachen untersuchen
- Fragen: Wo traten Abweichungen auf? Was waren die Ursachen? Wie hätten Probleme vermieden werden können?
- Projektplan-Soll vs. Ist-Ablauf vergleichen
- Erfahrungen des Teams: fachliche Probleme, Informationsdefizite, Kommunikationsprobleme, soziale Effekte, Terminüberschreitungen, Budgetüberschreitungen

**Verwertung:** Kennzahlen in Projektdatenbank ablegen; systematische Erkenntnisse → Änderungen oder Fortschreibung des Projektmanagement-Handbuchs.

**Kundenzufriedenheit:** Abnahme durch beauftragten Abnehmer ≠ Kundenzufriedenheit; separate Erhebung durch persönliche Gespräche oder standardisierte schriftliche Befragung (ermöglicht Projektvergleich).

**Mitarbeiterzufriedenheit:** Gleichwertig erfassen.

**Beispiel 11.7 — Standardisierter Mitarbeiterfragebogen:**
- 5 Fragen mit 5-stufiger Bewertungsskala zu Projektzufriedenheit
- 3 offene Fragen: besonders positiv/negativ aufgefallenes, Verbesserungsvorschläge
- Ergebnisse durch Projektleiter in persönlichem Gespräch vertieft

**Agile Erkenntnissicherung (Scrum):**
- Nicht erst am Projektende, sondern kontinuierlich
- Scrum Master pflegt Impediment Backlog (Probleme + Lösungen laufend)
- Kurzfristige Lösungen fließen direkt ins Daily Scrum ein
- Sprint Review (Produkt-Team + Product Owner): produktspezifische Erkenntnisse pro Sprint
- Sprint Retrospektive (mehrstündig, Team + Scrum Master): organisatorische Erfahrungen; Brainstorming → Analyse; Schwerpunkt auf Kommunikation intern + extern

#### 11.3.5 Projektauflösung

**Ablauf:**
- Abschlussbesprechung mit Auftraggeber-Vertretern, Projektmitarbeitern und Projektleiter: Erfahrungsaustausch zu Prozessen, Kommunikation, Problemlösung
- Projektgremien formal auflösen (in Abschlussbesprechung oder separatem Treffen mit gremieneigenen Erfahrungen)
- Ressourcen zurückgeben/verkaufen (Räume, Rechner, Maschinen, Werkzeuge)
- Claim Management abschließen: offene Ansprüche prüfen, Rechnungen, Außenstände, Verträge
- Projektkonten und Kostenstellen schließen
- Mitarbeiter an ursprüngliche Aufgaben zurückführen; vorbereitende Gespräche schon vor Projektende; Abschlussfeier als sozialen Abschluss nicht vergessen

---

### 12 Der Mensch im Projekt — Einführung (Seiten 295–301)

#### Lernziele Kapitel 12
- Berufliche und private Aktivitäten wie ein „Projekt im Kleinen" planen und steuern
- Sieben elementare Schritte effizienter Arbeitsorganisation beschreiben
- Stresssignale erkennen, Ursachen finden, Maßnahmen ergreifen
- Kompetenzen und Aufgaben der Projektleitung benennen
- Führungsstile im Spektrum autoritär–demokratisch einordnen
- Situative Reifegrad-Theorie: passenden Führungsstil je Qualifikationsniveau wählen
- Teambildungsprobleme erläutern und handhaben
- Persönlichkeitsprofile erfassen für Personalauswahl
- Reifungsphasen eines neu formierten Projektteams erkennen

#### 12.1 Selbstmanagement

##### 12.1.1 Aufgaben des Selbstmanagements

**Hierarchie der Planungsebenen:**
- Projektmanagement plant und steuert Arbeitspakete (typische Größe: 1–20 Personentage)
- Bearbeiter der Arbeitspakete sind für die Feinplanung ihrer einzelnen Arbeitsschritte selbst verantwortlich (Selbstmanagement)
- Auf AP-Ebene kommen Abhängigkeiten zwischen Arbeitsschritten hinzu sowie andere berufliche und private Aufgaben

**Definition:** Selbstmanagement = Planung und Steuerung persönlicher Tätigkeitsprozesse; umfasst auch die Abstimmung von Berufs- und Privatleben (methodische + emotionale Seite).

##### 12.1.2 Methoden des effizienten Arbeitens

Planungshorizont beim Selbstmanagement: ein Tag bis mehrere Tage.

**SPOC-Schema (Tab. 12.1) — vier Phasen:**

| Phase | Schritt | Inhalt |
|-------|---------|--------|
| study | 1. Analyse der Ausgangssituation | Was ist gegeben / passiert? |
| study | 2. Formulierung der Ziele | Was will/soll/muss ich erreichen? Priorität der Ziele (→ ABC-Analyse) |
| plan | 3. Erfassung notwendiger Aktivitäten | Was ist zu tun? (→ Todo-Liste); Zeitbedarf schätzen |
| plan | 4. Entscheidung über den Ablauf | Was ist wichtig? Was ist dringlich? Reihenfolge; feste Termine; Pufferzeiten freihalten |
| operate | 5. Ausführung der Aktivitäten | Probleme erkennen + beheben; Planänderungen wenn nötig; kein Perfektionismus |
| check | 6. Bewertung der Ergebnisse | Was erledigt? Was liegen geblieben? Ursachen für Abweichungen? Gelerntes? |

**Wichtige Planungsregeln:**
- ABC-Analyse für Zielpriorisierung: A = sehr wichtig, B = wichtig, C = weniger wichtig
- Zeitknappheit in Projekten ist kein Ausnahmezustand, sondern charakteristisches Merkmal
- Niemals 100 % der Zeit verplanen — ein Drittel der verfügbaren Zeit als Puffer für Unvorhergesehenes einhalten
- Kategorie C bei Zeitnot delegieren, verschieben oder streichen
- Persönliche Leistungskurve beachten: Tageshoch vormittags → wichtige/kreative Aufgaben; Nachmittag → Routinetätigkeiten
- Pareto-Prinzip: viele Arbeiten mit überschaubarem Aufwand gut (aber nicht perfekt) abschließen
- Fast fertige Arbeiten konsequent zu Ende bringen — offene Baustellen stapeln sich sonst

**Beispiel 12.1 — ALPEN-Methode (Tagesplanung):**
- **A**ufgaben auflisten: To-Do-Liste erstellen
- **L**änge schätzen: Aufwand für alle Aufgaben schätzen
- **P**ufferzeiten schaffen: nur ca. 60 % der Zeit verplanen
- **E**ntscheidung über Priorität: Wichtigkeit bestimmen
- **N**achkontrolle: Plan- und Istwerte der Aufgaben vergleichen
- Einmal täglich, schriftlich; bei Übung nur wenige Minuten

**Beispiel 12.2 — Getting Things Done (GTD) nach D. Allen:**
- Alle Arbeiten, Ideen, Notizen in Eingangsliste sammeln
- Regelmäßige Durcharbeitung: klassifizieren als „machbar" oder „nicht machbar"
- Machbar + ein Schritt + unter 2 Minuten → sofort erledigen
- Machbar + mehr Zeit → terminieren oder delegieren
- Machbar + mehrere Schritte → planen und terminieren
- Nicht machbar → Ablage-Liste (eventuell später machbar) oder Müll
- Hilfsmittel: Papierformulare oder spezielle Software

**Kernbotschaft:** Wichtiger als die Methode selbst ist, überhaupt eine Methode konsequent und regelmäßig einzusetzen.

##### 12.1.3 Umgang mit Stress

**Definition:** Stress entsteht wenn eine Anforderung das Normalmaß übersteigt und übliche Handlungsmuster nicht mehr greifen.

**Vier Stressor-Kategorien (Tab. 12.2):**
- Physische Stressoren: Lärm, Hitze, Platzmangel (durch Arbeitsumgebung verursacht)
- Kognitive Stressoren: hohe fachliche Anforderungen, Zeitdruck
- Soziale Stressoren: Konkurrenzdruck, Konflikte, Angriffe aus Zusammenarbeit
- Emotionale Stressoren: unechte Gefühle zeigen müssen, echte Gefühle unterdrücken

**Stress-Reaktionen:**
- Somatisch: vermehrte Adrenalinausschüttung, erhöhter Puls, Blutdruckanstieg, Erkrankungen
- Psychisch: Ärger, Frustration, Depression
- Reaktion ist subjektiv (von Person zu Person) und situativ (vom momentanen Zustand abhängig)

**Kurzzeitiger Stress:** Nicht grundsätzlich negativ — kann leistungsfördernd wirken. Problematisch bei: mehreren gleichzeitigen Stressoren, Dauerstress, mangelnder Bewältigung → Ermüdung, Konzentrationsmängel, Fehlerquote steigt, Resignation, soziales Fehlverhalten

**Maßnahmen zur Stressbewältigung:**

| Maßnahme | Erläuterung |
|----------|-------------|
| Physische Stressoren eliminieren | Externe Gestaltung der Arbeitsbedingungen |
| Handlungsspielraum und Entscheidungsfreiheit | Interne Unterstützung durch Projektorganisation |
| Körperlicher Ausgleich | Bewegung, Aktivität, Entspannung |
| Sozialer Ausgleich | Familie, Freunde, Freizeit |
| Perspektivwechsel | Herausforderung statt Belastung sehen; Stressresistenz aufbauen |
| Stress-Tagebuch und Aktionsplan | Systematische Analyse und Gegenstrategie |
| Soziale + emotionale Kompetenz | Kognitive Stressoren: Fachkenntnisse + effiziente Methoden; soziale: soziale Kompetenz; emotionale: emotionale Kompetenz |

**Projekts-spezifische Stressoren sind unvermeidlich:** fachlich anspruchsvolle Aufgaben, neuartige Probleme, enge Zusammenarbeit, Zeitdruck gehören zum Projektwesen. Daher bei Personalauswahl neben Fachqualifikation auch auf emotionale und soziale Kompetenzen achten.

**Hauptlast:** Stressbewältigung liegt beim Einzelnen. Arbeit nicht als absolut dominierend betrachten; Privatleben, Familie und Freunde als Gegengewicht sind wichtige Schutzfaktoren.
