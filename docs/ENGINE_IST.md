# ENGINE_IST — Bestandsaufnahme Platzierungs-/Rotationslogik vor dem Regelwerk-Einbau

Stand: 2026-09-29 · Auftrag „Wissensaufbau Notbeleuchtungsplanung" Schritt 5.1.
Referenz: `knowledge/Pläne zeichnen Wissen/_Analyse_Regelwerk/REGELWERK_Notbeleuchtung.json`
(RW-001–RW-027 = migrierte NB-R01–R27 + Ergänzungsregeln aus Projekten 2–5).

## Rotations-Rahmen (Single Source of Truth)

`src/notbeleuchtung/symbols/orientation.py` — NICHT umgehen, nur erweitern:
- `ZIEL_DEG = {rechts: 0, oben: 90, links: 180, unten: 270}`
- `_BLOCK_BASE_DEG = {rivo_arr_down: 270, rivo_arr_left: 180, rivo_arr_right: 0}`
- `transformation(catalog_key, richtung) → (rotation_deg, mirror_x)`; mirror_x
  immer False (3 getrennte Basis-Blöcke).
- Kernformel `bausteine.rotation_zur_tuer(dx, dy)`: (atan2+90°) auf 90° quantisiert.

## Regel → Code-Stelle (UMGESETZT)

| RW (nb_ref) | Regel-Kern | Code-Stelle |
|---|---|---|
| RW-001/002/003 (NB-R01/02/03) | Tür-RZ raumseitig, Piktogramm INS Rauminnere; Allgemeinbereiche; Haupteingang | `bausteine.rotation_piktogramm_in_raum` (R-B, negierte rotation_zur_tuer); `fachpraxis.plant_tuer_rz` (`_TUERLEUCHTEN_RAUMTYPEN`, communal-Kandidaten); `communal_stgh_strategy.py:118` (d_tuer ≤ 2000) |
| RW-004 (NB-R04) | Stiegenhauspfeil: UG-Ströme IN Pfeilrichtung hinauf, OG entgegen | `stgh_strategy.fluchtvektor` (Treppenlauf-Vektoren) |
| RW-005 (NB-R05) | RZ 800–1122 mm vor Antritts-/Austrittskante, Pfeil exakt Laufrichtung, nie auf Wand | `stgh_strategy.plan_stiegenhaus_rz` + R8-Nachpass `fachpraxis.stiegenhaus_rz_nachpass` |
| RW-006 (NB-R06) | gerader Gang: down-Typ, Welt-Pfeil ENTGEGEN Flucht (Front zur ankommenden Person) | `communal_stgh_strategy.py:132–137` + `gang_strategy._ist_abzweig` (45°-Schwelle) — Commit `710b859` |
| RW-007 (NB-R07) | links/rechts/unten-Wahl nach Frontalsicht der Person | `bausteine.select_key`/`key_und_rotation` + `richtung_und_rotation`; Erst-/Folgeleuchten-Winkel implizit über Sichtkette |
| RW-008 (NB-R08) | Erster-Blick-Sichtkette, Zusatz-RZ bei Distanz, Mehrfachbedienung | `sichtkette.kette_ausduennen` (l=z·h aus NormProvider) + `platzierer._sichtlinien_garantie`; Türaufschlag-Barrieren `sichtkette._sicht_frei` |
| RW-009 (NB-R09) | Gang↔STGH-Mündung | `anker_strategy` Kreuzungs-Anker (graph.kreuzungs_anker, Grad ≥3) |
| RW-010 (NB-R10) | Antipanik/Aufheller „durch Lichtberechnung zu bestätigen" | `deckung.verdichte_fluchtweg` (photometrisch) + `flaechen_strategy.plan_antipanik` (OVE-Trigger) + Lux-Nachweis-Bericht (pipeline auto) |
| RW-011 (NB-R11) | Versatz-Sonderfälle (Lichtkuppel etc.) | teilweise: `mittellinie_snap` (R1/R6 Bestandslinie); Schräg-Rotation exakt erhalten = OFFEN (s.u.) |
| RW-012 (NB-R12) | Alternativ-Positionen (gelber Kreis) | NICHT als Placement-Code (Owner-Ermessen); dokumentiert im Regelwerk |
| RW-013 (NB-R13) | UG flüchtet HINAUF | `bausteine.ist_untergeschoss` + `stgh_strategy.fluchtvektor(hinauf=True)` — Commit `59e8f31` |
| RW-014 (NB-R14) | Wand- vs. Deckenmontage | `montage_art`-Vergabe je Strategie + Decke-Default `platzierer.py:361–363` — Commit `09db956` |
| RW-015 (NB-R15) | Kabeltrasse 450 mm (FACHPRAXIS) | NICHT gebaut — Input-Daten (Trassenlage) fehlen im leeren Architekturplan (Selman-/LB-Naht) |
| RW-016 (NB-R16) | beidseitig an der Wasserscheide | `anker_strategy._wasserscheide_achse` + `graph.distanz_je_ausgang` — Commit `f6c69d0`; konservativ (nur Pflicht, keine orangen Alternativen) |
| RW-017 (NB-R17) | Garage Motorrad-durchquerbar | NICHT gebaut — Garage-Zirkulation fehlt aus Erkennung (Selman-Paket S-KG) |
| RW-018 (NB-R18) | Gebäudehälften: nie raten | Prozessregel; Engine-seitig kein Automatismus (bewusst) |
| RW-019 (NB-R19) | UG-Türleuchte (Technik/Keller) | `fachpraxis.plant_tuer_rz` (`_TUERLEUCHTEN_RAUMTYPEN` = TECHNIK/MUELLRAUM/KINDERWAGENRAUM + communal) |
| RW-020 (NB-R20) | türlose kurze Gänge: 1 Leuchte | `sichtkette`-Ausdünnung + `_MIN_KORRIDOR_ARM_MM`-Guard (teilweise) |
| RW-021 (NB-R21) | SV-Anlage nicht an E-Verteiler-Wand | NICHT gebaut (Anlagen-Platzierung = LB/circuit-Lane, kein Platzierer-Concern) |
| RW-022–027 (NB-R22–R27) | TOMA-Dokumentklassen-/Quellen-Disziplin, Lift/Schacht-Ausschluss | R27-Kern: `fachpraxis.entferne_schacht_leuchten` (D2) + `_TUERLEUCHTE_KEIN_COMMUNAL` (LIFT/SCHACHT); Rest = Prüf-/Prozessregeln (validierung-Lane) |

