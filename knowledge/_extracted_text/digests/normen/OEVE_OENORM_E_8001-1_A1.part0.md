# OEVE_OENORM_E_8001-1_A1 — Teil 0
> Quelle: OEVE_OENORM_E_8001-1_A1 (normen) · dieser Teil.

## Dokumentkopf

- **Bezeichnung:** ÖVE/ÖNORM E 8001-1/A1
- **Ausgabe:** 2002-04-01
- **ICS:** 29.240.01
- **Normengruppe:** 330
- **Titel:** Errichtung von elektrischen Anlagen mit Nennspannungen bis 1000 V und 1500 V — Teil 1: Begriffe und Schutz gegen elektrischen Schlag (Schutzmaßnahmen) — **Änderung (Amendment A1)**
- **Ersatz für:** ÖVE/ÖNORM E 8001-1/AC:2001-02
- **Grunddokument:** ÖVE/ÖNORM E 8001-1:2000 (ist gemeinsam mit A1 anzuwenden)
- **Rechtsstatus:** Doppelstatusdokument — gleichzeitig ÖSTERREICHISCHE BESTIMMUNGEN FÜR DIE ELEKTROTECHNIK (gemäß ETG 1992) und ÖNORM (gemäß NG 1971)
- **Herausgeber:** Österreichischer Verband für Elektrotechnik (ÖVE), 1010 Wien; Österreichisches Normungsinstitut (ON), 1020 Wien
- **Fachausschuss:** FA/FNA E — Elektrische Niederspannungsanlagen

---

## Vorbemerkung

- Alle künftigen elektrotechnischen Dokumente werden als „Doppelstatusdokumente" veröffentlicht (ÖVE + ON-Vereinbarung).
- Die Reihe ÖVE-EN 1 wird zur Reihe ÖVE/ÖNORM E 8001. In der Übergangszeit können Teile beider Reihen gleichzeitig gelten.
- Bei verbindlich erklärten BESTIMMUNGEN/ÖNORMEN:
  - Verweise beziehen sich auf den Stand zum Herausgabezeitpunkt; bei Anwendung ist der durch Verordnungen zum ETG festgelegte aktuelle Stand maßgebend.
  - Informative Anhänge, Fußnoten sowie normative Verweise auf nicht-verbindliche Texte werden von der Verbindlicherklärung nicht erfasst.
- Korrekturen gemäß ÖVE/ÖNORM E 8001-1/AC:2001-02 sind eingearbeitet (am linken Rand mit einem Strich markiert).

---

## Änderungen und Ergänzungen zum Grunddokument E 8001-1:2000

### Abschnitt 2 — Normative Verweise (Ergänzungen)

Folgende Normen wurden Abschnitt 2 neu hinzugefügt:

| Norm | Titel |
|---|---|
| ÖVE/ÖNORM IEC 60884-1 | Stecker und Steckdosen für den Hausgebrauch und ähnliche Zwecke – Teil 1: Allgemeine Anforderungen |
| ÖVE/ÖNORM EN 60309 (alle Teile) | Stecker, Steckdosen und Kupplungen für industrielle Anwendungen |
| ÖVE/ÖNORM E 8049-1 | Blitzschutz baulicher Anlagen – Teil 1: Allgemeine Grundsätze |

---

### Abschnitt 3.8.3 — Zusatzschutz (neu)

**Definition:** Ergänzende Maßnahme zum Verringern der Gefahren für Personen und Nutztiere, die entstehen können, wenn der Basisschutz und/oder der Fehlerschutz nicht wirksam sind.

**Umsetzung des Zusatzschutzes** (gemäß jeweiligen Anforderungen):
1. Einbau von Fehlerstrom-Schutzeinrichtungen (RCD) mit **Nennfehlerstrom I∆N ≤ 0,03 A**
2. Zusätzlicher Potentialausgleich (nur in besonderen Fällen, siehe 15.2)

**Schutzebenen-Hierarchie (aus Bild 3-13):**

