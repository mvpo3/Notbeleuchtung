# Erlaeuterungen_zu_OEVEOENORM__E_8001-1A42009-04-01 — Teil 0
> Quelle: Erlaeuterungen_zu_OEVEOENORM__E_8001-1A42009-04-01 (normen) · dieser Teil.

Herausgeber: OVE Österreichischer Verband für Elektrotechnik, Eschenbachgasse 9, 1010 Wien (Tel. +43 1 587 63 73, Fax +43 1 586 74 08, ove@ove.at, www.ove.at, ZVR 327279890, ATU36808601).
Dokument: **Erläuterungen zu ÖVE/ÖNORM E 8001-1/A4:2009-04-01** — Fachinformation des Österreichischen Elektrotechnischen Komitees (OEK). Ausgabe **November 2011**.
Markierungshinweis: Schlüsselpassagen sind im Original farblich, kursiv und in der Schriftart Times New Roman gekennzeichnet (Zitate aus dem Normtext).

## Inhalt

### 1. Einleitung
- Mit **ÖVE/ÖNORM E 8001-1/A4:2009** wurde der **Abschnitt 10 – Nullung** von ÖVE/ÖNORM **E 8001-1:2000** komplett überarbeitet und an verschiedene Teile des Europäischen Harmonisierungsdokuments **CENELEC HD 60364** (Basis **IEC 60364**) angeglichen.
- Verschärfungen gegenüber der bisherigen Fassung der Nullungs-Bestimmungen, für notwendig erachtet:
  - **a)** Bestimmungen über die **Ausschaltzeiten im Fehlerfall** sollten an das internationale Niveau angeglichen werden (Verringerung des Restrisikos).
  - **b)** Errichtung von Verbraucheranlagen mit **PEN-Leiter (TN-C-System)** innerhalb von Gebäuden (nunmehr „elektrisch versorgte Objekte“) sollte aus **EMV-Gründen** deutlich eingeschränkt werden. Begründung: Ein PEN-Leiter, der bestimmungsgemäß an mehreren, räumlich entfernten Punkten direkt oder über Schutzerdungsleiter mit Erde verbunden ist und gleichzeitig Betriebsstrom führt, kann Ströme über Erde und fremde leitfähige Teile verursachen → magnetische Felder → nachteilige Auswirkung auf empfindliche Betriebsmittel und vernetzte Einrichtungen der Informationstechnik.
- Erläuterungsbedarf entsteht durch die für Normen gebotene Kürze; die in **Anhang E** von E 8001-1/A4:2009 enthaltenen Erläuterungen sind laut Praxis nicht umfassend genug.
- Ziel der Überarbeitung von Abschnitt 10: die **Fünf-Leiter-Installation** innerhalb von Gebäuden von einer Empfehlung in eine **normative Bestimmung** umzuwandeln, da im TN-C-System bestimmte Betriebsmittel der Informationstechnik gestört werden können.
- Gegenargument: Aufwand in bestimmten Anlagen unzumutbar hoch, wenn die eingesetzte Informationstechnik erhöhte Störfestigkeit aufweist und zusätzliche Maßnahmen gesetzt werden.
- Andere Möglichkeit zur Vermeidung von EMV-Problemen: Anwendung eines komplexen, eng vermaschten **Erdungs-, Potenzialausgleichs- und Blitzschutzsystems** → großflächige Aufteilung von Ausgleichsströmen (z. B. Kraftwerke, Industrieanlagen).
- **Generell:** An den Bestimmungen für **Verteilungsnetze** hat sich inhaltlich nichts geändert, da die Abschnitte **10.2.2.2 bis 10.2.2.4** sich ausschließlich auf **Verbraucheranlagen** beziehen (abgegrenzt in Abschnitt **3.1.10**). Das TN-C-System mit Verbindung des PEN-Leiters zur verbraucherseitigen Erdungsanlage wird wegen sicherheitstechnischer Vorteile unverändert beibehalten.
- Bei Objekt mit eingebauter Netztrafostation oder mehreren Anspeisungen aus dem öffentlichen Verteilungsnetz → **mehrfache Verbindungen** des PEN-Leiters mit der Erdungsanlage (Anforderung der Nullungsverordnung für das öffentliche Verteilungsnetz).

