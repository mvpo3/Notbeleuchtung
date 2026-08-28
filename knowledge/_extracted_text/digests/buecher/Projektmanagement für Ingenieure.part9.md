# Projektmanagement für Ingenieure — Teil 9
> Quelle: Projektmanagement für Ingenieure (buecher) · Seiten 361-400.

Dieser Teil behandelt drei thematische Schwerpunkte: erstens den Einsatz künstlicher Intelligenz im Projektmanagement (Abschluss von Kapitel 13), zweitens das vollständige Kapitel 14 über agiles Projektmanagement mit Scrum (Rollen, Backlogs, Sprint-Ablauf, Vergleich klassisch/agil/hybrid), und drittens den Beginn des Anhangs mit Formularliste, PM-Prozesslandkarte und Glossar.

## Inhalt

### KI im Projektmanagement — Technische Grundlagen (Kap. 13.4, Fortsetzung)

**Künstliche neuronale Netze (KNN)**
- KNN sind dem menschlichen Gehirn nachempfunden; bestehen aus Tausenden künstlicher Neuronen mit vielen einstellbaren Parametern
- Nutzbarkeit entsteht erst durch maschinelles Lernen: Training mit großen Datenmengen bis korrekte Ergebnisse erzielt werden
- Verknüpfungsregeln der Eingangsdaten werden nicht manuell kodiert, sondern durch Lernprozesse implizit erzeugt
- Aus einem allgemeinen KNN entsteht durch Training ein spezialisiertes Netz für konkrete Aufgaben (Gesichtserkennung, Sprachantworten, autonomes Fahren)

**Generative KI (genKI)**
- Teilgebiet der KI zur Erzeugung neuer Datenobjekte: Texte, Programme, Bilder, Videos
- Chatbots verwenden Sprachmodelle, die zu vorhandenen Begriffen oder Wortfolgen statistische Fortsetzungen erzeugen
- Wissensbasis der Chatbots = im Internet verfügbare Texte, auf denen sie trainiert wurden
- Chatbots können Fragen beantworten und echten Dialog führen, anders als Suchmaschinen

**Grundstruktur eines lernenden KI-Systems**
- Zwei Phasen: (1) Trainingsphase mit Trainingsdaten + Lernfunktion + Verknüpfungsfunktion → KI-Systemparameter werden eingestellt; (2) Betriebsphase mit Betriebsdaten als Eingabe → Ausgaben/Ergebnisse

---

### KI-Automatisierbarkeit von PM-Aufgaben (Kap. 13.4.2)

**Grundproblem KI in Projekten**
- KI benötigt große Datenmengen aus bekannten, ähnlichen Lösungen
- Projekte sind durch Einzigartigkeit und Neuartigkeit charakterisiert → vergleichbare historische Daten oft rar
- PM hingegen hat viele wiederkehrende Aufgaben → dort KI einsetzbar

**Schwach automatisierbare Phasen**
- Projektgründung und Projektabschluss: sehr individuell, wenig Automatisierungspotenzial

**Gut automatisierbare PM-Aufgaben — Projektplanung**
- Erstellung Produkt- und Projektstrukturplan
- Aufwands- und Kostenschätzung auf Basis ähnlicher Projekte
- Planung der logischen Reihenfolge der Arbeitspakete
- Bestimmung möglicher Anfangs- und Endtermine
- Ressourcenzuordnung zu Vorgängen
- Identifikation von Risikofaktoren und Erstellung Risikoregister

**Gut automatisierbare PM-Aufgaben — Projektsteuerung**
- Berichte formulieren
- Abfrage von Projektinformationen und Projektstatus
- Analyse des Projektfortschritts anhand von Arbeitsleistungsdaten
- Vorhersage über weiteren Projektverlauf durch Datenregression
- Dokumentation erstellen
- (Nicht automatisierbar: direkte Kommunikation mit Personen, nonverbale Kommunikation)

---

### KI im PM — Stand der Technik (Kap. 13.4.3)

**Drei Kategorien von KI-Werkzeugen im PM**

1. **KI in etablierten PM-Systemen**
   - KI-basierte Algorithmen in vorhandene PM-Software integriert
   - Unterstützen z.B. Ablauf-/Terminplanung, Berichtserstellung
   - Benutzeroberfläche bleibt weitgehend unverändert → hohe Akzeptanz
   - Basieren oft auf Datensammlungen aus vielen Projekten → hohe Passgenauigkeit

2. **Datenanalyse-Tools**
   - KI ist nur so gut wie ihre Datenbasis
   - Erfahrungen aus zurückliegenden Projekten werden in der Praxis zu selten systematisch gesammelt
   - Datenvorbereitung nötig: unvollständige, ungültige oder widersprüchliche Daten bereinigen, strukturieren
   - Aus strukturierter Datenbasis lassen sich Kennwerte, kausale Zusammenhänge, Planungen und Prognosen ableiten

3. **Chatbots**
   - Basieren auf Sprachmodellen, an Millionen Internet-Texten trainiert
   - Leistungsstark, können aber auch Unsinn produzieren
   - Allgemeines Internet-Wissen = Vorteil, aber für PM-spezifische Aufgaben ein Nachteil
   - Vorteilhafter Einsatz erfordert Training mit branchen-, firmen- und projektspezifischen Texten

---

### KI im PM — Schlussfolgerungen und Perspektiven (Kap. 13.4.4)

**Einschätzung der Entwicklung**
- Kurzfristige Wirkungen werden überschätzt: Euphorie weicht Ernüchterung, Effekte kommen langsamer und schwächer als prophezeit
- Langfristige Wirkungen werden unterschätzt: ähnliche Umwälzung wie Einführung von Computern und Bürosoftware

