# ARCHICAD-BIM-Modellierungsrichtlinien — Teil 0
> Quelle: ARCHICAD-BIM-Modellierungsrichtlinien (buecher) · Seiten 1-32.

GRAPHISOFT-Leitfaden (Archicad 26, Stand 07/2022) für BIM-konformes Modellieren von Bauteilen, damit Modell, Plandarstellung, Massenermittlung und Datenaustausch mit AVA-/Fachplaner-/Holzbau-Software (IFC) sauber funktionieren. Teil 0 deckt das komplette Dokument ab: Projekteinrichtung, Geschoss-/Raumstempel-Logik, sämtliche Bauteil-Konstruktionsdetails (Gründung bis Dach), Durchbrüche und Flächen-/Volumenberechnung nach DIN 277. Hinweis: Es ist ein reiner CAD-Modellierungs-Leitfaden — er enthält keine ÖNORM/OVE-Elektroinhalte, aber relevante Klassifizierungs-, Höhenbezugs- und Layer-/Bauteil-Konventionen, die Parser-/Geometrie-Annahmen beim DXF/IFC-Handling stützen.

## Inhalt

### Grundprinzipien & Zielsetzung
- BIM in Archicad = aus dem Modell sowohl Pläne mit allen Informationen ableiten als auch Massen für Ausschreibungen generieren und an fachplanende Disziplinen weitergeben.
- Modellqualität muss dem Maßstab **1:50** der späteren Ausführung entsprechen.
- Lizenz: Creative Commons BY-NC-SA 4.0 International; Urheberrecht GRAPHISOFT Deutschland GmbH 2022. Adresse: Landaubogen 10, 81373 München.
- Grundsatz: Pro Element entweder das Gesamtelement ODER die Unterelemente klassifizieren — niemals beides gleichzeitig (sonst fehlerhafte Massenermittlung).

### Projektlage und Vermessungspunkt
- Modell auf oder nahe dem Projektursprung (0,0,0) modellieren.
- Position über Vermessungspunkt festlegen; Koordinaten + Nordrichtung unter **Optionen > Projektpräferenzen > Lage-Einstellungen**.
- Nordwinkel: Wert **0,0000°** liegt auf der X-Achse, Winkel gegen den Uhrzeigersinn; Norden = **90,0000°**.
- Nach Ersteinrichtung Koordinationsprüfung zwischen Archicad und anderen Softwarelösungen durchführen.

### Geschoss-Einstellung
- Zu Beginn festlegen, wo 0,00 liegt: auf **OKFF / FBOK** (Oberkante Fertigfußboden) oder **OKRD / DOK** (Oberkante Rohdecke).
- Archicad-Beispielvorlagen als Basis nutzen:
  - Österr. Vorlage „01 ARCHICAD Vorlage" → FBOK = ±0,00.
  - Deutsche Vorlage „01 … - Geschoss OKFF" → OKFF = ±0,00.
  - Deutsche Vorlage „02 … - Geschoss OKRD" → OKRD = ±0,00.
- Rohdecken-Position ist unabhängig von Geschoss-Einstellungen. Zwei Sichtweisen:
  - **Rohdecke unter Geschoss** → klassische Architektursicht (Rohdecke unterhalb des Raums).
  - **Rohdecke über Geschoss** → tragwerksnahe Sicht (Rohdecke oberhalb des Raums).

### Raumstempel (2 Varianten)
- Werkzeug: Raumflächen-Werkzeug; Klassifizierung: Raum; Konstruktionsmethode **Innenkante** empfohlen. In beiden Varianten Stärke des Bodenaufbaus angeben (bei Änderung auch im Raum nachziehen).
- **Variante 01:** Raum von **OK Rohdecke bis UK Rohdecke** — abgehängte Decke + Technikbereich darüber gehören vollständig zum Raum.
- **Variante 02:** Raum von **OK Rohdecke bis UK Abhangdecke**; Restbereich bis UK Rohdecke mit Luftschicht im mehrschichtigen Bauteil oder gesondertem Morph füllen.

