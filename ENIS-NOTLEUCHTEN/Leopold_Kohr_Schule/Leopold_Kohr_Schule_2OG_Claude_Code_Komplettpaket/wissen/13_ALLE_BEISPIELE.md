# Alle 25 Beispiele als lesbarer Text

Die Beispiele entsprechen dem freigegebenen Buch. Koordinaten beziehen sich auf das Originalblatt.

## W01 - Außenmauer: Ecke und Wandkörper

Lernbuch Seite 7; Detail-PDF Seite 1. Bild: `bilder/W01.png`. Originalausschnitt: `[25, 25, 415, 330]`.

### Warum Mauer?

Zwei Begrenzungen, Materialzeichnung und der durchgehende Anschluss an der Ecke bilden gemeinsam einen Wandkörper. Eine einzelne dicke Linie wäre als Beleg zu wenig.

### Von außen nach innen

Fassadenbekleidung, Dämmung und innerer Wandanteil gehören zum Aufbau. Die rote Gesamtmarkierung umfasst die erkennbaren Materialbereiche.

### Wegentscheidung

Der Körper kann diesen Wandstreifen nicht durchqueren. Auch die Fensteröffnung daneben verbindet nicht automatisch zwei Gehflächen.

### Markierungen

- **Außenkante** (blue): Die äußere Begrenzung läuft um die Gebäudeecke. Ziel `[47, 130]`, geschlossener Rahmen `[38, 90, 53, 190]`.
- **Material** (red): Die Schraffur liegt innerhalb des Wandkörpers. Ziel `[67, 220]`, geschlossener Rahmen `[53, 183, 83, 278]`.
- **Innenkante** (purple): Diese Kante grenzt die Mauer vom Raumboden ab. Ziel `[80, 250]`, geschlossener Rahmen `[75, 201, 88, 280]`.
- **Öffnung** (orange): Das Fenster unterbricht die Mauer; es ist kein freier Durchgang. Ziel `[283, 63]`, geschlossener Rahmen `[247, 47, 316, 77]`.

## W02 - Breite Außenwand: den ganzen Aufbau lesen

Lernbuch Seite 8; Detail-PDF Seite 2. Bild: `bilder/W02.png`. Originalausschnitt: `[1000, 22, 1580, 330]`.

### Warum die ganze Breite?

Nicht nur die auffälligste Linie sperrt den Weg. Der mehrschichtige Wandkörper reicht von seiner inneren bis zur äußeren Begrenzung.

### Was die Schraffur sagt

Sie stützt die Materialinterpretation. Den genauen Baustoff oder die Tragfähigkeit allein aus einem beliebigen Schraffurmuster festzulegen wäre zu weitgehend.

### Öffnungen separat

Unterbrechungen mit Rahmen, Glaslinien und Flügeln werden als Fenster untersucht. Die rote Kontur darf eine solche Öffnung nicht als durchgehendes Mauerstück schließen.

### Markierungen

- **Breiter Aufbau** (red): Der Rahmen umfasst den Wandquerschnitt mit seinen Schichten. Ziel `[1340, 64]`, geschlossener Rahmen `[1250, 40, 1440, 85]`.
- **Dämmung** (orange): Wiederholte Schleifen und Schräglinien liegen zwischen den Kanten. Ziel `[1400, 51]`, geschlossener Rahmen `[1340, 39, 1450, 61]`.
- **Eckanschluss** (blue): Die Außenmauer setzt sich am rechten Gebäuderand fort. Ziel `[1540, 120]`, geschlossener Rahmen `[1521, 80, 1562, 240]`.
- **Raumseite** (green): Auf der Innenseite beginnt die Bodenfläche des Bildungsraums. Ziel `[1460, 190]`, geschlossener Rahmen `[1400, 140, 1500, 225]`.

## W03 - Innenwand zwischen zwei Nutzbereichen

Lernbuch Seite 9; Detail-PDF Seite 3. Bild: `bilder/W03.png`. Originalausschnitt: `[555, 170, 730, 520]`.

### Warum Innenwand?

Der schraffierte Körper liegt zwischen Raumflächen und besitzt nachvollziehbare Anschlüsse. Er ist nicht bloß eine Raumstempellinie oder die Kante eines Tisches.

### Nicht jede Nachbarlinie zählt

Schrank-, Tisch- und Installationskonturen können dicht an einer Wand liegen. Sie dürfen die erkannte Wand nicht beliebig verbreitern.

### Für die Raumerkennung

Diese Wand trennt Bodenbereiche. Erst eine belegte Öffnung kann an einer bestimmten Stelle eine Verbindung herstellen.

### Markierungen

- **Wandstreifen** (red): Die beiden Kanten fassen einen schraffierten Streifen ein. Ziel `[598, 350]`, geschlossener Rahmen `[585, 284, 613, 421]`.
- **Zwei Seiten** (blue): Links und rechts schließen verschiedene Bodenbereiche an. Ziel `[603, 250]`, geschlossener Rahmen `[585, 210, 614, 276]`.
- **Anschluss** (orange): Die Innenwand trifft am unteren Ende auf den Queraufbau. Ziel `[598, 478]`, geschlossener Rahmen `[580, 451, 623, 503]`.
- **Einbau daneben** (purple): Möbellinien sind eigenständige Objekte, keine Fortsetzung der Wand. Ziel `[647, 205]`, geschlossener Rahmen `[622, 177, 698, 253]`.

