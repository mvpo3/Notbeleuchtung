# Analyse — Notbeleuchtung Baufeld E2 (Referenz-Praxis vs. EN 1838)

**Ziel:** Die vom Planer gesetzte Notbeleuchtung in den 9 Elektromontageplänen
(`Projekte/Baufeld E2/Elektromontageplan_*.dxf`, lokal/gitignored) extrahieren, mit
dem Normwissen (`knowledge/extracted/`) abgleichen und **nachvollziehen, warum** so
platziert wurde. Datenbasis: Streaming-Extraktion aller INSERTs im `Notbel`-Namespace
(Blockname `MEP-LV_Notbel_Fluchtwegleuchte_mit Piktogrammscheibe_<richtung>`).

## 1. Befund (extrahierte Platzierung)

| Etage | RZ-Leuchten | oben | unten | links | rechts | NN-Median |
|-------|-------------|------|-------|-------|--------|-----------|
| UG    | 92  | 39 | 24 | 19 | 10 | 2.0 m |
| EG    | 117 | 33 | 35 | 32 | 17 | 2.4 m |
| 1OG   | 80  | 36 | 18 | 6  | 20 | 2.5 m |
| 2OG   | 41  | 17 | 6  | 9  | 9  | 2.4 m |
| 3OG   | 42  | 17 | 7  | 9  | 9  | 2.4 m |
| 4OG   | 41  | 17 | 7  | 8  | 9  | 2.4 m |
| 5OG   | 41  | 17 | 7  | 8  | 9  | 1.9 m |
| 6OG   | 32  | 15 | 4  | 6  | 7  | 2.6 m |
| **Σ** | **486** | 191 | 108 | 97 | 90 | ~2.4 m |

**Ein einziger Leuchtentyp:** Alle 486 sind „Fluchtwegleuchten mit Piktogrammscheibe"
— **Kombileuchten** (Sicherheitsleuchte + Rettungszeichen in einem Gehäuse),
richtungsaufgelöst (oben/unten/links/rechts). Kein separater Antipanik-Block, kein
reiner Sicherheitsleuchten-Block im `Notbel`-Namespace (Stiegenhaus-Grundlicht liegt
separat als `ET_STGH_DECKENLEUCHTE`).

## 2. Warum so platziert — Abgleich mit EN 1838

### a) Warum Kombileuchten mit Richtungspiktogramm (kein Antipanik)
Baufeld E2 ist ein **Wohn-/Bürobau mit definierten Flucht-Korridoren** — keine großen
offenen Flächen > 60 m² ohne Wegenetz. EN 1838 §4.3 fordert Antipanik **nur** für
solche offenen Flächen (Hallen, Versammlung). Ergo: **korrekt keine Antipanik-Leuchten**
— der Fluchtweg ist überall als Gang/Treppe geführt, also reicht Fluchtweg-Beleuchtung
+ Rettungszeichen. Das erklärt den Ein-Typ-Katalog.

### b) Warum „oben" dominiert (191 / 39 %)
Pfeil **oben = „geradeaus weiter"** entlang des Korridors. Gerade Lauf-Segmente sind
der häufigste Fall → meiste Leuchten. unten/links/rechts (295) sitzen an
**Richtungswechseln, Kreuzungen, Türen, Treppen** (EN 1838 §4.1.2 b/e/f) — dort zeigt
der Pfeil in die Abzweig-/Ausgangsrichtung. **Direkte Bestätigung unseres
Richtungs-Konzepts:** der Planer nutzt vier richtungsspezifische Piktogramme, kein
rotiertes Einheitssymbol — genau wie unsere `notlicht_ks_stiege_{links,rechts,unten}`.

