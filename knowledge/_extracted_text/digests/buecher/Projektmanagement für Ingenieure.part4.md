# Projektmanagement für Ingenieure — Teil 4
> Quelle: Projektmanagement für Ingenieure (buecher) · Seiten 161-200.

Dieser Teil schließt Kapitel 5 (Strukturplanung) ab und behandelt dann vollständig Kapitel 6 (Projektschätzung) sowie den Beginn von Kapitel 7 (Ablauf- und Terminplanung). Kernthemen: Arbeitspaket-Beschreibung, Schätzmethoden, mathematische Grundlagen der Schätzung (Wahrscheinlichkeit, Normalverteilung, Zwei-/Dreipunktschätzung), das CoCoMo-Modell für Software-Aufwand sowie Anordnungsbeziehungen und Netzplantechniken (CPM, MPM).

## Inhalt

### 5.3 Vorgänge festlegen

#### 5.3.1 Arbeitspakete beschreiben

Ein Arbeitspaket (AP) ist die kleinste im Projektmanagement aktiv geplante Arbeitseinheit. Unterhalb dieser Ebene ist es Sache der einzelnen Mitarbeiter, die Arbeiten eigenständig zu gliedern.

**AP-Beschreibung: Aufbau und Anforderungen**
- Beschreibt Input (Voraussetzungen), auszuführende Schritte und angestrebten Output (Ergebnis)
- Kopfdaten: Projektname, Projektnummer, Projektleiter, fachliche Qualifikation der Bearbeiter, verantwortliche Person
- Personelle Zuordnung und Aufwand/Dauer können zunächst offen bleiben und werden in späteren Planungsschritten ergänzt
- Umfang: maximal eine Seite; Stichpunkte genügen (richtet sich am Qualifikationsniveau der Bearbeiter aus)
- Format sollte im Projekt standardisiert und als Formular im PM-Handbuch verfügbar sein

**Fallbeispiel „Solaranlage" — AP Beschaffung Solarmodule (Beispiel 5.8)**
- Auszuführende Arbeiten und angestrebtes Ergebnis präzise beschrieben
- Zuordnung zur Einkaufsabteilung und personelle Benennung bereits vorgenommen
- Voraussetzende Arbeitspakete benannt
- Arbeitsaufwand und Dauer noch offen (werden in der Ablaufplanung bestimmt)
- Festgestellte Mängel: fehlende Projektleiter-Benennung, fehlende Projektnummer (kann zu Verwechslungen führen), unübersichtliche dezimale AP-Nummerierung (für baumartigen PSP wäre untergliederte Codierung besser), noch keine Vorgangstermine eingetragen

#### 5.3.2 Vorgänge definieren

Ein Vorgang ist die zeitabhängige Abarbeitung aller Schritte eines Arbeitspakets — er hat einen definierten Anfang, ein definiertes Ende und erfordert einen bestimmten Aufwand.

**Ideale Vorgangsdauer**
- Untergrenze: 1 Personentag bzw. 1 Kalendertag (kleinerer Umfang erzeugt unverhältnismäßig hohen Planungs- und Steuerungsaufwand)
- Obergrenze: ca. 20 Tage (größere Pakete erhöhen das Risiko, Planabweichungen zu spät zu bemerken)
- Typischer Richtwert: 5 Tage (eine Woche) — Mitarbeiter erhält Auftrag und meldet Erledigung selbstständig zurück
- Bei unerfahrenen Zuständigen: kürzere Dauer bevorzugen
- Faustregel: Ein AP sollte möglichst einer einzelnen Person zugeordnet werden; bei mehreren Personen muss eine die Gesamtverantwortung tragen

**Beispiel PLT-Projekte — NAMUR NA 35 (Beispiel 5.7)**
- Prozessleitsysteme zur Automatisierung verfahrenstechnischer Anlagen sind neuartig und einmalig
- NAMUR (internationaler Verband Automatisierungstechnik Prozessindustrie) untersuchte zahlreiche PLT-Projekte und dokumentierte Gemeinsamkeiten im Arbeitsblatt NA 35 als Standard-Projektstruktur
- Typisches PLT-Projekt: 26 Einzelaktivitäten, 7 Projektphasen
- Aufwand für Projekt- und Qualitätsmanagement: ca. 7–10 % des Gesamtaufwands (in den Einzelaktivitäten enthalten)
- Aufwandsermittlung je Einzelaktivität als Prozentwert des Gesamtaufwands dokumentiert

---

### Kapitel 6: Projektschätzung

#### 6.1 Methodische Grundlagen des Schätzens

##### 6.1.1 Ziel des Schätzens

Aus dem PSP lassen sich Aussagen zu Ablauf, Ressourcen, Kosten, Terminen und Projektdauer nur ableiten, wenn Schätzwerte für Zeitaufwand, Materialbedarf und sonstige Kosten vorliegen. Projekte sind per Definition neuartig — daher ist detailsichere Planung ohne Schätzung nicht möglich.

