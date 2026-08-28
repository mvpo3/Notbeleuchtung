# Fachinfo_IS02_Anwendung_RCD_Stand_2021-07__UEberblick_ueber_die_Anwendung_von_Fehlerstrom-Schutzeinrichtungen__in_Niederspannungsanlagen_gemaess_den_in_OEsterreich_geltenden_anerkannten_Regeln_der_Technik__ — Teil 0
> Quelle: Fachinfo_IS02_Anwendung_RCD_Stand_2021-07__UEberblick_ueber_die_Anwendung_von_Fehlerstrom-Schutzeinrichtungen__in_Niederspannungsanlagen_gemaess_den_in_OEsterreich_geltenden_anerkannten_Regeln_der_Technik__ (normen) · Seiten 1-19.

OVE-Fachinformation **IS02**, Ausgabe **2021-07-01** (Ersatz für Ausgabe 2013-10), zuständig OVE/TSK IS23E – Schutzschalter. Sie gibt eine anwendungsbezogene Übersicht über die in Österreich genormten und am Markt verfügbaren Fehlerstrom-Schutzeinrichtungen (RCD/RCCB) und deren normgerechte Anwendung. Eingearbeitet sind die Änderungen aus OVE E 8101:2019-01-01, OVE E 8101/AC1:2019-05-01, OVE E 8601:2018 und ÖVE/ÖNORM E 8603:2015. ICS 29.020; 29.120; 29.130; 29.240.01; 91.140.50. Dieser Teil deckt das vollständige Dokument ab (Seiten 1-19), inkl. der großen Anwendungs-Übersichtstabelle (Tabelle 6) und der Literaturhinweise.

## Inhalt

### 1 Ausgangssituation
- In den letzten Jahren wurden wesentliche internationale, europäische und nationale anerkannte Regeln der Technik für Fehlerstrom-Schutzeinrichtungen (RCCBs) aktualisiert bzw. neu erstellt.
- Ziel der Fachinformation: dem Praktiker eine anwendungsbezogene Übersicht über die in einschlägigen Normen enthaltenen und am Markt erhältlichen Ausführungsformen von RCDs zu geben.

### 2.1 Sensitivität gegenüber Fehlerströmen — Typen (Tabelle 1)
Genormte RCD-Ausführungen nach Sensitivität gegenüber verschiedenen Kurvenformen des Fehlerstroms:

| Typ | Beschreibung | Norm |
|-----|--------------|------|
| **AC** | Wechselstromsensitiv. Sensitiv für sinusförmige Wechselfehlerströme (50/60 Hz), plötzlich oder langsam ansteigend. | OVE EN 61008-1, OVE EN 61009-1 |
| **A** | Pulsstromsensitiv. Sensitiv für sinusförmige Wechselfehlerströme und pulsierende Gleichfehlerströme (50/60 Hz), plötzlich oder langsam ansteigend. | OVE EN 61008-1, OVE EN 61009-1 |
| **F** | Sensitiv für sinusförmige Wechselfehlerströme, pulsierende Gleichfehlerströme (50/60 Hz) **mit überlagerten glatten Gleichfehlerströmen von max. 10 mA**, sowie für zusammengesetzte Fehlerströme, plötzlich oder langsam ansteigend. | ÖVE/ÖNORM EN 62423 |
| **B** | Sensitiv für sinusförmige Wechselfehlerströme, pulsierende sowie **glatte Gleichfehlerströme** und Wechselfehlerströme mit **Frequenzen bis 1 000 Hz**, plötzlich oder langsam ansteigend. | ÖVE/ÖNORM EN 62423 |

- Diese Typen erfassen die in Tabelle 2 dargestellten Kurvenformen von Fehlerströmen.

### 2.1 (Forts.) Kurvenformen von Fehlerströmen — Auswahlhilfe (Tabelle 2, Schaltungsarten 1-13)
Zuordnung von Fehlerstrom-Kurvenformen zu RCD-Typen (Quelle: OVE E 8101:2019-01-01). Schaltungsarten:
1. Phasenanschnittssteuerung
2. Paketsteuerung (Burst-Steuerung)
3. Einphasig
4. Zweipuls-Brückenschaltung
5. Zweipuls-Brückenschaltung, halbgesteuert
6. Frequenzinverter mit Zweipuls-Brückenschaltung
7. Einphasig mit Glättung
8. Frequenzinverter mit Zweipuls-Brückenschaltung und PFC (PFC … Power Factor Correction)
9. Zweipuls-Brückenschaltung zwischen Außenleitern
10. Frequenzinverter mit Zweipuls-Brückenschaltung zwischen den Außenleitern
11. Drehstrom-Sternschaltung
12. Sechspuls-Brückenschaltung
13. Frequenzinverter mit Sechspuls-Brückenschaltung

