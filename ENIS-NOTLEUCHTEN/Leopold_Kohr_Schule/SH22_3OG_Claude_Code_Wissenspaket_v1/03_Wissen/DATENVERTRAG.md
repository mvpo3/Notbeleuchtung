# Datenverträge und Bedeutung der Dateien

## Drei Ebenen getrennt halten

| Ebene | Dateien | Aussage |
| --- | --- | --- |
| Quelle | Original-PDF/DXF, `quellen.json` | Was im übergebenen Plan steht |
| Fachliche Lerninterpretation | Lernbuch, Beispiele, Regeln, Linienbelege | Warum eine bestimmte Lesart am Beispiel begründet ist |
| Tatsächliche Softwareausgabe | Vom Repository zu erzeugender Ergebnisbericht | Was die aktuelle Engine wirklich ermittelt hat |

Die im Paket bereits enthaltenen Daten sind keine Messung der Engine. `ergebnis_vorlage.json` ist absichtlich leer und mit `not_run` markiert.

## Bibliothek der Beispiele

`lernbeispiele.json`: Ein Datensatz pro Beispiel, stabile `example_id`, A-/B-Seite, Fundstelle, Einzelmerkmale, ausführliche Beweiskette, Gegenbeispiel, Modellwirkung und offene Eigenschaft. `erkennungsregeln.json` enthält daraus abgeleitete fachliche Regeln, keine ausführbaren geometrischen Schwellwerte.

`linienbelege.json`: die 134 markierten Einzelmerkmale mit farbigen Polylinien, kubischen Bézierkurven, Punkten und Pfeilzielen. Die `feature_id` verweist auf dasselbe Merkmal in `lernbeispiele.json`. `original_pdf_path` bedeutet aus dem lokalen PDF-Pfadbestand gelesen. `manual_teaching_mark` kann eine Textunterstreichung, ein gewählter Originalausschnitt oder eine ausdrücklich gedachte Stellung sein. Der begleitende Merkmaltext bestimmt die Bedeutung.

Ein `pdf_drawing_index` ist ein Index in der für diese Lernfassung erzeugten PDF-Pfadliste. Er ist **kein DXF-Handle** und kann sich mit Parser/Export ändern. Die direkt gespeicherte Geometrie plus Quellenhash ist die verlässlichere lokale Fundstelle. Enthaltene `source_layer_hint` sind unterstützende Metadaten und kein alleiniger Wahrheitsbeweis.

`raumregister.json`: 30 gruppierte Registerzeilen aus S. 84–85; nicht 30 Räume. Gruppierte IDs und Namen bleiben in ihrer ursprünglichen Gruppierung. `3.007.A / B / C` wird nicht ohne weitere Prüfung in vollständige produktive Raumobjekte aufgespalten. `dxf_textfragmente.json` enthält Textfragmente und Einfügekoordinaten, keine verifizierten Text-Bounding-Boxes oder fertigen Raumstempel.

## Vorschlag für das produktive Modell

`07_Schemata/erkennungsmodell.schema.json` beschreibt einen **Adapter-/Zielvertrag**, keinen behaupteten bestehenden Repo-Typ. Bestehende Modelle bevorzugen und ihre Felder darauf abbilden. Ein fachliches Objekt umfasst mindestens:

- stabile Objekt-ID, Klasse, Quellbezüge und Koordinatensystem;
- Klassifikationsstatus `confirmed`, `supported`, `unknown` oder `conflicting`, ohne frei erfundene Wahrscheinlichkeiten;
- Begründung, geprüfte Alternative und offene Eigenschaften;
- Attribute mit eigenem Status, z. B. Klasse Fenster bestätigt, genaue Verglasung unbekannt;
- Geometrie mit Typ und explizitem Koordinatensystem oder `null`, solange nicht bestimmt;
- getrennte Bodenexistenz, allgemeine Zugänglichkeit und feste Barrierewirkung;
- Beziehungen wie `bounds`, `contains`, `connects`, `located_in`, `part_of` oder `annotates`, jeweils mit Beleg.

Die Statuswerte sind Arbeitskonventionen dieses Pakets, keine Messwerte. `confirmed` darf nur mit hinreichenden konkreten Belegen gesetzt werden; ein Layer allein reicht dafür nicht. `unknown` bedeutet unbekannt und darf nicht als `false` oder `0` exportiert werden.

## Geometrievertrag

`plan_norm_2000`: Original-PDF auf Breite 2000 normalisiert; Ursprung links oben, y nach unten. `source_pdf_points`: 4268 × 2953 PDF-Punkte. Die DXF hat laut Header `$INSUNITS = 4` (Millimeter), `$MEASUREMENT = 1`, `$LUNITS = 2`. Vor physikalischen Abständen trotzdem mindestens bekannte Maße und Blockskalierungen abgleichen. Der Ausschnitt `[x0,y0,x1,y1]` dient ausschließlich zum Wiederfinden.

Die in `koordinaten.json` gespeicherte DXF/PDF-Registrierung wurde für Fundstellen verwendet. Es liegt kein quantifizierter Registrierfehler vor. Deshalb vor millimetergenauen Aussagen mehrere unabhängige Kontrollpunkte prüfen. Schräglagen, andere Layouts und andere Quellen nicht mit dieser Transformation erzwingen.

Polygone müssen echte Grenzen abbilden: gültige geschlossene Ringe, richtige Innenringe, kein Durchstich durch Wände. Im JSON-Schema ist die Grundstruktur prüfbar; geometrische Gültigkeit, Selbstüberschneidungen, Topologie und Einheitenkorrektheit sind zusätzliche Aufgaben der Engine.

## Ergebnisvertrag der 32 Sollfälle

`07_Schemata/pruefergebnis.schema.json` und `05_Pruefung/ergebnis_vorlage.json` definieren:

- `run_id`, `engine_revision`, Hashes beider Originalquellen;
- pro Fall `case_id`, Status `observed` oder `not_run`;
- `claims` mit aus dem tatsächlichen Modell berechneten Aussagen;
- `evidence_by_claim` mit Originalquelle, konkretem Fundstellenbezug und tatsächlichem Engine-/Prüfbeleg je Aussage.

Die erwarteten Werte stehen ausschließlich in `akzeptanzfaelle.json`. Der Adapter muss sie unabhängig berechnen. Falsch wäre ein Adapter, der die Sollwerte direkt kopiert, die Lernkoordinaten als Klassifikator verwendet oder lediglich das Vorhandensein der MD-Dateien testet.

Der Ergebnisprüfer vergleicht die Aussagen und prüft Mindestbelege. Er kann nicht beweisen, dass eingetragene Belegtexte wahr sind. Deshalb bleiben Overlay-Sichtprüfung, tatsächliche Objektgeometrie und Reproduktion des Engine-Laufs zwingend Teil der Abnahme.