**Spektrum: Raten — Schätzen — Wissen**
- Raten: keinerlei verwertbare Information vorhanden, Verlässlichkeit 0 %
- Wissen: vollständige Information, Verlässlichkeit 100 %
- Schätzen: partielle Ungewissheit — der Normalfall in Projekten

Aus praktisch jeder Situation lassen sich verwertbare Informationen gewinnen: Ober-/Untergrenzen für den Wertebereich, Hilfsgrößen die mit der Zielgröße korrelieren, Erfahrungswerte aus ähnlichen Projekten oder Teilaufgaben. Die Aufgabe des Schätzens besteht darin, diese Informationen zugänglich zu machen und daraus belastbare Schlussfolgerungen zu ziehen.

**Psychologische Aspekte**
- Menschen bevorzugen präzise Aussagen oder gar keine — Schätzung erzeugt Unbehagen
- Drohende Bestrafung für Fehlschätzung führt zu verdecktem Einbau von Sicherheitspuffern
- Fertige Arbeit wird künstlich verzögert, um keine zu großzügige Schätzung zu offenbaren
- Lösung: motivationsfreie Schätzung (Schätzen ohne Angst vor Konsequenzen) und schätzungsfreie Motivation (Leistungsanreize nicht aus Schätzwerten ableiten)

**Fallbeispiel Landflächenschätzung (Beispiel 6.1)**
- Spontanschätzung ohne Hilfsmittel: Bandbreite 100 Tsd. km² bis 1000 Mio. km² (Faktor 10⁴)
- Weg über Bevölkerungsdichte: Deutschland 400 Tsd. km², 80 Mio. Ew. → 200 Ew./km²; Weltbevölkerung ca. 6 Mrd. bei Dichte 4–10× geringer → Landfläche ca. 120–300 Mio. km²
- Weg über Kugelgeometrie: Erdumfang 40 Tsd. km, Landanteil 30 % → ca. 160 Mio. km²
- Erdumfang notfalls aus Roman-Daten ableitbar (80 Tage, 10 h/Tag, 50 km/h → ~40 Tsd. km)

##### 6.1.2 Schätzmethoden

**Intuitive Schätzung**
- Einzelperson oder Gruppe äußert „gefühlte" Einschätzung, mit oder ohne Begründung
- Qualität steigt mit Erfahrung der Schätzenden; bei Experten manchmal Spontanschätzung besser als durchdachte
- Große Streuungen und Unsicherheiten; Nicht-Fachleute liefern Werte die um Zehnerpotenzen auseinanderliegen können
- Einsatz: nur zur groben Eingrenzung der Werteskala in frühen Phasen

**Vergleichende Schätzung**
- Abgeschlossene Projekte aufsteigend nach Gesamtaufwand sortiert und in einer Skala dargestellt
- Neues Projekt qualitativ eingeordnet: „deutlich mehr als P1", „vergleichbar mit P4", usw.
- Anwendbar auch für einzelne Arbeitspakete durch Vergleich mit fachlich ähnlichen AP
- Voraussetzung: Erfahrungen aus vergleichbaren Projekten vorhanden; daher Nachbetrachtung jedes Projekts empfohlen

**Quantitative Schätzung — Kennzahlen**
- Aufwand proportional zu dominierendem Einflussparameter: A = C₀ · E₀
- Beispiele: 10 €/kg bei Stahlkonstruktionen; 400 €/m³ umbautem Raum; 3 Personenmonate/1000 Programmzeilen
- Mehrere Parameter als Linearkombination: A = Σᵢ Cᵢ · Eᵢ

**Tabelle: Gebäudekostenkennzahlen (Beispiel 6.2 / Tab. 6.1)**

| Gebäude | Nutzfläche | Kosten | Kosten/m² |
|---|---|---|---|
| Taipeh 101 (1999–2004) | 412 Tsd. m² | 1600 Mio. € | 3.900 € |
| Burj Dubai (2004–2010) | 517 Tsd. m² | 1400 Mio. € | 2.700 € |
| Dom Aquaree Hotel Berlin (2003) | 67 Tsd. m² | 340 Mio. € | 5.100 € |
| Messeturm Frankfurt (1988–1990) | 61 Tsd. m² | 250 Mio. € | 4.000 € |
| Kanzleramt Berlin (1997–2001) | 19 Tsd. m² | 250 Mio. € | 13.100 € |
| Klinikum Frankfurt-Höchst (2016–2021) | 34,5 Tsd. m² | 263 Mio. € | 7.600 € |
| Einfamilienhaus | 150 m² | 600 Tsd. € | 4.000 € |

Trotz Faktor 6,5 Unterschied in Kosten/m² ist die Kennzahl ein nützlicher erster Schätzparameter.

**Kalkulationsschema für Entwicklungskosten (Beispiel 6.3 / Tab. 6.2)**

Bei einem Hersteller programmierbarer Messgeräte wurde durch Auswertung abgeschlossener Projekte folgendes Schätzmodell erarbeitet: Zunächst werden nur die Realisierungsaufwände geschätzt — Gehäusekonstruktion (E₁), Elektronik-Realisierung (E₂), Programmierung (E₃). Daraus hochgerechnet:

