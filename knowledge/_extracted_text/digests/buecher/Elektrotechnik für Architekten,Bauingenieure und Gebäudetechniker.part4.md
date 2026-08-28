# Elektrotechnik für Architekten,Bauingenieure und Gebäudetechniker — Teil 4
> Quelle: Elektrotechnik für Architekten,Bauingenieure und Gebäudetechniker (buecher) · Seiten 161-200.

Dieser Teil schließt die Grundlagen der Drehstromtechnik ab (Kapitel 13) und führt dann in die normative Welt der Elektroplanung ein: Kapitel 14 behandelt Begriffe, Definitionen, Institutionen und Rechtsnormen (VDE, DIN, DKE, IEC, CENELEC), Kapitel 15 beginnt mit den konkreten Planungsgrundlagen für Elektroanlagen in Wohngebäuden (Leistungsbedarfsberechnung, Elektromobilität, DIN 18015).

## Inhalt

### Drehstromtechnik — Schaltungen und Kenngrößen (Kapitel 13, Seiten 161–170)

#### Spannungsbeziehungen im Drehstromsystem

- Drei Strangspannungen sind jeweils um 120° gegeneinander phasenverschoben:
  - u₁(t) = û · sin(ωt)
  - u₂(t) = û · sin(ωt − 120°)
  - u₃(t) = û · sin(ωt − 240°)
- Komplexe Darstellung: U₁ = U₁·e^(j0°), U₂ = U₁·e^(−j120°), U₃ = U₁·e^(−j240°)
- In der Sternschaltung gibt es zwei Spannungsarten:
  - Sternpunktspannungen (Strangspannungen): U₁, U₂, U₃ — je 120° versetzt
  - Leiter-Leiter-Spannungen (verkettete Spannungen): U₁₂, U₂₃, U₃₁
- Summe symmetrischer Größen ist stets null: U₁ + U₂ + U₃ = 0; ebenso U₁₂ + U₂₃ + U₃₁ = 0
- Beziehung Leiterspannung zu Strangspannung: UL = UStr · √3 (Formel 13.15)
  - Leiterspannungen sind um den Faktor √3 größer als Strangspannungen

#### Symmetrische Sternschaltung mit Neutralleiter

- Außenleiter und Sternpunkte von Quelle und Verbraucher werden zusammengeschaltet
- Außenleiterströme: I₁ = U₁/Z; I₂ = I₁ · e^(−j120°); I₃ = I₁ · e^(−j240°)
- Neutralleiterstrom bei symmetrischem System: IN = I₁ + I₂ + I₃ = 0 (Formel 13.22)
- In der Sternschaltung gilt: IL = IStr

#### Symmetrische Dreieckschaltung

- Nur Außenleiter von Quelle und Verbraucher werden verbunden (kein Neutralleiter)
- Strangströme bei symmetrischer Beschaltung (Z₁₂ = Z₂₃ = Z₃₁) sind betragsmäßig gleich und 120° versetzt
- Außenleiterströme werden über Knotenregel bestimmt, z.B.: I₁ = I₁₂ − I₃₁ = I₁₂ · √3 · ∠−30°
- Beziehung Außenleiter- zu Strangstrom: IL = √3 · IStr (Formel 13.32)

#### Unsymmetrische Drehstromsysteme

- Zwei Ursachen für Unsymmetrie: (1) Erzeuger-Spannungen unterscheiden sich in Betrag oder Winkel; (2) Lastimpedanzen sind ungleich
- Unsymmetrische Sternschaltung mit Neutralleiter: Ströme I₁ = U₁/ZL₁, I₂ = U₂/ZL₂, I₃ = U₃/ZL₃; Neutralleiterstrom IN = I₁ + I₂ + I₃ ≠ 0
- Unsymmetrische Dreieckschaltung: Strangströme ergeben sich aus den unterschiedlichen Impedanzen in den einzelnen Zweigen

#### Verkettungsfaktor

- Verhältnis Dreieck- zu Sternspannung: UDreieck / UStern = √3 (aus geometrischer Beziehung sin 60° = √3/2)

#### Leistungen im Drehstromsystem

- Drei Leistungsarten (Effektivwerte von U und I):
  - Scheinleistung S [VA]: S = √3 · U · I
  - Wirkleistung P [W]: P = √3 · U · I · cos φ
  - Blindleistung Q [var]: Q = √3 · U · I · sin φ

#### Berechnungsbeispiel: Verbraucherströme (Seite 149)

- Netz: 400 V / 230 V, 50 Hz; drei einphasige Verbraucher
- Elektroherd 2000 W, cos φ = 1: Ib = 2000 W / 230 V = 8,7 A
- Mikrowelle 500 W, cos φ = 1: Ib = 500 W / 230 V = 2,17 A
- Steckdosen 1000 W, cos φ = 1: Ib = 1000 W / 230 V = 4,34 A

