# Projektmanagement für Ingenieure — Teil 0
> Quelle: Projektmanagement für Ingenieure (buecher) · Seiten 1-40.

Dieses Lehrbuch (6. Auflage, Walter Jakoby, Hochschule Trier, 2025) behandelt das systematische Projektmanagement für Ingenieure und technische Berufe. Teil 0 umfasst Verzeichnisse, Vorwort, Abkürzungsschlüssel sowie das vollständige Kapitel 1 „Projekte" (Definitionen, Systemsicht, Probleme, PM-Grundlagen) und gibt einen Überblick über den Aufbau des gesamten Werks.

## Inhalt

### Vorwort und Einordnung

- Projekte werden zur dominierenden Arbeitsform — getrieben durch Vernetzung und Digitalisierung.
- PM ist kein geschlossenes Monument, sondern ein flexibles Portfolio vieler ergänzender Methoden; Auswahl richtet sich nach Projektprofil.
- KI-Algorithmen werden in naher Zukunft PM-Werkzeuge effizienzsprungartig verändern.
- Buch eignet sich für Selbststudium und vorlesungsbegleitend; Umfang ausgelegt auf 5–10 ECTS-CP.
- Ergänzungsmaterialien: Übungsbuch „Intensivtraining Projektmanagement", Formular- und Foliendownload auf walterjakoby.de/PM.htm.

---

### Abkürzungsverzeichnis (Symbole und Kenngrößen)

| Kürzel | Bedeutung |
|--------|-----------|
| A | Aufwand |
| a / b / c | kleinster (optimistisch) / größter (pessimistisch) / wahrscheinlichster (realistisch) Schätzwert |
| C | Konstante |
| Di | Dauer des Vorgangs i |
| E | Erwartungswert einer Verteilungsfunktion |
| F(x) | Verteilungsfunktion einer Zufallsvariablen |
| FAi / FEi | Frühester Anfangs- / Endtermin für Vorgang i |
| Fi | Frühester Termin für Ereignis i |
| FP | Freier Puffer |
| GP | Gesamtpuffer |
| I(t) | Ist-Verlauf |
| L | Länge (z. B. Programm) |
| M | Median einer Verteilungsfunktion; auch: Maßnahmen-Szenario (Risikovermeidung) |
| P | Zeitlicher Puffer |
| PT | Personentag |
| PM | Personenmonat (1 PM = 20 PT) |
| PJ | Personenjahr (1 PJ = 11 PM = 220 PT) |
| P(t) | Plan-Verlauf |
| p(x) | Wahrscheinlichkeitsdichtefunktion |
| R | Risiko |
| S | Standardabweichung; auch: Schadensausmaß |
| SAi / SEi | Spätester Anfangs- / Endtermin für Vorgang i |
| Si | Spätester Termin für Ereignis i |
| T | Zeitdauer |
| To / Tp / Tw / Te / Ts | Zeitdauer optimistisch / pessimistisch / wahrscheinlichst / Erwartungswert / Standardabweichung |
| V | Varianz einer Verteilungsfunktion |
| W | Wahrscheinlichster Wert einer Verteilungsfunktion |
| X | Zufallsvariable |
| x | Wert einer Variablen |

---

### Inhaltsübersicht des Gesamtwerks (Kapitelstruktur)

Das Buch gliedert sich in 14 Kapitel:

