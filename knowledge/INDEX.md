# Wissens-Index (GENERIERT — nicht von Hand editieren)

Landkarte des Wissens-Korpus. Regenerieren: `python scripts/wissen_index.py`.
Der Index verlinkt nur; die Quell-Dateien sind die Wahrheit. **Norm-Werte niemals
aus dem Index zitieren — immer der autoritativen YAML/dem Contract folgen.**

## Norm-Wissen — AUTORITATIV (nur abfragen, nie umschreiben; Enis' Lane)
*Single-Source-of-Truth der EN-1838/ÖNorm-Werte. Änderungen NUR über Enis + Contract.*

- [en1838_grundwerte](src/notbeleuchtung/normwissen/data/en1838_grundwerte.yaml) — en1838_grundwerte.yaml — Norm-Grundwerte Notbeleuchtung (ÖNORM EN 1838:2013)
- [lb_extraktion](src/notbeleuchtung/normwissen/data/lb_extraktion.yaml) — lb_extraktion.yaml — Vokabular + Muster für das LB-Parsing (2. Input)
- [oib_rl2_tabelle6](src/notbeleuchtung/normwissen/data/oib_rl2_tabelle6.yaml) — oib_rl2_tabelle6.yaml — OIB-Richtlinie 2, Punkt 5.4 + Tabelle 6
- [ove_e8101_zusatz](src/notbeleuchtung/normwissen/data/ove_e8101_zusatz.yaml) — ove_e8101_zusatz.yaml — belegte Zusatz-Anforderungen aus OVE E 8101
- [platzierung_regeln](src/notbeleuchtung/normwissen/data/platzierung_regeln.yaml) — platzierung_regeln.yaml — Placement-Decision-Matrix Notbeleuchtung
- [raumtyp_regeln](src/notbeleuchtung/normwissen/data/raumtyp_regeln.yaml) — raumtyp_regeln.yaml — Raumtyp × Fluchtweg → NormAnforderung
- [regel_deckung](src/notbeleuchtung/normwissen/data/regel_deckung.yaml) — regel_deckung.yaml — Deckungs-Matrix Kanon-Raumtyp → Regelwerk (Owner: Enis)
- [sonderstellen](src/notbeleuchtung/normwissen/data/sonderstellen.yaml) — sonderstellen.yaml — Typ-Katalog der hervorzuhebenden Stellen (EN 1838 §4.1.2)

## Extrahiertes Wissen / Digests
*Produkt-/Norm-/Referenz-Digests, Wettbewerb. Prosa — KI darf verlinken/zusammenfassen.*