### 2. Interpretationsbedürftige Textabschnitte von ÖVE/ÖNORM E 8001-1/A4:2009 (zitierter Normtext)

**Abschnitt 3.1.7 — (elektrisch versorgtes) Objekt:** Bauwerk einschließlich zugehöriger Außenanlagen mit gemeinsamer Versorgungseinrichtung für elektrische Energie (Hausanschluss, Transformator, Generator) und Hauptpotenzialausgleich.
- Als Objekt gelten auch **Gebäudekomplexe** aus mehreren Bauteilen, die gemeinsam mit elektrischer Energie versorgt werden UND ein gemeinsames System für den Hauptpotenzialausgleich haben.
- Auch elektrische Verbraucheranlagen **ohne Gebäude**, jedoch mit gemeinsamem Anschluss, gelten als ein elektrisch versorgtes Objekt.

**Bild 3-6a** — Abgrenzung zwischen Verteilungsnetz und elektrischen Anlagen in Objekten — Situation mit **einem öffentlichen Verteilernetz**.

**Abschnitt 3.1.10 — Verbraucheranlage:** Gesamtheit aller elektrischen Betriebsmittel innerhalb eines elektrisch versorgten Objekts ab der technischen Grenze des Verteilungsnetzes (gemäß Bild 3-6a und 3-6b), ausgenommen die technisch dem Verteilungsnetz zuzurechnenden Teile des Hausanschlusses.
- Im Objekt vorhandene **Stromquellen** gehören **nicht** zur Verbraucheranlage in diesem Sinne.
- **Fußnote 1):** technische Grenze = bis zur ersten Überstrom-Schutzeinrichtung in der ersten Verteilung bei bzw. nach der Nullungsverbindung des zu speisenden Objektes (Verteilungsnetze unabhängig ihrer Eigentumssituation), siehe E 8001-1/A4:2009 Abschnitt 10.2.1, 1. Aufzählungsstrich.

**Bild 3-6b** — Abgrenzung zwischen Verteilungsnetz und elektrischen Anlagen in Objekten — Situation mit **einem betrieblichen Verteilungsnetz**.

**Abschnitt 10.1.1, zweiter Absatz:** Innerhalb eines elektrisch versorgten Objekts ist für **Neuanlagen** die Verwendung eines **PEN-Leiters ab dem Anschlusspunkt der Nullungsverbindung nicht mehr zulässig**. N- und PE-Leiter müssen ab diesem Punkt als **getrennte Leiter** ausgeführt werden. Der PEN-Leiter endet am Anschlusspunkt der Nullungsverbindung (siehe Bild 3-6a, 3-6b).

**Abschnitt 10.2.2.1 — Erdungsbedingungen für Verteilnetze, Ziffer 1):** Für (z. B. öffentliche) Verteilungsnetze:
- Der PEN-Leiter muss **in der Nähe der Stromquelle (Transformator)** und **nahe den Enden der Netzausläufer** geerdet werden (**Betriebserdung**).
- **Netzausläufer = Abzweige mit Länge > 100 m.**
- In neu zu errichtenden Netzen mit überwiegend Verbraucheranlagen mit Nullung als Fehlerschutz sind Erdungen an den Enden der Netzausläufer nur dort erforderlich, wo **netzseitig Überspannungs-Schutzeinrichtungen** zum Einsatz kommen.

**Abschnitt 10.2.2.3 — Erdungsbedingungen in Verbraucheranlagen mit eigener Stromquelle (Zitat):** In Verbraucheranlagen mit **einer einzigen Stromquelle** (Transformator oder Generator) darf der Sternpunkt **nur an einem Punkt geerdet** werden (Betriebserdung). Innerhalb des Objektes sind N-Leiter und PE-Leiter **getrennt zu führen (TN-S-System)**.

**Abschnitt 10.2.2.4 — Erdungsbedingungen in Verbraucheranlagen mit mehreren Stromquellen.** ANMERKUNG: Physikalische Grundsätze für Parallelbetrieb mehrerer Stromquellen innerhalb eines elektrisch versorgten Objektes → siehe **Anhang E**.