| Ebene | Bezeichnung | Maßnahme |
|---|---|---|
| 1 | Basisschutz | Schutz gegen direktes Berühren aktiver Teile |
| 2 | Fehlerschutz | Schutz bei Isolationsfehler (Fehler nicht erkennbar) |
| 3 | Zusatzschutz | RCD I∆N ≤ 0,03 A; zusätzlicher Potentialausgleich¹ |

¹ Nur in besonderen Fällen (siehe 15.2)

---

### Abschnitt 6.1.1 — Steckdosenstromkreise: RCD-Pflicht (neu)

**Verpflichtender Zusatzschutz durch RCD (I∆N ≤ 0,03 A) für:**

- Stromkreise in Wechselspannungsanlagen mit **Steckdosen für den Hausgebrauch und ähnliche Zwecke** gemäß ÖVE/ÖNORM IEC 60884-1:
  - bis **16 A Bemessungsstrom**
  - **250 V bis 440 V Bemessungsspannung**
- Stromkreise mit **genormten Steckdosen für industrielle Anwendungen** gemäß ÖVE/ÖNORM EN 60309:
  - bis **16 A Nennstrom**
  - Nennbetriebsspannung **200 V bis 250 V** und **380 V bis 480 V**

**Gilt bei Anwendung folgender Fehlerschutz-Maßnahmen:**
- Schutzerdung
- Nullung
- Fehlerstrom-Schutzschaltung

> **ANMERKUNG:** Bei Anwendung der Maßnahme „Fehlerstrom-Schutzschaltung" sind **zwei Fehlerstrom-Schutzschalter in Serie** einzubauen.

**Empfehlung** (nicht Pflicht): Für Stromkreise mit Steckdosen **über 16 A Nennstrom** wird Zusatzschutz durch RCD mit I∆N ≤ 0,03 A empfohlen.

**Verweis:** Weitere verpflichtende Anwendungen des Zusatzschutzes durch RCD I∆N ≤ 0,03 A: ÖVE-EN 1 Teil 4 bzw. ÖVE/ÖNORM E 8001-4 (jeweilige Paragraphen/Hauptabschnitte).

---

### Abschnitt 6.2 — Zusatzschutz durch zusätzlichen Potentialausgleich (neu)

Verweist auf Abschnitt 15.2.

---

### Abschnitt 12.2.5 — Fehlerkorrektur

**Korrekte Fassung:**
> Eine Fehlerstrom-Schutzeinrichtung darf **nicht gleichzeitig** für den Fehlerschutz und den Zusatzschutz verwendet werden.

---

### Bilder 15-1 und 15-2 — Erläuterung Punkt 4 (neu)

**Punkt 4 lautet:**
> Schutzerdungsleiter der Hauptleitung (PE-Leiter) — entfällt bei Weiterführung des PEN-Leiters, z.B. zu einem Unterverteiler.

---

### Abschnitt 15.2 — Zusätzlicher Potentialausgleich (neu)

**Grundregel:**
- Ein örtlicher zusätzlicher Potentialausgleich ist **zusätzlich zum Hauptpotentialausgleich** (gemäß 15.1) zu errichten, wenn:
  - besondere Gefährdung vorliegt (z.B. Netzspannung höher als 230 V gegen Erde, erschwerte Umgebungsbedingungen, Beeinflussung), **oder**
  - in den jeweiligen technischen Bestimmungen gefordert.

**Empfehlung für mehrstöckige Gebäude:**
- In Gebäuden mit vernetzten Einrichtungen der Informationstechnik wird ein zusätzlicher Potentialausgleich an der **Hauptverteilung jedes Stockwerkes** empfohlen (Ziel: Potentialunterschiede am Schutzerdungsleiter minimieren).

#### 15.2.1 — Einzubeziehende Teile

In den zusätzlichen Potentialausgleich müssen einbezogen werden:
- Alle gleichzeitig berührbaren leitfähigen Teile **ortsfester Betriebsmittel der Schutzklasse I**
- **Schutzerdungsleiteranschlüsse**
- Alle **fremden leitfähigen Teile**
- **Bewehrung der Stahlbetonkonstruktion** von Gebäuden (soweit durchführbar)

