# Datenbedeutung und Koordinaten

## Zwei Koordinatensysteme

1. DXF: lokale Projektkoordinaten in **mm**, x nach rechts, y nach oben. Negative Koordinaten bleiben erhalten. Keine geografischen Koordinaten.
2. PDF-Suchbereiche: PDF-Punkte, Ursprung links oben, y nach unten, Format `[x0, y0, x1, y1]` auf der unveränderten Seite von `Schule_SH22_EG.pdf`.

Registrierung: `x_pdf = 3398.78476561896 + x_dxf * 0.056691975091847105`; `y_pdf = 2928.9804439164363 - y_dxf * 0.056691975091847105`. Werte nicht auf andere Planversionen übertragen. Jede Ableitung bindet sich an die Quellenprüfsumme.

## Datenklassen

- Regeln: Wissensaussagen, keine ausführbaren Normregeln.
- Beispiele: Belege mit Suchbereich und erklärtem Schluss; Suchbereich ist keine Objektgrenze.
- Prüffälle: noch nicht an eine Engine angebundene Spezifikationen.
- Mauer-GeoJSON: lokale Koordinaten trotz GeoJSON-Form; keine EPSG:4326-Daten. Nur visuelle Umrandung, keine Maße und keine freigegebenen Wandflächen.
- Treppen: EG-Instanzen mit gemeinsamen Anlagen-IDs. Null bei Höhe/Zielgeschoss heißt unbekannt, nicht null Meter oder kein Anschluss.
- Textbelege: DXF-Texte können in mehrere Fragmente zerlegt sein. Zugehörigkeit aus Nähe, Ausrichtung und Kontext bestimmen; nicht blind nach Dateireihenfolge zusammenfügen.

## Spätere Engine-Ausgabe

Pro Objekt sind mindestens ID, Objektklasse, Originalgeometrie, Einheiten, Quell-Handles, Herkunft und Unsicherheitsstatus sinnvoll. Ein Türportal benötigt seine beiden tatsächlich belegten Anschlussseiten. Ein Wegobjekt unterscheidet geometrische Verbindung, Türzustand, Nutzbarkeit und Freigabe. Ein Treppenanschluss benötigt zwei belegte Endpunkte.

Keine API-, Klassennamen oder Dateipfade der tatsächlichen Engine werden hier vorgegeben; erst die bestehende Implementierung prüfen. Beispielhafte Datenschemata nicht ungeprüft als neue Architektur einführen.


## Revision: grüne Flächen und Bildpfeile
`12_GEHFLaECHEN_EG.geojson`: PDF-Punkte, Ursprung links oben, Originalblatt 5227 × 3727 pt. `13_BILDANNOTATIONEN_EG.json`: visuelle Zeigerziele im selben System. Rote Wandkonturen bleiben DXF-mm. Beide sind illustrative Geometrie. Kein automatischer Import als Trainingsmaske.

## Revision 4: geschlossene Rahmen und Originalbögen

`closed_frames` in `daten/13_BILDANNOTATIONEN_EG.json` enthält 38 geschlossene Rechtecke (bei schrägen Wänden gedreht). `polygon_pdf_pt` verwendet Original-PDF-Punkte. `headings` und die `frame_ids` der Zeiger stellen die Textzuordnung her. Die Rolle `Erklaerrahmen_keine_Objektgrenze` ist verbindlich: Der Rahmen grenzt den erklärten Bildbereich ab; er ist keine exakte Wandfläche. Mehrere Randlinien-Erklärungen können denselben Rahmen verwenden.

`source_arc_highlights` enthält 11 zusätzliche farbige Nachzeichnungen nativer DXF-ELLIPSE-Bögen. `handle` und `layer` verweisen auf die Original-DXF. `points` sind mit 0,5 mm Näherungstoleranz abgeflachte Kurven, anschließend in PDF-Punkte transformiert. Ein Bogen bleibt ein Öffnungssymbol, keine Raumgrenze und keine Gehfläche. Die Farbe ist eine Lernmarkierung. Bereits vorhandene Bogenmarkierungen (etwa EG-09) bleiben in den gelieferten Bildern erhalten.
