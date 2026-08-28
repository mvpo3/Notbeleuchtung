# Sicherheitsvorschriften_Elektro — Teil 3
> Quelle: Sicherheitsvorschriften_Elektro (normen) · Seiten 121-160.

WIFI-Lehrunterlage "Elektrotechnische Sicherheitsvorschriften" auf Basis ÖVE/ÖNORM E 8101, E 8001 und ETG/ESV. Dieser Teil deckt ab: Fehlerspannungsbegrenzung im TT/TN-Netz, IT-Systeme, den Fehlerstromschutzschalter (FI/RCD) vollständig, den Brandschutzschalter AFDD, Potentialausgleich + Schutzleiter, Dokumentation/Anlagenbuch und die Überprüfung der Schutzmaßnahmen (Besichtigen, Erproben, Messen).

## Inhalt

### 22.8 Begrenzung der Fehlerspannung am geerdeten Systemleiter
- TT-/TN-Netze müssen an einem Systemleiter (N- bzw. PEN-Leiter) über einen **Betriebserder** geerdet werden.
- Gesamterdungswiderstand aller Betriebserder möglichst niedrig; **Wert von 2 Ω gilt als ausreichend**. Für Böden mit höheren Erdungswiderständen siehe ÖVE E 8101.
- R_E = kleinster Erdungswiderstand von nicht mit Schutzleiter verbundenen fremden leitfähigen Teilen, über die ein Erdschluss entstehen kann.
- Rechenbeispiel (Abb. 37): Bedingung für U_B ≤ 65 V → R_B/(R_B+R_E) × 230 V ≤ 65 V; mit R_E = 165 Ω ergibt sich R_B = 2 Ω → U_B = 65 V.

### 22.9 IT-Systeme
- Anwendung vorwiegend in Fabriken, Bergwerken, Krankenhäusern, ähnlichen Großbetrieben → hohe Betriebssicherheit erwünscht.
- IT-Systeme müssen gegen Erde **isoliert** sein oder über eine **hochohmige Impedanz** mit Erde verbunden werden. Fehlerstrom dadurch so gering, dass beim **ersten Fehler keine Ausschaltung** gefordert ist. Bei **zwei Fehlern** sind Maßnahmen gegen elektrischen Schlag zu treffen.
- Bedingung Körper-Erdung: **R_A × I_d ≤ 50 V** (I_d = Fehlerstrom beim ersten Fehler).
- Zulässige Überwachungs-Schutzgeräte: Isolationswächter (IMD), Differenzstromüberwachung (RCM), Isolationsfehlersucheinrichtung (IFLS), Überstromschutzeinrichtungen, Fehlerstromschutzeinrichtungen (RCD).
- Wenn beim ersten Fehler keine Abschaltung erfolgt, ist der Fehler durch zu melden: Isolationswächter (kombinierbar mit IFLS) oder Differenzstromüberwachung (erfasst auftretenden Differenzstrom).
- Schutzgeräte müssen **akustisches und/oder optisches Signal** erzeugen; bei beiden darf die akustische Meldung quittiert werden. Personen muss Wahrnehmung möglich sein.
- Beim **zweiten Fehler** muss automatische Abschaltung möglich sein. Bedingungen, wenn Körper über Schutzleiter an gleicher Erdungsanlage geerdet:
  - System **ohne Neutralleiter**: Z_s ≤ U / (2 × I_a)
  - System **mit Neutralleiter**: Z'_s ≤ U / (2 × I_a)
  - Z_s = Fehlerschleifenimpedanz Außenleiter↔Schutzleiter; Z'_s = Außenleiter↔Neutralleiter; I_a = Strom, der die Schutzeinrichtung betätigt.
- Bei gruppenweiser/einzelner Erdung gilt: **R_A ≤ 50 V / I_a**.

### 23 Der Fehlerstromschutzschalter (FI / RCD)
**23.1 Aufbau** — Gehäuse, Anschlussklemmen, innere Verdrahtung, Prüftaste (regelmäßige Funktionskontrolle), Prüfwiderstand. Herzstück = **Summenstromwandler** mit aufsitzender Auslösespule, die den Schaltkontakt betätigt.

