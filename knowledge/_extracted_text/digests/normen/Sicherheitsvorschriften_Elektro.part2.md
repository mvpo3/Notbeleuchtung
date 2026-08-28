# Sicherheitsvorschriften_Elektro — Teil 2
> Quelle: Sicherheitsvorschriften_Elektro (normen) · Seiten 81-120.

WIFI-Schulungsunterlage "Elektrotechnische Sicherheitsvorschriften" auf Basis der ÖVE/ÖNORM E8001-1 (mit Nachträgen A1–A4) und der ÖVE E8101. Dieser Teil 2 behandelt: Leiterbezeichnungen und Farbkennzeichnung, Überspannungsschutz (SPD), das dreistufige Schutzkonzept (Basis-/Fehler-/Zusatzschutz), die acht Fehlerschutzvorkehrungen (Schutzisolierung, SELV/PELV, Schutztrennung) und die automatische Abschaltung im TT- und TN-Netz inklusive der drei Nullungsbedingungen und der seit 01.12.2008 gültigen Nullungs-Ausführung.

## Inhalt

### 18.5 Leiterbezeichnung

**Kennzeichnung in Schaltplänen (18.5.1):**
- N = Neutralleiter
- PE = Protection Earth (SL = Schutzleiter)
- PEN-Leiter = Kombination aus Schutz- und Neutralleiter
- L = Line (Außenleiter)

**Funktion der einzelnen Leiter (18.5.2)** — jeder Leiter darf nur für seine zugeteilte Funktion verwendet werden; Farbabweichungen behandelt ÖNORM E8001-3 (Kabel und Leitungen):
- **Außenleiter (L):** steht im üblichen Betrieb unter Spannung, überträgt/verteilt Energie, ist kein Neutral- oder Mittelleiter.
- **Neutralleiter (N):** mit dem Neutralpunkt elektrisch verbunden, trägt zur Energieverteilung bei.
- **Schutzleiter (PE):** Leiter zum Zweck der Sicherheit, z.B. Schutz gegen elektrischen Schlag.
- **Schutzerdungsleiter:** Schutzleiter zur Verbindung mit Erdpotentialen.
- **Potentialausgleichsleiter (PA-Leiter):** elektrische Verbindung zum Herstellen des Potentialausgleichs.
- **Nullungsverbindung:** möglichst kurze, leitfähige Verbindung, mit der der PEN-Leiter im ersten geeigneten Sicherungs-/Verteilerkasten einer Verbraucheranlage direkt oder über den Hauptpotentialausgleich mit dem Schutzerdungsleiter verbunden wird.
- **PEN-Leiter:** erfüllt zugleich Funktion von Schutzerdungs- und Neutralleiter.
- **PEM-Leiter** (selten): Schutzerdungs- + Mittelpunktleiter.
- **PEL-Leiter** (selten): Schutzerdungs- + Außenleiter (z.B. geerdete Steuerspannung).

**Farbkennzeichnung der Leiter (18.5.3):**
- **Grün/Gelb (gn/ge):** ausschließlich für Leiter mit Schutzfunktion (Schutzleiter, PEN-Leiter, Potentialausgleichsleiter).
- **Hellblau (hbl):** ausschließlich für den Neutralleiter — auch nicht als Schalterdraht in 3-poligen Leitungen.
- **Schwarz, Braun, Grau (sw, br, gr):** Außenleiter in neuen Drehstromkabeln. Grau ausschließlich als Außenleiter (nicht wie in Altanlagen als Neutralleiter). Keine Vorschrift zur Phasenfolge, jedoch innerhalb einer Anlage immer gleiche Kombination. Empfohlen: Braun (L1), Schwarz (L2), Grau (L3) — entspricht der Anordnung im Kabel, kein "Auskreuzen" nötig.
- **Altanlagen:** an Steckdosen je nach Errichtungsjahr Schwarz (L), Grau (N), Rot (PE). Drei Außenleiter teils Gelb (L1), Grün (L2), Violett (L3). Ehemalige Beschriftung: R (L1), S (L2), T (L3).

### 19 Überspannungsschutz
Quellen: BGBl II 222/2002 (ÖVE/ÖNORM E8001-1), BGBl II 33/2006 (E8001-1 A2). Anlagenschäden durch Überspannungen stark zugenommen. Schutz vor Störspannungen/EMV: ÖVE E8101 Kap. 4-44; Einrichtungen zum Schutz bei Überspannung: Abschnitt 5.534. Weitere Norm: E8049 bzw. EN 62305.

**Überspannungsarten (19.1):**
- **Innere Überspannungen:** durch Schaltvorgänge in der Anlage, Schaltüberspannungen des Energieversorgers (Transformatorschaltung), Bürstenfeuer von Maschinen.
- **Äußere Überspannungen:** atmosphärische Entladungen (Gewitter), transiente Überspannungen.

