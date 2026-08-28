# ArchiteCAD a large-scale architectural CAD dataset for symbol spotting towards CAD-to-BIM conversion — Teil 0
> Quelle: ArchiteCAD a large-scale architectural CAD dataset for symbol spotting towards CAD-to-BIM conversion (buecher) · Seiten 1-19.

Wissenschaftlicher Artikel aus dem International Journal on Document Analysis and Recognition (IJDAR), DOI 10.1007/s10032-025-00557-3. Das Dokument stellt den ArchiteCAD-Datensatz (Vektorformat, 5.933 Grundrisse aus realen AECO-Projekten) und das darauf aufbauende Modell ArchiteCADNet vor, das auf Graph Attention Networks (GATv2) basiert und automatische Symbelerkennung in CAD-Zeichnungen zur BIM-Konvertierung ermöglicht. Dieser Teil umfasst Einleitung, Literaturüberblick, Datensatz-Beschreibung, Modellarchitektur sowie Experimente und Schlussfolgerungen (Seiten 1–19).

## Inhalt

### Einleitung und Motivation

- Building Information Modeling (BIM) ist ein zentrales Konzept in der Architektur-, Ingenieur-, Bau- und Betriebsbranche (AECO), mit Anwendungsfeldern wie Stadtplanung, Baustellenmanagement, Facility Management und Energieeffizienz.
- Für Bestandsgebäude, die vor der BIM-Ära errichtet wurden, sind CAD-Zeichnungen nach wie vor die primäre Informationsquelle für Gebäudedaten.
- CAD-Zeichnungen sind semantisch reichhaltige Vektordaten, die präzise geometrische und topologische Details enthalten; sie sind in der AECO-Branche weit verbreitet und gelten als Pflichtbestandteil für Baugenehmigungen.
- Traditionelle regelbasierte CAD-zu-BIM-Konvertierungssysteme werden mit wachsenden Anforderungen zunehmend komplex, wartungsintensiv und abhängig von manueller Benutzerinteraktion.
- Datengetriebene Ansätze mit maschinellem Lernen gewinnen an Bedeutung; die meisten bestehenden Methoden verarbeiten jedoch gerasterte (rasterisierte) CAD-Zeichnungen statt nativer Vektordaten.
- Zwei Hauptgründe für den Mangel an Vektorverarbeitungsmethoden: (1) geringe Datenverfügbarkeit — CAD-Zeichnungen werden nur innerhalb der AECO-Branche geteilt; (2) fehlende Methoden für unstrukturierte Vektordaten in der frühen Deep-Learning-Phase.
- Graph Neural Networks (GNNs) ermöglichen die Repräsentation von Vektordaten als Graphen und bieten einen neuen Lösungsweg.
- FloorplanCAD (2021) war der erste großmaßstäbliche Vektordatensatz mit semantischen und Instanz-Annotationen für CAD-Grundrisse (37 Kategorien); darauf aufbauend wurde GAT-CADNet entwickelt.
- Schwächen von FloorplanCAD: unvollständige Abdeckung, eingestellte Wartung, fehlerhafte DWG-zu-SVG-Konvertierung mit Datenverlust; GAT-CADNet leidet unter statischer Aufmerksamkeit (global monotone Attention).

### Hauptbeiträge der Studie

- **ArchiteCAD-Datensatz:** Zusammenstellung realer CAD-Zeichnungen aus AECO-Projekten, robuste DWG-zu-SVG-Konvertierung, umfassende semantische und Instanz-Annotationen für BIM-Komponentensymbole.
- **ArchiteCADNet:** Verbessertes Modell auf Basis von GAT-CADNet; ersetzt GAT-Schichten durch GATv2-Schichten, die dynamische statt statischer Attention berechnen; vereinfachte Modellstruktur bei gesteigerter Klassifikationsgenauigkeit.

### Literaturüberblick — Bestehende Datensätze

#### Rasterformat-Datensätze
- Frühe Datensätze für Architekturzeichnungen lagen primär als Rasterbilder vor (z.B. SESYD, RPLAN, BRIDGE, ZSCVFP, RFP, LIFULL, CubiCasa5K, HouseExpo).
- Rasterbilder sind leicht verfügbar und verteilbar, liefern aber keine präzisen Geometrieinformationen und sind für BIM-Modellierung unzureichend.