**23.2 Wirkungsweise** — nach dem 1. Kirchhoffschen Gesetz; bei gleicher Summe zu-/abfließender Ströme heben sich Magnetfelder im Summenstromwandler auf. Fehlerstrom gegen Erde → Felder ungleich → in Auslösespule Spannung induziert (Transformatorprinzip) → Strom betätigt Schaltschloss → Abschaltung.
- **Abschaltzeit Personenschutz in der Praxis: 10 ms – 30 ms.**
- **Maximal erlaubte Abschaltzeit (Standardbaureihe, einfacher Auslösestrom): 300 ms.**
- Prüftaste zwischen zwei Außenleitern oder Außenleiter↔Neutralleiter; erzeugt künstlichen Fehler durch Überbrücken des Summenstromwandlers; Prüfwiderstand = Strombegrenzer (kein Kurzschluss).
- Bei Nicht-Betätigung können Adhäsionskräfte zwischen Kontakten die Federkraft übersteigen → FI bleibt „picken". **FI im Haushalt halbjährlich testen**; Herstellerangaben zu Prüfintervallen beachten; zuständig = Anlagenbetreiber/Verbraucher.

**23.3 Begriffe**
- 23.3.1 Verträglichkeit: keine Störung durch nachgeschaltete Betriebsmittel.
- 23.3.2 Kurzschlussfestigkeit: Kurzschluss nach dem FI darf für die Ausschaltzeit der vorgeschalteten Sicherung den FI nicht schädigen.
- 23.3.3 Überlastfestigkeit: Überstromschutzeinrichtungen können bis zu **einer Stunde** (großer Prüfstrom) Überströme führen → keine thermischen Schäden am FI (max. Vorsicherung beachten).
- 23.3.4 Stoßstromfestigkeit: keine Fehlauslösung durch transiente Überspannungen; **Type G 3 kA, Type S 5 kA**.
- 23.3.5 Selektivität: nur ein FI von zwei in Serie löst aus → unterschiedliche, nicht überschneidende Auslösekennlinien.
- 23.3.6 Zeitverzögerung: Ausschaltzeit abhängig vom Auslösefehlerstrom; **G-Type 10 ms – 300 ms, S-Type 40 ms – 500 ms**.
- 23.3.7 Umrichterfestigkeit: ignoriert betriebsmäßige Ableitströme **> 50 Hz** aus Umrichteranlagen.
- 23.3.8 Temperaturbeständigkeit: Funktion bis angegebener Temperatur (Baustromverteiler, Kühlräume, Freiluftverteiler).
- 23.3.9 Auslösefehlerstrom **I_ΔN** = Strom, der den FI auslöst (am FI angegeben).

**23.3.10 Kurzzeichen (Tabelle)**
| Kurz­zeichen | Bedeutung |
|---|---|
| RCD | residual current protective device — Fehlerstromschutzeinrichtung (Oberbegriff) |
| PRCD | portable residual current operated device — ortsveränderliche FI-/DI-Schalter |
| SRCD | fixed socket outlets RCD — ortsfeste FI-/DI-Schalter in Steckdosenausführung |
| RCCB | RCD ohne integralen Überstromschutz — FI-/DI-Schalter ohne eingebauten Überstromschutz |
| RCBO | RCD mit integralem Überstromschutz — FI-/DI-Schalter mit eingebautem Überstromschutz |
| RCM | residual current monitors — FI-/DI-Überwachungs- und Meldeeinrichtung |
| CBR | circuit breaker incorporating RC protection — Leistungsschalter mit integriertem Fehlerstromschutz |
| MRCD | modular residual current device — modularer Fehlerstromschutzschalter (Fehlerstromrelais) |

**23.4 Anforderungen** (ÖVE E 8101 Teil **531.3**; auch in Kapiteln Fehlerschutz/Zusatzschutz; dort auch Überstromschutzorgane + Brandschutzschalter)
- 23.4.1 Allgemein: Prüfeinrichtung leicht zugänglich. Wo unbeabsichtigtes Ausschalten Personen-/Sachschaden verursacht → **Type G oder S** (Intensivtierhaltung, Computer, Tiefkühltruhen). Für Sonderanlagen (unbesetzte Sendeanlagen, Relaisstationen, Wasserwerke) dürfen selbst-wiedereinschaltende FI verwendet werden. FI dürfen **nicht durch künstlichen Fehler abgeschaltet** werden (z. B. Not-Aus). Externe Prüfeinrichtungen, die gefährliche Fehlerspannungen erzeugen, verboten. **FI müssen allpolig inkl. Neutralleiter abschalten.** Schutzleiter **darf nicht durch den FI** geführt werden. Steckdosen-FI nur für Zusatzschutz. FI alleine in Anlagen **ohne Schutzerdungsleiter** erfüllt **nicht** den Fehlerschutz. FI vor Überlast schützen (Herstellerangaben). Eine FI-Einrichtung darf **nicht gleichzeitig Fehlerschutz und Zusatzschutz**. FI vor Inbetriebnahme prüfen.
- 23.4.2 Fehlerschutz **TN-Netz**: am Beginn der Anlage; unerwünschte Auslösungen vermeiden; PEN-Aufteilung **vor** der Schutzeinrichtung; **keine N-PE-Verbindung nach dem FI**; **kein FI in TN-C-Netz**. **TT-Netz**: am Beginn; unerwünschte Auslösungen vermeiden; R_A-Maximalwert nicht überschreiten: **R_A ≤ 50 V / I_ΔN**.
- 23.4.3 Zusatzschutz: **I_ΔN ≤ 30 mA**; Ausführungen **RCCB, RCBO**; ein RCD nicht gleichzeitig Fehler-+Zusatzschutz; Einbau vorzugsweise im Verteiler.
- 23.4.4 Brandschutz: **I_ΔN ≤ 300 mA**; Installation am Anfang der Leitungsanlage.
- 23.4.5 Vermeidung von Fehlauslösungen: Aufteilung auf mehrere FI (**max. Belastung 0,3 × I_ΔN je FI**); kurzzeitverzögerte FI; richtige Schaltung.
- 23.4.6 Auswahl nach Personengruppen: Laien (BA1), Kinder (BA2), Menschen mit Beeinträchtigung (BA3) → nur **RCCB, RCBO**. Unterwiesene Personen (BA4) + Elektrofachkräfte (BA5) → **RCCB, RCBO, MRCD**.