## W04 - Wandanschlüsse im inneren Kern

Lernbuch Seite 10; Detail-PDF Seite 4. Bild: `bilder/W04.png`. Originalausschnitt: `[610, 610, 1007, 940]`.

### Warum Mauer?

Materialdarstellung und Kanten setzen sich bis in den Anschluss fort. Ein sichtbares Wandende ist nicht automatisch eine Türlaibung.

### Was offen bleibt

Im benachbarten Wartungsbereich sind Zugang und Niveau gesondert zu prüfen. Er wird nicht wie ein normaler Flur behandelt.

### Wichtig für die Markierung

Jedes erklärte Wandstück ist zusätzlich rechteckig eingerahmt. Der Pfeil ordnet den Text genau diesem Ausschnitt zu.

### Markierungen

- **Seitliche Mauer** (red): Der schraffierte Wandkörper läuft entlang des Kerns. Ziel `[648, 818]`, geschlossener Rahmen `[633, 786, 660, 885]`.
- **Querwand** (red): Ein geschlossener Rahmen markiert das erklärte Querwandstück. Ziel `[804, 908]`, geschlossener Rahmen `[710, 897, 907, 922]`.
- **Anschluss** (orange): Hier treffen Längs- und Querwand ohne Durchgang aufeinander. Ziel `[649, 908]`, geschlossener Rahmen `[633, 894, 671, 926]`.
- **Sonderbereich** (purple): Die Beschriftung nennt einen Gitterrost-Wartungssteg. Ziel `[805, 850]`, geschlossener Rahmen `[710, 817, 899, 887]`.

## W05 - Dünne feste Trennwand bleibt ein Hindernis

Lernbuch Seite 11; Detail-PDF Seite 5. Bild: `bilder/W05.png`. Originalausschnitt: `[1195, 605, 1425, 750]`.

### Warum trotz geringer Dicke?

Eine feste Kabinentrennwand lässt sich nicht durchqueren. Ihre geringe Zeichnungsbreite ist kein Beleg für einen freien Weg.

### Bauteilklasse sauber halten

Hier handelt es sich um eine dünne Trennwand. Daraus folgt keine Aussage, dass sie gemauert oder tragend wäre.

### Tür unterscheiden

Ein bewegliches Blatt steht in einer Öffnung. Die feststehende Trennwand daneben bleibt ein Hindernis, auch bei offener Tür.

### Markierungen

- **Dünne Trennwand** (red): Zwei eng benachbarte Linien begrenzen das feste Trennwandstück. Ziel `[1276.4, 694]`, geschlossener Rahmen `[1271, 670, 1282, 724]`.
- **Zweites Beispiel** (red): Dasselbe Merkmal wiederholt sich an der nächsten Kabine. Ziel `[1325.7, 694]`, geschlossener Rahmen `[1320, 670, 1331, 724]`.
- **Türblatt** (blue): Die bewegliche Linie im Öffnungsbereich ist keine feste Mauer. Ziel `[1322, 639]`, geschlossener Rahmen `[1317, 611, 1328, 657]`.
- **Raumbegrenzung** (orange): Die seitliche und untere Einfassung schließt an feste Bauteile an. Ziel `[1248, 733]`, geschlossener Rahmen `[1210, 725, 1300, 744]`.

## W06 - Schachtwand und Aufzug getrennt erkennen

Lernbuch Seite 12; Detail-PDF Seite 6. Bild: `bilder/W06.png`. Originalausschnitt: `[1175, 1195, 1330, 1510]`.

### Warum ein Schacht?

Die umschließenden Wände, die eingezeichnete Kabine und die Beschriftung gehören zusammen. Ein weißes Rechteck innerhalb einer Wand ist kein automatisch begehbarer Raum.

### Aufzug nicht als Treppe

Der Aufzug ist eine eigene vertikale Verbindung mit Betriebszustand. Es gibt hier keine Folge von Stufenkanten.

### Grüne Fläche

Der Schacht bleibt ausgespart. Ein Weg endet an der Aufzugstür, bis eine gesonderte Aufzugsverbindung modelliert ist.

### Markierungen

- **Feste Schachtwand** (red): Der Rahmen umfasst den massiven seitlichen Wandstreifen. Ziel `[1213, 1320]`, geschlossener Rahmen `[1200, 1260, 1221, 1396]`.
- **Kabine** (blue): Die inneren Linien beschreiben den Aufzug, keinen Flur. Ziel `[1260, 1300]`, geschlossener Rahmen `[1228, 1260, 1295, 1377]`.
- **Türzone** (orange): Nur hier liegt der Zugang; nicht entlang der ganzen Schachtseite. Ziel `[1260, 1242]`, geschlossener Rahmen `[1223, 1232, 1298, 1255]`.
- **Bauteilbeleg** (purple): FWA und die Kabinenangaben stützen die Zuordnung. Ziel `[1261, 1287]`, geschlossener Rahmen `[1238, 1272, 1295, 1300]`.

## W07 - Massive Stütze in einer Außenfläche

Lernbuch Seite 13; Detail-PDF Seite 7. Bild: `bilder/W07.png`. Originalausschnitt: `[665, 1735, 770, 1865]`.

### Warum rot?