#### Vektorformat-Datensätze
- Vektorformat-Datensätze stehen vor zwei Problemen: mangelnde Datenverfügbarkeit (DWG-Format ist proprietär und nur mit Spezial-CAD-Software nutzbar) sowie fehlende Forschungsparadigmen für unstrukturierte Vektordaten.
- FPLAN-POLY: 42 Grundrisse, Vektorformat, 38 Klassen, mit semantischen und Instanz-Labels.
- FloorplanCAD (2022): 10.094 ausgeschnittene Zeichnungsrahmen, Vektorformat, 35 Klassen, mit semantischen und Instanz-Labels; Tausende Expertenstunden für Annotationen; erste Balance aus Authentizität, Datensatzgröße und Annotationsqualität; jedoch enthält es viele Möbel-Layout-Symbole, die für stadtweite BIM-Modellierung irrelevant sind; DWG-zu-SVG-Konvertierung führt zu teilweisem Datenverlust.

#### Vergleichstabelle bestehender Datensätze

| Datensatz | Quelle | Umfang | Format | Sem. Klassen | Semantisch | Instanz |
|---|---|---|---|---|---|---|
| SESYD | Synthetisch | 1.000 | Raster/Vektor | 16 | Ja | Ja |
| RPLAN | Synthetisch | 80.788 | Raster/Vektor | 4 | Ja | — |
| BRIDGE | Internet | 13.000 | Raster | 14 | Ja | — |
| ZSCVFP | Internet | 10.800 | Raster | 6 | Ja | — |
| RFP | Internet | 7.000 | Raster | 7 | Ja | — |
| LIFULL | Industrie | 5.300.000+ | Raster | — | — | — |
| CubiCasa5K | Internet | 5.000 | Raster | 80 | Ja | — |
| HouseExpo | Synthetisch | 35.126 | Raster | 2 | — | — |
| FPLAN-POLY | Internet | 42 | Vektor | 38 | Ja | Ja |
| FloorPlanCAD | Industrie | 10.094 (Ausschnitte) | Vektor | 35 | Ja | Ja |
| ArchiteCAD (Ours) | Industrie | 5.933 (vollständige Rahmen) | Vektor | 9 | Ja | Ja |

### Literaturüberblick — Automatische Analyse von Architekturzeichnungen

- Klassische regelbasierte Systeme werden zunehmend durch maschinelles Lernen und Deep Learning verdrängt.
- CNN-basierte Ansätze dominieren durch Rasterimage-Datensätze; leiden aber unter eingeschränkter Generalisierbarkeit zwischen Datensätzen.
- **PanCADNet** (Fan et al.): Kombination aus CNN-Backbone und GNN-Detektionskopf; Vektordaten werden in Graphen umgewandelt, Knoten repräsentieren Vektorelemente mit Geometriemerkmalen; Geometrie- und Texturmerkmale werden kombiniert und in GNN sowie Fast R-CNN eingespeist zur Klassifikation und Instanz-Segmentierung.
- **GAT-CADNet** (Zheng et al.): Vollständig vektorbasiertes Modell; nutzt Graph Attention Networks (GAT) als Backbone; Knoten=Vektorelemente mit geometrischen Attributen, Kanten=topologische Beziehungen mit Kantenattributen; Ausgabe umfasst semantische Klassifikation der Knoten und Adjazenzmatrix-Vorhersagen für Kanten (Instanz-Segmentierung über Attention-Koeffizienten der letzten GAT-Schicht).

### Literaturüberblick — Graph Neural Networks und Attention-Mechanismen

#### Graph Neural Networks (GNNs)
- GNNs sind neuronale Netze für graphstrukturierte Daten (Knoten + Kanten), typisch in sozialen Netzwerken oder Molekülstrukturen.
- Kernprinzip: iterative Weitergabe und Aggregation von Informationen entlang der Kanten, um Repräsentationsvektoren der Knoten zu aktualisieren.
- Iterationsformel: h(t+1)_v = f(h(t)_v, {h(t)_u : u ∈ N(v)}), wobei h(t+1)_v der Zustand von Knoten v nach t-ter Iteration ist, N(v) die Nachbarknoten bezeichnet, und f die Propagations- und Aggregationsfunktion darstellt.
- Vektordaten eignen sich natürlich für Graphdarstellung: jedes Vektorgrafik-Element wird als Knoten modelliert, topologische Beziehungen werden als Kanten dargestellt.
- Vorteil: hohe geometrische Präzision mit geringer Redundanz → spärliche Graphstruktur → hohe Recheneffizienz.

