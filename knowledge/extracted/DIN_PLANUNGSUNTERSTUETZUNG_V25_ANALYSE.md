# din Planungsunterstützung V25 — Analyse eines realen Referenz-Notbeleuchtungsplans

**Quelle:** `DIN-Notbeleuchtungspläne(Beispiele)/din Planungsunterstützung_V25.dxf` (11 MB, AC1032/R2018).
Analysiert 2026-09-09 (Leonis). Ein von **din (Dietmar Nocker)** bestückter **realer 7-Geschoss-
Wohnbau** (Architektur als DWG-XRef je Geschoss, Notbeleuchtung im Modelspace) — d.h. ein
**Profi-Referenzplan**, kein synthetisches Beispiel. Zweck hier: lernen, WIE und WARUM die
Notbeleuchtung platziert ist, gegen unser Norm-Wissen (EN 1838) belegt.

Raum-Labels liegen in den externen XRef-DWGs (`Xref/ARAI5_FE_XEL_ZZ_MOP_<Geschoss>_*.dwg`,
UG/EG/OG1–4/DD) — ohne ODA File Converter (nicht installiert) hier nicht lesbar. Die Räume sind
darum aus Layer-Namen + Symbol-Logik je Geschoss charakterisiert.

## 1. Struktur (WAS)

- **Modelspace = 211 INSERTs** (die platzierte Notbeleuchtung) über 7 XRef-Geschossen
  (Einfügepunkte gestapelt: UG y=−100 k … DD y=+500 k). Kein Text im Master (alle Raumnamen im XRef).
- **Layer-Schema `din_SIBEL_NN_*`** — deckt sich mit unserem `SAFETY_LAYER =
  din_SIBEL_10_emergency_lighting`. Zwei Platzierungs-Layer:
  - **`din_SIBEL_10_emergency_lighting` (grün) = Rettungszeichen (RZ) + Zentrale (SYSTEM).**
  - **`din_SIBEL_10_emergency_lighting_yellow` (gelb) = Sicherheitsleuchten (SL/SPOT).**
  → **din trennt farblich: grün = Zeichen (Piktogramm), gelb = Leuchte (Ausleuchtung).** Wir
  rendern bisher ALLES grün — Übernahme-Kandidat (RZ grün / SL gelb).
  - `din_SIBEL_11_emergency_lighting_system` (5×) · `_70_legend_*` · `_62_QRCode`.

### Platzierung je Geschoss (aus INSERT-Positionen, Cluster um XRef-Anker)

| Geschoss | Σ | RZ_PU↓ | RZ_PLPR (beidseitig) | RZ_PL/PR | SL | SPOT | SPOT_SL | SYSTEM |
|----------|---|--------|----------------------|----------|----|------|---------|--------|
| **UG** (Garage/Technik) | **106** | 31 | 12 | 3 | 30 | 19 | 3 | **5** |
| **EG** (Eingang/Durchgang) | 37 | 7 | **13** | 6 | 6 | 2 | 3 | – |
| OG1 | 9 | 3 | 1 | 2 | – | – | 3 | – |
| OG2 | 13 | 5 | 1 | 2 | – | – | 5 | – |
| OG3 | 12 | 4 | 1 | 2 | – | – | 5 | – |
| OG4 | 3 | 1 | – | 1 | – | – | 1 | – |

**Muster:** UG dominiert (Tiefgarage = lange Fahrgassen → viele Fluchtweg-SL + Antipanik-SPOTs
in der offenen Fläche + die **5 Zentralbatterie/Überwachungs-Einheiten** liegen im UG-Technikraum).
EG hat die meisten **beidseitigen RZ** (13× PLPR — Eingangsebene = viele Kreuzungen/
Richtungswechsel zu den Ausgängen ins Freie). OG1–4 (Wohnungen) sind dünn: je Geschoss ein paar
**RZ_PU über den Türen** zum Stiegenhaus + je 3–5 **SPOT_SL** (Aufheller im Wohnungsgang), fast
keine reinen SL → kurze, eindeutige Wege.

