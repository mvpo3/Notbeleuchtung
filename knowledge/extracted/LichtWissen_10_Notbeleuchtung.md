# licht.wissen 10 — Notbeleuchtung, Sicherheitsbeleuchtung (Februar 2016)
**Quelle:** knowledge/1603_lw10_Notbeleuchtung_web.pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
**Einordnung:** Referenz-Praxis (DE-Branchenpublikation; DIN/VDE-lastig — AT-Geltung nur wo EN-identisch)

Herausgeber: licht.de — Fördergemeinschaft Gutes Licht, eine Brancheninitiative des ZVEI e.V.
ISBN Druck 978-3-945220-12-2 · ISBN PDF 978-3-945220-13-9 · Stand Februar 2016 (S. 51).

**ACHTUNG DE/AT:** Das Heft argumentiert durchgehend mit deutschem Recht (ArbStättV, ASR,
Muster-Bauverordnungen MVStättV/MBeVO/MVkVO/MGarVO/MBO/MHHR/MSchulbauR, DIN V VDE V 0108-100).
Für die Engine (Österreich) sind nur die EN-identischen Inhalte direkt gültig (DIN EN 1838 = EN 1838,
DIN EN ISO 7010, DIN EN 12193, DIN EN 50172, DIN EN 60598-2-22, DIN EN 62034, DIN EN 50171).
DE-only-Regeln dienen als Referenz-Praxis-Analogie; AT-Pendants stehen in OVE E 8101 / ÖNorm
(siehe `knowledge/extracted/` — EN-1838- und OVE-Regeln dort NICHT dupliziert, nur referenziert).
Einzige explizite AT-Aussage im Heft: 2.000-m²-Schwelle für Verkaufsstätten gilt „gleichermaßen auch
in Österreich" (S. 42).

## Relevanz für die Engine

1. **Platzierungs-Checkliste (S. 10/11, Abb. 7/8)** — die kompakteste Praxis-Liste der
   „hervorzuhebenden Stellen" nach EN 1838 inkl. der 2-m-Horizontalabstand-Regel („nahe" = max. 2 m):
   direkt als Platzierungs-Trigger-Katalog für Leonis' `NotlichtPlatzierer` nutzbar (Türen,
   Niveauänderungen, Treppen, Richtungsänderungen, Kreuzungen, Erste-Hilfe/Brandmelde-Stellen 5 lx
   vertikal, Barrierefreiheits-Punkte).
2. **Erkennungsweiten-Faustformeln (S. 23)** — l = h·200 (hinterleuchtet) / l = h·100 (beleuchtet):
   deckt sich mit dem Distanzfaktor-Modell l = z·h aus EN 1838 (z=200 bzw. z=100); bestätigt die
   bestehende Engine-Formel.
3. **Gebäudetyp-Tabelle (S. 46, DIN V VDE V 0108-100)** — Umschaltzeit + Bemessungsbetriebsdauer +
   zulässige Stromquellen je Gebäudetyp: als DE-Referenz-Praxis für LB-Lücken; AT-Werte aus
   OVE E 8101 haben Vorrang.
4. **RZ-Betriebslogik** — Rettungszeichenleuchten praktisch immer in Dauerschaltung; beleuchtetes
   (nicht hinterleuchtetes) Schild braucht eigene Sicherheitsleuchte in max. 2 m Abstand: relevant für
   Symbolwahl/Stückzahllogik.
5. **Priorisierung hinterleuchteter RZ** — doppelte Erkennungsweite bei gleicher Zeichenhöhe,
   rauchresistenter: Default-Empfehlung der Engine, wenn LB nichts vorgibt.

## Planungsregeln-Tabelle

IDs LW10-R1… · Seitenangaben = PDF-Seitenmarker. „DE-only?": **ja** = deutsches Recht/deutsche Norm
ohne EN-Basis · **teilw.** = gemischt (EN-Kern + DE-Zusatz) · **nein** = EN-identisch/AT-anwendbar.

### A. Platzierung von Sicherheits-/Rettungszeichenleuchten (EN 1838)

| ID | Kapitel (Seite) | Regel/Faustformel | Werte | zitierte Norm | DE-only? |
|----|-----------------|-------------------|-------|---------------|----------|
| LW10-R1 | Sicherheitsbeleuchtung (S. 10, 11) | Leuchten zur Ausleuchtung und Kennzeichnung des Fluchtwegs mindestens 2 m über dem Boden anbringen | ≥ 2 m Montagehöhe | DIN EN 1838 | nein |
| LW10-R2 | Sicherheitsbeleuchtung (S. 10) | Leuchte an jeder im Notfall zu benutzenden Ausgangstür | — | DIN EN 1838 | nein |
| LW10-R3 | Sicherheitsbeleuchtung (S. 10) | Leuchte nahe jeder Niveauänderung im Fluchtweg (z. B. Rampe, Podest); „nahe" = max. 2 m Abstand in der Horizontalen | ≤ 2 m horizontal | DIN EN 1838 | nein |
| LW10-R4 | Sicherheitsbeleuchtung (S. 10) | Leuchte außerhalb und nahe jedes Notausgangs bis zu einem sicheren Bereich | ≤ 2 m horizontal | DIN EN 1838 | nein |
| LW10-R5 | Sicherheitsbeleuchtung (S. 10) | Leuchte nahe Treppen, um jede Treppenstufe direkt zu beleuchten | ≤ 2 m horizontal | DIN EN 1838 | nein |
| LW10-R6 | Sicherheitsbeleuchtung (S. 10) | Leuchte nahe jeder Erste-Hilfe-Stelle; dort vertikale Beleuchtungsstärke 5 Lux | ≤ 2 m horizontal; Ev = 5 lx | DIN EN 1838 | nein |
| LW10-R7 | Sicherheitsbeleuchtung (S. 10) | Leuchte nahe jeder Brandbekämpfungs- oder Meldeeinrichtung; dort vertikale Beleuchtungsstärke 5 Lux | ≤ 2 m horizontal; Ev = 5 lx | DIN EN 1838 | nein |
| LW10-R8 | Sicherheitsbeleuchtung (S. 10) | Leuchte nahe Fluchtgeräten für Menschen mit Behinderung | ≤ 2 m horizontal | DIN EN 1838 | nein |
| LW10-R9 | Sicherheitsbeleuchtung (S. 10) | Leuchte nahe Schutzbereichen für Menschen mit Behinderung und deren Rufanlagen/Kommunikationseinrichtungen sowie Alarmeinrichtungen in Behindertentoiletten; Antipanikbeleuchtung in Toiletten für Menschen mit Behinderung | ≤ 2 m horizontal | DIN EN 1838 | nein |
| LW10-R10 | Sicherheitsbeleuchtung (S. 10) | Leuchte an jeder Kreuzung der Flure/Gänge | — | DIN EN 1838 | nein |
| LW10-R11 | Sicherheitsbeleuchtung (S. 10, 11) | Leuchte/Kennzeichnung bei jeder Richtungsänderung des Fluchtwegs | — | DIN EN 1838 | nein |
| LW10-R12 | Sicherheitsbeleuchtung (S. 10) | Antipanikbeleuchtung auch auf Wegen zu Räumen, in denen Sicherheitsbeleuchtung erforderlich ist, die aber nicht direkt an einen Fluchtweg angrenzen | — | DIN EN 1838 | nein |
| LW10-R13 | Sicherheitsbeleuchtung (S. 10; S. 7) | Sicherheits- und Richtungszeichen an Fluchtwegen müssen auch bei ungestörter Allgemeinbeleuchtung be- oder hinterleuchtet sein (RZ-Leuchten während der Betriebszeiten stets eingeschaltet, Mindesthelligkeit) | Dauerschaltung | DIN EN 1838 / DIN 4844 | nein |
| LW10-R14 | Sicherheitsbeleuchtung (S. 11) | Ist ein Notausgang nicht direkt zu sehen, müssen ein oder mehrere beleuchtete oder hinterleuchtete Rettungszeichen entlang des Fluchtwegs installiert werden | — | DIN EN 1838 | nein |
| LW10-R15 | Fluchtwege (S. 12; S. 22) | An jeder Stelle eines Fluchtwegs muss mindestens ein Rettungszeichen erkennbar sein (Orientierung, Tür im Wegverlauf oder Notausgang) | ≥ 1 RZ sichtbar | DIN EN 1838 | nein |

