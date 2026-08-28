# Sicherheitsvorschriften Elektro — „Elektrotechnische Sicherheitsvorschriften als Voraussetzung für den Gewerbezugang", Dipl.-HTL-Ing. Ing. Dietmar Stöger, WIFI Österreich (Wirtschaftskammer), Auflage 4.0 / Juli 2019
**Quelle:** knowledge/Sicherheitsvorschriften_Elektro (1).pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf; vertieft: Notbeleuchtungs-relevante Kapitel

## Charakter des Dokuments

**Schulungsunterlage / Kursskript** — keine Norm, keine Verordnung. Herausgeber ist das
WIFI Österreich (Bildungsträger der Wirtschaftskammer), Zweck ist die Ausbildung zum
**Gewerbezugang Elektrotechnik** (Impressum S. 2: „als Voraussetzung für den Gewerbezugang",
„alle Angaben trotz sorgfältiger Bearbeitung ohne Gewähr", Haftung ausgeschlossen; basiert
auf WIFI-Skript Version 12.0 von 2012). Das Skript **referiert** österreichische Gesetze
(ETG 1992, ETV 2002, ESV 2012) und Normen (ÖVE E8001, ÖVE E8101, ÖVE-Richtlinien) in
Auszügen und didaktischer Aufbereitung.

**Einordnung in die Engine-Hierarchie:** Das Dokument selbst ist **nicht rechtsverbindlich**
und **keine Norm-Primärquelle**. Es rangiert unterhalb von „Referenz-Praxis" — brauchbar als
**Norm-Landkarte** (welche ÖVE-Norm regelt was, welches Regelwerk hat welche ablöste) und als
Plausibilisierung, aber **kein Wert aus diesem Skript darf als `norm_quelle` für eine
Platzierungsentscheidung dienen**. Für zitierfähige Werte immer die Primärnorm (EN 1838,
ÖVE E8101, ÖVE E 8002, TRVB E 102) heranziehen.

## Relevanz für die Engine

**Gering bis null für die Platzierungslogik.** Das Skript behandelt auf 167 Seiten fast
ausschließlich Personenschutz gegen elektrischen Schlag (Schutzmaßnahmen, Nullung, FI, Netz-
systeme, Erdung, Prüfung). Es enthält **keinen einzigen Abschnitt zu Notbeleuchtung,
Sicherheitsbeleuchtung, Fluchtwegen, Rettungszeichen oder EN 1838** — die Begriffe
„Notbeleuchtung", „Sicherheitsbeleuchtung", „Fluchtweg", „Rettungsweg", „Notausgang",
„EN 1838", „Antipanik", „Funktionserhalt" kommen im Volltext **nicht vor** (Grep-verifiziert).

Verwertbar ist ausschließlich der **normative Kontext**:

1. **Norm-Landkarte Österreich:** ÖVE E 8002 (Versammlungsstätten, alt EN2) und
   ÖVE E 8007 (medizinische Räume) wurden per 1. Jänner 2019 **in die ÖVE E8101 integriert**
   (S. 47). Für Sicherheitsanforderungen bei Menschenansammlungen ist heute also die
   E8101 das maßgebende Errichtungs-Regelwerk — relevant für Enis' `NormRegelwerk.quellen`.
2. **Struktur-Anker in E8001/E8101**, unter denen Notbeleuchtungs-nahe Errichtungsregeln
   stehen: E8001 Teil 4 §53 (Ersatzstromversorgungsanlagen), §57 (Elektrische Anlagen für
   Sicherheitszwecke); E8101 Kapitel 35 + 56 (Einrichtungen für Sicherheitszwecke),
   Abschnitt 559 (Leuchten und Beleuchtungsanlagen).
3. **Sicherheitskreis-Peripherie** (getrennter Sicherheitskreis lt. Mission): FI-Brandschutz
   I∆N ≤ 300 mA, AFDD-Einbaupflichten, verschärfte Prüfmaßstäbe für Notstromversorgungs-
   anlagen und Räume mit Menschenansammlungen.

## Dokument-Landkarte

167 Seiten (PDF), 31 Kapitel. Kapitelangaben = Skript-Kapitel (Druckseite lt. Fußzeile).

