# Wissens-Digest — Profi-DIN-Plan + Vorschriften (extrahiert 2026-08-31)

Quellen: echter professioneller Notbeleuchtungsplan `DIN-Notbeleuchtungspläne(Beispiele)/
din_support_ReMi_Barawitzkagasse_28.04.2026.dxf` (11 MB, R2018, mm) + `knowledge/sonstiges
Wissen Notbeleuchtung/` (Vorschriften-Kurzübersicht AT/DE, Referenzbilder). Extrahiert via
ultracode-Fan-out (7 Agenten) + inline ezdxf-Analyse.

---

## 1. Profi-Plan-Konventionen (aus dem echten DXF — wie Profis wirklich planen)

### 1.1 Profi-Stückliste (Barawitzkagasse) — Typ-Letter → Produkt → Anzahl

| Typ | Art | Anz | Produkt (TYPENAME) | Anmerkung |
|-----|-----|----:|--------------------|-----------|
| A | RZ | 20 | BASIC 2  E-SIGN RZ plus DA | dominante RZ-Variante |
| B | RZ | 5 | CONCEPT 2  AP WA  **EW 20m** | Erkennungsweite im Namen |
| C | RZ | 3 | BASIC 2  E-LED RZ1/AP WA | |
| D | RZ | 2 | BASIC 2  E-LED RZ2 DA | |
| E | RZ | 2 | CONCEPT 2  SL DA  **EW 20m** | |
| F | RZ | 1 | CONCEPT 2  AP WA90  **EW 20m** | |
| G | SL | 6 | BASIC 2  E-LED RZ1/AP DA | |
| H | SL | 6 | BASIC 2  E-SIGN SL WAP | |
| I | SL | 1 | CONCEPT 2  AP WA | |

**~33 RZ + 13 SL + 2 Zentralen.** Produktfamilien **BASIC 2 / CONCEPT 2**. Montage-Suffixe
`AP`=Aufputz, `WA`=Wand, `WA90`=Wand 90°, `WAP`=Wand-Aufputz, `DA`=Decken-/Direkt-Anbau.
**„EW 20m"** = Erkennungsweite direkt im Produktnamen → bestätigt `l = z·h`.

### 1.2 RZ-Richtungsvarianten als eigene Blocks ↔ unser `richtung`-Konzept

| Profi-Block | Anz | Bedeutung | Unser `richtung` |
|-------------|----:|-----------|------------------|
| `STANDARDMASK_RZ_PLPR` | 12 | Pfeil links **+** rechts = **beidseitig** | **`beidseitig` (NEU!)** |
| `STANDARDMASK_RZ_PL` | 11 | Pfeil links | `links` |
| `STANDARDMASK_RZ_PU` | 7 | Pfeil unten/oben (vertikal) | `unten`/`oben` |
| `STANDARDMASK_RZ_PR` | 7 | Pfeil rechts | `rechts` |
| `STANDARDMASK_SL` | 16 | Sicherheitsleuchte | SL |
| `STANDARDMASK_SYSTEM` | 2 | Zentralbatterie/Adresse | CPS-Knoten |

Profis nutzen **diskrete Richtungs-Blocks** (nicht nur Rotation). `RZ_PLPR` (beidseitig, mit 12
die häufigste RZ-Variante) sitzt in der Flur-Mitte zwischen zwei Ausgängen — unser
`richtung_durch_tuer` kennt das noch nicht. Rotation (0°/270°) wird **zusätzlich** genutzt.

### 1.3 DIN_SIBEL-Layer-Schema (28 Layer, semantisch getrennt)