### B. Lichttechnik Fluchtwege

| ID | Kapitel (Seite) | Regel/Faustformel | Werte | zitierte Norm | DE-only? |
|----|-----------------|-------------------|-------|---------------|----------|
| LW10-R16 | Fluchtwege (S. 12) | Fluchtwege werden normseitig immer auf Streifen von 2 m Breite bezogen; breitere Wege = mehrere 2-m-Streifen | 2-m-Streifen-Modell | DIN EN 1838 | nein |
| LW10-R17 | Fluchtwege (S. 12, 14, 15) | Horizontale Beleuchtungsstärke auf der Mittelachse des Fluchtwegs mindestens 1 Lux; Messhöhe 2 cm über Laufebene (EN 1838) bzw. bis 20 cm (ASR) | Emin = 1 lx; Messhöhe 2 cm (EN) / ≤ 20 cm (ASR) | DIN EN 1838; ASR A3.4/3 | teilw. (ASR-Messhöhe DE) |
| LW10-R18 | Fluchtwege (S. 14) | Im Abstand von 0,5 m links/rechts der Mittellinie darf die Beleuchtungsstärke um jeweils 50 % abnehmen | ±0,5 m → −50 % zulässig | ASR A3.4/3 | ja |
| LW10-R19 | Fluchtwege (S. 12, 14, 15) | Gleichmäßigkeit: Verhältnis größte:kleinste Beleuchtungsstärke entlang der Mittellinie max. 40:1 — gilt für den ungünstigsten Fall (z. B. Ende der Bemessungsbetriebsdauer, zwischen zwei Leuchten) | Emax:Emin ≤ 40:1 | DIN EN 1838; ASR A3.4/3 | nein |
| LW10-R20 | Fluchtwege (S. 14) | Innerhalb von 15 s nach Ausfall der Allgemeinbeleuchtung muss die Sicherheitsbeleuchtung 100 % Lichtleistung erreicht haben; Aggregate mit Verbrennungsmotor haben meist selbst 15 s Umschaltzeit → dafür nur batteriegestützte Stromquellen geeignet | ≤ 15 s → 100 % | DIN EN 1838 / ASR (Heftaussage; vgl. EN 1838: 50 % in 5 s, 100 % in 60 s — siehe Offene Punkte) | teilw. |
| LW10-R21 | Fluchtwege (S. 14, 15) | Farbwiedergabeindex der Lichtquellen mindestens Ra 40, damit Sicherheitszeichen und -farben erkannt werden | Ra ≥ 40 | DIN EN 1838 | nein |
| LW10-R22 | Fluchtwege (S. 12, 15) | Blendungsbegrenzung: max. Lichtstärke Imax je Montagehöhe h; bei horizontalen Fluchtwegen für alle Azimutwinkel in der Zone 60°–90° gegen die Vertikale; bei allen anderen Fluchtwegen/Bereichen bei keinem Winkel überschreiten | h≤2,5 m: 500 cd · 2,5≤h<3: 900 · 3≤h≤3,5: 1.600 · 3,5≤h≤4: 2.500 · 4≤h≤4,5: 3.500 · h≥4,5: 5.000 cd | DIN EN 1838 | nein |
| LW10-R23 | Fluchtwege (S. 14, 15) | Bemessungsbetriebsdauer der Sicherheitsbeleuchtung für Rettungswege 1 Stunde (Arbeitsstätten: mindestens 1 h); andere Anwendungsbereiche siehe Tabelle S. 46 (LW10-R68) | ≥ 1 h | DIN EN 1838 | nein |

### C. Arbeitsstätten und Arbeitsplätze mit besonderer Gefährdung

