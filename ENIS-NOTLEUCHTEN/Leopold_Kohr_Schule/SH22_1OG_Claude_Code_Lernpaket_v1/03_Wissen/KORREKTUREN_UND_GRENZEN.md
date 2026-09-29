# Korrekturen und verbleibender Umfang

## In diesem Paket berücksichtigte Korrekturen

| Fall | Stelle | Korrigiertes Verständnis |
|---|---|---|
| K01 / M05 | Lernbuch 20–21, Terrasse F1.04 | Die beanstandete projizierte Kontur ist hier keine Mauer; Grün setzt sich fort. |
| K02 / M06 | Lernbuch 22–23, Außenränder | Randsicherungen werden gesondert rot gestrichelt markiert und als solche erklärt. |
| K03 / W02 | Lernbuch 38–39, zentraler Innenrand | „Absturzsicherung raumhoch“ wird gelesen, vergrößert gezeigt und der Begrenzung zugeordnet. Der Durchtritt bleibt gesperrt. |
| K04 / W06 | Lernbuch 7, Z03 | Pauschaler weißer Balken entfernt; rechter Randspalt und Anschluss an die Außentreppe grün geschlossen. |

Weitere erhaltene Unterscheidungen: Türblätter und Bögen sind keine Wandkörper; Möbel und Sanitärgegenstände bilden nicht automatisch neue Räume; Fensterbögen erzeugen keine gewöhnlichen Durchgänge; weißer Hintergrund allein ist keine Aussage über Begehbarkeit.

## Was vollständig vorliegt

- Die drei aktuellen Lern-PDFs und der unveränderte Originalplan als vier PDFs.
- Die vollständige Original-DXF dieses Geschosses.
- Die 23 Detailfälle des Lernbuchs plus die zusätzliche Korrektur W06 auf Seite 7.
- Regeln, Korrekturen, Quellenbezug, Koordinatentransformation, Umsetzungsauftrag und Werkzeuge für einen reproduzierbaren Versuch.

## Was die Engine noch selbst ermitteln muss

- Alle Räume mit vollständigen Raumkonturen, IDs, Nutzung und Nachbarschaften.
- Ein vollständiges Inventar aller Türen, Fenster und sonstigen Öffnungen.
- Eine vollständige, aus den Quellen abgeleitete Unterscheidung von massiven Wänden, dünnen Trennwänden, Randsicherungen und nicht wirksamen Projektionen.
- Ein vollständiges Wegenetz mit belegten Verbindungen auf beiden Seiten jeder Öffnung.
- Die genauen Geschossanschlüsse der Treppen und Lifte, soweit diese weitere Geschosspläne benötigen.

Die Referenzflächen sind Lern-Overlays. Einzelne ursprüngliche Flächenmasken sind manuell angenähert und müssen für eine produktive Segmentierung erneut aus der Originalgeometrie bestimmt werden. Insbesondere darf die Korrektur in Z03 nicht als universelle Aussage über alle Pflanzentröge auf dem Plan missverstanden werden.

Material, numerische Höhe der raumhohen Sicherung, betriebliche Zugänglichkeit sowie lichte Nutzmaße werden nicht aus fehlenden Angaben erfunden. Das Wort „raumhoch“ bleibt eine qualitative Angabe.

## Was bereits getestet wurde und was noch nicht

Die Paketprüfung betrifft Dateivollständigkeit, Prüfsummen, JSON-Struktur, Querverweise, ausgewählte DXF-Belege und die mitgelieferten Werkzeuge. Sie ist vom Ergebnis einer Raumerkennungsengine getrennt.

In diesem Paket wurde keine Software-Engine des Nutzers ausgeführt oder verändert. Es liegt daher noch kein belegter Vorher/Nachher-Erfolg der Engine vor. Der Auftrag an Claude Code besteht gerade darin, diesen Versuch mit dem vorhandenen Repository durchzuführen und sein Ergebnis offen zu berichten.

Die 37 Prüfaussagen sind gezielte Regressionen, keine vollständige Abnahme sämtlicher Räume. Ein Algorithmus, der nur diese Stellen oder die Referenzpolygone kopiert, hat noch keine allgemeine Erkennung gelernt.
