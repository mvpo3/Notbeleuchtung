# Lichtberechnungs-Referenz — echte Profi-Notberechnungen (extrahiert 2026-09-08)

**Erste echte professionelle Lichtberechnungen mit Zahlenwerten im Repo.** Zwei
unabhängige Fachbüros, zwei Programme (Relux + DIALux), beide als
**EN-1838-Notbeleuchtungsszene**. Damit lässt sich `platzierung/lux.py` +
`deckung.py` erstmals gegen echte Nachweise **kalibrieren** statt nur gegen selbst
hergeleitete Defaults.

Quellen (im Repo):
- **`Lichtberechnung/Lichtberechnung.pdf`** (60 S., Relux) — *WHA Aichholzgasse 35*,
  Datum 10.09.2025, **Schrack-Technik**-Leuchten. Gänge aller Geschosse + Garage.
- **`Lichtberechnung/Barawitzka/Lichtberechnung/LiBer_Bawarawitzkagasse 24_{Garage,
  Stiege A,Stiege B}.pdf`** (DIALux, „xuLAID"=DIALux) — *Barawitzkagasse 24*,
  17.–20.04.2026, Bearb. Michaela Reip, **din-Sicherheitstechnik**-Leuchten.
- **`DIN-Notbeleuchtungspläne(Beispiele)/Linke Wienzeile/20250408 - DIN {Plan,Bericht,
  Imagebilder} - geprüft.pdf`** (DIALux, **GEPRÜFT**) — *WHA Linke Wienzeile, 1100 Wien*,
  02.04.2025, Planer **AnlagenPlan** GmbH, din-Produkte. Komplett-Paket: Plan (Symbolik) +
  Bericht (Photometrie) + Imagebilder (Datenblatt je Typ-Buchstabe). **3. Report — bestätigt
  alle Parameter** (MF 0,80 · ohne Reflexion · 0,02 m/0,5 m · Mittellinie ≥1 lx + Mittelfläche
  ≥0,5 lx · Ud ≥0,025). Produkte: `BASIC 2 SIGN-plus` (RZ 80/242 lm), `STRING 2 eco spot SL`
  (127 lm), `CONCEPT 2 AP3 Wandausleger EW 32 m` (Typ B, 1,3 W). Emin durchweg **>1,0 lx**
  (Planer-Sicherheitsmarge), Treppen-Nachweis auf Podest-Höhen 0,18/2,2/2,4 m.

Extraktion: `pypdfium2` (Render) + `pdfplumber` (Text) über den Repo-venv —
`pdftoppm`/Read-Visual fehlt auf der Maschine. Werte gegen die PDF-Seiten geprüft
(Seiten unten zitiert).

> **⚠️ Ordnername-Falle:** `DIN-Notbeleuchtungspläne(Beispiele)/Aichholzgasse/` +
> `Projekte/Aichholzgasse/` enthalten **Architektur-Polierpläne** (HOT ARCHITEKTUR
> ZT, „POLIERPLAN / GRUNDRISS EG"; Legende rein baulich — Bestand/Ziegel/Stahlbeton/
> Durchbrüche/Türtaster, **null Rettungszeichen-Symbolik**), NICHT fertige
> Notbeleuchtungspläne. Das sind leere **Architektur-Inputs** (Selman-Domäne, Wien
> Wohnbau GK5, Geschosse 2UG..2DG). Die zugehörige Notbeleuchtung steckt in der
> Relux-`Lichtberechnung.pdf`.

---

## 1. Berechnungs-Parameter (beide Büros übereinstimmend)

| Parameter | Relux (Schrack) | DIALux (din) | Engine-Bezug |
|---|---|---|---|
| Szene | Notbeleuchtung EN 1838 | Notbeleuchtung EN 1838 | — |
| **Reflexion** | **0** (Boden/Decke/Wände r=0) | **„ohne Reflexion"** | ✅ deckt sich mit Engine (kein Reflexionsterm) |
| **Wartungsfaktor (MF)** | **0,80** | **0,80 innen / 0,57 außen** | ❌ Engine wendet KEINEN MF an → überschätzt ~25 % |
| Nutzebene-Höhe | **0,020 m** | 0,020 m (Randzone 0,000) | Punktmethode misst am Boden ≈ ident |
| Randzone | **0,500 m** (Rand raus) | 0,500 m | ✅ `lux_raster(rand_mm=500)` |
| Berechnungsraster | 128×128 / 128×8 (schmale Gänge) | — | Engine 250 mm Raster (`_NACHWEIS_RASTER_MM`) |
| Montagehöhe Gang | 2,500 m (Decke) | — | `anf.montagehoehe_mm` |
| Möblierung | berücksichtigt (Verschattung) | „platzierte Möbel" | ❌ Engine ignoriert (Backlog) |

**Reflexions-Nuance:** DIALux *listet* zwar Raumreflexionsgrade (Stiege A: Decke
70 % / Wände 48,7 % / Boden 20 %), die **Notbeleuchtungsszene rechnet sie aber nicht
ein** („erfolgte ohne Reflexion") — Worst-Case, direkte Komponente only. Genau die
Annahme der Engine. **→ Validierung, kein Fix.**

**MF-Beleg doppelt bestätigt:** INOTEC-Handbuch-Digest nennt schon „Wartungsfaktor
0,8 → 1,25 lx projektieren" (Referenz-Praxis); beide realen Reports setzen ihn
tatsächlich → belastbarer Engine-Kandidat (s. `platzierung/lux.py`-Slice).

## 2. Nachweis-Metriken

- **Rettungsweg (DIALux, Garage Barawitzka):** getrennter Nachweis für
  **Mittellinie ≥ 1,00 lx** UND **Mittelfläche ≥ 0,50 lx** (halbes Band). Ud-Spalte =
  Emin/Emax, Soll „≤ 40.000" (= Emax:Emin ≤ 40 → Ud ≥ 0,025). Höhe 0,000 m.
  → deckt sich exakt mit `deckung._nachweis_punkte` (Mittellinie 1 lx + Band 0,5 lx).
- **Fläche/Gang (Relux):** Ē, Emin, Emax, **g1 = Emin/Ē**, **g2 = Emin/Emax**.
  Bindend bleibt Emax/Emin ≤ 40 (g2 ≥ 0,025) — in allen Räumen locker erfüllt.
- **Treppe (DIALux, Stiege A):** horizontale Beleuchtungsstärke je Podest-Ebene
  (Ē/Emin, Emax/Emin), Leuchten je Geschosshöhe.

## 3. Leuchten-Realdaten (Notbetrieb) — Kalibrier-Referenz

### 3a. Schrack-Technik (Relux, WHA Aichholzgasse 35, S. 4–9)

| Artikel | Optik/Rolle | Φ Leuchte (Notbetrieb) | Φ Lampe | P | CIE-Flux-Code | LDT im Repo? |
|---|---|---:|---:|---:|---|---|
| `NLIL.L423.` corridor lens | Fluchtweg-SL Corridor | **211 lm** | 240 | 0 W* | 29 55 91 98 88 | ~ (NLKBU corridor da) |
| `NLIL.L423.` round lens | SL/Antipanik Rund | **208 lm** | 240 | 0 W* | 23 78 99 99 87 | ✅ `antipanik_nlildl423_round.ldt` |
| `NLKSC003WL` Akku LiFePO4 3,2V/3,0Ah -3h | SL, 4×HP-LED, Rund | **146 lm** | 170 | 4,0 W | 42 70 90 84 85 | — |
| `NLKWIC433._1h_3h` +4 corridor lenses (cross) | Garage-Hochleistung Corridor | **387 lm** | 520 | 0 W* | 29 55 89 97 76 | — |
| `NLKWID433W 1h 3h` opal high (cross) | Garage opal | **320 lm** | 520 | 0 W* | 27 55 80 70 61 | — |

\* „0.0 W" = zentralversorgt (kein Akku im Kopf); NLKSC = Einzelbatterie (4 W).

### 3b. din-Sicherheitstechnik (DIALux, Barawitzka, S. 5–6)

| Artikel | Rolle | Φ Notbetrieb | P | NBF | Dauer |
|---|---|---:|---:|---:|---|
| `BASIC 2 E-LED_AP3_Klar` | Antipanik | **147 lm** | 1,3 W | 100 % | — |
| `BASIC 2 E-LED_RZ1_LK3` | Rettungszeichen LK3 | **69 lm** | 1,3 W | 100 % | — |
| `BASIC 2 E-LED_RZ2_LK3` | Rettungszeichen LK3 | **86 lm** | 1,3 W | 100 % | — |
| `BASICsc 2 E-SIGN_RZ-plus_1-3h` | Rettungszeichen | **79 lm** | 2,5 W | 100 % | 1–3 h |
| `BASICsc 2 E-SIGN_SL_1-3h` | Sicherheitsleuchte | **53 lm** | 1,4 W | 100 % | 1–3 h |

→ Notbetriebs-Lichtströme liegen **40–400 lm** (nicht die generischen „200 cd" der
Engine-Annahme). RZ-Leuchten 53–86 lm, Fluchtweg-SL ~150–210 lm, Garage-Optik
320–390 lm. Bestätigt `PRODUKTE_SCHRACK_DIN.md` (Rolle ≠ Produkt: AP3/E-LED als
Universalkopf mit Linsenwahl).

## 4. Per-Raum-Ergebnisse (Relux, WHA Aichholzgasse 35) — Golden-Kandidaten

Alle Gänge: Montagehöhe 2,5 m, MF 0,80, Nutzebene 0,02 m, Randzone 0,5 m. Ē/Emin/Emax
in lx. Leuchten = NLIL (corridor/round, 208–211 lm) + NLKSC Akku (146 lm).

| Bereich (Seite) | Fläche | Leuchten | Ē | Emin | Emax | g1 | g2 |
|---|---:|---|---:|---:|---:|---:|---:|
| Gang 2.DG (S.10) | 7,74 m² | 1 round + 1 Akku | 4,35 | 2,44 | 11 | 0,560 | 0,221 |
| Gang links 1.OG–1.DG (S.16) | 23,38 m² | 1 corridor + 1 Akku | 3,31 | 1,29 | 5,82 | 0,389 | 0,221 |
| Gang rechts 1.OG–1.DG (S.22) | 17,34 m² | 1 round + 3 Akku | 5,35 | 2,11 | 9,74 | 0,393 | 0,216 |
| Gang EG links (S.28) | 31,40 m² | 2 corridor + 2 Akku | 4,38 | 1,71 | 10 | 0,392 | 0,164 |
| Gang EG rechts (S.34) | 22,29 m² | 1 round + 4 Akku | 5,02 | 2,03 | 11 | 0,404 | 0,180 |
| Gang links 1.UG (S.40) | 36,67 m² | 2 corridor + 3 Akku | 4,44 | **1,00** | 14 | 0,225 | 0,071 |
| Gang rechts 1.UG (S.46) | 24,74 m² | 1 round + 4 Akku | 3,94 | **1,00** | 11 | 0,253 | 0,091 |
| **Garage (S.52)** | **210,00 m²** | 3× NLKWIC(387) + 3× NLKWID(320) | 5,21 | **1,00** | 15 | 0,191 | 0,064 |

**Beobachtungen (Platzierungs-Lehre):**
- **Designer dimensionieren exakt auf Emin = 1,00 lx** (UG-Gänge + Garage treffen
  1.00 punktgenau) — das Fluchtweg-Minimum ist die Auslegungsgrenze, nicht Ē.
- Gang-Muster: **je Segment 1 Fluchtweg-Leuchte (corridor/round) + N Akku-SL**; die
  NLKSC-Akku-Leuchte ist der Antipanik-/Grundlast-Arbeiter, die NLIL die
  Fluchtweg-Optik.
- **Corridor-Optik längs der Gangachse gedreht** (Koordinatenliste: Rotation Z =
  −90°/90°/−5°) → **bestätigt Optik-aus-Achse (#119)** an Realdaten.
- **Garage 210 m²: 6 Leuchten** (X = 2,7/11/17/23/28/33 m bei Y=3,0, cross-orientiert)
  → ~5–6 m Raster für Emin 1,0 lx. Hochleistungs-Corridor-Optik (387/320 lm).

## 5. Treppe (DIALux, Barawitzka Stiege A, 16,37 m²)

- 7× `BASICsc 2 E-SIGN RZ-plus` (79 lm) + 3× `SL` (53 lm), **Montagehöhen je
  Podest** (2,52 / 5,40 / 8,28 / 10,80 m — ein RZ-Podest je Geschoss).
- Berechnungsfläche (Podest, Höhe 4,332 m): Ē 3,13 lx, Emin 1,97, Emax 5,43,
  Ē/Emin 1,59, Emax/Emin 2,76. Reflexionsgrade gelistet (70/48,7/20 %), aber Szene
  ohne Reflexion.

## 6. Engine-Konsequenzen (Zusammenfassung)

1. **Wartungsfaktor 0,80/0,57 fehlt** in `lux.py`/`deckung.py` → Kern-Slice
   (Mechanismus F2-Lane; Norm-Wert 0,80/0,57 via `NormAnforderung`, Enis-Naht).
   Kalibrier-Test-Kandidat: Gang links 1.UG (2 corridor + 3 Akku, 36,67 m²,
   Soll Emin ≈ 1,0) oder Garage.
2. **Reflexion = 0** → bewusste Engine-Annahme, durch beide Reports validiert.
3. **Optik-aus-Achse (#119)** an Realdaten bestätigt (Corridor-Rotation längs Gang).
4. Randzone 0,5 m / Nutzebene 0,02 m = Engine-konform.
5. Möblierungs-Verschattung = offener Backlog (braucht RaumModell-Möbel, nachrangig).
6. Notbetriebs-Lichtströme 40–400 lm real → künftig Katalog-Φ statt generischer cd.

## 7. Engine-Baustein: `platzierung/lux_nachweis.py` (2026-09-08, F2)

Alle drei Profi-Reports liefern **denselben Nachweis** je Rettungsweg — die Engine
platzierte danach (`deckung`), gab ihn aber nie als Bericht aus. Neues, **isoliertes**
Modul `platzierung/lux_nachweis.py` (F1-kollisionsfrei — reine Konsumption des fertigen
`PlatzierungsErgebnis`, ändert keine Platzierung) erzeugt genau die Profi-Struktur:

- `nachweis_fluchtweg(raum, norm, ergebnis, …) → list[FluchtwegNachweis]` — je Korridor:
  **Emin Mittellinie** (Soll ≥ 1 lx), **Emin Mittelfläche** (Soll ≥ 0,5 lx), **Ud=Emin/Emax**
  (Soll ≥ 1:40), Wartungsfaktor (aus `anf.wartungsfaktor`, defensiv), `erfuellt`, `norm_quelle`.
- `nachweis_summary(…) → dict` (JSON-fähig) für `render_summary["lux_nachweis"]`.

**Hauptengine-Naht (offen, additiv):** `pipeline.run` ruft `nachweis_fluchtweg` + hängt
`nachweis_summary` unter `render_summary["lux_nachweis"]` (wie `["pruefung"]`/`["oib"]`);
Render kann daraus eine EN-1838-Nachweistabelle ins Blatt setzen. Wird koordiniert mit F1
gemacht (COORDINATION 2026-09-08), da `pipeline.py`/Render F1-Lane sind.
