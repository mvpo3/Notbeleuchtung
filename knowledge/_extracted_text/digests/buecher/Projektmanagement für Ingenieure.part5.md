# Projektmanagement für Ingenieure — Teil 5
> Quelle: Projektmanagement für Ingenieure (buecher) · Seiten 201-240.

Dieser Teil schließt Kapitel 7 (Ablauf- und Terminplanung) ab und führt Kapitel 8 (Risikomanagement) sowie den Beginn von Kapitel 9 (Kostenmanagement) ein. Behandelt werden stochastische Planungsmethoden (PERT, Dreipunktschätzung), Gantt-Diagramme, Kapazitätsplanung, systematische Risikoidentifikation und -bewertung (Risk-Map, Risikograph, FMEA), sowie Grundlagen der Projektkostenrechnung, Stundensatzkalkulation und Earned Value Analyse.

## Inhalt

### 7.2.3 PERT-Methode (Program Evaluation and Review Technique)

- PERT arbeitet ähnlich wie CPM, ersetzt aber direkte Einzelschätzwerte durch aus der Dreipunktschätzung abgeleitete Mittelwerte.
- Erstmals 1958 im US-amerikanischen Polaris-Raketenprojekt eingesetzt.
- Grundannahme: Vorgangsdauern folgen einer Beta-Verteilung — nach unten und oben begrenzt, linksschiefe Dichtefunktion (häufiger kurze, selten sehr lange Dauern).
- Drei Schätzpunkte je Vorgang: To (optimistisch), Tw (wahrscheinlichst), Tp (pessimistisch).
- Erwartungswert Te und Standardabweichung Ts der Beta-Verteilung:
  - Te = (To + 4·Tw + Tp) / 6
  - Ts = (Tp − To) / 6
- Gesamtprojekt-Laufzeit: Summe der Te-Werte der Vorgänge auf dem kritischen Pfad; die Summen-Verteilung nähert sich einer Normalverteilung an → statistische Aussagen über Einhaltungswahrscheinlichkeiten möglich.
- Gesamtvarianz des kritischen Pfads: Quadratische Addition der Einzelvarianzen → Ts_gesamt = Wurzel aus Summe aller Ts²_i.

#### Beispiel 7.4 PERT-Projektanalyse

- Ausgangssituation: Projektleiterin schätzte 275 PT Gesamtaufwand, Güte der Schätzung unbekannt.
- Gruppenabfrage ergab: To = 200 Tage, Tw = 250 Tage, Tp = 350 Tage.
- Daraus: Te = 258 Tage, Ts = 25 Tage.
- Verteilungsfunktion F(A) des Gesamtaufwands A (A = Te + z·Ts):

| z-Wert | Aufwand A (Tage) | Wahrscheinlichkeit F(A) |
|--------|-----------------|------------------------|
| 0,00 | 258 | 50 % |
| 0,25 | 265 | 60 % |
| 0,52 | 271 | 70 % |
| 0,84 | 279 | 80 % |
| 1,28 | 290 | 90 % |
| 1,64 | 299 | 95 % |
| 2,00 | 308 | 98 % |

- Projektleiterin hatte intuitiv 275 PT geschätzt → entspricht ca. 75 % Einhaltungswahrscheinlichkeit.
- Zerlegung in 10 Arbeitspakete mit Dreipunktschätzung je AP:

| Vorgang | Vorgänger | To | Tw | Tp | Te | Ts |
|---------|-----------|----|----|----|----|-----|
| A1 | — | 20 | 25 | 40 | 26,7 | 3,3 |
| A2 | A1 | 15 | 18 | 25 | 18,7 | 1,7 |
| A3 | A1 | 10 | 15 | 20 | 15,0 | 1,7 |
| B1 | A1 | 40 | 50 | 90 | 55,0 | 8,3 |
| B2 | A2 | 25 | 30 | 40 | 30,8 | 2,5 |
| C1 | A3 | 25 | 30 | 45 | 31,7 | 3,3 |
| C2 | B1; B2; C1 | 10 | 12 | 15 | 12,2 | 0,8 |
| D1 | A2 | 10 | 15 | 20 | 15,0 | 1,7 |
| D2 | D1 | 20 | 25 | 30 | 25,0 | 1,7 |
| D3 | C2; D2 | 20 | 25 | 35 | 25,8 | 2,5 |
| **Laufzeit** | | 90,0 | 112,0 | 180,0 | 119,7 | 9,4 |
| **Aufwand** | | 195 | 245 | 360 | 255,9 | 10,7 |

- Kritischer Pfad: A1 → B1 → C2 → D3.
- Ergebnis: Erwarteter Aufwand 256 PT (kaum verändert), aber Standardabweichung sank von 25,0 auf 10,7 Tage (Unsicherheit drastisch reduziert durch Zerlegung).
- Mit 98 % Wahrscheinlichkeit Abschluss innerhalb 139 Tagen (= Te_laufzeit + 2·Ts = 119,7 + 2·9,4 ≈ 139 Tage) und maximal 277 PT Aufwand.

