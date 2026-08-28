# AC 26 Grundkurs — Teil 1
> Quelle: AC 26 Grundkurs (buecher) · Seiten 41-80.

Hinweis zur Einordnung: Dies ist **kein** elektrotechnisches Normwerk (kein OVE/ÖNorm-Inhalt), sondern ein **Archicad-26-Grundkurs von GRAPHISOFT Deutschland** (CAD/BIM-Modellierungs-Schulung, Kapitel 4 "3D-Gebäudemodell erstellen"). Teil 1 (S. 41-80) behandelt die schrittweise Modellierung eines Beispielgebäudes: Bodenaufbauten, Schnitte/Ansichten, Dach, Fenster/Türen/Fassade, Treppen/Geländer, Möblierung, Räume und Bemaßung. Die enthaltenen Zahlenwerte sind CAD-Bauteilparameter (Stärken, Höhen, Neigungen, Abstände), keine Elektroplanungs-Normwerte. Alle konkreten Werte sind unten vollständig festgehalten.

## Inhalt

### 4.2 (Fortsetzung) Bodenaufbauten hinzufügen
- Bodenaufbauten in allen Geschossen mit dem **Deckenwerkzeug** modellieren; Start im Erdgeschoss (EG).
- Grundeinstellungen Decke: **Deckenstärke = 0,10**, **Abstand zum Ursprungsgeschoss = 0,00**.
- Baustoff: **BODENAUFBAU**. Ebene: **20 Bodenaufbau...**. Mit OK bestätigen.
- Mit dem **Zauberstab (Leertaste)** in allen Räumen des EG einen Bodenaufbau erzeugen; gleiches Vorgehen in Obergeschoss (OG) und Dachgeschoss (DG), inkl. Bodenaufbau auf der **Terrasse im OG** (schnellste Methode: im Grundriss mit Zauberstab).

### 4.3 Schnitte und Ansichten
- **Schnitt-Werkzeug** liegt unter Kategorie "Sichten" im Werkzeugkasten; Aufruf der Einstellungen per Doppelklick.
- Menü Allgemein: Schnitt erhält **Referenz-ID** und **Namen**. Konvention: Schnitte mit Großbuchstaben benennen — erster Schnitt **A-A** (Referenz-ID = A), nächster **B-B** (Referenz-ID = B) usw., damit der Schnittmarker korrekt beschriftet wird.
- Schnittlinie zeichnen: Startpunkt links vom Grundriss klicken, Endpunkt rechts vom Gebäude. Für exakt gerade Linie **Umschalt-Taste** gedrückt halten (nach Startpunkt drücken, erst nach Endpunkt loslassen).
- **Augencursor** definiert die Blickrichtung; ein kleines Dreieck an der Schnittlinie zeigt die Blickrichtung an. Schnitt per Doppelklick im Navigator aufrufen. Übung: zweiten Schnitt B-B als Quer-/Längsschnitt erstellen.
- **Ansichts-Werkzeug**: analog zum Schnitt, aber außerhalb des Gebäudes platziert. Ansichtslinie waagrecht von links über dem Grundriss nach rechts ziehen, Blickrichtung mit Augencursor festlegen. Aufruf über Navigator. Übung: Nord-, Süd-, West-, Ostansicht erstellen.
- **Kontextmenü (Rechtsklick)** auf Schnitt-/Ansichtslinie im Grundriss oder Navigator: Einstellungsfenster öffnen, Ansicht/Schnitt öffnen, oder Linien ausblenden via **Ebenen > Ebene ausblenden**. Alles wieder einblenden: Menü **Dokumentation > Ebenen > Alle Ebenen sichtbar**.

### 4.4 Dach
- Werkzeugwahl nach Dachform:
  - **Geneigte Dächer** → **Dachflächen-Werkzeug**.
  - **Flachdächer** → **Decken-Werkzeug**.
  - **Geschwungene/Freiformdächer** → **Schalen-Werkzeug**.
