# Bild-Lehren — EN 1838:2019 + OVE-Fachinfo E-08
**Methode:** Alle Seiten als Bild gesichtet (110 dpi), 2026-08-28. Ergänzt die Text-Digests um die visuellen Konzepte.

Gesichtet: EN 1838 (ÖNORM-Ausgabe 2019-11-15, Kerntext = EN 1838:2013 D) — 22 Seiten;
OVE-Fachinformation E08:2021-04-01 — 6 Seiten. Die Norm enthält genau **4 nummerierte
Bilder** (Bild 1 S.4, Bild 2 + Bild 3 S.10, Bild 4 S.14) und **1 Tabelle** (Tabelle 1 S.11).
Die E-08 enthält **1 Bild** (Bild 1, S.3) und **2 Tabellen** (Tabelle 1 S.4, Tabelle 2 S.5).

## EN 1838 — Bild für Bild

### Bild 1 (S.4 / s006) — Arten der Notbeleuchtung (Hierarchie-Baum)
Kastendiagramm in 4 Ebenen, Verbindung über rechtwinklige Linien:

```
                    ┌───────────────┐
                    │ Notbeleuchtung│                     (Ebene 1: Oberbegriff)
                    └───────┬───────┘
          ┌─────────────────┴──────────────────┐
┌─────────┴────────────┐              ┌────────┴──────────┐
│Sicherheitsbeleuchtung│              │ Ersatzbeleuchtung │   (Ebene 2)
└─────────┬────────────┘              └───────────────────┘
  ┌───────┼──────────────────────┬──────────────────────────┐
┌─┴──────────────────┐ ┌─────────┴──────────┐ ┌─────────────┴───────────┐
│Sicherheitsbeleuchtg.│ │Antipanikbeleuchtung│ │Sicherheitsbeleuchtg. für│  (Ebene 3)
│ für Rettungswege    │ │                    │ │Arbeitsplätze m. besond. │
└─────────┬──────────┘ └────────────────────┘ │Gefährdung               │
┌─────────┴─────────┐                          └─────────────────────────┘
│ Sicherheitszeichen│                                              (Ebene 4)
└───────────────────┘
```

Wesentlich am Bild (nicht aus dem Text allein ersichtlich):
- **Ersatzbeleuchtung ist Geschwister der Sicherheitsbeleuchtung**, nicht deren Unterart —
  sie hängt direkt an „Notbeleuchtung".
- Die Sicherheitsbeleuchtung zerfällt in exakt **drei** Unterarten: Rettungswege,
  Antipanik, Arbeitsplätze mit besonderer Gefährdung.
- **„Sicherheitszeichen" hängt ausschließlich unter „Sicherheitsbeleuchtung für
  Rettungswege"** (4. Ebene) — Rettungszeichen sind im Normmodell ein Bestandteil der
  Rettungsweg-Beleuchtung, keine eigene vierte Kategorie neben Antipanik.

**LEHRE für die Engine:** Das Datenmodell einer Platzierung braucht genau diese Taxonomie
als Enum/Feld (`rettungsweg | antipanik | arbeitsplatz_gefaehrdung | ersatz`), wobei
Rettungszeichen (RZ) als Kind der Rettungsweg-Kategorie modelliert werden (RZ-Platzierung
erbt die Rettungsweg-Anforderungen: Sichtbarkeit, ≥2 m Montagehöhe, Erkennungsweite).
Ersatzbeleuchtung ist ein Sonderpfad (4.5): nur relevant, wenn die LB sie explizit fordert.

### Bild 2 (S.10 / s012) — Horizontal verlaufende Rettungswege (Blendungs-Zone)
Vertikaler **Raum-/Flur-Querschnitt**: links eine Wand, oben die Decke, unten der Boden
(Schraffur). Zwei Leuchten eingezeichnet:
1. **Wandleuchte** an der linken Wand (kleines Rechteck),
2. **Deckenleuchte** an der Decke (kleines Rechteck mit Sockel).

