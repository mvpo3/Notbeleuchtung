# Notbeleuchtungs-Regelbasis (NB-R) — aus PDF „Notbeleuchtungen zeichnen" + Mollgasse-Erklärungs-DXFs

Entstanden 2026-09-18 (Phase B): jede Regel ist am PDF-Text begründet UND an der
DXF-Geometrie belegt (Beispiel-IDs aus `beispiele.json`, DXF-Handles dort und in
`abgleich/<G>/abgleich_<G>.md`). Maschinenlesbar: `regeln.yaml`. Symboltypen sind
ausschließlich Registry-catalog_keys (`symbol_konvention.md`). Konfidenz: hoch =
mehrfach belegt, mittel = wenige Belege, niedrig = 1 Beleg / nur Text.

Meta-Regel vorweg (NB-R00, hoch): **„Pfeil nach unten/links/rechts" im PDF
bezeichnet den Block-TYP, nie die Weltrichtung.** Welt-Pfeil = Blockbasis
(down 270° / left 180° / right 0°) + INSERT-Rotation, Toleranz ±1,5°
(lokale Plan-Verdrehungen bis −0,3° gemessen). Positionsmessung immer über
Bbox-Zentren der sichtbaren Geometrie (Basispunkt-Offsets bis >1 km!).
[Belege: EG-01/05, 3OG-Beob.7/8, 4OG-R1, 2OG-R4]

## NB-R01 — Tür-Regel (hoch)
**Wenn** ein Raum über eine Tür an den Fluchtweg anbindet und ein Tür-RZ gesetzt
wird: RZ vom Typ `notlicht_ks_stiege_unten` **in der Türachse** (Querabweichung
gemessen 3–35 mm) und **raumseitig versetzt** (735–930 mm hinter der Schwelle,
gemessen 735/840/913/929; 1OG: 258 mm gangseitig der Wandachse bei Gang-Türen).
**Rotation:** Welt-Pfeil zeigt IN den Raum hinein = entgegen der Fluchtrichtung
durch die Tür = entgegen der Tür-Öffnungsrichtung (1OG-01: Türflügel öffnet Süd,
Pfeil Nord; 7/7 EG-Türbeispiele).
[EG-01/02/03/04/11/12/13, 1OG-01, 2OG-01/03; PDF S.1–4, 12, 14, 20]

## NB-R02 — Allgemeinbereiche (hoch)
**Wenn** ein Raum ein Allgemeinbereich ist (für ALLE Bewohner zugänglich, meist
EG/UG; PDF-Aufzählung nicht abschließend: Müllraum, Fahrradraum, Kinderwagenraum,
Kellerabteil, Technikraum, Spielraum, Geschäftslokal, Innenhof): **immer eine
Leuchte bei der Tür** nach NB-R01. Ein einzelnes Tür-RZ genügt, wenn es vom
gesamten Raum sichtbar ist (EG-11 Sichtlinie 9143 mm).
RaumTyp-Mapping (docs/VOKABULAR.md): MUELLRAUM, KINDERWAGENRAUM, TECHNIK,
ABSTELLRAUM/LAGER (nur ist_communal), KELLERABTEIL, GESCHAEFT/GESCHAEFTSLOKAL,
SPIELRAUM; Innenhof/GEHWEG = Außen-Anbindung an die Gebäudetür (Leuchte an der
Tür, Pfeil in den Hof). [EG-02/03/04/08/11/12/13; PDF S.2–4, 11–13]

## NB-R03 — Haupteingang (hoch)
Über der Haupteingangs-/Hauptausgangstür hängt immer ein RZ vom Typ
`notlicht_ks_stiege_unten`, mittig zur Tür (26 mm), raumseitig davor
(375–840 mm), Welt-Pfeil ins Rauminnere. Es ist das Ziel der Sichtkette beider
Personenströme (UG + OG). [EG-01, EG-07 (H); PDF S.1, 6, 8, 10]

