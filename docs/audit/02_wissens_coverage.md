# 02 — Wissens-Coverage-Audit (A2)

**Frage:** Welches Normwissen ist WIRKLICH in der Engine aktiv, welches ist totes
Wissen (existiert in YAML/Regel, wird aber von KEINEM Codepfad zur Laufzeit gelesen)?

**Scope:** die 8 `src/notbeleuchtung/normwissen/data/*.yaml` + ihre Konsumenten im
Code + die für Platzierung/Lichtberechnung relevanten Regel-IDs. `knowledge/`
(P2, s. letzter Abschnitt) ist Prosa-Digest, kein Engine-Input.

**Methode:** Für jeden YAML-Schlüssel wurde der Konsum-Pfad gegrept (Provider-
Methode → Aufrufer in `platzierung/` bzw. `hauptengine/`). Ein Wert gilt als
**zur Laufzeit gelesen = ja** nur, wenn ein Aufruf aus einem produktiven Codepfad
(Pipeline/Platzierung/Validierung/Render) ihn erreicht. Aufrufe nur aus Tests oder
nur aus dem eigenen Provider-Modul (ohne externen Konsumenten) zählen als **nein**.

---

## A. Der harte Befund: was die Engine zur Laufzeit vom NormProvider abruft

Grep über `src/notbeleuchtung/platzierung/**` + `hauptengine/**` zeigt: von der
gesamten `NormProvider`-API werden produktiv NUR diese vier Methoden aufgerufen
(alle im offiziellen `ports.NormProvider`-Protocol, `ports.py:46-52`):

| Methode | Aufrufer (Beleg) |
|---|---|
| `fuer_raum(raum_typ, ist_fluchtweg)` | `gang_strategy.py:106`, `flaechen_strategy.py:168`, `deckung.py:95`, `fachpraxis.py:140`, `sonderstellen_strategy.py:177`, `lux_nachweis.py:101`, `render/lux_nachweis_bericht.py:91` |
| `fuer_fluchtweg_abschnitt(seg)` | `anker_strategy.py:112,223`, `communal_stgh_strategy.py:78`, `fachpraxis.py:296` |
| `erkennungsweite_m(h, hinterleuchtet)` | `deckungs_zuordnung.py:72`, `anker_strategy.py:217`, `fachpraxis.py:322` |
| `regelwerk_snapshot()` | `validierung.py:100`, `flaechen_strategy.py:46,148`, `bausteine.py:98` |

Die `OibRl2Provider.bewerte_oib` (`pipeline.py:187`) und `OveZusatzKatalog`
(`validierung.py:397-400`) werden ebenfalls produktiv aufgerufen.

**Alles andere am NormProvider ist tot** (kein produktiver Aufrufer, nur eigenes
Modul + Tests): `weg_nachweis`, `antipanik_randstreifen_mm`,
`antipanik_randstreifen_quelle`, `hat_at_abweichung`, `fuer_sonderstelle`,
`zur_pruefung`, `fuer_raum_attribut` — bestätigt durch Grep
`\.fuer_sonderstelle\(|\.zur_pruefung\(|\.fuer_raum_attribut\(|\.weg_nachweis\(|\.antipanik_randstreifen|\.hat_at_abweichung\(`
über `src/` → **No files found**. Diese sind laut Docstring (`provider.py:150-221`)
bewusste PROTOTYPEN, nicht im Protocol.

---

## B. en1838_grundwerte.yaml — Zeile für Zeile

Geltungs-Tag: alle EN-1838-§-Werte sind [AT-verbindlich] (ÖNORM EN 1838 ist in AT
verbindlich übernommen; die Datei selbst führt keine AT-A-Abweichung, `:104`).

