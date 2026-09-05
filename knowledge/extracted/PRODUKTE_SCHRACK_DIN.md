# Wissens-Digest — Produktsortimente Schrack Technik + DIN Notlicht (Web-Recherche 2026-09-05)

Quellen: schrack-technik.de / schrack.at (Shop + Know-how-CIP) und din-notlicht.com
(Website + 3 Original-PDFs: BASIC-2-Übersicht, CONCEPT-2-Katalog 22 S. Stand 03/2025,
SU-NET-Folder 02/2025). Recherchiert via 2 parallele Web-Agenten; Auftrag des Owners:
alle Produkte + Datenblätter beider Hersteller sichten.

---

## Teil A — Schrack Technik (Notleuchten)

### Sortimentsstruktur

1. **Rettungszeichenleuchten** — Familien K2, K3, K5, KB, KC, KM, KS, KW, KX,
   A-Serie (AI/AM/AX), WHX/WHG (Würfel), FM (dynamisches Leitsystem).
2. **Aufhellungs-/Sicherheitsleuchten** — IL, K6, KWI, KMB, EE, WER, WEF, WAF, ZA, DLE.

Fast jede Familie in 3 Elektronik-Varianten (Artikelnummern-Suffix):
Einzelbatterie Autotest/SelfControl (`S`/`SC`) · Einzelbatterie WirelessControl (`W`) ·
Zentralbatterie (`E`/`EL`). Gemeinsam: **BL/DL per Konfiguration umschaltbar** ·
Autonomie 1h/3h/8h wählbar (Auslieferung 3h) · LiFePO4-Akkus (neu) · ISO-7010-Piktos ·
„Cool"-Versionen bis −25/−30 °C · Artikelschema `NL`+Familie+Montage(U/D/W/E)+Konfig+Suffix.

### Rettungszeichenleuchten (Kernwerte)