```
din_SIBEL_10_emergency_lighting (+_white/+_yellow)  Leuchten-Geometrie
din_SIBEL_11_system  / _12_modules                  Zentralbatterie/System · Module
din_SIBEL_30..34_color_green/white/black/yellow/red/sperr  Farb-/Zustandsebenen
din_SIBEL_40_UMRISS                                 Symbol-Umriss
din_SIBEL_50_type_name / _51_typenumber             TYPENAME · Legenden-Letter
din_SIBEL_52_info / _53/_54_additional              Zusatzinfo
din_SIBEL_61_labeling / _62_QRCode / _63_luminaire_ID  Beschriftung · QR · Leuchten-ID
din_SIBEL_70_legend_green/white/yellow              Stücklisten-Legende
din_SIBEL_99_general
```
`_34_color_..._sperr` = eigener Layer für **gesperrte Zustände** → Layer-Farbtrennung ist
bereits **dynamik-fähig** (adaptive Fluchtweglenkung grün=aktiv/rot=gesperrt).

### 1.4 Reiches Symbol-Datenmodell (Block-Attribute je Leuchte)

Jedes Symbol trägt einen vollständigen Produkt-/Wartungs-Datensatz (weit mehr als unser
`catalog_key`): `TYPE`(RZ/SL) · `TYPENAME`(Produkt) · `TYPENUMBER`(Legenden-Letter Typ A/…) ·
`QRGuid`(Wartungs-Scan) · `NODEID1/2`(Zentralbatterie-Adresse) · `ProductFamily`/`ArticleNumber`
(codiert) · `MountingMethod`(AP/WA/DA) · `Technology`/`SwitchMode` · `Rotation`.

---

## 2. Normwissen aus den Vorschriften (AT/OIB + DE/VDE)

### 2.1 EN-1838-Lichttechnik (AT & DE identisch) — Norm-Default-Ebene

| Bereichstyp | E_min | Gleichmäßigkeit | Trigger |
|-------------|-------|-----------------|---------|
| **Rettungsweg** (Mittellinie horiz.) | ≥ 1 lx | ≤ 40:1 | Streifen ≤ 2 m; > 2 m → Antipanik |
| **Antipanik** (freie Bodenfläche) | ≥ 0,5 lx | ≤ 40:1 | ab **≥ 60 m²**, 0,5 m Rand aus |
| **Arbeitsplatz bes. Gefährdung** | ≥ 15 lx **&** ≥ 10 % Allg. | ≤ 10:1 | in ≤ 0,5 s |
| **Hervorzuhebende Stellen** | **5 lx vertikal** | — | Leuchte < 2 m |
| **Barrierefreie WC/Dusche** | ≥ 1 lx horiz. | — | > 8 m² → Antipanik |
| **Betriebs-/Schalträume** | ≥ 0,5 lx Boden; 5 lx Schalttafel | — | — |
| **Hallenbad** | 5 lx Wasseroberfläche + Umrandung | — | Sonderfall |

**Erkennungsweite `l = z·h`:** z=100 beleuchtet/angestrahlt, **z=200 hinterleuchtet**
(Rettungszeichenleuchte); h=Piktogramm-Höhe. → z-Fallunterscheidung fehlt uns noch.

**Harte Konstanten:** „nahe" = **< 2 m** (bindend) · **2-Leuchten-Redundanz** je
Rettungswegabschnitt (EN 1838 §5.1.8) · Montagehöhe 2,0–3,0 m, Zeichen ≥ 2,0 m ·
Fluchtweg-Breitenschwelle 2 m.

**Hervorzuhebende Stellen (5 lx vertikal, Leuchte < 2 m):** Erste-Hilfe-Stellen/-Kästen,
Brandbekämpfungs-/Meldeeinrichtungen (BMZ/Brandmelder), Flucht-/Rettungspläne (ISO 23601),
behindertengerechte Sicherheitseinrichtungen, Aufzugs-Alarmruf, manuelle Türentriegelungen.

### 2.2 Pflicht-Platzierungspunkte für SL (EN 1838 — RaumProvider muss finden)

nahe jedem Notausgang · nahe Treppen (jede Stufe) + jeder Niveauänderung · an
Richtungsänderungen · bei jeder Gang-/Flurkreuzung · nahe letztem Notausgang + außerhalb bis
sicherer Bereich · Aufzugstüren-Flure bis zum nächsten Rettungsweg.

### 2.3 Gebäudeklassen-Pflichten + Betriebsdauern

