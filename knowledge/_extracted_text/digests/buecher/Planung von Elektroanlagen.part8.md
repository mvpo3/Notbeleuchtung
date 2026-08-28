# Planung von Elektroanlagen — Teil 8
> Quelle: Planung von Elektroanlagen (buecher) · Seiten 321-360.

Dieser Teil behandelt Niederspannungsanlagen: Vorschriften, Normen und deren rechtliche Einordnung (VDE, HOAI, VOB), Planungsrichtlinien und Dokumentationsanforderungen, Berechnungsgrundlagen für Anschlussleistungen und Leitungsdimensionierung, sowie umfangreiche Berechnungsbeispiele (Hochhaus, Küche, Industrieanlage, Fabrik). Abschließend folgt eine Einleitung in den Schutz gegen elektrischen Schlag mit Netzsystemkennzeichnung (TN, TT, IT).

## Inhalt

### NS-Verteilungsanlagen — Planungsparameter (Kapitel 15)

Für die Planung einer Niederspannungsverteilungsanlage sind folgende Grundparameter festzulegen:
- Bemessungsströme: Sammelschiene, Abzweige, Einspeisung
- Schutz- und Aufstellungsort inkl. Schutzart
- Schutzklasse gegen elektrischen Schlag
- Geräteeinbauart: Festeinbau, Einschub- oder Stecktechnik
- Verwendungszweck: Hauptverteiler, Unterverteiler, Motor-Control-Center, Licht- und Steckdosenverteiler
- Steuerungskonzept

---

### 15.1 Vorschriften und Normen

- Der **VDE** (Technisch Wissenschaftlicher Verband der Elektrotechnik, Elektronik und Informationstechnik, gegründet 1893) erarbeitet Schutzbestimmungen gegen elektrische Gefahren.
- Die **DKE** (Deutsche Elektrotechnische Kommission in DIN und VDE) ist nationale Normungsorganisation für nationale und internationale Normen.
- VDE-Bestimmungen sind **kein Gesetz**, gelten aber als anerkannte Regeln der Technik.
- Verstöße sind nicht direkt strafbar; Strafverfolgung droht nur bei nachweisbarem Unfallzusammenhang durch Nichteinhaltung.

**Bestandteile des VDE-Vorschriftenwerks:**
- **Satzung:** Anforderungen für öffentlich-rechtliche Anerkennung des VDE-Werks
- **VDE-Bestimmungen:** Sicherheitstechnische Festlegungen für Errichten, Herstellen und Betreiben elektrischer Anlagen und Betriebsmittel; auch Blitzschutz
- **VDE-Richtlinien:** Stand-der-Technik-Hinweise, Beispielsammlungen für eigene sicherheitstechnische Entscheidungen
- **VDE-Vornormen:** Nicht Teil des deutschen Normenwerks, behandeln normungswürdige Gegenstände
- **VDE-Beiblätter:** Erläuterungen zu VDE-Bestimmungen, keine Festlegungen, nur Empfehlungen

---

### 15.3 Rechtliche Bedeutung des VDE-Werks

Relevante Gesetze und Verordnungen mit Bezug auf VDE-Bestimmungen:

- **Energiewirtschaftsgesetz:** §1 der 2. DVO verlangt Beachtung der anerkannten Regeln der Technik bei Errichtung und Unterhaltung elektrischer Anlagen
- **Gesetz über technische Arbeitsmittel (§3 Abs.1):** Technische Arbeitsmittel dürfen nur in Verkehr gebracht werden, wenn sie nach anerkannten Regeln der Technik sowie Arbeitsschutz- und Unfallverhütungsvorschriften Benutzer und Dritte ausreichend schützen
- **Niederspannungsverordnung:** Elektrische Betriebsmittel von 50–1000 V Wechselstrom bzw. 75–1500 V Gleichstrom müssen dem EG-Stand der Sicherheitstechnik entsprechen (VDE-Bestimmungen spiegeln diesen Stand)
- **Medizingerätesicherheit:** Medizinische Geräte müssen Medizingeräteverordnung sowie allgemeinen Regeln der Technik entsprechen
- **Explosionsschutz:** Genehmigungsbedürftige oder überwachungspflichtige Anlagen unterliegen VDE-Bestimmungen
- **DGUV Vorschrift 3 (früher BGV A3):** Elektrische Anlagen und Betriebsmittel müssen nach anerkannten Regeln der Technik errichtet, betrieben, geändert und instandgehalten werden

**Übersicht Gesetze und Verordnungen (Tab. 15.1):**

| Instrument | Inhalt/Zweck |
|---|---|
| Grundgesetz | Staatliche Fürsorgepflicht |
| Ordnungsrecht / Polizeirecht | Gefahrenabwehr für öffentliche Sicherheit |
| Baurecht / Bauaufsichtsrecht | Sicherheit für Leben und Gesundheit im Bau- und Siedlungswesen |
| Bauplanungsrecht | Planungsbehörden; z.B. EltBAuVo (Verordnung über Betriebsräume für elektrische Anlagen) |
| Landesbauordnungen | Verordnungen für besondere Bauten (z.B. Arbeitsstätten-Richtlinie) |
| Anerkannte Regeln der Technik | Praxiserprobter Stand, maßgeblich für strafrechtliche und zivilrechtliche Haftung |
| DGUV Vorschrift 3 | Gesetzliche Unfallverhütungsvorschriften; verbindlich für Unternehmer, Versicherte, Vorgesetzte |
| Gewerbeordnung | Bindend für Planer und Errichter |
| AvBEltV | Regelung des Anschlusses an das Versorgungsnetz |
| TAB | Bedingungen für Ausführung der Elektroinstallation von Tarifkunden |
| Merkblätter | Kein Gesetzescharakter; bindend wenn Vertragsbestandteil |
| HEA | Anforderungen, Planung und Bewertung der Elektroinstallation in Gebäuden mit drei Ausstattungswerten |
| VdS | Vorschriften und Merkblätter zu Schäden; enthält Hinweise für Planung, Bau und Betrieb elektrischer Anlagen; Beachtung zwingend |

