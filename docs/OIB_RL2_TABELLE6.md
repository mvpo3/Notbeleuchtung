# OIB-Richtlinie 2 — Punkt 5.4 + Tabelle 6 (Erforderlichkeit Sicherheitsbeleuchtung)

**Analysiert:** 2026-08-30 (Enis) · **rein lesend aus den Original-PDFs**, nichts aus
Modellwissen ergänzt. Diese Datei ist die fachliche Grundlage für den späteren
OIB-Resolver in `normwissen/`; die Contract-Spezifikation dazu liegt in
[`SPEC_PROJEKTKONTEXT_OIB.md`](SPEC_PROJEKTKONTEXT_OIB.md).

## Quellen (alle Ausgabe Mai 2023, Original-PDFs im Repo)

| Kürzel | Pfad | Dok.-Nr. | Seiten-Offset |
|---|---|---|---|
| RL 2 | `knowledge/OIB-Richtlinien/OIB-Richtlinie 2 Brandschutz/oib-rl_2_ausgabe_mai_2023.pdf` | OIB-330.2-029/23 | PDF-Seite = Norm-Seite + 2 |
| RL 2-Erl | `…/OIB-Richtlinie 2 Brandschutz/erlaeuterungen_oib-rl_2_ausgabe_mai_2023.pdf` | OIB-330.2-034/23 | PDF-Seite = Erl.-Seite + 2 |
| Begriffe | `…/OIB Richtlinie Begriffsbestimmung/oib-rl_begriffsbestimmungen_ausgabe_mai_2023.pdf` | OIB-330-003/23 | PDF-Seiten direkt zitiert |
| RL 2.1 | `…/OIB Richtline 2.1 Branschutz bei Betriebsbauten/oib-rl_2.1_ausgabe_mai_2023.pdf` | OIB-330.2-030/23 | |
| RL 2.2 | `…/OIB Richtlinie 2.2 Branschutz bei Garagen…/oib-richtlinie_2.2_ausgabe_mai_2023.pdf` | OIB-330.2-031/23 | |
| RL 2.3 | `…/OIB Richtlinie 2.3 Brandschutz bei Gebäuden…22m/oib-rl_2.3_ausgabe_mai_2023.pdf` | OIB-330.2-032/23 | |

> ⚠ Die Quell-PDFs liegen seit 2026-08-30 im Repo (getrackt). Der frühere
> Trailing-Space im Ordnernamen ist beim Committen bereinigt worden; Umlaute in
> den Unterordnern sind NFD-kodiert und die Schreibweisen der Originalordner
> (`Branschutz`, `Richtline`) bewusst unverändert. Beim Skripten `glob` statt
> handgetippter Pfade verwenden.

## Punkt 5.4 (RL 2, PDF-S.14 = Norm-S.12), vollständig

> „Für die in der Tabelle 6 angeführten Nutzungen ist eine entsprechende
> Sicherheitsbeleuchtung gemäß dieser Tabelle zu errichten. Bei Gebäuden bzw.
> Bauwerken mit jeweils gemischter Nutzung gelten die für die jeweilige Nutzung
> anzuwendenden Anforderungen."

## Tabelle 6 (RL 2, PDF-S.34 = Norm-S.32)

**Struktur:** genau **zwei** Wertespalten — (A) „Sicherheitsbeleuchtung eingeschränkt
auf Fluchtwege und festverlegtes Rettungswegesystem" (das ist EINE Spalte, kein
eigenes Kriterium) und (B) „Sicherheitsbeleuchtung, uneingeschränkt".
Eine Spalte „nicht erforderlich" existiert **nicht**.

