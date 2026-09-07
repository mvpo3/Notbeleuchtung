# Offene Fragen — Plan-Befunde & Regel-Lücken

Sammelstelle für Befunde, die eine Owner-Entscheidung brauchen. Regel-Lücken
je Raumtyp stehen maschinenlesbar in `normwissen/data/regel_deckung.yaml`
(`offen:`-Einträge, Guard `tests/naht/test_regel_deckung.py`).

## Barawitzka EG — keine expliziten Fluchtweg-Linien (2026-09)

Korrektur einer früheren Annahme: die 16 Farbe-96-Linien im Plan sind
**Katastergrenzen** (Layer »Kataster Grenzen«), keine FLW-Linien; Farbe 30 ist
ein Wand-/Bau-Layer, keine Brandabschnittslinie; kein BST/T30-Text. Brandschutz
real vorhanden: Layer »0._EG PP_2_970 Brandschutz« (Messlinien Farbe 16 mit
Distanz-Texten) + 6× »Glaswand EI30 + A2«-Texte (Layer 870).

Folgen:
- Die Soll-Erwartung »≥16 Segmente quelle LINIE« ist mit diesem Plan **nicht
  erfüllbar** — `tests/naht/test_soll_barawitzka.py` bleibt xfail und
  dokumentiert das.
- Die Quelle »explizite FLW-Linie« wird trotzdem **generisch** gebaut:
  Layer-Muster FLW/09-WEG + `materialien.yaml`-Semantik FLUCHTWEG + Farbe 96
  NUR wenn der Layername nicht Kataster/Grenze/verm enthält.

## Rennweg — Erkennungs-Lücken (2026-09)

- Lift OG3: kein X-Rechteck, nur MTEXT »AUFZUG 8 PERS. …« → Lift-Erkennung
  muss textbasiert + nächstes geschlossenes Rechteck 1.0-2.8 m funktionieren.
- Stufenlinien-Abstand OG3 gemessen 186-227 mm — Toleranz der
  Stiegen-Erkennung (150-350 mm) beachten.
- EG: Hauseingang ist KEIN Türblock in der Straßenfassade (nur
  »TÜRSCHLIESSER«-MTEXT); zweiter Plan-Cluster im selben Modelspace.

## Mollgasse — LIFT-Block (2026-09)

LIFT-Block 1.65×1.90 m mit **Achsenkreuz** (Mittellinien) statt X-Diagonalen;
Lift-Erkennung muss Achsenkreuz UND Diagonalen akzeptieren + Blockname »LIFT«.

## Fachteil 1 — konservative Entscheidungen (2026-09, Selman)

- **Fenstertür im EG:** Eine Fassadentür AUSSEN×WOHNUNG_PRIVAT ist immer
  `balkontuer` (nie Ausgang) — auch im EG, wo eine Fenstertür faktisch ins
  Freie führt. Ob EG-Fenstertüren als Notausgang zählen dürfen, ist eine
  Norm-Frage (Owner Enis); bis dahin konservativ KEIN Ausgang.
- **stair_exit nur aus `stiegenhaustuer`/`brandschutztuer`:** Wohnungseingänge
  direkt ins Stiegenhaus (Rennweg-T7-Muster) erzeugen KEINEN Geschossausgang —
  sonst produziert jede Wohnungstür einen Pfeil (Mollgasse: 10 statt 3).
  Sie sind Startpunkte des Fluchtwegs (quelle GRAPH).
- **`tuer_detail`-Kette (ein Feld im Contract):** STIEGENHAUS×PRIVAT →
  `wohnungseingang` (die Startseite gewinnt); die Stiegenhaus-Seite
  rekonstruiert `ausgaenge.py` aus den Raum-Seiten. `brandschutztuer` nur für
  sonst untypisierte Türen — ein spezifischeres Detail bleibt stehen, der
  Brandschutz-Hinweis geht dann nicht in den Contract (Feld fehlt; bei Bedarf
  Contract-Vorschlag »brandschutz: bool« an alle 3 Owner).
- **Brandabschnitts-LINIEN kreuzen:** kein Producer für Brandabschnittslinien
  im Repo — Brandschutz-Typisierung nutzt heute nur BST/T30/T90/EI30/EI90-
  Texte in 500 mm Umkreis.
- **Durchgänge ohne Türblatt:** Kontaktzone zweier Raumpolygone minus
  Wandkörper, > 800 mm, keine bekannte Tür in 600 mm — kann auf lückigen
  Wandkörpern übererkennen (Mollgasse: +78 Durchgänge); Öffnungen tragen
  `ohne_tuerblatt=True` und sind darüber filterbar.

## Fachteil 2 — Lift/Stiegenhaus/Anker (2026-09, Selman)

