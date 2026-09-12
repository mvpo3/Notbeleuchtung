# Entscheidungsvorlage: der Layer-Korpus trägt kein Label

**An:** @mvpo3 · **Von:** Selman (`raumerkennung`) · **Stand:** `91ad7cc`,
2026-09-12 · **Status:** Vorlage, **nicht entschieden**

Alle Zahlen unten sind auf `91ad7cc` selbst gemessen. Wo eine Zahl aus einer
früheren Runde stammt und ich sie nachgemessen habe, steht das Ergebnis der
Nachmessung — auch wenn es die alte Angabe widerlegt.

---

## 1. Der Befund

`schreibe_korpus` speichert `b.rolle`, also die **Ausgabe von
`entscheide_rolle`**, und daneben `label_quelle="namensregel_heute"`. Ein
Label-Feld existiert nicht: die Zeilen tragen `rolle`, `confidence`, `modus`,
`label_quelle` — kein `label`.

Selbst nachgezählt, `rolle` gegen `label_namensregel` je (Plan, Layername):

| | Zeilen |
|---|--:|
| `rolle` == Namensregel-Label | 292 |
| **Widerspruch** | **209** (41,7 %) |
| ohne Gegenstück | 0 |
| Summe | 501 |

Je Plan: Barawitzka_EG 72 · Mollgasse_EG 51 · EG_Grundriss_DE_NEU 28 ·
Fischamend BT1 EG 20 · Muthgasse_E2 16 · Rennweg_EG 11 · Rennweg_OG3 11.

Für diese 209 Zeilen ist die Herkunftsangabe `label_quelle` **faktisch falsch**.
Wer auf `rolle` trainiert, bringt einem Modell bei, `entscheide_rolle` zu
imitieren — genau dein Zirkularitäts-Einwand.

**Die Richtung der Widersprüche ist der interessante Teil:**

| `rolle` statt Label | Zeilen |
|---|--:|
| `wand` statt `rest` | **119** |
| `rest` statt `oeffnung` | 24 |
| `rest` statt `wand` | 22 |
| `raumkontur` statt `rest` | 22 |
| `wand` statt `oeffnung` | 8 |
| `rest` statt `raumkontur` | 8 |
| `oeffnung` statt `rest` | 5 |
| `wand` statt `raumkontur` | 1 |

**119 der 209** sind Layer, die die Regel als `wand` erkennt und die
Namensregel als `rest` abtut. Das ist kein Argument für eine der beiden Optionen
— aber es heißt: das Namensregel-Label ist nicht automatisch das bessere
Trainingsziel. Wer es einspeist, trainiert unter anderem auf 119 Layer, die
geometrisch nach Wand aussehen und nur keinen erkennbaren Namen haben.

### 1a. Zweiter Befund, beim Nachmessen aufgefallen

Der Korpus ist **nicht selbstgenügsam**. Der 37er-Vektor trägt weder
`flaeche_median_m2` noch `n_punkte`, `entscheide_rolle` braucht aber beide (den
Flächen-Term in `s_raum` und den Geometrie-Deckel). **Der Regel-Entscheid ist
aus dem Korpus allein nicht reproduzierbar.** Für diese Vorlage musste ich über
`Projekte/_layermerkmale/merkmale.json` gehen und den Flächen-Term aus
`scores["raumkontur"]` zurückrechnen (gelingt für 501 von 501 Layern im
gültigen Bereich). Wer den Korpus später ohne die Merkmalstabelle bekommt, kann
weder die Rolle nachrechnen noch die Deckel nachvollziehen.

---

## 2. Option A — Label-Feld plus Herkunfts-Flag

`_korpus_zeile` um `label` erweitern, `schreibe_korpus` ein
`labels`-Mapping `(plan_id, layer_name) -> Rolle` mitgeben; `label_aus_namensregel`
liegt im Aufrufer `scripts/analyse/layer_merkmale.py` bereits bereit. Dazu ein
Feld, das die tatsächliche Herkunft je Zeile führt (Namensregel / Regel-Ausgabe /
später: Mensch).

| | |
|---|---|
| Aufwand | klein, eine Funktion plus Testanpassung |
| Vektor | **unverändert** — kein Versionssprung nötig |
| Wirkung auf die 209 | **keine** — die Widersprüche bleiben alle 209, sie sind danach nur korrekt *beschriftet* statt falsch deklariert |
| löst | die falsche Herkunftsangabe, die Zirkularität beim Training |
| löst nicht | die Frage, welches Label das richtige Ziel ist |

Option A behebt also eine **Falschaussage**, nicht die Sachfrage.

---

## 3. Option B — Renormierung der Gewichte

Der neutrale Wert 0,0 in den Feldern 31–37 ist arithmetisch kein Neutrum:
`s_oeffnung` hängt zu 0,25 an `wand_parallel_quote` und zu 0,20 an
`wand_endpunkt_quote` (zusammen **0,45** von 1,00), `s_raum` zu je 0,20 an
`wand_umschlossen_quote` und `wand_kontur_deckung` (**0,40**), während `s_wand`
nur die Wandfern-Dämpfung überspringt. Renormierung heißt: nicht messbare Terme
streichen und die Restgewichte auf Summe 1 skalieren.

**Durchgerechnet über alle 501 Layer** (Wegwerf-Skript, kein Eingriff in den
Produktionscode; Gegenprobe: der Nachbau reproduziert mit `renorm=False`
**0 Rollen- und 0 Modus-Abweichungen**, ist also exakt):