### Gründung, Fundament, Außenwand (Streifenfundament)
- Für Gründung/Fundamente ein **eigenes Geschoss** erstellen.
- **01 Außenwand:** Wand-Werkzeug, Mehrschichtiges Bauteil, Klassifizierung Wand, tragend, außen; von **OK Sohlplatte bis OK Rohdecke**.
- **02 Sohlplatte:** Decken-Werkzeug, Einschichtiges Bauteil, Klassifizierung Rohbaudecke oder Fundament-Bodenplatte/Flachgründung, tragend, außen; **VK Sohlplatte = VK Rohbauwand** (bis Vorderkante Rohbauwand modellieren für korrekte Grundrissdarstellung).
- **03 Streifenfundament:** Wand-/Träger-Werkzeug, Mehrschichtiges Bauteil / Profil-Träger, Klassifizierung Fundament-Streifenfundament, tragend, außen; **OK Fundament = OK Sohlplatte**; bis OK Sohlplatte modellieren; Profil-Wand/Träger bei komplexen Geometrien (Profil-Manager).
- **04 Dämmkeil:** Träger-Werkzeug, Profil-Träger, Klassifizierung Bekleidung/Belag-Dämmung, nicht tragend, außen.
- Empfehlung: Streifenfundament und Dämmkeil getrennt modellieren (korrekte Klassifizierung + Einzelauswertung).

### Flachgründung, Außenwand, Sohlplatte
- **01 Außenwand:** Wand-Werkzeug, Mehrschichtig oder Profil-Wand, Klassifizierung Wand, tragend, außen; **Referenzlinie auf Kern außen**; **UK Wand = OK Rohdecke**; Verschneidung über Baustoffprioritäten. (UK auf OK Rohdecke → Brüstungshöhen im Fensterstempel bzgl. Roh-/Fertigfußboden anzeigbar.)
- **02 Dämmung vor Sohlplatte:** Träger-Werkzeug (vermeidet Verschneidungsprobleme mit Innenwänden), Profil-Träger, Bekleidung/Belag-Dämmung, nicht tragend, außen; von **UK Sohlplatte bis OK Sohlplatte**.
- **03 Sohlplatte:** Decken-Werkzeug, Einschichtig, Rohbaudecke oder Fundament-Bodenplatte/Flachgründung, tragend, außen.
- **04 Dämmung unter Sohlplatte:** Decken-Werkzeug, Einschichtig, Bekleidung/Belag-Dämmung, nicht tragend, außen.
- Soll Dämmung unter Sohlplatte als tragend gelten: 03 + 04 als ein mehrschichtiges Bauteil modellieren (besseres Filtern nach tragenden Elementen); dann 02 Dämmung vor Sohlplatte von UK 04 bis OK 03 modellieren.

### Punktfundament
- **01 Punktfundament:** Stützen-/Decken-/Morph-Werkzeug, Klassifizierung Fundament-Punktfundament, tragend, außen.
- **02 Köcherfundament:** Stützen-/Morph-Werkzeug, Fundament-Punktfundament, tragend, außen.
- Stützen-Werkzeug bevorzugen (unterschiedliche Geometrien konstruierbar).

### Stütze, Träger, Fertigteil
- Immer entweder Gesamtelement ODER Unterelemente klassifizieren (nicht beides).
- **01 Stütze:** Stützen-Werkzeug, Stütze und Profil-Stütze, Klassifizierung Stütze/Pfeiler-Stütze, tragend, innen oder außen; Segmente mit verschiedenen Geometrien; von **OK Rohdecke bis UK Rohdecke**.
- **02 Träger / Unterzug:** Träger-Werkzeug, Träger oder Profil-Träger, Klassifizierung Träger/Balken/Unterzug-Unterzug, tragend, innen oder außen; Segmente mit verschiedenen Geometrien (Bauteilanschlüsse, Auflager, Verjüngungen innerhalb eines Elements via Trennen).

### Außenwand, Rohdecke, Fußbodenaufbau
- **01 Außenwand:** Wand-Werkzeug, Mehrschichtig, Wand, tragend, außen; **Referenzlinie auf Kern außen**; **UK Wand = OK Rohdecke**, **OK Wand = OK Rohdecke im nächsten Geschoss**; Verschneidung über Baustoffprioritäten. (Referenzlinie Kern außen → reagiert unkompliziert auf Wandstärken-/Dämmdickenänderung ohne Außenkante Rohbau zu verschieben.)
- **02 Rohdecke:** Decken-Werkzeug, Einschichtig, Rohbaudecke, tragend, innen.
- **03 Fußbodenaufbau:** Decken-Werkzeug, Mehrschichtig (ohne Kern), Bekleidung/Belag-Fußbodenaufbau, nicht tragend, innen; raum-/bereichsweise erstellen (Bodenbeläge variieren).

