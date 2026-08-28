# Fachinformation_Koordination_UeSchutz_Hersteller_2013_11__Koordination_von_UEberspannungs-Schutzgeraeten_verschiedener_Hersteller_ — Teil 0
> Quelle: Fachinformation_Koordination_UeSchutz_Hersteller_2013_11__Koordination_von_UEberspannungs-Schutzgeraeten_verschiedener_Hersteller_ (normen) · dieser Teil.

---

## Metadaten

| Feld | Wert |
|---|---|
| Herausgeber | OVE Österreichischer Verband für Elektrotechnik |
| Adresse | Eschenbachgasse 9, 1010 Wien |
| Kontakt | Tel.: +43 1 587 63 73 · Fax: +43 1 587 63 73-99 · ove@ove.at · www.ove.at |
| ZVR | 327279890 · ATU36808601 |
| Banken | BA-CA Kto.-Nr. 0043-28423/00 · PSK Kto.-Nr. 1.935.655 |
| Titel | Fachinformation des Österreichischen Elektrotechnischen Komitees (OEK): Koordination von Überspannungs-Schutzgeräten verschiedener Hersteller |
| Ausgearbeitet von | Technisches Komitee Blitzschutz (TK BL) und Technisches Subkomitee Überspannungsableiter für Niederspannung (TSK IS 37A) des OVE; mit Genehmigung des Ausschuss für Blitzschutz und Blitzforschung des VDE (ABB) |
| Ausgabe | November 2013 |
| Nachdruck | Nur wortgetreu und ohne Auslassung oder Zusatz |

---

## Abschnitt 1 — Problemstellung

- Bei Neuinstallationen sowie bei Änderungen oder Erweiterungen in elektrischen Installationen tritt häufig die Situation auf, dass Überspannungsschutzgeräte (SPDs) von unterschiedlichen Herstellern eingebaut werden (sollen).
- Die **Verantwortung** für die Sicherstellung der Koordination zwischen diesen SPDs liegt beim **Planer/Errichter** der Installation.

### Normative Verweise

- **ÖVE/ÖNORM E 8001-1/A2:2003, Abschnitt 18.2.2.1.3, dritter Absatz:** Hinweis auf die Notwendigkeit der Koordinierung der einzelnen SPD-Schutzstufen.
- **ÖVE/ÖNORM EN 62305-3:2008, Abschnitt 6.2.4 (letzter Absatz) und 6.2.5 (letzter Absatz):** Bei Ausführung von mehreren SPD-Schutzstufen muss die Koordinierung erfüllt werden.
- **ÖVE/ÖNORM EN 62305-3:2012, Abschnitt 6.2.4 (letzter Absatz) und 6.2.5 (letzter Absatz):** Identische Anforderung wie die 2008-Ausgabe.

### Ausgangslage

- Hersteller können Anfragen zur Koordination ohne aufwändige Untersuchungen in der Regel **nicht** beantworten.
- Bei der Vielzahl weltweiter SPD-Hersteller kann nicht erwartet werden, dass für beliebige Kombinationen die Koordination durch Versuche oder Berechnungen nachgewiesen wird.
- Die Frage genereller Aussagen zur Koordination wurde eingehend diskutiert; nachfolgende Lösungsmöglichkeiten wurden gemeinsam mit Vertretern der SPD-Hersteller erarbeitet.

---

## Abschnitt 2 — Lösungsmöglichkeiten

### Grundsätzlicher Aufbau einer gestaffelten Installation (Bild 1)

| Stufe | Lage | SPD-Typ |
|---|---|---|
| SPD1 | Unmittelbar nahe der Einspeisung | Typ 1 (Blitzstrom-Ableiter) |
| SPD2 | Haupt- oder Unterverteilung | Typ 2 (typisch) |
| SPD3 | Unterverteilung oder Steckdosenbereich | Typ 2 oder Typ 3 |

- Die einzelnen Stufen sind durch **Impedanzen (Z1, Z2)** entkoppelt.
- Realisierung der Impedanz: durch die Impedanz der zwischen den SPDs liegenden Leitung **oder** durch diskrete Impedanzen.

---

### Koordination SPD1 – SPD2

**Generelle Koordination** zwischen SPD1 und SPD2 ist **nur** bei „klassischen" Funkenstrecken als SPD1 möglich.

**Definition „klassische" Funkenstrecke:**
- SPDs **ohne** spezielle Maßnahmen zur internen Triggerung oder zur Netzfolgestrom-Begrenzung.

