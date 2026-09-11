# Offene Fragen — Plan-Befunde & Regel-Lücken

Sammelstelle für Befunde, die eine Owner-Entscheidung brauchen. Regel-Lücken
je Raumtyp stehen maschinenlesbar in `normwissen/data/regel_deckung.yaml`
(`offen:`-Einträge, Guard `tests/naht/test_regel_deckung.py`).

## Lichtberechnungs-Analyse — zwei Nähte (2026-09-08)

Aus den echten Profi-Notberechnungen (Doku:
`knowledge/extracted/LICHTBERECHNUNG_REFERENZ.md`):

- **@polatselman — Aichholzgasse = Architektur-Testfamilie, kein Notplan.** Die
  PDFs in `DIN-Notbeleuchtungspläne(Beispiele)/Aichholzgasse/` + `Projekte/
  Aichholzgasse/` sind **Architektur-Polierpläne** (HOT ARCHITEKTUR ZT, „POLIERPLAN
  GRUNDRISS", rein bauliche Legende, null RZ-Symbolik) — Wien Wohnbau **GK5**,
  Geschosse **2UG..2DG**. Der Ordnername ist irreführend. Kandidat als neue
  Architektur-Input-Testfamilie (RaumModell). Die zugehörige Notbeleuchtung liegt in
  `Lichtberechnung/Lichtberechnung.pdf` (Relux, Schrack).
- **@EnisAMG — Wartungsfaktor als Norm-Wert.** Beide Büros rechnen den Nachweis mit
  **MF 0,80 innen / 0,57 außen** (INOTEC-Handbuch-Digest nennt 0,8 → 1,25 lx bereits
  als Referenz-Praxis). Leonis baut den **Anwendungs-Mechanismus** in `platzierung/
  lux.py`+`deckung.py` (inert, Default 1,0), konsumiert defensiv `NormAnforderung.
  wartungsfaktor`. **Bitte Feld `wartungsfaktor` auf `NormAnforderung` + Werte in
  `en1838_grundwerte.yaml`** (3-Owner, Contract-Version-Bump). Aktivierung kippt die
  E2E-Bänder (dichtere Platzierung) → erst mit Owner-GO.

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
  Wandsegment. Stand der aktuellen Berichte („Rotationsprüfung RZ über Tür"):
  Mollgasse **1/8** abweichend (`tuer_70`, Δ=90°), Barawitzka **2/2** abweichend
  (`aussenoeffnung_1`, `durchgang_63`, je Δ=90°), Rennweg OG3 kein RZ näher als
  1 m an einer Tür. Die Mollgasse-Zahl ist der Stand nach dem Rotationsfix
  (s.u.). Nach ADR-0006 ist rotation_deg der RZ heute reine CAD-Symbol-
  Rotation — die Messung dokumentiert die Lücke, ändert aber nichts.
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
  tests/naht/ verankert. Ist 2026-09-07: Mollgasse 48 % (72/150),
  Barawitzka 55 % (59/108), Rennweg EG 54 % — Hauptgrund `unbekannte_kombination` (Nachbarräume ohne
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

## Mollgasse — Gebäude schließt nicht: 960 m² Inneres gelten als AUSSEN (2026-09-07, Selman)

**Befund (gemessen, nicht geschätzt).** Die Erklärung „Doppellinien-Stummel +
fehlende Endpunkt-Dedup" für die 40 notausgang_kandidaten oben greift zu kurz.
Ursache ist eine Stufe früher, in der Wandkörper-Erkennung:

| Messgröße | Mollgasse EG | Barawitzka EG |
|---|--:|--:|
| Wandkörper (`finde_wandkoerper`) | 171 | 1243 |
| Segmente auf den Wand-Layern | 989 | — |
| Gebäude-Komponenten | 5 | 1 |
| größte Komponente (m²) | 364.6 | 426.0 |
| als AUSSEN „offen" erkannt (m²) | **960.3** + 7 weitere | 76.1 + 4 weitere |
| `gedeckt()` gesamt (m²) | 497.4 | 413.5 |

**Ursachenkette.** `finde_wandkoerper` (wandkoerper.py) baut Wandkörper aus
HATCH-Flächen. Bei Mollgasse liegen die Wand-*Umrisse* aber als LINE/LWPOLYLINE
auf `02-TWA-`/`02-WDA-`/`02-ZWA-…` (989 Segmente); nur die Material-Schraffuren
(`02-FIL-…-GK`/`-STB`/`-ORANGE`) werden zu Körpern. Der vorhandene
Doppellinien-Fallback `_doppellinien` steht hinter der Bedingung
`if len(out) < 5:` — Mollgasse liefert 171 Hatch-Körper, also läuft er **nie**,
und die 989 Wandsegmente bleiben ungenutzt. Folge: die Wand-Union schließt sich
nicht zu einem Trakt, `erkenne_aussenbereiche` findet 5 Mini-Komponenten, und
die verbleibende freie Fläche (960 m²) berührt den Rand der konvexen Hülle →
sie wird als offener AUSSEN-Bereich klassifiziert.

**Beleg für die Fehlklassifikation.** 20 der 64 erkannten Mollgasse-Räume liegen
mehrheitlich in dieser 960-m²-Fläche, darunter `raum_2`/`raum_3`/`raum_4`/
`raum_7`/`raum_41`/`raum_56` (Typ GANG) und neun Räume vom Typ ZIMMER, sieben
davon zu 100 %. Gänge und Zimmer sind nie Außenbereich.

**Warum das die 40 Kandidaten erklärt.** Weil das Gebäudeinnere als AUSSEN gilt,
liegen viele Grad-1-Endpunkte des 09-WEG-Layers „außerhalb der Kontur, nahe
einer Komponentenkante" und zählen als Außenkanten-Endpunkte. Gleichzeitig gibt
es dort keine Tür mit AUSSEN-Seite → **alle 40 Kandidaten** melden „keine Öffnung
in der Außenwand ≤ 3 m gefunden". Leonis' Einschätzung (real fehlen 1–2
Endausgänge) ist plausibel; der Kreuzcheck überzeichnet um Faktor ~20.

**Warum hier kein Fix steht.** Drei Varianten gemessen, jede verschlechtert
Barawitzka:

1. `_doppellinien` zusätzlich laufen lassen (+883 Körper, 0.2 s): Mollgasse
   `gedeckt()` 497 → 585 m², AUSSEN bleibt bei 936 m². Löst es nicht.
2. Alle Innenraum-Polygone (Nutzungsklasse ≠ AUSSEN) aus der freien Fläche
   schneiden: Mollgasse 960 → 522 m², aber Barawitzka verliert seinen
   AUSSEN_GESCHLOSSEN-Hof (23.5 m² → 0) und `test_aussenbereich.py` bricht.
3. Wie 2, aber nur positiv typisierte Räume: Mollgasse 960 → 622 m², Barawitzka
   Hof weiterhin verloren (23.5 → 0, wird fälschlich „offen").

Ein tragfähiger Fix muss an der Wandkörper-Erkennung ansetzen (Umriss-Linien der
Wand-Layer gleichrangig zu Schraffuren auswerten), nicht an der Außen-Analyse.
Das ist genau die „nächste Baustelle der Raumerkennung", die Leonis' Punkt 5
benennt — sie ist auch der dominante Grund für die niedrige Türquote
(`unbekannte_kombination`: Mollgasse 57/78 der untypisierten Türen).

**Reproduktion.** `finde_wandkoerper` + `erkenne_aussenbereiche` auf
`Projekte/_eingang/Mollgasse_EG.dxf` und `…/Barawitzka_EG.dxf`, Flächen der
`komponenten`/`offen`/`geschlossen` vergleichen; Räume gegen die größte
`offen`-Fläche schneiden.

## Owner-Entscheidung: „ins Freie" heißt über die Grundstücksgrenze (2026-09-07, Selman)

**Entscheidung (gesetzt, ersetzt die frühere offene Frage an Enis):**
Jedes Projekt hat einen **Flächengrundriss bis zur Grundstücksgrenze**; der
umfasst nicht nur die bebaute Fläche, sondern auch Garten, Innenhof und
Vorplatz. „Ins Freie" heißt: aus diesem Flächengrundriss **heraus** auf
öffentlichen Grund. Ein Innenhof, der zwei Stiegenhäuser verbindet, damit man
zwischen den Stiegen pendeln kann, aber ringsum von Mauern geschlossen ist und
keinen Weg auf die Straße hat, ist **kein final_exit** — der Fluchtweg muss von
dort weitergehen.

**Was daran vorher falsch war (gemessen).** `erkenne_aussenbereiche` nahm die
**konvexe Hülle der Gebäudekomponenten** als äußere Grenze und stufte jede
freie Fläche, die deren Rand berührt, als offen (= AUSSEN) ein. Zwei belegte
Folgefehler:

- **Barawitzka EG:** die Freiflächen 89.7 m² und 76.1 m² hängen über eine
  0.05-m-Engstelle zusammen und bilden **einen Hof von 190.2 m², der beide
  Stiegenhäuser verbindet** (raum_35 und raum_37, je Abstand 0.00 m). Seine
  Randlänge an der Straßenkante ist **0.0 m** — er ist der von Selman
  beschriebene Fall. Trotzdem galt er als offen, und
  `exit_durchgang_62` (8.78, −22.66) wurde als final_exit ausgegeben.
- **Mollgasse EG:** die konvexe Hülle (1804.5 m²) ist **größer** als das
  Grundstück (1510.2 m²) und ragt mit 405.3 m² auf öffentlichen Grund.

**Neue Regel.** Bezugspolygon ist die Grundstücksgrenze, nicht die Hülle; und
eine freie Fläche ist nur dann offen, wenn sie die **Straßenkante** der Grenze
erreicht (Engstellen-Test gegen Zeichnungs-Splitter: `buffer(-400).buffer(420)`).

| Plan | Grundstücksgrenze | offen (m²) alt → neu | geschlossen (m²) alt → neu |
|---|--:|---|---|
| Barawitzka_EG | 616.8 | [9.3, 9.7, 12.5, 76.1, 89.7] → **[12.5]** | [23.5] → **[23.5, 190.2]** |
| Mollgasse_EG | 1510.2 | [13.2 … 960.3] → **[910.1]** | [] → **[73.0]** |
| Rennweg_EG | — | [] → [] (Fallback) | [] → [] |
| Rennweg_OG3 | — | unverändert (Fallback) | unverändert |
| Muthgasse_E2 | — | unverändert (Fallback) | unverändert |

Barawitzka liefert danach **1 final_exit** (`exit_tuer_27`, an der Straße)
statt 2; Mollgasse **9** statt 10, beide Hofausgangs-Cluster erhalten.

**Zweiter, unabhängiger Codepfad — wichtig für Nachfolger.** Der
Außenbereichs-Fix allein reichte NICHT. `tuer_typisierung` Regel 1
(`AUSSEN × ALLGEMEIN_ERSCHLIESSUNG → hauseingang`) bezieht ihr AUSSEN aus
`nutzungsklasse.py` (`TERRASSE → AUSSEN`), nicht aus `aussenbereich`. Die Tür
STIEGENHAUS raum_37 → TERRASSE raum_43 (im ummauerten Hof) wurde dadurch
`hauseingang` und über `ausgaenge.py` zum final_exit, an der Außen-Analyse
vorbei. Deshalb der Guard `kein_weg_ins_freie` in `typisiere_tueren`.

### Offene Schwächen dieser Regel (bewusst benannt)

- **Nur 2 von 5 Plänen tragen eine Grundstücksgrenze** (Barawitzka als 16
  Linien mit Lücken an 7 Grenzpunkt-Markern, Brückung < 400 mm nötig;
  Mollgasse als geschlossene Polylinie). Rennweg EG hat keine, Rennweg OG3 nur
  Bemaßung auf dem gleichnamigen Layer (deshalb ist der **Entity-Typ-Filter
  Pflicht**, sonst Falschpositiv), Muthgasse nur INSERTs. Dort greift weiter
  der Hüllen-Fallback samt seinem bekannten Fehler.
- **Die Straßenkante hängt an Layer-Namen** (GEHSTEIG|GEHWEG|RANDSTEIN|
  BORDSTEIN). `STRA.ENVERKEHR` darf **nicht** hinein: der Layer
  »Straßenverkehr_Situationslinie.verm« läuft bei Barawitzka auch an der
  Südgrenze und würde den Hof wieder öffnen. Ein Plan mit Hof, aber ohne
  Gehsteig-Layer, ist im Repo nicht vorhanden und damit ungetestet.
- `_STRASSE_NAH_MM = 3000` und die Brückung `400 mm` sind an genau zwei
  Plänen kalibriert.

## Überdachung vor dem Haupteingang — Erkennung steht auf einem einzigen Beleg

Selman (2026-09-07): vor Haupteingang und Hauptausgang ist zu wissen, ob eine
Überdachung vorliegt, weil dort Notbeleuchtung bzw. Aufheller platziert werden.

**Datenlage, gemessen: dünn.** Kein Plan trägt Layer, Block oder Text
VORDACH|ÜBERDACHUNG|AUSKRAGUNG|LAUBENGANG|ARKADE|PERGOLA|CANOPY — geprüft über
129/90/67/66/55 Layer, alle Blockdefinitionen und alle Texte. Namensbasierte
Erkennung ist tot. Einziges Signal ist ein **nicht flächendeckender**
Decken-Layer, geschnitten mit den offenen Außenflächen.

Ist-Ergebnis: **Barawitzka 1 Überdachung, 0.707 m², 2.22 m vor
`exit_tuer_27`.** Mollgasse, Muthgasse, Rennweg: keine.

Zwei Schwächen, beide Owner-Entscheidungen wert:
1. Der Flächendeckungs-Filter (`_DECKE_MAX_ANTEIL = 0.9`) greift bei
   Barawitzka mit **0.865** nur knapp — die Regel steht auf 3.5
   Prozentpunkten. Ein engerer Decken-Regex (nur »210 Decke« statt auch
   »Deckendurchbruchsymbol«/»Dachaufbau«) verschiebt den Anteil deutlich.
2. `_MIN_UEBERDACHUNG_M2` steht auf **0.5**, weil das einzige real gemessene
   Vordach 0.707 m² misst; bei 1.0 m² fiele genau der Fall weg, für den die
   Erkennung gebaut ist. Kalibriert an EINEM Plan.

**Bewusst kein Contract-Feld.** Ein `Ausgang.ueberdacht: bool` wäre die
natürliche Naht zu Leonis' Aufheller-Platzierung, bräuchte aber
3-Owner-Approval. Auf Basis eines einzigen Plans und eines 0.7-m²-Stücks ist
das zu früh. Die Erkennung liegt deshalb als reiner Prüfstrecken-Output im
Bericht (Abschnitt „Außenbereich"). Der Antrag geht raus, sobald Leonis den
Aufheller wirklich abhängig davon setzen will.

## Baufeld-Crash: nicht Ausreißer-Extents, sondern falsche mm-Kalibrierung (2026-09-08, Selman)

Leonis meldete am 2026-09-07 (COORDINATION.md): Baufeld-4OG crasht die
Stempel-Flutung mit einem 2,56-TiB-Raster; Hauptinhalt bei y ≈ 3,475e11 mm,
Vermutung „zwei Cluster → ausreißer-robuste Extents nötig".

**Nachgemessen: die Cluster-Hypothese trägt nicht.** Die Wandkörper des 4OG
liegen NICHT in zwei kompakten Haufen, sondern durchgehend über 72–85 km
verteilt. Jede Lückenteilung lässt beide Seiten riesig (größte Lücke in x:
1065 m, teilt 1950/185 Körper — die 1950 spannen dann immer noch 72 460 m).
Ein Cluster-Filter hätte hier nichts gerettet.

**Die Ursache liegt eine Stufe früher, in `dxf_load._calibrate_factor`.**
Der mm-Faktor wird aus `_raw_wall_span` abgeleitet. Diese Funktion sah nur
Modelspace-Entities auf Wand-Layern. Bei Baufeld 1OG/2OG/4OG liegen dort aber
nur INSERTs (die Wand-Linien stecken in der Blockdefinition) → 0 Punkte →
`raw_span = 0` → keine Dekade plausibel → Fallback auf `$INSUNITS`. Das meldet
6 (Meter), obwohl die Zeichnung in mm vorliegt → **Faktor 1000**. Der
Terabyte-Raster ist die Folge, nicht die Ursache.

Messwerte je Geschoss (Faktor vorher → nachher, Wandkörper-Spannweite):

| Geschoss | Faktor alt | Spannweite alt | Faktor neu | Status vorher |
|---|--:|--:|--:|---|
| 1OG | 1000 | 83 310 m | 1 | Absturz (2.60 TiB) |
| 2OG | 1000 | 82 910 m | 1 | Absturz (2.58 TiB) |
| 3OG | 10 | 819 m | 1 | still 10× falsch |
| 4OG | 1000 | 81 911 m | 1 | Absturz (2.56 TiB) |
| 5OG | 1 | 82 m | 1 | ok |
| 6OG | 10 | 819 m | 1 | still 10× falsch |
| EG | 1 | 87 m | 1 | ok |
| UG | 1 | 87 m | 1 | ok |

**Fünf von acht Geschossen waren betroffen, nicht eines** — und die beiden
10×-Fälle sind die unangenehmeren: sie rechneten ohne Absturz mit falschem
Maßstab weiter.

**Fix (zwei Teile):**
1. `_raw_wall_span` steigt jetzt in Blöcke ab (`_wand_punkte`, Tiefe ≤ 3) und
   misst die Spannweite über ein 2–98-%-Perzentil-Fenster statt min/max.
   Damit fallen Plankopf-/Phantom-Punkte heraus (dieselbe Fehlerklasse wie der
   Rennweg-Phantomraum #126). Alle acht Baufeld-Geschosse landen auf Faktor 1
   bei einheitlich 82–91 m Spannweite.
2. `flute_stempel` hat eine Reißleine (`_MAX_RASTER_ZELLEN = 5e8`, ~477 MiB
   bool): unplausible Extents → `RuntimeWarning` + keine gefluteten Räume,
   statt den ganzen Parse zu verlieren. Zum Vergleich: Muthgasse E2, der
   größte Plan im Repo, braucht 4.6e7 Zellen.

**Nachweis, dass die Bestandspläne unberührt bleiben** (die entscheidende
Bedingung, vor der Umsetzung gemessen): Barawitzka 1000, Mollgasse 1000,
Muthgasse 10, Rennweg EG/OG3 je 1 — alle fünf Faktoren identisch zu vorher.
Volle Suite unverändert grün.

**Offen:** Die Baufeld-Pläne liegen nur als `Projekte/Baufeld_E2.zip` im Repo;
`tests/naht/test_soll_baufeld.py` skippt deshalb. Die Messungen oben stammen
aus einer temporären Entpackung außerhalb des Repos. Wer die Familie dauerhaft
in die Prüfstrecke nehmen will, muss die Geschosse nach `Projekte/_eingang/`
legen — dann greifen die Soll-Nahttests wie bei den anderen vier Familien.

## Stempel-Vokabular — Sweep über alle Plan-Familien (2026-09-08, Selman)

Anlass: `KINDERWAGENRAUM` war als Kanon-Typ tot, weil reale Pläne **`KIWA`**
schreiben, nicht „Kinderwagen" (Mollgasse „KIWA" / „FAHRRADRAUM / KIWA",
Barawitzka „Fahrrad+ KiWa"). Behoben. Danach systematischer Sweep: 892 Stempel
aus 11 Plänen plus roher Textdump über alle 60 Projekt-DXF (29 593 Texte).

**Trefferquote `raumtyp_flags`: 217/249 = 87 %** auf den fünf Prüfstrecken-Plänen
(Barawitzka_EG 38/38, Muthgasse_E2 99/99, Rennweg_OG3 10/10, Rennweg_EG 14/19,
Mollgasse_EG 56/83). Alle Fehlschläge liegen in den beiden EG-Plänen; 18 der 32
sind **korrekt** untypisiert (Außenanlagen, Wohnungs-IDs „TOP n", Plankopf).

**Bewusst NICHT aufgenommene Alias-Kandidaten** — jeder erzeugt einen belegten
Fehltreffer, deshalb ist der Status quo besser als die Ergänzung:

- `vp`/`vorplatz` → VORRAUM: die 34 `VP` bei Herrenholzgasse liegen auf demselben
  Layer wie „Vorgarten"/„Vorplatz" (Außenflächen, bis 28 m²), und Herrenholz hat
  pro Reihenhaus schon einen eigenen Stempel „Vorraum". VORRAUM trägt
  `ist_fluchtweg` + `ist_communal` → 40 Außen-Vorplätze würden Fluchtweg-Innenräume.
- `tr` → STIEGENHAUS: die 37 `TR` sind die private Reihenhaus-Innentreppe, kein
  communales Stiegenhaus. STIEGENHAUS wird von `ausgaenge.py` (stair_exit),
  `fluchtweg.py`, `gang_strategy` und `communal_stgh_strategy` konsumiert → 37
  Phantom-Fluchtweg-Anker in einem Plan.
- `er` → KELLER: 2 der 24 Belege sind „ER-GESAMT" (54/108 m²) — Summenzeilen, keine
  Räume; zudem kippt ein bestehender TECHNIK-Stempel auf KELLER, und ausgeschrieben
  liefert „Einlagerungsraum" schon ABSTELLRAUM (zwei Typen für dieselbe Sache).
- `podest` → STIEGENHAUS: die beiden Mollgasse-PODEST sind nicht dasselbe — das
  11,02-m²-Exemplar liegt laut Raster-Umriss AUSSEN am Gebäuderand (Nachbarn WC,
  SR, VORRAUM; nächster STGH-Stempel 9,9 m weg).
- `aufzug` → LIFT: redundant, `lift_erkennung._LIFT_TEXT` greift den Stempel schon —
  und dort ohne das Fluchtweg-Flag, das bei LIFT (Nutzungsklasse KEIN_RAUM) ein
  Widerspruch wäre.
- `wr`, `sr`, `dusche`: mehrdeutig bzw. n=1 ohne zweiten Beleg (`WR` steht im Repo
  für Waschraum, Wechselrichter UND „Wiener Null").

**Offen, echte Kanon-Lücke (3-Owner):** `GESCHÄFTSLOKAL` (4 Vorkommen auf 2 Plänen,
inkl. Tippfehler „GESCHÄFTLOKAL") ist keine Schreibweisen-, sondern eine
Typ-Lücke — eine Verkaufsstätte (OIB RL2 Tab. 6) passt in keine der fünf
`Nutzungsklasse`-Literale. Aufnahme wäre VOKABULAR.md + `raumtyp.py` +
LB-Stützliste + Nutzungsklasse in einem Zug. **Frage an Enis/Leonis:
brauchen wir den Typ, und welche Nutzungsklasse trägt er?**

## Symbol-Library & Photometrie — Nachmessung (2026-09-09)

Aus der ezdxf-Nachmessung der kanonischen Library, der E-Symbole-Nebenvarianten und
der 4 LDT (Doku: `docs/REFERENZ_PLATZIERUNG.md` Abschnitt 4a/4b und 5). Alles
READ-ONLY erhoben, nichts geändert. **Keine Norm-Ableitung von mir.**

- **Lichtstrom-Differenz `antipanik_nlildl423_round.ldt` — welcher Wert gilt für den
  Nachweis?** Beleg: die LDT gibt in Zeile 29 **240 lm**;
  `CAD_Symbole/photometrie/QUELLEN.md` (Abschnitt „In echten Lichtberechnungen
  verwendet") nennt für dieselbe Leuchte **208 lm** (round) bzw. 211 lm (corridor),
  laut QUELLEN.md aus der Relux-Berechnung WHA Aichholzgasse
  (`knowledge/extracted/LICHTBERECHNUNG_REFERENZ.md`), nicht aus der LDT.
  **Owner: Enis (Norm/Nachweis)** — LDT-Wert oder Relux-Wert?
- **`notlicht_kw_garage` — RZ-Symbol mit SL-Optik, Absicht oder Altlast?** Beleg:
  `schrack_symbol_mapping.yaml` mappt den Key auf den Rettungszeichen-Block
  `notbeleuchtung- richtungspfeil nach unten`, `symbols/photometrie_mapping.yaml`
  aber auf `sl_nlkbu433_3h_round.ldt` (Sicherheitsleuchte, Rundlinse).
  **Owner: Symbol-/Produkt-Owner (Leonis, Gegenzeichnung Enis).**
- **`sicherheitsleuchte_spot` ohne LDT — soll er erben?** Beleg: kein Eintrag in
  `photometrie_mapping.yaml` → `photometrie_katalog.ldt_pfad_fuer` liefert `None`,
  der Lux-Nachweis fällt für diesen Key auf die isotrope Annahme zurück; laut
  Mapping-Kommentar ist es zugleich die häufigste SL-Darstellung des
  din-Referenzplans (40× im Barawitzka-Plan). Vorschlag zur Entscheidung:
  `sl_nlkbu433_3h_round.ldt` erben, bis eine STRING-2-LDT beschafft ist.
  **Owner: Enis (Nachweis) + Produkt-Owner (LDT-Beschaffung).**
- **OCS-Extrusion im `nach rechts`-Block — Dauerzustand oder Umbau?** Beleg: die
  HATCH-Entity des Blocks in `CAD_Symbole/Notbeleuchtungssymbole.dxf` trägt
  `extrusion = (0,0,−1)`, die vier Rahmen-LINEs derselben Block-Definition **nicht**.
  Roh (ohne OCS→WCS) gelesen liegt die Pfeilspitze bei x = −5209.7994 relativ zum
  Blockzentrum → Fehlalarm „Block korrupt / zeigt nach links". Über ezdxf/AutoCAD
  funktioniert alles. **Owner: Symbol-Owner (zeichnen/freigeben, ADR-0002).**
- **Verbleib der E-Symbole-Nebenvarianten.** Beleg (gemessen,
  `docs/REFERENZ_PLATZIERUNG.md` 5.1): `E-Symbole-clean.dxf` enthält den Block
  `notbeleuchtung-richtungspfeil nach rechts` in der **korrupten Alt-Fassung**
  (2606.183 × 2300.291 statt 3.134 × 1.567) und es fehlen 5 der 8 gemappten Blöcke;
  `E-Symbole.dxf` fehlen 3; `E-Symbole_recover.dwg` ist mit 1 760 B ein leerer
  Stummel. Keine der Dateien ist als `NOTBELEUCHTUNG_SYMBOL_LIB` brauchbar
  (`load_mapping()` bricht fail-loud). Löschen ist ausgeschlossen (Repo-Regel „nie
  löschen, immer versionieren") — **Vorschlag:** nach `CAD_Symbole/_herkunft/`
  verschieben und in ADR-0002 vermerken. Nicht ausgeführt (READ-ONLY).
  **Owner: Repo-/Symbol-Owner.**
- **Guard für die stillschweigende Kopplung „Tür-Formel (A+90) ⇒ unten-Block"?**
  Beleg: `communal_stgh_strategy.py:106` und `fachpraxis.py:302` rufen
  `_select_key(anf.symbol_katalog_keys, "unten")` und rechnen danach hart mit der
  unten-Block-Formel; `bausteine.select_key` (`bausteine.py:56-64`) fällt auf
  `keys[0]` zurück, wenn kein Key auf `_unten` endet. Heute ist `keys[0]` in
  `normwissen/data/raumtyp_regeln.yaml:44` und `:77` = `notlicht_ks_stiege` (Block
  „nach unten", basis 270), also korrekt — steht dort jemals ein links/rechts-Key
  zuerst, ist der Pfeil 90 bzw. 270 Grad falsch, ohne Test, der das fängt.
  Vorschlag: Assertion `basis_deg(block_name(key)) == 270` an den vier Fundstellen
  **oder** ein Test über `raumtyp_regeln.yaml`. **Owner: `platzierung/` + `tests/`
  (Leonis).**

Zwei weitere Befunde derselben Messung sind gemeldet, aber keine Entscheidung:
die Contract-Semantik `richtung="unten"` bei `rotation_deg != 0` (verlässlich ist nur
`fachpraxis._effektive_richtung_deg`) und das Bankers-Rounding in
`round((deg+90)/90)*90` bei exakt diagonalen Türrichtungen — beides in
`docs/REFERENZ_PLATZIERUNG.md` Abschnitt 4b festgehalten.

## Referenzplan Barawitzka — zweite Sichtung (2026-09-09)

Aus der Nachsichtung des Fachplaner-Plans (Doku: `docs/REFERENZ_PLATZIERUNG.md`
Abschnitt 1a–1d). Messungen mit ezdxf, Engine-Lauf über `build_default_bundle()`.

- **Blatt 2 (Frames F4–F7) hat keine gemessenen Offsets — kalibrieren?** Beleg: die
  4 Frames sind lokalisiert (Fenster-Tabelle in 1a, 14 Leuchten), Kandidaten-DXF sind
  `Projekte/Barawitzkagasse/…_1_5 2 St`, `…_1_6 3 St`, `…_1_7 1 DG`, `…_1_8 2 DG`,
  `…_1_9 DD STG1` — **5 Dateien für 4 Frames**, die Frame-zu-Geschoss-Zuordnung ist
  unbestimmt. **Owner: Auftraggeber der Sichtung** (Aufwand: je Geschoss ~100–200 s
  Parse plus Kalibrierung).
- **Warum liefert `raum.parse` für das KG 0 Anker / 0 Ausgänge / 0 Stiegenhäuser?**
  Beleg: `415_260415_PP_VA_1_2 -1 KG.dxf`, Parse 197 s, 14/17 Referenzpunkte fallen
  trotzdem sauber in erkannte Räume — die Räume stehen also, die Anker fehlen (EG
  liefert 28). Raumerkennungs-Befund, außerhalb des Sichtungs-Auftrags.
  **Owner: `raumerkennung/` (Selman) — soll dem nachgegangen werden?**
- **OG1: zwei Referenzleuchten landen 4.7 / 5.8 m im Nichts.** Beleg: mit Offset
  (−18.34, −38.66) liegen RZ_PL Typ B (4.10, −21.30) und RZ_PLPR Typ E
  (10.28, −21.06) außerhalb jedes erkannten Raums, während die 3 Kit-Leuchten auf
  0.17–0.50 m sitzen; das „1 St"-DXF ist 186 m breit (EG 80 m). **Hypothese, nicht
  verifiziert:** der Frame deckt nur den Stiegen-1-Bereich, oder der OG1-Offset ist
  nur lokal am Stiegenhaus kalibriert. **Owner: Auftraggeber der Sichtung.**
- **Zieltest `tests/naht/test_soll_referenzvergleich.py`: Quote je Geschoss oder
  Gesamtquote?** Beleg: bei zusätzlicher UG/OG1-Verdrahtung fällt die Gesamtquote von
  18 % (2/11) auf ~13 % (4/32); Parse-Zeit für 3 Geschosse ~350 s, der Test bräuchte
  eine session-weite bzw. gecachte RaumModell-Fixture. **Owner: `tests/` + Leonis.**
- **Nachvollziehbarkeit der Restfehler-Angaben in `REFERENZ_PLATZIERUNG.md`
  Abschnitt 1.** Die EG-Bestückung (11 Leuchten: 5× A, 3× B, 1× F, 1× H, 1× I) ist
  durch die Nachmessung bestätigt; die Restfehler Ø 0.33 / 0.19 / 0.04 m ließen sich
  **mangels dokumentierter Kalibrier-Punkte nicht nachrechnen**. Vorschlag: die
  verwendeten Punktpaare je Geschoss mitdokumentieren. **Owner: Autor der
  Erstkalibrierung (2026-09-07).**

## Mollgasse-„Laubengänge" — bewusste Grenze: kein lichtes Polygon (2026-09-10, Selman)

Auftrag war zu prüfen, ob sich für Laubengänge (einseitig offen, Begrenzung
durch Geländer/Stützen statt Wand) ein lichtes Polygon bilden lässt, ohne auf
den anderen vier Plänen Phantom-Räume zu erzeugen. **Ergebnis: nein — und es
gibt auf Mollgasse gar keine Laubengänge.** Die 12 nicht messbaren Segmente
bleiben `None` mit Grund; es wurde keine Erkennung gebaut.

Messstand (reproduziert, Cache neu geparst: `parse_s=31.8, raeume=64,
segmente=126`): Barawitzka 12/12 · Mollgasse 107/126 (`flaeche_fehlt` 12,
`nur_tuer_oder_eckpunkte` 7) · Muthgasse 154/155 · Rennweg EG 9/9 · Rennweg
OG3 5/5 → **287/307 = 93.5 %**. Diese Zahlen ändern sich durch die
Entscheidung nicht.

**Was die 12 Mollgasse-Segmente wirklich sind.** Alle 12 haben `quelle=LINIE`
und stammen aus `zirkulation._weg_polylinien` über `WEG_PREFIX=("09-WEG",)` —
dem **Außenanlagen-Layer** `09-WEG_G00-LEG-M0`, nicht aus einer Raumgeometrie:

- **6 entartete Polylinien-Endpunkte:** seg_41 = 0.0 mm, seg_27 = 0.3 mm,
  seg_10 = 20 mm, seg_34 = 50 mm, seg_8 = 68 mm, seg_9 = 105 mm (1–2
  Abtastpunkte). Sie landen nur deshalb im Topf `flaeche_fehlt` statt bei
  `nur_tuer_oder_eckpunkte`, weil die Flächensuche vor der Punktzählung greift.
- **4 Linien = 2 Doppellinien-Paare:** seg_92/seg_94 sind zwei parallele Linien
  im Abstand **50 mm** über 6.2 m, seg_93/seg_95 dasselbe über 0.85 m — je zwei
  Zeichnungslinien derselben Wegkante, nicht zwei Wege.
- **2 echte Außenwege:** seg_4 (7451.5 mm, alle 75 Abtastpunkte außerhalb des
  `footprint.gebaeude_umriss`, 2002 mm von jeder Wand) und seg_7 (1500 mm,
  Außenstummel an einer Wartungstür). seg_34 liegt ebenfalls vollständig
  außerhalb (2287 mm zur nächsten Wand), ist aber mit 50 mm selbst ein Stummel.

Faktisch sind es damit **4 reale Außenwegzüge**, nicht 12 Fehlstellen.

**Darstellungsbefund: Freiraumplanung, keine Laubengänge.** Nächste Texte:
`MAUERSOCKEL + ZAUN, H = 1.00 m` (439 mm), `SANDKISTE 200x200cm`,
`KLETTERPFLANZEN`, `PFLANZTROG, h=40cm` (279 mm), `RIGOL`, `GEFÄLLE 2%`,
`RESTMÜLL 1100 L`. Layergruppe `09-` = Außenanlagen (`09-WEG` 140, `09-NAT`
115, `09-SYM-GEHSTEIG` 6, `09-VER-GRUNDSTÜCKSGRENZE` 1 Entity). Der Plan trägt
weder Layer noch Block noch Text `VORDACH|ÜBERDACHUNG|AUSKRAGUNG|LAUBENGANG|
ARKADE|PERGOLA|CANOPY` — 0 Treffer, deckungsgleich mit dem Befund oben
(»Überdachung vor dem Haupteingang«) und `aussenbereich.py`. Überdacht ist
keines der Segmente (Mollgasse: 0 Überdachungen gemessen).

**Warum kein lichtes Polygon gebildet werden kann** (Senkrecht-Strahlen alle
100 mm, Trefferfenster 300–4000 mm, Deckung + Streuung je Layer und Seite):

| Hypothese | Messergebnis |
|---|---|
| beidseitige durchgehende Begrenzung | seg_4 links bester Layer `02-AXO` **8 %** Deckung; rechts `02-AXO` 100 %, d = 346–369 mm, sd 7 — das ist das **Achsraster**, keine Bauteilkante. seg_92/94 rechts `09-SYM-GEHSTEIG` 100 %, d = 2449–2475 mm, sd 8; links `02-HID` 93 % bei d = 418–2540 mm, sd 435. Kein Segment hat beidseitig eine verwertbare Kante. |
| Stützenreihe | 4 Texte `STB SÄULE …` im ganzen Plan, davon 2 bei seg_92/94 (Abstand 2810 mm) — zwei Stützen auf 6.2 m, keine dritte. 44 STB-Hatches sind 0.3–2.2 m² Wand-/Deckenschraffuren; Lücken auf der Achse 4342/391/1142/390 mm, keine Regelmäßigkeit. |
| Geländer-/Brüstungslinie | Mollgasse: **0 Entities** auf einem Layer mit `GELÄNDER|BRÜSTUNG`, nur 26 Textannotationen auf `02-TXT`/`05-TXT`. Text trägt keine Geometrie. |
| Zaun als eigener Layer | existiert nicht (0 Layer mit `ZAUN`). |
| nächstes Raumpolygon heranziehen | 200.0–1269.6 mm entfernt; bei seg_4/seg_7 **exakt eine Wandstärke** — das Polygon liegt jenseits der Fassade, seine Kante ist die Innenseite eines anderen Raums. Wäre die falsche Fläche. |

**Gegenprobe — jede solche Regel wäre unbrauchbar, und das fällt schon auf
Mollgasse selbst:** eine Regel „nimm die nächste durchgehende Linie als
Wegrand" greift bei **107 von 107** heute korrekt gemessenen Segmenten auf das
Achsraster zu (`AXO<4m` 107/107) und würde jede richtige Messung durch eine
erfundene ersetzen. Die Gehsteig-Variante berührt 0 der messbaren, steht aber
auf 6 Entities eines einzigen Plans. Layer-Inventar über alle fünf Pläne
(Entities AXO/HLP/HID/09-WEG/09-NAT/GEHSTEIG): Mollgasse 267/94/268/140/115/6,
Barawitzka 0/0/0/0/0/5, Muthgasse 0, Rennweg EG 0, Rennweg OG3 0. Das gesamte
Begrenzungs-Vokabular existiert **nur auf Mollgasse** — auf den vier anderen
Plänen wäre die Regel weder wirksam noch prüfbar; man könnte dort nicht einmal
messen, ob sie Phantom-Räume erzeugt. Barawitzkas 688
„Geländer/Brüstung"-Entities sind ArchiCAD-Stiftlayer und bereits abgeräumt
(`docs/ENIS_UEBERGABE_0908.md` § 270: 123 Entities, 2 räumliche Cluster auf
20 × 34 m → „trägt nicht").

**Entscheidung:** keine Erkennung. Ein aus Gehsteigkante oder Achsraster
gebautes Polygon wäre ein erfundenes Maß und arbeitete gegen
`tests/contract/test_keine_erfundenen_masse.py`. Die 12 Segmente bleiben `None`
mit Grund, ebenso die 8 Stummel unter `nur_tuer_oder_eckpunkte`. Belege
(Session-Scratchpad): `_lg_seg_tab.py/.json`, `_lg_umfeld2.py` +
`_lg_umfeld_Mollgasse_EG.json`, `_lg_texte.py`, `_lg_rays.py`,
`_lg_kandidaten.py`, `_lg_stuetzen.py`, `_lg_gelaender.py`, `_lg_gegen.py`,
`_lg_phantom.py`, `_lg_aussen.py`, `_p5_mess_lg_repro.json`, Planausschnitte
`_lg_A_seg4.png` … `_lg_F_seg8.png`.

### @EnisAMG — Fluchtwegbreite auf Wegen im Freien (Hofweg / Vorplatz / Laubengang)

Diese Frage ist von der Erkennungs-Entscheidung **unabhängig** und bleibt auch
dann offen, wenn wir nie ein Außen-Polygon bauen.

Kontext: `raumerkennung/breitenprofil` misst 287/307 Fluchtwegsegmente. Von den
20 Resten liegen 12 auf Mollgasse_EG (seg_4/7/8/9/10/27/34/41/92/93/94/95),
alle aus dem Außenanlagen-Layer `09-WEG_G00-LEG-M0`, ohne Raumpolygon (nächstes
200.0–1269.6 mm entfernt). Begrenzt sind sie, wenn überhaupt, durch Zäune
(H = 1.00/1.20/1.50 m), Mauersockel, Pflanztröge (h = 40 cm) und die
Gehsteigkante — nicht durch Wände. Überdacht ist keiner.

- **Frage 1:** Ist ein Weg im Freien auf Eigengrund (Hofweg, Vorplatz,
  Laubengang/Außengang) im Sinne von OIB-RL 4 Kapitel 2 ein Fluchtweg **mit**
  Breitenanforderung — oder endet die Breitenanforderung an der Gebäudehülle,
  weil der Weg ins Freie dort bereits erreicht ist?
- **Frage 2:** Falls ja — worauf bezieht sich dann die „Breite"? Bei einem Zaun
  mit H = 1.00 m oder einem Pflanztrog mit h = 40 cm gibt es keine
  raumbildende Begrenzung; die nächste durchgehende Linie im Plan ist das
  Achsraster.
- **Frage 3:** Falls nein — dürfen wir die betroffenen Segmente dauerhaft mit
  `None` + Grund führen (kein Zielbandverstoß), oder sollen sie vorher aus der
  Fluchtwegmenge fallen? Heute zählen sie in den Nenner 307 hinein.

Was unsere eigene Quelle hergibt (`normwissen/data/oib_rl4_fluchtwegbreiten.yaml`,
gegen das Original geprüft): `anwendungsbereich.gilt_fuer` = „Gebäude; für
sonstige Bauwerke sind die Bestimmungen sinngemäß anzuwenden" — ob ein Hofweg
ein „sonstiges Bauwerk" ist, sagt die Richtlinie nicht. `ausnahme_kleingebaeude`
kennt nur eingeschossige Gebäude ≤ 15 m² BGF, keine Wege.
`mindestbreiten.gaenge` (2.4.1): Hauptgang 1.20 m, 1.00 m nur in der
abschließenden Fallliste — „Gang" ist nicht definiert und nicht auf innen/außen
abgegrenzt. `mindestbreiten.durchgangshoehe` (2.4.8): 2.10 m auch für Gänge —
im Freien nicht sinnvoll anwendbar, was gegen eine ungeprüfte Ausdehnung des
Gangbegriffs spricht. Die einzigen Stellen mit „im Freien" sind
`stadien_versammlungsstaetten_im_freien` (2.4.6) und `tueren.stadien_im_freien`
(2.8.2) — anderer Gegenstand. `⚠_fertigmass` gilt (Vergleich mit Roh-/Nennmaß
unzulässig). `status: nicht_pruefbar`; `benoetigte_angaben` verlangt von uns die
„tatsächliche lichte Breite je Fluchtweg-Abschnitt" — genau die Größe, die hier
nicht existiert.

`knowledge/` gibt nichts her (Volltextsuche `laubengang|außengang|offener gang|
im freien` über `knowledge/extracted` und `normwissen/`): nur
`knowledge/_extracted_text/digests/buecher/Baukonstruktionslehe 1.part11.md:177`
(„Balkone können Erschließungswege (Laubenganghäuser), Fluchtwege … bilden" —
Fachbuch, keine Norm, ohne Maßangabe),
`knowledge/extracted/bildlehren/Bildlehren_GSYSTEMS.md:89` (EN 1838,
Beleuchtung einschließlich außenliegender Treppen — keine Breitenanforderung)
und `knowledge/extracted/OVE_E_8101_niederspannungsanlagen.md:69`
(Fluchtweg-Definition über das Ziel „sicherer Ort im Freien", ohne Aussage zur
Breite des Wegs dorthin).

Ohne Antwort bleibt die Behandlung wie heute: keine Messung, `None` mit Grund.
**Owner: Enis (`normwissen/`).**

### @EnisAMG — Raumstempel-Abkürzungen ohne Kanon-Eintrag (Muthgasse E2)

Reine Vokabular-Entscheidung, keine Code-Frage. Belege in
`docs/ENIS_UEBERGABE_0908.md` § 13.

Alle 10 untypisierten Räume in Muthgasse_E2 tragen einen **vollständigen,
korrekt gefundenen** Raumstempel auf `A-AREA-IDEN` (Nummer, Name, m², Belag).
Sie bleiben untypisiert, weil der Name in keinem der drei Wörterbücher in
`raumtyp.py` steht (`_EXTRA_LABELS:65`, `_EXTRA_DIRECT:95`,
`_EXTRA_OVERRIDE:125`) und `stempel_anker.py:219-221` ohne erkannten Namen gar
keinen `Stempel` erzeugt. Wir setzen nichts, solange die Zuordnung nicht
fachlich entschieden ist — ein geratener `raum_typ` erzeugt eine Leuchte an
falscher Stelle.

- **Frage 1 — `Schl.` (2 Räume: `raum_65` 13,04 m², `raum_67` 3,73 m²).**
  Der Plan belegt eine Verkehrsfläche: Nummer `E2-VF-11a`/`-11b`, und das
  Präfix `VF` trägt in diesem Plan ausschließlich Verkehrsflächen (`STGH`,
  `Gang`, `Aufzug 1/2`, `FW-Aufzug`, `Podest`, `Stiege`) — kein einziger
  Wohnungsraum, die tragen Top-Nummern. `raum_65` liegt mit 0 mm Abstand an
  fünf STIEGENHAUS-Polygonen, hat `Ker.Bel.` und `EI ₂ 30-C`-Türen an beiden
  Durchgängen. Wir lesen das als **Schleuse** (Brandschutzschleuse vor dem
  Stiegenhaus), nicht als Schlafzimmer — ausgeschrieben steht es im Plan
  nirgends.
  → Bekommt `Schleuse` einen eigenen Kanon-Typ (`docs/VOKABULAR.md` § 1 kennt
  ihn nicht), und mit welcher Nutzungsklasse? Wirkung, gemessen:
  `ALLGEMEIN_ERSCHLIESSUNG` würde 2 Räume typisieren und `tuer_50` zur
  `stiegenhaustuer` machen (+1 `stair_exit` für `test_soll_stair_exits`);
  `WOHNUNG_PRIVAT` hätte keine Wirkung auf die Ausgänge.
  → **Ausformuliert mit Planausschnitt, Indizientabelle und Kurzform-Scan über
  alle fünf Pläne im letzten Abschnitt dieser Datei.**
- **Frage 2 — `Vorr.` (3 Räume) und `Schrankr.` (1 Raum).**
  Gilt `Vorr.` als `VORRAUM` und `Schrankr.` als `ABSTELLRAUM`? Beide Kanon-Typen
  existieren, nur die Abkürzung fehlt im Wörterbuch. Beide führen zu
  `WOHNUNG_PRIVAT`, also ohne Wirkung auf Ausgänge — sie schließen aber die
  Türtypisierungs-Lücke `unbekannte_kombination` bei `tuer_11/12/13`.
- **Frage 3 — `SR` (2 Räume Muthgasse, je 1 in Barawitzka und Mollgasse) sowie
  `Aufzug 1`/`Aufzug 2` (2 Räume).** `SR` ist ohne Auflösung mehrdeutig.
  `Aufzug` steht als Token nur über `fw` (`FW-Aufzug`) im Wörterbuch; ein
  Eintrag `aufzug` hätte über alle fünf Pläne **11 Falschtreffer** (Kabinen- und
  Bedienfeldbeschriftungen, Maßketten) und ist ohne m²-Kontextbedingung nicht
  sicher.

Falschtreffer-Messung über alle fünf Pläne (`_r65_falschtreffer.py`,
token-exakt, „Falschtreffer" = Treffer ohne m²-Nachbar, also kein Raumstempel):
`schl` 0, `vorr` 0, `schrankr` 0, `sr` 0, `aufzug` 11, `stiege` 4, `podest` 4.
Die ersten vier wären also risikofrei umsetzbar, sobald das **Label** feststeht.

**Owner: Enis (`normwissen/`).** Bis zur Antwort bleiben die Räume untypisiert;
das ist gewollt und kein Defekt.

### @EnisAMG — Entscheidung `Schl.`: **Schleuse** oder **Schlafzimmer**? (2026-09-10, Selman)

Ausformulierung der Frage 1 aus dem Abschnitt darüber. Alle Zahlen gemessen
(`_s2_r65_steckbrief.py`, `_s2_r67.py`, `_s2_kurzform_scan.py`,
`_s2_kurzform_bilanz.py`), Belege in `docs/ENIS_UEBERGABE_0908.md` § 13.
**Es ist nichts gesetzt und nichts geraten: der `xfail` bleibt, ein neuer
Kanon-Typ entsteht erst nach deiner Entscheidung.**

#### Planausschnitt `raum_65` (Muthgasse_E2)

| Feld | Wert |
|---|---|
| Fläche | **13,04 m²** (Stempel `13,04 m²`, deckungsgleich mit dem Polygon) |
| Zentrum (xy_mm) | 335 283 / 108 862 |
| bbox | x 333 153…337 815, y 106 351…111 004 mm → 4,66 × 4,65 m, **L-förmig um den Stiegenkern gewickelt** |
| Umfang / Punkte | 15,28 m / 15 Stützpunkte |
| Stempelgruppe (`A-AREA-IDEN`) | `E2-VF-11a` · **`Schl.`** · `13,04 m²` · `Ker.Bel.` |
| Heute | `raum_typ` leer, `nutzungsklasse=None`, `flag=kein_stempel`, Kaskadenzweig `L` |

**Nachbarräume (Polygonabstand ≤ 2000 mm):**

| Abstand | Raum | raum_typ | Nutzungsklasse | Fläche |
|--:|---|---|---|--:|
| 0 mm | `stiegenhaus_1` | STIEGENHAUS | ALLGEMEIN_ERSCHLIESSUNG | 11,16 m² |
| 0 mm | `stiegenhaus_2` | STIEGENHAUS | ALLGEMEIN_ERSCHLIESSUNG | 7,89 m² |
| 0 mm | `stiegenhaus_3` | STIEGENHAUS | ALLGEMEIN_ERSCHLIESSUNG | 8,14 m² |
| 0 mm | `stiegenhaus_4` | STIEGENHAUS | ALLGEMEIN_ERSCHLIESSUNG | 8,22 m² |
| 0 mm | `stiegenhaus_5` | STIEGENHAUS | ALLGEMEIN_ERSCHLIESSUNG | 10,66 m² |
| 180 mm | `raum_52` | untypisiert (Stempel `SR`) | – | 5,19 m² |
| 180 mm | `raum_46` | GANG | ALLGEMEIN_ERSCHLIESSUNG | 28,52 m² |
| 267 mm | `raum_89` | BAD | WOHNUNG_PRIVAT | 4,19 m² (**nur Wandkontakt, keine Tür**) |
| 666 mm | `raum_94` | GANG | ALLGEMEIN_ERSCHLIESSUNG | 18,10 m² |
| 1522 mm | `raum_50` | ZIMMER | WOHNUNG_PRIVAT | 13,38 m² |
| 1809 / 1920 mm | `lift_4` / `lift_5` | LIFT | KEIN_RAUM | je 3,73 m² |

**Lage zum Stiegenhaus:** Abstand **0 mm zu fünf STIEGENHAUS-Polygonen**
(`stiegenhaus_1…5` sind Podest- und Laufteilstücke desselben Kerns),
gemeinsame Kontaktlänge zusammen ~8,2 m.

**Türen (5 echte Übergänge, dazu 2 Selbstbezüge aus Textankern):**

| Tür | Quelle | lichte Breite | von → nach | Gegenseite |
|---|---|--:|---|---|
| `tuer_50` | `arc_aussen+text:E2-VF-12a` | 655 mm | `stiegenhaus_1` → `raum_65` | STIEGENHAUS |
| `durchgang_140` | `durchgang+text:E2-VF-12a` | 1126 mm | `raum_65` → `stiegenhaus_1` | STIEGENHAUS |
| `durchgang_141` | `durchgang+text:T-E2-VF-11a-1` | 1513 mm | `raum_65` → `stiegenhaus_2` | STIEGENHAUS |
| `durchgang_142` | `durchgang` | 1515 mm | `raum_65` → `stiegenhaus_2` | STIEGENHAUS |
| `durchgang_120` | `durchgang+text:T-E2-VF-11a-2` | 2196 mm | `raum_52` → `raum_65` | untypisiert (`SR`) |

**4 von 5 Übergängen führen direkt ins Stiegenhaus. Kein einziger Übergang
führt zu einem Raum mit `nutzungsklasse=WOHNUNG_PRIVAT`.** An zwei der
Stiegenhaus-Durchgänge steht die Türbeschriftung **EI₂30-C** (im DXF in drei
MTEXT-Fragmente zerlegt: `EI` + Index 2 + `30-C`), dazu `121`/`200` als lichtes
Maß und `STUK= +11,12`. Im 5-m-Ring: `Glaswand EI90+A2`, 2× `E90`.

#### Indizien für beide Lesarten

| Indiz | Messwert | spricht für |
|---|---|---|
| Nummernpräfix | `E2-VF-11a` — `VF` trägt im Plan **ausschließlich** Verkehrsflächen (STGH, Gang, Aufzug, Podest, Stiege); Wohnungsräume tragen Top-Nummern `E2-7-…` bis `E2-10-…` | Schleuse |
| Wohnungszugehörigkeit | keine Tür zu einem `WOHNUNG_PRIVAT`-Raum | Schleuse |
| Türen ins Stiegenhaus | 4 von 5 | Schleuse |
| Brandschutz | 2× vollständige EI₂30-C-Beschriftung, exakt an den beiden Stiegenhaus-Durchgängen | Schleuse |
| Anzahl Öffnungen | 3 Öffnungen — Durchgangsraum, kein Sackraum | Schleuse |
| Geometrie | L-förmig, 15 Punkte, um den Stiegenkern gewickelt, 8,2 m gemeinsame Kante, Abstand 0 mm | Schleuse |
| Belag | `Ker.Bel.` (Keramik). Wohnräume dieses Plans tragen `Parkett` (49×), Nassräume `Ker.Bel.` (26×) | Schleuse |
| Plan-Vokabular | Schlafräume heißen in diesem Plan ausgeschrieben **`Zimmer` (20×)**; die Tokens `Schlaf…` und `SZ` kommen **null Mal** vor | Schleuse |
| Zweiter `Schl.`-Raum | `raum_67`, `E2-VF-11b`, **3,73 m²**, Nachbarn `raum_88` STIEGENHAUS (0 mm) und `raum_68` GANG (180 mm), Türen → Stiegenhaus + Gang, ebenfalls `Ker.Bel.` — als Schlafzimmer physisch ausgeschlossen | Schleuse |
| **Fläche 13,04 m²** | liegt im Zimmer-Flächenband des Plans (19 ZIMMER: min 1,17 / median 10,31 / max 18,95 m²) | **Schlafzimmer** |
| Nachbarschaft `raum_89` BAD (267 mm) | Wandkontakt, aber **keine Tür** dorthin | neutral |

**Für „Schlafzimmer" spricht ausschließlich die Fläche** — und diese nur bei
`raum_65`, nicht bei `raum_67` (3,73 m² unter derselben Abkürzung, gleiche
Nummernserie `E2-VF-11a/b`). Jedes andere gemessene Merkmal spricht für eine
Rauch-/Brandschutzschleuse vor dem Stiegenhaus.

#### Die Entscheidungsfrage

> **Ist `Schl.` in dieser Plan-Familie eine Schleuse oder ein Schlafzimmer?**
>
> - **Schleuse** — Brandschutz-/Rauchschutzschleuse vor dem Stiegenhaus, Teil
>   der Erschließung, damit **beleuchtungspflichtig**. Dann brauchen wir von dir
>   das Kanon-Label: eigener Typ `SCHLEUSE` in `docs/VOKABULAR.md` § 1 +
>   `RoomType` (heute existiert beides nicht), oder Zuordnung auf einen
>   bestehenden Typ (`VORRAUM`/`GANG`) — plus die Nutzungsklasse
>   (`ALLGEMEIN_ERSCHLIESSUNG`?).
> - **Schlafzimmer** — privat, **keine Notbeleuchtung**. Dann Wörterbucheintrag
>   `schl → ZIMMER`, Nutzungsklasse `WOHNUNG_PRIVAT`.

Gemessene Wirkung der Entscheidung: `ALLGEMEIN_ERSCHLIESSUNG` typisiert 2 Räume
und macht `tuer_50` zur `stiegenhaustuer` (+1 `stair_exit` in
`test_soll_stair_exits`); `WOHNUNG_PRIVAT` hat keine Wirkung auf die Ausgänge.
Falschtrefferrisiko für den Token `schl` über alle fünf Pläne: **0**
(token-exakt gemessen, „Falschtreffer" = Treffer ohne m²-Nachbar).

Ersatzweise `GANG`/`VORRAUM` **zu raten** ist der einzige Weg, den wir nicht
gehen: er entscheidet über Leuchte oder keine Leuchte.

#### Kurzform-Scan über die anderen vier Pläne — ist das ein Einzelfall?

Methode: alle m²-verankerten Stempelgruppen (r=1500 mm, wie
`stempel_anker._stempel_aus_texten`, zusätzlich auf den Layer des m²-Ankers
eingegrenzt) plus alle INSERT/ATTRIB-Stempel aus `finde_stempel`.
„Nicht aufgelöst" = kein Kandidat der Gruppe liefert `raumtyp_flags(...)` ungleich `None`.

| Plan | Stempelgruppen | aufgelöst | **nicht aufgelöst** | INSERT-Stempel ohne Typ |
|---|--:|--:|--:|--:|
| Barawitzka_EG | 65 | 36 | **29** | 0 |
| Mollgasse_EG | 4 | 0 | **4** | **27** |
| Muthgasse_E2 | 130 | 99 | **31** | 0 |
| Rennweg_EG | 0 | 0 | 0 | **5** |
| Rennweg_OG3 | 0 | 0 | 0 | 0 |

Echte Abkürzungen ohne Kanon-Auflösung (je `raumtyp_flags=None`,
`classify_room=UNKNOWN`):

| Kurzform | Bara. | Moll. | Muth. | Renn_EG | Renn_OG3 | Σ |
|---|--:|--:|--:|--:|--:|--:|
| `Vorr.` | 0 | 0 | 8 | 0 | 0 | **8** |
| `SR` | 1 | 1 | 3 | 0 | 0 | **5** |
| **`Schl.`** | 0 | 0 | **2** | 0 | 0 | **2** |
| `Schrankr.` | 0 | 0 | 1 | 0 | 0 | **1** |
| `gärtn. gest.` | 2 | 0 | 0 | 0 | 0 | 2 |

**`Schl.` kommt nur in Muthgasse_E2 vor, dort zweimal — in den anderen vier
Plänen null Mal.** Es ist damit kein einmaliger Ausrutscher, aber auch nicht die
Spitze: Platz 3 hinter `Vorr.` (8) und `SR` (5).

Wirkung auf die Untypisiert-Zahl (50 untypisierte Räume über fünf Pläne,
identisch mit § 13.6): `Schl.` kostet **2 von 50** (4 %). Die vier Kurzformen
zusammen (`SR` 4, `Vorr.` 3, `Schl.` 2, `Schrankr.` 1) kosten **10 Räume =
20 %**. Die Mehrheit (Mollgasse 28, Rennweg_EG 5) hängt dagegen an
**ausgeschriebenen** Außenraum- und Nutzungsbegriffen (`EIGENGARTEN`, `GEHWEG`,
`VORPLATZ`, `TOP n`, `GESCHÄFTSLOKAL`, `Müllplatz`), nicht an Abkürzungen — das
ist eine getrennte Vokabularfrage und nicht Teil dieser Entscheidung.

**Owner: Enis (`normwissen/`).** Bis zur Antwort bleiben `raum_65` und
`raum_67` untypisiert, der `xfail` bleibt stehen, und es entsteht **kein neuer
Kanon-Typ**.

### Entscheidung `Schl.` (Enis, 2026-09-11) + Entscheidungsvorlage für die übrigen Vorkommen

Antwort auf die Frage im Abschnitt darüber — der bleibt als Herleitung stehen,
**zwei seiner Zahlen sind unten korrigiert**. Alle Zahlen hier aus einem
Inventar-Lauf über 13 DXF (fünf Prüfpläne + Muthgasse DD/E2–E9), Texte gelesen
wie `stempel_anker.finde_stempel` (TEXT, MTEXT `plain_text()`, ATTRIB,
Blocktexte), Token-Regel `raumtyp._WORT`.

**Entschieden: `E2-VF-11a` = `SCHLEUSE`** (Rauch-/Brandschutzschleuse vor dem
Stiegenkern), Nutzungsklasse `ALLGEMEIN_ERSCHLIESSUNG`, Fluchtweg + communal.
Die **Notbeleuchtungsanforderung bleibt ausdrücklich offen** und ist gesondert
zu prüfen (`normwissen/data/regel_deckung.yaml` → `SCHLEUSE: offen`, Owner
Enis). Begründung (Enis): Lage beim Stiegenkern und der ausgeschriebene
Vergleichstext `DBA-Abstr. Schleuse` in E8/E9 an derselben Lage.

Umgesetzt ist genau das — und nicht mehr:

- Kanon-Typ `SCHLEUSE` in `docs/VOKABULAR.md` §1, `raumtyp._EXTRA_DIRECT`
  (**nur das ausgeschriebene Wort** `schleuse`), `nutzungsklasse._MAP`,
  Enis' LB-Stützliste und `regel_deckung.yaml`.
- Das **Kürzel** `Schl.` steht bewusst NICHT im Wörterbuch. Es löst nur
  `raumerkennung/kuerzel_entscheid.py` auf, und nur bei **Zusatzbeleg UND
  Owner-Entscheidung für genau diese Stempelnummer**. Beleg ohne Entscheidung →
  untypisiert + Hinweis „Entscheidung ausstehend"; kein Beleg → untypisiert +
  Hinweis „kein Zusatzbeleg". Beide Hinweise stehen im Prüfbericht
  (`bericht.md` → „Hinweise Kürzel-Auflösung").

#### Inventar: alle `Schl.`-Vorkommen über die fünf Prüfpläne

`Schl.` kommt **nur in Muthgasse_E2** vor, dort 2×. Token `schl` in den anderen
vier Plänen: **0** (die Substring-Treffer `Anschluß`, `Lüftungsschlitz`,
`TÜRSCHLIESSER`, `Frischluftansaugung`, `E-HAUSANSCHLUSSKASTEN` sind keine
Tokens). Token `schleuse` in allen fünf Plänen: **0** — der neue
Wörterbuch-Eintrag ändert an den fünf Plänen also nichts.

| Vorkommen | Lage (xy_mm) | Stempelgruppe | Raum (`raeume.json`) | Belege | was fehlt |
|---|---|---|---|---|---|
| `E2-VF-11a` | 335 239 / 108 646, MTEXT `A-AREA-IDEN` | `E2-VF-11a` · `Schl.` · `13,04 m²` · `Ker.Bel.` | `raum_65`, Quelle L, Typ leer, 13,04 m², 15 Punkte | Stiegenkern-Lage (0 mm zu den Treppen-Extents) · Text `DBA` in 1495 mm (ab Namens-Text; der Code misst ab dem m²-Anker `Stempel.position_mm`: 1663 mm bei Radius 2000 mm) · E8 `DBA-Abstr. Schleuse` 627 mm, E9 10 mm | **nichts — entschieden** |
| `E2-VF-11b` | 333 017 / 97 219, MTEXT `A-AREA-IDEN` | `E2-VF-11b` · `Schl.` · `3,73 m²` · `Ker.Bel.` (Nummerntext 350 mm) | `raum_67`, Quelle L, Typ leer, 3,73 m², 8 Punkte; liegt zu **99,3 %** in `raum_88` (Quelle F, STIEGENHAUS) | Stiegenkern-Lage (0 mm zu `raum_88`) · Text `WDB DBA` in 1042 mm (ab m²-Anker 1232 mm), `DBA` in 1787 mm | **Owner-Entscheidung** (s. offene Frage unten) |
| Barawitzka_EG, Mollgasse_EG, Rennweg_EG, Rennweg_OG3 | — | 0 Treffer | — | — | — |

#### Zwei Korrekturen am Abschnitt darüber (gemessen, nicht geglättet)

1. **„~8,2 m gemeinsame Kontaktlänge" ist mit der dortigen Definition nicht
   reproduzierbar.** Nachgemessen ergibt die gemeinsame Kante von `raum_65` zu
   `stiegenhaus_1…5` **Σ 4,72 m** (Gegenrichtung gemessen **Σ 5,21 m**), nicht
   8,2 m. Die Einzelkanten: 662 / 1132 / 1131 / 1131 / 662 mm.
2. **„0 mm Abstand zu fünf STIEGENHAUS-Polygonen" beruht auf Überlappung mit
   Treppen-Rechtecken, nicht auf Wandkontakt zu Raumpolygonen.** Die Räume
   `stiegenhaus_1…8` sind Bounding-Rechtecke der Treppen-Blockreferenzen
   (`geometrie_typ.py:47-63`, `:89`) und stehen nur im Provider-Dump, **nicht in
   `raeume.json`**. Geometrisch sind die fünf nur **2 Lagen** (IoU 0,960–0,991
   bzw. 0,956). Gegen das STIEGENHAUS-Polygon `raum_88` aus `raeume.json` ist
   `raum_65` **4848 mm** entfernt. Und: dieselbe 0-mm-Klasse enthält die Küchen
   `raum_29`, `raum_91`, `raum_86` — **das Merkmal trennt Schleuse nicht von
   Küche.** Genau darum ist die Stiegenkern-Lage im Code nur *Beleg*, nie
   Entscheidung.

#### Der eigentliche Unterscheider: das Vergleichsgeschoss

E3–E9 teilen das Koordinatensystem von E2 (häufigster Versatz je Geschoss
`0 / 0`; der Text `DBA` steht in E2–E9 exakt bei 331 620 / 98 334).

| Geschoss | an der Lage von `raum_65` | an der Lage von `raum_67` |
|---|---|---|
| E3–E6 | `Schl.` `E?-VF-11a`, 13,03–13,04 m², IoU ≥ 0,999 | `Schl.` `E?-VF-11b`, 3,73 m², IoU ≥ 0,999 |
| E7 | `Schl.` `E7-VF-11`, 13,03 m² | **WC** `E7-SF-32`, 4,36 m² |
| E8 | `Schl.` `E8-VF-11`, 13,03 m² | **SR** `E8-114-06`, 6,07 m², Parkett |
| E9 | KIWA + Gang (`Schl.` dort verlegt) | **SR** `E9-121-06`, 6,07 m² |

`DBA-Abstr. Schleuse` steht in **E8** bei 332 846 / 108 857 = **627 mm von
`raum_65`**, 9791 mm von `raum_67`; in **E9** **10 mm von `raum_65`**.
In E2 selbst kommen `Schleuse` und `Abstr` **nicht** vor.

**Folge für den Code:** ein Einzelplan-Parse sieht die Nachbargeschosse nicht —
dieser Beleg steckt deshalb in der *Entscheidung* (Register in
`kuerzel_entscheid.py`), nicht in einer Erkennungsregel.

#### @EnisAMG — offene Frage: gilt die Entscheidung auch für `E2-VF-11b` (`raum_67`)?

Bis zu deiner Antwort bleibt `raum_67` **untypisiert** mit dem Hinweis
„Entscheidung ausstehend" im Prüfbericht. Das ist gewollt und kein Defekt.

| spricht dafür (auch Schleuse) | spricht dagegen |
|---|---|
| gleiche Nummernserie `E2-VF-11a/b`, gleicher Belag `Ker.Bel.` | **3,73 m²** — klein für eine Schleuse, und identisch mit der Fläche von `lift_4`/`lift_5` |
| 0 mm zum STIEGENHAUS-Polygon `raum_88`, 180 mm zum GANG `raum_68` | liegt zu **99,3 %** in `raum_88` (F-Artefakt) — die Lage ist also teilweise dieselbe Fläche, kein eigener Vorraum |
| Text-Beleg `WDB DBA` in 1042 mm (ab m²-Anker 1232 mm) | `DBA-Abstr. Schleuse` steht in E8/E9 **9,8 m entfernt**, also an `raum_65`, nicht hier |
| E3–E6 tragen an derselben Lage `Schl.` `E?-VF-11b` | **E7 trägt dort ein WC**, **E8/E9 ein SR** (6,07 m², Parkett) — die Lage ist über die Geschosse nicht stabil erschließungsgenutzt |
| 2 Übergänge (Stiegenhaus + Gang), kein Sackraum | nur 1 `EI`+`30-C`-Beschriftung im Polygon + 500-mm-Ring (bei `raum_65`: 3) |

Zum Entscheiden brauchen wir von dir genau eine Aussage: **`E2-VF-11b` = auch
`SCHLEUSE`** (dann ein zweiter Register-Eintrag) **oder ein anderer Typ** (dann
welcher) **oder bleibt untypisiert**.

## Auflage A — `lichte_quelle` mit dem ersten Erzeuger von `lichte_mm` (Enis, Contract 1.4.0)

Stand 2026-09-12, Selman. Auflage von @EnisAMG zur Zustimmung `raum_modell`
1.4.0: **„`lichte_quelle` samt Test spätestens mit dem ersten Erzeuger von
`lichte_mm`."** Heute setzt **kein** Code `lichte_mm`: das Feld ist nur
deklariert (`hauptengine/contracts/raum_modell.py:107`),
`tests/raumerkennung/test_tueren.py:141` pinnt `lichte_mm is None`, und
`lichte_quelle` ist bewusst nicht angelegt (`docs/ENIS_UEBERGABE_0908.md:744-745`
— ohne Erzeuger wäre es ein totes Feld). Gemessen über die fünf Prüfpläne
(612 Türen, echter Provider-Lauf): **`lichte_mm` gesetzt bei 0 Türen.**

**Auslöser-Regel.** Wer `lichte_mm` zum ersten Mal auf einen Wert ungleich
`None` setzt, legt **im selben PR** an:

1. `Tuer.lichte_quelle: str | None = None` — Beleg im Format `text:<Beleg>`
   oder `blockname:<Blockname>`, gesetzt genau dann, wenn `lichte_mm` gesetzt ist;
2. den Test „kein `lichte_mm` ohne `lichte_quelle`; ohne Beleg bleibt
   `lichte_mm` `None`" — **fertige Skizze unten**, Ziel
   `tests/raumerkennung/test_tueren.py` neben dem None-Pin Z. 141;
3. die Contract-Änderung mit `CONTRACT_VERSION`-Bump, `python
   scripts/gen_schema.py` (Drift-Gate `tests/contract/test_schema_drift.py`) und
   Approval aller drei Owner auf dem aktuellen Head (Check `contract-freeze`).

Ein PR, der `lichte_mm` ohne 1.–3. setzt, bekommt kein Approval.

**Wo der erste Erzeuger sitzen wird.** Gemessen an Muthgasse_E2, dem einzigen
der fünf Prüfpläne mit Lichte-Angaben; die anderen vier haben 0 DL-Blöcke und
0 `b/h`-Texte.

| Beleg im Plan | Codestelle heute | Was dort fehlt |
|---|---|---|
| **Blockname mit `DL`**: 16 INSERTs in 15 Namen, `TU DF 1 - Umfassungszarge flächenbündig - DL - 800 x 2490` (einmal `x 2000`) | `raumerkennung/tueren.py::_block_tueren` Z. 92–98 — die einzige Stelle, an der ein Blockname zu einer `Tuer` mit Maß wird (`b = _breite_mm(e.dxf.name)` Z. 92, `Tuer(…, breite_quelle="BLOCKNAME" …)` Z. 93–98). Dort käme `lichte_mm=…, lichte_quelle=f"blockname:{e.dxf.name}"` dazu. | Die DL-Blöcke kommen dort **nicht an**: `_ist_tuer_block` (Z. 50–58, Filter Z. 89) liefert für alle 16 `False`, weil `_DOOR_HINT` (Z. 36) `TU DF` nicht kennt. 12 der 16 sieht die Pipeline heute nur über ihren Schwenkbogen, als `TuerOeffnung(quelle="arc", breite_mm=800.0, GEOMETRIE_SCHWENKRADIUS)` 400 mm neben dem INSERT (`tuer_oeffnungen` Z. 182–194); 1 in 1635 mm Abstand, 2 ohne Öffnung in der Nähe, 1 liegt 0 mm auf einem Türblock `…_95x200` (→ 950 mm BLOCKNAME). Der erste Erzeuger muss also die Tür-Erkennung Z. 36/50–58 mit erweitern — das ändert die Türmenge von Muthgasse und braucht einen Prüfstreckenlauf. |
| **Texte `90` / `200`** neben einer der 83 Durchgangslichte-Fahnen (`docs/ENIS_UEBERGABE_0908.md:639-652`) | keine Stelle | Die Fahnen verwirft `_ist_tuer_block` Z. 51–57; übrig bleibt nur der Zähler `_verworfene_bloecke` (Z. 33), die Position geht verloren. „90/200" steht in keinem Prüfplan als **ein** Text (0 Treffer; Muthgasse hat 26 `b/h`-Einzeltexte, häufigster `45,5/100` 12×, keiner `90/200`). Ein Text-Erzeuger wäre eine neue Funktion neben `text_tueren` (`tueren.py:336-353`), aufgerufen in `provider.py::parse` nach Z. 135 (dort ist die Türmenge vollständig, IDs sind neu vergeben) und vor `typisiere_tueren` Z. 141. |

**Kein Erzeuger-Kandidat:** `tuer_zuordnung.py:155-159` und `:217-222` liefern
`GEOMETRIE_OEFFNUNG`, also die Rohbauöffnung, die systematisch **größer** als die
Durchgangslichte ist (`ENIS_UEBERGABE_0908.md:622`). `provider.py:91-98` baut
Türen aus `TuerOeffnung`; die Dataclass (`tueren.py:129-138`) hat kein
Lichte-Feld, und der Pfad greift nur, wenn `tueren_aus_dxf` leer ist (Rennweg,
0 DL-Blöcke).

**Die heutigen 19 BLOCKNAME-INSERTs von Muthgasse tragen keinen einzigen
DL-Token:** `…_1DF_90x200` 8, `…_1DF_95x200` 6, `FE TÜR 2 tlg … 1000 x 2550` 3,
`2D_barrierefrei_Türbereich 150_200 - r75` 2. Damit ist § 6.2 der Übergabe
(`ENIS_UEBERGABE_0908.md:625`, „die 18 BLOCKNAME-Türen trügen DL-Notation")
**durch Messung widerlegt** — die `- DL -`-Blöcke sind gar keine Tür-Blöcke. Ob
`90x200` die Durchgangslichte nennt, ist Enis' offene Frage 9
(`ENIS_UEBERGABE_0908.md:848`); bis zur Antwort ist das kein Beleg und
`lichte_mm` bleibt dort `None`. Ein Messpunkt dazu, ausdrücklich als
Interpretation und nur ein Einzelfall: an einer Position liegt der DL-Block
`DL - 800 x 2490` genau (0 mm) auf einem Türblock `…_95x200` (→ `breite_mm` 950).
Beschreiben beide dieselbe Tür, kann `95x200` dort nicht die Durchgangslichte
sein.

**Randbedingung für den Parser:** `2D_barrierefrei_Türbereich 150_200 - r75`
ergibt über die „erste Zahl"-Heuristik von `_breite_mm` (`tueren.py:77-83`)
750 mm BLOCKNAME — das ist vermutlich ein Radius, nicht eine Türbreite
(semantisch nicht geprüft). Ein Lichte-Parser darf diese Heuristik deshalb
**nicht** übernehmen, sondern muss an den `DL`-Token gebunden sein.

**Was der bestehende Riegel schon leistet — und was nicht.** `lichte_mm` ist
über die Endung `_mm` automatisch Messfeld von
`tests/contract/test_keine_erfundenen_masse.py` (`_messfelder()` Z. 48–58,
nachgeprüft: `lichte_mm in MESSFELDER` = True). `Tuer(lichte_mm=900)` oder
`t.lichte_mm or 900` wird damit rot (Z. 98–108). Ein aus Blockname oder Text
**geparster** Wert ist aber kein Zahl-Literal und geht durch; ob er belegt ist,
sieht der AST nicht. Genau diese Lücke schließt `lichte_quelle` samt Test.

**Test-Skizze (fertig, nicht als lebende Testdatei eingecheckt).** Unverändert
als Scratchpad-Kopie gegen den heutigen Code gelaufen: **`2 passed, 2 xfailed`**
— die Invariante und der Negativfall sind heute grün, die beiden Positivfälle
sind strict-xfail. Der Erzeuger-PR dreht sie auf XPASS (= rot) und muss die
xfails entfernen.

```python
"""Auflage A (Enis, Contract 1.4.0): lichte_mm nur mit Beleg in lichte_quelle.

Jede Tuer mit ``lichte_mm is not None`` traegt ``lichte_quelle`` im Format
``text:<Beleg>`` oder ``blockname:<Blockname>``. Ohne Beleg bleibt lichte_mm
None — nie aus breite_mm abgeleitet, kein Abschlag, kein Faktor.
"""
import re

import ezdxf
import pytest

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.tueren import text_tueren, tueren_aus_dxf

_LICHTE_QUELLE = re.compile(r"^(text|blockname):\S.*$")

# echte Blocknamen aus Muthgasse_E2 (Projekte/_eingang/Muthgasse_E2.dxf)
DL_BLOCK = ("TU DF 1 - Umfassungszarge flächenbündig - DL - 800 x 2490 "
            "-Glas-V147-E 2 - FOK AF 300")
FAHNE = ("HNP_Beschriftung Türen - AF 50 - Durchgangslichte_ Nummer_ "
         "Brandschutz_ STUK oben Projekt-12188994-1")
TUERBLATT = "HNP_T_BZ_1-DF - HNP_T32_BZ-S_H_EI230_1DF_90x200 WET-16703914-1"


def _tueren(plan):
    # ANPASSEN im Erzeuger-PR: die Kette aufrufen, die lichte_mm setzt.
    t = tueren_aus_dxf(plan)
    return t + text_tueren(plan, t)


def _verstoesse(tueren) -> list[str]:
    return [f"{t.id}: lichte_mm={t.lichte_mm} "
            f"lichte_quelle={getattr(t, 'lichte_quelle', None)!r}"
            for t in tueren
            if t.lichte_mm is not None
            and not _LICHTE_QUELLE.match(getattr(t, "lichte_quelle", None) or "")]


@pytest.fixture
def lichte_plan(tmp_path):
    """Drei Tueren nebeneinander (je 6 m Abstand, ausserhalb _TEXT_TUER_NAH_MM):
    (a) Blockname mit DL-Token, (b) Tuerblatt + Durchgangslichte-Fahne mit den
    Texten "90"/"200" (so steht es in Muthgasse, ENIS_UEBERGABE_0908.md:639-652),
    (c) Negativfall: Nennmass im Namen + ein b/h-Text OHNE Fahne."""
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    for name, r in ((DL_BLOCK, 800), (TUERBLATT, 900), ("TÜR-80", 800)):
        doc.blocks.new(name=name).add_arc((0, 0), r, 0, 90)
    doc.blocks.new(name=FAHNE).add_line((0, 0), (0, 1200))
    msp.add_blockref(DL_BLOCK, (2000, 4000))                        # (a)
    msp.add_blockref(TUERBLATT, (8000, 4000))                       # (b)
    msp.add_blockref(FAHNE, (8300, 4300))
    msp.add_text("200", dxfattribs={"insert": (8300, 4400)})
    msp.add_text("90", dxfattribs={"insert": (8300, 4450)})
    msp.add_blockref("TÜR-80", (14000, 4000))                       # (c)
    msp.add_text("45,5/100", dxfattribs={"insert": (14300, 4300)})
    p = tmp_path / "lichte.dxf"
    doc.saveas(str(p))
    return lade_dxf(p)


def _bei(tueren, x):
    return [t for t in tueren if abs(t.xy_mm[0] - x) < 1500]


def test_lichte_nur_mit_beleg(lichte_plan):
    """Invariante — gilt heute (leer) und muss jeden kuenftigen Erzeuger ueberleben."""
    assert not _verstoesse(_tueren(lichte_plan))


def test_ohne_beleg_bleibt_lichte_none(lichte_plan):
    (t,) = _bei(_tueren(lichte_plan), 14000)
    assert t.breite_mm == 800.0 and t.breite_quelle == "BLOCKNAME"
    assert t.lichte_mm is None          # nie aus breite_mm, nie aus "45,5/100"


@pytest.mark.xfail(strict=True, reason="Auflage A: noch kein Erzeuger von lichte_mm")
def test_blockname_dl_setzt_lichte_mit_quelle(lichte_plan):
    (t,) = _bei(_tueren(lichte_plan), 2000)
    assert t.lichte_mm == 800
    assert t.lichte_quelle == f"blockname:{DL_BLOCK}"


@pytest.mark.xfail(strict=True, reason="Auflage A: noch kein Erzeuger von lichte_mm")
def test_text_an_fahne_setzt_lichte_mit_quelle(lichte_plan):
    (t,) = _bei(_tueren(lichte_plan), 8000)
    assert t.lichte_mm == 900
    assert t.lichte_quelle.startswith("text:")
```

**Contract-Skizze (künftige Änderung, hier NICHT umgesetzt):**

```python
class Tuer(BaseModel):
    ...
    lichte_mm: int | None = None
    # Beleg fuer lichte_mm: "text:<Beleg>" | "blockname:<Blockname>".
    # Gesetzt genau dann, wenn lichte_mm gesetzt ist.
    lichte_quelle: str | None = None
```

Dazu eine Zeile in `docs/CONTRACTS.md` bei den `tueren[]`-Punkten. Die
Versionsstufe legt die 3-Owner-Runde fest (sie hängt auch davon ab, ob Auflage B
vorher umgesetzt wird).

**Offen, weil nicht aus dem Plan entscheidbar:** das Format von `text:<Beleg>`
bei zusammengesetzten Angaben — in Muthgasse stehen `90` und `200` als getrennte
Texte. `text:90/200` wäre zusammengesetzt und nicht wörtlich. Die Paarungsregel
Fahne ↔ Texte ↔ Tür ist eine Interpretation und braucht Enis' Zustimmung.

**Owner:** Erzeuger und Test = Selman (`raumerkennung/`); die Contract-Änderung
braucht alle drei; die DL-Lesart entscheidet Enis.

## Auflage B — `STANDARDWERT` ersatzlos streichen? (Vorschlag an Enis, Contract 1.4.0)

Stand 2026-09-12, Selman. **Nur Vorschlag. Der Contract wird nicht ohne
Abstimmung zu dritt geändert** (Check `contract-freeze`, CODEOWNERS). Hier ist
nichts umgesetzt.

@EnisAMG fragt als Auflage zur Zustimmung `raum_modell` 1.4.0, ob
`STANDARDWERT` in `Tuer.breite_quelle` gebraucht wird. Unsere Antwort: **nein.**
Der Wert hat seit dem Riegel gegen erfundene Maße keinen legitimen Erzeuger
mehr, und im Modell hatte er nie einen.

**Ist-Zählung über die fünf Prüfpläne** (echter Provider-Lauf, Stand `804e6af`,
`src/` identisch mit `main` `e79276b`; Dumps je Plan aus
`ArchitekturRaumProvider().parse(...)` wie `plan_pruefen.py:1169-1171`):

| | Barawitzka_EG | Mollgasse_EG | Muthgasse_E2 | Rennweg_EG | Rennweg_OG3 | **Summe** |
|---|--:|--:|--:|--:|--:|--:|
| Türen | 106 | 147 | 291 | 41 | 27 | **612** |
| `STANDARDWERT` | 0 | 0 | 0 | 0 | 0 | **0** |
| `ATTRIBUT` | 0 | 0 | 0 | 0 | 0 | **0** |
| BLOCKNAME | 0 | 40 | 18 | 0 | 0 | 58 |
| GEOMETRIE_SCHWENKRADIUS | 36 | 27 | 28 | 10 | 3 | 104 |
| GEOMETRIE_SUMME | 2 | 0 | 0 | 0 | 0 | 2 |
| GEOMETRIE_OEFFNUNG | 68 | 76 | 170 | 30 | 24 | 368 |
| UNBEKANNT | 0 | 4 | 75 | 1 | 0 | 80 |

Dazu: `breite_mm is None` 80, davon **80 mit `breite_grund`**, 0 ohne;
`breite_mm == 0.0` **0**; `lichte_mm` gesetzt **0**. Es gibt also **keine
einzige Tür mit `STANDARDWERT`** — die Spalte ist über alle fünf Pläne leer.

**Fundstellen, vollständig** (`grep -rIn`, auch ohne Groß-/Kleinschreibung, ohne
`.venv`/`__pycache__`): `hauptengine/contracts/raum_modell.py:41` (Literal, mit
dem Kommentar „Reserve; gehoert NICHT ins Modell (nur Render)"),
`hauptengine/contracts/schema/raum_modell.schema.json:676` (generiert),
`docs/CONTRACTS.md:13` (Spezifikation), dazu historisch
`docs/ENIS_UEBERGABE_0908.md:581/:611/:735` und `docs/COORDINATION.md:371/:375`.
**Erzeuger in `src/` und `scripts/`: 0. Tests: 0. Fixtures/JSON-Daten: 0.** Kein
Code zählt das Vokabular auf; `BreiteQuelle` erscheint nur in
`raum_modell.py:35` und `:105` sowie in einem Kommentar in `tueren.py:137`. Der
einzige Leser von `breite_quelle` außerhalb des Modells,
`scripts/plan_pruefen.py:982-983`, gibt den String nur aus.

**Warum der Wert keinen legitimen Erzeuger mehr hat.**

- Er war nie mehr als der Name für den Zeichen-Default des Renderers. Den gibt
  es weiterhin, aber als benannte Konstante **außerhalb** des Modells:
  `hauptengine/render/dxf_renderer.py:520` `_ZEICHEN_ERSATZBREITE_MM = 900.0`,
  benutzt in `:533` (`breite = t.breite_mm or _ZEICHEN_ERSATZBREITE_MM`).
  Kommentar `:515-519`: „ZEICHEN-ERSATZMASS, KEINE MESSUNG … reine Bildgroesse:
  er wird nirgends zurueckgeschrieben, verlaesst `_draw_tueren` nicht und ist
  KEIN Mass der Tuer." (Die Docs zitieren dafür noch die alte Zeile `:524`.)
- Ein `STANDARDWERT`-Erzeuger im Modell müsste eine Zahl **ohne Messung** in
  `breite_mm` schreiben. Genau das verbietet
  `tests/contract/test_keine_erfundenen_masse.py`: „der Code erfindet keine
  Masse. Fehlt eine Messung, ist das Feld `None` mit `quelle=UNBEKANNT` und
  einem Grund — nie ein Default, nie ein Normwert, nie ein Mittelwert" (Z. 3–5),
  durchgesetzt über `feld or <Zahl>` (Z. 98–103), `feld=<Zahl>` im Aufruf
  (Z. 105–108) und `min/max(feld, <Zahl>)` (Z. 110–119). Für „nicht gemessen"
  gibt es `UNBEKANNT` + `breite_grund` — 80 von 80 Fällen halten das ein.
- **Grenze des Riegels, gemessen:** er erkennt nur Zahlen-**Literale** (`_zahl`
  Z. 64–69) und prüft nur `src/**`. In einer Probe über 11 Muster fängt er 4;
  `Tuer(breite_mm=_KONSTANTE, breite_quelle="STANDARDWERT")`,
  `t.breite_mm = 900.0`, `model_copy(update=…)` und `x if y else 900.0` gehen
  durch, und `breite_quelle` prüft er überhaupt nicht. Ein Enum-Wert, der genau
  den verbotenen Fall benennt, lädt also dazu ein. Streichen macht daraus einen
  Pydantic-`ValidationError` — ohne neuen Riegel.

**Was eine Streichung berühren würde (nicht umgesetzt):**

1. `hauptengine/contracts/raum_modell.py:41` — Zeile aus `BreiteQuelle`.
2. `raum_modell.py:18` — `CONTRACT_VERSION`. Eine Einengung des Enums ist
   formal **nicht** additiv (die Bumps bis 1.4.0 waren additiv). Datenbestand
   mit dem Wert: 0. Die Stufe legt die 3-Owner-Runde fest.
3. `contracts/schema/raum_modell.schema.json:676` — per `python
   scripts/gen_schema.py` neu erzeugen; bis dahin ist
   `tests/contract/test_schema_drift.py` rot.
4. `docs/CONTRACTS.md:13` — den Wert aus der Aufzählung nehmen.
5. Tests: keiner referenziert `STANDARDWERT`; außer dem Drift-Gate ist nichts
   anzupassen. Optional ein Pin: `Tuer(…, breite_quelle="STANDARDWERT")` →
   `ValidationError`.
6. **Nicht anfassen:** die historischen Stellen (`ENIS_UEBERGABE_0908.md`,
   `COORDINATION.md`) bleiben stehen und bekommen einen Nachtrag.
   `dxf_renderer.py` (Leonis' Lane) ist nicht betroffen.
7. Approval aller drei Owner auf dem Head des PR (`contract-freeze`).

**Owner:** Contract = alle drei; die Entscheidung stößt Enis an. Der Vorschlag
ist zusätzlich als Kommentar in PR #154 hinterlegt
(`#154 issuecomment-5641436979`).
