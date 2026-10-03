# ABWEICHUNGEN PDF ↔ DXF — Mollgasse (alle Geschosse)

Aus dem Detail-Zweitpass (Spalte abweichung_pdf_dxf) + bekannte Fälle.

- **S.1 (EG):** PDF nennt die gezeigte Tür 'Haupteingangstür'. Der im Bild gezeigte horizontale down-RZ passt geometrisch zu Handle 20286 (Wand Vorplatz/Müllraum). Die auf S.6 als Haupteingangstür bezeichnete Leuchte (D)=20240 liegt aber ~2.2m weiter östlich und ist 90° rotiert (vertikal). Entweder zeigt S.1 eine zweite Ausgangstür (Müllraum/Vorplatz) oder der Begriff 'Haupteingang' wird für beide Westtüren benutzt.
- **S.4 (EG):** PDF spricht von 'einer Notleuchte'; im DXF liegen an dieser Tür ZWEI deckungsgleiche down-Blöcke als beidseitig-Gruppe (202CC + 2137C, Abstand ~66mm) = doppelseitiges Schild. Im Bild ist das nicht unterscheidbar.
- **S.5 (EG):** (A): PDF sagt 'Pfeil nach links'; DXF zeigt left-Block um 90° rotiert mit Welt-Pfeil 269.99° (Süd/unten im Bild). Lesart: 'links' = Blockvarianten-Name + personenrelative Abbiegung (wer nach Westen läuft, biegt bei Pfeil-Süd nach LINKS ab); bildabsolut zeigt der Pfeil nach unten.
- **S.6 (EG):** (D): PDF 'Pfeil nach unten' = down-BLOCKVARIANTE (Ausgang hier); im DXF ist der Block um 89.99° rotiert, Welt-Pfeil 0° (Ost) — der Pfeil zeigt im Plan also nach rechts ins Gebäudeinnere, nicht 'nach unten' im Weltkoordinatensinn. 'Nach unten' meint die Symbolik auf dem Schild (Türwand-Montage).
- **S.10 (EG):** (H) 'Pfeil nach unten': DXF-Block down um 269.99° rotiert, Welt-Pfeil 179.99° (West). 'Nach unten' bezeichnet wieder die Blockvariante, nicht die Weltrichtung. Zudem nennt der Text die Tür wechselnd 'Hauptausgang'/'Haupteingangstür' für dieselbe Tür.
- **S.11 (EG):** Müllraum-(A): PDF 'Notleuchte mit Pfeil nach unten'; DXF: down-Block um 269.99° rotiert -> Welt-Pfeil 179.99° (West in den Raum). Wieder Variantenname vs. Weltrichtung. Zusätzlich: Die türkise Anmerkung im DXF argumentiert, eine ANTIPANIKLEUCHTE sei 'nicht unbedingt notwendig' — der PDF-Fließtext formuliert dieselbe Situation positiv ('reicht eine Notleuchte aus').
- **S.13 (EG):** Keine Sichtlinie zu (C) im DXF — die einzige EG-Sichtlinie (Handle 212EE) liegt beim Hauptausgang, nicht in diesem Bildausschnitt; die Erkennung der (C) wird hier nur im Text beschrieben
- **S.16 (1OG):** Die Alternativ-Position von (C) (mittig im Gang) existiert nur als Bild-Variante im PDF-Screenshot; das DXF enthält genau EINE (C)-Instanz (95019, vor der Stiege) — keine zweite Alternativ-Instanz als Block
- **S.19 (1OG):** Text behauptet, BEIDE türkisen Linien (von '2OG' und von '1OG' bei Top 2+3) führten zur Notleuchte (B); im DXF endet Linie 95621 an (B), Linie 957AC aber an (A) — eine der beiden Sichtlinien dokumentiert also die Sicht auf (A), nicht (B) (Text zudem in sich gemischt: erst 'A direkt sichtbar', dann 'Linien zur B')
- **S.21 (2OG):** Die drei Stiegenhaus-Sichtlinien liegen im DXF auf dem Architektur-Layer '00-AUF---------M0' statt auf Layer '0' wie alle übrigen Sichtlinien — vermutlich Zeichen-Versehen des Owners (inhaltlich korrekt)
- **S.23 (2OG):** Dieselben Top-Nummern 13/14/15 wie der Gang auf S.20 — es ist derselbe Gang, aber als separate Plan-Kopie im DXF mit ANDERER (D)-Instanz gezeichnet: S.20-(D)=852B6 (Pfeil-unten-Block an der Tür), S.23-(D)=852E4 (Pfeil-links-Block mittig zur Stiege); die beiden Erklärfiguren zeigen also zwei verschiedene (D)-Situationen unter derselben Kennung
- **S.25 (2OG):** (C) samt Nordast (2 Personen, 2 Sichtlinien) ist im Bild sichtbar, wird aber auf S.25/26 nicht erklärt; zusätzlich existiert im 2OG-DXF die Leuchte 8532F (down-Block, xy -72431/61138) ganz ohne Kennung und ohne PDF-Erwähnung
- **S.29 (3OG):** Das 3OG-DXF enthält westlich an der Stiege zusätzlich die down-Leuchte 78DFD (rot 269.71°, welt_pfeil 179.71°) mit DXF-Kennung „(A)“ (Text-Handle 793DF, dist 277mm) samt 2 Personen (79084, 792FF) und 3-Punkt-Sichtlinien-Polylinie 79301 — dieser (A)-Teil liegt außerhalb des PDF-Bildausschnitts und wird auf S.29/30 nirgends erwähnt
- **S.35 (4OG):** Die im PDF als „(B)“-Ersatz gezeigte Falsch-Leuchte ist im DXF die Instanz 413E8, die dort die Kennung „(D)“ trägt (Text-Handle 415D9) und im Übersichtsbild S.36 als (D) im oberen Gang erscheint — PDF-Beschriftung (B) und DXF-Kennung (D) widersprechen sich
- **S.36 (4OG):** Seitentext ist ein wortgleiches Duplikat des Vergleichstexts von S.35 (ober- UND unterhalb des Bildes wiederholt), das Bild zeigt aber NICHT die Falsch-Variante, sondern die korrekte Gesamtübersicht; zudem: (C)=415B6 und (D)=413E8 sind im Bild beschriftet, werden aber in keinem Seitentext S.31-36 erklärt; 413E8 hat Doppelrolle (hier (D) im oberen Gang, auf S.35 als Falsch-„(B)“ präsentiert)
- **S.37 (4OG):** Die als „falsch“ markierte Demo-Variante bei (C) ist im DXF real gezeichnet (415B6 = RZ_right um 90° gedreht, Pfeil oben); rotes Rechteck/„falsch“-Text sind in der Evidenz-Extraktion nicht als Entitäten erfasst. S.38 nennt (C) später „Pfeil nach rechts“ — das gilt aus Sicht einer nach Westen blickenden Person (Plan-Pfeil zeigt nach oben).
- **S.38 (4OG):** Text-Reihenfolge C→D→B entspricht nicht der West-Ost-Geometrie des Bildes (D und B liegen östlich, C ganz westlich am Ende des unteren Laufs); die Kette stimmt nur, wenn die DG-Personen am Westende ankommen, die Runde über oberen Lauf/Ostwende laufen und am Ende wieder bei (C) abwärts abbiegen.
- **S.39 (DG):** DXF enthält im Westteil des DG zwei weitere Leuchten (B)=206DB (ARR-left, x≈-17184) und (D)=206D6 (ARR-down, x≈-16047) samt Kennungen 206DA/206DD und Sichtlinie 206E0 — in den PDF-Seiten 39–41 weder im Bild noch im Text behandelt.
- **S.40 (DG):** Die blaue Lichtkuppel-Markierung ist in der Evidenz-Extraktion nicht als eigene Entität erfasst (nur im PNG sichtbar); die „ursprünglich vorgesehene Position“ von (A) existiert im DXF nicht als Marker — nur die versetzte Ist-Position.
- **S.41 (1KG):** Kennungsbuchstaben sind im 1.KG nicht eindeutig: dieselben Buchstaben (A)/(B)/(C) existieren an der ER-Stiege erneut (1BEE4/1CD8C/1CB3E, Kennungen mit Leerzeichen „(B )“ usw.) — kennung_map führt für 1KG deshalb A doppelt (1BEE4+1BCBB) und B/C nur einfach.
- **S.44 (1KG):** Zuordnung der beiden Kreise zu „Wand“ vs. „Decke“ ist aus den Koordinaten plausibel (1CA9B liegt mittig über dem Stiegenlauf), im DXF aber nicht beschriftet unterscheidbar.
- **S.47 (1KG):** kennung_map.json führt für 1KG KEINEN Key „E“ (auch kein „D“): die Kennungen „(B )/(C )/(D )/(E )“ mit Leerzeichen vor der Klammer wurden vom Matcher nicht erfasst — Zuordnung (E)→1BF97 hier manuell über Koordinaten (≈346mm) belegt.
- **S.48 (1KG):** Leuchte (D) 1BFC3 (Kennung „(D )“ 1C5E7) ist im Bild deutlich sichtbar und hat im DXF eine eigene Blicklinie 1CACF, wird im PDF-Text der Seite aber nicht erklärt; ebenso ist die Übergabe-Blicklinie 1CAD1 zu „(B )“ 1CD8C schon gezeichnet, textlich aber erst Folgeseiten-Stoff. kennung_map.json hat für 1KG keine Keys C(ER-Strang)/D/E (Leerzeichen-Kennungen „(C )“ usw. nicht gematcht; Map-Key „C“ zeigt auf die random-Raum-Stiege 1BE99).
- **S.57 (2KG):** BEKANNTER B↔C-FEHLER, im Bild verifiziert: Der Folgetext (S.58) behauptet, die Antipanikleuchte (B) sei 'vertikal ausgerichtet' — im Bild S.57 und im DXF liegt (B) (Handle 1C707, rot 178,7°) eindeutig HORIZONTAL auf der gelben Diagonale. Vertikal ausgerichtet ist stattdessen die Antipanikleuchte (C) (Handle 1C706, rot 268,7°, Bild S.59). Die Orientierungs-Aussagen von (B) und (C) sind im Text vertauscht; Positionen, Diagonalen und Kennungen selbst stimmen mit dem DXF überein.
- **S.58 (2KG):** B↔C-Textfehler (bekannt, dies ist die Textseite dazu): Die Aussage 'Die Antipanikleuchte wurde außerdem vertikal ausgerichtet' trifft auf (B) NICHT zu — DXF 1C707 rot 178,7° = horizontal (so auch im Bild S.57 sichtbar). Vertikal ist die Antipanik (C) (1C706, rot 268,7°, S.59). Der Begründungs-Absatz zur vertikalen Ausrichtung gehört inhaltlich zu (C).
- **S.59 (2KG):** Gegenstück zum B↔C-Fehler: Die auf S.58 fälschlich (B) zugeschriebene 'vertikal'-Begründung gehört zu dieser Leuchte (C) — (C) ist die vertikal ausgerichtete Antipanik (DXF 1C706, rot 268,7°). Text/Bild dieser Seite selbst sind konsistent (Diagonale, Position, ER-Nummern stimmen mit dem DXF überein).
- **S.75 (2KG):** 'Pfeil nach rechts' bei (M)/(N) beschreibt die Bild-Ansicht; die DXF-Welt-Pfeile sind (M) ≈269° und (N) ≈179° — die Mollgasse-Bildausschnitte sind gegenüber Weltkoordinaten gedreht
- **S.76 (2KG):** Rote Trennlinie und rote Anmerkungstexte sind im Evidenz-JSON nicht als Kategorie extrahiert (Kategorien nur leuchten/personen/sichtlinien/fluchtwege/kennungen/gelb_marker) → Handles unbekannt
- **S.77 (2KG (Bild: EG als Referenz)):** FREIHEIT/KEINE-FREIHEIT-Kästen und alle EG-Inhalte liegen im EG-DXF und sind im 2KG-Evidenz-JSON nicht enthalten
- **S.79 (2KG):** (A): PDF sagt 'Pfeil nach unten', der gezeichnete Pfeil zeigt in Weltkoordinaten nach oben (≈90°), weil der ARR-down-Block um ≈180° gedreht wurde — genau das meint 'entgegen der tatsächlichen Richtung des Fluchtwegs'; die orange Alternative hat im DXF keine Buchstaben-Kennung
- **S.82 (2KG):** Die Antipanikleuchte (B) erscheint im Bild als gerenderter Leucht-Balken (Block Antipanikleuchte-RIVO), nicht als RZ-Kästchen; das kleine leere Rechteck mittig hat keine Entsprechung im Evidenz-JSON
- **S.84 (2KG):** Die breiten gelben Blockpfeile im Doppelparker-Bereich sind im Evidenz-JSON nicht unter gelb_marker erfasst (die 10 extrahierten gelb_marker liegen an anderen Koordinaten) → Handles unbekannt; (I) ist im Bild gelabelt, wird im Seitentext aber nicht erwähnt
- **S.92 (2KG):** Menschen flüchten stiegenAUFwärts (grüne Pfeile + Text „geht hinauf richtung 1KG“), während der rote Architektur-Stiegenpfeil im Bild abwärts zeigt — die auf S.93 zitierte UG-Regel „in Richtung des Stiegenhauspfeils“ ist nur aus Bild+Text gemeinsam eindeutig lesbar
- **S.94 (2KG):** BEKANNTER FALL: PDF-Text sagt „Notleuchte mit Pfeil nach rechts verwendet und so rotiert, dass der Pfeil … nach links zeigt“ — im DXF ist (N) aber ein ARR-left-Block (1C95A, rot 179.84°, xscale -29.866). Die sichtbare Pfeilrichtung (links) stimmt in PDF und DXF überein; nur die benannte Block-Familie (rechts vs. left) weicht ab. Lehre für die Engine: nie die rohe Blockfamilie/rot lesen, sondern die effektive Anzeige-Richtung (Spiegelung+Rotation) — deckt Regel #8 (Blick=180+rot bei xs>0).

