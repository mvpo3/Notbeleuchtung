# OVE E 8101:2019 — Elektrische Niederspannungsanlagen
**Quelle:** knowledge/OVE E 8101_2019 (1).pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf; gezielt vertieft: Abschnitte für Sicherheitszwecke/Notbeleuchtung

Ausgabe: 2019-01-01. Nationale elektrotechnische Norm gemäß ETG 1992; strukturell und technisch gleichwertig zum CENELEC-Harmonisierungsdokument HD 60364 (Reihe). Ersetzt (teilweise) die ÖVE-EN 1 Reihe und die ÖVE/ÖNORM E 8001 Reihe. Nationale AT-Ergänzungen sind im Nummerierungsschema mit „AT" bzw. „NE" gekennzeichnet.

## Relevanz für die Engine

OVE E 8101 ist die österreichische Errichtungsnorm für Niederspannungsanlagen. Für die Notbeleuchtungs-Engine ist sie die **elektrotechnische Hard-Stop-Ebene** (OVE-Verbote) und die Quelle der Stromkreis-/Versorgungsregeln, die die Platzierung mitbestimmen:

1. **Teil 5-56 „Einrichtungen für Sicherheitszwecke" (Abschnitt 560)** ist DER Kernabschnitt: Stromquellen, Sicherheitsstromkreise, Kabel/Funktionserhalt, Anforderungen an Sicherheitsbeleuchtungsanlagen (560.9), inkl. Endstromkreis-Grenzen (max. 20 Leuchten, 60 % Nennstrom) und der Pflicht, Sicherheitsleuchten in einem Brandabschnitt **abwechselnd auf mindestens zwei Stromkreise** zu verteilen → direkt platzierungs- und stromkreisrelevant.
2. **Anhang 56.A / Tabelle 56.A.1.AT** liefert je Nutzungsart (Versammlungsstätte, Beherbergung, Schule, Garage, Krankenhaus, Pflegeheim …) die **Bemessungsbetriebsdauer der Sicherheitsstromquelle (1 h/3 h/8 h)**, die zulässigen Versorgungssysteme und ob Sicherheitszeichen in Dauerbetrieb gefordert/zulässig sind.
3. **Teil 7-718 (öffentliche Einrichtungen/Arbeitsstätten)** nennt **konkrete Zusatz-Orte, die Sicherheitsbeleuchtung brauchen** (Fahrtreppen, Sanitärräume ≥ 8 m², barrierefreie WCs, Technik-/Verteilerräume, Wartezonen/Flächen > 60 m² in Bahnhöfen/Flughäfen) und die **Antipanik-Pflichten in Versammlungsstätten** → direkte Platzierungsregeln.
4. Lichttechnische Werte (Lux, Erkennungsweite, Leuchtenabstände) regelt OVE E 8101 **nicht** selbst — sie verweist durchgehend auf **ÖNORM EN 1838** (Werte), **ÖVE/ÖNORM EN 50172** (Errichtung/Betrieb/Wartung) und **OVE-Richtlinie R 12-2** (wo Sicherheitsbeleuchtung nach Nutzungsart erforderlich ist, Funktionserhalt-Dauern). Die Engine-Hierarchie „LB → Referenz → EN-1838-Default → OVE-Verbot" bleibt konsistent: E 8101 liefert v. a. Verbote und System-/Stromkreisregeln.
5. Begriffs-Anker (560.3): Notbeleuchtung ⊃ Sicherheitsbeleuchtung (Fluchtweg + Antipanik + Arbeitsplätze mit besonderer Gefährdung) + Ersatzbeleuchtung; „Rettungsweg" (international) wird in OVE E 8101 einheitlich durch **„Fluchtweg"** ersetzt (ANMERKUNG 1.AT zu 560.9.1, S. 479).

## Dokument-Landkarte

| Teil | Inhalt (1 Zeile) |
|---|---|
| Vorwort/Inhalt (S. 1–10) | Herkunft (HD 60364), Gegenüberstellung alt→neu (Tab. I.2), Aufbau (Tab. I.3/I.4). |
| Teil 1 — Allgemeine Grundsätze (ab S. 11) | Anwendungsbereich, Schutzanforderungen (131, u. a. 131.7 Schutz bei Unterbrechung der Stromversorgung), Planung (132, u. a. 132.4 Anlagen für Sicherheitszwecke), Prüfen. |
| Teil 2 — Begriffe (S. ~25–100) | Alle Definitionen inkl. 560.3.x (Notbeleuchtung, Sicherheitsbeleuchtung, Sicherheitsleuchte, Sicherheitszeichen, Dauer-/Bereitschaftsbetrieb, Umschaltzeit, CPS/LPS, Fluchtweg). |
| Teil 3 — Bestimmung allgemeiner Merkmale (S. ~97–160) | 313.2 Stromversorgungen für Sicherheitszwecke, Abschnitt 35 (zulässige Sicherheitsstromquellen, Verweis auf 560), 36 Verfügbarkeit der Versorgung, Anhang 3.A Netzformen. |
| Teil 4-41 | Schutz gegen elektrischen Schlag (TN/TT/IT, Abschaltzeiten, RCD). |
| Teil 4-42 (S. ~167 ff.) | Schutz gegen thermische Einflüsse; **422.2 Bedingungen für Evakuierung im Notfall** (Kabel in Fluchtwegen/Treppenhäusern, Feuerwiderstand 1 h für Sicherheitsstromkreise) — engine-relevant. |
| Teil 4-43 / 4-44 / 4-45 / 4-46 | Überstromschutz / Störspannungen+EMV (442/443/444) / Unterspannung / Trennen und Schalten. |
| Teil 5-51 | Allgemeine Bestimmungen Betriebsmittelauswahl; äußere Einflüsse (Tab. 51.ZA: BD1–BD4 Evakuierungsbedingungen, BE2/BE3 Brand-/Ex-Risiko). |
| Teil 5-52 | Kabel- und Leitungsanlagen (Verlegearten, 527.1 innerhalb Brandabschnitt). |
| Teil 5-53 (inkl. 534, 537) | Schalt-/Steuergeräte, Überspannungsschutz, Trennen/Schalten. |
| Teil 5-54 | Erdung, Schutzleiter, Schutzpotentialausgleich. |
| Teil 5-55 (551/557/559) | Stromerzeugungseinrichtungen (551 = Ersatzstromversorgung), Hilfsstromkreise, **559 Leuchten/Beleuchtungsanlagen** (559.1 verweist für Notbeleuchtung auf Teil 5-56 + EN 50172 + EN 1838 + EN 60598-2-22). |
| **Teil 5-56 (S. 473–491)** | **Einrichtungen für Sicherheitszwecke — Kernabschnitt, vollständig unten digestiert.** |
| Teil 6 — Prüfung (ab S. 491) | Erstprüfung/wiederkehrende Prüfung elektrischer Anlagen. |
| Teil 7-701…7-706 | Bad/Dusche, Schwimmbecken, Sauna, Baustellen (704.56: Sicherheitsbeleuchtung ggf. erforderlich), Landwirtschaft, leitfähige enge Bereiche. |
| Teil 7-708/709 | Camping, Marinas. |
| **Teil 7-710 (S. ~585–621)** | **Medizinisch genutzte Bereiche**: SV-Klassen (SV ≤ 0,5 s / SV ≤ 15 s / > 15 s), Beleuchtungsstromkreis-Aufteilung, 710.560.9 Sicherheitsbeleuchtung, NE für Pflegeheime (8 h Fluchtweg). |
| Teil 7-711 | Ausstellungen/Shows/Stände (711.560.9: Sicherheitsbeleuchtung → Teil 5-56 + R 12-2). |
| Teil 7-712…7-715, 7-717 | PV, Möbel, Beleuchtung im Freien, Kleinspannungsbeleuchtung, transportable Einheiten. |
| **Teil 7-718 (S. ~675–682)** | **Öffentliche Einrichtungen und Arbeitsstätten**: Zusatz-Orte für Sicherheitsbeleuchtung, Antipanik in Versammlungsstätten (718.NE.1), Garagen (718.NE.2). |
| Teil 7-721/722 | Caravans, E-Fahrzeug-Ladung. |
| Teil 7-729 (S. ~707 ff.) | Bedienungs-/Instandhaltungsgänge; 729.560.9: Notbeleuchtung in abgeschlossenen el. Betriebsstätten ggf. erforderlich. |
| Teil 7-730 / 7-740 / 7-753 | Binnenschiff-Landanschluss / fliegende Bauten & Zirkusse (740: Sicherheitsbeleuchtung → Teil 5-56) / Heizanlagen. |
| Verweisungen (S. ~747 ff.) | U. a. ÖVE/ÖNORM EN 50171 (Zentrale Stromversorgungssysteme), EN 50172 (Sicherheitsbeleuchtungsanlagen), EN 62034 (automatische Prüfsysteme), ÖNORM EN 1838 (Notbeleuchtung). |

## Regel-Tabelle (maschinen-orientiert) — Sicherheitszwecke/Notbeleuchtung

Typ ∈ {Gebot, Verbot, Grenzwert, Definition, Empfehlung}. Seitenangaben = PDF-Seiten (===== SEITE n =====).

### Teil 1 / Teil 3 — Grundsätze

| ID | §/Abschnitt (Seite) | Regel | Werte/Grenzwerte | Typ |
|---|---|---|---|---|
| OVE8101-R1 | 131.7 (S. 15) | Wo Gefahr/Schaden durch Unterbrechung der Stromversorgung zu erwarten ist, sind geeignete Vorkehrungen in Anlage oder Betriebsmitteln zu treffen. | — | Gebot |
| OVE8101-R2 | 132.4 (S. 17) | Bei Planung sind für Anlagen für Sicherheitszwecke Stromquelle (Art, Kenngrößen) und zu versorgende Stromkreise festzulegen. | — | Gebot |
| OVE8101-R3 | 313.2 (S. 111) | Versorgungen für Sicherheitszwecke sind getrennt zu bestimmen und hinsichtlich Leistung, Zuverlässigkeit, Bemessungsgrößen und geeigneter Umschaltzeit auszulegen. | — | Gebot |
| OVE8101-R4 | 35/351 (S. 112) | Geeignete Sicherheitsstromquellen: Sekundärzellen-Batterien, Primärzellen-Batterien, netzunabhängige Generatoren, separate unabhängige Netzeinspeisung (mit 560.6.5). | 4 Quellenarten | Definition |

### Teil 2 — Begriffe (560.3, S. 55–57)

