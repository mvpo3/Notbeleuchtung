# ENGINE_WISSEN_IST — Platzierungs- & Rotationsengine (Ist-Stand 2026-09-30)

Quelle: vollständige Code-Lektüre `src/notbeleuchtung/platzierung/*.py`,
`symbols/orientation.py`, Daten-Dateien. Schritt 1 des Mollgasse-Review-Auftrags.
Naht-Grenzen: NormProvider-Abfragen = Enis' Lane; Symbole & Orientierungen =
Rivoplan-Registry (Leonis); LB-Vorgaben = 3. Schicht.

## TEIL 1: REGELN (je 1 Satz + Fundstelle)

### Platzierungs-Orchestration

1. **Fahrplan-Reihenfolge:** Anker → Linie → Fläche → Deckung; liefert der Graph Kreuzungen (degree ≥ 3), RZ an Kreuzungen + Ausgängen (anker_strategy), sonst Segment-Strategie (communal_stgh_strategy), Fallback Gang-Mittellinien (gang_strategy). — `platzierer.py:7-12`, `anker_strategy.py:1-18`, `communal_stgh_strategy.py:1-8`, `gang_strategy.py:1-15`
2. **RZ an Segment-Enden:** 1 RZ je Fluchtweg-Segment am Ausgangs-Endpunkt, Orientierung vom Anlauf zur nächsten Tür/zum Ausgang. — `communal_stgh_strategy.py:58-156`
3. **RZ an Ankern (Kreuzungen):** 1 RZ je Knoten mit degree ≥ 3, Pfeil zeigt zum nächsten Ausgang (Dijkstra-Gefälle). — `anker_strategy.py:1-126`, `graph.py:39-45`
4. **Beidseitige RZ an Wasserscheiden:** Kreuzung ≈ gleich weit zu zwei Ausgängen (±15 % rel.), Wege in Gegenrichtung (cos < −0,5) → Doppel-Zeichen, Achse = Korridor-Symmetrie. — `anker_strategy.py:55-99`, `bausteine.py:190-199`
5. **Tür-RZ-Rotation (R-B):** Piktogramm zeigt INS Rauminnere = Gegenrichtung der Fluchtachse. — `bausteine.py:110-122` (`rotation_piktogramm_in_raum`)
6. **RZ-Entzerrung:** 3 unabhängige Strategien können RZ nahe beieinander erzeugen; `abstand_nachpass.entzerre` (250 mm Mindestabstand) mergt/nudgt post-hoc. — `abstand_nachpass.py:1-156`
7. **Gang-Fallback:** Ohne Segmente UND ohne Kreuzungen → RZ entlang der Korridor-Mittelachse im Abstand der Erkennungsweite (l=z·h), Pfeil zum nächsten Ausgang. — `gang_strategy.py:109-166`, `platzierer.py:237-240`
8. **Sichtkette (Ausdünnung):** redundante RZ fallen, solange jeder Einzugspunkt ≥1 RZ sieht und jedes RZ weiterführt; Strahl bleibt im Korridor. — `sichtkette.py:99-213`
9. **Längs-RZ in Gang-Armen:** Lücken > Erkennungsweite zwischen End-RZ eines Arms → Zwischen-RZ. — `platzierer.py:93-131` (`_arm_gap_mm`)
10. **Tür-Lücken-RZ (Punkt 2):** zwischen Abteil-Türen (Aufschlag = Sichtbarriere) punktweise RZ-Kandidaten, Ausdünnung via Sichtkette. — `platzierer.py:134-177`

### Rotation & Richtung

11. **Rotations-Konvention:** Pfeil-unten-Block (Basis 270°, −Y) → `rotation = (Ziel-Azimut + 90°) % 360°`, quantisiert auf 4 Kardinalrichtungen. — `bausteine.py:50-56` (`rotation_zur_tuer`), `symbols/orientation.py:19-60`
12. **Richtungs-Block-Wahl:** existiert der native Block (links/rechts/unten), wird er unrotiert gesetzt; sonst Fallback-Rotation. — `bausteine.py:146-178` (`select_key`, `key_und_rotation`)
13. **Abzweig-Erkennung:** Knick > 45° (cos < 0,707) → Abzweig-RZ zeigt den WEG (links/rechts); gerade → down-Typ, Front zur ankommenden Person (NB-R06/R07). — `gang_strategy.py:45-57,146-163`
14. **Stiegenhaus-Fluchtvektor (NB-R13):** Fluchtrichtung aus Treppenlauf-Vektoren; UG kehrt um (hinauf = Flucht). — `stgh_strategy.py:39-65`

