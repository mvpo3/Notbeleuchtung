# Blocker 2 — Scope-Gate der Flächen-Schwellen, je Schwelle getrennt

> Enis (@EnisAMG), 2026-09-05. **Reine Analyse.** Beide Schwellen bleiben leer,
> kein Contract geändert, nichts aktiviert. Stand: `origin/main` = `5e4a46e`.

## 1. Quellen — am Original geprüft

| Ausgabe | Fundstelle | im Repo |
|---|---|---|
| **OVE E 8101:2019-01-01** | 718.560.9.001.AT, Teil 7-718 Seite 4 (PDF-S. 678) | `knowledge/OVE E 8101_2019 (1).pdf` — **Original geprüft** |
| **OVE E 8101:2025-10-01** | 718.560.9.001.AT, Teil 7-718 Seite 4 (PDF-S. 746), dort als „Füge hinzu:" | `knowledge/OVE E8101_2025 (1).pdf` — **Original geprüft** |
| **ÖVE/ÖNORM E 8002-1, Ausgabe 2007-10-01** | 3.2.2.1.2 „Antipanikbeleuchtung" | **nur Textextraktion**, kein Original im Repo → Aussagen dazu bleiben ungeprüft |

### 1a. Normtext (wörtlich, OVE E 8101:2019 = :2025 bis auf eine Wortänderung)

> **718.560.9.001.AT** Für **Räume, Anlagen oder Gebäude**, an die erhöhte
> Anforderungen nach der Art der Nutzung (siehe OVE-Richtlinie R 12-2 bzw.
> OIB-Richtlinie 2) gestellt werden, ist in folgenden Bereichen zusätzlich eine
> Sicherheitsbeleuchtung erforderlich:
>
> 1) bei Fahrtreppen, **in Sanitärbereichen ab 8 m² Größe** und **in
>    barrierefreien WC-Anlagen**;
> 2) in Räumen für Sicherheits- und Ersatzstromaggregate … (hier nicht relevant)
> 3) **in verkehrstechnischen Einrichtungen wie zB Flughäfen und Bahnhöfen** ist
>    **zusätzlich** zu den Einrichtungen gemäß 1) und 2):
>    – in Wartezonen, Abfertigungshallen, **Geschäftsflächen über 60 m²**,
>    – in **Arbeitsräumen und Räumen über 60 m² Fläche, die zur Aufrechterhaltung
>      des Betriebes notwendig sind**,
>    eine Sicherheitsbeleuchtung (**Antipanikbeleuchtung**) zu errichten.

**Einzige Änderung 2019 → 2025 an dieser Stelle:** in Punkt 1) heißt es statt
„in barrierefreien WC-Anlagen" jetzt „in **WC-Anlagen für Menschen mit
Behinderung**". Die Schwellen 8 m² und 60 m² sind unverändert.

### 1b. ANMERKUNG (informativ) — ÖVE/ÖNORM E 8002-1 3.2.2.1.2

