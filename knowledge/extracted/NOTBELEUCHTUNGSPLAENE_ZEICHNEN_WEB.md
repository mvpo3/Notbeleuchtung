<!-- Quelle: ultracode-Web-Recherche-Workflow (7 Angles, adversarial verifiziert), 2026-09-09.
     NICHT autoritativ fuer Norm-Werte — autoritativ bleibt src/notbeleuchtung/normwissen/data/*.yaml (Enis). -->

# Wissens-Digest: Notbeleuchtungspläne zeichnen — Recherche-Erweiterung

**Stand:** 2026-09-09 · **Scope:** ÖNorm/EN 1838 (AT-Fokus, DACH-relevant) · **Status-Filter:** Nur adversarial als **BESTÄTIGT** verifizierte Aussagen sind Fakt-übernommen; Zweifelhaftes ist unten separat gelistet.

> **WARNUNG (bindend):** Alle Norm-WERTE hier sind Recherche-Ergebnis, **nicht autoritativ**. Autoritativ bleibt allein Enis' `src/notbeleuchtung/normwissen/data/*.yaml` (`[BELEGT]`-Marker am Norm-Original). Dieser Digest ist Eingabe für Enis' Pflege, kein Ersatz.

---

## 1. Plan-Zeichenkonventionen & Symbolik

- **Rettungszeichen-Leuchtdichte (EN 1838, beleuchtete/hinterleuchtete Schilder):** Sicherheitsfarbe (grün) auf gesamter Fläche **≥ 2 cd/m²**; Lmax/Lmin **innerhalb einer Farbfläche ≤ 10:1**; Kontrast weiß↔Sicherheitsfarbe **≥ 5:1 und ≤ 15:1** (https://www.glamox.com/en/pbs/application-guide/emergency-lighting/rules-and-regulations/safety-signs/ · https://www.299lighting.co.uk/en/safety-signs-in-bs-en-1838-2013-emergency-lighting).
- **Erkennungsweite l = z·h:** z = **100 extern angestrahlt / 200 hinterleuchtet**; hinterleuchtet = doppelte Erkennungsweite bei gleicher Zeichenhöhe (https://www.licht.de/de/lichtthemen/notbeleuchtung/sicherheitszeichen).
- **Fluchtweg-Gleichmäßigkeit max/min ≤ 40:1** (EN 1838, Fluchtweg und Antipanik) (https://www.299lighting.co.uk/en/safety-signs-in-bs-en-1838-2013).
- **Kennzeichnungsschild an jeder SL (DIN VDE 0100-560):** rotes Zeichen mit Anlage-/Kreis-/Leuchtennummer; **Ø ≥ 30 mm ist nur die absolute Untergrenze** — praxisüblich **40 mm (bis 3,5 m Montagehöhe), 70 mm (bis 6 m)** (https://www.licht.de/de/lichtthemen/notbeleuchtung/sicherheitszeichen · schilder-klar.de / er-elektronik.de).
- **DIN 4844-1 „≥ 80 lx" gilt für NORMALbetrieb (Netz)**, nicht generell; im Notbetrieb ≈ 30 lx auf dem Schild; außen ≥ 50 lx (bevorzugt 80) normal / ≥ 5 lx Notbetrieb (https://www.licht.de/de/lichtthemen/notbeleuchtung/sicherheitszeichen).

## 2. Normrahmen & Pflicht-Gebäude (DACH)

- **Österreich — TRVB E 102 (2005) zurückgezogen per 08.07.2021.** Maßgeblich jetzt OIB-Richtlinie 2 + OVE E 8101 + OVE-Richtlinie R 12-2 + ÖNORM EN 1838 / EN 50172. TRVB E 102 nur noch als historische/optionale LB-Referenz führen (https://din-notlicht.com/de-at/vorschrift/elektrotechnische-und-lichttechnische-vorschriften/trvb-e-102/ · https://ltg.at/notbeleuchtung/).
- **AT Fluchtweg-Geometrie (OVE E08):** von jedem Punkt **≤ 10 m Verkehrsweg bis zum Fluchtweg**, **≤ 40 m Gesamtfluchtweglänge** bis gesicherter Bereich (https://www.ove.at/fileadmin/userdaten/docs/fachinformationen/Fachinfo_E-08_Sicherheitsbeleuchtung_Arbeitsstaetten_2021-04.pdf).
- **AT Umschaltverhalten (OVE E08):** 50 % in ≤ 5 s, 100 % in ≤ 60 s; Fluchtweg-Minimum i.d.R. 1 lx; besondere Gefährdung ≤ 0,5 s, ≥ 10 % der Allgemeinbeleuchtung, **≥ 15 lx** (ebd.).
- **AT Stromkreis-Regel (OVE E08):** **max. 20 Leuchten je Endstromkreis**, Fluchtweg-Leuchten **alternierend auf ≥ 2 Stromkreise** (ebd.). — Validiert unser bestehendes Cap-20-Digest.
- **AT Raumflächen-/Tageslicht-Trigger (OVE E08 Tabelle 1, 4-Band-Matrix):**
  - **< 30 m²:** ohne Tageslicht → nachleuchtende Orientierungshilfen; mit Tageslicht → keine Ausstattung
  - **30–100 m²:** ohne Tageslicht → nachleuchtende Orientierungshilfen; **mit Tageslicht → Sicherheitsleuchten**
  - **> 100–1600 m²:** ohne Tageslicht → Orientierungshilfen und/oder Sicherheitsleuchten; **mit Tageslicht → Sicherheitsleuchten**
  - **> 1600 m²:** beide Spalten → Sicherheitsleuchten

  (Quelle: OVE E08 Volltext Tabelle 1.) **ACHTUNG — Achsen NICHT verwechseln:** SL werden bei **Tageslicht-Räumen schon ab 30 m²** verlangt, bei **Räumen ohne Tageslicht erst ab > 1600 m²** zwingend. Trigger muss beide Achsen (Fläche + `natuerliche_belichtung`) an die 4-Band-Matrix koppeln, nicht an zwei Einzelschwellen.
- **DE Betriebsdauer ist gebäude-/nutzungsabhängig (nicht global):** Beherbergungsstätten/Heime und **Wohnhochhäuser = 8 h**; **3 h zulässig, wenn geschaltetes Dauerlicht mit Leuchttaster + selbsttätig ausschaltendem Zeitlicht** (https://library.e.abb.com/public/2e03924857f347d08e1094795360fb00/2CDC910011B0101.pdf · licht.de bestätigt).

## 3. Platzierungs-/Bemessungs-Methodik

- **Fluchtweg-Mittellinie (EN 1838 §4.2.1):** ≥ 1 lx an allen Punkten der Mittellinie (Weg bis 2 m breit); mittleres Band (≥ 50 % der Wegbreite) ≥ 0,5 lx; breitere Wege als mehrere 2-m-Streifen behandeln. **Mittellinie und Band sind getrennt nachzuweisen** (https://www.rp-group.com/sicherheitsbeleuchtung-lichttechnische-anforderungen · philippayne.co.uk; deckungsgleich mit `en1838_grundwerte.yaml` `[BELEGT]`).
- **Antipanik / offene Fläche (§4.3):** ≥ 0,5 lx auf der Kernfläche, umlaufender **0,5-m-Randstreifen** ausgeschlossen; Gleichmäßigkeit ≤ 40:1 (ebd.).
- **Pflicht-Platzierungspunkte:** SL zwingend an jeder Notausgangstür, an Treppen (jeder Lauf), an jeder Niveau- und Richtungsänderung, an Gang-Kreuzungen, an Erste-Hilfe-/Brandbekämpfungseinrichtungen (https://www.299lighting.co.uk/en/emergency-escape-lighting-in-bs-en-1838-2013).
- **„Nahe" = ≤ 2 m horizontal** (Leitfaden-Konvention, trägt operabel als „erste Leuchte ≤ 2 m"-Regel) (ebd.).
- **5 lx vertikal an Sicherheitseinrichtungen** (Brand-/Handfeuermelder, Feuerlöscher, Erste-Hilfe) (ebd.).
- **Zeitverhalten Fluchtweg/Antipanik:** 50 % in ≤ 5 s, 100 % in ≤ 60 s; Betriebsdauer ≥ 1 h (ebd.).
- **Arbeitsplätze mit besonderer Gefährdung:** Wartungswert ≥ 10 % der Nennbeleuchtung, aber **≥ 15 lx**; Umschaltung **≤ 0,5 s** (NUR Hochrisiko, nicht mit 5 s/60 s des Fluchtwegs verwechseln) (ebd.).

## 4. Lichtberechnung / Photometrie / Nachweis

- **Punktlichtstärke-Methode:** `E = (I · cos³θ) / d²` (I = Lichtstärke in cd in Ausstrahlrichtung, θ = Winkel zur Vertikalen, d = Montagehöhe); Beiträge mehrerer Leuchten je Rasterpunkt superponiert. Rechenbeispiel (I=200 cd, θ=10°, h=2 m → **47,76 lx**) mathematisch verifiziert (Formel-Beleg: Electrical4U / CCS / electrical-knowhow — **nicht** connectedlight, s. Widersprüche).
- **Blendungsbegrenzung — Imax je Montagehöhe (60°–90°-Zone gegen die Senkrechte), oft übersehener Gate:** h ≤ 2,5 m → **500 cd**; 2,5–3 m → **900**; 3–3,5 m → **1.600**; 3,5–4 m → **2.500**; 4–4,5 m → **3.500**; > 4,5 m → **5.000 cd**. Für Arbeitsplätze mit Gefährdung verdoppelt (1.000/1.800/3.200/5.000/7.000/10.000 cd) (https://www.licht.de/fileadmin/Publikationen_Downloads/1603_lw10_Notbeleuchtung_web.pdf).
- **Gleichmäßigkeit:** Emax:Emin ≤ 40:1 Fluchtweg; **10:1 Arbeitsplätze mit besonderer Gefährdung** (ebd.).
- **Reflexionsgrade = 0 als Nachweisstandard:** DIALux-evo-Notlichtmodul rechnet im Default **ohne Reflexionen und ohne Möblierung** — im Bericht ausdrücklich „Reflexion 0 %" ausweisen (https://www.dial.de/de-DE/presse/not-und-sicherheitsbeleuchtung-mit-dialux-evo-planen).
- **EN-50172-Re-Verifikation:** photometrischer Nachweis nach EN 1838 (Annex B) in Intervallen **≤ 5 Jahre** wiederholen (https://connectedlight.co.uk/photometric-verification-for-emergency-lighting/).

## 5. Software & Werkzeuge der Praxis

- **DIALux evo** plant Not-/Sicherheitsbeleuchtung erst ab **evo 10**; photometrische Grundlage **DIN EN 1838:2019-11** + ASR A2.3/A3.4 (2022-03). **Hinweis:** DIN EN 1838 ist seit **März 2025 durch DIN EN 1838:2025-03 ersetzt** (2019-11 nur noch für laufende Planung) (https://www.dial.de/de-DE/presse/not-und-sicherheitsbeleuchtung-mit-dialux-evo-planen · licht.de 2025-03).
- **DIALux-Berechnungsflächen als eigene Objekte:** Fluchtweg (Linienanordnung), Antipanik-Fläche (autom. Gleichverteilung, einstellbare Randzone), gefährdete Arbeitsplätze, hervorgehobene Zonen — je mit eigener Breite/Randzone; kreuzende Fluchtwege werden verschmolzen (https://www.dialux.com/en-GB/emergency-lighting).
- **Notlichtstrom ODER Notlicht-Faktor** je Leuchte, ineinander umrechenbar (https://www.dial.de/de-DE/presse/not-und-sicherheitsbeleuchtung-mit-dialux-evo-planen).
- **DIALux-DWG-Export-Layerschema:** Präfix **`DLX_`**, Hierarchie **`BLD0_…BLD3_`** (Gebäude) / **`FL0_…FL2_`** (Geschoss), z. B. `DLX_BLD0_FL1_CONT`; WYSIWYG (2D-View→2D-DWG); **eine DWG je Lichtszene** (https://evo.support-en.dial.de/support/solutions/articles/9000073182-dwg-export).
- **DIN ISO 23601 Flucht-/Rettungsplan = separates Deliverable** (nicht der Elektroplan): Maßstab **1:100** (klein/mittel), **1:250** (groß), **1:350** (Einzelraum); Format **A3** (A4 Einzelraum); Sicherheitszeichen **≥ 7 mm**, Text **≥ 2 mm**, Standort-Marker blau Ø **≥ 7 mm**, Außenwände **≥ 1,6 mm**, Innenwände ≥ 0,6 mm Strichstärke; ISO-7010-Symbole, ISO-3864-1-Farben (https://www.feuertrutz.de/erstellung-von-flucht-und-rettungsplaenen-nach-din-iso-23601-09092019).
- **Plan-Standort selbst braucht Sicherheit:** aushängender Flucht-/Rettungsplan im Blackout entweder langnachleuchtend (ISO 17398 mind. Klasse C) ODER mit **≥ 5 lx vertikal** beleuchtet — d. h. Aushang-Standort ist eigener POI-Typ „Sicherheitseinrichtung" (ebd.).

## 6. Zeichnungs-Workflow & Best Practices & Fehler

- **EN 1838 Fluchtweg (licht.de, wörtlich):** Mittellinie ≥ 1 lx; Messung bis 20 cm über Laufebene (ASR A3.4/3), besser bodennah; Bezug 2 m Wegbreite; seitlicher Abfall max. 50 % nach 0,5 m; Gleichmäßigkeit ≤ 40:1; **auf Treppen/nicht-horizontalen Wegen gelten die Blend-Grenzwerte bei ALLEN Winkeln** (horizontal nur 60°–90°) (https://www.licht.de/de/lichtthemen/notbeleuchtung/sicherheitsbeleuchtung/fluchtwege).
- **Häufigster Blindfleck:** Feuerlöscher/Erste-Hilfe (5 lx) und die Zone unmittelbar am/hinter dem Notausgang + am sicheren Bereich werden am häufigsten übersehen (https://www.saxonia-licht.de/not-und-sicherheitsbeleuchtung-diese-fehler-sehen-wir-leider-viel-zu-oft/).
- **Max. 20 Leuchten je Endstromkreis (DIN VDE 0100-560)** — **plus ≤ 60 % des Bemessungsstroms des vorgeschalteten Überstromschutzorgans** (die 60-%-Regel ergänzt die reine Stückzahl; verankert in DIN VDE 0100-560, nicht primär EN 50172).
- **Installations-Fehlerklassen (Prüferpraxis):** (a) RZ direkt über der Tür lässt Boden davor dunkel → RZ-Erkennbarkeit ≠ Fluchtweg-Bodenlux, getrennte Nachweise; (b) Notleuchte an geschalteter statt ungeschalteter Leitung → Akku entlädt lautlos; (c) „leuchtet ja" ≠ konform (toter Akku bleibt im Netzausfall dunkel — Messung statt Sichturteil) (https://www.paclights.com/learning-center/emergency-egress-lighting-codes-what-you-need-to-know-for-compliance/).

## 7. Kennzeichnung, Leitsysteme, dynamische Fluchtweglenkung

- **DIN ISO 23601 Flucht-/Rettungsplan ≠ Notbeleuchtungs-Elektroplan** — grafisches Orientierungsdokument (Betrachterstandort, Fluchtwege, Feuerlöscher, AED, Sammelplatz, Verhaltensregeln), ISO-7010/ISO-3864-1 (https://din-notlicht.com/de-at/vorschriften/faq/ · https://www.fluchtplan24.de/informationen/gestaltung-flucht-und-rettungsplan-din-iso-23601/).
- **Rettungsplan als „hervorgehobene Stelle" (EN 1838 Kap. 6.3.2, Fassung 2025):** min. **5 lx vertikal** ODER min. **2 cd/m² hinterleuchtet** (https://din-notlicht.com/de-at/vorschriften/faq/).
- **Langnachleuchtende Materialien (DIN 67510 / ASR A3.4/3):** min. **80 mcd/m² @ 10 min** und **12 mcd/m² @ 60 min**; Schmalvariante 2,5 cm (statt 5 cm) → erhöht **100/15 mcd/m²**; Mindestklasse C (https://vorschriften.bgn-branchenwissen.de/daten/tr/asr_a3_4_3/5.htm).
- **Bodennahe optische Leitsysteme (ASR A3.4/3):** Oberkante ≤ 40 cm über Boden; Bodenmarkierung ≥ 5 cm Kantenlänge, **≥ 3 Markierungen/m**; Sicherheitszeichen entlang Fluchtweg **≤ 10 m Abstand** (ebd.).
- **Elektrisches Leitsystem (ASR A3.4/3):** min. **1 lx, gemessen 20 cm über Boden** (50 cm von der Wand), Gleichmäßigkeit < 40:1, Betriebsdauer ≥ 60 min; **beidseitig markieren, wenn Verrauchung nicht ausschließbar UND Fluchtwegbreite > 3,60 m** (ebd.).
- **DIN 14036:2023-12 — Dynamische/Adaptive Fluchtweglenkung:** DFWL (dynamisch) vs. AFWL (adaptiv, informativ); deckt Planung/Montage/Inbetriebnahme/Abnahme/Betrieb (https://www.dgwz.de/normen/din-14036-dynamische-adaptive-fluchtweglenkung · https://www.feuertrutz.de/dynamische-und-adaptive-fluchtweglenkung-din-14036-erschienen-02112023).
- **BMA-Kopplung:** Brandmeldeanlage detektiert je Brandabschnitt und schaltet an das Leitsystem, das adressierbare dynamische Leuchten ansteuert; kompromittierter Abschnitt wird „visuell geschlossen", Route herumgeführt (https://www.inotec-licht.de/en/practice/dynamic-escape-routing/).
- **CEN/TS 17951:2024 „Adaptive Emergency Escape Lighting Systems"** existiert als europäische TS (Scope: adaptive Steuerung von Lichtstrom, Fluchtrichtung, Zeichen-Bedeutung nach Situationsinputs) — künftige Norm-Quelle für `normwissen`, adaptiv haben wir noch nicht (https://standards.iteh.ai/catalog/standards/sist/7fca80cc-26d3-4332-8fca-318358c26626/sist-ts-cen-ts-17951-2024).

---

## NEU für unsere Engine

Konkreteste Erweiterungen gegenüber unserem Bestand (EN-1838-Kernwerte, l=z·h, 5 lx, OVE-Stack, Wartungsfaktor 0,80, DIN-SIBEL-Layer):

1. **Blendungs-Gate Imax je Montagehöhe (500/900/1.600/2.500/3.500/5.000 cd im 60°–90°-Band).** Aus den vorhandenen Hersteller-LDT direkt prüfbar → neue automatische Gate-Regel analog zu den OVE-Hard-Stops. Auf Treppen bei ALLEN Winkeln, nicht nur 60°–90°.
2. **RZ-Leuchtdichte-Gleichmäßigkeit am Schild selbst** (≥ 2 cd/m² grün, Lmax/Lmin ≤ 10:1 innen, Kontrast 5:1…15:1) — eigener Nachweis über die reine Fluchtweg-Ud-Regel hinaus, Kandidat für Guard bei hinterleuchteten RZ.
3. **OVE-E08-4-Band-Trigger (Fläche × Tageslicht)** als raumgenaue Platzierungs-Regel — koppelt an Selmans Raumfläche + neues `natuerliche_belichtung`-Flag. Zwischen den Bändern sind nachleuchtende Orientierungshilfen normkonforme Alternative (Rolle ≠ Produkt).
4. **Betriebsdauer als raumtyp-/gebäudetyp-getriebenes Feld (1/3/8/24 h)** statt Konstante; 8 h für Beherbergung/Heime/Wohnhochhaus, 3-h-Reduktion nur als LB-/Konzept-Option (Leuchttaster + Zeitlicht).
5. **Mittelband-Nachweis getrennt von der Mittellinie** (≥ 0,5 lx über dem mittleren 50-%-Band) + bei Weg > 2 m automatisch auf Antipanik umschalten/splitten.
6. **Reflexion 0 % + Notlicht-Faktor als getrennte, ausgewiesene Multiplikatoren** im lux-Bericht (WF × Notlicht-Faktor separat, nicht vermengt).
7. **Bodennahe Leitsystem-Ebene** (OK ≤ 40 cm, Messhöhe 20 cm, 1 lx, U < 40:1, ≥ 3 Marker/m, Zeichen ≤ 10 m) als zusätzliche Platzierungs-Ebene UNTER den Wand-RZ — Trigger „Verrauchung nicht ausschließbar"; beidseitig ab Wegbreite > 3,60 m.
8. **Kennzeichnungsschild-Geometrie montagehöhen-abhängig** (40 mm bis 3,5 m / 70 mm bis 6 m; 30 mm nur Untergrenze) für das `circuit_hint`-Rendering — bisher nur Textblock ohne Schildgeometrie.
9. **Zweiter Ausgabe-Modus DIN ISO 23601** (Flucht-/Rettungsplan, ISO-7010/3864-1, A3/1:100/1:250/1:350, Sammelplatz E007, Betrachterstandort) — eigener Rendering-Pfad, wiederverwendet Selmans Raumerkennung, NICHT mit dem DIN-SIBEL-Elektroplan vermischen.
10. **DIALux-kompatibler DWG-Export-Adapter** (`DLX_`/`BLD_`/`FL_`-Layerschema) als optionaler zweiter Ausgabekanal für DIALux-gewohnte Prüfer.
11. **Prüf-Metadaten am Plan/Prüfvermerk:** max-20-Kreis **+ ≤ 60 % Bemessungsstrom**; EN-50172-Re-Verifikation ≤ 5 Jahre. Macht den Plan „prüferfertig".
12. **Dynamische Fluchtweglenkung (DIN 14036) als optionaler LB-Modus** — RZ-Leuchten brauchen dann ein Richtungs-Zustandsmodell (alternative Pfeilrichtung + Kreuz/Sperrsymbol) + BMA-Brandabschnitt-Zuordnung + Invariante „hochliegend == bodennah gleiche Richtung".

## Engine-Kandidaten (Owner-Zuordnung)

> **Norm-WERTE = Recherche, nicht autoritativ.** Vor Einbau in Logik übernimmt Enis den Wert exakt in `normwissen/data/*.yaml` (`[BELEGT]` am Norm-Original). Leonis parst nie YAML, sondern fragt `NormProvider`.

**Enis (`normwissen/`, autoritative Werte + LB-Parsing):**
- Blendungs-Imax-Tabelle je Montagehöhe (inkl. Verdopplung Hochrisiko) als Norm-Regel.
- RZ-Leuchtdichte-Fenster (2 cd/m², 10:1, 5:1…15:1) und ≥ 5 lx / 2 cd/m² für „hervorgehobene Stellen"/Aushang-Plan.
- OVE-E08-4-Band-Matrix (Fläche × Tageslicht) als Auslöse-Regel; TRVB E 102 als „historisch/zurückgezogen" markieren.
- Betriebsdauer-Klassen 1/3/8/24 h + 3-h-Reduktionsbedingung.
- Kreis-Regel max-20 **+ 60-%-Bemessungsstrom** (DIN VDE 0100-560).
- ASR-A3.4/3-Werte für bodennahe/elektrische Leitsysteme + langnachleuchtend (mcd/m²-Klassen).
- Neue Quellen aufnehmen: DIN EN 1838:2025-03, CEN/TS 17951:2024, DIN 14036:2023-12.
- LB-Modi: „beleuchtet vs. hinterleuchtet" (dedizierte Anstrahl-SL je Schild), „dynamische Fluchtweglenkung".

**Leonis (`platzierung/`):**
- Mittelband-Nachweis + Weg->2-m-Split; „nahe" = ≤ 2 m operabel; SL bis über die Ausgangsschwelle + in den Zielbereich ziehen (Blindfleck-Regel).
- Blendungs-Gate aus LDT konsumieren (Werte via NormProvider).
- Bodennahe Leitsystem-Ebene als zweite Platzierungs-Strategie unter Wand-RZ.
- Antipanik = autom. Gleichverteilung mit 0,5-m-Randabzug; Fluchtweg = Linienanordnung (bestätigt bestehende Zwei-Strategien-Trennung).
- Kennzeichnungsschild-Geometrie montagehöhen-abhängig im circuit_hint-Rendering.

**Selman (`raumerkennung/`):**
- `natuerliche_belichtung`-Flag je Raum (Achse des OVE-4-Band-Triggers).
- Fluchtweg-Flächentypen als First-Class-Objekte (Mittellinie + Breite, Antipanik-Polygon mit Randabzug) statt reiner Raum-Lux-Prüfung.
- Weglängen-Daten (≤ 10 m / ≤ 40 m) als Grundlage der (bislang vertagten) N2-Weglängen-Deckung.

**Hauptengine (`hauptengine/`, gemeinsam):**
- Zweiter Ausgabe-Modus DIN ISO 23601 (eigener Render-Pfad).
- DIALux-kompatibler DWG-Export-Adapter.
- Prüf-Metadaten/Prüfvermerk (Re-Verifikations-Intervall, Kreis-Regeln).

## Widersprüche / Offen (nicht ungeprüft übernehmen)

- **DL/BL-Symbolik (Dreieck=DL, Kreuz-Kreis=BL) ist NICHT genormt** — einquellig (elektro.net), aber richtungskonsistent mit unserer Referenz-Praxis. Weiter als **Konvention** labeln (`norm_quelle` = Konvention, nicht EN/DIN), nicht als Norm-Zwang.
- **60 m² Antipanik-Schwelle / 8 m² Zwei-Quellen-Ausnahme sind NICHT EN 1838** — kursieren in UK-Design-Guides, unsere autoritative `en1838_grundwerte.yaml` stellt ausdrücklich klar: EN 1838 kennt keine flächenbezogene Auslöse-Schwelle. Flächen-Trigger existieren, aber SCOPE-gebunden in OVE E 8101 / ÖVE E 8002-1. Für AT-Projekte kein EN-1838-Fakt.
- **„EN 1838:2024 kippt das Mittellinien-Prinzip → ganze Wegbreite"** — **unbestätigt/überzogen**; die zitierte Quelle belegt nur eine Mess-Ausschluss-Methodik, keinen Prinzipwechsel. Nicht als Norm-Aussage übernehmen.
- **Messhöhe „2 cm über Boden"** — **unbestätigt** als EN-1838-Wert; EN 1838 misst „auf dem Boden", die 20 cm stammen aus ASR A3.4/3. Nicht vermischen.
- **Uniformität „10:1" für Hochrisiko als Emax:Emin** — Maß-Bezeichnung fragwürdig; §4.4.2 arbeitet mit Uo ≥ 0,1 (kleinste:mittlere), nicht Ud. Wert plausibel, Maß vor Einbau klären.
- **EN-62034-Typklassen „S/P/ER/PRN"** — **unbestätigt**; Quellen nennen uneinheitlich P/ER/PER/S bzw. AT/STS/ST. „PRN" vermutlich falsch → „PER". Vor Aufnahme gegen DIN EN 62034 (VDE 0711-400):2013-02 im Original prüfen.
- **„Wechseltest-Verbot bei Zentralbatterie / Dauertest zwingend unter Volllast"** — **unbestätigt** (an zitierter Quelle nicht auffindbar, keine Zweitquelle). Plausibel als Ingenieurslogik, nicht als Fakt führen.
- **DC-Spannung 24 V/48 V für Zentralbatterie-Kreise** — Herstellerpraxis, nicht norm-verifiziert.
- **Erkennungsweite-Faktor „100 = hinterleuchtet" (Angle 7)** — die dortige Einzelquelle stützt die hinterleuchtet/beleuchtet-Aufschlüsselung NICHT; verlässlich bleibt die z=100 extern / z=200 hinterleuchtet-Zuordnung aus Angle 1/3 (`[BELEGT]` §5.5).
- **DFWL/AFWL-Feindefinition + „Annex B" + CEN/TS-17951↔EN-50172-Kopplung** — **unbestätigt** in den Primärquellen; DIN 14036 und CEN/TS 17951 existieren, aber Feindetails vor Einbau gegen Originalnorm prüfen.
- **ISO 3864-1 „Sicherheitsfarbe ≥ 50 % der Zeichenfläche" / E001–E024** — in dieser Runde nicht hart gegengeprüft; als noch-nicht-hart einstufen.