**Überspannungsableiter-Arten (SPD = Surge Protected Device) (19.2):** Normenreihe ÖVE-SN60 ersetzt durch ÖVE/ÖNORM EN 61643.

Klassifikation ÖVE-SN60 (19.2.1):
- Klasse A: Überspannungsableiter für Freileitungen
- Klasse B: Blitzstromableiter für Montage in Gebäuden
- Klasse C: Überspannungsableiter für Montage in Gebäuden
- Klasse D: ortsveränderliche Überspannungsschutzgeräte
- Klasse E: Überspannungs-Feinschutzelemente

Klassifikation EN 61643-11 (2003) (19.2.2):
- **Type 1:** Prüfstrom Iimp definiert durch Amplitude, Ladung, spezifische Energie (Wellenform 10/350 µs). Entspricht etwa Klasse B.
- **Type 2:** Prüfstrom In mit Wellenform 8/20 µs. Für SPDs ohne Reihenimpedanzen (One-Port-SPDs). Entspricht etwa Klasse A, C, D.
- **Type 3:** Prüfung mit Hybridgenerator, Leerlaufspannung Uoc 1,2/50 µs, Kurzschlussstrom Isc 8/20 µs. Für SPDs mit Reihenimpedanzen (Two-Port-SPDs). Entspricht etwa Klasse D und E.

**Verwendung von SPDs (19.3)** — drei Bereiche laut ÖVE/ÖNORM E8001:
- SPDs im Verteilungsnetz
- SPDs für Installationen gegen indirekte Blitzeinwirkungen (transiente Überspannungen aus dem NS-Verteilungsnetz, Schaltüberspannungen)
- SPDs gegen direkte Blitzeinwirkungen (direkte Einschläge in Gebäude / Nähe von Gebäuden mit Blitzschutzanlage)

Gilt für Wechsel- und Gleichspannungsanlagen. Für informationstechnische Anlagen (Antennen u.a.): ÖVE-F1 Teil 7. Bahn/Hochspannung: weitere Maßnahmen.

**Installation von SPDs (19.3.1):**
- Mindestens eine SPD-Kombination so nah wie möglich an der Einspeisung.
- Bei Blitz- und Schaltüberspannungen: mind. **Type 2**.
- Bei Anlagen mit äußerem Blitzschutzsystem: mind. **Type 1**.
- Reicht der Schutzpegel nicht, zusätzliche SPDs bzw. Kombiableiter einsetzen.
- Zusätzliche SPDs auch bei empfindlichen Geräten (z.B. Steckdoseneinbau); im Endstromkreis verbaut → dauerhafter Hinweis im Verteiler nötig.

Schutz gegen transiente Überspannungen:
- SPDs zwischen aktiven Leitern (inkl. N) und Schutzleiter: **Pflicht**.
- SPDs zwischen Außenleitern und Neutralleiter: **empfohlen** (Betriebsmittelschutz).
- SPDs zwischen Außenleitern: **optional**.

**Anschlussbeispiele (19.3.2):** Schaltungen 3+0, 4+0, 3+1. In TN-S/TN-C-S kann auf SPD zwischen N und PE verzichtet werden, wenn die Aufteilung N/PE **nicht weiter als 0,5 m** vom Ableiter entfernt ist oder im selben Schaltschrank erfolgt.

**Auswahl für SPDs (19.4):** Schutzpegel UP, höchste Dauerspannung UC, Nennableitstoßstrom IN und Blitzstoßstrom Iimp, Koordination, Kurzschlussfestigkeit, Folgestromlöschfähigkeit.

**Koordination (19.5):** Kurzschlussschutz über richtige Überstromschutzeinrichtung (OCPD) ≤ maximal zulässiger Überstromschutz lt. Hersteller. Anschlussleitungsquerschnitte müssen dem Kurzschlussstrom standhalten. Überlastströme treten bei SPDs nach EN 61643-11 normalerweise nicht auf → kein Überlastschutz erforderlich.

**Fehlerschutz bei SPDs (19.6):** Fehlerschutz darf durch defekte SPDs nicht beeinträchtigt werden.
- Einbau eines **Typ-1-Ableiters nach dem FI: nicht zulässig** (außer Überspannung lastseitig zu erwarten).
- Einbau eines **Typ-2-Ableiters nach dem FI:** nur zulässig, wenn bereits vor dem FI ein Typ-2-Ableiter verbaut ist oder die Überspannung lastseitig zu erwarten ist.

**Anschluss und Querschnitt von SPDs (19.7):**
- Zwischen SPD und Haupterdungsschiene: **6 mm² bei Typ 2**, **16 mm² bei Typ 1**.
- Zwischen aktiven Leitern und SPD: **2,5 mm² bei Typ 2**, **6 mm² bei Typ 1**.
- Muss der Kurzschlussstrombelastung standhalten.
- Verbindungs-/Anschlussleitungen möglichst kurz und gerade; **Gesamtlänge der Anschluss- und Ableitung max. 0,5 m**; Leiterschleifen vermeiden; V-förmige Verdrahtung vorteilhaft.