Der Abschnitt ist eine **Begriffsbestimmung** („Antipanikbeleuchtung"), die
60 m² stehen in ihrer **ANMERKUNG**:

> ANMERKUNG … Sie wird bei **Bereichen ohne festgelegte Rettungswege** in Hallen
> oder baulichen Anlagen mit einer Fläche **größer 60 m²** angewendet **oder bei
> kleineren Flächen, sofern dort durch eine größere Menschenansammlung ein
> erhöhtes Risiko besteht**.

Drei Relativierungen in einem Satz: informativ (ANMERKUNG in einer Definition) ·
gebunden an „Bereiche **ohne festgelegte Rettungswege**" · nach unten offen
(kleinere Flächen bei Menschenansammlung). **Nicht am Original geprüft** — das
PDF fehlt im Repo.

### 1c. Was davon Auslegung ist (meine, nicht die Norm)

* ~~Dass „erhöhte Anforderungen nach der Art der Nutzung" **durch den OIB-Pfad
  beantwortbar** sind — die Norm verweist auf R 12-2 **bzw.** OIB-RL 2; wir werten
  nur OIB-RL 2 aus. R 12-2 liegt nicht vor.~~ **Am 05.09. für Zeile 4
  (Verkaufs-/Ausstellungsstätten) belegt** — siehe Abschnitt 9. Für alle anderen
  Nutzungen bleibt die Aussage bestehen.
* Dass eine OIB-Stufe `eingeschraenkt`/`uneingeschraenkt` gleichbedeutend mit
  „erhöhte Anforderungen" ist.
* Die Zuordnung unserer Raumtypen (`WC`, `SANITAER`, …) zu „Sanitärbereich".

## 2. Geltungsbereiche, getrennt

| | **8 m²** | **60 m²** |
|---|---|---|
| Fundstelle | 718.560.9.001.AT **1)** | 718.560.9.001.AT **3)** |
| Verbindlichkeit | normativ | normativ |
| Nutzungsart | jede mit „erhöhten Anforderungen" (R 12-2 / OIB-RL 2) | **nur** verkehrstechnische Einrichtungen (Flughäfen, Bahnhöfe) |
| räumlicher Bezug | **Sanitärbereich** ab 8 m²; **zusätzlich** barrierefreie WC-Anlagen **ohne Flächenmaß** | nur bestimmte **Raumkategorien**: Wartezonen, Abfertigungshallen, Geschäftsflächen > 60 m², Arbeitsräume/Räume > 60 m² **die zur Aufrechterhaltung des Betriebes notwendig sind** |
| Bezugseinheit | **Raum, Anlage oder Gebäude** — nicht das Projekt | dito |
| Lichtart | „Sicherheitsbeleuchtung" (Art nicht spezifiziert) | ausdrücklich **Antipanikbeleuchtung** |

**Folge 1:** `wc_sanitaer_min_m2` bildet Punkt 1) nur zur Hälfte ab — die
barrierefreie WC-Anlage **ohne** Flächenmaß fehlt im Schwellen-Pfad.

> **Korrektur 05.09. (am laufenden Code geprüft).** Die frühere Formulierung „ein
> 4 m² großes barrierefreies WC fällt durch jedes Schwellenraster" war
> missverständlich. Mit echtem Provider und vollem Platzierungspfad:
>
> | Fall | Ergebnis |
> |---|---|
> | barrierefreies WC, 4 m² | **1 Antipanik-Leuchte**, `norm_quelle = ÖNORM EN 1838:2013 §4.3.1` |
> | gewöhnliches WC, 4 m² | keine Leuchte |
>
> Es sind **zwei verschiedene Auslöser**, und nur einer fehlt:
>
> * **greift bereits:** EN 1838 **§4.3.8** über `Raum.ist_barrierefrei` →
>   `sonderstellen_strategy.plan_flag_raeume` — flächenunabhängig, auf `main`.
>   Ein barrierefreies WC bekommt also Licht, unabhängig von jeder Schwelle und
>   vom OVE-Scope.
> * **fehlt:** der OVE-Auslöser aus Punkt 1) zweiter Halbsatz im
>   **Schwellen-Pfad** (`_ist_sanitaer_schwelle`). Er ist keine Schwelle und
>   gehört nicht in `wc_sanitaer_min_m2`.
>
> Die Lücke betrifft damit die **Vollständigkeit des Audit-Trails**, nicht eine
> fehlende Leuchte.
**Folge 2:** `antipanik_min_m2` als reine Flächenzahl bildet Punkt 3) **nicht**
ab: dort hängt die Pflicht an der Raumkategorie, nicht an der Fläche allein.

## 3. Datenfluss und wo er sich weitet

```
ProjektKontext.gebaeudeteile[]            je Teil: nutzungsart, Kennzahlen, raum_referenzen[]
  └─ OibRl2Provider.bewerte_oib()         → OibBefund.ergebnisse[] je GEBÄUDETEIL (stufe)
      └─ oib_gate.flaechen_trigger_offen()  ⚠️ ODER über alle Teile → EIN Boolean fürs Projekt
      └─ oib_gate.freigegebene_raeume()     ⚠️ fällt auf „alle Räume" zurück
          └─ flaechen_strategy._plan_raumleuchten()  wendet BEIDE Schwellen mit demselben Gate an
              └─ pipeline.render_summary["oib"] → api `_SUMMARY_HEADER_KEYS`
```

**Weitung 1 — `flaechen_trigger_offen` (`platzierung/oib_gate.py`)**

