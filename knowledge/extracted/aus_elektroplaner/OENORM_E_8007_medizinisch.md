# ÖVE/ÖNORM E 8007 (2007) — Sicherheitsstromversorgung in Krankenhäusern/medizinischen Räumen
**Quelle:** elektro-planer knowledge/normen/OEVE_OENORM_E_8007*.txt, via Teil-Digests · **Übernommen:** 2026-08-28
**Einordnung:** AT-Norm, Basis für OVE E 8101 Teil 7-710. Relevant für medizinische Gebäudetypen der Engine.

Hinweis zur Nummerierung: Die Regel-Tabelle folgt der konsolidierten Fassung **E 8007:2007** (Digest part0/part1).
Die Änderungen A1:2001 / A2:2002 amendieren noch die alte ÖVE-EN-7-Nummerierung (dort Abschn. 5.x statt 6.x);
inhaltlich gleiche Regeln sind zusammengeführt, abweichende/ergänzende A1-A2-Werte in Klammern vermerkt.

## Relevanz für die Engine
- E 8007 ist die **medizinisch-spezifische Ergänzung** zu E 8001 / E 8002-1. Für medizinische Gebäudetypen
  (Krankenhaus, Ambulatorium, Praxis, Pflegeheim/Kuranstalt) übersteuert bzw. verschärft sie die allgemeine
  Notbeleuchtungs-/SV-Logik. Sie definiert **welche Räume in welche Anwendungsgruppe** (AG 0/1/2) fallen und
  daraus **welche Umschaltzeit + Betriebsdauer** die Sicherheits-/Ersatzbeleuchtung und die (zusätzliche)
  Sicherheitsstromversorgung haben muss.
- Kern-Achsen für die Platzierungs-/Norm-Logik: **AG des Raums** → **Umschaltzeit-Klasse** (0,5 s / 15 s / >15 s)
  → **Betriebsdauer** (24 h / 3 h bzw. 3 h / 1 h für ZSV) → **Anteil der aus SV zu speisenden Raumbeleuchtung**.
- Rettungswege/Rettungszeichen selbst verweisen zusätzlich auf **EN 1838** (Lux, Erkennungsweite) und
  **E 8002-1** (Sicherheitsbeleuchtungs-Technik). E 8007 setzt darüber die **KH-spezifischen Betriebsdauern**
  (8 h für Treppen-Rettungswege/Rettungszeichen aus A1/A2; 24 h Gesamt-SV) und Zusatzräume.
- Für die Engine relevant als **Gebäudetyp-Weiche**: Ist das Objekt medizinisch → E 8007-Regeln aktiv
  (AG-Zuordnung Tabelle 1, OP/Intensiv → ZSV 0,5 s/15 s), sonst nur E 8002-Reihe.