**Was KI im PM leisten kann**
- Routineaufgaben übernehmen: E-Mails, Berichte, Grafiken, Präsentationen
- Muster in großen Datenmengen erkennen → Risiken, Kosten-/Qualitätsprobleme frühzeitig identifizieren
- Komplexe Optimierungsaufgaben: Ablaufplanung, Terminierung, Ressourcenzuordnung — auch bei regelmäßig nötigen Planungsänderungen

**Was KI nicht kann (bisher)**
- Soft Skills der Projektleitung: Teamzusammenstellung, Teamführung, Konfliktlösung
- Nonverbale Kommunikation
- Kombination mehrerer Intelligenzformen gleichzeitig

**Voraussetzungen für nutzbringenden KI-Einsatz**
- Große Datenmenge aus vergangenen Projekten systematisch und sorgfältig sammeln
- Datenqualität und -form beachten
- Umgang mit KI-Tools erlernen (inkl. Prompt Engineering als eigenem Kompetenzfeld)
- Kenntnis der Grenzen und typischen Fehler der KI
- KI-Ergebnisse sind keine fertigen Produkte, sondern Vorleistungen die qualitätsgeprüft und weiterverarbeitet werden müssen

**Perspektive**
- KI übernimmt assistierende, keine ersetzende Rolle
- Projektleiter werden weniger als Zahlen-/Textproduzenten gebraucht, stärker als Team-Führungsexperten

---

### Kapitel 14: Agiles Projektmanagement — Überblick

**Entstehungshintergrund**
- Gegenbewegung zu umfangreichen Prozessmodellen klassischer PM-Standards
- Verlagerung Schwerpunkt: weg von Prozessen/Dokumenten/Plänen → hin zu Personen und Kundennutzen
- Entstanden primär in der Software-Entwicklung (junge Disziplin, hohe Komplexität, schwer konkretisierbare Anforderungen)

---

### Klassisches vs. agiles PM — Problemlage (Kap. 14.1.1)

**Häufigste Misserfolgsfaktoren in Projekten (GPM-Berichte, Standish Group Chaos-Reports)**

1. **Anforderungsprobleme** (meistgenannter Risikofaktor)
   - Auftraggeber wissen nicht genau was sie wollen
   - Anforderungen sind unvollständig und unklar
   - Änderungen im Projektverlauf → Mehraufwand und Konflikte

2. **Unzureichende Kommunikation**
   - Innerhalb des Teams
   - Mit anderen Abteilungen und Management
   - Fehlende Einbindung der Nutzer auf Auftraggeberseite

3. **Mangelnde Kompetenzen, Ressourcen und Planung**
   - Andere Abteilungen sehen Projektteam als Konkurrenz → unzureichende Unterstützung
   - Fehlende PM-Tool/Methoden-Erfahrung
   - Planung unzureichend oder wird im Projektverlauf vernachlässigt

**Reaktion der klassischen PM-Standards**
- ISO 21500, PMBOK, Prince 2, IPMA-ICB legen zahlreiche Prozesse und Dokumente fest
- Werden als zu umfangreich und aufwendig wahrgenommen (besonders in kleinen/mittleren Projekten)
- Dokumente werden als Pflichtübung behandelt → Nutzen sinkt weiter

**Agile Alternativen**
- Drastische Reduzierung des methodischen Aufwands
- Praktische Einschränkungen als Normalfall akzeptiert, nicht als Planungsfehler
- Feste Kosten und Termine werden zugunsten der Ergebnisqualität gelockert
- Bekanntester Vertreter: Scrum

---

### Agile Werte und Prinzipien (Kap. 14.1.2)

**Das agile Manifest — 4 Werte**

| Kürzel | Gewichtung |
|--------|-----------|
| I | Individuen und Interaktionen sind wichtiger als Prozesse und Werkzeuge |
| S | Funktionierende Software/Produkte sind wichtiger als umfassende Dokumentation |
| K | Zusammenarbeit mit dem Kunden ist wichtiger als Vertragsverhandlung |
| V | Reagieren auf Veränderung ist wichtiger als das Befolgen eines Plans |

Erläuterungen zu den Werten:
- Wert I: Keine Methodik ersetzt die Fähigkeiten der beteiligten Personen
- Wert S: Dokumentation ist Mittel zum Zweck, nicht Selbstzweck
- Wert K: Kunden sollen durchgängig eingebunden sein, nicht nur bei Anforderungsformulierung und Abnahme
- Wert V: Bei veränderlichen Anforderungen kann kein starrer Plan bestehen; flexible Reaktion wird höher gewichtet

**Die 12 Prinzipien des agilen Manifests** (Bezug zu den 4 Werten I/S/K/V)

| Nr. | Prinzip | Wertbezug |
|-----|---------|-----------|
| 1 | Kunden werden durch frühe und stetige Auslieferung zufriedengestellt | S, K |
| 2 | Anforderungsänderungen sind willkommen, da sie den Kundennutzen verbessern | K, V |
| 3 | Funktionierende Produktversionen werden innerhalb weniger Wochen/Monate ausgeliefert | S, K |
| 4 | Die Zusammenarbeit im Projektteam erfolgt täglich | I, S |
| 5 | Das Umfeld motiviert die Akteure durch Unterstützung und Vertrauen | I |
| 6 | Die beste Kommunikation sind persönliche Gespräche der Beteiligten | I, K |
| 7 | Funktionierende Produktversionen sind die beste Fortschrittsmessung | S |
| 8 | Nachhaltige Entwicklung ermöglicht konstant machbares Tempo auf unbegrenzte Zeit | S |
| 9 | Technische Exzellenz fördert die Agilität | S |
| 10 | Fokus liegt auf einfachen Lösungen und effizienten Arbeitsabläufen | V |
| 11 | Die besten Ergebnisse erzielen selbstorganisierende Teams | I |
| 12 | Regelmäßige Reflexion der eigenen Arbeit ermöglicht stetige Verbesserung | I, V |