| Schlüssel | Aussage | Typ | Tag | in Engine | Fundstelle YAML | Konsum-Pfad | gelesen |
|---|---|---|---|---|---|---|---|
| `norm` | "ÖNORM EN 1838:2013" | Wert | [AT-verbindlich] | ja | `:33` | `provider.py:411` → `NormRegelwerk.norm` | ja |
| `montagehoehe_min_mm: 2000` | Leuchten ≥2 m (§4.1.1 Floor) | Wert | [AT-verbindlich] | ja | `:38` | `provider.py:142-144` `_montagehoehe` → jede Anforderung | ja |
| `dauer_min: 60` | Notbetriebsdauer ≥60 min | Wert | [AT-verbindlich] | ja | `:41` | `provider.py:135` → `NormAnforderung.dauer_min` | ja |
| `erkennungsweite.z_hinterleuchtet: 200` | z-Faktor hinterleuchtet (§5.5) | Wert | [AT-verbindlich] | ja | `:45` | `provider.py:147-148,389,414` | ja |
| `erkennungsweite.z_beleuchtet: 100` | z-Faktor beleuchtet (§5.5) | Wert | [AT-verbindlich] | ja | `:46` | `provider.py:389,415` (`erkennungsweite_m` false-Zweig) | ja |
| `erkennungsweite.piktogramm_hoehe_default_m: 0.15` | RZ-Höhe 150 mm [PRAXIS] | Wert | [AT-Referenzpraxis] | ja | `:49` | `provider.py:148` → Default-Erkennungsweite 30 m | ja |
| `lux.rettungsweg: 1.0` | Mittellinie 1 lx (§4.2.1) | Wert | [AT-verbindlich] | ja | `:55` | `provider.py:97-98` `_lux` via `min_lux_ref` | ja |
| `lux.antipanik: 0.5` | Antipanik 0,5 lx (§4.3.1) | Wert | [AT-verbindlich] | ja | `:58` | `provider.py:97-98` via `min_lux_ref` | ja |
| `geometrie.rettungsweg.max_breite_mm: 2000` | Geltungsbereich Mittellinie | Wert | [AT-verbindlich] | **nein** | `:72` | nur `provider.py:161-174` `weg_nachweis` — **kein produktiver Aufrufer** | **nein** |
| `geometrie.rettungsweg.mittelbereich_breite_anteil: 0.5` | halbe Wegbreite | Wert | [AT-verbindlich] | **nein** | `:76` | `weg_nachweis` (tot) | **nein** |
| `geometrie.rettungsweg.mittelbereich_lux_anteil: 0.5` | 50 % v. 1 lx | Wert | [AT-verbindlich] | **nein** | `:77` | `weg_nachweis` (tot) | **nein** |
| `geometrie.rettungsweg.breiter_weg_optionen[]` | Streifen 2 m / Antipanik | Trigger | [AT-verbindlich] | **nein** | `:82-84` | `weg_nachweis` (tot) | **nein** |
| `geometrie.rettungsweg.breiter_weg_entscheidung: planer` | KANN-Regel | Trigger | [AT-verbindlich] | **nein** | `:85` | kein Konsument gefunden | **nein** |
| `geometrie.antipanik.randstreifen_mm: 500` | 0,5-m-Rand (§4.3.1) | Geometrie | [AT-verbindlich] | **nein** | `:96` | nur `provider.py:202` `antipanik_randstreifen_mm` — **kein produktiver Aufrufer** | **nein** |
| `geometrie.antipanik.randstreifen_gilt_fuer` | Zuordnung Kernbereich | Wert | [AT-verbindlich] | **nein** | `:97` | kein Konsument gefunden | **nein** |
| `anhang_b_at_abweichung: false` | keine AT-A-Abweichung | Trigger | [AT-verbindlich] | **nein** | `:104` | nur `provider.py:209` `hat_at_abweichung` — **kein produktiver Aufrufer** | **nein** |
| `gleichmaessigkeit.rettungsweg: 40.0` | Ud 1:40 (§4.2.2) | Wert | [AT-verbindlich] | ja | `:112` | `provider.py:110-111` via `gleichmaessigkeit_ref` → `NormAnforderung.gleichmaessigkeit_max` | ja |
| `gleichmaessigkeit.antipanik: 40.0` | Ud 1:40 (§4.3.2) | Wert | [AT-verbindlich] | ja | `:116` | `provider.py:110-111` (SAAL/AUFENTHALTSRAUM Regeln) | ja |
| `umschaltzeit.vollwert_s: 60.0` | 100 % in 60 s (§4.2.6) | Wert | [AT-verbindlich] | ja | `:130` | `provider.py:120` `_umschaltzeit` → `NormAnforderung.umschaltzeit_max_s` | ja |
| `umschaltzeit.halbwert_s: 5.0` | 50 % in 5 s | Wert | [AT-verbindlich] | **nein** | `:131` | Kommentar sagt selbst "kein Contract-Feld"; kein Konsument | **nein** |
| `quellen.rettungsweg/antipanik/sicherheitsleuchte` | Audit-Fundstellen | Wert | [AT-verbindlich] | ja | `:151-157` | `provider.py:100-101` `_quelle` via `quelle_ref` → `NormAnforderung.quelle` + Snapshot-quellen | ja |