#### 15.2.2 — Ausführung

- Zusätzlicher Potentialausgleich muss mit einem **Potentialausgleichsleiter** gemäß **21.5 (Tabelle 21-3-2)** ausgeführt werden.

---

### Abschnitt 18.1 — Transiente Überspannungen: Allgemeines (neu)

**Arten transienter Überspannungen** (im Rahmen dieses Abschnittes):
- **Leitungsgebundene (indirekte) Blitzeinwirkungen** — über das NS-Verteilungsnetz in die Verbraucheranlage gelangende Einwirkungen
- **Direkte Blitzeinwirkungen** — ergänzende Maßnahmen gemäß ÖVE-E 49 bzw. ÖVE/ÖNORM E 8049-1 erforderlich
- Entstehung auch durch **Schaltvorgänge**

> Abschnitt 18 sichert **Schutz gegen indirekte Blitzeinwirkungen**. Direkte Blitzeinwirkungen → separate Maßnahmen gemäß ÖVE-E 49 / E 8049-1.

**Geltungsbereich:** Wechselspannungsanlagen (sinngemäß auch für Gleichspannungsanlagen).

---

### Abschnitt 18.2 — Hauptpotentialausgleich und zusätzlicher Potentialausgleich (neu)

Verweis auf Abschnitt 15.

---

### Abschnitt 18.3.1 (2) — Bemessungsspannung von Überspannungs-Schutzeinrichtungen (neu)

Mindest-Bemessungsspannung der Überspannungs-Schutzeinrichtungen:

| Netzform | Anforderung |
|---|---|
| TN-C-System | ≥ 1,45-fache Leiter-Erde-Spannung |
| TN-S / TT-System, Installation gemäß (1) a) | ≥ 1,1-fache Leiter-Erde-Spannung |
| TN-S / TT-System, Installation gemäß (1) b) — Außenleiter | ≥ 1,45-fache Leiter-Erde-Spannung |
| TN-S / TT-System, Installation gemäß (1) b) — N-PE-Ableiter | ≥ 1,1-fache Leiter-Erde-Spannung |
| IT-System | ≥ 1,1-fache Außenleiterspannung |

---

### Abschnitt 18.3.1.2 — Gemischte Kabel- und Freileitungsnetze (neu)

#### 18.3.1.2.1 — Netze mit geringer Ausdehnung des Kabelabschnittes

- Mindestens Überspannungs-Schutzeinrichtungen:
  - **Ableiterklasse A** (Freileitung) oder **C** (Kabelverteiler)
  - bzw. **Prüfklasse II** gemäß ÖVE-SN 60 / IEC 61643-1
- **Abstände der Einbaustellen** in Freileitungsabschnitten:
  - Normalgebiet: im Mittel **≤ 1000 m**
  - Gebiete mit **erhöhter oder hoher Blitzdichte** (siehe Anhang A): im Mittel **≤ 500 m**
- Innerhalb Kabelabschnitte: Einbau empfohlen (nicht Pflicht)
- **Transformatorstationen** und **Übergänge Freileitung–Kabel** sind zusätzlich zu schützen.

#### 18.3.1.2.2 — Andere Netze in Gebieten mit erhöhter oder hoher Blitzdichte

- Mindestens Ableiterklasse A (Freileitung) oder C (Kabelverteiler) bzw. Prüfklasse II (ÖVE-SN 60 / IEC 61643-1)
- Abstände der Einbaustellen in Freileitungsabschnitten: im Mittel **≤ 500 m**
- Innerhalb Kabelabschnitte: Einbau empfohlen
- Transformatorstationen und Übergänge Freileitung–Kabel zusätzlich zu schützen.

---

### Abschnitt 18.3.1.3.1 — Kabelnetze (neu)

**Kabelnetze mit geringer Ausdehnung (Gesamtlänge < 500 m) und Kabelnetze in Gebieten geringer Bodenleitfähigkeit:**