**AT-Ausbaustufen (OIB):** `eingeschränkt` (nur Fluchtwege) vs. `uneingeschränkt` (+ Antipanik
Versammlung > 20 m², Fahrtreppen, Aggregat-/Schaltanlagenräume).

**Nennbetriebsdauer AT (OVE E 8101 Tab. 56.A.1.AT):** GK4/GK5, kleine Schulen/Hotels
(10–100 Betten), Verkauf 200–3000 m², Versammlung ≤ 240 P → **1 h** · große Schulen > 3200 m²,
Verkauf > 3000 m², Versammlung > 240 P → **3 h** · Beherbergung > 100 Betten, Pflege > 16
Betten → **8 h** · Krankenhaus → **24 h** · Hochhaus FLN 22–32 m = 3 h / > 32 m = 8 h.

**Bemessungsbetriebsdauer DE (DIN VDE V 0108-100-1):** Versammlung/Verkauf/Restaurant/Bühne
3 h · Garage/Arbeitsstätte 1 h · Beherbergung/Heim 8 h · Schule 3 h · Krankenhaus 24 h ·
Wohnhochhaus 8 h.

**Umschaltzeiten:** RZ Dauerbetrieb · allgemein ≤ 1 s · bes. Gefährdung ≤ 0,5 s · Hochhaus/
Garage/Beherbergung/Schule 15 s.

**Flächen-/Zahlen-Trigger:** Antipanik ≥ 60 m² · Toiletten/Umkleiden > 8 m² → Antipanik ·
Arbeitsräume: SL ohne Tageslicht ab 30 m², mit Tageslicht ab > 100 m² (AStV) · **Auto-
Prüfeinrichtung (EN 62034) Pflicht ab > 20 SL** im Gebäudeteil.

**Stromquellen:** EB (Einzelbatterie) · LPS (Gruppen-/Zentralbatterie, < 100 Leuchten keine
E-Betriebsstätte) · CPS (Zentralbatterie, > 2 kWh eigener Raum) · SA (Aggregat, ≤ 0,5 s).

**Verdrahtung (OVE R 12-2 Bild 8.9):** je Geschoß + Treppenhaus = eigener Brandabschnitt =
eigener Endstromkreis · CPS im Keller (abgeschlossene E-Betriebsstätte) · Steigleitung Typ A
(TRVB 110 B), E30-Dosen je Geschoß.

**Normen-Stände:** OVE E 8101:2025-10 · OVE R 12-2:2025-10 · OIB-RL 2 (Mai 2023) ·
OVE EN 50172:2024-11 · ÖNORM EN 1838:2025-03.

---

## 3. Engine-Empfehlungen (priorisiert; Aufwand S/M/L)

### P0 — Naht-kritisch, hoher Hebel
1. **RZ-Richtungsvarianten als Blocks** + `richtung=beidseitig` (PLPR) NEU im Contract — **Contract+F1, M**
2. **DIN_SIBEL-Layer-Schema** im Render statt Ad-hoc — prüfstellen-kompatibel — **Hauptengine, M**
3. **EN-1838-Lux-Grenzwerte als NormRegelwerk** (1/0,5/15/5 lx + Gleichmäßigkeiten) — **F2, M**
4. **`z`-Fallunterscheidung** (100 beleuchtet / 200 hinterleuchtet) in `l=z·h` — **F2+F1, S**
5. **„nahe" = < 2 m** als harte Konstante — **F2+F1, S**

### P1 — Datenmodell & Prüfbarkeit
6. **Platzierung um `TYPENAME/TYPENUMBER/luminaire_ID/MountingMethod/Technology`** erweitern — **Contract+F1, M**
7. **Stückliste als Typ-Letter-Legende** (Gruppierung nach TYPENUMBER) — **Hauptengine, M**
8. **2-Leuchten-Redundanz** je Rettungswegabschnitt (§5.1.8) als Invariante — **F1, S**
9. **QR/`QRGuid` + `NODEID`** je Leuchte (Wartung/Adressierung) — **Hauptengine, M**
10. **Pflicht-Platzierungspunkte-Katalog** (Ausgang/Treppe/Kreuzung/Aufzugsflur…) — **F1+Selman, L**

