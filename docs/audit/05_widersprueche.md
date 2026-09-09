# 05 — Widerspruchs-Matrix (A4)

**Subagent A4.** Synthese aus A1 (`01_plan_forensik.md`), A2 (`02_wissens_coverage.md`),
A3 (`03_engine_ist.md`), stichprobenartig gegen echten Code/YAML gegengeprüft
(Beleg `datei:zeile`). Vier Kollisions-Richtungen: **Norm↔Norm**, **Norm↔Code-Konstante**,
**Enis-Daten↔Platzierungslogik**, **Plan-Praxis(A1)↔Regel(A3)**.

## Auflösungs-Hierarchie (BINDEND)

```
LB-explizit  →  Referenz-Praxis  →  EN/ÖNorm-Default  →  OVE-Verbote (Hard Stop)
```
DE-only wird NIE Default, nur Referenz-Praxis-Fallback. Jede Kollision trägt **eine**
Auflösung — kein „beides möglich".

Schwere: **S1** Hard-Stop/Verbot verletzt · **S2** Code tut nachweislich Falsches ·
**S3** Regel fehlt ganz · **S4** Drift/kosmetisch.

---

## Verifikations-Notizen (eigene Gegenprüfung)

- `lux_nachweis_bericht.py:41` `MF, HM, _ICD = 0.80, 2.4, 45.0`; **doppelter Pfad im
  selben File**: `_lux_feld` (`:60-70`) endet `return e * MF` (0,80 hart), aber
  `_rw_stats` (`:90-103`) rechnet mit `anf.wartungsfaktor or 1.0` (`:92,98,99`).
  → zwei WF-Quellen in einem Bericht, bestätigt (verschärft A3 (b)).
- `validierung.py:35` `_REDUNDANZ_REICHWEITE_MM = 30000.0` mit Kommentar „z=200·h=0,15";
  dieselbe Zahl entsteht dynamisch aus `erkennungsweite_m` (`provider.py:387-390`,
  YAML `en1838_grundwerte.yaml:45,49`). Duplikat bestätigt.
- `sonderstellen_strategy.py:57` `_TOILETTEN_TYPEN = {"WC","TOILETTE"}` — hartkodiert,
  dupliziert `sonderstellen.yaml raumtypen_eindeutig [WC,TOILETTE]` (A2 §E). Bestätigt.
