# Quellenverarbeitung — Stand je Dokument und je Thema

**Fortführung von** [`QUELLENWIRKUNG_2026-09-07.md`](QUELLENWIRKUNG_2026-09-07.md)
(Verzeichnis der Quelldateien + Kapitel 2 „Anforderungen bis zum Code verfolgt").
Diese Datei ersetzt jenen Bericht **nicht** — sie führt seine Tabellen fort und
ergänzt die Spalten, die dort fehlten: **benötigte Projektangaben**, **tatsächlicher
Verbraucher** und **verbleibende Arbeit**.

**Stand:** 2026-09-08 · **Branch:** `enis/regel-deckung-abnahme-0907`
**Nicht neu geprüft:** R-12-2-Tabelle 5.1, A1–A5, EN 1838 §4.1.2, die
Deckungs-Abnahme und das Quellen-Audit selbst gelten unverändert weiter.

---

## 0. Die vier Verarbeitungsstufen — getrennt geführt

| Stufe | Bedeutung | Nachweis |
|---|---|---|
| **① extrahiert** | Datei liegt vor, Volltext gelesen, Fundstellen notiert | Zitat mit Seite/Abschnitt |
| **② fachlich geprüft** | Anforderung, Bedingungen und Ausnahmen sind herausgearbeitet und gegen das Original geprüft | Bericht in `docs/` |
| **③ lokal implementiert** | steht in `normwissen/data` bzw. `normwissen/*.py` und ist durch einen Test gedeckt | Test in `tests/normwissen/` |
| **④ im gemeinsamen Stand verwendet und getestet** | ein Konsument (Pipeline/Platzierung/Ausgabe) nutzt es **auf `origin/main`** und ein Test dort weist es nach | Lauf gegen `origin/main` |

⚠️ **③ ist nicht ④.** Eine YAML-Datei und ein isoliert grüner Helfer belegen keine
Nutzung durch die Engine. Wo die Kette bei ③ endet, steht das ausdrücklich da.

---

## 1. Paket `knowledge/Österreichische Rechtsquelle/`

| Datei | Art | Ebene | Stufe | Bemerkung |
|---|---|---|---|---|
| `RIS_AStV_geltende_Fassung_2026-09-06.pdf` (27 S.) | Rechtsverordnung | **A** | **③** | Volltext ausgewertet (§ 1, § 9, § 13). ⚠️ Liegt **nur** auf `enis/sanitaer-beleuchtungsart-0906` (`ee55445`), nicht auf diesem Branch |
| `RIS_AStV_§9_…_Auszug.md` | Wortlaut-Auszug | **A** | **③** | Grundlage der Regeln unten |
| `RIS_ASchG_geltende_Fassung_2026-09-06.pdf` | Bundesgesetz | **A** | **②** | § 19 (Arbeitsstätten-Begriff) geprüft; § 94 als Behördenpfad benannt |
| `RIS_ASchG_§19_…_Auszug.md` | Wortlaut-Auszug | **A** | **②** | trägt die Legaldefinition, an der `arbeitsstaette_nach_aschg` hängt |
| `RIVOPLAN_Oesterreichische_Rechtsquellen_Notbeleuchtung_AT.pdf` (10 S.) | **eigene Zusammenfassung, NICHT amtlich** | — | **①** | Sekundär. Wird **nicht** als Beleg verwendet; jede Aussage daraus ist am RIS-Original nachzuprüfen |

## 2. Paket `knowledge/OVE-Fachinformation/` (17 Dateien)

| Datei | einschlägig | Ebene | Stufe | Bemerkung |
|---|---|---|---|---|
| `Fachinfo_E-08_…Arbeitsstaetten_2021-04.pdf` | **ja, Kern** | **D** | **③** | Volltext (6 S.) ausgewertet: Tabelle 1, Abschnitte 4, 5.1–5.3, 6 → `data/astv_arbeitsstaetten.yaml` |
| `Fachinfo_E-07_Sicherheitsbeleuchtung_2020-12.pdf` | ja | **D** | **②** | Volltext **und Bilder 1–6** ausgewertet (Abschnitt 5a) → `data/ove_e07_funktionserhalt.yaml`. Keine Umsetzung: Leitungs-/Stromkreismodell fehlt. ⚠️ Bezugsnorm **E 8002-1:2002 fehlt im Repo** |
| `Fachinfo_E-05_…Garagen_2020-12.pdf` | am Rand | **D** | **②** | Volltext (1 S.) ausgewertet (Abschnitt 5c) → `data/ove_e05_e06_anlagen.yaml`. ⚠️ Inhalt von **1991**, Bezugsnorm **ÖVE-EN 1 Teil 4 § 90:1991 fehlt** |
| `Fachinfo_E-06_Bussystem_2020-12.pdf` | am Rand | **D** | **②** | Volltext (2 S.) ausgewertet (Abschnitt 5c). ⚠️ Inhalt von **2009**, Bezugsnorm **ÖVE/ÖNORM E 8002-1:2007 fehlt** |
| E-01 · E-02 · E-03 · E-04 · E-09 · E-10 · E-11 · E-13 · H02 · `fachmeinung04` · `klemmen` · `8001_2` · `OVE-IM12` | **nein** | D | **⑦ außerhalb** | Licht-/Steckdosenstromkreise, Korrekturen zu E 8001, USV, Ableitströme, SPD-Schutzbereich, Spannungsabfall, Voruntersuchungen, Kabel/Leitungen, Klemmen. Kein Notbeleuchtungs-Tatbestand; **kurz begründet ausgeschlossen, Originale bleiben liegen** |

## 3. Paket `knowledge/OIB-Richtlinien/` (48 Dateien)

Unverändert gegenüber dem Audit (Kapitel 1.1 + K3) — hier nur der Stand:

| Richtlinie | einschlägig | Stufe | Verbraucher |
|---|---|---|---|
| **RL 2** Brandschutz (Mai 2023 **und** April 2019, je + Erläuterungen + Änderungen) | **ja, Kern** | **④** | `oib_rl2_tabelle6.yaml` → `oib/tabelle6.py` → `pipeline:bewerte_oib` |
| **RL 2.1** Betriebsbauten (3.6.5) · **RL 2.3** Fluchtniveau > 22 m (2.14) | ja | ④ | nur Verweis auf Tabelle 6 → über RL 2 abgedeckt |
| **RL 2.2** Garagen (5.5.3, Tab. 3 Z. 8.2) | ja | ④ | Zeile 11.1, Bänder 250/1 600 m² — gemessen |
| **RL Begriffsbestimmungen** · **RL Zitierte Normen** | ja | ② | Netto-Grundfläche (→ ÖNORM B 1800, **fehlt**), Ausgabestände |
| **RL 4** Nutzungssicherheit/Barrierefreiheit | **ja** (Korrektur K3) | **②** | Kapitel 2 erfasst (Abschnitt 5b) → `data/oib_rl4_fluchtwegbreiten.yaml`. ⚠️ Liefert die **erforderliche Mindestbreite**, **nicht** die gemessene Breite für § 4.2.1 |
| RL 3 · RL 1 · RL 5 · RL 6 · RL 7 | **nein** | ⑦ | Hygiene („beleuchtbar", kein Notlicht-Tatbestand) · Tragwerk · Schall · Energie · Grundlagendokument |

---

## 4. Themen-Tabelle — Arbeitsstätten / AStV / OVE E08 (dieser Block)

| # | Quelle · Ausgabe · Fundstelle | Fachliche Anforderung | Bedingungen / Ausnahmen | Benötigte Projektangabe | Regel-/Codestelle | Tatsächlicher Verbraucher | Nachweis | Verbleibende Arbeit | Stufe |
|---|---|---|---|---|---|---|---|---|---|
| **AS-1** | AStV BGBl. II 368/1998 i.d.g.F. (Fassung 06.09.2026) **§ 9 Abs. 1 Z 1** | Sicherheitsbeleuchtung für **Arbeitsräume und Fluchtwege, die nicht natürlich belichtet sind** | Arbeitsraum = mind. ein ständiger Arbeitsplatz (§ 1 Abs. 4). § 9 nennt **weder Beleuchtungsart noch Lux** | `natuerlich_belichtet` je Raum/Abschnitt **+** Arbeitsraum-Eigenschaft | `data/astv_arbeitsstaetten.yaml::tatbestaende[0]` · `normwissen/astv.py` | **Hinweis** über `oib/provider.py::_astv_hinweise` → `OibBefund.hinweise` | `tests/normwissen/test_astv_arbeitsstaetten.py` (26) | Contract-Feld für die Belichtung (3 Owner, Erhebung @polatselman) | **③** |
| **AS-2** | dito **§ 9 Abs. 1 Z 2** | Sicherheitsbeleuchtung für **Fluchtwege**, deren vorhandene natürliche Belichtung bei Ausfall der künstlichen Beleuchtung **nicht ausreicht** | ⚠️ **nur Fluchtwege** — nicht Arbeitsräume. **Nicht aus Z 1 ableitbar**: Beurteilungsgründe sind „bauliche Gegebenheiten"/„Lage der Arbeitszeit" | dreiwertige **Beurteilung** je Fluchtweg-Abschnitt + Begründung | dito `tatbestaende[1]` | dito | dito (`test_z2_gilt_nur_fuer_fluchtwege`) | Feld im `ProjektKontext`/LB (3 Owner) | **③** |
| **AS-3** | dito **§ 9 Abs. 1 Z 3** | Sicherheitsbeleuchtung für **Bereiche mit besonderer Gefahr** bei Ausfall der Beleuchtung | ⚠️ **nicht** gleichzusetzen mit `RaumModell.Raum.besondere_gefaehrdung` (das trägt EN 1838 § 4.4). Z 3 sperrt zusätzlich das Wahlrecht nach Abs. 4 | Gefahrenbeurteilung je Bereich | dito `tatbestaende[2]` | dito | dito (`test_z3_wird_nicht_mit_dem_contract_feld_gleichgesetzt`) | eigenes Feld **oder** dokumentierte Abgrenzung (3 Owner) | **③** |
| **AS-4** | dito **§ 9 Abs. 4** | **Zulässige Ausführungswahl:** selbst-/nachleuchtende Orientierungshilfen **statt** Sicherheitsbeleuchtung | Nur wenn **kein** Bereich nach Z 3 vorliegt; **nur abweichend von Z 1 und Z 2**; Abs. 2 und Abs. 3 Z 1 gelten weiter. ⚠️ **Ersetzt keine** Anforderung aus OVE E 8101, R 12-2 oder OIB-RL 2 | Planer-/AG-Entscheidung (LB) | `wahlrecht_abs4` | dito | `test_wahlrecht_bleibt_beim_planer_und_deckt_nur_z1_und_z2` | LB-Feld + Ausweis im Prüfbericht | **③** |
| **AS-5** | dito **§ 1 Abs. 1/2/3/4** | **Anwendungsbereich/Reichweite** | Abs. 3 setzt **nur Abs. 2** außer Kraft, unter **vier kumulativen** Bedingungen; **kein** pauschaler Wohnbau-Ausschluss; Behördenpfad § 94 ASchG bleibt | `arbeitsstaette_nach_aschg` (**vorhanden**) + Lage des Raums, Mitbenutzung, überwiegende Wohnnutzung | `reichweite` | `astv.py::reichweite_vorbehalt` (**noch kein Konsument**) | `test_abs3_ist_keine_wohnbau_bereichsausnahme`, `test_false_erzeugt_keinen_freibrief` | drei fehlende Angaben je Gebäudeteil/Raum | **③** |
| **AS-6** | **OVE-Fachinfo E08:2021-04-01, Tabelle 1** | Empfehlung zur Ausstattung von **Arbeitsräumen** nach Raumgröße (< 30 / 30–100 / > 100–1 600 / > 1 600 m²) und Belichtung | **Ebene D — Empfehlung, keine Rechtspflicht.** Leere Zelle „< 30 m² mit natürlichem Licht" = **Schweigen**, kein „nicht erforderlich". Fußnote a: im Zweifel Sicherheitsleuchten | Arbeitsraum ja/nein · natürlich belichtet ja/nein · Fläche m² | `ausfuehrung_e08[0]` | — (**nicht aktiv**) | `test_e08_tabelle1_…` | erst nach AS-1; dann Entscheidung, ob eine D-Empfehlung überhaupt platzieren darf | **③** |
| **AS-7** | **E08 Abschnitt 4** | zu beleuchtende Stellen im Fluchtweg (Ausgang/Tür, Treppen, Niveauänderung, Richtungsänderung/Kreuzung, Bereich nach dem Ausgang) | deckt sich mit EN 1838 § 4.1.2 → **Bestätigung auf Ebene D**, keine neue Grundlage | — | `ausfuehrung_e08[1]` | die Sonderstellen bleiben **auf EN 1838 gestützt** (`sonderstellen.yaml`) | `test_e08_fluchtwegstellen_bestaetigen_en1838_ohne_neue_grundlage` | keine | **③/④** |
| **AS-8** | **E08 Abschnitt 5.1/5.2** | Anlagen-/Ausführungsangaben: 5 s/50 % · 60 s/100 % · ≥ 60 min · 1 lx im Regelfall · **> 20 Leuchten → automatische Prüfeinrichtung EN 62034** · LPS/CPS: alternierend ≥ 2 Stromkreise, ≤ 20 Leuchten je Endstromkreis | Ebene D | Anlagenkonzept (Stromkreise), Leuchtenzahl je Gebäudeteil | `ausfuehrung_e08[2].deckung_mit_engine` | Umschaltzeit/Dauer/1 lx **bereits** über EN 1838; Prüfeinrichtung + Stromkreise **nicht abgebildet** | `test_anlagenanforderungen_trennen_gedeckt_von_offen` | Prüfregel „> 20 Leuchten" wäre in `hauptengine/validierung.py` → **gemeinsame Naht** | **③ teils** |
| **AS-9** | **E08 5.3** + **EN 1838 § 4.4.1** | besondere Gefährdung: ≥ 10 % **und mindestens 15 lx**; 0,5 s; Dauer nach Gefährdungsdauer | ⚠️ **Bezugsgröße verschieden**: EN 1838 = Wartungswert der **Aufgaben**beleuchtung auf der **Arbeitsfläche**, E08 = **Allgemein**beleuchtung am Arbeitsplatz. Gleich ist nur die absolute Untergrenze **15 lx** | Aufgaben-/Allgemeinbeleuchtungswert **und** Arbeitsfläche — **beides kein Engine-Eingang** | `ausfuehrung_e08[3]` | `NormRegelwerk.arbeitsplatz_lux` bleibt **leer**; Prüfregel in `validierung.py` sagt „manuell prüfen" | `test_e08_15_lx_ist_belegt_aber_nicht_aktivierbar`, `test_kein_contract_wert_wird_aktiviert` | Bezugsfläche modellieren (3 Owner) — **bis dahin bewusst nicht aktiviert** | **② belegt, nicht aktivierbar** |
| **AS-10** | **AStV § 13** + **E08 Abschnitt 6/Tabelle 2** | Betrieb: jährliche Prüfung, monatliche Funktionskontrolle, Aufbewahrung 3 Jahre / 6 Monate, BA5/BA4 | **Funktionsbereich Betrieb/Instandhaltung** — keine Planungsanforderung, erzeugt kein Symbol | — | `betrieb_wartung` | keiner (bewusst) | `test_betriebspflichten_liegen_ausserhalb_der_plangenerierung` | ggf. als Hinweisblock in der Übergabedoku | **③ (eigener Funktionsbereich)** |

---

## 5. Wo die Wirkung heute endet — gemessen, nicht behauptet

Echter Lauf, Owner-Trio (`build_default_bundle`), `Projekte/Mollgasse/1.Kellergeschoß.dxf`,
`Gebaeudeteil(arbeitsstaette_nach_aschg=True)`:

| Stelle | lokale Basis (`enis/regel-deckung-abnahme-0907`) | `origin/main`-Basis (`4c5df91`, mit #132) |
|---|---|---|
| `OibBefund.ergebnisse[*].hinweise` | **enthält** die § 9-Prüfpunkte | **enthält** sie |
| `render_summary["oib"]["hinweise"]` | ⚠️ **nein** — die alte `gate_summary` verwirft Provider-Hinweise | ✅ **ja**, als `[t1] AStV § 9 Abs. 1 nennt drei GETRENNTE Tatbestaende …` |
| gezeichnetes DXF | nein | nein — Hinweise leben im Summary/API; das Blatt trägt nur die Stufe |
| **API-Header `X-Notbeleuchtung`** | ⚠️ nein (der `oib`-Block trägt die Hinweise nicht, weil `gate_summary` sie verwirft) | ✅ **ja** — `oib` steht in `_SUMMARY_HEADER_KEYS`, die AStV-Hinweise sind im Header enthalten |
| voller Prüfbericht (`pruefung`) | nein | nein — **das** ist L2 |

**Korrektur zum ersten Bericht:** die Aussage „DXF/API: nein → L2" war zu pauschal.
Richtig ist: der **API-Header trägt die AStV-Hinweise** (ab `origin/main`), der
**gezeichnete Plan** trägt sie nicht, und der **volle Prüfbericht** ist weiterhin
nicht abrufbar (L2). ⚠️ Aus derselben Messung: der `oib`-Block wächst **linear mit
der Zahl der Gebäudeteile** (~2 KB je Gebäudeteil ohne AStV-Hinweis, ~2,6 KB mit) —
ab etwa drei Arbeitsstätten-Gebäudeteilen reißt der Header die ~8-KB-Grenze.
Details und Messreihe: `docs/proposals/ASTV_E08_ENTSCHEIDUNGSREGELN.md` Abschnitt 8.

---

## 5a. Themen-Tabelle — OVE-Fachinformation E07 (Funktionserhalt)

**Blockstatus: Quellenarbeit abgeschlossen, keine Umsetzung — der Engine fehlen
Leitungs-, Stromkreis- und Brandabschnittsmodelle.**
Daten: `normwissen/data/ove_e07_funktionserhalt.yaml` · Tests:
`tests/normwissen/test_quellenblock_e07_rl4.py`.

| # | Quelle · Fundstelle | Anforderung | Bedingungen / Ausnahmen | Benötigte Angaben | Funktionsbereich | Verbraucher | Nachweis | Verbleibende Arbeit | Stufe |
|---|---|---|---|---|---|---|---|---|---|
| **E07-1** | E07 Einl., S. 1 (zitiert **E 8002-1:2002** 5.4 (1)) | Funktionserhalt ≥ **30 min** für Leitungsanlagen | ausgenommen Endstromkreis-Teile ohne Beeinträchtigung anderer Bereiche | Leitungsanlage, Endstromkreis-Topologie | Elektro-Ausführungsplanung | — | YAML + Test | ⚠️ **historischer Wert** — OVE E 8101 nennt keine Minutenzahl, nur „angemessene Dauer" + R 12-2 | **②** |
| **E07-2** | E07 Abschn. 1 | Schutzziel: lokaler Brand darf Fluchtwege **anderer** Brandabschnitte nicht beeinträchtigen | — | Brandabschnitte, Zuordnung Leuchte → Abschnitt | Schutzziel | — | dito | Brandabschnittsmodell fehlt | **②** |
| **E07-3** | E07 Abschn. 1 | Verzicht in **Unterbrandabschnitten** zulässig | **kumulativ**: ≤ 2 Sicherheitsleuchten je Unterbrandabschnitt **und** Rettungswege nicht beeinträchtigt; **Fluchtstiegenhäuser ausgenommen** | Unterbrandabschnitte (TRVB B 108) | Elektro-Ausführungsplanung | — | dito | ⚠️ **TRVB B 108 fehlt im Repo** → Begriff nicht definierbar | **②** |
| **E07-4** | E07 Abschn. 1 | „nicht beeinträchtigt" = **ca. 50 %** Restfunktion im Rettungsweg | Beispiel: alternierende Stromkreisaufteilung | Stromkreiszuordnung je Leuchte | Elektro-Ausführungsplanung | — | dito | Auslegungsangabe, **kein Normwert** | **②** |
| **E07-5** | E07 Abschn. 2.1 | Leitungen, die Brandabschnitte **queren**, brauchen Funktionserhalt; **innerhalb** darf verzichtet werden | — | Brandabschnittsgrenzen, Leitungsverlauf | Elektro-Ausführungsplanung | — | **Gegenprobe an OVE E 8101** (2019 560.9.1 / 2025 560.9.2): **Struktur bestätigt**, Dauer nicht | Modell fehlt | **②** |
| **E07-6** | E07 Abschn. 2.1 + Bild 1 | E-30-Dosen mit Abzweigsicherungen | Endstromkreis beginnt im Verteiler; Sicherungen nur Kurzschlussschutz, zeitselektiv; 1-/2-polig; kennzeichnen, dokumentieren, zugänglich | Verteiler, Dosen, Stromkreise | Elektro-Ausführungsplanung | — | Bildinhalt jetzt erfasst | Modell fehlt | **②** |
| **E07-7** | E07 Fußnote zu Bild 5 | eigener Steigschacht **F 30** → Leitung ohne Funktionserhalt („E 0") zulässig | nur wenn Einbauten die Sicherheitsbeleuchtung nicht beeinträchtigen | Schachtausbildung | Elektro-Ausführungsplanung | — | Fußnote am Original gelesen | Modell fehlt | **②** |
| **E07-8** | **OVE E 8101:2019 560.9.2** (Ebene **C**) | **max. 20 Leuchten je Endstromkreis**, ≤ 60 % des Nennstroms; Kurzschluss darf Nachbarleuchten nicht abschalten | — | Stromkreise | Anlagenplanung | — | Volltext geprüft, Ausgabe 2025 gleich | ⚠️ dieselbe Grenze nennt E08 5.2 — sie ist **normativ**, nicht nur Ebene D | **②** |

**Extraktionslücken des Digests geschlossen** (`OVE_Fachinfos_E05_E06_E07.md`):
Bilder 1–6 und die Symbollegende sind am Original erfasst; die Legende bindet die
Beispiele ausdrücklich an **Brandabschnitte bis 1.600 m²**.
⚠️ **Die Bilder 2–6 zeigen Leuchten in Abstell-, Sanitär- und Technikräumen — das
ist Illustration der Leitungsführung, keine Platzierungsvorgabe.** Aus ihnen wird
kein Norm-Trigger abgeleitet (durch Test gesichert).
⚠️ **Offen in der Quelle selbst:** „für Brandabschnitte über 1 600 m² sind weiter
gehende Überlegungen anzustellen" — E07 sagt nicht, welche.

## 5b. Themen-Tabelle — OIB-RL 4, Kapitel 2 (Fluchtwegbreiten)

**Blockstatus: Quellenarbeit abgeschlossen, keine Umsetzung — und ausdrücklich
kein Eingang in die Lichtberechnung.**
Daten: `normwissen/data/oib_rl4_fluchtwegbreiten.yaml`.

| # | Fundstelle (RL 4, Mai 2023) | Erforderliche Mindestbreite | Bedingungen / Ausnahmen | Benötigte Angaben | Stufe |
|---|---|---|---|---|---|
| **RL4-1** | 2.4.1 | Hauptgang **1,20 m**; 1,00 m in sechs benannten Fällen (≤ 3 Wohnungen, Reihenhäuser, Nebengänge …) | Aufzählung mit Bedingungen, keine allgemeine Alternative | Gangart, Gebäudeart | **②** |
| **RL4-2** | 2.4.3 Tab. 1 | Haupttreppe **1,20 m** · Wohnungstreppe **0,90 m** · Nebentreppe **0,60 m** | gilt sinngemäß für Podeste; Sonderfall anpassbare Wohnungen 1,10/1,20 m | Treppenart | **②** |
| **RL4-3** | 2.4.4 | Rampen: Tabelle 1 sinngemäß; barrierefrei **1,20 m** | — | Rampe, Barrierefreiheit | **②** |
| **RL4-4** | 2.4.5 | über **120 Personen**: +10 cm je weitere angefangene 10 Personen | gilt für Gänge, Treppen, Rampen | **Personenzahl je Abschnitt** | **②** |
| **RL4-5** | 2.4.7 / 2.4.8 | Zwischenhandläufe > 240 Personen und > 2,40 m; lichte Höhe **2,10 m** | — | Personenzahl, Geometrie | **②** |
| **RL4-6** | 2.8.1 | Türen im Fluchtweg: **80 / 90 / 100 cm** nach ≤ 40 / 80 / 120 Personen | zwei Türen ≤ 20 cm nebeneinander zählen als eine | nutzbare Türbreite, Personenzahl | **②** |
| **RL4-7** | 2.5.1–2.5.4 | **zulässige Einengungen** (Pfeiler 10 cm auf 1,20 m Länge, Handläufe 10 cm je Seite, …) | — | — | **②** |

⚠️ **Die zentrale Trennung:** RL 4 liefert die **erforderliche Mindestbreite**
(Anforderung an den Entwurf); EN 1838 § 4.2.1 braucht die **tatsächliche
geometrische Breite** (Mittelbereich/Randstreifen). **Kein RL-4-Wert darf als
`breite_mm` in die Lux-/Deckungsrechnung** — weder als Default noch als Fallback.
Punkt 2.5 belegt das doppelt: die lichte Breite darf stellenweise **unter** der
Mindestbreite liegen. Die fehlende Messung bleibt der offene Punkt aus
`WEGBREITE_RANDSTREIFEN.md`.

## 5c. Themen-Tabelle — OVE-Fachinformationen E05 (Garagen) und E06 (Bussysteme)

**Blockstatus beider: Quellenarbeit abgeschlossen, keine Umsetzung — beide
betreffen die Anlagentechnik, nicht Erforderlichkeit oder Platzierung.**
Daten: `normwissen/data/ove_e05_e06_anlagen.yaml`.

| # | Quelle · Fundstelle | Aussage | Anwendungsbereich / Grenze | Funktionsbereich | Verbraucher | Verbleibende Arbeit | Stufe |
|---|---|---|---|---|---|---|---|
| **E05-1** | E05:2021-01-01 (Inhalt **e&i 1991**), zu **ÖVE-EN 1 Teil 4 § 90** | „Garagen sind brandgefährdete Räume" ist zu lesen als **„im Sinne dieser Bestimmungen"** — elektrotechnische Klassifikationen gelten nur im **eigenen Geltungsbereich** | Absicht war allein, Starkstromanlagen bis AC 1000 V / DC 1500 V den Installationsbestimmungen des **§ 50** zu unterwerfen | Installationsplanung | — | ⚠️ **§ 50 und § 90 fehlen im Repo** — Inhalt **nicht ergänzt** | **②** |
| **E05-2** | Gegenprobe **OVE E 8101:2025 Teil 7-7N90** | Garagen haben heute einen **eigenen Teil**; die pauschale Einstufung ist **nicht wiederholt**, brandgefährdete Bereiche stehen dort als **bedingter Verweis** (ANMERKUNG 3.AT) | Großgaragen → Teil 7-718; bautechnisch → OIB-Richtlinien | Installationsplanung | — | E05-Aussage bleibt **an 1991 gebunden** | **②** |
| **E05-3** | Verhältnis zu **OIB-RL 2.2 Punkt 5.5.3** | zwei **verschiedene Fragen**: E05 = *wie* installieren, OIB = *ob* Sicherheitsbeleuchtung (> 250 m² Nutzfläche) | ⚠️ Begriffsgleichheit „brandgefährdet" ist **keine** Sachgleichheit | — | OIB-Seite ist **④** (Zeile 11.1) | keine | **②** |
| **E06-1** | E06:2021-01-01 (Inhalt **Jänner 2009**), zu **E 8002-1:2007 Abschn. 7.8.3** | **Kombinierte** Bussysteme = Bus steuert/überwacht **nicht nur** die Sicherheitsbeleuchtung | ⚠️ Alle E06-Punkte gelten **nur** für diesen Fall; getrennter Bus ist **zu bevorzugen** | Anlagensteuerung | — | Bezugsnorm **fehlt** | **②** |
| **E06-2** | E06 2.1.1 | Herstellerbestätigung: **Umschaltzeit ≤ 0,5 s** bei voller Buskomponenten-Bestückung + Kompatibilität Bus–EVG–Leuchte | ⚠️ **Nicht** die EN-1838-Umschaltzeit (5 s/60 s) und **nicht** § 4.4.6; `umschaltzeit_max_s` bleibt **60 s** | Anlagensteuerung | — | keine | **②** |
| **E06-3** | E06 2.1.2–2.1.6 | Rückwirkungsfreiheit bestätigen; Bestückung/Parameter dokumentieren; Änderungen nur willentlich; integrierte Sicherheitsleuchten und Prüf-Schalteinrichtungen kennzeichnen | Ausführungs- und Bestandsdokumentation | Dokumentation | — | keine | **②** |
| **E06-4** | E06 2.2 / 2.3 | **Erstprüfung** (5 Punkte, ggf. befugte Fachkraft) und **Wiederholungsprüfung** (4 Punkte, zusätzlich **Aktualität** der Doku) | ⚠️ E06 nennt **kein Intervall** — Intervalle stehen in AStV § 13 / E08 Abschnitt 6 | Prüfung/Betrieb | — | keine | **②** |

## 5d. Verbleibender Bestand nach diesem Arbeitsblock

### Noch unbearbeitete relevante Abschnitte

| Ordner | offen | Einschätzung |
|---|---|---|
| `OVE-Fachinformation/` | **keine** notbeleuchtungsrelevante Datei mehr | E05–E08 sind ausgewertet; E01–E04, E09–E13, H02 und die übrigen sind begründet außerhalb |
| `OIB-Richtlinien/` | **RL 2 Begriffsbestimmungen** (Netto-Grundflächen-Kette) · **RL Zitierte Normen** (Ausgabestände) | beides **②**, blockiert durch **ÖNORM B 1800** |
| `Österreichische Rechtsquelle/` | **AStV-Ausgabenvergleich (K1)** — zweiter Ausdruck fehlt · übrige AStV-Abschnitte ohne Beleuchtungsbezug | RIVOPLAN-Zusammenfassung bleibt **Sekundärquelle** |

### Aufbereitete Regeln, die auf Integration warten

| Regel | liegt in | fehlt |
|---|---|---|
| AStV § 9 Z 1–Z 3, Abs. 4, § 1 | `astv.py` + YAML | **Aufrufer** (validierung) **und** die Eingaben |
| `weg_nachweis()` (§ 4.2.1-Regime) | `provider.py` | **Aufrufer** — bis heute nur Tests |
| `deckung_fuer()` (S1-Herkunftsauskunft) | `provider.py` | **Aufrufer** — bewusst, siehe S1 |
| RL-4-Mindestbreiten, E07-, E05/E06-Regeln | YAML | Aufrufer **und** Modelle (Breite, Stromkreise) |

⚠️ **Vier normwissen-Auskünfte ohne Konsument** — das ist ein Muster, kein
Einzelfall. Der Integrationsauftrag an @mvpo3 deckt sie gemeinsam ab.

### Abhängigkeiten von fehlenden Primärquellen

| Fehlende Quelle | blockiert |
|---|---|
| **ÖVE/ÖNORM E 8002-1:2002** | E07-Funktionserhalt-Dauer, Schalterbegriff § 7.7.14 |
| **ÖVE/ÖNORM E 8002-1:2007** | E06-Definition + Schutzziel |
| **ÖVE-EN 1 Teil 4 §§ 50/90:1991** | Inhalt der E05-Installationsbestimmungen |
| **TRVB B 108** | Begriff „Unterbrandabschnitt" (E07) |
| **ÖNORM B 1800** | Netto-Grundfläche (OIB Zeilen 2, 10) |
| **EN 81-20 / EN 81-72 / TRVB 150 S** | Aufzug/Schacht (Deckungsmatrix) |
| **AStV-Zweitausdruck** | Ausgabenvergleich K1 |

### Was die Engine durch diesen Arbeitsblock zusätzlich kann

* Sie **benennt** im Prüfbericht/Header die drei AStV-Tatbestände, ihre Grenzen
  und das Wahlrecht — statt eines pauschalen Satzes.
* Sie **verwechselt nichts mehr**: Z 3 ≠ `besondere_gefaehrdung`, E06-0,5 s ≠
  EN-1838-Umschaltzeit, „brandgefährdet" (E05) ≠ OIB-Garagenschwelle,
  20 Leuchten je Endstromkreis ≠ 20 Leuchten je Gebäudeteil, RL-4-Mindestbreite ≠
  gemessene Breite. Jede dieser Trennungen ist durch einen Test gesichert.
* Sie **kennt ihre Grenzen belegt**: zu jeder nicht umgesetzten Regel steht,
  welche Angabe fehlt und wer sie liefert.
* **Nicht** hinzugekommen ist eine neue Entscheidung oder Platzierung.

## 5e. Bestandsaufnahme je Dokument (2026-09-08, zweite Runde)

Verweist auf die bestehenden Audits statt sie zu wiederholen:
Dateiverzeichnis → `QUELLENWIRKUNG_2026-09-07.md` Kap. 1 · Wirkungsketten → dort
Kap. 2 · Themen → Abschnitte 4, 5a–5c dieser Datei.
**Spalte „Verbraucher" nennt nur, was die Engine wirklich aufruft.** Eine
Wissensdatei ohne Aufrufer steht als **„keiner"** — nicht als integriert.

### `knowledge/Österreichische Rechtsquelle/`

| Dokument | relevant | begründet ausgeschlossen | Umsetzung | Verbraucher | Blockade |
|---|---|---|---|---|---|
| **AStV** (RIS 06.09.2026) | § 1 Abs. 1–4 · § 9 Abs. 1–4 · § 13 | übrige §§ (Sanitär, Raumhöhen, Verkehrswege …) — kein Beleuchtungstatbestand | `astv_arbeitsstaetten.yaml` + `astv.py` + Hinweistext | **Hinweistext**: `_astv_hinweise` → `OibBefund` → Header. **`astv.py`: keiner** | Eingaben (Z 1–Z 3, Abs. 4, Zuordnung) + Aufrufer |
| **ASchG** (RIS 06.09.2026) | § 19 (Arbeitsstätten-Begriff), § 94 (Behördenpfad) | Rest — Arbeitnehmerschutz allgemein | nur zitiert | keiner | — |
| **RIVOPLAN-Zusammenfassung** | — | **Sekundärquelle**, nicht amtlich | **keine** | keiner | wird nicht als Beleg verwendet |

### `knowledge/OVE-Fachinformation/`

| Dokument | relevant | begründet ausgeschlossen | Umsetzung | Verbraucher | Blockade |
|---|---|---|---|---|---|
| **E08** Arbeitsstätten | Tab. 1 · Abschn. 4 · 5.1–5.3 · 6 | — | `astv_arbeitsstaetten.yaml` | Hinweistext · ⚠️ **`pipeline._coverage`** (20-Leuchten-Hinweis, Quelle ist aber **OVE E 8101 560.9.001.AT**, Ebene C) | Belichtungsangabe (Tab. 1) · **Bezugseinheit** des 20er-Hinweises (5.2/560.9.001.AT) · Bezugsfläche (5.3) |
| **E07** Funktionserhalt | Einl. · Abschn. 1 · 2.1–2.3 · Bilder 1–6 | — | `ove_e07_funktionserhalt.yaml` | **keiner** | Brandabschnitte · Stromkreise · Verteiler · **TRVB B 108** · **E 8002-1:2002** |
| **E06** Bussysteme | Abschn. 1 · 2.1–2.3 | — | `ove_e05_e06_anlagen.yaml` | **keiner** | **E 8002-1:2007**; Funktionsbereich Anlagentechnik |
| **E05** Garagen | ganze Seite (1 S.) | — | dito | **keiner** | **ÖVE-EN 1 Teil 4 §§ 50/90:1991**; betrifft Installation, nicht Notlicht |
| E01–E04, E09–E13, H02, `fachmeinung04`, `klemmen`, `8001_2`, `OVE-IM12` | — | Licht-/Steckdosenstromkreise, E-8001-Korrekturen, USV, Ableitströme, SPD, Spannungsabfall, Voruntersuchungen, Kabel/Leitungen, Klemmen — **kein Notbeleuchtungs-Tatbestand** | keine | keiner | — |

### `knowledge/OIB-Richtlinien/`

| Dokument | relevant | begründet ausgeschlossen | Umsetzung | Verbraucher | Blockade |
|---|---|---|---|---|---|
| **RL 2** + Erl. (Mai 2023 **und** April 2019) | Punkt 5.4 · **Tabelle 6** (18 Zeilen) · Erl. zu 5.4 (AStV-Pfad) | übrige Kapitel (Bauteile, Abstände) | `oib_rl2_tabelle6.yaml` | **`oib/tabelle6.py` → `pipeline:bewerte_oib`** — **echter Verbraucher** | Zeile 10 (AStV-Auswertung) · Netto-Grundfläche (**ÖNORM B 1800**) |
| **RL 2.1 / 2.2 / 2.3** | 3.6.5 · 5.5.3 + Tab. 3 Z. 8.2 · 2.14 | Rest | über RL 2 abgebildet (Zeile 11.1 mit Bändern) | dito | — |
| **RL 4** (Mai 2023) | **Vorbemerkungen** (Anwendungsbereich, Fertigmaß, Personenzahl) · Kap. 2.4/2.5/2.7/2.8 | Kap. 3–8 (Absturzsicherung, Blitzschutz, Barrierefreiheit im Detail) — kein Notlicht-Bezug | `oib_rl4_fluchtwegbreiten.yaml` | **keiner** | gemessene Breite je Abschnitt · Personenzahl je Abschnitt · Türmaß-Semantik |
| **RL Begriffsbestimmungen** · **Zitierte Normen** | Netto-Grundfläche, Fluchtweg-Begriff, Ausgabestände | Rest | als Fundstelle zitiert | mittelbar über RL 2 | **ÖNORM B 1800** |
| RL 1 · 3 · 5 · 6 · 7 | — | Tragwerk · Hygiene („beleuchtbar", kein Notlicht) · Schall · Energie · Grundlagendokument | keine | keiner | — |

### Zusammenfassung in einer Zeile

Von **65 Quelldateien** wirken heute in die Ausgabe: die **OIB-RL-2-Familie**
(über `bewerte_oib`), der **AStV/E08-Hinweistext** (über `_astv_hinweise`) und —
⚠️ **nachgetragen 2026-09-08** — der **20-Leuchten-Hinweis in
`pipeline.py::_coverage`**, dessen Fundstelle **OVE E 8101 560.9.001.AT**
(Ebene C, 2019 und 2025) korrekt ist, dessen **Bezugseinheit** aber ungeklärt
bleibt (gezählt wird ein Geschoss, die Norm meint den zusammenhängenden
Gebäudeteil). Alles Übrige ist aufbereitet, aber **ohne Aufrufer** — die
Integration bleibt der Engpass.

## 5f. Beleg der Aussage „die drei Ordner sind ausgewertet" (bereinigt)

Gezählt am 2026-09-08 **auf Dateiebene**, ohne `.DS_Store`. **Ausgewertet heißt:
Volltext gelesen und Ergebnis in einer Wissensdatei oder einem Bericht** —
**nicht** „von der Engine genutzt" (dazu 5e).
⚠️ **Korrektur der ersten Fassung:** dort standen „27 + 38 = 65" **und**
zusätzlich „2 blockiert" — das ging nicht auf. Richtig ist die Aufteilung unten;
die blockierten Dokumente sind eine **Teilmenge der ausgewerteten**, keine
eigene Kategorie, und **zwei Dateien waren gar nicht bearbeitet**.

### Basis A — Dateien im Arbeitsbaum: **65**

| Ordner | Dateien | ausgewertet | begründet ausgeschlossen | **noch nicht bearbeitet** |
|---|---|---|---|---|
| `OIB-Richtlinien/` | **47** | **23** — RL 2 Brandschutz (5) · RL 2.1 (3) · RL 2.2 (3) · RL 2.3 (3) · RL 4 (3) · Begriffsbestimmungen (2) · Zitierte Normen (4) | **22** — RL 1 (5) · RL 3 (3) · RL 5 (3) · RL 6 (7) · RL 6 Leitfaden (3) · RL 7 (1): Tragwerk, Hygiene, Schall, Energie, Grundlagendokument — kein Notbeleuchtungs-Tatbestand (Audit K3) | **2** — „OIB-Richtlinie 2 Abweichungen im Brandschutz und Brandschutzkonzepte" |
| `OVE-Fachinformation/` | **17** | **4** — E05 · E06 · E07 · E08 | **13** — E01–E04, E09–E13, H02, `fachmeinung04`, `klemmen`, `8001_2`, `OVE-IM12` | 0 |
| `Österreichische Rechtsquelle/` | **1** | 0 | **1** — RIVOPLAN-Zusammenfassung: Sekundärquelle, nicht amtlich, wird nicht als Beleg verwendet | 0 |
| **Summe** | **65** | **27** | **36** | **2** |

**27 + 36 + 2 = 65.** ✔

### Basis B — zusätzlich außerhalb des Arbeitsbaums

Vier amtliche Dateien liegen **nur** auf `enis/sanitaer-beleuchtungsart-0906`
(`ee55445`): AStV-Volltext + § 9-Auszug, ASchG-Volltext + § 19-Auszug — **alle
vier ausgewertet**. Vereinigungsmenge: **69 Dateien, davon 31 ausgewertet**.

### Teilmengen und eigene Vorgänge — ausdrücklich getrennt

| | Zuordnung |
|---|---|
| **Begriffsbestimmungen (2) + Zitierte Normen (4)** | **Teilmenge der 27 ausgewerteten.** Sie sind gelesen und zitiert; blockiert ist nur die **Weiterverwendung** der Netto-Grundflächen-Kette (**ÖNORM B 1800** fehlt). **Nicht zusätzlich zählen.** |
| **„OIB-Richtlinie 2 Abweichungen im Brandschutz und Brandschutzkonzepte" (2)** | **eigene Kategorie: noch nicht bearbeitet.** Zu prüfen ist, ob Abweichungs-/Brandschutzkonzepte einen Notbeleuchtungsbezug haben. **Der einzige unbearbeitete Rest der drei Ordner.** |
| **AStV-Ausgabenvergleich (K1)** | **eigener offener Vorgang, kein Dokument.** Der zweite RIS-Ausdruck (Fassung 30.08.2026) fehlt; ohne ihn keine Aussage über Rechtsänderungen. Zählt in **keiner** Dateispalte. |

**Damit ist die Aussage präzise:** die drei Ordner sind **bis auf zwei Dateien**
ausgewertet; von den 65 Dateien im Arbeitsbaum sind **27 ausgewertet**, **36
begründet ausgeschlossen**, **2 offen**. Dazu ein offener Vorgang
(Ausgabenvergleich) und eine blockierte Weiterverwendung (ÖNORM B 1800).
⚠️ **Keine dieser Zahlen sagt etwas über die Nutzung durch die Engine** — dazu 5e.

## 6. Nächster Quellenblock

~~1. OVE-Fachinformation E-07~~ → **erledigt** (Abschnitt 5a).
~~2. OIB RL 4 Kapitel 2~~ → **erledigt** (Abschnitt 5b).
~~3. E-05~~ und ~~4. E-06~~ → **erledigt** (Abschnitt 5c).
5. **OIB-RL 2 Begriffsbestimmungen / Zitierte Normen** — Netto-Grundflächen-Kette;
   ⚠️ endet bei **ÖNORM B 1800** (fehlt) → voraussichtlich nur Dokumentation.
6. **Danach ist der vorhandene Bestand ausgewertet.** Der nächste sinnvolle
   Schritt ist keine weitere Quelle, sondern die **Integration** der aufbereiteten
   Regeln (Abschnitt 5d) bzw. die **Beschaffung** der sieben fehlenden Quellen.
