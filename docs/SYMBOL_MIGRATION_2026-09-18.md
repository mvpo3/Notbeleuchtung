# Symbol- und Vorlagen-Migration — Phase A (2026-09-18)

Owner-Auftrag: die neue Symbolbibliothek `CAD_Symbole/Notbeleuchtungssymbole_neu+.dxf`
und die neue Planvorlage `Vorlagen-Legende/Notbeleuchtungspläne-Vorlage.dxf` sind ab
jetzt die EINZIGEN Quellen — alte Symbole/Fallbacks sind entfernt (Git-Historie =
Backup). Grundprinzip: **Erscheinungsbild ist Wahrheit, Metadaten sind Hinweis.**

## Symbol-Registry

Die zentrale Symbolzuordnung ist das Paar:

- `src/notbeleuchtung/symbols/schrack_symbol_mapping.yaml` — catalog_key →
  Blockname + `scale_abs` (Weltgrößen-Kalibrierung),
- `src/notbeleuchtung/symbols/orientation.py::_BLOCK_BASE_DEG` — gemessene
  Basisorientierung (lokaler Pfeilvektor) je Block bei Rotation 0.

Basispunkte: alle Blöcke werden beim Import auf ihr Extents-Zentrum normalisiert
(`library._normalize_block_origin`, NUR Top-Block — die frühere rekursive
Kind-Zentrierung zerriss die RIVO-Komposition aus verschachteltem Läufer/Pfeil).

## Mapping alt → neu

| catalog_key | alter Block | neuer Block | scale_abs | Weltgröße | Pfeilvektor lokal |
|---|---|---|---|---|---|
| notlicht_ks_stiege(+_unten, kw_garage) | „…- Richtungspfeil nach unten" | `RIVO-SIBEL-ARR-down` | 36,0 | ≈636 mm | (0,−1) → Basis 270° |
| notlicht_ks_stiege_links | „…-Richtungspfeil nach links" | `RIVO-SIBEL-ARR-left` | 36,0 | ≈636 mm | (−1,0) → Basis 180° |
| notlicht_ks_stiege_rechts | „…-Richtungspfeil nach rechts" | `RIVO-RZ-ARR_right` | 1,372 | ≈636 mm | (+1,0) → Basis 0° |
| sicherheitsleuchte_aufheller | „Aufheller Notbeleuchtung" (grün via BYLAYER) | `Aufheller Notbeleuchtung` (**Owner-Blau bleibt**) | 52,5 | ≈97 mm Ø | — |
| sicherheitsleuchte_spot | „Spot Notbeleuchtung" | `Spot Notbeleuchtung` | 54,4 | ≈97 mm Ø | — |
| antipanik_leuchte | „Notbeleuchtung- Antipanikleuchte" | `Antipanikleuchte-RIVO` | 46,0 | ≈539 mm | — |
| gruppenbatterie_anlage | „Gruppenbatterie" | `Gruppenbatterie-Verteiler` | 25,25 | ≈430 mm | — |
| vorlage_legende | „Vorlage_Legende" | `Vorlage_Legende` (unverändert) | — | — | — |

Skalen kalibriert an den dominanten INSERT-Skalen der Owner-Erklärungspläne
(`knowledge/Pläne zeichnen Wissen/Mollgasse-Notbeleuchtungserklärung/`, alle 6
Geschosse gemessen). `inserter.DE_GLOBAL_SCALE` (185) bleibt nur als Fallback für
Einträge ohne `scale_abs`.

## Entfernt (kein Fallback)

- `CAD_Symbole/Notbeleuchtungssymbole.dxf` (git rm; .gitignore-Whitelist umgestellt).
- Blau→BYLAYER-Farb-Umschreibung in `library.py` (hätte den Owner-blauen Aufheller
  grün gefärbt) — die neuen Blöcke tragen ihre Farben explizit.
- Gelber SL-Zwilling-Layer (`library.SAFETY_LAYER_SL`,
  `din_SIBEL_10_emergency_lighting_yellow`) + `render_dxf(rz_sl_farbtrennung=…)`:
  ALLE Symbole liegen auf dem EINEN Notbeleuchtungs-Layer der Vorlage
  (`din_SIBEL_10_emergency_lighting`, true_color 0x1EB350). Ausnahme: der
  String „…_yellow" lebt als FREMD-Konvention im din-Referenzplan-Leser
  (`scripts/plan_pruefen._REF_LAYER_KIND`) weiter.
- Hartkodierte Alt-Block-Maße im Renderer (Gruppenbatterie-Tiefe 4,46 → aus
  Registry; `_LEGENDE_BLOCKS` → neue Blocknamen).

## Vorlage

`Vorlagen-Legende/Notbeleuchtungspläne-Vorlage.dxf` ist derselbe Pfad, den der
Renderer schon lud (`blatt_vorlage_pfad()`); der Owner hat die neue Fassung
in-place geliefert (jetzt versioniert). Inhalt liegt im Paperspace Layout1
(Modelspace leer): Blattrahmen, Schriftfeld (reine TEXT-Entities, keine ATTDEFs),
Legende mit 8 Zeilen aus den neuen Blöcken (Pfeil unten/links/rechts, Aufheller,
Antipanikleuchte, RZ-beidseitig [= 2× left, eine gespiegelt], Gruppenbatterie-
Verteiler, Spot-Aufheller), Haupt-Viewport, Rivoplan-Logo.

## Guard

`tests/render/test_migration_guard.py`: kein alter Blockname, kein alter
Bibliothekspfad, keine SL-Zwilling-Konstante, kein `rz_sl_farbtrennung` in
src/tests/scripts (docs/ ausgenommen — dieses Dokument IST das Mapping alt→neu);
Registry löst jeden Typ auf; Rotations-Algebra Basis+Transformation=Ziel.

## Verifikation (Prüfstrecke, 2026-09-18)

`scripts/plan_pruefen.py` auf `Projekte/_eingang/Mollgasse_EG.dxf` + voller
Pipeline-Render (`Projekte/_ergebnis/Mollgasse_EG/notbeleuchtung_phaseA.dxf|_plan.pdf`):
53 Symbol-INSERTs = ausschließlich neue Blöcke (RIVO-SIBEL-ARR-down 19, -left 4,
RIVO-RZ-ARR_right 4, Aufheller 26), alle auf `din_SIBEL_10_emergency_lighting`,
0 Alt-Blöcke im Output, Blatt + Vorlagen-Legende gezeichnet. Volle Suite 1389 grün.

Offene Punkte: `knowledge/notbeleuchtung/offene_fragen.md`.
