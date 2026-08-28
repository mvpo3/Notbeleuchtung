# Standesregeln Elektrotechnik — Verordnung des Bundesministers für Wirtschaft, Familie und Jugend über Standesregeln für das Gewerbe der Elektrotechnik

**Quelle:** knowledge/RIS - Standesregeln für das Gewerbe der Elektrotechnik - Bundesrecht konsolidiert, Fassung vom 22.04.2024 (1).pdf (RIS, 3 S.; StF BGBl. II Nr. 12/2014, auf Grund § 69 Abs. 2 GewO 1994) · **Extrahiert:** 2026-08-28, Volltext via pypdf

## Relevanz für die Engine

Berufsrecht, keine Planungs-/Platzierungsnorm — **keine direkten Regeln für die Engine-Logik**, aber Rahmen für den Anwender (Elektrotechnik-Gewerbetreibende, § 94 Z 16 GewO 1994), der die generierten Pläne ausführt bzw. verantwortet:

1. **Normbindung als Standespflicht:** § 4 Z 8 macht die Einhaltung von ETG, ETV (SNT-Bestimmungen), Elektroschutzverordnung, der **OVE- und ÖNORM-Regeln der Technik** und der Werkvertragsnormen der Haustechnik zur Standespflicht — ein von der Engine erzeugter Plan, der OVE/ÖNORM verletzt, würde den ausführenden Gewerbetreibenden standesrechtlich exponieren. Das stützt die Architektur-Regel „OVE-Verbote = Hard Stop".
2. **Regeln der Technik + aktuelles Fachwissen** (§ 2, § 6 Z 3): Tätigkeit ist nach den anerkannten Regeln der Technik auszuüben, Fachwissen aktuell zu halten — Argument dafür, dass die Engine stets auf die aktuelle Normfassung referenziert (Audit-Trail `norm_quelle`).
3. **Leistungsbeschreibungen** werden im Anhang Z 4 ausdrücklich als im Unternehmen verfügbar zu haltende Unterlagen genannt — passt zum LB-Input-Konzept der Engine (LB als verbindliches Projektdokument).
4. **Planer-Haftung:** § 5 Z 3 — grob mangelhafte Ausschreibungsunterlagen (vorsätzlich/grob fahrlässig als Planer erstellt) sind standeswidrig; ein Qualitätsargument für normkonforme, auditierbare Engine-Outputs.

## Kernaussagen-Tabelle

