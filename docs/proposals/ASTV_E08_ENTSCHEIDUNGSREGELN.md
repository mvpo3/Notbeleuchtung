# Arbeitsstätten-Pfad — belegte Entscheidungsregeln (AStV § 9, OVE-Fachinfo E08)

**2026-09-08 · Enis · Branch `enis/regel-deckung-abnahme-0907`**
**Grundlage:** amtlicher RIS-Ausdruck der AStV (Fassung 06.09.2026, Wortlaut-Auszug
`RIS_AStV_§9_…_Auszug.md`), OVE-Fachinformation E08:2021-04-01 (Volltext, 6 S.),
ÖNORM EN 1838:2019-11-15. Fortführung des Quellenaudits (`K2`, `K5.2`) —
**der Audit wird nicht wiederholt**, nur seine offenen Punkte werden bearbeitet.

**Kein Contract, kein Schema, kein Versions-Bump. Keine Platzierung aktiviert.**

---

## 1. Was der Audit offen ließ — und was davon jetzt geschlossen ist

| Audit-Punkt | Stand 07.09. | Stand 08.09. |
|---|---|---|
| **D1** § 9 Abs. 1 Z 1 (natürliche Belichtung) | ⑥ Eingabe fehlt | **③ als Prüfpunkt geführt**, Eingabe weiterhin offen |
| **D2** Z 3 vs. `besondere_gefaehrdung` | ⑤ Gefahr der stillen Gleichsetzung | **③ ausdrücklich abgegrenzt**, durch Test gesichert |
| **D3** § 9 Abs. 4 (Orientierungshilfen) | ⑥ Ausnahme nicht abgebildet | **③ als Wahlrecht ausgewiesen**, Grenzen belegt |
| **D4** § 1 Abs. 2/3 Reichweite | ⑥ nicht abgebildet | **③ Vorbehalt formuliert**, vier kumulative Bedingungen geführt |
| **E1** Fachinfo E-07/E-08 | ① nur gespeichert | **E08 ③ ausgewertet**; E-07 bleibt ① |
| **L1** AStV-Hinweis erreicht die Ausgabe nicht | 🔴 offen | **auf `main` geschlossen** (#132) — dort tragen die Hinweise jetzt auch die Prüfpunkte |
| **L2** Prüfbericht über die API | 🔴 offen | **unverändert offen** (eigene Aufgabe) |

## 2. Die Regeln, wie sie gelten — vier getrennte Sachverhalte

### 2.1 Anwendungsbereich / Reichweite (§ 1)

```
WENN  gebaeudeteil.arbeitsstaette_nach_aschg IS TRUE
DANN  § 9 gilt innerhalb der Arbeitsstätte → alle drei Tatbestände sind zu prüfen.

WENN  … IS NULL
DANN  zusätzlich ist offen, OB die AStV greift → Prüfpunkte + Statusvorbehalt.

WENN  … IS FALSE
DANN  KEINE AStV-Prüfpunkte für diesen Gebäudeteil,
      ABER: § 1 Abs. 2 erfasst weiterhin die außerhalb einer Arbeitsstätte
      gelegenen, von Arbeitnehmer/innen benutzten Gebäudeteile.
      § 1 Abs. 3 nimmt davon nur aus, wenn ALLE VIER Bedingungen zutreffen:
        (a) Arbeitsstätte umfasst nur einen Teilbereich des Gebäudes
        (b) der Gebäudeteil liegt außerhalb der Arbeitsstätte
        (c) er wird auch von Hausbewohner/innen benutzt
        (d) das Gebäude ist überwiegend zu Wohnzwecken vorgesehen
      Und selbst dann bleibt § 94 ASchG (Behördenauftrag) offen.
```
⚠️ **Kein Umkehrschluss:** aus `False` folgt **kein** „keine Sicherheitsbeleuchtung
erforderlich". Der Test `test_false_erzeugt_keinen_freibrief` nagelt fest, dass
der Vorbehalt in diesem Fall **länger** wird, nicht kürzer.

### 2.2 Fehlende bzw. unzureichende natürliche Belichtung (§ 9 Abs. 1 Z 1 und Z 2)

| | **Z 1** | **Z 2** |
|---|---|---|
| Gegenstand | Arbeitsräume **und** Fluchtwege | ⚠️ **nur Fluchtwege** |
| Tatbestand | **nicht** natürlich belichtet | belichtet, aber die Belichtung **reicht nicht aus**, um bei Ausfall der künstlichen Beleuchtung das rasche und gefahrlose Verlassen zu ermöglichen |
| Art der Feststellung | Bau-/Erkennungstatsache (Fenster, Lichtkuppel) | **Beurteilung** — Gründe laut Wortlaut „bauliche Gegebenheiten", „Lage der Arbeitszeit" |
| Ableitbar aus dem jeweils anderen? | **nein** | **nein** |

**Regel:**
```
Z1_erfuellt  := (raum ist Arbeitsraum ODER Fluchtweg) UND natuerlich_belichtet IS FALSE
Z2_erfuellt  := (abschnitt ist Fluchtweg) UND natuerlich_belichtet IS TRUE
                UND belichtung_reicht_bei_ausfall IS FALSE
unbekannt    := jede der Angaben IS NULL  →  Punkt bleibt `ungeprueft`
```
Keine der drei Angaben existiert heute im `RaumModell` oder `ProjektKontext`
→ jeder Fall endet bei `ungeprueft`, nie bei „erfüllt" oder „nicht erforderlich".

### 2.3 Besondere Gefährdung — zwei verschiedene Dinge

| | **AStV § 9 Abs. 1 Z 3** | **EN 1838 § 4.4** |
|---|---|---|
| Frage | **Ob** eine Sicherheitsbeleuchtung erforderlich ist | **Wie hell** am Arbeitsplatz |
| Bezug | **Bereich** | **Arbeitsfläche** |
| Nebenwirkung | sperrt das Wahlrecht nach Abs. 4 | keine |
| Feld heute | **keines** | `RaumModell.Raum.besondere_gefaehrdung` |

**Regel:** `besondere_gefaehrdung == True` ist **kein** Nachweis für Z 3 und
umgekehrt. Wer beides gleichsetzt, macht aus einem Lux-Attribut eine Rechtsfolge.
Gesichert durch `test_z3_wird_nicht_mit_dem_contract_feld_gleichgesetzt`.

**Lux-Werte, beide Quellen nebeneinander:**

| | EN 1838 § 4.4.1 (Ebene C) | E08 § 5.3 (Ebene D) |
|---|---|---|
| Prozentwert | ≥ 10 % des Wartungswertes der **Aufgaben**beleuchtung | ≥ 10 % der **Allgemein**beleuchtung am Arbeitsplatz |
| Absolute Untergrenze | **15 lx** | **15 lx** |
| Bezugsfläche | **Arbeitsfläche** | (nicht ausdrücklich) |

→ **Die 15 lx sind belegt, die Bezugsfläche fehlt.** `NormRegelwerk.arbeitsplatz_lux`
bleibt deshalb **leer**: ein gefüllter Skalar würde von den Konsumenten auf den
Bodenwert aus `lux_raster` bezogen — eine andere Bezugsfläche. Der Nachweis bleibt
`MANUELL PRÜFEN` (Prüfregel in `hauptengine/validierung.py`).

### 2.4 Zulässige Ausführungswahl (§ 9 Abs. 4)

```
WENN  in den betroffenen Arbeitsräumen/Fluchtwegen KEIN Bereich nach Z 3 liegt
DANN  sind selbst-/nachleuchtende Orientierungshilfen ZULÄSSIG
      — abweichend NUR von Z 1 und Z 2,
      — nur wenn sie ein sicheres Verlassen gewährleisten,
      — Abs. 2 und Abs. 3 Z 1 gelten für sie weiter.
```
⚠️ Es ist ein **Wahlrecht des Planers bzw. Auftraggebers**, keine Regel: die Engine
darf es weder ausüben noch unterstellen. Und es wirkt **nur innerhalb der AStV** —
Anforderungen aus **OVE E 8101 718.560.9.001.AT**, **R 12-2 Tabelle 5.1** oder
**OIB-RL 2 Tabelle 6** bleiben davon unberührt.

## 3. Was heute umgesetzt ist

| Artefakt | Inhalt |
|---|---|
| `normwissen/data/astv_arbeitsstaetten.yaml` | Tatbestände Z 1–Z 3, Wahlrecht Abs. 4, Reichweite § 1, E08-Ausführung (Tabelle 1, Abschn. 4, 5.1–5.3), Betriebspflichten — je mit Ebene, Fundstelle, benötigter Angabe und Status |
| `normwissen/astv.py` | `ArbeitsstaettenWissen`: `pruefpunkte()`, `wahlrecht()`, `reichweite_vorbehalt()`, `ausfuehrung_e08()`, `betriebspflichten()`, `hinweise_fuer_ausgabe()` — **lazy**, ohne Contract-Bezug |
| `data/oib_rl2_tabelle6.yaml::astv_parallelpfad.pruefpunkte_kurz` | ein Satzblock, der die drei Tatbestände und das Wahlrecht **in der Ausgabe** benennt |
| `oib/provider.py::_astv_hinweise` | hängt diesen Block an beide Hinweisvarianten (`True`, `None`) |
| `tests/normwissen/test_astv_arbeitsstaetten.py` | **26 Tests** |

**Was die Engine dadurch zusätzlich kann:** Sie sagt in jedem Plan mit
Arbeitsstätten-Bezug **konkret**, welche drei Tatbestände offen sind, dass Z 2 nur
Fluchtwege betrifft, dass Z 3 nicht das Contract-Feld ist, dass ein Wahlrecht
besteht und wo dessen Grenzen liegen. Vorher stand dort **ein** Satz („kann
zusätzliche Anforderungen begründen").

**Was sie weiterhin nicht kann:** entscheiden, ob eine AStV-Sicherheitsbeleuchtung
erforderlich ist. Alle drei Tatbestände hängen an Angaben, die kein Contract führt.

## 4. Übergabeauftrag — was von Selman und Leonis gebraucht wird

### 4.1 @polatselman — ein `RaumModell`-Feld (3-Owner-Contract)

| | |
|---|---|
| **Benötigte Information** | `natuerlich_belichtet: bool \| None` je `Raum` (und, wenn erkennbar, je Fluchtweg-Abschnitt) |
| **Fachliche Bedeutung** | Trägt AStV § 9 Abs. 1 Z 1. E08 nennt als Merkmal „Belichtungsflächen, wie Fenster oder Lichtkuppeln" |
| **Vorgeschlagene Einbindung** | additives Feld, Default `None` = nicht erhoben; **kein** Default `False` — das wäre eine stille Behauptung |
| **Erwartetes Verhalten** | `None` → Prüfpunkt bleibt `ungeprueft` und erscheint im Bericht · `False` → Z-1-Tatbestand erfüllt, Erforderlichkeit **ausweisen**, nicht platzieren (die Art nennt § 9 nicht) · `True` → Z 1 verneint, **Z 2 bleibt offen** |
| **Testfall** | Raum mit Fenster-Öffnung → `True`; fensterloser Kellerraum → `False`; Raum ohne Auswertung → `None`. In allen drei Fällen: **Platzierung unverändert** |

### 4.2 @mvpo3 + 3 Owner — zwei Felder im `ProjektKontext`

| | |
|---|---|
| **Benötigte Information** | (a) `belichtung_reicht_bei_ausfall: bool \| None` je Fluchtweg-Abschnitt (Z 2) · (b) `orientierungshilfen_statt_sicherheitsbeleuchtung: bool \| None` (Abs. 4) |
| **Fachliche Bedeutung** | (a) ist eine **Beurteilung**, keine Geometrie → gehört in Kontext/LB, nicht in die Erkennung · (b) ist ein **Wahlrecht** des Planers/AG |
| **Vorgeschlagene Einbindung** | beide dreiwertig, Default `None`; (b) zusätzlich nur wirksam, wenn kein Z-3-Bereich angegeben ist |
| **Erwartetes Verhalten** | `None` → Bericht sagt „nicht entschieden" · (b) `True` → Bericht weist die Wahl aus **und** den Vorbehalt, dass sie nur Z 1/Z 2 und nur die AStV betrifft |
| **Testfall** | Kontext mit (b) `True` **und** einem Z-3-Bereich → die Wahl darf **nicht** als zulässig ausgegeben werden |

### 4.3 @mvpo3 — Prüfregel „mehr als 20 Sicherheitsleuchten" (E08 5.2, Ebene D)

| | |
|---|---|
| **Benötigte Information** | Anzahl Sicherheitsleuchten je zusammenhängendem Gebäudeteil (liegt im `PlatzierungsErgebnis` vor) |
| **Fachliche Bedeutung** | E08 empfiehlt ab > 20 Leuchten eine automatische Prüfeinrichtung nach ÖVE/ÖNORM EN 62034; LPS/CPS zusätzlich ≥ 2 alternierende Stromkreise, ≤ 20 Leuchten je Endstromkreis |
| **Vorgeschlagene Einbindung** | Befund in `hauptengine/validierung.py` (gemeinsame Naht), Wortlaut und Fundstelle aus `astv_arbeitsstaetten.yaml` |
| **Erwartetes Verhalten** | reiner **Hinweis** (`warnung`), keine Platzierungsänderung; ausdrücklich als **Ebene D** gekennzeichnet |
| **Testfall** | Plan mit 21 Sicherheitsleuchten → Befund vorhanden; mit 20 → kein Befund |

## 5. Blockiert / bewusst offen

* **AS-9 Aktivierung** (`arbeitsplatz_lux`) — blockiert durch die fehlende
  Bezugsfläche, **nicht** durch fehlende Quelle.
* **E08 Tabelle 1** — setzt 4.1 voraus; zusätzlich ist zu entscheiden, ob eine
  **Empfehlung der Ebene D** überhaupt platzieren darf. Nicht einseitig.
* **L2** (Prüfbericht über die API) — ohne sie bleiben alle Hinweise dieses Blocks
  im Summary und erreichen den Planer nicht über den Plan.
* **AStV-Ausgabenvergleich** (K1) — der zweite Ausdruck fehlt weiterhin.

---

## 6. Blockstatus — vier Ebenen getrennt geführt

**Gesamteinstufung: „Quellenarbeit und Teilimplementierung vorhanden; vollständige
Entscheidungslogik und Integration offen."**

### 6.1 Bereits verwendet (wirkt in der Ausgabe)

| | |
|---|---|
| Artefakt | `astv_parallelpfad.wenn_arbeitsstaette` / `wenn_unbekannt` **+ `pruefpunkte_kurz`** |
| Weg | `oib/provider.py::_astv_hinweise` → `OibBefund.hinweise` → (ab `origin/main`, #132) `gate_summary` → `render_summary["oib"]["hinweise"]` → **`X-Notbeleuchtung`-Header** der API |
| Inhalt | die drei Tatbestände, die Fluchtweg-Beschränkung von Z 2, die Abgrenzung von Z 3, das Wahlrecht des Abs. 4 mit seinen Grenzen, E08 als Ebene D |
| Nachweis | `test_pruefpunkte_erreichen_den_oib_befund`, Messung Abschnitt 8 |

### 6.2 Vorhanden, aber **nicht aufgerufen**

| | |
|---|---|
| Artefakt | `normwissen/astv.py::ArbeitsstaettenWissen` — `pruefpunkte()`, `wahlrecht()`, `reichweite_vorbehalt()`, `ausfuehrung_e08()`, `betriebspflichten()`, `hinweise_fuer_ausgabe()` |
| Zustand | vollständig, getestet (27 Tests), **kein Konsument** — `test_kein_konsument_ruft_die_auskunft_auf` hält das sichtbar |
| Warum | die strukturierte Auskunft ist erst nützlich, wenn ein Konsument die **Antworten** des Projekts entgegennimmt; heute gäbe es nur `ungeprueft` zurück |
| Was fehlt zur Nutzung | ein Aufrufer in `hauptengine/validierung.py` (Prüfbericht) **oder** in `platzierung` — Naht, nicht Enis-Lane allein |

### 6.3 Fehlende Eingaben und Entscheidungen

| Fehlt | Art | bei wem |
|---|---|---|
| `natuerlich_belichtet` je Raum/Abschnitt (Z 1) | **Eingabe** (Erkennung) | @polatselman + 3 Owner |
| `belichtung_reicht_bei_ausfall` je Fluchtweg-Abschnitt (Z 2) | **Beurteilung** (Kontext/LB) | 3 Owner |
| Z-3-Bereich ja/nein | **Gefahrenbeurteilung** | 3 Owner |
| `orientierungshilfen_statt_sicherheitsbeleuchtung` (Abs. 4) | **Wahlrecht** (Planer/AG) | 3 Owner |
| Lage innerhalb/außerhalb der Arbeitsstätte, Mitbenutzung, überwiegende Wohnnutzung (§ 1 Abs. 2/3) | **Eingaben** | 3 Owner |
| Bezugsfläche + Aufgaben-/Allgemeinbeleuchtung (AS-9, 15 lx) | **Eingaben** | 3 Owner — bis dahin `arbeitsplatz_lux` leer |
| darf eine **Ebene-D-Empfehlung** (E08 Tabelle 1) platzieren? | **Entscheidung** | 3 Owner |

### 6.4 Benötigte Integration

1. **Aufrufer für `ArbeitsstaettenWissen`** — sinnvollster Ort: `validierung.pruefbericht`,
   je Gebäudeteil ein Befund „AStV-Pfad ungeprüft" mit der Liste der fehlenden Angaben.
   ⚠️ `validierung.py` gehört der Hauptengine → Abstimmung, nicht einseitig.
2. **Antwortweg für die Angaben** aus 6.3 — ohne sie bleibt jeder Aufruf bei `ungeprueft`.
3. **L2** (voller Prüfbericht über die API) — der Header trägt heute nur den
   `oib`-Block; Befunde aus `pruefung` erreichen den Client nicht.

---

## 7. Zwei kopierfertige Aufträge (vorbereitet, **nicht versendet**)

### 7.1 An Selmans Claude (@polatselman)

```text
Betreff: RaumModell — Feld `natuerlich_belichtet` für den AStV-Pfad (3-Owner-Contract)

Worum es geht
AStV § 9 Abs. 1 Z 1 verlangt eine Sicherheitsbeleuchtung für "Arbeitsräume und
Fluchtwege, die nicht natürlich belichtet sind". Das ist der einzige der drei
§-9-Tatbestände, der überhaupt aus dem Plan erkennbar ist — Z 2 und Z 3 sind
Beurteilungen und gehören in den ProjektKontext, nicht in die Erkennung.

Benötigte Eingabe
  Feld : natuerlich_belichtet: bool | None
  Ort  : RaumModell.Raum (und, wenn erkennbar, je Fluchtweg-Abschnitt)
  Default: None  — ausdrücklich NICHT False.

Fachliche Bedeutung
"Natürlich belichtet" heißt: der Raum hat Belichtungsflächen. Die OVE-Fachinfo
E08 (Ausgabe 2021-04-01, Abschnitt 3) nennt als Beispiele "Fenster oder
Lichtkuppeln". Das ist Ebene D (Auslegungshilfe), taugt aber als Merkmalsliste.

Herkunft der Angabe
  * aus dem Architekturplan erkennbar: Fensteröffnungen, Lichtkuppeln,
    Oberlichten in der Außenwand/Decke des Raums;
  * NICHT ableitbar aus Raumtyp, Lage im Geschoss oder Raumname. Ein Kellerraum
    kann belichtet sein, ein Innenraum im Erdgeschoss unbelichtet.

Umgang mit unbekannten Werten — das ist der Kern
  * None = "nicht erhoben". Die Engine führt den Prüfpunkt dann als `ungeprueft`
    und schreibt ihn in den Bericht. Das ist der gewünschte Zustand.
  * False darf NUR gesetzt werden, wenn tatsächlich festgestellt wurde, dass
    keine Belichtungsfläche vorhanden ist. False ist eine Tatsachenbehauptung,
    die eine Rechtsfolge auslöst (Z 1 erfüllt) — ein Default False wäre eine
    stille Behauptung über jedes Gebäude.
  * True verneint nur Z 1. Z 2 (Fluchtweg, dessen vorhandene Belichtung im
    Ausfallfall nicht ausreicht) bleibt davon unberührt und weiterhin offen.

Erwartetes Verhalten
  None  -> Prüfpunkt bleibt offen, erscheint im Bericht, Platzierung unverändert
  False -> Z-1-Tatbestand erfüllt: Erforderlichkeit AUSWEISEN, nicht platzieren
           (§ 9 nennt weder Beleuchtungsart noch Lux-Wert)
  True  -> Z 1 verneint, Z 2 bleibt offen
In allen drei Fällen ändert sich die Platzierung nicht.

Testfälle
  1. Raum mit Fensteröffnung in der Außenwand              -> True
  2. fensterloser Kellerraum                               -> False
  3. Raum ohne Belichtungsauswertung                       -> None
  4. Regression: für alle drei Fälle identische Platzierung (Symbolzahl,
     Positionen, norm_quelle) wie heute.

Warum ich es nicht selbst einbaue
RaumModell ist Contract (3 Owner) und die Erhebung liegt in deiner Lane. Fachliche
Herleitung: docs/proposals/ASTV_E08_ENTSCHEIDUNGSREGELN.md Abschnitt 2.2.
Bitte keine konkurrierende Modellierung entwerfen — falls du das Merkmal anders
schneiden willst (z. B. Fensterfläche in m² statt bool), sag es, bevor jemand
etwas baut; dann stimmen wir es gemeinsam ab.
```

### 7.2 An Leonis' Claude (@mvpo3)

```text
Betreff: AStV-Auswertung aufrufen + zwei ProjektKontext-Felder + E08-Prüfregel

Stand bei mir (alles lokal, nichts gepusht)
`normwissen/astv.py::ArbeitsstaettenWissen` ist fertig und getestet: sie sagt je
Gebäudeteil, welche AStV-§-9-Prüfpunkte offen sind und welche Angabe jeder
braucht. Sie entscheidet nichts und aktiviert nichts. Kurzfassung der drei
Tatbestände hängt bereits an den bestehenden AStV-Hinweisen und erreicht über
deinen gate_summary-Fix (#132) den X-Notbeleuchtung-Header.

1) Aufruf der Auswertung — die eigentliche Bitte
Heute ruft NIEMAND die Auswertung auf; sie ist Wissen auf Vorrat. Sinnvollster
Ort ist `hauptengine/validierung.py::pruefbericht`:

    from notbeleuchtung.normwissen.astv import ArbeitsstaettenWissen
    wissen = ArbeitsstaettenWissen()
    for teil in projekt.gebaeudeteile:
        for p in wissen.pruefpunkte(teil.arbeitsstaette_nach_aschg):
            befunde.append(Befund(
                f"AStV {p.fundstelle} — ungeprüft",
                "warnung",
                p.hinweis + " Benötigt: " + "; ".join(p.benoetigte_angabe),
            ))

Übergabe der Ergebnisse an bestehende Verbraucher
  * `pruefbericht` -> `render_summary["pruefung"]` (bestehender Weg)
  * der gezeichnete Prüfvermerk zählt Befunde bereits — die Zahl steigt, der
    Text am Blatt bleibt unverändert
  * ⚠️ `pruefung` steht NICHT in `_SUMMARY_HEADER_KEYS`; die Befunde erreichen
    den Client also erst mit L2. Bitte L2 dadurch nicht vorwegnehmen.

Fachliche Akzeptanzfälle
  A. Gebäudeteil arbeitsstaette_nach_aschg=True  -> 3 Befunde (Z 1, Z 2, Z 3),
     jeder mit Fundstelle und benötigter Angabe, Status "warnung"
  B. =None -> dieselben 3 Befunde, zusätzlich der Statusvorbehalt aus
     `reichweite_vorbehalt(None)`
  C. =False -> KEINE Prüfpunkte, aber der Reichweiten-Vorbehalt aus
     `reichweite_vorbehalt(False)` bleibt sichtbar (§ 1 Abs. 2 erfasst
     mitbenutzte Gebäudeteile außerhalb der Arbeitsstätte)
  D. Platzierung in A, B und C identisch zu heute — die Auswertung erzeugt
     ausschließlich Befunde
  E. kein ProjektKontext -> kein AStV-Befund, keine Ausnahme

2) Zwei ProjektKontext-Felder (3-Owner-Contract, Formulierung von mir)
  belichtung_reicht_bei_ausfall: bool | None       (Z 2, je Fluchtweg-Abschnitt)
  orientierungshilfen_statt_sicherheitsbeleuchtung: bool | None  (Abs. 4)
Beide dreiwertig, Default None. Fachlich: Z 2 ist eine Beurteilung ("bauliche
Gegebenheiten", "Lage der Arbeitszeit"), Abs. 4 ein Wahlrecht des Planers/AG.
Akzeptanzfall: Kontext mit Abs.-4-Wahl = True UND einem Z-3-Bereich -> die Wahl
darf NICHT als zulässig ausgegeben werden (Abs. 4 gilt nur ohne Z-3-Bereich und
nur abweichend von Z 1/Z 2; OVE E 8101, R 12-2 und OIB-RL 2 bleiben unberührt).

3) Prüfregel "mehr als 20 Sicherheitsleuchten"
Belegt auf ZWEI Ebenen: OVE E 8101:2019 Teil 5-56, 560.9.2 (Norm, Ebene C) —
"von einem Endstromkreis dürfen nicht mehr als 20 Leuchten mit einer
Gesamtbelastung von nicht mehr als 60 % des Nennstromes gespeist werden";
gleicher Wortlaut in der Ausgabe 2025. OVE-Fachinfo E08 Abschnitt 5.2 (Ebene D)
nennt zusätzlich ab >20 Leuchten je zusammenhängendem Gebäudeteil eine
automatische Prüfeinrichtung nach ÖVE/ÖNORM EN 62034.
  Eingabe : Leuchtenzahl je Gebäudeteil (liegt im PlatzierungsErgebnis)
  Wirkung : reiner Befund ("warnung"), keine Platzierungsänderung
  Grenze  : ⚠️ Die 20er-Grenze der Norm gilt JE ENDSTROMKREIS — die Engine führt
            keine Stromkreise. Der Befund darf deshalb nur sagen: "ab dieser
            Leuchtenzahl ist die Stromkreisaufteilung nachzuweisen", nicht
            "Grenze überschritten".
  Testfall: 21 Leuchten -> Befund; 20 -> kein Befund.

Nicht Gegenstand dieser Nachricht: L2, T1, Schriftfix/Layout. Fachliche
Herleitung: docs/proposals/ASTV_E08_ENTSCHEIDUNGSREGELN.md,
docs/audit/QUELLENVERARBEITUNG.md.
```

---

## 8. Korrektur zur Wirkung — der API-Header trägt den `oib`-Block

Der frühere Satz „DXF/API: nein → L2" war **zu pauschal**. Gemessen auf der
`origin/main`-Basis (`4c5df91`, echte Pipeline, Mollgasse KG):

| Kanal | Befund |
|---|---|
| **API-Header `X-Notbeleuchtung`** | ✅ **trägt die AStV-Hinweise** — `oib` steht in `_SUMMARY_HEADER_KEYS`, und `render_summary["oib"]["hinweise"]` enthält sie (`arbeitsstaette=True`: 10 Hinweise, davon 2 AStV) |
| **Sichtbarer Text auf dem Plan** | ❌ **nein** — das Blatt trägt nur die OIB-**Stufe**; Hinweise werden nicht gezeichnet |
| **Voller Prüfbericht** | ❌ **nein** — `pruefung` fehlt in `_SUMMARY_HEADER_KEYS`; beide Routen antworten mit `FileResponse`. **Das** ist L2 |

⚠️ **Neuer Befund aus derselben Messung — Header-Budget.** `gate_summary` stellt
jedem Provider-Hinweis `[gebaeudeteil]` voran und dedupliziert deshalb **nicht
über Gebäudeteile hinweg**; der `oib`-Block wächst linear mit ihrer Zahl, und
`json.dumps(..., ensure_ascii=True)` bläht jeden Umlaut auf sechs Zeichen.
Gemessen mit dem **ersten**, langen Prüfpunkt-Text (1 262 B):

| Gebäudeteile (alle Arbeitsstätte) | Header |
|---|---|
| 1 | 4 236 B |
| 2 | 7 151 B |
| 4 | **12 981 B — über der ~8-KB-Grenze von uvicorn** |
| 6 | **18 811 B** |

**Was in dieser Lane geändert wurde:** der Prüfpunkt-Text ist von 1 262 B auf
**661 B** gekürzt; der Langtext lebt in `astv_arbeitsstaetten.yaml` bzw.
`ArbeitsstaettenWissen`. Ein Guard (`test_hinweis_bleibt_im_header_budget`) hält
die Grenze. **Erneut gemessen, gleiche Bedingungen:**

| Gebäudeteile | vorher | nach der Kürzung |
|---|---|---|
| 1 | 4 236 B | **3 610 B** |
| 2 | 7 151 B | **5 899 B** |
| 4 | 12 981 B | **10 477 B — weiterhin über der Grenze** |
| 6 | 18 811 B | **15 055 B — weiterhin über der Grenze** |

⚠️ **Damit ist der Befund nicht erledigt, sondern nur entschärft.** Die Kürzung
spart rund **626 B je Gebäudeteil**; der Header sprengt die ~8-KB-Grenze jetzt ab
etwa **drei** Arbeitsstätten-Gebäudeteilen statt ab vier. Der Grund liegt tiefer:
schon **ohne** jeden AStV-Hinweis trägt der `oib`-Block rund **2 KB je
Gebäudeteil** (gemessen: 2 166 B bei einem Gebäudeteil mit
`arbeitsstaette_nach_aschg=False`), weil `gate_summary` jeden Hinweis je
Gebäudeteil mit `[id]`-Präfix wiederholt. **Das ist älter als dieser Block und
gehört zur L2-Entscheidung** (gekürzter Header gegen eigenen Endpunkt) —
hier ausdrücklich **nicht** angefasst, keine L2-Implementierung gestartet.
⚠️ Für @mvpo3 heißt das: die Wahl „Header kürzen" löst L2 nicht, solange der
`oib`-Block selbst linear mitwächst.

---

## 9. Korrekturen an den Aufträgen aus Abschnitt 7 (Stand 2026-09-08, zweite Runde)

Die Aufträge in Abschnitt 7 bleiben als Entwurf stehen; **maßgeblich sind die
Korrekturen hier**. Fünf Punkte waren zu ungenau oder falsch.

### 9.1 Fluchtwegbreiten — drei Größen statt einer

Mein Auftrag hatte für einen Abschnitt „die **engste** Stelle" verlangt. **Das ist
falsch:** die Engstelle lässt breitere Bereiche aus der Bewertung verschwinden —
und genau dort greift EN 1838 § 4.2.1 **Satz 3** (Streifenbetrachtung oder
Antipanik). Richtig sind **drei getrennte Größen**:

| Größe | Herkunft | wofür |
|---|---|---|
| **erforderliche Mindestbreite** | OIB-RL 4 Kap. 2, **Fertigmaß** | Vergleichsmaßstab eines Nachweises |
| **örtliche Engstelle** | Geometrie, schmalste Stelle | Prüfung gegen die Mindestbreite |
| **tatsächliche Breite entlang des Weges** | Geometrie, Verlauf | **einziger** Eingang der Lichtrechnung |

**Bei wechselnder Breite** ist entweder in **Abschnitte konstanter Breite** zu
teilen **oder** ein **Breitenprofil** je Abschnitt zu führen. Beide Wege müssen
die 2-m-Grenze dort erkennen, wo sie tatsächlich überschritten wird.

### 9.2 Türbreiten — Prüfung **zurückgezogen**, bis die Semantik geklärt ist

Am Code von `origin/main` geprüft: **`Tuer.breite_mm` trägt mindestens drei
Bedeutungen** — Nennmaß aus dem Blocknamen (`tueren.py::_breite_mm`: „TUER-80"
→ 800 mm), ein geometrisch abgeleitetes Maß (`tuer_zuordnung.py:155`) und
**`0.0` = keine Messung** (Öffnungs-Marker). RL 4 verlangt die **nutzbare
Durchgangslichte**, und die Vorbemerkungen halten fest: **„Alle … Maße verstehen
sich als Fertigmaße nach Vollendung der Bauführung."**

→ **Kein Prüfvorschlag mehr.** Ein Nennmaß gegen ein lichtes Fertigmaß zu prüfen
fiele systematisch zu günstig aus (Zarge und Blatt fehlen), und `0.0` würde als
Unterschreitung gelesen. Erst zu klären: welche Herkunft im Modell vorliegt, ob
eine belegte Umrechnung existiert, wie „keine Messung" unterschieden wird.

**Anwendungsbereich und Ausnahmen am Original ergänzt:** RL 4 gilt für Gebäude
(sonstige Bauwerke sinngemäß); **nicht** für eingeschossige, nicht barrierefreie
Gebäude ohne Wohnung ≤ 15 m² BGF; **Barrierefreiheits-Pflicht kommt aus dem
Landesrecht**, nicht aus RL 4; nach Landesrecht darf bei nachgewiesen gleichem
Schutzniveau abgewichen werden → ein Befund darf nur **„Anforderung nicht
nachgewiesen"** sagen, nie „unzulässig".

### 9.3 Natürliche Belichtung — Erkennungsvollständigkeit ist Teil der Angabe

Mein Auftrag ließ zu, aus „keine Fensteröffnung erkannt" ein `False` zu machen.
**Das ist bei unvollständiger Erkennung unzulässig.** Ergänzt:

* `False` **nur**, wenn die Fenster-/Öffnungserkennung für diesen Raum als
  **vollständig** gilt und dabei nichts gefunden wurde.
* Ist die Erkennung unvollständig, nicht gelaufen oder nicht bewertbar → **`None`**.
* Der Unterschied muss **im Modell erkennbar** sein, nicht nur im Kopf des
  Erkenners — sonst kann der Prüfbericht „nicht belichtet" und „nicht erhoben"
  nicht auseinanderhalten.

### 9.4 AStV — zwei globale Felder reichen nicht

Auch das war zu grob. § 9 knüpft an **drei verschiedene Bezugsobjekte** an:

| Tatbestand | Bezugsobjekt | heutiger Träger |
|---|---|---|
| Z 1 | **Raum** (Arbeitsraum) **und Fluchtweg-Abschnitt** | Raum: ja · Abschnitt: `FluchtwegSegment` |
| Z 2 | **nur Fluchtweg-Abschnitt** | `FluchtwegSegment` |
| Z 3 | **Bereich** — im Modell am ehesten der Raum | **eigenes Feld nötig** |
| Abs. 4 | Arbeitsräume/Fluchtwege **innerhalb der Arbeitsstätte** | Gebäudeteil + Zuordnung |
| § 1 Abs. 2/3 | **Gebäudeteil** + Lage des Raums dazu | `arbeitsstaette_nach_aschg` + Zuordnung |

**Erforderlich ist deshalb eine Zuordnung, kein Projektschalter.** Ohne geklärten
Geltungsbereich ist eine globale Angabe nicht auswertbar: sie ließe offen, für
welche Räume sie gilt. `Gebaeudeteil.raum_referenzen` existiert und ist der
naheliegende Träger — in den Realprojekten aber oft leer (der OIB-Pfad meldet
das bereits als eigenen Hinweis).

⚠️ **Z 3 braucht eine eigene Eingabe.** `Raum.besondere_gefaehrdung` trägt
EN 1838 § 4.4 (Lux auf der Arbeitsfläche) und wird **nicht** übernommen: das
Feld beantwortet eine andere Frage, und aus ihm eine Rechtsfolge abzuleiten wäre
eine stille Gleichsetzung. Ob ein Projekt beide Angaben gleich befüllt, ist seine
Entscheidung — nicht unsere Annahme.

### 9.5 Die zwei 20-Leuchten-Regeln — Anwendungsbereich belegt, Zählung offen

| | **(a) Endstromkreis** | **(b) Prüfeinrichtung** |
|---|---|---|
| Fundstelle | OVE E 8101 Teil 5-56 **560.9.2** (2019 **und** 2025) | OVE-Fachinfo **E08 5.2** |
| Ebene | **C** | **D** |
| Bezugsgröße | **je Endstromkreis** | **je zusammenhängendem Gebäudeteil** |
| heute prüfbar | **nein** — die Engine führt keine Stromkreise (`circuit_hint` ist Freitext) | **nein** — s. u. |

⚠️ **Die gebäudeteilbezogene Zählung ist heute nicht nachweisbar:**
`Platzierung` trägt **weder `raum_id` noch `gebaeudeteil_id`** (geprüft an
`origin/main` `4c5df91`), und `Gebaeudeteil.raum_referenzen` ist optional. Eine
Zählung „je Gebäudeteil" wäre geraten. Zusätzlich definiert E08 den Begriff
„zusammenhängend" nicht.

⚠️ **Wortlautgrenze für jeden künftigen Befund:** er darf sagen, dass ab dieser
Zahl eine automatische Prüfeinrichtung **vorzusehen** ist und dass die Engine
deren Vorhandensein **nicht kennt**. Er darf **nicht** behaupten, eine
Prüfeinrichtung **fehle** — das ist eine Anlagen-Tatsache außerhalb des Plans.

---

## 10. Der erste gemeinsam umsetzbare AStV-Integrationsschritt

**Kennzeichnung vorweg: dieser Schritt macht ausschließlich OFFENE PRÜFPUNKTE
SICHTBAR. Er wertet keine eingegebenen Antworten aus** — es gibt noch keine
Felder, in denen Antworten stehen könnten. Fehlende Angaben bleiben erkennbar,
weil jeder Befund die benötigte Angabe mitführt.

| Stufe | konkret |
|---|---|
| **Projektangabe** | `ProjektKontext.gebaeudeteile[*].arbeitsstaette_nach_aschg` — **existiert bereits**, dreiwertig |
| **Normauswertung** | `normwissen.astv.ArbeitsstaettenWissen.pruefpunkte(angabe)` + `.reichweite_vorbehalt(angabe)` — vorhanden, lazy, ohne Contract-Bezug |
| **Ergebnis** | je Gebäudeteil 3 `AstvPruefpunkt` (Z 1, Z 2, Z 3) mit `fundstelle`, `hinweis`, `benoetigte_angabe`, `status="ungeprueft"`; bei `False` **keine** Prüfpunkte, aber der längere Reichweiten-Vorbehalt |
| **Tatsächlicher Aufrufer** | `hauptengine/validierung.py::pruefbericht` — **gemeinsame Naht, Umsetzung bei @mvpo3** |
| **Überprüfbare Ausgabe** | drei zusätzliche `Befund`-Einträge (`status="warnung"`) in `render_summary["pruefung"]["befunde"]`; die Zählung im gezeichneten Prüfvermerk steigt entsprechend. ⚠️ Über die API sichtbar erst mit **L2** (`pruefung` fehlt in `_SUMMARY_HEADER_KEYS`) — **kein Teil dieses Schritts** |

**Warum dieser Schnitt zuerst:** er braucht **keinen Contract**, keine neue
Eingabe und keine Entscheidung über Bedeutung — nur einen Aufruf. Er macht die
Lücke sichtbar, statt sie zu füllen, und ist damit die Voraussetzung dafür, dass
die späteren Felder (9.3, 9.4) überhaupt einen Ort haben, an dem sie wirken.

**Akzeptanzfälle** siehe Auftrag B unten (A–E). **Abgrenzung:** dieser Schritt
ändert keine Platzierung, keine Stufe, keinen Contract und keinen Header.

---

## 11. Nachtrag 2026-09-08 (3) — die 20-Leuchten-Prüfeinrichtung ist normativ, und sie hat bereits einen Verbraucher

Zwei eigene Aussagen aus Abschnitt 9.5 waren **falsch**. Beide sind am Original
beider OVE-E-8101-Ausgaben nachgeprüft.

### 11.1 Korrektur 1 — die Fundstelle

| | frühere Aussage | **belegt** |
|---|---|---|
| Prüfeinrichtung | „für (b) ist E08 die einzige vorliegende Quelle, und sie ist Ebene D" | **OVE E 8101 Teil 5-56, 560.9.001.AT — Ebene C, in Ausgabe 2019-01-01 UND 2025-10-01 wortgleich.** E08 5.2 **wiederholt** sie |

**Wortlaut (beide Ausgaben):** „Bei mehr als 20 Sicherheitsleuchten in einem
zusammenhängenden Gebäudeteil ist eine automatische Prüfeinrichtung mit zentraler
Erfassung/Registrierung gemäß ÖVE/ÖNORM EN 62034 vorzusehen."

**Die drei Aussagen nebeneinander:**

| | **560.9.2** | **560.9.001.AT** | **E08 5.2** |
|---|---|---|---|
| Ausgabe | 2019 **und** 2025 | 2019 **und** 2025 | 2021-04-01 |
| Ebene | **C** | **C** | **D** (Wiederholung) |
| Bezugseinheit | **Endstromkreis** | **zusammenhängender Gebäudeteil** | dito |
| gezählt wird | Leuchten **eines Endstromkreises** | **Sicherheitsleuchten** im Gebäudeteil | dito |
| Rechtsfolge | Bemessungsgrenze (≤ 20, ≤ 60 % Nennstrom) | **Prüfeinrichtung nach EN 62034 vorzusehen** | dito |

**Unterschiede 2019 ↔ 2025 nur in den Unterpunkten:** 2019 b) „zyklische
Überwachung … der angeschlossenen Verbraucher", Prüfdauer **zwischen 0,5 und
5 min**; 2025 b) auf die **Sicherheitsleuchten** umformuliert, Prüfdauer
**höchstens 5 min** (keine Untergrenze); 2025 a) auf **Batterieanlagen**
präzisiert; 2025 c) **Überwachung des Übertragungsweges** samt Anzeige-, Melde-
und Protokollpflicht statt bloßer Fehlermeldung.

