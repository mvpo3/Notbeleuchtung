# A3 — Engine-IST + Lichtberechnung (Call-Graph-basiert)

Stand 2026-09-09. Alle Befunde mit Beleg `datei:zeile`, Geltungs-Tag
`[AT-verbindlich]` (ÖNORM EN 1838:2013 / OVE E 8101) · `[AT-Referenzpraxis]`
(Owner-/Fachpraxis, kein Norm-Beleg) · `[DE-only]` (deutsche Herkunft, in AT
allenfalls Referenz).

## Produktions-Call-Graph (pipeline.run → place)

```
pipeline.run                                     pipeline.py:134
 └─ _parse_raum → bundle.raum.parse              pipeline.py:122 (Selman)
 └─ _run_mit_quelle                              pipeline.py:158
     ├─ bundle.lb.parse_lb (opt)                 pipeline.py:179 (Enis)
     ├─ bundle.oib.bewerte_oib (opt)             pipeline.py:187
     ├─ bundle.platzierer.place(raum,norm,lb,oib) pipeline.py:189/191
     │   └─ NotlichtPlatzierer.place             platzierer.py:128
     │       ├─ _plan_rettungszeichen            platzierer.py:143 → :95
     │       │   ├─ kreuzungs_anker? → plan_rettungszeichen_anker  anker_strategy.py:73
     │       │   ├─ sonst plan_rettungszeichen (Segment)          communal_stgh_strategy
     │       │   ├─ sonst plan_rettungszeichen_gang               gang_strategy.py:92
     │       │   └─ _sichtlinien_garantie → plan_rettungszeichen_gang  platzierer.py:61
     │       ├─ fachpraxis.tuerleuchte_pflichtraeume  platzierer.py:150
     │       ├─ plan_sicherheitsleuchten          flaechen_strategy.py:211
     │       ├─ plan_antipanik                    flaechen_strategy.py:216 → _antipanik_punkte → lux_raster
     │       ├─ plan_sonderstellen / plan_flag_raeume  sonderstellen_strategy
     │       ├─ plan_aussenleuchten               aussen_strategy
     │       ├─ verdichte_fluchtweg               deckung.py:70 → mittellinie + lux_punkte/lux_raster/max_leuchtenabstand_mm
     │       ├─ fachpraxis.aufheller_je_rz        platzierer.py:162
     │       ├─ lb_override.anwenden             platzierer.py:166
     │       ├─ verbotszonen_nachpass            platzierer.py:170
     │       ├─ abstand_nachpass.entzerre        platzierer.py:174
     │       ├─ deckungs_zuordnung.zuordnen      platzierer.py:177 → norm.erkennungsweite_m  deckungs_zuordnung.py:72
     │       └─ circuit_zuordnung.zuordnen       platzierer.py:180
     ├─ pruefbericht                              pipeline.py:192 → validierung.pruefe
     ├─ render_dxf (nur mit out_path)             pipeline.py:197
     └─ schreibe_bericht (lux_nachweis_bericht)   pipeline.py:206 (matplotlib, additiv)
```

---

## (a) mirror_x / Pfeilrichtung — Setzen vs. Konsum

**Setzen (Platzierer):**
- Einziger Ableiter: `bausteine.key_und_rotation` → `orientation.transformation`
  liefert `(rotation_deg, mirror_x)`; `mirror_x` ist **immer `False`** —
  `transformation` gibt in allen Zweigen `False` zurück (`orientation.py:47,52`).
  Kommentar bestätigt: „Spiegelung ist nie nötig" (`bausteine.py:69-70`,
  `orientation.py:42-43`). Basisorientierungen GEMESSEN (`orientation.py:25-29`),
  drei eigene Blöcke unten/links/rechts.
- Konsumenten des Setzers: `anker_strategy.py:113`, `gang_strategy.py:133`.
  `flaechen_strategy`, `deckung`, `fachpraxis` setzen `mirror_x` gar nicht
  (Default `False`) — richtungslose bzw. `richtung="gerade"`-Leuchten.
- **Golden-Fixture** trägt durchweg `mirror_x=false` (`platzierung_4og.json`).
  [AT-verbindlich] (EN ISO 7010 Pfeilrichtung) / [AT-Referenzpraxis] (Block-Wahl).

**Konsum (Renderer/Inserter):** `inserter._skalen` (`inserter.py:40-52`):
effektive Spiegelung = `entry["mirror_x"] XOR p.mirror_x`, umgesetzt als negativer
xscale (`-scale if mirrored`). Der Mapping-Eintrag kann selbst ein `mirror_x`
tragen; der Contract-Wert wird per XOR verrechnet.

