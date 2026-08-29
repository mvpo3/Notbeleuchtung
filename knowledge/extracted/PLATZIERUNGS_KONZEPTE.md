# Platzierungs-Konzepte — die Denkweise hinter der Norm (Engine-Synthese)

**Zweck:** Nicht *was* die Normen sagen (das steht in den Digests + Regel-Tabellen),
sondern *wie ein Planer denkt* — das mentale Modell, das die Platzierungs-Engine
nachbilden muss. Synthetisiert aus der **visuellen** Analyse (Bild-Lehren, Ordner
`bildlehren/`) von EN 1838, OVE-Fachinfo E-08, Zumtobel-AT, INOTEC 2026, GSYSTEMS
2026/27, ABB Kaufel + den Text-Digests. Wo 5–6 unabhängige Quellen dasselbe Muster
zeigen, ist es als **[KONVERGENT]** markiert — das sind die belastbaren Engine-Regeln.

**Hierarchie-Erinnerung (CLAUDE.md):** LB-explizit → Referenz-Praxis → EN-1838/ÖNorm
→ OVE-Verbote (Hard Stop). AT-Rangfolge: OVE E 8101 + OIB-RL 2 + AStV vor DE-Quellen
(DIN VDE 0108, ASR, MLAR = DE-only, markiert).

---

## Die zentrale Erkenntnis: Platzierung ist Graph-Logik, kein Raster

**[KONVERGENT — alle 6 Quellen]** Jeder Profi-Beispielplan (GSYSTEMS S.182–185,
Zumtobel S.31, INOTEC S.44–62, Kaufel Abb. 11–20) platziert Leuchten **nicht** in
einem gleichmäßigen Deckenraster, sondern in drei Schichten:

```
1. ANKER  — Pflichtpunkte an Architektur-/Objekt-Knoten (diskret, „hervorzuhebende Stellen")
2. LINIE  — Verdichtung entlang der Fluchtweg-Mittelachse, bis Lux + Gleichmäßigkeit halten
3. FLÄCHE — Antipanik-Füllung großer Räume (Kern, Rand ausgenommen)
```

Die Engine arbeitet also **auf Selmans Zirkulationsgraph** (Segmente = Wegachsen,
Knoten = Türen/Kreuzungen/Treppen), nicht auf der Rohfläche. Das deckt sich exakt
mit dem bestehenden Contract: `RaumModell.zirkulation.segmente[].polyline_mm` ist
die Wegachse, `covers_segment` verankert jede Platzierung daran.

---

## Schicht 1 — Anker: der universelle „hervorzuhebende Stelle"-Constraint

**[KONVERGENT]** Alle Quellen reduzieren die lange §4.2-Pflichtliste auf **einen
einzigen Constraint-Typ**, nur parametrisiert:

```
Anker = (position, max_horizontal=2.0 m, lux_zusatz ∈ {None, 5 lx}, mess_ebene ∈ {boden, vertikal}, zeichen?)
```

- **„nahe" = ≤ 2,0 m horizontaler Abstand** — die eine Zahl, die in *jeder* Quelle
  identisch auftaucht (EN 1838 §definiert, INOTEC-Fußnote auf jeder Seite,
  Zumtobel S.31, Kaufel, GSYSTEMS S.180). Harter Platzierungsradius.
- **Montagehöhe Leuchten ≥ 2,0 m** über Boden (alle).
- **„bei Kreuzung/Richtungsänderung" = beide Richtungen ausleuchten** (EN 1838
  §4.2, Zumtobel-Fußnote **, Kaufel Abb. 14).

### Die Anker-Punktliste (aus RaumModell ableitbar)

| Anker | Quelle im RaumModell | lux_zusatz | Besonderheit |
|-------|----------------------|-----------|--------------|
| Jede benutzte Ausgangstür | `tueren[ist_notausgang]`, `ausgaenge` | 1 lx | RZ **an/über** Tür + SL **≤ 2 m davor** = ZWEI Anker |
| Letzter Ausgang **+ außen** | `ausgaenge[typ=final_exit]` | 1 lx | zusätzliche Leuchte **außerhalb** der Gebäudehülle bis zum sicheren Bereich [KONVERGENT] |
| Treppe (jede Stufe direkt) | `segmente[reason]`, Niveauänderung | 1 lx | **Direktlicht-/Sichtlinien**-Bedingung, nicht nur Abstand; Leuchte **oberhalb** des Laufs, Kegel über alle Stufen |
| Niveauänderung | `segmente` | 1 lx | löst Vollkreis-Blendmodus aus (s.u.) |
| Richtungsänderung / Kreuzung | Graph-Knoten (Grad ≥ 3 oder Winkel) | 1 lx | Leuchte auf Achsen-Schnittpunkt, RZ quer/mehrseitig |
| Erste-Hilfe-Stelle | (LB/Objektlage) | **5 lx vertikal** | Leuchte direkt über dem Objekt |
| Brandbekämpfung / BMA / Melder | (LB/Objektlage) | **5 lx vertikal** | dito |
| Behinderten-Einrichtung / barrierefreies WC | `raeume[raum_typ]` | 1 lx + Antipanik | + 2-Wege-Kommunikation/Alarm |