- **Aufsetzlinie** (blau bei Auswahl): Konstruktionsachse, an der Neigung und Höhe der Dachfläche ausgerichtet werden.
- **Pultdach erstellen** (im DG):
  - **Abstand der Aufsetzlinie zum Ursprungsgeschoss (DG) = 2,40**.
  - Baustoff **DACHAUFBAU**, einfache Struktur, **Dicke = 0,345**.
  - Geometriemethode = **Einzeldach**, **Dachneigung = 3,00°**, **Vertikaler Abschluss** für die Dachkanten.
  - Ebene **30 Dachaufbau**; mit OK übernehmen.
  - Konstruktionsmethode = **Rechteckig**. Aufsetzlinie: Gebäudeecke links oben → rechts oben (oberste Außenkante). Anstiegsrichtung mit Augen-Cursor **unterhalb** der Aufsetzlinie wählen (Dach steigt nach unten an).
  - Dachfläche: linke obere Außenecke → rechte untere Außenecke.
  - 3D-Fenster: Shortcut **Cmd+3 (Mac) / Strg+3 (WIN)**. Wände stehen zunächst über das Dach hinaus.
- **Wände an Dach anpassen** (alle DG-Wände + Dach aktivieren):
  - **Suchen & Aktivieren** (Menü Bearbeiten > Suchen & aktivieren...): Element-Typ = **Wand**; Kriterium **Positionierung Ursprungsgeschoss** hinzufügen; von EG auf **DG** umstellen; mit Plus-Symbol alle DG-Wände auswählen.
  - **Wände trimmen**: Dach via Shift+Klick zur Auswahl hinzufügen → Befehl **Elemente mit Dach/Schale trimmen** → Option **Dächer/Schalen aus der aktuellen Auswahl benutzen** → **Trimmen**. Auswahl mit Esc / Linksklick aufheben.

### 4.5 Fenster, Türen und Fassade
- **Fenster-Einstellungen** (einflügelige Fenster):
  - Bibliotheken-Browser: Katalog **2.01 Rechteckfenster**, **1-Flügelfenster**.
  - **Fensterbreite = 1,00**, **Fensterhöhe = 2,135**.
  - Anker = **Brüstung/Schwelle zu Geschoss 0**, Wert **0,00**.
  - **Anschlag zu Wandfläche = 0,075**.
  - Öffnungstyp und Winkel: Hauptflügel = **Festverglast**.
  - Modelleigenschaften: Konstruktionstyp = **Holz**, alle Rahmenoberflächen = **Holz Lärche** (Konstruktionstyp wechselt dadurch auf "Frei definierbar 1").
- **Fenster im Grundriss platzieren** (EG):
  - Bei Gebäudeecken landet das Fenster auf einer der beiden Wände; mit **Tab-Taste** auf die andere Wand wechseln.
  - Ankerpunkt auf **Seite 2** setzen; Cursor auf Schnittpunkt horizontale Innenwand × rechte Außenwand; ggf. Tab für Außenwand.
  - **Sonnensymbol** = Außenseite des Fensters; mit Tab korrigierbar. Öffnungsrichtung (Türsymbol-Cursor) per Mausklick bestätigen.
- **Fenster-Favorit**: Reiter Favoriten → Ordner **RICHTIG-KONSTRUIEREN** → Favorit **01_Kombi-Fenster_Nord-EG**. Weitere Fenster in EG/OG/DG laut Schaubildern mit Favoriten ergänzen.
- **3D-Darstellung der Fenster anpassen**:
  - **Modelldarstellung** = Darstellungseinstellung in den Schnelloptionen (unterer Bildschirmrand, "zwei konzentrische Rechtecke"); regelt Detaillierungsgrad in Grundriss/Schnitt/3D.
  - Aufruf: **Dokumentation > Modelldarstellung > Modelldarstellung erstellen...**.
  - Modelldarstellung **04 Beispiel Genehmigungsplanung** auswählen, vor Änderung **duplizieren** (Neu...), neuer Name z. B. **04 Fenster 3D detailliert**.
  - Reiter **Detaillierung für Tür-, Fenster- und Dachfenstersymbole**: Bereich Tür und Fenster jeweils **3D-Darstellung = Komplett**.