| Kap. | Titel (Druckseite) | Inhalt in 1–2 Zeilen | NB-relevant? |
|------|--------------------|----------------------|--------------|
| 1 | Entstehung der Schutzmaßnahmen und Normen (1) | Historie, Normungswesen, seit Jänner 2019 ist ÖVE E8101 maßgebend für Anlagenerrichtung. | indirekt |
| 2 | Wirkungen des Stromes (3) | Körperströme, Schwellenwerte (Wahrnehmung/Krampf/Gefahr/Tod), Herzkammerflimmern. | nein |
| 3 | Der Stromunfall (5) | Bergung, Erste Hilfe, Defibrillator, Schockbekämpfung. | nein |
| 4 | Arbeiten an elektrischen Anlagen (8) | Die 5 Sicherheitsregeln; „allseitig freischalten" umfasst auch Notstromgenerator/USV als zweite Anspeisung (S. 9). | nein |
| 5 | Einteilung des Fachpersonals (10) | Laie / unterwiesene Person / Elektrofachkraft; ABV, ALV, AB; Prüferanforderungen. | nein |
| 6 | Gesetzliche Grundlagen (13) | ETG, ETV, ESV, SNT-Vorschriften, ÖVE E8101, TAEV — österreichische Rechts-Pyramide. | indirekt |
| 7 | Elektrotechnikgesetz — Auszug (16) | ETG 1992 inkl. Novellen 2015/2017 (Auszug). | nein |
| 8 | Elektrotechnikverordnung — Auszug (26) | ETV2002 + A1/A2 + ETV2014: verbindlich erklärte Normen. | indirekt |
| 9 | Elektroschutzverordnung 2012 — Auszug (30) | ArbeitnehmerInnenschutz bei Elektroarbeiten. | nein |
| 10 | Standesregeln für Elektrotechnik — Auszug (39) | Berufsrecht/Standesregeln. | nein |
| 11 | Normenkurzüberblick (42) | Tabelle wichtiger ÖVE-Normen, u.a. **ÖVE E 8002** (Versammlungsstätten, alt EN2), EN50272 (Batterieanlagen). | **ja** |
| 12 | Die ÖVE/ÖNORM E8001 (43) | Aufbau der (2019 abgelösten) E8001; Teil 4 enthält **§53 Ersatzstromversorgungsanlagen** und **§57 Elektrische Anlagen für Sicherheitszwecke**. | **ja** |
| 13 | ÖVE Richtlinien (45) | R1–R27; u.a. R12 Brandschutz in el. Anlagen (Trafostationen/Schalträume). ÖVE-Richtlinien = anerkannte Regeln der Technik. | teilweise |
| 14 | Die ÖVE E8101 (47) | Aktuelles Errichtungs-Regelwerk (seit 1.1.2019, Basis HD 60364); **integriert E8001 + E8007 + E8002**; Struktur mit Kap. 35/56 „Einrichtungen für Sicherheitszwecke", 559 „Leuchten und Beleuchtungsanlagen". | **ja** |
| 15 | Einteilung der Betriebsmittel (51) | Schutzklassen I/II/III, IP-System (EN 60529). | nein |
| 16 | Kennzeichnung der Betriebsmittel (56) | Prüfzeichen (ÖVE etc.). | nein |
| 17 | Begriffe lt. ÖVE E8101 bzw. E8001 (58) | Begriffsdefinitionen: Anlagenteile, Fehlerarten, Fehlerspannungen. | nein |
| 18 | Die Netzsysteme (64) | TN/TT/IT, Leiterbezeichnung, Farbkennzeichnung; Erdung der Stromquelle inkl. Notstromaggregat. | nein |
| 19 | Der Überspannungsschutz (72) | SPD-Typen, Auswahl, Koordination. | nein |
| 20 | Einteilung des Schutzkonzeptes (79) | Basisschutz / Fehlerschutz / Zusatzschutz. | nein |
| 21 | Schutz gegen den elektrischen Schlag (84) | Anwendung und Einteilung der Schutzmaßnahmen. | nein |
| 22 | Die Fehlerschutzvorkehrungen (87) | Isolierung, SELV/PELV, Schutztrennung, Abschaltung TN/TT, Nullungsbedingungen. | nein |
| 23 | Der Fehlerstromschutzschalter (112) | FI-Aufbau, Typen (AC/A/F/B/PD/G/S); **23.4.4 Brandschutz: I∆N ≤ 300 mA, Einbau am Anfang der Leitungsanlage**. | Rand |
| 24 | Der Brandschutzschalter AFDD (121) | Fehlerlichtbogen-Erkennung; Einbaupflicht (Schlafräume Heime/Kindergärten, BE2-Räume) und Einbauempfehlung. | Rand |
| 25 | Der Potentialausgleich (123) | Haupt-/zusätzlicher Potentialausgleich, Querschnitte, Schutzleiter. | nein |
| 26 | Dokumentation (129) | Mindestumfang Anlagendokumentation, Prüfbericht. | nein |
| 27 | Überprüfung der Schutzmaßnahmen (132) | Erstprüfung/wiederkehrende Prüfung; **strengere Maßstäbe** u.a. für Räume mit Menschenansammlungen und Notstromversorgungsanlagen (S. 132). | Rand |
| 28 | Errichtung von Fundamenterdern (149) | Ausführung, Werkstoff, Kontrolle. | nein |
| 29–31 | Quellennachweis / Abbildungen / Schluss (152–155) | Verzeichnisse. | nein |

