# OEVE_OENORM_E_8001-1 — Teil 1
> Quelle: OEVE_OENORM_E_8001-1 (normen) · Seiten 41-70.

ÖVE/ÖNORM E 8001-1 ist die österreichische Grundnorm für die Errichtung elektrischer Niederspannungsanlagen (Schutz gegen elektrischen Schlag, Erdung, Potentialausgleich, Überspannungsschutz). Dieser Teil deckt die Abschnitte 12.2–22 sowie die informativen Anhänge A und B ab: Fehlerstrom-Schutzschaltung, Schutztrennung, Begrenzung der Fehlerspannung am geerdeten Systemleiter (Betriebserder-Dimensionierung), Potentialausgleich, Erder, Erdungs-/Schutzerdungs-/Potentialausgleichsleiter, Isolationswiderstand, Prüfung, Blitzgefährdung in Österreich und Literaturhinweise.

## Inhalt

### 12.2 Fehlerstrom-Schutzschaltung (RCD als Fehlerschutz)
- **12.2.1.1** Alle zu schützenden Anlagenteile müssen mit geeignetem Erder verbunden sein. Erdungswiderstand R_A: **R_A ≤ 65 V / I∆N** UND **R_A ≤ 100 Ω**, je nachdem welcher Wert kleiner ist. I∆N = Nennwert des Auslösefehlerstromes (Nennfehlerstrom) der FI-Schutzeinrichtung.
- **12.2.1.2** Errichtung der Erdungen nach Abschnitt 20 und 21.
- **12.2.2.1** FI-Schutzeinrichtungen, deren Erfassungs-/Ausschaltbauteile in gemeinsamem Gehäuse sitzen (FI-Schalter), müssen **allpolig einschließlich Neutralleiter** ausschalten.
- **12.2.2.2** Für FI-Einrichtungen > **63 A** mit getrennten Gehäusen (z. B. Leistungsschalter mit Fehlerstromrelais) wird Ausschalten des N-Leiters i. d. R. nicht gefordert — ausgenommen TT-Systeme gemäß 14.2.3.1.
- **12.2.2.3** Netzspannungsabhängige FI-Einrichtungen dürfen bei Netzspannungsausfall nicht ausschalten; Fehlerstrom-Erfassung muss netzspannungsunabhängig sein.
- **12.2.2.4** Bei FI-Schaltern (12.2.2.1) darf der Auslösefehlerstrom **nicht verstellbar** sein. Bei 12.2.2.2 darf er verstellbar sein; falls Ausschaltzeit verstellbar, darf diese im gesamten Einstellbereich beim **5-fachen Einstellwert** nicht größer als **0,15 s** sein.
- **12.2.2.5** Bauart S oder mit einstellbarer Ausschaltzeit: **I∆N ≥ 0,1 A**.
- **12.2.3** Alleinige FI-Verwendung in Anlagen **ohne Schutzerdungsleiter** erfüllt nicht die Fehlerschutz-Anforderungen.
- **12.2.4** Netzseitig vor der FI liegende Anlagenteile brauchen eigene Fehlerschutzmaßnahme (z. B. Schutzisolierung). Schutzerdungsleiter darf vor der FI in gemeinsamer Umhüllung mit aktiven Leitern verlegt werden.
- **12.2.5** Eine FI-Einrichtung darf **nicht gleichzeitig** für Fehler- UND Zusatzschutz verwendet werden.
- **12.2.6** FI-Schutzschaltung muss vor erster Inbetriebnahme geprüft und dokumentiert werden (Abschnitt 22).

### 13 Schutztrennung
- Trennung des Verbraucher-Stromkreises mittels Trenntransformator oder gleichwertigem Motorgenerator vom speisenden Netz. Wirksam nur, solange auf der Sekundärseite kein Erdschluss auftritt.
- **13.2.1** Nur zulässig in Netzen mit Nennspannung **≤ 690 V**; Sekundärseite **≤ 500 V** (Leiter-Leiter).
- **13.2.2** Fehlerstrom bei einpoligem Erdschluss im Sekundärkreis **≤ 30 mA**. Eingehalten, wenn Produkt aus Nennspannung (V) × Leitungslänge (m) den Wert **100 000 nicht überschreitet**. Empfehlung: Leitungslänge wegen Beschädigungsgefahr auf **500 m** beschränken.
- **13.2.3** Bei mehreren Betriebsmitteln: Schutzkontakte von Steckdosen und/oder fest angeschlossene Betriebsmittel der Schutzklasse I über **ungeerdete isolierte Potentialausgleichsleiter** verbinden, bemessen nach Tabelle 21-3-2.
- **13.2.4** Ortsveränderliche Trenntransformatoren müssen schutzisoliert sein, fest eingebaute Steckdosen haben.
- **13.2.4.1** Schutzkontakte von Steckdosen müssen von berührbaren leitfähigen Teilen UND von nicht berührbaren aktiven/inaktiven Teilen des Trafos/Motorgenerators sicher elektrisch getrennt sein.
- **13.2.4.2** Bei nur einer Steckdose bleibt Schutzkontakt unbeschaltet; bei mehreren: über ungeerdete isolierte Potentialausgleichsleiter verbinden (siehe 13.2.3).
- **13.2.5** Flexible Leitungen mindestens schwere Gummischlauchleitung (ÖVE-K 40) oder mittlere PVC-Schlauchleitung (ÖVE-K 41).
- **13.2.6** Trenntransformatoren: ÖVE EN 60742 bzw. ÖVE EN 61558 Reihe; Motorgeneratoren: ÖVE EN 60034 Reihe; Kennzeichnung mit Zeichen gemäß Bild 13-3.
- **13.2.7** Sekundärstromkreise dürfen **nicht geerdet** und nicht mit anderen Anlagenteilen leitend verbunden werden.
- **13.2.8** Bei elektrisch leitendem Standort (Kessel, Stahlgerüste, Schiffsrümpfe): Gehäuse der Schutzklasse-I-Betriebsmittel mit dem Standort über **Kupferleiter ≥ 4 mm²** verbinden (oder Potentialausgleichsleiter mit Standort verbinden). Trafo/Motorgenerator möglichst außerhalb des Arbeitsbereiches aufstellen.