### Fenster, Bodentiefes Fenster
- **01 Fenster / Bodentiefes Fenster:** Fenster-Werkzeug, Klassifizierung Fenster, nicht tragend, außen; in Fenster-Einstellungen unter **Fensterrahmen** unterschiedliche Breiten aktivieren und bei **Breite unten** die Höhe des Fußbodenaufbaus addieren (Aufdopplung). Bei Außenwand-Fenstern auf Wandöffnung achten — unter **Anschlag** Dämmungsüberstände, unter **Schichteinzug** Verhalten zwischen Wand und Fenster festlegen.
- **02 Fußbodenaufbau:** in die Fensteröffnung modellieren, Stärke der Rahmentiefe aussparen.
- **03 Sturz:** Träger-Werkzeug, Träger oder Profil-Träger, Klassifizierung Träger/Balken/Unterzug-Sturz, tragend, außen; automatisch über Baustoffprioritäten mit Wand verschnitten.
- **04 Absturzsicherung:** Geländer-Werkzeug oder Wand-Werkzeug, Klassifizierung Geländer, nicht tragend, außen.

### Balkon mit tragendem Dämmelement
- **01 Balkon:** Träger-Werkzeug, Klassifizierung Rohbaudecke, tragend, außen; unterschiedliche Segmente/Profile (Profil-Manager) für verschiedene Querschnitte (z.B. Fertigteil).
- **02 Tragendes Dämmelement** (zwischen Balkon und tragender Decke): Träger-Werkzeug, Bekleidung/Belag-Dämmung, **tragend**, außen; gesonderter Baustoff mit **höherer Baustoffpriorität** anlegen → verschneidet sich automatisch korrekt mit Dämmung der Außenwand.
- **03 Absturzsicherung:** Geländer-/Wand-Werkzeug, Geländer, nicht tragend, außen.
- Außenwände von OK Rohdecke bis OK Rohdecke im darüber liegenden Geschoss.

### Abgehängte Decke und Sichtinstallation
- **01 Abgehängte Decke:** Decken-Werkzeug, Mehrschichtiges Bauteil (eigentliche Decke + Luftschicht für Unterkonstruktion), Bekleidung/Belag-Abgehängte Decke, nicht tragend, innen; GK-Koffer mit Profil-Träger oder Wand-/Decken-Werkzeug; raum-/bereichsweise. Für Unterkonstruktion neuen Baustoff aus Luftschicht anlegen und **„bei Kollisionsprüfungen berücksichtigen" einschalten**.
- **02 Bereich für Haustechnik:** Morph-Werkzeug, Morph-Körper, Klassifizierung **Raumvorschlag**, nicht tragend, innen; gesondert erstellen (für Fachplaner direkt ersichtlich). Bei Sichtinstallation wird ausschließlich der Haustechnik-Bereich modelliert.
- Da Haustechnik-Bereich später meist wieder aus Modell entfernt wird, Raum hier von **OK Rohdecke bis UK Rohdecke** modellieren.

### Abgehängte Decke, Variante
- **01 Abgehängte Decke:** Decken-Werkzeug, Mehrschichtig mit eigentlicher Decke + erster Luftschicht (Unterkonstruktion, bei Kollisionsprüfung berücksichtigen) + **zweiter Luftschicht** für Haustechnik-Bereich bis UK Rohdecke; Bekleidung/Belag-Abgehängte Decke, nicht tragend, innen.
- Zweite Luftschicht = normale Luftschicht, bei Kollisionen **nicht** berücksichtigt (später Haustechnik-Modell des Fachplaners).
- Zugehöriger Raum von **OK Rohdecke bis UK Abgehängte Decke**.

### Außenwand, Dämmstreifen
- **01 Dämmstreifen** (vor Rohdecke): Träger-Werkzeug, Profil-Träger, Bekleidung/Belag-Dämmung, nicht tragend, außen.
- **02 Rohdecke:** Decken-Werkzeug, Einschichtig, Rohbaudecke, tragend, innen.
- **03 Außenwand:** Wand-Werkzeug, Mehrschichtig, Wand, tragend, außen; nur **bis UK Rohdecke** modellieren (verhindert doppelte Mengen bei Auswertung).