| ID | §/Abschnitt (Seite) | Regel | Werte/Grenzwerte | Typ |
|---|---|---|---|---|
| OVE8101-R5 | 560.3.6 (S. 55) | Notbeleuchtung = Beleuchtung, die bei Störung der Stromversorgung der allgemeinen künstlichen Beleuchtung wirksam wird; umfasst gemäß EN 1838 Sicherheitsbeleuchtung für Fluchtwege, Antipanikbeleuchtung, Sicherheitsbeleuchtung für Arbeitsplätze mit besonderer Gefährdung und Ersatzbeleuchtung. | — | Definition |
| OVE8101-R6 | 560.3.001.AT (S. 55) | Sicherheitsbeleuchtung = Teil der Notbeleuchtung, der sicheres Verlassen eines Raums/Gebäudes bzw. Beenden eines gefährlichen Arbeitsablaufs ermöglicht. | — | Definition |
| OVE8101-R7 | 560.3.7 / 560.3.002.AT (S. 55) | Notleuchte = Leuchte (mit oder ohne eigene Sicherheitsstromquelle) für Sicherheits- oder Notbeleuchtung; Sicherheitsleuchte = Notleuchte für die Sicherheitsbeleuchtung. | — | Definition |
| OVE8101-R8 | 560.3.003.AT / 560.3.8.AT (S. 55–56) | Sicherheitszeichen = Zeichen aus Farbe + geometrischer Form (+ Symbol); beleuchtet (extern) bzw. hinterleuchtet (intern). | — | Definition |
| OVE8101-R9 | 560.3.9 / 560.3.10 (S. 56) | Dauerbetrieb = Lampen der Sicherheitsbeleuchtung ständig in Betrieb, wenn Beleuchtung erforderlich; Bereitschaftsbetrieb = nur nach Ausfall der allgemeinen Beleuchtung in Betrieb. | — | Definition |
| OVE8101-R10 | 560.3.11 (S. 56) | Umschaltzeit = Zeitspanne zwischen Ausfall der allgemeinen Stromversorgung und Übernahme durch Ersatz-/Sicherheitsstromquelle. | — | Definition |
| OVE8101-R11 | 560.3.12 / 560.3.13 (S. 56) | CPS = zentrales Stromversorgungssystem ohne Leistungsbegrenzung; LPS = mit Leistungsbegrenzung auf 500 W für 3 h oder 1 500 W für 1 h. | 500 W/3 h; 1 500 W/1 h | Definition |
| OVE8101-R12 | 560.3.14.004.AT (S. 56) | Fluchtweg = Weg, der Benützern im Gefahrenfall grundsätzlich ohne fremde Hilfe das Erreichen eines sicheren Ortes im Freien ermöglicht (Quelle: OIB-Richtlinie). | — | Definition |
| OVE8101-R13 | 560.3.16 (S. 57) | Mindestbeleuchtungsstärke = Beleuchtungsstärke der Sicherheitsbeleuchtung am Ende der Bemessungsbetriebsdauer. | — | Definition |

### Teil 5-56 — 560.4/560.5 Klassifizierung & Allgemeines

| ID | §/Abschnitt (Seite) | Regel | Werte/Grenzwerte | Typ |
|---|---|---|---|---|
| OVE8101-R14 | 560.4.1 (S. 473–474) | Stromversorgungssystem für Sicherheitszwecke ist nicht-automatisch (Einschaltung durch Personal) oder automatisch; automatische Versorgung klassifiziert nach max. Umschaltzeit: unterbrechungsfrei / sehr kurz ≤ 0,15 s / kurz ≤ 0,5 s / durchschnittlich ≤ 5 s / mittel ≤ 15 s / lang > 15 s. | 0,15 s / 0,5 s / 5 s / 15 s | Definition |
| OVE8101-R15 | 560.4.1 ANM. AT (S. 473) | Nicht-automatische Stromversorgung kommt im Anwendungsbereich von Teil 7-710 (medizinisch) und Teil 7-718 (öffentl. Einrichtungen/Arbeitsstätten) NICHT zur Anwendung. | — | Verbot |
| OVE8101-R16 | 560.4.2 (S. 474) | Wesentliche Betriebsmittel der Sicherheitseinrichtungen müssen mit der Umschaltzeit kompatibel sein. | — | Gebot |
| OVE8101-R17 | 560.5.1 (S. 474) | Funktion ggf. jederzeit, auch bei Ausfall der Haupt- und lokalen Stromversorgung und im Brandfall, aufrechtzuerhalten; ergänzend gilt OVE-Richtlinie R 12-2; Notwendigkeit des Funktionserhalts aus brandschutz-/bautechnischen Richtlinien, Behördenvorschreibung oder R 12-2. | — | Gebot |
| OVE8101-R18 | 560.5.2 (S. 474) | Bei gefordertem Funktionserhalt im Brandfall: Stromquelle mit ausreichender Versorgungsdauer wählen UND alle Betriebsmittel durch Bauart oder Errichtungsart für ausreichende Dauer feuerbeständig schützen (Dauer siehe R 12-2). | — | Gebot |
| OVE8101-R19 | 560.5.3 (S. 474) | Bei Schutz durch automatische Abschaltung sind Schutzmaßnahmen ohne Abschaltung beim ersten Fehler zu bevorzugen; in IT-Systemen Isolationsüberwachung mit akustischer UND optischer Erstfehlermeldung. | — | Gebot |
| OVE8101-R20 | 560.5.4 (S. 474) | Eine Störung im Steuerungs- oder Bussystem der Anlage darf die Funktion der Einrichtungen für Sicherheitszwecke nicht beeinträchtigen. | — | Verbot |
| OVE8101-R21 | 560.5.001.AT (S. 475) | Anlagenzustand des Sicherheitsstromversorgungssystems (betriebsbereit / Speisung aus Sicherheitsstromquelle / Störung) ist an zentraler, ständig überwachter Stelle anzuzeigen; gilt NICHT für Einzelbatterieanlagen bis 20 Sicherheitsleuchten. | Ausnahme ≤ 20 Leuchten | Gebot |

### Teil 5-56 — 560.6 Stromquellen für Sicherheitszwecke

| ID | §/Abschnitt (Seite) | Regel | Werte/Grenzwerte | Typ |
|---|---|---|---|---|
| OVE8101-R22 | 560.6.1 (S. 475) | Zulässige Stromquellen: Sekundärzellen-Batterien, Primärzellen-Batterien, netzunabhängige Generatoren, separate unabhängige Netzeinspeisung; Einzelbatterie-Sicherheitsleuchten gemäß ÖVE/ÖNORM EN 60598-2-22. | — | Gebot |
| OVE8101-R23 | 560.6.1 (S. 475) | **Batterien mit Primärzellen dürfen für Sicherheitsbeleuchtungsanlagen NICHT verwendet werden.** | — | Verbot |
| OVE8101-R24 | 560.6.2 (S. 475) | Sicherheitsstromquellen als ortsfeste Anlagen errichten; dürfen durch Ausfall der allgemeinen Stromversorgung nicht beeinträchtigt werden. | — | Gebot |
| OVE8101-R25 | 560.6.3 (S. 475) | Standort geeignet; nur Elektrofachkräften (BA5) oder elektrotechnisch unterwiesenen Personen (BA4) zugänglich. | — | Gebot |
| OVE8101-R26 | 560.6.4 (S. 475) | Standort ständig und angemessen be-/entlüftet; Gase/Rauch/Dämpfe dürfen nicht in von Personen genutzte Bereiche eindringen. | — | Gebot |
| OVE8101-R27 | 560.6.5 (S. 475) | Separate unabhängige Netzeinspeisungen nur zulässig, wenn zugesichert ist, dass gleichzeitiger Ausfall beider Einspeisungen unwahrscheinlich ist. | — | Gebot |
| OVE8101-R28 | 560.6.6 (S. 475) | Sicherheitsstromquelle muss ausreichende Kapazität für die zugehörigen Einrichtungen haben. | — | Gebot |
| OVE8101-R29 | 560.6.7 (S. 475) | Nutzung für andere Zwecke nur, wenn Verfügbarkeit für Sicherheitszwecke nicht beeinträchtigt; ein Fehler in einem Fremd-Stromkreis darf keinen Sicherheits-Stromkreis unterbrechen. | — | Verbot |
| OVE8101-R30 | 560.6.8 (S. 475–476) | Nicht parallelbetriebsfähige Quellen: Parallelbetrieb verhindern (z. B. mechanische Verriegelung); Kurzschluss- und Fehlerschutz je Quelle sicherstellen. | — | Gebot |
| OVE8101-R31 | 560.6.9 (S. 476) | Parallelbetriebsfähige Quellen: Kurzschluss- und Fehlerschutz für Einzel- und Parallelbetrieb sicherstellen (Netzbetreiber-Genehmigung, Rückspeise-Schutz beachten). | — | Gebot |
| OVE8101-R32 | 560.6.10 (S. 476) | CPS: Batterien wartungsarm, geschlossene/verschlossene Bauart, Industrieausführung (OVE EN 60623 / EN 60896); zentrale Systeme für Sicherheitsbeleuchtung gemäß ÖVE/ÖNORM EN 50171. | — | Gebot |
| OVE8101-R33 | 560.6.11 (S. 476) | LPS: Ausgangsleistung begrenzt auf 500 W für 3 h bzw. 1 500 W für 1 h; ebenfalls EN 50171. | 500 W/3 h; 1 500 W/1 h | Grenzwert |
| OVE8101-R34 | 560.6.12 (S. 476) | USV muss: Schutzeinrichtungen auslösen können, im Batterie-Notbetrieb die Sicherheitseinrichtungen starten/betreiben, 560.6.10 erfüllen, ggf. EN 62040-1/-3 entsprechen. | — | Gebot |
| OVE8101-R35 | 560.6.13 (S. 476) | Stromerzeugungsaggregate für Sicherheitszwecke gemäß ISO 8528-12, DIN 6280-12 bzw. DIN 6280-13. | — | Gebot |
| OVE8101-R36 | 560.6.14 (S. 476) | Zustand der Sicherheitsstromquelle (betriebsbereit / Störung / in Betrieb) muss angezeigt werden. | — | Gebot |

### Teil 5-56 — 560.7 Stromkreise für Sicherheitszwecke