| Zeile | Nutzungsart | Kriterium | (A) eingeschränkt | (B) uneingeschränkt |
|---|---|---|---|---|
| 1 | *Gruppenkopf:* Gebäude mit Fluchtniveau ≤ 22 m | — | — | — |
| 1.1 | Wohngebäude der GK 5, außerhalb von Wohnungen | Gebäudeklasse | erforderlich | nicht erforderlich |
| 1.2 | sonstige Gebäude der GK 4 und 5 | Gebäudeklasse | erforderlich | nicht erforderlich |
| 2 | Schul-/Kindergartengebäude + vergleichbare Nutzung | Netto-Grundfläche (1) | ≤ 3.200 m² | > 3.200 m² |
| 3 | Beherbergungsstätten, Studentenheime + vergleichbar | Betten | > 10 und ≤ 100 | > 100 |
| 4 | Verkaufsstätten, Ausstellungsstätten | Verkaufsfläche (2) | > 200 m² und ≤ 3.000 m² | > 3.000 m² |
| 5 | *Gruppenkopf:* Gaststätten | — | — | — |
| 5.1 | Schank- oder Speisewirtschaften | Verabreichungsplätze | > 60 und ≤ 240 | > 240 |
| 5.2 | Diskotheken und Tanzcafés | Personen | ≤ 120 | > 120 |
| 6 | Alters-/Alten-/Seniorenheime, Seniorenresidenzen + vergleichbar | Betten | > 10 und ≤ 100 | > 100 |
| 7 | Pflegeheime | Betten | ≤ 16 | > 16 |
| 8 | Krankenhäuser | — | nicht zutreffend | erforderlich |
| 9 | *Gruppenkopf:* Räume für eine größere Personenanzahl (Theater, Kinos, Stadien, Sportstätten, Schwimmhallen, Sitzungssaal und dergleichen) | — | — | — |
| 9.1 | Versammlungsstätten **innerhalb** von Gebäuden, Versammlungsräume und sonstige Räume, die für den Aufenthalt von **mehr als 60 Personen** bestimmt sind | Personen | ≤ 240 | > 240 |
| 9.2 | Versammlungsstätten + zugehörige Bühnen/Szeneflächen sowie Sportstätten **außerhalb** von Gebäuden | Personen | > 120 und ≤ 5000 | > 5000 |
| 10 | Betriebsbauten | Netto-Grundfläche (1) | > 200 m² | **gemäß Arbeitsstättenverordnung (AStV)** |
| 11 | *Gruppenkopf:* Garagen, überdachte Stellplätze und Parkdecks | — | — | — |
| 11.1 | Garagen und Parkdecks | Nutzfläche (3) | > 250 m² und ≤ 1.600 m² | > 1.600 m² |
| 11.2 | überdachte Stellplätze | Nutzfläche | > 1.600 m² | nicht erforderlich |
| 12 | *Gruppenkopf:* Gebäude mit Fluchtniveau > 22 m | — | — | — |
| 12.1 | Wohngebäude, außerhalb von Wohnungen | Fluchtniveau | > 22 m und ≤ 32 m | > 32 m |
| 12.2 | sonstige Gebäude | — | nicht zutreffend | erforderlich |

**Fußnoten (Original):** (1) Netto-Grundfläche · (2) Verkaufsfläche (gemäß
OIB-Begriffsbestimmungen) · (3) Nutzfläche – Garagen, überdachte Stellplätze,
Parkdecks (gemäß OIB-Begriffsbestimmungen).

**Ausnahme außerhalb der Tabelle** — RL 2 Punkt **7.9.12** (PDF-S.22):
> „Abweichend zu Punkt 3 der Tabelle 6 ist für Schutzhütten in Extremlage erst ab
> 30 Schlafplätzen eine Sicherheitsbeleuchtung erforderlich."

### MANUELL PRÜFEN
- Zeile 11.2: Flächeneinheit ohne Fußnoten-Marker im Original (vermutlich (3)).
- Begriffe PDF-S.10: Definition „Netto-Grundfläche" war im Textextrakt nicht
  sauber auslesbar — vor Verwendung am PDF gegenlesen.
- Zeile 9.1 nennt zwei Personenzahlen (Anwendungsschwelle > 60, Stufenschwelle 240).
  Dass beide dieselbe Größe meinen, ist naheliegend, aber Auslegung.

## Erläuterungen zu Punkt 5.4 (RL 2-Erl, PDF-S.50 = Erl.-S.48)