**[EN 1838:2025 — NEU, via INOTEC/GSYSTEMS]** Zusatz-Anker der aktuellen Ausgabe:
Aufzugsflure (bis zum nächsten Rettungsweg), manuelle Türentriegelung (5 lx **am
Bedienelement**, vertikal), Flucht-/Rettungspläne (5 lx), Hauptverteiler Allgemein-/
SiBe (5 lx), Technik-/Betriebsräume (0,5 lx flächig / 5 lx an Schalttafeln),
Hallenbäder (5 lx auf **Wasserfläche** — Nachweisfläche ≠ Montagefläche, Leuchten am
Beckenumgang), Toiletten nach Raumtyp (0,5/1 lx). **Versions-Delta:** unser
EN-1838-PDF ist 2019, aber alle NEU-Stellen sind im Repo mit Seiten-Refs belegt →
`Handbuch_NotSicherheitsbeleuchtung_2026.md` (HB2026-R39…R45, DIN EN 1838:2025-03
§4.2/5.4). Sekundärquelle (INOTEC-Hersteller-Handbuch) — nie alleinige `norm_quelle`,
aber die 2025er-Werte sind damit belastbar erfasst.

**Lehre:** Schild (RZ) und Leuchte (SL) sind an einer Tür **getrennte Anker** mit
getrennten Regeln — im Datenmodell nicht vermischen. RZ = „so nah wie möglich an/über
der Tür" (Sichtbarkeitskriterium), SL = „erste Leuchte ≤ 2 m davor" (Abstandskriterium).

---

## Schicht 2 — Linie: Ausleuchtung als Geometrie-Operation

**Wichtige Erkenntnis mit Versions-Bruch:**

- **EN 1838:2019 (unser Repo-Stand)** denkt den Rettungsweg als **Mittellinie**:
  ≥ 1 lx entlang der Mittellinie (Weg ≤ 2 m), zentrierter Streifen halber Breite
  ≥ 0,5 lx, U_d = E_min:E_max ≥ 1:40. Breite Wege → in 2-m-Streifen zerlegen oder
  Antipanik. (Kein Norm-Bild dazu — reiner Text, visuell bestätigt.)
- **EN 1838:2025 (INOTEC S.61 / GSYSTEMS S.176)** wechselt zu **flächendeckend ≥ 1 lx**:
  Nachweisfläche = Fluchtweg-Polygon mit **seitlichem Innen-Offset −c** (c = 0,5 m bei
  Breite a > 2 m; c = 0,25·a bei a ≤ 2 m), **kein** Rückschnitt an Anfang/Ende (läuft
  bis an die Türen). Antipanik-Durchgangswege dagegen: Band ≥ 2 m mit 1 lx, an Enden
  0,5 m ausgenommen.

**Lehre für die Engine (beide Versionen abbildbar):** Ausleuchtungs-Nachweis =
**Polygon-Offset-Operation** auf dem Wegsegment. Solange keine Photometrie-Engine
existiert, gilt der Praxis-Ersatz **[KONVERGENT INOTEC/GSYSTEMS/Kaufel]**:
Hersteller-**Abstandstabellen** je Leuchte, Referenz-Wegbreite 2,0 m, projektiert auf
**1,25 lx** (Wartungsfaktor 0,8 → Neuwert-Aufschlag). Bis 2025er-Original vorliegt:
konservativ mit der Mittellinien-Regel (2019) rechnen.

### Zwei unabhängige Abstands-Limits [KONVERGENT Kaufel/GSYSTEMS/Zumtobel]