#### Graph Attention Networks (GAT)
- GAT (Veličković et al.) erweitert GNNs um gewichtete Nachbarn-Aggregation anstelle gleichgewichteter Behandlung aller Nachbarn (wie in GCN, GraphSAGE).
- Eingabe: Knotenfeature-Menge h = {h_1, h_2, ..., h_N}, h_i ∈ R^F; Ausgabe: h' = {h'_1, h'_2, ..., h'_N}, h'_i ∈ R^F'.
- Attention-Koeffizient: e_ij = a(W·h_i, W·h_j), normalisiert mit Softmax: α_ij = exp(e_ij) / Σ_{k∈Ni} exp(e_ik).
- Implementierung: einschichtiges Feedforward-Netz mit gelerntem Gewichtsvektor a→, LeakyReLU-Nichtlinearität:
  α_ij = exp(LeakyReLU(a→^T [W·h_i || W·h_j])) / Σ_{k∈Ni} exp(LeakyReLU(a→^T [W·h_i || W·h_k]))
- Ausgabe-Feature pro Knoten: h'_i = σ(Σ_{j∈Ni} α_ij · W·h_j), wobei σ eine optionale nichtlineare Aktivierungsfunktion ist.
- Vorteil für CAD-Daten: Attention unterscheidet die Bedeutung verschiedener Knoten → genauere Erkennung von Symbolen, die aus Kompositionsmustern elementarer Grafikelemente bestehen.

#### Problem: Statische Attention in GAT
- GAT leidet unter globaler statischer Attention: für beliebige Abfrageknoten bleibt die Rangfolge der Aufmerksamkeitsscores monoton, d.h. die Attention-Rangfolge ist über alle Knoten im Graph gleich, unabhängig vom jeweiligen Abfrageknoten.
- Formal: e_ij = LeakyReLU(a→^T [W·h_i || W·h_j]); die aufeinanderfolgenden lernbaren Schichten W und a→ können zu einer einzigen linearen Schicht zusammengefasst werden → globale Monotonie.
- Folge: reduzierte Ausdrucksstärke des Attention-Mechanismus bei der Erfassung relativer Wichtigkeit von Nachbarn.

#### GATv2 — Dynamische Attention
- GATv2 (Brody, Alon, Yahav 2021) behebt das Problem durch einfache Umordnung der Operationen: a→ wird nach der Nichtlinearität angewendet, W-Schicht nach der Konkatenation:
  e_ij = a→^T · LeakyReLU(W · [h_i || h_j])
- Ergebnis: dynamische Attention, die je nach Abfragekontext variiert; gleiche Zeitkomplexität wie GAT; gesteigerte Ausdrucksstärke und Recheneffizienz.

### Der ArchiteCAD-Datensatz

#### Datenquellen und Umfang
- Gesammelt aus realen AECO-Projekten: über 2.000 Wohnbauprojekte und mehrere hundert Projekte für öffentliche Gebäude.
- Originale CAD-Zeichnungen dienten als Grundlage für BIM-Modellierungen; sowohl CAD-Zeichnungen als auch resultierende BIM-Modelle wurden von städtischen Wohnbau- und Baubehörden auf Korrektheit und Zuverlässigkeit geprüft.

#### Vorverarbeitung (Preprocess)
- Einzelne AECO-Projektdateien enthalten mehrere Zeichnungsblätter (z.B. Grundrisse, Schnitte, Aufrisse, Detailzeichnungen, Tabellen).
- Nach manueller Blatt-Segmentierung enthält der aktuelle Datensatz 5.933 Grundrisse.
- Elemente in einem Grundriss: Grafikelemente (Konturen, Symbole als BlockReference, Schraffuren), Beschriftungselemente (Texte, Anmerkungen, Leader), Achsraster, Zeichnungsrahmen, Tabellen/Notizen.
- Zur Unterdrückung georeferenzieller Information: Achsraster und Titelblöcke wurden während der Datensatzvorbereitung entfernt; nur für räumliche Gebäudebeschreibung wesentliche Elemente wurden beibehalten.