### 14 Begrenzung der Fehlerspannung am geerdeten Systemleiter (Betriebserder)
- **14.1** TT-/TN-Niederspannungsnetze an einem Systemleiter (bei Sternpunkt: N- oder PEN-Leiter) über Betriebserder R_B erden.
- **14.2.1** Erdungswiderstand der Gesamtheit aller Betriebserder ausreichend niedrig; **2 Ω gilt i. d. R. als ausreichend**. Bedingung (Formel 1): **R_B ≤ R_E · 65 / (U_N − 65)**.
  - R_B = Erdungswiderstand aller Betriebserder; R_E = kleinster abschätzbarer Erdausbreitungswiderstand der nicht mit PE/PA verbundenen fremden leitfähigen Teile; U_N = Nennspannung gegen geerdete Leiter; R_A = Erdungswiderstand der Verbraucheranlage.
  - In Gebieten geschlossener Bebauung (3.6.15) und bei reinen Kabel-Verteilungsnetzen gilt die Anforderung immer als erfüllt.
  - Abschätzung R_E: Leitungsriss Freileitung mit 10 m Leiterseil satt am Boden; Formel (2): **R_E = (ρ_E / (2·π·L)) · ln(L/d)** mit ρ_E = niedrigster spez. Erdwiderstand, L = 10 m (Annahme), d = 0,015 m (Annahme Seildurchmesser). Für U_N = 230 V Werte aus Bildern 14-2-1/14-2-2.
- **14.2.2 TN-System** PEN-Leiter hat auch Schutzerdungsleiter-Funktion; durch an PEN angeschlossenen Hauptpotentialausgleich in jeder Verbraucheranlage ist 14.2.1 immer sichergestellt. Betriebserder nach Möglichkeit mit guten Erdern verbinden.
- **14.2.3.1 TT-System** Wenn N-Leiter aus Netzbetriebsgründen sicher geerdet sein muss (nicht geschaltet, ÖVE-E 5 Teil 1 / ÖVE EN 50110): 14.2.1 einhalten; Betriebserder nach Möglichkeit mit guten Erdern verbinden, jedoch NICHT mit Anlagenerdern (Hauptpotentialausgleich) oder damit verbundenen Erdern (Blitzschutz-/Antennenerder).
- **14.2.3.2 TT-System** Wird N-Leiter als aktiver Teil betrachtet und geschaltet (ÖVE-E 5 Teil 1 / ÖVE EN 50110): Verzicht auf 14.2.1 zulässig.

### 15 Potentialausgleich
- **15.1 Hauptpotentialausgleich** Für jeden Hausanschluss / gleichwertige Versorgungseinrichtung erforderlich. An Haupterdungsschiene (Potentialausgleichsschiene PAS) / Haupterdungsklemme anschließen (falls zutreffend):
  - Erdungsleiter zum Anlagenerder
  - Nullungsverbindung (bei Ausführung gemäß Bild 10-1b)
  - Schutzerdungsleiter der Hauptleitung (PE-/PEN-Leiter)
  - Potentialausgleichsleiter von Antennenanlagen
  - Funktions- und Überspannungs-Erdungsleiter der Informationstechnik (ÖVE-F 1 Teil 7)
  - Potentialausgleichsleiter zur Blitzschutzanlage
  - Potentialausgleichsleiter zu leitfähigen Wasserverbrauchsleitungen
  - Potentialausgleichsleiter zu leitfähigen Gasinnenleitungen
  - Potentialausgleichsleiter zu anderen metallenen Rohrsystemen (z. B. Heizungs-/Klima-Steigleitungen)
  - Potentialausgleichsleiter zu Metallteilen der Gebäudekonstruktion (soweit sinnvoll)
  - ANMERKUNG: **Kabeltassen u. ä. brauchen NICHT** einbezogen werden.
  - Blitzschutz-Verbindung möglichst nahe deren Erder; entfällt, wenn sichergestellt ist, dass Blitzschutz am Anlagenerder (Fundamenterder) angeschlossen ist.
  - Bei größeren Anlagen statt einer PAS mehrere Erdungsschienen/Haupterdungsklemmen an durchlaufender Potentialausgleichsleitung; diese je nach Anforderung als Schutzerdungsleiter (Tabelle 21-2) oder Potentialausgleichsleiter (Tabelle 21-3-1) dimensionieren.