| ID | §/Abschnitt (Seite) | Regel | Werte/Grenzwerte | Typ |
|---|---|---|---|---|
| OVE8101-R37 | 560.7.1 (S. 476–477) | Sicherheitsstromkreise müssen von anderen Stromkreisen unabhängig sein (Fehler/Eingriff/Änderung im einen System darf das andere nicht beeinträchtigen; ggf. Trennung durch feuerbeständiges Material, getrennte Trassen oder Umhüllungen). | — | Gebot |
| OVE8101-R38 | 560.7.2 (S. 477) | Sicherheitsstromkreise dürfen NICHT durch Bereiche mit hohem Brandrisiko (BE2) geführt werden, außer sie erfüllen 560.8.1; **in keinem Fall durch explosionsgefährdete Bereiche (BE3)**. | — | Verbot |
| OVE8101-R39 | 560.7.3 (S. 477) | Verzicht auf Überlastschutz (gemäß 433.3.3) zulässig, wenn Versorgungsausfall größere Gefahr bedeutet; dann muss Überlast angezeigt werden. | — | Gebot |
| OVE8101-R40 | 560.7.4 (S. 477) | Überstrom-Schutzeinrichtungen so wählen/errichten, dass Überstrom in einem Stromkreis andere Sicherheitsstromkreise nicht beeinträchtigt (Selektivität). | — | Gebot |
| OVE8101-R41 | 560.7.5 (S. 477) | Schalt-/Steuergeräte für Sicherheitsstromkreise eindeutig kennzeichnen; nur an Standorten, die nur BA5/BA4 zugänglich sind (versperrbares Gehäuse gilt als erfüllt). | — | Gebot |
| OVE8101-R42 | 560.7.6 (S. 477) | Bei Versorgung eines Betriebsmittels aus zwei unabhängigen Stromkreisen darf ein Fehler in einem Kreis weder Schutz gegen elektrischen Schlag noch Funktion des anderen beeinträchtigen; ggf. mit Schutzleitern beider Kreise verbinden. | — | Gebot |
| OVE8101-R43 | 560.7.7 (S. 477) | Sicherheits-Kabel ohne 560.8.1/560.8.2-Eigenschaften sind von anderen Kabeln durch Abstand oder räumliche Trennung (z. B. Trennsteg) zu trennen; mehrere Sicherheitsstromkreise gemeinsam verlegen zulässig; im letzten Brandabschnitt gemeinsames Tragsystem mit anderen Kabeln zulässig. | — | Gebot |
| OVE8101-R44 | 560.7.8 (S. 477) | Sicherheitsstromkreise dürfen NICHT in Aufzugsschächten oder anderen kaminähnlichen Schächten (Zugwirkung) verlegt werden — Ausnahme: Versorgungsleitungen für Feuerwehraufzüge und Aufzüge mit besonderen Anforderungen. | — | Verbot |
| OVE8101-R45 | 560.7.9–560.7.12 (S. 477–478) | Doku-Pflichten: einpoliger Prinzipschaltplan + vollständige Angaben aller Sicherheitsstromquellen (Aufbewahrung bei Quelle und Hauptverteiler); aktuelle Pläne mit genauen Standorten aller Betriebsmittel/Verteiler, Sicherheitseinrichtungen mit Endstromkreis-Kennzeichnung und Zweck, Schalt-/Überwachungseinrichtungen; Verbraucherliste (Nennleistung, Nenn-/Anlaufströme, Anlaufzeit); Betriebsanleitungen. | — | Gebot |
| OVE8101-R46 | 560.7.13 (S. 478) | Batterieanlagen gemäß ÖVE/ÖNORM EN 50272-2. | — | Gebot |

### Teil 5-56 — 560.8 Kabel- und Leitungsanlagen (Funktionserhalt)

| ID | §/Abschnitt (Seite) | Regel | Werte/Grenzwerte | Typ |
|---|---|---|---|---|
| OVE8101-R47 | 560.8.1 (S. 478) | Bei Funktionserhalt im Brandfall: mineralisolierte Kabel (EN 60702-1/-2) ODER feuerbeständige Kabel mit Isolationserhalt (OVE EN 50200 + EN 60332-1-2) ODER Kabelanlage mit Schutz gegen Feuer und mechanische Beschädigung (z. B. Funktionserhalt nach ÖNORM DIN 4102-12, bauliche Umhüllung, Führung in getrennten Brandabschnitten, Schienenverteiler im Schacht mit Funktionserhalt); Befestigung/Errichtung so, dass Funktion im Brandfall nicht beeinträchtigt wird. | — | Gebot |
| OVE8101-R48 | 560.8.2 (S. 478) | 560.8.1 gilt auch für Kabel von Steuerungs- und Bussystemen der Sicherheitseinrichtungen (außer Stromkreise ohne nachteiligen Einfluss). | — | Gebot |
| OVE8101-R49 | 560.8.3 (S. 478) | Erdverlegte Sicherheitsstromkreise gegen Erdarbeiten schützen; AT-Praxis: getrennte Trassen mit ≥ 2 m Horizontalabstand oder Stufenkünette mit ≥ 1 m Höhenunterschied; Unterschreitung nahe Gebäudeeinführung nur mit besonderem mechanischem Schutz. | 2 m horizontal; 1 m Stufe | Gebot |
| OVE8101-R50 | 560.8.4 (S. 479) | Gleichstrom-gespeiste Sicherheitsstromkreise: zweipolige Überstrom-Schutzeinrichtungen. | — | Gebot |
| OVE8101-R51 | 560.8.5 (S. 479) | Schalt-/Steuergeräte für AC- und DC-Quellen müssen für beide Betriebsarten geeignet sein. | — | Gebot |

### Teil 5-56 — 560.9 Sicherheitsbeleuchtungsanlagen

| ID | §/Abschnitt (Seite) | Regel | Werte/Grenzwerte | Typ |
|---|---|---|---|---|
| OVE8101-R52 | 560.9 ANM. 1.AT–4.AT (S. 479) | WO Sicherheitsbeleuchtung erforderlich ist (nach Nutzungsart) → OVE-Richtlinie R 12-2; Errichtung/Überwachung/Wartung → ÖVE/ÖNORM EN 50172; lichttechnische Anforderungen + Messungen → ÖNORM EN 1838; Sonderanlagen (Sport: EN 12193; Aufzüge: EN 81-20/81-72, TRVB 150 S); Behörden können zusätzlich vorschreiben. | — | Gebot |
| OVE8101-R53 | 560.9.1 (S. 479) | Sicherheitsbeleuchtungsanlagen entweder aus zentralem Stromversorgungssystem ODER als Sicherheitsleuchten mit Einzelbatterie; Einzelbatterie-Leuchten sind von 560.9.1–560.9.4 (Versorgungs-Anforderungen) ausgenommen. | — | Gebot |
| OVE8101-R54 | 560.9.1 (S. 479) | Zentral versorgt: Versorgung von Stromquelle bis zu den Sicherheitsleuchten muss im Brandfall für angemessene Dauer erhalten bleiben (Kabel gemäß 560.8.1/560.8.2 zur Durchleitung durch Brandabschnitte); innerhalb des Brandabschnitts gilt 527.1. | — | Gebot |
| OVE8101-R55 | 560.9.1 (S. 479) | **In Brandabschnitten mit mehr als einer Sicherheitsleuchte sind die Leuchten abwechselnd auf mindestens zwei verschiedene Stromkreise zu verteilen**, sodass bei Ausfall eines Stromkreises eine Grundbeleuchtung entlang des Fluchtweges sichergestellt ist. | ≥ 2 Stromkreise | Gebot |
| OVE8101-R56 | 560.9.1 ANM. 1.AT (S. 479) | Begriff: „Rettungsweg" (international) = Oberbegriff Selbst-+Fremdrettung; Selbstrettungs-Anteil national = „Fluchtweg"; OVE E 8101 verwendet einheitlich „Fluchtweg". | — | Definition |
| OVE8101-R57 | 560.9.2 (S. 480) | Bei Aufteilung auf Stromkreise: Überstromschutz muss sicherstellen, dass ein Kurzschluss in einem Stromkreis benachbarte Leuchten im Brandabschnitt oder Leuchten in anderen Brandabschnitten nicht unterbricht. | — | Gebot |
| OVE8101-R58 | 560.9.2 (S. 480) | **Je Endstromkreis max. 20 Leuchten, Gesamtbelastung max. 60 % des Nennstroms der Überstrom-Schutzeinrichtung**; Verteiler/Steuer-/Schutzeinrichtungen dürfen die Funktionsfähigkeit nicht beeinträchtigen. | ≤ 20 Leuchten; ≤ 60 % In | Grenzwert |
| OVE8101-R59 | 560.9.3 (S. 480) | Für die Evakuierung: ausreichende Mindestbeleuchtungsstärke, Umschaltzeit und Bemessungsbetriebsdauer gemäß ÖNORM EN 1838; Planungs-Leitfaden Tabelle 56.A.1.AT; Arbeitsstätten (ASchG): Arbeitsstättenverordnung. | — | Gebot |
| OVE8101-R60 | 560.9.4 (S. 480) | Sicherheitsbeleuchtung muss im Dauerbetrieb ODER Bereitschaftsbetrieb geschaltet sein; Kombination zulässig. | — | Gebot |
| OVE8101-R61 | 560.9.5 (S. 480) | Bereitschaftsbetrieb: Stromversorgung der allgemeinen Beleuchtung des Bereichs muss im Endstromkreis überwacht werden; bei Ausfall der allgemeinen Beleuchtung ist die Sicherheitsbeleuchtung automatisch zu aktivieren (auch bei Ausfall der allgemeinen Stromversorgung: örtliche Aktivierung sicherstellen). | — | Gebot |
| OVE8101-R62 | 560.9.6 (S. 480) | Bei Kombination Dauer-/Bereitschaftsbetrieb: jede Umschaltvorrichtung mit eigener Überwachungseinrichtung, gesondert schaltbar. | — | Gebot |
| OVE8101-R63 | 560.9.7 (S. 480) | Dauerbetriebs-Sicherheitsbeleuchtung darf nur in Bereichen gemeinsam mit der allgemeinen Beleuchtung geschaltet werden, die während des Betriebs nicht verdunkelt werden können oder nicht ständig genutzt werden. | — | Gebot |
| OVE8101-R64 | 560.9.8 (S. 480) | Funktion der Sicherheitsbeleuchtung darf von keinem Steuerungssystem beeinträchtigt werden; bei Fehler im Steuerungssystem und/oder im Endstromkreis der allgemeinen Beleuchtung müssen alle Sicherheitsleuchten des betroffenen Bereichs die erforderliche Beleuchtungsstärke erbringen. | — | Verbot |
| OVE8101-R65 | 560.9.9 (S. 480) | Automatische Umschaltung auf Notbetrieb, sobald Versorgungsspannung > 0,5 s unter 0,6 × Bemessungsspannung fällt; Rückkehr zum Normalbetrieb bei > 0,85 × Bemessungsspannung. | 0,6 Un / 0,5 s; 0,85 Un | Grenzwert |
| OVE8101-R66 | 560.9.10 (S. 480–481) | Nach Wiederkehr der allgemeinen Versorgung: automatische Abschaltung des Bereitschaftsbetriebs (Wiederzünd-Zeit der Allgemeinbeleuchtung berücksichtigen); in vor dem Ausfall betrieblich verdunkelten Räumen darf die Sicherheitsbeleuchtung NICHT automatisch abschalten. | — | Verbot |
| OVE8101-R67 | 560.9.11 (S. 481) | Zusätzlich zur zentralen Umschaltung ist bereichsweise Überwachung/Steuerung zulässig. | — | Gebot |
| OVE8101-R68 | 560.9.12 (S. 481) | Lampenausführung und Umschaltzeit müssen aufeinander abgestimmt sein (vorgegebene Beleuchtungsstärke sicherstellen). | — | Gebot |
| OVE8101-R69 | 560.9.13 (S. 481) | Steuerschalter der Sicherheitsbeleuchtung an gekennzeichneten Stellen; gegen Bedienung durch Unbefugte gesichert. | — | Gebot |
| OVE8101-R70 | 560.9.14 (S. 481) | Betriebszustand der Sicherheitsbeleuchtung für jede Stromquelle an gut einsehbarem Standort anzeigen. | — | Gebot |
| OVE8101-R71 | 560.9.15 (S. 481) | Sicherheitsleuchten + zugehörige Komponenten mit gut sichtbarem, einfach lesbarem **rotem oder grünem Schild** kennzeichnen (AT: andere eindeutige Identifizierung zulässig); **in Leuchtennähe/an der Leuchte: Verteiler-, Stromkreis- und Leuchtennummer anbringen**. | — | Gebot |
| OVE8101-R72 | 560.9.001.AT (S. 481) | Bei > 20 Sicherheitsleuchten in einem zusammenhängenden Gebäudeteil: automatische Prüfeinrichtung mit zentraler Erfassung gemäß ÖVE/ÖNORM EN 62034; Ladungsüberwachung kontinuierlich oder in Abständen < 5 min; Funktionsüberwachung der Verbraucher: Fehleranzeige bereits bei Ausfall EINER Leuchte, Prüfzyklus täglich, Prüfdauer 0,5–5 min; Fehlermeldung bei Übertragungsfehlern. | > 20 Leuchten; < 5 min; täglich; 0,5–5 min | Gebot |