### 20 Einteilung des Schutzkonzeptes
Quelle BGBl II 222/2002 (E8001-1). System der dreifachen Sicherheit (auch in ÖVE E8101), drei hintereinander wirkende Ebenen — versagt eine Maßnahme, greift die nächste:
- Basisschutz
- Fehlerschutz
- Zusätzlicher Schutz

**Basisschutz (20.1):** verhindert Stromfluss durch Körper (Mensch/Nutztier) bzw. begrenzt die Stromhöhe auf ungefährlichen Wert; üblicherweise Schutz gegen direktes Berühren.
- Fehlerarten: **nichtsichtbare Fehler** (Versagen der Basisisolation, leitfähige Teile werden spannungsführend) und **sichtbare Fehler** (Beschädigung Gehäuse, Feuchtigkeit/Wasser → Versagen der Basisisolation).
- Begriffe: Basisisolierung; Betriebsisolierung; **Handbereich** (mit Händen von Standflächen aus erreichbar); Standfläche.
- Durchführung (20.1.3): Basisisolierung, Abdeckung, Abgrenzung, Schutzgitter, Montage außerhalb des Handbereichs. Abdeckungen nur mit Werkzeug/Schlüssel entfernbar. **Schutzart mind. IP2X** (Ausnahmen z.B. Lampenfassung). Ausnahmeregeln für Bereiche nur für Elektrofachkräfte (BA5) oder unterwiesene Personen (BA4).
- Normen: ÖVE/ÖNORM EN 61140 (Schutz vor elektrischem Schlag), Grundsätzliches in ÖVE E8101. Handbereich gilt für NS-Anlagen bis **1000 V AC / 1500 V DC**; Hochspannung (ab 1000 V AC): andere Abstände lt. ÖVE/ÖNORM E8383.
- **Handbereich-Maße (Abb. 25):** R = 2,5 m über der Standfläche; R = 1,25 m seitlich; 0,75 m (S = Standfläche üblicherweise betretener Bereiche).

**Fehlerschutz (20.2):** wirkt bei Versagen des Basisschutzes (inaktive Teile werden spannungsführend). Verhindert/begrenzt den Strom durch Personen/Nutztiere nach Wert und Dauer.

**Zusätzlicher Schutz / Zusatzschutz (20.3):** ergänzende Maßnahme bei Versagen von Basis- und/oder Fehlerschutz, besonders bei erhöhter Gefährdung durch äußere Einflüsse/Nutzung. Üblich durch **FI-Schutzschalter mit I∆N ≤ 30 mA** und/oder zusätzlichen Potentialausgleich.

Zusatzschutz **zwingend** vorgeschrieben (20.3.2):
- Steckdosenkreise bis 20 A (lt. ÖVE-E8001 bis 16 A)
- ortsveränderliche Betriebsmittel im Freien bis 32 A
- landwirtschaftliche Betriebsstätten
- gartenbauliche Anlagen
- medizinisch genutzte Bereiche
- Unterrichtsräume mit Experimentierständen
- Campingplätze, Baustellen, Provisorien, Liegeplätze für Wasserfahrzeuge
- Schwimmbäder, Saunaanlagen, Baderäume, Springbrunnen

Details in ÖVE E8101 Teil 7; z.B. Baustellen bis 32 A Steckvorrichtungen, Landwirtschaft alle Steckvorrichtungen ohne Nennstrombegrenzung. Zusätzlicher Potentialausgleich z.B. in Landwirtschaft/Medizin.

**Ausnahme Zusatzschutz darf entfallen**, wenn alle erfüllt: Steckdosen nicht für Laien zugänglich; nur fest angebrachte/ortsfeste Betriebsmittel angesteckt; Steckdosen dauerhaft und eindeutig beschriftet.

### 21 Schutz gegen den elektrischen Schlag
Mindestens eine Schutzmaßnahme nötig, mehrere erlaubt. Eine Schutzmaßnahme = Kombination aus Basisschutz- und Fehlerschutzvorkehrung (oder verstärkter Vorkehrung), bei Bedarf zusätzliche Schutzvorkehrung.