#### Annotation
- Ground-Truth-Annotationen bestehen aus semantischen Labels (Klassenbezeichnung) und Instanzindizes (eindeutige Instanznummer innerhalb einer Klasse).
- Die gesammelten Zeichnungen entstammen BIM-Modellierungsprojekten, bei denen die relevanten Bauteilschichten reorganisiert und Symbole in relativ einheitlichem Stil von Domänenexperten neu gezeichnet wurden.
- Neun Symbolkategorien für Neubeschriftung definiert: Wände/Stützen, Vorhangfassaden, Türen, Fenster, Treppen, Balkone, Öffnungen/Durchbrüche, Bodenplatten, Anmerkungen.
- Neuzeichnung erfolgte in separaten Schichten ohne Veränderung der Originalschichten → Integrität der Quellzeichnungen erhalten.
- Annotationsübertragung: Durch Überlagerung originaler und neu gezeichneter Symbole wird jedes Originalsymbol einer Komponentenkategorie zugewiesen und als eigene Instanz segmentiert.
- Im SVG-Format: semantische Labels und Instanzindizes werden als Attributfelder in die zugehörigen SVG-Elemente eingebettet.
- Da die BIM-Modelle bereits von Domänenexperten verifiziert wurden, gelten die übertragenen Annotationen als hoch zuverlässig und konsistent.

#### Formatkonvertierung DWG → SVG
- SVG ist ein offenes Vektorgrafik-Format, das Elemente als XML-Textdateien definiert und speichert; weit unterstützt von Grafiksoftware und Webbrowsern (Chrome, Firefox).
- FloorplanCAD zerlegt DWG-Designelemente (BlockReference, Region, Polyline) und reorganisiert SVG-Elemente manuell nach semantischen Labels → Verlust struktureller DWG-Informationen.
- Ansatz dieser Studie: strukturelle Integrität der DWG-Datei möglichst vollständig erhalten.
- Mapping DWG → SVG:
  - **Grundlegende Grafikelemente** (unteilbar oder mit direkten SVG-Entsprechungen):
    - Linie, Kreis, Ellipse, Text → direkte SVG-Entsprechungen
    - Arc → `<path>`
    - Polyline → `<polyline>`
    - Region → `<polygon>`
  - **Komplexe Elemente** → SVG `<g>`-Elemente mit expliziten Typ-Attributen:
    - Layer: behält originale DWG-Schichtinformation ohne Reorganisation
    - BlockReference (wiederverwendbare Symbole): `<g>`-Element innerhalb von Layer-`<g>` neben anderen Grundelementen
    - Hatch (Schraffur für Material-/Eigenschaftsinformationen in geschlossenen Formen): `<g>`-Element innerhalb von Layer-`<g>`
  - Verschachtelte `<g>`-Elemente auf mehreren Ebenen bewahren die strukturelle Integrität der DWG-Datei.
- DWG-Ansicht: in AutoCAD; SVG-Ansicht: direkt im Chrome-Browser.

#### Datensatz-Eigenschaften und Vorteile gegenüber bestehenden Datensätzen

1. **Großmaßstäbliche Realdaten:** Gestützt auf jahrelange städtische BIM-Modellierungsprojekte, umfangreiche Sammlung aus realen AECO-Projekten.
2. **Vollständige Vektormerkmale:** SVG-Format erhält Struktur der originalen DWG-Dateien inklusive geometrischer Eigenschaften, Attributinformationen, Schichtorganisation und Zeichenstile.
3. **Umfassende Ground-Truth-Annotationen:** Semantische Labels und Instanzindizes für jedes Element ermöglichen genaue Auswertung von Klassifikations- und Instanz-Segmentierungsaufgaben.

### ArchiteCADNet — Modell für CAD-Zeichnungswahrnehmung mit GATv2

#### Graphkonstruktion — Konvertierung in Graphstruktur

- Eingabe-CAD-Vektorzeichnung wird als ungerichteter Graph g = (V, E) dargestellt.
- V = Knotenmenge; jeder Knoten v_i entspricht einem elementaren Vektorgrafik-Element.
- E = Kantenmenge; Kante e_ij verbindet Knotenpaare v_i und v_j.
- Kantenerzeugungsregeln — eine Kante e_ij entsteht, wenn eine der folgenden Bedingungen erfüllt ist:
  1. Die durch v_i und v_j repräsentierten Basisvektorelemente schneiden sich (Schnitt-Nachbarn / intersecting neighbors).
  2. Der Abstand der Mittelpunkte der durch v_i und v_j dargestellten Elemente ist kleiner als die Hälfte der Summe ihrer Längen (benachbarte Nachbarn / adjacent neighbors).