⚠️ **Grenze im Original:** „**zusammenhängender Gebäudeteil**" ist **nicht
definiert** — im Volltext 2025 kommt der Ausdruck nur an dieser einen Stelle vor,
Teil 2 „Begriffe" führt ihn nicht, und E08 definiert ihn ebenfalls nicht. Die
Bezugseinheit bleibt quellenseitig offen.
⚠️ **Nebenfundstelle 2025:** in der Legende zu den Bildern der Nationalen
Ergänzung **710.NE2** (Teil 7-710, medizinisch genutzte Bereiche) erscheint
560.9.001.AT als Zeile 13, daneben Zeile 12 „Sicherheitsbeleuchtung gemäß 560.9
(mehr als 20 Sicherheitsleuchten …)". Das ist ein **Verweis in einer Bildlegende**,
keine zweite Anforderung.

### 11.2 Korrektur 2 — es gibt bereits einen Verbraucher

`hauptengine/pipeline.py::_coverage` trägt seit Längerem
`_AUTO_PRUEF_SCHWELLE = 20` und hängt ab **> 20 Platzierungen** einen
nicht-blockierenden Hinweis an, der **dieselbe Fundstelle** nennt
(`OVE E 8101 560.9.001.AT / EN 62034`). Meine Aussage „von 65 Quelldateien wirken
nur die OIB-RL-2-Familie und ein Hinweistext" war deshalb **unvollständig**.

