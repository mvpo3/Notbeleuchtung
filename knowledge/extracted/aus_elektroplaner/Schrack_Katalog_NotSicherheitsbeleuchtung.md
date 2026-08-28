# Schrack „Not- und Sicherheitsbeleuchtung" — Produktkatalog (k-sibe-at9)
**Quelle:** elektro-planer knowledge/buecher/k-sibe-at9.pdf (400 S.), via Teil-Digests synthetisiert · **Übernommen:** 2026-08-28
**Einordnung:** Referenz-Praxis + Hersteller-Produktdaten der Marke, die die Engine rendert (Schrack). Nie alleinige norm_quelle.

## Relevanz für die Engine

Die Engine rendert Schrack-Symbole (`CAD_Symbole/E-Symbole.dxf` + `schrack_symbol_mapping.yaml`).
Dieser Katalog liefert die **Produkt-Realität hinter den Blöcken**: welche Leuchtenfamilien
Schrack anbietet, ihre **Erkennungsweiten** (EW, bestimmt max. Piktogramm-Sichtabstand nach
EN 1838), **Leuchtenabstände** (AL, max. Abstand für 1 lx Fluchtweg-Aufhellung), **Montagearten**
(Bestellschlüssel-Buchstabe → Wand/Decke/Einbau/Pendel/Seil), **Autonomiezeiten** (1/3/8 h) und
die **System-Architektur** (Einzelbatterie vs. Gruppen-/Zentralbatterie mit Überwachung).

Für die **Platzierungs-Logik (Leonis)** sind vor allem relevant:
- **EW/Piktogrammgröße** → max. Abstand zwischen zwei Rettungszeichenleuchten entlang eines Fluchtwegs.
- **AL / Abstandstabellen** → max. Abstand zwischen Sicherheits-/Antipanik-Leuchten für 1 lx auf der Mittellinie (abhängig von Montagehöhe, WF 0,80).
- **Montageart** (Wand=RZ, Decke=SI) → Symbolwahl + Orientierung.
- **Autonomiezeit** und **Überwachungspflicht (>20 Leuchten → zentrale Erfassung)** → Systemwahl, i. d. R. LB-getrieben.

Norm-Referenzen sind durchgängig zu bestätigen bei Enis (`normwissen/`); Schrack-Werte sind
Hersteller-Auslegung, **kein** norm_quelle-Ersatz.

## Produkt-Landkarte (Leuchtenfamilien + Einsatzzweck)

### A. Rettungszeichenleuchten — statisch (Piktogramm ISO 7010, Kennzeichnung Fluchtweg)
Steckpiktogramm-Set (Pfeil l/r/o/u + weiße Folie einseitig), Ausleuchtung des grünen Piktogramms.
Auswahlkriterium = **Erkennungsweite (EW)**.

| Familie | EW | Bauart / Besonderheit | IP | SK |
|---|---|---|---|---|
| OM (OLED) | 20 m | OLED, 100 % homogene Fläche, Design | IP20 | II |
| AI / AM / AX (Serie A, Zinkdruckguss) | 15 / 22 / 30 m | Metall-Scheibe, Duo-Technik optional (ERT-LED zusatz) | IP40 | I |
| ASM (Aluprofil) | 22 m | Universalmontage | IP40 | I |
| MM (Zinkdruckguss) | 22 m | Metall, Duo optional | IP40 | I |
| FM (Zinkdruckguss) | 22 m | Wand-Aufbau, robust | IP65 | I |
| KS (Kunststoff-Scheibe) | 22 m | Universal, komb. Kennz.+Ausleuchtung (KSC) | IP54 | II |
| KX (Kunststoff-Scheibe) | 30 m | ERT-LED, große Abstände | IP40 | II |
| K2 | 27 m | EB-Autotest, Universal | IP44 | II |
| KB (modular, DUO) | 14 / 22 / 30 m | 3 Scheibengrößen, DUO Ausleuchtung 4 Richtungen | IP65 (Pendel IP40) | II |
| KM | 24 m | schlank, Universal | IP54 | II |
| KT | 16 m | nur EB 3h | IP54 | II |
| K3 | 27 m | EB-Autotest, Nahbereichs-Aufhellung unten | IP44 | II |
| GX (GXD/GXS/GXW) | 30 m | Scheibe, Decke/Wand/Seil | IP40 | II |
| KD | 22 m | schlank, Universal | IP54 | II |
| LM / LX / LS (Aluprofil) | 22 / 34 / 56 m | Design, sehr große EW (LS werkseitig bedruckt) | IP40 | I |
| V2 (Edelstahl V2A/V4A) | 30 m | vandalensicher, Wand | IP65 | I |
| WG / WX (Würfel) | 46 / 90 m | Rundum-Erkennung, Wegkreuzungen | IP20 | I |
| KC / KW / K5 (Industrie) | 30 / 16 / 20 m | Wand=RZ / Decke=SI, Spiegelreflektor | IP54/IP43/IP65 | II |
| EXIT / EXIT 2 (Ex-Schutz) | 25 m | ATEX Zone 1/21 bzw. 2/22, feste Pfeilrichtung | IP66 | I |