- Anmerkung zu IF2 (bei Schaltungsarten 6, 8, 10, 13): Die tatsächliche Frequenz kann von der dargestellten Frequenz von 50 Hz deutlich abweichen.
- Zeilen 8 und 10 enthalten korrigierte Darstellungen, da in OVE E 8101:2019-01-01 Anhang 531.A sowie HD/IEC 60364 Series darstellungstechnische Unklarheiten entdeckt wurden.
- Farbkennzeichnung in der Tabelle: **Grün** = RCD kann Fehlerströme dieses Typs erfassen; **Rot** = RCD kann Fehlerströme dieses Typs nicht erfassen.

### 2.2 Bauformen von Fehlerstrom-Schutzeinrichtungen (Tabelle 3)
Neben der „üblichen Bauform" existieren folgende (Sonder-)Bauformen:

| Bauform | Beschreibung | Kennzeichnung |
|---------|--------------|---------------|
| **übliche** | Bauform ohne Zeitverzögerung gemäß OVE EN 61008-1. RCD ohne definierte Nichtauslösezeit. | keine |
| **G** | Kurzzeitverzögert gemäß OVE E 8601. Verhindert mit hoher Wahrscheinlichkeit ungewolltes Auslösen bei Überspannungen durch Einhalten einer **Nichtauslösezeit von 0,01 s**. | G |
| **S** | Selektiv gemäß OVE EN 61008-1. RCD mit Zeitverzögerung, unterschreitet je nach Fehlerstromwert einen festgelegten Wert der Nichtauslösezeit nicht und schaltet selektiv mit nachgeschalteten RCDs. **Kürzeste Nichtauslösezeit 0,04 s.** | S |
| **M** | Selektiv gemäß ÖVE/ÖNORM E 8603. RCD mit Zeitverzögerung, **Nennströme über 32 A**, selektiv mit elektromagnetischen Schnellauslösern von Leitungsschutzschaltern nach ÖVE/ÖNORM EN 60898 Reihe und mit RCDs der Bauformen „allgemein", G und „S" gemäß OVE EN 61008-1, OVE E 8601. **Kürzeste Nichtauslösezeit 0,2 s.** | M |

### 2.3 Überlast- und Kurzschlussschutz gemäß OVE E 8101
- Quellen für die Festlegung: ÖVE-EN 1, Teil 1b/1995 § 12.12; ÖVE/ÖNORM E 8001-1:2010, Abschnitt 12.1; OVE E 8101:2019, Unterabschnitte **536.4.2.4** und **536.4.3.2**.
- Fehlerstromschutzschalter (RCCB) sind **gegen Kurzschluss** und **gegen thermische Überlastung** zu schützen.
- Sowohl Bemessungswert für Überlastschutz als auch für Kurzschlussschutz (z.B. Vorsicherung) sind bei der Installation zu beachten.
- Fehlt die Herstellerangabe des höchstzulässigen Nennstroms der Überlast-Schutzeinrichtung, gilt: Bemessungsstrom IN der RCD = deren dauernd zulässiger Überstrom IZ (**IN = IZ**). Es ist sicherzustellen, dass IN nicht über die konventionelle Ausschaltzeit der Überstrom-Schutzeinrichtung hinaus auf Dauer fließen kann.
- **Dimensionierungsregel** vorgeschaltete Überstrom-Schutzeinrichtung: **IN (RCD) ≥ I2 (Überstrom-Schutzeinrichtung)**
  - IN = Bemessungsstrom der RCD; I2 = konventioneller Auslösestrom.
  - I2 = jener Strom, der mit Sicherheit zur Auslösung führt (Auslösestrom bei Leistungsschaltern bzw. großer Prüfstrom bei Sicherungen und Leitungsschutzschaltern).
  - Bei Schmelzsicherungen Klasse **gG** entspricht I2 dem konventionellen Auslösestrom If. Für Schmelzsicherungen der Nennstromstärken **25 A bis 400 A**: **If = 1,6 · IN(Schmelzsicherung)**.
  - Für Leitungsschutzschalter der Charakteristiken **B und C**: **I2 = 1,45 · IN(Leitungsschutzschalter)**.
  - Bei von gG abweichenden Kennlinien sind Herstellerangaben für den konventionellen Auslösestrom zu beachten.