---

### 15.4 Gesetzliche Regelungen, HOAI und VOB

- Bei öffentlichen Aufträgen gilt **VOB** (Verdingungsordnung für Bauleistungen) als Vertragsgrundlage, **HOAI** (Honorarordnung für Architekten und Ingenieure) regelt Entgelte.
- Besonders relevante VOB-Normen: **DIN 18382** (Kabel- und Leitungsanlagen in Gebäuden, VOB Teil C), **DIN 18299** (Allgemeine Regelungen alle Bauarten), **DIN 18384 Teil C** (Blitzschutzanlagen)
- Die **HOAI** regelt Honorarzonen:

| Honorarzone | Inhalte |
|---|---|
| I | Einfache Niederspannungs- und Fernmeldeinstallationen |
| II | Kompaktstationen, Niederspannungsinstallations- und -verteilungsanlagen (soweit nicht in I oder III), Blitzschutzanlagen, Beleuchtungsanlagen |
| III | HS- und MS-Anlagen, NS-Schaltanlagen, Eigenstromerzeugungs- und Umformeranlagen, NS-Leitungsanlagen und Beleuchtungsanlagen mit hohem Planungsaufwand, große Fernmeldeanlagen und -netze |

- Leistungsbild „Technische Ausrüstung" umfasst nach §73 alle Auftragnehmerleistungen
- Kostenmittlung durch den Elektroplaner nach **DIN 276** mit Kostengruppen
- Leistungsverzeichnis (Raumbuch) oder Anlagenbeschreibung nach DIN/DIN VDE möglich
- Die ausführende Firma muss Bedenken gegen vorgesehene Ausführungsart **schriftlich** mitteilen
- Nach Fertigstellung: Übersichtsschaltpläne und Installationspläne nach **DIN EN 61346** liefern
- Vor Inbetriebnahme: Prüfung nach **DIN VDE 0100-600**

**Zeitlicher Ablauf einer Projektierung:**
1. Kundenanfrage
2. Vorentwurf und Angebotsabgabe
3. Kostenschätzung nach DIN 276
4. Verhandlung
5. Projektbeginn, Bearbeitung
6. Planerstellung, Ausschreibung
7. Auftragserstellung
8. Ausführung, Überwachung
9. Montage
10. Inbetriebnahme, Messungen
11. Übergabe, Dokumentation, Gewährleistung

---

### 15.5 Richtlinien für die Projektierung elektrischer Anlagen

Nach **DIN EN 61346** erforderliche Unterlagen:

1. **Leistungsbilanz** der Gesamtanlage: NS (230 V, 400 V, 690 V), MS (6 kV, 10 kV, 20 kV), ggf. HS (110 kV, 220 kV, 380 kV)
2. **Motorenlisten** nach IEC 60034, DIN VDE 0530 mit: Bemessungsleistung (kW), Spannung (V), Drehzahl (U/min), Drehmoment (Nm), Massenträgheitsmoment (kg·m²), Umgebungstemperatur (°C), Motorart/-klasse, Bauform/Baugröße/Schutzart, Fabrikat, Zubehör, Klemmenbezeichnungen, Lastdaten, Betriebsart, Anzugsmoment/-strom, Wirkungsgrad, Schaltspiel
3. **Übersichtsschaltpläne:** Vereinfachte Darstellung mit Spannungen, Frequenz, Leistung, Klemmenbezeichnungen, Transformatordaten
4. **Netzpläne:** Maßstabfreie Darstellung aller Verbindungen und Netzteile
5. **Ein- oder dreipolige Schaltpläne:** HS/MS/NS-Schaltanlagen, Licht-/Kraft-/Kommunikations-/Gleichstromverteilungen, Notstromversorgung
6. **Anordnungsplan:** Räumliche Lage aller elektrischen Betriebsmittel
7. **Trassenpläne:** Art und Weise der Kabelverlegung (z.B. auf Kabelpritschen)
8. **Bauangaben:** Lagerichtige Darstellung von Transformatoren, Schalträumen, Kabelkanälen, Durchbrüchen, Verteilungen
9. **Funktionsbeschreibungen:** Betriebsbedingungen, Anzahl/Art der Steuerungen als Logikplan, Funktionsplan, Struktogramm oder PAP
10. **Stromlaufplan** nach IEC 61082: DIN A3 oder A4, mit Überstromschutzeinrichtungen, Geräten, Klemmen/-leisten, Verlegearten, Querschnitten, Leistungen, Spannungen, Frequenzen und Stückliste
11. **Klemmen- und Rangierpläne:** Anschlusspläne für Klemmenleisten, Klemmennummer, Zielbezeichnungen, Kabeltyp
12. **Kabelliste:** Kabelnummer, Typ, Querschnitt, Spannung, Aderzahl, Länge, Verlegung
13. **Erdungs- und Blitzschutzpläne** nach EN 50522, DIN VDE 0100 Teil 540, DIN VDE 0185
14. **Kommunikationsanlagen:** Sprech-, Telefon-, Brandmeldeanlagen auf eigenen Installationsplänen
15. **Materiallisten:** Beschaffenheit des Elektromaterials und Vergabeunterlagen
16. **Montagezeitplan:** Gesamter Ablauf mit Zeitabschnitten und Stunden
17. **Dokumentation:** Nach Fertigstellung alle Zeichnungen, Unterlagen und Messurkunden prüfen und aktualisieren