### Rotationen (bestätigt unser Modell)
`STANDARD_RZ_PU` erscheint in allen 4 Rotationen {0,90,180,270} → **der „Pfeil-unten"-Block wird
gedreht**, um den Pfeil in die Fluchtrichtung zu zeigen — genau unser `orientation.py`/#111-Ansatz.
`SPOT` immer 0° (rund/symmetrisch). `SL` längs der Gang-Achse. `SYSTEM` 90°.

## 2. Warum so platziert (EN 1838 §4.1.2, belegt)

Die Platzierung ist die **Überlagerung von drei Regeln** (alle normativ):
1. **Punkt-Pflichtstellen §4.1.2 a–k** — „nahe" = **≤ 2 m** — an: jeder Ausgangstür (R13),
   Treppen/jede Stufe (R14), Niveauänderung (R15), **Richtungsänderung — Leuchte leuchtet BEIDE
   Richtungen (R17)**, **Kreuzung — beide Richtungen (R18)**, letztem Ausgang + außerhalb ins Freie
   (R19), Erste-Hilfe (≥5 lx vertikal, R20), Brandbekämpfung/-melder (≥5 lx, R21), Fluchtgeräten/
   Schutzbereichen für Menschen mit Behinderung (R22/R23). Quelle: `EN_1838_notbeleuchtung.md:52–61,170–186`.
2. **Lux-Bemessung §4.2/4.3** — Rettungsweg **≥1 lx** Mittellinie flächendeckend, **Ud ≥ 1:40**
   (`:189,190`); **Antipanik ≥0,5 lx** Kernfläche (Rand 0,5 m ausgenommen), Räume/Flächen **>60 m²**
   ohne definierten Weg (`:210`; `GSYSTEMS_Planungshandbuch.md:103`); Arbeitsplätze ≥15 lx (`:221`).
3. **Sichtlinie / Erkennungsweite l = z·h** — z=200 hinterleuchtet (≥500 cd/m²) / z=100 beleuchtet /
   z=300 Schrift; von jeder Stelle muss ein RZ in Fluchtrichtung sichtbar bleiben → begrenzt den
   **RZ-Abstand** (`EN_1838_notbeleuchtung.md:106`; hochmontiert max. 10 m, `Bildlehren_INOTEC.md:94`).