#### Tabelle 4 — Maximale Vorsicherung (Klasse gL) für Überlastschutz, wenn keine Herstellerangabe besteht
| Nennstrom RCD (A) | Max. Vorsicherung Klasse gL für Überlastschutz (A, gerundet) |
|-------------------|--------------------------------------------------------------|
| 16 | 10 |
| 25 | 16 |
| 40 | 25 |
| 63 | 40 |
| 80 | 50 |
| 100 | 63 |

### 3 Einsatzbedingungen von Fehlerstrom-Schutzeinrichtungen (Tabelle 5)
- RCDs nach OVE EN 61008-1, ÖVE/ÖNORM EN 62423 und OVE EN 61009-1 sind für definierte Einsatzbedingungen entwickelt; nur dafür gelten die technischen Spezifikationen.
- Produkte nur unter definierten Bedingungen betreiben oder zusätzliche Maßnahmen am Einbauort (z.B. im Verteiler) treffen: Schaltschrankbelüftung, Heizung, Klimatisierung, notwendige Vorsicherung(en).

Einflussgrößen und definierte Einsatzbedingungen (Auswahl):
- **Umgebungstemperatur im Verteiler:** –5 °C bis +40 °C; bzw. –25 °C bis +40 °C (RCCBs für diesen Bereich müssen entsprechend beschriftet sein); **24-h-Mittelwert ≤ 35 °C**. (Nach Vereinbarung Hersteller/Anwender Werte außerhalb des Bereichs zulässig, wo härtere klimatische Bedingungen herrschen.)
- **Höhenlage:** nicht über **2000 m**.
- **Relative Feuchte (Höchstwert bei 40 °C):** **50 %**. Höhere Werte bei niedrigen Temperaturen zulässig (z.B. **90 % bei 20 °C**).
- **Lage:** wie vom Hersteller angegeben, mit Abweichung von **2°** in jeder Richtung. Gerät muss ohne funktionsbeeinträchtigende Verformung befestigt werden.
- **Frequenz:** Bezugswert **±5 %**.
- **Vorsicherung für Überlast:** lt. Herstellerangabe.
- **Vorsicherung für Kurzschluss:** lt. Herstellerangabe.
- **Elektromagnetische Umgebung:** Störfestigkeitsangaben lt. Hersteller, z.B. OVE EN IEC 61000-6-1:2019 (Wohnbereich, Geschäfts-/Gewerbebereiche, Kleinbetriebe) und/oder OVE EN IEC 61000-6-2:2019 (Industriebereiche).

### 4 Anwendung von Fehlerstrom-Schutzeinrichtungen — Überblick (Tabelle 6)
Schutzziel-Abkürzungen: **FS** = Fehlerschutz · **ZS** = Zusatzschutz · **BS** = Brandschutz.
Alle Normenreferenzen beziehen sich auf **OVE E 8101:2019**.

**Zeile 1 — Alle Bereiche bei Schutzmaßnahme Fehlerstrom-Schutzschaltung** (FS, Unterabschnitt 411.5.3):
- Auswahl von IΔN unter Einhaltung: **ZS ≤ U0 / (5 · IΔN)** und **ZS ≤ 100 Ω**, je nachdem welcher Wert kleiner ist.
- Bauform: übliche, S, G. Typ: AC, A, F, B.
- Auswahl der Bauart (übliche/S/G) nach Kriterium der Vermeidung unerwünschter/unbeabsichtigter Auslösungen, z.B. bei Anlagenteilen, deren unbeabsichtigtes Ausschalten mittelbare Personen- oder Sachschäden verursachen kann (z.B. Tiefkühltruhen, Intensivtierhaltung, Computer). Kriterium nach OVE E 8101:2019 Unterabschnitte 531.3.1.003.AT und 531.3.2.