Die Stütze ist ein massiver Körper im Bewegungsraum. Für die Raumerkennung gehört sie zu den festen Hindernissen, auch wenn sie keinen ganzen Raum abtrennt.

### Nicht übermalen

Die grüne Bodenfüllung spart den Stützenkörper aus. Das ist ein Unterschied zu einer Flächenfüllung ohne Hindernisabzug.

### Maße lesen

Die schriftliche Angabe dient als Hinweis. Das verkleinerte Lernblatt ist keine maßstäbliche Messgrundlage.

### Markierungen

- **Stützenkörper** (red): Ein kleiner geschlossener Körper mit Materialdarstellung. Ziel `[706, 1824]`, geschlossener Rahmen `[691, 1808, 722, 1840]`.
- **Eigenes Hindernis** (orange): Auch ohne lange Wand ist der Körper nicht durchquerbar. Ziel `[713, 1820]`, geschlossener Rahmen `[687, 1804, 726, 1843]`.
- **Maßhinweis** (blue): Die nahe Angabe 43/43 gehört zur Stütze. Ziel `[718, 1838]`, geschlossener Rahmen `[703, 1830, 741, 1848]`.
- **Umgehbare Fläche** (green): Die Bodenfläche neben der Stütze ist gesondert erkennbar. Ziel `[752, 1830]`, geschlossener Rahmen `[739, 1818, 765, 1852]`.

## W08 - Absturzsicherung und Brüstung sind eigene Bauteile

Lernbuch Seite 14; Detail-PDF Seite 8. Bild: `bilder/W08.png`. Originalausschnitt: `[1690, 1100, 2610, 1530]`.

### Warum nicht pauschal Mauer?

Eine Brüstung oder Absturzsicherung begrenzt den Körperweg, ist aber eine andere Bauteilklasse als eine massive geschosshohe Wand. Die Originalbeschriftung entscheidet mit.

### Keine grüne Abkürzung

Die große umwehrte Fläche wird nicht als durchgehend betretbarer Boden eingefärbt. Die schräge Brückendarstellung wird ohne bestätigten Höhenanschluss nicht als 2.-OG-Route freigegeben.

### Lernregel

Bauteil und Wegwirkung getrennt speichern: Geländer kann den Durchgang sperren, ohne ein Mauerobjekt zu sein.

### Markierungen

- **Absturzsicherung** (purple): Der Text benennt die Umwehrung ausdrücklich. Ziel `[1815, 1458]`, geschlossener Rahmen `[1780, 1446, 1880, 1470]`.
- **Raumhohe Grenze** (purple): Diese Kante wird nicht als massive Mauer umgedeutet. Ziel `[1736, 1320]`, geschlossener Rahmen `[1725, 1210, 1745, 1410]`.
- **Brüstung** (orange): Die nahe Beschriftung lautet Brüstung H=120cm. Ziel `[2160, 1174]`, geschlossener Rahmen `[2128, 1148, 2205, 1206]`.
- **Brückenbereich** (blue): Der schräge Bereich braucht einen belegten Niveauanschluss. Ziel `[2275, 1305]`, geschlossener Rahmen `[2215, 1260, 2340, 1360]`.

## D01 - Tür: Blatt, Drehpunkt, Bogen und Schließlage

Lernbuch Seite 15; Detail-PDF Seite 9. Bild: `bilder/D01.png`. Originalausschnitt: `[400, 420, 625, 545]`.

### Warum eine Tür?

Die Unterbrechung im Wandaufbau, ein am Anschlag drehendes Blatt und der zugehörige Bogen liefern gemeinsam den Beleg.

### Drehpunkt und Bogen

Der Drehpunkt liegt am Anfang des blauen Blatts. Der orange Bogen beschreibt dessen Bewegung. Er ist keine gekrümmte Wand und keine Weglinie.

### Wann ist der Weg offen?

Bei geöffneter Tür verbindet die Öffnung die beiden Bodenbereiche. Der tatsächliche Türzustand und die benötigte Körperbreite werden zusätzlich geprüft.

### Markierungen

- **Wandlaibung** (red): Der eingerahmte Wandabschluss begrenzt die Öffnung. Ziel `[452, 482]`, geschlossener Rahmen `[446, 455, 459, 502]`.
- **Türblatt** (blue): Blau liegt direkt auf der gezeichneten Blattlage. Ziel `[460.64, 490]`, geschlossener Rahmen `[456, 468, 466, 517]`.
- **Schwenkbogen** (orange): Orange zeichnet den originalen Öffnungsbogen nach. Ziel `[494.45, 501.7]`, geschlossener Rahmen `[483, 488, 507, 516]`.
- **Gedacht geschlossen** (purple): Violett gestrichelt: gedachte Schließlage, keine zusätzliche Mauer. Ziel `[483, 467.9]`, geschlossener Rahmen `[461, 462, 509, 475]`.

## D02 - Türangaben: Öffnung und Höhe nicht verwechseln

Lernbuch Seite 16; Detail-PDF Seite 10. Bild: `bilder/D02.png`. Originalausschnitt: `[445, 440, 565, 530]`.

### Was der Plan angibt

An dieser Tür stehen DL 90 und DL 210. Die Zuordnung ist eine lichte Breite von 90 cm und eine lichte Höhe von 210 cm in der üblichen Maßangabe dieses Plans.

### Andere Bezugshöhe