---

### Normen und Vorschriften (Kapitel 14, Seiten 171–180)

#### Begriffe und Definitionen (DIN VDE 0100, DIN VDE 0105)

- **Elektrische Anlage**: Zusammenschluss von Betriebsmitteln zum Erzeugen, Fortleiten, Umwandeln, Verteilen und Verbrauchen elektrischer Energie für mechanische Arbeit, Wärme-/Lichterzeugung oder elektrochemische Prozesse
- **Elektrische Betriebsmittel**: Gegenstände, die in elektrischen Anlagen zur Nutzung elektrischer Energie dienen; Unterteilung in ortsfeste, festangebrachte und ortsveränderliche Geräte sowie Handgeräte
- **Elektrische Betriebsräume**: Abgegrenzte Räume, Bereiche und Schränke zur Unterbringung von Betriebsmitteln
- **Instandhaltung**: Oberbegriff für Inspektion, Wartung, Instandsetzung, Erneuerung und Überwachung von Elektroanlagen
- **Elektrofachkraft** (nach DIN VDE 0100 Teil 10 und DIN VDE 0105): Person mit fachlicher Qualifikation durch Ausbildung, mehrjährige Mitarbeit, Normenkenntnisse und Gefahrenbeurteilungsfähigkeit — für Errichten und Betrieb von Elektroanlagen zuständig
- **Elektrotechnisch unterwiesene Person**: Weniger qualifiziert als Elektrofachkraft; muss Kenntnisse und fachgerechtes Verhalten nachweisen
- **Elektrotechnischer Laie**: Weder Fachkraft noch unterwiesene Person; darf ausschließlich unter ständiger Aufsicht einer Elektrofachkraft tätig sein; nicht zuständig für Errichten, Ändern oder Betreiben von Elektroanlagen
- **Elektrotechnische Regeln**: "Allgemein anerkannte Regeln der Technik" in DIN-VDE-Normen; Bestandteil der Unfallverhütungsvorschriften (UVV) → rechtsverbindlich, zwingend einzuhalten

#### Rechtliche Grundlagen

- **Energiewirtschaftsgesetz (2. DVO, § 1 Abs. 1)**: Bei Errichtung und Unterhalt von Stromerzeugungsanlagen, Leitungsanlagen und Abgabeanlagen sind die allgemein anerkannten Regeln der Technik einzuhalten
- **BGV A2 (Unfallverhütungsvorschrift), Abs. 3**: Unternehmer muss sicherstellen, dass elektrische Anlagen und Betriebsmittel nur von oder unter Leitung einer Elektrofachkraft errichtet, geändert und instandgehalten werden
- **BGV A2, Abs. 5**: Unternehmer muss ordnungsgemäßen Zustand der Anlagen prüfen lassen
- **BGB § 276**: Fahrlässig handelt, wer die im Verkehr erforderliche Sorgfalt missachtet; Planer/Errichter können Sorgfalt nur nachweisen, wenn sie allgemein anerkannte Regeln berücksichtigen
- **StGB § 323, Abs. 1**: Wer bei Planung, Leitung oder Ausführung von Bau oder Abbruch gegen anerkannte Regeln der Technik verstößt und dadurch Leib oder Leben gefährdet, wird mit Freiheitsstrafe bis zu 5 Jahren oder Geldstrafe bestraft

#### DIN — Deutsches Institut für Normung e.V.

- Sitz in Berlin; technisch-wissenschaftlicher Verein
- Normungsvertrag mit Bundesregierung vom 5. Juni 1975 → DIN als zuständige Normungsorganisation für Deutschland
- Vereinbarung mit DDR vom 4. Juli 1990 → Normenunion
- DIN vertritt deutsche Interessen in nichtstaatlichen internationalen Normungsorganisationen
- Verfolgt gemeinnützige Zwecke: Rationalisierung, Qualitätssicherung, Sicherheit, Umweltschutz, Verständigung
- Normung = Selbstverwaltungsaufgabe aller interessierten Kreise

#### DKE — Deutsche Kommission Elektrotechnik Elektronik Informationstechnik

- Gegründet 1970; gemeinsame Organisation von DIN und VDE
- Erarbeitet Normen und Sicherheitsbestimmungen für Elektrotechnik, Elektronik, Informationstechnik
- Vertritt Deutschland in CENELEC (Europa) und IEC (international)
- Rund 3.500 Experten aus Wirtschaft, Wissenschaft und Verwaltung
- VDE-Bestimmungen basieren zu ca. 80 % auf europäischen Normen, diese wiederum zu ca. 80 % auf IEC-Ergebnissen
- Ergebnisse der DKE-Normungsarbeit werden als DIN-Normen veröffentlicht; normen mit sicherheitstechnischen Festlegungen erhalten zusätzlich VDE-Klassifikation
- Aufgaben der DKE:
  1. Anerkannte Regeln der Technik erarbeiten und veröffentlichen (DIN-Normen)
  2. Normen mit Sicherheitsfestlegungen → VDE-Klassifikation
  3. Mitarbeit bei regionalen und internationalen Spezifikationen