## Regel-Tabelle (maschinen-orientiert) — Notbeleuchtungs-relevante Inhalte

Hinweis: Alles Folgende sind **Sekundär-Aussagen eines Schulungsskripts** über Normen —
zitierfähig nur als Landkarte, nicht als `norm_quelle`.

| ID | Kapitel (Seite) | Regel | Werte/Grenzwerte | Typ |
|----|-----------------|-------|------------------|-----|
| SVE-R1 | Kap. 11, Normenkurzüberblick (S. 42) | ÖVE E 8002 regelt „Errichtung und Betrieb von Elektroanlagen in Versammlungsstätten usw." (alt EN2) — das ist das österreichische Regelwerk, unter dem Sicherheitsbeleuchtung in Versammlungsstätten historisch verortet ist. | — | Definition |
| SVE-R2 | Kap. 14 (S. 47) | Die ÖVE E8101 (gültig seit 1. Jänner 2019, Basis HD 60364) integriert die noch verbindlichen Teile der ÖVE-EN1/E8001, die ÖVE E8007 (medizinisch genutzte Räume) und die **ÖVE E8002 („Sicherheitsanforderungen bei Menschenansammlungen")**. E8101 ist die aktuelle anerkannte Regel der Technik. | Stichtag 01.01.2019 | Definition |
| SVE-R3 | Kap. 14.1 (S. 48–49) | Struktur-Anker in der ÖVE E8101: Teil 3 Kap. **35 „Einrichtungen für Sicherheitszwecke"**, Teil 3 Kap. 36 „Verfügbarkeit der Versorgung", Teil 5 Kap. **56 „Einrichtungen für Sicherheitszwecke"**, Abschnitt **559 „Leuchten und Beleuchtungsanlagen"**, 551 „Niederspannungsstromerzeugungseinrichtungen". Dort sind Sicherheitsstromversorgung/Sicherheitsbeleuchtungs-Errichtung zu suchen. | — | Definition |
| SVE-R4 | Kap. 12 (S. 44) | Struktur-Anker in der (Alt-)Norm ÖVE E8001 Teil 4: **§53 „Ersatzstromversorgungsanlagen und andere Versorgungsanlagen für den vorübergehenden Betrieb"** und **§57 „Elektrische Anlagen für Sicherheitszwecke"**; Teil 2 §32 „Leuchten und Beleuchtungsanlagen". Relevant für Bestandsanlagen (errichtet 2000–2018). | Geltung E8001: 2000–2018 | Definition |
| SVE-R5 | Kap. 11 (S. 42) | ÖVE EN 50272 regelt „Akkumulatoren und Batterieanlagen" — einschlägig für Batterieanlagen der Sicherheitsstromversorgung (Zentralbatterie). | — | Definition |
| SVE-R6 | Kap. 13 (S. 45) | ÖVE-Richtlinien (R1–R27) sind „ebenfalls anerkannte Regeln der Technik und somit anzuwenden"; u.a. R12 „Brandschutz in elektrischen Anlagen – Trafostationen und Räume mit Schaltanlagen". | — | Gebot |
| SVE-R7 | Kap. 23.4.4 (S. 116) | FI-Schutzeinrichtung für den **Brandschutz**: maximaler Auslösefehlerstrom und Einbauort am Anfang der Leitungsanlage. | I∆N ≤ 300 mA | Grenzwert |
| SVE-R8 | Kap. 23.4.3 (S. 116) | FI für den Zusatzschutz: I∆N ≤ 30 mA; ein RCD darf **nicht** gleichzeitig Fehlerschutz und Zusatzschutz erfüllen. | I∆N ≤ 30 mA | Verbot |
| SVE-R9 | Kap. 24.1.1 (S. 122) | AFDD-**Einbaupflicht** in Wechselstromkreisen bis 16 A Nennstrom: Schlafräume von Heimen für behinderte/alte Menschen, Schlafräume von Kindergärten, Räume mit Brandrisiko durch Materialien (Einstufung BE2). | ≤ 16 A Nennstrom | Gebot |
| SVE-R10 | Kap. 27.1 (S. 132) | Bei der Anlagenprüfung sind „besonders strenge Maßstäbe" anzulegen u.a. für: Räume mit größeren **Menschenansammlungen**, Spitäler, **Notstromversorgungsanlagen**, feuer-/explosionsgefährdete Räume. | — | Gebot |
| SVE-R11 | Kap. 4.1.2 (S. 9) | Beim Freischalten gilt „allseitig" auch für Anlagen mit zwei oder mehreren Anspeisungen (**Notstromgenerator**, 2 Trafos, PV, Speicher); Kapazitäten (USV, Kondensatoren) sind zu entladen. Betriebsrelevanz: ein getrennter Sicherheitskreis ist eine zweite Anspeisung. | — | Gebot |
| SVE-R12 | Kap. 1.4 (S. 2) | Für die Anlagenerrichtung ist seit Jänner 2019 die ÖVE E8101 maßgebend (Begriffe, Schutzmaßnahmen, Betriebsmittel, Leitungsdimensionierung, Installationsvorschriften, Prüfung). | — | Gebot |

## Detail-Digest der relevanten Kapitel

### Kap. 11 — Normenkurzüberblick (S. 42)
Reine Katalogtabelle „Vorschrift / Benennung". Für die Engine relevanter Ausschnitt:
- **ÖVE E 8002** — „Errichtung und Betrieb von Elektroanlagen in Versammlungsstätten usw. (alt EN2)". Einziger direkter Berührungspunkt des Skripts mit dem Themenfeld Sicherheitsbeleuchtung (die E 8002 ist die österreichische Trägernorm dafür); das Skript nennt nur den Titel, **keinerlei Inhalte** daraus.
- ÖVE E 8007 — medizinisch genutzte Räume (alt EN7).
- ÖVE EN 50272 — Akkumulatoren und Batterieanlagen (→ Zentralbatterieanlagen).
- ÖVE E 8101 — Errichtung von Starkstromanlagen bis 1 kV AC / 1,5 kV DC (alt E8001); E 8001 galt 2000–2018.

### Kap. 12 — Die ÖVE/ÖNORM E8001 (S. 43–44)
Abgelöst am 1.1.2019 durch E8101, aber wichtig für Bestandsanlagen (fast 20 Jahre Errichtungsgrundlage). Gliederung in 6 Teile; im Teil 4 „Anlagen besonderer Art" liegen die Notbeleuchtungs-nahen Paragrafen: **§53 Ersatzstromversorgungsanlagen** und **§57 Elektrische Anlagen für Sicherheitszwecke**; im Teil 2 der **§32 Leuchten und Beleuchtungsanlagen**. Inhalte dieser Paragrafen werden im Skript **nicht wiedergegeben** — nur die Überschriften.

### Kap. 13 — ÖVE Richtlinien (S. 45–46)
ÖVE-Richtlinien ergänzen Normen um technische Details und sind „ebenfalls anerkannte Regeln der Technik und somit anzuwenden". Liste R1–R27; brandschutz-/gebäudetechnik-nah: R12 (Brandschutz in el. Anlagen — Trafostationen und Schalträume), R13 (Beleuchtung/Befeuerung von Flugplätzen). Keine Richtlinie zu Sicherheitsbeleuchtung genannt.

### Kap. 14 — Die ÖVE E8101 (S. 47–50)
Kernaussage für die Norm-Landkarte der Engine: Die E8101 (Basis: europäisches Harmonisierungsdokument **HD 60364**, europaweit gleiche Struktur) hat die E8001, E8007 **und E8002 („Sicherheitsanforderungen bei Menschenansammlungen")** in einem Werk zusammengeführt (Abbildung 4, S. 47). Struktur in 7 Teilen; für Sicherheitsbeleuchtung/Sicherheitsstromversorgung einschlägige Kapitel-Nummern:
- Teil 3 (Bestimmungen allgemeiner Merkmale): Kap. **35 „Einrichtungen für Sicherheitszwecke"**, Kap. 36 „Verfügbarkeit der Versorgung".
- Teil 5 (Auswahl und Installation elektrischer Betriebsmittel): Abschnitt 551 (Stromerzeugungseinrichtungen), **559 „Leuchten und Beleuchtungsanlagen"**, Kap. **56 „Einrichtungen für Sicherheitszwecke"**.
- Teil 7 (Räume und Anlagen besonderer Art): u.a. 710 medizinisch genutzte Bereiche, 718 **öffentliche Einrichtungen und Arbeitsstätten** (dorthin ist der E8002-Stoff gewandert), 714 Beleuchtungsanlagen im Freien, 715 Kleinspannungsbeleuchtungsanlagen.
Auch hier: nur Strukturüberschriften, keine inhaltlichen Anforderungen im Skript.

### Kap. 23.4.4 / 23.4.3 — FI-Anforderungen Brandschutz/Zusatzschutz (S. 116)
Brandschutz: I∆N ≤ 300 mA, Installation am Anfang der Leitungsanlage. Zusatzschutz: I∆N ≤ 30 mA (RCCB/RCBO); ein RCD darf nicht gleichzeitig Fehlerschutz und Zusatzschutz erfüllen. Für die Engine nur peripher (Elektro-Planung des Sicherheitskreises, nicht Leuchten-Platzierung).

### Kap. 24 — Brandschutzschalter AFDD (S. 121–122)
AFDD erkennt Fehlerlichtbögen (seriell und parallel) und schaltet ab, bevor ein elektrisch gezündeter Brand entsteht; RCD kann das nicht (Stromsumme bleibt Null). Einbaupflicht (≤ 16 A AC): Schlafräume von Behinderten-/Altenheimen und Kindergärten, BE2-Räume (brennbare Materialien/Staub); Einbauempfehlung: Schlafräume in Wohngebäuden, Räume mit unersetzbaren Gütern. AFDDs müssen ggf. bei Isolationsmessung abgeschaltet werden.

### Kap. 27.1 — Überprüfung, verschärfte Maßstäbe (S. 132)
Jede Anlage ist vor Inbetriebnahme zu prüfen (Elektrofachkraft mit Erfahrung, Prüfbericht). „Besonders strenge Maßstäbe" u.a. bei: Räumen mit größeren Menschenansammlungen, Spitälern, **Notstromversorgungsanlagen**, feuer-/explosionsgefährdeten Räumen — der einzige Punkt, an dem das Skript Notstromversorgung überhaupt materiell anspricht (als Prüf-Sonderfall, ohne technische Anforderungen).

## Offene Punkte / Extraktionslücken

- **Kein Notbeleuchtungs-Fachinhalt vorhanden:** Die Begriffe Notbeleuchtung, Sicherheitsbeleuchtung, Fluchtweg, Rettungsweg, Notausgang, Antipanik, Funktionserhalt, EN 1838, Erkennungsweite, Lux/Beleuchtungsstärke, Zentral-/Einzelbatterie kommen im gesamten Volltext nicht vor (Grep über den 273k-Zeichen-Volltext). Das Dokument liefert der Engine **keine Platzierungs- oder Lichttechnik-Regeln** — nur die Norm-Landkarte (SVE-R1…R6).
- Die Inhalte von ÖVE E 8002 / E8101 Kap. 35, 56, 559 / E8001 §53, §57 werden im Skript nur als Überschriften genannt. [Extraktionslücke: die eigentlichen Anforderungen — Umschaltzeiten, Betriebsdauer, Leitungs-Funktionserhalt, Stromkreis-Trennung — müssen aus den Primärnormen (ÖVE E8101, EN 1838, ÖVE/ÖNORM EN 50172, TRVB E 102) gezogen werden; sie sind hier nicht enthalten.]
- Skript-Stand ist Juli 2019; Aussagen zur E8101 beziehen sich auf deren Erstausgabe 2019. [Extraktionslücke: spätere E8101-Ausgaben/Änderungen sind nicht abgedeckt.]
- Die PDF-Textextraktion enthält OCR-/Layout-Artefakte (getrennte Wörter, Tabellenumbrüche); Seitenzahlen der Fußzeile (Druckseiten) weichen von PDF-Seiten ab. Kapitel-/Seitenangaben oben folgen der Druckseiten-Fußzeile bzw. dem Inhaltsverzeichnis.
- Detail-Zahlenwerte außerhalb der NB-relevanten Teile (Körperstrom-Schwellen, Nullungsbedingungen, Querschnitte) wurden bewusst nicht extrahiert (nicht Engine-relevant).