## NB-R04 — Stiegenhauspfeil-Logik (hoch)
Der Architekten-Stiegenhauspfeil zeigt die **Aufwärtsrichtung JE LAUF** (nicht je
Stiegenhaus — 3OG: zwei gegenläufige Pfeile in einem STGH). Personen aus dem UG
bewegen sich IN Pfeilrichtung hinauf, Personen aus OG/DG ENTGEGEN hinunter
(vektoriell: Delta 168–180° an allen 6 Geschossen). Die Leuchte wird so gesetzt,
dass sie beim Erreichen des Geschosses (Blick nach links/rechts) SOFORT sichtbar
ist — je Personenstrom ggf. eine eigene ((A) für UG- vs. (C) für OG-Ankömmlinge,
EG-05). [EG-05/06, 1OG-02/05, 2OG-02/05, 3OG-01/02, 4OG-02/07, DG-01/02]

## NB-R05 — Leuchte vor der Stiege (hoch)
Das Richtungs-RZ vor einer Stiege steht **800–1122 mm vor der Antritts-/
Austrittskante**, auf der Stiegen-/Laufachse (quer 20–130 mm) — Wandmontage als
Alternative, wenn die Sichtbarkeit beim Hinuntergehen es verlangt (4OG-02 (C)).
**Der Welt-Pfeil zeigt exakt in die Abstiegs-/Weiterrichtung des Laufs (≤0,6°)
und nie auf eine Wand** — dafür wird die Position „vor der Stiege" statt
Gangmitte gewählt (PDF S.30 explizit). [1OG-02/05, 2OG-02/05, 3OG-01/02,
4OG-04, DG-01/02; Messwerte 801/810/868/931/940/957/1110/1122 mm]

## NB-R06 — „Pfeil nach unten" = geradeaus, mittig im Gang (hoch)
Ein `notlicht_ks_stiege_unten` im Gangverlauf bedeutet „geradeaus weiter". Es
steht **mittig im Gang** (6–95 mm neben der Gangachse bei 1,2–1,7 m Breite) und
wird so rotiert, dass der **Welt-Pfeil ENTGEGEN der Fluchtrichtung** zeigt
(Delta 178,6–180,0° an 9 Instanzen über 1OG/2OG/4OG/DG) — dadurch steht die
Vorderseite frontal zum ankommenden Strom. [1OG-02/04/05, 2OG-01…05,
4OG-03/07, DG-02; PDF S.18, 33]

## NB-R07 — Auswahl links/rechts/unten nach Frontalsicht (hoch)
Die Pfeilrichtung muss der Fluchtrichtung AUS SICHT der Person entsprechen UND
die Person muss die **Vorderseite** sehen: Symbol-Längsachse quer zum
Betrachter-Korridor; gemessene Sichtwinkel zur Flächennormalen bei
Erst-Leuchten 0,3–45,5° (die im PDF durchgespielten „falsch"-Varianten ergäben
~89° = Seitenansicht). Verläuft der Fluchtweg aus Personensicht nach rechts,
MUSS ein rechts-Typ verwendet werden (und umgekehrt); down-Typ nur, wenn die
Person frontal auf die Breitseite schaut und geradeaus weitergeht.
Für FOLGE-Leuchten in der Kette genügt Sichtbarkeit (bis ~47,5° und
Seitenansicht toleriert: Tür-RZ am Gangende wird von den Wohnungstüren unter
86–90° gesehen — 1OG-O1-Befund). [4OG-01…07, DG-01/02, 1OG-R7, 2OG-R5;
PDF S.31–37]