- Ziele der DKE:
  1. Sichere und rationelle Erzeugung, Verteilung und Nutzung von Elektrizität zum Wohl der Allgemeinheit
  2. Deutsche Interessen bei IEC/CENELEC vertreten → Handelshemmnisse abbauen, Märkte öffnen
  3. Marktdurchdringung neuer Technologien durch Normen und Spezifikationen beschleunigen
- Zusammenarbeit als NSO (Nationale Normungsorganisation) mit ETSI (European Telecommunications Standards Institute)

#### Arbeitsgruppen (Working Groups) in der DKE/DIN-Normungsarbeit

- Zusammensetzung: Hersteller, Handel, Verbraucher, Handwerk, Dienstleister, Wissenschaft, technische Überwachung, Staat und weitere Interessierte
- Normung als Selbstverwaltungsaufgabe; Fachleute werden von Fachkreisen (Verbände, Behörden, Hochschulen) autorisiert
- Fachkreise müssen angemessen vertreten sein, besonders bei Sicherheitsnormen
- Arbeitsergebnisse müssen der Öffentlichkeit vorgestellt werden; Stellungnahmen der Öffentlichkeit sind zu berücksichtigen
- Bei Meinungsverschiedenheiten: Schlichtungsverfahren, danach ggf. Schiedsverfahren

#### VDE — Verband der Elektrotechnik Elektronik Informationstechnik e.V.

- Gegründet 1893; technisch-wissenschaftlicher Verein
- "VDE" ist ein markenrechtlich geschütztes Verbandszeichen (Kollektivmarke) → kennzeichnet Sicherheitsnormen der Elektrotechnik (VDE-Bestimmungen, VDE-Leitlinien, VDE-Vornormen) und das VDE-Zeichen für Erzeugnisse
- Aktuell 32 Regional- und Bezirksvereine in Deutschland
- Wichtige Gesetze, Verordnungen und Vorschriften für Errichtung und Betrieb elektrischer Anlagen:
  1. Energiewirtschaftsgesetz (EnWG)
  2. Gerätesicherheitsgesetz (GSG)
  3. Unfallverhütungsvorschriften der gewerblichen Berufsgenossenschaften
  4. AVBEltV — Allgemeine Bedingungen für die Elektrizitätsversorgung von Tarifkunden
  5. Technische Anschlussbedingungen (TAB)
  6. Hauptberatungsstelle für Elektrizitätsanwendung e.V. (HEA)
  7. DIN-VDE-Normen, DIN-Normen
  8. Merkblätter der Überwachungsvereine
  9. VdS-Vorschriften (Versicherungswirtschaft)
  10. Baurecht, Bauplanungsrecht
  11. Bürgerliches Recht und Strafrecht
  12. Landesbauordnungen der Bundesländer

#### Struktur des VDE-Vorschriftenwerks (DIN-VDE-Normen-Gruppen)

Elektrische Anlagen müssen so ausgeführt und betrieben werden, dass Personen-, Tier- und Sachschutz gewährleistet ist. Das VDE-Vorschriftenwerk ist nach VDE 0022 gegliedert:

| Gruppe | Inhalt |
|--------|--------|
| 0 | Allgemeine Grundsätze |
| 1 | Energieanlagen (z.B. DIN VDE 0100) |
| 2 | Energieleiter (z.B. DIN VDE 0250) |
| 3 | Isolierstoffe |
| 4 | Messen, Steuern, Prüfen |
| 5 | Maschinen, Umformer |
| 6 | Installationsmaterial, Schaltgeräte |
| 7 | Gebrauchsgeräte, Arbeitsgeräte |
| 8 | Informationstechnik |

#### Institutionen, Verordnungen, Gesetze — weitere Regelwerke

- **Bautechnischer Brandschutz**: Landesbauordnung Baden-Württemberg (LBO) § 15, Musterbauordnung (MBO) § 17; bauliche Anlagen sind so anzuordnen, dass Brandentstehung und -ausbreitung verhindert wird und wirksame Löscharbeiten sowie Personenrettung möglich sind
- **Leitungsanlagen-Richtlinie (LAR)** gilt für:
  - Leitungsanlagen in Rettungswegen
  - Funktionserhalt von Sicherheitsvorrichtungen
  - Brandschottungen bei Durchbrüchen durch Brandwände
- **TAB** — Richtlinien der Versorgungsbetreiber (Netzbetreiber)
- **VdS-Richtlinien** (Gesamtverband der Deutschen Versicherungswirtschaft GDV): kein Gesetz; Sachschutz im Vordergrund; unverbindliche Empfehlungen, nur im Rahmen eines Versicherungsvertrages vereinbarbar