In Gebieten mit erhöhter oder hoher Blitzdichte (Anhang A):
- Mindestens Ableiterklasse **C** bzw. **Prüfklasse II** gemäß ÖVE-SN 60 Teil 4 / IEC 61643-1
- Innerhalb Kabelabschnitte: Einbau empfohlen
- Transformatorstationen sind gegen Überspannung zu schützen.

---

### Abschnitt 18.3.2 — Mindestanforderungen an Verbraucheranlagen (erster Absatz, neu)

- Die Bestimmungen dieses Abschnittes sind als **Mindestanforderungen** zu betrachten.
- Abhängig von zu schützenden Anlagen/Geräten und anderen Einflussfaktoren kann die Installation von Überspannungs-Schutzeinrichtungen auch für nicht genannte Anlagen sinnvoll oder notwendig sein.
- Anforderungen gelten soweit anwendbar unverändert, sonst sinngemäß.

#### 18.3.2 (2) — Mindestanforderungen (neu)

Überspannungs-Schutzeinrichtungen müssen entsprechen:
- **Ableiterklasse C** bzw. **Prüfklasse II** gemäß ÖVE-SN 60 Teil 4 / IEC 61643-1
- **Nennableitstoßstrom ≥ 5 kA (8/20 µs)**
- **Schutzpegel** gemäß Tabelle 18-1:

**Tabelle 18-1 — Maximaler Schutzpegel**

| Nennspannung der Verbraucheranlage | Außenleiter-Neutralleiter-Spannung (AC oder DC) | Maximaler Schutzpegel |
|---|---|---|
| — | bis 50 V | 500 V |
| — | über 50 bis 100 V | 800 V |
| — | über 100 bis 150 V | 1500 V |
| **230/400 V** | **über 150 bis 300 V** | **2500 V** |
| **400/690 V** | über 300 bis 600 V | 4000 V |
| **1000 V** | über 600 bis 1000 V | 6000 V |

> **ANMERKUNG:** Korrektur: Maximaler Schutzpegel für **230/400 V-Netze** wurde von 2000 V (Basis ÖVE-SN 60) auf **2500 V** angehoben (angelehnt an IEC 60664-1 und aktuelle Entwürfe IEC TC 64).

#### 18.3.2 (3) — Ableiter zwischen Neutralleiter und Haupterdungsschiene (neu)

Bei Installation gemäß 18.3.2.1 (1) b), 18.3.2.2 (1) b) oder 18.3.2.3 (1) b):

| Anlagentyp | Mindest-Nennableitstoßstrom (N–PAS oder PE-Schiene) |
|---|---|
| **Einphasige** Verbraucheranlage | **≥ 10 kA (8/20 µs)** |
| **Dreiphasige** Verbraucheranlage | **≥ 20 kA (8/20 µs)** |

> **ANMERKUNG:** Diese Mindestanforderung (10 kA / 20 kA) bleibt unverändert, auch wenn Ableiter zwischen Außenleitern und Neutralleiter mit höheren Nennableitstoßströmen (z.B. 15 kA) eingesetzt werden.

---

### Abschnitt 18.3.2.1 (2) — TN-S-System: Bemessungsspannung (neu)

Überspannungs-Schutzeinrichtungen müssen:
- Für **alle Außenleiter**: Bemessungsspannung ≥ **1,45-fache Leiter-Erde-Spannung**
- Für Ableiter **zwischen Neutralleiter und PE-Leiter** (falls erforderlich): Bemessungsspannung ≥ **1,1-fache Leiter-Erde-Spannung**

---

### Abschnitt 18.3.2.2 (3) — TT-System: Ableitertrennschalter (neu)

**Bedingung für Verzicht auf Ableitertrennschalter:**

```
RA ≤ UFL / IA
```

- RA = Erdungswiderstand des Anlagenerders
- UFL = vereinbarter Grenzwert der Fehlerspannung
- IA = Ausschaltstrom der vorgeschalteten oder im Ableiter integrierten Überstrom-Schutzeinrichtung

