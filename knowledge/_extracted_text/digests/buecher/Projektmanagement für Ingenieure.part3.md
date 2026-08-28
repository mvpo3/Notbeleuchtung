# Projektmanagement für Ingenieure — Teil 3
> Quelle: Projektmanagement für Ingenieure (buecher) · Seiten 121-160.

Dieser Teil schließt Kapitel 4 (Projektorganisation) ab — Ablauforganisation, Ablaufmodelle, Informationsmanagement und das PM-Handbuch — und beginnt Kapitel 5 (Strukturplanung) mit Produkt- und Projektstrukturplanung.

## Inhalt

### 4.2.1 Gliederungstiefe bei Projekten (Teilprojekte und Arbeitspakete)

- Projekte werden je nach Größe auf mehreren Ebenen untergliedert:

| Projektgröße | Umfang | Untergliederung |
|---|---|---|
| Groß-Projekt | 50–500 Personenjahre (PJ) | Teilprojekte → Teilprojekte → Arbeitspakete |
| Mittleres Projekt | 5–50 PJ | Teilprojekte → Arbeitspakete |
| Kleines Projekt | 0,5–5 PJ | Teilprojekte |
| Teilprojekt | 0,5–5 Personenmonate (PM) | Arbeitspakete (1–10 PT) |

- Neben der inhaltlichen (objektorientierten) Untergliederung ist auch eine ablauforientierte Bildung von Teilprojekten möglich: z.B. alle Entwurfsarbeiten (Gehäuse, Schaltung, Programm) bilden das Teilprojekt „Entwurf", alle Testarbeiten das Teilprojekt „Test".
- Ein Teilprojekt braucht klaren Start- und Endtermin sowie ein prüfbares Ergebnis. Anders als ein Arbeitspaket erfordert ein Teilprojekt während seiner gesamten Laufzeit PM-Aktivitäten: Planung, Überwachung, Steuerung.
- Typischer Umfang eines Teilprojekts: rund 0,5–5 Personenmonate, enthält durchschnittlich etwa 10 Arbeitspakete.
- Bei noch größeren Projekten können Teilprojekte auf mehreren Ebenen zusammengefasst werden, bevor man auf Gesamtprojektebene gelangt.

### 4.2.2 Phasen und Meilensteine

- Neben der statischen Strukturierung in Teilprojekte ist der Ablauf als Prozesskette von Bedeutung. Teilprojekte/Arbeitspakete können sequentiell oder parallel bearbeitet werden; parallelisiertes Arbeiten verkürzt die Durchlaufzeit.
- Jeder Prozess hat mindestens einen Start- und Endtermin. Zusätzlich werden übergeordnete Termine definiert, an denen wesentliche Projektphasen abgeschlossen werden: diese heißen **Meilensteine**.
- Eine **Projektphase** ist ein zeitlich abgegrenzter Teil des Projekts. Sie kann ein oder mehrere Teilprojekte umfassen.
- Ein **Meilenstein** gilt als erreicht, wenn alle Ergebnisse der vorangehenden Phase vorliegen. Start- und Endpunkt einer Projektphase stellen Meilensteine dar.
- Jede Projektphase muss vollständig abgeschlossen sein, bevor die nächste beginnen darf. Das ermöglicht Zwischenergebnisse schon früh zu überprüfen, nicht erst am Projektende.
- Wenn eine Phase ihren Meilenstein nicht fristgemäß erreicht, sind mögliche Reaktionen: Verlängerung der Phase (mit entsprechender Verschiebung aller Folgemeilensteine und des Endtermins) oder im Extremfall Projektabbruch.
- Ohne Phasengrenzen werden Überprüfungen und Entscheidungen oft aufgeschoben — typische Folgen: ergebnisloses Beenden von Arbeitspaketen, drastische Terminüberschreitungen, Scheitern des Projekts.

#### Beispiel 4.9: HOAI-Leistungsphasen (Bauprojekte)

Die HOAI unterteilt Architekten- und Ingenieurleistungen in 9 aufeinanderfolgende Phasen mit erfahrungsgemäßen Aufwandsanteilen:

| Nr. | Phase | Aufwand (%) |
|---|---|---|
| 1 | Grundlagenermittlung | 3 |
| 2 | Vorplanung | 7 |
| 3 | Entwurfsplanung | 11 |
| 4 | Genehmigungsplanung | 6 |
| 5 | Ausführungsplanung | 25 |
| 6 | Vorbereitung der Vergabe | 10 |
| 7 | Mitwirkung bei der Vergabe | 4 |
| 8 | Objektüberwachung (Bauleitung) | 31 |
| 9 | Dokumentation | 3 |

- In Phase 1 werden Bauherrenwünsche und Ist-Zustand erfasst. Phasen 2–4 sind drei Entwurfsphasen (Konzept + Kostenschätzung → Detailplanung + Kostenrechnung → Genehmigungsunterlagen). Phasen 5–7 umfassen Ausführungsplanung und Vergabe. Phase 8 ist die eigentliche Bauleitung (höchster Aufwandsanteil: 31 %). Phase 9 schließt mit der Dokumentation ab.