### B. Rettungszeichenleuchten — dynamisch
- **FM Flexway** (EW 20 m, IP65): dynamisches **LCD-Piktogramm** mit **10 Anzeigeoptionen**
  (8 Pfeilrichtungen + „Fluchtweg gesperrt" + „Anzeige aus"). Je eine Einstellung Normal-/Notbetrieb,
  Umschaltung über **potentialfreien Kontakt** (BMA/Rauchmelder). Teil eines Systems nach EN 50171.
  → Für dynamische Fluchtwegsteuerung (Umgehen von Gefahrenquellen).

### C. Sicherheits-/Fluchtweg-Aufhellungsleuchten (ohne Piktogramm, 1 lx Mittellinie)
Auswahlkriterium = **Leuchtenabstand AL** aus Abstandstabellen (Montagehöhe-abhängig).
Linsenoptik bestimmt Lichtverteilung:
- **Rund (R):** Kreuzungen, Deckenhöhe bis ~4 m; auch **Antipanik nach EN 1838**.
- **Flur/Längsrichtung (F):** Fluchtweg gerichtet, AL **>18–24 m**.
- **Spot (S):** hohe Räume bis **16 m**; auch Antipanik in hohen Räumen.
- **Hallenlicht (H):** hohe Räume bis 16 m, AL **>30–35 m**, nur ZB/GB.

Familien: **KMB, KS, KE, KX, KB, KC, KW, K5** (kombiniert Kennz.+Ausleuchtung), **LINDA** (Industrie/Feuchtraum, IP65, IK10),
**FM** (ERT-LED Decke, IP65), **EE** (dezenter Deckeneinbau, ERT-LED 1 W), **IL/EA** (ERT-LED 3 W, 4 Linsen, Antipanik-tauglich),
**DE/DL/DO** (kompakte Deckeneinbau), **WER/WEF/WAF** (Wandeinbau/-anbau parallel zur Wand), **ZA** (Ausgangsbereich, IP65 außen, LiFePO4),
**QG/QAW** (Fläche), **FL** (Außen-Strahler 10/30 W), **HX** (Handscheinwerfer), **SKS/SGS** (Notlichtstrahler 10/30/50 W).

### D. Universal-/Industrieleuchten
Übergreifend die K-Serien (KS/KX/KM/K2/KB/KT/K3/GX) sowie KC/KW/K5 — je nach Piktogramm-Bestückung
RZ oder als reine Sicherheitsleuchte betreibbar (Wand vs. Decke).

## Platzierungs-/Auslegungs-relevante Kennwerte

