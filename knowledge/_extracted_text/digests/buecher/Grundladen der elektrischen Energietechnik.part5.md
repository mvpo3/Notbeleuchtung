# Grundladen der elektrischen Energietechnik — Teil 5
> Quelle: Grundladen der elektrischen Energietechnik (buecher) · Seiten 201-240.

Dieser Teil behandelt elektrische Anlagen und Betriebsmittel im Drehstromnetz. Der Fokus liegt auf dem Aufbau und der Struktur der Netzebenen (NS bis HöS), den Steuerungs- und Regelungsaufgaben, den FACTS-Elementen zur Blindleistungskompensation sowie dem vollständigen Kapitel über Freileitungen inklusive Aufbau, Leiterseile, Erdseile und elektrische Betriebseigenschaften.

## Inhalt

### Einleitung und Abgrenzung Gleichstromtechnik

- Gleichstromtechnik spielt in der übergeordneten Betrachtung eine Nebenrolle; Drehstromnetze stehen im Mittelpunkt.
- Anwendungen von Gleichstrom: Straßenbahnen (typisch 600 V), Kraftfahrzeuge unabhängig vom Antriebstyp, Teile der Schutzkleinspannung in der Gebäudetechnik (Abschnitt 5.1).
- Oberschwingungsfilter werden wegen Netzrückwirkungen der Stromrichterventile installiert.
- Netzrückwirkungen werden durch diese Filter begrenzt; Diskussionen über Gleichstromnetze in der Gebäudetechnik laufen.

### 3.1 Drehstromnetze — Aufbau

- Drehstromnetze bestehen aus Leitungen zwischen Knotenpunkten (Sammelschienen in Schalt- und Umspannanlagen).
- Leistungsschalter unterbrechen oder schließen die Stromkreise an jedem Leitungsende.
- Vier Spannungsebenen: NS (Niederspannung), MS (Mittelspannung), HS (Hochspannung), HöS (Höchstspannung).
- Normspannungen nach DIN EN 60038 (VDE 0175).

**Internationale Spannungsbezeichnungen nach IEEE 1312:**

| Kürzel | Bezeichnung | Spannungsbereich |
|--------|-------------|-----------------|
| LV | low voltage | 50 V ≤ U < 1 kV |
| MV | medium voltage | 1 kV ≤ U < 100 kV |
| HV | high voltage | 100 kV ≤ U < 345 kV |
| EHV | extra-high voltage | 345 kV ≤ U ≤ 765 kV |
| UHV | ultra-high voltage | U > 765 kV |

- Aussereuropäische Spannungen: Kanada/USA bis 735 kV bzw. 765 kV, Russland 750-kV-Netz (Verbindungen nach Polen, Ungarn, Rumänien, Bulgarien), China 500/750/1000 kV, Indien 1200 kV im Probebetrieb.

**Transformatoren in Deutschland (Schätzung nach VDN Jahresbericht 2006):**

| Spannungsebene | Anzahl Transformatoren |
|----------------|----------------------|
| NS (0,4 kV) | 557 700 |
| MS (6 kV ≤ U ≤ 60 kV) | 7 500 |
| HS (60 kV < U < 220 kV) | 1 100 |
| HöS (U ≥ 220 kV) | — |
| Gesamt | 566 300 |

**Leitungslängen und Kabelanteile in Deutschland:**

| Ebene | Länge 1992 (km) | Kabelanteil 1992 (%) | Länge 2011 (km) | Kabelanteil 2011 (%) | Länge 2024 (km) |
|-------|-----------------|----------------------|-----------------|----------------------|-----------------|
| NS | 903 413 | 72 | 1 158 031 | 89 | 1 119 000 |
| MS | 470 321 | 59 | 511 852 | 77 | 520 000 |
| HS | 73 516 | 5,8 | 79 395 | 9,0 | 94 000 |
| HöS | 40 127 | 0,23 | 34 754 | 0,3 | 37 000 |

- In der NS-Ebene steigt der Kabelanteil; in der HöS-Ebene verharrt er nahe 100 % Freileitungsanteil; Änderung durch DC-Links erwartet.

**Sonderformen der Leitungsführung:**
- **Luftkabel:** isolierte Leiter an Freileitungsmasten, vor allem NS/selten MS; gewährleistet Berührungsschutz und erleichtert Bewuchsfreihalten.
- **Gasisolierte Rohrleiter (GIL):** konzentrisch angeordnete Metallrohre; äusserer Leiter geerdet, innerer führt Betriebsstrom; isolierendes Druckgas zwischen den Rohren; vereinzelt in der HöS-Ebene.
- **Supraleitende Kabel:** einzelne Modell-/Forschungsprojekte wie AmpaCity in Essen.

### 3.1.1 Aufbau und Struktur der Netzebenen

**(n–1)-Ausfallkriterium:** Ein einzelner Fehler darf die Versorgung nicht unterbrechen; erst ein zweiter gleichzeitiger Fehler kann zu Kundenabschaltungen führen.

**Störungshäufigkeit im deutschen Drehstromnetz:**