1. Projekte (Definitionen, Systemsicht, PM-Grundlagen)
2. Projekte als Problemlösungsprozesse (Modelle, Zielbildung, Ideenfindung, Lösungsauswahl)
3. Projektgründung (Initiierung, Projektauftrag, Lastenheft/Pflichtenheft, Kalkulation)
4. Projektorganisation (Aufbauorganisation, Ablauforganisation, Informationsflüsse, PM-Handbuch)
5. Strukturplanung (Produktstrukturplan, Projektstrukturplan, Arbeitspakete)
6. Projektschätzung (Schätzmethoden, Wahrscheinlichkeitsrechnung, Zwei- und Dreipunktschätzung, Software-Aufwand)
7. Ablauf- und Terminplanung (Anordnungsbeziehungen, Netzpläne, CPM, MPM, PERT, Gantt, Kapazitätsplanung)
8. Risikomanagement (Risikoidentifikation, -bewertung, -behandlung, -überwachung)
9. Kostenmanagement (Kosten, Projektkalkulation, Earned Value Analyse)
10. Qualitätsmanagement (ISO 9000, TQM, Lean, KVP, Reifegradmodelle, QM in Projekten)
11. Projektsteuerung (Überwachung, Fortschrittsplanung, Meilenstein-Trendanalyse, Lenkung, Abschluss)
12. Der Mensch im Projekt (Selbstmanagement, Projektleiter, Projektteams, Führungsstile)
13. Software-Werkzeuge (Office-Werkzeuge, MS-Project, KI im PM)
14. Agiles Projektmanagement (Scrum, Rollen, Sprints, klassisch vs. agil, Hybrid)

Anhänge: Formulare (A1), Landkarte PM-Prozesse und -Dokumente (A2), Glossar (A3), Literatur, Stichwortverzeichnis.

---

### Kapitel 1: Projekte — Definitionen

#### 1.1.1 Projektbeispiele

Projekte sind in allen Bereichen präsent: Entwicklungsprojekte in Industrieabteilungen, Einführungsprojekte für Software, Managementprojekte für Unternehmensübernahmen, Buchprojekte, Filmprojekte, Entwurfsprojekte in der Architektur.

**Bekannte Großprojekte (historische Referenzpunkte):**
- Empire State Building (New York): Errichtung 1930–1931 in nur 410 Arbeitstagen, Kosten 25 Mio. USD — nur die Hälfte des geplanten Budgets; Arbeitsaufwand 7 Mio. Stunden (~4.000 Personenjahre); Gesamthöhe 449 m, bis 1972 höchstes Gebäude der Welt.
- Hoover Dam (1931–1935): Gilt als eines der ersten Bauprojekte mit dokumentierten, systematischen Planungs- und Steuerungsmethoden; 221 m hohe, 379 m lange Mauer; Kosten 32 Mio. USD — ebenfalls unter dem Planwert.
- Gotthard-Basistunnel (Schweiz): 57 km Tunnelstrecke, Kosten 5 Mrd. USD.
- Flughafen Chek Lap Kok (Hongkong): Künstliche Insel aus 340 Mio. m³ Gesteinsmasse, Fläche 938 ha, Gesamtkosten Insel + Einrichtungen 20 Mrd. USD.
- „The World" in Dubai: Inselgruppe mit 5.400 ha Fläche, Kosten 7,6 Mrd. USD.

**Gescheiterte oder überteuerte Projekte:**
- Toll Collect (Deutschland): Mautsystem für LKW; Auftrag Juli 2002, geplante Inbetriebnahme August 2003, tatsächlich vollständig in Betrieb Januar 2006 — aus geplanten 14 Monaten wurden 42 Monate.
- Opernhaus Sydney: Baubeginn 1959, Fertigstellung für 1965 geplant bei 7 Mio. australischen Dollar kalkuliert — tatsächlich Fertigstellung 1973, Kosten 102 Mio. australische Dollar.
- Standish Group Langzeitstudie (seit 1994, über 40.000 Software-Projekte): ca. 25–35 % erfolgreich, ca. 40–50 % verspätet (viele deutlich verspätet), ca. 20 % vollständig abgebrochen.

**Schlussfolgerung:** Systematisches Projektmanagement ist nicht nur für Großprojekte sinnvoll. Kleinere Vorhaben mit wenigen Personenmonaten erfordern ebenso klare methodische Ansätze, da Komplexität, Abstraktionsniveau und Kosten-/Zeitdruck gestiegen sind.

---