**Nicht modelliert (bewusst leer, gar kein YAML-Wert):** `flaechen_schwellen`
(§ 60/8 m²) und `arbeitsplatz_lux` — Kommentar `:136-147`. Das Contract-Feld
`flaechen_schwellen` WIRD zur Laufzeit gelesen (`flaechen_strategy.py:148`), ist
aber immer leer → der Flächen-Trigger ist auf echten Daten inert (No-op).
`arbeitsplatz_lux` wird in `validierung.py:346` nur als "ungefüllt"-Hinweis erwähnt.

---

## C. raumtyp_regeln.yaml — vollständig aktiv

| Schlüssel | in Engine | gelesen | Beleg |
|---|---|---|---|
| `default` (klassifikation/min_lux_ref/quelle_ref/gleichmaessigkeit_ref/montagehoehe_mm/mindest_anzahl/symbol_katalog_keys) | ja | ja | `provider.py:380` (Fallback in `fuer_raum`) |
| `regeln[]` STIEGENHAUS / GANG / SAAL / AUFENTHALTSRAUM (alle Felder) | ja | ja | `provider.py:84-87` Index → `fuer_raum` + `_snapshot` (`:395-402`) |

Alle 4 Regeln + default werden über den `(raum_typ, ist_fluchtweg)`-Index
aufgelöst. `montagehoehe_mm: 2400` [ANNAHME], `mindest_anzahl` [ANNAHME] werden
gelesen und wirken. **Kein totes Feld in dieser Datei.** Tag durchweg
[AT-Referenzpraxis] für die Raumtyp→Klassifikation-Zuordnung (Engineering-Auslegung,
`:24-25`), die Lux/Ud/Dauer-Werte dahinter sind [AT-verbindlich].

---

## D. platzierung_regeln.yaml (Decision-Matrix) — GESAMT TOT als Laufzeit-Wissen

`PlatzierungsRegelwerk` (`platzierungsregeln.py`) ist die Query-API über diese
Datei. Grep `PlatzierungsRegelwerk` über `src/`: Vorkommen NUR in
`normwissen/__init__.py` (Export), `sonderstellen.py:410` (`_pruefe_regel_ids` —
Selbst-Guard beim YAML-Laden) und im eigenen Modul. **Kein Aufruf aus
`platzierung/` oder `hauptengine/`.** Die 25 RZ-/SL-/Hard-Stop-Regeln (RZ-01…RZ-11,
SL-01…SL-14, HS-01…HS-04) werden vom Platzierer NICHT über diese Matrix konsumiert
— der Platzierer implementiert seine Logik in `platzierung/*_strategy.py` direkt
gegen `NormAnforderung` aus `fuer_raum`/`fuer_fluchtweg_abschnitt`.