```python
def flaechen_trigger_offen(oib):
    return bool(_bestaetigende(oib))      # ein bestätigender Teil genügt fürs ganze Projekt
```

Ein einziger bestätigter Gebäudeteil öffnet das Gate **für alle Räume aller
Geschosse** — obwohl der Normsatz an „Räume, Anlagen oder Gebäude" anknüpft.

**Weitung 2 — `freigegebene_raeume`**

```python
if not bestaetigend or any(not e.raum_referenzen for e in bestaetigend):
    return None                            # None = keine Einschränkung = alle Räume
```

Fehlt **einem** bestätigenden Teil die Raumzuordnung, gilt das offene Gate wieder
projektweit. Als konservative Auslegung nachvollziehbar — für eine
Pflicht-Auslösung ist sie zu weit.

**Weitung 3 — eine Entscheidung für zwei Schwellen**

```python
ap_referenz = _antipanik_referenz(norm) if klassifikation == "antipanik" and flaechen_trigger_offen(oib) else None
...
if ap is not None and flaeche_m2 >= ap: return True
return wc is not None and raum_typ.upper() in _WC_TYPEN and flaeche_m2 >= wc
```

`_ist_flaechen_antipanik` prüft beide Schwellen hinter **demselben** Gate,
obwohl ihre Nutzungsart-Scopes verschieden sind.

**Fehlende Angaben im Datenfluss:** je Raum fehlt die Zugehörigkeit zu einem
Gebäudeteil (nur die Rückrichtung `Gebaeudeteil.raum_referenzen` existiert, und
sie ist optional); für Punkt 3) fehlt jede **Raumkategorie**
(Wartezone / Abfertigungshalle / Geschäftsfläche / betriebsnotwendiger
Arbeitsraum); für Punkt 1) fehlt das Merkmal **barrierefreie WC-Anlage** als
eigener, flächenunabhängiger Auslöser (`Raum.ist_barrierefrei` existiert seit
#93 — es ist heute nicht mit dem OVE-Trigger verbunden).

## 4. Reproduktionen (lokal, `5e4a46e`, Schwellen im Fake auf 60/8 gesetzt)

Drei Räume im EG: `wc_verkauf` (WC, 9 m²), `wc_wohnen` (WC, 9 m²),
`halle` (80 m²).

| # | Szenario | Stufen | Gate | Raum-Scope | erzeugte Antipanik-Leuchten |
|---|---|---|---|---|---|
| A | Verkauf + Wohnen, **beide mit** `raum_referenzen` | verkauf `eingeschraenkt`, wohnen `review_required` | offen | `{wc_verkauf}` | **4** — korrekt |
| B | Verkauf + Wohnen, **ohne** `raum_referenzen` | dieselben | offen | **alle** | **12** — auch `wc_wohnen` (unbestätigter Teil) und `halle` |
| C | **nur Bahnhof** | `review_required` | **zu** | — | **0** — der einzige Fall, für den die 60 m² belegt sind, feuert nicht |
| D | Bahnhof + Verkaufsstätte | bahnhof `review_required`, verkauf `eingeschraenkt` | offen | alle | **12** — die 80-m²-Halle feuert wegen des **Verkaufs**teils, nicht wegen des Bahnhofs |
| E | Verkaufsstätte **ohne Kennzahlen** | `review_required` | zu | — | **0** |

Zwei Befunde daraus:

* **B und D wenden die Pflicht auf Räume an, für die kein bestätigter
  Geltungsbereich vorliegt.** In D kommt hinzu, dass die 60-m²-Regel ausgelöst
  wird, obwohl der bestätigende Teil **kein** Verkehrsbauwerk ist — und die Halle
  keiner der in Punkt 3) genannten Raumkategorien zugeordnet ist.
* **C ist die Umkehrung:** Verkehrseinrichtungen haben in OIB-RL 2 Tabelle 6
  keine Zeile (Bundeszuständigkeit) → `review_required` → Gate zu. Für den
  einzigen normativ belegten 60-m²-Fall ist das Gate **gesperrt**.