- **15.1.2** Bei Isolierstücken an Rohrleitungen: Anschluss jeweils gebäude-/anlagenseitig.
- **15.1.3** Mehrere leitfähige Teile dürfen örtlich über einen Potentialausgleichsleiter gemeinsam und mit der PAS verbunden werden (kein eigener Leiter pro Teil nötig; Bild 15-2).
- **15.1.4** Gasinnenleitung auch ohne Isolierstück einbeziehen; mit Isolierstück Anschluss nach Bild 15-1.
- **15.1.5** Teilweise nichtmetallene Gas-/Wasserleitungen brauchen an diesen Stellen keine Überbrückung — ausgenommen Wasserverbrauchsleitungen, die in Bestandsanlagen noch als Schutzerdungsleiter dienen; Überbrückungsleiter nach Tabelle 21-2.
- **Bild 15-1/15-2 Legende:** 1 Hauptsicherungskasten, 2 Erdungsleiter zum Anlagenerder, 3 Nullungsverbindung (soweit anwendbar), 4 Schutzerdungsleiter der Hauptleitung (PE), 5 Haupterdungsschiene (PAS) bzw. Haupterdungsklemme, 6 PA-Leiter Antennen-/Photovoltaikanlagen, 7 Funktions-/Überspannungs-Schutzerdungsleitungen Informationstechnik, 8 PA-Leiter zur Blitzschutzanlage, 9 leitf. Wasserverbrauchsleitung, 10 leitf. Gasinnenleitung, 11 Isolierstück, 12 Wasserzähler, 13 leitf. Heizungsrohre, 14 leitf. Abwasserrohr, 15 Anlagenerder, 16 Isolierstück oder nichtleitende Wasserleitung.
- **15.2 Zusätzlicher Potentialausgleich** Zusätzlich zum Hauptpotentialausgleich bei besonderer Gefährdung (z. B. **Netznennspannung > 250 V gegen Erde**, erschwerte Umgebungsbedingungen, Beeinflussung). In mehrstöckigen Gebäuden mit vernetzter Informationstechnik: zusätzlicher Potentialausgleich an der Hauptverteilung **jedes Stockwerks** empfohlen (zur Minimierung von Potentialunterschieden am PE).
  - **15.2.1** Einzubeziehen: alle gleichzeitig berührbaren leitfähigen Teile ortsfester Betriebsmittel, Schutzerdungsleiteranschlüsse, alle fremden leitfähigen Teile, Stahlbeton-Bewehrung (soweit durchführbar).
  - **15.2.2** Ausführung mit Potentialausgleichsleiter gemäß 21.5 (Tabelle 21-3-2).

### 16 Verwenden von Gas-/Wasserleitungen als Erder etc.
- **16.1** Unabhängig vom Hauptpotentialausgleich (15.1) dürfen Gas- und Wasserleitungen **NICHT** als Schutzerdungsleiter, Erdungsleiter, Potentialausgleichsleiter oder Erder verwendet werden; ihre natürliche Wirksamkeit (Erderwirksamkeit, Stromtragfähigkeit) nicht in Dimensionierung berücksichtigen.
- **16.2** Bei wesentlichen Erweiterungen/Änderungen in Bestandsanlagen: Fehlerschutz ohne Wasserrohrnetz/-verbrauchsleitungen sicherstellen.
- **16.3** Gleichstromanlagen: ÖVE-B 5 beachten.

### 17 Zusammenschluss von Erdungen in Nieder- und Hochspannungsanlagen
- Siehe ÖVE-EH 41 bzw. ÖVE/ÖNORM E 8383.

### 18 Schutz gegen transiente Überspannungen (Überspannungs-Schutzeinrichtungen, ÜSE)
- Schutz gegen **indirekte** Blitzeinwirkungen (leitungsgebunden über das NS-Verteilungsnetz); direkte Blitzeinwirkungen: ÖVE-E 49 bzw. ENV 61024; informationstechnische Anlagen: ÖVE-F 1 Teil 7.
- **18.1** Haupt- und zusätzlicher Potentialausgleich: siehe Abschnitt 15. **18.2** bleibt frei.
- **18.3.1 ÜSE im Verteilungsnetz** Alle aktiven Leiter schützen. Schaltung:
  - TN-C: zwischen jedem Außenleiter und PEN-Leiter
  - TN-S/TT: a) zwischen jedem aktiven Leiter (Außen- + Neutralleiter) und PE-Leiter/geeignetem Betriebserder ODER b) zwischen jedem Außenleiter und Neutralleiter sowie Neutralleiter–PE-Leiter/Betriebserder
  - IT: zwischen jedem aktiven Leiter und Schutzerder
  - Geerdeter Neutralleiter an/nahe Einbaustelle → ÜSE für Neutralleiter entfällt.
  - Bemessungsspannung: TN-C **≥ 1,45-fache** Leiter-Erde-Spannung; TN-S/TT (1a) (√3-fache) Leiter-Erde-Spannung; TN-S/TT (1b) Außenleiter **≥ 1,45-fach**, N–PE **≥ 1,1-fach** Leiter-Erde-Spannung; IT **≥ 1,1-fache** Außenleiterspannung. Zusätzliche ÜSE zwischen zwei Außenleitern mit ≥ 1,1-facher Außenleiterspannung zulässig.
- **18.3.1.1 Freileitungsnetze** ÜSE Ableiterklasse A bzw. Prüfklasse I oder II (ÖVE-SN 60 / IEC 61643-1). Abstände der Einbaustellen **≤ 1000 m**; bei erhöhter/hoher Blitzdichte (Anhang A) im Mittel auf **500 m** verringern; Einbau bei Betriebserdungen und Transformatorstationen empfohlen.
- **18.3.1.2 Gemischte Kabel-/Freileitungsnetze**
  - .2.1 Netze mit geringer Kabelausdehnung: ÜSE mind. Ableiterklasse C / Prüfklasse II (ÖVE-SN 60 Teil 4 / IEC 61643-1); Freileitungs-Abstände im Mittel **≤ 1000 m**, bei erhöhter/hoher Blitzdichte **≤ 500 m**; zusätzlich bei Transformatorstationen und Kabelendverschlüssen.
  - .2.2 Andere Netze in Gegenden erhöhter/hoher Blitzdichte: mind. Klasse C/Prüfklasse II; Freileitungs-Abstände im Mittel **≤ 500 m**; zusätzlich bei Transformatorstationen und Kabelendverschlüssen.
  - .2.3 Sonst: Einbau im Kabelabschnitt empfohlen.