| ID | Kapitel (Seite) | Regel/Faustformel | Werte | zitierte Norm | DE-only? |
|----|-----------------|-------------------|-------|---------------|----------|
| LW10-R24 | Arbeitsstätten (S. 16) | Ob Sicherheitsbeleuchtung nötig ist, ergibt die dokumentationspflichtige Gefährdungsbeurteilung; wegen Dunkelheit in Wintermonaten ist „fast immer" eine Sicherheitsbeleuchtung notwendig (min. 1 lx) | E ≥ 1 lx | § 5, § 6 ArbSchG; ASR | ja |
| LW10-R25 | Arbeitsstätten (S. 16) | In Räumen, die jeder Arbeitnehmer gefahrlos verlassen kann, müssen nur die Ausgänge gekennzeichnet sein | — | ASR | ja |
| LW10-R26 | Arbeitsstätten (S. 16, 18, 19) | Arbeitsplätze mit besonderer Gefährdung: Sicherheitsbeleuchtung mit mindestens 15 Lux; ASR-Empfehlung: besser 10 % der vor Ort erforderlichen Allgemeinbeleuchtungsstärke | Emin ≥ 15 lx; Empfehlung 10 % der Allgemeinbel. | DIN EN 1838; ASR A3.4/3 | teilw. (10 %-Empfehlung DE) |
| LW10-R27 | Arbeitsstätten (S. 18, 19) | Besondere Gefährdung: Gleichmäßigkeit Emax:Emin max. 10:1 | ≤ 10:1 | DIN EN 1838 | nein |
| LW10-R28 | Arbeitsstätten (S. 18) | Besondere Gefährdung — Blendungsbegrenzung: Imax je Montagehöhe, für alle Azimutwinkel in der Zone 60°–90° gegen die Vertikale | h≤2,5 m: 1.000 cd · 2,5≤h<3: 1.800 · 3≤h≤3,5: 3.200 · 3,5≤h≤4: 5.000 · 4≤h≤4,5: 7.000 · h≥4,5: 10.000 cd | DIN EN 1838 | nein |
| LW10-R29 | Arbeitsstätten (S. 18, 19) | Besondere Gefährdung: erforderliche Beleuchtungsstärke nach spätestens 0,5 s erreichen (praktisch nur mit Dauerschaltung realisierbar); Bemessungsbetriebsdauer = solange die Gefährdung besteht (aus Gefährdungsbeurteilung) | ≤ 0,5 s; Dauer = Gefährdungsdauer | DIN EN 1838; ASR A3.4/3 | nein |
| LW10-R30 | Arbeitsstätten (S. 17) | Katalog „besondere Gefährdung": Labore mit akuter Gefährdung, betriebsbedingt dunkle Arbeitsplätze, elektrische Betriebsräume/Haustechnikräume, lang nachlaufende bewegte Arbeitsmittel, Schaltwarten/Leitstände, heiße Bäder/Gießgruben, offene Arbeitsgruben, Baustellen | — | ASR A3.4/3 Abs. 4.2; DIN EN 1838 | teilw. |
| LW10-R31 | Arbeitsstätten (S. 19) | Baustellen: Sicherheitsbeleuchtung zwingend, wenn Tageslicht die 1-lx-Fluchtwegbeleuchtung nicht sicherstellt (Abend-/Nachtarbeit); Kellergeschosse erhöhtes Niveau, z. B. min. 15 lx wie bei Tunnelbauarbeiten | 1 lx; Keller/Tunnel ≥ 15 lx | ASR A3.4/3 | ja |
| LW10-R32 | Arbeitsstätten (S. 16, 24) | Bei Verrauchungsgefahr im Brandfall muss zusätzlich zur Sicherheitsbeleuchtung ein optisches Sicherheitsleitsystem installiert werden; vorgeschrieben, wenn Verrauchung nicht ausgeschlossen und Fluchtwege breiter als 3,6 m | Zusatzpflicht ab > 3,6 m Wegbreite | ASR A3.4/3 | ja |
| LW10-R33 | Arbeitsstätten (S. 19) | Optische Leitsystem-Elemente (Schilder/Markierungen) an der Wand max. 40 cm über Boden oder direkt auf dem Boden montieren; kein Ersatz für Sicherheitsbeleuchtung, nur Ergänzung | ≤ 40 cm Montagehöhe | ASR A3.4/3 (Praxis) | ja |

### D. Antipanikbeleuchtung

| ID | Kapitel (Seite) | Regel/Faustformel | Werte | zitierte Norm | DE-only? |
|----|-----------------|-------------------|-------|---------------|----------|
| LW10-R34 | Antipanik (S. 20) | DE-Planungspraxis (mangels konkreter Basis in Baurecht/ASR): horizontale Beleuchtungsstärke 1 lx auf der freien Bodenfläche, Bemessungsbetriebsdauer 3 h | Eh = 1 lx; 3 h | Praxiskonvention DE (EN-1838-Default: 0,5 lx — siehe EN-1838-Extrakt, nicht dupliziert) | ja |
| LW10-R35 | Antipanik (S. 20) | Antipanikbeleuchtung erforderlich: große Hallen ohne eindeutig definierte Fluchtwege bzw. gesamte Hallenfläche als Rettungsweg; Konferenzräume > 60 m² ohne ausgewiesene Fluchtwege; kleinere Bereiche mit Panikrisiko durch Menschengruppen, z. B. Aufzugskabinen | > 60 m² (Konferenzräume) | Praxis / DIN EN 1838 | teilw. |
| LW10-R36 | Antipanik (S. 20) | Antipanikbeleuchtung direkt nach unten richten und Hindernisse beleuchten; Gleichmäßigkeit ≤ 40:1; Ra ≥ 40; Blendungsbegrenzung wie Fluchtwege (Tabelle S. 15) | 40:1; Ra ≥ 40 | DIN EN 1838 | nein |

### E. Rettungszeichen: Erkennungsweite, Photometrie, Pfeile

