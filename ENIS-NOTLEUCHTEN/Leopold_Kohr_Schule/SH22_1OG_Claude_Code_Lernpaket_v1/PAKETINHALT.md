# Vollständiger Paketinhalt

Dieses Paket enthält 40 Dateien. Es enthält ausschließlich Unterlagen für SH22, 1. OG.

Vier PDFs und eine Original-DXF sind enthalten. JSON-Dateien sind sowohl Klartextdaten als auch ein komprimierter Geometriekontext. Alle Einzeldateien sind über SHA-256 prüfbar.

## 01_PDF

- `01_PDF/SH22_1OG_Gehflaechen_Gruen.pdf`
- `01_PDF/SH22_1OG_Lernbuch.pdf`
- `01_PDF/SH22_1OG_Mauern_Rot.pdf`

## 02_Originalquellen

- `02_Originalquellen/20220225-SH22-LKS-GE-AP-01-01-A-1OG.dxf`
- `02_Originalquellen/Schule_SH22_1_OG.pdf`

## 03_Wissen

- `03_Wissen/ERKENNUNGSREGELN.md`
- `03_Wissen/KOORDINATEN_UND_DATEN.md`
- `03_Wissen/KORREKTUREN_UND_GRENZEN.md`
- `03_Wissen/PRUEFEN_UND_VERGLEICHEN.md`
- `03_Wissen/UMSETZUNG_IN_DER_ENGINE.md`

## 04_Daten

- `04_Daten/ausschnitte.json`
- `04_Daten/datenumfang.json`
- `04_Daten/koordinaten.json`
- `04_Daten/korrekturen.json`
- `04_Daten/lernfaelle.json`
- `04_Daten/prueffaelle.json`
- `04_Daten/quellanker.json`
- `04_Daten/quellen.json`
- `04_Daten/quellentexte.json`
- `04_Daten/quellgeometrie_pdf.json.gz`
- `04_Daten/randsicherungen_quelllinien.json`
- `04_Daten/referenzflaechen_pdf.json`
- `04_Daten/regeln.json`

## 05_Schemas

- `05_Schemas/engine_ergebnis.schema.json`
- `05_Schemas/lernfaelle.schema.json`

## 06_Werkzeuge

- `06_Werkzeuge/ausschnitte_rendern.py`
- `06_Werkzeuge/bewerte_engine_ergebnis.py`
- `06_Werkzeuge/common.py`
- `06_Werkzeuge/dxf_belege_pruefen.py`
- `06_Werkzeuge/koordinaten.py`
- `06_Werkzeuge/pruefe_paket.py`
- `06_Werkzeuge/requirements.txt`

## 07_Pruefung

- `07_Pruefung/PRUEFBERICHT.md`
- `07_Pruefung/quellpruefung.json`
- `07_Pruefung/werkzeugpruefung.json`

## Einstieg und Vollständigkeit

- `CLAUDE_AUFTRAG.md`
- `MANIFEST.json`
- `PAKETINHALT.md`
- `SHA256SUMS.txt`
- `START_HIER.md`

## Lesereihenfolge

`START_HIER.md` → `CLAUDE_AUFTRAG.md` → Lernbuch und `03_Wissen/` → Fälle und Korrekturen in `04_Daten/` → vorhandene Engine untersuchen → Prüfadapter und Ergebnisvergleich.

`referenzflaechen_pdf.json` und Erklärrahmen sind keine vollständige Soll-Raumsegmentierung. Die Original-DXF ist für die tatsächliche Erkennung maßgeblich.