- **18.3.1.3 Kabelnetze**
  - .3.1 Geringe Ausdehnung (Gesamtlänge **< 500 m**) und Gebiete geringer Bodenleitfähigkeit: bei erhöhter/hoher Blitzdichte mind. Klasse C/Prüfklasse II bei Transformatorstationen und Kabelendverschlüssen.
  - .3.2 Andere Kabelnetze: Einbau empfohlen.
- **18.3.2 ÜSE in Verbraucheranlagen** (Mindestanforderungen):
  - (1) Anlagen aus Netzen nach 18.3.1.1/.2/.3.1 sowie Gebäude mit äußerem Blitzschutz (ÖVE-E 49/ENV 61024): mind. ÜSE im Bereich der Hauptleitung.
  - (2) Mind. Ableiterklasse C / Prüfklasse II (ÖVE-SN 60 Teil 4 / IEC 61643-1), **Nennableitstoßstrom ≥ 5 kA (8/20 µs)**, **Schutzpegel ≤ 2000 V**.
  - (3) Bei Schaltung (1b): Nennableitstoßstrom N–PAS/PE-Schiene = Summe der Nennableitstoßströme der Außenleiter-ÜSE **plus 5 kA**. → **einphasig mind. 10 kA**, **3-phasig mind. 20 kA**.
  - (4) Ableiter so nahe wie möglich bei PAS/PE-Schiene.
  - ANMERKUNG: Nähe von Hochspannungserdungen/Bahnschienen kann höhere Mindestbemessungsspannungen erfordern.
- **18.3.2.1 Nullung (Abschnitt 10)** Schaltung je nach getrennt/nicht getrennt geführtem Schutzerdungsleiter (Bilder 18-1 bis 18-4):
  - ohne getrennten PE: zwischen jedem Außenleiter und PAS/PEN-Leiter/PEN-Schiene (Bild 18-1)
  - mit getrenntem PE: a) jeden Außenleiter + N gegen PAS/PE-Schiene (Bild 18-3) oder b) jeden Außenleiter–N sowie N–PAS/PE-Schiene (Bild 18-4)
  - Bei hergestellter Nullungsverbindung an/nahe Einbaustelle (Bild 18-2) entfällt ÜSE für N.
  - Bemessungsspannung **≥ 1,45-fache** Leiter-Erde-Spannung; zusätzliche ÜSE zwischen Außenleitern ≥ 1,1-fache Außenleiterspannung zulässig.
- **18.3.2.2 Fehlerstrom-Schutzschaltung (12.2)** Schaltung (1a) jeden Außenleiter + ggf. N gegen PAS/PE (Bild 18-5) oder (1b) jeden Außenleiter–N sowie N–PAS/PE (Bild 18-6). Bei mit PAS/PE verbundenem N (Sonderfall 14.2.3.1) entfällt ÜSE für N.
  - Bemessungsspannung (1a) ≥ 1,1-fach, (1b) Außenleiter ≥ 1,45-fach / N–PE ≥ 1,1-fach Leiter-Erde-Spannung.
  - (3) Bei ÜSE (1a) vor der FI: Bedingung **R_A ≤ U_FL / I_A** (R_A = Erdungswiderstand Anlagenerder, U_FL = vereinbarter Grenzwert Fehlerspannung, I_A = Ausschaltstrom vorgeschalteter/integrierter Überstrom-Schutzeinrichtung, Tabelle 10-1). Wenn nicht erfüllt: Ableitertrennschalter in Zuleitung/Erdungsleitung einbauen (Bild 18-5) oder nach (1b) installieren (Bild 18-6). Trennschalter-Stoßstromfestigkeit ≥ Summe der Nennableitstoßströme (einphasig mind. 10 kA, 3-phasig mind. 20 kA). Weiter: **R_A ≤ U_FL / I_FN** (I_FN = Auslösenennstrom Ableitertrennschalter).
  - ÜSE Ableiterklasse B / Prüfklasse I nach FI **nicht zulässig** (außer Überspannungen von Lastseite). Klasse C / Prüfklasse II nach FI nur zulässig, wenn vor FI bereits ÜSE nach 18.3.2 (2)/(3) installiert oder Überspannungen lastseitig zu erwarten (Bild 18-7) → dann FI **Bauart S oder Bauart G**.
  - (4)/(5): ÜSE gemeinsam mit vorgeschalteten Schutzeinrichtungen (AT-Schalter, Vorsicherung) nach IEC 61643-1:1998-02 Abschnitt 7.7.4, ohne Gefährdung von Personen/Sachwerten.
