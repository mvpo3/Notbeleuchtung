# Notbeleuchtung zeichnen lernen — Owner-Fachdoku (AUTORITATIV)

**Quelle:** `knowledge/sonstiges Wissen Notbeleuchtung/Notbeleuchtung zeichnen lernen.pdf`
(Owner-erstellt, Stand v2 2026-09-12, 12 Seiten; Grundriss-Abbildungen sind autoritativ,
Referenzgebäude = Elektroplan DE EG/1OG). Erster Stand — Owner kündigt weitere
Beispiele an. Ground-Truth-DXF:
`Projektbeispiele-demo-Platzierungslogik/nachgezeichnet_out/v5/{EG,1OG}_notbeleuchtung_korrigiert.dxf`
(Lehrdateien: enthalten Engine-v5-Stand als um −46.324 m x-verschobene „Vorher"-Kopie
+ Owner-Korrektur an Originalkoordinaten mit Owner-eigenen Blockdefinitionen).

Geltung: **Referenz-Praxis** (Owner-Vorgabe für die Platzierungslogik). Norm-Referenzen
je Regel sind in der PDF ausdrücklich als „Track B" (Enis) offen markiert.

## R-A — Schritt 1: Fluchtwegstruktur vor jeder Platzierung (S.1–2)
Erst Gänge / Stiegenhäuser / Schlussausgänge + angeschlossene Räume erfassen
(= RaumModell), dann platzieren. Geschossweise, EG zuerst (dort enden alle Fluchtwege).
Offen (Owner-Fragen an sich selbst): Aufzug-Vorbereich (→Track B), Fluchtweg-Beginn an
der Wohnungstür, Geschoss-Reihenfolge nach EG.

## R-B — Tür-RZ: Rotation „Piktogramm ins Rauminnere" (S.3–5, ZENTRAL, ausnahmslos)
Jede Pfeil-unten-RZ an einer Tür wird so rotiert, dass das **Piktogramm in den Raum
hineinschaut** — die flüchtende Person ist im Raum und muss es lesen. Blickrichtung =
**Gegenrichtung zur Fluchtachse durch die Tür**. Gilt unabhängig von Raumtyp, Türziel
(Gang/Freies) und Türaufschlag. ⚠️ Frühere Merkregel „entgegen der Türöffnungsrichtung"
ist **NICHT das Kriterium** (kann falsch werden). Implementierung lt. PDF: Wandkanten-
Normale an der Tür, Vorzeichen ins Rauminnere (Achse wie `_wand_normale` in
`aussen_strategy.py`, Commit `c61dd55`, Vorzeichen invers).

## R-C — Tür-RZ: Position raumseitig (S.3, S.5)
RZ „bei der Tür, **innerhalb des Raums** über bzw. neben der Türöffnung". Referenz-Maße
aus Ground-Truth-DXF: Nebenraum ~176 mm, Hauseingang ~420 mm raumseitig der Tür-
Station (kleine Wand-Offsets, kein Normmaß).

## R-D — Nebenräume mit einer Fluchttür (S.3): NIEDERSP=Technik, Fahrradraum, Müllraum
RZ Pfeil-unten an der Tür nach R-B/R-C. Kontext ohne Rotations-Einfluss: Technik/Fahrrad
→ Tür in den Gang; **Müllraum → eigener Ausgang direkt ins Freie** (Müllabfuhr-
Erschließung) → RZ an der Außentür (Ground truth EG: 2884296/1730460, Südtür).
Gilt geschossunabhängig auch im OG (Hausbetreuung, Spielraum genauso).

## R-E — Außenbereich am Schlussausgang: DREIFALL (S.5–6, Owner-Antworten 2026-09-12)
| Situation draußen | Maßnahme |
|---|---|
| Überdachung vorhanden | Antipanikleuchte **mittig in der Überdachungsfläche**, auf derselben Achse wie die Tür-RZ (senkrecht zur Türebene). Position aus der Überdachungs-GEOMETRIE, **kein fester Abstand zur Tür**. Grund: überdachter Bereich bekommt nachts kein Außenlicht, gehört aber zum Fluchtweg. |
| Keine Überdachung, Flucht draußen nur in EINE Richtung (Sackgasse/versperrte Seite) | Antipanikleuchte an der **Außenwand seitlich neben der Tür auf der NUTZBAREN Seite** (rechts versperrt → links, und umgekehrt). Leuchte symbolisiert die Wenderichtung. Seltener Fall. |
| Keine Überdachung, Flucht in beide Richtungen möglich | **KEINE Außenleuchte notwendig** (Owner-Antwort 5). |
⚠️ Ersetzt die pauschale 1-m-vor-der-Tür-Regel (EN 1838 §4.1.2 b bleibt der Anlass,
die AUSFÜHRUNG folgt dem Dreifall). Sackgassen-Bedingung steht NICHT im Grundriss-DXF
(Lageplan/Ortskenntnis; erkennbar in großen Plänen wie din V25) → kein Automatismus,
Eingabe/Owner-Review (Owner-Antwort 6).

