# Fachinfo_IS-03_Anwendung_AFDD_2023-12 — Teil 0
> Quelle: Fachinfo_IS-03_Anwendung_AFDD_2023-12 (normen) · dieser Teil.

## Metadaten

- **Dokument:** OVE-Fachinformation IS03
- **Ausgabe:** 2023-12-01
- **Seiten:** 8
- **Zuständiges Komitee:** OVE/TSK IS23E – Schutzschalter
- **ICS-Nummern:** 13.260; 29.020; 29.100; 29.120; 29.120.50; 29.130; 91.140.50
- **Ersatz für:** – (kein Vorgängerdokument angegeben)
- **Herausgeber:** OVE Österreichischer Verband für Elektrotechnik, Eschenbachgasse 9, A-1010 Wien

---

## 1 Ausgangssituation

Zweck: Vermittlung der grundlegenden Funktion und charakteristischen Eigenschaften von **Fehlerlichtbogen-Schutzeinrichtungen AFDD** (en: Arc Fault Detection Device) gemäß Produktnorm **OVE EN 62606**; Überblick über die Anwendung gemäß den anerkannten Regeln der Technik, insbesondere **OVE E 8101**.

Rechtliche Grundlage: **Österreichisches Elektrotechnikgesetz 1992 – ETG 1992** (BGBl. Nr. 106/1993): Elektrische Anlagen und Betriebsmittel sind so zu errichten, herzustellen, instand zu halten und zu betreiben, dass Betriebssicherheit, Sicherheit von Personen und Sachen sowie ungestörter und sicherer Betrieb anderer Anlagen gewährleistet sind.

**Statistik:** Brandschadenstatistik der österreichischen Brandverhütungsstellen 2021:
- Zündquelle „Elektrische Energie": **1 313 Brände**
- Schadenssumme: **über 90 Millionen Euro**
- Elektrische Energie zählt damit zu den häufigsten Brandursachen

---

## 2 Grundlagen

### 2.1 Einleitung

- Brände durch elektrische Anlagen können ihren Ursprung in **Fehlerlichtbögen** haben.
- **Parallele und serielle Lichtbögen** entstehen durch fehlerhafte Isolierung aktiver Leiter oder durch lose elektrische Verbindungen.

**Warum RCD und OCPD allein nicht ausreichen:**

| Fehlerart | RCD (RCCB) | OCPD (Leitungsschutzschalter/Sicherung) |
|-----------|-----------|----------------------------------------|
| Serieller Lichtbogen | Kein Ableitstrom zur Erde → RCD erkennt nicht | Impedanz des Lichtbogens reduziert Laststrom → unter Auslösegrenzwert |
| Paralleler Lichtbogen (L–L oder L–N) | Nur bedingt wirksam | Strom durch Impedanz der Installation + Lichtbogen begrenzt → ggf. unter Auslösegrenzwert |
| Fehlerstrom-Lichtbogen gegen Erde | RCD mit IΔn ≤ 300 mA kann wirksam sein, aber: Frequenzspektrum des Erdschlussstroms geht weit über 50/60 Hz → RCD erkennt ggf. nicht |  |

**Hinweis:** Der Effektivwert eines vom Fehlerlichtbogen verursachten Erdschlussstroms ist nicht auf die Bemessungsfrequenz 50/60 Hz begrenzt, sondern enthält ein viel höheres Frequenzspektrum, das von RCCB unter Umständen nicht erkannt wird.

### 2.2 Arten von Lichtbögen

**Definition Lichtbogen:** Elektrische Entladung zwischen zwei Elektroden, die bei entsprechender Spannung und Stromdichte durch Ionisation entsteht; Gasentladung bildet ein Plasma.

| Lichtbogenart | Beschreibung |
|---------------|-------------|
| **Betriebsbedingte Lichtbögen** | zB Schaltlichtbögen, Bürstenfeuer einer Bohrmaschine — kein Fehler |
| **Störlichtbogen (arc flash)** | Fehler in Anlagen größerer Leistung (zB Kurzschluss in Industrie-Schaltanlagen); tritt explosionsartig auf, unmittelbare Auswirkungen; Schutzsysteme löschen innerhalb **5 ms** |
| **Fehlerlichtbögen** | Fehler geringerer Leistung (zB beschädigte Isolation in Hausinstallationen oder Betriebsmitteln); können **lange unerkannt** bleiben; thermische Auswirkungen → elektrisch gezündete Brände; hierfür ist AFDD konzipiert |

### 2.3 Ursachen für elektrisch gezündete Brände

