# k-sibe-at9 — Teil 8
> Quelle: k-sibe-at9 (buecher) · Seiten 321-360.

Dieser Teil ist der Schrack-Sicherheitsbeleuchtungs-Katalog (k-sibe = Katalog Sicherheitsbeleuchtung) und behandelt **Zentralbatterieanlagen (CPS)** und **Gruppenbatterieanlagen** sowie deren Systemkomponenten. Abgedeckt werden die 19"-Serien **MaxiControl (MCX)**, **MultiControl (MC)**, deren **Unterstationen / Unterverteiler**, die Serie **MDC** (CBS-Anlage ohne Leistungsbegrenzung), sowie sämtliche Systembausteine (Stromkreismodule, Ladeteile, Netzwächter, Schalterabfragemodule, Meldetableaus, Leuchten-Netzteile/EVGs, Umschaltweichen, Batterien). Maßgebliche Normen durchgehend: **ÖVE/ÖNORM EN 50171** (zentrales Stromversorgungssystem), **EN 50172 / ÖVE/ÖNORM E 8002-1 / OVE E 8101** (Sicherheitsbeleuchtung), **ÖVE/ÖNORM EN 62034** (automatische Prüfeinrichtung), **EN 50272-2** (Batterieladung), **DIN VDE 0100-718 / 0108**, **EN 60598-2-22**, **E DIN IEC 60998-2-5**, **DIN 4102 Teil 12** (Funktionserhalt E30).

## Inhalt

### Zentralbatterieanlage MaxiControl MCX (Serie, S. 321-325)
- Modulares 19"-Zentralbatteriesystem mit **zusatzleitungsloser Einzelleuchtenüberwachung**, frei programmierbaren Stromkreisen und **5-Jahres-Speicher (Prüfbuch)**. Anschluss von Not-/Sicherheitsbeleuchtung mit LED-, Leuchtstoff- oder Halogen-Leuchtmitteln.
- Eingebautes Webinterface mit Visualisierungssoftware (Darstellung auf Gebäudegrundriss); Konfiguration per Tastatur am Gerät oder über TCP/IP. 19"-Rack-Technik → Module nach-/umrüstbar.
- **Maximalausbau: bis zu 30 Stromkreismodule für bis zu 60 Stromkreise** in einem Gehäuse.
- Jedes Stromkreismodul = **2 Abgangskreise mit je bis zu 20 Leuchten**. Jeder Kreis programmierbar als: Dauerlicht (DS), Bereitschaftslicht (BS), geschaltetes Dauerlicht oder Treppenlicht. Bereitschafts- und Rettungszeichenleuchten kombiniert betreibbar.
- Mit Stromkreismodul **DCM12E (2×1,1A / 2×250VA)** + "EL"-Leuchten → Notleuchten zentral einzeln schaltbar.
- Geräumiges Batteriefach: Front-Terminal-Batterien **bis 150 Ah** im selben Schrank. Einstündige Anlagen bis ca. **20,5 kW** (abzüglich 25% Alterungsreserve) pro Schrank realisierbar.
- **Achtung:** Bei Anbindung von Unterstationen/Unterverteilern bzw. optionalen Baugruppen (SAM24M, SAM08M, IOM01M) → technische Fertigung vorab klären; ggf. zusätzlicher Platzbedarf, Reduzierung der max. Stromkreisanzahl bzw. Ladeteile.

**Eigenschaften MaxiControl:**
- Zentrales Stromversorgungssystem nach ÖVE/ÖNORM EN 50171; Sicherheitsbeleuchtung nach EN 50172, E 8002-1, OVE E 8101.
- Automatische Prüfeinrichtung gemäß ÖVE/ÖNORM EN 62034 (Prüfung jeder angeschlossenen Leuchte); Prüfergebnisse 5 Jahre abrufbar.
- Mikroprozessorgesteuert; hinterleuchtetes LCD-Klartextdisplay, mehrsprachig, passwortgeschützt, 8-Tasten-Programmierung, externe USB-PC-Tastatur, MultiMediaCard für Updates, Ethernet, Browser-Steuerung.
- Endstromkreismodule DCM mit **3A, 4A, 6A Nennstrom**; kompatibel zu Einschub NLDCM12E (1A) für zentral einzelschaltbare Leuchten.
- Einzelleuchtenüberwachung ohne Zusatzleitung; adaptive Stromüberwachung + selektive Isolationsprüfung je Endstromkreis; bis zu **60 Endstromkreise pro 19"-Schrank**.
- Batterieladung nach **IUTQ-Kennlinienfeld**; externe Bausteine (Netzwächter etc.) über Bussystem.

**Technische Daten MaxiControl:**
- Montage: Wand/Stand. Gehäuse: Stahlblech RAL 7035. Abmessungen: **1850 × 800 × 600 mm (HxBxT)** (inkl. 50 mm Sockel).
- Schutzart/-klasse: **IP20 / I**. Kabeleinführung: Dacheinführung.
- Netzanschluss: **3×230V AC ±10% 50/60 Hz**. Ausgangsspannung: **230V AC / 216V DC**.
- Abgangskreise: max. 60, Umschaltung Dauer-/Bereitschaft je Kreis. Max. Lader: **10 A**.
- Batterie (nicht enthalten): wartungsfreie verschlossene Bleibatterie Front Terminal OGiV/OGI/OPzV oder wartungsarme NiCd.
- Zulässige Umgebungstemp.: **10° bis 35° C**.
- Gewicht: NLMCX148 = 200 kg, NLMCX448 = 225 kg (ohne Batterien).