### Teil 5-56 — 560.10 Brandschutztechnische Einrichtungen

| ID | §/Abschnitt (Seite) | Regel | Werte/Grenzwerte | Typ |
|---|---|---|---|---|
| OVE8101-R73 | 560.10.1 (S. 481) | Stromversorgung brandschutztechnischer Einrichtungen: separater Stromkreis von der Hauptverteilung. | — | Gebot |
| OVE8101-R74 | 560.10.2 (S. 481) | Vorrangige Stromkreise (falls vorhanden) direkt an der Einspeiseseite des Trennschalters der Hauptverteilung anschließen. | — | Gebot |
| OVE8101-R75 | 560.10.3 (S. 482) | Geräte zur Alarmierung eindeutig kennzeichnen. | — | Gebot |

### Anhang 56.A (informativ) — Tabelle 56.A.1.AT Leitfaden Sicherheitsbeleuchtung (S. 483–485)

Beleuchtungsstärke und max. Umschaltzeit sind überall „a" = Ausführung gemäß ÖNORM EN 1838 (Ausnahme: Krankenhäuser mit expliziter Umschaltzeit 15 s). Spalten der Versorgungssysteme: Sicherheitszeichen-Dauerbetrieb / CPS / LPS / Einzelbatterie / Aggregat 0 s / Aggregat ≤ 0,5 s / Aggregat ≤ 15 s (X = zulässig, – = nicht zulässig).

| ID | Nutzungsart (Zeile) | Bemessungsbetriebsdauer | Systeme (linearer Tabellen-Lesart, siehe Extraktionslücke E1) | Typ |
|---|---|---|---|---|
| OVE8101-R76 | Räume für größere Personenzahl (Versammlungsstätten stationär: Theater, Kinos, Sportstätten, Schwimmhallen, Sitzungssäle inkl. Bühnen/Szenenflächen) | 3 h | X X X X X X – (Aggregat mit mittlerer Unterbrechung ≤ 15 s nicht zulässig) | Grenzwert |
| OVE8101-R77 | Vorübergehend errichtete Aufbauten | ≥ 1 h | X X X X X X – | Grenzwert |
| OVE8101-R78 | Ausstellungsstätten / Verkaufsstätten / Gaststätten | je 3 h | X X X X X X – | Grenzwert |
| OVE8101-R79 | Beherbergungsstätten u. vergleichbar | **8 h** | X X X X X X X (alle Systeme zulässig) | Grenzwert |
| OVE8101-R80 | Studenten-/Alters-/Altenwohn-/Seniorenheime, Seniorenresidenzen u. vergleichbar | 3 h | X X X X X X X | Grenzwert |
| OVE8101-R81 | Schul- und Kindergartengebäude, Universitäten/FH/VHS, Bildungsstätten | 3 h | X X X X X X X | Grenzwert |
| OVE8101-R82 | Garagen, überdachte Stellplätze, Parkdecks | a (gemäß EN 1838) | X X X X X X X | Grenzwert |
| OVE8101-R83 | Öffentlich zugängliche Bereiche verkehrstechnischer Einrichtungen (Flughäfen, Bahnhöfe) | 3 h | X X X X X X – | Grenzwert |
| OVE8101-R84 | Gebäude Fluchtniveau ≤ 22 m (OIB) | a (gemäß EN 1838) | X X X X X X – | Grenzwert |
| OVE8101-R85 | Gebäude Fluchtniveau > 22 m (OIB) | 3 h; **Wohngebäude mit Fluchtniveau > 32 m: 8 h** (Fußnote b) | X X X X X X X | Grenzwert |
| OVE8101-R86 | Betriebsbauten (OIB) | a (gemäß EN 1838) | X X X X X X – | Grenzwert |
| OVE8101-R87 | Bereiche mit besonderer Gefährdung | a; Änderung der Betriebsdauer gemäß EN 50172 nach Risikobeurteilung (Fußnote e) | X X X X X X – | Grenzwert |
| OVE8101-R88 | Krankenhäuser | a; **max. Umschaltzeit 15 s** | X X X X X X – | Grenzwert |
| OVE8101-R89 | Pflegeheime | **8 h** (Fußnote f → Teil 7-710) | X X X X X X – | Grenzwert |
| OVE8101-R90 | Arbeitsstätten (ASchG) | siehe Arbeitsstättenverordnung | — | Gebot |
| OVE8101-R91 | Fußnoten c/d (S. 485) | Einzelbatteriesysteme: Herstellerangaben (insb. zulässige Umgebungstemperaturen) beachten; Bemessungsbetriebsdauer der Quelle ≥ Tabellenwert; Batterie-Nennbetriebsdauer darf bei zusätzlichem Sicherheitsstromaggregat auf 1 h reduziert werden, wenn der SV-Hauptverteiler am Aggregat hängt und die geforderte Nennbetriebsdauer über das Aggregat gesichert ist. | 1 h Reduktion | Gebot |

### Anhang 56.B (informativ) — Tabelle 56.B.1 brandschutztechnische Einrichtungen (S. 486)

| ID | Einrichtung | Bemessungsbetriebsdauer / max. Umschaltzeit | Typ |
|---|---|---|---|
| OVE8101-R92 | Anlagen zur Löschwasserversorgung (ohne Sprinkler gemäß TRVB 127 S) | 12 h / 15 s | Grenzwert |
| OVE8101-R93 | Feuerwehraufzüge | 8 h / 15 s | Grenzwert |
| OVE8101-R94 | Alarmierungs-/Evakuierungsanlagen | 3 h / 15 s | Grenzwert |
| OVE8101-R95 | Mechanische Rauch-/Wärmeabzugs-, Druckbelüftungsanlagen | 3 h / 15 s | Grenzwert |
| OVE8101-R96 | CO-Warnanlagen | 1 h / 15 s | Grenzwert |

### Nationale Ergänzung 56.NE (normativ, S. 487–489)

| ID | §/Abschnitt (Seite) | Regel | Werte/Grenzwerte | Typ |
|---|---|---|---|---|
| OVE8101-R97 | 56.NE.560.514.5.1.2 (S. 487) | Schaltplan der Sicherheitsbeleuchtung muss bei Schalteinrichtung, Sicherheitsstromquelle und Hauptverteiler vorhanden sein; Inhalt: Stromlaufplan inkl. Netzüberwachung, **Anzahl der Leuchten je Endstromkreis**, Belastung je Endstromkreis + Gesamtbelastung. | — | Gebot |
| OVE8101-R98 | 56.NE.560.600.4.1 Nr. 7 (S. 488) | Erstprüfung: lichttechnische Anforderungen gemäß ÖNORM EN 1838 durch Messung der Beleuchtungsstärke nachweisen; wo Messung nicht möglich: Berechnung oder Übertragung von Messwerten aus Bereichen mit gleichen Leuchtmitteln und gleicher Einbauhöhe. | — | Gebot |
| OVE8101-R99 | 56.NE.560.600.5.1/5.2 (S. 488) | Wiederkehrende Prüfung: ohne automatische Prüfeinrichtung gemäß EN 50172, mit automatischer Prüfeinrichtung gemäß EN 62034; jährlicher Nachweis der Bemessungsbetriebsdauer der Batterie. | jährlich | Gebot |
| OVE8101-R100 | 56.NE.560.600.5.3/5.4 (S. 488–489) | Monatlicher Funktionstest des Aggregats mit ≥ 50 % der Bemessungsleistung (mind. schadfreie Minimalleistung); mindestens jährlich Funktionsprüfung ≥ 1 h durch Unterbrechung der Hauptzuleitung. | monatlich ≥ 50 %; jährlich ≥ 1 h | Gebot |
| OVE8101-R101 | 56.NE.560.600.5.7 (S. 489) | Messung der Beleuchtungsstärke der Sicherheitsbeleuchtung gemäß ÖNORM EN 1838 in Abständen von höchstens 3 Jahren. | ≤ 3 Jahre | Gebot |
| OVE8101-R102 | 56.NE.560.6.500.9 (S. 489) | Prüfbücher über regelmäßige Prüfungen führen; Kontrolle über mindestens 3 Jahre; der Dokumentation beifügen. | ≥ 3 Jahre | Gebot |