- [Analyse — Notbeleuchtung Baufeld E2 (Referenz-Praxis vs. EN 1838)](knowledge/extracted/ANALYSE_Baufeld_E2_Notbeleuchtung.md) — **Ziel:** Die vom Planer gesetzte Notbeleuchtung in den 9 Elektromontageplänen
- [ÖVE/ÖNORM E 8002 (2007) — Sicherheitsstromversorgung in baulichen Anlagen für Menschenansammlungen](knowledge/extracted/aus_elektroplaner/OENORM_E_8002_Menschenansammlungen.md) — **Quelle:** elektro-planer knowledge/normen/OEVE_OENORM_E_8002-{1,2,8}.txt, via Teil-Digests (`digests/normen/OEVE_OENORM_E_8002-1.part0.md…
- [ÖVE/ÖNORM E 8007 (2007) — Sicherheitsstromversorgung in Krankenhäusern/medizinischen Räumen](knowledge/extracted/aus_elektroplaner/OENORM_E_8007_medizinisch.md) — **Quelle:** elektro-planer knowledge/normen/OEVE_OENORM_E_8007*.txt, via Teil-Digests · **Übernommen:** 2026-08-28
- [OVE E 8101:2025-10 — Notbeleuchtungs-Deltas gegenüber Ausgabe 2019](knowledge/extracted/aus_elektroplaner/OVE_E_8101_2025_Deltas.md) — **Quelle:** elektro-planer knowledge/normen/OVE E8101_2025.txt (852 S.), via Teil-Digests (part4 = Teil 4-42, part13 = Teil 5-56/560 + Anhä…
- [OVE-Fachinformationen E-05 / E-06 / E-07 — Sicherheitsbeleuchtung (AT)](knowledge/extracted/aus_elektroplaner/OVE_Fachinfos_E05_E06_E07.md) — **Quelle:** elektro-planer knowledge/normen/Fachinfo_E-0{5,6,7}...txt · **Übernommen:** 2026-08-28
- [aus_elektroplaner — gefiltertes Norm-/Praxiswissen aus dem elektro-planer-Projekt](knowledge/extracted/aus_elektroplaner/README.md) — Das elektro-planer-Projekt hatte eine große Wissensbasis (~1140 extrahierte
- [Schrack „Not- und Sicherheitsbeleuchtung" — Produktkatalog (k-sibe-at9)](knowledge/extracted/aus_elektroplaner/Schrack_Katalog_NotSicherheitsbeleuchtung.md) — **Quelle:** elektro-planer knowledge/buecher/k-sibe-at9.pdf (400 S.), via Teil-Digests synthetisiert · **Übernommen:** 2026-08-28
- [Bild-Lehren — Beispiel-Notbeleuchtungspläne (Web-Fundstücke)](knowledge/extracted/bildlehren/Bildlehren_Beispielplaene_Web.md) — **Methode:** Vom Owner gesammelte Beispiel-Visualisierungen aus dem Netz, 2026-08-29
- [Bild-Lehren — EN 1838:2019 + OVE-Fachinfo E-08](knowledge/extracted/bildlehren/Bildlehren_EN1838_E08.md) — **Methode:** Alle Seiten als Bild gesichtet (110 dpi), 2026-08-28. Ergänzt die Text-Digests um die visuellen Konzepte.
- [Bild-Lehren — GSYSTEMS Planungshandbuch 2026/27](knowledge/extracted/bildlehren/Bildlehren_GSYSTEMS.md) — **Methode:** Planungs-Kapitel vollständig als Bild gesichtet (110 dpi), 2026-08-28.
- [Bild-Lehren — INOTEC Handbuch 2026](knowledge/extracted/bildlehren/Bildlehren_INOTEC.md) — **Methode:** Planungs-Kapitel vollständig als Bild gesichtet (110 dpi), 2026-08-28.
- [Bild-Lehren — ABB Kaufel Planungsgrundlagen](knowledge/extracted/bildlehren/Bildlehren_Kaufel.md) — **Methode:** Planungs-Kapitel vollständig als Bild gesichtet (110 dpi), Katalogteil stichprobenartig, 2026-08-28.
- [Bild-Lehren — licht.wissen 10](knowledge/extracted/bildlehren/Bildlehren_LichtWissen10.md) — **Methode:** Bildstarke Seiten gesichtet (110 dpi), 2026-08-28. ~30 Seiten-Views,
- [Bild-Lehren — Zumtobel „Sicherheitsbeleuchtung Österreich"](knowledge/extracted/bildlehren/Bildlehren_ONL_Zumtobel.md) — **Methode:** Alle 48 Seiten als Bild gesichtet (110 dpi), 2026-08-28. Kritische
- [EN 1838:2019 — Angewandte Lichttechnik — Notbeleuchtung](knowledge/extracted/EN_1838_notbeleuchtung.md) — **Quelle:** knowledge/EN 1838 - Notbeleuchtung 2019 (1).pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
- [ESV 2012 — Verordnung über den Schutz der Arbeitnehmer/innen vor Gefahren durch den elektrischen Strom (Elektroschutzverordnung 2012 – ESV 2012)](knowledge/extracted/ESV_2012.md) — **Quelle:** knowledge/esv_2012.pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
- [ETG 1992 — Bundesgesetz über Sicherheitsmaßnahmen, Normalisierung und Typisierung auf dem Gebiete der Elektrotechnik (Elektrotechnikgesetz 1992 – ETG 1992)](knowledge/extracted/ETG_1992.md) — **Quelle:** knowledge/etg_1992.pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
- [ETV — Elektrotechnikverordnung 2002 / 2010 / 2020 (drei Fassungen, gemeinsames Digest)](knowledge/extracted/ETV_2002_2010_2020.md) — **Quelle:** knowledge/ETV_2002.pdf (RIS-Konsolidierung ETV 2002, Fassung vom 30.01.2006, 25 S.) · knowledge/ETV_2010.pdf (RIS-Konsolidierun…
- [Fachinfo E-08 — OVE-Fachinformation E08 „Arbeitsstätten – Ausführung von Sicherheitsbeleuchtung und nachleuchtenden Orientierungshilfen", OVE Österreichischer Verband für Elektrotechnik, Ausgabe 2021-04-01 (Ersatz für Ausgabe 2012-09)](knowledge/extracted/Fachinfo_E08_Arbeitsstaetten.md) — **Quelle:** knowledge/Fachinfo_E-08_Sicherheitsbeleuchtung_Arbeitsstaetten_2021-04.pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
- [Wissens-Digest — Fluchtwegplan-Zimmeraushang (Hotel-Referenzfoto)](knowledge/extracted/FLUCHTWEG_AUSHANG_REFERENZ.md) — Quelle: Referenzfoto Hotel-Zimmeraushang (Elitoria Hotel, Zimmer 1514, „Yangın
- [G-SYSTEMS Planungshandbuch — „Sicherheitsbeleuchtung Planungshandbuch 2026/27 — Technische Regeln, Normen und Gesetze"](knowledge/extracted/GSYSTEMS_Planungshandbuch.md) — **Quelle:** knowledge/Planungshandbuch_Sibe_GSYSTEMS.pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
- [Handbuch zur Sicherheitsbeleuchtung und Dynamischen Fluchtweglenkung 2026 — INOTEC Sicherheitstechnik GmbH, 2026](knowledge/extracted/Handbuch_NotSicherheitsbeleuchtung_2026.md) — **Quelle:** knowledge/101208382_005_Handbuch_NotundSicherheitsbeleuchtung-2026.pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
- [Kaufel Planungshandbuch — „Planungsgrundlagen Sicherheitsbeleuchtung", ABB Kaufel, 6. Auflage (© 2016, Dok-Nr. 460.102.DE.06)](knowledge/extracted/Kaufel_Planungshandbuch.md) — **Quelle:** knowledge/Kaufel Planungshandbuch.pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
- [LB-Analyse — reale Leistungsbeschreibungen → `LBVorgabe`-Contract-Groundwork](knowledge/extracted/LB_ANALYSE_beispiele.md) — **Zweck:** Der 2. Engine-Input (Leistungsbeschreibung) trägt die **expliziten,
- [Lichtberechnungs-Referenz — echte Profi-Notberechnungen (extrahiert 2026-09-08)](knowledge/extracted/LICHTBERECHNUNG_REFERENZ.md) — **Erste echte professionelle Lichtberechnungen mit Zahlenwerten im Repo.** Zwei
- [licht.wissen 10 — Notbeleuchtung, Sicherheitsbeleuchtung (Februar 2016)](knowledge/extracted/LichtWissen_10_Notbeleuchtung.md) — **Quelle:** knowledge/1603_lw10_Notbeleuchtung_web.pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
- [Wissens-Digest — Muthgasse 109B Polierpläne: Brandschutz-Gerüst + 6. CAD-Familie](knowledge/extracted/MUTHGASSE_POLIERPLAN_BRANDSCHUTZ.md) — Quellen: `Projekte/Pläne 19., Muthgasse 109B - 2026-05-07_13-12/Architekt/Ausführungsplan/`
- [Nullungsverordnung — Verordnung über die Anforderungen an öffentliche Verteilungsnetze mit der Nennspannung 400/230 V und an diese angeschlossene Verbraucheranlagen zur grundsätzlichen Anwendung der Schutzmaßnahme Nullung](knowledge/extracted/Nullungsverordnung.md) — **Quelle:** knowledge/Nullungsverordnung (1).pdf (RIS, Bundesrecht konsolidiert, Fassung vom 22.04.2024, 5 S.; StF BGBl. II Nr. 322/1998) ·…
- [ÖNORM E 8014 — OVE E 8014 „Fundamenterder und ergänzende Maßnahmen mit Erdung und Potentialausgleich für Einrichtungen der Informationstechnik" (Ausgabe 2019-01-01)](knowledge/extracted/OENORM_E_8014.md) — **Quelle:** knowledge/ÖNORM E 8014 (1).pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
- [Sicherheitsbeleuchtung Österreich (Normenbroschüre) — Zumtobel Lighting GmbH, 02/2020](knowledge/extracted/ONL_Normen_AT.md) — **Quelle:** knowledge/ONL_Normen_AT.pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
- [OVE E 8015:2022 — Elektrische Anlagen in Wohngebäuden — Art und Umfang der Mindestausstattung sowie zusätzliche Anforderungen an Planung und Errichtung](knowledge/extracted/OVE_E_8015.md) — **Quelle:** knowledge/OVE E 8015_2022 (1).pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
- [OVE E 8101:2019 — Elektrische Niederspannungsanlagen](knowledge/extracted/OVE_E_8101_niederspannungsanlagen.md) — **Quelle:** knowledge/OVE E 8101_2019 (1).pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf; gezielt vertieft: Abschnitte für Sicherheit…
- [OVE E 8350 — Bekämpfung von Bränden in elektrischen Anlagen und in deren Nähe](knowledge/extracted/OVE_E_8350.md) — **Quelle:** knowledge/OVE E 8350 (1).pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
- [OVE E 8351 — Erste Hilfe bei Unfällen durch Elektrizität](knowledge/extracted/OVE_E_8351.md) — **Quelle:** knowledge/OVE E 8351 (1).pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf
- [Platzierungs-Konzepte — die Denkweise hinter der Norm (Engine-Synthese)](knowledge/extracted/PLATZIERUNGS_KONZEPTE.md) — **Zweck:** Nicht *was* die Normen sagen (das steht in den Digests + Regel-Tabellen),
- [Wissens-Digest — Produktsortimente Schrack Technik + DIN Notlicht (Web-Recherche 2026-09-05)](knowledge/extracted/PRODUKTE_SCHRACK_DIN.md) — Quellen: schrack-technik.de / schrack.at (Shop + Know-how-CIP) und din-notlicht.com
- [Wissens-Digest — Profi-DIN-Plan + Vorschriften (extrahiert 2026-08-31)](knowledge/extracted/PROFI_DIN_PLAN_UND_VORSCHRIFTEN.md) — Quellen: echter professioneller Notbeleuchtungsplan `DIN-Notbeleuchtungspläne(Beispiele)/
- [knowledge/extracted — Norm-Digests für die Notbeleuchtungs-Engine](knowledge/extracted/README.md) — Maschinen-orientierte Extraktion der 20 Norm-/Rechts-/Praxis-PDFs aus
- [Standesregeln Elektrotechnik — Verordnung des Bundesministers für Wirtschaft, Familie und Jugend über Standesregeln für das Gewerbe der Elektrotechnik](knowledge/extracted/RIS_Standesregeln_Elektrotechnik.md) — **Quelle:** knowledge/RIS - Standesregeln für das Gewerbe der Elektrotechnik - Bundesrecht konsolidiert, Fassung vom 22.04.2024 (1).pdf (RI…
- [Sicherheitsvorschriften Elektro — „Elektrotechnische Sicherheitsvorschriften als Voraussetzung für den Gewerbezugang", Dipl.-HTL-Ing. Ing. Dietmar Stöger, WIFI Österreich (Wirtschaftskammer), Auflage 4.0 / Juli 2019](knowledge/extracted/Sicherheitsvorschriften_Elektro.md) — **Quelle:** knowledge/Sicherheitsvorschriften_Elektro (1).pdf · **Extrahiert:** 2026-08-28, Volltext via pypdf; vertieft: Notbeleuchtungs-r…
- [Stromkreisnummern-Schema aus dem DIN-Planungsplan (Stromkreisnummer.dwg)](knowledge/extracted/STROMKREISNUMMER_DWG.md) — **Quelle:** `knowledge/sonstiges Wissen Notbeleuchtung/din Planungsunterstützung_Stromkreisnummer.dwg`
- [Wettbewerbsbericht: Endra AI (endra.ai)](knowledge/extracted/WETTBEWERB_ENDRA_AI.md) — Stand: 02.09.2026 · Zweck: Einordnung des Wettbewerbers Endra gegenüber unserer Notbeleuchtungs-Engine (DXF + LB → ÖNorm/EN-1838-konformer…

## Entscheidungen, Vokabular & Koordination (docs)
*ADRs, VOKABULAR, COORDINATION, OFFENE_FRAGEN, PORT_LOG — das WARUM (Begruendungen).*

- [ADR-0001 — Kein Git-LFS](docs/adr/0001-kein-git-lfs.md) — **Status:** bindend · **Datum:** 2026-08-28 · **Owner:** Leonis (User-GO)
- [ADR-0002 — Kanonische Symbol-Library = `CAD_Symbole/Notbeleuchtungssymbole.dxf`](docs/adr/0002-kanonische-symbol-library.md) — **Status:** bindend · **Datum:** 2026-09-05 · **Owner:** Owner-Entscheidung
- [ADR-0003 — Blatt-Modus: das Blatt trägt alles](docs/adr/0003-blatt-traegt-alles.md) — **Status:** bindend · **Datum:** 2026-09-05 (Owner-Fixierung an
- [ADR-0004 — Antipanik-Gleichmäßigkeit Ud = 1:40 (nicht 1:10)](docs/adr/0004-antipanik-ud-40.md) — **Status:** bindend · **Datum:** 2026-09-02 · **Owner:** Enis (von Leonis übernommen)
- [ADR-0005 — Photometrie ohne Ausrichtungs-Zusicherung: Minimum über C](docs/adr/0005-photometrie-minimum-ueber-c.md) — **Status:** bindend · **Datum:** 2026-09-05 (#117, Enis)
- [ADR-0006 — Fluchtweg-SL: `rotation_deg` = Optik-Zusicherung aus der Korridor-Achse](docs/adr/0006-rotation-als-optik-zusicherung.md) — **Status:** bindend · **Datum:** 2026-09-06 (#119, Leonis; adressiert Enis'
- [ADRs — bindende Entscheidungen (nicht neu aufrollen)](docs/adr/README.md) — Kurzform-Architecture-Decision-Records: was entschieden wurde, warum, und was
- [Mollgasse UG — unabhängige Notbeleuchtungs-Referenz aus den GU-Plänen](docs/analyse/mollgasse_ug_notbeleuchtung.md) — **Slice 4.1 (MEGA-Prompt 2026-09-07).** Quelle: GU-Elektro-Grundrisse
- [Contracts — menschenlesbare Spezifikation](docs/CONTRACTS.md) — Code = Wahrheit (`src/notbeleuchtung/hauptengine/contracts/*.py`, Pydantic).
- [COORDINATION — 2-Fenster-Parallelbetrieb](docs/COORDINATION.md) — **Zweck:** Zwei Claude-Code-Sessions arbeiten parallel in getrennten Worktrees. Diese
- [DoD-Sichtprüfungs-Bericht — Mollgasse Notbeleuchtungsplan (8 Geschosse)](docs/DOD_GEBAEUDE_MOLLGASSE.md) — **NEIN — das Gebäude-Plan-Set ist nicht auslieferbar.** Kein einziges der 8 Geschosse ist abnahmefähig. Zwei strukturelle Ursachen dominier…
- [DoD-Sichtprüfung — Real-Plan Mollgasse EG](docs/DOD_SICHTPRUEFUNG.md) — **Stand:** 2026-08-31 · **Prüfer:** Leonis (F1) · **Fall:** `Projekte/Mollgasse/Erdgeschoß.dxf`
- [0001 — Raumerkennung: Sprache (Python bleibt) + ML-Strategie](docs/entscheidungen/0001-raumerkennung-sprache-python-und-ml.md) — **Status:** angenommen · **Datum:** 2026-08-30 · **Betrifft:** Selman
- [Infrastruktur — Entscheidung (Stand 2026-08-27)](docs/INFRASTRUKTUR.md) — **Leitsatz:** Infra folgt der Phase, nicht dem Hype. Solange die Engine gebaut
- [Hauptengine in eine eigene App integrieren](docs/INTEGRATION.md) — Für Host-/Demo-Apps, die die Notbeleuchtungs-Engine aufrufen wollen (Raumerkennung +
- [Plan Barawitzka_EG](docs/MATERIAL_REPORT.md) — <!-- generiert von scripts/plan_pruefen.py — nicht von Hand pflegen -->
- [Normquellen-Status (Enis) — was liegt vor, was ist belegt, was fehlt](docs/NORMQUELLEN_AT.md) — **Stand:** 2026-08-30 · Bestandsaufnahme rein lesend aus `knowledge/`.
- [Offene Fragen — Plan-Befunde & Regel-Lücken](docs/OFFENE_FRAGEN.md) — Sammelstelle für Befunde, die eine Owner-Entscheidung brauchen. Regel-Lücken
- [OIB-Richtlinie 2 — Punkt 5.4 + Tabelle 6 (Erforderlichkeit Sicherheitsbeleuchtung)](docs/OIB_RL2_TABELLE6.md) — **Analysiert:** 2026-08-30 (Enis) · **rein lesend aus den Original-PDFs**, nichts aus
- [Onboarding — Start hier (Selman · Leonis · Enis)](docs/ONBOARDING.md) — Ihr arbeitet **alle drei gleichzeitig** in eurem eigenen Package. Dank
- [Placement-Decision-Matrix — Notbeleuchtung](docs/PLACEMENT_DECISION_MATRIX.md) — Die Engine wusste bisher zwei Dinge:
- [PORT_LOG — Herkunft der aus `elektro-planer` portierten Module](docs/PORT_LOG.md) — Quelle: `github.com/mvpo3/MVP-Planer` (lokal `../elektro-planer`), Branch `mvp-main`.
- [Programm-Board „Notbeleuchtung" — lebender Status (Single Source of Truth)](docs/PROGRAMM_NOTBELEUCHTUNG.md) — **Start:** 2026-08-27 · Board gewinnt bei Drift gegen GitHub-Projects. Jeder Owner
- [Blocker 2 — Scope-Gate der Flächen-Schwellen, je Schwelle getrennt](docs/proposals/BLOCKER2_FLAECHEN_SCOPE.md) — **Einzige Änderung 2019 → 2025 an dieser Stelle:** in Punkt 1) heißt es statt
- [Vorschlag — Quellen-Naht für Sonderstellen (Umsetzung von SPEC §8)](docs/proposals/SONDERSTELLEN_QUELLEN_NAHT.md) — Eine Pflicht-Leuchte an einer Sonderstelle trägt heute die `quelle` der
- [Wegbreite > 2 m und Randstreifen — Befund und Anschlussvorschlag](docs/proposals/WEGBREITE_RANDSTREIFEN.md) — Drei Punkte, die auseinandergehalten werden müssen:
- [Spec — ProjektKontext + OibErgebnis (Enis → Leonis)](docs/SPEC_PROJEKTKONTEXT_OIB.md) — **Absender:** Enis (`src/notbeleuchtung/normwissen/`) · **Adressat:** Leonis (Owner
- [Spec — Sonderstellen im `RaumModell` (Contract-Vorschlag)](docs/SPEC_SONDERSTELLEN_CONTRACT.md) — EN 1838 §4.1.2 verlangt, dass bestimmte **Stellen** hervorgehoben werden — jeder
- [Stempel-Report — Projekte/_eingang](docs/STEMPEL_REPORT.md) — Erzeugt mit `scripts/stempel_report.py` am 2026-09-05.
- [Vokabular — kanonische Begriffe der 3-Owner-Naht](docs/VOKABULAR.md) — Antwort auf die offene COORDINATION-Frage *„Wo ist die Liste kanonisch?"*:

## Handoffs (Owner-Sessions)
*Rollen, Packages, Contracts, Slice-Stände je Owner.*

- [Handoff — Enis (Normwissen + LB)](Handoff/ENIS.md) — 1. **`origin/main` = `1092d77`.** (Der frühere Stand `5e4a46e` steht weiter unten
- [Handoff — Leonis (Platzierung + Integration)](Handoff/LEONIS.md) — **Enis' gemeinsame L1/L3-Fassung reviewt** (Commit `8801aa6`, Branch
- [Handoff — Perfekter Start je Owner](Handoff/README.md) — Jeder von euch arbeitet in einer **eigenen Claude-Code-Session im Repo-Ordner**.
- [Handoff — Selman (Raumerkennung)](Handoff/SELMAN.md) — Du bist ein Agent — **führe diese Schritte selbst aus**, frag nicht lang nach.
- [SYNC — Stand nachziehen, ohne Arbeit zu verlieren](Handoff/SYNC.md) — **Auslöser:** Der Owner schreibt in seiner Session **„Sync"** (oder „GitHub wurde
