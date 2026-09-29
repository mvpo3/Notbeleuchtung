# Bauteile, Räume und Wege im 1. OG erkennen

## Evidenz kombinieren

Eine Linie allein ist noch kein Bauteil. Lies den Originalplan in dieser Reihenfolge: benachbarter Text und seine Zuordnung, geometrischer Aufbau, Anschluss an andere Bauteile, Darstellungsebene und schließlich die Wirkung auf Boden und Durchgang.

Der Text kann das Objekt ausdrücklich benennen. Beispiele sind „Absturzsicherung raumhoch“, „Terrasse“, „Stiege“ und „Pflanzentrog“. Seine Position allein liefert aber keine exakte Objektfläche. Eine Beschriftung kann neben einem Bauteil stehen; ein frei gewählter Rahmen um sie darf keine neue physische Grenze erzeugen.

Halte die Herkunft fest: Originaldatei, DXF-Handle, Text, Koordinaten, Begründung und Status. Eine plausible Klassifizierung und ein vermessener Bauteilumriss sind verschiedene Ergebnisse.

## Mauern und Stützen

M01–M04 zeigen Wandkern, äußere Schichten, Anschlüsse und dünne Trennwände. Mehrere parallele Begrenzungen, Schraffur oder massive Füllung sowie ein durchgehender Anschluss stützen die Wandzuordnung. Bei der Wegeprüfung ist der gesamte Wandaufbau zu berücksichtigen, nicht nur eine Mittellinie.

Eine geschlossene Ecke verhindert auch einen diagonalen Durchtritt. Ein scheinbar kleiner Restspalt kann ein Zeichen- oder Registrierungsfehler sein. Er ist erst dann eine Öffnung, wenn die Quelle ihn als tatsächlichen Durchgang stützt.

Auch dünne WC-Trennwände sperren den direkten Durchtritt. Geringe Dicke ist kein Argument für Boden. Sanitärgegenstände und Schränke haben dagegen eine andere Funktion: Sie belegen Stellfläche innerhalb des Raumes und erzeugen nicht allein einen neuen Raum.

Die rote Lernmarkierung ist keine Materialklassifizierung. Tragend, nicht tragend, Material und Bauteilhöhe dürfen nur aus zusätzlichen Belegen übernommen werden.

## Randsicherungen

M06 und W02 behandeln Geländer, Brüstung und Absturzsicherung. Die aktuelle Darstellung verwendet **rot durchgezogen für Wandkörper** und **rot gestrichelt für Randsicherungen**. Die gestrichelte Lernfarbe ist eine Ergänzung; sie ist nicht automatisch der ursprüngliche CAD-Linientyp.

Im zentralen Innenbereich steht am unteren Rand „Absturzsicherung raumhoch“. Die zugeordnete Begrenzung ist kein freier Durchgang. Der Gang verläuft außen herum. „Raumhoch“ beschreibt die Höhe qualitativ, liefert aber keinen numerischen Wert und kein gesichertes Material wie Glas oder Netz.

Eine Randsicherung kann ein Wegenetz begrenzen, ohne eine massive Raumwand zu sein. Raumgrenzen, durchtrittssperrende Grenzen und sonstige Hindernisse deshalb getrennt speichern.

## Türen

T01–T03 zeigen Anschlag/Drehpunkt, geöffnetes Blatt, Schwenkbogen und die ergänzte geschlossene Stellung. Die Öffnung liegt zwischen den zugehörigen Laibungen beziehungsweise Anschlägen. Der Bogen zeigt die Blattbewegung und ist keine Mauer.

Bei einer zweiflügeligen Tür gehören zwei Blätter und gegebenenfalls unterschiedlich große Bögen zu einer Öffnung. Weit zurückgeschwenkte Flügel vergrößern den baulichen Öffnungsabschnitt nicht.

Eine Personentür verbindet angrenzende Bodenbereiche, wenn beidseitiger Anschluss belegt ist. Prüfe den tatsächlichen Portalabschnitt. Verbindungen durch benachbarte geschlossene Wandstücke sind falsch. Ein geöffneter Flügel darf nicht als dauerhafte zusätzliche Raumtrennwand behandelt werden.

Türmaße aus der Beschriftung separat erfassen. Ein Bogenradius oder die Länge einer Blattlinie ist nicht automatisch die lichte Öffnungsbreite.

## Fenster

F01 und F02 zeigen parallele Rahmenlinien in der Fassade, bewegliche Flügel und den Hinweis `FPH ü. FBOK 0,85`. Die Ausrichtung auf dem Papier verändert die Bauteilklasse nicht.