| | Zeilen |
|---|--:|
| von den 209 Widersprüchen kippen auf das Label | **2** |
| neu widersprüchlich | **8** |
| **netto** | **−6** (mehr Widerspruch, nicht weniger) |
| Rollen-Wechsel gesamt | 10, **alle** `rest → oeffnung` |
| Modus-Wechsel | 3 (2× HARD_STOP → BESTAETIGEN, 1× BESTAETIGEN → UEBERNEHMEN) |

| | |
|---|---|
| Aufwand | mittel, Score-Formel plus Flag-Logik |
| Vektor | **verschiebt sich** → `lf-3`, Korpus komplett neu schreiben |
| löst | die falsche Neutralität, systematische Richtung auf `wand`/`rest` |
| löst nicht | das Label-Problem — messbar **nicht**: netto sechs Widersprüche mehr |

---

## 4. MAJOR 2 gehört mit entschieden

`runde2_belegt` steht auf Zeilen `True`, die die Felder 32–34 strukturell nicht
messen können. Selbst nachgezählt:

| | Zeilen |
|---|--:|
| ohne eigene Segmente (`laenge_p50_mm == 0`) | 115 |
| davon ganz ohne Geometrie | 28 |
| **davon segmentlos MIT Geometrie** (der Problemfall) | **87** |
| davon `rolle = wand` | 14 |
| davon Modus `UEBERNEHMEN` | **6** von insgesamt nur 16 |

**Eine Zahl aus der Vorrunde ist gefallen:** dort stand „10 Zeilen haben alle
sechs Messfelder auf 0,0 und sind von *gar nicht gemessen* nicht
unterscheidbar". Gemessen sind es **0**. Die Aussage bleibt in ihrer Substanz
richtig (`wand_naehe_quote`, `wand_parallel_quote` und `wand_endpunkt_quote`
sind bei allen 87 strukturell 0), aber nicht in dieser Form.

Bei den 87 greift der Restklassen-Deckel **nicht** — deshalb stammen 6 der 16
automatischen Freigaben aus genau dieser Gruppe.

---

## 5. Raumzahl-Streuung in `test_soll_muthgasse.py` (dein Punkt 4b)

Es sind nicht drei falsche Zahlen, sondern **vier Zählweisen plus drei
Zwischenstände** für dasselbe Wort „Raum":

| Zahl | Fundstelle | Messbasis | Ist auf `91ad7cc` |
|---|---|---|---|
| **114** | Modul-Docstring Z10, Assert-Meldung Z246 („Ist 114") | Roh-Kaskade vor der Bereinigung, inkl. Einträge ohne Polygon | **nicht reproduzierbar** |
| **113** | Z20 („Provider-Parse E2, 825,6 s"), Z41 | Parse-Stand vor der Bereinigung | **nicht reproduzierbar** |
| **109** | Z168, Nebenbefund | Parse auf schmutzigem Arbeitsbaum (unfertige `bereinigung.py`/`kaskade.py`) | **nicht reproduzierbar**, im Text schon so gekennzeichnet |
| 110 | — | `len(raeume)` in `raeume.json` | **110** |
| 97 | `VERLAUF` „Räume gesamt" | Einträge mit ≥ 3 Punkten | **97** |
| 101 | `BAND_RAEUME` | `_zaehle_raeume`: 97 lebend + 4 entfallen | **101** |
| 101 | `bericht.md` „Stempel" | Einträge mit `flaeche_stempel` | **101** |
| 88 | — | `raum_typ` gesetzt | **88** |

**Ursache:** 13 der 110 Einträge in `raeume.json` tragen weniger als 3 Punkte,
also kein verwertbares Polygon (110 − 97). Diese Differenz, kombiniert mit
„vor/nach Bereinigung" und „mit/ohne Entfall", erzeugt die ganze Streuung.

Das Band `>= 98` hält — aber es misst eine **fünfte** Basis (`len(rm.raeume)`
im Modell) und liegt zwischen 97 und 110. Die Assert-Meldung „Ist 114" nennt
einen Wert, den kein aktueller Lauf stützt.

---

## 6. Was zu entscheiden ist

1. **Option A, Option B, oder beide?** Gemessen löst nur A das Label-Problem;
   B ist eine Korrektheitsfrage der Score-Neutralität und verschlechtert die
   Label-Übereinstimmung netto um 6 Zeilen. Beide zusammen sind **ein**
   Neuschrieb (`lf-3`) statt zwei.
2. **Welches Label ist das Trainingsziel?** Namensregel-Label, Regel-Ausgabe,
   oder erst ein von Hand gesetztes? Die 119 `wand`-statt-`rest`-Fälle sagen,
   dass die Namensregel kein neutraler Schiedsrichter ist.
3. **Wird der Korpus selbstgenügsam gemacht?** Ohne `flaeche_median_m2` und
   `n_punkte` ist der Entscheid aus ihm nicht nachrechenbar (Befund 1a).
4. **MAJOR 2 per zweitem Flag** („eigene Segmente vorhanden") oder per
   Renormierung (Option B)? Das zweite Flag ist die kleinere Änderung und
   verschiebt keinen Vektor.
5. **Raumzahl:** soll „Raum" in den Naht-Tests auf **eine** Messbasis
   festgelegt werden, und welche? Die drei nicht reproduzierbaren Zahlen
   gehören dann als Zwischenstände gekennzeichnet, nicht gelöscht.

Reihenfolge bleibt wie vereinbart: **dein Einwand 5 (Gebäudeausgänge) vor
`lf-3`.** Einwand 5 ist in dieser Runde umgesetzt; `lf-3` wartet auf diese
Entscheidung.