**Abschnitt 10.2.2.4.1 — Ausführung mit Sternpunkts-Verbindungs-Leitung (SVL):**
- Bei mehreren Stromquellen (z. B. Transformatoren, Generatoren), einzeln oder parallel betrieben, sind die Sternpunkte **vorzugsweise** mittels eines **Sternpunkt-Verbindungs-Leiters (SVL)** (siehe 3.3.3.7) zu verbinden.
- Der SVL muss an **einem einzigen Punkt** geerdet werden. Ab diesem Punkt muss die Anlage als **TN-S-System** errichtet werden (symbolische Darstellung Bild 10-4).
- Der PE-Leiter darf **beliebig oft zusätzlich** geerdet oder mit dem Potenzialausgleich verbunden werden.
- ANMERKUNG: Voraussetzung ist, dass die Entfernung zwischen den Stromquellen **nicht zu groß** ist; sonst kann die Ausschaltbedingung im Fehlerfall wegen zu hoher Schleifenwiderstände nicht/nur mit hohem Aufwand erfüllt werden.

**Abschnitt 10.2.2.4.2 — Alternative Ausführung:** Ist eine Ausführung nach 10.2.2.4.1 technisch nicht sinnvoll realisierbar, darf die Speisung auf mehrere einzelne Stromquellen oder mehrere Gruppen von Stromquellen mit jeweils separatem SVL aufgeteilt werden, deren Sternpunkte bzw. SVL **jeder für sich geerdet** sind. Eine Zusammenschaltung dieser Gruppen **sollte vermieden** werden.

**Hinweis (Verbindlichkeit):** Mit der **Elektrotechnikverordnung 2002/A2, BGBl. II Nr. 223 vom 12. Juli 2010** wurde die o. a. ÖVE/ÖNORM (mit **Ausnahme des Abschnittes 10.2.2.4**) als **SNT-Bestimmung für verbindlich** erklärt. Neue Anlagen sind **bereits seit 1. Jänner 2011** dementsprechend zu errichten.

### 3. Erläuterung der einzelnen Absätze
Erläuterungen in der Reihenfolge der Abschnittsnummerierung als Interpretationshilfe.

**Zu Abschnitt 1 – Anwendungsbereich:** Mit Änderung A4 nicht verändert.
- International sind Anlagen der öffentlichen Stromversorgung vom Geltungsbereich der IEC 60364 / CENELEC HD 60364 ausgenommen; Einbeziehung den Nationalkomitees überlassen.
- In Österreich erfolgt für Verteilungsnetze durch besondere, von den internationalen Normen abweichende Aussagen: **Ausschaltstromfaktor m = 1,6** sowie generelle Anwendung des **TN-C-Systems** gemäß Nullungsverordnung.
- Ziel: deutliche Verringerung der Fehlerspannung bis zum Hausanschluss + möglichst flacher Verlauf des Fehlerspannungstrichters außerhalb des Einflussbereichs der Erdungsanlagen.

**Zu Abschnitt 3.1.7 und 3.1.9:**
- Neuer Begriff „elektrisch versorgtes Objekt“ + Neuformulierung 3.1.9 „Verteilungsleitung“ nötig, um Verteilungsnetz von „Verteilungsleitungen“ innerhalb der Objekte abzugrenzen — weil für diese **unterschiedliche Ausschaltbedingungen** festgelegt wurden.
- Früherer Begriff „Gebäude“ war unzureichend, da auch Außenanlagen einzubeziehen sind.
- Eigentumsgrenzen werden mit Netzbetreibern vertraglich geregelt → regionale Unterschiede.
- **Zulässig (unverändert):** Für eine auf gemeinsamer Fundamentplatte errichtete **Wohnhausanlage mit mehreren Stiegen** darf jede Stiege einen **eigenen Hausanschluss** erhalten und die jeweilige Nullungsverbindung mit der (eventuell gemeinsamen) Erdungsanlage verbunden werden. Gilt auch für **Einfamilien-Reihenhäuser**.
- Keine sinnvolle messtechnische Überprüfung möglich, ob Erdungsanlagen benachbarter Objekte galvanisch verbunden sind (z. B. über Fernmelde-, Fernwärmeleitungen, Blitzschutzanlagen).
- In dicht verbauten Gebieten mit eng vermaschten Erdungs-/Potenzialausgleichssystemen → „**globales Erdungssystem**“ (sicherheitstechnisch sehr vorteilhaft).
- Ein Gebäudekomplex aus mehreren Bauwerken ist dann **ein** elektrisch versorgtes Objekt, wenn er **nur einen Netzanschluss** hat UND einen gemeinsamen, umfassenden Hauptpotenzialausgleich aufweist.