## Einordnung (kuratiert 2026-09-30)

**Kein Fall stellt eine Zeichen-REGEL in Frage.** Die 34 Vermerke zerfallen in
6 Klassen:

1. **Sprachkonvention „Blockvariante ≠ Weltrichtung"** (S.5/6/10/11/75/79/94):
   „Pfeil nach unten/links/rechts" benennt die BLOCK-Familie; die Weltrichtung
   entsteht erst durch Rotation (+ Spiegelung bei xscale<0). KEIN Fehler —
   aber die wichtigste Lese-Lehre für die Engine (deckt Regel #8 / NB-R00).
   **Korrektur zu S.79:** der um 180° gedrehte down-Block ENTGEGEN der
   Fluchtrichtung ist exakt NB-R06 (Front zur ankommenden Person) —
   regelkonform, kein Abweichungsfall.
2. **Bekannte PDF-Textfehler** (S.57/58/59 B↔C-Vertauschung — im Bild UND DXF
   verifiziert; S.36 Text-Duplikat; S.19 „beide Linien zu (B)"; S.35 (B)↔(D)-
   Kennungs-Doppelrolle 413E8): an Owner melden (S.57 seit 2026-09-20 offen).
3. **Bekannte Kopier-/Arbeitsreste** (S.4: 202CC+2137C ist KEINE beidseitig-
   Gruppe, sondern der dokumentierte EG-Kopier-Rest `2137C` von der
   Owner-TODO-Liste 2026-09-18; ebenso 3OG-Fragment-Familie): beim Validieren
   ausfiltern, Owner-Löschliste bleibt offen.
4. **Im DXF vorhanden, im PDF unerklärt** (S.25 `8532F` ohne Kennung; S.29
   `78DFD`-(A)-Szene; S.39 DG-West `206DB`/`206D6`; S.48 `(D) 1BFC3`): nach
   Basis-Regeln bewertet unauffällig — Kandidaten für PDF-Erweiterung, keine
   Regel-Widersprüche (deckt offene_fragen.md „unerklärte Leuchten").
5. **Extraktions-Lücken unserer Evidenz** (S.76 rote Trennlinie/Texte; S.40
   blaue Lichtkuppel-Markierung; S.84 gelbe Blockpfeile; S.21 Sichtlinien auf
   Architektur-Layer; S.41/47 Leerzeichen-Kennungen „(B )" im kennung_map-
   Matcher): Werkzeug-Backlog, keine Plan-Fehler.
6. **Benennungs-Unschärfen der PDF** (S.1/S.10 „Haupteingang/Hauptausgang"
   für zwei Westtüren; S.23 gleiche Kennung (D) für zwei Situationen;
   S.44 Wand/Decke-Kreise unbeschriftet): Owner-Fragen, Regelgehalt unberührt.

**Für den Engine-Einbau relevant:** Klasse 1 (Lese-Konvention ist in der
Engine korrekt implementiert — orientation.py + Regel #8), Klasse 3
(Validierungs-Filter für Kopier-Reste), Klasse 5 (Extraktor-Erweiterungen
vor dem nächsten GT-Re-Run).