- Bedingung 1 erfasst die typischen Überschneidungsmuster in CAD-Symbolen.
- Bedingung 2 dient als Kompensationsmechanismus für geometrische Ungenauigkeiten durch manuelle CAD-Erstellung (z.B. durch Object-Snapping entstehende unsichtbare Versätze, die mathematisch vorhanden aber visuell nicht erkennbar sind) → vollständigere Graphstruktur.

#### Knotenmerkmale (Node Features)

- Knotenfeature-Vektor v_i ∈ R^33, unterteilt in drei Kategorien:
  1. **Typinformation t→ ∈ R^2:** One-Hot-Kodierung des Typs des Basisvektorelements.
  2. **Geometrische Attribute s→ ∈ R^3:**
     - Für Liniensegmente: Länge (restliche 2 Dimensionen mit Nullen aufgefüllt).
     - Für Bögen: Bogenlänge, Bogenmaß (Radian), Radius des zugehörigen Kreises.
  3. **Nachbarschafts-Statistikmerkmale n→ ∈ R^28**, bestehend aus zwei Teilen:
     - **Nachbarschaftstyp-Statistik types→ ∈ R^23:** Gesamtanzahl der Schnitt-Nachbarn v_j von v_i, Anzahl Schnitt-Nachbarn nach Typ, Gesamtanzahl benachbarter Nachbarn v_k.
     - **Nachbarschaftsverteilungs-Statistik distribution→ ∈ R^5:** Durchschnittlicher Mittelpunktsabstand, relative Richtungsverteilung und orthogonales Verhältnis zwischen v_i und Schnitt-Nachbar v_a; sowie die gleichen Statistiken für v_i und benachbarten Nachbar v_b.
- Mittelpunktbezogene Merkmale liefern genauere räumliche Beziehungen für Liniensegmente und Bögen.
- Detaillierte Schnitttypen für Liniensegment-Bogen-Kombinationen: siehe Appendix A im Supplementary Material.

#### Kantenmerkmale (Edge Features)

- Kantenfeature-Vektor e_ij ∈ R^30, unterteilt in:
  1. **Kantentypinformation et→ ∈ R^27**, drei Komponenten:
     - **pair→ ∈ R^3:** One-Hot-Kodierung der Elementtypen an den zwei Kantenenden; drei Kombinationen: "Liniensegment–Liniensegment", "Liniensegment–Bogen", "Bogen–Bogen".
     - **rel→ ∈ R^2:** One-Hot-Kodierung des Kantenkonstruktionstyps: Schnitt-Nachbarkante oder benachbarte Nachbarkante.
     - **intersect→ ∈ R^22:** Schnitttyp, konsistent mit den Regeln in den Nachbarschaftstyp-Statistiken der Knotenmerkmale.
  2. **Geometrische Kantenattribute es→ ∈ R^3**, drei Komponenten:
     - **(a) Winkel zwischen Elementen:** Für zwei Liniensegmente l_i und l_j: Bogenmaß zwischen Vektordarstellungen v_i→ und v_j→; für Kombinationen mit Bögen wird der Bogen durch einen Vektor von Start- zu Endpunkt dargestellt und analog berechnet.
     - **(b) Kantenlänge:** Abstand zwischen den Schwerpunkten der durch die beiden Knoten repräsentierten Vektorelemente.
     - **(c) Längenverhältnis:** Verhältnis der Längen der durch die beiden Knoten dargestellten Vektorelemente.

#### Netzwerkarchitektur

- Aufgabe: Symboltyp-Klassifikation von Vektorelement-Knoten.
- **Labels:** y ∈ {0, 1, 2, 3, 4, 5, 6, 7, 8}, semantisches Label des Elements (9 Kategorien).
- **Eingabe:** Für ungerichteten Graph g = (V, E) mit N Knoten und E Kanten: Knotenfeatures V ∈ R^(N×33) und Kantenfeatures E ∈ R^(E×30).
- **Ausgabe:** p = [p_0, p_1, ..., p_8], 0 ≤ p_i ≤ 1, Σp_i = 1; Wahrscheinlichkeitsverteilung über 9 Symboltypen.
- Drei Hauptkomponenten: Eingabeschicht, gestapelte GATv2-Schichten, Ausgabeschicht.

##### Feature Embeddings und Relative Spatial Encoding

