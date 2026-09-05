# Wegbreite > 2 m und Randstreifen — Befund und Anschlussvorschlag

> Enis (@EnisAMG), 2026-09-05. Der Normwissen-Teil ist umgesetzt; alles unter
> „Anschlussvorschlag" ist **Vorschlag, nicht angewendet** — es berührt
> `platzierung/**` (@mvpo3) bzw. `hauptengine/contracts/**` (3-Owner).
>
> Quelle durchgehend: `knowledge/EN 1838 - Notbeleuchtung 2019 (1).pdf`, Kopfzeile
> **„EN 1838:2013 (D)"** — dieselbe Ausgabe wie für alle übrigen Werte.

## 1. Die vier Größen, fachlich getrennt

| Größe | Wortlaut | Fundstelle |
|---|---|---|
| **Mittellinie** | „Bei Rettungswegen mit einer Breite **bis zu 2 m** müssen die horizontalen Beleuchtungsstärken auf dem Boden entlang der Mittellinie des Rettungsweges mindestens 1 lx betragen." | §4.2.1 Satz 1, Norm-S. 9 |
| **Mittelbereich** | „Der Mittelbereich, der nicht weniger als der **Hälfte der Breite** des Weges entspricht, muss mindestens mit **50 % dieses Wertes** beleuchtet sein." | §4.2.1 Satz 2, Norm-S. 9 |
| **Breitere Wege** | „Breitere Rettungswege **können** als mehrere 2 m breite Streifen betrachtet werden **oder** mit Antipanikbeleuchtung ausgerüstet werden." | §4.2.1 Satz 3, Norm-S. 9 |
| **Randstreifen** | „Die horizontale Beleuchtungsstärke darf 0,5 lx auf der freien Bodenfläche im **Kernbereich** nicht unterschreiten, wobei **Randbereiche mit einer Breite von 0,5 m** nicht berücksichtigt werden." | **§4.3.1**, Norm-S. 11 |

Drei Punkte, die auseinandergehalten werden müssen:

1. Die **2 m** sind ein **Geltungsbereich**, kein Planungsmaß. Oberhalb gilt nicht
   „strenger", sondern **ein anderer Satz**.
2. Satz 3 ist eine **KANN-Aussage mit zwei Wegen**. Welchen man geht, ist eine
   Planer-Entscheidung — dieselbe Logik wie bei der OIB-„Kann"-Gleichstellung für
   Verkehrsbauwerke.
3. Der **Randstreifen gehört zu §4.3.1 (Antipanik)**, nicht zu §4.2.1. Der
   Rettungsweg-Nachweis kennt keinen Randstreifen, sondern Mittellinie +
   Mittelbereich.

**Anhang B** (Norm-S. 16–17, informativ) führt Frankreich, Italien, Deutschland
und die Niederlande. **Für Österreich gibt es keine A-Abweichung**; keine der
Abweichungen ändert die 2-m-Grenze oder den Mittelbereich. Die französischen
Sonderregeln (Leuchtenabstand ≤ 15 m, 5 lm/m², Abstand < 4 × Montagehöhe) gelten
nur dort und sind keine Auslegungshilfe für Österreich.

## 2. Abgleich mit #108 (`platzierung/deckung.py`, `lux.py`)

**Was bereits geprüft wird — und richtig ist:**

* `lux_punkte` auf der **Mittellinie** gegen `anf.min_lux` (1 lx) → §4.2.1 Satz 1.
* Ein **Mittenband** bei ± Breite/4 gegen `ziel/2` → Satz 2 korrekt modelliert:
  ein Band der halben Breite hat die Offsets ± B/4, und 50 % des Wertes ist der
  halbe Zielwert.
* Ud auf der Mittellinie (§4.2.2).

**Was fehlt:**

| Lücke | Belegstelle im Code | Wirkung |
|---|---|---|
| **Der 2-m-Geltungsbereich wird nicht geprüft** | `deckung.py::verdichte_fluchtweg` — kein Vergleich gegen eine Grenze | Bei einem 6 m breiten Weg wird ein Nachweis geführt, den §4.2.1 für diese Breite nicht vorsieht; das Band wächst auf ± 1,5 m mit, ohne dass Satz 3 je gestellt wird |
| **Die Breite wird aus der Bounding-Box geraten** | `breite = min(bounds[2]-bounds[0], bounds[3]-bounds[1])` | Für einen L-förmigen oder schrägen Korridor ist das nicht die Wegbreite |
| **`rand_mm=500` trägt die falsche Fundstelle** | `lux.py::lux_raster`-Docstring: „Randstreifen, der laut EN 1838 **§4.2.1** vom Nachweis ausgenommen ist" | Der Wert ist richtig (0,5 m) und wirkt am richtigen Ort (Antipanik-Raster), stammt aber aus **§4.3.1**. Im Fluchtweg-Fallback wird er zusätzlich auf einen §4.2.1-Nachweis angewandt, der keinen Randstreifen kennt |
| **Randstreifen wirkt auf die Bounding-Box** | `lux_raster` schneidet `bounds_mm` um `rand_mm` ein | §4.3.1 nennt den Randbereich der **freien Bodenfläche im Kernbereich**; bei nicht-rechteckigen Räumen ist der bbox-Rand etwas anderes |

