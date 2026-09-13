# Raumerkennung Rennweg — Bericht

Stand **2026-09-13** · Owner Selman (`raumerkennung`) · Branch `selman/geschoss-erkennung`
Gerechnet auf Commit **`511ad36`** (identische Kennzahlen wie der erste Lauf auf `538d8d8`).
`src/` ist dort `origin/main` `c820b68` plus der eigene,
nicht freigegebene Geschoss-Commit `47e9e44`. **Gegenprobe auf reinem `origin/main`:** alle
Owner-Kennzahlen der 7 Pläne identisch; nur das Geschoss fehlt dort (leer statt DG/EG/1OG …).

- **Eingang:** `Projekte_Leere Architektpläne (Input)/Rennweg.zip` → 7 DXF, entpackt nach
  `Projekte_Leere Architektpläne (Input)/Rennweg/` (gitignored, so in `main` vorgesehen).
- **Ausgabe:** `Projekte/_ergebnis_raumerkennung/README.md` → `Rennweg/README.md` (im
  GitHub-Browser lesbar, Bilder eingebettet). Offline dieselben Inhalte als `index.html`.

Dieser Durchgang ist **nur Messen und Darstellen**. An der Erkennung wurde nichts geändert.
Alles unter § 2 ist offen.

---

## 1. Ergebnis je Plan

| Plan | Räume | UNBEKANNT | mit Stempel | Abw. > 10 % | Wohnungen | Räume je Wohnung | Laufzeit s |
|---|--:|--:|--:|--:|--:|---|--:|
| UG  | 23 | 10 | 17 | 0 | 4 | 1 · 1 · 1 · 1 | 16,9 |
| EG  | 22 |  5 | 19 | 0 | 2 | 4 · 1 | 22,6 |
| OG1 | 18 |  1 | 15 | 0 | 3 | 9 · 1 · 1 | 18,3 |
| OG2 | 18 |  1 | 15 | 0 | 2 | 10 · 1 | 20,8 |
| OG3 | 15 |  1 | 10 | 0 | 2 | 5 · 3 | 18,2 |
| DG1 | 15 |  1 | 11 | 1 | 1 | 8 | 18,1 |
| DG2 | 14 |  0 |  7 | 0 | 1 | 4 | 18,6 |
| **gesamt** | **125** | **19** | **94** | **1** | **15** | | 133,5 |

7 von 7 ausgewertet · 0 kein Grundriss · 0 Dubletten · 0 Fehler · Wandzeit 0,8 min.

**Dubletten:** innerhalb von `Rennweg.zip` keine. Alle 7 Dateien sind byte-identisch (SHA-256)
mit `Projekte/Rennweg/*.dxf`, das EG zusätzlich mit `Projekte/_eingang/Rennweg_EG.dxf`.
Gerechnet wurde nur der Eingangsordner.

**Nicht-Grundrisse:** `Rennweg.zip` enthält keine. Die Dachdraufsicht `DD - …` und
`Legende/Baulegende.dxf` liegen nur unter `Projekte/Rennweg/`, nicht im ZIP.

---

## 2. Befunde an der Erkennung — nicht repariert

### 2.1 Wohnungsbildung: 8 von 15 „Wohnungen" sind ein einzelner Raum