#### 1.1.2 Abgrenzung von Nicht-Projekten

**Definition Projekt:**
Ein Projekt ist ein organisierter Prozess zur Erreichung eines schwierigen Ziels in vorgegebener Zeit und mit begrenzten Ressourcen.

**Sechs Projektmerkmale (Kürzel Z-S-P-O-R-T):**

| Kürzel | Merkmal | Typische Problematik |
|--------|---------|----------------------|
| Z | Zielexistenz (Zielklarheit) | Unklare, veränderliche Anforderungen |
| S | Schwierigkeit / Neuartigkeit | Unklare, schwierige Realisierbarkeit |
| P | Prozesscharakter (viele vernetzte Tätigkeiten) | Viele und stark vernetzte Aktivitäten |
| O | Organisation / Teambildung (Beteiligte) | Unklare Verantwortungen und Befugnisse |
| R | Ressourcenbegrenzung (Kapital) | Knappe Ressourcen, insb. Kapital |
| T | Terminierung (Zeitbegrenzung) | Knappe Termine |

**Stufenmodell der Aufgabentypen:**
- Aufgabe: klares Ziel vorhanden.
- Problem: Aufgabe ist schwierig (Hindernis auf dem Weg zum Ziel).
- Prozess: Lösung erfordert viele vernetzte Tätigkeiten.
- Projekt: Prozess mit mehreren Beteiligten, Zeitbegrenzung und Ressourcenlimitierung.

**Notwendige vs. schwache Kriterien:**
- Notwendige Kriterien (müssen erfüllt sein): Einmaligkeit und Zielklarheit, Zeitbegrenzung, Mehrschrittigkeit.
- Schwächere Kriterien (unterschiedlich ausgeprägt): Schwierigkeit, Zahl der Beteiligten, Ressourcenbegrenzung.

**Beispiel Studium (Beispiel 1.3):** Ein Studium erfüllt alle Projektmerkmale — Ziel mit nachprüfbarer Zielerreichung, zeitliche Limitierung, Ressourcenbegrenzung (Finanzierung, Hörsäle, Laborplätze), Beteiligung mehrerer Personen (Professoren, Kommilitonen, Eltern). Fazit: Studium ist eindeutig ein Projekt.

**Beispiel Projektkriterien (Beispiel 1.4):**

| Vorhaben | Z | S | P | O | R | T | Ergebnis |
|----------|---|---|---|---|---|---|---------|
| Unternehmensleitung | + | o | + | + | − | − | Nein (keine Zeitbegrenzung) |
| Entwicklung neue Mikroprozessorschaltung | + | + | + | o | + | + | Ja |
| Re-Design Mikroprozessorschaltung | + | − | + | o | + | + | Nein (fehlende Neuartigkeit/Schwierigkeit) |
| Neuer Energiespeicher | o | + | + | + | − | − | Unklar (Zielklarheit und Terminierung offen) |
| Jährliche Inventur | + | − | o | + | + | + | Nein (Routine-Prozess, kein einmaliges Vorhaben) |

Z: Zielklarheit, S: Schwierigkeit, P: Prozesscharakter, O: viele Beteiligte, R: Ressourcenbegrenzung, T: Terminierung; +: erfüllt, o: teilweise/unklar, −: nicht erfüllt.

---

#### 1.1.3 Klassifizierung von Projekten

**Klassifizierungsdimension 1 — Projektgröße (gemessen in Personenjahren):**

Einheitendefinitionen im Buch:
- 1 PT = Personentag
- 1 PM = 20 PT = 1 Personenmonat
- 1 PJ = 11 PM = 220 PT = 1 Personenjahr

Jährlich produktive Arbeitstage (nach Abzug Wochenenden, Feiertage, Urlaub 25–30 Tage, Krankheitsfehlzeiten): ca. 210–220 Arbeitstage.

**Projektgrößenklassen:**

