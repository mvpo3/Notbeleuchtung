# Wettbewerbsbericht: Endra AI (endra.ai)

Stand: 02.09.2026 · Zweck: Einordnung des Wettbewerbers Endra gegenüber unserer Notbeleuchtungs-Engine (DXF + LB → ÖNorm/EN-1838-konformer Notbeleuchtungsplan).

**Vorab-Klarstellung Identität:** Das relevante Unternehmen ist **Endra Systems AB** („Endra" / „Endra AI"), ein **schwedisches** Startup (Sitz Stockholm) unter der Domain **endra.ai**. Es ist **nicht** aus dem DACH-Raum (Deutschland ist nur Expansions-/Beta-Markt) und **nicht** zu verwechseln mit ENDRA Life Sciences (US-Medizintechnik, endrainc.com) oder Endava. Alle Produkt-, Presse- und Funding-Quellen beziehen sich konsistent auf das schwedische MEP-AI-Startup.

---

## 1. Wer ist Endra AI — Identität, Team, Funding, Reife

### Identität und Team (belegt)
- **Firma:** Endra Systems AB, Hauptsitz Stockholm (Östermalm); weitere Standorte laut Stellenanzeigen/Presse: Malmö, London, New York (NA-HQ), San Francisco.
- **Gründer:** Niklas Lindgren (CEO), Anton Juric (COO) — beide Serial Entrepreneurs aus Security/technischer Infrastruktur (u. a. Startup „Sectragon", Kindheitsfreunde) — sowie Gustav Hammarlund und David Rydberg (Technical Co-Founders, zuvor kritische Infrastruktur für Goldman-Sachs-Aktienhandelsplattformen EMEA). Bemerkenswert: **kein CAD/TGA-Domänenhintergrund im Gründerteam**; der Gründungsimpuls kam über Lindgrens Vater (Architekt), der den manuellen MEP-Prozess als Flaschenhals beschrieb.
- **Mission:** „The AI-powered MEP platform" — „Generate your models & documents. At the click of a button." Automatisierung der MEP-Planung (Mechanical/Electrical/Plumbing) für Gebäude.

### Widersprüchliche / unsichere Angaben (explizit markiert)
- **Gründungsjahr — WIDERSPRÜCHLICH:** SiliconANGLE sagt „late 2024", builtin.com-Stellenanzeigen und ein Forbes-/Vestbee-Snippet sagen **2023**. Das Norrsken-Investmentmemo (Mai 2025) spricht von „eight months of operation" → operativer Start ~Herbst 2024 ist am plausibelsten; 2023 könnte formale Firmengründung oder Teamstart sein. **Nicht abschließend geklärt.**
- **Teamgröße — schnell wachsend, Quellen divergieren je nach Zeitpunkt:** ~10 Mitarbeiter (Dez 2025, SiliconANGLE), 23 (30.04.2026, Tracxn), 28 (builtin-Stellenanzeigen, ~Aug 2026). Verdreifachung binnen eines Jahres angekündigt; ~14 offene Stellen (Stand Sept 2026).
- **Modul-Status Lighting/Containments — INKONSISTENT:** verschiedene Website-Snapshots listen Lighting/Containments teils als „Live", teils als „Coming Soon" (siehe Abschnitt 2). Vermutlich Early-Access-Grauzone; **Status unsicher**.

### Funding und Reife (belegt)
- **€3 Mio. Pre-Seed** (Mai 2025, Norrsken VC; Angels u. a. Max Viessmann, Epidemic-Sound-Gründer).
- **$20 Mio. Seed** (Dez 2025, Lead Notion Capital, mit Norrsken VC + Angels) — einer der größten schwedischen Seeds.
- **$50 Mio. Series A** (~Juni 2026, Lead **Andreessen Horowitz**, mit Notion Capital und Norrsken VC).
- **Gesamt: ~$75 Mio. in unter zwei Jahren.** Bewertung nicht offengelegt.
- **Traktion (überwiegend Eigenangaben):** Produkt-Launch August 2025; Warteliste 600+ Firmen aus 90+ Ländern; ~30 Enterprise-Kunden; Pilot-/Referenzkunden AtkinsRéalis, Buro Happold, Hoare Lea, Ramboll, Tetra Tech, Rejlers; **offizielle AFRY-Partnerschaft** (Pressemitteilung 23.04.2026, Elektro- + Brandschutzplanung, v. a. frühe Projektphasen, laufend „throughout Endra's development phase" — d. h. Produkt noch in Entwicklung, AFRY als Pilot-/Evaluierungspartner). Claims wie „100 % Pilot-zu-Paid-Konversion", „min. 12x Effizienz", „10 Wochen Scope in 8 Stunden" sind **self-reported, nicht unabhängig verifiziert**.
- **Reife-Einschätzung:** enorm gut finanziert, aber öffentlich dünne Produkt-Substanz (Resources-Seite hat nur 2 Artikel, Case Study enthält noch Lorem-ipsum-Platzhalter, /pricing liefert 404). Ein Modul (Fire Alarm) ist live, das zweite (Electrical) wird erst am **14.09.2026** auf dem eigenen Event „Epoch" (AREA15, Las Vegas, Vorabend der Autodesk University; Speaker u. a. Garry Kasparov, Johnson-Controls-CEO) enthüllt.

---

## 2. Produkt im Detail

### Gewerke / Module
| Modul | Status | Inhalt |
|---|---|---|
| **Fire Alarm** (Brandmeldeanlagen) | **Live** (seit ~Aug 2025) | Automatische Geräteplatzierung, Kabelrouting, Zonenpläne, Riser-Diagramme, Berechnungen |
| **Electrical** | Early Access; offizieller Launch 14.09.2026 (Epoch, Las Vegas) | Stromkreise, Kabeldimensionierung, Schedules, Spannungsfall |
| **Containments & Conduits** | Status inkonsistent (Live/Early) | 3D-Trassen-/Leerrohrmodelle |
| **Lighting Systems** | Status inkonsistent (Live/Coming Soon je nach Snapshot) | „Instant lighting concepts", 2D/3D + integrierte Berechnungen |
| HVAC, Plumbing/Sprinkler, Data & Fibre, Security, Access | Coming Soon | angekündigt „within the next year" (HVAC/Plumbing) |

**Zentral für uns: Notbeleuchtung / EN 1838 / EN 50172 / ÖNorm wird NIRGENDS erwähnt** — weder als Modul noch in Resources noch in Presse. Gezielte Suchen (endra + emergency lighting / Notbeleuchtung / EN 1838) liefern keine Treffer. Nächste Nachbarn: das Lighting-Modul, „Battery Calculations" im Fire-Alarm-Output und das Fire-Safety-Feld der AFRY-Partnerschaft. Naheliegend, dass Notbeleuchtung mit Electrical/Lighting irgendwann kommt — **das ist aber Spekulation, unbelegt.**

### Inputs
- **Datei-Upload per Drag-and-drop: IFC, DXF (DWG), PDF** (Fire-Alarm-Seite wörtlich).
- **Revit nativ** über eigenes Add-in, inkl. privater Revit-Familien / gehosteter Familienbibliotheken pro Kunde.
- Projektdaten + Code-/Normauswahl + „human-like Q&A input" (dialogbasierte Konfiguration: Routing-Präferenzen, No-Go-Zonen, Gebäudeparameter).
- Importierbare Kabeltrassen-Modelle zur Steuerung des Routings.
- **Wichtig:** Primärer Input ist ein **3D-Architekturmodell mit BIM-Semantik** (IFC/Revit) — nicht ein leerer 2D-Plan wie bei uns. Ein expliziter zweiter Text-Input à la Leistungsbeschreibung (LB) ist **nicht dokumentiert**; die LLMs lesen laut Presse aber „building specifications and regulatory documents" — funktional verwandt, Details unbelegt.

### Outputs
- Export: **DXF (DWG), PDF, RVT (3D), IFC (3D)** („robust export engine").
- Dokumenttypen (Case Study, 9 Stück): Shop Drawings, Riser-Diagramme, Wiring-Diagramme, Lastberechnungen, **Batterieberechnungen**, Spannungsfall-Berechnungen, Zonenpläne, Produktmatrix, Sequence of Operations. Dazu automatische Naming-Conventions und Schedules/Listen.

### Workflow (6 Stufen, Fire Alarm)
1. Projektdaten-/Info-Input → 2. Modell-Upload & Review → 3. automatische Geräteplatzierung („analyze your building and code, and place all your units... within seconds") → 4. Zone Mapping (normkonforme Zonenpläne) → 5. Cable Routing (KI-Pfadoptimierung, konfigurierbare No-Go-Zonen) → 6. Dokumentations-Export. Danach optional Übergabe nach Revit via Add-in (Family-Mapping-Grid, Objekte inkl. MEP-Konnektoren, Koordinaten/Level/Orientierung). **„Chat-to-CAD" / „Human Language to CAD" ist als Feature angekündigt** — das ist die direkte Konkurrenz zu unserem Chat-Interface-Nordstern.

### Was manuell bleibt (Engineer-in-the-Loop)
Q&A-Konfiguration, finales Review + Freigabe; nach Revit-Import Konnektivitäts-Prüfung, Clash-Detection, Parameter-Validierung, Nachjustieren falsch platzierter Elemente. Positionierung explizit „firmly in the loop", keine Black Box; Anspruch bis RIBA Stage 4 (technische Ausführungsplanung).

### Normen-Abdeckung
Fire Alarm: **SBF 110:8 (SE), NFPA 72 (US), BS 5839 (UK), DIN 14675 (DE)** — DIN/Deutschland ist also bereits abgedeckt, EU/UK/US in Beta. **ÖNorm/OVE/Österreich und EN 1838 werden nirgends erwähnt.** Plattform derzeit nur auf Englisch.

### Preismodell / Go-to-Market
Kein öffentliches Pricing (**/pricing → HTTP 404**); Zugang nur über „Request Access"-Formular (Firma, Land, Größe 1–10 bis 1000+, relevante Systeme) → Sales-geführtes Enterprise-B2B, Zielkunden sind große Ingenieurbüros/Design-Build-Firmen. Fokus große Gewerbeprojekte (Referenz: 185.000-m²-Logistikzentrum; 500.000-sq-ft-Elektroplanung), nicht Wohnbau/kleinere DACH-Einreichprojekte.

### Flagship-Case (Eigenangabe, mit konkreten Zahlen)
185.000-m²-Logistikzentrum Schweden, BMA Klasse A, **2.758 Komponenten** (2.130 Rauchmelder, 185 Wärmemelder, 96 I/O, 343 Handmelder, 4 Anzeigen). Berater **304 h vs. Endra 0,5 h** (~600x): Platzierung 89 h→6 min, Routing 82 h→12 min, Riser 28 h→30 s, Zonenpläne 44 h→2 min. Qualitätsmetrik: **98,8 % Übereinstimmung der automatischen Platzierung mit dem manuellen Referenzentwurf** — nicht unabhängig geprüft, aber methodisch interessant (Benchmark gegen menschlichen Golden-Standard).

---

## 3. Technik-Stack + Methodik

Quellen: primär Stellenanzeigen (builtin.com, Norrsken-Jobboard) + Presse-Interviews (Fortune, SiliconANGLE, AEC Business). **Keine öffentliche API-Doku, keine Whitepaper, keine Patente auffindbar; GitHub-Org `endra-ai` existiert, hat aber 0 öffentliche Repos/Member — vollständig closed-source.**

### Stack (aus Stellenanzeigen, belegt)
- **Core-Engine: C++23**, von Grund auf neu — geometrische Primitiven, „advanced optimization algorithms", MEP-Entscheidungs-/Validierungslogik.
- **Backend: leichtgewichtige asynchrone Python-API auf GCP, Postgres**; generiert Reports und bindet die C++-Library an (C++/Python-Interop via Bindings/Embedding als Job-Anforderung).
- **Frontend: eigene In-Browser-CAD-Applikation** aus Svelte + Custom-TypeScript + **WebAssembly** (vermutlich der C++-Core als WASM; „vermutlich" = unsere Schlussfolgerung, nicht belegt). Kein Desktop-CAD.
- **BIM-Schicht: Revit-Add-ins in C#/.NET** (5+ Jahre gefordert; Families, Parameters, Worksharing, Schedules, WPF, Autodesk Platform Services); IFC/OpenBIM-Export auf Roadmap, heute Revit-nativ.
- Sicherheit: AES-256-GCM in transit + at rest, Trust Center (trust.endra.ai), Statuspage; explizit **kein Training auf Kundendaten**.

### Methodik: ML vs. Regeln (Kernbefund)
Der Algorithmus-Kern ist **klassische Informatik, nicht Deep Learning**: Die Optimization-Rolle verlangt Graphenalgorithmen, kombinatorische Optimierung, Computational Geometry (2D/3D), Kollisionserkennung, 3D-Placement und Routing — **in keiner Engineering-Stellenanzeige tauchen PyTorch/TensorFlow oder eine ML-Engineer-Rolle auf**. Die Presse-Darstellung ist ein Hybrid:
1. **LLMs** interpretieren „architectural intent" und bauen Kontext aus Regulierungs-/Spezifikationsdokumenten auf — CEO-Zitat: LLMs helfen „identify room types, identify objects" und zu verstehen, „how the architect thinks this building should be used" → **LLM-basierte Raumtyp-/Objekt-Klassifikation** als Verständnisschicht (Analogon zu unserer `classify_room` + LB-Parsing).
2. **Deterministische Optimierungs-/„ML"-Modelle** lösen „hard optimisation problems" im 3D-Raum (Platzierung, Routing) — Investor-Zitat Notion Capital: „not your regular AI company building on top of foundational models... solving hard optimisation problems using deterministic ML models"; Positionierung „spatial AI, physics, and deterministic algorithms rather than generative guessing".
3. **3D-Simulation** + proprietäre Geometry-Engine + **eigenes granulares 3D-Datenmodell** als Single Source of Truth („from receptacle to transformer") — bewusst KEIN Revit-Plugin als Kern, weil laut Lindgren „Revit's underlying data model is too coarse to support deep automation"; Revit wird zur „Orchestration Layer" degradiert.

### Wie sie Pläne „parsen" (Einordnung)
Endra muss deutlich weniger Geometrie-Erkennung leisten als wir: Der IFC/Revit-Input liefert Räume, Türen, Ebenen und Semantik weitgehend mit; das LLM klassifiziert Raumtypen/Nutzung. Wie DXF- und PDF-Inputs konkret verarbeitet werden (Vektor-Parsing? Raster? OCR?), ist **nirgends dokumentiert**. Ein Audit-Trail-Konzept (Entscheidungsquelle je Platzierung wie unser `norm_quelle`) wird **nirgends erwähnt**.

---

## 4. Vergleich mit unserer Engine

| Dimension | Endra | Wir (Notbeleuchtung) |
|---|---|---|
| **Vertikale** | Ganzes MEP; live nur Fire Alarm (+ Electrical im Launch); **keine Notbeleuchtung, kein EN 1838** | Genau eine Vertikale: Notbeleuchtung nach EN 1838/EN 50172/ÖNorm (RZ + SL + Antipanik) |
| **Primär-Input** | 3D/BIM-first: IFC, Revit (nativ), dazu DXF(DWG) + PDF; Semantik kommt großteils aus dem Modell | 2D-DXF-first: leerer Architekturplan, eigene Raumerkennung aus nackter Vektorgeometrie |
| **Zweiter Input (Spec)** | Kein dokumentiertes LB-Konzept; LLMs lesen „specifications/regulatory documents" (Details unbelegt); Q&A-Dialog zur Konfiguration | Explizite Leistungsbeschreibung → `LBVorgabe`-Contract mit bindender Override-Hierarchie (LB > Referenz > Norm-Default > OVE-Hard-Stop) |
| **Normwissen** | Pro Region hinterlegt (SBF 110:8/NFPA 72/BS 5839/DIN 14675); ÖNorm fehlt | YAML-Wissensbasis (`normwissen/data`), EN 1838/ÖNorm, versioniert |
| **Audit-Trail** | „Code compliance" als Versprechen; Entscheidungsquellen je Element nirgends erwähnt | Jede Platzierung trägt `norm_quelle`/`lb_quelle` — nachvollziehbarer Einzelnachweis |
| **Kern-Methodik** | Hybrid: LLM-Verständnisschicht + deterministische Geometrie/Optimierung (C++23, Graphen, Combinatorial Opt., Kollision) + 3D-Simulation | Deterministisch: Python, Pydantic-Contracts, numpy/NetworkX-Geometrie/Graphen, regelbasiert |
| **Output** | DXF/DWG, PDF, RVT, IFC + 9 Doku-Typen (Riser, Batterie-/Spannungsfall-Berechnung, Zonenpläne, Produktmatrix...) | DXF + matplotlib-PDF, Lux-Nachweis, Stromkreis-Belegungsliste (DL/BL), Höhenkoten |
| **UI** | Eigener Browser-CAD-Editor (Svelte/TS/WASM, Drag&Drop-Nachbearbeitung) + Revit-Add-in; Chat-to-CAD angekündigt | Kein UI, nur FastAPI `POST /plan`; Chat-Interface ist unser Nordstern |
| **Symbol-/Produktkatalog** | Private Revit-Families + gehostete Familienbibliotheken pro Kunde, Family-Mapping-Grid | Eine Schrack-Library (`E-Symbole.dxf`) + `schrack_symbol_mapping.yaml`; keine Hersteller-Photometrie |
| **Team/Architektur** | ~28 Personen, C++/Python/TS/C#-Multistack, Cloud (GCP) | 3 Owner, Plugin-Modell (Ports & Adapters), Contract-Freeze, Fake-Provider-first |
| **Zielmarkt** | Enterprise-Ingenieurbüros (AFRY, Ramboll...), Großprojekte (Logistik, 500k sq ft), SE/UK/US + DE-Beta | AT/DACH, Wohn-/Bestandsprojekte (Muthgasse/Mollgasse), ÖNorm-Einreichpraxis |
| **Validierung** | Benchmark gegen manuellen Referenzentwurf (98,8 % Match), self-reported | Golden-Fixtures, DoD-Harness, Contract-Drift-Gate, E2E auf echten Plänen |
| **Funding/Risiko** | $75M, a16z — kann jede Vertikale schnell nachbauen, sobald priorisiert | 0 externes Kapital, aber tiefe Nische, die Endra öffentlich (noch) nicht besetzt |

**Fazit Bedrohungslage:** Keine direkte Produkt-Überschneidung heute — Notbeleuchtung/EN 1838/ÖNorm ist bei Endra öffentlich nicht existent. Aber das Muster ihres Fire-Alarm-Moduls (code-getriebene Platzierung + Zonierung + Kreisverkabelung + Berechnungsnachweise) ist **exakt dasselbe Muster wie unsere Engine, nur ein anderes Gewerk** — mit Lighting + Electrical im Anlauf und $75M ist Notbeleuchtung für Endra ein plausibler nächster Schritt. Unser Zeitfenster-Vorteil: ÖNorm/Österreich, LB-Override-Hierarchie mit Audit-Trail, 2D-DXF-Realität kleiner DACH-Projekte (Endra ist BIM-first — genau die Projekte OHNE sauberes IFC-Modell sind ihr blinder Fleck und unser Terrain).

---

## 5. Was wir konkret übernehmen können (priorisiert)

**P1 — Qualitätsmetrik „% Übereinstimmung mit Referenzplan" (S, hauptengine + platzierung).** Endras 98,8-%-Match gegen den manuellen Beraterentwurf ist ihre stärkste Verkaufszahl. Wir haben mit dem Profi-Barawitzkagasse-Plan und dem DoD-Harness bereits das Material: einen automatisierten Vergleich „unsere Platzierung vs. Profi-DIN-Plan" (Treffer innerhalb Toleranzradius, fehlend, überzählig) als Score in den DoD-Harness einbauen und als Case-Study-Zahl dokumentieren. Kleinster Aufwand, größter Glaubwürdigkeits- und Marketing-Hebel.

**P2 — No-Go-Zonen als Contract-Feld (S/M, hauptengine/contracts + platzierung).** Endras konfigurierbare No-Go-Zonen für Routing/Platzierung sind ein simples, praxisnahes Feature (Wandflächen mit Vitrinen, denkmalgeschützte Decken, Kundenwunsch aus der LB). Bei uns: optionales `no_go_zonen: list[Polygon]`-Feld (aus LB oder API-Parameter), das der Platzierer als harte Ausschlussflächen respektiert. Achtung: Contract-Änderung → 3-Owner-Approval + Version-Bump.

**P3 — Batterie-/Autonomie-Berechnung als Output-Dokument (M, platzierung + normwissen).** Endra liefert Battery Calculations und Spannungsfall standardmäßig mit. Für Notbeleuchtung ist das fachlich zwingend (EN 50172: Bemessungsbetriebsdauer 1 h/3 h, Einzelbatterie vs. Zentralbatterie/CPS): pro Stromkreis Leuchtenanzahl × Leistung × Betriebsdauer aus dem NormRegelwerk/der LB → Belegungsliste erweitern. Wir haben mit der DL/BL-Stromkreis-Belegungsliste schon die halbe Infrastruktur; Enis liefert die Normwerte (Betriebsdauer steckt teils schon im LB-Parser).

**P4 — LLM-Raumtyp-Klassifikation als Fallback-Provider (M, raumerkennung; Schnitt über bestehenden Port).** Endras CEO benennt exakt unsere Schwachstelle als LLM-Use-Case: „identify room types, identify objects". Unsere Layer-Regex-/Token-Klassifikation (`classify_room`) versagt bei fremden CAD-Konventionen (Mollgasse-Problem). Ein optionaler LLM-Fallback (Raumtext + Kontext → Raumtyp-Enum), nur wenn die deterministische Klassifikation UNKNOWN liefert, mit `quelle="llm_fallback"` im Audit-Trail und Review-Flag — deterministischer Kern bleibt, Coverage steigt. Passt in Selmans RaumProvider ohne Contract-Änderung.

**P5 — Kunden-Symbolbibliotheken statt Schrack-only (M, hauptengine + normwissen).** Endras „private families / hosted family libraries" pro Kunde ist der richtige Ansatz gegen unsere Hersteller-Bindung: `schrack_symbol_mapping.yaml` zu einem austauschbaren Katalog-Mapping pro Projekt/Kunde verallgemeinern (Katalog-Datei als Input neben Plan + LB; LB-Regel „Produkte des Herstellers X" greift dann direkt). Die Contract-Invariante `catalog_key ∈ mapping` bleibt, nur die Mapping-Quelle wird parametrisierbar.

**P6 — Q&A-/Rückfragen-Schritt vor der Generierung (M, hauptengine + normwissen/lb).** Endras „human-like Q&A input" löst das Problem unterspezifizierter Inputs. Bei uns existiert mit `LbReviewRequired` bereits der Fail-Closed-Mechanismus — Ausbau zur strukturierten Rückfrage-Liste (fehlende Betriebsdauer? Gebäudeklasse? Zentralbatterie ja/nein?) als API-Response, die das künftige Chat-Interface direkt als Dialog rendern kann. Das ist unser natürlicher Weg zu „Chat-to-CAD", ohne LLM im Platzierungspfad.

**P7 — IFC als zweiter Input-Pfad (L, raumerkennung, Roadmap).** Endras BIM-first-Vorteil: IFC liefert Räume/Türen/Ebenen semantisch frei Haus. Ein `IfcRaumProvider` (z. B. via IfcOpenShell) hinter demselben `RaumProvider`-Port würde unsere größte Schwäche (Raumerkennung nur auf wenige CAD-Konventionen kalibriert) für alle Projekte MIT Modell umgehen — der DXF-Pfad bleibt für den DACH-Bestand. Großer Brocken, aber sauber durch unser Plugin-Modell abgedeckt; erst nach Stabilisierung des DXF-Pfads (Owner-Entscheidung Selman). Der frühere IFC-Spike (PR #9-Umfeld) ist der Startpunkt.

**P8 — „Zonenplan"-artiges Übersichtsdokument (S, platzierung/Render).** Endras Code-Compliant Zone Maps (Feuerwehr-Orientierungspläne) haben ein direktes Notlicht-Pendant: eine Übersichtsseite pro Geschoss mit Stromkreis-Färbung, Leuchten-Anzahl je Kreis und Norm-Nachweisen als zusätzliche PDF-Seite aus vorhandenen Daten (NODEID, Belegungsliste, Lux-Nachweis existieren schon).

**P9 — Zeitmessungs-Case-Study nach Endra-Muster (S, docs).** „304 h vs. 0,5 h" mit Tätigkeits-Tabelle ist kommunikativ brillant. Für Mollgasse/Muthgasse dieselbe Tabelle aufsetzen (manuelle Notlicht-Planung je Schritt geschätzt/erhoben vs. Engine-Laufzeit) — kostet fast nichts, weil die Pipeline-Schritte 1:1 auf Endras 6 Stufen mappen.

---

## 6. Was wir bewusst NICHT kopieren sollten

1. **C++-Core / Rewrite für Performance.** Endra braucht C++23+WASM für 3D-Kollisionsrouting über 185.000 m² im Browser. Unser 2D-Problem (Platzierung + Sichtlinien + Raster) läuft in Python/numpy in Sekunden; ein Rewrite würde das 3-Owner-Team monatelang binden, ohne ein einziges Kundenproblem zu lösen.
2. **Eigener Browser-CAD-Editor.** Svelte/TS/WASM-CAD ist ein Mannjahre-Projekt und Endras Antwort auf „Engineering-Teams arbeiten interaktiv im Modell". Unser Nordstern ist bewusst dünner: Chat-Hülle über `POST /plan`, Output ist der fertige DXF/PDF-Plan. Interaktive Nachbearbeitung passiert beim Kunden im CAD — das ist Feature, nicht Lücke.
3. **BIM-first-Pivot (Revit/eigenes 3D-Datenmodell als Kern).** Endras These „Revit zu grob → eigenes granulares 3D-Modell" ist für Voll-MEP richtig; wir haben das strukturelle Äquivalent längst (eigene Contracts/RaumModell statt CAD-nativer Strukturen). Unser Markt (österreichische Bestands-/Wohnprojekte) hat mehrheitlich KEIN sauberes BIM-Modell — 2D-DXF-first ist unsere Differenzierung, nicht unser Rückstand. IFC nur als zusätzlicher Provider (P7), nie als Ersatz.
4. **LLM im Platzierungs-/Compliance-Pfad.** Selbst Endra hält den Entscheidungskern deterministisch („deterministic algorithms rather than generative guessing"). Für uns kommt dazu: Unser Audit-Trail (`norm_quelle` je Platzierung) und die Haftungsrealität (Planer stempelt und haftet persönlich — von Beobachtern als DIE Adoptionshürde der Branche genannt) verbieten nicht-reproduzierbare Entscheidungen. LLM ausschließlich als Verständnisschicht mit Review-Flag (P4/P6).
5. **Gated-Enterprise-Vertrieb / Intransparenz (404-Pricing, 2 Resources-Artikel, Platzhalter-Content).** Bei $75M-Funding verzeiht der Markt das; bei uns wäre verifizierbare Offenheit (nachvollziehbare Norm-Nachweise, reproduzierbare Benchmarks) das Gegen-Asset gegen „viel Funding, wenig verifizierbare Tiefe".
6. **Breite vor Tiefe (7+ Gewerke parallel ankündigen).** Endras „Coming Soon"-Wand funktioniert als Fundraising-Story. Für 3 Owner gilt das Gegenteil: Die eine Vertikale (Notbeleuchtung ÖNorm) vollständig, auditierbar und auf echten Plänen robust — genau dort, wo Endra nichts hat.

---

## 7. Quellenliste (URL je Kernaussage)

| Kernaussage | Quelle |
|---|---|
| Positionierung, Module (Live/Coming Soon), Import/Export-Formate, Normenliste (SBF 110:8/NFPA 72/BS 5839/DIN 14675), AES-256-GCM, kein Training auf Kundendaten, Revit-nativ, nur Englisch | https://www.endra.ai/ |
| Fire-Alarm-Features, IFC/DXF(DWG)/PDF-Upload, automatische Platzierung/Routing, Q&A-Input, Human Language to CAD, Zone Maps, Riser, Cloud-Vergleichstabelle | https://www.endra.ai/product/fire-alarm |
| Case Study 304 h vs. 0,5 h, 185.000 m², 2.758 Komponenten, 98,8 % Match, 9 Dokumenttypen, 6-Stufen-Workflow, Platzhalter-Content | https://www.endra.ai/resources/300-hours-vs-30-minutes-the-power-of-Endra |
| Revit-Add-in, Family-Mapping-Grid, MEP-Konnektoren, manuelle QA-Schritte nach Import | https://www.endra.ai/resources/endra-revit-addin-help |
| $20M Seed (Notion Capital), Gründung „late 2024", ~10 MA, Warteliste 600+/90+ Länder, LLM+ML+3D-Simulation+deterministische Algorithmen, Expansion US/UK/DE | https://siliconangle.com/2025/12/19/endra-secures-20m-automate-mechanical-electrical-plumbing-design-construction/ |
| Hybrid-KI-Architektur, proprietäre Geometry-Engine, 500k-sq-ft-Claim, Seed-Details | https://fortune.com/2025/12/18/endra-ai-startup-automating-mep-design-sweden-20-million-seed-round-notion-capital/ |
| $50M Series A (a16z), Kundenliste AtkinsRéalis/Buro Happold/Hoare Lea/Ramboll/AFRY, „spatial AI + Physik + deterministische Algorithmen", Haftungs-/Adoptions-Kritik, „$75M gesamt" | https://bricks-bytes.com/ai/andreessen-horowitz-just-put-50m-into-endra/ · https://www.axios.com/pro/enterprise-software-deals/2026/06/01/endras-engineer-buildings-ai |
| AFRY-Partnerschaft (23.04.2026), Elektro + Fire Safety, frühe Projektphasen, Produkt noch in Entwicklungsphase | https://afry.com/en/newsroom/press-releases/afry-partners-endra-ai-in-building-design |
| Eigenes granulares 3D-Datenmodell, „Revit too coarse", RIBA Stage 4, Electrical-Launch 14.09. Las Vegas, Series A | https://aec-business.com/endra-rethinks-mep-design-with-ai/ |
| Gründerquartett, Goldman-Sachs-Hintergrund, €3M Pre-Seed, Angels (Viessmann u. a.), „8 Monate operativ" (Mai 2025), 70x-Claim | https://www.norrsken.vc/post/endra · https://tech.eu/2025/05/28/ai-startup-endra-secures-eur3m-funding-to-transform-outdated-mep-market/ |
| Tech-Stack: C++23-Core, Python/GCP/Postgres, Svelte/TS/WASM-Browser-CAD, C#/.NET-Revit-Add-ins, Graphen/kombinatorische Optimierung/Computational Geometry, „gegründet 2023, 28 MA" | https://builtin.com/job/software-engineer-core/9727916 · https://builtin.com/job/software-engineer-optimization/9727913 · https://builtin.com/job/bim-engineer/9727944 · https://jobs.norrsken.org/companies/endra/jobs/76472549-software-engineer-product |
| GitHub-Org leer (closed-source) | https://github.com/endra-ai |
| Epoch-Event 14.09.2026 (AREA15, Las Vegas) | https://www.endra.ai/epoch |
| Teamgröße 23 (Apr 2026) | https://tracxn.com/d/companies/endra/__f1yiUY0tQymjEwuAbbXdE9YaGCYKyCofVWxq9cLomDA |
| Expansion NY/SF/London | https://www.citybiz.co/article/882274/endra-expands-to-new-york-san-francisco-and-london/ |
| Wettbewerber Augmenta/Consigli(→AECOM)/ArchiLabs; DIALux als manueller Notlicht-Standard | https://aecmag.com/mep/agentic-ai-accelerates-electrical-design/ · https://www.dialux.com |
| /pricing → 404, Request-Access-Modell | https://www.endra.ai/access |
| Marktgröße MEP-Software (~$4,85 Mrd 2025) — nur „wahrscheinlich" | https://market.us/report/mep-software-market/ |

**Ehrlichkeits-Hinweis zur Quellenlage:** Endra ist gut presse-dokumentiert (Funding), aber produktseitig dünn: nur 2 Resources-Artikel, kein API-/Entwickler-Material, keine öffentlichen Repos, keine Preise. Die Methodik-Aussagen stammen fast ausschließlich aus Interviews und Stellenanzeigen; alle Effizienz-Zahlen sind Eigenangaben.

---

## Nachtrag: Nachrecherche (Vollständigkeits-Kritik, 02.09.2026)

- **Gründungsjahr GEKLÄRT (amtlich): Endra Systems AB wurde am 13.09.2024 im schwedischen Handelsregister eingetragen, Org.-Nr. 559496-5898, Sitz Stockholm, Branche Datautveckling/Systemutveckling. Damit ist 'late 2024' (SiliconANGLE) korrekt und konsistent mit Norrskens 'eight months of operation' (Mai 2025); die '2023'-Angaben (builtin/Forbes-Snippet) sind falsch oder beziehen sich allenfalls auf informellen Teamstart, nicht auf die Firma.** (Quelle: https://www.allabolag.se/foretag/endra-systems-ab/stockholm/datautveckling-systemutveckling-programutveckling/2KJ3JBEI5YDOJ)
- **Umsatz-Lücke TEILWEISE GESCHLOSSEN (erster Jahresabschluss): FY2025 Umsatz nur 160 TSEK (~15 T€), Ergebnis nach Finanznetto −12.481 TSEK, 7 Angestellte (Jahresabschluss-Zahl; Presse-Teamgrößen zählen offenbar Konsultants/spätere Hires). Endra ist trotz ~$75 Mio. Funding praktisch pre-revenue — stützt die Reife-Einschätzung 'viel Kapital, dünne Produkt-Substanz'. CEO lt. Register: Niklas Erik Robin Lindgren (Jg. 1995), Verwaltungsratsvorsitz: Gustav Olof Hammarlund (Jg. 1990).** (Quelle: https://www.allabolag.se/foretag/endra-systems-ab/stockholm/datautveckling-systemutveckling-programutveckling/2KJ3JBEI5YDOJ)
- **Modul-Status-Inkonsistenz für den AKTUELLEN Stand geklärt (Live-Abruf endra.ai am 02.09.2026): Nur Fire Alarm = 'Live'. Electrical, Containments & Conduits, Lighting Systems, HVAC, Plumbing & Sprinkler, Data & Fibre und Security sind ALLE als 'Coming Soon' gelistet. Lighting und Containments sind Stand heute also NICHT live; frühere 'Live'-Snapshots waren Early-Access-/Marketing-Grauzone. Keine Erwähnung von Emergency Lighting, Pricing oder Audit-Trail auf der Startseite.** (Quelle: https://endra.ai)
- **Fire-Alarm-Produktseite (Live-Abruf 02.09.2026) bestätigt: Inputs wörtlich 'You can drop IFC, DXF (DWG) and PDF files'; KEINE Erwähnung von Emergency Lighting, Battery Calculations, Audit-Trail/Traceability oder konkret benannten Normen (kein NFPA/BS/EN explizit, nur generisch 'code-compliant'). Zur Parsing-Technik nur die Blackbox-Aussage 'analyze your building and code, and place all your units accordingly' — stützt die Berichts-These, dass die DXF/PDF-Verarbeitung nicht dokumentiert ist.** (Quelle: https://www.endra.ai/product/fire-alarm)
- **AFRY-Partnerschaft an der Primärquelle verifiziert (AFRY-Pressemitteilung 23.04.2026): 'strategic collaboration' für AI-Plattform 'within electrical, and fire safety design', Fokus frühe Projektphasen ('early phases of building projects'), Laufzeit 'throughout Endra's development phase' — AFRY positioniert es explizit als Lern-/Evaluierungspartnerschaft ('build hands-on experience in the application of AI'), nicht als produktiven Rollout. Zitatgeber: Thomas Hoff, Head of Public & Commercial Places Sweden.** (Quelle: https://afry.com/en/newsroom/press-releases/afry-partners-endra-ai-in-building-design)
- **Series A unabhängig (jenseits Eigen-PR) bestätigt: DLA Piper beriet Andreessen Horowitz beim $50-Mio.-Investment in Endra (Meldung Juni 2026, mit Notion Capital und Norrsken VC, Gesamt $75 Mio.). Eine Bewertung wird auch in Kanzlei-, Dealroom- und Presse-Quellen NICHT genannt — Bewertung bleibt nicht offengelegt.** (Quelle: https://www.dlapiper.com/en/news/2026/06/dla-piper-advises-andreessen-horowitz-on-usd50-million-investment-in-endra)
- **Notbeleuchtungs-Lücke erneut gezielt geprüft: Suche nach endra.ai + 'emergency lighting'/'escape lighting' liefert ausschließlich fremde Hersteller (ETAP, Ansell etc.), null Endra-Treffer; auch Startseite und Fire-Alarm-Seite erwähnen Notbeleuchtung nicht. Die Nicht-Existenz öffentlicher Notbeleuchtungs-Aussagen ist damit doppelt abgesichert (Stand 02.09.2026).** (Quelle: https://www.endra.ai/product/fire-alarm)

### Öffentlich nicht klärbar

- Ob Lighting-/Electrical-Modul künftig Notbeleuchtung (EN 1838/EN 50172) enthält: keine öffentliche Roadmap-Aussage auffindbar; ÖNorm/Österreich weiterhin nirgends erwähnt (gezielte Suchen ergebnislos).
- Bewertung der Series A: in keiner Quelle (a16z, DLA Piper, Dealroom, Presse) offengelegt.
- Preismodell: weiterhin keine Lizenz-/Seat-/Projektpreise öffentlich; Website zeigt nur Request-Access, /pricing-Link ohne Inhalt.
- ML-Methodik (welche LLMs, eigene Modelle, 'deterministic ML'): keine Whitepaper oder technischen Interviews auffindbar; Produktseiten bleiben Blackbox ('analyze your building and code').
- Konkrete DXF-/PDF-Parsing-Technik und Raumerkennung ohne BIM-Semantik: öffentlich nicht dokumentiert (Produktseite nennt nur die Formate, nicht das Verfahren).
- Existenz eines expliziten Spec-/LB-Text-Inputs mit Override-Logik (Analogon LBVorgabe): keine Produktdoku dazu auffindbar.
- Audit-Trail-/Entscheidungsquellen-Konzept (Pendant zu norm_quelle): weiterhin keine Erwähnung auf Produktseiten; Fehlen bleibt unbeweisbar.
- Unabhängige Verifikation der Effizienz-/Qualitäts-Claims (304h→0,5h, 98,8 %, 12x, 100 % Pilot-Konversion): keine Drittquellen gefunden.
- Patente: Suche nach 'Endra Systems'/Lindgren + Patent liefert keine Treffer; Espacenet-Direktrecherche ist per Web-Suche nicht abbildbar — ob Schutzrechte angemeldet sind, bleibt offen.
- Demo-Material (YouTube/Webinare) inhaltlich: per Web-Suche nicht auswertbar, Produkt bleibt hinter Request-Access.

---

## Nachtrag 2: Tiefen-Recherche Raumerkennung (02.09.2026, 3 Spezial-Sweeps)

### Kernbefund: Endra LÖST unser Raumerkennungsproblem nicht — sie UMGEHEN es

Endras Erkennungsschicht ist zweigeteilt, und beide Hälften setzen semantikreiche
3D-BIM-Inputs voraus:

1. **Geometrie/Topologie — deterministisch aus BIM:** Primärpfad ist das
   Architekten-IFC bzw. Live-Revit-Daten („architect's IFC in, fully coordinated MEP
   design … out" — Lindgren, Digital Construction Plus). Räume, Wände, Türen, Ebenen
   liegen dort bereits als Objekte vor (IfcSpace/Revit Rooms). Endra „reconstructs a
   building in 3D" (a16z) in einem **eigenen granularen 3D-Datenmodell**, weil „Revit's
   underlying data model is too coarse to support deep automation" (Lindgren, AEC
   Business). Die C#/.NET-Revit-Add-ins ziehen Modelldaten per API; IFC-Import
   vermutlich eigenes Parsing im C++23-Core (IFC-Erfahrung ist beim BIM Engineer nur
   „nice-to-have"; IFC-Export erst „on the near-term roadmap").
2. **Semantik — LLM als Normalisierer, nicht als Entdecker:** „LLMs … help us
   **identify room types, identify objects**, and also the intent of the architect"
   (Lindgren, Fortune). Der a16z-Essay beschreibt den Mechanismus explizit: BIM-Modelle
   tragen Raum-Metadaten „entered inconsistently and in formats that varied by firm and
   project… **LLMs parse the unstructured metadata, classify it semantically, and hand
   structured inputs to downstream engineering algorithms.**" Das LLM klassifiziert
   also VORHANDENE Raum-Labels/Parameter — es erfindet keine Räume aus Geometrie.

### Negativbefunde (dreifach abgesichert)

- **Keine Computer Vision, kein OCR, kein Point-Cloud, kein 2D-Plan-Parsing:** In
  keiner der ~14 Stellenanzeigen (builtin, Norrsken-Board, archivierte Careers-Seiten)
  tauchen CV/OCR/PDF-Verarbeitung/IfcOpenShell/DXF-Libraries auf; es gibt **keine
  einzige ML-/CV-/LLM-Engineer-Rolle**. Die Platzierungs-Engine ist C++23 Computational
  Geometry + Graphen + kombinatorische Optimierung.
- **DXF/PDF werden als Upload akzeptiert, aber nirgends als analysierter Pfad
  beschrieben** — PDF taucht in der FAQ sogar nur als OUTPUT-Format auf. Wie (ob) aus
  einem nackten 2D-DXF Räume werden, ist in keiner Quelle dokumentiert; plausibel ist
  Underlay-/Referenz-Nutzung, nicht semantische Erkennung (Interpretation).
- **Keine Patente auffindbar** (Google-Patents-API: „Endra Systems" 0 Treffer, alle
  Gründer-Namen nur Namensvettern; Anmeldungen < 18 Monate wären allerdings noch
  unsichtbar). Burggraben laut Fortune: proprietäre Geometry-Engine + Datenmodell
  (Trade Secret). Keine Papers/Abschlussarbeiten der Gründer (Ex-Goldman-Sachs-
  Infrastruktur, keine Akademiker-Spur).
- **Welche LLM-Anbieter** (OpenAI/Anthropic/Vertex) als Subprozessor dienen, war nicht
  verifizierbar (trust.endra.ai = Vanta-JS-App, ohne Browser-Render nicht lesbar).

### Prozess-Detail mit Übernahme-Wert

Der offizielle 6-Stufen-Workflow enthält **„2. Model input & review"** als expliziten
Human-Gate ZWISCHEN Modell-Import und Platzierung: das erkannte Gebäudemodell wird dem
Ingenieur zur Prüfung vorgelegt, bevor die Engine platziert. Das ist exakt unsere
RaumModell→Platzierer-Naht — als sichtbarer Review-Schritt produktisiert.

### Konsequenzen für uns

1. **Unser 2D-DXF-Pfad bleibt Differenzierung:** Für Pläne ohne BIM-Semantik (der
   österreichische Bestand) zeigt Endra öffentlich keine Lösung. Unsere Raumerkennung
   aus nackter Vektorgeometrie ist genau das, was sie umgangen haben.
2. **LLM-Raumtyp-Fallback (P4) doppelt validiert:** Endra nutzt LLMs exakt an der
   Stelle, an der unsere Layer-Regex/Token-Klassifikation scheitert — als semantischen
   Normalisierer über vorhandenen Labels, mit deterministischem Kern dahinter. Gleiches
   Muster bei uns: `classify_room` deterministisch, LLM nur bei UNKNOWN, Audit-Flag.
3. **„Model input & review" als Produkt-Feature (NEU, S/M):** Ein Zwischen-Output
   „erkanntes RaumModell zur Prüfung" (Raum-Polygone + Typen + Ausgänge als
   Übersichtsplan/JSON vor der Platzierung) — macht unsere Erkennnungs-Schwächen
   sichtbar statt still und ist der natürliche erste Dialog-Schritt fürs
   Chat-Interface. Passt zu P6 (Q&A-Rückfragen).
4. **Eigenes granulares Datenmodell statt CAD-Semantik:** Endras Kern-These („Revit
   too coarse") ist strukturell unsere Contract-Architektur (RaumModell statt
   DXF-Layer) — kein Handlungsbedarf, aber ein starkes externes Validierungs-Argument.

Quellen: Fortune (18.12.2025) · a16z.news „Every building you've ever been in" +
a16z-Announcement · AEC Business Podcast (Lindgren) · Digital Construction Plus ·
SiliconANGLE · builtin.com-Stellenanzeigen (BIM Engineer 9727944, Optimization 9727913,
Core 9727916, Product 9727939) · Wayback-Snapshots endra.ai (01/2025, 07/2025, 03/2026,
Careers 01/2026) · Google-Patents-API · trust.endra.ai (Vanta).


### Nachtrag 3: Subprozessoren-/LLM-Anbieter-Versuch (02.09.2026)

Direkter Zugriff auf trust.endra.ai (Vanta) technisch nachgestellt: Das Trust Center
nutzt **signierte GraphQL-Persisted-Operations** (Signature-Manifest mit 3.881
Operationen; die gesuchte heißt `SubprocessorsSectionPaginated`). Der Server verlangt
zur Signatur zusätzlich den vollen Query-Text, der nur in einem minifizierten
Lazy-Chunk als AST liegt — Rekonstruktion unverhältnismäßig; ohne Browser-Rendering
bleibt die Liste verschlossen.

Ersatz-Fund in der statischen **Privacy Policy** (endra.ai/legal/privacy-policy):
Unter „Analytics/Service Providers" steht wörtlich *„Other cloud providers (AWS,
Google or Azure) tools to train models and track user patterns"* — generisch
(bezieht sich auf Usage-Daten, nicht Kundenmodelle; deckt sich mit dem GCP-Backend
aus den Stellenanzeigen). **Kein LLM-Anbieter (OpenAI/Anthropic/Vertex/Gemini) wird
irgendwo auf der statischen Website namentlich genannt.** Die konkrete
Subprozessoren-Liste ist nur über ein echtes Browser-Rendering des Vanta-Trust-
Centers auslesbar.