| Bereich | PM | Analyse | Entwurf | Realisierung | Test | Doku | Faktor |
|---|---|---|---|---|---|---|---|
| Gehäuse | E₁·0,10 | — | E₁·0,25 | E₁ | E₁·0,25 | — | ×1,6 |
| Elektronik | E₂·0,10 | — | E₂·0,25 | E₂ | E₂·0,75 | E₂·0,40 | ×2,5 |
| Programm | E₃·0,15 | — | E₃·0,20 | E₃ | E₃·0,85 | E₃·0,30 | ×2,5 |

Gesamtaufwand: A = 1,6 · E₁ + 2,5 · E₂ + 2,5 · E₃

Zahlenbeispiel: E₁ = 30 PT, E₂ = 60 PT, E₃ = 70 PT → A = 48 + 150 + 175 = 403 PT ≈ 20 Personenmonate

**Zerlegung der Schätzgröße**
- Gesamtgröße in Einzelkomponenten zerlegen, jede separat schätzen, dann summieren: A = Σᵢ Aᵢ
- Durch Überlagerung positiver und negativer Abweichungen ist Gesamtschätzung in der Regel genauer als die Einzelschätzungen
- Anwendung im PSP: Zeitaufwand je AP schätzen und summieren

**Fallbeispiel Solaranlage — Aufwandsschätzung (Beispiel 6.4)**
- Personalaufwand schwierig direkt zu schätzen, einfacher wenn AP einzeln aufgelistet werden
- Einzelne, kleinere AP sind besser schätzbar als komplexe zusammengesetzte Arbeiten
- Auflistung reduziert Gefahr, AP komplett zu vergessen

**Kombination mehrerer Schätzmethoden**
- Fehler in einem Ansatz fallen durch anderen Ansatz auf → gegenseitige Korrektur
- Wertebereich wird weiter eingeschränkt, Aussage gefestigt

**Gruppenschätzung**
- Mehrere Experten unabhängig schätzen, dann mitteln → Gruppenresultat besser als Einzelresultat
- Gilt nur bei annähernd gleichem Qualifikationsniveau; ein einzelner Experte schlägt eine Gruppe von Laien

**Delphi-Methode**
- Entwickelt von Rand Corporation in den 1960er Jahren
- Ablauf: Experten schätzen unabhängig → Werte werden präsentiert und begründet (keine Überzeugungsdiskussion, nur Gedankengänge offenlegen) → jeder korrigiert ggf. eigene Schätzung → erneutes Schätzen → Mittelwert als Ergebnis

**Schätzklausur**
- Gruppe von ca. 3 bis 7 Experten erhält Projektinformationen
- Jeder erstellt individuelle Vorab-Schätzung für AP und Teilprojekte
- Austausch und Besprechung der Werte; bei großen Diskrepanzen treten Risiken und implizite Annahmen zutage
- In der Regel Annäherung der Schätzwerte; abschließend gemeinsam getragenes Ergebnis

**Tabelle: Schätzmethoden im Vergleich (Tab. 6.3)**

| Methode | Merkmale |
|---|---|
| Intuitiv | Minimaler Aufwand, sehr große Unsicherheit |
| Vergleichend | Einfach, unsicher |
| Kennzahlen | Steigender Aufwand, steigende Sicherheit |
| Zerlegung | Bei gleicher Einzel-Unsicherheit steigt Gesamt-Sicherheit |
| Kombination | Unterschiedliche Wege nutzen |
| Gruppe | Gruppe schätzt besser als Einzelperson |

**Planning Poker (für agile Projekte)**
- Schätzt Umfang von Anforderungspaketen (User-Stories aus dem Product Backlog) in abstrakten Story Points, nicht in Personentagen
- Skala: exponentiell ansteigend, angelehnt an Fibonacci; Cohn-Zahlenreihe: 1, 2, 3, 5, 8, 13, 20, 40, 100
- Interpretation: Paket mit 3 Story Points ist dreimal so umfangreich wie Paket mit 1 Point; hohe Punktzahl = hohe Unsicherheit
- Ablauf: jedes Mitglied wählt in Runde 1 eine Karte; Karten werden gleichzeitig aufgedeckt; Person mit höchstem und niedrigstem Wert erläutert Gedankengang; erneute Runde bis Konvergenz
- Bleiben Diskrepanzen groß: noch Klärungsbedarf für dieses Anforderungspaket
- Zu Projektbeginn: alle User-Stories schätzen; laufend neue Stories und Korrekturen vorhandener Schätzungen
- Sprint Velocity: am Sprint-Ende ermittelte realisierte Story Points → Basis für nächste Sprint-Planung
- Vorteil: besseres Verständnis der Aufgabe, breite personelle Basis
- Nachteil: erheblicher Aufwand, Subjektivität

##### 6.1.3 Bedingungen des Schätzens

**Schätzaufwand vs. Schätzgenauigkeit**
- Je größer der investierte Schätzaufwand, desto zuverlässiger das Ergebnis
- Bei ca. 1 % Schätzaufwand: Unsicherheit ca. −25 bis +75 %
- Bei ca. 5 % Schätzaufwand: deutlich geringere Unsicherheit
- In der Praxis: einfache Verfahren für erste grobe Aussage, dann aufwändigere Verfahren zur Steigerung der Sicherheit