| Regel-Gruppe | Aussage (kurz) | Typ | Tag | in Engine (Verhalten) | gelesen (via diese YAML) |
|---|---|---|---|---|---|
| RZ-01…RZ-04, RZ-07…RZ-10 | RZ an Ausgang/Richtung/Kreuzung/Treppe/Sichtachse | Trigger/Geometrie | [AT-verbindlich] §4.1.2 | Verhalten in `anker_strategy`/`gang_strategy` real umgesetzt | **nein** (Regel-Text nicht gelesen) |
| RZ-05, RZ-07 (stair_exit) | Treppe/Stiegenhaus | Trigger | [AT-verbindlich] | `engine_status: teilweise` — Raumerkennung liefert kein `stair`-Node | nein |
| RZ-06 (Niveauänderung) | RZ an Niveausprung | Trigger | [AT-Referenzpraxis]/[LB] | `input_fehlt` — kein RaumModell-Merkmal | nein |
| SL-01, SL-02, SL-09 | Fluchtweg/Treppe/Antipanik | Trigger | [AT-verbindlich] | Verhalten real (gang/flaechen strategy) | nein |
| SL-03, SL-14, RZ-11 | Kreuzung/Widerspruch/Fluchtweg-unklar | Trigger | [AT-verbindlich]/Auslegung | teilweise | nein |
| SL-04, SL-05, SL-06, SL-07, SL-08, SL-10, SL-11 | Niveau/Erste-Hilfe/Feuerlöscher/Hydrant/Melder/barrierefrei-WC/Gefährdung | Trigger + Lux 5 lx vert. / 15 lx | [AT-verbindlich] §4.1.2 h/i, §4.3.8, §4.4.1 | `input_fehlt` — RaumModell trägt Stellen/Attribute nicht | nein |
| SL-12 (GARAGE), SL-13 (TECHNIK/LAGER/KELLER/MUELLRAUM) | LB-Regel Nebenräume | Trigger | [LB] | `unterstuetzt` — aber Verhalten kommt aus LB-Pfad, nicht aus dieser YAML | nein |
| HS-01 Montagehöhe 2000 | Hard Stop | Wert | [AT-verbindlich] | Wert kommt aus en1838 `montagehoehe_min_mm` (aktiv), nicht aus dieser Regel | nein |
| HS-02…HS-04 | Betriebsdauer/LB-Exklusion/geratene Richtung | Trigger | [AT-verbindlich]/Auslegung | Hard-Stop-Text nicht maschinell konsumiert | nein |

**Wichtig:** Das *Verhalten* vieler dieser Regeln existiert in der Engine (die
Platzierer setzen RZ an Ausgängen etc.), aber **die YAML-Datei selbst ist nicht der
Datenlieferant dafür** — sie ist Doku/Contract-Kandidat. `decision_sources` (Rang-
Hierarchie), `blockiert_durch_contract`, `umsetzbar`, `review_faelle`, `gewinner`
werden nur in Tests aufgerufen. Als *gelesenes Laufzeit-Wissen* = **komplett tot**.

---

## E. sonderstellen.yaml — TOT (Prototyp, nie verdrahtet)

`SonderstellenKatalog` wird in `provider.py:90` instanziiert und in `_snapshot`
(`:408`) für `quellen()` konsumiert — d.h. die **Quellen-Strings** der Sonderstellen
fließen in `NormRegelwerk.quellen` (Naht-Invariante). Das ist der EINZIGE aktive
Konsum-Pfad. Die eigentlichen Anforderungs-Methoden (`fuer_sonderstelle`,
`zur_pruefung`, `fuer_raum_attribut`, `norm_anforderung_roh`, `bewerte`) haben
KEINEN produktiven Aufrufer (Grep: no files).