| Ebene | Stromkreislänge (km) | Störungen/Jahr | Störungen/100 km | Erdfehler (%) | Ohne Unterbrechung (%) |
|-------|---------------------|---------------|-----------------|---------------|----------------------|
| MS | 493 000 | 18 083 | 3,67 | 85,5 | 46 |
| HS | 75 200 | 3 733 | 4,96 | 86,9 | 94 |
| HöS | 36 000 | 666 | 1,85 | 61,8 | 99 |

**Niederspannungsnetze:**
- Vierleitersysteme, damit einphasige Wechselstromverbraucher angeschlossen werden können.
- Speisung aus Netzstationen; typische Bemessungsscheinleistungen: 400 kVA, 630 kVA, 800 kVA bis ca. 3000 kVA; Bestandsanlagen auch mit 250 kVA und weniger.
- Grenze der Betreiberverantwortung: Hausanschlusssicherungen im Hausanschlusskasten (HAK) oder alternativ Hausanschlusssäule ausserhalb des Gebäudes.
- Innerhalb des Gebäudes trägt der Anschlussnehmer die Verantwortung.

**Netzformen in der NS-Ebene:**

*Strahlennetz:*
- Einfachste Netzform; verbreitet im ländlichen Raum bei geringer Lastdichte.
- Vorteile: einfacher Aufbau, unkomplizierter Schutz, geringer Planungs- und Wartungsaufwand, überschaubare Kosten.
- Nachteile: Spannungsabsenkung bei hohen Lasten oder Spannungserhöhung durch regenerative Einspeisung (PV-Anlagen); keine Reserve bei Leitungs- oder Stationsausfall; längere Unterbrechungszeiten (ggf. mobile Notstromaggregate oder rückwärtige Einspeisung über Verbindungsleitung).

*Ringnetz (offen betrieben):*
- Ringleitungen an beiden Strassenseiten; offene Trennstellen im ungestörten Betrieb → de-facto-Strahlennetz.
- Kabelverteilerschrank (KVS): NH-Sicherungen ermöglichen Verbindung oder Trennung zwischen Erdkabeln.
- Fehlerfall: betroffenen Kabelabschnitt heraustrennnen, Trennstelle schliessen → Rückwärtseinspeisung.
- Bevorzugter Kabelanteil wegen besserem Schutz gegenüber Erntemaschinen, Witterung, Sturm; kleinere Wirkwiderstände; höhere Stromstärken möglich.

*Maschennetz:*
- Bis zu 16 Transformatoren speisen ein Maschennetz.
- Bessere Spannungshaltung, grundsätzlich weniger Verluste.
- Nachteile: schwieriger Neustart nach Totalausfall (nur manuelles Zuschalten, erste Station rasch überlastet); Fehlersuche komplex.
- Seit längerer Zeit werden bei Neubauten keine Maschennetze mehr gebaut; bestehende Maschen werden nach Möglichkeit entflochten.

**Mittelspannungsnetze:**
- Anbindung über Umspannstationen (typische Bemessungsscheinleistung 20–50 MVA) an HS-Netze.
- Überwiegend Kabel in Städten; Abstände zwischen Netzstationen selten mehr als 500 m.
- Ring mit 5–10 Netzstationen; jede Station kann Leitungsabschnitte freischalten.
- Schwerpunktstationen (auch "Schalthäuser") ohne Umspanner zur Weiterverteilung.
- Je Umspannstation i.d.R. zwei Trafos zur gegenseitigen Reservehaltung.

**Hoch- und Höchstspannungsnetze:**
- HS mit HöS verbunden über Umspannwerke; 380/110-kV-Transformatoren mit 300–400 MVA.
- In der HS-Ebene: Freileitungen und Kabel etwa gleich verteilt; in der HöS-Ebene: Freileitungen dominant.
- Gründe für HöS-Freileitung-Dominanz: günstigerer Bau, geringere kapazitive Ladeströme, einfachere Reparatur nach Ausfall.
- 110-kV-Netze in Ballungsräumen überwiegend als Kabel mit radialer Struktur.
- HöS-Netze sind vermascht → geringere Verluste, bessere Spannungshaltung, flexible Reaktion auf Lastsituationen.

### Energiewende und Netzentwicklung