**Zeile 2 — Alle Bereiche bei Schutzmaßnahme Nullung** (wenn Ausschaltbedingung mittels Überstrom-Schutzeinrichtungen nicht eingehalten werden kann) (FS, Unterabschnitt 411.4.5):
- Auswahl von IΔN unter Einhaltung: **ZS ≤ U0 / (5 · IΔN)**. IA = Fehlerstrom, der Abschaltung innerhalb 411.3.2.2 oder 411.3.2.3 bewirkt.
- Bauform: übliche, S, G, M. Typ: AC, A, F, B.
- Zusätzliche Bedingung: Überstromschutz jedes Stromkreises muss sichergestellt sein.

**Zeile 3 — Alle Stromkreise mit Steckdosen (Wechselspannung) bis Bemessungsstrom 20 A; Stromkreise für ortsveränderliche Betriebsmittel im Freien bis Bemessungsstrom 32 A** (ZS, Unterabschnitt 415.1):
- **IΔN ≤ 0,03 A**. Bauform: übliche, G. Typ: AC.
- Nur bei Nullung, Schutzerdung, Fehlerstrom-Schutzschaltung als Fehlerschutz-Maßnahme. Achtung: in besonderen Anlagen teils abweichende Bedingungen (siehe ab Zeile 5).

**Zeile 4 — Räume/Orte mit besonderem Brandrisiko (Merkmal BE2)** (BS, Unterabschnitt 422.3.9):
- Endstromkreise in solchen Räumen, die Betriebsmittel versorgen oder durchqueren, sind zu schützen.
- **422.3.9 a) TN-/TT-Systeme:** IΔN ≤ 0,3 A (Bauform übliche, S, G) **oder** IΔN ≤ 0,03 A (Bauform übliche, G). Typ: AC, A, F, B. RCD mit IΔN ≤ 0,3 A einsetzen; wo widerstandsbehaftete Fehler einen Brand entzünden können (z.B. Deckenheizungen mit Flächenheizelementen), muss **IΔN ≤ 0,03 A** betragen.
- **422.3.9 b) IT-Systeme:** IΔN ≤ 0,3 A (übliche, S, G) oder IΔN ≤ 0,03 A (übliche, G). Typ: AC, A, F, B. Als Alternative zu RCM oder IMD; beim Auftreten des zweiten Fehlers siehe Ausschaltzeiten Teil 4-41.

**Zeile 5 — Räume/Orte mit Badewanne und Dusche** (ZS, Unterabschnitt 701.415.1):
- **IΔN ≤ 0,03 A**. Bauform: übliche, G. Typ: AC. Für **alle** Stromkreise.
- Ausnahmen: Schutztrennung (wenn von jeder Sekundärwicklung des Trenntransformators gemäß ÖVE/ÖNORM EN 61558-2-4 nur ein Verbrauchsmittel versorgt wird); Schutz durch Kleinspannung SELV oder PELV; Isolations-Überwachungssystem.

**Zeile 6 — Schwimmbecken und Springbrunnen** (ZS, Unterabschnitte 702.410.3.101.2 und 702.410.3.101.3):
- **IΔN ≤ 0,03 A**. Bauform: übliche, G. Typ: AC.
- Schutz jedes Stromkreises in Bereichen 0 und 1 von Springbrunnen bei Nullung oder Fehlerstrom-Schutzschaltung.
- Schutz jedes Stromkreises im Bereich 2 von Schwimmbecken bei Nullung oder Fehlerstrom-Schutzschaltung.
- Schutz des versorgenden Stromkreises der SELV-Stromquelle, wenn diese im Bereich 2 angeordnet ist und SELV für Schaltgeräte, Steuergeräte und Steckdosen im Bereich 1 angewendet wird.
- Schutz von Stromkreisen für Schaltgeräte, Steuergeräte, Steckdosen im Bereich 2 bei Nullung oder Fehlerstrom-Schutzschaltung.
- Schutz des versorgenden Stromkreises der Stromquelle für Schutztrennung, wenn diese im Bereich 2 angeordnet ist.

**Zeile 7 — Räume und Kabinen mit Saunaheizgeräten** (ZS, Unterabschnitt 703.415.1):
- **IΔN ≤ 0,03 A**. Bauform: übliche, G. Typ: AC. Für alle Stromkreise.
- Ausnahmen: Schutztrennung; Schutz durch Kleinspannung SELV oder PELV.