**23.5 Ausführungsformen**
- 23.5.1 Type **AC** (Wechselstromsensitiv): nur sinusförmige Wechselfehlerströme; Gleichstromanteile beeinflussen Abschaltung nachteilig.
- 23.5.2 Type **A** (Pulsstromsensitiv): zusätzlich pulsierende Gleichströme mit bis **6 mA** Gleichstromanteil.
- 23.5.3 Type **F**: wie A, jedoch Gleichstromanteil bis **10 mA**.
- 23.5.4 Type **B** (Allstromsensitiv): sinusförmige Wechselfehlerströme (**1000 Hz**), pulsierende und reine Gleichfehlerströme.
- 23.5.5 Type **PD**: spezieller FI für **Ladebetriebsart 3** von Elektrofahrzeugen (Allstromsensitiv).
- 23.5.6 **G-Type**: in allen Anlagen einbaubar; verhindert Fehlauslösung durch transiente Überspannungen. Zwingend vorgeschrieben lt. **ÖVE-E 8001-1** in Intensivtierhaltung, Rechenzentren, Kühlgeräten (großer wirtschaftlicher Schaden bei unbeabsichtigter Abschaltung). G = **stoßstromfest bis 3 kA (8/20 µs), kurzzeitverzögert mind. 10 ms**.
- 23.5.7 **S-Type**: für Serienschaltung; bei zwei FI in Serie muss Selektivität gewährleistet sein (Kombination Normal/G-Type mit S-Type). Netzseitig vorgeschalteter FI = **Type S mit dreifachem Auslösestrom**. S = **selektiv-stoßstromfest bis 5 kA (8/20 µs), kurzzeitverzögert mind. 40 ms**.

**23.6 Einbau des FI**
- Unterscheidung Fehlerschutz / Zusatzschutz / Brandschutz; ein FI nie gleichzeitig Fehler- + Zusatzschutz; maximale Vorsicherung richtig dimensionieren.
- 23.6.1 **Vorsicherung**: ohne Datenblatt-Angabe gilt: **Nennstrom der Vorsicherung muss um Faktor 1,6 kleiner sein als der FI-Nennstrom.**
  - Beispiel: FI I_N = 40 A → 40 A / 1,6 = 25 A → Sicherung I_N = 25 A.
  - Bzw. Sicherung 35 A → 35 A × 1,6 = 56 A → FI I_N = 63 A.
  - Thermisch eigensichere Typen dürfen **1:1** abgesichert werden (FI-Nennstrom = Sicherungsnennstrom).
- 23.6.2 Staffelung: vorgeschalteter FI muss alle auftretenden Fehlerströme erkennen.