---

### Lean-Prinzipien (Kap. 14.1.3)

**Ursprung**
- Toyota-Produktions-System (TPS) im japanischen Automobilbau
- Ziel: hohes Qualitätsniveau bei gleichzeitig kontrollierten/reduzierten Kosten
- Studie über TPS führte zur Zusammenfassung unter dem Begriff Lean Management
- Toyota wurde damit weltgrößter Automobilhersteller

**5 Grundprinzipien des Lean Management**

1. **Kundennutzen**: Der Nutzwert des Produkts für den Kunden hat bei allen Arbeiten und Entscheidungen höchste Priorität; Produkte ohne Nutzwert finden keine Käufer dauerhaft

2. **Wertschöpfungsprozesse**: Alle beteiligten Prozesse müssen ihren Anteil zum Wert liefern — Herstellprozesse, Entwicklungsprozesse, Unterstützungsprozesse und die gesamte Zulieferkette

3. **Prozessfluss**: Jeder Prozess soll kontinuierlichen Output liefern; unnötiges Puffern, Liegezeiten und Transportwege sind zu vermeiden

4. **Pull-Prinzip**: Aufträge werden nicht von oben in die Produktion gedrückt, sondern durch die Prozesskette gezogen; jeder Prozess reagiert auf Anforderung seines Nachfolgeprozesses → Teile werden nur in benötigter Menge produziert. Bekannteste Umsetzung: Kanban (Entnahme einer Menge löst Produktionsauftrag für vorgelagerten Prozess aus)

5. **Kontinuierliche Verbesserung**: Kein Prozess ist dauerhaft optimal; Verbesserung ist Daueraufgabe, nicht nur bei Problemauftreten; Verbesserungsmöglichkeiten aktiv suchen und systematisch umsetzen

**Methoden zur Umsetzung der Lean-Prinzipien**
- Just-in-Time, Kanban, One-Piece-Flow, Wertstromdesign
- Einige dieser Techniken wurden in agile PM-Modelle übernommen

---

### Scrum — Überblick (Kap. 14.1.4)

**Charakteristik**
- Derzeit bekanntestes agiles PM-Vorgehensmodell
- Entstand Anfang der 1990er Jahre in Software-Projekten
- Name „Scrum" (Rugby-Begriff für enges Gedränge) symbolisiert eng zusammenarbeitendes, selbstorganisierendes Team
- Übernahm Erfahrungen aus Lean Management zur kontinuierlichen Verbesserung

**Grundstruktur**
- Zyklischer Ablauf: Analyse, Entwurf, Realisierung und Test in sich wiederholenden Sprints
- Zu Projektbeginn: grobe Planung des Umfangs und Ablaufs, Anforderungen im Product Backlog erfasst
- Jeder Sprint dauert ca. 2–4 Wochen und liefert lauffähiges Produktinkrement
- Am Projektende: vollständiges Produkt

**3 Rollen in Scrum**
- Product Owner (Kundeninteressen-Vertreter)
- Team (5–10 Personen, eigenverantwortlich)
- Scrum Master (Einführung und Einhaltung der Scrum-Regeln)

---

### Aufbauorganisation mit Scrum-Rollen (Kap. 14.2)

**Aufgabenverteilung in Scrum**
- Keine klassische Projektleitungsrolle in Scrum
- Aufgaben der Projektleitung verteilt auf drei Rollen:
  - Scrum Master: Einhaltung organisatorischer Regeln
  - Product Owner: Interessenvertretung der Auftraggeber/Kunden, übergeordnete Leitungsaufgaben
  - Team: Detailplanung, Ablaufsteuerung, konkrete fachliche Entscheidungen (eigenverantwortlich)

**Product Owner (Kap. 14.2.1)**

Aufgaben:
- Schnittstelle zwischen Kunden und Projektteam
- Ideen, Wünsche und Vorstellungen der Kunden erfassen, formulieren, dokumentieren
- Team emotional auf Ziel ausrichten, Projektvision kommunizieren
- Tägliche, enge Kommunikation mit Team während Projektdurchführung
- Releaseplanung, -steuerung, -kontrolle

Befugnisse:
- Teamzusammenstellung
- Prioritätensetzung
- Alle wichtigen Entscheidungen im Projekt treffen

Anforderungen:
- Product Owner ist Produktmanager, Projektleiter, Chefarchitekt und Chief Engineer in einer Person
- Erfordert umfangreiche fachliche Fähigkeiten und vor allem Führungsfähigkeit
- Legt Ziele und Prioritäten von globalem Niveau aus fest; Detailformulierung wird ans Team delegiert

**Scrum Master (Kap. 14.2.2)**

Aufgaben:
- Scrum-Methodik einführen und umsetzen
- Organisatorische Hindernisse beseitigen (unklare Anforderungsdefinitionen, fehlende Prioritäten, unzureichende Kommunikation, mangelnde Ressourcen)
- Arbeit mit Team, Product Owner und Projektexternen
- Team in Leistungsphase führen, Teamkonflikte erkennen und lenken
- Leistungsprinzip etablieren und gleichzeitig Sicherheit vermitteln
- Ersten Sprint besonders unterstützen (hat entscheidende Wirkung auf Akzeptanz)

Befugnisse/Position:
- Weder Projektleiter noch Product Owner noch Teammitglied
- Verantwortlich für organisatorische und personelle Belange, nicht für fachliche Fragen

Voraussetzungen:
- Sehr gute Scrum-Kenntnisse (praktische Erfahrung als Teammitglied unerlässlich)
- Kooperationsfähigkeit und Konfliktresistenz
- Autorität durch umfangreiche Kompetenzen oder durch Vergabe durch das Team