**Durchführung Fehlerschutz (21.2):** automatische Abschaltung, schutzisolierte Ausführung, elektrische Trennung, Schutzkleinspannung; dauerhafte/sinnvolle Ausführung, richtige Schaltung; gut leitende Verbindung aller berührbaren inaktiven Teile mit Schutzleiteranschlussklemme/Schutzleiter.
- Schutzkontaktsteckdosen ohne angeschlossenen Schutzleiter dürfen **nicht** verwendet werden.
- In Räumen mit Schutzkontaktsteckdosen/Betriebsmitteln für Schutzleiter-Maßnahmen dürfen keine Schutzkontaktsteckdosen ohne Schutzleiter vorhanden sein (Ausnahme: Schutztrennung, Schutzkleinspannung).
- Schutzleiter in gemeinsamer Umhüllung beweglicher Anschlussleitungen führen. Überprüfung von Schutzmaßnahme und Isolationszustand.

**Ausnahmen Fehlerschutz darf entfallen (21.2.1):** Metallstützen von Freileitungsisolatoren (am Gebäude, außerhalb Handbereich), Stahl-/Betonmaste in Verteilungsnetzen, Elektrizitätszähler, Hausanschlusskästen, Metallrohre/-schläuche mit isolierender Auskleidung, Dachständer u.a.

**Einteilung der Schutzmaßnahmen (21.3, ÖVE E8101 Tabelle 41.001.AT):** Maßnahmen mit Schutzleiter benötigen ein bestimmtes Netz und können eine gesamte Anlage schützen; Maßnahmen ohne Schutzleiter sind netzunabhängig, schützen aber nur einzelne Betriebsmittel.

**Tabellenübersicht Schutzmaßnahmen (Abb. 26)** — Schutzmaßnahme / Basisschutzvorkehrung / Fehlerschutzvorkehrung / Zusatzschutz:
- **Nullung:** Basisisolierung / automatische Abschaltung beim ersten Fehler + Schutzpotentialausgleich / RCD I∆N ≤ 30 mA + zus. Schutzpotentialausgleich
- **Fehlerstrom-Schutzschaltung:** Basisisolierung / automatische Abschaltung beim ersten Fehler + Schutzpotentialausgleich / RCD I∆N ≤ 30 mA + zus. Schutzpotentialausgleich
- **Überstrom-Schutzerdung:** Basisisolierung / automatische Abschaltung beim ersten Fehler + Schutzpotentialausgleich / RCD I∆N ≤ 30 mA + zus. Schutzpotentialausgleich
- **Isolations-Überwachungssystem:** Basisisolierung / Warnung beim ersten Fehler + automatische Abschaltung beim zweiten Fehler + Schutzpotentialausgleich
- **Doppelte oder verstärkte Isolierung:** Basisisolierung / Isolation zwischen aktiven Teilen mit Basisisolierung und berührbaren Teilen
- **Schutztrennung:** Basisisolierung / Isolation zwischen aktiven Teilen unterschiedlicher Stromkreise + Begrenzung der Längen / Schutzpotentialausgleich für mehrere Betriebsmittel
- **SELV:** Basisisolierung oder Begrenzung der Spannung auf 25 V/AC / Spannung im Normalbetrieb unter Grenzwert für Kleinspannung + frei von Erde
- **PELV:** Basisisolierung oder Begrenzung der Spannung auf 25 V/AC / Spannung im Normalbetrieb unter Grenzwert für Kleinspannung

### 22 Die Fehlerschutzvorkehrungen
Quellen: BGBl II 222/2002 (E8001-1 + A1), BGBl II 33/2006 (A2), BGBl II 223/2010 (A3, A4). Acht mögliche Maßnahmen, müssen in einer Anlage vorhanden sein.

**22.1 Doppelte oder verstärkte Isolierung** (ÖVE 8101 Teil 4.412): zusätzliche Isolierung neben der Basisisolierung. Varianten: Basisschutz durch Basisisolierung + Fehlerschutz durch zusätzliche Isolierung; oder Basis- und Fehlerschutz durch verstärkte Isolierung. Betriebsmittel **Schutzklasse II**, typgeprüft, mit SK-II-Symbol gekennzeichnet.
- Leitfähige Teile in Umhüllung mind. **IP2X** oder Schutzzwischenisolierung gemäß ÖVE IM12.
- Isolierung muss mechanischer, elektrischer, thermischer Belastung standhalten; Anstrich/Farbe genügt i.A. nicht (außer typgeprüfte Überzüge).
- Isolierung darf nirgends unterbrochen sein und Potential übertragen; keine Befestigungen/Schrauben, durch deren Austausch auf Metall Potential übertragbar wäre.
- Bei ohne Werkzeug entfernbaren Abdeckungen dürfen dahinter keine berührbaren Teile liegen (mind. IP2X).
- Keine Schutzleiter anschließen, ggf. aber durch Betriebsmittel durchführen. Zuleitung zu SK-II-Betriebsmitteln muss durchgehenden Schutzleiter enthalten (für Laien-Austausch, z.B. Lichtauslass → Lampe könnte auf SK I gewechselt werden).
- SK-II-Geräte: feste Anschlussleitung mit Stecker ohne Schutzkontakt (Konturen- oder Flachstecker), Stecker mit Leitung unteilbares Ganzes (angegossen, nicht geschraubt).
- **Flachstecker max. 2,5 A**, **Konturenstecker max. 16 A**; Stifte bis zur Hälfte isoliert (Berührungsschutz in Schukosteckdosen).