#### Rechtliche Bedeutung technischer Normen

- Technische Normen sind keine Rechtsnormen; sie enthalten Regeln für allgemeine Anwendung
- Rechtliche Bedeutung erlangen sie durch:
  - Vertragsbeziehungen (z.B. VOB) als Erkenntnisquelle für Behörden und Gerichte
  - Integration in rechtliche Regelungen
- Verbindlich werden Normen durch Einbindung in:
  1. Energiewirtschaftsgesetz
  2. Unfallverhütungsvorschriften
  3. Gerätesicherheitsgesetz

---

### Planung von Elektroanlagen (Kapitel 15, Seiten 181–200)

#### Art der Einspeisung (15.1)

- Drei mögliche Netzstrukturen in der Praxis:
  1. Allgemeine Stromversorgung — für normale Verbraucher
  2. Sicherheitsstromversorgung — für Anlagen, die im Gefahrenfall Personen schützen
  3. USV (unterbrechungsfreie Stromversorgung) — für sehr empfindliche Anlagen, unterbrechungsloser Dauerbetrieb
- Netzbelastung für Wohneinheiten kann an drei Stellen ermittelt werden:
  1. Vorplanung: maximale Leistung der Wohnung/Gewerbe in kW/m²
  2. Belastbarkeit der Wohnung nach DIN 18015
  3. Alle Wohnungen zusammen → Bemessungsleistung des Transformators bzw. Größe des Hausanschlusskastens (HAK)
- Wohngebäude bis ca. 100 Wohneinheiten können in der Regel über das Niederspannungsnetz des Netzbetreibers versorgt werden

#### Leistungsbedarfsberechnung (15.2)

- Bei der Planung sind frühzeitig zu klären: Gesamtleistung, Transformatorgröße/-anzahl, Kabeldimensionierung, Betriebs- und Kurzschlussströme, Betriebsstörungen, Lage/Größe von Hausanschlusskasten, Elektroraum, Steigschächten
- Zu berücksichtigen: thermische und dynamische Kurzschlussströme, Einschalt-/Ausschaltvermögen der Schutzgeräte, Beiträge von NS-Motoren zu Anfangs-Kurzschlusswechselstrom, Stoßkurzschlussstrom, Ausschaltstrom, Spannungsfall, Netzrückwirkungen
- Elektrische Betriebsmittel dürfen nicht durch elektromagnetische Einflüsse gestört werden und keine Störquelle für andere sein → EMV-Maßnahmen frühzeitig einplanen
- Charakteristische Angaben für NS-Anlagen-Planung:
  - Versorgungsart, übertragbare Leistung, Gleichzeitigkeitsfaktor, Systemformen, äußere Einflüsse auf Betriebsmittel, maximale Übertragungslänge, Anzahl Anschlussgeräte, Querschnitte für Abgänge, Absicherung der Stromkreise, EMV, Wartbarkeit

**Formeln zur Leistungsbedarfsberechnung:**

- Maximaler Leistungsbedarf (Grundformel): Pmax = Σ(Pi · gi)
  - gi = Gleichzeitigkeitsfaktor (Bedarfsfaktor) — gibt an, wie viele Verbraucher gleichzeitig Leistung abnehmen
- Mit motorischen Antrieben (Auslastungsfaktor ai und Wirkungsgrad ηi):
  - Pmax = Σ (PrM · gi · ai / ηi)
- Zulässige Bemessungsleistung zur Beherrschung des (n-1)-Ausfallprinzips:
  - Szul(n-1) ≤ (n-1)/n · k · Σ(SrTi)
- Scheinleistung der Netzeinspeisung: Smax = Pmax / cos φ

**Symbole und Bedeutungen:**
- Pmax = Leistungsbedarf
- Pi = installierte Leistung
- gi = Gleichzeitigkeitsfaktor
- ai = Auslastungsfaktor der Motoren
- ηi = Wirkungsgrad des Motors
- PrM = Bemessungsleistung des Motors
- SrTi = Transformatorbemessungsleistung
- n = Anzahl der installierten Transformatoren
- Szul(n-1) = zulässige Leistung zur Beherrschung des (n-1)-Prinzips
- k = Belastbarkeitsfaktor von Transformatoren (1,4 bei GEAFOL-Gießharztransformatoren)

**Anforderung nach DIN 18015:**
- Mindestabsicherung einer Wohnungsinstallation: 63 A

- Zu beachten in der Planung: Oberschwingungen, Blindleistungskompensation, Überspannungen, elektromagnetische Felder, Spannungsqualität, Netzschutz
- Betriebsmittel (Kabel, Leitungen, Sicherungen, Leistungsschalter, Transformatoren) sind so auszuwählen, dass ein wirtschaftlich und technisch optimales Ergebnis entsteht