### 24 Der Brandschutzschalter AFDD (Arc Fault Detection Device)
- In ÖVE E 8101 eigene Kapitel für Schutz vor elektrischem Brand + Brandausbreitung; AFDD erstmals in einer österreichischen Norm erwähnt.
- **24.1 Wirkungsweise**: elektronische Schaltung erfasst Fehlerlichtbogen; muss **am Beginn des Stromkreises** sitzen. Lichtbogen erzeugt „Rauschen", das ausgewertet wird; unterscheidet Fehler vom normalen Lichtbogen (z. B. Lichtschalter). **Serien- (Leiterbruch) oder Parallellichtbogen (L-N) unerheblich** — AFDD schaltet ab, bevor Brand entstehen kann.
- **RCD erfasst solche Fehler nicht** (Stromsumme bleibt Null). AFDD ersetzt nicht weitere Maßnahmen.
- Ausführungen je Hersteller: Kombination mit Leitungsschutzschalter oder mit FI/LS. **Reine Kombination AFDD + FI derzeit nicht verfügbar** und nicht sinnvoll (Fehlersuche schwierig; manche Lichtbögen erst nach Zeit/Belastung). AFDD besitzt Prüftaste + Kontrollleuchte. **Bei Isolationsmessung je nach Hersteller abschalten!**
- **24.1.1 Einbaupflicht** (Wechselstromkreise bis **16 A** Nennstrom): Schlafräume von Heimen für behinderte Menschen, Heimen für alte Menschen, Kindergärten; Räume/Orte mit Brandrisiko durch verarbeitete/gelagerte Materialien (**BE2**). BE2 = Herstellung/Bearbeitung/Lagerung entflammbaren Materials inkl. Staub (Scheunen, Holzverarbeitungs-Werkstätten, Papier- und Textilfabriken).
- **24.1.2 Einbauempfehlung** (bis 16 A): Schlafräume in Wohngebäuden (insb. dauerhaft mobilitätseingeschränkte Personen); Räume/Orte mit Gefährdung unersetzbarer Güter.

### 25 Der Potentialausgleich (Quelle BGBl II 222/2002, ÖVE/ÖNORM E 8001-1)
- Drei Arten: Hauptpotentialausgleich, zusätzlicher Potentialausgleich, Potentialsteuerung. Für jeden Hausanschluss/gleichwertige Versorgungseinrichtung erforderlich.
- **25.1 Hauptpotentialausgleich** — an Haupterdungsschiene anzuschließen (falls zutreffend): Erdungsleiter zum Anlagenerder, Schutzerdungsleiter der Hauptleitung, Nullungsverbindung, Blitzschutzanlage, Funktions-/Überspannungsschutzerdung der Fernmeldeanlage, Antennenanlagen, Wasserrohre, Gasrohre, andere metallische Rohrsysteme (z. B. zentrale Heizungs-Steigleitungen), Metallteile + Gebäudekonstruktionsteile soweit möglich.
  - **Kabeltassen u. ä. brauchen nicht einbezogen werden.** Verbindung zur Blitzschutzanlage möglichst nahe deren Erdern; bei Verbindung über Fundamenterder entfällt gesonderte Verbindung.
  - Erfolgt normalerweise über **Potentialausgleichsschiene 'PAS'**; in größeren Anlagen mehrere PAS möglich.
- **25.2 Zusätzlicher Potentialausgleich** — örtlich zusätzlich zum Hauptpotentialausgleich, wenn wegen besonderer Gefährdung gefordert (erschwerte Umgebung, **Nennspannung gegen Erde > 250 V** …). In mehrstöckigen Gebäuden mit vernetzten Informationsnetzen: zusätzlicher PA an der Hauptverteilung **jedes Stockwerks** empfohlen. Einzubeziehen: alle gleichzeitig berührbaren Teile ortsfester Betriebsmittel, Schutzerdungsleiteranschlüsse, alle fremden leitfähigen Teile, Bewehrung der Stahlbetonkonstruktion (soweit durchführbar).
- **25.2.1 Mindestquerschnitte Potentialausgleichsleiter (zusätzlicher PA):**
  - Zwischen zwei Körpern: **1 × Querschnitt des kleineren PE-Leiters**.
  - Zwischen Körper und fremdem leitfähigen Teil: **0,5 × Querschnitt des PE-Leiters**.
  - Mindestens **2,5 mm² Cu** (mit mechanischem Schutz) bzw. **4,0 mm² Cu** (ohne mechanischen Schutz).

### 25.4 Ausführung des Schutzleiters
**25.4.1 Schutzleiterquerschnitt — Zuordnung zum Außenleiter** (Schutz-/PEN-Leiter für isolierte Starkstromleitung sowie 0,6/1 kV Kabel mit 4 Leitern, alle in mm²):
| Außenleiter | Schutzleiter/PEN (isol. Starkstromltg.) | Schutzleiter/PEN (0,6/1 kV Kabel 4-Leiter) |
|---|---|---|
| 1,5 | 1,5 | 1,5 |
| 2,5 | 2,5 | 2,5 |
| 4,0 | 4,0 | 4,0 |
| 6,0 | 6,0 | 6,0 |
| 10 | 10 | 10 |
| 16 | 16 | 16 |
| 25 | 16 | 16 |
| 35 | 16 | 16 |
| 50 | 25 | 25 |
- Laut Nullung ist die **Verminderung des PEN-Leiters nicht mehr zu empfehlen**.
- Gemeinsamer Schutzleiter für mehrere Stromkreise → nach dem **größten Außenleiter** bemessen.