Von jeder Leuchte ist die **Senkrechte nach unten** (Vertikale durch den Lichtpunkt) als
Bezugsachse gezeichnet. Von dieser Vertikalen aus ist der Winkel **60°** mit Winkelbogen
kotiert. Der **grau gerasterte Keil** beginnt bei 60° gegen die Vertikale und reicht bis
**90° (= Horizontale auf Augenhöhen-Ebene)** — bei der Deckenleuchte ein Keil schräg nach
rechts unten bis zur Horizontalen, bei der Wandleuchte spiegelbildlich in den Raum hinein.
Beide Keile tragen die Ziffer **1**; Legende: „1 = Bereich, in dem die maximale Lichtstärke
die Werte in Tabelle 1 nicht überschreiten darf."

Geometrische Aussage des Bildes:
- Die Blendungsbegrenzung gilt **nur im Winkelband 60°–90° gegen die Vertikale** (das ist
  der Bereich, der einem aufrecht gehenden Menschen horizontal bis leicht schräg von oben
  in die Augen strahlt) — und zwar **für alle Azimutwinkel** (rotationssymmetrisch um die
  Leuchten-Vertikale).
- **Unterhalb von 60°** (steiler nach unten gerichtetes Licht) ist die Lichtstärke
  unbegrenzt — dort darf die Leuchte ihr Nutzlicht konzentrieren.
- Das Bild zeigt Wand- UND Deckenmontage: die Regel ist montageortunabhängig, die
  Bezugsachse ist immer die Vertikale durch den Lichtpunkt.

**LEHRE für die Engine:** Blendungsprüfung = Kegelgeometrie um die Leuchten-Vertikale:
Lichtstärkewerte der Leuchte im Polarwinkel-Band γ ∈ [60°, 90°] gegen I_max aus Tabelle 1
prüfen (Grenzwert-Auswahl über die Montagehöhe h). Für die Platzierung heißt das: Leuchten
mit breitstrahlender Charakteristik in niedrigen Räumen (h < 2,5 m ⇒ I_max nur 500 cd)
sind die kritische Kombination; bei Katalog-Auswahl ist die Befestigungshöhe die
Eingangsgröße der Grenzwertzeile.

### Bild 3 (S.10 / s012) — Andere Rettungswege und Flächen (Blendung bei Niveauänderung)
Gleicher Querschnitt-Typ wie Bild 2 (Wandleuchte links, Deckenleuchte), aber der Boden ist
**keine Ebene**: rechts im Schnitt sind **Stufen/Treppenabsätze** gezeichnet (mehrere
Niveausprünge in der Bodenlinie). Der entscheidende visuelle Unterschied: um jede Leuchte
ist jetzt ein **voll gerasterter Kreis** (Kugel um den Lichtpunkt) gezeichnet — kein
60°-Keil mehr. Ziffer 1 mit derselben Legende (Bereich, in dem I_max aus Tabelle 1 gilt).

Geometrische Aussage: Sobald der Rettungsweg **nicht horizontal** verläuft (Treppen, Rampen,
Niveauänderungen) oder es sich um sonstige Flächen (Antipanik) handelt, gilt die
Lichtstärkebegrenzung **in allen Raumrichtungen** („bei keinem Winkel überschreiten",
4.2.3 Abs. 3) — weil die Blickrichtung der Fliehenden auf Treppen geneigt ist und damit
jeder Abstrahlwinkel zur Blendquelle werden kann.

**LEHRE für die Engine:** Der Blend-Check hat **zwei Modi**, ausgewählt durch die
Weg-Topologie aus dem RaumModell: (a) Segment horizontal ⇒ Begrenzung nur 60°–90°;
(b) Segment enthält Treppe/Rampe/Niveauänderung (oder Antipanik-Fläche) ⇒ Begrenzung
für **alle** Winkel. Das RaumModell muss also pro Segment ein Flag „horizontal /
niveauändernd" liefern können — Niveauänderungen sind ohnehin hervorzuhebende Stellen
(4.1.2 b, c).

### Tabelle 1 (S.11 / s013) — Grenzwerte der physiologischen Blendung (visuell geprüft)
Drei Spalten, sechs Zeilen; visuell bestätigt:

| Befestigungshöhe h (m) | I_max Rettungswege + Antipanik (cd) | I_max Arbeitsplätze bes. Gefährdung (cd) |
|---|---|---|
| h < 2,5 | 500 | 1 000 |
| 2,5 ≤ h < 3,0 | 900 | 1 800 |
| 3,0 ≤ h < 3,5 | 1 600 | 3 200 |
| 3,5 ≤ h < 4,0 | 2 500 | 5 000 |
| 4,0 ≤ h < 4,5 | 3 500 | 7 000 |
| h ≥ 4,5 | 5 000 | 10 000 |