**Varianten der Hauptleitungsbemessung nach DIN 18015 (Bild 15.3/15.4):**
- Mit elektrischer Warmwasserbereitung und Elektroheizung
- Mit Speicher für elektrische Warmwasserbereitung für Bade-/Waschzwecke oder mit Durchlauferhitzer
- Ohne elektrische Warmwasserbereitung (nur Licht und Kleingeräte)

**Koordination bei Projektierungsaufgaben:**
- Bauherr, Architekt, Planer für Starkstrom-, Kommunikations-, Mess- und Regeltechnik-, Aufzugs-Anlagen sowie technische/technologische Anlagen müssen koordiniert werden
- Einzuhaltende Normen: IEC, EN, DIN VDE oder besondere Ländervorschriften

**Wichtige Normen für Projektierung (vollständige Liste):**
- DIN VDE 0100 — Errichten von Starkstromanlagen bis 1000 V
- DIN EN 60909-0 — Berechnung der Kurzschlussströme in DS-Netzen
- DIN VDE 0100-710 — Medizinisch genutzte Räume
- DIN VDE 0100-718 — Starkstromanlagen und Sicherheitsstromversorgung in baulichen Anlagen für Menschenansammlungen
- DIN VDE 0113 (DIN EN 60204-1) — Ausrüstung von Industriemaschinen
- DIN VDE 0165 — Errichten elektrischer Anlagen in explosionsgefährdeten Bereichen
- IEC 62305, DIN EN 62305 (VDE 0185) — Blitzschutzanlagen
- DIN VDE 0298 — Strombelastbarkeit von Leitungen und Kabeln
- DIN VDE 0276-1000 — Umrechnungsfaktoren für die Strombelastbarkeit
- BGV A2 — Berufsgenossenschaftliche Vorschriften für Sicherheit und Gesundheit
- DIN 18015 Teile 1, 2, 3 — Planung elektrischer Anlagen in Wohngebäuden
- GVD-Vorschriften (Gesamtverband der Deutschen Versicherungswirtschaft)
- TAB — Technische Anschlussbedingungen
- DIN EN 12464-1, 5035-7 — Beleuchtungstechnik
- Landesbauordnungen der Bundesländer
- DIN EN 60617 — Schaltzeichen
- DIN 18012 — Hausanschluss
- DIN 18014 — Fundamenterder
- Energiewirtschaftsgesetz

**Zwei Planungsfälle in der Praxis:**

Fall I — Einfache Betrachtung:
1. Verbraucher und Anschlussorte bekannt
2. Gleichzeitigkeitsfaktor gegeben oder aus Tabellen
3. Leistung und Kurzschlussspannung des Transformators gegeben
4. Kurzschlussstrom bekannt (oder vom Netzbetreiber angegeben)
5. Berechnung: Querschnitt der Hauptzuleitung, Kurzschlussströme, Spannungsfälle

Fall II — Ausführliche Betrachtung (15 Schritte):
1. Vorimpedanz des vorgelagerten Netzes und Länge bis Hauptverteilungs-Einspeisung gegeben
2. Verbraucherdaten bekannt → in Grundrissplan einzeichnen
3. Gleichzeitigkeitsfaktor gegeben
4. Schutzmaßnahme (TN- oder TT-System) festgelegt
5. Installierte Gesamt-Wirk- und -Blindleistungen berechnen
6. Betriebsstrom aus Gesamtwirkleistung berechnen
7. Querschnitt der Zuleitung unter Beachtung Verlegeart und Spannungsfall bestimmen
8. Hauptsicherung oder Leistungsschalter für gewähltes Kabel festlegen
9. Einzelimpedanzen der Leitungen/Kabel für Kurzschlussstromberechnung ermitteln
10. Kurzschlussströme bei dreipoligem und einpoligem Kurzschluss berechnen
11. Querschnitte nach DIN VDE 0100 Teile 410/430/520/540, DIN VDE 0298 Teil 2 und 4, DIN VDE 0276 Teil 1000 bestimmen
12. Überstrom-Schutzeinrichtungen (ÜSE) für diese Querschnitte auswählen
13. Abschaltzeiten aus Kennlinien oder aus DIN VDE 0100 Gruppe 600 ablesen
14. Selektivität der Überstromschutzeinrichtungen prüfen
15. Alle ermittelten Daten in Übersichts-, Schalt- und Grundrisspläne übertragen

#### Grundlagen der Elektromobilität (15.3)

- Norm: DIN VDE 0100-722 (VDE 0100-722) — Anschluss von Ladevorrichtungen an das Niederspannungsnetz