**Zu Bild 3-6a:** Dient der Verdeutlichung der Abgrenzungen zwischen:
- a) Verteilungsnetzen gemäß Abschnitt **3.1.3**,
- b) Verteilungsleitungen gemäß Abschnitt **3.1.9** (zu denen nunmehr auch **Hauptleitungen** gemäß Abschnitt **3.1.10** gehören),
- c) Endstromkreisen gemäß Abschnitt **3.1.11.3**.
- Symbolisch dargestellt: PEN-Leiter des Verteilungsnetzes wird **nur in das Objekt eingeführt** und endet an der Verteilung am Anschlusspunkt der Nullungsverbindung (bisher durfte PEN-Leiter weiter in die Anlage geführt werden). Über Verbindung/Trennung der Erdungsanlagen der einzelnen Objekte sagt das Bild nichts aus.

**Zu Bild 3-6b:** Auch ein „betriebliches Verteilungsnetz“ kann als **TN-C-System** ausgeführt werden (vorausgesetzt, keine EMV-Probleme zu erwarten). Beispiel: Betrieb mit mehreren Gebäuden, Niederspannungs-Verteilungsnetz ähnlich einem öffentlichen Netz.
- In der Trafostation ist wegen des nach außen weiterführenden TN-C-Systems ein **Verteiler mit PEN-Leiter** vorhanden.
- Anzunehmen: Betriebserdung des Transformators UND Nullungsverbindung im Objekt sind an dasselbe Erdungssystem (z. B. **Fundamenterder**) angeschlossen. Aus EMV-Sicht nicht optimal, aber bei **kurzer Entfernung** der beiden Anschlüsse vom neutralen Punkt zur Erdungsanlage tolerierbar. Auch anwendbar, wenn die Trafostation für die öffentliche Versorgung weiterer Objekte genutzt wird.
- Verantwortlichkeit/Zugang/Instandhaltung der Erdungsanlage bei unterschiedlichen Betreibern vertraglich zu regeln.
- Lassen sich Verbindungen über leitfähige Systeme (Rohrleitungen, geschirmte Kabel der Informationstechnik) nicht vermeiden, ist die **EMV in diesem Bereich zu gewährleisten**.

**Zu Abschnitt 10.2.1.2 – Ausschaltbedingung für Verteilungsleitungen in Verbraucheranlagen und für Endstromkreise mit Überstrom-Schutzeinrichtungen mit Nennstrom über 32 A:**
- Verweis auf redaktionelle Korrektur der Fachinformation „Korrekturen zu ÖVE/ÖNORM E 8001-1“ vom **2010-07-01**: Anwendung der Ausschaltstromfaktoren gilt als **Alternative** zur Ermittlung der Ausschaltzeit.
- Ausschaltstromfaktoren wurden zum Teil **verschärft** und kommen auch für **Hauptleitungen („Steigleitungen“) gemäß 3.1.9.1** zur Anwendung (für die bisher die Bedingungen für Verteilungsnetze gelten durften).

**Zu Abschnitt 10.2.1.3 – Ausschaltbedingung für Endstromkreise bis einschließlich 32 A Nennstrom:**
- Verweis auf dieselbe redaktionelle Korrektur vom 2010-07-01: Ausschaltstromfaktoren als Alternative zur Ermittlung der Ausschaltzeit.

**Zu Abschnitt 10.2.2.3 – Erdungsbedingungen in Verbraucheranlagen mit eigener Stromquelle:**
- Eine Stromquelle gehört laut Definition **nicht** zur Verbraucheranlage. Daher hat die Forderung „nur an einem Punkt geerdet“ keine Bedeutung für eine allfällige **Betriebserdung des Transformatorsternpunktes** am Transformatorstandort.
- Diese Betrachtungsweise ist aus EMV-Sicht physikalisch nicht korrekt, aber aus schutz- und abgrenzungstechnischen Gründen zulässig.
- Bei besonders empfindlichen Einrichtungen: Installation ab dem Transformator als **TN-S-System gemäß Abschnitt 10.1.3** ausführen und **nur einen einzigen Erdungspunkt** des Neutralleiters in der gesamten Anlage (beim Transformator oder in der Niederspannungshauptverteilung) realisieren.
- Das **Gehäuse einer Stromquelle** muss angemessen in eine Schutzmaßnahme einbezogen werden.
- **Schutzleiterdimensionierung:** Angaben in **ÖVE/ÖNORM E 8001-1/A5:2010**. Für den Schutzerdungsleiter zum Gehäuse einer Stromquelle: Querschnitte gemäß **Tabelle 21** reichen in Abhängigkeit von der Abschaltzeit u. U. nicht aus → dann nach **Abschnitt 21.3.1.1** zu ermitteln.