Muster: Spalte 3 = exakt **2 × Spalte 2** in jeder Zeile; Grenzwerte steigen mit der
Montagehöhe (höher montiert = weiter aus dem Blickfeld = mehr Lichtstärke erlaubt).

### Bild 4 (S.14 / s016) — Erkennungsweite (Sichtgeometrie des Rettungszeichens)
Zweiteilige Grafik:
- Links: das grüne Rettungszeichen (ISO-7010-Stil: laufende Person durch Tür + weißer
  Richtungspfeil nach rechts auf grünem Grund) als Beispiel des betrachteten Zeichens.
- Rechts: **Seitenansicht der Sichtgeometrie**: eine vertikale Linie stellt die
  Zeichentafel dar, ihre Höhe ist mit **h** kotiert (Maßpfeile oben/unten). Von Ober- und
  Unterkante der Tafel laufen zwei Sichtstrahlen kegelförmig zu einem **Augensymbol**
  rechts. Durch die Mitte verläuft eine horizontale **Strichpunkt-Sichtachse** (zentrale
  Blickrichtung). Unter der Grafik die kotierte Distanz **l** von der Tafel bis zum Auge.

Aussage: Die Erkennungsweite ist eine reine **Proportionsgeometrie** entlang der zentralen
Sichtachse: `l = z · h` mit h = **Zeichenhöhe** (Höhe der Tafel, nicht Montagehöhe!),
z = 100 (beleuchtet) bzw. z = 200 (hinterleuchtet). Ergänzende Textregel (4.1.1/5.5): das
Zeichen soll ≤ 20° über der horizontalen Blickrichtung liegen (bei maximaler
Erkennungsweite) — der Sichtkegel des Bildes ist bewusst flach/horizontal gezeichnet.

**LEHRE für die Engine:** Jede RZ-Platzierung erzeugt einen **Sichtbarkeits-Radius**
l = z·h um das Zeichen (Kreis in der Planebene, gerichtet auf die Zeichen-Normale).
Abdeckungsprüfung: von jedem Punkt des Rettungswegs muss mindestens ein RZ innerhalb
seines l-Radius **und** in Sichtlinie (keine Wand dazwischen) liegen. Die Zeichengröße h
ist damit ein Auslegungsparameter: größeres Panel ⇒ größerer Deckungsradius ⇒ weniger
Zeichen. Die 20°-Regel begrenzt zusätzlich die Montagehöhe relativ zur Distanz
(Höhendifferenz ≤ tan(20°) · Distanz ≈ 0,36 · Distanz).

### Kein Bild vorhanden — Mittellinien-/Streifen-Konzept (4.2.1) ist reiner Text
Wichtiger Sichtungs-Befund: In dieser Ausgabe (EN 1838:2013 D / ÖNORM 2019) gibt es **kein
Bild** zur Rettungsweg-Ausleuchtungsgeometrie. Das Mittellinien-/Streifen-Konzept steht
ausschließlich als Text in 4.2.1:
- Rettungsweg **Breite ≤ 2 m**: ≥ **1 lx** horizontal am Boden **entlang der Mittellinie**;
- der **Mittelbereich** (mittiger Streifen von mindestens der **halben Wegbreite**) muss
  ≥ **50 %** davon (= 0,5 lx) erreichen;
- **breitere Wege** = Behandlung „als mehrere 2 m breite Streifen" **oder** mit
  Antipanikbeleuchtung (0,5 lx auf freier Bodenfläche im Kernbereich, Randstreifen 0,5 m
  ausgenommen, 4.3.1);
- Gleichmäßigkeit entlang der Mittellinie: U_d = E_min : E_max ≥ 1 : 40 (4.2.2).

Das implizite geometrische Modell (aus Text rekonstruiert, kein Normbild):

```
Wand ────────────────────────────────────────
      Randzone            ≥ 0,5 lx   ┐
   ── Mittellinie ······· ≥ 1 lx     │ Mittelbereich ≥ B/2 (zentriert)
      Randzone            ≥ 0,5 lx   ┘
Wand ────────────────────────────────────────   Wegbreite B ≤ 2 m
```