| Thema | Wert/Regel | Bezug |
|---|---|---|
| Erkennungsweite EW | Katalog-Kennwert je Familie (14–90 m), = max. Piktogramm-Sichtabstand | EN 1838 |
| Leuchtenabstand AL (Aufhellung) | Abstandstabellen: 1 lx Mittellinie, **Wartungsfaktor 0,80**, je Montagehöhe | EN 1838 |
| Antipanik / hohe Räume | Rund- (R) und Spot-Linse (S) explizit als Antipanik-tauglich ausgewiesen | EN 1838 |
| Sicherheitseinrichtungen (z. B. Feuerlöscher) | Abstandstabellen für **5 lx** (statt 1 lx) vorhanden (KMB, KS) | EN 1838 |
| Montageart-Codes | W Wandanbau · R Wandeinbau · D Deckenanbau/Ausleger · C Deckeneinbau · E Einbau · U Universal | Bestellschlüssel |
| Linsen-Codes | F Flur · R Rund · H hohe Decken · S Spot | Bestellschlüssel |
| Wand vs. Decke | Wandmontage → Rettungszeichen (RZ); Deckenmontage → Sicherheitsleuchte (SI) | Katalog-Konvention |
| Autonomiezeit | LED-Autotest-EB **1/3/8 h einstellbar**, Auslieferzustand **3 h** | — |
| 8 h Pflicht | Beherbergungsbetriebe + Hochhäuser: 8 h | ÖVE/ÖNORM E 8002-1:2007 |
| Autotest-Zyklus | Funktionstest alle **7 Tage**, Betriebsdauertest alle **52 Wochen** | EN 62034 |
| Max. Leuchten je Stromkreis (ZB/GB) | **bis 20 Leuchten** je Abgangskreis (DCM-Modul) | Schrack-Anlagen |
| Zentrale-Überwachungspflicht EB | **>20 EB-Leuchten → zentrale Erfassung** (OVE E 8101:2019); ab 50 nach älterer E 8002-1:2007/TRVB E102 | OVE E 8101 |
| Autotest ohne Zentrale | bis **20 Leuchten** (SelfControl) zulässig | OVE E 8101:2019 |
| Erkennungsweite-Terminologie | EW = Piktogramm-Sichtweite; AL = Fluchtweg-Aufhellungsabstand (1 lx @ MH 3 m, WF 0,8) | EN 1838 |
| Piktogramme | ISO 7010, Pfeil l/r/o/u + weiße Folie; steckbar vor Ort | ISO 7010 |
| IP-Zuordnung | Innen-Design meist IP20/IP40; Feucht/Industrie IP54; Außen/Ausgang/robust IP65; Ex IP66 | EN 60529 |
| Cool-Ausführung | bis **−30 °C** (Kühlhaus/Außen); Akku+Elektronik in separater IP54-Box, 2-pol. Kabel 1–2,5 mm² | — |
| Netzbetrieb-Dimmung | ERT-LED-ZB/GB (…039EL) ab Werk 50 % gedimmt, im Batteriebetrieb/bei Phasenüberwachung 100 % | Energieeffizienz |
| Leuchtmittel-Stromaufnahme (216 V DC) | LED 1 W→2 W · 2 W→3 W · 3 W→4,5 W · 4 W→5,5 W · 5 W→6,5 W | Systemauslegung |

**Beispiel Erkennungsweiten-Tabelle (statisch, Piktogramm) — die Serien-A-Systematik:**
EW skaliert mit Piktogramm/Scheibengröße: AI **15 m** (HP-LED 2 W) · AM **22 m** (2 W) · AX **30 m** (3 W);
KB modular in **14 / 22 / 30 m** über austauschbare Scheiben (gleiches Gehäuse).

**Beispiel Abstandstabelle (Aufhellung IL/EA rund, ERT-LED 3 W, WF 0,80, ZB/GB):** Montagehöhe 2,0 m →
seitliche/längs-Abstände bis ~11,3 m; 3,0 m → ~14,9 m; 4,0 m → ~14,6 m. (Die Engine sollte solche
Tabellen NICHT hart einbrennen — sie sind Hersteller-Auslegungshilfen; Norm-Grenzwert bleibt 1 lx/EN 1838.)

## System-Architektur (Einzel- vs. Gruppen-/Zentralbatterie)