Der Leuchtenabstand entlang der Achse wird durch **zwei** Bedingungen begrenzt:
1. **Photometrie**: max. Abstand aus der Katalog-Abstandstabelle (1-lx-Kriterium).
2. **Gleichmäßigkeit 1:40**: E_min (in der Kegel-**Naht** mittig zwischen zwei Leuchten)
   zu E_max (direkt unter der Leuchte, ≤ 40 lx bei Mindestwert 1 lx). Der Naht-Punkt
   ist der Prüfpunkt der Engine.

### Abstandstabellen sind Lookups, NIE Formeln [KONVERGENT — kritisch]

Kaufel S.78 (per Zoom verifiziert): die h→Abstand-Werte sind **nicht monoton**
(Optik D: h=3,5 m → 4,1 m Randabstand, h=4,0 m → 1,4 m, ab h=5,0 m **unzulässig/leere
Zelle**). ⇒ Die Engine muss je `catalog_key` + Optik + Montageart eine diskrete
h→(rand, folge)-Tabelle vorhalten und **strikt auf der 0,5-m-Stufe nachschlagen —
niemals interpolieren/extrapolieren**; leere Zelle = Leuchte für diese Höhe unzulässig.
(Diese Tabellen liegen NICHT im Repo — Datenlücke, herstellerspezifisch.)

---

## Schicht 3 — Fläche: Antipanik-Zerlegung

**[KONVERGENT GSYSTEMS S.184/185, Zumtobel S.34, INOTEC S.62]** Großraum (Schwelle
> 60 m², DE-Vornorm-Wert / AT via R 12-2 Raumtypen) zerfällt in zwei Klassen:

- **mit ausgewiesenem Weg** (bestuhlte Halle): Wegenetz = 1,0 lx (wie Flur),
  Restflächen/Bestuhlung = 0,5 lx Antipanik. Die Engine subtrahiert Einrichtungs-/
  Bestuhlungsflächen vom Weggraph und behandelt sie als Antipanik-Zonen.
- **ohne ausgewiesenen Weg**: Kernfläche gleichmäßig ≥ 0,5 lx (Deckenleuchten im
  ~Drittel-Raster), **umlaufender Randbereich 0,5 m ausgenommen**, Ausgänge müssen
  erreichbar/erkennbar bleiben.

Antipanik-Leuchte sitzt **raummittig**, nicht türnah (die Tür hat ihre Leuchte schon
über die Anker-Regel).

---

## Blendung: Winkelzonen-Prüfung mit Topologie-Schalter [KONVERGENT EN/Kaufel/Zumtobel]

Die EN-1838-Bilder 2/3 (visuell erfasst) zeigen **zwei Modi**, umgeschaltet durch die
Weg-Topologie:

- **Horizontaler Weg** → I_max-Grenze (Tabelle 1) gilt nur im Kegelband
  **γ ∈ [60°, 90°] gegen die Leuchten-Vertikale**, für alle Azimute. Darunter frei.
- **Treppe / Rampe / Niveauänderung / jede Fläche** → I_max gilt in **allen** Winkeln
  (Vollkugel). Das „60°–90°" darf dort NICHT angewendet werden.

⇒ Das RaumModell muss pro Segment ein Flag **horizontal vs. niveauändernd** liefern.
Grenzwert-Zeile wählt die **Montagehöhe** (I_max steigt mit h; Arbeitsplatz-Spalte =
exakt 2× Rettungsweg-Spalte):

| h (m) | I_max Rettungsweg/Antipanik | I_max Arbeitsplatz bes. Gefährdung |
|-------|----------------------------|-----------------------------------|
| < 2,5 | 500 cd | 1 000 cd |
| 2,5–3,0 | 900 | 1 800 |
| 3,0–3,5 | 1 600 | 3 200 |
| 3,5–4,0 | 2 500 | 5 000 |
| 4,0–4,5 | 3 500 | 7 000 |
| ≥ 4,5 | 5 000 | 10 000 |

---

## Rettungszeichen: Sichtbarkeit als Radius-Deckungsproblem [KONVERGENT alle]

- **Erkennungsweite l = z · h** mit h = **Piktogrammhöhe** (nicht Montagehöhe!),
  z = 100 (beleuchtet) / 200 (hinterleuchtet) / 300 (Schriftzeichen). Hinterleuchtet =
  Default (doppelte Weite); ein nur beleuchtetes Schild braucht bei gleicher Weite die
  **doppelte Baugröße** und eine eigene Dauerlicht-Leuchte (+1 Leuchte).
  Bedingungen (EN 1838:2025): z=100 nur bei ≥ 50 lx auf dem Zeichen; z=200 nur bei
  ≥ 500 cd/m². Praxis-Default in Projektierung: **z = 200** (INOTEC S.150).