**Wenn Bedingung NICHT erfüllt:**
- Ableitertrennschalter in Zuleitungen oder Erdungsleitung einbauen (Bild 18-5), **oder**
- Überspannungs-Schutzeinrichtungen gemäß (1) b) installieren (Bild 18-6)

**Mindest-Stoßstromfestigkeit des Ableitertrennschalters:**

| Anlagentyp | Mindest-Stoßstromfestigkeit |
|---|---|
| Einphasige Verbraucheranlage | **≥ 10 kA (8/20 µs)** |
| Dreiphasige Verbraucheranlage | **≥ 20 kA (8/20 µs)** |

> **ANMERKUNG:** Mindestanforderung (10 kA / 20 kA) bleibt unverändert, auch bei Ableitern mit höheren Nennableitstoßströmen (z.B. 15 kA). Bei Stoßströmen über der Stoßstromfestigkeit des Ableitertrennschalters kann es zu Fehlauslösungen kommen.

**Erdungswiderstand RA muss erfüllen:**

```
RA ≤ UFL / IFN
```

- IFN = Auslösenennstrom des Ableitertrennschalters

> **ANMERKUNG:** Eingebaute Abtrennvorrichtungen der Ableiter sind nur Überlastungs-/Überhitzungsschutz für den Fall, dass der Ableiter leitend wird. Bei Einhaltung der RA-Bedingungen gemäß 12.2 (Fehlerstrom-Schutzschaltung) können unzulässig hohe Berührungsspannungen vermieden werden.

**Installationsregeln für Ableiter nach Fehlerstrom-Schutzeinrichtungen:**

- **Ableiterklasse B / Prüfklasse I** nach FI-Schutzeinrichtung: **NICHT zulässig**, außer Überspannungen sind von der Lastseite der FI-Einrichtung zu erwarten.
- **Ableiterklasse C / Prüfklasse II** nach FI-Schutzeinrichtung: **Nur zulässig**, wenn:
  - vor der FI-Einrichtung bereits Ableiter gemäß 18.3.2 (2)/(3) installiert sind, **oder**
  - Überspannungen von der Lastseite der FI-Einrichtung zu erwarten sind (Bild 18-7).
  - In solchen Fällen: **FI-Schutzschalter der Bauart S oder Bauart G** zu installieren.

---

### Abschnitt 20.0 — Erdung: Allgemeines (neu hinzugekommen)

**Fundamenterder-Pflicht:**

> Bei **neu zu errichtenden Gebäuden**, in denen elektrische Anlagen errichtet werden sollen, ist — wenn sie mit geeigneten erdfühligen Fundamenten ausgeführt werden — ein **Fundamenterder** gemäß **ÖNORM E 2790** zu verlegen.

---

## Referenzierte Normen und Standards (Gesamtübersicht)

| Norm | Inhalt |
|---|---|
| ÖVE/ÖNORM E 8001-1:2000 | Grunddokument (gemeinsam mit A1 anzuwenden) |
| ÖVE/ÖNORM E 8001-1/AC:2001-02 | Corrigendum (eingearbeitet) |
| ÖVE/ÖNORM IEC 60884-1 | Stecker/Steckdosen Hausgebrauch |
| ÖVE/ÖNORM EN 60309 (alle Teile) | Stecker/Steckdosen industrielle Anwendungen |
| ÖVE/ÖNORM E 8049-1 | Blitzschutz baulicher Anlagen — Teil 1 |
| ÖVE-E 49 | Blitzschutz (ältere Bezeichnung) |
| ÖVE-EN 1 Teil 4 / ÖVE/ÖNORM E 8001-4 | Besondere Anlagen (weitere RCD-Pflichten) |
| ÖVE-SN 60 / ÖVE-SN 60 Teil 4 | Überspannungs-Schutzeinrichtungen |
| IEC 61643-1 | Überspannungs-Schutzeinrichtungen |
| IEC 60664-1 | Isolationskoordination |
| ÖNORM E 2790 | Fundamenterder |
| ETG 1992 | Elektrotechnikgesetz |
| NG 1971 | Normungsgrundsätze |