### Einzelbatterie (EB) + Überwachung
- **SelfControl (SC)** Autotest je Leuchte; bis **20 Leuchten** ohne Zentrale (OVE E 8101:2019).
- **WirelessControl Professional (WL):** Funk **868 MHz**, garantierte Reichweite **30 m** horizontal
  im Gebäude, stockwerksübergreifend; **250 Geräte** je Zentrale (auf 1000 erweiterbar, mehrere Zentralen
  vernetzbar); keine Busverkabelung, nur 230 V AC → ideal für Bestand/Denkmalschutz. Zentrale =
  Touch-Netbook (NLWLTOUCH5) + USB-Koordinator; IO-Box für BMA-Kontakt.
- Vorteil EB gegenüber ZB: **kein nachträgliches E30** in Brandabschnitte nötig.

### Gruppenbatterie (LPS, „Low Power System", ≤ 1.500 W)
Pro Brandabschnitt eine Anlage → **macht E30-Verkabelung überflüssig** (dezentral). Vernetzbar per TCP/IP.

| System | max. Kreise | Leistung/Autonomie | max. Leuchten |
|---|---|---|---|
| MyControl (MY) | 4 (+1) | 500 W/1h · 210 W/3h · 90 W/8h | 80 (20/Kreis) |
| MicroControl (MI) | 6 (+1) | 500 W/1h · 200 W/3h · 80 W/8h | 120 |
| MiniControl (MN) | 12 (+1) | 1.500 W/1h · 500 W/3h · 300 W/8h | 240 |
| MiniControl XL | 32 | 1.500 W/1h · 500 W/3h · 300 W/8h | 640 |

### Zentralbatterie (CPS, „Central Power System")
Alle Leuchten von zentralem Punkt, **E30-Leitungen** zu den Leuchten.

| System | max. Kreise | Leistung/Autonomie | max. Leuchten |
|---|---|---|---|
| MidiControl (MD) | 32 | 6.324 W/1h · 2.598 W/3h · 1.194 W/8h | 640 |
| MaxiControl (MCX) | 60 | ~17–20,5 kW/1h (Batt. bis 150 Ah) | 1.200 |
| MultiControl (MC) | 96 | bis 40.000 W | 1.920 |
| MDC (ohne Leistungsbegrenzung) | 72 (à 10 A) | bis 40.000 W, keine Einzelleuchtenüberwachung | — |