### Sicherheitsleuchten & Antipanik

15. **Aufheller-500mm (B1):** je RZ ein Aufheller 500 mm hinter dem RZ, falls nicht schon lux-gedeckt (Hersteller-Photometrie-Gate). — `fachpraxis.py:174-242` (`QUELLE_AUFHELLER`)
16. **Tür-RZ/SL in Pflichträumen:** TECHNIK/MUELLRAUM/KINDERWAGENRAUM + communal Nebenräume (Ausnahmen `_TUERLEUCHTE_KEIN_COMMUNAL`). — `fachpraxis.py:60-107`
17. **Mittige Zusatzleuchte:** Raum < 60 m² → Aufheller; ≥ 60 m² oder nicht-konvex (Fläche/Bbox < 0,85 = L-Raum) → Antipanik. — `fachpraxis.py:98-106,298-400`
18. **Antipanik-Flächentrigger:** Sanitär ≥ 8 m² (OVE P.1); Verkehr ≥ 60 m² (OVE P.3); `ist_barrierefrei`-Toilette → Pflicht (§4.3.8). — `flaechen_strategy.py:52-95`, `sonderstellen_strategy.py:137-175`
19. **Antipanik-Raster:** Start beim Norm-Mindestraster, Verdichtung bis EN-1838-Nachweis (1 lx, Ud ≥ 1:40); max. 6 Runden / 25 Leuchten. — `flaechen_strategy.py:97-123`
20. **Sonderstellen (§4.1.2):** je Sonderstelle eine SL direkt an der Stelle; RZ an Niveauänderung nur per LB (fail-closed). — `sonderstellen_strategy.py:105-175`
21. **Außenleuchte (§4.1.2 b):** je final_exit eine SL 1 m VOR der Tür, Richtung = Auswärts-Normale der Wandkante. — `aussen_strategy.py:66-97`

### Deckung (Lux-getrieben)

22. **Fluchtweg-SL entlang Mittelachse:** photometrischer Nachweis (≥ 1 lx, Ud ≥ 1:40) auf der Korridor-Mittellinie; Abstand aus Hersteller-LDT. — `deckung.py:1-40`, `lux.py:107-300`
23. **Abstand-Verdichtung:** Faktor 1,3 je Iteration bis Nachweis hält oder 4 m Mindestabstand; max. 6 Runden. — `deckung.py:252-297`
24. **Redundanz-Garantie (EN 50172 §5.1.8):** je Fluchtweg-Abschnitt ≥ 2 Leuchten in Erkennungsweite. — `deckung.py:113-150`
25. **S4-Drossel:** RZ zählt als Stützpunkt nur im Gang oder ≤ 2 m vom Rand; Aufheller nur bei Lücke > 8 m. — `deckung.py:49-54`

### Geometrische Nachpässe

26. **Verbotszonen:** Platzierungen auf Stiegen-Laufflächen/Öffnungen → relocate in den Wirts-Raum. — `verbotszonen_nachpass.py:43-77`
27. **Abstand-Nachpass:** Paare < 250 mm an Strategie-Nähten mergen (gleiche Art) oder nudgen (Rang: rz > sicherheitsleuchte > antipanik); SL-Dubletten < 2 m im GLEICHEN Raum mergen. — `abstand_nachpass.py:155-200`
28. **Mittellinien-Snap (R1/R6):** Gang-Symbole auf Kurzachsen-Mitte; bei Bestandsleuchten-Reihe deren Linie, nie AUF einem Bestands-Spot; Tür-RZ ≤ 500 mm ausgenommen. — `mittellinie_snap.py:90-135`

### LB-Übersteuerung & Stromkreise

29. **LB-Exklusion:** LB kann SL/AP je Raumtyp verbieten. — `lb_override.py:37-72`
30. **LB-Inklusion:** LB kann SL in zusätzlichen Raumtypen erzwingen (`lb_quelle`). — `lb_override.py:75-110`
31. **Bauteil-Cluster A|B:** x-Spannweite > 20 m → Teilung; Sicherheitskreis F13, max. 20 Leuchten je Kreis. — `bausteine.py:181-187`, `circuit_zuordnung.py:36`
32. **Montage-Art (NB-R14):** Stiegen-/Tür-/Ausgangs-RZ = WA; Gang-/Flächen-Leuchten = DA; Decke-Default-Nachpass. — `bausteine.py:23-28`, `platzierer.py:361-363`

