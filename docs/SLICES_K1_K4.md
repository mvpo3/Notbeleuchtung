# Slices K1–K4 — Stapel ab `de31621`

Vier Slices aus Enis' Referenzen, Reihenfolge K1 → K2 → K3 → K4, je Slice ein
eigener Branch auf dem Stand des vorigen gebauten Slice. Diese Datei wächst
entlang des Stapels: je Slice ein Abschnitt mit Befund (gemessen), Regel
(wörtlich), Umsetzung, Test, Blast Radius, Gate, betroffenen fremden Lanes und
offenen Owner-Fragen.

**Basis des Stapels:** `de31621` (Code-Stand `60c671a` = Türstapel `aa05143` +
VOK-a + Darstellungsskripte). Basisläufe: alle 23 Prüfgeschosse (Rennweg 7,
Mollgasse 8, Muthgasse E2–E9) mit `ArchitekturRaumProvider().parse` auf `de31621`,
je Raum Typ, Polygon, Fläche, Nutzungsklasse, Wohnung, Notlicht-Flags, Kaskaden-
Quelle, dazu Türen, Ausgänge, Stempel-Zuordnungen und alle Wandkörper. Die
Messskripte liegen außerhalb des Repos (Scratch).

**Vor K3 im Stapel:**

* **K1 — Möbel sind keine Wände:** Prämisse falsch, nichts gebaut. Bericht auf
  Branch `selman/fix-k1-moebel-keine-wand` (`558dee3`).
* **K2 — Schächte nur mit Beleg:** STOPP (neuer Gate-Verstoß (3) M3 DG2). Bericht
  auf Branch `selman/fix-k2-schacht-beleg` (`381c033`).

K3 baut deshalb direkt auf `de31621`. Die Abschnitte K1 und K2 stehen auf ihren
Branches; diese Datei beginnt auf dem K3-Branch mit K3. K4 baut auf K3
(`f682c77`, Branch `selman/fix-k4-klasse-gang-vorraum`), sein Abschnitt steht
unten.

---

## K3 — Bad und WC aus Sanitärbeleg (Enis Referenz 07)

**Status: GEBAUT.** Regel umgesetzt, K3-Tests grün, Gate ohne neuen Verstoß
(Messung ohne `meta` identisch mit `de31621`), keine Wand verloren, kein
Notlicht-Wechsel. Branch `selman/fix-k3-sanitaer-bad` von `de31621`:
`56fb690` Test (rot), `7f2dd0e` Fix, danach dieser Bericht.

**Review (unabhängig nachgemessen):** Test rot auf `56fb690` (2 ImportError, naht
7 failed), grün auf dem Fix (54 passed); Blast Radius 23/23 mit eigenem Diff
bestätigt (Summen unten stimmen); eigene Gate-Messung: dieselben 2 Verstöße,
ohne `meta` gleich der Bau-Messung, M17 18/18; Platzierung OG3 und Mollgasse
2.OG identisch; Zensus-Plausibilität 184/84 und die 3 Kandidaten bestätigt.
Korrigiert: „Vorlauf ohne Rückkopplung" war ungenau (einmalige Rückkante,
Owner-Frage 9), Duschset-Kommentar (121 : 119).

### Owner-Befund (wörtlich)

> OG3 „UNBEKANNT 6,6 m²" links hat zwei Waschbecken und WC-Symbole, liegt im
> Umriss von top_2, kein Stempel.

### Regel (wörtlich)

> Regel: ein Raum ohne Stempel innerhalb einer Wohnung mit mindestens zwei
> Sanitärobjekten (WC, Waschbecken, Dusche, Badewanne, Bidet) wird BAD; mit
> genau WC oder WC plus Waschbecken wird WC. Sanitärobjekte aus Blocknamen und
> Einbaulayer, wie bei der Fenstererkennung nach Erscheinungsbild. Fliesenbelag
> allein reicht nicht, wie Enis schreibt.
> Der Top-Stempel ist Kontrolle: der Raum muss innerhalb eines
> Wohnungsumrisses liegen, sonst bleibt UNBEKANNT.

**Planer-Präzisierung (verbindlich vorgegeben):** Objekte als Multimenge —
genau {WC} oder genau {WC, Waschbecken} (je eines) → WC; sonst ≥ 2 Objekte →
BAD; sonst unverändert. Nur Räume mit `raum_typ == ""` und ohne zugeordneten
Stempel. „Top-Stempel ist Kontrolle" = der Wohnungsumriss (`top_n`) ist
Kontrolle.

**Lesarten** (je einzeln gekennzeichnet, Owner-Bestätigung erbeten):