**Häufige Schätzfehler**
- Tendenz zur Unterschätzung: besonders bei neuen Themen und selten schätzenden Mitarbeitern; zu frühe Berücksichtigung knapper Ressourcen
- Tendenz zur Überschätzung: um zugesagte Leistung sicher erbringen zu können
- Lösung: motivationsfreie Schätzung (allein auf Verlässlichkeit ausgerichtet) + schätzungsfreie Motivation (Leistungsanreize unabhängig von Schätzwerten)

---

#### 6.2 Mathematische Grundlagen des Schätzens

##### 6.2.1 Wahrscheinlichkeitsrechnung

Eine unbekannte Schätzgröße wird als Zufallsvariable X beschrieben.

**Grundbegriffe**
- Verteilungsfunktion: F(x) = P(X ≤ x) — gibt an, mit welcher Wahrscheinlichkeit X einen Wert ≤ x annimmt; beginnt bei 0, steigt stetig auf 1 an
- Dichtefunktion: p(x) = P(X = x) = F'(x) — Wahrscheinlichkeit, dass exakt Wert x angenommen wird
- Schmale Dichtefunktion = geringe Unsicherheit; breite = hohe Unsicherheit
- „Wissen": Dichtefunktion hat an einer einzigen Stelle den Wert 1
- „Raten": Dichtefunktion geht überall gegen 0

**Wichtige Verteilungstypen**
- Gleichverteilung: Minimalwert a, Maximalwert b; alle Zwischenwerte gleich wahrscheinlich (rechteckförmige Dichtefunktion); wird oft mangels besserem Wissen angenommen
- Dreiecksverteilung: drei Werte nötig — Minimum a, Maximum b, wahrscheinlichster Wert c; realistischer als Gleichverteilung (Randwerte weniger wahrscheinlich)
- Beta-Verteilung: weitere Verdichtung zur Mitte hin; Basis für Zwei-/Dreipunktschätzung

**Kennwerte zur Charakterisierung**
- Erwartungswert: E = ∫ x · p(x) dx ≈ Σᵢ xᵢ · p(xᵢ) (Formel 6.5) — Schwerpunkt der Fläche unter der Dichtefunktion
- Median M: teilt die Fläche unter der Dichtefunktion in zwei gleiche Hälften (je 50 %)
- Modus W: Wert, bei dem Wahrscheinlichkeit maximal wird
- Bei symmetrischen Dichtefunktionen: E = M = W; bei unsymmetrischen können sie abweichen
- Varianz: V = E{(x−E)²} = ∫ (x−E)² · p(x) dx (Formel 6.8)
- Standardabweichung: S = √V (Formel 6.9) — Maß für Schätzunsicherheit

**Fallbeispiel Projektdauer-Schätzung (Beispiel 6.5)**
- 8 Projektbeteiligte schätzen unabhängig, Gewichtung mit 20 Punkten je Person
- Kleinster genannter Wert: 20 Arbeitstage; größter: 50 Arbeitstage
- Aus der gemittelten Dichtefunktion ermittelt:
  - Wahrscheinlichster Wert W = 28,0 Tage
  - Median M = 30,8 Tage
  - Erwartungswert E = 32,0 Tage
  - Standardabweichung S = 5,9 Tage

##### 6.2.2 Die Normalverteilung

Die Normalverteilung (Gaußsche Glockenkurve) ist in Theorie und Praxis von zentraler Bedeutung.

**Eigenschaften**
- Symmetrisch um den Erwartungswert; E = M = W
- Vollständig durch Erwartungswert E und Standardabweichung S bestimmt
- Gültigkeit durch zentralen Grenzwertsatz: Summe vieler unabhängiger, beliebig verteilter Zufallsvariablen nähert sich mit steigendem n der Normalverteilung an → Projektgesamtschätzung (als Summe vieler Teilschätzungen) ist normalverteilt, unabhängig von den Einzelverteilungen

**Wahrscheinlichkeitswerte der Normalverteilung (Tab. 6.4)**

Bei x = E + z · S gilt:

| z | P(x < E − z·S) [%] | P(E − z·S < x < E + z·S) [%] | P(x < E + z·S) [%] |
|---|---|---|---|
| 0,000 | 50,0 | 0,0 | 50,0 |
| 0,524 | 30,0 | 40,0 | 70,0 |
| 1,000 | 15,87 | 68,27 | 84,13 |
| 1,282 | 10,0 | 80,0 | 90,0 |
| 1,645 | 5,0 | 90,0 | 95,0 |
| 2,000 | 2,28 | 95,45 | 97,72 |
| 3,090 | 0,1 | 99,8 | 99,9 |