STUK ü. FBOK +2,18 bezeichnet die Sturzunterkante über dem Fertigboden. Das ist nicht dieselbe Größe wie die lichte Türhöhe.

### Für Claude Code

Türkennung und Originaltexte mitführen. Geschriebene Maße nicht durch Abmessen an der verkleinerten Buchseite ersetzen.

### Markierungen

- **DL 90** (blue): Die erste DL-Angabe benennt die lichte Breite. Ziel `[478.2, 483]`, geschlossener Rahmen `[474, 474, 482, 496]`.
- **DL 210** (orange): Die zweite DL-Angabe benennt die lichte Höhe. Ziel `[484.7, 485]`, geschlossener Rahmen `[481, 474, 489, 496]`.
- **STUK +2,18** (purple): Unterkante des Sturzes über der Oberkante des Fertigbodens. Ziel `[514, 456.8]`, geschlossener Rahmen `[483, 450, 544, 463]`.
- **Türkennung** (green): 2.17-358 / TI A 01 identifiziert das Türelement. Ziel `[485, 506]`, geschlossener Rahmen `[470, 497, 497, 514]`.

## D03 - Zweiflügelige Tür zur Stiegenerschließung

Lernbuch Seite 17; Detail-PDF Seite 11. Bild: `bilder/D03.png`. Originalausschnitt: `[1040, 1000, 1230, 1200]`.

### Warum zwei Flügel?

Zwei Drehpunkte und zwei zugehörige Bewegungsbögen bilden eine gemeinsame Türöffnung. Sie sind nicht zwei voneinander unabhängige Räume.

### Öffnungsweite

Die gezeichnete Flügelstellung zeigt die Konstruktion. Für einen Körperweg ist die nutzbare lichte Öffnung maßgeblich, nicht die gesamte Bogenfläche.

### Verbindung

Hier wird die Erschließung mit dem Vorbereich von Stiege 2 verbunden. Die Treppe dahinter erhält eine eigene Verbindungsklasse.

### Markierungen

- **Zwei Anschläge** (blue): Je ein Flügel gehört zum oberen und unteren Anschlag. Ziel `[1117.45, 1034.99]`, geschlossener Rahmen `[1108, 1027, 1126, 1140]`.
- **Zwei Bögen** (orange): Beide orange Kurven stammen aus der Originalzeichnung. Ziel `[1150, 1067]`, geschlossener Rahmen `[1120, 1036, 1168, 1126]`.
- **Öffnungsstreifen** (green): Die Passage liegt zwischen den Anschlägen in der Wandebene. Ziel `[1117.45, 1083]`, geschlossener Rahmen `[1107, 1039, 1127, 1127]`.
- **Feste Wand** (red): Der feste Anschluss oberhalb der Tür bleibt vom Bogen getrennt. Ziel `[1121.3, 1015]`, geschlossener Rahmen `[1096, 1003, 1130, 1029]`.

## D04 - Glasabschluss: durchsichtig heißt nicht durchgehbar

Lernbuch Seite 18; Detail-PDF Seite 12. Bild: `bilder/D04.png`. Originalausschnitt: `[505, 1400, 1120, 1545]`.

### Warum kein offener Weg?

Ein Glasfeld kann Sicht zulassen und trotzdem den Körperweg sperren. Mehrere Rahmenlinien ohne Türbeleg werden nicht als offene Passage behandelt.

### Tür gezielt suchen

Ein tatsächlich beweglicher Durchgang braucht eigene Flügel-, Öffnungs- oder Bauteilbelege. Nicht jedes Fassadenfeld ist eine Tür.

### Grüne Flächen

Innen- und Außenboden können beide grün sein. Eine feste Trennlinie dazwischen verhindert trotzdem eine direkte Verbindung.

### Markierungen

- **Fester Glasabschluss** (purple): Die durchgehende Rahmenzone bildet hier eine Grenze. Ziel `[824, 1488]`, geschlossener Rahmen `[680, 1475, 968, 1504]`.
- **Rahmen / Pfosten** (blue): Senkrechte Teilungen gehören zum Fassadenelement. Ziel `[740, 1487]`, geschlossener Rahmen `[734, 1477, 749, 1504]`.
- **Innenboden** (green): Die Erschließung liegt auf der Innenseite. Ziel `[820, 1440]`, geschlossener Rahmen `[775, 1410, 883, 1461]`.
- **Außenbereich** (orange): Die Freiklasse liegt jenseits des Abschlusses. Ziel `[816, 1530]`, geschlossener Rahmen `[767, 1511, 890, 1542]`.

## F01 - Fenster mit Öffnungsbogen: keine Tür

Lernbuch Seite 19; Detail-PDF Seite 13. Bild: `bilder/F01.png`. Originalausschnitt: `[235, 27, 380, 160]`.

### Warum ein Fenster?

Die Lage in der Außenfassade, die Rahmen-/Glaslinien und der Höhenhinweis passen zusammen. Ein Bogen allein würde Tür und Fenster nicht sicher unterscheiden.

### Kein Körperdurchgang

Die angegebene Fertigparapethöhe liegt über dem Boden. Diese Öffnung ist deshalb nicht als bodengleiche Türpassage zu behandeln.

### Markierungen

Blau hebt Rahmen und Flügel hervor. Orange folgt dem originalen Bogen. Der Textpfeil benennt den zusätzlichen Höhenbeleg.

### Markierungen