**Max. Anschlussleistung DC (Summe aller Endstromkreise, inkl. 25% Alterungsreserve):**
| Batterie (FT) | 1h | 3h | 8h |
|---|---|---|---|
| 55 Ah | 27,1A / 5,86kW | 11,4A / 2,47kW | 5,3A / 1,15kW |
| 80 Ah | 36,6A / 7,91kW | 15,3A / 3,3kW | 7,2A / 1,56kW |
| 100 Ah | 51,8A / 11,18kW | 21,8A / 4,71kW | 9,6A / 2,07kW |
| 150 Ah | 78,8A / 17,0kW | 34,2A / 7,38kW | 13,8A / 2,97kW |

**Batteriesätze 216V DC (18× 12V), Gewicht:** 55Ah=346 kg · 80Ah=468 kg · 100Ah=585 kg · 150Ah=819 kg.

**Stromkreismodule MaxiControl (Typ / Absicherung / max. Belastung pro Modul):**
- DCM12E: 4× F5A — 1A / 2×300VA
- DCM32: 4× F5A — 3A / 2×650VA
- DCM42: 4× F6,3A — 4A / 2×860VA
- DCM62: 4× F10A — 6A / 2×1300VA

**Bestellnummern Zentralbatterieanlagen (alle Gehäuse H1850×B800×T600, Batteriefach bis 150Ah, ohne Einschübe/Batterien):**
- NLMCX148: Lader 2,5A, max. 48 Kreise · NLMCX248: Lader 5A, 48 Kreise · NLMCX348: Lader 7,5A, 48 Kreise · NLMCX448: Lader 10A, 48 Kreise
- NLMCX260: Lader 5A, 60 Kreise · NLMCX360: Lader 7,5A, 60 Kreise
- NLMCX200: Lader 5A, 0 Kreise · NLMCX212: Lader 5A, 12 Kreise · NLMCX224: Lader 5A, 24 Kreise · NLMCX236: Lader 5A, 36 Kreise · NLMCX336: Lader 7,5A, 36 Kreise

**Notwendiges Zubehör (Stromkreiseinschübe):**
- NLDCM12E: 19" 2×1A/300VA, Absicherung 4×F5A, für zentral einzelschaltbare Notleuchten NL…EL / NL…E
- NLDCM42: 19" 2×4A/860VA, Absicherung 6,3A, Mischbetrieb DS/BS
- NLDCM62: 19" 2×4A/1300VA, Absicherung 10A, Mischbetrieb DS/BS
- NLMCPAKET (CPS-Basisausstattung): kritische Stromkreisüberwachung CCIF, Servicesteckdose SSD, Türfeststeller TFST, Schranksockel BASO, Lüfterkontakt LUAN1, Lichtschalterabfragemodul SAM24

**Batteriesätze 216V, 18 Stk. Longlife Front Terminal OGiV (C20) inkl. Verbinder:** NLBAS080FT (12V/80Ah) · NLBAS100FT (12V/110Ah) · NLBAS150FT (12V/159Ah).

**Optionales Zubehör (MaxiControl):**
- NLPLX185: Polycarbonat-Sichttür 480×530mm für Schrank H=1850mm
- NLMCLM: Dreiphasen-Netzüberwachung mit Busanbindung · NLPC2300: Dreiphasennetzüberwachung PC230
- NLMCT15 / NLMCT15S: Meldetableau LCD-Klartext mit Busanbindung (S = mit Schlüsselschalter)
- NLSAM24 / NLSAM24M (eingebaut, inkl. Klemmen): Lichtschalterabfragemodul 8 Eingänge inkl. Netzwächter · NLSAM08: 8 Eingänge ohne Netzwächter
- NLMCBD04: Einbaudrucker für Midi-/Maxi-/MultiControl
- NLMCABUS: Abgang Unterstation · NLMCABUV: Abgang Unterverteilung (nur mit NLUVKOP) · NLUVKOP: Bus-Konverter zur Vernetzung von Unterverteilern
- NLMCMODBUS: GLT Modbus Gateway inkl. Software · NLMCXML: XML-Datenschnittstelle
- NLWES852: Switch 5-Port 10/100BASE-TX (DIN-Schiene) · NLWES882: Switch 8-Port · NLPANPC1: Panel/Tablet-PC Touchscreen Fronteinbau
- Einzelblockbatterieüberwachung Bat-Logg® (für 18 Batterien): NLBTLMC181 (65–260Ah, Interface in Anlage, max. 2,5 m Abstand), NLBTSMC181 (65–260Ah, externer Schrank, max. 8 m), NLBTLMC184 (17–60Ah, in Anlage, max. 5 m), NLBTSMC184 (17–60Ah, extern, max. 8 m); Ersatzsensoren NLBTLSENS1 / NLBTLSENS4.