---

### 15.7 Darstellung der Schaltungsunterlagen (IEC 61082)

Definitionen wichtiger Planarten:
- **Stromlaufplan:** Ausführliche Darstellung einer Schaltung, zeigt Wirkungsweisen elektrischer Schaltungen
- **Übersichtsschaltplan:** Vereinfachte einpolige Darstellung mit Adernkennzahl
- **Anschluss- und Verdrahtungsplan:** Innere und äußere Verbindungen plus Einbauort der Betriebsmittel
- **Anordnungsplan:** Räumliche Lage der Betriebsmittel
- **Ersatzschaltplan:** Eigenschaften von Stromkreisen für Analyse und Berechnung
- **Schaltzeichen:** Kennzeichnung der Betriebsmittel
- **Schaltgeräte:** Sichern einwandfreien Stromfluss
- **Betriebsmittel:** Alle Teile einer elektrischen Anlage bzw. eines Stromkreises

---

### 15.8 Inhalt der Elektroinstallation

Für einheitliche Installationspläne notwendige Angaben:
1. Anschlussstelle des Netzbetreibers (Hausanschlusskasten, Trafostation)
2. Netz- und Betriebsbedingungen
3. Umgebungsbedingungen
4. Schutzmaßnahme und Schutzart
5. Verlegeart der Leitungen und Kabel
6. Querschnitte der Leitungen und Kabel
7. Zuordnung von Überstromschutzeinrichtungen zu Leitungen/Kabeln
8. Installationshöhe der Schalter und Steckdosen
9. Kennbuchstaben bzw. Zählnummer für Schutzeinrichtungen, Betriebsmittel, Klemmenbezeichnungen
10. Einheitliche Schaltzeichen und Symbole für alle Betriebsmittel

---

### 15.9 Bestimmung der Anschlussleistung

- Richtwerte für Gleichzeitigkeitsfaktoren und installierte Leistung je Verbraucher berücksichtigen
- Untere Grenze bereitzustellender Leistung: **2,5 kVA** (1 Wohneinheit)
- Bei Industrieanlagen: eigene Leistungsbilanz je Verteileranlage erstellen
- Bei gegenseitiger Verriegelung: Verbrauch der größten Anschlussleistung berechnen

---

### 15.10 Elektrische Leistungsformeln

**Formeln (Übersicht):**

| Nr. | Anwendung | Formel |
|---|---|---|
| 1 | Einzelverbraucher (Motor): Zugeführte = abgegebene Leistung dividiert durch Wirkungsgrad | Pzu = Pab / η |
| 2 | Leistung Drehstrom | Pzu = √3 · U · I · cos φ |
| 3 | Strom Drehstrom | I = Pzu / (√3 · U · cos φ) |
| 4 | Leistung Wechselstrom | Pzu = U₀ · I · cos φ |
| 5 | Strom Wechselstrom | I = Pzu / (U₀ · cos φ) |
| 6 | Mittlerer Leistungsfaktor | cos φ_mit = (P1·cos φ1 + P2·cos φ2 + … + Pn·cos φn) / (P1 + P2 + … + Pn) |
| 7 | Gesamtstrom mit Gleichzeitigkeitsfaktor g (Drehstrom) | I_ges = Pzu / (√3 · U · cos φ · g) |
| 8 | Anschlussleistung der Anlage | PG = P_inst · g |

Symbole: U = Spannung zwischen Außenleitern (V), U₀ = Spannung Außenleiter zu Sternpunkt (V), I = Strom je Phase (A), Pzu = zugeführte Leistung (W), η = Wirkungsgrad, PG = Gesamtleistung (W), P_inst = installierte Leistung (W), g = Gleichzeitigkeitsfaktor

---

### 15.11 Anschlusswerte von Elektrogeräten

Bemessungsgrundlage: DIN VDE-Bestimmungen und DIN 18015 Teil 1.

**Tab. 15.3 — Leuchtstofflampen-Vorschaltgeräte (Anschlusswerte):**

| Lampentyp | KVG (W) | EVG (W) | Länge (mm) |
|---|---|---|---|
| 1 × 18 W | 28 | 19 | 590 |
| 2 × 18 W | 38 | — | — |
| 1 × 36 W | 46 | 36 | 1200 |
| 2 × 36 W | 74 | — | — |
| 1 × 58 W | 71 | 57 | 1500 |
| 2 × 58 W | 114 | — | — |

**Tab. 15.4 — Anschlusswerte typischer Elektrogeräte:**

| Betriebsmittel | Anschlusswert (kW) |
|---|---|
| Elektroherd | 12 |
| Grillgerät | 2 |
| Mikrowelle | 1,5 |
| Warmwasserboiler | 2 |
| Kühlschrank | 0,2 |
| Klimagerät | 3 |
| Gefriergerät | 0,3 |
| Fritteuse | 2 |
| Geschirrspülmaschine | 3,5 |
| Waschmaschine | 3,5 |
| Wäschetrockner | 3,5 |
| Bügelmaschine | 2 |
| Einbaubackofen | 2,5–5 |
| Haartrockner | 0,8 |
| Staubsauger | 1,0 |
| Fernsehgerät | 0,35 |
| Rasenmäher | 1 |
| Sonnenbank | 2,8 |
| Tauchsieder | 2 |
| Toaster | 2 |
| Trockner | 3,3 |
| Warmwasserspeicher 15 l | 4 |
| Warmwasserspeicher 80 l | 6 |
| Durchlauferhitzer 30–120 l | 18, 21, 24 |

