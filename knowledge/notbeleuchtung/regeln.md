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

## Integration (Vorschlag — NICHT umgesetzt, Phase-B-Grenze)
- NB-R01/R03 decken sich weitgehend mit R-B/R-C/`rotation_piktogramm_in_raum` +
  `_RZ_INS_RAUM_MM=150` — ABER die Owner-Messwerte sagen 735–930 mm raumseitig:
  Kalibrierfrage an den Owner (150 vs. ~800 mm), dann `bausteine.RZ_INS_RAUM_MM`.
- NB-R05 (800–1120 mm vor der Stiege, Pfeil=Laufrichtung) gehört in
  `stgh_strategy`/R8 (heute Zentrum-Approximation bzw. `fluchtvektor`).
- NB-R06 (Welt-Pfeil entgegen Fluchtrichtung bei down-RZ) widerspricht ggf.
  dem heutigen „Pfeil in Fluchtrichtung"-Verständnis einzelner Sites — vor
  Umsetzung Owner-Review der betroffenen Call-Sites (D3-Runde).
- NB-R07 (Frontalsicht) wäre ein neues Auswahl-Kriterium in
  `bausteine.key_und_rotation` (Blick-Korridor der ankommenden Person).
- NB-R08 entspricht `sichtkette`/`_sichtlinien_garantie` — Parameter (eine
  Sichtlinie je Wohnungstür, Zusatz-RZ bei Distanz) präzisieren.
- NB-R09-Alternativen als LB-/Owner-Parameter (`gang_grundbeleuchtung`:
  antipanik|aufheller|rz_unten|rz_plus_aufheller).
- NB-R11 als Erweiterung von `verbotszonen_nachpass` (Hindernis-Polygone,
  Versatz statt Entfall — Selman-Naht: Lichtkuppel-Erkennung).