### Zentralbatterieanlage MultiControl MC (Serie, S. 326-331)
- Modulares 19"-Zentralbatteriesystem mit zusatzleitungsloser Einzelleuchtenüberwachung, frei programmierbaren Stromkreisen, 5-Jahres-Speicher. Gehäusevarianten mit integriertem oder externem Batteriefach.
- **Maximalausbau: bis zu 48 Stromkreismodule für bis zu 96 Stromkreise** pro Gehäuse. Jedes Modul = 2 Abgangskreise mit je bis zu 20 Leuchten.
- Anschluss von LED-, Leuchtstoff- oder Halogen-Niedervoltlampen. **Bis zu 32 Anlagen/Unterstationen** über seriell oder TCP/IP vernetzbar → max. **3072 Stromkreise bzw. 61440 Leuchten** überwachbar. Auch mit zertifiziertem **E30-Schrank** erhältlich.
- DCM12E (2×1,1A / 2×250VA) + "EL"-Leuchten → zentral einzeln schaltbar.
- Eigenschaften wie MaxiControl; zusätzlich: externe PC-Tastatur via **PS2**, optional integrierter Drucker, **bis zu 96 Endstromkreise pro 19"-Schrank**.

**Technische Daten MultiControl:**
- Montage Wand/Stand; Gehäuse Stahlblech RAL 7035; optional **Brandschutzgehäuse E30** (ausgewählte Typen auf Anfrage).
- Abmessungen (HxBxT): **900×600×450 mm** (ohne Batterieschrank); **1800×600×450 mm**; **1500×600×450 mm** (Kombischrank bis 45Ah).
- Schutzart/-klasse IP20 / I. Kabeleinführung Dacheinführung.
- Netzanschluss 3×230V AC ±10% 50/60 Hz. Umschaltbetrieb **230V AC / 216V DC ±15%**.
- Abgangskreise max. 96 (Umschaltung Dauer-/Bereitschaft je Kreis). Max. Lader: **25 A**.
- Batterie: wartungsfreie verschlossene Bleibatterie FT OGiV/OGI/OPzS oder wartungsarme NiCd. Max. Anschlussleistung DC: abhängig von Projektierung. Umgebungstemp. 10°–35° C.
- Stromkreismodule identisch zu MaxiControl: DCM12E (4×F5A, 1A/2×300VA), DCM32 (4×F5A, 3A/2×650VA), DCM42 (4×F6,3A, 4A/2×860VA), DCM62 (4×F10A, 6A/2×1300VA).

**Anlagenliste MultiControl (Auszug — Ausführung / Lader / Gehäuse HxBxT / max. Kreise / max. DCM); Hinweis: ein zusätzlicher Stromkreis ist als Standard immer integriert:**
- *Kombigerät Batteriefach bis 17Ah (1000×600×400):* 12/2,5A → 12 Kr / 6 DCM · 24/2,5A → 24/12 · 36/2,5A → 36/18
- *Kombigerät Batteriefach bis 45Ah (1500×600×450):* 12/2,5A → 12/6 · 24/2,5A → 24/12 · 36/2,5A → 36/18
- *Grundgerät 900×600×450:* 900 12/2,5A → 12/6 · 900 24/2,5A → 24/12 · 900 36/5,0A → 36/18 · 900 36/7,5A → 36/18 · 900 48/7,5A → 48/24
- *Grundgerät 1800×600×450:* 12er-Reihe mit Lader 7,5 / 10,0 / 12,5 / 15,0 / 17,5 / 20,0 / 22,5 / 25,0A → je 12 Kr / 6 DCM; 24/20,0A → 24/12 · 24/25,0A → 24/12; 36/10,0A · 36/20,0A · 36/25,0A → je 36/18; 48/12,5A · 48/25,0A → je 48/24; 60/20,0A → 60/30; 72/15,0A · 72/25,0A → je 72/36; 96/15,0A → 96/48.
- Weitere Konfigurationen (z.B. größere Lader) auf Anfrage. Achtung wie bei MaxiControl: optionale Baugruppen (SAM08M, IOM01M) / Unterstationen vorab klären → ggf. Reduktion Kreise/Ladeteile.

### Unterstationen MultiControl (S. 332-333)
- Unterstationen bieten gleiche Funktionen wie die MultiControl-Zentrale; **mikroprozessorgesteuert, arbeiten bei Ausfall des Hauptrechners autark weiter**. Alle Programmiermöglichkeiten/Schnittstellen wie Zentrale. Zusatzleitungslose Einzelleuchtenüberwachung, frei programmierbare Stromkreise. Auch in **E30** erhältlich. DCM12E + "EL" → zentral einzeln schaltbar.
- **Kompakte MicroControl-Unterstation:** für MultiControl auf Basis MicroControl-Steuerungsrechner für **2, 4 oder 6 Hauptstromkreise**. Abmessungen **430×350×230 mm (HxBxT)**. Komplett mit I/O-Modul, SAM08-Modul, überwachter Ruhestromschleife CCIF, Webinterface, Ethernet-vernetzbar. **Max. Anschlussleistung 2.000 VA.**
- Technische Daten: Gehäuse Stahlblech grau RAL 7035; Schutzart **IP21** (opt. IP54, E30, E90); Schutzklasse I; Kabeleinführung von oben bzw. unten bei 900er-Schrank; Netzanschluss 1 oder 3×230V 50Hz.