| Plan | Einraum-„Wohnung" (Typ, m², Stempel) |
|---|---|
| UG  | `top_1` WC 6,2 („Beh.WC / WC-D") · `top_2` WC 1,5 („WC-D") · `top_3` WC 1,5 („WC-H") · `top_4` ABSTELLRAUM 1,1 („AR") |
| EG  | `top_2` KÜCHE 9,3 („v.Küche") |
| OG1 | `top_2` ABSTELLRAUM 4,5 („AR") · `top_3` WC 3,5 („WC") |
| OG2 | `top_2` ZIMMER 22,2 („Zimmer") |

Am anderen Ende umfasst OG1 `top_1` 9 Räume (4 Zimmer, 2 Bäder, 2 Vorräume, Gang) und
OG2 `top_1` 10 Räume (4 Zimmer, 3 Bäder, WC, Gang, Vorraum). Ob das je eine Wohnung ist, ist
am Plan zu prüfen.

Die großen Wohnräume sind UNBEKANNT (§ 2.2) und gehören darum zu keiner Wohnung:
`wohnungen.py` verbindet nur Räume der Nutzungsklasse `WOHNUNG_PRIVAT`.

### 2.2 UNBEKANNT: 19 Räume, 15 davon mit lesbarem Stempel

Stempeltexte, aus denen kein Typ entsteht:

- **EG:** „GESCHÄFTLOKAL" 111,0 m² · „Geschäftslokal 1" 29,1 · „Garageneinfahrt" 14,1 ·
  „Zugangsweg" 5,5 · „Müllplatz" 4,0
- **UG:** „DBA Raum" 6,1 · „WR-H" 5,8 und 1,5 · „WR-H /Umkleide" 5,7 · „Umkleide-D" 4,9 ·
  „WR-D" 2,8 · „Dusche-H" 1,5
- **OG1:** „Wohnkche" 73,1 m² (so im Plan geschrieben, ohne ü)
- **OG2:** „Wohnbereich" 59,5 m²
- **DG1:** „TV Raum" 15,9 m²

Ohne Stempel: UG 27,8 · 20,1 · 15,2 m², OG3 10,1 m².

### 2.3 Außenbereich liegt auf erkannten Räumen

Schnittfläche der offenen Außenbereiche (`provider.letzte_aussenbereiche.offen`) mit den
Raumpolygonen:

| DG1 | OG3 | OG1 | OG2 | DG2 | EG | UG |
|--:|--:|--:|--:|--:|--:|--:|
| 122,6 m² | 110,4 m² | 46,4 m² | 44,1 m² | 16,0 m² | 0 | 0 |

Im Bild als blaue Schraffur über Zimmern, Bädern und dem DG1-Wohnzimmer sichtbar.

### 2.4 Stiegenhaus

- **Rest am Lift:** neben jedem Lift bleibt eine eigene STIEGENHAUS-Fläche, die den Lift
  berührt: UG 0,95 · EG 0,96 · OG1 1,00 · DG1 0,73 · DG2 0,87 m². OG2 und OG3 haben sie nicht.
- **DG2:** ein achsparalleles STIEGENHAUS-Rechteck von 15,9 m² liegt über ZIMMER (2,3 m²
  Überlappung), VORRAUM (2,4 m²) und einer zweiten Stiegenhausfläche (6,4 m²). DG2 hat
  insgesamt 5 STIEGENHAUS-Flächen: 15,9 · 6,6 · 4,0 · 1,2 · 0,9 m².

### 2.5 Stempel

- **DG1:** WOHNZIMMER 73,9 m² gegen Stempel „Wohnzimmer" 83,93 m² = −11,9 %. Das ist die
  einzige rote Zahl in Rennweg. Alle anderen zugeordneten Stempel mit m²-Angabe liegen
  innerhalb ±10 %.
- **OG2:** Stempel „VR" 4,92 m² ist keinem Raum zugeordnet (`kein_polygon`). Er liegt in einem
  VORRAUM-Polygon von 4,9 m², das selbst keinen Stempel trägt. Im Bild: magenta ×.
- **EG, zweite Zeichnung:** Stempel „Stiegenhaus" liegt 450 mm neben seinem
  STIEGENHAUS-Polygon (6,7 m²). Im Bild: rote Linie.
- **EG:** 11 der 19 Stempel tragen keine m²-Angabe (die ganze zweite Zeichnung). Dort ist die
  10-%-Prüfung nicht möglich.

### 2.6 EG: zwei Grundrisse im selben Modelspace

Der EG-Modelspace trägt zwei Zeichnungen, 1,38 km auseinander (Δx 736 m, Δy 1167 m), mit je
11 Räumen. Die zweite enthält `top_1` (Wohnküche 45,6 · AR 5,1 · Bad/WC 5,1 · Zimmer 11,1),
Vorraum 21,0, Garage 36,5, Terrasse 17,1, Stiegenhaus 6,7 und drei Außenflächen. Welches
Gebäude oder Geschoss das ist, sagt der Plan hier nicht. Im Index als „Ausschnitt 2 von 2".

### 2.7 Typ aus Mischstempel — zur Kenntnis

„Hobbyraum/Fitness" → ZIMMER (OG3) · „v.Küche" → KÜCHE (EG) · „VR/Büro" → VORRAUM (DG2) ·
„KiWa - Fahrradraum" → KINDERWAGENRAUM (UG) · „Beh.WC / WC-D" → WC (UG).

### 2.8 Geschoss — Nebenbefund

DG1 und DG2 bekommen beide `DG` (Quelle Dateiname). UG → UG, EG → EG, OG1–3 → 1OG–3OG.

---

## 3. Der bekannte Fall aus dem letzten Lauf — nachgemessen

`Projekte/EG_Grundriss_DE_NEU.dxf` liegt nicht im Eingang und ist nicht Teil der Ausgabe.
Einzeln nachgerechnet mit derselben Erkennung (`src/` wie `538d8d8`), Zuordnung aus
`KaskadeErgebnis.zuordnungen`:

- **„BAD/WC" 6,93 m²** liegt geometrisch im 22,5-m²-ZIMMER, ist von der Erkennung aber
  **keinem Raum zugeordnet** (`kein_polygon`). Das ZIMMER trägt den Stempel „ZIMMER" 11,89 m²
  (`flutung_unsicher`, +89 %). Das alte Bild (`gesamtdarstellung._stempel_je_raum`,
  Punkt-in-Polygon) hat BAD/WC diesem Raum angeheftet. Die Erkennung tat das nicht.
- Der zweite „BAD/WC"-Stempel 6,93 m² ist einem BAD von 11,5 m² zugeordnet
  (`flutung_unsicher`, +66 %).
- **„Top 1" 55,36 m²** ist tatsächlich einem UNBEKANNT-Raum von 13,3 m² zugeordnet
  (`flutung_unsicher`). „Top 2" 55,36 m² bleibt ohne Raum.

Der Wohnungsstempel wird also wie ein Raumstempel geflutet. Die BAD/WC-Zuordnung aus dem
letzten Lauf war dagegen ein Artefakt der Darstellung.

---

## 4. Darstellung — Entscheidungen

- **Ausrichtung:** die 7 Rennweg-DXF haben keine Papierbereich-Viewports (Roh-Scan der
  VIEWPORT-Entities). Geplottet wird der Modelspace, also 0°. `plan_pruefen._rotation` liefert
  ebenfalls 0°.
- **EG hat zwei Bilder** statt einem (§ 2.6). Die Legende zählt je Bild.
- **Bildbreite** adaptiv 2500–8000 px Plananteil. Rennweg: rund 2550 px Plan + 640 px Legende.
- **Label ohne Platz:** □ im Raum, in Legende und Index gezählt. Betrifft 1 Raum im DG2.
- **Stempel-Linie:** wenn der Stempel mehr als 0,3 m neben dem zugeordneten Raum liegt oder im
  Inneren eines anderen Raums.
- **Grau** umfasst auch Müllraum, Waschküche und Kinderwagenraum. Das steht so in der Legende.
- **kennzahlen.json:** die Owner-Kennzahlen stehen oben, `kontext` erklärt nur das Bild.
- **256-Farben-PNG** mit exakten Signalfarben. Gemessen: Median-Cut allein zog Magenta
  #ff00ff auf #fb63ff.

## 5. Reproduktion

```
.venv/Scripts/python.exe scripts/analyse/raumerkennung_darstellung.py --ordner Rennweg --neu
```

Das Skript entpackt die ZIPs, rechnet Rennweg und schreibt beide Index-Seiten. Nur die
Index-Seiten: `--nur-index`. Bilder aus dem Cache: `--nur-zeichnen`.