## E-08 — visuelle Konzepte

### Bild 1 (S.3) — Erläuterung der Begriffe zur sicheren Flucht (verschachtelte Pfeile)
Drei ineinander geschachtelte, nach rechts zeigende Blockpfeile:
- **Gelb (außen): Verkehrsweg** — beginnt ganz links;
- **Grün (darin): Fluchtweg** — beginnt nach dem gelben Anfangsstück;
- **Rot (Spitze): gesicherter Fluchtbereich** — letztes Stück, mündet in die Beschriftung
  „Endausgang; ins sichere Freie".

Zwei Maßketten über dem Pfeil:
- **„max. 10 m"** über dem gelben Anfangsstück: von jedem Punkt der Arbeitsstätte muss
  nach höchstens 10 m Verkehrsweg ein Fluchtweg erreicht sein;
- **„i.d.R. max. 40 m"** über der Strecke ab Fluchtweg-Beginn bis zum Endausgang: der
  Bereich, durch den der Fluchtweg führt, muss in seinem gesamten Verlauf bis zum
  Endausgang bzw. ins sichere Freie den AStV-Anforderungen entsprechen (Fluchtweglänge
  kann laut Anmerkung gemäß OIB-Richtlinie/Brandschutzkonzept auch länger sein).

**LEHRE für die Engine:** Die Fluchtweg-Zirkulation ist eine **Kette aus drei
Wegklassen** mit Längenbudgets: Punkt → (≤10 m) → Fluchtweg-Eintritt → (i.d.R. ≤40 m
gesamt) → Endausgang/sicherer Bereich. Für die Platzierung heißt das: schon der
Verkehrsweg-Anteil im Arbeitsraum kann Teil des Fluchtwegs sein (E-08 Abschn. 3: in
großen Räumen beginnt der Fluchtweg **im Raum selbst**) und ist dann wie ein
Rettungsweg auszustatten. Die 10 m/40 m sind Prüfgrößen für das RaumModell
(Distanzfeld vom Endausgang rückwärts), keine Leuchtenabstände.

### Tabelle 1 (S.4) — Ausstattung von Arbeitsräumen (Entscheidungsmatrix, visuell geprüft)
Struktur bestätigt: **3 Spalten** — (1) Raumgröße in m², (2) Arbeitsräume, in denen bei
natürlichem Licht gearbeitet wird, (3) Arbeitsräume ohne natürliche Belichtung. 4 Zeilen:

| Raumgröße (m²) | mit natürlichem Licht | ohne natürliche Belichtung |
|---|---|---|
| < 30 | – (nichts erforderlich) | nachleuchtende Orientierungshilfen |
| 30 – 100 | nachleuchtende Orientierungshilfen | Sicherheitsleuchten |
| > 100 – 1 600 | nachleuchtende Orientierungshilfen und/oder Sicherheitsleuchten ᵃ | Sicherheitsleuchten |
| > 1 600 | Sicherheitsleuchten | Sicherheitsleuchten |

Fußnote ᵃ (in der Tabelle selbst): ob Orientierungshilfen oder Sicherheitsleuchten,
entscheidet die örtliche Gefahrenbeurteilung im Einzelfall — **im Zweifelsfall
Sicherheitsleuchten**.

Lesart der Matrix: zwei Achsen — **Raumfläche** (4 Stufen: 30 / 100 / 1 600 m²) ×
**natürliche Belichtung ja/nein**. Ohne Tageslicht ist ab 30 m² immer aktive
Sicherheitsbeleuchtung nötig; mit Tageslicht erst ab > 1 600 m² zwingend.

### Tabelle 2 (S.5) — Intervalle und Umfang für Prüfungen und Wartungen (visuell geprüft)
Zwei Spalten (Prüfintervall | Prüf- und Wartungstätigkeit), zwei Intervall-Zeilen, wobei
„Jährlich" **zwei** Tätigkeitszellen hat:
- **Jährlich:** (a) Überprüfung der ausreichenden Batteriekapazität (z. B. Entladung mit
  allen angeschlossenen Verbrauchern); (b) manuelle Prüfung der Anlagenfunktion durch
  Unterbrechung der Netzzuleitung (auch bei automatischem Prüfsystem);
- **Monatlich:** manuelle Funktionsprüfung der Leuchten bei Anlagen **ohne**
  automatisches Prüfsystem.