**Bestellnummern Unterstationen (inkl. Prozessor für MultiControl):**
- NLUCW12: max. 6 DCM / 12 Stromkreise, H550×B600×T450mm · NLUCW12E30: E30-Schrank H1050×B650×T341mm
- NLUCW24: max. 12 DCM / 24 Kreise, H550×B600×T450mm · NLUCW24E30: E30 H1050×B650×T341mm
- NLUCW36: max. 18 DCM / 36 Kreise (Text S.333 nennt einmal "18 Stromkreise", einmal 36), H900×B600×T450mm · NLUCW36E30: E30 H1150×B760×T575mm
- Notwendiges Zubehör (Stromkreiseinschübe): NLDCM12E (2×1A/300VA, 4×F5A, NL…EL/NL…E), NLDCM32 (2×3A/650VA, 5A, DS/BS), NLDCM42 (2×4A/860VA, 6,3A, DS/BS), NLDCM62 (2×4A/1300VA, 10A, DS/BS).

### Unterverteiler MCUV-E — Einleitertechnik (S. 334-336)
- Neueste Unterverteiler-Serie für MaxiControl/MultiControl. Auslagerung einzelner Stromkreismodule (**Tragschienenmodul TSM32**) in eigenes Gehäuse → spart bei großen Objekten Kabelwege und Installationsmaterial.
- **Energieversorgung in Einleitertechnik** durch AC/DC-Umschaltung im Hauptgerät: MCUV-E mit AC versorgt solange Hauptgerät im Netzbetrieb; bei Netzausfall/Test mit DC. Nur **eine Versorgungsleitung (AC/DC)** statt zwei (AC + DC).
- Jeder Unterverteiler: **4 separate CCIF** → 4 Ruhestromschleifen einzeln überwachbar.
- Option: zusätzliche Einspeisung aus lokalem Allgemeinlichtverteiler → mieterbezogene Energieversorgung. Im Normalbetrieb Versorgung der Leuchten aus lokalem AV; erst bei dessen Ausfall bzw. Not-/Testbetrieb über Einleiterversorgung aus Hauptgerät.
- **TSC-UV (Tragschienen-Controller):** Kontroll-/Schaltmodul, überwacht bis 4 Ruhestromschleifen + optionale AV-Einspeisung, schaltet TSM32 in Betriebszustände.
- **TSM32 (TragschienenStromkreisModul):** versorgt/überwacht 2 Stromkreise mit je max. 20 Sicherheits-/Rettungszeichenleuchten. Einzelleuchtenabfrage + selbstkalibrierende Stromüberwachung. Mischbetrieb Sicherheits-/Rettungszeichenleuchten in einem Kreis in BS/DS/geschaltetem DS ohne separate Datenleitung. Schaltung über SAM: Dauerlicht (DS), modifizierte Bereitschaft (MB), geschaltete modifizierte Bereitschaft (gMB). Anbindung an Zentrale über **RS485 BUS**; jeder Stromkreis frontseitig mit **5 AT** abgesichert.

**E30-Kabelabzweigkasten NLAKE3016 (Installation mit Funktionserhalt E30):**
- Abmessungen **314×314×168 mm**. Absicherung **2× Neozed D02 / 25A**. Klemmenquerschnitt max. **16 mm²**. Max. Anschlussleistung **4300 VA / 4000 W**. Kabel ohne Funktionserhalt: NYM.

**Bestellnummern Unterverteiler (TSC-UV + SAM, IP20):**
- NLMCUV02S: 1×TSM32, 3 Reihen, 515×305×99mm · NLMCUV04S: 2×TSM32, 3 Reihen, 515×305×99mm
- NLMCUV06S: 3×TSM32, 4 Reihen, 640×305×99mm · NLMCUV08S: 4×TSM32, 4 Reihen, 640×305×99mm
- NLMCUV10S: 5×TSM32, 5 Reihen, 800×300×165mm · NLMCUV12S: 6×TSM32, 5 Reihen, 800×300×165mm
- Zubehör: NLTSCUV (Controller inkl. 4×CCIF, Schützansteuerung/-überwachung); NLTSM32 (Stromkreisbaugruppe 2 Kreise 3A (T5A), Schaltarten DS/BS/gDS); NLAKE30-16 (E30-Abzweigkasten 16mm² Durchgangsklemmen, max. 4 kW, 314×314×168mm).