### Teil 4-42 — 422.2 Evakuierung im Notfall (Fluchtwege/Treppenhäuser, S. 170–171)

| ID | §/Abschnitt (Seite) | Regel | Werte/Grenzwerte | Typ |
|---|---|---|---|---|
| OVE8101-R103 | 422.2 (S. 170) | Evakuierungs-Merkmale gemäß Teil 5-51 Tab. 51.A: BD2 (geringe Personendichte, schwierige Evakuierung), BD3 (große Dichte, einfach), BD4 (große Dichte, schwierig); Kabelauswahl in Fluchtwegen gemäß OIB-Richtlinien; 422.2 + R 12-2 ergänzen die bautechnischen Brandschutzanforderungen. | — | Definition |
| OVE8101-R104 | 422.2.1 (S. 170) | Kabel-/Leitungsanlagen dürfen grundsätzlich NICHT in notwendige Treppenhäuser bzw. gesicherte Fluchtbereiche hinein- oder hindurchführen — außer brandschutztechnisch ummantelt/umhüllt. | — | Verbot |
| OVE8101-R105 | 422.2.1 (S. 170) | Solche Kabelanlagen dürfen sich nicht im Handbereich befinden, außer mit Schutz gegen mechanische Beschädigung während eines Rettungsvorgangs. | — | Verbot |
| OVE8101-R106 | 422.2.1 (S. 171) | Kabelanlagen in notwendigen Treppenhäusern/gesicherten Fluchtbereichen: kürzeste Wege, nicht flammenausbreitend (EN 60332-Reihe u. a.), nur geringe Rauchentwicklung (Empfehlung: Lichtdurchlassgrad 60 % gemäß EN 61034-2). | — | Gebot |
| OVE8101-R107 | 422.2.1 (S. 171) | **Kabelanlagen, die Sicherheitsstromkreise versorgen: Feuerwiderstandsdauer gemäß R 12-2 bzw. Behördenvorschreibung — fehlen solche Bestimmungen: 1 Stunde.** | 1 h Default | Grenzwert |
| OVE8101-R108 | 422.2.2 (S. 171) | Schalt-/Steuergeräte in Treppenhäusern/Fluchtbereichen (außer flucht-erleichternde) nur für zugelassene Personen zugänglich; in Gängen: Unterbringung in Schränken/Gehäusen aus nichtbrennbarem/schwer brennbarem Material. | — | Gebot |
| OVE8101-R109 | 422.2.3 (S. 171) | In notwendigen Treppenhäusern bzw. gesicherten Fluchtbereichen ist die Verwendung elektrischer Betriebsmittel mit entzündlichen Flüssigkeiten VERBOTEN. | — | Verbot |

### Teil 7-710 — Medizinisch genutzte Bereiche (Auszug Sicherheitszwecke/Beleuchtung)

| ID | §/Abschnitt (Seite) | Regel | Werte/Grenzwerte | Typ |
|---|---|---|---|---|
| OVE8101-R110 | 710.559.101 (S. 600) | Gruppe 1: mindestens zwei verschiedene Stromquellen für Beleuchtungsstromkreise, davon eine Sicherheitsstromquelle; Gruppe 2: allgemeine Raumbeleuchtung aus SV ≤ 0,5 s UND SV ≤ 15 s, mindestens 50 % der Raumbeleuchtung an SV ≤ 15 s. | ≥ 50 % | Gebot |
| OVE8101-R111 | 710.559.101 (S. 600) | **In Fluchtwegen (medizinischer Bereich) müssen die Leuchten der Allgemeinbeleuchtung abwechselnd auf zwei Stromquellen aufgeteilt werden, davon mindestens eine Sicherheitsstromquelle.** | 2 Stromquellen | Gebot |
| OVE8101-R112 | 710.560.9 (S. 605) | Umschaltzeit der Sicherheitsstromquelle ≤ 15 s; Mindestbeleuchtungsstärke erforderlich in: Räumen für Sicherheitsstromquellen und Hauptverteilern (AV + SV), Bereichen lebenswichtiger Dienste (je Bereich ≥ 1 Leuchte an SV), Standorten von Brandmeldezentrale/Überwachungsanlagen, Etagenbädern/Toiletten/Nasszellen für Patienten, betriebsnotwendigen Räumen (je Raum ≥ 1 Leuchte an SV). | ≤ 15 s; ≥ 1 Leuchte je Raum | Gebot |
| OVE8101-R113 | 710.560.9 (S. 605) | Bei Schutz durch automatische Abschaltung: Stromkreise so anordnen, dass beim Ansprechen einer Schutzeinrichtung NICHT alle Beleuchtungsstromkreise eines Raums oder Fluchtwegs ausfallen. | — | Verbot |
| OVE8101-R114 | 710.560.6.104.1 (S. 602) | SV ≤ 0,5 s muss ≥ 3 h versorgen: OP-Leuchten/unentbehrliche Leuchten, lebenserhaltende/lebenswichtige chirurgische ME-Geräte, lebenswichtige Überwachung, ME-Geräte mit anwendungsnotwendigen Lichtquellen; Reduktion auf 1 h nur mit weiterer unabhängiger 3-h-Quelle. | ≤ 0,5 s; 3 h (1 h) | Grenzwert |
| OVE8101-R115 | 710.560.6.104.2 (S. 603) | SV ≤ 15 s: Verbraucher gemäß 710.560.9 + 710.56 innerhalb 15 s mit sicherer Quelle für ≥ 24 h verbinden (Auslöser: Spannung < 90 % Un an ≥ 1 Außenleiter > 0,5 s); Reduktion auf 3 h, wenn Behandlung beendet + Gebäude in 3 h evakuierbar. | 15 s; 24 h→3 h; 90 % Un/0,5 s | Grenzwert |
| OVE8101-R116 | 710.560.6.104.3 (S. 603) | SV > 15 s: übrige betriebsnotwendige Verbraucher automatisch oder manuell an Sicherheitsstromquelle ≥ 24 h (Reduktion auf ≥ 3 h analog). | 24 h→3 h | Grenzwert |
| OVE8101-R117 | 710.560.6.1.101 (S. 603) | Batterien mit Primärzellen sind als Sicherheitsstromquellen (Gruppe 1 und 2) NICHT zulässig. | — | Verbot |
| OVE8101-R118 | 710.52 (S. 605) | In einem mehradrigen Kabel der Sicherheitsstromversorgung darf ein Stromkreis nur mit einem zugehörigen Hilfsstromkreis zusammengefasst werden; Zusammenfassen mehrerer Hauptstromkreise (z. B. Beleuchtungsstromkreise mit gemeinsamem Neutralleiter) ist NICHT zulässig. | — | Verbot |
| OVE8101-R119 | 710.52 (S. 604–605) | Erdverlegung AV/SV ≤ 15 s/SV ≤ 0,5 s: getrennte Trassen ≥ 2 m bzw. Stufenkünette ≥ 1 m; außerhalb des Erdreichs gemeinsame Trasse nur mit Funktionserhalt ≥ 90 min gemäß ÖNORM DIN 4102-12 (entfällt bei anderweitiger Gewährleistung). | 2 m; 1 m; 90 min | Gebot |
| OVE8101-R120 | 710.NE.1.4 (S. 615) | Gruppe-1-Räume: Ersatzbeleuchtung für 1 h mit Umschaltzeit ≤ 15 s; Gruppe-2-Räume: OP-/unentbehrliche Leuchten + lebenswichtige ME-Geräte aus SV ≤ 0,5 s für ≥ 3 h (regelt NICHT die Fluchtweg-Sicherheitsbeleuchtung). | 1 h/15 s; 3 h/0,5 s | Grenzwert |
| OVE8101-R121 | 710.NE.3.1.1.2 (S. 617) | **Pflegeheime/Kuranstalten: Sicherheitsbeleuchtung in Fluchtwegen gemäß Teil 5-56 mit gesamter Mindestbetriebsdauer 8 h** (Kombination Batterie + Aggregat zulässig). | 8 h | Grenzwert |
| OVE8101-R122 | 710.NE.3.1.1.3 (S. 617) | In für Heimbewohner zugänglichen Sanitärräumen: Maßnahmen für gefahrloses Verlassen bei Stromausfall (z. B. Sicherheitsleuchte, beleuchteter Notruftaster, Leuchtfolie). | — | Gebot |
| OVE8101-R123 | 710.NE.3.1.1.1 (S. 617) | Pflegeheim-Aggregat: stationär ≥ 24 h Betriebsdauer oder transportabel binnen 3 h betriebsbereit mit 24 h Betriebsdauer (Nachtanken organisatorisch zulässig). | 24 h; 3 h | Grenzwert |

### Teil 7-718 — Öffentliche Einrichtungen und Arbeitsstätten