| Schlüssel | Aussage | Tag | in Engine | gelesen |
|---|---|---|---|---|
| `norm_anforderung.typen.*.quelle` (feuerloescher/hydrant/erste_hilfe/brandmelder/niveauaenderung) | §4.1.2 h/i/c Fundstellen | [AT-verbindlich] | teilweise | **ja** — nur als String in `quellen()` → Snapshot (`provider.py:408`) |
| `norm_anforderung.raum_attribute.*.quelle` (ist_barrierefrei §4.3.8, besondere_gefaehrdung §4.4.1) | Fundstellen | [AT-verbindlich] | teilweise | **ja** — via `quellen()` |
| `sonderstellen_typen[].lux_anforderung.norm_wert: 5.0` (4×) | 5 lx vertikal am Gerät | Wert | [AT-verbindlich] | **nein** | `norm_lux_vertikal` nur in `_baue`/`_lux_anforderung`, die kein produktiver Pfad ruft |
| `sonderstellen_typen[].max_horizontal_zum_punkt_mm: 2000` | 2-m-Regel | Geometrie | [AT-verbindlich] | **nein** | `max_abstand_mm` — kein Aufrufer |
| `raum_attribute[].aktiviert_regeln`, `norm_ref`, `beleg`, `datenquellen` | Contract-Vorschlag-Metadaten | — | [AT-verbindlich] | **nein** | nur Tests/eigenes Modul |
| `norm_anforderung.raum_attribute.ist_barrierefrei.raumtypen_eindeutig [WC,TOILETTE]` | Toiletten-Scope | Trigger | [AT-verbindlich] | **nein** (via YAML) | `gilt_nur_fuer_raumtypen` — kein Aufruf; ABER die Logik ist in `sonderstellen_strategy.py:180` als `_TOILETTEN_TYPEN` **hartkodiert dupliziert** |
| `raum_attribute.besondere_gefaehrdung.lux_mindestwert: 15.0 / lux_anteil: 0.10` | §4.4.1 15 lx / 10 % | Wert | [AT-verbindlich] | **nein** | `_lux_anforderung` arbeitsflaeche-Zweig — kein Aufrufer |
| `beobachtet_ohne_regel`, `datenquellen.*.erkannt_heute` | Doku | — | — | **nein** | Tests |

**Kern-Widerspruch:** Die §4.3.8- und §4.4.1-Anforderungen WERDEN in der Engine
umgesetzt — aber über `sonderstellen_strategy.py:144-191` (`plan_flag_raeume`), das
`Raum.ist_barrierefrei`/`besondere_gefaehrdung` direkt liest und `norm.fuer_raum`
statt der Sonderstellen-Prototyp-API nutzt. Der Toiletten-Scope `[WC, TOILETTE]`
ist dort als Python-Konstante dupliziert, NICHT aus dieser YAML gezogen → die
`raumtypen_eindeutig`-Werte sind totes Wissen, obwohl gleichlautende Logik lebt.

---

## F. oib_rl2_tabelle6.yaml — AKTIV (Befund-Pfad)

`OibRl2Provider` liest die Datei (`oib/provider.py:45-47`), `bewerte_oib` läuft in
der Pipeline (`pipeline.py:187`). Alle Zeilen (1.1…12.2), `auswahl`,
`voraussetzungen`, `entscheidung`, `unsicherheiten`, `review_nutzungsarten`,
`jurisdiktion`, `ausfuehrungs_verweise`, `astv_parallelpfad`, `hinweise_global`
werden von `tabelle6.py` + `provider.py:75-152` konsumiert.

| Schlüssel-Gruppe | Tag | gelesen | Beleg |
|---|---|---|---|
| `zeilen[]` (alle 15 Zeilen, Schwellen/Bänder) | [AT-verbindlich] | ja | `provider.py:48,110` → `tabelle6.waehle_zeile/werte_zeile_aus` |
| `review_nutzungsarten`, `jurisdiktion`, `astv_parallelpfad`, `ausfuehrungs_verweise`, `hinweise_global` | [AT-verbindlich] | ja | `provider.py:101,130,145,95-96` |
| `meta.*` (quelle, norm_ausgabe, fundstelle_seite) | [AT-verbindlich] | ja | `provider.py:47,89-91` |

**Einschränkung des Effekts:** `bewerte_oib` produziert einen `OibBefund`; dieser
gibt NIE `nicht_erforderlich` zurück (fail closed) und **platziert selbst keine
Leuchte** — er speist Prüfbericht (`validierung.py`) und den Flächen-Trigger-Gate
(`flaechen_strategy.py`, der aber wg. leerer `flaechen_schwellen` inert ist). Das
Wissen ist gelesen, aber sein Placement-Effekt ist heute Null. **Kein totes Feld,
aber wirkungsschwach.**

---

## G. ove_e8101_zusatz.yaml — AKTIV (Befund-Pfad, ein Fall)

`OveZusatzKatalog` in `validierung.py:397-441` konsumiert produktiv:
`quellen`, `belegte_faelle[verkaufsstaette_sanitaer]` (nutzungsart/oib_stufe/
kennzahl/bereich/offen), `passt_zur_geprueften_oib_ausgabe`, `ist_belegte_nutzung`,
`kennzahl_erfuellt`, `bereich_erfuellt`, `begruendung`, `offene_punkte`.