- `en1838_grundwerte.yaml:136-139`: `flaechen_schwellen` **bewusst leer** („60/8 m²
  stehen NICHT in EN 1838"). → Flächen-Trigger inert (A2 §B/§F). Bestätigt.
- `dxf_renderer.py:33` `LAYER_NOTBELEUCHTUNG = library.SAFETY_LAYER` (EIN Symbol-Layer
  für RZ+SL+Antipanik); `:36` `LAYER_FLUCHTWEG` grün. **Kein gelb-Layer** für SL.
  → A1-F18 (grün RZ / gelb SL) bestätigt: Engine trennt nicht zweifarbig.
- `erkennungsweite.z_hinterleuchtet: 200.0` (`en1838_grundwerte.yaml:45`),
  `piktogramm_hoehe_default_m: 0.15` (`:49`) → 30 m. Bestätigt.

---

## A. Widerspruchs-Matrix

| ID | Seite A + Beleg | Seite B + Beleg | Geltungs-Tags | Schwere | Owner | Auflösung (nach Hierarchie) |
|----|-----------------|-----------------|---------------|---------|-------|------------------------------|
| **W01** | Montagehöhe im Stiegenhaus **bis 10,8 m** real gebaut, 1 SL+RZ je Podest (A1 F07/F08, Baraw. Stiege A S.5/8-9) | Engine floor `montagehoehe_min_mm: 2000` fest, Deckungs-Radius fix z·h=30 m mit `HINTERLEUCHTET_DEFAULT` (A3 §b; `provider.py:141-144`); RZ-Höchsthöhe „≤10 m" wird bei 10,8 m überschritten | [AT-Referenzpraxis] / [AT-verbindlich] | **S2** | Enis (Höhen-Naht) / Leonis (Stiegen-Strategie) | Referenz-Praxis schlägt Default: Stiegenhaus braucht **podest-gestaffelte Höhe** statt fixem Floor; Enis liefert höhen-/podestabhängigen Wert, Leonis konsumiert je Geschoss. 10-m-Kappung als weiche Warnung, nicht Hard-Stop (real >10 m belegt). |
| **W02** | din prüft Rettungsweg **vertikal (senkrecht, adaptiv)** an Objekt-/Türhöhen 0,0/0,18/2,2/2,4 m (A1 F05/N02, LW Bericht S.9) | Engine misst **horizontal** in Mittellinie, 1 lx, Höhe 2,0 m (A3 „1-lx-Band"; `deckung.py:70-162`, `lux.py`) | [AT-verbindlich] / [AT-Referenzpraxis] | **S3** | Leonis (lux-Nachweis) / Enis (Nachweis-Typ-Naht) | Beide Nachweise gelten (EN 1838 fordert horizontal am Boden; din-Praxis ergänzt vertikal). Regel fehlt ganz → **vertikalen Nachweis-Typ ergänzen** als Zusatz-Nachweis, horizontaler bleibt Pflicht-Default. Kein Ersatz. |
| **W03** | din berücksichtigt **Möbel-Verschattung** in Garage/Stiege (A1 F22/N05, Baraw. Garage S.7) | Engine-lux ist **möbelfrei** (leerer Raum), keine Verschattung (A3 lux.py; A2 §B) | [AT-Referenzpraxis] | **S3** | Selman (Möbel im RaumModell) / Leonis (lux-Konsum) | Referenz-Praxis = zulässige Verschärfung. Regel fehlt → Möbel als optionale Verschattungs-Geometrie modellieren; solange RaumModell keine Möbel trägt, bleibt möbelfrei der konservativ-zulässige Default (nicht falsch, nur weniger streng). |
| **W04** | **Blendungsbegrenzung f(h)**, Treppe = jeder Winkel (A1-Kontext EN 1838 §4.1 Tab.; A3 „Blendungsgrenzen FEHLT") | Grep `blendung/glare/luminanz/cd/m²` = **0 Treffer** (A3; `src/**`) | [AT-verbindlich] | **S3** | Leonis (lux) / Enis (Grenzwert-Naht) | EN-Default fehlt komplett → Blendungs-/Leuchtdichte-Grenzraster ergänzen; Enis liefert die h-abhängigen cd/m²-Grenzen, Leonis prüft. Bis dahin bewusst als bekannte Lücke markieren. |
| **W05** | Ud-Grenze 1:40 in **zwei Schreibweisen** real: `Ud ≥ 0.025` (LW) und `Ud ≤ 40.000` (Baraw.) (A1 F04/N03) | Engine kennt nur `gleichmaessigkeit_max: 40.0` und prüft `ud = min/max ≥ 1/40` (`lux.py:59,173`); Bericht schreibt `ok_ud: ud >= 0.025` (`lux_nachweis_bericht.py:103`) — nur EINE Schreibweise beschriftet | [AT-verbindlich] | **S4** | Leonis (Bericht-Beschriftung) | Beide sind dieselbe Norm-Kennzahl gespiegelt. Auflösung: Bericht muss **beide Konventionen korrekt labeln** (Emin/Emax UND Emax/Emin), sonst Fehl-„ok". Rechenweg stimmt; rein kosmetisch/Beschriftung. |
| **W06** | din trennt Layer **zweifarbig: grün = RZ/Zeichen, gelb = SL/Ausleuchtung** (A1 F18, V25.dxf) | Engine rendert ALLE Notlicht-Symbole auf **einem** Layer `din_SIBEL_10_emergency_lighting` (A3-Kontext; `dxf_renderer.py:33` `LAYER_NOTBELEUCHTUNG = SAFETY_LAYER`), Fluchtweg separat grün (`:36`) | [AT-Referenzpraxis] | **S4** | Leonis (render) | Referenz-Praxis, nicht normativ erzwungen. Auflösung: **zweifarbige Layer-Trennung übernehmen** (SL/SPOT auf gelb-Layer, RZ auf grün) als Referenz-Praxis-Angleichung. Kosmetisch, kein Norm-Verstoß, daher S4. |
| **W07** | Außen-Wartungsfaktor **0,57** gleichzeitig mit innen 0,8 in EINEM Projekt (A1 F02/N01, beide Baraw.-Berichte S.2) | Engine kennt nur EINEN `wartungsfaktor` je Anforderung (A3 „Wartungsfaktor"; `deckung.py:104` etc., Default 1,0) — kein bereichs-(innen/außen)-abhängiger WF | [AT-Referenzpraxis] | **S3** | Enis (`NormAnforderung.wartungsfaktor` bereichsabhängig) / Leonis (Konsum) | Referenz-Praxis. Regel fehlt → WF **bereichsabhängig** (innen 0,80 / außen 0,57). Enis erweitert die Naht, Leonis wählt je Raum/Außenzone. Single-WF bleibt Fallback bis Naht steht. |
| **W08** | Norm-Wert Erkennungsweite z·h = 30 m lebt in `en1838_grundwerte.yaml:45,49` und wird dynamisch via `erkennungsweite_m` berechnet (A2 §B; A3 §b) | **Duplikat als Code-Konstante** `_REDUNDANZ_REICHWEITE_MM = 30000.0` (`validierung.py:35`) — heute gleiche Zahl, aber entkoppelt | [AT-verbindlich] | **S4** | Leonis (validierung) / Enis (Wert-Quelle) | Drift-Risiko: ändert Enis z oder h, driftet die 4b-Redundanzprüfung still. Auflösung: Konstante **durch `norm.erkennungsweite_m(...)` ersetzen** (Single Source = YAML). Zahlen heute gleich → S4. |
| **W09** | WF-Anzeige im PDF-Bericht **hartkodiert 0,80** in `_lux_feld` (`lux_nachweis_bericht.py:41,70` `return e * MF`) | derselbe Bericht rechnet in `_rw_stats` mit `anf.wartungsfaktor or 1.0` (`:92,98,99`); Engine-Default sonst 1,0 (A3) | [AT-Referenzpraxis] | **S2** | Leonis (render) / Enis (WF-Wert) | Zwei WF-Quellen in EINEM Bericht = nachweislich inkonsistent (Feld-Overlay 0,80 vs. Mittellinie 1,0). Auflösung: **beide Pfade auf `anf.wartungsfaktor` ziehen** (eine Quelle = Enis' Norm-Naht). Bericht zeigt sonst zwei verschiedene lux-Niveaus für denselben Raum. |
| **W10** | Toiletten-Scope `raumtypen_eindeutig [WC, TOILETTE]` in `sonderstellen.yaml` (A2 §E, `:349`-Bereich) | **hartkodiert dupliziert** `_TOILETTEN_TYPEN = {"WC","TOILETTE"}` (`sonderstellen_strategy.py:57,180`); YAML-Wert ist totes Wissen | [AT-verbindlich] | **S4** | Enis (YAML) / Leonis (Strategie) | Gleiche Werte, zwei Quellen → Drift. Auflösung: Strategie **liest den Scope aus dem Provider/Snapshot** statt Python-Konstante; oder YAML löschen und Python als Single Source deklarieren. Da Logik lebt und Werte gleich → S4. |
| **W11** | din: Antipanik-**Flächen-Trigger** real (>60 m²-Praxis, UG-Garage 19 SPOT / 3×AP3) (A1 F15) | Contract-Feld `flaechen_schwellen` **bewusst leer** (`en1838_grundwerte.yaml:136-139` „60/8 m² stehen NICHT in EN 1838"); `flaechen_strategy.py:148` liest es → **inert/No-op** (A2 §B/§F) | [AT-verbindlich] (EN kennt keine Schwelle) / [AT-Referenzpraxis] (60 m²-Praxis) | **S3** | Enis (Wert-Quelle) / Leonis (Trigger) | EN 1838 hat KEINE m²-Schwelle → sie darf nicht als Norm-Default hardcodiert werden. Die 60/8 m² sind [AT-Referenzpraxis]/DE-Herkunft. Auflösung: als **Referenz-Praxis-Trigger** füllen (nicht als Norm), klar getaggt; solange leer, ist der Antipanik-Flächen-Auslöser real inaktiv → dokumentierte Lücke. |
| **W12** | Sonderstellen §4.1.2 h/i: **5 lx vertikal** am Feuerlöscher/Hydrant/Erste-Hilfe/Melder + 2-m-Regel (A1-Kontext; A2 §E, `sonderstellen.yaml`) | Werte **nirgends zur Laufzeit gelesen** (`fuer_sonderstelle`/`zur_pruefung` ohne Konsument, A2 §A/§E); `engine_status: input_fehlt` — RaumModell trägt keine Stellen | [AT-verbindlich] | **S3** | Selman (Stellen im RaumModell) / Enis (Naht) / Leonis (Konsum) | Norm-Pflicht, aber Input fehlt. Auflösung: Selman liefert Sonderstellen-POIs im RaumModell, dann Leonis konsumiert die (belegten) 5-lx-Werte über `NormAnforderung`. Bis dahin bewusst offener Norm-Gap, nicht falsch platziert (kein Silent-OK). |
| **W13** | din: **Getrennter Sicherheitskreis + Bereitschaftsschaltung**, SL eigene Stromkreise (A1 F12, Aichh. P03 EG S.1, OIB-RL) | Engine trägt DL/BL + circuit_hint (`IsBLString`, #96/#98) — vorhanden; aber Cap-20/Bereitschaft nur als Label, keine echte Kreis-Trennungs-Prüfung als Hard-Stop | [AT-verbindlich] | **S3** | Leonis (circuit_zuordnung) / gemeinsam (Contract) | Kernmission. Vorhanden als Datenfeld, fehlt als **erzwungene Invariante** (getrennter Sicherheitskreis = OVE/OIB-Pflicht). Auflösung: Kreis-Trennung als Prüf-Regel/Hard-Stop ergänzen (SL nie auf Allgemein-Kreis). Feld existiert → nur die Prüfung fehlt. |
| **W14** | din: `RZ_00` (ohne Pfeil) bei **Deckenmontage direkt über Tür** — Tür selbst = Richtung (A1 F19, V25 Katalog) | Engine-Regel 13 nutzt Pfeil-Block + Pfeil-durch-Tür-Formel dreifach dupliziert (A3 §a; `anker_strategy.py:140`, `gang_strategy.py:143`, `fachpraxis.py:303`) — kein pfeilloser Über-Tür-Fall | [AT-Referenzpraxis] | **S3** | Leonis (orientation/bausteine) | Referenz-Praxis ergänzt EN-Default. Regel fehlt → **pfeillose RZ_00-Variante** für Deckenmontage exakt über der Tür. Zugleich Rotations-Formel entduplizieren (Drift-Risiko, s. W16). |
| **W15** | din: photometrischer **a/b-Tabellen-Lookup** je Montagehöhe (0,5-m-Stufe, nie interpolieren) (A1-Kontext; A3 Checkliste) | Engine **bisektioniert analytisch** aus Punktmethode (`lux.max_leuchtenabstand_mm:231-282`) und **interpoliert** zwischen C-Ebenen (`ldt.py:77`) | [DE-only] (a/b-Tabellen = DE-Hersteller/DIN-Praxis) | **S4** | Leonis (lux) | a/b-Tabelle ist **DE-only** → wird NIE Default. Die analytische Punktmethode (physikalisch korrekt, kontinuierlich) bleibt der Weg. Auflösung: **Engine-Verfahren behalten**, a/b-Tabelle allenfalls als Referenz-Cross-Check. Kein Handlungszwang → S4. |
| **W16** | Pfeil-zur-Tür-Rotationsformel als kanonische Regel (A3 §a) | **dreifach kopiert**: `anker_strategy.py:140`, `gang_strategy.py:143`, `fachpraxis.py:303` (identische Formel) | [AT-verbindlich] (Pfeilrichtung) | **S4** | Leonis (platzierung) | Zahlen/Formel identisch, aber Drift-Risiko bei Änderung. Auflösung: in **eine Helper-Funktion** ziehen (z.B. `orientation`), alle drei rufen sie. Kosmetisch → S4. |
| **W17** | `plan_rettungszeichen_sichtlinie` ruft `norm.erkennungsweite_m` direkt (Sichtlinien-Deckung) | Funktion ist **NICHT im place()-Pfad** — nur test-only (A3 §b: 8 Test-Treffer, 0 Produktions-Aufrufer) | [AT-verbindlich] | **S3** | Leonis (platzierung) | Sichtachsen-Deckung (EN 1838 §5.x Erkennbarkeit) ist real gefordert, aber der Code-Pfad ist tot. Auflösung: entweder **in place() verdrahten** (wenn Sichtachsen-Garantie gewollt) oder als bewusst deaktiviert dokumentieren. Aktuell stille Lücke. |
| **W18** | `platzierung_regeln.yaml` = 25 deklarative RZ/SL/HS-Regeln als „Datenlieferant" gedacht (A2 §D) | **GESAMT tot** — Platzierer implementiert Logik prozedural in `*_strategy.py`, liest die YAML nie (A2 §D: kein src-Konsument) | [AT-verbindlich] | **S4** | gemeinsam (Contract) / Enis (YAML) | YAML und Code können driften (Doku vs. Verhalten). Auflösung: YAML als **Contract/Doku-Kandidat deklarieren** oder verdrahten. Da Verhalten korrekt in Code lebt → S4 (kein falsches Verhalten, nur Doku-Drift). |
| **W19** | ≥2 Leuchten je Bereich (EN 50172 / EN 1838 §5.1.8) real gefordert | Engine prüft nur als **QA-Warnung, kein Hard-Fail** (`validierung.py:159-177`, Kommentar „Hard-Fail folgt später"); Platzierung erzwingt es nicht (A3 Checkliste) | [AT-verbindlich] | **S2** | Leonis (validierung + platzierung) | Redundanz ist normativ Pflicht (Ausfall einer Leuchte darf Fluchtweg nicht verdunkeln). Warnung statt Fail = Silent-Pass möglich. Auflösung: **auf Hard-Fail hochziehen** und Platzierung 2-Leuchten-garantiert machen. |

---

## B. Norm↔Norm (Hierarchie-Kollisionen, konsolidiert)

- **Montagehöhe:** EN 1838 „≥ 2 m" Floor (aktiv, `en1838_grundwerte.yaml:38`) vs.
  Referenz-Praxis „bis 10,8 m gestaffelt im Stiegenhaus" (W01). Auflösung: Floor
  bleibt Untergrenze [AT-verbindlich]; die Höhen-Staffelung nach oben ist
  Referenz-Praxis und darf den Floor nicht unterschreiten, aber die 10-m-Kappung
  ist nur weiche Warnung.
- **WF innen 0,80 vs. außen 0,57:** kein Norm-Norm-Konflikt, sondern
  bereichsabhängige Referenz-Praxis (W07) — beide gelten gleichzeitig je Zone.
- **Ud ≥0,025 vs. ≤40:** identische Norm, gespiegelte Kennzahl (W05) — kein echter
  Konflikt, reine Beschriftungsfrage.

---

## Unbelegt

- **Keine.** Alle in dieser Matrix geführten Kollisionen tragen einen Beleg
  `datei:zeile` oder eine A1/A2/A3-Fundstelle. Die aus dem A1-Report bewusst
  ungelesenen 7 DWG-XRefs (Raum-Labels, ODA nicht installiert, A1 §D) sowie die
  P2-Prosa-Digests (A2 §J, kein Engine-Input) erzeugen KEINE hier bewertbaren
  Code-Kollisionen und sind daher nicht als Widerspruch, sondern als Scope-Grenze
  vermerkt.