**Team (Kap. 14.2.3)**

Aufgaben und Befugnisse (Tab. 14.5):
- Festlegung von Umfang und Inhalt der Sprints (autonome Entscheidung)
- Verantwortung für Einhaltung eigener Zusagen
- Organisation der teameigenen Aufgaben
- Lösung teaminterner Probleme
- Selbständige Organisation der Kooperation im Team

Merkmale:
- Interdisziplinäre Zusammensetzung (alle benötigten Kompetenzen abgedeckt)
- Kleine Teams (ca. 5–9 Personen); über 10 Personen → Kommunikationsaufwand steigt, Untergruppen entstehen
- Vollzeit-Mitarbeit; Teilzeit führt zu vielfältigen Problemen
- Räumliche und zeitliche Nähe der Teammitglieder

Arbeitsweise:
- Nicht mehr nach Command-and-Control-Prinzip
- Team als Ganzes übernimmt Aufgaben, trifft Entscheidungen, macht Zusagen
- Keine strenge Arbeitsteilung → keine Verantwortungsverteilung auf Einzelpersonen
- Probleme werden im Team gelöst, nicht nach außen getragen
- Team legt eigenständig Kooperationsregeln fest (Meetings, Entscheidungsfindung, Konfliktumgang)
- Autonomie des Teams ≠ Autonomie der Einzelmitglieder; Einzelne müssen zur Einheit zusammenwachsen

**Externe Rollen (Kap. 14.2.4)**
- Kunden (Customer): Auftraggeber; Product Owner ist ihre Schnittstelle, vertritt ihre Interessen
- Anwender (User): Nutzer des Produkts auf Kundenseite; beste Auskunftgeber für Anforderungen; wichtig bei Anforderungsbestimmung und Release-Tests
- Management: Zuständig für Projektrahmenbedingungen, materielle Ressourcen, strategische Unterstützung; muss im gleichen Unternehmen wie das Scrum-Team beheimatet sein

---

### Ablauf- und Informationsorganisation in Sprints (Kap. 14.3)

**Product Backlog — Anforderungserfassung (Kap. 14.3.1)**

Unterschied zu klassischer Anforderungserfassung:
- Klassisch: Lastenheft am Anfang vollständig, dann Pflichtenheft, dann Realisierung
- Scrum: Anforderungsänderungen sind Normalfall, nicht Ausnahme; Änderungsmanagement in iterativen Ablauf integriert

Charakteristik des Product Backlog:
- Geht von vagen Vorstellungen aus und konkretisiert schrittweise
- Formlose Notizen, handgeschriebene Karteikarten oder elektronische Entsprechungen (keine formalen papierbasierten Dokumente)
- Wird vom Product Owner erstellt (mit Beteiligung von Kunden, Anwendern, Management, Team)
- Anforderungs-Workshops mit allen relevanten Beteiligten als effektive Methode

**User Stories**
- Beschreiben aus Anwendersicht welche Funktionen genutzt werden sollen
- Benötigen: Benutzerrolle + auszuführende Funktion + ggf. Begründung des Zwecks
- Können abstrakt erfasst und später konkretisiert werden

Beispiel-Tabelle User Stories für Web-App (Tab. 14.6):

| Benutzerrolle | Ziel | Priorität | Story Points |
|---------------|------|-----------|-------------|
| Als Kunde | eigene Profilseite anlegen | C | 5 |
| Als Kunde | Profilseiten anderer Nutzer anschauen | C | 2 |
| Als Kunde | andere Nutzer als Kontakt hinzufügen | B | 3 |
| Als Admin | Kundenkonten anlegen und verwalten | A | 10 |
| Als Admin | Produktseiten anlegen, verändern und löschen | A | 8 |
| Als Kunde oder Nicht-Kunde | Produktseiten anschauen | A | 3 |

**Aufwandsschätzung mit Story Points**
- Absolute Aufwandsaussagen (Personentage) schwierig; relative Einordnung leichter
- Story Points ermöglichen relatives Vergleichen der Anforderungen untereinander
- Kein direkter Bezug zu Kosten/Terminen, aber Gespür für Aufwand

**Priorisierung der Anforderungen**
- Verantwortung: Product Owner auf Basis aller Beteiligten
- Kriterien: Nutzen (Wert für Anwender), Kosten (Realisierungsaufwand), Risiko (Machbarkeit)
- Skalen: Punkte 1–10, Prozentsätze, ABC-Analyse

**Ergebnis des Product Backlog**
- Enthält alle Anforderungen + Prioritäten + relative Aufwandsschätzungen
- Nicht zu detailliert; keine Realisierungsdetails oder Aktivitäten
- Ist Momentaufnahme; wird im Projektverlauf fortgeschrieben (ggf. versioniert)
- Unterschied zum Lastenheft: Product Backlog ist lebendes Dokument

---

**Grobplanung mit Releases (Kap. 14.3.2)**

**Releaseplanung**
- Sprint Backlog greift höchstpriore Anforderungen aus Product Backlog heraus
- Releaseplanung untersucht: Welche Anforderungen in welchen Sprints? Wie hoch die Leistung pro Sprint? Wie viele Sprints gesamt?
- Hochpriorisierte Anforderungen den frühen Sprints zuordnen ("do first things first")
- Ergebnis: Anzahl der Sprints, Zeitplan für einzelne Releases

**Velocity und Workload**
- Velocity = tatsächlich erreichte Story Points pro Zeiteinheit eines Sprints
- Workload = Verhältnis geplante Story Points zu tatsächlich erreichten Story Points
  - Workload = 1,0: Plan und Realität stimmen überein
  - Workload > 1,0: Plan zu optimistisch → Projekt dauert länger oder niedrig priorisierte Anforderungen werden gestrichen
  - Workload < 1,0: Kürzere Projektlaufzeit möglich