**Konvention stimmig?** JA für den Platzierer-Pfad: er setzt `mirror_x`
konsequent `False`, der Inserter spiegelt dann ausschließlich nach der
Mapping-Konvention. Der XOR-Pfad ist damit HEUTE eine reine Mapping-Angelegenheit
(Contract-Term stets 0). **Latentes Risiko:** würde je eine Strategie wieder ein
`mirror_x=True` setzen (Historie: der „mirror_x-Hack ist Geschichte",
`orientation.py:12-13`), verrechnet der Inserter es blind per XOR mit einer
evtl. schon gespiegelten Mapping-Basis — es gibt keine Absicherung, dass
Setz-Basis und Mapping-Basis konsistent sind. Für den aktuellen Code kein
Fehler, aber die zwei Konventionen (gemessene Block-Basis in `orientation` vs.
Mapping-`mirror_x` im Inserter) leben getrennt.

**Rotation:** Pfeil-zur-Tür-Formel `rotation = (round((deg(atan2(dy,dx))+90)/90)*90)%360`
lebt an DREI Stellen dupliziert: `anker_strategy.py:140`, `gang_strategy.py:143`,
`fachpraxis.py:303`. Alle nutzen dieselbe Formel (unten-Block-Basis 270°). Konsistent,
aber dreifach kopiert (Drift-Risiko bei Änderung).

## (b) erkennungsweite_m — im Produktionspfad?

`norm.erkennungsweite_m(...)` (Norm-Methode, `provider.py:387`) wird im
Produktionspfad **an genau einer Stelle** gerufen:
`deckungs_zuordnung._radius_mm` (`deckungs_zuordnung.py:72`) ← `zuordnen`
(`:76`) ← `place` (`platzierer.py:177`). Dort setzt sie den Deckungs-**Radius**
(l=z·h → 30 m hinterleuchtet) für die nachträgliche `covers_segment`-Zuordnung.

Der **`NormAnforderung.erkennungsweite_m`-Feldwert** (aus `provider.py:127`,
nur für `klass=="rz"` gefüllt via `_default_erkennungsweite_m` :146) wird
produktiv gelesen in:
- `gang_strategy._abstand_mm` (`gang_strategy.py:43,110`) — RZ-Abstand entlang
  GANG-Mittellinie (nur Fallback-Pfad, wenn weder Anker noch Segment).
- `fachpraxis.py:322` — Reichweiten-Check Türleuchte.

`plan_rettungszeichen_sichtlinie` (`anker_strategy.py:181,217`) ruft
`norm.erkennungsweite_m` DIREKT — aber diese Funktion ist **NICHT im
place()-Pfad**: `place → _plan_rettungszeichen` verzweigt nur auf
`plan_rettungszeichen_anker` / `plan_rettungszeichen` (Segment) /
`plan_rettungszeichen_gang`. `plan_rettungszeichen_sichtlinie` ist ausschließlich
in `tests/platzierung/test_sichtlinie.py` referenziert (Grep: 8 Test-Treffer,
0 Produktions-Aufrufer außer Docstring). **Toter Produktionspfad / test-only.**

Call-Graph bis zur Norm (produktiv): `place` → `deckungs_zuordnung.zuordnen`
→ `_radius_mm` → `En1838NormProvider.erkennungsweite_m` → `data/en1838_grundwerte.yaml`
(`z_hinterleuchtet` · `piktogramm_hoehe_default_m`, `provider.py:388-390`).
[AT-verbindlich] EN 1838 §5.5 (l=z·h). Anker-RZ selbst setzt seinen Abstand
NICHT über l=z·h — es setzt RZ an Graph-Ankern/Ausgängen; l=z·h greift dort erst
nachgelagert als Deckungs-Radius.

## (c) id()-gekeyter Cache

**Kein `id()`-gekeyter Cache im Repo.** Grep `id\(` über
`platzierung/**` liefert nur `np.meshgrid` (`lux.py:150`), Treffer war
`gx, gy` — kein `id()`-Builtin. Grep `_cache|lru_cache|{id(` über gesamtes
`src/**` = **0 Treffer**. Der einzige Cache ist `functools.cached_property`
`_snapshot` (`provider.py:392`) — an die Provider-Instanz gebunden, kein
`id()`-Key, kein GC-Wiederverwendungs-Risiko. **Widerlegt** — die im Prompt
vermutete Fundstelle existiert in diesem Stand nicht (evtl. bereits entfernt
oder in anderem Owner-Package/Branch).

## (d) Golden-Fixtures vs. Produktionspfad