### Zentralbatterieanlage MDC — CBS ohne Leistungsbegrenzung (S. 337-338)
- Ableitung der MultiControl-Serie; **zentrales Stromversorgungssystem ohne Leistungsbegrenzung (CBS)** nach **EN 50171** bzw. **DIN VDE 0100-718** und **EN 50172**.
- Aufbau: Notlichtsteuerrechner **NLSR** (Web-Interface + Visualisierung + 5-Jahresspeicher), Ladeeinheiten **LDM25**, mind. ein Relaisinterface-Modul **IO**, **RS-Module** zum Schalten der Schützgruppen (DS oder BS programmierbar).
- Jeder Schützgruppe (DS/BS) bis zu **6 Schaltbefehle (ds)** bzw. Ruhestromschleifen (mb) über SAM24 + Netzwächter MC-LM zuordenbar. Meldetableaus MCT anschließbar.
- Über Schützgruppen versorgte Sicherungsautomaten (Allstrom) oder Sicherungselemente (**NEOZED D01/D02**) sichern Endstromkreise im Netz- und Batteriebetrieb (**230 VAC / 216 VDC**) ab.
- Selbstkalibrierende Gesamtstromüberwachung wertet prozentuale Abweichungen des Batterie-Entladestroms aus: **5%, 10%, 20%, 50%**.
- An MDC-Hauptstation bis zu **32 MDC-Unterstationen** via Ethernet; mehrere MDC-Unterverteiler via **RS422-Bus**. Anschluss LED-/Leuchtstoff-/Halogenlampen.
- Technische Daten: Gehäuse Stahlblech RAL 7035; Schutzart IP20 (opt. IP54/E30/E90); Klasse I; Abmessungen ohne Batterieschrank 900×600×450mm bzw. 1800×600×450mm, Kombischrank (bis 33Ah) 1500×600×450mm; Kabeleinführung oben/unten bei 900er; Netz 3×230V 50Hz; Batterie OGiV/OGi/OPzS oder NiCd; Ausgang 230V AC / 216V DC; Umgebungstemp. 10°C–35°C.
- Bestellnummern: NLBZV2200 (BZV 220-DC 2×10 Kreise 10kW, ohne Batt., MDC 0); NLBZV2201 (20 Kreise 15kW/1h, Batt. 120Ah, MDC I); NLBZV2202 (20 Kreise 19kW/1h, Batt. 150Ah, MDC II).

### E30-Abzweigdose doppelt gesichert NLWKE304 (S. 339)
- Verbindungskasten nach **E DIN IEC 60998-2-5**, **IP66**, **Ui = 450V**, echter Funktionserhalt **E30 nach DIN 4102 Teil 12**. Als Abzweigkasten mit doppelt abgesichertem Zweig. Maße **L×B×H = 160×160×110 mm**.
- Spezial-Duroplast-Reihenklemmen auf Normschiene: 3-polig im Durchgang, Klemmvermögen pro Pol 2× 0,5–4 mm²; 3-polig im doppelt abgesicherten Abzweig, 2× Sicherungsreihenklemme max. **6,3A (5×20mm)**, Klemmvermögen pro Pol 1× 0,5–4 mm². Mit Dübelset und 3 Kabelverschraubungen **M25** (Dichtbereich 6–15 mm).
- Bestellnummer NLWKE304: E30-Abzweigdose 3-polig für CPS mit Selektivsicherung 2-polig.

### Systemkomponenten — Stromkreis- und Ladeteilbaugruppen (S. 340-345)
**Stromkreisbaugruppe DCM (S. 343):** 19"-Einschubtechnik, Spannungsversorgung von Sicherheits-/Rettungszeichenleuchten. Je 2 Stromkreise (bis 20 Leuchten/Kreis, jeder Kreis mit 2 Sicherungen). Für Micro-/Mini-/Midi-/Maxi-/MultiControl. Jeder Abgang stromkreis- oder einzelleuchtenüberwacht, kombiniert möglich; Schaltarten DS/BS/geschaltetes DS/Treppenlicht. DCM12E zusätzlich Einzelleuchtenschaltbarkeit (Leuchten Artikelnr. endet auf EL/E, zentral einzeln schaltbar ohne Zusatzleitung, Zuordnung zu SAM24-Kontakten). Abmessungen **128×35×173 mm (HxBxT)**.
- (DCM-Tabelle S.344 vertauscht Werte — maßgeblich gilt die konsistente Modul-Spezifikation: DCM12E = 1A/2×300VA/4×F5A; DCM32 = 3A/2×650VA/4×F5A; DCM42 = 4A/2×860VA/4×F6,3A; DCM62 = 6A/2×1300VA/4×F10A.)
- Bestellnummern: NLDCM32 (2×3A/650VA, 5A, DS/BS) · NLDCM42 (2×4A/860VA, 6,3A) · NLDCM62 (2×4A/1300VA, 10A) · NLDCM12E (2×1A/300VA, 4×F5A, für NL…EL/NL…E).

**Stromkreisbaugruppe ACM (S. 344):** 19"-Einschub, Wechselspannungsversorgung von Sicherheits-/Rettungszeichenleuchten (Micro–MultiControl). **1 Stromkreis, max. 500 VA**. Umschaltbetrieb: Normal 230V AC 50/60Hz, Notbetrieb Batteriespannung → 230V 50Hz Rechteckspannung. Erdschlussüberwachung (rote LED), Überlastschutz mit Abschaltung + optischer Anzeige. Abmessungen **128×35×173 mm (HxBxT)**. Bestellnr. NLACM (ACM 19" 230VAC 500VA).