**Bedingung für Koordination:**
- Vorgaben des Herstellers von SPD1 werden eingehalten:
  - **Mindestentkopplung Z1**
  - **Mindest-Nennstrom In für SPD2**

**In allen anderen Fällen** (ohne spezielle Berechnungen oder Labortest) kann eine Koordination **nicht** angenommen werden:

| SPD1-Technologie | Begründung für fehlende generelle Koordination |
|---|---|
| Spannungsschaltende SPDs (außer klassische Funkenstrecken) | Technologien der einzelnen Hersteller zu unterschiedlich |
| Spannungsbegrenzende Komponenten in SPD1 (z.B. Varistoren) | Koordination extrem von diversen Parametern beider Geräte abhängig — generelle Koordination praktisch ausgeschlossen |

**Verifikationsmöglichkeiten:**
- Laborexperimente
- Berechnungen mit Netzwerkanalyse-Programmen
- Koordinationsverfahren beschrieben in: **CLC/TS 61643-12** und **ÖVE/ÖNORM EN 62305-4**

**Praxisempfehlung:** In vielen Fällen kommen Kombinationen von SPD1 und SPD2 **eines Herstellers** zum Einsatz, der Vorgaben für die richtige Installation gibt und die Koordination der SPDs garantiert.

---

### Koordination SPD2 – SPD3

**Bedingung für ordnungsgemäße Koordination:**
- Ausreichende Entkopplung Z2 zu SPD3 wird eingehalten:
  - **Typisch: 10 µH oder 10 m Leitungslänge**
- Bei Einhaltung dieser Bedingung kann von einer ordnungsgemäßen Koordination zu **beliebigen SPD3** ausgegangen werden.

**Praxissituation:** Nach einem SPD2 liegt in der Regel eine Verzweigung auf mehrere Leitungen vor → Stromaufteilung auf mehrere SPD3.

**Hauptaufgabe SPD3:**
- Nicht die Übernahme von Blitzteilströmen, sondern die **Begrenzung relativ energieschwacher Überspannungen**, die nach SPD2 in die Installation induziert werden.

---

### Elektroinstallation mit mehreren Abzweigen (Bild 2)

**Koordinationsanforderungen:**

1. **SPD1 – erstes SPD2 jedes Abzweigs:**
   - SPD1: meist Typ 1 nahe der Hauseinführung oder in der Hauptverteilung
   - SPD2: meist Typ 2, z.B. in einer Unterverteilung
   - Koordination muss zwischen SPD1 und dem **ersten** SPD2 jedes Abzweigs gegeben sein.

2. **Alle weiteren SPDs3 (Typ 2 oder Typ 3):**
   - Die **Bemessungsspannung Uc** jedes SPD3 muss **größer oder gleich** der Bemessungsspannung des vorangehenden SPDs sein.
   - Zweck: Überlastung sicher ausschließen.
   - Diese SPD3 können praxisgerecht von **unterschiedlichen Herstellern** sein.

---

## Normverweise (Zusammenfassung)

| Norm | Relevanter Abschnitt | Inhalt |
|---|---|---|
| ÖVE/ÖNORM E 8001-1/A2:2003 | 18.2.2.1.3, Abs. 3 | Notwendigkeit der Koordinierung der SPD-Schutzstufen |
| ÖVE/ÖNORM EN 62305-3:2008 | 6.2.4 (letzter Abs.) und 6.2.5 (letzter Abs.) | Koordinierungspflicht bei mehreren SPD-Schutzstufen |
| ÖVE/ÖNORM EN 62305-3:2012 | 6.2.4 (letzter Abs.) und 6.2.5 (letzter Abs.) | Koordinierungspflicht bei mehreren SPD-Schutzstufen |
| CLC/TS 61643-12 | — | Koordinationsverfahren für SPDs |
| ÖVE/ÖNORM EN 62305-4 | — | Koordinationsverfahren für SPDs |

---

## Schlüsseldaten / Normative Kennwerte

| Parameter | Wert | Kontext |
|---|---|---|
| Mindestentkopplung Z2 (SPD2–SPD3) | 10 µH **oder** 10 m Leitungslänge | Bedingung für freie Herstellerwahl bei SPD3 |
| Bemessungsspannung Uc SPD3 | ≥ Uc des vorangehenden SPD | Schutz vor Überlastung in Mehrfachabzweig-Installation |
| Koordination SPD1–SPD2 (klassische Funkenstrecke) | Vorgaben Hersteller (Z1_min, In_min für SPD2) | Einzige generell koordinierbare Konstellation ohne Labortest |