- **Feature Embeddings:** In der Eingabeschicht empfangen zwei MLPs (Multilayer Perceptrons) die initialen Knotenfeatures V und Kantenfeatures E; sie betten diese ein in V' ∈ R^(N×128) und E' ∈ R^(E×128).
- Beide MLPs haben identische Größe: jeweils zwei vollständig verbundene Schichten mit ReLU-Aktivierung dazwischen.
- ReLU-Funktion: ReLU(x) = max(0, x); weit verbreitet in Deep Learning durch Einfachheit und Effektivität.
- **Relative Spatial Encoding (RSE):** Häufig in Punktwolkenverarbeitung und NLP eingesetzt für Translationsinvarianz; Kantenfeatures werden durch ein MLP-Modul verarbeitet und in nachfolgende GATv2-Schichten eingespeist zur Verbesserung der Attention.

##### Optimierte Graph-Attention-Stufe

- GATv2-Stufen beginnen mit der ersten GATv2-Schicht, die eingebettete Features V' und E' empfängt.
- Nachfolgende GATv2-Schichten nehmen Ausgabe-Knoten- und Kantenfeatures der vorherigen Schicht.
- Jede GATv2-Schicht erhält das RSE der Kantenfeatures, das vor der Wertmatrix-Berechnung mit den Attention-Scores konkateniert wird.
- Größe der Knoten- und Kantenfeatures bleibt über alle GATv2-Schichten konstant.

##### Ausgabeschicht und Verlustfunktion

- MLP in der Ausgabeschicht nimmt Knotenfeatures V'' aus den GATv2-Schichten und bildet diese auf den Wahrscheinlichkeitsverteilungsvektor p ab.
- Ausgabe-MLP: zwei vollständig verbundene Schichten mit ReLU-Aktivierung dazwischen, gefolgt von Softmax-Aktivierung.
- Softmax-Funktion für Vektor z = [z_1, ..., z_C] (C Klassen): Softmax(z_i) = exp(z_i) / Σ_{j=1}^{C} exp(z_j); bildet Ausgabe auf [0,1] ab, Summe aller Wahrscheinlichkeiten = 1.
- Verlustfunktion: Kreuzentropie; Loss(y, p) = -Σ_{i=0}^{8} y_i · log(p_i), wobei y_i das i-te Element des One-Hot-kodierten Labels ist.

### Experimente und Auswertung

#### Datensatz und Implementierungsdetails

- 3.500 Grundriss-Samples für das Experiment, zufällig aufgeteilt im Verhältnis 6:2:2 (Training:Validierung:Test).
- Verbesserte GAT-Stufe (ArchiteCADNet): 4 GATv2-Schichten.
- Baseline GAT-CADNet: 8 GAT-Schichten.
- Beide Modelle: 8 Attention-Köpfe (H = 8), Adam-Optimizer mit β1 = 0,9, β2 = 0,999, Lernrate lr = 0,01.
- Lernraten-Anpassung: bei Stagnation über mehr als 4 Epochen → Lernrate × 0,6; bei Stagnation über mehr als 20 Epochen → Trainingsabbruch.

#### Klassifikationsergebnisse

- Nach ca. 80 Trainings-Epochen konvergierte das Modell.
- Endgültige Klassifikationsgenauigkeiten: Training 84,8%, Validierung 85,1%, Test 84,5%.
- Trainingsverlust: 0,399; Validierungsverlust: 0,432.

#### Konfusionsmatrix (Ground Truth vs. Vorhersage, Testset)

| Klasse (GT) | Wand/Stütze | Vorhang-wand | Tür | Fenster | Treppe | Balkon | Öffnung | Boden | Anmerkung |
|---|---|---|---|---|---|---|---|---|---|
| Wand/Stütze | 471.271 | 1 | 20.947 | 10.245 | 1.841 | 2.075 | 26 | 237 | 0 |
| Vorhangfassade | 2.045 | 12 | 155 | 77 | 0 | 0 | 0 | 1 | 0 |
| Tür | 20.288 | 0 | 147.644 | 6.544 | 518 | 431 | 4 | 509 | 0 |
| Fenster | 27.654 | 33 | 4.196 | 111.270 | 398 | 53 | 2 | 156 | 0 |
| Treppe | 6.964 | 0 | 1.003 | 1.127 | 25.738 | 834 | 12 | 45 | 0 |
| Balkon | 3.534 | 0 | 10.214 | 95 | 55 | 6.033 | 22 | 1 | 0 |
| Öffnung | 314 | 0 | 15 | 47 | 53 | 138 | 385 | 23 | 0 |
| Boden | 6.911 | 0 | 8.348 | 1.102 | 181 | 151 | 30 | 8.135 | 0 |
| Anmerkung | 505 | 0 | 140 | 112 | 10 | 31 | 1 | 79 | 0 |