#### Beispiel 7.5 Temperaturmessbox-Projekt

- Kritischer Pfad: 5 Vorgänge (V1, V4, V6, V7, V8).
- Summierte Laufzeitverteilung des kritischen Pfads: Te = 21,5 Tage, Ts = 1,8 Tage.
- Verteilungsfunktion F(T) der Projektlaufzeit:

| Laufzeit T | Wahrscheinlichkeit F(T) |
|-----------|------------------------|
| 17,9 Tage | 2 % |
| 19,7 Tage | 18 % |
| 21,5 Tage | 50 % |
| 23,3 Tage | 84 % |
| 25,1 Tage | 98 % |

- Pessimistisches Szenario (alle Pakete maximal): 34 Tage, optimistisches (alle minimal): 15 Tage — beide sehr unwahrscheinlich.
- Einhaltung Erwartungswert: 50 %; plus einfache Standardabweichung: 84 %; plus doppelte: 98 %.

### 7.2.4 Gantt-Diagramme

- Balkendiagramm: Vorgänge als Balken, Balkenlänge proportional zur Zeitdauer — anschaulich, sofort verständlich.
- Entwickelt 1910 vom US-Ingenieur H. Gantt.
- Ursprünglicher Zweck: Darstellung von Planungsergebnissen, nicht Planungswerkzeug an sich; logische Abhängigkeiten zwischen Vorgängen waren nicht erkennbar.
- Weiterentwicklung unter der Bezeichnung Plannet (Planning Network): Pfeile zwischen Balken symbolisieren Anordnungsbeziehungen.
- Heute Standardbestandteil aller Projektplanungssoftware; rechnergestützte Pflege erlaubt Sofort-Aktualisierung bei Planänderungen.
- Zusammenhang mit Netzplänen: Terminierungsdaten sind tabellarisch gespeichert; Gantt-Diagramm ist eine von mehreren Sichtweisen auf dieselbe Datenbasis.
- Historischer Kontext: CPM wurde ursprünglich auf einem UNIVAC-Rechner implementiert (> 10 t Gewicht, mehrere 100.000 USD, 1000 Worte Speicher, Ende der 1950er Jahre).

#### Beispiel 7.6 Maschinenterminal M4 — Gantt-Diagramm Elektronikentwicklung

- Lieferzeiten (z. B. CPU-Baugruppe +15 Tage, Textdisplay, Informationen für CPU-Auswahl +6 Tage) werden als Zeitbedingungen im Plan berücksichtigt.
- Vorgänge mit Dauer 0 modellieren Eintreffen von Lieferungen als Meilenstein-Vorgänger.
- Graphische Darstellung macht parallele und sequenzielle Strukturen sowie alle Abhängigkeiten sofort erkennbar.

### 7.3 Kapazitätsplanung

#### Grundlagen und Problemstellung

- Ablauf- und Terminplanung geht zunächst von unbegrenzt verfügbaren Kapazitäten aus — praxisfern.
- Reale Einschränkungen: begrenzte Personenzahl, nicht immer 100 % verfügbar, nicht über gesamte Projektlaufzeit verfügbar; gleiches gilt für materielle Ressourcen (Maschinen, Arbeitsplätze, Rohstoffe); Budgets werden zeitlich gestaffelt freigegeben.
- Terminierter Ablaufplan liefert nach Zuweisung von Vorgängen zu Personen ein Belastungsdiagramm — typischerweise ungleichmäßig, „Kapazitätsgebirge" genannt.
- Minimale theoretische Projektlaufzeit bei N Personen und Gesamtaufwand A: T = A/N — nur erreichbar wenn Personal vollständig und durchgängig beschäftigt werden kann.
- Realer Verlauf der Auslastung über Projektlaufzeit: buckelförmige „Walvischkurve" — anfangs wenig Personal (Analyse/Entwurf), Anstieg in Realisierung und Test, Abfall in Abschlussarbeiten.

#### Kapazitätskonflikt-Lösung