**Sichtbarkeit:** `gate_summary` ergänzt einen `review_required`-Hinweis **nur,
wenn das Gate zu ist**. In B und D — Gate offen, ein Teil unbestätigt — steht
davon nichts; der Hinweis lautet nur „projekt-global". Und der Gate-Zustand
erscheint ausschließlich in `render_summary["oib"]` (API-Header), **nicht im
Prüfbericht** (`grep -n "oib" hauptengine/validierung.py` → leer). Ein unklarer
Geltungsbereich wird damit weder als erfüllt noch als nicht erforderlich
ausgewiesen — er ist im Plan schlicht unsichtbar.

## 5. Bewertung je Schwelle — was reicht, was fehlt

### 8 m² (Sanitärbereiche) — nah dran, zwei Lücken

**Reicht bereits:** `Gebaeudeteil.nutzungsart` + Kennzahlen → OIB-Stufe;
`Gebaeudeteil.raum_referenzen` → Raum-Zuordnung; `Raum.raum_typ`,
`Raum.flaeche_m2`; `Raum.ist_barrierefrei` (seit #93).

**Fehlt:**
1. Ein Gate, das **je Raum** entscheidet und nicht auf „alle Räume" zurückfällt,
   wenn ein Teil keine Zuordnung trägt (Weitung 1 + 2).
2. Der **flächenunabhängige** Trigger „barrierefreie WC-Anlage" (Punkt 1, zweiter
   Halbsatz) — er ist keine Schwelle und passt deshalb nicht in
   `wc_sanitaer_min_m2`.

**Beides ist ohne Contract-Änderung erreichbar** (siehe 6). **Aber:** ein
korrektes raumbezogenes Gate macht den *Nutzungs*-Scope noch nicht belegt —
siehe den Vorbehalt in Abschnitt 8.

### 60 m² (Verkehrseinrichtungen) — weiter weg

**Reicht bereits:** nichts Entscheidendes.

**Fehlt:**
1. Ein Signal „Gebäudeteil ist **verkehrstechnische Einrichtung**". Die Angabe
   existiert (`Nutzungsart.VERKEHRSEINRICHTUNG`), erreicht den Konsumenten aber
   nur als `OibErgebnis.eingangswerte["nutzungsart"]` — ein Audit-Dict, kein
   verlässliches Feld.
2. Die **Raumkategorie** (Wartezone, Abfertigungshalle, Geschäftsfläche,
   betriebsnotwendiger Arbeitsraum). Ohne sie ist Punkt 3) nicht abbildbar — eine
   reine Flächenzahl trifft ihn nicht.
3. Eine Entscheidung, wie mit `review_required` für Verkehrseinrichtungen
   umzugehen ist (Tabelle 6 hat dafür keine Zeile).

**Die 8-m²-Lösung darf daran nicht hängen.** Punkt 1) und Punkt 3) sind im
Normtext getrennte Aufzählungspunkte mit verschiedenen Nutzungs-Scopes; die
Kopplung existiert nur in unserem Code.

## 6. Umsetzungsvorschlag

### 6a. Innerhalb der bestehenden Schnittstellen möglich

| Schritt | Ort | Lane |
|---|---|---|
| `flaechen_trigger_offen` / `freigegebene_raeume` durch **eine raumbezogene Frage** ersetzen: „ist DIESER Raum von einem bestätigenden Gebäudeteil erfasst?" Ohne Zuordnung → **nicht** erfasst (statt „alle") | `platzierung/oib_gate.py` | @mvpo3 |
| Beide Schwellen **getrennt** gaten: `_ist_flaechen_antipanik` bekommt zwei Signale statt einem | `platzierung/flaechen_strategy.py` | @mvpo3 |
| Prüfregel: bestätigender Gebäudeteil **ohne** `raum_referenzen` → Warnung „Geltungsbereich nicht raumgenau bestimmbar"; `review_required` → Warnung, **auch wenn** das Gate anderweitig offen ist | `hauptengine/validierung.py` | Integration |
| `barrierefreie WC-Anlage` als eigener, flächenunabhängiger Auslöser in meiner Regel-/Datenlage abbilden | `normwissen/data/*` | @EnisAMG |
| Nutzungsart-Signal aus `eingangswerte["nutzungsart"]` **lesen** statt raten | `platzierung/oib_gate.py` | @mvpo3 (Notlösung, siehe 6b) |

### 6b. Braucht eine 3-Owner-Erweiterung