Mechanische, thermische oder chemische **Alterung von Isoliermaterial** oder Kontaminierung mit Schmutz/Feuchtigkeit → Entladungen → Erhitzung und Verkohlung von Kunststoff → stabiler Fehlerlichtbogen → Brand.

**Häufig erkannte Fehlerquellen:**

- Beschädigte Isolierungen von Kabel/Leitungen: durch Nägel, Schrauben, Bohrungen oder **Nagetierverbiss**
- Gequetschte oder abgeknickte Kabel/Leitungen: Aderbrüche bei zu engem Biegeradius oder durch Quetschen beim Schließen von Türen/Fenstern
- Hoher Kontaktübergangswiderstand: schlechte Kontaktierung, zB lose Kontaktstellen in Steckdosen oder bei Schraubverbindungen
- Nicht sachgerecht ausgeführte Kabel-/Leitungsverlegung: zB durch Krallenbefestigung beschädigte Kabel/Leitungen in Steckdosen oder Schaltern
- Schädigung/Alterung der Isolation durch Umwelteinflüsse: UV-Strahlen, Temperatur, leitende Verschmutzung zwischen aktiven Leitern
- Beschädigte Elektrogeräte

### 2.4 Lichtbogen-Fehlersituationen

Der AFDD erweitert das Schutzkonzept aus RCD + OCPD und schließt die **Schutzlücke**, insbesondere bei seriellen Fehlerlichtbögen.

**Tabelle 1 – Fehlersituationen und Funktion von Schutzschaltgeräten:**

| Fehlerlichtbogen-Art | Beschreibung | Schutzfunktion |
|---------------------|-------------|----------------|
| **Fehlerlichtbogen gegen Erde** (Phase gegen Schutzleiter) | Strom vom aktiven Leiter gegen Erde | RCD (wirksam, auch IΔn ≤ 300 mA kann Brandschutz erfüllen); OCPD (abhängig von Fehlerkreisimpedanz); AFDD |
| **Paralleler Fehlerlichtbogen** (Phase–N oder Phase–Phase) | Lichtbogenstrom fließt zwischen aktiven Leitern parallel zur Last | OCPD (nur bedingt, abhängig von Impedanz); AFDD |
| **Serieller Fehlerlichtbogen** (kleine Unterbrechung Phase oder N) | Strom fließt durch die Last(en) des Verbraucherstromkreises | **Nur AFDD** (weder OCPD noch RCD können erkennen) |

> Anmerkung: OCPD-Schutz abhängig von der Impedanz des Fehlerkreises.

**Auslöseort:** Für das Auslösen des AFDD ist es grundsätzlich unerheblich, ob die Fehlstelle in der elektrischen Anlage, der Anschlussleitung eines Betriebsmittels oder in einem mit Netzspannung betriebenen elektrischen Gerät vorliegt.

---

## 3 Funktionsweise von Fehlerlichtbogen-Schutzeinrichtungen (AFDD)

### 3.1 Charakteristische Eigenschaften eines Fehlerlichtbogens

Fehlerlichtbögen weisen folgende charakteristische Merkmale auf:
- **Hochfrequentes Rauschen**
- **Zusammenbruch des Lichtbogenstroms nahe dem Nulldurchgang der treibenden Spannung**

Detektierung: Messung von Spannungs- und Stromverlauf über die Zeit → Auswertung mittels **digitaler Signalverarbeitung**.

### 3.2 Prinzipieller Aufbau

- Strom wird über **zwei getrennte Sensoren** permanent erfasst, verstärkt, aufbereitet und in einem **Mikrocontroller** ausgewertet.
- **RSSI** (Received Signal Strength Indication): entspricht der Leistung des Lichtbogens bei einer definierten Frequenz und Bandbreite.
- Bei Erfüllung der Kriterien für einen Fehlerlichtbogen → Schalter löst aus.

### 3.3 Vermeidung unerwünschter Auslösungen und Maskierung der Schutzfunktion

- Bei betriebsbedingten Lichtbögen (zB Bürstenfeuer Bohrmaschine, Einschaltvorgang Leuchtstofflampe) **darf keine Auslösung** erfolgen.
- Verwendung **spezieller Algorithmen**: Vergleich mit vorgespeicherten Signalmustern zur Unterscheidung zwischen Fehlerlichtbögen und Betriebslichtbögen.
- Zuverlässige Auslösung muss auch bei Überlagerung durch betriebsbedingte Lichtbögen gewährleistet sein.
- Nachweis durch **Maskierungstests** bei Typenprüfungen nach **OVE EN 62606**.
- **Kabel-/Leitungslänge** des zu schützenden Stromkreises ist zu beachten, da die Signatur eines Lichtbogens mit zunehmender Entfernung gedämpft wird.