- **Fassadenlattung** (vor Fenstern, als Sichtschutz/Gestaltung) mit dem **Fassaden-Werkzeug**:
  - EG: Favorit **01_Lattung-vertikal** (Ordner RICHTIG-KONSTRUIEREN) → Anwenden → OK. Geometriemethode **Einfach**; vom linken Fenster-Eckpunkt waagrecht nach rechts, **Abstand „1,2“** eintippen + Enter. Bei Überstand **Spiegeln** (Infoleiste) nutzen.
  - Vertikale Lattungen vor nördlichen EG-Fenstern; horizontale Lattung (Favorit **02_Lattung-horizontal**) vor Brüstung des südlichen Fensters.
  - **OG/DG**: Favorit **01_Lattung-vertikal**, Höhe des Fassadensystems im Bereich Geometrie und Positionierung auf **5,06** anpassen → OK. DG horizontale Lattungen via **02_Lattung-horizontal**.
- **Fassadenfarbe überschreiben**:
  - Oberflächenmaterial hängt am Baustoff: Baustoff **TRAGENDE BAUTEILE** → Oberfläche **Farbe weiß**; Baustoff **MW Kalksandstein** → Mauerwerkstextur.
  - Überschreiben ohne Konstruktionsänderung: Außenwände (Suchen & Aktivieren) → Wand-Einstellungen → **Oberflächenmaterial außen** = **Verputz, Lehmputz, braun** → OK.
  - Gleiches Überschreiben für Decken-Stirnseiten, Dach, Träger und Terrasse.
- **Türen** (analog zu Fenstern):
  - Innentüren: **Zargentür 1-fl** im Ordner **3.02 Innentüren (Deutschland)** bzw. **3.1 Innentüren (Österreich)**.
  - **Türbreite = 0,76**, **Türhöhe = 2,135**.
  - Grün markierte Innentüren mit diesen Einstellungen; rot markierte Außentüren über vorangelegte Favoriten; Positionen laut Bemaßungen in den Schaubildern (EG/OG/DG).
- **Bodenaufbauten an bodentiefe Fenster/Türen anpassen** (im Grundriss EG):
  - Bodenaufbau auswählen (ggf. Tab), auf Kante klicken → Pet-Palette → **Zum Polygon hinzufügen**.
  - Geometriemethode **Rechteckig**; Rechteck im Bereich der Fensterlaibung aufziehen, angrenzend an den Bodenaufbau.
  - Bei allen bodentiefen Fenstern und Türen (auch Innentüren) wiederholen.

### 4.6 Treppe und Geländer
- **Treppen-Werkzeug**: Entwurf typischer/spezieller Treppen, grafische Eingabe und Bearbeitung.
- **Interne Treppe (OG → DG)** im DG-Grundriss:
  - Favorit **01_interne-Treppe** → Anwenden.
  - **Treppenlaufbreite = 0,80**, **Anzahl Stufen = 14**.
  - Ursprungsgeschoss = **1. OG**, Oberkante verknüpft mit **2. DG**.
  - Eingabemethode (Infoleiste) = **Abwärts**. Startpunkt **0,90 m links** des Eckpunkts: Mauszeiger in rechte Ecke der Zwischenwand (nicht klicken) → Tastatur **X 0,9 – Enter**.
  - Konstruktionsmethode (Pet-Palette) = **Wendelung mit gleichen Auftritten**; Cursor entlang blauer Fanghilfe nach links bis Innenkante Außenwand → klicken → senkrecht nach unten → Doppelklick zum Fertigstellen.
  - Grundrissdarstellung ist geschossabhängig.