- Klassisch: unidirektionaler Leistungsfluss von Grosskraftwerken zur Steckdose; Netze auf Lastsicht ausgelegt.
- Neue Anforderungen durch regenerative Einspeisung: Spannungsband einhalten, Stromtragfähigkeit der Leitungen, zulässige Kurzschlussströme, Begrenzung von Störaussendungen.
- In der NS-Ebene bestehen über 90 % der volatilen Einspeisungen aus PV-Anlagen.
- Gleichzeitig wachsender Verbrauch durch Elektromobilität und Wärmepumpen.
- Massnahmen: Netzverstärkung (grössere Leitungsquerschnitte), Verschiebung der Trennstellen, Blindleistungseinstellung an Erzeugungsanlagen.
- Neuere Lösungen: MV-LVR (Medium Voltage Line Voltage Regulator) mit dynamischer/autonomer Spannungssteuerung; NS-Strangregler, Maschenstromregler, Speicher.
- Digitale Ortsnetztransformatoren bei Neubauten für Messwert-Fernübertragung und Asset-Management; regelbare Ortsnetztransformatoren i.d.R. aus wirtschaftlichen Gründen nicht eingesetzt.
- Übertragungsnetzbetreiber: Systemstudien vor Windpark-Anschluss (Leistungsfluss, Kurzschlussstrom, Oberschwingungen, Stabilität); zunehmendes Engpass-Management.
- Offshore-Windparks zentral in Nord- und Ostsee → Erzeugung driftet von Lastschwerpunkten weg → Verluste im Übertragungsnetz steigen tendenziell.
- Wegfall konventioneller Kraftwerke: Momentanreserve für Frequenz-Wirkleistungs-Regelung und Blindleistungskompensation muss das Netz übernehmen.
- Ausblick: Aktive Systeme / Smart Grids; Rolle von KI; offene Fragen zu Cybersecurity, Regulierung und Haftung.

**Netz-Unterteilung nach Funktion:**
- **Verbundnetz:** verbindet Grosskraftwerke, gegenseitige Aushilfe bei Ausfällen; nur wenige Kraftwerksblöcke schwarzstartfähig; auch Energietransport, aber nicht über sehr lange Strecken; Offshore-Windparks direkt angeschlossen.
- **Transportnetz:** versorgt 110-kV-Ebene; dient in Ballungsräumen als Verteilnetz, im ländlichen Raum als regionales Transportnetz; Direktanschluss grosser Industriekunden.
- **Verteilnetze:** regionale/lokale Versorgung; Tarifkunden an 0,4-kV-Ebene, Sondervertragskunden an 10/20-kV-Ebene; Wind- und PV-Anlagen speisen ein.

### 3.1.2 Steuerungs- und Regelungsaufgaben

Zwei Hauptregelaufgaben im HöS-Netz:
- **Frequenz-Wirkleistungs-Regelung (f-P-Regelung):** Frequenz ist global; Akronym AGC (Automated Generation Control); ausschliesslich Übertragungsnetzbetreiber (ÜNB) verantwortlich.
- **Spannungs-Blindleistungs-Regelung (U-Q-Regelung):** Spannung ist lokal; findet in Übertragungs- und Verteilnetz statt; teils zentral in der Netzführung, teils dezentral in der Schaltanlage.

Vier Systemdienstleistungen: Betriebsführung, Frequenzhaltung, Spannungshaltung, Versorgungswiederaufbau.

- Frequenz 50 Hz wird sehr genau eingehalten (Uhrsynchronisierung möglich).
- Zulässiges Spannungsband: ±10 % der Netznominalspannung; perspektivisch ±5 % in der HöS-Ebene.
- Blindleistung sollte möglichst vor Ort kompensiert werden, da Blindleistungstransite mit Wärmeverlusten verbunden sind.

**Frequenz-Wirkleistungs-Regelung:**
- ÜNB steuert Erzeugungsanlagen in seiner Regelzone: regelbare Kraftwerke (Kohle, Erdgas, Wasserkraft); PV- und Windkraftanlagen nur durch Abregelung.
- Inselnetz vs. Verbundnetz: Im Verbundnetz koordinieren alle TSO (Transmission System Operator) auf nationaler und europäischer Ebene unter ENTSO-E (European Network of Transmission System Operators for Electricity).

**Spannungs-Blindleistungs-Regelung mit Erzeugungsanlagen:**
- ÜNB weist Kraftwerke telefonisch an (spannungssenkend oder spannungserhöhend); Sollwerte für Spannung am Anschlusspunkt.
- Kraftwerk: Stufen des Maschinentransformators verändern, Rest erledigt Generatorregelung über Erregerstrom.
- Pumpspeicher- oder Druckluftspeicherkraftwerke: Phasenschieberbetrieb (P = 0) möglich.
- Offshore-Windparks meist über Gleichstromkabel angebunden; Blindleistung über Halbleiterventile der Wechselrichter kontinuierlich und stufenlos verstellbar.
- Verteilnetzbetreiber gibt Sollwert für Blindleistung vor (fest oder variabel per Fernwirkanlage); angewandte Verfahren:
  - Q(U): Blindleistungs-Spannungskennlinie
  - Q(P): Blindleistung als Funktion der Wirkleistung
  - Blindleistung mit Spannungsbegrenzungsfunktion
  - Fester Verschiebungsfaktor cos φ

### Blindleistungskompensation und Leistungsflusssteuerung — konventionelle Betriebsmittel

**Rotierende Phasenschieber (Synchronous Condenser / SynCon / Synchronous Capacitor / Synchronous Compensator):**
- Drehstrom-Synchrongeneratoren im reinen Phasenschieberbetrieb; eingesetzt von ÜNB.
- Dienen zusätzlich als Momentanreserve für f-P-Regelung und ermöglichen Netzintegration von PV/Wind an Netzknoten mit geringen Kurzschlussströmen.
- Neuere Entwicklung: rotierender asynchroner Phasenschieber ARESS (Asynchronous Rotating Energy System Stabilizer).
- Nachteil: höhere Verluste durch Lagerreibung der grossen rotierenden Massen (im Vergleich zu FACTS mit Leistungshalbleitern).