(Kein Entscheidungsbaum-Diagramm in der E-08 — die einzigen Grafikelemente sind Bild 1
und die zwei Tabellen.)

### Sonstige planungsrelevante E-08-Zahlen (Text, beim Sichten verifiziert)
- 5 s → 50 %, 60 s → 100 % der Mindestbeleuchtungsstärke; Bemessungsbetriebsdauer ≥ 60 min.
- Mindestbeleuchtungsstärke Fluchtweg „in der Regel 1 lx"; von **jedem Ort im gesamten
  Fluchtwegverlauf** muss mindestens ein be-/hinterleuchtetes Sicherheitszeichen erkennbar
  sein (Positionierungsregel!).
- > 20 Sicherheitsleuchten je zusammenhängendem Gebäudeteil ⇒ automatische Prüfeinrichtung
  gemäß ÖVE/ÖNORM EN 62034.
- LPS-/CPS-Systeme: Leuchten in Fluchtwegen **alternierend auf ≥ 2 Stromkreise**,
  max. 20 Leuchten je Endstromkreis (Verkabelungs-Constraint für den Sicherheitskreis).
- Besondere Gefährdung: Beleuchtungsstärke dauernd vorhanden oder in 0,5 s; ≥ 10 % der
  Allgemeinbeleuchtung, mindestens 15 lx.

## Konzept-Lehren für die Engine

1. **Taxonomie zuerst, Geometrie danach.** Bild 1 (EN) definiert den Entscheidungsraum:
   Jede Fläche des RaumModells wird zuerst klassifiziert (Rettungsweg-Segment /
   Antipanik-Kernbereich / Arbeitsplatz mit besonderer Gefährdung), erst danach greifen
   die je Kategorie unterschiedlichen Lux-, Gleichmäßigkeits- und Blendregeln.
   Rettungszeichen sind ein Unterast der Rettungsweg-Kategorie, keine Parallelwelt.

2. **Die Norm denkt Ausleuchtung als Linien- und Streifengeometrie, nicht als Fläche.**
   Der Rettungsweg wird auf seine **Mittellinie** reduziert (≥ 1 lx entlang der Linie,
   U ≥ 1:40) plus einen **zentrierten Streifen** halber Wegbreite (≥ 0,5 lx); breite Wege
   werden in **2-m-Streifen zerlegt** oder als Antipanik-Fläche (0,5 lx im Kernbereich,
   0,5-m-Randzone ausgenommen) behandelt. Ein Platzierungsalgorithmus arbeitet also auf
   der Wegachse (Polyline aus dem RaumModell) und prüft Lux-Profile entlang dieser Achse —
   das Messraster liegt am Boden (Messung bis 20 mm darüber zulässig, Anhang A.2).

3. **Blendung ist eine Winkelzonen-Prüfung mit Topologie-Schalter.** Bilder 2/3 (EN)
   zeigen: horizontale Wege ⇒ I_max-Begrenzung nur im Kegelband **60°–90° gegen die
   Leuchten-Vertikale** (alle Azimute); Wege mit Niveauänderung und alle sonstigen
   Flächen ⇒ Begrenzung **in allen Winkeln** (Vollkugel). Grenzwert-Zeile wählt die
   Montagehöhe (Tabelle 1; Arbeitsplatz-Spalte = 2× Rettungsweg-Spalte). Das RaumModell
   muss pro Wegsegment „horizontal vs. niveauändernd" kennen.

4. **Sichtbarkeit ist ein Radius-Deckungsproblem.** Bild 4 (EN) + E-08 („von jedem Ort
   erkennbar"): jedes RZ deckt einen Kreis l = z·h (z = 100 beleuchtet / 200
   hinterleuchtet, h = Panelhöhe); der komplette Fluchtwegverlauf muss von diesen
   Kreisen (mit Sichtlinien-Check und ≤ 20°-Höhenwinkel) überdeckt sein. Kein direkter
   Sichtkontakt zum Notausgang ⇒ zusätzliche Richtungszeichen einketten (4.1.1).

