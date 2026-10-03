# ANALYSE — Projekt 2 — Tomaschek-Schule

Generiert aus `evidenz/Tomaschek/seitenprotokoll.jsonl` (242 Seiten-Records) — nicht von Hand editieren.

**Bilanz:** 149 bestätigt · 57 neu · 0 Widerspruch · 36 ohne Regelgehalt (Deckblatt/Legende/…)

## S.  1 — Notbeleuchtungen zeichnen - Tomaschek-Schule
**Bereich:** Deckblatt
**Bild:** Deckblatt mit grauem Übersichtsgrundriss des Winkel-Baukörpers (Erweiterungstrakt + schräger Südflügel), ohne Symbole. Kennzahlen: 56 Fälle, 146 Positionen (81 RZ + 65 SL), 146 ersetzt, 14 RZ-Beispiele in 7 Legenden, 8 RIVO-Muster + 1 Versorgungsobjekt erhalten. Oranger Hinweis: Erklärungsunterlage, keine freigegebene Ausführungsplanung.
> „Runde Leuchten und quadratische Zeichen mit Mittelkreis erhalten RIVO_Aufheller_Variante; rechteckige Leuchten RIVO_Antipanik. Dies ist die vorgegebene grafische Zuordnung, kein Lichtnachweis.“
**Linien:** nur grauer Übersichtsgrundriss SG/EG/OG-Gebäude, keine Wege/Sichtlinien
**DXF-Abgleich:**  · Handles — · Deckblatt, kein Planausschnitt
**Bewertung:** kein_regelgehalt

## S.  2 — Inhaltsverzeichnis
**Bereich:** Inhaltsverzeichnis
**Bild:** Reines Inhaltsverzeichnis: Einleitungskapitel S.1-10, dann Fälle F-SG-01 bis F-SG-18 (Sockelgeschoss) und F-EG-01 bis F-EG-14 (Erdgeschoss) mit Seitenzahlen. Keine Planinhalte.
**Linien:** keine
**DXF-Abgleich:**  · Handles — · Inhaltsverzeichnis, kein Planausschnitt
**Bewertung:** kein_regelgehalt

## S.  3 — Inhaltsverzeichnis - Fortsetzung
**Bereich:** Inhaltsverzeichnis
**Bild:** Fortsetzung des Inhaltsverzeichnisses: F-EG-15 bis F-EG-17, F-OG-01 bis F-OG-17, geschossübergreifende Fälle F-X-01 bis F-X-04 (TH 4, TH 3, Bestandsflügel/TH 2, Dachgeschoss), danach Fallverzeichnis, Leuchtenregister, Symbol- und Transformationsprüfung, Prüfstand.
**Linien:** keine
**DXF-Abgleich:**  · Handles — · Inhaltsverzeichnis, kein Planausschnitt
**Bewertung:** kein_regelgehalt

## S.  4 — So lesen Sie einen Fall
**Bereich:** Leseanleitung
**Bild:** Textseite: Gliederungsschema A-J je Fall (A Ort, B Herkunft der Person, C Weg-Folge, D Front/Rückseite/seitliche Sicht, E Position+Funktion, F Symboltausch+Drehung mit Objekt-ID, G Alternative, H Normbezug mit Ausgabe, I fehlender Nachweis, J übertragbare Zeichenregel). Gleiches A-J-Raster wie die Mollgasse-Fallstruktur, um D/F/J erweitert formalisiert.
> „D Front, Rückseite und seitliche Sicht - Welche Zeichenfläche gesehen wird - frontal, rückseitig oder seitlich.“
> „J Übertragbare Zeichenregel - Die übertragbare Regel für die nächste Zeichensituation.“
**Linien:** keine
**DXF-Abgleich:**  · Handles — · Leseanleitung, kein Planausschnitt
**Bewertung:** kein_regelgehalt

## S.  5 — Grafische Sprache und Beleggrenzen
**Bereich:** Legende der Annotationssprache
**Bild:** Textseite: grün gestrichelte Wege mit Bewegungsperson = gekennzeichnete Interpretation (keine freigegebene Fluchtwegplanung), türkis gestrichelte Sichtlinien = angenommene Blickrichtung, orange Rahmen = diskutierte Tür/Bauteil, orange Objektmarken = nicht ersetzte Varianten. Frontnormale einseitiger RIVO-Zeichen bei 0° = lokal -Y, bei Rotation θ = (sin θ, -cos θ); beidseitige Zeichen haben zwei Fronten, Ankunft entlang der Tafelkante ist NICHT frontal. Keine erfundene Geometrie über Treppenauge/Wände.
> „Die einseitigen RIVO-Zeichen haben bei 0° ihre Frontnormalen in lokaler Richtung -Y. Bei Rotation θ wird daraus (sin θ, -cos θ).“
> „Eine Ankunft entlang der Tafelkante ist trotz "beidseitig" nicht frontal.“
> „Treppenauge, Geländer, Wände und geschlossene Raumtrennungen werden nicht durch eine angenommene Linie überbrückt.“
**Linien:** grün gestrichelt=interpretierter Weg, türkis gestrichelt=Sichtlinie, orange=Hervorhebung/nicht ersetzte Variante
**DXF-Abgleich:**  · Handles — · Konventionsseite; Frontnormalen-Definition deckt sich mit orientation.py-Rahmen (Front≠Pfeil), beidseitig ohne Rundumsicht = NB-R16-Aussage
**Bewertung:** bestaetigt:NB-R07

## S.  6 — Aufheller und Antipanik: warum hier?
**Bereich:** Symbol-Zuordnungslogik
**Bild:** Textseite: 51 runde/quadratische Bestandszeichen mit Mittelkreis (Typ B, C, D, E, F, G) werden mit RIVO_Aufheller_Variante, 14 rechteckige (Typ L, N, O, P, Q) mit RIVO_Antipanik dargestellt; die 81 RZ gehören zu keiner der Gruppen. Zuordnung = vom Auftraggeber festgelegte CAD-Sprache, keine Aussage über reale Optik; EN 1838 4.1.2 a-g und 4.2.1-4.2.2 (Aufheller-Aufgabe) bzw. 4.3.1-4.3.2 und 4.3.8 (Antipanik-Aufgabe) nur als Aufgaben-Referenz. Keine zusätzlichen Leuchten oder neuen Fluchtwege geplant.
> „Die Zuordnung beschreibt die vom Auftraggeber festgelegte CAD-Sprache und ist keine Aussage über die reale Optik.“
> „Deshalb bestimmt die CAD-Form nur das Ersatzsymbol; die konkrete Aufgabe unterscheidet sich je nach Gang, Tür, Stiege, Raum oder Außenanschluss.“
**Leuchten im Bild:** Typ B/C/D/E/F/G aufheller, Typ L/N/O/P/Q antipanik
**Linien:** keine
**DXF-Abgleich:**  · Handles — · Zuordnung gilt für alle 3 Erklärungs-DXFs; bestätigt Basis-Grundsatz Rolle≠Produkt, ergänzt formbasierte Bestandskonvention
**Bewertung:** neu → Bestandsplan-Formkonvention (LB/AG-Ebene): runde/quadratische Bestandsleuchten mit Mittelkreis → aufheller-Symbol, rechteckige → antipanik-Symbol; reine AG-CAD-Sprache ohne Lichtnachweis, RZ separat — übersteuert keine Platzierungsregel

## S.  7 — Eingaben, Repository und Bearbeitungsgrenze
**Bereich:** Quellenlage
**Bild:** Textseite: Eingaben = 3 Elektromontagepläne (Sockelgeschoss, Erdgeschoss, 1.Obergeschoss als DXF), RIVO_NL_Symbole.dxf, TOMA Flucht- und Rettungspläne.pdf (10 S., Planstand 27.07.2026), Mollgasse-Vorlage (95 S.). Zielobjekte überwiegend im Erweiterungstrakt; südlicher Bestandsflügel ohne vollständige erkannte Leuchtenfolge. Orange: Fluchtplan enthält ein Dachgeschoss ohne Elektromontage-DXF — aus fehlender Montagegrundlage wird KEIN fehlender Leuchtenbedarf abgeleitet.
> „Widersprüche und fehlende Freigaben werden nicht durch eine neue Planung ersetzt.“
> „aus der fehlenden Montagegrundlage wird kein fehlender Leuchtenbedarf abgeleitet.“
**Linien:** keine
**DXF-Abgleich:**  · Handles — · benennt die drei Quell-DXFs der Erklärungs-Ausgaben SG/EG/OG; Fluchtplan nur als Richtungs-Referenz = NB-R22-Quellentrennung
**Bewertung:** bestaetigt:NB-R22

## S.  8 — RIVO-Bibliothek: tatsächliche Planzeichen
**Bereich:** Symbol-Legende
**Bild:** Legendenseite mit 8 gerenderten Original-Blockgrafiken: RIVO_ARR_down (Pfeil lokal -Y, Front -Y), RIVO_ARR_left (Pfeil -X, Front -Y), RIVO_ARR_right (Pfeil +X, Front -Y), RIVO_Antipanik (weißes Rechteck), RIVO_Aufheller (weißer Kreis, hier nicht als Zielblock benutzt), RIVO_ARR_bothsided (zwei Fronten ±Y, beide Pfeile lokal -X, keine Rundumsicht), RIVO_Gruppenbatterie_Verteiler (grün/weiß diagonal geteiltes Rechteck, keine Leuchte), RIVO_Aufheller_Variante (Kreis mit gefüllten Kreissegmenten, verbindlicher Aufhellerblock, 51 Positionen).
> „RIVO_ARR_bothsided - Zwei Fronten ±Y; beide Pfeile lokal -X. Keine Rundumsicht.“
> „RIVO_Aufheller_Variante - Verbindlicher RIVO-Aufhellerblock ... Die Form beweist keine Lichtverteilung.“
**Leuchten im Bild:** RIVO_ARR_down down, RIVO_ARR_left left, RIVO_ARR_right right, RIVO_ARR_bothsided beidseitig, RIVO_Antipanik antipanik, RIVO_Aufheller aufheller, RIVO_Aufheller_Variante aufheller, RIVO_Gruppenbatterie_Verteiler anlage
**Linien:** keine
**DXF-Abgleich:**  · Handles — · Blocknamen decken sich mit RIVO_NL_Symbole.dxf der Engine-Library; lokale Achsdefinitionen konsistent zu orientation.py
**Bewertung:** kein_regelgehalt

## S.  9 — Normausgaben bewusst auseinanderhalten
**Bereich:** Normenregister/Ausgabenstände
**Bild:** Textseite ohne Plan: gelesene Ausgabe ÖNORM EN 1838:2019-11-15 (enthält EN 1838:2013-07), Katalog führt bereits 2025-03-01 (Volltext fehlt, keine Behauptungen daraus). OVE E 8101:2019 und :2025 getrennt gelesen; AC1:2020-05-01 ändert bereits Tabelle 56.A.1.AT, Dauerbetriebs-Zeichen, Fußnote c und BMA-Aktivierung — nicht als 2025-Neuerungen darstellen. 3.200-m²-Schwelle: OIB 2:2023 nennt Netto-Grundfläche, historischer Schulteil E8002-9:2002 Gesamtbruttofläche — nicht gleichsetzen. R12-2 nur als Korrigendum vorhanden; EN 50172/ISO 7010-Volltexte fehlen.
> „Diese Inhalte dürfen daher nicht als erst 2025 eingeführte Anforderungen dargestellt werden.“
> „Die 3.200-m²-Schwelle ist keine aus den vorliegenden Ausschnitten bestätigte Einstufung.“
> „"gesichtet" wird nicht als "vollständig gelesen" ausgegeben.“
**Linien:** keine
**DXF-Abgleich:**  · Handles — · kein Planbezug; Normquellen-Governance für alle Schul-Fälle
**Bewertung:** neu → Normausgaben-Disziplin (Prozessregel, Enis-Naht): norm_quelle IMMER mit exakter Ausgabe+Berichtigung führen; AC1:2020-Inhalte nicht als 2025 ausgeben; Flächenbegriffe Netto-Grundfläche (OIB 2:2023) vs Gesamtbruttofläche (E8002-9) nie mischen; fehlender Volltext = keine Klauselbehauptung

## S. 10 — Anforderungen als Prüfaufträge (A01-A05)
**Bereich:** Prüfauftrags-Katalog EN 1838
**Bild:** Textseite: A01 (EN 1838 4.1.1/5.1-5.5: zusätzliche RZ wenn Notausgang nicht direkt sichtbar), A02 (4.1.2 a-g: Ausgangstüren, Stufen, Richtungsänderungen, Kreuzungen, Außenweg gezielt beleuchten; SL muss an Richtungsänderungen beide Richtungen ausleuchten — keine pauschale Forderung nach einem RZ-Block; 'nahe' ≈ max 2 m horizontal), A03 (4.2.1-4.2.2: Mittellinie ≥1 lx, halbe Breite ≥0,5 lx, Ud ≥1:40), A04 (4.3.1-4.3.2: Antipanik ≥0,5 lx Kernbereich ohne 0,5-m-Randstreifen), A05 (4.3.8: Toiletten für Menschen mit Behinderung brauchen Antipanik — KEINE 8-m²-Grenze, gilt nicht automatisch für jeden barrierefreien Raum). Jede Anforderung mit Bedingung + benötigtem Nachweis.
> „Ist der Notausgang nicht direkt sichtbar, müssen ein oder mehrere zusätzliche beleuchtete oder hinterleuchtete Rettungszeichen das Erreichen des Ausgangs erleichtern.“
> „Bei Richtungsänderungen und Kreuzungen muss die Sicherheitsleuchte beide Richtungen ausleuchten; dies ist keine pauschale Forderung nach einem bestimmten RZ-Block.“
> „Diese Klausel nennt keine 8-m²-Grenze und gilt nicht automatisch für jeden barrierefreien Raum.“
**Linien:** keine
**DXF-Abgleich:**  · Handles — · kein Planbezug; A01 deckt NB-R08/NB-R12 (Sichtkette/Zusatz-RZ), A03/A04 decken Engine-Lux-Regeln (1 lx Mittellinie, 0,5 lx Antipanik)
**Bewertung:** bestaetigt:NB-R08

## S. 11 — Anforderungen als Prüfaufträge (A06-A10)
**Bereich:** Prüfauftrags-Katalog OVE/EN Fortsetzung
**Bild:** Textseite: A06 (OVE 718.560.9.001.AT: bei ERHÖHTEN Anforderungen zusätzlich Sanitärbereiche ab 8 m², barrierefreie WC-Anlagen und Elektro-/Sicherheitszentralen prüfen; 60-m²-Regel nur verkehrstechnische Einrichtungen, keine pauschale Schulregel), A07 (4.1.2 h-i: ≥5 lx vertikal an Erste-Hilfe-/Brandbekämpfungs-/Meldeeinrichtungen), A08 (4.4: besondere Gefährdung ≥10 % Wartungswert, ≥15 lx, Uo ≥0,1, ≤0,5 s; kein Automatismus aus Raumname Werken/Küche), A09 (5.5: Erkennungsweite l=z×h, z=100 extern/200 hinterleuchtet, reale Zeichenhöhe statt CAD-Symbolgröße; 20°-Aussage nur Sollte), A10 (≥1 h, 50 % in 5 s, 100 % in 60 s; keine Festlegung auf 1 h für die Schule).
> „Ziffer 3 ist ausdrücklich auf verkehrstechnische Einrichtungen begrenzt und begründet keine pauschale 60-m²-Schwelle für Schulräume.“
> „Erkennungsweite l = z × h; z=100 für extern beleuchtete, z=200 für hinterleuchtete Zeichen ... keine Umrechnung aus der grafischen Größe eines CAD-Symbols.“
> „Keine Festlegung auf 1 h für die Schule.“
**Linien:** keine
**DXF-Abgleich:**  · Handles — · kein Planbezug; l=z×h deckt sich mit normwissen-Basis; A06/A08/A10 sind schul-spezifische Bedingungsschärfungen ohne Widerspruch
**Bewertung:** neu → Schul-Prüfbedingungen (Validierungs-Layer, nachrangig): bei erhöhten Anforderungen Sanitär ≥8 m² + barrierefreie WCs + E-/Sicherheitszentralen als Antipanik-/SL-Kandidaten prüfen; 5 lx vertikal an Erste-Hilfe/Melde-/Brandbekämpfungseinrichtung als eigener Nachweis; KEINE pauschale 60-m²-Schulregel; Werk-/Küchenbereich nur mit Gefährdungsbeurteilung, nicht per Raumname

## S. 12 — Anforderungen als Prüfaufträge (A11-A15)
**Bereich:** Prüfauftrags-Katalog Schule/Versorgung
**Bild:** Textseite: A11 (Schulzeile 56.A.1.AT: unkorrigiert 2019 = 3 h informativ; AC1:2020 bindet die 3 h über Fußnote c an erhöhte Anforderungen; 2025 normativer Anhang, Schulzeile bleibt 3 h; keine aus CAD-Symbolen abgeleitete Betriebsdauer), A12 (OIB/Berichtigung: Schulen ≤3.200 m² allgemeine, >3.200 m² erhöhte Anforderungen; Schwelle = Netto-Grundfläche; drei Geschosse beweisen keine Gesamtfläche), A13 (560.9: je Brandabschnitt Leuchten abwechselnd auf ≥2 Stromkreise; je Endstromkreis ≤20 Leuchten und ≤60 % Nennstrom — nicht mit absoluter 20-Leuchten-Gebäudeobergrenze verwechseln; Einzelbatterie ausgenommen), A14 (Funktionserhalt nach Leitungsweg/letztem Brandabschnitt), A15 (lokalen Ausfall der Allgemeinbeleuchtung erfassen; >20 SL im zusammenhängenden Gebäudeteil → automatische Prüfeinrichtung; BMA-Aktivierung schon ab AC1:2020).
> „AC1:2020 ersetzt die Tabelle und bindet die Dauer über Fußnote c an erhöhte Anforderungen.“
> „Je Endstromkreis höchstens 20 Leuchten und höchstens 60 % des Nennstroms der Überstrom-Schutzeinrichtung ... nicht mit einer absoluten Obergrenze von 20 Leuchten im Gebäude verwechseln.“
> „Bei mehr als 20 Sicherheitsleuchten im zusammenhängenden Gebäudeteil ist die bezeichnete automatische Prüfung erforderlich.“
**Linien:** keine
**DXF-Abgleich:**  · Handles — · kein Planbezug; 20-Leuchten-Cap je ENDSTROMKREIS konsistent zur Engine (circuit_hint Cap≈20), präzisiert als Nicht-Gebäudeobergrenze; kein Widerspruch zu NB-R21
**Bewertung:** neu → Schul-Versorgungsbedingungen (nachrangig, Enis/Validierung): Nennbetriebsdauer Schule 3 h NUR an erhöhte Anforderungen gebunden (Fußnote c, AC1:2020) — nicht hardcoden; Einstufungs-Schwelle 3.200 m² Netto-Grundfläche projektweit klären (LB/Bescheid); je Endstromkreis ≤20 Leuchten/≤60 % Nennstrom + Wechselschaltung je Brandabschnitt; >20 SL je Gebäudeteil → automatische Prüfeinrichtung

## S. 13 — Anforderungen als Prüfaufträge (Fortsetzung, A16–A19)
**Bereich:** Normkatalog / Prüfaufträge
**Bild:** Reine Textseite ohne Plan. Vier Prüfaufträge: A16 (ISO 7010/3864 — CAD-Block ist Planzeichen, keine Produktzertifizierung), A17 (OVE E 8101 2019/AC1:2020/2025 — Dauerbetriebskennzeichnung von Zeichen; CAD-Drehwinkel oder grünes Symbol beweisen keinen Dauerbetrieb), A18 (EN 1838 4.1.2 j–k — barrierefreie Stellen/Rufanlagen ohne pauschalen 5-lx-Wert), A19 (EN 1838 4.3.9 — Raum ohne direkten Rettungswegzugang: dazwischenliegender Rettungsweg mitbeleuchten).
> „RIVO-Geometrie/Weißbalken ist eine CAD-Konvention, keine Zertifizierung und keine eigenständige normierte Pfeilbedeutung.“
> „CAD-Drehwinkel oder grünes Symbol beweisen keinen Dauerbetrieb.“
> „Ist Sicherheitsbeleuchtung in einem Raum erforderlich und besteht kein direkter Zugang zu den Rettungswegen im angrenzenden Brandabschnitt, muss auch der dazwischenliegende Rettungsweg beleuchtet werden.“
**Linien:** keine
**DXF-Abgleich:** None · Handles — · Textseite ohne Planbezug, kein DXF-Abgleich.
**Bewertung:** neu → Prüfauftrags-Katalog A16–A19: ISO-7010/3864- und Dauerbetriebs-Nachweis liegen außerhalb der CAD-Darstellung (Symbolgrafik ≠ Betriebsart-Beleg); EN 1838 4.3.9 = innenliegende Räume ohne direkten Rettungswegzugang erzwingen beleuchteten Zwischen-Rettungsweg; 4.1.2 j–k barrierefreie Stellen als hervorzuhebende Punkte ohne Pauschal-Lux — alles als offene Nachweise, nicht als Platzierungs-Automatik.

## S. 14 · SG — F-SG-01 Westlicher Ausgang und Ankunft aus TH 4
**Bereich:** Westlicher Gangabschluss, TH 4, Ausgang Lehrerparkplatz, Putzraum UG.64
**Bild:** Planausschnitt mit orange gerahmtem westlichem Ausgang, AP-Leuchte SG-026 außen an der Tür, RZ SG-027/SG-028 im Gang (Front nach Osten) und Tür-RZ SG-044 am TH-4-Ausgang (Front nach Süden). Grün gestrichelte Wege: P1 aus TH 4 von unten nach Norden in den Gang, P2 aus dem langen Gang von rechts nach Westen; türkise 2D-Sichtlinie längs des Gangs. Putzraumtür liegt im selben Bereich, ist aber kein Ausgang.
> „SG-044 wendet seine Zeichenfront nach unten zum Stiegenbereich. SG-027 und SG-028 wenden die Front nach rechts; so treffen Gangbenutzer auf die Vorderseite.“
> „Die Nähe zur Putzraumtür verlangt eine eindeutige Zuordnung zur tatsächlichen Ausgangsöffnung.“
> „Welche Außenfläche anschließend dauerhaft als sicherer Bereich genutzt wird, ist im Lageplan nicht vollständig nachgewiesen.“
**Leuchten im Bild:** (SG-026) antipanik, (SG-027) right, (SG-028) right, (SG-044) down
**Personen:** P1: TH 4 (von unten), P2: langer Hauptgang von Osten
**Linien:** grün gestrichelte Weginterpretation TH 4 → Gang → westliche Außentür; türkise 2D-Sichtlinie im Gang; orange Rahmen um die Ausgangsöffnung
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34B86, 34BA4, 34B68, 8C37F · SG-027=34B86, SG-028=34BA4 (beide RIVO_ARR_down0, rot 90°, Welt-Pfeil 0°=+X rechts — deckt 'Front nach rechts'); SG-044=34B68 (rot 0°, Welt-Pfeil 270°=-Y unten — deckt 'Front nach unten'). SG-026: Kennung 8C37F vorhanden, aber nächster RIVO_Antipanik0-Block im Leuchten-Inventar liegt 34 m entfernt → Symbol-Handle ?
**Bewertung:** bestaetigt:NB-R12

## S. 15 · SG — F-SG-01 Westlicher Ausgang und Ankunft aus TH 4 — Begründung/Normbezug
**Bereich:** Westlicher Ausgang (E–J-Begründungsseite)
**Bild:** Textseite: SG-026 beleuchtet den Außen-/Türbereich, drei RZ orientieren; Symboltausch-Register (SG-026 STANDARD_SL→RIVO_Antipanik0 0°; SG-027/028 STANDARD_RZ_PU→RIVO_ARR_down0 90°; SG-044 →RIVO_ARR_down0 0°). Normbezüge A01/A02/A03/A09/A17 mit Bedingungen; offene Nachweise orange (Außenbeleuchtung bis sicherer Bereich, Türfreigabe, Montagehöhen, Stufenbeleuchtung, Betriebsart).
> „Der eingerahmte Ausgang verhindert, dass die danebenliegenden Türen als Ziel missverstanden werden.“
> „Am Endausgang müssen Zeichen, tatsächliche Tür und beleuchteter Außenweg zusammenpassen. Eine Leuchte unmittelbar an der Tür beweist noch nicht den weiteren Außenweg.“
> „Erkennungsweite l = z × h; z=100 für extern beleuchtete, z=200 für hinterleuchtete Zeichen.“
**Leuchten im Bild:** (SG-026) antipanik, (SG-027) right, (SG-028) right, (SG-044) down
**Linien:** keine (Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34B86, 34BA4, 34B68 · Symboltausch-Angaben (down0/90°, down0/0°, bothsided-frei) decken sich mit Block+Rotation der Handles; Antipanik-Handle zu SG-026 im Inventar nicht auffindbar → ?
**Bewertung:** neu → Endausgang-Dreiklang (EN 1838 4.1.2 g): RZ, tatsächliche Ausgangstür und beleuchteter Außenweg bis zum sicheren Bereich müssen zusammen nachgewiesen werden — eine Leuchte an der Tür allein belegt den Außenweg nicht; verwechselbare Nachbartüren (Putzraum) verlangen eindeutige Zuordnung des RZ zur echten Ausgangsöffnung.

## S. 16 · SG — F-SG-01 Einzelbezüge — SG-026 (Typ N), SG-027 (Typ I)
**Bereich:** Westlicher Ausgang, Detailkrops
**Bild:** Zwei Detailausschnitte mit orangem Kreis um die besprochene Position. SG-026: AP-Position außen vor dem westlichen Ausgang, 'beleuchtet statt zu beschildern', Lichtachse ist keine Fluchtrichtungsangabe. SG-027: inneres Tür-/Durchgangszeichen, RIVO_ARR_down0 mit Blockrotation 90°, Zeichenfront und grafischer Pfeil im Plan nach rechts (+X), Annäherung von Osten frontal.
> „SG-026 beleuchtet statt zu beschildern.“
> „Eine Lichtachse ist keine Fluchtrichtungsangabe.“
> „RIVO_ARR_down0; Blockrotation 90°. Zeichenfront im Plan: rechts (+X). Grafischer Pfeil im Plan: rechts (+X).“
**Leuchten im Bild:** (SG-026) antipanik, (SG-027) right
**Linien:** orange Markierungskreise um SG-026 und SG-027 in den Krops
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34B86, 8C37F, 8C380 · SG-027=34B86 (Kennung 8C380, Abstand 299 mm, ARR_down0 rot 90° → Welt-Pfeil +X) bestätigt die Seitentexte; SG-026 nur über Kennung 8C37F belegt, Antipanik-Symbol-Handle ?
**Bewertung:** bestaetigt:NB-R07

## S. 17 · SG — F-SG-01 Einzelbezüge — SG-028 (Typ I), SG-044 (Typ I)
**Bereich:** Westliche Ausgangsfolge und TH-4-Ausgang
**Bild:** Zwei Detailkrops. SG-028: gangseitiges Zeichen östlich von SG-027, Front nach Osten (+X), erster Orientierungspunkt für Personen aus dem langen Hauptgang. SG-044: Türzeichen am nördlichen Ausgang von TH 4, Front nach Süden (-Y) in den Stiegenbereich — eine Person aus TH 4 muss die Front vor dem Türdurchgang erkennen; erst danach schließen die Gangzeichen an.
> „Die Person aus dem längeren Hauptgang erreicht zuerst diesen gangseitigen Orientierungspunkt.“
> „Eine Person aus TH 4 muss die südliche Front vor dem Türdurchgang erkennen.“
> „Erster Türpunkt der Stiegenankunft; erst danach schließen die Gangzeichen SG-028/027 an die westliche Ausgangsfolge an.“
**Leuchten im Bild:** (SG-028) right, (SG-044) down
**Linien:** orange Markierungskreise; keine Wegdarstellung in den Krops
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34BA4, 34B68, 8C381, 8C394 · SG-028=34BA4 (rot 90°, Welt-Pfeil +X, 394 mm zur Kennung) und SG-044=34B68 (rot 0°, Welt-Pfeil 270°=-Y, 412 mm) decken die beschriebenen Fronten exakt.
**Bewertung:** bestaetigt:NB-R04

## S. 18 · SG — F-SG-02 Westgang: Abzweig und beidseitiges Zeichen
**Bereich:** Westgang-Kreuzung bei Gartenspielgeräten/Nebenräumen, Möbellager UG.56, Mehrzweckraum UG.55
**Bild:** Planausschnitt des Ost-West-Hauptgangs mit T-Abzweig nach Süden. SG-029 (beidseitig, an der Verzweigung), SG-030 (einseitig, weiter östlich, Front nach Osten), SG-031 (gerichtete Sicherheitsleuchte als grüner Punkt weiter östlich). P1 kommt aus dem südlichen Verbindungsgang, P2 längs des Hauptgangs von Osten; grün gestrichelte Wege vereinigen sich nach Westen Richtung TH 4/F-SG-01.
> „Diese Ankünfte dürfen nicht gleichgesetzt werden.“
> „Die zwei Fronten von SG-029 liegen bei Rotation 0° nördlich und südlich. […] längs des Ost-West-Gangs ist derselbe Block überwiegend seitlich zu sehen.“
> „„Beidseitig“ bedeutet hier nicht rundum sichtbar.“
**Leuchten im Bild:** (SG-029) beidseitig, (SG-030) right, (SG-031) aufheller
**Personen:** P1: südlicher Verbindungsgang, P2: Hauptgang von Osten
**Linien:** grün gestrichelte Wege von Süden und Osten, Vereinigung nach Westen; Leader von SG-031-Label zum grünen Leuchtpunkt
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34BC2, 34BE0, 8C382, 8C383, 8C384 · SG-029=34BC2 (RIVO_ARR_bothsided0, rot 0°, 440 mm zur Kennung); SG-030=34BE0 (ARR_down0 rot 90°, Welt-Pfeil +X, 299 mm). SG-031: nächster RIVO_Aufheller_Variante0 (34C36) liegt 5,7 m von Kennung 8C384 → Zuordnung ?
**Bewertung:** bestaetigt:NB-R16

## S. 19 · SG — F-SG-02 Westgang: Abzweig und beidseitiges Zeichen — Begründung/Normbezug
**Bereich:** Westgang-Kreuzung (E–J-Begründungsseite)
**Bild:** Textseite: SG-031 als beleuchtender Punkt östlich der Verzweigung (Richtungsinformation liegt getrennt bei SG-029/030); quadratische Spot-Bestandsform wird nach Auftraggebervorgabe mit RIVO_Aufheller_Variante dargestellt. Symboltausch-Register: SG-029 STANDARD_RZ_PLPR→RIVO_ARR_bothsided0 0°, SG-030 →RIVO_ARR_down0 90°, SG-031 STANDARD_SPOT_SL_DA→RIVO_Aufheller_Variante0 (Bestands-/Zieldrehung 0°). Normbezüge A01/A03/A09.
> „SG-029 einfach um 90° zu drehen würde zugleich den dargestellten Pfeil ändern.“
> „Richtung des gezeichneten Pfeils und Seite, von der er gelesen wird, müssen getrennt geprüft werden.“
> „Seine quadratische Spot-Bestandsform mit mittigem Kreis wird nach Auftraggebervorgabe mit RIVO_Aufheller_Variante dargestellt.“
**Leuchten im Bild:** (SG-029) beidseitig, (SG-030) right, (SG-031) aufheller
**Linien:** keine (Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34BC2, 34BE0 · Registerangaben (bothsided0/0°, down0/90°) stimmen mit den Handles überein; Aufheller-Handle zu SG-031 nicht eindeutig (Kandidat 34C36, 5,7 m) → ?
**Bewertung:** bestaetigt:NB-R07

## S. 20 · SG — F-SG-02 Einzelbezüge — SG-029 (Typ I), SG-030 (Typ I)
**Bereich:** Westgang-Kreuzung, Detailkrops
**Bild:** Zwei Detailkrops. SG-029: beidseitiges Zeichen an der Gangverzweigung, RIVO_ARR_bothsided0 Rotation 0°, Fronten unten (-Y) und oben (+Y), grafischer Pfeil links (-X) nach Westen; Ankünfte aus Nord/Süd sehen je eine Front, Längsläufer nur die Kante. SG-030: einseitiges Zeichen, Front nach Osten (+X) für die Annäherung aus dem östlichen Gangabschnitt.
> „Ankünfte aus den nördlichen oder südlichen Anschlüssen können je eine Front sehen; Personen längs des Ost-West-Gangs sehen dagegen eher die Kante.“
> „Welche Türen beide Fronten tatsächlich bedienen und ob ein Längsläufer ausreichend orientiert wird, ist mit Personen und realer Montage zu prüfen.“
**Leuchten im Bild:** (SG-029) beidseitig, (SG-030) right
**Linien:** orange Markierungskreise in den Krops
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34BC2, 34BE0, 8C382, 8C383 · Beide Handles bestätigt (Abstände 440/299 mm zur jeweiligen Kennung); Block/Rotation decken die Textangaben Fronten ±Y bzw. +X.
**Bewertung:** bestaetigt:NB-R16

## S. 21 · SG — F-SG-02 Einzelbezüge — SG-031 (Typ E)
**Bereich:** Hauptgang östlich der westlichen Verzweigung, vor Mehrzweckraum UG.55
**Bild:** Detailkrop mit orangem Kreis um den grünen Aufheller-Punkt SG-031 im Hauptgang. Beleuchtender SL-DA-Spot ohne RZ-Front; Bodenlichtverteilung des Gangabschnitts und der Raumzugänge muss aus der tatsächlichen Optik geprüft werden. Symboltausch STANDARD_SPOT_SL_DA → RIVO_Aufheller_Variante0, Bestands- und Zieldrehung 0°; die schwarze Bestandsachse entfällt grafisch.
> „das Objekt trägt keine RZ-Front.“
> „eine Leuchtenachse ist kein Rettungszeichenpfeil.“
> „Die schwarze Bestandsachse entfällt im RIVO-Block; Originalrotation und Produktdaten bleiben dokumentiert. Die reale optische Abstrahlung ist daraus nicht nachgewiesen.“
**Leuchten im Bild:** (SG-031) aufheller
**Linien:** orange Markierungskreis um SG-031
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 8C384 · Kennung 8C384 belegt; nächster RIVO_Aufheller_Variante0-Block (34C36) liegt 5,7 m entfernt — Symbol-Handle nicht sicher zuordenbar → ?
**Bewertung:** neu → Aufheller-Formregel (Auftraggebervorgabe, Schule): Bestands-Spot STANDARD_SPOT_SL_DA (quadratisch, mittiger Kreis) wird 1:1 als RIVO_Aufheller_Variante dargestellt — Bestandsrotation wird als Zieldrehung übernommen, die gezeichnete Leuchtenachse entfällt grafisch und ist KEIN Fluchtrichtungspfeil; Originalrotation/Produktdaten bleiben im Register, Optik-/Lux-Nachweis bleibt offen.

## S. 22 · SG — F-SG-03 Gartenspielgeräte: Lichtachse im schmalen Abschnitt
**Bereich:** Schmaler Nebenraum-/Verbindungsgang bei Gartenspielgeräten und AR MZ, südlich des Westgangs
**Bild:** Planausschnitt eines schmalen Nord-Süd-Verbindungsgangs. SG-048 als grüner Aufheller-Punkt neben Person P1; grün gestrichelte Weginterpretation führt nach Norden zum Hauptgang, wo ein RZ sichtbar ist. Die alternative südliche Treppe ist ohne Freigabe des zugehörigen Außenwegs nicht als gleichwertiger Fluchtweg festgelegt.
> „Dies ist eine beleuchtende Sicherheitsleuchte ohne Rettungszeichen. Eine Betrachtung ihrer Front als Wegweiser wäre sachlich falsch.“
> „Eine alternative Benutzung der südlichen Treppe ist ohne Freigabe des zugehörigen Außenwegs nicht als gleichwertiger Fluchtweg festgelegt.“
**Leuchten im Bild:** (SG-048) aufheller
**Personen:** P1: angrenzende Nebenräume / südlicher Türbereich
**Linien:** grün gestrichelte Weginterpretation nach Norden zum Hauptgang-RZ
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 8C399 · Kennung 8C399 belegt; kein RIVO_Aufheller_Variante0-Block nahe der Kennung im Leuchten-Inventar (nächster Kandidat 34C1C, 7,7 m) — Symbol-Handle ? (Inventar möglicherweise unvollständig).
**Bewertung:** bestaetigt:NB-R25

## S. 23 · SG — F-SG-03 Gartenspielgeräte — Begründung/Normbezug
**Bereich:** Schmaler Verbindungsgang (E–J-Begründungsseite)
**Bild:** Textseite: SG-048 als eigener Leuchtpunkt für Boden und Türbereich im schmalen Gang, ohne Freigabe der südlichen Tür zu behaupten. Symboltausch STANDARD_SPOT_SL_DA → RIVO_Aufheller_Variante0 mit Bestands-/Zieldrehung 270°; frühere Achse und Rotation belegen weder Fluchtrichtung noch Lichtverteilung. Normbezüge A02/A03; offen: Montage, Leuchtendaten, Abschattung durch Lagergut, Nutzbarkeit der südlichen Tür.
> „die frühere gezeichnete Achse und 270°-Rotation belegen weder Fluchtrichtung noch Lichtverteilung.“
> „Die Formzuordnung kann projektübergreifend übernommen werden; optische Richtung, Montage und tatsächliche Lichtabdeckung müssen trotzdem anhand des jeweiligen Produkts geprüft werden.“
**Leuchten im Bild:** (SG-048) aufheller
**Linien:** keine (Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 8C399 · Registerangabe 270°→270° nicht am Symbol verifizierbar, da Aufheller-Handle zur Kennung fehlt → ?
**Bewertung:** neu → Rotationserhalt bei Aufheller-Formtausch: Zieldrehung = Bestandsdrehung (hier 270°), auch wenn die Achse grafisch entfällt — die alte Achse/Rotation ist reine Dokumentation und darf nie als Fluchtrichtungs- oder Lichtverteilungs-Beleg gelesen werden; Formzuordnung ist projektübergreifend übertragbar, Optik-Nachweis bleibt produktspezifisch.

## S. 24 · SG — F-SG-03 Einzelbezüge — SG-048 (Typ E)
**Bereich:** Schmaler westlicher Nebenraum-/Verbindungsgang, Detailkrop
**Bild:** Detailkrop mit orangem Kreis um SG-048 (grüner Aufheller-Punkt) im schmalen Gang zwischen Türen. Wiederholung des Formtauschs STANDARD_SPOT_SL_DA → RIVO_Aufheller_Variante0 mit erhaltener 270°-Drehung; keine Zeichenfront vorhanden; der Abschnitt ist vom östlich anschließenden Musikraum getrennt zu betrachten. Türverbindungen, Hindernisse und Weiterführung zur Hauptgangfolge sind noch nicht vollständig belegt.
> „Personen aus den angrenzenden Nebenräumen treten in den schmalen Gang; eine konkrete Zeichenfront existiert hier nicht.“
> „Erfasst die Beleuchtung dieses eigenen Stich-/Nebengangabschnitts, nicht die des großen Musikraums östlich davon.“
**Leuchten im Bild:** (SG-048) aufheller
**Linien:** orange Markierungskreis um SG-048
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 8C399 · Wie S.22/23: Kennung belegt, Aufheller-Symbol-Handle im Inventar nicht auffindbar → ?
**Bewertung:** neu → Aufheller-Zuständigkeitsschnitt: ein beleuchtender Punkt gehört genau EINEM Gang-/Stichabschnitt und wird nicht auf angrenzende Großräume (Musikraum) angerechnet — Abschnittsgrenzen bestimmen den Lux-Nachweisraum.

## S. 25 · SG — F-SG-04 Mehrzweckraum mit Musik: zwei Saalbereiche und nördlicher Ausgang
**Bereich:** Mehrzweckraum inkl. Musik (UG.55), nördliche Doppeltür zum Hauptgang
**Bild:** Grundriss-Ausschnitt: Tür-RZ SG-036 an der nördlichen Doppeltür (orange markiert), zwei runde Aufheller SG-045 (westlicher Saalteil) und SG-049 (östlich, raumtiefer) im selben Saal. Grün gestrichelte Weginterpretation läuft von SG-049 nach Norden zur Doppeltür und im Hauptgang weiter nach Westen. Eine Person (P1) steht beim östlichen Saalteil nahe SG-049 mit Blick nach Norden zur Tür.
> „SG-036 zeigt seine weiße Vorderkante nach Süden in den Mehrzweckraum.“
> „Von außen ist die Rückseite desselben einseitigen Zeichens kein zusätzlicher Wegweiser.“
> „Das benachbarte Möbellager ist ein eigener Bereich; diese beiden Leuchten belegen keine dortige Ausleuchtung.“
**Leuchten im Bild:** SG-036 down, SG-045 aufheller, SG-049 aufheller
**Personen:** östlicher Saalteil bei SG-049 (P1)
**Linien:** grün gestrichelt = Weginterpretation Saal->Nordtür->Hauptgang West; orange Rechteck = markierte Doppeltür
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34BFE, 34C1C, 34C36 · SG-036=34BFE RIVO_ARR_down0 rot 0 (Welt-Pfeil 270=unten, Front in den Saal) bestätigt; SG-045=34C1C, SG-049=34C36 beide RIVO_Aufheller_Variante0 rot 0 bestätigt (Kennung-Leuchte-Abstand 239-538 mm).
**Bewertung:** bestaetigt:NB-R01

## S. 26 · SG — F-SG-04 Mehrzweckraum mit Musik (E-J: Begründung, CAD-Zuordnung, Normbezug)
**Bereich:** Mehrzweckraum inkl. Musik (UG.55)
**Bild:** Textseite ohne Planbild: Symboltausch-Protokoll (SG-036 STANDARD_RZ_PU->RIVO_ARR_down0 0°; SG-045/049 STANDARD_SPOT->RIVO_Aufheller_Variante0 0°), Normbezüge A01/A04/A08/A12 und offene Nachweise (Möblierung, Veranstaltungsbelegung, Photometrie). Übertragbare Zeichenregel: zwei Leuchten in einem Ausschnitt bedeuten nicht zwei getrennte Räume.
> „A08 — ... Bei besonderer Gefährdung: auf der Arbeitsfläche mindestens 10 % des für die Aufgabe erforderlichen Wartungswerts und mindestens 15 lx ... kein Automatismus allein aus Raumname.“
> „A12 — ... N04 trennt für Schulen ≤3.200 m² allgemeine und >3.200 m² erhöhte Anforderungen ... bezeichnet die Fläche ausdrücklich als Netto-Grundfläche.“
> „Zwei Leuchten in einem Ausschnitt bedeuten nicht automatisch zwei getrennte Räume.“
**Leuchten im Bild:** SG-036 down, SG-045 aufheller, SG-049 aufheller
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34BFE, 34C1C, 34C36 · Symboltausch-Angaben (Blocknamen, Drehung 0°) decken sich mit den DXF-Blöcken der drei Leuchten.
**Bewertung:** neu → Schul-Anforderungsschwelle: OIB-RL2/OVE R12-2 trennen für Schulen bei 3.200 m² NETTO-Grundfläche allgemeine vs. erhöhte Anforderungen (eingeschränkte vs. uneingeschränkte Sicherheitsbeleuchtung); gemischte Nutzung und maßgebende Ausgabe zuerst klären — Flächenschwelle als LB/Norm-Eingang, nicht hardcoden. Zusatz: A08-Gefährdungsflag nie allein aus Raumnamen ableiten.

## S. 27 · SG — F-SG-04 Einzelbezüge (SG-036 Typ H, SG-045 Typ B)
**Bereich:** Mehrzweckraum inkl. Musik (UG.55)
**Bild:** Zwei Detail-Ausschnitte mit orangem Kreis: SG-036 als grünes Tür-RZ mittig an der nördlichen Doppeltür (RIVO_ARR_down0, Blockrotation 0°, Zeichenfront und grafischer Pfeil im Plan unten/-Y); SG-045 als runder grüner Aufheller frei im westlichen Saalteil. Keine zusätzlichen Weglinien in den Details.
> „RIVO_ARR_down0; Blockrotation 0°. Zeichenfront im Plan: unten (-Y).“
> „Runde, richtungsfreie AP-Spot-Darstellung ... Eine Lichtachse ist keine Fluchtrichtungsangabe.“
> „Einziger Türbezug dieser Dreiergruppe; SG-045/049 sind zwei Lichtpositionen im selben Raum.“
**Leuchten im Bild:** SG-036 down, SG-045 aufheller
**Personen:** westlicher Saalteil (bei SG-045) und östlicher Saalteil (bei SG-049)
**Linien:** orange Kreise = besprochene Position, sonst keine
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34BFE, 34C1C · Blockname und Rotation 0° beider Leuchten im DXF bestätigt; Tür-RZ sitzt in der Türachse der Doppeltür.
**Bewertung:** bestaetigt:NB-R01

## S. 28 · SG — F-SG-04 Einzelbezüge (SG-049 Typ B)
**Bereich:** Mehrzweckraum inkl. Musik (UG.55), östlicher raumtiefer Saalteil
**Bild:** Detail-Ausschnitt mit orangem Kreis um den runden Aufheller SG-049 frei in der Saalfläche, ohne Wandkontakt. Nur Raumstempel-Fragmente als Kontext, keine Weglinien. Text charakterisiert die Position als flächige AP-/Aufhellerposition, ausdrücklich kein Wegweiser.
> „Personen aus diesem Saalbereich bewegen sich zur nördlichen Doppeltür SG-036; der Standort ist kein Wegweiser.“
> „Gegenstück zu SG-045 im westlichen Saalteil; beide ... bedienen unterschiedliche Flächenbereiche.“
> „Eine Lichtachse ist keine Fluchtrichtungsangabe.“
**Leuchten im Bild:** SG-049 aufheller
**Personen:** östlicher Saalbereich
**Linien:** orange Kreis = besprochene Position, sonst keine
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34C36 · SG-049=34C36 RIVO_Aufheller_Variante0 rot 0 bestätigt.
**Bewertung:** bestaetigt:NB-R10

## S. 29 · SG — F-SG-05 Werken VS - Reinbereich
**Bereich:** Werkraum VS Reinbereich (UG.54) südlich des Hauptgangs
**Bild:** Grundriss-Ausschnitt: Tür-RZ SG-037 am nördlichen Zugang des Werkraums (orange markiert), Aufheller SG-046 mit Personendarstellung im Raum. Grün gestrichelte Weginterpretation vom Raum zur Nordtür und weiter im Hauptgang nach Osten/Westen; im Gang ein weiteres grünes Symbol als Folgeziel. Vorderseite von SG-037 zeigt nach Süden in den Raum.
> „SG-037 sitzt an seinem Zugang, SG-046 ist der beleuchtende AP-Spot im Raum.“
> „Die Vorderseite von SG-037 zeigt nach Süden in den Raum.“
> „die Raumtür alleine ist noch kein letzter Ausgang.“
**Leuchten im Bild:** SG-037 down, SG-046 aufheller
**Personen:** Werkraum, bei SG-046
**Linien:** grün gestrichelt = Weginterpretation Werkraum->Nordtür->Hauptgang; orange Rechteck = markierte Tür
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34C50, 34C6E · SG-037=34C50 RIVO_ARR_down0 rot 0 (Front nach Süden in den Raum) und SG-046=34C6E RIVO_Aufheller_Variante0 rot 0 bestätigt.
**Bewertung:** bestaetigt:NB-R01

## S. 30 · SG — F-SG-05 Werken VS - Reinbereich (E-J: Begründung, CAD-Zuordnung, Normbezug)
**Bereich:** Werkraum VS Reinbereich (UG.54)
**Bild:** Textseite ohne Planbild: Symboltausch SG-037 (RZ_PU->RIVO_ARR_down0, 0°) und SG-046 (SPOT->Aufheller, 0°); Normbezüge A01/A04/A08. Kernaussage: die AP-Bezeichnung im Produktattribut ersetzt keine Gefährdungsbeurteilung des Werkbetriebs; bei Werkräumen ist neben Fluchtorientierung das sichere Beenden gefährlicher Tätigkeiten zu betrachten.
> „Die AP-Bezeichnung im Produktattribut beschreibt den Bestand; sie ersetzt keine Gefährdungsbeurteilung des Werkbetriebs.“
> „A08 — ... auf der Arbeitsfläche mindestens 10 % des für die Aufgabe erforderlichen Wartungswerts und mindestens 15 lx; Gleichmäßigkeit Uo mindestens 0,1 ... innerhalb 0,5 s erreicht werden.“
> „Bei Werkräumen muss neben der Fluchtorientierung auch ein sicheres Beenden gefährlicher Tätigkeiten betrachtet werden.“
**Leuchten im Bild:** SG-037 down, SG-046 aufheller
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34C50, 34C6E · Symboltausch-Angaben decken sich mit den DXF-Blöcken.
**Bewertung:** neu → Schul-Werkraum-Regel (EN 1838 4.4.1-4.4.7): Räume mit besonderer Gefährdung (Werken, Küche) brauchen zusätzlich zur Flucht-Notbeleuchtung eine Arbeitsplatz-Sicherheitsbeleuchtung (min. 10 % des Wartungswerts, min. 15 lx, Uo>=0,1, innerhalb 0,5 s, für die Gefährdungsdauer) — als lux_nachweis-/Gefährdungsflag je Raum, ausgelöst durch Gefährdungsbeurteilung, NICHT automatisch durch den Raumnamen.

## S. 31 · SG — F-SG-05 Einzelbezüge (SG-037 Typ H, SG-046 Typ B)
**Bereich:** Werkraum VS Reinbereich (UG.54)
**Bild:** Zwei Detail-Ausschnitte mit orangem Kreis: SG-037 als Tür-RZ in der Türachse des nördlichen Werkraum-Ausgangs (RIVO_ARR_down0, 0°, Front/Pfeil unten/-Y in den Raum); SG-046 als runder Aufheller frei in der Raumfläche. Keine Weglinien in den Details.
> „Türzeichen am nördlichen Ausgang des Werkraums Reinbereich; Front nach Süden in den Raum.“
> „Ergänzt das Türzeichen als Raumbeleuchtung; kein zusätzliches Richtungsschild im Hauptgang.“
> „Werkbänke, Maschinen und eine mögliche besondere Gefährdung sind gesondert zu prüfen; der Raumname allein entscheidet dies nicht.“
**Leuchten im Bild:** SG-037 down, SG-046 aufheller
**Personen:** Werkplätze im Raum
**Linien:** orange Kreise = besprochene Position, sonst keine
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34C50, 34C6E · Blockname/Rotation beider Leuchten im DXF bestätigt.
**Bewertung:** bestaetigt:NB-R01

## S. 32 · SG — F-SG-06 Server- und E-Raum am kurzen Stichgang
**Bereich:** Technikstichgang nördlich des Hauptgangs mit Serverraum (UG.59) und E-Raum (UG.58)
**Bild:** Grundriss-Ausschnitt: drei einseitige Tür-RZ an verschiedenen Türen — SG-002 (Serverraum, 90°, Front nach Osten), SG-016 (E-Raum, 90°, Front nach Osten), SG-020 (Stichgang-Südausgang, 180°, Front nach Norden) — plus Gang-Aufheller SG-009 im Stichgang. Grün gestrichelte Wegfolge Raumtür->Stichgang->südliche Gangtür->Hauptgang mit Pfeil nach Süden; zwei Personen P1/P2 aus Serverraum und E-Raum.
> „Die drei einseitigen Zeichen gehören zu verschiedenen Türen; SG-009 beleuchtet den Gang.“
> „SG-002 und SG-016 haben 90° Rotation und wenden die Vorderseite nach Osten zu den Räumen. SG-020 hat 180° und wendet sie nach Norden zum Stichgang.“
> „Die erforderliche Leserichtung wechselt an der gemeinsamen Ausgangstür.“
**Leuchten im Bild:** SG-002 down, SG-009 aufheller, SG-016 down, SG-020 down
**Personen:** Serverraum (P1), E-Raum (P2)
**Linien:** grün gestrichelt = Wegfolge Raumtür->Stichgang->Hauptgang (Pfeil nach Süden)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34CD9, 34CA7 · SG-002=34CD9 und SG-016=34CA7 (beide RIVO_ARR_down0 rot 90, Welt-Pfeil 0=+X/Osten) bestätigt. Für SG-009 und SG-020 liegt in der JSON-Extraktion KEINE Leuchte im Nahbereich der Kennung (nächste Treffer 2,1-2,3 m entfernt, bereits SG-002/016 zugeordnet) — Extraktionslücke, Leuchten-Handles ?
**Bewertung:** bestaetigt:NB-R19

## S. 33 · SG — F-SG-06 Server- und E-Raum am kurzen Stichgang (E-J: Begründung, CAD-Zuordnung, Normbezug)
**Bereich:** Technikstichgang mit Serverraum und E-Raum
**Bild:** Textseite ohne Planbild: Symboltausch aller vier Leuchten (SG-002/016 90°, SG-020 180°, SG-009 Aufheller 270°); Normbezüge A01/A02/A06/A19. Kernaussagen: kurze Strecke kann mehrere nacheinander nötige Blickrichtungen enthalten; 'nahe beieinander' ist kein Löschkriterium für Zeichen; A19-Zwischenweg-Beleuchtung als bedingter Prüfauftrag.
> „A19 — ÖNORM EN 1838 ... 4.3.9: Ist Sicherheitsbeleuchtung in einem Raum erforderlich und besteht kein direkter Zugang zu den Rettungswegen im angrenzenden Brandabschnitt, muss auch der dazwischenliegende Rettungsweg beleuchtet werden.“
> „A06 — OVE E 8101 ... Bei erhöhten Anforderungen zusätzlich Sanitärbereiche ab 8 m², barrierefreie WC-Anlagen und bezeichnete Elektro-/Sicherheitszentralen prüfen ... begründet keine pauschale 60-m²-Schwelle für Schulräume.“
> „Eine kurze Strecke kann mehrere nacheinander nötige Blickrichtungen enthalten. 'Nahe beieinander' ist kein Löschkriterium für Zeichen.“
**Leuchten im Bild:** SG-002 down, SG-009 aufheller, SG-016 down, SG-020 down
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34CD9, 34CA7 · Drehungen 90°/90° (SG-002/016) im DXF bestätigt; SG-009 (Aufheller 270°) und SG-020 (180°) in der JSON-Extraktion nicht auffindbar (siehe S.32).
**Bewertung:** neu → Ketten-/Prüfregeln aus EN 1838 + OVE E 8101 für mehrstufige Raumfolgen: (a) 4.3.9-Zwischenweg — braucht ein Raum Sicherheitsbeleuchtung und hat keinen direkten Zugang zum Rettungsweg des angrenzenden Brandabschnitts, ist der dazwischenliegende Weg (Stichgang) mitzubeleuchten; (b) bei erhöhten Anforderungen zusätzlich Sanitärräume ab 8 m², barrierefreie WCs und E-/Sicherheitszentralen prüfen; (c) RZ dürfen nicht wegen räumlicher Nähe zusammengelegt/gelöscht werden, wenn die Leserichtung wechselt (verschärft NB-R12/NB-R19).

## S. 34 · SG — F-SG-06 Einzelbezüge (SG-002 Typ J, SG-009 Typ E)
**Bereich:** Technikstichgang, Serverraum-Zugang und Gangmitte
**Bild:** Zwei Detail-Ausschnitte mit orangem Kreis: SG-002 als einseitiges Tür-RZ am Serverraumausgang (RIVO_ARR_down0, Blockrotation 90°, Zeichenfront/Pfeil rechts/+X zu den aus dem Raum Kommenden); SG-009 als runder Aufheller im Stichgang zwischen den beiden Raumzugängen (Bestand STANDARD_SPOT_SL_DA 270° -> RIVO_Aufheller_Variante0 270°).
> „Das bei 90 Grad nach Osten zeigende Frontbild ist für Personen aus dem östlich anschließenden Serverraum vorgesehen; Schränke können die Sicht verdecken.“
> „STANDARD_SPOT_SL_DA -> RIVO_Aufheller_Variante0 nach Auftraggeber-Formregel. Bestandsdrehung 270°, neue Blockdrehung 270°; eine Leuchtenachse ist kein Rettungszeichenpfeil.“
> „Die schwarze Bestandsachse entfällt im RIVO-Block; Originalrotation und Produktdaten bleiben dokumentiert.“
**Leuchten im Bild:** SG-002 down, SG-009 aufheller
**Personen:** Serverraum bzw. E-Raum
**Linien:** orange Kreise = besprochene Position, sonst keine
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34CD9 · SG-002=34CD9 RIVO_ARR_down0 rot 90 bestätigt. SG-009: in der JSON-Extraktion keine Aufheller-Leuchte an der Kennung-Position (Extraktionslücke) — Handle ?
**Bewertung:** bestaetigt:NB-R01

## S. 35 · SG — F-SG-06 Einzelbezüge (SG-016 Typ J, SG-020 Typ I)
**Bereich:** Technikstichgang, E-Raum-Zugang und südlicher Gangausgang
**Bild:** Zwei Detail-Ausschnitte mit orangem Kreis: SG-016 als Tür-RZ des E-Raums (RIVO_ARR_down0, 90°, Front rechts/+X nach Osten zum Raum); SG-020 als Zeichen am südlichen Stichgang-Ausgang in den Hauptgang (RIVO_ARR_down0, 180°, Front oben/+Y nach Norden, frontal zum von Norden ankommenden Strom aus beiden Räumen).
> „Türzeichen des E-Raums am westlichen Technikstichgang; Front nach Osten.“
> „Personen aus Serverraum oder E-Raum kommen im Stichgang von Norden auf diese Front zu.“
> „Gemeinsames Folgezeichen nach den verschiedenen Raumtüren SG-002 und SG-016.“
**Leuchten im Bild:** SG-016 down, SG-020 down
**Personen:** Serverraum oder E-Raum, im Stichgang von Norden
**Linien:** orange Kreise = besprochene Position, sonst keine
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34CA7 · SG-016=34CA7 RIVO_ARR_down0 rot 90 bestätigt. SG-020 (laut PDF rot 180): in der JSON-Extraktion keine Leuchte im Nahbereich der Kennung; nächster rot-180-Block 34CF7 ist SG-021 zugeordnet — Handle ?
**Bewertung:** bestaetigt:NB-R07

## S. 36 · SG — F-SG-07 Technikfläche: RZ und zwei rechteckige SL
**Bereich:** Technikfläche (UG.53) zwischen Stichgang und TH 3
**Bild:** Grundriss-Ausschnitt: zwei rechteckige gelb-grüne BASIC-SL-Leuchten SG-010 und SG-017 in der Technikfläche, Tür-RZ SG-021 an der südlichen Tür (orange markiert, 180° gedreht, Front nach Norden zur Fläche). Grün gestrichelte Weginterpretation von P1 in der Fläche zur Südtür und in den Hauptgang; darunter grünes Folgesymbol. Hinweis: der E-Schacht neben TH 3 ist kein Durchgang.
> „Sie enthält zwei rechteckige BASIC-SL-Leuchten und ein Rettungszeichen an der südlichen Tür.“
> „SG-021 ist um 180° gedreht und somit mit seiner Vorderseite nach Norden zur Technikfläche ausgerichtet.“
> „der E-Schacht neben TH 3 ist kein Durchgang.“
**Leuchten im Bild:** SG-010 antipanik, SG-017 antipanik, SG-021 down
**Personen:** Technikfläche (P1, nördlich)
**Linien:** grün gestrichelt = Weginterpretation Technikfläche->Südtür->Hauptgang; türkis gestrichelt = angenommene 2D-Sicht; orange Rechteck = markierte Tür
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 350E4, 350FF, 34CF7 · SG-010=350E4 und SG-017=350FF als RIVO_Antipanik0 rot 0 (im PDF 'rechteckige BASIC-SL' genannt) sowie SG-021=34CF7 RIVO_ARR_down0 rot 180 (Welt-Pfeil 90=+Y/Norden, Front zur Fläche) bestätigt.
**Bewertung:** bestaetigt:NB-R19

## S. 37 · SG — F-SG-07 Technikfläche: RZ und zwei rechteckige SL
**Bereich:** Technikfläche UG.53 (Sockelgeschoss), südliche Tür
**Bild:** Reine Begründungsseite (E-J) ohne Planbild. SG-010 und SG-017 sind zwei rechteckige Bestands-SL in verschiedenen Teilen der Technikfläche, die nach Auftraggeber-Formregel die RIVO_Antipanik-Darstellung erhalten (getrennte Lichtzonen); SG-021 bezeichnet als Tür-RZ die südliche Tür. Normbezug A01/A06/A08; A06 stellt klar, dass die 60-m²-Regel der OVE E 8101 nur verkehrstechnische Einrichtungen betrifft und keine pauschale Schwelle für Schulräume begründet.
> „Aus dem Rechteck folgt weder eine geprüfte Antipanikfläche noch die Eignung für besonders gefährliche Tätigkeiten; Anlagenaufstellung und Photometrie fehlen.“
> „Ziffer 3 ist ausdrücklich auf verkehrstechnische Einrichtungen begrenzt und begründet keine pauschale 60-m²-Schwelle für Schulräume.“
> „J: Symboltausch darf keine neue Funktionsklassifikation verdeckt einführen.“
**Leuchten im Bild:** SG-010 antipanik, SG-017 antipanik, SG-021 down
**Linien:** keine (Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 350E4, 350FF, 34CF7 · SG-010=350E4 RIVO_Antipanik0 rot 0°, SG-017=350FF RIVO_Antipanik0 rot 0°, SG-021=34CF7 RIVO_ARR_down0 rot 180° — deckt sich mit Abschnitt F (Bestandsdrehung/Zieldrehung).
**Bewertung:** bestaetigt:NB-R19

## S. 38 · SG — F-SG-07 Einzelbezüge — SG-010 / SG-017
**Bereich:** Technikfläche UG.53, westlicher und östlicher Raumteil
**Bild:** Zwei DXF-Ausschnitte mit orangem Kreis um SG-010 (westlicher Raumteil, Raumstempel UG.53 Technikfläche) und SG-017 (östlicher Raumteil an der Stiege). Beide sind rechteckige BASIC-SL-Leuchten, grafisch als RIVO_Antipanik0 dargestellt, Drehung 0°. Sie decken die beiden Raumteile ab, weil feste Anlagen Blick und Licht zum Ausgang verdecken können; das Symbol hat keine Wegweiserfront.
> „Feste Anlagen können den Blick zum Ausgang und das Licht verdecken.“
> „Eine Leuchtenachse ist kein Rettungszeichenpfeil.“
> „Das Rechteck ist kein Antipanik-Nachweis.“
**Leuchten im Bild:** SG-010 antipanik, SG-017 antipanik
**Personen:** Technikfläche (Ankunft und Bewegung im Raum)
**Linien:** keine Weg-/Sichtlinien in den Detailausschnitten (Detail ohne zusätzliche Wegbehauptung)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 350E4, 350FF · Beide RIVO_Antipanik0 rot 0.0° im Inventar; Positionen westlich/östlich in der Technikfläche plausibel zu den Ausschnitten.
**Bewertung:** bestaetigt:NB-R10

## S. 39 · SG — F-SG-07 Einzelbezüge — SG-021
**Bereich:** Technikfläche UG.53, südliche Ausgangstür
**Bild:** DXF-Ausschnitt mit orangem Kreis um das Tür-RZ SG-021 an der südlichen Tür der Technikfläche (Türbogen 120/210 sichtbar, darunter grüner Aufheller im Gang). Front nach Norden in den Raum; ein orientierendes Zeichen bedient die gesamte Technikfläche, während SG-010/017 ausschließlich beleuchten.
> „Türzeichen am südlichen Ausgang der Technikfläche; Front nach Norden in den Raum.“
> „Orientierende Position für die gesamte Technikfläche; SG-010/017 sind dagegen ausschließlich beleuchtend.“
> „RIVO_ARR_down0; Blockrotation 180°. Zeichenfront im Plan: oben (+Y).“
**Leuchten im Bild:** SG-021 down
**Personen:** Raumteile bei SG-010 und SG-017
**Linien:** keine (Detail ohne zusätzliche Wegbehauptung)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34CF7 · 34CF7 RIVO_ARR_down0 rot 180°, Welt-Pfeil 90° (+Y, in den Raum) — exakt Abschnitt F der Fallseite; Ein-RZ-für-ganzen-Raum wie NB-R02.
**Bewertung:** bestaetigt:NB-R01

## S. 40 · SG — F-SG-08 Hauptgang vor Schulwart, Teeküche und Knoten
**Bereich:** Hauptgang mit Schulwart UG.52, Teeküche UG.51, östlicher Verbindungsknoten
**Bild:** Fallseite mit Planbild: Hauptgang, darunter Schulwart FM (UG.52) und Teeküche FM (UG.51). P1 im Schulwart und P2 in der Teeküche treten mit grün gestrichelten Weglinien nach Norden in den Gang und weiter nach Osten zum Knoten (SG-033, türkise Sichtannahme). SG-038/039 sind Tür-RZ mit Front nach Süden zu ihren Räumen, SG-032 ist der Gang-Aufheller weiter westlich; SG-033 steht mit 272,32° annähernd quer zur Ankunft von Westen — die Abweichung von 270° stammt aus dem Bestand und wurde nicht begradigt.
> „SG-032 beleuchtet den Gang, die übrigen Positionen sind Rettungszeichen.“
> „SG-038 und SG-039 wenden die Front nach Süden zu ihren Räumen.“
> „Die geringe Abweichung von 270° stammt aus dem Bestand und wurde nicht begradigt.“
**Leuchten im Bild:** SG-032 aufheller, SG-033 down, SG-038 down, SG-039 down
**Personen:** P1 Schulwart UG.52, P2 Teeküche UG.51
**Linien:** grün gestrichelt: Weg beider Personen in den Gang und nach Osten zum Knoten; türkis: 2D-Sicht auf SG-033; orange: markierte Bauteile
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34D6F, 34D8D, 34DAB · SG-033=34D6F rot 272.32° (Welt-Pfeil 182.32°), SG-038=34D8D und SG-039=34DAB rot 0° (Welt-Pfeil 270°, Front -Y zu den Räumen) — deckungsgleich mit Abschnitt D/F. Aufheller-Handle für SG-032 im Inventar nicht eindeutig zuordenbar (nächster Aufheller 34C6E, ~6,6 m vom Kennungstext): ?
**Bewertung:** bestaetigt:NB-R01

## S. 41 · SG — F-SG-08 Hauptgang vor Schulwart, Teeküche und Knoten (Begründung)
**Bereich:** Hauptgang UG.52/UG.51 und östlicher Verbindungsknoten
**Bild:** Begründungsseite (E-J) ohne Planbild. SG-032 (STANDARD_SPOT_SL_DA → RIVO_Aufheller_Variante0) hellt den Gang auf, die benachbarten RZ übernehmen Türen und Folgeentscheidung. Abschnitt G begrenzt die Zusammenlegung: ein einziges Gangzeichen wäre bei geschlossenen Türen oder Wandvorsprüngen nicht automatisch gleichwertig zu den einzelnen Raum-Türzeichen. Normbezug A01/A02/A03 (EN 1838 4.1.1, 4.1.2 a-g, 4.2.1-4.2.2 Mittellinien-Lux).
> „Die benachbarten Rettungszeichen sind für Türen und die folgende Entscheidung zuständig, nicht für Bodenlicht.“
> „Die Raumzeichen durch ein einziges Gangzeichen zu ersetzen wäre bei geschlossenen Türen oder Wandvorsprüngen nicht automatisch gleichwertig.“
> „J: Leuchten können im selben Bild verschiedene Etappen erklären: aus dem Raum heraus und danach am gemeinsamen Entscheidungspunkt weiter.“
**Leuchten im Bild:** SG-032 aufheller, SG-033 down, SG-038 down, SG-039 down
**Linien:** keine (Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34D6F, 34D8D, 34DAB · Drehungen aus Abschnitt F (272.319°/0°/0°) stimmen mit Inventar überein; Mehrtüren-Bedienung nur mit Sichtprüfung = Bedingung, kein Widerspruch zur Mollgasse-Mehrfachbedienung.
**Bewertung:** bestaetigt:NB-R08

## S. 42 · SG — F-SG-08 Einzelbezüge — SG-032 / SG-033
**Bereich:** Hauptgang vor Technik-/Schulwartbereich; Übergang zum zentralen Knoten
**Bild:** Zwei DXF-Ausschnitte: SG-032 (grüner Kreis-Spot mit X, Aufheller) mittig im Hauptgang — er betrifft Gangfläche und Türannäherungen, nicht die Richtungsinformation. SG-033 (einseitiges down-RZ) am Übergang vom Hauptgang zum zentralen Knoten, Front annähernd nach Westen (Blockrotation 272,319°), sodass die westliche Ankunft frontal auf das Zeichen zukommt.
> „Er betrifft Gangfläche und Türannäherungen an diesem Abschnitt, nicht die Richtungsinformation der Zeichen.“
> „Personen aus dem westlichen Hauptgang kommen auf die Westfront zu.“
> „SG-034 übernimmt dort eine andere, beidseitige Abzweigrolle.“
**Leuchten im Bild:** SG-032 aufheller, SG-033 down
**Personen:** westlicher Hauptgang
**Linien:** keine (Detail ohne zusätzliche Wegbehauptung)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34D6F · SG-033=34D6F RIVO_ARR_down0 rot 272.32°, Zeichenfront -X = frontal zum West-Strom (Erstleuchten-Frontalsicht). SG-032-Handle unsicher: ?
**Bewertung:** bestaetigt:NB-R07

## S. 43 · SG — F-SG-08 Einzelbezüge — SG-038 / SG-039
**Bereich:** Nördliche Ausgänge von Schulwartraum UG.52 und Teeküche UG.51
**Bild:** Zwei DXF-Ausschnitte mit Tür-RZ SG-038 (nördlicher Ausgang Schulwartraum) und SG-039 (nördlicher Ausgang Teeküche), beide RIVO_ARR_down0 mit Blockrotation 0°, Zeichenfront nach unten (-Y) in den jeweiligen Raum. Jeder Raum erhält sein eigenes Türzeichen; die beiden Türen dürfen nicht durch einen einzigen generischen Ankunftspunkt ersetzt werden.
> „Türzeichen am nördlichen Ausgang des Schulwartraums; Front nach Süden.“
> „Separater Raum neben SG-038; die beiden Türen dürfen nicht durch einen einzigen generischen Ankunftspunkt ersetzt werden.“
> „Eigener Raumzugang westlich der Teeküche SG-039; SG-032 ist dagegen gemeinsame Gangbeleuchtung.“
**Leuchten im Bild:** SG-038 down, SG-039 down
**Personen:** Schulwartraum UG.52, Teeküche UG.51
**Linien:** keine (Detail ohne zusätzliche Wegbehauptung)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34D8D, 34DAB · Beide RIVO_ARR_down0 rot 0°, Welt-Pfeil 270° (-Y, raumseitige Front) — bestätigt Tür-RZ raumseitig mit Pfeil in den Raum wie NB-R01.
**Bewertung:** bestaetigt:NB-R01

## S. 44 · SG — F-SG-09 TH 3, Windfang und Ausgang nach außen
**Bereich:** TH 3 (Raumcode 4.1.2), Windfang 4.1.1, östliche Außentür, E-Schacht
**Bild:** Fallseite mit Planbild: TH 3 mündet im Sockelgeschoss in einen Windfang, eine zweite Tür verbindet den südlichen Gang mit dem Windfang, die Außentür liegt rechts (Osten). P1 kommt aus dem Stiegenhaus von Westen (Tür SG-003), P2 aus dem Schulgang von Süden (Tür SG-011); beide Wege laufen grün gestrichelt über das beidseitige SG-001 zur Außentür SG-004; SG-005 ist die beleuchtende Außenposition. Orange Rahmen markieren die beiden Windfang-Bauteile.
> „Es gibt mindestens zwei Ankünfte: aus dem Stiegenhaus von Westen und aus dem Schulgang von Süden. Beide müssen zur östlichen Außentür gelangen.“
> „SG-001 hat zwei Ansichtsseiten und weist im Grundriss nach Osten; für die südliche Ankunft ist eine Front passend, bei rein westlicher Annäherung ist der seitliche Blick eigens zu prüfen.“
> „Im Windfang folgt die Führung über SG-001 zur Außentür SG-004.“
**Leuchten im Bild:** SG-001 beidseitig, SG-003 down, SG-004 down, SG-005 antipanik, SG-011 down
**Personen:** P1 TH 3 (von Westen), P2 Schulgang (von Süden)
**Linien:** grün gestrichelt: beide Fluchtwege zum Ausgang Ost; türkis gestrichelt: 2D-Sicht auf SG-001/SG-004; orange: markierte Windfang-Bauteile
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 3511A, 34D15, 34D51, 350AD, 34D33 · SG-001=3511A RIVO_ARR_bothsided0 rot 180°, SG-003=34D15 rot 277°, SG-004=34D51 rot 270°, SG-005=350AD Antipanik0 rot 0°, SG-011=34D33 rot 7° — alle Drehungen decken sich mit Abschnitt F (S.45).
**Bewertung:** bestaetigt:NB-R16

## S. 45 · SG — F-SG-09 TH 3, Windfang und Ausgang nach außen (Begründung)
**Bereich:** TH 3, Windfang, östliche Außentür
**Bild:** Begründungsseite (E-J) ohne Planbild. Die Türfolge trennt Stiegenraum, Windfang und Außenbereich; kein Weg wird durch den E-Schacht oder über das Geländer gezeichnet, die Schrägstellung von SG-003/011 folgt dem Bestand. Abschnitt F listet alle fünf Symboltausche mit Drehungen; Normbezug A01/A02/A09 (Erkennungsweite l = z × h, z=100 extern / z=200 hinterleuchtet, keine Umrechnung aus der CAD-Symbolgröße).
> „Kein Weg wird durch den E-Schacht oder über das Geländer gezeichnet.“
> „Nur ein Zeichen am Außenausgang könnte von hinter der Stiegenhaustür oder dem Wandvorsprung verdeckt sein. Eine Vereinfachung setzt die Prüfung beider Ankünfte voraus.“
> „J: Am gemeinsamen Ausgang müssen alle relevanten Ankünfte geprüft werden; die Stiegenrichtung allein beschreibt den Windfang noch nicht.“
**Leuchten im Bild:** SG-001 beidseitig, SG-003 down, SG-004 down, SG-005 antipanik, SG-011 down
**Linien:** keine (Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 3511A, 34D15, 34D51, 350AD, 34D33 · Drehungen 180/277/270/0/7° identisch im Inventar; Schrägstellungen (277°, 7°) sind Bestandsrotationen, nicht begradigt.
**Bewertung:** bestaetigt:NB-R16

## S. 46 · SG — F-SG-09 Einzelbezüge — SG-001 / SG-003
**Bereich:** Windfang 4.1.1 und Stiegenhaustür TH 3
**Bild:** Zwei DXF-Ausschnitte: SG-001 als beidseitiges Richtungszeichen im Windfang zwischen Stiegenhaustür, südlicher Gangtür und östlicher Außentür (Blockrotation 180°, Fronten +Y/-Y, grafischer Pfeil +X nach Osten). SG-003 als Tür-RZ zwischen TH 3 und Windfang, Front annähernd nach Westen (Blockrotation 277°) — die aus TH 3 kommende Person muss es vor dem Durchgang sehen. Offener Befund: die westliche Ankunft trifft bei SG-001 eher die Schmalseite.
> „Ankunft aus dem südlichen Gang trifft die nach Süden gerichtete Ansichtsseite; Ankunft aus TH 3 von Westen trifft eher die Schmalseite.“
> „Verbindet zwei Ankünfte innerhalb des Windfangs; SG-003 und SG-011 kennzeichnen zuvor verschiedene Türen, SG-004 die Außentür.“
> „Eine aus TH 3 kommende Person muss dieses Zeichen vor dem Durchgang in den Windfang sehen.“
**Leuchten im Bild:** SG-001 beidseitig, SG-003 down
**Personen:** südlicher Gang, TH 3 von Westen
**Linien:** keine (Detail ohne zusätzliche Wegbehauptung)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 3511A, 34D15 · 3511A RIVO_ARR_bothsided0 rot 180° (ein Block, nicht zwei gespiegelte Einzel-RZ wie im Mollgasse-GT), 34D15 rot 277° (Welt-Pfeil 187°). Schmalseiten-Problem der westlichen Ankunft = dokumentierte NB-R07-Grenze, als offener Befund geführt.
**Bewertung:** bestaetigt:NB-R16

## S. 47 · SG — F-SG-09 Einzelbezüge — SG-004 / SG-005
**Bereich:** Östliche Außentür des Windfangs und Außenseite des Ausgangs
**Bild:** Zwei DXF-Ausschnitte: SG-004 als Zeichen an der östlichen Außentür, Front nach Westen (-X) in den Windfang, sodass Personen aus beiden Windfangzugängen die Ausgangstafel von innen sehen. SG-005 ist die einzige erfasste beleuchtende Position unmittelbar außen am Windfangausgang (Bestand CONCEPT AP 3W WA, gelb-grünes Antipanik-Rechteck an der Fassade); sie hat keine Rettungszeichenfront und ist von der weiter entfernten Fassadenreihe SG-006/007/008 zu trennen.
> „Zeichen an der östlichen Außentür des Windfangs; Front nach Westen in den Windfang.“
> „Beleuchtende Position unmittelbar außen am Windfangausgang, im Bestand CONCEPT AP 3W WA.“
> „AP ausdrücklich im Produktattribut; rechteckiges AP-Symbol der Bibliothek. Keine neue lichttechnische Bewertung.“
**Leuchten im Bild:** SG-004 down, SG-005 antipanik
**Personen:** beide Windfangzugänge (TH 3 und Schulgang)
**Linien:** keine (Detail ohne zusätzliche Wegbehauptung)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34D51, 350AD · SG-004=34D51 rot 270° (Front -X raumseitig = Ausgangstür-Muster wie NB-R03), SG-005=350AD RIVO_Antipanik0 rot 0° außen an der Fassade. Außenleuchte am letzten Ausgang ist in NB-R01..R27 nicht als eigene Regel abgedeckt (EN 1838 4.1.2, Engine-Owner-Regel existiert, Regelbasis-Lücke).
**Bewertung:** neu → Außenleuchte am letzten Ausgang: unmittelbar außen am Gebäudeausgang eine beleuchtende Position (Antipanik-/SL-Typ, keine RZ-Front) für den Außenweg vom letzten Ausgang (EN 1838 4.1.2); getrennt von weiter entfernten Fassadenleuchten zu führen

## S. 48 · SG — F-SG-09 Einzelbezüge — SG-011
**Bereich:** Südlicher Zugang vom Schulgang in den Windfang
**Bild:** DXF-Ausschnitt mit orangem Kreis um das Tür-RZ SG-011 am südlichen Zugang vom Schulgang in den Windfang (Doppeltür sichtbar, Waschraum UG.44 rechts). Front annähernd nach Süden zum ankommenden Schulgang-Strom; Blockrotation 7° folgt der Bestands-Schrägstellung. Erster Türbezug der südlichen Ankunft, danach folgt die neue Blicksituation zu SG-001/004.
> „Türzeichen am südlichen Zugang vom Schulgang in den Windfang; Front annähernd nach Süden.“
> „Eine Person aus dem Schulgang sieht die Front vor dem Türdurchgang; danach folgt die neue Blicksituation zu SG-001/004.“
> „RIVO_ARR_down0; Blockrotation 7°. Zeichenfront im Plan: unten (-Y).“
**Leuchten im Bild:** SG-011 down
**Personen:** Schulgang von Süden
**Linien:** keine (Detail ohne zusätzliche Wegbehauptung)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34D33 · 34D33 RIVO_ARR_down0 rot 7°, Welt-Pfeil 277° — Tür-RZ frontal zum ankommenden Strom, Bestandsrotation beibehalten; Etappen-Kette (Tür-RZ → Knoten-RZ) wie NB-R08/NB-R12.
**Bewertung:** bestaetigt:NB-R01

## S. 49 · SG — F-SG-10 Damen-Garderobe und Waschraum
**Bereich:** Damen-Garderobe UG.43 + Waschraum noerdlich des Quergangs, Weg zum Knoten und Windfang TH 3
**Bild:** Fallseite A-D mit Planausschnitt: mehrstufige Raumfolge Waschraum -> Damengarderobe -> Quergang. Gruen gestrichelte Weginterpretation fuehrt von P1 (Waschraum) ueber die Garderobe zur Tuer bei SG-022 und nach Sueden/Westen in den Quergang. SG-012 (inneres Tuer-RZ, schraeg zur inneren Verbindung), SG-013 (Aufheller in der Garderobe), SG-022 (aeusseres Tuer-RZ, orange markiert, Front nach Norden in die Garderobe). Jede Front muss fuer ihre eigene Tuer gelesen werden.
> „Die erkennbare Folge fuehrt aus dem Waschraum ueber den zugehoerigen Garderobenbereich zur Tuer bei SG-022 und in den Quergang.“
> „SG-022 wendet seine Front ungefaehr nach Norden in die Garderobe. Jede Front muss fuer ihre eigene Tuer gelesen werden.“
> „Eine Sicht durch die geschlossene Zwischentuer wird nicht vorausgesetzt.“
**Leuchten im Bild:** SG-012 down, SG-013 aufheller, SG-022 down
**Personen:** P1 Waschbereich/Damengarderobe
**Linien:** gruen gestrichelt Weginterpretation Waschraum->Garderobe->Quergang; orange Rechteck um SG-022-Bauteil
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34E79, 34E97, 34E1F · Alle drei Kennungen im DXF gefunden: SG-012=34E79 RIVO_ARR_down0 rot 277, SG-013=34E97 RIVO_Aufheller_Variante0 rot 0, SG-022=34E1F RIVO_ARR_down0 rot 187 — deckungsgleich mit Seitentext.
**Bewertung:** bestaetigt:NB-R01

## S. 50 · SG — F-SG-10 Damen-Garderobe und Waschraum (E-J)
**Bereich:** Damen-Garderobe + Waschraum, Begruendung/CAD-Zuordnung/Normbezug
**Bild:** Textseite E-J ohne Planbild. E: Aufheller SG-013 fuer die Bewegungsflaeche zwischen den beiden Tuerentscheidungen, ersetzt die Tuerzeichen SG-012/022 nicht. F: Symboltausch STANDARD_RZ_PU->RIVO_ARR_down0 (277 Grad / 187 Grad) und STANDARD_SPOT_DA->RIVO_Aufheller_Variante0 (0 Grad). H: Normbezuege A01/A04/A06/A19, darunter EN 1838 4.3.9 (Zwischenweg-Beleuchtung) und OVE E 8101 Sanitaerbereiche ab 8 m2. J: Sanitaerfolgen mit mehreren Tueren brauchen gestufte Betrachtung.
> „er ersetzt die Tuerzeichen SG-012/022 nicht“
> „A19 — ... 4.3.9: Ist Sicherheitsbeleuchtung in einem Raum erforderlich und besteht kein direkter Zugang zu den Rettungswegen im angrenzenden Brandabschnitt, muss auch der dazwischenliegende Rettungsweg beleuchtet werden.“
> „A06 — ... Bei erhoehten Anforderungen zusaetzlich Sanitaerbereiche ab 8 m2, barrierefreie WC-Anlagen und bezeichnete Elektro-/Sicherheitszentralen pruefen. ... begruendet keine pauschale 60-m2-Schwelle fuer Schulraeume.“
> „Sanitaerfolgen mit mehreren Tueren benoetigen eine gestufte Betrachtung von Wegweisung und Beleuchtung.“
**Leuchten im Bild:** SG-012 down, SG-013 aufheller, SG-022 down
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34E79, 34E97, 34E1F · F-Block-Drehungen (277/0/187) stimmen mit DXF-rot_deg der drei Handles ueberein.
**Bewertung:** neu → Mehrstufige Raum-/Tuerfolge (Raum->Raum->Gang, z.B. Sanitaerfolge): jede Tuer der Folge erhaelt ihr eigenes Tuer-RZ mit eigener Front; ein Aufheller im Zwischenraum ersetzt kein Tuer-RZ; nach EN 1838 4.3.9 ist der dazwischenliegende Rettungsweg mitzubeleuchten (bedingter Pruefauftrag, Brandabschnitt + Erforderlichkeit zuerst feststellen). Erweitert NB-R01/NB-R19 um die Ketten-Dimension.

## S. 51 · SG — F-SG-10 Einzelbezuege (SG-012, SG-013)
**Bereich:** Damenwaschraum-Tuer und Damengarderobe
**Bild:** Einzelbezugsseite mit zwei Detailausschnitten. SG-012 Typ I: inneres Tuer-RZ vom westlichen Damenwaschraum zur Garderobe, RIVO_ARR_down0 Blockrotation 277 Grad, Zeichenfront und grafischer Pfeil im Plan links (-X); Person aus dem Waschraum naehert sich der Front. SG-013 Typ F: AP-DA-Aufheller in der Damengarderobe zwischen beiden Tueren, Blockdrehung 0 Grad; eine Leuchtenachse ist kein Rettungszeichenpfeil.
> „Eine Person aus dem Waschraum naehert sich dieser Front und gelangt erst danach in die Garderobe.“
> „SG-013 ersetzt keines der beiden Tuerzeichen.“
> „eine Leuchtenachse ist kein Rettungszeichenpfeil“
**Leuchten im Bild:** SG-012 down, SG-013 aufheller
**Personen:** Waschraum (beschrieben, nicht gezeichnet)
**Linien:** orange Kreise um die besprochenen Positionen, keine Weglinien
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34E79, 34E97 · SG-012=34E79 rot 277 (Welt-Pfeil 187 = links/-X-nah), SG-013=34E97 Aufheller rot 0 — Seitentext bestaetigt.
**Bewertung:** bestaetigt:NB-R01

## S. 52 · SG — F-SG-10 Einzelbezuege (SG-022)
**Bereich:** Ausgangstuer Damengarderobe -> Quergang
**Bild:** Einzelbezugsseite SG-022 Typ I: aeusseres Tuer-RZ der Damengarderobe in den suedlich angrenzenden Gang. RIVO_ARR_down0, Blockrotation 187 Grad, Zeichenfront und grafischer Pfeil im Plan oben (+Y), also Front nach Norden in die Garderobe zur von innen ankommenden Person. Offener Befund: Blickrichtung nach Austritt und Sicht zum naechsten Gangzeichen bei realem Tuerblatt pruefen.
> „Personen aus Garderobe oder vorherigem Waschraum kommen von innen auf die Front zu.“
> „RIVO_ARR_down0; Blockrotation 187. Zeichenfront im Plan: oben (+Y).“
**Leuchten im Bild:** SG-022 down
**Personen:** Damengarderobe/Waschraum (beschrieben)
**Linien:** orange Kreis um SG-022
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34E1F · SG-022=34E1F RIVO_ARR_down0 rot 187 (Welt-Pfeil 97) — identisch mit Seitenangabe.
**Bewertung:** bestaetigt:NB-R01

## S. 53 · SG — F-SG-11 Herren-Garderobe und Waschraum
**Bereich:** Herren-Garderobe UG.45 + Waschraum, gespiegeltes Gegenstueck zum Damenbereich
**Bild:** Fallseite A-D mit Planausschnitt: gespiegelte Raumfolge Herrenwaschraum -> Herrengarderobe -> Quergang bei SG-024, weiter nach Westen zum Knoten und Norden zu TH 3. P1 im inneren Bereich, gruene Weginterpretation nach Sueden. SG-015 ist annaehernd nach Osten lesbar (statt Westen wie SG-012), SG-024 nach Norden. Kernaussage: raeumliche Aehnlichkeit ersetzt keine Pruefung der gespiegelten Zugaenge.
> „Die raeumliche Aehnlichkeit zum Damenbereich ersetzt keine Pruefung seiner gespiegelten Zugaenge.“
> „SG-015 ist annaehernd nach Osten lesbar, SG-024 nach Norden. Die Drehung des ersten Zeichens unterscheidet sich damit vom Damenbereich.“
**Leuchten im Bild:** SG-014 aufheller, SG-015 down, SG-024 down
**Personen:** P1 Herrenwaschraum/innerer Bereich
**Linien:** gruen gestrichelt Weginterpretation nach Sueden mit Abzweig nach Westen; orange Rechteck um SG-024
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34EB3, 34E5B, 34E3D · SG-014=34EB3 Aufheller rot 0, SG-015=34E5B down rot 97, SG-024=34E3D down rot 187 — Spiegelung zur Damenseite (SG-012 rot 277) im DXF nachvollzogen.
**Bewertung:** bestaetigt:NB-R07

## S. 54 · SG — F-SG-11 Herren-Garderobe und Waschraum (E-J)
**Bereich:** Herren-Garderobe + Waschraum, Begruendung/CAD-Zuordnung/Normbezug
**Bild:** Textseite E-J. E: Aufheller SG-014 in der getrennten Herrengarderobe; Trennwand verhindert Mitbeleuchtung der Damengarderobe. F: SG-014 Aufheller 0 Grad, SG-015 down 97 Grad, SG-024 down 187 Grad. G nennt die Grenze: eine bloss kopierte Drehung aus dem Damenbereich wuerde die relevante Vorderseite vertauschen. H: gleiche Normbezuege A01/A04/A06/A19 wie F-SG-10. J: aehnliche Nachbarraeume sind keine identischen Symbolfaelle; Tuerlage und Ankunftsseite entscheiden.
> „Eine bloss kopierte Drehung aus dem Damenbereich wuerde die relevante Vorderseite vertauschen.“
> „Aehnliche Nachbarraeume sind keine identischen Symbolfaelle; Tuerlage und Ankunftsseite entscheiden.“
> „Die Damengarderobe wird wegen der Trennwand dadurch nicht mitbeleuchtet.“
**Leuchten im Bild:** SG-014 aufheller, SG-015 down, SG-024 down
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34EB3, 34E5B, 34E3D · F-Block-Drehungen (0/97/187) stimmen mit DXF ueberein; SG-015 rot 97 vs. SG-012 rot 277 belegt die nicht-kopierte, gespiegelte Drehung.
**Bewertung:** bestaetigt:NB-R07

## S. 55 · SG — F-SG-11 Einzelbezuege (SG-014, SG-015)
**Bereich:** Herrengarderobe und Herrenwaschraum-Tuer
**Bild:** Einzelbezugsseite. SG-014 Typ F: eigene AP-DA-Aufheller-Position in der Herrengarderobe vor dem oestlichen Waschraumbereich, Blockdrehung 0 Grad; Trennwand verhindert Gleichsetzung mit SG-013. SG-015 Typ I: inneres Tuer-RZ vom oestlichen Herrenwaschraum in die Garderobe, RIVO_ARR_down0 Blockrotation 97 Grad, Zeichenfront und Pfeil im Plan rechts (+X); Person kommt von Osten auf die Front zu.
> „die Trennwand verhindert eine Gleichsetzung mit SG-013“
> „Eine Person aus dem Waschraum kommt von Osten auf die Front zu, bevor sie sich in der Garderobe neu orientiert.“
> „Inneres Gegenstueck zu SG-012 auf der anderen Seite“
**Leuchten im Bild:** SG-014 aufheller, SG-015 down
**Personen:** oestlicher Herrenwaschraum (beschrieben)
**Linien:** orange Kreise um die besprochenen Positionen
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34EB3, 34E5B · SG-014=34EB3 Aufheller rot 0, SG-015=34E5B down rot 97 (Welt-Pfeil 7 = rechts/+X-nah) — Seitentext bestaetigt.
**Bewertung:** bestaetigt:NB-R01

## S. 56 · SG — F-SG-11 Einzelbezuege (SG-024)
**Bereich:** Ausgangstuer Herrengarderobe -> Quergang
**Bild:** Einzelbezugsseite SG-024 Typ I: aeusseres Tuer-RZ der Herrengarderobe zum Gang, RIVO_ARR_down0 Blockrotation 187 Grad, Zeichenfront und Pfeil im Plan oben (+Y), Front nach Norden zur von innen kommenden Person. Zweiter Tuerdurchgang nach SG-015; raeumlich von SG-022 (Damengarderobe) zu unterscheiden. Offener Befund: Sicht in der Garderobe und Anschlussorientierung im Gang sind nicht durch die Nachbarleuchte SG-023 bewiesen.
> „Personen aus der Herrengarderobe und zuvor aus dem oestlichen Waschraum treffen die Raumfront.“
> „Sicht innerhalb der Garderobe und Anschlussorientierung im Gang sind nicht durch die benachbarte Leuchte SG-023 bewiesen.“
**Leuchten im Bild:** SG-024 down
**Personen:** Herrengarderobe/oestlicher Waschraum (beschrieben)
**Linien:** orange Kreis um SG-024
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34E3D · SG-024=34E3D RIVO_ARR_down0 rot 187 (Welt-Pfeil 97) — identisch mit SG-022-Geometrie, aber eigener Handle im Herrenbereich.
**Bewertung:** bestaetigt:NB-R01

## S. 57 · SG — F-SG-12 Verbindungsknoten, WC Beh. und Technikzugang
**Bereich:** Gangkreuzung Hauptgang/Quergang/Suedgang; barrierefreies WC UG.39 und Technikraum UG.40
**Bild:** Fallseite A-D mit grossem Planausschnitt der Kreuzung. Gruene Weginterpretation fuehrt vom Knoten nach Norden zu TH 3/Windfang; Ankuenfte aus Westgang, Garderoben im Osten und Suedgang (P2). SG-034 ist ein beidseitiges RZ am Knoten (Fronten ca. West/Ost, Pfeil ca. Nord, Drehung 277 Grad) fuer die beiden Querankuenfte; SG-035 (orange markiert) ist das Tuer-RZ des Technikraums UG.40; SG-023 und SG-047 sind Gang-Aufheller; SG-040 liegt im WC UG.39.
> „SG-034 ist beidseitig um 277 Grad gedreht: Seine Fronten liegen ungefaehr westlich/oestlich, sein Pfeil weist ungefaehr nach Norden. Das passt zur Zusammenfuehrung der beiden Querankuenfte“
> „fuer eine Person unmittelbar aus Sueden ist der Blick staerker seitlich.“
> „Das benachbarte WC UG.39 hat einen eigenen westlichen Ausgang in den Suedgang.“
**Leuchten im Bild:** SG-023 aufheller, SG-034 beidseitig, SG-035 down, SG-040 aufheller, SG-047 aufheller
**Personen:** P2 Suedgang
**Linien:** gruen gestrichelte Fluchtwege aus Ost/West/Sued zum Knoten und nach Norden; tuerkise 2D-Sichtlinie am Knoten; orange Rechteck um SG-035
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34F6E, 34F50, 34E01, 34DE7, 34F85 · Alle 5 Kennungen im DXF: SG-023=34F6E Aufheller rot 7.78, SG-034=34F50 RIVO_ARR_bothsided0 rot 277, SG-035=34E01 down rot 8, SG-040=34DE7 Aufheller rot 0, SG-047=34F85 Aufheller rot 277.78 — deckungsgleich.
**Bewertung:** bestaetigt:NB-R16

## S. 58 · SG — F-SG-12 Verbindungsknoten, WC Beh. und Technikzugang (E-J)
**Bereich:** Kreuzungsknoten, barrierefreies WC UG.39, Technikraum UG.40 — Begruendung/Normbezug
**Bild:** Textseite E-J. E: SG-023/047 sind Bodenlichtpunkte im Gang, SG-034/035 liefern Richtungs- und Tuerinformation; SG-040 liegt im barrierefreien WC UG.39, wo Antipanik nach A05 zu pruefen ist. F: fuenf Symboltausche inkl. STANDARD_RZ_PLPR->RIVO_ARR_bothsided0 (277 Grad). H: A02 (Kreuzungen: Leuchte muss beide Richtungen ausleuchten, keine pauschale RZ-Block-Forderung), A05 (EN 1838 4.3.8: WC fuer Menschen mit Behinderung braucht Antipanik, keine 8-m2-Grenze), A18 (4.1.2 j-k Rufanlagen/Schutzbereiche, kein pauschaler 5-lx-Wert). I: Ruf-/Alarmanlage nicht belegt, wird nicht erfunden.
> „A05 — ... 4.3.8: Toiletten fuer Menschen mit Behinderung benoetigen Antipanikbeleuchtung. Bedingung: Raum ist tatsaechlich eine Toilette fuer Menschen mit Behinderung. Diese Klausel nennt keine 8-m2-Grenze und gilt nicht automatisch fuer jeden barrierefreien Raum.“
> „A02 — ... Bei Richtungsaenderungen und Kreuzungen muss die Sicherheitsleuchte beide Richtungen ausleuchten; dies ist keine pauschale Forderung nach einem bestimmten RZ-Block.“
> „Es wird keine solche Einrichtung erfunden und kein pauschaler 5-lx-Wert angesetzt.“
> „Kreuzung, barrierefreies WC und angrenzender Technikbereich verlangen unterschiedliche Nachweise trotz raeumlicher Naehe.“
**Leuchten im Bild:** SG-023 aufheller, SG-034 beidseitig, SG-035 down, SG-040 aufheller, SG-047 aufheller
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34F6E, 34F50, 34E01, 34DE7, 34F85 · F-Block-Drehungen (7.78/277/8/0/277.78) stimmen mit den DXF-rot_deg aller fuenf Handles ueberein.
**Bewertung:** neu → Barrierefreies WC (Toilette fuer Menschen mit Behinderung) benoetigt Antipanikbeleuchtung nach EN 1838 4.3.8 — eigener Antipanik-Trigger unabhaengig von Sichtblockade (NB-R10) und Flaeche; KEINE pauschale 8-m2- oder 60-m2-Schwelle fuer Schulraeume (OVE-60-m2-Ziffer gilt nur verkehrstechnischen Einrichtungen); Ruf-/Alarmanlagen (4.1.2 j-k) nur beruecksichtigen, wenn tatsaechlich belegt — nichts erfinden.

## S. 59 · SG — F-SG-12 Einzelbezuege (SG-023, SG-034)
**Bereich:** Quergang vor den Garderobenausgaengen und zentraler Kreuzungsknoten
**Bild:** Einzelbezugsseite. SG-023 Typ D: Aufheller (SL-Spot) im Quergang vor beiden Garderobenausgaengen SG-022/024, Bestandsdrehung 7.78 Grad beibehalten; die Bestandsachse ist keine Fluchtrichtung, er ersetzt weder Garderobenleuchten noch Rettungszeichen. SG-034 Typ H: beidseitiges Richtungszeichen RIVO_ARR_bothsided0 am zentralen Knoten, Blockrotation 277 Grad, Zeichenfronten links (-X) und rechts (+X), grafischer Pfeil oben (+Y); Personen aus West- und Ostgang sehen unterschiedliche Ansichtsseiten, suedliche Laengsankunft trifft eher die Kante.
> „Er betrifft den gemeinsamen Tuervorbereich ausserhalb der Raeume und ersetzt weder die Garderobenleuchten noch die Rettungszeichen.“
> „Die 7,78-Grad-Achse gehoert zur Bestandsdarstellung und ist keine Fluchtrichtung“
> „Personen aus westlichem oder oestlichem Quergang sehen unterschiedliche Ansichtsseiten; eine suedliche Laengsankunft trifft eher die Kante.“
**Leuchten im Bild:** SG-023 aufheller, SG-034 beidseitig
**Personen:** westlicher und oestlicher Quergang (beschrieben)
**Linien:** orange Kreise um die besprochenen Positionen
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34F6E, 34F50 · SG-023=34F6E Aufheller rot 7.78 (Bestandsrotation uebernommen), SG-034=34F50 bothsided rot 277 — Seitentext bestaetigt; ein RZ-Paar bedient zwei Gegenstroeme wie Mollgasse-GT.
**Bewertung:** bestaetigt:NB-R16

## S. 60 · SG — F-SG-12 Einzelbezuege (SG-035, SG-040)
**Bereich:** Technikraum UG.40 (Nordtuer) und barrierefreies WC UG.39
**Bild:** Einzelbezugsseite. SG-035 Typ J: Tuer-RZ an der noerdlichen Tuer von UG.40 Technik zum Quergang, RIVO_ARR_down0 Blockrotation 8 Grad, Zeichenfront und Pfeil im Plan unten (-Y), also Front nach Sueden in den Technikraum zur ankommenden Person. SG-040 Typ C: richtungsfreie Aufheller-/AP-Position im barrierefreien WC UG.39, Blockrotation 0 Grad; stellt keine Richtung zum Ausgang dar, WC hat eigene Westtuer zum Suedgang. Klare raeumliche Trennung der Nachweise beider Raeume.
> „Tuerzeichen an der noerdlichen Tuer von UG.40 Technik zum Quergang; Front annaehernd nach Sueden in den Technikraum.“
> „SG-040 stellt keine Richtung zum Ausgang dar.“
> „Aus dem benachbarten Technikraumzeichen SG-035 ergibt sich kein Nachweis der Ausgangskennzeichnung oder Sichtfuehrung dieses WC.“
> „Eine Lichtachse ist keine Fluchtrichtungsangabe.“
**Leuchten im Bild:** SG-035 down, SG-040 aufheller
**Personen:** UG.40 Technik (beschrieben), WC UG.39 (beschrieben)
**Linien:** orange Kreise um die besprochenen Positionen
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34E01, 34DE7 · SG-035=34E01 down rot 8 (Welt-Pfeil 278 = unten/-Y-nah), SG-040=34DE7 Aufheller rot 0 — Technikraum-Tuerleuchte nach NB-R19-Muster, WC-Leuchte als eigener Raum-Nachweis.
**Bewertung:** bestaetigt:NB-R19

## S. 61 · SG — F-SG-12 Einzelbezüge
**Bereich:** nördlicher Abschnitt des schrägen Südgangs vor dem zentralen Knoten (bei UG.39 WC Beh)
**Bild:** Einzelbezug-Seite zu SG-047 (Typ D) mit einem Planausschnitt: orange eingekreister grüner Aufheller-Punkt im Gang, daneben Raumstempel Gang/UG.39 WC Beh und Türmaße. Der Text erklärt den SL-Spot als beleuchtenden Gangpunkt ohne Schildfront, getrennt von der Garderobenbeleuchtung SG-053/056. Symboltausch STANDARD_SPOT_SL zu RIVO_Aufheller_Variante0, Bestands- und Blockdrehung 277,78 Grad.
> „eine Leuchtenachse ist kein Rettungszeichenpfeil“
> „Die 277,78-Grad-Achse stammt aus dem Bestandsprodukt und ist keine bestätigte Fluchtrichtung; Lichtverteilung und Gangabdeckung fehlen.“
> „das Symbol hat keine Schildfront“
**Leuchten im Bild:** SG-047 aufheller
**Linien:** kein Weg- oder Sichtliniennetz; orange Detailkreis um SG-047
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34F85 · 34F85 = RIVO_Aufheller_Variante0, rot 277.78°, xy [-2154, 5871] — Lage und Rotation decken sich mit Kennung SG-047 (8C397, Abstand ca. 275 mm); PDF-Angaben bestätigt.
**Bewertung:** neu → bestandsachse_keine_fluchtrichtung — die aus dem Bestandsprodukt übernommene Block-/Leuchtenachse (hier 277,78°) eines SL/Aufhellers ist KEINE Fluchtrichtungs- und keine photometrische Aussage; Originalrotation nur dokumentieren, nie als Pfeil interpretieren

## S. 62 · SG — F-SG-13 Gymnastiksaal: Zugang und direkter Außenausgang
**Bereich:** Gymnastiksaal UG.49 mit westlichem Gangzugang und südlichem Ausgang ins Freie
**Bild:** Fallseite A–D mit Planausschnitt des Gymnastiksaals: zwei AP-Leuchten SG-018/019 im Saal, Tür-RZ SG-041 (westliche Saaltür, orange gerahmt) und SG-042 (südliche Saaltür, orange gerahmt). Grün gestrichelter Weg von P1 im westlichen Quergang ostwärts durch den Saal mit Ast nach Süden durch SG-042 ins Freie und Ast nach Nordosten zu P2. SG-041 wendet die Front nach Westen zum Gang, SG-042 nach Norden in den Saal.
> „SG-041 wendet die Front nach Westen zum ankommenden Gangbenutzer. Damit ist dieses Zeichen kein frontal lesbarer Rückwegweiser für eine bereits im Saal stehende Person östlich der Tür.“
> „Der Außenabgang ist gesondert zu beleuchten und auf sichere Fortsetzung zu prüfen.“
**Leuchten im Bild:** SG-018 antipanik, SG-019 antipanik, SG-041 down, SG-042 down
**Personen:** P1 westlicher Quergang vor der Saaltür, P2 nordöstlicher Bereich (Wegfortsetzung)
**Linien:** grün gestrichelte Weginterpretation P1→Saal→südlicher Ausgang bzw. Ast zu P2; türkise 2D-Sichtannahme; orange Rahmen um beide Saaltüren
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 3552F, 3554A, 34F32, 34F14 · 3552F/3554A = RIVO_Antipanik0 rot 96.55° (SG-018/019), 34F32 = RIVO_ARR_down0 rot 277° (SG-041), 34F14 = RIVO_ARR_down0 rot 187° (SG-042) — Lagen nahe den Kennungslabels, Rotationen wie im PDF.
**Bewertung:** bestaetigt:NB-R07

## S. 63 · SG — F-SG-13 Gymnastiksaal: Zugang und direkter Außenausgang (E–J)
**Bereich:** Gymnastiksaal UG.49 — Begründung, CAD-Zuordnung, Normbezug
**Bild:** Reine Textseite E–J: Symboltauschliste (SG-018/019 STANDARD_SL→RIVO_Antipanik0 96.5526°; SG-041 STANDARD_RZ_PU→RIVO_ARR_down0 277°; SG-042 dito 187°), Normbezüge A01 (EN 1838 4.1.1), A02 (4.1.2 a–g), A04 (4.3.1–4.3.2 Antipanik 0,5 lx, Ud 1:40), A09 (5.5 Erkennungsweite l=z×h). J formuliert die Leseseiten-Regel für Saaltüren.
> „Ein Zeichen an einer Saaltür kann für Personen vor dem Saal bestimmt sein. Die Leseseite entscheidet, welche Ankunft es tatsächlich bedient.“
> „Ein zusätzliches Zeichen zur westlichen Rückflucht wäre nur nach bestätigter Fluchtwegzuordnung sinnvoll. Es darf nicht aus der bestehenden Gang-Ansichtsseite abgeleitet werden.“
> „Antipanik: mindestens 0,5 lx auf der freien Bodenfläche im Kernbereich; ein 0,5 m breiter Randstreifen wird nicht berücksichtigt. Verhältnis kleinste/größte Beleuchtungsstärke Ud mindestens 1:40.“
**Leuchten im Bild:** SG-018 antipanik, SG-019 antipanik, SG-041 down, SG-042 down
**Linien:** keine (Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 3552F, 3554A, 34F32, 34F14 · Symboltausch-Angaben (Blocknamen + Drehungen 96.55/277/187) stimmen mit den DXF-Einträgen überein.
**Bewertung:** bestaetigt:NB-R07

## S. 64 · SG — F-SG-13 Einzelbezüge (SG-018, SG-019)
**Bereich:** Gymnastiksaal UG.49 — Saalflächen-Antipanik west/ost
**Bild:** Zwei Einzelbezüge (Typ O) mit Detailausschnitten: orange eingekreiste rechteckige AP-Leuchten SG-018 (westliche Saalhälfte) und SG-019 (östliche Saalhälfte), beide ohne umgebende Wandgeometrie im Detail. AP ist ausdrücklich im Produktattribut (BSK-Angabe); Blockrotation 96,5526°; die Lichtachse wird ausdrücklich nicht als Fluchtrichtungsangabe gewertet.
> „Personen im westlichen Saalteil müssen zwischen tatsächlichen Saalausgängen orientiert werden; SG-018 selbst ist kein Zeichen.“
> „Eine Lichtachse ist keine Fluchtrichtungsangabe.“
> „Geräte, Trennungen, Verdunkelung und die Abdeckung bis zum südlichen Ausgang sind nicht photometrisch nachgewiesen.“
**Leuchten im Bild:** SG-018 antipanik, SG-019 antipanik
**Linien:** keine; nur orange Detailkreise
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 3552F, 3554A · Beide RIVO_Antipanik0 mit rot 96.55° im Saalbereich nahe der Kennungen — deckungsgleich mit PDF.
**Bewertung:** neu → antipanik_grossraum_saal — großflächiger Versammlungs-/Turnsaal erhält flächige Antipanik-Leuchten (hier 2 AP im Saal) unabhängig von Sichtblockade; Mollgasse-NB-R10 kennt Antipanik nur bei Sichtblockade/Lux-Scheitern, der Saal-Fall ist schulspezifisch (EN 1838 4.3 als Normanker A04)

## S. 65 · SG — F-SG-13 Einzelbezüge (SG-041, SG-042)
**Bereich:** Gymnastiksaal UG.49 — westliche und südliche Saaltür
**Bild:** Zwei Einzelbezüge (Typ K): SG-041 an der westlichen Saaltür, RIVO_ARR_down0 mit Blockrotation 277°, Zeichenfront und grafischer Pfeil im Plan nach links (-X) zum Gang; SG-042 an der südlichen Saaltür, Blockrotation 187°, Front und Pfeil nach oben (+Y) in den Saal. Beide Details mit orange eingekreistem grünem RZ an der Türstelle.
> „Die geometrisch passende frontale Ankunft liegt im westlichen Gang; Personen aus dem Saal sehen die andere Seite.“
> „Die gezeichnete Westfront darf nicht als bewiesene Ausgangsorientierung aus dem Saal ausgegeben werden; Montageart und Fluchtzuordnung sind zu klären.“
> „Eine Person aus dem Saal nähert sich der nordwärts gerichteten Front am südlichen Türdurchgang.“
**Leuchten im Bild:** SG-041 down, SG-042 down
**Linien:** keine; orange Detailkreise an beiden Türstellen
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34F32, 34F14 · 34F32 rot 277° und 34F14 rot 187° (beide RIVO_ARR_down0) — Front-/Pfeilangaben des PDF konsistent mit Blockrotationen.
**Bewertung:** bestaetigt:NB-R07

## S. 66 · SG — F-SG-14 Außenleuchten um den Gymnastiksaal
**Bereich:** Außenfassaden Nord/Ost/Süd des Gymnastiksaals UG.49
**Bild:** Fallseite A–D mit Übersichtsplan: fünf rechteckige Leuchten außerhalb der Saalkontur — SG-006/007/008 als Reihe an der Nordfassade, SG-025 an der schrägen Ostfassade, SG-043 südlich östlich des Saalausgangs. Keine Weg-, Sicht- oder Personenmarkierungen; die Leuchten werden ausdrücklich als beleuchtende Fassadenpositionen ohne Rettungszeichenfunktion beschrieben.
> „Ihre Positionen folgen den Fassaden und sind keine zusätzlichen Rettungszeichen.“
> „Sie wird nicht zu einem durchgehend freigegebenen Rundweg ergänzt: Gelände, Einfriedung und sichere Zielbereiche sind nicht hinreichend belegt.“
> „weder eine gezeichnete Achse noch die Blockrotation ist ein Fluchtrichtungspfeil oder eine photometrische Aussage“
**Leuchten im Bild:** SG-006 antipanik, SG-007 antipanik, SG-008 antipanik, SG-025 antipanik, SG-043 antipanik
**Linien:** keine Weg-/Sichtlinien; nur Leuchtpositionen entlang der Außenkontur
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 36BA5, 36BC2, 36BDF, 36BFC, 36C19 · Kandidaten über Rotationsabgleich: 36BA5/36BC2/36BDF (RIVO_Antipanik0, rot 0°, West-Ost-Reihe = SG-006/007/008), 36BFC (rot 279.21° = SG-025), 36C19 (rot 9.21° = SG-043); Cluster liegt jedoch in anderem Koordinatenbereich als die Kennungslabels — Frame-Zuordnung ?
**Bewertung:** neu → aussenleuchten_kein_wegnachweis — Fassaden-/Außenleuchten entlang der Gebäudekontur belegen KEINEN begehbaren Außenfluchtweg; der Außenweg vom letzten Ausgang bis zum sicheren Bereich ist gesondert festzulegen und zu beleuchten (EN 1838 4.1.2), eine umlaufende Leuchtenanordnung darf nicht als Rundweg interpretiert werden

## S. 67 · SG — F-SG-14 Außenleuchten um den Gymnastiksaal (E–J)
**Bereich:** Außenfassaden des Gymnastiksaals — Begründung, CAD-Zuordnung, Normbezug
**Bild:** Reine Textseite E–J: alle fünf Fassadenleuchten STANDARD_SL_MITTE_PFEIL→RIVO_Antipanik0 mit erhaltener Bestandsdrehung (0/0/0/279.211/9.211 Grad) und Aspektkonflikt (Höhe proportional 44,28 % kleiner). Normbezüge A02 (EN 1838 4.1.2 a–g, Außenweg) und A03 (4.2.1–4.2.2 Rettungsweg-Lux 1 lx Mittellinie). J: umlaufende Anordnung beweist keine Nutzbarkeit des Wegs.
> „Eine bloße Aneinanderreihung rechteckiger Symbole würde einen durchgehenden Außenweg vortäuschen.“
> „Außenleuchten müssen entlang des tatsächlich notwendigen Wegs beurteilt werden; eine umlaufende Anordnung beweist dessen Nutzbarkeit nicht.“
> „Ausgangstüren, Treppenstufen, Niveauwechsel, Richtungsänderungen, Gangkreuzungen und der Außenweg vom letzten Ausgang bis zum sicheren Bereich sind gezielt zu beleuchten.“
**Leuchten im Bild:** SG-006 antipanik, SG-007 antipanik, SG-008 antipanik, SG-025 antipanik, SG-043 antipanik
**Linien:** keine (Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 36BA5, 36BC2, 36BDF, 36BFC, 36C19 · Rotationswerte des PDF (0/0/0/279.211/9.211) exakt in den Kandidaten-Handles wiedergefunden; Koordinaten-Frame der Kennungslabels abweichend — Zuordnung ?
**Bewertung:** neu → aussenleuchten_kein_wegnachweis — wie S.66; zusätzlich Prozessregel: Außenlichtberechnung, Gelände-/Fassadenhöhen und Freihaltung sind eigene offene Nachweise, nicht aus dem Symbolbestand ableitbar

## S. 68 · SG — F-SG-14 Einzelbezüge (SG-006, SG-007)
**Bereich:** Nordfassade des Gymnastiksaals, westlicher und mittlerer Abschnitt
**Bild:** Zwei Einzelbezüge (Typ P): SG-006 an der westlichen Nordfassade nahe dem Windfang, SG-007 als mittlere der drei Nordfassadenleuchten. Details zeigen orange eingekreiste grün-gelbe Rechtecke direkt an der schraffierten Außenwand. Beide bleiben Bestandsdrehung 0°; ein benutzbarer Außenfluchtweg ist ausdrücklich nicht belegt und die Leuchten haben keine Rettungszeichenfunktion.
> „Eine konkrete Ankunft auf einem äußeren Weg ist hier noch nicht festgelegt; die beleuchtende Leuchte hat keine Rettungszeichenfunktion.“
> „Es fehlt der Nachweis einer begehbaren, freizuhaltenden Verbindung und der tatsächlichen Beleuchtung zwischen den Fassadenpunkten.“
**Leuchten im Bild:** SG-006 antipanik, SG-007 antipanik
**Linien:** keine; orange Detailkreise an der Fassadenschraffur
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 36BA5, 36BC2 · Kandidaten der Nordreihe (rot 0°, westlichster + mittlerer Punkt); Frame-Zuordnung ? (siehe S.66).
**Bewertung:** neu → aussenleuchten_kein_wegnachweis — Einzelbeleg: auch zwischen benachbarten Fassadenleuchten gilt keine implizite Wegverbindung

## S. 69 · SG — F-SG-14 Einzelbezüge (SG-008, SG-025)
**Bereich:** Nordöstliches Fassadeneck und schräge Ostfassade des Gymnastiksaals
**Bild:** Zwei Einzelbezüge (Typ P): SG-008 am nordöstlichen Fassadeneck (Bestandsdrehung 0°) und SG-025 an der schrägen Ostfassade mit abweichender Bestandsrotation 279,211°. Details zeigen die orange eingekreisten Rechtecke an den schraffierten Außenwänden. Kernaussage: aus zwei benachbarten Fassadenleuchten folgt keine freigegebene Eckumgehung.
> „Aus zwei benachbarten Fassadenleuchten folgt keine freigegebene Eckumgehung; Gelände, Hindernisse und Lichtüberdeckung sind offen.“
> „Andere Fassadenseite und Achse als die Nordreihe SG-006/007/008; nicht als deren Richtungsschild zu verstehen.“
**Leuchten im Bild:** SG-008 antipanik, SG-025 antipanik
**Linien:** keine; orange Detailkreise
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 36BDF, 36BFC · 36BDF (rot 0°, östlichster Punkt der Nordreihe) und 36BFC (rot 279.21°) passen zu SG-008/SG-025; Frame-Zuordnung ? (siehe S.66).
**Bewertung:** neu → aussenleuchten_kein_wegnachweis — Einzelbeleg Eckumgehung: benachbarte Fassadenleuchten um eine Gebäudeecke begründen keinen Eck-Fluchtweg

## S. 70 · SG — F-SG-14 Einzelbezüge (SG-043)
**Bereich:** Südfassade des Gymnastiksaals, östlich des Saalausgangs
**Bild:** Einzelbezug (Typ P) zu SG-043: orange eingekreistes Rechteck an der südlichen Außenwandschraffur, Bestandsdrehung 9,21103°. Die Leuchte betrifft den äußeren Tür- und Fassadenbereich beim südlichen Saalausgang; ob der Fluchtweg vom Ausgang tatsächlich an ihr vorbeiführt, bleibt offen; sie ist ausdrücklich kein Wegweiser.
> „Ankunft aus dem Saal ist nur bei bestätigter äußerer Wegführung zuzuordnen; die beleuchtende Leuchte ist kein Wegweiser.“
> „Ob der Weg vom südlichen Ausgang tatsächlich an dieser Leuchte vorbeiführt sowie Gelände und Lichtverteilung bleiben offen.“
**Leuchten im Bild:** SG-043 antipanik
**Linien:** keine; orange Detailkreis
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 36C19 · 36C19 (RIVO_Antipanik0, rot 9.21°) einziger Kandidat mit dieser Rotation; Frame-Zuordnung ? (siehe S.66).
**Bewertung:** neu → aussenleuchten_kein_wegnachweis — Einzelbeleg Südfassade: Leuchte am Außenbereich des Ausgangs ersetzt nicht die Festlegung des Außenwegs (EN 1838 4.1.2, Außenweg bis sicherer Bereich)

## S. 71 · SG — F-SG-15 AR Lehrmittel / AR FM am Südgang
**Bereich:** Tür AR Lehrmittel/AR FM (UG.31/UG.38-Zone) in den nördlichen Abschnitt des Südgangs
**Bild:** Fallseite A–D mit Planausschnitt: orange gerahmte Türstelle des AR Lehrmittel zum Südgang mit grünem RZ SG-050 raumseitig an der Tür; grün gestrichelter Weg von P1 aus dem Raum ostwärts durch die Tür und dann nordwärts den Gang hinauf Richtung Knoten/Windfang bei TH 3; im Norden und rechts weitere unbeschriftete grüne Notleuchten (Gang-RZ). Bei 277° blickt die Vorderseite von SG-050 nach Westen in den Raum; der Längsgang sieht überwiegend die Seitenansicht.
> „Bei 277° blickt die Vorderseite ungefähr nach Westen in den Raum. Der Längsgang ist für dieses Zeichen überwiegend eine Seitenansicht und keine zweite vollwertige Leserichtung.“
> „SG-050 kennzeichnet die Tür aus AR Lehrmittel / AR FM in den nördlichen Abschnitt des Südgangs.“
**Leuchten im Bild:** SG-050 down
**Personen:** P1 aus AR Lehrmittel / AR FM (von Westen)
**Linien:** grün gestrichelte Weginterpretation Raum→Tür→Gang nordwärts; orange Rahmen um die Türstelle
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34DC9 · 34DC9 = RIVO_ARR_down0, rot 277°, nahe Kennung SG-050 (8C39C, Abstand ca. 390 mm) — Position und Drehung wie im PDF.
**Bewertung:** bestaetigt:NB-R01

## S. 72 · SG — F-SG-15 AR Lehrmittel / AR FM am Südgang (E–J)
**Bereich:** Tür AR Lehrmittel/AR FM am Südgang — Begründung, CAD-Zuordnung, Normbezug
**Bild:** Reine Textseite E–J: SG-050 STANDARD_RZ_PU→RIVO_ARR_down0, Drehung 277°, Status ersetzt. Normbezüge A01 (EN 1838 4.1.1) und A09 (5.5 Erkennungsweite l=z×h, z=100/200, reale Zeichenhöhe statt CAD-Symbolgröße). G warnt, dass eine Verschiebung auf die gegenüberliegende Gangwand Türzuordnung und Erkennungsweite ändert. J trennt raumbezogene und gangbezogene Zeichen an derselben Tür.
> „Ein raumbezogenes Zeichen und ein gangbezogenes Zeichen erfüllen auch an derselben Tür nicht automatisch dieselbe Aufgabe.“
> „Erkennungsweite l = z × h; z=100 für extern beleuchtete, z=200 für hinterleuchtete Zeichen. h ist die reale Zeichenhöhe“
> „Eine Verschiebung auf die gegenüberliegende Gangwand könnte die Zuordnung zur Tür und die Erkennungsweite ändern.“
**Leuchten im Bild:** SG-050 down
**Linien:** keine (Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34DC9 · Symboltausch-Angabe (RIVO_ARR_down0, 277°) deckt sich mit dem DXF-Eintrag 34DC9.
**Bewertung:** bestaetigt:NB-R01

## S. 73 · SG — F-SG-15 Einzelbezüge — SG-050 Typ H
**Bereich:** Westrand Südgang / AR Lehrmittel-FM (Abstellraum)
**Bild:** Detailausschnitt mit orangem Kreis um SG-050 an der Tür des AR Lehrmittel/FM am westlichen Rand des Südgangs. Grünes down-RZ in der Türzone, Front annähernd nach Westen zum Raum; Personen kommen aus dem westlich anschließenden Abstellraum auf die Türfront zu und treten in den Gang. Kein Ersatz für die Gangrichtungszeichen; lokaler Raumzugang zwischen zentralem Knoten und südlicher Gangfolge.
> „Türzeichen des AR Lehrmittel/FM am westlichen Rand des Südgangs; Front annähernd nach Westen zum Raum.“
> „Personen kommen aus dem westlich anschließenden Abstellraum auf die Türfront zu und treten danach in den Gang.“
> „RIVO_ARR_down0; Blockrotation 277°. Zeichenfront im Plan: links (-X).“
**Leuchten im Bild:** SG-050 down
**Personen:** Abstellraum AR Lehrmittel/FM (westlich)
**Linien:** oranger Markierungskreis; keine Weg-/Sichtlinien im Detail
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34DC9, 8C39C · RIVO_ARR_down0 rot 277° im Inventar 389 mm neben Kennung 8C39C — deckt sich mit PDF-Angabe.
**Bewertung:** bestaetigt:NB-R01

## S. 74 · SG — F-SG-16 Südgang mit Garderobe Cluster 1
**Bereich:** langer Südgang entlang Garderobe Cluster 1 (UG.37/UG.36)
**Bild:** Übersicht des leicht schrägen Südgangs: drei beidseitige RZ (SG-052, SG-054, SG-057) in Folge im Gang, zwei Aufheller-Spots (SG-053, SG-056) in der westlichen Garderobenzone. Person P1 steht im Südgang, grün gestrichelte Weginterpretation läuft längs des Gangs nach Süden zum Quergang F-SG-17. Die Querung aus den Garderoben in den Gang wird mangels belegter Öffnung nicht eingezeichnet.
> „Die drei Zeichen sind um 97° gedreht; ihre Pfeile weisen entlang des leicht schrägen Gangs nach Süden.“
> „Die Fronten der beidseitigen Zeichen liegen ungefähr östlich und westlich. Sie eignen sich geometrisch für seitliche Ankünfte; eine Person, die bereits nach Süden läuft, sieht die Tafeln stärker von der Seite.“
> „Die konkrete Querung aus den Garderoben in den Gang ist anhand der überlagerten Bestandslinien nicht als freier Durchgang belegt und wird deshalb nicht eingezeichnet.“
**Leuchten im Bild:** SG-052 beidseitig, SG-053 aufheller, SG-054 beidseitig, SG-056 aufheller, SG-057 beidseitig
**Personen:** P1 bereits im Südgang (auch Garderoben UG.37/UG.36 und östliche Räume möglich)
**Linien:** grün gestrichelte Weginterpretation südwärts im Gang; beginnt innerhalb des belegbaren Gangs, keine Querung der Garderobenbegrenzung
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34FD6, 35030, 34FF4, 3504A, 35012 · 3× RIVO_ARR_bothsided0 rot 97° + 2× RIVO_Aufheller_Variante0 rot 0° nahe den Kennungen 8C39F/8C3A0/8C3A1/8C3A4/8C3A5 bestätigt.
**Bewertung:** bestaetigt:NB-R16

## S. 75 · SG — F-SG-16 Südgang mit Garderobe Cluster 1 — E-J
**Bereich:** Südgang / Garderobenbereiche UG.37 und UG.36
**Bild:** Begründungsseite ohne Planbild: Symboltausch-Liste (3× STANDARD_RZ_PLPR zu RIVO_ARR_bothsided0 bei 97°, 2× STANDARD_SPOT zu RIVO_Aufheller_Variante0 bei 0°), Normbezüge A01/A03/A04/A09 der ÖNORM EN 1838 und offene Nachweise (Sicht für Längsläufer, Fluchtzuordnung Nord/Süd, Lichtabdeckung Garderobe). J-Regel: Reihe beidseitiger Zeichen bedient seitliche Raumankünfte ohne durchgehende Frontallesbarkeit für den Längsweg.
> „Eine Reihe beidseitiger Zeichen kann seitliche Raumankünfte bedienen, ohne für den gesamten Längsweg frontal lesbar zu sein.“
> „SG-053/056 sind die beleuchtenden Positionen in den Garderobenbereichen UG.37/UG.36. Einbauten, Kleidung und die bauliche Begrenzung zum Gang können Licht und Sicht beeinflussen.“
> „Die Zeichen weiter in die Gangmitte zu setzen könnte Leseseiten und Kollisionsfreiheit verbessern, ist ohne Höhen-/Möblierungsprüfung aber keine ausgeführte Planänderung.“
**Leuchten im Bild:** SG-052 beidseitig, SG-053 aufheller, SG-054 beidseitig, SG-056 aufheller, SG-057 beidseitig
**Linien:** keine (Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34FD6, 34FF4, 35012, 35030, 3504A · Symboltausch-Angaben (bothsided0 97°, Aufheller_Variante0 0°) decken sich mit dem Inventar.
**Bewertung:** neu → Schul-Garderobenzone: Eine REIHE beidseitiger RZ längs des Gangs bedient seitliche Raumankünfte (Fronten quer zum Gang); lückenlose Frontalsicht für Längsläufer wird NICHT behauptet und nicht gefordert — nuanciert NB-R07 (Folgeleuchten) und generalisiert NB-R16 von Einzelknoten auf eine Gangfolge; Garderoben-Aufheller decken die Raumzone, freie Querung zum Gang bleibt nachweispflichtig.

## S. 76 · SG — F-SG-16 Einzelbezüge — SG-052 Typ H / SG-053 Typ B
**Bereich:** Nordteil Südgang / Garderobe Cluster 1 UG.37
**Bild:** Zwei Detailausschnitte: SG-052 als nördliches beidseitiges RZ der Südgangfolge (bothsided0, 97°, Fronten Ost/West, Pfeil südwärts) und SG-053 als runder richtungsfreier Aufheller-Spot in der Garderobe UG.37 (Blockrotation 0°). Ankünfte aus Ost/West sehen je eine Front; Längsläufer sehen das Zeichen seitlich. Für SG-053 sind Gangzugang, Garderobenaufstellung und Sicht auf SG-052/054 nicht belegt.
> „Ankünfte aus östlichen oder westlichen Anschlüssen können je eine Front sehen; eine bereits südwärts gehende Person sieht das Zeichen dagegen eher seitlich.“
> „Runde, richtungsfreie AP-Spot-Darstellung; Produkt-/Montagedaten bleiben in Attributen erhalten. Eine Lichtachse ist keine Fluchtrichtungsangabe.“
**Leuchten im Bild:** SG-052 beidseitig, SG-053 aufheller
**Personen:** östliche/westliche Anschlüsse bzw. Garderobenbereich UG.37
**Linien:** orange Markierungskreise; keine Weg-/Sichtlinien
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34FD6, 35030 · bothsided0 97° (300 mm neben Kennung 8C39F) und Aufheller_Variante0 0° (265 mm neben 8C3A0) bestätigt.
**Bewertung:** bestaetigt:NB-R16

## S. 77 · SG — F-SG-16 Einzelbezüge — SG-054 Typ H / SG-056 Typ B
**Bereich:** Mittelteil Südgang / Garderobe Cluster 1 UG.36
**Bild:** Zwei Detailausschnitte: SG-054 als mittleres beidseitiges RZ im schrägen Südgang (bothsided0, 97°, Pfeile südwärts, Fronten Ost/West) zwischen SG-052 und SG-057; SG-056 als südlicher Aufheller-Spot in der Garderobe UG.36 (0°, richtungsfrei). Die Reihenfolge allein weist keine Sichtkontinuität nach; eine seitliche Querung aus der Garderobe wird ohne belegte Öffnung nicht angenommen.
> „Mittlerer Orientierungspunkt zwischen SG-052 und SG-057, kein Nachweis der Sichtkontinuität allein durch die Reihenfolge.“
> „Personen halten sich im südlichen Garderobenbereich UG.36 auf. Eine seitliche Querung zum Südgang wird ohne belegte Öffnung nicht angenommen.“
**Leuchten im Bild:** SG-054 beidseitig, SG-056 aufheller
**Personen:** Ankunft aus Osten oder Westen bzw. Garderobenbereich UG.36
**Linien:** orange Markierungskreise; keine Weg-/Sichtlinien
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34FF4, 3504A · bothsided0 97° (300 mm neben Kennung 8C3A1) und Aufheller_Variante0 0° (228 mm neben 8C3A4) bestätigt.
**Bewertung:** bestaetigt:NB-R16

## S. 78 · SG — F-SG-16 Einzelbezüge — SG-057 Typ H
**Bereich:** Südende Südgang vor dem Quergangknoten
**Bild:** Detailausschnitt: SG-057 als südlichstes beidseitiges RZ der Südgangfolge (bothsided0, 97°) vor dem Übergang zum südlichen Quergang. Letzter Orientierungspunkt vor dem Knoten SG-060 und dem westlichen Ausgang SG-059; seitliche Ankunft trifft eine Ost-/Westfront, Personen von Norden sehen die Tafel stärker seitlich.
> „Letzter Orientierungspunkt vor dem Quergangknoten SG-060 und dem westlichen Ausgang SG-059.“
> „Sicht beim Übergang vom Längsgang zum Quergang und die verbindliche Richtungszuweisung müssen ausdrücklich geprüft werden.“
**Leuchten im Bild:** SG-057 beidseitig
**Personen:** von Norden längs des Südgangs bzw. seitliche Ankunft
**Linien:** oranger Markierungskreis; keine Weg-/Sichtlinien
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 35012 · bothsided0 97° (300 mm neben Kennung 8C3A5) bestätigt.
**Bewertung:** bestaetigt:NB-R16

## S. 79 · SG — F-SG-17 Südlicher Quergang, Ausgang und Übergang TH 2
**Bereich:** südlicher Quergang zwischen Außenausgang (West) und Bestands-TH 2 (Ost)
**Bild:** Übersicht des südlichen Quergangs: Außentür SG-059 mit Tür-RZ (Front nach Osten) und außenliegendem AP-Punkt SG-058 links, beidseitiges Knoten-RZ SG-060 (7°, Pfeile nach Westen) in der Gangmitte, Aufheller-Spot SG-061 im östlichen Abschnitt Richtung TH 2. Person P1 kommt aus der Garderobe von Norden, grün gestrichelte Weginterpretation läuft westwärts durch die Tür ins Freie; für die östliche Weiterführung nach TH 2 wird keine neue Zeichenfolge erfunden.
> „Die westliche Führung endet an der Außentür SG-059; SG-058 liegt außen. SG-060 zeigt bei 7° ungefähr nach Westen und kann die nördliche Ankunft zum Ausgang lenken.“
> „Für die östliche Weiterführung nach TH 2 wird keine zusätzliche neue Zeichenfolge erfunden.“
> „SG-060 hat Fronten nach Norden/Süden; die Ankunft von Osten ist seitlich. Diese unterschiedliche Abdeckung ist bei der Abstimmung mit TH 2 wichtig.“
**Leuchten im Bild:** SG-058 antipanik, SG-059 down, SG-060 beidseitig, SG-061 aufheller
**Personen:** P1 aus der Garderobe von Norden; weitere aus dem bestehenden südlichen Gebäudeteil von Osten
**Linien:** grün gestrichelte Weginterpretation von P1 nach Süden und westwärts durch die Tür ins Freie; oranges Rechteck um die Ausgangszone SG-058/059
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34FB9, 34F9C, 8C3A6, 8C3A9 · SG-059 (down0 97°, Handle 34FB9) und SG-060 (bothsided0 7°, 34F9C) bestätigt; für SG-058 (Antipanik0 277°) und SG-061 (Aufheller 6.17519°) findet das Inventar-JSON keinen Block nahe der Kennung — Leuchten-Handles ?, nur Kennungs-Handles angegeben.
**Bewertung:** bestaetigt:NB-R25

## S. 80 · SG — F-SG-17 Südlicher Quergang, Ausgang und Übergang TH 2 — E-J
**Bereich:** südlicher Quergang / Außenausgang / TH-2-Anschluss
**Bild:** Begründungsseite ohne Planbild: Symboltausch-Liste (SG-058 STANDARD_SL zu RIVO_Antipanik0 277°; SG-059 STANDARD_RZ_PU zu RIVO_ARR_down0 97°; SG-060 STANDARD_RZ_PLPR zu RIVO_ARR_bothsided0 7°; SG-061 STANDARD_SPOT_SL_DA zu RIVO_Aufheller_Variante0 6.17519°), Normbezüge A01/A02/A03. J-Regel: letzte Richtungsentscheidung, Türdurchgang und Beleuchtung dahinter als zusammenhängende Folge prüfen; offene Nachweise Außentreppe, Weg zum sicheren Bereich, TH-2-Anschluss.
> „Die letzte Richtungsentscheidung, der Türdurchgang und die Beleuchtung dahinter müssen als zusammenhängende Folge geprüft werden.“
> „Ein beidseitiges Zeichen alleine wäre kein Ersatz für das konkrete Ausgangszeichen, wenn die Außentür aus einer Ankunft verdeckt ist.“
> „A02 [...] der Außenweg vom letzten Ausgang bis zum sicheren Bereich sind gezielt zu beleuchten.“
**Leuchten im Bild:** SG-058 antipanik, SG-059 down, SG-060 beidseitig, SG-061 aufheller
**Linien:** keine (Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34FB9, 34F9C · Drehungen 97°/7° der auffindbaren Blöcke stimmen; SG-058/SG-061-Blöcke im Inventar-JSON nicht nahe der Kennung auffindbar (?).
**Bewertung:** bestaetigt:NB-R12

## S. 81 · SG — F-SG-17 Einzelbezüge — SG-058 Typ N / SG-059 Typ I
**Bereich:** westlicher Außenausgang des südlichen Quergangs
**Bild:** Zwei Detailausschnitte: SG-058 als beleuchtende AP-Position AUSSEN westlich des Quergangausgangs (RIVO_Antipanik0, 277°, kein RZ, keine lesbare Schildfront) und SG-059 als Tür-RZ an der westlichen Außentür (down0, 97°, Front nach Osten in den Quergang). Personen aus dem Quergang kommen von Osten auf die Türfront zu und treten ins Freie; Gelände, Niveauwechsel und Außenlichtberechnung bleiben offen.
> „Beleuchtende AP-Position außen westlich des südlichen Quergangausgangs.“
> „Personen kommen durch die Tür bei SG-059 ins Freie; SG-058 ist kein RZ und hat keine lesbare Schildfront.“
> „Zeichen an der westlichen Außentür des südlichen Quergangs; Front annähernd nach Osten.“
**Leuchten im Bild:** SG-058 antipanik, SG-059 down
**Personen:** aus dem Quergang von Osten
**Linien:** orange Markierungskreise; keine Weg-/Sichtlinien
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34FB9, 8C3A6 · SG-059 down0 97° (283 mm neben Kennung 8C3A7) bestätigt; SG-058-Antipanik-Block (277°) im Inventar-JSON nicht auffindbar (?).
**Bewertung:** bestaetigt:NB-R01

## S. 82 · SG — F-SG-17 Einzelbezüge — SG-060 Typ I / SG-061 Typ E
**Bereich:** Knoten Südgang/Quergang und östlicher TH-2-Anschluss
**Bild:** Zwei Detailausschnitte: SG-060 als beidseitiges RZ am Knoten von Südgang und südlichem Quergang (bothsided0, 7°, Fronten Nord/Süd, Pfeile nach Westen zur Tür SG-059) und SG-061 als Bestands-SL-DA-Spot im östlichen Quergang Richtung TH 2, nach Auftraggeber-Formregel als RIVO_Aufheller_Variante0 mit unveränderter Drehung 6.17519°. Ankunft aus TH 2 trifft SG-060 seitlich; zwei Fronten bestätigen keine Lesbarkeit von Osten. Eine Leuchtenachse ist kein Rettungszeichenpfeil; die schwarze Bestandsachse entfällt im RIVO-Block.
> „Die Person aus TH 2 benötigt eine eigene Sichtbetrachtung; zwei Fronten bestätigen keine Lesbarkeit von Osten.“
> „Bestandsdrehung 6.17519°, neue Blockdrehung 6.17519°; eine Leuchtenachse ist kein Rettungszeichenpfeil.“
> „Einziger erfasster Lichtpunkt dieser östlichen Anschlussgruppe; er beweist keine vollständige Leuchtenfolge in TH 2 oder im Bestandsflügel.“
**Leuchten im Bild:** SG-060 beidseitig, SG-061 aufheller
**Personen:** aus dem nördlichen Südgang bzw. aus dem Bestands-/TH-2-Anschluss von Osten
**Linien:** orange Markierungskreise; keine Weg-/Sichtlinien
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34F9C, 8C3A9 · SG-060 bothsided0 7° (483 mm neben Kennung 8C3A8) bestätigt; SG-061-Aufheller-Block (6.17519°) im Inventar-JSON nicht nahe der Kennung auffindbar (?).
**Bewertung:** bestaetigt:NB-R16

## S. 83 · SG — F-SG-18 Zwei FLAP-SL an der östlichen Bestandsfassade
**Bereich:** östliche Fassade des Bestandsflügels bei Bewegungs-/Werkbereichen (UG.11/UG.09)
**Bild:** Übersicht der östlichen Bestandsfassade mit zwei rechteckigen gelb-grünen FLAP-Leuchten SG-051 und SG-055 an verschiedenen Fassadenabschnitten. Keine Personen, keine grüne Weglinie: aus der bloßen Nähe zur Fassade folgt weder eine Türfunktion noch ein begehbarer äußerer Fluchtweg; eine äußere Verbindung zwischen SG-051 und SG-055 wird mangels Beleg nicht eingezeichnet. Beide Objekte sind SL-Leuchten ohne Piktogramm, Front-/Rückseitenbetrachtung ist nicht anwendbar.
> „Die CAD-Symbole belegen dort Leuchtenpositionen. Aus der bloßen Nähe zur Fassade folgt weder eine Türfunktion noch ein begehbarer äußerer Fluchtweg.“
> „Eine äußere Verbindung zwischen SG-051 und SG-055 ist nicht hinreichend belegt und wird deshalb nicht eingezeichnet.“
> „Beide Objekte sind SL-Leuchten ohne Piktogramm; Vorder-/Rückseitenbetrachtung eines Rettungszeichens ist nicht anwendbar.“
**Leuchten im Bild:** SG-051 antipanik, SG-055 antipanik
**Linien:** keine Weg-/Sichtlinien (bewusst nicht eingezeichnet)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 36C36, 36C52 · 2× RIVO_Antipanik0 rot 0° je 614 mm neben Kennungen 8C39D/8C3A2 bestätigt.
**Bewertung:** bestaetigt:NB-R22

## S. 84 · SG — F-SG-18 Zwei FLAP-SL an der östlichen Bestandsfassade — E-J
**Bereich:** östliche Bestandsfassade / Bestandsleuchten-Dokumentation
**Bild:** Begründungsseite ohne Planbild: SG-051/SG-055 sind rechteckige FLAP-Bestandsleuchten, die nach Auftraggeber-Formregel als RIVO_Antipanik0 dargestellt werden (Rechteckform entscheidet den CAD-Block, nicht die reale SL-/AP-Produktfunktion); Drehung 0° erhalten, Höhe proportional 44,28 % kleiner (Aspektkonflikt). Normbezüge A02/A03; offen bleiben Fassadenmontage, beleuchteter Bereich, Leitung/Versorgung und Optikdaten. J-Regel: räumlich isolierte Bestandsleuchten müssen dokumentiert werden, auch ohne sichere Aufgabenerklärung.
> „Die Rechteckform entscheidet nach Auftraggeberregel den CAD-Block, nicht die reale SL-/AP-Produktfunktion.“
> „Problematisch wäre, aus der RIVO_Antipanik-Grafik einen freigegebenen Außenweg oder eine geprüfte Beleuchtungsstärke zwischen SG-051 und SG-055 abzuleiten.“
> „Eine räumlich isolierte Bestandsleuchte muss dokumentiert werden, auch wenn sich ihre Aufgabe aus den bereitgestellten Plänen nicht sicher erklären lässt.“
**Leuchten im Bild:** SG-051 antipanik, SG-055 antipanik
**Linien:** keine (Textseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 36C36, 36C52 · Bestandsdrehung 0° = Zieldrehung 0° im Inventar bestätigt; Aspektkonflikt (Höhe -44,28 %) nur aus PDF, geometrisch nicht gegengeprüft.
**Bewertung:** neu → Bestandsleuchten-Formregel + Dokumentationspflicht: rechteckige FLAP-/SL-Bestandssymbole werden nach Auftraggeber-Formregel dem RIVO_Antipanik-Block zugeordnet (Form entscheidet, Produktfunktion bleibt Attribut; Aspektkonflikt der Blockhöhe dokumentieren); räumlich isolierte Bestandsleuchten werden dokumentiert, ohne daraus Fluchtweg, Türfunktion oder Lichtnachweis abzuleiten.

## S. 85 · SG — F-SG-18 Einzelbezüge — SG-051 / SG-055 (TYP Q)
**Bereich:** östliche Bestandsfassade, zwei getrennte Fassadenabschnitte (außen)
**Bild:** Zwei Detail-Ausschnitte mit orangen Kreisen an der östlichen Bestandsfassade: SG-051 nördlicher, SG-055 südlicher Abschnitt, je eine rechteckige FLAP-SL-Leuchte (grün/orange Balkensymbol). Symboltausch STANDARD_SL → RIVO_Antipanik0, Bestands- und Blockdrehung 0°. Keine Wegbehauptung: weder Ankunft noch zugehörige Ausgangstür bestimmbar, keine begehbare Verbindung zwischen beiden belegt.
> „Eine Leuchtenachse ist kein Rettungszeichenpfeil.“
> „Proportionale Einpassung mit gleicher sichtbarer Breite, aber 44,28 % geringerer Höhe; keine Verzerrung.“
> „Montage, tatsächlich beleuchtete Fläche und zulässiger Außenweg müssen örtlich beziehungsweise aus Elektro-/Geländeunterlagen geklärt werden.“
**Leuchten im Bild:** SG-051 antipanik, SG-055 antipanik
**Linien:** orange Kreise = besprochene Position; keine Weg-/Sichtlinien (Detail ohne zusätzliche Wegbehauptung)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 8C39D, 36C36, 8C3A2, 36C52 · Kennungen SG-051/SG-055 (Layer RIVO_ERK_KENNUNG) je ~614 mm neben Leuchte; beide Leuchten Block RIVO_Antipanik0, rot 0° — deckt sich mit Seitentext
**Bewertung:** neu → aussen_sl_fassade: Außen-SL an der Fassade (FLAP-SL) als richtungsfreies Antipanik-/SL-Symbol führen; aus Leuchtenachse und Fassadenlage NIE Fluchtrichtung oder Außenweg ableiten — Außenweg-Nachweis bleibt offene Frage (Elektro-/Geländeunterlagen)

## S. 86 · EG — F-EG-01 E.41 Projektraum: Raumtür und Aufheller
**Bereich:** E.41 Projektraum nördlich des gemeinsamen Gangs, Gangtür zur MFU
**Bild:** Grundriss-Ausschnitt E.41 Projektraum mit rundem Aufheller EG-004 im Raum und Tür-RZ EG-016 an der südlichen Gangtür (orange umrahmt). Person P1 kommt aus der Raumnutzung, grün gestrichelte Weginterpretation durch die Tür in den Gang, türkise 2D-Sichtlinie zum Zeichen. Front des um 180° gedrehten einseitigen Zeichens zeigt nach Norden in den Raum.
> „Das einseitige Zeichen ist um 180° gedreht. Seine Front zeigt in den Raum, also nach Norden; vom Gang sieht man eher die Rückseite.“
> „Der grafische Abwärtspfeil bezeichnet hier den Türdurchgang und ist kein Höhenplan.“
> „Die Folge lautet Raum – bezeichnete Tür – Gang – TH 4 im Westen.“
**Leuchten im Bild:** EG-004 aufheller, EG-016 down
**Personen:** Raumnutzung E.41, zwischen den Möbeln zur Tür
**Linien:** grün gestrichelt = Weginterpretation Raum→Tür→Gang; türkis = angenommene 2D-Sicht; orange = markierte Tür
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49EF1, 20982, 49EFE, 20596 · EG-004 = RIVO_Aufheller_Variante rot 0°, EG-016 = RIVO_ARR_down rot 180° — Blöcke und Drehungen decken sich mit Seitentext
**Bewertung:** bestaetigt:NB-R01

## S. 87 · EG — F-EG-01 E.41 Projektraum: Raumtür und Aufheller (E–J)
**Bereich:** E.41 Projektraum, Begründung/CAD-Zuordnung/Normbezug
**Bild:** Textseite ohne Planausschnitt: Begründung der Türposition (Orientierung an konkreter Öffnung) und der Aufheller-Funktion (Beleuchtungsaufgabe im Raum), Symboltausch EG-004 STANDARD_SPOT→RIVO_Aufheller_Variante 0° und EG-016 STANDARD_RZ_PU→RIVO_ARR_down 180°, Normbezüge A01/A03/A04/A09 (EN 1838), offene Nachweise orange markiert.
> „Der Aufheller erfüllt die Beleuchtungsaufgabe im Raum. Seine mittige Lage beweist weder den Mindestwert am Boden noch die Ausleuchtung hinter Schränken.“
> „A09: Erkennungsweite l = z × h; z=100 für extern beleuchtete, z=200 für hinterleuchtete Zeichen; keine Umrechnung aus der grafischen Größe eines CAD-Symbols.“
> „Zuerst die Person im Raum und die reale Tür zuordnen, danach die Fortsetzung im Gang prüfen; Zeichen- und Beleuchtungsaufgabe bleiben getrennt.“
**Leuchten im Bild:** EG-004 aufheller, EG-016 down
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 20982, 20596 · Symboltausch-Angaben (Block + Drehung 0°/180°) stimmen mit Inventar überein
**Bewertung:** neu → schulraum_aufheller: Unterrichts-/Projektraum (Schule) erhält eigenen Raum-Aufheller (Beleuchtungsaufgabe) ZUSÄTZLICH zum Tür-RZ — anders als Wohnräume (dort kein Notlicht); Zeichen- und Beleuchtungsaufgabe strikt getrennt, mittige Lage ersetzt keinen Lux-Nachweis

## S. 88 · EG — F-EG-01 Einzelbezüge — EG-004 (Typ B) / EG-016 (Typ H)
**Bereich:** E.41 Projektraum: Rauminneres + südliche Tür
**Bild:** Zwei Detail-Ausschnitte mit orangen Kreisen: EG-004 runder grüner Aufheller mittig im Projektraum E41; EG-016 Tür-RZ an der südlichen Tür, Blockrotation 180°, Zeichenfront und grafischer Pfeil im Plan oben (+Y), Front nach Norden in den Raum. CAD-Konvention wird ausdrücklich von Personenbewegung und realem Piktogramm getrennt.
> „Runde, richtungsfreie AP-Spot-Darstellung; eine Lichtachse ist keine Fluchtrichtungsangabe.“
> „RIVO_ARR_down; Blockrotation 180°. Zeichenfront im Plan: oben (+Y). Dies beschreibt die CAD-Konvention; Personenbewegung und reales Piktogramm sind getrennt zu prüfen.“
> „Raummöblierung, Abschattung und ausreichendes Licht bis zur Südtür sind nicht nachgewiesen.“
**Leuchten im Bild:** EG-004 aufheller, EG-016 down
**Linien:** orange Kreise = besprochene Position; keine Weglinien in den Details
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 20982, 20596 · EG-004 RIVO_Aufheller_Variante 0°, EG-016 RIVO_ARR_down 180° — konsistent
**Bewertung:** bestaetigt:NB-R01

## S. 89 · EG — F-EG-02 E.40 Bildungsraum: südliche Ausgangstür
**Bereich:** E.40 Bildungsraum (6-18) nördlich des Gangs, Tür zum Gang
**Bild:** Grundriss-Ausschnitt E.40 Bildungsraum mit Aufheller EG-005 im Raum und Tür-RZ EG-017 an der südlichen Gangtür (orange umrahmt). Person P1 aus der Raumnutzung, grün gestrichelter Weg durch die Tür in den Gang, türkise Sichtlinie. Front des 180°-Zeichens nach Norden in den Raum; Folge Raum–Tür–Gang–TH 4 im Westen bis zum westlichen Ausgang im Sockelgeschoss.
> „Das einseitige Zeichen ist um 180° gedreht. Seine Front zeigt in den Raum, also nach Norden; vom Gang sieht man eher die Rückseite.“
> „Die endgültige Zuordnung jedes Raums zu einem Ausgang bleibt mit dem Fluchtwegkonzept abzugleichen.“
> „Eine Ankunft aus dem Gang ist eine andere Blickrichtung.“
**Leuchten im Bild:** EG-005 aufheller, EG-017 down
**Personen:** Raumnutzung E.40, zwischen den Möbeln zur Tür
**Linien:** grün gestrichelt = Weginterpretation; türkis = 2D-Sicht; orange = markierte Tür
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49EF2, 20742, 49EFF, 20578 · EG-005 = RIVO_Aufheller_Variante rot 0°, EG-017 = RIVO_ARR_down rot 180° — deckt sich mit Seitentext
**Bewertung:** bestaetigt:NB-R01

## S. 90 · EG — F-EG-02 E.40 Bildungsraum: südliche Ausgangstür (E–J)
**Bereich:** E.40 Bildungsraum, Begründung/CAD-Zuordnung/Normbezug
**Bild:** Textseite, baugleich zu S.87 für E.40: Türposition als Orientierungsanker, Aufheller als Beleuchtungsaufgabe im Raum, Symboltausch EG-005 STANDARD_SPOT→RIVO_Aufheller_Variante 0° und EG-017 STANDARD_RZ_PU→RIVO_ARR_down 180°, Normbezüge A01/A03/A04/A09, offene Nachweise (Notlichtberechnung, Möblierung, Montagehöhen, reale Zeichenhöhe, Sicht bei geöffnetem Türblatt).
> „Seine mittige Lage beweist weder den Mindestwert am Boden noch die Ausleuchtung hinter Schränken.“
> „Aus der Anzahl von zwei Symbolen wird keine vollständige Raumabdeckung abgeleitet.“
> „Zeichen- und Beleuchtungsaufgabe bleiben getrennt.“
**Leuchten im Bild:** EG-005 aufheller, EG-017 down
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 20742, 20578 · Symboltausch-Angaben stimmen mit Inventar überein
**Bewertung:** neu → schulraum_aufheller (2. Beleg): Muster Unterrichtsraum = 1 Aufheller im Raum + 1 Tür-RZ (Front in den Raum) wiederholt sich je Bildungsraum; Symbolanzahl allein belegt keine Raumabdeckung (Lux-Nachweis getrennt)

## S. 91 · EG — F-EG-02 Einzelbezüge — EG-005 (Typ B) / EG-017 (Typ H)
**Bereich:** E.40 Bildungsraum: Rauminneres + südliche Tür
**Bild:** Zwei Detail-Ausschnitte mit orangen Kreisen: EG-005 runder Aufheller im Bildungsraum E40 (Personen müssen die südliche Tür EG-017 erreichen und erkennen); EG-017 Tür-RZ mit Blockrotation 180°, Zeichenfront und Pfeil im Plan oben (+Y), Front nach Norden. Abgrenzung zur getrennten Projektraumtür EG-016.
> „Personen im Unterrichtsraum müssen die südliche Tür EG-017 erreichen und erkennen können.“
> „Eine Lichtachse ist keine Fluchtrichtungsangabe.“
> „Möblierung, geöffnete Tür und Blick zum nächsten Zeichen sind gesondert zu prüfen.“
**Leuchten im Bild:** EG-005 aufheller, EG-017 down
**Linien:** orange Kreise = besprochene Position
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 20742, 20578 · Blöcke/Drehungen konsistent (Aufheller 0°, ARR_down 180°)
**Bewertung:** bestaetigt:NB-R01

## S. 92 · EG — F-EG-03 Westgang: Zeichenfolge vor TH 4
**Bereich:** westlicher Gang zwischen MFU, Bildungsräumen E.38–E.40 und TH 4 / Lift 2
**Bild:** Grundriss des Westgangs: EG-025 (Tür-RZ, 90°, Front nach Osten) am MFU-Übergang zum schmaleren Gang, EG-024 (Aufheller) im Gang, EG-023 (beidseitiges Zeichen, 90°, Fronten Ost/West, Pfeile nach Süden) am Ende vor dem Abgang nach Süden in TH 4. Person P1 kommt aus der MFU von Osten, grün gestrichelte Wegkette entlang des Gangs mit Knick nach Süden zu TH 4, türkise Sichtlinie über die Gangflucht.
> „EG-025 weist den Türdurchgang nach Westen aus. Am Ende lenkt EG-023 mit seiner 90°-Drehung nach Süden in TH 4.“
> „EG-023 hat Fronten nach Osten und Westen und Pfeile nach Süden. Diese Kombination ist für die östliche Ankunft nachvollziehbar; nördliche Raumankünfte treffen eher auf die Kante des beidseitigen Zeichens.“
> „Die Hauptankunft kommt aus der MFU von Osten. Personen aus den Räumen kommen zusätzlich von Norden und Süden seitlich in den Gang.“
**Leuchten im Bild:** EG-023 beidseitig, EG-024 aufheller, EG-025 down
**Personen:** MFU von Osten (Hauptstrom); seitlich Raumankünfte von Norden und Süden
**Linien:** grün gestrichelt = Wegkette Gang→TH 4; türkis = 2D-Sicht entlang der Gangflucht; orange = markiertes Bauteil
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49F05, 20493, 49F06, 2092E, 49F07, 205B4 · EG-023 = RIVO_ARR_bothsided rot 90° (beidseitig_gruppe 1), EG-024 = RIVO_Aufheller_Variante 0°, EG-025 = RIVO_ARR_down rot 90° — alle drei decken sich mit Seitentext
**Bewertung:** bestaetigt:NB-R16

## S. 93 · EG — F-EG-03 Westgang: Zeichenfolge vor TH 4 (E–J)
**Bereich:** westlicher Gang vor TH 4, Begründung/Normbezug
**Bild:** Textseite: EG-024 als Gang-Aufheller beim Richtungswechsel (Bodenbeleuchtungs-Nachweis gefordert, Zeichen sind kein Ersatz), Symboltausch EG-023 STANDARD_RZ_PLPR→RIVO_ARR_bothsided 90°, EG-024 SPOT→Aufheller 0°, EG-025 RZ_PU→ARR_down 90°. Normbezüge A01/A02/A03/A09 sowie A17 (OVE E 8101: Dauerbetriebs-Kennzeichnung für Zeichen auf Fluchtwegen ab AC1:2020).
> „Der Richtungswechsel verlangt zusätzlich einen Nachweis der Bodenbeleuchtung; die zwei Zeichen sind dafür kein Ersatz.“
> „A02: Bei Richtungsänderungen und Kreuzungen muss die Sicherheitsleuchte beide Richtungen ausleuchten; dies ist keine pauschale Forderung nach einem bestimmten RZ-Block.“
> „Ein bloßer Austausch des beidseitigen Zeichens gegen ein ungedrehtes Linksschild würde die Richtungsentscheidung zur Stiege verlieren.“
> „Türpassage und Richtungswechsel können kurz aufeinanderfolgen und trotzdem zwei verschiedene Zeichenfunktionen sein.“
**Leuchten im Bild:** EG-023 beidseitig, EG-024 aufheller, EG-025 down
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 20493, 2092E, 205B4 · Symboltausch-Angaben (bothsided 90° / Aufheller 0° / down 90°) stimmen mit Inventar überein
**Bewertung:** bestaetigt:NB-R16

## S. 94 · EG — F-EG-03 Einzelbezüge — EG-023 (Typ H) / EG-024 (Typ B)
**Bereich:** westlicher Gang am TH-4-Anschluss
**Bild:** Zwei Detail-Ausschnitte: EG-023 beidseitiges Zeichen vor TH 4, Blockrotation 90°, Zeichenfront rechts (+X) und links (-X), grafischer Pfeil unten (-Y) — Ankünfte längs des Gangs treffen unterschiedliche Fronten und werden zur südlichen Stiegentür orientiert. EG-024 Aufheller im Hauptgang bei der TH-4-/MFU-Verbindung ohne Schildfrontbezug. Hinweis: im OG sitzt an der entsprechenden Stelle mit OG-029 ein anders ausgebildetes einseitiges Türzeichen.
> „Beidseitiges Zeichen im westlichen Gang am TH-4-Anschluss; Fronten Ost/West, Pfeile nach Süden.“
> „Türlage, Abstand zur Stiegentür und Blick bei geöffneter Tür sind pro Ankunft zu prüfen; EG und OG nicht identisch darstellen.“
> „Lichtabdeckung der einzelnen Türvorbereiche und reale Hindernisse im Gang sind nicht berechnet.“
**Leuchten im Bild:** EG-023 beidseitig, EG-024 aufheller
**Linien:** orange Kreise = besprochene Position
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 20493, 2092E · EG-023 bothsided 90° / EG-024 Aufheller 0° konsistent; OG-Gegenstelle OG-029 (einseitig) im OG-Inventar nachprüfbar
**Bewertung:** bestaetigt:NB-R16

## S. 95 · EG — F-EG-03 Einzelbezüge — EG-025 (Typ H)
**Bereich:** westlicher MFU-Ausgang in den Westgang
**Bild:** Detail-Ausschnitt mit orangem Kreis: EG-025 Türzeichen am westlichen Ausgang der MFU in den Gang, Blockrotation 90°, Zeichenfront und grafischer Pfeil im Plan rechts (+X), Front nach Osten frontal zum ankommenden MFU-Strom. Markiert den Raum-/Gangübergang vor EG-023; EG-024 beleuchtet den Bereich dazwischen.
> „Personen aus der MFU kommen von Osten auf die Türfront zu und müssen sich nach dem Durchgang zur Stiege neu orientieren.“
> „Sicht aus der MFU und auf EG-023 nach dem Austritt, abhängig vom Türblatt, ist noch zu bestätigen.“
**Leuchten im Bild:** EG-025 down
**Linien:** orange Kreis = besprochene Position
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49F07, 205B4 · EG-025 = RIVO_ARR_down rot 90°, Front +X — deckt sich mit Seitentext
**Bewertung:** bestaetigt:NB-R07

## S. 96 · EG — F-EG-04 TH 4: Eintritt, zwei Läufe und Zwischenpodest
**Bereich:** TH 4 am westlichen Kopf mit Lift 2 daneben
**Bild:** Grundriss TH 4 mit zwei Stiegenläufen und Treppenauge: EG-032 (Aufheller) am oberen Zugangspodest beim TH-4-Eintritt, EG-041 (Richtungs-RZ, 90°, weist nach Süden, Front nach Osten) am oberen Lauf, EG-045 (Richtungs-RZ, 269,007°, weist ungefähr nach Norden, Front nach Westen) am unteren Podest — gegenüberliegende Laufrichtungen. Lift 2 samt Tür und Schacht ist orange eingerahmt, damit er nicht mit dem Treppenzugang verwechselt wird; Ankunft aus dem Gang von Norden.
> „Links daneben befindet sich Lift 2; seine Tür und der kleine Schacht sind eingerahmt, damit er nicht mit dem Treppenzugang verwechselt wird.“
> „Der Aufzug ist im vorliegenden Material nicht als Evakuierungsaufzug nachgewiesen.“
> „Der genaue Höhenwechsel wird als Schnitt-/Vor-Ort-Prüfung behandelt; keine Linie überbrückt das Treppenauge.“
> „Die unterschiedliche Blickseite passt zu gegenüberliegenden Laufrichtungen an den Podesten; sie belegt allein noch nicht die Höhenfolge.“
**Leuchten im Bild:** EG-032 aufheller, EG-041 left, EG-045 left
**Linien:** orange Rahmen = Lift 2 (markiertes Bauteil); keine Linie über das Treppenauge
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49F0F, 20948, 49F1A, 20A11, 49F1E, 43561 · EG-032 = RIVO_Aufheller_Variante 0°, EG-041 = RIVO_ARR_left rot 90°, EG-045 = RIVO_ARR_left rot 269,01° — Rotationen decken sich exakt mit Seitentext (269,007°)
**Bewertung:** bestaetigt:NB-R27

## S. 97 · EG — F-EG-04 TH 4: Eintritt, zwei Läufe und Zwischenpodest — Begründung/Normbezug
**Bereich:** TH 4 (westliches Stiegenhaus), Eintritts-/Podestbereich
**Bild:** Reine Textseite (Abschnitte E-J) ohne Planausschnitt. Begründet den Bestands-Spot EG-032 (ECO SPOT AP DA E -> RIVO_Aufheller_Variante) am Übergang Gang->Stiege plus die Richtungszeichen EG-041 (90°) und EG-045 (269.007°). Normbezug A01/A02/A03/A09; offene Nachweise Höhenschnitt, Stufen, Handlaufabschattung, Lichtdaten.
> „Bei Stiegen zuerst Podeste und Laufkanten lesen. Architektur-Aufwärtspfeile dürfen nicht ungeprüft als Fluchtpfeile verwendet werden.“
> „Ein einziges Zeichen am Gang würde die Richtungsumkehr am unteren Podest nicht erklären. Ein Weg über die Mitte wäre trotz kürzerer Planlinie unzulässig.“
> „Die geringe Schrägstellung von EG-045 wurde bewusst erhalten.“
**Leuchten im Bild:** EG-032 aufheller, EG-041 left, EG-045 left
**Linien:** keine (Textseite); orange Hinweistexte in Abschnitt I
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Kennungen EG-032/041/045 aus Seitentext
**Bewertung:** bestaetigt:NB-R04

## S. 98 · EG — F-EG-04 Einzelbezüge — EG-032 (Typ F) und EG-041 (Typ I)
**Bereich:** TH 4, Eintritts-/Podestbereich und westlicher Stiegenabschnitt
**Bild:** Zwei DXF-Detailausschnitte mit orangem Kreis um die besprochene Position. Oben EG-032: Aufheller-Kreissymbol am TH-4-Podest neben der Raumbeschriftung TH 4 (Raumcode 4.2.2), links Lift 2, rechts oben ein grünes Tür-RZ. Unten EG-041: grünes RZ mit Abwärtspfeil an der westlichen Stiegenhauswand über dem Treppenlauf (Beschriftungen F.EG.28, RPH 66/FPH 70).
> „Personen kommen vom westlichen Gang in das Stiegenhaus und benötigen Licht am realen Podest.“
> „Bestandsdrehung 0°, neue Blockdrehung 0°; eine Leuchtenachse ist kein Rettungszeichenpfeil.“
> „RIVO_ARR_left; Blockrotation 90°. Zeichenfront im Plan: rechts (+X). Grafischer Pfeil im Plan: unten (-Y).“
> „Konkrete Geschossherkunft und Stufenfolge sind ohne vollständigen Schnitt nicht sicher; keine Linie durch das Treppenauge ziehen.“
**Leuchten im Bild:** EG-032 aufheller, EG-041 left
**Personen:** westlicher Gang
**Linien:** orange Markierungskreise um EG-032 und EG-041; keine Weglinien
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Rotation 90° und Front +X aus Seitentext
**Bewertung:** bestaetigt:NB-R07

## S. 99 · EG — F-EG-04 Einzelbezüge — EG-045 (Typ I)
**Bereich:** TH 4, südlicher Wendebereich (Wendepodest)
**Bild:** Ein DXF-Detail: grünes RZ EG-045 mit orangem Markierungskreis am südlichen Wendepodest von TH 4, über dem Lauf mit Architekten-Abwärtspfeil; rechts unten Wandaufbau-Schraffur und Beschriftungen RPH 66/FPH 70, AL-Koten. Front annähernd nach Westen (-X), grafischer Pfeil nach oben (+Y), Blockrotation exakt 269.007°.
> „Anderer Podestblick als EG-041; die 269,007-Grad-Bestandsdrehung ist keine pauschal auf 270 Grad zu normalisierende Angabe.“
> „RIVO_ARR_left; Blockrotation 269.007°. Zeichenfront im Plan: links (-X). Grafischer Pfeil im Plan: oben (+Y).“
> „Montagesituation, Niveau und Sicht nach der Wende sind zu prüfen; aus zwei Zeichen folgt keine bestätigte direkte Stufenbeleuchtung.“
**Leuchten im Bild:** EG-045 left
**Personen:** westlicher Podestabschnitt
**Linien:** oranger Markierungskreis um EG-045; Architektur-Laufpfeil im Treppenlauf
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Bestandsdrehung 269.007° aus Seitentext
**Bewertung:** neu → Bestandsdrehungen beim Symboltausch exakt uebernehmen: krumme Winkel (269.007°) NICHT auf 90-Grad-Raster normalisieren; geringe Schraegstellung ist bewusste Bestandsinformation (ergaenzt NB-R11-Prinzip 'Rotation unveraendert' um den Tausch-Fall)

## S.100 · EG — F-EG-05 E.39 Bildungsraum am westlichen Stiegenhaus — A-D
**Bereich:** E.39 Bildungsraum (6-10), suedlich des gemeinsamen Gangs, an TH 4
**Bild:** Planausschnitt: Bildungsraum E.39 (Raumcode 1.2.1b) suedlich des Gangs (Raumcode 4.2.1). Tuer-RZ EG-033 (orange umrahmt) sitzt raumseitig in der Gangtuer, Front nach Sueden in den Raum; Person P1 mit gruen gestrichelter Weglinie laeuft von Sueden durch die Tuer nach Norden in den Gang. Runder Aufheller EG-042 mittig im Raum; links TH 4 mit Aufheller-Symbol, oben im Gang ein weiteres gruenes Symbol.
> „Das Rettungszeichen sitzt an der zugehörigen Gangtür; der runde Aufheller liegt innerhalb des Raums.“
> „Das einseitige Zeichen ist um 0° gedreht. Seine Front zeigt in den Raum, also nach Süden; vom Gang sieht man eher die Rückseite. Der grafische Abwärtspfeil bezeichnet hier den Türdurchgang und ist kein Höhenplan.“
> „Die Folge lautet Raum – bezeichnete Tür – Gang – TH 4 im Westen.“
**Leuchten im Bild:** EG-033 down, EG-042 aufheller
**Personen:** Raumnutzung E.39 (zwischen den Moebeln)
**Linien:** gruen gestrichelte Weginterpretation P1->Tuer->Gang; tuerkise angenommene 2D-Sicht; oranges Rechteck um EG-033
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Kennungen EG-033/042 aus Seitentext
**Bewertung:** bestaetigt:NB-R01

## S.101 · EG — F-EG-05 E.39 Bildungsraum — Begründung/Normbezug (E-J)
**Bereich:** E.39 Bildungsraum (6-10)
**Bild:** Reine Textseite. Symboltausch EG-033 STANDARD_RZ_PU->RIVO_ARR_down (0°) und EG-042 STANDARD_SPOT->RIVO_Aufheller_Variante (0°). Normbezug A01/A03/A04 (Antipanik 0,5 lx, 0,5-m-Randstreifen, Ud 1:40)/A09. Trennung von Zeichen- und Beleuchtungsaufgabe als uebertragbare Regel.
> „Die Türposition verknüpft die Orientierung mit einer konkreten Öffnung. Der Aufheller erfüllt die Beleuchtungsaufgabe im Raum. Seine mittige Lage beweist weder den Mindestwert am Boden noch die Ausleuchtung hinter Schränken.“
> „Zuerst die Person im Raum und die reale Tür zuordnen, danach die Fortsetzung im Gang prüfen; Zeichen- und Beleuchtungsaufgabe bleiben getrennt.“
> „A04 — ... Antipanik: mindestens 0,5 lx auf der freien Bodenfläche im Kernbereich; ein 0,5 m breiter Randstreifen wird nicht berücksichtigt.“
**Leuchten im Bild:** EG-033 down, EG-042 aufheller
**Linien:** keine (Textseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft
**Bewertung:** neu → Schul-Unterrichtsraum-Muster (Bildungsraum): je Klassenraum genau EIN raumseitiges Tuer-RZ (down, Front in den Raum, NB-R01) PLUS EIN Aufheller/AP mittig im Raum; Aufheller wirkt nur im eigenen Raum (keine Wirkung durch Trennwaende). Erweitert NB-R02: Unterrichtsraeume erhalten anders als Wohnungen eigene Raumbeleuchtung

## S.102 · EG — F-EG-05 Einzelbezüge — EG-033 (Typ H) und EG-042 (Typ B)
**Bereich:** E.39 Bildungsraum, Nordtuer und Rauminneres
**Bild:** Zwei DXF-Details mit orangen Markierungskreisen. Oben EG-033: gruenes down-RZ raumseitig in der Nordtuer von E.39, Tuerfluegel-Bogen sichtbar, Front nach Sueden. Unten EG-042: runder gruener Aufheller frei im Raum E.39 (Raumcode 1.2.1b), ohne Richtungsbezug.
> „Türzeichen am nördlichen Ausgang des Bildungsraums E39; Front nach Süden.“
> „RIVO_ARR_down; Blockrotation 0°. Zeichenfront im Plan: unten (-Y). Grafischer Pfeil im Plan: unten (-Y).“
> „Eigene Raumbeleuchtung des Paars EG-033/042; getrennt von EG-043/044 hinter eigenen Raumwänden.“
> „Runde, richtungsfreie AP-Spot-Darstellung; ... Eine Lichtachse ist keine Fluchtrichtungsangabe.“
**Leuchten im Bild:** EG-033 down, EG-042 aufheller
**Personen:** E.39 von Sueden
**Linien:** orange Markierungskreise; keine Weglinien
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft
**Bewertung:** bestaetigt:NB-R01

## S.103 · EG — F-EG-06 E.38 Bildungsraum an der MFU — A-D
**Bereich:** E.38 Bildungsraum (6-10), suedlich des gemeinsamen Gangs, mittlerer der drei Klassenraeume
**Bild:** Planausschnitt analog F-EG-05: Tuer-RZ EG-034 (orange umrahmt) raumseitig in der Nordtuer von E.38, Front nach Sueden; Person P1 mit gruen gestrichelter Weglinie von Sueden zur Tuer und in den Gang. Runder Aufheller EG-043 im Raum; links oben ein weiteres Tuer-RZ mit Massketten 160/210.
> „Das Rettungszeichen sitzt an der zugehörigen Gangtür; der runde Aufheller liegt innerhalb des Raums.“
> „Die Person kommt aus der Raumnutzung, bewegt sich zwischen den tatsächlichen Möbeln zur Tür und tritt erst danach in den Gang. Eine Ankunft aus dem Gang ist eine andere Blickrichtung.“
> „Der grafische Abwärtspfeil bezeichnet hier den Türdurchgang und ist kein Höhenplan.“
**Leuchten im Bild:** EG-034 down, EG-043 aufheller
**Personen:** Raumnutzung E.38
**Linien:** gruen gestrichelte Weginterpretation; tuerkise 2D-Sicht; oranges Rechteck um EG-034
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft
**Bewertung:** bestaetigt:NB-R01

## S.104 · EG — F-EG-06 E.38 Bildungsraum — Begründung/Normbezug (E-J)
**Bereich:** E.38 Bildungsraum (6-10)
**Bild:** Reine Textseite, wortgleiches Muster zu S.101 fuer E.38: EG-034 STANDARD_RZ_PU->RIVO_ARR_down (0°), EG-043 STANDARD_SPOT->RIVO_Aufheller_Variante (0°). Normbezug A01/A03/A04/A09; offene Nachweise Notlichtberechnung, Moeblierung, Montagehoehen, reale Zeichenhoehe, Sicht bei geoeffnetem Tuerblatt.
> „Die Türposition verknüpft die Orientierung mit einer konkreten Öffnung. Der Aufheller erfüllt die Beleuchtungsaufgabe im Raum.“
> „Aus der Anzahl von zwei Symbolen wird keine vollständige Raumabdeckung abgeleitet.“
> „Zeichen- und Beleuchtungsaufgabe bleiben getrennt.“
**Leuchten im Bild:** EG-034 down, EG-043 aufheller
**Linien:** keine (Textseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft
**Bewertung:** bestaetigt:NB-R01

## S.105 · EG — F-EG-06 Einzelbezüge — EG-034 (Typ H) und EG-043 (Typ B)
**Bereich:** E.38 Bildungsraum, Nordtuer und Rauminneres
**Bild:** Zwei DXF-Details mit orangen Markierungskreisen. Oben EG-034: gruenes down-RZ raumseitig in der Nordtuer von E.38 mit Tuerfluegel-Bogen; links oben ein weiteres gruenes Tuer-RZ (160/210). Unten EG-043: runder Aufheller frei im Raum E.37/E.38-Bereich ohne Richtungsbezug.
> „Türzeichen am nördlichen Ausgang des Bildungsraums E38; Front nach Süden.“
> „Mittlerer der drei südlichen Bildungsraumzugänge; EG-043 ist seine eigene Raumbeleuchtung.“
> „Mittlerer Lichtpunkt der drei Raumgruppen; die Nachbarleuchten gehören jeweils zu getrennten Räumen.“
**Leuchten im Bild:** EG-034 down, EG-043 aufheller
**Personen:** E.38 von innen
**Linien:** orange Markierungskreise; keine Weglinien
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft
**Bewertung:** bestaetigt:NB-R01

## S.106 · EG — F-EG-07 E.37 Bildungsraum am mittleren Gang — A-D
**Bereich:** E.37 Bildungsraum (6-10), suedlich des Gangs, oestlicher der drei Klassenraeume, neben Sozialraum E.33
**Bild:** Planausschnitt: Tuer-RZ EG-035 (orange umrahmt) raumseitig in der Nordtuer von E.37, Front nach Sueden; gruener Aufwaertspfeil der Weginterpretation durch die Tuer in den Gang, Person P1 mit tuerkiser Sichtlinie. Aufheller EG-044 im Raum E.37; rechts Sozialraum E.33 und oben rechts weitere gruene Tuer-RZ (160/210).
> „Das Rettungszeichen sitzt an der zugehörigen Gangtür; der runde Aufheller liegt innerhalb des Raums.“
> „Die Folge lautet Raum – bezeichnete Tür – Gang – zum mittleren Gang und weiter zur im Fluchtplan zugewiesenen Stiege.“
> „Die endgültige Zuordnung jedes Raums zu einem Ausgang bleibt mit dem Fluchtwegkonzept abzugleichen.“
**Leuchten im Bild:** EG-035 down, EG-044 aufheller
**Personen:** Raumnutzung E.37
**Linien:** gruen gestrichelte Weginterpretation mit Pfeil durch die Tuer; tuerkise 2D-Sicht; oranges Rechteck um EG-035
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft
**Bewertung:** bestaetigt:NB-R01

## S.107 · EG — F-EG-07 E.37 Bildungsraum — Begründung/Normbezug (E-J)
**Bereich:** E.37 Bildungsraum (6-10)
**Bild:** Reine Textseite, wortgleiches Muster zu S.101/104 fuer E.37: EG-035 STANDARD_RZ_PU->RIVO_ARR_down (0°), EG-044 STANDARD_SPOT->RIVO_Aufheller_Variante (0°). Normbezug A01/A03/A04/A09; gleiche offene Nachweise (Notlichtberechnung, Moeblierung, Montagehoehen, Zeichenhoehe, Tuerblatt-Sicht).
> „Seine mittige Lage beweist weder den Mindestwert am Boden noch die Ausleuchtung hinter Schränken.“
> „Eine Verlegung des Zeichens auf die Gangseite würde die Lesbarkeit beim Verlassen des Raums verändern.“
> „Zuerst die Person im Raum und die reale Tür zuordnen, danach die Fortsetzung im Gang prüfen.“
**Leuchten im Bild:** EG-035 down, EG-044 aufheller
**Linien:** keine (Textseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft
**Bewertung:** bestaetigt:NB-R01

## S.108 · EG — F-EG-07 Einzelbezüge — EG-035 (Typ H) und EG-044 (Typ B)
**Bereich:** E.37 Bildungsraum, Nordtuer und Rauminneres
**Bild:** Zwei DXF-Details mit orangen Markierungskreisen. Oben EG-035: gruenes down-RZ raumseitig in der Nordtuer von E.37 mit Tuerfluegel-Bogen, Wandschraffuren beidseitig. Unten EG-044: runder Aufheller im Raum E.37 (Raumcode 1.2.1b), richtungsfrei; Hinweis, dass er den benachbarten Sozialraum durch die Trennwand NICHT mitbeleuchtet.
> „Türzeichen am nördlichen Ausgang des Bildungsraums E37; Front nach Süden.“
> „Östlicher Lichtpunkt der Reihe; keine Beleuchtung des benachbarten Sozialraums durch die Trennwand anzunehmen.“
> „Eine Lichtachse ist keine Fluchtrichtungsangabe.“
**Leuchten im Bild:** EG-035 down, EG-044 aufheller
**Personen:** E.37 von innen
**Linien:** orange Markierungskreise; keine Weglinien
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft
**Bewertung:** bestaetigt:NB-R01

## S.109 · EG — F-EG-08 MFU: offene Fläche zwischen zwei Gangabschnitten
**Bereich:** MFU nördlich des Hauptgangs, zwischen westlichem Raumtrakt und E.36
**Bild:** Grundriss-Ausschnitt der großen offenen MFU mit dem einzelnen AP-Spot EG-010 (grüner runder Aufheller). Person P1 steht unter dem Spot, grün gestrichelte Weginterpretation führt nach Süden in den angrenzenden Gang (Raumcode 4.2.1.1). Tür-RZ-Symbole an den Rändern (E.36-Zugang rechts, Ausgang links unten).
> „EG-010 ist der einzelne erfasste AP-Spot innerhalb dieser offenen Fläche.“
> „Die lokale Fortsetzung führt aus der offenen MFU in den südlich angrenzenden Gang.“
> „EG-010 besitzt kein Rettungszeichen. Seine runde Darstellung hat keine lesbare Vorder- oder Rückseite und gibt keine Fluchtrichtung vor.“
**Leuchten im Bild:** EG-010 aufheller
**Personen:** Arbeits-/Aufenthaltsstellen der MFU und angrenzende Türen
**Linien:** grün gestrichelte Weginterpretation von P1 nach Süden in den Gang; Orange-Rahmen fehlt in diesem Ausschnitt
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 20796 · EG-010 = 20796 RIVO_Aufheller_Variante rot 0° (Label-Abstand 239 mm) — deckt sich mit PDF (Drehung 0°, Status ersetzt).
**Bewertung:** bestaetigt:NB-R23

## S.110 · EG — F-EG-08 MFU: offene Fläche zwischen zwei Gangabschnitten (E–J)
**Bereich:** MFU nördlich des Hauptgangs
**Bild:** Textseite E–J ohne Planbild: Begründung des Symboltauschs EG-010 STANDARD_SPOT → RIVO_Aufheller_Variante (Drehung 0°), Normbezug A01 (EN 1838 4.1.1) und A04 (4.3.1–4.3.2 Antipanik 0,5 lx, Ud 1:40), offener Nachweis in Orange.
> „Die Lichtaufgabe auf einer großen offenen Fläche unterscheidet sich von einer bloßen Mittellinie im schmalen Gang.“
> „Ein dichteres Leuchtenraster kann erst aus einer Berechnung entstehen.“
> „Große offene Flächen mit mehreren Ankünften separat betrachten; Leuchtenzahl und grafische Symmetrie ersetzen keine Lichtberechnung.“
**Leuchten im Bild:** EG-010 aufheller
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 20796 · Symboltausch wie beschrieben im Inventar belegt (RIVO_Aufheller_Variante, rot 0°).
**Bewertung:** bestaetigt:NB-R10

## S.111 · EG — F-EG-08 Einzelbezüge — EG-010 Typ B
**Bereich:** nördliche offene MFU
**Bild:** Einzelbezugsseite: Detailausschnitt mit orangem Kreis um EG-010 am Originalstandort der RIVO-DXF. Rechts Steckbrief: Funktion (beleuchtende AP-Position), keine RZ-Front, Blockrotation 0°, offener Einzelbefund in Orange.
> „Runde, richtungsfreie AP-Spot-Darstellung; Produkt-/Montagedaten bleiben in Attributen erhalten. Eine Lichtachse ist keine Fluchtrichtungsangabe.“
> „Möblierung und die tatsächlich frei verbundene Fläche sind mit der Lichtberechnung abzugleichen; keine Mitbeleuchtung durch geschlossene Wände annehmen.“
**Leuchten im Bild:** EG-010 aufheller
**Linien:** oranger Markierungskreis, keine Weglinien (Detail ohne zusätzliche Wegbehauptung)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 20796 · Standort und Rotation 0° im Inventar bestätigt.
**Bewertung:** bestaetigt:NB-R10

## S.112 · EG — F-EG-09 E.36 Projektraum: seitlicher Türdurchgang
**Bereich:** Projektraum E.36 östlich der MFU (Raumcode 1.2.3)
**Bild:** Grundriss-Ausschnitt E.36 mit orange markierter westlicher Tür (Bauteil-Rahmen). Tür-RZ EG-006 sitzt in der Türachse der Westwand, Aufheller EG-002 im Raum. Person P1 kommt von Osten, grün gestrichelte Weginterpretation und türkise Sichtlinie laufen nach Westen durch die Tür.
> „Seine Tür liegt in der westlichen Raumwand; EG-006 ist daher gegenüber den südlichen Raumtüren um 90° ausgerichtet.“
> „Die Front von EG-006 zeigt bei 90° nach Osten in den Raum.“
> „Der gezeichnete Pfeil und die Wandlage dürfen nicht isoliert als Nord-/Süd-Entscheidung gelesen werden.“
**Leuchten im Bild:** EG-002 aufheller, EG-006 right
**Personen:** aus E.36 von Osten
**Linien:** grün gestrichelter Weg P1→Tür nach Westen; türkise 2D-Sichtlinie; oranger Rahmen um Türbereich
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 2099C, 20964 · EG-002 = 2099C Aufheller rot 0°; EG-006 = 20964 RIVO_ARR_down rot 90° (Pfeil +X in den Raum) — deckt sich mit PDF.
**Bewertung:** bestaetigt:NB-R01

## S.113 · EG — F-EG-09 E.36 Projektraum: seitlicher Türdurchgang (E–J)
**Bereich:** Projektraum E.36
**Bild:** Textseite E–J: Aufgabentrennung Raumlicht (EG-002) vs. Türkennzeichnung (EG-006), Symboltausch mit Drehung 90°, Normbezüge A01/A03/A04/A09 (u.a. Erkennungsweite l = z × h), offener Nachweis in Orange.
> „EG-002 beleuchtet den Raum; EG-006 kennzeichnet die Tür.“
> „Ein ungedrehtes Türzeichen wäre bei dieser seitlichen Tür vom Raum aus seitlich zu sehen. Eine Drehung muss immer zur Wandlage und Ankunft passen.“
> „Das gleiche Symbol erhält an einer anders orientierten Raumwand eine andere Rotation.“
**Leuchten im Bild:** EG-002 aufheller, EG-006 right
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 2099C, 20964 · Drehung 90° für EG-006 im Inventar bestätigt.
**Bewertung:** bestaetigt:NB-R07

## S.114 · EG — F-EG-09 Einzelbezüge — EG-002 Typ B / EG-006 Typ H
**Bereich:** Projektraum E.36
**Bild:** Zwei Einzelbezüge: EG-002 (Aufheller im Projektraum, Blockrotation 0°, orange umkreist) und EG-006 (Tür-RZ RIVO_ARR_down mit Blockrotation 90°, Zeichenfront und Pfeil im Plan rechts +X, an der westlichen Tür). Offene Einzelbefunde in Orange.
> „Beleuchtende AP-/Aufhellerposition im westlichen Projektraum E36.“
> „Türzeichen am westlichen Ausgang des Projektraums E36; Front nach Osten in den Raum.“
> „Türfunktion zum Raumlicht EG-002; kein Richtungszeichen für Personen, die schon westlich im MFU stehen.“
**Leuchten im Bild:** EG-002 aufheller, EG-006 right
**Linien:** orange Markierungskreise, keine Weglinien
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 2099C, 20964 · Beide Positionen im Inventar bestätigt (Aufheller rot 0°, ARR_down rot 90°).
**Bewertung:** neu → Schule: Unterrichts-/Projektraum erhält eine eigene AP-/Aufheller-Position (Raumlicht bis zur Tür) ZUSÄTZLICH zum Tür-RZ; beide Aufgaben getrennt führen (Raumlicht ohne Front, Tür-RZ mit Front zur Raum-Ankunft) — geht über NB-R10 (Antipanik nur bei Sichtblockade/Lux) hinaus.

## S.115 · EG — F-EG-10 Mittlerer Gang: zwei unterschiedliche Zeichen an einem Knoten
**Bereich:** mittlerer Hauptgang vor dem WC-Stichgang (Sanitärknoten)
**Bild:** Grundriss des mittleren Gangs: Aufheller EG-026 westlich, am Knoten dicht nebeneinander das einseitige Zeichen EG-027 und das beidseitige Zeichen EG-028. Person P1 kommt von Westen, grün gestrichelter Weg läuft nach Osten durch den Durchgang weiter Richtung Gang; türkise Sichtlinie vom WC-Stichgang.
> „Das ist im Bestand ein Paar unterschiedlicher Zeichenfunktionen und kein versehentlich doppelt erfasster Block.“
> „EG-027 hat bei 270° eine Front nach Westen. EG-028 bei 180° hat Fronten nach Norden/Süden und Pfeile nach Osten.“
> „Diese beiden Frontsysteme ergänzen einander; eines davon allein deckt nicht jede Ankunft frontal ab.“
**Leuchten im Bild:** EG-026 aufheller, EG-027 left, EG-028 beidseitig
**Personen:** längs des Gangs von Westen, quer aus dem WC-Stichgang von Norden bzw. aus südlichen Räumen
**Linien:** grün gestrichelte Weginterpretation West→Ost durch den Knoten; türkise 2D-Sichtlinie aus dem Stichgang
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 207B0, 209D4 · EG-026 = 207B0 Aufheller rot 0° bestätigt. Am Knoten findet das Inventar nur EIN RZ (209D4 RIVO_ARR_down, rot_deg 0°, welt_pfeil 270°, Label-Abstand ~2 m); das im PDF beschriebene Paar down 270° + bothsided 180° ist an dieser Stelle nicht beide auffindbar (nächste bothsided-180° = 209F2 bei ganz anderer Koordinate) — Zuordnung EG-027/EG-028 ?
**Bewertung:** neu → Knoten mit drei Ankunftsrichtungen: Kombination aus einseitigem RZ (frontal zur Längsankunft) + beidseitigem RZ (Fronten zu den Querankünften) am SELBEN Knoten; dicht benachbarte Zeichen zuerst funktional analysieren, nicht als Dublette mergen — erweitert NB-R16 (nur Gegenstrom-Paar) und die SL<2m-Merge-Praxis.

## S.116 · EG — F-EG-10 Mittlerer Gang: zwei unterschiedliche Zeichen an einem Knoten (E–J)
**Bereich:** mittlerer Hauptgang, Sanitärknoten
**Bild:** Textseite E–J: Symboltausch EG-026 (Aufheller 0°), EG-027 (ARR_down 270°), EG-028 (ARR_bothsided 180°); Warnung vor Zusammenlegung zu einem einzigen beidseitigen Zeichen; Normbezüge A01/A02/A03/A09, offener Nachweis in Orange.
> „Beide Zeichen zu einem einzigen beidseitigen Zeichen zusammenzulegen könnte die westliche Frontalansicht verlieren.“
> „Bei Richtungsänderungen und Kreuzungen muss die Sicherheitsleuchte beide Richtungen ausleuchten; dies ist keine pauschale Forderung nach einem bestimmten RZ-Block.“
> „Nahe Positionen sind zuerst funktional zu analysieren, bevor man sie als Dublette behandelt.“
**Leuchten im Bild:** EG-026 aufheller, EG-027 left, EG-028 beidseitig
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 207B0, 209D4 · Wie S.115: EG-027/EG-028 im Inventar nicht als Paar verifizierbar (nur 209D4 am Knoten) — ?
**Bewertung:** bestaetigt:NB-R07

## S.117 · EG — F-EG-10 Einzelbezüge — EG-026 Typ C / EG-027 Typ H
**Bereich:** mittlerer Hauptgang westlich des Sanitärknotens
**Bild:** Zwei Einzelbezüge: EG-026 (Aufheller im Gang, Blockrotation 0°, orange umkreist) und EG-027 (RIVO_ARR_down Blockrotation 270°, Zeichenfront und Pfeil im Plan links -X, am zentralen Gangdurchgang). Offene Einzelbefunde in Orange.
> „Beleuchtende AP-/Aufhellerposition im mittleren Hauptgang westlich des Sanitärknotens.“
> „Einseitiges Zeichen am zentralen Gangdurchgang; Front nach Westen.“
> „Übernimmt die westliche Längsankunft vor dem beidseitigen Knotenzeichen EG-028.“
**Leuchten im Bild:** EG-026 aufheller, EG-027 left
**Linien:** orange Markierungskreise, keine Weglinien
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 207B0, 209D4 · EG-026 bestätigt; EG-027-Handle unsicher (Inventar: 209D4 rot_deg 0° statt PDF-Drehung 270°) — ?
**Bewertung:** bestaetigt:NB-R06

## S.118 · EG — F-EG-10 Einzelbezüge — EG-028 Typ H
**Bereich:** mittlerer Knoten am WC-Stichgang
**Bild:** Einzelbezug EG-028: beidseitiges Zeichen RIVO_ARR_bothsided, Blockrotation 180°, Zeichenfronten im Plan oben (+Y) und unten (-Y), grafischer Pfeil rechts (+X); orange umkreist im Detailausschnitt. Offener Einzelbefund in Orange.
> „Beidseitiges Zeichen am mittleren Knoten; Fronten Nord/Süd, Pfeile nach Osten.“
> „Ankünfte aus nördlichen oder südlichen Anschlussbereichen können je eine Front sehen; eine rein westliche Ankunft trifft dagegen eher die Kante.“
> „Für die Übergabe von EG-027 zu EG-028 sind tatsächliche Personenposition und Sicht zu prüfen; keine Rundumsicht unterstellen.“
**Leuchten im Bild:** EG-028 beidseitig
**Linien:** oranger Markierungskreis, keine Weglinien
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · Kein RIVO_ARR_bothsided an der Knotenposition im Inventar auffindbar (bothsided-180° existiert nur als 209F2 bei [115058,127430]) — Handle-Zuordnung ?
**Bewertung:** bestaetigt:NB-R16

## S.119 · EG — F-EG-11 WC Personal und barrierefreies WC: zwei Zugänge
**Bereich:** WC-Bereich nördlich des Hauptgangs: E.29 WC Päd, E.28 Barrierefreies WC, E.27 WC gesch.
**Bild:** Grundriss-Ausschnitt der WC-Gruppe: Aufheller EG-011 beim westlichen Zugang von WC Päd/Personal zum Stichgang, Aufheller EG-012 im barrierefreien WC E.28 mit eigener südlicher Tür zum Hauptgang. Unten am Hauptgang zwei Tür-RZ-Symbole; keine Personenmarke im Ausschnitt.
> „EG-011 liegt als gerichtete beleuchtende Position beim Personal-WC-Zugang, EG-012 im barrierefreien WC.“
> „Diese beiden Ankünfte dürfen nicht als identische Raum-/Türfolge erklärt werden.“
> „Beide Objekte dienen der Beleuchtung. Sie besitzen kein Rettungszeichen und sind keine Belege für die Lesbarkeit eines Ausgangspiktogramms.“
**Leuchten im Bild:** EG-011 aufheller, EG-012 aufheller
**Linien:** keine Weg-/Sichtlinien im Ausschnitt erkennbar (nur Legendenzeile)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 206C3, 206DA · EG-011 = 206C3 Aufheller rot 90° (PDF: Bestands- und Zieldrehung 90°), EG-012 = 206DA Aufheller rot 0° — beide bestätigt.
**Bewertung:** neu → Getrennte WC-Zugänge = getrennte Fluchtfolgen: je WC-Einheit eigene AP-/Aufhellerposition; direkter Gangzugang (barrierefreies WC) und indirekter Weg über Stichgang (Personal-WC) nie als identische Raum-/Türfolge behandeln.

## S.120 · EG — F-EG-11 WC Personal und barrierefreies WC: zwei Zugänge (E–J)
**Bereich:** WC-Gruppe am Hauptgang
**Bild:** Textseite E–J: Symboltausch EG-011 (SPOT_SL → Aufheller, 90°) und EG-012 (SPOT → Aufheller, 0°); Normbezüge A03, A05 (EN 1838 4.3.8 Antipanik in Behinderten-WC, KEINE 8-m²-Grenze), A06 (OVE E 8101 718.560.9.001.AT: Sanitär ab 8 m², 60-m²-Regel nur verkehrstechnisch), A18 (4.1.2 j–k Rufanlagen), A19 (4.3.9 Zwischenweg); langer offener Nachweisblock in Orange.
> „Toiletten für Menschen mit Behinderung benötigen Antipanikbeleuchtung. [...] Diese Klausel nennt keine 8-m²-Grenze und gilt nicht automatisch für jeden barrierefreien Raum.“
> „Bei erhöhten Anforderungen zusätzlich Sanitärbereiche ab 8 m², barrierefreie WC-Anlagen und bezeichnete Elektro-/Sicherheitszentralen prüfen.“
> „Barrierefreie WC-Funktion gesondert prüfen; Flächenschwellen anderer Regeln nicht ungeprüft übertragen.“
**Leuchten im Bild:** EG-011 aufheller, EG-012 aufheller
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 206C3, 206DA · Symboltausch beider Positionen im Inventar bestätigt.
**Bewertung:** neu → Barrierefreies WC benötigt Antipanikbeleuchtung (EN 1838 4.3.8 — ohne Flächengrenze, nur bei echter Behinderten-Toilette); bei erhöhten Anforderungen Sanitärbereiche ab 8 m² prüfen (OVE E 8101 718.560.9.001.AT, 60-m²-Ziffer NUR verkehrstechnische Einrichtungen); Zwischenweg-Beleuchtung nach 4.3.9 als bedingten Prüfauftrag führen, nie Ausstattung (Rufanlage) oder pauschale 5-lx-Werte erfinden.

## S.121 · EG — F-EG-11 Einzelbezüge
**Bereich:** Stichgang WC Päd/Personal E.29 + barrierefreies WC E.28
**Bild:** Zwei Detail-Ausschnitte mit orangem Kreis um die besprochene Position. EG-011 liegt im Stichgang beim WC Päd (E.29) als grüner Aufheller-Kreis mit Achskreuz; EG-012 liegt mittig im barrierefreien WC (E.28). Beide ohne RZ-Front, reine Lichtpunkte.
> „Grafischer Symboltausch geprüft: STANDARD_SPOT_SL → RIVO_Aufheller_Variante nach Auftraggeber-Formregel. Bestandsdrehung 90°, neue Blockdrehung 90°; eine Leuchtenachse ist kein Rettungszeichenpfeil.“
> „Personen bewegen sich innerhalb des geschlossenen barrierefreien WC und verlassen es durch die südliche Tür direkt in den Hauptgang; für den Lichtpunkt gibt es keine RZ-Vorder-/Rückseite.“
> „Die 90-Grad-Bestandsachse und gerichtete Produktoptik sind gesondert zu prüfen; Türvorbereiche und Abschattung der Nebenraumzugänge erfordern einen Lichtnachweis.“
**Leuchten im Bild:** EG-011 aufheller, EG-012 aufheller
**Linien:** oranger Positionskreis je Detail; keine Weg-/Sichtlinien (Detail ohne zusätzliche Wegbehauptung)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49EF8, 49EFA · Kennungen EG-011/EG-012 im DXF-Inventar auf Layer RIVO_ERK_KENNUNG vorhanden; Symboltausch auf RIVO_Aufheller_Variante laut Seite mit Drehung 90°/0°
**Bewertung:** neu → Sanitaer-Nebenraeume: WC-Zugangs-Stichgang und barrierefreies WC erhalten je einen eigenen richtungsfreien Aufheller-Lichtpunkt (keine RZ-Front); Bestands-Leuchtenachse ist kein Rettungszeichenpfeil, gerichtete Optik nur ueber Lichtnachweis anrechenbar

## S.122 · EG — F-EG-12 Sanitär Damen/Herren und Gang davor
**Bereich:** Sanitärraum D (E.26) + Sanitärraum H (E.25) unter TH 3, Gang davor
**Bild:** Fallübersicht: zwei nebeneinanderliegende Sanitärräume mit Kabinentrennwänden. Je Raum ein Aufheller innen (EG-013/014) und ein Tür-RZ an der südlichen Tür (EG-018/019, um 180° gedreht, Front nach Norden in den Raum); EG-029 als Aufheller im Gang davor. P1/P2 mit grün gestrichelten Weglinien von den Kabinen durch die eigene Tür nach Süden in den Gang.
> „Jeder hat ein Rettungszeichen an der südlichen Tür und einen Aufheller innen; EG-029 beleuchtet den Gang davor.“
> „Es gibt keine Verbindung durch die mittlere WC-Trennwand.“
> „EG-018 und EG-019 sind um 180° gedreht und wenden die Front nach Norden in die Sanitärräume. Vom Gang aus ist ihre Rückseite keine verlässliche Wegweisung.“
**Leuchten im Bild:** EG-013 aufheller, EG-014 aufheller, EG-018 down, EG-019 down, EG-029 aufheller
**Personen:** P1 Kabinen/Waschzone Sanitärraum D, P2 Kabinen/Waschzone Sanitärraum H
**Linien:** grün gestrichelt Weginterpretation durch die jeweils eigene Südtür; türkis 2D-Sicht; orange Rahmen um beide Türbereiche
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49EFB, 49EFC, 49F00, 49F01, 49F0B · alle 5 Kennungen im DXF-Inventar (RIVO_ERK_KENNUNG) verifiziert; EG-018/019 als RIVO_ARR_down 180° = Front raumseitig
**Bewertung:** bestaetigt:NB-R01

## S.123 · EG — F-EG-12 Sanitär Damen/Herren und Gang davor — Begründung/Normbezug
**Bereich:** Sanitärräume E.25/E.26 + Gang, Blöcke E-J
**Bild:** Textseite ohne Planbild: Begründung der 5 Positionen, Symboltausch-Liste (EG-013/014/029 → RIVO_Aufheller_Variante 0°; EG-018/019 → RIVO_ARR_down 180°), Normbezüge A01/A03/A06/A09 und offene Nachweise.
> „Ein Lichtpunkt im Gang leuchtet nicht durch die Raumwände; Innenräume, Kabinen und beide Türvorbereiche sind getrennt zu prüfen.“
> „A06 — OVE E 8101: Bei erhöhten Anforderungen zusätzlich Sanitärbereiche ab 8 m², barrierefreie WC-Anlagen und bezeichnete Elektro-/Sicherheitszentralen prüfen. Ziffer 3 ist ausdrücklich auf verkehrstechnische Einrichtungen begrenzt und begründet keine pauschale 60-m²-Schwelle für Schulräume.“
> „Sanitärflächen sind keine leeren Rechtecke. Innere Raumteilung und der Übergang zum Gang bestimmen den Prüfbedarf.“
**Leuchten im Bild:** EG-013 aufheller, EG-014 aufheller, EG-018 down, EG-019 down, EG-029 aufheller
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49EFB, 49EFC, 49F00, 49F01, 49F0B · Symboltausch-Angaben decken sich mit Kennungs-Inventar; Drehungen 0°/180° wie Blatt F angegeben
**Bewertung:** neu → OVE E 8101 718.560.9.001.AT: bei erhoehten Anforderungen Sanitaerbereiche ab 8 m2 und barrierefreie WC-Anlagen auf Notbeleuchtung pruefen; die 60-m2-Regel (Ziffer 3) gilt NUR fuer verkehrstechnische Einrichtungen, keine Pauschal-Schwelle fuer Schulraeume; Licht rechnet nie durch Raumwaende

## S.124 · EG — F-EG-12 Einzelbezüge
**Bereich:** Sanitärraum D (E.26) + Sanitärraum H (E.25)
**Bild:** Zwei Detail-Ausschnitte mit orangem Kreis: EG-013 als Aufheller im westlichen Damenraum vor den Kabinen, EG-014 als Aufheller im östlichen Herrenraum nahe E-Schacht/Lift. Beide Blockrotation 0°, richtungsfreie AP-Spot-Darstellung.
> „Personen verlassen den Raum über die südliche Tür EG-018 und brauchen bis dorthin Licht.“
> „WC-Trennwände und Einbauten können abgeschattete Bereiche erzeugen; der Raumlichtnachweis fehlt.“
> „die mittlere Gangposition EG-029 beleuchtet keinen geschlossenen WC-Raum durch die Wand.“
**Leuchten im Bild:** EG-013 aufheller, EG-014 aufheller
**Linien:** oranger Positionskreis je Detail; keine Weg-/Sichtlinien
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49EFB, 49EFC · Kennungen EG-013/EG-014 im DXF-Inventar verifiziert; STANDARD_SPOT → RIVO_Aufheller_Variante, Drehung 0°
**Bewertung:** bestaetigt:NB-R10

## S.125 · EG — F-EG-12 Einzelbezüge
**Bereich:** Südtüren Sanitärraum D (E.26) und Sanitärraum H (E.25)
**Bild:** Zwei Detail-Ausschnitte: EG-018 und EG-019 als grüne RZ-Blöcke in der jeweiligen südlichen Türachse, oranger Kreis um die Position. Beide RIVO_ARR_down mit Blockrotation 180°, Zeichenfront und grafischer Pfeil im Plan nach oben (+Y) in den Raum.
> „Türzeichen am südlichen Ausgang des westlichen Damen-Sanitärraums; Front nach Norden.“
> „RIVO_ARR_down; Blockrotation 180°. Zeichenfront im Plan: oben (+Y). Grafischer Pfeil im Plan: oben (+Y). Dies beschreibt die CAD-Konvention; Personenbewegung und reales Piktogramm sind getrennt zu prüfen.“
> „WC-Trennwände und Türblatt können die Sicht beeinflussen; der gemeinsame Ganglichtpunkt EG-029 beweist diese Sicht nicht.“
**Leuchten im Bild:** EG-018 down, EG-019 down
**Linien:** oranger Positionskreis je Detail; keine Weg-/Sichtlinien
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49F00, 49F01 · Kennungen EG-018/EG-019 im DXF-Inventar verifiziert; down-Typ 180° = Welt-Pfeil in den Raum, deckungsgleich mit NB-R01-Muster
**Bewertung:** bestaetigt:NB-R01

## S.126 · EG — F-EG-12 Einzelbezüge
**Bereich:** Gang vor den Sanitärtüren E.25/E.26
**Bild:** Detail-Ausschnitt mit orangem Kreis um EG-029: Aufheller-Kreissymbol mittig im Gang zwischen beiden Sanitärtüren, südlich davon ein weiteres Gang-RZ. Im Bestand gerichteter SL-Spot, als richtungsfreie RIVO_Aufheller_Variante dargestellt.
> „Im Gang vor den Damen- und Herren-Sanitärtüren liegt ein im Bestand gerichteter SL-Spot. Er betrifft beide äußeren Türvorbereiche.“
> „Bestandsdrehung 0°, neue Blockdrehung 0°; eine Leuchtenachse ist kein Rettungszeichenpfeil.“
> „Gerichtete Optik und Lichtüberdeckung beider Türvorbereiche bleiben offen; das Symbol ist kein Rettungszeichenpfeil.“
**Leuchten im Bild:** EG-029 aufheller
**Linien:** oranger Positionskreis; keine Weg-/Sichtlinien
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49F0B · Kennung EG-029 im DXF-Inventar verifiziert; STANDARD_SPOT_SL → RIVO_Aufheller_Variante 0°
**Bewertung:** neu → Ein gemeinsamer Gang-Aufheller darf mehrere benachbarte Tuervorbereiche bedienen (SL-Analogie zu NB-R08-Mehrfachbedienung); er ersetzt aber keinen Raumlichtpunkt hinter der Wand und traegt keine Richtungsinformation

## S.127 · EG — F-EG-13 Sozialraum, Teamraum und südliche MFU
**Bereich:** Sozialraum inkl. Küche (E.33), Teamraum (E.32), offene MFU (MUFU 2.2.1)
**Bild:** Fallübersicht: Gang mit zwei südlich anschließenden geschlossenen Räumen. EG-036/037 als Tür-RZ an deren nördlichen Türen (Blockrotation 0°, Front nach Süden in den Raum), grün gestrichelte Weglinien von P1/P2 aus den Räumen nach Norden in den Gang. EG-038 als Aufheller in der offenen MFU östlich davon.
> „EG-036/037 kennzeichnen deren nördliche Türen. EG-038 gehört zur offenen MFU östlich davon.“
> „Die Raumtüren führen nach Norden in den Gang. Von dort setzt sich der Fluchtweg zur zugewiesenen Stiege fort.“
> „EG-036/037 sind bei 0° frontal aus den südlichen Räumen lesbar. Personen im Gang sehen ihre Rückseiten. EG-038 hat keine Piktogrammseite.“
**Leuchten im Bild:** EG-036 down, EG-037 down, EG-038 aufheller
**Personen:** P1 Sozialraum inkl. Küche, P2 Teamraum
**Linien:** grün gestrichelt Weginterpretation aus beiden Räumen in den Gang; türkis 2D-Sicht; orange markierte Türbauteile
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49F14, 49F15, 49F16 · Kennungen EG-036/037/038 im DXF-Inventar verifiziert; Tür-RZ down 0° = Front raumseitig
**Bewertung:** bestaetigt:NB-R01

## S.128 · EG — F-EG-13 Sozialraum, Teamraum und südliche MFU — Begründung/Normbezug
**Bereich:** Sozialraum/Küche + Teamraum + MFU, Blöcke E-J
**Bild:** Textseite ohne Planbild: Begründung der Türpositionen, Symboltausch-Liste (EG-036/037 → RIVO_ARR_down 0°; EG-038 → RIVO_Aufheller_Variante 0°), Normbezüge A01/A03/A04/A08 und offene Nachweise zur Raumbeleuchtung und Küche.
> „In diesen geschlossenen Räumen ist keine zusätzliche physische SL-Position in der erfassten Zielmenge vorhanden; das ist eine Nachweislücke, keine Behauptung, vor Ort fehle sicher jede Leuchte.“
> „A08 — EN 1838 4.4.1-4.4.7: Bei besonderer Gefährdung: auf der Arbeitsfläche mindestens 10 % des für die Aufgabe erforderlichen Wartungswerts und mindestens 15 lx; Gleichmäßigkeit Uo mindestens 0,1. Bedingung: Gefährdungsbeurteilung für z. B. Werk-/Küchenbereich erforderlich; kein Automatismus allein aus Raumname.“
> „Ein Nachbarsymbol hinter einer Wand darf bei der Raumprüfung nicht als vorhandene Lichtabdeckung mitgezählt werden.“
**Leuchten im Bild:** EG-036 down, EG-037 down, EG-038 aufheller
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49F14, 49F15, 49F16 · Symboltausch-Angaben decken sich mit Kennungs-Inventar
**Bewertung:** neu → Kuechen-/Werkbereiche (Schule): EN 1838 4.4 besondere Gefaehrdung nur ueber Gefaehrdungsbeurteilung ausloesen (>=10% Wartungswert, >=15 lx, Uo>=0,1, verfuegbar in 0,5 s) — KEIN Automatismus aus dem Raumnamen; Nachbarleuchte hinter Wand zaehlt nie als Raumabdeckung

## S.129 · EG — F-EG-13 Einzelbezüge
**Bereich:** Nordtüren Sozialraum (E.33) und Teamraum (E.32)
**Bild:** Zwei Detail-Ausschnitte mit orangem Kreis: EG-036 und EG-037 als grüne Tür-RZ in den nördlichen Türachsen der beiden Räume. Beide RIVO_ARR_down, Blockrotation 0°, Zeichenfront und grafischer Pfeil im Plan nach unten (-Y) in den geschlossenen Raum.
> „Türzeichen am nördlichen Ausgang des Sozialraums inklusive Küche; Front nach Süden in den geschlossenen Raum.“
> „RIVO_ARR_down; Blockrotation 0°. Zeichenfront im Plan: unten (-Y). Grafischer Pfeil im Plan: unten (-Y).“
> „Eine zusätzliche eigene Raum-SL ist in der Zielmenge nicht erfasst. Beleuchtung, Kücheneinbauten und Türsicht bleiben offen.“
**Leuchten im Bild:** EG-036 down, EG-037 down
**Linien:** oranger Positionskreis je Detail; keine Weg-/Sichtlinien
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49F14, 49F15 · Kennungen EG-036/EG-037 im DXF-Inventar verifiziert; down 0° = Welt-Pfeil in den Raum (Türachse), NB-R01-Muster
**Bewertung:** bestaetigt:NB-R01

## S.130 · EG — F-EG-13 Einzelbezüge
**Bereich:** Offene MFU (MUFU, Raumcode 2.2.1)
**Bild:** Detail-Ausschnitt mit orangem Kreis um EG-038: richtungsfreier Aufheller-Kreis in der offenen Multifunktionsfläche östlich von Sozial- und Teamraum, nahe der südlichen Fassade. Keine Piktogrammseite, keine Wegbehauptung.
> „Beleuchtende AP-/Aufhellerposition in der offenen MFU östlich von Sozial- und Teamraum.“
> „Lichtpunkt außerhalb der geschlossenen Räume EG-036/037; deren Innenflächen werden dadurch nicht automatisch erfasst.“
> „Offene Flächengrenzen, Möblierung und Lichtverteilung sind nachzuweisen; keine Lichtwirkung durch geschlossene Raumwände behaupten.“
**Leuchten im Bild:** EG-038 aufheller
**Linien:** oranger Positionskreis; keine Weg-/Sichtlinien
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49F16 · Kennung EG-038 im DXF-Inventar verifiziert; STANDARD_SPOT → RIVO_Aufheller_Variante 0°
**Bewertung:** bestaetigt:NB-R23

## S.131 · EG — F-EG-14 TH 3: zwei Podestzeichen und Balkonzugang
**Bereich:** Stiegenhaus TH 3 (4.2.2) mit Balkonanschluss Ost
**Bild:** Fallübersicht des Stiegenhauses TH 3: EG-001 als left-RZ am nördlichen Stiegenabschnitt (0°, Pfeil nach Westen, Front Süd), EG-007 als left-RZ 180° am südlichen Abschnitt (Pfeil nach Osten, Front Nord), EG-003 als beidseitiges RZ am östlichen Balkon-/Türanschluss (Pfeile nach Westen, Fronten Nord/Süd). Treppenlauf mit Auge, östlich Balkon und E-Schacht.
> „EG-001/007 liegen an gegenüberliegenden Stiegenabschnitten; EG-003 steht östlich am Balkon-/Türanschluss.“
> „Der Balkon wird nicht als sicherer Endausgang behandelt. Der Weg zwischen den Läufen muss das westliche Zwischenpodest benutzen, nicht das Treppenauge.“
> „EG-003 ist beidseitig bei 0° mit Pfeilen nach Westen und Fronten Nord/Süd; von Osten kann es überwiegend seitlich erscheinen.“
**Leuchten im Bild:** EG-001 left, EG-003 beidseitig, EG-007 left
**Linien:** grün gestrichelte Weginterpretation von MFU/Küche zum Stiegenhaus; türkis angenommene 2D-Sicht; orange markierter Balkonanschluss
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49EEE, 49EF0, 49EF4 · Kennungen EG-001/003/007 im DXF-Inventar verifiziert; EG-003 = RIVO_ARR_bothsided (beidseitig-Gruppe im Inventar vorhanden)
**Bewertung:** bestaetigt:NB-R04

## S.132 · EG — F-EG-14 TH 3: zwei Podestzeichen und Balkonzugang — Begründung/Normbezug
**Bereich:** Stiegenhaus TH 3, Blöcke E-J
**Bild:** Textseite ohne Planbild: Symboltausch-Liste (EG-001 → RIVO_ARR_left 0°, EG-003 → RIVO_ARR_bothsided 0°, EG-007 → RIVO_ARR_left 180°), Normbezüge A01/A02/A03/A09 und offene Nachweise zu Schnitt/Höhenkoten, Balkonanschluss und Stufenbeleuchtung.
> „In der Zielmenge ist keine eigene SL im TH-3-Lauf erfasst; Stufenbeleuchtung bleibt daher ausdrücklich nachzuweisen.“
> „A02 — EN 1838 4.1.2 a-g: Bei Richtungsänderungen und Kreuzungen muss die Sicherheitsleuchte beide Richtungen ausleuchten; dies ist keine pauschale Forderung nach einem bestimmten RZ-Block.“
> „Die Architektur-Aufwärtspfeile legen nicht automatisch den Rettungsweg nach unten fest.“
> „Gegensinnige Podestpfeile sind nur zusammen mit Lauf, Podest und Höhe erklärbar.“
**Leuchten im Bild:** EG-001 left, EG-003 beidseitig, EG-007 left
**Linien:** keine (reine Textseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 49EEE, 49EF0, 49EF4 · Symboltausch-Angaben decken sich mit Kennungs-Inventar; bothsided-Block als eine Einheit (Engine-Konvention) statt 2 gespiegelter Einzelbloecke
**Bewertung:** neu → Stiegen-Interpretation nur mit Lauf+Podest+Hoehe: Architektur-Aufwaertspfeile legen den Rettungsweg NICHT automatisch nach unten fest (Pruefvorbehalt zu NB-R04/NB-R13, Schnitt/Hoehenkoten noetig); EN 1838 4.1.2 fordert Ausleuchtung beider Richtungen, aber keinen bestimmten RZ-Blocktyp

## S.133 · EG — F-EG-14 Einzelbezüge — EG-001 / EG-003
**Bereich:** TH 3, gegenüberliegende Stiegenabschnitte + östlicher Zugang
**Bild:** Zwei Detailausschnitte mit orangem Kreis um die besprochene Position. EG-001 (RIVO_ARR_left, Rotation 0°) sitzt am nördlichen der beiden gegenüberliegenden Stiegenabschnitte von TH 3, Front nach Süden zum ankommenden Podest-/Laufstrom. EG-003 (RIVO_ARR_bothsided, Rotation 0°) sitzt am östlichen Zugang beim Balkon-/Türanschluss, Fronten Nord/Süd, Pfeile nach Westen.
> „Gegenläufige Orientierung zu EG-007 am anderen Abschnitt“
> „Eine Person auf dem zugehörigen südlich ankommenden Podest-/Laufabschnitt kann die Front sehen; die konkrete Geschossherkunft braucht den Schnitt.“
> „Keine Verbindung quer über das Treppenauge zeichnen.“
> „keine zusätzliche Frontalansicht allein durch Beidseitigkeit“
> „Balkon ist kein bestätigter sicherer Endausgang.“
**Leuchten im Bild:** EG-001 left, EG-003 beidseitig
**Linien:** keine Weg-/Sichtlinien; orange Positionskreise um beide Symbole
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 2075C, 20669 · EG-001=2075C (RIVO_ARR_left rot 0°) und EG-003=20669 (RIVO_ARR_bothsided rot 0°) via Kennung-Nähe (411/301 mm) bestätigt; Block+Rotation deckungsgleich mit Seitentext
**Bewertung:** bestaetigt:NB-R04

## S.134 · EG — F-EG-14 Einzelbezüge — EG-007
**Bereich:** TH 3, südlicher Gegenabschnitt der Stiege
**Bild:** Ein Detailausschnitt: EG-007 (RIVO_ARR_left, Rotation 180°) am südlichen Gegenabschnitt von TH 3 im Raum mit Stempel 'TH 3, Raumcode 4.2.2'; Pfeil nach Osten, Front nach Norden zum passenden Lauf-/Podestniveau. Um 180° gegenüber EG-001 gedreht — je Lauf/Personenstrom eine eigene Richtungsphase.
> „Um 180 Grad gegenüber EG-001 gedreht; erklärt die andere Richtungsphase in der Stiege, nicht denselben Blickpunkt.“
> „Höhenkoten und tatsächlicher Abstieg über das Podest müssen bestätigt werden; der Grundriss allein ordnet keinen Treppenlauf sicher zu.“
**Leuchten im Bild:** EG-007 left
**Linien:** keine; oranger Positionskreis
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 20779 · EG-007=20779 (RIVO_ARR_left rot 180°) via Kennung-Nähe (213 mm) bestätigt; deckungsgleich mit Seitentext
**Bewertung:** bestaetigt:NB-R04

## S.135 · EG — F-EG-15 Küche und westlicher Zugang: kombinierte Ankünfte — Fallseite A-D
**Bereich:** Küchenbereich östlich von TH 3, Übergang Gang/offene Fläche
**Bild:** Planausschnitt mit vier Positionen: EG-008 (Tür-RZ an der westlichen Küchenwand, oranger Rahmen), EG-009 (Aufheller in der Küche mit Raumstempel 'mküche'), EG-020/030 (beidseitige Zeichen am Übergang Gang/offene Fläche). Person P1 steht östlich in der Küche, grün gestrichelte Weglinie nach Westen auf EG-008 zu.
> „Personen kommen aus der Küche von Osten, längs des Gangs von Westen und quer aus der offenen Fläche. Diese Wege treffen nicht unter demselben Sichtwinkel auf die Zeichen.“
> „EG-008 hat Front nach Osten.“
> „Bei EG-008/020 weicht der Produkttext 'CONCEPT AP … EW20m' von einer bloßen Standard-RZ-Bezeichnung ab: Produkt-/Kombifunktion bleibt zu prüfen.“
**Leuchten im Bild:** EG-008 down, EG-009 aufheller, EG-020 beidseitig, EG-030 beidseitig
**Personen:** P1 aus der Küche (Osten)
**Linien:** grün gestrichelte Weginterpretation P1->EG-008; oranger Rahmen um EG-008-Bauteil
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 208A0, 2064B · EG-009=208A0 (Aufheller, 294 mm) und EG-030=2064B (bothsided rot 270°, 300 mm) bestätigt; EG-008/EG-020: Kennungslabels >2.9 m von der nächsten passenden Leuchte (Leader-Versatz), Handle-Zuordnung ? — Blocktyp/Drehung laut Seitentext down 90° bzw. bothsided 270°
**Bewertung:** bestaetigt:NB-R01

## S.136 · EG — F-EG-15 Küche und westlicher Zugang — Begründung/Normbezug (E-J)
**Bereich:** Küchenbereich östlich von TH 3
**Bild:** Reine Textseite (E-J) ohne Planausschnitt. Symboltausch-Protokoll: EG-008 STANDARD_RZ_PU->RIVO_ARR_down 90°, EG-009 STANDARD_SPOT->RIVO_Aufheller_Variante 0°, EG-020/030 STANDARD_RZ_PLPR->RIVO_ARR_bothsided 270°, alle 'ersetzt, Bezugspunkt und Attribute erhalten'. Normbezug A01/A03/A04/A08 (Küche = mögliche besondere Gefährdung, 15 lx) und A09 (l=z×h). Orange offene Nachweise: Hersteller-/Kombinationsdaten, Fluchttürfolge, Küchen-Gefährdung, Lichtwerte.
> „Der Symboltausch übernimmt die vorhandene RZ-Grafik von EG-008/020, ohne aus dem Produktnamen eine zusätzliche Leuchte zu erzeugen oder eine Kombifunktion zu löschen.“
> „Ein genereller Ersatz der RZ-Blöcke durch AP-Kreise nur wegen des Produkttexts würde die vorhandene Richtungsinformation verlieren.“
> „A08 … Bedingung: Gefährdungsbeurteilung für z. B. Werk-/Küchenbereich erforderlich; kein Automatismus allein aus Raumname.“
> „CAD-Grafik, Attribute und reale Gerätefunktion gemeinsam prüfen; widersprüchliche Hinweise sichtbar erhalten.“
**Leuchten im Bild:** EG-008 down, EG-009 aufheller, EG-020 beidseitig, EG-030 beidseitig
**Linien:** keine (Textseite); orange Hinweistexte in Abschnitt I
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 208A0, 2064B · wie S.135; Symboltausch-Zeilen (F) decken sich mit Block/Rotation der bestätigten Handles
**Bewertung:** neu → Attribut/Grafik-Widerspruch: weicht der Produkttext (z.B. 'CONCEPT AP … EW20m') von der RZ-Grafik ab, wird die Grafik-Rolle beibehalten und der Widerspruch sichtbar als offener Prüfpunkt erhalten — kein automatischer Symboltyp-Wechsel aus Produktnamen, keine Zusatzleuchte aus Attributen; Gefährdungs-Lux (15 lx, EN 1838 4.4) nie allein aus dem Raumnamen ableiten

## S.137 · EG — F-EG-15 Einzelbezüge — EG-008 / EG-009
**Bereich:** Küche, westlicher Küchenausgang
**Bild:** Zwei Detailausschnitte. EG-008 (RIVO_ARR_down, Rotation 90°) als Tür-RZ am westlichen Küchenausgang in der Türachse, Zeichenfront +X nach Osten in den Küchenraum. EG-009 (STANDARD_SPOT->RIVO_Aufheller_Variante, 0°) als runder richtungsfreier Aufheller in der Küche ('warmküche'-Stempel).
> „Personen aus der Küche kommen auf die östliche Schildfront zu und treten danach in den angrenzenden Bereich.“
> „Eine Lichtachse ist keine Fluchtrichtungsangabe.“
> „Produktattribute CONCEPT AP/EW 20 m passen nicht eindeutig zur RZ-Grafik.“
> „Einbauten, Arbeitsplätze und mögliche besondere Gefährdung benötigen eigene Bewertung; allein der Raumname liefert keinen fertigen Nachweis.“
**Leuchten im Bild:** EG-008 down, EG-009 aufheller
**Linien:** keine; orange Positionskreise
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 208A0 · EG-009=208A0 bestätigt; EG-008-Handle ? (Kennungslabel abgesetzt), Typ laut Text RIVO_ARR_down rot 90°
**Bewertung:** bestaetigt:NB-R01

## S.138 · EG — F-EG-15 Einzelbezüge — EG-020 / EG-030
**Bereich:** Westlicher Küchenanschluss / Hauptgang vor der TH-3-Folge
**Bild:** Zwei Detailausschnitte mit je einem beidseitigen Richtungszeichen (RIVO_ARR_bothsided, Rotation 270°): EG-020 näher an der Küchenfolge EG-008/009, EG-030 als vorgelagerter Orientierungspunkt im Hauptgang. Beide Fronten Ost/West, grafischer Pfeil +Y nach Norden; südliche Längsankunft sieht sie nur seitlich.
> „Seitliche Ankünfte aus Küche/Verbindung beziehungsweise westlichem Bereich treffen verschiedene Fronten; eine Längsankunft von Süden kann seitlich sein.“
> „Vorgelagerter Orientierungspunkt westlich von EG-020, kein zweites Zeichen an derselben Küchentür.“
> „Produkt-/Attributwiderspruch CONCEPT AP/EW 20 m sowie genaue Ankunftszuordnung und Montage müssen vor einer fachlichen Freigabe geklärt werden.“
**Leuchten im Bild:** EG-020 beidseitig, EG-030 beidseitig
**Linien:** keine; orange Positionskreise
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 2064B · EG-030=2064B (bothsided rot 270°, 300 mm) bestätigt; EG-020-Handle ? (nächster passender Block 2.9 m vom Kennungslabel, Leader-Versatz)
**Bewertung:** bestaetigt:NB-R16

## S.139 · EG — F-EG-16 Personalnebenräume am östlichen Rand — Fallseite A-D
**Bereich:** Ostrand: Sozialraum KP (E.23), Garderobe/Umkleide (E.21), Dusch-/WC KP (E.22)
**Bild:** Planausschnitt der Nebenraumkette am schrägen Ostrand: EG-015 (Tür-RZ am südlichen Sozialraumausgang), EG-021 (Aufheller in der Garderobe E.21), EG-022 (beidseitiges Zeichen in der Verbindung), EG-031 (Tür-/Durchgangszeichen am südlichen Ende zur offenen Fläche). Raumstempel mit Raumcodes 3.2.5/3.2.6/3.2.2 sichtbar; keine Personenmarker.
> „Drei Rettungszeichen ordnen die aufeinanderfolgenden Übergänge; EG-021 ist ein Aufheller im Nebenraum.“
> „EG-015 kennzeichnet den ersten südlichen Türdurchgang; EG-022 lenkt bei 90° nach Süden, EG-031 markiert den anschließenden Durchgang in die offene Fläche.“
> „Die vollständige Sichtfolge ist deshalb nicht allein durch die Anzahl drei belegt.“
**Leuchten im Bild:** EG-015 down, EG-021 aufheller, EG-022 beidseitig, EG-031 down
**Linien:** keine expliziten Weg-/Sichtlinien im Ausschnitt; Legende Grün/Türkis/Orange im Fußtext
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 209B6, 20914, 208F6, 208BA · EG-015=209B6 (down 180°), EG-021=20914 (Aufheller), EG-022=208F6 (bothsided 90°), EG-031=208BA (down 180°) — alle via Kennung-Nähe 177-341 mm bestätigt, Block+Rotation deckungsgleich
**Bewertung:** bestaetigt:NB-R12

## S.140 · EG — F-EG-16 Personalnebenräume am östlichen Rand — Begründung/Normbezug (E-J)
**Bereich:** Ostrand: Sozialraum/Umkleide/WC-Folge
**Bild:** Reine Textseite (E-J). Symboltausch: EG-015/031 RZ_PU->RIVO_ARR_down 180°, EG-021 SPOT->Aufheller 0°, EG-022 RZ_PLPR->RIVO_ARR_bothsided 90°. Normbezug A01/A02/A03/A09 plus A06 (OVE E 8101: Sanitärbereiche ab 8 m², barrierefreie WCs; 60-m²-Regel nur verkehrstechnische Einrichtungen) und A19 (EN 1838 4.3.9: Zwischenweg-Beleuchtung als bedingter Prüfauftrag). Orange offene Nachweise zu Türnutzung, Befestigungsseiten, Zellensicht, Zwischenweg.
> „EG-021 kann nur die tatsächlich erreichbare Nebenraumfläche beleuchten; geschlossene WC-Trennwände bleiben zu berücksichtigen.“
> „Das mittlere Zeichen wegen seiner Nähe zu den anderen zu entfernen würde eine seitliche Ankunft möglicherweise ohne Richtungsinformation lassen.“
> „A06 … Ziffer 3 ist ausdrücklich auf verkehrstechnische Einrichtungen begrenzt und begründet keine pauschale 60-m²-Schwelle für Schulräume.“
> „A19 … besteht kein direkter Zugang zu den Rettungswegen im angrenzenden Brandabschnitt, muss auch der dazwischenliegende Rettungsweg beleuchtet werden.“
> „Auch kurze Nebenraumfolgen brauchen eine Prüfung jeder Tür und jeder seitlichen Ankunft.“
**Leuchten im Bild:** EG-015 down, EG-021 aufheller, EG-022 beidseitig, EG-031 down
**Linien:** keine (Textseite); orange Hinweistexte in Abschnitt I
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 209B6, 20914, 208F6, 208BA · wie S.139; Symboltausch-Zeilen (F) decken sich mit den bestätigten Handles
**Bewertung:** neu → Mehrstufige Nebenraumfolgen (Sozialraum->Umkleide/WC->Gang, Schul-/Personalbereich): je Tür UND je seitlicher Ankunft eigene Sichtprüfung; Aufheller deckt nur die real erreichbare Fläche (kein Licht durch geschlossene Trennwände); EN 1838 4.3.9-Zwischenweg und OVE-Sanitärschwellen (ab 8 m², barrierefreie WCs) als BEDINGTE Prüfaufträge führen — keine pauschale 60-m²-Schwelle für Schulräume

## S.141 · EG — F-EG-16 Einzelbezüge — EG-015 / EG-021
**Bereich:** Sozialraum-KP-Ausgang und Garderobe E.21
**Bild:** Zwei Detailausschnitte. EG-015 (RIVO_ARR_down, Rotation 180°) als Türzeichen am südlichen Sozialraumausgang, Zeichenfront +Y nach Norden zum ankommenden Strom; im Ausschnitt darunter ist bereits EG-022 sichtbar. EG-021 (SPOT->RIVO_Aufheller_Variante, 0°) im Garderobenraum E.21 (Raumcode 3.2.6) zwischen Dusch- und WC-Raum E.22.
> „Personen aus dem Sozialraum kommen von Norden auf die Front zu und gelangen in die Nebenraumverbindung.“
> „Erster Türdurchgang der Folge EG-015, EG-022, EG-031; die drei Zeichen bedienen unterschiedliche Übergänge.“
> „Lichtabdeckung hinter WC-/Umkleidetrennwänden und die genaue Raumfläche bleiben offen; kein Lichtdurchgang durch geschlossene Wände annehmen.“
**Leuchten im Bild:** EG-015 down, EG-021 aufheller
**Linien:** keine; orange Positionskreise
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 209B6, 20914 · EG-015=209B6 (down 180°) und EG-021=20914 (Aufheller 0°) bestätigt
**Bewertung:** bestaetigt:NB-R01

## S.142 · EG — F-EG-16 Einzelbezüge — EG-022 / EG-031
**Bereich:** Verbindung der östlichen Personalnebenräume, südlicher Austritt
**Bild:** Zwei Detailausschnitte. EG-022 (RIVO_ARR_bothsided, Rotation 90°) in der Nebenraumverbindung: Fronten +X/-X (Ost/West), grafischer Pfeil -Y nach Süden; die längs von Norden kommende Person trifft nur die Kante. EG-031 (RIVO_ARR_down, Rotation 180°) am südlichen Durchgang zur offenen Fläche, Front +Y nach Norden.
> „Eine seitliche Ankunft aus Umkleide oder Nebenraum kann eine Front sehen; die Person aus dem nördlichen Sozialraum trifft eher die Kante.“
> „Die nördliche Längsankunft braucht eine eigene Sichtprüfung; eine lückenlose lesbare Dreierfolge ist nicht allein aus drei Symbolen belegt.“
> „Personen aus den nördlichen Nebenräumen kommen auf die Front zu, nachdem sie den Bereich EG-022 passiert haben.“
**Leuchten im Bild:** EG-022 beidseitig, EG-031 down
**Linien:** keine; orange Positionskreise
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 208F6, 208BA · EG-022=208F6 (bothsided 90°) und EG-031=208BA (down 180°) bestätigt
**Bewertung:** bestaetigt:NB-R07

## S.143 · EG — F-EG-17 Östliche MFU und Verbindung zum Bestand — Fallseite A-D
**Bereich:** Östliche offene MFU, Übergang zum Bestand (Essbereich E.20, Richtung TH 2)
**Bild:** Breiter Planausschnitt der östlichen MFU mit schräger Bestandsfuge (STUK +3,00). EG-039 (beidseitiges Zeichen, Fronten Ost/West, Pfeil nach Norden) und EG-040 (grüner Aufheller-Spot ohne Piktogrammseite) liegen nördlich des Essbereichs E.20; am oberen Rand weitere schon behandelte Symbole der Nebenraumfolge. Keine Personenmarker, keine Weg-/Sichtlinien im Ausschnitt.
> „EG-040 ist ein beleuchtender Spot mit im Bestand gerichteter SL-Variante, der nach Formregel als Aufheller dargestellt wird.“
> „Der südliche Bestandsflügel mit TH 2 ist im Fluchtplan enthalten, aber nicht durch eine vollständige erkannte RIVO-Zielobjektfolge abgedeckt; siehe F-X-03.“
> „Die südliche Ankunft kann auf die Schmalseite treffen und verlangt eine zusätzliche Sichtprüfung. EG-040 hat keine Piktogrammseite.“
**Leuchten im Bild:** EG-039 beidseitig, EG-040 aufheller
**Linien:** keine im Ausschnitt; Legende Grün/Türkis/Orange im Fußtext
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 2082F, 2084D · EG-039=2082F (bothsided rot 270°) und EG-040=2084D (Aufheller 0°) via Kennung-Nähe (300/333 mm) bestätigt
**Bewertung:** bestaetigt:NB-R24

## S.144 · EG — F-EG-17 Östliche MFU und Verbindung zum Bestand — Begründung/Normbezug (E-J)
**Bereich:** Östliche offene MFU / Bestandsanschluss
**Bild:** Reine Textseite (E-J). Symboltausch: EG-039 RZ_PLPR->RIVO_ARR_bothsided 270°; EG-040 STANDARD_SPOT_SL->RIVO_Aufheller_Variante 0°/0° ('Bestandsachse entfällt grafisch, Optik offen'). Große freie Fläche als mögliche Antipanik-Aufgabe (A04) benannt, aber Umfang erst mit Fluchtwegkonzept und Lichtberechnung. Orange offene Nachweise: Bestandsanschluss, Nordfreigabe, Südsicht, Flächenbeleuchtung.
> „Die große freie Fläche kann eine Antipanik-Beleuchtungsaufgabe auslösen, doch Umfang, Anschluss und geforderte Werte sind erst mit Fluchtwegkonzept und Lichtberechnung festzustellen.“
> „Eine angenommene Fortsetzung nach Süden ohne weitere Bestandsaufnahme wäre kein geschlossener Nachweis bis zum Ausgang.“
> „Der Rand einer erfassten Leuchtenmenge ist nicht automatisch der Rand des zu prüfenden Rettungswegs.“
**Leuchten im Bild:** EG-039 beidseitig, EG-040 aufheller
**Linien:** keine (Textseite); orange Hinweistexte in Abschnitt I
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 2082F, 2084D · wie S.143; SL-Bestandsachse von EG-040 im Ziel-DXF grafisch entfallen (Optik offen)
**Bewertung:** neu → Erfassungsrand ≠ Prüfrand: das Ende der erfassten/ersetzten Leuchtenmenge (RIVO-Zielobjektfolge) beendet NICHT den nachzuweisenden Rettungsweg — angrenzende Bestandsflügel (hier TH 2) bleiben als offene Frage/eigener Nachweis geführt, nie als stillschweigend abgedeckt; angenommene Fortsetzungen ohne Bestandsaufnahme sind kein geschlossener Nachweis

## S.145 · EG — F-EG-17 Einzelbezüge
**Bereich:** östliche MFU / Übergang zum südlichen Bestandsbereich
**Bild:** Zwei Detail-Ausschnitte mit orangen Kreisen um die Originalstandorte in der RIVO-DXF. EG-039 (Typ H) ist ein beidseitiges Zeichen in der östlichen MFU am Übergang zum Bestand, Fronten Ost/West, grafischer Pfeil +Y. EG-040 (Typ D) ist der ehemals gerichtete SL-Spot, jetzt runde Aufheller-Variante, als rein beleuchtender Teil der Gruppe. Offene Befunde orange: südliche Person/seitliche Sicht und TH-2-Bestandsfolge nicht erfasst; gerichtete Optik nicht nachgewiesen.
> „Beidseitiges Zeichen in der östlichen MFU am Übergang zum südlichen Bestandsbereich; Fronten Ost/West, Pfeile nach Norden.“
> „Er ist der beleuchtende Teil dieser Situation; EG-039 übernimmt getrennt die Richtungsinformation.“
> „eine Leuchtenachse ist kein Rettungszeichenpfeil“
**Leuchten im Bild:** (EG-039) beidseitig, (EG-040) aufheller
**Linien:** keine Weg-/Sichtlinien, nur orange Positionskreise (Detail ohne Wegbehauptung)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 2082F, 2084D · 2082F = RIVO_ARR_bothsided rot 270° (deckt Text 'Blockrotation 270°, Fronten -X/+X, Pfeil +Y'); 2084D = RIVO_Aufheller_Variante rot 0° (STANDARD_SPOT_SL ersetzt) — beides bestätigt.
**Bewertung:** bestaetigt:NB-R16

## S.146 · OG — F-OG-01 1.39 Projektraum: Tür zum Westgang
**Bereich:** 1.39 Projektraum nördlich des gemeinsamen Gangs
**Bild:** Fallseite A–D mit Planausschnitt: Person P1 im Projektraum 1.39, grün gestrichelte Weginterpretation von der Raumnutzung zur südlichen Gangtür mit Tür-RZ OG-017 (orange umrahmtes Bauteil = Tür), Aufheller OG-003 mittig im Raum. Türkise Linie als angenommene 2D-Sicht. Folge: Raum – Tür – Gang – TH 4 im Westen – über untere Podeste zum Westausgang im SG.
> „Das Rettungszeichen sitzt an der zugehörigen Gangtür; der runde Aufheller liegt innerhalb des Raums.“
> „Das einseitige Zeichen ist um 180° gedreht. Seine Front zeigt in den Raum, also nach Norden; vom Gang sieht man eher die Rückseite.“
> „Der grafische Abwärtspfeil bezeichnet hier den Türdurchgang und ist kein Höhenplan.“
**Leuchten im Bild:** (OG-003) aufheller, (OG-017) down
**Personen:** Raumnutzung 1.39 Projektraum (P1, zwischen den Möbeln)
**Linien:** grün gestrichelt Raum→Tür→Gang; türkis 2D-Sichtlinie P1→OG-017; orange Türrahmen
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B7D2, 1B437 · 1B7D2 = RIVO_Aufheller_Variante rot 0°; 1B437 = RIVO_ARR_down rot 180° — deckt Text (Front +Y in den Raum) exakt.
**Bewertung:** neu → Schul-Muster Unterrichts-/Projektraum: JEDER Unterrichtsraum erhält ein raumseitiges Tür-RZ nach NB-R01 (Front in den Raum, down-Typ, 180°) PLUS genau einen Aufheller im Rauminneren — der Wohnbau-Skip (WOHNUNG_PRIVAT ohne Innen-Notlicht) gilt für Klassenräume NICHT.

## S.147 · OG — F-OG-01 1.39 Projektraum: Tür zum Westgang (E–J)
**Bereich:** 1.39 Projektraum — Begründung/Normbezug
**Bild:** Reine Textseite E–J ohne Planbild. Symboltausch dokumentiert (OG-003 SPOT→Aufheller 0°, OG-017 RZ_PU→ARR_down 180°). Normbezüge A01 (EN 1838 4.1.1 Sichtkette), A03 (4.2.1–4.2.2 Fluchtweg-Lux 1 lx Mittellinie), A04 (4.3 Antipanik 0,5 lx), A09 (5.5 Erkennungsweite l=z×h, z=100/200). Orange: für 1.39 fehlen Notlichtberechnung, Möblierung, Montagehöhen, reale Zeichenhöhe, Sicht bei offenem Türblatt.
> „Die Türposition verknüpft die Orientierung mit einer konkreten Öffnung. Der Aufheller erfüllt die Beleuchtungsaufgabe im Raum.“
> „Erkennungsweite l = z × h; z=100 für extern beleuchtete, z=200 für hinterleuchtete Zeichen ... keine Umrechnung aus der grafischen Größe eines CAD-Symbols.“
> „Zuerst die Person im Raum und die reale Tür zuordnen, danach die Fortsetzung im Gang prüfen; Zeichen- und Beleuchtungsaufgabe bleiben getrennt.“
**Leuchten im Bild:** (OG-003) aufheller, (OG-017) down
**Linien:** keine (Textseite)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B7D2, 1B437 · Symboltausch-Angaben (Blöcke, Drehungen 0°/180°) stimmen mit Inventar überein.
**Bewertung:** bestaetigt:NB-R01

## S.148 · OG — F-OG-01 Einzelbezüge
**Bereich:** 1.39 Projektraum
**Bild:** Einzelbezugs-Seite: OG-003 (Typ B) als beleuchtende AP-/Aufhellerposition im Projektraum 1.39, richtungsfreie runde Darstellung; OG-017 (Typ H) als Türzeichen an der Südtür, Front nach Norden in den Raum. Orange Kreise markieren die Originalstandorte, offene Einzelbefunde zu Möblierung, offenem Türblatt und Anschluss-Sicht in der MFU.
> „Türzeichen an der südlichen Tür des Projektraums 1.39; Front nach Norden.“
> „Personen aus dem Projektraum kommen auf die innere Front zu; nach der Tür beginnt die eigene MFU-Sichtfolge.“
> „Eine Lichtachse ist keine Fluchtrichtungsangabe.“
**Leuchten im Bild:** (OG-003) aufheller, (OG-017) down
**Linien:** nur orange Positionskreise, keine Wegbehauptung
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B7D2, 1B437 · RIVO_ARR_down rot 180° und Aufheller rot 0° bestätigt.
**Bewertung:** bestaetigt:NB-R01

## S.149 · OG — F-OG-02 1.38 Bildungsraum: Raumankunft von Norden
**Bereich:** 1.38 Bildungsraum nördlich des gemeinsamen Gangs
**Bild:** Fallseite A–D, baugleiches Muster wie F-OG-01 im Nachbarraum: Person P1 im Bildungsraum 1.38, grüne Weginterpretation zur südlichen Gangtür mit Tür-RZ OG-014 (orange markiert), Aufheller OG-004 im Raum. Folge Raum – Tür – Gang – TH 4 – untere Podeste – Westausgang SG; endgültige Raum-zu-Ausgang-Zuordnung bleibt mit dem Fluchtwegkonzept abzugleichen.
> „Das Rettungszeichen sitzt an der zugehörigen Gangtür; der runde Aufheller liegt innerhalb des Raums.“
> „Das einseitige Zeichen ist um 180° gedreht. Seine Front zeigt in den Raum, also nach Norden; vom Gang sieht man eher die Rückseite.“
> „Die endgültige Zuordnung jedes Raums zu einem Ausgang bleibt mit dem Fluchtwegkonzept abzugleichen.“
**Leuchten im Bild:** (OG-004) aufheller, (OG-014) down
**Personen:** Raumnutzung 1.38 Bildungsraum (P1)
**Linien:** grün gestrichelt Raum→Tür; türkis 2D-Sicht; orange Türrahmen
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B6B5, 1B455 · 1B6B5 = RIVO_Aufheller_Variante rot 0°; 1B455 = RIVO_ARR_down rot 180° — bestätigt.
**Bewertung:** bestaetigt:NB-R01

## S.150 · OG — F-OG-02 1.38 Bildungsraum: Raumankunft von Norden (E–J)
**Bereich:** 1.38 Bildungsraum — Begründung/Normbezug
**Bild:** Textseite E–J, wortgleiches Gerüst wie S.147 für den Bildungsraum 1.38. Symboltausch OG-004 SPOT→Aufheller 0° und OG-014 RZ_PU→ARR_down 180°. Normbezüge A01/A03/A04/A09 (EN 1838). Orange: Notlichtberechnung, Möblierung, Montagehöhen, reale Zeichenhöhe und Sicht bei geöffnetem Türblatt fehlen; aus zwei Symbolen wird keine vollständige Raumabdeckung abgeleitet.
> „Seine mittige Lage beweist weder den Mindestwert am Boden noch die Ausleuchtung hinter Schränken.“
> „Aus der Anzahl von zwei Symbolen wird keine vollständige Raumabdeckung abgeleitet.“
> „Zeichen- und Beleuchtungsaufgabe bleiben getrennt.“
**Leuchten im Bild:** (OG-004) aufheller, (OG-014) down
**Linien:** keine (Textseite)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B6B5, 1B455 · Drehungen 0°/180° und Blocknamen decken sich mit dem Inventar.
**Bewertung:** bestaetigt:NB-R01

## S.151 · OG — F-OG-02 Einzelbezüge
**Bereich:** 1.38 Bildungsraum
**Bild:** Einzelbezugs-Seite: OG-004 (Typ B) beleuchtende Aufhellerposition im Bildungsraum 1.38; OG-014 (Typ H) Türzeichen am südlichen Ausgang, Front nach Norden. Explizite Abgrenzung zum Nachbarraum: keine gemeinsame Fläche durch die Trennwand, jeder Raum hat sein eigenes Paar (1.38: OG-004/014, 1.39: OG-003/017).
> „Eigene Raumbeleuchtung neben dem Projektraum mit OG-003/017; keine gemeinsame Fläche durch die Trennwand.“
> „Personen aus dem Bildungsraum kommen von innen auf die Türfront zu, bevor sie die MFU erreichen.“
> „Orientierende Ergänzung zur Raumbeleuchtung OG-004“
**Leuchten im Bild:** (OG-004) aufheller, (OG-014) down
**Linien:** nur orange Positionskreise
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B6B5, 1B455 · bestätigt (Aufheller 0°, ARR_down 180°).
**Bewertung:** bestaetigt:NB-R01

## S.152 · OG — F-OG-03 Westgang und Tür in TH 4
**Bereich:** Westgang zwischen MFU und TH 4, südlicher Stiegenzugang
**Bild:** Fallseite A–D mit Gangausschnitt: P1 kommt aus der MFU von Osten, grüne Weginterpretation läuft nach Westen durch den Gang und biegt vor TH 4 nach Süden ab. OG-019 (Tür-RZ, 90°, Front Ost) am MFU-Ausgang, OG-018 (Aufheller) mittig im Gang, OG-029 (Tür-RZ, 180°, Front Nord) an der Stiegentür; Lift 2 grenzt an. Der Richtungswechsel wird durch die Abfolge zweier Türsituationen gelöst, ausdrücklich OHNE beidseitiges Zeichen.
> „Anders als im EG ist der Stiegeneintritt durch OG-029 als einseitiges Türzeichen dargestellt.“
> „OG-019 bei 90° ist frontal aus Osten lesbar; OG-029 bei 180° ist frontal von Norden lesbar.“
> „Der Richtungswechsel entsteht durch die Abfolge zweier Türsituationen, nicht durch ein hier nicht vorhandenes beidseitiges Zeichen.“
**Leuchten im Bild:** (OG-018) aufheller, (OG-019) down, (OG-029) down
**Personen:** MFU von Osten, seitlich aus Bildungs-/Projekträumen (P1)
**Linien:** grün gestrichelte Fluchtlinie Ost→West→Süd-Abzweig; türkise Sichtannahme; orange markierte Türen
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B737, 1B4AF, 1B491 · 1B737 Aufheller 0°, 1B4AF ARR_down 90° (Front +X), 1B491 ARR_down 180° (Front +Y) — deckt Text exakt.
**Bewertung:** bestaetigt:NB-R07

## S.153 · OG — F-OG-03 Westgang und Tür in TH 4 (E–J)
**Bereich:** Westgang/TH 4 — Begründung/Normbezug
**Bild:** Textseite E–J: Symboltausch OG-018 SPOT→Aufheller 0°, OG-019 RZ_PU→ARR_down 90°, OG-029 RZ_PU→ARR_down 180°. Normbezüge A01, A02 (EN 1838 4.1.2 a–g: Richtungsänderungen/Kreuzungen beidseitig AUSLEUCHTEN, keine pauschale RZ-Block-Forderung), A03, A09 und neu A17 (OVE E 8101: X-Kennzeichnung 2019 vs. Erforderlich-Zeichen für Dauerbetrieb ab AC1:2020). Orange: Sicht zur Stiegentür nach dem ersten Durchgang, Türblätter, Lichtwerte am Abzweig, Schaltungs-/Betriebsnachweis offen.
> „Die EG-Konfiguration einfach ins OG zu kopieren würde den tatsächlich unterschiedlichen Bestand überschreiben.“
> „Bei Richtungsänderungen und Kreuzungen muss die Sicherheitsleuchte beide Richtungen ausleuchten; dies ist keine pauschale Forderung nach einem bestimmten RZ-Block.“
> „Ähnliche Geschosse anhand ihrer wirklichen Blöcke prüfen; Unterschiede zwischen EG und OG sind Teil der Erklärung.“
**Leuchten im Bild:** (OG-018) aufheller, (OG-019) down, (OG-029) down
**Linien:** keine (Textseite)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B737, 1B4AF, 1B491 · Drehungen 0°/90°/180° stimmen mit dem Inventar überein.
**Bewertung:** neu → Geschoss-Individualität: dieselbe Grundriss-Stelle kann je Geschoss einen anderen Zeichentyp brauchen (EG-023 beidseitig vs. OG-029 einseitig am selben TH-4-Zugang); Geschoss-Konfigurationen NIE kopieren, sondern je Geschoss gegen die wirklichen Blöcke/den Bestand prüfen. Ergänzend A17/OVE E 8101: Betriebsart (Dauerbetrieb auf Fluchtwegen ab AC1:2020) ist gebäudeweit festzulegen und aus der RZ-Grafik nicht ablesbar (Enis-Lane).

## S.154 · OG — F-OG-03 Einzelbezüge
**Bereich:** Westgang zwischen MFU und TH 4
**Bild:** Einzelbezugs-Seite: OG-018 (Typ B) als gemeinsame Gangbeleuchtung zwischen den beiden Türzeichen, kein Schildfrontbezug; OG-019 (Typ H) Türzeichen am westlichen MFU-Ausgang mit Blockrotation 90°, Zeichenfront und Pfeil im Plan nach rechts (+X), frontal für den von Osten ankommenden Strom.
> „Gemeinsame Gangbeleuchtung bei den unterschiedlichen Türzeichen OG-019 und OG-029.“
> „Personen aus der MFU nähern sich von Osten der Front und orientieren sich nach dem Gangdurchtritt neu.“
> „Erster Übergang zum westlichen Gang; OG-029 bezeichnet danach die eigene Stiegentür, OG-018 beleuchtet dazwischen.“
**Leuchten im Bild:** (OG-018) aufheller, (OG-019) down
**Linien:** nur orange Positionskreise
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B737, 1B4AF · ARR_down rot 90° = Front +X wie beschrieben; Aufheller rot 0° — bestätigt.
**Bewertung:** bestaetigt:NB-R07

## S.155 · OG — F-OG-03 Einzelbezüge (Fortsetzung)
**Bereich:** südlicher TH-4-Zugang aus dem Westgang
**Bild:** Einzelbezugs-Seite nur für OG-029 (Typ H): einseitiges Türzeichen an der Stiegentür, Blockrotation 180°, Front nach Norden zum ankommenden Gangstrom. Ausdrückliche Abgrenzung zum EG: dort ist die gleiche Stelle mit dem beidseitigen EG-023 gelöst; EG-/OG-Diagramme dürfen nicht gleichgesetzt werden. Orange: Sicht am Türblatt, Anschlussorientierung zu OG-036/040 und eine fehlende eigene obere Podest-SL.
> „Anders als EG-023 ist es ein einseitiges Türzeichen statt eines beidseitigen Richtungszeichens; EG-/OG-Diagramme dürfen nicht gleichgesetzt werden.“
> „Personen im Gang kommen von Norden auf die Front an der Stiegentür zu.“
> „eine eigene obere Podest-SL ist in der Zielmenge nicht erfasst.“
**Leuchten im Bild:** (OG-029) down
**Linien:** nur oranger Positionskreis
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B491 · RIVO_ARR_down rot 180°, Front +Y — bestätigt. Beidseitig nur dort, wo tatsächlich Gegenströme denselben Knoten nutzen (EG), sonst einseitig (OG).
**Bewertung:** bestaetigt:NB-R16

## S.156 · OG — F-OG-04 TH 4: Podestfolge ohne erfasste eigene SL
**Bereich:** Stiegenhaus TH 4 am Westkopf mit Lift 2
**Bild:** Fallseite A–D mit Stiegenhausausschnitt: zwei Läufe mit Zwischenpodest, angrenzender Lift 2 (orange markiert). OG-036 (90°, zeigt nach Süden, Front Ost) und OG-040 (270°, zeigt nach Norden, Front West) sind die zwei erfassten RZ — jede Tafel für eine andere Podest-/Laufankunft. Der Lift wird mangels Nachweis nicht als Evakuierungsweg eingezeichnet; Abkürzung über die Mittelöffnung ausgeschlossen; Lauf/Podest-Wechsel braucht Höhen-/Schnittabgleich.
> „Der Lift wird mangels Nachweis nicht als Evakuierungsweg eingezeichnet.“
> „OG-036 zeigt bei 90° nach Süden und hat Front nach Osten. OG-040 zeigt bei 270° nach Norden, Front nach Westen. Jede Tafel ist für eine andere Podest-/Laufankunft ausgerichtet.“
> „Die geschossübergreifende Folge verläuft über EG und SG zum Westausgang.“
**Leuchten im Bild:** (OG-036) left, (OG-040) left
**Linien:** grün gestrichelte Wegdeutung im Stiegenhaus; orange Rahmen um Lift 2
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B3FD, 1B41A · 1B3FD = RIVO_ARR_left rot 90° (Pfeil Süd, Front Ost), 1B41A = RIVO_ARR_left rot 270° (Pfeil Nord, Front West) — je Lauf/Podest-Ankunft eine eigene Tafel; Lift-Ausschluss deckt NB-R27, Je-Lauf-Ausrichtung deckt NB-R04/NB-R05.
**Bewertung:** bestaetigt:NB-R04

## S.157 · OG — F-OG-04 TH 4: Podestfolge ohne erfasste eigene SL
**Bereich:** TH 4, westlicher Stiegenabschnitt + südlicher Wendebereich
**Bild:** Reine Textseite (E-J) zum Fall F-OG-04. Beide RZ (OG-036/OG-040) werden lagegleich ersetzt (STANDARD_RZ_PL -> RIVO_ARR_left, 90°/270°). Kernaussage: In der erfassten Zielmenge existiert keine eigene Stiegen-SL; das wird als fehlender Beleuchtungsnachweis und Bestandsklärung ausgewiesen. Normzitate A01/A02/A03/A09 (EN 1838 4.1.1, 4.1.2 a-g, 4.2.1-4.2.2, 5.5).
> „Die beiden grünen Zeichen als ausreichende Stufenbeleuchtung anzurechnen würde zwei unterschiedliche Anforderungen verwechseln.“
> „Eine plausible Zeichenfolge kann gleichzeitig eine ungeklärte Beleuchtungsaufgabe enthalten.“
> „Schnitt, Höhen, reale SL-Ausstattung, jede direkt beleuchtete Stufe und Abschattung durch Handläufe sind offen.“
**Leuchten im Bild:** OG-036 left, OG-040 left
**Linien:** keine Grafik, reine Begründungsseite
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B3FD, 1B41A · OG-036 = RIVO_ARR_left rot 90° (Welt-Pfeil 270°/Süd), OG-040 = RIVO_ARR_left rot 270° (Welt-Pfeil 90°/Nord) — deckt die F-Angaben der Seite exakt; keine Aufheller-/SL-Position an TH 4 im OG-Bestand = deckt den Befund 'keine eigene Stiegen-SL'.
**Bewertung:** neu → RZ ersetzt keine Stufen-SL: eine plausible Richtungszeichen-Kette an einer Stiege deckt NICHT die Beleuchtungsaufgabe der Stufen (EN 1838 4.1.2 b); fehlt eine eigene Stiegen-SL in der Zielmenge, ist das als fehlender Beleuchtungsnachweis + Bestandsklärung auszuweisen, nicht durch Anrechnung der RZ zu heilen.

## S.158 · OG — F-OG-04 Einzelbezüge
**Bereich:** TH 4 bei Lift 2, Stiegenlauf + südlicher Wendebereich
**Bild:** Zwei DXF-Ausschnitte mit orangen Kreisen. OG-036: Richtungszeichen am westlichen Stiegenabschnitt von TH 4 (neben Lift 2), Front nach Osten, Pfeil nach Süden, RIVO_ARR_left rot 90°. OG-040: Richtungszeichen am südlichen Wendebereich, Front nach Westen, Pfeil nach Norden, RIVO_ARR_left rot 270°. Beide bedienen je eine Richtungsphase des Laufs; Zugang aus dem Gang wird zuvor durch OG-029 bezeichnet.
> „Die frontale Ankunft liegt auf dem passenden östlichen Lauf-/Podestabschnitt; die Höhenzuordnung braucht den Schnitt.“
> „Die Person muss auf dem zugehörigen westlichen Podestabschnitt auf die Front treffen, nachdem sie den realen Richtungswechsel vollzogen hat.“
> „kein Sprung über das Treppenauge“
**Leuchten im Bild:** OG-036 left, OG-040 left
**Personen:** OG-Strom auf dem Lauf-/Podestabschnitt von TH 4 (implizit, nicht gezeichnet)
**Linien:** keine Weg-/Sichtlinien; nur orange Positionskreise im DXF-Ausschnitt
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B3FD, 1B41A · Blocknamen und Rotationen (left/90° und left/270°) im DXF identisch zur Seitenangabe; Welt-Pfeile 270°(Süd)/90°(Nord) passen zu 'Pfeil nach Süden'/'Pfeil nach Norden'.
**Bewertung:** bestaetigt:NB-R05

## S.159 · OG — F-OG-05 1.37 Bildungsraum neben TH 4
**Bereich:** 1.37 Bildungsraum (6-10), südlich des gemeinsamen Gangs, nahe TH 4
**Bild:** Fallseite A-D mit DXF-Ausschnitt: Tür-RZ OG-030 sitzt an der Gangtür des Bildungsraums 1.37 (orange gerahmt), runder Aufheller OG-037 liegt mittig im Raum. Person P1 steht im Raum, grün gestrichelte Weginterpretation führt durch die Tür in den Gang Richtung TH 4. Front des einseitigen Zeichens zeigt nach Süden in den Raum; der grafische Abwärtspfeil bezeichnet den Türdurchgang, kein Höhenplan.
> „Das Rettungszeichen sitzt an der zugehörigen Gangtür; der runde Aufheller liegt innerhalb des Raums.“
> „Die Person kommt aus der Raumnutzung ... und tritt erst danach in den Gang.“
> „Seine Front zeigt in den Raum, also nach Süden; vom Gang sieht man eher die Rückseite.“
> „Der grafische Abwärtspfeil bezeichnet hier den Türdurchgang und ist kein Höhenplan.“
**Leuchten im Bild:** OG-030 down, OG-037 aufheller
**Personen:** P1 aus der Raumnutzung des Bildungsraums 1.37 (Süden)
**Linien:** grün gestrichelt = Weginterpretation Raum-Tür-Gang; türkis = angenommene 2D-Sicht; orange = markiertes Bauteil (Tür)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B473, 1B69B · OG-030 = RIVO_ARR_down rot 0° (Welt-Pfeil 270°/Süd = Front in den Raum), OG-037 = RIVO_Aufheller_Variante rot 0° — deckt Seite.
**Bewertung:** neu → Schul-Unterrichtsraum-Ausstattung: jeder Bildungsraum erhält ein Tür-RZ an der Gangtür (raumseitig, Front in den Raum, nach NB-R01) PLUS einen richtungsfreien AP-Aufheller im Rauminneren — anders als Wohnbau (WOHNUNG_PRIVAT ohne Innen-Notlicht); Zeichen- und Beleuchtungsaufgabe getrennt, Lux-Nachweis bleibt offen.

## S.160 · OG — F-OG-05 1.37 Bildungsraum neben TH 4
**Bereich:** 1.37 Bildungsraum, Gangtür + Rauminneres
**Bild:** Reine Textseite (E-J) zu F-OG-05. Symboltausch: OG-030 STANDARD_RZ_PU -> RIVO_ARR_down 0°, OG-037 STANDARD_SPOT -> RIVO_Aufheller_Variante 0°. Türposition verknüpft Orientierung mit konkreter Öffnung; der Aufheller trägt die Beleuchtungsaufgabe, seine mittige Lage beweist aber weder Mindestwert am Boden noch Ausleuchtung hinter Schränken. Normzitate A01/A03/A04/A09.
> „Die Türposition verknüpft die Orientierung mit einer konkreten Öffnung. Der Aufheller erfüllt die Beleuchtungsaufgabe im Raum.“
> „Seine mittige Lage beweist weder den Mindestwert am Boden noch die Ausleuchtung hinter Schränken.“
> „Zuerst die Person im Raum und die reale Tür zuordnen, danach die Fortsetzung im Gang prüfen; Zeichen- und Beleuchtungsaufgabe bleiben getrennt.“
> „Aus der Anzahl von zwei Symbolen wird keine vollständige Raumabdeckung abgeleitet.“
**Leuchten im Bild:** OG-030 down, OG-037 aufheller
**Linien:** keine Grafik, reine Begründungsseite
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B473, 1B69B · Symboltausch-Angaben (down 0°, Aufheller 0°) im DXF bestätigt.
**Bewertung:** bestaetigt:NB-R01

## S.161 · OG — F-OG-05 Einzelbezüge
**Bereich:** 1.37 Bildungsraum: Nordtür + Raummitte
**Bild:** Zwei Einzel-Ausschnitte. OG-030 Typ H: Türzeichen am nördlichen Ausgang des Bildungsraums 1.37, Front nach Süden (RIVO_ARR_down 0°, Zeichenfront -Y, Pfeil -Y); westlichster der drei südlichen Bildungsraumzugänge. OG-037 Typ B: beleuchtende AP-/Aufhellerposition im Raum (RIVO_Aufheller_Variante 0°), rund und richtungsfrei; eine Lichtachse ist keine Fluchtrichtungsangabe.
> „Türzeichen am nördlichen Ausgang des Bildungsraums 1.37; Front nach Süden.“
> „Runde, richtungsfreie AP-Spot-Darstellung; Produkt-/Montagedaten bleiben in Attributen erhalten. Eine Lichtachse ist keine Fluchtrichtungsangabe.“
> „Möblierung, Abschattung und Lichtabdeckung bis zur Nordtür bleiben offen.“
**Leuchten im Bild:** OG-030 down, OG-037 aufheller
**Personen:** Personen aus 1.37 (von innen)
**Linien:** keine Weg-/Sichtlinien; nur orange Positionskreise
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B473, 1B69B · Block/Rotation beider Leuchten im DXF identisch zur Seitenangabe.
**Bewertung:** bestaetigt:NB-R01

## S.162 · OG — F-OG-06 1.36 Bildungsraum an der MFU
**Bereich:** 1.36 Bildungsraum (6-10), mittlerer der drei südlichen Bildungsräume
**Bild:** Fallseite A-D, Muster identisch zu F-OG-05: Tür-RZ OG-031 an der Gangtür (orange gerahmt), Aufheller OG-038 im Rauminneren, Person P1 im Raum mit grün gestrichelter Weginterpretation durch die Tür in den Gang Richtung TH 4. Front des einseitigen Zeichens (0°) zeigt nach Süden in den Raum; Abwärtspfeil = Türdurchgang, kein Höhenplan.
> „Das Rettungszeichen sitzt an der zugehörigen Gangtür; der runde Aufheller liegt innerhalb des Raums.“
> „Die Folge lautet Raum - bezeichnete Tür - Gang - TH 4 im Westen.“
> „Die endgültige Zuordnung jedes Raums zu einem Ausgang bleibt mit dem Fluchtwegkonzept abzugleichen.“
**Leuchten im Bild:** OG-031 down, OG-038 aufheller
**Personen:** P1 aus der Raumnutzung des Bildungsraums 1.36 (Süden)
**Linien:** grün gestrichelt = Weginterpretation; türkis = angenommene 2D-Sicht; orange = markiertes Bauteil (Tür)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B4CD, 1B667 · OG-031 = RIVO_ARR_down rot 0° (Welt-Pfeil 270°/Süd), OG-038 = RIVO_Aufheller_Variante 0° — deckt Seite; Muster identisch zu F-OG-05.
**Bewertung:** bestaetigt:NB-R01

## S.163 · OG — F-OG-06 1.36 Bildungsraum an der MFU
**Bereich:** 1.36 Bildungsraum, Gangtür + Rauminneres
**Bild:** Reine Textseite (E-J), wortgleich zum Muster F-OG-05: OG-031 STANDARD_RZ_PU -> RIVO_ARR_down 0°, OG-038 STANDARD_SPOT -> RIVO_Aufheller_Variante 0°. Türposition = Orientierung an konkreter Öffnung, Aufheller = Beleuchtungsaufgabe; mittige Lage beweist keinen Mindestwert. Normzitate A01/A03/A04/A09; offene Nachweise Notlichtberechnung, Möblierung, Montagehöhen, Zeichenhöhe, Türblatt-Sicht.
> „Die Türposition verknüpft die Orientierung mit einer konkreten Öffnung.“
> „Eine Verlegung des Zeichens auf die Gangseite würde die Lesbarkeit beim Verlassen des Raums verändern.“
> „Aus der Anzahl von zwei Symbolen wird keine vollständige Raumabdeckung abgeleitet.“
**Leuchten im Bild:** OG-031 down, OG-038 aufheller
**Linien:** keine Grafik, reine Begründungsseite
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B4CD, 1B667 · Symboltausch-Angaben im DXF bestätigt.
**Bewertung:** bestaetigt:NB-R01

## S.164 · OG — F-OG-06 Einzelbezüge
**Bereich:** 1.36 Bildungsraum: Nordtür + Raummitte
**Bild:** Zwei Einzel-Ausschnitte. OG-031 Typ H: Türzeichen am nördlichen Ausgang von 1.36, Front nach Süden (RIVO_ARR_down 0°); mittlerer Raumzugang der Dreierreihe. OG-038 Typ B: Aufhellerposition im Raum (RIVO_Aufheller_Variante 0°), mittlere Raumbeleuchtung zwischen OG-037 und OG-039; ausdrücklich kein gemeinsamer Lichtnachweis für die drei Räume — Licht zählt je Raum, nicht über Trennwände.
> „Mittlere Raumbeleuchtung zwischen OG-037 und OG-039, kein gemeinsamer Lichtnachweis für die drei Räume.“
> „Freie Sicht aus den Nutzungsbereichen und das nächste Zeichen nach der Tür sind offen.“
> „Nutzbare Fläche, Schrank-/Tischanordnung und Türvorbereich sind noch nicht photometrisch nachgewiesen.“
**Leuchten im Bild:** OG-031 down, OG-038 aufheller
**Personen:** Personen aus dem mittleren Bildungsraum (von Süden)
**Linien:** keine Weg-/Sichtlinien; nur orange Positionskreise
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B4CD, 1B667 · Block/Rotation im DXF identisch zur Seitenangabe.
**Bewertung:** bestaetigt:NB-R01

## S.165 · OG — F-OG-07 1.35 Bildungsraum am mittleren Gang
**Bereich:** 1.35 Bildungsraum (6-10), östlicher der drei südlichen Bildungsräume, neben Sozialraum 1.24
**Bild:** Fallseite A-D, drittes identisches Muster: Tür-RZ OG-032 an der Gangtür (orange gerahmt), Aufheller OG-039 im Rauminneren, Person P1 mit grün gestrichelter Weginterpretation. Folge hier: Raum - Tür - Gang - mittlerer Gang - im Fluchtplan zugewiesene Stiege (Zuordnung mit Fluchtwegkonzept abzugleichen). Front des Zeichens (0°) nach Süden in den Raum; Abwärtspfeil = Türdurchgang.
> „Die Folge lautet Raum - bezeichnete Tür - Gang - zum mittleren Gang und weiter zur im Fluchtplan zugewiesenen Stiege.“
> „Die endgültige Zuordnung jedes Raums zu einem Ausgang bleibt mit dem Fluchtwegkonzept abzugleichen.“
> „Seine Front zeigt in den Raum, also nach Süden; vom Gang sieht man eher die Rückseite.“
**Leuchten im Bild:** OG-032 down, OG-039 aufheller
**Personen:** P1 aus der Raumnutzung des Bildungsraums 1.35 (Süden)
**Linien:** grün gestrichelt = Weginterpretation; türkis = angenommene 2D-Sicht; orange = markiertes Bauteil (Tür)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B4EB, 1B681 · OG-032 = RIVO_ARR_down rot 0° (Welt-Pfeil 270°/Süd), OG-039 = RIVO_Aufheller_Variante 0° — deckt Seite; Stiegen-Zuweisung über Fluchtplan = gerichtete TH-Zuordnung (vgl. NB-R24).
**Bewertung:** bestaetigt:NB-R01

## S.166 · OG — F-OG-07 1.35 Bildungsraum am mittleren Gang
**Bereich:** 1.35 Bildungsraum, Gangtür + Rauminneres
**Bild:** Reine Textseite (E-J), Muster wie F-OG-05/06: OG-032 STANDARD_RZ_PU -> RIVO_ARR_down 0°, OG-039 STANDARD_SPOT -> RIVO_Aufheller_Variante 0°. Türposition trägt die Orientierung, Aufheller die Beleuchtung; mittige Lage beweist keinen Bodenmindestwert. Normzitate A01/A03/A04/A09; offene Nachweise identisch (Notlichtberechnung, Möblierung, Montagehöhen, Zeichenhöhe, Türblatt-Sicht).
> „Der Aufheller erfüllt die Beleuchtungsaufgabe im Raum. Seine mittige Lage beweist weder den Mindestwert am Boden noch die Ausleuchtung hinter Schränken.“
> „Ein zusätzliches Gangzeichen müsste als eigene Funktion mit passender Richtung beurteilt werden.“
> „Zeichen- und Beleuchtungsaufgabe bleiben getrennt.“
**Leuchten im Bild:** OG-032 down, OG-039 aufheller
**Linien:** keine Grafik, reine Begründungsseite
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B4EB, 1B681 · Symboltausch-Angaben im DXF bestätigt.
**Bewertung:** bestaetigt:NB-R01

## S.167 · OG — F-OG-07 Einzelbezüge
**Bereich:** 1.35 Bildungsraum: Nordtür + Raummitte
**Bild:** Zwei Einzel-Ausschnitte. OG-032 Typ H: Türzeichen am nördlichen Ausgang von 1.35, Front nach Süden (RIVO_ARR_down 0°); östlichster der drei Bildungsraumzugänge. OG-039 Typ B: Aufheller im Raum (RIVO_Aufheller_Variante 0°), östlicher Lichtpunkt der Reihe, ausdrücklich von der offenen MFU-Leuchte OG-035 zu trennen; Licht durch die Trennwand in Nachbarräume wird nicht angenommen.
> „Östlicher der drei Bildungsraumzugänge; OG-039 beleuchtet seinen Innenraum.“
> „Östlicher Lichtpunkt der südlichen Bildungsraumreihe; von der offenen MFU-Leuchte OG-035 zu trennen.“
> „Raummöblierung und vollständige Lichtabdeckung bleiben offen; Licht durch die Trennwand in Nachbarräume wird nicht angenommen.“
**Leuchten im Bild:** OG-032 down, OG-039 aufheller
**Personen:** Personen aus dem östlichen Bildungsraum
**Linien:** keine Weg-/Sichtlinien; nur orange Positionskreise
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B4EB, 1B681 · Block/Rotation im DXF identisch zur Seitenangabe.
**Bewertung:** bestaetigt:NB-R01

## S.168 · OG — F-OG-08 MFU im Obergeschoss: freie Kernfläche
**Bereich:** große offene MFU nördlich des Gangs, Kernfläche
**Bild:** Fallseite A-D: Aufheller OG-009 liegt in der großen offenen MFU (MUFU OG.1.1.2). Person P1 steht neben der Leuchte, grün gestrichelte Weginterpretation führt nach Süden in den Gang. Benutzer kommen aus unterschiedlichen Teilen der offenen Nutzung, nicht nur entlang einer einzelnen Mittellinie; westlich schließen F-OG-03/04 an, östlich der mittlere Knoten. Das runde AP-Symbol ist ein Beleuchtungszeichen ohne Pfeil und ohne Vorder-/Rückseitenfunktion.
> „Benutzer kommen aus unterschiedlichen Teilen der offenen Nutzung, nicht nur entlang einer einzelnen Mittellinie.“
> „Die Fläche öffnet sich nach Süden in den Gang. ... die Fluchtplanzuweisung entscheidet über die endgültige Stiege und den Außenweg.“
> „Das runde AP-Symbol ist ein Beleuchtungszeichen ohne Pfeil und ohne Vorder-/Rückseitenfunktion.“
**Leuchten im Bild:** OG-009 aufheller
**Personen:** P1 aus der offenen MFU-Nutzung (Kernfläche)
**Linien:** grün gestrichelt = Weginterpretation MFU -> Gang; türkis = angenommene 2D-Sicht; orange = markiertes Bauteil
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B6CF · OG-009 = RIVO_Aufheller_Variante rot 0° in der MFU-Kernfläche — deckt Seite; richtungsfreier AP-Punkt in offener Lernlandschaft, die den Fluchtweg trägt.
**Bewertung:** bestaetigt:NB-R23

## S.169 · OG — F-OG-08 MFU im Obergeschoss: freie Kernfläche
**Bereich:** MFU (offene Multifunktionsfläche), nördlicher Bereich OG
**Bild:** Reine Textseite (E-J-Begründung) zum Aufheller OG-009 in der offenen MFU. Kernaussage: Für eine offene Fläche ist die freie Boden-Kernfläche zu berechnen, nicht nur ein Weg unter der Leuchte. Normbezüge A01 (EN 1838 4.1.1) und A04 (Antipanik 4.3.1-4.3.2: 0,5 lx Kernbereich, 0,5-m-Randstreifen ausgenommen, Ud 1:40).
> „Für eine offene Fläche ist die freie Boden-Kernfläche zu berechnen, nicht nur ein Weg unter der Leuchte.“
> „Antipanikflächen flächenbezogen bewerten und anschließend den Anschluss an den Rettungsweg prüfen.“
> „A04: Antipanik: mindestens 0,5 lx auf der freien Bodenfläche im Kernbereich; ein 0,5 m breiter Randstreifen wird nicht berücksichtigt.“
**Leuchten im Bild:** OG-009 aufheller
**Linien:** keine (Textseite)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B6CF · OG-009 = RIVO_Aufheller_Variante rot 0° nahe Kennung (295 mm) — deckt sich mit F-Block (STANDARD_SPOT -> RIVO_Aufheller_Variante, Drehung 0°).
**Bewertung:** neu → Offene Cluster-/MFU-Flächen: Antipanik FLÄCHENBEZOGEN bewerten (freie Boden-Kernfläche nach EN 1838 4.3, 0,5-m-Randstreifen ausgenommen), nicht nur Weg unter der Leuchte; danach Anschluss an den Rettungsweg prüfen — Erweiterung von NB-R10/NB-R23 auf Schul-Lernlandschaften.

## S.170 · OG — F-OG-08 Einzelbezüge — OG-009 Typ B
**Bereich:** nördliche offene MFU
**Bild:** Einzelbezug-Seite mit Detailausschnitt: grüner Aufheller-Spot OG-009 mit orangem Kreis in der MFU (Raumstempel MUFU, OG.1.1.2). Beleuchtende AP-/Aufhellerposition; Personen kommen aus verschiedenen angrenzenden Raumtüren in die gemeinsame offene Fläche. Runde, richtungsfreie AP-Spot-Darstellung.
> „Eine Lichtachse ist keine Fluchtrichtungsangabe.“
> „Personen kommen aus verschiedenen angrenzenden Raumtüren und bewegen sich in der gemeinsamen offenen Fläche.“
> „Beleuchtung durch geschlossene Wände ist nicht nachgewiesen.“
**Leuchten im Bild:** OG-009 aufheller
**Personen:** aus verschiedenen angrenzenden Raumtüren
**Linien:** oranger Markierungskreis um OG-009
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B6CF · RIVO_Aufheller_Variante rot 0°, Kennungstext OG-009 295 mm daneben auf Layer RIVO_ERK_KENNUNG — konsistent.
**Bewertung:** bestaetigt:NB-R10

## S.171 · OG — F-OG-09 1.34 Projektraum mit westlicher Tür
**Bereich:** Projektraum 1.34 östlich der MFU
**Bild:** Grundrissausschnitt: Projektraum 1.34 mit seitlicher Westtür (orange eingerahmt), Tür-RZ OG-005 in der Türzone, Aufheller OG-006 im Raum. Person P1 mit grün gestrichelter Weginterpretation nach Westen durch die Tür und türkiser 2D-Sichtlinie auf OG-005. Darunter Räume 1.33 Ruheraum und 1.32 Bspraum.
> „Eine Person nähert sich aus dem Raum von Osten und blickt auf die Westwand.“
> „OG-005 ist um 90° gedreht und hat die Front nach Osten in den Raum. Von der MFU aus ist seine Rückseite keine Wegweisung in den Raum.“
> „Durch die bezeichnete Tür erreicht sie die MFU und danach den südlichen Gang.“
**Leuchten im Bild:** OG-005 down, OG-006 aufheller
**Personen:** P1 aus Raum 1.34 von Osten
**Linien:** grün gestrichelt: Fluchtweg nach Westen durch die Tür; türkis gestrichelt: 2D-Sichtlinie P1->OG-005; orange: markierte Türzone
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B806, 1B7EC · OG-005 = RIVO_ARR_down rot 90° (400 mm neben Kennung), OG-006 = RIVO_Aufheller_Variante rot 0° (258 mm) — beide decken sich mit F-Block.
**Bewertung:** bestaetigt:NB-R01

## S.172 · OG — F-OG-09 1.34 Projektraum mit westlicher Tür (E-J)
**Bereich:** Projektraum 1.34
**Bild:** Textseite: Türpfeil OG-005 übernimmt die Orientierung, Aufheller OG-006 die Beleuchtungsaufgabe. Symboltausch OG-005 STANDARD_RZ_PU -> RIVO_ARR_down Drehung 90°, OG-006 STANDARD_SPOT -> RIVO_Aufheller_Variante 0°. Warnung: Übernahme der 180°-Drehung aus dem Nachbar-Nordraum würde die Front an der falschen Türseite ausrichten. Normbezüge A01/A03/A04/A09.
> „Gleiche Nutzung bedeutet nicht gleiche Symbolrotation; entscheidend sind Türwand und Ankunft.“
> „Eine Übernahme der 180°-Drehung aus dem benachbarten Nordraum würde hier die Front an der falschen Seite der Tür ausrichten.“
> „Der Türpfeil übernimmt die Orientierung, der Aufheller die Beleuchtungsaufgabe.“
**Leuchten im Bild:** OG-005 down, OG-006 aufheller
**Linien:** keine (Textseite)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B806, 1B7EC · Drehungen 90°/0° im Inventar bestätigt.
**Bewertung:** bestaetigt:NB-R01

## S.173 · OG — F-OG-09 Einzelbezüge — OG-005 Typ H, OG-006 Typ B
**Bereich:** Projektraum 1.34, Westtür
**Bild:** Zwei Einzelbezüge mit Detailausschnitten: OG-005 als Tür-RZ am westlichen Ausgang (Front nach Osten in den Raum, Zeichenfront und Pfeil im Plan +X bei Blockrotation 90°); OG-006 als richtungsfreier Aufheller im Raum, der Licht zur Westtür liefert. Arbeitsteilung Türzeichen vs. Raumlicht explizit benannt.
> „Türzeichen am westlichen Ausgang des Projektraums 1.34; Front nach Osten in den Raum.“
> „Personen im Raum benötigen Licht zur westlichen Tür OG-005; das Symbol trägt keine Richtungsinformation.“
> „RIVO_ARR_down; Blockrotation 90°. Zeichenfront im Plan: rechts (+X).“
**Leuchten im Bild:** OG-005 down, OG-006 aufheller
**Personen:** aus 1.34 von Osten
**Linien:** orange Markierungskreise um OG-005 bzw. OG-006
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B806, 1B7EC · konsistent (down rot 90 = Welt-Pfeil 0°/+X; Aufheller rot 0).
**Bewertung:** bestaetigt:NB-R07

## S.174 · OG — F-OG-10 Serverraum 2: Ausgangszeichen ohne Lichtnachweis
**Bereich:** Serverraum 2 (1.31.1) westlich von TH 3, mit AR Lehrmittel 1.31 und Putzraum 1.30
**Bild:** Grundrissausschnitt: kleine verwinkelte Ausgangssituation von Serverraum 2 mit orange eingerahmter Tür und Tür-RZ OG-002. Wartungspersonal kommt aus dem Serverraum; Rack-/Schrankstellung nicht dargestellt. Weiterführung zu TH 3 muss über Tür-/Zugangsplan bestätigt werden — keine Verbindung durch Putzraum oder Schacht erfinden.
> „Der erste sichere Schritt ist der reale Türdurchgang in den angrenzenden Bereich.“
> „eine Verbindung durch Putzraum oder Schacht wird nicht erfunden.“
> „Das Bestandszeichen ist bei 90° nach Osten frontal. Ob diese Front zur tatsächlichen Tür-/Montagesituation passt, ist ... gesondert zu prüfen.“
**Leuchten im Bild:** OG-002 down
**Personen:** Wartungspersonal aus dem Serverraum
**Linien:** orange: markierte kleine Türsituation; grün gestrichelt/türkis laut Legende (im Ausschnitt nur angedeutet)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 70A9A · OG-002 = RIVO_ARR_down rot 90° (Welt-Pfeil 0°/+X), 400 mm neben Kennung — deckt sich mit Bestandsfront nach Osten.
**Bewertung:** bestaetigt:NB-R19

## S.175 · OG — F-OG-10 Serverraum 2 (E-J)
**Bereich:** Serverraum 2 westlich TH 3
**Bild:** Textseite: RIVO-Block übernimmt Lage und 90° unverändert; ein eigener SL-Block im Serverraum fehlt in der Zielmenge — das RZ beweist keine Arbeits- oder Rettungswegbeleuchtung. Drehen auf 180° ohne Tür-/Montageabgleich wäre eine Planänderung ohne belastbare Grundlage. Normbezug A06 (OVE E 8101 718.560.9.001.AT) mit Klarstellung: die 60-m²-Regel in Ziffer 3 betrifft NUR verkehrstechnische Einrichtungen, keine pauschale Schwelle für Schulräume.
> „Das Zeichen ohne Tür-/Montageabgleich einfach auf 180° zu drehen wäre eine Planänderung ohne belastbare Grundlage.“
> „Eine unsichere kleine Türsituation als eigenen Fall behandeln und die Bestandsinformation erhalten.“
> „Ziffer 3 ist ausdrücklich auf verkehrstechnische Einrichtungen begrenzt und begründet keine pauschale 60-m²-Schwelle für Schulräume.“
**Leuchten im Bild:** OG-002 down
**Linien:** keine (Textseite)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 70A9A · Lage und Drehung 90° im Inventar unverändert bestätigt.
**Bewertung:** neu → Bestandsübernahme-Prozessregel: Bestands-RZ bei unsicherer Tür-/Montagesituation UNVERÄNDERT übernehmen (keine Rotation ohne belastbare Grundlage), Situation als eigenen offenen Fall führen — generalisiert die NB-R18-Prozessregel 'unklar -> niemals raten' vom Zuordnungs- auf den Bestands-Symbolfall. Zusatz: RZ im Raum beweist keine SL-Abdeckung (Rolle RZ ≠ Beleuchtungsnachweis).

## S.176 · OG — F-OG-10 Einzelbezüge — OG-002 Typ H
**Bereich:** Serverraum 2, kleine verwinkelte Ausgangssituation
**Bild:** Einzelbezug mit Detailausschnitt: OG-002 mit orangem Kreis an der Serverraum-Tür zwischen 1.31.1 und Putzraum 1.30. Einzelner lokaler Raumtürbezug ohne erfasste eigene SL im Raum; nicht Teil der gegenüberliegenden TH-3-Podestzeichen. CAD-Konvention: Blockrotation 90°, Zeichenfront und Pfeil +X.
> „Einzelner lokaler Raumtürbezug ohne erfasste eigene SL im Raum; nicht Teil der gegenüberliegenden TH-3-Podestzeichen.“
> „Tür-/Montagedetail, Rackstellung und Weiterführung zu TH 3 sind offen. Keine Verbindung durch Putzraum oder Schacht erfinden.“
**Leuchten im Bild:** OG-002 down
**Personen:** Wartungspersonal aus dem Serverraum
**Linien:** oranger Markierungskreis um OG-002
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 70A9A · konsistent (down rot 90, Kennungsabstand 400 mm).
**Bewertung:** bestaetigt:NB-R19

## S.177 · OG — F-OG-11 Mittlerer Knoten: Westankunft und Querankunft
**Bereich:** zentraler Gangknoten am Zugang zu den WC-Nebenräumen (u.a. 1.28 Barrierefreies WC)
**Bild:** Grundrissausschnitt des mittleren Knotens: Aufheller OG-020 im Gang westlich, dicht daneben zwei unterschiedliche RZ — OG-021 (einseitig, Front West) und OG-022 (beidseitig, Fronten Nord/Süd, Pfeile Ost). Grün gestrichelte Weginterpretation läuft von West nach Ost durch den Knoten, Personensymbol mit türkiser Sichtannahme im Gang. Die zwei Blöcke sind explizit keine identischen Dubletten.
> „Am Zugang zu den WC-Nebenräumen stehen zwei unterschiedliche RZ dicht nebeneinander.“
> „Die Längsankunft kommt aus Westen; Querankünfte kommen aus Norden bzw. Süden.“
> „OG-021 hat bei 270° Front nach Westen. OG-022 bei 180° hat Fronten Nord/Süd und Pfeile nach Osten. Die zwei Blöcke sind daher keine identischen Dubletten.“
**Leuchten im Bild:** OG-020 aufheller, OG-021 down, OG-022 beidseitig
**Personen:** Längsankunft aus Westen (Hauptgang), Querankünfte aus Norden bzw. Süden
**Linien:** grün gestrichelt: Fluchtweg West->Ost durch den Knoten; türkis gestrichelt: 2D-Sichtannahme; orange laut Legende
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B6E9, 1B618, 1B509 · OG-020 = Aufheller rot 0° (331 mm, ok); OG-022 = RIVO_ARR_bothsided rot 180° (306 mm, ok). OG-021 (laut PDF RIVO_ARR_down rot 270°) hat im Leuchten-Inventar KEINEN passenden Treffer nahe der Kennung — einziger down rot 270° liegt 55 m entfernt (1B5F9); nächster down (1B509, 2257 mm) hat rot 0°. ? Inventar-Lücke oder Extraktions-Differenz am Knoten.
**Bewertung:** bestaetigt:NB-R16

## S.178 · OG — F-OG-11 Mittlerer Knoten (E-J)
**Bereich:** zentraler Gangknoten
**Bild:** Textseite: getrennte Erfassung von OG-021 und OG-022 erhält beide Sichtaufgaben; eine Zusammenlegung könnte eine Ankunftsrichtung ohne frontal lesbare Fläche lassen. Symboltausch: OG-020 SPOT->Aufheller 0°, OG-021 RZ_PU->ARR_down 270°, OG-022 RZ_PLPR->ARR_bothsided 180°. Normbezug A02 betont: An Kreuzungen muss die Sicherheitsleuchte beide Richtungen ausleuchten — das ist keine pauschale Forderung nach einem bestimmten RZ-Block.
> „Ein Zeichenpaar anhand seiner Fronten und Ankünfte erklären, nicht nur nach seiner Nähe sortieren.“
> „Eine Zusammenlegung könnte eine der beiden Ankunftsrichtungen ohne frontal lesbare Fläche lassen.“
> „Bei Richtungsänderungen und Kreuzungen muss die Sicherheitsleuchte beide Richtungen ausleuchten; dies ist keine pauschale Forderung nach einem bestimmten RZ-Block.“
**Leuchten im Bild:** OG-020 aufheller, OG-021 down, OG-022 beidseitig
**Linien:** keine (Textseite)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B6E9, 1B618 · OG-020/OG-022 bestätigt; OG-021-Drehung 270° im Inventar nicht verifizierbar (siehe S.177).
**Bewertung:** bestaetigt:NB-R07

## S.179 · OG — F-OG-11 Einzelbezüge — OG-020 Typ C, OG-021 Typ H
**Bereich:** mittlerer Hauptgang / zentraler Gangdurchgang
**Bild:** Zwei Einzelbezüge: OG-020 als Aufheller im mittleren Hauptgang westlich des Knotens (Lichtanteil der Dreiergruppe mit OG-021/OG-022); OG-021 als einseitiges Zeichen am zentralen Gangdurchgang mit Front nach Westen (Blockrotation 270°, Zeichenfront und Pfeil -X), auf das Personen aus dem westlichen Hauptgang frontal zukommen.
> „Lichtanteil der Gruppe mit Übergangszeichen OG-021 und Knotenzeichen OG-022.“
> „Einseitiges Zeichen am zentralen Gangdurchgang; Front nach Westen.“
> „Personen aus dem westlichen Hauptgang kommen frontal auf das Zeichen zu.“
**Leuchten im Bild:** OG-020 aufheller, OG-021 down
**Personen:** aus dem westlichen Hauptgang
**Linien:** orange Markierungskreise um OG-020 bzw. OG-021
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B6E9, 1B509 · OG-020 ok. OG-021: kein down-Block rot 270° nahe der Kennung im Inventar (nächster down 1B509 rot 0°, 2257 mm) — ? nicht bestätigt.
**Bewertung:** bestaetigt:NB-R07

## S.180 · OG — F-OG-11 Einzelbezüge — OG-022 Typ H
**Bereich:** mittlerer Knoten
**Bild:** Einzelbezug: beidseitiges Zeichen OG-022 am mittleren Knoten, Blockrotation 180°, Zeichenfronten +Y/-Y (Nord/Süd), grafischer Pfeil +X (Ost). Personen aus nördlichen und südlichen Anschlussbereichen sehen unterschiedliche Fronten; die westliche Längsankunft kann seitlich sein. Warnung: keine Rundumsicht unterstellen, Blickpunkte je Ankunft einzeln zeigen.
> „Beidseitiges Zeichen am mittleren Knoten; Fronten Nord/Süd, Pfeile nach Osten.“
> „Die tatsächlichen Blickpunkte am Knoten und der nächste erkennbare Wegpunkt müssen je Ankunft gezeigt werden; keine Rundumsicht unterstellen.“
> „Personen aus nördlichen und südlichen Anschlussbereichen sehen unterschiedliche Fronten; westliche Längsankunft kann seitlich sein.“
**Leuchten im Bild:** OG-022 beidseitig
**Personen:** aus nördlichen und südlichen Anschlussbereichen, westliche Längsankunft
**Linien:** oranger Markierungskreis um OG-022
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B618 · RIVO_ARR_bothsided rot 180° 306 mm neben Kennung — deckt sich exakt mit F-Block.
**Bewertung:** bestaetigt:NB-R16

## S.181 · OG — F-OG-12 Barrierefreies WC und Personal-WC — Ort/Person/Folge/Front (A-D)
**Bereich:** Nördlich des Hauptgangs: WC Pädagogik 1.29, westlicher Stichgang, barrierefreies WC 1.28
**Bild:** Planausschnitt mit WC Päd 1.29 (OG-010 als grüner Spot im Stichgang-Anschluss) und Barrierefreiem WC 1.28 (OG-015 als grüner Spot im Raum). Räume mit Türbeschriftungen 90/210 bzw. 100/210; unten am Hauptgang zwei grüne RZ-Blöcke. Keine Personenmarken im Ausschnitt sichtbar.
> „Diese beiden Ankünfte dürfen nicht als gemeinsame Stichgangfolge beschrieben werden.“
> „Zwischen den WC-Räumen wird keine Verbindung durch die Trennwand angenommen. Für 1.28 wird kein Umweg durch den Stichgang erfunden.“
> „Beide Leuchten sind ohne Rettungszeichen. Eine Front-/Rückseitenprüfung betrifft hier die benachbarten RZ am Knoten, nicht diese Lichtpunkte.“
**Leuchten im Bild:** OG-010 aufheller, OG-015 aufheller
**Personen:** WC Pädagogik 1.29 (durch westliche Tür in den Stichgang, dann nach Süden zum Hauptgang), barrierefreies WC 1.28 (durch südliche Tür direkt in den Hauptgang)
**Linien:** keine sichtbaren Weglinien/Personenmarken im Ausschnitt; nur OG-010/OG-015-Kennzeichnungen
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Kennungen OG-010/OG-015 aus Seitentext
**Bewertung:** neu → Benachbarte Sanitärräume nie als gemeinsame Fluchtfolge lesen: keine angenommene Verbindung durch Trennwände, kein erfundener Umweg; jede Tür erhält ihre eigene Ankunftsfolge. Leuchten ohne RZ-Front (SL/AP-Spots) sind von der Front-/Rückseitenprüfung ausgenommen.

## S.182 · OG — F-OG-12 Barrierefreies WC und Personal-WC — Begründung/CAD-Zuordnung/Normbezug (E-J)
**Bereich:** WC Pädagogik 1.29 + Stichgang + barrierefreies WC 1.28
**Bild:** Reine Textseite (Abschnitte E-J) ohne Planausschnitt. Symboltausch OG-010 (STANDARD_SPOT_SL -> RIVO_Aufheller_Variante, 90°->90°) und OG-015 (STANDARD_SPOT -> RIVO_Aufheller_Variante, 0°). Normbezüge A03, A05 (AP-Pflicht barrierefreies WC), A06 (OVE Sanitär ab 8 m²), A18 (Rufanlagen/Schutzbereiche), A19 (Zwischenweg-Beleuchtung). Offene Nachweise in Orange (Abschnitt I).
> „A05 — ÖNORM EN 1838, 4.3.8: Toiletten für Menschen mit Behinderung benötigen Antipanikbeleuchtung. Diese Klausel nennt keine 8-m²-Grenze und gilt nicht automatisch für jeden barrierefreien Raum.“
> „A06 — OVE E 8101, 718.560.9.001.AT: Bei erhöhten Anforderungen zusätzlich Sanitärbereiche ab 8 m², barrierefreie WC-Anlagen und bezeichnete Elektro-/Sicherheitszentralen prüfen. Ziffer 3 ist ausdrücklich auf verkehrstechnische Einrichtungen begrenzt und begründet keine pauschale 60-m²-Schwelle für Schulräume.“
> „A19 — ÖNORM EN 1838, 4.3.9: Ist Sicherheitsbeleuchtung in einem Raum erforderlich und besteht kein direkter Zugang zu den Rettungswegen im angrenzenden Brandabschnitt, muss auch der dazwischenliegende Rettungsweg beleuchtet werden.“
> „Problematisch wäre, den Punkt im Stichgang als Nachweis für den Lichtwert im getrennten barrierefreien WC oder als Richtungspfeil zu lesen.“
**Leuchten im Bild:** OG-010 aufheller, OG-015 aufheller
**Linien:** keine (Textseite); orange Hinweistexte in Abschnitt I
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Symboltausch- und Rotationsangaben aus Abschnitt F
**Bewertung:** neu → Barrierefreie WCs benötigen Antipanikbeleuchtung (EN 1838 4.3.8, ohne 8-m²-Grenze, aber nur echte Behinderten-Toiletten); Sanitärbereiche ab 8 m² nur bei erhöhten Anforderungen prüfen (OVE E 8101 718.560.9.001.AT); Raum ohne direkten Rettungswegzugang -> dazwischenliegenden Weg mitbeleuchten (4.3.9). Kein Regelgehalt aus der Symbolform ableiten.

## S.183 · OG — F-OG-12 Einzelbezüge — OG-010 (Typ D) und OG-015 (Typ C)
**Bereich:** Stichgang WC Pädagogik 1.29 und barrierefreies WC 1.28
**Bild:** Zwei DXF-Detailausschnitte mit orangem Markierungskreis. Oben OG-010: grüner Spot im Stichgang zwischen Absaugraum 1.32 und WC Päd 1.29 (F.OG.I.05, FPH 85). Unten OG-015: grüner Spot im barrierefreien WC 1.28 (Metalldecke, Fliesen), südliche Tür 100/210 zum Hauptgang.
> „Bestandsdrehung 90°, neue Blockdrehung 90°; eine Leuchtenachse ist kein Rettungszeichenpfeil.“
> „Runde, richtungsfreie AP-Spot-Darstellung; Produkt-/Montagedaten bleiben in Attributen erhalten. Eine Lichtachse ist keine Fluchtrichtungsangabe.“
> „Die 90-Grad-Bestandsachse, gerichtete Produktoptik und Lichtabdeckung der verschiedenen Türvorbereiche bleiben gesondert zu prüfen.“
> „Ausstattung, freie Bewegungsflächen und Innenraumlichtnachweis sind offen; das Ganglicht ersetzt sie nicht.“
**Leuchten im Bild:** OG-010 aufheller, OG-015 aufheller
**Personen:** WC Pädagogik 1.29, barrierefreies WC 1.28
**Linien:** orange Markierungskreise um OG-010 und OG-015; keine Weglinien
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Rotationen 90°/0° und Blocknamen aus Seitentext
**Bewertung:** bestaetigt:NB-R10

## S.184 · OG — F-OG-13 Sanitärbereiche unter TH 3 — Ort/Person/Folge/Front (A-D)
**Bereich:** Sanitärraum D 1.26 (Damen) und Sanitärraum 1.25 (Herren) zwischen TH 3 und Hauptgang
**Bild:** Planausschnitt mit beiden Sanitärräumen: AP-Aufheller OG-011 (Damen) und OG-012 (Herren) im Rauminneren, Tür-RZ OG-023 und OG-025 an den südlichen Türen (orange umrahmt), Aufheller OG-024 im Gang südlich davor. Personenmarken P1/P2 mit grün gestrichelten Wegen nach Süden durch die jeweilige Tür. Rechts E-Schacht, Lift 1, HT Schacht.
> „Je ein RZ markiert die südliche Tür, je ein AP-Aufheller liegt im Raum. OG-024 sitzt im Gang.“
> „Personen kommen aus Kabinen und Waschzonen auf ihre eigene Tür zu. Der benachbarte Sanitärraum bleibt durch eine Wand getrennt.“
> „Die Raumtür ist ein lokaler Schritt, noch kein letzter Ausgang.“
> „Beide Türzeichen sind bei 180° frontal aus Norden sichtbar. Gangbenutzer sehen die Rückseiten. OG-024 besitzt keine Zeichenfront.“
**Leuchten im Bild:** OG-011 aufheller, OG-012 aufheller, OG-023 down, OG-024 aufheller, OG-025 down
**Personen:** P1: Damen-Sanitärraum 1.26 (Kabinen/Waschzone), P2: Herren-Sanitärraum 1.25 (Kabinen/Waschzone)
**Linien:** grün gestrichelte Wege von P1/P2 nach Süden durch die Türen in den Gang; orange Rechtecke um die Türbereiche OG-023/OG-025
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Kennungen OG-011/012/023/024/025 aus Seitentext
**Bewertung:** bestaetigt:NB-R01

## S.185 · OG — F-OG-13 Sanitärbereiche unter TH 3 — Begründung/CAD-Zuordnung/Normbezug (E-J)
**Bereich:** Sanitärräume 1.25/1.26 unter TH 3 + gemeinsamer Gang
**Bild:** Reine Textseite (E-J). Symboltausch: OG-011/012 STANDARD_SPOT -> RIVO_Aufheller_Variante 0°; OG-023/025 STANDARD_RZ_PU -> RIVO_ARR_down 180°; OG-024 STANDARD_SPOT_SL -> RIVO_Aufheller_Variante 0°. Normbezüge A01, A03, A06 (Sanitär ab 8 m²), A09 (Erkennungsweite l=z×h). Offener Nachweis: Kabinenabschattung, Raumflächen, Beleuchtungsstärken.
> „Die Lage von OG-024 erklärt die gemeinsame Türvorbereichsbeleuchtung, nicht die Ausleuchtung hinter den Raumwänden oder Kabinentrennungen.“
> „Eine gemeinsame Leuchte über der mittleren Trennwand wäre ohne nachgewiesene Lichtdurchgänge keine gleichwertige Lösung.“
> „A09 — Erkennungsweite l = z × h; z=100 für extern beleuchtete, z=200 für hinterleuchtete Zeichen. Bedingung: Reale Zeichenhöhe und Bauart; keine Umrechnung aus der grafischen Größe eines CAD-Symbols.“
> „Die Türfolge jedes Sanitäraums getrennt lesen und die Gangbeleuchtung danach anschließen.“
**Leuchten im Bild:** OG-011 aufheller, OG-012 aufheller, OG-023 down, OG-024 aufheller, OG-025 down
**Linien:** keine (Textseite); orange Hinweistext in Abschnitt I
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Symboltausch- und Drehungsangaben aus Abschnitt F
**Bewertung:** neu → Ein Gang-Aufheller vor mehreren Türen deckt nur die gemeinsamen Türvorbereiche, nie die Innenräume hinter Wänden/Kabinentrennungen; eine gemeinsame Leuchte über einer Trennwand ist ohne nachgewiesenen Lichtdurchgang keine gleichwertige Lösung. Sanitärbereiche ab 8 m² nur bei erhöhten Anforderungen prüfen (OVE, A06).

## S.186 · OG — F-OG-13 Einzelbezüge — OG-011 (Typ C) und OG-012 (Typ C)
**Bereich:** Damen-Sanitärraum 1.26 (West) und Herren-Sanitärraum 1.25 (Ost)
**Bild:** Zwei DXF-Detailausschnitte mit orangem Kreis. Oben OG-011: grüner AP-Spot im westlichen Damen-Sanitärraum neben WC geschlechtsneutral 1.27; unten grünes Tür-RZ am Raumausgang. Unten OG-012: grüner AP-Spot im östlichen Herren-Sanitärraum nahe E-Schacht/Lift 1; unten grünes Tür-RZ.
> „Personen im Raum müssen bis zur südlichen Tür OG-023 Licht haben.“
> „STANDARD_SPOT -> RIVO_Aufheller_Variante; Blockrotation 0°. Runde, richtungsfreie AP-Spot-Darstellung; Produkt-/Montagedaten bleiben in Attributen erhalten. Eine Lichtachse ist keine Fluchtrichtungsangabe.“
> „WC-Trennwände und Einbauten können Abschattungen verursachen; der Innenraumnachweis fehlt.“
> „Trennwände, Einbauten und Abdeckung bis zur Südseite sind ohne Photometrie nicht bestätigt.“
**Leuchten im Bild:** OG-011 aufheller, OG-012 aufheller
**Personen:** innere Sanitärbereiche (Kabinen/Waschzonen) beider Räume
**Linien:** orange Markierungskreise um OG-011 und OG-012; keine Weglinien
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Blockrotationen aus Seitentext
**Bewertung:** bestaetigt:NB-R10

## S.187 · OG — F-OG-13 Einzelbezüge — OG-023 (Typ H) und OG-024 (Typ D)
**Bereich:** Südlicher Ausgang Damen-Sanitärraum + Gang vor beiden Sanitärausgängen
**Bild:** Zwei DXF-Detailausschnitte mit orangem Kreis. Oben OG-023: grünes Tür-RZ raumseitig an der südlichen Tür des Damen-Sanitärraums, darunter im Gang der grüne Spot OG-024. Unten OG-024: grüner Aufheller-Spot im Gang zwischen den beiden Sanitärtüren, umliegend zwei weitere grüne RZ am Gang.
> „Türzeichen am südlichen Ausgang des westlichen Damen-Sanitärraums; Front nach Norden.“
> „RIVO_ARR_down; Blockrotation 180°. Zeichenfront im Plan: oben (+Y). Grafischer Pfeil im Plan: oben (+Y). Dies beschreibt die CAD-Konvention; Personenbewegung und reales Piktogramm sind getrennt zu prüfen.“
> „Gemeinsame äußere Türvorbereichsbeleuchtung; OG-011/012 beleuchten die getrennten Innenräume.“
> „Gerichtete Produktoptik und Überdeckung beider Türvorbereiche sind offen; die Achse des Bestandsprodukts ist kein Fluchtrichtungspfeil.“
**Leuchten im Bild:** OG-023 down, OG-024 aufheller
**Personen:** Sanitärbereiche (Damenraum), Gangbenutzer
**Linien:** orange Markierungskreise um OG-023 und OG-024; keine Weglinien
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Rotation 180° und Front +Y aus Seitentext
**Bewertung:** bestaetigt:NB-R01

## S.188 · OG — F-OG-13 Einzelbezüge — OG-025 (Typ H)
**Bereich:** Südlicher Ausgang Herren-Sanitärraum 1.25
**Bild:** Ein DXF-Detailausschnitt mit orangem Kreis um OG-025: grünes Tür-RZ raumseitig an der südlichen Tür des Herren-Sanitärraums (90/210), rechts HT Schacht. Front laut Text nach Norden (ins Rauminnere).
> „Türzeichen am südlichen Ausgang des östlichen Herren-Sanitärraums; Front nach Norden.“
> „Personen aus dem Herrenraum kommen von innen auf die Türfront zu.“
> „RIVO_ARR_down; Blockrotation 180°. Zeichenfront im Plan: oben (+Y). Grafischer Pfeil im Plan: oben (+Y).“
> „Türblatt und innere Trennwände können die Sicht beeinflussen; der Ganglichtpunkt OG-024 liefert dafür keinen Sichtnachweis.“
**Leuchten im Bild:** OG-025 down
**Personen:** Herren-Sanitärraum 1.25
**Linien:** oranger Markierungskreis um OG-025; keine Weglinien
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Rotation 180° und Front +Y aus Seitentext
**Bewertung:** bestaetigt:NB-R01

## S.189 · OG — F-OG-14 Sozialraum und Teamraum: reine Türkennzeichnung — Ort/Person/Folge/Front (A-D)
**Bereich:** Sozialraum inkl. Küche 1.24 und Teamraum 1.23 südlich des mittleren Gangs
**Bild:** Planausschnitt: Tür-RZ OG-033 (Sozialraum) und OG-034 (Teamraum) an den nördlichen Türen zum Gang; Personenmarken P1/P2 südlich davon mit grün gestrichelten Pfeilen nach Norden auf die Türen. Links oben zwei grüne RZ-Blöcke am Gang, rechts oben ein grüner Spot. Unten Fassadenbeschriftungen (RPH/FPH, F.OG.33/34).
> „Die zwei erfassten Positionen sind Rettungszeichen an den nördlichen Türen.“
> „Der lokale Weg führt über die jeweilige Tür nach Norden und danach zur festgelegten Stiege. Er wird nicht durch den Nachbarraum abgekürzt.“
> „OG-033/034 sind bei 0° mit der Front nach Süden ausgerichtet. Sie bedienen die Raumankunft und keine vom Gang ausgehende Suche nach dem Raum.“
**Leuchten im Bild:** OG-033 down, OG-034 down
**Personen:** P1: Sozialraum inkl. Küche 1.24, P2: Teamraum 1.23
**Linien:** grün gestrichelte Pfeile von P1/P2 nach Norden durch die jeweilige Tür in den Gang
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Kennungen OG-033/OG-034 aus Seitentext
**Bewertung:** bestaetigt:NB-R01

## S.190 · OG — F-OG-14 Sozialraum und Teamraum — Begründung/CAD-Zuordnung/Normbezug (E-J)
**Bereich:** Sozialraum inkl. Küche 1.24 und Teamraum 1.23
**Bild:** Reine Textseite (E-J). Symboltausch: OG-033/034 STANDARD_RZ_PU -> RIVO_ARR_down, Drehung 0°, lagegleich ersetzt. Normbezüge A01, A03, A04 (Antipanik 0,5 lx), A08 (besondere Gefährdung: 10 % Wartungswert, mind. 15 lx, Uo>=0,1, 0,5 s). Offener Nachweis in Orange: Raumbeleuchtung, Küchennutzung, Möbel, Montagehöhen.
> „Eine weitere eigene SL im Inneren dieser Räume ist in der erfassten Zielmenge nicht enthalten; das wird als Prüfpunkt dokumentiert.“
> „Ein Aufheller in einer anderen MFU kann hinter geschlossener Wand nicht ohne Lichtnachweis mitgerechnet werden.“
> „A08 — Bei besonderer Gefährdung: auf der Arbeitsfläche mindestens 10 % des für die Aufgabe erforderlichen Wartungswerts und mindestens 15 lx; Gleichmäßigkeit Uo mindestens 0,1. Bedingung: Gefährdungsbeurteilung für z. B. Werk-/Küchenbereich erforderlich; kein Automatismus allein aus Raumname.“
> „Eine vollständige RZ-Erfassung kann mit einer unvollständigen Beleuchtungsgrundlage zusammentreffen.“
**Leuchten im Bild:** OG-033 down, OG-034 down
**Linien:** keine (Textseite); orange Hinweistext in Abschnitt I
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Symboltausch- und Drehungsangaben aus Abschnitt F
**Bewertung:** neu → Küchen-/Werkbereiche: Sicherheitsbeleuchtung für besondere Gefährdung nur über Gefährdungsbeurteilung (EN 1838 4.4: >=10 % Wartungswert, >=15 lx, Uo>=0,1, 0,5 s), nie automatisch aus dem Raumnamen. Fehlende Raum-SL in der Zielmenge als expliziten Prüfpunkt dokumentieren statt stillschweigend zu ergänzen.

## S.191 · OG — F-OG-14 Einzelbezüge — OG-033 (Typ H) und OG-034 (Typ H)
**Bereich:** Nördliche Türen von Sozialraum 1.24 und Teamraum 1.23
**Bild:** Zwei DXF-Detailausschnitte mit orangem Kreis. Oben OG-033: grünes Tür-RZ an der nördlichen Sozialraumtür (90/210), links oben zwei RZ-Blöcke des Gangs. Unten OG-034: grünes Tür-RZ an der nördlichen Teamraumtür (Raum 1.23), rechts oben ein grüner Spot (OG-035 in anderer MFU).
> „Türzeichen am nördlichen Ausgang des Sozialraums inklusive Küche; Front nach Süden.“
> „RIVO_ARR_down; Blockrotation 0°. Zeichenfront im Plan: unten (-Y). Grafischer Pfeil im Plan: unten (-Y). Dies beschreibt die CAD-Konvention; Personenbewegung und reales Piktogramm sind getrennt zu prüfen.“
> „Eigene Raum-SL ist in der Zielmenge nicht erfasst. Küche, Möblierung und Innenraumbeleuchtung benötigen einen getrennten Nachweis.“
> „Separater Tür- und Raumbezug gegenüber OG-033; kein Lichtnachweis durch OG-035 außerhalb des Raums.“
**Leuchten im Bild:** OG-033 down, OG-034 down
**Personen:** geschlossener Sozialraum 1.24 bzw. Teamraum 1.23
**Linien:** orange Markierungskreise um OG-033 und OG-034; keine Weglinien
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Rotation 0° und Front -Y aus Seitentext
**Bewertung:** bestaetigt:NB-R01

## S.192 · OG — F-OG-15 TH 3 und Anschluss aus der östlichen MFU — Ort/Person/Folge/Front (A-D)
**Bereich:** Treppenhaus TH 3 (Raumcode 4.3.2) mit Podesten und östlicher Zugangssituation zur MFU
**Bild:** Planausschnitt TH 3 mit Treppenläufen und Treppenauge; Podest-RZ OG-001 (oben am nördlichen Podest) und OG-007 (unten am südlichen Podest) gegenüberliegend, beidseitiges RZ OG-008 östlich an der Zugangssituation zur MFU. Links Serverraum 2 1.31.1, unten E-Schacht.
> „TH 3 besitzt die beiden gegenüberliegenden Podestzeichen OG-001/007. Das beidseitige OG-008 liegt östlich an der Zugangssituation.“
> „Ankünfte kommen aus der östlichen MFU und aus den Stiegenläufen. Der jeweilige Höhenstand ist bei der Deutung entscheidend.“
> „Der Grundriss zeigt das Treppenauge als Hindernis; der Wechsel der Läufe erfolgt über Podeste. Der konkrete Höhenverlauf bleibt bis zum Schnittabgleich offen.“
> „OG-001 bei 0° weist nach Westen, Front Süden; OG-007 bei 180° nach Osten, Front Norden. OG-008 hat Fronten Nord/Süd und Pfeile Westen. Die Ankunft von Osten kann dessen Schmalseite treffen.“
**Leuchten im Bild:** OG-001 left, OG-007 right, OG-008 beidseitig
**Personen:** östliche MFU, Stiegenläufe TH 3 (Höhenstand entscheidend)
**Linien:** keine Personenmarken/Weglinien im Ausschnitt; Kennzeichnungslinien zu OG-001/007/008
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht geprueft; Rotationen 0°/180° und Frontangaben aus Abschnitt D; Schmalseiten-Problem der Ost-Ankunft auf OG-008 im Text offen benannt
**Bewertung:** bestaetigt:NB-R16

## S.193 · OG — F-OG-15 TH 3 und Anschluss aus der östlichen MFU — Begründung/Normbezug
**Bereich:** TH 3 mit zwei gegenüberliegenden Stiegenabschnitten + östlicher MFU-Zugang
**Bild:** Reine Textseite (E-J) zum Fall F-OG-15. Drei Symboltausche werden dokumentiert: OG-001 und OG-007 als gegenläufige Podest-Richtungszeichen (RIVO_ARR_left, 0° bzw. 180°), OG-008 als beidseitiges Zeichen am östlichen Geschosszugang. Normbezüge A01/A02/A03/A09 (EN 1838); offene Nachweise: Höhenschnitt, MFU-Blick, Türstellungen, Stufenbeleuchtung.
> „Die beiden Podestzeichen zu einem Zeichen an der Tür zusammenzufassen könnte eine Richtungsumkehr im Abstieg unbeschildert lassen.“
> „Die Folge über mehrere Geschosse muss bis zur Außentür geprüft werden; ein Podestpfeil ist nur ein Teil davon.“
> „Eine eigenständige SL auf den Stiegenläufen ist in der Zielmenge nicht erfasst; direkte Stufenbeleuchtung bleibt nachzuweisen.“
**Leuchten im Bild:** OG-001 left, OG-007 left, OG-008 beidseitig
**Linien:** keine (Textseite)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · 
**Bewertung:** bestaetigt:NB-R04

## S.194 · OG — F-OG-15 Einzelbezüge — OG-001 / OG-007
**Bereich:** TH 3, nördlicher und südlicher Podest-/Laufabschnitt
**Bild:** Zwei Detail-Ausschnitte der RIVO-DXF. OG-001 (Typ I): RIVO_ARR_left, Rotation 0°, am nördlichen Stiegenabschnitt von TH 3, Front Süden, Pfeil Westen; orange Kreis markiert die Position. OG-007 (Typ I): RIVO_ARR_left, Rotation 180°, südlicher Gegenabschnitt, Front Norden, Pfeil Osten. Je Richtungsphase der Stiegenbewegung ein eigenes, gegenläufiges Podestzeichen.
> „Um 180 Grad gegenüber OG-001 gedreht; bedient die andere Richtungsphase der Stiegenbewegung.“
> „Die Person muss vom passenden südlichen Lauf-/Podestabschnitt kommen; der tatsächliche Höhenstand ist entscheidend.“
> „Architektur-Aufwärtspfeile allein legen keine Fluchtfolge fest.“
> „keine Verbindung über das Treppenauge zeichnen.“
**Leuchten im Bild:** OG-001 left, OG-007 left
**Personen:** südlicher Lauf-/Podestabschnitt (für OG-001) bzw. nördlicher Abschnitt (für OG-007)
**Linien:** orange Markierungskreise um die Symbolpositionen, keine Wegbehauptungslinien
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · 
**Bewertung:** bestaetigt:NB-R04

## S.195 · OG — F-OG-15 Einzelbezüge — OG-008
**Bereich:** östlicher Zugang zu TH 3 aus der MFU
**Bild:** Detail-Ausschnitt mit OG-008 (Typ H): RIVO_ARR_bothsided, Rotation 0°, am östlichen Geschosszugang zu TH 3; Fronten Nord und Süd, Pfeile nach Westen. Orange Kreis um die Position, Türmaße FPH 0 / 100-210 im Ausschnitt sichtbar. Wichtiger Hinweis: eine Person aus der östlichen MFU trifft eher die SCHMALSEITE — beidseitige Ausbildung erzeugt keine zusätzliche Ostfront.
> „Eine Person aus der östlichen MFU trifft eher die Schmalseite; beidseitige Ausbildung erzeugt keine zusätzliche Ostfront.“
> „der Balkon-/Dachbezug darf nicht zum sicheren Endpunkt erklärt werden.“
**Leuchten im Bild:** OG-008 beidseitig
**Personen:** östliche MFU
**Linien:** orange Markierungskreis, keine Wegbehauptung
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · 
**Bewertung:** bestaetigt:NB-R16

## S.196 · OG — F-OG-16 Bildungsraum Plus: nördliche Raumankunft — Ort/Person/Folge/Sicht
**Bereich:** Bildungsraum I - Plus (1.21) östlich von TH 3, südliche Ausgangstür zur MFU
**Bild:** Grundriss-Ausschnitt des großen Bildungsraums Plus mit Person P1 im Norden, grün gestrichelter Weginterpretation nach Süden zur Tür OG-027 (orange Rahmen) und türkiser 2D-Sichtlinie; OG-013 als Aufheller-Punkt mitten im Raum. Die Tür OG-027 trägt ein down-RZ bei 180° mit Front nach Norden in den Raum.
> „OG-027 ist bei 180° mit der Front nach Norden in den Raum gerichtet.“
> „Der nach oben wirkende CAD-Pfeil ist hier die gedrehte Darstellung eines Durchgangszeichens und keine Aufforderung, ein Geschoss aufwärts zu laufen.“
> „Durch die südliche Tür OG-027 gelangt man in die MFU. Von dort führt die zugewiesene Folge nach Westen zum TH-3-Anschluss.“
**Leuchten im Bild:** OG-013 aufheller, OG-027 down
**Personen:** P1, aus dem Raum von Norden (zwischen mobilen Möbeln/Gruppenarbeitsplätzen)
**Linien:** grün gestrichelt = Weginterpretation Nord->Süd zur Tür; türkis = angenommene 2D-Sicht; orange = markiertes Bauteil (Türbereich)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · 
**Bewertung:** bestaetigt:NB-R01

## S.197 · OG — F-OG-16 Bildungsraum Plus — Begründung/Normbezug
**Bereich:** Bildungsraum Plus (großer Unterrichtsraum) mit Raum-Aufheller + Tür-RZ
**Bild:** Textseite (E-J): OG-013 beleuchtet den Raum (STANDARD_SPOT -> RIVO_Aufheller_Variante, 0°), OG-027 markiert die Tür (STANDARD_RZ_PU -> RIVO_ARR_down, 180°). Die große Raumtiefe verlangt Prüfung der realen Erkennungsweite (A09: l = z x h) und der Flächenausleuchtung (A04 Antipanik 0,5 lx). Kernaussage: ein größer gezeichnetes CAD-Symbol erhöht NICHT die reale Zeichenhöhe/Erkennungsweite.
> „Ein größeres gezeichnetes Symbol erhöht nicht die reale Zeichenhöhe eines Produkts und damit nicht automatisch seine Erkennungsweite.“
> „Grafische Symbolgröße, reale Produkthöhe und Erkennungsweite sind drei getrennte Größen.“
> „Die große Raumtiefe verlangt eine Prüfung der realen Erkennungsweite und Flächenausleuchtung.“
**Leuchten im Bild:** OG-013 aufheller, OG-027 down
**Linien:** keine (Textseite)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · 
**Bewertung:** neu → Schul-Großraum (Bildungsraum/Cluster): Ausstattungsmuster = 1 AP-Aufheller im Raum + Tür-RZ (Front in den Raum, NB-R01); bei großer Raumtiefe Erkennungsweiten-Check l=z*h gegen reale Zeichenhöhe verpflichtend — grafische CAD-Symbolgröße, reale Produkthöhe und Erkennungsweite sind drei getrennte Größen (keine Kompensation durch größeres Symbol).

## S.198 · OG — F-OG-16 Einzelbezüge — OG-013 / OG-027
**Bereich:** Bildungsraum Plus: Rauminneres + südlicher Türausgang
**Bild:** Zwei Detail-Ausschnitte. OG-013 (Typ B): runder, richtungsfreier Aufheller (RIVO_Aufheller_Variante, 0°) im Rauminneren; ausdrücklich: eine Lichtachse ist keine Fluchtrichtungsangabe. OG-027 (Typ H): RIVO_ARR_down bei 180°, Zeichenfront im Plan oben (+Y) = in den Raum; Türzeichen am südlichen Ausgang mit Türmaß 90/210.
> „Runde, richtungsfreie AP-Spot-Darstellung; Produkt-/Montagedaten bleiben in Attributen erhalten. Eine Lichtachse ist keine Fluchtrichtungsangabe.“
> „Türzeichen am südlichen Ausgang des Bildungsraums Plus; Front nach Norden.“
> „das Türzeichen allein legt die gesamte weitere Route nicht fest.“
**Leuchten im Bild:** OG-013 aufheller, OG-027 down
**Personen:** aus dem Bildungsraum Plus (Norden)
**Linien:** orange Markierungskreise, keine Wegbehauptung
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · 
**Bewertung:** bestaetigt:NB-R01

## S.199 · OG — F-OG-17 Essbereich, MFU und südlicher Bestandsanschluss — Ort/Person/Folge/Sicht
**Bereich:** östlicher Essbereich, MUFU (1.1.2), Kommunikations-/Begegnungsflächen, Übergang zu TH 3 und Bestand/TH 2
**Bild:** Großer Grundriss-Ausschnitt mit vier Leuchten: OG-016 (Aufheller, Essbereich Ost), OG-035 (Aufheller, südliche offene MFU), OG-026 (beidseitig, westlicher Übergang), OG-028 (down-Türzeichen an leicht schräger Wand, orange gerahmt, mit P1 und grün gestrichelter Weginterpretation von Osten). Die Folge führt über OG-028 (Tür) und OG-026 (270°, nach Norden) zum TH-3-Anschluss; die südliche Bestandsverbindung bleibt als Schnittstelle F-X-03 offen.
> „OG-028 ist um 96° gedreht: die Front ist ungefähr östlich, mit der Wand mitgedreht.“
> „OG-026 hat Fronten Ost/West; von Süden kann es nur seitlich sichtbar sein.“
> „OG-026 weist bei 270° nach Norden zum TH-3-Anschluss.“
> „Die südliche Verbindung in den Bestand ... bleibt als Schnittstelle F-X-03 separat offen.“
**Leuchten im Bild:** OG-016 aufheller, OG-026 beidseitig, OG-028 down, OG-035 aufheller
**Personen:** P1, aus dem Essbereich von Osten; weitere Ströme aus offenen Flächen von Süden und Bildungsraum Plus von Norden
**Linien:** grün gestrichelt = Weginterpretation zum westlichen Türdurchgang; türkis = 2D-Sicht; orange = markierte Türwand (schräg)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · 
**Bewertung:** bestaetigt:NB-R23

## S.200 · OG — F-OG-17 Essbereich/MFU — Begründung/Normbezug
**Bereich:** Essbereich + MFU: 4 Symboltausche, schräge Türwand 96°
**Bild:** Textseite (E-J) mit vier Symboltauschen: OG-016 und OG-035 Aufheller (0°), OG-026 bothsided (270°), OG-028 down mit 96° Drehung. Kernaussage: die 96°-Drehung der schrägen Türwand wird ERHALTEN und nicht auf einen rechten Winkel gerundet; ein Zurückdrehen auf 90° würde den Wandbezug verändern. Normbezüge A01/A02/A04/A09.
> „Die 96°-Drehung wird erhalten und nicht auf einen rechten Winkel gerundet.“
> „Ein Zurückdrehen auf 90° würde den Bezug zur schrägen Wand verändern.“
> „Kleine Winkelabweichungen können einen realen Gebäudebezug haben und müssen beim Symboltausch erhalten bleiben.“
**Leuchten im Bild:** OG-016 aufheller, OG-026 beidseitig, OG-028 down, OG-035 aufheller
**Linien:** keine (Textseite)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · 
**Bewertung:** neu → Tür-RZ an schräger Wand: Symbol-Rotation folgt exakt dem realen Wandwinkel (hier 96°) und darf beim Symboltausch/Rendern NICHT auf 90°-Raster gerundet werden — kleine Winkelabweichungen tragen realen Gebäudebezug (erweitert NB-R11: Rotation unverändert erhalten).

## S.201 · OG — F-OG-17 Einzelbezüge — OG-016 / OG-026
**Bereich:** östlicher Essbereich + westlicher Übergang der MFU-/Essbereichsgruppe
**Bild:** Zwei Detail-Ausschnitte. OG-016 (Typ B): richtungsfreier Aufheller im östlichen Essbereich. OG-026 (Typ H): RIVO_ARR_bothsided bei 270°, Fronten Ost/West, Pfeile nach Norden Richtung TH-3-Anschluss; die Ankunft aus dem östlichen Essbereich kann eine Front treffen, eine südliche Ankunft aus dem Bestand sieht eher die Kante.
> „Die Ankunft aus dem östlichen Essbereich kann eine Front treffen; eine südliche Ankunft aus dem Bestand sieht eher die Kante.“
> „keine lückenlos frontale Folge für alle Personen behaupten.“
> „Eine Lichtachse ist keine Fluchtrichtungsangabe.“
**Leuchten im Bild:** OG-016 aufheller, OG-026 beidseitig
**Personen:** östlicher Essbereich (trifft Front) und südlicher Bestand (sieht Kante)
**Linien:** orange Markierungskreise, keine Wegbehauptung
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · 
**Bewertung:** bestaetigt:NB-R16

## S.202 · OG — F-OG-17 Einzelbezüge — OG-028 / OG-035
**Bereich:** westlicher Essbereich-Ausgang (schräge Wand) + südliche offene MFU
**Bild:** Zwei Detail-Ausschnitte. OG-028 (Typ H): RIVO_ARR_down bei 96°, Türzeichen an leicht schräger Wand, Front annähernd nach Osten (mit der Wand mitgedreht), Türmaß 160/210. OG-035 (Typ B): richtungsfreier Aufheller in der südlichen offenen MFU bei der Bestandsverbindung; keine Raumbeleuchtung für Sozial-/Teamräume hinter Wänden.
> „Lokaler Türbezug vor dem beidseitigen Übergangszeichen OG-026; die Bestandsdrehung beträgt 96 Grad und bleibt erhalten.“
> „Montage parallel zur tatsächlichen Wand, freier Blick zwischen Tischen und Anschlussblick nach der Tür sind zu prüfen.“
> „Anderer offener Flächenbereich als OG-016 im östlichen Essbereich; keine Raumbeleuchtung für Sozial-/Teamraum hinter Wänden.“
**Leuchten im Bild:** OG-028 down, OG-035 aufheller
**Personen:** Essbereich von Osten (OG-028) bzw. offene Fläche/südlicher Bestandsanschluss (OG-035)
**Linien:** orange Markierungskreise, keine Wegbehauptung
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · 
**Bewertung:** bestaetigt:NB-R01

## S.203 — F-X-01 TH 4: vom Obergeschoss bis vor die westliche Außentür — geschossübergreifende Folge
**Bereich:** TH 4 (westliches Gebäudeende) über OG, EG und SG bis westliche Außentür
**Bild:** Drei nebeneinandergestellte Grundriss-Ausschnitte (OG / EG / SG) von TH 4 mit den vorhandenen RZ an Podesten und Zugängen; im SG zusätzlich Nebenräume UG.64 Putzraum / UG.65 Garten WC. Ausdrücklich als NICHT maßstäbliches Ablaufschema deklariert: OG -> EG -> SG -> Außentür -> sicherer Bereich; Lauf-/Podest- und Höhenabgleich bleibt offen. Kein Zeichen wird aus der Rückseite als lesbar angenommen.
> „Die Pfeile dieser Textfolge sind keine maßstäbliche Verbindung durch die Grundrisse. Lauf-/Podest- und Höhenabgleich bleibt offen.“
> „Linke und rechte Laufseiten haben gegenläufige Pfeile und verschiedene Frontnormalen.“
> „Eine Person soll am jeweiligen Podest die nächste erforderliche Richtungsentscheidung erkennen können. Kein Zeichen wird aus der Rückseite als lesbar angenommen.“
**Leuchten im Bild:** ? left, ? beidseitig
**Personen:** westliche Raumgänge und höhere Stiegenläufe (getrennt zu beurteilen)
**Linien:** keine gezeichneten Wegverbindungen; nur schematische Textfolge OG->EG->SG->Außentür
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · 
**Bewertung:** bestaetigt:NB-R12

## S.204 — F-X-01 TH 4 — Begründung/Normbezug der geschossübergreifenden Folge
**Bereich:** TH 4 gesamtvertikal (OG-EG-SG), Zeichen-Betriebsart A17
**Bild:** Textseite (E-J), geschossübergreifende Erklärung ohne zusätzlichen Symboltausch. Aufzüge werden ohne Evakuierungsnachweis NICHT in die Fluchtfolge eingebunden. Neu gegenüber den Fallseiten: A17 (OVE E 8101, Ausgaben 2019/AC1:2020/2025) zur Betriebsart — ab AC1:2020 Erforderlich-Zeichen für Dauerbetrieb der RZ auf Fluchtwegen; die sichtbare RZ-Grafik belegt weder Dauerbetrieb noch Normenausgabe. J: geschossweise richtige Einzelzeichen erst nach Abgleich der Übergänge als zusammenhängende Folge bewerten.
> „Aufzüge werden ohne Evakuierungsnachweis nicht in die Folge eingebunden.“
> „Eine einzige vertikale Verbindungslinie durch übereinandergelegte Pläne würde Lauf, Treppenauge und Podeste verschleiern.“
> „Geschossweise richtige Einzelzeichen erst nach dem Abgleich der Übergänge als zusammenhängende Folge bewerten.“
> „Die sichtbare RZ-Grafik belegt weder Dauerbetrieb noch die angewandte Normenausgabe; Schaltungs- und Betriebsnachweis offen.“
**Linien:** keine (Textseite)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · 
**Bewertung:** bestaetigt:NB-R27

## S.205 — F-X-02 TH 3: Podestfolge, Windfang und äußerer Anschluss
**Bereich:** TH 3 geschossübergreifend OG-EG-SG, Windfang und Außentür
**Bild:** Drei nebeneinandergestellte Planausschnitte OG/EG/SG zeigen TH 3 mit Stiegenläufen, E-Schacht, Windfang (SG) und grünen RZ an den Podesten. Orange Hinweiszeile: die schematische Folge OG→EG→SG→Außentür→sicherer Bereich ist keine maßstäbliche Verbindung; Lauf-/Podest- und Höhenabgleich bleibt offen. Text: nördliche und südliche Podestzeichen haben entgegengesetzte Fronten/Pfeile; Balkon ist kein automatisch sicherer Endpunkt; Höhenverlauf wird nicht aus einem Architektur-Aufwärtspfeil allein abgeleitet.
> „Die erklärte Folge lautet OG – TH-3-Läufe/Podeste – EG – SG – Windfang – Außentür – sicherer Außenbereich. Der Balkon ist kein automatisch sicherer Endpunkt.“
> „Der konkrete Höhenverlauf wird nicht aus einem Architektur-Aufwärtspfeil allein abgeleitet.“
> „Die nördlichen und südlichen Podestzeichen besitzen entgegengesetzte Fronten und Pfeile.“
**Leuchten im Bild:** SG-001 beidseitig, SG-003 down, SG-004 down, SG-005 antipanik, SG-011 down
**Personen:** östliche MFU / Stiegenläufe / oberer DG-Anschluss je Ebene
**Linien:** orange Hinweistexte; keine gezeichneten Verbindungslinien durch die Grundrisse (ausdrücklich)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · geschossübergreifender Fall (bezieht F-OG-15/F-EG-14/F-SG-09); SG-Kennungen aus Leuchtenregister S.213, nicht einzeln geprüft
**Bewertung:** bestaetigt:NB-R25

## S.206 — F-X-02 TH 3 — Begründung, CAD-Zuordnung, Normbezug, offene Nachweise
**Bereich:** TH 3 geschossübergreifend, Normbezugs-Seite
**Bild:** Reine Textseite (Abschnitte E-J) ohne Planausschnitt. RZ und SL im Ausgangsbereich erfüllen getrennte Aufgaben; keine weitere physische Leuchte gezählt. G verwirft Abkürzungen durchs Treppenauge/über Geländer. Normbezug A01 (Kette bis zum sicheren Bereich), A02 (4.1.2 a-g, beide Richtungen ausleuchten, kein bestimmter RZ-Block gefordert), A03 (1 lx Mittellinie, Ud 1:40), A09 (l=z×h, z=100/200), A17 (Dauerbetrieb der Zeichen ab AC1:2020). Orange: DG-Grundlagen, Podest-/Stufenbeleuchtung und Betriebsnachweis offen.
> „Ist der Notausgang nicht direkt sichtbar, müssen ein oder mehrere zusätzliche beleuchtete oder hinterleuchtete Rettungszeichen das Erreichen des Ausgangs erleichtern.“
> „Bei Richtungsänderungen und Kreuzungen muss die Sicherheitsleuchte beide Richtungen ausleuchten; dies ist keine pauschale Forderung nach einem bestimmten RZ-Block.“
> „Ein Weg mitten durch das Treppenauge oder geradlinig quer über Geländer würde eine nicht begehbare Abkürzung zeigen.“
> „Die sichtbare RZ-Grafik belegt weder Dauerbetrieb noch die angewandte Normenausgabe; Schaltungs- und Betriebsnachweis offen.“
**Linien:** keine (Textseite); orange Hinweistexte in Abschnitt I
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · nicht geprüft; Seite zählt ausdrücklich keinen zusätzlichen Symboltausch
**Bewertung:** bestaetigt:NB-R12

## S.207 — F-X-03 Bestandsflügel und TH 2: Grenze der belegten Leuchtenfolge
**Bereich:** südlicher Bestandsflügel und TH 2, gesamtes Gebäude
**Bild:** Ein Gesamtgrundriss zeigt Erweiterung plus südlichen Bestandsflügel als graue Architektur ohne markierte Leuchtenkette. Orange Hinweiszeile: alle Originalinhalte bleiben in der DXF erhalten; die fehlende durchgehende Zielobjektfolge im Bestand wird nicht durch angenommene neue Symbole ersetzt. Text: erkannte physische Zielobjekte liegen überwiegend im Erweiterungsbereich; für EG/OG wird keine neue RZ-Kette über den Bestandsflügel erfunden; im SG ist der südliche Quergang mit TH-2-Anschluss (F-SG-17) dokumentiert.
> „Die fehlende durchgehende Zielobjektfolge im Bestand wird nicht durch angenommene neue Symbole ersetzt.“
> „Ankünfte aus dem Bestand dürfen bei einer gesamthaften Schulprüfung nicht verschwinden, nur weil hier keine durchgehende Zielobjektfolge erkannt wurde.“
> „Die südlichen Ankünfte treffen teilweise seitlich auf vorhandene beidseitige Zeichen.“
**Leuchten im Bild:** SG-058 antipanik, SG-059 down, SG-060 beidseitig, SG-061 aufheller
**Personen:** Bestandsflügel Süd/Ost
**Linien:** keine erfundenen Ketten-/Sichtlinien im Bestand (ausdrücklich)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · Kennungen = F-SG-17-Positionen aus Leuchtenregister S.215 als dokumentierter TH-2-Anschluss; Bestandsflügel selbst ohne erfasste Zielobjekte
**Bewertung:** neu → Erfassungsgrenzen-Disziplin: erkannter Symbolumfang ≠ Planblattfläche ≠ Bewertungsumfang — im Bestand ohne belegte Zielobjektfolge KEINE Symbole erfinden, Bestands-Ankünfte aber als offene Prüfpflicht führen (verallgemeinert NB-R18/NB-R24-Prozessregel 'nicht raten' auf Bestand/Erweiterung)

## S.208 — F-X-03 Bestandsflügel und TH 2 — Begründung, Normbezug, offene Nachweise
**Bereich:** Bestandsflügel/TH 2, Normbezugs-Seite (Schul-Einstufung)
**Bild:** Reine Textseite (E-J). Kernpunkt: Umfang der erkannten Symbolmenge, Gebäudefläche und normativ zu bewertendes Gesamtobjekt sind zu unterscheiden. Normbezug A11 (OVE E 8101: Schulzeile 3 h Betriebsdauer, AC1:2020 bindet an erhöhte Anforderungen), A12 (OVE R12-2/OIB RL2: Schwelle 3.200 m² Netto-Grundfläche trennt allgemeine und erhöhte Anforderungen), A17 (Zeichen-Dauerbetrieb). G warnt: nur die Erweiterungsfläche zur 3.200-m²-Schwelle heranzuziehen könnte die Einstufung verfälschen. J: Erfassungsgrenze, Planblattgrenze und rechtlicher Bewertungsumfang sind nicht dasselbe.
> „Nur die Erweiterungsfläche zur 3.200-m²-Schulschwelle heranzuziehen könnte die Einstufung verändern; erforderlich ist die maßgebende Gesamtfläche nach der tatsächlich anwendbaren Regel.“
> „N04 trennt für Schulen ≤3.200 m² allgemeine und >3.200 m² erhöhte Anforderungen; N05 bezeichnet die Fläche ausdrücklich als Netto-Grundfläche.“
> „Die unkorrigierte Ausgabe 2019 nennt im informativen Leitfaden 3 h für Schulen.“
> „Erfassungsgrenze, Planblattgrenze und rechtlicher Bewertungsumfang sind nicht dasselbe.“
**Linien:** keine (Textseite); orange Hinweistexte in Abschnitt I
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · nicht geprüft; kein Symboltausch auf dieser Seite
**Bewertung:** neu → Schul-Einstufung (Enis-Lane): 3.200-m²-Netto-Grundflächen-Schwelle (OIB RL2 Tab.6 / OVE R12-2 Tab.5.1) IMMER über die maßgebende Gesamtfläche inkl. Bestand bestimmen, nie nur über die Erweiterung; Schul-Betriebsdauer 3 h (OVE E 8101 56.A.1.AT); Ausgabenstände (2019/AC1:2020/2025) nicht mischen

## S.209 — F-X-04 Dachgeschoss: Technikraum, Dachzugang und TH 3 — offene Elektrogrundlage
**Bereich:** Dachgeschoss (Quellenabbildung Flucht- und Rettungsplan S.10)
**Bild:** Ganzseitige Wiedergabe des Original-Flucht- und Rettungsplans Seite 10 (Dachgeschoss, M 1:250) mit Verhaltensregeln Unfall/Brandfall, Legende, Lageplan und Grundriss mit Technikraum, TH 3 und Dachflächen; Standortmarke und grüne Fluchtwegsymbole sind Quellplaninhalte. Orange Beschriftung: ausdrücklich KEIN RIVO-Ergebnisplan und kein Ersatz für den fehlenden Elektromontageplan des DG. Text: grüne Richtungssymbole sind Quellplaninformationen, keine vermessenen Leuchtenfronten; Dachfläche ist keine frei begehbare Fluchtfläche und kein sicherer Endpunkt.
> „Dies ist ausdrücklich KEIN RIVO-Ergebnisplan und kein Ersatz für einen fehlenden Elektromontageplan des DG.“
> „Die im Fluchtplan gezeichneten grünen Richtungssymbole sind Quellplaninformationen und keine vermessenen RIVO-Leuchtenfronten.“
> „Aus den gezeichneten Dachflächen wird keine frei begehbare Fluchtfläche abgeleitet.“
> „Aufzug nicht benutzen (Verhalten im Brandfall, Quellplan-Legende).“
**Personen:** Technikraum / freigegebener Wartungsbereich der Dachfläche / oberer Anschluss TH 3
**Linien:** grüne Fluchtweg-/Richtungssymbole und Standortmarke = Quellplaninhalt, keine RIVO-Elemente
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · kein DG-DXF in der Zielobjektmenge vorhanden; Quellenabbildung ohne RIVO-Kennungen
**Bewertung:** bestaetigt:NB-R22

## S.210 — F-X-04 Dachgeschoss — Begründung, Normbezug, offene Nachweise
**Bereich:** Dachgeschoss, Normbezugs-Seite (Technikraum-Einstufung)
**Bild:** Reine Textseite (E-J). Der Raumname Technikraum allein belegt weder besondere Gefährdung noch die Einstufung als bezeichnete Elektro-/Sicherheitszentrale. F: reiner Ergänzungs-/Prüfbereich, keine Leuchte und kein Symboltausch gezählt; Quellplanausschnitt ist als Quellenabbildung zu beschriften. Normbezug A01, A02 und A06 (OVE E 8101 718.560.9.001.AT: bei erhöhten Anforderungen Sanitär ab 8 m², barrierefreie WCs, bezeichnete Elektro-/Sicherheitszentralen; 60-m²-Regel nur für verkehrstechnische Einrichtungen). Orange: DG-Elektroplan, Dachbegehung, Türfreigaben, Höhenkoten, Licht-/Sichtnachweis offen — die 146 Zielobjekte in SG/EG/OG schließen diese Lücke nicht.
> „Der Raumname Technikraum allein belegt weder eine besondere Gefährdung noch die Einstufung als bezeichnete Elektro-/Sicherheitszentrale.“
> „Ziffer 3 ist ausdrücklich auf verkehrstechnische Einrichtungen begrenzt und begründet keine pauschale 60-m²-Schwelle für Schulräume.“
> „Es wäre falsch, die Quelle mangels DG-Elektrosymbolen wegzulassen oder ihre grünen Piktogramme als bereits ausgetauschte Leuchten auszugeben.“
> „Das Dachgeschoss gehört zur dokumentierten Gebäudeprüfung, obwohl hier noch keine physische Leuchte zugeordnet ist.“
**Linien:** keine (Textseite); orange Hinweistexte in Abschnitt I
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht geprüft; Seite zählt ausdrücklich keine Leuchte und keinen Symboltausch
**Bewertung:** neu → Raumnamen-Disziplin (Selman-/Enis-Naht): Raumlabel 'Technikraum' allein löst KEINE Sonderregel aus — Einstufung als Elektro-/Sicherheitszentrale, Sanitär ≥8 m² und barrierefreie WCs sind nur bei festgestellten erhöhten Anforderungen zu prüfen (OVE E 8101 718.560.9.001.AT); 60-m²-Schwelle gilt NUR für verkehrstechnische Einrichtungen, nicht pauschal für Schulräume

## S.211 — Fallverzeichnis — Alle physischen Positionen genau einem örtlichen Grundfall zugeordnet
**Bereich:** Verzeichnis F-SG-01 bis F-OG-09
**Bild:** Reine Verzeichnisseite: Liste der Fälle F-SG-01..18, F-EG-01..17 und F-OG-01..09 mit Seitenzahl und Kurztitel. Keine Planausschnitte, keine Leuchten, keine Personen. Dient als Inhaltsindex der Einzelfälle.
> „Alle physischen Positionen genau einem örtlichen Grundfall zugeordnet.“
**Linien:** keine
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · nicht anwendbar (Verzeichnisseite)
**Bewertung:** kein_regelgehalt

## S.212 — Fallverzeichnis — Fortsetzung
**Bereich:** Verzeichnis F-OG-10 bis F-X-04
**Bild:** Reine Verzeichnisseite: Fortsetzung der Fallliste F-OG-10..17 und der geschossübergreifenden Fälle F-X-01..04 mit Seitenzahlen und Kurztiteln. Keine Planausschnitte, keine Leuchten.
**Linien:** keine
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · nicht anwendbar (Verzeichnisseite)
**Bewertung:** kein_regelgehalt

## S.213 · SG — Leuchtenregister — Sockelgeschoss SG-001 bis SG-023
**Bereich:** Register Sockelgeschoss (Transformationen, Attribute)
**Bild:** Reine Registerseite: je Leuchte Kennung, Typ-Letter (B-P), Status 'ersetzt', Fall- und Einzelbezug-Seite, Block-Mapping STANDARD_* → RIVO_*0 mit Handle und Rotation θ. Abgedeckte Mappings: RZ_PU→ARR_down0, RZ_PLPR→ARR_bothsided0, SL/SL_MITTE_PFEIL→Antipanik0, SPOT/SPOT_SL/SPOT_DA/SPOT_SL_DA→Aufheller_Variante0. Keine Planausschnitte, keine Personen.
> „Vollständige Transformationen, Attribute und Textkandidaten in JSON/CSV.“
**Leuchten im Bild:** SG-001 beidseitig, SG-002 down, SG-003 down, SG-004 down, SG-005 antipanik, SG-006 antipanik, SG-007 antipanik, SG-008 antipanik, SG-009 aufheller, SG-010 antipanik, SG-011 down, SG-012 down, SG-013 aufheller, SG-014 aufheller, SG-015 down, SG-016 down, SG-017 antipanik, SG-018 antipanik, SG-019 antipanik, SG-020 down, SG-021 down, SG-022 down, SG-023 aufheller
**Linien:** keine (Registerseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 3511A, 34CD9, 34D15, 34D51, 350AD, 36BA5, 36BC2, 36BDF, 34EFD, 350E4, 34D33, 34E79, 34E97, 34EB3, 34E5B, 34CA7, 350FF, 3552F, 3554A, 34C88, 34CF7, 34E1F, 34F6E · Stichprobe 3511A/34CD9/34D15/350AD in SG_RIVO_Erklaerung.json bestätigt; übrige Handles aus Registerseite übernommen
**Bewertung:** kein_regelgehalt

## S.214 · SG — Leuchtenregister — Fortsetzung SG-024 bis SG-046
**Bereich:** Register Sockelgeschoss (Transformationen, Attribute)
**Bild:** Reine Registerseite, Fortsetzung: SG-024 bis SG-046 mit Kennung, Typ-Letter, Fall-/Einzelbezug, Mapping STANDARD_* → RIVO_*0, Handle und θ. Auffällig sind krumme Rotationen wie 272.319°, 279.211°, 9.21103° und 7.78035° (aus Bestandsgeometrie übernommen). Keine Planausschnitte, keine Personen.
**Leuchten im Bild:** SG-024 down, SG-025 antipanik, SG-026 antipanik, SG-027 down, SG-028 down, SG-029 beidseitig, SG-030 down, SG-031 aufheller, SG-032 aufheller, SG-033 down, SG-034 beidseitig, SG-035 down, SG-036 down, SG-037 down, SG-038 down, SG-039 down, SG-040 aufheller, SG-041 down, SG-042 down, SG-043 antipanik, SG-044 down, SG-045 aufheller, SG-046 aufheller
**Linien:** keine (Registerseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34E3D, 36BFC, 36A7C, 34B86, 34BA4, 34BC2, 34BE0, 34ECF, 34EE6, 34D6F, 34F50, 34E01, 34BFE, 34C50, 34D8D, 34DAB, 34DE7, 34F32, 34F14, 36C19, 34B68, 34C1C, 34C6E · Stichprobe 34E01/36C19 in SG_RIVO_Erklaerung.json bestätigt; übrige Handles aus Registerseite übernommen
**Bewertung:** kein_regelgehalt

## S.215 — Leuchtenregister — Fortsetzung SG-047 bis SG-061 und Erdgeschoss EG-001 bis EG-008
**Bereich:** Register Sockelgeschoss-Schluss + Beginn Erdgeschoss
**Bild:** Reine Registerseite: Abschluss Sockelgeschoss (SG-047..061, inkl. zwei FLAP-SL-Positionen SG-051/SG-055 aus F-SG-18) und Beginn Erdgeschoss (EG-001..008). Im EG erscheinen erstmals RIVO-Blocknamen ohne 0-Suffix (RIVO_ARR_left, RIVO_ARR_down, RIVO_ARR_bothsided, RIVO_Aufheller_Variante) sowie das Mapping STANDARD_RZ_PL→RIVO_ARR_left. Keine Planausschnitte, keine Personen.
**Leuchten im Bild:** SG-047 aufheller, SG-048 aufheller, SG-049 aufheller, SG-050 down, SG-051 antipanik, SG-052 beidseitig, SG-053 aufheller, SG-054 beidseitig, SG-055 antipanik, SG-056 aufheller, SG-057 beidseitig, SG-058 antipanik, SG-059 down, SG-060 beidseitig, SG-061 aufheller, EG-001 left, EG-002 aufheller, EG-003 beidseitig, EG-004 aufheller, EG-005 aufheller, EG-006 down, EG-007 left, EG-008 down
**Linien:** keine (Registerseite)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles 34F85, 3507B, 34C36, 34DC9, 36C36, 34FD6, 35030, 34FF4, 36C52, 3504A, 35012, 350C8, 34FB9, 34F9C, 35064, 2075C, 2099C, 20669, 20982, 20742, 20964, 20779, 20864 · seitenübergreifend SG+EG: EG-Handles gehören zu EG_RIVO_Erklaerung.dxf; Stichprobe 34F9C/35064 (SG) und 2075C/20669/20964 (EG) in den Inventar-JSONs bestätigt
**Bewertung:** kein_regelgehalt

## S.216 · EG — Leuchtenregister — Fortsetzung EG-009 bis EG-031
**Bereich:** Register Erdgeschoss (Transformationen, Attribute)
**Bild:** Reine Registerseite: EG-009 bis EG-031 mit Kennung, Typ-Letter, Status 'ersetzt', Fall-/Einzelbezug, Mapping STANDARD_* → RIVO_* (ohne 0-Suffix), Handle und θ. Mappings: SPOT/SPOT_SL→Aufheller_Variante, RZ_PU→ARR_down, RZ_PLPR→ARR_bothsided. Keine Planausschnitte, keine Personen.
**Leuchten im Bild:** EG-009 aufheller, EG-010 aufheller, EG-011 aufheller, EG-012 aufheller, EG-013 aufheller, EG-014 aufheller, EG-015 down, EG-016 down, EG-017 down, EG-018 down, EG-019 down, EG-020 beidseitig, EG-021 aufheller, EG-022 beidseitig, EG-023 beidseitig, EG-024 aufheller, EG-025 down, EG-026 aufheller, EG-027 down, EG-028 beidseitig, EG-029 aufheller, EG-030 beidseitig, EG-031 down
**Linien:** keine (Registerseite)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 208A0, 20796, 206C3, 206DA, 20815, 207FB, 209B6, 20596, 20578, 20687, 206A5, 20882, 20914, 208F6, 20493, 2092E, 205B4, 207B0, 2062C, 209F2, 207CA, 2064B, 208BA · Stichprobe 208BA/207CA/20493 in EG_RIVO_Erklaerung.json bestätigt; übrige Handles aus Registerseite übernommen
**Bewertung:** kein_regelgehalt

## S.217 — Leuchtenregister (Fortsetzung) — EG-032 bis EG-045 + Beginn 1. Obergeschoss (OG-001 bis OG-009)
**Bereich:** Register-Tabelle EG/OG, keine Planausschnitte
**Bild:** Reine Textseite: Fortsetzung des Leuchtenregisters mit 14 EG-Einträgen (EG-032 bis EG-045) und Abschnittsstart '1. Obergeschoss' mit OG-001 bis OG-009. Jeder Eintrag nennt Kennung, Typ-Letter (B/C/D/F/H/I), Status 'ersetzt', Fall-Referenz (F-EG-xx/F-OG-xx mit Seite) und Einzelbezugs-Seite sowie die Block-Ersetzung STANDARD_* → RIVO_* mit DXF-Handle und Rotationswinkel θ. Auffällig EG-045 mit θ=269.007° — die schiefwinkelige Bestandsrotation wird bei der Ersetzung exakt erhalten.
> „EG-039 · Typ H · ersetzt · F-EG-17, S. 143; Einzelbezug S. 145 — STANDARD_RZ_PLPR → RIVO_ARR_bothsided; Handle 2082F; θ=270°.“
> „EG-045 · Typ I · ersetzt · F-EG-04, S. 96; Einzelbezug S. 99 — STANDARD_RZ_PL → RIVO_ARR_left; Handle 43561; θ=269.007°.“
**Leuchten im Bild:** EG-032 aufheller, EG-033 down, EG-034 down, EG-035 down, EG-036 down, EG-037 down, EG-038 aufheller, EG-039 beidseitig, EG-040 aufheller, EG-041 left, EG-042 aufheller, EG-043 aufheller, EG-044 aufheller, EG-045 left, OG-001 left, OG-002 down, OG-003 aufheller, OG-004 aufheller, OG-005 down, OG-006 aufheller, OG-007 left, OG-008 beidseitig, OG-009 aufheller
**Linien:** keine (Registerseite ohne Grafik)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles 20948, 2055A, 205D2, 205F0, 209D4, 2060E, 207E1, 2082F, 2084D, 20A11, 20728, 206F4, 2070E, 43561 · alle 14 EG-Handles in EG_RIVO_Erklaerung.json vorhanden, Block und θ stimmen 1:1; die 9 OG-Handles (1B3C3, 70A9A, 1B7D2, 1B6B5, 1B806, 1B7EC, 1B3E0, 1B5BD, 1B6CF) ebenso 1:1 gegen OG_RIVO_Erklaerung.json verifiziert
**Bewertung:** kein_regelgehalt

## S.218 · OG — Leuchtenregister (Fortsetzung) — OG-010 bis OG-032
**Bereich:** Register-Tabelle 1. Obergeschoss, keine Planausschnitte
**Bild:** Reine Textseite: 23 Register-Einträge OG-010 bis OG-032, gleiches Schema (Kennung, Typ-Letter, 'ersetzt', Fall-/Einzelbezugs-Seite, STANDARD_* → RIVO_*, Handle, θ). Rotationen überwiegend orthogonal (0°/90°/180°/270°); einzige Ausnahme OG-028 mit θ=96° (schiefwinkelige Bestandslage erhalten). Typen: 13x RZ_PU→ARR_down, 2x RZ_PLPR→ARR_bothsided, 8x SPOT/SPOT_SL→Aufheller_Variante.
> „OG-022 · Typ H · ersetzt · F-OG-11, S. 177; Einzelbezug S. 180 — STANDARD_RZ_PLPR → RIVO_ARR_bothsided; Handle 1B618; θ=180°.“
> „OG-028 · Typ H · ersetzt · F-OG-17, S. 199; Einzelbezug S. 202 — STANDARD_RZ_PU → RIVO_ARR_down; Handle 1B563; θ=96°.“
**Leuchten im Bild:** OG-010 aufheller, OG-011 aufheller, OG-012 aufheller, OG-013 aufheller, OG-014 down, OG-015 aufheller, OG-016 aufheller, OG-017 down, OG-018 aufheller, OG-019 down, OG-020 aufheller, OG-021 down, OG-022 beidseitig, OG-023 down, OG-024 aufheller, OG-025 down, OG-026 beidseitig, OG-027 down, OG-028 down, OG-029 down, OG-030 down, OG-031 down, OG-032 down
**Linien:** keine (Registerseite ohne Grafik)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B636, 1B71D, 1B703, 1B782, 1B455, 1B64D, 1B79C, 1B437, 1B737, 1B4AF, 1B6E9, 1B5F9, 1B618, 1B59F, 1B751, 1B581, 1B5DB, 1B545, 1B563, 1B491, 1B473, 1B4CD, 1B4EB · alle 23 Handles in OG_RIVO_Erklaerung.json vorhanden, Block und θ stimmen 1:1 (verifiziert)
**Bewertung:** kein_regelgehalt

## S.219 · OG — Leuchtenregister (Fortsetzung/Abschluss) — OG-033 bis OG-040
**Bereich:** Register-Tabelle 1. Obergeschoss, keine Planausschnitte
**Bild:** Reine Textseite mit den letzten 8 Register-Einträgen OG-033 bis OG-040, danach endet das Register. Schema unverändert; OG-036 (θ=90°) und OG-040 (θ=270°) sind die beiden left-RZ des OG-Falls F-OG-04, die übrigen Einträge sind down-RZ (θ=0°) und Aufheller (θ=0°). Restliche Seite leer.
> „OG-036 · Typ I · ersetzt · F-OG-04, S. 156; Einzelbezug S. 158 — STANDARD_RZ_PL → RIVO_ARR_left; Handle 1B3FD; θ=90°.“
> „OG-040 · Typ I · ersetzt · F-OG-04, S. 156; Einzelbezug S. 158 — STANDARD_RZ_PL → RIVO_ARR_left; Handle 1B41A; θ=270°.“
**Leuchten im Bild:** OG-033 down, OG-034 down, OG-035 aufheller, OG-036 left, OG-037 aufheller, OG-038 aufheller, OG-039 aufheller, OG-040 left
**Linien:** keine (Registerseite ohne Grafik)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles 1B509, 1B527, 1B768, 1B3FD, 1B69B, 1B667, 1B681, 1B41A · alle 8 Handles in OG_RIVO_Erklaerung.json vorhanden, Block und θ stimmen 1:1 (verifiziert)
**Bewertung:** kein_regelgehalt

## S.220 · SG — Symbol- und Transformationsprüfung — V001 (SG-001, 180°), V002 (SG-002, 90°), V003 (SG-003, 277°)
**Bereich:** Symbolvarianten-Katalog Sockelgeschoss (original vs. Ergebnis, maßstabsfrei)
**Bild:** Erste Seite des Varianten-Katalogs: je Variante links das Original-Bestandssymbol, rechts das RIVO-Ergebnis auf schwarzer Kachel. V001 beidseitiges RZ (STANDARD_RZ_PLPR → RIVO_ARR_bothsided0) bei 180°, Skalierung 0.5. V002/V003 down-RZ (STANDARD_RZ_PU → RIVO_ARR_down0) bei 90° bzw. 277° — die schiefwinkelige 277°-Rotation wird im Ergebnis exakt reproduziert. Jede Variante listet ihre Bestandsskalierung und alle Positionen, die sie verwenden.
> „Links: original · rechts: Ergebnis · tatsächliche Varianten, maßstabsfrei“
> „STANDARD_RZ_PLPR → RIVO_ARR_bothsided0 — Bestandsskalierung [0.5, 0.5, 0.5]; Positionen: SG-001“
> „STANDARD_RZ_PU → RIVO_ARR_down0 — Bestandsskalierung [0.7, 0.7, 0.7]; Positionen: SG-003, SG-012, SG-050“
**Leuchten im Bild:** SG-001 beidseitig, SG-002 down, SG-016 down, SG-027 down, SG-028 down, SG-030 down, SG-003 down, SG-012 down, SG-050 down
**Linien:** keine Plan-Linien; nur Symbolpaare auf schwarzen Bildkacheln
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · SG_RIVO_Erklaerung.json bestätigt die 0-Suffix-Variantenblöcke (26x RIVO_ARR_down0, 8x RIVO_ARR_bothsided0) und die Rotationswerte 180° (3x), 90° (5x), 277° (6x)
**Bewertung:** neu → Formkorrektur-Ersetzung bestandstreu: STANDARD-Block → RIVO-*0-Variante übernimmt Position, Kennung und Bestandsrotation exakt — auch die schiefwinkelige Rotationsfamilie 7°/97°/187°/277° (schräger Gebäudeflügel?) — und dokumentiert die Bestandsskalierung (0.5/0.7/1.0) je Variante; nur die Blockgrafik wechselt

## S.221 · SG — Symbol- und Transformationsprüfung — V004 (SG-004, 270°), V005 (SG-005, 0°), V006 (SG-006, 0°)
**Bereich:** Symbolvarianten-Katalog Sockelgeschoss (original vs. Ergebnis, maßstabsfrei)
**Bild:** V004 down-RZ (STANDARD_RZ_PU → RIVO_ARR_down0) bei 270°, Skalierung 0.7. V005 Sicherheitsleuchte als gelbe Doppeldreieck-Grafik (STANDARD_SL → RIVO_Antipanik0), Ergebnis ein richtungsfreies gelbes Rechteck mit grünem Rand. V006 STANDARD_SL_MITTE_PFEIL (gelbes Doppeldreieck MIT schwarzem Doppelpfeil) ebenfalls → RIVO_Antipanik0: der Pfeil der Bestandsgrafik entfällt im richtungsfreien Ergebnis (Lichtachse, keine Fluchtrichtungsangabe).
> „STANDARD_SL → RIVO_Antipanik0 — Bestandsskalierung [0.7, 0.7, 0.7]; Positionen: SG-005, SG-010, SG-017“
> „STANDARD_SL_MITTE_PFEIL → RIVO_Antipanik0 — Bestandsskalierung [1, 1, 1]; Positionen: SG-006, SG-007, SG-008“
**Leuchten im Bild:** SG-004 down, SG-005 antipanik, SG-010 antipanik, SG-017 antipanik, SG-006 antipanik, SG-007 antipanik, SG-008 antipanik
**Linien:** keine Plan-Linien; nur Symbolpaare auf schwarzen Bildkacheln
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · SG_RIVO_Erklaerung.json bestätigt 15x RIVO_Antipanik0 und Rotation 270° (3x); Einzelpositionen nicht kennungsgenau geprüft
**Bewertung:** kein_regelgehalt

## S.222 · SG — Symbol- und Transformationsprüfung — V007 (SG-009, 270°), V008 (SG-011, 7°), V009 (SG-013, 0°)
**Bereich:** Symbolvarianten-Katalog Sockelgeschoss (original vs. Ergebnis, maßstabsfrei)
**Bild:** V007 gelbes Quadrat-Symbol mit Kreis und Doppelpfeil (STANDARD_SPOT_SL_DA → RIVO_Aufheller_Variante0), Ergebnis der grüne Vierquadranten-Kreis (Aufheller), Doppelpfeil entfällt. V008 down-RZ bei 7° Schrägstellung (STANDARD_RZ_PU → RIVO_ARR_down0) — die kleine Bestandsneigung bleibt im Ergebnis erhalten. V009 rundes Bestandssymbol (STANDARD_SPOT_DA → RIVO_Aufheller_Variante0) bei 0°, Positionen SG-013, SG-014 und geschossübergreifend EG-032.
> „STANDARD_SPOT_SL_DA → RIVO_Aufheller_Variante0 — Bestandsskalierung [0.7, 0.7, 0.7]; Positionen: SG-009, SG-048“
> „STANDARD_RZ_PU → RIVO_ARR_down0 — Bestandsskalierung [0.7, 0.7, 0.7]; Positionen: SG-011“
> „STANDARD_SPOT_DA → RIVO_Aufheller_Variante0 — Bestandsskalierung [1, 1, 1]; Positionen: SG-013, SG-014, EG-032“
**Leuchten im Bild:** SG-009 aufheller, SG-048 aufheller, SG-011 down, SG-013 aufheller, SG-014 aufheller, EG-032 aufheller
**Linien:** keine Plan-Linien; nur Symbolpaare auf schwarzen Bildkacheln
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · SG_RIVO_Erklaerung.json bestätigt 16x RIVO_Aufheller_Variante0 und die Rotationswerte 270° und 7° (2x); EG-032 (Handle 20948) in EG_RIVO_Erklaerung.json verifiziert
**Bewertung:** kein_regelgehalt

## S.223 · SG — Symbol- und Transformationsprüfung — V010 (SG-015, 97°), V011 (SG-018, 96.5526°), V012 (SG-020, 180°)
**Bereich:** Symbolvarianten-Katalog Sockelgeschoss (original vs. Ergebnis, maßstabsfrei)
**Bild:** V010 down-RZ bei 97° (STANDARD_RZ_PU → RIVO_ARR_down0), die 7°-über-orthogonal-Schrägstellung bleibt erhalten. V011 Sicherheitsleuchte bei 96.5526° (STANDARD_SL → RIVO_Antipanik0), Ergebnis ein entsprechend gedrehtes gelbes Rechteck. V012 down-RZ bei 180° (STANDARD_RZ_PU → RIVO_ARR_down0) für SG-020 und SG-021; das Original zeigt hier die Aufwärtspfeil-Ansicht, das Ergebnis den RIVO-down-Block in 180°-Lage.
> „STANDARD_RZ_PU → RIVO_ARR_down0 — Bestandsskalierung [0.7, 0.7, 0.7]; Positionen: SG-015“
> „STANDARD_SL → RIVO_Antipanik0 — Bestandsskalierung [0.7, 0.7, 0.7]; Positionen: SG-018, SG-019“
> „STANDARD_RZ_PU → RIVO_ARR_down0 — Bestandsskalierung [0.7, 0.7, 0.7]; Positionen: SG-020, SG-021“
**Leuchten im Bild:** SG-015 down, SG-018 antipanik, SG-019 antipanik, SG-020 down, SG-021 down
**Linien:** keine Plan-Linien; nur Symbolpaare auf schwarzen Bildkacheln
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · SG_RIVO_Erklaerung.json bestätigt die Rotationswerte 97° (5x), 96.55° (2x), 180° (3x)
**Bewertung:** kein_regelgehalt

## S.224 · SG — Symbol- und Transformationsprüfung — V013 (SG-022, 187°), V014 (SG-023, 7.78035°), V015 (SG-025, 279.211°)
**Bereich:** Symbolvarianten-Katalog Sockelgeschoss (original vs. Ergebnis, maßstabsfrei)
**Bild:** V013 down-RZ bei 187° (STANDARD_RZ_PU → RIVO_ARR_down0) für SG-022, SG-024, SG-042 — wieder die 7°-Offset-Familie. V014 rundes Bestandssymbol mit Doppelpfeil (STANDARD_SPOT_SL → RIVO_Aufheller_Variante0) bei 7.78035°, Ergebnis der richtungsfreie grüne Vierquadranten-Kreis. V015 STANDARD_SL_MITTE_PFEIL bei 279.211° → RIVO_Antipanik0 als hochkant gedrehtes gelbes Rechteck; die vertikalen Bestandspfeile entfallen.
> „STANDARD_RZ_PU → RIVO_ARR_down0 — Bestandsskalierung [0.7, 0.7, 0.7]; Positionen: SG-022, SG-024, SG-042“
> „STANDARD_SPOT_SL → RIVO_Aufheller_Variante0 — Bestandsskalierung [1, 1, 1]; Positionen: SG-023“
> „STANDARD_SL_MITTE_PFEIL → RIVO_Antipanik0 — Bestandsskalierung [1, 1, 1]; Positionen: SG-025“
**Leuchten im Bild:** SG-022 down, SG-024 down, SG-042 down, SG-023 aufheller, SG-025 antipanik
**Linien:** keine Plan-Linien; nur Symbolpaare auf schwarzen Bildkacheln
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · SG_RIVO_Erklaerung.json bestätigt die Rotationswerte 187° (3x), 7.78° (1x), 279.21° (1x)
**Bewertung:** kein_regelgehalt

## S.225 · SG — Symbol- und Transformationsprüfung — V016 (SG-026, 0°), V017 (SG-029, 0°), V018 (SG-031, 0°)
**Bereich:** Symbolvarianten-Katalog Sockelgeschoss (original vs. Ergebnis, maßstabsfrei)
**Bild:** V016 Sicherheitsleuchte (STANDARD_SL → RIVO_Antipanik0) bei 0°, Skalierung 1, für SG-026, SG-051, SG-055. V017 beidseitiges RZ mit Links-Pfeilen (STANDARD_RZ_PLPR → RIVO_ARR_bothsided0) bei 0°, Skalierung 0.5, Ergebnis der zweizeilige RIVO-Block mit beiden Pfeilen nach links. V018 gelbes Quadrat-Symbol mit horizontalem Doppelpfeil (STANDARD_SPOT_SL_DA → RIVO_Aufheller_Variante0) bei 0° für SG-031, SG-032.
> „STANDARD_SL → RIVO_Antipanik0 — Bestandsskalierung [1, 1, 1]; Positionen: SG-026, SG-051, SG-055“
> „STANDARD_RZ_PLPR → RIVO_ARR_bothsided0 — Bestandsskalierung [0.5, 0.5, 0.5]; Positionen: SG-029“
> „STANDARD_SPOT_SL_DA → RIVO_Aufheller_Variante0 — Bestandsskalierung [0.7, 0.7, 0.7]; Positionen: SG-031, SG-032“
**Leuchten im Bild:** SG-026 antipanik, SG-051 antipanik, SG-055 antipanik, SG-029 beidseitig, SG-031 aufheller, SG-032 aufheller
**Linien:** keine Plan-Linien; nur Symbolpaare auf schwarzen Bildkacheln
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · SG_RIVO_Erklaerung.json bestätigt 41 Leuchten mit Rotation 0° sowie die Blöcke RIVO_Antipanik0/RIVO_ARR_bothsided0/RIVO_Aufheller_Variante0
**Bewertung:** kein_regelgehalt

## S.226 · SG — Symbol- und Transformationsprüfung — V019 (SG-033, 272.319°), V020 (SG-034, 277°), V021 (SG-035, 8°)
**Bereich:** Symbolvarianten-Katalog Sockelgeschoss (original vs. Ergebnis, maßstabsfrei)
**Bild:** V019 down-RZ bei 272.319° (STANDARD_RZ_PU → RIVO_ARR_down0), hochkant mit leichter Neigung. V020 beidseitiges RZ mit Aufwärtspfeilen bei 277° (STANDARD_RZ_PLPR → RIVO_ARR_bothsided0, Skalierung 0.5), das Ergebnis reproduziert die Doppel-Kachel samt Schrägstellung. V021 down-RZ bei 8° (STANDARD_RZ_PU → RIVO_ARR_down0) — erneut die kleine Schrägstellungs-Familie um 7-9°.
> „STANDARD_RZ_PU → RIVO_ARR_down0 — Bestandsskalierung [0.7, 0.7, 0.7]; Positionen: SG-033“
> „STANDARD_RZ_PLPR → RIVO_ARR_bothsided0 — Bestandsskalierung [0.5, 0.5, 0.5]; Positionen: SG-034“
> „STANDARD_RZ_PU → RIVO_ARR_down0 — Bestandsskalierung [0.7, 0.7, 0.7]; Positionen: SG-035“
**Leuchten im Bild:** SG-033 down, SG-034 beidseitig, SG-035 down
**Linien:** keine Plan-Linien; nur Symbolpaare auf schwarzen Bildkacheln
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · SG_RIVO_Erklaerung.json bestätigt die Rotationswerte 272.32° (1x), 277° (6x), 8° (1x)
**Bewertung:** kein_regelgehalt

## S.227 · SG — Symbol- und Transformationsprüfung — V022 (SG-036, 0°), V023 (SG-040, 0°), V024 (SG-041, 277°)
**Bereich:** Symbolvarianten-Katalog Sockelgeschoss (+EG-Mitnutzung), original vs. Ergebnis, maßstabsfrei
**Bild:** V022 down-RZ bei 0° (STANDARD_RZ_PU → RIVO_ARR_down0) für fünf SG-Positionen. V023 ist die meistgenutzte Variante des Katalogs: rundes gelb-weißes Bestandssymbol (STANDARD_SPOT → RIVO_Aufheller_Variante0) bei 0°, Skalierung 0.7, mit 21 Positionen quer durch SG UND EG (SG-040 bis SG-056 sowie EG-002 bis EG-044) — eine Variante wird geschossübergreifend wiederverwendet. V024 down-RZ bei 277° (STANDARD_RZ_PU → RIVO_ARR_down0) für SG-041.
> „STANDARD_RZ_PU → RIVO_ARR_down0 — Bestandsskalierung [0.7, 0.7, 0.7]; Positionen: SG-036, SG-037, SG-038, SG-039, SG-044“
> „STANDARD_SPOT → RIVO_Aufheller_Variante0 — Bestandsskalierung [0.7, 0.7, 0.7]; Positionen: SG-040, SG-045, SG-046, SG-049, SG-053, SG-056, EG-002, EG-004, EG-005, EG-009, EG-010, EG-012, EG-013, EG-014, EG-021, EG-024, EG-026, EG-038, EG-042, EG-043, EG-044“
**Leuchten im Bild:** SG-036 down, SG-037 down, SG-038 down, SG-039 down, SG-044 down, SG-040 aufheller, SG-045 aufheller, SG-046 aufheller, SG-049 aufheller, SG-053 aufheller, SG-056 aufheller, EG-002 aufheller, EG-004 aufheller, EG-005 aufheller, EG-009 aufheller, EG-010 aufheller, EG-012 aufheller, EG-013 aufheller, EG-014 aufheller, EG-021 aufheller, EG-024 aufheller, EG-026 aufheller, EG-038 aufheller, EG-042 aufheller, EG-043 aufheller, EG-044 aufheller, SG-041 down
**Linien:** keine Plan-Linien; nur Symbolpaare auf schwarzen Bildkacheln
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · SG_RIVO_Erklaerung.json bestätigt 16x RIVO_Aufheller_Variante0 und 26x RIVO_ARR_down0; EG-Mitnutzungen liegen in EG_RIVO_Erklaerung.dxf (dort als RIVO_Aufheller_Variante, stichprobenhaft über Register-Handles verifiziert)
**Bewertung:** kein_regelgehalt

## S.228 · SG — Symbol- und Transformationsprüfung — V025 (SG-043, 9.21103°), V026 (SG-047, 277.78°), V027 (SG-052, 97°)
**Bereich:** Symbolvarianten-Katalog Sockelgeschoss (original vs. Ergebnis, maßstabsfrei)
**Bild:** V025 STANDARD_SL_MITTE_PFEIL bei 9.21103° → RIVO_Antipanik0 als leicht schräges gelbes Rechteck (Pfeile entfallen). V026 rundes Bestandssymbol mit vertikalem Doppelpfeil (STANDARD_SPOT_SL → RIVO_Aufheller_Variante0) bei 277.78°, Ergebnis der richtungsfreie grüne Vierquadranten-Kreis. V027 beidseitiges RZ mit Abwärtspfeilen bei 97° (STANDARD_RZ_PLPR → RIVO_ARR_bothsided0, Skalierung 0.5) für SG-052, SG-054, SG-057.
> „STANDARD_SL_MITTE_PFEIL → RIVO_Antipanik0 — Bestandsskalierung [1, 1, 1]; Positionen: SG-043“
> „STANDARD_SPOT_SL → RIVO_Aufheller_Variante0 — Bestandsskalierung [1, 1, 1]; Positionen: SG-047“
> „STANDARD_RZ_PLPR → RIVO_ARR_bothsided0 — Bestandsskalierung [0.5, 0.5, 0.5]; Positionen: SG-052, SG-054, SG-057“
**Leuchten im Bild:** SG-043 antipanik, SG-047 aufheller, SG-052 beidseitig, SG-054 beidseitig, SG-057 beidseitig
**Linien:** keine Plan-Linien; nur Symbolpaare auf schwarzen Bildkacheln
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · SG_RIVO_Erklaerung.json bestätigt die Rotationswerte 9.21° (1x), 277.78° (1x), 97° (5x) und 8x RIVO_ARR_bothsided0
**Bewertung:** kein_regelgehalt

## S.229 · SG — Symbol- und Transformationsprüfung — V028-V030 (SG-058 bis SG-060)
**Bereich:** Register Symboltausch Sockelgeschoss
**Bild:** Registerseite mit drei Original/Ergebnis-Paaren auf schwarzen Kacheln, kein Grundriss. V028: gelb-weiße rechteckige Bestandsleuchte (STANDARD_SL) wird zu RIVO_Antipanik0, Bestandsrotation 277° erhalten. V029: kleines grünes RZ mit Rechtspfeil (STANDARD_RZ_PU) wird zu RIVO_ARR_down0 bei 97°. V030: Doppel-RZ mit zwei Linkspfeilen (STANDARD_RZ_PLPR) wird zu RIVO_ARR_bothsided0 bei 7°. Alle schrägen Bestandsrotationen und Bestandsskalierungen (0.7/0.7/0.5) werden unverändert übernommen.
> „Links: original · rechts: Ergebnis · tatsächliche Varianten, maßstabsfrei“
> „STANDARD_SL → RIVO_Antipanik0 · Bestandsskalierung [0.7, 0.7, 0.7]“
**Leuchten im Bild:** SG-058 antipanik, SG-059 down, SG-060 beidseitig
**Linien:** keine (schwarze Symbol-Kacheln, kein Planausschnitt)
**DXF-Abgleich:** SG_RIVO_Erklaerung.dxf · Handles — · Zielblöcke RIVO_Antipanik0 (15x), RIVO_ARR_down0 (26x), RIVO_ARR_bothsided0 (8x) im SG-Inventar vorhanden; schräge rot_deg 277.0/97.0/7.0 im DXF-Inventar bestätigt. Kennungen SG-0xx sind Registernummern, keine DXF-Handles.
**Bewertung:** kein_regelgehalt

## S.230 — Symbol- und Transformationsprüfung — V031-V033 (SG-061, EG-001, EG-003)
**Bereich:** Register Symboltausch SG/EG-Übergang
**Bild:** Registerseite mit drei Original/Ergebnis-Paaren, kein Grundriss. V031: gelber quadratischer Spot mit Doppelpfeil (STANDARD_SPOT_SL_DA) wird zum grünen Kreis-Aufheller RIVO_Aufheller_Variante0, schräge Bestandsrotation 6.17519° erhalten. V032: RZ mit Linkspfeil und Läufer (STANDARD_RZ_PL) wird zu RIVO_ARR_left bei 0°. V033: Doppel-RZ (STANDARD_RZ_PLPR) wird zu RIVO_ARR_bothsided bei 0°, dieselbe Variante gilt auch für Position OG-008. SG-Blöcke tragen 0-Suffix, EG/OG-Blöcke nicht.
> „STANDARD_SPOT_SL_DA → RIVO_Aufheller_Variante0“
> „Positionen: EG-003, OG-008“
**Leuchten im Bild:** SG-061 aufheller, EG-001 left, EG-003 beidseitig, OG-008 beidseitig
**Linien:** keine (schwarze Symbol-Kacheln, kein Planausschnitt)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · EG-Inventar: RIVO_ARR_left 5x, RIVO_ARR_bothsided 8x vorhanden; SG-Inventar: RIVO_Aufheller_Variante0 16x, rot_deg 6.18 bestätigt; OG-Inventar: RIVO_ARR_bothsided 4x. Seite mischt SG- und EG/OG-Positionen.
**Bewertung:** kein_regelgehalt

## S.231 · EG — Symbol- und Transformationsprüfung — V034-V036 (EG-006 bis EG-008)
**Bereich:** Register Symboltausch Erdgeschoss
**Bild:** Registerseite mit drei Original/Ergebnis-Paaren, kein Grundriss. V034: STANDARD_RZ_PU (Rechtspfeil, hochkant) wird zu RIVO_ARR_down bei 90°, Skalierung 0.6. V035: STANDARD_RZ_PL wird zu RIVO_ARR_left bei 180°, Skalierung 0.7. V036: STANDARD_RZ_PU wird zu RIVO_ARR_down bei 90°, Skalierung 0.6. Bestandsrotation und -skalierung jeweils unverändert übernommen.
> „STANDARD_RZ_PU → RIVO_ARR_down · Bestandsskalierung [0.6, 0.6, 0.6]“
**Leuchten im Bild:** EG-006 down, EG-007 left, EG-008 down
**Linien:** keine (schwarze Symbol-Kacheln, kein Planausschnitt)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · EG-Inventar: RIVO_ARR_down 16x, RIVO_ARR_left 5x vorhanden; rot_deg-Menge {0, 90, 180, 269.01, 270} deckt 90°/180° ab.
**Bewertung:** kein_regelgehalt

## S.232 · EG — Symbol- und Transformationsprüfung — V037-V039 (EG-011, EG-015, EG-016)
**Bereich:** Register Symboltausch Erdgeschoss
**Bild:** Registerseite mit drei Original/Ergebnis-Paaren, kein Grundriss. V037: gelb-weißer Kreis-Spot mit Vertikal-Doppelpfeil (STANDARD_SPOT_SL) wird zum grünen Kreis-Aufheller RIVO_Aufheller_Variante bei 90°, Skalierung 1. V038: STANDARD_RZ_PU (Aufwärtspfeil) wird zu RIVO_ARR_down bei 180°, Variante gilt für EG-015, EG-018, EG-019, EG-031. V039: identische Zuordnung bei 180° für EG-016, EG-017. Eine Variante bündelt mehrere gleich transformierte Positionen.
> „STANDARD_SPOT_SL → RIVO_Aufheller_Variante · Bestandsskalierung [1, 1, 1]“
> „Positionen: EG-015, EG-018, EG-019, EG-031“
**Leuchten im Bild:** EG-011 aufheller, EG-015 down, EG-018 down, EG-019 down, EG-031 down, EG-016 down, EG-017 down
**Linien:** keine (schwarze Symbol-Kacheln, kein Planausschnitt)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · EG-Inventar: RIVO_Aufheller_Variante 20x, RIVO_ARR_down 16x — die 7 hier gelisteten down-Positionen passen ins Band.
**Bewertung:** kein_regelgehalt

## S.233 · EG — Symbol- und Transformationsprüfung — V040-V042 (EG-020, EG-022, EG-023)
**Bereich:** Register Symboltausch Erdgeschoss, beidseitige Zeichen
**Bild:** Registerseite mit drei Original/Ergebnis-Paaren, kein Grundriss, alle drei beidseitig. V040: STANDARD_RZ_PLPR (Doppel-Aufwärtspfeil) wird zu RIVO_ARR_bothsided bei 270°. V041: STANDARD_RZ_PLPR (Doppel-Abwärtspfeil) wird zu RIVO_ARR_bothsided bei 90°. V042: gleiche Zuordnung bei 90°, aber mit krummer Bestandsskalierung 0.482583 statt 0.7 — auch nicht-runde Bestandsskalen werden exakt erhalten.
> „STANDARD_RZ_PLPR → RIVO_ARR_bothsided“
> „Bestandsskalierung [0.482583, 0.482583, 0.482583]; Positionen: EG-023“
**Leuchten im Bild:** EG-020 beidseitig, EG-022 beidseitig, EG-023 beidseitig
**Linien:** keine (schwarze Symbol-Kacheln, kein Planausschnitt)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · EG-Inventar: RIVO_ARR_bothsided 8x, n_beidseitig_gruppen=8 — drei der Gruppen hier dokumentiert.
**Bewertung:** kein_regelgehalt

## S.234 · EG — Symbol- und Transformationsprüfung — V043-V045 (EG-025, EG-027, EG-028)
**Bereich:** Register Symboltausch Erdgeschoss
**Bild:** Registerseite mit drei Original/Ergebnis-Paaren, kein Grundriss. V043: STANDARD_RZ_PU wird zu RIVO_ARR_down bei 90°. V044: STANDARD_RZ_PU (Linkspfeil hochkant) wird zu RIVO_ARR_down bei 270°. V045: STANDARD_RZ_PLPR (zwei Rechtspfeile) wird zu RIVO_ARR_bothsided bei 180°. Rotation und Skalierung (0.6/0.6/0.7) unverändert aus dem Bestand.
> „STANDARD_RZ_PU → RIVO_ARR_down · Bestandsskalierung [0.6, 0.6, 0.6]“
**Leuchten im Bild:** EG-025 down, EG-027 down, EG-028 beidseitig
**Linien:** keine (schwarze Symbol-Kacheln, kein Planausschnitt)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · EG-Inventar deckt down 16x und bothsided 8x; Rotationen 90/270/180 im rot_deg-Set vorhanden.
**Bewertung:** kein_regelgehalt

## S.235 · EG — Symbol- und Transformationsprüfung — V046-V048 (EG-029, EG-030, EG-033)
**Bereich:** Register Symboltausch Erdgeschoss, Sammelvarianten
**Bild:** Registerseite mit drei Original/Ergebnis-Paaren, kein Grundriss. V046: gelb-weißer Kreis-Spot mit Horizontal-Doppelpfeil (STANDARD_SPOT_SL) wird zum grünen Kreis-Aufheller, gilt für EG-029 und EG-040. V047: STANDARD_RZ_PLPR (Doppel-Aufwärtspfeil) wird zu RIVO_ARR_bothsided bei 270°, gilt für EG-030 und EG-039. V048: STANDARD_RZ_PU (Abwärtspfeil) wird zu RIVO_ARR_down bei 0° für fünf Positionen EG-033 bis EG-037.
> „STANDARD_SPOT_SL → RIVO_Aufheller_Variante · Positionen: EG-029, EG-040“
> „Positionen: EG-033, EG-034, EG-035, EG-036, EG-037“
**Leuchten im Bild:** EG-029 aufheller, EG-040 aufheller, EG-030 beidseitig, EG-039 beidseitig, EG-033 down, EG-034 down, EG-035 down, EG-036 down, EG-037 down
**Linien:** keine (schwarze Symbol-Kacheln, kein Planausschnitt)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · EG-Inventar: Aufheller_Variante 20x, bothsided 8x, down 16x — die 9 hier gebündelten Positionen passen ins Band.
**Bewertung:** kein_regelgehalt

## S.236 — Symbol- und Transformationsprüfung — V049-V051 (EG-041, EG-045, OG-001)
**Bereich:** Register Symboltausch EG/OG-Übergang, Stiegenhaus-Zeichen TH 4
**Bild:** Registerseite mit drei Original/Ergebnis-Paaren, kein Grundriss. V049: STANDARD_RZ_PL (Abwärtspfeil hochkant) wird zu RIVO_ARR_left bei 90°. V050: STANDARD_RZ_PL (Aufwärtspfeil) wird zu RIVO_ARR_left bei 269.007° — die aus F-EG-04 bekannte bewusst erhaltene geringe Schrägstellung erscheint hier als exakter Registerwert. V051: STANDARD_RZ_PL wird zu RIVO_ARR_left bei 0°, Skalierung 0.6 (OG).
> „STANDARD_RZ_PL → RIVO_ARR_left“
> „V050 · EG-045 · 269.007° · ersetzt“
**Leuchten im Bild:** EG-041 left, EG-045 left, OG-001 left
**Linien:** keine (schwarze Symbol-Kacheln, kein Planausschnitt)
**DXF-Abgleich:** EG_RIVO_Erklaerung.dxf · Handles — · EG-Inventar: RIVO_ARR_left 5x, rot_deg 269.01 im DXF bestätigt (einziger schräger EG-Winkel); OG-Inventar: RIVO_ARR_left 5x.
**Bewertung:** kein_regelgehalt

## S.237 · OG — Symbol- und Transformationsprüfung — V052-V054 (OG-002, OG-003, OG-007)
**Bereich:** Register Symboltausch Obergeschoss, größte Sammelvariante
**Bild:** Registerseite mit drei Original/Ergebnis-Paaren, kein Grundriss. V052: STANDARD_RZ_PU wird zu RIVO_ARR_down bei 90° für OG-002 und OG-005. V053: gelb-weißer Kreis-Spot OHNE Pfeil (STANDARD_SPOT) wird zum grünen Kreis-Aufheller bei 0° — größte Sammelvariante des Registers mit 15 Positionen (OG-003, OG-004, OG-006, OG-009, OG-011, OG-012, OG-013, OG-015, OG-016, OG-018, OG-020, OG-035, OG-037, OG-038, OG-039). V054: STANDARD_RZ_PL wird zu RIVO_ARR_left bei 180°.
> „STANDARD_SPOT → RIVO_Aufheller_Variante · Bestandsskalierung [0.5, 0.5, 0.5]“
**Leuchten im Bild:** OG-002 down, OG-005 down, OG-003 aufheller, OG-004 aufheller, OG-006 aufheller, OG-009 aufheller, OG-011 aufheller, OG-012 aufheller, OG-013 aufheller, OG-015 aufheller, OG-016 aufheller, OG-018 aufheller, OG-020 aufheller, OG-035 aufheller, OG-037 aufheller, OG-038 aufheller, OG-039 aufheller, OG-007 left
**Linien:** keine (schwarze Symbol-Kacheln, kein Planausschnitt)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · OG-Inventar: RIVO_Aufheller_Variante 18x (15 aus V053 + V055/V060 plausibel), RIVO_ARR_down 17x, RIVO_ARR_left 5x.
**Bewertung:** kein_regelgehalt

## S.238 · OG — Symbol- und Transformationsprüfung — V055-V057 (OG-010, OG-014, OG-019)
**Bereich:** Register Symboltausch Obergeschoss
**Bild:** Registerseite mit drei Original/Ergebnis-Paaren, kein Grundriss. V055: gelb-weißer Kreis-Spot mit Vertikal-Doppelpfeil (STANDARD_SPOT_SL) wird zum Kreis-Aufheller bei 90°. V056: STANDARD_RZ_PU (Aufwärtspfeil) wird zu RIVO_ARR_down bei 180° für sechs Positionen (OG-014, OG-017, OG-023, OG-025, OG-027, OG-029). V057: STANDARD_RZ_PU (Rechtspfeil hochkant) wird zu RIVO_ARR_down bei 90°.
> „STANDARD_RZ_PU → RIVO_ARR_down · Positionen: OG-014, OG-017, OG-023, OG-025, OG-027, OG-029“
**Leuchten im Bild:** OG-010 aufheller, OG-014 down, OG-017 down, OG-023 down, OG-025 down, OG-027 down, OG-029 down, OG-019 down
**Linien:** keine (schwarze Symbol-Kacheln, kein Planausschnitt)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · OG-Inventar: RIVO_ARR_down 17x — die 7 hier gelisteten down-Positionen passen ins Band; Aufheller_Variante 18x.
**Bewertung:** kein_regelgehalt

## S.239 · OG — Symbol- und Transformationsprüfung — V058-V060 (OG-021, OG-022, OG-024)
**Bereich:** Register Symboltausch Obergeschoss
**Bild:** Registerseite mit drei Original/Ergebnis-Paaren, kein Grundriss. V058: STANDARD_RZ_PU (Linkspfeil hochkant) wird zu RIVO_ARR_down bei 270°. V059: STANDARD_RZ_PLPR (zwei Rechtspfeile) wird zu RIVO_ARR_bothsided bei 180°. V060: gelb-weißer Kreis-Spot mit Horizontal-Doppelpfeil (STANDARD_SPOT_SL) wird zum grünen Kreis-Aufheller bei 0°.
> „STANDARD_RZ_PLPR → RIVO_ARR_bothsided · Bestandsskalierung [0.7, 0.7, 0.7]“
**Leuchten im Bild:** OG-021 down, OG-022 beidseitig, OG-024 aufheller
**Linien:** keine (schwarze Symbol-Kacheln, kein Planausschnitt)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · OG-Inventar: RIVO_ARR_bothsided 4x (n_beidseitig_gruppen=4), down 17x, Aufheller 18x — konsistent.
**Bewertung:** kein_regelgehalt

## S.240 · OG — Symbol- und Transformationsprüfung — V061-V063 (OG-026, OG-028, OG-030)
**Bereich:** Register Symboltausch Obergeschoss
**Bild:** Registerseite mit drei Original/Ergebnis-Paaren, kein Grundriss. V061: STANDARD_RZ_PLPR (Doppel-Aufwärtspfeil) wird zu RIVO_ARR_bothsided bei 270°. V062: STANDARD_RZ_PU wird zu RIVO_ARR_down bei schräger Bestandsrotation 96°, unverändert erhalten. V063: STANDARD_RZ_PU (Abwärtspfeil) wird zu RIVO_ARR_down bei 0° für fünf Positionen OG-030 bis OG-034.
> „V062 · OG-028 · 96° · ersetzt“
> „Positionen: OG-030, OG-031, OG-032, OG-033, OG-034“
**Leuchten im Bild:** OG-026 beidseitig, OG-028 down, OG-030 down, OG-031 down, OG-032 down, OG-033 down, OG-034 down
**Linien:** keine (schwarze Symbol-Kacheln, kein Planausschnitt)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · OG-Inventar: rot_deg 96.0 im DXF bestätigt (einziger schräger OG-Winkel); down 17x, bothsided 4x.
**Bewertung:** kein_regelgehalt

## S.241 · OG — Symbol- und Transformationsprüfung — V064-V065 (OG-036, OG-040), Registerende
**Bereich:** Register Symboltausch Obergeschoss, letzte Varianten
**Bild:** Letzte Registerseite mit nur zwei Original/Ergebnis-Paaren, kein Grundriss. V064: STANDARD_RZ_PL (Abwärtspfeil hochkant) wird zu RIVO_ARR_left bei 90°. V065: STANDARD_RZ_PL (Aufwärtspfeil hochkant) wird zu RIVO_ARR_left bei 270°. Damit endet das Variantenregister bei V065; Skalierung jeweils 0.6.
> „STANDARD_RZ_PL → RIVO_ARR_left · Bestandsskalierung [0.6, 0.6, 0.6]“
**Leuchten im Bild:** OG-036 left, OG-040 left
**Linien:** keine (schwarze Symbol-Kacheln, kein Planausschnitt)
**DXF-Abgleich:** OG_RIVO_Erklaerung.dxf · Handles — · OG-Inventar: RIVO_ARR_left 5x (OG-001, OG-007, OG-036, OG-040 + Legendenmuster plausibel); Rotationen 90/270 vorhanden.
**Bewertung:** kein_regelgehalt

## S.242 — Prüfstand und fachlicher Abschluss
**Bereich:** Schlussseite: durchgeführte Dateiprüfung und offene Projektprüfung
**Bild:** Reine Textseite ohne Planausschnitt. Beschreibt den begrenzten Eingriff in die Original-DXF (nur registrierte INSERT-Transformationen/Blocknamen, Bibliotheksergänzungen, Legendenbeispiele, Blocktabellenzahl, Handle-Zähler; unbeteiligte Objekte byteweise verglichen) und die maschinelle Nachprüfung mit ezdxf plus visueller Renderkontrolle. Oranger Warnblock: AutoCAD-Abnahme, Prüfung an der realen Anlage, Beleuchtungsberechnung/Messung, Batterie-/Stromkreis-/Funktionserhaltsnachweis und rechtliche Projektgeltung wurden NICHT durchgeführt. Offene Punkte: Sicht auf die Schmalseite beidseitiger Zeichen, Podest-/Höhenfolgen, Räume ohne zusätzliche Sicherheitsleuchte, Produkt-/Kombifunktionen, südlicher Bestandsanschluss.
> „Ein erfolgreicher Parserlauf ersetzt diese Prüfungen nicht.“
> „0 grafisch unveränderte Leuchtenpositionen sind im Register begründet.“
> „Weitere offene Punkte umfassen Sicht auf die Schmalseite beidseitiger Zeichen [...]. Lichttechnische und bauliche Nachweise bleiben auch nach vollständigem grafischem Symboltausch offen.“
**Linien:** keine (Textseite mit orangem Hinweisblock)
**DXF-Abgleich:**  · Handles — · Abschluss-Textseite, kein Planausschnitt; verweist auf PRUEFBERICHT.md, OFFENE_PUNKTE.md, INPUT_MANIFEST.json, PRUEFSUMMEN.txt.
**Bewertung:** kein_regelgehalt