**Zeile 8 — Baustellen:**
- **ZS (Unterabschnitt 704.410.3.101):** IΔN ≤ 0,03 A. Bauform übliche, G. Typ AC. Bei Nullung oder Fehlerstrom-Schutzschaltung: Endstromkreise bis einschließlich **32 A** zur Versorgung von Steckdosen jeder Art und andere Stromkreise mit fest angeschlossenen handgeführten Verbrauchsmitteln bis einschließlich 32 A.
- **FS (Unterabschnitt 704.411.3.2.1):** Bauform übliche, S, G. Typ AC, A, F, B. Alle Stromkreise bei Schutzmaßnahme Nullung.
- **BS (Unterabschnitt 704.411.3.2.1):** IΔN ≤ 0,5 A. Bauform übliche, S, G. Typ AC, A, F, B. Alle Endstromkreise mit Bemessungsströmen **über 32 A** zur Versorgung von Steckdosen jeder Art.

**Zeile 9 — Elektrische Anlagen von landwirtschaftlichen und gartenbaulichen Betriebsstätten:**
- **FS (705.411.1):** IΔN ≤ 0,3 A. Bauform übliche, S, G. Typ AC, A, F, B. Bei automatischer Abschaltung in allen Stromkreisen.
- **ZS (705.411.1; neue Nr. 705.415.1.001 AT):** IΔN ≤ 0,03 A. Bauform übliche, G. Typ AC. Bei automatischer Abschaltung in TN-/TT-Systemen in allen Endstromkreisen mit Steckdosen unabhängig vom Bemessungsstrom. Stromkreise mit hoher Verfügbarkeit sollten durch RCDs mit IΔN ≤ 0,03 A geschützt werden, die kurzzeitverzögert abschalten (z.B. Typ G).
- **FS (705.411.5.2):** Bauform übliche, S, G. Typ AC, A, F, B. Bei automatischer Abschaltung im TT-System müssen in allen Stromkreisen **zwei RCDs in Reihe** wirksam sein.
- **BS (705.422.7):** IΔN ≤ 0,3 A. Bauform übliche, M, S, G. Typ AC, A, F, B. Bei automatischer Abschaltung in TN- oder TT-Systemen.

**Zeile 10 — Caravanplätze, Campingplätze und ähnliche Bereiche** (ZS, Unterabschnitt 708.415.1):
- **IΔN ≤ 0,03 A**. Bauform übliche, G. Typ AC. Jede Steckdose muss einzeln geschützt sein. Jeder Endstromkreis für festen Anschluss eines Mobilheimes/Parkwohnheimes muss einzeln geschützt sein.

**Zeile 11 — Marinas und ähnliche Bereiche** (ZS, Unterabschnitt 709.531.3):
- **IΔN ≤ 0,03 A**. Bauform übliche, G. Typ AC. Schutz jeder einzelnen Steckdose; Schutz jedes Endstromkreises für festen Anschluss eines Hausbootes.

**Zeile 12 — Medizinisch genutzte Bereiche:**
- **FS (710.415.1):** IΔN ≤ 0,3 A. Bauform übliche, G. Typ AC, A, F, B. Bei Schutzmaßnahme Nullung für Endstromkreise **über 63 A**.
- **ZS (710.415.1):** IΔN ≤ 0,03 A. Bauform: **Stoßstromfestigkeit mindestens 3 kA**, G. Typ AC. Für alle Endstromkreise in Räumen der Gruppe 2, bei denen Schutz durch automatische Abschaltung im ersten Fehlerfall zulässig ist, für Betriebsmittel im Handbereich **bis 63 A**.

**Zeile 13 — Ausstellungen, Shows und Stände** (ZS, Unterabschnitt 711.415.1):
- **IΔN ≤ 0,03 A**. Bauform übliche, G. Typ AC. Alle Endstromkreise bis einschließlich **32 A** für Beleuchtung, Steckdosen und ortsveränderliche Betriebsmittel (über flexible Kabel/Leitungen angeschlossen).
- Vorzugsweise kombinierte kurzzeitverzögerte Fehlerstrom-Leitungsschutzschalter mit ausreichender Stoßstromfestigkeit (z.B. Typ G).
- Ausnahmen: Schutztrennung; Schutz durch Kleinspannung SELV oder PELV. (Text gemäß Beschluss OVE TK-E-505: 705.415.1.001 AT)

