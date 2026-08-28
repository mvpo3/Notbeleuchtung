# OVE-Fachinformationen E-05 / E-06 / E-07 — Sicherheitsbeleuchtung (AT)
**Quelle:** elektro-planer knowledge/normen/Fachinfo_E-0{5,6,7}...txt · **Übernommen:** 2026-08-28
**Einordnung:** OVE-Fachinformationen (Interpretationen zu OVE E 8101 / ÖVE E 8002), AT. Referenz-Praxis mit hoher Autorität (OVE-Fachausschuss). Alle drei Ausgabe 2021-01-01, Aktualitätsprüfung 2020-12, zuständig OVE/TSK E04 Sonderanlagen (E-05: OVE/TK E „Elektrische Niederspannungsanlagen"). Jeweils nur gemeinsam mit der Bezugsnorm anwendbar (E-05: ÖVE-EN 1 Teil 4 § 90:1991; E-06/E-07: ÖVE/ÖNORM E 8002-1).

## E-07 — Funktionserhalt Leitungsanlagen der Sicherheitsbeleuchtung
Bezugsnorm: **ÖVE/ÖNORM E 8002-1:2002, Abschnitt 5.4 (1)** — Leitungsanlagen von Sicherheitsbeleuchtungen müssen einen **Funktionserhalt von mindestens 30 Minuten** haben. **Ausgenommen** sind Teile der Endstromkreise, deren Ausfall **zu keiner Beeinträchtigung anderer (nachgelagerter) Bereiche** führt (S.1). Die Fachinformation klärt den Interpretationsspielraum: Sind „nachgelagerte Bereiche" gleich Brandabschnitte? Was heißt „Beeinträchtigung im Brandfall"?

**Schutzziel (§1, S.1):** Bei einem **lokalen Brand** darf es zu **keiner Beeinträchtigung** der Sicherheitsbeleuchtung in **Rettungs-/Fluchtwegen anderer Brandabschnitte** kommen.

**Verzicht auf Funktionserhalt in Unterbrandabschnitten** (im Sinne der **TRVB B 108**, ausgenommen **Fluchtstiegenhäuser**) des betrachteten Brandabschnitts ist zulässig, **wenn beide** Bedingungen erfüllt sind (§1, S.1):
1. je Unterbrandabschnitt **nicht mehr als zwei Sicherheitsleuchten** (mit oder ohne Piktogramm) vorhanden sind, **und**
2. **keine** Sicherheitsleuchten der Rettungswege unzulässig beeinträchtigt werden — gilt als erfüllt, wenn **ca. 50 %** der Sicherheitsbeleuchtung in den Rettungswegen funktionsfähig bleibt (z. B. durch **alternierende Stromkreisaufteilung**).

**Brandabschnitte bis zu 1600 m² (§2.1, S.1–3):**
- Leitungen, die **Brandabschnitte queren**, brauchen **jedenfalls 30 min Funktionserhalt**.
- **Innerhalb** eines Brandabschnitts kann für die entsprechenden Endstromkreis-Teile auf den Funktionserhalt **verzichtet** werden.
- Für Brandabschnitte **über 1600 m²** sind weiter gehende Überlegungen anzustellen (Einleitung, S.1).
- Alternative zur alternierenden Stromkreisaufteilung: **E 30-Dosen mit Abzweigsicherungen** (Bild 1). Dabei gilt (S.2–3):
  - Der **Endstromkreis beginnt im Haupt-/Unterverteiler**, nicht in den E 30-Dosen.
  - Die Abzweigsicherungen dienen **nicht dem Leitungsschutz**, sondern nur dem **Kurzschlussschutz im Brandfall**; sie müssen **zeitselektiv** zur Stromkreissicherung im Haupt-/Unterverteiler sein.
  - Ausführung **einpolig** in der Phasenleitung (AC-Betrieb; bzw. **+** im DC-Betrieb) **oder zweipolig**.
  - Einbauort (z. B. Zwischendeckenbereich) und Dosen **dauerhaft und sichtbar kennzeichnen**, in Dokumentation eintragen, **leichte Zugänglichkeit** gewährleisten.
  - Festhaltung ÖVE-FUA-E04: „Schalter/Schaltelement" nach E 8002-1:2002 **§7.7.14** = nur **manuell** schaltbare Einrichtungen; Überstrom-/Kurzschlussschutz (z. B. einmal auslösende Sicherungen) sind **keine** Schalteinrichtungen i. S. d. §7.7.14.

**Bauliche Vorkehrungen (§2.3, S.4–5):** Bei einem als **eigener Brandabschnitt** ausgebildeten Stiegenhaus siehe Bilder 5/6. **Fußnote zu Bild 5:** Bei Verlegung in einem **eigenen Steigschacht (F 30)** darf die Leitungsanlage **ohne Funktionserhalt („E 0")** ausgeführt werden, wenn sichergestellt ist, dass durch allfällige Einbauten keine Beeinträchtigung der Sicherheitsbeleuchtung eintreten kann.

## E-06 — Sicherheitsbeleuchtung mit kombinierten Bussystemen
**Definition (§1, S.1):** Kombinierte Bussysteme gemäß **ÖVE/ÖNORM E 8002-1:2007, Abschnitt 7.8.3** = Bussysteme, die **nicht ausschließlich** die Sicherheitsbeleuchtung steuern/überwachen, sondern über denselben Bus auch andere Gebäudetechnik (z. B. Allgemeinbeleuchtung). Risiko: Im Fehlerfall wird das **Schutzziel gemäß E 8002-1:2007 Abschnitt 4.1.1** verfehlt. **Grundsatz-Empfehlung: Für die Sicherheitsbeleuchtung ist ein getrenntes Bussystem zu bevorzugen.**

**Planung/Errichtung/Dokumentation (§2.1, S.1–2):**
- **2.1.1** Vor Ausführung schriftliche Hersteller-Bestätigung: Einhaltung der **Umschaltzeit max. 0,5 s** bei voller Bestückung mit allen Buskomponenten (z. B. EVG) + **Kompatibilität Bus–EVG–Leuchte**.
- **2.1.2** Schriftliche Hersteller-Bestätigung: bei Störungen (Kurzschluss, Brand an Leitungsanlage/Buscontroller) **keine Rückwirkungen** auf die Sicherheitsbeleuchtung.
- **2.1.3–2.1.6** Bestückung + spätere Parameteränderungen dokumentieren; Änderungen von Betriebszuständen nur **willentlich** (Passwort/befugte Personen); jede in die Allgemeinbeleuchtung integrierte Sicherheitsleuchte **kennzeichnen** (Programmierungsart, Adresse, Dimmwerte); alle Prüf-Schalteinrichtungen kennzeichnen und dokumentieren.

**Erst- und Wiederholungsprüfung (§2.2/§2.3, S.2):** Funktionsprüfung bei **ausgeschalteter Bussteuerung** (Netztrennung) und bei **simulierter Bus-Störung** (Kurzschluss/Unterbrechung Busleitung, Ausfall Steuerung). Sicherstellen, dass bei **aktivierter Sicherheitsbeleuchtung** die Buskomponenten/EVGs **weder im AC- noch DC-Betrieb geschaltet oder gedimmt** werden können. Vollständigkeit/Aktualität der Dokumentation prüfen. Führt der Errichter die Erstprüfung nicht selbst durch, ist eine **befugte Fachkraft** (akkreditierte Prüfstelle, Ziviltechniker für Elektrotechnik) heranzuziehen.

## E-05 — Sicherheitsbeleuchtung/Niederspannung in Garagen
Interpretation des Fachausschusses EN zu **§ 90 der ÖVE-EN 1 Teil 4** (Erstveröffentlichung e&i 1991). **Anlass:** Vorwurf, § 90.1 „Garagen sind brandgefährdete Räume" widerspreche den meisten Landesbauordnungen, die Garagen i. d. R. **nicht** als brandgefährdete Räume einstufen (S.1).

**Kernaussage:** Der Widerspruch besteht **nur scheinbar**. Elektrotechnische Raum-/Bereichsklassifikationen gelten **immer nur innerhalb ihres eigenen Geltungsbereichs** — auch bei wort-/sinngleichen Begriffen anderer Normen. § 90.1 ist daher zu lesen als „**Garagen sind brandgefährdete Räume im Sinne dieser Bestimmungen**". Absicht war nur, **Starkstromanlagen bis AC 1000 V / DC 1500 V** in Garagen den Installationsbestimmungen für brandgefährdete Räume nach **§ 50 ÖVE-EN 1 Teil 4** zu unterwerfen (S.1).

*Relevanz für Notbeleuchtung:* E-05 betrifft Niederspannungs-Installation/Brandschutzeinstufung von Garagen, nicht direkt die Sicherheitsleuchten-Platzierung; liefert aber die AT-Einstufung „Garage = brandgefährdeter Raum (elektrotechnisch)", die für Leitungsführung/Funktionserhalt in Garagen mitzudenken ist.

## Regel-Tabelle
| ID | Fachinfo §/Seite | Regel | Werte | Typ |
|----|------------------|-------|-------|-----|
| E07-R1 | E-07 §5.4(1) E 8002-1 / S.1 | Leitungsanlagen der Sicherheitsbeleuchtung brauchen Funktionserhalt | ≥ 30 min | FRIST |
| E07-R2 | E-07 §5.4(1) / S.1 | Ausgenommen: Endstromkreis-Teile ohne Beeinträchtigung anderer (nachgelagerter) Bereiche | — | AUSNAHME |
| E07-R3 | E-07 §1 / S.1 | Bei lokalem Brand keine Beeinträchtigung der Sicherheitsbeleuchtung in Rettungswegen anderer Brandabschnitte | — | SCHUTZZIEL |
| E07-R4 | E-07 §1 / S.1 | Verzicht auf Funktionserhalt in Unterbrandabschnitten (TRVB B 108, außer Fluchtstiegenhäuser): max. 2 Sicherheitsleuchten je Unterbrandabschnitt UND Rettungswege nicht beeinträchtigt | ≤ 2 Leuchten | PFLICHT |
| E07-R5 | E-07 §1 / S.1 | „Rettungswege nicht beeinträchtigt" erfüllt, wenn Restfunktion in Rettungswegen erhalten (z. B. alternierende Stromkreisaufteilung) | ca. 50 % | DEFINITION |
| E07-R6 | E-07 Einl./§2.1 / S.1 | Schwelle „großer" Brandabschnitt: Beispiele §2.1 gelten bis 1600 m²; darüber weiter gehende Überlegungen | 1600 m² | ABSTAND/SCHWELLE |
| E07-R7 | E-07 §2.1 / S.1 | Leitungen, die Brandabschnitte queren, brauchen Funktionserhalt; innerhalb kann verzichtet werden | 30 min | FRIST |
| E07-R8 | E-07 §2.1 / S.2 | Bei E 30-Dosen mit Abzweigsicherungen beginnt der Endstromkreis im Haupt-/Unterverteiler, nicht in den Dosen | — | STROMKREIS |
| E07-R9 | E-07 §2.1 / S.2 | Abzweigsicherungen in E 30-Dosen = nur Kurzschlussschutz im Brandfall, kein Leitungsschutz; zeitselektiv zur Verteilersicherung | — | SCHUTZ |
| E07-R10 | E-07 §2.1 / S.3 | Ausführung der Abzweigsicherungen: einpolig in Phase (AC; + bei DC) oder zweipolig | 1- oder 2-polig | STROMKREIS |
| E07-R11 | E-07 §2.1 / S.2–3 | E 30-Dosen: Einbauort und Dosen dauerhaft/sichtbar kennzeichnen, dokumentieren, leicht zugänglich | — | PFLICHT |
| E07-R12 | E-07 §2.1 (FUA-E04) / S.3 | „Schalter/Schaltelement" nach E 8002-1 §7.7.14 = nur manuell schaltbar; Sicherungen sind keine Schalteinrichtungen | — | DEFINITION |
| E07-R13 | E-07 §2.3 (Fußn. Bild 5) / S.4 | Eigener Steigschacht F 30 → Leitung ohne Funktionserhalt („E 0") zulässig, wenn keine Beeinträchtigung durch Einbauten | E 0 / F 30 | AUSNAHME |
| E06-R1 | E-06 §7.8.3 E 8002-1:2007 / S.1 | Kombiniertes Bussystem = Bus steuert/überwacht nicht nur Sicherheitsbeleuchtung, sondern auch andere Gebäudetechnik | — | DEFINITION |
| E06-R2 | E-06 §1 / S.1 | Für Sicherheitsbeleuchtung getrenntes Bussystem bevorzugen | — | EMPFEHLUNG |
| E06-R3 | E-06 §2.1.1 / S.1 | Umschaltzeit bei voller Buskomponenten-Bestückung, schriftlich vom Hersteller bestätigt | max. 0,5 s | FRIST |
| E06-R4 | E-06 §2.1.1 / S.1 | Schriftliche Hersteller-Bestätigung Kompatibilität Bus–EVG–Leuchte | — | PFLICHT |
| E06-R5 | E-06 §2.1.2 / S.1 | Schriftliche Hersteller-Bestätigung: Störungen (Kurzschluss, Brand an Leitung/Buscontroller) ohne Rückwirkung auf Sicherheitsbeleuchtung | — | PFLICHT |
| E06-R6 | E-06 §2.1.3–2.1.6 / S.1–2 | Bestückung/Parameteränderungen, integrierte Leuchten, Prüf-Schalteinrichtungen kennzeichnen und dokumentieren; Änderungen nur willentlich | — | PFLICHT |
| E06-R7 | E-06 §2.2.3 / §2.3.3 / S.2 | Bei aktivierter Sicherheitsbeleuchtung dürfen Buskomponenten/EVGs weder im AC- noch DC-Betrieb geschaltet/gedimmt werden | — | PFLICHT |
| E06-R8 | E-06 §2.2 / §2.3 / S.2 | Erst- und Wiederholungsprüfung: Funktion bei ausgeschalteter Bussteuerung und bei simulierter Bus-Störung nachweisen | — | PRÜFUNG |
| E06-R9 | E-06 §2.2.5 / S.2 | Erstprüfung ggf. durch befugte Fachkraft (akkreditierte Prüfstelle, Ziviltechniker) | — | PFLICHT |
| E05-R1 | E-05 §90.1 ÖVE-EN 1 Teil 4 / S.1 | Garagen = brandgefährdete Räume „im Sinne dieser Bestimmungen" (elektrotechnisch), unabhängig von Landesbauordnung | — | DEFINITION |
| E05-R2 | E-05 §50/§90 ÖVE-EN 1 Teil 4 / S.1 | Starkstromanlagen in Garagen den Installationsbestimmungen für brandgefährdete Räume nach § 50 unterwerfen | — | PFLICHT |
| E05-R3 | E-05 §90 ÖVE-EN 1 Teil 4 / S.1 | Geltungsbereich Nennspannung | ≤ AC 1000 V / DC 1500 V | DEFINITION |
| E05-R4 | E-05 / S.1 | Elektrotechnische Raum-/Bereichsklassifikationen gelten nur im eigenen Geltungsbereich | — | DEFINITION |

## Offene Punkte / Extraktionslücken
- **Bilder 1–6 (E-07)** sind Grafiken (Ausführungsvarianten, Symbollegende) und im Textextrakt **nicht** enthalten — die konkrete Leitungsführung/Stromkreis-Topologie ist nur verbal beschrieben.
- **E-07 §2.2 (Unterbrandabschnitte):** Der erläuternde Text zu den Bildern 2–4 fehlt weitgehend; nur die Bildüberschriften sind extrahiert.
- **E-07:** Aussage „über 1600 m² weiter gehende Überlegungen" ist genannt, aber **nicht ausgeführt** (was konkret zu tun ist, steht nicht im Text).
- **E-05:** § 50 und § 90 ÖVE-EN 1 Teil 4 werden referenziert, aber deren Inhalt (konkrete Installationsanforderungen für brandgefährdete Räume) ist nicht Teil dieser Fachinformation.
- Alle drei Fachinfos sind **nur gemeinsam mit der jeweiligen Bezugsnorm** anwendbar; die Bezugsnormen selbst liegen hier nicht als Digest vor.
