# Review — `knowledge/Pläne zeichnen Wissen` (2026-10-03)

Konsolidiertes Review des Referenz-Wissens-Korpus (Owner-Auftrag). Read-only
erhoben über 6 parallele Analyse-Agenten je Projekt + Querschnitt; Quellen sind
die digesteten Evidenz-JSONs (`_Analyse_Regelwerk/evidenz/<Projekt>/`), die
`ANALYSE_*.md` und die projektweiten Analyse-Docs. Scope-Ausnahme laut Owner:
**Baufeld E2 nur der UG-DXF-Plan** (EG/OG, `neu/`, `FINAL_…`, ZIP nicht geöffnet).

## Inhalt des Ordners

5 Referenz-Plansätze (Erklärungs-DXFs je Geschoss) + projektübergreifendes
Regelwerk (66 Regeln, 538 Belegseiten) + Master-Lehrdoc
`Notbeleuchtungen zeichnen.docx`. Gesamtbild: **sauber, ehrlich, evidenzgetrieben**
— die Doku grenzt ihre Lücken selbst ab statt sie zu kaschieren.

| Satz | Typ | Stand | Inhalt | Lehrwert einzigartig |
|---|---|---|---|---|
| **Mollgasse** | Wohnbau, 8 Gesch. | BASIS, autoritativ | 95-S-PDF + Tiefen-Analyse; GT ~97 Leuchten | Grundgerüst RW-001–021 + Antipanik-Konstruktion (mm-genau) |
| **Hausfeld** | Wohnbau, 5 Gesch. | fertig, 0 Widerspruch | 58 RZ (down 25 / left 22 / right 11) | **M3-Gegenwächter** (Richtung geschossabhängig) |
| **Am Rain** | Wohnbau, 6 Gesch. | TEILSTAND | nur 95 RZ ersetzt, **182 SL/AP/Aufheller offen** | Quellen-Disziplin (Textanker ≠ Ausgang) |
| **Tomaschek** | **Schule**, 3 Gesch. | hoch, hash-verifiziert | 146 Leuchten (81 RZ + 65 SL/AP) | Schul-Logik bricht Wohnbau-Regel |
| **Baufeld E2** (nur UG) | UG/Garage | Lehrlayer-GT | 89 RZ, 87 ok / 2 Abw. | reine Basis-Validierung + Lehrlayer-Harness |

## Quer-Erkenntnisse

1. **M3 = zentraler Leitsatz, projektweit belegt.** RZ-Pfeiltyp = **Frontalsicht
   der ankommenden Person, NICHT Weltrichtung**. Block-Name (links/rechts/down) =
   Variante; Weltrichtung entsteht erst durch Rotation (+ Spiegelung bei
   xscale < 0). Weißer Balken immer zur Person; der Pfeil ist ein getrennter
   Freiheitsgrad. Mollgasse lehrt's 7-fach, das Master-docx ist die Quelle.