---

### 15.12 Richtwerte für die Anlagenberechnung

**Tab. 15.5 — Steckdosen-Anschlusswerte:**

| Typ | P (kW) | IB (A) | gL,In (A) | Querschnitt (mm²) |
|---|---|---|---|---|
| Wechselstrom | 3,5 | 16 | 25 | 4 |
| Drehstrom | 11 | 16 | 16 | 2,5 |
| Drehstrom | 22 | 32 | 35 | 10 |

Leistungen pro Steckdose und max. Steckdosen pro Stromkreis:
- Wohnung: 0,2 kW, bis zu **16 Steckdosen** pro Stromkreis
- Landwirtschaft: 0,4 kW, bis zu **8 Steckdosen** pro Stromkreis
- Gewerbe/Industrie: 0,5 kW, bis zu **6 Steckdosen** pro Stromkreis

**Tab. 15.6 — Sicherungsgrößen und Anschlussquerschnitte:**

| Größe | Nennstrombereich (A) | Anschlussquerschnitt (mm²) |
|---|---|---|
| 00 | 6–100 | 16–50 |
| 0a | 6–160 | 35–95 |
| 1 | 80–250 | 70–150 |
| 2 | 125–400 | 150–300 |
| 3 | 315–630 | 2 × (40–5) |
| 4 | 500–1250 | 2 × (60–5) |
| 4a | 500–1250 | 2 × (80–5) (nur Ersatzbedarf, nicht für Neuanlagen) |

**Tab. 15.7 — Auswahl Überstromschutzeinrichtungen:**

| Gerät | Typen | Strombereich (A) |
|---|---|---|
| Leitungsschutzschalter | B | 6–63 |
| | C | 0,5–63 |
| | K | 2–125 |
| | Z | 0,5–63 |
| | E | 10–100 |
| Neozed-Sicherungen | D01 | 2–16 |
| | D02 | 20–63 |
| | D03 | 80–100 |
| NH-Sicherungen | NH00 | 6–100 |
| | NH0 | 6–160 |
| | NH1 | 80–250 |
| | NH2 | 125–400 |
| | NH3 | 315–630 |
| | NH4a | 500–1250 |

**Richtwerte für Berechnungen:**
- Wirkungsgrad von Motoren: η = 0,85; cos φ = 0,82
- Leuchtstofflampen zweiflammig (kompensiert): cos φ = 0,95
- Leuchtstofflampen einflammig (unkompensiert): cos φ = 0,42
- Leistungen mit Drossel nach TAB: L18 W → 26 W, L36 W → 44 W, L58 W → 69 W

**Tab. 15.8 — Belastbarkeit der Hauptleitung nach DIN 18015 Teil 1:**

Ohne elektrische Warmwasserbereitung:

| Wohneinheiten | Sicherungsgröße (A) |
|---|---|
| 1–5 | 63 |
| 6–10 | 80 |
| 11–18 | 100 |
| 19–36 | 125 |
| 37–100 | 160 |

Mit elektrischer Warmwasserbereitung:

| Wohneinheiten | Sicherungsgröße (A) |
|---|---|
| 1 | 63 |
| 2 | 80 |
| 3 | 100 |
| 4–6 | 125 |
| 7–11 | 160 |
| 12–22 | 200 |
| 23–48 | 250 |

**Tab. 15.9 — Gleichzeitigkeitsfaktoren nach Badenwerk:**

| Anzahl WE | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| gS (Speicher) | 1 | 0,72 | 0,60 | 0,53 | 0,47 | 0,44 | 0,41 | 0,39 | 0,37 | 0,35 |
| gD (Durchlauf) | 1 | 0,63 | 0,48 | 0,38 | 0,32 | 0,28 | 0,26 | 0,22 | 0,20 | 0,19 |
| gF (Fußbodenheizung) | 0,9 | 0,8 | — | — | — | — | — | — | — | — |
| gZ (Zentralspeicher) | 1 | — | — | — | — | — | — | — | — | — |

---

### 15.13 Berechnung der Hauptversorgungsleitung

Formeln für elektrisch versorgte Wohngebäude:

**Warmwasser über Speicher (< 10 Wohneinheiten):**
P = PH · gH + 12 · n · gS

**Warmwasser über Durchlauferhitzer (< 10 Wohneinheiten):**
P = PH · gH + 10 · n · gA + PDE · gD

Symbole:
- P = Bemessungsleistung des Hauptversorgungssystems
- PH = Gesamtheizleistung inkl. Wassererwärmung (installiert)
- PDE = Aufnahmeleistung aller Durchlauferhitzer
- n = Anzahl der Wohneinheiten
- gS = Gleichzeitigkeitsfaktor Warmwasserspeicher
- gD = Gleichzeitigkeitsfaktor Durchlauferhitzer
- gF = Gleichzeitigkeitsfaktor Fußbodenheizungsgeräte
- gZ = Gleichzeitigkeitsfaktor Zentralspeicher

---

### 15.14 Elektrische Anlagen — Leistungsbedarf und Gleichzeitigkeitsfaktoren

Frühzeitig festzulegen bei Netz- und Anlagenplanung:
- Erdungsart
- Gesamtleistung der Anlage
- Größe und Anzahl der Transformatoren
- Kabel- und Leitungsquerschnitte
- Betriebs- und Kurzschlussströme, Lastverteilung

Formel für maximalen Leistungsbedarf:
**Pmax = Σ (Pi · gi)**