**Zeile 14 — Photovoltaische Anlagen (PV-Anlagen)** (FS, Unterabschnitt 712.531.3.101):
- Bauform übliche, S, G. **Typ B**.
- Ausnahmen (kein Typ-B-RCD erforderlich): PCE (Power Conversion Equipment) besitzt mindestens einfache Trennung zwischen AC- und DC-Seite; **oder** PV-Anlage besitzt mindestens einfache Trennung zwischen PCE und RCD durch Transformator mit getrennten Wicklungen; **oder** PCE erfüllt ÖVE/ÖNORM EN 62109-1 und erfordert laut Hersteller-Bestätigung kein RCD vom Typ B.

**Zeile 15 — Möbel** (ZS, Unterabschnitt 713.415):
- **IΔN ≤ 0,03 A**. Bauform übliche, G. Typ AC. Für die gesamte elektrische Anlage für Möbel.

**Zeile 16 — Beleuchtungsanlagen im Freien** (ZS, Unterabschnitt 714.415):
- **IΔN ≤ 0,03 A**. Bauform übliche, G. Typ AC. Einrichtungen in Telefonzellen, Wartehäuschen, Werbeschilder, Leuchtkästen (z.B. für Stadtpläne) und ähnliche Anlagen mit integrierter Beleuchtung.

**Zeile 17 — Ortsveränderliche oder transportable Baueinheiten:**
- **FS (717.411 b):** IΔN ≤ 0,03 A. Bauform übliche, G. Typ AC, A, F, B. Für ortsfeste Anlage, die ein TT- oder TN-System bildet.
- **ZS (717.415):** IΔN ≤ 0,03 A. Bauform übliche, G. Typ AC. Bei Nullung oder Fehlerstrom-Schutzschaltung (zusätzlich): Alle Stromkreise in Wechselspannungsanlagen unabhängig vom Bemessungsstrom, die der Versorgung von Verbrauchsmitteln außerhalb der Baueinheit dienen.

**Zeile 18 — Öffentliche Einrichtungen und Arbeitsstätten** (ZS, Unterabschnitt 718.NE.1.415.1):
- **IΔN ≤ 0,03 A**. Bauform übliche, G. Typ AC. Leuchten im Handbereich in Umkleideräumen für Darsteller, in Friseur- und Maskenbildnerräumen.

**Zeile 19 — Elektrische Anlagen in Caravans und Motorcaravans** (ZS, Unterabschnitt 721.415):
- **IΔN ≤ 0,03 A**. Bauform übliche, G. Typ AC. Bei (Fehler-)Schutz durch automatische Abschaltung der Stromversorgung.

**Zeile 20 — Stromversorgung von Elektrofahrzeugen** (ZS, Unterabschnitt 722.531.3):
- **IΔN ≤ 0,03 A**. Bauform übliche, G. Typ A (in Verbindung mit geeigneter Einrichtung zur Abschaltung bei Gleichfehlerströmen **> 6 mA**), B. Mit Ausnahme von Stromkreisen mit Schutztrennung muss jeder Anschlusspunkt durch eine eigene RCD geschützt sein.

**Zeile 21 — Vorübergehend errichtete Anlagen für Aufbauten, Vergnügungseinrichtungen, Buden auf Veranstaltungsplätzen, Zirkusse** (ZS, Unterabschnitt 740.415.1):
- **IΔN ≤ 0,03 A**. Bauform übliche, G. Typ AC. Alle Endstromkreise bis einschließlich **32 A** für Beleuchtung, Steckdosen und ortsveränderliche Betriebsmittel (über flexible Kabel/Leitungen). Vorzugsweise kombinierte kurzzeitverzögerte Fehlerstrom-Leitungsschutzschalter mit ausreichender Stoßstromfestigkeit (z.B. Typ G).
- Ausnahmen: Schutztrennung; Schutz durch Kleinspannung SELV oder PELV.

**Zeile 22 — Heizanlagen mit Heizleitungen und Flächenheizelementen** (ZS, Unterabschnitt 753.415.1):
- **IΔN ≤ 0,03 A**. Bauform übliche, G. Typ AC. Bei Nullung, Fehlerstrom-Schutzschaltung oder Überstrom-Schutzerdung: für alle Stromkreise, die Heizeinheiten speisen.