| Schlüssel | Tag | gelesen | Beleg |
|---|---|---|---|
| `belegte_faelle[0]` (Verkaufsstätte Sanitär >3000/≥8 m²) | [AT-verbindlich] | ja | `validierung.py:415-438` |
| `quellen.{ove_e8101,r12_2,oib_rl2}` | [AT-verbindlich] | ja | `ove_zusatz.py:64-76,95` → `validierung.py:441` |
| `ausgaben_pruefung.vorpruefungs_satz` | [AT-verbindlich] | teilw. | `ove_zusatz.py:115` `vorpruefungs_satz` — kein produktiver Aufrufer (nur Test) → **nein** |
| `nicht_uebertragbar.ove_e8101_2025` | [AT-verbindlich] | **nein** | `hinweis_2025()` kein produktiver Aufrufer |
| `ausgaben_pruefung.{oib_rl2,ove_e8101,r12_2}` (Status-Dict) | — | **nein** | `ausgaben_pruefstatus()` kein Aufrufer |

Produziert nur einen Befund ("erforderlich"), platziert nichts (`ove_zusatz.py:11`).

---

## H. lb_extraktion.yaml — AKTIV (LB-Parser)

Der LB-Parser (`normwissen/lb/parser.py`, `felder.py`, `struktur.py`) wird in
`pipeline.py:179` (`bundle.lb.parse_lb`) produktiv aufgerufen. Grep bestätigt
Konsum von `raum_typ_vokabular`, `unterstuetzte_raum_typen`, `batterie_standort`,
`funktionserhalt_muster`, `piktogramm_muster`, `norm_bezug`, `sonder_lux`,
`rz_stellen`, `negation_muster`, `inklusion_muster`, `begruendung_muster`,
`eigene_vorgabe_felder`, `sl_abschnitt_anker`, `dokument_arten`, `abschnitt_muster`
in `struktur.py` + `parser.py` + `felder.py`.

| Schlüssel-Gruppe | Tag | gelesen |
|---|---|---|
| `struktur.*`, `dokument_arten`, `verweise`, `eigene_vorgabe_felder`, `sl_abschnitt_anker/ausschluss` | [AT-Referenzpraxis] (LB-Parsing-Heuristik) | ja |
| `felder.{betriebsdauer_min,umschaltzeit_max_s,mindest_lux_fluchtweg}` | [AT-Referenzpraxis] | ja |
| `enums.{system_typ,ueberwachung,pruefung}` | [AT-Referenzpraxis] | ja |
| `rz_stellen`, `sonder_lux`, `batterie_standort`, `piktogramm_muster`, `norm_bezug`, `funktionserhalt_muster` | [AT-Referenzpraxis] | ja |
| `raum_typ_vokabular`, `unterstuetzte_raum_typen`, `negation_muster`, `inklusion_muster`, `begruendung_muster` | [AT-Referenzpraxis] | ja |

**Kein totes Feld** — alle Muster werden vom Parser geladen. (Ob der LB-Pfad in
einem konkreten Lauf feuert, hängt vom Input ab; die YAML ist aber vollständig
verdrahtet.)

---

## I. regel_deckung.yaml — TOT als Laufzeit-Wissen (Test-only Guard)

Grep `regel_deckung` über `src/` → nur die YAML selbst. **Kein Python-Konsument in
`src/`.** Die Datei wird ausschließlich von `tests/naht/test_regel_deckung.py`
gelesen (Guard: jeder Kanon-Raumtyp genau ein Eintrag, jede referenzierte Regel-ID
existiert). Ihr Inhalt (`deckung.STIEGENHAUS…WASCHKÜCHE`, `bewusst_keine`, `offen`)
beeinflusst KEINE Platzierung zur Laufzeit.

| Schlüssel | Tag | in Engine | gelesen |
|---|---|---|---|
| `deckung.*` (22 Kanon-Typen) | [AT-Referenzpraxis] | nein (Test-Guard) | **nein** (kein src-Konsument) |