**Zu Abschnitt 10.2.2.4 – Erdungsbedingungen in Verbraucheranlagen mit mehreren Stromquellen:**
- Abgeleitet aus **IEC 60364-4-444**; Maßnahmen zur EMV-Verbesserung durch Vermeidung von Ausgleichsströmen, die in konventionell im **TN-C-S-System** ausgeführten Anlagen durch mehrere Erdungspunkte an verschiedenen Stromquellen verursacht werden.
- Weitere EMV-Maßnahmen für informationstechnische Anlagen können nötig sein (bestimmte Verlegetechniken, Abschirmmaßnahmen). Ein CENELEC-Harmonisierungsdokument ist erschienen, Umsetzung steht aus.
- Gemäß 10.2.2.4.1 ist die Anlage **vorzugsweise** gemäß **Bild 10-4 bzw. Bild 10-5** auszuführen; Alternativen zulässig (Alternative in 10.2.2.4.2). Eine Zusammenschaltung der Gruppen soll vermieden werden, ist aber **nicht ausgeschlossen** → **kein Verbot**.
- International empfohlener Verzicht auf Mehrfacherdung des neutralen Punktes in Hochleistungsanlagen → deutliche Reduzierung der Ströme auf Schutzleitern und damit der EMV-Beeinflussungen.
- Weniger empfindliche Datenübertragungs-Technologien verfügbar (siehe **ÖVE/ÖNORM EN 61000-6-1** und **ÖVE/ÖNORM EN 61000-6-2**).

**Denkbare Alternativen:**
- **a)** Für Anlagen ohne empfindliche / mit ausreichend störfester Informationstechnik kann die bisherige Lösung eines **TN-C-S-Systems** ausgeführt werden. Im TN-C-Teil lassen sich die Stromquellen jeweils unmittelbar an den Sternpunkten erden und parallel schalten (durch Schieflasten verursachte Ausgleichsströme über Erdungs-/Potenzialausgleichssystem werden in Kauf genommen).
- **b)** Mehrere kleinere Stationen mit jeweils **nur einer Stromquelle** gemäß 10.2.2.4.2, die nur die zugeordneten Verbraucherstromkreise versorgen und **nicht parallel** betrieben werden. Umschaltung zwischen Stationsbereichen erfolgt **ausschließlich vierpolig und mit kurzer Unterbrechung** (auch wegen zu beherrschender Kurzschlussleistung).

**Details bei vorzugsweiser Ausführung nach 10.2.2.4.1 (schon bei Planung der baulichen und elektrischen Anlagen zu berücksichtigen):**
- Alle (auch nur kurzzeitig) parallel betriebenen Stromquellen möglichst **nahe beieinander** und **nahe bei der Hauptverteilung** anordnen — gilt auch für **Ersatzstromanlagen**.
- Der **Kessel** der einspeisenden Transformatoren ist durch eine Schutzmaßnahme mit automatischer Abschaltung zu schützen; entsprechender **Primärschutz mit kurzer Ausschaltzeit** erforderlich, notfalls über **Leistungsschalter**. Bei Primärschutz durch **HH-Sicherungen** muss gewährleistet sein, dass diese so rasch ausschalten, dass der Schutzerdungsleiter zum Trafokessel nicht überlastet wird. Bei Schaltung gemäß **Bild 10-5** ist der **komplexe Widerstand der Fehlerschleife** vom Trafokessel über Schutzerdungsleiter, Schutzleiterschiene und SVL zurück zum Sternpunkt zu berücksichtigen. **Die Regel, dass der halbe Querschnitt eines Außenleiters für den Schutzerdungsleiter jedenfalls ausreicht, gilt in diesem speziellen Fall NICHT.** Auch der **induktive Widerstand** der Fehlerschleife ist jedenfalls zu berücksichtigen.
- Das **Gehäuse eines Generators** muss geschützt und der zuführende Schutzleiter ausreichend dimensioniert sein. Ggf. **vierpoliger Generatorschalter** verwenden, der vom Generatorschutz **unverzögert** ausgelöst wird; durch geeigneten Schaltkontakt im SVL wird der Fehlerstromkreis (Generatorgehäuse → Schutzerdungsleiter → Schutzleiterschiene → SVL → Sternpunkt) rasch unterbrochen → geeignete Dimensionierung des Schutzerdungsleiters möglich. **Auch hier gilt die Regel des halben Außenleiter-Querschnitts NICHT.** Induktiver Widerstand der Fehlerschleife bei Fehler der Stromquelle zu deren Gehäuse ist zu berücksichtigen.
- **Ausschaltbedingungen gemäß Abschnitten 10.2.1.2 bis 10.2.1.4** sind für **jeden vorhersehbaren Betriebszustand** (auch bei Betrieb der Ersatzstromanlagen) sicherzustellen.
- Durch geeignete Auswahl von Schienen und Kabeln und deren **induktionsarme Verlegeanordnung** sind induzierte Ströme auf Schutzerdungs- und Schutzpotenzialausgleichsleitern zu minimieren.