`tests/fixtures/platzierung_4og.json` (5 RZ) wird **von KEINEM Produktionscode
geladen** (Grep `fixtures|platzierung_4og` über `src/**` = 0 Treffer) — reine
Test-Fixture. `_source`-Feld sagt selbst: „generativ vom echten
NotlichtPlatzierer erzeugt". Fixture-Werte: `catalog_key=notlicht_ks_stiege_links/
_rechts`, `rotation_deg=0.0`, `mirror_x=false`, `richtung=links/rechts`. Das ist
das **alte** Richtungs-Block-Schema (dedizierte `_links/_rechts`-Blöcke, `is_directional
→ rotation 0`), das der heutige `key_und_rotation`/`select_key`-Pfad noch bedient
(`bausteine.py:44-57`). **Keine Wert-Drift festgestellt** — das Fixture-Schema
ist mit dem produktiven `select_key`-Pfad konsistent (dedizierter Block → rot 0,
mirror False). Das Fixture deckt aber NUR RZ ab (kein SL/Antipanik/Deckung), deckt
also den Lux-getriebenen Teil des Produktionspfads gar nicht ab — dort fehlt eine
Golden-Absicherung gegen Drift.

---

## Lichtberechnung — Checkliste (implementiert / rudimentär / fehlt)

Kern-Engine: `platzierung/lux.py` (Punktmethode E = I·cos³θ/h²), konsumiert von
`deckung.verdichte_fluchtweg`, `flaechen_strategy._antipanik_punkte`,
`platzierung/lux_nachweis.py` (Reporting) und `render/lux_nachweis_bericht.py` (PDF-Seite).

### · Photometrischer Tabellen-Lookup a/b je Montagehöhe h (0,5-m-Stufe, nie interpolieren)
**FEHLT.** Die Engine nutzt KEINE a/b-Abstandstabelle je Montagehöhe. Der
Leuchtenabstand wird analytisch aus der Punktmethode bisektioniert
(`lux.max_leuchtenabstand_mm`, `lux.py:231-282`), nicht per Tabellen-Zelle
gelesen. Photometrie kommt als kontinuierliches Callable `i_cd_fn(γ,C)` aus
LDT/EULUMDAT (`normwissen/photometrie/ldt.py`) — dort wird zwischen C-Ebenen
sogar INTERPOLIERT (`ldt.py:77`). Es gibt kein „fehlende Zelle = unzulässig".
[DE-only] (a/b-Tabellen sind deutsche Hersteller-/DIN-Praxis; ÖNorm fordert sie nicht explizit)

### · Gleichmäßigkeit 40:1 entlang Mittellinie
**IMPLEMENTIERT.** `ud = min/max`, Grenze `ud_min_aus_norm(gleichmaessigkeit_max)`
= 1/40 Default (`lux.py:59,69-80,173`). Auf der Mittellinie geprüft via
`lux_punkte(kandidaten, linie, ud_min=...)` (`deckung.py:127`, `lux_nachweis.py:113`).
Verdichtung bis `mitte.erfuellt_ud` (`deckung.py:135-141`).
[AT-verbindlich] EN 1838 §4.2.2 (Ud 1:40). Hinweis: gerechnet über min:max der
diskreten Nachweis-Punkte, kein separater „entlang der Mittellinie"-Gradient.

### · Blendungsgrenzen f(h), Treppe = jeder Winkel
**FEHLT.** Grep `blendung|glare|luminanz|cd/m²` über `src/**` = 0 Treffer. Keine
Begrenzung der Leuchtdichte / kein h-abhängiges Blendungsraster, keine
Sonderbehandlung von Treppen für Abstrahlwinkel.
[AT-verbindlich] EN 1838 §4.1 Tab. (Blendungsbegrenzung) — nicht abgebildet.

### · l = z·h_Piktogramm (z=200 Default)
**IMPLEMENTIERT** (z=200 hinterleuchtet). `erkennungsweite_m = z·h`
(`provider.py:387-390`), z aus `en1838_grundwerte.yaml`. Produktiv als
Deckungs-Radius (`deckungs_zuordnung.py:72`, `HINTERLEUCHTET_DEFAULT=True`
→ 30 m) und als RZ-Abstand im Gang-Fallback (`gang_strategy.py:110`).
z=100 beleuchtet vorhanden, aber Default-Pfad nutzt hinterleuchtet.
[AT-verbindlich] EN 1838 §5.5.

### · Höhenformel h_m ≤ 1,5 + tan(20°)·l
**FEHLT.** Grep `tan.*20|1\.5.*tan|hoehenformel` = 0 Treffer. Montagehöhe kommt
als fester Norm-Wert `montagehoehe_mm` (Floor 2000 mm, `provider.py:141-144`),
keine Ableitung aus der Erkennungsweite/Sichtwinkel.
[AT-Referenzpraxis]/[DE-only] (Sichtwinkel-Höhenformel).

### · Randbereichs-Offset (nur Längsseiten, Stirnseiten bis zur Tür)
**RUDIMENTÄR.** Es gibt einen **umlaufenden** Randstreifen `rand_mm` (Default
500 mm, `lux.py:104,142-147`) — er wird aber undifferenziert auf ALLEN vier
Seiten der bbox abgezogen, NICHT selektiv (Längsseiten vs. Stirnseiten bis zur
Tür). Der Rand gilt zudem nur im Flächen-Raster (`lux_raster`), der
Mittellinien-Nachweis (`lux_punkte`) kennt keinen Rand-Offset. Norm-Bezug in
`provider.antipanik_randstreifen_mm` (`provider.py:194-202`, §4.3.1, 0,5 m) —
existiert als Norm-Wert, wird aber im Nachweis nicht seitenselektiv angewandt.
[AT-verbindlich] EN 1838 §4.2.1/§4.3.1.

### · 1-lx-Band-Verdichtung
**IMPLEMENTIERT.** `verdichte_fluchtweg` (`deckung.py:70-162`): Start-Abstand
photometrisch (`max_leuchtenabstand_mm`), dann Schleife ÷1.3 bis Mittellinie
≥ `ziel` (1 lx) UND halbes Mittenband ≥ ziel/2 (0,5 lx) UND Ud halten
(`deckung.py:119-141`). Mittenband ± Breite/4 entlang lokaler Tangente
(`_nachweis_punkte`, `deckung.py:47-67`).
[AT-verbindlich] EN 1838 §4.2.1.

### · Antipanik 0,5 lx mit 0,5-m-Rand
**IMPLEMENTIERT (Lux) / RUDIMENTÄR (Rand).** `_antipanik_punkte`
(`flaechen_strategy.py:96-122`) verdichtet Raster bis `lux_raster` mit
`ziel_lux=anf.min_lux` (0,5 lx) + Ud erfüllt. Der Rand kommt aus dem
generischen `rand_mm`-Default (500 mm) in `lux_raster` — der Aufruf
(`flaechen_strategy.py:110`) übergibt `rand_mm` NICHT explizit, nutzt also den
500-mm-Default = zufällig §4.3.1-konform, aber nicht aus
`norm.antipanik_randstreifen_mm` gezogen (lose Kopplung). Fläche < Nachweisfenster
→ Fallback auf Norm-Raster (`flaechen_strategy.py:114-115`).
[AT-verbindlich] EN 1838 §4.3.1.

### · ≥ 2 Leuchten je Bereich
**RUDIMENTÄR (nur QA-Warnung, keine Platzierungs-Garantie).** Geprüft in
`validierung.pruefe` Regel 4b (`validierung.py:159-177`): < 2 Leuchten (RZ/SL)
in 30 m Reichweite je Segment → **Warnung, kein Hard-Fail** (Kommentar: „Hard-Fail
folgt später", `:161-162`). Die Platzierung selbst ERZWINGT keine 2 Leuchten je
Bereich; der Wert wird nur reportet.
[AT-verbindlich] EN 50172 / EN 1838 §5.1.8.

---

## Weitere IST-Beobachtungen (belegt)

- **Wartungsfaktor** durchgereicht (`anf.wartungsfaktor`, defensiv `or 1.0`):
  `deckung.py:104`, `lux_nachweis.py:105`, `lux.py:171,221,271`. Default 1,0 =
  no-op solange Enis' Norm-Naht den Wert nicht liefert. Der PDF-Bericht
  hardcodet dagegen `MF=0.80` (`lux_nachweis_bericht.py:41`) — Divergenz
  zwischen Engine-Default (1,0) und Bericht-Anzeige (0,80). [AT-Referenzpraxis]
- **Anisotrope Photometrie mit C-Ebene** korrekt: `_i_cd_vektor` übergibt (γ,C),
  Azimut relativ zur Optik-C0 (`lux.py:163-168,214-216`). Einparametrige
  Callables (Fakes) fallen auf γ-only zurück (`lux.py:43-56`).
- **Extents-Robustheit** gegen Phantom-Koordinaten: Raster-Cap 8 Mio Punkte
  (`lux.py:66,144-145`, `mittellinie.py:28,38-41`).
- **Punktmethode ohne Reflexion** (Reflexion=0, konsistent mit Referenz-Praxis,
  `lux_nachweis_bericht.py:333`). [AT-Referenzpraxis] (Relux/DIALux-Notberechnung).
- **Fluchtweg-Nachweis-Bericht** `lux_nachweis.nachweis_fluchtweg` prüft
  Mittellinie ≥ 1 lx + Mittelfläche ≥ 0,5 lx + Ud ≥ 1:40 (`lux_nachweis.py:122-127`).
  Additiv/Reporting, ändert keine Platzierung.

## Unbelegt (keine Fundstelle)

- Keine — alle Prompt-Punkte konnten mit Beleg bestätigt/widerlegt werden.