- **Außentreppe** (im OG, Favorit **02_Außentreppe**): Ursprungsgeschoss = **EG**, Oberkante = **OG**.
- **Treppendurchbruch**:
  - Schnitt A-A zeigt: Decke (Rohdecke + Bodenaufbau) muss durchbrochen werden.
  - Im DG-Grundriss bei aktivierter **Schnellauswahl (Magnet-Symbol)**: per Tab die **Rohdecke** auswählen (Vorschau zeigt **Struktur: TRAGENDE BAUTEILE**) → Kante klicken → Pet-Palette → **Vom Polygon abziehen** → Geometriemethode **Polygon** → alle Treppeneckpunkte anklicken.
  - Vorgang für **Bodenaufbau** wiederholen (Vorschau: **Struktur: BODENAUFBAU**).
- **Geländer-Werkzeug**: 3D-Gebäudeelement, assoziativ zu Treppen, Decken, Wänden, Dächern und Freiflächen (passt sich automatisch an).
  - Interne Treppe (im OG): Abschnitt "Geländer" markieren → Favorit **Glas, eingespannt mit Abstand** (Ordner Geländer) → Anwenden → OK.
  - Platzieren: **Segment Assoziativität = Statisch**; **Referenzlinie = versetzt**, **Abstand = 0,04**; unteren rechten Treppenpunkt → zweiten Punkt (Treppe muss blau erscheinen = assoziativ) → Doppelklick zum Fertigstellen. Verklickt: **Backspace** löst letzten Punkt.
  - DG: Geländer rund um Treppenausschnitt, gleiche Einstellungen, Bodenaufbau muss blau sein (ggf. Tab), Start oben rechts an der Austrittsstufe.
  - Detaildarstellung: Modelldarstellung **04 Fenster 3D detailliert** → **Geländer-Optionen** → **Geländer 3D und Schnitt/Ansicht = Komplett**; umbenennen in **04 Fenster und Geländer 3D detailliert** → OK.
  - Geländer an Terrasse und Außentreppe: Favorit **01_Gelaender-Aussen** (Ordner RICHTIG-KONSTRUIEREN), assoziativ zu Treppe bzw. Bodenaufbau.

### 4.7 Möblierung
- **Objekt-Werkzeug** für Sanitär- und Einrichtungsgegenstände (funktioniert wie Fenster-/Tür-Werkzeug).
- Bibliotheken-Browser: Kategorie/Ordner wählen oder Namen neben der Lupe eintippen; Suche auch online auf **www.bimcomponents.com** (GRAPHISOFT) bei Internetverbindung.
- **Schwerkraft-Funktion** (Standard-Symbolleiste): platziert Objekt automatisch auf Höhe der darunterliegenden Decke/Dach/Schale/Freifläche. Wirkt **nur auf neu erstellte** Elemente (nicht zum Bearbeiten vorhandener). Über Pfeil neben Schwerkraft-Symbol: Bauteil-Art festlegen, zu der die Schwerkraft wirkt.
- **Objekt platzieren/bearbeiten**: Draufsicht "hängt" am Cursor; **Fixpunkte** (X-Symbole) wählbar als Einfüge-/Ankerpunkt (gerahmter Fixpunkt). Pet-Palette (Klick auf Knotenpunkt): verschieben, drehen, multiplizieren, **Knotenpunkt verschieben** (Dimension ändern, z. B. Schrank).
- **Editierbare Hotspots** (pinke Punkte) im 3D-Fenster: z. B. äußerer Hotspot in Schranktürmitte ziehen → Schranktüren öffnen.
- Übung: Grundrisse aller Geschosse (EG/OG/DG) laut Einrichtungsvorschlag möblieren.

### 4.8 Räume
- **Raumflächen-Werkzeug** für normale Räume und offene Räume ohne begrenzende Wände. Einstellbar: Raumname, Raumnummer, Höhe, Unterkante u. a.
- **Raumstempel** maßstabsabhängig: festlegbar, welche Infos in welchem Maßstab erscheinen (z. B. **Inhalt 1:100**).
- Konstruktionsmethoden:
  - Manuell: **Polygon, Rechteck, gedrehtes Rechteck**.
  - Automatisch: **Innenkante, Referenzlinie**.
  - Automatische Methode **Innenkante**: in von Wänden umschlossenen Bereich klicken (Cursor = Hammer-Symbol), Raum findet Grenzen automatisch.