- Verschiebung von Vorgängen mit genügend Puffer: unproblematisch.
- Wenn Puffer nicht ausreicht: Termine auf kritischem Pfad müssen verändert werden → Auswirkung auf Meilensteine.
- Vorübergehende Personalaufstockung als letzte Option: führt zu überproportional steigendem Aufwand durch Einarbeitungszeit und Kommunikationsmehraufwand (Brooks'sches Gesetz: zusätzliches Personal in verzögerten Projekten macht diese noch später).
- Iterativer Prozess: grob → fein; Puffer in frühen Planungsiterationen offen lassen für spätere Feinjustierung.

#### Beispiel 7.7 Prozesssteuerung (Steinbachwerke)

- Projekt: mikroprozessorbasierte Steuerungsanlage; 2 Mitarbeiter (P1 Hardware, P2 Software).
- Geplante Laufzeit 9 Wochen bei 24 Personenwochen Gesamtaufwand → theoretisches Minimum mit 2 Personen: 12 Wochen.
- Realisierung in 9 Wochen erfordert phasenweise 2,7 Personen (24 PW / 9 W) → zusätzliche Person zeitweise nötig.

#### Beispiel 7.8 Kapazitätsplanung Software-Projekt

- 3 Personen A, B, C; A zunächst allein für Analyse und Konzept (B und C in anderem Projekt); ab Codierung alle 3 parallel.
- Überlast bei B und C von KW 24 bis KW 36 wegen 42 erforderlicher Personenwochen gegenüber 39 verfügbaren (3 Personen × 13 Wochen).
- Kompromisslösung ohne Terminüberschreitung durch vier Maßnahmen:
  1. Datenbankschnittstellen-Programmierung und -test von B auf A verlagert.
  2. A übernimmt Benutzerhandbuch und Programmdokumentation.
  3. Mit Auftraggeber vereinbart: Programmdokumentation erst in KW 40 (nicht KW 36).
  4. Systemtest durch B und C startet bereits parallel zum Abschluss der Datenbankschnittstelle durch A.

---

### Kapitel 8: Risikomanagement

#### 8.1 Projektrisiko

##### 8.1.1 Unsicherheiten in Projekten

- Projekte basieren auf unvollständigen Informationen und veränderlichen Anforderungen → jede Entscheidung ist mit Unsicherheit behaftet.
- Risikofaktoren sind alle Erfolgsfaktoren des Projekts zugleich (Arbeitspaketausführung, Teilelieferungen, Lastenheft-Vollständigkeit, Technologieentscheidungen, Personaleinsatz).
- Konsequenzen von Risikofällen: Terminüberschreitungen, Kostenbudgetsprengung, Qualitätsmangel, im Extremfall Projektscheitern.
- Zwei Fehlhaltungen: vollständiges Ignorieren von Risiken vs. rein mathematische Risikoquantifizierung ohne Bodenhaftung.
- Risikomanagement ist der angemessene Mittelweg: analysiert, was schief gehen kann, wie es verhindert werden kann, und was bei Eintritt zu tun ist.
- Qualitative Methoden liefern Überblick über das Risikoumfeld; quantitative Methoden machen Risiken und Maßnahmen nachvollziehbar und belegbar.

##### 8.1.2 Der Risikobegriff

- Risiko entsteht aus dem Zusammenwirken eines potentiellen negativen Ereignisses und dem dadurch im Projekt verursachten Schaden.
- Eintrittswahrscheinlichkeit: zwischen 0 % (tritt sicher nicht ein) und 100 % (tritt sicher ein).
- Schadensformen: erhöhter Aufwand, verspäteter Abschluss, verschlechterte Qualität, Scheitern des Projekts.
- Definition nach DIN IEC 62198: Projektrisiko ist die Kombination aus Eintrittswahrscheinlichkeit eines Ereignisses und seinen Folgen für die Projektziele.
- Mathematische Formulierung Risiko R als Schadens-Erwartungswert für Maßnahmen-Szenario M:
  - R(M) = Σ (pᵢ · Sᵢ), Summe über alle N möglichen Ergebnisse mit Eintrittswahrscheinlichkeit pᵢ und Schadensausmaß Sᵢ
- Risikoverringernde Maßnahmen senken pᵢ (vor Schadenseintritt); schadensbegrenzende Maßnahmen senken Sᵢ (nach Schadenseintritt).
- Optimales Szenario: dasjenige, das R(M) minimiert; Kosten der Maßnahmen müssen gegen erzielte Risikoreduktion abgewogen werden.
- Vollständige Beseitigung aller Risiken ist praktisch nicht möglich; kein Risiko bedeutet auch keine Chance.

#### Beispiel 8.1 Personalrisiko

- Annahme: Projekt läuft 1 Jahr, 10 Mitarbeiter, mittlere Verweildauer im Unternehmen 5 Jahre.
- Kündigungswahrscheinlichkeit eines Mitarbeiters: 1/5 = 20 % pro Jahr.
- Wahrscheinlichkeit, dass kein einziger kündigt: 0,8^10 ≈ 10 % — sehr gering.
- Schadensausmaß hängt von Qualifikation des Betroffenen und Verfügbarkeit von Ersatz ab.

#### 8.2 Der Risikomanagement-Prozess

Vier aufeinander folgende Schritte; jeder liefert Eingaben für den nächsten. Gesamtergebnis ist eine Risiko-Datenbank.

##### 8.2.1 Risiko-Identifikation

- Ziel: alle Risikoquellen systematisch aufdecken, offensichtliche wie versteckte.
- Leitprinzip: Suche immer in Bezug auf Projektziele — nur Ereignisse, die Ziele gefährden, sind Risikofaktoren.
- Strukturierter Ansatz: Projekt als System betrachten (interne Komponenten + externe Schnittstellen = alle potentiellen Risikoquellen).
- Externe Schnittstelle: Lastenheft des Auftraggebers — Risiko widersprüchlicher, unvollständiger oder nicht realisierbarer Anforderungen.
- Pflichtenheft als Gegenmaßnahme: soll Lastenheft-Lücken und -Widersprüche bereinigen, explizit auch Nicht-Anforderungen nennen (Abgrenzung), um späte Diskussionen zu vermeiden.
- Technische Unsicherheiten im Pflichtenheft benennen und Auftraggeber entscheiden lassen: Risiko mittragen oder Anforderung abschwächen.

**Checkliste Risikofaktoren (Tab. 8.1):**

- Auftrags-Risiken:
  - Anforderungen klar, vollständig, widerspruchsfrei?
  - Können sich Zielvorgaben/Prioritäten ändern?
  - Projektplan kommuniziert und akzeptiert?
- Randbedingungsrisiken — Unternehmen:
  - Notwendige Priorität im Unternehmen vorhanden?
  - Benötigtes Personal und Ressourcen verfügbar?
- Randbedingungsrisiken — Auftraggeber:
  - Bonität gesichert?
  - Kontakt zu späteren Nutzern des Ergebnisses?
- Randbedingungsrisiken — Lieferanten:
  - Liefertreue, Termintreue, Qualitätstreue?
- Randbedingungsrisiken — Recht & Gesetz:
  - Rechtliche Bedingungen bekannt (Normen, Richtlinien, Genehmigungen)?
  - Patentsituation geklärt?
- Personelle Risiken — Projektleiter:
  - Erfahrung in Projektleitung vorhanden?
  - Belastbarkeit in Überlastsituationen?
- Personelle Risiken — Projektmitarbeiter:
  - Verfügbarkeit zum Bedarfszeitpunkt?
  - Ausreichende fachliche Qualifikation?
  - Soziale Spannungen (Konflikte, Egoismen)?
- Technische Risiken:
  - Eingesetzte Technologien am Ende ihrer Lebensphase?
  - Rohstoffverfügbarkeit gesichert?
  - Werkzeugverfügbarkeit und Schnittstellenkompatibilität?
- Organisatorische Risiken:
  - Planungsrisiken: Realismus der Aufwands- und Terminschätzungen, Vollständigkeit des Strukturplans?
  - Steuerungsrisiken: Projektkontrolle eingerichtet, Risikokontrolle vorhanden?

- Schadensfall abgeschlossener Projekte = Risikofaktor des nächsten Projekts: Erfahrungen in PM-Handbuch-Checkliste überführen.

#### Beispiel 8.2 Risiken bei der Entwicklung einer Elektronikbaugruppe

Typische Risikoprüffragen je Arbeitspaket:
- Alle Anforderungen an die Baugruppe bekannt?
- Elektrische und mechanische Schnittstellen definiert?
- Aufgabe mit vorhandenen Kenntnissen lösbar?
- Zeitschätzung realistisch?
- Bauelemente mit geforderten Spezifikationen verfügbar?
- Lieferzeiten beim Lieferanten einzuhalten?
- Alle relevanten Richtlinien beachtet (EMV, schadstoffarme Bauteile, Sicherheit)?

##### 8.2.2 Risiko-Bewertung

- Risiko = Eintrittswahrscheinlichkeit × Schadensausmaß.
- Bei fehlenden exakten Zahlenwerten genügt qualitative Näherung.

**Risk-Map (Abb. 8.2):**
- Koordinatensystem: x-Achse = Eintrittswahrscheinlichkeit p, y-Achse = Schadensausmaß S.
- Jedes Risiko als Punkt darstellbar; weiter rechts und oben = größeres Risiko.
- Punkte gleichen Risikos bilden eine Hyperbel im Diagramm.
- Wahrscheinlichkeitsklassen: p0 sehr unwahrscheinlich (< 0,1 %), p1 unwahrscheinlich (0,1 %–1 %), p2 wenig wahrscheinlich (1 %–10 %), p3 ziemlich wahrscheinlich (> 10 %).
- Schadensklassen: geringe Mehrkosten, moderate Mehrkosten, erhebliche Mehrkosten, Scheitern des Projekts.
- Kombination der Klassen ergibt Risiko-Portfolio des Projekts.

**Risikoklassen (Tab. 8.2):**

| Schadensausmaß | Eintrittswahrscheinlichkeit | Risikoklasse |
|---|---|---|
| Scheitern (Katastrophe: bis 100 % Gesamtkosten) | wenig oder ziemlich wahrscheinlich | A |
| Scheitern | unwahrscheinlich | B |
| Scheitern | sehr unwahrscheinlich | C |
| Erhebliche Kosten (Notfall: 10–30 % Gesamtkosten) | sonst (außer sehr unwahrscheinlich) | B |
| Erhebliche Kosten | sehr unwahrscheinlich | C |
| Moderate Mehrkosten (Störung: 3–10 % Gesamtkosten) | sonst | C |
| Moderate Mehrkosten | unwahrscheinlich | D |
| Moderate Mehrkosten | sehr unwahrscheinlich | E |
| Geringe Mehrkosten (< 3 % Gesamtkosten) | sonst | D |
| Geringe Mehrkosten | unwahrscheinlich | E |

**Projekt-FMEA (Fehler-Möglichkeits- und Einfluss-Analyse):**
- Quantitatives Verfahren; jedes Arbeitspaket wird auf Fehlerquellen untersucht.
- Drei bewertete Parameter, jeweils Skala 1–10:
  - Auftrittswahrscheinlichkeit pA: 1 = gering, 10 = sehr hoch
  - Schadensausmaß S (Bedeutung B): 1 = gering, 10 = Projektscheitern
  - Entdeckungswahrscheinlichkeit pE: 1 = hoch, 10 = sehr gering (Skala umgekehrt)
- Risikoprioritätszahl RPZ = pA × pE × B; Wertebereich 1–1000.
- Grenzwerte: RPZ < 40 unkritisch; RPZ > 100 kritisch, vorbeugende Maßnahmen erforderlich.

**Skalentabelle FMEA (Tab. 8.3):**

| Wahrscheinlichkeit | Wert pA | Wert pE | Budget-/Terminüberschreitung | Wert B |
|---|---|---|---|---|
| unwahrscheinlich < 0,1 % | 1 | 10 | < 5 % | 1 |
| sehr gering < 1,0 % | 2, 3 | 8, 9 | < 10 % | 2, 3 |
| gering < 10 % | 4, 5 | 6, 7 | < 20 % | 4, 5 |
| mittel < 25 % | 6, 7 | 4, 5 | < 50 % | 6, 7 |
| hoch > 25 % | 8, 9 | 2, 3 | > 50 % | 8, 9 |
| sehr hoch > 50 % | 10 | 1 | Scheitern | 10 |

#### Beispiel 8.3 FMEA Maschinenterminal (Auszug Tab. 8.4)

| Risikofaktor | pA | pE | B | RPZ | Bewertung |
|---|---|---|---|---|---|
| Wichtiger Projektmitarbeiter kündigt | 6 | 7 | 4 | 168 | Kritisch — vorbeugende Maßnahmen nötig |
| CPU wird abgekündigt | 3 | 4 | 2 | 24 | Unkritisch — Ersatztyp bereits vorgesehen |
| Benutzerschnittstelle wird nicht akzeptiert | 7 | 2 | 5 | 70 | Erhöht — Risikoreduktion durch Prototyp-Präsentation zu Projektbeginn |

##### 8.2.3 Risiko-Behandlung

- Ausgangspunkt: priorisierte Risikoliste aus Identifikation und Bewertung.
- Gesamtrisiko über akzeptablem Niveau → gravierendste Risiken einzeln angreifen.
- Zwei Stellhebel: pᵢ senken (Eintrittswahrscheinlichkeit) oder Sᵢ senken (Schadensausmaß).
- Praxisziel: Risikostufe um eine Klasse senken (Katastrophe → Notfall, Notfall → Störung).

**Risk Reduction Stair (Tab. 8.5) — Klasse zu Maßnahmenziel:**

| Klasse | Ziel | Bedeutung |
|---|---|---|
| A | Avoid | Risiko verhindern: Schaden oder Eintrittswahrscheinlichkeit auf null senken |
| B | Mitigate | Risiko lindern: Wahrscheinlichkeit verringern, Schaden minimieren |
| C | Limit | Risiko begrenzen: obere Schadensgrenze sicherstellen |
| D | Transfer | Risiko übertragen: z. B. finanziellen in zeitlichen Schaden umwandeln |
| E | Accept | Risiko akzeptieren |

- ALARP-Strategie (as low as reasonably practicable): Risikoreduzierung nur so weit wie praktisch vertretbar — betont die Kosten-Nutzen-Relation.

**Typische Maßnahmen je Risikotyp:**
- Vergessene Anforderungen: gründliche Aufgabenanalyse und sorgfältiges Pflichtenheft; Nicht-Anforderungen explizit ausschließen.
- Schätzunsicherheit: Gruppenabschätzung, Dreipunktschätzung, Zerlegung in Einzelfaktoren.
- Technische Unsicherheiten: mehrere Varianten ausarbeiten bevor eine realisiert wird; separate Machbarkeitsstudie vor Projektstart.
- Personalausfall (zeitlich begrenzt): etwas größzügigere Personaldecke; Ressourcen im Standby; zeitliche Puffer auf unkritischen Pfaden.
- Personalausfall (dauerhaft): Aufstockung (teuer und überproportional aufwändig wegen Einarbeitung und Koordination).
- Grundsatz: Risikomanagement kostet Geld; fehlendes Risikomanagement kostet mehr.

#### Beispiel 8.4 Hardware-Entwicklungsprojekt (Steinbachwerke — Rechnerbaugruppe)

- Risikofaktor: Abkündigung des eingesetzten Mikroprozessors während 5-jähriger Lieferzeit.
- Normale Prozessoren: 10–20 Jahre lieferbar → trotzdem Abkündigungswahrscheinlichkeit 25 % angesetzt.
- Schaden bei Abkündigung (Neu-/Umentwicklung): 50 Tsd. EUR → Risiko = 25 % × 50 Tsd. = 12,5 Tsd. EUR.
- Bewertete Maßnahmen:
  - Prozessor mit kompatiblem Ersatztyp: Schaden sinkt deutlich (Umstieg auf Ersatztyp trivial), Mehrkosten 1,0 Tsd. EUR wegen leicht schlechterer Leistung → beste Option.
  - Prozessor in großer Stückzahl: Abkündigungswahrscheinlichkeit sinkt deutlich.
  - Prozessor mit Zweitlieferant (Second Source): Wahrscheinlichkeit sinkt noch weiter.
  - Liefergarantie vom Hersteller: Kosten 5 Tsd. EUR.
  - Versicherung: Prämie 6,5 Tsd. EUR.
- Alle Maßnahmen verbessern gegenüber Ausgangssituation; bester Gesamtwert (R + C) beim Prozessor mit kompatiblem Ersatztyp.

#### Eventualfallplanung

- Nicht alle Risiken lassen sich ausschalten; Maßnahmenplanung für vorhersehbare und unvorhergesehene Schadensfälle schon in der Planungsphase erforderlich.
- Vorboten von Schadensfällen: veränderte Verhaltensweisen (Klagen über Kommunikation, Leistungsabfall, Verschlossenheit → mögliche Kündigung), ständige „Restarbeiten" und Verzögerungen bei Ergebnissen (→ vertuschte technische Probleme).
- Für wichtige Risikofaktoren: Indikatoren festlegen, die während Projektdurchführung frühzeitiges Erkennen und Eingreifen ermöglichen.

#### 8.2.4 Risiko-Überwachung

- Risikobewusstsein im Projekt muss aktiv gepflegt werden; Eintrittsindikatoren gezielt beobachten.
- Personelle Risiken: Verantwortung des Projektleiters; informelle Gespräche mit Teammitgliedern; auf zwischenmenschliche Signale achten.
- Technische und organisatorische Risiken: im Rahmen der Projektsteuerung durch Soll-Ist-Vergleich der Fortschrittswerte; Abweichungen auf Risikopotential prüfen.
- Fachliche Risiken: demjenigen Mitarbeiter zuordnen, der auch das Arbeitspaket verantwortet.

#### Beispiel 8.5 Personalrisiko in einem Messgerät-Entwicklungsprojekt

- 160 PT Hardware-Entwicklung von einem Mitarbeiter geplant; Projektlaufzeit 12 Monate.
- Risiko: Kündigung → Einarbeitungszeit Nachfolger ca. 8 Wochen → Projektverzug mindestens 4 Wochen.
- Gegenmaßnahme: Hardware-Arbeitspakete auf 2 Entwickler aufteilen → Ausfall eines Entwicklers nicht mehr projektkritisch.

#### Beispiel 8.6 Fallbeispiel CAD-Software — Risikoportfolio

- Drei identifizierte Risikofaktoren R1–R3 bei Einführung eines neuen CAD-Systems:
  - R1 (Auswahl): Auswahldauer sehr wahrscheinlich zu lang bei 5-Monatsprojektrahmen → Maßnahme: Projektbeginn um 2 Monate verschieben auf Fachesse-Termin, Vorauswahl direkt auf Messe.
  - R2 (Kompatibilität mit bisherigen Datenformaten): Wahrscheinlichkeit moderat, aber möglicher Mehraufwand > 20 % Gesamtbudget → Maßnahme: Exemplarische Altsteuerdateien an Hersteller übergeben, rechtlich bindende Kompatibilitätszusage einholen (Schaden vollständig auf Lieferanten übertragen).
  - R3 (Einarbeitungsaufwand): Wirtschaftlicher Schaden erheblich → Maßnahme: Prototyp-Phase mit einem Mitarbeiter (Schulung + Ablauftest auf neuem System); Systemeinführung für alle erst danach.
- Durch Maßnahmen verschieben sich alle drei Risiken in Richtung geringerer Wahrscheinlichkeit bzw. geringerem Schaden im Risiko-Portfolio.

**Empfohlene Normen und Literatur:**
- ISO 31000: Risikomanagement — Leitlinien; definiert allgemeines Prozessmodell.
- DIN IEC 62198: Risikomanagement für Projekte — Anwendungsleitfaden; basiert auf ISO 31000, spezifisch für Projekte.

---

### Kapitel 9: Kostenmanagement

#### 9.1 Kosten

##### 9.1.1 Grundbegriffe der Kostenrechnung

- Kosten: der gesamte in Geld bewertete Verbrauch von Gütern und Dienstleistungen zur Erstellung einer Leistung.
- Projekt-Kosten entstehen durch: Personalarbeit (Gehälter), Arbeitsplätze und Werkzeuge, Unternehmensinfrastruktur, zugekaufte externe Güter und Leistungen.
- Kostenrechnung erfasst drei Dimensionen:
  - Kostenart: welche Kosten? (Personal, Material, Abschreibungen, Kalkulatorisches, Zulieferung)
  - Kostenstelle: wo entstanden? (Bereiche, Arbeitsgruppen, Aufträge, Projekte)
  - Kostenträger: wofür? (Unternehmen, Abteilungen, Aufträge, Projekte)
- Typische Kostenstellen im Projekt: Teilprojekte, Projektphasen, größere Arbeitspakete.
- Projekt als einzige Kostenstelle: zu wenig Transparenz; Kostenabweichungen nicht lokalisierbar.
- Einzelkosten (direkte Kosten): einem Kostenträger direkt zurechenbar — Löhne, Gehälter, Rechnungsbeträge für Material, Lagerentnahmen.
- Gemeinkosten (indirekte Kosten): nicht direkt zurechenbar (Abteilungsnutzung, Infrastruktur, Schulung, Miete, Zinsen); werden als prozentualer Zuschlag auf direkte Kosten berücksichtigt.

##### 9.1.2 Arbeitskosten

- In personalintensiven Projekten dominieren Arbeitskosten → Stundensatz besonders kritisch.
- Fehler im Stundensatz pflanzen sich proportional auf das gesamte Projekt fort.
- Stundensätze werden nicht individuell, sondern nach Personengruppen einheitlich bestimmt.
- Indirekte Personalkosten fließen als pauschaler Gemeinkostenzuschlag ein.

**Kalkulationsgrößen (Tab. 9.1):**

| Symbol | Bedeutung | Beispielwert |
|---|---|---|
| TA | Nominelle jährliche Arbeitszeit (Personenstunden) | 1.760 Pers.-Std. |
| CP | Korrekturfaktor produktive Arbeitszeit | 0,85 |
| KB | Jährliches Bruttogehalt | 60.000 EUR |
| CV | Korrekturfaktor AG-Anteil Sozialversicherung | 1,26 |
| CS | Korrekturfaktor Arbeitsplatz-Sachkosten | 1,38 |
| KS | Kalkulierter Stundensatz | 69,74 EUR/Pers.-Std. |

- Berechnungsformel Stundensatz:
  KS = (CS · CV · KB) / (CP · TA)
- Jahresbasis stellt sicher, dass saisonale Effekte (Urlaub, Weihnachtsgeld) einbezogen sind.

#### Beispiel 9.1 Stundensatz-Ermittlung Ingenieurdienstleister

- Sachkosten (Raumnutzung, Arbeitsmittel, Fahrzeuge, Reisekosten, Abschreibung, kalkulatorische Kapitalverzinsung) = 4,2 Mio. EUR bei 14,3 Mio. EUR Arbeitskosten → 29,4 % der Arbeitskosten → pauschaler Zuschlag 30 %.
- Arbeitszeitberechnung: 365 Tage − Wochenenden − Feiertage − Urlaub − durchschnittliche Krankheitstage = 211 Arbeitstage.
- Produktive Tage nach Abzug Weiterbildung und Verwaltungsaufwand (ca. 7 % pauschal): 187 produktive Arbeitstage = 1.496 produktive Arbeitsstunden/Jahr.
- Drei Gehaltsgruppen für unterschiedliche Stundensätze: Ingenieure, Techniker, Sonstige.
- Vom monatlichen Bruttogehalt: Jahresbruttogehalt (inkl. Urlaubs- und Weihnachtsgeld) → Brutto-Stundensatz → Aufschlag Arbeitgeberbeiträge Sozialversicherung und Berufsgenossenschaft → Stundensatz für produktive Zeit → Aufschlag 30 % Sachkosten = Arbeitskosten-Stundensatz.

#### 9.2 Kostenplanung in Projekten

Drei Hauptaufgaben der Kostenplanung (Tab. 9.2):

| Aufgabe | Zweck |
|---|---|
| Angebotskalkulation | Angebotserstellung und Vergabeverhandlung |
| Ermittlung des zeitlichen Plankostenverlaufs | Budgetbildung und Kontrolle des Istverlaufs |
| Kostenverteilung auf Teilprojekte und Arbeitspakete | Kontrolle von Soll- und Istverlauf |

##### 9.2.1 Projektkalkulation

- Grobe Kostenschätzung über Kennwerte (Kubatur im Bau, Gewicht im Stahlbau, Programmzeilen in der Software-Entwicklung): schnell, aber nur für ersten Richtwert.
- Genauere Schätzungen durch Zerlegung in Pakete nach Kostenarten (Arbeitskosten, Materialkosten, Zukaufkosten) und Kostenstellen.
- Kostengliederung soll Projektstrukturplan-Gliederung entsprechen (Teilprojekte, ggf. größere Arbeitspakete als Kostenstellen; kleine Pakete nicht einzeln).
- Detaillierungsgrad-Prinzip: so detailliert wie nötig, so grob wie möglich.
- ABC-Analyse + Pareto-Prinzip: A-Faktoren (≈ 80 % der Kosten) detailliert schätzen; B-Faktoren genauer; C-Faktoren durch prozentualen Zuschlag.
- Zukäufe passend zur Projektgliederung aufteilen (nicht als Block).
- Plankostengliederung und Istkostengliederung müssen übereinstimmen → Kontrolle und Steuerung möglich.
- Arbeitskosten = Aufwandsschätzwerte (aus Terminplanung) × Stundensätze.
- Verantwortliche der Teilprojekte/Arbeitspakete einbinden: präzisere Schätzungen und höhere Akzeptanz der Kostenziele.
- Gesamter Projektlebenszyklus berücksichtigen (life cycle costing): Vorprojektarbeiten und Restarbeiten nach Abnahme.
- Achtung: Projekte werden oft „schön gerechnet" durch Umbuchen von Projektkosten auf andere Kostenstellen — kurzfristig verlockend, aber Kosten fallen trotzdem an.

##### 9.2.2 Kostenverteilung

- Kostenverteilung auf Zeitperioden: aus Ablauf- und Terminplan + Kostenschätzungen je Arbeitspaket → monatliche oder quartalsweise Plankosten.
- Kostenstellenbetrachtung: lokalisiert Kostenabweichungen; Ursachen identifizierbar und korrigierbar.

#### Beispiel 9.2 Kostenplanung — Projekt mit 7 Teilprojekten

- Projektzeitraum: Anfang April bis Mitte März des Folgejahres.
- Gliederung: 7 Teilprojekte (TP1–TP7), 4 Projektphasen (I–IV).
- Kostenarten je Teilprojekt: Personalkosten (PK), Materialkosten (MK), Zukaufkosten (ZK), Summe (SK) in Tsd. EUR.
- Phasenbudgets: I = 39, II = 67, III = 123, IV = 26 Tsd. EUR.
- Gesamtkosten: 255 Tsd. EUR (Summation aller SK).
- Monatliche Plankosten und kumulierte Plankostensumme:

| Monat | Apr | Mai | Jun | Jul | Aug | Sep | Okt | Nov | Dez | Jan | Feb | Mär |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Monatliche PK (Tsd. EUR) | 27 | 12 | — | 26 | 28 | 38 | 31 | 43 | 20 | 11 | 8 | 8 | (ca. 3 in Mär) |
| Kum. PK (Tsd. EUR) | 27 | 39 | 65 | 93 | 131 | 162 | 205 | 225 | 236 | 244 | 252 | 255 |

- Phasen passen nicht exakt in Monatsraster; in manchen Monaten fallen Kosten aus verschiedenen Phasen an.

#### 9.3 Kostencontrolling mittels Earned Value Analyse

##### 9.3.1 Aufgabe und Ziele des Kostencontrollings

- Aufgabe: Kostenverlauf so steuern, dass Kostenziele aus Projektdefinition eingehalten werden.
- Drei Kostenkategorien parallel verfolgen:
  - Plankosten: zeitlich geplanter Kostenverlauf.
  - Istkosten: tatsächlich angefallene Kosten.
  - Sollkosten: aus tatsächlichem Projektfortschritt abgeleitete erwartete Kosten (notwendig bei Abweichungen vom Planverlauf, z. B. wegen Verzögerungen oder Vorziehen von Arbeitspaketen).
- Regelmäßige Aufgabe: Istkosten erfassen, Sollkosten berechnen, Plan/Ist/Soll vergleichen, bei Abweichungen korrigierend eingreifen.
- Earned Value Analyse (EVA): bekannteste Methode des Kostencontrollings — analysiert Projektfortschritt aus Sicht von Aufwand und Nutzen.
- EVA-Grundprinzip: bei normalem Projektverlauf sollten geschaffener Nutzwert und eingesetzter Aufwand übereinstimmen; Abweichungen zwischen geplanten, tatsächlichen und erarbeiteten Werten zeigen Kosten- und Zeitprobleme frühzeitig.
- Beobachtungsfrequenz EVA: ca. alle 2–4 Wochen.
