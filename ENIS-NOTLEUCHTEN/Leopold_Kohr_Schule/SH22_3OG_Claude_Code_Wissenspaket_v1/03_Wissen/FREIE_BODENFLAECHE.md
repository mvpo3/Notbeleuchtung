# Boden, Raum und Bewegung sauber auseinanderhalten

## Was grün werden soll

Die gesamte belegte freie Bodenfläche: alle Breiten eines Gangs, Aufweitungen, Nischen, zugängliche Endbereiche und freie Zwischenräume um einzelne Möbel. Eine Mittelachse oder eine dick gemalte Route genügt nicht. Die grünen Lernübersichten im PDF erklären diese Anforderung. Sie sind keine exportierte metrische Ground Truth.

## Rechenmodell als fachlicher Ausgangspunkt

`freie_bodenflaeche = bestaetigte_bodenflaeche minus bodenwirksame_feste_bauteile minus belegte_hindernisse`

Das ist ein Konzept, kein Aufruf einer bereits vorhandenen Repo-Funktion. Unbestätigte Bodenflächen dürfen nicht automatisch in den ersten Term eingehen. Ein nur angenommener Leerraum, ein Schacht oder ein unklarer Innenbereich wird separat behandelt. Ein Wartungssteg kann echten Boden haben, ist aber nicht deshalb allgemeiner Gehweg.

1. Bestimme Bodenexistenz und Höhenebene. Zugang allein beweist nicht die gesamte Bodenfläche; eine geschlossene Kontur ebenfalls nicht.
2. Bestimme feste Wand-/Brüstungs-/Trennplattenflächen und andere tatsächliche Bodenhindernisse. Bei Geländern wirkt eine Randbarriere, nicht ein erfundener massiver Raum dahinter.
3. Ziehe Möbel nur mit ihren belegten Stellflächen ab. Kein grobes Sammelrechteck um eine Möbelreihe, das freie Zwischenräume verschluckt. Unsichere Stellfläche kennzeichnen und belegen.
4. Trenne Raum-/Nutzungsflächen von freiem Boden. Ein Möbel ändert die nutzbare Fläche, aber nicht automatisch die bauliche Raumgrenze.
5. Verbinde benachbarte Flächen nur über verifizierte Öffnungen. Ein fast berührendes Polygon oder ein Rasterspalt ist kein Türbeleg.
6. Bestimme erst danach eine konkrete Route und ihre Bedingungen.

## Linien ohne massive Stellfläche

Tür-/Fensterbögen, Maßlinien, Raumstempel, Beschriftungszeiger, Gefällelinien und Darstellungsbrüche sind keine massiven Hindernisse. Ein geöffneter Türflügel bleibt ein tatsächliches bewegliches Bauteil; seine momentane Kollisionswirkung und sein Freihaltebereich sind getrennte Modelle. Die ganze Schwenkfläche pauschal vom Boden abzuziehen ist falsch.

## Bewegung mit endlicher Körperbreite

Ein geometrisch freier Spalt kann zu schmal für das gewählte Bewegungsprofil sein. Körper-/Hilfsmittelabmessungen und erforderliche Abstände gehören in eine separate, maßlich begründete Prüfung. Diese reduziert den Bewegungsraum innerhalb des freien Bodens; sie verkleinert nicht stillschweigend den dargestellten Raumgrundriss. Es gibt in diesem Paket keinen universellen neuen Mindestbreitenwert.

## Türen, Treppen, Lift und Wartung

| Element | Boden-/Verbindungswirkung |
| --- | --- |
| Normale Tür | Portal an der lichten Öffnung, abhängig von Zustand/Zugang |
| Fenster mit FPH 0,85 über FBOK | Kein normaler bodengleicher Durchtritt |
| Treppenlauf | Höhenverbindung, Podeste und reale Anschlusshöhen getrennt |
| Liftkabine | Bedingt betretbare Kabine, kein dauerhaft freier kompletter Schacht |
| Wartungssteg | Eigene Nutzungs-/Zugangsbedingung; kein allgemeiner Gang aus Weißfläche |
| Absturzsicherung | Querung am Rand gesperrt; Tiefe des Bereichs dahinter extra prüfen |

## Unzulässige Reparaturen

Keine künstlichen Wanddurchbrüche, keine Verbindung durch Fensterbrüstungen, keine erfundene Fläche über Lufträumen, kein Zusammenkleben von Treppenläufen ohne Höhenbezug. Bei unterbrochener Topologie den konkreten Fehler und seine Belege berichten. Ein zusammenhängender Graph ist nur dann richtig, wenn seine Verbindungen physisch begründet sind.

Im Paket liegen bewusst keine als millimetergenaue Sollpolygone bezeichneten Masken vor. Die exakten Produktionsflächen werden aus den Originalquellen neu berechnet und anschließend gegen die fachlichen Beispiele geprüft.