### Außenwand, Brandriegel
- **01 Brandriegel** (vor Rohdecke): Träger-Werkzeug, Profil-Träger, Bekleidung/Belag-Dämmung, nicht tragend, außen.
- **02 Rohdecke:** Decken-Werkzeug, Einschichtig, Rohbaudecke, tragend, innen.
- **03 Außenwand:** Wand-Werkzeug, Mehrschichtig, Wand, tragend, außen; nur **bis UK Rohdecke** (gegen doppelte Mengen).

### Außenwand, Auskragung
- **01 Wand über Auskragung:** Wand-Werkzeug, Mehrschichtig, Wand, tragend, außen; **von OK Rohdecke**, Referenzlinie Kern außen. (UK auf OK Rohdecke → Brüstungshöhe im Fensterstempel anzeigbar.)
- **02 Dämmstreifen:** Träger-Werkzeug, Profil-Träger, Bekleidung/Belag-Dämmung, nicht tragend, außen; eigene Ebene (nur in Schnitt/Ansicht sichtbar).
- **03 Dämmung unter Decke:** Decken-Werkzeug, Mehrschichtig, Bekleidung/Belag-Dämmung, nicht tragend, außen; im Geschoss der Rohdecke erstellen; eigene Ebene (nur in Schnitt/Ansicht sichtbar).
- **04 Wand unter Auskragung:** Wand-Werkzeug, Mehrschichtig, Wand, tragend, außen; von **OK Rohdecke bis UK Rohdecke**, Referenzlinie Kern außen.
- Empfehlung: Dämmstreifen + Dämmung unter Decke aus zwei getrennten Elementen (statt einem Profil-Träger) für bessere Auswertung; Dämmungselemente auf eigene Ebene (nur Schnitt/Ansicht/3D sichtbar).

### Innenwand (2 Varianten)
- **01 Innenwand:** Wand-Werkzeug, Mehrschichtig, Wand, **nicht tragend**, innen; steht auf Estrich → von **OK Estrich bis UK Rohdecke**. Wand um Höhe des Bodenbelags tiefer setzen.
- **02 Innenwand:** Wand-Werkzeug, Mehrschichtig, Wand, **tragend / nicht tragend**, innen; von **OK Rohdecke bis UK Rohdecke**.
- Fußbodenaufbau raum-/bereichsweise; Platzierung mit Bezug auf die jeweilige Geschosshöhe.

### Innenwand zwischen Stützen
- Archicad erzeugt korrekte Darstellung durchdrungener Innenwände über automatische Baustoff-Verschneidung.
- Zur Ermittlung der Anzahl von Anschlussschienen etc. die Wände **an der Stützenachse splitten**.

### Vorwandinstallation
- **01 Vorwandinstallation:** Wand-Werkzeug, **Profilwand**, Klassifizierung Wand-Vorwand/Installationswand, nicht tragend, innen; leerer Bereich mit Baustoff **Luftschicht** füllen; seitlicher Abschluss mit mehrschichtiger Wand. Einstellung **„Auswirkung auf Raum" = „Von Raumfläche und -volumen abziehen"**. Im Eigenschaften-Manager Funktion „Berechnung" für OK-Vorwandinstallation; via Etikett für Plandokumentation darstellbar.
- **02 Bereich für Haustechnik:** Morph-Werkzeug, Morph-Körper, Klassifizierung Raumvorschlag, nicht tragend, innen. Empfehlung: alle Technikbereiche (abgehängte Decken, Böden, Schlitze, Technikräume) mit Morphs füllen → vollständiges TGA-Bereichsmodell zum Abgleich mit Fachplaner.

### Satteldach, Dachdeckung, Sparrenlage, Ringanker
- **01 Dachdeckung:** Dach-Werkzeug, Mehrschichtig, Bekleidung/Belag-Dachdeckung, nicht tragend, außen.
- **02 Sparrenlage mit Dämmung:** Dach-Werkzeug, Mehrschichtig, Klassifizierung Dach, tragend, außen.
- **03 Fußpfette:** Träger / Bibliothekselement, Klassifizierung Dach, tragend, außen.
- **04 Ringanker:** Träger, Profil-Träger, Klassifizierung Dach, tragend, außen; auch in Giebelwänden modellierbar.
- **05 Dämmung vor Ringanker:** Wand-Werkzeug, Profil-Wand, Klassifizierung Wand, nicht tragend, außen; „Auswirkung auf Raumfläche" = „Von Raumfläche und -volumen abziehen"; kann Sonderelemente enthalten.
- **07 Außenwand:** Wand-Werkzeug, Mehrschichtig, Wand, tragend, außen; geht bis **UK Ringanker (04)**.
- Abschließend 02 Sparrenlage, 03 Fußpfette, 04 Ringanker, 05 Dämmung vor Ringanker mit Befehl **„Elemente verschmelzen"** → korrekte Darstellung nach Baustoffprioritäten.

