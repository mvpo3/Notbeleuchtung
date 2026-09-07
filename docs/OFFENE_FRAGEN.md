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