- Darstellung pro Maßstab anpassbar: Raum aktivieren → Einstellungen → Bereich **Erscheinungsbild 1:100** (z. B. Rahmen-Stil); Bezeichnung **"NGF"** im Bereich **Fläche, Volumen 1:100** entfernbar.
- **Raumstempel-Textfeld** verschieben: pinken Punkt in Textfeldmitte klicken + ziehen; Pet-Palette-Befehl **Unterelement bewegen** aktiv.
- **Räume ohne begrenzende Wände**:
  - **Linie als Raumgrenze**: Linien-Werkzeug → Funktion **Raumflächen-Begrenzung** aktivieren → Linie auf separate Ebene (z. B. **00 Hilfskonstruktion**) → Geometriemethode **Einzeln** → Linie zeichnen → dann Raumwerkzeug nutzen → Ebene danach ausblenden. (Beispiel: Wohn- und Eingangsbereich im EG trennen.)
  - **Räume manuell zeichnen** (OG): Raumwerkzeug → Konstruktionsmethode **Individuell (Polylinie)** → Raumecken anklicken → erster Punkt + Hammer-Symbol für Raumstempel. Hinweis: manuell erstellte Räume passen sich **nicht automatisch** an; manuelle Anpassung über Pet-Palette.
- **Räume nachträglich ändern**: Räume aus **Innenkante/Referenzlinie** passen sich automatisch an. Beispiel DG: Trennwand Wohnzimmer/Bad, **Wandstärke = 0,25** → Bad wird kleiner → Befehl **Räume aktualisieren** (Menü Planung) → Option **Raumstempel-Positionen bei Aktualisierung behalten** → **Alle Raumflächen aktualisieren** (Ergebnisprotokoll erscheint). Änderungen anschließend rückgängig machen.

### 4.9 Bemaßung
- Mehrere automatisch anpassende Bemaßungs-Werkzeuge; vorgestellt: **Einzelbemaßung** und **Automatische Bemaßung**.
- **Einzelbemaßung**: Bemaßungs-Grundeinstellung (Markertyp, Schriftart, -stil, Maßhilfslinie). Punkte anklicken (ggf. Tab); Markierungen: **runde Markierung = am Element gebundener Punkt**, **eckige Markierung = freier Punkt**. Doppelklick → Hammersymbol → Bemaßung setzen. Fenster/Türen erhalten Höhen- und Breitenmaß (falls in Bemaßungsdetails aktiviert). Gebundene Bemaßungspunkte passen sich bei Modelländerungen automatisch an.
- **Automatische Bemaßung**: im Grundriss für Wände, im Schnitt für Decken. Erst alle zu bemaßenden Wände auswählen → **Dokumentation > Beschriftung > Automatische Bemaßung > Außenbemaßung** (oder Symbolleiste). Menü legt Bemaßungsart und Abstand zwischen Maßlinien fest. Auf Außenwandkante klicken (Cursor = "dicker Mercedesstern") → Cursor = Hammersymbol (A) bzw. im Freiflächenbereich Stiftsymbol (B) → Bemaßung platzieren.
- Maßketten nachträglich änderbar (Punkte hinzufügen/entfernen), löschbar (z. B. doppelte Maßketten) oder verschiebbar. Übung: Bemaßung für alle Geschosse erstellen.

---
**Relevanz für ElektroPlaner:** gering — reines Architektur-CAD-Tutorial (Archicad 26). Nutzbar allenfalls als Hintergrund zu Geschoss-/Bauteilstrukturen (Ebenen wie "20 Bodenaufbau", "30 Dachaufbau", Baustoffe TRAGENDE BAUTEILE/BODENAUFBAU/DACHAUFBAU, Raumstempel-Logik), aber **keine** OVE-/ÖNorm-Elektroplanungsinhalte.
