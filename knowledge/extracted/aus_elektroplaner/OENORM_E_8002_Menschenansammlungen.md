# ÖVE/ÖNORM E 8002 (2007) — Sicherheitsstromversorgung in baulichen Anlagen für Menschenansammlungen
**Quelle:** elektro-planer knowledge/normen/OEVE_OENORM_E_8002-{1,2,8}.txt, via Teil-Digests (`digests/normen/OEVE_OENORM_E_8002-1.part0.md`, `.part1.md`, `-2.part0.md`, `-8.part0.md`) · **Übernommen:** 2026-08-28
**Einordnung:** Historische AT-Norm (2019 in OVE E 8101 Teil 5-56/7-718 integriert). Für Neubau gilt E 8101; hier als konzeptioneller Ursprung + Bestandsrelevanz. Teil 1 (Allgemeines) ist mit dem jeweils zutreffenden Teil 2–6/8/9 gemeinsam anzuwenden; bei Mehrfachzuordnung gelten die **höheren** Sicherheitsanforderungen.

**Teile-Übersicht (Reihe E 8002):**
- **Teil 1 — Allgemeines:** trägt den kompletten technischen Regelinhalt (Anforderungen an Sicherheitsbeleuchtung, Sicherheitsstromquellen, Verteiler, Kabel, Funktionserhalt, Prüfung). Alle anderen Teile bauen darauf auf.
- **Teil 2 — Veranstaltungsstätten:** Versammlungsräume/Bühnen/Sportstätten; Erfordernis erst ab Personen-Schwellen (>100/120/200; Freilicht >1 000/5 000). Ergänzt v.a. Antipanik + Schaltung.
- **Teil 3 — Verkaufs- und Ausstellungsstätten** (nicht separat extrahiert; in Tabelle 1 als Spalten „bis/über 20 Sicherheitsleuchten").
- **Teil 4 — Hochhäuser** (Referenz für 8-h-Nennbetriebsdauer via Fußnote c).
- **Teil 5 — Gaststätten** (Referenz für 8-h-Nennbetriebsdauer via Fußnote c).
- **Teil 6 — Großgaragen** (Tabelle-1-Spalte: keine Antipanik-Pflicht, Nennbetriebsdauer 1 h).
- **Teil 7 — bleibt frei.**
- **Teil 8 — Fliegende Bauten** (Zelte, temporäre Nutzung fester Bauwerke) als Veranstaltungs-/Verkaufs-/Ausstellungsstätten/Gaststätten: reduzierte Anforderungen (Nennbetriebsdauer 1 h, Einzelbatterien immer zulässig, kein Funktionserhalt).
- **Teil 9 — Schulen** (in Tabelle 1 mit Beherbergung/Hochhäusern zusammengefasst).

## Relevanz für die Engine
- **Erforderlichkeit je Gebäudetyp** (2. Input LB / Norm-Default): Diese Reihe liefert die AT-spezifische Antwort auf „WANN ist Sicherheitsbeleuchtung Pflicht" nach Nutzungsart + Schwellenwert (Fläche/Personenzahl) — komplementär zu EN 1838, die nur das „WIE" (Lux, Erkennungsweite) regelt.
- **Antipanik-Trigger:** Fläche > 60 m² ohne festgelegte Rettungswege (E 8002-1, 3.2.2.1.2) → deckungsgleich mit dem Antipanik-Konzept der Engine; zusätzlich nutzungsspezifische Antipanik-Pflichten (Veranstaltungsstätten, Verkehrsbauten).
- **Betriebsdauer/Umschaltzeit** als harte Grenzwerte für Dimensionierung (Tabelle 1: 1 lx Rettungsweg, 0,5 lx Antipanik, 3 h/1 h/8 h Nennbetriebsdauer, 5 s→50 % / 60 s→100 %).
- **Endstromkreis-Invarianten** (max. 20 Leuchten/Kreis, alternierend auf ≥ 2 Schutzeinrichtungen, ≤ 13 A, max. 60 % Last) sind direkt platzierungs- und verkabelungsrelevant und potenziell als Platzierungs-Constraints abbildbar.
- **Achtung Aktualität:** Werte sind der Stand 2007. Für Neubau ist OVE E 8101 (bereits im Repo) die maßgebliche Quelle; E 8002 dient als Herkunft/Bestandsabgleich. `norm_quelle` sollte für Neubauplanung auf E 8101 zeigen, nicht auf E 8002.

## Regel-Tabelle (Notbeleuchtungs-relevant)
| ID | Teil/§ (Seite) | Regel | Werte | Typ |
|----|----------------|-------|-------|-----|
| E8002-R1 | T1 §4.3.1, Tab.1 Z.1 (S.~15) | Mindestbeleuchtungsstärke Rettungswege (alle Nutzungsarten) | **1 lx** | Grenzwert |
| E8002-R2 | T1 §4.3.1, Tab.1 Z.2 (S.~15) | Mindestbeleuchtungsstärke Antipanik (außer Großgaragen) | **0,5 lx**; Großgaragen: keine | Grenzwert |
| E8002-R3 | T1 §4.3.1, Tab.1 Z.3 (S.~15) | Zeit bis Erreichen des Mindestwerts | **50 % nach 5 s, 100 % nach 60 s** | Grenzwert |
| E8002-R4 | T1 §4.3.1, Tab.1 Z.4 (S.~15) | Nennbetriebsdauer Sicherheitsstromquelle | Regelfall **3 h**; Großgaragen **1 h**; Beherbergung+Hochhäuser **3 bzw. 8 h** (Fußnote c) | Grenzwert |
| E8002-R5 | T1 §4.3.1, Tab.1 Z.5 (S.~15) | Rettungszeichen an Rettungswegen in Dauerschaltung | gefordert (Bereitschaftsschaltung nur zulässig, wenn Allgemein-/Tageslicht + Beleuchtungsstärke **> 50 lx** an Zeichenoberfläche, außer Verkaufsstätten) | Gebot |
| E8002-R6 | T1 §3.2.18 / §7.1.1 (S.~10) | Umschaltung Sicherheitsstromversorgung: Störung = Spannung > 0,5 s unter 75 % der Netznennspannung | **> 0,5 s**, **< 75 % U_N** | Definition |
| E8002-R7 | T1 §3.2.2.1.2 (S.~9) | Antipanikbeleuchtung erforderlich bei Bereichen ohne festgelegte Rettungswege | Fläche **> 60 m²** (bzw. kleiner bei erhöhtem Risiko) | Gebot |
| E8002-R8 | T1 §4.3.1 Nr.1 (S.~14) | Sicherheitsbeleuchtung in Sanitärbereichen | ab **8 m²** + Behinderten-WCs | Gebot |
| E8002-R9 | T1 §4.3.1 Nr.4 (S.~14) | Bodennahes Sicherheitsleitsystem prüfen bei erhöhter Gefährdung | zusammenhängende Räume **> 8 000 m²** + hoher Anteil Ortsunkundiger; Ausführung TRVB E 102 / BGR 216 | Empfehlung |
| E8002-R10 | T1 §3.2.26 (S.~10) | Bodennahe Sicherheitsleitsysteme: Oberkante über Fußboden | **≤ 40 cm** | Definition |
| E8002-R11 | T1 §3.2.4 (S.~9) | Dauerschaltung: max. zulässige Unterbrechung | **≤ 0,5 s** | Definition |
| E8002-R12 | T1 §7.7.15 (S.~40) | Max. Leuchten je Endstromkreis der Sicherheitsbeleuchtung | **20 Leuchten** | Grenzwert |
| E8002-R13 | T1 §7.7.16 (S.~40) | In Räumen/Rettungswegen mit > 1 Leuchte: abwechselnd auf ≥ 2 unabhängige Überstromschutzeinrichtungen (außer Einzelbatterie) | **≥ 2 Stromkreise** | Gebot |
| E8002-R14 | T1 §7.7.13 (S.~40) | Endstromkreis Sicherheitsbeleuchtung: Überstromschutz + Belastung | Schutz **≤ 13 A**, max. **60 %** Belastung | Grenzwert |
| E8002-R15 | T1 §7.7.9 (S.~40) | Mindest-Leiterquerschnitt Endstromkreise | **1,5 mm²** | Grenzwert |
| E8002-R16 | T1 §7.7.17 / §7.8.1 (S.~40) | Sicherheitsleuchten + Verbindungs-/Abzweigstellen kennzeichnen | Farbe **grün** + Verteiler-/Stromkreis-/Leuchtennummer | Gebot |
| E8002-R17 | T1 §7.8.2 (S.~40) | Wechselrichter-Grenzen | Einzelwechselrichter **1–2 Leuchten**; Gruppenwechselrichter **≤ 20 Leuchten/Endstromkreis**, Reserve **≥ 120 %**, Strom **≤ 6 A**; Funktion **5–40 °C** | Grenzwert |
| E8002-R18 | T1 §3.2.13.2 / §7.4.2 (S.~9/38) | Gruppenbatterieanlage (LPS): max. Anschlussleistung | **500 W bei 3 h** bzw. **1 500 W bei 1 h**; Brauchbarkeit **≥ 5 J** bei 20 °C; Ladung nach 12 h ≥ 80 % | Grenzwert |
| E8002-R19 | T1 §3.2.13.3 / §7.4.3 (S.~9/38) | Zentralbatterieanlage (CPS): keine Leistungsbegrenzung | Brauchbarkeit **≥ 10 J** bei 20 °C; Ladung nach 12 h ≥ 80 % | Definition |
| E8002-R20 | T1 §3.2.13.1 (S.~9) | Einzelbatterieanlage versorgt | i.A. **eine, höchstens zwei** Sicherheitszeichen / eine Sicherheitseinrichtung | Definition |
| E8002-R21 | T1 §7.1.4 / §7.4.1 / §7.4.2 / §7.4.3 (S.~38) | Ab-Schwelle für automatische Prüfeinrichtung mit zentraler Registrierung | **50 Sicherheits-/Einzelbatterieleuchten** im zusammenhängenden Gebäudeteil | Gebot |
| E8002-R22 | T1 §3.2.13.4 / §7.4.4–7.4.5 (S.~9) | Umschaltzeiten Aggregate | Sicherheitsstromaggregat **≤ 15 s**; Schnellbereitschaft **≤ 0,5 s**; Sofortbereitschaft **ohne Unterbrechung** | Grenzwert |
| E8002-R23 | T1 §7.4.4 (S.~38) | Benzinbetriebene Ottomotoren als Sicherheitsstromaggregat | **verboten** (Benzin = Gefahrenklasse I VbF); i.A. Diesel + Synchrongenerator | Verbot |
| E8002-R24 | T1 Tab.1 Z.6/Z.9 (S.~15) | Einzelbatterieleuchten bzw. Aggregat allein: Zulässigkeit nach Nutzungsart | Einzelbatterie **nicht** zulässig bei Veranstaltung/Verkauf>20/Großgaragen/Verkehr; Aggregat allein **nicht** bei Veranstaltung + Verkauf | Verbot |
| E8002-R25 | T1 §5.4 (S.~14) | Funktionserhalt Sicherheitsbeleuchtung: Mindestdauer | **30 min**; Löschwasser/mech. RWA/Feuerwehraufzug **90 min** | Grenzwert |
| E8002-R26 | T1 §5.4 (S.~14) | Bei lokalem Brand im mitversorgten Unterbrandabschnitt: verbleibende Rettungsweg-Sicherheitsbeleuchtung | **≥ 50 %** funktionsfähig; **Fluchtstiegenhäuser 100 %**; Unterbrandabschnitt max. **2 Leuchten** (TRVB B 108) | Grenzwert |
| E8002-R27 | T1 Tab.2 (S.~15) | Andere Sicherheitseinrichtungen: Nennbetriebsdauer / max. Unterbrechung | Löschwasser **4 h**/15 s · Feuerwehraufzug/Alarmierung/RWA/Personenaufzug **3 h**/15 s · CO-Warnanlage **1 h**/15 s | Grenzwert |
| E8002-R28 | T2 §1.2 (S.~2) | Veranstaltungsstätte = Sicherheitsbeleuchtung erforderlich ab Personen-Schwelle | Bühnen/Film **>100**; allg. Versammlung **>120**; beidseitig ins Freie **>200**; Freilicht Szene **>1 000**; Sport **>5 000** (Rasen nur >15 Stufen) | Gebot |
| E8002-R29 | T2 §4 (S.~4) | Antipanik zusätzlich in Versammlungsräumen, Mittel-/Vollbühnen, Bühnenbetriebsräumen > 20 m², Bildwerferräumen, Manegen, Sportbahnen, Freiluft-Stehplätzen | Bühnenbetriebsräume **> 20 m²** | Gebot |
| E8002-R30 | T2 §7.2(2) (S.~7) | Verdunkelte Versammlungsräume/Bühnen: Bereitschaftsschaltung, keine Selbstabschaltung bei Netzwiederkehr | nur Hand-Aus an Schalttafel | Gebot |
| E8002-R31 | T8 §7.1 (S.~5) | Fliegende Bauten: reduzierte Nennbetriebsdauer + Einzelbatterien immer zulässig | Nennbetriebsdauer **1 h**; Einzelbatterien **in allen Fällen** zulässig | Empfehlung |
| E8002-R32 | T8 §5 (S.~5) | Fliegende Bauten: Funktionserhalt (E 8002-1 Abschnitt 5) | **nicht anzuwenden** | Definition |
| E8002-R33 | T8 §7.4(2) (S.~5) | Fliegende Bauten: Kfz-Starterbatterien in CPS zulässig | nur **24 V, 48 V, 60 V** | Empfehlung |
| E8002-R34 | T1 §A.2 (S.~50) | Rettungsweg innerhalb elektrischer Betriebsräume bis Ausgang | **≤ 40 m**; lichte Höhe **≥ 2 m** (Gänge ≥ 1,80 m) | Grenzwert |

## Detail-Digest (Sicherheitsbeleuchtung/-stromversorgung)

### Begriffshierarchie (T1 §3.2, Bild 1)
Oberbegriff **Notbeleuchtung** = **Sicherheitsbeleuchtung** (Rettungswege · Antipanik · Arbeitsplätze mit besonderer Gefährdung) + **Ersatzbeleuchtung**. Diese Struktur deckt sich mit EN 1838; die E 8002 ergänzt die österreichische Erforderlichkeits-Systematik nach Gebäudetyp.

### Wo Sicherheitsbeleuchtung erforderlich ist (T1 §4.3.1)
Rettungswege, Nahbereich der Ausgänge außerhalb des Gebäudes, Aufzugskabinen + Triebwerksräume, Rolltreppen, Erste-Hilfe-Stellen, **Sanitärbereiche ab 8 m²** + Behinderten-WCs; Aggregate-/Verteiler-/Schaltanlagenräume (> 1 kV), Räume zentraler brandschutztechnischer Einrichtungen. Bei Verkehrsbauten (Flughäfen/Bahnhöfe) zusätzlich Antipanik in Wartezonen/Hallen und Geschäfts-/Betriebsflächen **> 60 m²**.

### Rettungszeichen (T1 §4.3.1.2)
Bei nicht unmittelbar sichtbarem Ausgang Richtungszeichen; jedes Rettungszeichen muss von **allen Punkten des Rettungsweges** sichtbar sein. Farbe/Gestaltung nach ÖNORM Z 1000-1/-2, Leuchtdichte nach EN 1838 — die eigentlichen lichttechnischen Werte (Erkennungsweite l = z × h) liegen also in EN 1838, nicht in E 8002.

### Schaltung (T1 §7.2)
Dauer- oder Bereitschaftsschaltung, kombinierbar, sofern nicht in Tabelle 1 bzw. Teil 2–9 festgelegt. Dauerschaltung: Überwachung am Hauptverteiler, selbsttätige Rückschaltung bei Netzwiederkehr. In tageslichtbeleuchteten, nicht verdunkelbaren Räumen darf Dauerschaltung mit der Allgemeinbeleuchtung geschaltet werden; bei Branderkennung (BMA) muss Bereitschaftsschaltung aktiviert werden (nicht bis 50 Einzelbatterieleuchten).

### Sicherheitsstromquellen (T1 §7.4) — Auswahl je Nutzungsart (Tabelle 1)
- **Einzelbatterie (3.2.13.1):** 1–2 Zeichen; nicht zulässig bei Veranstaltungsstätten, Verkauf > 20 Leuchten, Großgaragen, Verkehrsbauten.
- **Gruppenbatterie/LPS (3.2.13.2, EN 50171):** 500 W@3 h / 1 500 W@1 h; ortsfeste Batterien ≥ 3 J wartungsfrei; Brauchbarkeit ≥ 5 J@20 °C.
- **Zentralbatterie/CPS (3.2.13.3, EN 50171):** keine Leistungsbegrenzung; Brauchbarkeit ≥ 10 J@20 °C.
- **Aggregate:** Umschaltzeiten 15 s / 0,5 s / 0 s; Benzin-Otto verboten; Dieselbetrieb i.A. Standard; Batterie-Nennbetriebsdauer darf bei zusätzlichem Aggregat auf **1 h** reduziert werden (7.1.2).
- **Zwei unabhängige Netze (7.4.6):** nur wenn Energieversorger gleichzeitigen Ausfall ausschließt.

### Verteiler-/Endstromkreis-Invarianten (T1 §7.6/§7.7)
Max. 20 Leuchten je Endstromkreis; bei > 1 Leuchte alternierend auf ≥ 2 Schutzeinrichtungen (Ausfallredundanz); Überstromschutz ≤ 13 A + max. 60 % Last; ≥ 1,5 mm²; TN-S ab letztem Verteiler; grüne Kennzeichnung aller Sicherheitsleuchten + Abzweigstellen. In mehradrigem Kabel nur ein (Haupt-)Stromkreis. Getrennte Verlegung von Kabeln der Sicherheits- vs. allgemeinen Stromversorgung (Trennsteg auf gemeinsamer Tasse).

### Instandhaltung/Prüfung (T1 §9/§10) — für Audit/LB relevant
Erstprüfung inkl. Beleuchtungsstärkemessung nach EN 1838 (9.2.9). Wiederkehrend: tägliche Prüfung Gruppen-/Zentralbatterie (10.2.3), wöchentliche Prüfung Einzelbatterien (10.2.4), jährliche Batterieentladung (10.2.2), Beleuchtungsstärke ≥ alle 2 Jahre (10.2.11), Prüfbuch über ≥ 3 Jahre. Batterien mit < 2/3 der Nennbetriebsdauer sind zu erneuern (10.3.1). Automatische Prüfeinrichtung (7.4.3.9, EN 62034): Ladeüberwachung < 5 min, täglicher Funktionstest 0,5–5 min, Fehleranzeige schon bei Ausfall **einer** Leuchte.

### Teil 2 (Veranstaltungsstätten) — Spezifika
Erforderlichkeit personenzahlgebunden (>100/120/200/1 000/5 000). Antipanik zusätzlich in Versammlungsräumen, Mittel-/Vollbühnen, Bühnenbetriebsräumen > 20 m². In verdunkelten Räumen/Bühnen Bereitschaftsschaltung ohne Selbstabschaltung. Kleine Theater ≤ 200 Plätze mit Fußboden ≤ 1 m Höhendifferenz: Sicherheitsbeleuchtung muss nur Türen/Gänge/Stufen erkennbar machen.

### Teil 8 (Fliegende Bauten) — Spezifika
Reduziertes Regime für temporäre Bauten/Zelte: Nennbetriebsdauer **1 h**, Einzelbatterien immer zulässig (Batterie + Leuchte als bauliche Einheit), Kfz-Starterbatterien in CPS zulässig (24/48/60 V), **kein Funktionserhalt** (Abschnitt 5 nicht anzuwenden), Verteiler-Schutzbereich 2,4 m frei von entzündlichem Material, keine Betriebsmittel > 1 kV (außer Leuchtröhren EN 50107), keine sichtbar glühenden Strahlungsheizgeräte.

## Verhältnis zu OVE E 8101 (was wurde übernommen)
- E 8002 ist die **2007er Vorläufernorm**; ihr Regelinhalt zur Sicherheitsstromversorgung wurde 2019 in **OVE E 8101** überführt (v.a. Teil 5-56 „Errichten von Anlagen für Sicherheitszwecke" und Teil 7-718 „Anlagen baulicher Anlagen für Menschenansammlungen"). Für **Neubau/Erweiterung** gilt E 8101.
- **Übernommene Kernkonzepte** (weitgehend identisch geführt): Umschaltkriterium > 0,5 s / < 75 % U_N; getrennter Sicherheitskreis ab Hauptverteiler; max. 20 Leuchten/Endstromkreis; alternierende Aufteilung auf ≥ 2 Stromkreise; Funktionserhalt-Systematik (E 30/E 90 nach ÖNORM DIN 4102-12); Quellenarten Einzel-/Gruppen-/Zentralbatterie + Aggregat mit Umschaltzeiten 0,5/15 s; automatische Prüfeinrichtung nach EN 62034; lichttechnische Delegation an EN 1838.
- **Weiterhin extern referenziert (nicht in E 8101 aufgegangen):** EN 1838 (Lichttechnik), EN 50171 (CPS), EN 50172 (Sicherheitsbeleuchtungsanlagen), TRVB E 102 / BGR 216 (bodennahe Leitsysteme).
- **Bestandsrelevanz:** Bei Bestandsanlagen, die nach E 8002 errichtet wurden, sind deren Nutzungsart-Schwellen (Tabelle 1) und Betriebsdauern der maßgebliche historische Bezug — für einen Bestandsabgleich/Audit nutzbar.

## Offene Punkte / Extraktionslücken
- **Teile 3, 4, 5, 6, 9 nicht separat extrahiert:** Ihre nutzungsspezifischen Schwellen (Verkaufsstätten-Flächen, Hochhaus-Höhengrenzen, Gaststätten-Personenzahlen, Großgaragen-Details, Schul-Kriterien) fehlen im Detail. Die Tabelle-1-Spalten und Fußnoten (c: 8 h nur Beherbergung/Hochhäuser via E 8002-4/-5:2002) geben nur einen Teilbezug. Bei Bedarf Volltexte `OEVE_OENORM_E_8002-{3,4,5,6,9}.txt` nachziehen.
- **Seitenzahlen** in der Regel-Tabelle sind aus der part-Digest-Struktur genähert (Teil 1: part0 = S.1–40, part1 = S.41–58); exakte Seiten bei Zitatpflicht am Volltext verifizieren.
- **E 8002-1 §7.2.3** (konkrete Beleuchtungsstärke-Formulierung, auf die Teil 2 verweist) ist im part-Digest nicht ausformuliert — bei Bedarf Volltext prüfen.
- **Antipanik-Beleuchtungsstärkeverlauf über die Fläche** (Gleichmäßigkeit, Randabstände) steht in EN 1838, nicht in E 8002; für die Engine dort verankern.
- Werte sind **Stand 2007** — für Neubau immer gegen OVE E 8101 (Repo) gegenprüfen, bevor sie als `norm_quelle` gesetzt werden.
