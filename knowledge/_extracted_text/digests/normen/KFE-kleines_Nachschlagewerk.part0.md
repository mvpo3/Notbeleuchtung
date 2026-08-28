# KFE-kleines_Nachschlagewerk — Teil 0
> Quelle: KFE-kleines_Nachschlagewerk (normen) · Seiten 1-2.

Das "kleine Nachschlagewerk" ist eine kompakte Tabellen- und Formelsammlung des Kuratoriums für Elektrotechnik (KFE) für die elektrotechnische Praxis nach OVE E 8101. Dieser Teil (Seiten 1-2 = vollständiges Dokument) deckt Niederohmigkeit, Nullung (ZSmax-Tabellen, Ausschaltbedingungen, Ausschaltfaktoren), Fehlerstrom-Schutzschalter, Isolationswiderstand, IP-Schutzarten, Tiefenerder und Spannungsabfall ab.

**Herausgeber:** Kuratorium für Elektrotechnik (KFE), 1220 Wien, Rautenweg 15  
**Stand:** Empfehlung ET: 06.2023  
**Hinweis:** Meinungen und Interpretationen durch KFE; die Elektrofachkraft entscheidet über die Anwendung der zutreffenden Normen. Irrtümer, Satz- und Druckfehler vorbehalten.

## Inhalt

### 1. Niederohmigkeit von Leitern (Widerstandsberechnung)

**Vereinfachte Berechnung von Widerständen zum Nachweis der Niederohmigkeit (RLO):**  
Der Wert ist normativ nicht festgelegt; es sollte annähernd der zu erwartende Wert erreicht werden.

**Formelzeichen:**
- R = Widerstand [Ω]
- l = Länge [m]
- κ = Leitfähigkeit (Kupfer: 57, Aluminium: 35,4)
- A = Querschnitt [mm²]

### 1.1 Einfacher Leitungsweg (z. B. für den Potentialausgleich)

```
R = l / (κ × A)
```

### 1.2 Doppelter Leitungsweg (z. B. für ZS / ZI)

```
R = (2 × l) / (κ × A)
```

**Rechenbeispiel:** 50 m Yf 10 mm² → ca. 0,0877 Ω

---

### 2. Nullung — Maximale Schleifenimpedanz ZS (mit 2/3-Regel)

### 2.1 Endstromkreise bis 32 A

| Schutzeinrichtung | Maximaler ZS [Ω] |
|---|---|
| LS 6 A / Charakteristik B | 5,11 |
| LS 10 A / B | 3,07 |
| LS 13 A / B | 2,36 |
| LS 16 A / B | 1,92 |
| LS 6 A / Charakteristik C | 2,56 |
| LS 10 A / C | 1,53 |
| LS 13 A / C | 1,18 |
| LS 16 A / C | 0,96 |
| LS 20 A / C | 0,76 |
| LS 32 A / C | 0,48 |
| gG 13 A | 1,18 |
| gG 16 A | 0,96 |
| gG 20 A | 0,76 |
| gG 25 A | 0,61 |
| gG 32 A | 0,48 |

### 2.2 Endstromkreise über 32 A / Verteilungsstromkreise

| Schutzeinrichtung | Maximaler ZS [Ω] |
|---|---|
| gG 6 A | 7,30 |
| gG 10 A | 4,38 |
| gG 13 A | 3,36 |
| gG 16 A | 2,73 |
| gG 20 A | 2,19 |
| gG 25 A | 1,75 |
| gG 32 A | 1,36 |
| gG 35 A | 1,25 |
| gG 40 A | 1,09 |
| gG 50 A | 0,87 |
| gG 63 A | 0,69 |
| gG 80 A | 0,54 |
| gG 100 A | 0,43 |
| gG 125 A | 0,35 |

**Berechnungsgrundlage:**

```
Zsmax = (U0 × 2) / (IA × 3)
```

---

### 3. Nullung — Ausschaltbedingungen und Ausschaltfaktoren

### 3.1 Grundlegende Auslösezeitanforderungen

- **Endstromkreise mit Nennstrom ≤ 32 A:** max. **0,4 Sekunden**
- **Verteilungsleitungen in Verbraucheranlagen und Endstromkreise mit Nennstrom > 32 A:** max. **5 Sekunden**