### 3.4 Grenzwerte der Betriebskriterien gemäß OVE EN 62606

**Tabelle 2 – Grenzwerte von AFDD bei niedrigen Lichtbogenströmen bis 63 A (Serielle Lichtbögen):**

| Prüflichtbogenstrom (Effektivwert) | Höchstzulässige Ausschaltzeit |
|-----------------------------------|------------------------------|
| 2,5 A | 1 s |
| 5 A | 0,5 s |
| 10 A | 0,25 s |
| 16 A | 0,15 s |
| 32 A | 0,12 s |
| 63 A | 0,12 s |

**Tabelle 3 – Grenzwerte von AFDD bei hohen Lichtbogenströmen über 63 A (Parallele Lichtbögen):**

| Prüflichtbogenstrom (Effektivwert)^a | N (Anzahl Halbperioden bei Bemessungsfrequenz)^b |
|--------------------------------------|--------------------------------------------------|
| 75 A | 12 |
| 100 A | 10 |
| 150 A | 8 |
| 200 A | 8 |
| 300 A | 8 |
| 500 A | 8 |

> ^a Prüfstrom = unbeeinflusster Strom vor der Lichtbogenbildung im Prüfkreis.
> ^b N = Anzahl der Halbperioden bei Bemessungsfrequenz.

### 3.5 Prüffunktion

- Vorgesehen sein muss: **händisch betätigbare Prüftaste** und/oder **automatische Prüffunktion**.
- **Händische Prüfung:** AFDD muss auslösen.
- **Automatische Prüfung:** bei jedem Einschalten und in Intervallen von **mindestens einmal täglich**; AFDD muss dabei **nicht** abschalten, außer bei Vorliegen eines Fehlers.
- Derzeit **keine Vorgaben** für periodische Funktionsprüfung durch externe Prüfgeräte.
- Handelsübliche Installationsprüfgeräte erfüllen diese Testfunktion derzeit **nicht**.

### 3.6 Überspannungen

- Bei Unterbrechung des Neutralleiters in einer Drehstromanlage kann eine Außenleiter-Neutralleiter-Überspannung auftreten (Höchstwert = Spannung zwischen Außenleitern).
- Folge: außergewöhnliche Erwärmung von Lasten → Brandgefahr.
- AFDD können Vorrichtungen enthalten, die **zB bei U > 270 V** abschalten.

### 3.7 Bedienbarkeit, Trennfunktion, Netzsysteme

- AFDD gemäß OVE EN 62606 dürfen von **elektrotechnischen Laien (BA1)** betätigt werden.
- **Keine Instandhaltung** erforderlich.
- In Ausschaltstellung: erfüllen Anforderungen für **sichere Trennung**.
- Geeignet für: **TN-, TT- und IT-Systeme**.

### 3.8 Einsatzbedingungen

- **Verschmutzungsgrad 2**: normalerweise keine leitfähige Verschmutzung; gelegentlich vorübergehende Leitfähigkeit durch Betauung.

**Tabelle 4 – Normbedingungen für den Betrieb:**

| Einflussgröße | Normbereich der Anwendung | Bezugswert | Prüfabweichungen |
|--------------|--------------------------|-----------|-----------------|
| Umgebungstemperatur | –5 °C bis +40 °C (max. mittl. Tagestemperatur +35 °C) | 20 °C | ±5 °C |
| Höhenlage | Nicht über 2 000 m | – | – |
| Relative Feuchte (Höchstwert bei 40 °C) | 50 % (höhere Werte bei niedrigen Temp. zulässig, zB 90 % bei 20 °C) | – | – |
| Äußeres Magnetfeld | Nicht über dem 5-fachen Erdmagnetfeld in jeder Richtung | Erdmagnetfeld | – |
| Lage | Wie vom Hersteller angegeben, mit Abweichung von 2° in jeder Richtung | Wie vom Hersteller angegeben | 2° in jeder Richtung |
| Frequenz | Bezugswert ±5 % | Bemessungswert | ±2 % |
| Verzerrung der Sinusform | Nicht über 5 % | Null | 5 % |

> Lagerung und Transport: Höchstgrenzen –20 °C bis +60 °C zulässig (bei Konstruktion berücksichtigen).
> Härtere klimatische Bedingungen: Werte außerhalb des Normbereichs nach Vereinbarung Hersteller–Anwender zulässig.

### 3.9 Bauformen