**Schalt- und Regelungselemente:**
- Längs-, Schräg- und Querregeltransformatoren: Stufenweise Einstellung von Spannungen und Wirkleistungen an Netzknoten.
- Konventionelle Drosselspulen oder Leistungskondensatoren parallel → Blindleistungskompensation (Shunt-Elemente).
- Leistungskondensatoren auch in Serie → Wirkleistungssteuerung = Leistungsflusssteuerung (Series-Elemente).

**Mechanisch schaltbare Shunt- und Series-Elemente (Tab. 3.8):**

| Parallel (Shunt) | In Serie (Series) |
|-----------------|------------------|
| MSC (Mechanical Switched Condensator) | FSC (Fixed Series Capacitor) |
| MSCDN (MSC with Damping Network) | — |
| MSR (Mechanical Switched Reactor) | — |
| → Blindleistungskompensation | → Wirkleistungssteuerung |

- Kondensatoren: nur ein-/ausschaltbar; Drosselspulen manchmal gestuft.
- Änderungszeiten von Erregereinrichtungen (Phasenschieber) oder mechanischen Stufenschaltern: im Minutenbereich.

### Flexible Drehstrom-Übertragungssysteme (FACTS)

- FACTS = Flexible AC Transmission Systems; kennzeichnend ist Einsatz von Leistungshalbleitern.
- Betriebsgrössen in Echtzeit stufenlos regelbar → bessere Auslastung, sicherer Betrieb, Engpass-Management, weniger aufwendige Zubaumassnahmen.

**Auswahl von FACTS (Tab. 3.9):**

| Parallel (Shunt) — Blindleistungskompensation | In Reihe (Series) — Wirkleistungssteuerung |
|----------------------------------------------|-------------------------------------------|
| TSC (Thyristor Switched Capacitor) | TSSC (Thyristor-Switched Series Capacitor) |
| TCR (Thyristor Controlled Reactor) | TCSC (Thyristor Controlled Series Capacitor) |
| SVC (Static Var Compensator) | TCSR (Thyristor Controlled Series Reactor) |
| STATCOM (Static Synchronous Compensator) | SSSC (Static Synchronous Series Compensator) |

- Parallelgeschaltete FACTS: dienen Spannungsregelung, verbessern Übertragungsstabilität; können Systemdienstleistung konventioneller Kraftwerke ersetzen; Führungsgrösse = Leiter-Erd-Spannung am Anschlusspunkt.
- Ankopplung über Drehstromtransformatoren (Stromrichterventile müssen nicht für volle Spannung ausgelegt werden); Schaltgruppen zur Minderung von Oberschwingungen.

**SVC (Static Var Compensator):**
- Kombination aus TCR + TSC; Bezeichnung "statisch" bedeutet keine rotierenden Maschinen.
- Koordinierte Steuerung kann sowohl induktive als auch kapazitive Blindleistung bereitstellen.

**STATCOM (Static Synchronous Compensator):**
- Aufgebaut aus selbstgeführten Umrichtern: GTOs (Gate Turn-Off), IGBTs (Insulated-Gate Bipolar Transistor) oder IGCTs (IGC-Thyristor).
- Kann auf Kondensatoren und Drosselspulen verzichten.
- **E-STATCOM:** STATCOM + SCESS (Super Capacitor Energy Storage System als Kurzzeitenergiespeicher) → zusätzlich kurze Momentanreserve für f-P-Regelung.

**Series-FACTS:**
- Führungsgrösse der Regeleinrichtungen: elektrischer Strom in der Leitung.
- TSSC: thyristorgeschaltete Serienkondensatoren.
- TCSC: thyristorgeregelte Serienkondensatoren.
- TCSR: thyristorgeregelte Serienreaktanzen.
- SSSC (Static Synchronous Series Compensator / Advanced Series Compensation ASC): wie eine in Serie geschaltete STATCOM aufgebaut.
- PAR (Phase Angle Regulator) und UPFC (Unified Power Flow Controller): Kombinationen aus Shunt- und Serienelement.

### 3.2 Freileitungen

#### 3.2.1 Aufbau

**Normative Grundlagen (Tab. 3.10):**

| Norm | Inhalt |
|------|--------|
| EN 50182 / — | Leiter — konzentrisch verseilte runde Drähte |
| EN 50341 / VDE 0210 | Freileitungen über AC 1 kV |
| — / VDE 0211 | Starkstrom-Freileitungen bis 1000 V Nennspannung |
| — / VDE 0212 | Armaturen für Freileitungen |
| EN 60433 / VDE 0446 | Isolatoren für Freileitungen > 1 kV (Keramik, Wechselspannung) |
| EN 60466 / VDE 0674 | Verbund-Kettenisolatoren > 1 kV |