### 3.2 Ausschaltfaktoren „m"

Quelle: OVE E 8101-4-41-411.4.4.003.AT Tabelle 41.002.AT

| Art der Überstromschutzeinrichtung | Endstromkreise mit Nennstrom ≤ 32 A | Verteilungsleitungen und Endstromkreise mit Nennstrom > 32 A |
|---|---|---|
| Schmelzsicherungen bis 125 A (gG) | 10 | 3,5 |
| Leitungsschutzschalter B | 5 | 3,5 |
| Leitungsschutzschalter C | 10 | 3,5 |
| Leitungsschutzschalter D | 20 | 3,5 |

### 3.3 Definitionen

- **Verteilungsstromkreis:** Stromkreis, der einen oder mehrere Verteiler versorgt.
- **Endstromkreis:** Stromkreis, der dafür vorgesehen ist, elektrische Verbrauchsmittel oder Steckdosen unmittelbar mit Strom zu versorgen.

---

### 4. Fehlerstrom-Schutzschalter (RCD)

### 4.1 Auslösezeiten nach Bauart

| Bauart | Auslösezeit [ms] | Stromart | Bereich % von IΔN |
|---|---|---|---|
| Standard | 0–300 | AC | 50 bis 100 |
| G (verzögert) | 10–300 | A 0 Grad | 35 bis 140 |
| S (selektiv) | 40–500 | B | 50 bis 200 |

### 4.2 Fehlerstrom-Schutzschaltung im TT-System

- **Höchstzulässige Auslösezeit:** **200 ms**
- **Zulässige Schleifenimpedanz ZS** — der jeweils **kleinere** der folgenden Werte ist anzuwenden:
  - `Zsmax ≤ 100 Ω`
  - `Zsmax ≤ U0 / (5 × IΔN)`

---

### 5. Isolationswiderstand

Quelle: OVE E 8101-6-600.4.3.3 Tabelle 6.1

| Nennspannung der Stromkreise [V] | Prüfspannung DC [V] | Isolationswiderstand [MΩ] |
|---|---|---|
| SELV und PELV | 250 | ≥ 0,5 |
| bis einschließlich 500 V sowie FELV | 500 | ≥ 1,0 |
| über 500 V | 1000 | ≥ 1,0 |

**Achtung:** Bei Überspannungsableitern kann eine Reduktion der Prüfspannung erforderlich sein.

---

### 6. Schutzarten (IP-Code) nach ÖVE/ÖNORM EN 60529

### 6.1 Erste Kennziffer — Schutz gegen feste Fremdkörper

| Kennziffer | Schutz |
|---|---|
| X oder 0 | Keine Anforderungen |
| 1 | Schutz gegen feste Fremdkörper ≥ 50 mm und gegen Zugang mit dem Handrücken |
| 2 | Schutz gegen feste Fremdkörper ≥ 12,5 mm und gegen Zugang mit dem Finger |
| 3 | Schutz gegen feste Fremdkörper ≥ 2,5 mm und gegen Zugang mit Werkzeug |
| 4 | Schutz gegen feste Fremdkörper ≥ 1,0 mm und gegen Zugang mit Draht |
| 5 | Staubgeschützt und gegen Zugang mit Draht |
| 6 | Staubdicht und gegen Zugang mit Draht |

### 6.2 Zweite Kennziffer — Schutz gegen Wasser

| Kennziffer | Schutz |
|---|---|
| X oder 0 | Keine Anforderungen |
| 1 | Schutz gegen senkrecht fallendes Tropfwasser |
| 2 | Schutz gegen Tropfwasser, wenn das Gehäuse bis zu 15° geneigt ist |
| 3 | Schutz gegen Sprühwasser |
| 4 | Schutz gegen Spritzwasser |
| 5 | Schutz gegen Strahlwasser |
| 6 | Schutz gegen starkes Strahlwasser |
| 7 | Schutz gegen zeitweiliges Untertauchen |
| 8 | Schutz gegen dauerndes Untertauchen |
| 9 | Schutz gegen Hochdruck und hohe Strahlwassertemperatur |

### 6.3 Dritte Stelle des IP-Codes (Kennbuchstaben)