**Zuordnung Beobachtung → Norm:**
- **RZ_PU über Türen / am Ausgang** → §4.1.2 a (R13, Ausgangstür). EG viele **PLPR beidseitig** →
  §4.1.2 e/f (R17/R18, Richtungsänderung/Kreuzung: „beide Richtungen ausleuchten").
- **UG viele SL entlang der Fahrgassen** → 1-lx-Rettungsweg; **SPOT (19×) in der Garage** → Antipanik
  0,5 lx auf der offenen Fläche >60 m² (kein definierter Einzelweg).
- **OG RZ_PU über der Wohnungs-/Ganstür Richtung Stiegenhaus** → §4.1.2 a + Treppe (R14).
- **5× SYSTEM im UG** → Zentralbatterie/Überwachungsanlage (Technikraum), speist die SV-Kreise.
- **RZ_00 (ohne Pfeil, 7× im Katalog/Modelspace)** → Piktogramm E001/E002 **nur mit Pfeil zulässig**
  (`Handbuch_…:90`); `_00` = Deckenmontage direkt über/an der Tür, wo die Tür selbst die Richtung ist.

## 3. din-Symbol-/Layer-Vokabular (gelernt — direkt für unsere Symbol-Naht nutzbar)

**Block-Namensschema:** `<FAMILIE>_<ROLLE>_<PFEIL>` bzw. `<FAMILIE>_RZ_<PFEIL>`.
- **Pfeil-Suffix:** `PU`=unten, `PO`=oben, `PL`=links, `PR`=rechts; `PLPR`/`PRPL`=beidseitig;
  `SO/SU`=schräg oben/unten (`PRSO`,`PLSU`,`PRSOPLSO`…); `_00`=ohne Pfeil (über Tür); `_W90`=
  Wandmontage (Pikto 90° gedreht sichtbar); `_SYM`=nur Symbol. → **45°-Raster wie E DIN 4844.**
- **Rollen (SL):** `_SL_AP`=Antipanik · `_SL_SL`=Fluchtweg · `_SL_TS` · plus `SPOT`/`SPOT_SL`
  (Spot-Aufheller). **Ein Gehäuse, mehrere Rollen (Rolle ≠ Produkt)** — bestätigt
  (`PRODUKTE_SCHRACK_DIN.md:67,150`; din Concept 2 AP3 = Universalkopf).
- **Produkt-Familien:** `STANDARD`, `Concept`(+`_LK3`), `BASIC`, `STRING/STRING1/STRING2`(+`_LA`),
  `Cube`, `INDUSTRY_X32`, `FSU`, `DKM`, `USERDEF`.
- **Sonder-RZ:** `WHEELCHAIR_*`=barrierefrei (Rollstuhl-Fluchtweg, §4.1.2 j/k), `SONDERSTIEGE_*`=
  Sonderstiege, `ISO7010_RZ_*` + `din_*` (Feuerlöscher F001, Hydrant F002, Erste-Hilfe E003,
  Defi E010, DKM/Druckknopfmelder F005, Sammelplatz E007, Notrufstelle E004, Augendusche E011,
  Verweilbereich-Rollstuhl E024, EX-Bereich W002) = die **Sonderstellen** aus §4.1.2 h–k.

## 4. Erkenntnisse für unsere Engine (Kandidaten)

1. **Grün/Gelb-Layer-Trennung** RZ (grün) vs SL/SPOT (gelb) — wir rendern alles grün. Owner fragen,
   ob wir das übernehmen (2 Layer statt einem).
2. **Beidseitige RZ (PLPR) an Kreuzungen/Richtungswechsel** — die din-Praxis setzt sie GENAU dort
   (EG 13×). Unser „gerade"/Doppelpfeil deckt das, aber der Trigger „an jeder Kreuzung/jedem
   Richtungswechsel ein beidseitiges RZ" ist schärfer als heute (wir setzen es an Wasserscheiden).
3. **Antipanik-SPOT auf offenen Flächen >60 m² (UG-Garage)** — unser `flaechen_strategy`-Trigger
   passt; SPOT als eigener Symbol-Typ (rund, rot=0°) ist im Katalog.
4. **SYSTEM/Zentralbatterie-Symbol im Technikraum** — deckt sich mit unserem Gruppenbatterie-Symbol
   (LB-getrieben, #112).
5. **`_00`-RZ (ohne Pfeil) über Türen** — heute nutzen wir immer einen Pfeil-Block; klären, ob
   Deckenmontage-über-Tür ohne Pfeil ein eigener Fall ist.
6. **`SAFETY_LAYER = din_SIBEL_10_emergency_lighting` ist bestätigt korrekt** (byte-genau dieselbe
   din-Konvention).

## 5. Projekt-Verständnis (die 7 Geschosse)

**Wohnbau, 7 Ebenen:** **UG** = Tiefgarage + Technik/E-Schacht (dichteste Notbeleuchtung: lange
Fahrgassen-SL, Antipanik-SPOTs, die 5 Zentralbatterie-Einheiten) · **EG** = Eingangs-/Durchgangs-
ebene mit den Schlussausgängen ins Freie (viele beidseitige RZ an Kreuzungen) · **OG1–OG4** =
Wohngeschosse (kurze Wohnungs-/Ganstüren zum Stiegenhaus → wenige RZ_PU + Gang-Aufheller) · **DD** =
Dachdraufsicht (keine Notbeleuchtung). Das erklärt die Symbol-Verteilung 106/37/9/13/12/3 direkt aus
der Nutzung: **je öffentlicher/größer/wegereicher die Ebene, desto mehr Notbeleuchtung.**

Verwandt: [[EN_1838_notbeleuchtung]] · `PRODUKTE_SCHRACK_DIN.md` · `PROFI_DIN_PLAN_UND_VORSCHRIFTEN.md`
· `bildlehren/Bildlehren_INOTEC.md`.