### Satteldach, Datenaustausch mit Holzbausoftware
- Dachaufbau aus einzelnen Bauteilen für korrekten Fußpunkt-Anschluss.
- **01 Dachdeckung:** Dach-Werkzeug, Mehrschichtig, Bekleidung/Belag-Dachdeckung, nicht tragend, außen.
- **02 Sparrenlage mit Dämmung:** Dach-Werkzeug, Mehrschichtig, Dach, tragend, außen.
- **03 Fußpfette:** Träger / Bibliothekselement, Dach, tragend, außen.
- **04 Ringanker:** Träger, Profil-Träger, Dach, tragend, außen.
- **06 Dämmung vor Ringanker:** Wand-Werkzeug, Profil-Wand, Wand, nicht tragend, außen; „Von Raumfläche und -volumen abziehen".
- **07 Außenwand mit Ringanker:** Wand-Werkzeug, Mehrschichtig, Wand, tragend, außen; geht **bis UK des Ringankers**.
- **08 Verkleidung:** Dach-Werkzeug, Mehrschichtig, Dach, tragend, außen.
- Abschließend 02, 03, 04, 06, 08 mit „Elemente verschmelzen" sortieren. Empfohlen für Holzbau-Übergabe: dreiteiliger Dachaufbau aus **Oberdach, Dämmschicht (Sparrenlage), Verkleidung**.

### Satteldach, Giebelwand, Ortgang, Ringanker
- **01 Dachdeckung:** Dach-Werkzeug, Mehrschichtig, Bekleidung/Belag-Dachdeckung, nicht tragend, außen.
- **02 Sparrenlage mit Dämmung:** Dach-Werkzeug, Mehrschichtig, Dach, tragend, außen.
- **03 Außenwand (Giebel):** Wand-Werkzeug, Mehrschichtig, Wand, tragend, außen; an jeder Stelle **höher als Dachdeckung (01)**.
- **04 Ringanker:** Träger oder Profil-Träger, Dach, tragend, außen; verschneidet sich selbstständig über Baustoffe mit Außenwand; unterer Trägerabschluss darf nicht in traufseitige Außenwand überstehen.
- Workflow: 03 Außenwand + 01 Dachdeckung mit **„Elemente mit Dach/Schale trimmen"** verschneiden; unterste Bauteilschicht des Oberdachs muss höhere Baustoffpriorität haben als alle Außenwand-Baustoffe; dann 02, 03, 04 mit „Elemente verschmelzen" sortieren.

### Flachdach mit Gefälle
- **01 Rohdecke:** Decken-Werkzeug, Einschichtig, Rohbaudecke, tragend, außen.
- **02 Dämmung** (Mindestdicke): Decken-Werkzeug, Einschichtig, Bekleidung/Belag-Dämmung, nicht tragend, außen.
- **03 Gefälledämmung/Dachhaut:** Dach-Werkzeug (Einzeldachflächen, geneigt), Einschichtig oder Mehrschichtig, Klassifizierung Bekleidung/Belag-Dämmung bzw. Bekleidung/Belag-Dachdeckung, nicht tragend, außen.
- Workflow: erste Dämmlage (Mindestdicke) mit Decken-Werkzeug auf Rohdecke; Gefälledämmung + restlicher Dachaufbau mit Dach-Werkzeug darüber; dann über **Solid-Element-Befehle** die Dämmung (02) von Gefälledämmung/Dachhaut (03) mit „Abzug mit Verlängerung nach unten" abziehen. Alternativ: alles oberhalb Rohdecke aus einem mehrschichtigen Dach, dann Rohdecke vom Dach abziehen.