2. **Hausfeld: Richtung ist geschossabhängig im selben Haus.** 2DG **3/3 left**
   (Richtungswechsel aufs Podest), UG **19/32 down** (Garagenstrom flüchtet
   HINAUF). Eine „Stiegen-RZ ⇒ down"-Heuristik setzt 2DG komplett falsch →
   Hausfeld = Pflicht-Wächter gegen Pauschalierung („Stiegen-Richtung =
   Erkennungs-Decke").
3. **Baufeld-UG bestätigt KG-Semantik:** 4× Textkennung „richtung EG" = Flucht
   hinauf; 89 RZ, sonst nichts → valides UG-Blatt darf rein RZ sein (Engine darf
   im UG kein SL/Aufheller erzwingen). Lehrlayer-Trio (118 Personen + 269
   Blickkeile + 60 Fluchtlinien) = fertiges GT-Harness.
4. **Tomaschek bricht die Wohnbau-Kernregel:** Unterrichtsraum bekommt
   **Innen-Notlicht** (Tür-RZ + Aufheller je Raum) — `WOHNUNG_PRIVAT`-Skip gilt
   NICHT. Antipanik flächenbezogen in Sälen (alle 14 im SG), nicht
   sichtblockade-getrieben wie im Wohnbau.
5. **Reproduktion << Wissen.** Mollgasse: 54 % Regel-Deckung deckungsgleich, aber
   nur 34 % Leuchten-Paarung (33/97), 13 % Typ-Match. Lücke = 3 Mechanismen:
   M3-Pfeiltyp (Leonis, ~20 Misses, in Arbeit `bd9f070`), Positions-Band RW-005
   (Leonis), KG-/beidseitig-Erkennung (Selman).

## Regelwerk-Querschnitt

66 Regeln (35 Basis RW-001–035 Mollgasse-belegt + 31 Ergänzung RW-101–131),
dedupliziert aus 111 Kandidaten-Records. **0 echte Widersprüche in 538 Seiten**
(einziger Konflikt K-01 = PDF-interner Textfehler S.57 B↔C, kein Regelwiderspruch).
Belege sauber (quelle_pdf + belege_dxf + Begründung je Regel); nur RW-026/RW-119
ohne DXF-Beleg = sachlich korrekt (Text-/OVE-Label-Regeln). Projekt-Arbeitsteilung
komplementär: Mollgasse = Gerüst, Tomaschek = Schule + Norm-Schwellen (37 Regeln,
größter Einzelbeitrag), AmRain = Bestands-/Quellen-Disziplin, Hausfeld =
Wohnbau-Detail, Baufeld E2 = reine Basis-Validierung (0 eigene Regeln).
Master-docx = **Mollgasse-Dublette** (31 Mollgasse-Nennungen, 0 für andere
Projekte) = editierbare Quelle des Mollgasse-Lehr-PDF → nicht erneut digesten.

## Fazit

Korpus **hochwertig und übernahmereif als Lehr-/GT-Basis**. Das Problem ist
**nicht Wissen, sondern Reproduktion** — und der größte Hebel (M3) liegt in
Leonis' Lane und läuft bereits.

---

## To-do / Backlog (aus diesem Review)

| # | To-do | Lane | Status |
|---|---|---|---|
| T1 | RW-101–131 im `platzierung/regelwerk.py`-Mapping (UMSETZUNG/NICHT_UMSETZBAR) klassifizieren — Mapping endet heute bei RW-035 | Leonis | **in Arbeit (dieses Review)** |
| T2 | `Nutzungsklasse` (`contracts/raum_modell.py`) um Bildungsraum-Typen erweitern (Tomaschek-Hauptregel nicht ausdrückbar) | 3-Owner-Contract (Selman+Enis+Leonis) | **geflaggt — braucht Owner-GO + Contract-Freeze** |
| T3 | Am Rain: 182 offene SL/AP/Aufheller-Symbole (warten auf Projekt-Legende); Build-Skripte + Originale liegen nur im Windows-Papierkorb → sichern vor Leeren | Owner | **geflaggt — Owner-Aktion (Dateien), NICHT blind angefasst** |
| T4 | Doku-Hygiene: `konfidenz` nur 41 % gefüllt; RW-026 `quelle_pdf`=Hausfeld ≠ Begründung=Tomaschek | Leonis/Doku | offen (minor) |

### Owner-offene Fragen (blockieren saubere Engine-Verbesserung)

1. ~~**Tür-RZ-Versatz widersprüchlich**~~ **GELÖST 2026-10-03:** kein fixes Maß —
   RZ **mittig auf der Tür** (Türöffnungs-Mitte); 735–930 mm sind deskriptiv, nicht
   präskriptiv. `RZ_INS_RAUM_MM=0` bleibt (Engine schon korrekt). Beleg-Crop
   `scratchpad/beleg_tuer_rz_913mm.png`.
2. **B1-Aufheller 500 mm je RZ:** kein Mollgasse-PDF-Beleg, aber Haupttreiber der
   115 Überschuss-Leuchten (EG allein 48). Drosseln oder behalten?
3. **S.57/58 B↔C:** PDF-Textfehler (Positionen stimmen, Labels vertauscht), seit
   2026-09-20 offen.
4. **beidseitig-Format:** GT = 2 gespiegelte Einzel-RZ, Engine = 1 `bothsided`-Block.
   Zielformat?
