# f-roll-at1 — Teil 0
> Quelle: f-roll-at1 (buecher) · Seiten 1-12.

Schrack-Technik-Produktbroschüre/Preisliste zur **Jalousie- und Rollladensteuerung** (Best.-Nr. F-ROLL-AT1). Dieser Teil deckt das komplette System ab: zentrales Steuermodul, Erweiterungsmodule (Aus-/Eingang), Sensorik (Sonne/Dämmerung/Wind/Regen), Bedienelemente (Jalousietaster/-schalter, UP-Relais), Ausbaustufen, technische Daten und UVP-Preise. Kein Norm-Dokument, sondern Hersteller-Komponentenwissen für die Gebäudetechnik (Beschattung/Verschattung).

## Inhalt

### Systemüberblick / Funktionsprinzip
- Elektrisch betriebene Rollläden, Jalousien und Markisen steuerbar: einzeln, zentral oder in Gruppen; spontan, nach Zeit und über Sensoren auch helligkeits- oder witterungsabhängig.
- Steuerbar über Sensorik: Sonne, Dämmerung, Wind, Regen.
- Für eine Fassaden-Steuerung können **3 Sonnensensoren** angeschlossen werden.

### Zentralmodul EH952JRM-- (Jalousie-/Rollladenmodul, 12 Motoren)
Funktionsübersicht:
- **24 Ausgänge 230 V~** für 12 Motoren (max. **1 A** pro Motor).
- **24 Eingänge 24 V** für 12 Doppeltaster AUF/AB.
- **2 Eingänge** für Zentralsteuerung AUF/AB (Doppeltaster).
- **1 Eingang** zum Aktivieren/Deaktivieren der Sensorik (Automatik EIN/AUS) mittels separatem Schalter auf Eingang **I32** (auch direkt am Modul in der Menüführung möglich).
- **6 Eingänge für 3 Gruppen** (Doppeltaster AUF/AB).
- **3 Eingänge (24 V)** für Sensorik (Dämmerungs-, Sonnensensor und Wind/Regensensor).
- Einzelne Lokalbedienung für 12 Rollläden/Jalousien.
- Lokalbedienung von 3 Gruppen frei konfigurierbar.
- Individuelle Zeitsteuerung pro Antrieb; optionale Zeitsteuerung je Motor möglich.
- Ein Antrieb oder eine Gruppe mit mehreren Tastern ansteuerbar.
- Erweiterbar auf drei Sonnensensoren (bei Wegfall einer Gruppe).
- Zeitsteuerung deaktivierbar („Partyschaltung").
- Beleuchtete LCD-Anzeige; übersichtliches, logisches Menü zur Einstellung der Schaltzeiten mit **Tages-/Wochenprogramm** und Gruppenzugehörigkeit sowie Sensorzuweisung.
- **Spezielle Anschlussmöglichkeit für FI-Schutzschalter (Nassräume)** — befindet sich bei **L0**, rote Anschlussmöglichkeit links oben am Modul.
- Spannungsversorgung **230 V AC / 24 V DC** inkl.
- Bauform: Aufrasten auf DIN-Tragschiene, **216 mm breit (12 TE)**, IP20.
- UVP: **961,50** · Best.-Nr. EH952JRM-- · PREG 3310.

### Erweiterungsmodul Ausgang EH940JRM-- (4 Motoren)
- Aufrasten auf DIN-Tragschiene; **8 Relaisausgänge 4 A** zum Schalten von 4 Rollläden mit 230-V~-Motoren.
- 230 V AC / 1 A Motoren, inkl. Verbindungskabel **30 cm**, **72 mm breit (4 TE)**, IP20.
- UVP: **398,40** · Best.-Nr. EH940JRM-- · PREG 3310.

### Erweiterungsmodul Eingang EH94024EMR (16 Eingänge)
- Aufrasten auf DIN-Tragschiene; **16 Eingänge für 24 V DC**, davon 16 mit Rückmeldung.
- Anschluss von max. **16 Tastern**; Anschluss von max. **4 Schaltern** anstatt Tastern zulässig.
- Inkl. Verbindungskabel **30 cm**, **72 mm breit (4 TE)**, IP20.
- UVP: **256,90** · Best.-Nr. EH94024EMR · PREG 3310.

### Ausbaustufen
- **Ausbaustufe 1:** Grundmodul EH952JRM-- (12 Motoren).
- **Ausbaustufe 2:** Erweiterbar auf bis zu **20 Motoren** durch Anschluss eines Eingangsmoduls mit 16 Eingängen (EH94024EMR) und zwei Erweiterungsmodulen mit je 4 Motoren (EH940JRM--). EH952JRM-- kompakt verbunden mit EH94024EMR + zwei EH940JRM--.
  - 20 Motoren in dieser Variante ebenfalls in Gruppe und zentral schaltbar.
  - Mehrere EH952JRM-- über einen Sonnen-, Dämmerungs-, Regen- und/oder Windsensor betreibbar: das EH952JRM-- mit angeschlossenem Sensor fungiert als **Master**, die per Bus verbundenen EH952JRM-- als **Slave**.
  - Jalousien dabei nicht modulübergreifend zentral oder als Gruppe steuerbar; jedoch werden Sensorwerte über die Busverkabelung an alle Module übertragen.
- **Ausbaustufe 3:** Kombination aus Ausbaustufe 1 und 2 möglich — Busverbindung zwischen den EH952JRM-- Modulen und Verbindung vom Mastermodul zu den Erweiterungsmodulen.
  - Alle Motoren mittels Sensorik steuerbar, aber Zentral-/Gruppenschaltung funktioniert nur für jedes EH952JRM-Modul selbst, **nicht modulübergreifend** (über BUS verbundene Module nicht gemeinsam zentral/als Gruppe steuerbar, nur jedes Modul für sich).
  - Das **Mastermodul ist immer der erste Aktor „EH952JRM--", der aktiviert wird.**

### Sensorik – Dämmerungs-/Lichtsensor
**EH941LUX-- (Dämmerungs-/Lichtsensor mit Auswerteeinheit, IP44):**
- Anschluss an EH952JRM, bestehend aus Lichtsensor (IP44) und Auswerteeinheit (2 TE) für DIN-Tragschiene.
- Empfohlene Anschlussleitung **JY (ST) Y 2 x 2 x 0,8 mm**; Entfernung Lichtsensor zur Auswerteeinheit max. **100 m**; ggf. Abschirmung verwenden.
- Schwellwerteinstellungen:
  - Dämmerung: **1–200 Lux**; Schalthysterese **1,5** (fest eingestellt).
  - Sonne: **2000–200000 Lux**; Schalthysterese **0,2–0,8** (einstellbar).
- UVP: **329,70** · Best.-Nr. EH941LUX-- · PREG 3310.

**EH941LUXR- (Auswerteeinheit für Lichtsensor, Erweiterung, IP20):**
- Zusätzliche Auswerteeinheit (**2 TE**) für DIN-Tragschiene für den Dämmerungs-/Lichtsensor EH941LUX--, zur Auswertung eines weiteren Lichtwertes.
- Bis zu **10 Auswerteeinheiten** mit einem Lichtsensor betreibbar.
- UVP: **218,40** · Best.-Nr. EH941LUXR- · PREG 3310.

### Sensorik – Windsensor
**EH940WS--- (Windsensor mit Anschlusskabel, IP20, grau):**
- Anschlusskabel **4,5 m**, 2-Draht-Anschluss, max. Leitungslänge (min. **0,75 mm²**) **100 m**.
- Befestigungsrohr **Ø 12 mm**, Befestigung mittels PG-13,5-Verschraubung möglich.
- Passende Auswerteeinheit: EH940WSAE- · Passender Wandhalter: EH940WSRS-.
- UVP: **274,70** · Best.-Nr. EH940WS--- · PREG 3310.

**EH940WSAE- (Auswerteeinheit für Windsensor, IP54):**
- Zum Anschluss von 1 Windsensor EH940WS, Reiheneinbaugerät, **36 mm breit (2 TE)**.
- Versorgung **24 V DC** aus dem Jalousie-/Rollladenmodul EH952JRM--, Eigenverbrauch **10 mA**.
- In **8 Stufen** einstellbare Schaltschwelle **3…10** (entspricht etwa **3,6 m/s bis 24 m/s**).
- Einschaltzeitverzögerung ca. **10 Sek.**, Ausschaltzeitverzögerung ca. **10 Min.** nach Unterschreiten der nächstkleineren Windstärke.
- Potenzialfreier Relaisausgang, Wechsler, Schaltleistung **230 V AC, 2 A** bzw. max. **50 V DC, 0,5 A**.
- UVP: **222,50** · Best.-Nr. EH940WSAE- · PREG 3310.

### Sensorik – Regensensor
**EH940RS--- (Regensensor / Niederschlagswächter, IP54, grau):**
- Kabeleinführung mit einer **M-16-Verschraubung**, Abstand der Befestigungslöcher **50 x 70 mm**.
- Versorgung **24 V DC** (z. B. aus EH952JRM--), Eigenverbrauch **25 mA**, mit zugeschalteter Sensorflächenheizung **50 mA**.
- Sensorempfindlichkeit einstellbar, potenzialfreier Relaisausgang, Wechsler, Schaltleistung **230 V AC, 2 A** bzw. max. **50 V DC, 0,5 A**.
- Empfohlene Anschlussleitung **JY (ST) Y 2 x 2 x 0,8 mm**; Montage auf **30° geneigter Fläche** vorzunehmen.
- Passender Wandhalter: EH940WSRS-.
- UVP: **274,70** · Best.-Nr. EH940RS--- · PREG 3310.

### Wandhalterung für Sensoren
**EH94WSRS-- (Wandhalterung für Wind-/Regensensor, reinweiß):**
- Zur Aufnahme eines Windsensors EH940WS--- und eines Regensensors EH940RS--- in **30° geneigter Position**.
- Ausziehbar von **280–430 mm**.
- UVP: **178,60** · Best.-Nr. EH94WSRS-- · PREG 3310.
- (Auch als EH940WSRS- referenziert als „passender Wandhalter" zu Wind- und Regensensor.)

### Bedienelemente – Jalousietaster
**EV100027 (Jalousietaster-Einsatz, Steckklemmen):**
- Ausgestattet mit **elektrischer Verriegelung**, damit bei gleichzeitiger Betätigung der Wippen nur ein Ausgang durchschaltet.
- Nennstrom: **10 A**; Nennspannung: **250 V AC**.
- UVP: **13,29** · Best.-Nr. EV100027 · PREG 3110.
- **EV102012 (Wippe, weiß):** UVP **5,05** · PREG 3110.

### Bedienelemente – Jalousieschalter (digital)
**EV103007 (Digitaler Jalousieschalter-Einsatz, Schraubklemme):**
- Digitaler Jalousieschalter mit **Wochenprogramm** für manuelles und zeitprogrammiertes Schalten einer Jalousie/Rolllade/Markise.
- Automatische Sommer-/Winterzeitumstellung; Zufallsprogramm; **4 Betriebsbereiche pro Tag**.
- Nennspannung: **230 V AC**.
- UVP: **33,39** · Best.-Nr. EV103007 · PREG 3110.
- **EV103008 (Elektronischer Jalousieschalter-Aufsatz, weiß):** UVP **93,25** · PREG 3110.

### Bedienelemente – Jalousie-Steuerungsrelais (Unterputz)
**EV103041 (Jalousie-Steuerungsrelais UP, Schraubklemme):**
- Ermöglicht den Aufbau von **Gruppen- und Zentralsteuerungen** für Rollläden und Jalousien.
- Jede Jalousie einzeln über einen Jalousietaster ansteuerbar; zusätzlich über den Zentraleingang eine **Vorrangsteuerung** realisierbar.
- **Wichtig: Es dürfen nur Jalousietaster und keine Jalousieschalter verwendet werden!**
- Technische Daten:
  - Nennspannung **230 V AC**.
  - Max. Schaltleistung: **8 A (AC1) / 3 A (induktiv)**.
  - Abmessungen: **54 x 49 x 21 mm**.
- Durch flache Bauform (nur **21 mm**) in Standard-Unterputzdose montierbar; empfohlen jedoch Installation in tiefer Unterputzdose.
- UVP: **98,45** · Best.-Nr. EV103041 · PREG 3110.

### Preis-/Lieferhinweise (sachlich relevant)
- Best.-Nr. blau = Lagerware, üblicherweise versandbereit am Bestelltag; zusätzliche Abholverfügbarkeit in jedem Schrack Store.
- UVP = unverbindliche Schrack-Technik-Preisempfehlung in EUR exkl. MWSt.; PREG = Preisgruppe des Artikels.
- Es gelten ausschließlich die Allgemeinen Lieferbedingungen des Fachverbandes der Elektro- und Elektronikindustrie Österreichs (FEEI, www.feei.at).
- Hersteller/Vertrieb: Schrack Technik GmbH, Seybelgasse 13, 1230 Wien.