#### Statistische Auswertung pro Klasse (Testset)

| Klasse | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Wand/Stütze | 0,87 | 0,93 | 0,90 | 506.643 |
| Vorhangfassade | 0,26 | 0,01 | 0,01 | 2.290 |
| Tür | 0,77 | 0,84 | 0,80 | 175.938 |
| Fenster | 0,85 | 0,77 | 0,81 | 143.762 |
| Treppe | 0,89 | 0,72 | 0,80 | 35.723 |
| Balkon | 0,62 | 0,30 | 0,41 | 19.954 |
| Öffnung | 0,80 | 0,39 | 0,53 | 975 |
| Boden | 0,89 | 0,33 | 0,48 | 24.858 |
| Anmerkung | 0,00 | 0,00 | 0,00 | 878 |
| **Genauigkeit gesamt** | | | **0,85** | **911.021** |
| Macro Avg | 0,66 | 0,48 | 0,53 | 911.021 |
| Weighted Avg | 0,84 | 0,85 | 0,84 | 911.021 |

- Klassen mit wenig Trainingssamples (Vorhangfassade, Anmerkung) zeigen deutlich niedrigere Precision und Recall als häufige Klassen (Wand/Stütze, Tür).
- Klassenimbalance stammt aus den realen CAD-Daten: Vorhangfassaden und Textelemente kommen selten vor im Vergleich zu Wänden, Türen und Fenstern.
- Klassen mit mehr Samples tendieren zu besserer Klassifikationsleistung.

### Ablationsstudie

#### (1) Optimierte Graph-Attention: GATv2 vs. GAT

- Vergleich GAT-CADNet (8 GAT-Schichten) vs. ArchiteCADNet (4 GATv2-Schichten), jeweils 8 Attention-Köpfe.

| Modell | GAT(v2)-Stufen | Attention-Köpfe | Accuracy | Weighted F1 | MIoU |
|---|---|---|---|---|---|
| GAT-CADNet | 8 | 8 | 0,82 | 0,81 | 0,697 |
| ArchiteCADNet (Ours) | 4 | 8 | 0,85 | 0,84 | 0,733 |

- ArchiteCADNet übertrifft GAT-CADNet in allen Metriken trotz nur halb so vieler Schichten.
- Ursache: statische Attention in GAT untergräbt Zuverlässigkeit und Ausdrucksstärke der Attention-Ranglisten → verschlechterte Modellleistung.
- GATv2-dynamische Attention ermöglicht kontextabhängige Fokussierung auf verschiedene Graphteile → besonders wichtig für komplexe und variierende Strukturmuster in CAD-Zeichnungen.
- Reduzierte Schichtenanzahl verhindert Overfitting, reduziert Rechenkomplexität ohne Verlust der Repräsentationskapazität.
- Qualitative Ergebnisse: ArchiteCADNet reduziert Klassifikationsfehler für spezifische Kategorien und erzielt stabilere Vorhersagen in Bereichen mit dichten oder komplexen Symbolansammlungen.

#### (2) Anzahl der GATv2-Stufen

- Phänomen Over-Smoothing in GNNs: wiederholte Aggregation über viele Schichten lässt Knotenfeatures zunehmend ähnlich werden → Feature-Vektoren werden homogen → Modell verliert Sensitivität für Unterschiede zwischen Knoten → Leistungsabfall.
- GATv2 lindert Over-Smoothing durch Attention-Gewichtung, beseitigt es aber nicht vollständig bei sehr tiefen Netzen.
- Optimum liegt bei 4 GATv2-Stufen: von 3 auf 4 Stufen → deutlicher Rückgang des Konvergenzverlusts; über 4 Stufen → Konvergenzverlust steigt wieder (Over-Smoothing).
- Prinzip: mehr Schichten erfassen zunächst komplexere Graphstrukturinformation, dann überwiegt Over-Smoothing-Effekt und reduziert Generalisierungsfähigkeit.