**Praktische Schlussfolgerungen für die Terminplanung**
- Nur 50 % Wahrscheinlichkeit, ein Projekt bis zum Erwartungswert E fertigzustellen — genau so verlässlich wie Roulette auf „Rouge"
- Werden wahrscheinlichste Werte (Modus) statt Erwartungswerte summiert, sinkt die Erfolgswahrscheinlichkeit noch weiter (Modus liegt aufgrund der Schiefe unter E)
- Für 84 % Wahrscheinlichkeit: Zusagetermin = E + 1 · S
- Für 98 % Wahrscheinlichkeit: Zusagetermin = E + 2 · S

**Fallbeispiel Aufwand und Laufzeit (Beispiel 6.6)**
- PSP mit Gesamt-Erwartungswert E = 240 PT, Standardabweichung S = 32 PT
- Team-Vorschlag Planwert 240 PT: nur 50 % Wahrscheinlichkeit → vom PL abgelehnt
- Einigung auf 272 PT (= 240 + 1,0 · 32) → Wahrscheinlichkeit 84 %
- Argument des PL „nicht weniger als 200 PT" (= 240 − 1,25 · 32 → ca. 90 % richtig) riskant, weil der genannte Zahlenwert 200 beim Auftraggeber als Planwert hängen bleibt

##### 6.2.3 Zwei- und Dreipunktschätzung

**Zweipunktschätzung**
- Angabe: Minimalwert a, Maximalwert b
- Erwartungswert: E = (a + b) / 2 (Formel 6.10)
- Standardabweichung (Beta-Verteilungsannahme): S = (b − a) / 6 (Formel 6.11)

**Dreipunktschätzung**
- Angabe: Minimalwert a, Maximalwert b, wahrscheinlichster Wert c (muss nicht in der Mitte liegen)
- Erwartungswert: E = (a + 4·c + b) / 6 (Formel 6.12)
- Standardabweichung: S = (b − a) / 6 (Formel 6.13, identisch mit Zweipunktschätzung)

**Fallbeispiel Projektdauer-Vergleich (Beispiel 6.7)**
- Eingabewerte: a = 20 Tage, b = 50 Tage, c = 28 Tage
- Zweipunktschätzung: E = 35,0 Tage, S = 5,0 Tage
- Dreipunktschätzung: E = 30,3 Tage, S = 5,0 Tage
- Vergleich mit Exaktwerten (E = 32,0, S = 5,9): Dreipunktschätzung näher am Exaktergebnis
- Gleichverteilung hätte ergeben: E = 35,0, S = 8,7 Tage
- Dreiecksverteilung: E = 32,7, S = 6,3 Tage
- Schluss: Je mehr Informationen über die Verteilungsform (Randwerte unwahrscheinlicher), desto geringere Standardabweichung

**Additivität von Erwartungswert und Varianz**
- Erwartungswert der Summe = Summe der Erwartungswerte: E = Σᵢ Eᵢ (Formel 6.14)
- Standardabweichung der Summe = Wurzel der Summe der Einzelvarianzen: S = √(Σᵢ Sᵢ²) (Formel 6.15)
- Durch die Wurzelfunktion ist die Gesamt-Standardabweichung typischerweise kleiner als die Summe der Einzel-Standardabweichungen → getrennte Schätzung der Teilgrößen verbessert die Gesamtschätzgenauigkeit erheblich

**Fallbeispiel Aufwandsschätzung 7 AP (Beispiel 6.8)**
- Projekt aus 7 Arbeitspaketen (AP1–AP7), je mit optimistischem (a), pessimistischem (b) und realistischem (c) Wert
- Dreipunktformel liefert je AP: E und S
- Ergebnis der zusammengesetzten Schätzung: E = 174,8 Tage, S = 16,5 Tage
- Direkte Gesamtschätzung (a = 90, b = 307, c = 163): E = 174,8 Tage, S = 36,2 Tage
- Gleicher Erwartungswert, aber deutlich geringere Standardabweichung durch getrennte AP-Schätzung

---

#### 6.3 Schätzung der Projektdauer

**Grundformel**
- T = A / (L · P) (Formel 6.16)
- T = Zeitdauer, A = Arbeitsaufwand, L = Leistung (0 bis 1), P = Personenzahl

Beispiel: AP mit 20 Personentagen → bei 1 Person mit 100 % Leistung = 20 Arbeitstage; bei 2 Personen = 10 Tage; bei 0,5 Leistung = 40 Tage

**Nichtlinearität bei größerem Personaleinsatz**
- Theoretisch: beliebige Parallelisierung möglich → Zeitdauer beliebig verkürzbar
- Praktisch: mit steigender Personenzahl N wächst Kommunikationsaufwand A₁ (mindestens linear, realistisch exponentiell)
- Gesamtaufwand: A = A₀ (Arbeitsaufwand) + A₁ (Kommunikationsaufwand)
- Zeitdauer T als Funktion der Personenzahl N zeigt ein Minimum; ober- und unterhalb des Optimums steigt T
- Unterhalb des Optimums (N < optimal): langsamer Anstieg der Laufzeit
- Oberhalb: zunächst langsamer, dann stärker ansteigend
- Bei N < 1 (Person nur Teilzeit): Leistungsverlust durch zeitaufwändiges Umdenken

