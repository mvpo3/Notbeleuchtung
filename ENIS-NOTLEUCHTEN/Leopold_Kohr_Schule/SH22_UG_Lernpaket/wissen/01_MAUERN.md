# Mauern und andere feste Begrenzungen

## Was ist eine Mauer im Grundriss?

Eine Mauer bzw. Wand ist ein baulicher Körper mit Dicke und Verlauf. Der Grundriss zeigt häufig seine Schnittfläche und weitere sichtbare oder projizierte Teile. Eine schwarze oder graue Linie allein ist noch keine Wand. Für dieses Lernziel werden gemauerte, massive und andere feste Wandkonstruktionen unter dem Oberbegriff „Wand“ gelesen; ihre Materialart wird nicht ohne Beleg festgelegt.

## Woran erkennt man sie?

Zusammenpassende Merkmale sind begrenzende Kanten, eine zusammenhängende Dicke, Materialschraffuren oder Schichtmuster, Ecken und Anschlüsse an andere Bauteile. Im UG sind besonders mehrschichtige Außenwände mit Diagonalschraffur und Zickzackmuster erkennbar. Mehrere Muster und Linien können zu einer einzigen Wandgruppe gehören. Es müssen nicht alle Merkmale bei jeder Wand vorhanden sein: Auch eine dünne Trennwand kann fest sein.

Die DXF enthält keine bequem auswertbare Liste vollständiger Wandobjekte. Viele Darstellungen sind in Linien und Füllungen zerlegt. Auf Wandlayern liegen auch Türgrafiken. Deshalb würde das pauschale Einfärben eines Wandlayers Türen zusetzen. Die roten Konturen des Pakets gruppieren Materialmuster und wurden abschnittsweise betrachtet.

## Was lässt sich ablesen?

Verlauf, Ecken, Öffnungsunterbrechungen, sichtbare Schichtfolge und Anschlüsse. Exakte Dicke braucht Originalbemaßung oder bestätigte Skalierung. Der DXF-Einheitenkopf allein ist keine ausreichende Kalibrierung. Die rote Markierung liegt geringfügig neben den Originalkanten und ist nicht zum Messen bestimmt.

Tragwirkung, Material, Feuerwiderstand und Wandhöhe nicht allein aus Druckfarbe oder Strichdicke ableiten. Eine Layerbezeichnung wie „tragend“ ist ein Quellenhinweis, keine eigenständige statische Prüfung. Projektionslinien können Bauteile auf anderen Höhen zeigen.

## Was folgt für Raum und Weg?

Die freie Raumfläche endet an der raumseitigen Wandoberfläche. Der Wandkörper zählt nicht als freier Boden. Ecken und Rücksprünge müssen erhalten bleiben. Innerhalb einer mehrschichtigen Wand werden keine begehbaren Mikroräume erzeugt.

Eine Stütze ist ebenfalls ein festes Hindernis, aber kein eigener Raum. Eine niedrige Brüstung kann das gewöhnliche Durchgehen seitlich verhindern, obwohl sie keine deckenhohe Wand ist. Umgekehrt kann ein projiziertes Bauteil unterhalb des Bodens im Grundriss erscheinen, ohne auf dem Laufniveau zu sperren. Höhe und Rolle immer mitlesen.

## UG-Lernfälle

- [M01 – Wand erkennen](../lektionen/M01.md)
- [M02 – Alle Außenwandschichten](../lektionen/M02.md)
- [M03 – Rücksprünge](../lektionen/M03.md)
- [M04 – Dünne feste Trennwände](../lektionen/M04.md)

Der vollständige Kontrollgang führt über Z01–Z08 in `../daten/ausschnitte.json`. Rot ist eine Lernhilfe, keine unabhängig vermessene vollständige Wandobjektliste.
