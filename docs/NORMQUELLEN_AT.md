# Normquellen-Status (Enis) — was liegt vor, was ist belegt, was fehlt

**Stand:** 2026-08-30 · Bestandsaufnahme rein lesend aus `knowledge/`.
Zweck: Trennung **Primärquelle / Sekundärquelle** und **Verbindlichkeitsebene**,
bevor Normwerte in `normwissen/data/` bestätigt oder geändert werden.

Ebenen: **A** verbindliche Rechtsquelle · **B** Richtlinie (OIB) · **C** Norm ·
**D** Fachinformation / Auslegungshilfe. *Eine Fachinformation ersetzt nie eine Norm
oder Rechtsvorschrift.*

## 1. Vorhanden (Original-PDFs, `knowledge/`)

### C — Normen
| Dokument | Ausgabe | S. | Pfad | Hinweis |
|---|---|---|---|---|
| ÖNORM EN 1838 | **2019-11-15** (IDT EN 1838:2013-07, Ersatz für ÖNORM EN 1838:2013-09) | 22 | `knowledge/EN 1838 - Notbeleuchtung 2019 (1).pdf` | Lizenzexemplar; **die im Repo zitierte Ausgabe 2013-09 liegt NICHT vor** |
| OVE E 8101 | 2025-10-01 | 852 | `knowledge/OVE E8101_2025 (1).pdf` | Teil 5-56 „Einrichtungen für Sicherheitszwecke" enthalten |
| OVE E 8101 | 2019-01-01 | 758 | `knowledge/OVE E 8101_2019 (1).pdf` | ältere Ausgabe |
| OVE E 8015 / E 8350 / E 8351 / OVE E 8014 | 2022 / 2017 / 2016 / 2019 | | `knowledge/…` | Randbezug |

### B — OIB-Richtlinien (Ausgabe Mai 2023, komplett RL 1–7 + Sonderrichtlinien)
`knowledge/OIB-Richtlinien/` — notbeleuchtungsrelevant: **RL 2** (Punkt 5.4 +
Tabelle 6), **RL 2-Erläuterungen** (S.48 zu Punkt 5.4), **RL 2.1** (3.6.5),
**RL 2.2** (4.3, 5.5.3, Tab. 3 Zeile 8.2), **RL 2.3** (2.14),
**Begriffsbestimmungen**, **Zitierte Normen und sonstige technische Regelwerke**.
Details: [`OIB_RL2_TABELLE6.md`](OIB_RL2_TABELLE6.md).
Verbindlichkeit entsteht erst durch Übernahme ins Landesbaurecht — in keinem der
Dokumente belegt → offen.

### A — Rechtsquellen (RIS-Ausdrucke)
ETG 1992 · ETV 2002/2010/2020 · ESV 2012 · Nullungsverordnung · Standesregeln.
Keine davon regelt die Erforderlichkeit von Notbeleuchtung direkt.

### D — Fachinformationen
`knowledge/OVE-Fachinformation/` (E01–E13, H02): notbeleuchtungsrelevant **E06**
(Bussysteme), **E07** (Funktionserhalt Leitungsanlagen), **E08** (Arbeitsstätten —
Ausführung von Sicherheitsbeleuchtung und nachleuchtenden Orientierungshilfen,
Ausgabe 2021-04-01).
Weiters `knowledge/extracted/` (38 selbst erzeugte Digests, **Sekundär**) und
Hersteller-Handbücher (Handbuch 2026, GSYSTEMS, Kaufel, licht.wissen 10, ONL).

### Sonderfall — eigene Arbeitskopie, NICHT amtlich
`knowledge/Österreichische Rechtsquelle/RIVOPLAN_Oesterreichische_Rechtsquellen_Notbeleuchtung_AT.pdf`
(Autor RIVOPLAN, erstellt 2026-08-30, 10 S.). Enthält aufbereitete Texte zu
**AStV § 9**, **AStV § 13**, **ASchG §§ 20/21**, **KennV inkl. Anhang 1 Pkt. 1.4**
plus RIS-Gesetzesnummern (ASchG 10008910, AStV 10009098, KennV 10009067 /
BGBl. II Nr. 101/1997). **Sekundärquelle** — die amtlichen RIS-Volltexte fehlen.

### LB-Material
`Leistungsbeschreibung BSP/` (4 PDFs, untracked): `mo-leistungsbeschreibung_Elektro_240718.pdf`
(Elektro-LV, direkter Kandidat), `250116_GU Leistungsbeschreibung.pdf`,
`20241209_E LV Fischa 46.pdf`, `mo-Bau-_und_Ausstattungsbeschreibung_…pdf`.

## 2. Prüfung der aktiven Werte gegen die vorhandene EN-1838-Ausgabe

Geprüft am 2026-08-29 gegen `knowledge/EN 1838 - Notbeleuchtung 2019 (1).pdf`
(PDF-Seite = Norm-Seite + 2).