## Audit-Trail

`PlatzierungsErgebnis.norm_quelle` (Naht-Invariante: ∈ `NormRegelwerk.quellen`,
geprüft auf der Golden-Fixture) · Praxis-Kanal existiert: Präfixe
`"Referenz-Praxis: …"` / `"fachpraxis: …"` (z.B. `QUELLE_AUFHELLER`,
sichtkette-Schutzcheck `sichtkette.py:155`). **Einbau-Muster für rule_ids:**
neue praxisbegründete Platzierungen → `norm_quelle = "Referenz-Praxis: RW-### — …"`;
bestehende norm-begründete Sites → NICHT anfassen, Mapping in
`platzierung/regelwerk.py::UMSETZUNG`.

## FEHLT (Kandidaten für Schritt 5.3, nur wenn Regelwerk-belegt)

1. **Balken-zeigt-zum-Menschen als explizite Prüfung** — implizit über NB-R06-
   Rotation, aber keine Verifikation gegen Personen-/Ankunftsrichtung.
   (E2-Auswertung zeigt: mechanisch prüfbar, 87/89 ok.)
2. **beidseitig = gespiegelte Pfeil-rechts-Leuchte** — Render nutzt
   `notlicht_ks_beidseitig`-Block; die Mollgasse-GT zeichnet 2 ko-lokalisierte
   Einzel-Blöcke. Konvention dokumentieren; orientation.py-Erweiterung nur falls
   Regelwerk eine Achs-Rotation fordert (NB-R16 liefert die Achse bereits).
3. **ER-Tür-Ausschluss** („nicht jede einzelne Kellerabteil-Tür") — teilweise über
   `ist_abteil_tuer`-Barrieren + `_tuer_luecken_rz`; expliziter Ausschluss einzelner
   ER-Türen von Türleuchten prüfen.
4. **Schräg-Rotation exakt erhalten** (Tomaschek S.200: 96° nie auf 90° runden;
   `rotation_zur_tuer` quantisiert auf 90°!) — Grenzfall schräge Wände.
5. **Schul-Muster** (Unterrichtsraum = Tür-RZ + Raum-Aufheller) — Ergänzungsregel,
   braucht Raumtyp KLASSENRAUM aus Erkennung (Selman-Naht).
6. **Knick-RZ im abknickenden Stiegenlauf** (Hausfeld S.50/57) — stgh_strategy
   kennt nur Antritt/Austritt.

## WIDERSPRICHT (Regelwerk vs. Engine) — Stand der Analyse

Keine harten Widersprüche gefunden; 1 Kalibrier-Delta: `RZ_INS_RAUM_MM = 0`
(Owner „Wandlinie") vs. Regelwerk-Parameter `raumseitiger_versatz_mm` gemessen
735–930 (NB-R01) — Owner-Ansage 2026-09-18 gilt („kein fixer Sollwert"), Parameter
bleibt dokumentarisch. Bei Owner-Rückfrage: offene_fragen.md #34.