### 4.2.3 Standard-Ablaufstrukturen

- Ausgangspunkt: Projekt als systematischer Problemlösungsprozess mit den vier Schritten **Problemanalyse → Lösungsentwurf → Realisierung → Validierung**.
  - Problemanalyse: Input ist die Problembeschreibung (oft unspezifisch/lückenhaft); Output ist eine möglichst vollständige, widerspruchsfreie Aufgabenbeschreibung.
  - Lösungsentwurf: nicht sofort auf eine einzige Lösung konzentrieren, sondern mehrere Varianten ausarbeiten, vergleichen, beste auswählen und als detaillierten Plan ausformulieren.
  - Realisierung: Plan wird in reale Lösung umgesetzt.
  - Validierung: Prüfung ob Lösung das Problem tatsächlich löst, Randbedingungen eingehalten sind, Gütekriterium optimiert wurde.

#### Wasserfallmodell

- Jeder der vier Schritte bildet ein eigenes Teilprojekt und eine eigene Projektphase; Abfolge ist rein sequentiell, Kaskadenform.
- Vorteile: einfacher, klarer Aufbau; gut für Projektkontrolle geeignet.
- Nachteile: hohe Durchlaufzeit; in der Praxis selten in Reinform umsetzbar (Analysen können nicht immer vollständig abgeschlossen werden bevor Entwurf beginnt; neue Probleme tauchen beim Entwurf auf usw.).

#### Simultaneous Engineering (SE)

- Auch als Concurrent Engineering oder Integrierte Produktentwicklung bezeichnet.
- Kerngedanke: Prozesse so weit wie möglich parallelisieren um Durchlaufzeit zu minimieren.
- Sobald erste Analyseergebnisse vorliegen, beginnt bereits der Entwurf; Realisierung und Validierung starten ebenfalls so früh wie möglich.
- „Over-the-wall"-Engineering (sequentielle Übergaben ohne Rückkopplung) wird als Ursache vieler Probleme erkannt.
- Vollständige Parallelisierung nicht erreichbar — es gibt einen möglichst kleinen zeitlichen Versatz.
- Nachteile: höheres Risiko (frühe Fehler fließen in viele Folgearbeiten ein), gravierender organisatorischer Umbau notwendig, deutlich höherer Kommunikationsaufwand.
- Lohn: minimale Projektlaufzeit.

#### Beispiel 4.10: Sequentielle vs. parallele Bearbeitung

- Kleines Projekt mit 4 Phasen (Analyse, Entwurf, Realisierung, Validierung), je unterteilt in Grob- und Fein-Phase → 8 Phasen gesamt.
- Rein sequentiell: Durchlaufzeit 63 Arbeitstage.
- Mit SE (kritische Grob-Phasen zuerst, dann Überlappung mit Fein-Phasen der nächsten Phase): Durchlaufzeit reduziert auf 44 Arbeitstage.

#### Beispiel 4.11: Maschinenterminal — Simultaneous Engineering

- Entwicklungsziel: Serienreife in maximal 8 Monaten (wegen auslaufender Zuliefererverträge).
- Vorgehen: Zunächst Grob-Analyse und Grob-Entwurf mit den wesentlichen Entwurfsentscheidungen (Plattform x86, DOS-Betriebssystem, PC/104-Format für CPU-Module, Kunststoffgehäuse, externer Stecker-Netzadapter, Platzbedarf Elektronik ca. 18 × 25 × 5 cm).
- Danach parallele Bearbeitung der Teilgebiete: mechanische Arbeiten (Gehäuse, Einbaugeräte, Tastatur, Stecker, Zubehör), elektrische Arbeiten (Schaltungsentwurf, Layout, Test), Softwarearbeiten (Protokolle, Datensicherung, Benutzerdialog, Programmierung, Test).

### 4.2.4 Varianten von Ablaufstrukturen

- Wasserfallmodell (sequentiell, einmalig) und SE (parallel, einmalig) sind Extremformen. Dazwischen gibt es iterative Ablaufmodelle basierend auf der Unterteilung des Projektergebnisses in mehrere Teile.

**Drei Produktmodelle für iterative Gliederung:**

- **Komponentenmodell**: Produkt wird in gleichwertige, unabhängige Module zerlegt; jedes kann separat realisiert und am Ende zusammengesetzt werden (Beispiel: modularer Fahrzeugbaukasten).
- **Schichtenmodell**: Produkt aus aufeinander aufbauenden Schichten; jede Schicht greift auf darunter liegende zurück und stellt Funktionen für darüber liegende bereit (Anwendung: Software, Kommunikationssysteme, Rechnersysteme).
- **Prototypenmodell**: Produkt in mehreren Konkretisierungsstufen; beginnt mit abstraktem, einfachem Prototyp der einen wichtigen Aspekt zeigt; schrittweise Verfeinerung bis zum vollständigen Ergebnis. Typisch 2–3 Iterationen.

**Vier Ablaufvarianten bei iterativem Vorgehen (Kombination Iterationsreihenfolge × Teilprozesskettung):**