| ID | Kapitel (Seite) | Regel/Faustformel | Werte | zitierte Norm | DE-only? |
|----|-----------------|-------------------|-------|---------------|----------|
| LW10-R37 | Ausleuchtung (S. 23) | Erkennungsweite hinterleuchteter Zeichen: l = h · 200 (Beispiel: h = 15 cm → 30 m) | z = 200 | DIN EN 1838 | nein |
| LW10-R38 | Ausleuchtung (S. 23) | Erkennungsweite beleuchteter Zeichen (Schilder): l = h · 100 (Beispiel: h = 15 cm → 15 m); für gleiche Erkennungsweite doppelte Zeichenhöhe nötig | z = 100 | DIN EN 1838 / DIN 4844 | nein |
| LW10-R39 | Ausleuchtung (S. 22–23) | Montageempfehlung der Norm: be-/hinterleuchtete Rettungszeichen nicht höher als 20° über der horizontalen Blickrichtung — bezogen auf die maximale Erkennungsweite | ≤ 20° Blickwinkel | DIN EN 1838 (Beiblatt in Vorbereitung, Stand 2016) | nein |
| LW10-R40 | Ausleuchtung (S. 22) | Neuinstallationen: Rettungszeichen nach DIN EN ISO 7010 (E001/E002) mit Zusatzzeichen Richtungspfeil Typ D nach DIN ISO 3864-3; Altzeichen nach DIN 4844-2:2001 müssen laut ZVEI nicht ausgetauscht werden (gleichwertige Sicherheitsaussage) | E001/E002 + Pfeil Typ D | DIN EN ISO 7010:2012-10; ASR A1.3:2013-02; DIN ISO 3864-3 | teilw. (Bestandsschutz-Aussage DE) |
| LW10-R41 | Ausleuchtung (S. 23) | Photometrik-Vergleich Normalbetrieb (DIN 4844-1) vs. Notbetrieb (EN 1838): Gleichmäßigkeit Lmin/Lmax ≥ 0,2 vs. ≥ 0,1; Kontrast Lweiß:Lgrün = 5:1 bis 15:1; mittlere Leuchtdichte weiße Kontrastfarbe ≥ 500 cd/m² (4844-1, Netzbetrieb); Leuchtdichte grüne Sicherheitsfarbe ≥ 2 cd/m² (EN 1838); rechnerische mittlere Leuchtdichte gesamtes RZ ≥ 200 cd/m² (4844-1) vs. ≥ 5 cd/m² (EN 1838) | siehe Werte | DIN 4844-1 (2012-06); DIN EN 1838; ISO 3864-4 (Farben) | teilw. (DIN 4844-1 = DE) |
| LW10-R42 | Ausleuchtung (S. 23–24) | Beleuchtetes (nicht hinterleuchtetes) Rettungszeichen: zugehörige Sicherheitsleuchte max. 2 m vom Schild entfernt; Beleuchtungsstärke auf dem Zeichen vorzugsweise ≥ 80 lx (DIN 4844-1: ≥ 50 lx, vorzugsweise ≥ 80 lx, Netzbetrieb); im Notbetrieb ca. 30 lx auf dem Zeichen erforderlich; je beleuchtetem Zeichen eine eigene Sicherheitsleuchte in Dauerschaltung | ≤ 2 m Abstand; ≥ 50/80 lx Netz; ca. 30 lx Notbetrieb | DIN 4844-1; DIN EN 1838 | teilw. |
| LW10-R43 | Rettungszeichen (S. 24, Abb. 27) | Mindestleuchtdichte der weißen Kontrastfarbe im Notbetrieb 10 cd/m² (RZ-Leuchte, auch nach 60 min Betriebsdauer) | Lweiß ≥ 10 cd/m² | DIN EN 1838 | nein |
| LW10-R44 | Rettungszeichen (S. 24) | Lang nachleuchtende Rettungszeichen sind für die Sicherheitsbeleuchtung nur zulässig, wenn sie mit einer Sicherheitsleuchte beleuchtet werden (Sicherheitsfarbe Grün muss im Notfall „Grün" bleiben); lichtspeichernde Leitsysteme erfüllen Farbwiedergabe-/Beleuchtungsstärke-Vorgaben nicht | — | DIN EN 1838; Kommentar zur ArbStättV 2004 (Rz. 68) | teilw. |
| LW10-R45 | Rettungszeichen (S. 24) | Praxis-Vergleich Erkennungsweite (20-cm-Zeichen): RZ-Leuchte 40 m, beleuchtetes Schild 20 m, nachleuchtendes Schild nach 10 min nur noch ca. 5 m, nach 1 h nur unmittelbar davor lesbar; Leuchtdichte-Unterschied nach 60 min bis Faktor 1.000 | 40 m / 20 m / ~5 m | Herstellerpraxis (licht.de) | nein |
| LW10-R46 | Hoch oder runter? (S. 47) | Pfeilrichtung: keine verbindliche Festlegung; ISO 16069:2003 / DIN SPEC 4844-4 schlagen Pfeil nach oben für Wegverlauf vor; ZVEI-Empfehlung: Pfeil nach unten zusätzlich = „geradeaus gehen" und „geradeaus durch die Tür, wenn Zeichen über einer Tür" (vermeidet Fehlleitung nach oben in Mehrgeschossern) | — | ISO 16069:2003; DIN SPEC 4844-4; ZVEI-Positionspapier 2016 | teilw. |

### F. Leuchten, Stromquellen, Schaltung, Prüfung

| ID | Kapitel (Seite) | Regel/Faustformel | Werte | zitierte Norm | DE-only? |
|----|-----------------|-------------------|-------|---------------|----------|
| LW10-R47 | Leuchten (S. 26, 28) | Typenschild-Codierung von Sicherheitsleuchten: Abschnitt 1 Bauart (X = Einzelbatterie, Z = zentrale Versorgung); Abschnitt 2 Betriebsart (0 = Bereitschaft, 1 = Dauer, 2/3 = kombiniert, 4/5 = Mutter/Tochter, 6 = Tochterleuchte); Abschnitt 3 Einrichtungen (A Prüfeinrichtung, B Fernschaltung Ruhezustand, C Fernausschaltung, D Leuchte für besondere Gefährdung, E nicht tauschbare Lampe/Batterie, F Betriebsgerät mit autom. Prüfung nach IEC 61347-2-7 „EL-T", G von innen beleuchtetes Zeichen); Abschnitt 4 (nur Einzelbatterie) Betriebsdauer 10/60/120/180 min | Beispiel: X 1 AB\*\*\*\*\* 120 | DIN EN 60598-2-22; DIN EN 60598-1; DIN EN 62034 | nein |
| LW10-R48 | Leuchten (S. 29) | Zwei Realisierungsvarianten: A eigenständige Sicherheitsleuchten (optimierte Lichtverteilung, große Montageabstände, geringe Leistung) vs. B Allgemeinleuchten mit Notfunktion (kleinere Abstände, deutlich höhere Notstromkapazität). Rechenbeispiel Flur 3 m Höhe, g2 = 5:1: Variante A Montageabstand 15,6 m bei 6 W; Variante B 8 m bei 115 W | A: 15,6 m/6 W · B: 8 m/115 W | licht.de-Beispielrechnung | nein |
| LW10-R49 | Betrieb (S. 30) | Stromquellen für Sicherheitszwecke: zentrale Batteriesysteme nach DIN EN 50171; Einzelbatterieleuchten nach DIN EN 60598-2-22; Stromerzeugungsaggregate nach DIN 6280-13/-14; zwei unabhängige Netzeinspeisungen nur mit Nachweis (Bestätigung des Netzbetreibers), dass beide nicht gleichzeitig ausfallen können | — | DIN EN 50171; DIN EN 60598-2-22; DIN 6280-13/-14 | teilw. (DIN 6280 DE) |
| LW10-R50 | Betrieb (S. 30) | Ist nur eine Stromquelle für Sicherheitszwecke vorhanden, darf sie nicht für andere Zwecke genutzt werden | — | ASR A3.4/3 Pkt. 6.6 | ja |
| LW10-R51 | Betrieb (S. 30) | Drei Schaltungsarten: Bereitschaftsbetrieb (nur bei Netzausfall; in allen Gebäudearten für Fluchtwegbeleuchtung zulässig), Dauerbetrieb (RZ-Leuchten bis auf wenige Ausnahmen ausschließlich Dauerschaltung), geschalteter Dauerbetrieb (mit Allgemeinbeleuchtung geschaltet) | — | DIN V VDE V 0108-100 (sinngemäß EN 50172) | teilw. |
| LW10-R52 | Betrieb (S. 30) | Umschaltkriterium: Umschalten auf Sicherheitsstromquelle, wenn die Netzspannung länger als 0,5 s den Nennwert der Bemessungsspannung um 40 % unterschreitet; nach Netzwiederkehr automatische Abschaltung der Bereitschaftsleuchten nur, wenn Allgemeinbeleuchtung sofort volles Niveau erreicht — sonst Rückschaltverzögerung oder (verdunkelte Räume, z. B. Kinos) Handrückschaltung | > 0,5 s; −40 % Un | DIN V VDE V 0108-100 | teilw. |
| LW10-R53 | Betrieb (S. 30, Tabelle) | Batterie-Eckwerte: CPS (ohne Leistungsbegrenzung) — Spannung beliebig, vorzugsweise 216 V, Blei 2,0 V/Zelle, konstruktive Lebensdauer 10 Jahre bei 20 °C. LPS (mit Leistungsbegrenzung) — vorzugsweise 24/48 V, max. 1.500 W für 1 h bzw. max. 500 W für 3 h, Lebensdauer mind. 5 Jahre (Empfehlung 10). Einzelbatterie — Li-Ion 3,6 V / NiMH 1,2 V / NiCd 1,2 V pro Zelle, konstruktive Lebensdauer 4 Jahre | siehe Werte | DIN EN 50171 (CPS/LPS) | nein |
| LW10-R54 | Betrieb (S. 33) | Prüftaster oder Anschluss für Fernprüfeinrichtung (Netzausfall-Simulation) an jeder Einzelbatterieleuchte bzw. an der zentralen Stromquelle; Handprüftaster müssen selbsttätig zurückstellen | — | DIN EN 60598-2-22 (sinngemäß) | nein |
| LW10-R55 | Betrieb (S. 33) | Steuerungs- und BUS-Systeme der Sicherheitsbeleuchtung müssen unabhängig von den Systemen der Allgemeinbeleuchtung arbeiten | — | DIN V VDE V 0108-100 Pkt. 4.5 | ja |
| LW10-R56 | Prüfung (S. 34) | Prüfregime: täglich Sichtprüfung der zentralen Stromversorgung; mindestens wöchentlich Funktionsprüfung mit Zuschaltung der Sicherheitsstromquelle inkl. Einzelleuchtenüberwachung (batteriegestützte Systeme); monatlich Umschaltprüfung durch Netzausfall-Simulation mit Funktionsprüfung jeder Leuchte; jährlich Prüfung über die komplette Bemessungsbetriebsdauer mit allen Verbrauchern; Aggregate zusätzlich nach DIN 6280-13, Batterien nach DIN EN 50272-2 | täglich/wöchentlich/monatlich/jährlich | DIN V VDE V 0108-100; DIN EN 50172; DIN EN 62034; DIN EN 50272-2 | teilw. (Wochenrhythmus DE-Vornorm) |
| LW10-R57 | Prüfung (S. 34) | Prüfbuchpflicht: rückwirkende Kontrolle über mindestens 4 Jahre; handschriftlich oder per automatischer Prüfeinrichtung nach DIN EN 62034; Betreiber benennt verantwortliche Person; Prüfung/Wartung nur durch fachlich geeignetes Personal (DIN VDE 0105-100, DIN VDE 1000-10, TRBS 1203) | ≥ 4 Jahre | DIN EN 62034; DIN VDE 0105-100; TRBS 1203 | teilw. |

### G. Baurechtliche Gebäudetyp-Anforderungen (DE-Musterverordnungen — Referenz-Praxis)

| ID | Kapitel (Seite) | Regel/Faustformel | Werte | zitierte Norm | DE-only? |
|----|-----------------|-------------------|-------|---------------|----------|
| LW10-R58 | Versammlungsstätten (S. 35–36) | Anwendungsschwellen MVStättV: Versammlungsräume, die einzeln/gemeinsam ≥ 200 Personen fassen (Aulen, Foyers, Hörsäle, Kinos, Studios; nicht Unterrichtsräume); Versammlungsstätten im Freien mit Szenenflächen ab 1.000 Personen (Szenenfläche erst ab 20 m²); Sportstadien > 5.000 Besucher. Nicht erfasst: Gottesdiensträume, Museums-Ausstellungsräume, fliegende Bauten | 200 P / 1.000 P / 5.000 P | MVStättV 2014-07 | ja |
| LW10-R59 | Versammlungsstätten (S. 36) | Besucherzahl-Bemessung: Sitzplätze an Tischen 1 Besucher/m²; Sitzreihen und Stehplätze 2 Besucher/m²; Stehplätze auf Stufenreihen 2 Besucher/lfm Stufenreihe; Ausstellungsräume 1 Besucher/m² | 1/m² · 2/m² · 2/lfm · 1/m² | MVStättV 2014-07 | ja |
| LW10-R60 | Versammlungsstätten (S. 36–37) | Sicherheitsbeleuchtung erforderlich in: notwendigen Treppenräumen, Räumen zwischen Treppenraum und Ausgang ins Freie, notwendigen Fluren; Versammlungsräumen und allen Besucherräumen (Foyer, Garderobe, Toilette); Bühnen/Szenenflächen; Räumen für Mitwirkende/Beschäftigte > 20 m² (außer Büros); elektrischen Betriebsräumen und Haustechnikräumen, Scheinwerfer-/Bildwerferräumen; Freianlagen/Stadien bei Nutzung während Dunkelheit; für Sicherheitszeichen der Ausgänge/Fluchtwege; für Stufenbeleuchtung (außer Gänge bei auswechselbarer Bestuhlung) | > 20 m² Nebenräume | MVStättV 2014-07 | ja |
| LW10-R61 | Versammlungsstätten (S. 37) | Betriebsmäßig verdunkelte Versammlungsräume/Bühnen: Sicherheitsbeleuchtung in Bereitschaftsschaltung; darf sich nach Netzwiederkehr nicht selbsttätig ausschalten — Handrückschaltung an der Schalttafel und im Regieraum; Ausgänge, Gänge, Stufen müssen auch bei Verdunkelung unabhängig von der übrigen Sicherheitsbeleuchtung erkennbar sein | — | MVStättV; DIN V VDE V 0108-100 (früher DIN VDE 0108 zwingend) | ja |
| LW10-R62 | Sportstätten (S. 38–39) | Sicherheitsbeleuchtung für Sport-Teilnehmer (geordnetes Beenden der Veranstaltung), Niveau als Prozent der sportartspezifischen Beleuchtung: Schwimmen 5 %/≥30 s; Turnen (innen) 5 %/≥30 s; Reiten (innen+außen) 5 %/≥120 s; Eisschnelllauf 5 %/≥30 s; Bob/Rennschlitten 10 %/≥120 s; Skispringen (Ab-/Aufsprungzone) 10 %/≥30 s; Skiabfahrt 10 %/≥30 s; Radsport Bahn 10 %/≥60 s; muss sofort einsetzen | 5–10 % / 30–120 s | DIN EN 12193 | nein |
| LW10-R63 | Schwimmbäder (S. 39) | KOK-Richtlinien für Bäderbau (2013): ab 1,35 m Wassertiefe 15 lx Sicherheitsbeleuchtung auf der Wasseroberfläche; DGUV Regel 107-001 (2011-06): bei Unfallgefahr 1 % der Allgemeinbeleuchtung, mindestens 1 lx (Hallenbäder, Beckenumgänge, Dusch-/Umkleide-/Technikräume, Fluchtwege, Tribünen) | ≥ 1,35 m → 15 lx; 1 %, min. 1 lx | KOK-Richtlinien 2013; DGUV Regel 107-001 | ja |
| LW10-R64 | Gaststätten (S. 40) | Gaststätten/Restaurants sind Versammlungsstätten (MVStättV): Anforderungen wie LW10-R60 ab > 200 Besucherplätzen; Bemessung: Sitzplätze 1 Besucher/m² Gastraumfläche ohne Tresen (d. h. ab 200 m²), Stehplätze (z. B. Diskotheken) 2 Besucher/m² (d. h. ab 100 m²) | 200 P; ab 200/100 m² | MVStättV 2014-07 | ja |
| LW10-R65 | Beherbergungsstätten (S. 41) | Pflicht ab > 12 Gästebetten (MBeVO; nicht für Hochhäuser): Sicherheitsbeleuchtung in notwendigen Fluren und Treppenräumen, Räumen zwischen Treppenraum und Ausgang ins Freie, für Ausgangs-Sicherheitszeichen und Stufen in notwendigen Fluren | > 12 Betten | MBeVO 2014-05 | ja |
| LW10-R66 | Beherbergungsstätten (S. 41) | Bei nur 3 h Bemessungsbetriebsdauer der Stromquelle: geschaltete Dauerschaltung mit Leuchttastern und Zeitlicht (selbsttätige Abschaltung nach eingestellter Zeit) einplanen; sonst Kapazität für 8 h auslegen | 3 h (mit Schaltung) / 8 h | DIN V VDE V 0108-100 | ja |
| LW10-R67 | Verkaufsstätten (S. 42–43) | Pflicht ab > 2.000 m² Verkaufsräume + Ladenstraßen (MVkVO) — **Schwelle gilt laut Heft „gleichermaßen auch in Österreich"**. Sicherheitsbeleuchtung bis zu den öffentlichen Verkehrsflächen: Verkaufs-/Besucherräume > 50 m²; notwendige Treppenräume/Flure und Räume zum Ausgang; Beschäftigtenräume > 20 m² (außer Büros); Toilettenräume > 50 m² (Bayern/Brandenburg: jede Größe); elektrische Betriebs-/Haustechnikräume; Ausgangs-Hinweisschilder und Stufenbeleuchtung | > 2.000 m²; Räume > 50/20 m² | MVkVO 2014-07 | teilw. (2.000-m²-Schwelle auch AT) |
| LW10-R68 | Schulen (S. 43) | MSchulbauR (2009-04, allgemein-/berufsbildende Schulen, nicht Hochschulen/VHS/Musik-/Fahrschulen): Sicherheitsbeleuchtung in Hallen, durch die Fluchtwege führen, in notwendigen Fluren und Treppenräumen sowie in fensterlosen Aufenthaltsräumen | — | MSchulbauR 2009-04 | ja |
| LW10-R69 | Krankenhäuser (S. 43) | DIN VDE 0100-710 (Krankenhäuser, Kliniken, Sanatorien, Ärztehäuser, Pflegeheime …): Sicherheitsbeleuchtung für Fluchtwege; Räume mit Schalt-/Steuergeräten für Notstromaggregate und Hauptverteiler; Bereiche lebenswichtiger Dienste; Räume Gruppe 1 (Untersuchung/Behandlung) und Gruppe 2 (OP, Intensiv): Teil der Leuchten an 2 Stromquellen/2 Stromkreisen, einer davon an der Sicherheitsstromversorgung; Gruppe 2: mindestens 50 % der Beleuchtung aus der Sicherheitsbeleuchtung; Standorte von Brandmeldezentrale und Überwachungseinrichtungen | Gruppe 2: ≥ 50 % | DIN VDE 0100-710 (2012-10) | teilw. (HD-60364-basiert, AT-Pendant prüfen) |
| LW10-R70 | Hochhäuser (S. 45) | MBO 2012-09: Hochhaus = Gebäude > 22 m (Fußbodenoberkante oberstes Aufenthaltsgeschoss); Sicherheitsbeleuchtung für innenliegende Treppenräume bereits ab 13 m Gebäudehöhe (§ 35 (7)); MHHR (2008-04): zusätzlich Vorräume von Aufzügen; Wohnhochhäuser: 3-h-Regel mit geschalteter Dauerschaltung/Leuchttaster/Zeitlicht, sonst 8 h (wie LW10-R66) | > 22 m; ab 13 m; 3 h/8 h | MBO 2012-09; MHHR 2008-04; DIN V VDE V 0108-100 | ja |
| LW10-R71 | Großgaragen (S. 45) | MGarVO 2008-05: Sicherheitsbeleuchtung für geschlossene Großgaragen > 1.000 m² Nutzfläche (Einstellplätze + Verkehrsflächen), ausgenommen eingeschossige Großgaragen mit festem Benutzerkreis; Fluchtwege umfassen Fahrgassen, Gehwege neben Zu-/Abfahrten, Treppen und Wege zu den Ausgängen | > 1.000 m² | MGarVO 2008-05 | ja |

### H. System-Tabelle DIN V VDE V 0108-100:2010-08 (S. 46) — DE-only, Referenz-Praxis

Beleuchtungsstärke jeweils nach DIN EN 1838 (Fußnote 2), außer Bühnen. Alle Zeilen: CPS, LPS,
Einzelbatterie und Aggregate (0 s / ≤ 0,5 s / ≤ 15 s Unterbrechung) zulässig, sofern nicht anders
vermerkt; „besonders gesichertes Netz" nur wo angegeben.

| ID | Gebäudetyp (S. 46) | Umschaltzeit max. | Bemessungsbetriebsdauer | Besonderheiten |
|----|--------------------|-------------------|--------------------------|----------------|
| LW10-R72a | Versammlungsstätten (außer fliegende Bauten), Theater, Kinos | 1 s | 3 h | Dauerbetrieb-RZ Pflicht; kein besonders gesichertes Netz |
| LW10-R72b | Fliegende Bauten (Versammlungsstätten) | 1 s | 3 h | wie oben |
| LW10-R72c | Ausstellungshallen | 1 s | 3 h | wie oben |
| LW10-R72d | Verkaufsstätten | 1 s | 3 h | wie oben |
| LW10-R72e | Restaurants | 1 s | 3 h | wie oben |
| LW10-R72f | Beherbergungsstätten, Heime | 1 s (je nach Panikrisiko 1–15 s + Gefährdungsbeurteilung) | 8 h; 3 h genügen mit Schaltung 4.4.8 | besonders gesichertes Netz zulässig |
| LW10-R72g | Schulen | 1 s (1–15 s je Panikrisiko) | 3 h | besonders gesichertes Netz zulässig |
| LW10-R72h | Parkhäuser, Tiefgaragen | 15 s | 1 h | besonders gesichertes Netz zulässig |
| LW10-R72i | Flughäfen, Bahnhöfe | 1 s | 3 h (oberirdische Bahnhofsbereiche je nach Evakuierungskonzept 1 h zulässig) | — |
| LW10-R72j | Hochhäuser | 1 s (1–15 s je Panikrisiko) | 8 h; Wohnhochhäuser 3 h mit Schaltung 4.4.8 | besonders gesichertes Netz zulässig |
| LW10-R72k | Flucht-/Rettungswege in Arbeitsstätten | 15 s | 1 h | Dauerbetrieb-RZ nicht gefordert (Fußnote 7); besonders gesichertes Netz und Zwei-Netz-Einspeisung zulässig |
| LW10-R72l | Arbeitsplätze mit besonderer Gefährdung | 0,5 s | Zeitraum der bestehenden Gefährdung | Zwei-Netz-Einspeisung zulässig |
| LW10-R72m | Bühnen | 1 s | 3 h | **Beleuchtungsstärke 3 lx** (einzige explizite lx-Angabe der Tabelle) |

Schaltung 4.4.8 (Anmerkung S. 46): Sicherheitsbeleuchtung im Dauerbetrieb mit der
Allgemeinbeleuchtung geschaltet (Wohnhochhäuser, Beherbergungsstätten, Heime) bei nur 3 h
Betriebsdauer; Leuchttaster so anbringen, dass von jedem Standort mindestens einer auch bei Ausfall
der Allgemeinbeleuchtung erkennbar ist; selbsttätige Abschaltung nach einstellbarer Zeit im
Batteriebetrieb.

## Zitierte Norm-Werte (Quelle-der-Quelle)

- **DIN EN 1838 (2013-10)** — S. 10/11 (Platzierungsstellen, ≥ 2 m Montagehöhe, „nahe" = ≤ 2 m,
  5 lx vertikal an Erste-Hilfe-/Brandmeldestellen), S. 12–15 (Fluchtweg 1 lx Mittelachse/2 cm
  Messhöhe, 40:1, Ra ≥ 40, Blendungstabelle 500–5.000 cd, 1 h), S. 18 (besondere Gefährdung 15 lx,
  10:1, 0,5 s, Blendung 1.000–10.000 cd), S. 23 (grün ≥ 2 cd/m², mittl. RZ-Leuchtdichte ≥ 5 cd/m²,
  Gleichmäßigkeit ≥ 0,1, Kontrast 5:1–15:1, z = 200/100), S. 24 (weiß ≥ 10 cd/m²). → EN-identisch,
  AT-gültig; Details siehe EN-1838-Extrakt (82 Regeln, nicht dupliziert).
- **DIN 4844-1 (2012-06)** — S. 15, 22–23: Normalbetriebsanforderungen an RZ (weiß ≥ 500 cd/m²,
  mittl. Leuchtdichte ≥ 200 cd/m², Gleichmäßigkeit ≥ 0,2, Schildbeleuchtung ≥ 50 lx, vorzugsweise
  ≥ 80 lx, Dauerbetrieb ja). **DE-only** (deutsches Zeichenrecht).
- **DIN EN ISO 7010 (2012-10) / DIN ISO 3864-1/-3, ISO 3864-4** — S. 22: E001/E002, Pfeil Typ D,
  Farbfestlegungen. EN/ISO-identisch.
- **DIN V VDE V 0108-100 (2010-08, Vornorm)** — S. 33, 41, 45, 46: Systemanforderungen,
  Gebäudetyp-Tabelle (Umschaltzeiten 0,5/1/15 s; Betriebsdauern 1/3/8 h), Schaltung 4.4.8,
  BUS-Unabhängigkeit (Pkt. 4.5). **DE-only** (Anwendung vom UK 221.3 der DKE nur „empfohlen");
  AT-Pendant: OVE E 8101 / ÖVE-Richtlinien maßgeblich.
- **DIN EN 50172 (2005-01)** — S. 49 (Normenliste; = VDE 0108-100): Sicherheitsbeleuchtungsanlagen.
  EN-identisch, aber im Heft inhaltlich meist über die DE-Vornorm referenziert.
- **DIN EN 60598-2-22 (2015-06)** — S. 26, 30: Leuchtenanforderungen, Typenschild-Codierung,
  Einzelbatterieleuchten. EN/IEC-identisch.
- **DIN EN 62034 (2013-02)** — S. 26, 34: automatische Prüfsysteme, elektronisches Prüfbuch.
  EN/IEC-identisch.
- **DIN EN 50171 (2001-11)** — S. 30: CPS/LPS-Anforderungen (LPS max. 1.500 W/1 h bzw. 500 W/3 h).
  EN-identisch.
- **DIN EN 50272-2 (2001-12)** — S. 34: jährliche Batterieprüfung. EN-identisch.
- **DIN EN 12193** — S. 38–39: Sportstätten-Sicherheitsbeleuchtung, Prozent-/Zeitwerte je Sportart.
  EN-identisch.
- **DIN VDE 0100-710 (2012-10)** — S. 43: medizinisch genutzte Bereiche, Gruppe-1/2-Räume, ≥ 50 %
  Regel. HD-60364-7-710-basiert; für AT das nationale Pendant heranziehen.
- **ASR A2.3 (2007-08, geänd. 2014), ASR A3.4/3 (2009-05, geänd. 2014), ASR A1.3 (2013-02),
  ArbStättV 2004, ArbSchG § 5/§ 6** — S. 12, 14, 16–19, 24, 30: Messhöhe ≤ 20 cm, ±0,5-m-50 %-Regel,
  10 %-Empfehlung, Baustellen/Keller/Tunnel 15 lx, Leitsystem-Pflicht > 3,6 m, Quellen-Exklusivität
  (Pkt. 6.6). **Alle DE-only** (Arbeitsschutzrecht DE; Anm.: ASR **A3.4/3**, nicht „A3.4/7").
- **Muster-Bauverordnungen** MVStättV 2014-07, MBeVO 2014-05, MVkVO 2014-07, MGarVO 2008-05,
  MBO 2012-09, MHHR 2008-04, MSchulbauR 2009-04, MLAR 2005-11, MIndBauRL 2014-02,
  M-EltBauVO 2009-01 — S. 35–46, 49. **Alle DE-only**; Ausnahme-Aussage: 2.000-m²-Schwelle
  Verkaufsstätten gilt auch in AT (S. 42).
- **ISO 16069:2003 / DIN SPEC 4844-4 / ZVEI-Positionspapier „Kennzeichnung der Fluchtrichtung"
  (2016)** — S. 47: Pfeilrichtungssystematik (in DE nicht verbindlich).
- **KOK-Richtlinien für Bäderbau (2013), DGUV Regel 107-001 (2011-06)** — S. 39: 15 lx ab 1,35 m
  Wassertiefe; 1 % / min. 1 lx. DE-only.
- **ISO 30061 / CIE S 020 (2007-11)** — S. 49: internationale Notbeleuchtungsnorm (nur Normenliste).

## Detail-Digest

**Begriffssystematik (S. 3, 8–9, 48):** Notbeleuchtung = Oberbegriff, gegliedert in
Sicherheitsbeleuchtung und Ersatzbeleuchtung. Sicherheitsbeleuchtung gliedert sich in (1) Fluchtweg-
Sicherheitsbeleuchtung inkl. Kennzeichnung, (2) Sicherheitsbeleuchtung für Arbeitsbereiche mit
besonderer Gefährdung, (3) Antipanikbeleuchtung. Ersatzbeleuchtung = Fortsetzung einer Tätigkeit
ohne Personengefährdung; sie ist kein Sicherheitsthema. Trigger der Pflicht (DE): dokumentierte
Gefährdungsbeurteilung nach ArbSchG.

**Platzierung (S. 10–11):** Abb. 7 listet die hervorzuhebenden Stellen (LW10-R1…R14) — das ist
1:1 das Trigger-Set, das Leonis' Platzierer je RaumModell-Feature abarbeiten kann. Wichtig fürs
Datenmodell: „nahe" ist normativ als max. 2 m Horizontalabstand definiert; Erste-Hilfe- und
Brandmeldepunkte verlangen 5 lx **vertikal** (nicht horizontal). Barrierefreiheit ist eigener
Trigger-Block (Schutzbereiche, Rufanlagen, Behindertentoiletten mit Antipanik).

**Fluchtweg-Lichttechnik (S. 12–15):** 2-m-Streifen-Modell; 1 lx Mittelachse; 40:1; Ra ≥ 40;
Blendungstabelle nach Montagehöhe (Zone 60°–90°). Die Tabelle S. 15 fasst alles für Rettungswege
zusammen (Betriebsdauer 1 h). Für die Engine ist die Aussage relevant, dass die 40:1-Prüfung für
den ungünstigsten Fall (Ende der Betriebsdauer, Punkt zwischen zwei Leuchten) gilt →
Leuchtenabstands-Constraint.

**Arbeitsstätten (S. 16–19):** 15-lx-Regel für besondere Gefährdung mit 0,5-s-Anlauf und 10:1;
Katalogliste der Gefährdungs-Arbeitsplätze (Labore, Leitstände, Gießgruben, Baustellen …);
ASR-Zusatzpraxis (10 %-Empfehlung, ±0,5-m-Regel, Messhöhe ≤ 20 cm) ist DE-spezifisch.
Verrauchungsrisiko + Wegbreite > 3,6 m → zusätzliches bodennahes Leitsystem (≤ 40 cm).

**Antipanik (S. 20):** DE hat keine baurechtliche Antipanik-Basis; Praxis plant 1 lx auf freier
Bodenfläche und 3 h. Anwendungstrigger: undefinierte Fluchtwege in Hallen, Konferenzräume > 60 m²
ohne ausgewiesene Fluchtwege, Aufzugskabinen. Für die Engine: EN-1838-Default (0,5 lx) bleibt der
Norm-Default; die 1-lx/3-h-Praxis ist ein Referenz-Praxis-Kandidat, wenn die LB nichts sagt und
konservativ geplant werden soll.

**Rettungszeichen (S. 22–25):** Zwei Betriebszustände mit getrennten Anforderungsprofilen —
Normalbetrieb (DIN 4844-1, hell: weiß ≥ 500 cd/m²) vs. Notbetrieb (EN 1838, dunkel: gesamt
≥ 5 cd/m², grün ≥ 2, weiß ≥ 10). Hinterleuchtet schlägt beleuchtet (z = 200 vs. 100; rauchfester;
konstant hell). Nachleuchtende Schilder sind allein unzulässig (Farbverfälschung, Erkennungsweite
kollabiert auf ~5 m nach 10 min). Beleuchtetes Schild erzwingt eine dedizierte Sicherheitsleuchte
≤ 2 m in Dauerschaltung (~30 lx Notbetrieb, ≥ 80 lx Netz) — d. h. „beleuchtetes Schild" kostet in
der Stückzahllogik immer +1 Leuchte. Montageempfehlung ≤ 20° über horizontaler Blickrichtung.
Pfeilsystematik ungeklärt (ISO 16069 „hoch" vs. ZVEI-Praxis „runter = geradeaus/durch die Tür").

**Leuchten/Systeme (S. 26–33):** Typenschild-Code (X/Z · 0–6 · A–G · Minuten) als Katalog-Metadaten
nützlich. Variante A (dedizierte Sicherheitsleuchten) erlaubt fast doppelte Montageabstände bei
~1/20 der Anschlussleistung gegenüber Variante B (Allgemeinleuchten im Notbetrieb) — Beispielwerte
15,6 m/6 W vs. 8 m/115 W bei 3 m Flurhöhe. Umschaltkriterium −40 % Un für > 0,5 s;
Rückschalt-Sonderregeln für verdunkelte Räume (Kino/Bühne: Handrückschaltung). Sicherheits-BUS
strikt getrennt von der Allgemeinbeleuchtungs-Steuerung.

**Prüfung (S. 33–34):** täglich (Sicht, Zentrale) / wöchentlich (Funktion + Einzelleuchte) /
monatlich (Netzausfall-Simulation) / jährlich (volle Betriebsdauer); Prüfbuch ≥ 4 Jahre;
Automatisierung nach EN 62034. Für die Engine allenfalls als Hinweistext im Planoutput relevant.

**Baurecht-Kapitel (S. 35–46):** Gebäudetypen-Schwellen und Raumlisten (LW10-R58…R72) — als
DE-Referenz-Praxis für die Frage „welche Räume bekommen überhaupt Sicherheitsbeleuchtung",
solange die LB/AT-Vorschrift nichts Spezifischeres sagt. Die S.-46-Tabelle liefert das kompletteste
Umschaltzeit/Betriebsdauer-Raster je Gebäudetyp (0,5/1/15 s; 1/3/8 h; Bühnen 3 lx).

## Offene Punkte / Extraktionslücken

1. **15-s/100-%-Aussage (S. 14, LW10-R20):** Das Heft verlangt pauschal 100 % Lichtleistung binnen
   15 s. EN 1838 selbst staffelt für Fluchtwege 50 % in 5 s / 100 % in 60 s (siehe EN-1838-Extrakt);
   die 15 s stammen aus dem DE-Umschaltzeitraster (V 0108-100). Für die Engine: AT-Werte aus
   OVE E 8101/EN 1838 maßgeblich, Heftwert nur als konservative Praxis behandeln.
2. **Antipanik 1 lx (S. 20)** widerspricht dem EN-1838-Default 0,5 lx — bewusst als DE-Praxis
   markiert (LW10-R34); Entscheid, ob die Engine die konservative 1-lx-Praxis als
   Referenz-Praxis-Layer übernimmt, steht aus.
3. **Abbildungsgebundene Inhalte** (Abb. 9–14, 16, 32–48, 65/66) sind im Textextrakt nur als
   Bildunterschriften enthalten; Grafikdetails (z. B. exakte Pfeil-Kombinatorik-Matrix S. 22/47,
   Blockschaltbilder S. 32–34) konnten nicht vollständig extrahiert werden.
4. **PDF-Encoding-Artefakte:** Vergleichsoperatoren erschienen als Glyph-Codes (/L50871 = „≥",
   /L50872 = „≤" u. ä.); die Werte der Blendungs- und RZ-Tabellen wurden aus dem Kontext
   rekonstruiert (Höhenklassen-Grenzen ≤/< wie in EN 1838 üblich). Bei Zweifel gegen
   EN-1838-Original prüfen.
5. **Stand 2016:** DIN V VDE V 0108-100 (2010) und MVStättV (2014) sind inzwischen ggf.
   fortgeschrieben (DIN VDE V 0108-100-1:2018 etc.); Werte hier = Stand der Publikation.
6. Erwähnte, aber nicht enthaltene Vertiefungen: licht.forum 56 (Arbeitsstätten), licht.forum 57
   (optische Sicherheitsleitsysteme), ZVEI-Positionspapiere „Automatische Testsysteme" und
   „Kennzeichnung der Fluchtrichtung" (2016), Beiblatt zu DIN EN 1838 (2016 in Vorbereitung).