**Ergänzende Verweise:** ÖVE/ÖNORM **EN 50310** und ÖVE/ÖNORM **EN 50174**.

## Maschinen-Regeln

- [ABSTAND] Netzausläufer = Abzweige mit Länge > 100 m (PEN-Leiter nahe Stromquelle und nahe Netzausläufer-Enden zu erden) (E 8001-1/A4:2009 Abschnitt 10.2.2.1 Ziffer 1, S.4)
- [STROMKREIS] Ausschaltstromfaktor für Verteilungsnetze in Österreich: m = 1,6 (Erläuterung zu Abschnitt 1, S.5)
- [STROMKREIS] Ausschaltbedingung für Verteilungsleitungen in Verbraucheranlagen und Endstromkreise mit Überstrom-Schutzeinrichtung > 32 A Nennstrom: Ausschaltstromfaktoren als Alternative zur Ausschaltzeit-Ermittlung (Abschnitt 10.2.1.2, S.6)
- [STROMKREIS] Ausschaltbedingung für Endstromkreise bis einschließlich 32 A Nennstrom: Ausschaltstromfaktoren als Alternative zur Ausschaltzeit-Ermittlung (Abschnitt 10.2.1.3, S.6)
- [STROMKREIS] Ausschaltstromfaktoren gelten auch für Hauptleitungen ("Steigleitungen") gemäß 3.1.9.1 (Abschnitt 10.2.1.2, S.6)
- [STROMKREIS] Ausschaltbedingungen gemäß Abschnitten 10.2.1.2 bis 10.2.1.4 sind für jeden vorhersehbaren Betriebszustand (auch Ersatzstrombetrieb) sicherzustellen (Erläuterung 10.2.2.4.1, S.7)
- [PFLICHT] Neuanlagen: PEN-Leiter ab Anschlusspunkt der Nullungsverbindung nicht mehr zulässig; N- und PE-Leiter ab diesem Punkt als getrennte Leiter (TN-S) ausführen (Abschnitt 10.1.1 Abs.2, S.3/4)
- [PFLICHT] PEN-Leiter endet am Anschlusspunkt der Nullungsverbindung (Abschnitt 10.1.1 Abs.2, S.4)
- [PFLICHT] Verbraucheranlage mit einer einzigen Stromquelle: Sternpunkt nur an einem Punkt erden (Betriebserdung); N- und PE-Leiter getrennt führen = TN-S-System (Abschnitt 10.2.2.3, S.4)
- [PFLICHT] Bei mehreren Stromquellen mit SVL: SVL an einem einzigen Punkt erden; ab dort TN-S-System; PE-Leiter darf beliebig oft zusätzlich geerdet/mit Potenzialausgleich verbunden werden (Abschnitt 10.2.2.4.1, S.4)
- [PFLICHT] Umschaltung zwischen Stationsbereichen (Alternative b) ausschließlich vierpolig und mit kurzer Unterbrechung (Erläuterung 10.2.2.4, S.7)
- [LEITUNG/QUERSCHNITT] Bei Fehlerschleife Trafokessel→Schutzerdungsleiter→Schutzleiterschiene→SVL→Sternpunkt (Bild 10-5) gilt die Regel "halber Außenleiter-Querschnitt reicht für Schutzerdungsleiter" NICHT; induktiver Widerstand der Fehlerschleife zu berücksichtigen (Erläuterung 10.2.2.4.1, S.7/8)
- [LEITUNG/QUERSCHNITT] Generatorgehäuse-Schutzleiter: Regel "halber Außenleiter-Querschnitt reicht" gilt NICHT; induktiver Widerstand der Fehlerschleife zu berücksichtigen (Erläuterung 10.2.2.4.1, S.8)
- [LEITUNG/QUERSCHNITT] Schutzerdungsleiter zum Gehäuse einer Stromquelle: Querschnitte gemäß Tabelle 21 reichen je nach Abschaltzeit u. U. nicht aus → nach Abschnitt 21.3.1.1 ermitteln; Schutzleiterdimensionierung siehe E 8001-1/A5:2010 (Erläuterung 10.2.2.3, S.6)
- [PFLICHT] Bei mehreren Stromquellen: Generator ggf. mit vierpoligem, unverzögert vom Generatorschutz ausgelöstem Generatorschalter; Schaltkontakt im SVL (Erläuterung 10.2.2.4.1, S.8)
- [DEFINITION] (Elektrisch versorgtes) Objekt = Bauwerk inkl. zugehöriger Außenanlagen mit gemeinsamer Versorgungseinrichtung (Hausanschluss/Transformator/Generator) und Hauptpotenzialausgleich; auch Gebäudekomplexe mit gemeinsamer Versorgung + gemeinsamem Hauptpotenzialausgleich; auch Verbraucheranlagen ohne Gebäude mit gemeinsamem Anschluss (Abschnitt 3.1.7, S.2)
- [DEFINITION] Verbraucheranlage = Gesamtheit aller elektrischen Betriebsmittel innerhalb eines elektrisch versorgten Objekts ab der technischen Grenze des Verteilungsnetzes, ausgenommen dem Verteilungsnetz zuzurechnende Teile des Hausanschlusses; Stromquellen im Objekt gehören nicht dazu (Abschnitt 3.1.10, S.3)
- [DEFINITION] Technische Grenze des Verteilungsnetzes = bis zur ersten Überstrom-Schutzeinrichtung in der ersten Verteilung bei/nach der Nullungsverbindung des zu speisenden Objektes (Fußnote zu 3.1.10 / 10.2.1, S.3)
- [DEFINITION] Globales Erdungssystem = eng vermaschtes Erdungs-/Potenzialausgleichssystem in dicht verbauten Gebieten (sicherheitstechnisch sehr vorteilhaft) (Erläuterung 3.1.7, S.5)
- [PFLICHT] Wohnhausanlage mit mehreren Stiegen auf gemeinsamer Fundamentplatte: je Stiege eigener Hausanschluss zulässig, Nullungsverbindung mit (ggf. gemeinsamer) Erdungsanlage; gilt auch für Einfamilien-Reihenhäuser (Erläuterung 3.1.7, S.5)
- [PFLICHT] Gebäudekomplex = ein elektrisch versorgtes Objekt nur bei genau einem Netzanschluss UND gemeinsamem umfassendem Hauptpotenzialausgleich (Erläuterung 3.1.7, S.5)
- [FRIST] Elektrotechnikverordnung 2002/A2, BGBl. II Nr. 223 vom 12.07.2010 erklärt E 8001-1/A4:2009 (außer Abschnitt 10.2.2.4) für verbindlich; Neuanlagen seit 1. Jänner 2011 entsprechend zu errichten (Hinweis Abschnitt 2, S.4)
- [PFLICHT] Parallel betriebene Stromquellen inkl. Ersatzstromanlagen möglichst nahe beieinander und nahe bei der Hauptverteilung anordnen (Erläuterung 10.2.2.4.1, S.7)
- [PFLICHT] Trafokessel mit automatischer Abschaltung schützen; Primärschutz mit kurzer Ausschaltzeit, notfalls Leistungsschalter; bei HH-Sicherungen rasche Abschaltung damit Schutzerdungsleiter nicht überlastet (Erläuterung 10.2.2.4.1, S.7)