- **AUFZUGSVORPLATZ wird nicht automatisch typisiert:** ein Vorplatz zählt nur
  als eigener Raum, wenn der Plan ihn als solchen abgrenzt (eigener Raum vor
  der Lifttür). Automatisch ist die Lifttür heute nicht erkennbar (kein
  Türblock am Schacht in den Realplänen) — die Fläche bleibt Teil des
  Stiegenhauses.
- **Marker-Evidenz (X/Achsenkreuz) nur in der Erschließung:** Betten, Möbel
  und Waschmaschinen tragen dieselben Diagonalen/Kreuze (Barawitzka-Befund:
  9 Fehltreffer in Küche/Bad/Waschküche/Terrasse). `lift_erkennung` wertet
  X/Achsenkreuz deshalb nur, wenn das Rechteck in STIEGENHAUS/GANG liegt;
  Text- und Blockname-Evidenz gilt überall. Markierte Schächte im Liftmaß
  typen dann als LIFT — gleichwertig `KEIN_RAUM`/Verbotszone; ein eigener
  SCHACHT-Typ wäre ein Vokabular-Vorschlag an alle 3 Owner.
- **Laufrichtung ohne Nummern/Gehlinie bleibt `unbekannt`:** kein Norm- oder
  Geometrie-Kriterium erfunden; Rennweg liefert Nummern 1..20, Mollgasse die
  Gehlinie — sonst trägt der Lauf `richtung='unbekannt'` und
  `fluchtrichtung_grad=None`.
- **Verbotszonen-Konsum in der Platzierung fehlt:** die Platzierung liest
  `stiegenhaeuser[].verbotszonen_mm` noch nicht. Mollgasse EG ist nach dem
  Liftschacht-Ausstanzen trotzdem sauber (0 Leuchten im Liftpolygon, scharfer
  Test) — der generische Konsum (auch Laufflächen) bleibt Leonis, Fachteil 3.

## Fachteil 3 — Prüfstrecken-Befunde 05/06 (2026-09, Selman)

Quelle: `scripts/plan_pruefen.py` (05_fluchtweg.png / 06_platzierung.png +
bericht.md-Fachteil-3-Block). Alles hier ist MESSUNG/BERICHT — die
Platzierungslogik wurde nicht geändert (Owner-Grenze, ADR-0006).

- **Leuchten auf Treppenlauf/Verbotszone:** Barawitzka 4, Mollgasse 7 — Folge
  des offenen Verbotszonen-Konsums (s. Fachteil-2-Eintrag oben). Als BEFUND in
  bericht.md ausgewiesen, Konsum bleibt Leonis.
- **Leuchten in WOHNUNG_PRIVAT (Mollgasse: 4):** vier Leuchten liegen in
  Räumen, die die Wohnungsbildung als privat markiert. Entweder
  Erkennungs-Frage (Raum fälschlich privat, z.B. entlang der 09-WEG-Linien)
  oder fehlender `nutzungsklasse`-Konsum der Platzierung — zur Klärung mit
  Leonis; hier nur BEFUND.
- **RZ-Rotation vs. Türwandwinkel:** gemessen ±2° gegen das nächste
  Wandsegment. Mollgasse 4/8 abweichend (Δ≈90°: rotation_deg=0 an Türen in
  vertikaler Wand), Barawitzka 1/1 abweichend. Nach ADR-0006 ist rotation_deg
  der RZ heute reine CAD-Symbol-Rotation — die Messung dokumentiert die Lücke,
  ändert aber nichts.
- **Leuchten „kein Raum"** (Rennweg 1, Mollgasse 6, Barawitzka 1): Leuchten
  außerhalb jedes erkannten Raumpolygons (Außenleuchten an final_exits und
  Zonen ohne Raum-Polygon) — erwartbar, kein Fehler.
- **Mollgasse Stiegenhaus-Verbotszonen übergroß (Sichtbefund 06):** einzelne
  Treppenlauf-Hüllen im Südost-Teil (Garagen-/Rampenbereich) spannen
  Riesen-Dreiecke auf — Stufen-Gruppierung fasst dort entfernte parallele
  Linien zusammen. Erkennungs-Verbesserung (Distanz-Deckel je Lauf-Hülle)
  als eigener Schritt, NICHT in Fachteil 3 gefixt.

## Rotationsfix + neue Familien (2026-09-07)