Der Gleichzeitigkeitsfaktor (Bedarfsfaktor) gi gibt an, wie viele Verbraucher gleichzeitig in Betrieb sind. Werte stammen aus Erfahrungswerten oder Messungen.

Für Haushaltskunden gilt näherungsweise:
- gn = g1 + (1 − g1) / (4√(n³)); g1 = 0,06 bis 0,07
- Alternativ: g = 100% / n^x oder g = 0,07 + 0,93/n; Nutzungsfaktor x = 0,06 bis 1

Bei Anlagen mit überwiegend motorischen Antrieben:
**Pmax = Σ (PrM · gi · ai / ηi)**
- ai = Auslastungsfaktor der Motoren
- ηi = Wirkungsgrad des jeweiligen Motors
- PrM = Bemessungsleistung des Motors

**Tab. 15.10 — Gleichzeitigkeitsfaktoren für Verbrauchergruppen:**

| Verbrauchergruppe | Bürogebäude | Krankenhäuser | Kaufhäuser |
|---|---|---|---|
| Beleuchtung | 0,85–0,95 | 0,7–0,9 | 0,85–0,95 |
| Steckdosen | 0,1–0,15 | 0,1–0,2 | 0,2 |
| Küchen | 0,5–0,85 | 0,6–0,8 | 0,6–0,8 |
| Klimaanlagen | 1 | 1 | 1 |
| Aufzüge/Rolltreppen | 0,7–1 | 0,5–1 | 0,7–1 |

**Tab. 15.11 — Gleichzeitigkeitsfaktoren Haupteinspeisung nach Gebäudetyp:**

| Gebäudeart | Teilbereich | Faktor |
|---|---|---|
| Wohngebäude | — | 0,4 |
| Wohnblocks mit elektr. Heizung | — | 0,8–1 |
| Wohnblocks ohne elektr. Heizung | — | 0,6 |
| Bürohochhaus | Lüftung/Heizung | 1 |
| | Datenverarbeitung | 1 |
| | Beleuchtung | 1 |
| | Sprinkleranlage | 1 |
| | Sanitäranlage | 0,8 |
| | Aufzüge | 0,7 |
| | Kälteanlage | 1 |
| Schulen | — | 0,6–0,7 |
| Versammlungsräume, Theater, Restaurants | — | 0,6–0,8 |
| Ladengeschäfte | — | 0,6–0,7 |
| Verkehrsanlagen | — | 1 |
| Verwaltungsgebäude/Banken | — | 0,7–0,9 |
| Kindergärten | — | 0,6–0,9 |
| Schreinereien | — | 0,2–0,6 |
| Metzgereien | — | 0,5–0,8 |
| Bäckereien | — | 0,4–0,8 |
| Baustellen | — | 0,2–0,4 |
| Kräne | — | 0,7 je Kran |

**Tab. 15.12 — Gleichzeitigkeitsfaktoren für Wohnungen:**

| Anzahl Wohnungen | Gleichzeitigkeitsfaktor |
|---|---|
| 2–4 | 1 |
| 5–9 | 0,78 |
| 10–14 | 0,63 |
| 15–19 | 0,53 |
| 20–24 | 0,49 |
| 25–29 | 0,46 |
| 30–34 | 0,44 |
| 35–39 | 0,42 |
| 40–49 | 0,41 |
| ≥ 50 | 0,40 |

---

### 15.15 Berechnungsbeispiel: Hochhaus-Projektierung

**Objekt:** Wohn- und Geschäftsgebäude ohne elektrische Warmwasserbereitung; 15 Wohneinheiten, Allgemeinbedarf, Büro; zentraler Zählerplatz.

**a) Leistungsbedarf:**

1. Wohneinheiten (15 WE): P1 = 15 kVA/WE × 15 = 63 kVA → 59,85 kW (cos φ = 0,95); theoretischer g-Faktor für 15 WE = 0,28; Absicherung: NH00/100 A
2. Allgemeinbedarf: P2 = 11 kVA × 0,7 = 7,7 kVA → 7,3 kW
3. Büro: P3 = 80 kVA × 0,7 = 56 kVA → 53,2 kW
4. Gesamtleistung: PG = 59,85 + 7,3 + 53,2 = **120,35 kW** (≈ 126,86 kVA bei cos φ = 0,95)

**b) Bemessungsströme und Leitungsauswahl:**

**1. Hauptzuleitung HAK → Hauptverteiler:**
- IB = 120,35 kW / (√3 × 400 V × 0,95) = **182,9 A**
- Schutzeinrichtung: NH1-200 A (Bedingung: In > IB)
- Verlegeart C, 3 belastete Adern, 25 °C, ohne Häufung
- Korrekturfaktoren: f1 (Temperatur 25°C) = 1,06; f2 (Wand, kein Häuf) = 1,0
- Bemessungsregel: Iz_erf = 200 A / (1,06 × 1,0) = 188,7 A
- Auslöseregel: Iz_erf = (200 A × 1,6) / (1,45 × 1,06 × 1,0) = 208,2 A
- Ergebnis nach Tab. 10.2 Spalte 11: **223 A → NYY-J 4 × 95 mm²**

**2. Zuleitung Zähler Allgemeinbedarf:**
- IB ≈ 11,1 A; In = 63 A gG/NH00; Verlegeart C, 25 °C, 2 Systeme Häufung
- f1 = 1,06; f2 = 0,94
- Bemessungsregel: Iz = 63 / (1,06 × 0,94) = 63,23 A
- Auslöseregel: Iz = 63 × 1,6 / (1,45 × 1,06 × 0,94) = 69,77 A
- Ergebnis: **76 A → NYY-J 4 × 16 mm²**