**Welcher Eingabewert fehlt:** eine **belegte Wegbreite je Fluchtweg-Abschnitt**.
Weder `RaumModell` noch `FluchtwegSegment` führen sie; die Raumerkennung erzeugt
sie heute nicht. Ohne sie ist nicht entscheidbar, ob Satz 1 oder Satz 3 gilt — und
sie zu raten hieße, den Geltungsbereich der Norm zu erfinden.

## 3. Umgesetzt (normwissen, eigene Lane)

* `data/en1838_grundwerte.yaml`, neuer Abschnitt `geometrie`: `max_breite_mm`
  (2000), `mittelbereich_breite_anteil` (0.5), `mittelbereich_lux_anteil` (0.5),
  `breiter_weg_optionen` + `breiter_weg_entscheidung: planer`,
  `antipanik.randstreifen_mm` (500) — jeweils mit Wortlaut und Fundstelle.
  **Keine doppelte Zahlenpflege:** die Anteile rechnen auf `lux.rettungsweg`, es
  gibt keinen zweiten Absolutwert. **Kein Default für die Wegbreite.**
* `En1838NormProvider.weg_nachweis(breite_mm)` → `WegNachweis` mit
  `regime = mittellinie | breiter_weg | unbestimmbar`, den abgeleiteten
  Mittelbereichs-Werten und `review_erforderlich` samt Begründung.
* `antipanik_randstreifen_mm()` / `antipanik_randstreifen_quelle()` — mit §4.3.1
  als Quelle, ausdrücklich getrennt vom Rettungsweg.
* `hat_at_abweichung()` → `False` (Anhang B, Österreich).

Diese Methoden sind — wie die Sonderstellen-Methoden — ein **Prototyp**: nicht im
`ports.NormProvider`-Protocol, `WegNachweis` ist ein normwissen-eigener Typ. Kein
Konsum über `getattr`, kein paketübergreifender Import.

## 4. Anschlussvorschlag (nicht angewendet)

### 4a. Eingabewert — 3-Owner, Erkennung @polatselman

```python
 class FluchtwegSegment(BaseModel):
     segment_id: str
     polyline_mm: list[XY]
     reason: str
+    #: Lichte Breite des Weges an diesem Abschnitt. None = unbekannt → der
+    #: §4.2.1-Geltungsbereich ist nicht entscheidbar (kein Default!).
+    breite_mm: float | None = None
```

Rein additiv; `raum_modell`-`CONTRACT_VERSION` **1.1.0 → 1.2.0**, Schema-Regen,
Fixture-Nachzug. Die Erkennung (Wandabstand quer zur Wegachse) kann später
folgen — bis dahin bleibt das Feld `None`, was ehrlich ist.

### 4b. Konsumption — @mvpo3

```diff
-        breite = min(bounds[2] - bounds[0], bounds[3] - bounds[1])
-        linie, band = _nachweis_punkte(mittellinie(...), breite)
+        nachweis = norm.weg_nachweis(segment_breite_mm)   # None, solange 4a fehlt
+        if nachweis.regime != "mittellinie":
+            # >2 m oder unbekannt: §4.2.1 Satz 1 ist nicht anwendbar. Kein
+            # stiller Nachweis — der Fall gehört in den Prüfbericht.
+            ...
+        linie, band = _nachweis_punkte(
+            mittellinie(...), nachweis.mittelbereich_breite_mm * 2
+        )
```

### 4c. Prüfbericht

Zwei neue Regeln im Muster 8b/12:

* **Weg breiter als 2 m** → Warnung: „§4.2.1 lässt Zerlegung in 2-m-Streifen ODER
  Antipanikbeleuchtung zu — Planer-Entscheidung, nicht automatisch getroffen."
* **Wegbreite unbekannt** → Warnung: „Geltungsbereich des Mittellinien-Nachweises
  nicht bestimmbar."

### 4d. Kleine Korrektur, unabhängig davon — @mvpo3

Der Docstring von `lux.py::lux_raster` schreibt `rand_mm` §4.2.1 zu; richtig ist
**§4.3.1**. Reine Doku-Korrektur, kein Verhalten.

## 5. Was offen bleibt

* Ohne 4a bleibt jede Breiten-Auswertung eine Schätzung — deshalb ist in
  `normwissen` bewusst **kein** Default hinterlegt.
* Der Randstreifen wirkt weiterhin auf die Bounding-Box statt auf die freie
  Bodenfläche; das ist eine Geometrie-Frage in `platzierung`, kein Normwert.
* `flaechen_schwellen` und `engine_status` sind davon unberührt.