| Klasse | Personalaufwand [PJ] | Kosten (Richtwert) |
|--------|---------------------|--------------------|
| Sehr klein | < 0,4 PJ | < 100.000 € |
| Klein | 0,4–4 PJ | 100.000–1 Mio. € |
| Mittel | 4–40 PJ | 1–10 Mio. € |
| Groß | 40–400 PJ | 10–100 Mio. € |
| Sehr groß | 400–4.000 PJ | 100 Mio. – 1 Mrd. € |
| Mega-Projekt | > 4.000 PJ | > 1 Mrd. € |

**Formeln auf der Projektgrößen-Diagonalen** (A = Aufwand in PM, N = Personenzahl, D = Laufzeit in Monaten):
- D [Monate] = 3 · A^(1/3) [PM]
- N [Personen] = (1/3) · A^(2/3) [PM]
- D [Monate] = 5 · N^(1/2)

Diese Formeln erlauben eine erste grobe Schätzung von Laufzeit und Personenzahl, wenn der Personalaufwand bekannt ist.

**Kostenrichtwert:** 1 PJ entspricht grob 250.000 € Gesamtkosten (inkl. Material, Maschinen), gemittelt über viele Branchen (entspricht ca. dem Median des Jahresumsatzes pro Mitarbeiter). Reine Personalkosten: 60.000–125.000 €/PJ. Faustformel: ca. 10.000 € pro Personenmonat.

**Projektgrößen-Kennzahlen aus der Praxis (Beispiel 1.5):**

| Projekt | Laufzeit [J] | Aufwand [PJ] | Kosten [Mio. €] | €/PJ [Mio.] | Personen |
|---------|-------------|-------------|-----------------|-------------|---------|
| Gotthard-Basistunnel | 17 | 25.000 | 10.000 | 0,40 | 1.500 |
| Entwicklung neues Automodell | 4 | 4.000 | 2.000 | 0,50 | 1.000 |
| Bau Elbphilharmonie | 10 | 2.000 | 800 | 0,40 | 180 |
| Neues Werk für Baumaschinenhersteller | 1,9 | 565 | 130 | 0,23 | 300 |
| Neue Spiele-Software (Quake Engine 3, ~400.000 Zeilen) | 3,3 | 200 | 41 | 0,20 | 60 |
| Deutscher Kinofilm | 2,5 | 25 | 5 | 0,20 | 10 |
| Aufbau einer Gebäudehebeanlage (bis 80 elektrohydr. Heber) | 1,75 | 3,5 | 0,9 | 0,25 | 2 |
| Entwicklung einer neuen App | 0,4 | 0,4 | 0,05 | 0,125 | 1 |

**Klassifizierungsdimension 2 — Projektgegenstand:**
- Baubranche: Tiefbau (Straßen, Tunnel, Kanäle), Hochbau.
- Maschinenbau / Konstruktion.
- Chemie / Biochemie (Medikamente, Werkstoffe).
- Elektro- und Elektronikentwicklung.
- Softwareentwicklung.

**Klassifizierungsdimension 3 — Projektart:**
- Forschungsprojekte: Suche nach neuen wissenschaftlichen Erkenntnissen; hohe Neuartigkeit, abstrakte Ziele, hohe Planungsunsicherheit.
- Entwicklungsprojekte: Entwicklung neuer Geräte, Maschinen, Programme, Medikamente; hohe Neuartigkeit, aber konkretere Ziele als Forschung; erfahrungsgemäß dennoch hohe Kosten-/Terminunsicherheit.
- Projektierungsprojekte: Entwurf und Aufbau aus vorhandenen Modulen; geringe bis mittlere Neuartigkeit; oft auf Kundenbasis mit klar definiertem Umfang; Hauptproblem: Vereinbarung gegenläufiger Anforderungen.
- Organisationsprojekte: Veränderung oder Neuaufbau betrieblicher Abläufe/Organisationen; Besonderheit: Projektgegenstand ist das Zusammenwirken von Menschen selbst; psychische Vorgänge der Beteiligten als zentrale Herausforderung.
- Investitionsprojekte: Bau großer einmaliger Bauten (Gebäude, Straßen, Staudämme, Inseln, Kanäle, Flughäfen, Produktionsanlagen); älteste Projektart mit höchstem PM-Reifegrad; besonderes Merkmal: hohes Kostenbudget durch Maschinen-, Rohstoff- und Zulieferteilbedarf.