**22.2 Schutz durch Kleinspannung SELV / PELV** (ÖVE E8101 Punkt 4.414):
- SELV = Safety Extra Low Voltage; PELV = Protective Extra Low Voltage.
- Prinzip: Begrenzung der Systemspannung, sichere Trennung von anderen Stromkreisen, Basisisolierung zwischen SELV und Erde (nur bei SELV).
- **Erzeugung (22.2.2):** sichere galvanische Trennung Primär/Sekundär — Sicherheitstransformator (ÖVE/ÖNORM EN 61558), Kleinspannungsgenerator, Umformer mit galvanisch getrennten Wicklungen, Akkumulatoren, elektronische Einrichtungen mit bauartbedingter Spannungsbegrenzung. **Verboten:** Spannungsteiler, Vorwiderstände, Potentiometer, Spartrafos.
- **Anforderungen (22.2.3):** Basisisolierung; sichere Trennung von aktiven Teilen anderer Stromkreise; SELV isoliert gegen Erde; **PELV darf geerdet werden**; sichere Trennung der Kabel-/Leitungsanlagen (räumliche Trennung, höherwertige Isolierung); geeignete Stecker-/Steckdosensysteme (Verwechslungsschutz, ohne PE); Basisisolierung darf unter bestimmten Voraussetzungen entfallen (begrenzte Spannung, normale äußere Einflüsse).

**22.3 Schutztrennung:** Basisschutz durch Basisisolierung, Fehlerschutz durch Isolierung zwischen aktiven Teilen unterschiedlicher Stromkreise + Begrenzung der Leitungslängen. Vom Erdpotential getrenntes Netz, höchstzulässige Spannung sekundärseitig **500 V**. Grundsätzlich nur ein Betriebsmittel; bei mehreren zusätzliche Anforderungen. Trennung über Trenntrafo oder gleichwertigen Motorgenerator; nur wirksam solange sekundärseitig kein Erdschluss.
- Bewegliche Leitungen über gesamte Länge sichtbar (wenn beansprucht).
- Flexible Leitungen mind. schwere Gummischlauchleitungen oder mittlere PVC-Schlauchleitungen.
- Schutzerdung darf sekundärseitig nicht geerdet werden.
- Bei mehreren Geräten an einem Trenntrafo: leitfähige Gehäuse über Schutzkontakte und Potentialausgleichsleitungen verbunden (Vermeidung Potentialunterschied bei Doppelfehler → Abschaltung der Sicherungen).
- **Maximale sekundäre Leitungslänge: U × l ≤ 100.000 Vm**, **maximale Gesamtleitungslänge 500 m** (l = Hin- + Rückleitung).

**22.4 Automatische Abschaltung der Stromversorgung im Fehlerfall:** Abschaltung in angemessener Zeit; Zeiten gelten für TT- und TN-Netz sowie für Überstrom- und Fehlerstromschutzeinrichtungen.

**Abschaltzeiten Endstromkreise bis inkl. 32 A (Abb. 30):**

| System | 50 V < U0 ≤ 120 V (AC/DC) | 120 V < U0 ≤ 230 V (AC/DC) | 230 V < U0 ≤ 400 V (AC/DC) | U0 > 400 V (AC/DC) |
|--------|---------------------------|-----------------------------|-----------------------------|---------------------|
| **TN** | 0,8 s / — | 0,4 s / 5 s | 0,2 s / 0,4 s | 0,1 s / 0,1 s |
| **TT** | 0,3 s / — | 0,2 s / 0,4 s | (in Österreich nicht zulässig) | — |

In TN-Netzen: für Verteilungsstromkreise und Endstromkreise über 32 A max. Abschaltzeit **5 s**.