- **Rahmen und Glas** (blue): Mehrere dünne parallele Linien liegen in der Außenöffnung. Ziel `[280, 65]`, geschlossener Rahmen `[250, 57, 313, 75]`.
- **Fensterflügel** (blue): Der gezeichnete Flügel liegt am Rahmenanschlag. Ziel `[313.68, 99]`, geschlossener Rahmen `[309, 66, 319, 127]`.
- **Öffnungsbogen** (orange): Auch ein Fenster kann einen Viertelkreisbogen haben. Ziel `[270.8, 106.9]`, geschlossener Rahmen `[252, 82, 312, 128]`.
- **Parapethöhe** (purple): FPH ü. FBOK 0,85 bezeichnet die Fensterbrüstungshöhe. Ziel `[285, 85.5]`, geschlossener Rahmen `[255, 77, 309, 91]`.

## F02 - Fensterhöhen: Rohbau und Fertigboden unterscheiden

Lernbuch Seite 20; Detail-PDF Seite 14. Bild: `bilder/F02.png`. Originalausschnitt: `[385, 25, 625, 150]`.

### Was ablesbar ist

Die Originalangaben unterscheiden RPH über Rohdeckenoberkante und FPH über Fertigbodenoberkante. Der FPH-Wert 0,85 ist hier unmittelbar lesbar.

### Hochgestellte Ziffer

Bei der RPH steht eine hochgestellte 5 hinter 1,18. Solche Maßschreibweisen vollständig erhalten; nicht beim OCR wegwerfen oder zu einer neuen Maßzahl zusammenziehen.

### Wegentscheidung

Die Fensterzone bleibt als Barriere erhalten. Weder ein großer Fensterflügel noch eine transparente Glaslinie beweist eine Gehöffnung.

### Markierungen

- **RPH** (orange): Rohparapethöhe wird auf RDOK bezogen. Ziel `[465, 80]`, geschlossener Rahmen `[435, 74, 491, 83]`.
- **FPH 0,85** (purple): Fertigparapethöhe wird auf FBOK bezogen. Ziel `[465, 85.5]`, geschlossener Rahmen `[435, 82, 487, 92]`.
- **Glaslinien** (blue): Die eng benachbarten Linien markieren das Fassadenfeld. Ziel `[521, 64]`, geschlossener Rahmen `[493, 56, 548, 75]`.
- **Wandstück** (red): Materialzeichnung zwischen den Öffnungen bleibt ein fester Körper. Ziel `[576, 54]`, geschlossener Rahmen `[557, 39, 603, 77]`.

## F03 - Wartungsflügel mit begrenzter Öffnung

Lernbuch Seite 21; Detail-PDF Seite 15. Bild: `bilder/F03.png`. Originalausschnitt: `[995, 25, 1135, 155]`.

### Text vor Vermutung

Im Plan steht Wartungsflügel mit Öffnungsbegrenzer, angetrieben durch BMA. Diese Funktion darf nicht durch eine reine Bogen-Erkennung zu einer Tür werden.

### Geometrie und Semantik

Der kurze Bogen und die Beschriftung erklären denselben Bauteilbereich. Beide Hinweise werden zusammen dokumentiert.

### Erkennungsregel

Fenster, Wartungsöffnung und Tür bekommen unterschiedliche Klassen. Nur eine belegte begehbare Öffnung verbindet reguläre Bodenbereiche.

### Markierungen

- **Wartungsflügel** (purple): Die Beschriftung nennt die Funktion ausdrücklich. Ziel `[1090, 81]`, geschlossener Rahmen `[1063, 75, 1131, 98]`.
- **Kleiner Bogen** (orange): Der kurze Originalbogen zeigt eine begrenzte Flügelstellung. Ziel `[1054, 73]`, geschlossener Rahmen `[1048, 63, 1068, 84]`.
- **Rahmenzone** (blue): Der Flügel sitzt in der Fassadenöffnung. Ziel `[1080, 65]`, geschlossener Rahmen `[1047, 54, 1116, 77]`.
- **Begrenzung** (red): Ein Wartungsflügel ist kein normaler Türdurchgang. Ziel `[1117, 95]`, geschlossener Rahmen `[1112, 79, 1128, 143]`.

## G01 - Zusammenhängender Weg im westlichen Cluster

Lernbuch Seite 22; Detail-PDF Seite 16. Bild: `bilder/G01.png`. Originalausschnitt: `[440, 480, 1125, 1480]`.

### Warum ein Weg?

Die Quelle bezeichnet die Zone als Erschließung. Zusätzlich ist ein zusammenhängender Bodenstreifen ohne querende Mauer erkennbar.

### Wie weiter?

Die Verbindung läuft um den festen Kern. Raumzugänge werden an ihren Türen erkannt; durch den Kern selbst gibt es keinen beliebigen Durchgang.

### Grün richtig lesen

Die Füllung beschreibt interpretierte Bodenflächen. Sie ersetzt keine Prüfung der realen Möblierung, Türzustände oder erforderlichen Körperbreite.

### Markierungen