**Parallelisierungsgrenzen**
- Manche Arbeiten können grundsätzlich nicht beliebig parallelisiert werden (natürliche Obergrenze)
- Beispiel: Grubenausschachtung 1m × 1m × 1m — 20 Arbeiter gleichzeitig nicht möglich (kein Platz)
- Laufzeit-Minimierung erfordert genaue Planung parallelisierbarer vs. serieller Teilaufgaben (→ Ablaufplanung Kapitel 7)

---

#### 6.4 Schätzung des Aufwands bei Software-Systemen — CoCoMo

**CoCoMo (Constructive Cost Model)**
- Entwickelt von Barry Boehm (1981), basierend auf Auswertung von 63 Software-Projekten (2 KLOC bis 966 KLOC; 6 PM bis 11.400 PM)
- Grundprinzip: Aufwand A hängt im Wesentlichen von der Programmlänge L ab; Programmlänge ist besser vorhersagbar als Aufwand direkt

**Messgröße Programmlänge**
- Einheit: KLOC (Kilo Lines of Code) bzw. KDLI (Kilo Delivered Lines of Instruction)
- Nur Quellcode-Zeilen gezählt; Kommentare, Dokumentation und Hilfs-/Testkode ausgeschlossen
- 1 Personenmonat = 152 Personenstunden; 12 Personenmonate = 1 Personenjahr

**Basic Model (Formel 6.17)**
- A = C₁ · L
- Ermittelter Wertebereich: C₁ = 1 … 40 [PM/KLOC]
- Mittelwert: C₁ = 3 [PM/KLOC] → Produktivität 1/C₁ = 0,333 KLOC/PM = 2,2 LOC/Stunde
- Hohe Varianz → nur als sehr grober Schätzwert verwendbar; berücksichtigt alle Projektphasen (Analyse, Entwurf, Test, Doku)

**Erweitertes Modell (Formel 6.18)**
- A = C₁ · L^C₂
- C₂ > 1 berücksichtigt überproportionalen Aufwandsanstieg bei großen Projekten
- C₂-Bereich: 1,05 bis 1,20

**Drei Projekttypen**

| Eigenschaft | Organic | Semi-Detached | Embedded |
|---|---|---|---|
| Organisation versteht Zielsetzung | Gründlich | Einigermaßen | In Grundzügen |
| Erfahrung mit ähnlichen Systemen | Viel | Mittel | Etwas |
| Einhaltung externer Schnittstellen | Etwas | Mittel | Sehr stark |
| Parallele Entwicklung mit HW/Prozessen | Wenig | Etwas | Stark |
| Neue Technologien nötig | Gering | Etwas | Merklich |
| Softwareumfang | < 50 KDLI | < 300 KDLI | Jede Größe |

**CoCoMo-Parameter nach Projekttyp (Tab. 6.5)**

| Parameter | Organic | Semi-Detached | Embedded |
|---|---|---|---|
| C₁ | 2,4 | 3,0 | 3,6 |
| C₂ | 1,05 | 1,12 | 1,20 |
| C₃ | 2,5 | 2,5 | 2,5 |
| C₄ | 0,38 | 0,35 | 0,32 |

**Optimale Projektdauer und Teamgröße (Formel 6.19)**
- D = C₃ · A^C₄ (optimale Dauer in Monaten)
- N = A / D (optimale Teamgröße)

**Fallbeispiel Projektierungs-Software (Beispiel 6.9)**
- Programm: grafischer Editor, Symbol-Datenbank, Auswerteteil
- Geschätzte Programmlänge: 33.000 Zeilen (33 KLOC) durch Vergleich
- Projekttyp: organic (entsprechende Vorkenntnisse vorhanden)
- Berechnung: A = 2,4 · 33^1,05 = 94,3 Personenmonate; D = 2,5 · 94,3^0,38 = 14 Monate; N = 6,8 Mitarbeiter

**Fallbeispiel Transportbahn-Berechnungsprogramm (Beispiel 6.10)**
- Vorhandenes Basic-Programm (~30 Jahre alt, spartanische Oberfläche) sollte in C++ neu geschrieben werden
- Basic-Quellcode: 56 Seiten × 50 Zeilen = 2800 Zeilen → L = 2,8 KLOC
- Dateigröße: 91.386 Zeichen → 33 Zeichen/Zeile (plausibel)
- Schätzung: A = 2,4 · 2,8^1,05 = 7,1 PM; D = 2,5 · 7,1^0,35 = 4,95 Monate; N = 1,4 Mitarbeiter
- Tatsächliches Ergebnis: C++-Quellcode 2839 Zeilen (113.864 Byte); 1 Mitarbeiter; Fertigstellung inkl. Test und Doku in knapp 7 Monaten (längere Laufzeit wegen Einzelperson, aber Aufwand sogar etwas unter Schätzung)

**Korrekturfaktoren (Erweitertes CoCoMo, Formel 6.20)**
- 15 multiplikative Korrekturfaktoren Eᵢ: A = C₁ · L^C₂ · Π₁₅ Eᵢ
- Im Normalfall Eᵢ = 1; Variation nach oben/unten je nach Projektmerkmalen
- Details: Boehm 1981