**Anforderungen an Freileitungen:**
- Ausreichende Strombelastbarkeit.
- Geringe Stromwärme- und Koronaverluste.
- Hohe Verfügbarkeit, geringe Ausfallrate.
- Mechanische Auslegung für Temperaturschwankungen, Wind- und Schneelasten.
- Sichere Ableitung gefährlicher Schritt- und Berührungsspannungen bis zur Kurzschlussabschaltung.
- Elektromagnetische Verträglichkeit; Reduktion von Koronageräuschen.
- Blitzschutz: Blitzüberspannungen sicher ins Erdreich ableiten.
- Vogelschutz (Hauben an MS-Leitungen, Markierungen an Erdseilen in HöS-Ebene).
- Geringer Eingriff ins Landschaftsbild.

**Bestandteile einer Freileitung:**
- Stützpunkte (Masten oder Dachständer).
- Erd- und Leiterseile.
- Isolatoren und Armaturen.
- Traversen: waagerechte Mastelemente zur Befestigung der Isolatoren.
- Leitersystem: Gesamtheit der drei Leiter L1, L2, L3.
- Spannfeld: Bereich zwischen zwei Masten; derzeitig längste Spannweite 5376 m (Ameralik-Fjord, Grönland).

**Masttypen:**
- Tragmasten: nehmen Gewicht der Leiterseile auf; standhalten zusätzlich vertikalen und horizontalen Windkomponenten.
- Abspannmasten: nehmen Leiterzugkräfte auf; höhere mechanische Anforderungen; Start- und Endpunkte der Leiterseile (Seiltrommel bis ca. 3,5 km Länge); ca. jeder 4.–5. Mast ist ein Abspannmast; Leiterseile werden in Stromschlaufe unterhalb der Masttraverse weitergeführt.
- Tragmasten: in geraden Abschnitten; Winkeltragsmasten bis 160°; Winkelabspannmasten für grössere Richtungsänderungen.
- Verteilungsmasten: Aufsplitten des Leitersystems auf zwei Trassen.

**Materialien nach Spannungsebene:**
- NS/MS: Holz, Beton oder Stahlvollwände.
- HS (wenn Klima erlaubt): Holzmasten möglich.
- HöS: ausschliesslich Stahlgittermasten.

**Mastbilder (Auswahl nach Abb. 3.38):**
1. NS-Holzmast
2. MS-Holzmast mit Stützisolatoren
3. MS-Betonmast
4. Donaumast (110 kV bis 380 kV) — in Deutschland als Standard durchgesetzt
5. Einebenenmast (110 kV bis 380 kV; erfordert grössere Trassenbreite)
6. Tonnenmast
7. Mehrfachleitung für vier Stromkreise mit Viererbündel (Doppeltonnenmast)
8. Portalmast für Einfachleitung (110 kV bis 750 kV)
9. Y-Mastbild (110 kV bis 750 kV)

Beispielmasse Donaumast (Abb. 3.37): Höhe ca. 66,75 m (Sechsstromkreis-Version); 380-kV-Einfachleitung: ca. 39,7 m; 735-kV-Leitung (Kanada): ca. 42 m.

**Isolatoren und Armaturen:**
- Umweltbelastung: Regen, Schnee, Staub, Salz in Meeresnähe; Schmutzbelag → leitfähiger Film → Kriechstrom → Überschlagrisiko.
- Form der Isolatoren: gerippt; verlängert Kriechstromweg; waagerechte Unterseite bleibt bei Regen trocken.
- Material: überwiegend braunes Porzellan; oberhalb 100 kV in Deutschland ausschliesslich Verbundisolatoren aus Silikon bei Neubauten; im Ausland Glaskappenisolatoren (in Ketten für hohe Spannungen).
- Bis 20 kV: Stützisolatoren; darüber: Hängeisolatoren.
- Bei 220 kV: zwei Langstabisolatoren hintereinander; bei 380 kV: drei oder vier; bei Verbund-Silikon: ein einzelner Stab.
- Bruchsicherheit: zwei parallele Isolatoren z.B. bei Autostrassen-Querung.
- Armaturen: Trag- und Abspannklemmen; ab 110 kV Lichtbogenschutzarmaturen (Potenzialsteuerung vermeidet Glimmentladung; schützt Isolator vor Lichtbogen).