| Bauform | Beschreibung |
|---------|-------------|
| **a) AFD-Einheit + Ausschaltvorrichtung** | Kein integrierter Überstrom- oder Fehlerstromschutz; Anschluss in Reihe mit geeigneten Schutzeinrichtungen |
| **b) AFD-Einheit integriert in Schutzschaltgerät** | Entsprechend einer oder mehreren der Normen: OVE EN 60898-1, OVE EN 61008-1, OVE EN 61009-1 oder OVE EN 62423 |
| **c) AFD-Einheit + angegebene Schutzeinrichtung** | zB Leitungsschutzschalter oder Fehlerstromschutzschalter; vor Ort zusammenzubauen |

---

## 4 Anwendung von Fehlerlichtbogen-Schutzeinrichtungen

### 4.1 Schutz gegen die Auswirkungen von Fehlerlichtbögen

Rechtsgrundlage: **OVE E 8101, Unterabschnitt 421.7** – besondere Maßnahmen zum Schutz gegen Auswirkungen von Lichtbögen in einzelnen Endstromkreisen.

**Geltungsbereich:** Wechselstromkreise mit einem **Nennstrom nicht größer als 16 A**.

#### a) AFDD-Installation VORGESCHRIEBEN in:
- **Schlafräumen** von Heimen für behinderte oder alte Menschen (zB Senioren- oder Pensionistenheime) oder Schlafräumen von **Kindergärten**
- **Räumen oder Orten mit einem Brandrisiko** durch verarbeitete oder gelagerte Materialien, zB **BE2** gemäß OVE E 8101 Teil 5-51

#### b) AFDD EMPFOHLEN in:
- **Schlafräumen in Wohngebäuden** (insbesondere bei Nutzung durch in ihrer Mobilität dauerhaft eingeschränkten Personen infolge körperlicher oder geistiger Behinderung)
- **Räumen oder Orten mit Gefährdung unersetzbarer Güter**

**Installationsanforderungen bei Verwendung von AFDD:**
- Müssen den Anforderungen von **OVE EN 62606** entsprechen.
- Müssen **am Anfang des zu schützenden Stromkreises** installiert werden.
- **Installationshinweise des Herstellers** sind zu beachten (zB maximale Leitungslänge).
- Der Einsatz eines AFDD **schließt weitere Maßnahmen** gemäß **OVE E 8101 Teil 4-42** nicht aus.

### 4.2 Installationsbeispiel

Bild 2 zeigt ein Installationsbeispiel für AFDD (Bild im Originaldokument, nicht als Text extrahierbar).

---

## Literaturhinweise

| Dokument | Titel |
|----------|-------|
| **OVE E 8101** | Elektrische Niederspannungsanlagen |
| **OVE EN 60898-1** | Leitungsschutzschalter für Hausinstallationen und ähnliche Zwecke – Teil 1: Leitungsschutzschalter für Wechselstrom (AC) |
| **OVE EN 62606** | Allgemeine Anforderungen an Fehlerlichtbogen-Schutzeinrichtungen |
| **OVE EN 61008-1** | Fehlerstrom-/Differenzstrom-Schutzschalter mit eingebautem Überstromschutz (RCCBs) – Teil 1: Allgemeine Anforderungen |
| **OVE EN 61009-1** | Fehlerstrom-/Differenzstrom-Schutzschalter ohne eingebauten Überstromschutz (RCBOs) – Teil 1: Allgemeine Anforderungen |
| **OVE EN 62423** | Fehlerstrom-/Differenzstrom-Schutzschalter Typ F und Typ B mit und ohne eingebautem Überstromschutz |
| **BGBl. Nr. 106/1993** | Elektrotechnikgesetz 1992 – ETG 1992 |

**Weblinks:**
- Brandschadenstatistik: https://brandverhuetung-oesterreich.at/brandstatistik/

---

## Schlüssel-Kennwerte auf einen Blick

| Parameter | Wert |
|-----------|------|
| Nennstrom-Obergrenze (AFDD-Pflicht-/Empfehlungsbereich) | ≤ 16 A (Wechselstrom) |
| Auslösegrenze bei 2,5 A seriellem Lichtbogen | 1 s |
| Auslösegrenze ab 32 A seriellem Lichtbogen | 0,12 s |
| Paralleler Lichtbogen 75 A: Halbperioden N | 12 |
| Störlichtbogen-Löschzeit (Industrie) | ≤ 5 ms |
| Überspannungsabschaltung (optional) | bei U > 270 V |
| Umgebungstemperatur Betrieb | –5 °C bis +40 °C |
| Umgebungstemperatur Lagerung/Transport | –20 °C bis +60 °C |
| Höhenlage max. | 2 000 m |
| Verschmutzungsgrad | 2 |
| Netzsysteme | TN, TT, IT |
| Bedienbarkeit | BA1 (elektrotechnische Laien) |
| Automatische Selbstprüfintervall | mindestens einmal täglich |
