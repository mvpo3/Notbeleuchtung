# Türen und offene Durchgänge

## Was ist eine Tür?

Eine Tür ist ein beweglicher Abschluss einer Öffnung. Im Grundriss werden häufig die Öffnung zwischen Wandenden, der angeschlagene Flügel und sein Schwenkbogen dargestellt. Zusammen belegen diese Zeichen eine geplante Türstelle. Andere Türarten können andere Symbole verwenden; das konkrete UG-Beispiel darf nicht zu einer universellen „jede Tür hat einen Bogen“-Regel werden.

## Warum reicht ein Bogen nicht?

Im UG gibt es Sportbögen in den Hallen und gebogene Treppenzeichen. Eine Tür braucht den passenden Bezug zur Wandöffnung und zum Flügel. Ein Bogen mitten auf dem Hallenboden ohne diese Nachbarschaft ist kein Türbeleg.

Bei T01 liegt DL 90 / DL 210 an einer eindeutigen Türdarstellung. Die Werte werden als Tür-Durchlichtangaben für Breite und Höhe gelesen; die Einheit und die tatsächliche nutzbare Breite müssen vor metrischer Anwendung bestätigt werden. Der gezeichnete Flügel erlaubt eine Aussage zur dargestellten Öffnungsseite, nicht zum derzeitigen Öffnungszustand. Verriegelung, Zutrittsrecht und Dauerfreigabe sind hier nicht dokumentiert.

## Zwei Flügel und ein Portal

Bei T02 gehören zwei Flügel zu einer gemeinsamen breiten Öffnung. Daraus entstehen nicht automatisch zwei unabhängige Zugänge. Ein X im Öffnungsfeld widerlegt die Tür nicht, wenn Flügel, Bogen, Wandenden und Maßbeschriftung passen; siehe T03.

## Offener Durchgang ohne Türblatt

Eine Lücke zwischen begrenzenden Bauteilen kann ein offener Durchgang sein. Dafür müssen die Wandenden tatsächlich eine Öffnung begrenzen und begehbare Flächen auf beiden Seiten anschließen. Fehlt nur ein Stück Linie durch Exportfehler, Überdeckung oder Ausschnittbegrenzung, ist noch kein Durchgang bewiesen. Auch Glaslinien, niedrige Brüstungen, Stufen oder ein Schacht können eine scheinbare Lücke anders erklären.

Das Fehlen eines eingezeichneten Türflügels allein beweist deshalb keine dauerhaft freie Passage. Eine bestätigte Öffnung ohne Tür wird als offene Verbindung gespeichert; eine Türöffnung bleibt eine Verbindung mit Türzustand. Ein offener Zugang zu einer Treppe wird zusätzlich als Übergang zu einem Höhenwechsel erfasst.

## Räume getrennt, Verbindung erhalten

Eine rechnerische Raumkontur darf an der Tür geschlossen werden. Diese Schließlinie ist virtuell. Sie darf weder als Mauer in der Kollisionsprüfung erscheinen noch die Portalkante entfernen. Umgekehrt verschmilzt eine Tür nicht automatisch die beiden angrenzenden Räume.

## UG-Lernfälle

- [T01 – Einflügelige Tür](../lektionen/T01.md)
- [T02 – Zweiflügelige Tür](../lektionen/T02.md)
- [T03 – Tür mit Kreuzfeld](../lektionen/T03.md)
- [W02 – Verbindung durch eine Tür](../lektionen/W02.md)