- **Deckungsregel:** von **jedem Punkt** des Fluchtwegs muss ≥ 1 RZ innerhalb seines
  l-Radius **und in Sichtlinie** (keine Wand dazwischen) liegen. Kein direkter
  Sichtkontakt zum Notausgang ⇒ zusätzliche Richtungszeichen einketten (EN 1838 §4.1.1).
- **Montagehöhe ↔ Erkennungsweite als Constraint-Paar** (GSYSTEMS S.165, exakt bemaßt):
  Zeichen ≤ 20° über Blickhöhe 1,5 m ⇒ **h_montage ≤ 1,5 + tan(20°)·l ≈ 1,5 + 0,364·l**.
  Umgekehrt: hohe Montage begrenzt die nutzbare Weite.
- **Höhenbänder** (Fußboden → **Unterkante** Zeichen): EN 1838 quer/über Tür 2,0–3,0 m
  (2025: 2–3 m); ASR (DE-only) Wandschild 1,7–2,0 m, RZ-Leuchte 2,0–2,5 m; barrierefrei
  1,2–1,4 m **neben** (nicht über) der Tür, ergänzend. RZ **nicht auf Türblättern**,
  nicht auf Zwischenpodesten; im Treppenraum **1 RZ je Etage** nach dem Zugang, Pfeil =
  Laufrichtung.
- **Pfeil-Semantik** (GSYSTEMS S.170) ist ein Lookup aus (Zeichenposition rel. Tür/
  Treppe, Fluchtrichtung, Etagenwechsel). Gebäudeweite **Einheitlichkeit** des Pfeilstils
  ist Pflicht (Konsistenz-Check über alle RZ).

---

## Systemintegrität: die harte Nachbedingung [KONVERGENT alle]

**Je Bereich/Fluchtweg ≥ 2 Leuchten** — Einzelausfall darf den Rettungsweg nie
verdunkeln. Ausnahme: Bereich < 8 m² mit hinterleuchtetem RZ. Kombileuchten (RZ+SL in
einem Gehäuse) zählen **nicht** für die Fluchtweg-Ausleuchtung (EN 1838 §5.1.8).

Daraus folgt die **Stromkreis-Alternierung** (INOTEC S.79, GSYSTEMS S.141, Kaufel,
Zumtobel S.14): Leuchten eines Segments abwechselnd auf Kreis A/B/A/B entlang der
Weg-Topologie, **RZ-Leuchten eingeschlossen**. Fällt ein Kreis aus, bleibt je Weg
mindestens eine Kennzeichnung + jede zweite Ausleuchtung aktiv.

Elektro-Constraints (für spätere Slices; AT-Werte via OVE E 8101 §560.9):
≥ 2 Kreise je Brandabschnitt · ≤ 20 Leuchten/Endstromkreis bei ≤ 60 % Nennstrom des
Schutzorgans · > 20 Leuchten/Gebäudeteil → automatische Prüfeinrichtung (EN 62034) ·
jede Leuchte trägt Verteiler/Stromkreis/Leuchten-Nummer (Ø-30-mm-Schild, §560.9.15).

---

## Der Vor-Filter: WANN überhaupt platzieren?

Bevor Geometrie greift, entscheidet die **Erforderlichkeit** je Raum/Gebäude:

- **AStV §9 (AT-Arbeitsstätten, Fachinfo E-08)** — Entscheidungsmatrix Raumfläche
  (30/100/1600 m²) × natürliche Belichtung: ohne Tageslicht ab 30 m² Pflicht, mit
  Tageslicht erst > 1600 m²; besondere Gefährdung → immer (dort keine nachleuchtende
  Substitution). Wegbudgets: ≤ 10 m bis zum Fluchtweg, i.d.R. ≤ 40 m gesamt.
- **OIB-RL 2 + OVE R 12-2 (AT-Gebäude, Zumtobel S.28/29)** — **zweistufige
  Erforderlichkeit** je Gebäudetyp: „eingeschränkt" (nur Fluchtwege, 1 h) vs.
  „uneingeschränkt/erhöht" (ganzes Gebäude, 3 h; 8 h Beherbergung > 100 Betten /
  Pflege > 16 Betten). Kennzahl (m²/Betten/Personen/Fluchtniveau) schaltet um.
  → Engine-Modell: `gebaeudetyp + kennzahl → {umfang, betriebsdauer, zulässige Stromquelle}`.

Das ist der klassische Punkt, den die **LB projektspezifisch übersteuert**.

