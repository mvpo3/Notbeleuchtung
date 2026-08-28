# OVE E 8101:2025-10 — Notbeleuchtungs-Deltas gegenüber Ausgabe 2019
**Quelle:** elektro-planer knowledge/normen/OVE E8101_2025.txt (852 S.), via Teil-Digests (part4 = Teil 4-42, part13 = Teil 5-56/560 + Anhänge 56.A–56.E + 56.NE, part16 = Teil 7-710, Teil 7-718 aus Volltext S. 743–750) · **Übernommen:** 2026-08-28
**Einordnung:** AKTUELLE Errichtungsnorm-Ausgabe (löst 2019 ab). Ersetzt OVE E 8101:2019-01-01 + AC1:2020 sowie die OVE-Richtlinien R 2000-5-55N01/N02 und R 2000-7-7N54/N90/N95/N96 (jetzt eingearbeitet). Unser Bestands-Digest ist 2019 → hier nur die Änderungen für Notbeleuchtung. Nationale AT-Ergänzungen/Änderungen sind in der 2025-Ausgabe blau bzw. mit „AT" markiert; geänderte Stellen tragen einen Randstrich.

## Zusammenfassung der Änderungen (Notbeleuchtung)

Die Kern-Systematik von Teil 5-56 (Stromquellen, Sicherheitsstromkreise, Funktionserhalt, Sicherheitsbeleuchtung 560.9) bleibt inhaltlich weitgehend erhalten. Wichtig für die Engine sind aber **fünf harte Deltas**:

1. **Neues Verbot 560.7.13 (2025): RCD und AFDD dürfen NICHT zum Schutz von Sicherheitsstromkreisen verwendet werden** (Brandtemperatur → ungewollte Auslösung). In 2019 fehlte dieser explizite Satz. → Neuer OVE-Hard-Stop.
2. **Betriebsdauer-Tabelle 56.A.1.AT: mehrere Zeilen, die 2019 „a" (rein nach EN 1838) trugen, haben 2025 einen expliziten 1-h-Wert** (Garagen, Betriebsbauten, Bereiche mit besonderer Gefährdung), und „vorübergehende Aufbauten" steht jetzt fix auf **1 h** (2019: „≥ 1 h"). **Krankenhäuser + Pflegeheime** sind aus der 56.A-Zeile herausgelöst und tragen jetzt Verweis **„e → Teil 7-710"** (2019 stand hier noch „Umschaltzeit 15 s" bzw. „8 h" direkt in 56.A). Die 8-h-Kernwerte (Beherbergung, Wohnhochhaus > 32 m, Pflegeheim-Fluchtweg) sind **unverändert**.
3. **Teil 7-718 Versammlungsstätten: Personen-Schwelle für die Nationale Ergänzung 718.NE.1 von > 400 (2019) auf > 240 Personen (2025) gesenkt** (innerhalb Gebäuden); außerhalb weiter > 5 000. **Die 2019er Erleichterung für kleine Theater (≤ 400 Personen, Fußböden ≤ 1 m) ist in 2025 ersatzlos entfallen.** → Antipanik-/Dauerbetriebspflichten greifen jetzt bei deutlich mehr Objekten.
4. **Neue Bestimmung 560.9.17: jeder Einphasen-Wechselstromkreis der Sicherheitsbeleuchtung braucht einen eigenen Neutralleiter** — gemeinsamer N für > 1 Kreis nicht zulässig (Verweis 521.8.2). In 2019 nicht als eigene 560.9-Regel geführt (nur medizinisch in 710.52). → Stromkreis-Planungsregel.
5. **Neue quantitative Batterie-Lebensdauer für Zentralsysteme:** CPS-Batterien mind. **10 Jahre**, LPS-Batterien mind. **5 Jahre** Brauchbarkeitsdauer bei 20 °C (nach OVE EN 50171). 2019 nannte nur „wartungsarm/Industrieausführung" ohne Jahreswert.

Ergänzend: Funktionserhalt-Kabelnormen aktualisiert (feuerbeständige Kabel jetzt **OVE EN IEC 60331-1** + 60332-1-2 statt „OVE EN 50200 + EN 60332-1-2"); neuer informativer **Anhang 56.E** (Leiterwiderstand-Erhöhung im Brandfall, Berechnung); Anhang **56.C Feuerwehrschalter** ausdrücklich in AT NICHT übernommen. Betriebsdauer-Tabelle 56.A ist in 2025 **normativ** (2019 informativ).

## Delta-Tabelle

| Abschnitt | 2019 | 2025 | Auswirkung für die Engine |
|---|---|---|---|
| 560.7.13 (Stromkreise) | keine explizite RCD/AFDD-Regel | **RCD und AFDD dürfen NICHT für Sicherheitsstromkreise verwendet werden** | Neuer Hard-Stop; Stromkreis-Generator darf keine RCD/AFDD in SV-Endstromkreisen setzen |
| 560.9.17 (Sicherheitsbeleuchtung) | nicht als 560.9-Regel geführt | **eigener Neutralleiter je Einphasen-Wechselstromkreis** (gemeinsamer N für > 1 Kreis unzulässig, 521.8.2) | Stromkreis-Aufteilung: kein N-Sharing zwischen SV-Kreisen |
| 560.9.001.AT Prüfdauer | „Prüfdauer 0,5–5 min" | **„Prüfdauer höchstens 5 min"** (Untergrenze 0,5 min entfällt) | Nur Doku/Prüf-Metadaten; platzierungsneutral |
| 560.9.002.AT (neu) | — | **Bereiche mit Brandmeldeanlage: bei Ansprechen Sicherheitsbeleuchtung aktivieren** | Schaltlogik-Regel (Ansteuerung), kein Platzierungsdelta |
| 560.6.10 CPS-Batterie | „wartungsarm, Industrieausführung" | zusätzlich **Brauchbarkeitsdauer ≥ 10 Jahre bei 20 °C** (EN 50171) | Produktauswahl CPS |
| 560.6.11/.10.002 LPS-Batterie | 500 W/3 h; 1 500 W/1 h | Werte gleich **+ Brauchbarkeitsdauer ≥ 5 Jahre bei 20 °C** | Produktauswahl LPS; Leistungsgrenzen unverändert |
| 560.8.1 Funktionserhalt-Kabel | mineralisoliert EN 60702-1/-2; feuerbeständig **OVE EN 50200** + EN 60332-1-2; DIN 4102-12 | mineralisoliert EN 60702-1/-2 + **60332-1-2**; feuerbeständig **OVE EN IEC 60331-1** + 60332-1-2; DIN 4102-12 | Nur Normverweis-Update; Funktionserhalt-Logik gleich |
| 560.7.2 Schacht-Ausnahme | Verbot BE3 / Aufzugsschächte | gleich, **+ Klarstellung: Elektro-Steigschächte gelten nicht als kaminähnliche Schächte** | Verlegeregel etwas gelockert (Klarstellung) |
| Anhang 56.A Status | **informativ** | **normativ** | Betriebsdauern jetzt verbindlich (nicht nur Leitfaden) |
| 56.A „vorübergehende Aufbauten" | ≥ 1 h | **1 h** | Betriebsdauer fixiert |
| 56.A „Garagen/Stellplätze/Parkdecks" | a (nach EN 1838) | **1 h** | Betriebsdauer jetzt fix 1 h |
| 56.A „Betriebsbauten (OIB)" | a (nach EN 1838) | **1 h** | Betriebsdauer jetzt fix 1 h |
| 56.A „Bereiche besonderer Gefährdung" | a (Anpassung EN 50172) | **1 h** (Fußnote d: Anpassung nach EN 50172 + Risikobeurteilung weiterhin möglich) | Default 1 h, per Risikobeurteilung änderbar |
| 56.A Wohn-/Gebäude Fluchtniveau | ≤ 22 m: a · > 22 m: 3 h · Wohn-HH > 32 m: 8 h | **GK-fein aufgeschlüsselt** (11.1/11.2 FLN ≤ 22 m = a; 12.1 Wohn > 22–32 m = a; 12.2 Wohn > 32 m = **8 h**; 12.3 sonstige > 22 m = **8 h**) | Zeilen-Zuordnung präziser; > 32-m-Wohnbau bleibt 8 h; sonstige Gebäude > 22 m jetzt 8 h |
| 56.A Krankenhäuser | a; **Umschaltzeit 15 s** direkt in 56.A | **e → Teil 7-710** (Wert dort: SV-Umschaltzeit ≤ 15 s, SV-Klassen) | Engine muss für KH/Pflegeheim in Teil 7-710 nachschlagen, nicht in 56.A |
| 56.A Pflegeheime | 8 h (Fußnote → 7-710) | **e → Teil 7-710** (dort: Fluchtweg-Sicherheitsbeleuchtung 8 h gesamt, 710.NE1.2) | 8-h-Wert steht jetzt in 7-710, nicht mehr in 56.A |
| 56.A Beherbergung / Heime / Schulen / Versammlung / Verkauf | 8 h / 3 h / 3 h / 3 h / 3 h | **unverändert** (8 / 3 / 3 / 3 / 3 h) | keine Änderung |
| 56.A Fußnote c (Batterie-Reduktion) | Batterie-Nenndauer auf 1 h reduzierbar mit Zusatz-Aggregat | **unverändert** | keine Änderung |
| 56.A Spalten (Systeme) | 7 Spalten; Aggregat 0 s / ≤ 0,5 s / ≤ 15 s (Extraktionslücke E1 2019) | **klar benannt: CPS / LPS / Einzelbatterie / Aggregat Klasse A (unterbrechungsfrei) / Klasse C (≤ 0,5 s) / Klasse E (≤ 15 s)** | Extraktionslücke E1 aus 2019 ist mit den 2025-Spaltennamen aufgelöst (Klassen A/C/E) |
| 56.B Brandschutzeinrichtungen | Löschwasser 12 h · FW-Aufzug 8 h · Alarm 3 h · RWA 3 h · CO 1 h (je /15 s) | **unverändert** | keine Änderung |
| 56.NE Erstprüfung/Wiederkehrend | jährl. Aggregat-Test, 3-Jahres-Lux-Messung etc. | **inhaltlich unverändert**; Normverweise aktualisiert (EN IEC 62485-2/-5 statt EN 50272-2) | Prüf-Metadaten; platzierungsneutral |
| Teil 4-42 §422.2.1 (Fluchtwege) | SV-Kabel Feuerwiderstand: R 12-2 / Behörde / sonst **1 h**; „notwendiges Treppenhaus" OIB 2:**2019** | gleiche 1-h-Default-Regel; Verweis auf **OIB-Richtlinie 2:2023** | Funktionserhalt-Default 1 h unverändert; nur OIB-Fassung neuer |
| Teil 4-42 §421.7 AFDD (neu prominent) | AFDD nur knapp | **AFDD-Pflicht** in Schlafräumen von Senioren-/Pflegeheimen, Kindergärten/Krippen + BE2-Räumen (AC ≤ 16 A) | Betrifft Allgemeininstallation, nicht Sicherheitskreise (dort 560.7.13 = AFDD verboten) |
| Teil 7-718 Schwelle 718.NE.1 | > **400** Personen (innen) / > 5 000 (außen) | > **240** Personen (innen) / > 5 000 (außen) | Antipanik-/Versammlungsstätten-Regeln greifen bei mehr Objekten |
| Teil 7-718 Kleintheater-Erleichterung | Theater ≤ 400 Pers., Böden ≤ 1 m: reduzierte Sicherheitsbeleuchtung zulässig | **entfällt (in 2025 nicht mehr vorhanden)** | Keine Sonder-Erleichterung mehr für kleine Theater |
| Teil 7-718 Zusatz-Orte 560.9.001.AT Nr. 1 | Fahrtreppen, Sanitär ≥ 8 m², **barrierefreie WC-Anlagen** | Fahrtreppen, Sanitär ≥ 8 m², **WC-Anlagen für Menschen mit Behinderung** | inhaltlich gleich; nur Formulierung |
| Teil 7-718 Zusatz-Orte Nr. 2 + Nr. 3 (Aggregat-/HV-Räume, Schaltanlagen > 1 kV, Brandschutz-Bedienräume; verkehrstechn. Wartezonen/Hallen/Flächen > 60 m²) | identisch | **unverändert** | keine Änderung |
| Teil 7-718 Antipanik-Orte 718.NE.1.560.9 (Bühnenbetriebsräume > 20 m², Bildwerfer, Manegen, Sportrennbahnen, Stehplatzbereiche) | identisch | **unverändert** | keine Änderung |
| Teil 7-718 Dauerbetriebspflicht 718.NE.1.560.9.4 (Fluchtwege außerhalb Versammlungsraum/Bühne, Fluchtweg-Hinweise) | identisch | **unverändert** | keine Änderung |
| Teil 7-718 Garagen-NE | > 1 600 m²; Steckdosen nicht an Allgemeinbeleuchtung | **unverändert** | keine Änderung |
| Teil 7-710 (medizinisch) | SV-Klassen ≤ 0,5 s / ≤ 15 s / > 15 s; Fluchtweg 2 Stromquellen; Pflegeheim Fluchtweg 8 h | **inhaltlich unverändert**; Klassen jetzt als **A / C / E / F** benannt (710.560.4.1); Zusatzschutz-Schwellen präzisiert (> 63 A → RCD 0,3 A) | KH/Pflegeheim-Werte stabil; nur Klassenbezeichnung + RCD-Details neu |

## Betriebsdauern Anhang 56.A (2025) — vollständig (Tabelle 56.A.1.AT, jetzt normativ)

Beleuchtungsstärke + Zeit bis Erreichen = Ausführung nach **ÖNORM EN 1838:2025** (Fußnote a). Zulässige Stromquellen-Spalten (X = zulässig): CPS ohne Leistungsbegrenzung / CPS mit Leistungsbegrenzung (= LPS) / Einzelbatteriesystem / Aggregat **Klasse A** (unterbrechungsfrei) / **Klasse C** (≤ 0,5 s) / **Klasse E** (≤ 15 s).

| Nr. | Räume/Anlagen besonderer Art | Bemessungsbetriebsdauer (h) | Δ ggü. 2019 |
|---|---|---|---|
| 1 | Räume für größere Personenzahl / Versammlungsstätten (Theater, Kinos, Sportstätten, Schwimmhallen, Sitzungssäle, Bühnen, Szenenflächen) | 3 | = |
| 2 | vorübergehend errichtete Aufbauten | 1 | 2019 „≥ 1 h" → jetzt fix 1 h |
| 3 | Ausstellungsstätten | 3 | = |
| 4 | Verkaufsstätten | 3 | = |
| 5 | Gaststätten | 3 | = |
| 6 | Beherbergungsstätten + vergleichbar | 8 | = |
| 7 | Studenten-/Alters-/Altenwohn-/Seniorenheime, -residenzen + vergleichbar | 3 | = |
| 8 | Schul-/Kindergartengebäude, Universitäten/Hochschulen, FH, VHS, Bildungsstätten | 3 | = |
| 9 | Garagen, überdachte Stellplätze, Parkdecks | 1 | 2019 „a" → jetzt fix 1 h |
| 10 | Öffentlich zugängliche Bereiche verkehrstechnischer Einrichtungen (Flughäfen, Bahnhöfe) | 3 | = |
| 11.1 | Wohngebäude GK 5 außerhalb Wohnungen (FLN ≤ 22 m) | a (EN 1838) | Zeile 2019 zusammengefasst; Wert = |
| 11.2 | Sonstige Gebäude GK 4 + GK 5 (FLN ≤ 22 m) | a (EN 1838) | = |
| 12.1 | Wohngebäude außerhalb Wohnungen, FLN > 22 m und ≤ 32 m | a (EN 1838) | neu aufgeschlüsselt |
| 12.2 | Wohngebäude außerhalb Wohnungen, FLN > 32 m | 8 | = (2019: Wohn-HH > 32 m = 8 h) |
| 12.3 | Sonstige Gebäude, FLN > 22 m | 8 | 2019: „> 22 m = 3 h" → jetzt 8 h (Verschärfung) |
| 13 | Betriebsbauten gemäß OIB-Richtlinien | 1 | 2019 „a" → jetzt fix 1 h |
| 14 | Bereiche mit besonderer Gefährdung | 1 (Fußnote d) | 2019 „a" → jetzt 1 h; Anpassung per EN 50172 + Risikobeurteilung |
| 15 | Krankenhäuser | e → Teil 7-710 | 2019 „a, Umschaltzeit 15 s" direkt in 56.A → jetzt Verweis 7-710 |
| 16 | Pflegeheime | e → Teil 7-710 | 2019 „8 h" direkt → jetzt Verweis 7-710 (dort Fluchtweg 8 h) |
| 17 | Arbeitsstätten (ArbeitnehmerInnenschutzgesetz) | siehe Arbeitsstättenverordnung | = |

Fußnoten 2025: (a) Ausführung nach ÖNORM EN 1838:2025; (b) Einzelbatterie: Herstellerangaben/Umgebungstemperaturen beachten; (c) Bemessungsdauer mind. nach Tabelle (R 12-2), Batterie-Nenndauer auf **1 h** reduzierbar mit zusätzlichem Aggregat, wenn Hauptverteiler am Aggregat + Aggregat sichert die geforderte Nenndauer; (d) Änderung nach OVE EN 50172 + Risikobeurteilung möglich; (e) siehe Teil 7-710.
Legende: **■** = Sicherheitszeichen für Fluchtwege/gesicherte Fluchtbereiche im Dauerbetrieb während betriebserforderlicher Zeit; FLN = Fluchtniveau; GK = Gebäudeklasse.

**Fazit 56.A: Ja, die Tabelle 56.A.1.AT hat sich geändert** — aber nicht bei den „großen" 8-h/3-h-Werten (die sind stabil), sondern (i) durch Konkretisierung mehrerer „a"-Zeilen auf fix **1 h** (Garagen, Betriebsbauten, besondere Gefährdung, vorüb. Aufbauten), (ii) durch Herauslösen von Krankenhaus/Pflegeheim nach Teil 7-710 (Fußnote e), (iii) durch feinere Fluchtniveau-/Gebäudeklassen-Zeilen (sonstige Gebäude > 22 m jetzt **8 h** statt 3 h) und (iv) durch den Status-Wechsel informativ → **normativ**.

## Neue/geänderte Pflicht-Orte (Teil 7-718)

- **Schwelle Versammlungsstätten gesenkt:** 718.NE.1 gilt jetzt ab **> 240 Personen** innerhalb von Gebäuden (2019: > 400). Außerhalb von Gebäuden unverändert **> 5 000 Personen**. → Antipanikbeleuchtung, Dauerbetriebspflicht für Fluchtwege außerhalb der Versammlungsräume/Bühnen und Antipanik-Schaltanforderungen (keine Dimmung, beleuchtete Schaltstellen je Ausgang) greifen bei deutlich kleineren Objekten.
- **Kleintheater-Erleichterung entfallen:** Die 2019er Sonderregel (Theater/Film ≤ 400 Personen, Fußböden ≤ 1 m über/unter Fluchtweg-Verkehrsflächen → reduzierte Sicherheitsbeleuchtung, nur Türen/Gänge/Stufen erkennbar) ist in 2025 nicht mehr enthalten.
- **Zusatz-Orte 718.560.9.001.AT (unverändert im Inhalt, WC-Formulierung angepasst):**
  - Nr. 1: Fahrtreppen, Sanitärbereiche **ab 8 m²**, **WC-Anlagen für Menschen mit Behinderung** (2019: „barrierefreie WC-Anlagen").
  - Nr. 2: Räume für Sicherheits-/Ersatzstromaggregate, Hauptverteiler-Räume (SV/Ersatz/allgemein), Schaltanlagen **> 1 kV**, Bedienräume zentraler Brandschutzeinrichtungen (Sprinkler-/Brandmeldezentrale).
  - Nr. 3 (verkehrstechnische Einrichtungen, zusätzlich zu 1+2): Antipanikbeleuchtung in Wartezonen, Abfertigungshallen, Geschäftsflächen **> 60 m²**, Arbeits-/betriebsnotwendigen Räumen **> 60 m²**.
- **Neue Hinweise (2025, ANMERKUNG 2.AT):** bei erweiterten Gefahrenmomenten laut Risikobewertung kann ein **elektrisch betriebenes Sicherheitsleitsystem** erforderlich sein; **optische Sicherheitsleitsysteme ersetzen keine Sicherheitsbeleuchtung**.
- **Neu 718.NE.1.415.1.003.AT / .559:** Leuchten im Handbereich in Umkleide-/Masken-/Dekorations-/Lagerräumen → RCD IΔn ≤ 0,03 A; dort nur fest montierte Leuchten (Allgemein-, keine Sicherheitsbeleuchtungs-Regel, aber platzierungs-nah).
- **Antipanik-Orte 718.NE.1.560.9 unverändert:** Versammlungsstätten, Bühnenbetriebsräume > 20 m² (Probebühnen, Chor-/Ballett-/Orchester-Übungsräume, Stimmzimmer, Aufenthaltsräume Mitwirkender), Bildwerferräume, Manegen, Sportrennbahnen, Stehplatzbereiche mit nicht überdachten Spielflächen.
- **Garagen 718.NE.2 unverändert:** gilt ab **> 1 600 m²**; Steckdosen im Einstellplatz-/Verkehrsflächenbereich nicht an Stromkreise der allgemeinen Beleuchtung.

## Unverändert (kurz bestätigt)

- **560.9.1/.9.2 Kernregel Platzierung:** in Brandabschnitten mit > 1 Sicherheitsleuchte → Leuchten **abwechselnd auf mind. 2 Stromkreise** verteilen (Grundbeleuchtung bei Kreisausfall). Unverändert.
- **560.9.3 Endstromkreis-Grenzen:** **≤ 20 Leuchten** und **≤ 60 % des Nennstroms** der Überstrom-Schutzeinrichtung. Unverändert.
- **560.9.001.AT Prüfeinrichtung:** ab **> 20 Sicherheitsleuchten** je zusammenhängendem Gebäudeteil automatische Prüfeinrichtung nach EN 62034 (Ladungsüberwachung < 5 min, tägliche Funktionsprüfung). Unverändert (nur Prüfdauer-Untergrenze entfällt).
- **560.6.1 / 560.6.23 Primärzellen-Verbot:** Batterien mit Primärzellen für Sicherheitsbeleuchtungsanlagen **verboten**. Unverändert.
- **560.9.10 Umschaltschwellen:** Notbetrieb bei U < **0,6 × Un** für > 0,5 s; Rückschaltung bei U > **0,85 × Un**. Unverändert.
- **560.4 Umschaltzeit-Klassen:** unterbrechungsfrei / ≤ 0,15 s / ≤ 0,5 s / ≤ 5 s / ≤ 15 s / > 15 s. Unverändert.
- **LPS-Leistungsgrenzen:** 500 W/3 h bzw. 1 500 W/1 h. Unverändert.
- **Funktionserhalt-Erdverlegung:** getrennte Trassen ≥ 2 m horizontal bzw. Stufenkünette ≥ 1 m. Unverändert.
- **560.9.15 Kennzeichnung:** rotes/grünes Schild + Verteiler-, Stromkreis- und Leuchtennummer an/nahe der Leuchte. Unverändert (→ Render/Beschriftung).
- **Anhang 56.B (Brandschutzeinrichtungen):** Löschwasser 12 h · Feuerwehraufzug 8 h · Alarm/Evakuierung 3 h · RWA/Druckbelüftung 3 h · CO-Warnanlage 1 h (je Umschaltzeit 15 s). Unverändert.
- **Teil 4-42 §422.2:** Fluchtweg-Kabel-Verbote + SV-Kabel-Funktionserhalt-Default **1 h** (mangels R-12-2-/Behördenwert). Unverändert (nur OIB-Verweis 2019 → 2023).
- **Teil 7-710:** SV-Klassen (≤ 0,5 s / ≤ 15 s / > 15 s), Fluchtweg-Leuchten abwechselnd auf 2 Stromquellen (1× SV), Pflegeheim-Fluchtweg **8 h**, Gr.2-Raumbeleuchtung ≥ 50 % aus SV ≤ 15 s. Inhaltlich unverändert (Klassenbezeichnung jetzt A/C/E/F).
- **Normverweis-Dreieck 560.9:** WO nach Nutzung → R 12-2; WIE errichten → EN 50172; Lichtwerte → EN 1838. Unverändert.

## Offene Punkte / Extraktionslücken

- **[D1] Teil 7-718 nicht in den Teil-Digests part16/part17 enthalten** (part16 endet auf S. 680 mit Teil 7-710, part17 beginnt S. 681 mit 710-Bildern + 7-711). Die 718-Deltas oben (Schwelle 240, WC-Formulierung, Zusatz-Orte, entfallene Kleintheater-Erleichterung) wurden direkt aus dem **Volltext** OVE E8101_2025.txt S. 743–750 (Zeilen 43571–43977) verifiziert — belastbar.
- **[E1 aus 2019 aufgelöst] 56.A-Spaltenzuordnung:** Die 2019er Unsicherheit über die 7 System-Spalten ist durch die 2025-Spaltennamen (CPS / LPS / Einzelbatterie / Aggregat Klasse A/C/E) benannt; die exakten X/–-Markierungen je Zeile sind aus dem Text-Digest nicht sicher extrahierbar (Tabellenraster) — für harte System-Zulässigkeits-Regeln am PDF-Layout gegenprüfen.
- **[D2] R 12-2:** weiterhin durchgehend normativ referenziert (WO Sicherheitsbeleuchtung nach Nutzung, Funktionserhalt-Dauern, Aufstellräume). Liegt nicht im Repo — für vollständige „Erforderlichkeit je Nutzungsart" beschaffen; sonst LB/EN-1838-Default als Fallback. Bühnen-Beispielbild 710.NE2 verweist noch auf **R 12-2:2019**.
- **[D3] EN 1838:** Die 56.A-Fußnote a verweist jetzt explizit auf **ÖNORM EN 1838:2025** — prüfen, ob unser EN-1838-Digest (2019) upzudaten ist (separate Norm, nicht Teil dieses Deltas).
- **[D4] Betriebsdauer „sonstige Gebäude FLN > 22 m" (Zeile 12.3) = 8 h:** Diese Zahl stammt aus dem part13-Digest; da es eine potenzielle Verschärfung ggü. 2019 (3 h) ist, vor Engine-Hardcoding am PDF verifizieren.