- **Flurfläche** (green): Die grüne Füllung folgt dem Boden seitlich am Kern vorbei. Ziel `[557, 1050]`, geschlossener Rahmen `[521, 941, 606, 1190]`.
- **Türverbindung** (blue): An einer nachgewiesenen Tür kann der Weg in den Raum wechseln. Ziel `[639, 953]`, geschlossener Rahmen `[612, 907, 686, 999]`.
- **Wandgrenze** (red): Die eingerahmte Querwand wird nicht grün überbrückt. Ziel `[805, 1250]`, geschlossener Rahmen `[710, 1224, 917, 1266]`.
- **Zweite Flurseite** (green): Ein weiterer Bodenstreifen erschließt die andere Kernseite. Ziel `[1040, 1110]`, geschlossener Rahmen `[1002, 1015, 1085, 1210]`.

## G02 - Mittelzone: am Rand entlang statt über die Öffnung

Lernbuch Seite 23; Detail-PDF Seite 17. Bild: `bilder/G02.png`. Originalausschnitt: `[1520, 995, 2710, 1640]`.

### Wegbeleg

Der Raumstempel 2.004 benennt die Erschließung. Die Bodenflächen um den umwehrten Bereich können als zusammenhängende Zone untersucht werden.

### Keine weiße Fläche erraten

Große freie Zeichenflächen können einen Luftraum, eine andere Ebene oder eine Sonderkonstruktion darstellen. Weiß allein beweist keinen begehbaren Boden.

### Brücke separat

Die schräge Darstellung wird als eigener Kandidat geführt. Für eine nutzbare Verbindung auf diesem Geschoss fehlen hier bestätigte Anschluss- und Höhenbelege.

### Markierungen

- **Oberer Umgang** (green): Der Bodenstreifen verbindet die Seiten der Erschließung. Ziel `[2040, 1094]`, geschlossener Rahmen `[1880, 1052, 2230, 1123]`.
- **Unterer Umgang** (green): Auch der untere Streifen wird flächig dargestellt. Ziel `[2090, 1541]`, geschlossener Rahmen `[1920, 1498, 2260, 1580]`.
- **Feste Grenze** (purple): Die Absturzsicherung unterbricht den direkten Körperweg. Ziel `[1736, 1280]`, geschlossener Rahmen `[1724, 1198, 1748, 1410]`.
- **Ungeklärter Anschluss** (orange): Die Brückendarstellung ist kein pauschaler Bodenfüllbereich. Ziel `[2220, 1290]`, geschlossener Rahmen `[1995, 1146, 2480, 1480]`.

## G03 - Endraum: hinein und auf demselben Weg zurück

Lernbuch Seite 24; Detail-PDF Seite 18. Bild: `bilder/G03.png`. Originalausschnitt: `[62, 62, 617, 542]`.

### Sackgasse bedeutet nicht unbegehbar

Der Bildungsraum 2.17 ist über seine eingezeichnete Tür erreichbar. Als Durchgangsroute endet der Weg jedoch im Raum.

### Warum Ende?

Die übrigen Seiten zeigen Wände bzw. Fenster. Eine weitere reguläre Tür ist im dargestellten Raum nicht belegt.

### Rückweg

Zum Verlassen wird derselbe Türzugang benutzt. Eine Raumerkennung muss Endräume und gesperrte Flächen unterschiedlich behandeln.

### Markierungen

- **Ein belegter Zugang** (green): Die Tür 2.17-358 liegt am unteren Raumrand. Ziel `[460.64, 467.9]`, geschlossener Rahmen `[448, 453, 517, 520]`.
- **Raumboden** (green): Die freie Fläche zwischen den Einbauten kann betreten werden. Ziel `[408, 293]`, geschlossener Rahmen `[380, 233, 434, 337]`.
- **Fester Abschluss** (red): Die Innenwand bietet hier keinen weiteren Durchgang. Ziel `[598, 267]`, geschlossener Rahmen `[584, 216, 615, 346]`.
- **Fenster bleibt Grenze** (purple): Die Außenöffnung ist wegen des Parapets keine Ausgehtür. Ziel `[281, 65]`, geschlossener Rahmen `[247, 49, 315, 88]`.

## G04 - Wartungssteg ist kein normaler Flur

Lernbuch Seite 25; Detail-PDF Seite 19. Bild: `bilder/G04.png`. Originalausschnitt: `[620, 730, 1005, 933]`.

### Was unterscheidet den Bereich?

Die Quelle nennt Wartung und Stahlunterkonstruktion. Das ist ein Funktionshinweis, der eine pauschale Gleichsetzung mit dem regulären Flur verhindert.

### Kein erfundener Normalweg

Zugänglichkeit, Nutzungsberechtigung und Höhenlage müssen für diesen Sonderbereich gesondert belegt werden.

### Lernen für ähnliche Stellen

Die gleiche Regel gilt für die weiteren bezeichneten Wartungsbereiche bei den Kernen. Schwarze schräge Darstellungen darin sind nicht automatisch neue Mauern.

### Markierungen

- **Originaltext** (purple): Gitterrost-Wartungssteg steht direkt im Bereich. Ziel `[800, 855]`, geschlossener Rahmen `[710, 813, 911, 889]`.
- **Eigener Zugang** (orange): Die beschriftete Öffnung gehört zum Wartungsbereich. Ziel `[980, 870]`, geschlossener Rahmen `[968, 836, 998, 906]`.
- **Wand unten** (red): Das feste Querwandstück bleibt eingerahmt und gesperrt. Ziel `[805, 907]`, geschlossener Rahmen `[710, 897, 910, 924]`.
- **Sonderfläche** (blue): Diese Fläche wird nicht als gewöhnlicher Gehbereich grün gefüllt. Ziel `[838, 797]`, geschlossener Rahmen `[772, 782, 921, 815]`.