#### (3) Anzahl der Attention-Köpfe in GATv2

- Multi-Head-Attention: jeder Kopf lernt unabhängig und fokussiert auf andere Informationssubsets; Ausgaben werden zusammengeführt; erhöht Modellkapazität und Verständnis über mehrere Datendimensionen.
- Von 2 auf 8 Köpfe: Konvergenzverlust nimmt kontinuierlich ab → mehr Köpfe verbessern Leistung.
- Über 8 Köpfe hinaus: Konvergenzverlust beginnt langsam zu steigen → übermäßige Spezialisierung und Overfitting beeinträchtigen Generalisierungsfähigkeit.
- Optimale Anzahl Attention-Köpfe: 8.

### Ingenieuranwendungen

#### ArchiteCADNet in der Online-CAD-zu-BIM-Plattform

- ArchiteCADNet wurde in praktischen BIM-Modellierungsworkflows eingesetzt.
- End-to-End Deep-Learning-Methoden erreichen keine 100% Präzision → manuelle Nachkorrektur bleibt notwendig.
- In der Praxis sind CAD-Zeichnungen meist so organisiert, dass Symbole verschiedener Kategorien in klar getrennten Schichten liegen, häufig als vollständige BlockReferences.
- BIM-Modellierung erfordert erheblichen Aufwand für Schichtklassifikation und -gruppierung nach tatsächlichem Inhalt.
- Lösungsansatz: ArchiteCADNet klassifiziert semantisch alle Symbole in einer Zeichnung; durch Aggregation der Klassifikationsergebnisse werden dominante semantische Kategorien je Schicht identifiziert → effiziente Beschleunigung der Schicht-Klassifikation.
- Online-Plattform erreichbar unter: http://geodatapipeline.com/holoarch/
- Quellcode von ArchiteCADNet: https://gitee.com/zhoulch/archite-cadnet

### Schlussfolgerungen

- ArchiteCAD bietet einen robusten Vektordatensatz für datengetriebene CAD-zu-BIM-Forschung.
- Robuste DWG-zu-SVG-Konvertierung verbessert Datenzugänglichkeit gegenüber FloorplanCAD.
- ArchiteCADNet mit GATv2 adressiert Static-Attention-Limitation von GAT-CADNet und erzielt verbesserte Leistung bei vereinfachter Architektur.

#### Einschränkungen und zukünftige Arbeit

- Datensatz enthält überwiegend Wohngebäude-Zeichnungen; Gewerbe- und Bildungsgebäude sind unterrepräsentiert → eingeschränkte Vielfalt.
- Annotierungsumfang fokussiert auf BIM-relevante Elemente; andere CAD-Merkmale wie Vermessungsmarkierungen und Materialdetails sind nicht annotiert.
- Modellverbesserungen konzentrieren sich auf semantische Klassifikation; Instanz-Segmentierung ist noch offen.
- Geplante Erweiterungen: Datensatzgröße und Gebäudetypenabdeckung ausbauen, breitere Annotationsschemata entwickeln, Modellarchitektur insbesondere für Instanz-Segmentierung weiter optimieren.

### Literaturverweise (ausgewählte)

- [17] Fan et al.: FloorplanCAD — erster großmaßstäblicher Vektor-CAD-Datensatz, Panoptic Symbol Spotting, PanCADNet-Modell (ICCV 2021).
- [18] Zheng et al.: GAT-CADNet — vollständig vektorbasiertes Modell mit GAT-Backbone (CVPR 2022).
- [19] Brody, Alon, Yahav: GATv2 — Adressierung der statischen Attention in GAT (arXiv 2105.14491, 2021).
- [16] Scarselli et al.: Graph Neural Network Modell — grundlegende GNN-Theorie (IEEE Trans. Neural Networks 2008).
- [35] Veličković et al.: Graph Attention Networks — GAT-Originalarbeit (arXiv 1710.10903).
- [34] Kipf, Welling: GCN — Semi-supervised classification with graph convolutional networks.
- [33] Hamilton, Ying, Leskovec: GraphSAGE — Inductive representation learning on large graphs.
- Finanzierung: National Key Research and Development Program of China, Grant Nr. 2022YFC3803601.
- Datensatz: aufgrund von Datenschutzbestimmungen der Behörden derzeit nicht öffentlich verfügbar; Quellcode des Modells ist öffentlich auf Gitee.
