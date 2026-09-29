# Koordinaten, Datenrollen und Quellenbezug

## Bezugssystem

Alle Lernmarkierungen und Prüfpositionen beziehen sich auf Seite 1 von `Schule_SH22_1_OG.pdf`. Blattgröße: **4268 × 3325 PDF-Punkte**. Ursprung links oben, x nach rechts, y nach unten. Die Kennung lautet `sh22_1og_pdf_pt_top_left`.

Ein PDF-Punkt ist eine Blatteinheit. Er ist keine Länge im Gebäude. Die 1000 × 707 Punkte großen Lernbuchseiten haben ein anderes Layout; Prüfkoordinaten beziehen sich immer auf den Originalplan und niemals auf die Position eines Ausschnitts im Lernbuch.

Die Registrierung steht vollständig in `04_Daten/koordinaten.json`:

```text
pdf_x = 2530.494102783198 + 0.05667995001595397 * cad_x
pdf_y = 2923.3616110185685 - 0.05667995001595397 * cad_y
```

Das Minuszeichen berücksichtigt die umgekehrte y-Richtung. Die inverse Matrix liegt ebenfalls bei. Diese Registrierung gilt nur für das beigefügte Quellpaar.

```bash
python3 06_Werkzeuge/koordinaten.py pdf_to_cad 800 1895
```

Die Original-DXF deklariert `$INSUNITS = 4` (Millimeter). Das ist eine Einheitenangabe im Dateikopf. Lichte Öffnungsbreiten und sonstige reale Nutzmaße wurden mit diesem Paket nicht unabhängig vermessen. Maße aus Text, Blattlinie und Bogenradius nicht ungeprüft gleichsetzen.

## Datenrollen

| Datei | Inhalt und zulässige Verwendung |
|---|---|
| `quellen.json` | Exakte Dateien, SHA-256, Größen, Rollen und PDF-Seitenzahlen |
| `lernfaelle.json` | 24 erklärte Fälle; Buchseiten, Ausschnitt, Lernregel, Zielpunkte und Markierungen |
| `ausschnitte.json` | Ausschnittsrechtecke der Fälle und sieben Übersichtsbereiche |
| `regeln.json` | 15 fachliche Regeln mit zugeordneten Beispielen |
| `korrekturen.json` | Die vier wesentlichen Korrekturgruppen und ihre Belege |
| `prueffaelle.json` | 37 ausgewählte Prüfaussagen für eine spätere Engine-Ausgabe |
| `referenzflaechen_pdf.json` | Die approximierten Flächen der PDF-Lernmarkierung, einschließlich ausgesparter Bereiche |
| `randsicherungen_quelllinien.json` | 1.209 ausgewählte Quelllinien/-kurven für Randsicherungen |
| `quellentexte.json` | 3.074 MTEXT-Fragmente mit Handle, PDF-Position und CAD-Einfügepunkt |
| `quellgeometrie_pdf.json.gz` | Komprimierter Kontext mit 205.070 Top-Level-Elementen |
| `quellanker.json` | Ausgewählte originale Linien- und Texthandles zur Registrierungsprüfung |
| `datenumfang.json` | Maschinenlesbare Angaben zu Umfang und ausdrücklich fehlenden Vollinventaren |

## Markierungen sind nicht automatisch Bauteilflächen

Ein Rechteck in `marks.shape` umrahmt einen Erklärbereich. Ein Pfeilziel nennt eine Stelle, ein Kreis hebt ein Detail hervor, eine ergänzte gestrichelte Linie kann die geschlossene Stellung eines Türblatts erklären. Solche Markierungen sind keine fertigen, vermessenen Bauteilpolygone.

`annotation_geometry_role` macht diese Trennung maschinenlesbar. `source_handles` verweisen auf konkrete Originalelemente. Die Quellkurven im Kontext wurden teilweise als Punktefolge abgetastet; exakte Ellipsenparameter stehen in der DXF.

Die Referenzflächen wurden aus Planinterpretation, Geometrieaufbereitung und manuellen Korrekturen erstellt. Für die Darstellung wurden sie mit maximal 0,25 PDF-Punkten Vereinfachungstoleranz vereinfacht. Sie sind für visuelle Vergleiche geeignet. Sie ersetzen keine vollständige Raumsegmentierung und keine Vermessung.

Ihre Geometrie verwendet die bekannte Struktur `type`/`coordinates` mit Polygonringen und Löchern. Die Koordinaten sind lokal; es handelt sich nicht um geografische Längen- und Breitengrade.

## Vollständige DXF und begrenzter Geometriekontext

Die Original-DXF enthält 206.095 Modelspace-Elemente. Der komprimierte Kontext enthält nur LINE, ELLIPSE, SOLID und MTEXT. **928 INSERTs, 96 CIRCLEs und 1 TEXT** sind darin nicht enthalten. Sie befinden sich weiterhin in der vollständigen Original-DXF. Blöcke und deren Transformationen muss die produktive Engine selbst auswerten.

Die Textfragmente sind zunächst unzugeordnet. Zusammengehörige Wörter können getrennte Handles besitzen. Bei „Absturzsicherung raumhoch“ sind beispielsweise zwei Textobjekte zu verbinden. Der nächste Text ist nicht automatisch die richtige Bezeichnung für jede benachbarte Linie.

Das Paket enthält keine ungesicherten Python-Pickles. Die Daten können als JSON beziehungsweise GZIP-JSON gelesen werden.