| ID | §/Abschnitt (Seite) | Regel | Werte/Grenzwerte | Typ |
|---|---|---|---|---|
| OVE8101-R124 | 718.1 (S. 675) | Anwendungsbereich: Versammlungsstätten, Ausstellungs-/Verkaufsstätten, Gaststätten, Beherbergung, Heime, Schulen/Kindergärten, Garagen, verkehrstechnische Gebäude, Gebäude Fluchtniveau > 22 m, Betriebsbauten, Arbeitsstätten (ASchG); **Zugänge und Fluchtwege gehören dazu**; bei Mehrfach-Zuordnung gelten die jeweils höheren Sicherheitsanforderungen. | — | Gebot |
| OVE8101-R125 | 718.559.101.1 (S. 677) | Allgemeinbeleuchtung: Räume mit geringem Risiko (BD1) 1 Endstromkreis zulässig; andere Räume (BD2–BD4): ≥ 2 Endstromkreise, sodass ein Fehler eines Endstromkreises nicht zu unzureichender Beleuchtung führt; eine RCD darf dabei nicht mehr als einen Endstromkreis versorgen. | ≥ 2 Endstromkreise; 1 RCD = 1 Kreis | Gebot |
| OVE8101-R126 | 718.559.101.2 (S. 678) | Dimmbare Allgemeinbeleuchtung in öffentlich zugänglichen Bereichen: volle Beleuchtungsstärke muss von geeigneter Stelle wiederherstellbar sein. | — | Gebot |
| OVE8101-R127 | 718.560.9.001.AT Nr. 1 (S. 678) | **Zusätzliche Sicherheitsbeleuchtung erforderlich (bei erhöhten Anforderungen gemäß R 12-2/OIB-2): bei Fahrtreppen, in Sanitärbereichen ab 8 m² Größe und in barrierefreien WC-Anlagen** (Aufzüge: EN 81-20/81-72, TRVB 150 S). | ≥ 8 m² | Gebot |
| OVE8101-R128 | 718.560.9.001.AT Nr. 2 (S. 678) | **Zusätzliche Sicherheitsbeleuchtung in: Räumen für Sicherheits-/Ersatzstromaggregate, Räumen der Hauptverteiler (SV-, Ersatz- und allgemeine Stromversorgung), Schaltanlagen > 1 kV, Räumen zur Bedienung zentraler brandschutztechnischer Einrichtungen (z. B. Sprinklerzentrale, Brandmeldezentrale).** | — | Gebot |
| OVE8101-R129 | 718.560.9.001.AT Nr. 3 (S. 678) | **Verkehrstechnische Einrichtungen (Flughäfen, Bahnhöfe), zusätzlich zu Nr. 1+2: Sicherheitsbeleuchtung (Antipanikbeleuchtung) in Wartezonen, Abfertigungshallen, Geschäftsflächen über 60 m² sowie in Arbeitsräumen und betriebsnotwendigen Räumen über 60 m²** (siehe EN 50172). | > 60 m² | Gebot |
| OVE8101-R130 | 718.560.9.002.AT (S. 678) | Arbeitsstätten gemäß ASchG: für die Sicherheitsbeleuchtung gelten grundsätzlich die Anforderungen der Arbeitsstättenverordnung (Details: AStV + ÖNORM EN 1838). | — | Gebot |
| OVE8101-R131 | 718.NE.1.1 (S. 679) | 718.NE.1 (Versammlungsstätten) gilt ergänzend ab > 400 Personen (innerhalb von Gebäuden) bzw. > 5 000 Personen (Versammlungs-/Sportstätten außerhalb von Gebäuden). | 400 / 5 000 Personen | Definition |
| OVE8101-R132 | 718.NE.1.560.9 (S. 680) | **Antipanikbeleuchtung gemäß ÖNORM EN 1838 erforderlich in: Versammlungsstätten, Bühnenbetriebsräumen über 20 m² (Probebühnen, Chor-/Ballett-/Orchesterübungsräume, Stimmzimmer, Aufenthaltsräume Mitwirkender), Bildwerferräumen, Manegen, Sportrennbahnen, Stehplatzbereichen von Versammlungsstätten mit nicht überdachten Spielflächen.** | > 20 m² | Gebot |
| OVE8101-R133 | 718.NE.1.560.9 (S. 680) | Erleichterung: Theater/Film-Versammlungsstätten für höchstens 400 Personen mit Fußböden ≤ 1 m über/unter den Fluchtweg-Verkehrsflächen: Sicherheitsbeleuchtung darf so bemessen werden, dass bei Verdunklung und Netzausfall mindestens Türen, Gänge und Stufen erkennbar sind. | ≤ 400 Pers.; ≤ 1 m | Gebot |
| OVE8101-R134 | 718.NE.1.560.9.003.AT a) (S. 681) | Antipanikbeleuchtung in betriebsmäßig verdunkelbaren Räumen: unabhängig von der Verdunkelungssteuerung vom verdunkelten Raum aus einschaltbar; **eine Helligkeitsregelung (Dimmung) ist NICHT zulässig**. | — | Verbot |
| OVE8101-R135 | 718.NE.1.560.9.003.AT b)+c) (S. 681) | Schaltstellen der Antipanikbeleuchtung: nahe mindestens je einem Ausgang jeder Platzfläche, für Aufsichtspersonen leicht zugänglich, gegen unbeabsichtigte Betätigung gesichert; Bühnen-Schaltstelle nahe der Zugangstür auf der Bühne; Schaltstellen sind zu beleuchten; Einschaltung durch einen Schalter darf nicht durch einen anderen aufgehoben werden können (Ausschalten im Lichtregieraum zulässig). | — | Gebot |
| OVE8101-R136 | 718.NE.1.560.9.4 Nr. 1 (S. 681) | **Dauerbetrieb der Sicherheitsbeleuchtung zwingend bei: a) Fluchtwegen außerhalb von Versammlungsräumen/Bühnen/Szenenflächen, b) Fluchtwegen außerhalb nicht überdachter Platzflächen von Versammlungsstätten mit nicht überdachten Spielflächen, c) Hinweisen auf Fluchtwege (Sicherheitszeichen).** | — | Gebot |
| OVE8101-R137 | 718.NE.1.560.9.4 Nr. 2 (S. 681) | In betriebsmäßig verdunkelten Räumen ist Bereitschaftsbetrieb zulässig — AUSGENOMMEN Sicherheitsleuchten mit Sicherheitszeichen; Erkennbarkeit von Fluchttüren, Gängen, Stufen muss gegeben sein; diese Bereitschafts-Sicherheitsbeleuchtung darf bei Wiederkehr der allgemeinen Stromversorgung NICHT von selbst ausschalten (nur von Hand am Bedienteil). | — | Verbot |
| OVE8101-R138 | 718.NE.1.560.6 (S. 680) | Versammlungsstätten mit nicht überdachten Spielflächen: andere Stromquellen als Sicherheitsstromquellen nur zulässig, wenn Aggregat + Kraftstoffbehälter dem Zugriff Unbefugter entzogen sind und auch im Panik-/Brandfall die Sicherheitsbeleuchtung versorgt werden kann. | — | Gebot |
| OVE8101-R139 | 718.512.2.001.AT (S. 676) | Öffentlich zugängliche Bereiche: Hausanschlusskästen/Hauptverteiler in eigenen Räumen oder Nischen (Abtrennung REI30/EI30, Feuerschutzabschlüsse EI30; im Gefahrenfall leicht und sicher erreichbar). | REI30/EI30 | Gebot |
| OVE8101-R140 | 718.NE.2 (S. 681–682) | Garagen-NE gilt für Garagen/überdachte Stellplätze/Parkdecks > 1 600 m² Nutzfläche; Steckdosen im Bereich von Einstellplätzen/Verkehrsflächen dürfen NICHT an Stromkreise der allgemeinen Beleuchtung angeschlossen werden. | > 1 600 m² | Verbot |

### Sonstige Teile (Sicherheitsbeleuchtungs-Bezug)

| ID | §/Abschnitt (Seite) | Regel | Werte/Grenzwerte | Typ |
|---|---|---|---|---|
| OVE8101-R141 | 559.1 (S. 464) | Anforderungen für eine Notbeleuchtung: siehe Teil 5-56, ÖVE/ÖNORM EN 50172, ÖNORM EN 1838 und ÖVE/ÖNORM EN 60598-2-22 (Einzelbatterieleuchten). | — | Gebot |
| OVE8101-R142 | 704.56 (S. 546) | Baustellen: Einrichtungen für Sicherheitszwecke (z. B. Sicherheitsbeleuchtung) können erforderlich sein. | — | Empfehlung |
| OVE8101-R143 | 711.560.9 (S. 630) | Ausstellungen/Shows/Stände: ist eine Sicherheitsbeleuchtung erforderlich → Teil 5-56 und OVE-Richtlinie R 12-2. | — | Gebot |
| OVE8101-R144 | 729.560.9 (S. 712) | Abgeschlossene elektrische Betriebsstätten: je nach Größe Notbeleuchtung errichten oder organisatorische Maßnahmen treffen; Arbeitsstätten → Arbeitsstättenverordnung. | — | Empfehlung |
| OVE8101-R145 | 740.415 ANM. 2.AT (S. ~726) | Fliegende Bauten/Zirkusse: ist eine Sicherheitsbeleuchtung erforderlich → Teil 5-56. | — | Gebot |
| OVE8101-R146 | 560.1 (S. 473) | Teil 5-56 gilt NICHT für Anlagen in explosionsgefährdeten Bereichen (BE3 → EN 60079-14) und NICHT für Ersatzstromversorgungsanlagen (→ Abschnitt 551). | — | Definition |

**Bilanz: 146 Regeln, davon 17 explizite Verbote** (R15, R20, R23, R29, R38, R44, R64, R66, R104, R105, R109, R113, R117, R118, R134, R137, R140).

## Detail-Digest der relevanten Abschnitte

### Teil 5-56 „Einrichtungen für Sicherheitszwecke" (PDF-S. 473–491) — vollständig

**560.1 Anwendungsbereich (S. 473).** Allgemeine Anforderungen für Einrichtungen für Sicherheitszwecke, deren elektrische Anlagen und Stromquellen. Ergänzende Anforderungen in Teil 7-718 (öffentliche Einrichtungen/Arbeitsstätten) und Teil 7-710 (Krankenhäuser/medizinische Bereiche). Gilt nicht für BE3-Bereiche (→ EN 60079-14) und nicht für Ersatzstromversorgungsanlagen (→ 551). Plus 56.NE.

**560.4 Klassifizierung (S. 473–474).** Nicht-automatische vs. automatische Stromversorgung; automatische nach maximaler Umschaltzeit: unterbrechungsfrei (fortlaufende Versorgung innerhalb festgelegter Spannungs-/Frequenzbedingungen), sehr kurze Unterbrechung ≤ 0,15 s, kurze ≤ 0,5 s, durchschnittliche ≤ 5 s, mittlere ≤ 15 s, lange > 15 s. AT: nicht-automatische Versorgung kommt in 7-710/7-718 nicht zur Anwendung. Betriebsmittel müssen mit der Umschaltzeit kompatibel sein (560.4.2).

**560.5 Allgemeines (S. 474–475).** Funktion ggf. zu jeder Zeit — auch bei Ausfall der Haupt-/lokalen Versorgung und im Brandfall; dafür besondere Stromquellen, Betriebsmittel, Stromkreise, Kabelanlagen. Ergänzend gilt OVE-Richtlinie R 12-2. Die nationale Funktionserhalt-Notwendigkeit ergibt sich aus brandschutz-/bautechnischen Richtlinien bzw. Behördenvorschreibung oder aus R 12-2 (erhöhte Anforderungen nach Nutzungsart). Bei Brandfall-Funktionserhalt (560.5.2): Quelle mit ausreichender Versorgungsdauer + feuerbeständig geschützte Betriebsmittel (Dauer → R 12-2); die Sicherheitsstromquelle existiert zusätzlich zur allgemeinen Versorgung. 560.5.3: Schutzmaßnahmen ohne automatische Abschaltung beim ersten Fehler bevorzugen; IT-System mit Isolationsüberwachung (akustisch + optisch). 560.5.4: Störungen in Steuerungs-/Bussystemen dürfen die Sicherheitsfunktion nicht beeinträchtigen. 560.5.001.AT: zentrale Zustandsanzeige (betriebsbereit/SV-Speisung/Störung) an ständig überwachter Stelle — nicht nötig bei Einzelbatterieanlagen bis 20 Sicherheitsleuchten; akustische Meldung zusätzlich erlaubt, Meldung über Gebäudeleitsystem erlaubt.