- Beobachtete Workload aus einem Sprint kann auf folgende Sprints hochgerechnet werden

**Rechenbeispiel 14.1 — Aufwandsschätzung und Workload**
- Skala 1–10 für Aufwandsschätzung
- Sprint 1 geplant: 500 Punkte; realisiert: 400 Punkte → Workload = 1,25 (500/400)
- Sprint 2 geplant: 600 Punkte; erwartet realisierbar: 480 Punkte (600/1,25)
- Team: 5 Mitglieder + Product Owner + Scrum Master = 7 Personen; Sprint = 20 Tage
- Erzielte Leistung rückblickend: 500 ÷ (7 × 20) = 3,57 Punkte je Personentag

**Sprint-Typen bei nichtlinearem Projektfortschritt**
- Scrum setzt linearen Fortschritt voraus, aber viele Projekte zeigen S-förmige Kurve (langsam → schnell → langsam)
- Explorations-Sprints zu Projektbeginn: kein oder geringes Produktinkrement; dienen Einarbeitung, Analyse, Wissensaufbau
- Release-Sprints: dienen vorwiegend Aufbereitung eines Produktstands zur Weitergabe an Kunden; entsprechen nicht dem Scrum-Konzept → möglichst vermeiden oder kurz halten

---

**Ablauf eines Sprints (Kap. 14.3.3)**

- Sprints dauern 2–4 Wochen, alle gleich lang, gleicher Aufbau
- Zeitlicher Schwerpunkt: Ausführung der Aufgaben
- Planungs- und Nachbereitungsaktivitäten: maximal 10 % der Gesamtdauer
  - Bei 20 Tagen Sprint: ca. 1 Tag Planung am Anfang + ca. 1 Tag Review/Retrospektive am Ende

**Sprint-Struktur**
1. Sprint-Vorbereitung + Sprint-Planung
2. Ausführungsphase (tägliche Intervalle mit Daily Scrum)
3. Sprint Review + Retrospektive

---

**Sprint-Vorbereitung und -Planung (Kap. 14.3.4)**

Sprint-Vorbereitung (Tab. 14.7):
- Anlass: Sprint-Anfang
- Dauer: 1–2 Stunden
- Teilnehmer: Team + Product Owner
- Zweck: Vorbereitung der Planung
- Ergebnisse: Sprint-Ziel, ausgewählte Backlog Items, Teamkapazitätsberechnung

Product Owner:
- Formuliert nachvollziehbares, knappes Sprint-Ziel (zur Orientierung während Sprint)
- Wählt Anforderungen aus Product Backlog nach Priorität aus
- Konkretisiert und detailliert relativ abstrakt gehaltene Anforderungen weiter

Team:
- Bestimmt Teamkapazität für Sprint (Personalstärke, Urlaubs-/Feiertage berücksichtigen)
- Personalstärke soll während Sprint konstant sein; personelle Änderungen nur an Sprintgrenzen

Sprint-Planung (Tab. 14.8):
- Anlass: Sprint-Anfang
- Dauer: 2 Stunden
- Teilnehmer: Team + Product Owner + Scrum Master
- Zweck: Planung des Arbeitsumfangs
- Ergebnis: Sprint Backlog (vollständige Liste aller im Sprint zu bearbeitenden Aufgaben)

Ablauf der Sprint-Planungssitzung:
- Product Owner stellt vorgesehene Anforderungen vor
- Team ermittelt benötigte Funktionen und daraus resultierende Detailaufgaben (Design, Implementierung, Test, Dokumentation)
- Team arbeitet nach Pull-Prinzip: wählt Anforderungen aus, kein "Pushen" durch Product Owner (Scrum Master verhindert dies)
- Timeboxing-Prinzip: Beginn und Dauer fix; Umfang wird bei zu großem Aufwand angepasst

Typische Fehler in der Planungssitzung:
- Rollenkompetenz überschreiten oder nicht ausfüllen
- Diskussionen über Entwurfs-/Programmierdetails
- Voreilige personelle Zuordnungen der Aufgaben
- Aufgabe des Scrum Masters: diese Fehler erkennen und verhindern

---

**Sprint-Ausführung (Kap. 14.3.5)**

Daily Scrum (Tab. 14.9):
- Anlass: Tagesanfang
- Dauer: strikt 15 Minuten
- Teilnehmer: Team + Scrum Master + (Product Owner); Externe können passiv zuhören
- Zweck: tägliche Bestandsaufnahme und Planung
- Ergebnis: aktualisierte Aufgabenliste (Task Board)
- Gleiche Zeit, gleicher Ort täglich; alle stehen im Kreis; keine Unterbrechungen erlaubt
- Jedes Teammitglied beantwortet: Was gestern erledigt? Welche Aufgabe heute? Gibt es Hindernisse?
- Probleme werden nur angesprochen, nicht in dieser Sitzung gelöst → danach separat behandeln

Task Board:
- Große Wandfläche in 4 Spalten eingeteilt:
  1. Anforderungen des Sprints (Selected Backlog Items)
  2. Zu erledigende Aufgaben
  3. In Arbeit (Work in Progress)
  4. Erledigt
- Ermöglicht auf einen Blick Überblick über Arbeitsstand im Sprint
- Aufgaben idealerweise so formuliert, dass sie innerhalb eines Tages erledigbar sind

Burndown Chart:
- Diagramm: täglich verbleibende Story Points über Zeit aufgetragen
- Ideal: lineare Kurve von Gesamtaufwand zu Null
- In der Realität: Abweichungen aufwärts und abwärts
- Mit Erläuterungen der Abweichungen und Reaktionen = Sprint-Burndown-Bericht

Impediment Backlog:
- Liste der Probleme/Hindernisse, die nicht sofort beseitigt werden können
- Verhindert Vergessen und Wiederholung gleicher Probleme
- Gibt Überblick über Störursachen und deren Status