## TEIL 2: IMPLIZITE ANNAHMEN & KONSTANTEN

### Geometrisch-normativ

| Name | Wert | Fundstelle | Wirkung |
|---|---|---|---|
| `RZ_INS_RAUM_MM` | 0,0 | bausteine.py:58-64 | Tür-RZ auf Wandachse (war 150; Owner 2026-09-18: „kein fixer Sollwert") |
| `_MIN_KORRIDOR_ARM_MM` | 6000 | platzierer.py:65 | kleinster separat behandelter Gang-Arm |
| `_MAX_RZ_ARM_GAP_FALLBACK_MM` | 12000 | platzierer.py:70 | RZ-Abstands-Fallback ohne Norm-Erkennungsweite |
| `_TUER_MAX_BREITE_MM` | 1300 | bausteine.py:70 | breiter = Wandloch, keine echte Tür |
| `_ABTEIL_MAX_M2` | 8 | bausteine.py:89 | Abteil-Schwelle |
| `BUILDING_SPREAD_MM` | 20000 | bausteine.py:31 | Bauteil-Cluster-Teilung |

### Sichtkette

| Name | Wert | Fundstelle | Wirkung |
|---|---|---|---|
| `_SCHUTZ_RADIUS_MM` | 2000 | sichtkette.py:43 | Exit-/Kreuzungs-RZ ≤ 2 m = nie ausdünnen |
| `_KONTUR_PUFFER_MM` | 500 | sichtkette.py:50 | Zugehörigkeits-Puffer Zacken-Konturen (D6) |
| `_PIKTO_HOEHE_M` | 0,15 | sichtkette.py:53 | Basis für Erkennungsweite l=z·h |
| `_SAMPLES` / `_RAND_ANTEIL` | 12 / 0,08 | sichtkette.py:56-57 | Strahl-Abtastung |

### Anker / Gang

| Name | Wert | Fundstelle | Wirkung |
|---|---|---|---|
| `_WASSERSCHEIDE_TOL` | 0,15 | anker_strategy.py:60 | Distanz-Balance ±15 % |
| `_WASSERSCHEIDE_COS` | −0,5 | anker_strategy.py:61 | Gegenrichtung > 120° |
| `_MIN_RZ_MERGE_MM` | 250 | anker_strategy.py:110 | Anker-Dedupe |
| `_TUERWAND_SUCH_MM` | 600 | anker_strategy.py:129 | Tür-Wandkanten-Suche |
| `_DEFAULT_RZ_ABSTAND_MM` | 15000 | gang_strategy.py:43 | Fallback-RZ-Abstand |
| `_ABZWEIG_COS` | 0,707 | gang_strategy.py:48 | 45°-Abzweig-Schwelle |

### Fachpraxis

| Name | Wert | Fundstelle | Wirkung |
|---|---|---|---|
| `aufheller_abstand_mm` | 500 | fachpraxis.py:121 | B1-Versatz hinter RZ |
| `TUERLEUCHTE_HOEHE_MM` | 2400 | fachpraxis.py:95 | Montagehöhe Zusatzleuchte |
| `_ANTIPANIK_AB_M2` | 60 | fachpraxis.py:100 | Aufheller↔Antipanik-Schwelle |
| `_KONVEX_MIN` | 0,85 | fachpraxis.py:105 | L-Raum-Erkennung |
| `_RZ_REICHWEITE_FALLBACK_MM` | 15000 | fachpraxis.py:102 | Aufheller-Lux-Gate-Sichtlinie |
| `_WOHNUNGS_VORRAUM_MAX_M2` | 6 | fachpraxis.py:523 | R7-Vorraum-Filter |
| `_STGH_EXIT_RADIUS_MM` | 2500 | fachpraxis.py:572 | stair_exit↔STGH-Zuordnung |

### Deckung / Lux

| Name | Wert | Fundstelle | Wirkung |
|---|---|---|---|
| `_MIN_ABSTAND_MM` | 4000 | deckung.py:44 | SL-Mindestabstand |
| `_MAX_ABSTAND_MM` | 30000 | deckung.py:45 | Hersteller-Cap |
| `_VERDICHTUNGS_FAKTOR` / `_MAX_VERDICHTUNGEN` | 1,3 / 6 | deckung.py:42-43 | Verdichtungsschritte |
| `_REDUNDANZ_MIN` | 2 | deckung.py:47 | EN 50172 §5.1.8 |
| `_DROSSEL_RANDNAH_MM` / `_DROSSEL_LUECKE_MM` | 2000 / 8000 | deckung.py:53-54 | S4-Drossel |
| `_NACHWEIS_RASTER_MM` | 250 | deckung.py:46 | Lux-Raster |
| `_UD_DEFAULT` | 1/40 | lux.py:73 | EN-1838-Default |
| `_MAX_RASTER_PUNKTE` | 8 Mio. | lux.py:80 | Phantom-Extents-Schutz |
| `wartungsfaktor` | 1,0 Default | lux.py:27-37 | MF-Slice inert bis Enis-Werte |
| `_ANTIPANIK_MAX_LEUCHTEN` / `_RUNDEN` | 25 / 6 | flaechen_strategy.py:31-32 | Überproduktions-Cap |

### Nachpässe / Sonstiges

| Name | Wert | Fundstelle | Wirkung |
|---|---|---|---|
| `_MIN_ABSTAND_MM` (Nachpass) | 250 | abstand_nachpass.py:48 | Symbol-Mindestabstand |
| `_DUBLETTEN_ABSTAND_MM` | SL: 2000 | abstand_nachpass.py:55 | SL<2m-Merge (nur gleicher Raum) |
| `_LAENGS_FAKTOR` / `_MIN_SNAP_MM` | 2 / 20 | mittellinie_snap.py:33-34 | Korridor-Snap |
| `_BESTAND_QUER_SPREAD_MM` / `_MIN_LAENGS_MM` | 600 / 800 | mittellinie_snap.py:37-42 | R1/R6 Bestandslinie |
| `_TUER_RZ_SNAP_FREI_MM` | 500 | mittellinie_snap.py:87 | Tür-RZ nicht snappen |
| `_ABSTAND_AUSSEN_MM` | 1000 | aussen_strategy.py:28 | Außenleuchte 1 m vor Tür |
| `_MAX_LEUCHTEN_JE_KREIS` | 20 | circuit_zuordnung.py:36 | Stromkreis-Cap |
| `_MAX_RASTER_PX` | 8 Mio. | mittellinie.py:28 | Skelettierungs-Cap |
| `scale_abs` RZ/beids./AP/Aufheller | 50 | schrack_symbol_mapping.yaml:39-84 | Weltgrößen 883/586/192 mm |

## TEIL 3: Block-Basis-Orientierungen (orientation.py — Single Source)

- `RIVO_ARR_down` 270° (−Y) · `RIVO_ARR_left` 180° (−X) · `RIVO_ARR_right` 0° (+X)
- `RIVO_ARR_bothsided`: KEINE Basis — Achs-Rotation (Wasserscheide).
- Gemessen 2026-09-07; Rivoplan-Bibliothek 2026-09-21 byte-identisch.

## TEIL 4: NormProvider-Abhängigkeiten (Enis-Naht)

| Abfrage | Bedeutung | Konsumenten |
|---|---|---|
| `erkennungsweite_m(h, hinterleuchtet)` | l = z·h | sichtkette, gang, deckung, redundanz |
| `fuer_fluchtweg_abschnitt(segment)` | Symbol/Höhe/Quelle für RZ/SL | communal, anker, gang, deckung |
| `fuer_raum(raum_typ, ist_fluchtweg)` | Symbol/Höhe/Mindestanzahl/AP-Schwelle | flaechen, fachpraxis |
| `regelwerk_snapshot()` | Flächen-Schwellen (Sanitär/Verkehr) | flaechen, sonderstellen |

## TEIL 5: RW-Mapping (platzierung/regelwerk.py)

UMSETZUNG (23): RW-001–010, 012–014, 016, 018–020, 027, 029–032, 034.
NICHT_UMSETZBAR mit Grund (12): RW-011, 015, 017, 021–026, 028, 033, 035.
Audit-Kanal: `regelwerk.quelle("RW-###")` = `"Referenz-Praxis: RW-### — <thema>"`.