---

## Was die Engine ausgeben muss (normativ definierter Output)

**[KONVERGENT Zumtobel S.46, INOTEC, EN 50172]** Der Auslassplan ist normativ
vorgeschrieben mit: Lage **aller** Sicherheitseinrichtungen, **Endstromkreis­bezeichnung
+ Verbraucherleistung** je Leuchte, Verteiler-/Betriebsstätten-Lage. ⇒ Der DXF/PDF-
Output der Engine muss Stromkreis-Attribute tragen. Das legt eine künftige Contract-B-
Erweiterung nahe (`circuit_hint` existiert bereits als Keim; ergänzbar um
Verteiler/Leuchtennummer/Leistung).

---

## Algorithmus-Skizze für Leonis' Platzierer (Ziel-Architektur)

```
1. VOR-FILTER  je Raum: erforderlich? (AStV-Matrix / OIB-R12-2 + LB)  → sonst skip
2. ANKER       Pflichtpunkte aus Graph besetzen (Türen, Treppen, Kreuzungen,
               Niveauänderungen, letzter Ausgang+außen, 5-lx-Objekte, Raumtyp-Trigger)
               je Anker: RZ- und/oder SL-Platzierung, ≤ 2 m, Höhe ≥ 2 m
3. LINIE       Segmente zwischen Ankern mit SL auffüllen bis Abstandstabelle (1 lx)
               UND 1:40-Naht-Prüfung halten
4. FLÄCHE      Räume > 60 m² / Antipanik-Typen: Kern 0,5 lx (Rand 0,5 m frei),
               Wegenetz 1 lx
5. RZ-DECKUNG  Sichtbarkeits-Radien l=z·h + Sichtlinien-Check; Lücken → Richtungszeichen
6. CHECKS      Blendung (Winkelmodus je Topologie), Montagehöhe↔Weite, Systemintegrität ≥2,
               Pfeil-Einheitlichkeit
7. E-TOPOLOGIE (späterer Slice) Stromkreis-Alternierung A/B, ≤20/Kreis, Nummerierung
8. HARD STOPS  OVE-E-8101-Verbote prüfen (keine Platzierung in verbotenen Trassen etc.)
```

**Verbindung zum bestehenden Code:** Schritt 2–5 operieren auf
`RaumModell.zirkulation` + `raeume`; jede Platzierung füllt `covers_segment`,
`kind`, `richtung`, `norm_quelle` (Regel-ID aus den Digests, z.B. `EN1838-R…`).
Der heutige `NotlichtPlatzierer` (Slice 2, generativ) macht bereits Schritt 2 für RZ
am Ausgangs-Segment — die übrigen Schichten sind die Ausbaustufen.

---

## Offene Datenlücken (für spätere Beschaffung)

1. **EN 1838:2025-03 Kernwerte** — BELEGT via `Handbuch_NotSicherheitsbeleuchtung_2026.md`
   (Lux-Tabelle R24, Offset-Formel R26, NEU-Stellen R39–R45, z-Faktoren R49,
   Systembetriebsdauer Tab. A.1 R57 — alle mit Seiten-Refs). Rest-Lücke nur noch der
   zitierbare Originaltext; die Sekundärerfassung reicht für die Engine.
2. **Hersteller-Abstandstabellen** je Leuchte (h→Abstand) — OFFEN. Herstellerspezifisch,
   NICHT im Norm-Handbuch gedruckt (HB2026-R27 nennt nur die INOTEC-Referenzbreite 2,0 m);
   nötig für die photometriefreie Linien-Verdichtung. Beschaffung: Produktkataloge/Planungstools.
3. **OVE R 12-2 / OIB-RL 2 Originale** — OFFEN (AT-spezifisch; HB2026 ist DE-only). EN 50172
   dagegen via HB2026-R55–R58 (DIN EN 50172:2024-10) belegt.
4. ~~TRVB E 102 / 123 S~~ — GESTRICHEN: TRVB E 102 seit 2019-02-14 zurückgezogen, ersetzt
   durch ÖNORM E 8101 + OVE R 12-2 + EN 1838 + EN 50172 + OIB-RL 2 (→ deckt sich mit Lücke #3).

---

*Detail je Quelle: `bildlehren/Bildlehren_*.md`. Regel-Tabellen mit §-Referenzen:
die jeweiligen `*.md`-Digests. Diese Synthese ist Referenz-Praxis-Lehre — die harten,
zitierbaren Werte stehen in den Digests mit ihrer Norm-Fundstelle.*