## R-F — Gang/Stiegenhaus: RZ-Kette entlang der SICHTLINIE (S.7–9)
RZ werden nicht nach festem Abstand gesetzt, sondern als **lückenlose Sichtkette**: von
jedem Punkt des Fluchtwegs ≥1 RZ sichtbar; von RZ (A) muss das nächste RZ (B) sichtbar
sein. **Ein zusätzliches RZ nur, wenn die Kette sonst abreißt** — Sichtbarkeit ersetzt
Zeichen (Wohnungstüren: kein eigenes RZ, wenn RZ (B) direkt sichtbar). Gang-RZ (A):
„im Gang, in einer Linie mit den übrigen Leuchten, zwischen ihnen" (Bestands-Lichtlinie,
Spot-Lückenmitte). Sichtbarkeits-Berechnung: freie Sichtlinie ohne Wandschnitt +
Erkennungsweite nach Norm (→ Track A Geometrie / Track B Normwert).
**Glastür/Trennelement zählt als Sichtunterbrechung** (Owner: „JA sie zählt").

## R-G — Leuchtentyp folgt aus der POSITION, nicht aus der Fluchtrichtung (S.11–12)
Position an Tür/Durchgang? ja → **Pfeil nach unten** („hier durch"), Piktogramm ins
Rauminnere. nein (im Verlauf des Fluchtwegs) → **Richtungspfeil** entlang der
Fluchtachse („weiter in diese Richtung"). RZ-Paar am Übergang Gang→STGH: (A) Pfeil-unten
an der Tür + (D) Richtungspfeil im STGH nach dem Durchtritt. ⚠️ Korrektur zur früheren
Fassung: (A) war Richtungspfeil, ist jetzt Pfeil-unten (allgemeine Türregel greift).

## R-H — Stiegenhaus: Laufrichtung ermitteln (S.7, S.10)
Vor der Platzierung Laufrichtung der Stiege bestimmen (Referenz: EG→1.OG im
Uhrzeigersinn; Fluchtrichtung 1.OG→EG gegen den Uhrzeigersinn). Sie bestimmt die
Blickrichtung beim Austritt → Position des ersten Gang-RZ bzw. Pfeilrichtung des
STGH-RZ (1OG-Variante: RZ an der STGH-Wand, Pfeil in Weitergeh-Richtung). Maschinelle
Ableitung: Contract kennt `Treppenlauf.richtung` (v1.2.0), am 02-TWA-Dialekt liefert
die Erkennung aber nichts → Selman-Naht (COORDINATION 2026-09-12 (c)).

## R-I — 2D-Artefakt Pfeil-unten (S.8–9, S.11)
Real hängt die RZ an der Decke, Pfeil zeigt zum BODEN; im 2D-Plan ist Abwärts nicht
darstellbar → Blockrotation ist Darstellung, **keine Gehrichtung**. Ein Prüflauf, der
die Pfeilrichtung als Gehrichtung bewertet und Fehler meldet, liegt falsch.

## R-J — Aufheller: Entscheidung durch LICHTBERECHNUNG (S.10–11)
Ob ein Aufheller erforderlich ist, entscheidet **nicht die Platzierungsregel, sondern
die Lichtberechnung**: erreicht der Fluchtweg die geforderte Beleuchtungsstärke ohne
ihn, entfällt er. Architektur-Abgrenzung: **Rettungszeichen → Platzierungsregeln
(Sichtlinie, Türlogik) · Aufheller/Sicherheitsleuchten → Ergebnis der Lichtberechnung.**
Ground truth EG: Gang-Aufheller 5→1 (übrig: Spot-Lückenmitte 2880881/1735829).

## R-K — OG-Planumfang (S.9–10)
Nicht jedes OG braucht einen eigenen Plan; Kriterium = EINDEUTIGKEIT des Fluchtwegs.
Kein Plan nötig: 1 STGH + gerader Gang in eine Richtung. Eigener Plan: Fluchtweg nicht
auf einen Blick (L-Gang, Sichtabbruch an Ecke, trennende Bauteile/Glastür).
**Status lt. PDF: Orientierung, NICHT implementierbare Regel** → Hard-Stop,
Entscheidung beim Owner. 1OG-Regeln gelten für alle weiteren OGs.

## Offene Punkte → Handoff
**Enis (Track B):** Montagehöhe/Bezug Türoberkante · Norm-Referenz je Regel ·
Erkennungsweite je Piktogrammgröße · Abstand von der Türlaibung · Aufzug-Vorbereich ·
Sichtweiten-Normwert der Kette. **Selman (Track C):** Überdachungs-Polygon im DXF
(eigener Layer/Schraffur/Polygon ohne Raum) · Stiegen-Laufrichtung maschinell ·
„mittig" bei unregelmäßiger Überdachung (Schwerpunkt vs. Bbox-Mitte, Owner tendiert
Geometrie). **Owner:** Sackgassen-Kennzeichnung (manuell im Plan / Parameter je
Ausgang / Review).

## Abgleich mit bestehendem Wissen
- Ersetzt/präzisiert: „RZ an Tür, Pfeil DURCH die Tür" (rz-tuer-regel, #111) → Rotation
  jetzt über Piktogramm-Blick INS Rauminnere; Pfeil-unten-Rotation ist Darstellung (R-I).
- Bestätigt: R1/R6 (Bestandslinie + Spot-Lückenmitte), R7 (Wohnungs-Vorräume ohne RZ =
  Sichtbarkeits-Prinzip), Türleuchten-Scope communal Nebenräume (R3/R5).
- Kein Widerspruch zu EN-1838-Werten (Lux/Erkennungsweite bleiben Enis' YAML).