| Wert in `normwissen/data/` | Fundstelle | Ergebnis |
|---|---|---|
| `z_hinterleuchtet: 200`, `z_beleuchtet: 100` | §5.5, Norm-S.13 | **bestätigt**, wörtlich („z ist eine Konstante: 100 für beleuchtete, 200 für hinterleuchtete Zeichen") |
| Formel `l = z·h`, h = „Höhe des Zeichens" | §5.5, Norm-S.13 | **bestätigt**; Maßeinheit von h und l muss gleich sein |
| `dauer_min: 60` | §4.2.5, §4.3.5, §5.4.5 | **bestätigt** („mindestens 1 h") |
| `lux.rettungsweg: 1.0` | §4.2.1, Norm-S.9 | bestätigt, **aber** gebunden an Wegbreite ≤ 2 m + 50-%-Mittelbereich + Anhang-B-Länderabweichungen — in der YAML nicht modelliert |
| `lux.antipanik: 0.5` | §4.3.1, Norm-S.11 | bestätigt („freie Bodenfläche **im Kernbereich**", Randbereiche 0,5 m ausgenommen — Randbereich fehlt in der YAML). Wortlaut „im Kernbereich" ist die **2019er** Fassung |
| `montagehoehe_min_mm: 2000` | §4.1.1, Norm-S.8 | bestätigt als Wert; Wortlaut ist ein **Erfüllungs-Kriterium**, kein absolutes Minimum — YAML-Kommentar „Hard Floor" ist strenger als die Norm |
| `norm: "ÖNORM EN 1838:2013"` | — | **nicht belegt** — diese Ausgabe liegt nicht vor; vorhanden ist 2019-11-15 |
| `piktogramm_hoehe_default_m: 0.15` | — | **nicht in EN 1838**; Praxiswert aus `_port_source/rz_coverage_oenorm.yaml` |
| `montagehoehe_mm: 2400` (raumtyp_regeln) | — | **unbelegt** — kein Notlicht-Eintrag in `heights_fachpraxis.yaml`; stammt aus der Slice-0-Fake-Fixture |
| `mindest_anzahl: 1` / `4` | — | **Engineering-/Fixture-Annahmen**, keine Normwerte |
| Zuordnung `STIEGENHAUS → sicherheitsleuchte`, Quelle „§4.1" | §4.1.2 b), Norm-S.8 | Art teilweise gestützt („nahe Treppen, um jede Treppenstufe direkt zu beleuchten"); die Regelform „eine Leuchte je Stiegenhaus-Raum" ist Auslegung, Quellenstring zu grob |

## 2a. Entscheidung zur Ausgabe-Bezeichnung (2026-08-30, Owner)

Der String `ÖNORM EN 1838:2013` **bleibt vorerst unverändert**, obwohl im Repo die
Ausgabe 2019-11-15 liegt. Grund: er ist keine reine `normwissen/`-Angelegenheit,
sondern **Naht-Invariante** (`Platzierung.norm_quelle ∈ NormRegelwerk.quellen`) und
hängt an sechs Stellen quer durch fremde Zuständigkeiten:

| Fundstelle | Eigentümer |
|---|---|
| `normwissen/data/en1838_grundwerte.yaml` (`norm:` + 3 `quellen`) | Enis |
| `tests/fixtures/norm_regelwerk_snapshot.json` | 3-Owner (CODEOWNERS) |
| `tests/fixtures/platzierung_4og.json` (5× `norm_quelle`) | 3-Owner (CODEOWNERS) |
| `tests/fakes.py` (`FakeNormProvider`) | Leonis' Test-Double |
| `tests/platzierung/test_flaechen_strategy.py` (harte Assertion) | Leonis |
| `hauptengine/contracts/norm_regelwerk.py` (Default + Docstring) | 3-Owner + `contract_version`-Bump + Schema-Regen |

⇒ Die Umstellung ist ein **eigener koordinierter Slice** (Fixture-Regen aus dem
echten Provider + Leonis-Abstimmung), kein Housekeeping. Bis dahin ist der
Beleg-Status direkt in `normwissen/data/*.yaml` als Kommentar markiert, damit kein
Leser den String für belegt hält. Inhaltlich ist die Deckungsgleichheit gegeben
(2019-11-15 ist IDT mit EN 1838:2013-07) — es geht rein um die **Bezeichnung**.

## 3. Fehlt — kostenlos beschaffbar
1. **AStV, ASchG, KennV inkl. Anhang 1** als amtliche RIS-Ausdrucke (Gesetzesnummern s.o.).
2. Kommentierte AStV der Arbeitsinspektion (nur verlinkt).
3. **OVE-Richtlinie R 12-2** — von RL 2-Erl S.48 ausdrücklich als Anforderungsquelle zitiert; im Repo nur ein Bildausschnitt (`knowledge/extracted/bildlehren/beispiel_OVE_R12-2_Bild8-9.jpg`).
4. Landesbaurecht, das die OIB-Richtlinien verbindlich macht (Verbindlichkeitsanker).

## 4. Fehlt — kostenpflichtig
1. **ÖNORM EN 1838:2025-03-01** — Nachfolgeausgabe der Kernnorm; laut den
   Hersteller-Digests mit platzierungsrelevanten Änderungen.
2. **OVE/ÖVE EN 50172** (2024-11-01) — in EN 1838 §4.1.1 normativ verwiesen **und**
   in RL 2-Erl S.48 gemeinsam mit EN 1838 als Ausführungsanforderung genannt ⇒
   Pflicht-Baustein, nicht optional.
3. Nachrangig: TRVB E 102, TRVB B 108, ÖNORM EN ISO 7010.