**Leiterseile:**
- Mindestens sieben Einzeldrähte; Massivleiter nicht zulässig.
- Werkstoff: meist Aluminium oder Aluminiumlegierung (Aldrey = Al-Mg-Si); selten Kupfer oder Bronze.
- Aluminium: geringes Gewicht; Oxidschicht verhindert Korrosion und elektrisch isoliert Einzeldrähte → reduziert Wirbelstromverluste.
- **Einwerkstoffseile:** alle Drähte homogenes Material (z.B. NS: Beseilung aus Aluminium).
- **Verbundseile:** innere Lagen Stahl (Seele), äussere Lagen Aluminium; Stahldrähte können mit Aluminium ummantelt sein; ab 110-kV-Ebene in Deutschland Standard.
- Seilschlag: abwechselnde Drehrichtung der Lagen; senkt Wirbelstromverluste, verbessert mechanische Eigenschaften, verringert Betriebsinduktivität.
- In HS/HöS: ausschliesslich Verbundseile wegen grösserer Spannweiten (Aluminium hat geringe Zugfestigkeit); mechanische Festigkeit durch Stahl + Aluminiumdrähte.
- Aldrey-Seile: ohne Stahlkern hohe Zugfestigkeit.
- Risiko Windanregung: stehende Wellen → Ermüdungsbrüche möglich; moderate Zugspannungen; Dämpfung durch selbstdämpfende Feldabstandshalter oder Stockbridge-Schwingungsdämpfer nahe Aufhängepunkten.
- Phasenabstandshalter (Schutz gegen Lichtbogenkurzschlüsse zwischen Leiterseilen): werden sehr ungern und nie bei Neubauten eingesetzt.

**Temperaturgrenzwerte der Leiterseile:**
- Aluminium (konventionell): max. ca. 80 °C.
- Kupfer: max. ca. 70 °C.
- Aldrey: max. ca. 90 °C.
- HTLS-Leiter (High Temperature Low Sag): über 200 °C möglich; geringerer Durchhang; Leiterdrähte aus Spezialialuminium; Kern aus Kohlefaserverbund, Keramikfaser-Aluminium-Verbund oder konventionellem Stahl.
- Bei HTLS: höhere Wirkwiderstände durch hohe Temperaturen + höhere Ströme → mehr Stromwärmeverluste (R·I²); stärkere Durchhangvariation → ggf. höhere Masten erforderlich.

**Querschnittsbezeichnung:** Angabe in mm², Verbundseile als Verhältnis; Beispiel: 34-AL1/6-ST1A = Aluminiumquerschnitt ca. 34 mm², Stahlquerschnitt ca. 6 mm².

**Kriterien für Seilquerschnitt:**
- Ausreichende Stromtragfähigkeit (abhängig von max. zulässiger Temperatur, Umgebungstemperatur, Windgeschwindigkeit, Oberflächenbeschaffenheit).
- Ab 110 kV: elektrische Oberflächenrandfeldstärke beachten.
  - Oberhalb ca. 21 kV/cm → Glimm-/Korona-Entladungen: hörbare Geräusche, Störung von Mittelwellensendern und Rundsteuerung, erhöhte Übertragungsverluste.
  - Unterhalb ca. 16 kV/cm bei Nennspannung → Störeffekte vernachlässigbar.

**Bündelleiter:**
- Aus mehreren Verbundseilen bestehend; reduziert Koronaverluste, verbessert Wärmeabfuhr und mechanische Eigenschaften; wirtschaftlicher als Querschnittsvergrösserung.
- In Europa: 2, 3 oder 4 Teilleiter; in Deutschland HöS-Ebene nur noch Vierer-Bündel (Lärmschutz).
- Bei sehr hohen Spannungen: bis zu acht Teilleiter.
- Abstandshalter: im Abstand von 50–80 m zur Sicherung des Teileiterabstands; heute selbstdämpfende Abstandshalter.

**Erdseile:**
- Vorwiegend ab 110-kV-Ebene eingesetzt; an Mastenspitze, galvanisch mit Mast verbunden; manchmal zwei Erdseile.
- Frühere Querschnitte: 94-AL1/15-ST1A (ein Erdseil) bzw. 70-AL1/11-ST1A (zwei Erdseile).
- Heute HöS-Ebene: 265-AL1/35-ST1A (wegen hoher Kurzschlussströme).

**Drei Aufgaben der Erdseile:**
1. Blitzschutz: Blitzüberspannungen werden meist vom Erdseil aufgenommen und über Erdungsanlagen sicher abgeführt; ca. 1–2 % der Blitze enden auf Leiterseilen; in Schaltanlagen daher Überspannungsableiter.
2. Erdkurzschlussschutz: häufigster Fehler in Freileitungsnetzen ist Erdkurzschluss; Fehlerstromkreis schliesst sich überwiegend über Erdseil und Sternpunkte der Drehstromtransformatoren → verhindert nennenswertem Fehlerstrom über Erdreich in Mastsnähe.
3. Nachrichtenübertragung: Edelstahlröhrchen (Grösse eines Stahldrahts) in der Seele; darin Glasfasern eingezogen → digitale Datenübertragung (OPGW); bei Neuverlegung häufig Regelfall.

**Erdungsanforderungen (DIN VDE 0141):**
- Fundament jedes Mastes wird geerdet; Erdungsübergangswiderstand wird in der Bauphase gemessen; bei Überschreitung des Schwellwerts: zusätzliche Erdungsmassnahmen.
- An Anfang und Ende: durchgehendes Erdseil wird in Schaltanlagen an Erdungsanlagen (Kombination Maschen- und Tiefenerder) angeschlossen.

**Blitzschutzraum:** Erdseil erzeugt Schutzbereich; Masche 10 m × 50 m.

#### 3.2.2 Elektrische Eigenschaften