- **18.3.2.3 Isolationsüberwachung (Abschnitt 11) / IT-Netze ≤ 250 V** Schaltung (1a) jeden Außenleiter + ggf. N gegen PAS/PE (Bild 18-8) oder (1b) wie Bild 18-6. Bemessungsspannung (1a) ≥ 1,1-fache Außenleiterspannung, (1b) Außenleiter ≥ 1,45-fach / N–PE ≥ 1,1-fache Außenleiter-Neutralleiter-Spannung.
- **18.3.2.4.1 Kombination mit FI** Bei ÜSE Klasse C / Prüfklasse II oder III nach FI muss FI **Bauart G oder S** (ÖVE-SN 50 / ÖVE EN 61008 Reihe). Fehlauslösungen bei Stoßströmen **> 3 kA (Bauart G)** bzw. **> 5 kA (Bauart S)**; auch beim Defektwerden eines Ableiters löst FI aus.
- **18.3.2.4.2 Anschlussleitungen** Zu-/Erdungsleitungen möglichst kurz (**vorzugsweise ≤ 0,5 m**), schleifenfrei/impedanzarm (Bild 18-9); sonst V-förmiger Anschluss mit möglichst großem Abstand (Bild 18-10). Ableitung zur kürzeren Strecke (PAS oder PE/PEN-Schiene). **Mindestquerschnitt 4 mm² Kupfer** (sonst nach max. Kurzschlussstrom); Überlastschutz darf entfallen.
- **18.3.2.4.3 Schutz bei Überstrom** Max. Kurzschlussstrom und Vorsicherung nicht größer als Herstellerangabe; ÜSE **ohne eingebaute/vorgeschaltete Kurzschluss-Schutzeinrichtung nicht zulässig** (gilt nicht für ÜSE zwischen N und PAS/PE).
- **18.3.2.4.4 Einbau** ÜSE nicht ohne Zusatzmaßnahmen (ÖVE-EX 65) in brand-/explosionsgefährdeten Räumen; von leicht/normal brennbaren Materialien (ÖNORM B 3800) mind. brandhemmend trennen. In Laien-zugänglichen Verteilern Kennmelder durch Laien kontrollierbar. Wenn Isolationsmessung mit installierten ÜSE nicht möglich: Hinweisschild „Bei Isolationswiderstands-Messungen Überspannungs-Schutzeinrichtungen trennen oder ansteigende Prüfspannung verwenden!" deutlich sichtbar im Verteiler.
- **18.3.2.4.5/.6** Hersteller-Angaben zur Koordination der ÜSE beachten; max. Ableitvermögen der vorgeschalteten Überstrom-Schutzeinrichtungen ist begrenzt.
- **18.4/18.5** Leitungsverlegung/Leitungstragwerke in/auf Gebäuden mit Blitzschutz: zusätzlich zu ÖVE-EN 1 Teil 3 → ÖVE-E 49 / ENV 61024 und (Tragwerke) ÖVE-L 1.

### 19 Isolationswiderstand
- Ohne Verbrauchsgeräte, zwischen zwei Überstrom-Schutzeinrichtungen oder hinter der letzten: mind. **0,5 MΩ** bei Nennspannung bis 500 V, **1 MΩ** bei Nennspannung bis 1000 V, gemessen mit Gleichspannung.

### 20 Erdung
- **20.1 Einteilung der Erder:**
  - Nach Lage: **Horizontalerder** (waagrecht, geringe Tiefe; Strahlen-, Ring-, Maschenerder oder Kombination), **Vertikalerder** (lotrecht, größere Tiefe).
  - Nach Form/Profil: Banderder, Runderder, Rohrerder, Staberder, Plattenerder, Seilerder.
  - **Fundamenterder** (in Beton eingebettet, großflächig leitend mit Erde), **natürliche Erder** (Metallteile mit ursprünglich anderem Zweck: Rohrleitungen, Spundwände, Betonbewehrung, Stahlteile), **Kabel mit Erderwirkung** (sinngemäß natürliche Erder), **Steuererder** (Potentialsteuerung).
- **20.2.1 Spezifischer Erdwiderstand (Tabelle 20-1, Richtwerte ρ_E in Ω·m):**
  - Moorboden: 5–40
  - Lehm, Ton, Humus: 20–200
  - Sand: 200–2 500
  - Kies: 2 000–3 000
  - verwittertes Gestein: meist unter 1 000
  - Granit, Grauwacke, Hartgestein feucht: 2 000–3 000
  - Bei Fundamenterdern darf gerechnet werden, als ob der Leiter im umgebenden Erdreich läge.
- **20.2.2 Ausbreitungswiderstand** hängt von ρ_E, Abmessungen, Anordnung ab — v. a. von der Länge (weniger Querschnitt). Maschenerder näherungsweise **R_E = ρ_E / (2·D)** (D = Durchmesser eines flächengleichen Kreises). Zugängige Messstellen für getrennte Einzelerder-Messungen vorsehen; aus Einzelmessungen nicht ohne weiteres auf Gesamterdungswiderstand schließbar.
- **20.3 Werkstoffe/Mindestabmessungen:**
  - **20.3.1** Werkstoff Stahl oder Kupfer (sonst ÖVE-E 40); Korrosion durch Elementbildung beachten (Spannungsreihe). Fundamenterder und Kupfererder ≈ gleiches elektrochemisches Potential.
  - **20.3.2** Mindestabmessungen nach Tabelle 20-2.
  - **20.3.3** Reine Potentialausgleichs-Erder: feuerverzinkter/kupferplattierter Stahl **16 mm²**, Kupfer **10 mm²**. Bei Korrosionsgefahr/unverzinktem Stahl ca. **1,5-facher** Querschnitt empfohlen.
- **Tabelle 20-2 (Werkstoffe für Erder, Mindestmaße bzgl. Korrosion; Beschichtung Dicke Mindest-/Mittelwert µm):**
  - Stahl feuerverzinkt (auch Betoneinbettung): Band 90 mm²/3 mm Dicke, 60/70 µm; Kreuzprofil o. dgl. 90 mm²/3 mm, 60/70 µm; Rund Vertikalerder 20 mm Ø, 60/70 µm; Rund Horizontalerder 10 mm Ø (Fernmelde-Kabelbegleiterdung 8 mm), 40/50 µm.
  - Edelstahl V4A korrosionsbeständig: Band 90 mm²/3 mm; Rund Vertikalerder 20 mm Ø; Rund Horizontalerder 10 mm Ø (keine Beschichtung).
  - Kupfer blank: Band 50 mm²/2 mm; Rund Horizontalerder 7 mm Ø; Seil Einzeldrähte 1,8 mm / Querschnitt 25 mm².
  - Bevorzugte Bandquerschnitte (in Ringen): 30×3 mm, 40×3 mm, 40×4 mm.