---

**Sprint Review und Retrospektive (Kap. 14.3.6)**

Sprint Review (Tab. 14.10):
- Anlass: Sprint-Ende
- Dauer: 1–2 Stunden
- Teilnehmer: Team + Product Owner + Scrum Master; Management/Anwender optional
- Zweck: Vorstellung und Abnahme des Produktinkrements
- Ergebnis: Sprint-Ende-Bericht (des Product Owners)

Ablauf Sprint Review:
- Product Owner ruft Sprint-Ziel und geplante Anforderungen in Erinnerung
- Team stellt Produktinkrement vor (nicht als aufwendige Präsentation, sondern als aktuelle laufende Version auf Testrechner)
- Product Owner prüft aktiv ob zugesagte Funktionen vorhanden und funktionsfähig sind
- Nur vollständig erfüllte Anforderungen werden abgenommen
- Teilweise funktionierende oder nicht getestete Anforderungen werden nicht abgenommen (täuschen falschen Fortschritt vor)
- Fehler und Mängel müssen offen angesprochen werden (sachlich, ohne persönliche Vorwürfe)
- Fehler in Scrum = immer Fehler des Teams, nicht einzelner Mitglieder

Ergebnisse des Reviews:
- Unerledigte Anforderungen wandern als Erstes in nächsten Sprint
- Neue Anforderungen können hinzukommen → Product Backlog wird fortgeschrieben
- Personelle Veränderungen im Team möglich

Retrospektive (Tab. 14.11):
- Anlass: Sprint-Ende (unmittelbar nach Review)
- Dauer: 2–3 Stunden
- Teilnehmer: Team + Product Owner + Scrum Master
- Zweck: Analyse der Arbeitsabläufe im Sprint
- Ergebnisse: Lessons Learned, kurzer Maßnahmenkatalog

Ablauf Retrospektive:
- Anderer Raum, entspannte Atmosphäre, unüblicher Termin angestrebt → Lösung vom Projektalltag
- Jede Person nennt maximal 3 Probleme (keine Dominanz durch Einzelne)
- Probleme auf Karten; alle verteilen festgelegte Punktzahl auf Karten → wichtigste Probleme kristallisieren sich durch Visualisierung heraus
- Für wichtigste Probleme: systematische Ursachenanalyse (mehrere Iterationen, auch Ursachenketten)
- Maßnahmen: konkret, realistisch, wenige und wichtige (keine zu umfangreichen Kataloge)
- Maßnahmen werden in nächstem Sprint umgesetzt; in Planungssitzung eingeplant
- Prüfung ob zuvor ergriffene Maßnahmen umgesetzt wurden und wirkten (oft mehrere Sprints bis vollständige Wirkung)

---

### Klassisch, agil oder hybrid? (Kap. 14.4)

**Vergleich der Organisationsformen (Kap. 14.4.1)**

Klassische vs. agile Aufbau-, Ablauf- und Informationsorganisation (Tab. 14.12):

| Aspekt | Klassisch | Agil |
|--------|-----------|------|
| Rollen | Projektleitung, Projektteam, Lenkungsgremium, Verschiedene Externe | Scrum Master, Team, Product Owner, Verschiedene Externe |
| Aufbaustrukturen | Reine PO, Auftrags-PO, Matrix-PO, Linien-PO, Einfluss-PO | Reine PO |
| Ablaufstrukturen | Sequentiell (Wasserfall), Iterativ (Spiralmodell), Parallel (Simultaneous Engineering) | Sequentielle Sprints, Inkrementell (Produktinkremente), Parallele Aktivitäten im Sprint |
| Kommunikation | Formalisiert | Informell |
| Dokumentation | Lasten-/Pflichtenheft, Produkt- und Projektstrukturplan, Ablauf- und Terminpläne | Product Backlog, Sprint Backlogs, Task Board, Releaseplan |

Weitere Unterschiede bei Aufbauorganisation:
- Klassisch: Verschiedene Organisationsformen der Projekteinbindung (Matrix, Linie, Einfluss)
- Agil: Immer reine Projektorganisation; Owner/Master/Team fest im Projektteam
- Agile Qualifikationsanforderungen sehr hoch (eigenverantwortliches Arbeiten)
- Agile Teamgröße stark limitiert (5–10 Personen) → begrenzt auch Projektumfang

Ablauforganisation:
- Klassische Modelle kennen nicht nur Wasserfall: auch parallele und iterative Ansätze (Spiralmodell)
- Agil: Sprints sequentiell, Aktivitäten im Sprint parallel, Ergebnisse inkrementell
- Agile PM-Aufgaben werden vom Team selbst übernommen (keine separate PM-Instanz)

Informationsorganisation:
- Klassisch: Stark formalisiert, viele Berichte und Pläne ("plangetrieben", "dokumentenlastig")
- Agil: Wenige festgelegte Dokumente, spontane Kommunikation nach Bedarf, Notizen auf Karten an Pinnwänden; Meetings streng kurz gehalten

---

**Nutzen agiler Vorgehensweisen (Kap. 14.4.2)**

Stärken agiler Methoden:
- Umgang mit unvermeidlicher Anforderungsunsicherheit
- Product Owner vertritt Kundenanforderungen permanent während Projektverlauf
- Frühe und regelmäßige Auslieferung → Kunde kann Produktstatus validieren und Anforderungen konkretisieren

Voraussetzungen der Auftraggeber:
- Müssen flexibel sein bei Umfang und Zeitpunkt der Lieferung
- Projektauftrag eher als Rahmenvereinbarung oder Absichtserklärung (kein Festpreis/fixer Termin)
- Kunden müssen permanent in den Ablauf eingebunden sein