## Regel-Tabelle (Sicherheitsbeleuchtung/-stromversorgung medizinisch)
| ID | §/Anhang (Seite) | Regel | Werte (SV-Klasse/Zeit/Dauer) | Typ |
|----|------------------|-------|------------------------------|-----|
| E8007-R1 | §3.4.6 (S.~14) | Umschaltzeit = Zeit AV-Störung → Wirksamwerden SV | Definition | Begriff |
| E8007-R2 | §3.4.7 (S.14) | Störung AV: Spannung > 0,5 s < 90 % Nennspannung; für Sicherheitsbeleuchtung (E 8002-1) > 0,5 s < 75 % | 0,5 s / 90 % (bzw. 75 %) | Auslösekriterium |
| E8007-R3 | §6.1 (S.~ SV) | SV grundsätzlich erforderlich; Betriebsdauer aus ≥1 Sicherheitsstromquelle | ≥ 24 h | Dauer |
| E8007-R4 | §6.1 / AC1 §5.1 | Reduktion Betriebsdauer, wenn gefahrlose Beendigung + geordnetes Verlassen in 3 h möglich (z. B. phys. Therapie, Röntgeninstitute) | ≥ 3 h (statt 24 h) | Dauer-Ausnahme |
| E8007-R5 | §6.2 (S.~) | SV-Klasse „Sicherheits-/Ersatzbeleuchtung + NSE": Umschaltzeit | 0 s … 15 s | SV-Klasse |
| E8007-R6 | §6.2.1.1 | Sicherheitsbeleuchtung (nach E 8002-1) für: Rettungswege; Rettungszeichen(-hinterleuchtung); Arbeitsplätze bes. Gefährdung; Räume SV-Aggregate/HV-SV/Schaltanlagen > 1 kV | Umschaltzeit ≤ 15 s | Beleuchtung |
| E8007-R7 | §6.2.1.1 | Ab **50 Sicherheitsleuchten** automatische Prüfeinrichtung (E 8002-1:2007 7.4.3.8); sonst empfohlen | ≥ 50 Leuchten → Auto-Test | Prüfung |
| E8007-R8 | §6.2.1.2(1) | Ersatzbeleuchtung Arbeitsräume (arbeitnehmerschutzrechtlich) | ≤ 15 s | Beleuchtung |
| E8007-R9 | §6.2.1.2(2) | AG 1: je Raum ≥ 1 Allgemeinleuchte + vorhandene Untersuchungsleuchten aus SV | ≤ 15 s | AG1-Beleuchtung |
| E8007-R10 | §6.2.1.2(3) | AG 2: Raumbeleuchtung aus SV und aus AV/ZSV; **≥ 50 %** der Raumbeleuchtung aus SV-Quelle | ≥ 50 % / ≤ 15 s | AG2-Beleuchtung |
| E8007-R10b | A1 §5.1.1(6) | (A1-Variante, verschärft): AG 2 — **gesamte** Raumbeleuchtung aus SV weiterbetreiben (A2 §5.1.1.2(4) relativiert wieder auf ≥ 50 %) | 100 % bzw. ≥ 50 % | AG2-Beleuchtung |
| E8007-R11 | §6.2.1.2(4) | Etagenbäder/Toiletten/Nasszellen für Patienten: SV-Beleuchtung | ≤ 15 s | Beleuchtung |
| E8007-R12 | §6.2.1.2(5) | Für KH-Betrieb notwendige Räume: je Raum ≥ 1 Leuchte aus SV | ≤ 15 s | Beleuchtung |
| E8007-R13 | §6.2.2 | NSE bis 15 s: Feuerwehr-/notw. Bettenaufzüge, RWA/Druckbelüftung, Lüftung SV-Betriebsräume, Personenruf/Telefon, Alarm/Warn, Löschwasser (außer Sprinkler) | ≤ 15 s | NSE |
| E8007-R14 | §6.2.3 | Med.-techn. Einrichtungen bis 15 s: notw. med. Geräte, el. Einrichtungen med. Gasversorgung (Druckluft, Vakuum, Narkosegasabsaugung) + Überwachung | ≤ 15 s | Med.-techn. |
| E8007-R15 | §6.3 | SV ohne festgelegte Umschaltzeit (nach 6.2 gesichert): Sterilisation, Haustechnik, Kühlung, Kochen, Akku-Ladung, Aufzüge | > 15 s | SV-Klasse |
| E8007-R16 | §6.4.1 | ZSV bis 15 s: lebenswichtige/chirurg. Geräte AG 2 innerhalb 15 s aus ZSV | ≤ 15 s / ≥ 3 h (≥ 1 h wenn weitere unabh. Quelle 3 h sichert) | ZSV |
| E8007-R17 | §6.4.1 | Frühgeborenen-Stationen/akut gefährdete Patienten: Beatmungs-/Überwachungsgeräte weiterversorgen | ≤ 0,5 s | ZSV |
| E8007-R18 | §6.4.2 | ZSV bis 0,5 s: OP-Leuchten u. vergleichbare Leuchten aus SV, wenn Spannung < 90 % Nenn; Quelle | ≤ 0,5 s / 3 h (bzw. 1 h + weitere Quelle) | ZSV |
| E8007-R18b | A2 §5.3.2 | OP-Leuchte 0,5 s-Auslösung: Spannung am OP-Licht-Eingang sinkt > 10 % der Nennspannung | ≤ 0,5 s | ZSV-Auslöse |
| E8007-R19 | §6.4.2 | In Räumen mit ZSV-Geräten zusätzlich ZSV-versorgte Beleuchtung; OP-/vergleichbare Leuchten fest angeschlossen | — | ZSV-Beleuchtung |
| E8007-R20 | §6.4.5 | ZSV-Notbetrieb: Meldung hohe Priorität an Technik + akustisch (quittierbar) + optisch an med. Personal; entfällt bei Tank ≥ 12 h | ≥ 12 h Tank | Meldung |
| E8007-R21 | §6.5.3 / A1 §5.4.3, A2 §5.4.3 | SV-Bemessung: ≥ 80 % Verbraucherleistung in 15 s, restliche 20 % nach weiteren 5 s; Abw. ≤ 10 % U_N / 5 Hz | 80 %/15 s + 20 %/+5 s | Bemessung |
| E8007-R22 | §6.7.2 | Batterie-ZSV aus Erhaltungsladung: Nennleistung (cos φ ≥ 0,8 ind.) bei +20 °C | ≥ 3 h (1 h + weitere Quelle); Nachladung ≤ 6 h | Batterie-Dauer |
| E8007-R23 | §6.8 / §6.4.2 | OP-Leuchten-SV: nach Lastwechsel 100 % Nennleistung Grenzwerte in ≤ 0,5 s wieder eingehalten | ≤ 0,5 s | OP-Leuchte |
| E8007-R24 | §7.2.3.1 (S.~) | Funktionserhalt Leitungen NSE (DIN 4102-12): Sicherheitsbeleuchtung Rettungswege, Alarm/Anweisung, RWA (natürl.), Aufzüge | ≥ 30 min (E 30) | Funktionserhalt |
| E8007-R25 | §7.2.3.1 | Bei lokalem Brand ≥ 50 % Sicherheitsbeleuchtung Rettungswege funktionsfähig (alternierende Stromkreise); Fluchtstiegenhäuser 100 % | 50 % / 100 % | Funktionserhalt |
| E8007-R26 | §7.2.3.1 | Funktionserhalt ≥ 90 min (E 90): Löschwasser, Lüftung Sicherheitstreppenräume/Feuerwehraufzug, mech. RWA/Druckbelüftung, ZSV (6.4) | ≥ 90 min (E 90) | Funktionserhalt |
| E8007-R27 | §4.4.2 | Beleuchtung Rettungswege + AG-1/2-Räume mit > 1 Leuchte: auf ≥ 2 Stromkreise aufteilen; in Rettungswegen abwechselnd zugeordnet | ≥ 2 Stromkreise | Verteilung |
| E8007-R28 | §9.1.4 | Praxisräume (außerhalb KH): SV bei Störung; AG 2 aus Quelle 6.4: OP-Leuchten ≤ 0,5 s, lebenswichtige Geräte ≤ 15 s | ≥ 3 h; 0,5 s / 15 s | Praxis-SV |
| E8007-R29 | §9.3.1.1.2 (S.41) | Rettungswege **Treppen**: Dauer- oder Bereitschaftsschaltung (E 8002-1) | ≥ 8 h (bzw. 3 h + ext. Einspeisung in 3 h) | Rettungsweg-Treppe |
| E8007-R30 | §9.3.1.1.3 (S.41) | Rettungswege **außer Treppen**: Dauerschaltung oder Bereitschaftsschaltung (E 8002-5) | Umschaltzeit ≤ 15 s | Rettungsweg |
| E8007-R31 | §9.3.1.1.4 (S.41) | Rettungszeichenleuchten (EN 60598-2-22): Dauerschaltung | ≥ 8 h (3 h wenn ext. Einspeisung o. Anstrahlung nach EN 1838) | Rettungszeichen |
| E8007-R32 | A1 §5.1.1(1) (S.~5) | Rettungsweg-Mindestbeleuchtungsstärke Mittellinie, 0,2 m über Boden/Stufen | 1 lx | Lux |
| E8007-R33 | A1 §5.1.1(3) | Räume Schaltanlagen > 1 kV / Ersatzstromaggregate / HV: Mindestbeleuchtungsstärke | 10 % der Nenn-Bel., mind. 15 lx (0,2 m Höhe) | Lux |
| E8007-R34 | A1 §5.1.1(4) | Arbeitsräume > 50 m² (Werkstatt/Küche/Wäscherei/Labor): Mindestbeleuchtungsstärke | 1 lx (0,2 m Höhe) | Lux |
| E8007-R35 | §9.3.1.1.5 | Sanitärräume Heimbewohner: gefahrloses Verlassen (Sicherheitsleuchte / beleuchteter Notruftaster / Leuchtfolie) | — | Heim |
| E8007-R36 | §9.3.1.2 / A2 §5.3.2 | OP-Leuchten + lebenswichtige Geräte: ZSV nach 6.4 unabhängig von SV med.-techn. Einrichtungen (6.2.3) vorsehen | ≤ 0,5 s / ≤ 15 s | ZSV-Pflicht |
| E8007-R37 | §9.3.1.1.1 | Pflegeheim/Kuranstalt: Notbetrieb bei Netzausfall (stationäres o. organisatorisch verfügbares transportables Aggregat) für NSE (Notruf, Sicherheitsbel., Drucksteigerung, notw. med. Geräte) | — | Pflegeheim |