* **Executor-Lesart „Objekt":** ein INSERT, dessen Blockname die Art nennt UND
  der auf einem Möbel-/Einbau-/Sanitär-Layer liegt (Rennweg `New_060 Möbel
  Einbau` und `New_065 Möbel Einrichtung` — der Owner nennt beide in K1 als
  „Möbel- und Einbaulayer" —, Mollgasse `07-SAN-…`, Muthgasse `P-SANR-FIXT`).
  Lage = Mitte der Block-Bbox. Nur die Arten der Owner-Liste; Urinal, Spüle,
  Waschmaschine zählen nicht. Die Armatur „Duschset" zählt nicht neben der
  Dusche (Muthgasse: 121 Duschsets neben 119 Duschen).
* **Executor-Lesart „Wohnungsumriss":** die Räume einer Wohnung samt dem, was
  zwischen ihnen und der Gebäudehülle liegt. Geprüft über die Nachbarschaft:
  jeder Nachbarraum bis 500 mm (Wanddicke) gehört zu derselben Wohnung
  (Schacht/Lift `KEIN_RAUM` und Freiflächen `AUSSEN` zählen nicht mit), und
  jede Tür des Raums führt in diese Wohnung. Begründung unten („Diagnose").
* **„Erscheinungsbild" nicht gebaut:** Sanitärobjekte als zerlegte Linien ohne
  Block (Barawitzka `540 Sanitäreinrichtung`) erkennt K3 nicht. Gemessen ohne
  Wirkung auf den 23 Prüfgeschossen und im Gate-Plan (Owner-Frage 2).

### Diagnose Rennweg OG3 `rest_6` (Basis `de31621`)

* Raum `rest_6`, Quelle R (Rest-Stufe), 6,56 m², Typ leer, Klasse `None`,
  Wohnung `None`, Flags 00. Kein Stempel: die zehn Stempel des Geschosses sind
  alle `raum_1` … `raum_10` zugeordnet.
* Im Polygon (Bbox-Mitte im Raum), alle INSERTs auf `New_060 Möbel Einbau`:

  | Block | Bbox | Art |
  |---|---|---|
  | `WC_1_Symbol 10[35]` | 501 × 594 mm | WC |
  | `Shower Kit 27[38]` | 604 × 418 mm | Dusche |
  | `Waschbecken_3 10[56]` | 933 × 776 mm | Waschbecken |
  | `Waschbecken_3 10[57]` | 933 × 776 mm | Waschbecken |

  Dazu eine einzelne LINE auf `New_060 Möbel Einbau_Pen_No__1` (1 212 × 527 mm,
  kein Block), Beschriftungs-MTEXT und Bemaßung. Multimenge {WC 1, Dusche 1,
  Waschbecken 2} → **BAD**. Der Befund (zwei Waschbecken, WC) stimmt; dazu
  kommt eine Dusche.
* Nachbarn: `raum_2` ZIMMER (99 mm), `raum_3` ZIMMER (152 mm), `raum_5` BAD
  (69 mm), `raum_8` WC (100 mm), `rest_5` GANG (0 mm) — alle `top_2`; links die
  Außenwand. Türen: `tuer_9` → `rest_5` (Block, Rolle `None`), `durchgang_4` →
  `raum_8` (blattlos, 1 292 mm, Rolle `None`).
* **„im Umriss von top_2" hängt am Umriss-Begriff.** Die Außenkontur der
  Raumvereinigung von `top_2` ohne Löcher, geschlossen mit ±250 mm (Definition
  aus dem K1-Auftrag, die auch die Darstellung mit ±200 mm zeichnet), deckt
  `rest_6` zu **0 %** (±500 mm: 0 %, ±1 000 mm: 1,9 %, ±2 000 mm: 100 %). Der
  Raum sitzt in einer Bucht von `top_2`, die zur Fassade offen ist; der
  gezeichnete Umriss läuft um ihn herum. In der Sache liegt er in `top_2`: jeder
  Nachbar gehört dazu, die Bucht schließt nur die Außenwand. Daher die
  Nachbarschafts-Lesart oben statt eines Schließ-Maßes.

### Zensus Sanitär-Blocknamen und -Layer (alle drei Familien, Basis-DXF)

INSERTs im Architektur-Raum, Summe über die Geschosse, Namen ohne
ArchiCAD-/Revit-Zähler. „Art" = Ergebnis von `sanitaer.objektklasse`.

| Familie | Blockname | Layer | Anzahl | Art |
|---|---|---|--:|---|
| Rennweg | `Waschbecken_3` | `New_060 Möbel Einbau` / `New_065 Möbel Einrichtung` | 9 / 12 | Waschbecken |
| Rennweg | `Waschbecken_4` | `New_065 Möbel Einrichtung` | 1 | Waschbecken |
| Rennweg | `WC_1_Symbol` | `New_060` / `New_065` | 9 / 9 | WC |
| Rennweg | `WC Disabled` | `New_065` | 1 | WC |
| Rennweg | `Shower Kit` | `New_060` / `New_065` | 6 / 5 | Dusche |
| Rennweg | `Badewanne`, `Badewanne_freistehend` | `New_065` | 2, 1 | Badewanne |
| Rennweg | `Urinal` | `New_065` | 2 | — (nicht in der Liste) |
| Rennweg | Zonenstempel mit Sanitärwort, u. a. `WC__5`, `Bad_WC__3`, `Dusche-H__9` | `New_080 Raumdefinitionen` | 9 | — (kein Einbaulayer) |
| Mollgasse | `07-WC` | `07-SAN-G00-L…-M0` | 59 | WC |
| Mollgasse | `07-WT60`, `07-WT-WC`, `07-WT120`, `07-WT80`, `07-WT_Sonderwunsch…` | `07-SAN-…-M0` | 56, 44, 3, 1, 2 | Waschbecken (`07-WT-WC` = Handwaschbecken im WC) |
| Mollgasse | `07-Badewanne`, `…_175x75`, `…_140x140` | `07-SAN-…-M0` | 18, 1, 1 | Badewanne |
| Mollgasse | `07-Dusche`, `07-Dusche_2`, `07-Dusche 80-100/90-110/90-150` | `07-SAN-…-M0` | 14, 3, 3 | Dusche |
| Mollgasse | `07-WM` / `Spüle` | `07-SAN-…-M0` / `07-SAN-…-Küche` | 45 / 44 | — (Waschmaschine, Küche) |
| Muthgasse | `WC UP-Spülkasten Betätigung vorne - 36 x 49cm` / `36 x 53cm` | `P-SANR-FIXT` | 93 / 43 | WC |
| Muthgasse | `WC UP-Spülkasten … 35 x 55cm` (E2, im Block des Nachbarhauses 109A) | `P-SANR-FIXT` | 2 | nicht gelesen (nur oberste Ebene; außerhalb jedes Raums) |
| Muthgasse | `WC Barrierefrei - WC` | `P-SANR-FIXT` | 1 | WC |
| Muthgasse | `Dusche bodeneben - Ablaufrinne - 1000x1300x90` / `900x1300x90` | `P-SANR-FIXT` | 118 / 1 | Dusche |
| Muthgasse | `2D Waschbecken … Laufen VAL` / `… Pro S`, `Waschbecken 08`, `Waschtisch - 45 x 35cm` | `P-SANR-FIXT` | 72 / 47, 17, 16 | Waschbecken |
| Muthgasse | `HNP_Extern_Duschset` | `P-SANR-FIXT` | 121 | — (Armatur der Dusche) |
| Muthgasse | `Haltegriff gerade`, `Stützklappgriff`, `Winkelgriff` | `P-SANR-FIXT` | 291, 187, 1 | — (Zubehör) |
| Muthgasse | `2D_barrierefrei_WC` / `_Waschtischplatz` / `_Duschplatz` | `A-GENM` | 115 / 135 / 94 | — (Bewegungsfläche, kein Einbaulayer) |
| Muthgasse | Türen `HNP_T_UZ_1-DF … -WT` / `-WTN` | `A-DOOR` | 344 | — (Tür) |
| Barawitzka (Gate-Plan, nicht im 23er-Satz) | keine INSERTs | `540 Sanitäreinrichtung` (zerlegte Linien), `550 Fliesen` | EG 329 Entities | nicht gelesen |

**Plausibilität an den gestempelten Räumen** (dieselben Funktionen, 23
Basisläufe): gestempelte BAD 184 Räume — Regel BAD 166, WC 3 (genau WC bzw.
WC + Waschbecken im Polygon), kein Typ 15; gestempelte WC 84 Räume — Regel WC
82, kein Typ 2. „Kein Typ" heißt: weniger als zwei Objektmitten im Polygon und
nicht genau ein WC. K3 wirkt nur ohne Stempel; an gestempelten Räumen ändert
es nichts.

### Umsetzung

* `src/notbeleuchtung/raumerkennung/sanitaer.py` (neu)
  * `objektklasse(blockname, layer)`: Art aus dem Blocknamen (Waschbecken vor
    WC, weil `07-WT-WC`), nur auf `M.{1,2}BEL|EINBAU|SAN`-Layern, ohne
    `DUSCHSET`.
  * `sanitaerobjekte(plan)`: (Art, Bbox-Mitte) aller INSERTs der obersten
    Ebene des Architektur-Raums.
  * `sanitaer_typ(Counter)`: Multimenge → `WC` / `BAD` / `None` (Präzisierung).
  * `kandidaten(raeume, objekte, gestempelt)`: Typ leer, ohne zugeordneten
    Stempel, Typ aus den Objekten mit Mitte im Polygon.
  * `typisiere_sanitaer(raeume, kand, probe_raeume, probe_tueren)`: Kontrolle
    über `umschliessende_wohnung` in der Probe; setzt am echten Raum nur
    `raum_typ` und Flags über `raumtyp_flags("BAD"/"WC")` — wie ein Stempel;
    `nutzungsklasse` und `wohnung_id` nie. Je Kandidat eine Befundzeile.
* `src/notbeleuchtung/raumerkennung/wohnungsumriss.py` (neu, gemeinsame
  Hilfsfunktion für K3/K4): `umschliessende_wohnung(raum, raeume, tueren)` →
  `(wohnung_id | None, grund)`. Liest `wohnung_id`, Klasse und Türen, setzt
  nichts. `NACHBAR_MM = 500` (Knopf, gemessen).
* `src/notbeleuchtung/raumerkennung/provider.py`
  * Der Block Türzuordnung → Liftschacht-Reste → Durchgänge →
    `typisiere_tueren` → `bilde_wohnungen` steht unverändert in
    `_tueren_und_wohnungen`; die LINIE-Markierung der Zirkulation und
    `flw_enden` (türunabhängig) stehen davor.
  * **Einmaliger Vorlauf (Probe):** gibt es Kandidaten, läuft
    `_tueren_und_wohnungen` einmal als Probe auf `copy.deepcopy` von Räumen
    und Türen; `typisiere_sanitaer` prüft darin den Umriss und typisiert die
    echten Räume; danach läuft `_tueren_und_wohnungen` EINMAL regulär. Klasse
    (statisch `WOHNUNG_PRIVAT`) und Wohnung entstehen dort aus rohen Türen wie
    für jeden gestempelten Raum. Keine Iteration, deterministisch — aber eine
    einmalige Rückkante Probe-Klasse/-Wohnung → Typ → rohe Türrolle
    (Owner-Frage 9). Ohne
    Kandidaten keine Probe (20 der 23 Geschosse); Mollgasse 3.OG läuft mit
    Probe, sein Kandidat bleibt UNBEKANNT, das Ergebnis ist unverändert.
  * Prüfstrecken-Ausgabe `sanitaer_befund` (wie `tuer_warnungen`, kein
    Contract-Feld).
* Die Außenanalyse (Innen-Zonen) läuft vor dem Vorlauf und sieht den Raum noch
  untypisiert. Gemessen ohne Wirkung: `rest_6` (OG3) und `rest_4` (Mollgasse
  2.OG) sind schon auf `de31621` Innen-Zone (Sanitärblock im Polygon,
  `waehle_innen_zonen`).

**Reihenfolge — Vorlauf (i) gewählt, Nachlauf (ii) verworfen (beide gemessen,
in-memory auf `de31621`, Rennweg OG3 und Mollgasse 2.OG):**

| | (i) Vorlauf: Typ vor der Türzuordnung | (ii) Nachlauf: Typ + Klasse nach `bilde_wohnungen` |
|---|---|---|
| OG3 `rest_6` | BAD, `WOHNUNG_PRIVAT`, Wohnung `top_2` | BAD, `WOHNUNG_PRIVAT`, Wohnung `None` |
| Mollgasse 2.OG `rest_4` | BAD, `WOHNUNG_PRIVAT`, Wohnung `top_13` | BAD, `WOHNUNG_PRIVAT`, Wohnung `None` |
| Türrollen | `tuer_9` None → wohnungseingang, `durchgang_4` None → zimmertuer, `tuer_72` None → wohnungseingang | unverändert |
| privater Raum ohne Wohnung | OG3 0 → 0, 2.OG 2 → 2 | **OG3 0 → 1**, 2.OG 2 → 3 |
| sonst (Räume, Flags, Warnungen, Ausgänge, Wohnungen) | unverändert | unverändert |

(ii) hinterlässt ein privates Bad ohne Wohnung. Das ist genau die Gate-Kennzahl
(3) `M4.privatraum_ohne_wohnung` (gezählt wie dort über `PRIVAT_TYPEN`: OG3
0 → 1, ein neuer Verstoß), und eine spätere
Auswertung aus rohen Türen (`wohnungszugehoerigkeit`) stellte das Bad in `top_2`
— zwei Antworten auf Frage (b). (i) lässt Frage (b) bei den rohen Türen.

### Test

* `tests/raumerkennung/test_sanitaer.py` (neu): Multimenge → Typ (10 Fälle),
  Objektart aus den gemessenen Blocknamen und Layern der drei Familien inklusive
  Ausschlüssen (Duschset, Bewegungsfläche `A-GENM`, Tür, Spüle, Waschmaschine,
  Urinal, Zonenstempel), Kandidaten (Stempel, Typ, ein Objekt, Objekt außerhalb),
  Vorlauf setzt nur Typ/Flags und lässt die Probe unberührt, drei Fälle „nicht
  im Umriss → bleibt UNBEKANNT".
* `tests/raumerkennung/test_wohnungsumriss.py` (neu): Bucht an der Fassade
  liegt im Umriss; fremde Wohnung, Erschließung, unbekannter Nachbar nehmen
  heraus; Schacht/Lift/Balkon neutral; Nachbar hinter > 500 mm zählt nicht; Tür
  ins Freie/Unerkannte nimmt heraus; ohne Nachbarn kein Umriss.
* `tests/naht/test_k3_sanitaer_bad.py` (neu, drei echte Parse-Läufe): Rennweg
  OG3 Raum 6,3–6,9 m² an der Stelle von `rest_6` ist BAD, `WOHNUNG_PRIVAT`,
  Flags 00, Wohnung `top_2`, beide Türen mit Rolle; Mollgasse 2.OG BAD in
  `top_13`; Mollgasse 3.OG bleibt UNBEKANNT mit Befundzeile; jeder aus
  Sanitärbeleg typisierte Raum liegt nachher in der Wohnung, deren Umriss ihn in
  der Probe umschloss.
* `tests/plaene.py`: Mollgasse 2.OG/3.OG (getrackt).
* **Rot auf `de31621`** (`56fb690`): `test_sanitaer` und `test_wohnungsumriss`
  ImportError (Module fehlen), `test_k3_sanitaer_bad` 7 failed (79 s).
  **Grün auf `7f2dd0e`:** 47 passed (1 s) + 7 passed (81 s).

### Blast Radius (23 Geschosse, `de31621` → `7f2dd0e`)

Vorher = Basisläufe `de31621`, nachher = 23 echte `ArchitekturRaumProvider().parse`
auf `7f2dd0e` (alle `status ok`, Arbeitsbaum sauber). Räume per IoU ≥ 0,5
zugeordnet; Fläche = Änderung ≥ 0,5 m² oder ≥ 2 %; Notlicht-Flags =
(`ist_fluchtweg`, `ist_communal`); Türen per Lage ≤ 150 mm, Ausgänge ≤ 500 mm;
Wandkörper = Anzahl (Fläche mitverglichen).

| Projekt | Plan | Räume v→n | Typ | Klasse | Fläche | neu/weg | Wohnungen v→n | Einraum v→n | Notlicht-Flags | Türen v→n | Türrolle | Ausgänge v→n | SCHACHT v→n | NISCHE v→n | Wandkörper v→n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mollgasse | 1.KG | 31→31 | 0 | 0 | 0 | 0/0 | 0→0 | 0→0 | 0 | 23→23 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 116→116 |
| Mollgasse | 1.OG | 93→93 | 0 | 0 | 0 | 0/0 | 33→33 | 20→20 | 0 | 112→112 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 338→338 |
| Mollgasse | 2.KG | 30→30 | 0 | 0 | 0 | 0/0 | 1→1 | 1→1 | 0 | 40→40 (+0/−0) | 0 | 1→1 | 1→1 | 0→0 | 144→144 |
| Mollgasse | 2.OG | 98→98 | 1 | 1 | 0 | 0/0 | 33→33 | 18→18 | 0 | 121→121 (+0/−0) | 1 | 1→1 | 1→1 | 0→0 | 354→354 |
| Mollgasse | 3.OG | 65→65 | 0 | 0 | 0 | 0/0 | 26→26 | 15→15 | 0 | 93→93 (+0/−0) | 0 | 4→4 | 0→0 | 0→0 | 239→239 |
| Mollgasse | 4.OG | 53→53 | 0 | 0 | 0 | 0/0 | 15→15 | 7→7 | 0 | 59→59 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 211→211 |
| Mollgasse | DG | 35→35 | 0 | 0 | 0 | 0/0 | 10→10 | 3→3 | 0 | 38→38 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 177→177 |
| Mollgasse | EG | 64→64 | 0 | 0 | 0 | 0/0 | 21→21 | 15→15 | 0 | 102→102 (+0/−0) | 0 | 9→9 | 0→0 | 0→0 | 171→171 |
| Muthgasse | E2 | 108→108 | 0 | 0 | 0 | 0/0 | 22→22 | 8→8 | 0 | 193→193 (+0/−0) | 0 | 1→1 | 2→2 | 0→0 | 737→737 |
| Muthgasse | E3 | 124→124 | 0 | 0 | 0 | 0/0 | 23→23 | 6→6 | 0 | 141→141 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 839→839 |
| Muthgasse | E4 | 120→120 | 0 | 0 | 0 | 0/0 | 21→21 | 5→5 | 0 | 139→139 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 815→815 |
| Muthgasse | E5 | 123→123 | 0 | 0 | 0 | 0/0 | 21→21 | 4→4 | 0 | 144→144 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 1250→1250 |
| Muthgasse | E6 | 122→122 | 0 | 0 | 0 | 0/0 | 22→22 | 4→4 | 0 | 146→146 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 1249→1249 |
| Muthgasse | E7 | 96→96 | 0 | 0 | 0 | 0/0 | 19→19 | 4→4 | 0 | 100→100 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 1029→1029 |
| Muthgasse | E8 | 97→97 | 0 | 0 | 0 | 0/0 | 13→13 | 2→2 | 0 | 112→112 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 994→994 |
| Muthgasse | E9 | 61→61 | 0 | 0 | 0 | 0/0 | 9→9 | 2→2 | 0 | 58→58 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 701→701 |
| Rennweg | DG1 | 15→15 | 0 | 0 | 0 | 0/0 | 1→1 | 0→0 | 0 | 14→14 (+0/−0) | 0 | 2→2 | 2→2 | 0→0 | 194→194 |
| Rennweg | DG2 | 13→13 | 0 | 0 | 0 | 0/0 | 2→2 | 1→1 | 0 | 10→10 (+0/−0) | 0 | 3→3 | 3→3 | 0→0 | 183→183 |
| Rennweg | EG | 24→24 | 0 | 0 | 0 | 0/0 | 2→2 | 1→1 | 0 | 40→40 (+0/−0) | 0 | 5→5 | 1→1 | 0→0 | 192→192 |
| Rennweg | OG1 | 18→18 | 0 | 0 | 0 | 0/0 | 3→3 | 1→1 | 0 | 18→18 (+0/−0) | 0 | 2→2 | 1→1 | 0→0 | 196→196 |
| Rennweg | OG2 | 18→18 | 0 | 0 | 0 | 0/0 | 2→2 | 0→0 | 0 | 22→22 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 177→177 |
| Rennweg | OG3 | 17→17 | 1 | 1 | 0 | 0/0 | 2→2 | 0→0 | 0 | 18→18 (+0/−0) | 2 | 3→3 | 2→2 | 0→0 | 204→204 |
| Rennweg | UG | 24→24 | 0 | 0 | 0 | 0/0 | 4→4 | 3→3 | 0 | 21→21 (+0/−0) | 0 | 2→2 | 1→1 | 0→0 | 187→187 |

**Summen:** 2 Typwechsel, 2 Klassenwechsel, 0 Flächenänderungen, 0 neue / 0
entfallene Räume, Wohnungen und Einraum-Wohnungen in allen 23 Geschossen
unverändert, **0 Notlicht-Flag-Wechsel** (00 ↔ 11: keiner), 3
Türrollen-Wechsel, 0 neue/entfallene Türen, 0 Ausgangs-Änderungen, Wandkörper in
allen 23 Geschossen gleich (Anzahl und Fläche) — **keine Wand verloren**. Je
Raum zusätzlich verglichen: Polygone, Stempel-Zuordnungen und alle Warnungen
(Wohnungsklasse, Ausgang, Fluchtweg, Tür) in 23/23 Geschossen unverändert;
`wohnung_id` ändert sich nur an den zwei typisierten Räumen.

Einzelliste:

* Rennweg OG3 `rest_6` 6,56 m²: — → **BAD**, Klasse `None` → `WOHNUNG_PRIVAT`,
  Wohnung `None` → `top_2`, Flags 00 → 00. `tuer_9` (Bad ↔ `rest_5` GANG) Rolle
  `None` → `wohnungseingang`, `durchgang_4` (WC `raum_8` ↔ Bad, blattlos) `None`
  → `zimmertuer`.
* Mollgasse 2.OG `rest_4` 5,40 m²: — → **BAD**, Klasse `None` →
  `WOHNUNG_PRIVAT`, Wohnung `None` → `top_13`, Flags 00 → 00. `tuer_72`
  (Bad ↔ `raum_53` GANG) Rolle `None` → `wohnungseingang`.

### Zählung über die 23 Geschosse

| Geschoss | BAD | WC | m² | Wohnung nachher | Umriss (Probe) |
|---|--:|--:|--:|---|---|
| Rennweg OG3 | 1 | 0 | 6,56 | `top_2` | `top_2` |
| Mollgasse 2.OG | 1 | 0 | 5,40 | `top_13` | `top_13` |
| übrige 21 Geschosse | 0 | 0 | — | — | — |
| **Summe** | **2** | **0** | **11,96** | | |

**Kein typisierter Raum liegt außerhalb eines Wohnungsumrisses:** beide lagen
in der Probe im Umriss genau einer Wohnung (alle Nachbarn und Türen dort) und
landen im regulären Lauf aus rohen Türen in genau dieser Wohnung.

Mit Sanitärbeleg, aber **UNBEKANNT geblieben** (Kontrolle greift): Mollgasse
3.OG `rest_2` 5,36 m² (Waschbecken 1, Badewanne 1) — Nachbar `raum_12` GANG ohne
Wohnung (Klasse `ALLGEMEIN_ERSCHLIESSUNG`), `raum_9` WC in `top_2`.

Nicht gezählt, weil gestempelt (Planer-Präzisierung „ohne zugeordneten
Stempel"): Rennweg UG `WR-D`, `WR-H`, `WR-H /Umkleide`, `Umkleide-D` (je ein
Waschbecken oder ein WC, Vokabular bei Enis).

### Notlicht-Wirkung je typisiertem Raum

| Raum | Klasse v→n | Flags v→n | Flächenleuchte v→n | Leuchten im Geschoss (`pipeline.run`) |
|---|---|---|---|---|
| Rennweg OG3 `rest_6` BAD | `None` → `WOHNUNG_PRIVAT` | 00 → 00 | 0 → 0 | 7 (5 RZ, 2 SL) → 7, Positionen identisch, 0 im Raum vorher/nachher |
| Mollgasse 2.OG `rest_4` BAD | `None` → `WOHNUNG_PRIVAT` | 00 → 00 | 0 → 0 | 18 (7 RZ, 11 SL) → 18, Positionen identisch, 0 im Raum vorher/nachher |

Die Bedingung „Flächenleuchte entfällt" (`flaechen_strategy.py` Zeilen 162–167:
Klasse `WOHNUNG_PRIVAT` ∧ Flags 00) gilt jetzt für beide Räume, sie entzieht
aber nichts: das Regelwerk liefert für einen untypisierten Raum wie für BAD die
Klassifikation `rz` (`norm.fuer_raum("", False)` = `norm.fuer_raum("BAD",
False)` = rz, EN 1838 § 4.2.1), also keine Flächenleuchte; die
8-m²-Sanitärschwelle (OVE Punkt 1) erreichen 6,56 und 5,40 m² nicht. Kein
GANG/VORRAUM berührt, `bestaetigt_privat` unverändert — kein Notlicht-Entzug
entgegen dem Grundsatz.

### Gate

| | `de31621` (vorher) | `7f2dd0e` (nachher) |
|---|---|---|
| `pruefe_gate(nullmessung_f15d03f, …)` | 2 Verstöße: (3) DG2 `M4.einraum` 0 → 1; (10) Barawitzka ABSTELLRAUM 1,98 m² ohne Tür | **dieselben 2 Verstöße, kein neuer** |
| Messung ohne `meta` | — | **identisch** mit `de31621` (alle Abschnitte: M17, Referenz, OG1, OG3, Barawitzka, DG1, Lift-Info, M1–M4) |
| M17 | 18/18 BESTANDEN | 18/18 BESTANDEN |
| M4 OG3 `privatraum_ohne_wohnung` | 0 | 0 |
| (11) DG1 | 2 Ausgänge, 0 durch den Liftschacht | 2 Ausgänge, 0 durch den Liftschacht |
| `pytest -m gate tests/gate` | 3 passed, 1 xfailed | 3 passed, 1 xfailed, 81 deselected (60 s) |

Messungen: `tests/gate/gate_messung.py --out _arbeit/gate/messung_<sha>.json`
(`de31621` aus dem K1-Lauf, `7f2dd0e` hier, `arbeitsbaum_src_scripts_sauber =
true`, 112 s).

### Fremde Lanes (gemessen, nichts geändert)

* `platzierung/` (Leonis): `pipeline.run(build_default_bundle(), …)` mit dem
  Code `de31621` und `7f2dd0e` — Rennweg OG3 und Mollgasse 2.OG je Leuchten
  (Art, Lage) identisch (Tabelle oben).
* `normwissen/` (Enis): nicht berührt. BAD ist Kanon-Typ; kein neues Vokabular,
  die Vokabular-Fälle (Geschäftslokal, Wohnküche, Wohnbereich, TV Raum,
  Personalräume UG, Schrankr., SR, Aufzug, Schl.) nicht angefasst.
* `hauptengine/contracts/`: nicht berührt (`raum_typ` freier String, keine
  neuen Felder; `sanitaer_befund` ist Prüfstrecken-Ausgabe am Provider).

### Gezielte Tests (`7f2dd0e`)

`pytest tests/raumerkennung tests/naht tests/contract`: **4 failed, 1 128 passed,
8 skipped, 14 xfailed** (20 min 36 s). Die 4 Fehlschläge sind genau die bekannt
roten, vorbestehenden: `test_s7_wohnungsklasse.py::test_keine_leuchten_in_wohnung_privat`
OG1/OG2/DG1 (Board 1, Leonis) und `test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell`.
`ruff check .` ohne Befund. Die volle Suite läuft erst im Output-Schritt.

### Offene Punkte / Owner-Fragen

1. **Lesart Wohnungsumriss bestätigen.** Umgesetzt: Nachbarn bis 500 mm alle in
   derselben Wohnung (Schacht/Lift/Freifläche neutral), jede Tür hinein. Die
   Außenkontur-Definition (±250 mm) deckt `rest_6` zu 0 %, weil die Bucht zur
   Fassade offen ist. K4 („GANG/VORRAUM vollständig innerhalb eines
   Wohnungsumrisses") kann dieselbe Funktion nehmen; ob ein Wohnungsflur mit
   Wohnungseingang zum Stiegenhaus dann „innerhalb" ist, entscheidet K4 — nach
   dieser Lesart wäre er es nicht (Nachbar Stiegenhaus).
2. **„Erscheinungsbild" (zerlegte Linien ohne Block) bauen?** Nur Barawitzka
   zeichnet Sanitärobjekte so (`540 Sanitäreinrichtung`, EG 329 Entities, kein
   INSERT). Gemessen über alle acht Barawitzka-Grundrisse (Basis-Code): genau
   **ein** Kandidat mit solcher Geometrie — 2.DG `rest_3`, 3,48 m², ohne
   Wohnung, 18 Entities; im Gate-Plan EG keiner. Ein Erkenner müsste
   Linienzüge clustern und nach Größe/Form klassifizieren (Vorbild
   `fenster_signatur`), kalibriert an den gestempelten Barawitzka-Bädern.
3. **Mollgasse 2.OG/3.OG: nicht zugeordneter Stempel „BAD 4,71 m²" im
   Rest-Raum.** Beide Räume tragen im Polygon einen Stempel „BAD", den die
   Kaskade keinem Raum zugeordnet hat (`flag = kein_polygon`); der Raum entsteht
   erst in der Rest-Stufe. Nach der Planer-Lesart („ohne zugeordneten Stempel")
   wirkt K3, im 2.OG mit demselben Ergebnis wie der Stempel. Die eigentliche
   Lücke ist die Stempelzuordnung nach der Rest-Stufe — eigener Slice? Im 3.OG
   verhindert der Gang `raum_12` ohne Wohnung die Typisierung; im 2.OG ist
   derselbe Gang (`raum_53`) Teil von `top_13` — das ist eine Frage an die
   Wohnungsbildung, nicht an K3.
4. **Türrolle Bad ↔ GANG = `wohnungseingang`** (`tuer_9` OG3, `tuer_72`
   Mollgasse 2.OG): dieselbe rohe Rolle wie die gestempelte WC ↔ GANG-Tür
   `tuer_8` im selben OG3 (GANG ist statisch Erschließung). Keine Wirkung auf
   Wohnungen, Klassen oder Flags gemessen; Hinweis, kein K3-Thema.
5. **Nicht in der Owner-Liste:** Urinal (Rennweg 2), Spüle, Waschmaschine,
   Zubehör (Duschset, Haltegriffe), Muthgasse-Bewegungsflächen
   (`2D_barrierefrei_*` auf `A-GENM`). Bestätigen, dass keins davon zählt.
6. **Nebenbefunde (nicht K3, gemessen):** Muthgasse E8/E9 `lift_1` (LIFT,
   5,88/5,89 m²) enthält WC, Dusche und Waschbecken — das Liftpolygon deckt eine
   Nasszelle; Mollgasse EG `raum_57` VORRAUM „GARDEROBE" enthält Badewanne, WC
   und zwei Waschtische — das Polygon deckt ein Bad.
7. **„Top-Stempel" wörtlich:** Mollgasse führt eigene Top-Symbole (`00-top`,
   43 Blöcke auf `01-SYM`). Nicht benutzt — Kontrolle ist nach Planer-Lesart der
   Umriss der Wohnung aus rohen Türen (`top_n`).
8. **Verschachtelte Blöcke** werden nicht gelesen (nur oberste Ebene):
   Muthgasse E2 hat 2 WC-Blöcke im eingebetteten Modell des Nachbarhauses
   (`Muth109A_RVT…`), gemessen außerhalb jedes Raums.
9. **Einbahn (Board 7): ist die Probe zulässig?** (Nachtrag Review.) Die Probe
   ist keine Iteration, aber eine einmalige Rückkante: `umschliessende_wohnung`
   liest Klasse und `wohnung_id` der Probe-Nachbarn, entscheidet damit, ob der
   Typ gesetzt wird, und der Typ geht in die rohen Türrollen des regulären
   Laufs ein (`tuer_9`, `tuer_72` → `wohnungseingang`, `durchgang_4` →
   `zimmertuer`). Board 7 sagt „rohe Rolle → Klasse → korrigierte Rolle →
   Fluchtweg, nie zurück". Gemessen: die Probe selbst verändert nichts (Probe
   mit wirkungslosem `typisiere_sanitaer` = Basis `de31621` in OG3 und
   Mollgasse 2.OG, 0 Abweichungen); das ausgelieferte Modell ist ein Fixpunkt
   (`bilde_wohnungen` auf dem Ergebnis nachgerechnet: 0 Klassen-, Wohnungs-,
   Flag- oder Rollen-Abweichungen in OG3, Mollgasse 2.OG und 3.OG); die
   Umriss-Kontrolle auf dem ausgelieferten Modell liefert dieselbe Wohnung wie
   die Probe (`top_2`, `top_13`, 3.OG keine). Die Rückkante wirkt nur als
   Sperre: sagt die Probe „nicht im Umriss", bleibt alles wie auf `de31621`.
   Alternativen: (ii) Nachlauf (gemessen: neuer Gate-Verstoß (3)) oder eine
   Umriss-Kontrolle ohne die Wohnungsbildung (z. B. Top-Symbole, Frage 7).
   K4 sollte `umschliessende_wohnung` erst nach diesem Entscheid über eine
   Probe nutzen.

---

## K4 — Nutzungsklasse für UNBESTIMMT-Gänge und -Vorräume (Owner-Lane)

**Status: STOPP.** Regel umgesetzt, K4-Tests grün, keine Wand verloren, kein
Notlicht-Flag-Wechsel (00 ↔ 11: keiner), Wohnungen unverändert — aber **ein
neuer Gate-Verstoß (6)**: Rennweg OG3 `raum_10` (Gang 9,38 m², R1-Wohnungsflur)
ist jetzt `WOHNUNG_PRIVAT` und behält seine drei eigenen Anker (die Ankerregel
bestätigt ihn nicht, Notlicht bleibt) → „Anker in WOHNUNG_PRIVAT (Rennweg OG3):
3, erwartet: 0". Dazu werden zwei Tests rot, die genau das zusichern
(`test_s7_wohnungsklasse.py::test_og3_keine_anker_in_wohnung_privat`,
`test_soll_rennweg.py::test_keine_anker_in_wohnung_privat`); sie sind nicht
grün gebogen. Branch `selman/fix-k4-klasse-gang-vorraum` von `f682c77`:
`4a578ff` Test (rot), `2241dd1` Fix, danach dieser Bericht. Ein nächster Slice
baut nicht auf K4.

### Owner-Befund (wörtlich)

> DG1 Gang 12,2, DG2 Vorraum 10,8, OG3 Gang 9,4 sind magenta schraffiert,
> Klasse offen.

Gemessen auf `f682c77` (Rennweg): DG1 `raum_4` GANG 12,19 m², DG2 `raum_1`
VORRAUM 10,84 m² (Stempel Garderobe), OG3 `raum_10` GANG 9,38 m² — alle drei
Klasse `None`, Flags 11, Wohnung `top_1`. Der Befund stimmt.

### Regel (wörtlich)

> Regel: liegt ein GANG oder VORRAUM vollständig innerhalb eines
> Wohnungsumrisses (top_n), ist er WOHNUNG_PRIVAT. Liegt er außerhalb jedes
> Umrisses und ist vom Stiegenhaus ohne Wohnungseingang erreichbar, ist er
> ALLGEMEIN_ERSCHLIESSUNG. Alles andere bleibt UNBESTIMMT mit Grund, Notlicht
> bleibt.

**Planer-Präzisierung (verbindlich vorgegeben):** „vollständig innerhalb" = ≥ 98 %
der Raumfläche im Umriss, gemeinsame Hilfsfunktion; ein Mitglied von `top_n`
liegt in `top_n`. Erreichbarkeit über ROHE Türrollen (Ankerregel-Semantik, keine
Klasse). Die Regel setzt nur die Nutzungsklasse (Frage (a)); `wohnung_id` bleibt
(Grundsatz (b)); Notlicht entzieht weiter allein `bestaetigt_privat`.

**Lesarten** (je einzeln, Owner-Bestätigung erbeten):

* **Umriss als Fläche:** Außenkontur ohne Löcher von `unary_union(Räume gleicher
  wohnung_id).buffer(+250).buffer(−250)` — die Definition aus dem K1-Auftrag
  (K1-Nebenbefund). Die Nachbarschafts-Lesart aus K3 (`umschliessende_wohnung`)
  nutzt K4 nicht; auf den 23 Geschossen entscheidet ohnehin die Mitgliedschaft
  (alle 94 Kandidaten haben eine Wohnung, siehe unten).
* **„außerhalb jedes Umrisses"** = höchstens 2 % der Fläche in jedem Umriss
  (spiegelbildlich zu 98 %). Auf den 23 Geschossen ohne Fall.
* **Riegel G3 geht vor:** „in keinem Schritt PRIVAT" (Owner 2026-09-22) gilt auch
  für K4 — ein GANG/VORRAUM mit Hauseingang, Tür ins Freie oder Tür zum
  allgemeinen Nebenraum bleibt im Umriss unbestimmt. Gefunden von der
  Zufallssuche (Topologie 136); auf den 23 Geschossen 4 Räume (unten).
* **Nur, was nach der Klassen-Iteration unbestimmt ist:** K4 läuft einmal nach
  der Wohnungsbildung, die Iteration sieht es nicht.

### Vorher (`f682c77`): die unbestimmten GANG/VORRAUM

**94 Räume** mit Klasse `None` (auf `de31621` dieselben 94; die Zahl 47 aus dem
Auftrag habe ich nicht reproduziert — 81 der 94 sind Muthgasse-Vorräume).
Alle 94 sind Mitglied einer Wohnung (`wohnung_id` aus rohen Türen). Herkunft —
die Owner-Festlegung, die sie bisher offen ließ und die K4 ausdrücklich
überstimmt:

| Herkunft | Anzahl | Owner-Festlegung „bleibt unbestimmt" | K4 → privat | K4 → bleibt |
|---|--:|---|--:|--:|
| Loch: vom Stiegenhaus über keine Tür erreichbar, über rohe Zimmertür an die Wohnung gebunden | 86 | E3 (2026-09-21: „Tür- oder Raumerkennungsloch, kein Klassifikationsproblem"), G1.2 (2026-09-22: gehört zur Wohnung, Klasse offen) | 83 | 3 |
| Loch-GANG R1 (hinter seinen rohen Wohnungseingängen nur Einzelräume): Mollgasse 3.OG `raum_48`, 4.OG `raum_10`, DG `raum_13` | 3 | R1 (2026-09-22: „er selbst bleibt für (a) unbestimmt mit Notlicht") | 2 | 1 |
| R1-Erweiterung A+C, Wohnungsflur hinter der Stiegenhaustür: Rennweg OG3 `raum_10` | 1 | Owner 2026-09-27 („gehört zur Wohnung, ist kein Beleg für eine eigene Wohnung; unbestimmt heißt Notlicht bleibt") | 1 | 0 |
| nur durch eine blattlose Öffnung vom Stiegenhaus getrennt: Rennweg DG1 `raum_4`, DG2 `raum_1`, Mollgasse EG `raum_23`, `raum_55` | 4 | E1 (2026-09-21: „eine blattlose Öffnung schließt keine Wohnung ab") mit dem Fail-Safe-Riegel der Ankerregel („nicht auswertbar" → offen) | 4 | 0 |
| Schritt 3 (Iteration ohne Fixpunkt) | 0 | § 6g Schritt 3 | — | — |
| **Summe** | **94** | | **90** | **4** |

(Die Loch-Zeile zählt die drei R1-Loch-Gänge nicht mit; 86 + 3 + 1 + 4 = 94.)

Räume je Geschoss (ID, Typ, m², Wohnung; **offen** = bleibt unbestimmt):

* Mollgasse 3.Obergeschoß: `raum_48` GANG 4,58 (top_21); `raum_51` VORRAUM 5,41 (top_20)
* Mollgasse 4.Obergeschoß: `raum_10` GANG 5,95 (top_1, **offen**); `raum_12` VORRAUM 2,74 (top_2, **offen**)
* Mollgasse Dachgeschoß: `raum_9` VORRAUM 9,10 (top_7); `raum_12` VORRAUM 7,18 (top_3); `raum_13` GANG 3,44 (top_4)
* Mollgasse Erdgeschoß: `raum_23` VORRAUM 7,91 (top_11); `raum_49` VORRAUM 2,17 (top_20); `raum_55` GANG 8,77 (top_1)
* Muthgasse E2: `raum_2` VORRAUM 4,18 (top_8); `raum_42` VORRAUM 6,55 (top_15); `raum_48` VORRAUM 11,91 (top_17); `raum_51` VORRAUM 9,07 (top_16); `raum_54` VORRAUM 11,56 (top_14); `raum_57` VORRAUM 13,10 (top_13); `raum_59` VORRAUM 10,92 (top_4); `raum_80` VORRAUM 4,73 (top_15)
* Muthgasse E3: `raum_22` VORRAUM 5,06 (top_11); `raum_64` VORRAUM 4,18 (top_6); `raum_67` VORRAUM 9,07 (top_5); `raum_76` VORRAUM 13,10 (top_18); `raum_80` VORRAUM 15,23 (top_22); `raum_83` VORRAUM 3,93 (top_2); `raum_84` VORRAUM 13,10 (top_2); `raum_86` VORRAUM 4,73 (top_4); `raum_87` VORRAUM 3,62 (top_16); `raum_89` VORRAUM 3,86 (top_11, **offen**); `raum_92` VORRAUM 7,06 (top_14); `raum_99` VORRAUM 3,60 (top_13); `raum_102` VORRAUM 11,55 (top_3)
* Muthgasse E4: `raum_47` VORRAUM 4,18 (top_7); `raum_50` VORRAUM 9,07 (top_5); `raum_58` VORRAUM 12,90 (top_12); `raum_60` VORRAUM 4,73 (top_4); `raum_64` VORRAUM 5,06 (top_8); `raum_65` VORRAUM 3,86 (top_8, **offen**); `raum_76` VORRAUM 15,23 (top_18); `raum_80` VORRAUM 13,10 (top_19); `raum_98` VORRAUM 7,06 (top_21); `raum_99` VORRAUM 3,60 (top_6); `raum_101` VORRAUM 3,62 (top_2); `raum_102` VORRAUM 11,55 (top_3)
* Muthgasse E5: `raum_6` VORRAUM 3,68 (top_16); `raum_45` VORRAUM 5,65 (top_11); `raum_54` VORRAUM 5,65 (top_17); `raum_58` VORRAUM 3,80 (top_15); `raum_61` VORRAUM 3,98 (top_15); `raum_65` VORRAUM 4,36 (top_1); `raum_72` VORRAUM 11,28 (top_13); `raum_79` VORRAUM 8,41 (top_6); `raum_89` VORRAUM 7,00 (top_2); `raum_91` VORRAUM 3,65 (top_9); `raum_95` VORRAUM 3,56 (top_10); `raum_99` VORRAUM 5,63 (top_3); `raum_108` VORRAUM 4,47 (top_4)
* Muthgasse E6: `raum_42` VORRAUM 5,65 (top_11); `raum_53` VORRAUM 4,36 (top_1); `raum_60` VORRAUM 11,28 (top_14); `raum_65` VORRAUM 2,25 (top_14); `raum_67` VORRAUM 8,41 (top_9); `raum_77` VORRAUM 3,98 (top_16); `raum_78` VORRAUM 3,80 (top_16); `raum_83` VORRAUM 5,63 (top_17); `raum_86` VORRAUM 3,68 (top_10); `raum_95` VORRAUM 3,65 (top_7); `raum_101` VORRAUM 7,00 (top_2); `raum_108` VORRAUM 3,56 (top_3); `raum_109` VORRAUM 4,47 (top_4); `raum_110` VORRAUM 5,65 (top_6)
* Muthgasse E7: `raum_8` VORRAUM 6,19 (top_1); `raum_23` VORRAUM 4,47 (top_1); `raum_33` VORRAUM 5,65 (top_9); `raum_37` VORRAUM 3,98 (top_8); `raum_44` VORRAUM 11,28 (top_5); `raum_51` VORRAUM 8,41 (top_15); `raum_66` VORRAUM 3,80 (top_8); `raum_75` VORRAUM 5,63 (top_18); `raum_82` VORRAUM 3,68 (top_19)
* Muthgasse E8: `raum_27` VORRAUM 4,47 (top_2); `raum_37` VORRAUM 5,65 (top_6); `raum_41` VORRAUM 3,98 (top_5); `raum_44` VORRAUM 3,80 (top_5); `raum_50` VORRAUM 11,28 (top_2); `raum_57` VORRAUM 8,41 (top_2); `raum_76` VORRAUM 5,63 (top_11); `raum_83` VORRAUM 3,88 (top_13)
* Muthgasse E9: `raum_13` VORRAUM 11,28 (top_1); `raum_18` VORRAUM 4,47 (top_3); `raum_23` VORRAUM 8,41 (top_5); `raum_38` VORRAUM 3,72 (top_7)
* Rennweg DG1: `raum_4` GANG 12,19 (top_1)
* Rennweg DG2: `raum_1` VORRAUM 10,84 (top_1)
* Rennweg OG3: `raum_10` GANG 9,38 (top_1)

### Umsetzung

* `src/notbeleuchtung/raumerkennung/wohnungsumriss.py` (gemeinsame Hilfsfunktion,
  K3-Modul erweitert)
  * `wohnungsumrisse(raeume)`: `{wohnung_id: Umriss}`, Außenkontur ohne Löcher
    der ±`SCHLIESS_MM` (250) geschlossenen Raumvereinigung; liest nur
    `wohnung_id` und Polygone.
  * `anteile_im_umriss(raum, umrisse)`: Flächenanteil je Umriss; ein Mitglied
    liegt in seiner Wohnung ganz (1,0). `VOLL = 0.98`.
* `src/notbeleuchtung/raumerkennung/wohnungsklasse.py:klasse_aus_umriss` — die
  Regel für jeden GANG/VORRAUM mit Klasse `None`: im Umriss (≥ 98 %) →
  `WOHNUNG_PRIVAT`, außer der Riegel G3 greift; außerhalb (≤ 2 %) und
  `ankerurteil` allgemein → `ALLGEMEIN_ERSCHLIESSUNG`; sonst `None` mit Grund.
  Setzt nichts, liest keine Klasse außer der eigenen (`None`).
* `src/notbeleuchtung/raumerkennung/wohnungen.py:bilde_wohnungen` — K4 läuft
  nach dem Setzen von `wohnung_id` und vor `setze_wohnungsflags`; setzt nur
  `nutzungsklasse`. Die Berichtszeilen (`unbestimmt:`, `loch:`, `r1:`,
  `tiebreak:`) werden jetzt nach K4 geschrieben; je K4-Raum kommt eine Zeile
  `k4: <id> — privat|allgemein|offen: <Grund>; vorher unbestimmt: <alter
  Grund>` dazu (Prüfstrecken-Ausgabe, kein Contract-Feld).
* **Einbahn (Board 7):** K4 liest `wohnung_id` (rohe Türen) und die Ankerregel
  (rohe Rollen), schreibt nur die Klasse; daraus folgen wie für jeden Raum
  Flags (`bestaetigt_privat`), korrigierte Rollen, Fluchtweg. Keine Probe, keine
  Rückkante zu den rohen Rollen, keine Iteration (anders als K3, Owner-Frage 9).
* `hauptengine/contracts/`, `platzierung/`, `normwissen/`: nicht berührt.

### Test

* `tests/raumerkennung/test_k4_klasse_umriss.py` (neu, 18 Fälle): Umriss schließt
  Wände und füllt Löcher; Mitglied liegt ganz in seiner Wohnung; Flächenanteile
  1,0 / 1,0 / 0,5 / 0,0; unbestimmtes Mitglied → privat; ohne Wohnung voll im
  Umriss → privat; außerhalb und ohne Wohnungseingang erreichbar → allgemein;
  außerhalb, nur über Wohnungseingang oder gar nicht erreichbar → bleibt;
  teilweise (50 %) → bleibt; Riegel G3 geht vor; liest keine Nachbarklasse;
  nur unbestimmte GANG/VORRAUM; setzt nichts; im Durchlauf: Loch-Vorraum wird
  privat, Flags 11, `k4:`-Zeile, keine `unbestimmt:`-Zeile; Wohnungen gleich.
* `tests/naht/test_k4_klasse_gang_vorraum.py` (neu, drei echte Parse-Läufe):
  DG1 Gang 12,19, DG2 Vorraum 10,84, OG3 Gang 9,38 haben eine Klasse
  (`WOHNUNG_PRIVAT`), Wohnung `top_1` unverändert, Flags 11, `k4:`-Zeile.
* `tests/raumerkennung/test_wohnungsklasse.py::test_k4_zufallssuche` (neu): die
  200 Topologien der Fixpunkt-Suche je mit und ohne K4 — K4 ändert nur die
  Klasse vorher unbestimmter GANG/VORRAUM, Wohnungen gleich, kein Riegel-Raum
  privat, Flags nur 11 → 00 und nur mit `bestaetigt_privat`, wer offen bleibt,
  hat Flags 11. Gemessen: 76 unbestimmte, K4 → 71 privat, 5 offen, **0
  Flag-Wechsel**.
* **Rot auf `f682c77`** (`4a578ff`): `test_k4_klasse_umriss` ImportError
  (`klasse_aus_umriss` fehlt), `test_k4_klasse_gang_vorraum` 3 failed (Klasse
  `None`). **Grün auf `2241dd1`:** 21 passed (10 s).
* **Umgestellte Tests** — sie banden die Festlegungen „Klasse bleibt offen", die
  K4 überstimmt; je Test steht die K4-Erwartung und der alte Grund in der
  `k4:`-Zeile, alle übrigen Zusicherungen (Wohnung, Flags, Wege, Warnzeilen)
  unverändert:
  * `test_wohnungsklasse.py`: `test_nicht_auswertbarer_raum_wird_unbestimmt_…`
    (umbenannt in `…_behaelt_notlicht`), `test_ohne_fixpunkt_im_deckel_…`,
    `test_e5_loch_paar_folgt_rohen_tueren`, `test_e5_keine_wohnung_ohne_eingang_…`,
    `test_nicht_konvergenz_wird_unbestimmt_mit_grund`,
    `test_e5_loch_paar_haengt_nicht_am_etikett` (4), `test_e5_loch_raum_ueber_…`,
    `test_e5_loch_raum_bleibt_offen_…` (2), `test_r10_loch_raum_folgt_rohen_tueren`
    (2), `test_r11_loch_gang_zu_einzelraeumen_…`, `test_r14_ohne_fixpunkt_…`,
    `test_r1ac_wohnungsflur_hinter_stiegenhaustuer_…`, `test_r1ac_loch_gang_…`.
    `test_e5_zwei_fixpunkte_zufallssuche` prüft die Iteration und läuft jetzt
    ohne K4 (K4 hat die eigene Suche oben).
  * `test_s7_wohnungsklasse.py`: `test_kandidatenklasse_ist_fixpunkt_…[og3]`,
    `test_r7_klasse_nach_den_owner_entscheiden[dg2-raum_1]`,
    `test_loch_raum_folgt_rohen_tueren[og3-raum_10]`,
    `test_moll_eg_raum_23_behaelt_seine_wege` (Wege unverändert: ≥ 3
    Stützpunkt-Segmente, ≥ 10 Punkte).
  * **Einzige Notlicht-Wirkung in einem Test:** `test_ohne_fixpunkt_im_deckel_…`
    erzwingt `DECKEL = 1`; der dort unbestimmte Vorraum V wird durch K4 privat,
    und weil die Ankerregel ihn bestätigt (Wohnungseingang mit Blatt, Zimmer in
    der Wohnung), nimmt `bestaetigt_privat` ihm die Flags — dasselbe Ergebnis wie
    ohne Deckel. Auf den 23 Geschossen und in den 200 Zufallstopologien: 0 Fälle
    (Owner-Frage 4).

### Blast Radius (23 Geschosse, `f682c77` → `2241dd1`)

Vorher = die K3-Nachher-Läufe (`7f2dd0e`, src bis `f682c77` nur Kommentare),
nachher = 23 echte `ArchitekturRaumProvider().parse` auf `2241dd1` (alle
`status ok`; Muthgasse E2 lief im ersten Versuch in einen `MemoryError` und
wurde einzeln wiederholt). Zuordnung und Schwellen wie in K3. Zusätzlich 23
erweiterte Läufe auf `f682c77` (Segmente, Anker, korrigierte Rollen,
`bestaetigt_privat`): Räume und Türen darin gleich den K3-Läufen (23/23).

| Projekt | Plan | Räume v→n | Typ | Klasse | Fläche | neu/weg | Wohnungen v→n | Einraum v→n | Notlicht-Flags | Türen v→n | Türrolle | Ausgänge v→n | SCHACHT v→n | NISCHE v→n | Wandkörper v→n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mollgasse | 1.Kellergeschoß | 31→31 | 0 | 0 | 0 | 0/0 | 0→0 | 0→0 | 0 | 23→23 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 116→116 |
| Mollgasse | 1.Obergeschoß | 93→93 | 0 | 0 | 0 | 0/0 | 33→33 | 20→20 | 0 | 112→112 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 338→338 |
| Mollgasse | 2.Kellergeschoß | 30→30 | 0 | 0 | 0 | 0/0 | 1→1 | 1→1 | 0 | 40→40 (+0/−0) | 0 | 1→1 | 1→1 | 0→0 | 144→144 |
| Mollgasse | 2.Obergeschoß | 98→98 | 0 | 0 | 0 | 0/0 | 33→33 | 18→18 | 0 | 121→121 (+0/−0) | 0 | 1→1 | 1→1 | 0→0 | 354→354 |
| Mollgasse | 3.Obergeschoß | 65→65 | 0 | 2 | 0 | 0/0 | 26→26 | 15→15 | 0 | 93→93 (+0/−0) | 0 | 4→4 | 0→0 | 0→0 | 239→239 |
| Mollgasse | 4.Obergeschoß | 53→53 | 0 | 0 | 0 | 0/0 | 15→15 | 7→7 | 0 | 59→59 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 211→211 |
| Mollgasse | Dachgeschoß | 35→35 | 0 | 3 | 0 | 0/0 | 10→10 | 3→3 | 0 | 38→38 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 177→177 |
| Mollgasse | Erdgeschoß | 64→64 | 0 | 3 | 0 | 0/0 | 21→21 | 15→15 | 0 | 102→102 (+0/−0) | 0 | 9→9 | 0→0 | 0→0 | 171→171 |
| Muthgasse | E2 | 108→108 | 0 | 8 | 0 | 0/0 | 22→22 | 8→8 | 0 | 193→193 (+0/−0) | 0 | 1→1 | 2→2 | 0→0 | 737→737 |
| Muthgasse | E3 | 124→124 | 0 | 12 | 0 | 0/0 | 23→23 | 6→6 | 0 | 141→141 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 839→839 |
| Muthgasse | E4 | 120→120 | 0 | 11 | 0 | 0/0 | 21→21 | 5→5 | 0 | 139→139 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 815→815 |
| Muthgasse | E5 | 123→123 | 0 | 13 | 0 | 0/0 | 21→21 | 4→4 | 0 | 144→144 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 1250→1250 |
| Muthgasse | E6 | 122→122 | 0 | 14 | 0 | 0/0 | 22→22 | 4→4 | 0 | 146→146 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 1249→1249 |
| Muthgasse | E7 | 96→96 | 0 | 9 | 0 | 0/0 | 19→19 | 4→4 | 0 | 100→100 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 1029→1029 |
| Muthgasse | E8 | 97→97 | 0 | 8 | 0 | 0/0 | 13→13 | 2→2 | 0 | 112→112 (+0/−0) | 0 | 0→0 | 2→2 | 0→0 | 994→994 |
| Muthgasse | E9 | 61→61 | 0 | 4 | 0 | 0/0 | 9→9 | 2→2 | 0 | 58→58 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 701→701 |
| Rennweg | DG1 | 15→15 | 0 | 1 | 0 | 0/0 | 1→1 | 0→0 | 0 | 14→14 (+0/−0) | 0 | 2→2 | 2→2 | 0→0 | 194→194 |
| Rennweg | DG2 | 13→13 | 0 | 1 | 0 | 0/0 | 2→2 | 1→1 | 0 | 10→10 (+0/−0) | 0 | 3→3 | 3→3 | 0→0 | 183→183 |
| Rennweg | EG | 24→24 | 0 | 0 | 0 | 0/0 | 2→2 | 1→1 | 0 | 40→40 (+0/−0) | 0 | 5→5 | 1→1 | 0→0 | 192→192 |
| Rennweg | OG1 | 18→18 | 0 | 0 | 0 | 0/0 | 3→3 | 1→1 | 0 | 18→18 (+0/−0) | 0 | 2→2 | 1→1 | 0→0 | 196→196 |
| Rennweg | OG2 | 18→18 | 0 | 0 | 0 | 0/0 | 2→2 | 0→0 | 0 | 22→22 (+0/−0) | 0 | 1→1 | 0→0 | 0→0 | 177→177 |
| Rennweg | OG3 | 17→17 | 0 | 1 | 0 | 0/0 | 2→2 | 0→0 | 0 | 18→18 (+0/−0) | 0 | 3→3 | 2→2 | 0→0 | 204→204 |
| Rennweg | UG | 24→24 | 0 | 0 | 0 | 0/0 | 4→4 | 3→3 | 0 | 21→21 (+0/−0) | 0 | 2→2 | 1→1 | 0→0 | 187→187 |

**Summen:** 0 Typwechsel, **90 Klassenwechsel** (alle `None` → `WOHNUNG_PRIVAT`,
alle GANG/VORRAUM), 0 Flächenänderungen, 0 neue / 0 entfallene Räume,
Wohnungen und Einraum-Wohnungen in allen 23 Geschossen unverändert, **0
Notlicht-Flag-Wechsel** (00 ↔ 11: keiner), 0 Türrollen-Wechsel (roh), 0
neue/entfallene Türen, 0 Ausgangs-Änderungen, Wandkörper in allen 23 Geschossen
gleich (Anzahl und Fläche) — **keine Wand verloren**. `wohnung_id` ändert sich an
keinem Raum.

Einzelliste: die 90 Klassenwechsel sind genau die Räume der Liste oben ohne
„offen". Dazu aus den erweiterten Läufen (`f682c77` ↔ `2241dd1`):

| Wirkung | Anzahl | wo |
|---|--:|---|
| korrigierte Türrolle (Fluchtweg/Zirkulation, Frage (a)) `zimmertuer` → `wohnungseingang` | 277 | Muthgasse E2–E9 263, Mollgasse DG 10, 3.OG 3, EG 1 — jede Tür eines Loch-Raums zu seiner Wohnung (Erklärung unten) |
| Fluchtweg-Segmente neu / entfallen / geändert | 0 / 0 / 0 | 23/23 gleich |
| Anker neu / entfallen / verschoben | 0 / 0 / 1 | Rennweg OG3 `rest_3_tuer_tuer_5` (Türanker des Stiegenhauses auf der Schwelle `tuer_5`) aus `raum_10` auf die Stiegenhaus-Seite gezogen (`anker_aus_privat_ziehen`) |
| Anker in `WOHNUNG_PRIVAT` (Punkt ≥ 1 mm innen) | 4 → 27 | +23, alle eigene Anker der neu privaten Gänge: Rennweg OG3 `raum_10` 3, DG1 `raum_4` 5, Mollgasse 3.OG `raum_48` 4, DG `raum_13` 5, EG `raum_55` 6 |
| `bestaetigt_privat` neu / entfallen | 0 / 0 | |
| Fluchtweg-Warnungen neu / entfallen | 1 / 0 | Mollgasse EG: „EG/UG: kein final_exit erreichbar von Tür tuer_29 (Endraum raum_48)" |
| Ausgangs- und Tür-Warnungen | 0 / 0 | |
| Wohnungsklasse-Warnungen | | 90 `unbestimmt:`-Zeilen entfallen, 94 `k4:`-Zeilen neu; `loch:`- und `r1:`-Zeilen der betroffenen Räume nennen „Klasse privat" statt „offen" |

**Korrigierte Rollen, gemessen:** ein Loch-Raum zählte bisher für die
korrigierten Rollen als privat (`wohnungsraeume`: „die unbestimmten LOCH-Räume
… privat"). Mit Klasse `WOHNUNG_PRIVAT`, aber ohne Bestätigung durch die
Ankerregel, ist er jetzt „unbestätigt privat" und zählt nach Option W als
Erschließung („wer Notlicht behält, behält seine Zirkulation") — seine Türen zu
den eigenen Zimmern werden korrigiert `wohnungseingang`, also Startpunkte des
Fluchtwegs. Da ein Loch-Raum vom Stiegenhaus über keine Tür erreichbar ist,
findet kein neuer Start einen Weg: 0 neue Segmente; im Obergeschoss ohne
Warnung, im EG eine Warnung (Mollgasse `tuer_29`). Die rohen Rollen und damit
Wohnungen und Klassen-Iteration ändern sich nicht (Einbahn).

### Zählung über die 23 Geschosse

| Geschoss | unbestimmt vorher | → privat | → allgemein | bleibt | Herkunft (Regel, die sie offen ließ) |
|---|--:|--:|--:|--:|---|
| Mollgasse 3.Obergeschoß | 2 | 2 | 0 | 0 | Loch-GANG R1 (nur Einzelräume dahinter) 1, Loch (über keine Tür erreichbar) 1 |
| Mollgasse 4.Obergeschoß | 2 | 0 | 0 | 2 | Loch-GANG R1 (nur Einzelräume dahinter) 1, Loch (über keine Tür erreichbar) 1 |
| Mollgasse Dachgeschoß | 3 | 3 | 0 | 0 | Loch (über keine Tür erreichbar) 2, Loch-GANG R1 (nur Einzelräume dahinter) 1 |
| Mollgasse Erdgeschoß | 3 | 3 | 0 | 0 | blattlos getrennt 2, Loch (über keine Tür erreichbar) 1 |
| Muthgasse E2 | 8 | 8 | 0 | 0 | Loch (über keine Tür erreichbar) 8 |
| Muthgasse E3 | 13 | 12 | 0 | 1 | Loch (über keine Tür erreichbar) 13 |
| Muthgasse E4 | 12 | 11 | 0 | 1 | Loch (über keine Tür erreichbar) 12 |
| Muthgasse E5 | 13 | 13 | 0 | 0 | Loch (über keine Tür erreichbar) 13 |
| Muthgasse E6 | 14 | 14 | 0 | 0 | Loch (über keine Tür erreichbar) 14 |
| Muthgasse E7 | 9 | 9 | 0 | 0 | Loch (über keine Tür erreichbar) 9 |
| Muthgasse E8 | 8 | 8 | 0 | 0 | Loch (über keine Tür erreichbar) 8 |
| Muthgasse E9 | 4 | 4 | 0 | 0 | Loch (über keine Tür erreichbar) 4 |
| Rennweg DG1 | 1 | 1 | 0 | 0 | blattlos getrennt 1 |
| Rennweg DG2 | 1 | 1 | 0 | 0 | blattlos getrennt 1 |
| Rennweg OG3 | 1 | 1 | 0 | 0 | R1 Wohnungsflur hinter Stiegenhaustür 1 |
| **Summe** | **94** | **90** | **0** | **4** | |

**94 unbestimmt → 90 entschieden (90 privat, 0 allgemein), 4 bleiben.** Keiner
der 94 liegt außerhalb eines Wohnungsumrisses (alle sind Mitglied einer Wohnung
aus rohen Türen), darum greift der Allgemein-Zweig nirgends. Die vier, die
bleiben — alle mit Grund, Flags 11 (Notlicht bleibt):

* Mollgasse 4.OG `raum_10` GANG 5,95 m² (`top_1`, Loch-GANG R1): Riegel G3, Tür
  ins Freie `tuer_8` (Blocktür „block+windfang", roh ohne Rolle).
* Mollgasse 4.OG `raum_12` VORRAUM 2,74 m² (`top_2`): Riegel G3, `tuer_47` —
  roh `balkontuer`.
* Muthgasse E3 `raum_89` VORRAUM 3,86 m² (`top_11`): Riegel G3, `tuer_28` — roh
  `balkontuer`.
* Muthgasse E4 `raum_65` VORRAUM 3,86 m² (`top_8`): Riegel G3, `tuer_29` — roh
  `balkontuer`.

Die drei Owner-Räume: Rennweg DG1 `raum_4` → privat (blattlos getrennt, Mitglied
`top_1`), DG2 `raum_1` → privat (dito), OG3 `raum_10` → privat (R1-Flur, Mitglied
`top_1`); alle Flags 11.

### Notlicht

* **Flags:** 0 Wechsel in 23/23 Geschossen, `bestaetigt_privat` unverändert —
  keiner der 90 wird von der Ankerregel privat bestätigt (85 Loch-Räume „über
  keine Tür erreichbar", 4 „nur blattlos getrennt", OG3 `raum_10` „ohne
  Wohnungseingang erreichbar"). Kein 11 → 00, also auch keiner ohne
  `bestaetigt_privat`.
* **Anker:** keiner entfernt oder neu; die eigenen Anker der fünf neu privaten
  Gänge bleiben (s. o., +23 Anker in `WOHNUNG_PRIVAT`), ein fremder
  Stiegenhaus-Türanker in OG3 wird gezogen, nicht gestrichen.
* **Leuchten** (`pipeline.run`, fremde Lane, nur gemessen, unten): Positionen
  und Arten unverändert.

### Gate

| | `f682c77` (vorher) | `2241dd1` (nachher) |
|---|---|---|
| `pruefe_gate(nullmessung_f15d03f, …)` | 2 Verstöße: (3) DG2 `M4.einraum` 0 → 1; (10) Barawitzka ABSTELLRAUM 1,98 m² ohne Tür | **3 Verstöße: dieselben 2 + (6) „Anker in WOHNUNG_PRIVAT (Rennweg OG3): 3, erwartet: 0"** |
| Messung ohne `meta`, Unterschiede | — | `og3.anker_in_wohnung_privat` 0 → 3, `og3.raeume_wohnung_privat_gang` 1 → 2; alles andere gleich (M17, Referenz, OG1, Barawitzka, DG1, Lift-Info, M1–M4) |
| M17 | 18/18 BESTANDEN | 18/18 BESTANDEN |
| (11) DG1 | 2 Ausgänge, 0 durch den Liftschacht | 2 Ausgänge, 0 durch den Liftschacht |
| `pytest -m gate tests/gate` | 3 passed, 1 xfailed | 3 passed, 1 xfailed, 81 deselected (60 s) |

Messungen: vorher die K3-Messung auf `7f2dd0e` (src bis `f682c77` nur
Kommentare, 2 Dateien), nachher `tests/gate/gate_messung.py --out
_arbeit/gate/messung_2241dd1.json` (`arbeitsbaum_src_scripts_sauber = true`,
102 s). Die drei Anker sind `raum_10_tuer_1`, `raum_10_tuer_3`,
`raum_10_tuer_4` — die eigenen Gang-Anker von `raum_10`
(`provider.py`: Anker für jeden GANG außerhalb `bestaetigt_privat`).

### Fremde Lanes (gemessen, nichts geändert)

* `platzierung/` (Leonis), `pipeline.run(build_default_bundle(), …)`:
  * **Board 1, `test_keine_leuchten_in_wohnung_privat`** (Rennweg, Zählweise
    des Tests): OG1 2 → 2, OG2 2 → 2, OG3 0 → 0, **DG1 1 → 2** (dazu
    `raum_4:rz`). Rot bleiben OG1/OG2/DG1 wie vorher, OG3 bleibt grün;
    `test_soll_rennweg.py::test_soll_keine_leuchten_in_wohnung_privat` (OG3)
    bleibt grün.
  * **Leuchten gleich:** Art und Lage je Leuchte identisch auf den 7
    Rennweg-Geschossen, Mollgasse 3.OG/DG/EG und Muthgasse E9 (beide Stände
    gemessen). Muthgasse E2–E8 nur nachher gemessen; ihre Eingaben an die
    Platzierung sind bis auf die Klasse gleich (Flags, Anker, Segmente, Türen,
    siehe Blast Radius), und die Platzierung liest die Klasse nur zusammen mit
    Flags 00 (`platzierung/flaechen_strategy.py`, Bedingung „Klasse
    `WOHNUNG_PRIVAT` ∧ beide Flags aus") — gleiche Leuchten erwartet, dort nicht
    doppelt gemessen.
  * **Leuchten in den neu privaten Räumen** (standen vorher schon dort, zählen
    jetzt als „in `WOHNUNG_PRIVAT`"): 60 — 21 Rettungszeichen, 39
    Sicherheitsleuchten. Rennweg DG1 `raum_4` 1 RZ; Mollgasse 3.OG `raum_48`
    1 RZ, DG `raum_13` 1 RZ; Muthgasse E2 4, E3 8, E4 2, E5 12, E6 9, E7 12,
    E8 9, E9 1. Rennweg DG2/OG3 und Mollgasse EG: 0.
* `normwissen/` (Enis): nicht berührt; kein Vokabular angefasst (Geschäftslokal,
  Wohnküche, Wohnbereich, TV Raum, Personalräume UG, Schrankr., SR, Aufzug,
  Schl.).
* `hauptengine/contracts/`: nicht berührt (`nutzungsklasse` war schon
  optional; `k4:`-Zeilen sind Prüfstrecken-Ausgabe).

### Gezielte Tests (`2241dd1`)

`pytest tests/raumerkennung tests/naht tests/contract`: **6 failed, 1 148
passed, 8 skipped, 14 xfailed** (20 min 34 s). Vier Fehlschläge sind die bekannt
roten, vorbestehenden (`test_s7_wohnungsklasse.py::test_keine_leuchten_in_wohnung_privat`
OG1/OG2/DG1, Board 1/Leonis; `test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell`).
**Neu rot, zwei:** `test_s7_wohnungsklasse.py::test_og3_keine_anker_in_wohnung_privat`
und `test_soll_rennweg.py::test_keine_anker_in_wohnung_privat` — beide „Anker in
WOHNUNG_PRIVAT: `raum_10_tuer_1`, `raum_10_tuer_3`, `raum_10_tuer_4`", derselbe
Befund wie Gate (6). `ruff check .` ohne Befund. Die volle Suite läuft erst im
Output-Schritt.

### Offene Punkte / Owner-Fragen

1. **STOPP-Grund: Anker in einem privat gewordenen Gang (Gate (6)).** K4 macht
   Gänge privat, denen die Ankerregel nichts entzieht; nach dem Grundsatz
   behalten sie Flags, Anker und Leuchten. Gate (6) und die zwei roten Tests
   sichern dagegen „kein Anker in `WOHNUNG_PRIVAT`" (Rennweg OG3). Gemessen:
   alle 23 neuen Anker in `WOHNUNG_PRIVAT` sind eigene Anker von fünf Gängen
   (Rennweg OG3 `raum_10` 3, DG1 `raum_4` 5, Mollgasse 3.OG `raum_48` 4, DG
   `raum_13` 5, EG `raum_55` 6); Vorräume tragen keine eigenen Anker. Wege:
   (A) Zählweise von (6) und den beiden Tests auf den Entzug beschränken
   (Anker in `bestaetigt_privat`-Räumen oder fremde Anker) — Gate-/Test-Regel,
   Board; (B) K4 nicht auf Gänge anwenden, die die Ankerregel „ohne
   Wohnungseingang erreichbar" nennt (R1-Flur OG3) — dann bekommt der
   Owner-Raum OG3 Gang 9,4 keine Klasse, gegen den Befund; (C) die Anker der
   K4-Räume streichen — Notlicht-Entzug gegen den Grundsatz, nicht empfohlen.
2. **Korrigierte Rollen der Loch-Räume (277 Türen).** Bisher zählte ein
   Loch-Raum für Fluchtweg/Zirkulation als privat; privat geworden, aber
   unbestätigt, zählt er nach Option W als Erschließung, seine Türen zur eigenen
   Wohnung werden korrigiert `wohnungseingang`. Gemessen ohne Segment- oder
   Ankerwirkung, eine neue Warnung (Mollgasse EG `tuer_29`). Soll ein
   K4-privater Loch-Raum für `wohnungsraeume` weiter als privat zählen (wie
   vorher), oder gilt Option W?
3. **Riegel G3 vor K4, Balkontür.** Vier Räume bleiben unbestimmt, weil G3 sie
   sperrt — drei davon nur wegen einer rohen `balkontuer` (G3 zählt jede Tür
   nach AUSSEN, die Asymmetrie steht in `riegel_nie_privat`). Soll eine
   Balkontür K4 sperren? Ohne sie würden Mollgasse 4.OG `raum_12`, Muthgasse E3
   `raum_89`, E4 `raum_65` privat (Notlicht bliebe, keine Bestätigung).
   Mollgasse 4.OG `raum_10` hat eine rollenlose Blocktür nach AUSSEN
   („block+windfang") im Obergeschoss — Türerkennung prüfen?
4. **Schritt 3 und K4.** Ein Raum, den die Iteration ohne Fixpunkt offen lässt
   („im Zweifel Notlicht"), wird durch K4 privat; bestätigt ihn die Ankerregel,
   entzieht `bestaetigt_privat` ihm das Notlicht. Nur synthetisch gesehen
   (`test_ohne_fixpunkt_im_deckel_…` mit erzwungenem Deckel 1); auf den 23
   Geschossen und in 200 Zufallstopologien 0 Fälle. Gewollt, oder soll K4 nie
   entziehen?
5. **Zahl 47.** Gemessen sind 94 unbestimmte GANG/VORRAUM auf `f682c77` und
   `de31621` (Muthgasse 81, Mollgasse 10, Rennweg 3). Woher die 47 stammen,
   habe ich nicht gefunden.
6. **Zwei Umriss-Begriffe.** K3 prüft „im Umriss" über die Nachbarschaft
   (`umschliessende_wohnung`, für Räume ohne Wohnung), K4 über die Fläche
   (Planer-Präzisierung). Auf den 23 Geschossen entscheidet in K4 nur die
   Mitgliedschaft. Zusammenführen, sobald ein Fall ohne Wohnung auftaucht?
