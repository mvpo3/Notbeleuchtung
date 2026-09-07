# Referenz-Platzierung — Muster aus Fachplaner-Plan, Beispielbildern und Wissensquellen

**Zweck:** Die beobachteten Platzierungs-MUSTER der Referenz-Praxis, als Vorbild für
die Platzierungs-Strategien (Leonis) und den Referenzvergleich
(`scripts/plan_pruefen.py`, `07_referenzvergleich.png`). KEINE Normwerte — wo eine
Zahl steht, ist sie eine **Messung am Referenzmaterial**, keine Norm-Anforderung.
Normzitate nur mit Fundstelle (siehe Quellenliste unten).

Erhoben 2026-09-07 (selbst gemessen an der Referenz-DXF bzw. an den Bildern; Skript-
Messungen mit ezdxf, temporär, gelöscht).

---

## 1. Fachplaner-Referenzplan Barawitzkagasse

**Quelle:** `DIN-Notbeleuchtungspläne(Beispiele)/din_support_ReMi_Barawitzkagasse_28.04.2026.dxf`
(R2018, mm, DIN-Notlicht-Planungstool „din support"). 46 Leuchten + 1 Controller auf
Layer `din_SIBEL_10_emergency_lighting` (RZ, 33×), `…_yellow` (SL, 13×),
`…_system` (Controller, 1×); Legenden-Duplikate auf `din_SIBEL_70_legend_*`
nicht mitzählen. Unterlage = gescannte JPG (Xref fehlt im Repo), mehrere
Geschoss-Frames nebeneinander im Modelspace.

### Frame → unser PP_2-Plan (m)

`our = ref/1000 + Offset` (Frame-Kalibrierung gegen unsere Barawitzka-EG-Erkennung):

| Geschoss | Offset (m) | Restfehler |
|---|---|---|
| UG | (-77.85, -37.66) | Ø 0.33 m |
| EG | (-48.44, -39.04) | Ø 0.19 m |
| OG1 | (-18.34, -38.66) | Ø 0.04 m |

EG-Bestückung (11 Leuchten): 5× RZ Typ A, 3× RZ Typ B, 1× RZ Typ F, 1× SL Typ H,
1× SL Typ I.

### Symbolik des Fachplaners

Blöcke `STANDARDMASK_RZ_PL` / `_PR` / `_PU` / `_PLPR` (Rettungszeichen: Pfeil links /
rechts / unten / links+rechts beidseitig), `STANDARDMASK_SL` (Sicherheitsleuchte),
`STANDARDMASK_SYSTEM` (SV-Anlage/Controller). Typen A–I in Attribut `TYPENUMBER`
(Schrack/din-Produkte BASICsc / CONCEPTsc, CMR 1–8 h in `TYPENAME`).
**Rotation strikt im 90°-Raster** und immer = Wand-/Gangwinkel — kein freier Winkel
im ganzen Plan (33 RZ gemessen: nur 0/90/180/270).

### Beobachtete Muster (mit Beispielkoordinaten in unserem m-System)

1. **RZ_PU mittig über der Ausgangstür**, 0.25–1.0 m vor der Türsehne (Innenseite).
   Beispiel EG: RZ_PU Typ A ref (62766, 35912) → our **(14.33, -3.13)**.
2. **SL zusätzlich AUSSEN über jedem Endausgang**; Typ I sitzt 0.35 m vor dem
   RZ des Ausgangs. Beispiel EG: SL Typ I ref (62773, 36264) → our
   **(14.33, -2.78)** — 0.35 m über dem RZ_PU aus Muster 1.
3. **Stiegenhaus-Regelgeschoss-Kit** — identisch je Geschoss wiederholt:
   RZ_PL an der Stiegenhaus-Tür + SL 2.2 m daneben am Podest + RZ_PLPR diagonal im
   Gang. Beispiel OG1 (Stiege 1): RZ_PL ref (56589, 128956) → our (8.15, -9.70),
   SL Typ H ref (58805, 128966) → our (10.37, -9.69) [2.2 m daneben],
   RZ_PLPR ref (61564, 130914) → our (13.12, -7.75). Wiederholung OG2 wortgleich:
   RZ_PL (56272, 157590), SL (58442, 157603), RZ_PLPR (61133, 159517).
4. **Richtungs-RZ an der Wand entlang der Gangachse** (Wandabstand ≤ 0.3 m),
   an Richtungswechseln **paarweise gegenläufig** (PL gegen PR). Beispiel EG:
   RZ_PR rot=0 ref (56580, 32797) ↔ RZ_PR rot=180 ref (56894, 30254).
5. **RZ_PLPR (beidseitig) an Gangknoten und Gang-Enden**, quer zur Gangachse
   gedreht. Beispiel UG: RZ_PLPR rot=270 ref (80989, 11556) und (83929, 18141).
6. **SL-Kette im innenliegenden Kellergang** alle ~4–5 m (Typ G). Beispiel UG:
   SL (83871, 23151) → SL (83871, 27255) = 4.1 m Abstand auf derselben Achse.
7. **Controller/SV-Anlage im UG-Technikraum**, 1× je Objekt:
   STANDARDMASK_SYSTEM „Anlage A" ref (90443, 29407).
8. **Außen-Fluchtweg als Sichtverbindungskette** mit Typen der
   20-m-Erkennungsweite-Klasse (Fachplaner-Typenwahl, nicht Normwert).

---

## 2. Muster aus den 6 Beispielbildern

Alle in `DIN-Notbeleuchtungspläne(Beispiele)/`, selbst gesichtet 2026-09-07.

### `OVE-Richtlinie-R-12-2_Bild-8.9.jpg` (OVE R 12-2:2019 Bild 8.9, Beispiel 3)

- Schema-Schnitt: **je Geschoss eine Kette von SL** entlang des Ganges, RZ (grüner
  Pfeil) am Gang-Ende **Richtung Treppenhaus**.
- **Treppenhaus als eigener Strang**: SL je Podest/Halbgeschoss, Pfeile abwärts.
- **CPS-Anlage im Keller** in „abgeschlossener elektrischer Betriebsstätte",
  Steigschacht-Verkabelung je Geschoss als eigener Brandabschnitt (Anmerkung im
  Bild: E30-Dosen, TRVB 110 B).

### `LST_Notlicht.jpg` (licht.de, Gebäudeschnitt-3D)

- **RZ über jeder Tür in Fluchtrichtung** (auch Zwischentüren im Gang), SL an der
  Decke der Raummitte — Funk-Überwachungssymbolik an jeder Leuchte.
- **Treppenhaus: RZ an der Tür jedes Geschosses** + SL über den Läufen.
- **Zentrale (Batterie + Controller) im EG/UG-Technikbereich**, beide Wandgeräte
  nebeneinander.

### `uds-fluchtweglenkung-simulation.jpg` (dynamische Fluchtweglenkung, 3D-Sim)

- **Adaptive RZ**: gesperrte Richtung = rotes X-Zeichen, freigegebene Richtung =
  grüner Pfeil — RZ an jedem **Gangknoten paarweise** (je Laufrichtung eines).
- **Bodennahe SL-Punkte in Kette** entlang der Gang-Mittellinie (regelmäßiger
  Abstand), sichtbar als Punktreihe im geführten (grün markierten) Weg.
- RZ „Pfeil unten" **direkt am Ausgangs-/Türsturz**, Pfeil in Durchgangsrichtung.

### `mobile_krankenhaus_erhoeht.jpg` (licht.wissen-Stil, Krankenhaus „erhöhte" Sibe)

- **Lux-Beschriftung je SL** (0,5 lx Allgemein, 1 lx Gang, 5 lx Sonderstellen,
  15 lx Behandlungsplatz) — die Sonderstellen (Treppe, Erste-Hilfe-Kasten =
  grünes Kreuz-Symbol, Feuerlöscher = rotes Symbol) bekommen **eigene SL davor**.
- **RZ an jeder Gang-Verzweigung und über jeder Fluchttür**, WC-Trakt mit eigenem
  RZ „Pfeil unten" je Kabinenzeile.
- **Außenbereich vor dem Endausgang** bekommt eine eigene Leuchte (0,5 lx-Feld
  außerhalb der Fassade).

### `mobile_schule_erhoeht_2021.jpg` (licht.wissen-Stil, Schule)

- **Gang als Rückgrat**: 1-lx-SL-Kette in regelmäßigem Raster über die volle
  Ganglänge, Klassenräume je 2–4 SL (0,5 lx) an den Raum-Diagonalen.
- **Beide Stiegenhäuser symmetrisch bestückt**: RZ+SL am Antritt, 1-lx-Leuchte
  auf den Läufen, 5-lx-Punkt an der untersten Stufe (Typ-Beschriftung „5 lx").
- **Erste-Hilfe-/Brandschutz-Sonderstellen** (grünes Kreuz im Chemiesaal-Vorraum,
  rote Melder an den Stiegen) mit eigener davor gesetzter Leuchte.

### `csm_16_lw10_47_INO_Visualisierung_94461653fe.jpg` (INOTEC/licht.de, Monitoring-Grundriss)

- **Sparsame RZ-Setzung im Flur-Rückgrat**: nur an Knoten und Richtungswechseln
  (4 RZ + 3 Antipanik-Punkte für einen ganzen Riegel) — Überwachungs-Software
  zeigt Status je Leuchte (rot = gestörte Leuchte).
- **RZ paarweise gegenläufig am selben Flurpunkt** (links/rechts-Kombination am
  mittleren Knoten), Pfeilrichtung folgt der jeweils kürzeren Richtung zum Ausgang.
- **Treppenhaus-Kern: RZ „Pfeil unten + Lauffigur" direkt am Treppenantritt**.

---

## 3. Quellenliste (`knowledge/`)

Kurzaussage = wofür die Quelle bei Platzierungsfragen taugt; Fundstelle = Datei
(+ Abschnitt). **Keine Normwerte aus dieser Tabelle ableiten** — Werte immer in der
Quelle selbst nachschlagen und mit Fundstelle zitieren.

| Pfad | Kurzaussage | Fundstelle |
|---|---|---|
| `knowledge/extracted/EN_1838_notbeleuchtung.md` | Basis-Norm: Lux-Werte, Erkennungsweite l=z·h, Pflicht-Betonungspunkte des Fluchtwegs | §4.1 (Fluchtweg), §4.1.2 (Betonungspunkte a–j), §5 (RZ) |
| `knowledge/extracted/Fachinfo_E08_Arbeitsstaetten.md` | Wann Sicherheitsbeleuchtung in AT-Arbeitsstätten Pflicht ist (subsidiär zu E 8101/R 12-2/OIB 2) | Kopf „Einordnung" (S. 1) |
| `knowledge/extracted/OVE_E_8101_niederspannungsanlagen.md` | Elektrische Ausführung Sicherheitszwecke (Speisung, Stromkreise) | Abschnitte 560 + 7-718 |
| `knowledge/OVE-Richtlinie R 12-2 AC 2019-07-01.pdf` | Anlagen-Ausführung Sicherheitsbeleuchtung AT; Ausführungs-Beispiele mit baulichen Maßnahmen | Bild 8.9 (Beispiel 3, siehe Abschnitt 2) |
| `knowledge/sonstiges Wissen Notbeleuchtung/vorschriftenkurzuebersicht-at.pdf` | AT-Vorschriften-Überblick (welche Regel wofür) auf einer Seite | Gesamtdokument |
| `knowledge/sonstiges Wissen Notbeleuchtung/vorschriftenkurzuebersicht_de.pdf` | DE-Pendant — nur zum Abgleich, nicht AT-bindend | Gesamtdokument |
| `knowledge/extracted/PLATZIERUNGS_KONZEPTE.md` | Das Planer-Denkmodell hinter den Strategien (Schicht-1-Anker, Tür-Regel) | „Schicht-1-Anker" |
| `knowledge/extracted/PROFI_DIN_PLAN_UND_VORSCHRIFTEN.md` | Erst-Digest des Barawitzka-Referenzplans + Vorschriften-Scans | §1 (Plan-Analyse) |
| `knowledge/extracted/PRODUKTE_SCHRACK_DIN.md` | Produktfamilien (BASICsc/CONCEPTsc, CMR) hinter den Typen A–I | BASIC-2/CONCEPT-2-Abschnitte |
| `knowledge/extracted/Handbuch_NotSicherheitsbeleuchtung_2026.md` | INOTEC-Planungs-Blaupause inkl. dynamischer Fluchtweglenkung | Kopf „Einordnung" |
| `knowledge/extracted/GSYSTEMS_Planungshandbuch.md` | Hersteller-Planungshandbuch (Referenz-Praxis) | Kopf „Einordnung" |
| `knowledge/extracted/Kaufel_Planungshandbuch.md` | DE-Planungshandbuch — nur EN-identische Teile für AT nutzen | Kopf „Einordnung" (DE-only-Hinweis) |
| `knowledge/extracted/LichtWissen_10_Notbeleuchtung.md` | DE-Branchenpublikation, Bildvorlagen (mobile_*-Bilder oben) | Kopf „Einordnung" |
| `knowledge/extracted/ONL_Normen_AT.md` | Zumtobel-Zusammenfassung der AT-Norm-Lage (Sekundärquelle) | Kopf „Einordnung" |
| `knowledge/extracted/ANALYSE_Baufeld_E2_Notbeleuchtung.md` | Referenz-Praxis eines realen Planers vs. EN 1838 (Baufeld E2) | Kopf „Ziel" |
| `knowledge/extracted/FLUCHTWEG_AUSHANG_REFERENZ.md` | Zimmeraushang-Referenz (Darstellungs-Konventionen) | Gesamtdigest |
| `knowledge/extracted/MUTHGASSE_POLIERPLAN_BRANDSCHUTZ.md` | Muthgasse-Polierpläne: Brandschutz-Gerüst, 6. CAD-Familie | Gesamtdigest |
| `knowledge/extracted/LB_ANALYSE_beispiele.md` | Was reale LBs vorschreiben (Input 2, übersteuert Norm-Defaults) | Gesamtdigest |
| `knowledge/extracted/STROMKREISNUMMER_DWG.md` | Stromkreis-Nummernschema des din-Planungstools | Gesamtdigest |
| `knowledge/extracted/ESV_2012.md`, `ETG_1992.md`, `ETV_2002_2010_2020.md`, `Nullungsverordnung.md`, `RIS_Standesregeln_Elektrotechnik.md`, `Sicherheitsvorschriften_Elektro.md`, `OENORM_E_8014.md`, `OVE_E_8015.md`, `OVE_E_8350.md`, `OVE_E_8351.md` | Rechts-/Elektro-Rahmen (kein Platzierungs-Wissen) | jeweils Kopf „Relevanz für die Engine" |
| `knowledge/extracted/WETTBEWERB_ENDRA_AI.md` | Wettbewerber-Einordnung (kein Platzierungs-Wissen) | Kopf |

---

## 4. Symbolkonvention unserer Library (selbst verifiziert)

Quelle: `CAD_Symbole/Notbeleuchtungssymbole.dxf` + `src/notbeleuchtung/symbols/`
(Mapping `schrack_symbol_mapping.yaml`, Insert-Pfad `inserter.py`/`library.py`).
Verifiziert 2026-09-07 per ezdxf-Geometrie-Dump **und** Render der drei
Pfeil-Blöcke (temporäres Skript, gelöscht).

Wichtig: `library.import_block()` **zentriert** jeden Block beim Import auf sein
Extents-Zentrum (die Roh-Blöcke tragen Basispunkt (0,0,0), aber Geometrie bei
~(2603, 2306)) — **effektiver Basispunkt = Symbol-Mitte**. Rotation ist DXF-CCW
um diesen Punkt.

| catalog_key | Block | Basispunkt (effektiv) | Pfeilrichtung bei rot=0 | Nullrichtung (Azimut) |
|---|---|---|---|---|
| `notlicht_ks_stiege`, `notlicht_ks_stiege_unten`, `notlicht_kw_garage` | `notbeleuchtung- richtungspfeil nach unten` | Symbol-Mitte | **−Y (unten)** | 270° |
| `notlicht_ks_stiege_links` | `notbeleuchtung-richtungspfeil nach links` | Symbol-Mitte | **−X (links)** | 180° |
| `notlicht_ks_stiege_rechts` | `notbeleuchtung-richtungspfeil nach rechts` | Symbol-Mitte | **+X (rechts)** | 0° |
| `sicherheitsleuchte_aufheller` | `aufheller notbeleuchtung` | Symbol-Mitte | richtungslos (Kreis) | — (`rotation_deg` = Optik-Azimut, ADR-0006) |
| `sicherheitsleuchte_spot` | `spot notbeleuchtung` | Symbol-Mitte | richtungslos | — (ADR-0006) |
| `antipanik_leuchte` | `notbeleuchtung- antipanikleuchte` | Symbol-Mitte | richtungslos | — |
| `gruppenbatterie_anlage` | `gruppenbatterie` | Symbol-Mitte | richtungslos | — |

**Folgerung (Rotations-Konvention, bindend für Pfeil-Blöcke):** Soll der Pfeil des
`unten`-Blocks in Azimut A zeigen, ist `rotation_deg = (A + 90) % 360`:
oben→180, rechts→90, links→270, unten→0. Genau so rechnen die Tür-Formel
(`atan2 + 90°`) und die `_ROT`-Tabelle der Sichtlinien-Strategie; `richtung_und_
rotation` in `platzierung/bausteine.py` ist seit dem Rotationsfix
(tests/platzierung/test_rotation_konvention.py) darauf geeicht. Die dedizierten
links/rechts-Blöcke zeigen bei rot=0 bereits in ihre Richtung (`is_directional`,
rotation=0). `richtung="gerade"` rendert der Inserter als Doppelpfeil
(links+rechts, gemeinsame Achsen-Rotation).