- **20.4 Natürliche Erder** dürfen verwendet werden, wenn Ausbau/Austausch gegen nichtleitende Teile ausgeschlossen oder gemeldet wird und sie gut leitend verbunden sind (Nachweis z. B. durch Widerstandsmessung). I. d. R. als gute Erder i. S. v. 14.2. Kunststofffreie, direkt im Erdreich verlegte Kabel-Metallmäntel zulässig, wenn Muffen-Verbindungen mind. leitwertgleich zum Mantel.
- **20.5 Anordnung/Ausführung:**
  - **20.5.1** Örtliche Verhältnisse, Bodenbeschaffenheit, zulässiger Ausbreitungswiderstand, korrosive Beeinflussung verschiedener Erdermaterialien beachten. Erder einschlämmen (nichtbindig) / stampfen (bindig).
  - **20.5.2** Horizontalerder frostfrei, i. d. R. Mindesttiefe **0,8 m**; Strahlenerder-Winkel zwischen benachbarten Strahlen **≥ 60°**.
  - **20.5.3** Vertikalerder lotrecht; bei mehreren gegenseitiger Abstand **≥ wirksame Länge eines Einzelerders**.
  - **20.5.4 Fundamenterder** (ÖNORMEN B 5432, E 2790): verzinkter/blanker Bandstahl mind. **30×3 mm** oder Rundstahl mind. **10 mm Ø**. Im Beton blank, außerhalb über Erde mind. feuerverzinkt, unterirdische Ausleitung nur Kupfer; Bewehrungsstähle/einbetonierte Stahlteile dürfen einbezogen werden (Schweißen nur im Einvernehmen mit Stahlbeton-Ersteller). Anordnung: (1) geschlossener Ring im Fundament der Umfassungsmauer; (2) Punkte > **5 m** vom Erder → weitere Verbindungen einlegen; (3) Dehnungsfugen außerhalb Beton korrosionsgeschützt verbinden. Mind. eine Anschlussfahne (weitere für Blitzschutz/Erweiterungen). Erdreich-Ausleitungen aus Kupfer oder kunststoffummantelt, mind. **0,25 m oder halbe Betonkörperdicke** in den Beton reichend.
  - **20.5.5** Erder durch Schweiß-/Schraub-/Klemmverbindung elektrisch leitend und mechanisch fest verbinden; Einzelschraube/Anschlussschelle an Rohrerdern mind. **Gewinde M 10**.

### 21 Erdungsleitungen, Schutzerdungsleiter, Potentialausgleichsleiter
- **21.1 Erdungsleitungen** Mindestquerschnitte nach Tabelle 21-1; Einzelschraube mind. Gewinde M 10 (an Seilen auch Hülsen-/Kerb-/Press-/Schraubverbinder); über Erde sichtbar/zugänglich verlegen, gegen mechanische/chemische Zerstörung schützen; **Schalter oder werkzeuglos lösbare Verbindungen unzulässig**. Betriebserder im Handbereich so befestigen, dass er nicht umfasst werden kann.
- **Tabelle 21-1 (Mindestquerschnitte Erdungsleitungen):**
  - Isoliert, mechanisch geschützt (YY/Rohr): wie 21.3 gefordert. Mechanisch ungeschützt: mind. **4 mm² Cu**, zulässige Begrenzung 16 mm² Cu; Aluminium unzulässig.
  - Blank, mechanisch ungeschützt: Aluminium unzulässig; **Kupfer 25 mm²**; **Eisen feuerverzinkt 50 mm²** (jedoch nicht im Einflussbereich von / in Kombination mit Fundament-/Kupfererdern).
- **21.2 Haupterdungsschiene (PAS) / Haupterdungsklemme** Abtrennvorrichtungen zugänglich, zweckmäßig mit PAS/Haupterdungsklemme kombiniert (für Widerstandsmessung), nur mit Werkzeug lösbar; ausreichende mechanische Festigkeit, dauerhafte elektrische Verbindung.
- **21.3 Schutzerdungsleiter:**
  - **Tabelle 21-2 (Zuordnung Schutzerdungsleiter/PEN zum Außenleiter; Querschnitt A der Außenleiter):**
    - A ≤ 16 mm² → A_PE(N),min = A
    - 16 < A ≤ 35 mm² → 16 mm²
    - A > 35 mm² → A/2
    - Gilt nur bei gleichem Metall; sonst Querschnitt so, dass gleiche Leitfähigkeit. Nicht genormte A/2 → nächstgrößerer Nennquerschnitt. (Bestand Kabel 3×16+10: PEN 10 mm² zulässig.)
  - **21.3.1.1** Auswahl i. allg. nach Tabelle 21-2; besondere Anforderungen (Leistungselektronik) → ÖVE EN 50178; Grenzfälle Berechnung nach HD 384.5.54 S1. In genullten Anlagen Verringerung unter **halben Außenleiterquerschnitt nicht zulässig** (außer Betriebsmittelbestimmungen, z. B. ÖVE EN 60439).
  - **21.3.1.2** Schutzerdungsleiter nicht in gemeinsamer Umhüllung mit Außen-/Neutralleiter mind.: **2,5 mm² Cu** (mechanisch geschützt), **4 mm² Cu** (ungeschützt), **50 mm² Stahl** (Rundstahl ≥ 8 mm Ø, Bandstahl ≥ 3 mm Dicke).
  - **21.3.1.3** Gemeinsamer Schutzerdungsleiter mehrerer Stromkreise: nach größtem Außenleiterquerschnitt.
  - **21.3.2.1** Zulässige Schutzerdungsleiter: Leiter in mehradrigen Kabeln; isolierte/blanke Leiter in gemeinsamer Umhüllung mit Außen-/Neutralleiter (Installationsrohre/-kanäle); fest verlegte blanke/isolierte Leiter; metallene Umhüllungen (Mäntel, Schirme, konzentrische Leiter, Installationsrohre/-kanäle, siehe 21.3.2.3); Profilschienen (auch mit Klemmen/Geräten); Gehäuse/Bauteile elektrischer Betriebsmittel (bestimmungsgemäß, siehe 21.3.2.2). **Fremde leitfähige Teile NICHT** zulässig.
  - **21.3.2.2** Metallgehäuse/Konstruktionsteile von Schaltgeräte-Kombinationen / metallgekapselte Stromschienensysteme zulässig, wenn: (1) durchgehende Verbindung gegen Verschlechterung gesichert, Ausbau einzelner Teile darf PE-Bahn nicht unterbrechen, (2) Leitfähigkeit ≥ Tabelle 21-2, (3) andere PE-Leiter an jeder vorgesehenen Stelle anschließbar. Anschlussstellen mit Schutzleiter-Zeichen nach ÖNORM E 1357 kennzeichnen.
  - **21.3.2.3** Metallene Umhüllungen von Kabeln/Leitungen (insb. mineralisolierte Leitungen, Installationsrohre/-kanäle) als PE des entsprechenden Stromkreises, wenn 21.3.2.2 (1)+(2) erfüllt.
  - **21.3.3** Verbindungen gegen mechanische/chemische/elektrochemische Verschlechterung geschützt; Befestigungs-/Verbindungsschrauben nicht für PE-Anschluss; zur Besichtigung/Prüfung zugänglich (außer vergossen); **keine Schalteinrichtung im PE** (Trennstellen nur werkzeuglösbar für Prüfung); Körper von Betriebsmitteln nicht als PE für andere Betriebsmittel (außer 21.3.2.2); gegen Lockern gesichert (ÖVE EN 60999).