**Ladeteilbaugruppe LDM25 (S. 344):** 19"-Einschub, Aufladung von Batteriesätzen (Micro–MultiControl). Arbeitet mit Trenntransformator (galvanische Trennung) nach **IUP(TS)-Kennlinie gemäß EN 50272-2**. Ausgangsstrom begrenzt auf **0,5A / 1,0A / 2,5A**; mehrere Module parallel für höheren Ladestrom. Vorprogrammierte Ladekennlinien für **NiCd, OGI/OPzS/OPzV, OGIV**. Integrierter redundanter Batteriespannungswächter (BSW) gegen Überladung. Abmessungen **128×70×173 mm (HxBxT)**. Bestellnr. NLLDM25 (2,5A).

### Systemkomponenten — Schalt-, Melde- und Netzwerkmodule (S. 345-349)
**Schalteingangs-/Ausgangsmodul IOM01 (NLIOM01):** 7 Relaisausgänge mit potentialfreien Wechselkontakten (max. **6A/250V AC1, 6A/30V DC**) für Signalisierung (Batteriebetrieb, Störung, Tiefentladung). 4 galvanisch getrennte Schalteingänge (**185–255V 50/60Hz AC, 18–250V DC**) für externe Steuersignale/Sensoren (Betriebsartenwahlschalter, Luftstromwächter) — Eingänge müssen mit externer Spannung betrieben werden. **Bis zu 5 IO-Module pro Anlage**. Für Micro–MultiControl. Montage DIN-Schiene TS35. Abmessungen **105×85×65 mm (BxHxT)**.

**GLT Modbus Gateway (NLMCMODBUS):** unterstützt **Modbus oder BACnet**; Zugriff via Modbus/TCP oder OPC (KNX auf Anfrage). BACnet-Merkmale inkl. BBC-Profil. Auslesbar bis Leuchtenebene: Leuchtenfehler je Leuchte, Stromkreisfehler (Isolation, Sicherung, Stromüberwachung), Anlagenzustand (BAS, Sammelstörung), Fehlerspeicher, Messwerte (Netz, Batterie). Bei Vernetzung: nur Master mit vollem Gateway, Unterstationen mit eingeschränkter Tiefe.

**Lichtschalter-Abfragemodul SAM08 (NLSAM08):** gemeinsames Schalten von Sicherheitsleuchten mit Allgemeinbeleuchtung oder Treppenhauslichtsteuerung im Batteriebetrieb. **8 galvanisch getrennte Eingänge, durch 230V geschaltet**. Treppenhauslichtsteuerung: an 2 Eingängen bis zu **12 beleuchtete Taster** für zeitbegrenzte Aktivierung; erfordert Versorgung aus ACM-Einschub. Montage TS35. Abmessungen 105×85×65 mm (BxHxT).

**Lichtschalter-Abfragemodul SAM24 (NLSAM24):** Abfrage von Lichtschaltern + gemeinsames Schalten Sicherheits-/Allgemeinbeleuchtung im Netzbetrieb. **8 Schalteingänge** wahlweise **185–255V AC und/oder 24–255V DC**; Schließer und Öffner verwendbar. Integrierter aktivierbarer **Dreiphasenwächter**. Zwei RS485-Bus-Anschlüsse (Durchgangs-/Sternverdrahtung weiterer SAM/MC-LM); Adressierung per Drehcodierschalter; LEDs für Störung/Schaltzustand/Betrieb. Montage TS35. Abmessungen 105×85×65 mm.

**Fernmeldetableau MCT15 / MCT15S (NLMCT15 / NLMCT15S):** Fernanzeige auch bei Netzausfall. Variante mit Taster oder Schlüsselschalter (S) als Betriebsartenwahlschalter → Blockierung des Notlichtbetriebes während Betriebsruhe (beeinflusst nicht die Batterieerhaltungsladung im Netzbetrieb); Schlüsselschalter verhindert unbefugte Bedienung. Dreizeiliges Display, 16 Zeichen/Zeile, Klartext: Batteriespannung, Netzspannung, Batterie-/Umgebungstemperatur, Systemfehler. Integrierte Busleitungsüberwachung → bei Kurzschluss/Drahtbruch sofortiges Einschalten aller Stromkreise. 3 LED-Anzeigen (betriebsbereit / Netz- oder Batteriebetrieb / Systemfehler) + akustisches Signal im Fehlerfall. Abmessungen **116×116×24 mm (BxHxT)**.

**Panel PC für CPS (NLPANPC1):** optionale Ausrüstung der MultiControl; Webinterface direkt an der Anlage. **12" (2 Höheneinheiten) oder 15" (3 Höheneinheiten)** → reduziert Anzahl installierbarer Stromkreismodule im selben Gehäuse (Unterverteiler/Unterstationen weiter anschließbar). Multitouch-Display, **Windows 8/10**; Gebäudepläne speicherbar (höhere Kapazität + schnellerer Zugriff als interner Speicher).