**22.5 Automatische Abschaltung im TT-Netz** (ÖVE E8101 Abschnitt 4.411.5): gilt für Schutzerdung und Fehlerstromschutzschaltung. Geräte über Schutzleiter mit Erder verbunden; bei Körperschluss fließt Strom über Betriebs- und Anlagenerder → Schutzorgan schaltet ab. Vorzugsweise RCDs; Überstrom-Schutzerdung nur bei dauerhaft niederohmiger Fehlerschleifenimpedanz. **Schutzerdung im öffentlichen Netz in Österreich nicht mehr zulässig (ESV 2012)** — bei wesentlichen Änderungen/Erweiterungen Umstellung auf andere Maßnahme (z.B. Überstromschutzerdung).
- **22.5.1 Überstrom-Schutzeinrichtung:** Zs = U0 / IA mit IA = m × IN (lt. E8001-1/A4 bzw. E8101) + dauerhafte zuverlässige Erdungsanlage. IA = Abschaltstrom innerhalb der erforderlichen Zeit. Verteilungsstromkreise max. **0,4 s**, Endstromkreise nicht über 32 A max. **0,2 s** (Nennspannung max. 230 V gegen Erde).
- **22.5.2 Fehlerstrom-Schutzeinrichtung:** Zs ≤ 5 × U0 / I∆N bzw. Zs ≤ 100 Ω (lt. E8001-1/A3 bzw. E8101) + dauerhafte Erdungsanlage und entsprechende Ausschaltzeit. Vorzugsweise **Fundamenterder nach ÖVE E8014** bzw. Erdungsanlage gemäß ÖVE E8101 Teil 5-54; Mindestmaße korrosionsbeständig: **Horizontalerder mind. 10 m Länge**, **Vertikalerder mind. 4,5 m Tiefe**. Verteilungsstromkreise max. **0,4 s**, Endstromkreise nicht über 32 A max. **0,2 s** (Nennspannung max. 230 V gegen Erde).

**22.6 Automatische Abschaltung im TN-Netz (Nullung):** in ÖVE E8001 auch "Neutralleiter-Schutzerdung". Fehlerkreis über Betriebs- + Anlagenerder; Verbindung im TN-C über PEN-Leiter, im TN-S über eigenen PE-Leiter → geringer Widerstand, höherer Kurzschlussstrom, leichteres Erreichen des Abschaltstroms.

Technische Grundsätze:
- Bei für Nullung freigegebenem Verteilnetz: Nullung verwirklichen.
- Bei noch nicht freigegebenem Netz: Anlage so ausführen, dass Umstellung mit minimalen Kosten möglich ist (Nullungsverordnung); Nullungsverbindung vorbereiten, aber bis Freigabe nicht anschließen.
- Bei wesentlichen Änderungen/Erweiterungen einer nicht genullten Anlage: Nullung realisieren bzw. vorbereiten.
- Neue/umzustellende Anlagen: Hauptpotentialausgleich gemäß Vorschriften erforderlich; fehlende anzuschließende Teile vor Umstellung nachrüsten.
- Besondere Maßnahmen bei Bahn-, Hochspannungs- und kathodischen Korrosionsschutzanlagen.

**22.6.1 1. Nullungsbedingung (Ausschaltbedingung):** mindestens der Abschaltstrom der Sicherung muss fließen; Kurzschlussstrom durch Schleifenimpedanz begrenzt (Trafoimpedanz + Leitungswiderstand Außenleiter + PEN-Leiter bis Fehlerstelle). IK = U0 / ZS, IK ≥ IA, IA = m × IN. Kennwerte der Überstromschutzeinrichtungen und Querschnitte so abstimmen, dass bei Fehler mit vernachlässigbarer Impedanz zwischen Außenleiter und Schutz-/PEN-Leiter automatische Abschaltung erfolgt. Kann die 1. Bedingung nicht eingehalten werden → Einbau von FI-Schutzschaltern zulässig, wobei der Mindestkurzschlussstrom der vorgeschalteten Überstromschutzeinrichtung das **2,5-fache ihres Bemessungsstromes** betragen muss.

**22.6.2 2. Nullungsbedingung (Erdungsbedingung):** PEN-Leiter nahe der Stromquelle und nahe den Netzausläufern erden (Netzausläufer = Abzweige/Stiche > 100 m). Betriebserdung nach ÖVE/ÖNORM E8101. Nullung erfordert dauerhafte Anlagenerdung, vorzugsweise Fundamenterder; sonst korrosionsbeständige Erdungsanlage mit Mindestmaßen: **Horizontalerder mind. 10 m Länge**, **Vertikalerder mind. 4,5 m Tiefe** (wirksame Erderlänge).

**22.6.3 3. Nullungsbedingung (Verlegebedingung)** (ÖVE E8101 Teil 5: 514.3.2 bzw. 543.4):
- PEN-Leiter weder einzeln gesichert noch einzeln geschaltet (Gefahr Spannungsverschleppung bei PEN-Leiterbruch).
- PEN-Leiter nur in fest installierten Anlagen zulässig.
- Schaltung nur zusammen mit den Außenleitern (Ein voreilend, Aus nacheilend).
- PEN-Leiter mit allen guten Erdern verbinden.
- Nach Aufteilung in N und PE keine Wiederverbindung.
- PEN, Neutral- und Schutzleiter dürfen beliebig oft abgezweigt werden.
- PEN-Leiter an die PAS (Potentialausgleichsschiene) anschließen.
- Konzentrische Leiter von Starkstromkabeln dürfen als PEN-Leiter dienen.
- In Freileitungsnetzen mit blanken Leitern PEN nicht oberhalb der Außenleiter verlegen.
- Bei Querschnitten unter **10 mm² Cu (16 mm² Al)** PEN-Leiter getrennt führen.
- Kennzeichnung: durchgehend Grün-Gelb mit zusätzlicher blauer Markierung an den Leiterenden (bei Altanlagen-Umstellung auch Blau mit Grün-Gelber Markierung an den Enden).