| Was | Warum |
|---|---|
| `OibErgebnis.nutzungsart: Nutzungsart \| None` (oder ein boolesches `ist_verkehrstechnische_einrichtung`) | die Nutzungsart ist heute nur Audit-Dict; für eine Pflicht-Auslösung braucht es ein zugesichertes Feld |
| `Raum.nutzungskategorie` o.ä. für Wartezone / Abfertigungshalle / Geschäftsfläche / betriebsnotwendiger Arbeitsraum | ohne sie ist Punkt 3) nicht abbildbar |
| ggf. `FlaechenSchwellen` je Scope trennen statt zwei nackte Zahlen in einem Objekt | macht die unterschiedlichen Geltungsbereiche im Contract sichtbar |

### 6c. Reihenfolge

1. **Zuerst 6a**, Zeile 1–3: das behebt die Über-Anwendung (B/D) und macht den
   unklaren Fall sichtbar — ohne jede Contract-Änderung und ohne dass eine
   Schwelle gefüllt sein muss.
2. **Dann die 8 m²** — aber erst, wenn zusätzlich zum raumbezogenen Gate der
   Bedeutungs-Vorbehalt aus Abschnitt 8 ausgeräumt ist (die Gleichsetzung
   „Tabelle-6-Erforderlichkeit = erhöhte Anforderungen nach der Art der Nutzung"
   ist bislang Auslegung). Dazu der flächenunabhängige Barrierefrei-Trigger.
3. **Die 60 m²** bleiben, bis 6b entschieden ist. Sie sind der kleinere Nutzen
   (nur Flughäfen/Bahnhöfe) und der größere Aufwand.

## 7. Status

Beide Felder bleiben **leer**, `engine_status` unverändert, kein Contract
angefasst. Diese Datei ist Analyse und Vorschlag — nichts davon ist umgesetzt.


---

## 8. Nachtrag 05.09. — Umsetzung von 6a.1–3, und was sie NICHT leistet

Umgesetzt (lokal, Branch `enis/blocker2-scope-analyse-0905`): Scope je Raum
(`sanitaer_scope` / `verkehr_scope` mit `anwendbar | nicht_anwendbar |
ungeklaert`), getrennte Schwellen-Auswertung, Prüfregel 13.

### 8a. Bedeutungs-Vorbehalt — der Nutzungs-Scope bleibt angenähert

Die entscheidende Frage: **welcher OIB-Befund begründet eigentlich
`sanitaer_scope = anwendbar`?**

`OibRl2Provider` beantwortet **OIB-RL 2 Punkt 5.4 / Tabelle 6**: „Für die in der
Tabelle 6 angeführten Nutzungen ist eine entsprechende Sicherheitsbeleuchtung
gemäß dieser Tabelle zu errichten." Die Stufen bedeuten laut den Erläuterungen
(Erl.-S. 48, in `oib_rl2_tabelle6.yaml` hinterlegt):

* `eingeschraenkt` — „Sicherheitsbeleuchtung für **Fluchtwege** gemäß ÖNORM
  EN 1838 sowie ÖVE/ÖNORM EN 50172";
* `uneingeschraenkt` — dasselbe, „**NICHT auf Fluchtwege eingeschränkt**".

Die OVE-Klausel fragt nach etwas anderem: nach **„erhöhten Anforderungen nach der
Art der Nutzung (siehe OVE-Richtlinie **R 12-2** bzw. OIB-Richtlinie 2)"**.

**Das ist nicht dasselbe, und die Gleichsetzung ist nicht belegt:**

* **R 12-2 liegt nicht im Repo.** Die Klausel nennt sie zuerst; wir können nur den
  OIB-Zweig auswerten.
* Die OIB-Erläuterungen verweisen ihrerseits auf „OVE-Richtlinie R 12-2 Punkte 3,
  4 und 5.1 bis 5.3" nur **„je nach Zutreffen"** — also selbst bedingt.
* Tabelle 6 sagt „Sicherheitsbeleuchtung **erforderlich**", nicht „erhöhte
  Anforderungen **nach der Art der Nutzung**".

**Konsequenz im Code (umgesetzt):** die beiden Fragen sind getrennt.