Produktvoraussetzungen für agiles Vorgehen:
- Produkt muss gut modularisierbar sein (Teilmengen realisierter Funktionen schon nutzbar)
- Typische agil realisierte Systeme: Web-Anwendungen mit wählbaren Funktionen
- Nicht geeignet: zeitkritische, sicherheitskritische oder hardwarenahe Systeme, stark vernetzte Software, Produkte die sich nicht in entkoppelte Teilprodukte zerlegen lassen

Teamvoraussetzungen:
- Kleine Teams: ca. 5–10 Personen, täglich in räumlicher Nähe
- Typische agile Projektgröße: 2,5 bis 20 Personenjahre (0,5–2 Jahre Laufzeit × 5–10 Personen)
- Nicht geeignet für: sehr große Teams, verteilt arbeitende Teams, Teams mit geringer Projekterfahrung

Grenzen agiler Projekte:
- Strikte Vorgaben für Funktionsumfang, fixe Termine, eng begrenzte Kostenrahmen → Schwächen bei agilen Projekten
- Großprojekte mit vielen räumlich verteilten Beteiligten → klassische Modelle notwendig

**Merkmale klassischer vs. agiler PM-Modelle (Tab. 14.13)**

| Merkmal | Klassisch | Agil |
|---------|-----------|------|
| Anforderungen | Fest, sicher, bekannt | Veränderlich, unsicher, teilweise unklar |
| Projektteam | Sehr unterschiedliche Teamgrößen | Ca. 5–10 Personen |
| Unternehmenskopplung | Oft eng | Entkopplung vom Unternehmen |
| Arbeitsweise | Eng an Pläne gebunden | Eigenverantwortlich |
| Kundenbindung | Lose, nur am Anfang und Ende | Enge Einbindung |
| Auslieferung | Nur am Ende | Früh und regelmäßig |

---

**Hybride Vorgehensweisen (Kap. 14.4.3)**

Grundprinzip:
- Klassisch und agil sind keine unvereinbaren Gegensätze, sondern können kombiniert werden
- Aber: Agilität erfordert bestimmte Organisationsregeln; ein Projekt kann nicht "ein bisschen agil" sein

Zwei Formen hybrider PM-Modelle:

1. **Sequentiell hybrid**
   - Frühe Phasen (Analyse, Entwurf) werden klassisch durchgeführt (wegen Wechselwirkungen des Gesamtsystems)
   - Realisierungsphase wird, wenn Voraussetzungen erfüllt, agil durchgeführt
   - Beispiel: bei komplexem elektrischen Gerät muss Elektronik grob bekannt sein bevor Gehäuse und Software entworfen werden → Analyse/Entwurf klassisch, Realisierung agil möglich
   - Gilt ähnlich für umfangreiche Bauprojekte (viele Details müssen vor Baubeginn feststehen)

2. **Parallel hybrid**
   - Gesamtprojekt zu groß für agiles Vorgehen
   - Bestimmte Teilprojekte werden agil, andere klassisch durchgeführt
   - Beispiel: mechanische und elektronische Konstruktion klassisch, Software-Entwicklung agil
   - Vorteil: begrenzte agile Teamgröße wird nicht zum Hindernis

Punktuelle Übernahme von Methoden der anderen "Welt":
- In klassischen Projekten z.B.: tägliches kurzes Meeting im Daily-Scrum-Stil oder Burndown-Chart statt Fortschrittskurve
- In agilen Projekten z.B.: Projektdefinition erstellen oder Produktstrukturplan verwenden
- Solche punktuellen Maßnahmen rechtfertigen allein keine Bezeichnung als "hybrides PM-Modell"

Fazit:
- Zunehmend werden Stärken beider "Welten" anerkannt
- Ziel: PM als flexibler Werkzeugkasten, aus dem für jedes Projekt individuell die passendsten Vorgehensweisen, Methoden und Dokumente ausgewählt werden

---

### Anhang A1 — Formulare (Seite 379)

Verfügbare Standardformulare des Buches (als Word-Vorlagen auf Website des Autors):

| Formular | Verwendungszweck | Buchverweis |
|----------|-----------------|-------------|
| Abnahmeprotokoll | Abnahme des Projekts durch Auftraggeber | Abb. 11.19–11.21 |
| Änderungsantrag | Änderungsantrag für die Projektsteuerung | Abb. 11.15 |
| AP-Beschreibung | Beschreibung eines Arbeitspakets | Abb. 5.13 |
| Besprechungsbericht | Dokumentation der Ergebnisse einer Besprechung | Abb. 4.16 |
| Mitarbeiterzufriedenheit | Abfrage der Mitarbeiterzufriedenheit | Abb. 11.23 |
| Projektdefinition | Projektdefinition (Projekt-"Steckbrief") | Abb. 3.2 |
| Projektdokument | Allgemeines Projektdokument | — |
| Risikoanalyse | Analyseergebnis für je einen Risikofaktor | Abb. 8.5 |
| Statusbericht | Dokumentation des Projektstatus | Abb. 11.2 |
| To-do-Liste | Liste für kleinere Arbeiten, die kein Arbeitspaket sind | — |

---

### Anhang A2 — Landkarte der PM-Prozesse und -Dokumente (Seite 381)

Strukturelle Übersicht aller PM-Prozesse gegliedert nach Projektphasen:

**Projektgründung**
- Projekt initiieren
- Anforderungen entwickeln (Lastenheft, Ausschreibung)
- Aufbauorganisation definieren (Projektstukturdiagramm, Stakeholder-Register, Rollenbeschreibung, PM-Handbuch)
- Ablauforganisation festlegen
- Kommunikation planen (Kommunikationsplan)