- **Pro 19"-Schrank:** bis **96 Kreise / 1.920 Leuchten**. Bis **32 Systeme** vernetzbar → max. **61.440 Leuchten**.
- **Stromkreismodule (DCM):** je 2 Abgangskreise, je ≤ 20 Leuchten. DCM12E (1 A/300 VA, ELS = zentrale
  Einzelleuchtenschaltbarkeit für „…EL/…E"-Leuchten) · DCM32 (3 A/650 VA) · DCM42 (4 A/860 VA) · DCM62 (6 A/1300 VA).
  Mischen ELS-fähiger und herkömmlicher Leuchten in einem Kreis **nicht zulässig**.
- **Stromfehler-Auslösung** bei 5–50 % Abweichung vom Referenzwert (einstellbar).
- **Batterien:** RPower OGiV (AGM, 10–12 J Lebensdauer) und OPzV (Panzerplatte, 20 J); Auslegung
  je Leistung/Zeit, +25 % Alterungsreserve; Lüftung/Sicherheitsabstand nach EN 50272-2.

### Normbezüge (System-Ebene, zu bestätigen bei Enis)
EN 50171 (zentrale Stromversorgung) · EN 50172 (Sicherheitsbeleuchtung) · EN 62034 (autom. Prüfeinrichtung Typ ER) ·
EN 50272-2 (Batterieladung/Lüftung) · EN 60598-1 / -2-22 (Leuchten) · EN 1838 (lichttechnisch) ·
OVE E 8101:2019 · ÖVE/ÖNORM E 8002-1:2007 · TRVB E 102 · OVE R 12-2 · DIN 4102-12 (E30-Funktionserhalt) ·
ATEX 2014/34/EU (EXIT).

## Verknüpfung mit unserem Symbol-Mapping

Das aktuelle `schrack_symbol_mapping.yaml` ist bewusst minimal (nur `category: notlicht`, Richtungspfeil-Blöcke):
`notlicht_ks_stiege` / `_unten` / `_links` / `_rechts` (Rettungszeichen-Pfeile) und `notlicht_kw_garage`.
Die Keys tragen bereits die Schrack-Kürzel **KS** und **KW** im Namen — beide sind reale Katalog-Familien:

- **`notlicht_ks_stiege*`** → Katalog-Familie **KS** (Kunststoff-Scheibe, Universalmontage, **EW 22 m**,
  komb. Kennzeichnung+Ausleuchtung als KSC). Passt gut als generische Rettungszeichenleuchte für
  Stiegen/Gänge (Wandmontage → RZ). Die Pfeilrichtung (unten/links/rechts) wählt der Platzierer je
  Ausgangs-/Fluchtweg-Geometrie via Rotation/mirror_x — deckt sich mit Steckpiktogramm-Systematik (Pfeil l/r/o/u).
- **`notlicht_kw_garage`** → Katalog-Familie **KW** (Industrie-Kunststoffleuchte, **EW 16 m**, schmale
  Bauform Wand/Decke, IP54). Plausibel für Garage/Nebenräume.

**Hinweise für künftige Mapping-Erweiterung** (wenn `category` über `notlicht` hinaus wächst):
- Neue Kategorie **`sicherheitsleuchte`** (Aufhellung, kein Piktogramm) für Familien **IL/EA, EE, KMB, KE, DE/DL/DO** —
  Auswahl über AL/Montagehöhe statt EW.
- Neue Kategorie **`antipanik`** — dieselben Rund-(R)/Spot-(S)-Linsenvarianten (IL R/S explizit EN-1838-Antipanik-tauglich).
- **`rettungszeichen`** mit EW-Staffelung: kleine EW (AI 15 / KW 16 / KT 16), Standard (AM/KS/MM/KD 22 / KM 24 / K2/K3 27),
  groß (AX/KX/GX/V2 30 / LX 34 / WG 46 / LS 56 / WX 90). EW als Attribut → treibt max. Leuchtenabstand entlang Fluchtweg.
- **`dynamisch`** für FM Flexway (LCD, potentialfreier Kontakt).
- **`ex`** für EXIT (feste Pfeilrichtung, keine Steckpiktogramme → eigene Blöcke je Richtung nötig).
- Ob jede Familie einen eigenen DXF-Block in `E-Symbole.dxf` hat, ist NICHT aus dem Katalog ableitbar —
  vor Erweiterung muss die tatsächliche Block-Liste der Library geprüft werden (Naht-Invariante:
  `catalog_key ∈ schrack_symbol_mapping.yaml`, `block_name ∈ E-Symbole.dxf`).

## Offene Punkte / Extraktionslücken

- **Block-Namen ↔ Katalog-Familien nicht 1:1 belegt:** Der Katalog nennt keine DXF-Block-Namen; die
  Zuordnung KS/KW → Library-Blöcke muss gegen `E-Symbole.dxf` verifiziert werden.
- **Piktogrammgrößen in mm** nicht durchgängig extrahiert — der Katalog gibt Erkennungsweite (m) statt
  Piktogramm-Höhe (mm) an. Umrechnung EW → Höhe über l = z×h (z=100 bzw. 200) liegt bei Enis/Norm, nicht im Katalog.
- **Abstandstabellen** liegen als lange Zahlenreihen je Montagehöhe vor (in den Teil-Digests erhalten, hier
  nur exemplarisch). Bei Bedarf für konkrete Auslegung Volltext `buecher/k-sibe-at9.txt` je Familie lesen.
- **Reine Bestellnummern-Listen** (mehrere hundert NL…-Artikel) bewusst nicht übernommen — nur Systematik.
- Genauer **EW-vs-EN-1838-Grenzwert-Abgleich** (Schrack-EW vs. Norm-Erkennungsweite) ist bei Enis zu klären;
  Schrack-Werte sind Hersteller-Angabe.
