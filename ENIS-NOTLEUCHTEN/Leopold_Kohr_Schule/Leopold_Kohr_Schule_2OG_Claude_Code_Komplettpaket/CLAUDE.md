# Arbeitskontext: SH22-LKS / 2. OG

Du bearbeitest Raumerkennung für das 2. OG der Leopold-Kohr-Schule. Der Auftrag ist, das Lernpaket zu verstehen und danach im bestehenden Projekt einen belegbaren Umsetzungsversuch zu machen. Die Freigabe für das ZIP liegt vor. Fragen nach einer erneuten PDF- oder ZIP-Freigabe sind nicht nötig.

## Lesereihenfolge

1. `START_HIER.md` und `wissen/00_DATEIWEGWEISER.md`.
2. `pdf/2OG_Lernbuch.pdf` und `wissen/01_MAUERN.md` bis `wissen/06_TREPPEN.md`.
3. `wissen/07_FEHLKLASSIFIZIERUNGEN.md`, `wissen/08_DATEN_UND_KOORDINATEN.md` und `wissen/11_GRENZEN_UND_OFFENES.md`.
4. `daten/03_BEISPIELE.json`, `daten/11_PRUEFFAELLE.json`, `daten/14_KLASSEN_UND_REGELN.json`.
5. `wissen/09_UMSETZUNGSPLAN.md` und `wissen/10_ABNAHME.md`, dann den Projektcode.

## Fachliche Arbeitsregeln

- Mauern anhand von Körper, Kanten, Material, Anschluss und Text erkennen. Auch breite Außenwände und dünne feste Trennwände beachten.
- Türen anhand von Öffnung, Blatt/Anschlag, Bogen oder eindeutiger Beschriftung erkennen. Ein Bogen alleine genügt nicht.
- Fenster, Wartungsflügel und Glasgrenzen nicht als gewöhnliche Türen behandeln. Parapet- und Höhenangaben vollständig mitlesen.
- Geländer, Brüstung und Absturzsicherung als eigene Bauteile führen; Wegwirkung und Materialklasse trennen.
- Boden, Hindernisse und Verbindungen getrennt modellieren. Keine erfundenen Durchgänge durch eine Mauer und keine automatische Freigabe von Weißraum.
- Treppen benötigen Stufen, Lauf, Podest und Höhen-/Beschriftungsbelege. Unbekannte Zielgeschosse unbekannt lassen.
- Wenn du Erklärbilder neu ausgibst: geschlossene Rahmen UND Pfeile an jedem erklärten Wandstück, konkrete farbige Tür-/Fenstermerkmale, flächiges Grün, schwarze Originalstufen, Vektoren in PDFs erhalten.

## Umgang mit den Daten

`daten/05_ERKLAERRAHMEN.geojson` ist kein Raum- oder Wandmodell. `daten/06_WAND_LERNKONTUREN.geojson` und `daten/07_BODEN_LERNFLAECHEN.geojson` sind visuelle Referenzen, keine millimetergenaue Wahrheit. Rohdaten nur gezielt lesen; die komplette DXF und Linienliste nicht in den Sprachmodellkontext laden.

## Umsetzung

Die vorhandenen Repo-Anweisungen und die tatsächliche Architektur zuerst prüfen. Unveränderten Ausgangslauf dokumentieren, konkrete Fehler mit Originalbelegen lokalisieren, eine daraus begründete allgemeine Regel ändern und den Effekt vergleichen. Dieses Paket ist kein Ersatz für einen Erkennungslauf.

Die Freigabe betrifft diesen fachlichen Umsetzungsversuch. Bestehende Projektberechtigungen für Veröffentlichungen, Push oder Merge bleiben maßgeblich. Andere Geschosse und parallel bearbeitete Dateien nicht überschreiben. Ergebnisse mit Quelle, Code-Stand, Befehl, tatsächlichem Resultat und offenen Punkten ablegen.