**Verdrillen:**
- Kapazitäten und Induktivitäten hängen von Leitergeometrie ab (εr ≈ 1, μr ≈ 1 in Luft → geometrieabhängig).
- In HS/HöS: Freileitungen werden verdrillt; einfachster Fall: Leiterpositionen L1/L2/L3 an 1/3 und 2/3 der Trassenlänge vertauscht.
- Ziel: gleiche kapazitive und induktive Eigenschaften für alle drei Leiter → symmetrisches Verhalten; dann genügt einphasiges Ersatzschaltbild.

**Erd- und Betriebskapazität:**
- Erdkapazität CE: Mittelwert der drei Kapazitäten Leiter-Erde (C1E, C2E, C3E).
- Koppelkapazität CL: Mittelwert der drei Kapazitäten zwischen je zwei Leiterseilen (C12, C23, C31).
- Bei verdrillter Leitung: C1E = C2E = C3E = CE; C12 = C23 = C31 = CL.
- Umwandlung Dreieck→Stern: Sternpunkt Y auf Erdpotenzial; Betriebskapazität Cb = CE + CY = CE + 3·CL.
- Formel für Betriebskapazität: Cb ≈ 2π·ε₀·l / ln(a/r); mit mittlerem Leiterabstand a = ³√(d₁₂·d₂₃·d₃₁) und Leiterradius r.
- Bündelleiter: grössere effektive Leiterradien → höhere Betriebskapazität.
- Leitungsbeläge: C'b = Cb/l [F/km]; C'0 = CE/l [F/km].

**Betriebsinduktivität:**
- Betriebsinduktivität Lb: Mittelwert der drei Induktivitäten L1, L2, L3.
- Bei verdrilltem Leitersystem: gleiche Lb für alle Leiterseile.
- Näherungsformel: Lb = (μ₀/2π) · ln(a/r) · l.
- Leitungsbelag: L'b = Lb/l [mH/km]; Reaktanzbelag: X'b = ω·L'b [Ω/km].

**Elektrischer Widerstand:**
- Ausgangspunkt: Gleichstromwiderstand R₂₀ = ρ₂₀·l/A = l/(κ₂₀·A); Referenztemperatur 20 °C.
- Für Freileitungen ist Gleichstromformel zu ungenau, da:
  - Seilschlag verlängert effektive Leiterlänge um 6–8 % → Korrekturfaktor 1,06 bis 1,08.
  - Wechselstrom: Stromverdrängungseffekte je nach Frequenz und Querschnitt (resistiver Stromverdrängungsfaktor).
  - Bei mehrdrähtigen Leitern: Stromverdrängung durch Querschnittsaufteilung und isolierende Oxidhaut abgeschwächt.
  - Zusätzliche Verluste im Stahlkern der Verbundseile.
- Praxis: Wirkwiderstandsbelag R'b = Rb/l [Ω/km] aus Herstellerangaben (Tab. 3.11 und 4.5).

**Ableitung:**
- Koronaverluste + Leckströme über Isolatoren; wetterabhängig; Kriechstromverluste meist gegenüber Koronaverlusten vernachlässigbar.
- Wirkleitwert je Leiter für verdrillte Einfachleitung: Gb = GE + 3·GL.
- Ableitungsbelag: G'b = Gb/l [S/km].
- Freileitungen: G'b in Grössenordnung 10⁻⁸ S/km → in Leistungsfluss- und Kurzschlussberechnungen gegenüber ω·C'b vernachlässigbar.
- Kabel: dielektrische Verluste statt Korona; G'b ca. 10⁻⁶ S/km → selbst im Leerlauf vernachlässigbar gegenüber ω·C'b.

**Freileitungsparameter je Spannungsebene (Tab. 3.11, b = Anzahl Bündelleiter):**

| Un (kV) | b | X'b (Ω/km) | R'b (Ω/km) | C'b (nF/km) | Pnat (MW) | Sr (MVA) |
|---------|---|-----------|-----------|------------|----------|---------|
| 110 | 1 | 0,4 | 0,12 | 9,5 | 33 | 60 |
| 220 | 2 | 0,35 | 0,08 | 12,5 | 160 | 250 |
| 380 | 3–4 | 0,32 | 0,02 | 14 | 600 | 1000 |
| 500 | 4 | 0,3 | 0,018 | 15 | 1000 | 2000 |
| 750 | 6 | 0,28 | 0,012 | 13,5 | 2300 | 5000 |
| 1000 | 8 | 0,26 | 0,008 | 14 | 4100 | 11000 |

#### 3.2.3 Dynamisches Verhalten

- Dynamische Vorgänge (Wanderwellen): erfordern exakte Leitungsdifferenzialgleichungen mit verteilten Parametern (elektrisch lange Leitungen).
- **Elektrisch kurze Leitung:** Leitungslänge l ≪ Wellenlänge λ; Bedingung: l ≤ λ/60 für ΔU < 0,5 %.
- Wellenlänge bei 50 Hz: λ = c/f; Freileitung (εr = 1, μr = 1): λ = 6000 km; Kabel (εr = 4): λ = 3000 km.