**Leitungsanforderungen für E-Fahrzeug-Ladepunkte:**
- Zuleitung mit drei Außenleitern (3L, N, PE), zulässige Strombelastbarkeit: 32 A
- Verlauf: von der Hauptverteilung bzw. dem Zählerschrank zum Ladeplatz
- Alternativ: mindestens ein entsprechendes Installationsrohr vorsehen
- Zusätzlich: Installationsrohr für ein Netzwerkkabel von Hauptverteilung/Zählerschrank zum Ladeplatz
- Im Verteiler: Platz für weitere Reiheneinbaugeräte sowie einen zusätzlichen Energiezähler vorsehen (Smart Grid, spezielle Abrechnungsmöglichkeiten)

**Mögliche Ladeleistungen je nach Betriebsart:**
- Maximal 1-phasig, 16 A: 3,7 kW
- 3-phasig, 16 A: 11 kW
- 3-phasig, 32 A: 22 kW
- 2-phasig, 80 A: (weitere Variante)
- Typische DC-Ladeleistungen (Schnellladen): aktuell ca. 50 kW
- Gleichzeitigkeitsfaktor der Verteilerstromkreise: 1 (bei Laststeuerung kann er sich reduzieren)

**Überspannungsschutz:**
- Schutz gegen atmosphärische Überspannungen nach DIN VDE 0100-443
- Auswahl der Überspannungsschutzeinrichtungen nach DIN VDE 0100-534

**Elektrische Installationsvoraussetzungen für Ladepunkte (DIN VDE 0100-722 / IEC 60364-7-722):**
- Jeder Ladepunkt benötigt eine eigene Fehlerstromschutzeinrichtung mit Bemessungsfehlerstrom I∆n = 30 mA
- Für Ladepunkte mit Steckvorrichtung nach IEC 62196: zusätzlich Schutz bei glatten Gleichfehlerströmen iF,DC = 6 mA (z.B. RCD Typ B)
- Gewählter RCD: mindestens Typ A; muss alle aktiven Leiter einschließlich Neutralleiter abschalten
- Bei Steckvorrichtung nach IEC 62196: RCD Typ B oder Typ A mit Sondererkennung von Gleichfehlerströmen > 6 mA zwingend

**Lademöglichkeiten für Elektrofahrzeuge:**
1. **Wechselstromladung (AC Laden)**: Fahrzeug wird über Ladesystem und Ladeleitung mit ein- oder dreiphasigem Wechselstromnetz verbunden; fahrzeugeigenes Ladegerät übernimmt Gleichrichtung und steuert Batterie-Ladung
2. **Gleichstromladung (DC Laden)**: Fahrzeug wird mit Ladestation über Ladeleitung verbunden; Ladegerät ist in der Ladestation integriert; Ladesteuerung erfolgt über Kommunikationsschnittstelle zwischen Fahrzeug und Ladestation
3. **Induktive Ladung**: Funktioniert nach dem Transformatorprinzip; für Elektrofahrzeuge zum Zeitpunkt der Buchveröffentlichung noch in Entwicklung und Standardisierung

#### Elektrische Anlagen in Wohngebäuden — DIN 18015 (15.4)

**Geltungsbereich DIN 18015-1-2-3-4:**
- Mehrfamilienhäuser, Reihenhäuser, Einfamilienhäuser sowie zugehörige Außenanlagen
- Ausgenommen: Ausstattung technischer Betriebsräume und betriebstechnischer Anlagen
- Gilt auch für Wohngebäude mit teilgewerblicher Nutzung und für Gebäude mit Gebäudesystemtechnik

**Begriffe (15.4.1):**
- **Kundenanlage**: Elektrische Anlage hinter dem Übergabepunkt des vorgelagerten Verteilungsnetzes
- **Verteilungsnetz**: Gesamtheit aller Anlagen, Leitungen und Kabel des vorgelagerten Netzes bis zum Übergabepunkt zur Kundenanlage (Verbraucheranlage)
- **Netzbetreiber**: Betreiber eines Elektrizitätsversorgungsnetzes, Telekommunikationsnetzes, Breitbandkommunikationsnetzes, Versorgungsnetzes, Verteilungsnetzes oder Fernnetzes für Gas, Übertragungs- oder Verteilungsnetzes für Fernwärme oder Fernkälte

**Normbereiche DIN 18015 (Teile 1–4):**
- Teil 1: Planungsgrundlagen
- Teil 2: Art und Umfang der Mindestausstattung
- Teil 3: Leitungsführung und Anordnung der Betriebsmittel
- Teil 4: Gebäudesystemtechnik

**Verfahrensanforderungen:**
- Anschlussvoraussetzungen frühzeitig mit Netzbetreiber klären
- Grafische Symbole für Installationspläne nach DIN EN 60617 und DIN EN 61082-4
- Planungsunterlagen nach Ausführung an aktuellen Stand anpassen

