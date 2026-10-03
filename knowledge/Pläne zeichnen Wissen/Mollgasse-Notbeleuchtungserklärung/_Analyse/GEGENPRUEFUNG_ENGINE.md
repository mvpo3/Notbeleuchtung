# GEGENPRÜFUNG Engine ↔ Mollgasse-PDF/DXF (Schritt 5)

Stand 2026-09-30. Basis: `ENGINE_WISSEN_IST.md` (32 Engine-Regeln + Konstanten)
↔ `REGELWERK_Mollgasse.{md,json}` (35 Basis-Regeln RW-001–035) ↔ echter
Engine-Lauf auf allen 8 Mollgasse-DXFs (Validierung 2026-09-29, je
Referenzleuchte in `ANALYSE_DXF_<G>.md` Spalte „Engine heute";
Aggregat: 33/97 gepaart, 13/33 Typ-Match, 64 fehlt, 115 überflüssig).

Klassen: **DG** = deckungsgleich · **AB** = abweichend · **F** = fehlt ·
Wirkung = was der echte Lauf auf den Mollgasse-DXFs zeigt.

## 1. Regel-für-Regel (35 Basis-Regeln)

| RW (NB) | Thema | Klasse | Fundstelle / Differenz | Wirkung im Lauf |
|---|---|---|---|---|
| RW-001 (R01) | Tür-RZ raumseitig, Piktogramm in den Raum | **AB** | `bausteine.rotation_piktogramm_in_raum` + `RZ_INS_RAUM_MM=0` — PDF-Vermessung zeigt 735–930 mm raumseitigen Versatz, Engine setzt auf Wandachse (Owner-Ansage 18.09. „kein fixer Sollwert" — Konflikt der Owner-Aussagen!) | Tür-RZ paaren meist (<1,3 m), Versatz-Differenz geht voll in die Median-Distanz |
| RW-002 (R02) | Allgemeinbereichs-Tür-RZ, 1 RZ bei freier Sicht | **DG** | `fachpraxis.plant_tuer_rz` (communal) | EG-Nebenräume paaren |
| RW-003 (R03) | Haupteingang = Ziel beider Sichtketten | **DG** | anker final_exit + fachpraxis | EG (D) gepaart (959–1240 mm) |
| RW-004 (R04) | Stiegenhauspfeil: UG mit, OG entgegen | **DG** | `stgh_strategy.fluchtvektor` | greift; Positions-Differenz s. RW-005 |
| RW-005 (R05) | 800–1122 mm vor Antritts-/Austrittskante, auf Laufachse, nie auf Wand | **AB** | `stgh_strategy.plan_stiegenhaus_rz` platziert am Podest-/Exit-Anker, NICHT im 800–1122-Band vor der Kante | Haupttreiber der 1–2-m-Paarungs-Distanzen in allen Geschossen |
| RW-006 (R06) | gerade Gang-RZ: down, Front ENTGEGEN Flucht | **DG** | `communal_stgh`/`gang_strategy` (Commit 710b859) | Typ-Matches kommen fast nur hierher |
| RW-007 (R07) | links/rechts/unten nach Frontalsicht der Person | **AB** | `richtung_und_rotation` wählt nach FLUCHTVEKTOR-Quantisierung, nicht nach Personen-SICHT; Erstleuchten-Winkelband (0,3–45,5°) ungeprüft | 20/33 Paare mit falscher Typ-Familie — größter Typ-Hebel |
| RW-008 (R08) | Erster-Blick + Zusatz-RZ + Mehrfachbedienung | **DG** | `sichtkette.kette_ausduennen` + `_arm_gap_mm` | trägt; Sichtprüfung nutzt Segment-Polygone statt Personen-Punkte |
| RW-009 (R09) | Gang↔STGH-Mündung | **DG** | anker (Grad ≥3) | Kreuzungs-RZ paaren |
| RW-010 (R10) | Antipanik/Aufheller „durch Lichtberechnung bestätigt" | **DG** | deckung/flaechen + Lux-Bericht | vorhanden; ABER Überschuss-Lane s. §3 |
| RW-011 (R11) | Hindernis (Lichtkuppel) → versetzen, Ausrichtung behalten | **F** | nur `verbotszonen_nachpass` (Stiegenflächen); generisches Decken-Hindernis fehlt (Input fehlt auch) | DG (A) 20864 versetzt — Engine kennt die Kuppel nicht |
| RW-012 (R12) | Sichtkette lückenlos | **DG** | sichtkette | trägt |
| RW-013 (R13) | UG flüchtet HINAUF | **DG** | `ist_untergeschoss` + fluchtvektor(hinauf) | 1KG/2KG-Stiegen-RZ richtige Richtung |
| RW-014 (R14) | Wand vs. Decke | **DG** | montage_art (Commit 09db956) | gesetzt |
| RW-015 (R15) | Kabeltrasse ≥450 mm, 5-Schritt-Ausweich | **F** | Trassenlage fehlt im leeren Input (Selman/LB-Naht) | 2KG-Trassen-Ausweichpositionen nicht reproduzierbar |
| RW-016 (R16) | beidseitig an Wasserscheide | **AB** | `_wasserscheide_achse` GEBAUT, aber 0/8 Treffer: KG-Zirkulation liefert keine Gegenrichtungs-Pfade; zudem rendert Engine EINEN bothsided-Block, GT = 2 gespiegelte Einzel-Blöcke (Δ264–318 mm) | beidseitig 0/8 = kompletter Miss |
| RW-017 (R17) | Garage Motorrad-durchquerbar | **F** | Garage-Zirkulation fehlt (Selman S-KG) | 2KG-Garage leer |
| RW-018 (R18) | Gebäudehälften nie raten | **DG** | Prozessregel, kein Automatismus (bewusst) | — |
| RW-019 (R19) | UG-Türleuchte Technik/Keller | **DG** | `_TUERLEUCHTE_RAUMTYPEN` | greift wo Räume erkannt |
| RW-020 (R20) | türloser kurzer Gang: 1 Leuchte | **DG** | sichtkette + `_MIN_KORRIDOR_ARM_MM` | ok |
| RW-021 (R21) | SV-Anlage ≠ E-Verteiler-Wand | **F** | Anlagen-Platzierung nicht im Platzierer (circuit/LB-Lane) | 1KG 1CB68 nicht gesetzt |
| RW-022–027 (R22–27) | TOMA-Quellen-/Dokument-Disziplin, Lift-Ausschluss | **DG** | R27: `entferne_schacht_leuchten` + KEIN_COMMUNAL; Rest Prozess/Healthcheck | 0 Symbole in Lift/Schacht ✓ |
| RW-028 | Antipanik-Längsachse in Zielbereich drehen | **F** | AP wird rotationslos gesetzt | (B)/(C) 2KG-Orientierung nicht reproduziert |
| RW-029 | Antipanik mittig auf Bereichs-Diagonale | **AB** | `find_center_visual` ≈ mittig, aber NICHT das Diagonale-Mittelpunkt-Rezept — Detail-Pass beweist: Owner setzt EXAKT auf Diagonalen-Mitte (Δ23–33 mm!) | AP-Positionen weichen dm-weit ab |
| RW-030 | Antipanik-Kann-Fall zur Lux-Stützung | **DG** | verdichte_fluchtweg (lux-getrieben) | ok |
| RW-031 | Geräte-Wahl je Geschoss (AP=UG, Aufheller=EG–OG) | **AB** | Engine wählt nach Fläche/Konvexität (60 m²/0,85), nicht nach Geschoss | Typ-Mix im UG teils falsch herum |
| RW-032 | Decke-mittig-Alternative Stiegen-Leuchte | **DG** | dokumentierte Alternative (Regelfall WA gebaut) | — |
| RW-033 | OG-Ausnahme: 1 STGH + I-Gang → kein Zusatz-RZ | **F** | sichtkette dünnt, aber keine explizite OG-Ausnahme | OG-Überschuss 8–10 je Geschoss |
| RW-034 | Lichtberechnungs-QA jedes Geschoss | **DG** | pipeline.run → Lux-Bericht automatisch | ✓ |
| RW-035 | Stiegenpfeil = Farbe der Stiege | **F** | Erkennungs-Heuristik (Selman-Lane) | — |

**Bilanz nach Regelanzahl: 19 DG · 6 AB · 10 F** (RW-022–027 als 6 gezählt).
**Bilanz nach Belegen (97 Referenzleuchten, echter Lauf): 33 gepaart (34 %),
davon 13 mit richtiger Typ-Familie (13 %).** Die Regel-Abdeckung (54 % DG) ist
deutlich besser als die Leuchten-Reproduktion — die Differenz ist Positions-
Konvention (RW-005/001), Typ-Wahl (RW-007) und Erkennungs-Nähte (RW-015/016/017).

## 2. Der echte Engine-Lauf (Schritt-5-Pflicht, je Referenzleuchte)

Vollständig gelaufen (kein Schätzen nötig): leerer Mollgasse-Plan → echte
Provider → `pipeline.run` je Geschoss; je Referenzleuchte Ergebnis in
`ANALYSE_DXF_<G>.md` (Spalte „Engine heute": gepaart+Distanz+Typ / FEHLT).
Roh-Daten: `Projekte/_ergebnis/Mollgasse_GT/<G>/vergleich.json` (paare/fehlt/
ueberfluessig einzeln). Kennzahlen: EG 5/17 · 1OG 4/11 · 2OG 4/11 · 3OG 1/4 ·
4OG 5/7 · DG 2/6 · 1KG 3/12 · 2KG 9/29.

## 3. ENGINE-ÜBERSCHUSS (Engine-Regeln ohne Mollgasse-PDF-Beleg)

| Engine-Regel | Fundstelle | PDF-Status | Bewertung |
|---|---|---|---|
| **Aufheller-500mm je RZ (B1)** | fachpraxis.py:174-242 | KEIN Mollgasse-Beleg — PDF kennt Aufheller nur lichtberechnungs-getrieben (RW-030/031) | **Haupttreiber der 115 Überschüsse (EG 48!)**; Quelle = Owner-Ansage 2026-09-09, vom PDF-Regelwerk überholt? → Owner-Frage |
| Tür-SL `antipanik_leuchte` in Pflichträumen | fachpraxis.py:60-107 | PDF setzt Tür-**RZ**, Zusatzleuchte nur per Lichtberechnung | Referenz-Praxis (din/TOMA) — kompatibel, aber Mollgasse-fremd |
| Redundanz ≥2 je Abschnitt | deckung.py:113-150 | nicht im PDF | EN-50172-Norm-Pflicht — behalten (Hard-Stop-Lane) |
| Verkehrsfläche ≥60 m² → AP | flaechen_strategy | nicht im PDF (PDF: Diagonale/Lux) | OVE-Norm — behalten |
| SL<2m-Merge | abstand_nachpass | nicht im PDF | kompatibel (betrifft nie RZ) |
| R1/R6 Bestandslinien-Snap | mittellinie_snap | nicht im Mollgasse-PDF (Elektroplan-DE-Owner-Regel) | kompatibel; auf Mollgasse inaktiv (kein Bestand im leeren Plan) |
| Fluchtweg-SL-Kette (deckung, 4-m-Min) | deckung.py | PDF deckt Gänge über RZ+Aufheller+Lichtberechnung, keine SL-Reihen | zweiter Überschuss-Treiber — Kalibrier-Frage S4 |

## 4. Kern-Erkenntnisse des Detail-Passes (neu, mm-belegt)

1. **Diagonale = exaktes Mittelpunkt-Rezept** (S.57–59): AP (B) Δ33 mm, (C)
   Δ23 mm von der Diagonalen-Mitte; Konstruktionslinien im DXF real (1D03D,
   1D044, 1D813/1D816). → RW-029 ist ALGORITHMISCH einbaubar (Mauerkante→
   Gangecke-Diagonale, Mitte, fertig).
2. **Achs-Fluchtung AP↔nächste Notleuchte**: (K) Δ24 mm in Achse mit (H),
   wandmittig Δ8 mm (gelbe Hilfslinien 1D097–1D099). → zweites exaktes Rezept.
3. **283 Regel-Aussagen mit Warum** — die Warum-Schicht (was sieht die Person
   als Nächstes) ist die eigentliche Semantik von RW-007/008; Engine prüft
   Sicht heute geometrisch (Segment-Polygone), nicht personenbezogen.
4. **Blockfamilie ≠ Weltrichtung** durchgängig bestätigt (7 Fälle) — Engine-
   Konvention (orientation.py + Regel #8) ist korrekt; jede künftige
   Text-Auswertung muss das beachten.