**Eingeschränkte Stufe** („allgemeine Anforderungen"):
1. Sicherheitsbeleuchtung **für Fluchtwege** gemäß **ÖNORM EN 1838** sowie
   **ÖVE/ÖNORM EN 50172**;
2. elektrische Anlage gemäß **OVE E 8101** (allgemeine Errichtung) sowie – je nach
   Zutreffen – **OVE-Richtlinie R 12-2 Punkte 3, 4 und 5.1 bis 5.3**;
3. Betrieb im Brandfall (Funktionserhalt) gemäß OVE E 8101 sowie **R 12-2 Punkt 6**,
   **wobei abgewichen werden kann**, wenn die Räume durch andere brandschutz-
   technische Maßnahmen (z.B. automatische Brandmeldeanlage) geschützt sind.

**Uneingeschränkte Stufe** („erhöhte Anforderungen"): dieselben drei Punkte, aber
Sicherheitsbeleuchtung **nicht** auf Fluchtwege eingeschränkt und **ohne** die
Abweichungsmöglichkeit bei Punkt 6.

Weitere Aussagen derselben Seite:
- Herkunft der Grenzwerte: „bei der Festlegung der Grenzwerte wurde auf die bereits
  in der Praxis üblichen Werte zurückgegriffen."
- Verkehrstechnische Einrichtungen (Flughäfen, Bahnhöfe): Zuständigkeit beim Bund,
  daher keine Werte; „sinngemäß **können** jedoch diese Nutzungen mit Punkt 4
  gleichgestellt werden" → **Kann-Aussage**, kein Automatismus.
- **Begriffsbrücke:** „Es wird darauf hingewiesen, dass mit der Bezeichnung
  ‚Rettungsweg' in der ÖNORM EN 1838 die Bezeichnung ‚Fluchtweg' gemäß
  OIB-Richtlinien Begriffsbestimmungen gemeint ist."
- **AStV-Parallelpfad:** Gebäude/Räume, die nach ASchG Arbeitsstätte sind, sind
  gemäß AStV erforderlichenfalls mit Sicherheitsbeleuchtung auszustatten, „auch wenn
  gemäß Tabelle 6 … keine Sicherheitsbeleuchtung verlangt oder sie in Tabelle 6
  nicht enthalten ist"; Unterstützung gibt die OEK-Fachinformation (= OVE E08).

## Sonderrichtlinien 2.1 / 2.2 / 2.3

| Dokument | Gebäudetyp | Fundstelle | eigene Regel? | Verweis auf Tabelle 6? | Zusatzbedingung |
|---|---|---|---|---|---|
| RL 2.1 | Betriebsbauten | Punkt **3.6.5**, PDF-S.7 | nein | ja, ausschließlich | — |
| RL 2.2 | überdachte Stellplätze > 250 m² | Punkt **4.3**, PDF-S.6 | nein | ja | Kap.-Anwendungsbereich > 250 m² |
| RL 2.2 | Garagen > 250 m² | Punkt **5.5.3**, PDF-S.7 | **teilweise** — „In Garagen mit einer Nutzfläche von mehr als 250 m² ist eine Sicherheitsbeleuchtung erforderlich, wobei die Anforderungen der Tabelle 6 … gelten." | ja (Ausgestaltung) | > 250 m² Nutzfläche |
| RL 2.2 | Parkdecks | Tabelle 3, Zeile **8.2**, PDF-S.13 | nein | ja („siehe Tabelle 6 der OIB-Richtlinie 2") | — |
| RL 2.3 | Fluchtniveau > 22 m | Punkt **2.14**, PDF-S.8 | nein | ja, ausschließlich | RL gliedert nach ≤ 32 / > 32 ≤ 90 / > 90 m; Tabelle 6 kennt nur 32 m |

Für **Garagen und überdachte Stellplätze ≤ 250 m²** (RL 2.2 Kap. 2 und 3) gibt es
**keinen** Sicherheitsbeleuchtungs-Punkt → Schweigen, kein „nicht erforderlich".

## Begriffsbestimmungen (Ausgabe Mai 2023, PDF-Seiten)

| Begriff | S. | Kern |
|---|---|---|
| Betriebsbau | 5 | Bauwerk/Teil, das der Produktion (Herstellung, Behandlung, Verwertung, Verteilung) bzw. Lagerung von Produkten/Gütern dient |
| Fluchtniveau | 7 | Höhendifferenz Fußbodenoberkante höchstgelegenes oberirdisches Geschoß ↔ angrenzende Geländeoberfläche nach Fertigstellung im Mittel |
| Fluchtweg | 8 | Weg, der im Gefahrenfall ohne fremde Hilfe das Erreichen eines sicheren Ortes im Freien ermöglicht |
| Garage | 8 | Gebäude/Gebäudeteil zum Einstellen von Kraftfahrzeugen |
| GK 4 | 8 | ≤ 4 oberirdische Geschoße, Fluchtniveau ≤ 11 m, mehrere Wohnungen/Betriebseinheiten à ≤ 400 m² Nutzfläche |
| GK 5 | 8 | Fluchtniveau ≤ 22 m, nicht in GK 1–4 fallend |
| Netto-Grundfläche | 10 | **MANUELL PRÜFEN** (Extrakt unvollständig) |
| Nutzfläche – Garage/überd. Stellplatz/Parkdeck | 11 | Summe der Stellplatz- und Fahrflächen, ausgenommen Zu-/Abfahrten außerhalb |
| Parkdeck | 11 | Bauwerk, das in allen Parkebenen an ≥ 2 Seiten unverschließbare Öffnungen ≥ ⅓ der Umfassungswandfläche aufweist |
| Stellplatz, überdacht | 13 | überdachte Fläche, an höchstens zwei Seiten umschlossen |
| Verkaufsfläche | 14 | Bereiche, in denen Waren zum Verkauf angeboten werden, inkl. Kassen, Windfänge, Ausstellungs-/Vorführ-/Beratungsräume, gastgewerblich genutzte Räume |
| Versammlungsraum / -stätte | 14 | Raum bzw. Bauwerk für größere Menschenansammlungen |
| Wohngebäude | 15 | Gebäude, die ganz oder überwiegend zum Wohnen genutzt werden |

## Verbindlichkeit — offen

Keines der geprüften Dokumente sagt, wodurch eine OIB-Richtlinie im konkreten
Projekt verbindlich wird (Übernahme ins Landesbaurecht). Für den Audit-Trail ist
das noch zu klären → `bundesland` + Rechtsgrundlage im Projektkontext, siehe Spec.