- **21.4 PEN-Leiter:**
  - **21.4.1** Bei Nullung (Abschnitt 10), fester Verlegung und Querschnitt **≥ 10 mm² Cu bzw. 16 mm² Al** ein einziger PEN-Leiter zulässig. Bei konzentrischem Leiter mit doppelten Verbindungen an allen Anschlussstellen min. **4 mm²**.
  - **21.4.2** N-, PEN- und PE-Leiter beliebig oft vom PEN abzweigbar; abgezweigter N-Leiter danach nicht mehr erden / mit PE verbinden.
  - **21.4.3** Profilschienen als PEN nur wenn nicht aus Stahl und nur Klemmen (keine Geräte) tragend.
  - **21.4.4** Fremde leitfähige Teile nicht als PEN.
  - **21.4.5** Bei vernetzter Informationstechnik: Verzicht auf PEN auch > 10 mm² Cu / 16 mm² Al empfohlen (getrennt geführter PE, gegen Ausgleichsströme).
- **21.5 Potentialausgleichsleiter:**
  - **Tabelle 21-3-1 (Hauptpotentialausgleich):** normal **0,5 × Querschnitt des größten PE-Leiters der Anlage**; mindestens **10 mm² Kupfer**; zulässige Begrenzung **25 mm² Kupfer** (oder gleicher Leitwert bei anderen Werkstoffen). Größter PE-Leiter = vom Hauptverteiler abgehender Schutzerdungsleiter mit größtem Querschnitt (bzw. Schutzerdungsleiter der Hauptleitung, falls kein Hauptverteiler; zentrale Zähleranordnung gilt als Hauptverteiler).
  - **Tabelle 21-3-2 (zusätzlicher Potentialausgleich):** zwischen zwei Körpern **1 × Querschnitt des kleineren PE-Leiters**; zwischen Körper und fremdem leitfähigem Teil **0,5 × Querschnitt des PE-Leiters**; mindestens **2,5 mm² Cu** (mit mechanischem Schutz) bzw. **4 mm² Cu** (ohne mechanischen Schutz).
  - **21.5.2** Anschluss an Rohrleitungen: Rohrschellen/Anschlussfahnen/Kontaktbolzen/Hartlöt-/Schweißverbindung; Rohrschellen-/Spannbandschrauben mind. **M 6**, Einzelschraube mind. **M 10**; zugänglich.
  - **21.5.3** Korrosionsschutz bei Erde/feucht/nass/stark korrosiv (Stallungen): Vergussmasse + Korrosionsschutzbinde, Korrosionsschutzbinde mit unverrottbarem Trägergewebe + Kunststofffolie, oder Schrumpfschläuche; in feuchten/nassen Räumen auch Anstriche/Beschichtungen/korrosionsbeständige Werkstoffe.
- **21.6 Kennzeichnung:** Isolierte PE- und PEN-Leiter durchgehend **grün-gelb** (ÖVE-EN 1 Teil 3 § 40); zulässig auch für Potentialausgleichs-/Erdungs-/Verbindungs-/Überbrückungsleiter; für andere Leiter grün-gelb **unzulässig**. Bei ein-/mehradrigen Kabeln ÖVE-EN 1 Teil 3 § 40. Kennzeichnung darf entfallen bei blanken Schutzerdungsleitern (wenn dauerhafte Kennzeichnung unmöglich), bei PE aus leitfähigen Konstruktionsteilen (21.3.2.2), bei Freileitungen.

### 22 Prüfung des Schutzes gegen elektrischen Schlag
- Wirksamkeit der Schutzmaßnahmen vor erster Inbetriebnahme prüfen (**Erstprüfung**); Anleitungen/Methoden in ÖVE/ÖNORM E 8001-6-61; sämtliche Bestimmungen einhalten; Messergebnisse dokumentieren.