| Kürzel | Iterationen | Teilprozesse | Beispiel |
|---|---|---|---|
| iss | sequentiell | sequentiell | Spiralmodell |
| ips | sequentiell | parallel | Scrum |
| isp | überlappend | sequentiell | — |
| ipp | überlappend | parallel | max. Parallelisierung |

- iss erhöht nicht die Durchlaufzeit gegenüber Wasserfall, aber Fehler werden früher entdeckt und überprüfbare Zwischenergebnisse liegen früher vor.
- ips (Scrum): deutliche Laufzeitverkürzung bei noch überschaubarer Komplexität durch klar abgegrenzte Iterationsphasen.
- ipp: kürzeste Durchlaufzeit, höchste Komplexität.

#### Spiralmodell (Boehm 1988)

- Basiert auf Pareto-Prinzip: in jeder Phase gibt es kritische Entscheidungsarbeiten mit weitreichenden Konsequenzen und weniger kritische Fleißarbeiten.
- Vollständiger Zyklus wird zuerst für die kritischen Arbeiten durchlaufen, danach erst die Fleißarbeiten.
- Fehlerrisiko sinkt, da fundamentale Fehler früh aufgedeckt werden bevor viel Aufwand in Details geflossen ist.
- Projektlaufzeit ändert sich gegenüber Wasserfall nicht (nur Reihenfolge der Arbeiten anders).
- Darstellung spiralförmig nach außen: jede Umdrehung = ein vollständiger Teilablauf.

#### Beispiel 4.12: DeLorean DMC-12