### Attika
- **01 Attika:** Wand-Werkzeug, Profil-Wand / Mehrschichtig, Wand, tragend, außen; **Platzierung auf OK-Rohdecke**.
- **02 Rohdecke/Flachdach:** Decken-Werkzeug, Einschichtig, Rohbaudecke, tragend, außen.
- **03 Attika-Abdeckung:** Träger-Werkzeug (bessere Sichtbarkeit in Dachaufsichten), Profil-Träger, Klassifizierung Bekleidung/Belag, nicht tragend, außen; als gesondertes Element für gewerkeweise Auswertung.
- **04 Gefälledämmung:** Geneigter Aufbau – Einzeldachflächen, Einschichtig/Mehrschichtig, Bekleidung/Belag-Dämmung, nicht tragend, außen.
- **05 Dämmung:** Decken-Werkzeug, Einschichtig, Bekleidung/Belag-Dämmung, nicht tragend, außen.

### Deckendurchbruch
- Öffnungen/Durchbrüche in Decken allgemein mit **Öffnungs-Werkzeug**; pro betroffenem Bauteil eine eigene Öffnung (korrekte Auswertung/Übergabe).
- **01 Deckendurchbruch:** Öffnungs-Werkzeug, Klassifizierung Durchbrüche/Schlitze-Öffnung, innen.
- **02 Aufzugsschacht:** Öffnungs-Werkzeug, Durchbrüche/Schlitze-Öffnung, innen.
- **03 Atrium/Innenhof o.Ä.:** als geometrisches Loch (Decken-Werkzeug schneiden) oder als Öffnung; **keine Solid-Element-Befehle** verwenden.
- In Fußbodenaufbauten **keine** Öffnungen platzieren — als geometrische Löcher mit dem Decken-Werkzeug aussparen.
- **Warnung:** Geometrische Löcher werden beim **IFC-Export nicht separat als IFC-Openings** ausgegeben.
- Öffnung/Durchbruch wird im Grundriss nur angezeigt, wenn das zugehörige Bauteil eingeblendet ist → Öffnung in Rohdecke immer im Ursprungsgeschoss UND ein Geschoss darüber/darunter anzeigen lassen.

### Wanddurchbruch
- Öffnungen/Durchbrüche in Wänden mit **Öffnungs-Werkzeug**; pro Bauteil eine gesonderte Öffnung.
- **01 Wanddurchbruch:** Öffnungs-Werkzeug, Durchbrüche/Schlitze-Öffnung, innen.
- **02 Wandschlitz:** Öffnungs-Werkzeug, Klassifizierung Durchbrüche/Schlitze-**Nische**, innen.
- **03 Leere Fensteröffnung:** Fenster-Werkzeug, Klassifizierung Fenster, außen/innen.
- **04 Leere Türöffnung:** Tür-Werkzeug, Klassifizierung Tür, außen/innen.
- Leere Fenster-/Türöffnungen mit Fenster-/Tür-Werkzeug erstellen und als Fenster/Tür klassifizieren → einheitlicher Fenster-/Türstempel, korrekte Listen/Auswertungen.
- Durchbruch wird im Grundriss nur bei eingeblendetem Bauteil angezeigt.

### Körper für Flächen-/Volumenberechnung (DIN 277)
- **01 Körper für Flächen-/Volumenberechnung:** Morph-Werkzeug, Klassifizierung Raum oder Bauelement (beliebig), tragende Funktion nicht definiert, Lage nicht definiert; **Klassifizierung nach DIN 277 muss festgelegt werden**; **Unterkante = Geschosshöhe**.
- Regelfall und Sonderfall als **separate Morph-Körper** modellieren; jedem Morph eine Klassifizierung nach DIN 277 zuweisen.
- Pro Geschoss Morph-Körper erstellen, die gemeinsam die Außenkubatur abbilden → Berechnung von Bruttorauminhalt und Bruttogrundfläche (Modell benötigt automatisch platzierte Räume).
- Morph-Körper + Morph-Flächen als IFC exportierbar → Kostenschätzung z.B. mit BKI.

### Grundflächen nach DIN 277 (GF, AF, BF, UF)
- Grundstücksfläche (GF), Außenanlagenfläche (AF), bebaute Fläche (BF), unbebaute Fläche (UF) nach DIN 277 in 3D modellieren, um sie als IFC zu übergeben.
- **01 Grundfläche nach DIN 277:** Morph-Werkzeug, Klassifizierung Raum oder Bauelement (beliebig), tragende Funktion/Lage nicht definiert; Eigenschaft **Flächenart nach DIN 277** für jede Fläche festlegen; Flächen entsprechend DIN-277-Vorgaben modellieren. Morph-Flächen dürfen sich im Modell überlagern; IFC-Export für Kostenschätzung (BKI) möglich.