**Die Quelle stimmt. Offen ist die Anwendung:**

| Punkt | Norm | Engine heute |
|---|---|---|
| gezählte Objekte | **Sicherheitsleuchten** | `len(platzierung.platzierungen)` — **alle** Platzierungen, inkl. Rettungszeichen |
| Bezugseinheit | **zusammenhängender Gebäudeteil** (undefiniert) | **ein Geschoss** (der Lauf ist geschossweise) |
| Formulierung | „ist … **vorzusehen**" | „… **erforderlich**" |

* **Rettungszeichen mitzuzählen ist vertretbar** — E08 Abschnitt 2: „Eine
  Sicherheitsleuchte kann mit oder ohne Sicherheitszeichen ausgeführt sein" —
  aber nicht ausdrücklich belegt.
* **Die Bezugseinheit Geschoss steht in keiner der drei Quellen.** Ein Gebäudeteil
  kann mehrere Geschosse umfassen (die Engine zählt dann zu wenig), ein Geschoss
  mehrere Gebäudeteile (dann zu viel).
* Der Text darf **nicht** behaupten, eine Prüfeinrichtung fehle.

**Einstufung: vorläufiger Hinweis.** ⚠️ Ein erläuternder Halbsatz macht aus der
Geschosszählung **keinen belastbaren Nachweis** — die Bezugseinheit der Norm
bleibt ungezählt. Solange sie ungeklärt ist, folgt aus der Geschosszahl **weder
eine abschließende Pflicht** (> 20 im Geschoss beweist nichts über den
Gebäudeteil) **noch eine Entwarnung** (≤ 20 im Geschoss schließt einen größeren
Gebäudeteil nicht aus).

⚠️ **Und es fehlt keine Quelle, sondern zwei Projektangaben:**
1. die **fachliche Abgrenzung**, welche Bereiche einen zusammenhängenden
   Gebäudeteil bilden — Festlegung des Brandschutzkonzepts bzw. des Planers;
2. die **Zuordnung Leuchte → Gebäudeteil** (heute trägt `Platzierung` weder
   `raum_id` noch `gebaeudeteil_id`).
Dazu die Klärung, ob Rettungszeichenleuchten mitzählen.

**Vorschlag (Leonis' Datei, keine einseitige Änderung):** den vorhandenen Hinweis
**behalten und als vorläufig kennzeichnen** — Fundstelle richtig, nicht
blockierend, und der einzige Ort, an dem die Anforderung heute sichtbar wird. Er
sollte sagen, **was gezählt wurde**, dass die **Norm eine andere Bezugseinheit**
meint und **welche zwei Angaben** für einen belastbaren Befund fehlen.
**Von Enis kommt keine zweite Regel daneben.**