Einordnung: kein „falsches" totes Wissen — es ist bewusst ein CI-Guard, kein
Engine-Input. Aber nach der strengen Definition der Aufgabe: **nicht zur Laufzeit
gelesen = NEIN**.

---

## J. knowledge/ (P2 Prosa)

`knowledge/extracted/*.md` (EN_1838_notbeleuchtung.md, GSYSTEMS_…, Kaufel_…,
LICHTBERECHNUNG_REFERENZ.md, PROFI_DIN_PLAN_…, PLATZIERUNGS_KONZEPTE.md etc.) und
`knowledge/INDEX.md` sind **Digests/Prosa**, kein Engine-Input. `INDEX.md:4-5` sagt
selbst: „Norm-Werte niemals aus dem Index zitieren — immer der autoritativen
YAML/dem Contract folgen." Grep nach Code-Referenzen auf `knowledge/` aus `src/`:
keine (nur `scripts/wissen_index.py` generiert den Index). Die ~1097 Regel-IDs des
Korpus (OVE8101/GSYS/HB2026/ONL/EN1838/LW10…) leben ausschließlich in diesen
Digests und sind **per Definition nicht in der Engine aktiv** — die Engine kennt
nur die kuratierten Werte der 8 YAMLs. Das ist by-design (Kuratierung), wird hier
aber als „nicht zur Laufzeit gelesen" verbucht.

---

## K. Zusammenfassung — Zählung

Gezählt auf Ebene sinnvoller Schlüssel-Gruppen der 8 YAMLs (nicht jede einzelne
Regel-ID der Digests):

- **AKTIV (zur Laufzeit gelesen, wirkt):** en1838 Kern-Werte (norm, montagehöhe,
  dauer, erkennungsweite z/h, lux rw/ap, gleichmäßigkeit rw/ap, umschaltzeit
  vollwert, quellen) · raumtyp_regeln (default + 4 Regeln, ALLE Felder) ·
  oib_rl2_tabelle6 (alle Zeilen + Metadaten) · ove_e8101_zusatz (belegter Fall +
  quellen) · lb_extraktion (ALLE Muster) · sonderstellen.quellen()-Strings.
  → **~6 von 8 Dateien tragen aktives Wissen.**
- **TEILWEISE:** oib + ove_zusatz (gelesen, aber nur Befund/Bericht, kein Placement;
  ove_zusatz platziert nichts, flaechen_schwellen leer → Trigger inert).
- **TOT (existiert, kein produktiver Konsument):**
  1. `platzierung_regeln.yaml` — GESAMT (25 Regeln), nur Doku/Tests.
  2. `regel_deckung.yaml` — GESAMT, nur CI-Test-Guard.
  3. `sonderstellen.yaml` — alle Anforderungs-Werte (5 lx vertikal ×4, 2-m-Abstand,
     15 lx/10 %, raumtypen_eindeutig), außer den Quellen-Strings.
  4. `en1838_grundwerte.geometrie.*` (Wegbreite/Randstreifen) + `anhang_b_at_abweichung`
     + `umschaltzeit.halbwert_s` — hängen an toten Provider-Prototypen
     (`weg_nachweis`, `antipanik_randstreifen_mm`, `hat_at_abweichung`).
  5. ove_zusatz `vorpruefungs_satz`/`hinweis_2025`/`ausgaben_pruefstatus`.

**Wichtigster systemischer Befund:** Die gesamte deklarative „WANN welche Leuchte
WO"-Matrix (`platzierung_regeln.yaml`) und der Sonderstellen-Katalog sind NICHT der
Datenlieferant der Platzierung — der Platzierer implementiert die Logik prozedural
in `platzierung/*_strategy.py` gegen `NormAnforderung`. YAML und Code können daher
auseinanderdriften (Beispiel: Toiletten-Scope `[WC,TOILETTE]` in YAML vs.
hartkodierter `_TOILETTEN_TYPEN` in `sonderstellen_strategy.py:180`). Die
Sonderstellen-§4.1.2-h/i-Werte (5 lx vertikal) sind normativ belegt, aber nirgends
zur Laufzeit gelesen — mangels RaumModell-Merkmal (`engine_status: input_fehlt`).
