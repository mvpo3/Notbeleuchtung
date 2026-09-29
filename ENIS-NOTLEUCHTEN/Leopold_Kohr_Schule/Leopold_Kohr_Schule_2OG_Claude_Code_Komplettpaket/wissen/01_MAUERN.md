# Mauern und feste Körper erkennen

Eine Mauer ist hier ein räumlicher Körper, der den Durchgang verhindert. Für die Klassifikation werden mindestens Körper-/Kantenbeleg und örtlicher Kontext zusammen benötigt. Eine dicke Linie alleine reicht nicht.

## Positive Merkmale

- Zwei passende Begrenzungen umschließen einen Streifen; Materialschraffuren liegen innerhalb dieses Streifens.
- Der Streifen setzt sich über Anschlüsse und Gebäudeecken nachvollziehbar fort.
- Außenwände umfassen den ganzen erkennbaren Aufbau, einschließlich breiter Bekleidungs-/Dämmbereiche; nicht nur die dunkelste Linie.
- Innenwände trennen Bodenbereiche. Schmale feste Trennwände und massive Stützen sind ebenfalls Hindernisse.
- Originaltexte und CAD-Layer stützen die Zuordnung. Ein Layer allein ersetzt keinen geometrischen und semantischen Beleg.

## Beispiele

W01/W02 zeigen Außenwand und Ecke; W03 die Innenwand zwischen Nutzbereichen; W04 den Anschluss im Kern; W05 dünne Kabinentrennwände; W06 die Aufzug-Schachtwand; W07 eine Stütze. Im Lernbuch sind dies die Seiten 7 bis 13.

## Was kein Mauerbeweis ist

Möbelraster, Bemaßung, Tür- und Fensterbögen, Gefällelinien, Treppenbruch und Decken-/Voutenhinweise dürfen nicht automatisch zu Mauern werden. Brüstungen, Geländer und Absturzsicherungen haben eine eigene Klasse, auch wenn sie den Weg sperren.

## Markierungsregel

Ein erklärtes Wandstück erhält einen geschlossenen rechteckigen Rahmen und einen zugeordneten Pfeil. Bei schrägen Bauteilen ist ein passend gedrehter Rahmen sinnvoll. Der Rahmen muss das tatsächlich erklärte Material zeigen und darf nicht nur ins leere Zentrum eines benachbarten Schachts zeigen. Die rote Gesamtkontur ist eine Lernkontur, keine Vermessung.

## Datenregel

Eine visuelle Kontur kann mehrere Wandstücke zusammenfassen oder einen Wandaufbau in mehrere Teile zerlegen. Deshalb ist die Zahl der Features in `daten/06_WAND_LERNKONTUREN.geojson` keine Zahl erkannter Wände. Keine synthetische Türöffnung aus einem kleinen Konturspalt erzeugen.