**Planung (Ablauf, Qualität, Kosten, Risiken)**
- ProdSP erstellen
- ProjSP erstellen
- Vorgänge festlegen (Vorgangsliste, AP-Beschreibungen)
- Vorgangsfolge festlegen
- Vorgangsdauer schätzen (Schätzwerte)
- Terminplan entwickeln (Vorgangs-Netzplan, Projektphasen, Meilensteine, Projekt-Terminplan)
- Qualitätsplanung (QM-Plan, Q-Plan)
- Risikoidentifikation
- Risikobewertung (Risiko-Register mit Ereignissen, Wirkung, Wahrscheinlichkeit, Schaden)
- Risikobehandlung (Risiko-Indikatoren, Maßnahmen)
- Kostenplanung/-schätzung (Kosten-Schätzwerte, Plan-Verlauf, Budgets)
- Ressourcen-Register

**Projektüberwachung**
- Fortschrittssteuerung (Fortschrittsdaten, Arbeitsleistungsinformation)
- Änderungsmanagement (Änderungsanträge)
- Qualitätslenkung
- Risikoüberwachung
- Kostenüberwachung (Istkosten)
- Korrigierende Maßnahmen

**Projektabschluss**
- Abnahme des Ergebnisses/Liefergegenstände
- Angebot kalkulieren (Angebot, Auftrag, Pflichtenheft)

---

### Anhang A3 — Glossar (Auswahl, Seiten 383–384)

Begriffsdefinitionen:

- **Ablauf**: Besteht aus mehreren aufeinanderfolgenden Arbeitsschritten
- **Ablaufplan**: Spezieller Netzplan, der den Ablauf eines Projekts als Netz von Vorgängen und Ereignissen beschreibt
- **Ablaufplan, terminierter**: Ordnet die Ereignisse im Ablauf eines Projekts festen Terminen zu
- **Ablaufplanung**: Festlegung der Reihenfolge der Arbeitspakete eines Projekts
- **Abnahme**: Bestätigung eines Auftragnehmers über vollständige Erbringung einer Lieferung/Leistung gemäß Auftrag; juristisch belastbares Gegenstück zum Projektauftrag; schriftlich als Abnahmeprotokoll dokumentieren
- **Abschlussbericht**: Fasst Verlauf, Ergebnisse und Erfahrungen eines Projekts am Ende zusammen
- **Änderungsmanagement**: Erfassung, Steuerung und Dokumentation notwendiger Änderungen in einem Prozess
- **Angebot**: Hält Kosten, Termine und Bedingungen der Lieferungen/Leistungen verbindlich oder unverbindlich fest
- **Anordnungsbeziehung**: Logische Abhängigkeit zwischen zwei Vorgängen; Typen: Anfangsfolge (Anfang-Anfang), Normalfolge (Ende-Anfang), Sprungfolge (Anfang-Ende), Endefolge (Ende-Ende)
- **Arbeitspaket**: Aus funktionell und zeitlich eng zusammengehörenden Arbeiten, die von einer Person ausgeführt werden; kleinste betrachtete Aktivitätseinheit im PM
- **Aufgabe**: Ein System aus einem Anfangs- in einen gewünschten Zielzustand bringen; wird zur Problemstellung wenn ein Hindernis den Weg erschwert
- **Auftrag**: Vertragliche Vereinbarung über zu erbringende Lieferung oder Leistung zwischen Auftraggeber und Auftragnehmer
- **Aufwandsschätzung**: Schätzung des Aufwands für Arbeitspakete zur Kostenermittlung und Zeitplanung
- **Balkendiagramm**: Grafische Darstellung mit Balkenlänge als Symbol für reale Ausdehnungen; Gantt-Diagramme sind Balkendiagramme für Prozesse
- **Bericht**: Dokument, das anlässlich eines bestimmten Ereignisses (Besprechung, Meilenstein) verfasst wird
- **Beziehungsdiagramm**: Stellt Wechselwirkungen zwischen Größen eines Sachverhalts als grafisches Netz dar
- **Bottom-Up-Vorgehensweise**: Aufgabenlösung durch zunächst spezielle Teillösungen, die schrittweise zur Gesamtlösung zusammengesetzt werden
- **Brainstorming**: Gruppen-Sitzung zur Erzeugung möglichst vieler Ideen; Ideen dürfen aufgegriffen und weiterentwickelt, aber nicht bewertet oder kritisiert werden
- **Budget**: Bestimmte zur Verfügung gestellte (finanzielle) Ressourcenmenge; zeitlicher Verlauf = zeitabhängiger Kostenplan
- **Burndown Chart**: Zeitdiagramm zur Visualisierung des Projektfortschritts; über Zeitachse werden noch zu bearbeitende Story Points dargestellt
- **Daily Scrum**: Kurze tägliche Besprechung über am Vortag erreichte Ergebnisse und am aktuellen Tag zu bearbeitende Tasks
- **Definition of Done (DoD)**: Checkliste mit Beschreibung wann eine geforderte Arbeit als erledigt gilt; sorgt für einheitliches Verständnis von "erledigt" bei allen Beteiligten
- **Delphi-Methode**: Schätzwert-Erstellung durch mehrere Experten in drei Schritten: verdeckt schätzen → Ergebnisse veröffentlichen → endgültig festlegen
- **Dokument**: Informationseinheit, die mehrere Informationen zu einer physischen Einheit (Papier oder elektronisch) zusammenfasst
- **Earned-Value-Analyse**: Methode des Kostencontrollings; analysiert zu verschiedenen Zeitpunkten entstandene Kosten und Wert der geschaffenen Leistungen; Vergleich mit Planwerten liefert Status- und Vorhersage-Kennzahlen
- **Einsatzmittel (Ressourcen)**: Sachmittel (nach DIN 69902 auch Personen), die zur Durchführung von Arbeitspaketen benötigt werden
- **Element**: Nicht weiter zerlegbares Objekt