---

### Kapitel 1: Systeme und Prozesse

#### 1.2.1 Systemdefinition

Ein System ist ein von seiner Umgebung klar abgrenzbares zusammenhängendes Gebilde. Charakteristika:

- Umgebung beeinflusst das System über **Eingangsgrößen u** (gezielte Beeinflussungen) und **Störgrößen v** (unerwünschte Einflüsse).
- Das System reagiert mit **gewünschten Ausgangsgrößen y** und **unerwünschten Nebenwirkungen n**.
- Im Inneren können Materie, Energie und Informationen gespeichert werden; der Zustand ist zu jedem Zeitpunkt durch die **Speichergrößen x** eindeutig bestimmt.

Beispiele für Systeme:
- Auto (ohne Fahrer): Eingangsgrößen = Gas, Schalten, Lenken; Störgrößen = Steigung, Seitenwind, Hindernisse; Zustandsgrößen = Position, Geschwindigkeit.
- Haus: Einwirkung durch Sonneneinstrahlung, Wind, Regen; Ausgangsgrößen = Wärmeabgabe, Lärm der Bewohner, Fundamentdruck.
- Internet: weltweites komplexes System aus Übertragungssystemen, Rechnern, Programmen.

**Interne vs. externe Systemsicht:**
- Extern: Schnittstellen zur Umgebung (Ein-/Ausgangsgrößen).
- Intern: Komponenten mit Wechselwirkungen untereinander.

**Systemgrenzenbestimmung:** Komponenten mit starker gegenseitiger Kopplung werden dem System zugeschlagen; Komponenten mit schwacher Kopplung zählen zur Umgebung.

---

#### 1.2.2 Projekte aus Systemsicht

Das Projektergebnis (Produkt) weist Systemcharakter auf: klare Abgrenzung zur Einsatzumgebung, mehrere in Wechselwirkung stehende Teilkomponenten.

Das Projekt selbst ist ebenfalls ein System: Es empfängt einen **Auftrag** als Input und liefert ein **Ergebnis** als Output.

**Teilsysteme eines Projekts:**
- Soziales Teilsystem: Projektbeteiligte mit Wechselwirkungen untereinander.
- Ressourcen-Teilsysteme: CAD-Systeme, Dokumentenmanagementsysteme, Maschinen.
- Arbeitssystem: auszuführende Arbeiten mit logischen/zeitlichen Abhängigkeiten.

**Sechs Kategorien von Projekt-Wechselwirkungen:**

| Kategorie | Bedeutung |
|-----------|-----------|
| A-A | Beziehungen zwischen Arbeiten (Teilarbeiten, Vorraussetzungen) |
| A-B | Beziehungen zwischen Arbeiten und Beteiligten (Ausführer, Informierter, Freigeber) |
| B-B | Beziehungen zwischen Beteiligten (Rollen, persönliche Dynamiken) |
| A-R | Ressourcenbedarf von Arbeiten (Maschinen, Kosten) |
| B-R | Ressourcenbedarf von Personen (Gehalt, Schreibtisch, Rechner) |
| R-R | Beziehungen zwischen Ressourcen (Platzbedarf, Kapitalbedarf) |

Statische Systemstruktur + dynamische Aspekte (Zeitabhängigkeiten, Sequenzierung) bilden zusammen die Grundlage für Termin- und Ablaufplanung.

**Dynamische Planungsfragen:**
- Wann muss das Projekt abgeschlossen sein?
- Wann kann eine Arbeit frühestens beginnen / spätestens enden?
- Wann wird eine Ressource benötigt?
- Wer steht in einem Zeitraum verfügbar?
- Welche Arbeiten müssen abgeschlossen sein, damit eine andere starten kann?