5. **Punkte vor Flächen: die „hervorzuhebenden Stellen" sind die primären Anker.**
   4.1.2 a)–k) + E-08 Abschn. 4 liefern die Pflicht-Positionen (Ausgangstüren, Treppen,
   Niveau-/Richtungsänderungen, Kreuzungen, letzter Ausgang + Bereich außerhalb bis zum
   sicheren Bereich, Erste-Hilfe-/Brandmelde-Stellen mit 5 lx vertikal). „Nahe" = ≤ 2 m
   horizontal; bei Richtungsänderung/Kreuzung muss die Leuchte **beide** Richtungen
   ausleuchten. Algorithmus: erst Pflichtpunkte besetzen, dann Lücken entlang der
   Mittellinie füllen, dann Antipanik-Flächen, dann Blend- und Sichtbarkeits-Checks.

6. **Die E-08-Matrix ist der Einstiegs-Gate je Raum.** Raumfläche × natürliche Belichtung
   entscheidet, ob ein Arbeitsraum überhaupt Sicherheitsleuchten braucht oder
   nachleuchtende Orientierungshilfen genügen (im Zweifel Leuchten). Zusammen mit den
   Wegbudgets (10 m bis zum Fluchtweg, i.d.R. 40 m gesamt) ist das der Vor-Filter, bevor
   die EN-1838-Geometrie überhaupt angewendet wird — und ein klassischer Punkt, den eine
   LB projektspezifisch übersteuern kann.

7. **Elektro-Constraints gehören in den Plan, nicht nur ins Licht.** E-08: alternierende
   Aufteilung der Fluchtweg-Leuchten auf ≥ 2 Stromkreise, ≤ 20 Leuchten je Endstromkreis,
   > 20 Leuchten ⇒ automatisches Prüfsystem. Der Platzierer sollte die Leuchten-Reihenfolge
   entlang des Wegs so ausgeben, dass die Kreis-Zuordnung (A/B/A/B…) ableitbar ist.

## Korrekturen am Text-Digest

1. **Bild-Nummerierung der Lücken:** Die Annahme „Bild 2/3 = Mittellinien-/Streifen-
   Geometrie" trifft nicht zu. In der ÖNORM EN 1838:2019 (Kern 2013 D) sind **Bild 2 und
   Bild 3 die Blendungs-Grafiken** (horizontal vs. andere Rettungswege) und **Bild 4 die
   Erkennungsweite**. Für das Mittellinien-/Streifen-Konzept existiert **kein Bild** —
   es steht nur als Text in 4.2.1 (siehe rekonstruierte Skizze oben). Ein Digest, der
   dafür eine Grafik zitiert, referenziert eine andere Ausgabe (z. B. EN 1838:1999).

2. **Blendungszone präzisiert:** Die 60°–90°-Zone wird **von der Vertikalen durch den
   Lichtpunkt** gemessen (nicht von der Horizontalen) und gilt laut Bild 2 für Wand-
   wie Deckenmontage identisch, für **alle Azimutwinkel**. Bild 3 (Vollkreis um die
   Leuchte) bedeutet: bei nicht-horizontalen Wegen gilt I_max **ohne Winkelfenster** —
   das „60°–90°" darf dort nicht angewendet werden.

3. **Tabelle 1 (EN) visuell bestätigt** — inkl. der Regelmäßigkeit „Arbeitsplatz-Spalte
   = 2 × Rettungsweg-Spalte", die als Plausibilitäts-Check ins Normwissen übernommen
   werden kann.

4. **E-08 Tabelle 1 visuell bestätigt**, mit zwei leicht verlierbaren Details: in der
   Zeile > 100–1 600 m² gilt die Fußnote ᵃ (Einzelfall-Gefahrenbeurteilung, im
   Zweifelsfall Sicherheitsleuchten) **nur für die Tageslicht-Spalte**; die Zeile < 30 m²
   verlangt mit Tageslicht **gar nichts** („–"), ohne Tageslicht nachleuchtende
   Orientierungshilfen.

5. **E-08 Bild 1 Maße:** „max. 10 m" bezieht sich auf den Verkehrsweg-Vorlauf bis zum
   Erreichen eines Fluchtwegs; „i.d.R. max. 40 m" auf den Fluchtweg-Verlauf bis
   Endausgang/sicheres Freie — mit expliziter Anmerkung, dass die Fluchtweglänge gemäß
   OIB-Richtlinie oder Brandschutzkonzept auch länger sein kann (also LB-/projekt-
   übersteuerbar, kein Hard Stop).