| Buchstabe | Beschreibung | Prüfsonde |
|---|---|---|
| A | Geschützt gegen Zugang mit dem Handrücken | Sonde 50 mm Durchmesser, ausreichend Abstand zu gefährlichen Teilen |
| B | Geschützt gegen Zugang mit dem Finger | Durchmesser 12 mm, Länge 80 mm, ausreichend Abstand zu gefährlichen Teilen |
| C | Geschützt gegen Zugang mit Werkzeug | Sonde 2,5 mm Durchmesser, 100 mm Länge, ausreichend Abstand |
| D | Geschützt gegen Zugang mit Draht | Sonde 1 mm Durchmesser, Länge 100 mm, ausreichend Abstand |

### 6.4 Mindestschutzarten (normative Anforderungen)

- **Verteiler:** Mindestschutzart **IP2XC** (Ausnahmen in abgeschlossenen elektrischen Betriebsstätten)
- **Betriebsmittel in Hohlwänden:** mindestens **IP30**
- Herstellerangaben bezüglich der Schutzart sind einzuhalten.

---

### 7. Tiefenerder (Vertikalerder)

**Vereinfachte Berechnung** für den zu erwartenden Widerstand eines Tiefenerders bis **10 m Länge:**

```
RA = ρE / l
```

**Formelzeichen:**
- RA = Widerstand [Ω]
- ρE = Spezifischer Bodenwiderstand [Ω·m]
- l = Länge [m]

**Hinweis:** Messergebnisse bei Erdern sind mit den erwarteten Werten zu vergleichen, die direkt mit dem spezifischen Erdwiderstand zusammenhängen.

---

### 8. Spannungsabfall

**Gesamtspannungsabfall** vom Übergabepunkt des Netzbetreibers bis zum letzten Verbrauchsgerät: begrenzt auf **4 % der Nennspannung**.

- Davon **1 %** reserviert für den Bereich von der Übergabestelle des Netzbetreibers bis zur Messeinrichtung.
- Für die Berechnung ist grundsätzlich der **Nennstrom der vorgeschalteten Überstrom-Schutzeinrichtung (IN)** heranzuziehen.
- Der Betriebsstrom (IB) wird nur in Ausnahmefällen verwendet, wenn er bekannt ist.

**Quelle:** OVE E 8101-5-52-525

### 8.1 Spannungsabfall bei einphasigem Wechselstrom

```
ΔU ≤ IN × (2 × l × cos φ) / (κ × A)
```

### 8.2 Spannungsabfall bei Drehstrom

```
ΔU ≤ IB × (√3 × l × cos φ) / (κ × A)
```

### 8.3 Spannungsabfall in Prozent

```
Δu = 100 × ΔU / U0
```

**Formelzeichen:**
- IB = Betriebsstrom
- IN = Nennstrom der vorgeschalteten Sicherung
- l = Länge [m]
- κ = Leitfähigkeit (57 Kupfer / 35,4 Aluminium)
- A = Querschnitt [mm²]
- U0 = Nennspannung [V]

### 8.4 Sonderregelungen Spannungsabfall

- Bei ausgedehnten Anlagen mit erhöhter Betriebssicherheit (z. B. Gesundheitseinrichtungen, Industrieanlagen, Tunnel, Straßenbeleuchtung mit Verkehrssicherungspflicht) kann der Betriebsstrom herangezogen werden, sofern bekannt.
- Bei **Erstprüfung nach OVE E 8101**: Beurteilung des Spannungsabfalls durch Messung oder rechnerischen Nachweis möglich.
- Bei **wiederkehrender Prüfung gemäß OVE E 8101:2019 Unterabschnitt 600.5** sowie bei Prüfung einer Bestandsanlage nach Vorgängernormen (ÖVE/ÖNORM E 8001, ÖVE-EN 1): Beurteilung des Spannungsabfalls **nicht erforderlich**, ausgenommen bei betriebsstrombeeinflussenden Änderungen.

**Weiterführende Quellen:**
- OVE-Fachinformation E10, Ausgabe: 2023-01-13
- KFE-Empfehlung ET 100-5 2023 (www.kfe.at → Medien → KFE Empfehlungen): Grenzlängen Spannungsabfall