---

#### 1.2.3 Probleme

**Definition Aufgabe:** Ein System durch geeignete Handlungen aus einem Anfangszustand in einen Zielzustand bringen.

**Definition Problem:** Eine Aufgabe wird zum Problem, wenn ein Hindernis den Weg zum Zielzustand erschwert oder verhindert.

**Hindernistypen:**
- Unklar was zu tun ist.
- Unklar wie es getan werden kann.
- Unklar welche der Handlungsmöglichkeiten die beste ist.
- Unklar in welcher Reihenfolge Handlungen auszuführen sind.
- Handlungsspielraum durch Randbedingungen eingeschränkt (knappe Zeit, knappe Ressourcen, fehlendes Fachwissen).
- Zielzustand oder Anfangszustand unklar.
- Kein Gütekriterium für Lösung bekannt.

**Zustandsraummodell des Problemlösens:**
- Problemdimensionen spannen einen Zustandsraum auf.
- Aufgabe: System aus Anfangszustand (links unten) in Zielzustand (rechts oben) bringen.
- Randbedingungen R1–R4 grenzen verbotene Bereiche ein (gelten während des Prozesses); R0 gilt nur nach Zielerreichung.
- Gütekriterium J bewertet und vergleicht verschiedene Lösungspfade.

**Beispiel Problemdimensionen (Beispiel 1.7):**
- Transport: Zeit, Kosten, Energie.
- Hausbau: Wohnfläche, Kosten, Bauzeit.
- Studium: erreichte Qualifikation, erforderlicher Aufwand.
- Jobsuche: Arbeitsfreude, Bezahlung, Branche, Region.
- Produktentwicklung: Funktionen, Benutzerfreundlichkeit, Entwicklungsaufwand, Zeitbedarf.

**Beispiel Aufgaben/Probleme/Projekte (Beispiel 1.6) — Typenklassifizierung:**
- Pakettransport München→Hamburg: reine Aufgabe (klar definiert, routiniert).
- Programm für größte 9-stellige Primzahl: Aufgabe mit algorithmischem Problem.
- Schaltnetzteil 100 W entwickeln: Entwicklungsprojekt.
- 1-wöchige PM-Schulung: Organisationsvorhaben.
- Bahnhofsgebäude zu Hotel umbauen: Investitions-/Bauprojekt.
- Auto mit < 1 l/100 km konstruieren: anspruchsvolles Entwicklungsprojekt (hohe Schwierigkeit).
- Neue Straßenverbindung an Autobahn: Investitions-/Bauprojekt.

---

### Kapitel 1: Projektmanagement (Abschnitt 1.3 — Überblick aus dem Inhaltsverzeichnis)

Folgende Unterabschnitte werden in Kapitel 1.3 behandelt (Inhalt liegt in Teilen 1 ff.; Seitenbereiche aus dem Inhaltsverzeichnis):
- 1.3.1 Der Projektmanagement-Prozess (S. 18)
- 1.3.2 Entwicklung des Fachgebiets (S. 21)
- 1.3.3 Vorgehensmodelle (S. 22)
- 1.3.4 Normen, Standards, Zertifizierung (S. 24)
- 1.3.5 Fallbeispiele: „Maschinenterminal M4", „Solaranlage", „CAD-Software" (S. 26–28)
- 1.3.6 Gliederung des Buchs (S. 28)

Diese Inhalte liegen jenseits Seite 40 und werden in folgenden Teilen digestiert.

---

### Verzeichnis relevanter Fallbeispiele (buchweite Übersicht, auszugsweise)