## SV-Klassen & Umschaltzeiten (Kern)
Drei Umschaltzeit-Klassen strukturieren die gesamte E-8007-SV-Logik (§6):

- **≤ 0,5 s (ZSV, „unterbrechungsnah")** — §6.4.2 / A2 §5.3.2: **OP-Leuchten** und vergleichbare Leuchten
  (auch Herzkatheter-, Entbindungs-Untersuchungsleuchten). Zusätzlich §6.4.1: Beatmungs-/Überwachungsgeräte
  auf Frühgeborenen-Stationen / bei akut gefährdeten Patienten. Betriebsdauer 3 h (oder 1 h + weitere
  unabhängige Quelle für 3 h). Auslösung: Spannung am OP-Licht < 90 % Nenn (> 10 % Absenkung).
- **≤ 15 s (SV + ZSV)** — §6.2 / §6.4.1: Sicherheits-/Ersatzbeleuchtung (Rettungswege, Rettungszeichen,
  AG-1/AG-2-Raumbeleuchtung, KH-Betriebsräume), NSE (Aufzüge, RWA, Personenruf, Löschwasser),
  med.-techn. Einrichtungen (Gasversorgung), **lebenswichtige/chirurgische Geräte AG 2**. Betriebsdauer:
  Sicherheitsbeleuchtung 24 h (bzw. 3 h Ausnahme); ZSV-Geräte 3 h (bzw. 1 h + weitere Quelle).
- **> 15 s (SV ohne festgelegte Umschaltzeit)** — §6.3: nachrangige Verbraucher (Sterilisation, Haustechnik,
  Kühlung, Kochen, Akku-Ladung, sonstige Aufzüge), erst nach gesichertem 6.2-Betrieb.

Auslösekriterien: allgemeine AV-Störung > 0,5 s < 90 % Nenn (§3.4.7); Sicherheitsbeleuchtung nach E 8002-1
> 0,5 s < 75 % Nenn (§3.4.7 / A2 §5.1).
Betriebsdauer-Grundregel: **24 h**, reduzierbar auf **3 h** wenn gefahrlose Beendigung + geordnetes Verlassen
in 3 h möglich (AC1-Ergänzung zu §5.1). SV-Bemessung: 80 % Last in 15 s, Rest 20 % nach + 5 s (§6.5.3).

## Raumtyp → Anforderung (medizinisch)
Anwendungsgruppen (§3.2, Tabelle 1) sind die Weiche:

- **AG 0** (keine/zulässige elektromed. Geräte, z. B. Bettenräume ohne Gerät, Praxisräume):
  Sicherheitsbeleuchtung nur nach allgemeiner Logik (Rettungswege/Rettungszeichen); keine besonderen
  IT-/ZSV-Anforderungen. Im Zweifel **nicht** AG 0 verwenden.
- **AG 1** (Geräte mit Patientenkontakt, Abbruch hinnehmbar — Bettenräume, phys./Hydro-Therapie, Massage,
  Praxis, Radiologie, Endoskopie, Dialyse, Intensiv-Untersuchung, Entbindung, chirurg. Ambulanz):
  je Raum ≥ 1 Allgemeinleuchte + Untersuchungsleuchten aus SV, Umschaltzeit ≤ 15 s (§6.2.1.2(2) / A1 5.1.1(5)).
- **AG 2** (operative/lebensnotwendige Maßnahmen, Weiterbetrieb zwingend — OP-Vorbereitung, OP, Aufwach-,
  OP-Gips-, Intensiv-Untersuchung/-Überwachung, Herzkatheter, Endoskopie mit Blutungsrisiko, Notfall-/
  Akutdialyse, klinische Entbindung, IMCU):
  - Raumbeleuchtung ≥ 50 % aus SV-Quelle, ≤ 15 s (§6.2.1.2(3); A1 verlangt 100 %, A2 stellt auf ≥ 50 %).
  - **OP-Leuchten/vergleichbare Leuchten**: ZSV ≤ 0,5 s, 3 h (§6.4.2 / A2 5.3.2), fest angeschlossen.
  - **Lebenswichtige/chirurgische Geräte**: ZSV ≤ 15 s, 3 h (bzw. 1 h + weitere Quelle) (§6.4.1).
  - Zusätzlich ZSV-versorgte Beleuchtung im Raum; eigenes ZSV-IT-System je Raum/Raumgruppe.
- **Praxis außerhalb KH** (§9.1, i. d. R. AG 1): SV ≥ 3 h; in AG 2 OP-Leuchten ≤ 0,5 s, lebenswichtige ≤ 15 s.
- **Pflegeheim/Kuranstalt** (§9.3): SV ersetzt durch Notbetrieb-Aggregat für NSE (Notruf, Sicherheitsbel.,
  Drucksteigerung, notw. med. Geräte). Rettungswege/Rettungszeichen: 8 h (Treppen/Zeichen), 15 s (Rettungswege).

Medizinische Nur-Elektro-Themen (nicht Notbeleuchtung, nur zur Abgrenzung): IT-Netz mit
Isolationsüberwachung je AG-2-Raum (§4.3.3.3, §5.3.5), zusätzlicher Potenzialausgleich in der
Patientenumgebung 1,5 m (§5.4, Anhang C), TN-S ohne PEN ab Gebäude-HV (§4.3.1) — hier nur erwähnt,
für die Notbeleuchtungs-Engine nicht regelbildend.

## Offene Punkte / Extraktionslücken
- **A1 vs. A2 Widerspruch AG-2-Beleuchtung:** A1 §5.1.1(6) fordert 100 % Raumbeleuchtung aus SV, die
  spätere A2 §5.1.1.2(4) und die konsolidierte §6.2.1.2(3) fordern ≥ 50 %. Für die Engine gilt die
  jüngste konsolidierte Fassung (**≥ 50 %**); Widerspruch dokumentiert, im Zweifel LB/Fachplaner.
- **Genaue Seitenzahlen** einzelner §6-Abschnitte (SV/ZSV) sind im Digest nur als Seitenbereich 1–40
  angegeben; präzise Seiten ggf. aus Volltext OEVE_OENORM_E_8007.txt nachziehen.
- **Betriebsdauer-Ausnahme 3 h** ist im Kern-Digest (§6.1) und im Corrigendum AC1 (§5.1) redundant;
  maßgeblich ist die berichtigte AC1-Fassung.
- Wechselwirkung mit **EN 1838** (Lux-Werte Rettungsweg/Antipanik) und **E 8002-1** (Technik) ist in E 8007
  nur per Verweis geregelt — die konkreten Lux/Erkennungsweiten kommen aus jenen Normen, nicht aus E 8007
  (Ausnahme: A1 §5.1.1 mit 1 lx / 15 lx-Werten, oben als R32–R34 erfasst).
- Abgleich mit **OVE E 8101 Teil 7-710** (Nachfolger) steht aus: prüfen, ob 7-710 die 0,5 s/15 s-Klassen
  und die AG-0/1/2-Systematik unverändert übernimmt.