## G05 - Außenboden, Stütze und Absturzsicherung

Lernbuch Seite 26; Detail-PDF Seite 20. Bild: `bilder/G05.png`. Originalausschnitt: `[490, 1460, 1565, 1980]`.

### Warum Außenboden?

Die Bereiche sind als Freiklasse bzw. Erschließung von Stiege 4 bezeichnet. Der Plan enthält dazu Boden- und Gefällehinweise.

### Wohin nicht?

Absturzsicherungen und feste Stützen sind Grenzen des Körperwegs. Ein außen liegender Bereich ist deshalb nicht vollständig frei durchquerbar.

### Gefälle ist keine Stufe

Lange Gefällelinien und Prozentangaben beschreiben den Boden bzw. die Entwässerung. Eine Treppe braucht zusätzlich wiederholte Stufenkanten und einen Laufbeleg.

### Markierungen

- **Freiklasse / Boden** (green): Die bezeichnete Außenfläche hat einen erkennbaren Bodenaufbau. Ziel `[640, 1690]`, geschlossener Rahmen `[572, 1598, 701, 1733]`.
- **Stütze aussparen** (red): Die grüne Fläche endet am festen Stützenkörper. Ziel `[706, 1824]`, geschlossener Rahmen `[691, 1808, 722, 1840]`.
- **Umwehrter Bereich** (purple): Die Absturzsicherung begrenzt die nicht grün gefüllte Fläche. Ziel `[822, 1802]`, geschlossener Rahmen `[750, 1600, 980, 1825]`.
- **Treppenlauf** (orange): Die Treppenfläche ist grün, ihre Originalstufen bleiben schwarz. Ziel `[1342, 1669]`, geschlossener Rahmen `[1115, 1613, 1545, 1745]`.

## S01 - Stiege 2: Stufen, Lauf und Podest

Lernbuch Seite 27; Detail-PDF Seite 21. Bild: `bilder/S01.png`. Originalausschnitt: `[1090, 1010, 1575, 1610]`.

### Warum Treppe?

Stufenlinien, fortlaufende Nummern, ein Laufpfeil, Podeste und die Beschriftung Stiege 2 belegen gemeinsam eine Treppe.

### Was 13 STG 15/30 bedeutet

Der Plan nennt 13 Steigungen mit 15 cm Steigung und 30 cm Auftritt. Daraus ergibt sich für diesen Lauf rechnerisch 1,95 m Höhenunterschied.

### Rauf oder runter?

Die aufsteigende Stufenzählung und der Laufpfeil helfen beim Lesen des Laufs. Welches benachbarte Geschoss am Ende erreicht wird, wird erst über Höhen und den Anschlussplan bestätigt.

### Markierungen

- **Stufenfolge** (blue): Die vielen regelmäßigen Querlinien bilden den Treppenlauf. Ziel `[1370, 1350]`, geschlossener Rahmen `[1315, 1250, 1420, 1448]`.
- **Laufhinweis** (orange): Pfeil, Stufennummern und 13 STG 15/30 gehören zusammen. Ziel `[1373, 1335]`, geschlossener Rahmen `[1354, 1313, 1393, 1354]`.
- **Podest** (green): Am Ende der Stufenfolge liegt die zusammenhängende Zwischenfläche. Ziel `[1430, 1510]`, geschlossener Rahmen `[1320, 1466, 1540, 1538]`.
- **Mittlere Grenze** (purple): Die beschriftete raumhohe Brüstung trennt die Läufe. Ziel `[1430, 1350]`, geschlossener Rahmen `[1421, 1238, 1437, 1458]`.

## S02 - Stiege 1: Bruchlinie und verdeckter Lauf

Lernbuch Seite 28; Detail-PDF Seite 22. Bild: `bilder/S02.png`. Originalausschnitt: `[2695, 1420, 3150, 2020]`.

### Warum die schräge Linie keine Wand ist

Sie liegt innerhalb der Treppendarstellung und unterbricht die Stufenfolge. Ein schraffierter geschlossener Wandkörper fehlt an dieser Stelle.

### Treppenumriss erhalten

Schwarze Stufen, Pfeile und gestrichelte Originalteile werden nicht von einer deckenden grünen Fläche verdeckt.

### Grenzen der Draufsicht

Eine Bruchlinie kennzeichnet die Darstellung, nicht automatisch eine bestimmte Bewegungsrichtung. Zielgeschoss und Anschlusshöhen benötigen zusätzliche Belege.

### Markierungen

- **Stufen bleiben schwarz** (blue): Die originalen Stufenkanten liegen sichtbar über der grünen Fläche. Ziel `[2898, 1800]`, geschlossener Rahmen `[2845, 1715, 2946, 1852]`.
- **Bruchdarstellung** (orange): Die schräge Unterbrechung markiert die Darstellung des Treppenlaufs. Ziel `[2770, 1755]`, geschlossener Rahmen `[2725, 1734, 2837, 1780]`.
- **Aufzug daneben** (purple): Der Schacht rechts ist eine eigene Anlage, keine Fortsetzung des Laufs. Ziel `[2990, 1730]`, geschlossener Rahmen `[2965, 1654, 3045, 1805]`.
- **Podestfläche** (green): Die größere Fläche am Laufende ist ein Podest. Ziel `[2848, 1940]`, geschlossener Rahmen `[2730, 1880, 2940, 1990]`.