Wiederkehrende Fallbeispiele im gesamten Buch:
- **Maschinenterminal M4**: Entwicklungsprojekt für ein industrielles Maschinenterminal; taucht in Kapiteln zu Organisation, Strukturplanung, Terminplanung, Risiko auf.
- **Solaranlage**: Projektierungsprojekt; genutzt für Strukturplanung, Aufwandsschätzung, Kostenplanung.
- **CAD-Software**: Entwicklungsprojekt; genutzt für Projektdefinition, Nutzwertanalyse, Risikoportfolio, Qualitätsbewertung, Kostenplanung.
- **Brandmeldezentrale**: Aufbauorganisation (Kap. 4).
- **DeLorean DMC-12**: Ablaufstrukturbeispiel (Kap. 4).
- **Temperaturmessbox**: Netzplan- und PERT-Beispiel (Kap. 7).
- **Gebäudehebeanlage** (bis 80 elektrohydr. Heber): Kennzahlen-Referenzprojekt.

---

### Tabellen- und Abbildungsverzeichnis — wichtige Tabellen für spätere Kapitel

Relevante Tabellen im Buch (Seitenreferenzen aus dem Verzeichnis):

| Tabelle | Inhalt | Seite |
|---------|--------|-------|
| Tab. 1.1 | Projektkriterien für verschiedene Vorhaben | 7 |
| Tab. 1.2 | Kennzahlen für verschiedene Projektkategorien | 9 |
| Tab. 4.4 | Leistungsphasen nach HOAI | 101 |
| Tab. 5.1 | 7er-Regel: Anzahl Elemente je Ebene | 136 |
| Tab. 6.2 | Kalkulationsschema für Entwicklungskosten | 150 |
| Tab. 6.3 | Gegenüberstellung verschiedener Schätzmethoden | 152 |
| Tab. 6.4 | Werte P(x, z) bei der Normalverteilung | 159 |
| Tab. 6.5 | CoCoMo-Schätzmodelle und Parameter | 165 |
| Tab. 8.1 | Checkliste Projekt-Risikofaktoren | 198 |
| Tab. 8.2 | Bestimmung von Risikoklassen | 201 |
| Tab. 8.3 | Bestimmung der Risikoprioritätszahl (RPZ) bei FMEA | 202 |
| Tab. 8.5 | Risk reduction stair | 203 |
| Tab. 9.5 | Kennzahlen der Earned Value Analyse | 224 |
| Tab. 10.1 | Wichtige QMS-Normen | 235 |
| Tab. 11.1 | Ermittlung des Fertigstellungsgrads (FGR, 0–100 %) | 265 |
| Tab. 12.6 | Situative Reifegrad-Theorie | 310 |
| Tab. 12.8 | Entwicklungsphasen von Arbeitsgruppen (nach Tuckman) | 316 |
| Tab. 14.1 | Die 4 Werte des agilen Manifests | 352 |
| Tab. 14.2 | Die 12 Prinzipien des agilen Manifests | 354 |
| Tab. 14.13 | Merkmale klassischer und agiler PM-Modelle | 376 |

---

### Hinweise zu weiteren Kapitelinhalten (ab Seite 40 — in späteren Parts)

Die restlichen Kapitel 1.3 ff. sowie Kapitel 2–14 und Anhänge fallen in die Parts 1–10 des Digests. Besonders für Ingenieure im Bau- und Elektrobereich relevant:
- Leistungsphasen nach HOAI (Tab. 4.4, Beispiel 4.9) — Planung/Vergabe für Bauprojekte.
- Beispiel „Brandmeldezentrale" und „QMS" (Kap. 4) — Technikprojekte mit Zertifizierungsbezug.
- Risiko-FMEA und RPZ-Berechnung (Kap. 8) — anwendbar auf elektrotechnische Projekte.
- CoCoMo-Schätzmodelle (Kap. 6) — ursprünglich für Software, aber auf Projektplanung generell anwendbar.
- Earned Value Analyse (Kap. 9) — Kosten-/Fortschrittscontrolling.
- ISO 9000 ff. und TQM (Kap. 10) — Qualitätsmanagementsysteme.