**PEN-/Schutzleiter-Dimensionierung (ÖVE E8101 Tabelle 54.2):**

| Querschnitt Außenleiter A | Mindestquerschnitt PEN-/Schutzleiter |
|----------------------------|--------------------------------------|
| A ≤ 16 mm² | A |
| 16 mm² < A ≤ 35 mm² | 16 mm² |
| A > 35 mm² | A / 2 |

(zusätzlich Bemessungsregeln für Neutralleiter wegen Oberschwingungsströmen). Wirksamkeit der Nullung vor Inbetriebnahme prüfen (Schleifenwiderstand messen → Kurzschlussstrom ermitteln).

**Nullung bei Nennspannung über 250 V gegen Erde:** z.B. geerdete 500-V-Netze → zusätzlicher Potentialausgleich gemäß E8001-1 anwenden, damit zulässige Berührungsspannungsgrenzen bei Körperschluss nicht überschritten werden.

### 22.7 Ausführung der Nullung seit 01.12.2008
Quelle BGBl II 223/2010 (E8001-1 A4); verbindlich mit der ETV 2010.

**Neue Begriffe / Änderungen (22.7.1):**
- **(elektrisch versorgtes) Objekt:** Bauwerk inkl. Außenanlagen mit gemeinsamer Versorgungseinrichtung (Hausanschluss, Transformator, Generator) und Hauptpotentialausgleich; auch Gebäudekomplexe aus mehreren Bauteilen mit gemeinsamer Versorgung und gemeinsamem Hauptpotentialausgleich; auch Verbraucheranlagen ohne Gebäude mit gemeinsamem Anschluss.
- **Verteilungsleitungen:** Leitungen innerhalb eines Objektes (inkl. Betriebsmittel) zwischen den Abgangsklemmen der Überstromschutzeinrichtungen des Verteilers mit Anschlusspunkt der Nullungsverbindung und den Eingangsklemmen der Überstromschutzeinrichtungen der Endstromkreise.
- **Hauptleitungen:** Verteilungsleitungen ab Hausanschluss bis zu den Messeinrichtungen (Zähler).
- **Verbraucheranlage:** alle Betriebsmittel innerhalb eines Objekts ab technischer Grenze des Verteilungsnetzes (ausgenommen dem Netz zuzurechnender Hausanschlussteil); objekteigene Stromquellen gehören nicht dazu.
- **Endstromkreis:** Stromkreis zu den Verbrauchsmitteln ab der letzten Überstromschutzeinrichtung.
- **Nullungsverbindung:** möglichst kurze, gut leitfähige Verbindung des PEN-Leiters des Verteilungsnetzes im ersten geeigneten Sicherungs-/Verteilerkasten direkt oder über Hauptpotentialausgleich mit dem Schutzerdungsleiter.
- **Anschlusspunkt der Nullungsverbindung:** Stelle, an der die Nullungsverbindung an den aus dem Netz kommenden PEN-Leiter angeschlossen wird.
- **Sternpunkt-Verbindungs-Leiter (SVL):** isolierter Leiter, der die Sternpunkte aller lokal parallel betriebenen Stromquellen dauernd verbindet und an einem einzigen definierten Punkt erdet; erfüllt primär N-Leiter-Funktion, führt im Fehlerfall auch zurückfließende Fehlerströme; bei IT-Systemen darf der SVL systembedingt nicht geerdet werden.

**Ausführung (22.7.2):** Nullung erfordert ein TN-System. Verteilungsnetz muss vom Netzbetreiber für Nullung freigegeben sein; sonst andere Maßnahme (z.B. FI-Schutzschaltung). Voraussetzung: definierte gut leitfähige Nullungsverbindung zwischen Schutzerdungsleiter im Objekt und PEN-Leiter des speisenden Netzes (für alle Verbraucheranlagen im Objekt wirksam).
- Für Neuanlagen ist die Verwendung des PEN-Leiters **ab dem Anschlusspunkt der Nullungsverbindung nicht mehr zulässig** — N und PE ab diesem Punkt getrennt; PEN-Leiter endet am Anschlusspunkt.
- Nullungsverbindung gemäß Bild A ausführen, dimensioniert als Schutzerdungsleiter nach Tabelle 21-2 (E8001-1); aus EMV-Gründen Querschnitt entsprechend dem größten ankommenden Außenleiter empfohlen.
- Lage des Anschlusspunktes auf einer Abdeckung der Verteilung und am Anschlusspunkt selbst sichtbar und dauerhaft mit PEN-Symbol kennzeichnen (im Freien Kennzeichnung auf Außenabdeckung darf entfallen). Für Umstellung vorhandener Anlagen Ausführung gemäß Bild B noch gebräuchlich.