**Maximale Leitungslängen lmax bei 50 Hz:**

| Leitungstyp | εr | μr | λ (km) | lmax (km) |
|-------------|----|----|--------|-----------|
| Freileitung | 1 | 1 | 6000 | 100 |
| Kabel | 4 | 1 | 3000 | 50 |

- Für verdrillte Freileitung bei üblichen Längen: Leitungsdifferenzialgleichungen (Telegrafengleichungen) mit Belägen R'b, L'b, C'b, G'b; Lösung liefert u(t,x) und i(t,x).

#### 3.2.4 Stationärer Betrieb

- Quasistationäre/stationäre Zustände: Effektivwertzeiger im Bildbereich.
- Elektrisch kurze Leitungen: T- oder Π-Ersatzschaltung mit konzentrierten Leitungsparametern Cb, Gb, Lb, Rb.
- Vollständige Π-Ersatzschaltung gültig auch für Kabel.
- Verluste der Leitung: Pδ = 3/2 · Gb · (UA² + UB²) + 3 · Rb · Ih²
- Blindleistungsbedarf: Q = 3/2 · ω·Cb · (UA² + UB²) + 3 · Xb · Ih²
- Ableitungen Gb: nur für Verlustberechnung relevant; für Strom-/Spannungsberechnungen vernachlässigbar.
- Längsspannungsfall: ΔU = UA − UB = (Rb + jXb) · Ih
- Übertragungswinkel / Leitungswinkel ϑ (auch δL): Phasendifferenz UA zu UB.
- Kapazitive Ladeströme: IAE = jω(Cb/2)·UA; IBE = jω(Cb/2)·UB.

**Leerlauf (IB = 0):**
- Ih = IBE; kapazitiver Ladestrom IBE eilt Spannung UB um 90° vor.
- **Ferranti-Effekt:** Spannung am Leitungsende UB > Spannung am Anfang UA; relative Erhöhung ca. 100 % bei 1000 km Freileitung; bei deutschen Verhältnissen max. 10–15 %.
- Ladestrom: IC ≈ ω·Cb·Un/√3
- Ladeleistung: QC = √3·Un·IC = ω·Cb·Un²

**Natürlicher Betrieb:**
- Drei Merkmale: (1) Verluste null (Rb = Gb = 0); (2) Nennspannung beidseitig (UA = UB = Un/√3); (3) kein Blindleistungsbedarf (Q = 0).
- Natürlicher Strom: Inat = (Un/√3) / ZW
- Wellenwiderstand (verlustlos): ZW = √(Lb/Cb) = √(L'b/C'b).
- Verlustbehaftete Leitung: ZW = √[(R'b + jωL'b)/(G'b + jωC'b)] (komplex).
- Natürliche Leistung: Pnat = √3·Un·Inat = Un²/ZW
- Natürlicher Betrieb = Anpassung: verlustlose Leitung bei Nennspannung mit ihrem Wellenwiderstand abgeschlossen.
- Unternatürlicher Betrieb (P < Pnat): kapazitives Verhalten dominiert.
- Übernatürlicher Betrieb (P > Pnat): Ausgangsspannung sinkt gegenüber Eingangsspannung; Ein- und Ausgangsstrom annähernd gleich.
- Pnat ist fiktive Rechengrösse; dient als Vergleichsmass für Übertragungsleistung von Fernleitungen.

**Hochspannungsfreileitung — Kenngrössen nach Spannungsebene (Tab. 3.13):**

| Un (kV) | Al/St | ZW (Ω) | Pnat (MW) | S1 (MVA) | P'δ (kW/km) | P'δ/S1 (%/km) | Smax (MVA) |
|---------|-------|---------|----------|---------|------------|--------------|----------|
| 10 | 50/8 | 330 | 0,3 | 0,9 | 4,3 | 0,50 | 3 |
| 30 | 120/20 | 335 | 2,7 | 6,2 | 10,5 | 0,17 | 14,2 |
| 110 | 240/40 ×1 | 380 | 32 | 46 | 20,7 | 0,045 | 123 |
| 220 | 240/40 ×2 | 276 | 175 | 183 | 41,5 | 0,023 | 492 |
| 380 | 240/40 ×4 | 240 | 602 | 632 | 83,0 | 0,013 | 1700 |
| 750 | 680/85 ×6 | 260 | 2160 | 3530 | 266 | 0,0075 | 5980 |

*Angaben für S1 und P'δ bei Stromdichte 1 A/mm².*

- Natürliche Leistung bei Freileitungen stets kleiner als thermische Grenzleistung (Stromwärmeverluste) und kleiner als Maximalwirkleistungen aus Wirkleistungs- und Spannungsstabilität.

**Kompensation:**
- Kapazitive Ladeleistungen im Leerlauf oder Schwachlastzeiten: Ausgleich durch parallele Kompensationsdrosselspulen.
- Früher Anschluss an Tertiärwicklungen der Umspanner; heute Direktanschluss.
- Standardgrössen: 120 MVar und 240 MVar.
- Leistungskondensatoren auch in Serie möglich (Wirkleistungssteuerung).