**3. Zuleitung Zähler Büro:**
- IB ≈ 80,83 A; In = 100 A gG/NH00; Verlegeart C, 25 °C, 2 Systeme
- f1 = 1,06; f2 = 0,94
- Bemessungsregel: Iz = 100 / (1,06 × 0,94) = 100,4 A
- Auslöseregel: Iz = 100 × 1,6 / (1,45 × 1,06 × 0,94) = 110,8 A
- Ergebnis: **119 A → NYY-J 4 × 35/16 mm²**

**4. Zuleitung Wohnungs-HV-Zählerverteilung:**
- IB = 59,85 kW / (√3 × 400 V × 0,95) = **90,93 A**
- In = 100 A gG/NH; Verlegeart C, 25 °C, ohne Häufung
- f1 = 1,06; f2 = 1
- Bemessungsregel: 94,4 A; Auslöseregel: 104,1 A
- Ergebnis: **119 A → NYY-J 4 × 35/16 mm²**

**5. Zuleitung zur Wohnungseinheit:**
- IB = 14,2 kW / (√3 × 400 V × 0,95) = **21,65 A**
- In = 63 A gG/NH00; Verlegeart C, 25 °C, ohne Häufung
- f1 = 1,06; f2 = 1
- Bemessungsregel: 59,43 A; Auslöseregel: 65,58 A
- Ergebnis: **76 A → NYY-J 4 × 16 mm²**

**6. Endstromkreise Wohnungsinstallation:**
- IB = 16 A; In = 16 A MCB; Verlegeart B1 (Rohr im Mauerwerk), 25 °C, 2 belastete Adern, ohne Häufung
- f1 = 1,06; f2 = 1
- Bemessungsregel: 15,09 A; Auslöseregel: 16,66 A
- Ergebnis: **17,5 A → NYY-J 3 × 1,5 mm²**

**c) Spannungsfälle (Leitertemperatur 50 °C, Korrekturfaktor 1,12):**

1. HAK → Hauptverteiler: In=200 A; S=4×95 mm²; l=25 m; cos φ=0,95 → **Δu = 0,45 %** (max. 1 % nach TAB für 100–250 kVA: erfüllt)
2. Hauptverteiler → Zähler Allgemeinbedarf: In=63 A; S=5×16 mm²; l=25 m → **Δu = 0,84 %**; Gesamt ungezählt: 0,45+0,84 = 1,29 %; verbleibender Rest für Endstromkreise: max. 3 % nach DIN 18015-1
3. Hauptverteiler → Zähler Büro: In=100 A; S=4×35/16 mm²; l=35 m → **Δu = 0,85 %**; Gesamt: 1,3 %
4. Hauptverteiler → zentraler Zählerverteiler Wohnungen: In=100 A; S=4×35/16 mm²; l=25 m → **Δu = 0,61 %**; Gesamt: 1,11 %
5. Zähler → Wohnraumverteiler: In=63 A; S=5×16 mm²; l=25 m → **Δu = 0,84 %**; Rest für Endstromkreise: 3% − 0,85% = **2,15 %**
6. Endstromkreise Steckdosen: In=16 A; S=3×1,5 mm²; l=20 m; Un=230 V → **Δu = 3,65 %** — überschreitet die zulässigen 2,15 %!
   - Abhilfe: Querschnitt auf **2,5 mm²** erhöhen **oder** Bemessungsstrom des LSS auf **10 A** reduzieren

**d) Selektivitätskontrolle:**

1. Sicherung-Sicherung: gG-Sicherungen bis AC 400 V sind im Verhältnis 1:1,6 selektiv; in der Praxis Verhältnis 1:2 empfohlen
2. Sicherung-LSS-Kombination: Kennlinienvergleich nach DIN EN 60898-1 erforderlich; bei NH00-63A-gG + MCB-16A-B (Strombegrenzungsklasse 3): Vollselektivität nur bis **2 kA** herstellerübergreifend; bei Kurzschlussstrom an Wohnungsverteilern < **1,7 kA** → Vollselektivität vorhanden; ab ca. **4 kA** Back-up-Schutz erforderlich (63-A-Vorsicherung löst schneller aus als LSS)

**e) Abschaltbedingungen nach DIN VDE 0100 Teil 410:**

Prüfbedingung im TN-System: Zs = U₀/Ia
- U₀ = 230 V bei 230/400-V-Netzen
- Minimaler einpoliger Fehlerstrom nach DIN EN 60909-0: c_min × U₀ = 0,9 × 230 V = 207 V

Berechnung bei Kurzschlusstemperatur PVC-Kupfer = 160 °C (Korrekturfaktor 1,56 für Widerstandserhöhung von 20°C auf 160°C); Reaktanz x' = 0,082 mΩ/m:

- Hauptzuleitung HAK→HV (l=25 m, S=70 mm²): ZS = 21,03 mΩ
- Zählerverteilung Wohnung (l=25 m, S=35 mm²): ZS = 41,26 mΩ
- Unterverteilung Wohnung (l=25 m, S=16 mm²): ZS = 90,27 mΩ
- Steckdose (l=20 m, S=1,5 mm²): ZS = 770,37 mΩ

Gesamtkurzschlussimpedanz: Zk = ZV + ZAnlage = 300 mΩ + 21,03 + 41,26 + 90,27 + 770,37 = **1,23 Ω**

Einpoliger Kurzschlussstrom an der Steckdose:
I''k1 = (0,9 × 400 V) / (√3 × 1,23 Ω) = **168,98 A**

