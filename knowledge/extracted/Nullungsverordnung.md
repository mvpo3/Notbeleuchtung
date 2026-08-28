# Nullungsverordnung — Verordnung über die Anforderungen an öffentliche Verteilungsnetze mit der Nennspannung 400/230 V und an diese angeschlossene Verbraucheranlagen zur grundsätzlichen Anwendung der Schutzmaßnahme Nullung

**Quelle:** knowledge/Nullungsverordnung (1).pdf (RIS, Bundesrecht konsolidiert, Fassung vom 22.04.2024, 5 S.; StF BGBl. II Nr. 322/1998) · **Extrahiert:** 2026-08-28, Volltext via pypdf

## Relevanz für die Engine

Für die Notbeleuchtungs-Platzierung selbst **nicht platzierungsrelevant** — die Verordnung regelt die Schutzmaßnahme bei indirektem Berühren (Nullung/TN-System) in Verteilungsnetzen und Verbraucheranlagen, nicht Beleuchtung. Indirekt relevant:

1. **Netzkontext des Sicherheitskreises:** Der von der Engine geplante getrennte Sicherheitsstromkreis hängt an einer Verbraucheranlage, die in Österreich seit 1.1.1999 grundsätzlich auf Nullung (TN-System) auszuführen bzw. vorzubereiten ist (§ 3 Abs. 1, § 6 Abs. 1). Annahme „TN-System" ist für österreichische Neuanlagen die richtige Default-Netzform.
2. **Kein Hardcode-Bedarf:** Schutzmaßnahmen-Details (PEN/PE-Querschnitte, Hauptpotentialausgleich, Erder) gehören zur Elektro-Ausführungsplanung, nicht zum Notbeleuchtungs-Plan; sie können aber in einer LB auftauchen (z.B. „Anlage im TT-Netz") und wären dann LB-explizit zu behandeln.
3. Die Verordnung verweist durchgehend auf ÖVE-EN 1, Teil 1/1989 (abgedruckt im Anhang zur ETV 1993) — ein Beispiel dafür, wie österreichisches Recht Norminhalte über Verweise bindend macht (gleiche Mechanik wie ETV → Audit-Trail-Prinzip der Engine).

## Kernaussagen-Tabelle

| ID | §/Abschnitt (Seite) | Aussage | Typ |
|----|---------------------|---------|-----|
| NULL-R1 | § 1 Abs. 1 (S. 1) | Gegenstand: Erhöhung der Zuverlässigkeit der Schutzmaßnahmen bei indirektem Berühren und langfristige Vereinheitlichung (Nullung) in öffentlichen 400/230-V-Verteilungsnetzen und unmittelbar angeschlossenen Verbraucheranlagen. | Definition |
| NULL-R2 | § 1 Abs. 2 (S. 1) | Anlagen mit eigener Stromquelle (nicht aus öffentlichem Netz gespeist) fallen nur insoweit darunter, als spezielle technische Betriebs-Anforderungen vorliegen und abweichende Schutzmaßnahmen getroffen sind. | Info |
| NULL-R3 | § 2 Abs. 1 (S. 1) | Begriffe: Verbraucheranlage (alle ortsfesten Betriebsmittel inkl. Hauptleitungen nach dem Hausanschluss); Hauptleitungen (Hausanschluss bis Zähler); Nullungsverbindung (möglichst kurze leitfähige Verbindung PEN-Leiter ↔ Schutzleiter, direkt oder über Hauptpotentialausgleich, im ersten geeigneten Sicherungs-/Verteilerkasten). | Definition |
| NULL-R4 | § 2 Abs. 2 (S. 1) | Verwiesene Teile der ÖVE-EN 1 sind im Anhang zur ETV 1993 (BGBl. Nr. 47/1994) abgedruckt. | Verweis-auf-Norm |
| NULL-R5 | § 3 Abs. 1 (S. 2) | Ab 1.1.1999 sind neue öffentliche Verteilungsnetze so auszuführen, dass sie die technischen Voraussetzungen für die Nullung in den Verbraucheranlagen erfüllen, und mit Inbetriebnahme für die Nullung freizugeben (Ausnahme: Übergangsphase bei Neuaufschließungen, wenn Zusammenschluss HS-Schutzerder/NS-Betriebserder Nullung unzulässig macht, aber „Gebiet mit geschlossener Bebauung" i.S. ÖVE-EN 1, Teil 1/1989, § 3.6.14 zu erwarten ist). | Pflicht |
| NULL-R6 | § 3 Abs. 2–3 (S. 2) | Bestehende Netze: EVU müssen technische Eignung ehestmöglich prüfen und Freigabe unverzüglich aussprechen (je Trafostationsbereich; vermaschte Netze zeitgleich); bei fehlender Eignung schrittweise Ertüchtigung, danach unverzügliche Freigabe. | Pflicht |
| NULL-R7 | § 3 Abs. 4 (S. 2) | Umstellungsmaßnahmen (Abs. 2 und 3) bis spätestens 31. Dezember 2008 abzuschließen. | Pflicht |
| NULL-R8 | § 3 Abs. 5–7 (S. 2–3) | EVU-Pflichten: Liste je Trafostationsbereich (freigegeben ja/nein) bis 1.1.1999, Meldeschema an BMwA, Fortschrittsmeldungen jeweils 1. Juli 2000/2002/2004/2006/2008, laufende Aktualisierung; kostenlose verbindliche Auskünfte an Anfragesteller. | Pflicht |
| NULL-R9 | § 4 Abs. 1 (S. 3) | Freigabekriterium: Erfüllung der Nullungsbedingungen gemäß den mittels jeweils gültiger ETV verbindlich erklärten SNT-Vorschriften im Normalschaltzustand des Netzes. | Verweis-auf-Norm |
| NULL-R10 | § 4 Abs. 2 (S. 3) | Kann die Ausschaltbedingung in Netzteilen noch nicht eingehalten werden, ist Freigabe mit Ausnahme dieser Netzteile zulässig; Nachrüstung bis Ende der Übergangsperiode, falls technisch möglich und wirtschaftlich vertretbar. | Pflicht |
| NULL-R11 | § 5 Abs. 1–2 (S. 3) | Blanke NS-Freileitungen mit obenliegendem N-Leiter gelten als „bestehende Freileitungsnetze" i.S. ÖVE-EN 1, Teil 1/1989, § 10.3.3.6; die 2. Nullungsbedingung (§ 10.3.2) kann durch Erdungsanlagen im EVU-Netz oder Nullungsverbindung in mindestens einer § 6-konformen Verbraucheranlage erfüllt werden. | Verweis-auf-Norm |
| NULL-R12 | § 6 Abs. 1 (S. 3) | Neue Verbraucheranlagen: a) Netz freigegeben → Nullung realisieren (Abs. 3–5 sinngemäß); b) Netz nicht freigegeben → Anlage so ausführen, dass Umstellung mit minimalen Kosten möglich ist; Nullungsverbindung vorbereiten, aber bis zur Freigabe nicht anschließen. | Pflicht |
| NULL-R13 | § 6 Abs. 2 (S. 3) | Wesentliche Änderungen/Erweiterungen an den Hauptleitungen einer noch nicht genullten Anlage → Nullung in der gesamten Verbraucheranlage realisieren bzw. vorbereiten. | Pflicht |
| NULL-R14 | § 6 Abs. 3–4 (S. 3–4) | Hauptpotentialausgleich gemäß geltenden SNT-Vorschriften muss vorhanden sein (ggf. nachrüsten) und mit einer Erdungsanlage angemessener Erderwirkung verbunden sein; Mindest-Nachrüstung: Horizontalerder ≥ 10 m oder Vertikalerder ≥ 4,5 m oder gleichwertige Kombination, korrosionsbeständig; Ausnahme mobile Anlagen (ÖVE-EN 1, Teil 4/1988 § 53.3 bzw. Teil 4/1990 § 97). | Pflicht |
| NULL-R15 | § 6 Abs. 5 (S. 4) | PEN-/PE-Leiter-Querschnitte nach geltenden SNT-Vorschriften (ggf. nach-/umrüsten); zusätzlich: a) Wasserverbrauchsleitungen als Schutzleiter sind vollständig durch Schutzleiter gemäß ÖVE-EN 1, Teil 1/1989, § 21.3 zu ersetzen; b) Schutzleiter generell nach Tabelle 21-2 Spalten 1–3 (nicht 4/5) dimensionieren. | Pflicht |
| NULL-R16 | § 6 Abs. 5 lit. a (S. 4) | Wasserverbrauchsleitungen dürfen nicht (weiter) als Schutzleiter dienen. | Verbot |
| NULL-R17 | § 6 Abs. 6 (S. 4) | Bisherige N-Leiter ≥ 10 mm² Cu oder ≥ 16 mm² Al dürfen als PEN-Leiter weiterverwendet werden; dauerhafte grün/gelbe Endenkennzeichnung genügt. | Info |
| NULL-R18 | § 6 Abs. 8 (S. 4) | Nullungsverbindung gemäß § 2 Abs. 3 herstellen; es gilt ÖVE-EN 1, Teil 1/1989, § 21; Bemessung als Schutzleiter nach § 21.3.1, Tab. 21-2 Spalten 1–3; ausnahmsweise darf der neu als PEN gekennzeichnete Leiter an der Neutralleiter-Klemme verbunden bleiben (entgegen § 21.4.2 zweiter Satz). | Pflicht |
| NULL-R19 | § 6 Abs. 9 (S. 4) | Die Umstellung auf Nullung ist keine „wesentliche Änderung" i.S. § 1 Abs. 3 ETG 1992. | Definition |
| NULL-R20 | § 7 Abs. 1 (S. 4) | Landwirtschaftliche Anlagen mit Nutztierhaltung: Umstellung nur zulässig, wenn Hauptpotentialausgleich vorhanden ist, in den Aufstallungen, Entmistungsanlagen, metallene Wasserleitungen etc. einbezogen sind. | Pflicht |
| NULL-R21 | § 7 Abs. 2–3 (S. 4–5) | Im Einflussbereich elektrischer Bahnen oder von HS-Erdungsanlagen mit starrer Sternpunkterdung: Zulässigkeit/Möglichkeit der Nullung mit den Betreibern klären; ggf. Ersatzmaßnahmen oder Absehen von § 3; bei neuen Netzen Anwendbarkeit prüfen. | Pflicht |
| NULL-R22 | Anlage (S. 5) | Prinzipschaltbilder: mehrere Möglichkeiten für Anordnung/Dimensionierung der Nullungsverbindung; Querschnitt gemäß § 6 Abs. 8; Anschluss des PEN an PE bzw. Hauptpotentialausgleich beispielhaft dargestellt. | Info |