**Weiterführende Literatur**
- Hummel, O.: Aufwandsschätzungen. Spektrum Akademischer Verlag, 2011 — Kompaktdarstellung wichtigster Schätzmethoden, Fokus Software-/Systementwicklung
- Boehm, B.: Software Engineering Economics. Prentice Hall, 1981 — Wirtschaftlichkeitsbetrachtungen und Kostenermittlung für Softwareerstellung

---

### Kapitel 7: Ablauf- und Terminplanung (Beginn)

#### 7.1 Ablaufmodelle

##### 7.1.1 Anordnungsbeziehungen

Die Ablaufplanung erfasst zunächst die logischen Kopplungen zwischen Arbeitspaketen. Vier Grundtypen:

**Vier Anordnungsbeziehungen**
- Normalfolge (EA — Ende-Anfang): Nachfolger kann erst starten, wenn Vorgänger vollständig abgeschlossen; häufigste Beziehung
- Anfangsfolge (AA — Anfang-Anfang): Beginn zweier Arbeiten aneinander gekoppelt; typisch bei parallel startenden Arbeiten mit fester Startreihenfolge
- Endefolge (EE — Ende-Ende): Abschluss zweier Arbeiten aneinander gekoppelt; typisch bei parallel endenden Arbeiten mit fester Endreihenfolge
- Sprungfolge (AE — Anfang-Ende): erste Arbeit kann erst enden, wenn zweite begonnen hat; notwendig bei erzwungener Überlappung

**Verzweigung und Zusammenführung**
- Verzweigung: Ende einer Arbeit löst Start mehrerer Folgearbeiten aus
- Zusammenführung: mehrere Arbeiten müssen abgeschlossen sein, bevor eine Folgearbeit starten kann

**Zeitparameter**
- Positiver Zeitparameter: Folgeereignis tritt erst einige Zeit nach Vorgängerereignis ein (z.B. Aushärtezeit, externe Lieferzeit ohne eigenen Aufwand)
- Negativer Zeitparameter: logisch abhängiges Ereignis muss zeitlich vor dem Vorgänger stattfinden (zeitliche und logische Reihenfolge unterscheiden sich)
- Exakter, minimaler oder maximaler Zeitabstand möglich

**Fallbeispiel Bodenplatte Großbaustelle (Beispiel 7.1 / Tab. 7.1)**

| Nr. | Arbeitspaket | Aufwand | Anordnungsbeziehung |
|---|---|---|---|
| 1 | Armierung | 1 Tag | — |
| 2 | Schalung | 1 Tag | — |
| 3 | Beton liefern | 8 h | 1EA; 2EA |
| 4 | Betonieren Frühschicht | 5 h | 3AA−1 Stunde; 5AE |
| 5 | Betonieren Spätschicht | 5 h | 3EE |
| 6 | Steine liefern | 1 Tag | 5EA + 2 Tage |

- Armierung und Schalung: vollständig fertig vor Betonlieferung (Normalfolge)
- Betonlieferung und Betonieren Frühschicht: Anfangsfolge mit negativem Zeitparameter −1 Stunde (Frühschicht muss schon da sein bevor Beton kommt)
- Früh- und Spätschicht: Sprungfolge (Frühschicht darf erst enden wenn Spätschicht begonnen hat)
- Spätschicht und Betonlieferung: Endefolge (Spätschicht endet erst wenn Lieferung fertig)
- Steine liefern: Normalfolge nach Spätschicht + 2 Tage Aushärtezeit

**Fallbeispiel Temperaturmessbox (Beispiel 7.2)**
- Messbox für Pizza-Produktionslinie: berührungslose Temperaturmessung, Aufzeichnung, drahtlose Übertragung
- Ablauf: Aufgabenanalyse → parallel Gehäuseauswahl / Schaltungsentwurf / Programmierung → Schaltungsaufbau nach Entwurf → Programmtest nach Programmierung → Systemtest nach HW+SW-Test → Montage + Inbetriebnahme

Anordnungsbeziehungen betreffen die Projektsteuerung direkt: Verzögerung eines Pakets pflanzt sich über die Beziehungen auf Folgepakete fort. Frühe Arbeitspakete mit vielen Abhängigkeiten sind besonders kritisch → Arbeiten möglichst entkoppeln und Puffer einbauen.

##### 7.1.2 Netzpläne

**Drei Grundelemente eines Netzplans**
- Vorgang: zeiterforderndes Geschehen mit definiertem Anfang und Ende; entspricht einem AP; wichtigste Kenngröße: Zeitdauer
- Ereignis: Zustandsübergang zu einem bestimmten Zeitpunkt, besitzt selbst keine Zeitdauer (typisch: Beginn/Abschluss von Vorgängen)
- Beziehung: zeitliche oder logische Kopplung zwischen Vorgängen/Ereignissen; kann fachliche, personelle oder materielle Ursache haben

**Netztypen**
- Vorgangs-Knoten-Netz (VKN): Vorgänge als Rechtecke, verbunden durch Pfeile; jeder Pfeil-Übergang = Ereignis
- Ereignis-Knoten-Netz (EKN): Ereignisse als Knoten (meist Kreise), Vorgänge als Pfeile zwischen den Knoten
- Vorgangs-Pfeil-Netz (VPN): vergleichbar mit EKN in der Zuordnung