| Funktion | Frage | Werte |
|---|---|---|
| `raum_zuordnung` | *räumlich:* erfasst ein Gebäudeteil mit positivem OIB-Befund diesen Raum? | `bestaetigt` · `nicht_bestaetigt` · `ungeklaert` |
| `sanitaer_scope` | *fachlich:* ist die OVE-Sanitärregel hier anwendbar? | `ungeklaert` (bewertet) · `nicht_bewertet` (kein OIB-Pfad) — **weder `anwendbar` noch `nicht_anwendbar`** |

**Beide Richtungen sind begründungspflichtig.**

* `anwendbar` bräuchte den Beleg, dass der Raum zu „Räumen … mit erhöhten
  Anforderungen **nach der Art der Nutzung**" gehört. Tabelle 6 belegt das nicht.
* `nicht_anwendbar` bräuchte den Beleg, dass die OVE-Regel hier **nachweislich
  nicht** gilt. Weder ein fehlender noch ein negativer OIB-Befund leistet das: die
  Klausel nennt **R 12-2 bzw. OIB-RL 2**, und „nach Tabelle 6 nicht erforderlich"
  schließt den R-12-2-Zweig nicht aus.
* `nicht_bewertet` (kein ProjektKontext) ist eine Aussage über den **Vorgang**,
  nicht über die Sache — sie darf in der Ausgabe nicht als Nicht-Erforderlichkeit
  erscheinen.

Auch eine im Test gesetzte 8-m²-Schwelle löst damit **keine** Platzierung aus.
Der Satz „der Scope stimmt jetzt" wäre falsch; richtig ist: *die Über-Anwendung
über Gebäudeteile hinweg ist behoben, und die verbleibende Unsicherheit wird
benannt statt in eine der beiden Richtungen aufgelöst.*

### Was nötig wäre, damit daraus `anwendbar` wird

Zwei **verschiedene** Dinge, die nicht gegeneinander eingetauscht werden können:

1. **Fachlich:** ein Quellenbeleg **mit Ausgabestand**, der die Gleichsetzung
   trägt — **OVE-Richtlinie R 12-2** in der zutreffenden Ausgabe, oder eine
   andere belegte Fundstelle, die „Tabelle-6-Erforderlichkeit" und „erhöhte
   Anforderungen nach der Art der Nutzung" verbindet. Das ist die eigentliche
   Voraussetzung.
2. **Organisatorisch:** eine 3-Owner-Freigabe für **Schnittstelle und Umsetzung**
   (Contract-Felder, Ports, Konsumption).

Punkt 2 ersetzt Punkt 1 nicht. Eine Freigabe entscheidet, *wie* etwas gebaut
wird — nicht, *ob* die Norm es hergibt. Und **„es gäbe weniger Warnungen" ist
keine Begründung**: die Warnungen sind die Folge der fehlenden Quelle, nicht ihre
Ursache.

### 8b. Widersprüche und ungültige Zuordnungen

* Ist derselbe Raum mehreren Gebäudeteilen mit **gegenläufigen** Aussagen
  zugeordnet, ist das Ergebnis `ungeklaert` — ein bestätigender Teil überstimmt
  einen ungeklärten oder verneinenden **nicht**. Gruppiert wird nach
  Aussage-Richtung: `eingeschraenkt` + `uneingeschraenkt` sind kein Widerspruch.
* Eine **Referenz auf einen nicht vorhandenen Raum** gibt nichts frei und wird als
  Datenfehler ausgewiesen (`unbekannte_raum_referenzen`, Hinweis + Summary-Feld).
  `OibBefund.nicht_zugeordnete_raum_referenzen` taugt dafür nicht: der Provider
  bekommt kein `RaumModell` und lässt das Feld bewusst leer.

### 8c. Sichtbarkeit bis zur Ausgabe — nachgewiesen

Ende-zu-Ende über `pipeline.run(out_path=…)` geprüft: Regel 13 steht als
`[WARNUNG] OVE-Flächen-Trigger: Geltungsbereich ungeklärt …` im **gezeichneten
Prüfbericht** des DXF-Plans, und der Gesamtstatus des Berichts kippt auf
`WARNUNG`.

