# Umsetzung in die vorhandene Raumerkennung

## Ausgangspunkt

Der freigegebene Lehrtext beschreibt das erwünschte fachliche Verhalten. Die beigefügten JSON-Dateien machen das Wissen gezielt abrufbar und prüfbar. Es liegt kein aktueller Code-Checkout mit ausführbarer Projektengine vor. Deshalb werden weder konkrete bestehende Funktionsnamen noch aktuelle Testzahlen erfunden. Die mitgelieferten Projektdateien zu `elektro-planer` enthalten ältere Stände und Mollgasse-Bezug; daraus folgt kein bestätigter heutiger Integrationspunkt für SH22.

## 1. Tatsächliche Pipeline aufnehmen

Finde Import/Einheiten, Textauswertung, Wandbildung, Öffnungen, Raumkonturen, Hindernisse, Topologie und Ausgabe. Dokumentiere für jeden Abschnitt Eingaben, Ausgaben und die bestehende Quelle der Entscheidung. Prüfe, ob bereits ein Evidenzmodell existiert. Erweitere dieses, statt ein zweites widersprüchliches Modell daneben zu bauen.

Bestimme vor Änderung die echten Fehlfälle am Originalinput. Bewahre Originaldateien, Konfiguration, Laufkommando und Softwarestand. Ein Paketprüflauf ist kein Engine-Baseline-Lauf. Für Repository-Pipeline und Gates gelten die aktuellen Regeln vor Ort.

## 2. Evidenz und Text vor endgültiger Klassifikation

Behalte LINE/ARC/LWPOLYLINE/HATCH, Blockreferenz, WCS-Koordinate, Einheit, Layer und ursprünglichen Text. Aufgelöste Blöcke benötigen Rückbezug zum ursprünglichen Insert und zur angewandten Transformation. Vermeide, dass Textkurven aus einer PDF zu Wänden werden. Bei DXF-Texten Fragmentierung, Ausrichtung, Hochstellung und außerhalb des Raums liegende Beschriftungen beachten.

Ordne Text über Zuordnungslinie, identifizierbaren Raumstempel, Bauteilanschluss und räumliche Lage zu. Nähe dient nur zur Kandidatensuche. Widersprüche werden gespeichert und nicht durch einen beliebigen nächstgelegenen Text überschrieben.

Ergebnis: nachvollziehbare Evidenzdatensätze. Prüfbeispiele R03, S02, B04, B05, F01.

## 3. Feste Bauteile, Öffnungen und bewegliche Teile

Wandkandidaten brauchen Kanten-/Körperzusammenhang, Anschluss und Schnittdarstellung. Schraffur hilft, begründet aber allein keine Materialklasse. Prüfe Trennplatten gesondert, da ihre geringe Dicke nicht Durchlässigkeit bedeutet. Die Produktions-Wandrepräsentation des Repos kann Achsen und Dicken verwenden; entscheidend ist, dass die gesperrte Fläche der ganzen Wandbreite entspricht.

Öffnungen sind lokale Unterbrechungen mit Rand-/Laibungsbezug. Ein schwingender Flügel besteht aus einem Drehpunkt, einer Blattgeometrie und einem passenden Bogen. Geometrische Toleranzen aus dokumentierter Zeichnungsauflösung und Skalierung ableiten, nicht SH22-Pixelwerte hardcoden. Typentscheidung erst mit Boden- und Höhenkontext treffen.

Ergebnis: feste Sperrflächen, gesonderte Fenster und bedingte Türportale. Prüfbeispiele W01–W03, D01–D03, F01–F03. Ein bestandener Türfall bei gleichzeitig als Tür fehlgedeutetem Fenster ist kein brauchbarer Fortschritt.

## 4. Boden, Hindernisse und Topologie

Zuerst bestätigten Boden bestimmen; danach echte Hindernisse abziehen. Wenn der vorhandene Raumdetektor Türöffnungen temporär schließt, müssen diese Hilfskanten als virtuelle Segmentierung gekennzeichnet sein und später kontrolliert in Portale übergehen. Keine fehlende physische Wand aus einem Hilfsstrich erfinden.

Eine Raumpolygonbildung allein genügt nicht: Innenringe, Schacht-/Sonderflächen, Möbel und Fassadenunterbrechungen bleiben erhalten. Raumfläche ist nicht dasselbe wie freie Bodenfläche. Nutzungszonen ohne feste Umfassung erzeugen keine neue Wand. Benachbarte Polygonkanten erzeugen ohne belegte Öffnung keine Graphkante.

Ergebnis: vollständige freie Flächen und belegte Verbindungen. Prüfbeispiele M01–M04, R01–R04, G01 sowie B01/B02 und L01/L02 als Sperr- und Sonderfälle.

## 5. Vertikale Verbindungen und Sonderzeichen

Treppen aus Stufenfolge, Bezeichnung, Pfeil, Nummern, Podesten und Höhen interpretieren. Blattorientierung und vertikalen Sinn nicht verwechseln. Ein Darstellungsbruch ist weder eine Mauer noch das physische Ende einer Treppe. Zielgeschoss nur mit passenden Anschlussdaten.

Lift: Schacht, Kabine und Tür unterscheiden; Kabine ist ein bedingt erreichbarer Boden, der Schacht kein dauerhaft begehbarer Raum. Wartungssteg/Schachtleiter sind technische Nutzung mit eigenem Zugang, keine normale Erschließung. „raumhoch“ an der Absturzsicherung belegt keine Atriumtiefe. Gefällelinien und Prozentangaben können zur wasserführenden Schicht gehören; den Hinweis zum Plattenbelag separat auswerten.

Ergebnis: korrekt typisierte Sonderobjekte mit offenen Eigenschaften. Prüfbeispiele T01–T05, L01/L02, B01–B05.

## 6. Nachweis und Übertragbarkeit

Für jeden Schritt die betroffenen vorhandenen Tests und die fachlich relevanten Gegenfälle prüfen. Die 32 Paketfälle decken konkrete Beweisketten ab, nicht jedes Objekt des Gebäudes. Keine Gesamt-Raumanzahl daraus ableiten. Die vollständige Ausgabe zusätzlich gegen den ganzen Originalplan prüfen.

Unbekannte Werte nicht zur Verbesserung einer Erfolgsquote wegfiltern. Auswerten: richtig/falsch/ungeprüft pro Fall und Eigenschaft. Ein zweiter unabhängiger Plan prüft Übertragbarkeit; dessen Sollwissen muss aus seinem eigenen Originalplan stammen. Alte Geschosse werden nicht ungeprüft umbenannt.

## Definition eines vollständigen Ergebnisses

- Die Engine trifft und begründet Entscheidungen anhand eingelesener Quellelemente.
- Der neue Code ist über die reale Pipeline erreichbar; reine Hilfsdokumentation reicht nicht.
- Die Raum-/Boden-/Portal-Ausgabe wird über dem Original sichtbar gemacht.
- Bericht, Code-Revision, Quellenhash, Konfiguration und tatsächliche Laufbefehle sind dokumentiert.
- Fehlende Nachweise werden offengelegt; keine automatische Behauptung „100 % Raumerkennung“ aus 32 Beispielprüfungen.