Abschaltstrom MCB: Ia = 5 × 16 A = 80 A → I''k1 (168,98 A) > Ia (80 A): **Forderung erfüllt**

---

### 15.16 Berechnungsbeispiel: Kücheninstallation

**Objekt:** Einbauküche in Altbau; Anschlussspannung 400/230 V, 50 Hz; UP-Verlegung; Schutzmaßnahme Abschaltung nach DIN VDE.

**Tab. 15.13 — Anschlusswertberechnung Küche:**

| Betriebsmittel | Anzahl | Stromkreis-Nr. | Anschlusswert (kW) |
|---|---|---|---|
| Elektroherd | 1 | 1 | 12 |
| Kühlschrank | 1 | 2 | 0,5 |
| Geschirrspüler | 1 | 3 | 3,5 |
| Waschmaschine | 1 | 4 | 2,2 |
| Trockner | 1 | 5 | 3,5 |
| Gefriergerät | 1 | 6 | 0,4 |
| Mikrowelle | 1 | 7 | 2,0 |
| Dunstabzugshaube | 1 | 8 | 0,1 |
| Steckdosen (11 Stück) | — | 8 | 2,0 |
| Leuchtstofflampen (4 Stück) | — | 9 | 0,12 |
| Glühlampen (3 Stück) | — | 9 | 0,18 |
| **Installierte Leistung Pi** | | | **26,5 kW** |
| Gleichzeitigkeitsfaktor 0,7 | | | 18,55 kW |
| Reserve 20 % | | | 3,71 kW |
| **Gesamtanschlussleistung PG** | | | **22,26 kW** |

**Ermittlung der Verteilerzuleitung:**
- PG (für Berechnung) = 9,54 kW (Teilmenge ohne Herd-Direktanschluss)
- IB = 9,54 kW / (√3 × 400 V × 0,95) = **33,82 A**
- Schutz bei Überlast (Verlegeart B2 nach DIN VDE 0100-520 Beiblatt 2): IB ≤ In ≤ Iz → 33,82 A ≤ 40 A ≤ 55 A
- Ergebnis: **NYM-J 5 × 10 mm²** (nach TAB bzw. DIN 18015)
- Übersichtsschaltplan nach DIN EN 61346 und DIN EN 61355 zu erstellen

---

### 15.17 Berechnungsbeispiel: Industrieanlage

**Objekt:** Anlage mit mehreren Unterverteilungen (UV1–UV4); Leistungsfaktor UV1 = 0,8; Gleichzeitigkeitsfaktor 0,8.

Gesamtleistung:
PG = P1 + P2 + P3 + P4 = 55 + 30 + 20 + 55 + 10 = **170 kW**

Gewählte Transformatornennleistung: **250 kVA**, 400/230 V, 50 Hz, uk = 4 %

Zuleitung Unterverteilung 4 (beispielhaft):
- IB = 55 kW / (√3 × 400 V × 0,8) = **99,23 A**
- Bedingung nach DIN VDE 0100-430: IB ≤ In ≤ Iz → 99,23 A ≤ 125 A ≤ 144 A
- Leitung: **NYY-J 4 × 50 mm²**
- Spannungsfall: ΔU = 144 A × √3 × 40 m × 0,8 / (56 m/(Ω·mm²) × 50 mm²) = **2,85 V** → Δu = 2,85 V × 100 % / 400 V = **0,712 %**

---

### 15.18 Berechnungsbeispiel: Energieversorgung einer Fabrik

**Objekt:** Fabrik; Einspeisung 20 kV, Verbrauchernetz 400/230 V, 50 Hz; cos φ_ges = 0,84; Reserve 30 %.

**Verbrauchergruppen:**
1. Beleuchtung: 230 × 100 W + 190 × 60 W + 140 × 40 W = 34,8 kW + 11,4 kW + 5,6 kW = 51,8 kW aktiv installiert (wird gewichtet mit g=0,68 berechnet), Anteil = **40 kW × 0,68 = 27,2 kW**
2. Motoren:
   - 12 × 5,5 kW / η=0,85 = 77,65 kW
   - 32 × 3 kW / η=0,80 = 120 kW
   - 10 × 2 kW / η=0,80 = 25 kW
   - PMGes = (77,65 + 120 + 25) × g=0,43 = **95,74 kW**
3. Thermische Heizung: 230 kW × g=0,57 = **131,1 kW**

Gesamtleistung der Fabrik: PG = 27,2 + 95,74 + 131,1 = **254 kW**

Scheinleistung: S = 254 kW / 0,84 = **302,43 kVA**

Mit 30 % Reserve: SG = 302,43 + 90,73 = **393,16 kVA**

Gewählte Transformatornennleistung: **500 kVA**

Ströme des Transformators (500 kVA):
- Niederspannungsseite: ILV = 500 kVA / (√3 × 0,4 kV) = **721,58 A**
- Hochspannungsseite: IHV = 500 kVA / (√3 × 20 kV) = **14,43 A**

Betriebsströme (bei 393,16 kVA):
- NS-seitig: INS = 393,16 kVA / (√3 × 0,4 kV) = **567,47 A**
- HS-seitig: IHS = 393,16 kVA / (√3 × 20 kV) = **11,35 A**

---

### 15.19 Technische Anschlussbedingungen (TAB)

Die TAB regeln Anschluss und Betrieb von Anlagen am Versorgungsnetz; bestimmte Verbrauchsmittel bedürfen vorheriger Zustimmung des Netzbetreibers.