**Was der `gate_summary`-Umbau an der Ausgabe ändert:** das Feld
`flaechen_trigger_gate` **entfällt** (es beschrieb ein Projekt-Gate, das es nicht
mehr gibt); neu sind `sanitaer_scope`, `verkehr_scope` und
`unbekannte_raum_referenzen`. Bekannte Verbraucher: der
`X-Notbeleuchtung`-Header (`_SUMMARY_HEADER_KEYS` enthält `oib`) und die Tests —
beide angepasst.

**Dokumentierte Grenze:** der Prüfbericht selbst steht **nicht** im Header;
Regel 13 erreicht den Client über den gezeichneten Plan.

### 8d. Zusammenspiel mit PR #109

Isolierte lokale Merge-Probe (`28b7740` + `f4ffd84`, Wegwerf-Branch, danach
gelöscht, veröffentlichte Branches unberührt): **konfliktfreier Auto-Merge**,
**684 passed**. Alle vier Prüfregeln stehen nebeneinander und feuern im selben
Lauf:

```
[warnung] Sonderstellen 5-lx-vertikal-Nachweis (EN 1838 §4.1.2 h/i)
[warnung] Arbeitsplatz-Lux bei besonderer Gefährdung (§4.4.1, Bezugsfläche ARBEITSFLÄCHE)
[warnung] Barrierefreier Sanitärraum — Toilettennutzung nicht bestimmbar (§4.3.8)
[warnung] OVE-Flächen-Trigger: Geltungsbereich ungeklärt (OVE E 8101 718.560.9.001.AT)
```

Die beiden Slices berühren dieselbe Datei (`hauptengine/validierung.py`) an
verschiedenen Stellen — Git löst das automatisch. Reihenfolge der Merges ist
damit egal.


---

## 9. Nachtrag 05.09. — R 12-2/AC:2019 schließt die Kette für **eine** Nutzung