#### Fußnoten zu Tabelle 6
- a) FS = Fehlerschutz; ZS = Zusatzschutz; BS = Brandschutz.
- b) Bei mehreren angegebenen Typen hängt der tatsächlich einzusetzende Typ von den Kurvenformen der zu erwartenden Fehlerströme ab (siehe Abschnitt 2.1).
- c) In Spalte „Erläuterungen" konnte nicht der volle Wortlaut der Normentexte aufgenommen werden — vor Anwendung den aktuellen Stand des Regelwerks beachten.
- d) Kriterium nach OVE E 8101:2019, Unterabschnitte 531.3.1.003.AT und 531.3.2.
- e) PCE = Power Conversion Equipment.
- f) In Verbindung mit geeigneter Einrichtung zur Abschaltung im Fall von Gleichfehlerströmen > 6 mA.
- Mehrere Textpassagen wurden gemäß Beschluss OVE TK-E E-505 als Änderungsvorschläge zu OVE E 8101:2019 in der 115. Sitzung des TK-E diskutiert und an die zuständigen TSKs weitergeleitet.

### Literaturhinweise
- **ÖVE-EN 1, Teil 1b** (Nachtrag b zu Teil 1/1989) — Errichtung von Starkstromanlagen mit Nennspannungen bis AC 1 000 V und DC 1 500 V – Teil 1 Begriffe und Schutz gegen elektrischen Schlag (Schutzmaßnahmen).
- **ÖVE/ÖNORM E 8001-1** — Errichtung von elektrischen Anlagen mit Nennspannungen bis AC 1 000 V und DC 1 500 V – Teil 1: Begriffe und Schutz gegen elektrischen Schlag.
- **OVE E 8101** — Elektrische Niederspannungsanlagen.
- **OVE E 8601** — Kurzzeitverzögerte Fehlerstrom-Schutzschalter des Typs G ohne und mit eingebautem Überstromschutz – Ergänzung zu OVE EN 61008-1 und OVE EN 61009-1.
- **ÖVE/ÖNORM E 8603** — Zeitverzögerte Fehlerstrom-Schutzschalter des Typs M ohne eingebauten Überstromschutz zur Anwendung in Stromkreisen mit Nennströmen über 32 A – Ergänzung zu ÖVE/ÖNORM EN 61008-1.
- **ÖVE/ÖNORM EN 60898 Reihe** — Leitungsschutzschalter für Hausinstallationen und ähnliche Zwecke.
- **OVE EN 61008-1** — Fehlerstrom-/Differenzstrom-Schutzschalter ohne eingebauten Überstromschutz (RCCBs) für Hausinstallationen und ähnliche Anwendungen – Teil 1: Allgemeine Anforderungen.
- **OVE EN 61009-1** — Fehlerstrom-/Differenzstrom-Schutzschalter mit eingebautem Überstromschutz (RCBOs) für Hausinstallationen und ähnliche Anwendungen – Teil 1: Allgemeine Anforderungen.
- **OVE EN IEC 61000-6-1** — EMV Teil 6-1: Fachgrundnormen – Störfestigkeit für Wohnbereich, Geschäfts-/Gewerbebereiche, Kleinbetriebe.
- **OVE EN IEC 61000-6-2** — EMV Teil 6-2: Fachgrundnormen – Störfestigkeit für Industriebereiche.
- **ÖVE/ÖNORM EN 61558-2-4** — Sicherheit von Transformatoren u.a. bis 1 100 V – Teil 2-4: Besondere Anforderungen an Trenntransformatoren.
- **ÖVE/ÖNORM EN 62109-1** — Sicherheit von Wechselrichtern in PV-Energiesystemen – Teil 1: Allgemeine Anforderungen.
- **ÖVE/ÖNORM EN 62423** — Fehlerstrom-/Differenzstrom-Schutzschalter Typ F und Typ B mit und ohne eingebauten Überstromschutz für Hausinstallationen und ähnliche Anwendungen.
- **HD 60364 Series** / **IEC 60364 Series** — Low-voltage electrical installations.
- Medieninhaber/Hersteller: OVE Österreichischer Verband für Elektrotechnik, Eschenbachgasse 9, A-1010 Wien. Copyright © OVE 2021.