| ID | §/Abschnitt (Seite) | Aussage | Typ |
|----|---------------------|---------|-----|
| STAND-R1 | § 1 (S. 1) | Anwendungsbereich: Gewerbetreibende des Elektrotechnik-Gewerbes (§ 94 Z 16 GewO 1994) in vollem oder eingeschränktem Umfang sowie Teilgewerbe aus dem Elektrotechniker-Gewerbe. | Definition |
| STAND-R2 | § 2 (S. 1) | Tätigkeit ist gewissenhaft, mit der Sorgfalt eines ordentlichen Unternehmers und **nach den anerkannten Regeln der Technik** auszuüben; standeswidriges Verhalten ist zu unterlassen. | Pflicht |
| STAND-R3 | § 3 (S. 1) | Standeswidrig ist jedes Verhalten (gegenüber Auftraggebern, Berufsangehörigen oder sonst), das das Ansehen des Berufsstandes beeinträchtigt oder gemeinsame Interessen schädigt. | Definition |
| STAND-R4 | § 4 Z 1–4 (S. 1) | Standeswidrig gegenüber Auftraggebern: absichtlich unrichtige/irreführende Angaben über eigene Leistungsfähigkeit; Preisabsprachen mit anderen Bietern; täuschende Angebote (Preis-Leistungs-Verhältnis); grobe Benachteiligung bzw. grob einseitige Risikoüberwälzung auf den Auftraggeber. | Verbot |
| STAND-R5 | § 4 Z 5–7 (S. 1–2) | Standeswidrig: ungeeigneten Geschäftsführer namhaft machen (§ 39 GewO); vertragliche Verschwiegenheitspflicht verletzen; Sachverständigen-Befund/Gutachten nicht nach bestem Wissen, unparteilich und nach den Regeln der Technik erstellen. | Verbot |
| STAND-R6 | § 4 Z 8 (S. 2) | Standeswidrig: Nichteinhaltung der gesetzlichen Bestimmungen, insbesondere ArbeitnehmerInnenschutzgesetz, **Elektrotechnikgesetz, Elektrotechnikverordnung (SNT-Bestimmungen), Elektroschutzverordnung, der durch OVE und ÖNORM veröffentlichten Regeln der Technik** oder der einschlägigen Werkvertragsnormen der Haustechnik. | Verbot |
| STAND-R7 | § 4 Z 9–10 (S. 2) | Standeswidrig: >2 Jahre Säumnis bei Umlagen/Beiträgen an Körperschaften öffentlichen Rechts; Verstöße gegen Lohn-/Sozialdumping-, kollektivvertragliche und arbeitsrechtliche Vorschriften. | Verbot |
| STAND-R8 | § 5 Z 1–4 (S. 2) | Standeswidrig gegenüber Berufskollegen: Scheinselbstständigen-Beschäftigung; unsachliche Herabsetzung anderer; als Planer/Generalunternehmer vorsätzlich oder grob fahrlässig grob mangelhafte Ausschreibungsunterlagen zu Lasten des Auftragnehmers erstellen; Leistungen unter Selbstkosten ohne sachliche Rechtfertigung. | Verbot |
| STAND-R9 | § 6 Z 1–2 (S. 2) | Pflichten: eingeschränkten Gewerbeumfang im Geschäftsverkehr anführen; Verschwiegenheit über berufsbekannt gewordene Tatsachen (auch Arbeitnehmer zu verpflichten; gilt nicht gegenüber Gerichten und Verwaltungsbehörden). | Pflicht |
| STAND-R10 | § 6 Z 3 (S. 2) | Fachwissen (eigenes und der Mitarbeiter) stets auf dem neuesten Stand halten und Berufsausübung danach ausrichten. | Pflicht |
| STAND-R11 | § 6 Z 4 + Anhang (S. 2–3) | Mindeststandard an Ausrüstung vorzuweisen (Anhang): Sicherheitswerkzeugkoffer, ÖVE-geprüfte Maschinen/Geräte, Messgeräte (Schutzmaßnahmenprüfgerät, Vielfachmessgerät, Spannungs-/Durchgangsprüfer, jeweils Stand der Technik), Schutzbekleidung für Arbeiten unter Spannung. | Pflicht |
| STAND-R12 | Anhang Z 4 (S. 3) | Im Unternehmen verfügbar zu halten: aktuelle elektrotechnische Sicherheitsvorschriften (ÖVE-Vorschriften, Technische Anschlussbedingungen), sonstige Schutzvorschriften, **Leistungsbeschreibungen**. | Pflicht |
| STAND-R13 | § 7 (S. 2) | Inkrafttreten mit dem der Kundmachung folgenden Monatsersten. | Info |

## Detail-Digest

Die Verordnung (BGBl. II Nr. 12/2014) konkretisiert das standesgemäße Verhalten des Elektrotechnik-Gewerbes: Generalklausel Sorgfalt + anerkannte Regeln der Technik (§ 2), Definition der Standeswidrigkeit (§ 3), Kataloge standeswidrigen Verhaltens gegenüber Auftraggebern (§ 4: Täuschung, Preisabsprachen, Risikoüberwälzung, Rechtsverstöße — darunter ausdrücklich ETG/ETV/OVE/ÖNORM) und gegenüber Berufsangehörigen (§ 5: Scheinselbstständigkeit, Herabsetzung, grob mangelhafte Ausschreibungen, Dumping unter Selbstkosten), sowie positive Berufspflichten (§ 6: Umfangs-Transparenz, Verschwiegenheit, Fortbildung, Mindestausrüstung). Der Anhang listet die Mindestausrüstung (Werkzeug, Maschinen, Messgeräte, verfügbar zu haltende Vorschriften inkl. Leistungsbeschreibungen, Schutzbekleidung).

**Relevanz fürs Gewerbe:** Wer Notbeleuchtungsanlagen plant/errichtet, ist standesrechtlich an ETG, ETV und die OVE/ÖNORM-Regeln der Technik gebunden (§ 4 Z 8) — Verstöße sind nicht nur technisch, sondern berufsrechtlich sanktionierbar (Verwaltungsverfahren nach GewO). Für Planer gilt zusätzlich das Verbot grob mangelhafter Ausschreibungsunterlagen (§ 5 Z 3).

## Offene Punkte / Extraktionslücken

- Keine inhaltlichen Extraktionslücken; der 3-seitige Text ist vollständig erfasst.
- Die Verordnung nennt die „Elektroschutzverordnung" (§ 4 Z 8) — deren Inhalt (ESV 2012, liegt als knowledge/ESV_2012 (1).pdf vor) ist hier nicht ausgewertet.
- Sanktionsmechanik (Verfahren nach § 69 GewO 1994 / § 367 ff GewO) ist nicht Teil des Verordnungstexts.
