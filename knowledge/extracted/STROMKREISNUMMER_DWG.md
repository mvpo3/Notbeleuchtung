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