**25.4.2 Arten von Schutzleitern**: Leiter in mehradrigen Kabeln; isolierte/blanke Leiter in gemeinsamer Umhüllung mit Außen-+Neutralleiter; fest verlegte blanke/isolierte Leiter; metallene Umhüllungen (Mäntel, konzentrische Leiter); Metallrohre/-kapselungen/Gehäuse; fremde leitfähige Teile; Profilschienen (auch mit Klemmen/Geräten).
- Gehäuse/Konstruktionsteile als Schutzleiter nur, wenn: durchgehende elektrische Verbindung ohne Verschlechterung, Leitfähigkeit entspricht Schutzleiter-Querschnitten, Ausbau einzelner Elemente unterbricht den Schutzleiter nicht (**zweiseitiger Anschluss**). Gleiches für metallene Kabelumhüllungen und fremde leitfähige Teile.
- **Verboten als Schutzleiter**: Spannseile, Aufhängeseile, Installations-Metallrohre u. ä.

**25.4.3 Sichere elektrische Verbindung**: Schutz gegen Verschlechterung durch mechanische/chemische/elektrochemische Einflüsse; Verbindungen zwecks Prüfung zugänglich (außer vergossen); gegen Lockern geschützt; **kein Schaltorgan im Schutzleiter**; Körper elektrischer Betriebsmittel **nicht als Schutzleiter** für andere Betriebsmittel.

### 26 Dokumentation
- Mit Elektroverordnung 2002 → Teil 6 der E 8001 (erstmals Anlagenbuch geregelt). Mit ÖVE E 8101: keine Rede mehr von „Anlagenbuch", sondern **Dokumentation der elektrischen Anlage** (Anlagenbuch = Teil davon). Teil 6 erklärt erforderliche Überprüfungen. Umfasst nicht nur Messergebnisse, auch Erdungsanlagen, Mindestausstattung, Blitzschutz.
- **26.2.1 Allgemeine Angaben**: Widmung, Bezeichnung, Beschreibung (Räume, besondere Anlagen), Bescheide, Behördenauflagen, Anlagenadresse, Auftraggeber, Planer, Anlagenerrichter, Netzbetreiber, Errichtungszeitraum.
- **26.2.2 Technische Angaben**: Pläne (evtl. Listen); Hauptleitungsschema (Leitermaterial, Länge, Querschnitt, Schutzeinrichtungen); Erdungsanlage (mit Fotos); Verteilerpläne (Einstellwerte Schutzorgane, Querschnitte); Stromlaufpläne; Funktionsbeschreibungen (Motorsteuerung, Bussysteme, Datenbanken); Einbauorte der Überspannungsableiter; fotografische Dokumentation nicht mehr zugänglicher Verbindungen.
- **26.2.3 Zusatzinfo Wartung**: Einstelldaten, Bedienungs-/Wartungs-/Prüfanleitungen, Sammlung aller Herstellerangaben, technische Beschreibungen + Prüfnachweise besonderer Anlagenteile.
- Bundeseinheitliche Befund-Fassung über Kuratorium für Elektrotechnik (keine Pflicht, aber guter Leitfaden). **Dokumentation bis Ende der Lebensdauer der Anlage aufbewahren; immer aktuell halten.**
- **26.3 Prüfbericht** — 26.3.1 Erstprüfung: Prüfbericht mit allen Messergebnissen; Mängel müssen behoben werden; darf Empfehlungen/Verbesserungsvorschläge enthalten; muss übergeben und unterschrieben werden; Empfehlung für wiederkehrende Prüfung (Quellenangabe z. B. ESV) angeben. 26.3.2 Wiederkehrende Prüfung: vorherige Befunde berücksichtigen; mit oder ohne Demontage; Schäden/Verschlechterungen/gefährliche Zustände aufzeichnen; Häufigkeit nach Nutzung/Belastung/gesetzlichen Vorgaben (ESV); Bericht erstellen; Befund nachweislich übergeben.

