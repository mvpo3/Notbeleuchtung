# Stromkreisnummern-Schema aus dem DIN-Planungsplan (Stromkreisnummer.dwg)

**Quelle:** `knowledge/sonstiges Wissen Notbeleuchtung/din Planungsunterstützung_Stromkreisnummer.dwg`
(864 KB DWG, via ODA-Konverter → DXF gelesen; Konvertat:
`din Planungsunterstützung_Stromkreisnummer.dxf` daneben). Elektromontageplan
1.UG/EG/1.OG (drei Xref-Etagen), DIN Notlicht (din-notlicht.at, GALA-Angebot
08.06.2022). Schließt den Wissens-Gap aus
`PROFI_DIN_PLAN_UND_VORSCHRIFTEN.md` („ODA-Konverter nötig").

## Kernbefund: das Nummern-Schema

**`LABELING1 = Anlage / Stromkreis / Adresse`** — z.B. `1/5/7`:

| Ebene | Bedeutung | Beleg im Plan |
|---|---|---|
| **Anlage** | Gruppenbatterie-System (je eines pro Versorgungsbereich) | 2 SYSTEM-Symbole: `Anlage_1_UG`, `Anlage_2_OG_links` — je **SU 6P NET E30**, Typ A, `Stromkreise=6`, Montage „E30 mit BP" |
| **Stromkreis** | Abgang der Anlage, 1…6 | beide Anlagen nutzen alle 6 Kreise |
| **Adresse** | Leuchten-Adresse im Kreis (PLC24-Bus, `Technology=PLC24` auf 139/140 Leuchten) | fortlaufend je Kreis, max. beobachtet **20** |

**Belegung real (138 adressierte Leuchten, 81 RZ + 57 SL):**
Anlage 1 (UG): Kreise 1–6 = 20/14/18/20/13/14 (99 Leuchten) ·
Anlage 2 (OG links): 7/7/11/6/4/4 (39 Leuchten).
→ Praxis-Regel: **≈20 Leuchten je Stromkreis als Obergrenze**, Kreise nach
Gebäudebereich geschnitten, Reserve bleibt (Anlage 2 halb voll).

## Symbol-Datenmodell (deckungsgleich mit Barawitzka-Profiplan)

Jedes Leuchten-INSERT trägt ATTRIBs: `TYPE` (RZ/SL/SYSTEM/PROJECT),
`TYPENUMBER` (**Typ-Letter A…P**, Typ A = die Anlage selbst), `TYPENAME`
(z.B. „Concept 2 AP3 PLC24"), `LABELING1` (Nummern-Schema oben), `INFOTEXT`
(`S2+WW`, `S2+DE`, „Druckknopfmelder ISO 7010-F005"), `CircuitString`/
`AddressString`, `System` (GUID → Anlage), `QRGuid`, `ProductFamily`/
`ProductName`/`MountingMethod`/`Technology`/`SelectedArticleNumber`
(Schrack-Artikel, z.B. 9020095009)/`Leistungsklasse` (LK3/LK5)/
`AccessoriesAsText` (u.a. „Concept-S2-PU — **Erkennungsweite 20 m**").

**`IsBLString` = True/False = Bereitschafts-/Dauerlicht je Leuchte** (41 True /
51 False / 46 ohne Feld) — exakt die `schaltungsart` DL/BL des
Symbol-Datenmodell-Contracts (PR #96/#98).

**Obfuskierung:** viele ATTRIB-Werte sind als `#v1` + Base64 kodiert; Klartext =
`bytes(b ^ 0xFF for b in base64.b64decode(wert[3:])).decode('cp1252')`.
(`LABELING1`/`TYPE`/`TYPENAME`/`TYPENUMBER`/`INFOTEXT` liegen im Klartext.)

**Block-Vokabular:** `STANDARD_RZ_PU` (×60, Piktogramm umlaufend),
`STANDARD_RZ_PLPR` (×24, beidseitig), `STANDARD_RZ_PL`/`_PR` (einseitig),
`STANDARD_SPOT` (×40), `STANDARD_SL` (×29), `STANDARD_SYSTEM` (Anlage) —
gleiche PL/PR/PLPR-Systematik wie im Barawitzka-Plan.

## Engine-Empfehlungen (Leonis/Hauptengine)

1. **Stromkreis-Zuweisung als eigener Pass** nach der Platzierung: Leuchten →
   Anlage (Versorgungsbereich/Geschoss-Cluster) → Kreis (räumlich geschnitten,
   **Cap ≈ 20 Adressen**) → fortlaufende Adresse. Ausgabe im Format
   `Anlage/Kreis/Adresse` als NODEID-Label (NODEID je Leuchte existiert seit #73/#74).
2. **Belegungsliste erweitern:** die Stromkreis-Belegungsliste (DL/BL, #74) um
   Spalten Anlage + Adresse ergänzen — dann ist sie deckungsgleich mit der
   DIN-Praxis (`1.xlsx`-kompatibel).
3. **Anlage als platzierbares SYSTEM-Symbol** (Gruppenbatterie, E30-Montage) —
   Kandidat für den Sonderstellen-Contract (#93/#95: BMZ-artige Pflicht-POIs).
4. `IsBLString`→`schaltungsart` bestätigt das Feld-Design von #96 — keine Änderung nötig.

## Für Enis (normwissen)

- Erkennungsweite 20 m für Concept-S2-PU (Zubehör-Text) — deckt sich mit dem
  Schrack-Katalog-Wissen (Erkennungsweiten je Familie).
- Leistungsklassen LK3/LK5 + Artikelnummern → Produktdaten-Quelle für
  `stromaufnahme_ma`-Follow-up.

---

# Voll-Analyse (2026-09-05) — alles jenseits des Nummern-Schemas

Zweiter, vollständiger Sweep (Layer/Blöcke/alle 18 Attribute dekodiert/ACAD_TABLE).

## 1. Komplettes DIN_SIBEL-Layer-Schema (mit ACI-Farben)

`10_emergency_lighting` (90=grün) · `10_…_yellow` (40) · `11_emergency_lighting_system` (90) ·
**`30_color_green`/`31_color_white`(255)/`32_color_black`(250)/`33_color_yellow`(40)/
`34_color_sperr`(10)** — Symbol-Innenfarben als eigene Layer! · **`50_type_name` ·
`51_typenumber`** (90) · `52_info` · **`53_additional_1`/`54_additional_2`** (114) ·
`61_labeling` · **`62_QRCode`** · `63_luminaire_ID` · `70_legend`(+`_green`(114)/`_white`(7)/
`_yellow`(40)) · `99_general` · **`din_brandabschnitte` + `din_brandabschnitte_virtuell`** (1=rot).
→ Unser Render nutzt erst eine Teilmenge; Brandabschnitts-Layer existieren als eigene Ebene.

## 2. Symbol-Blöcke: Varianten + ECHTE Größen (mm, scale=1!)

| Block | Anz. | Größe (mm) | Bedeutung |
|---|---|---|---|
| `STANDARD_RZ_PU` | **60** | 994×330 | RZ **Pfeil unten** — DIE Standardvariante (bestätigt Owner-Regel!) |
| `STANDARD_RZ_PLPR` | 24 | 994×**660** | beidseitig — DOPPELT hoch (2 Pfeilzeilen) |
| `STANDARD_RZ_PL` / `_PR` | 5/4 | ~994×330 | links/rechts |
| `STANDARD_SL` | 29 | 993×330 | Sicherheitsleuchte (rechteckig, NICHT rund!) |
| `STANDARD_SPOT` | **40** | 831×346 | eigene SPOT-Kategorie (TYPE trotzdem 'SL') |
| `STANDARD_SYSTEM` | 4 | 993×333 | Anlagen-Symbol (2× je Plan-Ansicht) |

Profi-Symbole sind ~1 m breit (unsere: RZ 580, Aufheller 342) und **unrotiert skaliert 1:1 in mm**.

## 3. Attribut-Schema vollständig dekodiert (18 Tags je INSERT)

Klartext: `TYPE` (RZ/SL) · `LABELING1` (Anlage/Kreis/Adresse) · `TYPENAME` · `TYPENUMBER` ·
`INFOTEXT`. `#v1`-XOR-kodiert: `ProductFamily/ProductName/MountingMethod/Technology/
SelectedArticleNumber/System/CircuitString/AddressString/IsBLString/Leistungsklasse:
SelectedValue/AccessoriesAsText/QRGuid`.

**Dekodierte Wertewelten (194 Leuchten):**
- **TYPENAME:** `Concept 2 AP3 PLC24` (88!) · `STRING 2 eco spot AP/SL DE 4000K PLC` (16/9) ·
  `Concept 2 RZ1 PLC24` (7) · **`BASIC 2 E-LED RZ1/SL PLC (115mA)`** (7 — Stromaufnahme
  IM Produktnamen!) · `STRING 2 power spot` (4) · `SU 6P NET E30` (2, **Art. 5188100**).
- **MountingMethod-Vokabular:** `Wandausleger parallel` (48) · `Deckeneinbau` (46) ·
  `Deckenaufbau` (29) · `Wandaufbau` (14) · `E30 mit BP` (2, Anlagen).
- **Leistungsklasse:** LK3 (85) / LK5 (5) · **Technology:** durchgehend PLC24.
- **INFOTEXT-Codes:** `S2+WW` (45) = S2-Scheibe + Wandwinkel · `S2+DE` (17) = + Decken-
  einbaukit · `Druckknopfmelder ISO 7010-F005` (3!) · Anlagen-Namen (`Anlage_1_UG`, …).
- **System-GUID:** exakt 2 GUIDs (100/40 Leuchten) = **maschinenlesbare Leuchte→Anlage-
  Zuordnung** (die Basis des Anlage-Anteils von LABELING1).
- **TYPENUMBER:** Letter mit SUB-Varianten (`Typ B1`/`Typ B2` getrennt!), bis `Typ O`.
- Anlagen-Verteilung: Anlage 1 = 99 Leuchten, Anlage 2 = 39.

## 4. ACAD_TABLE = die echte Legende — MIT Zubehör-Zeilen

Kopf `Stk. | Symbol | Typ | Artikel-Nr. | Beschreibung`; je Typ folgen **Zubehör-Zeilen als
eigene Artikel**: z.B. Typ C = `9020095009 Concept 2 AP3 PLC24` + `9020000024
Concept-S2-PL/PR — Erkennungsweite 20m` (die Piktogramm-Scheibe!) + `9020000071
Concept-DE/WE` (Einbaukit). → Eine Profi-Stückliste führt **Leuchte + Scheibe + Montagekit
getrennt** mit Stückzahlen.

## 5. Neue Engine-Empfehlungen aus der Voll-Analyse

1. **Symbolgrößen-Option:** Profi zeichnet ~1 m breite Symbole (1:100-lesbar) — unsere sind
   1/3 davon; Skalierungsfaktor als Render-Option erwägen (Owner-Geschmack abfragen).
2. **SPOT als eigene Darstellungs-Kategorie** (40× im Profi-Plan; TYPE bleibt SL) —
   Katalog-/Symbol-Mapping um Spot erweitern, wenn Produkte gewählt werden.
3. **Stückliste um Zubehör-Zeilen** (Scheibe EW-xx, DE/WE-Kit, WW) — Artikel-Logik:
   INFOTEXT-Codes tragen die Zubehör-Wahl je Leuchte.
4. **System-GUID-Muster** für unseren Stromkreis-Pass: Leuchte→Anlage als explizite
   Zuordnung statt Ableitung; STANDARD_SYSTEM-Symbol im Plan platzieren (wir haben
   noch kein Anlagen-Symbol).
5. **Brandabschnitts-Layer** (`din_brandabschnitte(_virtuell)`) — Naht zu Digest #14
   (Kreis je Brandabschnitt) und zur Muthgasse-Brandabschnitts-Erkenntnis.
6. `TYPENUMBER`-Sub-Letters (B1/B2) — unsere Typ-Letter-Stückliste (#105) kann Sub-
   Varianten bekommen, wenn gleiches Produkt mit anderem Zubehör auftritt.
7. **Stromaufnahme aus TYPENAME parsbar** (`(115mA)`) — Quelle für Enis'
   `stromaufnahme_ma`-Follow-up.