Ein Kreis- oder Ellipsenbogen kann zu Tür oder Fenster gehören. Entscheidend sind Lage, Anschlüsse, Rahmen, Höhenhinweise und Text. Aus einem Fensterflügel entsteht keine gewöhnliche Personendurchgangskante im Wegenetz.

F03 ist ein Gegenbeispiel: Die X-Felder liegen in einer Schrankreihe vor einer eigenen Innenwand. Diese Kreuzfelder sind hier weder Fenster noch neue Wandkörper.

## Boden, Wege und Endräume

W01, W05 und W06 erklären zusammenhängenden Boden. Erschließung und Terrasse können im Original weiß und ungeschraffiert sein. Nutzungsbezeichnung, Belag, tatsächliche Begrenzungen und Anschluss an Zugänge liefern die Belege.

Begehbarkeit, Erreichbarkeit und Durchgangsfunktion getrennt behandeln:

- Begehbarkeit beschreibt eine nutzbare Bodenfläche an diesem Niveau.
- Erreichbarkeit benötigt eine Verbindung von einem Ausgangsbereich zu dieser Fläche.
- Durchgangsfunktion bedeutet, dass von dort ein weiterer Bereich erreicht werden kann.

W04 zeigt einen Endraum. Eine einzige Tür macht seinen Boden nicht unbegehbar. Man kann hineingehen und durch dieselbe Tür zurückgehen; die gegenüberliegende Wand bleibt geschlossen.

In Z03 wurde ein breiter weißer Balken aus der Beschriftung „Pflanzentrog“ abgeleitet, ohne dass seine vier Kanten als Bauteilkontur belegt waren. Diese Maske ist entfernt. Der Boden reicht an der rechten Seite bis zur gezeichneten Randsicherung und schließt an die Außentreppe an. Ein später nachgewiesener Trog ist mit seiner tatsächlichen Kontur zu berücksichtigen, nicht mit der alten freien Rechteckmaske.

Die grünen Flächen zeigen das Planverständnis. Sie enthalten keine separate Simulation eines Körpers bestimmter Breite. Eine geometrische Körperprüfung darf bei Bedarf auf bestätigten Einheiten aufbauen; die hier enthaltenen Prüfproben sind keine baurechtliche Breitenprüfung.

## Treppen

S01–S04 zeigen wiederholte Stufenkanten, Lauflinie, Anfangsmarke, Pfeilspitze, Podest und Treppenbruch. Der Grundriss zeigt die Projektion; die Seitenansicht auf Seite 58 erklärt den Höhenwechsel.

Die Quelle nennt unter anderem `26 STG 15 / 30` und `31 STG 15 / 30`. Stufenzahl und Steigungsverhältnis als eigene Informationen erfassen. Das Lehrschema auf Seite 58 ist keine maßstäbliche Rekonstruktion eines vollständigen Laufs.

Ein Aufwärts- oder Abwärtsschluss braucht Laufzeichen und Geschossbezug. „Oben im Bild“ ist keine Höhenangabe. Das konkrete Zielgeschoss bleibt offen, wenn es aus diesem Geschossplan nicht eindeutig hervorgeht.

Eine Treppe ist begehbar und erhält zugleich das Merkmal `height_transition`. Sie darf nicht als ebene Abkürzung zwischen übereinanderliegenden Geschossen modelliert werden. Stufen- und Bruchlinien bleiben trotz grüner Füllung lesbar. Ein Treppenbruch ist kein fehlender Bodenabschnitt.

## Lift und technische Bereiche

L01 trennt Schachtwand, Kabine, Haltestellenzugang und technischen Restspalt. Die Kabine ist bedingt betretbar, wenn sie an der Haltestelle steht und zugänglich ist. Der Schacht und der Restspalt werden nicht als gewöhnlicher Gang geführt.

L02 zeigt einen technischen Wartungsbereich. Gitterrost-Wartungssteg, Schachtleiter und Installationen sind keine gewöhnliche Raumerschließung. Technische Zugänglichkeit und normaler Personendurchgang erhalten getrennte Eigenschaften.

## Fremde Planlinien und Projektionen

Blaue Beleuchtungsdiagonalen mit Lux- und Farbtemperaturangaben sind Elektroinformationen. Maßlinien, Textfelder und Gefällelinien sind ebenfalls keine Raumgrenzen. Bei M05 ist die beanstandete Terrassenkontur mit einem Untersichtsbezug verbunden. Solche projizierten Konturen dürfen nicht ungeprüft als Wand auf dem betrachteten Niveau wirken.

Layernamen unterstützen die Einordnung, ersetzen aber keine Prüfung. Die zentrale Absturzsicherung liegt teilweise auf einem Layer für vertikale Verkleidung. Der zugeordnete Originaltext liefert hier die entscheidende zusätzliche Information.