### Anhang A (informativ): Blitzgefährdung in Österreich
- Erdblitzdichte N_g = mittlere Blitzeinschläge pro km² und Jahr. Abschätzung aus Gewittertagen (IEC): **N_g = 0,04 · T_d^1,25** (T_d = mittlere Gewittertage/Jahr, aus isokeraunischem Pegel).
- **Tabelle A.1 (T_d ↔ N_g ↔ Kategorie):** T_d < 20 → N_g < 1,7 → gering; 20 ≤ T_d < 25 → 1,7 ≤ N_g < 2,2 → mäßig; 25 ≤ T_d < 30 → 2,2 ≤ N_g < 2,8 → erhöht; 30 ≤ T_d < 35 → 2,8 ≤ N_g < 3,4 → hoch; T_d > 35 → N_g > 3,4 → sehr hoch.
- „Blitzgefährdet" = i. d. R. **> 2,2 Einschläge/km²/Jahr** (entspricht > 25 Gewittertage). Datenquelle ALDIS (seit 1992). Kontakt: ÖVE-ALDIS, Kahlenberger Str. 2b, 1190 Wien, Tel. +43-1-3180566, www.aldis.at.
- Tabelle A.2 (Beispiel Bezirk Murau, Steiermark, 10×9 km, 1992–1997): Werte zwischen 1,1 und 5,9 Einschläge/km²/Jahr; deutliche Abhängigkeit von Topographie (Täler gering, Anstieg mit Höhe); Bezirksmittel Murau 3,03.
- **Tabelle A.3 (Bezirks-Blitzdichten N_g, ALDIS 1992–1997; Auszug, Schwerpunkt erhöht/hoch):**
  - Kärnten: Hermagor 2,51 (erhöht), Klagenfurt-Land 2,16 (mäßig), Villach-Stadt 2,20 (mäßig), Villach-Land 2,73 (erhöht), Völkermarkt 2,41 (erhöht), Spittal/Drau 2,18 (mäßig), St. Veit/Glan 3,28 (hoch), Wolfsberg 2,97 (hoch), Feldkirchen 2,96 (hoch).
  - Salzburg: Hallein 2,61 (erhöht), St. Johann/Pongau 2,28 (erhöht), Tamsweg 2,37 (erhöht), Zell am See 2,08 (mäßig).
  - Niederösterreich: Wiener Neustadt 2,26 (erhöht), Neunkirchen 2,74 (erhöht); niedrigste St. Pölten-Stadt 0,78, St. Pölten-Land 0,86, Wien-Umgebung 0,90.
  - Steiermark (hoch): Graz-Stadt 2,98, Graz-Umgebung 3,18, Hartberg 2,81, Knittelfeld 2,83, Mürzzuschlag 3,07, Murau 3,03, Voitsberg 3,38, Weiz 3,04, Deutschlandsberg 2,80; (erhöht): Bruck/Mur 2,69, Judenburg 2,58, Leoben 2,44, Liezen 2,24; (mäßig): Feldbach 2,20, Fürstenfeld 2,16, Leibnitz 2,05, Radkersburg 2,05.
  - Oberösterreich: meist gering; Gmunden 2,05 (mäßig), Kirchdorf/Krems 1,87 (mäßig).
  - Tirol: Kitzbühel 2,74 (erhöht), Kufstein 2,24 (erhöht), Schwaz 2,06 (mäßig).
  - Burgenland: Mattersburg 2,17 (mäßig), Oberwart 2,01 (mäßig), Oberpullendorf 1,80 (mäßig).
  - Vorarlberg: durchwegs gering/mäßig (Dornbirn 1,88 mäßig).
  - Wien: Wien-Stadt 0,78 (gering).

### Anhang B (informativ): Literaturhinweise (Auswahl)
- ÖVE-E 40 (Korrosionsschutz Erder/erdverlegte Metallteile); ÖVE-EH 41 (Erdungen Wechselstrom > 1 kV); ÖVE-EN 1 Teil 4 § 97 (Fliegende Bauten/Wagen Schaustellerart); ÖVE-EN 2 Teil 1–8 (Sicherheitsstromversorgung Menschenansammlungen); ÖVE-EN 7 (Krankenhäuser/medizinisch genutzte Räume); ÖVE EN 50178 (Starkstrom mit elektronischen Betriebsmitteln); ÖVE EN 60034 Reihe (Drehende elektrische Maschinen); ÖVE EN 60065 (netzbetriebene elektronische Geräte Hausgebrauch); ÖVE EN 60335 Reihe (Sicherheit Hausgeräte); ÖVE EN 60439-4 (NS-Schaltgerätekombinationen, Baustromverteiler BV); ÖVE EN 60519 Reihe (Elektrowärmeanlagen); ÖVE EN 60598 Reihe (Leuchten); ÖVE EN 60601 Reihe (Medizinische elektrische Geräte); ÖVE EN 60999 (Schraub-/schraubenlose Klemmstellen Kupferleiter); ÖVE EN 61557-8 (Isolationsüberwachungsgeräte IT-Netze AC 1 kV / DC 1,5 kV); ÖVE-EX 65 (Ex-Bereiche); ÖVE-F 1 Teil 7 (Überspannungsschutz Fernmelde); ÖVE HD 625.1 S1 (Isolationskoordination NS Teil 1); ÖVE-K 40 (Gummi-Energieleitungen); ÖVE-K 41 (PVC-Energieleitungen); ÖNORM B 3800 Reihe (Brandverhalten Baustoffe/Bauteile); ÖNORM F 1000 Reihe (Feuerwehr-/Brandschutzwesen); ISO/IEC-Guide 51 (Safety aspects in standards).