**Busfähige Dreiphasenüberwachung MC-LM (NLMCLM):** Multi-Control-Line-Monitor zur Überwachung von **AV-Netzen** (Allgemeinbeleuchtung), 3 Phasen. Nicht genutzte Phaseneingänge brücken. Schaltschwelle für Netzausfall/-schwankung bei **85% der Nennspannung (230V AC) = ca. 195V AC**. Anschluss über überwachte BUS-Leitung → keine E30-Leitungen nötig. Bis zu **16 MC-LM pro SIBE-Gerät**. Montage TS35. Abmessungen **54×96×54 mm (BxHxT)**.

**Dreiphasennetzüberwachung PC230 (NLPC2300):** Überwachung von AV-Netzen, 3 Phasen 230V gegen Nullleiter; nicht genutzte Anschlüsse brücken. Schaltschwelle **85% (ca. 195V AC)**. Zwei Wechslerkontakte, max. Schaltleistung **2A bei 30V DC oder 230V AC**; selbsttätige Rückschaltung. Montage TS35. Abmessungen 54×96×54 mm (BxHxT).

**CCIF-Modul — Kritisches Stromkreis-Überwachungs-Modul (NLCCIF):** für Midi-/MultiControl. Überwacht eine Ruhestromschleife (Netzwächterschleife) in Verbindung mit PC230. Netzwächter mit potentialfreiem Kontakt (geschlossen bei anliegender Überwachungsspannung). Auslösung des modifizierten Bereitschaftsbetriebes (Mod. BS) bei Unterbrechung der Ruhestromschleife bzw. Kurzschluss (Verklumpung). Modularer Aufbau → nachrüstbar; **keine brandbeständige Ausführung der Ruhestromschleife erforderlich** (auf Anfrage).

**WLAN-Modul (NLWLAN / NLMIWLAN eingebaut):** WLAN-Hotspot der Gruppen-/Zentralbatterieanlage, Fernzugriff zur Visualisierung/Wartung per Smartphone/Tablet/PC ohne Zusatzleitung. WLAN bis **150 Mbit/s**; kompatibel zu >120 UMTS/HSPA/EVDO-3G-USB-Modems; Betriebsarten 3G/4G-Router, Travel-Router (Accesspoint), WISP-Client. Abmessungen **57×57×18 mm (BxHxT)**.

**Industrial Ethernet Switches:** NLWES852 = 5 Ports 10/100Base-TX (24×74×109 mm); NLWES882 = 8 Ports (109×32×74 mm). Auto-Negotiation, Auto-MDI/MDI-X an allen Ports. Versorgung aus Zentralbatterieanlage → Kommunikation auch bei Netzausfall. Montage TS35.

### Leuchtenmodule, Netzteile und EVGs (S. 350-359)
**Schaltnetzteil MLED500 (NLMLED500E):** elektronisches Schaltnetzteil für LED-Leuchtmittel **bis 8W** mit Einzelleuchtenüberwachung, Leuchtencontroller, Netzüberwachung, Dimm-/Blinkfunktion. Netzwächter erlaubt Bereitschaftsschaltung an Dauerlichtstromkreis (bei Störung der Allgemeinbeleuchtung automatisch aktiv). Für My-/Micro-/Mini-/Midi-/Maxi-/MultiControl + Altanlagen BK/BX/ZX/ZDCL (mit SKMT). Ausgangsspannungen **4,3V / 12V / 24V**; Ausgangsströme **150 / 300 / 400 mA**; zentral einzeln schaltbar mit NLDCM12E; Eingangsklemmen 0,5–2,5 mm² starr.

**Schaltnetzteil RLED100 (NLRLED100):** mit Einzelleuchtenüberwachung. Für My–MultiControl. Nennspannung **230V AC 50Hz ±20% / 230V DC ±20%**; Ausgang **12V DC / 300 mA (begrenzt)**; Dauer-/Bereitschaftsschaltung; zentral einzeln schaltbar mit NLDCM12E; Einzelleuchtenüberwachung an Schrack-Anlagen nach EN 50171; verpolungstolerant; Klemmen 0,5–2,5 mm² starr. Abmessungen **55×51×32 mm (BxHxT)**.

**Schaltnetzteil NT24 (NLNT24):** für LED-Leuchten **bis 5W**. Nennspannung 230V AC 50Hz ±20% / 230V DC ±20%; Ausgangsspannungen **3,3V / 5V / 12V / 24V**; Ströme **150 / 300 mA** (Bestelltext: 150/200mA); Anschluss max. 1,5 mm² starr. Abmessungen **78×30×20 mm (LxBxH)**.

**Leuchtenüberwachung DCBLU05 (NLDCBLU05):** Einzelleuchtenabfrage für Anlagen Micro–MultiControl, gefertigt nach **EN 50171, DIN VDE 0108 bzw. ÖVE E8002 und OVE E 8101**. Überwacht gleichspannungstaugliche Vorschaltgeräte/Leuchtmittel **3–200 VA**. Nennspannung 230V AC 50Hz ±20% / 230V DC ±20%; Klemmen max. 1,5 mm² starr. Abmessungen **70×30×20 mm (LxBxH)**.

