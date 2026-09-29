# Visuelle Ausgabe nach den Vorgaben des Nutzers

## Direkt das erklärte Bauteil markieren

Keine zusätzlichen Suchquadrate oder Objektkästen um Türen, Fenster, Möbel oder Treppen. Eine Linie erklärt man durch Nachzeichnen dieser Linie; einen Bogen durch Nachzeichnen des Bogens. Der Pfeil endet direkt auf dem erklärten Merkmal. Originalrechtecke, z. B. ein gezeichneter Tisch oder Rahmen, bleiben natürlich Bestandteil des Plans.

- Wände: feste Körper rot, ihre ganze belegte Dicke bei Boden-/Sperrflächen berücksichtigen.
- Absturzsicherung: rot gestrichelte Randbarriere; nicht als massive Mauer umbenennen.
- Freier Boden: vollständig grün, mit erhaltenen inneren Hindernissen und Zwischenräumen. Dunkleres Grün kann Erschließung zeigen.
- Einzelteile: Blau/Violett/Türkis gemäß lokaler Beschriftung. Bei D01/F01 ist der Flügel blau, der Bogen violett. Farben anderer Detailseiten werden durch den jeweiligen Pfeiltext erklärt und sind keine universellen CAD-Klassen.
- Textbelege/Drehpunkte: gezielte Unterstreichung beziehungsweise Punktmarkierung; ein künstlicher Zustandsstrich bleibt als Lehrhilfe ausdrücklich gekennzeichnet.

## Jede Erklärung braucht eine Beweiskette

1. **Beobachtung:** Welche konkrete Linie, Kurve, Beschriftung oder Anschlussstelle ist sichtbar?
2. **Bedeutung:** Was stellt dieses einzelne Merkmal dar?
3. **Kombination:** Welche weiteren Merkmale begründen die Bauteilklasse?
4. **Gegenprobe:** Welche ähnlich aussehende Deutung ist geprüft und warum trifft sie hier nicht zu?
5. **Modellwirkung:** Was wird Wand, Öffnung, Boden, Hindernis, Zone oder Verbindung?
6. **Offener Punkt:** Was lässt sich daraus noch nicht ableiten?

Beispiel: Ein Bogen beschreibt die Spur einer Flügelspitze. Das gemeinsame Zentrum und der passende Abstand begründen die Bewegung. Erst Wandöffnung, Bodenanschluss und zugeordnete DL-Angaben begründen hier die Tür. Eine ähnliche Mechanik in einer Fassade mit Brüstung bleibt ein Fenster.

## Ausgabe für die Abnahme

Erzeuge eine Gesamtansicht mit vollständigen Boden- und Wandflächen sowie Details der tatsächlich ausgewerteten Problemstellen. Die Farben sollen den Originalplan lesbar lassen. Nicht nur das richtige Lehrbild zeigen: Das Overlay muss die vom aktuellen Code berechneten Objekte enthalten. Beschrifte Ansichten mit Quellenhash, Lauf-ID und Fall-ID, damit Originalbeleg und Engine-Ergebnis vergleichbar bleiben.

Das optionale Werkzeug `zeige_beleg.py` erzeugt eine Vorschau der bereits im Lernbuch erklärten **Quellenbelege**. Es ist kein Engine-Overlay und kein Leistungsnachweis. Sein Ausgabeformat ist SVG mit rasterisiertem Originalausschnitt und darüberliegenden exakten Markierungsgeometrien; die Original-PDF bleibt unverändert.