**Bestandteile elektrischer Anlagen in Wohngebäuden:**
1. Starkstromanlagen mit Nennspannungen bis 1000 V
2. Telekommunikationsanlagen, Hauskommunikationsanlagen, sonstige Melde- und Informationsverarbeitungsanlagen
3. Verteilanlagen für Radio und Fernsehen sowie interaktive Dienste (mit oder ohne Anschluss an öffentliches Netz)
4. Blitzschutzanlagen
5. Gebäudesystemtechnik (KNX/EIB — weltweiter Standard für Haus- und Gebäudesystemtechnik)

#### Anschlusswerte von Elektrogeräten (Tabelle 15.1)

| Gerät | Anschlusswert [W] |
|-------|-------------------|
| **Küche** | |
| Kühlschrank | 120 |
| Gefriertruhe | 140 |
| Elektroherd | 6000 |
| Kochplatte | 1500 |
| Einbaubackofen | 2500 |
| Mikrowelle | 1200 |
| Grillgerät | 2000 |
| Dunstabzugshaube | 220 |
| Warmwasserboiler | 2000 |
| Geschirrspülmaschine | 3400 |
| Wasserkocher | 2000 |
| Kaffeemaschine | 750 |
| Kaffeemühle | 110 |
| Küchenmaschine | 400 |
| Klimagerät | 3000 |
| Toaster | 1000 |
| Fritteuse | 2000 |
| Durchlauferhitzer | 21000 |
| **Hauswirtschaft** | |
| Waschmaschine | 3300 |
| Wäschetrockner | 2500 |
| Wäscheschleuder | 200 |
| Bügelmaschine | 2000 |
| Bügeleisen | 1000 |
| Trockner | 2000 |
| Nähmaschine | 400 |
| Rasenmäher | 1000 |
| Staubsauger | 2000 |
| **Bad** | |
| Haartrockner | 1000 |
| Durchlauferhitzer | 21000 |
| Sonnenbänke | 1500 |
| Warmwasserspeicher | 2000 |
| **Wohnen** | |
| Fernsehgerät | 180 |
| Radiogerät | 50 |
| Plattenspieler | 40 |
| Tonbandgerät | 80 |
| Tauchsieder | 2000 |
| Stereoanlage | 80 |
| Innenleuchten | 60–100 |
| **Büro** | |
| Schreibmaschine | 500 |
| Kopiergerät | 1400 |
| Computeranlage | 500 |
| **Heizgeräte** | |
| Heizstrahler | 2000 |
| Speicherheizgeräte | 4000 |
| Wärmepumpen | 2500 |
| Klimagerät, Klimatruhe | 2000 |

#### Gleichzeitigkeitsfaktoren für die Haupteinspeisung (Tabelle 15.2)

| Gebäudeart | Faktor |
|------------|--------|
| Wohngebäude | 0,4 |
| Wohnblocks mit elektr. Heizung | 0,8–1 |
| Wohnblocks ohne elektr. Heizung | 0,6 |
| Bürohochhaus — Lüftung, Heizung | 1 |
| Bürohochhaus — Datenverarbeitung | 1 |
| Bürohochhaus — Beleuchtung | 1 |
| Bürohochhaus — Sprinkleranlage | 1 |
| Bürohochhaus — Sanitäranlage | 0,8 |
| Bürohochhaus — Aufzüge | 0,7 |
| Bürohochhaus — Kälteanlage | 1 |
| Schulen | 0,6–0,7 |
| Versammlungsräume, Theater, Restaurants | 0,6–0,8 |
| Ladengeschäfte | 0,6–0,7 |
| Verkehrsanlagen | 1 |
| Verwaltungsgebäude, Banken | 0,7–0,9 |
| Kindergärten | 0,6–0,9 |
| Schreinereien | 0,2–0,6 |
| Metzgereien | 0,5–0,8 |
| Bäckereien | 0,4–0,8 |
| Baustellen | 0,2–0,4 |
| Kräne | 0,7 je Kran |

#### Gleichzeitigkeitsfaktoren für wichtige Verbrauchergruppen (Tabelle 15.3)

| Verbrauchergruppen | Bürogebäude | Krankenhäuser | Kaufhäuser |
|--------------------|-------------|---------------|------------|
| Beleuchtung | 0,85–0,95 | 0,7–0,9 | 0,85–0,95 |
| Steckdosen | 0,1–0,15 | 0,1–0,2 | 0,2 |
| Küchen | 0,5–0,85 | 0,6–0,8 | 0,6–0,8 |
| Klimaanlagen | 1 | 1 | 1 |
| Aufzüge, Rolltreppen | 0,7–1 | 0,5–1 | 0,7–1 |

#### Richtwerte Gleichzeitigkeitsfaktoren nach Anzahl Wohnungen (Tabelle 15.4)

| Anzahl Wohnungen | Gleichzeitigkeitsfaktor [%] |
|------------------|-----------------------------|
| 3–5 | 45 |
| 6–10 | 43 |
| 11–15 | 41 |
| 16–20 | 39 |
| 21–25 | 36 |
| 26–30 | 34 |
| 31–35 | 31 |
| 36–40 | 29 |
| 41–45 | 28 |
| 46–50 | 26 |
| 51–55 | 25 |
| 56–61 | 24 |
| > 62 | 23 |