### c) Warum Median-Abstand ~2.4 m + viele Paare ≤ 2 m
EN 1838 §4.1.2: an **jedem** Betonungspunkt (Ausgang, Richtungsänderung, Kreuzung,
Treppe, Niveauwechsel) eine Leuchte **≤ 2 m**. Der durchgehende ~2.4-m-Median +
36–48 Paare ≤ 2 m je Etage zeigt: die Leuchten stehen als **enge Anker-Cluster** an
diesen Punkten, dazwischen entlang der Ganglinie verdichtet (Ziel 1 lx / Ud ≥ 1:40,
EN 1838 §4.2). Kein Zufallsraster — geometrie-getriebene Anker + Linie.

### d) Warum EG/UG/1OG viel, 2.–5. OG gleich, 6OG weniger
- **2.–5. OG = Regelgeschoss:** RZ-Zahl praktisch identisch (41/42/41/41) → **gestapelte
  Standard-Wohngeschosse** mit gleichem Fluchtweg. (Absolut-Koordinaten je Blatt
  verschoben, daher Deckungscheck nur per Anzahl aussagekräftig.)
- **EG (117):** enthält die **letzten Ausgänge ins Freie** (EN 1838 §4.1.2 g — Weg bis
  zur Sammelstelle kennzeichnen) + komplexeste Zirkulation → meiste Leuchten.
- **UG (92):** Garage/Technik, lange Wege, mehrere Brandabschnitte.
- **1OG (80):** größere/gewerbliche Ebene (doppelt so viele wie Regelgeschoss).
- **6OG (32):** oberstes, kleineres/zurückgesetztes Geschoss.

### e) Stromkreis / Systemintegrität (aus Plan-Struktur ableitbar)
Notbeleuchtung liegt auf eigenem Layer-/Symbolsatz (`MEP-LV_Notbel`) getrennt von der
Allgemeinbeleuchtung — konsistent mit dem **getrennten Sicherheitskreis** (EN 1838
§4.1.1, OVE E 8101 §560.9.5; RCD-Verbot). Die Kombileuchten je Brandabschnitt ≥ 2
erfüllen die Systemintegrität (EN 1838 §5.1.8).

## 3. Was das für unsere Engine bestätigt / verlangt

1. **Richtungsspezifische RZ-Blöcke sind Referenz-Praxis** — unser gerade gebautes
   `_select_key`/links-rechts-unten-Konzept bildet exakt die Planer-Logik ab. ✔
2. **Antipanik ist Flächen-getrieben** — im Wohnbau korrekt leer; unsere
   norm-getriebene `plan_antipanik` (nur bei Klassifikation antipanik / offener Fläche)
   trifft das richtige Verhalten. ✔
3. **Anker-≤2 m + Linien-Verdichtung** ist der nächste Ausbau von `plan_rettungszeichen`
   (aktuell 1 RZ je Segment-Endpunkt): Betonungspunkte (Tür/Kreuzung/Treppe) explizit
   ankern + Gang bis 1 lx/Ud verdichten (EN 1838 §4.1.2 + §4.2). → Fahrplan
   Anker→Linie→Fläche in `PLATZIERUNGS_KONZEPTE.md`.
4. **„oben = geradeaus"** als Default-Piktogramm bei geradem Segment einbauen (fehlt
   noch als eigener Block/Key — Lib hat kein „nach oben", aktuell via Rotation).

## 4. Caveats
- Extraktion = INSERT-Blocknamen-Heuristik (`Notbel`-Namespace); wenige Streu-INSERTs
  (Legenden-/Referenzsymbole mit Ausreißer-Koordinaten) sind in den Roh-Counts, ohne
  Median/Verteilung zu verfälschen.
- Lux-/Ud-Werte sind **nicht** aus dem DXF prüfbar (keine Fotometrie im Plan) — die
  Abstands-/Anker-Argumentation ist geometrisch, nicht photometrisch.
- Absolut-Koordinaten je Blatt unterschiedlich referenziert → Geschoss-Deckung nur
  über Anzahl/Struktur, nicht Punkt-für-Punkt.