## NB-R08 — Erster-Blick-Regel (hoch)
Beim Verlassen JEDER Wohnung und jedes Raums muss eine für den weiteren Weg
relevante Leuchte direkt sichtbar sein (Sichtlinien: eine je Wohnungstür,
Start ≤136 mm neben der Tür, Länge 882–12028 mm, 0 Wandschnitte). Reicht die
Distanz/Erkennbarkeit nicht, kommt eine ZUSÄTZLICHE Leuchte dazwischen
(1OG-04: Zusatz-down-RZ (C), weil (D) „möglicherweise nicht ausreichend gut
erkennbar"; dient zugleich der Lux-Deckung). Ein RZ darf mehrere Türen
bedienen (bis 4 Wohnungstüren, 1140–4275 mm — keine Überproduktion).
[1OG-01/03/04, 2OG-01/04, 3OG-02, EG-08; PDF S.14, 17–18, 22, 27, 29–30, 39]

## NB-R09 — Gang mit vs. ohne Tür zum Stiegenhaus (hoch)
**Mit Trenntür:** Tür-RZ an der Trenntür (NB-R01) + Gang-Grundbeleuchtung:
gezeichnete Lösung = **2 Antipanikleuchten auf der Gangmittellinie** (55 mm
neben der Fluchtlinie; Teilung auf ~12-m-Gang: Tür-RZ –3,1 m– AP –6,3 m– AP
–2,6 m– Gangende). Textliche Alternativen (nicht gezeichnet, Konfidenz mittel):
2 Aufheller ODER mittiges down-RZ ODER down-RZ+Aufheller — Wahl nach Situation,
Lux-Nachweis entscheidet. **Ohne Trenntür:** KEIN Tür-RZ an der Mündung;
stattdessen Richtungs-RZ am Knick bzw. vor der Stiege. [1OG-01/05, 2OG-01,
3OG-02; PDF S.14, 19–21, 29]

## NB-R10 — Antipanik bei eingeschränkter Sicht (hoch)
Antipanikleuchten (`antipanik_leuchte`) stehen dort, wo die Sicht der Menschen
auf die Notleuchte blockiert ist (L-/U-Form, Wand dazwischen): EG-10 U-Raum —
Person→RZ 5213 mm wandgeblockt → AP im abgeschatteten Arm (3211 mm vor der
Person). Rechteckige Räume ohne Blockade bekommen KEINE (EG-02/12, 27,6/34,5 m²).
Zusätzlich sind AP/Aufheller Lux-getrieben in Gängen zulässig — der
Lux-Nachweis ist Sache der Lichtberechnung (Flag `lux_nachweis_erforderlich`),
nicht dieser Regelbasis. [EG-10, EG-02/12, 1OG-01, 2OG-01; PDF S.2, 10–12, 20]

## NB-R11 — Hindernisse (mittel — 1 Beleg)
Kollidiert die Sollposition mit einem Hindernis (Lichtkuppel, blau markiert):
Leuchte **entlang der Querrichtung versetzen bis frei** (DG-02: 142 mm aus der
Stiegenachse, 292 mm Zentrum→Kuppelkante), **Rotation/Ausrichtung bleibt
unverändert**. [DG-02; PDF S.40]

## NB-R12 — Sichtkette und Abstände (mittel-hoch)
Die RZ bilden eine lückenlose Kette (jedes RZ führt zum nächsten bzw. zum
Ausgang); gemessene Folgeabstände 1975–7749 mm (EG-Kette (A)→(B)→(D),
(E)→(F)→(H), (G)→(H)). Sichtlinien enden an der Symbol-KANTE. Wand-RZ:
Kante an Wandkante (15–101 mm). [EG-05…08, 4OG-R7/R10, DG-R6]

---

# Erweiterung 2026-09-20 — UG-Kapitel (PDF jetzt 95 S., 1KG S.41–56 / 2KG S.57–94)

Quellen: `abgleich/1KG/abgleich_1KG.md` (14 Beispiele, 12 bestätigt/2
präzisiert) + `abgleich/2KG/abgleich_2KG.md` (19 Beispiele, 16/2/1 —
der eine Widerspruch ist ein PDF-TEXTfehler B↔C auf S.57, an Owner gemeldet).
GT-Messdaten: `tests/fixtures/mollgasse_gt/<G>.json`
(`scripts/analyse/mollgasse_gt_extract.py`).

## NB-R13 — UG-Stiegenrichtung (hoch)
**Untergeschoße:** Menschen flüchten HINAUF **in Richtung des
Stiegenhauspfeils** (der Pfeil zeigt die Aufwärtsrichtung je Lauf, NB-R04);
Obergeschoße ENTGEGEN. Die Leuchte vor/an der Stiege wird so gewählt und
rotiert, dass ihr Welt-Pfeil der Hinauf-Bewegung entspricht und die Frontseite
zum ankommenden UG-Strom zeigt. [1KG-03 (rote Pfeile `1BD31`/`1BD32`),
1KG-06, 2KG-18/19 (`1CEFD` Blick 169,9°, `1CF44` „geht hinauf richtung 1KG");
PDF S.43, 54–55]

## NB-R14 — Montageort Wand vs. Decke (hoch, Fachpraxis)
„Nach der hier verwendeten Platzierungslogik werden Notleuchten an Wänden
hauptsächlich bei Stiegen platziert" (S.56) — **Stiegen-Leuchten = Wand,
Gang-Leuchten = Decke (mittig)**. Alle 14 1KG-Platzierungen konsistent.
Aufzugs-/Sonderfälle nur als Text-Alternative. [1KG-14; PDF S.56]

## NB-R15 — Kabeltrassen-Hindernis (hoch, FACHPRAXIS — kein Normzitat)
Kabeltrassen (blaue Balken, Beschriftung KT300/KT400/KT500): eine Notleuchte
darf **niemals auf/innerhalb** einer Kabeltrasse platziert werden; sie wird
**seitlich versetzt, möglichst ≥ 450 mm** Abstand („Als Platzierungsregel
verwenden wir hier möglichst einen Abstand von mindestens 450 mm zur
Kabeltrasse", S.63–64 — ausdrückliches Fachpraxis-SOLL). Nach dem Versatz
müssen erhalten bleiben: Fluchtwegbezug (Position zuerst fachlich bestimmen),
Sichtbarkeit, Pfeilrichtung, Frontseite, Gebäudehälfte (2KG (A)-Ana `1C7D0`
bleibt trotz 507-mm-Versatz auf der Anastasius-Seite). ⚠️ Befund: die
2KG-DXF-Trassen heißen „KT UK=+2,11 FBOK"; die vertikalen Schraffur-Leitern
sind **Rigole (Bodenrinnen)**, KEINE Kabeltrassen — Leuchten dürfen darauf
stehen. [2KG-05, 2KG-12; PDF S.63–64, 79, 81, 85]

## NB-R16 — Beidseitige Rettungszeichen (hoch)
**Pflicht-beidseitig**, wenn ZWEI Personenströme aus Gegenrichtungen denselben
Knoten nutzen und beide eine Frontseite (weißer Balken) sehen müssen: 2KG (O)/
(J)/(D)-Ana/(K)-Ana/(H)-Moll (Gruppen 1–5), 1KG (I) (Paar xscale ±44,7,
Versatz 395 mm), EG-Paar. **Nur-Alternative** (KEIN Muss): beidseitig am
Richtungswechsel, wenn ein einseitiges RZ fachlich genügt — orange
dargestellt, „muss nicht sein, aber es schadet nicht" (2KG Gruppe 6
`1D326`/`1D327`, S.79–83). Ground-Truth-Konstruktion = zwei gespiegelte
Einzel-Blöcke (Abstand 264–318 mm); die Engine setzt seit 2026-09-20 den
echten Rivoplan-Block `RIVO_NL_ARR_bothsided` (`notlicht_ks_beidseitig`).
ALTERNATIV wird NICHT automatisiert. [1KG-11, 2KG-06/07/10/13/16; PDF S.65–83]

## NB-R17 — Garage: durchquerbare Flächen (hoch, Fachpraxis)
**Motorrad-Parkplatzbereiche sind als Fluchtweg durchquerbar** (Personenreihe
`1CBF6`–`1CBFC` läuft durch die MOTORRAD-Stempel), **Doppelparker-/
PKW-Stellflächen nicht** (0 Fluchtwege durch DOPPELPARKER-Zonen; auch
Doppelparkergruben). Die Durchquerbarkeit folgt aus der realen freien
Geometrie, nicht aus dem Raumlabel. [2KG-06/08; PDF S.65–70]

## NB-R18 — Zwei Gebäudehälften (hoch, projektspezifisches MUSTER + Prozessregel)
Bei zwei zusammengebauten Gebäuden (Mollgasse/Anastasius-Grün-Gasse) teilt
sich der Fluchtweg: Trennung entlang der **weitergeführten Gebäudewand**
(rote Linie `1C7F4`, 116 m), Zuordnung wird am **EG-Grundriss** verifiziert;
jede Hälfte plant ihre Fluchtwege/Ausgänge/Stiegen separat (eigenes
Label-Alphabet A–O / A–N). **Prozessregel (bindend, S.78): unklare Zuordnung
NIEMALS raten → offene Frage.** [2KG-11/12/13/16/17; PDF S.76–83]

## NB-R19 — UG-Nebenräume: Türleuchte nach Nutzung (hoch)
Einzelne kleine Einlagerungsräume/Kellerabteile und kleine Medienräume
bekommen **keine eigene Türleuchte**, wenn nach dem Türdurchtritt sofort ein
Gang-RZ sichtbar ist (Negativ-Beleg im Bestand, 1KG S.53; 2KG Medienraum
S.93). **Technik-/Niederspannungs-/E-Räume bekommen die Tür-Leuchte** (1KG-09
(D): mittig 25 mm, 711 mm raumseitig + Merktext „Stromversorgung aller
Notleuchten"; 2KG S.73). Tür-RZ-Metrik im UG wie NB-R01 (mittig 3–26 mm,
711–779 mm zugangsseitig). [1KG-09/10/12, 2KG-09/15; PDF S.51–53, 71–73, 93]

## NB-R20 — Türlose Gänge und Durchgänge (hoch)
Ein **türloser zusammenhängender Gang** braucht keine Zwischen-RZ, solange die
Sichtkette steht (2KG S.58/61); ein **kurzer Gang mit Direktsicht aller
Türen** bekommt genau EIN Tür-RZ (2KG S.62, 90–91). Ein **offener türloser
Durchgang als Fluchtweg-Knoten** bekommt ein down-Typ-RZ **mittig im
Durchgang** (`1C64B`: 4 mm Mittigkeit in 1250-mm-Durchgang; rechts/links/
beidseitig wurden im PDF explizit durchgespielt und VERWORFEN — S.73–74 =
dokumentierte Negativ-Beispiele). [2KG-04/09/15/18; PDF S.58–62, 73–74, 90–91]

## NB-R21 — SV-Anlage (mittel)
EIN Notbeleuchtungs-Stromversorgungssystem je Projekt, „meistens" auch bei
zwei Gebäudehälften (Verteiler im Niederspannungsraum, 1KG `1CB68`); der
Verteiler wird **nicht an die E-Verteiler-Wand** gesetzt (2KG `1D10E`/`1D10F`,
S.72). [1KG-09, 2KG-09; PDF S.51, 71–72]

**Ergänzungen zu bestehenden Regeln:** NB-R10 (Antipanik) — UG-Belege dazu:
abgeschatteter L-Schenkel → AP mittig über gelbe Diagonalen-Konstruktion
(2KG-02 `1D03D` trifft `1C707` auf 9 mm); AP als Lux-Stütze ist „sinnvoll",
kein Muss (2KG-03); Faustregel „Antipanik meist UG, Aufheller eher EG–OG"
(1KG-07, Fachpraxis). NB-R12 (Sichtkette) — UG-Distanzen: Folge 1550–9572 mm,
längste Einzelsichtlinie 7250 mm (2KG (C)). **Lichtberechnung** (S.83–84,
wörtlich als Anforderung): alle Stockwerke mit der Lichtberechnung prüfen —
die fachliche Platzierung ist die Basis, die Lux-Prüfung die Kontrollschicht
(→ Ground-Truth-Harness G3, keine Regel dieser Basis).

---

# Erweiterung 2026-09-20 (2) — Schul-Typologie + Flucht-/Rettungsplan-Lehren (TOMA 44)

**Andere Dokumentklasse als NB-R00–R21.** Quelle = `TOMA_Flucht- und
Rettungspläne.pdf` (bestehender Flucht-/Rettungsplan einer Volksschule, 10 S.)
+ 3 Architektur-Ausführungs-DXFs (SG/EG/OG). Vollabgleich:
`abgleich/TOMA44/` (referenz_{SG,EG,OG,DG}.md, inventar_*.json,
vergleich_*.png, engine_anforderungen.md). Diese Lehren betreffen Fluchtweg-
STRUKTUR / Gebäude-TYPOLOGIE / QUELLEN-Disziplin (v.a. Selman-Naht +
Quellen-Hierarchie) — sie sind KEINE Platzierungs-/Rotationsregeln und
übersteuern NB-R00–R21 NICHT. Symbol-/Rotations-Konventionen der
Mollgasse-Erklärung wurden NICHT auf diesen Flucht-/Rettungsplan übertragen.

## NB-R22 — Flucht-/Rettungsplan ≠ Notbeleuchtungsplan (Quellen-Disziplin, bindend)
Ein grüner Flucht-/Rettungsplan belegt Fluchtweg-Richtung, benutzte Türen,
Fluchtstiegenhäuser, Ausgänge und Orientierungspunkte — **NICHT** Montage-
position einer Notleuchte, Wand-/Deckenmontage, Frontseite, ein-/beidseitig,
Leuchtentyp, Lichtverteilung, Montagehöhe, Luxwert oder Leuchten-Anzahl. Ein
Richtungssymbol im Fluchtplan darf NIE als mm-genaue Leuchtenposition
übernommen werden; ein Raum OHNE grüne Markierung heißt nicht „keine
Notbeleuchtung nötig". Auch: eine Standort-Marke ist der Aushang-Bezugspunkt,
keine Leuchte. Blatt-Richtung ≠ CAD-Richtung ≠ Personen-Bewegungsrichtung
(gedrehte Aushang-Blätter; mehrere Blätter desselben Geschosses = EINE
Referenz). [TOMA S.1–10; Klassifikation: Quellen-/Prozessregel]

## NB-R23 — Schul-Bildungscluster: offener Bewegungsbereich = Fluchtweg (Referenzpraxis)
In Schulen der Cluster-/offene-Lernlandschaft-Typologie trägt ein OFFENER
„Kommunikations- und Bewegungsbereich" den Fluchtweg, auf den die
Unterrichtsräume direkt öffnen — OHNE „Gang"-Label. Fluchtweg-Erkennung darf
nicht am Raumtext „Gang" hängen (generalisiert NB-R20 von der Durchgangs-
auf die Cluster-Ebene). [TOMA OG-04 (Unterrichtsraum 1–4 → Kommunikations-/
Bewegungsbereich → TH 2); Klassifikation: Referenzpraxis, Schule]

## NB-R24 — Mehrere Fluchtstiegenhäuser, gerichtete Zuordnung (Referenzpraxis)
Bei mehreren Fluchtstiegenhäusern (TOMA: TH 2/3/4) werden Cluster/
Gebäudeteile GEZIELT verschiedenen THs zugeordnet — NICHT alle Personen zum
nächstgelegenen TH oder zu einem einzigen Hauptausgang. Wo mehrere Richtungen
dargestellt sind, bleiben sie erhalten. Deckt sich mit der Mollgasse-
Gebäudehälften-Regel (NB-R18): unklare Zuordnung nicht raten. Engine: THs als
getrennte Ziele + cluster-/gebäudeteil-basierte Zuordnung statt Global-
Nearest. [TOMA SG/EG/OG; Klassifikation: Referenzpraxis]

## NB-R25 — Egress je Ebene; Sockelgeschoss ≠ Keller (Referenzpraxis)
Ein Sockel-/Untergeschoss kann direkte Außenausgänge auf EIGENER Ebene haben;
Flucht muss nicht zwingend über das Erdgeschoss laufen. Ziel-Typen strikt
trennen und NIE gleichsetzen: Übergang ins Fluchtstiegenhaus / Ausgang ins
Freie / Balkon-Terrasse-Loggia / vorläufige Evakuierungsstelle / Sammelstelle.
(Ergänzt NB-R13 „UG flüchtet hinauf" um „UG kann auch direkt ins Freie".)
[TOMA SG: viele EN-Türen ins Freie auf Sockel-Ebene; Klassifikation:
Referenzpraxis]

## NB-R26 — Ausführungsplan-Annotationen als Erkennungs-Anker (Datenquelle)
Architektur-Ausführungspläne dieser Klasse tragen die Fluchtdaten als
Text-Annotation GEOMETRISCH — wertvollere Ausgangs-/Brandabschnitt-Anker als
reine Raumpolygone: **EN 1125** (Panikstange) / **EN 179** (Notausgangs-
beschlag) = echte Ausgangstüren · **FLn** = Fluchtweg-Fläche mit Soll-m²
(TOMA EG FL1–4 72/72/33/39 m², OG FL1 48) · **EI 30/90/230-C** +
„brandlastfreie Zone" + **BA** = Brandabschnitte · **RWA** = Rauch-Wärme-
Abzug · **BMZ** = Brandmeldezentrale. Diese Layer/Texte sind Erkennungs-
Eingänge (Selman-Naht). ⚠️ Daten-Fallen: INSUNITS kann LÜGEN (TOMA INSUNITS=6
Meter, real mm — Einheit über Türbreiten/Wandstärken verifizieren); DXF kann
einen Riesen-Koordinaten-Offset tragen (TOMA SG ~−1,7e9 → Healthcheck/Nullung
vor jedem Engine-Lauf). [TOMA SG/EG/OG; Klassifikation: Referenz/Datenquelle]

## NB-R27 — Aufzug ist keine vertikale Fluchtverbindung (Referenzpraxis, bestätigt Engine-Standard)
Standard-Aushang „Aufzug nicht benutzen" → ein Aufzug wird NIE als vertikale
Flucht-Kante ins Wegenetz übernommen; der Aufzugsvorbereich ist getrennt zu
behandeln (kann Teil des Gangs sein). Deckt sich mit dem bestehenden
LIFT-Guard (`fachpraxis.entferne_schacht_leuchten`). [TOMA S.1–10 Brandfall-
Hinweis; Klassifikation: Referenzpraxis]

## Integration (Vorschlag — NICHT umgesetzt, Phase-B-Grenze)
- NB-R01/R03 decken sich weitgehend mit R-B/R-C/`rotation_piktogramm_in_raum` +
  `_RZ_INS_RAUM_MM=150` — ABER die Owner-Messwerte sagen 735–930 mm raumseitig:
  Kalibrierfrage an den Owner (150 vs. ~800 mm), dann `bausteine.RZ_INS_RAUM_MM`.
- NB-R05 (800–1120 mm vor der Stiege, Pfeil=Laufrichtung) gehört in
  `stgh_strategy`/R8 (heute Zentrum-Approximation bzw. `fluchtvektor`).
- NB-R06 **UMGESETZT 2026-09-20** (`710b859`, Owner-GO „alle PDF-Regeln"):
  gerade Gang-Zwischen-RZ = down-Typ, Welt-Pfeil ENTGEGEN der Flucht (Front zur
  ankommenden Person) via `gang_strategy` + `rotation_piktogramm_in_raum`; alter
  „Pfeil-zum-Ausgang"-Test/Gang-Fallback-Test begründet nachgezogen.
- NB-R07 **UMGESETZT 2026-09-20** (`710b859`): Abzweige (`_ist_abzweig` >45°)
  behalten den Richtungspfeil (links/rechts zeigt den Weg), gerade Fortsetzung
  fällt auf NB-R06 (down-Typ, Front zur Person).
- NB-R08 entspricht `sichtkette`/`_sichtlinien_garantie` — Parameter (eine
  Sichtlinie je Wohnungstür, Zusatz-RZ bei Distanz) präzisieren.
- NB-R09-Alternativen als LB-/Owner-Parameter (`gang_grundbeleuchtung`:
  antipanik|aufheller|rz_unten|rz_plus_aufheller).
- NB-R11 als Erweiterung von `verbotszonen_nachpass` (Hindernis-Polygone,
  Versatz statt Entfall — Selman-Naht: Lichtkuppel-Erkennung).
- **NB-R13** → `stgh_strategy` (UG-Zweig: `Treppenlauf.richtung` „auf" =
  Fluchtrichtung im UG; heute nur OG-Semantik kalibriert).
- **NB-R15** → Kabeltrassen-Extraktion aus dem Quell-DXF (Muster
  `bestand_leuchten.py`) + Versatz-Nachpass (Muster `abstand_nachpass`);
  450 mm als benannte FACHPRAXIS-Konstante mit Quelle-Tag, kein Norm-Claim.
- NB-R16 **UMGESETZT 2026-09-20** (`f6c69d0`): Wasserscheiden-Erkennung im
  aktiven Anker-Pfad (`_wasserscheide_achse` + `graph.distanz_je_ausgang`) —
  Kreuzung gleich weit zu zwei Ausgängen in Gegenrichtung → `richtung="gerade"`
  → Bothsided-Block; konservativ (nur Pflicht, keine Alternativen).
- **NB-R17** → hängt an Selmans Garage-Erkennung (Stellplatz-Stempel /
  freie Flächen) — bis dahin Gap.
- **NB-R18** → Gebäudehälften über Zirkulations-Graph-Komponenten
  (disconnected-graph-Anker existiert); wenn das RaumModell die Trennung
  nicht hergibt: Gap dokumentieren, NICHT raten (Prozessregel S.78).
- **NB-R19** → `tuerleuchte_pflichtraeume`/`fachpraxis` (TECHNIK ja,
  einzelne KELLERABTEIL/kleine Medienräume nein bei sofortiger Gang-Sicht).
- **NB-R20** → `sichtkette`/`_tuer_luecken_rz` (türlos = keine Zwischen-RZ)
  + Durchgangs-Knoten mittig (anker/gang).
- NB-R14 **UMGESETZT 2026-09-20** (`09db956`): `Platzierung.montage_art`
  (bestehendes Feld, war unbenutzt — KEIN Contract-Change) befüllt: Stiegen-/
  Tür-/Ausgangs-/Außen-RZ = `WA` (Wand), Gang-/Aufheller-/Antipanik-/Flächen-
  Leuchten = `DA` (Decke); Decke-Default-Nachpass im `platzierer` fängt den Rest.
  Die POSITION (Gang-Mitte vs. Stiegen-Wand) war geometrisch schon realisiert.
- **NB-R22** = Quellen-Disziplin (kein Code): Flucht-/Rettungsplan nie als
  Leuchten-Ground-Truth behandeln (nur Fluchtweg-Struktur). Neue Klasse
  „Schule" ist noch NIE durch die Engine gelaufen → Healthcheck vor Render.
- **NB-R23** → Selman: offene Cluster-/Bewegungsbereiche als Fluchtweg
  erkennen (nicht am „Gang"-Text hängen); Leonis konsumiert wie GANG.
- **NB-R24** → Mehr-TH-Zuordnung gerichtet (Cluster→TH statt Nearest) —
  hängt an Selmans Cluster-/Gebäudeteil-Zuordnung; = TOMA-Variante der
  NB-R18-Gebäudehälften.
- **NB-R25** → Ausgangs-/Ziel-Typen im Contract sauber unterscheiden
  (final_exit/stair_exit/Balkon/Evakuierungsstelle/Sammelstelle); Egress je
  Ebene zulassen (nicht zwingend über EG).
- **NB-R26** → Selman-Erkennungs-Eingänge: EN-1125/179-Türen, FLn-Flächen,
  EI-Brandabschnitte, RWA/BMZ aus den Ausführungs-Layern; Einheiten-Verify
  (INSUNITS lügt) + Offset-Healing als Healthcheck-Vorstufe.
- **NB-R27** = bereits erfüllt (LIFT-Guard) — als Referenz bestätigt.