#### Belastbarkeit der Hauptleitung gemäß DIN 18015 Teil 1 (Tabelle 15.5)

**Ohne elektrische Warmwasserbereitung:**

| Wohneinheiten | Sicherungsgröße [A] |
|---------------|---------------------|
| 1–5 | 63 |
| 6–10 | 80 |
| 11–18 | 100 |
| 19–36 | 125 |
| 37–100 | 160 |

**Mit elektrischer Warmwasserbereitung:**

| Wohneinheiten | Sicherungsgröße [A] |
|---------------|---------------------|
| 1 | 63 |
| 2 | 80 |
| 3 | 100 |
| 4–6 | 125 |
| 7–11 | 160 |
| 12–22 | 200 |
| 23–48 | 250 |

#### Leistungsbedarf von Gebäuden nach Nutzung (Tabelle 15.6)

| Gebäude | Durchschn. Leistungsbedarf [W/m²] | glz | Kosten [Euro/m³] |
|---------|-----------------------------------|-----|-----------------|
| Bank | 40–70 | 0,6 | 25–50 |
| Büro | 30–50 | 0,6 | 17–40 |
| Einkaufszentrum | 30–60 | 0,6 | 12–35 |
| Einfamilienhaus | 10–30 | 0,4 | — |
| Mehrfamilienhaus | 10–30 | 0,4 | 18–35 |
| Hotel | 30–60 | 0,6 | 10–35 |
| Kaufhaus | 30–60 | 0,6 | 20–45 |
| Krankenhaus | 80–120 | 0,6 | 10–40 |
| Kühlhalle | 500–1500 | 0,6 | 10–20 |
| Parkhaus | 3–10 | 0,6 | 7–15 |
| Rechenzentrum | 500–1500 | 0,6 | 15–30 |
| Schule | 10–30 | 0,6 | 8–25 |
| Turnhalle | 15–30 | 0,6 | 8–25 |
| Wohnheim/Altenpflege | 15–30 | 0,6 | 10–25 |

#### Leistungsbedarf verschiedener Funktionsbereiche (Tabelle 15.7)

| Funktionsbereich | Durchschn. Leistungsbedarf [W/m²] | glz |
|------------------|------------------------------------|-----|
| Flur/Vorraum | 5–15 | 0,3 |
| Treppenhaus | 5–15 | 0,3 |
| Technik allgemein | 5–15 | 0,3 |
| Empfangshalle | 10–30 | 1 |
| Aufenthaltsraum/Teeküche | 20–50 | 0,3 |
| WC-Bereiche | 5–15 | 1 |
| Reisezentrum | 60–80 | 0,8 |
| Büroflächen | 20–40 | 0,8 |
| Presse/Buchhandel | 80–120 | 0,8 |
| Blumen | 80–120 | 0,8 |
| Bäcker/Fleisch/Wurst | 250–350 | 0,8 |
| Obst/Gemüse | 80–120 | 0,8 |
| Bistro/Eiscafé | 150–250 | 0,8 |
| Imbiss | 180–220 | 0,8 |
| Gastronomie/Restaurant | 180–400 | 0,8 |
| Frisör | 220–280 | 0,8 |
| Reinigung/Wäscherei | 700–950 | 0,7 |
| Lagerfläche | 5–15 | 0,3 |
| Küchen | 200–400 | 0,7 |
| Photovoltaik Module | 200–300 | — |

#### DIN 18015 Teil 2 — Mindestausstattung (15.4.3)

- Gilt für Art und Umfang der Mindestausstattung in Wohngebäuden (Mehrfamilienhäuser, Reihenhäuser, Einfamilienhäuser), ausgenommen technische Betriebsräume und betriebstechnische Anlagen; gilt auch für Anlagen mit Gebäudesystemtechnik
- Im Beispiel (Bild 15.8): jeder Stromkreis mit kombinierter LS/RCD-Absicherung
- Verteilerplan sowie Übersichtsschaltplan werden für die Anlage erstellt
- Weitere Inhalte: Installationsplan Elternzimmer (Bild 15.9), Installationsplan Bad (Bild 15.10)
- Steckdosenanzahl, Auslässe und Anschlüsse gemäß DIN 18015-2 (Bild 15.6)
- Ausstattungswerte für Gebäudesystemtechnik nach DIN 18015-2 (Bild 15.7)
- Bestückung von Verteilern und Stromkreiseinteilung nach DIN 18015-2 (Bild 15.8):
  - Hinweis 1: Stromkreise über 50 m²
  - Hinweis 2: sofern erforderlich
  - Hinweis 3: im Zählerschrank