**560.6 Stromquellen (S. 475–476).** Zulässig: Sekundärzellen-Batterien, Primärzellen-Batterien, unabhängige Generatoren, separate unabhängige Netzeinspeisung. Einzelbatterie-Sicherheitsleuchten → EN 60598-2-22. **Primärzellen für Sicherheitsbeleuchtungsanlagen verboten.** Ortsfest; unbeeinflusst vom Ausfall der allgemeinen Versorgung; Standort nur BA4/BA5-zugänglich, ständig be-/entlüftet, keine Gase in Personenbereiche. Separate Doppel-Einspeisung nur bei zugesichert unwahrscheinlichem Gleichzeitig-Ausfall. Ausreichende Kapazität. Fremdnutzung nur ohne Verfügbarkeits-Beeinträchtigung; Fehler in Fremdkreisen dürfen Sicherheitskreise nicht unterbrechen. Parallelbetriebs-Regeln (560.6.8/560.6.9). CPS (560.6.10): wartungsarme Batterien geschlossener/verschlossener Bauart, Industrieausführung (EN 60623/EN 60896); Systeme für Sicherheitsbeleuchtung → EN 50171. LPS (560.6.11): 500 W/3 h bzw. 1 500 W/1 h; sonst wie CPS. USV (560.6.12): Schutzeinrichtungen auslösen können, Notbetrieb aus Batterie starten/betreiben, 560.6.10, EN 62040-1/-3. Aggregate (560.6.13): ISO 8528-12, DIN 6280-12/-13. Zustandsanzeige (560.6.14).

**560.7 Stromkreise (S. 476–478).** Unabhängigkeit von anderen Stromkreisen (ggf. feuerbeständige Trennung, getrennte Trassen, Umhüllung). Führungsverbote: nicht durch BE2 (außer 560.8.1-Ausführung), niemals durch BE3. Überlastschutz-Verzicht mit Anzeige möglich; Überstromschutz-Selektivität zwischen Sicherheitsstromkreisen. Schalt-/Steuergeräte gekennzeichnet + zugriffsbeschränkt (versperrbares Gehäuse genügt). Zwei-Kreis-Versorgung: gegenseitige Nicht-Beeinträchtigung, ggf. Schutzleiter beider Kreise. Trennung von Fremdkabeln durch Abstand/Trennsteg (wenn nicht 560.8.1/2-Ausführung); gemeinsame Verlegung mehrerer Sicherheitsstromkreise zulässig; im letzten Brandabschnitt gemeinsames Tragsystem zulässig. **Verbot Aufzugs-/Kaminschächte** (außer Feuerwehraufzugs-Zuleitungen). Dokumentation: Prinzipschaltplan, Quellen-Angaben, Lagepläne aller Betriebsmittel/Sicherheitseinrichtungen mit Endstromkreis-Kennzeichnung, Verbraucherliste, Betriebsanleitungen. Batterieanlagen → EN 50272-2.

**560.8 Kabel-/Leitungsanlagen (S. 478–479).** Funktionserhalt-Optionen: mineralisolierte Kabel (EN 60702-1/-2); feuerbeständige Kabel mit Isolationserhalt (OVE EN 50200 + EN 60332-1-2); geschützte Kabelanlage (Funktionserhalt ÖNORM DIN 4102-12 o. glw., bauliche Umhüllung, getrennte Brandabschnitte, Schienenverteiler in Schacht/Kanal mit integriertem Funktionserhalt). Befestigung brandfallsicher (Hinweis auf R 12-2 für Ausführung inkl. Verteiler und Leitungsverbindungen). Gilt auch für Steuer-/Bussysteme. Erdverlegung: Schutz vor Erdarbeiten; AT-Beispiel 2 m Trassenabstand bzw. 1 m Stufenkünette. DC-Kreise: zweipoliger Überstromschutz; kombinierte AC/DC-Geräte für beides geeignet.

**560.9 Sicherheitsbeleuchtungsanlagen (S. 479–481).** Normverweis-Dreieck: WO nach Nutzung → R 12-2; WIE errichten/betreiben/warten → EN 50172; lichttechnische Werte + Messung → EN 1838 (Sonderfälle: EN 12193 Sport; EN 81-20/81-72 + TRVB 150 S Aufzüge). Systemwahl: zentrale Versorgung oder Einzelbatterieleuchten (letztere von 560.9.1–560.9.4-Versorgungsanforderungen ausgenommen). Zentral: Funktionserhalt der Versorgung bis zu den Leuchten durch Brandabschnitte (560.8.1/2), innerhalb des Brandabschnitts 527.1. **Kernregel Platzierung/Stromkreise: > 1 Sicherheitsleuchte im Brandabschnitt → abwechselnde Aufteilung auf ≥ 2 Stromkreise, sodass bei Einzelkreis-Ausfall eine Grundbeleuchtung entlang des Fluchtwegs bleibt.** Kurzschluss in einem Kreis darf Nachbarleuchten (auch anderer Brandabschnitte) nicht ausfallen lassen. **Endstromkreis-Limit: ≤ 20 Leuchten und ≤ 60 % des Nennstroms der Überstrom-Schutzeinrichtung.** Evakuierung: Mindestbeleuchtungsstärke, Umschaltzeit, Bemessungsbetriebsdauer gemäß EN 1838 (Leitfaden: Tab. 56.A.1.AT; Arbeitsstätten: AStV). Betriebsarten: Dauer-/Bereitschaftsbetrieb, kombinierbar; im Bereitschaftsbetrieb Endstromkreis-Überwachung der Allgemeinbeleuchtung + automatische Aktivierung; kombinierte Systeme mit eigener Überwachung je Umschaltvorrichtung; gemeinsames Schalten mit Allgemeinbeleuchtung nur in nicht verdunkelbaren oder nicht ständig genutzten Bereichen. Steuerungssysteme dürfen nie beeinträchtigen (funktionale Sicherheit, EN 61508-4); bei Steuerungs-/Endstromkreis-Fehler volle Beleuchtungsstärke im betroffenen Bereich. Umschaltschwellen: Notbetrieb bei U < 0,6 Un für > 0,5 s; Rückschaltung bei U > 0,85 Un; automatische Abschaltung nach Netzwiederkehr (mit Wiederzünd-Zeit), aber nicht in betrieblich verdunkelten Räumen. Bereichsweise Überwachung zulässig. Lampen/Umschaltzeit abgestimmt. Steuerschalter gegen Unbefugte, Zustandsanzeige je Quelle gut einsehbar. Kennzeichnung: rotes oder grünes Schild an Leuchte/Komponenten (AT: Alternativen zulässig) + **Verteiler-, Stromkreis- und Leuchtennummer an/nahe der Leuchte** (→ Render/Beschriftung im Plan). **> 20 Sicherheitsleuchten je zusammenhängendem Gebäudeteil → automatische Prüfeinrichtung mit zentraler Erfassung (EN 62034)**: Ladungsüberwachung kontinuierlich/< 5 min, tägliche Funktionsprüfung der Leuchtmittel (Fehleranzeige ab 1 ausgefallener Leuchte, Prüfdauer 0,5–5 min), Fehlermeldung bei Übertragungsstörungen.

**560.10 Brandschutztechnische Einrichtungen (S. 481–482).** (Brandmelde-, Löscha-, RWA-, Druckbelüftungs-, Löschwasseranlagen …) — separater Stromkreis von der Hauptverteilung; vorrangige Stromkreise direkt an Einspeiseseite des Trennschalters; Alarmierungsgeräte gekennzeichnet; Errichtung → Tab. 56.B.1.

**Anhang 56.A (informativ, S. 483–485) — Tabelle 56.A.1.AT.** EN-1838-Werte gelten; Tabelle ergänzt je Nutzungsart Bemessungsbetriebsdauer (h), Umschaltzeit, zulässige Versorgungssysteme, Sicherheitszeichen-Dauerbetrieb — siehe Regeln R76–R91. Kernwerte: Standard 3 h; Beherbergung 8 h; Pflegeheime 8 h; Wohnhochhaus > 32 m Fluchtniveau 8 h; vorübergehende Aufbauten ≥ 1 h; Krankenhäuser Umschaltzeit 15 s; Garagen/niedrige Gebäude/Betriebsbauten rein nach EN 1838; Bereiche besonderer Gefährdung: Betriebsdauer-Anpassung per Risikobeurteilung (EN 50172). Fußnote d: Batterie-Nennbetriebsdauer auf 1 h reduzierbar bei zusätzlichem Aggregat, das die geforderte Dauer übernimmt.

**Anhang 56.B (informativ, S. 486) — Tabelle 56.B.1.** Betriebsdauern/Umschaltzeiten für Brandschutz-Einrichtungen: Löschwasser 12 h/15 s; Feuerwehraufzüge 8 h/15 s; Alarmierung/Evakuierung 3 h/15 s; RWA/Druckbelüftung 3 h/15 s; CO-Warnanlagen 1 h/15 s. (Geeignete-System-Markierungen der Tabelle sind im Text-Extrakt nicht lesbar — siehe Extraktionslücke E2.)

**56.NE (normativ, S. 487–489).** Instandhaltung nach Herstellerangaben. Schaltplan-Pflicht der Sicherheitsbeleuchtung (bei Schalteinrichtung, Quelle, Hauptverteiler) mit Stromlaufplan inkl. Netzüberwachung, Leuchtenanzahl je Endstromkreis, Belastungen. Erstprüfung: Lüftung Batterieraum (EN 50272-2), Aggregat-Aufstellraum, Batteriebemessung/Kapazität, Aggregat-Bemessung (Anlaufströme), Funktionsprüfungen inkl. Netzunterbrechung, lichttechnischer Nachweis nach EN 1838 (Messung; ersatzweise Berechnung/Übertragung bei gleichen Leuchtmitteln + gleicher Einbauhöhe). Wiederkehrend: ohne Prüfeinrichtung → EN 50172; mit → EN 62034; monatlicher Aggregat-Funktionstest ≥ 50 % Bemessungsleistung + Sichtprüfung + Kraftstoffvorratskontrolle; jährliche Aggregat-Funktionsprüfung ≥ 1 h; jährliche Umschalteinrichtungs-Prüfung (Doppeleinspeisung); jährlicher Leistungsnachweis der Quelle; **Beleuchtungsstärke-Messung nach EN 1838 höchstens alle 3 Jahre**; jährliche manuelle Prüfung bei EN-62034-Systemen; Prüfbücher ≥ 3 Jahre.