**Ausschaltbedingung ASB (22.7.3):** fehlerbehaftete Stromkreise bei Kurz-/Körperschluss mit vernachlässigbarer Impedanz in angemessener Zeit ausschalten, vorzugsweise mit Überstromschutzeinrichtungen. Unterscheidung:
1. Verteilungsnetze bis zur ersten Überstromschutzeinrichtung in der ersten Verteilung bei/nach der Nullungsverbindung.
2. Verteilungsleitungen in Verbraucheranlagen (unabhängig vom Nennstrom) sowie Endstromkreise mit mehr als 32 A.
3. Endstromkreise bis einschließlich 32 A.

**ASB in Verteilungsnetzen (22.7.4):**
- Nennspannung bis 400/230 V: **ZS ≤ 1,6 × U0 / IN**.
- Höhere Nennspannungen: **ZS ≤ 2,5 × U0 / IN**.
- ZS = Impedanz der Fehlerschleife (Rechnung/Messung); IN = Nennstrom der vorgelagerten Überstromschutzeinrichtung; U0 = Nennspannung gegen Erde.

**ASB für Verteilungsleitungen und Endstromkreise über 32 A (22.7.5):** zulässige Ausschaltzeit **5 s**. Einpoliger Kurzschlussstrom bei Körperschluss durch Berechnung/Messung der Fehlerschleifenimpedanz; Nachweis durch Vergleich mit Charakteristik der Überstromschutzeinrichtung. Alternativ Ausschaltstromfaktoren gemäß Tabelle A.

**ASB für Endstromkreise bis einschließlich 32 A (22.7.6):** zulässige Ausschaltzeit **0,4 s** für Nennspannung bis 230 V gegen Erde, **0,2 s** für bis 400 V gegen Erde. Nachweis wie oben; alternativ Tabelle A.

**Ausschaltstromfaktoren (22.7.7):** alternativ Bedingung ZS ≤ U0 / IA mit IA = m × IN; m aus Tabelle A.

**Tabelle A — Ausschaltstromfaktoren m:**

| Überstrom-Schutzeinrichtung | Endstromkreise ≤ 32 A | Verteilungsleitungen + Endstromkreise (>32 A / Vert.) |
|------------------------------|------------------------|--------------------------------------------------------|
| Schmelzsicherungen bis 125 A gG (EN 60269 Reihe) | 10 | 3,5 |
| Leitungsschutzschalter B (EN 60898 Reihe) | 5 | 3,5 |
| Leitungsschutzschalter C (EN 60898 Reihe) | 10 | 3,5 |
| Leitungsschutzschalter D (EN 60898 Reihe) | 20 | 3,5 |

Anmerkung: Für von B, C, D abweichende Kennlinien ist m so zu wählen, dass die Magnetauslösung des LS anspricht.

**Ausschaltung mittels FI-Schutzeinrichtungen (22.7.8):** kann in langen Stromkreisen die ASB / der Ausschaltstromfaktor wegen zu hoher Fehlerschleifenimpedanz nicht eingehalten werden, darf eine FI-Schutzeinrichtung (gemäß E8001-12.1.1, Bedingungen E8001-12.1) verwendet werden, wenn abweichend von Tabelle A mindestens **m = 2,5** bezogen auf die vorgelagerte Überstromschutzeinrichtung wirksam ist. Notwendiger Zusatzschutz durch weitere FI-Schutzeinrichtung mit **I∆N ≤ 30 mA**. m ≥ 2,5 sichert zeitgerechte Abschaltung auch bei Fehler zwischen Außen- und Neutralleiter.

**Ausschaltung mittels FI + zusätzlichem Potentialausgleich (22.7.9):** kann die ASB auch mit FI nicht eingehalten werden, darf **m = 1,6** gewählt werden, sofern vor Ort ein zusätzlicher Potentialausgleich errichtet wird.

**Erdungsbedingung mit eigener Stromquelle (22.7.10):** bei einer einzigen Stromquelle (Trafo/Generator) darf der Sternpunkt nur an einem Punkt geerdet werden (Betriebserdung); innerhalb des Objekts N- und PE-Leiter getrennt führen (TN-S-System).

**Ausführung mit Sternpunkt-Verbindungs-Leiter SVL (22.7.11):** mehrere Stromquellen (Trafos/Generatoren) einzeln oder parallel → Sternpunkte vorzugsweise über SVL verbinden. SVL an einem einzigen Punkt erden; ab diesem Punkt TN-S-System. Der PE-Leiter darf beliebig oft zusätzlich geerdet oder mit dem Potentialausgleich verbunden werden.