### 27 Überprüfung der Schutzmaßnahmen
Quellen: BGBl II 222/2002 (ÖVE/ÖNORM E 8001-6-61); BGBl II 223/2010 (ÖVE/ÖNORM EN 50110-1-2008).
- **27.1 Allgemeines**: ETG fordert Sicherheitsnachweis für jede Anlage. ÖVE E 8101 Teil 6 regelt Messmethoden bei Erstprüfung + Dokumentation. Jede Anlage **vor Inbetriebnahme** prüfen. Nur Elektrofachkräfte mit Erfahrung als Prüfer. Besonders strenge Maßstäbe bei: feuer-/explosionsgefährdeten Räumen, Räumen mit größeren Menschenansammlungen, Spitälern, Industriebetrieben, Notstromversorgungsanlagen.
- **Prüfbestimmungen 2000–2018**: ÖVE/ÖNORM E 8001-6-61 (Erstprüfung), -6-62 (Wiederkehrende + außerordentliche Prüfung), -6-63 (Anlagenbuch + Prüfberichte).
- **Prüfbestimmungen ab 2019**: ÖVE E 8101-6-600.3 (Erstprüfung), ÖVE E 8101-6-600.4 (Wiederkehrende Überprüfung), ÖVE E 8101-1-134 (Errichten + Prüfen elektrischer Anlagen).
- **27.2 Mängel laut ETG**: §9 Abs. 3 (Zustand/Betrieb entspricht nicht dem Gesetz/Verordnung); §9 Abs. 4 (zusätzlich unmittelbare Gefahr für Leben/Gesundheit von Personen oder Sachen).
- **27.3 Begriffe**: Prüfen umfasst Besichtigen, Erproben, Messen. Besichtigen = augenscheinliche Überprüfung der bestimmungsgemäßen Errichtung. Erproben/Messen = alles darüber hinaus zur Feststellung, ob die Anlage ihren Zweck erfüllt.

**27.4 Die Besichtigung** (erster Schritt, vorzugsweise bei abgeschalteter Anlage)
- **27.4.1 Punkte laut ÖVE E 8001-6-61**: Übereinstimmung mit Sicherheitsanforderungen (Aufschriften/Kennzeichnung/Zertifikate); korrekte Auswahl + Einbau; keine sichtbaren sicherheitsbeeinträchtigenden Beschädigungen; Art + Maßnahme des Fehlerschutzes; Selektivität; **Messung von Abständen (Handbereich, Schutzbereich im Bad)**; Brandabschottungen; Leiterquerschnitte vs. Strombelastung; Spannungsabfall; Leiter/Erdungsleitung/Erder inkl. Dokumentation; Schutz-/Überwachungseinrichtungen + Einstellung (Motorschutz); Trenn- und Schaltgeräte an richtiger Stelle; Einbauorte + Auswahl von SPDs; EMV-Maßnahmen; Schutzart (Schutzklasse, IP); Kennzeichnung/richtige Verwendung der Leiter (N, PE); Vorhandensein von Plänen; Warnhinweise/Absperrungen/Hindernisse; Kennzeichnung von Stromkreisen/Sicherungen/Schaltern/Klemmen; ordnungsgemäße Leiterverbindungen; leichte Zugänglichkeit zur Bedienung.
- **27.4.2 Schutzmaßnahmen mit Schutzleiter**: PE-/Erdungs-/PA-Leiter mit gefordertem Querschnitt, einwandfrei verlegt + zuverlässig angeschlossen + richtig gekennzeichnet; Schutzleiter nicht mit aktiven Teilen verbunden; PE und N nicht verwechselt; in Schaltanlagen/Verteilern Teil 2 §30 eingehalten; Schutzkontakte der Steckdosen ohne Mängel; in PEN-Leitern keine Überstromschutzeinrichtungen und PEN nicht allein schaltbar; Schutz-/Schaltgeräte richtig ausgewählt.
- **27.4.3 Schutzmaßnahmen ohne Schutzleiter**: bei Schutzkleinspannung (SELV), Funktionskleinspannung, Schutztrennung richtige Auswahl von Stromquellen/Leitungen/Betriebsmitteln; bei SELV/Funktionskleinspannung nur Steckdosen, die in derselben Anlage nicht für höhere Spannungen verwendet werden; Schutzisolierung nicht durch leitfähige Teile/Beschädigung unwirksam.