## Detail-Digest

Die Nullungsverordnung (BGBl. II Nr. 322/1998, auf Grundlage § 3 Abs. 3 und § 4 Abs. 2 ETG 1992 sowie § 205 Berggesetz 1975) verpflichtete Österreichs EVU, ihre öffentlichen 400/230-V-Verteilungsnetze bis Ende 2008 flächendeckend für die Schutzmaßnahme **Nullung (TN-System)** zu ertüchtigen und freizugeben (§ 3), und legt fest, wie Verbraucheranlagen dafür auszuführen sind (§ 6): Neuanlagen an freigegebenen Netzen sind zu nullen; an noch nicht freigegebenen Netzen ist die Nullung kostenminimal vorzubereiten (Verbindung vorbereitet, aber nicht angeschlossen). Kernbausteine der Ausführung: Hauptpotentialausgleich + Erdungsanlage (Mindesterder 10 m horizontal / 4,5 m vertikal), normgerechte PEN-/PE-Querschnitte (Tab. 21-2 Sp. 1–3 der ÖVE-EN 1 Teil 1/1989), Verbot der Wasserleitung als Schutzleiter, definierte Nullungsverbindung im ersten geeigneten Verteiler. Sonderfälle: Landwirtschaft mit Nutztieren (§ 7 Abs. 1), Bahn-/HS-Einflussbereiche (§ 7 Abs. 2–3). Die technische Referenz ist durchgehend die ÖVE-EN 1, Teil 1/1989 (§§ 3.6.14, 10.3.2, 10.3.3.6, 21) — heute historisch, funktional abgelöst durch die E-8001- bzw. OVE-E-8101-Welt; die Verordnung selbst ist laut RIS-Stand 22.04.2024 weiterhin geltendes Recht.

## Offene Punkte / Extraktionslücken

- [Extraktionslücke] Die Prinzipschaltbilder der Anlage (S. 5) sind im Textextrakt nicht enthalten (nur Bild im PDF).
- Die verwiesene ÖVE-EN 1, Teil 1/1989 (Tab. 21-2 etc.) liegt nicht als Quelle vor; konkrete Querschnittswerte sind hier nicht wiedergegeben.
- Keine unmittelbare Notbeleuchtungs-Regel enthalten; Aufnahme ins Regelwerk der Engine allenfalls als Kontext-Info (Netzform TN als Default).