## S03 - Stiege 4: gerader Außenlauf mit 26 Steigungen

Lernbuch Seite 29; Detail-PDF Seite 23. Bild: `bilder/S03.png`. Originalausschnitt: `[1080, 1575, 1575, 1795]`.

### Warum Außenstiege?

Der Raumstempel F2.03 benennt Stiege 4. Stufenfolge, Laufpfeil und Maßtext liefern die geometrischen Zusatzbelege.

### Höhenidee

26 mal 15 cm ergeben 3,90 m Höhenunterschied als Rechenbeispiel aus den Beschriftungen. Das legt noch nicht fest, welches Endpodest zum 2. OG gehört.

### Verbindung modellieren

Den Lauf als vertikale Verbindung mit zwei Enden speichern. Einen horizontalen Weg nicht einfach durch beide Geschosse auf derselben Höhe fortsetzen.

### Markierungen

- **26 STG** (orange): Die Originalbeschriftung nennt 26 STG 15/30. Ziel `[1124, 1675]`, geschlossener Rahmen `[1107, 1659, 1145, 1690]`.
- **Stufen / Nummern** (blue): Die regelmäßigen Querlinien und Nummern laufen über die Treppenfläche. Ziel `[1345, 1690]`, geschlossener Rahmen `[1284, 1620, 1440, 1740]`.
- **Bruch im Lauf** (purple): Die schräge Bruchdarstellung bleibt schwarz sichtbar. Ziel `[1130, 1660]`, geschlossener Rahmen `[1112, 1610, 1151, 1747]`.
- **Seitliche Sicherung** (purple): Die raumhohe Absturzsicherung begrenzt den Lauf. Ziel `[1465, 1731]`, geschlossener Rahmen `[1410, 1720, 1534, 1742]`.

## S04 - Stiege 3: derselbe Typ an anderer Stelle

Lernbuch Seite 30; Detail-PDF Seite 24. Bild: `bilder/S04.png`. Originalausschnitt: `[2675, 2515, 3200, 2750]`.

### Merkmale übertragen

Die gleiche Erkennungsregel gilt hier wie bei Stiege 4. Trotzdem erhalten Stiege 3 und Stiege 4 eigene Positionen und Verbindungen.

### 26 STG 15/30

Die Schrift unterstützt die Interpretation als Treppenlauf. Sie wird zusammen mit der Geometrie dokumentiert, nicht als bloßer Fließtext ignoriert.

### Keine Richtungsabkürzung

Rechts im Blatt bedeutet nicht automatisch hinauf. Den konkreten Geschossanschluss erst mit Höhen- und Nachbarplanbelegen festlegen.

### Markierungen

- **Treppenbeleg** (orange): F2.06 und Stiege 3 stehen innerhalb des Bereichs. Ziel `[2926, 2587]`, geschlossener Rahmen `[2900, 2568, 2970, 2610]`.
- **Stufenfolge** (blue): Die Originallinien wiederholen sich quer zum Lauf. Ziel `[2990, 2630]`, geschlossener Rahmen `[2960, 2555, 3115, 2698]`.
- **Absturzsicherung** (purple): Diese Grenze ist als raumhoch bezeichnet. Ziel `[3108, 2674]`, geschlossener Rahmen `[3075, 2661, 3180, 2686]`.
- **Vorbereich** (green): F2.05 bezeichnet die zugehörige Erschließung. Ziel `[2830, 2734]`, geschlossener Rahmen `[2750, 2713, 2925, 2745]`.

## S05 - Garderobenraster ist keine Treppe

Lernbuch Seite 31; Detail-PDF Seite 25. Bild: `bilder/S05.png`. Originalausschnitt: `[628, 917, 994, 1263]`.

### Warum dieser Vergleich wichtig ist

Wiederholte parallele Linien treten auch bei Regalen, Garderoben und anderen Einbauten auf. Eine Treppe darf nicht nur über dieses Muster erkannt werden.

### Zusätzliche Belege verlangen

Raumtext, Layer, Laufpfeil, Stufennummern und Podestgeometrie gemeinsam prüfen. Hier spricht der Originalplan für eine Garderobe.

### Grüne Fläche

Nur Boden zwischen den erkannten Einbauten wird gefüllt. Die Rasterkörper selbst bleiben ausgespart.

### Markierungen

- **Raumstempel** (purple): Der Plan benennt den Raum 2.26 als Garderobe. Ziel `[795, 955]`, geschlossener Rahmen `[778, 936, 874, 1005]`.
- **Einbauraster** (blue): Die kleinen Rechtecke gehören zu den Einbauten. Ziel `[807, 1019]`, geschlossener Rahmen `[752, 997, 932, 1052]`.
- **Keine Stufenbelege** (orange): Hier fehlen ein Treppenlauf, STG-Angabe und zusammengehörige Podeste. Ziel `[768, 1130]`, geschlossener Rahmen `[685, 1100, 875, 1160]`.
- **Türen zum Raum** (green): Die Seitenzugänge verbinden den Raum mit der Erschließung. Ziel `[981, 1208]`, geschlossener Rahmen `[935, 1150, 991, 1225]`.
