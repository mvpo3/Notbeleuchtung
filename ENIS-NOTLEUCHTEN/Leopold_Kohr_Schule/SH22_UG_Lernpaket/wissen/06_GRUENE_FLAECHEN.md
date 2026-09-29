# Den grünen Gesamtplan richtig lesen

Datei: `../plaene/SH22_UG_Begehbare_Flaechen_Gruen.pdf`.

Der Originalplan bleibt als Vektorgrafik erhalten. Die grüne Farbe liegt transparent darüber. Es wird eine Fläche gefüllt, nicht nur eine Mittellinie eingezeichnet.

## Farben und Grenzen

| Darstellung | Aussage |
|---|---|
| Dunkler grün | Gänge, Zugangsflächen, Treppen und Podeste |
| Heller grün | Angrenzende Raum-Bodenflächen; daraus folgt kein zweiter Ausgang |
| Rot | Wand- und feste Bauteilgrenzen; diese dürfen nicht als Abkürzung gequert werden |
| Schwarze Stufen und Lauflinien auf Grün | Treppenverbindung mit Höhenwechsel, kein ebener Gang |
| Weiß ausgespart | Wandkörper, Lift-/Schachtbereiche, ausgewählte Einbauten oder nicht bestätigte Bodenfläche |
| E1–E6 | Sechs konkret erklärte Endbereiche, keine allgemeingültigen Verbotsschilder |

Die stärkere grüne Tönung ist eine Lesehilfe für die Erschließung. Ihre Tönungsgrenze ist keine neue Wand und kein exakter Raumabschluss. Für die echte Grenze gelten Originalbauteile und Portale.

## Durchgang und Ende

Eine Tür kann zwei Flächen verbinden. Das setzt für die Nutzung voraus, dass die Tür tatsächlich nutzbar ist. Ihr Zustand ist aus der Zeichnung nicht bekannt. Das Grün darf deshalb nicht in „jede Tür steht offen“ übersetzt werden.

Im Archiv endet die mögliche Bewegung an der unteren Mauer. Man kann in den Bereich hineingehen und über denselben Zugang wieder hinaus. Das ist ein Endbereich, ohne dass der Boden dadurch unbetretbar wäre. Das Buch erklärt weitere markierte Endbereiche E2–E6. Die Endmarken sind konkrete Beispiele; sie behaupten keine vollständige Prüfung sämtlicher Betriebs- oder Fluchtwege.

## Treppen

Die Stufenfläche ist grün, die originalen Treppenkanten und Lauflinien wurden schwarz hervorgehoben. Gestrichelte Quelllinien bleiben als solche lesbar. Der mittlere Trennbereich und die Liftbereiche werden nicht zum Weg. Die Seitenansicht S07 erklärt, warum die Querlinien im Grundriss zu einem Höhenwechsel gehören.

## Genauigkeit

Die Flächen basieren auf ausgewählten Bodenbereichen, den ursprünglichen Wanddarstellungen und ausgesparten Einbauten. Der kleine Abstand zu den Wänden dient der Lesbarkeit. Er ist kein vermessener Körperabstand und keine pauschal festgelegte Mindestbreite.

Nicht jeder bewegliche Gegenstand oder jede kleine Einrichtung wurde als Hindernis inventarisiert. Eine freie Zeichnungsfläche ist deshalb nicht automatisch ein vor Ort freier, freigegebener oder ausreichend breiter Weg. Der vom Nutzer bestätigte Bereich K1 ist grün ergänzt. Die Hervorhebung zeigt eine Beispielstelle und keine vermessene vollständige Flächengrenze. Außerhalb der Markierung bedeutet Weiß nicht automatisch unbetretbar.

## Für Claude Code

`../daten/gruene_flaechen.json` enthält die ungefähren Flächen und ihre Bedeutung. Die Koordinaten liegen in PDF-Punkten mit Ursprung links oben; es sind keine geografischen Koordinaten und keine fertige Kollisionsmaske.

Die acht vergrößerten Bereiche stehen in `../bilder/gruen/`. Die originale CAD-Geometrie bleibt die Quelle für spätere exakte Flächen- und Verbindungsberechnungen.

## Korrektur K1

Der auf Seite 39 ursprünglich orange markierte Bereich ist begehbar. Dies wurde vom Nutzer am 21.09.2026 ausdrücklich bestätigt und ersetzt die vorherige offene Einordnung dieser Stelle. Die Bestätigung ist in `../daten/nutzerkorrekturen.json` dokumentiert.