**Mischbetriebs-Leuchtenmanager MU05 (NLMU05):** adressierbarer Controller zum Einbau in Sicherheitsleuchte; alle Schaltarten + Einzelleuchtenüberwachung ohne Zusatzleitung. Integrierter Netzwächter (Bereitschaftsschaltung an Dauerlichtstromkreis). Für Micro–MultiControl. Nennspannung 230V AC 50Hz ±20% / 230V DC ±20%; Verbraucherleistung **4–200 VA**; Klemmen 2,5 mm² mit Durchgangsverdrahtung; Dauer-/Bereitschaftsbetrieb einstellbar. Abmessungen **142×29×22 mm (LxBxH)**.
- **Elektronikbox MU05-Box (NLMU05BOX):** Kunststoffgehäuse **IP65** mit eingebautem MU05 + Anschlussklemmen, für feuchte oder abgesetzte Einbausituationen. Abmessungen **176×125×82 mm (BxHxT)**, für Leuchten 4–200 VA.

**Mischbetriebs-Leuchtenmanager MT400 (NLMT400 / NLMT400V):** elektronisches Vorschaltgerät für Leuchtstoffröhren mit Einzelleuchtenüberwachung, **Leistungsbereich 4–14W** (Leuchtstoff LL 4/6/8/14W; CFL 5/7/9/11/13W); automatische Anpassung; Softstart. Integriert Leuchtencontrollerfunktionen des MU05, Netzwächter, Schalteingang, alle Schaltarten. Für microControl/miniControl/MidiControl/MultiControl. Abmessungen **143×38×27 mm (LxBxH)**. NLMT400V = Service-EVG für ZDCL mit SKB.

**Prozessorgesteuerter Notlichteinsatz LPU für LED (NLLPUV5):** geeignet für **1W–5W ERT-LED**, 5-11-fach Low-Power-Streifen, 12V LED-Module nach **EN 60598-2-22, DIN VDE 0108, ÖVE E8002**. Schaltarten DS / BS / geschaltetes DS; Dimmfunktion; einstellbare Notbetriebszeit **1h / 3h / 8h** + Blinkbetrieb; integrierte Notlichtblockierung (F+f); Batterieladeeinrichtung mit Ladekontroll-LED; Fernausschaltvorrichtung; Funktionstest über externen Prüftaster; integrierte SELF-Control-Überwachung (SC); Anschluss für **4,8V bzw. 9,6V NiMh-Akku**. Abmessungen **142×29×22 mm (LxBxH)**.

**Umschaltweiche UW220 / UW500 (NLUW2200 / NLUW5000):** Betrieb von WR-Geräten (EVG mit 1 Einspeisung AC/DC) an Zentralbatterieanlagen über 2 Zuleitungen. Max. Umschaltleistung **250 bzw. 500 VA**. Wechselspannung über Lichtschalter der Raumbeleuchtung, AC/DC über Zentralbatterieanlage geschaltet; zeitverzögerter Noteingang mit vorheriger Abschaltung des Netzeingangs; UW500 Montage TS35. Abmessungen UW220 **100×44×32 mm**, UW500 **54×90×59 mm (BxHxT)**.

**Umschaltweiche BEPUE1 (NLBEPUE1):** mit integrierter Einphasen-Netzüberwachung. Sicherheitsleuchten im Netzbetrieb gemeinsam mit Allgemeinbeleuchtung über gemeinsame Lichtschalter schaltbar; bei Ausfall der Allgemeinbeleuchtung oder Unterschreiten von **85%** Netzspannung selbsttätige Umschaltung auf Dauerlichtkreis der Sicherheitsbeleuchtung. Montage TS35. Abmessungen **55×97×58 mm (BxHxT)**.

**UH-Elektronikbox NLUHBOX:** Universal-Kunststoffgehäuse zur Aufnahme von LPU, MLED500, MU05, NT24. Einbau über Standard-Deckenausschnitt **74 mm** in Hohlraumdecke; min. Installationstiefe **100 mm** (hinterer Teil bis 45° abknickbar). Netzklemme für 2,5 mm² Leitungen; Zugentlastungen beidseitig. Material PC+ABS, UV-Schutz, schwer entflammbar. Abmessungen **250×55×38 mm (LxBxH)**. Für Betoneinbau empfohlen: Dosen HaloX-0 + HaloX-40 (Fa. Kaiser).

**Ersatzprüftaster für Einzelbatterienotleuchten:** Ersatz-Folienprüftaster von Schrack. NLTEST (Standard) · NLTESTSC (mit Autotest / SelfControl SC) · NLTESTWL (WirelessControl Professional).

### Batterien und Zubehör (S. 360, Beginn)
- Kapitelstart: **RPOWER Gerätebatterien OGIV Longlife 10–12 Jahre**; **RPOWER Panzerplatten-Batterien OPzV Longlife 20 Jahre**; Batteriegestelle und Zubehör (Detailtabellen folgen im nächsten Teil).
