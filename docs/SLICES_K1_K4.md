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
Branches; diese Datei beginnt auf dem K3-Branch mit K3.

---

## K3 — Bad und WC aus Sanitärbeleg (Enis Referenz 07)

**Status: GEBAUT.** Regel umgesetzt, K3-Tests grün, Gate ohne neuen Verstoß
(Messung ohne `meta` identisch mit `de31621`), keine Wand verloren, kein
Notlicht-Wechsel. Branch `selman/fix-k3-sanitaer-bad` von `de31621`:
`56fb690` Test (rot), `7f2dd0e` Fix, danach dieser Bericht.

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
  * **Vorlauf ohne Rückkopplung:** gibt es Kandidaten, läuft
    `_tueren_und_wohnungen` einmal als Probe auf `copy.deepcopy` von Räumen
    und Türen; `typisiere_sanitaer` prüft darin den Umriss und typisiert die
    echten Räume; danach läuft `_tueren_und_wohnungen` EINMAL regulär. Klasse
    (statisch `WOHNUNG_PRIVAT`) und Wohnung entstehen dort aus rohen Türen wie
    für jeden gestempelten Raum. Keine Iteration, deterministisch. Ohne
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