**Scheinvorgänge**
- Kein reales AP, sondern nur zur Formulierung von Beziehungen die von der Normalfolge abweichen
- Haben keinen Aufwand und keine definierte Dauer (können verzögerungslos ablaufen oder unbestimmte Zeit dauern)
- Darstellung: gepunktete Linie im Netzplan
- Ermöglichen alle vier Anordnungsbeziehungstypen auch in EKN und VPN

**Fallbeispiel Scheinvorgänge (Beispiel 7.3)**
- V1 bis V5: V1 startet mit Projekt (E0); V2, V3 folgen V1; V5 folgt V4; V4 muss vor V3 abgeschlossen sein; Projekt endet mit V5 (nach Abschluss von V3)
- Scheinvorgänge: V6 (V4 kann irgendwann nach Projektstart beginnen), V7 (koppelt Beginn von V3 an Ende von V4), V8 (führt Ende von V3 zum Projektende)

**Grundprinzip der Ablaufplanung**
- Arbeiten sollten so früh wie nötig, aber so spät wie möglich eingeplant werden
- „Just in time": teure Ressourcen (z.B. Transportbehälter) erst bestellen wenn tatsächlich gebraucht → vermeidet unnötige Kapitalbindung und Lagerkosten

#### 7.2 Planungsmethoden

**Überblick Terminplanungsverfahren**
- Deterministische Verfahren (CPM, MPM): nehmen Schätzwerte als zutreffend an und berechnen alle Termine
- Stochastische Verfahren (PERT): berücksichtigen zusätzlich die Varianz der Schätzung und machen Aussagen über Wahrscheinlichkeit der Termineinhaltung
- Alle drei Verfahren entstanden Ende der 1950er Jahre

**Ziel:** frühest- und spätestmögliche Anfangs- und Endtermine für jeden Vorgang bestimmen sowie terminliche Spielräume (Puffer) identifizieren

##### 7.2.1 Critical-Path-Method (CPM)

- Entwickelt 1956 von DuPont zusammen mit Remington Rand
- Basiert auf VPN / EKN (Ereignis-Knoten-Netze)
- Ereignisknoten: abgerundete Rechtecke

**Vorwärtsrechnung — früheste Ereignistermine**
- Projektstart erhält Termin 0
- Für jedes Folgeereignis Ej: Fj = Max{Fi + Di} für alle vorangehenden Ereignisse i (Formel 7.1)
- Wenn mehrere Vorgänge zu einem Ereignis führen: frühester Termin = Maximum der frühestmöglichen Fertigstellungstermine aller eingehenden Vorgänge

**Rückwärtsrechnung — späteste Ereignistermine**
- Startet vom frühesten Projektendtermin (aus Vorwärtsrechnung)
- Für jedes Ereignis Ej: Sj = Min{Sk − Dk} für alle nachfolgenden Ereignisse k (Formel 7.2)
- Bei mehreren Folgeereignissen: minimaler Termin als spätester Ereignistermin

**Pufferzeit**
- Pj = Sj − Fj (Formel 7.3)
- Gibt an, um wie viel ein Ereignis verschoben werden kann ohne die Gesamtprojektlaufzeit zu verändern
- Puffer entstehen nur bei parallel ablaufenden Vorgängen unterschiedlicher Dauer

**Kritischer Pfad**
- Alle Ereignisse mit Pj = 0 (kein Spielraum) bilden zusammen mit den dazwischen liegenden Vorgängen den kritischen Pfad
- Durchlaufzeit des kritischen Pfades = Projekt-Durchlaufzeit
- Verkürzung der Projektlaufzeit nur auf dem kritischen Pfad möglich

##### 7.2.2 Metra-Potential-Methode (MPM)

- Entwickelt 1958 vom französischen Unternehmen Metra; erstmals bei Kreuzfahrtschiff-Bauprojekt eingesetzt
- Basiert auf VKN (Vorgangs-Knoten-Netze); Vorgänge als Rechtecke

**Knoteninhalt je Vorgang (Vorgangssymbol)**
- j: Vorgangsnummer
- D: Dauer
- FA: frühester Anfangstermin
- FE: frühester Endtermin
- SA: spätester Anfangstermin
- SE: spätester Endtermin
- GP: Gesamtpuffer
- FP: Freier Puffer

**Vorwärtsrechnung**
- FAj = Max{FEi} für alle vorangehenden Vorgänge i (Formel 7.4)
- FEj = FAj + Dj (Formel 7.5)

**Rückwärtsrechnung**
- SEj = Min{SAk} für alle nachfolgenden Vorgänge k (Formel 7.6)
- SAj = SEj − Dj (Formel 7.7)

Vorgehensweise vergleichbar mit CPM, aber statt Ereigniszeitpunkten werden direkt Anfangs- und Endtermine der Vorgänge berechnet. Neben dem Gesamtpuffer (GP) wird auch der freie Puffer (FP) bestimmt.
