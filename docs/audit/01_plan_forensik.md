# 01 — Plan-Forensik (P1 = `DIN-Notbeleuchtungspläne(Beispiele)`)

**Subagent A1 · Scope P1 nur.** Fremdmaterial (DIN/DE-Herkunft, Hersteller **din
Dietmar Nocker Sicherheitstechnik**, Planer AnlagenPlan GmbH / hot architektur ZT
GmbH). Gelesen, zitiert — **nicht ins Repo kopiert**. Belege = (Plan, Seite).

## Geltungs-Tag — Begründung der Einordnung

Die din-Beispiele sind **Wiener Projekte** (Bauträger A-1100/1120/1070 Wien, Planer
A-1100 Wien), **nach EN 1838 gerechnet** (jeder Bericht: „Notbeleuchtungsszene nach
Norm EN 1838"). EN 1838 gilt in AT als **ÖNORM EN 1838** wortgleich → alle
lux-/Ud-/Höhen-Aussagen sind **[AT-verbindlich]** (ÖNORM EN 1838 + OVE E 8101:2025).
Herstellerspezifische Produktwahl, Layer-Farben, Erkennungsweiten-Auslegung und
Stückzahl-Praxis sind **[AT-Referenzpraxis]** (so macht es das din/AnlagenPlan-Büro
in Wien, aber nicht normativ erzwungen). Reine DIN-Zeichenkonventionen ohne AT-Pendant
= **[DE-only]**. Der Aichholzgasse-Polierplan zitiert **OIB-RL 2019** direkt →
**[AT-verbindlich]**.

## Korpus-Übersicht (was P1 wirklich enthält)

| Datei | Art | forensischer Wert |
|---|---|---|
| **Linke Wienzeile / „DIN Plan - geprüft.pdf"** (10 S.) | **echter Notbeleuchtungsplan** UG/EG/OG1–6/DG + Legende | HÖCHSTER: platzierte Symbole, Stromkreis-Labels, volle Typ-Legende A–K |
| **Linke Wienzeile / „DIN-Bericht - geprüft.pdf"** (11 S.) | DIALux-Notberechnung + Produktdatenblätter | Emin/Ud-Sollwerte, Wartungsfaktor, LVK, Höhen-Messebenen |
| Linke Wienzeile / „DIN Imagebilder" | Renderbilder | gering |
| **Barawitzka / LiBer …_Garage.pdf** (9 S.) | DIALux Antipanik/Garage-Nachweis | Ud≤40-Konvention, Antipanik-Produkte, Möbel-Berücksichtigung |
| **Barawitzka / LiBer …_Stiege A.pdf** (10 S.) | DIALux Stiegenhaus-Nachweis | **exakte Leuchten-XY + Montagehöhen**, Stufen-E, 1-per-Podest |
| Barawitzka / LiBer …_Stiege B.pdf | wie Stiege A | Redundanz-Beleg |
| **Aichholzgasse P01–P09** (18 PDF, IdxA/B) | **Architektur-Polierpläne** („POLIERPLAN", hot architektur) — **KEIN Notplan** | nur Brandschutz-Textblock = OIB-RL-Belege |
| din Planungsunterstützung_V25.dxf (11 MB) | echter 7-Geschoss-din-Referenzplan (211 INSERTs) | über `DIN_PLANUNGSUNTERSTUETZUNG_V25_ANALYSE.md` ausgewertet |
| Barawitzka …28.04.2026.dxf (11 MB) | din-support Profiplan (gleiche Familie) | Struktur wie V25 (nicht neu geparst) |
| **11× DWG** (din V25 + Barawitzka + 7 XRef-Geschosse) | Architektur-/Notlicht-Quelle | **BLOCKIERT — ODA nicht installiert** (s. Limitationen) |

25 PDF (davon 18 = Aichholzgasse-Duplikate „(2)"), 2 DXF, 11 DWG. Bestätigt.

---

## A. Befund-Tabelle (jeder Befund: Muster | Häufigkeit | Beleg | Geltungs-Tag | Regel)

| # | Muster | Häufigkeit (n von m) | Beleg (Plan, S.) | Geltungs-Tag | bestätigt/widerspricht Regel-ID |
|---|--------|----------------------|------------------|--------------|-------------------------------|
| F01 | Berechnung nach EN 1838, **Wartungsfaktor 0,8 innen**, keine Reflexionen | 3/3 Berichte | LW Bericht S.2; Baraw. Garage S.2; Stiege A S.2 | [AT-verbindlich] | bestätigt Wartungsfaktor-Slice (`NormAnforderung.wartungsfaktor`) |
| F02 | **Wartungsfaktor 0,57 außen** (dualer WF) | 2/2 Baraw.-Berichte | Baraw. Garage S.2; Stiege A S.2 | [AT-Referenzpraxis] | **NEU — Engine kennt nur einen WF**, kein Außen-WF |
| F03 | Rettungsweg **Emin Mittellinie ≥ 1,00 lx**, **Emin Mittelfläche ≥ 0,50 lx** | 3/3 Berichte (7 Rettungswege) | LW Bericht S.9/11; Baraw. Garage S.7 | [AT-verbindlich] | bestätigt 1-lx-Mittellinie + Antipanik-0,5-lx (Regel A1/A2, Mittellinien-Nachweis #108) |
| F04 | **Ud-Grenze = 1:40**, zwei Schreibweisen: `Ud ≥ 0.025` (LW) **und** `Ud ≤ 40.000` (Baraw.) für dieselbe Regel | 3/3 | LW Bericht S.9; Baraw. Garage S.7 | [AT-verbindlich] | bestätigt Ud-Trigger (Regel A `gleichmaessigkeit_max`); **NEU: zwei Konventionen — Report muss beides kennen** |
| F05 | Rettungsweg als **senkrechte (vertikale) Beleuchtungsstärke „adaptiv"** gemessen, an mehreren Höhen | 3/3 | LW Bericht S.9 (Höhe 0,000 / 0,182 / 2,200 / 2,400 m); Baraw. Garage S.7 (0,000 m) | [AT-Referenzpraxis] | **NEU** — Engine misst horizontal in 2,0 m; din prüft **vertikal** an Objekt-/Türhöhen |
| F06 | **Stiege: horizontale E auf der Gehfläche**, Ē≈3,1 lx, **Emin 1,97 lx**, Emax/Emin 2,76 | 1/1 (Stiege A) | Baraw. Stiege A S.10 (Höhe 4,332 m = Gehebene mittig) | [AT-verbindlich] | bestätigt: Stiege = Rettungsweg 1 lx, Ud « 40 leicht erfüllt |
| F07 | **Genau 1 SL je Stiegenpodest/Geschoss**, gestapelt über die Stiegenhöhe (2,52 → 10,8 m) | 1/1 (Stiege A: 7 RZ + 3 SL, Montagehöhen 2,52/5,40/8,28 bzw. 3,80/6,59/9,59 m) | Baraw. Stiege A S.8–9 | [AT-Referenzpraxis] | bestätigt Treppen-Regel (R14 je Geschoss), präzisiert: **1 Leuchte je Podest, nicht je Stufe** |
| F08 | **Montagehöhe bis 10,8 m** in hohen Stiegenhäusern; Nutzebene 0,02 m, Randzone 0 m | 1/1 | Baraw. Stiege A S.5, S.8 | [AT-Referenzpraxis] | ergänzt lux-Höhe (Regel A4 2,0 m gilt für Flur, **nicht** Stiege) |
| F09 | **RZ-Erkennungsweite als Produktparameter**: Concept-S3 = 32 m, Concept-S2 = 20 m → begrenzt RZ-Abstand | LW: S3×3, S2×2 | LW Plan S.10 (Legende Typ B/C) | [AT-Referenzpraxis] | bestätigt l = z·h RZ-Dichte (RZ-Anzahl-Regel) |
| F10 | **RZ-Piktogramm-Richtung im Parameter**: „Männchen-Oben (Decke)-PU / -PL/PR" = Pfeil unten / links+rechts | LW Legende: PU, PL/PR Varianten | LW Plan S.10 | [DE-only]→[AT-Referenzpraxis] | bestätigt Pfeil-Suffix-Vokabular (PU/PL/PR/PLPR, orientation.py) |
| F11 | **Beidseitige RZ (PLPR) gehäuft in Eingangs-/Kreuzungsebene** | din V25: EG 13× PLPR vs OG je 1× | `DIN_..._V25_ANALYSE.md:30,38,64` (Beleg: V25.dxf) | [AT-Referenzpraxis] | bestätigt R17/R18 (Richtungswechsel/Kreuzung beidseitig); schärfer als „Wasserscheide" |
| F12 | **Getrennter Sicherheitskreis + Bereitschaftsschaltung** für SL in Treppenhäusern & Gängen, eigene Stromkreise | Aichh. Brandschutztext (alle 9 Geschosse) | Aichh. P03 EG S.1 („über eigene Stromkreise … in Bereitschaftsschaltung") | [AT-verbindlich] | bestätigt Kernmission „getrennter Sicherheitskreis" + DL/BL-Feld (`IsBLString`, #96/#98) |
| F13 | **Fluchtrichtung durch grüne Pfeile/Schrift auf Überglasern** kenntlich | Aichh. Brandschutztext | Aichh. P03 EG S.1 | [AT-verbindlich] | bestätigt Pfeil-zur-Tür + Fluchtweg-grün (#111) |
| F14 | **Sicherheitsbeleuchtung eingeschränkt auf Fluchtwege** (OIB-RL 2.2/2.3 Tab.5), GK5 | Aichh. (GK5-Bau) | Aichh. P03 EG S.1 | [AT-verbindlich] | bestätigt OIB-Gate (#87/#88); Räume ohne Fluchtweg → kein Notlicht |
| F15 | **Antipanik-SPOT (rund) auf offenen Flächen / Garage**, gehäuft im UG | din V25 UG: 19 SPOT; Baraw. Garage: 3× AP3 | `V25_ANALYSE.md:29,66` (V25.dxf); Baraw. Garage S.5 | [AT-verbindlich] | bestätigt Antipanik-Flächen-Trigger (>60 m² / kein def. Weg, `flaechen_strategy`) |
| F16 | **Zentralbatterie/Anlage-Symbol im Technikraum (UG)**; Nummer `Anlage/Kreis/Adresse` | din V25: 5× SYSTEM UG | `V25_ANALYSE.md:29,69`; `STROMKREISNUMMER_DWG.md:16` | [AT-Referenzpraxis] | bestätigt Gruppenbatterie-Symbol (#112) + circuit_hint |
| F17 | **Stromkreis-Cap ≈ 20 Leuchten**, Kreise nach Gebäudebereich geschnitten, alternierend gefüllt | Stromkreis-DWG: Anlage1 20/14/18/20/13/14 | `STROMKREISNUMMER_DWG.md:20–24` | [AT-Referenzpraxis] | bestätigt Cap-20-Regel; **kein strenges „gerade/ungerade"-Alternieren**, sondern räumlicher Schnitt |
| F18 | **grün = RZ/Zeichen, gelb = SL/SPOT (Ausleuchtung)** — farbige Layer-Trennung | din V25 (2 Layer) | `V25_ANALYSE.md:20–22` (V25.dxf) | [AT-Referenzpraxis] | **teilw. WIDERSPRUCH** — Engine rendert alles grün; din trennt zweifarbig |
| F19 | **RZ_00 (ohne Pfeil) bei Deckenmontage direkt über der Tür** (Tür selbst = Richtung) | din V25 Katalog | `V25_ANALYSE.md:70–71,100` (V25.dxf) | [AT-Referenzpraxis] | ergänzt Regel 13: nicht immer Pfeil-Block; über-Tür-Fall ohne Pfeil |
| F20 | **1–3 h Batterie-Autonomie** je Leuchte im Produktcode (`…_1-3h`, `RZ-plus_1-3h`) | Baraw. Stiege A (RZ-plus 1-3h, SL 1-3h); LW (115mA/1-3h) | Baraw. Stiege A S.8; LW Bericht S.3 | [AT-Referenzpraxis] | bestätigt Umschaltzeit/Betriebsdauer (Regel D); 1 h Wohnbau, 3 h öffentlich |
| F21 | **Sehr niedrige Leuchtenleistung** (SL 1,3–2,5 W, RZ 2,5–5 W, 53–242 lm) | 3/3 Berichte | LW Bericht S.5–7; Baraw. Garage S.5; Stiege A S.6 | [AT-Referenzpraxis] | Photometrie-Naht (LDT-Katalog #100/#121) — Notbetriebs-Lichtstrom, nicht Vollast |
| F22 | **Möbel in der Berechnung berücksichtigt** (Baraw.) vs. leerer Raum (LW) | Baraw. „unter Berücksichtigung der platzierten Möbel"; LW ohne | Baraw. Garage S.7, Stiege A S.6/10 | [AT-Referenzpraxis] | **NEU** — Verschattung durch Möbel ist zulässige Verschärfung; Engine ignoriert Möbel |
| F23 | **RZ dominiert Wohnbau-Notbeleuchtung** (LW: 62× BASIC E-SIGN Typ F von ~110 Symbolen) | 1/1 (LW-Legende) | LW Plan S.10 (Massenstückliste) | [AT-Referenzpraxis] | Mengengerüst-Kalibrierung: Wohnbau ≈ RZ-lastig, wenige SL |
| F24 | **Wandmontage-Variante** (Concept-WA / `_W90`) neben Deckenmontage | LW Typ B/C/E (WA-PP-G) | LW Plan S.10 | [AT-Referenzpraxis] | ergänzt Montageart-Feld (Decke vs Wand) |
| F25 | **CRI/CCT**: SL/SPOT 4000 K CRI 70; RZ-Signs 3000 K CRI 100 | LW Bericht S.5–7 | LW Bericht S.5 (3000 K/CRI100), S.7 (4000 K/CRI70) | [AT-Referenzpraxis] | Produktdaten-Detail; kein Engine-Trigger heute |

---

## B. NEGATIV-Befunde — Muster in P1, die in `knowledge/extracted/` fehlen

- **N01 (F02) — Außen-Wartungsfaktor 0,57.** Beide Barawitzka-Berichte nennen einen
  **zweiten WF für Außenbereiche (0,57)** neben 0,8 innen (Baraw. Garage S.2, Stiege A
  S.2). Unser Wissen (`LICHTBERECHNUNG_REFERENZ.md`, MEMORY) kennt **nur 0,8/0,57 als
  Alternativwerte**, nicht die **gleichzeitige** Innen/Außen-Anwendung in einem Projekt.
  → Enis-Naht: `wartungsfaktor` müsste bereichsabhängig (innen/außen) sein.
- **N02 (F05) — Rettungsweg als SENKRECHTE (vertikale) Beleuchtungsstärke, an mehreren
  Objekthöhen.** din prüft den Rettungsweg als „Senkrechte Beleuchtungsstärke (adaptiv)"
  bei Höhen 0,000 / 0,182 / 2,200 / 2,400 m (LW Bericht S.9). Unser Wissen prüft die
  Mittellinie **horizontal in 2,0 m Höhe** (`EN_1838…:189`, Regel A4). **Nicht abgedeckt:**
  vertikale Prüfung an Türhöhen/Objekten. Neuer Nachweis-Typ.
- **N03 (F04) — Ud-Schreibweise `≤ 40.000`.** Unser Wissen nennt die Gleichmäßigkeit
  als **1:40 / `gleichmaessigkeit_max`** (Verhältnis). Der Barawitzka-Report schreibt sie
  als **`Ud (Soll) ≤ 40.000`** (Emax/Emin), Linke Wienzeile als **`Ud ≥ 0.025`** (Emin/Emax).
  Dieselbe Norm, gespiegelte Kennzahl — im generierten Bericht müssen **beide Richtungen**
  korrekt beschriftet sein, sonst Fehl-„ok".
- **N04 (F07/F08) — Montagehöhe-Staffel im Stiegenhaus (2,52 → 10,8 m), 1 Leuchte je
  Podest.** Unser Wissen hat Höhe generisch (2,0 m lux-Ebene, hochmontiert ≤ 10 m RZ).
  **Nicht abgedeckt:** die konkrete Stiegen-Praxis „eine SL + RZ je Geschoss-Podest,
  gestapelt bis 10,8 m", die 10-m-Grenze wird bei 10,8 m sogar überschritten.
- **N05 (F22) — Möbel-Verschattung.** din rechnet in Garage/Stiege „unter Berücksichtigung
  der platzierten Möbel". Unser lux-Modell ist möbelfrei (leerer Raum). Kein Trigger im Wissen.
- **N06 — QR-Code / Adressier-Layer (`din_SIBEL_62_QRCode`).** din legt QR-Codes je Leuchte
  an (`V25_ANALYSE.md:23`, `STROMKREISNUMMER_DWG.md:32 QRGuid`). Kein Konzept in unserem
  Ausgabe-/Symbol-Modell (wäre reine Wartungs-Metadata).
- **N07 — `NBF 100 %` (Notbetriebs-Faktor je Leuchte).** Alle Produktdatenblätter führen
  `NBF = 100 %` (Notlicht-Lichtstrom = Vollstrom bei diesen Dauerlicht-LEDs). Unser
  LDT-Katalog kennt Notbetriebs-Photometrie, aber den **NBF als explizites Feld** nicht.

---

## C. Detail-Belege (Zitate)

### Linke Wienzeile — Typ-Legende (Plan S.10, hochauflösend gelesen)
```
Typ A  1× SU 6P ESF30                              (Anlage/Versorgungsgerät ESF30)
Typ B  RZ  Concept 2 AP3 / WA-PP-G / S3-Px Erkennungsweite 32 m   Männchen-Oben-PU / PL/PR
Typ C  RZ  Concept S2-Px Erkennungsweite 20 m                     Männchen-Oben-PU / PL/PR
Typ D  7× Concept 2 SL3 PLC24                      (Sicherheitsleuchte)
Typ E  Concept 2 AP3 / WA-PP-G                     (Wandmontage)
Typ F 62× BASIC 2 E-SIGN plus PLC 115 mA           (RZ-Escape-Sign — dominant)
Typ G 10× BASIC 2 E-LED RZ1/SL PLC 115 mA
Typ H  4× BASIC 2 E-LED RZ1/SL PLC 115 mA
Typ I 18× STRING 2 eco spot SL DA R 4000K PLC      (SL, Deckenanbau, rund)
Typ J  7× STRING 2 eco spot AP2 DA R 4000K PLC     (Antipanik)
Typ K  1× STRING 2 eco spot AP DA R 4000K PLC      (Antipanik)
```
Massenstückliste (Plan S.10): 62 E-SIGN + 14 E-LED RZ1/SL + 18 SL + 7 AP2 + 1 AP + 1 ESF30.
Stromkreis-Labels im Gang sichtbar: `1/6/5`, `1/5/8`, `F2/12` (Anlage/Kreis/Adresse-Schema, F04/F16).

### Barawitzka Stiege A — exakte Leuchtenkoordinaten (S.8–9)
RZ „BASICsc 2 E-SIGN_RZ-plus_1-3h" (7×): u.a. (6,342 / 1,891) auf **2,520 / 5,400 / 8,280 m**
(= je Geschoss-Podest gestapelt); (1,317 / 0,066) auf 5,0 / 7,9 / 10,8 m.
SL „BASICsc 2 E-SIGN_SL_1-3h" (3×): (3,423 / 0,052) auf **3,800 / 6,590 / 9,590 m**.
Stufen-Gehfläche (S.10): Höhe 4,332 m, Ē 3,13 lx, Emin 1,97 lx, Emax 5,43 lx → weit über 1 lx.

### Aichholzgasse P03 EG — Brandschutz-/Elektrotext (S.1, OIB-verbindlich)
> „Sicherheitsbeleuchtung ober- und unterirdisch sowie Garage gemäß OIB-RL 2.2/2.3
> Tabelle 5 ‚Sicherheitsbeleuchtung eingeschränkt auf Fluchtwege'. Die Sicherheitsleuchten
> werden über **eigene Stromkreise** in Treppenhäusern und Gänge in **Bereitschaftsschaltung**
> ausgeführt … Wo es zur Deutlichmachung der Fluchtrichtung erforderlich ist werden auf den
> Überglasern durchscheinende Kennzeichnungen, **Richtungspfeile, Schriften … in grüner
> Farbe** angebracht." (Gilt OIB-RL Ausgabe 2019, GK 5.)

---

## D. Limitationen

- **11 DWG blockiert** (din V25 + Barawitzka + 7 XRef-Geschosse): **ODA File Converter
  nicht installiert** → nicht in DXF wandelbar, nicht gelesen. Für die din-V25- und
  Barawitzka-DWG existieren aber gelesene DXF-Zwillinge (via V25-Analyse), sodass die
  Struktur-Befunde F11/F15–F19 belegt bleiben; die 7 Architektur-XRefs (Raum-Labels)
  bleiben ungelesen. **Nicht erzwungen.**
- Aichholzgasse = **Architektur-Polierpläne, kein Notplan** — liefert nur den (wertvollen)
  OIB-Normtext, keine Symbol-Platzierung. 18 der 25 PDF sind IdxA/B-Duplikate.
- Scan-Qualität der Linke-Wienzeile-Pläne begrenzt die pixelgenaue Einzel-Symbol-Geometrie
  (Abstände am Raster nur qualitativ; die Legende + der Bericht liefern die harten Zahlen).