### Teil 4-42 §422.2 — Evakuierung im Notfall (S. 170–171)

Begriffe: „gesicherter Fluchtbereich" = AStV-Begriff (brandschutztechnisch höherwertig, direkt ins Freie, z. B. Treppenhaus, Fluchttunnel); „notwendiges Treppenhaus" = OIB-Richtlinie 2:2019 Abschn. 5.1.1. Kabelauswahl in Fluchtwegen → OIB-Richtlinien; 422.2 + R 12-2 ergänzen. Evakuierungsklassen BD2/BD3/BD4 (Teil 5-51 Tab. 51.A). Regeln: Kabelanlagen grundsätzlich nicht in/durch notwendige Treppenhäuser bzw. gesicherte Fluchtbereiche (außer brandschutztechnisch ummantelt/umhüllt); nicht im Handbereich ohne mechanischen Schutz; kürzeste Wege; nicht flammenausbreitend; geringe Rauchentwicklung; **Sicherheitsstromkreis-Kabel: Feuerwiderstandsdauer nach R 12-2/Behörde, sonst Default 1 h**; Schalt-/Steuergeräte zugriffsbeschränkt bzw. in nichtbrennbaren Gehäusen; Verbot von Betriebsmitteln mit entzündlichen Flüssigkeiten.

### Teil 7-710 — Medizinisch genutzte Bereiche (S. ~585–621, Auszug)

SV-Klassen: SV ≤ 0,5 s (3 h; OP-/unentbehrliche Leuchten, lebenserhaltende ME-Geräte, Endoskopie-Lichtquellen; Reduktion auf 1 h nur mit weiterer unabhängiger 3-h-Quelle), SV ≤ 15 s (24 h für 710.560.9-Verbraucher + Sicherheitseinrichtungen; Trigger < 90 % Un für > 0,5 s; Reduktion auf 3 h bei evakuierbarem Betrieb), SV > 15 s (24 h→3 h für betriebsnotwendige Verbraucher). Primärzellen verboten. Beleuchtung: Gruppe 1 min. 2 Stromquellen (1× SV); Gruppe 2 Raumbeleuchtung aus SV ≤ 0,5 s und SV ≤ 15 s, ≥ 50 % an SV ≤ 15 s; **Fluchtwege: Allgemeinbeleuchtungs-Leuchten abwechselnd auf 2 Stromquellen (1× SV)**. 710.560.9: Umschaltzeit ≤ 15 s; Mindestbeleuchtungsstärke in Technikräumen (Quellen, Hauptverteiler), lebenswichtigen Bereichen (≥ 1 SV-Leuchte), Brandmeldezentrale/Überwachung, Patientenbädern/-toiletten/-nasszellen, betriebsnotwendigen Räumen (≥ 1 SV-Leuchte je Raum); nie alle Beleuchtungsstromkreise eines Raums/Fluchtwegs gleichzeitig abschaltbar. Verteilertrennung nach Versorgungsart (AV / SV ≤ 15 s / SV ≤ 0,5 s je eigene Verteilerbereiche, Trennung nach Funktionserhalt); mehradrige SV-Kabel: keine Zusammenfassung mehrerer Hauptstromkreise / kein gemeinsamer Neutralleiter. Trassenregeln (Erdreich 2 m/1 m-Stufe; gemeinsame Trasse außerhalb Erdreich nur mit 90-min-Funktionserhalt DIN 4102-12). NE: Gruppe-1-Ersatzbeleuchtung 1 h/≤ 15 s; Gruppe-2-Kernverbraucher 3 h aus SV ≤ 0,5 s (Fluchtweg-Sicherheitsbeleuchtung davon unberührt); Pflegeheime/Kuranstalten: Aggregat 24 h (transportabel binnen 3 h), **Fluchtweg-Sicherheitsbeleuchtung 8 h gesamt**, Sanitärräume mit Verlassens-Maßnahmen (Sicherheitsleuchte/Notruftaster/Leuchtfolie). Kennzeichnungsfarben: grün = SV ≤ 15 s-Bereiche, gelb/orange = SV ≤ 0,5 s-Bereiche (710.560.6.103 ANM. AT).

### Teil 7-718 — Öffentliche Einrichtungen und Arbeitsstätten (S. ~675–682)

Anwendungsbereich = die Nutzungsarten der Tab. 56.A.1.AT (inkl. Zugänge und Fluchtwege); bei Mehrfachnutzung höhere Anforderung maßgebend. Evakuierungsbedingungen BD festlegen (718.422.2.101). Allgemeinbeleuchtungs-Redundanz: BD1 1 Endstromkreis, sonst ≥ 2 Endstromkreise + RCD-Regel (1 RCD = max. 1 Endstromkreis). Dimm-Rückholung. **718.560.9.001.AT — konkrete Zusatz-Orte für Sicherheitsbeleuchtung:** Fahrtreppen, Sanitärbereiche ≥ 8 m², barrierefreie WCs; Aggregat-/Hauptverteilerräume, Schaltanlagen > 1 kV, Bedienräume zentraler Brandschutz-Einrichtungen; verkehrstechnische Gebäude: Antipanikbeleuchtung in Wartezonen, Abfertigungshallen, Geschäftsflächen > 60 m², Arbeits-/Betriebsräume > 60 m². Hinweis: adaptive dynamische Sicherheitsleitsysteme können zusätzlich nötig sein; optische Leitsysteme ersetzen keine Sicherheitsbeleuchtung. Arbeitsstätten → AStV. **718.NE.1 Versammlungsstätten (> 400 Personen innen / > 5 000 außen):** Antipanikbeleuchtung nach EN 1838 in Versammlungsstätten, Bühnenbetriebsräumen > 20 m², Bildwerferräumen, Manegen, Sportrennbahnen, Stehplatzbereichen; Erleichterung für kleine Theater ≤ 400 Personen (nur Türen/Gänge/Stufen erkennbar); Antipanik-Schalt-Anforderungen (keine Dimmung; Schaltstellen je Platzflächen-Ausgang, beleuchtet, nicht gegenseitig aufhebbar); **Dauerbetriebspflicht** für Fluchtwege außerhalb der Versammlungsräume/Bühnen und für Fluchtweg-Hinweise (Sicherheitszeichen); in verdunkelten Räumen Bereitschaftsbetrieb zulässig außer für Sicherheitsleuchten mit Sicherheitszeichen, kein Selbstabschalten bei Netzwiederkehr. Hauptverteiler-Räume REI30/EI30. 718.NE.2 Garagen > 1 600 m²: Lüfterredundanz, Steckdosen nicht an Beleuchtungsstromkreise.

### Verweisungen (S. 747 ff., Auswahl Notbeleuchtung)

ÖVE/ÖNORM EN 50171 (Zentrale Stromversorgungssysteme) · ÖVE/ÖNORM EN 50172 (Sicherheitsbeleuchtungsanlagen) · ÖVE/ÖNORM EN 62034 (Automatische Prüfsysteme für batteriebetriebene Sicherheitsbeleuchtung für Rettungswege) · ÖNORM EN 1838 (Angewandte Lichttechnik — Notbeleuchtung) · ÖVE/ÖNORM EN 60598-2-22 (Leuchten für Notbeleuchtung) · OVE-Richtlinie R 12-2 (Funktionserhalt/brandschutztechnische Anforderungen; mehrfach normativ referenziert, liegt nicht im Repo → Beschaffung prüfen).

## Offene Punkte / Extraktionslücken

- **[E1] Spaltenzuordnung Tabelle 56.A.1.AT (S. 483–485):** Die X/–-Marken wurden aus dem linearen Textfluss den 7 Spalten (Sicherheitszeichen-Dauerbetrieb, CPS, LPS, Einzelbatterie, Aggregat 0 s/≤ 0,5 s/≤ 15 s) in Lesereihenfolge zugeordnet. Die Zeilen sind konsistent (je 7 Marken), aber die exakte Spaltenzuordnung einzelner „–" (z. B. Krankenhäuser, Pflegeheime: letztes Feld „–" = Aggregat ≤ 15 s unzulässig?) sollte am PDF-Layout gegengeprüft werden, bevor die Engine daraus harte System-Zulässigkeitsregeln ableitet. Betriebsdauer- und Umschaltzeit-Spalten (lx/s/h-Werte) sind eindeutig.
- **[E2] Tabelle 56.B.1 (S. 486):** Die „geeignete Systeme"-Markierungen (Spalten 3–10) sind im Textextrakt als Grafik/Schattierung verloren gegangen; nur Betriebsdauer + Umschaltzeit (Spalten 1–2) und Fußnoten sind gesichert extrahiert.
- **[E3] OVE-Richtlinie R 12-2** wird in Teil 5-56 durchgehend normativ herangezogen (WO Sicherheitsbeleuchtung nach Nutzungsart, Funktionserhalt-Dauern, Aufstellräume der Stromquellen). Ohne R 12-2 kann die Engine die „Erforderlichkeit je Nutzungsart" nicht vollständig aus OVE-Quellen ableiten — Dokument beschaffen oder LB/EN-1838-Defaults als Fallback nutzen.
- **[E4]** Bilder 710.NE.4.001.AT/002.AT und 3.A-Netzbilder sind nur als Legenden extrahiert (Grafiken nicht im Textextrakt) — für die Engine ohne Belang, für menschliche Prüfung ggf. PDF konsultieren.
- **[E5]** Teil 7-718 nennt für Arbeitsstätten (ASchG) durchgehend die **Arbeitsstättenverordnung (AStV)** als maßgebliche Quelle für die Sicherheitsbeleuchtung — die AStV selbst ist nicht Teil dieser Norm; separate Extraktion nötig, falls Arbeitsstätten-Projekte geplant werden.
- Nicht vertieft (nach Kurzsichtung ohne Notbeleuchtungs-Regeln): Teile 4-41, 4-43…4-46, 5-51…5-54 (außer den zitierten Querverweisen 527.1, Tab. 51.ZA), 6, 7-701…7-709, 7-712…7-717, 7-721/722/730/753.