**27.5 Erproben und Messen**
- **27.5.1 Allgemeines**: Erprobung = Betätigung von Prüfeinrichtungen (Isolationswächter, FI, Not-Aus, sicherheitstechnische Einrichtungen). Messungen dürfen keine Unfall-/Brandgefahr erzeugen, daher: (1) Messgeräte, deren Ausgangsspannung bei Belastung die zulässige Berührungsspannung (z. B. 50 V bzw. 90 V) nicht überschreitet — Prüfgeräte nach ÖVE/ÖNORM EN 61557; (2) Maßnahmen gegen Mess-Spannungen/-Ströme (Abschranken, Beobachter). Bei nicht durchführbaren Messungen (ausgedehnte Erdungsanlagen, große Querschnitte) Nachweis durch Berechnung/Netzmodell.
- **Reihenfolge der Erprobungen/Messungen**: 1. Durchgängigkeit Schutzerdungs-/PA-Leiter (zweckmäßig auch N); 2. Isolationswiderstände der Anlage; 3. Isolationswiderstand bei SELV/PELV/Schutztrennung; 4. Isolationswiderstände bei isolierenden Fußböden/Wänden; 5. automatische Abschaltung im Fehlerfall; 6. Spannungspolarität; 7. Prüfung Fehlerschutz (automatische Abschaltung); 8. Zusatzschutz; 9. Phasenfolge; 10. Funktionsprüfungen; 11. Spannungsabfall. Bei festgestelltem Fehler betroffene Prüfungen nach Behebung wiederholen.
- **27.5.2 Durchgängigkeit der Leiter**: Messung mit Geräten nach **ÖVE EN 61557-4**. Zu messen: Schutzleiter inkl. PA-Leiter, Verbindungen zu Körpern, bei ringförmigen Endstromkreisen auch aktive Leiter.
- **27.5.3 Isolationswiderstand**:
  - a) Betriebsmittel (ÖVE E 8701, alt ÖVE HG701): schutzisolierte Geräte **≥ 2 MΩ**; Geräte mit Schutzleiter: Schutzleiterwiderstand **max. 0,3 Ω** (Anschlussleitung während Messung bewegen → Leitungsbruch/mangelhafter Anschluss feststellbar).
  - b) Anlage: zwischen allen aktiven Leitern und Erde messen; in TN-C wird PEN als geerdet betrachtet; N von Spannungsversorgung trennen; vorhandene Überspannungs-Schutzeinrichtungen abklemmen. Messung mit **Gleichspannung**, Prüfgerät muss bei **Messstrom 1 mA** die Prüfspannung abgeben. Bei elektronischen Geräten im Stromkreis: L und N während Messung verbinden.
  - **Mindestwerte Isolationswiderstand ÖVE E 8101**: SELV/PELV → Prüfspannung 250 V DC, ≥ **0,50 MΩ**; bis einschl. 500 V und FELV → 500 V DC, ≥ **1,00 MΩ**; über 500 V → 1000 V DC, ≥ **1,00 MΩ**.
  - **Mindestwerte Isolationswiderstand ÖVE E 8001** (älter): SELV/PELV → 250 V, ≥ **0,25 MΩ**; bis einschl. 500 V → 500 V, ≥ **0,50 MΩ**; über 500 V → 1000 V, ≥ **1,00 MΩ**.
  - Wenn Abtrennung der Überspannungs-Schutzeinrichtungen nicht möglich (z. B. eingebaut in Steckdosen): Prüfspannung auf **250 V** reduzierbar, Isolationswiderstand muss **1 MΩ** betragen.
  - Anlagen vor 2000: nach ÖVE EN1 — Mindestisolationswert **1 kΩ pro Volt**; in feuchten/nassen Räumen reduzierbar auf **500 Ω pro Volt**.
- **27.5.4 Spannungspolarität**: einpolige Schaltgeräte (Sicherungen) nur im Außenleiter; Lampenanschlüsse richtig (L-N) wenn vorgegeben; Steckdosen mit vorgegebenem N-Anschluss richtig angeschlossen.
- **27.5.5 Fehlerschutz**: Nachweis automatische Abschaltung mit Schutzleiter.
  - a) **TN-Netz** (FI für Brandschutz nach diesen Vorgaben prüfen): Messung der Fehlerschleifenimpedanz (entfällt, wenn Berechnung/Schutzerdungswiderstand vorliegt + Länge/Querschnitt nachweisbar → Durchgängigkeitsnachweis ausreichend); Nachweis der Schutzeinrichtungs-Charakteristik (eingestellter Auslösestrom Leistungsschalter, Nennstrom Sicherungen). Abschaltzeiten für TN einhalten.
  - b) **TT-Netz**: Messung Fehlerschleifenimpedanz; Nachweis Charakteristik; bei FI Besichtigung + Messung.
  - **Erforderliche Auslösezeiten FI bei I_ΔN**: allgemein **0,300 s**, Typ G **0,300 s**, Typ S **0,500 s**.