- Entwicklungsprojekt über fast 7 Jahre (ca. 1974–1981) in 6 Iterationen:
  1. Grundkonzept + Versuchsfahrzeug „Red Rocket" (Fiat X1/9-Basis, Ford-Motor, Borg-Warner-Getriebe) + Holzmodell 1:1 (Design-Studie)
  2. Erster DMC-12-Prototyp (Citroen-Motor; zu schwach)
  3. Zweiter Prototyp (Mittelmotor-Konzept aufgegeben → Heckantrieb)
  4. Lotus-Kooperation, viele ursprüngliche Ideen verworfen; Chefentwickler schied aus
  5. Pre-Production-Car
  6. Serienproduktion (8.583 Fahrzeuge hergestellt, danach Qualitätsmängel → Firma nach 2 Jahren eingestellt; Bekanntheit durch „Zurück in die Zukunft")
- Vorteil Prototypenmodell: kritische Fragen werden zuerst überprüft, Fehler früh erkannt und mit überschaubarem Aufwand behoben; bei grundlegenden Problemen kann Projekt früh abgebrochen werden.

**Vergleich der Grundmodelle:**

| Kriterium | Wasserfallmodell | Spiralmodell | Scrum | Simultaneous Eng. |
|---|---|---|---|---|
| Ablauf | sequentiell | iterativ | iterativ | parallel |
| Phasengrenzen | ausgeprägt | schwächer | schwächer | fehlen |
| Durchlaufzeit | lang | lang | kürzer | kurz |
| Fehlererkennung | spät | früher | früher | spät |
| Planungs-/Kommunikationsaufwand | gering | mittel | niedrig | hoch |

### 4.3 Organisation der Informationsflüsse

- Im Projektverlauf fallen sehr viele Informationen unterschiedlicher Bedeutung an. Nicht alle sind projektrelevant.
- Aufgabe des **Informationsmanagements**: relevante Informationen erfassen, speichern und zugänglich machen; irrelevante ignorieren.
- Regeln für Erfassung, Kommunikation und Speicherung sollten vor Projektbeginn festgelegt werden.

### 4.3.1 Information, Kommunikation, Dokumentation

- Information (theoretisch): Kenntnisgewinn über einen Sachverhalt. Informationsgehalt ist umso größer, je seltener/unwahrscheinlicher ein Ereignis ist (Beispiel: „Fußballmannschaft gewonnen" = 1 Bit; „Projektauftrag erhalten" = 1 Bit — gleicher theoretischer Informationsgehalt).
- Aus praktischer Sicht muss neben dem Informationsgehalt auch die **Relevanz** für das Projekt bewertet werden.
- Neu entstehende Informationen (z.B. Lieferungsstorno per E-Mail, telefonische Krankmeldung, Besprechungsbeschluss) müssen an die richtigen Adressaten kommuniziert und ggf. gespeichert werden.
- Informationen müssen in **Kategorien** eingeteilt werden mit allgemeingültigen Regeln je Kategorie.
- **Kommunikation**: technische Kanäle (Besprechung, Telefon, Videokonferenz, E-Mail, Datenbanken) sind zweitrangig gegenüber dem Ablauf beim Umgang mit Informationen.
  - Unwichtige Information: versenden/ablegen ohne weitere Aktivitäten.
  - Wichtige Information: Empfang quittieren lassen (Sicherstellung des Eingangs + Dokumentation der Weitergabe).

#### Beispiel 4.14: 5 Informationskategorien (I1–I5)

| Kategorie | Art der Information | Zu informieren | Reaktion |
|---|---|---|---|
| I1 | Gefährdet Projekterfolg insgesamt | Auftraggeber + Projektleiter | Krisensitzung mit Auftraggeber |
| I2 | Verursacht Verzögerung oder Mehraufwand | Auftraggeber + Projektleiter | Projektinterne Krisensitzung |
| I3 | Betrifft gesamtes Projektteam | Projektleiter + gesamtes Team | Behandlung auf regulärer Projektsitzung |
| I4 | Betrifft mehrere Projektbeteiligte | Projektleiter + alle Betroffenen | Besprechung der Betroffenen |
| I5 | Betrifft nur einen Projektbeteiligten | Betroffener | Bearbeitung durch Betroffenen |

- Kategorien I1–I5 können auch in der IMV-Matrix bei der Informationspflicht berücksichtigt werden.

- **Dokumentation**: dauerhafte Ablage von Informationen in Dokumenten (Papier oder elektronisch; Texte, Grafiken, Listen, Tabellen).
  - Freigegebenes Dokument darf nicht mehr geändert werden; notwendige Änderungen über **Versionierung** (neue Versionsnummer, z.B. Lastenheft Version 1.3) oder **Änderungsmitteilungen** (nur bei wenigen, kleinen Änderungen empfehlenswert).
  - Versionsnummern können hierarchisch gegliedert sein.
  - Bei vielen/großen Änderungen: versionierte Dokumente bevorzugen (übersichtlicher als Einzeländerungsmitteilungen).

### 4.3.2 Informationsmanagement

- Historische Entwicklung: von reiner Papierablage (Mappen, Ordner, Regale) zu elektronischer Datenverarbeitung → stark gestiegener Informationsfluss in Menge und Geschwindigkeit.
- Erste elektronische Dokumente auf Einzelrechnern → schwieriges Wiederauffinden; Verbesserung durch Netzlaufwerke und zentrale Dokumenten-Server.
- Unternehmen mit **Dokumentenmanagementsystem (DMS)** können Projektdokumente darin handhaben.
- Wesentliche Fragen an ein DMS:
  - Wo/wie werden Dokumente abgelegt?
  - Wer darf lesend zugreifen?
  - Wie wird Zugriff geschützt?
  - Wie wird Suche nach Dokumenten unterstützt?
  - Wie erfolgt Datensicherung?
- Alles als wichtig einzustufen und alles zu dokumentieren wäre überwältigend aufwändig und führt zu Informationsüberflutung (wichtige Infos werden in der Flut übersehen).
- Daher: Wichtigkeit bewerten → betroffene Empfänger identifizieren → Art und Ort der Dokumentation bestimmen.

### 4.3.3 Informationsmanagement im Projekt

- Jede Projektaktivität hat Input und Output; Dokumente sind die wichtigsten Ein- und Ausgaben.
- Dokumentenarten nach zeitlicher Abfolge im Projekt:
  - **Auftragsdokumente**: Anfrage, Lastenheft, Pflichtenheft, Angebot, Auftrag, Projektantrag, Projektdefinition (F)
  - **Organisationsdokumente**: Organigramm, Kalkulationsunterlagen, Liste der Projektbeteiligten, IMV-Matrix, Besprechungsberichte (F), Statusberichte (F), To-Do-Listen (F), PM-Handbuch
  - **Planungsdokumente**: Arbeitspaket-/Produktstrukturplan, Projektstrukturplan, Terminplan, Risikoanalyse, Kapazitätsplan, Personaleinsatzplan, Ressourcenliste, Meilensteinliste
  - **Steuerungsdokumente**: Änderungsanträge
  - **Abschlussdokumente**: Übergabeprotokoll, Nachkalkulation, Projekt-Daten-Sammlung
  - „**Dunkle Information**": unstrukturiert anfallende Daten (Notizen, E-Mails, Memoranden) — nicht formal dokumentiert, aber real wirksam (Analogie: dunkle Materie).
- Alle Projektdokumente sollten einheitliche Mindestanforderungen erfüllen; Kopf-/Fußzeile mit: Seitennummer, Dokumententitel, Datum.
- **Dokumentenstammdaten** (Pflichtfelder):
  - Titel/Thema
  - Anlass/Zweck/Art
  - Verfasserangaben
  - Verteiler (Lese-Verpflichtete und Lese-Berechtigte)
  - Erstellungs-/Freigabedatum
  - Stichworte (für Suche, Filtern, Sortieren)
- Zusätzlich in allen Projektdokumenten: Projektbezeichnung, Projektidentifikation (Kürzel/Nummer), Projektleiter.
- Für jede spezielle Dokumentenart sollte ein Formular-Template erstellt und in das PM-Handbuch aufgenommen werden.

**Wichtige Dokumententypen:**

- **Logbuch**: einfachste Form der Daueraufzeichnung; eine Person trägt alle Gedanken, Ideen, Gespräche chronologisch in gebundenes, fortlaufend nummeriertes Buch ein. Keine nachträglichen Eintragungen/Entfernungen möglich. Vorteil: niedrige Formalhürde. Nachteil: fehlende Gliederung, aufwändige Stichwortsuche. Eignet sich primär als individuelle Sammlung des Einzelnen.
- **To-Do-Liste**: listet auszuführende Aufgaben mit verantwortlicher Person und Zieltermin auf; optional Erledigungsstatus (offen/in Arbeit/erledigt), geplanter Beginn, Aufwand, Priorität. Ähnlich: **Liste offener Punkte (LOP)** für kleinere Aufgaben außerhalb des formalen Projektplans.
- **Notiz**: bei informationell relevantem Ereignis verfasst (Telefonnotiz, Aktennotiz, Gesprächsnotiz) — zur nachvollziehbaren Weitergabe und dauerhaften Speicherung.
- **Bericht**: anlässlich eines bestimmten Ereignisses erstellt, nach Freigabe nicht mehr änderbar. Höhere formale Anforderungen als Notiz. Wichtige Varianten:
  - **Besprechungsbericht**: Ergebnisprotokoll oder Diskussionsprotokoll; enthält Aufträge (wer/was/bis wann), Beschlüsse, Informationen. Regel: keine Besprechung ohne Bericht.
  - **Statusbericht**: zu festgelegten Zeitpunkten (periodisch oder an Meilensteinen); fasst Aktivitäten/Ergebnisse des Zeitraums zusammen; Aussagen zu Produkt, Aufwand, Kosten, Terminen.
  - **Projektabschlussbericht**.
- **Checklisten**: standardisierte Listen für bestimmte Aktivitäten; Punkte werden abgehakt. Sichern Vollständigkeit; erleichtern Übersicht bei unterschiedlichen Projekten und Beteiligten. Nachteil: zu allgemeine Checklisten werden umfangreich und enthalten viele für den Einzelfall unnötige Punkte.
- **Ressourcentabelle**: alle benötigten/verfügbaren Ressourcen mit Ausstattungs- und Verfügbarkeitsmerkmalen.
- **Personaltabelle**: alle Projektbeteiligten (alle Stakeholder) mit Attributen; beschreibt Einzelpersonen, keine Beziehungen zwischen Personen.
- **Planungsdokumente**: Produktstrukturplan, Projektstrukturplan, Testpläne, Ressourceneinsatzpläne, Personaleinsatzpläne, Kostenpläne — als Tabellen/Listen oder grafisch als Netzpläne/Ablaufpläne.

#### Beispiel 4.15: Besprechungsbericht im CAD-Software-Fallbeispiel

- Formular-Template aus Anhang; enthält grundlegende Projektangaben + wichtige Besprechungsergebnisse; jedes Ergebnis gekennzeichnet als Information (I), Beschluss (B) oder Auftrag (A); bei Aufträgen: verantwortliche Person + Erledigungstermin zwingend.

**Agile Projekte (Scrum):**
- Dokumentation tritt gegenüber Kommunikation in den Hintergrund.
- **Daily Scrum**: sehr kurze tägliche Teambesprechung; feste Uhrzeit (möglichst morgens), strikte Zeitbegrenzung (z.B. 15 Minuten). Inhalt: abgeschlossene Arbeiten, aufgetretene Probleme + Lösungsoptionen, nächste geplante Arbeiten. Scrum Master kann bei organisatorischen Problemen teilnehmen. Ermöglicht sehr zeitnahe Klärung von Fragen und Unstimmigkeiten.

### 4.4 Das Projektmanagement-Handbuch

- **PM-Handbuch** (nach DIN 69905): Zusammenstellung von Regelungen, die in einer Organisation generell für die Planung und Durchführung von Projekten gelten — nicht nur für ein einzelnes Projekt, sondern für alle Projekte im Unternehmen.
- Regelt: Weisungsbefugnisse, Ablauf der Arbeitsprozesse, Informationsflüsse.
- Ohne diese Regeln entstehen typische Probleme: Weisungswirrwarr zwischen Projekt- und Linienvorgesetzten, Projektfestfahren in Fehler-Notlösung-Fehler-Schleifen, nicht auffindbaren Dokumente.
- Ersteinmalig aufwändig; danach reduziert sich Organisationsarbeit bei jedem neuen Projekt auf Auswahl der passenden Organisations- und Ablaufform aus dem Handbuch.
- Verringert Gefahr, Projekte ohne organisatorische Regelungen zu beginnen.

**Empfohlene Gliederung eines PM-Handbuchs:**

1. Einleitung: Projektmerkmale, -definition, -arten; Aufgaben, Anwendungsbereich und Versionen des Handbuchs
2. Aufbauorganisation: Einordnung der Projektstrukturen; Rollenprofile; Aufgaben, Verantwortungen, Befugnisse der Beteiligten und Gremien
3. Ablauforganisation: bevorzugte Ablaufformen; Festlegungskriterien; Regeln für Teilprojektgliederung und Projektphasen; Muster-Standard-Projektstrukturplan
4. Informationsorganisation: Informationskategorien; Kommunikationswege; Dokumentationsmanagement
5. PM-Teilgebiete: Regeln für Gründung, Planung, Steuerung, Abschluss; Regeln für Kosten-, Qualitäts-, Risiko- und Änderungsmanagement
6. Anhang: Checklisten, Templates, Glossar (unternehmensspezifische Begriffe)

---

## Kapitel 5: Strukturplanung

### 5.1.1 Der Produktstrukturplan (ProdSP)

- Ausgangspunkt jeder Projektplanung ist das angestrebte Projektziel (Produkt). Von ihm ausgehend werden alle notwendigen Aktivitäten abgeleitet.
- Das Produkt — ob mechanische Konstruktion, elektrisches Gerät, Softwaresystem, Gebäude, Dokumentation, Verfahrensvorschrift oder Dienstleistung — besteht aus vielen hierarchisch gegliederten Komponenten.
- **Produktstrukturplan (ProdSP)**: hierarchisch gegliederte Liste aller Teile eines Produkts; als baumartig gegliederter Plan dargestellt.
  - Grafische Form: übersichtlich bei kleinerem Umfang; horizontale Strukturierung = verschiedene Produktteile, vertikale Strukturierung = Ebenen (oben: Gesamtprodukt; unten: elementare Komponenten).
  - Listenform: besser bei Dutzenden Produktteilen und Hunderten Komponenten.
- **Vollständigkeit** ist das wichtigste Qualitätsmerkmal: Wird ein Produktteil vergessen, tauchen die zugehörigen Arbeiten auch im Projektplan nicht auf → ungeplanter Mehraufwand + Terminprobleme. Ein nachträglicher Wechsel der Realisierungsform ist um eine Größenordnung weniger schädlich als komplett vergessene Teile.
- Gründliche Produktstrukturplanung deckt Unklarheiten, Lücken, Fehler und Widersprüche in der Aufgabendefinition auf; lässt Risikofaktoren erkennen.
- Geeignete Gliederungskriterien je nach Produkt: bei Mechanik → Teilkomponenten; bei Elektronik → Funktionen/Baugruppen; bei Software → Programme/Module/Funktionen; bei Gebäude → Gewerke.
- Detaillierungsgrad ausreichend, wenn für jeden Produktteil klar erkennbar ist, welche Arbeiten für Herstellung/Beschaffung notwendig sind.

#### Beispiel 5.1: Produktstrukturplan Wohnhaus

- Produkt „Wohnhaus" → erste Ebene: Baugrund, Rohbau, Ausbau.
- Ausbau → zweite Ebene: Wasserversorgung, Entsorgung, elektrische Anlagen, Heizung, Fenster, ...
- Elektrische Anlagen → dritte Ebene: elektrische Hauptleitung (Hausanschluss → Zähler), zentrale Energieverteilung mit Zähler und Sicherungen, Verteilungsleitungen, Verbraucher, Schaltkomponenten.
- Auf dieser dritten Ebene lassen sich einzelne Arbeitspakete identifizieren.

### 5.1.2 Zusammensetzung des Produktstrukturplans

- Kern des Produkts: **Liefergegenstände** (im Lastenheft gefordert, im Pflichtenheft explizit genannt) — hier ist Vergessen am unwahrscheinlichsten.
- Häufig vergessen: **Dokumentationen** (Benutzerhandbuch, Bedienungsanleitung, Betriebsanleitung) → gehören zum Produkt und müssen eingeplant werden.
- Auch Dienstleistungen zählen zum Produkt: Inbetriebnahme, Schulung, Service → verursachen Zeitaufwand, Vorbereitungsaufwand, Kosten.
- **Zwischenprodukte**: Produkte/Produktteile, die nicht ausgeliefert werden, aber im Projekt benötigt werden (z.B. Simulationsmodelle, Prototypen, Testversionen). Frühere Entwicklungsstufen, die am Ende nicht mehr in Erscheinung treten.
- **Hilfsprodukte**: zur Prüfung, Vermessung, Verarbeitung oder Transport der eigentlichen Produkte geschaffen. Müssen entwickelt oder zugekauft werden (auch beim Zukauf: Marktrecherche, Bestellung, Inbetriebnahme verursachen Aufwand) → müssen im Projekt berücksichtigt werden.
- **Eindeutige Bezeichnungen** wichtig (Verwechslungsgefahr bei ähnlichen Bezeichnungen); am besten durch numerischen Gliederungsschlüssel mit Positions-Codierung in der Baumstruktur.
  - Gegliederte Nummerierung (z.B. 2.1.5.3): übersichtlichste Form; Punkte trennen Ebenen; keine Einschränkung der Zahlen je Ebene.
  - Mehrstellige Dezimalzahlen (z.B. 2437): je Ebene eine Ziffer → maximal 10 Positionen je Ebene.
  - Alphanumerische Mischsysteme (z.B. IIIA17): eher unübersichtlich.
- **Standard-Produktstrukturplan**: bei ähnlichen Projekten empfohlen; Obermenge gemeinsamer Produktteile aus vergangenen Projekten. Neue Pläne durch Streichen und Konkretisieren erstellen — schneller, weniger fehleranfällig. Standardisierung deckt meist nur obere Ebenen ab (untere sind produktspezifisch).

#### Beispiel 5.2: Standard-ProdSP für Hersteller elektrischer Geräte

- Umfasst zwei oberste Ebenen; erleichtert Vollständigkeitscheck ohne alle Positionen erzwingen zu müssen.

### 5.1.3 Vorgehensweise zur Planerstellung (Top-down vs. Bottom-up)

- **Top-down**: beginnt beim Gesamtprodukt → Zerlegung in Hauptteile → weitere Zerlegung über mehrere Ebenen bis zu elementaren Bestandteilen (elementar = fertig beschaffbar oder alle Herstellarbeiten vollständig bekannt). Vorteil: Gliederung entsteht quasi von selbst. Nachteil: wenn Gliederung nicht vorab erkennbar ist, schwierig anzuwenden.
- **Bottom-up**: unstrukturiertes Brainstorming/Sammeln aller Produktteile → danach Gruppieren, Ordnen, hierarchisches Gliedern. Hilfreich: Produkt als System betrachten, dessen Schnittstellen zur Umgebung und realisierte Funktionen die Systemteile aufzeigen. Nachteil: schwer zu entscheiden wann Liste vollständig ist → Risiko zu früh aufzuhören oder Zeit zu verschwenden.
- **Empfehlung**: beide Ansätze kombinieren — Top-down eine hierarchische Grobstruktur + Bottom-up fehlende Teile sammeln → beide Listen zusammenführen.

#### Beispiel 5.3: Maschinenterminal — Produktstrukturplan

- Top-down: Gerät → Mechanik, Elektronik, Software, Dokumentation (erste Ebene); Mechanik → Ober-/Unterteil Gehäuse, Stecker Stromanschluss, Netzwerkstecker, Wandhalterung; Elektronik → CPU-Baugruppe, Benutzerschnittstelle, Lesegeräteinterface usw.
- Bottom-up-Brainstorming: Liste (Netzteil, CPU, Folientastatur, Lesestift, LAN-Stecker, Textdisplay, Wandhalter, ...) → danach Gruppierung zu Oberbegriffen.
- In früher Planungsphase: räumliche Anordnung, Verbindungen zwischen Teilen und Wechselwirkungen müssen noch nicht enthalten sein — Vollständigkeit der Teileliste hat Vorrang.

### 5.2.1 Der Projektstrukturplan (ProjSP)

- Ein Projekt enthält eine sehr große, oft nicht von Beginn an überschaubare Menge von Arbeiten. Viele Arbeiten sind zu Projektbeginn nur unvollständig bekannt.
- **Projektstrukturplan (ProjSP)** (engl. Work Breakdown Structure): fasst alle in einem Projekt notwendigen Arbeiten in einer hierarchisch strukturierten Liste zusammen; stellt sie als Baumstruktur dar.
  - Oberste (0.) Ebene: Gesamtprojekt.
  - Unterste Ebene: Arbeitspakete.
  - Dazwischen: je nach Projektumfang mehrere Teilprojektebenen.
- Notwendige Merkmale: **Vollständigkeit** (alle Aufgaben erfasst) und **Gesamtbetrachtungsweise** (keine Aufgabe isoliert, sondern im Gesamtzusammenhang).
- Basis für alle weiteren Planungsschritte: Festlegung der Vorgänge, Terminplanung, Kostenschätzung, Mitarbeiter- und Ressourceneinsatz.
- **Grob-Projektstrukturplan**: bei Angebotserstellung sinnvoll (nur ein Teil der Angebote wird zum Auftrag); Teilaufgaben soweit untergliedert, dass Aufwand/Kosten abschätzbar. Genauigkeit abhängig von Erfahrungen mit ähnlichen Projekten und Zweck der Abschätzung.
- **Fein-Projektstrukturplan**: erst nach Auftragserteilung sinnvoll; Konkretisierung der Aufgaben bis zu Einzelaufgaben, die gut überschaubar sind und eindeutig einer Person/Maschine/Arbeitsplatz zugeordnet werden können. Bildet Grundlage für die Ablaufplanung.

### 5.2.2 Produktorientierte Gliederung

- Leitet Arbeitspakete aus Produktteilen ab; lehnt sich an Produktstruktur an. Jeder Produktteil erfordert bestimmte Arbeiten → Teilaufgabe im ProjSP.
- Nicht identisch mit ProdSP: ProjSP enthält auch Arbeiten die keinem Produktteil direkt zugeordnet werden können (Projektmanagement-Arbeiten, Lastenheft-Analyse, Systemtest, Gesamtübergabe).
- Geeignet wenn Probleme im Projekt überwiegend technischer Art sind (z.B. neues technisches Produkt); fördert abteilungsübergreifende Zusammenarbeit bei komplexen Teilen.

#### Beispiel 5.4: Maschinenterminal — Projektstrukturplan (produktorientiert)

- Grobe Phaseneinteilung → Komponenten (Gehäuse, Elektronik, Software, Zubehör) → weitere Detaillierung.
- Ergebnis: ca. 50 Arbeitsgänge; bei mittlerem Aufwand von 5 Personentagen je Arbeitsgang → Gesamtumfang ca. 250 Personentage ≈ 1+ Personenjahr.

### 5.2.3 Prozessorientierte Gliederung

- Kriterium für Zuordnung zu Arbeitspaketen/Teilprojekten: Arbeitsabläufe und beteiligte Abteilungen des Betriebs; zeitliche Abfolge bestimmt Gruppierung.
- Geeignet wenn Probleme im Projekt vorwiegend organisatorischer Art sind (z.B. Organisationsprojekte, Projektierung von Anlagen aus verfügbaren Komponenten).
- Abteilungsfunktionen (Vertrieb, Einkauf, Montage, Service) sind eher unabhängig → deren Arbeitspakete werden als zusammenhängende Einheiten dargestellt.
- Lehnt sich stärker an bestehende Linienstruktur an → erleichtert Zuordnung zu Abteilungen/Personen. Nachteil: abteilungsübergreifendes Denken geht teilweise verloren.

#### Beispiel 5.5: Solaranlage Steinbachwerke — Projektstrukturplan (prozessorientiert)

- Bestandsheizung (Öl-Brenner 7 Jahre alt, bleibt erhalten) soll durch solarthermische Anlage (Flachkollektoren auf Maschinenhalle + neuer bivalenter Wärmespeicher) ergänzt werden. Alter Wasserspeicher wird ersetzt; Heizraum im Keller hat ausreichend Platz.
- Auftrag an externes Ingenieurbüro für Planung, Montage, Inbetriebnahme.
- ProjSP in 4 Phasen entsprechend Arbeitsablauf: Aufgabenanalyse → Beschaffung → Aufbau → Inbetriebnahme.
- Vorteil dieser Phaseneinteilung: Aufbau beginnt erst wenn alle Teile geliefert sind → keine Verzögerungen durch fehlende Materialien in der Aufbauphase.
- Jede Phase in Arbeitspakete unterteilt (abschätzbar, möglichst unabhängig voneinander).
- Nach Angebots-/Verhandlungsabschluss: Auftraggeber verlangt verlässlichen Ablauf- und Terminplan innerhalb einer Woche.

**Mischformen**: in der Praxis häufig; kombinieren Vorteile beider Grundformen. Entscheidungskriterium immer: welches Schema erleichtert die Zuordnung von Arbeiten zu Personen am besten?

### 5.2.4 Breite vs. Tiefe der Gliederung — 7er-Regel

- Menschliches Kurzzeitgedächtnis speichert bis zu 7 Informationseinheiten.
- Daraus abgeleitete **7er-Regel**: jedes Element sollte in ca. 7 Teilelemente untergliedert werden (Miller 1956; Wert ist Richtwert, Bandbreite 4–12 ist praktisch angemessen).
- Strukturbaum wächst mit jeder Ebene um Faktor 7:

| Ebene | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Elemente | 1 | 7 | 50 | 350 | 2.000 | 14.000 | 100.000 | 700.000 |

- Beispiele: Buch mit 300 Seiten (1 Unterkapitel ≈ 1 Seite) → 3 Gliederungsebenen ideal; Unternehmen mit 100.000 Beschäftigten → 6 Hierarchieebenen; Projekt mit ca. 50 Arbeitspaketen (≈1 Personenjahr) → sinnvoll: ca. 7 Teilprojekte (Ebene 1) × 7 Arbeitspakete (Ebene 2).

### 5.2.5 Standard-Projektstrukturpläne

- Vollständiger ProjSP ist Voraussetzung für zuverlässige Aufwandsschätzung und Terminplanung; trotzdem werden immer wieder Arbeitspakete vergessen oder unterschätzt.
- **Standard-Projektstrukturplan**: Obermenge aller typischerweise anfallenden Arbeitspakete in den Projekten eines Unternehmens — aus Analyse vergangener Projekte extrahiert.
- Erstellung eines konkreten ProjSP = Auswahl einer Teilmenge des Standard-ProjSP durch Streichen nicht benötigter Arbeiten + Konkretisierung verbleibender Pakete.
- Vorteile: Erfahrungen aus abgeschlossenen Projekten besser nutzbar (z.B. Kennzahlen für Aufwandsschätzung); Risiko vergessener Arbeitspakete deutlich verringert.

#### Beispiel 5.6: Standard-ProjSP für elektronische Steuerungen

- Auslöser: bei einem Hersteller kundenspezifscher Steuerungen traten trotz Neuartigkeit der Projekte wiederholt dieselben Ursachen für Beanstandungen und Zeitüberschreitungen auf: vollständiges Vergessen von Arbeitspaketen oder Unterschätzen des Aufwands.
- Analyse vergangener Projekte → trotz aller Unterschiede im Detail: abstraktere Betrachtung zeigt viele Gemeinsamkeiten.
- Resultierender grober Standard-ProjSP (oberste Ebene): Vor-Projekt, Konzeption, mechanische Konstruktion, Hardware-Entwicklung, Software-Entwicklung, Tests — jedes Teilprojekt weiter in Arbeitspakete unterteilt.
- Neues Projekt: immer zuerst Standard-Plan zugrunde legen → nicht notwendige Arbeiten streichen → verbleibende Grob-Pakete projektspezifisch verfeinern. Erfahrungswerte über Schätzgenauigkeit werden dadurch systematisch gesammelbar.
