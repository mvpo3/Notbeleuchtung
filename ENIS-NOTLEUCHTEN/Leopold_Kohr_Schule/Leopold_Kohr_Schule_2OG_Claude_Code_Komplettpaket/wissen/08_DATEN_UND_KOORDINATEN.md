# Datenmodell und Koordinaten

## Drei verschiedene Arten von Geometrie

1. **Originalgeometrie:** DXF-Entities und unveränderte PDF-Vektoren.
2. **Lernreferenzen:** manuelle Bereiche, Materialumrisse, grüne Bodenfüllung, Einbaukonturen und Erklärrahmen.
3. **Spätere Erkennungsergebnisse:** erst durch einen dokumentierten Engine-Lauf erzeugt; derzeit nicht enthalten.

Die Ebenen dürfen nicht vertauscht werden. `ground_truth: false` heißt hier, dass keine exakte vollständige Referenzsegmentierung behauptet wird. Eine menschliche Freigabe des Lernbuchs ist keine metrologische Bestätigung jedes Polygonpunkts.

## Koordinaten

Original-PDF: 4268 × 2953 pt, Ursprung links oben, y nach unten. DXF: Original-Modelspace, deklarierte Einheit mm, y nach oben. Exakte Formel und geschossspezifische Parameter stehen in `daten/02_KOORDINATEN.json`.

Die Parameter wurden an nativen Kontrollsegmenten registriert. Sie dürfen nicht auf EG/UG/1OG oder eine andere Planfassung übertragen werden. Die Registrierung ersetzt keine unabhängige Kontrolle geschriebener Realmaße.

Alle mit `.geojson` benannten Lerngeometrien verwenden **lokale PDF-Koordinaten**, keine geographische Länge/Breite und kein EPSG:4326. Polygone in einem Webkartenprogramm nicht als Orte auf der Erde interpretieren.

## Rohdaten

- `lines.json`: jede Zeile ist `[x1, y1, x2, y2, layer, handle]` in DXF-Modelspace.
- `arcs.json`: ELLIPSE-Daten mit Mittelpunkt, Hauptachsenvektor, Verhältnis und Start-/Endparameter in Radiant. Die Daten enthalten auch kleine Materialschleifen, nicht nur Öffnungsbögen.
- `texts.json`: einzelne originale TEXT-/MTEXT-Texte mit Position, Layer, Handle und Texthöhe.
- `texts_pdf.json`: dieselben Einträge mit zusätzlichem `u, v` im Original-PDF. Mehrteilige Maßbeschriftungen können auf mehrere Einträge verteilt sein.
- `lessons.json`, `annotations.json`: Rohfassung der Buchdaten; benannte konsumierbare Felder liegen in `daten/03_BEISPIELE.json` und `daten/04_ANNOTATIONEN.json`.

## Import in die Engine

Lernrahmen, farbige Pfeile, angedeutete Schließlagen und Konturfüllungen sind keine CAD-Wandobjekte. Produktive Konturen aus dem Original ermitteln. Referenzen nur zum Auffinden, Erklären und Vergleichen verwenden.

Ein mögliches Ergebnisformat liegt in `schemata/ERKENNUNGSERGEBNIS.schema.json`. Es ist ein Austauschformat dieses Pakets, keine Behauptung über ein bereits vorhandenes Repo-API. Ein vorhandenes Format darf über einen dokumentierten Adapter angebunden werden.