- **27.5.6 Zusätzlicher Schutz**: Wirksamkeit durch Messen + Besichtigen; Abschaltzeiten nach TN-Werten; erforderlicher Erdungswiderstand nachzuweisen.
- **27.5.7 Fehlerschleifenimpedanz**: mit Nennfrequenz messen; Methoden in ÖVE E 8001-6-61 Anhang D. Labor-/Fabrikmessungen mit nennenswerten Fehlerströmen dürfen berücksichtigt werden (fabriksfertige Schaltgerätekombinationen inkl. Sammelschienen, metallische Rohre, Kabel mit metallischen Umhüllungen).
- **27.5.8 Funktionsprüfungen**: Schaltgerätekombinationen, Antriebe, Stelleinrichtungen, Verriegelungen → Nachweis ordnungsgemäßer Befestigung/Einstellung/Anschluss; auch Not-Aus, Isolationswächter, FI.
- **27.5.9 Drehfeld**: Nachweis eines **rechtsdrehenden** Drehfeldes.
- **27.5.10 Spannungsabfall**: Nachweis mittels Berechnung (Impedanz des Stromkreises). In Verbraucheranlagen allgemein max. **1 % bis zur Messeinrichtung, 3 % ab der Messeinrichtung**. Bei Steckdosenstromkreisen ist der Sicherungsstrom für den Spannungsabfall maßgeblich.

**27.6 Messmethoden**
- **27.6.1 Erdungsmessung**:
  - a) **Erdungsmessbrücke**: in geschlossener Bebauung (Städte), wo Hilfserder nicht sinnvoll → andere Methoden (Stromwandler, Fehlerschleifenimpedanz).
  - b) **Erdungsmessung mit Wandlern**: selektive Messung einer einzelnen Erdungsanlage ohne Hilfserder/Sonde; geeignet bei geschlossener Bebauung, wenn benachbarte Erdungsanlagen über PEN verbunden. Zwei Stromwandler: einer induziert in der Schleife (inkl. R_X) eine Spannung, der zweite misst den Strom → Gesamtwiderstand berechenbar. Voraussetzung: zu messende Erdungsanlage nur über die erfasste Erdungsleitung (i. d. R. über PAS) mit PEN/N verbunden, alle anderen Erdungsleitungen geöffnet. Formel: **R_X ≈ R_Schleife = R_X + (R1 // R2 // … // Rn) + R_PEN = U / I**. Aufbau als Zangengehäuse oder mit zwei unabhängigen Wandlern + Grundgerät. **Für echte TT-Systeme nicht einsetzbar** (fehlender niederohmiger Rückschluss). Bei umfangreichen Anlagen nur an der Messstelle galvanische Verbindung sicherstellen.
  - c) **Messung der Fehlerschleifenimpedanz**: nur Näherungswert (ohne Phasenverschiebung); akzeptabel, wenn Reaktanz vernachlässigbar. Vor Messung Durchgängigkeit neutraler Punkt ↔ Körper prüfen. Z = (U1 − U2) / I_R.
  - d) **Korrektur des Schleifenwiderstandes**: Korrektur wegen Temperaturanstieg im Fehlerfall + Messungenauigkeit (Messungen bei kleinen Strömen + Raumtemperatur). Nachweis für TN, dass gemessene Fehlerschleifenimpedanz ÖVE/ÖNORM E 8001-1:2000-03 Abschnitt 10 erfüllt. **Achtung U_p max. 65 V (Berührungs-/Schrittspannung).** Bedingung als erfüllt, wenn:
    - **Z_s ≤ (2/3 × U_0) / I_A**; mit **I_A = 1,5 × I_K** und **I_A = m × I_N**.
    - Z_S = gemessene Fehlerschleifenimpedanz; U_0 = Nennspannung gegen Erde (V); I_A = Auslösestrom der automatischen Auslösung (A); m = Abschaltfaktor der Sicherung; I_N = Nennstrom der vorgeschalteten Leitungsschutzeinrichtung.
  - Bei **Nullung mit Zusatzschutz** ist die Ausschaltbedingung auch im FI-nachgeschalteten Anlagenteil nachzuweisen (Messung der Nullungsbedingungen am Anschlusspunkt + Schleifenwiderstand des nachgeschalteten Stromkreises).
- **Praxis-Empfehlung LS-Klasse**: standardmäßig **Leitungsschutzschalter Klasse B** statt Klasse C verwenden. Ein **16-A-LS Klasse B** schaltet bei **80 A** ab, ein **16-A-LS Klasse C** erst bei **160 A**. Beispiel: Messgerät zeigt 200 A I_K → nach Korrektur tatsächlicher Kurzschlussstrom **133 A** → LS Klasse C schaltet nicht mehr rechtzeitig ab.