### P2 — Gebäudeklassen-Logik & Zukunft
11. **Anwendungsfall-Klassifikation** (GK/Nutzung/Fläche/Personen → OIB-Stufe + Betriebsdauer + Stromquelle) aus LB — **F2, L**
12. **Flächenbasierte Bereichs-Trigger** (Antipanik ≥ 60 m², WC > 8 m², Arbeit 30/100 m²) — **F1, M**
13. **Auto-Prüfeinrichtungs-Flag** > 20 SL → EN-62034-Hinweis — **Hauptengine, S**
14. **Getrennter Sicherheitskreis modellieren** (Geschoß/Brandabschnitt, E30, NODEID) — **Hauptengine, L**
15. **Backlog: adaptive Fluchtweglenkung** (`richtung`-Zustand grün/gesperrt, Mehrfachrouten) — **Contract+F1, L**

### Sofort-Wins (je S, echte Norm-Lücken): #4 (z-Fall), #5 („nahe" < 2 m), #8 (2-Leuchten-Redundanz).

---

## 3b. Stromkreis-Belegungsplan (`1.xlsx`, Sheet „Stromkreise SU")

Profi-Verdrahtungsdoku (Inbetriebnahme-Vorlage, Version 3.4): Bauvorhaben/Anlage/verantwortl.
Monteur, dann je **Anlage → Stromkreis-Nummer → Leuchtenbelegung**:

| Feld | Beispiel | Zweck |
|------|----------|-------|
| Leuchten-ID | (matcht `din_SIBEL_63_luminaire_ID`) | eindeutige Leuchte |
| Bezeichnung (≤ 20 Z.) | `BASIC 2  E-SIGN plus 115mA DA` | Produkt |
| Beschreibung (≤ 50 Z.) | Standort/Raum | Freitext |
| **Schaltungsart** | **DL / BL** | **Dauerlicht** (maintained, RZ) / **Bereitschaftslicht** (non-maintained, SL) |
| Stromstärke | **115 mA / 350 mA** | Kreis-Dimensionierung (Leuchten je Kreis) |

**Neue Engine-Erkenntnisse:** (a) **`Schaltungsart` DL/BL** ist ein Pflicht-Attribut je Leuchte
(RZ = Dauerlicht, SL oft Bereitschaftslicht) — gehört ins Symbol-Datenmodell (Empf. #6) und
speist den Prüfbericht (RZ MUSS Dauerbetrieb). (b) **Leuchten-Stromstärke** (115/350 mA) treibt
die **Stromkreis-Belegung** (max. Leuchten je Endstromkreis) — konkretisiert Empfehlung #14.
(c) Struktur `Anlage → Stromkreis → Leuchten-ID` ist die Ziel-Datenstruktur für den getrennten
Sicherheitskreis. → **Empfehlung #14 erweitern:** Ergebnis soll eine Stromkreis-Belegungsliste
(je Kreis: Leuchten-IDs + Schaltungsart + Summenstrom) exportieren, kompatibel zu dieser Vorlage.

## 4. Nicht extrahiert / Gaps
- ~~`sonstiges Wissen/din Planungsunterstützung_Stromkreisnummer.dwg` — ODA-Konverter nötig~~
  **ERLEDIGT 2026-09-04** (dwg_input-Slice): extrahiert nach `STROMKREISNUMMER_DWG.md` —
  Schema `Anlage/Stromkreis/Adresse`, Cap ≈20 Leuchten/Kreis, `IsBLString`=DL/BL.
- `sonstiges Wissen/DIN4708_Bedarfskennzahl Eichholzgasse.pdf` — **OFF-TOPIC** (Trinkwarmwasser-Bedarfsnorm), NICHT ins NormRegelwerk.
- `.dwl/.dwl2` = AutoCAD-Lock (jemand hat die DWG offen) — nur der `.dxf`-Export wurde gelesen.