**Neue Primärquelle im Repo:** `knowledge/OVE-Richtlinie R 12-2 AC 2019-07-01.pdf`
(8 Seiten, frei über den OVE-Webshop). Es ist die **Berichtigung**; sie ersetzt
Abschnitt 5.1 vollständig („Abschnitt 5.1 lautet neu") und enthält **Tabelle 5.1**
auf S. 3–5. Die Basis-Richtlinie R 12-2 liegt weiterhin nicht vor.

**Geprüft wurde ausschließlich Zeile 4 — Verkaufs-/Ausstellungsstätten.**
Volle Kette und Wortlaute: `docs/NORMQUELLEN_AT.md` Abschnitt **2d**.

### 9a. Was jetzt belegt ist

R 12-2 Tabelle 5.1 führt die Unterscheidung als **Spaltenüberschriften**:
„Allgemeine Anforderungen" (Fußnote a: **eingeschränkt auf Fluchtwege**) gegen
„**Erhöhte** Anforderungen" (Fußnote b: ohne diese Einschränkung). Die
OIB-Tabelle 6 benennt dieselben zwei Spalten als „eingeschränkt auf Fluchtwege
und festverlegtes Rettungswegesystem" bzw. „**uneingeschränkt**". Die Werte für
Zeile 4 sind in beiden identisch (`> 200 ≤ 3 000` / `> 3 000`), und R 12-2 nennt
als Grundlage ausdrücklich OIB-RL 2:2019.

> **Damit gilt für diese Nutzung: OIB-Stufe `uneingeschraenkt` ⇔ „erhöhte
> Anforderungen nach der Art der Nutzung" (OVE E 8101 718.560.9.001.AT).**

Die in Abschnitt 8a als **unbelegte Auslegung** geführte Gleichsetzung ist für
Zeile 4 damit **belegt** — und nur für sie.

### 9b. Antworten auf die vier Umsetzungsfragen

| Frage | Antwort für Verkaufs-/Ausstellungsstätten |
|---|---|
| **Welche vorhandenen Eingaben belegen erhöhte Anforderungen?** | `Gebaeudeteil.nutzungsart = VERKAUFSSTAETTE_AUSSTELLUNGSSTAETTE` **und** `verkaufsflaeche_m2 > 3000` → unsere Auswertung liefert `uneingeschraenkt`. Beide Felder existieren im `ProjektKontext`; **keine Contract-Erweiterung nötig** |
| **Welche Aussage ist bei allgemeinen Anforderungen zulässig?** | `> 200 ≤ 3 000 m²` → `eingeschraenkt` = **Sicherheitsbeleuchtung für Fluchtwege** (EN 1838 Begriff 3.4, Bemessungsbetriebsdauer 1 h). Daraus folgt **kein** OVE-Zusatz-Trigger — aber auch **kein Ausschluss** anderer Anforderungen. Fußnote a: „weitere Arten der Notbeleuchtung (zB Antipanikbeleuchtung)" können je nach Nutzung nötig sein → **Review, keine Automatik** |
| **Wie bleibt die Anwendung auf den Sanitärbereich begrenzt?** | über die bereits gebaute Kette: `raum_zuordnung` (Gebäudeteil → Raum) **und** Raumtyp-Filter (`_WC_TYPEN`) **und** Flächenschwelle 8 m². R 12-2 Fußnote c („bei gemischter Nutzung gelten die für die **jeweilige Nutzung** anzuwendenden Anforderungen") bestätigt die raumbezogene Auswertung wörtlich |
| **Welche Beleglücke bleibt?** | siehe 9c — sie liegt **nicht mehr** beim Geltungsbereich, sondern bei **Beleuchtungsart und Nachweis** |

### 9c. Die verbleibende Lücke — drei Fragen, sauber getrennt

1. **Erforderlichkeit** — *gelöst* für diese Nutzung: `uneingeschraenkt` belegt
   die erhöhten Anforderungen, damit greift 718.560.9.001.AT Punkt 1 für
   Sanitärbereiche ab 8 m².
2. **Beleuchtungsart** — *offen*. OVE Punkt 1 verlangt „**eine
   Sicherheitsbeleuchtung**", ohne Art. R 12-2 Fußnote b nennt „Sicherheits-
   beleuchtung und ggfs. eine Ersatzbeleuchtung gemäß ÖNORM EN 1838". **Antipanik
   steht nirgends** — sie wird in Fußnote a nur als *mögliche weitere Art*
   erwähnt. Unsere `flaechen_strategy` erzeugt für den Schwellen-Trigger jedoch
   `kind="antipanik"`. Das wäre eine **Über-Spezifikation** und ist vor einer
   Aktivierung zu klären. (Nur **Punkt 3** der OVE-Klausel nennt Antipanik
   ausdrücklich — und der gilt nur für Verkehrseinrichtungen.)
3. **Lichttechnischer Nachweis** — *offen*. Für einen Sanitärraum nennt weder
   OVE E 8101 noch R 12-2 einen Lux-Wert. EN 1838 §4.3.1 (0,5 lx Antipanik,
   Randbereiche 0,5 m) darf **nicht** unterstellt werden, §4.2.1 (1 lx
   Mittellinie) gilt dem Rettungsweg. Ohne belegten Wert gibt es keinen Nachweis,
   nur eine gesetzte Leuchte.

### 9d. Was das für die Umsetzung heißt

**Belegtes Umsetzungskriterium** (für diese eine Nutzung):

```
nutzungsart == VERKAUFSSTAETTE_AUSSTELLUNGSSTAETTE
  und verkaufsflaeche_m2 > 3000            → OIB-Stufe uneingeschraenkt
  und raum_zuordnung(raum) == bestaetigt    → Raum gehört zu diesem Gebäudeteil
  und raum_typ ∈ WC/Sanitär und flaeche_m2 >= 8
  ⇒ „Sicherheitsbeleuchtung erforderlich" nach 718.560.9.001.AT Punkt 1
```

**Was den letzten Schritt weiterhin blockiert:** die Leuchtenart (2.) und der
fehlende Lux-Wert (3.). Solange beides offen ist, bleibt `wc_sanitaer_min_m2`
leer — der Grund hat sich aber **verschoben**: nicht mehr „Geltungsbereich
unbelegt", sondern „**Art und Nachweis der geforderten Beleuchtung unbelegt**".

**Ebenfalls weiter offen:** alle übrigen Zeilen der Tabelle (nur Zeile 4 geprüft) ·
die 60-m²-Schwelle (Punkt 3, Verkehrseinrichtungen, Raumkategorie fehlt) · die
Übertragung auf **OVE E 8101:2025**, die ebenfalls auf R 12-2 verweist — welche
R-12-2-Ausgabe dort gemeint ist, ist **nicht belegt**.