- **RZ-Rotation vs. Türwandwinkel — GEFIXT (Wurzel-Bug):**
  `bausteine.richtung_und_rotation` schrieb den Lauf-Azimut PUR als
  `rotation_deg`; der unten-Pfeilblock zeigt bei rot=0 aber nach −Y →
  jeder is_directional=False-Pfad drehte 90° falsch. Jetzt einheitlich
  rotation = (Azimut+90) % 360 (oben→180, rechts→90, links→270, unten→0;
  Guard `tests/platzierung/test_rotation_konvention.py`). Mollgasse-Messung
  4/8 → 1/8 abweichend. Restfall **durchgang_74**: Kreuzungs-RZ in
  graph-getrennter Komponente an der Nordgrenze — Pfeil zeigt längs der
  Wand zum nächsten Ausgang statt durch den Durchgang. Owner-Frage
  (Leonis): sollen auch Nicht-Ausgangs-Anker ≤1 m an einer Tür die
  Tür-Regel (Pfeil durch die Öffnung) bekommen?
- **Mollgasse Nord-Durchgänge ohne Ausgang:** die Durchgänge zur nördl.
  Grundstücksgrenze (durchgang_74/15, y≈1549) sind laut Außen-Analyse ein
  Weg ins Freie, der Provider liefert dort aber keinen final_exit — die
  RZ-Richtungen in der Nordzone routen deshalb südwärts. Selman-Frage.
- **Muthgasse E2 erschlossen, Stempel↔Raum-Lücke:** 98/98 Stempel mit
  Fläche+Typ, aber nur 34/114 Räume typisiert — die A-AREA-BNDY-Polygone
  matchen die Stempel noch nicht flächendeckend
  (xfail `tests/naht/test_soll_muthgasse.py`). 0 final_exit auf E2
  (unterstes Geschoss im Ordner — Klärung, wo der Endausgang liegt).
- **Referenzvergleich Barawitzka (07_referenzvergleich.png):** Treffer-
  Definition ≤1 m + Rotations-Δ ≤10° (Panel-Achse mod 180); Zielbild ≥80 %
  als strict-xfail in `tests/naht/test_soll_referenzvergleich.py` —
  Ist-Quote siehe bericht.md/VERLAUF.

## Fachliche Umsetzung Außen/Türquellen/Kreuzcheck (2026-09-07)

- **AUSSEN_GESCHLOSSEN (Frage an Enis):** ein Hof MIT Außenanlagen-Indiz,
  aber OHNE Weg ins Freie (alle Lücken ≤ 2.4 m, vom morphologischen
  Schließen versiegelt) wird als `AUSSEN_GESCHLOSSEN` klassifiziert
  (`raumerkennung/aussenbereich.py`): Türen dorthin werden NICHT AUSSEN,
  es entsteht kein final_exit. Ist das normseitig richtig — oder braucht
  ein geschlossener Hof eine eigene Behandlung (Sammelfläche, Antipanik)?
- **Mollgasse Nord-Durchgänge — teilbeantwortet:** der Hof samt Wegen ist
  jetzt AUSSEN; die Hoftüren Cluster A (Innenhof-Osttrakt) und Cluster B
  (Südgarten) liefern final_exits (Ist EG: 10 final_exit, alle mit
  `Tuer.quelle`-Begründung). Die Durchgänge an der nördl. Grundstücks-
  grenze selbst tragen weiter keinen final_exit — der Kreuzcheck listet
  sie als notausgang_kandidat (Prüf-Output).
- **Kreuzcheck-Endpunkt-Dedup (offen):** der 09-WEG-Layer zeichnet viele
  Doppellinien-Stummel; von 43 Grad-1-Endpunkten an der Gebäudekante sind
  nur 3 durch final_exits gedeckt → 40 Kandidaten (viele davon Paare
  ≤ 0.2 m). Ein Clustering der Endpunkte (z.B. 500 mm) würde die Liste
  ehrlicher machen — bewusst nicht mehr in diesem Schnitt.
- **Türen-Typisierungsquote:** Soll ≥ 90 % je Familie als strict-xfail in
  tests/naht/ verankert. Ist 2026-09-07: Mollgasse 48 %, Barawitzka 53 %,
  Rennweg EG 54 % — Hauptgrund `unbekannte_kombination` (Nachbarräume ohne
  Kanon-Typ); Gründe-Tabelle je Plan in bericht.md
  (`Tuer.untypisiert_grund`, Contract v1.3.0).
- **Restweg im EG:** bericht.md nennt für OG-Pläne den Restweg
  Stiegenhaustür→final_exit aus dem EG-Plan derselben Familie in
  Projekte/_eingang (Rennweg_EG.dxf neu aufgenommen), sonst „unbekannt".
- **RZ an neu erkannten Notausgängen (Frage an Leonis):** Barawitzka EG hat
  seit der Außen-Analyse 2 Notausgänge; die Platzierung deckt nur einen →
  Prüfregel »Rettungszeichen an Notausgängen (EN 1838 §4.1.2 g)« steht auf
  Warnung (1/2 ohne RZ in Reichweite; gepinnt in
  tests/e2e/test_familien_durchstich.py). Soll die Ausgangs-Priorität auch
  Ausgänge in graph-getrennten Komponenten mit einem RZ versorgen?