| Familie | EW (m) | Leistung/Lichtstrom | IP | Besonderheit |
|---|---|---|---|---|
| K2 / K3 | 27 | 3 W HP-LED | IP44 | Autotest, Kinoschaltung, 1/2/3/8h |
| K5 | 20 | 130–190 lm / 3 W | **IP65**/IK08 | Feuchtraum; auch als SL nutzbar |
| KB (modular) | **14/22/30** je Steckscheibe | 300 lm@1h / 150 lm@3h | — | 1 Gehäuse, 3 Scheiben |
| KC / KM / KS / KW / KX | ~14–24 | KM: 200 lm / 2 W | tw. IP54 | Scheiben-/Design-/Schmalbauformen |
| A-Serie AI/AM/AX | **15/22/30** | AM: 3,3 W DL / 0,9 W BL | IP40 | Design weiß/anthrazit |
| WHX/WHG (Würfel) | **30/50** | WHX-ZB: 5,2 W DL / 1,1 W BL | **IP65** | 3-seitig Piktos, Hallen |
| FM Flexway | 22 | — | — | **dynamisch** (10 Modi inkl. „gesperrt"), nur ZB |

### Sicherheitsleuchten / Aufheller (Kernwerte)

| Familie | Notbetriebs-Lichtstrom | Optik/Montage | Besonderheit |
|---|---|---|---|
| **KWI** | **520 lm** (1h/3h) · 210 lm (8h) | Decke/Wand, IP65 | Fluchtweg-Arbeitstier; auch RZ EW 16 |
| **IL** | 170 lm (3h) | 4 Wechsel-Optiken: R=rund/Antipanik · F=Flur **>24 m Abstand** · S=Spot (12–16 m Höhe) · H=Hochdecke >35 m (ZB) | Leuchtenabstands-Tabellen im Datenblatt |
| **K6** | 300 lm | Universal, Radial-/Korridorlinse | Design-Award; LiFePO4 |
| EE | — | Deckeneinbau; R (bis 3 m) / F (>18 m) / S | Downlight-Serie |
| WER / WEF / WAF | 140 / 420 / 420 lm | Wandeinbau Ø67 / Doppeldose / Wandanbau | WER+WEF nur ZB |
| ZA / KMB / DLE | — | Wand IP65 / Decke / Einbau-Downlight | Außen / Standard / ZB-Mischbetrieb |

### Photometrie/Datenblätter

**Eulumdat (.ldt) je Artikel im Shop downloadbar — bei Einzelbatterie getrennt je
Autonomiezeit** (KWI: eigene LDT für 1h/3h vs. 8h → Notbetriebs-Lichtstromreduktion
ist in den LDTs abgebildet). PDFs auf `image.schrackcdn.com`.

---

## Teil B — DIN Notlicht (din-Dietmar Nocker, Linz)

Durchgängig: 50.000 h/5,7 Jahre Vollgarantie · **PLC24** (Leuchten auf 24-V-DC-Kreisen
der SU-Anlage, Daten über dieselbe Leitung) · dimmbar (Notbetrieb automatisch 100 %).

### CONCEPT 2 (Katalog 03/2025) — modulare Serie, IP65 Standard

| Typ | Art | Kennwerte |
|---|---|---|
| RZ1 (plus/duo) | RZ niedrige Haube | **EK 12 m**; *plus* = +SL integriert; *duo* = RZ+SL getrennt schaltbar (**2 Adressen**) |
| RZ2 | RZ hohe Haube | **EK 24 m** |
| SL3/4/5 | Sicherheitsleuchte | 1 lx Mittellinie bis ~16,6–21,6 m Längsabstand (SL5, h 2,5–4,5 m) |
| AP3/4/5 | **Antipanik** (AP = Antipanik, NICHT Aufputz!) | Flächenausleuchtung |
| AS3/4/5 | Antipanik-Sicherheits-Kombi | Fläche + Fluchtweg |
| TS3/4/5 | Tiefstrahler | Montagehöhen 6–10 m |
| WAP AP/SL | wandparallel, neigbar (15°-Schritte) | **~1 W** |
| Piktoscheiben S1/S2/S3 | Zubehör | **EK 12 / 20 / 32 m** — „**EW 20m**" im Barawitzka-Plan = S2-Scheibe! |

Selbstversorger (scAT = Autotest 3h · scCMR = Funk 1–8h): LED-Notbetriebsströme
**350/200/100 mA für 1h/3h/8h** (RZ1: 350/300/120). Effizienz-Benchmark:
**100 m Fluchtweg à 1 lx = 14,97 W** (≈1,5 W je SL).

### BASIC 2 (Stand 11/2025) — E-LED (251×121) + E-SIGN (280×188)

E-LED RZ1/AP kombiniert (EK 22 m, 24 m mit Scheibe) · E-LED RZ2 (22 m) · E-SIGN RZ
(24 m; plus/duo-Varianten) · E-LED SL/TS (5–12 m Höhe)/AP · Ice-Varianten IP65/−30 °C.
Artikelnummern-Logik `9071 xx 010x`: Stelle für Überwachung (3=ILS, 9=PLC24), letzte
Stelle Betriebsdauer (0=scCMR 1–8h/zentralversorgt, 3=scAT 3h).

### Montage-Suffixe (Profi-Plan-Naht — jetzt vollständig aufgelöst)

DA=Deckenaufbau · DE=Deckeneinbau · WA=Wandausleger quer · WA90=90° · **WAP=wandparallel**
· EW xx m = Erkennungsweite/Piktoscheibe · plus/duo = integrierte SL / getrennt schaltbar.

### Versorgungssysteme

- **SU x NET** (Gruppenbatterie/LPS): SU 2 NET = 2×20, **SU 6 NET = 6×20 Adressen**,
  24 V DC 12 Ah (P-Varianten 36 Ah); **SU 6P NET ESF30 (Art. 5188300) = exakt die
  Anlage aus dem Stromkreisnummer-Profi-DWG** („SU 6P NET E30"). ESF30 = zertifizierter
  30-min-Funktionserhalt → spart E30-Verkabelung. **Mischbetrieb DL/BL auf einem
  Kreis, je Leuchte programmierbar**; Modbus/GLT, mySU, autom. Leuchtensuche.
- **SU NG** (Nachfolger): bis 16 Kreise/320 Leuchten, 240–960 W, Kreise bis 400 m.
- **SC NET CMR**: Einzelbatterie funk-überwacht (ohne Kreisverkabelung).

### Datenblätter/Photometrie

Übersichts-PDFs öffentlich (`din-notlicht.com/wp-content/uploads/...`); Artikel-
Datenblätter + Lichtverteilungen im Portal `productdata.din-notlicht.com` (UI öffentlich,
API token-gated — kein anonymer Massen-Scrape, Einzeldownload je Artikel möglich).

---

## Gemeinsame Engine-Erkenntnisse (beide Hersteller)

1. **Notbetriebs-Lumen der Aufheller: ~140–520 lm** (Schrack) bzw. ~1–1,5 W-Klasse
   (din PLC24). Hersteller geben **max. Leuchtenabstände direkt an** (Schrack IL-Flur
   >24 m, EE >18 m; din SL5 ~16–21 m) → bestätigt: unser 5,4-m-Ist-Raster in
   `deckung.py` ist Faktor 3–4 zu konservativ; Verdichtungs-Slice (Mittellinien-
   Nachweis + photometrischer Start-Abstand) ist der richtige Fix.
2. **8h-Betrieb ≈ halber Lichtstrom** (KWI 520→210; KB 300→150; din 350→100 mA):
   Bei LB „8 h" MUSS mit der 8h-Photometrie gerechnet werden — Schrack liefert
   getrennte LDTs je Autonomiezeit (Katalog-Erweiterung möglich).
3. **Cap 20 Leuchten/Kreis von din bestätigt** („je 20 Adressen") — unser
   `circuit_zuordnung`-Cap ist herstellerecht; Achtung: **duo-Leuchten = 2 Adressen**.
4. **DL/BL ist Konfiguration, nicht Produkt** (beide Hersteller; din sogar gemischt
   auf einem Kreis programmierbar) — deckt IsBLString-Befund; unsere getrennten
   DL/BL-Kreise sind eine zulässige (konservative) Konvention.
5. **Erkennungsweiten-Stufen fürs Produkt-Matching:** Schrack 14/15/16/20/22/24/27/
   30/50 m · din 12/20/22/24/32 m. „EW 20m"/„EK"-Angaben stehen im Produktnamen →
   LB-Parser kann Produktvorgaben direkt auf `erkennungsweite_m` mappen.
6. **`stromaufnahme_ma` (Enis-Follow-up #96) befüllbar:** din Einzelbatterie
   350/200/100 mA je Autonomie; Schrack über Watt (KWI-ZB 5,2 W DL/1,1 W BL);
   din-PLC24-Kreise rechnen in Watt-Budget statt mA-Summe.
7. **LB-Vokabular-Kandidaten:** „Cool"/Ice (−25/−30 °C), IP65 (Garage/Feuchtraum),
   scAT/scCMR/ILS/PLC24, ESF30/E30, Flexway/FSU (dynamische Fluchtweglenkung),
   WAP (wandparallel), duo/plus.
8. **Barawitzka-Profi-Plan jetzt vollständig dekodiert:** „CONCEPT 2 AP WA EW 20m" =
   din Antipanikleuchte, Wandausleger, S2-Scheibe 20 m; „BASIC 2 E-SIGN RZ plus DA" =
   RZ 24 m mit integrierter SL, Deckenaufbau; „SU 6P NET E30" = Art. 5188300,
   6×20 Adressen, 36 Ah, Funktionserhalt-Gehäuse.

## Quellen (Auswahl)

Schrack: [Notleuchten Know-how](https://www.schrack-technik.de/know-how-cip/notlicht-usv-co-blindstromkompensation/notleuchten) ·
[RZ-Familien](https://www.schrack.at/know-how-cip/notlicht-usv-co-blindstromkompensation/notbeleuchtung/rettungszeichenleuchten) ·
[Aufheller-Familien](https://www.schrack.at/know-how-cip/notlicht-usv-co-blindstromkompensation/notbeleuchtung/leuchten-zur-aufhellung-der-rettungswege) ·
Produktseiten NLKWID433S/NLK5U403/NLK3U013SC/NLK6U023SC u.a. ·
[K6-Katalog](https://image.schrackcdn.com/produktkataloge/f-k6--de25.pdf)
DIN: [Leuchten-Übersicht](https://din-notlicht.com/de-at/produkte-service/leuchten/) ·
[CONCEPT-2-Katalog](https://din-notlicht.com/wp-content/uploads/Katalog-CONCEPT-2-DE.pdf) ·
[BASIC-2-Übersicht](https://din-notlicht.com/wp-content/uploads/BASIC-2-Leuchtenuebersicht.pdf) ·
[SU-NET-Folder](https://din-notlicht.com/wp-content/uploads/Folder-SU-NET-AT.pdf) ·
[SU-NG](https://din-notlicht.com/wp-content/uploads/SUNG-Folder-DE.pdf) ·
Produktdaten-Portal productdata.din-notlicht.com