1. **Inbetriebnahme:** Einsatz von Überstromschutzeinrichtungen, RCD oder Hauptschalter möglich
2. **Plombenverschlüsse:** Anlagenteile mit ungezählter Energie müssen plombiert werden
3. **Zählerplätze:** Leicht zugängliche Räume wählen; feuchte Räume, Garagen, Heizräume vermeiden (Ausnahme: Räume mit Feuerstätten ≤ 50 kW gelten nicht als Heizräume); selektiver Hauptleitungsschutzschalter im unteren Anschlussraum bei vielen Netzbetreibern erlaubt
   - Mögliche Bestückungen nach DIN 18105 Teil 1: 63 A, 63–100 A, oder >100 A Belastbarkeit
   - Für Familienhäuser > 3 Wohneinheiten: eigene Hausanschlussräume nach DIN 18015
4. **Spannungsfall:** Zulässige Werte beachten
5. **Kurzschlussfestigkeit:** Von Leitungsschutzschaltern hinter dem Hausanschluss: 25, 16 oder 6 kA
6. **Selektivität:** Zwischen Sicherungen und LSS sicherstellen
7. **Hauptleitung:** Mit Gleichzeitigkeitsfaktor der Anlage festlegen
8. **Elektrowärmegeräte:** Ab **4,6 kW** Drehstromanschluss vorschreiben
9. **Durchlauferhitzer:** Thermisch gesteuerte Geräte ab **6 kW** müssen Gegenwiedereinschaltungseinrichtungen haben
10. **Heizung/Klimageräte:** Ab **2 kW** Drehstromanschluss vorsehen
11. **Netzrückwirkungen:** Zu vermeiden
12. **Schwingungspaketsteuerung:** Grenzwerte der Anschlussleistung nach TAB Tabelle 1 beachten
13. **Anschnittssteuerung von Gleichrichtern:** Grenzwerte nach TAB Tabelle 2 beachten
14. **Schutzmaßnahmen:** Fehlerschutz nach DIN VDE 0100 Teil 410; in Neubauten Fundamenterder nach **DIN 18014** planen
15. **Eigenerzeugeranlagen:** Planung, Errichtung und Betrieb nach **VDE-AR 4105**

---

### 16 Schutz gegen elektrischen Schlag (Einleitung)

Grundlage: **DIN VDE 0100 Teil 410**. Schutz kann sichergestellt werden durch:
- Kombinierten Schutz bei Normalbetrieb und Fehlerfall (direktes und indirektes Berühren)
- Schutz nur im Normalbetrieb (Basisschutz / direktes Berühren)
- Schutz nur im Fehlerfall (Fehlerschutz / indirektes Berühren)

**Körperimpedanz in Abhängigkeit von Berührungsspannung:**
- Bei 50 V Berührungsspannung:
  - 90 % der Bevölkerung: Körperimpedanz steigt auf **5000 Ω**
  - 10 % der Bevölkerung: Impedanz fällt auf **1000 Ω**
  - 99 %: steigt auf **2800 Ω**
  - 1 %: fällt auf **800 Ω**
- Bei 50 V und Einwirkdauer 5 s kann die Berührung theoretisch unbegrenzt dauern (Grundlage für IEC-Kurve)

**Tab. 16.1 — Wirkungsbereiche des elektrischen Stroms (15–100 Hz) nach IEC 479-1/479-2:**

| Bereich | Physiologische Wirkung |
|---|---|
| 1 | Normalerweise keine Reaktion |
| 2 | Normalerweise keine schädlichen physiologischen Effekte |
| 3 | Kein Organschaden, aber krampfartige Muskelkontraktionen, Atemprobleme, Vorhofflimmern, vorübergehender Herzstillstand möglich |
| 4 | Ohne Herzkammerflimmern bis Kurve 2 (5 %), steigendes Risiko bis Kurve 3 (50 %), über Kurve 3 (>50 %) |

**Strombereiche und Wirkungen:**
- **0–2 mA:** Wahrnehmungsschwelle (Kribbeln); Sekundärunfälle möglich (z.B. Sturz von Leiter)
- **>10 mA:** Loslassgrenze; Muskelverkrampfung (Hängenbleiben am Strom); bei längerem Einwirken: Atemlähmung, Bewusstlosigkeit
- **25–80 mA:** Herzstillstand oder Kammerflimmern; bleibende Schädigungen; Erste-Hilfe: Atemspende + Herzmassage
- **80–5000 mA:** Kammerflimmern, Tod nach kurzer Zeit
- **>5000 mA:** Herzstillstand, thermische Schäden, innere Verbrennungen durch Lichtbogen

---

### 16.1 / 16.2 Netzsystemkennzeichnung (TN-/TT-/IT-System)

Buchstabenkennzeichnung nach DIN VDE 0100 Teil 200:

**Erster Buchstabe** — Beziehung des Versorgungssystems zur Erde:
- **T:** Direkte Erdung eines Punktes
- **I:** Alle aktiven Teile isoliert von Erde, oder ein Punkt über Impedanz geerdet

**Zweiter Buchstabe** — Beziehung der Anlagenkörper zur Erde:
- **T:** Körper direkt geerdet, unabhängig von der Versorgungserdung
- **N:** Körper direkt mit der Betriebserde verbunden

**Weitere Buchstaben** — Anordnung von Neutral- und Schutzleiter:
- **S:** Neutralleiter und Schutzleiter getrennte Leiter
- **C:** Neutral- und Schutzleiterfunktion in einem gemeinsamen Leiter (PEN)

**TN-System:** Schutzleiter PE (kombiniert mit Neutralleiter oder getrennt) verbindet alle Körper; in jedem Gebäude über Erdungsklemme mit Fundamenterder geerdet; Schutzmaßnahme unabhängig von einer externen Erdungsanlage.
